# Security: Hide real extension of file by many white spaces - showSaveFilePicker

| Field | Value |
|-------|-------|
| **Issue ID** | [40053668](https://issues.chromium.org/issues/40053668) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Storage>FileSystem |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | ma...@gmail.com |
| **Assignee** | as...@chromium.org |
| **Created** | 2020-10-20 |
| **Bounty** | $1,000.00 |

## Description

New bug based on "<https://crbug.com/chromium/1140403#c6> by [maciekpul@gmail.com](mailto:maciekpul@gmail.com) on Tue, Oct 13, 2020, 3:06 PM GMT+2 (6 days ago)": <https://bugs.chromium.org/p/chromium/issues/detail?id=1137247#c6>

**VULNERABILITY DETAILS**  

If windows user has the option "show all file extensions" activated in the file explorer, we can hide the real extension by adding many white chars to accept - extension.

**VERSION**  

Chrome Version: [86.0.4240.75] + [stable]  

Operating System: [Windows 10 OS Version 1903 (Build 18362.1082)]

**REPRODUCTION CASE**  

Add many white spaces to accept - extension

SOLUTION  

Accept extension shouldn't allow many white spaces. Should be limited with max chars or an array of legit chars excluding white chars.

Reporter credit: Maciej Pulikowski

## Attachments

- [picture3.png](attachments/picture3.png) (image/png, 25.3 KB)
- [picture2.png](attachments/picture2.png) (image/png, 29.3 KB)
- [manyWhite.html](attachments/manyWhite.html) (text/plain, 1.7 KB)

## Timeline

### oc...@google.com (2020-10-20)

[Empty comment from Monorail migration]

[Monorail components: Blink>Storage>FileSystem]

### oc...@google.com (2020-10-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-21)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-21)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-03)

mek: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-11-17)

mek: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@gmail.com (2020-11-18)

Bug still persists in 87 version

### me...@chromium.org (2020-11-19)

We plan to not allow whitespace in extensions, and limit the length of extensions. 

### me...@chromium.org (2020-11-30)

Like the other issues, spec PR for this bug is https://github.com/WICG/file-system-access/pull/252.

### ma...@gmail.com (2020-12-04)

Issue should be fixed

https://chromium-review.googlesource.com/c/chromium/src/+/2568534
https://github.com/WICG/file-system-access/pull/252

"- Allowed code points: [A-Za-z0-9+.] "


### as...@chromium.org (2020-12-04)

Whoops, forgot to tag this bug. Thanks for the catch. Yes, the issue should now be fixed :)

### [Deleted User] (2020-12-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-05)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M88. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-05)

This bug requires manual review: M88's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2020-12-07)

asully@ please help answer https://crbug.com/chromium/1140403#c16 for merge review. 

### as...@chromium.org (2020-12-07)

There's merge approval for this CL in https://crbug.com/chromium/1152327

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/96db1e0e8c1dfdfab9b8e305e3d2f3ffc9e1ba49

commit 96db1e0e8c1dfdfab9b8e305e3d2f3ffc9e1ba49
Author: Austin Sullivan <asully@chromium.org>
Date: Mon Dec 07 22:09:02 2020

Add restrictions to allowed extensions for File System Access API

These restrictions apply to showOpenFilePicker and showSaveFilePicker.

Existing restriction:
- Extension must start with "."

New restrictions:
- Allowed code points: [A-Za-z0-9+.]
- Extension length cannot exceed to 16, inclusive of leading "."
- Extension cannot end with "."
- Extension cannot end with "local" or "lnk"

(cherry picked from commit c75c5a1e1d72fc923c82ebcaeacc874c88215eff)

Bug: 1137247, 1140403, 1140410, 1140417, 1140435, 1152327
Change-Id: I593f7ca60e05177402885bd3026add16b3a07d0c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2568534
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Commit-Queue: Austin Sullivan <asully@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#833695}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2576109
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Auto-Submit: Austin Sullivan <asully@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#649}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/96db1e0e8c1dfdfab9b8e305e3d2f3ffc9e1ba49/content/browser/file_system_access/file_system_chooser.cc
[modify] https://crrev.com/96db1e0e8c1dfdfab9b8e305e3d2f3ffc9e1ba49/content/browser/file_system_access/file_system_chooser_unittest.cc
[modify] https://crrev.com/96db1e0e8c1dfdfab9b8e305e3d2f3ffc9e1ba49/third_party/blink/renderer/modules/file_system_access/global_native_file_system.cc
[modify] https://crrev.com/96db1e0e8c1dfdfab9b8e305e3d2f3ffc9e1ba49/third_party/blink/web_tests/external/wpt/native-file-system/showPicker-errors.https.window.js


### ad...@google.com (2020-12-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-12-10)

Congratulations, the VRP panel has decided to award $1000 for this bug (and for two of your others, for $3000 total). Someone from our finance team will be in touch.

### ad...@google.com (2020-12-10)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-13)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### ja...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### as...@google.com (2021-01-28)

[Empty comment from Monorail migration]

### am...@google.com (2021-02-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1140403?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053668)*
