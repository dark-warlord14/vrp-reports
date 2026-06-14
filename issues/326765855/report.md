# UAF in v8_inspector::V8DebuggerAgentImpl::setBlackboxPatterns

| Field | Value |
|-------|-------|
| **Issue ID** | [326765855](https://issues.chromium.org/issues/326765855) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools |
| **Platforms** | Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | sz...@google.com |
| **Created** | 2024-02-26 |
| **Bounty** | $2,000.00 |

## Description

tested os:
ubuntu 22.04
tested chrome version:
stable & dev

repro steps:
/chrome --disable-gpu --auto-open-devtools-for-tabs   --disable-in-process-stack-traces --incognito --user-data-dir=/tmp/xx1 --js-flags=--expose-gc  http://localhost:8880/crash.html http://localhost:8880/crash.html  http://localhost:8880/crash.html http://localhost:8880/crash.html  http://localhost:8880/crash.html http://localhost:8880/crash.html  http://localhost:8880/crash.html http://localhost:8880/crash.html http://localhost:8880/crash.html http://localhost:8880/crash.html http://localhost:8880/crash.html http://localhost:8880/crash.html http://localhost:8880/crash.html
UAF will repro after several or dozens of refreshes. If it doesn't repro, try opening a few more tabs.

==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x514000141578 at pc 0x5561533891f4 bp 0x7f2ded449d10 sp 0x7f2ded449d08
READ of size 8 at 0x514000141578 thread T315 (DedicatedWorker)
    #0 0x5561533891f3 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:276:29
    #1 0x5561533891f3 in operator= ./../../third_party/libc++/src/include/__memory/unique_ptr.h:220:5
    #2 0x5561533891f3 in v8_inspector::V8DebuggerAgentImpl::setBlackboxPattern(v8_inspector::String16 const&) ./../../v8/src/inspector/v8-debugger-agent-impl.cc:1698:21
    #3 0x55615339fc39 in v8_inspector::V8DebuggerAgentImpl::setBlackboxPatterns(std::__Cr::unique_ptr<std::__Cr::vector<v8_inspector::String16, std::__Cr::allocator<v8_inspector::String16>>, std::__Cr::default_delete<std::__Cr::vector<v8_inspector::String16, std::__Cr::allocator<v8_inspector::String16>>>>) ./../../v8/src/inspector/v8-debugger-agent-impl.cc:1685:23
    #4 0x5561532e7d3b in v8_inspector::protocol::Debugger::DomainDispatcherImpl::setBlackboxPatterns(v8_crdtp::Dispatchable const&) ./gen/v8/src/inspector/protocol/Debugger.cpp:1294:44
    #5 0x5561534646ca in operator() ./../../third_party/libc++/src/include/__functional/function.h:714:12
    #6 0x5561534646ca in operator() ./../../third_party/libc++/src/include/__functional/function.h:981:10
    #7 0x5561534646ca in v8_crdtp::UberDispatcher::DispatchResult::Run() ./../../v8/third_party/inspector_protocol/crdtp/dispatch.cc:509:3
    #8 0x5561533fe83f in v8_inspector::V8InspectorSessionImpl::dispatchProtocolMessage(v8_inspector::StringView) ./../../v8/src/inspector/v8-inspector-session-impl.cc:395:39
    #9 0x55616a9f87b8 in blink::DevToolsSession::DispatchProtocolCommandImpl(int, WTF::String const&, base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) ./../../third_party/blink/renderer/core/inspector/devtools_session.cc:262:18
    #10 0x55616aa01e37 in Invoke<void (blink::DevToolsSession::*)(int, const WTF::String &, base::span<const unsigned char, 18446744073709551615UL, const unsigned char *>), blink::DevToolsSession *const &, int, WTF::String, WTF::Vector<unsigned char, 0U, WTF::PartitionAllocator> > ./../../base/functional/bind_internal.h:713:12
    #11 0x55616aa01e37 in MakeItSo<void (blink::DevToolsSession::*)(int, const WTF::String &, base::span<const unsigned char, 18446744073709551615UL, const unsigned char *>), std::__Cr::tuple<blink::internal::BasicUnwrappingCrossThreadHandle<blink::DevToolsSession, blink::internal::WeakCrossThreadHandleWeaknessPolicy>, int, WTF::String, WTF::Vector<unsigned char, 0U, WTF::PartitionAllocator> > > ./../../base/functional/bind_internal.h:892:5
    #12 0x55616aa01e37 in RunImpl<void (blink::DevToolsSession::*)(int, const WTF::String &, base::span<const unsigned char, 18446744073709551615UL, const unsigned char *>), std::__Cr::tuple<blink::internal::BasicUnwrappingCrossThreadHandle<blink::DevToolsSession, blink::internal::WeakCrossThreadHandleWeaknessPolicy>, int, WTF::String, WTF::Vector<unsigned char, 0U, WTF::PartitionAllocator> >, 0UL, 1UL, 2UL, 3UL> ./../../base/functional/bind_internal.h:1005:14
    #13 0x55616aa01e37 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::DevToolsSession::*)(int, WTF::String const&, base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>)>, base::internal::BindState<true, true, false, void (blink::DevToolsSession::*)(int, WTF::String const&, base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>), blink::internal::BasicUnwrappingCrossThreadHandle<blink::DevToolsSession, blink::internal::WeakCrossThreadHandleWeaknessPolicy>, int, WTF::String, WTF::Vector<unsigned char, 0u, WTF::PartitionAllocator>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:918:12
    #14 0x55616a6cf18f in Run ./../../base/functional/callback.h:156:12
    #15 0x55616a6cf18f in Run ./../../third_party/blink/renderer/platform/wtf/functional.h:341:33
    #16 0x55616a6cf18f in blink::InspectorTaskRunner::PerformSingleInterruptingTaskDontWait() ./../../third_party/blink/renderer/core/inspector/inspector_task_runner.cc:103:21
    #17 0x55616a6d0bf4 in Invoke<void (blink::InspectorTaskRunner::*)(), scoped_refptr<blink::InspectorTaskRunner> > ./../../base/functional/bind_internal.h:713:12
    #18 0x55616a6d0bf4 in MakeItSo<void (blink::InspectorTaskRunner::*)(), std::__Cr::tuple<scoped_refptr<blink::InspectorTaskRunner> > > ./../../base/functional/bind_internal.h:868:12
    #19 0x55616a6d0bf4 in RunImpl<void (blink::InspectorTaskRunner::*)(), std::__Cr::tuple<scoped_refptr<blink::InspectorTaskRunner> >, 0UL> ./../../base/functional/bind_internal.h:1005:14
    #20 0x55616a6d0bf4 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::InspectorTaskRunner::*)()>, base::internal::BindState<true, true, false, void (blink::InspectorTaskRunner::*)(), scoped_refptr<blink::InspectorTaskRunner>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:918:12
    #21 0x55615d5bf444 in Run ./../../base/functional/callback.h:156:12
    #22 0x55615d5bf444 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:202:34
    #23 0x55615d61e60f in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:11)> ./../../base/task/common/task_annotator.h:89:5
    #24 0x55615d61e60f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #25 0x55615d61d609 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:41
    #26 0x55615d61f3ca in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #27 0x55615d4bb12c in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #28 0x55615d62020e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:638:12
    #29 0x55615d5546df in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #30 0x5561745e4693 in content::(anonymous namespace)::NestedMessageLoopRunnerImpl::Run() ./../../content/child/blink_platform_impl.cc:88:14
    #31 0x55616bff2285 in blink::WorkerThread::PauseOrFreezeOnWorkerThread(blink::mojom::FrameLifecycleState, bool) ./../../third_party/blink/renderer/core/workers/worker_thread.cc:917:20
    #32 0x55616bfed8e3 in blink::WorkerThread::PauseOrFreeze(blink::mojom::FrameLifecycleState, bool) ./../../third_party/blink/renderer/core/workers/worker_thread.cc:857:5
    #33 0x55616a9db71f in blink::WorkerThreadDebugger::runMessageLoopOnPause(int) ./../../third_party/blink/renderer/core/inspector/worker_thread_debugger.cc:182:11
    #34 0x55616bfe9e49 in blink::WorkerThread::InitializeOnWorkerThread(std::__Cr::unique_ptr<blink::GlobalScopeCreationParams, std::__Cr::default_delete<blink::GlobalScopeCreationParams>>, std::__Cr::optional<blink::WorkerBackingThreadStartupData> const&, std::__Cr::unique_ptr<blink::WorkerDevToolsParams, std::__Cr::default_delete<blink::WorkerDevToolsParams>>) ./../../third_party/blink/renderer/core/workers/worker_thread.cc:671:33
    #35 0x55616bff3031 in Invoke<void (blink::WorkerThread::*)(std::__Cr::unique_ptr<blink::GlobalScopeCreationParams, std::__Cr::default_delete<blink::GlobalScopeCreationParams> >, const std::__Cr::optional<blink::WorkerBackingThreadStartupData> &, std::__Cr::unique_ptr<blink::WorkerDevToolsParams, std::__Cr::default_delete<blink::WorkerDevToolsParams> >), blink::WorkerThread *, std::__Cr::unique_ptr<blink::GlobalScopeCreationParams, std::__Cr::default_delete<blink::GlobalScopeCreationParams> >, std::__Cr::optional<blink::WorkerBackingThreadStartupData>, std::__Cr::unique_ptr<blink::WorkerDevToolsParams, std::__Cr::default_delete<blink::WorkerDevToolsParams> > > ./../../base/functional/bind_internal.h:713:12
    #36 0x55616bff3031 in MakeItSo<void (blink::WorkerThread::*)(std::__Cr::unique_ptr<blink::GlobalScopeCreationParams, std::__Cr::default_delete<blink::GlobalScopeCreationParams> >, const std::__Cr::optional<blink::WorkerBackingThreadStartupData> &, std::__Cr::unique_ptr<blink::WorkerDevToolsParams, std::__Cr::default_delete<blink::WorkerDevToolsParams> >), std::__Cr::tuple<WTF::CrossThreadUnretainedWrapper<blink::WorkerThread>, std::__Cr::unique_ptr<blink::GlobalScopeCreationParams, std::__Cr::default_delete<blink::GlobalScopeCreationParams> >, std::__Cr::optional<blink::WorkerBackingThreadStartupData>, std::__Cr::unique_ptr<blink::WorkerDevToolsParams, std::__Cr::default_delete<blink::WorkerDevToolsParams> > > > ./../../base/functional/bind_internal.h:868:12
    #37 0x55616bff3031 in RunImpl<void (blink::WorkerThread::*)(std::__Cr::unique_ptr<blink::GlobalScopeCreationParams, std::__Cr::default_delete<blink::GlobalScopeCreationParams> >, const std::__Cr::optional<blink::WorkerBackingThreadStartupData> &, std::__Cr::unique_ptr<blink::WorkerDevToolsParams, std::__Cr::default_delete<blink::WorkerDevToolsParams> >), std::__Cr::tuple<WTF::CrossThreadUnretainedWrapper<blink::WorkerThread>, std::__Cr::unique_ptr<blink::GlobalScopeCreationParams, std::__Cr::default_delete<blink::GlobalScopeCreationParams> >, std::__Cr::optional<blink::WorkerBackingThreadStartupData>, std::__Cr::unique_ptr<blink::WorkerDevToolsParams, std::__Cr::default_delete<blink::WorkerDevToolsParams> > >, 0UL, 1UL, 2UL, 3UL> ./../../base/functional/bind_internal.h:1005:14
    #38 0x55616bff3031 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::WorkerThread::*)(std::__Cr::unique_ptr<blink::GlobalScopeCreationParams, std::__Cr::default_delete<blink::GlobalScopeCreationParams>>, std::__Cr::optional<blink::WorkerBackingThreadStartupData> const&, std::__Cr::unique_ptr<blink::WorkerDevToolsParams, std::__Cr::default_delete<blink::WorkerDevToolsParams>>)>, base::internal::BindState<true, true, false, void (blink::WorkerThread::*)(std::__Cr::unique_ptr<blink::GlobalScopeCreationParams, std::__Cr::default_delete<blink::GlobalScopeCreationParams>>, std::__Cr::optional<blink::WorkerBackingThreadStartupData> const&, std::__Cr::unique_ptr<blink::WorkerDevToolsParams, std::__Cr::default_delete<blink::WorkerDevToolsParams>>), WTF::CrossThreadUnretainedWrapper<blink::WorkerThread>, std::__Cr::unique_ptr<blink::GlobalScopeCreationParams, std::__Cr::default_delete<blink::GlobalScopeCreationParams>>, std::__Cr::optional<blink::WorkerBackingThreadStartupData>, std::__Cr::unique_ptr<blink::WorkerDevToolsParams, std::__Cr::default_delete<blink::WorkerDevToolsParams>>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:918:12
    #39 0x55615d5bf444 in Run ./../../base/functional/callback.h:156:12
    #40 0x55615d5bf444 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:202:34
    #41 0x55615d61e60f in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:11)> ./../../base/task/common/task_annotator.h:89:5
    #42 0x55615d61e60f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #43 0x55615d61d609 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:41
    #44 0x55615d61f3ca in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #45 0x55615d4bb12c in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #46 0x55615d6200ff in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:641:12
    #47 0x55615d5546df in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #48 0x556159e4ffdc in blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run() ./../../third_party/blink/renderer/platform/scheduler/worker/non_main_thread_impl.cc:182:14
    #49 0x55615d6ed2b7 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:103:13
    #50 0x55614bc93918 in asan_thread_start(void*) _asan_rtl_:28

0x514000141578 is located 312 bytes inside of 400-byte region [0x514000141440,0x5140001415d0)
freed by thread T315 (DedicatedWorker) here:
    #0 0x55614bcca0bd in operator delete(void*) _asan_rtl_:3
    #1 0x5561533fb4b4 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:68:5
    #2 0x5561533fb4b4 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:279:7
    #3 0x5561533fb4b4 in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:249:71
    #4 0x5561533fb4b4 in v8_inspector::V8InspectorSessionImpl::~V8InspectorSessionImpl() ./../../v8/src/inspector/v8-inspector-session-impl.cc:169:1
    #5 0x5561533fbbb3 in v8_inspector::V8InspectorSessionImpl::~V8InspectorSessionImpl() ./../../v8/src/inspector/v8-inspector-session-impl.cc:160:51
    #6 0x55616a9f6b7c in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:68:5
    #7 0x55616a9f6b7c in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:279:7
    #8 0x55616a9f6b7c in blink::DevToolsSession::Detach() ./../../third_party/blink/renderer/core/inspector/devtools_session.cc:215:15
    #9 0x55616aa025f2 in Invoke<void (blink::DevToolsSession::*)(), const cppgc::internal::BasicPersistent<blink::DevToolsSession, cppgc::internal::WeakPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy> &> ./../../base/functional/bind_internal.h:713:12
    #10 0x55616aa025f2 in MakeItSo<void (blink::DevToolsSession::*)(), std::__Cr::tuple<cppgc::internal::BasicPersistent<blink::DevToolsSession, cppgc::internal::WeakPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy> > > ./../../base/functional/bind_internal.h:892:5
    #11 0x55616aa025f2 in RunImpl<void (blink::DevToolsSession::*)(), std::__Cr::tuple<cppgc::internal::BasicPersistent<blink::DevToolsSession, cppgc::internal::WeakPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy> >, 0UL> ./../../base/functional/bind_internal.h:1005:14
    #12 0x55616aa025f2 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::DevToolsSession::*)()>, base::internal::BindState<true, true, false, void (blink::DevToolsSession::*)(), cppgc::internal::BasicPersistent<blink::DevToolsSession, cppgc::internal::WeakPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:918:12
    #13 0x55615ec511c2 in Run ./../../base/functional/callback.h:156:12
    #14 0x55615ec511c2 in mojo::InterfaceEndpointClient::NotifyError(std::__Cr::optional<mojo::DisconnectReason> const&) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:744:31
    #15 0x55615ec77646 in mojo::internal::MultiplexRouter::ProcessNotifyErrorTask(mojo::internal::MultiplexRouter::Task*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:1010:13
    #16 0x55615ec6eb04 in mojo::internal::MultiplexRouter::ProcessTasks(mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:923:15
    #17 0x55615ec78a48 in mojo::internal::MultiplexRouter::LockAndCallProcessTasks() ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:1124:3
    #18 0x55615ec7a0b4 in Invoke<void (mojo::internal::MultiplexRouter::*)(), scoped_refptr<mojo::internal::MultiplexRouter> > ./../../base/functional/bind_internal.h:713:12
    #19 0x55615ec7a0b4 in MakeItSo<void (mojo::internal::MultiplexRouter::*)(), std::__Cr::tuple<scoped_refptr<mojo::internal::MultiplexRouter> > > ./../../base/functional/bind_internal.h:868:12
    #20 0x55615ec7a0b4 in RunImpl<void (mojo::internal::MultiplexRouter::*)(), std::__Cr::tuple<scoped_refptr<mojo::internal::MultiplexRouter> >, 0UL> ./../../base/functional/bind_internal.h:1005:14
    #21 0x55615ec7a0b4 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::internal::MultiplexRouter::*)()>, base::internal::BindState<true, true, false, void (mojo::internal::MultiplexRouter::*)(), scoped_refptr<mojo::internal::MultiplexRouter>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:918:12
    #22 0x55615d5bf444 in Run ./../../base/functional/callback.h:156:12
    #23 0x55615d5bf444 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:202:34
    #24 0x55615d61e60f in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:11)> ./../../base/task/common/task_annotator.h:89:5
    #25 0x55615d61e60f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #26 0x55615d61d609 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:41
    #27 0x55615d61f3ca in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #28 0x55615d4bb12c in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #29 0x55615d62020e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:638:12
    #30 0x55615d5546df in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #31 0x5561745e4693 in content::(anonymous namespace)::NestedMessageLoopRunnerImpl::Run() ./../../content/child/blink_platform_impl.cc:88:14
    #32 0x55616bff2285 in blink::WorkerThread::PauseOrFreezeOnWorkerThread(blink::mojom::FrameLifecycleState, bool) ./../../third_party/blink/renderer/core/workers/worker_thread.cc:917:20
    #33 0x556151510211 in v8::internal::Isolate::InvokeApiInterruptCallbacks() ./../../v8/src/execution/isolate.cc:1739:5
    #34 0x556151570b8c in v8::internal::StackGuard::HandleInterrupts(v8::internal::StackGuard::InterruptLevel) ./../../v8/src/execution/stack-guard.cc:371:15
    #35 0x5561524e238f in __RT_impl_Runtime_StackGuard ./../../v8/src/runtime/runtime-internal.cc:354:34
    #36 0x5561524e238f in v8::internal::Runtime_StackGuard(int, unsigned long*, v8::internal::Isolate*) ./../../v8/src/runtime/runtime-internal.cc:343:1
    #37 0x5561549a8df5 in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit setup-isolate-deserialize.cc:0:0
    #38 0x55615490fdf9 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc:0:0
    #39 0x55615490d7db in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc:0:0
    #40 0x55615490d506 in Builtins_JSEntry setup-isolate-deserialize.cc:0:0
    #41 0x5561514cf562 in Call ./../../v8/src/execution/simulator.h:178:12
    #42 0x5561514cf562 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:418:22
    #43 0x5561514d2b9d in v8::internal::(anonymous namespace)::InvokeWithTryCatch(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:475:18
    #44 0x5561514d2928 in v8::internal::Execution::TryCallScript(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::FixedArray>) ./../../v8/src/execution/execution.cc:551:10
    #45 0x5561519fd0c1 in v8::internal::Genesis::CompileExtension(v8::internal::Isolate*, v8::Extension*) ./../../v8/src/init/bootstrapper.cc:4975:11

previously allocated by thread T315 (DedicatedWorker) here:
    #0 0x55614bcc985d in operator new(unsigned long) _asan_rtl_:3
    #1 0x5561533fa206 in v8_inspector::V8InspectorSessionImpl::V8InspectorSessionImpl(v8_inspector::V8InspectorImpl*, int, int, v8_inspector::V8Inspector::Channel*, v8_inspector::StringView, v8_inspector::V8Inspector::ClientTrustLevel, std::__Cr::shared_ptr<v8_inspector::V8DebuggerBarrier>) ./../../v8/src/inspector/v8-inspector-session-impl.cc:129:25
    #2 0x5561533f99b6 in v8_inspector::V8InspectorSessionImpl::create(v8_inspector::V8InspectorImpl*, int, int, v8_inspector::V8Inspector::Channel*, v8_inspector::StringView, v8_inspector::V8Inspector::ClientTrustLevel, std::__Cr::shared_ptr<v8_inspector::V8DebuggerBarrier>) ./../../v8/src/inspector/v8-inspector-session-impl.cc:98:54
    #3 0x5561533e7cd8 in v8_inspector::V8InspectorImpl::connect(int, v8_inspector::V8Inspector::Channel*, v8_inspector::StringView, v8_inspector::V8Inspector::ClientTrustLevel, v8_inspector::V8Inspector::SessionPauseState) ./../../v8/src/inspector/v8-inspector-impl.cc:166:7
    #4 0x55616a9f7877 in blink::DevToolsSession::ConnectToV8(v8_inspector::V8Inspector*, int) ./../../third_party/blink/renderer/core/inspector/devtools_session.cc:181:28
    #5 0x55616a9dea02 in blink::WorkerInspectorController::AttachSession(blink::DevToolsSession*, bool) ./../../third_party/blink/renderer/core/inspector/worker_inspector_controller.cc:118:12
    #6 0x55616a9f55bb in blink::DevToolsSession::DevToolsSession(blink::DevToolsAgent*, mojo::PendingAssociatedRemote<blink::mojom::blink::DevToolsSessionHost>, mojo::PendingAssociatedReceiver<blink::mojom::blink::DevToolsSession>, mojo::PendingReceiver<blink::mojom::blink::DevToolsSession>, mojo::StructPtr<blink::mojom::blink::DevToolsSessionState>, bool, bool, WTF::String const&, bool, scoped_refptr<base::SequencedTaskRunner>) ./../../third_party/blink/renderer/core/inspector/devtools_session.cc:166:20
    #7 0x55616a9f2d66 in blink::DevToolsSession* cppgc::MakeGarbageCollectedTrait<blink::DevToolsSession>::Call<blink::DevToolsAgent*, mojo::PendingAssociatedRemote<blink::mojom::blink::DevToolsSessionHost>, mojo::PendingAssociatedReceiver<blink::mojom::blink::DevToolsSession>, mojo::PendingReceiver<blink::mojom::blink::DevToolsSession>, mojo::StructPtr<blink::mojom::blink::DevToolsSessionState>, bool&, bool&, WTF::String const&, bool&, scoped_refptr<base::SingleThreadTaskRunner>>(cppgc::AllocationHandle&, blink::DevToolsAgent*&&, mojo::PendingAssociatedRemote<blink::mojom::blink::DevToolsSessionHost>&&, mojo::PendingAssociatedReceiver<blink::mojom::blink::DevToolsSession>&&, mojo::PendingReceiver<blink::mojom::blink::DevToolsSession>&&, mojo::StructPtr<blink::mojom::blink::DevToolsSessionState>&&, bool&, bool&, WTF::String const&, bool&, scoped_refptr<base::SingleThreadTaskRunner>&&) ./../../v8/include/cppgc/allocation.h:242:32
    #8 0x55616a9e4a69 in MakeGarbageCollected<blink::DevToolsSession, blink::DevToolsAgent *, mojo::PendingAssociatedRemote<blink::mojom::blink::DevToolsSessionHost>, mojo::PendingAssociatedReceiver<blink::mojom::blink::DevToolsSession>, mojo::PendingReceiver<blink::mojom::blink::DevToolsSession>, mojo::StructPtr<blink::mojom::blink::DevToolsSessionState>, bool &, bool &, const WTF::String &, bool &, scoped_refptr<base::SingleThreadTaskRunner> > ./../../v8/include/cppgc/allocation.h:280:7
    #9 0x55616a9e4a69 in MakeGarbageCollected<blink::DevToolsSession, blink::DevToolsAgent *, mojo::PendingAssociatedRemote<blink::mojom::blink::DevToolsSessionHost>, mojo::PendingAssociatedReceiver<blink::mojom::blink::DevToolsSession>, mojo::PendingReceiver<blink::mojom::blink::DevToolsSession>, mojo::StructPtr<blink::mojom::blink::DevToolsSessionState>, bool &, bool &, const WTF::String &, bool &, scoped_refptr<base::SingleThreadTaskRunner> > ./../../third_party/blink/renderer/platform/heap/garbage_collected.h:37:10
    #10 0x55616a9e4a69 in blink::DevToolsAgent::AttachDevToolsSessionImpl(mojo::PendingAssociatedRemote<blink::mojom::blink::DevToolsSessionHost>, mojo::PendingAssociatedReceiver<blink::mojom::blink::DevToolsSession>, mojo::PendingReceiver<blink::mojom::blink::DevToolsSession>, mojo::StructPtr<blink::mojom::blink::DevToolsSessionState>, bool, bool, WTF::String const&, bool) ./../../third_party/blink/renderer/core/inspector/devtools_agent.cc:240:30
    #11 0x55616a9ee390 in void base::internal::FunctorTraits<void (blink::DevToolsAgent::*)(mojo::PendingAssociatedRemote<blink::mojom::blink::DevToolsSessionHost>, mojo::PendingAssociatedReceiver<blink::mojom::blink::DevToolsSession>, mojo::PendingReceiver<blink::mojom::blink::DevToolsSession>, mojo::StructPtr<blink::mojom::blink::DevToolsSessionState>, bool, bool, WTF::String const&, bool)>::Invoke<void (blink::DevToolsAgent::*)(mojo::PendingAssociatedRemote<blink::mojom::blink::DevToolsSessionHost>, mojo::PendingAssociatedReceiver<blink::mojom::blink::DevToolsSession>, mojo::PendingReceiver<blink::mojom::blink::DevToolsSession>, mojo::StructPtr<blink::mojom::blink::DevToolsSessionState>, bool, bool, WTF::String const&, bool), blink::DevToolsAgent* const&, mojo::PendingAssociatedRemote<blink::mojom::blink::DevToolsSessionHost>, mojo::PendingAssociatedReceiver<blink::mojom::blink::DevToolsSession>, mojo::PendingReceiver<blink::mojom::blink::DevToolsSession>, mojo::StructPtr<blink::mojom::blink::DevToolsSessionState>, bool, bool, WTF::String, bool>(void (blink::DevToolsAgent::*)(mojo::PendingAssociatedRemote<blink::mojom::blink::DevToolsSessionHost>, mojo::PendingAssociatedReceiver<blink::mojom::blink::DevToolsSession>, mojo::PendingReceiver<blink::mojom::blink::DevToolsSession>, mojo::StructPtr<blink::mojom::blink::DevToolsSessionState>, bool, bool, WTF::String const&, bool), blink::DevToolsAgent* const&, mojo::PendingAssociatedRemote<blink::mojom::blink::DevToolsSessionHost>&&, mojo::PendingAssociatedReceiver<blink::mojom::blink::DevToolsSession>&&, mojo::PendingReceiver<blink::mojom::blink::DevToolsSession>&&, mojo::StructPtr<blink::mojom::blink::DevToolsSessionState>&&, bool&&, bool&&, WTF::String&&, bool&&) ./../../base/functional/bind_internal.h:713:12
    #12 0x55616a9ee0b9 in MakeItSo<void (blink::DevToolsAgent::*)(mojo::PendingAssociatedRemote<blink::mojom::blink::DevToolsSessionHost>, mojo::PendingAssociatedReceiver<blink::mojom::blink::DevToolsSession>, mojo::PendingReceiver<blink::mojom::blink::DevToolsSession>, mojo::StructPtr<blink::mojom::blink::DevToolsSessionState>, bool, bool, const WTF::String &, bool), std::__Cr::tuple<blink::internal::BasicUnwrappingCrossThreadHandle<blink::DevToolsAgent, blink::internal::WeakCrossThreadHandleWeaknessPolicy>, mojo::PendingAssociatedRemote<blink::mojom::blink::DevToolsSessionHost>, mojo::PendingAssociatedReceiver<blink::mojom::blink::DevToolsSession>, mojo::PendingReceiver<blink::mojom::blink::DevToolsSession>, mojo::StructPtr<blink::mojom::blink::DevToolsSessionState>, bool, bool, WTF::String, bool> > ./../../base/functional/bind_internal.h:892:5
    #13 0x55616a9ee0b9 in RunImpl<void (blink::DevToolsAgent::*)(mojo::PendingAssociatedRemote<blink::mojom::blink::DevToolsSessionHost>, mojo::PendingAssociatedReceiver<blink::mojom::blink::DevToolsSession>, mojo::PendingReceiver<blink::mojom::blink::DevToolsSession>, mojo::StructPtr<blink::mojom::blink::DevToolsSessionState>, bool, bool, const WTF::String &, bool), std::__Cr::tuple<blink::internal::BasicUnwrappingCrossThreadHandle<blink::DevToolsAgent, blink::internal::WeakCrossThreadHandleWeaknessPolicy>, mojo::PendingAssociatedRemote<blink::mojom::blink::DevToolsSessionHost>, mojo::PendingAssociatedReceiver<blink::mojom::blink::DevToolsSession>, mojo::PendingReceiver<blink::mojom::blink::DevToolsSession>, mojo::StructPtr<blink::mojom::blink::DevToolsSessionState>, bool, bool, WTF::String, bool>, 0UL, 1UL, 2UL, 3UL, 4UL, 5UL, 6UL, 7UL, 8UL> ./../../base/functional/bind_internal.h:1005:14
    #14 0x55616a9ee0b9 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::DevToolsAgent::*)(mojo::PendingAssociatedRemote<blink::mojom::blink::DevToolsSessionHost>, mojo::PendingAssociatedReceiver<blink::mojom::blink::DevToolsSession>, mojo::PendingReceiver<blink::mojom::blink::DevToolsSession>, mojo::StructPtr<blink::mojom::blink::DevToolsSessionState>, bool, bool, WTF::String const&, bool)>, base::internal::BindState<true, true, false, void (blink::DevToolsAgent::*)(mojo::PendingAssociatedRemote<blink::mojom::blink::DevToolsSessionHost>, mojo::PendingAssociatedReceiver<blink::mojom::blink::DevToolsSession>, mojo::PendingReceiver<blink::mojom::blink::DevToolsSession>, mojo::StructPtr<blink::mojom::blink::DevToolsSessionState>, bool, bool, WTF::String const&, bool), blink::internal::BasicUnwrappingCrossThreadHandle<blink::DevToolsAgent, blink::internal::WeakCrossThreadHandleWeaknessPolicy>, mojo::PendingAssociatedRemote<blink::mojom::blink::DevToolsSessionHost>, mojo::PendingAssociatedReceiver<blink::mojom::blink::DevToolsSession>, mojo::PendingReceiver<blink::mojom::blink::DevToolsSession>, mojo::StructPtr<blink::mojom::blink::DevToolsSessionState>, bool, bool, WTF::String, bool>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:918:12
    #15 0x55616a6cf18f in Run ./../../base/functional/callback.h:156:12
    #16 0x55616a6cf18f in Run ./../../third_party/blink/renderer/platform/wtf/functional.h:341:33
    #17 0x55616a6cf18f in blink::InspectorTaskRunner::PerformSingleInterruptingTaskDontWait() ./../../third_party/blink/renderer/core/inspector/inspector_task_runner.cc:103:21
    #18 0x55616a6d0bf4 in Invoke<void (blink::InspectorTaskRunner::*)(), scoped_refptr<blink::InspectorTaskRunner> > ./../../base/functional/bind_internal.h:713:12
    #19 0x55616a6d0bf4 in MakeItSo<void (blink::InspectorTaskRunner::*)(), std::__Cr::tuple<scoped_refptr<blink::InspectorTaskRunner> > > ./../../base/functional/bind_internal.h:868:12
    #20 0x55616a6d0bf4 in RunImpl<void (blink::InspectorTaskRunner::*)(), std::__Cr::tuple<scoped_refptr<blink::InspectorTaskRunner> >, 0UL> ./../../base/functional/bind_internal.h:1005:14
    #21 0x55616a6d0bf4 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::InspectorTaskRunner::*)()>, base::internal::BindState<true, true, false, void (blink::InspectorTaskRunner::*)(), scoped_refptr<blink::InspectorTaskRunner>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:918:12
    #22 0x55615d5bf444 in Run ./../../base/functional/callback.h:156:12
    #23 0x55615d5bf444 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:202:34
    #24 0x55615d61e60f in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:11)> ./../../base/task/common/task_annotator.h:89:5
    #25 0x55615d61e60f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #26 0x55615d61d609 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:41
    #27 0x55615d61f3ca in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #28 0x55615d4bb12c in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #29 0x55615d62020e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:638:12
    #30 0x55615d5546df in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #31 0x5561745e4693 in content::(anonymous namespace)::NestedMessageLoopRunnerImpl::Run() ./../../content/child/blink_platform_impl.cc:88:14
    #32 0x55616bff2285 in blink::WorkerThread::PauseOrFreezeOnWorkerThread(blink::mojom::FrameLifecycleState, bool) ./../../third_party/blink/renderer/core/workers/worker_thread.cc:917:20
    #33 0x55616bfed8e3 in blink::WorkerThread::PauseOrFreeze(blink::mojom::FrameLifecycleState, bool) ./../../third_party/blink/renderer/core/workers/worker_thread.cc:857:5
    #34 0x55616a9db71f in blink::WorkerThreadDebugger::runMessageLoopOnPause(int) ./../../third_party/blink/renderer/core/inspector/worker_thread_debugger.cc:182:11
    #35 0x55616bfe9e49 in blink::WorkerThread::InitializeOnWorkerThread(std::__Cr::unique_ptr<blink::GlobalScopeCreationParams, std::__Cr::default_delete<blink::GlobalScopeCreationParams>>, std::__Cr::optional<blink::WorkerBackingThreadStartupData> const&, std::__Cr::unique_ptr<blink::WorkerDevToolsParams, std::__Cr::default_delete<blink::WorkerDevToolsParams>>) ./../../third_party/blink/renderer/core/workers/worker_thread.cc:671:33
    #36 0x55616bff3031 in Invoke<void (blink::WorkerThread::*)(std::__Cr::unique_ptr<blink::GlobalScopeCreationParams, std::__Cr::default_delete<blink::GlobalScopeCreationParams> >, const std::__Cr::optional<blink::WorkerBackingThreadStartupData> &, std::__Cr::unique_ptr<blink::WorkerDevToolsParams, std::__Cr::default_delete<blink::WorkerDevToolsParams> >), blink::WorkerThread *, std::__Cr::unique_ptr<blink::GlobalScopeCreationParams, std::__Cr::default_delete<blink::GlobalScopeCreationParams> >, std::__Cr::optional<blink::WorkerBackingThreadStartupData>, std::__Cr::unique_ptr<blink::WorkerDevToolsParams, std::__Cr::default_delete<blink::WorkerDevToolsParams> > > ./../../base/functional/bind_internal.h:713:12
    #37 0x55616bff3031 in MakeItSo<void (blink::WorkerThread::*)(std::__Cr::unique_ptr<blink::GlobalScopeCreationParams, std::__Cr::default_delete<blink::GlobalScopeCreationParams> >, const std::__Cr::optional<blink::WorkerBackingThreadStartupData> &, std::__Cr::unique_ptr<blink::WorkerDevToolsParams, std::__Cr::default_delete<blink::WorkerDevToolsParams> >), std::__Cr::tuple<WTF::CrossThreadUnretainedWrapper<blink::WorkerThread>, std::__Cr::unique_ptr<blink::GlobalScopeCreationParams, std::__Cr::default_delete<blink::GlobalScopeCreationParams> >, std::__Cr::optional<blink::WorkerBackingThreadStartupData>, std::__Cr::unique_ptr<blink::WorkerDevToolsParams, std::__Cr::default_delete<blink::WorkerDevToolsParams> > > > ./../../base/functional/bind_internal.h:868:12
    #38 0x55616bff3031 in RunImpl<void (blink::WorkerThread::*)(std::__Cr::unique_ptr<blink::GlobalScopeCreationParams, std::__Cr::default_delete<blink::GlobalScopeCreationParams> >, const std::__Cr::optional<blink::WorkerBackingThreadStartupData> &, std::__Cr::unique_ptr<blink::WorkerDevToolsParams, std::__Cr::default_delete<blink::WorkerDevToolsParams> >), std::__Cr::tuple<WTF::CrossThreadUnretainedWrapper<blink::WorkerThread>, std::__Cr::unique_ptr<blink::GlobalScopeCreationParams, std::__Cr::default_delete<blink::GlobalScopeCreationParams> >, std::__Cr::optional<blink::WorkerBackingThreadStartupData>, std::__Cr::unique_ptr<blink::WorkerDevToolsParams, std::__Cr::default_delete<blink::WorkerDevToolsParams> > >, 0UL, 1UL, 2UL, 3UL> ./../../base/functional/bind_internal.h:1005:14
    #39 0x55616bff3031 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::WorkerThread::*)(std::__Cr::unique_ptr<blink::GlobalScopeCreationParams, std::__Cr::default_delete<blink::GlobalScopeCreationParams>>, std::__Cr::optional<blink::WorkerBackingThreadStartupData> const&, std::__Cr::unique_ptr<blink::WorkerDevToolsParams, std::__Cr::default_delete<blink::WorkerDevToolsParams>>)>, base::internal::BindState<true, true, false, void (blink::WorkerThread::*)(std::__Cr::unique_ptr<blink::GlobalScopeCreationParams, std::__Cr::default_delete<blink::GlobalScopeCreationParams>>, std::__Cr::optional<blink::WorkerBackingThreadStartupData> const&, std::__Cr::unique_ptr<blink::WorkerDevToolsParams, std::__Cr::default_delete<blink::WorkerDevToolsParams>>), WTF::CrossThreadUnretainedWrapper<blink::WorkerThread>, std::__Cr::unique_ptr<blink::GlobalScopeCreationParams, std::__Cr::default_delete<blink::GlobalScopeCreationParams>>, std::__Cr::optional<blink::WorkerBackingThreadStartupData>, std::__Cr::unique_ptr<blink::WorkerDevToolsParams, std::__Cr::default_delete<blink::WorkerDevToolsParams>>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:918:12
    #40 0x55615d5bf444 in Run ./../../base/functional/callback.h:156:12
    #41 0x55615d5bf444 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:202:34
    #42 0x55615d61e60f in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:11)> ./../../base/task/common/task_annotator.h:89:5
    #43 0x55615d61e60f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #44 0x55615d61d609 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:41
    #45 0x55615d61f3ca in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0

Thread T315 (DedicatedWorker) created by T0 (chrome) here:
    #0 0x55614bc7b9f1 in ___interceptor_pthread_create _asan_rtl_:3
    #1 0x55615d6ec810 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) ./../../base/threading/platform_thread_posix.cc:148:13
    #2 0x55615d69fb98 in base::SimpleThread::StartAsync() ./../../base/threading/simple_thread.cc:55:13
    #3 0x556159e4d94a in blink::NonMainThread::CreateThread(blink::ThreadCreationParams const&) ./../../third_party/blink/renderer/platform/scheduler/worker/non_main_thread_impl.cc:40:11
    #4 0x55616bfc0bc9 in blink::WorkerBackingThread::WorkerBackingThread(blink::ThreadCreationParams const&) ./../../third_party/blink/renderer/core/workers/worker_backing_thread.cc:133:23
    #5 0x55616bfb1479 in make_unique<blink::WorkerBackingThread, blink::ThreadCreationParams &> ./../../third_party/libc++/src/include/__memory/unique_ptr.h:621:30
    #6 0x55616bfb1479 in blink::DedicatedWorkerThread::DedicatedWorkerThread(blink::ExecutionContext*, blink::DedicatedWorkerObjectProxy&, mojo::PendingRemote<blink::mojom::blink::DedicatedWorkerHost>, mojo::PendingRemote<blink::mojom::blink::BackForwardCacheControllerHost>) ./../../third_party/blink/renderer/core/workers/dedicated_worker_thread.cc:62:28
    #7 0x55616bf77ccf in make_unique<blink::DedicatedWorkerThread, blink::ExecutionContext *, blink::DedicatedWorkerObjectProxy &, mojo::PendingRemote<blink::mojom::blink::DedicatedWorkerHost>, mojo::PendingRemote<blink::mojom::blink::BackForwardCacheControllerHost> > ./../../third_party/libc++/src/include/__memory/unique_ptr.h:621:30
    #8 0x55616bf77ccf in blink::DedicatedWorkerMessagingProxy::CreateWorkerThread() ./../../third_party/blink/renderer/core/workers/dedicated_worker_messaging_proxy.cc:306:10
    #9 0x55616bfb8495 in blink::ThreadedMessagingProxyBase::InitializeWorkerThread(std::__Cr::unique_ptr<blink::GlobalScopeCreationParams, std::__Cr::default_delete<blink::GlobalScopeCreationParams>>, std::__Cr::optional<blink::WorkerBackingThreadStartupData> const&, std::__Cr::optional<base::TokenType<blink::DedicatedWorkerTokenTypeMarker> const> const&, std::__Cr::unique_ptr<blink::WorkerDevToolsParams, std::__Cr::default_delete<blink::WorkerDevToolsParams>>) ./../../third_party/blink/renderer/core/workers/threaded_messaging_proxy_base.cc:83:20
    #10 0x55616bf74664 in blink::DedicatedWorkerMessagingProxy::StartWorkerGlobalScope(std::__Cr::unique_ptr<blink::GlobalScopeCreationParams, std::__Cr::default_delete<blink::GlobalScopeCreationParams>>, std::__Cr::unique_ptr<blink::WorkerMainScriptLoadParameters, std::__Cr::default_delete<blink::WorkerMainScriptLoadParameters>>, blink::WorkerOptions const*, blink::KURL const&, blink::FetchClientSettingsObjectSnapshot const&, v8_inspector::V8StackTraceId const&, WTF::String const&, base::StrongAlias<blink::RejectCoepUnsafeNoneTag, bool>, base::TokenType<blink::DedicatedWorkerTokenTypeMarker> const&, mojo::PendingRemote<blink::mojom::blink::DedicatedWorkerHost>, mojo::PendingRemote<blink::mojom::blink::BackForwardCacheControllerHost>) ./../../third_party/blink/renderer/core/workers/dedicated_worker_messaging_proxy.cc:100:3
    #11 0x55616bfa85e0 in blink::DedicatedWorker::ContinueStart(blink::KURL const&, std::__Cr::unique_ptr<blink::WorkerMainScriptLoadParameters, std::__Cr::default_delete<blink::WorkerMainScriptLoadParameters>>, network::mojom::ReferrerPolicy, WTF::Vector<mojo::StructPtr<network::mojom::blink::ContentSecurityPolicy>, 0u, WTF::PartitionAllocator>, WTF::String const&, base::StrongAlias<blink::RejectCoepUnsafeNoneTag, bool>, mojo::PendingRemote<blink::mojom::blink::BackForwardCacheControllerHost>) ./../../third_party/blink/renderer/core/workers/dedicated_worker.cc:415:19
    #12 0x55616bfa925d in blink::DedicatedWorker::OnScriptLoadStarted(std::__Cr::unique_ptr<blink::WorkerMainScriptLoadParameters, std::__Cr::default_delete<blink::WorkerMainScriptLoadParameters>>, blink::CrossVariantMojoRemote<blink::mojom::BackForwardCacheControllerHostInterfaceBase>) ./../../third_party/blink/renderer/core/workers/dedicated_worker.cc:329:3
    #13 0x5561746ac8fa in content::DedicatedWorkerHostFactoryClient::OnScriptLoadStarted(mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::StructPtr<blink::mojom::WorkerMainScriptLoadParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, mojo::PendingReceiver<blink::mojom::SubresourceLoaderUpdater>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::PendingRemote<blink::mojom::BackForwardCacheControllerHost>) ./../../content/renderer/worker/dedicated_worker_host_factory_client.cc:206:12
    #14 0x556150216be2 in blink::mojom::DedicatedWorkerHostFactoryClientStubDispatch::Accept(blink::mojom::DedicatedWorkerHostFactoryClient*, mojo::Message*) ./gen/third_party/blink/public/mojom/worker/dedicated_worker_host_factory.mojom.cc:425:13
    #15 0x55615ec4b969 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1021:54
    #16 0x55615ec67b27 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #17 0x55615ec50a55 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:706:20
    #18 0x55615ec75134 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:1096:42
    #19 0x55615ec732b0 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:710:7
    #20 0x55615ec67b27 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #21 0x55615ec42ac0 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) ./../../mojo/public/cpp/bindings/lib/connector.cc:554:49
    #22 0x55615ec445aa in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:611:14
    #23 0x55615ec43fc9 in OnHandleReadyInternal ./../../mojo/public/cpp/bindings/lib/connector.cc:444:3
    #24 0x55615ec43fc9 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int) ./../../mojo/public/cpp/bindings/lib/connector.cc:410:3
    #25 0x55615ec45994 in Invoke<void (mojo::Connector::*)(const char *, unsigned int), mojo::Connector *, const char *, unsigned int> ./../../base/functional/bind_internal.h:713:12
    #26 0x55615ec45994 in MakeItSo<void (mojo::Connector::*const &)(const char *, unsigned int), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, unsigned int> ./../../base/functional/bind_internal.h:868:12
    #27 0x55615ec45994 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::*)(char const*, unsigned int)>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::RunImpl<void (mojo::Connector::* const&)(char const*, unsigned int), std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>> const&, 0ul, 1ul>(void (mojo::Connector::* const&)(char const*, unsigned int), std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>> const&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>, unsigned int&&) ./../../base/functional/bind_internal.h:1005:14
    #28 0x55615ec456e4 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::*)(char const*, unsigned int)>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int) ./../../base/functional/bind_internal.h:925:12
    #29 0x556150812183 in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & ./../../base/functional/callback.h:344:12
    #30 0x556150811f0f in Invoke<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind_internal.h:644:12
    #31 0x556150811f0f in MakeItSo<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind_internal.h:868:12
    #32 0x556150811f0f in RunImpl<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, 0UL> ./../../base/functional/bind_internal.h:1005:14
    #33 0x556150811f0f in base::internal::Invoker<base::internal::FunctorTraits<void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&)>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) ./../../base/functional/bind_internal.h:925:12
    #34 0x55615ecca68b in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & ./../../base/functional/callback.h:344:12
    #35 0x55615ecc9fad in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple_watcher.cc:278:14
    #36 0x55615eccb1f4 in Invoke<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), const base::WeakPtr<mojo::SimpleWatcher> &, int, unsigned int, mojo::HandleSignalsState> ./../../base/functional/bind_internal.h:713:12
    #37 0x55615eccb1f4 in MakeItSo<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> > ./../../base/functional/bind_internal.h:892:5
    #38 0x55615eccb1f4 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&)>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>) ./../../base/functional/bind_internal.h:1005:14
    #39 0x55615d5bf444 in Run ./../../base/functional/callback.h:156:12
    #40 0x55615d5bf444 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:202:34
    #41 0x55615d61e60f in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:11)> ./../../base/task/common/task_annotator.h:89:5
    #42 0x55615d61e60f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #43 0x55615d61d609 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:41
    #44 0x55615d61f3ca in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #45 0x55615d4bb12c in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #46 0x55615d6200ff in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:641:12
    #47 0x55615d5546df in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #48 0x55617462660a in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:367:16
    #49 0x55615acf5178 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:676:14
    #50 0x55615acf66bc in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:780:12
    #51 0x55615acf90ef in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1146:10
    #52 0x55615acf34d0 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:335:36
    #53 0x55615acf3b4b in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:348:10
    #54 0x55614bccbf28 in ChromeMain ./../../chrome/app/chrome_main.cc:192:12
    #55 0x7f323f029d8f in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16

SUMMARY: AddressSanitizer: heap-use-after-free (/home/pwn11/asan-linux-release/chrome+0x15bb11f3) (BuildId: 4e869c3b145cc235)
Shadow bytes around the buggy address:
  0x514000141280: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x514000141300: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x514000141380: 00 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa
  0x514000141400: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x514000141480: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x514000141500: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]
  0x514000141580: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa
  0x514000141600: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x514000141680: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x514000141700: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x514000141780: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa
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
    #0 0x55616a6ce5c0 in blink::InspectorTaskRunner::AppendTask(WTF::CrossThreadOnceFunction<void ()>) ./../../third_party/blink/renderer/core/inspector/inspector_task_runner.cc:40:30


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==1==END OF ADDITIONAL INFO
==1==ABORTING

## Attachments

- [crash.html](attachments/crash.html) (text/html, 1.3 KB)
- [asan.log](attachments/asan.log) (text/plain, 54.4 KB)
- [asan_log.txt](attachments/asan_log.txt) (text/plain, 51.7 KB)

## Timeline

### sa...@google.com (2024-02-29)

I haven't been able to reproduce this crash, neither locally nor on Clusterfuzz. What kind of build should this repro in? Locally I'm using:

```
is_debug = false
is_official_build = false
is_asan = true
symbol_level = 2

```

As this is crashing in the inspector, adding DevTools component. Also Cc'ing Benedikt, does this stacktrace mean anything to you or someone on your team?

### em...@gmail.com (2024-02-29)

My build flags are as follows, but I think your build flags should also be fine.
is_asan = true
is_debug = false
enable_nacl = false
treat_warnings_as_errors = false
is_component_build=false
dcheck_always_on = false
Or you can try the compiled asan version. I just tried the latest version and it will be reproduced soon.
Chromium 124.0.6330.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1266951.zip)

### pe...@google.com (2024-02-29)

Setting milestone because of s0/s1 severity.

### sz...@google.com (2024-03-04)

Andrey: I was wondering if this is a similar issue as [issue 40071155](https://issues.chromium.org/issues/40071155). From what I can tell from the stack traces it looks like the DevTools session is detached on a nested message loop directly via Mojo (due to a pipe disconnect).

The UAF happens during the "runIfWaitForDebugger" nested loop.

My current working assumption is that the worker is so short-lived that it's killed while we are still trying to set the worker up. But it's a bit hard since the second stack trace (where the session detaches) seems incomplete.

### sz...@google.com (2024-03-04)

Haven't been able to reproduce the crash yet.

### sa...@google.com (2024-03-11)

I've now managed to reproduce the crash locally with the flags from [comment #3](https://issues.chromium.org/issues/326765855#comment3) and on a commit from last week (<https://chromium.googlesource.com/chromium/src/+/182e9222e2342a4c43cefe26ee1e95cc51019c10>). In particular, I think `dcheck_always_on = false` is important, at least I wasn't able to reproduce without that earlier. Maybe it just affects the timing of things?

My Asan trace seems to match the one above, but I've also attached it. Simon, could you take another look? Feel free to reach out offline if you can't reproduce it.

### em...@gmail.com (2024-03-11)

I just tested it in other versions and it seems that POC is not easy to reproduce, but with the addition of GC(), it can be stably reproduced again. For example, modify the code in POC to:
Object.prototype.__defineGetter__("then", ()=>{
    GC(); GC(); GC(); GC(); GC(); GC(); 
    GC(); GC(); GC(); GC(); GC(); GC(); 
});
tested version:
Chromium 121.0.6163.0
Chromium 124.0.6340.0( gs://chromium-browser-asan/linux-release/asan-linux-release-asan-linux-release-1268379.zip)

### sz...@google.com (2024-03-13)

I'm still not able to reproduce on my cloudtop even with identical GN args and more calls to `GC()`.

From staring at the code it seems that the `--expose-gc` flag causes the corresponding `v8::Extension` to be compiled and run when the worker context is created. This breaks an invariant of the worker: No code must run between setting up the context (and InspectorTaskRunner) and starting the nested run-loop for `runIfWaitingForDebugger`:

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/workers/worker_thread.cc;l=642-673;drc=465365641ad68b8feb46a3d23111f221cd2ebc7c>

It looks like the Mojo pipe is torn down (and the DevTools session detached) while we actually bootstrap the v8::Context, but the worker\_thread itself is not yet terminated, so we can continue with the initialization work.

@Samuel: Could you add a `PostponeInterruptsScope postpone(isolate);` to `Genesis::CompileExtension` and see if it still reproduces? Just to confirm that this is indeed the issue.

`Genesis::CompileExtension`: <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/init/bootstrapper.cc;l=4932;drc=b639938e99fa6b5ffa9c859b18c72a251fd56942>

I'm not sure if this is how we generally want to fix this bug. Making extension compilation uninterruptible means developers won't be able to pause/debug via DevTools. This might be ok since v8::Extension is mostly used for Chromium developer tooling?

We could also expose the scope via V8 API, then worker\_thread.cc could install and use it directly, but there might be other code in blink that assumes that `Context::New` doesn't actually run any JS that could be interrupted.

### sa...@google.com (2024-03-13)

I tried this patch now:

```
diff --git a/src/init/bootstrapper.cc b/src/init/bootstrapper.cc
index fffda5a44af..f2fecc473f3 100644
--- a/src/init/bootstrapper.cc
+++ b/src/init/bootstrapper.cc
@@ -4930,6 +4930,7 @@ class TryCallScope {
 }  // namespace
 
 bool Genesis::CompileExtension(Isolate* isolate, v8::Extension* extension) {
+  PostponeInterruptsScope postpone(isolate);
   Factory* factory = isolate->factory();
   HandleScope scope(isolate);
   Handle<SharedFunctionInfo> function_info;

```

(With otherwise the same setting as in [comment #7](https://issues.chromium.org/issues/326765855#comment7)) and haven't been able to reproduce the bug since.

### em...@gmail.com (2024-03-13)

I haven't been able to reproduce it after patching.

### pe...@google.com (2024-03-28)

szuend: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-04-12)

szuend: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ad...@google.com (2024-04-19)

I discussed severity with szuend@ and, as this is a renderer process crash with the pre-requisite that the devtools have been opened, I think we can lower this to S2.

### ap...@google.com (2024-04-19)

Project: v8/v8
Branch: main

commit fd628a3450252d505bb017332c3cf09d26684668
Author: Simon Zünd <szuend@chromium.org>
Date:   Fri Apr 19 09:58:13 2024

    [genesis] Make v8::Extension compilation uninterruptible
    
    Blink generally assumes that v8::Context::New cannot be interrupted.
    Worker creation is especially sensitive if we interrupt and nuke
    a worker while we are still initializing said worker's context.
    
    Fixed: 326765855
    Change-Id: I931d72851d04906c511bd6d674f75a0afc2c58b0
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5467807
    Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    Commit-Queue: Simon Zünd <szuend@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#93457}

M       src/init/bootstrapper.cc

https://chromium-review.googlesource.com/5467807


### am...@google.com (2024-04-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-04-25)

Congratulations Cassidy Kim! The Chrome VRP Panel has decided to award you $2,000 for this report of a moderately mitigated memory corruption bug in the renderer process. Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2024-07-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/326765855)*
