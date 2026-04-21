# [module:breakout_box]use-after-poison in blink::FrameQueueUnderlyingSource

| Field | Value |
|-------|-------|
| **Issue ID** | [40075979](https://issues.chromium.org/issues/40075979) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>MediaStream |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | gu...@chromium.org |
| **Created** | 2023-10-31 |
| **Bounty** | $10,000.00 |

## Description

**Steps to reproduce the problem:**  

tested os:  

ubuntu 22.04

tested chrome version:  

Version 120.0.6091.0 (Developer Build) (64-bit)

repro steps:

1. ./chrome -user-data-dir=/tmp/xx3 --no-sandbox --incognito <http://localhost:8000/crash.html>

Repro is not very stable and may require multiple attempts. If the issue is not reproduced, you can try using Puppeteer for a more reliable reproduction.

To install Puppeteer, you can refer to this guide: <https://www.browserstack.com/guide/install-and-setup-puppeteer-with-npm-nodejs>  

Run node ./test.js 2>&1 | grep -E 'AddressSanitizer' in the terminal.  

Note:Modify the paths for Chrome and crash.html in the test.js file according to your actual environment.

**Problem Description:**  

==40227==ERROR: AddressSanitizer: use-after-poison on address 0x7ebd00dfc580 at pc 0x55b86f8e5453 bp 0x7ffc9ec08f30 sp 0x7ffc9ec08f28  

READ of size 8 at 0x7ebd00dfc580 thread T0 (chrome)  

#0 0x55b86f8e5452 in scoped\_refptr ./../../base/memory/scoped\_refptr.h:246:59  

#1 0x55b86f8e5452 in Queue ./../../third\_party/blink/renderer/modules/breakout\_box/frame\_queue.h:101:12  

#2 0x55b86f8e5452 in blink::FrameQueueUnderlyingSource<scoped\_refptr[media::AudioBuffer](javascript:void(0);)>::MaybeSendFrameFromQueueToStream() ./../../third\_party/blink/renderer/modules/breakout\_box/frame\_queue\_underlying\_source.cc:300:42  

#3 0x55b86f8f3fe0 in Invoke<void (blink::FrameQueueUnderlyingSource<scoped\_refptr[media::AudioBuffer](javascript:void(0);) >::\*)(), cppgc::internal::BasicCrossThreadPersistent<blink::FrameQueueUnderlyingSource<scoped\_refptr[media::AudioBuffer](javascript:void(0);) >, cppgc::internal::StrongCrossThreadPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy> > ./../../base/functional/bind\_internal.h:713:12  

#4 0x55b86f8f3fe0 in MakeItSo<void (blink::FrameQueueUnderlyingSource<scoped\_refptr[media::AudioBuffer](javascript:void(0);) >::\*)(), std::\_\_Cr::tuple<cppgc::internal::BasicCrossThreadPersistent<blink::FrameQueueUnderlyingSource<scoped\_refptr[media::AudioBuffer](javascript:void(0);) >, cppgc::internal::StrongCrossThreadPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy> > > ./../../base/functional/bind\_internal.h:868:12  

#5 0x55b86f8f3fe0 in RunImpl<void (blink::FrameQueueUnderlyingSource<scoped\_refptr[media::AudioBuffer](javascript:void(0);) >::\*)(), std::\_\_Cr::tuple<cppgc::internal::BasicCrossThreadPersistent<blink::FrameQueueUnderlyingSource<scoped\_refptr[media::AudioBuffer](javascript:void(0);) >, cppgc::internal::StrongCrossThreadPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy> >, 0UL> ./../../base/functional/bind\_internal.h:968:12  

#6 0x55b86f8f3fe0 in base::internal::Invoker<base::internal::BindState<void (blink::FrameQueueUnderlyingSource<scoped\_refptr[media::AudioBuffer](javascript:void(0);)>::\*)(), cppgc::internal::BasicCrossThreadPersistent<blink::FrameQueueUnderlyingSource<scoped\_refptr[media::AudioBuffer](javascript:void(0);)>, cppgc::internal::StrongCrossThreadPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:919:12  

#7 0x55b85c9c36cf in Run ./../../base/functional/callback.h:154:12  

#8 0x55b85c9c36cf in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:201:34  

#9 0x55b85ca2605d in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:463:11)> ./../../base/task/common/task\_annotator.h:89:5  

#10 0x55b85ca2605d in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:461:23  

#11 0x55b85ca24f82 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:326:41  

#12 0x55b85ca26e64 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#13 0x55b85c8ac910 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_default.cc:40:55  

#14 0x55b85ca27d08 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:626:12  

#15 0x55b85c9516ef in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:134:14  

#16 0x55b87499a57f in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer\_main.cc:364:16  

#17 0x55b859a26542 in content::RunZygote(content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:675:14  

#18 0x55b859a27d01 in content::RunOtherNamedProcessTypeMain(std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:779:12  

#19 0x55b859a2b034 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1144:10  

#20 0x55b859a23db8 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:334:36  

#21 0x55b859a249f9 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:347:10  

#22 0x55b85b493f75 in HeadlessChildMain ./../../headless/app/headless\_shell.cc:191:12  

#23 0x55b85b493f75 in headless::HeadlessShellMain(content::ContentMainParams) ./../../headless/app/headless\_shell.cc:252:5  

#24 0x55b849c06288 in ChromeMain ./

**Additional Comments:**

\*\*Chrome version: \*\* 120.0.6091.0 \*\*Channel: \*\* Dev

**OS:** Linux

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 1.9 KB)
- [asan.log](attachments/asan.log) (text/plain, 7.0 KB)
- [test.js](attachments/test.js) (text/plain, 1.1 KB)
- [asan2.log](attachments/asan2.log) (text/plain, 6.6 KB)

## Timeline

### [Deleted User] (2023-10-31)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-10-31)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6573551893544960.

### xi...@chromium.org (2023-10-31)

Thanks for the report. Reporter, does it reproduce in earlier Chrome versions, like Stable or Beta?

[Monorail components: Blink>MediaStream]

### em...@gmail.com (2023-11-01)

After testing, I determined that it only reproduces in the latest dev version.

### xi...@chromium.org (2023-11-01)

Thanks for checking. +guidou@, could you take a look? It seems that you have touched this function recently in https://crrev.com/c/4912794.

### [Deleted User] (2023-11-01)

[Empty comment from Monorail migration]

### gu...@chromium.org (2023-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-02)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-02)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-11-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fda4495a539531af4d31c041f58e5ded13285e68

commit fda4495a539531af4d31c041f58e5ded13285e68
Author: Guido Urdaneta <guidou@chromium.org>
Date: Mon Nov 06 09:31:51 2023

[BreakoutBox] Check validity of context before enqueuing frames.

Now that frames are enqueued in a separate task, it is possible that
the execution context is invalid by the time the task runs.
Drop the frame if the context is invalid to avoid entering an incorrect state hitting CHECK/DCHECK or accessing poisoned memory.

Bug: 1497984
Change-Id: I709a519186490052d8b22d6cfe9569602835f414
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4997039
Auto-Submit: Guido Urdaneta <guidou@chromium.org>
Reviewed-by: Tony Herre <toprice@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Tony Herre <toprice@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1220151}

[modify] https://crrev.com/fda4495a539531af4d31c041f58e5ded13285e68/third_party/blink/renderer/modules/breakout_box/frame_queue_underlying_source.cc
[modify] https://crrev.com/fda4495a539531af4d31c041f58e5ded13285e68/third_party/blink/renderer/modules/breakout_box/frame_queue_underlying_source.h


### gu...@chromium.org (2023-11-06)

[Empty comment from Monorail migration]

### gu...@chromium.org (2023-11-06)

[Empty comment from Monorail migration]

### gu...@chromium.org (2023-11-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-06)

[Empty comment from Monorail migration]

### gu...@chromium.org (2023-11-06)

[Empty comment from Monorail migration]

### gu...@chromium.org (2023-11-06)

[Empty comment from Monorail migration]

### gu...@chromium.org (2023-11-07)

The fix is available since Canary 121.0.6111.0. 
emilykim8708@: Can you verify?

### em...@gmail.com (2023-11-07)

#18
I confirmed that the issue can still be reproduced, and the asan log seems to be exactly the same as before.
tested chrome version:
Chromium 121.0.6113.0
Chromium 120.0.6090.0(with patch from cl:https://chromium-review.googlesource.com/c/chromium/src/+/4997039)

### gu...@chromium.org (2023-11-07)

[Empty comment from Monorail migration]

### gu...@chromium.org (2023-11-07)

emilykim8708@:  Can you share your args.gn file, so that I can try a build as close as possible to yours? I assume you're still using Linux to reproduce.

### em...@gmail.com (2023-11-07)

Below is the content of my args.gn. 

is_asan = true
is_debug = false
enable_nacl = false
treat_warnings_as_errors = false
is_component_build=false
dcheck_always_on = false
use_viz_debugger=false

### gu...@chromium.org (2023-11-07)

emilykim8708@: Can you check with a local build if you can reproduce if you apply this WIP patch: https://crrev.com/c/5009864 ?


### em...@gmail.com (2023-11-07)

guidou@
I have tested with the new cl many times and did not reproduce the issue again.

### gu...@chromium.org (2023-11-07)

@emilykim8708: Thanks a lot for providing feedback so quickly!

I'm surprised this issue doesn't reproduce for you on M119, since the root cause is present there.


### gu...@chromium.org (2023-11-07)

mlippautz@: Is https://crrev.com/c/5009864 acceptable to land?

I believe the issue is that an Oilpan object (MediaStreamAudioTrackUnderlyingSource) is referenced via a raw pointer on another thread and there is a race with the cleanup of the object.
The issue doesn't exist on the equivalent MediaStreamVideoTrackUnderlyingSource because the video code takes a callback with a CrossThreadPersistent reference to the Oilpan object.

The fix is very ugly. It uses a field containing a callback that is never called with a CrossThreadPersistent reference, and the field is set or cleared the way it would be if the target audio code took a callback instead of a raw pointer. Is there a way to make it less ugly until we figure out a way to refactor things such that an ugly solution is not necessary?


### gu...@chromium.org (2023-11-08)

emilykim8708@: Can you try again with the latest version of https://crrev.com/c/5009864 ?


### em...@gmail.com (2023-11-08)

guidou@
I have tested with the new cl many times and did not reproduce the issue.
Test environment:
original Chromium source with cl(https://crrev.com/c/5009864)

### gu...@chromium.org (2023-11-08)

emilykim8708@: Thanks again for the fast feedback!

### gu...@chromium.org (2023-11-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-11-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/186dad16ae69183f02730fb26d84e1d53f9f1b04

commit 186dad16ae69183f02730fb26d84e1d53f9f1b04
Author: Guido Urdaneta <guidou@chromium.org>
Date: Wed Nov 08 15:12:23 2023

[BreakoutBox] Use KeepAlive to prevent lifetime race with audio delivery

Bug: 1497984
Change-Id: Ic22729b2ef9690203bbb09555d32238959e93a0f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5009864
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1221614}

[modify] https://crrev.com/186dad16ae69183f02730fb26d84e1d53f9f1b04/third_party/blink/renderer/modules/breakout_box/media_stream_audio_track_underlying_source.h
[modify] https://crrev.com/186dad16ae69183f02730fb26d84e1d53f9f1b04/third_party/blink/renderer/modules/breakout_box/media_stream_audio_track_underlying_source.cc


### gu...@chromium.org (2023-11-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-08)

[Empty comment from Monorail migration]

### em...@gmail.com (2023-11-08)

Sorry, I missed #25 earlier.

I retested in the older version and did not reproduce the issue using the POC I provided in original report.
tested versions:
Chromium 119.0.6041.0
Chromium 120.0.6066.0 

### gu...@chromium.org (2023-11-08)

 emilykim8708@: Maybe the behavior change introduced in M120 makes it easier to reproduce, but the final fix is independent of the changes in M120.
I did find a bug introduced on M120 with the POC (fixed in https://crbug.com/chromium/1497984#c10).  
Again, thanks a lot for this report and your help testing and verifying all the patches. 


### gu...@chromium.org (2023-11-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-09)

Merge review required: M120 is already shipping to beta.

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

### am...@chromium.org (2023-11-10)

120 merge approved for https://crrev.com/c/5009864
please merge this fix to branch 6099 by EOD Monday so this fix can be included in the next 120 Beta update next week 

### gi...@appspot.gserviceaccount.com (2023-11-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5fde415e06f9ad10b2ae7a20563bfa9d2ce37ad2

commit 5fde415e06f9ad10b2ae7a20563bfa9d2ce37ad2
Author: Guido Urdaneta <guidou@chromium.org>
Date: Fri Nov 10 20:46:57 2023

[BreakoutBox] Use KeepAlive to prevent lifetime race with audio delivery

(cherry picked from commit 186dad16ae69183f02730fb26d84e1d53f9f1b04)

Bug: 1497984
Change-Id: Ic22729b2ef9690203bbb09555d32238959e93a0f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5009864
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1221614}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5018212
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/6099@{#500}
Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

[modify] https://crrev.com/5fde415e06f9ad10b2ae7a20563bfa9d2ce37ad2/third_party/blink/renderer/modules/breakout_box/media_stream_audio_track_underlying_source.h
[modify] https://crrev.com/5fde415e06f9ad10b2ae7a20563bfa9d2ce37ad2/third_party/blink/renderer/modules/breakout_box/media_stream_audio_track_underlying_source.cc


### [Deleted User] (2023-11-10)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-11-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/75f08d190ee294d67d09e4091a6a7c81d82405fd

commit 75f08d190ee294d67d09e4091a6a7c81d82405fd
Author: Guido Urdaneta <guidou@chromium.org>
Date: Fri Nov 10 22:12:24 2023

[BreakoutBox] Check validity of context before enqueuing frames.

Now that frames are enqueued in a separate task, it is possible that
the execution context is invalid by the time the task runs.
Drop the frame if the context is invalid to avoid entering an incorrect state hitting CHECK/DCHECK or accessing poisoned memory.

(cherry picked from commit fda4495a539531af4d31c041f58e5ded13285e68)

Bug: 1497984
Change-Id: I709a519186490052d8b22d6cfe9569602835f414
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4997039
Auto-Submit: Guido Urdaneta <guidou@chromium.org>
Reviewed-by: Tony Herre <toprice@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Tony Herre <toprice@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1220151}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5019488
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/6099@{#509}
Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

[modify] https://crrev.com/75f08d190ee294d67d09e4091a6a7c81d82405fd/third_party/blink/renderer/modules/breakout_box/frame_queue_underlying_source.cc
[modify] https://crrev.com/75f08d190ee294d67d09e4091a6a7c81d82405fd/third_party/blink/renderer/modules/breakout_box/frame_queue_underlying_source.h


### gu...@chromium.org (2023-11-11)

[Comment Deleted]

### gu...@chromium.org (2023-11-11)

1. Was this issue a regression for the milestone it was found in?
The issue has only been reproduced in M120 and later, but the root cause is present in earlier versions. I believe some changes we introduced in M120 make the issue more likely to occur.

2. Is this issue related to a change or feature merged after the latest LTS Milestone?
The original feature landed before the latest LTS milestone. The change that makes it more likely to be reproduced landed after the LTS milestone.

In this issue we landed two changes. In my opinion, we should merge one of them (r1221614) to LTS. The other one deals with a bug introduced in M120.

### vo...@google.com (2023-11-13)

[Empty comment from Monorail migration]

### vo...@google.com (2023-11-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-13)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2023-11-13)

1. one https://crrev.com/c/5019913
2. Low - no conflicts, small change
3. M120
4. Yes

### gm...@google.com (2023-11-14)

[Empty comment from Monorail migration]

### am...@google.com (2023-11-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-16)

Congratulations Cassidy Kim! The Chrome VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-11-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-12-04)

[Empty comment from Monorail migration]

### pg...@google.com (2023-12-06)

[Empty comment from Monorail migration]

### pg...@google.com (2023-12-06)

[Empty comment from Monorail migration]

### na...@google.com (2023-12-11)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### na...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2024-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a46a75912bb9f31397eeb7f5bc6a99c2f045b3a3

commit a46a75912bb9f31397eeb7f5bc6a99c2f045b3a3
Author: Zakhar Voit <voit@google.com>
Date: Thu Jan 11 22:29:27 2024

[M114-LTS][BreakoutBox] Use KeepAlive to prevent lifetime race with audio delivery

(cherry picked from commit 186dad16ae69183f02730fb26d84e1d53f9f1b04)

Bug: 1497984
Change-Id: Ic22729b2ef9690203bbb09555d32238959e93a0f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5009864
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1221614}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5019913
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/branch-heads/5735@{#1661}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/a46a75912bb9f31397eeb7f5bc6a99c2f045b3a3/third_party/blink/renderer/modules/breakout_box/media_stream_audio_track_underlying_source.h
[modify] https://crrev.com/a46a75912bb9f31397eeb7f5bc6a99c2f045b3a3/third_party/blink/renderer/modules/breakout_box/media_stream_audio_track_underlying_source.cc


### rz...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/1497984?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40075979)*
