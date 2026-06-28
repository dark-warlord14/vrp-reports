# OOB Write in GraphBuilderTflite::SerializeConv2d

| Field | Value |
|-------|-------|
| **Issue ID** | [492450478](https://issues.chromium.org/issues/492450478) |
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

The ARM ruy fast path computes the destination pointer in [MakeKernelParamsFloat](https://source.chromium.org/chromium/chromium/src/+/main:third_party/ruy/src/ruy/kernel_common.h;l=239) as `start_col * dst->layout.stride + start_row` using 32-bit signed arithmetic. Once the hidden transpose-convolution destination exceeds the safe `int` offset range, the pointer wraps and [ruy::KernelFloatNeon](https://source.chromium.org/chromium/chromium/src/+/main:third_party/ruy/src/ruy/kernel_arm.h;l=135) writes through an invalid address during WebNN dispatch.

> NOTE: this issue is different with the [issue 492350400](https://issues.chromium.org/issues/492350400) (the OOB write in the TFlite in the runtime\_shape.cc), since this one is the OOB write inside the ruy library of `ruy/kernel_common.h` caused by the integer overflow in `start_col * dst->layout.stride + start_row`.

### Details

[WebNNGraphBuilderImpl::ValidateGraphImpl](https://source.chromium.org/chromium/chromium/src/+/main:services/webnn/webnn_graph_builder_impl.cc;l=3087) rejects operands whose packed byte length exceeds the TFLite backend's [INT\_MAX cap](https://source.chromium.org/chromium/chromium/src/+/main:services/webnn/tflite/graph_builder_tflite.cc;l=614), but it never derives or bounds the hidden transpose-convolution scratch tensors that TFLite builds internally.

First, [ResizeCol2ImTensor](https://source.chromium.org/chromium/chromium/src/+/main:third_party/tflite/src/tensorflow/lite/kernels/transpose_conv.cc;l=205) resizes `col2im` to `[input_height * input_width, filter_height * filter_width * output_depth]` even though no corresponding WebNN operand exists:

```
  TF_LITE_ENSURE_EQ(context, NumElements(output_shape), 4);
  TfLiteIntArray* col2im_shape_array = TfLiteIntArrayCreate(2);
  const RuntimeShape& input_shape = GetTensorShape(input);
  const RuntimeShape& weights_shape = GetTensorShape(weights);
  col2im_shape_array->data[0] = input_shape.Dims(1) * input_shape.Dims(2);
  col2im_shape_array->data[1] =
      weights_shape.Dims(0) * weights_shape.Dims(1) * weights_shape.Dims(2);

```

Later, [tflite::optimized\_ops::TransposeConvV2](https://source.chromium.org/chromium/chromium/src/+/main:third_party/tflite/src/tensorflow/lite/kernels/internal/optimized/optimized_ops.h;l=5049) converts that same hidden buffer into a column-major GEMM destination whose total scalar slots are `input_image_size * filter_height * filter_width * output_depth`:

```
  const int input_image_size = input_shape.Dims(1) * input_shape.Dims(2);
...
  const int input_offset = input_image_size * input_depth;

```

The bad offset is created when `ruy` lowers that destination into ARM kernel parameters. [MakeKernelParamsFloat](https://source.chromium.org/chromium/chromium/src/+/main:third_party/ruy/src/ruy/kernel_common.h;l=239) still keeps the coordinates and strides in `std::int32_t` and computes the starting destination pointer with signed-`int` multiplication:

```
struct KernelParamsFloat {
  std::int32_t start_row;
  std::int32_t start_col;
  std::int32_t dst_rows;
  std::int32_t dst_cols;
  std::int32_t dst_stride;
  ...
};

params->dst_base_ptr =
    dst->data.get() + start_col * dst->layout.stride + start_row;
params->start_col = start_col;
params->dst_stride = sizeof(float) * dst->layout.stride;
params->dst_cols = dst->layout.cols;

```

If we build the following valid WebNN graph with:

- input: `[1, 8192, 10752, 1]`
- filter: `[1, 5, 5, 1]` with `filterLayout: "ohwi"`
- output: `[1, 8192, 10752, 1]`

Each declared float32 tensor is only `352321536` bytes, so Chromium accepts the graph. But the hidden transpose-convolution destination becomes `rows = 25`, `cols = 88080384`, for a total of `2202009600` float elements. That total is `54525953` larger than `INT32_MAX`. Because the destination is column-major, later kernel tiles use `start_col * 25` as the scalar base offset. `INT32_MAX / 25` is `85899345`, so once `start_col` reaches `85899352` or larger, `start_col * dst->layout.stride` overflows signed `int` before [ruy::KernelFloatNeon](https://source.chromium.org/chromium/chromium/src/+/main:third_party/ruy/src/ruy/kernel_arm.h;l=135) stores the block, leading to the OOB write in `ruy::KernelFloatNeon`.

### Bisection

This issue is introduced by the commit <https://source.chromium.org/chromium/_/chromium/external/github.com/google/ruy/+/ac7834ca5679bf28875f956e77741527af513a7a>, which introduce the integer overflow in `start_col * dst->layout.stride + start_row` in the `third_party/ruy/src/ruy/kernel_common.h`.

### Reproduction

Run chrome from ·[https://storage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-1598914.zip·](https://storage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-1598914.zip%C2%B7) with the following command:
···
./chrome --enable-features=ExperimentalWebMachineLearningNeuralNetwork,WebMachineLearningNeuralNetwork --no-sandbox poc.html
···
You would observe the invalid adderss write in `asan.txt` of the GPU process. This issues should only be reproduced on the arm device, hence this should affect the GPU process in the arm mac (Apple silicon chip devices) and the Android devices.

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 24.9 KB)
- [poc.html](attachments/poc.html) (text/html, 1.6 KB)
- [asan_windows.txt](attachments/asan_windows.txt) (text/plain, 22.7 KB)

## Timeline

### he...@gmail.com (2026-03-13)

Oh, there's typo in the `reproduction` section. It should be :

Download the chrome in `https://storage.googleapis.com/chromium-browser-asan/mac-release-arm64/asan-mac-release-1598431.zip`

Run:

```
./asan-mac-release-1598431/Chromium.app/Contents/MacOS/Chromium --enable-features=WebMachineLearningNeuralNetwork --disable-features=WebNNCoreML poc.html

```

You would observe the wild invalid write ASAN trace in the asan.txt of GPU process.

This could also be reproduced on the x64 device (not limited to the arm device), i.e., available on all platforms and devices. This is also reachable on the non-sandboxed Android GPU process.

The poc and the asan trace do not need to be changed.

### dc...@chromium.org (2026-03-16)

Marking this as "no security impact" due to (I think) the requirement of disabling an enabled-by-default feature.

### ni...@intel.com (2026-03-16)

@dc...@chromium.org, I don't have an Arm Mac for reproducing and debugging. Could you please assign to someone else?

### he...@gmail.com (2026-03-16)

Hi, I think this should also be reproduced on the x64 devices, since I double check the `KernelFloatAvx512`,`KernelFloatAvx2`,`KernelFloatAvx`, which also have the similar vulnerable implementation of `MakeKernelParamsFloat`. Hence I think you might be able to reproduce/debug it.

During the initial RCA, I only check the vulnerable `KernelFloatNeon` function, but the `MakeKernelParamsFloat` also have the similar issues, which is available on the x86/x64 platform, hence I think this issues should affect and be reproducible on all platforms.

Many thanks!

### ni...@intel.com (2026-03-16)

Thanks @he...@gmail.com, I can reproduce this issue on Windows with x64 asan build. Run

```
chrome.exe --enable-features=ExperimentalWebMachineLearningNeuralNetwork,WebMachineLearningNeuralNetwork --disable-features=WebNNOnnxRuntime,WebNNDirectML --no-sandbox ruy_poc.html

```

Attach the asan log, it crashes at `ruy::KernelFloatAvxCommon<32>(struct ruy::KernelParamsFloat<8, 8> const &) C:\b\s\w\ir\cache\builder\src\third_party\ruy\src\ruy\kernel_x86.h:704:11`

### dc...@chromium.org (2026-03-16)

OK, glad you were able to repro–I'll assign it back.

### cl...@appspot.gserviceaccount.com (2026-03-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5998149864816640.

### re...@chromium.org (2026-03-17)

Not sure why ClusterFuzz can't reproduce this on x64 if Ningxin can. Raising priority to P1 because this feature is enabled by default in M-147.

### dx...@google.com (2026-03-18)

Project: chromium/src  

Branch:  main  

Author:  Ningxin Hu [ningxin.hu@intel.com](mailto:ningxin.hu@intel.com)  

Link:    <https://chromium-review.googlesource.com/7672131>

WebNN: Prevent TransposeConv2d col2im temp buffer overflow in TFLite

---


Expand for full commit details
```
     
    Add a check to ensure the size of the internal col2im temporary tensor 
    used by TFLite's TransposeConvV2 implementation does not exceed the 
    maximum value of a 32-bit signed integer. 
     
    Bug: 492450478 
    Change-Id: I0e3935f9ca3c9d09fa99d74ee2d251f3385652f4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7672131 
    Reviewed-by: Hu, Ningxin <ningxin.hu@intel.com> 
    Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    Commit-Queue: Hu, Ningxin <ningxin.hu@intel.com> 
    Cr-Commit-Position: refs/heads/main@{#1601013}

```

---

Files:

- M `services/webnn/tflite/graph_builder_tflite.cc`

---

Hash: [9dcfa123f0e991bb059b387daf3e46a5dfc585a8](https://chromiumdash.appspot.com/commit/9dcfa123f0e991bb059b387daf3e46a5dfc585a8)  

Date: Wed Mar 18 04:06:33 2026


---

### he...@gmail.com (2026-03-18)

Thank you very much for the fix! I can verify that the fix commit works.

### ni...@intel.com (2026-03-18)

@he...@gmail.com thanks for the verification. Marked this issue fixed.

### re...@chromium.org (2026-03-19)

This fix has been on Canary for 24 hours. Requesting a merge.

### ch...@google.com (2026-03-19)

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

### re...@chromium.org (2026-03-19)

**Why does your merge fit within the merge criteria for these milestones?**  

It is a security issue.

**What changes specifically would you like to merge? Please link to Gerrit.**  

<https://chromium-review.googlesource.com/7672131>

**Have the changes been released and tested on canary?**  

Yes.

**Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?**  

Yes. It is enabled by default but kill-switchable with the `WebMachineLearningNeuralNetwork` flag.

**If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.**  

No.

### dr...@chromium.org (2026-03-20)

No crashes in Canary. Merge approved to M147

### re...@chromium.org (2026-03-21)

Please approve the merge request for [issue 492350400](https://issues.chromium.org/issues/492350400) as the CL here only applies cleanly on top of the fix for that issue.

### dx...@google.com (2026-03-23)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Ningxin Hu [ningxin.hu@intel.com](mailto:ningxin.hu@intel.com)  

Link:    <https://chromium-review.googlesource.com/7695058>

[M147] WebNN: Prevent TransposeConv2d col2im temp buffer overflow in TFLite

---


Expand for full commit details
```
     
    Add a check to ensure the size of the internal col2im temporary tensor 
    used by TFLite's TransposeConvV2 implementation does not exceed the 
    maximum value of a 32-bit signed integer. 
     
    (cherry picked from commit 9dcfa123f0e991bb059b387daf3e46a5dfc585a8) 
     
    Bug: 492450478 
    Change-Id: I0e3935f9ca3c9d09fa99d74ee2d251f3385652f4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7672131 
    Reviewed-by: Hu, Ningxin <ningxin.hu@intel.com> 
    Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    Commit-Queue: Hu, Ningxin <ningxin.hu@intel.com> 
    Cr-Original-Commit-Position: refs/heads/main@{#1601013} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7695058 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Reilly Grant <reillyg@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: Reilly Grant <reillyg@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7727@{#1311} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `services/webnn/tflite/graph_builder_tflite.cc`

---

Hash: [b6688a9d6456cccd11e71eba22ce365635d2a31e](https://chromiumdash.appspot.com/commit/b6688a9d6456cccd11e71eba22ce365635d2a31e)  

Date: Mon Mar 23 23:58:02 2026


---

### sp...@google.com (2026-05-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $43000.00 for this report.

Rationale for this decision:
High Quality with bisect and renderer bonus.  Sandbox escape / Memory corruption / RCE in a non-sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/492450478)*
