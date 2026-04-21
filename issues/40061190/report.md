# Security:  Chrome on Android the Fullscreen Notification Toast Not shown when fullscreen (screen lock mode landscape)

| Field | Value |
|-------|-------|
| **Issue ID** | [40061190](https://issues.chromium.org/issues/40061190) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Fullscreen |
| **Platforms** | Android |
| **Reporter** | sa...@gmail.com |
| **Assignee** | ji...@chromium.org |
| **Created** | 2022-09-30 |
| **Bounty** | $5,000.00 |

## Description

deleted

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2022-09-30)

[Empty comment from Monorail migration]

### mp...@chromium.org (2022-10-02)

Nice find, assigning the same people as https://crbug.com/chromium/1320538.

[Monorail components: Blink>Fullscreen]

### [Deleted User] (2022-10-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-03)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-03)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-14)

jinsukkim: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-24)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ji...@chromium.org (2022-10-28)

The hack exploits the condition on which we display the notification toast. OnLayoutChangeListener#onLayoutChange is triggered when the system UI (status/navigation bar) becomes invisible, and we check if the height got bigger (900x1500 -> 900x1600, for instance) to detect the fullscreen mode[1]

If the landscape lock is invoked as in the POC html, the layout change comes with the new size that reflects the change in not only the height but also the rotation. Therefore we get the layout change such as 900x1500 -> 1600x900, which fails to meet the condition that only cares about the height getting bigger.

One way to resolve the issue is to check both width and height, and acknowledges the fullscreen if either of them got bigger. 


 

 



[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java;l=589  

### gi...@appspot.gserviceaccount.com (2022-10-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f7878d78db2b2688c25b913caa41efb165d07715

commit f7878d78db2b2688c25b913caa41efb165d07715
Author: Jinsuk Kim <jinsukkim@chromium.org>
Date: Mon Oct 31 15:38:48 2022

Android: Check both width/height changes for fullscreen mode

When fullscreen request is followed immediately by screen rotation,
the condition checking the difference in height only cannot detect the
changes in the dimension, therefore fails to bring up the notification
toast. This CL checks both width and height to recognize the event
correctly.

Bug: 1370028
Change-Id: Ibe7c0add2137449ffedc8065205dce4e214b1152
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3990806
Reviewed-by: Matthew Jones <mdjones@chromium.org>
Commit-Queue: Jinsuk Kim <jinsukkim@chromium.org>
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1065504}

[modify] https://crrev.com/f7878d78db2b2688c25b913caa41efb165d07715/chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java
[modify] https://crrev.com/f7878d78db2b2688c25b913caa41efb165d07715/chrome/android/junit/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandlerUnitTest.java


### ji...@chromium.org (2022-10-31)

[Empty comment from Monorail migration]

### ji...@chromium.org (2022-10-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-31)

[Empty comment from Monorail migration]

### am...@google.com (2022-11-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-03)

Congratulations, Hafiizh! The VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-11-04)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-01-09)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### pg...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xp...@gmail.com (2023-02-06)

PoC should be undeleted ♥️

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1370028?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1373179]
[Monorail components added to Component Tags custom field.]

### ji...@chromium.org (2024-11-19)

b/40068581 -> jinsukkim@google.com

### bu...@google.com (2024-11-19)

You can't assign/cc Bugjuggler on closed bugs. You can make Bugjuggler the verifier though (go/bugjuggler#verifier).

### ji...@google.com (2024-11-19)

b/40068581 -> jinsukkim@google.com

### bu...@google.com (2024-11-19)

You can't assign/cc Bugjuggler on closed bugs. You can make Bugjuggler the verifier though (go/bugjuggler#verifier).

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061190)*
