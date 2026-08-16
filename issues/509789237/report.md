# [Security] Hole leakage into packed elements due to elided TDZ check in dynamic scope

| Field | Value |
|-------|-------|
| **Issue ID** | [509789237](https://issues.chromium.org/issues/509789237) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | v8 commit hash：c881fd2041aab48d976508be4a97d1fd59221ff6 |
| **Reporter** | gu...@gmail.com |
| **Assignee** | ve...@chromium.org |
| **Created** | 2026-05-05 |
| **Bounty** | $500.00 |

## Description

# Steps to reproduce the problem

1. Switch the commit hash of v8 to c881fd2041aab48d976508be4a97d1fd59221ff6
2. asan’s gn parameters:

```
v8_monolithic = true 
v8_use_external_startup_data = false 
is_component_build = false 
is_debug = true 
symbol_level = 2 
target_cpu = "x64" 
v8_enable_backtrace = true 
v8_enable_disassembler = true 
v8_enable_object_print = true 
v8_enable_verify_heap = true 
is_asan = true 
v8_fuzzilli = true

```

3. ./d8 /tmp/poc.js

# Problem Description

Fatal error in ../../src/objects/elements.cc, line 2822
Debug check failed: !IsTheHole(argument).

# Additional Comments

Minimum PoC will be given later.

# Summary

crash in v8

# Custom Questions

#### Type of crash:

tab

#### Crash state:

Fatal error in ../../src/objects/elements.cc, line 2822
Debug check failed: !IsTheHole(argument).

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 2.2 KB)
- [poc.js](attachments/poc.js) (text/javascript, 51.7 KB)
- [poc_min.js](attachments/poc_min.js) (text/javascript, 792 B)

## Timeline

### gu...@gmail.com (2026-05-05)

poc\_min.js

### cl...@appspot.gserviceaccount.com (2026-05-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6053819452522496.

### cl...@google.com (2026-05-06)

This analysis is AI-generated using the `v8-security-triaging` skill (Conversation ID: `7bb9da79-9b0e-455e-aadc-8ce5f99e66f0`).

- **Status:** Reproduced on `origin/main` (commit `d92dc7ec5d78`) using the provided `poc_min.js`.
- **Classification:** Vulnerability.
- **Rationale:** The bug allows leaking the internal `the_hole` value into a `PACKED_ELEMENTS` array via `Array.prototype.push.call`. The root cause is a failure in hole-check elision during scope analysis: when a function is forced into a dynamic scope (e.g., via `eval` or `with`), the compiler wrongly elides the TDZ hole check for certain variables.
- **Security Impact:** This is classified as a vulnerability because it violates a core V8 security invariant: packed arrays must never contain the internal hole sentinel. JIT-optimized code for packed arrays omits hole checks for performance; by injecting a hole into such an array, an attacker can create a type-confusion state. While defense-in-depth measures like `PushStackTraceAndDie` currently catch the hole when accessed in the interpreter/builtins, the initial corruption of the array's elements kind invariant is the primary vulnerability.
- **Local Reproduction Findings:**
  
  - **Reproduced:** Yes.
  - **Build Configuration:** `x64.debug` and `x64.release`.
  - **Verified Impact:** Confirmed `the_hole` is successfully pushed into a `PACKED_ELEMENTS` array. In debug builds, this triggers a `DCHECK(!IsTheHole(argument))` in `src/objects/elements.cc`. In release builds, the process safely terminates via `PushStackTraceAndDie` when the corrupted element is later accessed.
  - **GDB Backtrace Snippet:**
    ```
    #0 v8::base::OS::Abort() src/base/platform/platform-posix.cc:802
    #1 V8_Fatal(...) src/base/logging.cc:243
    #2 v8::internal::(anonymous namespace)::FastElementsAccessor<...>::AddArguments(...) src/objects/elements.cc:2822
    #3 v8::internal::Builtin_ArrayPush(...) src/builtins/builtins-array.cc:535
    
    ```
- **Reproduction:** Run `d8 poc_min.js`.
- **Proposed Owner:** `verwaest@chromium.org` (Scope/AST expert).

Comment created using go/buganizer-mcp-server

### cl...@chromium.org (2026-05-06)

Another hole leakage. It's still classified as vulnerability even though AI couldn't produce a crash from this. Please adjust as needed.

### 24...@project.gserviceaccount.com (2026-05-06)

Detailed Report: https://clusterfuzz.com/testcase?key=6053819452522496

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  !IsTheHole(argument) in elements.cc
  v8::internal::FastElementsAccessor<v8::internal::FastPackedObjectElementsAccesso
  v8::internal::ElementsAccessorBase<v8::internal::FastPackedObjectElementsAccesso
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=106396:106397

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6053819452522496

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### ch...@google.com (2026-05-07)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-05-07)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ch...@google.com (2026-05-07)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### 24...@project.gserviceaccount.com (2026-05-07)

ClusterFuzz testcase 6053819452522496 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=107116:107117

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### gu...@gmail.com (2026-05-07)

Reporter: Sullivan

### sp...@google.com (2026-05-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
Other Processes - v8 logic


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-03)

This is sufficiently serious that it should be merged to M150. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M150. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

### ch...@google.com (2026-06-03)

**M150** merge request created. **Please update [crbug/519445979](https://crbug.com/519445979) to have this merge reviewed.**

### is...@chromium.org (2026-06-03)

Hole leaks have no security impact these days as they are unmapped and any access on them will deterministically crash.

Reporter: You'd need to use the hole leak to show some other memory corruption to make this one count.

Same reasoning as in your other report: <https://crbug.com/508682215#comment11>.

### ch...@google.com (2026-08-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/509789237)*
