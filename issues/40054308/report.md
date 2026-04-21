# UAF in MediaStreamTrackProcessor

| Field | Value |
|-------|-------|
| **Issue ID** | [40054308](https://issues.chromium.org/issues/40054308) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>MediaStream |
| **Platforms** | Linux, Windows |
| **Reporter** | ne...@gmail.com |
| **Assignee** | gu...@chromium.org |
| **Created** | 2020-12-28 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36

Steps to reproduce the problem:
os version:
Ubuntu 20.04
chrome version:
Chromium 88.0.4324.11(with asan build)
Chromium 89.0.4371.0(gs://chromium-browser-asan/linux-release/asan-linux-release-839416.zip)

1 ./chrome --use-fake-device-for-media-stream  --enable-experimental-web-platform-features --user-data-dir=/tmp/xx --incognito   http://localhost:8000/crash.html
2 It'll pop up the "use camera?" message box,and click 'allow'.
3 And then will repro uaf.
3 Don't refresh manually, it will repro in a few seconds.In my local test, it repro in about 3 seconds.

What is the expected behavior?

What went wrong?
=1==ERROR: AddressSanitizer: heap-use-after-free on address 0x6140001e8bc8 at pc 0x5562ff2012ef bp 0x7fff57136fd0 sp 0x7fff57136fc8
READ of size 1 at 0x6140001e8bc8 thread T0 (chrome)
    #0 0x5562ff2012ee in blink::MediaStreamVideoTrackUnderlyingSink::write(blink::ScriptState*, blink::ScriptValue, blink::WritableStreamDefaultController*, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/mediastream/pushable_media_stream_video_source.h:29
    #1 0x5562ff2012ee in write ./../../third_party/blink/renderer/modules/mediastream/media_stream_video_track_underlying_sink.cc:42
    #2 0x5562ff2012ee in ?? ??:0
    #3 0x5562fe31da6c in blink::UnderlyingSinkBase::write(blink::ScriptState*, blink::ScriptValue, blink::ScriptValue, blink::ExceptionState&) ./../../third_party/blink/renderer/core/streams/underlying_sink_base.h:52
    #4 0x5562fe31da6c in ?? ??:0
    #5 0x5562fe31ce30 in blink::(anonymous namespace)::WriteOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/core/v8/v8_underlying_sink_base.cc:224
    #6 0x5562fe31ce30 in ?? ??:0
    #7 0x5562e87e6f61 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:158
    #8 0x5562e87e6f61 in ?? ??:0
    #9 0x5562e87e4b1e in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:111
    #10 0x5562e87e4b1e in ?? ??:0
    #11 0x5562e87e33d6 in v8::internal::Builtins::InvokeApiFunction(v8::internal::Isolate*, bool, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, v8::internal::Handle<v8::internal::HeapObject>) ./../../v8/src/builtins/builtins-api.cc:226
    #12 0x5562e87e33d6 in ?? ??:0
    #13 0x5562e8a8b72a in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:275
    #14 0x5562e8a8b72a in ?? ??:0
    #15 0x5562e8a8a120 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) ./../../v8/src/execution/execution.cc:462
    #16 0x5562e8a8a120 in ?? ??:0
    #17 0x5562e86b9c0e in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) ./../../v8/src/api/api.cc:5119
    #18 0x5562e86b9c0e in ?? ??:0
    #19 0x5562f9fede5d in blink::PromiseCall(blink::ScriptState*, v8::Local<v8::Function>, v8::Local<v8::Object>, int, v8::Local<v8::Value>*) ./../../third_party/blink/renderer/core/streams/miscellaneous_operations.cc:466
    #20 0x5562f9fede5d in ?? ??:0
    #21 0x5562f9fefa21 in blink::(anonymous namespace)::JavaScriptStreamAlgorithmWithExtraArg::Run(blink::ScriptState*, int, v8::Local<v8::Value>*) ./../../third_party/blink/renderer/core/streams/miscellaneous_operations.cc:182
    #22 0x5562f9fefa21 in ?? ??:0
    #23 0x5562fa0195cb in blink::WritableStreamDefaultController::ProcessWrite(blink::ScriptState*, blink::WritableStreamDefaultController*, v8::Local<v8::Value>) ./../../third_party/blink/renderer/core/streams/writable_stream_default_controller.cc:564
    #24 0x5562fa0195cb in ?? ??:0
    #25 0x5562fa018c85 in blink::WritableStreamDefaultController::Write(blink::ScriptState*, blink::WritableStreamDefaultController*, v8::Local<v8::Value>, double) ./../../third_party/blink/renderer/core/streams/writable_stream_default_controller.cc:379
    #26 0x5562fa018c85 in ?? ??:0
    #27 0x5562fa01c875 in blink::WritableStreamDefaultWriter::Write(blink::ScriptState*, blink::WritableStreamDefaultWriter*, v8::Local<v8::Value>) ./../../third_party/blink/renderer/core/streams/writable_stream_default_writer.cc:436
    #28 0x5562fa01c875 in ?? ??:0
    #29 0x5562f9fe72da in blink::ReadableStream::PipeToEngine::ReadFulfilled(v8::Local<v8::Value>) ./../../third_party/blink/renderer/core/streams/readable_stream.cc:390
    #30 0x5562f9fe72da in ?? ??:0
    #31 0x5562f9ff0b87 in blink::PromiseHandlerWithValue::CallRaw(v8::FunctionCallbackInfo<v8::Value> const&) ./../../third_party/blink/renderer/core/streams/promise_handler.cc:53
    #32 0x5562f9ff0b87 in ?? ??:0
    #33 0x5562e87e6f61 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:158
    #34 0x5562e87e6f61 in ?? ??:0
    #35 0x5562e87e4b1e in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:111
    #36 0x5562e87e4b1e in ?? ??:0
    #37 0x5562e87e2818 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:141
    #38 0x5562e87e2818 in ?? ??:0
    #39 0x5562ea9e5e97 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc:?
    #40 0x5562ea9e5e97 in ?? ??:0
    #41 0x5562eaa2fd5a in Builtins_PromiseFulfillReactionJob setup-isolate-deserialize.cc:?
    #42 0x5562eaa2fd5a in ?? ??:0
    #43 0x5562ea99fed6 in Builtins_RunMicrotasks setup-isolate-deserialize.cc:?
    #44 0x5562ea99fed6 in ?? ??:0
    #45 0x5562ea97d977 in Builtins_JSRunMicrotasksEntry setup-isolate-deserialize.cc:?
    #46 0x5562ea97d977 in ?? ??:0
    #47 0x5562e8a8af58 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/simulator.h:142
    #48 0x5562e8a8af58 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:383
    #49 0x5562e8a8af58 in ?? ??:0
    #50 0x5562e8a8ea88 in v8::internal::(anonymous namespace)::InvokeWithTryCatch(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:428
    #51 0x5562e8a8ea88 in ?? ??:0
    #52 0x5562e8a8eed8 in v8::internal::Execution::TryRunMicrotasks(v8::internal::Isolate*, v8::internal::MicrotaskQueue*, v8::internal::MaybeHandle<v8::internal::Object>*) ./../../v8/src/execution/execution.cc:505
    #53 0x5562e8a8eed8 in ?? ??:0
    #54 0x5562e8b19f76 in v8::internal::MicrotaskQueue::RunMicrotasks(v8::internal::Isolate*) ./../../v8/src/execution/microtask-queue.cc:165
    #55 0x5562e8b19f76 in ?? ??:0
    #56 0x5562e8b19955 in v8::internal::MicrotaskQueue::PerformCheckpoint(v8::Isolate*) ./../../v8/src/execution/microtask-queue.cc:117
    #57 0x5562e8b19955 in ?? ??:0
    #58 0x5562fa648067 in blink::V8ScriptRunner::CallFunction(v8::Local<v8::Function>, blink::ExecutionContext*, v8::Local<v8::Value>, int, v8::Local<v8::Value>*, v8::Isolate*) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:658
    #59 0x5562fa648067 in ?? ??:0
    #60 0x5562fb32823a in blink::bindings::CallbackInvokeHelper<blink::CallbackFunctionBase, (blink::bindings::CallbackInvokeHelperMode)0>::Call(int, v8::Local<v8::Value>*) ./../../third_party/blink/renderer/bindings/core/v8/callback_invoke_helper.cc:129
    #61 0x5562fb32823a in ?? ??:0
    #62 0x5562fb335848 in blink::V8Function::Invoke(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::HeapVector<blink::ScriptValue, 0u> const&) ./gen/third_party/blink/renderer/bindings/core/v8/v8_function.cc:62
    #63 0x5562fb335848 in ?? ??:0
    #64 0x5562fb335cdc in blink::V8Function::InvokeAndReportException(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::HeapVector<blink::ScriptValue, 0u> const&) ./gen/third_party/blink/renderer/bindings/core/v8/v8_function.cc:125
    #65 0x5562fb335cdc in ?? ??:0
    #66 0x5562fa5890c7 in blink::ScheduledAction::Execute(blink::ExecutionContext*) ./../../third_party/blink/renderer/bindings/core/v8/scheduled_action.cc:138
    #67 0x5562fa5890c7 in ?? ??:0
    #68 0x5562f86af07e in blink::DOMTimer::Fired() ./../../third_party/blink/renderer/core/frame/dom_timer.cc:209
    #69 0x5562f86af07e in ?? ??:0
    #70 0x5562fae0376a in blink::TimerBase::RunInternal() ./../../third_party/blink/renderer/platform/timer.cc:152
    #71 0x5562fae0376a in ?? ??:0
    #72 0x5562fae03cb4 in base::internal::Invoker<base::internal::BindState<void (blink::TimerBase::*)(), base::WeakPtr<blink::TimerBase> >, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:498
    #73 0x5562fae03cb4 in MakeItSo<void (blink::TimerBase::*)(), base::WeakPtr<blink::TimerBase>> ./../../base/bind_internal.h:657
    #74 0x5562fae03cb4 in RunImpl<void (blink::TimerBase::*)(), std::tuple<base::WeakPtr<blink::TimerBase> >, 0> ./../../base/bind_internal.h:710
    #75 0x5562fae03cb4 in RunOnce ./../../base/bind_internal.h:679
    #76 0x5562fae03cb4 in ?? ??:0
    #77 0x5562ebdaecc7 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/callback.h:101
    #78 0x5562ebdaecc7 in RunTask ./../../base/task/common/task_annotator.cc:163
    #79 0x5562ebdaecc7 in ?? ??:0
    #80 0x5562ebdec2b1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:351
    #81 0x5562ebdec2b1 in ?? ??:0
    #82 0x5562ebdeb9f4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:264
    #83 0x5562ebdeb9f4 in ?? ??:0
    #84 0x5562ebcd8080 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39
    #85 0x5562ebcd8080 in ?? ??:0
    #86 0x5562ebdee28c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:460
    #87 0x5562ebdee28c in ?? ??:0
    #88 0x5562ebd5c5a0 in base::RunLoop::Run() ./../../base/run_loop.cc:131
    #89 0x5562ebd5c5a0 in ?? ??:0
    #90 0x5562ff595b0e in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:260
    #91 0x5562ff595b0e in ?? ??:0
    #92 0x5562ebab9369 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:512
    #93 0x5562ebab9369 in ?? ??:0
    #94 0x5562ebabc699 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:902
    #95 0x5562ebabc699 in ?? ??:0
    #96 0x5562ebab67fe in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) ./../../content/app/content_main.cc:372
    #97 0x5562ebab67fe in ?? ??:0
    #98 0x5562ebab6dec in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:398
    #99 0x5562ebab6dec in ?? ??:0
    #100 0x5562e083c067 in ChromeMain ./../../chrome/app/chrome_main.cc:141
    #101 0x5562e083c067 in ?? ??:0
    #102 0x7fe1f0b320b2 in __libc_start_main ??:?
    #103 0x7fe1f0b320b2 in ?? ??:0
0x6140001e8bc8 is located 392 bytes inside of 424-byte region [0x6140001e8a40,0x6140001e8be8)
freed by thread T0 (chrome) here:
    #0 0x5562e0839dad in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160
    #1 0x5562e0839dad in ?? ??:0
    #2 0x5562fad58b32 in blink::MediaStreamSource::InvokePreFinalizer(blink::LivenessBroker const&, void*) ./../../buildtools/third_party/libc++/trunk/include/memory:2378
    #3 0x5562fad58b32 in reset ./../../buildtools/third_party/libc++/trunk/include/memory:2633
    #4 0x5562fad58b32 in Dispose ./../../third_party/blink/renderer/platform/mediastream/media_stream_source.cc:319
    #5 0x5562fad58b32 in InvokePreFinalizer ./../../third_party/blink/renderer/platform/mediastream/media_stream_source.h:57
    #6 0x5562fad58b32 in ?? ??:0
    #7 0x5562eab15caa in blink::ThreadState::InvokePreFinalizers() ./../../third_party/blink/renderer/platform/heap/impl/thread_state.cc:1061
    #8 0x5562eab15caa in ?? ??:0
    #9 0x5562eab19c91 in blink::ThreadState::AtomicPauseSweepAndCompact(blink::BlinkGC::CollectionType, blink::BlinkGC::MarkingType, blink::BlinkGC::SweepingType) ./../../third_party/blink/renderer/platform/heap/impl/thread_state.cc:1381
    #10 0x5562eab19c91 in ?? ??:0
    #11 0x5562eab1ef07 in blink::UnifiedHeapController::TraceEpilogue(v8::EmbedderHeapTracer::TraceSummary*) ./../../third_party/blink/renderer/platform/heap/impl/unified_heap_controller.cc:93
    #12 0x5562eab1ef07 in ?? ??:0
    #13 0x5562e8b87ed2 in v8::internal::LocalEmbedderHeapTracer::TraceEpilogue() ./../../v8/src/heap/embedder-tracing.cc:35
    #14 0x5562e8b87ed2 in ?? ??:0
    #15 0x5562e8c0e14b in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:2091
    #16 0x5562e8c0e14b in ?? ??:0
    #17 0x5562e8c05dde in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:1625
    #18 0x5562e8c05dde in ?? ??:0
    #19 0x5562e8c203f2 in v8::internal::Heap::FinalizeIncrementalMarkingIfComplete(v8::internal::GarbageCollectionReason) ./../../v8/src/heap/heap.cc:1317
    #20 0x5562e8c203f2 in FinalizeIncrementalMarkingIfComplete ./../../v8/src/heap/heap.cc:3469
    #21 0x5562e8c203f2 in ?? ??:0
    #22 0x5562e8c6301a in v8::internal::IncrementalMarkingJob::Task::RunInternal() ./../../v8/src/heap/incremental-marking-job.cc:90
    #23 0x5562e8c6301a in RunInternal ./../../v8/src/heap/incremental-marking-job.cc:128
    #24 0x5562e8c6301a in ?? ??:0
    #25 0x5562ebdaecc7 in Run ./../../base/callback.h:101
    #26 0x5562ebdaecc7 in RunTask ./../../base/task/common/task_annotator.cc:163
    #27 0x5562ebdaecc7 in ?? ??:0
    #28 0x5562ebdec2b1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:351
    #29 0x5562ebdec2b1 in ?? ??:0
    #30 0x5562ebdeb9f4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:264
    #31 0x5562ebdeb9f4 in ?? ??:0
    #32 0x5562ebcd8080 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39
    #33 0x5562ebcd8080 in ?? ??:0
    #34 0x5562ebdee28c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:460
    #35 0x5562ebdee28c in ?? ??:0
    #36 0x5562ebd5c5a0 in base::RunLoop::Run() ./../../base/run_loop.cc:131
    #37 0x5562ebd5c5a0 in ?? ??:0
    #38 0x5562ff595b0e in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:260
    #39 0x5562ff595b0e in ?? ??:0
    #40 0x5562ebab9369 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:512
    #41 0x5562ebab9369 in ?? ??:0
    #42 0x5562ebabc699 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:902
    #43 0x5562ebabc699 in ?? ??:0
    #44 0x5562ebab67fe in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) ./../../content/app/content_main.cc:372
    #45 0x5562ebab67fe in ?? ??:0
    #46 0x5562ebab6dec in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:398
    #47 0x5562ebab6dec in ?? ??:0
    #48 0x5562e083c067 in ChromeMain ./../../chrome/app/chrome_main.cc:141
    #49 0x5562e083c067 in ?? ??:0
    #50 0x7fe1f0b320b2 in __libc_start_main ??:?
    #51 0x7fe1f0b320b2 in ?? ??:0

previously allocated by thread T0 (chrome) here:
    #0 0x5562e083954d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99
    #1 0x5562e083954d in ?? ??:0
    #2 0x5562ff1ffeab in blink::MediaStreamTrackGenerator::CreateOutputPlatformTrack() ./../../buildtools/third_party/libc++/trunk/include/memory:3043
    #3 0x5562ff1ffeab in CreateOutputPlatformTrack ./../../third_party/blink/renderer/modules/mediastream/media_stream_track_generator.cc:48
    #4 0x5562ff1ffeab in ?? ??:0
    #5 0x5562ff1ffd61 in blink::MediaStreamTrackGenerator::MediaStreamTrackGenerator(blink::ScriptState*, blink::MediaStreamSource::StreamType, WTF::String const&) ./../../third_party/blink/renderer/modules/mediastream/media_stream_track_generator.cc:34
    #6 0x5562ff1ffd61 in ?? ??:0
    #7 0x5562ff20073a in blink::MediaStreamTrackGenerator::Create(blink::ScriptState*, WTF::String const&, blink::ExceptionState&) ./../../third_party/blink/renderer/platform/heap/impl/heap.h:568
    #8 0x5562ff20073a in MakeGarbageCollected<blink::MediaStreamTrackGenerator, blink::ScriptState *&, blink::MediaStreamSource::StreamType, WTF::String> ./../../third_party/blink/renderer/platform/heap/impl/heap.h:608
    #9 0x5562ff20073a in Create ./../../third_party/blink/renderer/modules/mediastream/media_stream_track_generator.cc:87
    #10 0x5562ff20073a in ?? ??:0
    #11 0x5562ff1ff203 in blink::(anonymous namespace)::ConstructorCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_media_stream_track_generator.cc:130
    #12 0x5562ff1ff203 in ?? ??:0
    #13 0x5562e87e6f61 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:158
    #14 0x5562e87e6f61 in ?? ??:0
    #15 0x5562e87e3e36 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:111
    #16 0x5562e87e3e36 in ?? ??:0
    #17 0x5562e87e278b in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:137
    #18 0x5562e87e278b in ?? ??:0
    #19 0x5562ea9e5e97 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc:?
    #20 0x5562ea9e5e97 in ?? ??:0
    #21 0x5562ea97cfe0 in Builtins_JSBuiltinsConstructStub setup-isolate-deserialize.cc:?
    #22 0x5562ea97cfe0 in ?? ??:0
    #23 0x5562eaa7217e in Builtins_ConstructHandler setup-isolate-deserialize.cc:?
    #24 0x5562eaa7217e in ?? ??:0
error: unknown argument '--demangle=True'
addr2line: '/home/test/an-linux-release/chrome': No such file
    #25 0x5562ea97fdae in
    #26 0x5562ea97fdae in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc:?
    #27 0x5562ea97fdae in ?? ??:0
    #28 0x5562ea97fdae in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc:?
    #29 0x5562ea97fdae in ?? ??:0
    #30 0x5562ea9acf60 in Builtins_AsyncFunctionAwaitResolveClosure setup-isolate-deserialize.cc:?
    #31 0x5562ea9acf60 in ?? ??:0
    #32 0x5562eaa2fd5a in Builtins_PromiseFulfillReactionJob setup-isolate-deserialize.cc:?
    #33 0x5562eaa2fd5a in ?? ??:0
    #34 0x5562ea99fed6 in Builtins_RunMicrotasks setup-isolate-deserialize.cc:?
    #35 0x5562ea99fed6 in ?? ??:0
    #36 0x5562ea97d977 in Builtins_JSRunMicrotasksEntry setup-isolate-deserialize.cc:?
    #37 0x5562ea97d977 in ?? ??:0
    #38 0x5562e8a8af58 in Call ./../../v8/src/execution/simulator.h:142
    #39 0x5562e8a8af58 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:383
    #40 0x5562e8a8af58 in ?? ??:0
    #41 0x5562e8a8ea88 in v8::internal::(anonymous namespace)::InvokeWithTryCatch(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:428
    #42 0x5562e8a8ea88 in ?? ??:0
    #43 0x5562e8a8eed8 in v8::internal::Execution::TryRunMicrotasks(v8::internal::Isolate*, v8::internal::MicrotaskQueue*, v8::internal::MaybeHandle<v8::internal::Object>*) ./../../v8/src/execution/execution.cc:505
    #44 0x5562e8a8eed8 in ?? ??:0
    #45 0x5562e8b19f76 in v8::internal::MicrotaskQueue::RunMicrotasks(v8::internal::Isolate*) ./../../v8/src/execution/microtask-queue.cc:165
    #46 0x5562e8b19f76 in ?? ??:0
    #47 0x5562e8b19955 in v8::internal::MicrotaskQueue::PerformCheckpoint(v8::Isolate*) ./../../v8/src/execution/microtask-queue.cc:117
    #48 0x5562e8b19955 in ?? ??:0
    #49 0x5562eaba4fa0 in blink::scheduler::MainThreadSchedulerImpl::OnTaskCompleted(base::WeakPtr<blink::scheduler::MainThreadTaskQueue>, base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::sequence_manager::LazyNow*) ./../../third_party/blink/renderer/platform/scheduler/main_thread/main_thread_scheduler_impl.cc:2632
    #50 0x5562eaba4fa0 in ?? ??:0
    #51 0x5562eabb2db3 in blink::scheduler::MainThreadTaskQueue::OnTaskCompleted(base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::sequence_manager::LazyNow*) ./../../third_party/blink/renderer/platform/scheduler/main_thread/main_thread_task_queue.cc:144
    #52 0x5562eabb2db3 in ?? ??:0
    #53 0x5562ebdbda7c in base::sequence_manager::internal::SequenceManagerImpl::NotifyDidProcessTask(base::sequence_manager::internal::SequenceManagerImpl::ExecutingTask*, base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/sequence_manager_impl.cc:852
    #54 0x5562ebdbda7c in ?? ??:0
    #55 0x5562ebdbd33c in base::sequence_manager::internal::SequenceManagerImpl::DidRunTask() ./../../base/task/sequence_manager/sequence_manager_impl.cc:677
    #56 0x5562ebdbd33c in ?? ??:0
    #57 0x5562ebdec38d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356
    #58 0x5562ebdec38d in ?? ??:0
    #59 0x5562ebdeb9f4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:264
    #60 0x5562ebdeb9f4 in ?? ??:0
    #61 0x5562ebcd8080 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39
    #62 0x5562ebcd8080 in ?? ??:0

Did this work before? N/A 

Chrome version: 89.0.4371.0  Channel: n/a
OS Version: 20.04
Flash Version:

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 4.7 KB)
- [chome.asan](attachments/chome.asan) (application/octet-stream, 16.8 KB)

## Timeline

### [Deleted User] (2020-12-28)

[Empty comment from Monorail migration]

### aj...@google.com (2020-12-28)

Thanks, this repros (renderer RCE) on Windows after ~10s.

--use-fake-device-for-media-stream --enable-experimental-web-platform-features --no-sandbox https://192.168.11.1:8443/crash.html

+mediastream owners, assigning guidou as owner using git blame. 

[Monorail components: Blink>GetUserMedia]

### aj...@google.com (2020-12-28)

(+Beta as M88)

### [Deleted User] (2020-12-28)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-29)

Setting milestone and target because of Security_Impact=Beta and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-29)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-29)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### hb...@chromium.org (2021-01-05)

Please take a look, Guido

### gu...@chromium.org (2021-01-05)

Note that this is behind a flag.
Fix sent for review at https://chromium-review.googlesource.com/c/chromium/src/+/2610036

### gu...@chromium.org (2021-01-05)

[Empty comment from Monorail migration]

[Monorail components: -Blink>GetUserMedia Blink>MediaStream]

### sr...@google.com (2021-01-05)

should this block stable , if this is behind a flag? adetaylor@

### ad...@chromium.org (2021-01-05)

Per https://chromium.googlesource.com/chromium/src/+/master/docs/security/security-labels.md#TOC-Security_Impact-None, this is Security_Impact-None if it's behind --enable-experimental-web-platform-features and therefore I have removed RBS.

Obviously it needs to be fixed before the feature becomes non-experimental.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/41ffde71b6cf181676a2bfbcbdcf015932dcab4b

commit 41ffde71b6cf181676a2bfbcbdcf015932dcab4b
Author: Guido Urdaneta <guidou@chromium.org>
Date: Wed Jan 06 11:05:31 2021

[BreakoutBox] Use weak pointer in MediaStreamVideoTrackUnderlyingSink

Replace the raw pointer to a PushableMediaStreamVideoSource with
a weak pointer.

Bug: 1162036
Change-Id: I9b786cfd3800f8e37daabacf039e6b12e2423f76
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2610036
Auto-Submit: Guido Urdaneta <guidou@chromium.org>
Reviewed-by: Thomas Guilbert <tguilbert@chromium.org>
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Reviewed-by: Harald Alvestrand <hta@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/heads/master@{#840551}

[modify] https://crrev.com/41ffde71b6cf181676a2bfbcbdcf015932dcab4b/third_party/blink/renderer/modules/mediastream/media_stream_video_track_underlying_sink.cc
[modify] https://crrev.com/41ffde71b6cf181676a2bfbcbdcf015932dcab4b/third_party/blink/renderer/modules/mediastream/media_stream_video_track_underlying_sink.h


### gu...@chromium.org (2021-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-06)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-01-14)

Congratulations! The VRP panel has decided to reward you $5000 for this report. Nice job!

### ad...@google.com (2021-01-14)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1162036?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054308)*
