# Security: OOB write after creating pinned tab that's also in a group

| Field | Value |
|-------|-------|
| **Issue ID** | [40055878](https://issues.chromium.org/issues/40055878) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>TopChrome>TabStrip>TabGroups |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | dp...@chromium.org |
| **Created** | 2021-05-15 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

A pinned tab typically can't be placed in a group. However, if a tab is created within the bounds of an existing group, the tab will be assigned to that group. This is true even if the tab is pinned.

An extension can then use this behavior to produce the same effect as described in <https://crbug.com/chromium/1198717>. Specifically, moving the group will also move the pinned tab, breaking the constraint that pinned tabs are always at the start of the tab strip. Then, attempting to move the pinned tab to a different index will result in an out-of-bounds write in the browser process.

**VERSION**  

Chrome Version: Tested on 92.0.4509.0 (latest asan build)  

Operating System: Windows 10, version 20H2

**REPRODUCTION CASE**

1. Install the attached extension.
2. Once installed, the extension will create a window with three tabs: two that are in a group and one that's not.
3. The extension will then create a new pinned tab using the following call:

chrome.tabs.create({windowId: newWindow.id, index: 1, pinned: true, url: "about:blank"});

Because the specified index is in the middle of the existing group, the tab will be added to that group, even though the tab is pinned.

4. The extension will then call chrome.tabGroups.move to move the group to the end of the tab strip. This will also move the pinned tab, meaning that there's now a pinned tab that's not at the start of the tab strip.
5. Finally, the extension will use chrome.tabs.move to move the pinned tab to index 0. This will result in an OOB write in the browser process.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [asan_output_883253.txt](attachments/asan_output_883253.txt) (text/plain, 12.0 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 196 B)
- [service_worker.js](attachments/service_worker.js) (text/plain, 1.0 KB)

## Timeline

### de...@gmail.com (2021-05-15)

The core issue here is that the code that checks whether a new tab should be added to an existing group doesn't check whether the tab is pinned:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/tabs/tab_strip_model.cc;l=1003;drc=511d2e61f78efa707c00efe3fbdd712b98fc0ebe

### [Deleted User] (2021-05-15)

[Empty comment from Monorail migration]

### xi...@chromium.org (2021-05-17)

Thanks for the report! Triaging the same way as https://crbug.com/1198717.

[Monorail components: UI>Browser>TabStrip]

### xi...@chromium.org (2021-05-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-17)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-29)

solomonkinard: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-06-12)

solomonkinard: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### so...@chromium.org (2021-06-29)

In me queue, but will ask for someone else to look.

### so...@chromium.org (2021-06-29)

[Empty comment from Monorail migration]

### so...@chromium.org (2021-06-29)

Connily mentioned that the tabs team may be able to start to consider this and related p1 bugs tomorrow, as some of the changes may be beyond the scope of the extensions API.

### so...@chromium.org (2021-06-29)

Thanks again Connily. Adding as owner so we don't lose track of them.

### rs...@chromium.org (2021-07-07)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>TopChrome>TabStrip>TabGroups]

### dp...@chromium.org (2021-07-09)

Taking a look at this tommorrow

### gi...@appspot.gserviceaccount.com (2021-07-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e06d6c59ec36066fa8ff9b9874b63c7e189fc1da

commit e06d6c59ec36066fa8ff9b9874b63c7e189fc1da
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Tue Jul 13 04:05:10 2021

Fix case where an extension could open a pinned grouped tab.

Bug: 1209469
Change-Id: Ib3dea05cbc1f8b29450a336a3089e0e2a6a8e9cf
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3018421
Commit-Queue: Peter Boström <pbos@chromium.org>
Auto-Submit: Taylor Bergquist <tbergquist@chromium.org>
Reviewed-by: Peter Boström <pbos@chromium.org>
Cr-Commit-Position: refs/heads/master@{#900825}

[modify] https://crrev.com/e06d6c59ec36066fa8ff9b9874b63c7e189fc1da/chrome/browser/ui/tabs/tab_strip_model.cc


### ad...@google.com (2021-07-14)

Thanks Taylor! Could you mark this as Fixed if you believe this is a complete fix? So that sheriffbot can do all the merge stuff - https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/security-labels.md#TOC-Merge-labels

### [Deleted User] (2021-07-14)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tb...@chromium.org (2021-07-14)

Yep 100% this should be fully fixed.

### [Deleted User] (2021-07-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-15)

Requesting merge to stable M91 because latest trunk commit (900825) appears to be after stable branch point (870763).

Requesting merge to beta M92 because latest trunk commit (900825) appears to be after beta branch point (885287).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-07-15)

This bug requires manual review: We are only 4 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), benmason@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-07-15)

Let's give this a little more bake time before merging to M92 and aim to merge it for the first security refresh.

### am...@google.com (2021-07-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-07-22)

Congrats, David-- The VRP Panel has decided to award you $10,000 for this report. Nice work! 

### am...@google.com (2021-07-23)

Approved for merge to M92, please merge to branch 4515 at your earliest convenience. 
Also, approved for merge to M91 as this has become the Extended Stable release branch; please also merge to branch 4472. Thank you! 

### am...@google.com (2021-07-23)

[Empty comment from Monorail migration]

### sr...@google.com (2021-07-29)

re-opening to get engineer attention for the merge

Please merge to M92 asap ( before EOD thursday July 29)

### dp...@chromium.org (2021-07-29)

Cherrypicked https://chromium-review.googlesource.com/c/chromium/src/+/3018421 to M92

### gi...@appspot.gserviceaccount.com (2021-07-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6411996ec3d8211269c1e3e4beabcecdc18dba68

commit 6411996ec3d8211269c1e3e4beabcecdc18dba68
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Thu Jul 29 22:01:52 2021

Fix case where an extension could open a pinned grouped tab.

(cherry picked from commit e06d6c59ec36066fa8ff9b9874b63c7e189fc1da)

Bug: 1209469
Change-Id: Ib3dea05cbc1f8b29450a336a3089e0e2a6a8e9cf
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3018421
Commit-Queue: Peter Boström <pbos@chromium.org>
Auto-Submit: Taylor Bergquist <tbergquist@chromium.org>
Reviewed-by: Peter Boström <pbos@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#900825}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3061459
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Commit-Queue: David Pennington <dpenning@chromium.org>
Cr-Commit-Position: refs/branch-heads/4515@{#1917}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/6411996ec3d8211269c1e3e4beabcecdc18dba68/chrome/browser/ui/tabs/tab_strip_model.cc


### am...@chromium.org (2021-07-30)

Hello dpenning@, apologies for the ping on another on this morning - but since this issue was discovered in M91, could you please merge to M91 branch 4472, asap for this issue to be a part of the extended stable release since we are moving toward a 4W stable release cycle. Thank you!

### pb...@chromium.org (2021-07-30)

I'll take care of the merge, David's out today.

### gi...@appspot.gserviceaccount.com (2021-07-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/35c7ba7daee91b9cbcdc5e805edb1f96336d2a59

commit 35c7ba7daee91b9cbcdc5e805edb1f96336d2a59
Author: Peter Boström <pbos@chromium.org>
Date: Fri Jul 30 18:33:48 2021

Fix case where an extension could open a pinned grouped tab.

(cherry picked from commit e06d6c59ec36066fa8ff9b9874b63c7e189fc1da)

(cherry picked from commit 6411996ec3d8211269c1e3e4beabcecdc18dba68)

Bug: 1209469
Change-Id: Ib3dea05cbc1f8b29450a336a3089e0e2a6a8e9cf
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3018421
Commit-Queue: Peter Boström <pbos@chromium.org>
Auto-Submit: Taylor Bergquist <tbergquist@chromium.org>
Reviewed-by: Peter Boström <pbos@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#900825}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3061459
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Commit-Queue: David Pennington <dpenning@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4515@{#1917}
Cr-Original-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3062587
Reviewed-by: Connie Wan <connily@chromium.org>
Cr-Commit-Position: refs/branch-heads/4472@{#1587}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/35c7ba7daee91b9cbcdc5e805edb1f96336d2a59/chrome/browser/ui/tabs/tab_strip_model.cc


### am...@chromium.org (2021-08-02)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

This bug is a regression and does not impact stable. Removing incorrectly added Release- labels.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-06)

closing as Fixed as was only re-opened in https://crbug.com/chromium/1209469#c28 to get attention for merge to 92 which was achieved. Need Sheriffbot to stop removing valid labels.

### am...@google.com (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

This bug is a regression and does not impact stable. Removing incorrectly added Release- labels.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-07)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### ad...@google.com (2021-08-07)

Apologies for label change spam - this was a bug in our changes to make Sheriffbot work with the Extended Stable branch.

### rz...@google.com (2021-08-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-11)

[Empty comment from Monorail migration]

### rz...@google.com (2021-08-19)

[Empty comment from Monorail migration]

### gi...@google.com (2021-08-20)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4a94360783033db3b52d8a03f408e6839a25b660

commit 4a94360783033db3b52d8a03f408e6839a25b660
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Fri Aug 20 17:37:48 2021

[M90-LTS] Fix case where an extension could open a pinned grouped tab.

(cherry picked from commit e06d6c59ec36066fa8ff9b9874b63c7e189fc1da)

Bug: 1209469
Change-Id: Ib3dea05cbc1f8b29450a336a3089e0e2a6a8e9cf
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3018421
Commit-Queue: Peter Boström <pbos@chromium.org>
Auto-Submit: Taylor Bergquist <tbergquist@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#900825}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3086688
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1571}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/4a94360783033db3b52d8a03f408e6839a25b660/chrome/browser/ui/tabs/tab_strip_model.cc


### rz...@google.com (2021-08-23)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1209469?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055878)*
