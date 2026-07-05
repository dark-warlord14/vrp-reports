# Heap OOB write in XNNPACK Pool2D via integer overflow

| Field | Value |
|-------|-------|
| **Issue ID** | [494158331](https://issues.chromium.org/issues/494158331) |
| **Status** | New |
| **Severity** | S4-Minimal |
| **Priority** | P0 |
| **Component** | Blink>WebML |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | we...@intel.com |
| **Created** | 2026-03-19 |
| **Bounty** | $43,000.00 |

## Description

# VULNERABILITY DETAILS

An integer overflow vulnerability exists in the WebNN TFLite XNNPACK backend when processing `Pool2d` operations, leading to heap out-of-bounds write.

The root cause resides in the WebNN frontend graph validation `ValidatePool2dAndInferOutput`. It reads `windowDimensions` into `uint32_t` `window_height` and `window_width` without restricting their maximum product [0].

```
  uint32_t window_height = input_height;
  uint32_t window_width = input_width;
  if (attributes.window_dimensions) {
    if (attributes.window_dimensions->height == 0 ||
        attributes.window_dimensions->width == 0) {
      return base::unexpected(ErrorWithLabel(
          label, "All window dimensions should be greater than 0."));
    }
    window_height = attributes.window_dimensions->height;
    window_width = attributes.window_dimensions->width; // [0]

```

These unchecked values flow down to the XNNPACK engine where they are used to compute `pooling_size` [1]. By supplying large `windowDimensions` (e.g. `1000092567` and `1152814792`), the 64-bit unsigned product `pooling_size` can overflow the 2^60 boundary.

Later, XNNPACK calculates `step_height` [2] and subsequently `indirection_buffer_size` [3]. Crucially, `indirection_buffer_size` multiplies `(pooling_size - 1) + ...` by `sizeof(void*)` (8 bytes). This multiplication by 8 overflows the 64-bit `size_t` variable, causing the resulting allocation size to wrap around to a small number.

As a result, `xnn_reallocate_memory` allocates a smaller buffer than required [4].

```
  const size_t pooling_height = max_pooling_op->convolution_op->kernel_height;
  const size_t pooling_width = max_pooling_op->convolution_op->kernel_width;
  const size_t pooling_size = pooling_height * pooling_width; // [1]
  const size_t output_height = max_pooling_op->convolution_op->output_height;
  const size_t output_width = max_pooling_op->convolution_op->output_width;

  const size_t step_width =
    max_pooling_op->convolution_op->dilation_width > 1 ? pooling_width : min(max_pooling_op->convolution_op->stride_width, pooling_width);
  const size_t step_height = pooling_size + (output_width - 1) * step_width * pooling_height; // [2]

  if (input_height != max_pooling_op->convolution_op->last_input_height ||
      input_width != max_pooling_op->convolution_op->last_input_width ||
      channels != max_pooling_op->convolution_op->last_input_channels)
  {
    const size_t indirection_buffer_size = sizeof(void*) * ((pooling_size - 1) + output_height * step_height); // [3]
    const void** indirection_buffer =
      (const void**) xnn_reallocate_memory(max_pooling_op->convolution_op->indirection_buffer, indirection_buffer_size); // [4]

```

However, the memory initialization loop logic relies on the original `kernel_height` and `kernel_width` [5], causing the loop to iterate and write out-of-bounds pointers into the `indirection_buffer` [6].

```
        for (size_t output_x = 0; output_x < output_width; output_x++) {
          for (size_t pooling_x = 0; pooling_x < kernel_width; pooling_x++) { // [5]
            const size_t input_x = min(doz(output_x * stride_width + pooling_x * dilation_width, input_padding_left), input_x_max);
            const size_t index = output_y * step_height + output_x * step_width * kernel_height + pooling_x * kernel_height + pooling_y;
            indirection_buffer[index] = (const void*) ((uintptr_t) input + (input_y * input_width + input_x) * input_pixel_stride); // [6]
          }
        }

```

[0] <https://source.chromium.org/chromium/chromium/src/+/main:services/webnn/public/cpp/graph_validation_utils.cc;drc=2d6b112c7b9888854636d22cee0aa4b9990c4425;l=2241>

[1] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/operators/max-pooling-nhwc.c;drc=e2430de679d9d16bbff0b3c6f923cc84b6fe3042;l=476>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/operators/max-pooling-nhwc.c;drc=e2430de679d9d16bbff0b3c6f923cc84b6fe3042;l=482>

[3] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/operators/max-pooling-nhwc.c;drc=e2430de679d9d16bbff0b3c6f923cc84b6fe3042;l=488>

[4] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/operators/max-pooling-nhwc.c;drc=e2430de679d9d16bbff0b3c6f923cc84b6fe3042;l=490>

[5] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/indirection.c;drc=e2430de679d9d16bbff0b3c6f923cc84b6fe3042;l=419>

[6] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/indirection.c;drc=e2430de679d9d16bbff0b3c6f923cc84b6fe3042;l=422>

# BISECTION

Introduced by XNNPACK upstream commit <https://github.com/google/XNNPACK/commit/fae4eb257a2cf76c243d7a0cd123303f0e27ad2c> (Rewrite maxpool kernels) which replaced the bounded tile constant with the attacker-controlled pooling size when calculating the indirection buffer size.

This regression was rolled into Chromium in commit <https://chromium.googlesource.com/chromium/src/+/85fc641cf32e5687c9384f35053e1d3d3f4eea5a> (Roll TFLite to Next Green Version).

# VERSION

Chrome Version: HEAD

Operating System: Linux

# REPRODUCTION CASE

1. Build Chromium with Asan.
2. Host the `poc.html` on an HTTP server.
3. Run Chrome against the PoC.

```
$ python3 -m http.server
$ ./out/asan/chrome --enable-features=WebMachineLearningNeuralNetwork "http://localhost:8000/poc.html"

```
# CRASH INFORMATION

Type of crash: GPU process

Crash log: see the attached `asan.txt` ASan trace.

# SUGGESTED FIX

Add a `base::CheckedNumeric<uint32_t>` multiplication check to `ValidatePool2dAndInferOutput`.

See `fix.patch` for details.

# CREDIT INFORMATION

Reporter credit: Anonymous

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 37.3 KB)
- [fix.patch](attachments/fix.patch) (text/x-diff, 839 B)
- [poc.html](attachments/poc.html) (text/html, 1.7 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4519177004023808.

### re...@chromium.org (2026-03-19)

Adding Dillon for XNNPACK visibility, but we should probably fix this within Chromium.

Ningxin, can you assign someone from your team to take a look at this? We should probably be limiting both the window and padding dimensions as if they were tensors we were creating ourselves even though for this operator (in contrast to conv2d) they're only created internally.

### ds...@google.com (2026-03-19)

In general I suspect that WebNN should disallow kernel sizes, dilations, strides that are greater than some constant upper bound, e.g. 65535. This will avoid a ton of issues like this that an adversarial user could cause, but probably not something we want to disallow in XNNPACK in general.

I don't think any reasonable uses of these operators will use dilation/stride greater than some very small value, I think 65535 is massive overkill.

### 24...@project.gserviceaccount.com (2026-03-20)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2026-03-20)

Detailed Report: https://clusterfuzz.com/testcase?key=4519177004023808

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN WRITE
Crash Address: 0x798cac8564b8
Crash State:
  xnn_indirection_init_maxpool2d
  reshape_max_pooling2d_nhwc
  xnn_reshape_max_pooling2d_nhwc_f32
  
Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1483298:1483300

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4519177004023808

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### re...@chromium.org (2026-03-20)

This and [issue 493747582](https://issues.chromium.org/issues/493747582) seem very similar.

### dx...@google.com (2026-03-21)

Project: chromium/src  

Branch:  main  

Author:  Wei Wang [wei4.wang@intel.com](mailto:wei4.wang@intel.com)  

Link:    <https://chromium-review.googlesource.com/7687618>

[WebNN] Prevent Pool2d indirection buffer overflow in TFLite

---


Expand for full commit details
```
     
    Add a check to ensure the size of the internal indirection buffer used 
    by TFLite's Pool2d implementation does not exceed the maximum value 
    of a size_t integer. 
     
    Bug: 494158331 
    Change-Id: I984556f0f608badf8f73fcbb096da5f41170a958 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7687618 
    Reviewed-by: Hu, Ningxin <ningxin.hu@intel.com> 
    Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    Commit-Queue: Wang, Wei4 <wei4.wang@intel.com> 
    Cr-Commit-Position: refs/heads/main@{#1602966}

```

---

Files:

- M `services/webnn/tflite/graph_builder_tflite.cc`

---

Hash: [41c622eea2736d8702b556f1e0ab8fa8a6bf4662](https://chromiumdash.appspot.com/commit/41c622eea2736d8702b556f1e0ab8fa8a6bf4662)  

Date: Sat Mar 21 02:57:55 2026


---

### ch...@google.com (2026-03-21)

Setting Priority to P0 to match Severity s0. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### 24...@project.gserviceaccount.com (2026-03-21)

ClusterFuzz testcase 4519177004023808 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1602919:1602928

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2026-03-22)

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to beta (M147) because latest trunk commit (1602966) appears to be after beta branch point (1596535).

Merge review required: M147 is already shipping to beta.

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dr...@chromium.org (2026-03-23)

No crashes in Canary, approved to merge to M147.

### re...@chromium.org (2026-03-23)

Blocked on merging the fix for [issue 493310458](https://issues.chromium.org/issues/493310458) due to patch conflicts.

### re...@chromium.org (2026-03-24)

Will be able to cherry-pick this once <https://crrev.com/c/7695357> lands.

### dx...@google.com (2026-03-24)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Wei Wang [wei4.wang@intel.com](mailto:wei4.wang@intel.com)  

Link:    <https://chromium-review.googlesource.com/7695601>

[M147] [WebNN] Prevent Pool2d indirection buffer overflow in TFLite

---


Expand for full commit details
```
     
    Add a check to ensure the size of the internal indirection buffer used 
    by TFLite's Pool2d implementation does not exceed the maximum value 
    of a size_t integer. 
     
    (cherry picked from commit 41c622eea2736d8702b556f1e0ab8fa8a6bf4662) 
     
    Bug: 494158331 
    Change-Id: I984556f0f608badf8f73fcbb096da5f41170a958 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7687618 
    Reviewed-by: Hu, Ningxin <ningxin.hu@intel.com> 
    Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    Commit-Queue: Wang, Wei4 <wei4.wang@intel.com> 
    Cr-Original-Commit-Position: refs/heads/main@{#1602966} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7695601 
    Auto-Submit: Reilly Grant <reillyg@chromium.org> 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Reilly Grant <reillyg@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7727@{#1334} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `services/webnn/tflite/graph_builder_tflite.cc`

---

Hash: [4fa8782e06a61ed38c63e850187efec50bd55e23](https://chromiumdash.appspot.com/commit/4fa8782e06a61ed38c63e850187efec50bd55e23)  

Date: Tue Mar 24 03:50:53 2026


---

### pe...@google.com (2026-03-24)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### re...@chromium.org (2026-03-24)

This feature was not enabled in M144.

### qk...@google.com (2026-03-25)

Labeled `LTS-NotApplicable-144`/`LTS-NotApplicable-138` because the feature was not enabled in M144 according to comment #17. 

### sp...@google.com (2026-04-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $43000.00 for this report.

Rationale for this decision:
High quality. Memory corruption in a highly privileged process (e.g. GPU, network processes)  with bisect


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### dx...@google.com (2026-04-03)

Project: chromium/src  

Branch:  main  

Author:  Wei Wang [wei4.wang@intel.com](mailto:wei4.wang@intel.com)  

Link:    <https://chromium-review.googlesource.com/7702495>

[WebNN] Add wpt for the product of window dimensions limitation check for Pool2d

---


Expand for full commit details
```
     
    Add regression wpt test for the product of window dimensions 
    limitation check for Pool2d. 
     
    Bug: 494158331 
    Change-Id: Ida13b2c43ab5746d02aecb690301eb6343030412 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7702495 
    Reviewed-by: Hu, Ningxin <ningxin.hu@intel.com> 
    Reviewed-by: Phillis Tang <phillis@chromium.org> 
    Commit-Queue: Wang, Wei4 <wei4.wang@intel.com> 
    Cr-Commit-Position: refs/heads/main@{#1609621}

```

---

Files:

- M `third_party/blink/web_tests/external/wpt/webnn/validation_tests/pooling.https.any.js`

---

Hash: [f87c506ec7be0828f9409f96b19234f8287656c2](https://chromiumdash.appspot.com/commit/f87c506ec7be0828f9409f96b19234f8287656c2)  

Date: Fri Apr 3 01:56:03 2026


---

### ch...@google.com (2026-06-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/494158331)*
