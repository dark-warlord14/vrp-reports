# OOB Write in GraphBuilderTflite::SerializeConv2d

| Field | Value |
|-------|-------|
| **Issue ID** | [492350400](https://issues.chromium.org/issues/492350400) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>WebML |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | ly...@google.com |
| **Created** | 2026-03-13 |
| **Bounty** | $23,000.00 |

## Description

### Summary

[GraphBuilderTflite::SerializeConv2d](https://source.chromium.org/chromium/chromium/src/+/main:services/webnn/tflite/graph_builder_tflite.cc;l=3982) lets WebNN lower a `conv2d` whose declared input, output, and filter tensors all remain below backend `tensor_byte_length_limit`, but it does not bound the implicit TFLite `im2col` temporary created during execution. TFLite [conv::Prepare](https://source.chromium.org/chromium/chromium/src/+/main:third_party/tflite/src/tensorflow/lite/kernels/conv.cc;l=479) computes that temporary in `size_t`, while [tflite::optimized\_ops::Im2col](https://source.chromium.org/chromium/chromium/src/+/main:third_party/tflite/src/tensorflow/lite/kernels/internal/optimized/optimized_ops.h;l=4949) later rebuilds the same shape through [RuntimeShape::FlatSize](https://source.chromium.org/chromium/chromium/src/+/main:third_party/tflite/src/tensorflow/lite/kernels/internal/runtime_shape.cc;l=54), which still multiplies dimensions in signed `int`. Once the backend-only temporary exceeds `INT32_MAX` elements, that flat-size arithmetic overflows and the WebNN GPU-process dispatch path reaches an invalid write inside `Im2col<float>`.

### Details

[WebNNGraphBuilderImpl::ValidateGraphImpl](https://source.chromium.org/chromium/chromium/src/+/main:services/webnn/webnn_graph_builder_impl.cc;l=3087) rejects operands whose packed byte length exceeds the TFLite backend's [INT\_MAX cap](https://source.chromium.org/chromium/chromium/src/+/main:services/webnn/tflite/graph_builder_tflite.cc;l=614), but it does not derive or bound the backend-generated `im2col` scratch tensor that float `CONV_2D` creates internally.

The descriptor-side limit comes from [WebNNGraphBuilderImpl::ValidateGraphImpl](https://source.chromium.org/chromium/chromium/src/+/main:services/webnn/webnn_graph_builder_impl.cc;l=3090) and the TFLite backend's [context properties](https://source.chromium.org/chromium/chromium/src/+/main:services/webnn/tflite/graph_builder_tflite.cc;l=614):

```
#if defined(ARCH_CPU_64_BITS)
  // Limit to INT_MAX for security reasons (similar to PartitionAlloc).
  static constexpr uint64_t kTensorByteLengthLimit =
      std::numeric_limits<int32_t>::max();
#else
  // Allocating 2GiB isn't practical on a 32-bit system. Use a 1GiB limit.
  static constexpr uint64_t kTensorByteLengthLimit = 1024 * 1024 * 1024;
#endif

```

That is enough for visible WebNN tensors, but not for TFLite's derived convolution scratch space. In the float conv preparer [tflite::ops::builtin::conv::Prepare](https://source.chromium.org/chromium/chromium/src/+/main:third_party/tflite/src/tensorflow/lite/kernels/conv.cc;l=479), the implicit `im2col` allocation is computed in `size_t`, so large backend-only temporaries remain allowed:

```
  const size_t im2col_bytes = static_cast<size_t>(batches) * out_height *
                              out_width * channels_in * filter_height *
                              filter_width * im2col_type_size; // [1] integer overflow here
  TF_LITE_ENSURE_STATUS(AllocateTemporaryTensorsIfRequired(
      context, node, is_hybrid, data->is_hybrid_per_channel, kernel_type,
      im2col_bytes));

```

The integer overflow happens in [1] because [RuntimeShape::FlatSize](https://source.chromium.org/chromium/chromium/src/+/main:third_party/tflite/src/tensorflow/lite/kernels/internal/runtime_shape.cc;l=54) still returns signed `int`, and [tflite::optimized\_ops::Im2col](https://source.chromium.org/chromium/chromium/src/+/main:third_party/tflite/src/tensorflow/lite/kernels/internal/optimized/optimized_ops.h;l=4949) uses that signed product to size and index the `im2col` buffer:

```
int RuntimeShape::FlatSize() const {
  int buffer_size = 1;
  const int* dims_data = reinterpret_cast<const int*>(DimsData());
  for (int i = 0; i < size_; i++) {
    buffer_size *= dims_data[i];
  }
  return buffer_size;
}

```

Therefore, we can build a valid WebNN graph with a dynamic float32 filter and these public tensors:

- input: `[1, 8192, 10752, 1]`
- filter: `[1, 5, 5, 1]`
- output: `[1, 8192, 10752, 1]`

Each declared tensor is only `352321536` bytes, so it passes Chromium's `INT_MAX` descriptor limit. But the backend `im2col` geometry becomes `row_shape = 88080384` and `col_shape = 25`, so `im2col_shape` needs `2202009600` float elements. That is `54525953` larger than `INT32_MAX`, so the signed `FlatSize()` multiplication overflows before `Im2col` zeroes and fills the temporary, leading to the out-of-bound WRITE.

### Bisection

This issue is introduced in the commit <https://source.chromium.org/chromium/_/chromium/external/github.com/tensorflow/tensorflow/+/174fbcfed43c816bdc98c760d2cd1705af27a819>. While it still failed to migrate im2col\_bytes integer overflow issue, the multiple calculations among the `int` type already overflows (due to the im2col\_type\_size is not limited on desktop actually) before finally assign the result to the im2col\_bytes.

### Reproduction

Download the chrome in `https://storage.googleapis.com/chromium-browser-asan/mac-release-arm64/asan-mac-release-1598431.zip`

Run:

```
./asan-mac-release-1598431/Chromium.app/Contents/MacOS/Chromium --enable-features=WebMachineLearningNeuralNetwork --disable-features=WebNNCoreML poc.html

```

You would observe the wild invalid write ASAN trace in the `asan.txt` of GPU process.

### Suggested Fix

In the Chromium side, we should add rejection for `conv2d` descriptors whose derived backend `im2col` element count exceeds the safe range of the TFLite kernel, so WebNN never hands this shape class to the vulnerable path. We may also want to add validation in the tflite side.

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 22.4 KB)
- [poc.html](attachments/poc.html) (text/html, 1.6 KB)
- [asan_linux.txt](attachments/asan_linux.txt) (text/plain, 18.4 KB)

## Timeline

### he...@gmail.com (2026-03-13)

NOTE: attach the asan trace on Linux on the ToT version, running with the same poc.

```
./chrome --no-sandbox --enable-features=ExperimentalWebMachineLearningNeuralNetwork,WebMachineLearningNeuralNetwork poc.html

```

### cl...@appspot.gserviceaccount.com (2026-03-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5314388521156608.

### 24...@project.gserviceaccount.com (2026-03-14)

Testcase 5314388521156608 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5314388521156608.

### he...@gmail.com (2026-03-14)

Seems that cf has internal error? Visiting the cf page just shows the cf's python error.

Appreciate if the security team can manually reproduce on it. Thank you.

### dc...@chromium.org (2026-03-16)

I was able to reproduce the crash; I wasn't able to convince Clusterfuzz to reproduce it on Linux (perhaps due to lack of GPU), but I'll assume the ASan trace attached in [comment #2](https://issues.chromium.org/issues/492350400#comment2) is accurate.

I /think/ this might be "none" for the security impact, but I'm not entirely sure either: on Mac, I can't repro without disabling WebNNCoreML, which is enabled by default–and on Linux, it seems to require ExperimentalWebMachineLearningNeuralNetwork which is also disabled by default. So I'll tag it as none for now, but please let me know if you're able to reproduce this without enabling disabled-by-default features or disabling enabled-by-default features.

### cl...@appspot.gserviceaccount.com (2026-03-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5894762351591424.

### re...@chromium.org (2026-03-16)

This should be reachable on any platform where we use TFLite, including Linux, macOS on Intel and Windows pre-24H2. I've re-uploaded the test case to ClusterFuzz with the correct command line switches (only `--enable-features=WebMachineLearningNeuralNetwork` should be necessary).

### re...@chromium.org (2026-03-16)

Lynne, please take a look at the integer overflow here.

### dx...@google.com (2026-03-17)

Project: chromium/src  

Branch:  main  

Author:  Lynne Jiang [lyjiang@google.com](mailto:lyjiang@google.com)  

Link:    <https://chromium-review.googlesource.com/7662595>

[webnn] Prevent Conv2d im2col buffer overflow in TFLite.

---


Expand for full commit details
```
     
    Add a check to ensure the size of the internal im2col temporary tensor 
    used by TFLite's Conv2d implementation does not exceed the maximum value 
    of a 32-bit signed integer. 
     
    Change-Id: Ifc1d06d24edfb7ba6c2d9191b693c47166e615c5 
    Bug: 492350400 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7662595 
    Commit-Queue: Lynne Jiang <lyjiang@google.com> 
    Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    Reviewed-by: Phillis Tang <phillis@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1600709}

```

---

Files:

- M `services/webnn/tflite/graph_builder_tflite.cc`

---

Hash: [202bf039b74e8930710e5d1f8ca0f0f7630f445c](https://chromiumdash.appspot.com/commit/202bf039b74e8930710e5d1f8ca0f0f7630f445c)  

Date: Tue Mar 17 19:03:50 2026


---

### ch...@google.com (2026-03-18)

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

### ly...@google.com (2026-03-18)

Fix confirmed on Chromium revision a9c23d2f. Validated that the out-of-bounds condition is caught and triggers the appropriate error response. [screenshot](https://screenshot.googleplex.com/8xPg8coEhidR9W5). Mark this bug as Fixed(Verified).

### ly...@google.com (2026-03-18)

**Why does your merge fit within the merge criteria for these milestones?**

This is a high-priority security fix (P1, S1 vulnerability) addressing an Out-Of-Bounds (OOB) write in WebNN's TFLite backend. Merging this is critical to protect users from potential exploits in M147 before it reaches Stable.

**What changes specifically would you like to merge? Please link to Gerrit.**

I would like to merge the validation check that prevents the Conv2d `im2col` buffer overflow.
Gerrit link: [https://chromium-review.googlesource.com/7662595](https://chromium-review.git.corp.google.com/c/chromium/src/+/7662595)

**Have the changes been released and tested on canary?**

Yes, the fix landed on 03/17 and merged in main and tested in Chromium revision a9c23d2f.

**Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?**

No, this is a strict security bug fix.

**[Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative?**

N/A.

**If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.**.

No further manual verification by the test team is required. I have already successfully verified the fix manually on the latest Chromium revision and confirmed the out-of-bounds condition is gracefully caught (see verification details and screenshot above).

### dx...@google.com (2026-03-19)

Project: chromium/src  

Branch:  main  

Author:  Reilly Grant [reillyg@chromium.org](mailto:reillyg@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7681973>

Roll TFLite/LiteRT to Next Green Version

---


Expand for full commit details
```
     
    Version Changes: 
    XNNPACK: ee91cc745bc715bfa38c5e8241aeb435ca59f433 to f1a5f31a23b9a0f5ccf027852731b11d1d1115d0 
    tflite: 24d66fbe6c5e87d291207494e4e83d39de3f7d90 to 4e546f69670b48c230e2a2f79ccccd52e5920a01 
    litert: 13469058b8ee37e2153481ba49644764666ad275 to 2dd2d2cea38fec8762a0aff19fed86af2fdf72e9 
     
    Bug: 388311883, 492350400 
    Cq-Include-Trybots: luci.chrome.try:optimization_guide-linux;luci.chrome.try:optimization_guide-mac-arm64;luci.chrome.try:optimization_guide-mac-x64;luci.chrome.try:optimization_guide-win32;luci.chrome.try:optimization_guide-win64 
    Include-Ci-Only-Tests: chromium.android:android-pie-arm64-rel|android_browsertests 
    Change-Id: I64792c881c49a3fa9e9831062c6ff516a75b6306 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7681973 
    Reviewed-by: Steven Holte <holte@chromium.org> 
    Commit-Queue: Reilly Grant <reillyg@chromium.org> 
    Auto-Submit: Reilly Grant <reillyg@chromium.org> 
    Commit-Queue: Steven Holte <holte@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1601681}

```

---

Files:

- M `DEPS`
- M `third_party/litert/README.chromium`
- M `third_party/litert/src`
- M `third_party/tflite/README.chromium`
- M `third_party/tflite/src`
- M `third_party/xnnpack/README.chromium`
- M `third_party/xnnpack/src`

---

Hash: [35aedc5d24e621dfe417c96c0866dc57544503a6](https://chromiumdash.appspot.com/commit/35aedc5d24e621dfe417c96c0866dc57544503a6)  

Date: Thu Mar 19 01:27:53 2026


---

### dr...@chromium.org (2026-03-21)

No crashes in Canary, approved for M147.

### dx...@google.com (2026-03-21)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Lynne Jiang [lyjiang@google.com](mailto:lyjiang@google.com)  

Link:    <https://chromium-review.googlesource.com/7689642>

[M147] [webnn] Prevent Conv2d im2col buffer overflow in TFLite.

---


Expand for full commit details
```
     
    Add a check to ensure the size of the internal im2col temporary tensor 
    used by TFLite's Conv2d implementation does not exceed the maximum value 
    of a 32-bit signed integer. 
     
    (cherry picked from commit 202bf039b74e8930710e5d1f8ca0f0f7630f445c) 
     
    Change-Id: Ifc1d06d24edfb7ba6c2d9191b693c47166e615c5 
    Bug: 492350400 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7662595 
    Commit-Queue: Lynne Jiang <lyjiang@google.com> 
    Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    Reviewed-by: Phillis Tang <phillis@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1600709} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7689642 
    Auto-Submit: Reilly Grant <reillyg@chromium.org> 
    Commit-Queue: Reilly Grant <reillyg@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7727@{#1080} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `services/webnn/tflite/graph_builder_tflite.cc`

---

Hash: [b0841751c935112ef42bf2b632211dbd415aa63c](https://chromiumdash.appspot.com/commit/b0841751c935112ef42bf2b632211dbd415aa63c)  

Date: Sat Mar 21 04:26:53 2026


---

### pe...@google.com (2026-03-21)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### re...@chromium.org (2026-03-21)

This feature was not enabled in M144.

### qk...@google.com (2026-03-25)

Labled 'LTS-NotApplicable-138/144' because the feature was not enabled by default in M138 and M144 according to the comment #18.

### sp...@google.com (2026-05-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $23000.00 for this report.

Rationale for this decision:
High quality with renderer and bisect bonus. Memory Corruption / RCE in a highly privileged process (e.g. GPU or network)


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/492350400)*
