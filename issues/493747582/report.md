# Heap OOB write in XNNPACK Pool2D via integer overflow

| Field | Value |
|-------|-------|
| **Issue ID** | [493747582](https://issues.chromium.org/issues/493747582) |
| **Status** | New |
| **Severity** | S4-Minimal |
| **Priority** | P0 |
| **Component** | Blink>WebML |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | we...@intel.com |
| **Created** | 2026-03-18 |
| **Bounty** | $43,000.00 |

## Description

# Integer overflow in XNNPack tensor size computation leads to heap OOB write in the GPU process via WebNN pool2d

## Summary

When the WebNN TFLite backend translates a `maxPool2d` (or `averagePool2d`) operation with explicit padding, it inserts an internal PAD node whose output tensor dimensions are not checked against the byte-size limit. XNNPack's `get_tensor_size` function then computes the tensor's byte size by multiplying the element count by the datatype width in a `uint64_t`, which silently wraps around for sufficiently large shapes. The memory planner allocates a workspace based on the wrapped value while the PAD kernel writes according to the true dimensions, producing an immediate heap buffer overflow in the GPU process. Affected platforms: all platforms where the TFLite WebNN backend is active (Linux, macOS, Windows, ChromeOS).

## Bisect

### XNNPack upstream — `xnn_shape_multiply_all_dims` never overflow-checked

- Commit: `0630d2941ca4b96b5f318ac3d03893922d55c3fa`
- Date: 2021-09-28
- Author: Marat Dukhan ([maratek@google.com](mailto:maratek@google.com))
- Subject: Refactor creation and setup of Operators from Nodes
- PiperOrigin-RevId: 399455001

This function is a simple `batch_size *= shape->dim[i]` loop with no overflow check, and has never had one. `get_tensor_size` multiplies the result by `xnn_datatype_size_bits` in `uint64_t`, which wraps for sufficiently large shapes, causing workspace underallocation.

### Became web-reachable — `InsertPadOperation` introduced with unchecked `SerializeTemporaryTensor`

- Commit: `ded4396ef94db6b715dda888751563a079f5497e`
- Date: 2024-03-12
- Author: Junwei Fu ([junwei.fu@intel.com](mailto:junwei.fu@intel.com))
- Subject: webnn: Support Conv2d in TFLite converter
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/5337479>

This commit introduced `InsertPadOperation` using `SerializeTemporaryTensor()` (no byte-size check) to create internal PAD output tensors. The function validates individual dimensions fit in `int32_t` but never checks the total byte size against `tensor_byte_length_limit`. The pool2d path was added subsequently and reuses the same function.

### Checked variant introduced but `InsertPadOperation` NOT updated

- Commit: `00516fef984120c951e854895bbbc80682f8b9d0`
- Date: 2025-10-31
- Author: Lynne Jiang ([lyjiang@google.com](mailto:lyjiang@google.com))
- Subject: webnn: Enable temp tensor byte size check.
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/7092679>

This commit introduced `SerializeTemporaryTensorWithByteSizeCheck()` and updated one call site (float16-to-float32 cast dequantize path), but `InsertPadOperation` and other callers of `SerializeTemporaryTensor` were not updated.

## Root Cause

The vulnerability spans two components: the Chromium WebNN translation layer and XNNPack's tensor size arithmetic.

When `maxPool2d` or `averagePool2d` receives explicit padding that cannot be expressed as TFLite SAME or VALID, `SerializePool2d` calls `InsertPadOperation` to emit a separate PAD node ahead of the pool. This function computes the padded output dimensions with checked arithmetic, verifying each individual dimension fits in `int32_t`, then creates the tensor:

```
// services/webnn/tflite/graph_builder_tflite.cc:3563-3565
const TensorIndex output_tensor_index =
    SerializeTemporaryTensor(output_shape, input_tensor_info.data_type,
                             input_tensor_info.quantize_params);

```

`SerializeTemporaryTensor` accepts any dimensions without validating total byte size:

```
// services/webnn/tflite/graph_builder_tflite.cc:3063-3074
TensorIndex GraphBuilderTflite::SerializeTemporaryTensor(
    base::span<const int32_t> dimensions,
    ::tflite::TensorType tensor_type,
    QuantizateParametersOffset quantize_params) {
  const TensorIndex temporary_tensor_index =
      base::checked_cast<TensorIndex>(tensors_.size());
  tensors_.emplace_back(::tflite::CreateTensor(
      builder_, builder_.CreateVector<int32_t>(dimensions), tensor_type,
      /*buffer=*/0, /*name=*/0, quantize_params));
  return temporary_tensor_index;
}

```

The codebase already provides a safe alternative, `SerializeTemporaryTensorWithByteSizeCheck`, which validates byte length against `context_properties_.tensor_byte_length_limit` before creation. `InsertPadOperation` does not use it.

XNNPack delegates the resulting PAD node and computes workspace requirements in `get_tensor_size`:

```
// third_party/xnnpack/src/src/tensor.c:779-781
uint64_t size_bits = xnn_datatype_size_bits(datatype);
size_bits *= xnn_shape_multiply_all_dims(shape);
return (size_bits + 7) >> 3;

```

`xnn_shape_multiply_all_dims` returns a `size_t` product of all dimensions:

```
// third_party/xnnpack/src/src/tensor.c:636-644
size_t xnn_shape_multiply_all_dims(const struct xnn_shape* shape) {
  size_t batch_size = 1;
  for (size_t i = 0; i < shape->num_dims; i++) {
    batch_size *= shape->dim[i];
  }
  return batch_size;
}

```

Neither multiplication is overflow-checked. For a padded tensor shape `[1, 32768, 32770, 536838146]`, the element count is 576,460,752,303,516,672. Multiplying by 32 bits yields 18,446,744,073,712,533,504, which exceeds `UINT64_MAX` by exactly 4,194,304. The wrapped `size_bits` value is 4,194,304, producing a workspace allocation of 524,288 bytes (512 KB).

The PAD operator's SSE2 fill kernel then writes zero-padding into this workspace following the true 4D strides. After approximately 131,072 float writes the kernel crosses the 512 KB boundary and corrupts adjacent heap memory, which ASAN detects as a heap-buffer-overflow WRITE.

The PoC constructs this condition through `maxPool2d` with the following parameters: input `[1, 1, 1, 536838146]`, window `[32768, 32770]`, strides `[32768, 32770]`, and padding `[32767, 0, 32769, 0]`. The pool's output shape is `[1, 1, 1, 536838146]`, which passes all WebNN validation, while the internal padded shape overflows XNNPack's size computation. Using strides equal to the window dimensions keeps the max-pooling indirection buffer at approximately 24 GB, which is large but within the reach of servers and workstations.

## Reproduce

Tested at commit `7c89d33808e55` on Linux x64.

ASAN build configuration (`out/asan-release/args.gn`):

```
is_asan = true
is_debug = false
dcheck_always_on = false
target_cpu = "x64"
is_component_build = true

```

Serve the PoC and launch:

```
python3 -m http.server 8888 --directory issue_tflite005_xnnpack_pad_oob --bind 127.0.0.1 &
ASAN_OPTIONS=detect_odr_violation=0 out/asan-release/chrome \
  --no-sandbox \
  --enable-features=WebMachineLearningNeuralNetwork \
  --user-data-dir=/tmp/poc-$(date +%s) \
  http://127.0.0.1:8888/poc.html

```

Graph construction takes approximately 60 to 90 seconds (the max-pooling indirection buffer is around 24 GB). After dispatch, the GPU process crashes immediately with an ASAN heap-buffer-overflow WRITE:

```
==PID==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7b7439c02820
WRITE of size 16 at 0x7b7439c02820 thread T79 (ThreadPoolForeg)
    #0 xnn_xx_fill_ukernel__sse2_u64 xx-fill-sse2-u64.c:32
    ...
    #9 xnn_run_operator_with_index operator-run.c:2147
    #10 xnn_invoke_runtime runtime.c:1143
    #11 tflite::xnnpack::SubgraphInvoke(...) xnnpack_delegate.cc:1429
    ...
    #15 webnn::tflite::GraphImplTflite::ComputeResources::DoDispatch(...) graph_impl_tflite.cc:328

0x7b7439c02820 is located 0 bytes after 524320-byte region [0x7b7439b82800,0x7b7439c02820)
allocated by thread T79 (ThreadPoolForeg) here:
    #1 xnn_aligned_allocate allocator.c:46
    #2 xnn_plan_memory allocator.h:60
    #3 tflite::xnnpack::SubgraphPrepare(...) xnnpack_delegate.cc:1266

SUMMARY: AddressSanitizer: heap-buffer-overflow xx-fill-sse2-u64.c:32 in xnn_xx_fill_ukernel__sse2_u64

```

The complete ASAN log is in `asan.log`.

## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 11.9 KB)
- [poc.html](attachments/poc.html) (text/html, 2.4 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5568481336524800.

### je...@gmail.com (2026-03-19)

Please note that since `graph construction takes approximately 60 to 90 seconds (the max-pooling indirection buffer is around 24 GB)`, ClusterFuzz may not be able to reproduce it. Please verify manually using ASan Chrome.

### es...@chromium.org (2026-03-20)

Reilly, I'm sending you another couple WebNN bugs that don't repro on Clusterfuzz -- would you be able to see if they look plausible and/or add other owners? Thank you!

### re...@chromium.org (2026-03-20)

Lynne, please take a look at this issue. It's similar to the last one you fixed where there's probably a systemic issue we could fix by ensuring that we adhere to our tensor byte length limits when serializing temporary tensors.

### re...@chromium.org (2026-03-20)

This and [issue 494158331](https://issues.chromium.org/issues/494158331) seem very similar.

### ly...@google.com (2026-03-20)

Yes last time my fix only covers some of them because changing all of them requires large refactoring, I'll just continue with that effort to fix this issue to ensure full coverage.

### re...@chromium.org (2026-03-21)

Check that <https://chromium-review.googlesource.com/7689396> hasn't already fixed this. I don't think <https://chromium-review.googlesource.com/7690057> covers this case. We've had a few people looking at restricting padding size for operators like pool2d from different angles.

### je...@gmail.com (2026-03-22)

I just checked <https://chromium-review.googlesource.com/c/chromium/src/+/7689396> and it can also fix this issue, but my issue is earlier than Bug: 494341335.

Edited:
An earlier vulnerability I previously submitted was also fixed by this CL.
<https://issues.chromium.org/u/5/issues/493082093>

The CL validates the intermediate padded tensor's byte size in the pool2d path. Since padded\_dim ≥ window\_dim is required for valid output, the PoC's large window dimensions force a padded tensor that exceeds tensor\_byte\_length\_limit, rejecting the operation before it reaches XNNPACK.

### je...@gmail.com (2026-03-22)

Additionally, I just submitted a new vulnerability (<https://issues.chromium.org/u/5/issues/494823884>). While the crash site is the same (`xnn_indirection_init_maxpool2d`), the root cause is fundamentally different — it is a union aliasing bug in XNNPACK's `optimize_common_subgraphs_merge_clamps`, which corrupts validated padding values internally, after all Chromium-side checks have passed. Restricting user-supplied padding size cannot mitigate this case.

I'm not trying to rush triage by cross-referencing here — I only mention it because the shared crash point might otherwise lead to the assumption that the existing padding-size restrictions already cover it. I hope the additional case is useful in informing a more comprehensive fix for this class of issue. Apologies for the extra noise.

### ni...@intel.com (2026-03-22)

@je...@gmail.com, could you please CC me in the new report <https://issues.chromium.org/u/5/issues/494823884>? I am interested in investigating it.

### je...@gmail.com (2026-03-22)

re #c11: Unfortunately, I don't have the permission to add CCs to that report. You may want to reach out to the Chromium security team directly to request access.

### el...@google.com (2026-03-24)

Security shepherd: this is Sev-0 for us since it's an OOB write in the GPU process. I think that, since this is behind an origin trial, the actual impact is limited but I can't call this SecImpact-None if it's enable for any users or origins.

### el...@google.com (2026-03-24)

Speculative FoundIn and OS from me, as well.

### dx...@google.com (2026-03-25)

Project: chromium/src  

Branch:  main  

Author:  Lynne Jiang [lyjiang@google.com](mailto:lyjiang@google.com)  

Link:    <https://chromium-review.googlesource.com/7693793>

[webnn] Switch to use SerializeTemporaryTensorWithByteSizeCheck in tflite graph builder.

---


Expand for full commit details
```
     
    Bug: 493747582 
    Binary-Size: Size increase is expected. 
    Change-Id: I420f1a26507007af0e4c17a5a48b1ea30e1b4c9d 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7693793 
    Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    Reviewed-by: Phillis Tang <phillis@chromium.org> 
    Commit-Queue: Lynne Jiang <lyjiang@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1604964}

```

---

Files:

- M `services/webnn/tflite/graph_builder_tflite.cc`
- M `services/webnn/tflite/graph_builder_tflite.h`

---

Hash: [db6bda50f023057ffa82845f232852dea0f271e1](https://chromiumdash.appspot.com/commit/db6bda50f023057ffa82845f232852dea0f271e1)  

Date: Wed Mar 25 18:10:24 2026


---

### ch...@google.com (2026-03-26)

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to beta (M147) because latest trunk commit (1604964) appears to be after beta branch point (1596535).

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2026-03-26)

Merge review required: M147 has already been cut for stable release.

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

### dr...@chromium.org (2026-03-27)

No crashes in Canary after 24 hours. Approved to merge to M147. Our release cut for M147 is Tuesday at 11am Pacific time, so please try to land by then.

### ch...@google.com (2026-03-31)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sr...@chromium.org (2026-03-31)

We are cutting M147 RC today around 12pm PST, if your merge is critical to be incliuded in the RC build and is not able to make that cut off, please reach out to me , ( i can give some buffer for critical fixes that needs to included in RC) 

### sp...@google.com (2026-04-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $43000.00 for this report.

Rationale for this decision:
High quality.  Memory corruption in a highly privileged process (e.g. GPU, network processes)  with bisect


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-04-04)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### re...@chromium.org (2026-04-10)

Clearing the merge fields because we've decided to delasy the WebNN OT so this no longer affects M147.

### ch...@google.com (2026-07-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/493747582)*
