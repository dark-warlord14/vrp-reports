# V8 Sandbox Bypass: AAW/PC control via type confusion for wasm exports in DebugBreakTrampoline

| Field | Value |
|-------|-------|
| **Issue ID** | [487213150](https://issues.chromium.org/issues/487213150) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | kr...@gmail.com |
| **Assignee** | ol...@chromium.org |
| **Created** | 2026-02-24 |
| **Bounty** | $5,000.00 |

## Description

### VULNERABILITY DETAILS

#### Details

> **Note:** This is being filed as a sandbox bypass as I don't actually know whether it's possible to normally install DebugBreakTrampoline on wasm exports. If it is possible, this actually leads to (mitigated?) renderer code execution.

Notice for WASM cases [CSA:GetSharedFunctionInfoCode loads the wrapper\_code field and casts it to Code](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/codegen/code-stub-assembler.cc;l=18582-18584;drc=5e5e2747d663a648f3ccca0ac91cd794763d7f40). This is wrong and trivially leads to type confusion as that field is actually an indirect pointer handle and not Code.

This is used to demonstrate a sandbox bypass by flooding the CodePointerTable such that a WASM export function's Code handle puns as a caged pointer into the writable V8 heap with forged Code that appears to takes fewer arguments than it really does. DebugBreakTrampoline is then installed on the WASM export and used to trigger under-application and imbalance the stack to obtain AAW/PC control as in the past.

### VERSION

V8 commit: feac87b355b1c547b3340f3b3fe1f2f829849cce

#### REPRODUCTION CASE

**NOTE (for the shepherd):** To reproduce in CF, the `linux_d8_sandbox_testing` job type with the below shell args should hopefully do the trick.

**Shell args**: `--allow-natives-syntax --sandbox-testing`

**Build args**:

```
is_debug=false
is_asan=true
v8_enable_sandbox=true
v8_enable_memory_corruption_api=true
dcheck_always_on=false
target_cpu="x64"

```

**Sample output (`--disable-in-process-stack-traces` used to show PC)**:

```
$ ./d8 --allow-natives-syntax --sandbox-testing --disable-in-process-stack-traces ./wasm-debugbreaktrampoline-poc.js 
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x7a4300000000,0x7b4300000000)

## V8 sandbox violation detected!

AddressSanitizer:DEADLYSIGNAL
=================================================================
==36183==ERROR: AddressSanitizer: SEGV on unknown address 0x424242424242 (pc 0x424242424242 bp 0x7ffec29222e8 sp 0x7ffec29224e0 T0)
==36183==The signal is caused by a READ memory access.
    #0 0x424242424242  (<unknown module>)

==36183==Register values:
rax = 0x00007a4300000011  rbx = 0x00007a4300000011  rcx = 0x0000000000000002  rdx = 0x0000424242424242  
rdi = 0x0000000000000000  rsi = 0x0000000000000000  rbp = 0x00007ffec29222e8  rsp = 0x00007ffec29224e0  
 r8 = 0x0000000000000001   r9 = 0x0000000000000000  r10 = 0x000055afdcd831ad  r11 = 0x00007ffec29222b1  
r12 = 0x00007ffec29221d0  r13 = 0x00007e94d53e1080  r14 = 0x00007a4300000000  r15 = 0x00007e54d53e0849  
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV (<unknown module>) 
==36183==ABORTING

```
### FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: Sandbox violation

### CREDIT INFORMATION

Reporter credit: Krishna Ravishankar (@krsh732)

## Attachments

- [wasm-debugbreaktrampoline-poc.js](attachments/wasm-debugbreaktrampoline-poc.js) (text/javascript, 2.0 KB)
- [wasm-debugbreaktrampoline-poc-cf.js](attachments/wasm-debugbreaktrampoline-poc-cf.js) (text/javascript, 2.0 KB)

## Timeline

### li...@chromium.org (2026-02-24)

Reassigning to V8 shepherd for further triage.

### kr...@gmail.com (2026-02-24)

I posted the following CLs:

- <https://crrev.com/c/7604772> (should fix the type confusion in CSA::GetSharedFunctionInfoCode)
- <https://crrev.com/c/7603043> (makes the runtime function get the SFI Code for DebugBreakTrampoline instead as per this [TODO](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/builtins/builtins-internal-gen.cc;l=114-117;drc=8c6dcc24e7a0a4330c8941da634587910dac0e81) to avoid any future issues relating to desyncs between SFI::GetCode vs CSA::GetSharedFunctionInfoCode).

### md...@google.com (2026-02-25)

Assign to Oliver, who last modified that code.

### cl...@appspot.gserviceaccount.com (2026-02-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5263809308459008.

### sa...@google.com (2026-02-26)

Great find, thanks for the report! @md...@google.com please also try to reproduce these crashes on CF, that's usually helpful if it works :) I uploaded the testcase now.

I was wondering how this code ever worked at all, and I guess the answer is "it didn't", but we don't really seem to use `CSA::GetSharedFunctionInfoCode` outside of the DebugBreakTrampoline, and presumably we never get there with a Wasm function? I think it'd be good to have a small, back-mergeable fix for this issue, but afterwards we should also think of some more thorough fixes. The whole SFI::function\_data mechanism is still pretty fragile I think. It's mostly an artifact of how V8 worked pre-sandbox, but maybe it'd be possible to do some bigger refactoring there eventually. Could we get rid of `CSA::GetSharedFunctionInfoCode` entirely? I'm also wondering if we should enforce type-checks on casts of TrustedObjects in CSA similar to how we now do that in C++ casts?

### kr...@gmail.com (2026-02-26)

Re [comment#5](https://issues.chromium.org/issues/487213150#comment5): Ah, my bad, I had the disassembler on when I was writing/testing the PoC. Can just change line 3 of PoC to `const kParameterCountOffset = 0x3c;` to repro on CF or use the file attached in this comment.

### ol...@chromium.org (2026-02-26)

I guess the proposed CL <https://chromium-review.googlesource.com/c/v8/v8/+/7604772> could be that small back-mergable CL?

I can look into restricting CAST in CSA.

### cl...@appspot.gserviceaccount.com (2026-02-26)

Detailed Report: https://clusterfuzz.com/testcase?key=6619493673402368

Fuzzer: None
Job Type: linux_asan_d8_sandbox_testing
Platform Id: linux

Crash Type: V8 sandbox violation
Crash Address: 0x424242424242
Crash State:
  NULL
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8_sandbox_testing&revision=105482

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6619493673402368

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### dx...@google.com (2026-02-27)

Project: v8/v8  

Branch:  main  

Author:  Olivier Flückiger [olivf@chromium.org](mailto:olivf@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7614271>

[csa] Fix reading wasm function data from SFI

---


Expand for full commit details
```
     
    NO_IFTTT=Other site is ok 
     
    Fixed: 487213150 
    Change-Id: I0a274bee5b09babaf9352f62664ba268444a14c2 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7614271 
    Auto-Submit: Olivier Flückiger <olivf@chromium.org> 
    Reviewed-by: Igor Sheludko <ishell@chromium.org> 
    Commit-Queue: Igor Sheludko <ishell@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105493}

```

---

Files:

- M `src/codegen/code-stub-assembler.cc`

---

Hash: [dec3cffe63aa917a7276ff56da34742d3323d311](https://chromiumdash.appspot.com/commit/dec3cffe63aa917a7276ff56da34742d3323d311)  

Date: Fri Feb 27 07:25:03 2026


---

### sa...@google.com (2026-02-27)

Great work here everyone! \o/ Also thanks for already looking into hardening CSA casts for trusted objects, Oli! I think we should definitely do that! Thinking about this bug again though, would it even work here? The code is broken in such a strong way that it ends up treating in-sandbox memory as a trusted object (IIUC), and then a type-check also won't make a difference because the attacker then also controls the instance type. Is my thinking correct? I think this kind of bug is probably quite rare (as such code can never work correctly and would immediately crash if it ever ran), but maybe we could detect such flawed logic at build time by checking if the result of a regular compressed pointer load flows into a cast to a trusted object? Or does your change actually already work here because we cannot write such a CAST anymore now?

### ol...@chromium.org (2026-02-27)

@sa...@chromium.org I just uploaded an initial version in <https://chromium-review.googlesource.com/c/v8/v8/+/7616687> . With this change we run into a static assert in the `CAST` where you are casting to a TrustedObject.

### sa...@google.com (2026-02-27)

Awesome! \o/

### dx...@google.com (2026-02-27)

Project: v8/v8  

Branch:  main  

Author:  Krishna Ravishankar [krishna.ravi732@gmail.com](mailto:krishna.ravi732@gmail.com)  

Link:    <https://chromium-review.googlesource.com/7603043>

[debug] Get Code with SFI::GetCode for DebugBreakTrampoline

---


Expand for full commit details
```
     
    Bug: 487213150, 451355210 
    Change-Id: I15e95ad60d0f8d26aa4ca0fbfe4f1239b1cd664e 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7603043 
    Reviewed-by: Olivier Flückiger <olivf@chromium.org> 
    Commit-Queue: Igor Sheludko <ishell@chromium.org> 
    Reviewed-by: Igor Sheludko <ishell@chromium.org> 
    Auto-Submit: Krishna Ravishankar <krishna.ravi732@gmail.com> 
    Cr-Commit-Position: refs/heads/main@{#105500}

```

---

Files:

- M `src/builtins/builtins-internal-gen.cc`
- M `src/codegen/external-reference.cc`
- M `src/runtime/runtime-debug.cc`

---

Hash: [c9d92eac458cdb227d37f2c839e966dc73803694](https://chromiumdash.appspot.com/commit/c9d92eac458cdb227d37f2c839e966dc73803694)  

Date: Fri Feb 27 12:30:17 2026


---

### ch...@google.com (2026-03-13)

Merge review required: M146 is already shipping to stable.

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
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ol...@chromium.org (2026-03-13)

1. V8 sandbox escape
2. <https://chromium-review.googlesource.com/7614271>
3. y
4. n
5. n

### dr...@chromium.org (2026-03-15)

Approved for merge to M146

### dr...@chromium.org (2026-03-18)

Friendly ping on the merge to M146!

### ch...@google.com (2026-03-19)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-03-19)

Project: v8/v8  

Branch:  refs/branch-heads/14.6  

Author:  Olivier Flückiger [olivf@chromium.org](mailto:olivf@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7679312>

Merged: [csa] Fix reading wasm function data from SFI

---


Expand for full commit details
```
     
    NO_IFTTT=Other site is ok 
     
    Fixed: 487213150 
    (cherry picked from commit dec3cffe63aa917a7276ff56da34742d3323d311) 
     
    Change-Id: I78de2ada515c180320167da1526b6509ddde0467 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7679312 
    Reviewed-by: Igor Sheludko <ishell@chromium.org> 
    Commit-Queue: Igor Sheludko <ishell@chromium.org> 
    Auto-Submit: Olivier Flückiger <olivf@chromium.org> 
    Commit-Queue: Olivier Flückiger <olivf@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.6@{#47} 
    Cr-Branched-From: e04c3a1a2543bdbee7beac8846c9cbe8f657636f-refs/heads/14.6.202@{#1} 
    Cr-Branched-From: 3b0b01e6594ec362369dc16f069012a81748c8ba-refs/heads/main@{#105132}

```

---

Files:

- M `src/codegen/code-stub-assembler.cc`

---

Hash: [5189528888b15364846ecae5ef39aa8b6355a14b](https://chromiumdash.appspot.com/commit/5189528888b15364846ecae5ef39aa8b6355a14b)  

Date: Fri Feb 27 07:25:03 2026


---

### pe...@google.com (2026-03-19)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### qk...@google.com (2026-03-23)

Labeled `LTS-NotApplicable-138` because merging the patch to M138 required to change other codes a lot.

### pe...@google.com (2026-03-27)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-03-27)

1. <https://chromium-review.git.corp.google.com/c/v8/v8/+/7691549>
2. Low - There was no conflict.
3. 146
4. Yes, M144 has the problem code[1] as well.

[1] [CSA:GetSharedFunctionInfoCode loads the wrapper\_code field and casts it to Code](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/codegen/code-stub-assembler.cc;l=18582-18584;drc=5e5e2747d663a648f3ccca0ac91cd794763d7f40)

### an...@google.com (2026-03-30)

Merge approved for LTS-144

### dx...@google.com (2026-04-01)

Project: v8/v8  

Branch:  main  

Author:  Olivier Flückiger [olivf@chromium.org](mailto:olivf@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7616687>

[csa] Don't allow casting to trusted objects by default

---


Expand for full commit details
```
     
    Ensure casting to TrustedObjects is a conscious choice. 
     
    * Avoid casting by giving precise return types to safe operations 
    * Disallow magic casts to TrustedObjects 
    * Require a justification for using the new TrustedCast 
     
    NO_IFTTT=No functional change 
     
    Bug: 487213150 
    Change-Id: If03f65561525054519a092b5eadff69e235437ba 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7616687 
    Commit-Queue: Olivier Flückiger <olivf@chromium.org> 
    Reviewed-by: Igor Sheludko <ishell@chromium.org> 
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
    Auto-Submit: Olivier Flückiger <olivf@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106203}

```

---

Files:

- M `src/builtins/builtins-constructor-gen.cc`
- M `src/builtins/builtins-internal-gen.cc`
- M `src/builtins/builtins-regexp-gen.cc`
- M `src/builtins/builtins-regexp-gen.h`
- M `src/builtins/builtins-wasm-gen.cc`
- M `src/builtins/regexp-match.tq`
- M `src/builtins/regexp-replace.tq`
- M `src/codegen/code-stub-assembler-inl.h`
- M `src/codegen/code-stub-assembler.cc`
- M `src/codegen/code-stub-assembler.h`
- M `src/compiler/code-assembler.h`
- M `src/ic/accessor-assembler.cc`
- M `src/interpreter/interpreter-assembler.cc`
- M `src/objects/js-regexp.tq`

---

Hash: [e9fe611b34f8634d87bc9bfa87f6b8d2d964d7a8](https://chromiumdash.appspot.com/commit/e9fe611b34f8634d87bc9bfa87f6b8d2d964d7a8)  

Date: Wed Apr 1 09:21:23 2026


---

### dx...@google.com (2026-04-09)

Project: v8/v8  

Branch:  refs/branch-heads/14.4  

Author:  Olivier Flückiger [olivf@chromium.org](mailto:olivf@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7691549>

[M144-LTS][csa] Fix reading wasm function data from SFI

---


Expand for full commit details
```
     
    NO_IFTTT=Other site is ok 
     
    (cherry picked from commit dec3cffe63aa917a7276ff56da34742d3323d311) 
     
    Fixed: 487213150 
    Change-Id: I0a274bee5b09babaf9352f62664ba268444a14c2 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7614271 
    Auto-Submit: Olivier Flückiger <olivf@chromium.org> 
    Reviewed-by: Igor Sheludko <ishell@chromium.org> 
    Commit-Queue: Igor Sheludko <ishell@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#105493} 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7691549 
    Reviewed-by: Olivier Flückiger <olivf@chromium.org> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Cr-Commit-Position: refs/branch-heads/14.4@{#66} 
    Cr-Branched-From: 80acc26727d5a34e77dabeebe7c9213ec1bd4768-refs/heads/14.4.258@{#1} 
    Cr-Branched-From: ce7e597e90f6df3fa4b6df224bc613b80c635450-refs/heads/main@{#104020}

```

---

Files:

- M `src/codegen/code-stub-assembler.cc`

---

Hash: [fd73d6e5660b38d65cc53d889c1ebdbb9d89c241](https://chromiumdash.appspot.com/commit/fd73d6e5660b38d65cc53d889c1ebdbb9d89c241)  

Date: Fri Feb 27 07:25:03 2026


---

### ch...@google.com (2026-06-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
baseline. v8 sandbox bypass.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### kr...@gmail.com (2026-06-15)

Would someone be able to provide clarification on why this is $5000 and not $20000+? As far as I understand, under the old rules that were applicable when this report was submitted:

1. This should have qualified for $20k similar to [b/462217236](https://issues.chromium.org/issues/462217236), [b/444865195](https://issues.chromium.org/issues/444865195), [b/451355210](https://issues.chromium.org/issues/451355210) and so on.
2. + a patch bonus for [comment#14](https://issues.chromium.org/issues/487213150#comment14)?

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/487213150)*
