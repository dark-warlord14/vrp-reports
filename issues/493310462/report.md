# Heap buffer overflow in TFLite StridedSlice via WebNN slice() due to float32 precision loss in output shape computation

| Field | Value |
|-------|-------|
| **Issue ID** | [493310462](https://issues.chromium.org/issues/493310462) |
| **Status** | New |
| **Severity** | S4-Minimal |
| **Priority** | P0 |
| **Component** | Blink>WebML |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | re...@chromium.org |
| **Created** | 2026-03-17 |
| **Bounty** | $43,000.00 |

## Description

# Heap buffer overflow in TFLite StridedSlice via WebNN slice() due to float32 precision loss in output shape computation

## Summary

The TFLite STRIDED\_SLICE kernel computes output tensor dimensions using float32 arithmetic, which silently loses precision for dimension values exceeding 2^24. The WebNN validation layer computes the same dimensions using exact integer arithmetic, so the graph passes validation while TFLite allocates a smaller output buffer than the data actually written during evaluation. A web page can exploit this discrepancy to trigger a heap buffer overflow in the GPU process through the WebNN `slice()` API. Affected platforms: Linux, Windows, macOS, ChromeOS (any platform where WebNN uses the TFLite backend).

## Bisect

Introducing Commit: [`6dfe00ca4114`](https://github.com/tensorflow/tensorflow/commit/6dfe00ca4114371ed47c93810219736e3deda2d2)

- Date: 2018-01-23
- Author: A. Unique TensorFlower
- Review: PiperOrigin-RevId: 183020501

This commit added the STRIDED\_SLICE kernel to TFLite with the float32 division in [`ResizeOutputTensor`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/tflite/src/tensorflow/lite/kernels/strided_slice.cc;l=225). The bug became web-reachable when Chrome integrated WebNN with the TFLite backend and translated `MLGraphBuilder.slice()` into the TFLite STRIDED\_SLICE op.

## Root Cause

When TFLite prepares a STRIDED\_SLICE operation, `ResizeOutputTensor` computes the output dimension along each axis by dividing the slice extent by the stride using float32:

```
// third_party/tflite/src/tensorflow/lite/kernels/strided_slice.cc
int32_t begin = ::tflite::strided_slice::StridedSliceStartForAxis(
    op_params, effective_input_shape, idx);
int32_t end = ::tflite::strided_slice::StridedSliceEndForAxis(
    op_params, effective_input_shape, idx, begin);

dim_shape = std::ceil((end - begin) / static_cast<float>(stride));

```

IEEE 754 single-precision floats have a 24-bit significand, so integers above 2^24 (16,777,216) cannot all be represented exactly. When `end - begin` equals 16,777,217 and `stride` equals 1, the cast `static_cast<float>(stride)` produces 1.0f, but the implicit promotion of `dim_shape` (16,777,217) to float rounds it down to 16,777,216.0f. The `std::ceil` call has no effect since the value is already integral after rounding. The output tensor is therefore allocated with 16,777,216 elements along that axis instead of 16,777,217.

The reference implementation of StridedSlice does not consult the output shape at all, as the code itself documents:

```
// third_party/tflite/src/tensorflow/lite/kernels/internal/reference/strided_slice.h
// Note that the output_shape is not used herein.

```

Instead, it recomputes begin and end from the original integer parameters and iterates over the true range. When the innermost stride is 1, it issues a single `memcpy` of `stop - start` elements per outer iteration through `SequentialTensorWriter::WriteN`:

```
// third_party/tflite/src/tensorflow/lite/kernels/internal/portable_tensor.h
void WriteN(int position, int len) {
    memcpy(output_ptr_, &input_data_[position], sizeof(T) * len);
    output_ptr_ += len;
}

```

This writes the correct number of elements into a buffer that is too small.

Chromium's WebNN service translates `MLGraphBuilder.slice()` into TFLite's STRIDED\_SLICE. The WebNN validation layer in `ValidateSliceAndInferOutput` computes the output shape using exact integer ceiling division:

```
// services/webnn/public/cpp/graph_validation_utils.cc
uint32_t output_size = attributes.sizes[i] / attributes.strides[i] +
                       (attributes.sizes[i] % attributes.strides[i] != 0);

```

This produces the correct value of 16,777,217, so the operation passes validation. After TFLite builds the model, a post-build check in `GraphImplTflite` compares each output tensor's byte count against the WebNN-expected size. However, this check only inspects the graph's final output tensors, not intermediate tensors. By chaining two slice operations, where the first produces the oversized intermediate tensor and the second extracts a small sub-tensor as the graph output, the mismatch on the intermediate tensor goes undetected and the graph builds successfully. When the graph is dispatched, the first slice writes past the end of its allocated arena buffer, corrupting adjacent memory in the GPU process.

## Reproduce

Tested at commit `7c89d33808e55` on Linux x86\_64. No source modifications required.

Build configuration (`out/asan-release/args.gn`):

```
is_asan = true
is_debug = false
dcheck_always_on = false
target_cpu = "x64"
is_component_build = true

```

Build:

```
autoninja -C out/asan-release chrome

```

Serve the PoC and launch Chrome:

```
python3 -m http.server 8888 &
ASAN_OPTIONS=detect_odr_violation=0 out/asan-release/chrome \
  --no-sandbox \
  --enable-features=WebMachineLearningNeuralNetwork \
  --user-data-dir=/tmp/poc-$(date +%s) \
  http://localhost:8888/poc.html

```

The GPU process crashes within a few seconds of page load with a heap-buffer-overflow in `__asan_memcpy`, called from `tflite::reference_ops::StridedSlice<unsigned char>`.

```
=================================================================
==1307355==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7b76f54a68c0 at pc 0x55d111bdcbae bp 0x7b7709aabcf0 sp 0x7b7709aab4b0
WRITE of size 65 at 0x7b76f54a68c0 thread T42 (ThreadPoolForeg)
    #0 0x55d111bdcbad in __asan_memcpy
    #1 0x7f775650a73e in void tflite::reference_ops::StridedSlice<unsigned char>(...) third_party/tflite/src/tensorflow/lite/kernels/internal/portable_tensor.h:130:5
    #2 0x7f7756504ed7 in tflite::ops::builtin::strided_slice::EvalImpl<...>(...) third_party/tflite/src/tensorflow/lite/kernels/internal/reference/strided_slice.h:140:3
    #3 0x7f77565056f9 in tflite::ops::builtin::strided_slice::Eval<...>(...) third_party/tflite/src/tensorflow/lite/kernels/strided_slice.cc:370:10
    #4 0x7f7755f62094 in tflite::Subgraph::InvokeImpl() third_party/tflite/src/tensorflow/lite/core/subgraph.cc
    #5 0x7f7755f6112e in tflite::Subgraph::Invoke() third_party/tflite/src/tensorflow/lite/core/subgraph.cc:1653:17
    #6 0x7f7755f3f6b4 in tflite::impl::Interpreter::Invoke() third_party/tflite/src/tensorflow/lite/core/interpreter.cc:247:48
    #7 0x7f77554ea7bd in webnn::tflite::GraphImplTflite::ComputeResources::DoDispatch(...) services/webnn/tflite/graph_impl_tflite.cc:328:41

0x7b76f54a68c0 is located 0 bytes after 2181038272-byte region [0x7b76734a6800,0x7b76f54a68c0)
allocated by thread T42 (ThreadPoolForeg) here:
    #0 0x55d111bdf772 in aligned_alloc
    #1 0x7f7755f9e814 in tflite::SimpleMemoryArena::Commit(bool*) third_party/tflite/src/tensorflow/lite/simple_memory_arena.cc:111:31
    #2 0x7f7755f14ec8 in tflite::ArenaPlanner::ExecuteAllocations(int, int) third_party/tflite/src/tensorflow/lite/arena_planner.cc:433:32
    #3 0x7f7755f5d87c in tflite::Subgraph::PrepareOpsAndTensors() third_party/tflite/src/tensorflow/lite/core/subgraph.cc:1604:42
    #4 0x7f7755f5beba in tflite::Subgraph::AllocateTensors(...) third_party/tflite/src/tensorflow/lite/core/subgraph.cc:1035:25
    #5 0x7f77554d8722 in webnn::tflite::GraphImplTflite::ComputeResources::Create(...) services/webnn/tflite/graph_impl_tflite.cc:221:34

SUMMARY: AddressSanitizer: heap-buffer-overflow in __asan_memcpy

```

Full ASAN log is attached as `asan.log`.

## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [poc.html](attachments/poc.html) (text/html, 2.3 KB)
- [asan.log](attachments/asan.log) (text/plain, 39.5 KB)
- [asan-full.log](attachments/asan-full.log) (text/plain, 58.5 KB)

## Timeline

### je...@gmail.com (2026-03-17)

ADDITIONAL INFO Forgot to attach, please check this asan-full.log.

### je...@gmail.com (2026-03-17)

## Another Bisect

StridedSlice float32 precision issue — the commit that made it web-reachable:

- Commit: d50e1bc169365e379ca6ab34df06868a8e5e50b2
- Date: 2024-11-06
- Author: Shiyi Zou ([shiyi.zou@intel.com](mailto:shiyi.zou@intel.com))
- Subject: "webnn: support strides for slice operator"
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/5975313>

This commit changed the WebNN slice() translation from TFLite SLICE to STRIDED\_SLICE, making the float32 precision loss bug in ResizeOutputTensor reachable from the web. The original
slice() → SLICE mapping (commit 192cbba1ee34, 2024-03-15, by junwei) was not affected because TFLite's SLICE op doesn't use float32 division for shape computation.

### cl...@appspot.gserviceaccount.com (2026-03-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5475875734716416.

### re...@chromium.org (2026-03-17)

Upstream TFLite fix out for review.

### ch...@google.com (2026-03-18)

Setting milestone because of s0/s1 severity.

### 24...@project.gserviceaccount.com (2026-03-18)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2026-03-18)

Detailed Report: https://clusterfuzz.com/testcase?key=5475875734716416

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE {*}
Crash Address: 0x74584a5ac8c0
Crash State:
  void tflite::reference_ops::StridedSlice<signed char>
  tflite::ops::builtin::strided_slice::EvalImpl
  tflite::ops::builtin::strided_slice::Eval
  
Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1601052:1601055

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5475875734716416

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### re...@chromium.org (2026-03-18)

Bugjuggler: <http://tap/tensorflow> is green on cl/885789312

### bu...@google.com (2026-03-18)

Sorry, Bugjuggler can only be used by users in the @google.com domain.

### bu...@google.com (2026-03-18)

Nothing was specified to wait for and there are no blocking bugs or pending CLs. For usage information see go/bugjuggler.

### re...@google.com (2026-03-18)

Bugjuggler: <http://tap/tensorflow> is green on cl/885789312

### bu...@google.com (2026-03-18)

Something went wrong parsing your comment: Unexpected "on" when parsing command. See http://go/bugjuggler#how-to-use-it for examples.
Error highlighted: Bugjuggler: http://tap/tensorflow is green *on* cl/885789312

### re...@google.com (2026-03-18)

Bugjuggler: <http://tap/tensorflow> contains cl/885789312 and is green

### bu...@google.com (2026-03-18)

Hi. I've received your bug and will wait for cl/885789312 to be submitted and for the last green CL of http://tap/tensorflow to be greater than the submitted CL and then assign the bug to reillyg@google.com.

### dx...@google.com (2026-03-19)

Project: chromium/src  

Branch:  main  

Author:  Reilly Grant [reillyg@chromium.org](mailto:reillyg@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7683565>

Roll TFLite/LiteRT to Next Green Version

---


Expand for full commit details
```
     
    Version Changes: 
    XNNPACK: f1a5f31a23b9a0f5ccf027852731b11d1d1115d0 to 811d0bd388ba8f4853c5560b6e16a5af3e8b895a 
    tflite: 4e546f69670b48c230e2a2f79ccccd52e5920a01 to 67d816626bf264e3b142187768601a200cbe810d 
    litert: 2dd2d2cea38fec8762a0aff19fed86af2fdf72e9 to 6933ef7f5d338fb7c75f542443af104b09e0849f 
     
    Bug: 388311883 
    Fixed: 493310462 
    Cq-Include-Trybots: luci.chrome.try:optimization_guide-linux;luci.chrome.try:optimization_guide-mac-arm64;luci.chrome.try:optimization_guide-mac-x64;luci.chrome.try:optimization_guide-win32;luci.chrome.try:optimization_guide-win64 
    Include-Ci-Only-Tests: chromium.android:android-pie-arm64-rel|android_browsertests 
    Change-Id: Ibc9f1a0677bafe37d03f0ab1b0ae52a28ce37225 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7683565 
    Auto-Submit: Reilly Grant <reillyg@chromium.org> 
    Commit-Queue: Reilly Grant <reillyg@chromium.org> 
    Reviewed-by: Steven Holte <holte@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1602118}

```

---

Files:

- M `DEPS`
- M `third_party/litert/README.chromium`
- M `third_party/litert/src`
- M `third_party/tflite/README.chromium`
- M `third_party/tflite/src`
- M `third_party/xnnpack/BUILD.gn`
- M `third_party/xnnpack/README.chromium`
- M `third_party/xnnpack/build_identifier.c`
- M `third_party/xnnpack/src`

---

Hash: [77b4bf2e3f249e53833be98b98bb582c13a38ed3](https://chromiumdash.appspot.com/commit/77b4bf2e3f249e53833be98b98bb582c13a38ed3)  

Date: Thu Mar 19 18:22:29 2026


---

### ch...@google.com (2026-03-20)

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to stable (M146) because latest trunk commit (1602118) appears to be after stable branch point (1582197).

Merge review required: a commit with DEPS changes was detected.

Requesting merge to beta (M147) because latest trunk commit (1602118) appears to be after beta branch point (1596535).

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### 24...@project.gserviceaccount.com (2026-03-20)

ClusterFuzz testcase 5475875734716416 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1602064:1602086

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### re...@chromium.org (2026-03-20)

**Which CLs should be backmerged? (Please include Gerrit links.)**

<https://chromium.googlesource.com/external/github.com/tensorflow/tensorflow/+/8cedce08e98d8f11e3ee5ced7a25fb830ccfb935> needs to be cherry-picked onto <https://chromium.googlesource.com/external/github.com/tensorflow/tensorflow/+/refs/heads/chromium/7727>.

**Has this fix been verified on Canary to not pose any stability regressions?** Yes.   

**Does this fix pose any potential non-verifiable stability risks?** No.   

**Does this fix pose any known compatibility risks?** No.   

**Does it require manual verification by the test team?** No.

### dr...@chromium.org (2026-03-23)

No crashes in Canary. Approved to merge to M146 and M147.

### re...@chromium.org (2026-03-23)

Updating milestone flags. We only need this merged to M147.

### re...@chromium.org (2026-03-23)

Blocked on getting permission to push the cherry-pick into the TFLite repo ([issue 495385040](https://issues.chromium.org/issues/495385040)).

### dx...@google.com (2026-03-24)

Project: external/github.com/tensorflow/tensorflow  

Branch:  chromium/7727  

Author:  Reilly Grant [reillyg@google.com](mailto:reillyg@google.com)  

Link:    <https://chromium-review.googlesource.com/7698812>

[M147] Avoid casting dimensions to float in STRIDED\_SLICE ResizeOutputTensor

---


Expand for full commit details
```
     
    Single-precision floats can only precisely represent values up to 2^24. If the size of the output slice were too large the previous logic would calculate the incorrect output dimension. 
     
    (Cherry-picked from commit 8cedce08e98d8f11e3ee5ced7a25fb830ccfb935.) 
     
    PiperOrigin-RevId: 885789312 
    Bug: 493310462 
    Change-Id: I7a3a1fadc152b1716e8e45e0cdf1dc125f7d82fd

```

---

Files:

- M `tensorflow/lite/kernels/strided_slice.cc`

---

Hash: [b476481b77f6e939e813ac93df22a4a6e7a3dd57](https://chromiumdash.appspot.com/commit/b476481b77f6e939e813ac93df22a4a6e7a3dd57)  

Date: Tue Mar 24 18:42:42 2026


---

### pe...@google.com (2026-03-24)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### re...@chromium.org (2026-03-24)

This feature was not enabled in M144.

### sp...@google.com (2026-04-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $43000.00 for this report.

Rationale for this decision:
High quality. Memory corruption in a highly privileged process (e.g. GPU, network processes)  with bisect


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
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/493310462)*
