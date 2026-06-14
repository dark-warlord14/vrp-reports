# Security: UaF in ImageCapture

| Field | Value |
|-------|-------|
| **Issue ID** | [40096129](https://issues.chromium.org/issues/40096129) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GetUserMedia |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | mm...@semmle.com |
| **Assignee** | ar...@chromium.org |
| **Created** | 2019-08-28 |
| **Bounty** | $20,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/master/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**

In various methods exposed by the mojo interface of ImageCapture, for example, ImageCaptureImpl::GetPhotoState, the corresponding implementation in VideoCaptureManager is called (in this case, VideoCaptureManager::GetPhotoState). In these methods, a callback will be push back to the photo\_request\_queue\_, for example, in VideoCaptureManager [1]

const VideoCaptureController\* controller =  

LookupControllerBySessionId(session\_id); //<-- controller comes from controllers\_, which is added in the VideoCaptureManager::ConnectClient method (a)  

if (!controller)  

return;  

if (controller->IsDeviceAlive()) { //<-- controller is not active if it is in the middle of launching (b)  

controller->GetPhotoState(std::move(callback));  

return;  

}

photo\_request\_queue\_.emplace\_back(  

session\_id,  

base::Bind(&VideoCaptureController::GetPhotoState,  

base::Unretained(controller), base::Passed(&callback))); // <-- unretained raw pointer (c)  

}

These callbacks contains an unretained pointer to a VideoCaptureController, that is managed by the the controller\_ collection. If ImageCaptureImpl::GetPhotoState is called when the device is being launched, then controller->IsDeviceAlive will be false and an unretained version of it will be added to the photo\_request\_queue\_.

During the OnDeviceLaunched method, which is when the device has finished launching, these callbacks will be called [2] In this case, the |IsDeviceAlive| method will return true as the device is already launched. Under normal situation, this will erase the callbacks while the controller and the controller will still be alive. (This is reached from the sequence of calls in the VideoCaptureManager::ProcessDeviceStartRequestQueue method, in which the controller is protected by a callback function)

However, it is possible to prevent the device from being launched by making a call to VideoCaptureHost::Stop while the device is being launched. This would prevent the OnDeviceLaunched method to be called and erase the callbacks in photo\_request\_queue\_ and also remove the controller from controllers\_. At this point, a dangling pointer would be created inside the photo\_request\_queue\_.

If we then make a call to VideoCaptureManager::Start again with the same device and session information, then when the device finished launching the second time, it will go through the photo\_request\_queue\_[3], and pick out the callbacks whose device type and id matches the ones that are being launched. As we can control these information so that the device that is currently launching is identical to the ones that the free'd controller held, the callbacks will be called, with the free'd controller unretained in it. This leads to UaF.

1. <https://cs.chromium.org/chromium/src/content/browser/renderer_host/media/video_capture_manager.cc?g=0&rcl=e83e287f638ab87320d12e9218b2763f9eb6132e&l=660>
2. <https://cs.chromium.org/chromium/src/content/browser/renderer_host/media/video_capture_manager.cc?g=0&rcl=e83e287f638ab87320d12e9218b2763f9eb6132e&l=343>
3. <https://cs.chromium.org/chromium/src/content/browser/renderer_host/media/video_capture_manager.cc?g=0&rcl=e83e287f638ab87320d12e9218b2763f9eb6132e&l=346>

**VERSION**  

Chrome Version: built from master commit faf9f3f, release build  

Operating System: Tested on Ubuntu 18.04.2 LTS, but possible affect other OS too.

**REPRODUCTION CASE**  

To reproduce the issue, a small change is needed because of a javascript bug in the mojo API mojoBinding.js. Since this is only used to emulate a compromised renderer, it has nothing to do with the vulnerability itself. The problem is that in that file, when deserializing UnguessableToken, which consists of 2 64 bit integers, the resulting 64 bit int was cast into Javascript numbers, which is represented as 53 bit doubles, so precision is lost and I cannot obtain the session token when calling the MediaStreamDispatcherHost::OpenDevice mojo API. This can be fixed from the renderer side or by using the cpp API. Either way will be rather tedious, so to keep it simple, I just change the browser side code to give me a fixed token that does not truncate. Specifically, this:

<https://cs.chromium.org/chromium/src/content/browser/renderer_host/media/video_capture_manager.cc?g=0&l=163&rcl=49d247544b7d5ee24821f76a2fc99b9db4aea87b>

is changed to base::UnguessableToken::Deserialize(2,0);

To produce something that does not truncate in Javascript. As the token can be obtained from renderer mojo API and OpenDevice is only called once, I don't believe this affects the vulnerability.

After these changes, run the followings:

$ python ./copy\_mojo\_js\_bindings.py /path/to/chrome/.../out/asan/gen  

$ python -m SimpleHTTPServer&

then replace mojo\_bindings.js with the attached file. This is to ignore some mojom error in original generated file. Then copy the attached image\_capture.mojom.js in to the media/capture/mojom directory and run

$out/asan/chrome --enable-blink-features=MojoJS --user-data-dir=/tmp/abc

and open the page '<http://localhost:8000/image_capture.html>', allow the site to use the camera. It may need to restart couple of times to get the timing right. It normally works for me after restarting once.

Thank you very much for your help and please let me know if there is anything that I can help. Thanks.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Man Yue Mo of Semmle Security Research Team

## Attachments

- [image_capture.mojom.js](attachments/image_capture.mojom.js) (text/plain, 46.3 KB)
- [mojo_bindings.js](attachments/mojo_bindings.js) (text/plain, 162.8 KB)
- [image_capture_asan](attachments/image_capture_asan) (text/plain, 28.5 KB)
- [image_capture.html](attachments/image_capture.html) (text/plain, 3.5 KB)
- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 514 B)

## Timeline

### ct...@chromium.org (2019-08-28)

Setting security labels: Sev-High for sandbox escape and Impact-Stable as it looks like this code has not been changed recently. I think this should affect all desktop OSes, but I'm not sure if this is reachable on Android.

Adding media owners.

+guidou@ can you please take a look? Thanks!


[Monorail components: Blink>GetUserMedia]

### ct...@chromium.org (2019-08-28)

[Empty comment from Monorail migration]

### gu...@chromium.org (2019-09-03)

armax@: Can you take a look?

### ar...@chromium.org (2019-09-04)

I think I have an idea as of how this could be prevented; I will prepare a CL for it today.

### ar...@chromium.org (2019-09-04)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a847b0d9d5bbcce7814f72eaba75ddbc92e3daff

commit a847b0d9d5bbcce7814f72eaba75ddbc92e3daff
Author: Armando Miraglia <armax@chromium.org>
Date: Wed Sep 04 13:50:27 2019

[Video Capture Manager] Guarantee that callbacks are removed on stop.

It was discovered that due the asynchronous nature of starting up a
video capture device, it is possible to leave a callback holding a
dangling pointer if the device is stopped before it is ready.

This change makes sure that when such a stop operation occurse, also the
callbacks associated to the sessions for the starting device are removed.

BUG=998548

Change-Id: I27d42f266b83a2dbb26f7ecfd117cc5931564375
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1782813
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Armando Miraglia <armax@chromium.org>
Cr-Commit-Position: refs/heads/master@{#693148}

[modify] https://crrev.com/a847b0d9d5bbcce7814f72eaba75ddbc92e3daff/content/browser/renderer_host/media/video_capture_manager.cc
[modify] https://crrev.com/a847b0d9d5bbcce7814f72eaba75ddbc92e3daff/content/browser/renderer_host/media/video_capture_manager.h


### ar...@chromium.org (2019-09-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-04)

Requesting merge to stable M76 because latest trunk commit (693148) appears to be after stable branch point (665002).

Requesting merge to beta M77 because latest trunk commit (693148) appears to be after beta branch point (681094).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-09-04)

This bug requires manual review: We are only 5 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@google.com (2019-09-04)

armax@ - can you respond to C#10 to consider the merge request

### gu...@chromium.org (2019-09-04)

1. Does your merge fit within the Merge Decision Guidelines?
Yes. However, the fix has not been completely verified and, while it fixes a security issue. It seems too premature to merge the fix at this time.

2. Links to the CLs you are requesting to merge.
r693148

3. Has the change landed and been verified on master/ToT?
It has landed, but it has not been completely verified.

4. Why are these changes required in this milestone after branch?
Sheriffbot automatically requested merge because this is a security issue.

5. Is this a new feature?
No.

6. If it is a new feature, is it behind a flag using finch?
N/A

### mm...@semmle.com (2019-09-05)

Thanks for the patch. I had a look and am slightly concern about using |session_id| to remove the callbacks. It is possible for multiple sessions to have the same controller [1]. So at least in theory, the following scenario may happen:

1. VideoCaptureHost::Start with session_1
2. GetPhotoState with session_1 (adds controller to |photo_request_queue_| with session_1 as key)
3. VideoCaptureHost::Start with session_2 (reuse the same controller)
4. GetPhotoState with session_2 (adds controller to |photo_request_queue_| with session_2 as key)
5. VideoCaptureHost::Stop with session_1 (because controller has another client (session_2), it will not be removed, but so are the callbacks)
6. VideoCaptureHost::Stop with session_2 (now controller has no more client and will be removed, but only callbacks associated with session_2 are removed, so callbacks with session_1 may still contain dangling pointers)

This is rather sketchy and I've not actually tried it, so it may well not be possible, but I'd think that it may be more robust to just use a WeakPtr instead of Unretained in the callbacks, because in the patch, you are trying to remove all callbacks that contain the controller when it is removed (rather than trying to call them), which should have the same effect as using WeakPtr (callbacks will not be called when WeakPtr is invalidated), but more robust.

Thanks and please let me know what you think.

1. https://cs.chromium.org/chromium/src/content/browser/renderer_host/media/video_capture_manager.cc?gsn=WebURL&targetos=linux&g=0&l=865&rcl%3De83e287f638ab87320d12e9218b2763f9eb6132e

### sr...@google.com (2019-09-05)

[Empty comment from Monorail migration]

### la...@google.com (2019-09-05)

Rejecting the merge so the fix can be properly vetted. Please target M78 as this is an existing problem prior to M77.

### ct...@chromium.org (2019-09-06)

+adetaylor to help evaluate getting this Sev-High sandbox escape into M-77.

### ar...@google.com (2019-09-06)

@mmo: sounds good, and indeed using a weak ptr in that case is in line with best practices. I have a question for you with respect to reproducibility. The instructions provided are not detailed enough for me to know what to do (for example you mention a copy_mojo_js_bindings.py file that I do not find anywhere).
Would you be able to provide more details steps so that I can confirm that the problem is resolved?

Thanks!
A.

### mm...@semmle.com (2019-09-06)

Thanks. Sorry about that, I forgot to attach the file (saw mojo_bindings.js and thought I've attached it) Thanks.

### ad...@chromium.org (2019-09-06)

srinivassista@ re https://crbug.com/chromium/998548#c14 - I agree we won't be able to get this into the initial drop of M77 as it sounds like there are unresolved issues in the fix, but we'll want to include this in the first respin. It's at the upper end of "high severity". I've therefore put back Merge-Request-77 -- but I'm not sure we have a process to note fixes that are in this sort of limbo. WDYT?

### sh...@chromium.org (2019-09-06)

This bug requires manual review: We are only 3 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@google.com (2019-09-06)

adetaylor@ - per our conversation, I am going to drop the Merge-Review-77 label. We can take this change if we decide to do an M77 respin later. Adding M78 as the Target as well.

### na...@google.com (2019-09-06)

[Empty comment from Monorail migration]

### ar...@google.com (2019-09-09)

For reference: https://chromium-review.googlesource.com/c/chromium/src/+/1789223 was landed to address the weak ptr concerns (currently in Canary 79).

### ar...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-09)

This bug requires manual review: We don't branch M78 until 2019-09-05.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), geohsu@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ar...@chromium.org (2019-09-09)

1. Does your merge fit within the Merge Decision Guidelines?
Yes.

2. Links to the CLs you are requesting to merge.
https://chromium-review.googlesource.com/c/chromium/src/+/1789223 

3. Has the change landed and been verified on master/ToT?
Yes (first version 79.0.3906.0); I have done manual verification on ToT

4. Why are these changes required in this milestone after branch?
The fix avoids the risk of using dangling pointers.

5. Is this a new feature?
No.

### ar...@chromium.org (2019-09-09)

FYI: after following the repro steps I was able to verify that before crrev.com/c/1782813 the UaF is hit relatively quickly, however I have run the same test around 10 times (hence closing and reopening the browser) without ever reproducing the issue so I am inclined to say that this verifies the fix.

### gu...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### sr...@google.com (2019-09-09)

Approved for merge to M78 ,branch:3904

### ar...@google.com (2019-09-10)

I am adding request to merge to 77, as per discussion in https://crbug.com/chromium/998548#c19.

### sh...@chromium.org (2019-09-10)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ar...@google.com (2019-09-10)

Does your merge fit within the Merge Decision Guidelines?
Yes.

2. Links to the CLs you are requesting to merge.
https://chromium-review.googlesource.com/c/chromium/src/+/17828131

3. Has the change landed and been verified on master/ToT?
Yes and it has been merged to M78

4. Why are these changes required in this milestone after branch?
See https://crbug.com/chromium/998548#c19.

5. Is this a new feature?
No

### ar...@google.com (2019-09-10)

@adetaylor: I am requesting merge only for the first CL since the second one is not required to fix this issue; the first does already the job. Further, the second fix, while important, is not related to any specific repro steps or exploitable vulnerability so it seems enough to have that in M78. Would you agree?

### ad...@chromium.org (2019-09-10)

armax@ - per https://crbug.com/chromium/998548#c13 the reporter reckons that with some changes it might be possible to continue the exploit even after your first fix, right? Do you disagree that the flow in https://crbug.com/chromium/998548#c13 is possible? Thanks!

### ar...@google.com (2019-09-11)

adetaylor@ - I do not have enough of a good understanding of this file to provide an answer :) per https://crbug.com/chromium/998548#c13 it seems plausible that indeed this might be an option but does the suspicion justify a cherrypick in the stable branch? This is a genuine question as I am in doubt mostly for two reasons: (a) this bug has existed for quite some time, and (b) cherrypicks in stable, for my understanding, should be trivial changes (no functionality). What do you think? Also, would do you think, lakpamarthy@?

Thanks for the help and guidance!

### ad...@chromium.org (2019-09-11)

armax@ all good questions.

I think you should cherry-pick the WeakPtr fix as well. Here's my reasoning. (1) It sounds like it's obviously correct (but tell me if I'm wrong). (2) Both fixes are now visible in git, so people will be paying extra attention to this area of code. Once a fix lands in git, we want to get it shipped as soon as possible, because adversaries do monitor our git repos. (3) This being in the browser process means it's fairly unusual and especially important to get right. Renderer code execution bugs are pretty common, whilst ability to jump from there into the browser process (and thence the rest of the PC) are unusual.

So I think we should be sure by shipping both bits of the fix in M77.

However this absolutely is a matter of judgement, so lakpamarthy@ should make the final call. If you have any stability concerns about the WeakPtr part of the fix, I'd probably change my mind.

### gu...@chromium.org (2019-09-13)

I think the WeakPtr part of the fix is safe and has already had some time to bake. 

### ad...@google.com (2019-09-13)

Re-adding Merge-Request-78. It's not mutually exclusive with Merge-Request-77.

### sh...@chromium.org (2019-09-13)

This bug requires manual review: We don't branch M78 until 2019-09-05.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), geohsu@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@google.com (2019-09-13)

[Empty comment from Monorail migration]

### la...@google.com (2019-09-13)

merge approved M77 branch 3865
merge approved M78 branch 3904

### ar...@google.com (2019-09-16)

FYI: I forgot to mention that the merge to M78 of the weak pointer CL has already happened (crrev.com/c/1795328) while the first CL first landed in M78 (crrev.com/c/1782813).

### ar...@google.com (2019-09-16)

The cherrypicks into M77 have landed:
- crrev.com/c/1803923
- crrev.com/c/1805656

Thanks for the help!
Cheers,
A.

### ar...@google.com (2019-09-16)

I have reverted crrev.com/c/1803923 since it was breaking the build (see crbug.com/1004257). I am, however, reasonably sure that the second CL is enough to address the security bug. I will, however, test a M77 build locally to confirm my understanding.

### ar...@chromium.org (2019-09-16)

I have attempted to reproduce the issue on M77 local build without success. I have change the generation of the session ID to be always 2 similar to how the unguessable token was fixed to a certain value in the repro-steps above. I believe this confirms https://crbug.com/chromium/998548#c44 indicating that the second CL should be the one that fixes the problem and hence enough for M77.

### mm...@semmle.com (2019-09-16)

The second CL alone should be sufficient, and a better way, to fix the bug. Thanks.

### na...@google.com (2019-09-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-09-16)

Congrats! The Panel decided to reward $20,000 for this report! 

### na...@google.com (2019-09-16)

[Empty comment from Monorail migration]

### be...@chromium.org (2019-09-16)

[Empty comment from Monorail migration]

### ad...@google.com (2019-09-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-18)

[Empty comment from Monorail migration]

### mm...@semmle.com (2019-09-19)

@pabrai Thank you very much and sorry for the late reply. My employer has a policy of donating reward to charity. Would you be able to donate the reward to TearFund (https://www.tearfund.org/) please? Thank you very much for your help!

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2020-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2020-01-08)

This issue was migrated from crbug.com/chromium/998548?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-28)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/chrome-blintz-user-guide

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40096129)*
