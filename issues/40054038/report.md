# use after poison in content::InspectorMediaEventHandler::SendQueuedMediaEvents

| Field | Value |
|-------|-------|
| **Issue ID** | [40054038](https://issues.chromium.org/issues/40054038) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Media |
| **Platforms** | Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | tg...@chromium.org |
| **Created** | 2020-12-02 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36

Steps to reproduce the problem:
os version:
ubuntu 20.04

reproduced version:
Chromium 89.0.4336.0 
Chromium 88.0.4324.11 

not reproduced with this version:
Chromium88.0.4315.5

For stable reproduction, more than 5 URLs need to be opened.
google-chrome --js-flags=--expose-gc --enable-experimental-web-platform-features --user-data-dir=/tmp/nonono http://localhost:8000/crash.html  http://localhost:8000/crash.html  http://localhost:8000/crash.html  http://localhost:8000/crash.html  http://localhost:8000/crash.html  http://localhost:8000/crash.html  http://localhost:8000/crash.html

What is the expected behavior?

What went wrong?
==1==ERROR: AddressSanitizer: use-after-poison on address 0x7ee63527da80 at pc 0x5639a6cc58cf bp 0x7ffc87dd2310 sp 0x7ffc87dd2308
READ of size 8 at 0x7ee63527da80 thread T0 (chrome)
error: unknown argument '--demangle=True'
    #0 0x5639a6cc58ce in content::InspectorMediaEventHandler::SendQueuedMediaEvents(std::__1::vector<media::MediaLogRecord, std::__1::allocator<media::MediaLogRecord> >) ./../../content/renderer/media/inspector_media_event_handler.cc:100
    #1 0x5639a6cc58ce in ?? ??:0
    #2 0x5639a6cb9c64 in content::BatchingMediaLog::SendQueuedMediaEvents() ./../../content/renderer/media/batching_media_log.cc:231
    #3 0x5639a6cb9c64 in ?? ??:0
    #4 0x5639a6cb92e4 in content::BatchingMediaLog::~BatchingMediaLog() ./../../content/renderer/media/batching_media_log.cc:80
    #5 0x5639a6cb92e4 in ?? ??:0
    #6 0x5639a6cb9fbd in content::BatchingMediaLog::~BatchingMediaLog() ./../../content/renderer/media/batching_media_log.cc:70
    #7 0x5639a6cb9fbd in ?? ??:0
    #8 0x563993fe4e1f in blink::NormalPage::ToBeFinalizedObject::Finalize() ./../../third_party/blink/renderer/platform/heap/impl/heap_page.cc:95
    #9 0x563993fe4e1f in Finalize ./../../third_party/blink/renderer/platform/heap/impl/heap_page.cc:1403
    #10 0x563993fe4e1f in ?? ??:0
    #11 0x563993fe62ab in blink::NormalPage::Sweep(blink::FinalizeType) ./../../third_party/blink/renderer/platform/heap/impl/heap_page.cc:1514
    #12 0x563993fe62ab in ?? ??:0
    #13 0x563993fdbf96 in blink::BaseArena::SweepUnsweptPage(blink::BasePage*) ./../../third_party/blink/renderer/platform/heap/impl/heap_page.cc:311
    #14 0x563993fdbf96 in ?? ??:0
    #15 0x563993fddbd1 in blink::BaseArena::CompleteSweep() ./../../third_party/blink/renderer/platform/heap/impl/heap_page.cc:407
    #16 0x563993fddbd1 in ?? ??:0
    #17 0x563993fcb3b4 in blink::ThreadHeap::CompleteSweep() ./../../third_party/blink/renderer/platform/heap/impl/heap.cc:709
    #18 0x563993fcb3b4 in ?? ??:0
    #19 0x563993ffb7a7 in blink::ThreadState::CompleteSweep() ./../../third_party/blink/renderer/platform/heap/impl/thread_state.cc:760
    #20 0x563993ffb7a7 in ?? ??:0
    #21 0x563994008dee in blink::ThreadState::AtomicPauseSweepAndCompact(blink::BlinkGC::CollectionType, blink::BlinkGC::MarkingType, blink::BlinkGC::SweepingType) ./../../third_party/blink/renderer/platform/heap/impl/thread_state.cc:1415
    #22 0x563994008dee in ?? ??:0
    #23 0x56399400de27 in blink::UnifiedHeapController::TraceEpilogue(v8::EmbedderHeapTracer::TraceSummary*) ./../../third_party/blink/renderer/platform/heap/impl/unified_heap_controller.cc:92
    #24 0x56399400de27 in ?? ??:0
    #25 0x563992090762 in v8::internal::LocalEmbedderHeapTracer::TraceEpilogue() ./../../v8/src/heap/embedder-tracing.cc:35
    #26 0x563992090762 in ?? ??:0
    #27 0x563992117710 in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:2027
    #28 0x563992117710 in ?? ??:0
    #29 0x56399210f8a3 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:1617
    #30 0x56399210f8a3 in ?? ??:0
    #31 0x5639921142bb in v8::internal::Heap::PreciseCollectAllGarbage(int, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:1306
    #32 0x5639921142bb in PreciseCollectAllGarbage ./../../v8/src/heap/heap.cc:1441
    #33 0x5639921142bb in ?? ??:0
    #34 0x563993ffff47 in blink::ThreadState::CollectAllGarbageForTesting(blink::BlinkGC::StackState) ./../../third_party/blink/renderer/platform/heap/impl/thread_state.cc:1680
    #35 0x563993ffff47 in ?? ??:0
    #36 0x563994004132 in blink::ThreadState::SafePoint(blink::BlinkGC::StackState) ./../../third_party/blink/renderer/platform/heap/impl/thread_state.cc:656
    #37 0x563994004132 in SafePoint ./../../third_party/blink/renderer/platform/heap/impl/thread_state.cc:965
    #38 0x563994004132 in ?? ??:0
    #39 0x56399528c38c in base::sequence_manager::internal::SequenceManagerImpl::NotifyDidProcessTask(base::sequence_manager::internal::SequenceManagerImpl::ExecutingTask*, base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/sequence_manager_impl.cc:866
    #40 0x56399528c38c in ?? ??:0
    #41 0x56399528b83c in base::sequence_manager::internal::SequenceManagerImpl::DidRunTask() ./../../base/task/sequence_manager/sequence_manager_impl.cc:668
    #42 0x56399528b83c in ?? ??:0
    #43 0x5639952ba6bd in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356
    #44 0x5639952ba6bd in ?? ??:0
    #45 0x5639952b9d34 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:264
    #46 0x5639952b9d34 in ?? ??:0
    #47 0x5639951a74c0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39
    #48 0x5639951a74c0 in ?? ??:0
    #49 0x5639952bc5ac in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:460
    #50 0x5639952bc5ac in ?? ??:0
    #51 0x56399522ab50 in base::RunLoop::Run() ./../../base/run_loop.cc:131
    #52 0x56399522ab50 in ?? ??:0
    #53 0x5639a89a73be in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:256
    #54 0x5639a89a73be in ?? ??:0
    #55 0x563994f8a229 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:498
    #56 0x563994f8a229 in ?? ??:0
    #57 0x563994f8d559 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:887
    #58 0x563994f8d559 in ?? ??:0
    #59 0x563994f876be in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) ./../../content/app/content_main.cc:372
    #60 0x563994f876be in ?? ??:0
    #61 0x563994f87cac in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:398
    #62 0x563994f87cac in ?? ??:0
    #63 0x56398a0f6337 in ChromeMain ./../../chrome/app/chrome_main.cc:130
    #64 0x56398a0f6337 in ?? ??:0
error: unknown argument '--demangle=True'
    #65 0x7ff88eea40b2 in __libc_start_main ??:?
    #66 0x7ff88eea40b2 in ?? ??:0

Address 0x7ee63527da80 is a wild pointer.
SUMMARY: AddressSanitizer: use-after-poison (/home/pwn/asan-linux-release/chrome+0x26e718ce)
Shadow bytes around the buggy address:
  0x0fdd46a47b00: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdd46a47b10: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdd46a47b20: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdd46a47b30: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdd46a47b40: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
=>0x0fdd46a47b50:[f7]f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdd46a47b60: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdd46a47b70: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdd46a47b80: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdd46a47b90: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdd46a47ba0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
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

Did this work before? N/A 

Chrome version: Chromium 88.0.4324.11   Channel: dev
OS Version: 20.04
Flash Version:

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 204 B)
- [crash2.html](attachments/crash2.html) (text/plain, 392 B)
- [empty-sw.js](attachments/empty-sw.js) (text/plain, 0 B)
- [testharness.js](attachments/testharness.js) (text/plain, 141.4 KB)
- [main.html](attachments/main.html) (text/plain, 228 B)
- [poc.html](attachments/poc.html) (text/plain, 409 B)

## Timeline

### [Deleted User] (2020-12-02)

[Empty comment from Monorail migration]

### es...@chromium.org (2020-12-02)

Setting to Security_Impact-None because it doesn't sound like it affects Chrome by default (without --enable-experimental-web-platform-features enabled).

Adding some media owners to please take a look.

[Monorail components: Blink>Media]

### es...@chromium.org (2020-12-02)

trying this again...

### ch...@chromium.org (2020-12-02)

> Setting to Security_Impact-None because it doesn't sound like it affects Chrome by default (without --enable-experimental-web-platform-features enabled).

We're actively doing an origin trial for WebCodecs (enabled by that flag), so there is possibility of users seeing this on sites that enroll for the trial. 

### ch...@chromium.org (2020-12-02)

At a glance, it looks like a racecondition using MediaLog w/ VideoDecoder.

### da...@chromium.org (2020-12-02)

Tagging with M-89 since this just landed.

### tg...@chromium.org (2020-12-02)

This might have been introduced by neutering the log when there is an error, from this CL:
https://chromium-review.googlesource.com/c/chromium/src/+/2538964/10/third_party/blink/renderer/modules/webcodecs/decoder_template.cc#427

### tg...@chromium.org (2020-12-02)

Calling InvalidateLog() instead of deleting the parent_media_log might be the fix.

### tg...@chromium.org (2020-12-02)

Actually, I'm not sure about C#8. I need to look into this deeper.

### tg...@chromium.org (2020-12-02)

Actually, I can't get this to repro. Could you share the build flags you used for your asan build and any extra ASAN_OPTIONS?

Also, the CL in C#7 landed in 89.0.4338.0, whereas this bug was reproduced on 89.0.4336.0. So, that CL is not responsible for making things worse.

### em...@gmail.com (2020-12-02)

I tested with two ways
1.download asan build canary:
Chromium 89.0.4342.0:
gsutil cp gs://chromium-browser-asan/linux-release/asan-linux-release-831814.zip .

2.build dev version with asan:
is_asan = true
is_debug = false
enable_nacl = false
treat_warnings_as_errors = false
is_component_build=false


### da...@chromium.org (2020-12-03)

This could be https://crbug.com/chromium/1148729 then if it's not your changes Thomas.

### tg...@chromium.org (2020-12-03)

I've tried both ways, and I'm still not getting a repro. Can someone else try on their machines?

I wondered if my machine was too powerful, so I tried opening dozens of tabs at once, but that didn't help. I wondered if I didn't build properly, but the ASAN basic check works (https://chromium.googlesource.com/chromium/src/+/master/docs/asan.md#verify-the-asan-tool-works)

I'm using "python -m SimpleHTTPServer 8000" to serve the test pages.

### tm...@chromium.org (2020-12-03)

Is it possible that there's a demangling issue here? It looks like inspector_media_event_handler.cc:100 is the source of the crash which would mean that InspectorMediaEventHandler::inspector_context_ has been freed, but it could just be missing some even earlier frames where https://crbug.com/chromium/1148729 is at fault.

### em...@gmail.com (2020-12-03)

I made a new poc that can stably reproduce the crash.
I tested with Google Chrome 88.0.4324.11 dev(office build non asan version) and latest canary version().
In local test, I found that it can be reproduced quickly in the none asan version(Google Chrome 88.0.4324.11 dev), and it takes about 10 seconds in the Asan version.
I think the new POC should be able to reproduce stably on all kinds of machines with different performance.
repro step:
There is no need to open multiple URLs
./chrome --enable-experimental-web-platform-features http://localhost:8000/main.html

### tg...@chromium.org (2020-12-03)

Thanks a lot! I do easily get a crash now.

### tg...@chromium.org (2020-12-03)

I logged whether or not the CodecLogger was neutered when it is destroyed. Crashes seemed to happen immediately after (or rather during) and un-neutered CodecLogger's destruction.

Adding a prefinalizer that neuters the CodecLogger fixed the issue, and logged if the neutering happened from the prefinalizer or the OnContextDestroyed(). The vast majority of time, we neuter through the OnContextDestroyed(), a few times through the prefinalizer. I assume that, of those few times, some of them would crash.

It turns out that we create CodecLoggers with already destroyed contexts sometimes (according to IsContextDestroyed()).

Checking for:

  if (!context->IsContextDestroyed()){
    parent_media_log_ = Platform::Current()->GetMediaLog(
        MediaInspectorContextImpl::From(*context), task_runner);
  }

In the CodecLogger constructor fixes the issue. Should we be instead preventing the creation of VideoDecoders etc. when the context is being destroyed somehow?

+dcheng@ for advice.

### tg...@chromium.org (2020-12-08)

dcheng@ and I discussed offline yesterday that the proposed fix in C#17 was fine. CL out here:
https://chromium-review.googlesource.com/c/chromium/src/+/2580478

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0774fed95e764dc8744fe82e8a050ccba3ffc139

commit 0774fed95e764dc8744fe82e8a050ccba3ffc139
Author: Thomas Guilbert <tguilbert@chromium.org>
Date: Thu Dec 10 22:05:00 2020

Prevent log creation in detached context

This CL fixes a race condition in which a MediaLog could be created in
a context that is already destroyed. See the attached bug for more
details.

Bug: 1154468
Change-Id: I26ae0c621d9a4557d224ca77f696ad3ce53b41c7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2580478
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Thomas Guilbert <tguilbert@chromium.org>
Auto-Submit: Thomas Guilbert <tguilbert@chromium.org>
Cr-Commit-Position: refs/heads/master@{#835842}

[modify] https://crrev.com/0774fed95e764dc8744fe82e8a050ccba3ffc139/third_party/blink/renderer/modules/webcodecs/codec_logger.cc


### tg...@chromium.org (2020-12-10)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-11)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-12)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-16)

Setting Secuity_Impact-Head per https://crbug.com/chromium/1154468#c4.

### ad...@google.com (2020-12-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-12-17)

Congratulations, the VRP panel has decided to award $5000 for this.

### [Deleted User] (2020-12-17)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-12-17)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-03-29)

@emilykim - we consider attachments/pocs included with reports to be an integral part of the report, so I've un-deleted them. Thanks!

### is...@google.com (2021-03-29)

This issue was migrated from crbug.com/chromium/1154468?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054038)*
