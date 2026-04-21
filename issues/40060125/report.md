# Security: Heap-use-after-free in SidePanelCoordinator::PopulateSidePanel

| Field | Value |
|-------|-------|
| **Issue ID** | [40060125](https://issues.chromium.org/issues/40060125) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>TopChrome>SidePanel |
| **Platforms** | Linux |
| **Reporter** | me...@gmail.com |
| **Assignee** | co...@chromium.org |
| **Created** | 2022-07-01 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**  

repro:

1. download asan-linux-release-1019940.zip and unzip
2. run `./chrome --enable-features=SidePanelJourneys,UnifiedSidePanel --user-data-dir=/tmp/noexist http://127.0.0.1:8605/poc.html` and allow popup
3. open side panel, switch the combobox to `Journeys`, when the new tab is shown, UAF occurs.

**Problem Description:**  

SidePanelEntry has a unique\_ptr `content_view_`, it can be re-assigned in `SidePanelEntry::CacheView`[1]. The old `content_view_` can be used in `SidePanelWebUIView::ShowUI`[2].

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/side_panel/side_panel_entry.cc;l=32;drc=20aad063bc0434f1d89ccfb023efe427afd3a96c>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/side_panel/side_panel_web_ui_view.cc;l=71>

**Additional Comments:**

\*\*Chrome version: \*\* 102.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 17.8 KB)
- [poc.html](attachments/poc.html) (text/plain, 76 B)
- [poc.webm](attachments/poc.webm) (video/webm, 635.7 KB)

## Timeline

### [Deleted User] (2022-07-01)

[Empty comment from Monorail migration]

### ca...@chromium.org (2022-07-01)

Thanks for the report, I was able to reproduce this, passing this to side panel owners for further triage.
Triaging this as severity high since it's a UaF in the browser process but it requires significant user interaction (opening the side panel and choosing journeys), and as impact none since it requires features that are disabled by default.

corising: Can you help further triage this and find an appropriate owner? Since this is a security issue, fixing this should be considered a blocker for enabling the features. Thanks

[Monorail components: UI>Browser>TopChrome>SidePanel]

### ad...@google.com (2022-07-01)

(auto-cc on security bug)

### me...@gmail.com (2022-07-06)

[Comment Deleted]

### co...@chromium.org (2022-07-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-07-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/05ec2a7e6aa0137ba416dd6f175634194466392e

commit 05ec2a7e6aa0137ba416dd6f175634194466392e
Author: Caroline Rising <corising@chromium.org>
Date: Fri Jul 08 13:55:55 2022

Unified side panel: make sure current and loading entries are handled correctly if the entry to be shown is the same.

Previously we were only early exiting in a Show call if the entry to be shown matched the loading entry (or the current entry if there was no loading entry). This missed the case where if Show was called for entry A while A was already visible but entry B was loading. Now in that case we will cancel the callback to show entry B when it has loaded, leave it cached, and early return since the desired entry is already showing.

Bug: 1341168
Change-Id: I5f312002ea8bc70b4073e0161041a4fa24e21ffc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3749836
Commit-Queue: Caroline Rising <corising@chromium.org>
Reviewed-by: Peter Boström <pbos@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1022133}

[modify] https://crrev.com/05ec2a7e6aa0137ba416dd6f175634194466392e/chrome/browser/ui/views/side_panel/side_panel_coordinator_unittest.cc
[modify] https://crrev.com/05ec2a7e6aa0137ba416dd6f175634194466392e/chrome/browser/ui/views/side_panel/side_panel_coordinator.cc
[modify] https://crrev.com/05ec2a7e6aa0137ba416dd6f175634194466392e/chrome/browser/ui/views/side_panel/side_panel_coordinator.h


### co...@chromium.org (2022-07-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-09)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-13)

Congratulations! The VRP Panel has decided to award you $3,000 for this report, based on this issue not being remote exploitable and requiring significant user interaction. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-07-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-11-21)

Hello, we consider attachments/POCs included with reports to be an integral part of the report (https://g.co/chrome/vrp), so I've undeleted them.

### is...@google.com (2022-11-21)

This issue was migrated from crbug.com/chromium/1341168?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060125)*
