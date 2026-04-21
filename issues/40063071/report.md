# Security: Document PiP window can be resized and moved by compromised renderer, user can interact with sensitive UI using keyboard without being aware

| Field | Value |
|-------|-------|
| **Issue ID** | [40063071](https://issues.chromium.org/issues/40063071) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Media>PictureInPicture |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | li...@google.com |
| **Created** | 2023-02-14 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

A compromised renderer can call window.resizeTo/By and window.moveTo/By on the Document PiP window.

This likely allows for similar impacts as <https://crbug.com/chromium/1290664> and <https://crbug.com/chromium/1302159>, since the Document PiP window is also created as an inactive window and stays on top of other active windows.

Document PiP is currently in origin trial and can also be enabled via flag. It also seems to be only enforced by renderer, so in theory a compromised renderer should also be able to toggle the flag.

The size appears to be limited to ~80% of the screen, possibly due to the 0.8 aspect ratio limit on PiP windows enforced by the browser: <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/picture_in_picture/picture_in_picture_window_manager.cc;l=28;drc=c13d0b19698dacedfa4d2d71d8c4e18be0b2ee01>

A renderer can send the frame::LocalMainFrameHost::SetWindowRect() Mojo message to resize the Document PiP window: <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/public/mojom/frame/frame.mojom;l=1127;drc=c13d0b19698dacedfa4d2d71d8c4e18be0b2ee01>

The Mojo message is used by LocalDOMWindow::resizeTo/By and moveTo/By, which are guarded in the renderer by IsPictureInPictureWindow():  

moveTo: <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/frame/local_dom_window.cc;l=1873;drc=c13d0b19698dacedfa4d2d71d8c4e18be0b2ee01>  

resizeTo: <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/frame/local_dom_window.cc;l=1914;drc=c13d0b19698dacedfa4d2d71d8c4e18be0b2ee01>

**VERSION**  

Chrome Version: 112.0.5589.0 local build based on commit 5fa7fe43cbd6a5e2f87e762ac1f872a114798fe5 from February 10th  

Operating System: Windows 10 Version 21H2 (Build 19044.2486)

**REPRODUCTION CASE**  

Setup:

1. Apply renderer-move-resize.patch and rebuild Chromium to simulate compromised renderer.
2. Enable Document PiP flag: chrome://flags/#document-picture-in-picture-api  
   
   Note: There is a Origin Trial that can also be used instead of enabling the flag. Compromised renderer might also be able to enable.

PoC:  

Prerequisites: Compromised/patched renderer + enabled Document PiP flag.

1. Navigate to <https://alesandroortiz.com/security/chromium/documentpip-move-resize.html>
2. Click anywhere in page or press any key.

Observed: Document PiP window can be moved and resized like a regular popup window.  

Expected: Document PiP window cannot be moved or resized like a regular popup window.

**CREDIT INFORMATION**  

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [documentpip-move-resize.html](attachments/documentpip-move-resize.html) (text/plain, 1.2 KB)
- [renderer-move-resize.patch](attachments/renderer-move-resize.patch) (text/plain, 683 B)
- [documentpip-move-resize.mp4](attachments/documentpip-move-resize.mp4) (video/mp4, 2.6 MB)

## Timeline

### [Deleted User] (2023-02-14)

[Empty comment from Monorail migration]

### th...@chromium.org (2023-02-15)

I can reproduce this on Linux on M110.

Setting security severity medium, though it could possibly be low. Went with medium because the impact seems similar to crbug.com/1290098, except that it does not need a cooperating extension, but it does need a compromised renderer.

liberato@, could you help triage this issue as appropriate?

[Monorail components: Blink>Media>PictureInPicture]

### [Deleted User] (2023-02-15)

[Empty comment from Monorail migration]

### li...@google.com (2023-02-15)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2023-02-15)

Also, a regular renderer can also set arbitrary width and height, therefore some of the impacts that don't require moving the PiP window can be achieved by a regular renderer. An attacker page could also ask the user to move the PiP window in these cases (which is simpler than asking them to resize a window).

This behavior is part of the spec, so it might require creative mitigations such as activating the PiP window by default, or having additional checks for inactive windows over active windows.

### al...@alesandroortiz.com (2023-02-15)

https://crbug.com/chromium/1416380#c5 note: arbitrary width+height within the browser-enforced 0.8 ratio limit.

A regular popup window that initiates a Document PiP could also be used for attacks with regular renderers, since popup windows can be moved to the lower right corner and resized, and then a larger Document PiP can be opened to obscure it.

### [Deleted User] (2023-02-16)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-16)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-02)

liberato: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-17)

liberato: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### li...@google.com (2023-03-20)

i haven't forgotten about this, but also haven't gotten to it.  i don't remember why this check was in the renderer -- it was a choice between there and the browser [1],  with the idea that we'd bake it into both places before the feature is enabled outside of OT.

why it's not there now, i don't remember.

[1] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc;drc=734cfaf6710d31da1b538a12eee68eeb75d7a9e3;l=5643

### li...@google.com (2023-03-21)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-03-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2150d3777153eb71d8b227bb1dc8d00fd51a12e3

commit 2150d3777153eb71d8b227bb1dc8d00fd51a12e3
Author: Frank Liberato <liberato@chromium.org>
Date: Tue Mar 21 16:34:21 2023

Dont allow move / resize of Document PiP in browser

Browser-side equivalent of:
https://chromium-review.googlesource.com/c/chromium/src/+/3840849

Bug: 1416380
Change-Id: Iceba6b9852381b6a902b44f74778845f3493403f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4354952
Reviewed-by: Fr <beaufort.francois@gmail.com>
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Frank Liberato <liberato@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1119986}

[modify] https://crrev.com/2150d3777153eb71d8b227bb1dc8d00fd51a12e3/chrome/browser/picture_in_picture/document_picture_in_picture_window_controller_browsertest.cc
[modify] https://crrev.com/2150d3777153eb71d8b227bb1dc8d00fd51a12e3/chrome/browser/ui/browser.cc


### li...@google.com (2023-03-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-22)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-30)

Congratulations, Alesandro! The VRP Panel has decided to award you $1,000 for this report. Thank you for your efforts and reporting this issue to us. 

### am...@chromium.org (2023-03-30)

As this UI issue requires a compromised renderer as a precondition, reducing to low severity. 

### am...@google.com (2023-04-01)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2023-04-22)

Thanks for the reward!

CL looks good, although I don't have a recent build environment to properly verify fix with compromised renderer. Considering as fixed.

### am...@chromium.org (2023-04-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-02)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1416380?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063071)*
