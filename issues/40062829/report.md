# Security: Debug check failed: kCanBeWeak || (!IsSmi() == HAS_STRONG_HEAP_OBJECT_TAG(ptr_))

| Field | Value |
|-------|-------|
| **Issue ID** | [40062829](https://issues.chromium.org/issues/40062829) |
| **Status** | Fixed |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | wh...@gmail.com |
| **Assignee** | vi...@chromium.org |
| **Created** | 2023-01-30 |
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

v8 current HEAD

it's bug found by fuzzilli

PoC  

function main() {  

const v2 = new Uint8ClampedArray("1073741824");  

for (const v4 in "string") {  

for (const v6 in "function") {  

function v7(v8,v9,v10,v11) {  

for (const v13 in "8HZHE5Q6G1") {  

}  

const v14 = {};  

for (const v15 in "8HZHE5Q6G1") {  

for (let v16 = 0; v16 < 3818; v16++) {  

}  

}  

return v11;  

}  

const v17 = v7("string",v4,v4,v2);  

for (let v18 = 0; v18 < 3818; v18++) {  

}  

}  

}  

}  

main();

with fuzzer log file get  

// CRASH INFO  

// ==========  

// TERMSIG: 6  

// STDERR:  

// #  

// # Fatal error in ../../src/objects/tagged-impl.h, line 142  

// # Debug check failed: kCanBeWeak || (!IsSmi() == HAS\_STRONG\_HEAP\_OBJECT\_TAG(ptr\_)).  

// #  

// #  

// #

but can't repro that error info, I get a segv accerr

➜ crashes /home/uuu/v8\_src.main/v8/out/x64.debug/d8 --expose-gc --future --assert-types --maglev-assert --turboshaft-assert-types --harmony-rab-gsab --interrupt-budget=1000 --maglev-ool-prologue --turboshaft --fuzzer-gc-analysis --always-turbofan ./1.js  

Received signal 11 SEGV\_ACCERR 0208d5880008

==== C stack trace ===============================

[0x7f30f8de46be]  

[0x7f30f8de45fe]  

[0x7f30f889e420]  

[0x5616e96e6a7c]  

[0x7f30fbe5ddb5]  

[0x7f30fbe5dd88]  

[0x7f30fc4a82d8]  

[0x7f30fc642fb0]  

[0x7f30fc66c3e5]  

[0x7f30fc66c1af]  

[0x7f30fc69dc8d]  

[0x7f30fc69d461]  

[0x7f30fc3c5692]  

[0x7f30fc3c50bc]  

[0x7f30fc3e4094]  

[0x7f30fc3e4170]  

[0x7f30fc5d2ec4]  

[0x7f30fc5ce344]  

[0x7f30fc5d2f0a]  

[0x7f30fc659252]  

[0x7f30fc64a2a1]  

[0x7f30fc64498c]  

[0x7f30fc5c7c3b]  

[0x7f30fc5c4d4e]  

[0x7f30fc5c2131]  

[0x7f30fc5c0ef9]  

[0x7f30fc5c0e3d]  

[0x7f30fc44b930]  

[0x7f30fd0398f4]  

[0x7f30fd039438]  

[0x7f307f96d53f]  

[end of stack trace]  

[1] 315227 segmentation fault (core dumped) /home/uuu/v8\_src.main/v8/out/x64.debug/d8 --expose-gc --future --assert-types

## Timeline

### [Deleted User] (2023-01-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-01-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4743912806875136.

### rs...@chromium.org (2023-01-30)

This does not reproduce on v8 head at 24b1878832, but it did at fa303fcd0b.

What revision did you test this at?

### rs...@chromium.org (2023-01-30)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### rs...@chromium.org (2023-01-30)

https://crbug.com/chromium/1406727 looks almost identical, but the fix range does not align with c#3.

### wh...@gmail.com (2023-01-31)

Hi, at current HEAD 8131315998ad, I still can get SEGV_ACCERR.
using debug version 
./d8 --expose-gc --future  --assert-types --maglev-assert --turboshaft-assert-types --harmony-rab-gsab   --interrupt-budget=1000   --maglev-ool-prologue  --turboshaft  --fuzzer-gc-analysis   --always-turbofan  ./1.js

and wait some seconds

### [Deleted User] (2023-01-31)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2023-01-31)

Detailed Report: https://clusterfuzz.com/testcase?key=5941764656660480

Fuzzer: None
Job Type: mac_asan_d8_dbg
Platform Id: mac

Crash Type: Bus on unknown address
Crash Address: 
Crash State:
  v8::internal::VerifyPointersVisitor::VerifyHeapObjectImpl
  v8::internal::VerifyPointersVisitor::VisitRootPointers
  v8::internal::MaglevFrame::Iterate
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=mac_asan_d8_dbg&range=85330:85331

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5941764656660480

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2023-01-31)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/9bd7c5e1bdd01c5af7923b3d8387ddae461249cd ([maglev] Fix visiting stack in StackGuard call).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### sa...@chromium.org (2023-01-31)

Thanks for the report and for using Fuzzilli!

### gi...@appspot.gserviceaccount.com (2023-01-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/5d8afae6d409cb59df959e2138180ed7be545ee5

commit 5d8afae6d409cb59df959e2138180ed7be545ee5
Author: Victor Gomes <victorgomes@chromium.org>
Date: Tue Jan 31 16:01:23 2023

[maglev] Remove MaglevOutOfLinePrologue

The flag is currently poorly tested and we are unlikely to
use the OutOfLinePrologue in its current form.

Bug: v8:7700, chromium:1411153
Change-Id: Ifd5867910d79fbdeaebb4c21f7070f806d78052c
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4208932
Auto-Submit: Victor Gomes <victorgomes@chromium.org>
Commit-Queue: Leszek Swirski <leszeks@chromium.org>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Cr-Commit-Position: refs/heads/main@{#85568}

[modify] https://crrev.com/5d8afae6d409cb59df959e2138180ed7be545ee5/src/maglev/x64/maglev-assembler-x64.cc
[modify] https://crrev.com/5d8afae6d409cb59df959e2138180ed7be545ee5/src/flags/flag-definitions.h
[modify] https://crrev.com/5d8afae6d409cb59df959e2138180ed7be545ee5/src/execution/frames.cc
[modify] https://crrev.com/5d8afae6d409cb59df959e2138180ed7be545ee5/src/builtins/builtins-definitions.h
[modify] https://crrev.com/5d8afae6d409cb59df959e2138180ed7be545ee5/src/builtins/x64/builtins-x64.cc
[modify] https://crrev.com/5d8afae6d409cb59df959e2138180ed7be545ee5/src/maglev/arm64/maglev-assembler-arm64.cc
[modify] https://crrev.com/5d8afae6d409cb59df959e2138180ed7be545ee5/src/builtins/builtins-internal-gen.cc


### vi...@chromium.org (2023-02-01)

No security impact, since Maglev is disabled.

### [Deleted User] (2023-02-01)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vi...@chromium.org (2023-02-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-02-01)

ClusterFuzz testcase 5941764656660480 is verified as fixed in https://clusterfuzz.com/revisions?job=mac_asan_d8_dbg&range=85567:85568

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-01)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-17)

Congratulations! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@chromium.org (2023-02-17)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-05-10)

This issue was migrated from crbug.com/chromium/1411153?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062829)*
