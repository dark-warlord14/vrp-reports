# uaf in blink::MediaInspectorContextImpl::CullPlayers(blink::WebString const&)

| Field | Value |
|-------|-------|
| **Issue ID** | [40058732](https://issues.chromium.org/issues/40058732) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | tm...@chromium.org |
| **Created** | 2022-02-09 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36

Steps to reproduce the problem:

OS Version:
Ubuntu 20.04
tested chrome version:
Chromium 99.0.4844.11(with asan build)
Version 100.0.4880.0 (Developer Build) (64-bit) gs://chromium-browser-asan/linux-release/asan-linux-release-968952.zip

This issue is not stable to reproduce with a single browser.
I used different user-data-dir to open one by one to reproduce.
In my local tests it is stable until the sixth browser is opened.

。/chrome --incognito --user-data-dir=/tmp/xx1  http://localhost:8000/crash.html
。/chrome --incognito --user-data-dir=/tmp/xx2  http://localhost:8000/crash.html
。/chrome --incognito --user-data-dir=/tmp/xx3  http://localhost:8000/crash.html
。/chrome --incognito --user-data-dir=/tmp/xx4  http://localhost:8000//crash.html
。/chrome --incognito --user-data-dir=/tmp/xx5  http://localhost:8000//crash.html
。/chrome --incognito --user-data-dir=/tmp/xx6  http://localhost:8000//crash.html

What is the expected behavior?

What went wrong?
==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x6160004fa840 at pc 0x55aa718dbc02 bp 0x7ffdc2125ac0 sp 0x7ffdc2125ab8
READ of size 8 at 0x6160004fa840 thread T0 (chrome)
    #0 0x55aa718dbc01 in blink::WebString::WebString(WTF::String const&) web_string.cc:?
    #1 0x55aa718dbc01 in ?? ??:0
    #2 0x55aa7006fc2f in blink::MediaInspectorContextImpl::CullPlayers(blink::WebString const&) inspector_media_context_impl.cc:?
    #3 0x55aa7006fc2f in ?? ??:0
    #4 0x55aa70071c91 in blink::MediaInspectorContextImpl::NotifyPlayerEvents(blink::WebString, blink::WebVector<blink::InspectorPlayerEvent> const&) inspector_media_context_impl.cc:?
    #5 0x55aa70071c91 in ?? ??:0
    #6 0x55aa730c2a55 in content::InspectorMediaEventHandler::SendQueuedMediaEvents(std::__1::vector<media::MediaLogRecord, std::__1::allocator<media::MediaLogRecord> >) inspector_media_event_handler.cc:?
    #7 0x55aa730c2a55 in ?? ??:0
    #8 0x55aa730c7454 in content::BatchingMediaLog::SendQueuedMediaEvents() batching_media_log.cc:?
    #9 0x55aa730c7454 in ?? ??:0
    #10 0x55aa730ca750 in base::internal::Invoker<base::internal::BindState<void (content::BatchingMediaLog::*)(), base::WeakPtr<content::BatchingMediaLog> >, void ()>::RunOnce(base::internal::BindStateBase*) batching_media_log.cc:?
    #11 0x55aa730ca750 in ?? ??:0
    #12 0x55aa6242bb33 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) task_annotator.cc:?
    #13 0x55aa6242bb33 in ?? ??:0
    #14 0x55aa6246d1c3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) thread_controller_with_message_pump_impl.cc:?
    #15 0x55aa6246d1c3 in ?? ??:0
    #16 0x55aa6246c9d7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() thread_controller_with_message_pump_impl.cc:?
    #17 0x55aa6246c9d7 in ?? ??:0
    #18 0x55aa6246dd91 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() thread_controller_with_message_pump_impl.cc:?
    #19 0x55aa6246dd91 in ?? ??:0
    #20 0x55aa62324b6f in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) message_pump_default.cc:?
    #21 0x55aa62324b6f in ?? ??:0
    #22 0x55aa6246e457 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) thread_controller_with_message_pump_impl.cc:?
    #23 0x55aa6246e457 in ?? ??:0
    #24 0x55aa623a73c9 in base::RunLoop::Run(base::Location const&) run_loop.cc:?
    #25 0x55aa623a73c9 in ?? ??:0
    #26 0x55aa7650f8ec in content::RendererMain(content::MainFunctionParams) renderer_main.cc:?
    #27 0x55aa7650f8ec in ?? ??:0
    #28 0x55aa611f9f92 in content::RunZygote(content::ContentMainDelegate*) content_main_runner_impl.cc:?
    #29 0x55aa611f9f92 in ?? ??:0
    #30 0x55aa611fba13 in content::RunOtherNamedProcessTypeMain(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, content::MainFunctionParams, content::ContentMainDelegate*) content_main_runner_impl.cc:?
    #31 0x55aa611fba13 in ?? ??:0
    #32 0x55aa611fd7af in content::ContentMainRunnerImpl::Run() content_main_runner_impl.cc:?
    #33 0x55aa611fd7af in ?? ??:0
    #34 0x55aa611f7393 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content_main.cc:?
    #35 0x55aa611f7393 in ?? ??:0
    #36 0x55aa611f7a6c in content::ContentMain(content::ContentMainParams) content_main.cc:?
    #37 0x55aa611f7a6c in ?? ??:0
    #38 0x55aa53f366b6 in ChromeMain ??:?
    #39 0x55aa53f366b6 in ?? ??:0
    #40 0x55aa53f36468 in main chrome_exe_main_aura.cc:?
    #41 0x55aa53f36468 in ?? ??:0
    #42 0x7ff035b77082 in __libc_start_main ??:?
    #43 0x7ff035b77082 in ?? ??:0

0x6160004fa840 is located 192 bytes inside of 592-byte region [0x6160004fa780,0x6160004fa9d0)
freed by thread T0 (chrome) here:
    #0 0x55aa53f02952 in __interceptor_free ??:?
    #1 0x55aa53f02952 in ?? ??:0
    #2 0x55aa5f063ad2 in WTF::Vector<WTF::String, 0u, WTF::PartitionAllocator>::ReallocateBuffer(unsigned int) page_state.mojom-blink.cc:?
    #3 0x55aa5f063ad2 in ?? ??:0
    #4 0x55aa7007843c in void WTF::Vector<WTF::String, 0u, WTF::PartitionAllocator>::AppendSlowCase<blink::WebString const&>(blink::WebString const&) inspector_media_context_impl.cc:?
    #5 0x55aa7007843c in ?? ??:0
    #6 0x55aa730c7822 in content::BatchingMediaLog::OnWebMediaPlayerDestroyedLocked() batching_media_log.cc:?
    #7 0x55aa730c7822 in ?? ??:0
    #8 0x55aa56f8514a in media::MediaLog::OnWebMediaPlayerDestroyed() media_log.cc:?
    #9 0x55aa56f8514a in ?? ??:0
    #10 0x55aa766d7536 in blink::WebMediaPlayerImpl::~WebMediaPlayerImpl() web_media_player_impl.cc:?
    #11 0x55aa766d7536 in ?? ??:0
    #12 0x55aa766d925d in blink::WebMediaPlayerImpl::~WebMediaPlayerImpl() web_media_player_impl.cc:?
    #13 0x55aa766d925d in ?? ??:0
    #14 0x55aa6fc22c7c in blink::HTMLMediaElement::ClearMediaPlayerAndAudioSourceProviderClientWithoutLocking() html_media_element.cc:?
    #15 0x55aa6fc22c7c in ?? ??:0
    #16 0x55aa6fc590d2 in blink::HTMLMediaElement::InvokePreFinalizer(cppgc::LivenessBroker const&, void*) html_media_element.cc:?
    #17 0x55aa6fc590d2 in ?? ??:0
    #18 0x55aa5e25c0ca in cppgc::internal::PreFinalizerHandler::InvokePreFinalizers() prefinalizer-handler.cc:?
    #19 0x55aa5e25c0ca in ?? ??:0
    #20 0x55aa5e23ab03 in cppgc::internal::HeapBase::ExecutePreFinalizers() heap-base.cc:?
    #21 0x55aa5e23ab03 in ?? ??:0
    #22 0x55aa5cda92af in v8::internal::CppHeap::TraceEpilogue() cpp-heap.cc:?
    #23 0x55aa5cda92af in ?? ??:0
    #24 0x55aa5cdbac39 in v8::internal::LocalEmbedderHeapTracer::TraceEpilogue() embedder-tracing.cc:?
    #25 0x55aa5cdbac39 in ?? ??:0
    #26 0x55aa5ce4868c in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::GCCallbackFlags) heap.cc:?
    #27 0x55aa5ce4868c in ?? ??:0
    #28 0x55aa5ce40201 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) heap.cc:?
    #29 0x55aa5ce40201 in ?? ??:0
    #30 0x55aa5ce45426 in v8::internal::Heap::FinalizeIncrementalMarkingAtomically(v8::internal::GarbageCollectionReason) heap.cc:?
    #31 0x55aa5ce45426 in ?? ??:0
    #32 0x55aa5cda974b in non-virtual thunk to v8::internal::CppHeap::AllocatedObjectSizeIncreased(unsigned long) cpp-heap.cc:?
    #33 0x55aa5cda974b in ?? ??:0
    #34 0x55aa5e2607d3 in cppgc::internal::StatsCollector::AllocatedObjectSizeSafepointImpl() stats-collector.cc:?
    #35 0x55aa5e2607d3 in ?? ??:0
    #36 0x55aa5e2508f5 in cppgc::internal::ObjectAllocator::OutOfLineAllocate(cppgc::internal::NormalPageSpace&, unsigned long, cppgc::internal::AlignVal, unsigned short) object-allocator.cc:?
    #37 0x55aa5e2508f5 in ?? ??:0
    #38 0x55aa700775c3 in blink::HeapHashTableBacking<WTF::HashTable<WTF::String, WTF::KeyValuePair<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy> >, WTF::KeyValuePairKeyExtractor, WTF::StringHash, WTF::HashMapValueTraits<WTF::HashTraits<WTF::String>, WTF::HashTraits<cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy> > >, WTF::HashTraits<WTF::String>, blink::HeapAllocator> >* cppgc::MakeGarbageCollectedTrait<blink::HeapHashTableBacking<WTF::HashTable<WTF::String, WTF::KeyValuePair<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy> >, WTF::KeyValuePairKeyExtractor, WTF::StringHash, WTF::HashMapValueTraits<WTF::HashTraits<WTF::String>, WTF::HashTraits<cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy> > >, WTF::HashTraits<WTF::String>, blink::HeapAllocator> > >::Call<>(cppgc::AllocationHandle&, unsigned long) inspector_media_context_impl.cc:?
    #39 0x55aa700775c3 in ?? ??:0
    #40 0x55aa70077b62 in WTF::HashTable<WTF::String, WTF::KeyValuePair<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy> >, WTF::KeyValuePairKeyExtractor, WTF::StringHash, WTF::HashMapValueTraits<WTF::HashTraits<WTF::String>, WTF::HashTraits<cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy> > >, WTF::HashTraits<WTF::String>, blink::HeapAllocator>::erase(WTF::KeyValuePair<WTF::String, cppgc::internal::BasicMember<blink::MediaPlayer, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy> > const*) inspector_media_context_impl.cc:?
    #41 0x55aa70077b62 in ?? ??:0
    #42 0x55aa7006df78 in blink::MediaInspectorContextImpl::RemovePlayer(blink::WebString const&) inspector_media_context_impl.cc:?
    #43 0x55aa7006df78 in ?? ??:0
    #44 0x55aa7006fc3b in blink::MediaInspectorContextImpl::CullPlayers(blink::WebString const&) inspector_media_context_impl.cc:?
    #45 0x55aa7006fc3b in ?? ??:0
    #46 0x55aa70071c91 in blink::MediaInspectorContextImpl::NotifyPlayerEvents(blink::WebString, blink::WebVector<blink::InspectorPlayerEvent> const&) inspector_media_context_impl.cc:?
    #47 0x55aa70071c91 in ?? ??:0
    #48 0x55aa730c2a55 in content::InspectorMediaEventHandler::SendQueuedMediaEvents(std::__1::vector<media::MediaLogRecord, std::__1::allocator<media::MediaLogRecord> >) inspector_media_event_handler.cc:?
    #49 0x55aa730c2a55 in ?? ??:0
    #50 0x55aa730c7454 in content::BatchingMediaLog::SendQueuedMediaEvents() batching_media_log.cc:?
    #51 0x55aa730c7454 in ?? ??:0
    #52 0x55aa730ca750 in base::internal::Invoker<base::internal::BindState<void (content::BatchingMediaLog::*)(), base::WeakPtr<content::BatchingMediaLog> >, void ()>::RunOnce(base::internal::BindStateBase*) batching_media_log.cc:?
    #53 0x55aa730ca750 in ?? ??:0
    #54 0x55aa6242bb33 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) task_annotator.cc:?
    #55 0x55aa6242bb33 in ?? ??:0
    #56 0x55aa6246d1c3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) thread_controller_with_message_pump_impl.cc:?
    #57 0x55aa6246d1c3 in ?? ??:0
    #58 0x55aa6246c9d7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() thread_controller_with_message_pump_impl.cc:?
    #59 0x55aa6246c9d7 in ?? ??:0

previously allocated by thread T0 (chrome) here:
    #0 0x55aa53f02bf6 in __interceptor_malloc ??:?
    #1 0x55aa53f02bf6 in ?? ??:0
    #2 0x55aa6256b498 in base::PartitionRoot<true>::Alloc(unsigned long, char const*) partition_root.cc:?
    #3 0x55aa6256b498 in ?? ??:0
    #4 0x55aa5f0639e1 in WTF::Vector<WTF::String, 0u, WTF::PartitionAllocator>::ReallocateBuffer(unsigned int) page_state.mojom-blink.cc:?
    #5 0x55aa5f0639e1 in ?? ??:0
    #6 0x55aa7007843c in void WTF::Vector<WTF::String, 0u, WTF::PartitionAllocator>::AppendSlowCase<blink::WebString const&>(blink::WebString const&) inspector_media_context_impl.cc:?
    #7 0x55aa7007843c in ?? ??:0
    #8 0x55aa730c7822 in content::BatchingMediaLog::OnWebMediaPlayerDestroyedLocked() batching_media_log.cc:?
    #9 0x55aa730c7822 in ?? ??:0
    #10 0x55aa56f8514a in media::MediaLog::OnWebMediaPlayerDestroyed() media_log.cc:?
    #11 0x55aa56f8514a in ?? ??:0
    #12 0x55aa766d7536 in blink::WebMediaPlayerImpl::~WebMediaPlayerImpl() web_media_player_impl.cc:?
    #13 0x55aa766d7536 in ?? ??:0
    #14 0x55aa766d925d in blink::WebMediaPlayerImpl::~WebMediaPlayerImpl() web_media_player_impl.cc:?
    #15 0x55aa766d925d in ?? ??:0
    #16 0x55aa6fc22c7c in blink::HTMLMediaElement::ClearMediaPlayerAndAudioSourceProviderClientWithoutLocking() html_media_element.cc:?
    #17 0x55aa6fc22c7c in ?? ??:0
    #18 0x55aa6fc590d2 in blink::HTMLMediaElement::InvokePreFinalizer(cppgc::LivenessBroker const&, void*) html_media_element.cc:?
    #19 0x55aa6fc590d2 in ?? ??:0
    #20 0x55aa5e25c0ca in cppgc::internal::PreFinalizerHandler::InvokePreFinalizers() prefinalizer-handler.cc:?
    #21 0x55aa5e25c0ca in ?? ??:0
    #22 0x55aa5e23ab03 in cppgc::internal::HeapBase::ExecutePreFinalizers() heap-base.cc:?
    #23 0x55aa5e23ab03 in ?? ??:0
    #24 0x55aa5cda92af in v8::internal::CppHeap::TraceEpilogue() cpp-heap.cc:?
    #25 0x55aa5cda92af in ?? ??:0
    #26 0x55aa5cdbac39 in v8::internal::LocalEmbedderHeapTracer::TraceEpilogue() embedder-tracing.cc:?
    #27 0x55aa5cdbac39 in ?? ??:0
    #28 0x55aa5ce4868c in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::GCCallbackFlags) heap.cc:?
    #29 0x55aa5ce4868c in ?? ??:0
    #30 0x55aa5ce40201 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) heap.cc:?
    #31 0x55aa5ce40201 in ?? ??:0
    #32 0x55aa5ce45426 in v8::internal::Heap::FinalizeIncrementalMarkingAtomically(v8::internal::GarbageCollectionReason) heap.cc:?
    #33 0x55aa5ce45426 in ?? ??:0
    #34 0x55aa5cda974b in non-virtual thunk to v8::internal::CppHeap::AllocatedObjectSizeIncreased(unsigned long) cpp-heap.cc:?
    #35 0x55aa5cda974b in ?? ??:0
    #36 0x55aa5e2607d3 in cppgc::internal::StatsCollector::AllocatedObjectSizeSafepointImpl() stats-collector.cc:?
    #37 0x55aa5e2607d3 in ?? ??:0
    #38 0x55aa5e2508f5 in cppgc::internal::ObjectAllocator::OutOfLineAllocate(cppgc::internal::NormalPageSpace&, unsigned long, cppgc::internal::AlignVal, unsigned short) object-allocator.cc:?
    #39 0x55aa5e2508f5 in ?? ??:0
    #40 0x55aa71bf33e9 in blink::HeapVectorBacking<cppgc::internal::BasicMember<blink::MediaStreamComponent, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>, WTF::VectorTraits<cppgc::internal::BasicMember<blink::MediaStreamComponent, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy> > >* cppgc::MakeGarbageCollectedTrait<blink::HeapVectorBacking<cppgc::internal::BasicMember<blink::MediaStreamComponent, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>, WTF::VectorTraits<cppgc::internal::BasicMember<blink::MediaStreamComponent, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy> > > >::Call<>(cppgc::AllocationHandle&, unsigned long) media_stream_descriptor.cc:?
    #41 0x55aa71bf33e9 in ?? ??:0
    #42 0x55aa71bf2969 in WTF::Vector<cppgc::internal::BasicMember<blink::MediaStreamComponent, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>, 0u, blink::HeapAllocator>::ReserveCapacity(unsigned int) media_stream_descriptor.cc:?
    #43 0x55aa71bf2969 in ?? ??:0
    #44 0x55aa743ed403 in WTF::Vector<cppgc::internal::BasicMember<blink::MediaStreamComponent, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>, 0u, blink::HeapAllocator>::operator=(WTF::Vector<cppgc::internal::BasicMember<blink::MediaStreamComponent, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy>, 0u, blink::HeapAllocator> const&) webmediaplayer_ms_compositor.cc:?
    #45 0x55aa743ed403 in ?? ??:0
    #46 0x55aa750aa406 in blink::MediaRecorderHandler::Start(int) media_recorder_handler.cc:?
    #47 0x55aa750aa406 in ?? ??:0
    #48 0x55aa750debe0 in blink::MediaRecorder::start(int, blink::ExceptionState&) media_recorder.cc:?
    #49 0x55aa750debe0 in ?? ??:0
    #50 0x55aa750ef455 in blink::(anonymous namespace)::v8_media_recorder::StartOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) v8_media_recorder.cc:?
    #51 0x55aa750ef455 in ?? ??:0
    #52 0x55aa5c9780e7 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) builtins-api.cc:?
    #53 0x55aa5c9780e7 in ?? ??:0
    #54 0x55aa5c975d33 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) builtins-api.cc:?
    #55 0x55aa5c975d33 in ?? ??:0
    #56 0x55aa5c97376c in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) builtins-api.cc:?
    #57 0x55aa5c97376c in ?? ??:0
    #58 0x55aa5c972cba in v8::internal::Builtin_HandleApiCall(int, unsigned long*, v8::internal::Isolate*) builtins-api.cc:?
    #59 0x55aa5c972cba in ?? ??:0

Did this work before? N/A 

Chrome version: 99.0.4844.11  Channel: stable
OS Version: 20.04

## Attachments

- deleted (application/octet-stream, 0 B)
- [xx.mp3](attachments/xx.mp3) (application/octet-stream, 2.3 KB)
- [crash.html](attachments/crash.html) (text/plain, 504 B)
- [crash.html](attachments/crash.html) (text/plain, 623 B)
- [exploit.zip](attachments/exploit.zip) (application/octet-stream, 1.1 KB)

## Timeline

### [Deleted User] (2022-02-09)

[Empty comment from Monorail migration]

### em...@gmail.com (2022-02-09)

I uploaded new poc.

### cl...@chromium.org (2022-02-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5472020779040768.

### ad...@google.com (2022-02-09)

Thanks for the report. I'm working on reproducing this manually but I'm uploading to ClusterFuzz just in case we get lucky.

### ad...@google.com (2022-02-09)

I got a different error in the same code from running this just once:

Received signal 11 SEGV_ACCERR 61a8000f6078
    #0 0x55dca72c0bff in backtrace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4277:13
    #1 0x55dcb5c570b9 in base::debug::CollectStackTrace(void**, unsigned long) ./../../base/debug/stack_trace_posix.cc:874:39
    #2 0x55dcb5a0a583 in StackTrace ./../../base/debug/stack_trace.cc:222:12
    #3 0x55dcb5a0a583 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:219:28
    #4 0x55dcb5c55b7e in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:371:3
    #5 0x7fbc267f83c0 in __funlockfile ??:?
    #6 0x55dcc3e2911c in ~scoped_refptr ./../../base/memory/scoped_refptr.h:222:9
    #7 0x55dcc3e2911c in ~String ./../../third_party/blink/renderer/platform/wtf/text/wtf_string.h:58:18
    #8 0x55dcc3e2911c in Destruct ./../../third_party/blink/renderer/platform/wtf/vector.h:138:15
    #9 0x55dcc3e2911c in Shrink ./../../third_party/blink/renderer/platform/wtf/vector.h:1646:3
    #10 0x55dcc3e2911c in pop_back ./../../third_party/blink/renderer/platform/wtf/vector.h:1225:5
    #11 0x55dcc3e2911c in blink::MediaInspectorContextImpl::CullPlayers(blink::WebString const&) ./../../third_party/blink/renderer/core/inspector/inspector_media_context_impl.cc:127:21
    #12 0x55dcc3e2ad42 in blink::MediaInspectorContextImpl::NotifyPlayerEvents(blink::WebString, blink::WebVector<blink::InspectorPlayerEvent> const&) ./../../third_party/blink/renderer/core/inspector/inspector_media_context_impl.cc:182:7
    #13 0x55dcc6e61bc6 in content::InspectorMediaEventHandler::SendQueuedMediaEvents(std::__1::vector<media::MediaLogRecord, std::__1::allocator<media::MediaLogRecord> >) ./../../content/renderer/media/inspector_media_event_handler.cc:111:25
    #14 0x55dcc6e665c5 in content::BatchingMediaLog::SendQueuedMediaEvents() ./../../content/renderer/media/batching_media_log.cc:232:14
    #15 0x55dcc6e698c1 in Invoke<void (content::BatchingMediaLog::*)(), base::WeakPtr<content::BatchingMediaLog> > ./../../base/bind_internal.h:542:12
    #16 0x55dcc6e698c1 in MakeItSo<void (content::BatchingMediaLog::*)(), base::WeakPtr<content::BatchingMediaLog> > ./../../base/bind_internal.h:726:5
    #17 0x55dcc6e698c1 in RunImpl<void (content::BatchingMediaLog::*)(), std::__1::tuple<base::WeakPtr<content::BatchingMediaLog> >, 0UL> ./../../base/bind_internal.h:779:12
    #18 0x55dcc6e698c1 in base::internal::Invoker<base::internal::BindState<void (content::BatchingMediaLog::*)(), base::WeakPtr<content::BatchingMediaLog> >, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:748:12
    #19 0x55dcb5b6d244 in Run ./../../base/callback.h:142:12
    #20 0x55dcb5b6d244 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:135:32
    #21 0x55dcb5bb02f8 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:389:29)> ./../../base/task/common/task_annotator.h:74:5
    #22 0x55dcb5bb02f8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:387:21
    #23 0x55dcb5baf9d5 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:292:41
    #24 0x55dcb5bb0fb2 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #25 0x55dcb5a661e0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:38:55
    #26 0x55dcb5bb1678 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:499:12
    #27 0x55dcb5ae8aaa in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:141:14
    #28 0x55dcc9af67cd in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:290:16
    #29 0x55dcb49395f3 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:610:14
    #30 0x55dcb493b104 in content::RunOtherNamedProcessTypeMain(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:692:12
    #31 0x55dcb493cea0 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1043:10
    #32 0x55dcb49369f4 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:399:36
    #33 0x55dcb49370cd in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:427:10
    #34 0x55dca733a477 in ChromeMain ./../../chrome/app/chrome_main.cc:176:12
    #35 0x55dca733a229 in main ./../../chrome/app/chrome_exe_main_aura.cc:17:10
    #36 0x7fbc2514e0b3 in __libc_start_main ??:0:0
    #37 0x55dca72874ea in _start ??:0:0
  r8: 0000000000000000  r9: 00000fd480029c82 r10: 00000c2a00001341 r11: 0000630000000400
 r12: 0000000000000000 r13: 00000c3580016c0f r14: 000061a0000f6080 r15: 00000007fffffff8
  di: 000060400027c890  si: 00007ea40014e430  bp: 00007ffcc78354b0  bx: 00007ffcc78353e0
  dx: 00000ff784469700  ax: 00000000ffffffff  cx: 00000000ffffffff  sp: 00007ffcc78353e0
  ip: 000055dcc3e2911c efl: 0000000000010246 cgf: 002b000000000033 erf: 0000000000000004
 trp: 000000000000000e msk: 0000000000000000 cr2: 000061a8000f6078
[end of stack trace]

This was on redshell with asan-linux-release-968952/chrome --user-data-dir=/tmp/ade1 ./crash.html

From the trace I assume this is an assertion failure rather than a memory safety problem, but it convinces me of some sort of lifetime problem in or around blink::MediaInspectorContextImpl::CullPlayers so I'll pass this over to engineering. Assuming a UaF in the renderer process => high severity. Assuming this affects all desktop platforms - not sure about Android.

I'll continue to try to reproduce the UaF itself, including back on stable builds.

Passing over to tmathmeyer@ to have a look

[Monorail components: Internals>Media]

### ad...@google.com (2022-02-09)

Unable to reproduce any problems with asan-linux-release-950353.

### ad...@google.com (2022-02-09)

I can reproduce the SEGV_ACCERR about 50% of the time on 968952 so I am now manually bisecting.

### [Deleted User] (2022-02-09)

[Empty comment from Monorail migration]

### ad...@google.com (2022-02-09)

I can't reproduce the problem on 964151 so I'm going to stop the bisection there. It appears that the problem was probably introduced subsequent to M99 branch point, and therefore FoundIn-100 is the correct label to represent affected branches. (The repro is of course not 100% reliable but that seems to be the way it's looking at the moment).

### ad...@google.com (2022-02-09)

(tmathmeyer@ the original reporter says they can reproduce this on M99. Once you've got to the root cause, please let us know the impacted versions back to M98, so we can work out which branches to merge this to.)

### em...@gmail.com (2022-02-09)

I uploaded new poc. 
modifed new WebAssembly.Memory({initial: 8}) ==> new WebAssembly.Memory({initial: 64}).grow(1);
 It will repro uaf rather than other crash.

### tm...@chromium.org (2022-02-10)

Thanks! taking a look for root cause RN.

### tm...@chromium.org (2022-02-10)

My thoughts are
A) there is a serious memory corruption bug here
B) It's not in media_inspector_context_impl

In defense of B), I found that not only can I make it crash reliably and without ASAN enabled, but that I sometimes get crashes outside of the media area, for example:
#
# Fatal error in ../../v8/src/heap/cppgc/marking-state.h, line 403
# Debug check failed: weak_containers_worklist_.Contains(&header).
#
#
#
#FailureMessage Object: 0x7ffe43e0a2b0#0 0x7fc725f94319 base::debug::CollectStackTrace()
#1 0x7fc725e8a5d3 base::debug::StackTrace::StackTrace()
#2 0x7fc7166f8d8d gin::(anonymous namespace)::PrintStackTrace()
#3 0x7fc710aeb9a8 V8_Fatal()
#4 0x7fc710aeb5a5 v8::base::(anonymous namespace)::DefaultDcheckHandler()
#5 0x7fc717b92372 cppgc::internal::ConservativeMarkingVisitor::VisitFullyConstructedConservatively()
#6 0x7fc717b9fc59 heap::base::(anonymous namespace)::IteratePointersImpl()
#7 0x7fc717b9fd33 (/chromium/src/out/Default/libv8.so+0x149fd32)
Received signal 4 ILL_ILLOPN 7fc710b056c3
#0 0x7fc725f94319 base::debug::CollectStackTrace()
#1 0x7fc725e8a5d3 base::debug::StackTrace::StackTrace()
#2 0x7fc725f93dd1 base::debug::(anonymous namespace)::StackDumpSignalHandler()
#3 0x7fc713f07200 (/usr/lib/x86_64-linux-gnu/libpthread-2.33.so+0x131ff)
#4 0x7fc710b056c3 v8::base::OS::Abort()
#5 0x7fc710aeb9b5 V8_Fatal()
#6 0x7fc710aeb5a5 v8::base::(anonymous namespace)::DefaultDcheckHandler()
#7 0x7fc717b92372 cppgc::internal::ConservativeMarkingVisitor::VisitFullyConstructedConservatively()
#8 0x7fc717b9fc59 heap::base::(anonymous namespace)::IteratePointersImpl()
#9 0x7fc717b9fd33 (/chromium/src/out/Default/libv8.so+0x149fd32)
  r8: 0000000000000000  r9: 00007ffe43e09500 r10: 00007fc710acf1ba r11: 00007fc710b056b0
 r12: 00007ffe43e0a570 r13: 00007fc710ad6573 r14: 0000000000000193 r15: 00007fc7169a905e
  di: 00007fc71384b660  si: 0000000000000000  bp: 00007ffe43e0a2a0  bx: 00007fc7138497a0
  dx: 0000000000000001  ax: 0000000000000000  cx: 0000000000000c00  sp: 00007ffe43e0a2a0
  ip: 00007fc710b056c3 efl: 0000000000010202 cgf: 002b000000000033 erf: 0000000000000000
 trp: 0000000000000006 msk: 0000000000000000 cr2: 0000000000000000
[end of stack trace]


Looks like the crash.html is hammering the media log with events as fast as it can, and the "cull players" method makes a lot of memory allocations and de-allocations, eventually getting caught in the crossfire. As for that function itself, it's only access point is thru InspectorMediaEventHandler::SendQueuedMediaEvents, which I put tracing events into and verified that it wasn't ever getting called "out of order" and CHECKs to ensure that none of the strings ever had null members.

### ad...@google.com (2022-02-10)

Ted has a theory, and if it's correct, this bug has been here ages => tagging as FoundIn-98

### tm...@chromium.org (2022-02-10)

yep, put out a CL for it here: https://chromium-review.googlesource.com/c/chromium/src/+/3451494

### [Deleted User] (2022-02-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-10)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tm...@chromium.org (2022-02-10)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-02-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/34526c3d0a857a22618e4d77c7f63b5ca6f8d3d2

commit 34526c3d0a857a22618e4d77c7f63b5ca6f8d3d2
Author: Ted Meyer <tmathmeyer@chromium.org>
Date: Mon Feb 14 21:00:35 2022

Guard BatchingMediaLog::event_handlers_ with lock

It seems that despite MediaLog::OnWebMediaPlayerDestroyed and
MediaLog::AddLogRecord both grabbing a lock,
BatchingMediaLog::AddLogRecordLocked can escape the lock handle by
posting BatchingMediaLog::SendQueuedMediaEvents, causing a race.

When the addition of an event is interrupted by the deletion of a player
due to player culling in MediaInspectorContextImpl, a UAF can occur.

R=dalecurtis

Bug: 1295786
Change-Id: I77df94988f806e4d98924669d27860e50455299d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3451494
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Commit-Queue: Ted (Chromium) Meyer <tmathmeyer@chromium.org>
Cr-Commit-Position: refs/heads/main@{#970815}

[modify] https://crrev.com/34526c3d0a857a22618e4d77c7f63b5ca6f8d3d2/content/renderer/media/batching_media_log.cc
[modify] https://crrev.com/34526c3d0a857a22618e4d77c7f63b5ca6f8d3d2/content/renderer/media/batching_media_log.h


### tm...@chromium.org (2022-02-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-15)

Requesting merge to stable M98 because latest trunk commit (970815) appears to be after stable branch point (950365).

Requesting merge to beta M99 because latest trunk commit (970815) appears to be after beta branch point (961656).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-02-15)

Since this fix CL just landed <24 hours ago, will review this for merge later in the weekend to allow for more bake time in Canary 

### [Deleted User] (2022-02-15)

Merge review required: M99 is already shipping to beta.

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
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-15)

Merge review required: M98 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tm...@chromium.org (2022-02-19)

Merge review answers for 98 (99 too)

1. Acceptable merges include fixes for urgent new regressions (especially user reports), urgent release blockers, and important security issues (medium severity or higher) requested by the security team.
This is (I think) Medium+ severity security issue from an external reporter.

2.  just this one: https://chromium-review.googlesource.com/c/chromium/src/+/3451494

3. yes

4. no

5. N/A

6. I'd say that yes, it should be tested. I'll re-upload the proof-of-concept from the reporter here. It should be slow and annoying on a fixed build (it's creating many new media elements per-second) but it shouldn't crash. It might take a few tries on a vulnerable build, since this proof-of-concept is non-deterministic. 

### am...@chromium.org (2022-02-22)

since this fix has been on canary for a week now, approving for merge to M98 and M99, please merge to branch 4758 for M98; please merge to branch 4844 ASAP so this fix can be included in next cut for M99 today. Thank you 

### gi...@appspot.gserviceaccount.com (2022-02-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5ee033bd9c6f7fb73c0c3af2ef6cad52855f8f28

commit 5ee033bd9c6f7fb73c0c3af2ef6cad52855f8f28
Author: Ted Meyer <tmathmeyer@chromium.org>
Date: Wed Feb 23 01:34:20 2022

Guard BatchingMediaLog::event_handlers_ with lock

It seems that despite MediaLog::OnWebMediaPlayerDestroyed and
MediaLog::AddLogRecord both grabbing a lock,
BatchingMediaLog::AddLogRecordLocked can escape the lock handle by
posting BatchingMediaLog::SendQueuedMediaEvents, causing a race.

When the addition of an event is interrupted by the deletion of a player
due to player culling in MediaInspectorContextImpl, a UAF can occur.

R=​dalecurtis

(cherry picked from commit 34526c3d0a857a22618e4d77c7f63b5ca6f8d3d2)

Bug: 1295786
Change-Id: I77df94988f806e4d98924669d27860e50455299d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3451494
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Commit-Queue: Ted (Chromium) Meyer <tmathmeyer@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#970815}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3482463
Auto-Submit: Ted (Chromium) Meyer <tmathmeyer@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4758@{#1192}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/5ee033bd9c6f7fb73c0c3af2ef6cad52855f8f28/content/renderer/media/batching_media_log.cc
[modify] https://crrev.com/5ee033bd9c6f7fb73c0c3af2ef6cad52855f8f28/content/renderer/media/batching_media_log.h


### [Deleted User] (2022-02-23)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-02-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ae144d56941a36e2c4e40a58c3fc508a4566a283

commit ae144d56941a36e2c4e40a58c3fc508a4566a283
Author: Ted Meyer <tmathmeyer@chromium.org>
Date: Wed Feb 23 01:48:56 2022

Guard BatchingMediaLog::event_handlers_ with lock

It seems that despite MediaLog::OnWebMediaPlayerDestroyed and
MediaLog::AddLogRecord both grabbing a lock,
BatchingMediaLog::AddLogRecordLocked can escape the lock handle by
posting BatchingMediaLog::SendQueuedMediaEvents, causing a race.

When the addition of an event is interrupted by the deletion of a player
due to player culling in MediaInspectorContextImpl, a UAF can occur.

R=​dalecurtis

(cherry picked from commit 34526c3d0a857a22618e4d77c7f63b5ca6f8d3d2)

Bug: 1295786
Change-Id: I77df94988f806e4d98924669d27860e50455299d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3451494
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Commit-Queue: Ted (Chromium) Meyer <tmathmeyer@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#970815}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3482761
Auto-Submit: Ted (Chromium) Meyer <tmathmeyer@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4844@{#786}
Cr-Branched-From: 007241ce2e6c8e5a7b306cc36c730cd07cd38825-refs/heads/main@{#961656}

[modify] https://crrev.com/ae144d56941a36e2c4e40a58c3fc508a4566a283/content/renderer/media/batching_media_log.cc
[modify] https://crrev.com/ae144d56941a36e2c4e40a58c3fc508a4566a283/content/renderer/media/batching_media_log.h


### rz...@google.com (2022-02-23)

[Empty comment from Monorail migration]

### rz...@google.com (2022-02-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-23)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-02-23)

1. Just https://crrev.com/c/3483655
2. Low, no conflicts
3. 98, 99
4. Yes

### rz...@google.com (2022-02-23)

Used the wrong label, the request is for 96

### [Deleted User] (2022-02-23)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-02-23)

The answer to the questionnaire is on https://crbug.com/chromium/1295786#c35

### gm...@google.com (2022-02-23)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-23)

Congratulations -- the VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts and reporting this issue to us! 

### gi...@appspot.gserviceaccount.com (2022-02-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6b2643846ae3a2ea925a0d3d0773bbf5c9565917

commit 6b2643846ae3a2ea925a0d3d0773bbf5c9565917
Author: Ted Meyer <tmathmeyer@chromium.org>
Date: Thu Feb 24 17:39:53 2022

[M96-LTS] Guard BatchingMediaLog::event_handlers_ with lock

It seems that despite MediaLog::OnWebMediaPlayerDestroyed and
MediaLog::AddLogRecord both grabbing a lock,
BatchingMediaLog::AddLogRecordLocked can escape the lock handle by
posting BatchingMediaLog::SendQueuedMediaEvents, causing a race.

When the addition of an event is interrupted by the deletion of a player
due to player culling in MediaInspectorContextImpl, a UAF can occur.

R=​dalecurtis

(cherry picked from commit 34526c3d0a857a22618e4d77c7f63b5ca6f8d3d2)

Bug: 1295786
Change-Id: I77df94988f806e4d98924669d27860e50455299d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3451494
Commit-Queue: Ted (Chromium) Meyer <tmathmeyer@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#970815}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3483655
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1508}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/6b2643846ae3a2ea925a0d3d0773bbf5c9565917/content/renderer/media/batching_media_log.cc
[modify] https://crrev.com/6b2643846ae3a2ea925a0d3d0773bbf5c9565917/content/renderer/media/batching_media_log.h


### rz...@google.com (2022-02-25)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-02-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-01)

[Empty comment from Monorail migration]

### da...@chromium.org (2022-04-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1295786?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1309120]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058732)*
