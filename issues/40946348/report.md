# UAF in blink::RTCEncodedAudioUnderlyingSource::OnFrameFromSource 

| Field | Value |
|-------|-------|
| **Issue ID** | [40946348](https://issues.chromium.org/issues/40946348) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | gu...@chromium.org |
| **Created** | 2023-11-28 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

tested os:ubuntu 22.04  

tested chromium version:  

Chromium 121.0.6151.0  

Chromium 116.0.5805.0

repro steps:  

1 ./chrome --autoplay-policy=no-user-gesture-required --no-sandbox --user-data-dir=/tmp/xx --js-flags=--expose-gc <http://localhost:8000/crash.html>

**Problem Description:**  

The reppro is unstable in the release build with asan; it took over 10 minutes to reproduce on my local machine. However, in the debug build, the DCHECK error is easily reproducible. By comparing the ASAN log and DCHECK log, it is confirmed that this DCheck was triggered before the undefiend behaviors occurred. I have uploaded both logs, hoping these will assist in identifying the root cause.  

1126/152826.116775:FATAL:rtc\_encoded\_audio\_underlying\_source.cc(67)] Check failed: task\_runner\_->BelongsToCurrentThread().  

#0 0x5606c28ae64c base::debug::CollectStackTrace()  

#1 0x5606c287729a base::debug::StackTrace::StackTrace()  

#2 0x5606c2877255 base::debug::StackTrace::StackTrace()  

#3 0x5606c260ab89 logging::LogMessage::~LogMessage()  

#4 0x5606c25dc3fc logging::(anonymous namespace)::DCheckLogMessage::~DCheckLogMessage()  

#5 0x5606c25dc429 logging::(anonymous namespace)::DCheckLogMessage::~DCheckLogMessage()  

#6 0x5606c25dc0bd logging::CheckError::~CheckError()  

#7 0x5606d1e83cba blink::RTCEncodedAudioUnderlyingSource::OnFrameFromSource()  

#8 0x5606d1e989cb blink::RTCRtpSender::OnAudioFrameFromEncoder()  

#9 0x5606d1e9df2c base::internal::FunctorTraits<>::Invoke<>()  

#10 0x5606d1e9ddf4 base::internal::InvokeHelper<>::MakeItSo<>()  

#11 0x5606d1e9dd65 base::internal::Invoker<>::RunImpl<>()  

#12 0x5606d1e9dcdf base::internal::Invoker<>::Run()  

#13 0x5606d1e787d3 base::RepeatingCallback<>::Run()  

#14 0x5606d1e77862 WTF::CrossThreadFunction<>::Run()  

#15 0x5606d1e768c7 blink::RTCEncodedAudioStreamTransformer::TransformFrame()  

#16 0x5606d1e76835 blink::RTCEncodedAudioStreamTransformer::Broker::TransformFrameOnSourceTaskRunner()  

#17 0x5606d1e7828c base::internal::FunctorTraits<>::Invoke<>()  

#18 0x5606d1e781dd base::internal::InvokeHelper<>::MakeItSo<>()  

#19 0x5606d1e7815d base::internal::Invoker<>::RunImpl<>()  

#20 0x5606d1e780d7 base::internal::Invoker<>::RunOnce()

```
Task trace:  
#0 0x5606d1e772e1 blink::(anonymous namespace)::RTCEncodedAudioStreamTransformerDelegate::Transform()  
#1 0x5606c4f052bd webrtc::voe::(anonymous namespace)::ChannelSend::ProcessAndEncodeAudio()  
  
**Additional Comments:**   
  
  
**Chrome version: ** 119.0.0.0 **Channel: ** Stable  
  
**OS:** Linux

```

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 5.1 KB)
- [1.mp3](attachments/1.mp3) (application/octet-stream, 2.3 KB)
- [dcheck.log](attachments/dcheck.log) (text/plain, 1.6 KB)
- [uaf-asan2.log](attachments/uaf-asan2.log) (text/plain, 47.3 KB)
- [uaf-asan1.log](attachments/uaf-asan1.log) (text/plain, 46.9 KB)

## Timeline

### [Deleted User] (2023-11-28)

[Empty comment from Monorail migration]

### sk...@chromium.org (2023-11-30)

I ran a ClusterFuzz report that did not seem to reproduce the issue [1]. Assigning to code owners of blink::RTCEncodedAudioUnderlyingSource

[1] https://clusterfuzz.com/testcase-detail/5964271008022528

[Monorail components: Blink>WebRTC]

### [Deleted User] (2023-11-30)

[Empty comment from Monorail migration]

### gu...@chromium.org (2023-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-30)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-12-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9d042e0d498356185fe9eb33c53b69fab33d06bf

commit 9d042e0d498356185fe9eb33c53b69fab33d06bf
Author: Guido Urdaneta <guidou@chromium.org>
Date: Fri Dec 01 08:19:24 2023

[InsertableStreams] Drop frames received on the wrong task runner

It can happen during transfer that a frame is posted from the
background media thread to the task runner of the old execution
context, which can lead to races and UAF.

This CL makes underlying sources drop frames received on the
wrong task runner to avoid the problem.

Bug: 1505708
Change-Id: I686228d88cb1c48bdf8c0b6bf85edd280a54300a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5077845
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Reviewed-by: Tony Herre <toprice@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1231802}

[modify] https://crrev.com/9d042e0d498356185fe9eb33c53b69fab33d06bf/third_party/blink/renderer/modules/peerconnection/rtc_encoded_audio_underlying_source.cc
[modify] https://crrev.com/9d042e0d498356185fe9eb33c53b69fab33d06bf/third_party/blink/renderer/modules/peerconnection/rtc_encoded_video_underlying_source.cc


### gu...@chromium.org (2023-12-01)

[Empty comment from Monorail migration]

### gu...@chromium.org (2023-12-01)

[Empty comment from Monorail migration]

### gu...@chromium.org (2023-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-02)

Merge review required: M120 has already been cut for stable release.

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
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-12-04)

M120 merge approved for https://crrev.com/c/5077845
please merge this fix to branch 6099 at your earliest convenience (before EOD Thursday, 7 December) so this fix can be included in the first M120 security refresh -- thanks! 

### gi...@appspot.gserviceaccount.com (2023-12-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/021598ea43c1cbcd6317432858c0f61929c51b1b

commit 021598ea43c1cbcd6317432858c0f61929c51b1b
Author: Guido Urdaneta <guidou@chromium.org>
Date: Mon Dec 04 23:00:41 2023

[InsertableStreams] Drop frames received on the wrong task runner

It can happen during transfer that a frame is posted from the
background media thread to the task runner of the old execution
context, which can lead to races and UAF.

This CL makes underlying sources drop frames received on the
wrong task runner to avoid the problem.

(cherry picked from commit 9d042e0d498356185fe9eb33c53b69fab33d06bf)

Bug: 1505708
Change-Id: I686228d88cb1c48bdf8c0b6bf85edd280a54300a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5077845
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Reviewed-by: Tony Herre <toprice@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1231802}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5082444
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/branch-heads/6099@{#1370}
Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

[modify] https://crrev.com/021598ea43c1cbcd6317432858c0f61929c51b1b/third_party/blink/renderer/modules/peerconnection/rtc_encoded_audio_underlying_source.cc
[modify] https://crrev.com/021598ea43c1cbcd6317432858c0f61929c51b1b/third_party/blink/renderer/modules/peerconnection/rtc_encoded_video_underlying_source.cc


### am...@google.com (2023-12-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-12-07)

Congratulations Cassidy Kim! The Chrome VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-12-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-12-11)

[Empty comment from Monorail migration]

### am...@google.com (2023-12-14)

[Empty comment from Monorail migration]

### am...@google.com (2023-12-14)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1505708?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40946348)*
