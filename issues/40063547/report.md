# Security: heap-use-after-free in extensions::NativeExtensionBindingsSystem::HandleResponse

| Field | Value |
|-------|-------|
| **Issue ID** | [40063547](https://issues.chromium.org/issues/40063547) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>ServiceWorker, Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | so...@chromium.org |
| **Created** | 2023-03-11 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

[TBD]

**VERSION**  

Chrome Version: 113.0.5630.0  

Operating System: Windows 11

**REPRODUCTION CASE**  

[TBD]

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: tab Crash State:

==8764==ERROR: AddressSanitizer: heap-use-after-free on address 0x11a679f6e280 at pc 0x7fff355a7716 bp 0x0003ceffe8c0 sp 0x0003ceffe908  

READ of size 8 at 0x11a679f6e280 thread T12  

==8764==WARNING: Failed to use and restart external symbolizer!  

==8764==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==8764==\*\*\* Most likely this means that the app is already \*\*\*  

==8764==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==8764==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==8764==\*\*\* or produce wrong results. \*\*\*  

#0 0x7fff355a7715 in extensions::NativeExtensionBindingsSystem::HandleResponse C:\b\s\w\ir\cache\builder\src\extensions\renderer\native\_extension\_bindings\_system.cc:644  

#1 0x7fff356080a4 in extensions::WorkerThreadDispatcher::OnResponseWorker C:\b\s\w\ir\cache\builder\src\extensions\renderer\worker\_thread\_dispatcher.cc:363  

#2 0x7fff35607cef in IPC::MessageT<ExtensionMsg\_ResponseWorker\_Meta,std::Cr::tuple<int,int,bool,ExtensionMsg\_ResponseWorkerData,std::Cr::basic\_string<char,std::Cr::char\_traits<char>,std::Cr::allocator<char> > >,void>::Dispatch<extensions::WorkerThreadDispatcher,extensions::WorkerThreadDispatcher,void,void (extensions::WorkerThreadDispatcher::\*)(int, int, bool, ExtensionMsg\_ResponseWorkerData, const std::Cr::basic\_string<char,std::Cr::char\_traits<char>,std::Cr::allocator<char> > &)> C:\b\s\w\ir\cache\builder\src\ipc\ipc\_message\_templates.h:141  

#3 0x7fff35604be9 in extensions::WorkerThreadDispatcher::OnMessageReceivedOnWorkerThread C:\b\s\w\ir\cache\builder\src\extensions\renderer\worker\_thread\_dispatcher.cc:318  

#4 0x7fff3560a783 in base::internal::Invoker<base::internal::BindState<void (\*)(int, const IPC::Message &),int,IPC::Message>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:985  

#5 0x7fff35bdc8da in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:162  

#6 0x7fff3906bd7f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:473  

#7 0x7fff3906a98a in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:337  

#8 0x7fff3908bea3 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:48  

#9 0x7fff3906e617 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:629  

#10 0x7fff35c52ca1 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#11 0x7fff33b096c7 in blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\scheduler\worker\non\_main\_thread\_impl.cc:169  

#12 0x7fff35ada281 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:133  

#13 0x7ff65f806033 in \_\_asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_thread.cpp:277  

#14 0x7ff8393426bc in BaseThreadInitThunk+0x1c (C:\WINDOWS\System32\KERNEL32.DLL+0x1800126bc)  

#15 0x7ff83a84a9f7 in RtlUserThreadStart+0x27 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005a9f7)

0x11a679f6e280 is located 0 bytes inside of 920-byte region [0x11a679f6e280,0x11a679f6e618)  

freed by thread T12 here:  

#0 0x7ff65f80f52d in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82 #1 0x7fff355d63fe in extensions::ServiceWorkerData::~ServiceWorkerData C:\b\s\w\ir\cache\builder\src\extensions\renderer\service\_worker\_data.cc:22  

#2 0x7fff3560a4b1 in extensions::WorkerThreadDispatcher::RemoveWorkerData C:\b\s\w\ir\cache\builder\src\extensions\renderer\worker\_thread\_dispatcher.cc:518  

#3 0x7fff3553be93 in extensions::Dispatcher::WillDestroyServiceWorkerContextOnWorkerThread C:\b\s\w\ir\cache\builder\src\extensions\renderer\dispatcher.cc:690  

#4 0x7fff4841d3ab in content::ServiceWorkerContextClient::WillDestroyWorkerContext C:\b\s\w\ir\cache\builder\src\content\renderer\service\_worker\service\_worker\_context\_client.cc:354  

#5 0x7fff49ac0c5a in blink::ServiceWorkerGlobalScopeProxy::WillDestroyWorkerGlobalScope C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\service\_worker\service\_worker\_global\_scope\_proxy.cc:218  

#6 0x7fff3ec056c7 in blink::WorkerThread::PrepareForShutdownOnWorkerThread C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\workers\worker\_thread.cc:760  

#7 0x7fff3ec0b075 in base::internal::Invoker<base::internal::BindState<void (\*)(blink::WorkerThread::InterruptData \*),WTF::CrossThreadUnretainedWrapper[blink::WorkerThread::InterruptData](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:985  

#8 0x7fff35bdc8da in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:162  

#9 0x7fff3906bd7f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:473  

#10 0x7fff3906a98a in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:337  

#11 0x7fff3908bea3 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:48  

#12 0x7fff3906e868 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:626  

#13 0x7fff35c52ca1 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#14 0x7fff385935fb in content::`anonymous namespace'::NestedMessageLoopRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\child\blink\_platform\_impl.cc:88  

#15 0x7fff3ec08901 in blink::WorkerThread::PauseOrFreezeOnWorkerThread C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\workers\worker\_thread.cc:917  

#16 0x7fff3ec038bb in blink::WorkerThread::PauseOrFreeze C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\workers\worker\_thread.cc:857  

#17 0x7fff43af2a3b in blink::WorkerThreadDebugger::runMessageLoopOnPause C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\inspector\worker\_thread\_debugger.cc:182  

#18 0x7fff2eb5d47c in v8\_inspector::V8Debugger::handleProgramBreak C:\b\s\w\ir\cache\builder\src\v8\src\inspector\v8-debugger.cc:508  

#19 0x7fff2eb5e933 in v8\_inspector::V8Debugger::BreakProgramRequested C:\b\s\w\ir\cache\builder\src\v8\src\inspector\v8-debugger.cc:634  

#20 0x7fff2cc6561c in v8::internal::Debug::OnDebugBreak C:\b\s\w\ir\cache\builder\src\v8\src\debug\debug.cc:2392  

#21 0x7fff2cc6292b in v8::internal::Debug::Break C:\b\s\w\ir\cache\builder\src\v8\src\debug\debug.cc:561  

#22 0x7fff2dd8bdd1 in v8::internal::Runtime\_DebugBreakOnBytecode C:\b\s\w\ir\cache\builder\src\v8\src\runtime\runtime-debug.cc:35  

#23 0x7fff4b5e487e in Builtins\_CEntry\_Return2\_ArgvOnStack\_NoBuiltinExit+0x3e (C:\Files\Chromium\Builds\asan-win32-release\_x64-1112844\chrome.dll+0x1a2d7487e)  

#24 0x7fff4b6894ba in Builtins\_DebugBreak2Handler+0x3a (C:\Files\Chromium\Builds\asan-win32-release\_x64-1112844\chrome.dll+0x1a2e194ba)  

#25 0x7fff4b557fa5 in Builtins\_InterpreterEntryTrampoline+0xe5 (C:\Files\Chromium\Builds\asan-win32-release\_x64-1112844\chrome.dll+0x1a2ce7fa5)  

#26 0x7fff4b5561db in Builtins\_JSEntryTrampoline+0x5b (C:\Files\Chromium\Builds\asan-win32-release\_x64-1112844\chrome.dll+0x1a2ce61db)  

#27 0x7fff4b555dda in Builtins\_JSEntry+0xda (C:\Files\Chromium\Builds\asan-win32-release\_x64-1112844\chrome.dll+0x1a2ce5dda)

previously allocated by thread T12 here:  

#0 0x7ff65f80f62d in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7fff4b6d311e in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7fff35537340 in extensions::Dispatcher::CreateBindingsSystem C:\b\s\w\ir\cache\builder\src\extensions\renderer\dispatcher.cc:1589  

#3 0x7fff3553ad32 in extensions::Dispatcher::WillEvaluateServiceWorkerOnWorkerThread C:\b\s\w\ir\cache\builder\src\extensions\renderer\dispatcher.cc:556  

#4 0x7fff4841c252 in content::ServiceWorkerContextClient::WillEvaluateScript C:\b\s\w\ir\cache\builder\src\content\renderer\service\_worker\service\_worker\_context\_client.cc:295  

#5 0x7fff49ac0042 in blink::ServiceWorkerGlobalScopeProxy::WillEvaluateScript C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\service\_worker\service\_worker\_global\_scope\_proxy.cc:181  

#6 0x7fff3f4b126d in blink::WorkerGlobalScope::RunWorkerScript C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\workers\worker\_global\_scope.cc:504  

#7 0x7fff3f4b08a2 in blink::WorkerGlobalScope::EvaluateClassicScript C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\workers\worker\_global\_scope.cc:455  

#8 0x7fff493ef981 in blink::ServiceWorkerGlobalScope::RunClassicScript C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\service\_worker\service\_worker\_global\_scope.cc:556  

#9 0x7fff493eed7e in blink::ServiceWorkerGlobalScope::DidFetchClassicScript C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\service\_worker\service\_worker\_global\_scope.cc:454  

#10 0x7fff49416376 in base::internal::Invoker<base::internal::BindState<void (blink::ServiceWorkerGlobalScope::\*)(blink::WorkerClassicScriptLoader \*, const v8\_inspector::V8StackTraceId &),cppgc::internal::BasicPersistent[blink::ServiceWorkerGlobalScope,cppgc::internal::WeakPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy](javascript:void(0);),cppgc::internal::BasicPersistent[blink::WorkerClassicScriptLoader,cppgc::internal::StrongPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy](javascript:void(0);),v8\_inspector::V8StackTraceId>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:985  

#11 0x7fff44507f01 in blink::WorkerClassicScriptLoader::OnFinishedLoadingWorkerMainScript C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\workers\worker\_classic\_script\_loader.cc:310  

#12 0x7fff33c558d6 in blink::WorkerMainScriptLoader::NotifyCompletionIfAppropriate C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\loader\fetch\url\_loader\worker\_main\_script\_loader.cc:270  

#13 0x7fff33c568c9 in blink::WorkerMainScriptLoader::OnReadable C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\loader\fetch\url\_loader\worker\_main\_script\_loader.cc:232  

#14 0x7fff33c57b1a in base::internal::Invoker<base::internal::BindState<void (blink::WorkerMainScriptLoader::\*)(unsigned int),cppgc::internal::BasicPersistent[blink::WorkerMainScriptLoader,cppgc::internal::WeakPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy](javascript:void(0);) >,void (unsigned int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:998  

#15 0x7fff2c152231 in base::RepeatingCallback<void (unsigned int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:333  

#16 0x7fff2c152038 in base::internal::Invoker<base::internal::BindState<void (\*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo::HandleSignalsState &)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:998  

#17 0x7fff35ee9924 in base::RepeatingCallback<void (unsigned int, const mojo::HandleSignalsState &)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:333  

#18 0x7fff35ee9440 in mojo::SimpleWatcher::OnHandleReady C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple\_watcher.cc:278  

#19 0x7fff35eea772 in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);),int,unsigned int,mojo::HandleSignalsState>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:985  

#20 0x7fff35bdc8da in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:162  

#21 0x7fff3906bd7f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:473  

#22 0x7fff3906a98a in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:337  

#23 0x7fff3908bea3 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:48  

#24 0x7fff3906e617 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:629  

#25 0x7fff35c52ca1 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#26 0x7fff33b096c7 in blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\scheduler\worker\non\_main\_thread\_impl.cc:169  

#27 0x7fff35ada281 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:133

Thread T12 created by T11 here:  

#0 0x7ff65f804b12 in \_\_asan\_wrap\_CreateThread C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_win.cpp:146  

#1 0x7fff35ad907f in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:198 #2 0x7fff35b824b9 in base::SimpleThread::StartAsync C:\b\s\w\ir\cache\builder\src\base\threading\simple_thread.cc:54 #3 0x7fff33b076b4 in blink::NonMainThread::CreateThread C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\scheduler\worker\non_main_thread_impl.cc:36 #4 0x7fff414b982b in blink::WorkerBackingThread::WorkerBackingThread C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\worker_backing_thread.cc:59 #5 0x7fff49ac238f in blink::ServiceWorkerThread::ServiceWorkerThread C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\service_worker\service_worker_thread.cc:56 #6 0x7fff48414639 in blink::WebEmbeddedWorkerImpl::StartWorkerThread C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\exported\web_embedded_worker_impl.cc:224 #7 0x7fff48413216 in blink::WebEmbeddedWorkerImpl::StartWorkerContext C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\exported\web_embedded_worker_impl.cc:131 #8 0x7fff4841a97a in content::ServiceWorkerContextClient::StartWorkerContextOnInitiatorThread C:\b\s\w\ir\cache\builder\src\content\renderer\service_worker\service_worker_context_client.cc:195 #9 0x7fff45ab53c6 in content::EmbeddedWorkerInstanceClientImpl::StartWorker C:\b\s\w\ir\cache\builder\src\content\renderer\service_worker\embedded_worker_instance_client_impl.cc:135 #10 0x7fff2bcc4d05 in blink::mojom::EmbeddedWorkerInstanceClientStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\public\mojom\service_worker\embedded_worker.mojom.cc:636 #11 0x7fff35ea68ca in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:1007 #12 0x7fff391be888 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43 #13 0x7fff35eac2b7 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:694 #14 0x7fff35e98500 in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1096 #15 0x7fff35e972e8 in mojo::internal::MultiplexRouter::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:710 #16 0x7fff391be888 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43 #17 0x7fff35ebcc30 in mojo::Connector::DispatchMessageW C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:550 #18 0x7fff35ebe5bc in mojo::Connector::ReadAllAvailableMessages C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:607 #19 0x7fff35ec0574 in base::internal::Invoker<base::internal::BindState<void (mojo::Connector::\*)(unsigned int),base::internal::UnretainedWrapper<mojo::Connector,base::unretained_traits::MayNotDangle,0> >,void (unsigned int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:998 #20 0x7fff2c152231 in base::RepeatingCallback<void (unsigned int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:333 #21 0x7fff2c152038 in base::internal::Invoker<base::internal::BindState<void (\*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo::HandleSignalsState &)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:998 #22 0x7fff35ee9924 in base::RepeatingCallback<void (unsigned int, const mojo::HandleSignalsState &)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:333 #23 0x7fff35ee9440 in mojo::SimpleWatcher::OnHandleReady C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc:278 #24 0x7fff35eea772 in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher>,int,unsigned int,mojo::HandleSignalsState>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:985 #25 0x7fff35bdc8da in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:162 #26 0x7fff3d25be8e in base::internal::TaskTracker::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:649 #27 0x7fff3d25d219 in base::internal::TaskTracker::RunSkipOnShutdown C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:634 #28 0x7fff3d25b2d1 in base::internal::TaskTracker::RunTask C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:491 #29 0x7fff3d25a33b in base::internal::TaskTracker::RunAndPopNextTask C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:406 #30 0x7fff428004ce in base::internal::WorkerThread::RunWorker C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:480 #31 0x7fff427ff7ef in base::internal::WorkerThread::RunSharedWorker C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:366 #32 0x7fff35ada281 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:133  

#33 0x7ff65f806033 in \_\_asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_thread.cpp:277  

#34 0x7ff8393426bc in BaseThreadInitThunk+0x1c (C:\WINDOWS\System32\KERNEL32.DLL+0x1800126bc)  

#35 0x7ff83a84a9f7 in RtlUserThreadStart+0x27 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005a9f7)

Thread T11 created by T0 here:  

#0 0x7ff65f804b12 in \_\_asan\_wrap\_CreateThread C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_win.cpp:146  

#1 0x7fff35ad907f in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:198  

#2 0x7fff427fdae0 in base::internal::WorkerThread::Start C:\b\s\w\ir\cache\builder\src\base\task\thread\_pool\worker\_thread.cc:193  

#3 0x7fff3d267015 in base::internal::PooledSingleThreadTaskRunnerManager::CreateSingleThreadTaskRunner C:\b\s\w\ir\cache\builder\src\base\task\thread\_pool\pooled\_single\_thread\_task\_runner\_manager.cc:618  

#4 0x7fff39048c83 in base::internal::ThreadPoolImpl::CreateSingleThreadTaskRunner C:\b\s\w\ir\cache\builder\src\base\task\thread\_pool\thread\_pool\_impl.cc:257  

#5 0x7fff35b95453 in base::ThreadPool::CreateSingleThreadTaskRunner C:\b\s\w\ir\cache\builder\src\base\task\thread\_pool.cc:115  

#6 0x7fff4149f7b3 in content::ExposeRendererInterfacesToBrowser C:\b\s\w\ir\cache\builder\src\content\renderer\browser\_exposed\_renderer\_interfaces.cc:181  

#7 0x7fff3c1e72f6 in content::RenderThreadImpl::Init C:\b\s\w\ir\cache\builder\src\content\renderer\render\_thread\_impl.cc:620  

#8 0x7fff3c1e9d3d in content::RenderThreadImpl::RenderThreadImpl C:\b\s\w\ir\cache\builder\src\content\renderer\render\_thread\_impl.cc:564  

#9 0x7fff388c9b94 in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer\_main.cc:282  

#10 0x7fff343d2592 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:783  

#11 0x7fff343d532e in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1154  

#12 0x7fff343d006c in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:324  

#13 0x7fff343d0c9c in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:341  

#14 0x7fff28871699 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:190  

#15 0x7ff65f7564e8 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:166  

#16 0x7ff65f752bad in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:390  

#17 0x7ff65fb7f05b in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288 #18 0x7ff8393426bc in BaseThreadInitThunk+0x1c (C:\WINDOWS\System32\KERNEL32.DLL+0x1800126bc)  

#19 0x7ff83a84a9f7 in RtlUserThreadStart+0x27 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005a9f7)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\extensions\renderer\native\_extension\_bindings\_system.cc:644 in extensions::NativeExtensionBindingsSystem::HandleResponse  

Shadow bytes around the buggy address:  

0x11a679f6e000: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11a679f6e080: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11a679f6e100: fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa fa  

0x11a679f6e180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x11a679f6e200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x11a679f6e280:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11a679f6e300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11a679f6e380: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11a679f6e400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11a679f6e480: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11a679f6e500: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb

==8764==ADDITIONAL INFO

==8764==Note: Please include this section with the ASan report.  

Task trace:  

#0 0x7fff35605f08 in extensions::WorkerThreadDispatcher::PostTaskToWorkerThread C:\b\s\w\ir\cache\builder\src\extensions\renderer\worker\_thread\_dispatcher.cc:336  

#1 0x7fff3647de38 in IPC::ChannelProxy::Context::OnMessageReceivedNoFilter C:\b\s\w\ir\cache\builder\src\ipc\ipc\_channel\_proxy.cc:130

==8764==END OF ADDITIONAL INFO  

==8764==ABORTING

## Attachments

- [poc.webm](attachments/poc.webm) (video/webm, 4.5 MB)
- [sw.js](attachments/sw.js) (text/plain, 149 B)
- [manifest.json](attachments/manifest.json) (text/plain, 151 B)

## Timeline

### [Deleted User] (2023-03-11)

[Empty comment from Monorail migration]

### st...@gmail.com (2023-03-11)

Alternative stack trace:

=================================================================
==27908==ERROR: AddressSanitizer: heap-use-after-free on address 0x12ecd2c0fe50 at pc 0x7fff356058e9 bp 0x00ebd15feac0 sp 0x00ebd15feb08
READ of size 8 at 0x12ecd2c0fe50 thread T13
==27908==WARNING: Failed to use and restart external symbolizer!
==27908==*** WARNING: Failed to initialize DbgHelp!              ***
==27908==*** Most likely this means that the app is already      ***
==27908==*** using DbgHelp, possibly with incompatible flags.    ***
==27908==*** Due to technical reasons, symbolization might crash ***
==27908==*** or produce wrong results.                           ***
    #0 0x7fff356058e8 in extensions::WorkerThreadDispatcher::DispatchEventHelper C:\b\s\w\ir\cache\builder\src\extensions\renderer\worker_thread_dispatcher.cc:397
    #1 0x7fff35605325 in extensions::WorkerThreadDispatcher::DispatchEventOnWorkerThread C:\b\s\w\ir\cache\builder\src\extensions\renderer\worker_thread_dispatcher.cc:197
    #2 0x7fff3560c025 in base::internal::Invoker<base::internal::BindState<void (*)(mojo::StructPtr<extensions::mojom::DispatchEventParams>, base::Value::List),mojo::StructPtr<extensions::mojom::DispatchEventParams>,base::Value::List>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:985
    #3 0x7fff35bdc8da in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:162
    #4 0x7fff3906bd7f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:473
    #5 0x7fff3906a98a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:337
    #6 0x7fff3908bea3 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:48
    #7 0x7fff3906e617 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:629
    #8 0x7fff35c52ca1 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:140
    #9 0x7fff33b096c7 in blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\scheduler\worker\non_main_thread_impl.cc:169
    #10 0x7fff35ada281 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:133
    #11 0x7ff65f806033 in __asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_thread.cpp:277
    #12 0x7ff8393426bc in BaseThreadInitThunk+0x1c (C:\WINDOWS\System32\KERNEL32.DLL+0x1800126bc)
    #13 0x7ff83a84a9f7 in RtlUserThreadStart+0x27 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005a9f7)

0x12ecd2c0fe50 is located 0 bytes inside of 48-byte region [0x12ecd2c0fe50,0x12ecd2c0fe80)
freed by thread T13 here:
    #0 0x7ff65f80f52d in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7fff3560a4b9 in extensions::WorkerThreadDispatcher::RemoveWorkerData C:\b\s\w\ir\cache\builder\src\extensions\renderer\worker_thread_dispatcher.cc:518
    #2 0x7fff3553be93 in extensions::Dispatcher::WillDestroyServiceWorkerContextOnWorkerThread C:\b\s\w\ir\cache\builder\src\extensions\renderer\dispatcher.cc:690
    #3 0x7fff4841d3ab in content::ServiceWorkerContextClient::WillDestroyWorkerContext C:\b\s\w\ir\cache\builder\src\content\renderer\service_worker\service_worker_context_client.cc:354
    #4 0x7fff49ac0c5a in blink::ServiceWorkerGlobalScopeProxy::WillDestroyWorkerGlobalScope C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\service_worker\service_worker_global_scope_proxy.cc:218
    #5 0x7fff3ec056c7 in blink::WorkerThread::PrepareForShutdownOnWorkerThread C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\worker_thread.cc:760
    #6 0x7fff3ec0b075 in base::internal::Invoker<base::internal::BindState<void (*)(blink::WorkerThread::InterruptData *),WTF::CrossThreadUnretainedWrapper<blink::WorkerThread::InterruptData> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:985
    #7 0x7fff35bdc8da in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:162
    #8 0x7fff3906bd7f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:473
    #9 0x7fff3906a98a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:337
    #10 0x7fff3908bea3 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:48
    #11 0x7fff3906e868 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:626
    #12 0x7fff35c52ca1 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:140
    #13 0x7fff385935fb in content::`anonymous namespace'::NestedMessageLoopRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\child\blink_platform_impl.cc:88
    #14 0x7fff3ec08901 in blink::WorkerThread::PauseOrFreezeOnWorkerThread C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\worker_thread.cc:917
    #15 0x7fff3ec038bb in blink::WorkerThread::PauseOrFreeze C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\worker_thread.cc:857
    #16 0x7fff43af2a3b in blink::WorkerThreadDebugger::runMessageLoopOnPause C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\inspector\worker_thread_debugger.cc:182
    #17 0x7fff2eb5d47c in v8_inspector::V8Debugger::handleProgramBreak C:\b\s\w\ir\cache\builder\src\v8\src\inspector\v8-debugger.cc:508
    #18 0x7fff2eb5e933 in v8_inspector::V8Debugger::BreakProgramRequested C:\b\s\w\ir\cache\builder\src\v8\src\inspector\v8-debugger.cc:634
    #19 0x7fff2cc6561c in v8::internal::Debug::OnDebugBreak C:\b\s\w\ir\cache\builder\src\v8\src\debug\debug.cc:2392
    #20 0x7fff2cc6292b in v8::internal::Debug::Break C:\b\s\w\ir\cache\builder\src\v8\src\debug\debug.cc:561
    #21 0x7fff2dd8bdd1 in v8::internal::Runtime_DebugBreakOnBytecode C:\b\s\w\ir\cache\builder\src\v8\src\runtime\runtime-debug.cc:35
    #22 0x7fff4b5e487e in Builtins_CEntry_Return2_ArgvOnStack_NoBuiltinExit+0x3e (C:\Files\Chromium\Builds\asan-win32-release_x64-1112844\chrome.dll+0x1a2d7487e)
    #23 0x7fff4b68937e in Builtins_DebugBreak0Handler+0x3e (C:\Files\Chromium\Builds\asan-win32-release_x64-1112844\chrome.dll+0x1a2e1937e)
    #24 0x7fff4b557fa5 in Builtins_InterpreterEntryTrampoline+0xe5 (C:\Files\Chromium\Builds\asan-win32-release_x64-1112844\chrome.dll+0x1a2ce7fa5)
    #25 0x7fff4b5561db in Builtins_JSEntryTrampoline+0x5b (C:\Files\Chromium\Builds\asan-win32-release_x64-1112844\chrome.dll+0x1a2ce61db)
    #26 0x7fff4b555dda in Builtins_JSEntry+0xda (C:\Files\Chromium\Builds\asan-win32-release_x64-1112844\chrome.dll+0x1a2ce5dda)
    #27 0x7fff2cd21f8b in v8::internal::`anonymous namespace'::Invoke C:\b\s\w\ir\cache\builder\src\v8\src\execution\execution.cc:427

previously allocated by thread T13 here:
    #0 0x7ff65f80f62d in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7fff4b6d311e in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
    #2 0x7fff35609964 in extensions::WorkerThreadDispatcher::AddWorkerData C:\b\s\w\ir\cache\builder\src\extensions\renderer\worker_thread_dispatcher.cc:465
    #3 0x7fff3553ad64 in extensions::Dispatcher::WillEvaluateServiceWorkerOnWorkerThread C:\b\s\w\ir\cache\builder\src\extensions\renderer\dispatcher.cc:554
    #4 0x7fff4841c252 in content::ServiceWorkerContextClient::WillEvaluateScript C:\b\s\w\ir\cache\builder\src\content\renderer\service_worker\service_worker_context_client.cc:295
    #5 0x7fff49ac0042 in blink::ServiceWorkerGlobalScopeProxy::WillEvaluateScript C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\service_worker\service_worker_global_scope_proxy.cc:181
    #6 0x7fff3f4b126d in blink::WorkerGlobalScope::RunWorkerScript C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\worker_global_scope.cc:504
    #7 0x7fff3f4b08a2 in blink::WorkerGlobalScope::EvaluateClassicScript C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\worker_global_scope.cc:455
    #8 0x7fff493ef981 in blink::ServiceWorkerGlobalScope::RunClassicScript C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\service_worker\service_worker_global_scope.cc:556
    #9 0x7fff493eed7e in blink::ServiceWorkerGlobalScope::DidFetchClassicScript C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\service_worker\service_worker_global_scope.cc:454
    #10 0x7fff49416376 in base::internal::Invoker<base::internal::BindState<void (blink::ServiceWorkerGlobalScope::*)(blink::WorkerClassicScriptLoader *, const v8_inspector::V8StackTraceId &),cppgc::internal::BasicPersistent<blink::ServiceWorkerGlobalScope,cppgc::internal::WeakPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy>,cppgc::internal::BasicPersistent<blink::WorkerClassicScriptLoader,cppgc::internal::StrongPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy>,v8_inspector::V8StackTraceId>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:985
    #11 0x7fff44507f01 in blink::WorkerClassicScriptLoader::OnFinishedLoadingWorkerMainScript C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\worker_classic_script_loader.cc:310
    #12 0x7fff33c558d6 in blink::WorkerMainScriptLoader::NotifyCompletionIfAppropriate C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\loader\fetch\url_loader\worker_main_script_loader.cc:270
    #13 0x7fff33c568c9 in blink::WorkerMainScriptLoader::OnReadable C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\loader\fetch\url_loader\worker_main_script_loader.cc:232
    #14 0x7fff33c57b1a in base::internal::Invoker<base::internal::BindState<void (blink::WorkerMainScriptLoader::*)(unsigned int),cppgc::internal::BasicPersistent<blink::WorkerMainScriptLoader,cppgc::internal::WeakPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy> >,void (unsigned int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:998
    #15 0x7fff2c152231 in base::RepeatingCallback<void (unsigned int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:333
    #16 0x7fff2c152038 in base::internal::Invoker<base::internal::BindState<void (*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo::HandleSignalsState &)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:998
    #17 0x7fff35ee9924 in base::RepeatingCallback<void (unsigned int, const mojo::HandleSignalsState &)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:333
    #18 0x7fff35ee9440 in mojo::SimpleWatcher::OnHandleReady C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc:278
    #19 0x7fff35eea772 in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher>,int,unsigned int,mojo::HandleSignalsState>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:985
    #20 0x7fff35bdc8da in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:162
    #21 0x7fff3906bd7f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:473
    #22 0x7fff3906a98a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:337
    #23 0x7fff3908bea3 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:48
    #24 0x7fff3906e617 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:629
    #25 0x7fff35c52ca1 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:140
    #26 0x7fff33b096c7 in blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\scheduler\worker\non_main_thread_impl.cc:169
    #27 0x7fff35ada281 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:133

Thread T13 created by T12 here:
    #0 0x7ff65f804b12 in __asan_wrap_CreateThread C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:146
    #1 0x7fff35ad907f in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:198
    #2 0x7fff35b824b9 in base::SimpleThread::StartAsync C:\b\s\w\ir\cache\builder\src\base\threading\simple_thread.cc:54
    #3 0x7fff33b076b4 in blink::NonMainThread::CreateThread C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\scheduler\worker\non_main_thread_impl.cc:36
    #4 0x7fff414b982b in blink::WorkerBackingThread::WorkerBackingThread C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\worker_backing_thread.cc:59
    #5 0x7fff49ac238f in blink::ServiceWorkerThread::ServiceWorkerThread C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\service_worker\service_worker_thread.cc:56
    #6 0x7fff48414639 in blink::WebEmbeddedWorkerImpl::StartWorkerThread C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\exported\web_embedded_worker_impl.cc:224
    #7 0x7fff48413216 in blink::WebEmbeddedWorkerImpl::StartWorkerContext C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\exported\web_embedded_worker_impl.cc:131
    #8 0x7fff4841a97a in content::ServiceWorkerContextClient::StartWorkerContextOnInitiatorThread C:\b\s\w\ir\cache\builder\src\content\renderer\service_worker\service_worker_context_client.cc:195
    #9 0x7fff45ab53c6 in content::EmbeddedWorkerInstanceClientImpl::StartWorker C:\b\s\w\ir\cache\builder\src\content\renderer\service_worker\embedded_worker_instance_client_impl.cc:135
    #10 0x7fff2bcc4d05 in blink::mojom::EmbeddedWorkerInstanceClientStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\public\mojom\service_worker\embedded_worker.mojom.cc:636
    #11 0x7fff35ea68ca in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:1007
    #12 0x7fff391be888 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #13 0x7fff35eac2b7 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:694
    #14 0x7fff35e98500 in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1096
    #15 0x7fff35e972e8 in mojo::internal::MultiplexRouter::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:710
    #16 0x7fff391be888 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #17 0x7fff35ebcc30 in mojo::Connector::DispatchMessageW C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:550
    #18 0x7fff35ebe5bc in mojo::Connector::ReadAllAvailableMessages C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:607
    #19 0x7fff35ec0574 in base::internal::Invoker<base::internal::BindState<void (mojo::Connector::*)(unsigned int),base::internal::UnretainedWrapper<mojo::Connector,base::unretained_traits::MayNotDangle,0> >,void (unsigned int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:998
    #20 0x7fff2c152231 in base::RepeatingCallback<void (unsigned int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:333
    #21 0x7fff2c152038 in base::internal::Invoker<base::internal::BindState<void (*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo::HandleSignalsState &)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:998
    #22 0x7fff35ee9924 in base::RepeatingCallback<void (unsigned int, const mojo::HandleSignalsState &)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:333
    #23 0x7fff35ee9440 in mojo::SimpleWatcher::OnHandleReady C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc:278
    #24 0x7fff35eea772 in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher>,int,unsigned int,mojo::HandleSignalsState>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:985
    #25 0x7fff35bdc8da in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:162
    #26 0x7fff3d25be8e in base::internal::TaskTracker::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:649
    #27 0x7fff3d25d219 in base::internal::TaskTracker::RunSkipOnShutdown C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:634
    #28 0x7fff3d25b2d1 in base::internal::TaskTracker::RunTask C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:491
    #29 0x7fff3d25a33b in base::internal::TaskTracker::RunAndPopNextTask C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:406
    #30 0x7fff428004ce in base::internal::WorkerThread::RunWorker C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:480
    #31 0x7fff427ff7ef in base::internal::WorkerThread::RunSharedWorker C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:366
    #32 0x7fff35ada281 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:133
    #33 0x7ff65f806033 in __asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_thread.cpp:277
    #34 0x7ff8393426bc in BaseThreadInitThunk+0x1c (C:\WINDOWS\System32\KERNEL32.DLL+0x1800126bc)
    #35 0x7ff83a84a9f7 in RtlUserThreadStart+0x27 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005a9f7)

Thread T12 created by T0 here:
    #0 0x7ff65f804b12 in __asan_wrap_CreateThread C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:146
    #1 0x7fff35ad907f in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:198
    #2 0x7fff427fdae0 in base::internal::WorkerThread::Start C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:193
    #3 0x7fff3d267015 in base::internal::PooledSingleThreadTaskRunnerManager::CreateSingleThreadTaskRunner C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\pooled_single_thread_task_runner_manager.cc:618
    #4 0x7fff39048c83 in base::internal::ThreadPoolImpl::CreateSingleThreadTaskRunner C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_pool_impl.cc:257
    #5 0x7fff35b95453 in base::ThreadPool::CreateSingleThreadTaskRunner C:\b\s\w\ir\cache\builder\src\base\task\thread_pool.cc:115
    #6 0x7fff4149f7b3 in content::ExposeRendererInterfacesToBrowser C:\b\s\w\ir\cache\builder\src\content\renderer\browser_exposed_renderer_interfaces.cc:181
    #7 0x7fff3c1e72f6 in content::RenderThreadImpl::Init C:\b\s\w\ir\cache\builder\src\content\renderer\render_thread_impl.cc:620
    #8 0x7fff3c1e9d3d in content::RenderThreadImpl::RenderThreadImpl C:\b\s\w\ir\cache\builder\src\content\renderer\render_thread_impl.cc:564
    #9 0x7fff388c9b94 in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:282
    #10 0x7fff343d2592 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:783
    #11 0x7fff343d532e in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1154
    #12 0x7fff343d006c in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:324
    #13 0x7fff343d0c9c in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:341
    #14 0x7fff28871699 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:190
    #15 0x7ff65f7564e8 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:166
    #16 0x7ff65f752bad in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:390
    #17 0x7ff65fb7f05b in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #18 0x7ff8393426bc in BaseThreadInitThunk+0x1c (C:\WINDOWS\System32\KERNEL32.DLL+0x1800126bc)
    #19 0x7ff83a84a9f7 in RtlUserThreadStart+0x27 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005a9f7)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\extensions\renderer\worker_thread_dispatcher.cc:397 in extensions::WorkerThreadDispatcher::DispatchEventHelper
Shadow bytes around the buggy address:
  0x12ecd2c0fb80: fa fa 00 00 00 00 00 00 fa fa fd fd fd fd fd fd
  0x12ecd2c0fc00: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fd
  0x12ecd2c0fc80: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fd
  0x12ecd2c0fd00: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fd
  0x12ecd2c0fd80: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fd
=>0x12ecd2c0fe00: fa fa 00 00 00 00 00 00 fa fa[fd]fd fd fd fd fd
  0x12ecd2c0fe80: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fd
  0x12ecd2c0ff00: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fd
  0x12ecd2c0ff80: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fa
  0x12ecd2c10000: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fd
  0x12ecd2c10080: fa fa 00 00 00 00 00 fa fa fa 00 00 00 00 00 00
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

==27908==ADDITIONAL INFO

==27908==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7fff35605f08 in extensions::WorkerThreadDispatcher::PostTaskToWorkerThread C:\b\s\w\ir\cache\builder\src\extensions\renderer\worker_thread_dispatcher.cc:336
    #1 0x7fff3646e323 in IPC::`anonymous namespace'::ChannelAssociatedGroupController::Accept C:\b\s\w\ir\cache\builder\src\ipc\ipc_mojo_bootstrap.cc:1017


==27908==END OF ADDITIONAL INFO
==27908==ABORTING

### st...@gmail.com (2023-03-11)

**BISECT**

Fixed in commit 9941f842083e7534f1824d59c864f3d60c28e47a

Affected (vulnerable) release branches:  

Extended: yes  

Stable: yes  

Beta: yes  

Dev: yes  

Canary: no, since 113.0.5640.0

### st...@gmail.com (2023-03-11)

I'll add the steps to reproduce and the POC extension here soon.

### st...@gmail.com (2023-03-13)

**VULNERABILITY DETAILS**  

Reloading an extension while the service worker is paused on a debugger breakpoint in the `chrome.runtime.onInstalled` callback causes heap-UAF.

**STEPS TO REPRODUCE**

1. Install the attached extension (no permissions)
2. Click on Inspect service worker
3. Reload the extension (by clicking the reload button or with `chrome.runtime.reload()`)

Tested in r1114555, see <https://crbug.com/chromium/1423656#c3> for affected versions. Does not repro on r1114579 and newer.

### ma...@chromium.org (2023-03-13)

Foundin-110 based on reported bisect results in https://crbug.com/chromium/1423656#c3.
Severity medium based on memory corruption that requires a cooperating extension to be installed. 

Seems curious that 9941f842083e7534f1824d59c864f3d60c28e47a would fix it,  just based on a skim of the CL it doesn't look like that would change behavior.
If that CL does fix it then we should merge that back to earlier branches, but cc'ing some people for more detailed look at this.


[Monorail components: Blink>ServiceWorker Platform>Extensions]

### [Deleted User] (2023-03-13)

[Empty comment from Monorail migration]

### pk...@chromium.org (2023-03-13)

I suspect that my CL changes this from a UAF to a null deref. If that's preferable you can try to merge back, although I'd be a little leery of doing so, since `thread_local` seems to be filled with dragons.

What I believe is happening from reading the stacks in https://crbug.com/chromium/1423656#c2 -- although it isn't 100% clear to me -- is that something, perhaps https://source.chromium.org/chromium/chromium/src/+/main:extensions/renderer/worker_thread_dispatcher.cc;l=392;drc=1cb13ea510f483d4c8e48b9239c446b67316ca55, is resulting in spinning a nested message loop between the null-check of the thread-local pointer atop WorkerThreadDispatcher::DispatchEventHelper() and the use of that pointer at the end of that function. This nested message loop is freeing the pointer and resetting the thread-local object to point to null. The difference before and after my patch is that before my patch we have a ThreadLocalPointer object and afterward we have a direct thread_local. So beforehand, the underlying pointer is freed and then `g_data_tls` is set to null, but anyone still holding `g_data_tls.Get()` (as this function is) will be holding a dangling pointer. Afterward, we're using the thread_local pointer directly, so when we return from the nested message loop, the thing we're dereffing is null. (Which will presumably crash.)

I don't know this code's invariants, so I don't know if the fix is to not spin a nested loop, or to save off the necessary state before possibly spinning it, or to null-check-and-bail on return from it. Sending to lazyboy@ based on blame.

### [Deleted User] (2023-03-14)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### so...@chromium.org (2023-03-16)

[Empty comment from Monorail migration]

### so...@chromium.org (2023-03-16)

Richard, would you like to add this to your queue?

### ri...@chromium.org (2023-03-16)

Sure

### [Deleted User] (2023-03-31)

richardzh: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### so...@chromium.org (2023-04-13)

Richard, have you been able to reproduce this issue?

### [Deleted User] (2023-04-14)

richardzh: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### st...@gmail.com (2023-05-16)

I can confirm this no longer reproduces in stable 113.0.5672.93 and head 115.0.5776.0. According to Chromium Dash, 9941f842083e7534f1824d59c864f3d60c28e47a (the commit after which this is no longer reproducible) is currently in all branches except extended and should reach M114 (for the extended channel) in May 30.

At this point, I'm not sure if merging this into stable will help the fix to reach the extended channel faster than just waiting for M114 to be rolled out.

### so...@chromium.org (2023-05-16)

If this no longer reproduces, should this bug be closed?

### so...@chromium.org (2023-05-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-17)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-05-22)

This appears to have been mitigated by https://chromium-review.googlesource.com/c/chromium/src/+/4318363, turning this UAF into a null deref, which was landed on 8 March based on previously planned work in https://crbug.com/chromium/1416710. 

### am...@google.com (2023-05-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-25)

Thank you for this report, Thomas! Given this issue was already being resolved prior to your report, we would like to extend you a $1,000 thank you reward so that we can evaluate the fix for this issue as a potential for backmerge given security implications. Thank you for your efforts!  

### am...@google.com (2023-05-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1423656?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>ServiceWorker, Platform>Extensions]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063547)*
