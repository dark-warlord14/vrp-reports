# [TF::OptimizationBug] After optimization, running the "poc.js" yields segmentation fault

| Field | Value |
|-------|-------|
| **Issue ID** | [40062684](https://issues.chromium.org/issues/40062684) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>API, Blink>JavaScript>Compiler, Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | kw...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2023-01-16 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

Run the below 'poc.js' on the release build of v8-11.1.193:

```
function opt() {  
    function aux(a, b, c) {  
        if (a == 4) {  
            c += b;  
        }  
        b << c;  
    }  
    for (let i = 0; i < 10; i++) {  
        aux(i, aux, i);  
    }  
    eval(["".concat()].join());  
}  
  
for (let i = 0; i < 1e4; i++) {  
    opt();  
}  

```

**Problem Description:**  

It yields the segmentation fault:

Received signal 11 SEGV\_MAPERR 0000000ddd80

==== C stack trace ===============================

[0x560bc2b60647]  

[0x7fa409027420]  

[0x560b5ff2cc20]  

[end of stack trace]

**Additional Comments:**

\*\*Chrome version: \*\* \*\*Channel: \*\* Not sure

**OS:** Linux

## Timeline

### [Deleted User] (2023-01-16)

[Empty comment from Monorail migration]

### kw...@gmail.com (2023-01-16)

Here is the more minized version of poc:

function opt(i) {
    function aux(a, b, c) {
        if (a) {
            c += b;
        }
        b << c;
    }
    for (let i = 0; i < 2; i++) {
        aux(i, aux, i);
    }
    eval();
}

for (let i = 0; i < 1e4; i++) {
    opt();
}

### bo...@google.com (2023-01-17)

Thanks for the report! Confirming on Linux d8 at ToT (111.0.5545.0) this morning. 

This looks like an optimization issue given the need to make the opt() function hot, but there's not enough information for me to tell whether this is a compiler or interpreter issue. Redirecting to v8 folks for further triage. 

I get a SEGV rather than an ASan report, which is curious, but setting Severity-High on the basis of memory corruption in the sandboxed renderer process. I'm also setting all platforms because this seems likely to be core v8 behavior. 

[Monorail components: Blink>JavaScript>Compiler]

### bo...@google.com (2023-01-17)

Oops, forgot to set FoundIn

### [Deleted User] (2023-01-17)

[Empty comment from Monorail migration]

### jg...@chromium.org (2023-01-18)

The segv is in the ShiftLeft builtin:

0x7faebfb6406b   8ab  498b85a81b0000       REX.W movq rax,[r13+0x1ba8] (external reference (check_object_type))
0x7faebfb64072   8b2  40f6c40f             testb rsp,0xf
0x7faebfb64076   8b6  7401                 jz 0x7faebfb64079  (ShiftLeft)
0x7faebfb64078   8b8  cc                   int3l
0x7faebfb64079   8b9  4c8d1500000000       REX.W leaq r10,[rip+0x0]
0x7faebfb64080   8c0  4d8995e0000000       REX.W movq [r13+0xe0] (external value (IsolateData::fast_c_call_caller_pc_address)),r10
0x7faebfb64087   8c7  4989add8000000       REX.W movq [r13+0xd8] (external value (IsolateData::fast_c_call_caller_fp_address)),rbp
0x7faebfb6408e   8ce  ffd0                 call rax
0x7faebfb64090   8d0  49c785d800000000000000 REX.W movq [r13+0xd8] (external value (IsolateData::fast_c_call_caller_fp_address)),0x0
0x7faebfb6409b   8db  488b2424             REX.W movq rsp,[rsp]
0x7faebfb6409f   8df  488b5de0             REX.W movq rbx,[rbp-0x20]
0x7faebfb640a3   8e3  8b7bff               movl rdi,[rbx-0x1] <- 
0x7faebfb640a6   8e6  4903fe               REX.W addq rdi,r14
0x7faebfb640a9   8e9  4989e2               REX.W movq r10,rsp
0x7faebfb640ac   8ec  4883ec08             REX.W subq rsp,0x8

(gdb) p/x $rbx
$2 = 0x13c721

### cl...@chromium.org (2023-01-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5177200834969600.

### te...@chromium.org (2023-01-18)

Assigning to Thibaud based on the Clusterfuzz regression range.

### cl...@chromium.org (2023-01-18)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>API Blink>JavaScript>Runtime]

### cl...@chromium.org (2023-01-18)

Detailed Report: https://clusterfuzz.com/testcase?key=5177200834969600

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x0000001263d4
Crash State:
  Builtins_BitwiseNot
  Builtins_StringSubstring
  Builtins_ConstructProxy
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=84365:84366

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5177200834969600

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


The recommended severity (Security_Severity-Medium) is different from what was assigned to the bug. Please double check the accuracy of the assigned severity.

### th...@chromium.org (2023-01-18)

There is some representation mix-up. We emit a gap move to meet a fixed input register constraint:
[rbx|R|t] = v52

And v52 is marked as tagged and is spilled, so after the CommitAssignment phase it becomes:
[rbx|R|t] = [stack:8|t]

But after the MoveOptimizer phase it becomes:
[rbx|R|t] = [rax|R|w32]

Which looks off. The gap resolver would previously emit a 'movq' for this move, but after my change it emits a 'movl' based on the source representation.

I will change the gap resolver so that it chooses the move width based on the destination representation again. But I will also look into the move optimizer, because it would be better to avoid such type inconsistencies in the first place

### [Deleted User] (2023-01-18)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2023-01-18)

Small clarification: v52 happens to still be stored in rax at this point even though it is marked as spilled, so the optimization makes sense. It's only the representation that doesn't match.

### [Deleted User] (2023-01-18)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-18)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2023-01-19)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-01-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/0bfae5d1657d078b3596856536a1803944474af4

commit 0bfae5d1657d078b3596856536a1803944474af4
Author: Thibaud Michaud <thibaudm@chromium.org>
Date: Thu Jan 19 13:45:16 2023

[gap-resolver] Emit move based on destination representation

If the phi moves are the same for all predecessors, the move optimizer
will merge them by picking an arbitrary move among them,
moving it to the phi's block, and eliminating the moves in the
predecessor blocks.
However, phi inputs may have different width, and this can result in a
mismatch between the source and destination representation.
Always emit gap moves based on the destination operand's
representation, to ensure that in this case the wider phi inputs are not
truncated.

R=tebbi@chromium.org
CC=dmercadier@chromium.org

Bug: chromium:1407571
Change-Id: I0263cd5024e8e1340fb971267b133a2a91090f8f
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4178824
Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
Reviewed-by: Tobias Tebbi <tebbi@chromium.org>
Cr-Commit-Position: refs/heads/main@{#85403}

[modify] https://crrev.com/0bfae5d1657d078b3596856536a1803944474af4/src/compiler/backend/ia32/code-generator-ia32.cc
[modify] https://crrev.com/0bfae5d1657d078b3596856536a1803944474af4/test/cctest/compiler/test-gap-resolver.cc
[modify] https://crrev.com/0bfae5d1657d078b3596856536a1803944474af4/src/compiler/backend/x64/code-generator-x64.cc
[modify] https://crrev.com/0bfae5d1657d078b3596856536a1803944474af4/src/compiler/backend/ppc/code-generator-ppc.cc
[modify] https://crrev.com/0bfae5d1657d078b3596856536a1803944474af4/src/compiler/backend/code-generator.h
[modify] https://crrev.com/0bfae5d1657d078b3596856536a1803944474af4/src/compiler/backend/arm/code-generator-arm.cc
[modify] https://crrev.com/0bfae5d1657d078b3596856536a1803944474af4/src/compiler/backend/mips64/code-generator-mips64.cc
[modify] https://crrev.com/0bfae5d1657d078b3596856536a1803944474af4/src/compiler/backend/arm64/code-generator-arm64.cc
[modify] https://crrev.com/0bfae5d1657d078b3596856536a1803944474af4/src/compiler/backend/riscv/code-generator-riscv.cc
[modify] https://crrev.com/0bfae5d1657d078b3596856536a1803944474af4/src/compiler/backend/s390/code-generator-s390.cc
[modify] https://crrev.com/0bfae5d1657d078b3596856536a1803944474af4/src/compiler/backend/gap-resolver.cc
[modify] https://crrev.com/0bfae5d1657d078b3596856536a1803944474af4/src/compiler/backend/gap-resolver.h
[modify] https://crrev.com/0bfae5d1657d078b3596856536a1803944474af4/src/compiler/backend/loong64/code-generator-loong64.cc


### th...@chromium.org (2023-01-19)

https://crbug.com/chromium/1407571#c17 should be backmerged to 110.

### cl...@chromium.org (2023-01-19)

ClusterFuzz testcase 5177200834969600 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=85402:85403

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-01-19)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-01-19)

Since this fix just landed today, leaving in the merge review queue for now to allow for more bake time on Canary. Will review on Monday to allow for enough merge time before next M110 beta release on Wednesday. 

### [Deleted User] (2023-01-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-20)

Merge review required: M110 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-01-24)

M110 merge approved, please merge this fix to relevant V8 branch for M110 (11.0-lkgr) at your earliest availability so this fix can be included in tomorrow's (Wednesday's) M110 beta / early stable -- thank you! 

### am...@google.com (2023-01-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-26)

Congratulations! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts in reporting this issue to us -- nice work! 

### kw...@gmail.com (2023-01-27)

Thank you!

### [Deleted User] (2023-01-27)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-01-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-01-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/e607d6d46f0509c11b69965ef1756be6a0a0b8c5

commit e607d6d46f0509c11b69965ef1756be6a0a0b8c5
Author: Thibaud Michaud <thibaudm@chromium.org>
Date: Mon Jan 30 11:59:45 2023

Merged: [gap-resolver] Emit move based on destination representation

If the phi moves are the same for all predecessors, the move optimizer
will merge them by picking an arbitrary move among them,
moving it to the phi's block, and eliminating the moves in the
predecessor blocks.
However, phi inputs may have different width, and this can result in a
mismatch between the source and destination representation.
Always emit gap moves based on the destination operand's
representation, to ensure that in this case the wider phi inputs are not
truncated.

R=​tebbi@chromium.org
CC=​dmercadier@chromium.org

Bug: chromium:1407571
(cherry picked from commit 0bfae5d1657d078b3596856536a1803944474af4)

Change-Id: Ic920731ef572f26ff3f1b04aa7bd642a122dafe9
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4197676
Reviewed-by: Tobias Tebbi <tebbi@chromium.org>
Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
Cr-Commit-Position: refs/branch-heads/11.0@{#25}
Cr-Branched-From: 06097c6f0c5af54fd5d6965d37027efb72decd4f-refs/heads/11.0.226@{#1}
Cr-Branched-From: 6bf3344f5d9940de1ab253f1817dcb99c641c9d3-refs/heads/main@{#84857}

[modify] https://crrev.com/e607d6d46f0509c11b69965ef1756be6a0a0b8c5/src/compiler/backend/ia32/code-generator-ia32.cc
[modify] https://crrev.com/e607d6d46f0509c11b69965ef1756be6a0a0b8c5/test/cctest/compiler/test-gap-resolver.cc
[modify] https://crrev.com/e607d6d46f0509c11b69965ef1756be6a0a0b8c5/src/compiler/backend/x64/code-generator-x64.cc
[modify] https://crrev.com/e607d6d46f0509c11b69965ef1756be6a0a0b8c5/src/compiler/backend/ppc/code-generator-ppc.cc
[modify] https://crrev.com/e607d6d46f0509c11b69965ef1756be6a0a0b8c5/src/compiler/backend/code-generator.h
[modify] https://crrev.com/e607d6d46f0509c11b69965ef1756be6a0a0b8c5/src/compiler/backend/mips64/code-generator-mips64.cc
[modify] https://crrev.com/e607d6d46f0509c11b69965ef1756be6a0a0b8c5/src/compiler/backend/arm/code-generator-arm.cc
[modify] https://crrev.com/e607d6d46f0509c11b69965ef1756be6a0a0b8c5/src/compiler/backend/arm64/code-generator-arm64.cc
[modify] https://crrev.com/e607d6d46f0509c11b69965ef1756be6a0a0b8c5/src/compiler/backend/riscv/code-generator-riscv.cc
[modify] https://crrev.com/e607d6d46f0509c11b69965ef1756be6a0a0b8c5/src/compiler/backend/s390/code-generator-s390.cc
[modify] https://crrev.com/e607d6d46f0509c11b69965ef1756be6a0a0b8c5/src/compiler/backend/gap-resolver.cc
[modify] https://crrev.com/e607d6d46f0509c11b69965ef1756be6a0a0b8c5/src/compiler/backend/gap-resolver.h
[modify] https://crrev.com/e607d6d46f0509c11b69965ef1756be6a0a0b8c5/src/compiler/backend/loong64/code-generator-loong64.cc


### [Deleted User] (2023-01-30)

LTS Milestone M108

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-30)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-01-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/87e2a8350307bd70848628b50d2da4c3c93827e8

commit 87e2a8350307bd70848628b50d2da4c3c93827e8
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Jan 30 18:23:55 2023

Roll v8 11.0 from 264676c3b788 to dc183b6f8195 (3 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/264676c3b788..dc183b6f8195

2023-01-30 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.0.226.13
2023-01-30 thibaudm@chromium.org Merged: [gap-resolver] Emit move based on destination representation
2023-01-30 clemensb@chromium.org Merged: [wasm] Fix printing of wasm-to-js frames

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-chromium-release-1
Please CC v8-waterfall-sheriff@grotations.appspotmail.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 11.0: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m110: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1402270,chromium:1407571
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: I09c6e366347c0a0bd350199ba259ffb784a2a4cf
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4204269
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5481@{#801}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/87e2a8350307bd70848628b50d2da4c3c93827e8/DEPS


### rz...@google.com (2023-02-01)

[Empty comment from Monorail migration]

### rz...@google.com (2023-02-01)

[Empty comment from Monorail migration]

### rz...@google.com (2023-02-01)

Commit that caused the regression isn't present in the 102 branch.

### rz...@google.com (2023-02-01)

Commit that caused the regression isn't present in the 108 branch

### [Deleted User] (2023-04-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1407571?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript>API, Blink>JavaScript>Compiler, Blink>JavaScript>Runtime]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062684)*
