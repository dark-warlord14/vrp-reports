# uaf in content::DesktopCaptureDevice::Core::AllocateAndStart

| Field | Value |
|-------|-------|
| **Issue ID** | [40057057](https://issues.chromium.org/issues/40057057) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>ScreenCapture |
| **Platforms** | Windows |
| **Reporter** | wx...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2021-08-27 |
| **Bounty** | $10,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36

Steps to reproduce the problem:
1.the first step is similar as  https://crbug.com/chromium/1244188
2.1. Apply the attached token.patch (*)
2. $ python ./copy_mojo_js_bindings.py /path/to/chrome/.../out/asan/gen
   $ python -m SimpleHTTPServer
3. Start chrome and visit poc.html with the "--enable-blink-features=MojoJS" (emulates a compromised renderer)
3.when visit poc.html, you should choose the entire screen, and before it reset, you should click the button of "capture", and alt+f4 close the window quickly, I just cause the similar access_violation stack race as https://crbug.com/chromium/1242036, I think it is possible to trigger uaf.

I submit a https://crbug.com/chromium/1242036 before, but this time I use MojoJs, 

What is the expected behavior?

What went wrong?
above all

Did this work before? N/A 

Chrome version: 92.0.4515.159  Channel: stable
OS Version: 10.0

## Attachments

- [access_violation.txt](attachments/access_violation.txt) (text/plain, 15.8 KB)
- deleted (application/octet-stream, 0 B)
- [mojo_test1.html](attachments/mojo_test1.html) (text/plain, 3.8 KB)
- [patch.PNG](attachments/patch.PNG) (image/png, 55.3 KB)

## Timeline

### [Deleted User] (2021-08-27)

[Empty comment from Monorail migration]

### wx...@gmail.com (2021-08-27)

of cause, I try many times, just win several times in a race condition.

### wx...@gmail.com (2021-08-28)

I can trigger the access_violation.txt every time that use this html.
```
out\asan\chrome.exe --enable-blink-features=MojoJS --no-sandbox http://127.0.0.1:8000/mojo_test1.html   http://127.0.0.1:8000/mojo_test1.html
```
you should choose to capture the entire screen and  click the button of "share".

### dr...@chromium.org (2021-08-31)

It looks like you talked about a token.patch, but didn't attach it. Can you share your patch?

### wx...@gmail.com (2021-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-31)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dc...@chromium.org (2021-09-06)

The attached stack trace is a null pointer deref. I'm not familiar enough with the IPC systems involved to understand if triggering an actual use-after-free is something a renderer can directly trigger.

To avoid bifurcating the discussion too much, I'm going to dupe the (older, definitely use-after-free) https://crbug.com/chromium/1242036 into this one since we're still trying to understand if this is reachable via a renderer.

There is 100% a use-after-free bug in this code:

1. We post a task to a helper thread here with a base::Unretained pointer to content::DesktopCaptureDevice::Core here: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/media/capture/desktop_capture_device.cc;l=593;drc=97d6e9c16991a75919ef817a700df1884bf022e1
2. We attempt to always delete the Core object on `thread_`: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/media/capture/desktop_capture_device.cc;l=598;drc=97d6e9c16991a75919ef817a700df1884bf022e1
3. However, we don't delete the Core object on `thread_` if `DesktopCaptureDevice` itself is destroyed and we haven't called `StopAndDeAllocate`.

I'm guessing that the desktop capture code has some internal invariants that are supposed to protect against deleting `DesktopCaptureDevice` without stopping it first—except there is one edge case where it can happen. Looking as the use-after-free stacks attached to https://crbug.com/chromium/1242036, they happen because of this line from https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/media/in_process_video_capture_device_launcher.cc;l=421;drc=5bc57681793ef5008225cf26900492f62f640dd0:

  std::move(result_callback).Run(std::move(video_capture_device));

The problem is that `result_callback` is a callback created by `base::BindPostTask()`. Internally, BindPostTask binds the arguments passed to `Run()` to a new callback and attempts to `PostTask()` the new callback to the correct sequence. However, if the `PostTask()` fails... we delete the newly-created callback (which we passed ownership of `video_capture_device` to by virtue of binding it!). This deletes `video_capture_device`, and now `content::DesktopCaptureDevice::Core` has been racily destroyed on the wrong thread. Oops.

joedow@, I'm assigning to you to help us understand if this is something a compromised renderer could trigger *without* requiring user interaction. I'm not familiar enough with how the desktop capture flow is started/stopped to definitively say.

I'm not sure where the right fix is at this point. We've had issues in the past with PostTask() failing, and I don't think we definitively have a right way of handling these sort of bugs / preventing them :( CCing danakj/gab/kylechar for thoughts...

[Monorail components: Internals>Media>SurfaceCapture]

### dc...@chromium.org (2021-09-06)

(sorry, somehow left kylechar off the CC list when updating the bug)

### dc...@chromium.org (2021-09-06)

[Empty comment from Monorail migration]

### ad...@google.com (2021-09-07)

Security sheriff here. Given https://crbug.com/chromium/1244205#c7 saying that there's a real UaF here, I'm going to mark this as Security_Severity High (browser UaF reachable from a compromised renderer). If this requires unlikely user interaction, we can downgrade this to Medium.

### [Deleted User] (2021-09-07)

[Empty comment from Monorail migration]

### mf...@chromium.org (2021-09-07)

The desktop capturer should not be able to be started without some kind of user gesture and consent flow (whether through a permissions dialog, or through the system UI in the case of ChromeOS).  Those are required before the renderer can get an unguessable token to pass with the IPC to start capture.

It looks like the PoC is passing a dummy token, but still requires the user to go through the screen share permissions dialog.





[Monorail components: -Internals>Media>SurfaceCapture Internals>Media>ScreenCapture]

### ad...@google.com (2021-09-08)

[Empty comment from Monorail migration]

### ad...@google.com (2021-09-08)

[Empty comment from Monorail migration]

### jo...@chromium.org (2021-09-08)

I can help take a look but I'm not very familiar with this code (I was added to the OWNERs file as I am an OWNER for WebRTC desktop capture).  It sounds like Mark has a much better understanding of the end-to-end use cases but I can certainly try to repro and work on a fix (unless there is someone who is more familiar who wants to take a look).

### [Deleted User] (2021-09-08)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-08)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### jo...@chromium.org (2021-09-13)

I got an ASAN build running today and I'm able to reproduce the crash.  I'll look into the potential fixes.  Based on Mark's reply it sounds like there isn't a way to trigger this w/o a user gesture so I'm not sure if that means lowering the priority and release versions we would want to merge to or not (I'll let the security folks update those as needed).

### jo...@chromium.org (2021-09-18)

After working on this for a bit, it looks like I'm not able to reproduce the original UAF.

For the ASAN errors I saw earlier this week, I was hitting a few DCHECKS and those caused ASAN to produce stacks which looked very similar to the uaf txt files attached to the bug (same method.  The issue pointed out in https://crbug.com/chromium/1244205#c7 still seems legit, I'm having a hard time reproducing it (note that I commented out a handful of DCHECKs that were firing which warned about the params being passed in via the repro html). 

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-29)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### ad...@google.com (2021-12-06)

Re https://crbug.com/chromium/1244205#c19 and the severity discussions, here's how this would work:
* Browser UaF = critical priority
* We downgraded this to High because it requires a compromised renderer
* We would downgrade it further if it required UNLIKELY user interaction (e.g. clicking a button six times while whistling the tune to the Star-Spangled Banner). It sounds like https://crbug.com/chromium/1244205#c12 suggests that this is reproducible with the normal user interaction, so High is correct.

joedow@ thanks a lot for looking into this. Who do you think would be the best owner? From https://crbug.com/chromium/1244205#c15 it sounds like there might be a better one?

### jo...@chromium.org (2021-12-06)

alcooper@ and mfoltz@ have taken ownership of desktop capture since that comment was made so I'll assign it over to Alex.

### [Deleted User] (2021-12-07)

alcooper: Uh oh! This issue still open and hasn't been updated in the last 101 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2021-12-13)

Starting to look into this now that I'm back; dcheng/kylechar/gab/danakj, were there any thoughts you all had about the post task failing? It seems like that destruction path is what's triggering this UAF?

I'm going to guess that despite the comment that the Stop/Join call should be quick, that we can't simply try to call StopAndDeAllocate in the CaptureDevice destructor if it still has a core_ object? 

However, I'd also guess that if the PostTask there failed, we likely wouldn't be in a good state to try to post an additional task/stop the thread....

The core object already seems to have a weak pointer factory, I believe it's safe to create one of those on any thread as long as they are only checked on a single thread (the one the task is posted to?); but I'm unsure if there's any weirdness with that invalidation if it is destroyed on the wrong thread...

### al...@chromium.org (2021-12-14)

It's worth noting that the token patch requested is also applied to the browser process. Can you describe the purpose of applying this patch and why it's necessary to cause this repro?

I've also tried with an ASAN build and am unable to reproduce this currently, as soon as I click "share", I hit: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/media/capture/desktop_capture_device.cc;drc=d7044ac79851029fa1698731d9ce5c251a5939be;l=244, which indicates that we've passed the race spoken of in both https://crbug.com/chromium/1244205#c0 and https://crbug.com/chromium/1244205#c7. (Note that I hit the dcheck even if I modify the VideoCaptureParams in the poc.html from https://crbug.com/chromium/1244205#c3 to pass non-zero values). If I comment out both of those DCHECKs, I hit some more related to them later in the code, but from the stacks mentioned and the theory in https://crbug.com/chromium/1244205#c7, if I'm hitting those DCHECKs, I'm not hitting this UAF issue.

If I add a delay before the AllocateAndStart task is run (by changing it to a PostDelayedTask), I hit: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/media/video_capture_controller.cc;drc=0e45c020c43b1a9f6d2870ff7f92b30a2f03a458;l=474

If I comment *that* out, things resolve and the tab just seems to close cleanly, without further interaction from me. (Though the task delay is at 1 second, at 100ms the task still seems to fire before the window close can happen).

From my knowledge of this code, nothing that's triggering the UAF *should* be Windows specific, though I am testing on Linux right now, and the reporter filed on Windows.

It does look like the poc from https://crbug.com/chromium/1244205#c0 was deleted and a new one uploaded with https://crbug.com/chromium/1244205#c3, so I assume that forcing the window to close should no longer be necessary.

It sounds as though this is also similar to https://crbug.com/chromium/1244188, which is still tagged as a security issue and I cannot access it. If someone could CC me on that one, it may give me more insight on what is going on here or if this issue was perhaps fixed.

### ky...@chromium.org (2021-12-14)

> Starting to look into this now that I'm back; dcheng/kylechar/gab/danakj, were there any thoughts you all had about the post task failing? It seems like that destruction path is what's triggering this UAF?

In general binding an object that has invariants about when/where it must be destroyed in a callback and posting that callback to another thread is problematic. If a PostTask() fails the callback (and any bound objects) will be immediately destroyed, possibly at an unexpected time or on the wrong thread. The callback being run at [1] binds |video_capture_device| into a OnceClosure and then PostTasks it.

So it looks like:
1.  InProcessVideoCaptureDeviceLauncher::LaunchDeviceAsync() runs on one thread. It creates |after_start_capture_callback| which will PostTask back to the current thread [2]. A task is posted to run DoStartDesktopCaptureOnDeviceThread() on another thread [3] which includes |after_start_capture_callback| as |result_callback|.
2. InProcessVideoCaptureDeviceLauncher::DoStartDesktopCaptureOnDeviceThread() runs on the other thread. |result_callback| is run with |video_capture_device|. This tries to PostTask back to the original thread.
3. The PostTask fails and |video_capture_device| is destroyed in the wrong place.

I don't know enough about media stack to understand why the post task fails.

> It's worth noting that the token patch requested is also applied to the browser process. 

Is https://bugs.chromium.org/p/chromium/issues/attachmentText?aid=461682 the patch? I'm also interested in why this is needed. That is forcing a collision between base::UnguessableTokens which doesn't seem like it should ever happen. 

[1] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/media/in_process_video_capture_device_launcher.cc;l=434;drc=f49f9c9697b11929d0747fc821e2d06ecc13be76
[2] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/media/in_process_video_capture_device_launcher.cc;l=131;drc=05f2eb78e8ed73d7f1b5ae51acc267d167356c02
[3] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/media/in_process_video_capture_device_launcher.cc;l=230-237;drc=05f2eb78e8ed73d7f1b5ae51acc267d167356c02

### [Deleted User] (2021-12-28)

alcooper: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2022-01-10)

I understand this code a little bit better now. DesktopCaptureDevice spins up a new thread, which it holds. It then has a child object, core, which lives on that thread. Calls to DesktopCaptureDevice post tasks to that thread, with a base::Unretained (presuming this is safe under the assumption that we control the lifetime). Interestingly the core child object *does* have a Weak Pointer Factory, but it is currently unused. 

Looking at the class declaration, it looks like the core object is declared after the thread object, which means that when we go to destroy the object, the Core object gets destroyed and *then* the thread object (which should be calling stop in it's destructor IIUC), is destroyed. However, with base::Unretained, this could cause a race wherein the thread hasn't been destroyed but the core object has, which I suspect could cause this issue.

There's a DCHECK in the destructor that StopAndDeAllocate was called, which a situation like this probably wouldn't fix. We've got a couple of options here, none of which are mutually exclusive:

1) Switch base::Unretained to use the WeakPtr for the Core object, WeakPtr's aren't used on Any other thread, so creating them for the sole purpose of binding to a single task runner should be safe.
2) Switch the declared order of Core/Thread, so that the Thread is the first DesktopCaptureDevice member destroyed
3) Call StopAndDeAllocate in the Destructor.

I'm disinclined to do #3, as I think that may hide a pattern where a legitimate consumer is holding it wrong; though the DCHECK makes it not apply to production builds, and likely a CHECK could trigger an edge case like this one, where the object hasn't *actually* been started, but the start is pending/queued.

### al...@chromium.org (2022-01-10)

Sorry, the options are *not* mutually exclusive.

### da...@chromium.org (2022-01-11)

I agree 2 is better than 3, and should be done.

It sounds like 1 isn't needed then, and the lifetimes here are well encapsulated inside a class, so I would personally fix this without adding weakptrs unless there's more complexity with and/or visibility of the `core` than what I understand from the above.

### ky...@chromium.org (2022-01-12)

I agree that #2 is a good change to make regardless.

Just curious if DesktopCaptureDevice::core is still (potentially) destroyed on the wrong thread with #2 though? I guess since thread |core| is normally accessed on would have shutdown already there is less risk of race accessing it and no risk of UAF from access by DesktopCaptureDevice::thread but wouldn't this DCHECK [1] fail?

[1] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/media/capture/desktop_capture_device.cc;l=233;drc=054e08864177603f17edbc111db7ebc8586906bd

### al...@chromium.org (2022-01-12)

Mark brought that up as well, and proposed keeping the destruction order as-is, but with Core being created with a base::OnTaskRunnerDeleter; but I'm inclined to agree that this should be a non-issue, as if it's thread is deleted on the same thread (via joining during Stop), then that effectively becomes the new "safe" thread for deleting the object.

https://chromium-review.googlesource.com/c/chromium/src/+/3379089/comment/66334758_c53b9b5d/

Obviously if anyone feels strongly I'm happy to defer.

### al...@chromium.org (2022-01-12)

Sorry, missed kyle's part about the DCHECK; technically the DCHECK(!core_) in the destructor would fail first; and since it's a DCHECK it shouldn't be triggered on a production build; but on a developer/debug build this is a signal that a dev is almost certainly holding it wrong (as I've been unable to make this issue repro otherwise).

After talking with Mark, I don't think he's opposed (and indeed we may want to look at changing the device contract if we can), to calling StopAndDeAllocate in the destructor, if we feel that's better than keeping the dcheck.

### gi...@appspot.gserviceaccount.com (2022-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5853e2baadfb4d13a6c62b7187d5cf12b3ce9f18

commit 5853e2baadfb4d13a6c62b7187d5cf12b3ce9f18
Author: Alexander Cooper <alcooper@chromium.org>
Date: Thu Jan 13 19:47:07 2022

Ensure lifetime of DesktopCaptureDevice::Core member

Due to the destruction order of the DesktopCaptureDevice::Core member
and it's owning thread, combined with the use of Base::Unretained, it is
possible for the Core object (which was passed to the thread with an
unretained), to be destroyed before the thread. This can result, in some
cases, with the thread attempting to still process the queued task, but
with a now-destroyed object. Two changes are made to ensure that this
cannot happen:

1) The currently unused WeakPtrFactory on the Core object is used to
   ensure that any tasks attempting to be run after the core object is
   destroyed fail.
2) The ordering of the members is flipped so that if a case *is* hit
   where the DesktopCaptureDevice is destroyed without a
   StopAndDeallocate call, that the thread is stopped first, further
   guaranteeing that no DesktopCaptureDevice members are accessed by it
   during the device's destruction.

Fixed: 1244205
Change-Id: I9837e722a2fe0327d68662c2d297eb1f377d3631
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3379089
Reviewed-by: Mark Foltz <mfoltz@chromium.org>
Commit-Queue: Alexander Cooper <alcooper@chromium.org>
Cr-Commit-Position: refs/heads/main@{#958760}

[modify] https://crrev.com/5853e2baadfb4d13a6c62b7187d5cf12b3ce9f18/content/browser/media/capture/desktop_capture_device.cc
[modify] https://crrev.com/5853e2baadfb4d13a6c62b7187d5cf12b3ce9f18/content/browser/media/capture/desktop_capture_device.h


### [Deleted User] (2022-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-14)

Requesting merge to extended stable M96 because latest trunk commit (958760) appears to be after extended stable branch point (929512).

Requesting merge to stable M97 because latest trunk commit (958760) appears to be after stable branch point (938553).

Requesting merge to beta M98 because latest trunk commit (958760) appears to be after beta branch point (950365).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-14)

Merge review required: M98 is already shipping to beta.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-14)

Merge review required: M97 is already shipping to stable.

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
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-14)

Merge review required: M96 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-01-18)

insufficient canary coverage to approve merges, will circle back later this week for merge review/approval 

### am...@chromium.org (2022-01-21)

merge approved for M98, please merge to branch 4758 ASAP/ NLT 11am PST Tuesday, 25 January so this fix can be included in the stable cut for M98 -- thank you 

### am...@chromium.org (2022-01-21)

missed these labels in my earlier review

### gi...@appspot.gserviceaccount.com (2022-01-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/769587ca2c8b060dad88264e16c0a42442041411

commit 769587ca2c8b060dad88264e16c0a42442041411
Author: Alexander Cooper <alcooper@chromium.org>
Date: Fri Jan 21 23:19:46 2022

Ensure lifetime of DesktopCaptureDevice::Core member

Due to the destruction order of the DesktopCaptureDevice::Core member
and it's owning thread, combined with the use of Base::Unretained, it is
possible for the Core object (which was passed to the thread with an
unretained), to be destroyed before the thread. This can result, in some
cases, with the thread attempting to still process the queued task, but
with a now-destroyed object. Two changes are made to ensure that this
cannot happen:

1) The currently unused WeakPtrFactory on the Core object is used to
   ensure that any tasks attempting to be run after the core object is
   destroyed fail.
2) The ordering of the members is flipped so that if a case *is* hit
   where the DesktopCaptureDevice is destroyed without a
   StopAndDeallocate call, that the thread is stopped first, further
   guaranteeing that no DesktopCaptureDevice members are accessed by it
   during the device's destruction.

(cherry picked from commit 5853e2baadfb4d13a6c62b7187d5cf12b3ce9f18)

Fixed: 1244205
Change-Id: I9837e722a2fe0327d68662c2d297eb1f377d3631
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3379089
Reviewed-by: Mark Foltz <mfoltz@chromium.org>
Commit-Queue: Alexander Cooper <alcooper@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#958760}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3407787
Auto-Submit: Alexander Cooper <alcooper@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4758@{#816}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/769587ca2c8b060dad88264e16c0a42442041411/content/browser/media/capture/desktop_capture_device.cc
[modify] https://crrev.com/769587ca2c8b060dad88264e16c0a42442041411/content/browser/media/capture/desktop_capture_device.h


### am...@chromium.org (2022-02-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### wx...@gmail.com (2022-02-17)

Oh, thank you. Hope to see you in my next bug.

### am...@google.com (2022-02-18)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-21)

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

This issue was migrated from crbug.com/chromium/1244205?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1242036]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-28)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/chrome-blintz-user-guide

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057057)*
