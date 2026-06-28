# Heap buffer overflow in TFLite FullyConnectedPerChannel via WebNN quantized GEMM with wrong per-axis quantization dimension

| Field | Value |
|-------|-------|
| **Issue ID** | [493319454](https://issues.chromium.org/issues/493319454) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>WebML |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | we...@intel.com |
| **Created** | 2026-03-17 |
| **Bounty** | $43,000.00 |

## Description

## Title

Heap buffer overflow in TFLite FullyConnectedPerChannel via WebNN quantized GEMM with wrong per-axis quantization dimension

## Summary

The WebNN-to-TFLite translation layer fuses a quantized GEMM into TFLite's FULLY\_CONNECTED operator without validating that the weight tensor's per-channel quantization axis is dimension 0 (output channels). An attacker can supply a weight tensor with per-channel quantization along dimension 1 (input channels) instead, causing `PrepareImpl` to allocate per-channel multiplier and shift arrays sized to the input channel count rather than the output channel count. When the kernel evaluates, it iterates over output channels and reads past the end of those arrays, producing a heap-buffer-overflow in the GPU process. Affected platforms: all where the TFLite WebNN backend is active (Linux, ChromeOS, Android by default; Windows and macOS as a fallback). No special GPU hardware is required.

## Bisect

### TFLite upstream — FullyConnectedPerChannel introduced

- Commit: `310635cc811ae3a64b3abc184885f6769c84f4d7`
- Date: 2022-06-12
- Author: A. Unique TensorFlower
- Subject: TFLite FC Layer Per-channel quantization (Full-Integer i8xi8->i8 or i16xi8->i16)
- Piper: PiperOrigin-RevId: 454517886
- URL: <https://github.com/tensorflow/tensorflow/commit/310635cc811ae3a64b3abc184885f6769c84f4d7>

This commit introduced per-channel quantization for FULLY\_CONNECTED in a single change: `PrepareImpl` allocates `per_channel_output_multiplier` and `per_channel_output_shift` arrays sized to `filter->dims->data[quantized_dimension]`, with only a self-referential consistency check (`scale->size == filter->dims->data[quantized_dimension]`) and no enforcement that `quantized_dimension == 0`. The optimized `FullyConnectedPerChannel` kernel then iterates over `filter->dims->data[0]` (output channels) elements, causing a heap OOB read when `quantized_dimension != 0` and dim 0 > dim quantized\_dimension.

### Became web-reachable

- Commit: `6e5458b43fdc3685cb17664e6709bd79a97dfb36`
- Date: 2025-06-20
- Author: Junwei Fu ([junwei.fu@intel.com](mailto:junwei.fu@intel.com))
- Subject: webnn: Fuse quantized GEMM into TFLite FULLY\_CONNECTED
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/6641102>

This commit added quantized GEMM fusion in the WebNN TFLite graph builder without validating that the weight tensor's per-channel quantization axis is dimension 0.

## Root Cause

WebNN's `dequantizeLinear` allows per-channel quantization where the scale tensor has a non-unit dimension indicating the quantization axis. When fusing a quantized GEMM into TFLite's `FULLY_CONNECTED`, `CanFuseQuantizeAndGetOutput(const mojom::Gemm&)` checks only whether B's scale has more than one element and whether `bTranspose` is true:

```
// services/webnn/tflite/graph_builder_tflite.cc:2072-2083
size_t number_of_b_scale =
    GetOperand(b_dequantize.scale_operand_id).descriptor.NumberOfElements();
const bool per_channel_quantization = number_of_b_scale != 1;
if (per_channel_quantization && !gemm.b_transpose) {
  return std::nullopt;
}

```

There is no validation that B's quantization axis will map to TFLite FULLY\_CONNECTED's filter dimension 0 (output channels). If B has shape `[N, K]` and its scale has shape `[1, K]`, `SerializeQuantizeParams` computes the quantization axis by scanning the scale shape for the non-unit dimension, arriving at axis 1:

```
// services/webnn/tflite/graph_builder_tflite.cc:7001-7009
for (size_t i = 0; i < scale_shape.size(); ++i) {
  if (scale_shape[i] != 1) {
    axis = (input_rank - scale_shape.size()) + i;   // yields axis = 1
  }
}

```

TFLite's `fully_connected::PrepareImpl` validates only that the scale array length matches the filter size along the declared quantization dimension, which is a self-consistent but semantically wrong check:

```
// third_party/tflite/src/tensorflow/lite/kernels/fully_connected.cc:453-463
TF_LITE_ENSURE_EQ(context, affine_quantization->scale->size,
                  filter->dims->data[affine_quantization->quantized_dimension]);
// ...
data->per_channel_output_multiplier.resize(per_channel_quantization_size);
data->per_channel_output_shift.resize(per_channel_quantization_size);

```

For a filter of shape `[1024, 2]` with `quantized_dimension = 1`, the arrays are allocated with size 2. The optimized `FullyConnectedPerChannel` kernel then passes these 2-element arrays as per-row multipliers to the ruy GEMM backend, which expects 1024 entries (one per output row). The ruy kernel reads well past the allocated buffer.

## Reproduce

Tested at commit `3ad31ba232d9a804b4de78d788e391f82b40a906`. No source modifications required.

Build:

```
autoninja -C out/asan-release chrome

```
### Windows

```
ASAN_OPTIONS=detect_odr_violation=0 out/asan-release/chrome.exe ^
  --no-sandbox ^
  --enable-features=WebMachineLearningNeuralNetwork ^
  --disable-features=WebNNOnnxRuntime ^
  --user-data-dir=%TEMP%\poc-tflite005 ^
  --enable-logging=stderr ^
  poc.html

```
### Linux

```
out/asan-release/chrome \
  --no-sandbox \
  --enable-features=WebMachineLearningNeuralNetwork \
  --enable-logging=stderr \
  poc.html

```

The GPU process crashes within seconds. ASAN reports a heap-buffer-overflow READ of size 32 in `ruy::Kernel8bitAvx2Impl`, called from `FullyConnectedPerChannel`. The complete ASAN log is attached in `issue_tflite005/asan.log`.

```
==23132==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x1254fc5da8af
READ of size 32 at 0x1254fc5da8af thread T23
    #0 ruy::Kernel8bitAvx2Impl<32>           kernel_avx2_fma.cc:359
    #5 GemmImplUsingRuy::Run                 cpu_backend_gemm_ruy.h:141
    #6 optimized_integer_ops::FullyConnectedPerChannel  fully_connected.h:95
    #7 fully_connected::EvalQuantized<1>     fully_connected.cc:1510
    #8 fully_connected::Eval<1>              fully_connected.cc:1795
    #12 webnn::tflite::GraphImplTflite::ComputeResources::DoDispatch  graph_impl_tflite.cc:328

0x1254fc5da8af is located 1 bytes before 8-byte region
allocated by thread T23 here:
    #1 std::vector<int>::resize              vector.h:1362
    #2 fully_connected::PrepareImpl          fully_connected.cc:463

SUMMARY: AddressSanitizer: heap-buffer-overflow ruy::Kernel8bitAvx2Impl

```
## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [poc.html](attachments/poc.html) (text/html, 3.7 KB)
- [asan_linux.log](attachments/asan_linux.log) (text/plain, 15.0 KB)
- [asan.log](attachments/asan.log) (text/plain, 28.5 KB)

## Timeline

### dr...@chromium.org (2026-03-17)

Reproduces in M146.

### re...@chromium.org (2026-03-17)

Ningxin, please have someone on your team take a look at this.

### ni...@intel.com (2026-03-18)

@we...@intel.com will help on this issue, thanks!

### ni...@intel.com (2026-03-18)

The per-channel fully connected reference kernel also requires the quantization dimension to be 0. [FullyConnectedPerChannel](https://source.chromium.org/chromium/chromium/src/+/main:third_party/litert/src/tflite/kernels/internal/reference/integer_ops/fully_connected.h;l=68;drc=9213607704a73d1e877921d0454abb11f761bdcc) indexes `output_multiplier` and `output_shift` arrays through output channels, e.g. for a 2D output in shape of [batch, output\_channels].

```
  const int output_depth = output_shape.Dims(output_dim_count - 1);
  ...
  for (int b = 0; b < batches; ++b) {
    for (int out_c = 0; out_c < output_depth; ++out_c) {
      ...
      int32_t acc_scaled = MultiplyByQuantizedMultiplier(
          acc, output_multiplier[out_c], output_shift[out_c]);

```

However [PrepareImpl](https://source.chromium.org/chromium/chromium/src/+/main:third_party/tflite/src/tensorflow/lite/kernels/fully_connected.cc;l=462;drc=93436b403fc528e47b9352057bacb391e87c92b8) allocates `output_multiplier` and `output_shift` arrays in size of `filterShape[quantized_dimension]`. e.g. for a 2D filter in shape of [output\_channels, input\_channels], if `quantized_dimension == 1` and `input_channels < output_channels`, it causes OOB read.

For per-channel quantized gemm, WebNN TFLite backend should reject fusing (and fall back to unfused operators path) if the quantized dimension of filter (operand B) is not 0.

I am not sure this restriction should be also checked at TFLite side, say PrepareImpl returns an error if this check fails?

### ch...@google.com (2026-03-18)

Setting milestone because of s0/s1 severity.

### re...@chromium.org (2026-03-19)

> I am not sure this restriction should be also checked at TFLite side, say PrepareImpl returns an error if this check fails?

We can work around the lack of a check in TFLite with checks in WebNN but and also propose adding a check to TFLite's prepare steps to catch the unsupported case.

### dx...@google.com (2026-03-19)

Project: chromium/src  

Branch:  main  

Author:  Wei Wang [wei4.wang@intel.com](mailto:wei4.wang@intel.com)  

Link:    <https://chromium-review.googlesource.com/7673406>

[WebNN] Reject fusing per-channel quantized gemm if the quantized dimension of filter is not 0

---


Expand for full commit details
```
     
    The FULLY_CONNECTED's underlying kernels expect the per-channel 
    quantization axis to be the output channel(axis 0). So reject 
    fusing per-channel quantized gemm and fall back to the unfused 
    operators path if the quantized dimension of filter is not 0. 
     
    Bug: 493319454 
    Change-Id: Ib7e1236a535dc6a34d3ff9b9f0124a101bd89dbf 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7673406 
    Reviewed-by: Phillis Tang <phillis@chromium.org> 
    Commit-Queue: Wang, Wei4 <wei4.wang@intel.com> 
    Reviewed-by: Hu, Ningxin <ningxin.hu@intel.com> 
    Cr-Commit-Position: refs/heads/main@{#1601718}

```

---

Files:

- M `services/webnn/tflite/graph_builder_tflite.cc`

---

Hash: [fc10b0d6304d7d8f31fea83811aa673a7f13f720](https://chromiumdash.appspot.com/commit/fc10b0d6304d7d8f31fea83811aa673a7f13f720)  

Date: Thu Mar 19 03:00:51 2026


---

### cl...@appspot.gserviceaccount.com (2026-03-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6292575979864064.

### ch...@google.com (2026-03-19)

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to stable (M146) because latest trunk commit (1601718) appears to be after stable branch point (1582197).

Requesting merge to beta (M147) because latest trunk commit (1601718) appears to be after beta branch point (1596535).

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### re...@chromium.org (2026-03-19)

Updated milestone and merge request because WebNN is not enabled on M-146. This only needs to be merged to M-147.

**Which CLs should be backmerged?**  

<https://chromium-review.googlesource.com/7673406>

**Has this fix been verified on Canary to not pose any stability regressions?**  

Yes, ClusterFuzz has verified the fix.

**Does this fix pose any potential non-verifiable stability risks?**  

No.

**Does this fix pose any known compatibility risks?**  

This reduces the set of models that WebNN declares it can execute, but those models didn't work anyways. No compat risk given this is all still in Origin Trial.

**Does it require manual verification by the test team?**  

No.

### ch...@google.com (2026-03-20)

Merge review required: M147 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### re...@chromium.org (2026-03-20)

**Why does your merge fit within the merge criteria for these milestones?**  

It is a security issue.

**What changes specifically would you like to merge? Please link to Gerrit.**  

<https://chromium-review.googlesource.com/7673406>

**Have the changes been released and tested on canary?**  

Yes.

**Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?**  

Yes. It is enabled by default but kill-switchable with the `WebMachineLearningNeuralNetwork` flag.

**If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.**  

No.

### dr...@chromium.org (2026-03-23)

No crashes in Canary, approved to merge to M147.

### dx...@google.com (2026-03-24)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Wei Wang [wei4.wang@intel.com](mailto:wei4.wang@intel.com)  

Link:    <https://chromium-review.googlesource.com/7693877>

[M147] [WebNN] Reject fusing per-channel quantized gemm if the quantized dimension of filter is not 0

---


Expand for full commit details
```
     
    The FULLY_CONNECTED's underlying kernels expect the per-channel 
    quantization axis to be the output channel(axis 0). So reject 
    fusing per-channel quantized gemm and fall back to the unfused 
    operators path if the quantized dimension of filter is not 0. 
     
    (cherry picked from commit fc10b0d6304d7d8f31fea83811aa673a7f13f720) 
     
    Bug: 493319454 
    Change-Id: Ib7e1236a535dc6a34d3ff9b9f0124a101bd89dbf 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7673406 
    Reviewed-by: Phillis Tang <phillis@chromium.org> 
    Commit-Queue: Wang, Wei4 <wei4.wang@intel.com> 
    Reviewed-by: Hu, Ningxin <ningxin.hu@intel.com> 
    Cr-Original-Commit-Position: refs/heads/main@{#1601718} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7693877 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Reilly Grant <reillyg@chromium.org> 
    Auto-Submit: Reilly Grant <reillyg@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7727@{#1314} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `services/webnn/tflite/graph_builder_tflite.cc`

---

Hash: [10bbd39937eb1765865d8ab784a0bb19dec041e5](https://chromiumdash.appspot.com/commit/10bbd39937eb1765865d8ab784a0bb19dec041e5)  

Date: Tue Mar 24 00:36:11 2026


---

### pe...@google.com (2026-03-24)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### re...@chromium.org (2026-03-24)

This feature was not enabled by default in M144.

### qk...@google.com (2026-03-24)

Labeled `LTS-NotApplicable-138` because M138 doens't have the suspected CL[1].

[1]  https://chromium-review.googlesource.com/c/chromium/src/+/6641102

### qk...@google.com (2026-03-24)

Labeled `LTS-NotApplicable-144` because the feature was not enabled M144 according to comment #17.

### dx...@google.com (2026-04-01)

Project: chromium/src  

Branch:  main  

Author:  Wei Wang [wei4.wang@intel.com](mailto:wei4.wang@intel.com)  

Link:    <https://chromium-review.googlesource.com/7702493>

[WebNN] Add wpt for quantized gemm with non-zero quantized dimension of the filter

---


Expand for full commit details
```
     
    Add regression wpt test for per-channel quantized gemm with non-zero 
    quantized dimension of the filter. 
     
    Bug: 493319454 
    Change-Id: Ia988b812b8773234936617c4ca73933f657cb5bf 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7702493 
    Reviewed-by: Hu, Ningxin <ningxin.hu@intel.com> 
    Reviewed-by: Phillis Tang <phillis@chromium.org> 
    Commit-Queue: Wang, Wei4 <wei4.wang@intel.com> 
    Cr-Commit-Position: refs/heads/main@{#1608242}

```

---

Files:

- M `third_party/blink/web_tests/external/wpt/webnn/conformance_tests/qdq_subgraph.https.any.js`

---

Hash: [c82377d134cc0a2fb6941b54e5b9d3826ed58446](https://chromiumdash.appspot.com/commit/c82377d134cc0a2fb6941b54e5b9d3826ed58446)  

Date: Wed Apr 1 01:31:22 2026


---

### sp...@google.com (2026-04-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $43000.00 for this report.

Rationale for this decision:
High quality. Memory corruption in a highly privileged process (e.g. GPU, network processes) with bisect


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/493319454)*
