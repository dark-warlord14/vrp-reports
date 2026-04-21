# use after free in SendQueuedMediaEvents

| Field | Value |
|-------|-------|
| **Issue ID** | [40059414](https://issues.chromium.org/issues/40059414) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media |
| **Platforms** | Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | tm...@chromium.org |
| **Created** | 2022-04-19 |
| **Bounty** | $5,000.00 |

## Description

**Steps to reproduce the problem:**  

OS Version:  

Ubuntu 20.04  

tested chrome version:  

Version 102.0.4972.0 (Official Build) dev (64-bit)  

Chromium 102.0.4997.0 with asan build  

This issue is not stable to reproduce with a single browser.  

In my local tests,I opened 5 tabs to reproduce this issue.  

--user-data-dir=/tmp/11 <http://localhost:8000/crash.html> <http://localhost:8000/crash.html> <http://localhost:8000/crash.html> <http://localhost:8000/crash.html> <http://localhost:8000/crash.html>

**Problem Description:**  

==263776==ERROR: AddressSanitizer: heap-use-after-free on address 0x6030001a2908 at pc 0x5619f3723a5a bp 0x7ffe4cf98d30 sp 0x7ffe4cf98d28  

READ of size 8 at 0x6030001a2908 thread T0 (chrome)  

==263776==WARNING: invalid path to external symbolizer!  

==263776==WARNING: Failed to use and restart external symbolizer!  

#0 0x5619f3723a59 in content::InspectorMediaEventHandler::SendQueuedMediaEvents(std::\_\_1::vector<media::MediaLogRecord, std::\_\_1::allocator[media::MediaLogRecord](javascript:void(0);) >) inspector\_media\_event\_handler.cc:?  

#1 0x5619f3723a59 in ?? ??:0  

#2 0x5619f372b4e7 in content::BatchingMediaLog::SendQueuedMediaEvents() batching\_media\_log.cc:?  

#3 0x5619f372b4e7 in ?? ??:0  

#4 0x5619f372f2e0 in base::internal::Invoker<base::internal::BindState<void (content::BatchingMediaLog::\*)(), base::WeakPtr[content::BatchingMediaLog](javascript:void(0);) >, void ()>::RunOnce(base::internal::BindStateBase\*) batching\_media\_log.cc:?  

#5 0x5619f372f2e0 in ?? ??:0  

#6 0x5619e1a6cea3 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) task\_annotator.cc:?  

#7 0x5619e1a6cea3 in ?? ??:0  

#8 0x5619e1aaf0dd in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) thread\_controller\_with\_message\_pump\_impl.cc:?  

#9 0x5619e1aaf0dd in ?? ??:0  

#10 0x5619e1aae7b4 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() thread\_controller\_with\_message\_pump\_impl.cc:?  

#11 0x5619e1aae7b4 in ?? ??:0  

#12 0x5619e1aafde1 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() thread\_controller\_with\_message\_pump\_impl.cc:?  

#13 0x5619e1aafde1 in ?? ??:0  

#14 0x5619e1965626 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) message\_pump\_default.cc:?  

#15 0x5619e1965626 in ?? ??:0  

#16 0x5619e1ab04a6 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) thread\_controller\_with\_message\_pump\_impl.cc:?  

#17 0x5619e1ab04a6 in ?? ??:0  

#18 0x5619e19e77f3 in base::RunLoop::Run(base::Location const&) run\_loop.cc:?  

#19 0x5619e19e77f3 in ?? ??:0  

#20 0x5619f63040cc in content::RendererMain(content::MainFunctionParams) renderer\_main.cc:?  

#21 0x5619f63040cc in ?? ??:0  

#22 0x5619e07d5878 in content::RunZygote(content::ContentMainDelegate\*) content\_main\_runner\_impl.cc:?  

#23 0x5619e07d5878 in ?? ??:0  

#24 0x5619e07d7373 in content::RunOtherNamedProcessTypeMain(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, content::MainFunctionParams, content::ContentMainDelegate\*) content\_main\_runner\_impl.cc:?  

#25 0x5619e07d7373 in ?? ??:0  

#26 0x5619e07d93bf in content::ContentMainRunnerImpl::Run() content\_main\_runner\_impl.cc:?  

#27 0x5619e07d93bf in ?? ??:0  

#28 0x5619e07d2c21 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) content\_main.cc:?  

#29 0x5619e07d2c21 in ?? ??:0  

#30 0x5619e07d334c in content::ContentMain(content::ContentMainParams) content\_main.cc:?  

#31 0x5619e07d334c in ?? ??:0  

#32 0x5619d290cba6 in ChromeMain ??:?  

#33 0x5619d290cba6 in ?? ??:0  

#34 0x7f3cdfe69d8f in \_\_libc\_start\_call\_main ./csu/../sysdeps/nptl/libc\_start\_call\_main.h:58  

#35 0x7f3cdfe69d8f in ?? ??:0

0x6030001a2908 is located 8 bytes inside of 32-byte region [0x6030001a2900,0x6030001a2920)  

freed by thread T0 (chrome) here:  

#0 0x5619d290abfd in operator delete(void\*) ??:?  

#1 0x5619d290abfd in ?? ??:0  

#2 0x5619f372adf2 in content::BatchingMediaLog::~BatchingMediaLog() batching\_media\_log.cc:?  

#3 0x5619f372adf2 in ?? ??:0  

#4 0x5619f372b89d in content::BatchingMediaLog::~BatchingMediaLog() batching\_media\_log.cc:?  

#5 0x5619f372b89d in ?? ??:0  

#6 0x5619f42277df in blink::DecoderTemplate[blink::VideoDecoderTraits](javascript:void(0);)::~DecoderTemplate() decoder\_template.cc:?  

#7 0x5619f42277df in ?? ??:0  

#8 0x5619dd694003 in cppgc::internal::(anonymous namespace)::SweepFinalizer::FinalizePage(cppgc::internal::(anonymous namespace)::SpaceState::SweptPageState\*) sweeper.cc:?  

#9 0x5619dd694003 in ?? ??:0  

#10 0x5619dd6931f9 in cppgc::internal::(anonymous namespace)::SweepFinalizer::FinalizeHeap(std::\_\_1::vector<cppgc::internal::(anonymous namespace)::SpaceState, std::\_\_1::allocator<cppgc::internal::(anonymous namespace)::SpaceState> >\*) sweeper.cc:?  

#11 0x5619dd6931f9 in ?? ??:0  

#12 0x5619dd690ae2 in cppgc::internal::Sweeper::SweeperImpl::Finish() sweeper.cc:?  

#13 0x5619dd690ae2 in ?? ??:0  

#14 0x5619dd68e472 in cppgc::internal::Sweeper::SweeperImpl::FinishIfRunning() sweeper.cc:?  

#15 0x5619dd68e472 in ?? ??:0  

#16 0x5619dd67b50b in cppgc::internal::ObjectAllocator::RefillLinearAllocationBuffer(cppgc::internal::NormalPageSpace&, unsigned long) object-allocator.cc:?  

#17 0x5619dd67b50b in ?? ??:0  

#18 0x5619dd67b03b in cppgc::internal::ObjectAllocator::OutOfLineAllocateImpl(cppgc::internal::Norma

**Additional Comments:**

\*\*Chrome version: \*\* Google Chrome 102.0.4972.0 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 355 B)
- [crash.html](attachments/crash.html) (text/plain, 408 B)

## Timeline

### dt...@chromium.org (2022-04-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-19)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-04-19)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-04-19)

Looks like tmathmeyer wrote most of   InspectorMediaEventHandler::SendQueuedMediaEvents(), assigning as such.

[Monorail components: Internals>Media]

### tm...@chromium.org (2022-04-19)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-04-21)

Repro'd at ToT (M103) but not at M100, despite a few tries. But since it is intermittent, it is hard to have confidence in how far back it goes. tmathmeyer, any estimate on when this might have broken?

### tm...@chromium.org (2022-04-21)

I was only able to get a different crash in the base::lock destructor yesterday. I'm sick today though, so i'll take a closer look tomorrow.

### tm...@chromium.org (2022-04-29)

the unique_ptr<CodecLogger> in DecoderTemplate is being destroyed, causing |parent_media_log_| and |media_log_| to be destroyed while there is still a pending call to BatchingMediaLog::SendQueuedMediaEvents floating about. I was under the impression that the |weak_this| involved in that OnceCallback should prevent that from firing if |weak_this_| is freed, but it appears that it isn't the case.


### tm...@chromium.org (2022-05-02)

@tsepez, are you able to repro with the same crash as the reporter? I can't get it to crash in that way, but I do get 
[1318086:1:0502/142228.234594:FATAL:lock.cc(23)] Check failed: owning_thread_ref_.is_null(). 
pretty consistently.

### an...@chromium.org (2022-05-06)

+ cc @tsepez to answer c#9.

I've tried reproducing on ToT(M103) and M102 asan builds on linux but have not been able to.

### bh...@google.com (2022-05-19)

I tried reproducing today on ToT(M104) asan build on linux, but was unable too.

### ke...@chromium.org (2022-05-19)

tsepez@: Ping for https://crbug.com/chromium/1317714#c9?

I've tried to reproduce and so far have only managed to see the CHECK failure, as tmathmeyer@ also observed.

### em...@gmail.com (2022-05-23)

I tested with asan-linux-release-999995.zip(Chromium 103.0.5046.0),and  found that the original POC cannot  reproduce this issue.
I made a simple modification. Please try the POC in the attachment again.


### ad...@google.com (2022-05-26)

tsepez@ is OOO for another 5 days.

tmathmeyer@, it would be great if you can let us know if this repros back to M102. There's no need to go earlier than that. But we need to add the right FoundIn label so that sheriffbot arranges for a fix eventually to be merged to the right channels, and so that release TPMs can hold releases to await a fix if this is a more recent regression.

### ts...@chromium.org (2022-05-31)

Confirmed PoC from https://crbug.com/chromium/1317714#c13 repros on chrome 104.0.5096.0. My recollection was that I got a repro on the orignal, but im not 100%. We seem to have a solid repro under the new PoC.

### tm...@chromium.org (2022-06-01)

I'm unable to actually get a crash, still, but I do get severe lockup and an eventual check failure. However I'm also pretty sure I've fixed the issue, and that was a failure to take the lock for reading internal state in BatchingMediaLog's destructor. This has been here for a while, so I think we can play it safe and say this was present at least as far back as 102. Fix is here: https://chromium-review.googlesource.com/c/chromium/src/+/3682060 and I'll start the merge back process when it's landed.

### tm...@chromium.org (2022-06-01)

Interestingly enough, the -Wthread-safety-analysis flag we use seems to fail to catch uses of GUARDED_BY variables in the class destructor, so maybe I'll give it a go and fix that if i can

### tm...@chromium.org (2022-06-01)

[Empty comment from Monorail migration]

### tm...@chromium.org (2022-06-01)

Finally got a crash, with symbolization:

==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x603002400af8 at pc 0x7f7930f29617 bp 0x7ffce932fbd0 sp 0x7ffce932fbc8
READ of size 8 at 0x603002400af8 thread T0 (chrome)
==1==WARNING: invalid path to external symbolizer!
==1==WARNING: Failed to use and restart external symbolizer!
    #0 0x7f7930f29616 in content::InspectorMediaEventHandler::SendQueuedMediaEvents(std::Cr::vector<media::MediaLogRecord, std::Cr::allocator<media::MediaLogRecord>>) ./../../content/renderer/media/inspector_media_event_handler.cc:154:5
    #1 0x7f7930f192dd in content::BatchingMediaLog::SendQueuedMediaEvents() ./../../content/renderer/media/batching_media_log.cc:238:14
    #2 0x7f7930f1d170 in void base::internal::FunctorTraits<void (content::BatchingMediaLog::*)(), void>::Invoke<void (content::BatchingMediaLog::*)(), base::WeakPtr<content::BatchingMediaLog>>(void (content::BatchingMediaLog::*)(), base::WeakPtr<content::BatchingMediaLog>&&) ./../../base/bind_internal.h:541:12
    #3 0x7f7930f1d170 in void base::internal::InvokeHelper<true, void>::MakeItSo<void (content::BatchingMediaLog::*)(), base::WeakPtr<content::BatchingMediaLog>>(void (content::BatchingMediaLog::*&&)(), base::WeakPtr<content::BatchingMediaLog>&&) ./../../base/bind_internal.h:725:5


0x603002400af8 is located 8 bytes inside of 32-byte region [0x603002400af0,0x603002400b10)
freed by thread T0 (chrome) here:
    #0 0x5611dbc125bd in operator delete(void*) _asan_rtl_:3
    #1 0x7f7930f18acf in std::Cr::default_delete<content::BatchingMediaLog::EventHandler>::operator()(content::BatchingMediaLog::EventHandler*) const ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:51:5
    #2 0x7f7930f18acf in std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>::reset(content::BatchingMediaLog::EventHandler*) ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:308:7
    #3 0x7f7930f18acf in std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>::~unique_ptr() ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:262:19
    #4 0x7f7930f18acf in std::Cr::allocator<std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>>::destroy(std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>*) ./../../buildtools/third_party/libc++/trunk/include/__memory/allocator.h:156:15
    #5 0x7f7930f18acf in void std::Cr::allocator_traits<std::Cr::allocator<std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>>>::destroy<std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>, void>(std::Cr::allocator<std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>>&, std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>*) ./../../buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:309:13
    #6 0x7f7930f18acf in std::Cr::vector<std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>, std::Cr::allocator<std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>>>::__base_destruct_at_end(std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>*) ./../../buildtools/third_party/libc++/trunk/include/vector:822:9
    #7 0x7f7930f18acf in std::Cr::vector<std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>, std::Cr::allocator<std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>>>::__clear() ./../../buildtools/third_party/libc++/trunk/include/vector:816:29
    #8 0x7f7930f18acf in std::Cr::vector<std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>, std::Cr::allocator<std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>>>::~vector() ./../../buildtools/third_party/libc++/trunk/include/vector:420:9
    #9 0x7f7930f18acf in content::BatchingMediaLog::~BatchingMediaLog() ./../../content/renderer/media/batching_media_log.cc:78:1
    #10 0x7f7930f196dd in content::BatchingMediaLog::~BatchingMediaLog() ./../../content/renderer/media/batching_media_log.cc:66:39
    #11 0x7f78f35b5972 in std::Cr::default_delete<media::MediaLog>::operator()(media::MediaLog*) const ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:51:5
    #12 0x7f78f35b5972 in std::Cr::unique_ptr<media::MediaLog, std::Cr::default_delete<media::MediaLog>>::reset(media::MediaLog*) ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:308:7
    #13 0x7f78f35b5972 in std::Cr::unique_ptr<media::MediaLog, std::Cr::default_delete<media::MediaLog>>::~unique_ptr() ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:262:19
    #14 0x7f78f35b5972 in blink::CodecLogger<media::TypedStatus<media::DecoderStatusTraits>>::~CodecLogger() ./../../third_party/blink/renderer/modules/webcodecs/codec_logger.h:77:72
    #15 0x7f78f35b5972 in std::Cr::default_delete<blink::CodecLogger<media::TypedStatus<media::DecoderStatusTraits>>>::operator()(blink::CodecLogger<media::TypedStatus<media::DecoderStatusTraits>>*) const ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:51:5


previously allocated by thread T0 (chrome) here:
    #0 0x5611dbc11d5d in operator new(unsigned long) _asan_rtl_:3
    #1 0x7f7931020156 in std::Cr::__unique_if<content::InspectorMediaEventHandler>::__unique_single std::Cr::make_unique<content::InspectorMediaEventHandler, blink::MediaInspectorContext*&>(blink::MediaInspectorContext*&) ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:717:28
    #2 0x7f7931020156 in content::RendererBlinkPlatformImpl::GetMediaLog(blink::MediaInspectorContext*, scoped_refptr<base::SingleThreadTaskRunner>, bool) ./../../content/renderer/renderer_blink_platform_impl.cc:1065:7
    #3 0x7f78f35c6720 in blink::CodecLogger<media::TypedStatus<media::DecoderStatusTraits>>::CodecLogger(blink::ExecutionContext*, scoped_refptr<base::SingleThreadTaskRunner>) ./../../third_party/blink/renderer/modules/webcodecs/codec_logger.h:63:48
    #4 0x7f78f35b4d15 in std::Cr::__unique_if<blink::CodecLogger<media::TypedStatus<media::DecoderStatusTraits>>>::__unique_single std::Cr::make_unique<blink::CodecLogger<media::TypedStatus<media::DecoderStatusTraits>>, blink::ExecutionContext*&, scoped_refptr<base::SingleThreadTaskRunner>&>(blink::ExecutionContext*&, scoped_refptr<base::SingleThreadTaskRunner>&) ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:717:32
    #5 0x7f78f35b4d15 in blink::DecoderTemplate<blink::VideoDecoderTraits>::DecoderTemplate(blink::ScriptState*, blink::VideoDecoderInit const*, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/webcodecs/decoder_template.cc:86:13
    #6 0x7f78f3615961 in blink::VideoDecoder::VideoDecoder(blink::ScriptState*, blink::VideoDecoderInit const*, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/webcodecs/video_decoder.cc:509:7
    #7 0x7f78f360fed0 in blink::VideoDecoder* cppgc::MakeGarbageCollectedTrait<blink::VideoDecoder>::Call<blink::ScriptState*&, blink::VideoDecoderInit const*&, blink::ExceptionState&>(cppgc::AllocationHandle&, blink::ScriptState*&, blink::VideoDecoderInit const*&, blink::ExceptionState&) ./../../v8/include/cppgc/allocation.h:242:32
    #8 0x7f78f360fed0 in blink::VideoDecoder* cppgc::MakeGarbageCollected<blink::VideoDecoder, blink::ScriptState*&, blink::VideoDecoderInit const*&, blink::ExceptionState&>(cppgc::AllocationHandle&, blink::ScriptState*&, blink::VideoDecoderInit const*&, blink::ExceptionState&) ./../../v8/include/cppgc/allocation.h:280:7
    #9 0x7f78f360fed0 in blink::VideoDecoder* blink::MakeGarbageCollected<blink::VideoDecoder, blink::ScriptState*&, blink::VideoDecoderInit const*&, blink::ExceptionState&>(blink::ScriptState*&, blink::VideoDecoderInit const*&, blink::ExceptionState&) ./../../third_party/blink/renderer/platform/heap/garbage_collected.h:34:10
    #10 0x7f78f360fed0 in blink::VideoDecoder::Create(blink::ScriptState*, blink::VideoDecoderInit const*, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/webcodecs/video_decoder.cc:259:7
    #11 0x7f78f1d95b79 in blink::(anonymous namespace)::v8_video_decoder::ConstructorCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_video_decoder.cc:142:23
    #12 0x7f78f6bdbf93 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:147:3
    #13 0x7f78f6bd8abc in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:114:36



### tm...@chromium.org (2022-06-01)

Actually looks like SendQueuedMediaEvents is tickling the blink GC, which deletes an object that owns BatchingMediaLog, which free's itself...

    #0 0x5611dbc125bd in operator delete(void*) _asan_rtl_:3
    #1 0x7f7930f18acf in std::Cr::default_delete<content::BatchingMediaLog::EventHandler>::operator()(content::BatchingMediaLog::EventHandler*) const ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:51:5
    #2 0x7f7930f18acf in std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>::reset(content::BatchingMediaLog::EventHandler*) ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:308:7
    #3 0x7f7930f18acf in std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>::~unique_ptr() ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:262:19
    #4 0x7f7930f18acf in std::Cr::allocator<std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>>::destroy(std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>*) ./../../buildtools/third_party/libc++/trunk/include/__memory/allocator.h:156:15
    #5 0x7f7930f18acf in void std::Cr::allocator_traits<std::Cr::allocator<std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>>>::destroy<std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>, void>(std::Cr::allocator<std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>>&, std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>*) ./../../buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:309:13
    #6 0x7f7930f18acf in std::Cr::vector<std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>, std::Cr::allocator<std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>>>::__base_destruct_at_end(std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>*) ./../../buildtools/third_party/libc++/trunk/include/vector:822:9
    #7 0x7f7930f18acf in std::Cr::vector<std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>, std::Cr::allocator<std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>>>::__clear() ./../../buildtools/third_party/libc++/trunk/include/vector:816:29
    #8 0x7f7930f18acf in std::Cr::vector<std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>, std::Cr::allocator<std::Cr::unique_ptr<content::BatchingMediaLog::EventHandler, std::Cr::default_delete<content::BatchingMediaLog::EventHandler>>>>::~vector() ./../../buildtools/third_party/libc++/trunk/include/vector:420:9
    #9 0x7f7930f18acf in content::BatchingMediaLog::~BatchingMediaLog() ./../../content/renderer/media/batching_media_log.cc:78:1
    #10 0x7f7930f196dd in content::BatchingMediaLog::~BatchingMediaLog() ./../../content/renderer/media/batching_media_log.cc:66:39
    #11 0x7f78f35b5972 in std::Cr::default_delete<media::MediaLog>::operator()(media::MediaLog*) const ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:51:5
    #12 0x7f78f35b5972 in std::Cr::unique_ptr<media::MediaLog, std::Cr::default_delete<media::MediaLog>>::reset(media::MediaLog*) ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:308:7
    #13 0x7f78f35b5972 in std::Cr::unique_ptr<media::MediaLog, std::Cr::default_delete<media::MediaLog>>::~unique_ptr() ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:262:19
    #14 0x7f78f35b5972 in blink::CodecLogger<media::TypedStatus<media::DecoderStatusTraits>>::~CodecLogger() ./../../third_party/blink/renderer/modules/webcodecs/codec_logger.h:77:72
    #15 0x7f78f35b5972 in std::Cr::default_delete<blink::CodecLogger<media::TypedStatus<media::DecoderStatusTraits>>>::operator()(blink::CodecLogger<media::TypedStatus<media::DecoderStatusTraits>>*) const ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:51:5
    #16 0x7f78f35b5972 in std::Cr::unique_ptr<blink::CodecLogger<media::TypedStatus<media::DecoderStatusTraits>>, std::Cr::default_delete<blink::CodecLogger<media::TypedStatus<media::DecoderStatusTraits>>>>::reset(blink::CodecLogger<media::TypedStatus<media::DecoderStatusTraits>>*) ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:308:7
    #17 0x7f78f35b5972 in std::Cr::unique_ptr<blink::CodecLogger<media::TypedStatus<media::DecoderStatusTraits>>, std::Cr::default_delete<blink::CodecLogger<media::TypedStatus<media::DecoderStatusTraits>>>>::~unique_ptr() ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:262:19
    #18 0x7f78f35b5972 in blink::DecoderTemplate<blink::VideoDecoderTraits>::~DecoderTemplate() ./../../third_party/blink/renderer/modules/webcodecs/decoder_template.cc:104:1
    #19 0x7f78f89d5bc3 in cppgc::internal::(anonymous namespace)::SweepFinalizer::FinalizePage(cppgc::internal::(anonymous namespace)::SpaceState::SweptPageState*)::'lambda'(cppgc::internal::HeapObjectHeader*)::operator()(cppgc::internal::HeapObjectHeader*) const ./../../v8/src/heap/cppgc/sweeper.cc:427:15
    #20 0x7f78f89d5bc3 in cppgc::internal::(anonymous namespace)::SweepFinalizer::FinalizePage(cppgc::internal::(anonymous namespace)::SpaceState::SweptPageState*) ./../../v8/src/heap/cppgc/sweeper.cc:438:7
    #21 0x7f78f89d4db9 in cppgc::internal::(anonymous namespace)::SweepFinalizer::FinalizeSpace(cppgc::internal::(anonymous namespace)::SpaceState*) ./../../v8/src/heap/cppgc/sweeper.cc:395:7
    #22 0x7f78f89d4db9 in cppgc::internal::(anonymous namespace)::SweepFinalizer::FinalizeHeap(std::Cr::vector<cppgc::internal::(anonymous namespace)::SpaceState, std::Cr::allocator<cppgc::internal::(anonymous namespace)::SpaceState>>*) ./../../v8/src/heap/cppgc/sweeper.cc:389:7
    #23 0x7f78f89d25c2 in cppgc::internal::Sweeper::SweeperImpl::Finish() ./../../v8/src/heap/cppgc/sweeper.cc:880:15
    #24 0x7f78f89cfcd2 in cppgc::internal::Sweeper::SweeperImpl::FinishIfRunning() ./../../v8/src/heap/cppgc/sweeper.cc:853:7
    #25 0x7f78f89b8f1b in cppgc::internal::ObjectAllocator::RefillLinearAllocationBuffer(cppgc::internal::NormalPageSpace&, unsigned long) ./../../v8/src/heap/cppgc/object-allocator.cc:184:11
    #26 0x7f78f89b887c in cppgc::internal::ObjectAllocator::OutOfLineAllocateImpl(cppgc::internal::NormalPageSpace&, unsigned long, cppgc::internal::AlignVal, unsigned short) ./../../v8/src/heap/cppgc/object-allocator.cc:152:3
    #27 0x7f78f89b83fe in cppgc::internal::ObjectAllocator::OutOfLineAllocate(cppgc::internal::NormalPageSpace&, unsigned long, cppgc::internal::AlignVal, unsigned short) ./../../v8/src/heap/cppgc/object-allocator.cc:111:18
    #28 0x7f7902297d63 in cppgc::internal::MakeGarbageCollectedTraitInternal::AllocationDispatcher<blink::HeapHashTableBacking<WTF::HashTable<WTF::String, WTF::KeyValuePair<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>, WTF::KeyValuePairKeyExtractor, WTF::StringHash, WTF::HashMapValueTraits<WTF::HashTraits<WTF::String>, WTF::HashTraits<cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>>, WTF::HashTraits<WTF::String>, blink::HeapAllocator>>, blink::HeapHashTableBackingSpace, 8ul>::Invoke(cppgc::AllocationHandle&, unsigned long) ./../../v8/include/cppgc/allocation.h:117:14
    #29 0x7f7902297d63 in cppgc::MakeGarbageCollectedTraitBase<blink::HeapHashTableBacking<WTF::HashTable<WTF::String, WTF::KeyValuePair<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>, WTF::KeyValuePairKeyExtractor, WTF::StringHash, WTF::HashMapValueTraits<WTF::HashTraits<WTF::String>, WTF::HashTraits<cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>>, WTF::HashTraits<WTF::String>, blink::HeapAllocator>>>::Allocate(cppgc::AllocationHandle&, unsigned long) ./../../v8/include/cppgc/allocation.h:180:12
    #30 0x7f7902297d63 in blink::HeapHashTableBacking<WTF::HashTable<WTF::String, WTF::KeyValuePair<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>, WTF::KeyValuePairKeyExtractor, WTF::StringHash, WTF::HashMapValueTraits<WTF::HashTraits<WTF::String>, WTF::HashTraits<cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>>, WTF::HashTraits<WTF::String>, blink::HeapAllocator>>* cppgc::MakeGarbageCollectedTrait<blink::HeapHashTableBacking<WTF::HashTable<WTF::String, WTF::KeyValuePair<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>, WTF::KeyValuePairKeyExtractor, WTF::StringHash, WTF::HashMapValueTraits<WTF::HashTraits<WTF::String>, WTF::HashTraits<cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>>, WTF::HashTraits<WTF::String>, blink::HeapAllocator>>>::Call<>(cppgc::AllocationHandle&, unsigned long) ./../../third_party/blink/renderer/platform/heap/collection_support/heap_hash_table_backing.h:435:20
    #31 0x7f79022988e4 in blink::HeapHashTableBacking<WTF::HashTable<WTF::String, WTF::KeyValuePair<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>, WTF::KeyValuePairKeyExtractor, WTF::StringHash, WTF::HashMapValueTraits<WTF::HashTraits<WTF::String>, WTF::HashTraits<cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>>, WTF::HashTraits<WTF::String>, blink::HeapAllocator>>* cppgc::MakeGarbageCollected<blink::HeapHashTableBacking<WTF::HashTable<WTF::String, WTF::KeyValuePair<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>, WTF::KeyValuePairKeyExtractor, WTF::StringHash, WTF::HashMapValueTraits<WTF::HashTraits<WTF::String>, WTF::HashTraits<cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>>, WTF::HashTraits<WTF::String>, blink::HeapAllocator>>, unsigned long>(cppgc::AllocationHandle&, unsigned long&&) ./../../v8/include/cppgc/allocation.h:280:7
    #32 0x7f79022988e4 in blink::HeapHashTableBacking<WTF::HashTable<WTF::String, WTF::KeyValuePair<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>, WTF::KeyValuePairKeyExtractor, WTF::StringHash, WTF::HashMapValueTraits<WTF::HashTraits<WTF::String>, WTF::HashTraits<cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>>, WTF::HashTraits<WTF::String>, blink::HeapAllocator>>* blink::MakeGarbageCollected<blink::HeapHashTableBacking<WTF::HashTable<WTF::String, WTF::KeyValuePair<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>, WTF::KeyValuePairKeyExtractor, WTF::StringHash, WTF::HashMapValueTraits<WTF::HashTraits<WTF::String>, WTF::HashTraits<cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>>, WTF::HashTraits<WTF::String>, blink::HeapAllocator>>, unsigned long>(unsigned long&&) ./../../third_party/blink/renderer/platform/heap/garbage_collected.h:34:10
    #33 0x7f79022988e4 in WTF::KeyValuePair<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>* blink::HeapAllocator::AllocateHashTableBacking<WTF::KeyValuePair<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>, WTF::HashTable<WTF::String, WTF::KeyValuePair<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>, WTF::KeyValuePairKeyExtractor, WTF::StringHash, WTF::HashMapValueTraits<WTF::HashTraits<WTF::String>, WTF::HashTraits<cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>>, WTF::HashTraits<WTF::String>, blink::HeapAllocator>>(unsigned long) ./../../third_party/blink/renderer/platform/heap/heap_allocator_impl.h:100:9
    #34 0x7f79022988e4 in WTF::KeyValuePair<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>* blink::HeapAllocator::AllocateZeroedHashTableBacking<WTF::KeyValuePair<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>, WTF::HashTable<WTF::String, WTF::KeyValuePair<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>, WTF::KeyValuePairKeyExtractor, WTF::StringHash, WTF::HashMapValueTraits<WTF::HashTraits<WTF::String>, WTF::HashTraits<cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>>, WTF::HashTraits<WTF::String>, blink::HeapAllocator>>(unsigned long) ./../../third_party/blink/renderer/platform/heap/heap_allocator_impl.h:106:12
    #35 0x7f79022988e4 in WTF::HashTable<WTF::String, WTF::KeyValuePair<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>, WTF::KeyValuePairKeyExtractor, WTF::StringHash, WTF::HashMapValueTraits<WTF::HashTraits<WTF::String>, WTF::HashTraits<cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>>, WTF::HashTraits<WTF::String>, blink::HeapAllocator>::AllocateTable(unsigned int) ./../../third_party/blink/renderer/platform/wtf/hash_table.h:1707:14
    #36 0x7f79022988e4 in WTF::HashTable<WTF::String, WTF::KeyValuePair<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>, WTF::KeyValuePairKeyExtractor, WTF::StringHash, WTF::HashMapValueTraits<WTF::HashTraits<WTF::String>, WTF::HashTraits<cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>>, WTF::HashTraits<WTF::String>, blink::HeapAllocator>::Rehash(unsigned int, WTF::KeyValuePair<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>*) ./../../third_party/blink/renderer/platform/wtf/hash_table.h:1944:26
    #37 0x7f79022988e4 in WTF::HashTable<WTF::String, WTF::KeyValuePair<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>, WTF::KeyValuePairKeyExtractor, WTF::StringHash, WTF::HashMapValueTraits<WTF::HashTraits<WTF::String>, WTF::HashTraits<cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>>, WTF::HashTraits<WTF::String>, blink::HeapAllocator>::Shrink() ./../../third_party/blink/renderer/platform/wtf/hash_table.h:918:19
    #38 0x7f79022988e4 in WTF::HashTable<WTF::String, WTF::KeyValuePair<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>, WTF::KeyValuePairKeyExtractor, WTF::StringHash, WTF::HashMapValueTraits<WTF::HashTraits<WTF::String>, WTF::HashTraits<cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>>, WTF::HashTraits<WTF::String>, blink::HeapAllocator>::erase(WTF::KeyValuePair<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>> const*) ./../../third_party/blink/renderer/platform/wtf/hash_table.h:1632:5
    #39 0x7f790228ea18 in WTF::HashTable<WTF::String, WTF::KeyValuePair<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>, WTF::KeyValuePairKeyExtractor, WTF::StringHash, WTF::HashMapValueTraits<WTF::HashTraits<WTF::String>, WTF::HashTraits<cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>>, WTF::HashTraits<WTF::String>, blink::HeapAllocator>::erase(WTF::HashTableIterator<WTF::String, WTF::KeyValuePair<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>, WTF::KeyValuePairKeyExtractor, WTF::StringHash, WTF::HashMapValueTraits<WTF::HashTraits<WTF::String>, WTF::HashTraits<cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>>, WTF::HashTraits<WTF::String>, blink::HeapAllocator>) ./../../third_party/blink/renderer/platform/wtf/hash_table.h:1647:3
    #40 0x7f790228ea18 in WTF::HashMap<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>, WTF::StringHash, WTF::HashTraits<WTF::String>, WTF::HashTraits<cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>, blink::HeapAllocator>::erase(WTF::HashTableIteratorAdapter<WTF::HashTable<WTF::String, WTF::KeyValuePair<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>, WTF::KeyValuePairKeyExtractor, WTF::StringHash, WTF::HashMapValueTraits<WTF::HashTraits<WTF::String>, WTF::HashTraits<cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>>, WTF::HashTraits<WTF::String>, blink::HeapAllocator>, WTF::KeyValuePair<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>>) ./../../third_party/blink/renderer/platform/wtf/hash_map.h:604:9
    #41 0x7f790228ea18 in WTF::HashMap<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>, WTF::StringHash, WTF::HashTraits<WTF::String>, WTF::HashTraits<cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>>, blink::HeapAllocator>::Take(WTF::String const&) ./../../third_party/blink/renderer/platform/wtf/hash_map.h:638:3
    #42 0x7f790228ea18 in blink::MediaInspectorContextImpl::RemovePlayer(blink::WebString const&) ./../../third_party/blink/renderer/core/inspector/inspector_media_context_impl.cc:80:33
    #43 0x7f79022909df in blink::MediaInspectorContextImpl::CullPlayers(blink::WebString const&) ./../../third_party/blink/renderer/core/inspector/inspector_media_context_impl.cc:126:5
    #44 0x7f79022926ef in blink::MediaInspectorContextImpl::NotifyPlayerEvents(blink::WebString, blink::WebVector<blink::InspectorPlayerEvent> const&) ./../../third_party/blink/renderer/core/inspector/inspector_media_context_impl.cc:182:7
    #45 0x7f7930f28da5 in content::InspectorMediaEventHandler::SendQueuedMediaEvents(std::Cr::vector<media::MediaLogRecord, std::Cr::allocator<media::MediaLogRecord>>) ./../../content/renderer/media/inspector_media_event_handler.cc:151:25
    #46 0x7f7930f192dd in content::BatchingMediaLog::SendQueuedMediaEvents() ./../../content/renderer/media/batching_media_log.cc:238:14

### ct...@chromium.org (2022-06-01)

Thanks for digging into this tmathmeyer@! Tentatively setting FoundIn-102 per the initial report, but it would be good to have confirmation whether you are able to trigger the crash in M-102 as well.

### [Deleted User] (2022-06-01)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-06-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/57e905d0943695fb96a1a1a251382d15a9b2fee1

commit 57e905d0943695fb96a1a1a251382d15a9b2fee1
Author: Ted Meyer <tmathmeyer@chromium.org>
Date: Wed Jun 01 17:09:14 2022

Post media log destruction to avoid destruction

SendQueuedMediaEvents is able to tickle oilpan just enough to cause
the owning BatchingMediaLog to be destroyed in the middle of executing,
causing a UAF.

Bug: 1317714
Change-Id: Iac2f32aee70eee183be279b372beb2ff39e6c5a0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3682060
Reviewed-by: Frank Liberato <liberato@chromium.org>
Auto-Submit: Ted (Chromium) Meyer <tmathmeyer@chromium.org>
Reviewed-by: Thomas Guilbert <tguilbert@chromium.org>
Commit-Queue: Ted (Chromium) Meyer <tmathmeyer@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1009670}

[modify] https://crrev.com/57e905d0943695fb96a1a1a251382d15a9b2fee1/third_party/blink/renderer/modules/webcodecs/codec_logger.h


### tm...@chromium.org (2022-06-01)

@cthomp this issue has existed long before 102, and will need to be merged back. 

### tm...@chromium.org (2022-06-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-02)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-06-06)

going outside the norm and manually adding merge review labels as I am unsure as to why sheriffbot did not already 

### ad...@google.com (2022-06-06)

Sheriffbot didn't add Merge-Request because there's no M- label, but I'm not sure why it didn't add an M- label. Perhaps it's something to do with the weird label removed in https://crbug.com/chromium/1317714#c28. I've reported the apparent sheriffbot bug as https://crbug.com/chromium/1333525.

In any case, approving merge of this fix to M102 and M103. Please merge to branches 5005 and 5060, assuming no problems have shown up in Canary related to this.

### gi...@appspot.gserviceaccount.com (2022-06-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c8d546614aa2b6a0c197dcfa549642f50a00eacf

commit c8d546614aa2b6a0c197dcfa549642f50a00eacf
Author: Ted Meyer <tmathmeyer@chromium.org>
Date: Mon Jun 06 21:18:48 2022

Post media log destruction to avoid destruction

SendQueuedMediaEvents is able to tickle oilpan just enough to cause
the owning BatchingMediaLog to be destroyed in the middle of executing,
causing a UAF.

(cherry picked from commit 57e905d0943695fb96a1a1a251382d15a9b2fee1)

Bug: 1317714
Change-Id: Iac2f32aee70eee183be279b372beb2ff39e6c5a0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3682060
Reviewed-by: Frank Liberato <liberato@chromium.org>
Auto-Submit: Ted (Chromium) Meyer <tmathmeyer@chromium.org>
Reviewed-by: Thomas Guilbert <tguilbert@chromium.org>
Commit-Queue: Ted (Chromium) Meyer <tmathmeyer@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1009670}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3691325
Reviewed-by: Dan Sanders <sandersd@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Dan Sanders <sandersd@chromium.org>
Cr-Commit-Position: refs/branch-heads/5005@{#1126}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/c8d546614aa2b6a0c197dcfa549642f50a00eacf/third_party/blink/renderer/modules/webcodecs/codec_logger.h


### gi...@appspot.gserviceaccount.com (2022-06-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8dfc224b256d42bbe11f317b1b9882c648589052

commit 8dfc224b256d42bbe11f317b1b9882c648589052
Author: Ted Meyer <tmathmeyer@chromium.org>
Date: Mon Jun 06 21:19:08 2022

Post media log destruction to avoid destruction

SendQueuedMediaEvents is able to tickle oilpan just enough to cause
the owning BatchingMediaLog to be destroyed in the middle of executing,
causing a UAF.

(cherry picked from commit 57e905d0943695fb96a1a1a251382d15a9b2fee1)

Bug: 1317714
Change-Id: Iac2f32aee70eee183be279b372beb2ff39e6c5a0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3682060
Reviewed-by: Frank Liberato <liberato@chromium.org>
Auto-Submit: Ted (Chromium) Meyer <tmathmeyer@chromium.org>
Reviewed-by: Thomas Guilbert <tguilbert@chromium.org>
Commit-Queue: Ted (Chromium) Meyer <tmathmeyer@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1009670}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3691383
Reviewed-by: Dan Sanders <sandersd@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5060@{#615}
Cr-Branched-From: b83393d0f4038aeaf67f970a024d8101df7348d1-refs/heads/main@{#1002911}

[modify] https://crrev.com/8dfc224b256d42bbe11f317b1b9882c648589052/third_party/blink/renderer/modules/webcodecs/codec_logger.h


### ad...@google.com (2022-06-06)

[Empty comment from Monorail migration]

### ad...@google.com (2022-06-06)

It turns out that this resulted in https://crbug.com/chromium/1333333, the fix for which we can't accommodate within the M102 security refresh, so we won't be releasing this fix in the M102 refresh after all. It will shortly be reverted.

### gi...@appspot.gserviceaccount.com (2022-06-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/600c54b08de09573bcfa2a88e02eac5c12e6b815

commit 600c54b08de09573bcfa2a88e02eac5c12e6b815
Author: Ted (Chromium) Meyer <tmathmeyer@chromium.org>
Date: Mon Jun 06 22:15:11 2022

Revert "Post media log destruction to avoid destruction"

This reverts commit c8d546614aa2b6a0c197dcfa549642f50a00eacf.

Reason for revert: needs additional fix

Original change's description:
> Post media log destruction to avoid destruction
>
> SendQueuedMediaEvents is able to tickle oilpan just enough to cause
> the owning BatchingMediaLog to be destroyed in the middle of executing,
> causing a UAF.
>
> (cherry picked from commit 57e905d0943695fb96a1a1a251382d15a9b2fee1)
>
> Bug: 1317714
> Change-Id: Iac2f32aee70eee183be279b372beb2ff39e6c5a0
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3682060
> Reviewed-by: Frank Liberato <liberato@chromium.org>
> Auto-Submit: Ted (Chromium) Meyer <tmathmeyer@chromium.org>
> Reviewed-by: Thomas Guilbert <tguilbert@chromium.org>
> Commit-Queue: Ted (Chromium) Meyer <tmathmeyer@chromium.org>
> Cr-Original-Commit-Position: refs/heads/main@{#1009670}
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3691325
> Reviewed-by: Dan Sanders <sandersd@chromium.org>
> Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
> Commit-Queue: Dan Sanders <sandersd@chromium.org>
> Cr-Commit-Position: refs/branch-heads/5005@{#1126}
> Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

Bug: 1317714
Change-Id: Iea4631830222937134cb4fa0d2d75da87e59aea4
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3692201
Commit-Queue: Prudhvikumar Bommana <pbommana@google.com>
Owners-Override: Prudhvikumar Bommana <pbommana@google.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Prudhvikumar Bommana <pbommana@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1132}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/600c54b08de09573bcfa2a88e02eac5c12e6b815/third_party/blink/renderer/modules/webcodecs/codec_logger.h


### am...@google.com (2022-06-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-13)

Congratulations, Cassidy Kim! The VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts and nice work! 

### am...@google.com (2022-06-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2022-12-13)

I believe this was released in M103 in the end. emilykim8708@ sorry you didn't get a release notes credit or a CVE assigned at the time, we'll take care of it!

### em...@gmail.com (2022-12-13)

Thanks for letting me know.

### pg...@google.com (2023-02-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2023-07-28)

This issue was migrated from crbug.com/chromium/1317714?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059414)*
