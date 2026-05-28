# Security: heap-use-after-free on ash/wm/desks/desks_controller.cc

| Field | Value |
|-------|-------|
| **Issue ID** | [40068144](https://issues.chromium.org/issues/40068144) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-07-26 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**

1. Open at least 2 desks and 1 active window (ex:browser)
2. Navigate to overview mode (F5) on active window and delete current desk with "SHIFT+SEARCH+MINUS"
3. Observe UAF

**Problem Description:**  

This bug is requires chrome://flags "#ash-limit-shelf-items-to-active-desk" or "PerDeskShelf", base::FEATURE\_DISABLED\_BY\_DEFAULT) expire: M118

bisect: <https://chromium-review.googlesource.com/c/chromium/src/+/2225517>

tested on 115.0.5790.98 and Dev channel

**Additional Comments:**

\*\*Chrome version: \*\* 115.0.5790.98 \*\*Channel: \*\* Stable

**OS:** Chrome OS

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 22.8 KB)
- [Screencast from 27-07-23.webm](attachments/Screencast from 27-07-23.webm) (video/webm, 7.0 MB)

## Timeline

### [Deleted User] (2023-07-26)

[Empty comment from Monorail migration]

### ma...@google.com (2023-07-27)

Over to ChromeOS triage

### ch...@google.com (2023-07-28)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/293540628). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

[Monorail blocking: b/293540628]

### [Deleted User] (2023-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-28)

[Empty comment from Monorail migration]

### ch...@google.com (2023-08-04)

Project: chromium/src
Branch: main

commit 74a061d3926bed95230398f68eef0897020fac2d
Author: Daniel Andersson <dandersson@chromium.org>
Date:   Mon Jul 31 18:25:55 2023

    ash: Fix a UAF in DesksController
   
    This change fixes a use-after-free in DesksController that occurs when
    current desk is removed using an accelerator while in overview mode and
    PerDeskShelf is enabled.
   
    DesksController::RemoveDeskInternal gets a list of windows associated
    with the desk that is being removed. In the above case, it will then
    remove some windows from that desk. The list may then hold one or more
    pointers to windows that have been destroyed.
   
    BUG=b:293540628
   
    Change-Id: I32f6a1ef548a02bb655327ff83f91cdfae09ec20
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4728915
    Commit-Queue: Daniel Andersson <dandersson@chromium.org>
    Reviewed-by: Yongshun Liu <yongshun@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1177366}

M       ash/wm/desks/desks_controller.cc

https://chromium-review.googlesource.com/4728915
20:28
20:28
CLs: Merged:​<none>      crrev/c/4728915
CLs: Pending:​crrev/c/4728915      <none>

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

Congratulations, Rheza! The Chrome VRP Panel has decided to award you $2,000 for this report of a highly mitigated security bug + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-09-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-11-11)

This issue was migrated from crbug.com/chromium/1467921?no_tracker_redirect=1

[Monorail blocking: b/293540628]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40068144)*
