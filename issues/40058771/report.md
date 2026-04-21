# Security: memory bug on webui tab dragging

| Field | Value |
|-------|-------|
| **Issue ID** | [40058771](https://issues.chromium.org/issues/40058771) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Shell>UIFoundations |
| **Platforms** | ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2022-02-14 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36
Platform: 14388.52.0 (Official Build) stable-channel strongbad

Steps to reproduce the problem:
Tested on real device on stable version.

1. Tablet mode only.
2. Launch two browser and have active desks.
3. Browser one with two tabs on left side with split view (larger), and other one browser on mini view that showing desk templates on the right side.
4. This point is important, hold with right hand in desk templates on right side and then hold one tab from browser with left hand, then drag them.

This repro only work on real device, while tried on linux-chromeOS I couldn't repro.

What is the expected behavior?
Not crash

What went wrong?
copying from https://bugs.chromium.org/p/chromium/issues/detail?id=1292271#c28

Crash from Monday, February 14, 2022 at 6:44:30 PM
Status:	Uploaded
Uploaded Crash Report ID:	62ac2faae9b97fc5
Upload Time:	Monday, February 14, 2022 at 6:56:38 PM

0x0000000008ad03c8	(chrome -unique_ptr.h:287)		ash::DragDropCaptureDelegate::TakeCapture(aura::Window*, aura::Window*, base::RepeatingCallback<void ()>, ui::TransferTouchesBehavior)
0x0000000008ad0d0f	(chrome -drag_drop_controller.cc:225)		ash::DragDropController::StartDragAndDrop(std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, aura::Window*, aura::Window*, gfx::Point const&, int, ui::mojom::DragEventSource)
0x00000000042bcc29	(chrome -web_contents_view_aura.cc:1159)		content::WebContentsViewAura::StartDragging(content::DropData const&, blink::DragOperationsMask, gfx::ImageSkia const&, gfx::Vector2d const&, blink::mojom::DragEventSourceInfo const&, content::RenderWidgetHostImpl*)
0x00000000041faa53	(chrome -render_widget_host_impl.cc:2833)		content::RenderWidgetHostImpl::StartDragging(mojo::StructPtr<blink::mojom::DragData>, blink::DragOperationsMask, SkBitmap const&, gfx::Vector2d const&, mojo::StructPtr<blink::mojom::DragEventSourceInfo>)
0x0000000003bc6007	(chrome -widget.mojom.cc:3052)		blink::mojom::FrameWidgetHostStubDispatch::Accept(blink::mojom::FrameWidgetHost*, mojo::Message*)

Did this work before? N/A 

Chrome version: 98.0.4758.91  Channel: stable
OS Version: 

Based on 0x0000000008ad03c8	(chrome -unique_ptr.h:287), it could be memory bug, so I filled as security bug.

The following crash ids for record.
eea84c44fb3dc0d9
27f9172c934619a1
ff93bfa40d3442a6
8dcf948100a04617

Please cc xdai@chromium.org and yuhengh@chromium.org

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [homestar-firmware-update-error.jpg](attachments/homestar-firmware-update-error.jpg) (image/jpeg, 1.2 MB)

## Timeline

### [Deleted User] (2022-02-14)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-02-14)

The screencast file larger than 10MB, so I share from google drive. Please let me know if you can access the link.

https://drive.google.com/file/d/1NdhYwOC7H7NovJqo2iNr_6gtNDx4Bkm2/view?usp=sharing

### rh...@gmail.com (2022-02-19)

Can you tell  me if the new crash id c82d70fab20a310b is actually same stack trace with previous crash in comment https://crbug.com/chromium/1297209#c0?

### rh...@gmail.com (2022-02-22)

Hi security team,

Can you assess this issue? so can be addressed quickly.  The screencast given in https://crbug.com/chromium/1297209#c2 was tested on real device.

### be...@google.com (2022-02-25)

[Empty comment from Monorail migration]

### be...@google.com (2022-02-25)

[Empty comment from Monorail migration]

[Monorail blocked-on: b/221468148]

### xd...@chromium.org (2022-02-25)

Re https://crbug.com/chromium/1297209#c3 rhezashan@: Yes it's the same crash stack https://crash.corp.google.com/browse?stbtiq=c82d70fab20a310b

As I noted in https://crbug.com/chromium/1292271#c28, this is probably introduced by https://chromium.googlesource.com/chromium/src.git/+/55ab85e8e168e9bbaeab47fa2e27df8bdc41f208. 

Since jonahwilliams@ is no longer in Chrome OS, oshima@, can you help find an owner please? Thanks!

### rh...@gmail.com (2022-02-25)

Thanks for confirming this xdai@

### os...@chromium.org (2022-03-08)

The root cause may be same as crbug.com/1297643. aluh@ can you test this when you fixed 1297643?

### al...@chromium.org (2022-03-09)

Yup, will look at this one as well.

### al...@chromium.org (2022-03-09)

[Empty comment from Monorail migration]

[Monorail components: UI>Shell>UIFoundations]

### ke...@google.com (2022-03-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-10)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rh...@gmail.com (2022-03-22)

Aluh@,

Sorry for asking this, but did you test per https://crbug.com/chromium/1297209#c9 to this issue? 

### al...@chromium.org (2022-03-22)

Thanks for checking in.  I'm in the process of getting a device to repro this.  I'll check if my fix for crbug.com/1297643 fixes this.  I suspect it could be a different root cause though.

### al...@chromium.org (2022-03-25)

@rhezashan, could you let me know what device you tried this on?

### rh...@gmail.com (2022-03-25)

Hi aluh@,

I tested on Lenovo chromebook duet 5 13", keyboard can detach/removed to transform tablet mode. Above issue still can repro.

I also tested on Asus chromebook flip C433, the above issue not repro on Asus/ flip chromebook. Tried the steps on point 4 above in https://crbug.com/chromium/1297209#c0, the dragging is cancelled, if use two fingers.

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### al...@chromium.org (2022-04-13)

Thanks for the info.  I tried this earlier on another detachable device that's also on the strongbad platform, on version 99, but could not repro the issue.  I also get the behavior that using 2 fingers, the dragging is either cancelled or transferred to the other finger.

I'm now getting a Lenovo chromebook duet 5 to see if I can reproduce it there.  I'm not too sure what makes that device different than this one though.

Have you updated your Lenovo to a later version?  If so, could you try reproducing it to see if it's still an issue?

### rh...@gmail.com (2022-04-13)

>>  I tried this earlier on another detachable device that's also on the strongbad platform, on version 99, but could not repro the issue.  I also get the behavior that using 2 fingers, the dragging is either cancelled or transferred to the other finger.

Yes, I tried on Asus Flip and two finger was not working.

>> Have you updated your Lenovo to a later version?  If so, could you try reproducing it to see if it's still an issue?
Yes, I've tested just now and I'm still able for the crash.

https://drive.google.com/file/d/14efGQ4dtHpk4JSHy6McNdAu2N9EjHjJA/view?usp=sharing

### al...@chromium.org (2022-04-14)

Thanks, that's very helpful.  I see the device is at version 100.  I'll try to repro with that.  Btw, did you have any flags turned on?

### al...@chromium.org (2022-04-14)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-04-14)

re: #22

Happy to help. I see no flags turned on but I will send later today or tomorrow for another screencast.

### os...@chromium.org (2022-04-14)

 rhezashan@ what's the latest chrome's version number you could repro this on?

### rh...@gmail.com (2022-04-14)

oshima@,

Tested on 100.0.4896.82 stable version.

### rh...@gmail.com (2022-04-14)

do you want me to test beta /dev version on the device?

### rh...@gmail.com (2022-04-14)

FYI, I filled this issue in https://crbug.com/chromium/1297209#c0 on version 98.0.4758.91 

### al...@chromium.org (2022-04-15)

I tried using 100.0.4896.82 on the Lenovo but still couldn't repro this.  I start dragging the Desk icon on the right, held it down, and start dragging a tab from the left, but the drag on the right side gets cancelled with no crash, while the dragging of the tab on the left is still dragging.

@rhezashan, I noticed that your firmware version is a bit old: 13577.299.  The device I'm testing with is on 13577.403.  This could be why you see the crash but I don't.  Could you manually click on the "Check for updates" button in the About page then reboot to see if it tries to update it?  Make sure it's connected to the internet too.

### rh...@gmail.com (2022-04-15)

Hi,

I updated the device and now its 100.0.4896.93, while on https://crbug.com/chromium/1297209#c21 version 100.0.4896.82. I rebooted 3 times but  firmware still on 13577.299. I think the differ is only minor version, mine 13577.299 while yours 13577.403.
I bought the devices on February 2022 shown on image attached and it's not quite old but I had no clue if amazon sent me old device.

aluh@, do you have suggest how to update firmware? I also wanted to say sorry for this issue and you were bought same device as mine.

### al...@chromium.org (2022-04-15)

I see.  Thanks for trying the steps.  No worries about us getting devices.  We really appreciate all the work you put in to report this, and we want to get to the bottom of it.  I'll ask my teammates about how to update the firmware and get back to you.

### al...@chromium.org (2022-04-15)

@jora, do you know how we can update the firmware?  Seems like both of our devices have old firmware, and we want to see if updating it might resolve this issue.

### rh...@gmail.com (2022-04-16)

@aluh,

can you provide full stack trace from the crash id: 62ac2faae9b97fc5 (copied from https://crbug.com/chromium/1297209#c0).


### [Deleted User] (2022-04-16)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2022-04-19)

[Empty comment from Monorail migration]

### ki...@google.com (2022-04-20)

It seems like this is another victim of go/cros-fw-downdate-postmortem.

Where FW + OS are on mismatched versions due to FW silently rolling back.

You can try and force a FW update (RW portion) by enabling developer mode + `chromeos-firmwareupdater --mode=autoupdate`.
+ reboot to see if the FW rolls back still.

If that's the case, it might be required to wait for a good AU push for strongbad(homestar model).

### al...@chromium.org (2022-04-20)

Does the device need have an official image, or can it be done with a test image?  My device is using a test image from goldeneye, but it's not able to update using the command.

Attached is the output from the firmware update command.

### ki...@google.com (2022-04-20)

You can force the update, but warning as it might brick your DUT unless you know how to reflash using servo/suzyq.

### al...@chromium.org (2022-04-20)

Is there a way to confirm that this is due to go/cros-fw-downdate-postmortem?  Do we just keep waiting?  Or is there something we can do?

### al...@chromium.org (2022-04-20)

I was finally able to reproduce this crash on 100.0.4896.82, yay!  So I'll investigate further.  At least we can probably rule out the firmware as the issue.

### al...@chromium.org (2022-04-26)

It's taking a while to investigate this.  Currently I narrowed it down to this:
When the 2nd finger drag happens, it takes capture and transfers touch events to a placeholder capture window.  In the process, it cancels all other touch events that did not originate from the source window.  But this sometimes ends up cancelling the original drag/capture, which destroys temporary helper objects like the DragDropCaptureDelegate, so when the rest of the capture logic happens, it tries to operate on them and crashes due to dangling pointer.

But this only happens sometimes, so it feels like a race condition.  The difference seems to be that the cancel touch event sometimes ends up canceling the original capture, but sometimes not.  It could be that the cancel touch event propagation is handled differently.  I will investigate into this more.

### al...@chromium.org (2022-04-28)

[Empty comment from Monorail migration]

### al...@chromium.org (2022-05-05)

A fix is currently being reviewed.

### gi...@appspot.gserviceaccount.com (2022-05-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1717b8590d3196d9d0f915d2cc18c36f87d0c18e

commit 1717b8590d3196d9d0f915d2cc18c36f87d0c18e
Author: Addison Luh <aluh@chromium.org>
Date: Thu May 12 18:39:05 2022

Fix crash when dragging two windows in tablet split view.

In tablet mode with split view, if a user touch and holds a window on one side and simultaneously drags a different window on the other side, it causes a race condition where the 2nd drag starts before the first touch and hold's gesture consumer gets cleaned up. This results in the 2nd drag canceling the first touch, which ends up canceling the 2nd drag that's in the process of taking capture and cleaning up the drag drop controller state. This was causing a use-after-free crash.

The fix detects if this or any similar situation happened while the 2nd drag is taking the capture and fail gracefully.

The original bug was dragging between a web ui browser tab on one side and a desks overview mini view on the other. But this bug can happen between any two windows that are on opposing sides of the tablet mode split view.

Bug: 1297209
Change-Id: I1e114079c90ce07a20914100b296804be5c6eb2c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3630844
Reviewed-by: Mitsuru Oshima <oshima@chromium.org>
Commit-Queue: Addison Luh <aluh@chromium.org>
Reviewed-by: Sadrul Chowdhury <sadrul@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1002758}

[modify] https://crrev.com/1717b8590d3196d9d0f915d2cc18c36f87d0c18e/ash/drag_drop/tab_drag_drop_delegate.h
[modify] https://crrev.com/1717b8590d3196d9d0f915d2cc18c36f87d0c18e/ash/drag_drop/toplevel_window_drag_delegate.h
[modify] https://crrev.com/1717b8590d3196d9d0f915d2cc18c36f87d0c18e/ash/drag_drop/drag_drop_capture_delegate_unittest.cc
[modify] https://crrev.com/1717b8590d3196d9d0f915d2cc18c36f87d0c18e/ash/drag_drop/drag_drop_controller.cc
[modify] https://crrev.com/1717b8590d3196d9d0f915d2cc18c36f87d0c18e/ash/drag_drop/drag_drop_controller_unittest.cc
[modify] https://crrev.com/1717b8590d3196d9d0f915d2cc18c36f87d0c18e/ui/events/gestures/gesture_recognizer_impl.cc
[modify] https://crrev.com/1717b8590d3196d9d0f915d2cc18c36f87d0c18e/ash/drag_drop/drag_drop_capture_delegate.cc
[modify] https://crrev.com/1717b8590d3196d9d0f915d2cc18c36f87d0c18e/ash/drag_drop/drag_drop_capture_delegate.h


### al...@chromium.org (2022-05-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-16)

Merge review required: M102 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2022-05-16)

1. This is a stability crash fix and a security fix.
2. crrev.com/c/3630844
3. yes
4. Not a new feature.
5. Will add EngProd representative (dhaddock@) to this bug.
6. The repro steps are in this bug.

### ce...@google.com (2022-05-17)

Merge approved for M102.

### gi...@appspot.gserviceaccount.com (2022-05-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/97030152ecf30fcad4b62e884460f5bf3dd91687

commit 97030152ecf30fcad4b62e884460f5bf3dd91687
Author: Addison Luh <aluh@chromium.org>
Date: Tue May 17 17:26:36 2022

Fix crash when dragging two windows in tablet split view.

In tablet mode with split view, if a user touch and holds a window on one side and simultaneously drags a different window on the other side, it causes a race condition where the 2nd drag starts before the first touch and hold's gesture consumer gets cleaned up. This results in the 2nd drag canceling the first touch, which ends up canceling the 2nd drag that's in the process of taking capture and cleaning up the drag drop controller state. This was causing a use-after-free crash.

The fix detects if this or any similar situation happened while the 2nd drag is taking the capture and fail gracefully.

The original bug was dragging between a web ui browser tab on one side and a desks overview mini view on the other. But this bug can happen between any two windows that are on opposing sides of the tablet mode split view.

(cherry picked from commit 1717b8590d3196d9d0f915d2cc18c36f87d0c18e)

Bug: 1297209,1319707
Change-Id: I1e114079c90ce07a20914100b296804be5c6eb2c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3630844
Reviewed-by: Mitsuru Oshima <oshima@chromium.org>
Commit-Queue: Addison Luh <aluh@chromium.org>
Reviewed-by: Sadrul Chowdhury <sadrul@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1002758}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3651282
Auto-Submit: Addison Luh <aluh@chromium.org>
Reviewed-by: Robert Kroeger <rjkroege@chromium.org>
Commit-Queue: Robert Kroeger <rjkroege@chromium.org>
Cr-Commit-Position: refs/branch-heads/5005@{#811}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/97030152ecf30fcad4b62e884460f5bf3dd91687/ash/drag_drop/tab_drag_drop_delegate.h
[modify] https://crrev.com/97030152ecf30fcad4b62e884460f5bf3dd91687/ash/drag_drop/toplevel_window_drag_delegate.h
[modify] https://crrev.com/97030152ecf30fcad4b62e884460f5bf3dd91687/ash/drag_drop/drag_drop_controller.cc
[modify] https://crrev.com/97030152ecf30fcad4b62e884460f5bf3dd91687/ash/drag_drop/drag_drop_capture_delegate_unittest.cc
[modify] https://crrev.com/97030152ecf30fcad4b62e884460f5bf3dd91687/ash/drag_drop/drag_drop_controller_unittest.cc
[modify] https://crrev.com/97030152ecf30fcad4b62e884460f5bf3dd91687/ui/events/gestures/gesture_recognizer_impl.cc
[modify] https://crrev.com/97030152ecf30fcad4b62e884460f5bf3dd91687/ash/drag_drop/drag_drop_capture_delegate.cc
[modify] https://crrev.com/97030152ecf30fcad4b62e884460f5bf3dd91687/ash/drag_drop/drag_drop_capture_delegate.h


### al...@chromium.org (2022-05-17)

This should now be fixed from M102 onward.

### [Deleted User] (2022-05-17)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-18)

[Empty comment from Monorail migration]

### al...@chromium.org (2022-05-20)

To answer https://crbug.com/chromium/1297209#c51:

1. No
2. I don't think so

### vo...@google.com (2022-05-23)

[Empty comment from Monorail migration]

### vo...@google.com (2022-05-23)

The crash happens in DragDropCaptureDelegate but it was only introduced here https://crrev.com/c/3318357 (M98). So we don't need this fix in M96.

### am...@chromium.org (2022-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-05-25)

Hello Rheza (and devs on this bug), while we were evaluating this issue in the VRP Panel, looking at all the stack traces from the crash reports for this issue, we unfortunately do not see any indication this is a user after free bug and all crash reports indicate this a null pointer deref. 

Rheza, if you can provide any evidence of a uaf bug from this issue we would be happy to reassess for a potential reward. 
Chrome OS devs on this bug, also if you can provide evidence of this being a uaf or other exploitable security bug, we would also appreciate that evidence. 

For now, leaving the security tags on this issue, but will update labeling if no data can be presented to continue handling this issue as a security bug. 

### al...@chromium.org (2022-05-25)

Here's a repro by running my regression test in asan for this bug with the fix removed, which shows that this crash is due to use after free:

```
==47890==ERROR: AddressSanitizer: heap-use-after-free on address 0x6060005798c8 at pc 0x7f404af8b789 bp 0x7ffe70fd6110 sp 0x7ffe70fd6108
READ of size 8 at 0x6060005798c8 thread T0
    #0 0x7f404af8b788 in operator-> buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:284:19
    #1 0x7f404af8b788 in ash::DragDropCaptureDelegate::TakeCapture(aura::Window*, aura::Window*, base::RepeatingCallback<void ()>, ui::TransferTouchesBehavior) ash/drag_drop/drag_drop_capture_delegate.cc:74:3
    #2 0x7f404af8d11b in ash::DragDropController::StartDragAndDrop(std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData>>, aura::Window*, aura::Window*, gfx::Point const&, int, ui::mojom::DragEventSource) ash/drag_drop/drag_drop_controller.cc:212:36
    #3 0x56249c19a337 in ash::(anonymous namespace)::TestDragDropController::StartDragAndDrop(std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData>>, aura::Window*, aura::Window*, gfx::Point const&, int, ui::mojom::DragEventSource) ash/drag_drop/drag_drop_controller_unittest.cc:192:32
    #4 0x56249c15f5a7 in ash::DragDropControllerTest_TabletSplitViewDragTwoBrowserTabs_Test::TestBody() ash/drag_drop/drag_drop_controller_unittest.cc:1685:48
    #5 0x56249f2496a7 in HandleExceptionsInMethodIfSupported<testing::Test, void> third_party/googletest/src/googletest/src/gtest.cc
    #6 0x56249f2496a7 in testing::Test::Run() third_party/googletest/src/googletest/src/gtest.cc:2670:5
    #7 0x56249f24b13b in testing::TestInfo::Run() third_party/googletest/src/googletest/src/gtest.cc:2849:11
    #8 0x56249f24d0ec in testing::TestSuite::Run() third_party/googletest/src/googletest/src/gtest.cc:3008:30
    #9 0x56249f2714e9 in testing::internal::UnitTestImpl::RunAllTests() third_party/googletest/src/googletest/src/gtest.cc:5866:44
    #10 0x56249f270b18 in HandleExceptionsInMethodIfSupported<testing::internal::UnitTestImpl, bool> third_party/googletest/src/googletest/src/gtest.cc
    #11 0x56249f270b18 in testing::UnitTest::Run() third_party/googletest/src/googletest/src/gtest.cc:5440:10
    #12 0x5624a15cf7f8 in RUN_ALL_TESTS third_party/googletest/src/googletest/include/gtest/gtest.h:2284:73
    #13 0x5624a15cf7f8 in base::TestSuite::Run() base/test/test_suite.cc:460:16
    #14 0x5624a15d9254 in base::OnceCallback<int ()>::Run() && base/callback.h:143:12
    #15 0x5624a15d7443 in base::(anonymous namespace)::LaunchUnitTestsInternal(base::OnceCallback<int ()>, unsigned long, int, unsigned long, bool, base::OnceCallback<void ()>) base/test/launcher/unit_test_launcher.cc:177:38
    #16 0x5624a15d709c in base::LaunchUnitTests(int, char**, base::OnceCallback<int ()>, unsigned long) base/test/launcher/unit_test_launcher.cc:268:10
    #17 0x56249d6b8161 in main ash/test/ash_unittests.cc:40:10
    #18 0x7f3ff32ad7fc in __libc_start_main csu/../csu/libc-start.c:332:16

0x6060005798c8 is located 8 bytes inside of 64-byte region [0x6060005798c0,0x606000579900)
freed by thread T0 here:
    #0 0x56249b47821d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x7f404af8c146 in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #2 0x7f404af8c146 in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #3 0x7f404af8c146 in ash::DragDropController::Cleanup() ash/drag_drop/drag_drop_controller.cc:769:27
    #4 0x7f404af93bb7 in ash::DragDropController::DoDragCancel(base::TimeDelta) ash/drag_drop/drag_drop_controller.cc:697:3
    #5 0x56249c19a529 in ash::(anonymous namespace)::TestDragDropController::DoDragCancel(base::TimeDelta) ash/drag_drop/drag_drop_controller_unittest.cc:225:25
    #6 0x7f404af8ea0d in ash::DragDropController::DragCancel() ash/drag_drop/drag_drop_controller.cc:321:3
    #7 0x56249c19a401 in ash::(anonymous namespace)::TestDragDropController::DragCancel() ash/drag_drop/drag_drop_controller_unittest.cc:213:25
    #8 0x7f403a96af35 in ui::EventDispatcher::DispatchEvent(ui::EventHandler*, ui::Event*) ui/events/event_dispatcher.cc:190:12
    #9 0x7f403a96abf0 in ui::EventDispatcher::DispatchEventToEventHandlers(std::__1::vector<ui::EventHandler*, std::__1::allocator<ui::EventHandler*>>*, ui::Event*) ui/events/event_dispatcher.cc:177:7
    #10 0x7f403a969e6f in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:125:3
    #11 0x7f403a969b09 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:83:14
    #12 0x7f403a9698e4 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:55:15
    #13 0x7f403a96e372 in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #14 0x7f403bad6bc9 in aura::WindowEventDispatcher::DispatchSyntheticTouchEvent(ui::TouchEvent*) ui/aura/window_event_dispatcher.cc:632:29
    #15 0x7f403a98ce5d in ui::GestureRecognizerImpl::CancelActiveTouchesImpl(ui::GestureConsumer*) ui/events/gestures/gesture_recognizer_impl.cc:347:13
    #16 0x7f403a98c9c8 in ui::GestureRecognizerImpl::CancelActiveTouchesExceptImpl(ui::GestureConsumer*) ui/events/gestures/gesture_recognizer_impl.cc:333:5
    #17 0x7f403a98d486 in ui::GestureRecognizerImpl::TransferEventsTo(ui::GestureConsumer*, ui::GestureConsumer*, ui::TransferTouchesBehavior) ui/events/gestures/gesture_recognizer_impl.cc:152:3
    #18 0x7f404af8b505 in ash::DragDropCaptureDelegate::TakeCapture(aura::Window*, aura::Window*, base::RepeatingCallback<void ()>, ui::TransferTouchesBehavior) ash/drag_drop/drag_drop_capture_delegate.cc:59:23
    #19 0x7f404af8d11b in ash::DragDropController::StartDragAndDrop(std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData>>, aura::Window*, aura::Window*, gfx::Point const&, int, ui::mojom::DragEventSource) ash/drag_drop/drag_drop_controller.cc:212:36
    #20 0x56249c19a337 in ash::(anonymous namespace)::TestDragDropController::StartDragAndDrop(std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData>>, aura::Window*, aura::Window*, gfx::Point const&, int, ui::mojom::DragEventSource) ash/drag_drop/drag_drop_controller_unittest.cc:192:32
    #21 0x56249c15f5a7 in ash::DragDropControllerTest_TabletSplitViewDragTwoBrowserTabs_Test::TestBody() ash/drag_drop/drag_drop_controller_unittest.cc:1685:48
    #22 0x56249f2496a7 in HandleExceptionsInMethodIfSupported<testing::Test, void> third_party/googletest/src/googletest/src/gtest.cc
    #23 0x56249f2496a7 in testing::Test::Run() third_party/googletest/src/googletest/src/gtest.cc:2670:5
    #24 0x56249f24b13b in testing::TestInfo::Run() third_party/googletest/src/googletest/src/gtest.cc:2849:11
    #25 0x56249f24d0ec in testing::TestSuite::Run() third_party/googletest/src/googletest/src/gtest.cc:3008:30
    #26 0x56249f2714e9 in testing::internal::UnitTestImpl::RunAllTests() third_party/googletest/src/googletest/src/gtest.cc:5866:44
    #27 0x56249f270b18 in HandleExceptionsInMethodIfSupported<testing::internal::UnitTestImpl, bool> third_party/googletest/src/googletest/src/gtest.cc
    #28 0x56249f270b18 in testing::UnitTest::Run() third_party/googletest/src/googletest/src/gtest.cc:5440:10
    #29 0x5624a15cf7f8 in RUN_ALL_TESTS third_party/googletest/src/googletest/include/gtest/gtest.h:2284:73
    #30 0x5624a15cf7f8 in base::TestSuite::Run() base/test/test_suite.cc:460:16
    #31 0x5624a15d9254 in base::OnceCallback<int ()>::Run() && base/callback.h:143:12
    #32 0x5624a15d7443 in base::(anonymous namespace)::LaunchUnitTestsInternal(base::OnceCallback<int ()>, unsigned long, int, unsigned long, bool, base::OnceCallback<void ()>) base/test/launcher/unit_test_launcher.cc:177:38
    #33 0x5624a15d709c in base::LaunchUnitTests(int, char**, base::OnceCallback<int ()>, unsigned long) base/test/launcher/unit_test_launcher.cc:268:10
    #34 0x56249d6b8161 in main ash/test/ash_unittests.cc:40:10

previously allocated by thread T0 here:
    #0 0x56249b4779bd in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x7f404af8cfb0 in make_unique<ash::TabDragDropDelegate, aura::Window *&, aura::Window *&, gfx::Point &> buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:725:28
    #2 0x7f404af8cfb0 in ash::DragDropController::StartDragAndDrop(std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData>>, aura::Window*, aura::Window*, gfx::Point const&, int, ui::mojom::DragEventSource) ash/drag_drop/drag_drop_controller.cc:205:31
    #3 0x56249c19a337 in ash::(anonymous namespace)::TestDragDropController::StartDragAndDrop(std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData>>, aura::Window*, aura::Window*, gfx::Point const&, int, ui::mojom::DragEventSource) ash/drag_drop/drag_drop_controller_unittest.cc:192:32
    #4 0x56249c15f5a7 in ash::DragDropControllerTest_TabletSplitViewDragTwoBrowserTabs_Test::TestBody() ash/drag_drop/drag_drop_controller_unittest.cc:1685:48
    #5 0x56249f2496a7 in HandleExceptionsInMethodIfSupported<testing::Test, void> third_party/googletest/src/googletest/src/gtest.cc
    #6 0x56249f2496a7 in testing::Test::Run() third_party/googletest/src/googletest/src/gtest.cc:2670:5
    #7 0x56249f24b13b in testing::TestInfo::Run() third_party/googletest/src/googletest/src/gtest.cc:2849:11
    #8 0x56249f24d0ec in testing::TestSuite::Run() third_party/googletest/src/googletest/src/gtest.cc:3008:30
    #9 0x56249f2714e9 in testing::internal::UnitTestImpl::RunAllTests() third_party/googletest/src/googletest/src/gtest.cc:5866:44
    #10 0x56249f270b18 in HandleExceptionsInMethodIfSupported<testing::internal::UnitTestImpl, bool> third_party/googletest/src/googletest/src/gtest.cc
    #11 0x56249f270b18 in testing::UnitTest::Run() third_party/googletest/src/googletest/src/gtest.cc:5440:10
    #12 0x5624a15cf7f8 in RUN_ALL_TESTS third_party/googletest/src/googletest/include/gtest/gtest.h:2284:73
    #13 0x5624a15cf7f8 in base::TestSuite::Run() base/test/test_suite.cc:460:16
    #14 0x5624a15d9254 in base::OnceCallback<int ()>::Run() && base/callback.h:143:12
    #15 0x5624a15d7443 in base::(anonymous namespace)::LaunchUnitTestsInternal(base::OnceCallback<int ()>, unsigned long, int, unsigned long, bool, base::OnceCallback<void ()>) base/test/launcher/unit_test_launcher.cc:177:38
    #16 0x5624a15d709c in base::LaunchUnitTests(int, char**, base::OnceCallback<int ()>, unsigned long) base/test/launcher/unit_test_launcher.cc:268:10
    #17 0x56249d6b8161 in main ash/test/ash_unittests.cc:40:10
    #18 0x7f3ff32ad7fc in __libc_start_main csu/../csu/libc-start.c:332:16

SUMMARY: AddressSanitizer: heap-use-after-free buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:284:19 in operator->
```

### am...@chromium.org (2022-05-25)

Hi aluh@, excellent - thanks so much for providing that. We'll definitely consider this in a reassessment of this issue for a potential VRP reward for Rheza. 

Additionally, security labels remain on this issue given that this issue does result in a UAF. 



### rh...@gmail.com (2022-05-25)

aluh@,

Thank you so much for help me providing the stack trace, without your help the reassessment couldn't happen.

amy@,

>>"Rheza, if you can provide any evidence of a uaf bug from this issue we would be happy to reassess for a potential reward. 
Chrome OS devs on this bug, also if you can provide evidence of this being a uaf or other exploitable security bug, we would also appreciate that evidence.

Thank you so much for pointing above, aluh did great job and help me a lot about this issue.

 I'm wishing you both the best!

### am...@chromium.org (2022-06-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-01)

Congratulations, Rheza! The VRP Panel has decided to award you $3,000 for this report (since this issue is fairly mitigated by not being remote exploitable and requiring user gesture). Thank you for your efforts in the reporting this issue to us and working with the devs toward a resolution. 

### rh...@gmail.com (2022-06-02)

Thanks a lot amy@ and aluh@!

### am...@google.com (2022-06-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1297209?no_tracker_redirect=1

[Monorail blocked-on: b/221468148]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058771)*
