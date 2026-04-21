# Android Chrome FullScreen Notification Can be Overlapped by Pop-up Blocker Notification

| Field | Value |
|-------|-------|
| **Issue ID** | [40059247](https://issues.chromium.org/issues/40059247) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>FullScreen, UI>Browser>Mobile>Messages |
| **Platforms** | Android |
| **Reporter** | sh...@gmail.com |
| **Assignee** | li...@chromium.org |
| **Created** | 2022-03-30 |
| **Bounty** | $3,000.00 |

## Description

Steps to reproduce the problem:
1. Open Chrome for Android and visit : http://sha4.unaux.com/cfs.html
2. Click anywhere on the page, it will open "about:blank" window with an error image inserted in body.
3. Now click anywhere on the error image page.
4. You will notice a fake Facebook phishing page in a FULL SCREEN mode and also you will notice the pop-up blocker notification gets placed above the notification that a window has gone full-screen.

What is the expected behavior?
The Pop-up blocker notification should not be placed above the FullScreen notification else it would be difficult to know that the browser is in FullScreen mode.

What went wrong?
The browser shows the Pop-up blocker notification above the FullScreen notification.

Did this work before? N/A 

Chrome version: 99.0.4844.88  Channel: n/a
OS Version: 

This issue is similar to - https://bugs.chromium.org/p/chromium/issues/detail?id=800056

## Attachments

- [PoC-1.html](attachments/PoC-1.html) (text/plain, 375 B)
- [PoC-2(cfs).html](attachments/PoC-2(cfs).html) (text/plain, 142.2 KB)
- [Screenrecorder-2022-03-30-20-05-02-977_918x1990.mp4](attachments/Screenrecorder-2022-03-30-20-05-02-977_918x1990.mp4) (video/mp4, 6.9 MB)
- [FB-PoC.mp4](attachments/FB-PoC.mp4) (video/mp4, 4.8 MB)

## Timeline

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### hc...@google.com (2022-03-31)

This does seem like its a bug, but I don't believe that this is a security bug. Moving this to the UI>Browser>FullScreen component as that's the component of https://bugs.chromium.org/p/chromium/issues/detail?id=800056

[Monorail components: UI>Browser>FullScreen]

### hc...@google.com (2022-03-31)

+avi as nominal owner since some other bugs in that component are owned by him.

### av...@chromium.org (2022-03-31)

I have zero ability to do any work on Android.

Android folks, do you triage at the OS level?

### si...@google.com (2022-04-01)

Jinsuk, sending this your way since you've been working on fullscreen toasts.

### sh...@gmail.com (2022-04-01)

[Comment Deleted]

### sh...@gmail.com (2022-04-01)

RE https://crbug.com/chromium/1311683#c2 - Hi hchao@ thank you for checking this report out. Just curious why this report doesn't considered as a Security-Bug because if you will take a look at the old report of Chrome For Windows - https://bugs.chromium.org/p/chromium/issues/detail?id=776418 this falls under Security-Bug and it's similar to my report.

I have created another PoC with different error page which looks less suspicious and user's won't be able to figure out that they are on a phishing page.

Live - http://sha4.unaux.com/fbpoc.html

### sh...@gmail.com (2022-04-01)

[Comment Deleted]

### ji...@chromium.org (2022-04-01)

Not sure what to do to mitigate this. +cc @twellington for insight. Should any messages UI be suppressed upon entering fullscreen?

### tw...@chromium.org (2022-04-01)

> Should any messages UI be suppressed upon entering fullscreen?

We do want Messages to show while in fullscreen (infobars did previously), so we need to prevent conflict with the toast UI.

+Matt for product guidance, Armina/Xiangqi for UX and Lijin for eng.

A couple of quick ideas:
 - Can we ensure the fullscreen 'toast' is a z-index higher than Messages so that it shows up on top?
 - Can we temporarily suppress Messages while the fullscreen 'toast' is visible then resume once it's gone? (toast shows then Message shows)

[Monorail components: UI>Browser>Mobile>Messages]

### ji...@chromium.org (2022-04-01)

For z-order, the toast view is added a child to Tab's ContentView [1] Lijin, is this easy to be placed on top of Messages UI?

And the presence of toast UI can be checked by seeing if |mNotificationToast| is null or not.


[1]  https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java;l=535;drc=5326b6967d000c677efa23b9f849145b0b06df07



### la...@chromium.org (2022-04-01)

>  is this easy to be placed on top of Messages UI?
MessageContainer is added here[1]. The view added later has a higher z-index value by default. I guess MessageContainer has a higher z-order? Not clear about that.

> And the presence of toast UI can be checked by seeing if |mNotificationToast| is null or not.
If there is an observer we can we observe, MessageQueueMediator[2] can subscribe it and suspend/resume queue; this can make sure message is not visible when toast is on screen

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/res_app/layout/main.xml;l=139?q=main.xml&ss=chromium
[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/messages/ChromeMessageQueueMediator.java;l=40

### tw...@chromium.org (2022-04-01)

> For z-order, the toast view is added a child to Tab's ContentView [1] Lijin, is this easy to be placed on top of Messages UI?

We could also look a using an AnchoredPopupWindow for the fullscreen toast, which should show on top of Messages.

### li...@google.com (2022-04-15)

[Empty comment from Monorail migration]

### li...@google.com (2022-04-15)

i'm currently doing some fixes in the fullscreen toast logic for unrelated bugs (crbug.com/1316051).  jinsukkim@ suggested that i do so with this bug in mind.

i'll see if z-index works or not, since it's easy to check.  however, AnchroedPopupWindow might be a more robust solution since z-index has some caveats.

either way, i'll see which are options then we can pick.

### li...@google.com (2022-04-15)

toast.bringToFront() does not fix it.  AnchoredPopupWindow seems to work fine.  i'll write up something based on that.

### li...@google.com (2022-04-15)

[Empty comment from Monorail migration]

### li...@chromium.org (2022-04-19)

there are a few issues with using AnchoredPopupWindow.  the biggest is that it repositions itself immediately after the fade-in animation completes, for reasons that i haven't been able to figure out yet.  it looks like it's moving up by the height of the omnibox, and i remember that the slide-around logic has some weird stuff going on there.

i'm not sure if i'm anchoring the popup to the wrong thing or what.  the video in the content view doesn't move, so i suspect that it's a timing thing.  the popup is memorizing its coordinates a little too quickly.  though i'm not sure why it jumps at the end of the animation, exactly, since the AnchordPopupWindow doesn't do any sort of layout except on the initial show().

### li...@chromium.org (2022-04-19)

also of note, the popup's coordinates are, in fact, correct -- y==0.  so it's definitely something changing with android layout.

### li...@chromium.org (2022-04-19)

to quote Lando, this deal's getting worse all the time.  :)

after more investigation, delaying the popup slightly does seem to make most things work better.  so some part of layout needs to settle.  however, it doesn't help me to figure out how to tell when everything is in steady-state without relying on timing.  it definitely does seem like the omnibox is what's doing it -- the toast jumps at what looks like about three seconds, which i think is when the omnibox finally hides for real in the 'visibility gone' sense.

tried to attach to layout inspector, but haven't had much luck yet.

i also started looking at how the notification about "popup blocked" works.  maybe i'll do whatever it's doing instead of AnchoredPopupWindow.

if all goes really badly, maybe i'll just create a dialog with screen-absolute positioning (not available in PopupWindow until Q, unfortuantely), and z-ordered above everything.  i really hope there's a better solution :)


### li...@chromium.org (2022-04-19)

new idea -- Activity.addContentView.  adds a new framelayout, which should be z-ordered above the others.  initial tests seem to work much better.  haven't exactly got it working yet, but it look like it's just that i haven't gotten the layout right.  doesn't seem to be jumping around like the previous attempt.

### li...@google.com (2022-04-22)

addContentView seems to work okay.  the only two tricks are that (a) we cannot remove a content view one we've added it, and (b) every once in a while i don't see the toast.

(a) isn't too bad -- we just give the thing an ID and see if it's there or not for the current activity.  when we want to get rid of it, we set it to visibility gone.

(b) i'm not sure about yet.  it's rare.  i don't know if it's being positioned incorrectly sometimes, or if it's deciding not to show the notification sometimes because one of the many conditions isn't being met.

### gi...@appspot.gserviceaccount.com (2022-04-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4467745fff4dab3f622baf75e40aca552b9ab6dc

commit 4467745fff4dab3f622baf75e40aca552b9ab6dc
Author: Frank Liberato <liberato@chromium.org>
Date: Mon Apr 25 23:03:37 2022

Improve full screen toast for picture in picture.

Previously, chrome would display a toast to tell the user how to
exit full screen.  When switching to picture in picture, the toast
would fail to fade out since the fade-out timer was stopped while
the toast was still on-screen.  This resulted in the toast being
visible in the picture in picture window indefinitely.

This CL generally cleans up the toast logic.  In the process, it
fixes that bug.  In particular, there is no longer any time at which
the toast is attached to the view hierarchy that there is not also a
timer running to remove it.

Once we enter a state where we believe that the user must see the
toast, we'll stay in that state until either (a) we successfully
show the toast long enough for the user to see it, or (b) we exit
fullscreen.  If we find a point where we shouldn't show the toast
right now, like entering picture in picture or losing the focus,
then we'll immediately hide the toast.  When we get back into a
state where the toast is relevant, we'll re-show it.

Previously, the toast timer could be stopped and re-started when
the toast was off screen.  This CL also does away with that; the
toast must be on-screen for a sufficiently long, continuous amount
of time so the user can read it.  The user probably does not read
half until it disappears due to entering picture in picture, then
read the other half; they probably start over.  At least, that's
not what I seem to do.

Toast animations are also cleaned up.  We now only fade out the
toast when the timer expires.  If we exit full screen, or enter
picture in picture, then we abruptly remove the toast as part of
the transition.  When we re-show the toast, we'll fade it back in.
This generally looks nicer; the transitions into and out of the
cases where we'd like to show a toast are abrupt anyway, so
removing the toast is invisible.

Change-Id: I97737cb557695933ae114eb37b1463aca2ed1b24
Bug: 1316051, 1311683
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3585548
Reviewed-by: Jinsuk Kim <jinsukkim@chromium.org>
Reviewed-by: Ted Choc <tedchoc@chromium.org>
Commit-Queue: Frank Liberato <liberato@chromium.org>
Cr-Commit-Position: refs/heads/main@{#995847}

[modify] https://crrev.com/4467745fff4dab3f622baf75e40aca552b9ab6dc/chrome/android/java/res/layout/fullscreen_notification.xml
[modify] https://crrev.com/4467745fff4dab3f622baf75e40aca552b9ab6dc/chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java
[modify] https://crrev.com/4467745fff4dab3f622baf75e40aca552b9ab6dc/chrome/android/junit/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandlerUnitTest.java


### gi...@appspot.gserviceaccount.com (2022-04-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4bcc293ec988f3598833e70c086c310a1faf992b

commit 4bcc293ec988f3598833e70c086c310a1faf992b
Author: Alex Ilin <alexilin@chromium.org>
Date: Tue Apr 26 13:24:04 2022

Revert "Improve full screen toast for picture in picture."

This reverts commit 4467745fff4dab3f622baf75e40aca552b9ab6dc.

Reason for revert: causes
FullscreenManagerTest#testFullscreenOptionsUpdatedCorrectly to fail 
(https://crbug.com/1319842)

Original change's description:
> Improve full screen toast for picture in picture.
>
> Previously, chrome would display a toast to tell the user how to
> exit full screen.  When switching to picture in picture, the toast
> would fail to fade out since the fade-out timer was stopped while
> the toast was still on-screen.  This resulted in the toast being
> visible in the picture in picture window indefinitely.
>
> This CL generally cleans up the toast logic.  In the process, it
> fixes that bug.  In particular, there is no longer any time at which
> the toast is attached to the view hierarchy that there is not also a
> timer running to remove it.
>
> Once we enter a state where we believe that the user must see the
> toast, we'll stay in that state until either (a) we successfully
> show the toast long enough for the user to see it, or (b) we exit
> fullscreen.  If we find a point where we shouldn't show the toast
> right now, like entering picture in picture or losing the focus,
> then we'll immediately hide the toast.  When we get back into a
> state where the toast is relevant, we'll re-show it.
>
> Previously, the toast timer could be stopped and re-started when
> the toast was off screen.  This CL also does away with that; the
> toast must be on-screen for a sufficiently long, continuous amount
> of time so the user can read it.  The user probably does not read
> half until it disappears due to entering picture in picture, then
> read the other half; they probably start over.  At least, that's
> not what I seem to do.
>
> Toast animations are also cleaned up.  We now only fade out the
> toast when the timer expires.  If we exit full screen, or enter
> picture in picture, then we abruptly remove the toast as part of
> the transition.  When we re-show the toast, we'll fade it back in.
> This generally looks nicer; the transitions into and out of the
> cases where we'd like to show a toast are abrupt anyway, so
> removing the toast is invisible.
>
> Change-Id: I97737cb557695933ae114eb37b1463aca2ed1b24
> Bug: 1316051, 1311683
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3585548
> Reviewed-by: Jinsuk Kim <jinsukkim@chromium.org>
> Reviewed-by: Ted Choc <tedchoc@chromium.org>
> Commit-Queue: Frank Liberato <liberato@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#995847}

Bug: 1316051, 1311683, 1319842
Change-Id: I668a005d055f08cac11d8ba9dc433660d0138de2
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3607957
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Owners-Override: Alex Ilin <alexilin@google.com>
Commit-Queue: Alex Ilin <alexilin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#996132}

[modify] https://crrev.com/4bcc293ec988f3598833e70c086c310a1faf992b/chrome/android/java/res/layout/fullscreen_notification.xml
[modify] https://crrev.com/4bcc293ec988f3598833e70c086c310a1faf992b/chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java
[modify] https://crrev.com/4bcc293ec988f3598833e70c086c310a1faf992b/chrome/android/junit/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandlerUnitTest.java


### gi...@appspot.gserviceaccount.com (2022-04-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a79690768271d9ef24f068c27d12c55a6decee52

commit a79690768271d9ef24f068c27d12c55a6decee52
Author: Frank Liberato <liberato@chromium.org>
Date: Wed Apr 27 20:19:10 2022

Reland "Improve full screen toast for picture in picture."

This is a reland of commit 4467745fff4dab3f622baf75e40aca552b9ab6dc

This change removes the assert, and replaces it with a no-op.

TL;DR: ordering guarantees aren't guaranteed, and doing
nothing is okay since it'll be consistent shortly.

Original change's description:
> Improve full screen toast for picture in picture.
>
> Previously, chrome would display a toast to tell the user how to
> exit full screen.  When switching to picture in picture, the toast
> would fail to fade out since the fade-out timer was stopped while
> the toast was still on-screen.  This resulted in the toast being
> visible in the picture in picture window indefinitely.
>
> This CL generally cleans up the toast logic.  In the process, it
> fixes that bug.  In particular, there is no longer any time at which
> the toast is attached to the view hierarchy that there is not also a
> timer running to remove it.
>
> Once we enter a state where we believe that the user must see the
> toast, we'll stay in that state until either (a) we successfully
> show the toast long enough for the user to see it, or (b) we exit
> fullscreen.  If we find a point where we shouldn't show the toast
> right now, like entering picture in picture or losing the focus,
> then we'll immediately hide the toast.  When we get back into a
> state where the toast is relevant, we'll re-show it.
>
> Previously, the toast timer could be stopped and re-started when
> the toast was off screen.  This CL also does away with that; the
> toast must be on-screen for a sufficiently long, continuous amount
> of time so the user can read it.  The user probably does not read
> half until it disappears due to entering picture in picture, then
> read the other half; they probably start over.  At least, that's
> not what I seem to do.
>
> Toast animations are also cleaned up.  We now only fade out the
> toast when the timer expires.  If we exit full screen, or enter
> picture in picture, then we abruptly remove the toast as part of
> the transition.  When we re-show the toast, we'll fade it back in.
> This generally looks nicer; the transitions into and out of the
> cases where we'd like to show a toast are abrupt anyway, so
> removing the toast is invisible.
>
> Change-Id: I97737cb557695933ae114eb37b1463aca2ed1b24
> Bug: 1316051, 1311683
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3585548
> Reviewed-by: Jinsuk Kim <jinsukkim@chromium.org>
> Reviewed-by: Ted Choc <tedchoc@chromium.org>
> Commit-Queue: Frank Liberato <liberato@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#995847}

Bug: 1316051, 1311683
Change-Id: I0915b728a54777f0f0436d3bfec5ce0da4e1bcf4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3608715
Reviewed-by: Jinsuk Kim <jinsukkim@chromium.org>
Commit-Queue: Frank Liberato <liberato@chromium.org>
Reviewed-by: Ted Choc <tedchoc@chromium.org>
Cr-Commit-Position: refs/heads/main@{#996865}

[modify] https://crrev.com/a79690768271d9ef24f068c27d12c55a6decee52/chrome/android/java/res/layout/fullscreen_notification.xml
[modify] https://crrev.com/a79690768271d9ef24f068c27d12c55a6decee52/chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java
[modify] https://crrev.com/a79690768271d9ef24f068c27d12c55a6decee52/chrome/android/junit/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandlerUnitTest.java


### li...@google.com (2022-04-27)

hopefully it doesn't need to be reverted this time.

### [Deleted User] (2022-04-28)

[Empty comment from Monorail migration]

### sh...@gmail.com (2022-05-07)

[Comment Deleted]

### am...@chromium.org (2022-06-13)

setting back as a security issue; setting foundin-100 based on oldest release channel (stable) at the time of this report 

### [Deleted User] (2022-06-13)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-06-13)

Hello, OP. Apologies for the delay in response as there was not a security team individual tagged on this issue and it not being typed as a security bug created a situation where it did not end up in any queue for evaluation, except via VRP evaluation. 
I've updated this to reflect it's appropriate status as a security bug. The commit for relanding this fix has already been merged to M103, so this fix should now be part of the M103 stable release. It will receive a CVE and acknowledgement at that time. 

### am...@google.com (2022-06-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-13)

Congratulations! The VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and reporting this issue to us! 

### sh...@gmail.com (2022-06-13)

Thank you soo much team for the bounty decision! 

### [Deleted User] (2022-06-14)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-06-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ji...@chromium.org (2022-08-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-12-13)

It appears the fix for this issue was not included by the automation for inclusion in release notes and CVE processing back when this fix shipped in M103/Stable (v 103.0.5060.53) --sincere apologies for that, OP! labeling accordingly so this can be rectified soon. 

### [Deleted User] (2022-12-14)

This bug is a regression and does not impact stable or extended stable.Removing incorrectly added Release- labels.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-12-14)

Issue is FoundIn-99, first 99/Stable shipped in February, so this issue would have been definitely impacted Stable and Extended Stable at the time of reporting, so you are incorrect, bot. 

### pg...@google.com (2023-02-12)

[Empty comment from Monorail migration]

### es...@chromium.org (2023-04-27)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2023-07-28)

This issue was migrated from crbug.com/chromium/1311683?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>FullScreen, UI>Browser>Mobile>Messages]
[Monorail mergedwith: crbug.com/chromium/1350831]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059247)*
