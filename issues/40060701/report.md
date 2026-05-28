# uaf in  webrtc::VideoStreamEncoder::RequestRefreshFrame

| Field | Value |
|-------|-------|
| **Issue ID** | [40060701](https://issues.chromium.org/issues/40060701) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | sp...@chromium.org |
| **Created** | 2022-08-28 |
| **Bounty** | $7,500.00 |

## Description

**Steps to reproduce the problem:**  

tested os:  

ubuntu 22.04  

tested chrome version:  

1)Chromium 107.0.5264.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1039798.zip)  

2)Chromium 106.0.5216.6(custom asan build)  

args.gn  

is\_asan = true  

is\_debug = false  

enable\_nacl = false  

treat\_warnings\_as\_errors = false  

is\_component\_build=false  

dcheck\_always\_on = fals  

I haven't figured out a way to stably reproduce this problem. I have two ways here.  

1)  

Open multiple browsers in different sessions at the same time，for example  

./chrome --use-file-for-fake-video-capture=|youer path|/fake-video.y4m --use-fake-ui-for-media-stream --use-fake-device-for-media-stream --autoplay-policy=no-user-gesture-required <http://localhost:8001/poc.html> --user-data-dir=/tmp/xx1  

...  

./chrome --use-file-for-fake-video-capture=|youer path|/fake-video.y4m --use-fake-ui-for-media-stream --use-fake-device-for-media-stream --autoplay-policy=no-user-gesture-required <http://localhost:8001/poc.html> --user-data-dir=/tmp/xx5  

I wrote a script that can be tested with one click(The path needs to be modified by yourself).If there is no repro within one or two minutes, ctrl-C to close the script(all browser will automatically close) and execute it again.  

./launcher.sh  

2)I think these 3 conditions are not directly related to this issue(maybe I wrong). Comment out these 3 conditions or any of them to quickly repro the problem.  

+} else if (!video\_is\_suspended && !pending\_frame\_ &&  

+ encoder\_paused\_and\_dropped\_frame\_) {

**Problem Description:**  

this is race issue in webrtc module,and started from this commit(<https://source.chromium.org/chromium/_/webrtc/src.git/+/5e13d0599cbe70070961908a1f6548e35d6a24a2>).  

+} else if (!video\_is\_suspended && !pending\_frame\_ &&  

+ encoder\_paused\_and\_dropped\_frame\_) {  

+ // A frame was enqueued during pause-state, but since it was a native  

+ // frame we could not store it in `pending_frame_` so request a  

+ // refresh-frame instead.  

+ RequestRefreshFrame();  

+}  

The |flag\_[1]|(in WebRTC\_Worker thread) is also released when ~VideoStreamEncoder is called.

[1]<https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/api/task_queue/pending_task_safety_flag.h;drc=2330c1533e39e4f8c195b0a2a05802ea9dee9c85;bpv=1;bpt=1;l=137>  

However, under extreme conditions, the following call chain[2] will be executed after flag\_ is released, and flag() will be forced to add one to the released memory area[3](in ThreadPoolForeg thread), resulting uaf write.  

[2]OnBitrateUpdated()->RequestRefreshFrame()->flag()  

[3]<https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/api/task_queue/pending_task_safety_flag.h;drc=2330c1533e39e4f8c195b0a2a05802ea9dee9c85;l=127>

==601933==ERROR: AddressSanitizer: heap-use-after-free on address 0x6020007fa590 at pc 0x558fefba5352 bp 0x7faf65bfad70 sp 0x7faf65bfad68  

WRITE of size 4 at 0x6020007fa590 thread T25 (ThreadPoolForeg)  

#0 0x558fefba5351 in \_\_cxx\_atomic\_fetch\_add<int> ./../../buildtools/third\_party/libc++/trunk/include/atomic:1009:12  

#1 0x558fefba5351 in fetch\_add ./../../buildtools/third\_party/libc++/trunk/include/atomic:1687:17  

#2 0x558fefba5351 in IncRef ./../../third\_party/webrtc/rtc\_base/ref\_counter.h:29:16  

#3 0x558fefba5351 in AddRef ./../../third\_party/webrtc/api/ref\_counted\_base.h:67:36  

#4 0x558fefba5351 in scoped\_refptr ./../../third\_party/webrtc/api/scoped\_refptr.h:86:13  

#5 0x558fefba5351 in flag ./../../third\_party/webrtc/api/task\_queue/pending\_task\_safety\_flag.h:127:67  

#6 0x558fefba5351 in webrtc::VideoStreamEncoder::RequestRefreshFrame() ./../../third\_party/webrtc/video/video\_stream\_encoder.cc:1916:49  

#7 0x558fefba8c4b in webrtc::VideoStreamEncoder::OnBitrateUpdated(webrtc::DataRate, webrtc::DataRate, webrtc::DataRate, unsigned char, long, double) ./../../third\_party/webrtc/video/video\_stream\_encoder.cc:2206:7  

#8 0x558fefbafe6f in operator() ./../../third\_party/webrtc/video/video\_stream\_encoder.cc:2143:7  

#9 0x558fefbafe6f in \_\_invoke<(lambda at ../../third\_party/webrtc/video/video\_stream\_encoder.cc:2138:29)> ./../../buildtools/third\_party/libc++/trunk/include/\_\_functional/invoke.h:394:23  

#10 0x558fefbafe6f in invoke<(lambda at ../../third\_party/webrtc/video/video\_stream\_encoder.cc:2138:29)> ./../../buildtools/third\_party/libc++/trunk/include/\_\_functional/invoke.h:531:12  

#11 0x558fefbafe6f in InvokeR<void, (lambda at ../../third\_party/webrtc/video/video\_stream\_encoder.cc:2138:29), void> ./../../third\_party/abseil-cpp/absl/functional/internal/any\_invocable.h:130:3  

#12 0x558fefbafe6f in void absl::internal\_any\_invocable::RemoteInvoker<false, void, webrtc::VideoStreamEncoder::OnBitrateUpdated(webrtc::DataRate, webrtc::DataRate, webrtc::DataRate, unsigned char, long, double)::$\_21&&>(absl::internal\_any\_invocable::TypeErasedState\*) ./../../third\_party/abseil-cpp/absl/functional/internal/any\_invocable.h:358:10  

#13 0x558fd07518eb in operator() ./../../third\_party/abseil-cpp/absl/functional/internal/any\_invocable.h:842:1  

#14 0x558fd07518eb in blink::WebRtcTaskQueue::RunTask(absl::AnyInvocable<void () &&>) ./../../third\_party/webrtc\_overrides/task\_queue\_factory.cc:100:3  

#15 0x558fd0753837 in Invoke<void (blink::WebRtcTaskQueue::\*)(absl::AnyInvocable<void () &&>), blink::WebRtcTaskQueue \*, absl::AnyInvocable<void () &&> > ./../../base/bind\_internal.h:608:12  

#16 0x558fd0753837 in MakeItSo<void (blink::WebRtcTaskQueue::\*)(absl::AnyInvocable<void () &&>), blink::WebRtcTaskQueue \*, absl::AnyInvocable<void () &&> > ./../../base/bind\_internal.h:777:12  

#17 0x558fd0753837 in RunImpl<void (blink::WebRtcTaskQueue::\*)(absl::AnyInvocable<void () &&>), std::Cr::tuple<base::internal::UnretainedWrapper[blink::WebRtcTaskQueue](javascript:void(0);), absl::AnyInvocable<void () &&> >, 0UL, 1UL> ./../../base/bind\_internal.h:850:12  

#18 0x558fd0753837 in base::internal::Invoker<base::internal::BindState<void (blink::WebRtcTaskQueue::\*)(absl::AnyInvocable<void () &&>), base::internal::UnretainedWrapper[blink::WebRtcTaskQueue](javascript:void(0);), absl::AnyInvocable<void () &&>>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/bind\_internal.h:819:12  

#19 0x558fddc413ef in Run ./../../base/callback.h:145:12  

#20 0x558fddc413ef in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:135:32  

#21 0x558fddca42c5 in RunTask<(lambda at ../../base/task/thread\_pool/task\_tracker.cc:710:35)> ./../../base/task/common/task\_annotator.h:74:5  

#22 0x558fddca42c5 i

**Additional Comments:**

\*\*Chrome version: \*\* 106.0.5216.6 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- asan.log (text/plain, 59.5 KB)
- poc.html (text/plain, 1.5 KB)
- [launcher.sh](attachments/launcher.sh) (text/plain, 2.4 KB)
- [fake-video.y4m](attachments/fake-video.y4m) (application/octet-stream, 8.1 MB)

## Timeline

### [Deleted User] (2022-08-28)

[Empty comment from Monorail migration]

### es...@chromium.org (2022-08-29)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebRTC]

### [Deleted User] (2022-08-29)

[Empty comment from Monorail migration]

### es...@chromium.org (2022-08-29)

I can't reproduce this on Linux. Are there any other instructions you can provide to repro? Thanks.
cc'ing WebRTC owners

### em...@gmail.com (2022-08-30)

This issue should be related to the machine performance. You can adjust the number of browser instances in launcher.sh and try it several times. Thanks.

### he...@chromium.org (2022-08-30)

Looks like a very extreme case where up to 10 different sessions of Chrome runs the same JS in parallel and it uses several non-default command-line flags, depends on input files instead of real medai and also disables the GPU.

Assigning to sprang@ given comment about 

"this is race issue in webrtc module,and started from this commit(https://source.chromium.org/chromium/_/webrtc/src.git/+/5e13d0599cbe70070961908a1f6548e35d6a24a2)"

but it is probably difficult to analyze this complex case analytically and a solid repro case would be preferable. 

### he...@chromium.org (2022-08-30)

[Empty comment from Monorail migration]

### em...@gmail.com (2022-08-30)

'--disable-gpu' has nothing to do with the issue itself, and can be omitted.
Other flags also have nothing to do with the issue, just to facilitate a test.
I have  reproduced it in a single browser(with origin build) in the local test, but the probability is very small.

Using the instruction step I mentioned earlier can be quickly repro in a single browser.
// Comment out these three conditions
-//} else if (!video_is_suspended && !pending_frame_ &&
-//           encoder_paused_and_dropped_frame_) {
+else{

I think these three conditions have nothing to do with the issue itself(I'm not 100% sure).
Thanks~

### he...@chromium.org (2022-08-30)

Can you add some more details and summarize what you are trying to accomplish in poc.html? Please add some short comments about the structure and what the end result is once it runs.

### he...@chromium.org (2022-08-30)

[Empty comment from Monorail migration]

### hb...@chromium.org (2022-08-30)

On encoder queue, OnBitrateUpdated calls RequestRefreshFrame, which obtains the flag() in order to PostTask.

It's not clear to me what the UAF is. Is there an issue with the PendingTaskSafetyFlag not being thread safe and the task queue deletion causing the posted task, and thus the flag reference, to be deleted on the wrong queue? Using the flag_ boolean on the wrong queue?

handellm@ mentioned something about TQ Delete causing tasks to be destroyed on the wrong sequence, is this related or unrelated?

### sp...@chromium.org (2022-08-30)

There's a few places posting safe tasks to the worker queue from the encoder queue. But that requires increasing the ref counter on the safety from the encoder queue.
The safety is however destroyed before the encoder queue, so if we're unlucky we're trying to read it on an errant task after destruction.

Looks to me like this could be simply fixed by moving the task safety declaration above the encoder queue?



### sp...@chromium.org (2022-08-30)

In any case, this does not seem directly related to r37660, but it might have made this more likely to trigger.
I can prepare a fix based on my hypothesis in #12.

### gi...@appspot.gserviceaccount.com (2022-08-30)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/1cb799c31c882e60d1d3d24863b61811a039d40c

commit 1cb799c31c882e60d1d3d24863b61811a039d40c
Author: Erik Språng <sprang@webrtc.org>
Date: Tue Aug 30 10:02:14 2022

Prevent potential UAF during VideoStreamEncoder teardown.

Bug: chromium:1357413
Change-Id: I9ec4d4fbafe1c25530346faf09f5b437fad718cc
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/273482
Reviewed-by: Markus Handell <handellm@webrtc.org>
Commit-Queue: Henrik Boström <hbos@webrtc.org>
Auto-Submit: Erik Språng <sprang@webrtc.org>
Reviewed-by: Henrik Boström <hbos@webrtc.org>
Commit-Queue: Markus Handell <handellm@webrtc.org>
Cr-Commit-Position: refs/heads/main@{#37948}

[modify] https://crrev.com/1cb799c31c882e60d1d3d24863b61811a039d40c/video/video_stream_encoder.h


### gi...@appspot.gserviceaccount.com (2022-08-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f853f1d7a926b5a2c53b4a706bfd42a9eebb8d65

commit f853f1d7a926b5a2c53b4a706bfd42a9eebb8d65
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Aug 30 16:41:27 2022

Roll WebRTC from 11093b2ca373 to 319531efa68d (9 revisions)

https://webrtc.googlesource.com/src.git/+log/11093b2ca373..319531efa68d

2022-08-30 asapersson@webrtc.org Add support for more scalability modes (1.5:1 resolution ratio).
2022-08-30 landrey@google.com Revert "Reland "ObjC ADM: record/play implementation via RTCAudioDevice [3/3]""
2022-08-30 daniel.l@hpcnt.com Add an API to query resolution ratio between spatial layers
2022-08-30 sprang@webrtc.org Prevent potential UAF during VideoStreamEncoder teardown.
2022-08-30 landrey@google.com Revert "rtpsender interface: make pure virtual again"
2022-08-30 yura.yaroshevich@gmail.com Reland "ObjC ADM: record/play implementation via RTCAudioDevice [3/3]"
2022-08-30 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision a5257ccce7..c29d1550ae (1040403:1040869)
2022-08-30 samvi@google.com Cleanup: Make AsyncResolveInterface::Start(addr,family) pure virtual
2022-08-30 asapersson@webrtc.org Add support for scalability modes S2T2, S3T1, S3T2.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/webrtc-chromium-autoroll
Please CC webrtc-chromium-sheriffs-robots@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in WebRTC: https://bugs.chromium.org/p/webrtc/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1357413
Tbr: webrtc-chromium-sheriffs-robots@google.com
Change-Id: I4e573311d08fe5efa5bed576e5c8fdf15dddb491
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3864812
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1041032}

[modify] https://crrev.com/f853f1d7a926b5a2c53b4a706bfd42a9eebb8d65/DEPS


### em...@gmail.com (2022-08-30)

I tested with this patch( https://crrev.com/1cb799c31c882e60d1d3d24863b61811a039d40c/video/video_stream_encoder.h),never repro again.
tested step:
1)Comment out these 3 conditions.
    -} else if (!video_is_suspended && !pending_frame_ &&
    -           encoder_paused_and_dropped_frame_) {
     +}else{
2)with single browser run about 10minitues.
3)with muli browser run about 10minitues.


### bo...@chromium.org (2022-08-31)

Hi there, this is your friendly security sheriff checking in. I'm setting severity to high due to potentially exploitable memory corruption in a sandboxed process. If you believe this is inaccurate please adjust accordingly with a brief rationale for the change. 

### ha...@google.com (2022-09-01)

We believe this is fixed now.

### [Deleted User] (2022-09-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-07)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-07)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-07)

Requesting merge to beta M106 because latest trunk commit (1041032) appears to be after beta branch point (1036826).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-07)

Merge review required: a commit with DEPS changes was detected.

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

### sp...@chromium.org (2022-09-08)

1. Crash
2. https://webrtc.googlesource.com/src.git/+/1cb799c31c882e60d1d3d24863b61811a039d40c
3. Yes.
4. No, pure bug fix.
5. -
6. Not a major issue in Stable.

### sr...@google.com (2022-09-08)

Merge approved for M106 branch: pls refer to go/chrome-branches for more info

### gi...@appspot.gserviceaccount.com (2022-09-09)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/860ad5321f87a0aeb6841e57b2fa73fa9ea3c65b

commit 860ad5321f87a0aeb6841e57b2fa73fa9ea3c65b
Author: Erik Språng <sprang@webrtc.org>
Date: Tue Aug 30 10:02:14 2022

[M106] Prevent potential UAF during VideoStreamEncoder teardown.

(cherry picked from commit 1cb799c31c882e60d1d3d24863b61811a039d40c)

Bug: chromium:1357413
Change-Id: I9ec4d4fbafe1c25530346faf09f5b437fad718cc
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/273482
Reviewed-by: Markus Handell <handellm@webrtc.org>
Commit-Queue: Henrik Boström <hbos@webrtc.org>
Auto-Submit: Erik Språng <sprang@webrtc.org>
Reviewed-by: Henrik Boström <hbos@webrtc.org>
Commit-Queue: Markus Handell <handellm@webrtc.org>
Cr-Original-Commit-Position: refs/heads/main@{#37948}
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/274703
Commit-Queue: Erik Språng <sprang@webrtc.org>
Cr-Commit-Position: refs/branch-heads/5249@{#3}
Cr-Branched-From: 7aaeb5a270ba23f5844f7301a50aaff9b6ca6126-refs/heads/main@{#37825}

[modify] https://crrev.com/860ad5321f87a0aeb6841e57b2fa73fa9ea3c65b/video/video_stream_encoder.h


### am...@google.com (2022-09-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-09-22)

Congratulations on another one, Cassidy Kim! The VRP Panel has decided to award you $7000 for this report + $500 bisect bonus. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2022-09-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1357413?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060701)*
