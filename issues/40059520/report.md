# Security: Debug check failed: marking_state_->IsBlackOrGrey(heap_object).

| Field | Value |
|-------|-------|
| **Issue ID** | [40059520](https://issues.chromium.org/issues/40059520) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | p4...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2022-04-29 |
| **Bounty** | $7,500.00 |

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

The bug is a same case as <https://crbug.com/chromium/1102161(https://bugs.chromium.org/p/chromium/issues/detail?id=1102161)>.

When fixing <https://crbug.com/chromium/1213770>, it moved the `weak_cell.set_unregister_token(undefined);` action from `MarkCompactCollector::ClearJSWeakRefs` to `JSFinalizationRegistry::RemoveCellFromUnregisterTokenMap` at <https://chromium.googlesource.com/v8/v8/+/eb798db452422033ee312aaef5fcb09a02e09447>.

It means that only the WeakCell in `cleared_cells` will set unregister\_token as undefined. But if a WeakCell which was unregisted is in gc's worklist\_, it won't added into cleared\_cells. So the WeakCell still keeps a stale ref to the unregister\_token.

We can push a WeakCell into worklist\_ via `MarkingBarrier` because the PushCell in FinalizationRegistryRegister writes the `next` of a WeakCell.[1]

```
transitioning macro PushCell(  
    finalizationRegistry: JSFinalizationRegistry, cell: WeakCell): void {  
 [1] cell.next = finalizationRegistry.active_cells;  
  typeswitch (finalizationRegistry.active_cells) {  
    case (Undefined): {  
    }  
    case (oldHead: WeakCell): {  
      oldHead.prev = cell;  
    }  
  }  
  finalizationRegistry.active_cells = cell;  
}  

```

It may lead to the garbage collector getting confused, maybe a Use-After-free.

**VERSION**  

V8 version : f47452080c0c67d665297e3cebe7d8a66c24e13f  

Operating System: ubuntu 20.04

**REPRODUCTION CASE**

1. execute the attach file in d8 version with flag "--allow-natives-syntax --expose-gc --verify-heap ".  
   
   in Debug version, it will crash with detail below:  
   
   // %DebugPrint(token);  
   
   // #  
   
   // # Fatal error in ../../src/heap/mark-compact.cc, line 288  
   
   // # Check failed: marking\_state\_->IsBlackOrGrey(heap\_object).  
   
   // #  
   
   // #  
   
   // #  
   
   // #FailureMessage Object: 0x7fff875b1ba0%

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tab]

I wrote a patch based on my understanding of the bug, see patch.diff.

## Attachments

- [test.js](attachments/test.js) (text/plain, 580 B)
- [patch.diff](attachments/patch.diff) (text/plain, 503 B)

## Timeline

### [Deleted User] (2022-04-29)

[Empty comment from Monorail migration]

### do...@chromium.org (2022-04-30)

+syg from https://crbug.com/chromium/1102161 and https://crbug.com/chromium/1213770

### [Deleted User] (2022-04-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-02)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sy...@chromium.org (2022-05-02)

Thank you for the detailed reports as well as a possible fix. Great find with the barrier preventing the nulling out of the unregister_token field!

I'm not sure how to yet convert this into a UAF, because IIUC this can only happen for unregistered cells. That said, most exploit writers are probably cleverer than I am.

### sy...@chromium.org (2022-05-02)

[Empty comment from Monorail migration]

### sy...@chromium.org (2022-05-03)

saelo@, can you provide an assessment on whether this should be backported to all branches? AFAICT this is mainly an assertion in the heap verifier, and only happens for WeakCells which are no longer reachable from JS programs.

### gi...@appspot.gserviceaccount.com (2022-05-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/dd3289d7945dac855d1287cf4ea248883e908d54

commit dd3289d7945dac855d1287cf4ea248883e908d54
Author: Shu-yu Guo <syg@chromium.org>
Date: Tue May 03 20:26:32 2022

[weakrefs] Set unregister_token to undefined when unregistering

Bug: chromium:1321078
Change-Id: I426327ffc3d7eebdb562c01a87039a93dfb79a88
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3620836
Commit-Queue: Shu-yu Guo <syg@chromium.org>
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#80349}

[modify] https://crrev.com/dd3289d7945dac855d1287cf4ea248883e908d54/src/objects/js-weak-refs-inl.h
[modify] https://crrev.com/dd3289d7945dac855d1287cf4ea248883e908d54/src/heap/mark-compact.cc
[modify] https://crrev.com/dd3289d7945dac855d1287cf4ea248883e908d54/src/objects/js-weak-refs.h
[modify] https://crrev.com/dd3289d7945dac855d1287cf4ea248883e908d54/src/objects/objects.cc
[modify] https://crrev.com/dd3289d7945dac855d1287cf4ea248883e908d54/test/cctest/test-js-weak-refs.cc


### p4...@gmail.com (2022-05-09)

[Comment Deleted]

### p4...@gmail.com (2022-05-16)

Sorry, may I ask are there any next action of this issue since it fixed about two weeks.

### sy...@chromium.org (2022-05-16)

[Empty comment from Monorail migration]

### sa...@google.com (2022-05-17)

Hi! So from my understanding of this issue, the outcome is a dangling pointer of the "unregister token" field that isn't directly accessible from JS but may be used to compute a hash from [1] (please correct me if I'm misunderstanding the issue). It seems that computing a hash of a freed (and possibly reclaimed) object may cause memory corruption, for example via String::ComputeAndSetHash() [2]. While I'm not 100% certain that this can happen in this situation, I think we should error on the safe side and assume that this type of bug can cause memory corruption and so is exploitable. Raising the severity accordingly.

[1] https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/js-weak-refs-inl.h;l=84;drc=9bf53ab9128027a4a3df5cc10485e7962ddfad4d
[2] https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/string.cc;l=1481;drc=9bf53ab9128027a4a3df5cc10485e7962ddfad4d

### sy...@chromium.org (2022-05-18)

Thanks for the assessment, saelo@. Sounds like we should prepare backmerges for all branches, then.

### sy...@chromium.org (2022-05-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-18)

Merge review required: M101 is already shipping to stable.

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
Owners: benmason (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-18)

Merge review required: M102 has already been cut for stable release.

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

### sy...@chromium.org (2022-05-18)


Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

It is a high-severity security bug.

2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/v8/v8/+/3620836

3. Have the changes been released and tested on canary?

It's been merged to Canary for 2 weeks.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No. It's exposed by WeakRefs, which has been shipped since M84.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Don't think so.


### am...@chromium.org (2022-05-18)

Hi syg@ thank you for fixing this issue. I've updated it as fixed based on the CLs landed and merges requested. For future reference, once a security bug is resolved, please just update the issue as Fixed and the bot will add the appropriate merge labels. 
M102 stable cut was just completed with stable release scheduled for 24 May; there are no further planned releases of M101 stable, so I adjusting labels accordingly. 

### sy...@chromium.org (2022-05-19)

amyressler@ thank you for the pointers!

### am...@chromium.org (2022-05-19)

M102 merge approved, please merge to 10.2-lkgr at your earliest convenience so this fix can be included in the first security refresh for M102. Just to reiterate the above, please mark issues as fixed as soon as the resolving CLs are landed so these types of fixed security bugs right away. This ensures the fixed bugs get to the merge review queue and the fixes merged to the relevant release branches as soon as it is safe to do so. We push on this to help make the patch gap as narrow as possible and reduce the potential for n-day patch gap exploitation as much as we can. Thank you! 

### am...@chromium.org (2022-05-19)

thanks syg@! and apologies for the comments collision -- didn't mean to pile on with the comments :) 

### am...@chromium.org (2022-05-19)

I guess it helps if I update the labels :)) 

### [Deleted User] (2022-05-19)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=1321078&entry.364066060=External&entry.958145677=Android&entry.958145677=Chrome&entry.958145677=Linux&entry.958145677=Mac&entry.958145677=Windows&entry.958145677=Lacros&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>JavaScript&entry.975983575=syg@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-19)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-05-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/3ada103ce62952983a667852b3cee56955acec1d

commit 3ada103ce62952983a667852b3cee56955acec1d
Author: Shu-yu Guo <syg@chromium.org>
Date: Tue May 03 20:26:32 2022

Merged: [weakrefs] Set unregister_token to undefined when unregistering

Bug: chromium:1321078
Change-Id: I426327ffc3d7eebdb562c01a87039a93dfb79a88
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3620836
Commit-Queue: Shu-yu Guo <syg@chromium.org>
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#80349}
(cherry picked from commit dd3289d7945dac855d1287cf4ea248883e908d54)
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3654954
Auto-Submit: Shu-yu Guo <syg@chromium.org>
Reviewed-by: Adam Klein <adamk@chromium.org>
Commit-Queue: Michael Lippautz <mlippautz@chromium.org>

[modify] https://crrev.com/3ada103ce62952983a667852b3cee56955acec1d/src/objects/js-weak-refs-inl.h
[modify] https://crrev.com/3ada103ce62952983a667852b3cee56955acec1d/src/heap/mark-compact.cc
[modify] https://crrev.com/3ada103ce62952983a667852b3cee56955acec1d/src/objects/js-weak-refs.h
[modify] https://crrev.com/3ada103ce62952983a667852b3cee56955acec1d/src/objects/objects.cc
[modify] https://crrev.com/3ada103ce62952983a667852b3cee56955acec1d/test/cctest/test-js-weak-refs.cc


### ea...@google.com (2022-05-23)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-27)

Congratulations! The VRP Panel has decided to award you $7500 for this report. Thanks for your efforts in reporting this issue to us and great work! 

### [Deleted User] (2022-05-27)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-05-30)

[Empty comment from Monorail migration]

### rz...@google.com (2022-05-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-30)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-05-30)

1. Just https://crrev.com/c/3676863
2. Low, no conflicts
3. 102
4. Yes

Tests passing locally

### gm...@google.com (2022-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-31)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-05-31)

[Empty comment from Monorail migration]

### rz...@google.com (2022-06-01)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-06-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/f07854e77ea7c59cfb4305df8e529b6ef5520cf5

commit f07854e77ea7c59cfb4305df8e529b6ef5520cf5
Author: Shu-yu Guo <syg@chromium.org>
Date: Tue May 03 20:26:32 2022

[M96-LTS][weakrefs] Set unregister_token to undefined when unregistering

(cherry picked from commit dd3289d7945dac855d1287cf4ea248883e908d54)

Bug: chromium:1321078
No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Change-Id: I426327ffc3d7eebdb562c01a87039a93dfb79a88
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3620836
Commit-Queue: Shu-yu Guo <syg@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#80349}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3676863
Reviewed-by: Dominik Inführ <dinfuehr@chromium.org>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/9.6@{#68}
Cr-Branched-From: 0b7bda016178bf438f09b3c93da572ae3663a1f7-refs/heads/9.6.180@{#1}
Cr-Branched-From: 41a5a247d9430b953e38631e88d17790306f7a4c-refs/heads/main@{#77244}

[modify] https://crrev.com/f07854e77ea7c59cfb4305df8e529b6ef5520cf5/src/objects/js-weak-refs-inl.h
[modify] https://crrev.com/f07854e77ea7c59cfb4305df8e529b6ef5520cf5/src/heap/mark-compact.cc
[modify] https://crrev.com/f07854e77ea7c59cfb4305df8e529b6ef5520cf5/src/objects/js-weak-refs.h
[modify] https://crrev.com/f07854e77ea7c59cfb4305df8e529b6ef5520cf5/src/objects/objects.cc
[modify] https://crrev.com/f07854e77ea7c59cfb4305df8e529b6ef5520cf5/test/cctest/test-js-weak-refs.cc


### am...@chromium.org (2022-06-10)

https://chromium-review.googlesource.com/c/v8/v8/+/3695262 CPed for 10.2 merge -- Thank you, Michael! 

### gi...@appspot.gserviceaccount.com (2022-06-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/44c4e56fea2cd45b5478e5671c84d91a70f0b6f0

commit 44c4e56fea2cd45b5478e5671c84d91a70f0b6f0
Author: Shu-yu Guo <syg@chromium.org>
Date: Tue May 03 20:26:32 2022

Merged: [weakrefs] Set unregister_token to undefined when unregistering

(cherry picked from commit dd3289d7945dac855d1287cf4ea248883e908d54)

Bug: chromium:1321078
Change-Id: Ic7537cc5101b35018911c27a81e9b0e0a7da154b
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3695262
Reviewed-by: Dominik Inführ <dinfuehr@chromium.org>
Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
Cr-Commit-Position: refs/branch-heads/10.2@{#16}
Cr-Branched-From: 374091f382e88095694c1283cbdc2acddc1b1417-refs/heads/10.2.154@{#1}
Cr-Branched-From: f0c353f6315eeb2212ba52478983a3b3af07b5b1-refs/heads/main@{#79976}

[modify] https://crrev.com/44c4e56fea2cd45b5478e5671c84d91a70f0b6f0/src/objects/js-weak-refs-inl.h
[modify] https://crrev.com/44c4e56fea2cd45b5478e5671c84d91a70f0b6f0/src/heap/mark-compact.cc
[modify] https://crrev.com/44c4e56fea2cd45b5478e5671c84d91a70f0b6f0/src/objects/objects.cc
[modify] https://crrev.com/44c4e56fea2cd45b5478e5671c84d91a70f0b6f0/src/objects/js-weak-refs.h
[modify] https://crrev.com/44c4e56fea2cd45b5478e5671c84d91a70f0b6f0/test/cctest/test-js-weak-refs.cc


### am...@chromium.org (2022-06-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-06-21)

[Empty comment from Monorail migration]

### rz...@google.com (2022-07-15)

Already merged to 102

### am...@google.com (2022-07-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1321078?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059520)*
