# heap-use-after-free in XNNPACK widen_fp16_accumulators

| Field | Value |
|-------|-------|
| **Issue ID** | [495864169](https://issues.chromium.org/issues/495864169) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P0 |
| **Component** | Blink>WebML |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | ly...@google.com |
| **Created** | 2026-03-24 |
| **Bounty** | $43,000.00 |

## Description

# VULNERABILITY DETAILS

A heap-use-after-free vulnerability exists in XNNPACK's subgraph optimization phase when processing WebNN graphs.

When XNNPACK optimizes subgraphs for FP16 inference, the `widen_fp16_accumulators` function is called to perform specific conversions. During this process, it caches raw pointers to internal `xnn_value` and `xnn_node` structures from the dynamically allocated `subgraph->values` and `subgraph->nodes` arrays [0] [1].

```
  struct xnn_value* reduced_value = &subgraph->values[node->inputs[0]]; // [0]
  struct xnn_value* arg_value = &subgraph->values[node->inputs[1]];
  struct xnn_node* reduce_node = &subgraph->nodes[reduced_value->producer];
  // ...
  struct xnn_value* output_value = &subgraph->values[output_id]; // [1]

```

To introduce a new conversion stage, it calls `xnn_define_tensor_value` [2] and passes `output_value->shape.dim` as the `dims` argument:

```
  enum xnn_status status = xnn_define_tensor_value( // [2]
      subgraph, xnn_datatype_fp32, output_value->shape.num_dims,
      output_value->shape.dim,
      /*data=*/NULL, XNN_INVALID_VALUE_ID,
      /*flags=*/0, &output_fp32_id);

```

Inside `xnn_define_tensor_value`, if the `subgraph->values` array lacks capacity, the internal allocation call (`xnn_subgraph_new_internal_value`) triggers a `realloc`, completely freeing the old tracking array. At this moment, the passed `dims` argument becomes a dangling pointer. `xnn_define_tensor_value` then proceeds to call `set_shape`, which executes a `memcpy` on the dangling pointer [3]:

```
static void set_shape(struct xnn_value* value, size_t num_dims, const size_t* dims) {
    // ...
    memcpy(value->shape.dim, dims, num_dims * sizeof(size_t));  // [3]
}

```

[0] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/subgraph.c;drc=f1a5f31a23b9a0f5ccf027852731b11d1d1115d0;l=2474>

[1] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/subgraph.c;drc=f1a5f31a23b9a0f5ccf027852731b11d1d1115d0;l=2509>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/subgraph.c;drc=f1a5f31a23b9a0f5ccf027852731b11d1d1115d0;l=2511>

[3] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/tensor.c;drc=f1a5f31a23b9a0f5ccf027852731b11d1d1115d0;l=43>

# BISECTION

Introduced by XNNPACK upstream commit [0] which replaced `optimize_common_subgraphs_scaled_sum_to_mean` with the buggy `widen_fp16_accumulators` function.

This regression was rolled into Chromium in commit [1].

[0] <https://github.com/google/XNNPACK/commit/de3504fd8cfcedf194cd0ae43afb37cdff824aa2> (Allow redundant reduction axes, and out of bounds reduction axes)

[1] <https://chromium.googlesource.com/chromium/src/+/4c34b3025a538acdc12e767e9bf9e96b1a76cbdc> (Roll TFLite/LiteRT to Next Green Version)

# VERSION

Chrome Version: HEAD

Operating System: Android, Linux

# REPRODUCTION CASE

1. This issue relies on native FP16 inference (e.g., ARM64 on Android). For testing on an x86/Linux environment, please apply the attached `x86_fp16_bypass.patch` to bypass the `xnn_is_f16_supported_natively` hardware check.
2. Build Chromium with HWASan (for Android) or ASan (for Linux).
3. Host the `poc.html` on an HTTP server.
4. Run Chrome against the PoC.

```
$ python3 -m http.server
$ ./out/asan/chrome --enable-features=WebMachineLearningNeuralNetwork "http://localhost:8000/poc.html"

```
# CRASH INFORMATION

Type of crash: GPU process

Crash log:

- Android (ARM64): See the attached `hwasan_android.txt` for the HWAddressSanitizer tag-mismatch (use-after-free) trace.
- Linux (x86): See the attached `asan_linux.txt` for the AddressSanitizer heap-use-after-free.

# SUGGESTED FIX

Based on similar upstream fixes on reshape (<https://github.com/google/XNNPACK/commit/474163f8aec45c77b48009eef6bb62886c3f25bd>), the most fundamental fix is to simply avoiding the creation of these extra nodes entirely.

See `fix.patch` for details.

# CREDIT INFORMATION

Reporter credit: Anonymous

## Attachments

- [asan_linux.txt](attachments/asan_linux.txt) (text/plain, 96.9 KB)
- [hwasan_android.txt](attachments/hwasan_android.txt) (text/plain, 190.2 KB)
- [poc.html](attachments/poc.html) (text/html, 2.2 KB)
- [fix.patch](attachments/fix.patch) (text/x-diff, 1.5 KB)
- [x86_fp16_bypass.patch](attachments/x86_fp16_bypass.patch) (text/x-diff, 670 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6171244898582528.

### wf...@chromium.org (2026-03-26)

clusterfuzz can't reproduce this, presumably because of the need for hardware support, but the reporter has a record of legitimate bugs and the bug looks very plausible so I am triaging this as sev critical as a web-accessible to unsandboxed (gpu process on android is unsandboxed).

### ch...@google.com (2026-03-27)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-27)

Setting Priority to P0 to match Severity s0. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### ds...@google.com (2026-03-27)

cl/890290919 should fix this (external PR: <https://github.com/google/XNNPACK/pull/9792>).

### ly...@google.com (2026-03-31)

Severity lowered as WebNN OT is no longer active. Final resolution is pending the next XNNPACK roll in Chromium.

### ch...@google.com (2026-04-01)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ly...@google.com (2026-04-01)

<https://github.com/google/XNNPACK/pull/9792> should be rolled into Chromium now, validated no crash in ToT, mark the bug as fixed.

### ch...@google.com (2026-04-08)

This is sufficiently serious that it should be merged to M148. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M148. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500600258](https://crbug.com/500600258) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500600496](https://crbug.com/500600496) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500600638](https://crbug.com/500600638) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500600863](https://crbug.com/500600863) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500601487](https://crbug.com/500601487) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500601981](https://crbug.com/500601981) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500602059](https://crbug.com/500602059) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500602062](https://crbug.com/500602062) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500603126](https://crbug.com/500603126) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500602987](https://crbug.com/500602987) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500604376](https://crbug.com/500604376) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500604498](https://crbug.com/500604498) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500604342](https://crbug.com/500604342) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500604408](https://crbug.com/500604408) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500605894](https://crbug.com/500605894) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500606411](https://crbug.com/500606411) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500605979](https://crbug.com/500605979) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500606813](https://crbug.com/500606813) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500606597](https://crbug.com/500606597) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500606717](https://crbug.com/500606717) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500607005](https://crbug.com/500607005) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500606770](https://crbug.com/500606770) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500606290](https://crbug.com/500606290) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500607880](https://crbug.com/500607880) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500608717](https://crbug.com/500608717) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500608814](https://crbug.com/500608814) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500608349](https://crbug.com/500608349) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500609912](https://crbug.com/500609912) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500610192](https://crbug.com/500610192) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500610258](https://crbug.com/500610258) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500609998](https://crbug.com/500609998) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500610738](https://crbug.com/500610738) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500610774](https://crbug.com/500610774) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500611047](https://crbug.com/500611047) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500611943](https://crbug.com/500611943) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500611355](https://crbug.com/500611355) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500612818](https://crbug.com/500612818) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500612426](https://crbug.com/500612426) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500612902](https://crbug.com/500612902) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500613340](https://crbug.com/500613340) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500613621](https://crbug.com/500613621) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500614062](https://crbug.com/500614062) to have this merge reviewed.**

### dr...@chromium.org (2026-04-08)

Sorry for the noise folks - we believe this is a novel edge case in our automation (https://crbug.com/500636350). I'll clean up the excess merge requests now.

### aj...@google.com (2026-04-23)

S0 as reachable on Android (still impact-none)

### sp...@google.com (2026-04-23)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $43000.00 for this report.

Rationale for this decision:
High Quality with Bisect. Memory corruption in a highly privileged process (e.g. GPU, network processes) 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2026-07-10)

This Blink bug has been marked as either a release blocker or a vulnerability bug. Blink bugs affect all OSs supported by Chrome (except iOS), so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/495864169)*
