# Security : Heap UaF on ash/wm/splitview/split_view_divider_view.cc:168:23

| Field | Value |
|-------|-------|
| **Issue ID** | [40065422](https://issues.chromium.org/issues/40065422) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | st...@google.com |
| **Created** | 2023-06-06 |
| **Bounty** | $2,000.00 |

## Description

**Steps to reproduce the problem:**

1. Build chromeOS under asan
2. Run tablet mode with touch-device ( --panel=hdp is enabled while writing this report)
3. Open two tabs and drag one tab out until split view and pick the center line to the left side or right side. Sometimes pick the center line is not required.

**Problem Description:**  

Bisect: <https://chromium-review.googlesource.com/c/chromium/src/+/4428712>

I currently had no idea if this report is duplicate to other report since it's trivial bug, but I need help to security team to triage the issue.

**Additional Comments:**  

screencast: <https://drive.google.com/file/d/12r5RMyEHTcjgJB9mIlHkr5K96v47P_oV/view?usp=sharing>

\*\*Chrome version: \*\* Chromium 116.0.5816.0 \*\*Channel: \*\* Dev

**OS:** Chrome OS

## Attachments

- [no_need_drag_center_line_asan.log](attachments/no_need_drag_center_line_asan.log) (text/plain, 8.4 KB)
- [asan1.log](attachments/asan1.log) (text/plain, 5.8 KB)

## Timeline

### [Deleted User] (2023-06-06)

[Empty comment from Monorail migration]

### st...@google.com (2023-06-07)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/286212523). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

### ch...@google.com (2023-06-12)

Marked as fixed.
Project: chromium/src
Branch: refs/branch-heads/5790

commit e7d314edbbaaa35f4d690d1b90dde75827340d77
Author: Michele Fan <michelefan@chromium.org>
Date:   Fri Jun 09 00:05:19 2023

    [Merge to M115]snap-group: Fix crash on mouse hover on the divider
   
    `kebab_button_` is not initialized to nullptr and it will cause crash on mouse hover as it may potentially contain some garbage.
   
    Fixed: b/286212523
    Test: Manual
    Change-Id: I26c5aae26bb052a9dd89523dfd23b23cbb05a0ca
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4600055
    Reviewed-by: Ahmed Fakhry <afakhry@chromium.org>
    Commit-Queue: Michele Fan <michelefan@chromium.org>
    Cr-Commit-Position: refs/branch-heads/5790@{#510}
    Cr-Branched-From: 1d71a337b1f6e707a13ae074dca1e2c34905eb9f-refs/heads/main@{#1148114}

M       ash/wm/splitview/split_view_divider_view.h

https://chromium-review.googlesource.com/4600055
02:06
02:06
Status:​Assigned      Fixed
02:06
CLs: Merged:​crrev/c/4600387      crrev/c/4600055, crrev/c/4600387
CLs: Pending:​crrev/c/4600055      <none>


### [Deleted User] (2023-06-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-12)

[Empty comment from Monorail migration]

### ch...@google.com (2023-06-20)

[Empty comment from Monorail migration]

[Monorail blocking: b/286212523]

### am...@google.com (2023-06-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-27)

Congratulations! The VRP Panel has decided to award you $2,000 for this report of a heavily mitigated security bug + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-06-29)

[Empty comment from Monorail migration]

### ch...@google.com (2023-07-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-12)

This bug is a regression and does not impact stable or extended stable.Removing incorrectly added Release- labels.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-07-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-13)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-07-18)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-09-18)

This issue was migrated from crbug.com/chromium/1451803?no_tracker_redirect=1

[Monorail blocking: b/286212523]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065422)*
