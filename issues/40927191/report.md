# Security: Chrome Download UI Clickjacking

| Field | Value |
|-------|-------|
| **Issue ID** | [40927191](https://issues.chromium.org/issues/40927191) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Bubbles>Download |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | fa...@gmail.com |
| **Assignee** | ch...@chromium.org |
| **Created** | 2023-08-18 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

The new Chrome download UI lacks clickjacking protection; therefore, an attacker could craft an engaging HTML page that lures the victim into launching an application or program after downloading, without their knowledge.

**VERSION**  

Chrome Version: 118.0.5951.0 (Official Build) dev (64-bit) (cohort: Dev)

**REPRODUCTION CASE**

1. Download the "poc.html" file.
2. Click the red button three times, which launches Notepad with the text 'clickjacked'.

**CREDIT INFORMATION**  

Reporter credit: Shaheen Fazim

## Attachments

- [demo.mp4](attachments/demo.mp4) (video/mp4, 643.0 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.0 KB)

## Timeline

### [Deleted User] (2023-08-18)

[Empty comment from Monorail migration]

### jd...@chromium.org (2023-08-18)

chlily@, would you please take a look at this? The typical clickjacking mitigation is to ignore clicks on the UI for the first ~500ms after it opens. If you search for fixed security bugs mentioning "clickjacking", you'll find a zillion.

I'm feeling generous right now, so marking this as Sev-Medium since downloads are a relatively high-risk operation. That said, whatever the user downloads will have to pass through Safe Browsing protections, and I'm not convinced that the narrow window between a file being downloaded and when the user opens the file is where they're most likely to consciously make a security decision.

[Monorail components: UI>Browser>Bubbles>Download]

### [Deleted User] (2023-08-18)

[Empty comment from Monorail migration]

### fa...@gmail.com (2023-08-18)

Thank you. When I tested the "Keep" or "Discard" buttons while downloading harmful files, I discovered that they also lack protection against Clickjacking.

### fa...@gmail.com (2023-08-18)

I believe the new download UI dialogue missed the ~500ms delay completely.

### [Deleted User] (2023-08-19)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-01)

chlily: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@chromium.org (2023-09-13)

I believe the dialog itself has InputEventActivationProtector (https://source.chromium.org/chromium/chromium/src/+/main:ui/views/window/dialog_client_view.h;l=183;drc=31fb07c05718d671d96c227855bfe97af9e3fb20) so only the row view needs it.

### gi...@appspot.gserviceaccount.com (2023-09-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e096c114b67893c9bd1a33782bf7f0299668f57f

commit e096c114b67893c9bd1a33782bf7f0299668f57f
Author: Lily Chen <chlily@chromium.org>
Date: Thu Sep 14 21:40:23 2023

[DownloadBubble] Add input event activation protector

To mitigate the risk of clickjacking, introduce a delay during which
no clicks will be processed.

Bug: 1473957
Change-Id: I2137e5602bad3ae324b462ca8ba9bffd6ba2056f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4864122
Commit-Queue: Lily Chen <chlily@chromium.org>
Reviewed-by: Xinghui Lu <xinghuilu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1196830}

[modify] https://crrev.com/e096c114b67893c9bd1a33782bf7f0299668f57f/chrome/browser/download/bubble/download_bubble_ui_controller.h
[modify] https://crrev.com/e096c114b67893c9bd1a33782bf7f0299668f57f/chrome/browser/ui/views/download/bubble/download_bubble_row_view.cc
[modify] https://crrev.com/e096c114b67893c9bd1a33782bf7f0299668f57f/chrome/browser/ui/views/download/bubble/download_bubble_row_view.h
[modify] https://crrev.com/e096c114b67893c9bd1a33782bf7f0299668f57f/chrome/browser/download/download_browsertest_utils.cc
[modify] https://crrev.com/e096c114b67893c9bd1a33782bf7f0299668f57f/chrome/browser/ui/views/download/bubble/download_bubble_row_view_unittest.cc


### ch...@chromium.org (2023-09-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-15)

[Empty comment from Monorail migration]

### am...@google.com (2023-09-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-21)

Congratulations Shaheen! The VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and reporting this issue to us!! 

### fa...@gmail.com (2023-09-22)

Thank you.

### am...@google.com (2023-09-22)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-30)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-01)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-01)

[Empty comment from Monorail migration]

### na...@google.com (2023-11-01)

[Empty comment from Monorail migration]

### vo...@google.com (2023-11-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-02)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2023-11-02)

1. One https://crrev.com/c/4999327
2. Medium - Medium size change with some conflicts but looks safe 
3. Landed to M119, not merged anywhere else
4. Yes

### na...@google.com (2023-11-02)

[Empty comment from Monorail migration]

### na...@google.com (2023-12-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-12-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3207219629c01938f5cc18259ea170bd46534cab

commit 3207219629c01938f5cc18259ea170bd46534cab
Author: Zakhar Voit <voit@google.com>
Date: Thu Dec 14 12:36:49 2023

[M114-LTS][DownloadBubble] Add input event activation protector

M114 conflict resolution:
- remove incompatible tests from download_bubble_row_view_unittest.cc
- use raw pointers instead of WeakPtr

To mitigate the risk of clickjacking, introduce a delay during which
no clicks will be processed.

(cherry picked from commit e096c114b67893c9bd1a33782bf7f0299668f57f)

Bug: 1473957
Change-Id: I2137e5602bad3ae324b462ca8ba9bffd6ba2056f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4864122
Commit-Queue: Lily Chen <chlily@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1196830}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4999327
Commit-Queue: Zakhar Voit <voit@google.com>
Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Reviewed-by: Lily Chen <chlily@chromium.org>
Cr-Commit-Position: refs/branch-heads/5735@{#1651}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/3207219629c01938f5cc18259ea170bd46534cab/chrome/browser/download/bubble/download_bubble_ui_controller.h
[modify] https://crrev.com/3207219629c01938f5cc18259ea170bd46534cab/chrome/browser/ui/views/download/bubble/download_bubble_row_view.cc
[modify] https://crrev.com/3207219629c01938f5cc18259ea170bd46534cab/chrome/browser/ui/views/download/bubble/download_bubble_row_view.h
[modify] https://crrev.com/3207219629c01938f5cc18259ea170bd46534cab/chrome/browser/download/download_browsertest_utils.cc
[modify] https://crrev.com/3207219629c01938f5cc18259ea170bd46534cab/chrome/browser/ui/views/download/bubble/download_bubble_row_view_unittest.cc


### vo...@google.com (2023-12-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1473957?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40927191)*
