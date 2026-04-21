# Security: Download notification can hide "Press and hold Esc to exit full screen" 

| Field | Value |
|-------|-------|
| **Issue ID** | [40061921](https://issues.chromium.org/issues/40061921) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Bubbles>Download, UI>Browser>Downloads |
| **Platforms** | Fuchsia, Linux, Mac, Windows |
| **Reporter** | ha...@gmail.com |
| **Assignee** | xi...@chromium.org |
| **Created** | 2022-11-26 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

In <https://bugs.chromium.org/p/chromium/issues/detail?id=1352388>, it was updated when download notification and fullscreen notification is shown at the same time, then the download notification will be combined with the fullscreen notification into "Press Esc to exit fullscreen and see download" so that a user will know they they are in fullscreen mode.

However there is another type of fullscreen notification which does not get combined properly with download notification. If the fullscreen notification is combined with a Keyboard Lock "Escape" key then "Press and hold Esc to exit full screen" notification is shown. But when fullscreen notification is combined with a Keyboard Lock "Escape" key as well as download notification, it will instead show "Press Esc to exit fullscreen and see download". This will mislead users into thinking that pressing Esc will exit fullscreen when it does not. A malicious attacker can proceed to put a fake omnibox after the "Esc" key is pressed.

It should be "Press and hold Esc to exit fullscreen and see download" when all 3 are combined.

**VERSION**  

Chrome Version: 107.0.5304.107 (Official Build) (64-bit) (cohort: Stable) Operating System: Windows 10 Version 21H2 (Build 19044.2251)

**REPRODUCTION CASE**

- Enable chrome://flags/#download-bubble

1. Host attached poc.html in a HTTPS server to enable navigation.keyboard.lock()
2. Click anywhere in poc.html, see "Press Esc to exit fullscreen and see download"
3. Now press Esc, "Insert omnibox here" gets shown. If I replace it with the real omnibox the user gets tricked into thinking they have escaped fullscreen.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 706 B)
- [Untitled_ Nov 26, 2022 12_48 PM.webm](attachments/Untitled_ Nov 26, 2022 12_48 PM.webm) (video/webm, 433.1 KB)

## Timeline

### [Deleted User] (2022-11-26)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-11-26)

Here is a video showing the poc. (You can use C://Users/User/poc.html as it is a secure origin)

See that the notification shown "Press Esc to exit fullscreen and see download" instead of "Press and hold Esc to exit fullscreen and see download". Therefore when pressing "Esc" I can insert fake omnibox and a user think they exit fullscreen.

I think this is probably more severe than https://bugs.chromium.org/p/chromium/issues/detail?id=1352388 as there the message telling you to press Esc which will also escape fullscreen. While here the message telling you to press Esc but then you do not escape fullscreen, which can be abused by an attacker to draw an omnibox when "Esc" is pressed.

### ha...@gmail.com (2022-11-28)

Some important notes from the Fullscreen API and keyboard lock specs:

1) https://fullscreen.spec.whatwg.org/#security-and-privacy-considerations

"User agents should provide a means of exiting fullscreen that always works and advertise this to the user..."

Currently, when the combination of 1) keyboard lock of "escape" key, 2) download notification and 3) fullscreen is used, the means of exiting fullscreen is wrongly advertised as "Press Esc" instead of "Press and hold Esc" which enables attackers to trick the user into thinking fullscreen as mentioned in https://crbug.com/chromium/1393732#c2.

2) https://wicg.github.io/keyboard-lock/#escape-key

"Because of the special actions associated with the Escape key, when the lock() request includes the Escape key, the user agent may need to make additional changes to the UX to account for the changed behavior

For example, if the user agent shows a user message "Press ESC to exit fullscreen" when Javascript-initiated fullscreen is activated, then that message will need to be updated when keyboard lock is in effect to read "Press and hold ESC to exit fullscreen."

This is not being done here.

-------------------------------------------

Also note that the owner of the previous report shouldn't own this as it looks like they no longer own the download bubble feature (they may have left Chromium as well) (ref: https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/download/bubble/OWNERS) additionally fullscreen and keyboard lock owners should be added too.


### ct...@chromium.org (2022-11-28)

Thanks for the report and finding this additional edge case! Assigning this to xinghuilu@.

Setting OSes based on https://source.chromium.org/chromium/chromium/src/+/main:testing/variations/fieldtrial_testing_config.json;l=4274;drc=534ccc3dd8471ebe3c1186807f4cadfa671f27cd

[Monorail components: UI>Browser>Bubbles>Download UI>Browser>Downloads]

### [Deleted User] (2022-11-28)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-11-29)

I would lean towards this being Security_Severity-High as an attacker can mislead a user into thinking they have exited fullscreen after pressing "Esc" and then draw a fake omnibox when they have done so, giving them full control over the omnibox (see poc.html and https://crbug.com/chromium/1393732#c2)

But I am fine with either severity.

### [Deleted User] (2022-11-29)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2022-11-30)

Thanks for the detailed report! I'm able to reproduce. Security_Severity-Medium seems reasonable to me given how we triaged bugs that prevent fullscreen exit in the past (e.g. https://crbug.com/798105).

### gi...@appspot.gserviceaccount.com (2022-12-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bda5d9406c47681babdf501440b9d4e05ac03371

commit bda5d9406c47681babdf501440b9d4e05ac03371
Author: Xinghui Lu <xinghuilu@chromium.org>
Date: Thu Dec 01 01:09:51 2022

[DownloadBubble] Update full screen notification text in keylock mode.

In keylock mode, the original notification is "Press and hold Esc to
exit full screen". However, when combined with download notification,
the notification doesn't mention the "hold" action and is still
displayed as "Press Esc to exit full screen and see download.".

In this CL, update the text to "Press and hold Esc to exit full screen
and see download.".

before: http://screen/5KkA4AdhagnPQY2
after: http://screen/5r7feSchzFtqrL9

Bug: 1393732
Change-Id: Ibe2cca42a5a65d3ac138444543d50169f9fb69b7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4064150
Commit-Queue: Xinghui Lu <xinghuilu@chromium.org>
Reviewed-by: Peter Boström <pbos@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1077712}

[add] https://crrev.com/bda5d9406c47681babdf501440b9d4e05ac03371/components/fullscreen_control_strings_grdp/IDS_FULLSCREEN_HOLD_TO_SEE_DOWNLOADS_AND_EXIT.png.sha1
[modify] https://crrev.com/bda5d9406c47681babdf501440b9d4e05ac03371/chrome/browser/ui/exclusive_access/exclusive_access_bubble_type.cc
[modify] https://crrev.com/bda5d9406c47681babdf501440b9d4e05ac03371/components/fullscreen_control_strings.grdp


### xi...@chromium.org (2022-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-12-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-16)

Congratulations, Axel! The VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts in discovering and reporting this issue to us! 

### am...@google.com (2022-12-16)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-03)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-07)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1393732?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Bubbles>Download, UI>Browser>Downloads]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061921)*
