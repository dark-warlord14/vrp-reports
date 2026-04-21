# Security: Chrome on Android Hide Fullscreen Notification Toast When Multiple Times Enter and Exit Fullscreen

| Field | Value |
|-------|-------|
| **Issue ID** | [40059501](https://issues.chromium.org/issues/40059501) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Fullscreen |
| **Platforms** | Android |
| **Reporter** | su...@gmail.com |
| **Assignee** | ji...@chromium.org |
| **Created** | 2022-04-27 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

When run setInterval method to multiple times calls requestFullScreen and append fullscreen element to another element to exit fullscreen mode, interestingly after one single tap it able to fire onfullscreenchange event multiple times.

Surprisingly I notice when onfullscreenchange event fired multiple times in one tap it able to immediately hide (dismiss) the fullscreen notification while the browser is goes into fullscreen mode.

**VERSION**

- Chrome 100.0.4896.127 on Android 11 (Mi 9T)
- Chrome Beta 101.0.4951.41 on Android 11 (Mi 9T)
- Chrome Dev 102.0.5005.22 on Android 11 (Mi 9T)
- Chrome Dev 102.0.5005.22 on Android 10 (Android Emulator Pixel\_2)

**REPRODUCTION CASE**

1. Visit attached testcase.html
2. Tap anywhere on the page
3. Tap again on the page
4. Browser goes into fullscreen without fullscreen notification toast

**CREDIT INFORMATION**  

Reporter credit: Irvan Kurniawan (sourc7)

## Attachments

- [testcase.html](attachments/testcase.html) (text/plain, 921 B)
- [Chrome for Android - Invoke requestFullScreen and Exit Multiple Times will Hide Fullscreen Notification Toast ](attachments/Chrome for Android - Invoke requestFullScreen and Exit Multiple Times will Hide Fullscreen Notification Toast) (text/plain, 3.0 MB)
- [Chrome for Android - Invoke requestFullScreen without Fullscreen Notification Toast.webm](attachments/Chrome for Android - Invoke requestFullScreen without Fullscreen Notification Toast.webm) (video/webm, 3.0 MB)

## Timeline

### su...@gmail.com (2022-04-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-27)

[Empty comment from Monorail migration]

### do...@chromium.org (2022-04-28)

I'm not sure this is a meaningful security issue as scrolling on Android Chrome also hides the location bar (which is in some ways similar to this: a user gesture ends up with the site in a "fullscreen" mode without a location bar).

+Android fullscreen folks to take a look. Assigning low severity for now, and FoundIn-96 as a suitable old version as I'm guessing this has been here for a while.

[Monorail components: Blink>Fullscreen]

### [Deleted User] (2022-04-28)

[Empty comment from Monorail migration]

### su...@gmail.com (2022-04-28)

> I'm not sure this is a meaningful security issue as scrolling on Android Chrome also hides the location bar (which is in some ways similar to this: a user gesture ends up with the site in a "fullscreen" mode without a location bar).

According to WhatWG Fullscreen API Standard "User agents should ensure, e.g. by means of an overlay, that the end user is aware something is displayed fullscreen. User agents should provide a means of exiting fullscreen that always works and advertise this to the user. This is to prevent a site from spoofing the end user by recreating the user agent or even operating system environment when fullscreen"

This only require tap gesture which normally doesn't hide the address bar. If attacker put Android status bar and address bar so it looks on the user operating system environment in the testcase.html to impersonate other origin, after tap to the page it looks convincing that Chrome is navigate to the trusted website (e.g. google.com sign in) on attacker controlled content.

Also this similar to https://crbug.com/chromium/1264561, https://crbug.com/chromium/1270052, and https://crbug.com/chromium/1301873 which assigned with higher severity.


### do...@chromium.org (2022-04-28)

Thanks for pointing out the other issues. Upping severity to Medium to match. :)

### su...@gmail.com (2022-04-28)

> Thanks for pointing out the other issues. Upping severity to Medium to match. :)

Thanks!

### [Deleted User] (2022-04-28)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-12)

jinsukkim: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2022-05-20)

jinsukkim@: Friendly ping.

### ji...@chromium.org (2022-05-23)

Regression started from https://chromium-review.googlesource.com/c/chromium/src/+/2516499 where both 
TWCDAImpl#enterFullscreenModeForTab and #fullscreenStateChangedForTab invoke the WCDA.enterFullscreenModeForTab(). On the second tap, full screen mode was already entered exited, followed by another (which is redundant and not quite correct in this case) request that puts Chrome in the fullscreen mode. again.

Needs a little more investigation as to why the notification toast is not brought up.



[1] https://chromium-review.googlesource.com/c/chromium/src/+/2516499



### ji...@chromium.org (2022-05-24)

Basically, the javascript shoots enter/exit fullscreen request too fast. Chrome can't fire the internal events in order as expected. Notification toast is triggered by #onLayoutChange [1] after the fullscreen mode is entered, but a barrage of enter/exit requests don't let the event happen in time - they come at the end in a bunch, all of them stopped early by the if statement right above it checking if there is any actual height increase indicating we entered the fullscreen mode.

The problem happens when 1) fullscreen gets exited by one of the exit requests 2) fullscreen-state-change event occurs 3) As opposed to the intention of https://chromium-review.googlesource.com/c/chromium/src/+/2516499, this turns on fullscreen mode again 3) now a series of #onLayoutChange event occurs but all early out as it doesn't see any height change (increase) at this point - bot old/new height are for fullscreen.

It can be fixed by limiting what fullscreen-state-change event does. Since this is introduced to invoke enter-fullscreen again even when it is already in fullscreen, in order to handle the fullscreen option that might have changed. It doesn't need to do anything when fullscreen was already exited.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java;l=585;drc=755573e31718405aa13648d37c73e6dbe7dfe572


### gi...@appspot.gserviceaccount.com (2022-05-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2ff6c2a00e731ac4b62c4def8fce6e9ed9e8415d

commit 2ff6c2a00e731ac4b62c4def8fce6e9ed9e8415d
Author: Jinsuk Kim <jinsukkim@chromium.org>
Date: Wed May 25 14:31:19 2022

Android: Process fullscreen state changes only when the mode is on

Fullscreen state change event in Android is used to enter fullscreen
mode again in order to deal with option-only changes even if the mode
is already on. This behavior, however, can be exploited to repeatedly
trigger the mode on and off quickly, delay the layout change events,
which results in the fullscreen notification being suppressed.

This CL modifies the behavior for fullscreen state change event. In
order to respect the intention of crrev.com/c/2516499 but also prevent
the potential issue at the same time, the flow proceeds only when
fullscreen mode is already on. It effectively stops the fullscreen mode
from being entered due to unintended state event changes.

Bug: 1320538
Change-Id: I71cc00a50cda9df70beaaf1067e32653a9de5e47
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3664159
Commit-Queue: Jinsuk Kim <jinsukkim@chromium.org>
Reviewed-by: Ted Choc <tedchoc@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1007373}

[modify] https://crrev.com/2ff6c2a00e731ac4b62c4def8fce6e9ed9e8415d/chrome/android/java/src/org/chromium/chrome/browser/tab/TabWebContentsDelegateAndroidImpl.java
[modify] https://crrev.com/2ff6c2a00e731ac4b62c4def8fce6e9ed9e8415d/chrome/android/java/src/org/chromium/chrome/browser/app/tab_activity_glue/ActivityTabWebContentsDelegateAndroid.java


### ji...@chromium.org (2022-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### am...@google.com (2022-06-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-01)

Congratulations on another one! The VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts and great work! 

### am...@google.com (2022-06-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-02)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1320538?no_tracker_redirect=1

[Auto-CCs applied]
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
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059501)*
