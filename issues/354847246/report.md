# UAF in blink::AudioBus::Zero()

| Field | Value |
|-------|-------|
| **Issue ID** | [354847246](https://issues.chromium.org/issues/354847246) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Media>Audio, Blink>WebAudio |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | ho...@chromium.org |
| **Created** | 2024-07-23 |
| **Bounty** | $3,000.00 |

## Description

tested OS:
ubuntu 22.04
MacOS 14.0

tested chrome version:
stable & beta & dev

also tested with latest asan built chrome (gs://chromium-browser-asan/linux-release/asan-linux-release-1331767.zip)

repro steps:
chrome --user-data-dir=/tmp/xx http://localhost:8880/crash.html
==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x518000055980 at pc 0x5583bc134d65 bp 0x78aa16535b90 sp 0x78aa16535360
WRITE of size 512 at 0x518000055980 thread T18 (Realtime AudioW)
    #0 0x5583bc134d64 in __asan_memset _asan_rtl_:3
    #1 0x5583de5c0e61 in Zero ./../../third_party/blink/renderer/platform/audio/audio_channel.h:0:0
    #2 0x5583de5c0e61 in blink::AudioBus::Zero() ./../../third_party/blink/renderer/platform/audio/audio_bus.cc:106:13
    #3 0x5583e211ebcd in blink::AudioWorkletHandler::Process(unsigned int) ./../../third_party/blink/renderer/modules/webaudio/audio_worklet_handler.cc:125:24
    #4 0x5583e20b0cf6 in blink::AudioHandler::ProcessIfNecessary(unsigned int) ./../../third_party/blink/renderer/modules/webaudio/audio_handler.cc:347:7
    #5 0x5583e218f8d2 in blink::DeferredTaskHandler::ProcessAutomaticPullNodes(unsigned int) ./../../third_party/blink/renderer/modules/webaudio/deferred_task_handler.cc:198:41
    #6 0x5583e2206a9f in blink::RealtimeAudioDestinationHandler::Render(blink::AudioBus*, unsigned int, blink::AudioIOPosition const&, blink::AudioCallbackMetric const&, base::TimeDelta, media::AudioGlitchInfo const&) ./../../third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc:246:37
    #7 0x5583e2212745 in PullFromCallback ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:589:14
    #8 0x5583e2212745 in blink::AudioDestination::ProvideResamplerInput(int, blink::AudioBus*) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:575:3
    #9 0x5583e22145fe in Invoke<void (blink::AudioDestination::*)(int, blink::AudioBus *), blink::AudioDestination *, int, blink::AudioBus *> ./../../base/functional/bind_internal.h:738:12
    #10 0x5583e22145fe in MakeItSo<void (blink::AudioDestination::*const &)(int, blink::AudioBus *), const std::__Cr::tuple<WTF::CrossThreadUnretainedWrapper<blink::AudioDestination> > &, int, blink::AudioBus *> ./../../base/functional/bind_internal.h:930:12
    #11 0x5583e22145fe in RunImpl<void (blink::AudioDestination::*const &)(int, blink::AudioBus *), const std::__Cr::tuple<WTF::CrossThreadUnretainedWrapper<blink::AudioDestination> > &, 0UL> ./../../base/functional/bind_internal.h:1067:14
    #12 0x5583e22145fe in base::internal::Invoker<base::internal::FunctorTraits<void (blink::AudioDestination::* const&)(int, blink::AudioBus*), blink::AudioDestination*>, base::internal::BindState<true, true, false, void (blink::AudioDestination::*)(int, blink::AudioBus*), WTF::CrossThreadUnretainedWrapper<blink::AudioDestination>>, void (int, blink::AudioBus*)>::Run(base::internal::BindStateBase*, int, blink::AudioBus*) ./../../base/functional/bind_internal.h:987:12
    #13 0x5583e21bd1ab in base::RepeatingCallback<void (int, blink::AudioBus*)>::Run(int, blink::AudioBus*) const & ./../../base/functional/callback.h:344:12
    #14 0x5583e21bc5f3 in Run ./../../third_party/blink/renderer/platform/wtf/functional.h:305:22
    #15 0x5583e21bc5f3 in blink::MediaMultiChannelResampler::ProvideResamplerInput(int, media::AudioBus*) ./../../third_party/blink/renderer/platform/audio/media_multi_channel_resampler.cc:59:12
    #16 0x5583e21bcec6 in Invoke<void (blink::MediaMultiChannelResampler::*)(int, media::AudioBus *), blink::MediaMultiChannelResampler *, int, media::AudioBus *> ./../../base/functional/bind_internal.h:738:12
    #17 0x5583e21bcec6 in MakeItSo<void (blink::MediaMultiChannelResampler::*const &)(int, media::AudioBus *), const std::__Cr::tuple<base::internal::UnretainedWrapper<blink::MediaMultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, int, media::AudioBus *> ./../../base/functional/bind_internal.h:930:12
    #18 0x5583e21bcec6 in RunImpl<void (blink::MediaMultiChannelResampler::*const &)(int, media::AudioBus *), const std::__Cr::tuple<base::internal::UnretainedWrapper<blink::MediaMultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, 0UL> ./../../base/functional/bind_internal.h:1067:14
    #19 0x5583e21bcec6 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::MediaMultiChannelResampler::* const&)(int, media::AudioBus*), blink::MediaMultiChannelResampler*>, base::internal::BindState<true, true, false, void (blink::MediaMultiChannelResampler::*)(int, media::AudioBus*), base::internal::UnretainedWrapper<blink::MediaMultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (int, media::AudioBus*)>::Run(base::internal::BindStateBase*, int, media::AudioBus*) ./../../base/functional/bind_internal.h:987:12
    #20 0x5583bedcb58b in base::RepeatingCallback<void (int, media::AudioBus*)>::Run(int, media::AudioBus*) const & ./../../base/functional/callback.h:344:12
    #21 0x5583bee4212d in Invoke<void (media::MultiChannelResampler::*)(int, int, float *), media::MultiChannelResampler *, const int &, int, float *> ./../../base/functional/bind_internal.h:738:12
    #22 0x5583bee4212d in MakeItSo<void (media::MultiChannelResampler::*const &)(int, int, float *), const std::__Cr::tuple<base::internal::UnretainedWrapper<media::MultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, int> &, int, float *> ./../../base/functional/bind_internal.h:930:12
    #23 0x5583bee4212d in RunImpl<void (media::MultiChannelResampler::*const &)(int, int, float *), const std::__Cr::tuple<base::internal::UnretainedWrapper<media::MultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, int> &, 0UL, 1UL> ./../../base/functional/bind_internal.h:1067:14
    #24 0x5583bee4212d in base::internal::Invoker<base::internal::FunctorTraits<void (media::MultiChannelResampler::* const&)(int, int, float*), media::MultiChannelResampler*, int const&>, base::internal::BindState<true, true, false, void (media::MultiChannelResampler::*)(int, int, float*), base::internal::UnretainedWrapper<media::MultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, int>, void (int, float*)>::Run(base::internal::BindStateBase*, int, float*) ./../../base/functional/bind_internal.h:987:12
    #25 0x5583bee87dfb in base::RepeatingCallback<void (int, float*)>::Run(int, float*) const & ./../../base/functional/callback.h:344:12
    #26 0x5583bee872f9 in media::SincResampler::Resample(int, float*) ./../../media/base/sinc_resampler.cc:283:14
    #27 0x5583e220cbfa in blink::AudioDestination::RequestRender(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:556:19
    #28 0x5583e22138fa in Invoke<void (blink::AudioDestination::*)(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, const media::AudioGlitchInfo &), scoped_refptr<blink::AudioDestination>, unsigned int, unsigned long, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo> ./../../base/functional/bind_internal.h:738:12
    #29 0x5583e22138fa in MakeItSo<void (blink::AudioDestination::*)(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, const media::AudioGlitchInfo &), std::__Cr::tuple<scoped_refptr<blink::AudioDestination>, unsigned int, unsigned long, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo> > ./../../base/functional/bind_internal.h:930:12
    #30 0x5583e22138fa in RunImpl<void (blink::AudioDestination::*)(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, const media::AudioGlitchInfo &), std::__Cr::tuple<scoped_refptr<blink::AudioDestination>, unsigned int, unsigned long, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo>, 0UL, 1UL, 2UL, 3UL, 4UL, 5UL> ./../../base/functional/bind_internal.h:1067:14
    #31 0x5583e22138fa in base::internal::Invoker<base::internal::FunctorTraits<void (blink::AudioDestination::*&&)(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&), scoped_refptr<blink::AudioDestination>&&, unsigned int&&, unsigned long&&, base::TimeDelta&&, base::TimeTicks&&, media::AudioGlitchInfo&&>, base::internal::BindState<true, true, false, void (blink::AudioDestination::*)(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&), scoped_refptr<blink::AudioDestination>, unsigned int, unsigned long, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:980:12
    #32 0x5583cf1a6fd4 in Run ./../../base/functional/callback.h:156:12
    #33 0x5583cf1a6fd4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:203:34
    #34 0x5583cf20e236 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:486:11)> ./../../base/task/common/task_annotator.h:90:5
    #35 0x5583cf20e236 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:484:23
    #36 0x5583cf20d150 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #37 0x5583cf20ef7a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #38 0x5583cf096b2d in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #39 0x5583cf20fbe6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:654:12
    #40 0x5583cf1370af in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #41 0x5583cba8de86 in blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run() ./../../third_party/blink/renderer/platform/scheduler/worker/non_main_thread_impl.cc:188:14
    #42 0x5583cf2dc667 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:101:13
    #43 0x5583bc134706 in asan_thread_start(void*) _asan_rtl_:28

0x518000055980 is located 256 bytes inside of 768-byte region [0x518000055880,0x518000055b80)
freed by thread T0 (chrome) here:
    #0 0x5583bc136a46 in __interceptor_free _asan_rtl_:3
    #1 0x5583bee85ffc in AlignedFree ./../../base/memory/aligned_memory.h:54:3
    #2 0x5583bee85ffc in operator() ./../../base/memory/aligned_memory.h:62:5
    #3 0x5583bee85ffc in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:468:7
    #4 0x5583bee85ffc in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:429:71
    #5 0x5583bee85ffc in media::SincResampler::~SincResampler() ./../../media/base/sinc_resampler.cc:194:31
    #6 0x5583bee42340 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:67:5
    #7 0x5583bee42340 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:278:7
    #8 0x5583bee42340 in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:248:71
    #9 0x5583bee42340 in __destroy_at<std::__Cr::unique_ptr<media::SincResampler, std::__Cr::default_delete<media::SincResampler> >, 0> ./../../third_party/libc++/src/include/__memory/construct_at.h:67:11
    #10 0x5583bee42340 in destroy<std::__Cr::unique_ptr<media::SincResampler, std::__Cr::default_delete<media::SincResampler> >, void, 0> ./../../third_party/libc++/src/include/__memory/allocator_traits.h:340:5
    #11 0x5583bee42340 in __base_destruct_at_end ./../../third_party/libc++/src/include/vector:950:7
    #12 0x5583bee42340 in __clear ./../../third_party/libc++/src/include/vector:944:5
    #13 0x5583bee42340 in std::__Cr::vector<std::__Cr::unique_ptr<media::SincResampler, std::__Cr::default_delete<media::SincResampler>>, std::__Cr::allocator<std::__Cr::unique_ptr<media::SincResampler, std::__Cr::default_delete<media::SincResampler>>>>::__destroy_vector::operator()() ./../../third_party/libc++/src/include/vector:522:16
    #14 0x5583bee411ad in ~vector ./../../third_party/libc++/src/include/vector:533:67
    #15 0x5583bee411ad in ~MultiChannelResampler ./../../media/base/multi_channel_resampler.cc:47:47
    #16 0x5583bee411ad in media::MultiChannelResampler::~MultiChannelResampler() ./../../media/base/multi_channel_resampler.cc:47:47
    #17 0x5583e22098b2 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:67:5
    #18 0x5583e22098b2 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:278:7
    #19 0x5583e22098b2 in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:248:71
    #20 0x5583e22098b2 in ~MediaMultiChannelResampler ./../../third_party/blink/renderer/platform/audio/media_multi_channel_resampler.h:25:23
    #21 0x5583e22098b2 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:67:5
    #22 0x5583e22098b2 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:278:7
    #23 0x5583e22098b2 in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:248:71
    #24 0x5583e22098b2 in blink::AudioDestination::~AudioDestination() ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:99:1
    #25 0x5583e2205745 in DeleteInternal<blink::AudioDestination> ./../../third_party/blink/renderer/platform/wtf/thread_safe_ref_counted.h:65:5
    #26 0x5583e2205745 in Destruct ./../../third_party/blink/renderer/platform/wtf/thread_safe_ref_counted.h:45:5
    #27 0x5583e2205745 in Release ./../../base/memory/ref_counted.h:416:7
    #28 0x5583e2205745 in Release ./../../base/memory/scoped_refptr.h:384:8
    #29 0x5583e2205745 in ~scoped_refptr ./../../base/memory/scoped_refptr.h:273:7
    #30 0x5583e2205745 in operator= ./../../base/memory/scoped_refptr.h:299:3
    #31 0x5583e2205745 in blink::RealtimeAudioDestinationHandler::CreatePlatformDestination() ./../../third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc:347:25
    #32 0x5583e2205e92 in blink::RealtimeAudioDestinationHandler::SetChannelCount(unsigned int, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc:137:3
    #33 0x5583e04ff634 in blink::(anonymous namespace)::v8_audio_node::ChannelCountAttributeSetCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_audio_node.cc:166:17
    #34 0x5583c1da0e08 in v8::internal::FunctionCallbackArguments::CallOrConstruct(v8::internal::Tagged<v8::internal::FunctionTemplateInfo>, bool) ./../../v8/src/api/api-arguments-inl.h:95:3
    #35 0x5583c1d9e060 in HandleApiCallHelper<false> ./../../v8/src/builtins/builtins-api.cc:108:36
    #36 0x5583c1d9e060 in v8::internal::Builtins::InvokeApiFunction(v8::internal::Isolate*, bool, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, v8::internal::Handle<v8::internal::HeapObject>) ./../../v8/src/builtins/builtins-api.cc:196:10
    #37 0x5583c2df4356 in v8::internal::Object::SetPropertyWithAccessor(v8::internal::LookupIterator*, v8::internal::Handle<v8::internal::Object>, v8::Maybe<v8::internal::ShouldThrow>) ./../../v8/src/objects/objects.cc:1549:5
    #38 0x5583c2dfa760 in v8::internal::Object::SetPropertyInternal(v8::internal::LookupIterator*, v8::internal::Handle<v8::internal::Object>, v8::Maybe<v8::internal::ShouldThrow>, v8::internal::StoreOrigin, bool*) ./../../v8/src/objects/objects.cc:2288:16
    #39 0x5583c2df9db6 in v8::internal::Object::SetProperty(v8::internal::LookupIterator*, v8::internal::Handle<v8::internal::Object>, v8::internal::StoreOrigin, v8::Maybe<v8::internal::ShouldThrow>) ./../../v8/src/objects/objects.cc:2361:9
    #40 0x5583c2615691 in v8::internal::StoreIC::Store(v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Name>, v8::internal::Handle<v8::internal::Object>, v8::internal::StoreOrigin) ./../../v8/src/ic/ic.cc:1948:5
    #41 0x5583c26292fd in __RT_impl_Runtime_StoreIC_Miss ./../../v8/src/ic/ic.cc:2929:3
    #42 0x5583c26292fd in v8::internal::Runtime_StoreIC_Miss(int, unsigned long*, v8::internal::Isolate*) ./../../v8/src/ic/ic.cc:2901:1
    #43 0x5583c5d2aef5 in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit setup-isolate-deserialize.cc:0:0
    #44 0x5583c5e15e26 in Builtins_SetNamedPropertyHandler setup-isolate-deserialize.cc:0:0
    #45 0x5583c5c8b8a6 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc:0:0
    #46 0x5583c5c8931b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc:0:0
    #47 0x5583c5c8905e in Builtins_JSEntry setup-isolate-deserialize.cc:0:0
    #48 0x5583c215316c in Call ./../../v8/src/execution/simulator.h:187:12
    #49 0x5583c215316c in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:420:22
    #50 0x5583c2151a9a in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) ./../../v8/src/execution/execution.cc:506:10
    #51 0x5583c1caf483 in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) ./../../v8/src/api/api.cc:5572:7
    #52 0x5583dae3699f in blink::V8ScriptRunner::CallFunction(v8::Local<v8::Function>, blink::ExecutionContext*, v8::Local<v8::Value>, int, v8::Local<v8::Value>*, v8::Isolate*) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:870:17
    #53 0x5583df92e7fe in CallInternal ./../../third_party/blink/renderer/bindings/core/v8/callback_invoke_helper.cc:142:12
    #54 0x5583df92e7fe in blink::bindings::CallbackInvokeHelper<blink::CallbackFunctionBase, (blink::bindings::CallbackInvokeHelperMode)2, (blink::bindings::CallbackReturnTypeIsPromise)0>::Call(int, v8::Local<v8::Value>*) ./../../third_party/blink/renderer/bindings/core/v8/callback_invoke_helper.cc:163:10
    #55 0x5583df93f4e2 in blink::V8EventHandlerNonNull::InvokeWithoutRunnabilityCheck(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::HeapVector<blink::ScriptValue, 0u> const&) ./gen/third_party/blink/renderer/bindings/core/v8/v8_event_handler_non_null.cc:189:13
    #56 0x5583db98a81a in blink::JSEventHandler::InvokeInternal(blink::EventTarget&, blink::Event&, v8::Local<v8::Value>) ./../../third_party/blink/renderer/bindings/core/v8/js_event_handler.cc:134:14
    #57 0x5583db861aaa in blink::JSBasedEventListener::Invoke(blink::ExecutionContext*, blink::Event*) ./../../third_party/blink/renderer/bindings/core/v8/js_based_event_listener.cc:158:5
    #58 0x5583db851d76 in blink::EventTarget::FireEventListeners(blink::Event&, blink::EventTargetData*, blink::HeapVector<cppgc::internal::BasicMember<blink::RegisteredEventListener, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 1u>) ./../../third_party/blink/renderer/core/dom/events/event_target.cc:1112:15
    #59 0x5583db84fd74 in blink::EventTarget::FireEventListeners(blink::Event&) ./../../third_party/blink/renderer/core/dom/events/event_target.cc:1031:29

previously allocated by thread T0 (chrome) here:
    #0 0x5583bc1377a7 in ___interceptor_posix_memalign _asan_rtl_:3
    #1 0x5583cf07fbc8 in base::AlignedAlloc(unsigned long, unsigned long) ./../../base/memory/aligned_memory.cc:34:13
    #2 0x5583bee851c5 in media::SincResampler::SincResampler(double, int, base::RepeatingCallback<void (int, float*)>) ./../../media/base/sinc_resampler.cc:170:11
    #3 0x5583bee405fe in make_unique<media::SincResampler, double &, unsigned long &, base::RepeatingCallback<void (int, float *)> > ./../../third_party/libc++/src/include/__memory/unique_ptr.h:620:30
    #4 0x5583bee405fe in media::MultiChannelResampler::MultiChannelResampler(int, double, unsigned long, base::RepeatingCallback<void (int, media::AudioBus*)>) ./../../media/base/multi_channel_resampler.cc:27:27
    #5 0x5583e21bc16a in make_unique<media::MultiChannelResampler, int &, double &, unsigned int &, base::RepeatingCallback<void (int, media::AudioBus *)> > ./../../third_party/libc++/src/include/__memory/unique_ptr.h:620:30
    #6 0x5583e21bc16a in blink::MediaMultiChannelResampler::MediaMultiChannelResampler(int, double, unsigned int, WTF::CrossThreadFunction<void (int, blink::AudioBus*)>) ./../../third_party/blink/renderer/platform/audio/media_multi_channel_resampler.cc:23:16
    #7 0x5583e22117eb in make_unique<blink::MediaMultiChannelResampler, unsigned int &, double &, unsigned int &, WTF::CrossThreadFunction<void (int, blink::AudioBus *)> > ./../../third_party/libc++/src/include/__memory/unique_ptr.h:620:30
    #8 0x5583e22117eb in blink::AudioDestination::AudioDestination(blink::AudioIOCallback&, blink::WebAudioSinkDescriptor const&, unsigned int, blink::WebAudioLatencyHint const&, std::__Cr::optional<float>, unsigned int) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:427:18
    #9 0x5583e22094a6 in blink::AudioDestination::Create(blink::AudioIOCallback&, blink::WebAudioSinkDescriptor const&, unsigned int, blink::WebAudioLatencyHint const&, std::__Cr::optional<float>, unsigned int) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:92:11
    #10 0x5583e2205683 in blink::RealtimeAudioDestinationHandler::CreatePlatformDestination() ./../../third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc:347:27
    #11 0x5583e2205503 in blink::RealtimeAudioDestinationHandler::Initialize() ./../../third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc:78:3
    #12 0x5583e2155396 in blink::BaseAudioContext::Initialize() ./../../third_party/blink/renderer/modules/webaudio/base_audio_context.cc:122:34
    #13 0x5583e2090de9 in blink::AudioContext::AudioContext(blink::LocalDOMWindow&, blink::WebAudioLatencyHint const&, std::__Cr::optional<float>, blink::WebAudioSinkDescriptor) ./../../third_party/blink/renderer/modules/webaudio/audio_context.cc:295:3
    #14 0x5583e208e9de in Call<blink::LocalDOMWindow &, blink::WebAudioLatencyHint &, std::__Cr::optional<float> &, blink::WebAudioSinkDescriptor &> ./../../v8/include/cppgc/allocation.h:241:32
    #15 0x5583e208e9de in MakeGarbageCollected<blink::AudioContext, blink::LocalDOMWindow &, blink::WebAudioLatencyHint &, std::__Cr::optional<float> &, blink::WebAudioSinkDescriptor &> ./../../v8/include/cppgc/allocation.h:279:7
    #16 0x5583e208e9de in MakeGarbageCollected<blink::AudioContext, blink::LocalDOMWindow &, blink::WebAudioLatencyHint &, std::__Cr::optional<float> &, blink::WebAudioSinkDescriptor &> ./../../third_party/blink/renderer/platform/heap/garbage_collected.h:37:10
    #17 0x5583e208e9de in blink::AudioContext::Create(blink::ExecutionContext*, blink::AudioContextOptions const*, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/webaudio/audio_context.cc:211:33
    #18 0x5583e051c32b in blink::(anonymous namespace)::v8_audio_context::ConstructorCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_audio_context.cc:293:23
    #19 0x5583c1da0e08 in v8::internal::FunctionCallbackArguments::CallOrConstruct(v8::internal::Tagged<v8::internal::FunctionTemplateInfo>, bool) ./../../v8/src/api/api-arguments-inl.h:95:3
    #20 0x5583c1d9edf5 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, unsigned long*, int) ./../../v8/src/builtins/builtins-api.cc:108:36
    #21 0x5583c1d9cdef in v8::internal::Builtin_Impl_HandleApiConstruct(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:139:3
    #22 0x5583c5d2ae35 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc:0:0
    #23 0x5583c5c8c4ce in construct_stub_invoke_deopt_addr setup-isolate-deserialize.cc:0:0
    #24 0x5583c5e21113 in Builtins_ConstructHandler setup-isolate-deserialize.cc:0:0
    #25 0x5583c5c8b8a6 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc:0:0
    #26 0x5583c5c8931b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc:0:0
    #27 0x5583c5c8905e in Builtins_JSEntry setup-isolate-deserialize.cc:0:0
    #28 0x5583c215316c in Call ./../../v8/src/execution/simulator.h:187:12
    #29 0x5583c215316c in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:420:22
    #30 0x5583c2155a41 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>) ./../../v8/src/execution/execution.cc:517:10
    #31 0x5583c1c6ee1e in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) ./../../v8/src/api/api.cc:2128:7
    #32 0x5583dae323f3 in blink::V8ScriptRunner::RunCompiledScript(v8::Isolate*, v8::Local<v8::Script>, v8::Local<v8::Data>, blink::ExecutionContext*) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:511:22
    #33 0x5583dae33ab4 in blink::V8ScriptRunner::CompileAndRunScript(blink::ScriptState*, blink::ClassicScript*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:634:22
    #34 0x5583ddd0d213 in blink::ClassicScript::RunScriptOnScriptStateAndReturnValue(blink::ScriptState*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption) ./../../third_party/blink/renderer/core/script/classic_script.cc:222:10
    #35 0x5583ddd62954 in blink::Script::RunScriptOnScriptState(blink::ScriptState*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption) ./../../third_party/blink/renderer/core/script/script.cc:33:17
    #36 0x5583ddd62c9b in blink::Script::RunScript(blink::LocalDOMWindow*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption) ./../../third_party/blink/renderer/core/script/script.cc:40:3

Thread T18 (Realtime AudioW) created by T0 (chrome) here:
    #0 0x5583bc11c511 in ___interceptor_pthread_create _asan_rtl_:3
    #1 0x5583cf2dbbb8 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) ./../../base/threading/platform_thread_posix.cc:146:13
    #2 0x5583cf28c8f8 in base::SimpleThread::StartAsync() ./../../base/threading/simple_thread.cc:55:13
    #3 0x5583cba8bb1a in blink::NonMainThread::CreateThread(blink::ThreadCreationParams const&) ./../../third_party/blink/renderer/platform/scheduler/worker/non_main_thread_impl.cc:41:11
    #4 0x5583de2727ca in blink::WorkerBackingThread::WorkerBackingThread(blink::ThreadCreationParams const&) ./../../third_party/blink/renderer/core/workers/worker_backing_thread.cc:114:23
    #5 0x5583e221f2a1 in make_unique<blink::WorkerBackingThread, blink::ThreadCreationParams &> ./../../third_party/libc++/src/include/__memory/unique_ptr.h:620:30
    #6 0x5583e221f2a1 in blink::RealtimeAudioWorkletThread::RealtimeAudioWorkletThread(blink::WorkerReportingProxy&, base::TimeDelta) ./../../third_party/blink/renderer/modules/webaudio/realtime_audio_worklet_thread.cc:87:30
    #7 0x5583e21293b8 in make_unique<blink::RealtimeAudioWorkletThread, blink::WorkerReportingProxy &, base::TimeDelta &> ./../../third_party/libc++/src/include/__memory/unique_ptr.h:620:30
    #8 0x5583e21293b8 in CreateWorkletThreadWithConstraints ./../../third_party/blink/renderer/modules/webaudio/audio_worklet_messaging_proxy.cc:131:12
    #9 0x5583e21293b8 in blink::AudioWorkletMessagingProxy::CreateWorkerThread() ./../../third_party/blink/renderer/modules/webaudio/audio_worklet_messaging_proxy.cc:116:10
    #10 0x5583de269b95 in blink::ThreadedMessagingProxyBase::InitializeWorkerThread(std::__Cr::unique_ptr<blink::GlobalScopeCreationParams, std::__Cr::default_delete<blink::GlobalScopeCreationParams>>, std::__Cr::optional<blink::WorkerBackingThreadStartupData> const&, std::__Cr::optional<base::TokenType<blink::DedicatedWorkerTokenTypeMarker> const> const&, std::__Cr::unique_ptr<blink::WorkerDevToolsParams, std::__Cr::default_delete<blink::WorkerDevToolsParams>>) ./../../third_party/blink/renderer/core/workers/threaded_messaging_proxy_base.cc:77:20
    #11 0x5583e18031f9 in blink::ThreadedWorkletMessagingProxy::Initialize(blink::WorkerClients*, blink::WorkletModuleResponsesMap*, std::__Cr::optional<blink::WorkerBackingThreadStartupData> const&, mojo::StructPtr<blink::mojom::blink::WorkletGlobalScopeCreationParams>) ./../../third_party/blink/renderer/core/workers/threaded_worklet_messaging_proxy.cc:160:3
    #12 0x5583e21261cd in blink::AudioWorklet::CreateGlobalScope() ./../../third_party/blink/renderer/modules/webaudio/audio_worklet.cc:82:10
    #13 0x5583de2b270f in blink::Worklet::FetchAndInvokeScript(blink::KURL const&, WTF::String const&, blink::WorkletPendingTasks*) ./../../third_party/blink/renderer/core/workers/worklet.cc:171:24
    #14 0x5583de2b36a4 in Invoke<void (blink::Worklet::*)(const blink::KURL &, const WTF::String &, blink::WorkletPendingTasks *), cppgc::internal::BasicPersistent<blink::Worklet, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, blink::KURL, blink::V8RequestCredentials, cppgc::internal::BasicPersistent<blink::WorkletPendingTasks, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy> > ./../../base/functional/bind_internal.h:738:12
    #15 0x5583de2b36a4 in MakeItSo<void (blink::Worklet::*)(const blink::KURL &, const WTF::String &, blink::WorkletPendingTasks *), std::__Cr::tuple<cppgc::internal::BasicPersistent<blink::Worklet, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, blink::KURL, blink::V8RequestCredentials, cppgc::internal::BasicPersistent<blink::WorkletPendingTasks, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy> > > ./../../base/functional/bind_internal.h:930:12
    #16 0x5583de2b36a4 in RunImpl<void (blink::Worklet::*)(const blink::KURL &, const WTF::String &, blink::WorkletPendingTasks *), std::__Cr::tuple<cppgc::internal::BasicPersistent<blink::Worklet, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, blink::KURL, blink::V8RequestCredentials, cppgc::internal::BasicPersistent<blink::WorkletPendingTasks, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy> >, 0UL, 1UL, 2UL, 3UL> ./../../base/functional/bind_internal.h:1067:14
    #17 0x5583de2b36a4 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::Worklet::*&&)(blink::KURL const&, WTF::String const&, blink::WorkletPendingTasks*), cppgc::internal::BasicPersistent<blink::Worklet, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>&&, blink::KURL&&, blink::V8RequestCredentials&&, cppgc::internal::BasicPersistent<blink::WorkletPendingTasks, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>&&>, base::internal::BindState<true, true, false, void (blink::Worklet::*)(blink::KURL const&, WTF::String const&, blink::WorkletPendingTasks*), cppgc::internal::BasicPersistent<blink::Worklet, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, blink::KURL, blink::V8RequestCredentials, cppgc::internal::BasicPersistent<blink::WorkletPendingTasks, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:980:12
    #18 0x5583cf1a6fd4 in Run ./../../base/functional/callback.h:156:12
    #19 0x5583cf1a6fd4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:203:34
    #20 0x5583cf20e236 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:486:11)> ./../../base/task/common/task_annotator.h:90:5
    #21 0x5583cf20e236 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:484:23
    #22 0x5583cf20d150 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #23 0x5583cf20ef7a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #24 0x5583cf096b2d in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #25 0x5583cf20fbe6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:654:12
    #26 0x5583cf1370af in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #27 0x5583e647c02c in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:359:16
    #28 0x5583cc7e4368 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:703:14
    #29 0x5583cc7e5469 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:807:12
    #30 0x5583cc7e7d4f in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1175:10
    #31 0x5583cc7e2645 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:333:36
    #32 0x5583cc7e2c3b in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:346:10
    #33 0x5583bc16f9b3 in ChromeMain ./../../chrome/app/chrome_main.cc:230:12
    #34 0x78aaac229d8f in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16

SUMMARY: AddressSanitizer: heap-use-after-free (/home/pwn11/asan-linux-release/chrome+0xf2e7d64) (BuildId: ae1cf88400c90eab)
Shadow bytes around the buggy address:
  0x518000055700: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x518000055780: 00 00 00 00 00 00 00 00 00 00 00 01 fa fa fa fa
  0x518000055800: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x518000055880: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x518000055900: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x518000055980:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x518000055a00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x518000055a80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x518000055b00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x518000055b80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x518000055c00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
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
    #0 0x5583e220ad46 in blink::AudioDestination::Render(base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, media::AudioBus*) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:204:34


Command line: `/proc/self/exe --type=renderer --crashpad-handler-pid=1079542 --enable-crash-reporter=, --user-data-dir=/tmp/xx2 --no-subproc-heap-profiling --change-stack-guard-on-fork=enable --file-url-path-alias=/gen=/home/pwn11/asan-linux-release/gen --disable-databases --disable-gpu-compositing --lang=en-US --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1721620696610055 --launch-time-ticks=130784094492 --shared-files=v8_context_snapshot_data:100 --metrics-shmem-handle=4,i,472013991247985170,11568835115277167954,2097152 --field-trial-handle=3,i,6690326979181892439,8267522154067825575,262144 --variations-seed-version`


MiraclePtr Status: MANUAL ANALYSIS REQUIRED
A pointer to the same region was extracted from a raw_ptr<T> object prior to this crash.
The "use" and "free" threads don't match. This crash is likely to have been caused by a race condition that is mislabeled as a use-after-free. Make sure that the "free" is sequenced after the "use" (e.g. both are on the same sequence, or the "free" is in a task posted after the "use"). Otherwise, the crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==1==END OF ADDITIONAL INFO
==1==ABORTING

## Attachments

- [crash.html](attachments/crash.html) (text/html, 977 B)
- [asan.log](attachments/asan.log) (text/plain, 37.6 KB)
- [2024-07-25_web_audio_bench_clean.txt](attachments/2024-07-25_web_audio_bench_clean.txt) (text/plain, 3.2 KB)
- [2024-07-25_web_audio_bench_with_patch.txt](attachments/2024-07-25_web_audio_bench_with_patch.txt) (text/plain, 3.2 KB)
- [asan2.log](attachments/asan2.log) (text/plain, 37.6 KB)

## Timeline

### em...@gmail.com (2024-07-23)

This issue is similar to https://issues.chromium.org/issues/40945671.

### cl...@appspot.gserviceaccount.com (2024-07-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5991663128215552.

### ma...@chromium.org (2024-07-23)

[security shepherd]
I was unable to reproduce with chromium-1331767-linux-asan or chromium-1331766-mac-asan. ClusterFuzz also failed to reproduce.

Do you have any recommendations on how to reliably reproduce this? Do you expect the test case crash immediately, or does it require waiting for some length of time before the crash?

### em...@gmail.com (2024-07-23)

I just noticed that on my setup, manually clicking on crash.html in the browser's list immediately reproduces the issue. However, directly passing crash.html as a command line argument in the terminal does not reproduce the issue as consistently.

Another stable way to reproduce the issue is to start the browser with the path to crash.html in the parameters (chrome --user-data-dir=/tmp/xx http://localhost:8880/crash.html), and then pressing ctrl+shift+i to open the developer tools will immediately reproduce the issue (although the bug itself is not related to the developer tools, it just affects the reproduction).

### pe...@google.com (2024-07-23)

Thank you for providing more feedback. Adding the requester to the CC list.

### ma...@chromium.org (2024-07-23)

[security shepherd]
Thanks so much for the quick response. Loading the POC, right-clicking, and selecting Inspect is sufficient to reliably trigger the ASan use-after-free detection on both macOS and Linux. I did also manage to reproduce it on Linux by selecting the URL from within Chrome's history or from the omnibox.

### ma...@chromium.org (2024-07-23)

[security shepherd]

I'm also able to reproduce with chromium-1300313-linux-asan, which is from shortly before the M126 branch point.

MiraclePtr's automatic analysis was unable to determine whether it would protect against this specific issue. I'm also not clear if it would based on looking at the relevant code, so for now I'll assume it does not and set the severity accordingly.

Marking as S1 as this is a use-after-free in the renderer. Assigning to hongchan@ based on third\_party/blink/renderer/modules/webaudio/OWNERS. Please reassign if someone else is better suited.

### ho...@chromium.org (2024-07-23)

markrowe@

The issue is still P4/S4. Can you confirm?

### ma...@chromium.org (2024-07-23)

I had intended to set it to S1 as per my comment. Fixed.

### pe...@google.com (2024-07-24)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-07-24)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### mj...@chromium.org (2024-07-24)

Reproduction case (crash.html) seems to be almost exactly the same as uaf_write.html from https://issues.chromium.org/issues/40945671 with the addition of a timeout that reloads the page after five seconds.

### mj...@chromium.org (2024-07-24)

I was able to reproduce the crash on a Linux ASAN build from tip of tree, although it is also not consistent for me.

### mj...@chromium.org (2024-07-24)

I can now reliably reproduce the crash on a ToT ASAN build by doing the following:
- Serve crash.html with "python -m http.server"
- Open chrome, load the page
- Open devtools with F12
- Repeatedly click on the empty webpage for 5 seconds until the page reloads
Then I get a sadtab with ASAN report.

The problem appears to be a stale pointer for the in-place processing buffer.  An aggressive solution is to remove in-place processing completely.  This will eliminate this entire category of bugs, but has the potential to worsen performance for all WebAudio users.

I wrote a CL to test this, and can't reproduce the crash after applying this change:
https://chromium-review.googlesource.com/c/chromium/src/+/5739335

Submitter / markrowe@, are you able to build with the changes from the above CL to verify?

### em...@gmail.com (2024-07-25)

I have just applied the patch and tested it many times. The issue did not repro.

Test version:
Chromium 128.0.6601.2(with CL:5739335)

### ho...@chromium.org (2024-07-25)

mjwilson@

Great! Could you run <https://spotify.github.io/web-audio-bench/> on both ToT and the patch to catch any performance regression?

### pe...@google.com (2024-07-25)

The NextAction date has arrived: 2024-07-25
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### mj...@chromium.org (2024-07-25)

Submitter, thank you for testing!

hongchan@, I am running the benchmarks and will report here when they finish.  They may not be completely representative, but will give us an idea of the difference.

I will also try a less aggressive solution that keeps in-place processing but doesn't store the pointer.

### mj...@chromium.org (2024-07-25)

Benchmark results were mixed, from a 13 us improvement with the patch to a -72 us worsening with the patch.  Most of the tests were within 10 us of each other.  These were run on official build, unbranded, with PGO turned off.  See attached.

This isn't a large absolute difference, but it does impact some nodes more than others.  Especially analyser (~38% regression), delay (~15%), waveshaper (~8%), and biquad (~5%), which is expected given that they are directly affected.  IIR should also be affected but doesn't seem to be in the benchmark suite.  It is also only one machine datapoint, so results could be different on different platforms.

The less aggressive solution is not as straightforward because we need to consider every usage of AudioOutput::Bus() since the semantics of that function will have to change.  I'm not sure yet if it will be a feasible solution.

Right now my feeling is that we should take the performance hit, disable in-place processing, and try to optimize the impacted nodes in other ways.  Some considerations:
- The original bug was recently made public and the PoC for this bug is almost identical, so there may be active exploits coming out soon.  It's not clear to me how exploitable this is, but it's a reason to try to push the working solution as soon as possible.
- AnalyserNode is used often, although usually there are only one or two in a graph.  a 38% performance hit will probably be noticeable but also probably won't make applications completely unusable.
- Biquad is probably used in greater numbers, but seems to be affected less.
- Panner actually seemed to improve, perhaps some compiler cache optimization with the smaller code size?  Or it could just be noise.

I'll keep trying to make the less aggressive approach work today, and hongchan@ and I will try to make a final decision on the fix tomorrow or Monday.

### pe...@google.com (2024-07-26)

The issue's primary component must be in the Component Tags, so re-adding it. To change the primary component, use the edit button at the top of the issue, just above the title.

### mj...@chromium.org (2024-07-26)

After discussion with hongchan@, here is our plan:
- We will keep https://crrev.com/c/5739335 in reserve since it can have significant performance implications, especially for deep graphs with chains of nodes that have the same channel layout.
- We would like to take one more week to look for alternative solutions.
- If we can't find anything in another week, or if we have to make an emergency rollout to fix an active exploit in the wild, we will land https://crrev.com/c/5739335.
- Hongchan will take over on Monday to look at things from a different angle (so assigning to hongchan@ now).
- I will prepare https://crrev.com/c/5739335 with an enabled-by-default flag guard in the meantime so it will be ready to land anytime.

I gave up on my less aggressive approach because the Bus() API is used in so many places.  It was turning into redesigning the entire in-place processing approach, which we may want to do in the future but probably isn't feasible to land as a security fix.

Thank you to the submitter for catching this!

### ho...@chromium.org (2024-07-29)

emilykim8708@

I am also working on <https://crrev.com/c/5744142>, and so far it has been successful (local repro, CI tests). Could you test this CL on your end too? Thanks so much for working with us on this!

### em...@gmail.com (2024-07-29)

It is still reproducible. The use of the stack is somewhat different from before. Now it accesses invalid memory again through [0]SilenceOutputs().

### ho...@chromium.org (2024-07-29)

```
==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x51800000e980 at pc 0x6119467a5d65 bp 0x791c8beddca0 sp 0x791c8bedd470
WRITE of size 512 at 0x51800000e980 thread T11 (Realtime AudioW)
    #0 0x6119467a5d64 in __asan_memset _asan_rtl_:3
    #1 0x611966657287 in Zero ./../../third_party/blink/renderer/platform/audio/audio_channel.h:0:0
    #2 0x611966657287 in blink::AudioBus::Zero() ./../../third_party/blink/renderer/platform/audio/audio_bus.cc:108:13
    #3 0x611969d106eb in SilenceOutputs ./../../third_party/blink/renderer/modules/webaudio/audio_handler.cc:401:20
    #4 0x611969d106eb in blink::AudioHandler::ProcessIfNecessary(unsigned int) ./../../third_party/blink/renderer/modules/webaudio/audio_handler.cc:336:7
    #5 0x611969ddef34 in blink::DeferredTaskHandler::ProcessAutomaticPullNodes(unsigned int) ./../../third_party/blink/renderer/modules/webaudio/deferred_task_handler.cc:198:41
    #6 0x611969e4f871 in blink::RealtimeAudioDestinationHandler::Render(blink::AudioBus*, unsigned int, blink::AudioIOPosition const&, blink::AudioCallbackMetric const&, base::TimeDelta, media::AudioGlitchInfo const&) ./../../third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc:247:37

```

Thanks. The problem is that I can't reproduce the crash with this stack trace. My guess is that this happens before AudioWorkletHandler::Process() function. We can extend the same fix to the AudioHandler::SilenceOutputs(). I will give it a try.

### ho...@chromium.org (2024-07-29)

emilykim8708@

I still can't reproduce the ASAN crash on any of my machines after several hours of running it.

That said, I updated <https://crrev.com/c/5744142> for you again and thanks for putting effort into verification.

### em...@gmail.com (2024-07-30)

I have tested it multiple times on Linux and Mac, and confirmed that the issue did not reproduce again.

### ho...@chromium.org (2024-07-30)

Thank you so much for verification!

We'll reevaluate our plan to land the fix and update this issue soon.

### ap...@google.com (2024-07-30)

Project: chromium/src
Branch: main

commit 52cfa2026953e072539248c4083848740f074afd
Author: Hongchan Choi <hongchan@chromium.org>
Date:   Tue Jul 30 16:32:05 2024

    Avoid accessing unconnected outputs in AudioWorkletHandler, AudioHandler
    
    This CL fixes the logic to zero out output buses regardless of the
    outgoing connection status. If an output bus is not connected (or
    disconnected), we should assume that the outgoing connection might
    be stale.
    
    This fix is verified locally by both the author and the reporter.
    
    Bug: 354847246
    Change-Id: If10c7bb816e50f7b88252aa9a981b53704724da0
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5744142
    Commit-Queue: Hongchan Choi <hongchan@chromium.org>
    Reviewed-by: Michael Wilson <mjwilson@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1334898}

M       third_party/blink/renderer/modules/webaudio/audio_handler.cc
M       third_party/blink/renderer/modules/webaudio/audio_worklet_handler.cc

https://chromium-review.googlesource.com/5744142


### ho...@chromium.org (2024-07-31)

The patch is in the latest Canary (129.0.6628.0):
<https://chromiumdash.appspot.com/commit/52cfa2026953e072539248c4083848740f074afd>

Once again - thanks for working closely with us, emilykim8708@!

### pe...@google.com (2024-08-01)

Requesting merge to extended stable (M126) because latest trunk commit (1334898) appears to be after extended stable branch point (1300313).
Requesting merge to stable (M127) because latest trunk commit (1334898) appears to be after stable branch point (1313161).
Requesting merge to beta (M128) because latest trunk commit (1334898) appears to be after beta branch point (1331488).
Merge review required: M126 is already shipping to stable.

Merge review required: M127 is already shipping to stable.

Merge review required: M128 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [126, 127, 128].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### ho...@chromium.org (2024-08-01)

1. <https://crrev.com/c/5744142>
2. Yes
3. No
4. No
5. No, but it would be helpful if the team team is able to reproduce the second problem ([#comment24](https://issues.chromium.org/issues/354847246#comment24)) and verify the fix manually. The original problem ([#comment1](https://issues.chromium.org/issues/354847246#comment1)) was reproduced, fixed, and verified, but I was not able to reproduce the second problem ([#comment24](https://issues.chromium.org/issues/354847246#comment24)) on my machine.

### am...@chromium.org (2024-08-02)

<https://crrev.com/5744142> approved for merges
please merge this fix to Beta M128 / branch 6613, Stable M127 / branch 6533, and Extended Stable / branch 6478 at soonest so this fix can be shipped in the next respective updates -- thank you

### ho...@chromium.org (2024-08-05)

6478 - <https://crrev.com/c/5762922> (thanks! srinivassista@)  

6533 - <https://crrev.com/c/5757952> (in flight)  

6613 - <https://crrev.com/c/5763055> (in flight)

### ap...@google.com (2024-08-05)

Project: chromium/src
Branch: refs/branch-heads/6613

commit ec37691819f653b42c2b83ed069d805dc13c4a40
Author: Hongchan Choi <hongchan@chromium.org>
Date:   Mon Aug 05 19:25:11 2024

    Avoid accessing unconnected outputs in AudioWorkletHandler, AudioHandler
    
    This CL fixes the logic to zero out output buses regardless of the
    outgoing connection status. If an output bus is not connected (or
    disconnected), we should assume that the outgoing connection might
    be stale.
    
    This fix is verified locally by both the author and the reporter.
    
    (cherry picked from commit 52cfa2026953e072539248c4083848740f074afd)
    
    Bug: 354847246
    Change-Id: If10c7bb816e50f7b88252aa9a981b53704724da0
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5744142
    Commit-Queue: Hongchan Choi <hongchan@chromium.org>
    Reviewed-by: Michael Wilson <mjwilson@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1334898}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5763055
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Auto-Submit: Hongchan Choi <hongchan@chromium.org>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6613@{#616}
    Cr-Branched-From: 03c1799e6f9c7239802827eab5e935b9e14fceae-refs/heads/main@{#1331488}

M       third_party/blink/renderer/modules/webaudio/audio_handler.cc
M       third_party/blink/renderer/modules/webaudio/audio_worklet_handler.cc

https://chromium-review.googlesource.com/5763055


### pe...@google.com (2024-08-05)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ap...@google.com (2024-08-05)

Project: chromium/src
Branch: refs/branch-heads/6533

commit 24437bb18f2fddce90e6dc26a515b8fc007c797e
Author: Hongchan Choi <hongchan@chromium.org>
Date:   Mon Aug 05 19:29:05 2024

    Avoid accessing unconnected outputs in AudioWorkletHandler, AudioHandler
    
    This CL fixes the logic to zero out output buses regardless of the
    outgoing connection status. If an output bus is not connected (or
    disconnected), we should assume that the outgoing connection might
    be stale.
    
    This fix is verified locally by both the author and the reporter.
    
    (cherry picked from commit 52cfa2026953e072539248c4083848740f074afd)
    
    Bug: 354847246
    Change-Id: If10c7bb816e50f7b88252aa9a981b53704724da0
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5744142
    Commit-Queue: Hongchan Choi <hongchan@chromium.org>
    Reviewed-by: Michael Wilson <mjwilson@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1334898}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5757952
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
    Auto-Submit: Hongchan Choi <hongchan@chromium.org>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6533@{#1909}
    Cr-Branched-From: 7e0b87ec6b8cb5cb2969e1479fc25776e582721d-refs/heads/main@{#1313161}

M       third_party/blink/renderer/modules/webaudio/audio_handler.cc
M       third_party/blink/renderer/modules/webaudio/audio_worklet_handler.cc

https://chromium-review.googlesource.com/5757952


### ho...@chromium.org (2024-08-05)

Re [#comment36](https://issues.chromium.org/issues/354847246#comment36):

1. Not a regression, but a bug that has existed originally.
2. No.

### ap...@google.com (2024-08-05)

Project: chromium/src
Branch: refs/branch-heads/6478

commit 2a4c54370053284b59406e15f7c99162e6fb411c
Author: Hongchan Choi <hongchan@chromium.org>
Date:   Mon Aug 05 21:00:36 2024

    Avoid accessing unconnected outputs in AudioWorkletHandler, AudioHandler
    
    This CL fixes the logic to zero out output buses regardless of the
    outgoing connection status. If an output bus is not connected (or
    disconnected), we should assume that the outgoing connection might
    be stale.
    
    This fix is verified locally by both the author and the reporter.
    
    (cherry picked from commit 52cfa2026953e072539248c4083848740f074afd)
    
    Bug: 354847246
    Change-Id: If10c7bb816e50f7b88252aa9a981b53704724da0
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5744142
    Commit-Queue: Hongchan Choi <hongchan@chromium.org>
    Reviewed-by: Michael Wilson <mjwilson@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1334898}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5762922
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
    Owners-Override: Srinivas Sista <srinivassista@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6478@{#1900}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       third_party/blink/renderer/modules/webaudio/audio_handler.cc
M       third_party/blink/renderer/modules/webaudio/audio_worklet_handler.cc

https://chromium-review.googlesource.com/5762922


### ap...@google.com (2024-08-08)

Project: chromium/src
Branch: refs/branch-heads/6478_182

commit 5bf7858ceef7c1c4d6cac0443a2847bb8281e886
Author: Hongchan Choi <hongchan@chromium.org>
Date:   Thu Aug 08 04:07:18 2024

    [CfM-R126] Avoid accessing unconnected outputs in AudioWorkletHandler, AudioHandler
    
    This CL fixes the logic to zero out output buses regardless of the
    outgoing connection status. If an output bus is not connected (or
    disconnected), we should assume that the outgoing connection might
    be stale.
    
    This fix is verified locally by both the author and the reporter.
    
    (cherry picked from commit 52cfa2026953e072539248c4083848740f074afd)
    
    (cherry picked from commit 2a4c54370053284b59406e15f7c99162e6fb411c)
    
    Bug: 354847246
    Change-Id: If10c7bb816e50f7b88252aa9a981b53704724da0
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5744142
    Commit-Queue: Hongchan Choi <hongchan@chromium.org>
    Reviewed-by: Michael Wilson <mjwilson@chromium.org>
    Cr-Original-Original-Commit-Position: refs/heads/main@{#1334898}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5762922
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
    Owners-Override: Srinivas Sista <srinivassista@chromium.org>
    Cr-Original-Commit-Position: refs/branch-heads/6478@{#1900}
    Cr-Original-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5772114
    Owners-Override: Pablo Ceballos <pceballos@chromium.org>
    Commit-Queue: Pablo Ceballos <pceballos@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6478_182@{#55}
    Cr-Branched-From: 5b5d8292ddf182f8b2096fa665b473b6317906d5-refs/branch-heads/6478@{#1776}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       third_party/blink/renderer/modules/webaudio/audio_handler.cc
M       third_party/blink/renderer/modules/webaudio/audio_worklet_handler.cc

https://chromium-review.googlesource.com/5772114


### sp...@google.com (2024-08-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
report of mildly mitigated memory corruption in a sandboxed process / the renderer; mitigated by user gesture / non-reliably reproducible 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-16)

Congratulations Cassidy Kim! Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2024-09-12)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### ho...@chromium.org (2024-09-13)

1. <https://crrev.com/c/5744142>
2. Low - The fix is to add simple checks
3. Yes
4. Yes

### ap...@google.com (2024-09-18)

Project: chromium/src
Branch: refs/branch-heads/6099

commit 576808e9bbf22cc0d31ac74179ba75baf8896174
Author: Hongchan Choi <hongchan@chromium.org>
Date:   Wed Sep 18 15:55:30 2024

    [M120-LTS] Avoid accessing unconnected outputs in AudioWorkletHandler, AudioHandler
    
    This CL fixes the logic to zero out output buses regardless of the
    outgoing connection status. If an output bus is not connected (or
    disconnected), we should assume that the outgoing connection might
    be stale.
    
    This fix is verified locally by both the author and the reporter.
    
    (cherry picked from commit 52cfa2026953e072539248c4083848740f074afd)
    (cherry picked from commit 002c5ea3e682b9943fb8332fb1793c138da9803e)
    
    Bug: 354847246
    Change-Id: If10c7bb816e50f7b88252aa9a981b53704724da0
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5744142
    Commit-Queue: Hongchan Choi <hongchan@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1334898}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5783475
    Reviewed-by: Hongchan Choi <hongchan@chromium.org>
    Reviewed-by: Giovanni Pezzino <giovax@google.com>
    Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#2085}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

M       third_party/blink/renderer/modules/webaudio/audio_handler.cc
M       third_party/blink/renderer/modules/webaudio/audio_worklet_handler.cc

https://chromium-review.googlesource.com/5783475


### pe...@google.com (2024-11-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/354847246)*
