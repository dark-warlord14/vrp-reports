# Security: WebUSB permission dialog can appear over the wrong tab 

| Field | Value |
|-------|-------|
| **Issue ID** | [40053729](https://issues.chromium.org/issues/40053729) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>USB, UI>Browser>Permissions>Prompts |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | re...@chromium.org |
| **Created** | 2020-10-28 |
| **Bounty** | $500.00 |

## Description

Chrome Version: 88.0.4305.0 canary  

Operating System: MacOS

Similar to <https://crbug.com/chromium/723503>.

**REPRODUCTION CASE**

1. Click anywhere on the page
2. Switch another tab e.g google.com
3. Observe the WebUSB permission dialog appear over google.com page

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 354 B)
- [screen.mov](attachments/screen.mov) (video/quicktime, 1.5 MB)
- [simple_poc.html](attachments/simple_poc.html) (text/plain, 207 B)

## Timeline

### wf...@chromium.org (2020-10-28)

Thanks for the report. reillyg - can you take a look at this issue?

[Monorail components: Blink>USB UI>Browser>Permissions>Prompts]

### re...@chromium.org (2020-10-28)

I swear we already had a bug open for this but I can't find it at the moment.

The high level issue is that there is complex logic in components/permissions which handles "normal" permissions requests and prevents conditions such as multiple requests appearing on top of each other and enforces that displayed requests match the currently selected tab, even swapping out which request the user sees when switching tabs. The infrastructure for the device selection bubble (used or Web Bluetooth, WebHID, WebUSB and Web Serial) does not have this and so if the page has a user activation but arranges to not be the currently selected tab it could display a prompt over a different tab.

Adding permissions OWNERS since I am not familiar with details the shared logic used for other permissions. Ideally we could reuse some of this.

### re...@chromium.org (2020-10-28)

The cleverness with redefining then() in the POC is not necessary as demonstrated by this simpler POC. I can't figure out how to open the new tab in addition to displaying the permission prompt as it appears that calling window.open() consumes the active user gesture.

### re...@chromium.org (2020-10-28)

As a matter of prioritization, I see that this was marked as "medium" severity. Is that because this issue "allows web content to tamper with trusted browser UI" or because it is similar to an address bar spoof?

### re...@chromium.org (2020-10-28)

Fix out for review: https://chromium-review.googlesource.com/c/chromium/src/+/2505746

Note, the one thing I don't like about this fix is that it doesn't seem as comprehensive as what we do for generic permissions.

### re...@chromium.org (2020-10-29)

I finally found the older report of this issue, it was filed against Web Bluetooth (which shares the same logic): https://crbug.com/825030

I'll mark that issue as a duplicate of this one since this is where I've collected more context on the problem.

### re...@chromium.org (2020-10-29)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9a99a9df56f8e7affd1e48f255fd1cf16f118b90

commit 9a99a9df56f8e7affd1e48f255fd1cf16f118b90
Author: Reilly Grant <reillyg@chromium.org>
Date: Mon Nov 02 21:34:16 2020

Ensure that chooser dialog is appearing on the active web contents

This change adds a check before creating a new chooser dialog that the
web contents it is being displayed over is the currently active one.

Bug: 1143057
Change-Id: I3a4e6fdb1745f2994e0e998fc2346d7485d118c7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2505746
Auto-Submit: Reilly Grant <reillyg@chromium.org>
Reviewed-by: Andy Paicu <andypaicu@chromium.org>
Commit-Queue: Reilly Grant <reillyg@chromium.org>
Cr-Commit-Position: refs/heads/master@{#823300}

[modify] https://crrev.com/9a99a9df56f8e7affd1e48f255fd1cf16f118b90/chrome/browser/ui/views/permission_bubble/chooser_bubble_ui.cc
[modify] https://crrev.com/9a99a9df56f8e7affd1e48f255fd1cf16f118b90/chrome/browser/usb/usb_browsertest.cc


### re...@chromium.org (2020-11-02)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-03)

Requesting merge to beta M87 because latest trunk commit (823300) appears to be after beta branch point (812852).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-11-03)

This bug requires manual review: We are only 13 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: benmason@(Android), bindusuvarna @(iOS), cindyb@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@google.com (2020-11-03)

reillyg@ - can you fill the merge questionnaire in c#15 to consider the merge request? 

### re...@chromium.org (2020-11-03)

1. Does your merge fit within the Merge Decision Guidelines?

This has been assigned a medium priority by the security team and given a target of M-87 which I assume means that it is considered critical enough to warrant a merge. The complexity of the change itself is low.

2. Links to the CLs you are requesting to merge.

https://chromium-review.googlesource.com/c/chromium/src/+/2505746

3. Has the change landed and been verified on ToT?

Verified on 88.0.4314.0.

4. Does this change need to be merged into other active release branches (M-1, M+1)?

No.

5. Why are these changes required in this milestone after branch?

The security severity is set to "medium".

6. Is this a new feature?

No.

7. If it is a new feature, is it behind a flag using finch?

No.

### la...@google.com (2020-11-03)

merge approved for M87 branch 4280

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/06c3622f9a9e8f22dfb980d138c7a3ab33a41715

commit 06c3622f9a9e8f22dfb980d138c7a3ab33a41715
Author: Reilly Grant <reillyg@chromium.org>
Date: Tue Nov 03 22:20:40 2020

Ensure that chooser dialog is appearing on the active web contents

This change adds a check before creating a new chooser dialog that the
web contents it is being displayed over is the currently active one.

(cherry picked from commit 9a99a9df56f8e7affd1e48f255fd1cf16f118b90)

Bug: 1143057
Change-Id: I3a4e6fdb1745f2994e0e998fc2346d7485d118c7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2505746
Auto-Submit: Reilly Grant <reillyg@chromium.org>
Reviewed-by: Andy Paicu <andypaicu@chromium.org>
Commit-Queue: Reilly Grant <reillyg@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#823300}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2518405
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Cr-Commit-Position: refs/branch-heads/4280@{#1097}
Cr-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}

[modify] https://crrev.com/06c3622f9a9e8f22dfb980d138c7a3ab33a41715/chrome/browser/ui/views/permission_bubble/chooser_bubble_ui.cc
[modify] https://crrev.com/06c3622f9a9e8f22dfb980d138c7a3ab33a41715/chrome/browser/usb/usb_browsertest.cc


### ad...@google.com (2020-11-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-11-11)

This was a known bug (#c7) but the VRP panel has decided to award $500 as a 'thank you' for bringing it higher up our attention stack.

### ad...@google.com (2020-11-12)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-16)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-16)

[Empty comment from Monorail migration]

### vs...@google.com (2020-12-10)

[Empty comment from Monorail migration]

### vs...@google.com (2020-12-10)

[Empty comment from Monorail migration]

### ke...@google.com (2020-12-11)

[Empty comment from Monorail migration]

### re...@chromium.org (2020-12-11)

The fix for this issue introduced https://crbug.com/chromium/1149692. So we should make sure that 83c20d21547fd6f8cf5f16a3a7e687e48390f142 gets merged to M-86 as well if this patch is.

### [Deleted User] (2020-12-14)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/13620fbbb5ca3171674c78ae04dead547bd9c1e0

commit 13620fbbb5ca3171674c78ae04dead547bd9c1e0
Author: Reilly Grant <reillyg@chromium.org>
Date: Wed Dec 16 19:09:29 2020

Ensure that chooser dialog is appearing on the active web contents

This change adds a check before creating a new chooser dialog that the
web contents it is being displayed over is the currently active one.

(cherry picked from commit 9a99a9df56f8e7affd1e48f255fd1cf16f118b90)

(cherry picked from commit 06c3622f9a9e8f22dfb980d138c7a3ab33a41715)

Bug: 1143057
Change-Id: I3a4e6fdb1745f2994e0e998fc2346d7485d118c7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2505746
Auto-Submit: Reilly Grant <reillyg@chromium.org>
Reviewed-by: Andy Paicu <andypaicu@chromium.org>
Commit-Queue: Reilly Grant <reillyg@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#823300}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2518405
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4280@{#1097}
Cr-Original-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2585092
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1494}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/13620fbbb5ca3171674c78ae04dead547bd9c1e0/chrome/browser/ui/views/permission_bubble/chooser_bubble_ui.cc
[modify] https://crrev.com/13620fbbb5ca3171674c78ae04dead547bd9c1e0/chrome/browser/usb/usb_browsertest.cc


### [Deleted User] (2020-12-18)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-01-07)

[Empty comment from Monorail migration]

### ja...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1143057?no_tracker_redirect=1

[Multiple monorail components: Blink>USB, UI>Browser>Permissions>Prompts]
[Monorail mergedwith: crbug.com/chromium/825030]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053729)*
