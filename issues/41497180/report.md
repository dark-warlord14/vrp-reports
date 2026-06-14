# UAF in webrtc::BitrateAllocator::OnNetworkEstimateChanged

| Field | Value |
|-------|-------|
| **Issue ID** | [41497180](https://issues.chromium.org/issues/41497180) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | pe...@chromium.org |
| **Created** | 2024-02-02 |
| **Bounty** | $11,000.00 |

## Description

**Steps to reproduce the problem:**  

repro steps:  

./chrome --use-file-for-fake-video-capture=/xx/fake-video.y4m --use-fake-ui-for-media-stream --use-fake-device-for-media-stream --incognito --user-data-dir=/tmp/xx --js-flags=--expose-gc <http://localhost:8880/crash,html>

**Problem Description:**  

Bisect:  

<https://webrtc-review.googlesource.com/c/src/+/335042>

RCA:  

The StartupVideoSendStream(), SignalEncoderActive()[0], and OnEncoderConfigurationChanged functions will register the current VideoSendStreamImpl instance as an observer of the BitrateAllocatorInterface (bitrate\_allocator\_).

The StopVideoSendStream()[1] and SignalEncoderTimedOut() functions will remove the current VideoSendStreamImpl instance from the observer list of the BitrateAllocatorInterface (bitrate\_allocator\_). Therefore, before a VideoSendStreamImpl instance is deleted, it is necessary to call StopVideoSendStream() or SignalEncoderTimedOut() to ensure it is removed from the observer list of the BitrateAllocatorInterface (bitrate\_allocator\_), otherwise bitrate\_allocator\_ will access a deleted VideoSendStreamImpl instance, ultimately leading to a Use-After-Free (UAF) issue[2].

Suggested fix:  

It might be necessary to add an additional IsRunning() condition check in SignalEncoderActive.  

diff --git a/video/video\_send\_stream\_impl.cc b/video/video\_send\_stream\_impl.cc  

@@ -764,9 +770,13 @@ void VideoSendStreamImpl::OnVideoLayersAllocationUpdated(

void VideoSendStreamImpl::SignalEncoderActive() {  

RTC\_DCHECK\_RUN\_ON(&thread\_checker\_);

- if (rtp\_video\_sender\_->IsActive()) {

- if (rtp\_video\_sender\_->IsActive() && IsRunning()) {  
  
  RTC\_LOG(LS\_INFO) << "SignalEncoderActive, Encoder is active.";  
  
  bitrate\_allocator\_->AddObserver(this, GetAllocationConfig());
- }

}

[0]<https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/video/video_send_stream_impl.cc;l=769;drc=400bd0d71fb18ec50bd4fb36cfe59b7b90411244;bpv=1>  

[1]<https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/video/video_send_stream_impl.cc;l=691;drc=400bd0d71fb18ec50bd4fb36cfe59b7b90411244;bpv=1>  

[2]<https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/call/bitrate_allocator.cc;l=413;bpv=1>

**Additional Comments:**

\*\*Chrome version: \*\* 123.0.6272.2 \*\*Channel: \*\* Dev

**OS:** Linux

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 2.2 KB)
- [fake-video.y4m](attachments/fake-video.y4m) (application/octet-stream, 8.1 MB)
- [asan.log](attachments/asan.log) (text/plain, 29.6 KB)
- [asan.log](attachments/asan_53032339.log) (text/plain, 31.2 KB)

## Timeline

### [Deleted User] (2024-02-02)

[Empty comment from Monorail migration]

### aj...@google.com (2024-02-02)

9c166e064fb2da8273e2d997ce182de49091dbd5 = foundin-123. Sev High as a UAF in the renderer.

==58804==ERROR: AddressSanitizer: heap-use-after-free on address 0x11efd6cca888 at pc 0x7ffdc386a904 bp 0x0036067fe460 sp 0x0036067fe4a8
READ of size 8 at 0x11efd6cca888 thread T16
    #0 0x7ffdc386a903 in webrtc::BitrateAllocator::OnNetworkEstimateChanged(struct webrtc::TargetTransferRate) D:\chromium\src\third_party\webrtc\call\bitrate_allocator.cc:413:52
    #1 0x7ffdbf164d85 in webrtc::internal::Call::OnTargetTransferRate(struct webrtc::TargetTransferRate) D:\chromium\src\third_party\webrtc\call\call.cc:1256:23


I can repro on Windows if I open several tabs and wait ~5 minutes.

.\out\asan\chrome.exe --no-sandbox --no-first-run --use-file-for-fake-video-capture=d:\pocs\1524235\fake-video.y4m   --use-fake-ui-for-media-stream --use-fake-device-for-media-stream --incognito --user-data-dir=d:\pocs\1524235\profile  --js-flags=--expose-gc http://localhost:8880/crash.html

perkj - please take a look.

[Monorail components: Blink>WebRTC]

### aj...@google.com (2024-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2024-02-02)

[Empty comment from Monorail migration]

### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/1524235?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-04)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-02-04)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2024-02-04)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### em...@gmail.com (2024-02-09)

Hi there, just a friendly ping to check in: Is there any progress? 

### pe...@webrtc.org (2024-02-09)

Sorry , I have been out sick was not aware. Looking now. 

### pe...@webrtc.org (2024-02-12)

https://webrtc-review.googlesource.com/c/src/+/338920

### hb...@chromium.org (2024-02-12)

I wanted to see if comment #12 fixes the issue but I was unable to build ASAN on my machine to repro and verify.

Per, can you try the get_asan_chrome script mentioned at https://chromium.googlesource.com/chromium/src/+/master/docs/asan.md ?

Alternatively, emilykim8708@ can you verify if comment #12 fixes the issue?

### em...@gmail.com (2024-02-12)

I have confirmed that UAF will not repro after patching.

### hb...@chromium.org (2024-02-12)

Excellent, thank you!

### pe...@webrtc.org (2024-02-12)

Thank you both!

### am...@google.com (2024-02-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-14)

Congratulations Cassidy Kim! The Chrome VRP Panel has decided to award you $10,000 for this high-quality report of memory corruption in a sandboxed process + $1,000 bisect bonus. Thank you for you efforts and reporting this issue to us -- great work!

### pe...@google.com (2024-02-21)

This is sufficiently serious that it should be merged to dev. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M123. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [123].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### am...@chromium.org (2024-02-21)

this fix (<https://webrtc-review.googlesource.com/c/src/+/338920>) landed on 123, as this was introduced in 123 there is no merge needed

### pe...@google.com (2024-05-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41497180)*
