# SIGTRAP hit in JIT code (Builtins_InterpreterEntryTrampoline)

| Field | Value |
|-------|-------|
| **Issue ID** | [40050925](https://issues.chromium.org/issues/40050925) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Compiler |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ta...@gmail.com |
| **Assignee** | ne...@chromium.org |
| **Created** | 2019-12-08 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36

Steps to reproduce the problem:
The following PoC found by fuzzing crashes v8 8.0.0 with a trap.
Run with the debug build of d8.

function opt() {
  var arr = [0, 0, 0];
  var j = 11;
  for (let i = 0; i < 100; i++) {
    if (i == 90) {
      i = j.toPrecision().trimLeft();
      ++arr[i];
      arr[Math.atan(i)] = 1;
    }
  }
}

function main() {
  for (let i = 0; i < 100; i++) {
    opt();
  }
}

main();

What is the expected behavior?

What went wrong?
Run in gdb, we can get:

Thread 1 "d8" received signal SIGTRAP, Trace/breakpoint trap.
0x00007e8a14e42dba in ?? ()

(gdb) x/4i $pc-0x7
   0x7e8a14e42db3:      jne    0x7e8a14e42f75
   0x7e8a14e42db9:      int3
=> 0x7e8a14e42dba:      xor    %r11d,%r11d
   0x7e8a14e42dbd:      push   %r11

From our study, we think this should be different issue from 1028862.

Did this work before? N/A 

Chrome version: 78.0.3904.108  Channel: stable
OS Version: 
Flash Version: 

Found by Soyeon Park and Wen Xu from SSLab, Gatech

## Timeline

### cl...@chromium.org (2019-12-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5979084169281536.

### cl...@chromium.org (2019-12-09)

Testcase 5979084169281536 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5979084169281536.

### me...@chromium.org (2019-12-09)

I was able to repro this locally.
Labelling this high since it seems like it could lead to renderer code execution.
Assigning to v8 sheriff. mstarzinger@ could you please take a look or find an appropriate owner?

[Monorail components: Blink>JavaScript]

### me...@chromium.org (2019-12-09)

[Empty comment from Monorail migration]

### ms...@chromium.org (2019-12-10)

Reproduces with a regular local x64.debug build. I am not sure why CF has a hard time reproducing, I hope it isn't getting confused by the SIGTRAP again, because that would be a bummer. I ran a local bisect and ended up with the following first bad commit. Georg, since Sathya is OOO and the int3 in question happens in optimized code, could you help find the appropriate owner for this?

commit a1a45f4caa5bd47948347eaf4b736b400dfbae55
Author: Sathya Gunasekaran <gsathya@chromium.org>
Date:   Wed Oct 16 14:06:24 2019 +0100

    [ic] KeyedLoadIC: Optimize string keys as ArrayIndex
    
    Updates CSA::TryToIntptr to handle array indices that are less than
    INT_MAX which allows to handle string keys in the ICs.
    
    Updates ICs to go monomorphic for string keys that are array indices.
    
    Updates Turbofan to handle array indices when lowering element access.
    
    Change-Id: Ibdde20130e075d0d645ab4a8266a968335eaad84
    Bug: v8:9449
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1813018
    Reviewed-by: Tobias Tebbi <tebbi@chromium.org>
    Reviewed-by: Toon Verwaest <verwaest@chromium.org>
    Reviewed-by: Georg Neis <neis@chromium.org>
    Commit-Queue: Sathya Gunasekaran  <gsathya@chromium.org>
    Cr-Commit-Position: refs/heads/master@{#64320}


[Monorail components: Blink>JavaScript>Compiler]

### mm...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-23)

neis: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### te...@chromium.org (2019-12-23)

[Comment Deleted]

### te...@chromium.org (2019-12-23)

I investigated the issue: The root cause is a wrong reduction in RedundancyElimination::ReduceSpeculativeNumberOperation where we remove a SpeculativeToNumber node while widening the type. This can lead to issues because by removing it we no longer deopt, making the type information unreliable.
It is possible that this is exploitable.
The bug has been around for more than a year already.
I'm going on holiday now so I don't have time to land a fix anymore. The fix would looks like this, I don't want to upload it unnecessarily early without being able to land and backmerge in time.

--- a/src/compiler/redundancy-elimination.cc
+++ b/src/compiler/redundancy-elimination.cc
@@ -385,7 +385,8 @@ Reduction RedundancyElimination::ReduceSpeculativeNumberOperation(Node* node) {
     // than the type of the {first} node, otherwise we
     // would end up replacing NumberConstant inputs with
     // CheckBounds operations, which is kind of pointless.
-    if (!NodeProperties::GetType(first).Is(NodeProperties::GetType(check))) {
+    if (!NodeProperties::GetType(first).Is(NodeProperties::GetType(check)) &&
+        NodeProperties::GetType(check).Is(NodeProperties::GetType(first))) {
       NodeProperties::ReplaceValueInput(node, check, 0);
     }
   }

### sh...@chromium.org (2020-01-06)

neis: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/3f7e99ac460c3ca689aac76c39fbdf1852c9a7be

commit 3f7e99ac460c3ca689aac76c39fbdf1852c9a7be
Author: Tobias Tebbi <tebbi@chromium.org>
Date: Tue Jan 07 12:38:05 2020

[turbofan] fix type widening bug in RedundancyElimination

Bug: chromium:1031909
Change-Id: Ibf120d722a8cb6eb9b9eaa15163cb7846dab64ea
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1981507
Reviewed-by: Michael Stanton <mvstanton@chromium.org>
Commit-Queue: Tobias Tebbi <tebbi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#65599}

[modify] https://crrev.com/3f7e99ac460c3ca689aac76c39fbdf1852c9a7be/src/compiler/redundancy-elimination.cc


### cl...@chromium.org (2020-01-10)

[Empty comment from Monorail migration]

### ad...@google.com (2020-01-10)

tebbi@ if this is fixed, please mark as such. Sheriffbot will want this backported to M80 and (in due course) M79. If you think it's not exploitable or is too risky to merge, please comment thusly.

### ne...@chromium.org (2020-01-13)

Thanks Tobias!

### te...@chromium.org (2020-01-13)

It is very safe to back-merge. It might be exploitable, hard to say. In principle such typing bugs can lead to exploits and have lead to exploits historically. As neis@ just told me, my fix is incomplete though. I'll write a more complete CL and we can back-merge both.

### sh...@chromium.org (2020-01-13)

This bug requires manual review: M80's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), Kariahda@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/69b195c935b28857ee8e85c22af14837a0ce2c62

commit 69b195c935b28857ee8e85c22af14837a0ce2c62
Author: Tobias Tebbi <tebbi@chromium.org>
Date: Mon Jan 13 12:18:45 2020

[turbofan] fix type widening bug in RedundancyElimination, completely

This is an improved version of
https://chromium-review.googlesource.com/c/v8/v8/+/1981507

Bug: chromium:1031909
Change-Id: I552f49bf87340eee3c85fa02893b8e63a77a3608
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1997129
Reviewed-by: Georg Neis <neis@chromium.org>
Commit-Queue: Tobias Tebbi <tebbi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#65722}

[modify] https://crrev.com/69b195c935b28857ee8e85c22af14837a0ce2c62/src/compiler/redundancy-elimination.cc


### te...@chromium.org (2020-01-13)

1. Yes
2. https://chromium-review.googlesource.com/c/v8/v8/+/1981507
    https://chromium-review.googlesource.com/c/v8/v8/+/1997129/
3. the first CL yes, the second CL not yet.
4. It's a security issue that's potentially exploitable and has been in the code for a long time.
5. no

### sh...@chromium.org (2020-01-13)

[Empty comment from Monorail migration]

### sr...@google.com (2020-01-13)

neis@ pls confirm here when the second CL is also ready to back port. I will approve both the CL's at the same time

### ne...@chromium.org (2020-01-14)

It's ready (looking good in 81.0.4027.0).

### sr...@google.com (2020-01-14)

merge approved fro M80, branch:3987 pls complete your merge to branch asap.

### na...@google.com (2020-01-14)

[Empty comment from Monorail migration]

### go...@chromium.org (2020-01-14)

Please merge your change to M80 branch 3987 ASAP so we can pick it up for tomorrow's beta release, we're cutting Beta RC soon. Thank you.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/9276af78f87a4e7160d67afca01239070f47e5a6

commit 9276af78f87a4e7160d67afca01239070f47e5a6
Author: Georg Neis <neis@chromium.org>
Date: Wed Jan 15 10:43:58 2020

Merged: Squashed multiple commits.

Merged: [turbofan] fix type widening bug in RedundancyElimination
Revision: 3f7e99ac460c3ca689aac76c39fbdf1852c9a7be

Merged: [turbofan] fix type widening bug in RedundancyElimination, completely
Revision: 69b195c935b28857ee8e85c22af14837a0ce2c62

BUG=chromium:1031909
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=tebbi@chromium.org

Change-Id: I938a5ad9c1b9f7bd345311f44d815f5e49dc08df
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2002388
Reviewed-by: Tobias Tebbi <tebbi@chromium.org>
Commit-Queue: Georg Neis <neis@chromium.org>
Cr-Commit-Position: refs/branch-heads/8.0@{#22}
Cr-Branched-From: 69827db645fcece065bf16a795a4ec8d3a51057f-refs/heads/8.0.426@{#2}
Cr-Branched-From: 2fe1552c5809d0dd92e81d36a5535cbb7c518800-refs/heads/master@{#65318}

[modify] https://crrev.com/9276af78f87a4e7160d67afca01239070f47e5a6/src/compiler/redundancy-elimination.cc


### ne...@chromium.org (2020-01-15)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-01-23)

Congrats the Panel decided to reward $2,000 for this report!

### na...@google.com (2020-01-23)

[Empty comment from Monorail migration]

### ad...@google.com (2020-02-02)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-03)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-10)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-04-21)

This issue was migrated from crbug.com/chromium/1031909?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript, Blink>JavaScript>Compiler]
[Monorail mergedwith: crbug.com/chromium/1039111]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-07)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/chrome-blintz-user-guide

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050925)*
