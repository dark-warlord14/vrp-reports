# V8 Sandbox Bypass: AAR/W via WASM function signature confusion in TurboFan call_ref

| Field | Value |
|-------|-------|
| **Issue ID** | [352689356](https://issues.chromium.org/issues/352689356) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>JavaScript>Sandbox, Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2024-07-13 |
| **Bounty** | $5,000.00 |

## Description

### VULNERABILITY DETAILS

V8 sandbox bypass, arbitrary address read/write via wasm function signature confusion in TurboFan `call_ref` with in-sandbox exploit primitives.

To prevent signature confusion in `call_ref`, commit 47ac44d introduced `signature_hash` verification followed by commit a6f1ecd checking this for inlining candidates. Unfortunately this is not enforced for non-inlined `call_ref` in TurboFan compiled code, leading to wasm function signature confusion with in-sandbox exploit primitives.

### VERSION

V8 Version: a79a5ebdb0feca029979e3a647e88ea31a75d8a2

### REPRODUCTION CASE

Repro added as `call-ref-tf.js`.

### FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: Sandbox violation

### CREDIT INFORMATION

Reporter credit: Seunghyun Lee (@0x10n)

## Attachments

- [call-ref-tf.js](attachments/call-ref-tf.js) (text/javascript, 73.2 KB)

## Timeline

### se...@gmail.com (2024-07-15)

Note that TurboFan inlining also does not have any signature checks as Turboshaft also did not in <https://crrev.com/c/5621153>. This results in various anomalous behaviors, some that I've seen is:

- Abort due to `munmap_chunk(): invalid pointer` when inlining functions with mismatching return count, suspected to be a result of heap corruption within `WasmGraphBuildingInterface::CallRef()`
- Successful inlining of functions with mismatching signatures (verified with `--trace-wasm-inlining`) resulting in AAR/W, using the same method in <https://chromium-review.googlesource.com/c/v8/v8/+/5621153/3/test/mjsunit/sandbox/wasm-inlining-sigcheck.js> (but with no calls to the corrupted function to avoid `call_ref` signature checks from Liftoff code)

Thus it is necessary to employ signature verification in both the inlining code and in non-inlined `call_ref`.

### am...@chromium.org (2024-07-15)

Thank you for this sandbox bypass report, Seunghyun.

Assigning to saelo@ (who also happens to be current V8 shepherd)
sev=low since sandbox is not considered a security boundary

### cl...@appspot.gserviceaccount.com (2024-07-16)

Detailed Report: https://clusterfuzz.com/testcase?key=5067978221486080

Fuzzer: None
Job Type: linux_d8_sandbox_testing
Platform Id: linux

Crash Type: V8 sandbox violation
Crash Address: 
Crash State:
  NULL
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_d8_sandbox_testing&revision=95040

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5067978221486080

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### sa...@chromium.org (2024-07-16)

Thanks! Reproduces without any issues on CF

### jk...@chromium.org (2024-07-16)

Turbofan will be replaced before the sandbox will be a reliable security boundary (hopefully even before any patches landed now will reach the stable channel), so porting sandbox fixes to Turbofan isn't worth the effort (and was skipped intentionally in previous sandbox-related patches).

### se...@gmail.com (2024-07-16)

Re #6: Thanks, is Turbofan planned to be completely replaced with Turboshaft?

### jk...@chromium.org (2024-07-16)

Yes. What you get today with `--turboshaft-wasm --turboshaft-wasm-instruction-selection-staged` will be the default Very Soon Now™ (in fact, we were hoping to ship it half a year ago, but a series of last-minute blockers kept delaying it month after month). So Turbofan is in maintenance mode: we'll fix serious bugs (such as crashes) but won't add new features (such as sandbox hardening).

### pe...@google.com (2024-10-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### am...@chromium.org (2025-02-07)

Fixed by shipping turboshaft-wasm

### sp...@google.com (2025-02-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
V8 sandbox bypass reward (submission in initial iteration) 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-02-14)

Congratulations Seunghyun! Thanks for reaching out to bring this to our attention.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/352689356)*
