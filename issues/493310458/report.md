# Heap buffer overflow in TFLite pooling via WebNN Pool2d windowDimensions uint32-to-int32 truncation

| Field | Value |
|-------|-------|
| **Issue ID** | [493310458](https://issues.chromium.org/issues/493310458) |
| **Status** | New |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>WebML |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | ly...@google.com |
| **Created** | 2026-03-17 |
| **Bounty** | $3,000.00 |

## Description

## Title

Heap buffer overflow in TFLite pooling via WebNN Pool2d windowDimensions uint32-to-int32 truncation

## Summary

The WebNN-to-TFLite translation layer in `GraphBuilderTflite::SerializePool2d` passes `uint32_t` window dimensions directly into TFLite's `CreatePool2DOptions`, which expects `int32_t` parameters. A web page can supply `windowDimensions` values at or above 0x80000000 that pass all WebNN validation but become negative when truncated to `int32_t`. TFLite's optimized pooling kernels then use these negative filter dimensions in loop-bound arithmetic, producing massively out-of-range array indices and triggering a heap-buffer-overflow in the GPU process. Affected platforms: all desktop and mobile platforms where the TFLite WebNN backend is active (Linux, ChromeOS, Android by default; Windows and macOS as a fallback when ONNX Runtime or CoreML are unavailable). No special GPU hardware is required.

## Bisect

Introducing Commit: `6c9e4fea79849343c09bae0214cd76904f43be22`

- Date: 2024-03-13
- Author: Junwei Fu ([junwei.fu@intel.com](mailto:junwei.fu@intel.com))
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/5359192>

## Root Cause

The WebNN Mojo interface defines `Pool2d.window_dimensions` as a `Size2d` of `uint32` fields. WebNN's validation layer (`ValidatePool2dAndInferOutput`, `CalculateConv2dOutputSize`) operates entirely in `uint32_t` and `double`, and will accept window dimension values up to UINT32\_MAX as long as the computed output size remains a valid positive integer. The TFLite FlatBuffer schema, however, defines `Pool2DOptions.filter_width` and `Pool2DOptions.filter_height` as `int32`. When `SerializePool2d` forwards the window dimensions into `CreatePool2DOptions`, the compiler performs an implicit narrowing conversion from `uint32_t` to `int32_t` with no range check:

```
// services/webnn/tflite/graph_builder_tflite.cc:6786-6805
webnn::Size2d<uint32_t> filter_size2d = {
    .height = pool2d.window_dimensions->height,   // uint32_t
    .width = pool2d.window_dimensions->width};     // uint32_t

const auto pool_2d_options = ::tflite::CreatePool2DOptions(
    builder_, padding_mode.mode, pool2d.strides->width,
    pool2d.strides->height, filter_size2d.width, filter_size2d.height,
    //                      ^^^^^^^^^^^^^^^^^^  ^^^^^^^^^^^^^^^^^^^
    //                      uint32_t silently narrowed to int32_t
    ::tflite::ActivationFunctionType_NONE);

```

A `windowDimensions` value of 0x80000000 (2,147,483,648) is a perfectly valid `uint32_t` but wraps to -2,147,483,648 (`INT32_MIN`) as a signed `int32_t`. Crucially, the attacker can choose explicit padding values that exactly match the SAME-padding formula so that `GetTfLitePaddingMode` returns `Padding_SAME` and no separate PAD operator is inserted. For a 1x1 input with window 0x80000000 and stride 1, the SAME-padding formula yields `begin = 0x3FFFFFFF`, `end = 0x40000000`, producing an output size of 1; all WebNN validation checks pass.

Once the model reaches TFLite, `GenericPrepare` calls `ComputePaddingHeightWidth` with the negative filter dimensions. The SAME-padding output-size formula ignores the filter entirely (`(in + stride - 1) / stride`), but the padding computation itself overflows:

```
// third_party/tflite/src/tensorflow/lite/kernels/padding.h
int padding_height =
    std::max(0, (out_height - 1) * stride_height
                + filter_height - in_height) / 2;

```

With `filter_height = INT32_MIN` and `in_height = 1`, the expression `INT32_MIN - 1` wraps (signed overflow) to `INT32_MAX`, so `padding_height` becomes `INT32_MAX / 2 = 1,073,741,823`.

The default-registered optimized pooling kernel (`Register_MAX_POOL_2D` selects `kGenericOptimized`) then iterates over input elements and projects each one onto the output range:

```
// third_party/tflite/src/tensorflow/lite/kernels/internal/optimized/optimized_ops.h:3200-3217
int hpad = h + params.padding_values.height;  // 0 + 1073741823
int h_start = (hpad < params.filter_height)   // 1073741823 < -2147483648? NO
    ? 0
    : (hpad - params.filter_height) / stride_height + 1;
    // (1073741823 - (-2147483648)) overflows to -1073741825
    // h_start = -1073741824

int h_end = std::min(hpad / stride_height + 1, output_height);
    // min(1073741824, 1) = 1

for (int ph = h_start; ph < h_end; ++ph) {       // -1073741824 < 1 => enters loop
  for (int pw = w_start; pw < w_end; ++pw) {
    int out_offset = NodeOffset(b, ph, pw, output_height, output_width);
    // NodeOffset(0, -1073741824, -1073741824, 1, 1) => huge negative
    out_mat.col(out_offset) = ...;                // OOB access
  }
}

```

The `NodeOffset` function computes `(b * height + h) * width + w`, which with negative `ph` and `pw` produces a massively negative index. `out_mat.col(negative_index)` accesses memory far before the allocated output buffer, causing a heap-buffer-overflow READ that ASAN catches immediately.

The ASAN stack trace confirms the crash occurs in the GPU process on a thread-pool worker, triggered via the Mojo IPC path from the renderer: `WebNNGraphImpl::Dispatch` posts a task to the GPU sequence, which calls `GraphImplTflite::ComputeResources::DoDispatch`, which invokes `tflite::impl::Interpreter::Invoke`, ultimately reaching the vulnerable `optimized_ops::MaxPool`.

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
  --user-data-dir=%TEMP%\poc-tflite013 ^
  --enable-logging=stderr ^
  poc.html

```

On Windows the default WebNN backend is ONNX Runtime, so `--disable-features=WebNNOnnxRuntime` is needed to fall through to TFLite.

### Linux

```
out/asan-release/chrome \
  --no-sandbox \
  --enable-features=WebMachineLearningNeuralNetwork \
  --enable-logging=stderr \
  poc.html

```

On Linux TFLite is the default backend; no feature overrides are needed beyond enabling WebNN itself.

The GPU process crashes within seconds of loading the page on both platforms. ASAN reports a heap-buffer-overflow READ in `tflite::optimized_ops::MaxPool`. Complete ASAN logs are attached in `issue_tflite013/`.

### Windows ASAN (excerpt)

```
==16276==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x11e0d481cff8
READ of size 4 at 0x11e0d481cff8 thread T23
    #0 in tflite::optimized_ops::MaxPool optimized_ops.h:3214
    #1 in pooling::MaxEvalFloat<1> pooling.cc:264
    #2 in pooling::MaxEval<1> pooling.cc:422
    #3 in tflite::Subgraph::InvokeImpl subgraph.cc:1761
    #5 in tflite::impl::Interpreter::Invoke interpreter.cc:247
    #6 in webnn::tflite::GraphImplTflite::ComputeResources::DoDispatch graph_impl_tflite.cc:328

0x11e0d481cffb is located 0 bytes after 91-byte region [0x11e0d481cfa0,0x11e0d481cffb)

SUMMARY: AddressSanitizer: heap-buffer-overflow optimized_ops.h:3214 in tflite::optimized_ops::MaxPool

```
### Linux ASAN (excerpt)

```
==1277192==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7bcac94e9154
READ of size 4 at 0x7bcac94e9154 thread T42 (ThreadPoolForeg)
    #0 in tflite::optimized_ops::MaxPool comp.h:42
    #1 in pooling::MaxEvalFloat<1> pooling.cc:264
    #2 in pooling::MaxEval<1> pooling.cc:422
    #3 in tflite::Subgraph::InvokeImpl subgraph.cc
    #5 in tflite::impl::Interpreter::Invoke interpreter.cc:247
    #6 in webnn::tflite::GraphImplTflite::ComputeResources::DoDispatch graph_impl_tflite.cc:328

0x7bcac94e9154 is located 0 bytes after 20-byte region [0x7bcac94e9140,0x7bcac94e9154)

SUMMARY: AddressSanitizer: heap-buffer-overflow in tflite::optimized_ops::MaxPool

```
## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [asan-linux.log](attachments/asan-linux.log) (text/plain, 31.6 KB)
- [asan.log](attachments/asan.log) (text/plain, 29.7 KB)
- [poc.html](attachments/poc.html) (text/html, 2.5 KB)

## Timeline

### je...@gmail.com (2026-03-17)

update bisect

## Bisect

### TFLite upstream — MaxPool + NodeOffset introduced

- Commit: 0b15439f8f0f2d4755587f4096c3ea04cb199d23
- Date: 2017-11-10
- Author: Andrew Selle ([aselle@google.com](mailto:aselle@google.com))
- Subject: Internal Change.
- Piper: PiperOrigin-RevId: 175307445
- URL: <https://github.com/tensorflow/tensorflow/commit/0b15439f8f0f2d4755587f4096c3ea04cb199d23>

The very first TFLite commit. Contains MaxPool() with NodeOffset() using unsafe signed int arithmetic that does not handle negative filter dimensions.

### TFLite upstream — ComputePaddingHeightWidth added

- Commit: 07bb8c1bbc93fe1162d247511c89c136273ddd07
- Date: 2018-05-16
- Author: A. Unique TensorFlower
- Subject: Implementation of transpose\_conv
- Piper: PiperOrigin-RevId: 196806646
- URL: <https://github.com/tensorflow/tensorflow/commit/07bb8c1bbc93fe1162d247511c89c136273ddd07>

Introduced ComputePaddingHeightWidth() in padding.h with signed int arithmetic that overflows when filter dimensions are negative.

### TFLite upstream — vulnerability chain connected

- Commit: 354b95f9588b6cfcdc8bc88601943b6e15f561bd
- Date: 2019-04-22
- Author: Renjie Liu
- Subject: Reuse ComputePaddingHeightWidth, also support dilation != 1 case.
- Piper: PiperOrigin-RevId: 244797614
- URL: <https://github.com/tensorflow/tensorflow/commit/354b95f9588b6cfcdc8bc88601943b6e15f561bd>

Changed pooling.cc to call ComputePaddingHeightWidth() from padding.h, feeding the overflow-susceptible padding values into MaxPool() in optimized\_ops.h. This is the commit that fully connected the vulnerability chain within TFLite. Neither filter\_height > 0 nor filter\_width > 0 is validated anywhere.

### Became web-reachable

- Commit: 6c9e4fea79849343c09bae0214cd76904f43be22
- Date: 2024-03-13
- Author: Junwei Fu ([junwei.fu@intel.com](mailto:junwei.fu@intel.com))
- Subject: webnn: Support Pool2d in //services/webnn/tflite
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/5359192>

This commit added SerializePool2d() which passes uint32\_t window dimensions directly to TFLite's CreatePool2DOptions (int32\_t) with no range check. Values >= 0x80000000 wrap to negative int32\_t, triggering the signed overflow chain in ComputePaddingHeightWidth → MaxPool → NodeOffset.

### dr...@chromium.org (2026-03-17)

This reproduces as claimed in M146. Triaging just like the other WebNN bugs.

### re...@chromium.org (2026-03-17)

WebNN is enabled by default for desktop platforms on M-147. Raising priority.

### re...@chromium.org (2026-03-17)

Lynne, please add the necessary checks here to catch an overflow when narrowing from `uint32_t` to `int32_t` and audit other places where we are calling any of the `::tflite::Create*` functions with `uint32_t` values.

### re...@chromium.org (2026-03-17)

It looks like we can opt into stricter checks by adding `//build/config/compiler:prevent_unsafe_narrowing` to the GN config for the target including `graph_builder_tflite.cc`. Please try this out and see how many warnings it generates.

### cl...@appspot.gserviceaccount.com (2026-03-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6077418720755712.

### ly...@google.com (2026-03-17)

Re [comment#6](https://issues.chromium.org/issues/493310458#comment6): I tested the `//build/config/compiler:prevent_unsafe_narrowing` config, which generated 85 warnings in total (details [here](https://paste.googleplex.com/5521152366739456)). However, it didn't capture the specific uint32\_t -> int32\_t case mentioned in this bug. To ensure full coverage, I audited the code using the Gemini CLI and found 4 tflite calls(`CreateDepthwiseConv2DOptions`, `CreateConv2DOptions`, `CreateTransposeConvOptions`, `CreatePool2DOptions`) in graph\_builder\_tflite.cc that have this exact issue. I will proceed with the fix adding the explicit bounds checks for all of them first.

### re...@chromium.org (2026-03-17)

As I feared this triggers a lot of failures in headers all over Chromium and TFLite. It looks like when you tested this Ninja didn't even get to trying to compile `graph_builder_tflite.cc`. We might be able to succeed if we only enable this for `graph_builder_tflite.cc` specifically by breaking that into its own GN target so we can set compiler flags independently from the rest of WebNN.

### re...@chromium.org (2026-03-17)

It looks like moving these two files into their own `source_set` works:

```
source_set("graph_builder_tflite") {
  sources = [
    "tflite/graph_builder_tflite.cc",
    "tflite/graph_builder_tflite.h",
  ]
  deps = [
    "//base",
    "//third_party/flatbuffers",
    "//third_party/fp16",
    "//third_party/tflite",
  ]
  configs += [
    "//build/config/compiler:prevent_unsafe_narrowing",
  ]
}

```

### 24...@project.gserviceaccount.com (2026-03-18)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2026-03-18)

Detailed Report: https://clusterfuzz.com/testcase?key=6077418720755712

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x76e32a550594
Crash State:
  void tflite::ops::builtin::pooling::MaxEvalFloat<
  TfLiteStatus tflite::ops::builtin::pooling::MaxEval<
  tflite::Subgraph::InvokeImpl
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1356883:1356886

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6077418720755712

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### dx...@google.com (2026-03-19)

Project: chromium/src  

Branch:  main  

Author:  Lynne Jiang [lyjiang@google.com](mailto:lyjiang@google.com)  

Link:    <https://chromium-review.googlesource.com/7675380>

[webnn] Add range checks and safe casts for TFLite options.

---


Expand for full commit details
```
     
    This change adds checks to ensure that unsigned integer values (e.g., 
    axis, strides, filter sizes) are within the range of `int32_t` before 
    being passed to TFLite option creation functions. `base::checked_cast` 
    is used for the conversion. Functions affected now return 
    `base::expected` to propagate potential errors from out-of-range values. 
     
    Bug: 493310458 
    Change-Id: I2126e55f766f4d302b7e9fd9072f440ee2da8871 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7675380 
    Commit-Queue: Lynne Jiang <lyjiang@google.com> 
    Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    Reviewed-by: Phillis Tang <phillis@chromium.org> 
    Reviewed-by: Hu, Ningxin <ningxin.hu@intel.com> 
    Cr-Commit-Position: refs/heads/main@{#1602104}

```

---

Files:

- M `services/webnn/tflite/graph_builder_tflite.cc`
- M `services/webnn/tflite/graph_builder_tflite.h`

---

Hash: [47e769f7990865a98f9d90ce6bc4271d4de373ea](https://chromiumdash.appspot.com/commit/47e769f7990865a98f9d90ce6bc4271d4de373ea)  

Date: Thu Mar 19 18:06:03 2026


---

### re...@chromium.org (2026-03-23)

Merging this change to M147 is blocking the merge of [issue 494158331](https://issues.chromium.org/issues/494158331).

### ch...@google.com (2026-03-23)

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

### re...@chromium.org (2026-03-23)

**Why does your merge fit within the merge criteria for these milestones?**  

It is a security issue.

**What changes specifically would you like to merge? Please link to Gerrit.**  

<https://chromium-review.googlesource.com/7675380>

**Have the changes been released and tested on canary?**  

Yes.

**Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?**  

Yes, it is enabled by default but kill-switchable via the `WebMachineLearningNeuralNetwork` feature flag.

**If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.**  

No.

### dr...@chromium.org (2026-03-23)

Hm. Looks like automation failed us here. It should have requested the merges automatically. Thank you for manually requesting, approved to merge to M147.

### dx...@google.com (2026-03-24)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Lynne Jiang [lyjiang@google.com](mailto:lyjiang@google.com)  

Link:    <https://chromium-review.googlesource.com/7695357>

[M147] [webnn] Add range checks and safe casts for TFLite options.

---


Expand for full commit details
```
     
    This change adds checks to ensure that unsigned integer values (e.g., 
    axis, strides, filter sizes) are within the range of `int32_t` before 
    being passed to TFLite option creation functions. `base::checked_cast` 
    is used for the conversion. Functions affected now return 
    `base::expected` to propagate potential errors from out-of-range values. 
     
    (cherry picked from commit 47e769f7990865a98f9d90ce6bc4271d4de373ea) 
     
    Bug: 493310458 
    Change-Id: I2126e55f766f4d302b7e9fd9072f440ee2da8871 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7675380 
    Commit-Queue: Lynne Jiang <lyjiang@google.com> 
    Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    Reviewed-by: Phillis Tang <phillis@chromium.org> 
    Reviewed-by: Hu, Ningxin <ningxin.hu@intel.com> 
    Cr-Original-Commit-Position: refs/heads/main@{#1602104} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7695357 
    Auto-Submit: Reilly Grant <reillyg@chromium.org> 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Reilly Grant <reillyg@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7727@{#1323} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `services/webnn/tflite/graph_builder_tflite.cc`
- M `services/webnn/tflite/graph_builder_tflite.h`

---

Hash: [c52281e6bd9e6acb9ae66f1257495f54a17a6489](https://chromiumdash.appspot.com/commit/c52281e6bd9e6acb9ae66f1257495f54a17a6489)  

Date: Tue Mar 24 01:40:08 2026


---

### pe...@google.com (2026-03-24)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### re...@chromium.org (2026-03-24)

This feature was not enabled in M144.

### qk...@google.com (2026-03-24)

Labeled `LTS-NotApplicable-144`/`LTS-NotApplicable-138` because the feature was not enabled in M144 according to comment #17. 

### aj...@google.com (2026-05-13)

Medium as this just looks like a read.

### sp...@google.com (2026-05-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline with bisect - User information disclosure


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
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/493310458)*
