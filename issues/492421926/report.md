# OOB read in TFLite TransposeConvV2

| Field | Value |
|-------|-------|
| **Issue ID** | [492421926](https://issues.chromium.org/issues/492421926) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>WebML |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | ju...@intel.com |
| **Created** | 2026-03-13 |
| **Bounty** | $3,000.00 |

## Description

### Summary

WebNN TFLite backend accepts non-scalar `int4` concat outputs in [`MLGraphBuilder::concat`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/ml/webnn/ml_graph_builder.cc;l=1924) and [`ValidateConcatAndInferOutput`](https://source.chromium.org/chromium/chromium/src/+/main:services/webnn/public/cpp/graph_validation_utils.cc;l=531) using packed-byte limits, but vendored TFLite later reinterprets the same shape through signed-element arithmetic in [`RuntimeShape::FlatSize`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/tflite/src/tensorflow/lite/kernels/internal/runtime_shape.cc;l=54), so [`tflite::reference_ops::Concatenation<Int4>`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/tflite/src/tensorflow/lite/kernels/internal/reference/concatenation.h;l=106) can derive an invalid size for its output-buffer clear.

### Details

Blink's [`MLGraphBuilder::concat`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/ml/webnn/ml_graph_builder.cc;l=1924) forwards directly to [`ValidateConcatAndInferOutput`](https://source.chromium.org/chromium/chromium/src/+/main:services/webnn/public/cpp/graph_validation_utils.cc;l=531), and the Linux TFLite backend continues to advertise non-scalar `int4` concat support through [`GraphBuilderTflite::GetContextProperties`](https://source.chromium.org/chromium/chromium/src/+/main:services/webnn/tflite/graph_builder_tflite.cc;l=647). In the current implementation, concat validation checks type compatibility, rank compatibility, and per-dimension shape agreement outside the concat axis, then computes the output extent by summing that axis into a `uint32_t`. The resulting descriptor is accepted if [`OperandDescriptor::Create`](https://source.chromium.org/chromium/chromium/src/+/main:services/webnn/public/cpp/operand_descriptor.cc;l=31) can represent the tensor's packed byte length, so sub-byte tensor types are constrained by bytes rather than by the number of logical elements.

[`ValidateConcatAndInferOutput`](https://source.chromium.org/chromium/chromium/src/+/main:services/webnn/public/cpp/graph_validation_utils.cc;l=598):

```
  auto axis_size = base::CheckedNumeric<uint32_t>(0);
  for (auto& input : inputs) {
    axis_size += input.shape()[axis];
  }
  std::vector<uint32_t> output_shape = first_input_shape;
  if (!axis_size.AssignIfValid(&output_shape[axis])) {
    return base::unexpected(
        ErrorWithLabel(label, "The concatenated dimension size is too large."));
  }

  return OperandDescriptor::Create(context_properties, output_type,
                                   output_shape, label);

```

[`OperandDescriptor::PackedByteLength`](https://source.chromium.org/chromium/chromium/src/+/main:services/webnn/public/cpp/operand_descriptor.cc;l=143):

```
size_t OperandDescriptor::PackedByteLength() const {
  // Overflow checks are not needed here because this same calculation is
  // performed with overflow checking in `Create()`. `this` would not exist if
  // those checks failed.
  base::CheckedNumeric<uint64_t> checked_number_of_bytes =
      (base::CheckedNumeric<uint64_t>(GetBitsPerElement(data_type_)) *
           NumberOfElements() +
       7) /
      8;
  return checked_number_of_bytes.ValueOrDie<size_t>();
}

```

For an output shape such as `[46341, 46341]`, that distinction matters: the tensor contains `2,147,488,281` `int4` elements, which exceeds `INT_MAX`, but only `1,073,744,141` packed bytes, which still satisfies the WebNN descriptor checks and can therefore be lowered into TFLite. No corresponding guard rejects shapes whose packed representation is legal while their logical element count exceeds the range assumed by downstream TFLite code.

The downstream TFLite path still derives the total element count through signed `int` multiplication in [`RuntimeShape::FlatSize`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/tflite/src/tensorflow/lite/kernels/internal/runtime_shape.cc;l=54), and the `int4` concat implementation in [`tflite::reference_ops::Concatenation<Int4>`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/tflite/src/tensorflow/lite/kernels/internal/reference/concatenation.h;l=106) uses that result to compute the byte count for its initial buffer clear, and leading to the out-of-bound write (cleanup) for the buffer.

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
```
uint8_t* output_ptr = reinterpret_cast<uint8_t*>(output_data);
// Note: output_shape.FlatSize() gives number of elements (nibbles).
// Bytes needed: (elements + 1) / 2.
memset(output_ptr, 0, (output_shape.FlatSize() + 1) / 2); // integer overflow here, making it OOB write

```
### Bisection

This issue is introduced by the upstream commit `fa5e7a9a6cce915128c4f3362a5a6588cbb12e29` in <https://github.com/tensorflow/tensorflow/commit/fa5e7a9a6cce915128c4f3362a5a6588cbb12e29>, which introduces the vulnerable `int4` concat output-clear path in vendored TFLite.

### Reproduction

Run chrome from `https://storage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-1598914.zip` with the following command:

```
./chrome --enable-features=ExperimentalWebMachineLearningNeuralNetwork,WebMachineLearningNeuralNetwork --no-sandbox poc.html

```

You would observe the negative-size-param with ASAN in asan.txt, while the negative-size is pass to the memset, it would lead to the massive memory being OOB written in to the zero value. In the release mode, this would cause the OOB write actually.

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 63.8 KB)
- [poc.html](attachments/poc.html) (text/html, 1.0 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4829813130952704.

### 24...@project.gserviceaccount.com (2026-03-14)

ClusterFuzz testcase 4829813130952704 appears to be flaky, updating reproducibility hotlist.

### 24...@project.gserviceaccount.com (2026-03-14)

Detailed Report: https://clusterfuzz.com/testcase?key=4829813130952704

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Negative-size-param
Crash Address: 
Crash State:
  void tflite::reference_ops::Concatenation<tflite::Int4>
  TfLiteStatus tflite::ops::builtin::concatenation::EvalImpl<
  tflite::ops::builtin::concatenation::Prepare
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1599437

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4829813130952704

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

### dc...@chromium.org (2026-03-16)

Similar to the other bug, I'm tagging as none because `ExperimentalWebMachineLearningNeuralNetwork` appears to be disabled by default. If you're able to reproduce without changing feature values from their defaults, please let me know.

### re...@chromium.org (2026-03-16)

Only `--enabled-features=WebMachineLearningNeuralNetwork` is required for this, and that flag is enabled by default in M-147, with the Javascript API available to sites with an Origin Trial token.

### he...@gmail.com (2026-03-16)

Thank you very much. Could the security team please triage my another [issue 492668885](https://issues.chromium.org/issues/492668885) which is also w.r.t. TFLite.

Many thanks!

### ph...@chromium.org (2026-03-16)

The WebNN [checks the element size limit](https://source.chromium.org/chromium/chromium/src/+/main:services/webnn/public/cpp/operand_descriptor.h;l=69) but it's against size\_t instead of int. We also have kTensorByteLengthLimit which is set to INT\_MAX so that covered the element size limit for >=INT8 data types.

The [RuntimeShape::FlatSize](https://source.chromium.org/chromium/chromium/src/+/main:third_party/tflite/src/tensorflow/lite/kernels/internal/runtime_shape.cc;l=54) usage is quite widespread so I think changing it's return type to size\_t is too risky and likely have more overflows downstream.
So I think we should change the element size limit to be INT\_MAX in WebNN.

### dx...@google.com (2026-03-18)

Project: chromium/src  

Branch:  main  

Author:  Phillis Tang [phillis@chromium.org](mailto:phillis@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7671499>

webnn: Limit element count to INT\_MAX

---


Expand for full commit details
```
     
    TFLite has implicit element count limit of int32 max because 
    `RuntimeShape::FlatSize` returns int, this function usage is widespread 
    so the assumption of int32 is deeply baked into the codebase. 
    Update WebNN's element count limit to INT_MAX to match with TFLite 
    expectation. 
     
    Bug: 492421926 
    Change-Id: Id4d26e77900787cc001df99a58015d578b2c57f3 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7671499 
    Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    Reviewed-by: Phillis Tang <phillis@chromium.org> 
    Commit-Queue: Phillis Tang <phillis@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1601340}

```

---

Files:

- M `services/webnn/public/cpp/operand_descriptor.h`
- M `services/webnn/webnn_tensor_impl_backend_test.cc`

---

Hash: [0d0cb58c007f114b90f1d1c3baf1b9140ec16cbf](https://chromiumdash.appspot.com/commit/0d0cb58c007f114b90f1d1c3baf1b9140ec16cbf)  

Date: Wed Mar 18 16:12:00 2026


---

### dx...@google.com (2026-03-18)

Project: chromium/src  

Branch:  main  

Author:  Peter Kotwicz [pkotwicz@chromium.org](mailto:pkotwicz@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7682211>

Revert "webnn: Limit element count to INT\_MAX"

---


Expand for full commit details
```
     
    This reverts commit 0d0cb58c007f114b90f1d1c3baf1b9140ec16cbf. 
     
    Reason for revert: 
    WebNNTensorImplBackendTest.CreateTooLargeTensorTest  
    started failing on android-10-x86-nofieldtrial-rel bot after CL 
    landed 
     
    Original change's description: 
    > webnn: Limit element count to INT_MAX 
    > 
    > TFLite has implicit element count limit of int32 max because 
    > `RuntimeShape::FlatSize` returns int, this function usage is widespread 
    > so the assumption of int32 is deeply baked into the codebase. 
    > Update WebNN's element count limit to INT_MAX to match with TFLite 
    > expectation. 
    > 
    > Bug: 492421926 
    > Change-Id: Id4d26e77900787cc001df99a58015d578b2c57f3 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7671499 
    > Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    > Reviewed-by: Phillis Tang <phillis@chromium.org> 
    > Commit-Queue: Phillis Tang <phillis@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1601340} 
     
    Bug: 492421926 
    No-Presubmit: true 
    No-Tree-Checks: true 
    No-Try: true 
    Change-Id: I4d88db3fbf8268767ee4f3192b42d822ca42aefe 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7682211 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Reviewed-by: Phillis Tang <phillis@chromium.org> 
    Commit-Queue: Phillis Tang <phillis@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1601470}

```

---

Files:

- M `services/webnn/public/cpp/operand_descriptor.h`
- M `services/webnn/webnn_tensor_impl_backend_test.cc`

---

Hash: [454b9cd2fef9433f3c4301e911f01dd6c16339a2](https://chromiumdash.appspot.com/commit/454b9cd2fef9433f3c4301e911f01dd6c16339a2)  

Date: Wed Mar 18 19:54:17 2026


---

### dx...@google.com (2026-03-19)

Project: chromium/src  

Branch:  main  

Author:  Phillis Tang [phillis@chromium.org](mailto:phillis@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7682064>

Reland "webnn: Limit element count to INT\_MAX"

---


Expand for full commit details
```
     
    This is a reland of commit 0d0cb58c007f114b90f1d1c3baf1b9140ec16cbf 
     
    Fix the bot failure by ensure the byte length is within system size_t. 
     
    Original change's description: 
    > webnn: Limit element count to INT_MAX 
    > 
    > TFLite has implicit element count limit of int32 max because 
    > `RuntimeShape::FlatSize` returns int, this function usage is widespread 
    > so the assumption of int32 is deeply baked into the codebase. 
    > Update WebNN's element count limit to INT_MAX to match with TFLite 
    > expectation. 
    > 
    > Bug: 492421926 
    > Change-Id: Id4d26e77900787cc001df99a58015d578b2c57f3 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7671499 
    > Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    > Reviewed-by: Phillis Tang <phillis@chromium.org> 
    > Commit-Queue: Phillis Tang <phillis@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1601340} 
     
    Bug: 492421926 
    Change-Id: I9eeb097c0922b57e57119ab689ccc639c473edae 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7682064 
    Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    Reviewed-by: Phillis Tang <phillis@chromium.org> 
    Commit-Queue: Phillis Tang <phillis@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1602083}

```

---

Files:

- M `services/webnn/public/cpp/operand_descriptor.h`
- M `services/webnn/webnn_tensor_impl_backend_test.cc`
- M `third_party/blink/web_tests/external/wpt/webnn/validation_tests/dequantizeLinear.https.any.js`

---

Hash: [1258512d6b2e5c5f8f6d97fae079ddd8fd274dd5](https://chromiumdash.appspot.com/commit/1258512d6b2e5c5f8f6d97fae079ddd8fd274dd5)  

Date: Thu Mar 19 17:24:29 2026


---

### dx...@google.com (2026-03-19)

Project: chromium/src  

Branch:  main  

Author:  Phillis Tang [phillis@chromium.org](mailto:phillis@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7676164>

webnn: add wpt for element count limit

---


Expand for full commit details
```
     
    Add regression test for concat with output exceeding element count 
    limit. 
     
    Bug: 492421926 
    Change-Id: I2efec24eed28f4f202e1bf17f6b17bcbce6c00b5 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7676164 
    Reviewed-by: Phillis Tang <phillis@chromium.org> 
    Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    Commit-Queue: Phillis Tang <phillis@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1602152}

```

---

Files:

- M `third_party/blink/web_tests/external/wpt/webnn/validation_tests/concat.https.any.js`

---

Hash: [a634ab50c193e0c2520a28473a10c352f4313fca](https://chromiumdash.appspot.com/commit/a634ab50c193e0c2520a28473a10c352f4313fca)  

Date: Thu Mar 19 19:17:16 2026


---

### ph...@chromium.org (2026-03-20)

Requesting merge as I've verified the bug is fixed in canary

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

<https://chromium-review.googlesource.com/7682064>

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

Author:  Phillis Tang [phillis@chromium.org](mailto:phillis@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7694794>

Reland "webnn: Limit element count to INT\_MAX"

---


Expand for full commit details
```
     
    This is a reland of commit 0d0cb58c007f114b90f1d1c3baf1b9140ec16cbf 
     
    Fix the bot failure by ensure the byte length is within system size_t. 
     
    Original change's description: 
    > webnn: Limit element count to INT_MAX 
    > 
    > TFLite has implicit element count limit of int32 max because 
    > `RuntimeShape::FlatSize` returns int, this function usage is widespread 
    > so the assumption of int32 is deeply baked into the codebase. 
    > Update WebNN's element count limit to INT_MAX to match with TFLite 
    > expectation. 
    > 
    > Bug: 492421926 
    > Change-Id: Id4d26e77900787cc001df99a58015d578b2c57f3 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7671499 
    > Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    > Reviewed-by: Phillis Tang <phillis@chromium.org> 
    > Commit-Queue: Phillis Tang <phillis@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1601340} 
     
    (cherry picked from commit 1258512d6b2e5c5f8f6d97fae079ddd8fd274dd5) 
     
    Bug: 492421926 
    Change-Id: I9eeb097c0922b57e57119ab689ccc639c473edae 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7682064 
    Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    Reviewed-by: Phillis Tang <phillis@chromium.org> 
    Commit-Queue: Phillis Tang <phillis@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1602083} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7694794 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7727@{#1318} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `services/webnn/public/cpp/operand_descriptor.h`
- M `services/webnn/webnn_tensor_impl_backend_test.cc`
- M `third_party/blink/web_tests/external/wpt/webnn/validation_tests/dequantizeLinear.https.any.js`

---

Hash: [072baf3aaa336268f02561ada8654910f9d404ce](https://chromiumdash.appspot.com/commit/072baf3aaa336268f02561ada8654910f9d404ce)  

Date: Tue Mar 24 00:58:28 2026


---

### pe...@google.com (2026-03-24)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### re...@chromium.org (2026-03-24)

This feature was not enabled in M144.

### qk...@google.com (2026-03-25)

Labeled `LTS-NotApplicable-144`/`LTS-NotApplicable-138` because the feature was not enabled in M144 according to comment #19. 

### sp...@google.com (2026-05-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $18000.00 for this report.

Rationale for this decision:
Baseline with bisect and renderer bonus. Memory Corruption / RCE in a highly privileged process (e.g. GPU or network)


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

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/492421926)*
