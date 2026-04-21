# Security: (Android) file download with long name cannot show the extension file it lead to spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [40918159](https://issues.chromium.org/issues/40918159) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Android |
| **Reporter** | sa...@gmail.com |
| **Assignee** | sh...@chromium.org |
| **Created** | 2023-06-21 |
| **Bounty** | $1,000.00 |

## Description

redacted

## Attachments

- video_2023-06-22_00-46-04.mp4 (video/mp4, 1.3 MB)
- downloadmenu.png (image/png, 63.9 KB)
- fileexplorer.jpg (image/jpeg, 112.4 KB)
- [Screenshot_20230720_135735_Chrome.jpg](attachments/Screenshot_20230720_135735_Chrome.jpg) (image/jpeg, 50.8 KB)

## Timeline

### [Deleted User] (2023-06-21)

[Empty comment from Monorail migration]

### xi...@chromium.org (2023-06-21)

Thanks for the report. This report is for spoofing the file type. There is a similar report that spoofs the download origin https://crbug.com/1281972. Triage it the same way. +shaktisahu@ to take a look.

[Monorail components: UI>Browser>Downloads]

### [Deleted User] (2023-06-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-23)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-06)

shaktisahu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-10)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ts...@chromium.org (2023-07-12)

Adding some CCs. dtrainor - is there someone who might have cycles to look at this?

### dt...@chromium.org (2023-07-20)

Yeah we should be able to truncate the file name and not the extension.  I believe we do this in other places.  shaktisahu@ can you take a look?  Let me know if you're unable and I can try to get to it.

### [Deleted User] (2023-07-20)

shaktisahu: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2023-07-20)

I see a warning dialog "File might be harmful" / "Do you want to download apkllllllllllllllllllllll<.....char repeats 3 lines .....>.puf.$apk anyway?"

This is in my canary as well as stable. 

### sh...@chromium.org (2023-07-20)

I am using Android 13 on SM-S906UI Build/TP1A.. with Chrome 114.0.5735.197

### sh...@chromium.org (2023-07-20)

Marking as Needs-Feedback as I can't repro

### sa...@gmail.com (2023-07-20)

Previously, my Chrome version was version 99 dev, then I updated to 116 dev (because I haven't updated via Playstore for a long time). then I run the POC on version 116 dev

### ct...@chromium.org (2023-07-20)

If we can elide in the middle to preserve start of filename and the entire extension, that seems ideal (as mentioned in c#8). Eliding at the start could be okay (it would preserve the extension), but would be a regression in usability as it would make it harder for the user to know what the file is in the long-but-not-abusive case.

### sh...@chromium.org (2023-07-21)

WIP CL: https://chromium-review.googlesource.com/c/chromium/src/+/4706260

### dr...@chromium.org (2023-08-07)

[security shepherd] shaktisahu@ - the WIP CL seems to be mostly reviewed. Will that fix this issue? Is there anything blocking it from being landed?

### za...@google.com (2023-08-11)

Secondary shepherd here, any update for this bug shaktisahu@? I see the CL is ready for review and mostly reviewed.

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### sa...@gmail.com (2023-09-04)

hello any updates?

### sa...@gmail.com (2023-09-18)

hello any updates?

### gi...@appspot.gserviceaccount.com (2023-09-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6c1a0cec38d714f2c82c9bdb319409c597781acd

commit 6c1a0cec38d714f2c82c9bdb319409c597781acd
Author: Shakti Sahu <shaktisahu@chromium.org>
Date: Wed Sep 20 22:41:24 2023

Elide filename and domains on start to show the extension / eTLD+1

Two changes:
1. The download home list item title was modified to make room for
file name extension and was elided in the middle. This is in line
with what notification does today.
2. The download home list item description was also modified in a
similar way as the notification code currently does. For very long
URLs it will prioritize showing only the eTLD+1.

Screenshot: https://screenshot.googleplex.com/8Yur9538FCobUun
Bug: 1281972, 1456876
Change-Id: I5982266bfe5698105d3bc31dcacf9d89b9455863
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4706260
Reviewed-by: David Trainor <dtrainor@chromium.org>
Commit-Queue: Shakti Sahu <shaktisahu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1199282}

[modify] https://crrev.com/6c1a0cec38d714f2c82c9bdb319409c597781acd/chrome/browser/download/internal/android/java/src/org/chromium/chrome/browser/download/home/list/holder/AudioViewHolder.java
[modify] https://crrev.com/6c1a0cec38d714f2c82c9bdb319409c597781acd/components/browser_ui/util/android/java/src/org/chromium/components/browser_ui/util/DownloadUtils.java
[modify] https://crrev.com/6c1a0cec38d714f2c82c9bdb319409c597781acd/chrome/android/java/src/org/chromium/chrome/browser/download/DownloadNotificationFactory.java
[modify] https://crrev.com/6c1a0cec38d714f2c82c9bdb319409c597781acd/chrome/browser/download/internal/android/java/src/org/chromium/chrome/browser/download/home/list/holder/PrefetchArticleViewHolder.java
[modify] https://crrev.com/6c1a0cec38d714f2c82c9bdb319409c597781acd/chrome/browser/download/internal/android/java/src/org/chromium/chrome/browser/download/home/list/UiUtils.java
[modify] https://crrev.com/6c1a0cec38d714f2c82c9bdb319409c597781acd/chrome/browser/download/internal/android/java/src/org/chromium/chrome/browser/download/home/list/holder/PrefetchGroupedItemViewHolder.java
[modify] https://crrev.com/6c1a0cec38d714f2c82c9bdb319409c597781acd/chrome/browser/download/internal/android/java/src/org/chromium/chrome/browser/download/home/list/holder/InProgressGenericViewHolder.java
[modify] https://crrev.com/6c1a0cec38d714f2c82c9bdb319409c597781acd/chrome/browser/download/internal/android/java/src/org/chromium/chrome/browser/download/home/list/holder/InProgressVideoViewHolder.java
[modify] https://crrev.com/6c1a0cec38d714f2c82c9bdb319409c597781acd/chrome/browser/download/internal/android/java/src/org/chromium/chrome/browser/download/home/list/holder/VideoViewHolder.java
[modify] https://crrev.com/6c1a0cec38d714f2c82c9bdb319409c597781acd/chrome/browser/download/internal/android/java/src/org/chromium/chrome/browser/download/home/DownloadActivityV2Test.java
[modify] https://crrev.com/6c1a0cec38d714f2c82c9bdb319409c597781acd/chrome/browser/download/internal/android/java/src/org/chromium/chrome/browser/download/home/list/holder/GenericViewHolder.java


### sa...@gmail.com (2023-09-25)

hello any updates?

### sh...@chromium.org (2023-09-25)

This is fixed now with the CL in https://crbug.com/chromium/1456876#c21

### [Deleted User] (2023-09-25)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-25)

[Empty comment from Monorail migration]

### am...@google.com (2023-09-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-29)

Congratulations! The Chrome VRP Panel has decided to aware you $1,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-09-30)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-30)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-01)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-01)

[Empty comment from Monorail migration]

### ad...@chromium.org (2023-11-13)

[Empty comment from Monorail migration]

### es...@chromium.org (2023-11-14)

Belatedly lowering severity because of the dangerous download warning mentioned in c10, and for consistency with https://crbug.com/chromium/1500810

### es...@chromium.org (2023-11-14)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1456876?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1488306]
[Monorail components added to Component Tags custom field.]

### mi...@gmail.com (2025-01-07)

deleted

### lu...@gmail.com (2025-01-11)

deleted

### lu...@gmail.com (2025-01-11)

deleted

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40918159)*
