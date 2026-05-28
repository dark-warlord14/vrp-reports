# Security: UAF in VideoCaptureDeviceWin

| Field | Value |
|-------|-------|
| **Issue ID** | [40061592](https://issues.chromium.org/issues/40061592) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>CameraCapture |
| **Platforms** | Windows |
| **Reporter** | le...@gmail.com |
| **Assignee** | il...@chromium.org |
| **Created** | 2022-11-04 |
| **Bounty** | $11,000.00 |

## Description

**VULNERABILITY DETAILS**

There is a race between `client_.reset` and `client_->OnIncomingCapturedData`:

```
void VideoCaptureDeviceWin::StopAndDeAllocate() {  
  [...]  
  HRESULT hr = media_control_->Stop();    // <<<---------[3]  
  [...]  
  {  
    base::AutoLock lock(lock_);  
    client_.reset();   //<<<------[1]  
    state_ = kIdle;  
  }  
  [...]  
}  
  
void VideoCaptureDeviceWin::FrameReceived(const uint8_t\* buffer,  
                                          int length,  
                                          const VideoCaptureFormat& format,  
                                          base::TimeDelta timestamp,  
                                          bool flip_y) {  
  [...]  
  client_->OnIncomingCapturedData(buffer, length, format, gfx::ColorSpace(),   //<<<------[2]  
                                  camera_rotation_.value(), flip_y,  
                                  base::TimeTicks::Now(), timestamp);  
  [...]  
}  

```

So if the `client_` is reset during the execution of `OnIncomingCapturedData`, the uaf will be triggered.

[1]. <https://source.chromium.org/chromium/chromium/src/+/main:media/capture/video/win/video_capture_device_win.cc;l=568;drc=d387f092f963cdceb9568d3a589686f7cf0e5986>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/main:media/capture/video/win/video_capture_device_win.cc;l=900;drc=d387f092f963cdceb9568d3a589686f7cf0e5986>

By the way, for some devices which use ksproxy filter, the pending event may block the `Stop`[3] function (and also the following `client_.reset()`):

```
media_control_->Stop()  
  => quartz!CFGControl::CImplMediaControl::Stop  
    => quartz!CFilterGraph::Stop  
     => for i in filters : i->Stop()  
           => FilterBase::Stop() [4]  
           => ksproxy!CKsProxy::Stop  
             => ksproxy!CKsOutputPin::Inactive  
CKsOutputPin::Inactive(CKsOutputPin \*this){  
	[...]  
	 if ( this->m_PendingIoCount )  
       WaitForSingleObjectEx(this->m_PendingIoCompletedEvent, 0xFFFFFFFF, 0); // will wait for the signal.  
    [...]  
}  

```

This will prevent this race from happening.

But for the devices whose filter is implemented in a non-blocking way, this UAF will be unavoidable. Take obs virtual camera as an example:

```
media_control_->Stop()  
  => quartz!CFGControl::CImplMediaControl::Stop  
    => quartz!CFilterGraph::Stop  
     => for i in filters : i->Stop()  
           => FilterBase::Stop() [4]  
           => obs_virtualcam_module64!DShow::OutputFilter::Stop  

```

`obs_virtualcam_module64!DShow::OutputFilter::Stop` will not wait for the signal.

[3]. <https://source.chromium.org/chromium/chromium/src/+/main:media/capture/video/win/video_capture_device_win.cc;l=555;drc=d387f092f963cdceb9568d3a589686f7cf0e5986>  

[4]. <https://source.chromium.org/chromium/chromium/src/+/main:media/capture/video/win/filter_base_win.cc;l=115;drc=d387f092f963cdceb9568d3a589686f7cf0e5986>

Fix Suggestion:

diff --git a/media/capture/video/win/video\_capture\_device\_win.cc b/media/capture/video/win/video\_capture\_device\_win.cc  

index 459c5ae1cc4..c8d32703aec 100644  

--- a/media/capture/video/win/video\_capture\_device\_win.cc  

+++ b/media/capture/video/win/video\_capture\_device\_win.cc  

@@ -897,9 +897,12 @@ void VideoCaptureDeviceWin::FrameReceived(const uint8\_t\* buffer,  

// DXVA\_ExtendedFormat. Then use its fields DXVA\_VideoPrimaries,  

// DXVA\_VideoTransferMatrix, DXVA\_VideoTransferFunction and  

// DXVA\_NominalRangeto build a gfx::ColorSpace. See <http://crbug.com/959992>.

- client\_->OnIncomingCapturedData(buffer, length, format, gfx::ColorSpace(),

- {
- base::AutoLock lock(lock\_);
- client\_->OnIncomingCapturedData(buffer, length, format, gfx::ColorSpace(),  
  
  camera\_rotation\_.value(), flip\_y,  
  
  base::TimeTicks::Now(), timestamp);
- }
  
  while (!take\_photo\_callbacks\_.empty()) {  
  
  TakePhotoCallback cb = std::move(take\_photo\_callbacks\_.front());

**VERSION**  

Chrome Version: stable  

Operating System: win

Bisect:

<https://crbug.com/chromium/1137308> added a lock `lock_` to solve the race problem. But since [a], it changed the scope of `lock_` in order to fix deadlock, which let the UAF free again.

[a]. <https://source.chromium.org/chromium/chromium/src/+/7619e9678c1fe8cc4e6025c447e958f5a22913e3>  

[b]. <https://source.chromium.org/chromium/chromium/src/+/6449272149c24168e5b5cd4ff84ea332a784f7bd>

**REPRODUCTION CASE**

$ python3 -m http.server 8000  

$ out/asan/chrome.exe --user-data-dir=xxxx "<http://localhost:8000/poc.html>"

(Make sure your device has a camera, you can download the obs and use its virtual camera: <https://obsproject.com/>)

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

Type of crash: VideoCaptureService utility process, medium integrity as browser process on Win.  

Crash State: see asan file.

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Vulnerability Research Institute

## Attachments

- [asan](attachments/asan) (text/plain, 23.2 KB)
- [poc.html](attachments/poc.html) (text/plain, 922 B)

## Timeline

### [Deleted User] (2022-11-04)

[Empty comment from Monorail migration]

### le...@gmail.com (2022-11-04)

[Comment Deleted]

### le...@gmail.com (2022-11-04)

correction:


VERSION
Chrome Version: stable
Operating System: win

Bisect:

https://crbug.com/chromium/1137308 added[a] a lock `lock_` to solve the race problem. But since [b], it changed the scope of `lock_` in order to fix deadlock, which let the UAF free again.

[a]. https://source.chromium.org/chromium/chromium/src/+/7619e9678c1fe8cc4e6025c447e958f5a22913e3
[b]. https://source.chromium.org/chromium/chromium/src/+/6449272149c24168e5b5cd4ff84ea332a784f7bd

### ke...@chromium.org (2022-11-07)

Thanks for the report.

I have not reproduced this, but the ASAN output along with the analysis appear sound.

hbos@: Can you please take this?

[Monorail components: Internals>Media>CameraCapture]

### [Deleted User] (2022-11-07)

[Empty comment from Monorail migration]

### ha...@google.com (2022-11-08)

[Empty comment from Monorail migration]

### il...@chromium.org (2022-11-08)

Yes, this is a real issue. Previously there was a deadlock there, so the locking was relaxed. Turns out it was relaxed too much.

However, I suggest not to grab the lock two times, but hold it throughout the |VideoCaptureDeviceWin::FrameReceived|.

I'm working on a fix.

### [Deleted User] (2022-11-08)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-11-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d08a3822658cb4ca4261659f1487069a14b51bd9

commit d08a3822658cb4ca4261659f1487069a14b51bd9
Author: Ilya Nikolaevskiy <ilnik@chromium.org>
Date: Wed Nov 09 09:43:24 2022

Fix UAF in VideoCaptureDeviceWin::FrameReceived

Bug: 1381401
Change-Id: Ib742ec7b86d3c419f37f12694bf9cd5f3f03305c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4013158
Reviewed-by: Markus Handell <handellm@google.com>
Commit-Queue: Ilya Nikolaevskiy <ilnik@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1069054}

[modify] https://crrev.com/d08a3822658cb4ca4261659f1487069a14b51bd9/media/capture/video/win/video_capture_device_win.cc


### le...@gmail.com (2022-11-09)

The fix works well in my local test.

### il...@chromium.org (2022-11-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-09)

Requesting merge to extended stable M106 because latest trunk commit (1069054) appears to be after extended stable branch point (1036826).

Requesting merge to stable M107 because latest trunk commit (1069054) appears to be after stable branch point (1047731).

Requesting merge to beta M108 because latest trunk commit (1069054) appears to be after beta branch point (1058933).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-10)

Merge review required: M108 is already shipping to beta.

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
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-10)

Merge review required: M107 is already shipping to stable.

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
Owners: govind (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-10)

Merge review required: M106 is already shipping to stable.

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

### il...@chromium.org (2022-11-10)

1) This is a fix to UAF
2) https://chromium-review.googlesource.com/c/chromium/src/+/4013158
3) Tested on canary 109.0.5411.0
4) No. A fix to vulnerability
5) N/A
6) N/A



### am...@chromium.org (2022-11-11)

M108 merge approved, please merge to branch 5359 by 12pm Pacific Time Monday, so this fix can be included in the M108/Stable cut 

(there are no further planned releases of M107/stable and M106/extended) 

### am...@chromium.org (2022-11-11)

adding label for 108 merge approval 

### gi...@appspot.gserviceaccount.com (2022-11-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/65ad70274d4ba4059a743dbe941c340e7670e2d0

commit 65ad70274d4ba4059a743dbe941c340e7670e2d0
Author: Ilya Nikolaevskiy <ilnik@chromium.org>
Date: Mon Nov 14 12:33:49 2022

Fix UAF in VideoCaptureDeviceWin::FrameReceived

(cherry picked from commit d08a3822658cb4ca4261659f1487069a14b51bd9)

Bug: 1381401
Change-Id: Ib742ec7b86d3c419f37f12694bf9cd5f3f03305c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4013158
Reviewed-by: Markus Handell <handellm@google.com>
Commit-Queue: Ilya Nikolaevskiy <ilnik@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1069054}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4023295
Cr-Commit-Position: refs/branch-heads/5359@{#809}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/65ad70274d4ba4059a743dbe941c340e7670e2d0/media/capture/video/win/video_capture_device_win.cc


### am...@google.com (2022-11-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-17)

Congratulations, Leecraso! The VRP Panel has decided to award you $7000 for this report of a mildly mitigated security bug (must allow web content access to camera) + $3000 for renderer bonus + $1000 bisect bonus for a total reward for $11,000. Thank you efforts in discovering and reporting this issue to us! 

### am...@google.com (2022-11-19)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-11-28)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### le...@gmail.com (2022-11-30)

Hi Amy, it seems the credit in the release note is out of date. Could you please help me to update it to "Leecraso and Guang Gong of 360 Vulnerability Research Institute"?

### am...@chromium.org (2022-11-30)

Hello! Yes, thank you for the ping-- the credit has been updated on the release blog as well as our database of email<->credit conversion so the automation will use the 360 VRI credit from now on. 

### [Deleted User] (2023-02-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1381401?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061592)*
