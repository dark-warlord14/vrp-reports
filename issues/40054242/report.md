# Security: Access to camera with clickjacking and popup window

| Field | Value |
|-------|-------|
| **Issue ID** | [40054242](https://issues.chromium.org/issues/40054242) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Permissions>Prompts |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | fj...@chromium.org |
| **Created** | 2020-12-19 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

It's possible to get the user to click the "Allow" button on the camera (or similar request dialogs) with the help of a popup window.

**VERSION**  

Chrome Version: 87.0.4280.88 + stable  

Operating System: Windows 10

**REPRODUCTION CASE**

1. Open a popup window at the same coordinates as the parent window
2. Call `getUserMedia` in the parent tab
3. User will be clicking in the popup window
4. The popup windows closes making the user click the "Accept" button

The exact x/y coordinates of the "Allow" button may differ by a few px depending on the user's Chrome UI, but mostly they should be the same.

Demo: <https://vuln.websec.blog/cam/>

**CREDIT INFORMATION**  

Reporter credit: Thomas Orlita

## Attachments

- [index.html](attachments/index.html) (text/plain, 1.1 KB)
- [game.html](attachments/game.html) (text/plain, 774 B)
- [camera.avi](attachments/camera.avi) (application/octet-stream, 2.2 MB)

## Timeline

### [Deleted User] (2020-12-19)

[Empty comment from Monorail migration]

### st...@gmail.com (2020-12-19)

I noticed the Permission request UI has changed in Chrome 88+ and now requires two clicks to allow access.

So, `navigator.getUserMedia({ video: true })` won't work in the new Chrome version.

However, if we also request pan/tilt/zoom permission, it'll use the old UI: `navigator.getUserMedia({ video: { pan: true, tilt: true, zoom: true } })`

### ca...@chromium.org (2020-12-21)

engedy: Can you help further triage this from the permissions side? I was able to reproduce this on stable, and it looks like pan/tilt resulting in the old UI might be a bug.

[Monorail components: UI>Browser>Permissions>Prompts]

### [Deleted User] (2020-12-22)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-22)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-01-03)

engedy: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-01-17)

engedy: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### en...@chromium.org (2021-01-17)

What you are seeing is the new "permission chip" style permission UI, but that is still experimental, and it is not yet supported for camera PTZ, this is why the old style permission prompt is being displayed for PTZ. That part is working as intended.

Regarding the clickjacking part, in general I agree that for permission prompts not using the "permission chip" pattern, there should be a short delay (0.5-1.0 secs, TBD w/ UX folks) before the "Accept" button becomes clickable after the dialog is shown. The "Deny" button should still be clickable immediately. 

This should already be achieved, however, by the fact that the dialog is ignoring a subsequent click that follows the previous one within the double-click duration. I will investigate why this might not be functioning in this particular situation.

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### wf...@chromium.org (2021-02-24)

Hi engedy, I wonder if you had any update here, has the PTZ permission started using the new method now? Is this bug still valid?

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### en...@chromium.org (2021-03-10)

Kamila, can you please take a look and evaluate what we can do here?

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-07-08)

hkamila@, any update?

### es...@chromium.org (2021-07-21)

I can still repro this in Chrome 94, though the PoC gets me to click the Block button rather than Allow. :)

### hk...@google.com (2021-07-22)

Sorry this got lost in my "I need to look at this later" list. Investigating now.

### hk...@google.com (2021-07-22)

Adding this to our fixit-week agenda. 

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-07-20)

engedy - is there perhaps another owner who could look at this very old bug? Thanks!

### hk...@google.com (2022-07-21)

I'm un-assigning, as I have no bandwidth right now. 

### am...@chromium.org (2022-07-28)

Hi hkamila@ security bugs cannot go without an owner, please coordinate assignment with another appropriate owner who can take this issue on. Thank you.

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### en...@chromium.org (2022-09-14)

Routing to Florian who volunteered to take a look.

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### fj...@chromium.org (2022-11-23)

Still reproducible in M110. To protect against this type of attack more generically, To resolve I think it makes sense to reactivate the input protector (https://source.chromium.org/chromium/chromium/src/+/main:ui/views/input_event_activation_protector.h) whenever the window showing the prompt has been in the background and just became the top window. The input protector will ignore fast consecutive clicks  (faster than the user's double click interval) if they start within the double click's interval from  the moment it is activated. If there's a window switch and more than the double click interval has passed, or if there's a pause longer than the double click interval between two clicks, the last click will be accepted.

We can observe the prompt bubble widget's OnWidgetActivationChanged. Because the prompt bubble widget is not a top level widget, we can't rely on its state alone to determine the window switch situation. However we can use the trigger and use widget and browser window widget states to determine whether the bubble is in the top window. Because the observation of the prompt bubble only starts after bubble creation, this logic is not triggered if there are no window switches. Afterwards, any top window change which brings the window with the prompt to the top will reactivate the input protection.

### fj...@chromium.org (2022-11-24)

[Empty comment from Monorail migration]

### fj...@chromium.org (2022-11-24)

Cc: pkasting@ for context on review and tungnh@ who is working on a similar issue

CL of the above approach is on Gerrit, but hasn't gone through review yet: https://chromium-review.googlesource.com/c/chromium/src/+/4051581

### en...@chromium.org (2022-11-24)

Florian, after your patch, what will be the behavior in the following scenario (changed in step 4 compared to the original repro):

1. Open a popup window at the same coordinates as the parent window
2. Call `getUserMedia` in the parent tab
3. User will be clicking in the popup window
4. The popup windows is not closed, but appropriately *resized* to a smaller size to reveal the "Allow" button

That is, in this case, there is a single click on the dialog. I imagine the mouse-down event will activate the dialog, so by the time there is mouse-up and the button click event is dispatched, the input protector will have been activated?

What about the following, benign scenario?

1. Two windows side-by-side, no popups.
2. Call `getUserMedia` in window A.
3. Users switches to window B.
4. User notices the prompt in window A, and clicks the "Allow" button.

In this case, I would expect that the click should be accepted.



### fj...@chromium.org (2022-11-24)

Scenario 1: no issue, because there is a window switch --> input protection is triggered with the proposed solution
Scenario 2: yes this is a restriction of this approach. A second click will be accepted. I do think that this is a somewhat uncommon case, supporting it would incur significant overhead. We can't just check for overlapping windows, we would need to check whether each window overlaps with the widget (not with the window containing the widget). We would also need to continually check for this.

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### fj...@chromium.org (2022-12-09)

Adding kerenzhu@ as he was proposed as additional reviewer by pkasting@

### gi...@appspot.gserviceaccount.com (2022-12-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b491e7324d790f854c8c80f17b21ddf8348a0a1f

commit b491e7324d790f854c8c80f17b21ddf8348a0a1f
Author: Florian Jacky <fjacky@chromium.org>
Date: Mon Dec 19 21:32:08 2022

Enable input protection for window changes

Refer to issue description for more details

Bug: 1160485
Change-Id: I4e92aac004c66821553280e1e81cc49a3d9c082b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4051581
Commit-Queue: Florian Jacky <fjacky@chromium.org>
Reviewed-by: Keren Zhu <kerenzhu@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1085116}

[modify] https://crrev.com/b491e7324d790f854c8c80f17b21ddf8348a0a1f/ui/views/window/dialog_client_view.h
[modify] https://crrev.com/b491e7324d790f854c8c80f17b21ddf8348a0a1f/chrome/browser/ui/views/permissions/permission_prompt_bubble.h
[modify] https://crrev.com/b491e7324d790f854c8c80f17b21ddf8348a0a1f/chrome/browser/ui/views/permissions/chip_controller.h
[modify] https://crrev.com/b491e7324d790f854c8c80f17b21ddf8348a0a1f/ui/views/window/dialog_client_view.cc
[modify] https://crrev.com/b491e7324d790f854c8c80f17b21ddf8348a0a1f/chrome/browser/ui/views/permissions/chip_controller.cc
[modify] https://crrev.com/b491e7324d790f854c8c80f17b21ddf8348a0a1f/chrome/browser/ui/views/permissions/permission_prompt_bubble.cc
[modify] https://crrev.com/b491e7324d790f854c8c80f17b21ddf8348a0a1f/ui/views/window/dialog_delegate.cc
[modify] https://crrev.com/b491e7324d790f854c8c80f17b21ddf8348a0a1f/ui/views/window/dialog_delegate.h


### gi...@appspot.gserviceaccount.com (2022-12-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ac826440f3dfd4b852fa6d9612457ae1092c1d01

commit ac826440f3dfd4b852fa6d9612457ae1092c1d01
Author: Nidhi Jaju <nidhijaju@chromium.org>
Date: Tue Dec 20 01:29:55 2022

Revert "Enable input protection for window changes"

This reverts commit b491e7324d790f854c8c80f17b21ddf8348a0a1f.

Reason for revert: Making several permission chip related tests fail on "chromium/ci/linux-ubsan-vptr" i.e. https://ci.chromium.org/ui/p/chromium/builders/ci/linux-ubsan-vptr/19510/overview

Original change's description:
> Enable input protection for window changes
>
> Refer to issue description for more details
>
> Bug: 1160485
> Change-Id: I4e92aac004c66821553280e1e81cc49a3d9c082b
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4051581
> Commit-Queue: Florian Jacky <fjacky@chromium.org>
> Reviewed-by: Keren Zhu <kerenzhu@chromium.org>
> Reviewed-by: Peter Kasting <pkasting@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1085116}

Bug: 1160485
Change-Id: I3e8cd7ebfa3cf1e762fc4ab3d4fafb4f0dc94b2f
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4113308
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Owners-Override: Nidhi Jaju <nidhijaju@chromium.org>
Commit-Queue: Nidhi Jaju <nidhijaju@chromium.org>
Auto-Submit: Nidhi Jaju <nidhijaju@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1085237}

[modify] https://crrev.com/ac826440f3dfd4b852fa6d9612457ae1092c1d01/ui/views/window/dialog_client_view.h
[modify] https://crrev.com/ac826440f3dfd4b852fa6d9612457ae1092c1d01/chrome/browser/ui/views/permissions/permission_prompt_bubble.h
[modify] https://crrev.com/ac826440f3dfd4b852fa6d9612457ae1092c1d01/chrome/browser/ui/views/permissions/chip_controller.h
[modify] https://crrev.com/ac826440f3dfd4b852fa6d9612457ae1092c1d01/ui/views/window/dialog_client_view.cc
[modify] https://crrev.com/ac826440f3dfd4b852fa6d9612457ae1092c1d01/chrome/browser/ui/views/permissions/chip_controller.cc
[modify] https://crrev.com/ac826440f3dfd4b852fa6d9612457ae1092c1d01/chrome/browser/ui/views/permissions/permission_prompt_bubble.cc
[modify] https://crrev.com/ac826440f3dfd4b852fa6d9612457ae1092c1d01/ui/views/window/dialog_delegate.cc
[modify] https://crrev.com/ac826440f3dfd4b852fa6d9612457ae1092c1d01/ui/views/window/dialog_delegate.h


### gi...@appspot.gserviceaccount.com (2022-12-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6e3fe13366e47d7baddbca167c5cdeb87eb063f3

commit 6e3fe13366e47d7baddbca167c5cdeb87eb063f3
Author: Florian Jacky <fjacky@chromium.org>
Date: Wed Dec 21 20:49:47 2022

Reland "Enable input protection for window changes"

This is a reland of commit b491e7324d790f854c8c80f17b21ddf8348a0a1f

The original CL made the erroneous assumption that bubble widgets
are always prompt bubble widgets. An undefined static cast of a
bubble widget thus led to a failure on a UBSan builder.

Original change's description:
> Enable input protection for window changes
>
> Refer to issue description for more details
>
> Bug: 1160485
> Change-Id: I4e92aac004c66821553280e1e81cc49a3d9c082b
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4051581
> Commit-Queue: Florian Jacky <fjacky@chromium.org>
> Reviewed-by: Keren Zhu <kerenzhu@chromium.org>
> Reviewed-by: Peter Kasting <pkasting@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1085116}

Bug: 1160485
Change-Id: I3b023d3d994c1ffdd6b73fb7bda8179c9a842eb8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4116798
Auto-Submit: Florian Jacky <fjacky@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Reviewed-by: Keren Zhu <kerenzhu@chromium.org>
Commit-Queue: Florian Jacky <fjacky@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1086065}

[modify] https://crrev.com/6e3fe13366e47d7baddbca167c5cdeb87eb063f3/ui/views/window/dialog_client_view.h
[modify] https://crrev.com/6e3fe13366e47d7baddbca167c5cdeb87eb063f3/chrome/browser/ui/views/permissions/permission_prompt_bubble.h
[modify] https://crrev.com/6e3fe13366e47d7baddbca167c5cdeb87eb063f3/chrome/browser/ui/views/permissions/chip_controller.h
[modify] https://crrev.com/6e3fe13366e47d7baddbca167c5cdeb87eb063f3/ui/views/window/dialog_client_view.cc
[modify] https://crrev.com/6e3fe13366e47d7baddbca167c5cdeb87eb063f3/chrome/browser/ui/views/permissions/chip_controller.cc
[modify] https://crrev.com/6e3fe13366e47d7baddbca167c5cdeb87eb063f3/chrome/browser/ui/views/permissions/permission_prompt_bubble.cc
[modify] https://crrev.com/6e3fe13366e47d7baddbca167c5cdeb87eb063f3/ui/views/window/dialog_delegate.cc
[modify] https://crrev.com/6e3fe13366e47d7baddbca167c5cdeb87eb063f3/ui/views/window/dialog_delegate.h


### fj...@chromium.org (2022-12-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-22)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-12)

Congratulations, Thomas! The VRP Panel has decided to award you $2,000 for this report. Thank you for your efforts in reporting this issue to us -- nice work! 

### am...@google.com (2023-01-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-06)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### pg...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1160485?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054242)*
