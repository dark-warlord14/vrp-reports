# Missing output channel divisibility check in grouped convolution leads to heap OOB read in the GPU process via WebNN

| Field | Value |
|-------|-------|
| **Issue ID** | [493708165](https://issues.chromium.org/issues/493708165) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>WebML |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | ly...@google.com |
| **Created** | 2026-03-18 |
| **Bounty** | $3,000.00 |

## Description

# Missing output channel divisibility check in grouped convolution leads to heap OOB read in the GPU process via WebNN

## Summary

The WebNN validation for `conv2d` with `groups > 1` checks that `input_channels % groups == 0` but omits the symmetric check that `output_channels % groups == 0`. When an attacker supplies a filter with an output channel count not divisible by the group count, the TFLite reference convolution kernel computes a truncated `filters_per_group` value that causes the inner loop to read input channels beyond the tensor boundary. Because the WebNN TFLite backend supplies input tensor data through `SetCustomAllocationForTensor`, the input buffer is a standalone heap allocation, and the out-of-bounds read is a direct heap overflow in the GPU process. Affected platforms: all platforms where the TFLite WebNN backend is active (Linux, macOS, Windows, ChromeOS).

## Bisect

### TFLite upstream — grouped conv reference kernel introduced

- Commit: `8ec0a3be4ccb1c13a32125ce9f17c3a919b36a68`
- Date: 2022-03-16
- Author: Weiyi Wang [weiyiw@google.com](mailto:weiyiw@google.com)
- Subject: Support group conv2d in reference kernels
- Piper: PiperOrigin-RevId: 435188767
- URL: <https://github.com/tensorflow/tensorflow/commit/8ec0a3be4ccb1c13a32125ce9f17c3a919b36a68>

This commit introduced `const int groups = input_depth / filter_input_depth; const int filters_per_group = output_depth / groups;` in `reference/conv.h` without checking `output_depth % groups == 0`. Integer division truncation causes `filters_per_group` to be too small, so the last few output channels compute a `group` index of `groups` (out of range `[0, groups-1]`), leading to OOB reads on the input tensor.

### Became web-reachable

- Commit: `ded4396ef94db6b715dda888751563a079f5497e`
- Date: 2024-03-12
- Author: Junwei Fu ([junwei.fu@intel.com](mailto:junwei.fu@intel.com))
- Subject: webnn: Support Conv2d in TFLite converter
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/5337479>

This commit added `SerializeConv2d` to the WebNN TFLite graph builder. It used `IsDepthwiseConv2d()` to route depthwise cases but let all other grouped conv (`groups > 1`) fall through to TFLite's `CONV_2D` operator without rejecting or validating `output_channels % groups == 0`.

## Root Cause

When a WebNN `conv2d` operation specifies `groups > 1`, the validation in `ValidateConv2dAndInferOutput` enforces only two constraints on the groups parameter:

```
// services/webnn/public/cpp/graph_validation_utils.cc:724-735
if (attributes.groups == 0) {
  return base::unexpected(
      ErrorWithLabel(label, "The groups should be greater than 0."));
}
if (input_info.channels % attributes.groups != 0 ||
    filter_input_channels != input_info.channels / attributes.groups) {
  return base::unexpected(ErrorWithLabel(
      label,
      "The groups must evenly divide the input channels to filter input "
      "channels."));
}

```

There is no check that `output_channels % groups == 0`. The TFLite `conv::Prepare` function similarly computes `data->groups = input_channel / filter_input_channel` without verifying the output side. When `groups != 1`, the TFLite evaluation path forces the reference kernel, which derives per-group assignments using truncated integer division:

```
// third_party/tflite/src/tensorflow/lite/kernels/internal/reference/conv.h:58-72
const int groups = input_depth / filter_input_depth;
const int filters_per_group = output_depth / groups;
...
for (int out_channel = 0; out_channel < output_depth; ++out_channel) {
  auto group = out_channel / filters_per_group;
  ...
  for (int in_channel = 0; in_channel < filter_input_depth; ++in_channel) {
    float input_value =
        input_data[Offset(input_shape, batch, in_y, in_x,
                          in_channel + group * filter_input_depth)];

```

When `output_depth` is not divisible by `groups`, `filters_per_group` is the floor of the true quotient. The remainder output channels produce a `group` index equal to `groups` itself rather than staying within the valid range `[0, groups - 1]`. The resulting channel offset `in_channel + group * filter_input_depth` then exceeds `input_depth`, causing a read past the end of the input tensor.

Consider a concrete construction: input shape `[1, 1, 1, 100]`, filter shape `[101, 1, 1, 50]`, and `groups = 2`. Validation passes because `100 % 2 == 0` and `filter_input_channels == 50 == 100 / 2`. The reference kernel then computes `filters_per_group = 101 / 2 = 50`. For `out_channel = 100`, `group = 100 / 50 = 2`, which is out of range. The inner loop reads at channel indices `100` through `149`, which lie 200 bytes past the 400-byte input buffer.

The input tensor's backing memory is allocated by `BufferContent::BufferContent` through `base::AlignedAlloc` and installed via `interpreter_->SetCustomAllocationForTensor`. This is a standalone heap allocation with ASAN redzones, so the out-of-bounds read is a genuine heap overflow rather than an intra-arena access.

The same truncated-division pattern is replicated in the quantized and hybrid Conv reference kernels in `reference/integer_ops/conv.h`, making int8 and int16 variants equally reachable through the QDQ fusion path.

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
python3 -m http.server 8889 --directory issue_tflite002_grouped_conv_oob --bind 127.0.0.1 &
ASAN_OPTIONS=detect_odr_violation=0 out/asan-release/chrome \
  --no-sandbox \
  --enable-features=WebMachineLearningNeuralNetwork \
  --user-data-dir=/tmp/poc-$(date +%s) \
  http://127.0.0.1:8889/poc.html

```

The GPU process crashes within seconds with an ASAN heap-buffer-overflow READ:

```
==PID==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7d043c8b03e0
READ of size 4 at 0x7d043c8b03e0 thread T78 (ThreadPoolForeg)
    #0 tflite::reference_ops::Conv(...) reference/conv.h:90
    #1 tflite::ops::builtin::conv::EvalFloat<kReference>(...) conv.cc:995
    ...
    #7 webnn::tflite::GraphImplTflite::ComputeResources::DoDispatch(...) graph_impl_tflite.cc:328

0x7d043c8b03e0 is located 0 bytes after 416-byte region [0x7d043c8b0240,0x7d043c8b03e0)
allocated by thread T84 (ThreadPoolSingl) here:
    #1 base::AlignedAlloc(...) aligned_memory.cc:35
    #2 webnn::tflite::BufferContent::BufferContent(...) buffer_content_tflite.cc:33

SUMMARY: AddressSanitizer: heap-buffer-overflow reference/conv.h:90 in tflite::reference_ops::Conv(...)

```

The complete ASAN log is in `asan.log`.

## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 16.8 KB)
- [poc.html](attachments/poc.html) (text/html, 3.3 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4911983371517952.

### 24...@project.gserviceaccount.com (2026-03-19)

Detailed Report: https://clusterfuzz.com/testcase?key=4911983371517952

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x7c5ce07804a0
Crash State:
  tflite::reference_ops::Conv
  void tflite::ops::builtin::conv::EvalFloat<
  TfLiteStatus tflite::ops::builtin::conv::EvalImpl<
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1356883:1356886

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4911983371517952

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### 24...@project.gserviceaccount.com (2026-03-19)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### re...@chromium.org (2026-03-19)

We should apply the suggested fix to the WebNN validation logic and check that this requirement is also captured in the specification.

### dx...@google.com (2026-03-20)

Project: chromium/src  

Branch:  main  

Author:  Lynne Jiang [lyjiang@google.com](mailto:lyjiang@google.com)  

Link:    <https://chromium-review.googlesource.com/7687895>

[webnn] Validate output channels are a multiple of groups in Conv2d.

---


Expand for full commit details
```
     
    Add a check in `ValidateConv2d` to ensure `output_channels % attributes.groups == 0`. This is a requirement for grouped convolutions. Add a unit test to cover this invalid case. 
     
    Bug: 493708165 
    Change-Id: Id83552a5fb2b95f84981f28ca7162331e17559cd 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7687895 
    Commit-Queue: Lynne Jiang <lyjiang@google.com> 
    Reviewed-by: Phillis Tang <phillis@chromium.org> 
    Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1602846}

```

---

Files:

- M `services/webnn/public/cpp/graph_validation_utils.cc`
- M `services/webnn/webnn_graph_impl_unittest.cc`

---

Hash: [c75f63de718803f929ada79ff96e9cb36d1acb2c](https://chromiumdash.appspot.com/commit/c75f63de718803f929ada79ff96e9cb36d1acb2c)  

Date: Fri Mar 20 21:20:32 2026


---

### ch...@google.com (2026-03-21)

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to beta (M147) because latest trunk commit (1602846) appears to be after beta branch point (1596535).

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### 24...@project.gserviceaccount.com (2026-03-21)

ClusterFuzz testcase 4911983371517952 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1602841:1602846

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### re...@chromium.org (2026-03-21)

**Which CLs should be backmerged? (Please include Gerrit links.)**  

<https://chromium-review.googlesource.com/7687895>

**Has this fix been verified on Canary to not pose any stability regressions?**  

Fix verified by unit tests and ClusterFuzz. Will see Canary stability data by Monday.

**Does this fix pose any potential non-verifiable stability risks?**  

No.

**Does this fix pose any known compatibility risks?**  

No, the cases blocked by this change were mathematically invalid.

**Does it require manual verification by the test team? If so, please describe required testing.**  

No.

### ch...@google.com (2026-03-21)

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

### dr...@chromium.org (2026-03-23)

No crashes in Canary, approved to merge to M147.

### ly...@google.com (2026-03-23)

**1. Why does your merge fit within the merge criteria for these milestones?**

This is a fix for a P1/S1 security vulnerability (heap OOB read in WebNN) that has already been verified.

**2. What changes specifically would you like to merge? Please link to Gerrit.**

<https://chromium-review.googlesource.com/c/chromium/src/+/7687895>

**3. Have the changes been released and tested on canary?**

Yes, the fix has been on Canary with no crashes observed (as noted in [comment #11](https://issues.chromium.org/issues/493708165#comment11)).

**4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?**

No, this is a security bug fix.

**5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative?**

N/A.

**6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.**

No, it has already been verified.

### dx...@google.com (2026-03-24)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Lynne Jiang [lyjiang@google.com](mailto:lyjiang@google.com)  

Link:    <https://chromium-review.googlesource.com/7695227>

[M147] [webnn] Validate output channels are a multiple of groups in Conv2d.

---


Expand for full commit details
```
     
    Add a check in `ValidateConv2d` to ensure `output_channels % 
    attributes.groups == 0`. This is a requirement for grouped convolutions. 
    Add a unit test to cover this invalid case. 
     
    (cherry picked from commit c75f63de718803f929ada79ff96e9cb36d1acb2c) 
     
    Bug: 493708165 
    Change-Id: Id83552a5fb2b95f84981f28ca7162331e17559cd 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7687895 
    Commit-Queue: Lynne Jiang <lyjiang@google.com> 
    Reviewed-by: Phillis Tang <phillis@chromium.org> 
    Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1602846} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7695227 
    Commit-Queue: Reilly Grant <reillyg@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7727@{#1320} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `services/webnn/public/cpp/graph_validation_utils.cc`
- M `services/webnn/webnn_graph_impl_unittest.cc`

---

Hash: [6ba947133675ff58aab508fdd430b0e2a046f6f9](https://chromiumdash.appspot.com/commit/6ba947133675ff58aab508fdd430b0e2a046f6f9)  

Date: Tue Mar 24 01:04:30 2026


---

### pe...@google.com (2026-03-24)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### re...@chromium.org (2026-03-24)

This feature was not enabled in M144.

### qk...@google.com (2026-03-27)

Labeled `LTS-NotApplicable-144`/`LTS-NotApplicable-138` because the feature was not enabled in M144 according to comment #15. 

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

### ch...@google.com (2026-06-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/493708165)*
