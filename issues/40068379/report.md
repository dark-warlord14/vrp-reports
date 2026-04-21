# Security: heap-use-after-free on ash/wm/overview/overview_item.cc

| Field | Value |
|-------|-------|
| **Issue ID** | [40068379](https://issues.chromium.org/issues/40068379) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-07-30 |
| **Bounty** | $2,000.00 |

## Description

**Steps to reproduce the problem:**

1. start with multi extended display (not mirror) on cros and one active window (ex: browser)
2. enter overview mode (F5) ,select and hold active window and enter overview mode again (F5)
3. observer UaF

**Problem Description:**  

This bug does crash on multi display. Single display was fine.

I have reverted ba77a409a302296a3305432de88359d6d306fe8e and the crash goes away.

```
Date:   Sun Jul 30 20:58:31 2023 +0700  
Revert "overview: Show jelly header when dragging in multi display"  
     
This reverts commit ba77a409a302296a3305432de88359d6d306fe8e.  

```

bisect: <https://chromium-review.googlesource.com/c/chromium/src/+/4708525>

**Additional Comments:**

\*\*Chrome version: \*\* 117.0.5897.3 \*\*Channel: \*\* Dev

**OS:** Chrome OS

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 36.5 KB)
- [Screencast from 31-07-23 20:12:27.webm](attachments/Screencast from 31-07-23 20_12_27.webm) (video/webm, 4.8 MB)

## Timeline

### [Deleted User] (2023-07-30)

[Empty comment from Monorail migration]

### rh...@gmail.com (2023-07-31)

uploading screencast

### th...@chromium.org (2023-07-31)

[Empty comment from Monorail migration]

### ch...@google.com (2023-07-31)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/293867778). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

[Monorail blocking: b/293867778]

### [Deleted User] (2023-07-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-31)

[Empty comment from Monorail migration]

### ch...@google.com (2023-08-04)

Marked as fixed.
Project: chromium/src
Branch: main

commit 1bd4358ad8f525a3b5919e65262dd9502fec1a2f
Author: Sammie Quon <sammiequon@chromium.org>
Date:   Wed Aug 02 18:49:27 2023

    overview: Fix u-a-f when dragging across multiple displays
   
    Make sure the mirror created by DragWindowController is destroyed
    before the window it is mirroring (item_widget_) is.
   
    Test: manual
    Test: ash_unittests *OverviewSessionTest.DraggingOnMultipleDisplay*
    Change-Id: I218da2ba78b1a84443fd6587eba319391853c4b4
    Fixed: b/293867778
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4740395
    Reviewed-by: Min Chen <minch@chromium.org>
    Commit-Queue: Sammie Quon <sammiequon@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1178584}

M       ash/wm/overview/overview_item.cc
M       ash/wm/overview/overview_session_unittest.cc

https://chromium-review.googlesource.com/4740395
20:52
20:52
Status:​Assigned      Fixed
20:52
CLs: Merged:​<none>      crrev/c/4740395
CLs: Pending:​crrev/c/4740395      <none>

### [Deleted User] (2023-08-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-04)

[Empty comment from Monorail migration]

### st...@google.com (2023-08-29)

[Empty comment from Monorail migration]

### am...@google.com (2023-09-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-14)

Congratulations on another one, Rheza! The Chrome VRP Panel has decided to award you $2,000 for this report of a heavily mitigated security bug + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-09-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-11-11)

This issue was migrated from crbug.com/chromium/1468813?no_tracker_redirect=1

[Monorail blocking: b/293867778]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40068379)*
