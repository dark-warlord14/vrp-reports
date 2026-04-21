# Security: container-overflow in ExtensionsToolbarContainer::SetExtensionIconVisibility

| Field | Value |
|-------|-------|
| **Issue ID** | [40057806](https://issues.chromium.org/issues/40057806) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | em...@chromium.org |
| **Created** | 2021-11-03 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

If you delete a extension while dragging, the container-overflow will be triggered.

**VERSION**  

Chrome Version: 97.0.4690.1 (Official Build) canary\_asan (win64)  

Operating System: Windows 10

**REPRODUCTION CASE**

1. Install two extensions from "chrome web store", pin those extensions.
2. Install the attached extension (let's say this is the third extension).
3. Once installed, the extension will open page.html in a new tab, then pin the extension. After that, click anywhere on the page.
4. Drag the third extension, and drop it after this extension is deleted (Ten seconds after being clicked, page.html will uninstall the extension using chrome.management.uninstallSelf).

**CREDIT INFORMATION**  

Reporter credit: Chen Rong

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 16.6 KB)
- [background.js](attachments/background.js) (text/plain, 39 B)
- [manifest.json](attachments/manifest.json) (text/plain, 169 B)
- [page.html](attachments/page.html) (text/plain, 98 B)
- [page.js](attachments/page.js) (text/plain, 135 B)

## Timeline

### [Deleted User] (2021-11-03)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-11-03)

I haven't reproduced this one yet. Setting the component and severity for now.

[Monorail components: Platform>Extensions]

### va...@chromium.org (2021-11-03)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-11-03)

It doesn't look like the code in question hasn't changed in a while so this probably affects Stable.
finnur@ -- can you please confirm that too when you take a look?

### rd...@chromium.org (2021-11-04)

Finnur hasn't worked on extensions in awhile (though you're always welcome to dive back in! ; ))

Passing to emiliapaz@.  Emilia, can you take a look at this?

### va...@chromium.org (2021-11-04)

Re https://crbug.com/chromium/1266510#c5: Sorry, I assigned based on chrome/browser/ui/extensions/OWNERS.

### em...@chromium.org (2021-11-05)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/92cf863b4197ec51ed3d0be9aa9abd33a78165c7

commit 92cf863b4197ec51ed3d0be9aa9abd33a78165c7
Author: Emilia Paz <emiliapaz@chromium.org>
Date: Mon Nov 08 18:47:23 2021

[Extensions] Drag/drop pinned extensions only when the extension exists

An extension can be deleted while dragging. Now, dropping will only
happen if there is an action for the extension dragged (either if the
drag was inside or outside the container).

Screencast:
https://screencast.googleplex.com/cast/NTI4ODA4NjgxMzU0MDM1MnwzNzU0MjBjNS0zMQ

Bug: 1266510

Change-Id: Ib7ed338ac792d455143008d81cbb0552092cec51
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3263281
Reviewed-by: Caroline Rising <corising@chromium.org>
Commit-Queue: Emilia Paz <emiliapaz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#939447}

[modify] https://crrev.com/92cf863b4197ec51ed3d0be9aa9abd33a78165c7/chrome/browser/ui/views/extensions/extensions_toolbar_container.cc


### em...@chromium.org (2021-11-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-08)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jd...@chromium.org (2021-11-08)

Assuming this has been in Chrome for a while, so setting FoundIn to current extended support and stable releases.

Setting OS everywhere we have extensions.


### [Deleted User] (2021-11-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-09)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### em...@chromium.org (2021-11-12)

CCed ChromeOS team, since crbug.com/1268239 may be related to this fix

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### em...@chromium.org (2021-11-23)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-23)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-23)

Requesting merge to stable M96 because latest trunk commit (939447) appears to be after stable branch point (929512).

Requesting merge to beta M97 because latest trunk commit (939447) appears to be after beta branch point (938553).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-23)

Merge review required: M97 is already shipping to beta.

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
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-23)

Merge review required: M96 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-11-29)

emiliapaz@ -- I also checked in on https://crbug.com/chromium/1268239 and wanted to see if that crash is fixed and confirm we aren't introducing any potential stability issues by merging this fix? 

### em...@chromium.org (2021-11-29)

Based on https://crbug.com/chromium/1266510#c15 on [https://crbug.com/chromium/1268239](https://bugs.chromium.org/p/chromium/issues/detail?id=1268239#c15), there hasn't been a crash on M97 for the last 3 weeks.



### am...@chromium.org (2021-11-29)

Thanks, I don't see anything on canary that looks related to this fix either. approving for merge to M97 and M96. 
please go ahead and merge to m97, branch 4692 ASAP so this fix can be included in tomorrow's beta cut 

please merge to m96, branch 4664 by EOD Friday, 3 December so this fix can be included in next week's stable channel refresh -- thank you! 

### gi...@appspot.gserviceaccount.com (2021-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9da7f37785eb871a24ec9d68cb61ccef87f60644

commit 9da7f37785eb871a24ec9d68cb61ccef87f60644
Author: Emilia Paz <emiliapaz@chromium.org>
Date: Tue Nov 30 00:53:37 2021

[M97][Extensions] Drag/drop pinned extensions only when extension exists

An extension can be deleted while dragging. Now, dropping will only
happen if there is an action for the extension dragged (either if the
drag was inside or outside the container).

Screencast:
https://screencast.googleplex.com/cast/NTI4ODA4NjgxMzU0MDM1MnwzNzU0MjBjNS0zMQ

Bug: 1266510

(cherry picked from commit 92cf863b4197ec51ed3d0be9aa9abd33a78165c7)

Change-Id: Ib7ed338ac792d455143008d81cbb0552092cec51
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3263281
Reviewed-by: Caroline Rising <corising@chromium.org>
Commit-Queue: Emilia Paz <emiliapaz@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#939447}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3306864
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/branch-heads/4692@{#552}
Cr-Branched-From: 038cd96142d384c0d2238973f1cb277725a62eba-refs/heads/main@{#938553}

[modify] https://crrev.com/9da7f37785eb871a24ec9d68cb61ccef87f60644/chrome/browser/ui/views/extensions/extensions_toolbar_container.cc


### am...@google.com (2021-12-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-12-01)

Congratulations - the VRP Panel has decided to award you $1000 for this report. A member of our finance team will be in touch soon to arrange payment. Thank you for this report! 

### gi...@appspot.gserviceaccount.com (2021-12-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cf1c0bd0cef311392254af8bc60ed9040c457aa7

commit cf1c0bd0cef311392254af8bc60ed9040c457aa7
Author: Emilia Paz <emiliapaz@chromium.org>
Date: Wed Dec 01 23:50:18 2021

[M96][Extensions] Drag/drop pinned extensions only when extension exists

An extension can be deleted while dragging. Now, dropping will only
happen if there is an action for the extension dragged (either if the
drag was inside or outside the container).

Screencast:
https://screencast.googleplex.com/cast/NTI4ODA4NjgxMzU0MDM1MnwzNzU0MjBjNS0zMQ

Bug: 1266510

(cherry picked from commit 92cf863b4197ec51ed3d0be9aa9abd33a78165c7)

Change-Id: Ib7ed338ac792d455143008d81cbb0552092cec51
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3263281
Reviewed-by: Caroline Rising <corising@chromium.org>
Commit-Queue: Emilia Paz <emiliapaz@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#939447}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3307077
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/branch-heads/4664@{#1201}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/cf1c0bd0cef311392254af8bc60ed9040c457aa7/chrome/browser/ui/views/extensions/extensions_toolbar_container.cc


### ad...@google.com (2021-12-03)

[Empty comment from Monorail migration]

### ad...@google.com (2021-12-03)

[Empty comment from Monorail migration]

### am...@google.com (2021-12-06)

[Empty comment from Monorail migration]

### am...@google.com (2021-12-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### em...@chromium.org (2023-02-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-16)

The older reward-topanel https://crbug.com/chromium/1201060 has been merged into this one. Please manually review this issue to see if the duplicate is potentially eligible for a reward.



### am...@chromium.org (2023-03-06)

 https://crbug.com/chromium/1201060 was also issued a VRP reward due to it being the earlier report of this issue and not closed out/merged as duplicate until now. 

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1266510?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1201060]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057806)*
