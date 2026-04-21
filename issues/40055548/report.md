# use-after-poison in  blink::ImageDecoderExternal::OnMetadata

| Field | Value |
|-------|-------|
| **Issue ID** | [40055548](https://issues.chromium.org/issues/40055548) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Media>WebCodecs |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ne...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2021-04-14 |
| **Bounty** | $7,500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36

Steps to reproduce the problem:
Uuntu 20.04
tested chrome version
Chromium 92.0.4477.0
Chromium 91.0.4469.4

google-chrome --enable-experimental-web-platform-features  http://localhost:8000/main.html

What is the expected behavior?

What went wrong?
WRITE of size 1 at 0x7e936f0e27b1 thread T0 (chrome)
==1==WARNING: invalid path to external symbolizer!
==1==WARNING: Failed to use and restart external symbolizer!
error: unknown argument '--demangle=True'
    #0 0x56375a1d4df0 in blink::ImageDecoderExternal::OnMetadata(blink::ImageDecoderCore::ImageMetadata) ./../../third_party/blink/renderer/modules/webcodecs/image_decoder_external.cc:508
    #1 0x56375a1d4df0 in ?? ??:0
    #2 0x56375a1d5817 in base::internal::Invoker<base::internal::BindState<void (blink::ImageDecoderExternal::*)(blink::ImageDecoderCore::ImageMetadata), base::WeakPtr<blink::ImageDecoderExternal> >, void (blink::ImageDecoderCore::ImageMetadata)>::RunOnce(base::internal::BindStateBase*, blink::ImageDecoderCore::ImageMetadata&&) ./../../base/bind_internal.h:509
    #3 0x56375a1d5817 in MakeItSo<void (blink::ImageDecoderExternal::*)(blink::ImageDecoderCore::ImageMetadata), base::WeakPtr<blink::ImageDecoderExternal>, blink::ImageDecoderCore::ImageMetadata> ./../../base/bind_internal.h:668
    #4 0x56375a1d5817 in RunImpl<void (blink::ImageDecoderExternal::*)(blink::ImageDecoderCore::ImageMetadata), std::tuple<base::WeakPtr<blink::ImageDecoderExternal> >, 0> ./../../base/bind_internal.h:721
    #5 0x56375a1d5817 in RunOnce ./../../base/bind_internal.h:690
    #6 0x56375a1d5817 in ?? ??:0
    #7 0x56375a1db9b3 in void base::internal::ReplyAdapter<blink::ImageDecoderCore::ImageMetadata, blink::ImageDecoderCore::ImageMetadata>(base::OnceCallback<void (blink::ImageDecoderCore::ImageMetadata)>, std::__1::unique_ptr<blink::ImageDecoderCore::ImageMetadata, std::__1::default_delete<blink::ImageDecoderCore::ImageMetadata> >*) ./../../base/callback.h:101
    #8 0x56375a1db9b3 in ReplyAdapter<blink::ImageDecoderCore::ImageMetadata, blink::ImageDecoderCore::ImageMetadata> ./../../base/post_task_and_reply_with_result_internal.h:30
    #9 0x56375a1db9b3 in ?? ??:0
    #10 0x56375a1dbd76 in base::internal::Invoker<base::internal::BindState<void (*)(base::OnceCallback<void (blink::ImageDecoderCore::ImageMetadata)>, std::__1::unique_ptr<blink::ImageDecoderCore::ImageMetadata, std::__1::default_delete<blink::ImageDecoderCore::ImageMetadata> >*), base::OnceCallback<void (blink::ImageDecoderCore::ImageMetadata)>, base::internal::OwnedWrapper<std::__1::unique_ptr<blink::ImageDecoderCore::ImageMetadata, std::__1::default_delete<blink::ImageDecoderCore::ImageMetadata> >, std::__1::default_delete<std::__1::unique_ptr<blink::ImageDecoderCore::ImageMetadata, std::__1::default_delete<blink::ImageDecoderCore::ImageMetadata> > > > >, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:404
    #11 0x56375a1dbd76 in MakeItSo<void (*)(base::OnceCallback<void (blink::ImageDecoderCore::ImageMetadata)>, std::unique_ptr<blink::ImageDecoderCore::ImageMetadata> *), base::OnceCallback<void (blink::ImageDecoderCore::ImageMetadata)>, std::unique_ptr<blink::ImageDecoderCore::ImageMetadata> *> ./../../base/bind_internal.h:648
    #12 0x56375a1dbd76 in RunImpl<void (*)(base::OnceCallback<void (blink::ImageDecoderCore::ImageMetadata)>, std::unique_ptr<blink::ImageDecoderCore::ImageMetadata> *), std::tuple<base::OnceCallback<void (blink::ImageDecoderCore::ImageMetadata)>, base::internal::OwnedWrapper<std::unique_ptr<blink::ImageDecoderCore::ImageMetadata> > >, 0, 1> ./../../base/bind_internal.h:721
    #13 0x56375a1dbd76 in RunOnce ./../../base/bind_internal.h:690
    #14 0x56375a1dbd76 in ?? ??:0
    #15 0x563746930d22 in base::(anonymous namespace)::PostTaskAndReplyRelay::RunReply(base::(anonymous namespace)::PostTaskAndReplyRelay) ./../../base/callback.h:101
    #16 0x563746930d22 in RunReply ./../../base/threading/post_task_and_reply_impl.cc:115
    #17 0x563746930d22 in ?? ??:0
    #18 0x563746930f68 in base::internal::Invoker<base::internal::BindState<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:404
    #19 0x563746930f68 in MakeItSo<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay> ./../../base/bind_internal.h:648
    #20 0x563746930f68 in RunImpl<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay), std::tuple<base::(anonymous namespace)::PostTaskAndReplyRelay>, 0> ./../../base/bind_internal.h:721
    #21 0x563746930f68 in RunOnce ./../../base/bind_internal.h:690
    #22 0x563746930f68 in ?? ??:0
    #23 0x5637468ab290 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/callback.h:101
    #24 0x5637468ab290 in RunTask ./../../base/task/common/task_annotator.cc:173
    #25 0x5637468ab290 in ?? ??:0
    #26 0x5637468e505f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:351
    #27 0x5637468e505f in ?? ??:0
    #28 0x5637468e4834 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:264
    #29 0x5637468e4834 in ?? ??:0
    #30 0x5637467a6f30 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39
    #31 0x5637467a6f30 in ?? ??:0
    #32 0x5637468e61cc in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:460
    #33 0x5637468e61cc in ?? ??:0
    #34 0x56374682b0f1 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:133
    #35 0x56374682b0f1 in ?? ??:0
    #36 0x56375af92b60 in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:252
    #37 0x56375af92b60 in ?? ??:0
    #38 0x56374657d9f0 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:572
    #39 0x56374657d9f0 in ?? ??:0
    #40 0x563746580b5e in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:958
    #41 0x563746580b5e in ?? ??:0
    #42 0x56374657b176 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) ./../../content/app/content_main.cc:372
    #43 0x56374657b176 in ?? ??:0
    #44 0x56374657b6cc in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:398
    #45 0x56374657b6cc in ?? ??:0
    #46 0x5637393353db in ChromeMain ./../../chrome/app/chrome_main.cc:151
    #47 0x5637393353db in ?? ??:0
error: unknown argument '--demangle=True'
    #48 0x7fb0f1e910b2 in __libc_start_main ??:?
    #49 0x7fb0f1e910b2 in ?? ??:0

Address 0x7e936f0e27b1 is a wild pointer inside of access range of size 0x000000000001.
SUMMARY: AddressSanitizer: use-after-poison (/home/test/asan-linux-release/chrome+0x2bb2adf0)
Shadow bytes around the buggy address:
  0x0fd2ede144a0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd2ede144b0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd2ede144c0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd2ede144d0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd2ede144e0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
=>0x0fd2ede144f0: f7 f7 f7 f7 f7 f7[f7]f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd2ede14500: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd2ede14510: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd2ede14520: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd2ede14530: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd2ede14540: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
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

Chrome version: 91.0.4469.4  Channel: dev
OS Version: 20.04
Flash Version:

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 241 B)
- [main.html](attachments/main.html) (text/plain, 293 B)
- [asan-linux-release-874061-asan.log](attachments/asan-linux-release-874061-asan.log) (text/plain, 8.6 KB)

## Timeline

### [Deleted User] (2021-04-14)

[Empty comment from Monorail migration]

### es...@chromium.org (2021-04-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-04-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6197649322344448.

### es...@chromium.org (2021-04-17)

Looks like Clusterfuzz wasn't able to reproduce this. dalecurtis, could you please take a look? Marking as Security_Impact-None since it seems that this feature isn't shipped yet.

[Monorail components: Blink>Media>WebCodecs]

### da...@chromium.org (2021-04-17)

WebCodecs is in OT, so it's not Sec_Impact-None if it reproduces. 

If the stack is accurate this is pointing at:
https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/modules/webcodecs/image_decoder_external.cc;l=508

But as l.500 show, OnMetadata() is bound by WeakPtr. Since the reproduction doesn't use any threads, I don't see how we could end up in OnMetadata at a point where |data_complete_|  wouldn't be valid.

I'll keep looking next week.

### da...@chromium.org (2021-04-17)

I also am not able to reproduce on Windows or Linux + ASAN.

### ne...@gmail.com (2021-04-19)

In my local test, I can stably repro this issue. I tested again with latest canary( gsutil cp gs://chromium-browser-asan/linux-release/asan-linux-release-873679.zip).
Or you can try to add  more "<iframe src="./crash.html"></iframe>" to main.html.

### da...@chromium.org (2021-04-19)

Added 20-30 crash.html -- that reproduced the CHECK() failures from https://crbug.com/chromium/1199703, fixing that revealed a DCHECK() which was problematic, but still haven't been able to reproduce any use after free. 

### da...@chromium.org (2021-04-19)

dcheng pointed out that WeakPtrs need special consideration when used with GC'd objects, so that's like the issue here even though I can't reproduce.

### da...@chromium.org (2021-04-19)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-04-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ad9b81155c87e9801783023452776391ea265527

commit ad9b81155c87e9801783023452776391ea265527
Author: Dale Curtis <dalecurtis@chromium.org>
Date: Mon Apr 19 21:14:04 2021

[ImageDecoder] Invalidate WeakPtrs upon ExecutionContext loss.

WeakPtrs need special consideration when used with a garbage collected
type; they must be invalidated ahead of finalization.

We also need to ensure that no further WeakPtrs are created, so close()
the decoder during ContextDestroyed() to prevent further operation.

This also fixes a DCHECK() that was incorrectly firing during the
reproduction case.

R=jbroman

Fixed: 1198895
Change-Id: Ib3d108233fa30d47688a6fba395afaab99e151cc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2836831
Commit-Queue: Dale Curtis <dalecurtis@chromium.org>
Commit-Queue: Jeremy Roman <jbroman@chromium.org>
Auto-Submit: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Jeremy Roman <jbroman@chromium.org>
Cr-Commit-Position: refs/heads/master@{#873967}

[modify] https://crrev.com/ad9b81155c87e9801783023452776391ea265527/third_party/blink/renderer/modules/webcodecs/image_decoder_external.cc
[modify] https://crrev.com/ad9b81155c87e9801783023452776391ea265527/third_party/blink/renderer/modules/webcodecs/image_decoder_external_test.cc


### da...@chromium.org (2021-04-19)

@neklab2015: Can you try a build after 873967 and see if you can reproduce?

### da...@chromium.org (2021-04-19)

[Empty comment from Monorail migration]

### ne...@gmail.com (2021-04-20)

I tested with latest canary,and still can repro.
Attachment is asan log with 874061.
asan-linux-release-874061.zip(Version 92.0.4483.0 (Developer Build) (64-bit))


### [Deleted User] (2021-04-20)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-04-20)

@jbroman, dcheng: Is OnContextDestroyed() guaranteed to be called ahead of GC in all cases?

cc:guidou who is working on a similar issue. 

### da...@chromium.org (2021-04-20)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-04-20)

Still not able to reproduce on my side unfortunately.

cc: haraken who guidou@ is asking a similar question of.

### jb...@chromium.org (2021-04-20)

As long as an ActiveScriptWrappable reports itself as alive and its EC is not destroyed it shouldn't be GCed. So assuming it's still live, it should be alive. I believe the EC destroyed notifications are synchronous and so should happen before any GC.

### da...@chromium.org (2021-04-20)

I was just testing this and it appears not to be true. If I add a DCHECK(closed_) in the destructor, it's failing on the test case provided after the attempted fix. So the EC is not being destroyed before GC happens.

### da...@chromium.org (2021-04-20)

[22280:58324:0420/112952.497:FATAL:image_decoder_external.cc(193)] Check failed: closed_.
Backtrace:
        base::debug::CollectStackTrace [0x00007FFD6A5A9862+18] (o:\base\debug\stack_trace_win.cc:303)
        base::debug::StackTrace::StackTrace [0x00007FFD6A4877F2+18] (o:\base\debug\stack_trace.cc:195)
        logging::LogMessage::~LogMessage [0x00007FFD6A4A4EF3+131] (o:\base\logging.cc:590)
        logging::LogMessage::~LogMessage [0x00007FFD6A4A5E50+16] (o:\base\logging.cc:583)
        blink::ImageDecoderExternal::~ImageDecoderExternal [0x00007FFD3923C6FE+222] (o:\third_party\blink\renderer\modules\webcodecs\image_decoder_external.cc:194)
        blink::ImageDecoderExternal::~ImageDecoderExternal [0x00007FFD3923EA80+16] (o:\third_party\blink\renderer\modules\webcodecs\image_decoder_external.cc:191)
        blink::NormalPage::ToBeFinalizedObject::Finalize [0x00007FFD3A832FBD+141] (o:\third_party\blink\renderer\platform\heap\impl\heap_page.cc:1417)
        blink::NormalPage::FinalizeSweep [0x00007FFD3A833028+72] (o:\third_party\blink\renderer\platform\heap\impl\heap_page.cc:1422)
        blink::BaseArena::InvokeFinalizersOnSweptPages [0x00007FFD3A82E206+278] (o:\third_party\blink\renderer\platform\heap\impl\heap_page.cc:385)
        blink::BaseArena::CompleteSweep [0x00007FFD3A82E3D0+272] (o:\third_party\blink\renderer\platform\heap\impl\heap_page.cc:411)
        blink::ThreadHeap::CompleteSweep [0x00007FFD3A822BF8+56] (o:\third_party\blink\renderer\platform\heap\impl\heap.cc:707)
        blink::ThreadState::CompleteSweep [0x00007FFD3A83EB39+249] (o:\third_party\blink\renderer\platform\heap\impl\thread_state.cc:752)
        blink::NormalPageArena::OutOfLineAllocateImpl [0x00007FFD3A831EB0+400] (o:\third_party\blink\renderer\platform\heap\impl\heap_page.cc:957)
        blink::NormalPageArena::OutOfLineAllocate [0x00007FFD3A82C4CE+14] (o:\third_party\blink\renderer\platform\heap\impl\heap_page.cc:925)
        blink::ThreadHeap::AllocateOnArenaIndex [0x00007FFD3A44B3AB+411] (o:\third_party\blink\renderer\platform\heap\impl\heap.h:619)
        blink::ThreadHeap::Allocate<blink::ScriptWrappable> [0x00007FFD3878CFE3+101] (o:\third_party\blink\renderer\platform\heap\impl\heap.h:628)
        blink::MakeGarbageCollectedTrait<blink::ImageTrackList>::Call<blink::ImageDecoderExternal *> [0x00007FFD3923FDE6+34] (o:\third_party\blink\renderer\platform\heap\impl\heap.h:526)
        blink::ImageDecoderExternal::ImageDecoderExternal [0x00007FFD3923BAAA+250] (o:\third_party\blink\renderer\modules\webcodecs\image_decoder_external.cc:103)
        blink::MakeGarbageCollectedTrait<blink::ImageDecoderExternal>::Call<blink::ScriptState *&,const blink::ImageDecoderInit *&,blink::ExceptionState &> [0x00007FFD3923FCC7+63] (o:\third_party\blink\renderer\platform\heap\impl\heap.h:530)
        blink::ImageDecoderExternal::Create [0x00007FFD3923B713+51] (o:\third_party\blink\renderer\modules\webcodecs\image_decoder_external.cc:70)
        blink::`anonymous namespace'::v8_image_decoder::ConstructorCallback [0x00007FFD3889F0F7+423] (o:\fake\prefix\gen\third_party\blink\renderer\bindings\modules\v8\v8_image_decoder.cc:161)
        v8::internal::FunctionCallbackArguments::Call [0x00007FFD3EC3ADE7+631] (o:\v8\src\api\api-arguments-inl.h:157)
        v8::internal::`anonymous namespace'::HandleApiCallHelper<1> [0x00007FFD3EC38E5B+987] (o:\v8\src\builtins\builtins-api.cc:114)
        v8::internal::Builtin_Impl_HandleApiCall [0x00007FFD3EC37E76+374] (o:\v8\src\builtins\builtins-api.cc:138)
        v8::internal::Builtin_HandleApiCall [0x00007FFD3EC3794E+126] (o:\v8\src\builtins\builtins-api.cc:130)
        (No symbol) [0x0000589C00383C43]

### jb...@chromium.org (2021-04-20)

Can you check if HasPendingActivity() ever returned false?

### da...@chromium.org (2021-04-20)

Yes, it's expected that it returns false when there's no pending promises. So maybe that's where our misunderstanding is. HPA() isn't accounting for tasks posted on the sequence bound worker, only for user generated requests.

If we need HPA() to account for that I could use HasWeakPtrs() in HPA, but that seems dicey.

### jb...@chromium.org (2021-04-20)

If you need to object to stay alive without references elsewhere on the heap, then HasPendingActivity needs to return for as long as you need to prevent the object from being collected (and HPA effectively returns false once the ExecutionContext is destroyed, as an upper limit to this extension).

HasWeakPtrs seems like the wrong level of abstraction. I assume these workers post tasks back when they are complete? I would record in some way the tasks which have been issued but which may yet have need of the object and its WeakPtrFactory to be alive. If such activity might not correspond to an element of pending_decodes_ or pending_metadata_decodes_, then you'll need to have some condition that does express it.

### jb...@chromium.org (2021-04-20)

> then HasPendingActivity needs to return

return `true`, if it wasn't clear :)

### jb...@chromium.org (2021-04-20)

i.e., at the moment when !IsContextDestroyed() && HasPendingActivity() starts being false (and there are no GC roots that reach the object), there should probably either be no outstanding WeakPtrs or if they are they should be invalidated then, because past that point the GC makes no promise to preserve your heap object

### da...@chromium.org (2021-04-20)

I can certainly do that, but it would artificially extend the lifetime of the object. I think that's okay in this case since the only automatic task we'll execute is metadata decoding, which should be fairly cheap and the WeakPtr invalidation only prevents us from processing our queue (which should be empty if HPA() is false).

### jb...@chromium.org (2021-04-20)

If it's an artificial lifetime extension (i.e., the object doesn't really need to be alive anymore), then we shouldn't need the WeakPtr anymore and can invalidate it. Either extend the lifetime of the pointee (by returning true from HPA for longer) or shorten the validity of the pointers; either should work.

We just can't have an interval where the weak pointers are outstanding but the GC is free to collect.

### da...@chromium.org (2021-04-20)

Hmm, there's actually a fair few bits of work we automatically queue. I'd need to add state tracking for all of that which seems brittle. Is that really preferred over using a pre-finalizer?

### da...@chromium.org (2021-04-20)

The problem is what signal to use to invalidate the weak ptrs? Apparently OnContextDestroyed() isn't sufficient. 

### jb...@chromium.org (2021-04-20)

You need to invalidate base::WeakPtrs, if any exist, when !IsContextDestroyed() && HasPendingActivity() becomes false, because after that point they may point to invalid things.

- ContextDestroyed will tell you when !IsContextDestroyed() becomes false
- when HasPendingActivity() becomes false (but the context is still not destroyed) depends on your class

Oilpan's integrated weak pointers (WeakMember, WeakPersistent, CrossThreadWeakPersistent) become invalid during weak processing, which works great for things where the only visible effect of an object going away is that some other resources (like other heap objects) can also be freed.

Using a pre-finalizer is heavy-weight (every pre-finalizer on the heap needs to be checked in one pass as the world is stopped) and makes the behavior of your code dependent on GC timing (your cancellable work really becomes uninteresting at the point that nothing is alive to hear of it, not when we happen to have used up enough heap memory to run the GC later on). So using a prefinalizer to do this will have the effect that those WeakPtrs will become null or not depending on heap pressure -- a recipe for weird bugs and, if this different is web-visible, possibly interop issues.

That's why I would advise in most cases that your object deterministically keep itself alive for as long as it makes sense to do so (i.e., as long as the activity could be visible to the user or to script), and then deterministically stop doing so once that's no longer true (the background activity that needs this object to be alive has finished, been cancelled, or the ExecutionContext is destroyed).

The GC can then free the heap memory at its leisure and the time that it chooses to do so isn't visible except in the amount of private memory the renderer is using. And since the GC is no longer promising to keep the object alive, base::WeakPtrs should be invalidated, because once sweeping begins the object may be in a weird state (in particular, its references to other on-heap objects should no longer be expected to be valid).

### da...@chromium.org (2021-04-20)

Without knowing if the class is still referenced by JavaScript, invalidating the WeakPtrs at time of !HasPendingActivity() will lead to incorrect operation. The work is only is only an artificial lifetime extension if there's no further usage (i.e., metadata decoding after a track change). So unfortunately it's not possible to just drop the tasks once we have no more pending activity.

For now I'll just add a has_pending_metadata_ and add some dchecks to the destructor to ensure this cleans up properly. If we get bit by this again a prefinalizer seems like a safer approach.

### gi...@appspot.gserviceaccount.com (2021-04-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0135fb6dd2ace333d823f84aadc70b8774a3b96e

commit 0135fb6dd2ace333d823f84aadc70b8774a3b96e
Author: Dale Curtis <dalecurtis@chromium.org>
Date: Wed Apr 21 00:49:46 2021

[ImageDecoder] Expand HasPendingActivity to include automatic work.

We can't rely on OnContextDestroyed() to ensure all outstanding
work is invalidated. Since ImageDecoder will automatically queue
metadata decoding, we must account for it in HasPendingActivity().

This change adds a counter for the number of outstanding metadata
requests (several may be in flight due to bytes received). Since
this is a bit fragile to future modification, DCHECKs() are added
to ~ImageDecoderExternal() to provide at least some safe guards.

R=jbroman

Fixed: 1198895
Change-Id: I500db2bf09c53206a5f022513b015bf93f303389
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2840409
Commit-Queue: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Jeremy Roman <jbroman@chromium.org>
Cr-Commit-Position: refs/heads/master@{#874506}

[modify] https://crrev.com/0135fb6dd2ace333d823f84aadc70b8774a3b96e/third_party/blink/renderer/modules/webcodecs/image_decoder_external.cc
[modify] https://crrev.com/0135fb6dd2ace333d823f84aadc70b8774a3b96e/third_party/blink/renderer/modules/webcodecs/image_decoder_external.h
[modify] https://crrev.com/0135fb6dd2ace333d823f84aadc70b8774a3b96e/third_party/blink/renderer/modules/webcodecs/image_decoder_external_test.cc


### da...@chromium.org (2021-04-21)

@neklab2015: Please try a build after 874506. Thanks!

### ne...@gmail.com (2021-04-21)

#34
I tested with buil asan-linux-release-874521.zip，ran it for more than 10 minutes, and did not repr this crash.

### da...@chromium.org (2021-04-21)

Thanks for verifying! I'll soak it on canary and request merge later Thursday.

### [Deleted User] (2021-04-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-21)

Setting milestone and target because of Security_Impact=Beta and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-21)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-21)

Requesting merge to beta M90 because latest trunk commit (874506) appears to be after beta branch point (857950).

Requesting merge to future beta M91 because latest trunk commit (874506) appears to be after future beta branch point (870763).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-21)

This bug requires manual review: Request affecting a post-stable build
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
Owners: govind@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2021-04-21)

1. Yes
2. ad9b81155c87e9801783023452776391ea265527 and 0135fb6dd2ace333d823f84aadc70b8774a3b96e
3. Yes.
4. No
5. Security issue found after branch.
6. Part of a new feature in OT.
7. It's in OT, so kind of behind a flag.

### ad...@google.com (2021-04-21)

Thanks for the fix!

Approving merge to M91, branch 4472. I'll approve M90 merge at a later date once this has had a bit of bake time.

One question on the fix itself: is there any way an attacker could cause the int to overflow?

### da...@chromium.org (2021-04-21)

M90 doesn't need a merge, only M91. 

Hypothetically if someone found a bug which could cause a hang on the ImageDecoderCore worker thread, they could then issue INT_MAX single-byte writes via the ReadableStream to overflow the counter. This would result in pretty extreme memory usage though -- probably 4 bytes * INT_MAX is the absolute lower bound and something like 512 * INT_MAX is more reasonable since each 1-byte would result in a new allocation that ends up posting work to the sequenced worker pool. I don't know if we have limits on the number of tasks, but that could also be problematic.

### da...@chromium.org (2021-04-21)

(Impact is limited to 91.0.4469.0+ since that's when 685170042e13b1215eeccc9dc50fcacf80779c3b landed. We didn't use WeakPtrs prior)

### da...@chromium.org (2021-04-21)

Merge 1/2 in CQ: https://chromium-review.googlesource.com/c/chromium/src/+/2845149

### gi...@appspot.gserviceaccount.com (2021-04-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f153371df68b503e38778cb6f2bf055d9e23ff80

commit f153371df68b503e38778cb6f2bf055d9e23ff80
Author: Dale Curtis <dalecurtis@chromium.org>
Date: Wed Apr 21 23:34:28 2021

Merge M91: "[ImageDecoder] Invalidate WeakPtrs upon ExecutionContext loss."

WeakPtrs need special consideration when used with a garbage collected
type; they must be invalidated ahead of finalization.

We also need to ensure that no further WeakPtrs are created, so close()
the decoder during ContextDestroyed() to prevent further operation.

This also fixes a DCHECK() that was incorrectly firing during the
reproduction case.

R=​jbroman

(cherry picked from commit ad9b81155c87e9801783023452776391ea265527)

Fixed: 1198895
Change-Id: Ib3d108233fa30d47688a6fba395afaab99e151cc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2836831
Commit-Queue: Dale Curtis <dalecurtis@chromium.org>
Commit-Queue: Jeremy Roman <jbroman@chromium.org>
Auto-Submit: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Jeremy Roman <jbroman@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#873967}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2845149
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4472@{#311}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/f153371df68b503e38778cb6f2bf055d9e23ff80/third_party/blink/renderer/modules/webcodecs/image_decoder_external.cc
[modify] https://crrev.com/f153371df68b503e38778cb6f2bf055d9e23ff80/third_party/blink/renderer/modules/webcodecs/image_decoder_external_test.cc


### da...@chromium.org (2021-04-21)

Merge 2/2: https://chromium-review.googlesource.com/c/chromium/src/+/2845489

### gi...@appspot.gserviceaccount.com (2021-04-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2d0a6b1eb0637c60edbbbd79e22855ed1b7f38e2

commit 2d0a6b1eb0637c60edbbbd79e22855ed1b7f38e2
Author: Dale Curtis <dalecurtis@chromium.org>
Date: Thu Apr 22 02:36:30 2021

Merge M91: "[ImageDecoder] Expand HasPendingActivity to include automatic work."

We can't rely on OnContextDestroyed() to ensure all outstanding
work is invalidated. Since ImageDecoder will automatically queue
metadata decoding, we must account for it in HasPendingActivity().

This change adds a counter for the number of outstanding metadata
requests (several may be in flight due to bytes received). Since
this is a bit fragile to future modification, DCHECKs() are added
to ~ImageDecoderExternal() to provide at least some safe guards.

R=​jbroman

(cherry picked from commit 0135fb6dd2ace333d823f84aadc70b8774a3b96e)

Fixed: 1198895
Change-Id: I500db2bf09c53206a5f022513b015bf93f303389
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2840409
Commit-Queue: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Jeremy Roman <jbroman@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#874506}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2845489
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Dale Curtis <dalecurtis@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4472@{#316}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/2d0a6b1eb0637c60edbbbd79e22855ed1b7f38e2/third_party/blink/renderer/modules/webcodecs/image_decoder_external.cc
[modify] https://crrev.com/2d0a6b1eb0637c60edbbbd79e22855ed1b7f38e2/third_party/blink/renderer/modules/webcodecs/image_decoder_external.h
[modify] https://crrev.com/2d0a6b1eb0637c60edbbbd79e22855ed1b7f38e2/third_party/blink/renderer/modules/webcodecs/image_decoder_external_test.cc


### sr...@google.com (2021-04-22)

Please have your CL cherrypicked to M90 and ready for merge ( run through dry-run CQ). Once I will review/approve these requests later today, but all approved merges need to land before Friday April 23, 12pm PT, so need your help to get the CP ready if not already done. 

### da...@chromium.org (2021-04-22)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-04-22)

As noted in https://bugs.chromium.org/p/chromium/issues/detail?id=1198895#c46 this only affects 91+

### [Deleted User] (2021-04-23)

Setting milestone and target because of Security_Impact=Beta and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-04-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-04-28)

Congratulations! The VRP Panel has decided to award you $7500 for this report. Thank you for the extra testing and responsiveness you provided as the team worked toward a fix! 

### am...@google.com (2021-04-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2021-11-01)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1198895?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1198894]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055548)*
