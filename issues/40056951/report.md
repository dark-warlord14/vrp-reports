# SUMMARY: AddressSanitizer: heap-use-after-free Runtime.cpp:439 in v8_inspector::protocol::Runtime::Frontend::exceptionThrown

| Field | Value |
|-------|-------|
| **Issue ID** | [40056951](https://issues.chromium.org/issues/40056951) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2021-08-20 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4594.0 Safari/537.36

Steps to reproduce the problem:
#TestOn
Windows NT 10.0; Win64; x64
gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-906640.zip

#Reproduce
The poc cannot reproduce the problem stably, but the problem can be easily found by auditing the code, so if I can make a stable reproducible POC, I will provide.

What is the expected behavior?

What went wrong?

Type of crash
render tab

#Analysis
class V8InspectorImpl has an unordered_map that contains the raw pointer of V8InspectorSessionImpl, but the life cycle of V8InspectorSessionImpl is not handled correctly, causing UAF issue.
```
v8/src/inspector/v8-inspector-impl.h:179
// contextGroupId -> sessionId -> session
std::unordered_map<int, std::map<int, V8InspectorSessionImpl*>> m_sessions;

```

#Patch
Not yet

#asan
=================================================================
==4864==ERROR: AddressSanitizer: heap-use-after-free on address 0x101941a49e18 at pc 0x7ff8a8d13d4e bp 0x00007dd8ed40 sp 0x00007dd8ed88
READ of size 8 at 0x101941a49e18 thread T130
==4864==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ff8a8d13d4d in v8_inspector::protocol::Runtime::Frontend::exceptionThrown C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\v8\src\inspector\protocol\Runtime.cpp:439
    #1 0x7ff8a8d9c452 in v8_inspector::V8ConsoleMessage::reportToFrontend C:\b\s\w\ir\cache\builder\src\v8\src\inspector\v8-console-message.cc:338
    #2 0x7ff8a8ea41fc in v8_inspector::V8RuntimeAgentImpl::messageAdded C:\b\s\w\ir\cache\builder\src\v8\src\inspector\v8-runtime-agent-impl.cc:925
    #3 0x7ff8a8e5dd32 in v8_inspector::V8InspectorImpl::forEachSession C:\b\s\w\ir\cache\builder\src\v8\src\inspector\v8-inspector-impl.cc:445
    #4 0x7ff8a8da9900 in v8_inspector::V8ConsoleMessageStorage::addMessage C:\b\s\w\ir\cache\builder\src\v8\src\inspector\v8-console-message.cc:572
    #5 0x7ff8a8e5fd1e in v8_inspector::V8InspectorImpl::exceptionThrown C:\b\s\w\ir\cache\builder\src\v8\src\inspector\v8-inspector-impl.cc:278
    #6 0x7ff8b3502c0f in blink::ThreadDebugger::PromiseRejected C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\inspector\thread_debugger.cc:149
    #7 0x7ff8b6f3ade3 in blink::RejectedPromises::Message::Report C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\rejected_promises.cc:90
    #8 0x7ff8b6f38fe1 in blink::RejectedPromises::ProcessQueueNow C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\rejected_promises.cc:261
    #9 0x7ff8b6f41af5 in base::internal::Invoker<base::internal::BindState<void (blink::RejectedPromises::*)(WTF::Vector<std::__1::unique_ptr<blink::RejectedPromises::Message,std::__1::default_delete<blink::RejectedPromises::Message> >,0,WTF::PartitionAllocator>),scoped_refptr<blink::RejectedPromises>,WTF::Vector<std::__1::unique_ptr<blink::RejectedPromises::Message,std::__1::default_delete<blink::RejectedPromises::Message> >,0,WTF::PartitionAllocator> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:690
    #10 0x7ff8ab3267ba in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178
    #11 0x7ff8adcd4442 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:360
    #12 0x7ff8adcd3aa2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:260
    #13 0x7ff8adcad1a7 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:39
    #14 0x7ff8adcd593e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:467
    #15 0x7ff8ab2a8c93 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #16 0x7ff8a9bbcd9c in blink::scheduler::WorkerThread::SimpleThreadImpl::Run C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\scheduler\worker\worker_thread.cc:154
    #17 0x7ff8ab3efd0f in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:121
    #18 0x1400b2693 in __asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_thread.cpp:278
    #19 0x7ff902387973 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017973)
    #20 0x7ff902d0a2f0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005a2f0)

0x101941a49e18 is located 24 bytes inside of 128-byte region [0x101941a49e00,0x101941a49e80)
freed by thread T130 here:
    #0 0x1400a6edb in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ff8a8ea42e3 in v8_inspector::V8RuntimeAgentImpl::~V8RuntimeAgentImpl C:\b\s\w\ir\cache\builder\src\v8\src\inspector\v8-runtime-agent-impl.cc:245
    #2 0x7ff8a8e69454 in v8_inspector::V8InspectorSessionImpl::~V8InspectorSessionImpl C:\b\s\w\ir\cache\builder\src\v8\src\inspector\v8-inspector-session-impl.cc:156
    #3 0x7ff8a8e7271f in v8_inspector::V8InspectorSessionImpl::~V8InspectorSessionImpl C:\b\s\w\ir\cache\builder\src\v8\src\inspector\v8-inspector-session-impl.cc:147
    #4 0x7ff8b39b01e3 in blink::DevToolsSession::Detach C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\inspector\devtools_session.cc:187
    #5 0x7ff8ab6763bd in mojo::InterfaceEndpointClient::NotifyError C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:685
    #6 0x7ff8ab68bd00 in mojo::internal::MultiplexRouter::ProcessNotifyErrorTask C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1019
    #7 0x7ff8ab6863b6 in mojo::internal::MultiplexRouter::ProcessTasks C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:932
    #8 0x7ff8ab68c8f6 in mojo::internal::MultiplexRouter::LockAndCallProcessTasks C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1127
    #9 0x7ff8ab3267ba in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178
    #10 0x7ff8adcd4442 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:360
    #11 0x7ff8adcd3aa2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:260
    #12 0x7ff8adcad1a7 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:39
    #13 0x7ff8adcd5a55 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:464
    #14 0x7ff8ab2a8c93 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #15 0x7ff8ad5b45f5 in content::`anonymous namespace'::NestedMessageLoopRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\child\blink_platform_impl.cc:89
    #16 0x7ff8b62cca68 in blink::WorkerThread::PauseOrFreezeOnWorkerThread C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\worker_thread.cc:863
    #17 0x7ff8a7657021 in v8::internal::Isolate::InvokeApiInterruptCallbacks C:\b\s\w\ir\cache\builder\src\v8\src\execution\isolate.cc:1499
    #18 0x7ff8a76b5e99 in v8::internal::StackGuard::HandleInterrupts C:\b\s\w\ir\cache\builder\src\v8\src\execution\stack-guard.cc:325
    #19 0x7ff8a83d9469 in v8::internal::Runtime_StackGuard C:\b\s\w\ir\cache\builder\src\v8\src\runtime\runtime-internal.cc:303
    #20 0x7ec2000bdf1b  (<unknown module>)

previously allocated by thread T130 here:
    #0 0x1400a6fdb in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ff8bd88b28a in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
    #2 0x7ff8a8e67a50 in v8_inspector::V8InspectorSessionImpl::V8InspectorSessionImpl C:\b\s\w\ir\cache\builder\src\v8\src\inspector\v8-inspector-session-impl.cc:113
    #3 0x7ff8a8e67357 in v8_inspector::V8InspectorSessionImpl::create C:\b\s\w\ir\cache\builder\src\v8\src\inspector\v8-inspector-session-impl.cc:89
    #4 0x7ff8a8e5b498 in v8_inspector::V8InspectorImpl::connect C:\b\s\w\ir\cache\builder\src\v8\src\inspector\v8-inspector-impl.cc:160
    #5 0x7ff8b39b0df7 in blink::DevToolsSession::ConnectToV8 C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\inspector\devtools_session.cc:159
    #6 0x7ff8b8bd940d in blink::WorkerInspectorController::AttachSession C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\inspector\worker_inspector_controller.cc:118
    #7 0x7ff8b39ae852 in blink::DevToolsSession::DevToolsSession C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\inspector\devtools_session.cc:143
    #8 0x7ff8b3beeb27 in blink::MakeGarbageCollectedTrait<blink::DevToolsSession>::Call<blink::DevToolsAgent *,mojo::PendingAssociatedRemote<blink::mojom::blink::DevToolsSessionHost>,mojo::PendingAssociatedReceiver<blink::mojom::blink::DevToolsSession>,mojo::PendingReceiver<blink::mojom::blink::DevToolsSession>,mojo::StructPtr<blink::mojom::blink::DevToolsSessionState>,bool &,const WTF::String &,scoped_refptr<base::SingleThreadTaskRunner> > C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\heap\impl\heap.h:528
    #9 0x7ff8b3be26ce in blink::DevToolsAgent::AttachDevToolsSessionImpl C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\inspector\devtools_agent.cc:228
    #10 0x7ff8b3be947a in base::internal::Invoker<base::internal::BindState<void (blink::DevToolsAgent::*)(mojo::PendingAssociatedRemote<blink::mojom::blink::DevToolsSessionHost>, mojo::PendingAssociatedReceiver<blink::mojom::blink::DevToolsSession>, mojo::PendingReceiver<blink::mojom::blink::DevToolsSession>, mojo::StructPtr<blink::mojom::blink::DevToolsSessionState>, bool, const WTF::String &),blink::CrossThreadWeakPersistent<blink::DevToolsAgent>,mojo::PendingAssociatedRemote<blink::mojom::blink::DevToolsSessionHost>,mojo::PendingAssociatedReceiver<blink::mojom::blink::DevToolsSession>,mojo::PendingReceiver<blink::mojom::blink::DevToolsSession>,mojo::StructPtr<blink::mojom::blink::DevToolsSessionState>,bool,WTF::String>,void ()>::RunImpl<void (blink::DevToolsAgent::*)(mojo::PendingAssociatedRemote<blink::mojom::blink::DevToolsSessionHost>, mojo::PendingAssociatedReceiver<blink::mojom::blink::DevToolsSession>, mojo::PendingReceiver<blink::mojom::blink::DevToolsSession>, mojo::StructPtr<blink::mojom::blink::DevToolsSessionState>, bool, const WTF::String &),std::__1::tuple<blink::CrossThreadWeakPersistent<blink::DevToolsAgent>,mojo::PendingAssociatedRemote<blink::mojom::blink::DevToolsSessionHost>,mojo::PendingAssociatedReceiver<blink::mojom::blink::DevToolsSession>,mojo::PendingReceiver<blink::mojom::blink::DevToolsSession>,mojo::StructPtr<blink::mojom::blink::DevToolsSessionState>,bool,WTF::String>,0,1,2,3,4,5,6> C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:721
    #11 0x7ff8b29bddcb in blink::InspectorTaskRunner::PerformSingleInterruptingTaskDontWait C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\inspector\inspector_task_runner.cc:69
    #12 0x7ff8ab3267ba in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178
    #13 0x7ff8adcd4442 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:360
    #14 0x7ff8adcd3aa2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:260
    #15 0x7ff8adcad1a7 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:39
    #16 0x7ff8adcd593e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:467
    #17 0x7ff8ab2a8c93 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #18 0x7ff8a9bbcd9c in blink::scheduler::WorkerThread::SimpleThreadImpl::Run C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\scheduler\worker\worker_thread.cc:154
    #19 0x7ff8ab3efd0f in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:121
    #20 0x1400b2693 in __asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_thread.cpp:278
    #21 0x7ff902387973 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017973)
    #22 0x7ff902d0a2f0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005a2f0)

Thread T130 created by T46 here:
    #0 0x1400b30f2 in __asan_wrap_CreateThread C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:146
    #1 0x7ff8ab3ef0ee in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:185
    #2 0x7ff8ab36a950 in base::SimpleThread::StartAsync C:\b\s\w\ir\cache\builder\src\base\threading\simple_thread.cc:51
    #3 0x7ff8a9b50696 in blink::Thread::CreateThread C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\scheduler\common\thread.cc:86
    #4 0x7ff8b43f1eab in blink::WorkerBackingThread::WorkerBackingThread C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\worker_backing_thread.cc:60
    #5 0x7ff8bbb76c62 in blink::DedicatedWorkerThread::DedicatedWorkerThread C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\dedicated_worker_thread.cc:59
    #6 0x7ff8bb08c14a in blink::DedicatedWorkerMessagingProxy::CreateWorkerThread C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\dedicated_worker_messaging_proxy.cc:270
    #7 0x7ff8b98e0c83 in blink::ThreadedMessagingProxyBase::InitializeWorkerThread C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\threaded_messaging_proxy_base.cc:73
    #8 0x7ff8bb0899b9 in blink::DedicatedWorkerMessagingProxy::StartWorkerGlobalScope C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\dedicated_worker_messaging_proxy.cc:73
    #9 0x7ff8bbb7092b in blink::DedicatedWorker::ContinueStart C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\dedicated_worker.cc:397
    #10 0x7ff8bbb6fdfd in blink::DedicatedWorker::OnFinished C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\dedicated_worker.cc:378
    #11 0x7ff8b62dcf35 in blink::WorkerClassicScriptLoader::DidFinishLoading C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\worker_classic_script_loader.cc:282
    #12 0x7ff8b360ecb4 in blink::ThreadableLoader::NotifyFinished C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\threadable_loader.cc:357
    #13 0x7ff8a9bffa4e in blink::Resource::NotifyFinished C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\loader\fetch\resource.cc:240
    #14 0x7ff8a9c2eaa6 in blink::ResourceFetcher::HandleLoaderFinish C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\loader\fetch\resource_fetcher.cc:1878
    #15 0x7ff8a9c5aa94 in blink::ResourceLoader::DidFinishLoading C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\loader\fetch\resource_loader.cc:1242
    #16 0x7ff8a9c5a623 in blink::ResourceLoader::DidFinishLoadingBody C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\loader\fetch\resource_loader.cc:612
    #17 0x7ff8a9c86535 in blink::ResponseBodyLoader::OnStateChange C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\loader\fetch\response_body_loader.cc:632
    #18 0x7ff8a9c5abb9 in blink::ResourceLoader::DidFinishLoading C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\loader\fetch\resource_loader.cc:1223
    #19 0x7ff8a9cd3d11 in blink::WebURLLoader::Context::OnCompletedRequest C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\loader\fetch\url_loader\web_url_loader.cc:715
    #20 0x7ff8a9cc8deb in blink::WebResourceRequestSender::OnRequestComplete C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\loader\fetch\url_loader\web_resource_request_sender.cc:608
    #21 0x7ff8a9cad49e in blink::MojoURLLoaderClient::OnComplete C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\loader\fetch\url_loader\mojo_url_loader_client.cc:503
    #22 0x7ff8a3a2c640 in blink::ThrottlingURLLoader::OnComplete C:\b\s\w\ir\cache\builder\src\third_party\blink\common\loader\throttling_url_loader.cc:894
    #23 0x7ff8a290c64d in network::mojom::URLLoaderClientStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\services\network\public\mojom\url_loader.mojom.cc:1253
    #24 0x7ff8ab672609 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:898
    #25 0x7ff8ade1694e in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #26 0x7ff8ab675e94 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:655
    #27 0x7ff8ab68a30d in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1099
    #28 0x7ff8ab68909f in mojo::internal::MultiplexRouter::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:719
    #29 0x7ff8ade1694e in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #30 0x7ff8ab66d3ca in mojo::Connector::DispatchMessageW C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:546
    #31 0x7ff8ab66ec17 in mojo::Connector::ReadAllAvailableMessages C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:604
    #32 0x7ff8ab6beb96 in mojo::SimpleWatcher::OnHandleReady C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc:278
    #33 0x7ff8ab3267ba in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178
    #34 0x7ff8adccf753 in base::sequence_manager::internal::ThreadControllerImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_impl.cc:199
    #35 0x7ff8adcd22d3 in base::internal::Invoker<base::internal::BindState<void (base::sequence_manager::internal::ThreadControllerImpl::*)(base::sequence_manager::internal::ThreadControllerImpl::WorkType),base::WeakPtr<base::sequence_manager::internal::ThreadControllerImpl>,base::sequence_manager::internal::ThreadControllerImpl::WorkType>,void ()>::Run C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:703
    #36 0x7ff8ab3267ba in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178
    #37 0x7ff8adcd4442 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:360
    #38 0x7ff8adcd3aa2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:260
    #39 0x7ff8ab3ce406 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:220
    #40 0x7ff8ab3cc648 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #41 0x7ff8adcd593e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:467
    #42 0x7ff8ab2a8c93 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #43 0x7ff8ab36d5d9 in base::Thread::Run C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:341
    #44 0x7ff8ab36daf0 in base::Thread::ThreadMain C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:412
    #45 0x7ff8ab3efd0f in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:121
    #46 0x1400b2693 in __asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_thread.cpp:278
    #47 0x7ff902387973 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017973)
    #48 0x7ff902d0a2f0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005a2f0)

Thread T46 created by T0 here:
    #0 0x1400b30f2 in __asan_wrap_CreateThread C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:146
    #1 0x7ff8ab3ef0ee in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:185
    #2 0x7ff8ab36c7fd in base::Thread::StartWithOptions C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:216
    #3 0x7ff8a541334f in content::RenderProcessHostImpl::Init C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_process_host_impl.cc:1980
    #4 0x7ff8a53f654a in content::RenderFrameHostManager::InitRenderView C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:2952
    #5 0x7ff8a53ecfa1 in content::RenderFrameHostManager::ReinitializeMainRenderFrame C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:3188
    #6 0x7ff8a53ea773 in content::RenderFrameHostManager::GetFrameHostForNavigation C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:1142
    #7 0x7ff8a53e930a in content::RenderFrameHostManager::DidCreateNavigationRequest C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:897
    #8 0x7ff8a5163855 in content::FrameTreeNode::CreatedNavigationRequest C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\frame_tree_node.cc:536
    #9 0x7ff8a531f25d in content::Navigator::Navigate C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigator.cc:603
    #10 0x7ff8a52911f5 in content::NavigationControllerImpl::NavigateWithoutEntry C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigation_controller_impl.cc:3244
    #11 0x7ff8a5290330 in content::NavigationControllerImpl::LoadURLWithParams C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigation_controller_impl.cc:1091
    #12 0x7ff8ad4af9fa in `anonymous namespace'::LoadURLInContents C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser_navigator.cc:387
    #13 0x7ff8ad4acdbc in Navigate C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser_navigator.cc:659
    #14 0x7ff8b4a66ad1 in StartupBrowserCreatorImpl::OpenTabsInBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:316
    #15 0x7ff8b4a68ada in StartupBrowserCreatorImpl::RestoreOrCreateBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:592
    #16 0x7ff8b4a65ca1 in StartupBrowserCreatorImpl::DetermineURLsAndLaunch C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:430
    #17 0x7ff8b4a65348 in StartupBrowserCreatorImpl::Launch C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:220
    #18 0x7ff8b092410c in StartupBrowserCreator::LaunchBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:619
    #19 0x7ff8b0926fce in StartupBrowserCreator::ProcessLastOpenedProfiles C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1233
    #20 0x7ff8b0926171 in StartupBrowserCreator::LaunchBrowserForLastProfiles C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:710
    #21 0x7ff8b0929fe3 in StartupBrowserCreator::StartupLaunchAfterProtocolHandler C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1186
    #22 0x7ff8b09235da in StartupBrowserCreator::ProcessCmdLineImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1146
    #23 0x7ff8b0921b85 in StartupBrowserCreator::Start C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:555
    #24 0x7ff8ad9c6cb1 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1679
    #25 0x7ff8ad9c48b2 in ChromeBrowserMainParts::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1052
    #26 0x7ff8a48c6296 in content::BrowserMainLoop::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:937
    #27 0x7ff8a56c24db in content::StartupTaskRunner::RunAllTasksNow C:\b\s\w\ir\cache\builder\src\content\browser\startup_task_runner.cc:41
    #28 0x7ff8a48c579d in content::BrowserMainLoop::CreateStartupTasks C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:845
    #29 0x7ff8a48cd1d1 in content::BrowserMainRunnerImpl::Initialize C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:131
    #30 0x7ff8a48c1f6c in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:45
    #31 0x7ff8a713eb34 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:608
    #32 0x7ff8a71413d0 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1104
    #33 0x7ff8a71405b7 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:971
    #34 0x7ff8a713d03a in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:390
    #35 0x7ff8a713e07c in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:418
    #36 0x7ff8a0b4145a in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:168
    #37 0x140005b74 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169
    #38 0x140002be8 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382
    #39 0x1403f512f in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #40 0x7ff902387973 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017973)
    #41 0x7ff902d0a2f0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005a2f0)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\v8\src\inspector\protocol\Runtime.cpp:439 in v8_inspector::protocol::Runtime::Frontend::exceptionThrown
Shadow bytes around the buggy address:
  0x020469a49370: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x020469a49380: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x020469a49390: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x020469a493a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x020469a493b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x020469a493c0: fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd
  0x020469a493d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x020469a493e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x020469a493f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x020469a49400: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x020469a49410: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==4864==ABORTING

Did this work before? N/A 

Chrome version: 94.0.4594.0  Channel: canary
OS Version: 10.0

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 27.5 KB)

## Timeline

### [Deleted User] (2021-08-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-08-20)

m.cooolie@ thanks for the report. I understand that there's no reliable POC, but could you tell us more about how you came to make this UaF occur? Was it through UI interaction, or through some JS snippet, etc.? We'll need to know that in order to determine the bug severity.

It looks like you were somehow inspecting V8 using devtools, then arranged to detach the session, right?

It would also be really helpful if you can tell us whether you can reproduce the problem back on Chrome 92. That helps us determine if this impacts stable / is a regression /etc. Thanks!

### m....@gmail.com (2021-08-21)

I use puppeteer for automation, it seems that puppeteer automatically turns on the devtools function.

### pa...@chromium.org (2021-08-23)

V8 friends: Could you perhaps take a look and see if you can confirm? Thanks!

[Monorail components: Blink>JavaScript]

### is...@chromium.org (2021-08-24)

CCing DevTools folks for double checking.

### [Deleted User] (2021-08-25)

[Empty comment from Monorail migration]

### dr...@chromium.org (2021-08-30)

Security sheriff here - yangguo@, friendly ping? Can you confirm the bug?

### va...@chromium.org (2021-08-31)

passing to the stability sheriff, PTAL

### is...@chromium.org (2021-08-31)

CCing DevTools folks again.

### is...@chromium.org (2021-08-31)

Jaro, PTAL

[Monorail components: Platform>DevTools>JavaScript]

### is...@chromium.org (2021-08-31)

[Empty comment from Monorail migration]

### me...@chromium.org (2021-08-31)

[Empty comment from Monorail migration]

### ja...@chromium.org (2021-08-31)

[Empty comment from Monorail migration]

### ja...@chromium.org (2021-08-31)

[Empty comment from Monorail migration]

### si...@chromium.org (2021-08-31)

Could you please share your PoC? This would help us determine severity of this issue.

### m....@gmail.com (2021-08-31)

re https://crbug.com/chromium/1241860#c15
The poc can't reproduce the problem stably, I forgot to save it. I can try to run the fuzz again if necessary.

### si...@chromium.org (2021-09-01)

No worries, thanks.

### si...@chromium.org (2021-09-01)

jarin and I looked into this yesterday.

Our current working hypothesis is that this is a reentrancy problem caused by V8ConsoleMessage::reportToFrontend entering JavaScript to serialize exception data for the front-end, but before the message to the front-end is sent. When upon exiting JavaScript again, an interrupt triggers, a nested message loop is started. If the DevTools session is disconnected due to a message handled in this nested message loop, then upon returning to V8ConsoleMessage::reportToFrontend, the session is no longer valid.

To validate this hypothesis we need a repro, jarin is looking into this today. If the hypothesis is confirmed, there might be the possibility for a small fix using https://source.chromium.org/chromium/chromium/src/+/main:v8/src/execution/interrupts-scope.h;l=48?q=PostponeInterrupt&sq=&ss=chromium to suppress the interrupts during the critical parts of reportToFrontend.

For handling this bug we have the following options:
  - The code-path critical for this issue is guarded by RuntimeEnabledFeatures::ExceptionMetaDataForDevToolsEnabled(), so we can disable this feature for M93 and M94 if we can't come up with a back-mergeable fix in time.
  - For M95 we can change the implementation on the V8 side to use an EphemeronHashTable without the WeakMap JavaScript wrapper. We currently assume that this removes the possibility to enter JavaScript, but this still needs to be confirmed.

Next steps are possible after we have a repro.




### [Deleted User] (2021-09-01)

[Empty comment from Monorail migration]

### si...@chromium.org (2021-09-01)

To gauge severity, we need to understand more about how to trigger this situation: While jarin and are convinced this is a genuine UAF, we don't yet how easy or difficult it is to trigger this situation. The reporter seems to imply that they found the bug by fuzzing CDP commands. If it turns out that triggering the situation requires CDP access of some sort, this bug would not be as severe as otherwise.

### m....@gmail.com (2021-09-01)

To be precise, I use puppeteer to let the browser automatically load the page generated by the fuzzer, not fuzzing cdp commands.


### si...@chromium.org (2021-09-01)

Upping priority as extensions with CDP access may be able to create the situation described in this issue.

### ja...@chromium.org (2021-09-01)

re https://crbug.com/chromium/1241860#c16,

could you at least share code for the puppeteer driver? We are specifically curious about how the session to the page gets closed - is it just page.close()?

### m....@gmail.com (2021-09-01)

[Comment Deleted]

### ja...@chromium.org (2021-09-03)

Unfortunately, I have not been able to construct a repro from JavaScript/Chrome, but I have v8 cc-test that illustrates the problem well-enough and a one-line fix.

See https://chromium-review.googlesource.com/c/v8/v8/+/3140597 for a WIP test and fix.

As Sigurd already outlined in https://crbug.com/chromium/1241860#c18, the problem is that V8ConsoleMessage::reportToFrontend calls to WeakMap.prototype.get, which in turn can trigger stack-check/interrupt. The interrupt handler pumps the message loop, and we are convinced that one of the messages was debugger disconnect (see the second stack trace in the report above). If the debugger disconnects while constructing the message, reportToFrontend will send the message to a deallocated debugger session, causing the use-after-free.

There are several options of how to fix this:
1. Disable interrupts during the weak map lookup.
2. Re-do the lookup of the session by its session ID after we construct the message and abort if the session is not found.
3. Replace the weak map with something that cannot cause interrupts on lookup.

In the prototype CL (https://chromium-review.googlesource.com/c/v8/v8/+/3140597), we implement option (1) because this is the least intrusive fix.

### ja...@chromium.org (2021-09-03)

Benedikt, could you take it from here? (I am on vacation next week.) I am adding some more details to the CL.

### si...@chromium.org (2021-09-07)

Benedikt, if we don't have a fix ready, I recommend disabling the feature in an appropriate way for M93. As it's practically my last day, I can't handle this today.

### ad...@google.com (2021-09-07)

Security sheriff here.

I'm going to set this as Security_Severity-High. This is a browser process UaF. That would normally be Critical, but this is mitigated down to High based on the need for a CDP connection/debugger connection/similar. There's an argument to mitigate it lower, since if the user has granted such a debug connection anyway, arguably the debugger already has similar powers to a compromised browser process (!) but for now we'll err on the side of caution and rate this High.

From https://crbug.com/chromium/1241860#c18 I think this is believed to be present back to M93 (at least) so I'm marking as FoundIn-93, to trigger _consideration_ of merges when we have a fix.

### [Deleted User] (2021-09-07)

[Empty comment from Monorail migration]

### bm...@chromium.org (2021-09-08)

Sorry, only got to this part of my inbox today, after vacation and Perf marathon.

Philip, can you please take care of Jaro's work from https://crbug.com/chromium/1241860#c25 and land the CL?

### [Deleted User] (2021-09-08)

pfaffe: Uh oh! This issue still open and hasn't been updated in the last 19 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pf...@chromium.org (2021-09-09)

sigurds@ recommended disabling metadata collection and reporting by not creating a context for the metadata. Implementation is here: https://crrev.com/c/3149456

### gi...@appspot.gserviceaccount.com (2021-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c8abd833c7f03877ae9082afe91db5862558625f

commit c8abd833c7f03877ae9082afe91db5862558625f
Author: Philip Pfaffe <pfaffe@chromium.org>
Date: Thu Sep 09 13:49:36 2021

Disable DevTools issues tests

Bug: 1241860
Change-Id: I91d14cc3874c45f8a7bca81008fbfe42d19e760f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3150017
Commit-Queue: Philip Pfaffe <pfaffe@chromium.org>
Commit-Queue: Benedikt Meurer <bmeurer@chromium.org>
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
Cr-Commit-Position: refs/heads/main@{#919767}

[modify] https://crrev.com/c8abd833c7f03877ae9082afe91db5862558625f/third_party/blink/web_tests/TestExpectations


### gi...@appspot.gserviceaccount.com (2021-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/25d5e5081280115348a237add544adfa0f43bc02

commit 25d5e5081280115348a237add544adfa0f43bc02
Author: Philip Pfaffe <pfaffe@chromium.org>
Date: Thu Sep 09 09:07:22 2021

Disable exception metadata

Bug: chromium:1241860
Change-Id: Ieee7d5c67f1a42c0c9855148a7d497586d6c5555
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3149456
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
Commit-Queue: Philip Pfaffe <pfaffe@chromium.org>
Cr-Commit-Position: refs/heads/main@{#76753}

[modify] https://crrev.com/25d5e5081280115348a237add544adfa0f43bc02/src/inspector/v8-inspector-impl.cc
[modify] https://crrev.com/25d5e5081280115348a237add544adfa0f43bc02/test/inspector/inspector.status


### [Deleted User] (2021-09-10)

[Empty comment from Monorail migration]

### pf...@chromium.org (2021-09-13)

m.cooolie@, can you confirm whether the UAF is mitigated by the change above? It rolled into M96.

### m....@gmail.com (2021-09-13)

https://crbug.com/chromium/1241860#c25 wrote a test case for this problem,I will try to run fuzz to see if it can trigger again.

### ja...@chromium.org (2021-09-13)

Re https://crbug.com/chromium/1241860#c37: The https://crbug.com/chromium/1241860#c25 test case is a C++ v8 test. I believe that cannot be fuzzed?

### ja...@chromium.org (2021-09-13)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/2084e90955adeb597e731d0a18351a930cf9a96a

commit 2084e90955adeb597e731d0a18351a930cf9a96a
Author: Simon Zünd <szuend@chromium.org>
Date: Wed Sep 15 08:45:07 2021

Skip e2etest that is blocking the Chromium roll

The "link to issue from console" test relies on exception metadata,
which was reverted.

R=pfaffe@chromium.org

Bug: 1241860
Change-Id: Id124759c58bdab1f35b6ac67e42112b6e7b73195
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/3161981
Commit-Queue: Simon Zünd <szuend@chromium.org>
Commit-Queue: Philip Pfaffe <pfaffe@chromium.org>
Auto-Submit: Simon Zünd <szuend@chromium.org>
Reviewed-by: Philip Pfaffe <pfaffe@chromium.org>

[modify] https://crrev.com/2084e90955adeb597e731d0a18351a930cf9a96a/test/e2e/issues/issue-links_test.ts


### m....@gmail.com (2021-09-15)

https://crbug.com/chromium/1241860#c36 Not reproduce in 20 hours.

### gi...@appspot.gserviceaccount.com (2021-09-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fe81bbc71b9893a4333a92fc82026d90a3b6c5de

commit fe81bbc71b9893a4333a92fc82026d90a3b6c5de
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Sep 15 15:02:36 2021

Roll DevTools Frontend from 4064ed6e13c6 to 49c262f1ca3d (13 revisions)

https://chromium.googlesource.com/devtools/devtools-frontend.git/+log/4064ed6e13c6..49c262f1ca3d

2021-09-15 liviurau@chromium.org Make auto-roller account an owner of DEPS
2021-09-15 kprokopenko@chromium.org Use type-safe events for SplitWidget
2021-09-15 kprokopenko@chromium.org Use type-safe events for LayerDetailsView
2021-09-15 jacktfranklin@chromium.org Add mocha-fgrep flag to run_test_suite.js
2021-09-15 jacktfranklin@chromium.org Fix contrast on delete icon for watch expression
2021-09-15 devtools-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Update DevTools Chromium DEPS.
2021-09-15 kprokopenko@chromium.org Use type-safe events for CSSOverviewSidebarPanel
2021-09-15 devtools-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Update DevTools DEPS.
2021-09-15 kprokopenko@chromium.org Use type-safe events for PaintProfilerView
2021-09-15 kprokopenko@chromium.org Use type-safe events for Layers3DView
2021-09-15 szuend@chromium.org [e2e] Skip extension test that fails often on Mac
2021-09-15 kprokopenko@chromium.org Use type-safe events for InspectedPagePlaceholder
2021-09-15 szuend@chromium.org Skip e2etest that is blocking the Chromium roll

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/devtools-frontend-chromium
Please CC devtools-waterfall-sheriff-onduty@grotations.appspotmail.com on the revert to ensure that a human
is aware of the problem.

To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1228674,chromium:1235962,chromium:1241860,chromium:1249774
Tbr: devtools-waterfall-sheriff-onduty@grotations.appspotmail.com
Change-Id: I97494019285b4657cf8ff9b837969bb9b9964973
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3162800
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#921652}

[modify] https://crrev.com/fe81bbc71b9893a4333a92fc82026d90a3b6c5de/DEPS


### gi...@appspot.gserviceaccount.com (2021-09-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/7994004493df2c9a24372587312ef6c458c7ed2b

commit 7994004493df2c9a24372587312ef6c458c7ed2b
Author: Jaroslav Sevcik <jarin@chromium.org>
Date: Tue Sep 14 19:08:03 2021

[inspector] Use ephemeron table for exception metadata

EphemeronHashTable does not trigger interrupts when accessed
(as opposed to calling the WeakMapGet builtin), so it avoids
the use-after-free problem when reading exception metadata
triggers session disconnect while holding a reference
to the session.

Bug: chromium:1241860
Change-Id: I29264b04b8daf682e7c33a97faedf50e323d57c4
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3158326
Commit-Queue: Jaroslav Sevcik <jarin@chromium.org>
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
Cr-Commit-Position: refs/heads/main@{#76864}

[modify] https://crrev.com/7994004493df2c9a24372587312ef6c458c7ed2b/src/api/api.h
[modify] https://crrev.com/7994004493df2c9a24372587312ef6c458c7ed2b/src/debug/debug-interface.cc
[modify] https://crrev.com/7994004493df2c9a24372587312ef6c458c7ed2b/src/debug/debug-interface.h
[modify] https://crrev.com/7994004493df2c9a24372587312ef6c458c7ed2b/src/inspector/inspected-context.cc
[modify] https://crrev.com/7994004493df2c9a24372587312ef6c458c7ed2b/src/inspector/inspected-context.h
[modify] https://crrev.com/7994004493df2c9a24372587312ef6c458c7ed2b/src/inspector/v8-inspector-impl.cc
[modify] https://crrev.com/7994004493df2c9a24372587312ef6c458c7ed2b/src/inspector/v8-inspector-impl.h
[modify] https://crrev.com/7994004493df2c9a24372587312ef6c458c7ed2b/test/cctest/test-debug.cc
[modify] https://crrev.com/7994004493df2c9a24372587312ef6c458c7ed2b/test/cctest/test-inspector.cc
[modify] https://crrev.com/7994004493df2c9a24372587312ef6c458c7ed2b/test/inspector/inspector.status


### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-27)

jarin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ja...@chromium.org (2021-09-28)

[Empty comment from Monorail migration]

### ya...@google.com (2021-09-28)

We use a PostponeInterruptsScope elsewhere to avoid re-entrancy [0]. Is this something that we should use more widely in v8 inspector?

[0] https://source.chromium.org/chromium/chromium/src/+/main:v8/src/debug/debug.cc;l=2196;drc=11b217db3f388050e6db1a5c4e83d63ad02f16d2;bpv=1;bpt=1

### [Deleted User] (2021-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-28)

Requesting merge to stable M94 because latest trunk commit (921652) appears to be after stable branch point (911515).

Requesting merge to beta M95 because latest trunk commit (921652) appears to be after beta branch point (920003).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-28)

Merge review required: a commit with DEPS changes was detected.

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
Owners: benmason (Android), harrysouders (iOS), None (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-28)

Merge review required: a commit with DEPS changes was detected.

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

### am...@chromium.org (2021-10-01)

As this appears to be on Canary for about 16 days and I presume no stability issue have been tied to this fix, please go ahead and merge to the respective V8 branches for M94 and M95. Please complete these merges by EOD Tuesday so this fix can be in the scheduled M94 refresh next week. Thank you! 

### pb...@google.com (2021-10-05)

Your change has been approved for M95. Please go ahead and merge the CL to branch 4638 manually asap so that it would be part of this week’s Beta release.

### am...@google.com (2021-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-06)

Congratulations, the VRP Panel have decided to award you $5000 for this report. Thank you for this report! 

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-10-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/29be6884cb8ac974de67691e35951a827a4bb186

commit 29be6884cb8ac974de67691e35951a827a4bb186
Author: Jaroslav Sevcik <jarin@chromium.org>
Date: Tue Sep 14 19:08:03 2021

Merge: [inspector] Use ephemeron table for exception metadata

EphemeronHashTable does not trigger interrupts when accessed
(as opposed to calling the WeakMapGet builtin), so it avoids
the use-after-free problem when reading exception metadata
triggers session disconnect while holding a reference
to the session.

(cherry picked from commit 7994004493df2c9a24372587312ef6c458c7ed2b)

Bug: chromium:1241860
No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Change-Id: I29264b04b8daf682e7c33a97faedf50e323d57c4
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3218987
Reviewed-by: Yang Guo <yangguo@chromium.org>
Commit-Queue: Yang Guo <yangguo@chromium.org>
Cr-Commit-Position: refs/branch-heads/9.5@{#38}
Cr-Branched-From: 4a03d61accede9dd0e3e6dc0456ff5a0e3f792b4-refs/heads/9.5.172@{#1}
Cr-Branched-From: 9a607043cb3161f8ceae1583807bece595388108-refs/heads/main@{#76741}

[modify] https://crrev.com/29be6884cb8ac974de67691e35951a827a4bb186/src/inspector/v8-inspector-impl.cc
[modify] https://crrev.com/29be6884cb8ac974de67691e35951a827a4bb186/test/cctest/test-inspector.cc
[modify] https://crrev.com/29be6884cb8ac974de67691e35951a827a4bb186/src/inspector/v8-inspector-impl.h
[modify] https://crrev.com/29be6884cb8ac974de67691e35951a827a4bb186/src/api/api.h
[modify] https://crrev.com/29be6884cb8ac974de67691e35951a827a4bb186/test/cctest/test-debug.cc
[modify] https://crrev.com/29be6884cb8ac974de67691e35951a827a4bb186/src/inspector/inspected-context.cc
[modify] https://crrev.com/29be6884cb8ac974de67691e35951a827a4bb186/src/debug/debug-interface.h
[modify] https://crrev.com/29be6884cb8ac974de67691e35951a827a4bb186/src/debug/debug-interface.cc
[modify] https://crrev.com/29be6884cb8ac974de67691e35951a827a4bb186/src/inspector/inspected-context.h


### sr...@google.com (2021-10-12)

Droppiong M95 approved label 

### ja...@chromium.org (2021-10-13)

Amy, Prudhvikumar, could we *not* merge it into 94?

Here my reasons for not merging:
- The patch does not apply cleanly anymore.
- The patch is not small.
- The bug is not P0, it can only occur with devtools open - it cannot affect ordinary users.
- The bug does not compromise the browser process, only the renderer is affected.
- It would be very very hard to exploit because one has to control where interrupts happen.

What do you think?

### am...@chromium.org (2021-10-13)

Hi Jaroslav, thank you for this question as well as providing much sound reasoning. 
Generally a renderer RCE is still of sufficiently scariness/severity levels that would still want to press ahead with getting it backmerged to extended stable; however, given the data points about it not patching cleanly and concerns about having to create a 94-specific patch and it's size introducing potential stability issues or other complexities + high barrier to exploit and not having a reliable POC, I'm okay with not backmerging this to Extended Stable. 

removing the merge-approval for 94 to get this off any nag lists. 

### am...@chromium.org (2021-10-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-19)

[Empty comment from Monorail migration]

### rz...@google.com (2021-10-21)

Labelling as not applicable as the exception metadata fixed code isn't present on M90

### am...@google.com (2021-11-02)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d3001a648110af5b6816c53498f20e73b0532723

commit d3001a648110af5b6816c53498f20e73b0532723
Author: Simon Zünd <szuend@chromium.org>
Date: Mon Nov 22 12:05:43 2021

Re-enable 4 inspector-protocol tests

The tests were temporarily disabled due to a feature revert. After the
feature was re-implemented, the tests were forgotten to be re-enabled.

Bug: 1241860
Change-Id: I5c2cb7a0f73708f31c65b7726638114537bfc0d7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3295542
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Simon Zünd <szuend@chromium.org>
Cr-Commit-Position: refs/heads/main@{#944024}

[modify] https://crrev.com/d3001a648110af5b6816c53498f20e73b0532723/third_party/blink/web_tests/TestExpectations


### [Deleted User] (2022-01-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bm...@chromium.org (2022-04-20)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-04-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/20fac7a3bc05b0d5fd942443c3f3a6a411eeef4b

commit 20fac7a3bc05b0d5fd942443c3f3a6a411eeef4b
Author: Benedikt Meurer <bmeurer@chromium.org>
Date: Wed Apr 20 12:07:37 2022

[e2e] Re-enable issues-link test.

The back-end functionality was brought back, but the test was forgotten.

Bug: chromium:1241860
Change-Id: Iccbabcb6cadac4aac851d0e752362d617d797556
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/3596241
Commit-Queue: Benedikt Meurer <bmeurer@chromium.org>
Auto-Submit: Benedikt Meurer <bmeurer@chromium.org>
Reviewed-by: Mathias Bynens <mathias@chromium.org>
Commit-Queue: Mathias Bynens <mathias@chromium.org>

[modify] https://crrev.com/20fac7a3bc05b0d5fd942443c3f3a6a411eeef4b/test/e2e/issues/issue-links_test.ts


### gi...@appspot.gserviceaccount.com (2022-04-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5c69380bb74de237634211a133393fff9aa9caa0

commit 5c69380bb74de237634211a133393fff9aa9caa0
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Apr 20 18:36:13 2022

Roll DevTools Frontend from 4d8add54bfc8 to 8b58098c83bc (14 revisions)

https://chromium.googlesource.com/devtools/devtools-frontend.git/+log/4d8add54bfc8..8b58098c83bc

2022-04-20 andoli@chromium.org Restore Interactions lane in the Performance panel
2022-04-20 wolfi@chromium.org Split i18nString into 2 separate i18nStrings
2022-04-20 jobay@chromium.org Change position of close button to 'absolute'
2022-04-20 bmeurer@chromium.org [e2e] Fix and reenable ServiceWorker frame tree test.
2022-04-20 bmeurer@chromium.org [cleanup] Remove annoying warning from ARIAUtils.ts
2022-04-20 devtools-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Update DevTools DEPS.
2022-04-20 bmeurer@chromium.org [e2e] Fix and re-enable WebAssembly stepping tests.
2022-04-20 alexrudenko@chromium.org Roll puppeteer to v13.6.0
2022-04-20 bmeurer@chromium.org [e2e] Re-enable issues-link test.
2022-04-20 mathias@chromium.org Re-enable pseudo-class tests
2022-04-20 bmeurer@chromium.org [e2e] Improve and re-enable CSP Issues to Sources tests.
2022-04-20 mathias@chromium.org Fix and re-enable Elements tab e2e test
2022-04-20 devtools-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Update DevTools Chromium DEPS.
2022-04-20 mathias@chromium.org Fix and re-enable adorner toggling tests

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/devtools-frontend-chromium
Please CC devtools-waterfall-sheriff-onduty@grotations.appspotmail.com on the revert to ensure that a human
is aware of the problem.

To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1071851,chromium:1134120,chromium:1134593,chromium:1158782,chromium:1241860,chromium:1280763,chromium:1317608,chromium:1317621
Tbr: devtools-waterfall-sheriff-onduty@grotations.appspotmail.com
Change-Id: Iabf1e302f54c337e71b4a2a90e169a2ba7a31d47
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3597611
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#994279}

[modify] https://crrev.com/5c69380bb74de237634211a133393fff9aa9caa0/DEPS


### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1241860?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript, Platform>DevTools>JavaScript]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056951)*
