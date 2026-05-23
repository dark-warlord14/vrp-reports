# Security: Chrome for Android Hide Entering Fullscreen Notification Toast with HTML Select Dropdown

| Field | Value |
|-------|-------|
| **Issue ID** | [40057906](https://issues.chromium.org/issues/40057906) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>FullScreen |
| **Platforms** | Android |
| **Reporter** | su...@gmail.com |
| **Assignee** | ji...@chromium.org |
| **Created** | 2021-11-13 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

On Chrome for Android after entering fullscreen it will show Android toast "Drag from top and touch the back button to exit full screen" to notify the user that the page is full screen.

I found the fullscreen toast will be immediately hidden after Chrome trigger Android Spinner i.e. from HTML5 input or select.

After initialize HTML5 select with a lot of 9000+ options, then add requestFullscreen to select onclick event handler. Interestingly after user click the select menu, the select dropdown will appear momentarily then close itself, the browser goes into fullscreen without fullscreen notification toast.

**VERSION**

- Chrome 95.0.4638.74 on Android 11; Mi 9T
- Chrome Dev 97.0.4692.10 on Android 11; Mi 9T
- Chrome Dev 97.0.4692.10 on Android 11; SM-J500F (2015 phone)
- Vivaldi Snapshot 4.4.2481.4 UA Chrome/96.0.4664.42 on Android 11; Android Emulator Pixel\_2\_API\_30

**REPRODUCTION CASE**

1. Visit attached selecthidetoast.html
2. Tap on "Tap Here" select element
3. Browser goes into fullscreen without fullscreen notification toast

**CREDIT INFORMATION**  

Reporter credit: Irvan Kurniawan (sourc7)

## Attachments

- [selecthidetoast.html](attachments/selecthidetoast.html) (text/plain, 1.7 KB)
- [selecthidetoast demonstration.mp4](attachments/selecthidetoast demonstration.mp4) (video/mp4, 179.2 KB)

## Timeline

### [Deleted User] (2021-11-13)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-11-15)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>FullScreen]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-16)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-16)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ts...@chromium.org (2021-12-07)

Assigning per chrome/browser/fullscreen/android/OWNERS, please fee to re-assign as appropriate. Thanks!

### [Deleted User] (2021-12-07)

mdjones: Uh oh! This issue still open and hasn't been updated in the last 23 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-17)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-27)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-06)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### md...@chromium.org (2022-01-06)

+jinsukkim@ as they seem to have most recently updated the code for the notification here:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java;drc=affba65e089bc0d7c2c1720f6d12e12a5cf32ae0;l=528

I haven't had time to debug this, but the notification is hidden in two call paths: when exiting fullscreen and on window focus change. My guess is that this is being triggered by a window focus change. If this is the case, we might need to loop in folks familiar with web UI or rather the delegate that triggers android UI for web pages.

### ji...@chromium.org (2022-01-06)

> My guess is that this is being triggered by a window focus change

Verified that Matt's guess is correct. The toast gets hidden due to window focus switching to the select dropdown window while the toast was being already shown. Will look into this to figure out what would be the right way to resolve this problem.

### md...@chromium.org (2022-01-06)

Thanks for picking this up Jinsuk!

### ji...@chromium.org (2022-01-07)

I think the toast should be closed either when the toast UI times out when fullscreen is exited, not when window focus is lost. Therefore the toast UI should be restored when focus comes back. My idea is that we simply flip the visibility of the toast the window at window focus event, rather than close it permanently.  

Not sure if it can happen that the focus never comes back to the main window, in which case the toast remains invisible and eventually gets removed upon timeout or fullscreen exit. I believe it can be looked into when the issue is actually reported.

### gi...@appspot.gserviceaccount.com (2022-01-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9126f59e3fe456c8bad83424bab74ec514380e79

commit 9126f59e3fe456c8bad83424bab74ec514380e79
Author: Jinsuk Kim <jinsukkim@chromium.org>
Date: Mon Jan 10 18:13:27 2022

Android: Extend the fullscreen toast duration when defocused

If the fullscreen toast message becomes invisible due to other window
stealing the focus, pause the timer of the toast and resume it
when the focus is regained. In this way we can guarantee that the toast
will be visible to users for the fixed amount of time.

Bug: 1270052
Change-Id: I4f80e160cb8b230de48473afbaf782443b6ff27d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3372521
Reviewed-by: Matthew Jones <mdjones@chromium.org>
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Commit-Queue: Jinsuk Kim <jinsukkim@chromium.org>
Cr-Commit-Position: refs/heads/main@{#957110}

[modify] https://crrev.com/9126f59e3fe456c8bad83424bab74ec514380e79/chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java


### ji...@chromium.org (2022-01-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-22)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-28)

Congratulations! The VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and nice work! 

### am...@google.com (2022-01-29)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-02-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-05-12)

Hello- we consider attachments/pocs included with reports to be an integral part of the report, so I've un-deleted them. Thanks!

### am...@google.com (2022-07-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### es...@chromium.org (2023-04-27)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1270052?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057906)*
