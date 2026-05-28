# V8 Sandbox Bypass: compiled JS-to-WASM wrappers don't guard against `trusted_function_data` overwrites

| Field | Value |
|-------|-------|
| **Issue ID** | [361862752](https://issues.chromium.org/issues/361862752) |
| **Status** | Fixed |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2024-12053 |
| **Reporter** | ma...@popax21.dev |
| **Assignee** | jk...@chromium.org |
| **Created** | 2024-08-25 |
| **Bounty** | $5,000.00 |

## Description

WASM function calls originating from JavaScript go through a layer of wrapper functions whose purpose is to translate arguments to WASM objects and to set up the WASM stack frame. This wrapper can either be the generic Torque `JSToWasmWrapperHelper`, or a purpose-compiled wrapper created by `WasmWrapperGraphBuilder::BuildJSToWasmWrapper` for hot functions.

In the latter case, these compiled wrapper functions lack any guards against an attacker swapping the `trusted_function_data` pointer of the function with that of a function with a different signature. This results in type confusion, since the stack frame is still set up for the signature of the original function, while a different function is actually being called. One can use this to escape the V8 sandbox by using the type confusion primitive to construct arbitrary read/write as well as stack leak primitives.

This issue was reproduced with V8 commit `779c29ef6a4b0191efe579ff067754219e9b420b` with build flags as specified in the V8 sandbox bypass VRP rules. See the attached POC JS file for a sample which reproduces this issue and triggers the V8 sandbox escape checker.

A probable fix for this bug would be to add a signature hash check to the compiled wrapper functions, similar to those already guarding WASM-internal function calls. For example, this might be done in `WasmWrapperGraphBuilder::BuildCallAndReturn` (other code paths seem to also be able to compile down to a WASM function call; as such this may not be the only function which requires such a check).

Reporter credit: if applicable, please credit my pseudonym "Popax21" in regards to this bug.

## Attachments

- [bypass.js](attachments/bypass.js) (text/javascript, 3.1 KB)
- [bypass.js](attachments/bypass.js) (text/javascript, 3.1 KB)

## Timeline

### am...@chromium.org (2024-08-26)

Thank you for the report.
low severity and SI-None, since the V8 sandbox is not currently considered a security boundary; assigning to saelo@

### cl...@appspot.gserviceaccount.com (2024-08-26)

Detailed Report: https://clusterfuzz.com/testcase?key=5152031480152064

Fuzzer: None
Job Type: linux_d8_sandbox_testing
Platform Id: linux

Crash Type: V8 sandbox violation
Crash Address: 
Crash State:
  NULL
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_d8_sandbox_testing&revision=95801

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5152031480152064

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### sa...@google.com (2024-08-26)

Great, thanks for this report! The testcase reproduces on Clusterfuzz without any issues.

Jakob or Clemens, could one of you take a look? Thanks!

### cl...@chromium.org (2024-08-26)

Ack, nice report! I guess the first one who is done with their current project can take a look at this, as it's not time critical.

### jk...@chromium.org (2024-08-26)

Nah, IIUC this is WAI: we are not implementing sandbox hardening in Turbofan, which is about to be replaced. In Turboshaft wrappers this is already fixed via <https://chromium-review.googlesource.com/c/v8/v8/+/5622490>.

I'll leave it to folks like Samuel and Amy to decide whether this qualifies as a security bug, and/or is worth a VRP reward, and/or whether our VRP rules need any tuning to reflect that the V8 sandbox is only implemented in Turboshaft.

### sa...@google.com (2024-08-26)

Ok, great! So IIUC, our plan is to enable Turboshaft to replace Turbofan by default soon (I guess we already wanted to enable it but had to delay the rollout)? I think in that case we could just treat this bug as being fixed by the Turbofan deprecation then. It's a legitimate issue at the moment, but I understand that it doesn't make much sense to fix it in soon-to-be-dead code. Do you have a rough estimate for when we'll ship Turboshaft? Adjusting the rules is a bit complicated, but we could file a public issue that documents that Turbofan doesn't properly support the sandbox (but Turboshaft does). We are doing that also for other sandbox bypasses that take a longer time to fix.

### jk...@chromium.org (2024-08-26)

#7: The estimate for shipping Turboshaft is EOY 2023 (sic!). Or, failing that: next milestone, next milestone for sure!

### sa...@google.com (2024-08-26)

I see! :) I've filed <https://issues.chromium.org/issues/362191724> now to document this and I'll set this issue as a child issue also.

### ma...@gmail.com (2024-08-26)

Out of curiosity: was the fact that non-Turboshaft Turbofan doesn't support the sandbox documented publicly anywhere before this? The only existing resource relating to this bug I was able to find was [issue 336507783](https://issues.chromium.org/issues/336507783), which seems to be fixed, and doesn't mention Turboshaft directly in any way.

### sa...@google.com (2024-08-27)

I am not aware that this was documented pre [issue 362191724](https://issues.chromium.org/issues/362191724), no. I guess when some of these fixes where implemented, turboshaft was already shipping but then had to be rolled back. Anyway, I'm not going to deduplicate/close this report and we'll keep it open until the issue is fixed, one way or another. It's a legitimate bypass at the moment :)

### 24...@project.gserviceaccount.com (2024-08-30)

ClusterFuzz testcase 5152031480152064 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_d8_sandbox_testing&range=95869:95870

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### sa...@google.com (2024-08-30)

This shouldn't be fixed yet, probably just some offsets changed. I'll see if I can repair the test case next week.

### ma...@gmail.com (2024-08-30)

I've already prepared a repaired test case (changed the SFI pointer offset from 0x14 to 0x10); see the attached script.

### cl...@appspot.gserviceaccount.com (2024-09-02)

Detailed Report: https://clusterfuzz.com/testcase?key=6072616750088192

Fuzzer: None
Job Type: linux_d8_sandbox_testing
Platform Id: linux

Crash Type: V8 sandbox violation
Crash Address: 
Crash State:
  NULL
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_d8_sandbox_testing&revision=95911

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6072616750088192

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### sa...@google.com (2024-09-02)

Great, thanks a lot!

### sa...@chromium.org (2024-10-28)

This should now be fixed: [--turboshaft-wasm was enabled by default last week](https://chromium.googlesource.com/v8/v8.git/+/b34e0aa98b28bfbf07b1f8a2a1ec89f8ac89e21c).

### sp...@google.com (2024-11-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
V8 sandbox bypass reward


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-18)

Congratulations Matthias! Given that this was a valid bypass submission, we do consider this eligible for the V8 sandbox bypass reward. We appreciate your efforts and submitting this issue to us -- nice work!

### pe...@google.com (2025-02-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### am...@chromium.org (2025-05-05)

On Friday, 2 May 2025, a third-party reported to us that they have witnessed ITW exploitation of this sandbox bypass as part of an exploit chain involving an exploit for CVE-2024-12053, despite both issues being long since resolved and fixes (for both) being included in Stable channel of Chrome as of early January / 132.
(The fix for CVE-2024-12053 shipped a month earlier in December as part of a 131 Stable update.)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/361862752)*
