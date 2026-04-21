# Security: Chrome for Android Hide Entering Fullscreen Notification Toast using Multiple Toast from Failed to Copy

| Field | Value |
|-------|-------|
| **Issue ID** | [40057755](https://issues.chromium.org/issues/40057755) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>FullScreen |
| **Platforms** | Android |
| **Reporter** | su...@gmail.com |
| **Assignee** | ji...@chromium.org |
| **Created** | 2021-10-28 |
| **Bounty** | $2,500.00 |

## Description

**VULNERABILITY DETAILS**  

I noticed on Android 11 after Chrome failed to copy text from the webpage it will show toast "Failed to copy to the clipboard".

When combined with requestFullScreen the "Failed to copy to the clipboard" toast will be shown first then after few seconds the entering fullscreen toast will also shown. Interestingly when called document.execCommand("copy") multiple times the failed to copy toast will be show multiple times, surprisingly after failed to copy toast over, the entering fullscreen toast will not show.

**VERSION**  

I have been tested this multiple times (works as described) on following device:

- Xiaomi Mi 9T (aarch64) on Android 11 using Chrome 94.0.4606.85 and Chrome Dev 97.0.4681.3
- Xiaomi Redmi Note 9 (aarch64) on Android 11 using Chrome Beta 96.0.4664.27 and Chrome Dev 97.0.4681.3
- Android Emulator Pixel\_2\_API\_30 (Play Store) (x86\_64) using Opera beta UA Chrome/92.0.4515.166 and Vivaldi Snapshot UA Chrome/94.0.4606.104

On Android Emulator on Windows 10 when using Chrome the device will immediately restart after visiting the testcase due to iFrame loop, so I'm using Opera and Vivaldi as the Chromium alternative.

**REPRODUCTION CASE**

1. Visit attached hidefullscreentoast.html
2. Single tap to the page
3. Chrome will show toast "Failed to copy to the clipboard" multiple times then entering fullscreen mode
4. After "Failed to copy to the clipboard" toast over, the fullscreen toast notification will not appear or show.

**CREDIT INFORMATION**  

Irvan Kurniawan (sourc7)

## Attachments

- [hidefullscreentoast.html](attachments/hidefullscreentoast.html) (text/plain, 1.9 MB)
- [Chrome Dev - Hide Entering Fullscreen Toast on Mi 9T.mp4](attachments/Chrome Dev - Hide Entering Fullscreen Toast on Mi 9T.mp4) (video/mp4, 1.9 MB)
- [Chromium Vivaldi Snapshot - Hide Entering Fullscreen Toast on Android Emulator API 30.mp4](attachments/Chromium Vivaldi Snapshot - Hide Entering Fullscreen Toast on Android Emulator API 30.mp4) (video/mp4, 2.4 MB)

## Timeline

### [Deleted User] (2021-10-28)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-11-03)

Does not repro on Linux. I don't have an Android test device handy.

### va...@chromium.org (2021-11-03)

This is an address bar spoof with mitigating factor: The toast message constantly showing.

[Monorail components: UI>Browser>FullScreen]

### va...@chromium.org (2021-11-03)

(I don't have an Android device at the moment to try it out so leaving it as unconfirmed.)

avi@ -- would you be interested in fixing or triaging this further?


### av...@chromium.org (2021-11-03)

I have zero Android knowledge, experience, or ability to address this. We need to find an Android peep.

### da...@chromium.org (2021-11-04)

boliu@ do you know who could have a look and try repro this?

### [Deleted User] (2021-11-04)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bo...@chromium.org (2021-11-04)

tedchoc to route?

Summarizing the problem:
JS can request entering fullscreen, and chrome shows a toast with the text "Drag from top and touch the back button to exit full screen." to warn the user. This is to prevent attacks like page silently request fullscreen, then draw the omnibox at the top to spoof the real one.

Clipboard failing to copy also shows a toast and this can also be triggered by JS. There isn't any throttling or priority for toasts in chromium (afaict), and android OS behavior leads allows JS spamming the clipboard toast effectively hide the enter fullscreen toast, which is a problem.

Fullscreen toast is here:
https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java;drc=16c985c2c7681255f4f88110f0a66eb7fecaebfc;l=516

Clipboard toast is here:
https://source.chromium.org/chromium/chromium/src/+/main:ui/android/java/src/org/chromium/ui/base/Clipboard.java;drc=921b54d38d22a66fae2397ed487eed667ff03bc5;l=567


Clipboard isn't triggered by the user this case, so maybe it shouldn't be showing a toast at all.

Also clipboard isn't the only toast can be triggered from JS. I found downloads triggers a toast as well. Ultimately, we need to go through toasts, identify the security sensitive ones, and ensure they are never overridden by other toasts

### [Deleted User] (2021-11-04)

[Empty comment from Monorail migration]

### te...@google.com (2021-11-06)

I'll punt to twellington@ to triage. It would be a shame to build up a ton of infrastructure for Toasts as they're really not used much, but maybe we can do something easy and simple here.

### tw...@chromium.org (2021-11-08)

It sounds like the issue is that "failed to copy" is preventing the enter fullsceen toast from showing?

Perhaps we can cancel non-security sensitive toasts when a new toast needs to show. +PM as an FYI since this is a product behavior change.

-> routing to Jinsuk since this is fullscreen related

### [Deleted User] (2021-11-12)

jinsukkim: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-22)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ji...@chromium.org (2021-12-03)

I'm thinking of introducing ToastManager that:
 - handles the priority to prevent important messages from being hidden as reported
 - suppresses spamming Toast messages that repeat too often

All the existing Toast.makeText will be updated to go through ToastManager. And no new |Toast.makeText| or |new Toast(...)| will be allowed. 

### ji...@chromium.org (2021-12-03)

Or Toast may not be the right UI for important messages like fullscreen entrance notification.  API reference recommends an alternative[1] to Toast for apps running in the foreground.

[1] https://developer.android.com/guide/topics/ui/notifiers/toasts#alternatives_to_using_toasts

### ji...@chromium.org (2021-12-03)

I put together some possible solutions I can think of in this doc https://docs.google.com/document/d/1b05NOXOyZVPWK10BjSAqvJEWlkoy4l19S0RnEN4zC4A/edit?resourcekey=0-BWJKrdcRP1vUUvEwjOhUMg#

Maybe mattrendely@ or twellington@ could help us make a decision.

Also cc'ed lazzzis@ who has been working on Messages UI to get his thought on whether it can be a good fit.


### ad...@google.com (2021-12-07)

Consensus seems to be that this is a real issue, and not a recent change, so marking as FoundIn-96 to complete our basic security labels.

### [Deleted User] (2021-12-07)

[Empty comment from Monorail migration]

### tw...@chromium.org (2021-12-07)

Thanks for the write up Jinsuk! Will review today.

cc'ing Elvin for UX input as well

### el...@google.com (2021-12-07)

Thanks for adding! Replied in Jinsuk's doc. Summary here: 
1) Among these options, Theresa's suggestion on show our own toast-like UI seems the most ideal from a UX perspective. I think it's ok that our toasts don't match the OS level toasts' appearance (which is the current behavior iirc). 
2) I'd recommend not using Snackbars or Messages. Messages should be contextual to contents on a page, and offer users (optional) actions to complete, which is doesn't match the use case here. Snackbar doesn't dismiss on its own which makes it feel too heavy. 

### tw...@chromium.org (2021-12-07)

Thanks for the quick feedback Elvin!

### ji...@chromium.org (2021-12-07)

Thanks elvinhu@ and twellington@.  Will go with a custom view.

### gi...@appspot.gserviceaccount.com (2021-12-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/df07056850f5788da2f16375b79b1a1180a07395

commit df07056850f5788da2f16375b79b1a1180a07395
Author: Jinsuk Kim <jinsukkim@chromium.org>
Date: Wed Dec 22 01:00:40 2021

Android: Custom Toast view for fullscreen

Replaces the framework-provided Toast widget with a custom view
implementation for fullscreen notification UI. The custom view lets us
avoid the UI from being canceled or hidden by other Toast messages.

Bug: 1264561
Change-Id: If8d425d875bdd26e1cf82623bacfbe19ca56d8eb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3329596
Reviewed-by: Sinan Sahin <sinansahin@google.com>
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Commit-Queue: Jinsuk Kim <jinsukkim@chromium.org>
Cr-Commit-Position: refs/heads/main@{#953391}

[add] https://crrev.com/df07056850f5788da2f16375b79b1a1180a07395/chrome/android/java/res/layout/fullscreen_notification.xml
[modify] https://crrev.com/df07056850f5788da2f16375b79b1a1180a07395/chrome/android/chrome_java_resources.gni
[modify] https://crrev.com/df07056850f5788da2f16375b79b1a1180a07395/ui/android/java/res/values-v17/styles.xml
[modify] https://crrev.com/df07056850f5788da2f16375b79b1a1180a07395/chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java
[modify] https://crrev.com/df07056850f5788da2f16375b79b1a1180a07395/chrome/android/java/res/values/dimens.xml
[add] https://crrev.com/df07056850f5788da2f16375b79b1a1180a07395/chrome/android/java/res/drawable/pill_background.xml


### ji...@chromium.org (2021-12-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-12-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a62652a590df20ab936dcb8b30c22095e01386c6

commit a62652a590df20ab936dcb8b30c22095e01386c6
Author: Theresa Sullivan <twellington@chromium.org>
Date: Wed Dec 22 17:14:29 2021

Revert "Android: Custom Toast view for fullscreen"

This reverts commit df07056850f5788da2f16375b79b1a1180a07395.

Reason for revert: cause of test failures

Original change's description:
> Android: Custom Toast view for fullscreen
>
> Replaces the framework-provided Toast widget with a custom view
> implementation for fullscreen notification UI. The custom view lets us
> avoid the UI from being canceled or hidden by other Toast messages.
>
> Bug: 1264561
> Change-Id: If8d425d875bdd26e1cf82623bacfbe19ca56d8eb
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3329596
> Reviewed-by: Sinan Sahin <sinansahin@google.com>
> Reviewed-by: Theresa Sullivan <twellington@chromium.org>
> Commit-Queue: Jinsuk Kim <jinsukkim@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#953391}

Bug: 1264561, 1282137
Change-Id: I6895d238fe5a036829cf1c219860c24cb361fa75
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3353181
Auto-Submit: Theresa Sullivan <twellington@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#953574}

[delete] https://crrev.com/25638676e5fbdd65095564e5f6f16e93c71f0058/chrome/android/java/res/layout/fullscreen_notification.xml
[modify] https://crrev.com/a62652a590df20ab936dcb8b30c22095e01386c6/chrome/android/chrome_java_resources.gni
[modify] https://crrev.com/a62652a590df20ab936dcb8b30c22095e01386c6/ui/android/java/res/values-v17/styles.xml
[modify] https://crrev.com/a62652a590df20ab936dcb8b30c22095e01386c6/chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java
[modify] https://crrev.com/a62652a590df20ab936dcb8b30c22095e01386c6/chrome/android/java/res/values/dimens.xml
[delete] https://crrev.com/25638676e5fbdd65095564e5f6f16e93c71f0058/chrome/android/java/res/drawable/pill_background.xml


### tw...@chromium.org (2021-12-22)

Re-opening since CL had to be reverted due to test failures.

### gi...@appspot.gserviceaccount.com (2022-01-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/affba65e089bc0d7c2c1720f6d12e12a5cf32ae0

commit affba65e089bc0d7c2c1720f6d12e12a5cf32ae0
Author: Jinsuk Kim <jinsukkim@chromium.org>
Date: Wed Jan 05 05:33:44 2022

Reland "Android: Custom Toast view for fullscreen"

The culprit CL used a delayed post runnable to remove the notification
view from the Tab's content view. It is possible, however, the Tab
already has been destroyed by the time the runnable is executed.

This CL reinstated the CL with an additional change that replaces
the assert with if statement to check the presence of the Tab and its
content view.

This reverts commit a62652a590df20ab936dcb8b30c22095e01386c6.

Bug: 1264561, 1282137
Change-Id: I5d5c46c37310e7d450918f4bf6969eb7132922d5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3354437
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Commit-Queue: Jinsuk Kim <jinsukkim@chromium.org>
Cr-Commit-Position: refs/heads/main@{#955569}

[add] https://crrev.com/affba65e089bc0d7c2c1720f6d12e12a5cf32ae0/chrome/android/java/res/layout/fullscreen_notification.xml
[modify] https://crrev.com/affba65e089bc0d7c2c1720f6d12e12a5cf32ae0/chrome/android/chrome_java_resources.gni
[modify] https://crrev.com/affba65e089bc0d7c2c1720f6d12e12a5cf32ae0/ui/android/java/res/values-v17/styles.xml
[modify] https://crrev.com/affba65e089bc0d7c2c1720f6d12e12a5cf32ae0/chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java
[modify] https://crrev.com/affba65e089bc0d7c2c1720f6d12e12a5cf32ae0/chrome/android/java/res/values/dimens.xml
[add] https://crrev.com/affba65e089bc0d7c2c1720f6d12e12a5cf32ae0/chrome/android/java/res/drawable/pill_background.xml


### ma...@google.com (2022-01-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-07)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ji...@chromium.org (2022-02-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-08)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-17)

Congratulations, Irvan! The VRP Panel has decided to award you $2500 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-02-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-02-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2022-07-29)

This issue was migrated from crbug.com/chromium/1264561?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057755)*
