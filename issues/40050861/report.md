# Security: URL bar spoofing with prompt dialog on iOS

| Field | Value |
|-------|-------|
| **Issue ID** | [40050861](https://issues.chromium.org/issues/40050861) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation, UI>Browser>Omnibox |
| **Platforms** | iOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | eu...@chromium.org |
| **Created** | 2019-12-02 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 79.0.3945.45 beta  

Operating System: iOS

See <https://crbug.com/chromium/1029637>

**REPRODUCTION CASE**

1. Go to the test case
2. Click on the button and wait
3. On the new page, you will see an alert dialog is displayed
4. Type any website e.g gmail.com and enter
5. Observe

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 261 B)
- [IMG_8248.MP4](attachments/IMG_8248.MP4) (video/mp4, 2.1 MB)

## Timeline

### ch...@gmail.com (2019-12-02)

[Empty comment from Monorail migration]

### pa...@chromium.org (2019-12-02)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-06-29)

Reopening as discussed in https://bugs.chromium.org/p/chromium/issues/detail?id=1029637#c41.

### ch...@gmail.com (2020-06-29)

[Comment Deleted]

### bd...@chromium.org (2020-06-29)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Mobile>Messages UI>Browser>Navigation UI>Browser>Omnibox]

### bd...@chromium.org (2020-06-29)

@eugenebut could you take a look at this?
It seems a little similiar to https://bugs.chromium.org/p/chromium/issues/detail?id=1082548&q=url%20prompt%20dialog%20ios&can=1

### bd...@chromium.org (2020-06-29)

[Empty comment from Monorail migration]

### eu...@chromium.org (2020-06-30)

[Empty comment from Monorail migration]

### ch...@gmail.com (2020-06-30)

I think this report is older than https://crbug.com/chromium/1082548.

### eu...@chromium.org (2020-06-30)

Thanks for pointing out. crbug.com/1082548 has more interesting comments, so I would prefer to keep 1082548 open and this dupped. But we should count this bug as original bug for panel reward purpose.

### eu...@chromium.org (2020-06-30)

Actually we should probably track this issue separately.

### eu...@chromium.org (2020-06-30)

Hi Charlie. This bug is iOS-specific spin off from crbug.com/1029637 where you commented on proposed fix. On iOS we don't have much control over rendering, but we can block the dialog is the origin of presenting main frame is different from visible URL. I will send a CL which does just that and I would appreciate if you could review it. 



[Monorail components: -UI>Browser>Mobile>Messages]

### eu...@chromium.org (2020-07-01)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a3ec688e23097721f2d3fa7225e67b0cf214f3fd

commit a3ec688e23097721f2d3fa7225e67b0cf214f3fd
Author: Eugene But <eugenebut@chromium.org>
Date: Wed Jul 01 15:55:58 2020

[ios] Suppress JS dialogs if visible URL origin differs dialog's origin

Please see crbug.com/1029907 for details.

Bug: 1029907
Change-Id: I2dab884278ada0d2532bbb0adb4cf3d71fd7850e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2277069
Auto-Submit: Eugene But <eugenebut@chromium.org>
Reviewed-by: Gauthier Ambard <gambard@chromium.org>
Commit-Queue: Eugene But <eugenebut@chromium.org>
Cr-Commit-Position: refs/heads/master@{#784420}

[modify] https://crrev.com/a3ec688e23097721f2d3fa7225e67b0cf214f3fd/ios/web/web_state/ui/crw_web_controller_unittest.mm
[modify] https://crrev.com/a3ec688e23097721f2d3fa7225e67b0cf214f3fd/ios/web/web_state/ui/crw_wk_ui_handler.mm


### eu...@chromium.org (2020-07-01)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-01)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-01)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-02)

Your change meets the bar and is auto-approved for M85. Please go ahead and merge the CL to branch 4183 (refs/branch-heads/4183) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: benmason@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-06)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-07)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-08)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-10)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-13)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2020-07-13)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f789a964ab51d62e8ace89f9d95b8fedee845e4d

commit f789a964ab51d62e8ace89f9d95b8fedee845e4d
Author: Eugene But <eugenebut@chromium.org>
Date: Mon Jul 13 20:17:07 2020

[ios] Suppress JS dialogs if visible URL origin differs dialog's origin

Please see crbug.com/1029907 for details.

(cherry picked from commit a3ec688e23097721f2d3fa7225e67b0cf214f3fd)

Bug: 1029907
TBR: gambard@chromium.org
Change-Id: I2dab884278ada0d2532bbb0adb4cf3d71fd7850e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2277069
Auto-Submit: Eugene But <eugenebut@chromium.org>
Reviewed-by: Gauthier Ambard <gambard@chromium.org>
Commit-Queue: Eugene But <eugenebut@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#784420}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2295400
Reviewed-by: Eugene But <eugenebut@chromium.org>
Cr-Commit-Position: refs/branch-heads/4183@{#477}
Cr-Branched-From: 740e9e8a40505392ba5c8e022a8024b3d018ca65-refs/heads/master@{#782793}

[modify] https://crrev.com/f789a964ab51d62e8ace89f9d95b8fedee845e4d/ios/web/web_state/ui/crw_web_controller_unittest.mm
[modify] https://crrev.com/f789a964ab51d62e8ace89f9d95b8fedee845e4d/ios/web/web_state/ui/crw_wk_ui_handler.mm


### ad...@google.com (2020-07-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-07-23)

Congratulations, the VRP panel has awarded $500 for this bug.

### ad...@google.com (2020-07-23)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-24)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-24)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-10-07)

This issue was migrated from crbug.com/chromium/1029907?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Navigation, UI>Browser>Omnibox]
[Monorail mergedinto: crbug.com/chromium/1082548]
[Monorail components added to Component Tags custom field.]

### dt...@google.com (2025-02-13)

Bulk update of issues accidentally marked as duplicate in issue tracker migration (b/325072672)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050861)*
