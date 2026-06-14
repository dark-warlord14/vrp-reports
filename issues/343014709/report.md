# Segv on unknown address in media::`anonymous namespace'::ConvertVideoFrameToRGBPixelsTask

| Field | Value |
|-------|-------|
| **Issue ID** | [343014709](https://issues.chromium.org/issues/343014709) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>GetUserMedia, Internals>Media>CameraCapture |
| **Platforms** | Windows |
| **Chrome Version** | 127.0.6506.0 |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ah...@google.com |
| **Created** | 2024-05-28 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

1. Run Chromium and enable chrome://flags/#camera-mic-preview
2. Open testcase.html
3. Click "Allow"

# Problem Description

Segv on unknown address in media::`anonymous namespace'::ConvertVideoFrameToRGBPixelsTask

# Summary

Segv on unknown address in media::`anonymous namespace'::ConvertVideoFrameToRGBPixelsTask

# Custom Questions

#### Type of crash:

Browser

#### Crash state:

=================================================================
==18408==ERROR: AddressSanitizer: access-violation on unknown address 0x022c33e32000 (pc 0x7ff9716f6206 bp 0x00e9c09fefb0 sp 0x00e9c09fef20 T24)
==18408==The signal is caused by a READ memory access.
==18408==WARNING: Failed to use and restart external symbolizer!
#0 0x7ff9716f6205 in I422ToARGBRow\_AVX2 C:\b\s\w\ir\cache\builder\src\third\_party\libyuv\source\row\_gcc.cc:3800
#1 0x7ff96e17fd86 in I420ToARGBMatrix C:\b\s\w\ir\cache\builder\src\third\_party\libyuv\source\convert\_argb.cc:146
#2 0x7ff962225527 in media::`anonymous namespace'::ConvertVideoFrameToRGBPixelsTask C:\b\s\w\ir\cache\builder\src\media\renderers\paint_canvas_video_renderer.cc:568 #3 0x7ff9622230fd in media::PaintCanvasVideoRenderer::ConvertVideoFrameToRGBPixels C:\b\s\w\ir\cache\builder\src\media\renderers\paint_canvas_video_renderer.cc:1430 #4 0x7ff9622314ec in media::VideoImageGenerator::GetPixels C:\b\s\w\ir\cache\builder\src\media\renderers\paint_canvas_video_renderer.cc:765 #5 0x7ff96e5d5195 in cc::PaintImage::Decode C:\b\s\w\ir\cache\builder\src\cc\paint\paint_image.cc:227 #6 0x7ff97ad69ab2 in cc::SoftwareImageDecodeCacheUtils::DoDecodeImage C:\b\s\w\ir\cache\builder\src\cc\tiles\software_image_decode_cache_utils.cc:89 #7 0x7ff976130f2a in cc::SoftwareImageDecodeCache::DecodeImageIfNecessary C:\b\s\w\ir\cache\builder\src\cc\tiles\software_image_decode_cache.cc:386 #8 0x7ff976130270 in cc::SoftwareImageDecodeCache::DecodeImageInTask C:\b\s\w\ir\cache\builder\src\cc\tiles\software_image_decode_cache.cc:353 #9 0x7ff97613aa6a in cc::`anonymous namespace'::SoftwareImageDecodeTaskImpl::RunOnWorkerThread C:\b\s\w\ir\cache\builder\src\cc\tiles\software\_image\_decode\_cache.cc:107
#10 0x7ff96e9bc36f in cc::SingleThreadTaskGraphRunner::RunTaskWithLockAcquired C:\b\s\w\ir\cache\builder\src\cc\raster\single\_thread\_task\_graph\_runner.cc:157
#11 0x7ff96e9bbf77 in cc::SingleThreadTaskGraphRunner::Run C:\b\s\w\ir\cache\builder\src\cc\raster\single\_thread\_task\_graph\_runner.cc:121
#12 0x7ff96d467452 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:138
#13 0x7ff6e217170d in asan\_thread\_start C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_win.cpp:147
#14 0x7ffa30ff257c in BaseThreadInitThunk+0x1c (C:\WINDOWS\System32\KERNEL32.DLL+0x18001257c)
#15 0x7ffa328caa47 in RtlUserThreadStart+0x27 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005aa47)

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: access-violation C:\b\s\w\ir\cache\builder\src\third\_party\libyuv\source\row\_gcc.cc:3800 in I422ToARGBRow\_AVX2
Thread T24 created by T0 here:
#0 0x7ff6e2171622 in CreateThread C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_win.cpp:158
#1 0x7ff96d466502 in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:203
#2 0x7ff96d4f125e in base::SimpleThread::StartAsync C:\b\s\w\ir\cache\builder\src\base\threading\simple\_thread.cc:55
#3 0x7ff9688caa1e in content::VizProcessTransportFactory::VizProcessTransportFactory C:\b\s\w\ir\cache\builder\src\content\browser\compositor\viz\_process\_transport\_factory.cc:143
#4 0x7ff966da9ef3 in content::BrowserMainLoop::PostCreateThreadsImpl C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1335
#5 0x7ff966da881e in content::BrowserMainLoop::PostCreateThreads C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:965
#6 0x7ff966db0018 in base::internal::Invoker<base::internal::FunctorTraits<int (content::BrowserMainLoop::\*&&)(),content::BrowserMainLoop *>,base::internal::BindState<1,1,0,int (content::BrowserMainLoop::*)(),base::internal::UnretainedWrapper[content::BrowserMainLoop,base::unretained\_traits::MayNotDangle,0](javascript:void(0);) >,int ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:980
#7 0x7ff968371f48 in content::StartupTaskRunner::RunAllTasksNow C:\b\s\w\ir\cache\builder\src\content\browser\startup\_task\_runner.cc:42
#8 0x7ff966da7bcd in content::BrowserMainLoop::CreateStartupTasks C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:893
#9 0x7ff966db2675 in content::BrowserMainRunnerImpl::Initialize C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:140
#10 0x7ff966da282c in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30
#11 0x7ff96be5adee in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:717
#12 0x7ff96be5e158 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1314
#13 0x7ff96be5da1e in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1166
#14 0x7ff96be591bd in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:332
#15 0x7ff96be59cad in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:345
#16 0x7ff95ecc1601 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:192
#17 0x7ff6e20a43a5 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:181
#18 0x7ff6e20a1db2 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:350
#19 0x7ff6e247e983 in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288
#20 0x7ffa30ff257c in BaseThreadInitThunk+0x1c (C:\WINDOWS\System32\KERNEL32.DLL+0x18001257c)
#21 0x7ffa328caa47 in RtlUserThreadStart+0x27 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005aa47)

==18408==ADDITIONAL INFO

==18408==Note: Please include this section with the ASan report.
Task trace:

==18408==END OF ADDITIONAL INFO
==18408==ABORTING

#### Reporter credit:

Khalil Zhani

# Additional Data

Category: Security   

Chrome Channel: Canary   

Regression: N/A

## Attachments

- [testcase.html](attachments/testcase.html) (text/html, 2.3 KB)
- [screen-capture.mp4](attachments/screen-capture.mp4) (video/mp4, 1.9 MB)
- [asan.log](attachments/asan.log) (text/plain, 5.8 KB)
- [Video_2024_05_30-3.webm](attachments/Video_2024_05_30-3.webm) (video/webm, 9.0 MB)

## Timeline

### li...@chromium.org (2024-05-28)

Hi,

Does your PoC require setting up a local server? I see that the PoC creates RTCPeerConnections.

### ch...@gmail.com (2024-05-28)

No, doesn't require setting up a local server to repro this bug. 

### pe...@google.com (2024-05-28)

Thank you for providing more feedback. Adding the requester to the CC list.

### mp...@google.com (2024-05-29)

I'm unable to reproduce on Chrome Linux with either 127 or Extended Stable 124, are there any other steps or restrictions required to hit this bug?

### ch...@gmail.com (2024-05-30)

I don't think this repro on Chrome Linux. Could you please try to repro on Chrome Windows from local (file:///)?


### pe...@google.com (2024-05-30)

Thank you for providing more feedback. Adding the requester to the CC list.

### ch...@gmail.com (2024-05-30)

Note: Sometimes looks like it can take several tries to repro the crash.

### pe...@google.com (2024-05-30)

The NextAction date has arrived: 2024-05-30 
 To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### aj...@chromium.org (2024-05-30)

On win32-release\_x64\_asan-win32-release\_x64-1308020.zip with the flag enabled I do not see any attempts to ask for Camera permissions.

### mp...@google.com (2024-05-30)

Reporter, can you maybe try bisecting this one? Otherwise it is difficult to move forward here.

### ch...@gmail.com (2024-06-02)

>> On win32-release_x64_asan-win32-release_x64-1308020.zip with the flag enabled I do not see any attempts to ask for Camera permissions.

Did you try on a Windows machine with camera option? my Windows machine has an integrated camera.

### ch...@gmail.com (2024-06-02)

>> Reporter, can you maybe try bisecting this one? Otherwise it is difficult to move forward here.

You are probably looking for a change made after 1293958 (known good), but no later than 1294010 (first known bad).
CHANGELOG URL:
  https://chromium.googlesource.com/chromium/src/+log/dfb101bfa0035e1ea942c96fac32d90379d2d5e3..3fd615ac2d048d60c6648c4ce2ee041242d8a19c


### pe...@google.com (2024-06-02)

Thank you for providing more feedback. Adding the requester to the CC list.

### ke...@chromium.org (2024-06-04)

Thanks for going through that.

I've reproduced the crash on Canary, so I have a crash report: d926a82cf0e14360

Leaving it as Severity 2 as an OOB read. Hotlist Security_Impact-None as an unreleased feature.

This seems likely to be https://chromium.googlesource.com/chromium/src/+/3ed166be0754082da5574d1691a0b93a2e8c6a99, so assigning to ahmedmoussa@. PTAL?

### mf...@chromium.org (2024-06-06)

We are currently rolling out CameraMicPreviews as a 50% dev/canary experiment. Does this justify pausing the rollout?

### da...@chromium.org (2024-06-07)

Another guess on what might be wrong based on info from <https://issues.chromium.org/issues/40811659#comment2>:

You may be tearing down VideoFrameHandler prematurely. At a glance it seems like it's not adding a destruction observer to the frame it's vending out, so if you tear down the handler it may be releasing the frame data:
<https://source.chromium.org/chromium/chromium/src/+/main:components/capture_mode/camera_video_frame_handler.cc;l=212;drc=1bee1dfd3a21ce91179f9ceecaa1dcbc00ff13ef>

### ke...@chromium.org (2024-06-11)

cc'ing amyressler@ to answer the question in comment 16
This is an out-of-bounds read, rated Sev-Medium/S2.

### ap...@google.com (2024-06-11)

Project: chromium/src
Branch: main

commit 9519fb766e1ca2e691ec99f50d6600af5aba6b53
Author: Ahmed Moussa <ahmedmoussa@google.com>
Date:   Tue Jun 11 20:35:40 2024

    [media-preview] Prevent a potential UAF during VideoFrames lifetime
    
    Extend mapping lifetime till the destruction of VideoFrames.
    
    Bug: b:343014709, b:40811659
    Change-Id: I581f90b25c57bd29d5f16ecb6870035d10a4f2f7
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5606664
    Reviewed-by: Ahmed Fakhry <afakhry@chromium.org>
    Commit-Queue: Ahmed Moussa <ahmedmoussa@google.com>
    Cr-Commit-Position: refs/heads/main@{#1313643}

M       components/capture_mode/camera_video_frame_handler.cc

https://chromium-review.googlesource.com/5606664


### am...@chromium.org (2024-06-11)

Since the OT is being rolled out on canary/dev I don't think there any need to pause that.
I am, however, updating the from SI-None to SI-Head, since this issue does impact some users in canary / dev due to OT.

### br...@chromium.org (2024-06-11)

Would the same apply to 1% stable? We do plan to do that during M126 if the canary/dev rollout goes well.

### pe...@google.com (2024-06-12)

Setting milestone because of s2 severity.

### pe...@google.com (2024-06-12)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ah...@google.com (2024-06-12)

The fix has landed in Chrome version >= `128.0.6534.0`.

When you get a chance, please verify.

### ch...@gmail.com (2024-06-13)

I verified on 128.0.6535.0 (Developer Build). Fixed.

### am...@chromium.org (2024-06-13)

re c#21 I'm not sure I'm following that 1% Stable rollout would occur during M126 since M126 is current Stable channel and this is still a Canary / Dev experiment.

This is a medium severity issue, so it doesn't meet the criteria for backmerge to current Stable. But we cannot introduce security regressions into Stable, so this would block Stable channel rollout of this feature in M126.

### pe...@google.com (2024-06-13)

Requesting merge to beta (M127) because latest trunk commit (1313643) appears to be after beta branch point (1313161).
Merge approved: your change passed merge requirements and is auto-approved for M127. Please go ahead and merge the CL to branch 6533 (refs/branch-heads/6533) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: eakpobaro (Android), eakpobaro (iOS), alonbajayo (ChromeOS), danielyip (Desktop)
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [127].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### ap...@google.com (2024-06-13)

Project: chromium/src
Branch: refs/branch-heads/6533

commit d26ad0f448e84a1cca3c37ece56e69dfe59a3df2
Author: Ahmed Moussa <ahmedmoussa@google.com>
Date:   Thu Jun 13 20:00:20 2024

    [M127][media-preview] Prevent potential UAF during VideoFrames lifetime
    
    Extend mapping lifetime till the destruction of VideoFrames.
    
    (cherry picked from commit 9519fb766e1ca2e691ec99f50d6600af5aba6b53)
    
    Bug: 343014709
    Change-Id: I581f90b25c57bd29d5f16ecb6870035d10a4f2f7
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5606664
    Reviewed-by: Ahmed Fakhry <afakhry@chromium.org>
    Commit-Queue: Ahmed Moussa <ahmedmoussa@google.com>
    Cr-Original-Commit-Position: refs/heads/main@{#1313643}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5629642
    Cr-Commit-Position: refs/branch-heads/6533@{#112}
    Cr-Branched-From: 7e0b87ec6b8cb5cb2969e1479fc25776e582721d-refs/heads/main@{#1313161}

M       components/capture_mode/camera_video_frame_handler.cc

https://chromium-review.googlesource.com/5629642


### sp...@google.com (2024-06-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
report of OOB read / user information disclosure


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-28)

Congratulations, Khalil! Thank you for your efforts and reporting this issue to us.

### pe...@google.com (2024-09-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/343014709)*
