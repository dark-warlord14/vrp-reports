# memeory corruption in frame_queue_underlying_source.cc

| Field | Value |
|-------|-------|
| **Issue ID** | [40059591](https://issues.chromium.org/issues/40059591) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>MediaStream |
| **Platforms** | Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | be...@google.com |
| **Created** | 2022-05-07 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**  

OS:  

Ubuntu 22.04  

Version 103.0.5042.0 (Official Build) dev (64-bit)

This issue is not stable to repro with chrome asan version.  

So,I tested with non asan version. It will crash about 30 ~ 60 seconds.

1.google-chrome --use-fake-device-for-media-stream --js-flags=--expose-gc --use-fake-ui-for-media-stream --user-data-dir=/tmp/xx67 --incognito <http://localhost:8000/crash.html>

**Problem Description:**  

Received signal 11 SEGV\_MAPERR 7ea500281000  

#0 0x564463a8c81b in \_\_interceptor\_backtrace ??:?  

#1 0x564463a8c81b in ?? ??:0  

#2 0x564472d54c19 in base::debug::CollectStackTrace(void\*\*, unsigned long) stack\_trace\_posix.cc:?  

#3 0x564472d54c19 in ?? ??:0  

#4 0x564472b02613 in base::debug::StackTrace::StackTrace() stack\_trace.cc:?  

#5 0x564472b02613 in ?? ??:0  

#6 0x564472d536de in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo\_t\*, void\*) stack\_trace\_posix.cc:?  

#7 0x564472d536de in ?? ??:0  

#8 0x7f58ac98e420 in \_\_funlockfile :?  

#9 0x7f58ac98e420 in ?? ??:0  

#10 0x56446e87fca7 in cppgc::internal::WeakCrossThreadPersistentPolicy::GetPersistentRegion(void const\*) pointer-policies.cc:?  

#11 0x56446e87fca7 in ?? ??:0  

#12 0x5644872fbbce in blink::FrameQueueUnderlyingSource<scoped\_refptr[media::VideoFrame](javascript:void(0);) >::Close() frame\_queue\_underlying\_source.cc:?  

#13 0x5644872fbbce in ?? ??:0  

#14 0x5644872fc815 in non-virtual thunk to blink::FrameQueueUnderlyingSource<scoped\_refptr[media::VideoFrame](javascript:void(0);) >::ContextDestroyed() frame\_queue\_underlying\_source.cc:?  

#15 0x5644872fc815 in ?? ??:0  

#16 0x5644830ec785 in blink::ContextLifecycleObserver::NotifyContextDestroyed() context\_lifecycle\_observer.cc:?  

#17 0x5644830ec785 in ?? ??:0  

#18 0x5644830e9e31 in blink::ContextLifecycleNotifier::NotifyContextDestroyed() context\_lifecycle\_notifier.cc:?  

#19 0x5644830e9e31 in ?? ??:0  

#20 0x56447ff6ae9a in blink::LocalDOMWindow::FrameDestroyed() local\_dom\_window.cc:?  

#21 0x56447ff6ae9a in ?? ??:0  

#22 0x56447ff6b1b6 in blink::LocalDOMWindow::Reset() local\_dom\_window.cc:?  

#23 0x56447ff6b1b6 in ?? ??:0  

#24 0x56447fe53102 in blink::LocalFrame::SetDOMWindow(blink::LocalDOMWindow\*) local\_frame.cc:?  

#25 0x56447fe53102 in ?? ??:0  

#26 0x56448235d88b in blink::DocumentLoader::InitializeWindow(blink::Document\*) document\_loader.cc:?  

#27 0x56448235d88b in ?? ??:0  

#28 0x56448236156f in blink::DocumentLoader::CommitNavigation() document\_loader.cc:?  

#29 0x56448236156f in ?? ??:0  

#30 0x5644823ba892 in blink::FrameLoader::CommitDocumentLoader(blink::DocumentLoader\*, blink::HistoryItem\*, blink::CommitReason) frame\_loader.cc:?  

#31 0x5644823ba892 in ?? ??:0  

#32 0x5644823c2d36 in blink::FrameLoader::CommitNavigation(std::\_\_1::unique\_ptr<blink::WebNavigationParams, std::\_\_1::default\_delete[blink::WebNavigationParams](javascript:void(0);) >, std::\_\_1::unique\_ptr<blink::WebDocumentLoader::ExtraData, std::\_\_1::default\_delete[blink::WebDocumentLoader::ExtraData](javascript:void(0);) >, blink::CommitReason) frame\_loader.cc:?  

#33 0x5644823c2d36 in ?? ??:0  

#34 0x564480f6dd4a in blink::WebLocalFrameImpl::CommitNavigation(std::\_\_1::unique\_ptr<blink::WebNavigationParams, std::\_\_1::default\_delete[blink::WebNavigationParams](javascript:void(0);) >, std::\_\_1::unique\_ptr<blink::WebDocumentLoader::ExtraData, std::\_\_1::default\_delete[blink::WebDocumentLoader::ExtraData](javascript:void(0);) >) web\_local\_frame\_impl.cc:?  

#35 0x564480f6dd4a in ?? ??:0  

#36 0x5644848527b2 in content::RenderFrameImpl::CommitNavigationWithParams(mojo::StructPtr[blink::mojom::CommonNavigationParams](javascript:void(0);), mojo::StructPtr[blink::mojom::CommitNavigationParams](javascript:void(0);), std::\_\_1::unique\_ptr<blink::PendingURLLoaderFactoryBundle, std::\_\_1::default\_delete[blink::PendingURLLoaderFactoryBundle](javascript:void(0);) >, absl::optional<std::\_\_1::vector<mojo::StructPtr[blink::mojom::TransferrableURLLoader](javascript:void(0);), std::\_\_1::allocator<mojo::StructPtr[blink::mojom::TransferrableURLLoader](javascript:void(0);) > > >, mojo::StructPtr[blink::mojom::ControllerServiceWorkerInfo](javascript:void(0);), mojo::StructPtr[blink::mojom::ServiceWorkerContainerInfoForClient](javascript:void(0);), mojo::PendingRemote[network::mojom::URLLoaderFactory](javascript:void(0);), mojo::PendingRemote[blink::mojom::CodeCacheHost](javascript:void(0);), mojo::StructPtr[content::mojom::CookieManagerInfo](javascript:void(0);), mojo::StructPtr[content::mojom::StorageInfo](javascript:void(0);), std::\_\_1::unique\_ptr<content::DocumentState, std::\_\_1::default\_delete[content::DocumentState](javascript:void(0);) >, std::\_\_1::unique\_ptr<blink::WebNavigationParams, std::\_\_1::default\_delete[blink::WebNavigationParams](javascript:void(0);) >) render\_frame\_impl.cc:?  

#37 0x5644848527b2 in ?? ??:0  

#38 0x5644848acac6 in void base::internal::FunctorTraits<void (content::RenderFrameImpl::\*)(mojo::StructPtr[blink::mojom::CommonNavigationParams](javascript:void(0);), mojo::StructPtr[blink::mojom::CommitNavigationParams](javascript:void(0);), std::\_\_1::unique\_ptr<blink::PendingURLLoaderFactoryBundle, std::\_\_1::default\_delete[blink::PendingURLLoaderFactoryBundle](javascript:void(0);) >, absl::optional<std::\_\_1::vector<mojo::StructPtr[blink::mojom::TransferrableURLLoader](javascript:void(0);), std::\_\_1::allocator<mojo::StructPtr[blink::mojom::TransferrableURLLoader](javascript:void(0);) > > >, mojo::StructPtr[blink::mojom::ControllerServiceWorkerInfo](javascript:void(0);), mojo::StructPtr[blink::mojom::ServiceWorkerContainerInfoForClient](javascript:void(0);), mojo::PendingRemote[network::mojom::URLLoaderFactory](javascript:void(0);), mojo::PendingRemote[blink::mojom::CodeCacheHost](javascript:void(0);), mojo::StructPtr[content::mojom::CookieManagerInfo](javascript:void(0);), mojo::StructPtr[content::mojom::StorageInfo](javascript:void(0);), std::\_\_1::unique\_ptr<content::DocumentState, std::\_\_1::default\_delete[content::DocumentState](javascript:void(0);) >, std:

**Additional Comments:**

\*\*Chrome version: \*\* Version 103.0.5042.0 (Official Build) dev (64-bit) \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 690 B)
- [ws.js](attachments/ws.js) (text/plain, 274 B)
- [crash.html](attachments/crash.html) (text/plain, 717 B)
- [wrapper.html](attachments/wrapper.html) (text/plain, 234 B)
- [ws.js](attachments/ws.js) (text/plain, 274 B)

## Timeline

### dt...@chromium.org (2022-05-10)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebAudio]

### am...@chromium.org (2022-06-14)

Due to an issue with the monorail wizard workflow, this issue was not originally labeled as a security bug and, therefore, this issue did not make it to the security team bug queue for triage. This wizard workflow issue was just discovered today, updating accordingly now. 

Tentatively setting these and others as security bugs for general tracking purposes and to go into actual security triage; however, there is no indication that this issue results in security consequences nor has it yet been evaluated for such. 

### [Deleted User] (2022-06-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-06-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6704443081031680.

### cl...@chromium.org (2022-06-14)

ClusterFuzz testcase 6704443081031680 is closed as invalid, so closing issue.

### xi...@chromium.org (2022-06-21)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-06-21)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-06-21)

Thanks for the report! I'm not able to reproduce, but the latest report https://crbug.com/1337806 has provided detailed analysis. +guidou@ to take a look. Thanks!

[Monorail components: Blink>MediaStream]

### [Deleted User] (2022-06-21)

[Empty comment from Monorail migration]

### el...@chromium.org (2022-06-21)

xinghuilu@, could you please approve those who are CCed on the current bug to also view crbug.com/1337806?

### gu...@chromium.org (2022-06-21)

[Empty comment from Monorail migration]

### el...@chromium.org (2022-06-21)

[Empty comment from Monorail migration]

### gu...@chromium.org (2022-06-21)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-06-21)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-06-21)

Re https://crbug.com/chromium/1323488#c10: Yes, you should have access to crbug.com/1337806 now

### [Deleted User] (2022-06-21)

herre: Uh oh! This issue still open and hasn't been updated in the last 44 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-21)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-05)

herre: Uh oh! This issue still open and hasn't been updated in the last 58 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vu...@sourcefire.com (2022-07-06)

We also discovered this issue as https://bugs.chromium.org/p/chromium/issues/detail?id=1337806 and ours was marked as duplicate.
However, I don't see any movement on a patch for this bug? 

### [Deleted User] (2022-07-06)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### he...@google.com (2022-07-07)

Ben, do you think you could take a look at this? As mentioned above, the details in crbug.com/1337806 should help.

### be...@chromium.org (2022-07-07)

[Empty comment from Monorail migration]

### be...@google.com (2022-07-12)

Sorry for the delay. I'm able to repro with 105.0.5148.2 (Official Build) dev (64-bit) on Linux, but haven't been able to repro in a test.


### em...@gmail.com (2022-08-20)

[Comment Deleted]

### em...@gmail.com (2022-08-20)

tested OS:
chrome version:
Version 106.0.5245.0 (Official Build) dev (64-bit)
Chromium 106.0.5223.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1032261.zip)

Is there any progress on this issue?
After simple modification, I can still stably reproduce in the new version of chrome

repro steps:
google-chrome --use-fake-device-for-media-stream    --js-flags=--expose-gc --use-fake-ui-for-media-stream --user-data-dir=/tmp/xx67 --incognito http://localhost:8000/wrapper.html

This issue will repro in about 30 seconds in my local pc.
Occasionally, this poc will repro  null pointer dereference(SEGV_MAPERR 000000000190) with similar  backtrace

### be...@google.com (2022-08-24)

[Empty comment from Monorail migration]

### be...@google.com (2022-08-24)

Apologies for the delay; I was unexpectedly away from work.

Unfortunately the repro from the bug description (or from https://crbug.com/chromium/1323488#c25) is not reliable enough to make into a test, so I will need to rely on manual testing. I have also not succeeded in reproducing the issue in a unit test.

Aside from hitting some DCHECKs in various other places in Chromium, the repro causes the worker thread's heap to be destroyed while the main thread still believes that the transferred source is alive. After discussing with mlippautz@, it seems like we can fix this by clearing host_->transferred_source_ in TransferredFrameQueueUnderlyingSource::ContextDestroyed(). I'll have to check if this is a valid fix.


### be...@google.com (2022-08-24)

[Empty comment from Monorail migration]

### vu...@sourcefire.com (2022-08-24)

Benjamin, did you look at our description and poc at https://bugs.chromium.org/p/chromium/issues/detail?id=1337806? 

### be...@google.com (2022-08-24)

Yes, I also tried to use the repro in https://crbug.com/chromium/1337806, but it is also not reliable. If left running for long enough, both the repro in this bug and the one in https://crbug.com/chromium/1337806 will reproduce the issue, but there's no way to make a reliable test from that, because a test needs to succeed or fail within a set amount of time.

### be...@google.com (2022-08-30)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/63ce9c40e1a67395278dfc70ecfb545a818747bb

commit 63ce9c40e1a67395278dfc70ecfb545a818747bb
Author: Ben Wagner <benjaminwagner@google.com>
Date: Wed Aug 31 09:23:46 2022

Fix races in FrameQueueUnderlyingSource related to CrossThreadPersistent

The repro in https://crbug.com/chromium/1323488 unfortunately does not reliably reproduce
the races when run as a web test. I was also not able to repro the
races in a unit test.

There are actually three fixes in this CL; it was easiest to fix them
all together so that I can run the repro locally for an extended period
without it being stopped by a crash.

The underlying cause for all three races is that CrossThreadPersistent
can refer to an object whose heap has already been destroyed. When
accessed on the thread corresponding to that heap, there is no race,
but when accessed from a different thread, there is a period of time
after the heap is destroyed before the CrossThreadPersistent is
cleared.

1. The FrameQueueUnderlyingSource::transferred_source_ member's pointer
   is accessed in FrameQueueUnderlyingSource::Close. This CL adds a
   callback to clear the pointer in
   TransferredFrameQueueUnderlyingSource::ContextDestroyed.

2. The TransferredFrameQueueUnderlyingSource constructor takes a raw
   pointer to the original FrameQueueUnderlyingSource, which is
   associated with a different thread. GC won't be able to update this
   raw pointer since it's on the wrong stack. This CL changes the raw
   pointer to a CrossThreadPersistent which is visible to GC.

3. Same as 2, but for the callstack ConnectHostCallback,
   MediaStream(Audio|Video)TrackUnderlyingSource::OnSourceTransferStarted
   and FrameQueueUnderlyingSource::TransferSource.

Bug: 1323488
Change-Id: Id63484eebefd2e003959b25bd752ac8263caab4f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3865452
Commit-Queue: Ben Wagner <benjaminwagner@google.com>
Reviewed-by: Thomas Guilbert <tguilbert@chromium.org>
Auto-Submit: Ben Wagner <benjaminwagner@google.com>
Cr-Commit-Position: refs/heads/main@{#1041434}

[modify] https://crrev.com/63ce9c40e1a67395278dfc70ecfb545a818747bb/third_party/blink/renderer/modules/breakout_box/transferred_frame_queue_underlying_source.h
[modify] https://crrev.com/63ce9c40e1a67395278dfc70ecfb545a818747bb/third_party/blink/renderer/modules/breakout_box/frame_queue_underlying_source.cc
[modify] https://crrev.com/63ce9c40e1a67395278dfc70ecfb545a818747bb/third_party/blink/renderer/modules/breakout_box/media_stream_video_track_underlying_source.h
[modify] https://crrev.com/63ce9c40e1a67395278dfc70ecfb545a818747bb/third_party/blink/renderer/modules/breakout_box/media_stream_audio_track_underlying_source.h
[modify] https://crrev.com/63ce9c40e1a67395278dfc70ecfb545a818747bb/third_party/blink/renderer/modules/breakout_box/frame_queue_transferring_optimizer.cc
[modify] https://crrev.com/63ce9c40e1a67395278dfc70ecfb545a818747bb/third_party/blink/renderer/modules/breakout_box/media_stream_video_track_underlying_source.cc
[modify] https://crrev.com/63ce9c40e1a67395278dfc70ecfb545a818747bb/third_party/blink/renderer/modules/breakout_box/media_stream_audio_track_underlying_source.cc
[modify] https://crrev.com/63ce9c40e1a67395278dfc70ecfb545a818747bb/third_party/blink/renderer/modules/breakout_box/frame_queue_transferring_optimizer.h
[modify] https://crrev.com/63ce9c40e1a67395278dfc70ecfb545a818747bb/third_party/blink/renderer/modules/breakout_box/transferred_frame_queue_underlying_source.cc
[modify] https://crrev.com/63ce9c40e1a67395278dfc70ecfb545a818747bb/third_party/blink/renderer/modules/breakout_box/frame_queue_underlying_source.h


### be...@google.com (2022-09-13)

Verified that 106.0.5249.30 (Official Build) beta (64-bit) Linux crashes within ~15s but 107.0.5286.2 (Official Build) dev (64-bit) Linux runs for 8h without crashing.


### [Deleted User] (2022-09-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-09-20)

For some reason this bug being updated to Fixed did not trigger the bot to add merge labels. While a page reload is a bit of a mitigation, it's somewhat part of a standard browser work flow and malicious web content could be crafted by an attacker to induce the user to reload, resulting in a potential oob read here. I feel like this is potentially a medium severity bug rather than a high, but given we are coming up on 106/Stable release, medium severity fixes should be backmerged to next stable at a minimum. 
Chatted with Ben off-bug and there are no issues with backmerging this to 106. Adding a merge approval label. Please backmerge ASAP this morning/today so this fix can be included in M106 Stable cut for release next week. Thank you! 



### am...@chromium.org (2022-09-20)

I'm just now reviewing the stack trace and other report, and this looks like a null pointer deref and would not be a security bug. There are no concerns if this fix is unable to be backmerged today. Apologies for any inconvenience caused. :( 

### gi...@appspot.gserviceaccount.com (2022-09-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fefd6198da317344f24d1c16ec9670cf0e93793e

commit fefd6198da317344f24d1c16ec9670cf0e93793e
Author: Ben Wagner <benjaminwagner@google.com>
Date: Tue Sep 20 18:38:53 2022

[M106] Fix races in FrameQueueUnderlyingSource related to CrossThreadPersistent

The repro in https://crbug.com/chromium/1323488 unfortunately does not reliably reproduce
the races when run as a web test. I was also not able to repro the
races in a unit test.

There are actually three fixes in this CL; it was easiest to fix them
all together so that I can run the repro locally for an extended period
without it being stopped by a crash.

The underlying cause for all three races is that CrossThreadPersistent
can refer to an object whose heap has already been destroyed. When
accessed on the thread corresponding to that heap, there is no race,
but when accessed from a different thread, there is a period of time
after the heap is destroyed before the CrossThreadPersistent is
cleared.

1. The FrameQueueUnderlyingSource::transferred_source_ member's pointer
   is accessed in FrameQueueUnderlyingSource::Close. This CL adds a
   callback to clear the pointer in
   TransferredFrameQueueUnderlyingSource::ContextDestroyed.

2. The TransferredFrameQueueUnderlyingSource constructor takes a raw
   pointer to the original FrameQueueUnderlyingSource, which is
   associated with a different thread. GC won't be able to update this
   raw pointer since it's on the wrong stack. This CL changes the raw
   pointer to a CrossThreadPersistent which is visible to GC.

3. Same as 2, but for the callstack ConnectHostCallback,
   MediaStream(Audio|Video)TrackUnderlyingSource::OnSourceTransferStarted
   and FrameQueueUnderlyingSource::TransferSource.

(cherry picked from commit 63ce9c40e1a67395278dfc70ecfb545a818747bb)

Bug: 1323488
Change-Id: Id63484eebefd2e003959b25bd752ac8263caab4f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3865452
Commit-Queue: Ben Wagner <benjaminwagner@google.com>
Reviewed-by: Thomas Guilbert <tguilbert@chromium.org>
Auto-Submit: Ben Wagner <benjaminwagner@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1041434}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3908010
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Reviewed-by: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/5249@{#521}
Cr-Branched-From: 4f7bea5de862aaa52e6bde5920755a9ef9db120b-refs/heads/main@{#1036826}

[modify] https://crrev.com/fefd6198da317344f24d1c16ec9670cf0e93793e/third_party/blink/renderer/modules/breakout_box/transferred_frame_queue_underlying_source.h
[modify] https://crrev.com/fefd6198da317344f24d1c16ec9670cf0e93793e/third_party/blink/renderer/modules/breakout_box/frame_queue_underlying_source.cc
[modify] https://crrev.com/fefd6198da317344f24d1c16ec9670cf0e93793e/third_party/blink/renderer/modules/breakout_box/media_stream_video_track_underlying_source.h
[modify] https://crrev.com/fefd6198da317344f24d1c16ec9670cf0e93793e/third_party/blink/renderer/modules/breakout_box/media_stream_audio_track_underlying_source.h
[modify] https://crrev.com/fefd6198da317344f24d1c16ec9670cf0e93793e/third_party/blink/renderer/modules/breakout_box/frame_queue_transferring_optimizer.cc
[modify] https://crrev.com/fefd6198da317344f24d1c16ec9670cf0e93793e/third_party/blink/renderer/modules/breakout_box/media_stream_video_track_underlying_source.cc
[modify] https://crrev.com/fefd6198da317344f24d1c16ec9670cf0e93793e/third_party/blink/renderer/modules/breakout_box/media_stream_audio_track_underlying_source.cc
[modify] https://crrev.com/fefd6198da317344f24d1c16ec9670cf0e93793e/third_party/blink/renderer/modules/breakout_box/frame_queue_transferring_optimizer.h
[modify] https://crrev.com/fefd6198da317344f24d1c16ec9670cf0e93793e/third_party/blink/renderer/modules/breakout_box/transferred_frame_queue_underlying_source.cc
[modify] https://crrev.com/fefd6198da317344f24d1c16ec9670cf0e93793e/third_party/blink/renderer/modules/breakout_box/frame_queue_underlying_source.h


### ad...@google.com (2022-09-21)

benjaminwagner@

https://crbug.com/chromium/1323488#c37 notes that the original report is a null pointer dereference, which we don't consider exploitable. But points 1-2 in your CL message strongly suggest that this can sometimes manifest as a UaF. Do you agree? If so the current severity is right.

We'll plan to include it in M106 release notes until/unless we become sure it's always a null pointer.

### ad...@google.com (2022-09-21)

[Empty comment from Monorail migration]

### be...@google.com (2022-09-21)

@adetaylor@google.com, IIRC, all three issues were UAF. In fact, IIUC, the code always handles the case of a null pointer correctly; the issue arises because the CTP is set to null a short time after the object is destroyed. (mlippautz@chromium.org would be able to confirm.)

### ml...@chromium.org (2022-09-21)

Re https://crbug.com/chromium/1323488#c41: I think we clear the CTP before we remove the object but you may read out the raw pointer from the CTP which gets cleared immediately afterwards. So, this should be a UAF in the worst case.

### am...@google.com (2022-09-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ho...@chromium.org (2022-09-22)

[Empty comment from Monorail migration]

[Monorail components: -Blink>WebAudio]

### am...@chromium.org (2022-09-22)

Congratulations! The VRP Panel has decided to award you $3,000 for this report of this moderately mitigated (https://g.co/chrome/vrp) security bug based on the very tight/difficult race condition for this to result in a uaf versus a null pointer deref and the evidence of both reports of this issue being of the null pointer vs the uaf. Thank you for your efforts in reporting this issue to us! 

### am...@google.com (2022-09-23)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-27)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-12-20)

This issue was migrated from crbug.com/chromium/1323488?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/chromium/1356185]
[Monorail mergedwith: crbug.com/chromium/1337806, crbug.com/chromium/1356185]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059591)*
