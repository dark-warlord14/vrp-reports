# V8 Sandbox Bypass: JSToWasmWrapperAsm accessible and allows type confusion

| Field | Value |
|-------|-------|
| **Issue ID** | [342866373](https://issues.chromium.org/issues/342866373) |
| **Status** | Fixed |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | Blink>JavaScript>Sandbox |
| **Reporter** | cl...@gmail.com |
| **Assignee** | sa...@google.com |
| **Created** | 2024-05-27 |
| **Bounty** | $5,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

VULNERABILITY DETAILS
By overwriting the code pointer on a function object, we can call JSToWasmWrapperAsm. The generated code (on x64) treats `rsi` (which contains the full JSFunction pointer) as a `WrapperBuffer` containing raw pointers, derefencing and calling sandbox-controllable pointers.

This happens as `JSToWasmWrapperAsm` uses the `kJSEntrypointTag` tag (i.e. untagged).

VERSION
V8 12.7.0, commit d4b2933dd0e9b51bd86227556062270384409c14

REPRODUCTION CASE
Please include a demonstration of the security bug, such as an attached HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE make the file as small as possible and remove any content not required to demonstrate the bug, or any personal or confidential information.

Please attach files directly, not in zip or other archive formats, and if you've created a demonstration site please also attach the files needed to reproduce the demonstration locally.

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: clubby789

## Attachments

- [arb-call.js](attachments/arb-call.js) (text/javascript, 1.2 KB)

## Timeline

### am...@chromium.org (2024-05-28)

The report is lacking detailed information and it is unclear if this report meets all the requirements of a valid V8 sandbox submission, but passing this along to saelo@ (who also happens to be current V8 security shepherd for your assessment

Setting as low (s3) severity and Security\_Impact-None as the V8 sandbox is not yet considered a security boundary

### cl...@gmail.com (2024-05-28)

To elaborate:

- In `CallJSFunction`, we load the entrypoint of the function using the indirect pointer 'code' field
- By overwriting the 'code' field of a `JSFunction`, an attacker can call any function within the code pointer table as long as it is untagged (i.e. uses a `SANDBOX_EXPOSED_DESCRIPTOR` with a tag of `kDefaultCodeEntrypointTag`/`kJSEntrypointTag`)
- One such function is the `JSToWasmWrapperAsm` builtin
- Calling this function in this way causes type confusion; it expects a `wrapper buffer` to be passed in `rdi` - this register *actually* contains the uncompressed pointer to the `JSFunction` object inside the V8 heap
- The wrapper buffer is expected to contain a number of registers, as well as a pointer to a function to be called
  In this way, the code is treating data inside the sandbox as an array of trusted pointers. It loads several general purpose and floating point registers from the buffer, finally calling a function pointer from the buffer.

In the demo attached, writing the `Sandbox.targetPage` pointer into the `JSFunction` object at the correct offset results in the pointer being trusted and called when the corrupted function object is called.

### cl...@appspot.gserviceaccount.com (2024-05-29)

Detailed Report: https://clusterfuzz.com/testcase?key=5107793525669888

Fuzzer: None
Job Type: linux_d8_sandbox_testing
Platform Id: linux

Crash Type: V8 sandbox violation
Crash Address: 
Crash State:
  NULL
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_d8_sandbox_testing&revision=94154

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5107793525669888

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### sa...@google.com (2024-05-29)

Nice find! Thanks! Seems like I assumed that these builtins were directly invoked from JavaScript/Wasm, but are actually internal builtins using a custom calling convention. This then leads to a calling convention mismatch and essentially a type confusion on the arguments. The descriptors should probably just be marked as INTERNAL\_DESCRIPTORS. Fix is here: <https://chromium-review.googlesource.com/c/v8/v8/+/5580045>

### ap...@google.com (2024-05-29)

Project: v8/v8
Branch: main

commit 8430125e7c0212a735600565b82ae43483bd788e
Author: Samuel Groß <saelo@chromium.org>
Date:   Wed May 29 11:49:31 2024

    [sandbox] Mark Wasm wrapper interface descriptors as internal
    
    These were incorrectly marked as sandbox-exposed descriptors even though
    they are not invoked via a JS/Wasm function and use a custom calling
    convention. As such, an attacker could invoke the respective builtins
    from within the sandbox (via the code pointer table, by e.g. overwriting
    the `code` field of a JSFunction), which would lead to a calling
    convention mismatch and a sandbox violation. This CL now marks these
    descriptors as internal descriptors. That way, they can no longer be
    invoked from within the sandbox.
    
    Bug: 342866373
    Change-Id: Icd62220b9ac8a6bd0011763440924ef7e979380e
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5580045
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Samuel Groß <saelo@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#94157}

M       src/codegen/interface-descriptors.h

https://chromium-review.googlesource.com/5580045


### 24...@project.gserviceaccount.com (2024-05-29)

ClusterFuzz testcase 5107793525669888 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_d8_sandbox_testing&range=94156:94157

If this is incorrect, please add the hotlistid:5432646 and re-open the issue.

### cl...@gmail.com (2024-07-05)

Since it's been a month, I just wanted to bump and ask if this is an eligible V8 sandbox submission.

### sa...@chromium.org (2024-07-08)

Sorry for the delay! This is definitely eligible. I'll bring this up with the VRP team and see if it can be prioritized.

### sp...@google.com (2024-07-17)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
V8 heap sandbox bypass reward


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-17)

Thank you for your efforts in discovering and reporting this V8 heap sandbox bypass -- nice work!

### pe...@google.com (2024-09-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/342866373)*
