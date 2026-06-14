# AddressSanitizer: heap-use-after-free on ScreenCaptureKitDeviceMac::ResetStreamTo

| Field | Value |
|-------|-------|
| **Issue ID** | [346898524](https://issues.chromium.org/issues/346898524) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>ScreenCapture |
| **Platforms** | Mac |
| **Chrome Version** | 126.0.0.0 |
| **Reporter** | li...@gmail.com |
| **Assignee** | kr...@chromium.org |
| **Created** | 2024-06-13 |
| **Bounty** | $6,000.00 |

## Description

# Steps to reproduce the problem

1. patch the sleep patch.
2. run the poc.html and share.
3. stop share then uaf

# Problem Description

0. As with the issue I reported earlier, there is a block function in `ResetStreamTo`, and `complexHandler` will execute tasks completely asynchronously for Macos. Therefore, if the `ScreenCaptureKitDeviceMac` class is destroyed while this block function is running, it will cause UAF.

```
 void ResetStreamTo(SCWindow* window) override {
   DCHECK(device_task_runner_->RunsTasksInCurrentSequence());

   if (!window || is_resetting_) {
     client()->OnError(
         media::VideoCaptureError::kScreenCaptureKitResetStreamError,
         FROM_HERE, "Error on ResetStreamTo.");
     return;
   }

   is_resetting_ = true;
   SCContentFilter* filter =
       [[SCContentFilter alloc] initWithDesktopIndependentWindow:window];

   [stream_ updateContentFilter:filter
              completionHandler:^(NSError* _Nullable error) { 
                is_resetting_ = false;    ///uaf
                if (error) {
                  client()->OnError(
                      media::VideoCaptureError::kScreenCaptureKitStreamError,
                      FROM_HERE,
                      "Error on updateContentFilter (fullscreen window).");
                }
              }];
 }

```

1. When you click to stop screen sharing ,it will call StopAndReleaseDeviceOnDeviceThread,then it will release ScreenCaptureKitDeviceMac ,see asan.log
2. <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/media/capture/screen_capture_kit_device_mac.mm;l=428?q=screen_capture_kit_device_mac.mm&ss=chromium%2Fchromium%2Fsrc>
3. <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/media/in_process_launched_video_capture_device.cc;l=29?q=StopAndReleaseDeviceOnDeviceThread&ss=chromium%2Fchromium%2Fsrc>

bitset: <https://source.chromium.org/chromium/chromium/src/+/f6eb52423e79e4ebd07a93da248c4c4a3d79f22e>

fix : will be update soon.

patch to sleep : will be update soon.

notice : it not protected by miracle.

!!! i will reduce my poc and update it soon. if you are confirm it, please fix it asap.!!!

# Summary

AddressSanitizer: heap-use-after-free on ScreenCaptureKitDeviceMac::ResetStreamTo

# Custom Questions

#### Type of crash:

browser

#### Crash state:

see asan.log

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 33.2 KB)
- [poc2.html](attachments/poc2.html) (text/html, 551 B)
- [sleep.diff](attachments/sleep.diff) (text/x-diff, 628 B)
- [uaf2-asan.log](attachments/uaf2-asan.log) (text/plain, 33.4 KB)

## Timeline

### li...@gmail.com (2024-06-13)

Then it is important to note that not all block functions are asynchronous, only handlers such as completedhandler are completely asynchronous.

### pg...@google.com (2024-06-13)

Thank you for the report!

Adding to needs-feedback while waiting for the patch and poc to be uploaded

### li...@gmail.com (2024-06-15)

OKay, finished!

repro:

1. lanuch chrome with poc2.html
2. then choice the window for keynote or Microsoft PowerPoint etc. then start slideshow.
3. then stop the share screen ,wait for uaf.

### pe...@google.com (2024-06-15)

Thank you for providing more feedback. Adding the requester to the CC list.

### li...@gmail.com (2024-06-15)

fix suggestions:
[1]. <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/media/capture/screen_capture_kit_device_mac.mm;l=280>

```
 void OnStreamSample(gfx::ScopedInUseIOSurface io_surface,
                      std::optional<gfx::Size> content_size,
                      std::optional<gfx::Rect> visible_rect) {
    DCHECK(device_task_runner_->RunsTasksInCurrentSequence());

[...]
          [stream_
              updateConfiguration:config
                completionHandler:^(NSError* _Nullable error) {
                  if (error) {
                    client()->OnError( //<--
                        media::VideoCaptureError::kScreenCaptureKitStreamError,
                        FROM_HERE, "Error on updateConfiguration");
                  }
                }];
[...]


```

[2]. <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/media/capture/screen_capture_kit_device_mac.mm;l=428>

```
  void ResetStreamTo(SCWindow* window) override {
    DCHECK(device_task_runner_->RunsTasksInCurrentSequence());
[...]
   [stream_ updateContentFilter:filter
               completionHandler:^(NSError* _Nullable error) {
                 is_resetting_ = false; // <-- 
                 if (error) {
                   client()->OnError( // <--
                       media::VideoCaptureError::kScreenCaptureKitStreamError,
                       FROM_HERE,
                       "Error on updateContentFilter (fullscreen window).");
                 }
               }];
[...]

```

Don't use member variables, in the place where `<--` point to.

### li...@gmail.com (2024-06-16)

deleted

### li...@gmail.com (2024-06-16)

Update bitset:

bug in OnStreamSample <https://source.chromium.org/chromium/chromium/src/+/7196a42b42ce13857777ccbefe9a53a54b1cf856>

bug in ResetStreamTo
<https://source.chromium.org/chromium/chromium/src/+/f6eb52423e79e4ebd07a93da248c4c4a3d79f22e>

overall ,the owner is @kron

### li...@gmail.com (2024-06-17)

One of the two places I provide POC is to trigger `ResetStreamTo`, and the other `OnStreamSample` trigger conditions will be less than ResetStreamTo, because it only needs to share any window, and then use JS `onactive hook` to close the sharing.

### am...@chromium.org (2024-06-18)

assigning to kron@ based on commit on 18 June

### am...@chromium.org (2024-06-18)

This looks like this issue has been around for some time, but setting foundin to 126 since that is current Stable / Extended Stable.

This is not protected by BRP, but there is a fair amount of user interaction required. Setting conservatively as high severity.

### kr...@google.com (2024-06-18)

I have a fix in review, <https://chromium-review.googlesource.com/c/chromium/src/+/5639016>

### li...@gmail.com (2024-06-19)

RE #11:
some user interaction can be replace by js code, so main of it is click window to share [1 step]. And this is probably very easy to convince the people to click it in the real world? for example, when meeting.

### kr...@google.com (2024-06-19)

There two are separate issues.

The potential UAF in `ResetStreamTo()` requires the user to share a window from a supported presentation software (PowerPoint, Keynote, OpenOffice) and click the Start slide show.

The code that is affected in `OnStreamSample()` is only executed if the user shares a window that is resized while sharing and there's an error. I haven't seen any errors occur during the resize operation.

[limmmmmeeee@gmail.com](mailto:limmmmmeeee@gmail.com) Have you been able to trigger this without the sleep() command?

### pe...@google.com (2024-06-19)

Setting milestone because of s0/s1 severity.

### ap...@google.com (2024-06-19)

Project: chromium/src
Branch: main

commit 38e4483e47f99a565221629e0a5446166193cb97
Author: Johannes Kron <kron@chromium.org>
Date:   Wed Jun 19 20:59:48 2024

    [SCK] Use BindPostTask() + weak pointer in callback handler
    
    The callback handler incorrectly accessed member objects directly which may
    cause UAF. Avoid this by using BindPostTask() together with a weak pointer.
    
    Fixed: 346898524
    Change-Id: I9d03d6decfd0212af88d3d0d8d70f83f1081d2e3
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5639016
    Reviewed-by: Avi Drissman <avi@chromium.org>
    Reviewed-by: Mark Foltz <mfoltz@chromium.org>
    Commit-Queue: Johannes Kron <kron@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1317142}

M       content/browser/media/capture/screen_capture_kit_device_mac.mm

https://chromium-review.googlesource.com/5639016


### li...@gmail.com (2024-06-20)

RE #14:
Hi kron. I'm not very familiar with this module. I don't know how to use media and its related modules to monitor and implement it, so I haven't tried it yet. :)

### pe...@google.com (2024-06-20)

Requesting merge to stable (M126) because latest trunk commit (1317142) appears to be after stable branch point (1300313).
Requesting merge to beta (M127) because latest trunk commit (1317142) appears to be after beta branch point (1313161).
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### li...@gmail.com (2024-06-20)

Hi,please update the credit to : lime(@limeSec\_) and fmyy(@binary\_fmyy) From TIANGONG Team of Legendsec at QI-ANXIN Group, thanks. :)

### pe...@google.com (2024-06-20)

Merge review required: M127 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), alonbajayo (ChromeOS), danielyip (Desktop)

### pe...@google.com (2024-06-20)

Merge review required: M126 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), srinivassista (Desktop)

### kr...@google.com (2024-06-24)

Answers to review questions in #20 and #21:

1. This is a security fix for a potential Use-after-free bug.
2. The CL to merge is <https://chromium-review.googlesource.com/c/chromium/src/+/5639016>
3. The change has been tested on Canary.
4. It's not a new feature, but it can be disabled using a Finch flag.
5. not applicable.
6. No manual verification is needed.

Additional questions in #18:

3. There are no known stability risks with the fix.
4. There are no known compatibility risks with the fix.

### am...@chromium.org (2024-06-25)

merges approved for <https://crrev.com/c/5639016> -- please merge this fix to M126 Stable (branch 6478) and M127 Beta (branch 6533) at soonest;
please merge to beta by EOD tomorrow (25 June) so this fix can be included in the next M127 Beta

M126 Stable has already been cut and shipped this week and next M126 Stable will go out after the upcoming release freeze

### ap...@google.com (2024-06-25)

Project: chromium/src
Branch: refs/branch-heads/6533

commit b0496edbc82c68c2b057ac9c04a142ee0ce5c748
Author: Johannes Kron <kron@chromium.org>
Date:   Tue Jun 25 17:39:55 2024

    [M127][SCK] Use BindPostTask() + weak pointer in callback handler
    
    The callback handler incorrectly accessed member objects directly which may
    cause UAF. Avoid this by using BindPostTask() together with a weak pointer.
    
    (cherry picked from commit 38e4483e47f99a565221629e0a5446166193cb97)
    
    Fixed: 346898524
    Change-Id: I9d03d6decfd0212af88d3d0d8d70f83f1081d2e3
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5639016
    Reviewed-by: Avi Drissman <avi@chromium.org>
    Reviewed-by: Mark Foltz <mfoltz@chromium.org>
    Commit-Queue: Johannes Kron <kron@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1317142}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5645201
    Auto-Submit: Johannes Kron <kron@chromium.org>
    Commit-Queue: Mark Foltz <mfoltz@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6533@{#672}
    Cr-Branched-From: 7e0b87ec6b8cb5cb2969e1479fc25776e582721d-refs/heads/main@{#1313161}

M       content/browser/media/capture/screen_capture_kit_device_mac.mm

https://chromium-review.googlesource.com/5645201


### ap...@google.com (2024-06-25)

Project: chromium/src
Branch: refs/branch-heads/6478

commit cfe4fef3f6e66b11ae2a946bd70c6559d83a26a7
Author: Johannes Kron <kron@chromium.org>
Date:   Tue Jun 25 21:43:16 2024

    [M126][SCK] Use BindPostTask() + weak pointer in callback handler
    
    The callback handler incorrectly accessed member objects directly which may
    cause UAF. Avoid this by using BindPostTask() together with a weak pointer.
    
    (cherry picked from commit 38e4483e47f99a565221629e0a5446166193cb97)
    
    Fixed: 346898524
    Change-Id: I9d03d6decfd0212af88d3d0d8d70f83f1081d2e3
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5639016
    Reviewed-by: Avi Drissman <avi@chromium.org>
    Reviewed-by: Mark Foltz <mfoltz@chromium.org>
    Commit-Queue: Johannes Kron <kron@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1317142}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5652684
    Auto-Submit: Johannes Kron <kron@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6478@{#1633}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       content/browser/media/capture/screen_capture_kit_device_mac.mm

https://chromium-review.googlesource.com/5652684


### sp...@google.com (2024-06-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $6000.00 for this report.

Rationale for this decision:
$5,000 for report of mildly mitigated memory corruption in a sandboxed process + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-27)

Congratulations on another one lime and fmyy -- thank you for your efforts and reporting this issue to us! 

### li...@gmail.com (2024-06-27)

Hi amy, I think this vulnerability belongs to the category "Sandbox escape / Memory corruption in a non-sandboxed process" rather than the category "Memory Corruption in a sandboxed process", because, I can breakpoint in the browser process, and then this also crashes in the browser process so can you take a look?

### am...@chromium.org (2024-06-27)

Apologies -- that was a typo. This is the correct reward amount, but the text is incorrect. This was supposed to read "mildly mitigated bug in a non-sandboxed process", which is the $5,000 reward amount falls into that. 


### li...@gmail.com (2024-06-27)

understand, thank you.

### pe...@google.com (2024-09-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/346898524)*
