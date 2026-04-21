#  uaf in AudioNodeOutput::Pull

| Field | Value |
|-------|-------|
| **Issue ID** | [40054024](https://issues.chromium.org/issues/40054024) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebAudio |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ne...@gmail.com |
| **Assignee** | rt...@chromium.org |
| **Created** | 2020-11-30 |
| **Bounty** | $6,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36

Steps to reproduce the problem:
chrome version:
Chromium 88.0.4315.5 (dev build)
Chromium 89.0.4342.0

The issue(1148170) state was set to "won't fix" and no one is tracking it. 
So I opened new issue. If necessary, it can be merged into that issue(1148170).
I still can reproduce this issue with dev and latest canary stably.

./chrome --js-flags=--expose-gc --user-data-dir=/tmp/nnn http://localhost:8000/crash.html

What is the expected behavior?

What went wrong?
=================================================================
==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x60b00005cec0 at pc 0x55602e1d6643 bp 0x7fcff044ee30 sp 0x7fcff044ee28
WRITE of size 1 at 0x60b00005cec0 thread T13 (Offline AudioWo)
error: unknown argument '--demangle=True'
    #0 0x55602e1d6642 in blink::AudioNodeOutput::Pull(blink::AudioBus*, unsigned int) ./../../third_party/blink/renderer/modules/webaudio/audio_node_output.cc:131
    #1 0x55602e1d6642 in ?? ??:0
    #2 0x55602e1f5f1c in blink::AudioNodeInput::Pull(blink::AudioBus*, unsigned int) ./../../third_party/blink/renderer/modules/webaudio/audio_node_input.cc:128
    #3 0x55602e1f5f1c in Pull ./../../third_party/blink/renderer/modules/webaudio/audio_node_input.cc:158
    #4 0x55602e1f5f1c in ?? ??:0
    #5 0x55602f8c2d13 in blink::OfflineAudioDestinationHandler::RenderIfNotSuspended(blink::AudioBus*, blink::AudioBus*, unsigned int) ./../../third_party/blink/renderer/modules/webaudio/offline_audio_destination_node.cc:302
    #6 0x55602f8c2d13 in ?? ??:0
    #7 0x55602f8c1a45 in blink::OfflineAudioDestinationHandler::DoOfflineRendering() ./../../third_party/blink/renderer/modules/webaudio/offline_audio_destination_node.cc:191
    #8 0x55602f8c1a45 in ?? ??:0
    #9 0x55601c9f9d67 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/callback.h:101
    #10 0x55601c9f9d67 in RunTask ./../../base/task/common/task_annotator.cc:163
    #11 0x55601c9f9d67 in ?? ??:0
    #12 0x55601ca37046 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:352
    #13 0x55601ca37046 in ?? ??:0
    #14 0x55601ca36784 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:268
    #15 0x55601ca36784 in ?? ??:0
    #16 0x55601c924c70 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39
    #17 0x55601c924c70 in ?? ??:0
    #18 0x55601ca39035 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:471
    #19 0x55601ca39035 in ?? ??:0
    #20 0x55601c9a7d20 in base::RunLoop::Run() ./../../base/run_loop.cc:124
    #21 0x55601c9a7d20 in ?? ??:0
    #22 0x55601b82d630 in blink::scheduler::WorkerThread::SimpleThreadImpl::Run() ./../../third_party/blink/renderer/platform/scheduler/worker/worker_thread.cc:169
    #23 0x55601b82d630 in ?? ??:0
    #24 0x55601cb1be70 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:87
    #25 0x55601cb1be70 in ?? ??:0
error: unknown argument '--demangle=True'
    #26 0x7fd007e7f608 in start_thread /build/glibc-ZN95T4/glibc-2.31/nptl/pthread_create.c:477
    #27 0x7fd007e7f608 in ?? ??:0

0x60b00005cec0 is located 32 bytes inside of 104-byte region [0x60b00005cea0,0x60b00005cf08)
freed by thread T0 (chrome) here:
    #0 0x556011a2cdd2 in __interceptor_free /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:127
    #1 0x556011a2cdd2 in ?? ??:0
    #2 0x55602e1de179 in blink::AudioHandler::~AudioHandler() ./../../buildtools/third_party/libc++/trunk/include/memory:2633
    #3 0x55602e1de179 in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/memory:2587
    #4 0x55602e1de179 in Destruct ./../../third_party/blink/renderer/platform/wtf/vector.h:110
    #5 0x55602e1de179 in Destruct ./../../third_party/blink/renderer/platform/wtf/vector.h:412
    #6 0x55602e1de179 in Finalize ./../../third_party/blink/renderer/platform/wtf/vector.h:1412
    #7 0x55602e1de179 in ~ConditionalDestructor ./../../third_party/blink/renderer/platform/wtf/conditional_destructor.h:24
    #8 0x55602e1de179 in ~AudioHandler ./../../third_party/blink/renderer/modules/webaudio/audio_node.cc:94
    #9 0x55602e1de179 in ?? ??:0
    #10 0x55602e341e9d in blink::ChannelSplitterHandler::~ChannelSplitterHandler() ./../../third_party/blink/renderer/modules/webaudio/channel_splitter_node.h:37
    #11 0x55602e341e9d in ?? ??:0
    #12 0x55602e1ff191 in WTF::Vector<scoped_refptr<blink::AudioHandler>, 0u, WTF::PartitionAllocator>::ShrinkCapacity(unsigned int) ./../../third_party/blink/renderer/platform/wtf/thread_safe_ref_counted.h:64
    #13 0x55602e1ff191 in Destruct ./../../third_party/blink/renderer/platform/wtf/thread_safe_ref_counted.h:44
    #14 0x55602e1ff191 in Release ./../../base/memory/ref_counted.h:400
    #15 0x55602e1ff191 in Release ./../../base/memory/scoped_refptr.h:322
    #16 0x55602e1ff191 in ~scoped_refptr ./../../base/memory/scoped_refptr.h:224
    #17 0x55602e1ff191 in Destruct ./../../third_party/blink/renderer/platform/wtf/vector.h:110
    #18 0x55602e1ff191 in Destruct ./../../third_party/blink/renderer/platform/wtf/vector.h:412
    #19 0x55602e1ff191 in Shrink ./../../third_party/blink/renderer/platform/wtf/vector.h:1770
    #20 0x55602e1ff191 in ShrinkCapacity ./../../third_party/blink/renderer/platform/wtf/vector.h:1832
    #21 0x55602e1ff191 in ?? ??:0
    #22 0x55602e1fd961 in blink::DeferredTaskHandler::ClearHandlersToBeDeleted() ./../../third_party/blink/renderer/platform/wtf/vector.h:1265
    #23 0x55602e1fd961 in ClearHandlersToBeDeleted ./../../third_party/blink/renderer/modules/webaudio/deferred_task_handler.cc:376
    #24 0x55602e1fd961 in ?? ??:0
    #25 0x55602e1a9f7d in blink::BaseAudioContext::Uninitialize() ./../../third_party/blink/renderer/modules/webaudio/base_audio_context.cc:146
    #26 0x55602e1a9f7d in Uninitialize ./../../third_party/blink/renderer/modules/webaudio/base_audio_context.cc:175
    #27 0x55602e1a9f7d in ?? ??:0
    #28 0x556028dd1d49 in blink::ExecutionContext::NotifyContextDestroyed() ./../../third_party/blink/renderer/core/execution_context/execution_context.cc:146
    #29 0x556028dd1d49 in ForEachObserver<(lambda at ../../third_party/blink/renderer/core/execution_context/execution_context.cc:145:7)> ./../../third_party/blink/renderer/platform/heap_observer_set.h:66
    #30 0x556028dd1d49 in NotifyContextDestroyed ./../../third_party/blink/renderer/core/execution_context/execution_context.cc:144
    #31 0x556028dd1d49 in ?? ??:0
    #32 0x556028f291b5 in blink::LocalDOMWindow::FrameDestroyed() ./../../third_party/blink/renderer/core/frame/local_dom_window.cc:797
    #33 0x556028f291b5 in ?? ??:0
    #34 0x556028f89946 in blink::LocalFrame::DetachImpl(blink::FrameDetachType) ./../../third_party/blink/renderer/core/frame/local_frame.cc:623
    #35 0x556028f89946 in ?? ??:0
    #36 0x556028f06c78 in blink::Frame::Detach(blink::FrameDetachType) ./../../third_party/blink/renderer/core/frame/frame.cc:124
    #37 0x556028f06c78 in ?? ??:0
    #38 0x556028684bb4 in blink::ChildFrameDisconnector::DisconnectCollectedFrameOwners() ./../../third_party/blink/renderer/core/dom/child_frame_disconnector.cc:59
    #39 0x556028684bb4 in ?? ??:0
    #40 0x556028684041 in blink::ChildFrameDisconnector::Disconnect(blink::ChildFrameDisconnector::DisconnectPolicy) ./../../third_party/blink/renderer/core/dom/child_frame_disconnector.cc:32
    #41 0x556028684041 in ?? ??:0
    #42 0x556028615fed in blink::ContainerNode::WillRemoveChild(blink::Node&) ./../../third_party/blink/renderer/core/dom/container_node.cc:624
    #43 0x556028615fed in ?? ??:0
    #44 0x556028615176 in blink::ContainerNode::RemoveChild(blink::Node*, blink::ExceptionState&) ./../../third_party/blink/renderer/core/dom/container_node.cc:700
    #45 0x556028615176 in ?? ??:0
    #46 0x5560289d0aa7 in blink::Node::removeChild(blink::Node*, blink::ExceptionState&) ./../../third_party/blink/renderer/core/dom/node.cc:739
    #47 0x5560289d0aa7 in ?? ??:0
    #48 0x55602bf50078 in blink::(anonymous namespace)::RemoveChildOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/core/v8/v8_node.cc:964
    #49 0x55602bf50078 in ?? ??:0
    #50 0x5560194b95b1 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:158
    #51 0x5560194b95b1 in ?? ??:0
    #52 0x5560194b717d in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:111
    #53 0x5560194b717d in ?? ??:0
    #54 0x5560194b4ec1 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:141
    #55 0x5560194b4ec1 in ?? ??:0
    #56 0x55601b6449b7 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc:?
    #57 0x55601b6449b7 in ?? ??:0
    #58 0x55601b5de96e in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc:?
    #59 0x55601b5de96e in ?? ??:0
    #60 0x55601b5dc5da in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc:?
    #61 0x55601b5dc5da in ?? ??:0
    #62 0x55601b5dc3b7 in Builtins_JSEntry setup-isolate-deserialize.cc:?
    #63 0x55601b5dc3b7 in ?? ??:0
    #64 0x556019757145 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/simulator.h:142
    #65 0x556019757145 in Invoke ./../../v8/src/execution/execution.cc:368
    #66 0x556019757145 in ?? ??:0
    #67 0x5560197560f0 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) ./../../v8/src/execution/execution.cc:462
    #68 0x5560197560f0 in ?? ??:0
    #69 0x55601938f02e in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) ./../../v8/src/api/api.cc:4984
    #70 0x55601938f02e in ?? ??:0
    #71 0x55602aea8371 in blink::V8ScriptRunner::CallFunction(v8::Local<v8::Function>, blink::ExecutionContext*, v8::Local<v8::Value>, int, v8::Local<v8::Value>*, v8::Isolate*) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:632
    #72 0x55602aea8371 in ?? ??:0
    #73 0x55602bb49dfa in blink::bindings::CallbackInvokeHelper<blink::CallbackFunctionBase, (blink::bindings::CallbackInvokeHelperMode)0>::Call(int, v8::Local<v8::Value>*) ./../../third_party/blink/renderer/bindings/core/v8/callback_invoke_helper.cc:129
    #74 0x55602bb49dfa in ?? ??:0
    #75 0x55602bb573fc in blink::V8Function::Invoke(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::HeapVector<blink::ScriptValue, 0u> const&) ./gen/third_party/blink/renderer/bindings/core/v8/v8_function.cc:62
    #76 0x55602bb573fc in ?? ??:0
    #77 0x55602bb5788c in blink::V8Function::InvokeAndReportException(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::HeapVector<blink::ScriptValue, 0u> const&) ./gen/third_party/blink/renderer/bindings/core/v8/v8_function.cc:125
    #78 0x55602bb5788c in ?? ??:0

previously allocated by thread T0 (chrome) here:
    #0 0x556011a2d03d in __interceptor_malloc /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:145
    #1 0x556011a2d03d in ?? ??:0
    #2 0x556021cb5a18 in WTF::Partitions::FastMalloc(unsigned long, char const*) ./../../base/allocator/partition_allocator/partition_root.h:781
    #3 0x556021cb5a18 in Alloc ./../../base/allocator/partition_allocator/partition_root.h:1029
    #4 0x556021cb5a18 in FastMalloc ./../../third_party/blink/renderer/platform/wtf/allocator/partitions.cc:265
    #5 0x556021cb5a18 in ?? ??:0
    #6 0x55602e1dea78 in blink::AudioHandler::AddOutput(unsigned int) ./../../third_party/blink/renderer/modules/webaudio/audio_node_output.h:44
    #7 0x55602e1dea78 in make_unique<blink::AudioNodeOutput, blink::AudioHandler *, unsigned int &> ./../../buildtools/third_party/libc++/trunk/include/memory:3043
    #8 0x55602e1dea78 in AddOutput ./../../third_party/blink/renderer/modules/webaudio/audio_node.cc:202
    #9 0x55602e1dea78 in ?? ??:0
    #10 0x55602e34042c in blink::ChannelSplitterHandler::ChannelSplitterHandler(blink::AudioNode&, float, unsigned int) ./../../third_party/blink/renderer/modules/webaudio/channel_splitter_node.cc:50
    #11 0x55602e34042c in ?? ??:0
    #12 0x55602e34194e in blink::ChannelSplitterNode::ChannelSplitterNode(blink::BaseAudioContext&, unsigned int) ./../../third_party/blink/renderer/modules/webaudio/channel_splitter_node.cc:60
    #13 0x55602e34194e in ChannelSplitterNode ./../../third_party/blink/renderer/modules/webaudio/channel_splitter_node.cc:133
    #14 0x55602e34194e in ?? ??:0
    #15 0x55602e341c9c in blink::ChannelSplitterNode::Create(blink::BaseAudioContext&, unsigned int, blink::ExceptionState&) ./../../third_party/blink/renderer/platform/heap/impl/heap.h:570
    #16 0x55602e341c9c in MakeGarbageCollected<blink::ChannelSplitterNode, blink::BaseAudioContext &, unsigned int &> ./../../third_party/blink/renderer/platform/heap/impl/heap.h:610
    #17 0x55602e341c9c in Create ./../../third_party/blink/renderer/modules/webaudio/channel_splitter_node.cc:164
    #18 0x55602e341c9c in ?? ??:0
    #19 0x55602e23e49b in blink::(anonymous namespace)::CreateChannelSplitterOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_base_audio_context.cc:458
    #20 0x55602e23e49b in ?? ??:0
    #21 0x5560194b95b1 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:158
    #22 0x5560194b95b1 in ?? ??:0
    #23 0x5560194b717d in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:111
    #24 0x5560194b717d in ?? ??:0
    #25 0x5560194b4ec1 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:141
    #26 0x5560194b4ec1 in ?? ??:0
    #27 0x55601b6449b7 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc:?
    #28 0x55601b6449b7 in ?? ??:0
    #29 0x55601b5de96e in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc:?
    #30 0x55601b5de96e in ?? ??:0
    #31 0x55601b60b840 in Builtins_AsyncFunctionAwaitResolveClosure setup-isolate-deserialize.cc:?
    #32 0x55601b60b840 in ?? ??:0
    #33 0x55601b68e73a in Builtins_PromiseFulfillReactionJob setup-isolate-deserialize.cc:?
    #34 0x55601b68e73a in ?? ??:0
    #35 0x55601b5fe8d6 in Builtins_RunMicrotasks setup-isolate-deserialize.cc:?
    #36 0x55601b5fe8d6 in ?? ??:0
    #37 0x55601b5dc537 in Builtins_JSRunMicrotasksEntry setup-isolate-deserialize.cc:?
    #38 0x55601b5dc537 in ?? ??:0
    #39 0x556019756f3e in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/simulator.h:142
    #40 0x556019756f3e in Invoke ./../../v8/src/execution/execution.cc:383
    #41 0x556019756f3e in ?? ??:0
    #42 0x55601975aa18 in v8::internal::(anonymous namespace)::InvokeWithTryCatch(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:428
    #43 0x55601975aa18 in ?? ??:0
    #44 0x55601975ae68 in v8::internal::Execution::TryRunMicrotasks(v8::internal::Isolate*, v8::internal::MicrotaskQueue*, v8::internal::MaybeHandle<v8::internal::Object>*) ./../../v8/src/execution/execution.cc:505
    #45 0x55601975ae68 in ?? ??:0
    #46 0x5560197e3676 in v8::internal::MicrotaskQueue::RunMicrotasks(v8::internal::Isolate*) ./../../v8/src/execution/microtask-queue.cc:165
    #47 0x5560197e3676 in ?? ??:0
    #48 0x5560197e3055 in v8::internal::MicrotaskQueue::PerformCheckpoint(v8::Isolate*) ./../../v8/src/execution/microtask-queue.cc:117
    #49 0x5560197e3055 in ?? ??:0
    #50 0x55601b8008c0 in blink::scheduler::MainThreadSchedulerImpl::OnTaskCompleted(base::WeakPtr<blink::scheduler::MainThreadTaskQueue>, base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::sequence_manager::LazyNow*) ./../../third_party/blink/renderer/platform/scheduler/main_thread/main_thread_scheduler_impl.cc:2634
    #51 0x55601b8008c0 in ?? ??:0
    #52 0x55601b80e363 in blink::scheduler::MainThreadTaskQueue::OnTaskCompleted(base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::sequence_manager::LazyNow*) ./../../third_party/blink/renderer/platform/scheduler/main_thread/main_thread_task_queue.cc:144
    #53 0x55601b80e363 in ?? ??:0
    #54 0x55601ca0894c in base::sequence_manager::internal::SequenceManagerImpl::NotifyDidProcessTask(base::sequence_manager::internal::SequenceManagerImpl::ExecutingTask*, base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/sequence_manager_impl.cc:843
    #55 0x55601ca0894c in ?? ??:0
    #56 0x55601ca0820c in base::sequence_manager::internal::SequenceManagerImpl::DidRunTask() ./../../base/task/sequence_manager/sequence_manager_impl.cc:668
    #57 0x55601ca0820c in ?? ??:0
    #58 0x55601ca37151 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:365
    #59 0x55601ca37151 in ?? ??:0
    #60 0x55601ca36784 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:268
    #61 0x55601ca36784 in ?? ??:0
    #62 0x55601c924c70 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39
    #63 0x55601c924c70 in ?? ??:0
    #64 0x55601ca39035 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:471
    #65 0x55601ca39035 in ?? ??:0
    #66 0x55601c9a7d20 in base::RunLoop::Run() ./../../base/run_loop.cc:124
    #67 0x55601c9a7d20 in ?? ??:0

Thread T13 (Offline AudioWo) created by T0 (chrome) here:
    #0 0x556011a1740a in __interceptor_pthread_create /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:214
    #1 0x556011a1740a in ?? ??:0
    #2 0x55601cb1b0fe in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, base::PlatformThreadHandle*, base::ThreadPriority) ./../../base/threading/platform_thread_posix.cc:126
    #3 0x55601cb1b0fe in ?? ??:0
    #4 0x55601ca8dc82 in base::SimpleThread::StartAsync() ./../../base/threading/simple_thread.cc:51
    #5 0x55601ca8dc82 in ?? ??:0
    #6 0x55601b82bc05 in blink::scheduler::WorkerThread::Init() ./../../third_party/blink/renderer/platform/scheduler/worker/worker_thread.cc:61
    #7 0x55601b82bc05 in ?? ??:0
    #8 0x55601b791d5a in blink::Thread::CreateThread(blink::ThreadCreationParams const&) ./../../third_party/blink/renderer/platform/scheduler/common/thread.cc:82
    #9 0x55601b791d5a in ?? ??:0
    #10 0x55602ad0b9e6 in blink::WorkerBackingThread::WorkerBackingThread(blink::ThreadCreationParams const&) ./../../third_party/blink/renderer/core/workers/worker_backing_thread.cc:60
    #11 0x55602ad0b9e6 in ?? ??:0
    #12 0x55602e2d4869 in blink::WorkletThreadHolder<blink::OfflineAudioWorkletThread>::EnsureInstance(blink::ThreadCreationParams const&) ./../../buildtools/third_party/libc++/trunk/include/memory:3043
    #13 0x55602e2d4869 in EnsureInstance ./../../third_party/blink/renderer/core/workers/worklet_thread_holder.h:34
    #14 0x55602e2d4869 in ?? ??:0
    #15 0x55602e2d5836 in blink::OfflineAudioWorkletThread::OfflineAudioWorkletThread(blink::WorkerReportingProxy&) ./../../third_party/blink/renderer/modules/webaudio/offline_audio_worklet_thread.cc:48
    #16 0x55602e2d5836 in OfflineAudioWorkletThread ./../../third_party/blink/renderer/modules/webaudio/offline_audio_worklet_thread.cc:31
    #17 0x55602e2d5836 in ?? ??:0
    #18 0x55602e283f69 in blink::AudioWorkletMessagingProxy::CreateWorkletThreadWithConstraints(blink::WorkerReportingProxy&, bool, bool) ./../../buildtools/third_party/libc++/trunk/include/memory:3043
    #19 0x55602e283f69 in CreateWorkletThreadWithConstraints ./../../third_party/blink/renderer/modules/webaudio/audio_worklet_messaging_proxy.cc:114
    #20 0x55602e283f69 in ?? ??:0
    #21 0x55602e283e71 in blink::AudioWorkletMessagingProxy::CreateWorkerThread() ./../../third_party/blink/renderer/modules/webaudio/audio_worklet_messaging_proxy.cc:102
    #22 0x55602e283e71 in ?? ??:0
    #23 0x55602acb356c in blink::ThreadedMessagingProxyBase::InitializeWorkerThread(std::__1::unique_ptr<blink::GlobalScopeCreationParams, std::__1::default_delete<blink::GlobalScopeCreationParams> >, base::Optional<blink::WorkerBackingThreadStartupData> const&, base::Optional<util::TokenType<blink::DedicatedWorkerTokenTypeMarker> const> const&) ./../../third_party/blink/renderer/core/workers/threaded_messaging_proxy_base.cc:73
    #24 0x55602acb356c in ?? ??:0
    #25 0x55602e2d8b1d in blink::ThreadedWorkletMessagingProxy::Initialize(blink::WorkerClients*, blink::WorkletModuleResponsesMap*, base::Optional<blink::WorkerBackingThreadStartupData> const&) ./../../third_party/blink/renderer/core/workers/threaded_worklet_messaging_proxy.cc:80
    #26 0x55602e2d8b1d in ?? ??:0
    #27 0x55602e282093 in blink::AudioWorklet::CreateGlobalScope() ./../../third_party/blink/renderer/modules/webaudio/audio_worklet.cc:81
    #28 0x55602e282093 in ?? ??:0
    #29 0x55602ad331ba in blink::Worklet::FetchAndInvokeScript(blink::KURL const&, WTF::String const&, blink::WorkletPendingTasks*) ./../../third_party/blink/renderer/core/workers/worklet.cc:166
    #30 0x55602ad331ba in ?? ??:0
    #31 0x55601c9f9d67 in Run ./../../base/callback.h:101
    #32 0x55601c9f9d67 in RunTask ./../../base/task/common/task_annotator.cc:163
    #33 0x55601c9f9d67 in ?? ??:0
    #34 0x55601ca37046 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:352
    #35 0x55601ca37046 in ?? ??:0
    #36 0x55601ca36784 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:268
    #37 0x55601ca36784 in ?? ??:0
    #38 0x55601c924c70 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39
    #39 0x55601c924c70 in ?? ??:0
    #40 0x55601ca39035 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:471
    #41 0x55601ca39035 in ?? ??:0
    #42 0x55601c9a7d20 in base::RunLoop::Run() ./../../base/run_loop.cc:124
    #43 0x55601c9a7d20 in ?? ??:0
    #44 0x55602fcd36fe in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:256
    #45 0x55602fcd36fe in ?? ??:0
    #46 0x55601c6e3d78 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:499
    #47 0x55601c6e3d78 in ?? ??:0
    #48 0x55601c6e70a9 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:885
    #49 0x55601c6e70a9 in ?? ??:0
    #50 0x55601c6e0cce in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) ./../../content/app/content_main.cc:372
    #51 0x55601c6e0cce in ?? ??:0
    #52 0x55601c6e12bc in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:398
    #53 0x55601c6e12bc in ?? ??:0
    #54 0x556011a596c7 in ChromeMain ./../../chrome/app/chrome_main.cc:130
    #55 0x556011a596c7 in ?? ??:0
error: unknown argument '--demangle=True'
    #56 0x7fd0062110b2 in __libc_start_main ??:?
    #57 0x7fd0062110b2 in ?? ??:0

SUMMARY: AddressSanitizer: heap-use-after-free (/home/test/asan-linux-release/chrome+0x269e0642)
Shadow bytes around the buggy address:
  0x0c1680003980: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa
  0x0c1680003990: fa fa fd fd fd fd fd fd fd fd fd fd fd fd fd fa
  0x0c16800039a0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c16800039b0: fd fd fd fd fd fa fa fa fa fa fa fa fa fa fd fd
  0x0c16800039c0: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
=>0x0c16800039d0: fa fa fa fa fd fd fd fd[fd]fd fd fd fd fd fd fd
  0x0c16800039e0: fd fa fa fa fa fa fa fa fa fa fd fd fd fd fd fd
  0x0c16800039f0: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x0c1680003a00: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa
  0x0c1680003a10: fa fa fa fa fa fa fd fd fd fd fd fd fd fd fd fd
  0x0c1680003a20: fd fd fd fa fa fa fa fa fa fa fa fa fd fd fd fd
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

Chrome version: Chromium 89.0.4342.0(Canary)  Channel: dev
OS Version: 20.04
Flash Version:

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 565 B)
- [processor.js](attachments/processor.js) (text/plain, 261 B)
- [sub_frame.html](attachments/sub_frame.html) (text/plain, 603 B)

## Timeline

### [Deleted User] (2020-11-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-12-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6278143293063168.

### cl...@chromium.org (2020-12-01)

Testcase 6278143293063168 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6278143293063168.

### ct...@chromium.org (2020-12-01)

I'm able to reproduce on a linux ASAN release build (r830420), but clusterfuzz is having some trouble. Doing some initial triage while I try to get clusterfuzz to reproduce this: Severity-High (memory corruption in renderer), Impact-Beta (until clusterfuzz can test futher), and setting all Blink platforms.

[Monorail components: Blink>WebAudio]

### ho...@chromium.org (2020-12-01)

That's interesting. I have not see any UaF from ChannelSplitter, but perhaps it's a problem in OfflineAudioContext. I don't think this is a regression.

adetaylor@ I don't have access to https://crbug.com/chromium/1148170. Could you cc me there?

### ad...@chromium.org (2020-12-01)

cc'd.

### ho...@chromium.org (2020-12-01)

Thank you!

### cl...@chromium.org (2020-12-01)

ClusterFuzz testcase 6278143293063168 appears to be flaky, updating reproducibility label.

### rt...@chromium.org (2020-12-01)

This looks very similar to https://crbug.com/chromium/1125635 which is also being handled in https://crbug.com/chromium/1150065

### ho...@chromium.org (2020-12-01)

FYI, this one is heavily involved with OfflineAudioWorkletThread.

### rt...@chromium.org (2020-12-01)

https://crbug.com/chromium/1125635 also has an offline audio worklet. I have not looked at the repro case though.

### [Deleted User] (2020-12-02)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ho...@chromium.org (2020-12-03)

[Comment Deleted]

### ho...@chromium.org (2020-12-03)

1. OfflineAudioDestinationHandler::DoOfflineRendering() is running the "while" loop with RenderIfNotSuspended() inside.
2. DeferredTaskHandler::ClearHandlersToBeDeleted() deletes an AudioHandler. 

The realtime context doesn't have this problem because it has a callback interval, instead of a while loop. I don't think ChannelSplitter has a special meaning. It's just an unfortunate victim in this repro case.

### ho...@chromium.org (2020-12-03)

[Empty comment from Monorail migration]

### ho...@chromium.org (2020-12-03)

rtoy@

PTAL at https://chromium-review.googlesource.com/c/chromium/src/+/2572397. Would like to hear your thoughts.

### rt...@chromium.org (2020-12-03)

Well, the bots are not happy.  I haven't tested, but I think this will also cause a deadlock.  From c#14, it seems very similar to https://crbug.com/chromium/1150065 (and https://crbug.com/chromium/1125635).  The offline context is rendering and handlers are deleted.  See 1150065 for a possible solution.  I have not yet tried it out.  I think it will work, but it might cause a memory leak.  Might be ok for the case where the iframe is going away, but not sure how it would work for the main frame.

### ho...@chromium.org (2020-12-04)

Yeah. Almost all tests are failing. It looks like a same issue with 1150065. But I won't mark this as a duplicate so we both can take a look and work together.

I also responded there so please take a look.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d866af575997f2b9c0476be5c58c09b7b7885c4e

commit d866af575997f2b9c0476be5c58c09b7b7885c4e
Author: Raymond Toy <rtoy@chromium.org>
Date: Mon Dec 07 17:55:30 2020

Clear handlers when the base context goes away.

Previously, in BaseAudioContext::Clear() we called
GetDeferredTaskHandler().ClearHandlersToBeDeleted().  But this was
also called in DeferredTaskHandler::ContextWillBeDestroyed(), which is
called in BaseAudioContext::~BaseAudioContext().

There's no need to call this twice while handling the audio context
going away.

Manually verified that the tests from https://crbug.com/chromium/1125635 and 1153658 work,
and the deadlock in https://crbug.com/chromium/1136571 is gone.

Bug: 1150065, 1153658
Change-Id: Iee15c31dc637bf82d66bfd79d5238b1f80813153
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2575418
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Cr-Commit-Position: refs/heads/master@{#834265}

[modify] https://crrev.com/d866af575997f2b9c0476be5c58c09b7b7885c4e/third_party/blink/renderer/modules/webaudio/base_audio_context.cc


### rt...@chromium.org (2020-12-08)

Fixed.  Seee 1150065 for more details.

### [Deleted User] (2020-12-09)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c28b3219b8d2c5923ec6b3e6fb8fd946f5c4785a

commit c28b3219b8d2c5923ec6b3e6fb8fd946f5c4785a
Author: Raymond Toy <rtoy@chromium.org>
Date: Wed Dec 09 19:07:38 2020

Clear handlers when the base context goes away.

Previously, in BaseAudioContext::Clear() we called
GetDeferredTaskHandler().ClearHandlersToBeDeleted().  But this was
also called in DeferredTaskHandler::ContextWillBeDestroyed(), which is
called in BaseAudioContext::~BaseAudioContext().

There's no need to call this twice while handling the audio context
going away.

Manually verified that the tests from https://crbug.com/chromium/1125635 and 1153658 work,
and the deadlock in https://crbug.com/chromium/1136571 is gone.

(cherry picked from commit d866af575997f2b9c0476be5c58c09b7b7885c4e)

Bug: 1150065, 1153658
Change-Id: Iee15c31dc637bf82d66bfd79d5238b1f80813153
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2575418
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#834265}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2581882
Reviewed-by: Raymond Toy <rtoy@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#748}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/c28b3219b8d2c5923ec6b3e6fb8fd946f5c4785a/third_party/blink/renderer/modules/webaudio/base_audio_context.cc


### [Deleted User] (2020-12-12)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-12-17)

Thanks for your persistence with this even after we closed https://crbug.com/chromium/1148170. The VRP panel has decided to award $5000 for this bug plus a $1000 bonus.

### ad...@google.com (2020-12-17)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6a22a0348cf9a37b2ac6eead23d3edc9a5fd23e2

commit 6a22a0348cf9a37b2ac6eead23d3edc9a5fd23e2
Author: Raymond Toy <rtoy@chromium.org>
Date: Tue Jan 05 18:29:02 2021

Clear handlers when the base context goes away.

Previously, in BaseAudioContext::Clear() we called
GetDeferredTaskHandler().ClearHandlersToBeDeleted().  But this was
also called in DeferredTaskHandler::ContextWillBeDestroyed(), which is
called in BaseAudioContext::~BaseAudioContext().

There's no need to call this twice while handling the audio context
going away.

Manually verified that the tests from https://crbug.com/chromium/1125635 and 1153658 work,
and the deadlock in https://crbug.com/chromium/1136571 is gone.

(cherry picked from commit d866af575997f2b9c0476be5c58c09b7b7885c4e)

Bug: 1150065, 1153658
Change-Id: Iee15c31dc637bf82d66bfd79d5238b1f80813153
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2575418
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#834265}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2610924
Reviewed-by: Raymond Toy <rtoy@chromium.org>
Cr-Commit-Position: refs/branch-heads/4280@{#2004}
Cr-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}

[modify] https://crrev.com/6a22a0348cf9a37b2ac6eead23d3edc9a5fd23e2/third_party/blink/renderer/modules/webaudio/base_audio_context.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/76fa0595af11a22baaeca911590fc50f29bf2c09

commit 76fa0595af11a22baaeca911590fc50f29bf2c09
Author: Achuith Bhandarkar <achuith@chromium.org>
Date: Mon Jan 11 17:53:16 2021

Clear handlers when the base context goes away.

Previously, in BaseAudioContext::Clear() we called
GetDeferredTaskHandler().ClearHandlersToBeDeleted().  But this was
also called in DeferredTaskHandler::ContextWillBeDestroyed(), which is
called in BaseAudioContext::~BaseAudioContext().

There's no need to call this twice while handling the audio context
going away.

Manually verified that the tests from https://crbug.com/chromium/1125635 and 1153658 work,
and the deadlock in https://crbug.com/chromium/1136571 is gone.

(cherry picked from commit d866af575997f2b9c0476be5c58c09b7b7885c4e)

Bug: 1150065, 1153658
Change-Id: Iee15c31dc637bf82d66bfd79d5238b1f80813153
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2575418
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#834265}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2617559
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1513}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/76fa0595af11a22baaeca911590fc50f29bf2c09/third_party/blink/renderer/modules/webaudio/base_audio_context.cc


### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-03-29)

@neklab2015 - we consider attachments/pocs included with reports to be an integral part of the report, so I've un-deleted them. Thanks!

### is...@google.com (2021-03-29)

This issue was migrated from crbug.com/chromium/1153658?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054024)*
