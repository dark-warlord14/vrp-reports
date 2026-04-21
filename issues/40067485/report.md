# Security: Debug check failed: !s.InSharedHeap().

| Field | Value |
|-------|-------|
| **Issue ID** | [40067485](https://issues.chromium.org/issues/40067485) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turbofan |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | wh...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2023-07-15 |
| **Bounty** | $7,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

use fuzzbuild-d8 will get

# 

# Fatal error in ../../src/objects/string-inl.h, line 672

# Debug check failed: !s.InSharedHeap().

# 

#7 0x000055d073997945 in v8::base::(anonymous namespace)::DefaultDcheckHandler(char const\*, int, char const\*) () at ../../src/base/logging.cc:57  

#8 0x000055d0739e5f33 in Flatten () at ../../src/objects/string-inl.h:672  

#9 0x000055d074d93c74 in SlowEquals () at ../../src/objects/string.cc:1170  

#10 0x000055d073eede40 in Equals () at ../../src/objects/string-inl.h:503  

#11 0x000055d0751cf494 in \_\_RT\_impl\_Runtime\_StringEqual () at ../../src/runtime/runtime-strings.cc:428  

#12 0x000055d0751ceec8 in Runtime\_StringEqual () at ../../src/runtime/runtime-strings.cc:423

use d8-linux-debug-v8-component-88899 will get  

Received signal 11 SEGV\_ACCERR 08ed00280004

**VERSION**  

**Chrome Version: [x.x.x.x] + [stable, beta, or dev]**  

**Operating System: [Please indicate OS, version, and service pack level]**

**REPRODUCTION CASE**  

--expose-gc --omit-quit --allow-natives-syntax --fuzzing --jit-fuzzing --turboshaft --harmony

PoC  

let v1 = -1494007688;  

function f3() {  

const v4 = (a5) => {  

return (this.name + "-name-") + a5;  

};  

return v4;  

}  

const o11 = {  

"name": "obj",  

"method": f3,  

};  

for (let i13 = 0; i13 < 10000; v1++) {  

const v21 = "test" + i13.toString();  

const t13 = o11.method(i13, "obj");  

if (t13(v21) !== ("obj-name-test" + i13.toString())) {  

BigUint64Array + ". Expected '";  

}  

}

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

**Reporter credit: [goes here]**

## Timeline

### [Deleted User] (2023-07-15)

[Empty comment from Monorail migration]

### wh...@gmail.com (2023-07-15)

bisect 

[turboshaft] Implement low-level Load Elimination


➜  d8-linux-debug-v8-component-88875 ./d8 --turboshaft poc.js
Received signal 11 SEGV_ACCERR 15b700280010

==== C stack trace ===============================

 [0x7fe410d4c5e3]
 [0x7fe410d4c532]
 [0x7fe40c042520]
 [0x7fe40df181ed]
[end of stack trace]

### cl...@chromium.org (2023-07-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6608678553321472.

### bo...@chromium.org (2023-07-16)

Hello again Carl, ClusterFuzz was also able to reproduce this report so I'm setting a provisional values for Severity and FoundIn and routing to you as the current V8 sheriff.

[Monorail components: Blink>JavaScript>Compiler>Turbofan]

### [Deleted User] (2023-07-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-07-16)

ClusterFuzz testcase 6608678553321472 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2023-07-16)

Detailed Report: https://clusterfuzz.com/testcase?key=6608678553321472

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: UNKNOWN WRITE
Crash Address: 0x7e9600280014
Crash State:
  Builtins_StringAdd_CheckNone
  Builtins_JSEntryTrampoline
  Builtins_JSEntry
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&revision=88947

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6608678553321472

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

### [Deleted User] (2023-07-16)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2023-07-17)

Detailed Report: https://clusterfuzz.com/testcase?key=6608678553321472

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: UNKNOWN WRITE
Crash Address: 0x7ead00280010
Crash State:
  Builtins_StringAdd_CheckNone
  Builtins_JSEntryTrampoline
  Builtins_JSEntry
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=80135:80136

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6608678553321472

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cf...@google.com (2023-07-17)

@tebbi, could you PTAL? This bisects to: crrev.com/e4cc6ed44b61d4431d3efcda3a1a298c1155719d.

### dm...@chromium.org (2023-07-17)

I bisected locally to https://crrev.com/c/4597457 (like https://crbug.com/chromium/1465130#c2 said). I'll look into it.

### gi...@appspot.gserviceaccount.com (2023-07-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/6a380857a405df0934d3e7db82529f2db397670d

commit 6a380857a405df0934d3e7db82529f2db397670d
Author: Darius M <dmercadier@chromium.org>
Date: Mon Jul 17 13:46:09 2023

[turboshaft] Fix wrong Effect on StringEqual builtin

Bug: v8:12783
Change-Id: I54097e0f7893433a87788f39e93cf87ed9141d26
Fixed: chromium:1465130
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4689683
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Auto-Submit: Darius Mercadier <dmercadier@chromium.org>
Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
Cr-Commit-Position: refs/heads/main@{#88964}

[modify] https://crrev.com/6a380857a405df0934d3e7db82529f2db397670d/src/compiler/turboshaft/builtin-call-descriptors.h


### [Deleted User] (2023-07-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-07-18)

ClusterFuzz testcase 6608678553321472 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=88963:88964

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### am...@google.com (2023-07-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-27)

Congratulations Ganjiang Zhou! The VRP Panel has decided to aware you $7,000 for this report. Thank you for your efforts and reporting this issue to us! N

### wh...@gmail.com (2023-07-28)

[Comment Deleted]

### am...@chromium.org (2023-07-28)

Hello, given that the an actual commit hash was actually provided by you nor was any information that help signify that commit title was verified to have introduced this issue, and we still have to actually perform a bisect to triage this issue in https://crbug.com/chromium/1465130#c11, we are unfortunately unable to extend a bisect bonus here. 
In the future, please be sure to provide at least the commit hash or gerrit CL link if you have done the work to perform a bisection. Thank you. 

### am...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1465130?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067485)*
