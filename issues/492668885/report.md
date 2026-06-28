# XNNPACK resizes output tensor

| Field | Value |
|-------|-------|
| **Issue ID** | [492668885](https://issues.chromium.org/issues/492668885) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>WebML |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | re...@chromium.org |
| **Assignee** | ju...@intel.com |
| **Created** | 2026-03-14 |
| **Bounty** | $3,000.00 |

## Description

### Summary

WebNN `convTranspose2d` with `outputPadding` or `outputSizes` causes a heap-buffer-overflow in TFLite’s [TransposeConvV2](https://source.chromium.org/chromium/chromium/src/+/main:third_party/tflite/src/tensorflow/lite/kernels/internal/optimized/optimized_ops.h;l=5015). The service-side [ConvertToConvTranspose2dAttributes](https://source.chromium.org/chromium/chromium/src/+/main:services/webnn/webnn_graph_builder_impl.cc;l=328) drops the adjustment fields and keeps only the final output shape, so [GetTfLitePaddingMode](https://source.chromium.org/chromium/chromium/src/+/main:services/webnn/tflite/graph_builder_tflite.cc;l=299) misclassifies the operation as `kTfLitePaddingSame`. TFLite then recomputes padding assuming zero adjustment, producing a geometry mismatch that overreads the temporary `col_data` buffer during `dispatch()`.

### Details

The bug is a semantic truncation across the Blink -> service boundary that cascades into a OOB read.

First, the Blink layer correctly preserves the transpose-conv adjustment geometry. [ConvertToConvTranspose2dAttributes](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/ml/webnn/ml_graph_builder.cc;l=650) captures both `outputPadding` and `outputSizes`:

```
const auto output_padding = options->getOutputPaddingOr({0, 0});
attributes.value().output_padding = webnn::Size2d<uint32_t>{
    .height = output_padding[0], .width = output_padding[1]};

if (options->hasOutputSizes()) {
  auto output_sizes = options->getOutputSizesOr({});
  attributes.value().output_sizes = webnn::Size2d<uint32_t>{
      .height = output_sizes[0], .width = output_sizes[1]};
}

```

**However, the service-side reconstruction discards this information.** The Mojo `Conv2d` type does not carry `outputPadding` or `outputSizes`. The service-side [ConvertToConvTranspose2dAttributes](https://source.chromium.org/chromium/chromium/src/+/main:services/webnn/webnn_graph_builder_impl.cc;l=328) reconstructs only the final output dimensions from the operand descriptor, losing the *reason* the output differs from canonical SAME geometry:

```
auto* output = GetMojoOperand(operands, conv2d.output_operand_id);
CHECK_EQ(output->descriptor.Rank(), 4u);
webnn::Size2d<uint32_t> output_sizes;
switch (context_properties.input_operand_layout) {
  case webnn::InputOperandLayout::kNhwc:
    output_sizes.height = output->descriptor.shape()[1];
    output_sizes.width = output->descriptor.shape()[2];
    component_attributes.filter_layout =
        ConvTranspose2dFilterOperandLayout::kOhwi;
    break;
  ...
}
component_attributes.output_sizes = std::move(output_sizes);

```

Consequently, the TFLite backend misclassifies the padding mode. Without the adjustment fields, it cannot distinguish canonical SAME from adjusted SAME. [GetTfLitePaddingMode](https://source.chromium.org/chromium/chromium/src/+/main:services/webnn/tflite/graph_builder_tflite.cc;l=299) selects `kTfLitePaddingSame` based solely on the explicit padding tuple, and [SerializeConv2d](https://source.chromium.org/chromium/chromium/src/+/main:services/webnn/tflite/graph_builder_tflite.cc;l=4024) lowers the operation with that mode plus the (adjusted) output-shape tensor:

```
if (explicit_padding == upper_padding) {
  return TfLitePadding{.mode = ::tflite::Padding_SAME};
}
...
op_inputs = {output_shape_tensor_index, filter_tensor_info.index,
             explicit_pad_index.value_or(input_tensor_info.index), bias_index};
operator_kind = ::tflite::BuiltinOperator_TRANSPOSE_CONV;
builtin_options = ::tflite::CreateTransposeConvOptions(
                      builder_, padding_mode.mode, conv2d.strides->width,
                      conv2d.strides->height, activation_type)
                      .Union();

```

At runtime, this mismatch causes a heap-buffer-overflow. [EvalFloat](https://source.chromium.org/chromium/chromium/src/+/main:third_party/tflite/src/tensorflow/lite/kernels/transpose_conv.cc;l=522) delegates to [TransposeConvV2](https://source.chromium.org/chromium/chromium/src/+/main:third_party/tflite/src/tensorflow/lite/kernels/internal/optimized/optimized_ops.h;l=5015), which recomputes SAME padding from the output dimensions assuming zero adjustment. Its `Col2im` loop traverses `col_data` using the recomputed geometry:

```
for (int h = 0; h < height_col; ++h) {
  int w_pad = -pad_l;
  for (int w = 0; w < width_col; ++w) {
    T* im_patch_data = im_data + (h_pad * width + w_pad) * depth;
    for (int ih = h_pad; ih < h_pad + filter_h; ++ih) {
      for (int iw = w_pad; iw < w_pad + filter_w; ++iw) {
        if (ih >= 0 && ih < height && iw >= 0 && iw < width) {
          for (int i = 0; i < depth; ++i) {
            im_patch_data[i] += col_data[i];
          }
        }
        im_patch_data += depth;
        col_data += depth;
      }

```

For example, with padding `[0,1,0,1]`, `stride=[2,2]`, `filter=[1,3,3,1]`, and an adjusted output like `7x7` / `7x6` / `6x7`, Chromium tells TFLite to use `SAME` but passes a non-canonical output extent. The `Col2im` traversal runs past the 340-byte temporary buffer, producing a heap-buffer-overflow.

### Bisection

This issue is introduced by the commit <https://chromium-review.googlesource.com/c/chromium/src/+/5635194>

### Reproduction

Run chrome from <https://storage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-1598914.zip> with the following command:

```
./chrome --enable-features=ExperimentalWebMachineLearningNeuralNetwork,WebMachineLearningNeuralNetwork --no-sandbox poc.html

```

You would observe the OOB shown in `asan.txt`

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 47.2 KB)
- [poc.html](attachments/poc.html) (text/html, 1.4 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6029985370275840.

### re...@chromium.org (2026-03-16)

Ningxin, can you find someone on your team to take a look at this as soon as possible?

### ni...@intel.com (2026-03-16)

Yes, Junwei will take a closer look at this issue.

### 24...@project.gserviceaccount.com (2026-03-17)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2026-03-17)

Detailed Report: https://clusterfuzz.com/testcase?key=6029985370275840

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x76c19ee6e1d4
Crash State:
  tflite::optimized_ops::TransposeConvV2
  void tflite::ops::builtin::transpose_conv::EvalFloat<
  TfLiteStatus tflite::ops::builtin::transpose_conv::Eval<
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1356883:1356886

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6029985370275840

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### ni...@intel.com (2026-03-17)

It looks like TFLite's [ComputePaddingHeightWidth](https://source.chromium.org/chromium/chromium/src/+/main:third_party/tflite/src/tensorflow/lite/kernels/transpose_conv.cc;l=841;drc=dde56340610b37d2f2696b654be50a74dd25ff84) assumes `dilation == 1` and `output padding == 0`.

Although mojo doesn't contain the output padding, it can be calculated by using existing attributes:

```
outputSizeWithoutOutputPadding = (inputSize - 1) * stride + (filterSize - 1) * dilation + 1 - beginningPadding - endingPadding
outputPadding = outputSize - outputSizeWithoutOutputPadding

```

When `outputPadding == 0`, we can follow the calculation of TFLite's `ComputePaddingHeightWidth` with `SAME` padding mode, and check whether the calculated total padding is equal to WebNN's.

There is another problem in `VALID` path. `PAD + VALID` DOESN'T work for transpose conv2d (although it works for direct conv2d). For transpose conv2d, it should crop (SLICE) the output after a full transpose conv2d (VALID, zero padding) rather than pad the input. We may need to pad the output

### re...@chromium.org (2026-03-17)

I suspect that that issue with transpose conv2d is part of what we've been trying to chase down in [issue 491869941](https://issues.chromium.org/issues/491869941).

### ch...@google.com (2026-03-18)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-18)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-03-19)

Project: chromium/src  

Branch:  main  

Author:  junwei [junwei.fu@intel.com](mailto:junwei.fu@intel.com)  

Link:    <https://chromium-review.googlesource.com/7677538>

WebNN: Use output size for TransposeConv SAME padding in TFLite

---


Expand for full commit details
```
     
    This CL aligns the TFLite backend's padding calculation for 
    convTranspose2d with the TFLite kernel implementation. 
     
    Previous implementation ignores WebNN convTranspose2d's non-zero output 
    padding which is not supported by TFLite SAME padding mode. However, 
    TFLite's TransposeConv kernel calculates 'SAME' padding by treating the 
    output size as the input to a regular convolution formula. 
     
    This CL also fixes an issue of the previous implementation that 
    incorrectly pads the input of transpose conv for explicit paddings 
    (crbug.com/491869941) by rejecting it. It should crop the output after 
    zero-padding (VALID) transpose conv instead. It will be implemented in a 
    separate CL. 
     
    Bug: 492668885, 491869941 
    Change-Id: Ibfbcd2bf9b80b6ab2b2f0fccf9596975537f9cc8 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7677538 
    Reviewed-by: Hu, Ningxin <ningxin.hu@intel.com> 
    Commit-Queue: Fu, Junwei <junwei.fu@intel.com> 
    Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1601883}

```

---

Files:

- M `services/webnn/tflite/graph_builder_tflite.cc`
- M `third_party/blink/web_tests/platform/mac/virtual/webnn-service-with-gpu/external/wpt/webnn/conformance_tests/conv_transpose2d.https.any_gpu-expected.txt`
- M `third_party/blink/web_tests/virtual/webnn-service-on-cpu/external/wpt/webnn/conformance_tests/conv_transpose2d.https.any_cpu-expected.txt`
- M `third_party/blink/web_tests/virtual/webnn-service-on-npu/external/wpt/webnn/conformance_tests/conv_transpose2d.https.any_npu-expected.txt`

---

Hash: [d141d62357df25a1ed50dc8494a73dca4fffa29c](https://chromiumdash.appspot.com/commit/d141d62357df25a1ed50dc8494a73dca4fffa29c)  

Date: Thu Mar 19 11:36:10 2026


---

### 24...@project.gserviceaccount.com (2026-03-19)

Detailed Report: https://clusterfuzz.com/testcase?key=6029985370275840

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x76c19ee6e1d4
Crash State:
  tflite::optimized_ops::TransposeConvV2
  void tflite::ops::builtin::transpose_conv::EvalFloat<
  TfLiteStatus tflite::ops::builtin::transpose_conv::Eval<
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1356883:1356886

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6029985370275840

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### re...@chromium.org (2026-03-19)

Ignore the above. ClusterFuzz is still working on verifying the fix.

### 24...@project.gserviceaccount.com (2026-03-19)

ClusterFuzz testcase 6029985370275840 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1601879:1601886

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2026-03-20)

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to beta (M147) because latest trunk commit (1601883) appears to be after beta branch point (1596535).

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

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

**Which CLs should be backmerged? (Please include Gerrit links.)**  

<https://chromium-review.googlesource.com/7677538>

**Has this fix been verified on Canary to not pose any stability regressions?**  

Yes.

**Does this fix pose any potential non-verifiable stability risks?**  

No.

**Does this fix pose any known compatibility risks?**  

No, it either fixes graphs which should've computed correctly or takes a few cases where we produced an error or incorrect results and throws a better error.

**Does it require manual verification by the test team? If so, please describe required testing.**  

No.

**Why does your merge fit within the merge criteria for these milestones?**  

It is a security issue.

**What changes specifically would you like to merge? Please link to Gerrit.**  

Answered above.

**Have the changes been released and tested on canary?**  

Answered above.

**Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?**  

Yes. It is enabled by default but kill-switchable with the `WebMachineLearningNeuralNetwork` flag.

**If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.**  

No.

### dr...@chromium.org (2026-03-23)

No crashes in Canary, approved to merge to M147.

### re...@chromium.org (2026-03-23)

Blocked on landing <https://crrev.com/c/7695058> first to avoid a merge conflict.

### dx...@google.com (2026-03-24)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  junwei [junwei.fu@intel.com](mailto:junwei.fu@intel.com)  

Link:    <https://chromium-review.googlesource.com/7693608>

[M147] WebNN: Use output size for TransposeConv SAME padding in TFLite

---


Expand for full commit details
```
     
    This CL aligns the TFLite backend's padding calculation for 
    convTranspose2d with the TFLite kernel implementation. 
     
    Previous implementation ignores WebNN convTranspose2d's non-zero output 
    padding which is not supported by TFLite SAME padding mode. However, 
    TFLite's TransposeConv kernel calculates 'SAME' padding by treating the 
    output size as the input to a regular convolution formula. 
     
    This CL also fixes an issue of the previous implementation that 
    incorrectly pads the input of transpose conv for explicit paddings 
    (crbug.com/491869941) by rejecting it. It should crop the output after 
    zero-padding (VALID) transpose conv instead. It will be implemented in a 
    separate CL. 
     
    (cherry picked from commit d141d62357df25a1ed50dc8494a73dca4fffa29c) 
     
    Bug: 492668885, 491869941 
    Change-Id: Ibfbcd2bf9b80b6ab2b2f0fccf9596975537f9cc8 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7677538 
    Reviewed-by: Hu, Ningxin <ningxin.hu@intel.com> 
    Commit-Queue: Fu, Junwei <junwei.fu@intel.com> 
    Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1601883} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7693608 
    Auto-Submit: Reilly Grant <reillyg@chromium.org> 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Reilly Grant <reillyg@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7727@{#1328} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `services/webnn/tflite/graph_builder_tflite.cc`
- M `third_party/blink/web_tests/platform/mac/virtual/webnn-service-with-gpu/external/wpt/webnn/conformance_tests/conv_transpose2d.https.any_gpu-expected.txt`
- M `third_party/blink/web_tests/virtual/webnn-service-on-cpu/external/wpt/webnn/conformance_tests/conv_transpose2d.https.any_cpu-expected.txt`
- M `third_party/blink/web_tests/virtual/webnn-service-on-npu/external/wpt/webnn/conformance_tests/conv_transpose2d.https.any_npu-expected.txt`

---

Hash: [dd2df93c85ca0d36af3f4e53bafae21f066a1f98](https://chromiumdash.appspot.com/commit/dd2df93c85ca0d36af3f4e53bafae21f066a1f98)  

Date: Tue Mar 24 02:40:18 2026


---

### pe...@google.com (2026-03-24)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### re...@chromium.org (2026-03-24)

This feature was not enabled in M147.

### qk...@google.com (2026-03-25)

Labeled `LTS-NotApplicable-144`/`LTS-NotApplicable-138` because the feature was not enabled in M144 according to comment #22. 

### sp...@google.com (2026-05-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline with bisect. User information disclosure


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Baseline with bisect. User information disclosure

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/492668885)*
