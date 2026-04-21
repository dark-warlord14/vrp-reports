# use after poison inMediaStreamAudioTrack::StopAndNotify

| Field | Value |
|-------|-------|
| **Issue ID** | [40055544](https://issues.chromium.org/issues/40055544) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>MediaStream |
| **Platforms** | Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | gu...@chromium.org |
| **Created** | 2021-04-14 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36

Steps to reproduce the problem:
Operating System:Ubuntu 20.04
Chrome version:
Chromium 92.0.4477.0 (gs://chromium-browser-asan/linux-release/asan-linux-release-872230.zip)
Chromium 91.0.4469.4 Dev (asan build)
args.gn
is_asan = true
is_debug = false
enable_nacl = false
treat_warnings_as_errors = false
#dcheck_always_on=true
is_component_build=false

./chrome --js-flags=--expose-gc --use-fake-device-for-media-stream --enable-experimental-web-platform-features http://localhost:8000/crash.html

What is the expected behavior?

What went wrong?
=================================================================
==1==ERROR: AddressSanitizer: use-after-poison on address 0x7e8646621ec0 at pc 0x563d7bba84ac bp 0x7ffcbcc79e50 sp 0x7ffcbcc79e48
READ of size 8 at 0x7e8646621ec0 thread T0 (chrome)
    #0 0x563d7bba84ab in blink::MediaStreamAudioTrack::StopAndNotify(base::OnceCallback<void ()>) ./../../third_party/blink/renderer/platform/mediastream/media_stream_audio_track.cc:129
    #1 0x563d7bba84ab in ?? ??:0
    #2 0x563d7bba5ff2 in blink::MediaStreamAudioTrack::~MediaStreamAudioTrack() ./../../third_party/blink/renderer/platform/mediastream/media_stream_track_platform.h:75
    #3 0x563d7bba5ff2 in ~MediaStreamAudioTrack ./../../third_party/blink/renderer/platform/mediastream/media_stream_audio_track.cc:38
    #4 0x563d7bba5ff2 in ?? ??:0
    #5 0x563d7bba643d in blink::MediaStreamAudioTrack::~MediaStreamAudioTrack() ./../../third_party/blink/renderer/platform/mediastream/media_stream_audio_track.cc:35
    #6 0x563d7bba643d in ?? ??:0
    #7 0x563d7bb85dfb in blink::MediaStreamComponent::InvokePreFinalizer(blink::LivenessBroker const&, void*) ./../../buildtools/third_party/libc++/trunk/include/memory:1335
    #8 0x563d7bb85dfb in reset ./../../buildtools/third_party/libc++/trunk/include/memory:1596
    #9 0x563d7bb85dfb in Dispose ./../../third_party/blink/renderer/platform/mediastream/media_stream_component.cc:72
    #10 0x563d7bb85dfb in InvokePreFinalizer ./../../third_party/blink/renderer/platform/mediastream/media_stream_component.h:57
    #11 0x563d7bb85dfb in ?? ??:0
    #12 0x563d6a539eda in blink::ThreadState::InvokePreFinalizers() ./../../third_party/blink/renderer/platform/heap/impl/thread_state.cc:986
    #13 0x563d6a539eda in ?? ??:0
    #14 0x563d6a53dea1 in blink::ThreadState::AtomicPauseSweepAndCompact(blink::BlinkGC::CollectionType, blink::BlinkGC::MarkingType, blink::BlinkGC::SweepingType) ./../../third_party/blink/renderer/platform/heap/impl/thread_state.cc:1306
    #15 0x563d6a53dea1 in ?? ??:0
    #16 0x563d6a541bc7 in blink::UnifiedHeapController::TraceEpilogue(v8::EmbedderHeapTracer::TraceSummary*) ./../../third_party/blink/renderer/platform/heap/impl/unified_heap_controller.cc:93
    #17 0x563d6a541bc7 in ?? ??:0
    #18 0x563d68521a12 in v8::internal::LocalEmbedderHeapTracer::TraceEpilogue() ./../../v8/src/heap/embedder-tracing.cc:36
    #19 0x563d68521a12 in ?? ??:0
    #20 0x563d685a72de in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:2091
    #21 0x563d685a72de in ?? ??:0
    #22 0x563d6859ea82 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:1632
    #23 0x563d6859ea82 in ?? ??:0
    #24 0x563d685b9362 in v8::internal::Heap::FinalizeIncrementalMarkingIfComplete(v8::internal::GarbageCollectionReason) ./../../v8/src/heap/heap.cc:1316
    #25 0x563d685b9362 in FinalizeIncrementalMarkingIfComplete ./../../v8/src/heap/heap.cc:3468
    #26 0x563d685b9362 in ?? ??:0
    #27 0x563d685f98ca in v8::internal::IncrementalMarkingJob::Task::RunInternal() ./../../v8/src/heap/incremental-marking-job.cc:90
    #28 0x563d685f98ca in RunInternal ./../../v8/src/heap/incremental-marking-job.cc:128
    #29 0x563d685f98ca in ?? ??:0
    #30 0x563d6bd15096 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/callback.h:101
    #31 0x563d6bd15096 in RunTask ./../../base/task/common/task_annotator.cc:168
    #32 0x563d6bd15096 in ?? ??:0
    #33 0x563d6bd50937 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:351
    #34 0x563d6bd50937 in ?? ??:0
    #35 0x563d6bd50164 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:264
    #36 0x563d6bd50164 in ?? ??:0
    #37 0x563d6bc0b8c0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39
    #38 0x563d6bc0b8c0 in ?? ??:0
    #39 0x563d6bd51a5c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:460
    #40 0x563d6bd51a5c in ?? ??:0
    #41 0x563d6bc92df1 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:133
    #42 0x563d6bc92df1 in ?? ??:0
    #43 0x563d8068e2f4 in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:264
    #44 0x563d8068e2f4 in ?? ??:0
    #45 0x563d6b9e5daa in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:556
    #46 0x563d6b9e5daa in ?? ??:0
    #47 0x563d6b9e8f2e in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:947
    #48 0x563d6b9e8f2e in ?? ??:0
    #49 0x563d6b9e3426 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) ./../../content/app/content_main.cc:372
    #50 0x563d6b9e3426 in ?? ??:0
    #51 0x563d6b9e397c in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:398
    #52 0x563d6b9e397c in ?? ??:0
    #53 0x563d5f47f947 in ChromeMain ./../../chrome/app/chrome_main.cc:141
    #54 0x563d5f47f947 in ?? ??:0
    #55 0x7fee5ff3d0b2 in __libc_start_main ??:?
    #56 0x7fee5ff3d0b2 in ?? ??:0

Address 0x7e8646621ec0 is a wild pointer.
SUMMARY: AddressSanitizer: use-after-poison (/home/exp0/asan-linux-release/chrome+0x271db4ab)
Shadow bytes around the buggy address:
  0x0fd148cbc380: f7 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fd148cbc390: 00 00 f7 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fd148cbc3a0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fd148cbc3b0: 00 00 00 00 00 f7 00 00 00 00 00 00 00 00 00 00
  0x0fd148cbc3c0: 00 00 00 00 00 00 00 00 00 00 00 f7 f7 f7 f7 f7
=>0x0fd148cbc3d0: f7 f7 f7 f7 f7 f7 f7 f7[f7]f7 f7 f7 f7 f7 f7 f7
  0x0fd148cbc3e0: f7 f7 f7 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fd148cbc3f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fd148cbc400: f7 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fd148cbc410: 00 00 00 00 00 00 00 f7 00 00 00 00 00 00 00 00
  0x0fd148cbc420: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==1==ABORTING
Received signal 6

Did this work before? N/A 

Chrome version: 91.0.4469.4  Channel: dev
OS Version: 20.04
Flash Version:

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 414 B)
- [testharness.js](attachments/testharness.js) (text/plain, 151.3 KB)

## Timeline

### [Deleted User] (2021-04-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-04-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5170475949686784.

### es...@chromium.org (2021-04-17)

Looks like Clusterfuzz wasn't able to reproduce this. Are there any other instructions that might help us reproduce this?

Marking as Security_Impact-None if --enable-experimental-web-platform-features is required to repro.

[Monorail components: Blink>MediaStream]

### gu...@chromium.org (2021-04-17)

The report is using a feature currently on origin trial (MediaStreamTrackProcessor). I'll take a look

### em...@gmail.com (2021-04-19)

#3.
I tested again with latest canary(Version 92.0.4482.0 (Developer Build) (64-bit)),and still repro stably.
The repro way is very simple. I don't have  any other instructions right now.

### gu...@chromium.org (2021-04-19)

[Empty comment from Monorail migration]

### gu...@chromium.org (2021-04-19)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-04-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/52639de9834b8f545e0b4ef4a01c674415fb8d1e

commit 52639de9834b8f545e0b4ef4a01c674415fb8d1e
Author: Guido Urdaneta <guidou@chromium.org>
Date: Mon Apr 19 21:27:03 2021

[BreakoutBox] Add prefinalizer to MediaStreamAudioTrackUnderlyingSource

The prefinalizer ensures the underlying source is disconnected from the
track when the source is marked for garbage collection.
Failing to do this can lead to crash in cases where the platform track
needs to access its sinks in its own cleanup after GC.

Video does not suffer from this bug because the platform track in that
case does not access its sinks during cleanup. This CL adds a test for
video anyway to prevent future regressions.

Fixed: 1198854
Change-Id: I2a05c0f4f8e5959fb637fc991bef0f9da629fe90
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2835750
Auto-Submit: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Thomas Guilbert <tguilbert@chromium.org>
Reviewed-by: Thomas Guilbert <tguilbert@chromium.org>
Cr-Commit-Position: refs/heads/master@{#873977}

[modify] https://crrev.com/52639de9834b8f545e0b4ef4a01c674415fb8d1e/third_party/blink/renderer/modules/breakout_box/media_stream_audio_track_underlying_source.h
[modify] https://crrev.com/52639de9834b8f545e0b4ef4a01c674415fb8d1e/third_party/blink/renderer/modules/breakout_box/media_stream_audio_track_underlying_source_test.cc
[modify] https://crrev.com/52639de9834b8f545e0b4ef4a01c674415fb8d1e/third_party/blink/renderer/modules/breakout_box/media_stream_video_track_underlying_source_test.cc


### gi...@appspot.gserviceaccount.com (2021-04-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f40ca0686cf6f85e83e883c5c342b892491f6e32

commit f40ca0686cf6f85e83e883c5c342b892491f6e32
Author: Guido Urdaneta <guidou@chromium.org>
Date: Tue Apr 20 06:00:13 2021

Revert "[BreakoutBox] Add prefinalizer to MediaStreamAudioTrackUnderlyingSource"

This reverts commit 52639de9834b8f545e0b4ef4a01c674415fb8d1e.

Reason for revert: Easier merging of alternative fix.

Original change's description:
> [BreakoutBox] Add prefinalizer to MediaStreamAudioTrackUnderlyingSource
>
> The prefinalizer ensures the underlying source is disconnected from the
> track when the source is marked for garbage collection.
> Failing to do this can lead to crash in cases where the platform track
> needs to access its sinks in its own cleanup after GC.
>
> Video does not suffer from this bug because the platform track in that
> case does not access its sinks during cleanup. This CL adds a test for
> video anyway to prevent future regressions.
>
> Fixed: 1198854
> Change-Id: I2a05c0f4f8e5959fb637fc991bef0f9da629fe90
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2835750
> Auto-Submit: Guido Urdaneta <guidou@chromium.org>
> Commit-Queue: Thomas Guilbert <tguilbert@chromium.org>
> Reviewed-by: Thomas Guilbert <tguilbert@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#873977}

Change-Id: I50791935d5954979da1fc5029d7ee9312a3481ff
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2837967
Auto-Submit: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#874146}

[modify] https://crrev.com/f40ca0686cf6f85e83e883c5c342b892491f6e32/third_party/blink/renderer/modules/breakout_box/media_stream_audio_track_underlying_source.h
[modify] https://crrev.com/f40ca0686cf6f85e83e883c5c342b892491f6e32/third_party/blink/renderer/modules/breakout_box/media_stream_audio_track_underlying_source_test.cc
[modify] https://crrev.com/f40ca0686cf6f85e83e883c5c342b892491f6e32/third_party/blink/renderer/modules/breakout_box/media_stream_video_track_underlying_source_test.cc


### gu...@chromium.org (2021-04-20)

[Empty comment from Monorail migration]

### em...@gmail.com (2021-04-20)

I tested with latest build 874136, and never repro this issue.

### gu...@chromium.org (2021-04-20)

r873977 fixed it, but we'll land a better fix later today.
I reverted the original fix so that the new fix is easier to merge back.

### gi...@appspot.gserviceaccount.com (2021-04-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ec8a80f06016f8ed026755b531f6c30d25efe6bd

commit ec8a80f06016f8ed026755b531f6c30d25efe6bd
Author: Guido Urdaneta <guidou@chromium.org>
Date: Thu Apr 22 07:03:38 2021

[BreakoutBox] Disconnect audio underlying source on GC/ContextDestroyed()

This CL:
1. Adds a prefinalizer to disconnect the underlying source from the
track when the underlying source is marked for GC. Failing to do this
can lead to crashes in cases where the MediaStreamAudioTrack needs to
access its sinks in its own cleanup after GC.
2. Overrides
MediaStreamAudioTrackUnderlyingSource::ContextDestroyed() to ensure
that the underlying source is disconnected from the track when the
execution context is destroyed. This ensures that the object is reset
when the execution context is gone (and the prefinalizer becomes a no-op
in this case).

Video does not need this because MediaStreamVideoTrack
does not access its sinks during cleanup. This CL adds a test for
video anyway to prevent future regressions.

Fixed: 1198854
Change-Id: I07f513d218cd533280540bbc8f0dfbdfa7e46d26
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2837970
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Reviewed-by: Thomas Guilbert <tguilbert@chromium.org>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Cr-Commit-Position: refs/heads/master@{#875039}

[modify] https://crrev.com/ec8a80f06016f8ed026755b531f6c30d25efe6bd/third_party/blink/renderer/modules/breakout_box/media_stream_audio_track_underlying_source.cc
[modify] https://crrev.com/ec8a80f06016f8ed026755b531f6c30d25efe6bd/third_party/blink/renderer/modules/breakout_box/media_stream_audio_track_underlying_source.h
[modify] https://crrev.com/ec8a80f06016f8ed026755b531f6c30d25efe6bd/third_party/blink/renderer/modules/breakout_box/media_stream_audio_track_underlying_source_test.cc
[modify] https://crrev.com/ec8a80f06016f8ed026755b531f6c30d25efe6bd/third_party/blink/renderer/modules/breakout_box/media_stream_video_track_underlying_source_test.cc


### gu...@chromium.org (2021-04-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-23)

This bug requires manual review: Reverts referenced in bugdroid comments after merge request.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), kbleicher@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gu...@chromium.org (2021-04-23)

1. Does your merge fit within the Merge Decision Guidelines?
Yes. Security fix.

2. Links to the CLs you are requesting to merge.
r875039

3. Has the change landed and been verified on ToT?
Yes

4. Does this change need to be merged into other active release branches (M-1, M+1)?
It would be good to merge to M90, although the code involved is active only on origin trial.

5. Why are these changes required in this milestone after branch?
We learned about this bug after branch.

6. Is this a new feature?
No.

7. If it is a new feature, is it behind a flag using finch?
N/A

### pb...@google.com (2021-04-26)

Approving the change to M91 Branch : 4472, Please go ahead and merge the CL to branch 4472 (/refs/branch-heads/4472) manually asap so that it would be part of next week's Beta release.


+Adetaylor(Security TPM) as fyi

### gi...@appspot.gserviceaccount.com (2021-04-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0112488f84305098aaa6eb82eb7187ef50f29b02

commit 0112488f84305098aaa6eb82eb7187ef50f29b02
Author: Guido Urdaneta <guidou@chromium.org>
Date: Tue Apr 27 15:21:31 2021

[M91][BreakoutBox] Disconnect audio underlying source on GC/ContextDestroyed()

This CL:
1. Adds a prefinalizer to disconnect the underlying source from the
track when the underlying source is marked for GC. Failing to do this
can lead to crashes in cases where the MediaStreamAudioTrack needs to
access its sinks in its own cleanup after GC.
2. Overrides
MediaStreamAudioTrackUnderlyingSource::ContextDestroyed() to ensure
that the underlying source is disconnected from the track when the
execution context is destroyed. This ensures that the object is reset
when the execution context is gone (and the prefinalizer becomes a no-op
in this case).

Video does not need this because MediaStreamVideoTrack
does not access its sinks during cleanup. This CL adds a test for
video anyway to prevent future regressions.

(cherry picked from commit ec8a80f06016f8ed026755b531f6c30d25efe6bd)

Fixed: 1198854
Change-Id: I07f513d218cd533280540bbc8f0dfbdfa7e46d26
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2837970
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Reviewed-by: Thomas Guilbert <tguilbert@chromium.org>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#875039}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2853359
Reviewed-by: Elad Alon <eladalon@chromium.org>
Cr-Commit-Position: refs/branch-heads/4472@{#466}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/0112488f84305098aaa6eb82eb7187ef50f29b02/third_party/blink/renderer/modules/mediastream/media_stream_audio_track_underlying_source.cc
[modify] https://crrev.com/0112488f84305098aaa6eb82eb7187ef50f29b02/third_party/blink/renderer/modules/mediastream/media_stream_audio_track_underlying_source.h
[modify] https://crrev.com/0112488f84305098aaa6eb82eb7187ef50f29b02/third_party/blink/renderer/modules/mediastream/media_stream_audio_track_underlying_source_test.cc
[modify] https://crrev.com/0112488f84305098aaa6eb82eb7187ef50f29b02/third_party/blink/renderer/modules/mediastream/media_stream_video_track_underlying_source_test.cc


### am...@chromium.org (2021-04-28)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-04-28)

Congratulations! The VRP Panel has decided to award you $5000 for this report. Nice work! 

### am...@google.com (2021-04-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-01-05)

Hello OP/emilykim@, we consider attachments/pocs included with reports to be an integral part of the report (https://bughunters.google.com/about/rules/5745167867576320), so I've undeleted them. Thank you! 

### is...@google.com (2022-01-05)

This issue was migrated from crbug.com/chromium/1198854?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-27)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/chrome-blintz-user-guide

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055544)*
