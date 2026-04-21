# Security: heap-use-after-free third_party\blink\renderer\core\workers\worker_thread.cc:905 in blink::WorkerThread::PauseOrFreezeOnWorkerThread

| Field | Value |
|-------|-------|
| **Issue ID** | [40061275](https://issues.chromium.org/issues/40061275) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GarbageCollection, Blink>WebAudio, Blink>Workers |
| **Platforms** | Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | dt...@chromium.org |
| **Created** | 2022-10-08 |
| **Bounty** | $7,000.00 |

## Description

**VERSION**  

WIN10 X64

 `git log commit 838cbb6cecb0c3443a2b7ad06ef0868ba8180041 (HEAD, origin/main, origin/HEAD) Author: Marc Treib <treib@chromium.org> Date: Fri Oct 7 07:54:00 2022 +0000` 

 `target_cpu = "x64" dcheck_always_on = false is_asan = true is_component_build = true is_debug = false enable_nacl = false` 

**REPRODUCTION CASE**  

install node  

install puppeteer-core  

node ch.test.js chrome\_bin\_path <http://localhost/poc.html>

The problem may crash at other points, ch.test will cycle the test ten times to ensure that the UAF problem occurs steadily

Type of crash: [tab]

#RCA  

Coming soon

# #Asan

==2956==ERROR: AddressSanitizer: heap-use-after-free on address 0x11fd92373ee8 at pc 0x7ffd4b776f8c bp 0x00278a7fd780 sp 0x00278a7fd7c8  

WRITE of size 8 at 0x11fd92373ee8 thread T24  

#0 0x7ffd4b776f8b in blink::WorkerThread::PauseOrFreezeOnWorkerThread D:\chromium\src\third\_party\blink\renderer\core\workers\worker\_thread.cc:905  

#1 0x7ffd4b77219b in blink::WorkerThread::PauseOrFreeze D:\chromium\src\third\_party\blink\renderer\core\workers\worker\_thread.cc:848  

#2 0x7ffd49d3a2fb in blink::WorkerThreadDebugger::runMessageLoopOnPause D:\chromium\src\third\_party\blink\renderer\core\inspector\worker\_thread\_debugger.cc:182  

#3 0x7ffd4b76e04a in blink::WorkerThread::InitializeOnWorkerThread D:\chromium\src\third\_party\blink\renderer\core\workers\worker\_thread.cc:667  

#4 0x7ffd4b777880 in base::internal::Invoker<base::internal::BindState<void (blink::WorkerThread::\*)(std::Cr::unique\_ptr<blink::GlobalScopeCreationParams,std::Cr::default\_delete[blink::GlobalScopeCreationParams](javascript:void(0);) >, const absl::optional[blink::WorkerBackingThreadStartupData](javascript:void(0);) &, std::Cr::unique\_ptr<blink::WorkerDevToolsParams,std::Cr::default\_delete[blink::WorkerDevToolsParams](javascript:void(0);) >),WTF::CrossThreadUnretainedWrapper[blink::WorkerThread](javascript:void(0);),std::Cr::unique\_ptr<blink::GlobalScopeCreationParams,std::Cr::default\_delete[blink::GlobalScopeCreationParams](javascript:void(0);) >,absl::optional[blink::WorkerBackingThreadStartupData](javascript:void(0);),std::Cr::unique\_ptr<blink::WorkerDevToolsParams,std::Cr::default\_delete[blink::WorkerDevToolsParams](javascript:void(0);) > >,void ()>::RunOnce D:\chromium\src\base\functional\bind\_internal.h:871  

#5 0x7ffd8731dde9 in base::TaskAnnotator::RunTaskImpl D:\chromium\src\base\task\common\task\_annotator.cc:133  

#6 0x7ffd873779ab in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl D:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:441  

#7 0x7ffd873767fd in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork D:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:297  

#8 0x7ffd871d60be in base::MessagePumpDefault::Run D:\chromium\src\base\message\_loop\message\_pump\_default.cc:40  

#9 0x7ffd87379fc1 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run D:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:597  

#10 0x7ffd8728dd3e in base::RunLoop::Run D:\chromium\src\base\run\_loop.cc:141  

#11 0x7ffd7ecb13f2 in content::`anonymous namespace'::NestedMessageLoopRunnerImpl::Run D:\chromium\src\content\child\blink_platform_impl.cc:87 #12 0x7ffd4b776c1b in blink::WorkerThread::PauseOrFreezeOnWorkerThread D:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:902 #13 0x7ffd4b77219b in blink::WorkerThread::PauseOrFreeze D:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:848 #14 0x7ffd49d3a2fb in blink::WorkerThreadDebugger::runMessageLoopOnPause D:\chromium\src\third_party\blink\renderer\core\inspector\worker_thread_debugger.cc:182 #15 0x7ffd4b76e04a in blink::WorkerThread::InitializeOnWorkerThread D:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:667 #16 0x7ffd4b777880 in base::internal::Invoker<base::internal::BindState<void (blink::WorkerThread::\*)(std::Cr::unique_ptr<blink::GlobalScopeCreationParams,std::Cr::default_delete<blink::GlobalScopeCreationParams> >, const absl::optional<blink::WorkerBackingThreadStartupData> &, std::Cr::unique_ptr<blink::WorkerDevToolsParams,std::Cr::default_delete<blink::WorkerDevToolsParams> >),WTF::CrossThreadUnretainedWrapper<blink::WorkerThread>,std::Cr::unique_ptr<blink::GlobalScopeCreationParams,std::Cr::default_delete<blink::GlobalScopeCreationParams> >,absl::optional<blink::WorkerBackingThreadStartupData>,std::Cr::unique_ptr<blink::WorkerDevToolsParams,std::Cr::default_delete<blink::WorkerDevToolsParams> > >,void ()>::RunOnce D:\chromium\src\base\functional\bind_internal.h:871 #17 0x7ffd8731dde9 in base::TaskAnnotator::RunTaskImpl D:\chromium\src\base\task\common\task_annotator.cc:133 #18 0x7ffd873779ab in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:441 #19 0x7ffd873767fd in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:297 #20 0x7ffd871d60be in base::MessagePumpDefault::Run D:\chromium\src\base\message_loop\message_pump_default.cc:40 #21 0x7ffd87379fc1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:597 #22 0x7ffd8728dd3e in base::RunLoop::Run D:\chromium\src\base\run_loop.cc:141 #23 0x7ffd7ecb13f2 in content::`anonymous namespace'::NestedMessageLoopRunnerImpl::Run D:\chromium\src\content\child\blink\_platform\_impl.cc:87  

#24 0x7ffd4b776c1b in blink::WorkerThread::PauseOrFreezeOnWorkerThread D:\chromium\src\third\_party\blink\renderer\core\workers\worker\_thread.cc:902  

#25 0x7ffd4b77219b in blink::WorkerThread::PauseOrFreeze D:\chromium\src\third\_party\blink\renderer\core\workers\worker\_thread.cc:848  

#26 0x7ffd49d3a2fb in blink::WorkerThreadDebugger::runMessageLoopOnPause D:\chromium\src\third\_party\blink\renderer\core\inspector\worker\_thread\_debugger.cc:182  

#27 0x7ffd4b76e04a in blink::WorkerThread::InitializeOnWorkerThread D:\chromium\src\third\_party\blink\renderer\core\workers\worker\_thread.cc:667  

#28 0x7ffd4b777880 in base::internal::Invoker<base::internal::BindState<void (blink::WorkerThread::\*)(std::Cr::unique\_ptr<blink::GlobalScopeCreationParams,std::Cr::default\_delete[blink::GlobalScopeCreationParams](javascript:void(0);) >, const absl::optional[blink::WorkerBackingThreadStartupData](javascript:void(0);) &, std::Cr::unique\_ptr<blink::WorkerDevToolsParams,std::Cr::default\_delete[blink::WorkerDevToolsParams](javascript:void(0);) >),WTF::CrossThreadUnretainedWrapper[blink::WorkerThread](javascript:void(0);),std::Cr::unique\_ptr<blink::GlobalScopeCreationParams,std::Cr::default\_delete[blink::GlobalScopeCreationParams](javascript:void(0);) >,absl::optional[blink::WorkerBackingThreadStartupData](javascript:void(0);),std::Cr::unique\_ptr<blink::WorkerDevToolsParams,std::Cr::default\_delete[blink::WorkerDevToolsParams](javascript:void(0);) > >,void ()>::RunOnce D:\chromium\src\base\functional\bind\_internal.h:871  

#29 0x7ffd8731dde9 in base::TaskAnnotator::RunTaskImpl D:\chromium\src\base\task\common\task\_annotator.cc:133  

#30 0x7ffd873779ab in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl D:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:441  

#31 0x7ffd873767fd in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork D:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:297  

#32 0x7ffd871d60be in base::MessagePumpDefault::Run D:\chromium\src\base\message\_loop\message\_pump\_default.cc:40  

#33 0x7ffd87379d8d in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run D:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:600  

#34 0x7ffd8728dd3e in base::RunLoop::Run D:\chromium\src\base\run\_loop.cc:141  

#35 0x7ffd443fc74b in blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run D:\chromium\src\third\_party\blink\renderer\platform\scheduler\worker\non\_main\_thread\_impl.cc:173  

#36 0x7ffd874c2bf1 in base::`anonymous namespace'::ThreadFunc D:\chromium\src\base\threading\platform\_thread\_win.cc:134  

#37 0x7ffd866dbc23 in \_asan\_default\_suppressions\_\_dll+0x13c3 (D:\chromium\src\out\asan\clang\_rt.asan\_dynamic-x86\_64.dll+0x18004bc23)  

#38 0x7ffdcd6a7033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#39 0x7ffdcebc26a0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800526a0)

0x11fd92373ee8 is located 168 bytes inside of 312-byte region [0x11fd92373e40,0x11fd92373f78)  

freed by thread T0 here:  

#0 0x7ffd866dddfd in operator delete+0x8d (D:\chromium\src\out\asan\clang\_rt.asan\_dynamic-x86\_64.dll+0x18004ddfd)  

#1 0x7ffd3fb1486d in blink::SemiRealtimeAudioWorkletThread::~SemiRealtimeAudioWorkletThread D:\chromium\src\third\_party\blink\renderer\modules\webaudio\semi\_realtime\_audio\_worklet\_thread.cc:57  

#2 0x7ffd4b73a814 in blink::ThreadedMessagingProxyBase::WorkerThreadTerminated D:\chromium\src\third\_party\blink\renderer\core\workers\threaded\_messaging\_proxy\_base.cc:141  

#3 0x7ffd4b73fb72 in base::internal::InvokeHelper<1,void,0>::MakeItSo<void (blink::ThreadedMessagingProxyBase::\*)(),std::Cr::tuple<cppgc::internal::BasicCrossThreadPersistent[blink::ThreadedMessagingProxyBase,cppgc::internal::WeakCrossThreadPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy](javascript:void(0);) > > D:\chromium\src\base\functional\bind\_internal.h:848  

#4 0x7ffd4b73f944 in base::internal::Invoker<base::internal::BindState<void (blink::ThreadedMessagingProxyBase::\*)(),cppgc::internal::BasicCrossThreadPersistent[blink::ThreadedMessagingProxyBase,cppgc::internal::WeakCrossThreadPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy](javascript:void(0);) >,void ()>::RunOnce D:\chromium\src\base\functional\bind\_internal.h:871  

#5 0x7ffd8731dde9 in base::TaskAnnotator::RunTaskImpl D:\chromium\src\base\task\common\task\_annotator.cc:133  

#6 0x7ffd873779ab in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl D:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:441  

#7 0x7ffd873767fd in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork D:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:297  

#8 0x7ffd871d60be in base::MessagePumpDefault::Run D:\chromium\src\base\message\_loop\message\_pump\_default.cc:40  

#9 0x7ffd87379d8d in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run D:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:600  

#10 0x7ffd8728dd3e in base::RunLoop::Run D:\chromium\src\base\run\_loop.cc:141  

#11 0x7ffd822210e3 in content::RendererMain D:\chromium\src\content\renderer\renderer\_main.cc:313  

#12 0x7ffd82736f48 in content::RunOtherNamedProcessTypeMain D:\chromium\src\content\app\content\_main\_runner\_impl.cc:752  

#13 0x7ffd82739180 in content::ContentMainRunnerImpl::Run D:\chromium\src\content\app\content\_main\_runner\_impl.cc:1105  

#14 0x7ffd827348b0 in content::RunContentProcess D:\chromium\src\content\app\content\_main.cc:342  

#15 0x7ffd827354d0 in content::ContentMain D:\chromium\src\content\app\content\_main.cc:370  

#16 0x7ffd6a3214bd in ChromeMain D:\chromium\src\chrome\app\chrome\_main.cc:175  

#17 0x7ff7809f522a in MainDllLoader::Launch D:\chromium\src\chrome\app\main\_dll\_loader\_win.cc:166  

#18 0x7ff7809f295f in main D:\chromium\src\chrome\app\chrome\_exe\_main\_win.cc:395  

#19 0x7ff780caa4e7 in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#20 0x7ffdcd6a7033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#21 0x7ffdcebc26a0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800526a0)

previously allocated by thread T0 here:  

#0 0x7ffd866dd5dd in operator new+0x8d (D:\chromium\src\out\asan\clang\_rt.asan\_dynamic-x86\_64.dll+0x18004d5dd)  

#1 0x7ffd3fa8365e in blink::AudioWorkletMessagingProxy::CreateWorkletThreadWithConstraints D:\chromium\src\third\_party\blink\renderer\modules\webaudio\audio\_worklet\_messaging\_proxy.cc:115  

#2 0x7ffd3fa835f5 in blink::AudioWorkletMessagingProxy::CreateWorkerThread D:\chromium\src\third\_party\blink\renderer\modules\webaudio\audio\_worklet\_messaging\_proxy.cc:105  

#3 0x7ffd4b73967e in blink::ThreadedMessagingProxyBase::InitializeWorkerThread D:\chromium\src\third\_party\blink\renderer\core\workers\threaded\_messaging\_proxy\_base.cc:76  

#4 0x7ffd4b741459 in blink::ThreadedWorkletMessagingProxy::Initialize D:\chromium\src\third\_party\blink\renderer\core\workers\threaded\_worklet\_messaging\_proxy.cc:98  

#5 0x7ffd3fa6ddd7 in blink::AudioWorklet::CreateGlobalScope D:\chromium\src\third\_party\blink\renderer\modules\webaudio\audio\_worklet.cc:82  

#6 0x7ffd4b77e5a7 in blink::Worklet::FetchAndInvokeScript D:\chromium\src\third\_party\blink\renderer\core\workers\worklet.cc:168  

#7 0x7ffd4b782419 in base::internal::Invoker<base::internal::BindState<void (blink::Worklet::\*)(const blink::KURL &, const WTF::String &, blink::WorkletPendingTasks \*),cppgc::internal::BasicPersistent[blink::Worklet,cppgc::internal::StrongPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy](javascript:void(0);),blink::KURL,blink::V8RequestCredentials,cppgc::internal::BasicPersistent[blink::WorkletPendingTasks,cppgc::internal::StrongPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy](javascript:void(0);) >,void ()>::RunOnce D:\chromium\src\base\functional\bind\_internal.h:871  

#8 0x7ffd8731dde9 in base::TaskAnnotator::RunTaskImpl D:\chromium\src\base\task\common\task\_annotator.cc:133  

#9 0x7ffd873779ab in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl D:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:441  

#10 0x7ffd873767fd in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork D:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:297  

#11 0x7ffd871d60be in base::MessagePumpDefault::Run D:\chromium\src\base\message\_loop\message\_pump\_default.cc:40  

#12 0x7ffd87379d8d in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run D:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:600  

#13 0x7ffd8728dd3e in base::RunLoop::Run D:\chromium\src\base\run\_loop.cc:141  

#14 0x7ffd822210e3 in content::RendererMain D:\chromium\src\content\renderer\renderer\_main.cc:313  

#15 0x7ffd82736f48 in content::RunOtherNamedProcessTypeMain D:\chromium\src\content\app\content\_main\_runner\_impl.cc:752  

#16 0x7ffd82739180 in content::ContentMainRunnerImpl::Run D:\chromium\src\content\app\content\_main\_runner\_impl.cc:1105  

#17 0x7ffd827348b0 in content::RunContentProcess D:\chromium\src\content\app\content\_main.cc:342  

#18 0x7ffd827354d0 in content::ContentMain D:\chromium\src\content\app\content\_main.cc:370  

#19 0x7ffd6a3214bd in ChromeMain D:\chromium\src\chrome\app\chrome\_main.cc:175  

#20 0x7ff7809f522a in MainDllLoader::Launch D:\chromium\src\chrome\app\main\_dll\_loader\_win.cc:166  

#21 0x7ff7809f295f in main D:\chromium\src\chrome\app\chrome\_exe\_main\_win.cc:395  

#22 0x7ff780caa4e7 in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#23 0x7ffdcd6a7033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#24 0x7ffdcebc26a0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800526a0)

Thread T24 created by T0 here:  

#0 0x7ffd866dcdc2 in \_asan\_wrap\_CreateThread+0x62 (D:\chromium\src\out\asan\clang\_rt.asan\_dynamic-x86\_64.dll+0x18004cdc2)  

#1 0x7ffd874c1c6b in base::`anonymous namespace'::CreateThreadInternal D:\chromium\src\base\threading\platform\_thread\_win.cc:199  

#2 0x7ffd873faf2d in base::SimpleThread::StartAsync D:\chromium\src\base\threading\simple\_thread.cc:52  

#3 0x7ffd443fa881 in blink::NonMainThread::CreateThread D:\chromium\src\third\_party\blink\renderer\platform\scheduler\worker\non\_main\_thread\_impl.cc:36  

#4 0x7ffd4b74652d in blink::WorkerBackingThread::WorkerBackingThread D:\chromium\src\third\_party\blink\renderer\core\workers\worker\_backing\_thread.cc:59  

#5 0x7ffd3fb12e8a in blink::WorkletThreadHolder[blink::SemiRealtimeAudioWorkletThread](javascript:void(0);)::EnsureInstance D:\chromium\src\third\_party\blink\renderer\core\workers\worklet\_thread\_holder.h:36  

#6 0x7ffd3fb141cf in blink::SemiRealtimeAudioWorkletThread::SemiRealtimeAudioWorkletThread D:\chromium\src\third\_party\blink\renderer\modules\webaudio\semi\_realtime\_audio\_worklet\_thread.cc:53  

#7 0x7ffd3fa83684 in blink::AudioWorkletMessagingProxy::CreateWorkletThreadWithConstraints D:\chromium\src\third\_party\blink\renderer\modules\webaudio\audio\_worklet\_messaging\_proxy.cc:124  

#8 0x7ffd3fa835f5 in blink::AudioWorkletMessagingProxy::CreateWorkerThread D:\chromium\src\third\_party\blink\renderer\modules\webaudio\audio\_worklet\_messaging\_proxy.cc:105  

#9 0x7ffd4b73967e in blink::ThreadedMessagingProxyBase::InitializeWorkerThread D:\chromium\src\third\_party\blink\renderer\core\workers\threaded\_messaging\_proxy\_base.cc:76  

#10 0x7ffd4b741459 in blink::ThreadedWorkletMessagingProxy::Initialize D:\chromium\src\third\_party\blink\renderer\core\workers\threaded\_worklet\_messaging\_proxy.cc:98  

#11 0x7ffd3fa6ddd7 in blink::AudioWorklet::CreateGlobalScope D:\chromium\src\third\_party\blink\renderer\modules\webaudio\audio\_worklet.cc:82  

#12 0x7ffd4b77e5a7 in blink::Worklet::FetchAndInvokeScript D:\chromium\src\third\_party\blink\renderer\core\workers\worklet.cc:168  

#13 0x7ffd4b782419 in base::internal::Invoker<base::internal::BindState<void (blink::Worklet::\*)(const blink::KURL &, const WTF::String &, blink::WorkletPendingTasks \*),cppgc::internal::BasicPersistent[blink::Worklet,cppgc::internal::StrongPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy](javascript:void(0);),blink::KURL,blink::V8RequestCredentials,cppgc::internal::BasicPersistent[blink::WorkletPendingTasks,cppgc::internal::StrongPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy](javascript:void(0);) >,void ()>::RunOnce D:\chromium\src\base\functional\bind\_internal.h:871  

#14 0x7ffd8731dde9 in base::TaskAnnotator::RunTaskImpl D:\chromium\src\base\task\common\task\_annotator.cc:133  

#15 0x7ffd873779ab in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl D:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:441  

#16 0x7ffd873767fd in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork D:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:297  

#17 0x7ffd871d60be in base::MessagePumpDefault::Run D:\chromium\src\base\message\_loop\message\_pump\_default.cc:40  

#18 0x7ffd87379d8d in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run D:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:600  

#19 0x7ffd8728dd3e in base::RunLoop::Run D:\chromium\src\base\run\_loop.cc:141  

#20 0x7ffd822210e3 in content::RendererMain D:\chromium\src\content\renderer\renderer\_main.cc:313  

#21 0x7ffd82736f48 in content::RunOtherNamedProcessTypeMain D:\chromium\src\content\app\content\_main\_runner\_impl.cc:752  

#22 0x7ffd82739180 in content::ContentMainRunnerImpl::Run D:\chromium\src\content\app\content\_main\_runner\_impl.cc:1105  

#23 0x7ffd827348b0 in content::RunContentProcess D:\chromium\src\content\app\content\_main.cc:342  

#24 0x7ffd827354d0 in content::ContentMain D:\chromium\src\content\app\content\_main.cc:370  

#25 0x7ffd6a3214bd in ChromeMain D:\chromium\src\chrome\app\chrome\_main.cc:175  

#26 0x7ff7809f522a in MainDllLoader::Launch D:\chromium\src\chrome\app\main\_dll\_loader\_win.cc:166  

#27 0x7ff7809f295f in main D:\chromium\src\chrome\app\chrome\_exe\_main\_win.cc:395  

#28 0x7ff780caa4e7 in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#29 0x7ffdcd6a7033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#30 0x7ffdcebc26a0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800526a0)

SUMMARY: AddressSanitizer: heap-use-after-free D:\chromium\src\third\_party\blink\renderer\core\workers\worker\_thread.cc:905 in blink::WorkerThread::PauseOrFreezeOnWorkerThread  

Shadow bytes around the buggy address:  

0x11fd92373c00: 00 00 00 00 00 00 00 00 00 00 fa fa fa fa fa fa  

0x11fd92373c80: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x11fd92373d00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11fd92373d80: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa  

0x11fd92373e00: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

=>0x11fd92373e80: fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd fd  

0x11fd92373f00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x11fd92373f80: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x11fd92374000: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11fd92374080: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa  

0x11fd92374100: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

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

==2956==ABORTING

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.6 KB)
- [zero-outputs-check-processor.js](attachments/zero-outputs-check-processor.js) (text/plain, 2.3 KB)
- deleted (application/octet-stream, 0 B)
- [asan.txt](attachments/asan.txt) (text/plain, 21.2 KB)

## Timeline

### [Deleted User] (2022-10-08)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-10-08)

#RCA
WorkerThread owns global_scope_ through CrossThreadPersistent[1], 
but CrossThreadPersistent does not guarantee that global_scope_ is valid in some cases[2], 
such as thread termination causing UAF.

```

https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/workers/worker_thread.h;drc=8d399817282e3c12ed54eb23ec42a5e418298ec6;l=468
CrossThreadPersistent<WorkerOrWorkletGlobalScope> global_scope_;		<<[1]

https://source.chromium.org/chromium/chromium/src/+/main:v8/include/cppgc/cross-thread-persistent.h;drc=8d399817282e3c12ed54eb23ec42a5e418298ec6;l=18
// Wrapper around PersistentBase that allows accessing poisoned memory when
// using ASAN. This is needed as the GC of the heap that owns the value
// of a CTP, may clear it (heap termination, weakness) while the object		<<[2]
// holding the CTP may be poisoned as itself may be deemed dead.
class CrossThreadPersistentBase : public PersistentBase {

```

### an...@chromium.org (2022-10-08)

Not sure how to route this, using the catch-all V8 bucket.

[Monorail components: Blink>JavaScript]

### an...@chromium.org (2022-10-08)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-10-08)

Adding Blink as component as well as not sure if this a V8 issue specifically (based on instructions in V8 Issue triage -HOWTO)

[Monorail components: Blink]

### sa...@chromium.org (2022-10-10)

From what I understand, this issue is unrelated to V8, but adding mlippautz to double check.

### ml...@chromium.org (2022-10-10)

Looks like the worklet was already destroyed and the CTP may not be used anymore. Yet another instance of the CTP misuse.

haraken: Can you help triage this?

[Monorail components: -Blink>JavaScript Blink>GarbageCollection Blink>WebAudio Blink>Workers]

### an...@chromium.org (2022-10-10)

Assigned haraken@ as OWNER. 

### [Deleted User] (2022-10-10)

[Empty comment from Monorail migration]

### ha...@google.com (2022-10-11)

hongchan: This looks like WebAudio related. Would you take a look?


### [Deleted User] (2022-10-11)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-11)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-11)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ho...@chromium.org (2022-10-11)

[Empty comment from Monorail migration]

### ho...@chromium.org (2022-10-11)

Re: haraken@

The crashing location is in worker_thread.cc, when the global scope's BFCache setting is changed:
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/workers/worker_thread.cc;l=905

The reproduction is using WebAudio, but the crashing point is in the WorkerOrWorklet infra. Not entirely confident that our team can work on this fast.

Also mlippautz@ - can you elaborate on "Yet another instance of the CTP misuse"? Perhaps the CTP usage in the AudioWorklet infra is problematic?

### ho...@chromium.org (2022-10-11)

[Empty comment from Monorail migration]

### ho...@chromium.org (2022-10-11)

Never mind. I re-read https://crbug.com/chromium/1372695#c2 and https://crbug.com/chromium/1372695#c7. The said CTP is in worker_thread.h.

For the record, I tried a regular ASAN on linux with the following command (from asan.txt above), but it didn't even launch the browser:
ASAN_OPTIONS=detect_stack_use_after_return=true:disable_coredump=true:allocator_may_return_null=1:max_allocation_size_mb=256:dump_instruction_bytes=true:quarantine_size_mb=256:malloc_context_size=48:soft_rss_limit_mb=4096:detect_odr_violation=0

./out/asan/chrome --user-data-dir=~/tmp/ --no-sandbox --js-flags=--expose-gc --allow-natives-syntax --no-first-run --disable-in-process-stack-traces --enable-experimental-extension-apis --disable-translate --disable-breakpad --no-user-gesture-required --disable-gesture-requirement-for-media-playback --use-file-for-fake-audio-capture=test.wav --use-file-for-fake-video-capture=test.mjpeg --use-fake-device-for-media-stream --use-fake-ui-for-media-stream --enable-blink-test-features --allow-file-access-from-files --window-size=1024768 --enable-experimental-web-platform-features --no-default-browser-check --disable-extensions --autoplay-policy=no-user-gesture-required

I'll try node + puppeteer next.

### ho...@chromium.org (2022-10-12)

This is the result from Linux (node + puppeteer):

[1012/152813.330204:ERROR:elf_dynamic_array_reader.h(64)] tag not found
[1012/152813.331711:ERROR:elf_dynamic_array_reader.h(64)] tag not found
[1012/152813.353657:ERROR:file_io_posix.cc(144)] open /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq: No such file or directory (2)
[1012/152813.353886:ERROR:file_io_posix.cc(144)] open /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq: No such file or directory (2)
/usr/local/google/home/hongchan/Downloads/bugs/1372695/node_modules/puppeteer-core/lib/cjs/puppeteer/common/util.js:283
    const timeoutError = new Errors_js_1.TimeoutError(`waiting for ${taskName} failed: timeout ${timeout}ms exceeded`);
                         ^

TimeoutError: waiting for target failed: timeout 30000ms exceeded
    at waitWithTimeout (/usr/local/google/home/hongchan/Downloads/bugs/1372695/node_modules/puppeteer-core/lib/cjs/puppeteer/common/util.js:283:26)
    at CDPBrowser.waitForTarget (/usr/local/google/home/hongchan/Downloads/bugs/1372695/node_modules/puppeteer-core/lib/cjs/puppeteer/common/Browser.js:341:56)
    at ChromeLauncher.launch (/usr/local/google/home/hongchan/Downloads/bugs/1372695/node_modules/puppeteer-core/lib/cjs/puppeteer/node/ChromeLauncher.js:100:31)
    at async one_fuzzlop (/usr/local/google/home/hongchan/Downloads/bugs/1372695/ch.test.js:9:17)
    at async /usr/local/google/home/hongchan/Downloads/bugs/1372695/ch.test.js:101:3

Node.js v18.7.0

It looks like this needs a windows machine to repro properly.

### m....@gmail.com (2022-10-12)

[Comment Deleted]

### m....@gmail.com (2022-10-12)

Test ENV:
WIN10 x64
node v16.15.1
puppeteer-core@18.0.2

### ml...@chromium.org (2022-10-12)

#https://crbug.com/chromium/1372695#c15: Trying to answer on a high level as I didn't have time to dig into this yet. CTP does not protect against workers going away in general. In other words, holding a CTP does not prevent a thread from terminating. With workers there's usually a well known shutdown sequence so the chances of accessing an outdated CTP (the GC clears them racefully) doesn't happen. In case there's something off with a shutdown sequence, code may be accessing an oudated CTP which is either garbage or null, depending on timing.

### ho...@chromium.org (2022-10-12)

>  In case there's something off with a shutdown sequence, code may be accessing an oudated CTP which is either garbage or null, depending on timing.

I see. It looks like that's what's happening in the stack trace above. The said UAF occurs at where globalScope() is being touched after it's gone. The repro does create a worker, create an iframe inside, and then create an AudioContext and activate the AudioWorklet thread. Of course it shuts everything down and repeats.

Any advice on how to approach this problem would be appreciated!

### ml...@chromium.org (2022-10-12)

CTP relies on the fact that worker shutdown also shuts down everything that could access a CTP. Naively, I would say that worker shutdown also needs to shutdown anything related to AudioWorklet.

Does that help? I realize it's not very concrete advice but it's also not exactly what CTP was designed for.

### js...@google.com (2022-10-12)

[Empty comment from Monorail migration]

[Monorail components: -Blink]

### ho...@chromium.org (2022-10-12)

I am getting a different stack trace:

=================================================================
==27420==ERROR: AddressSanitizer: access-violation on unknown address 0x000000000264 (pc 0x7ffb89d1a89b bp 0x0016219f9670 sp 0x0016219f9590 T17)
==27420==The signal is caused by a READ memory access.
==27420==Hint: address points to the zero page.
fuzz->aft close:http://localhost:8000/poc.html tick->304889
fuzz->aft sleep2:http://localhost:8000/poc.html tick->306900
    #0 0x7ffb89d1a89a in blink::WorkerOrWorkletGlobalScope::SetDefersLoadingForResourceFetchers C:\chromium\src\third_party\blink\renderer\core\workers\worker_or_worklet_global_scope.cc:546
    #1 0x7ffb89d2b49d in blink::WorkerThread::PauseOrFreezeOnWorkerThread C:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:905
    #2 0x7ffb89d2694b in blink::WorkerThread::PauseOrFreeze C:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:849
    #3 0x7ffb882c6c6b in blink::WorkerThreadDebugger::runMessageLoopOnPause C:\chromium\src\third_party\blink\renderer\core\inspector\worker_thread_debugger.cc:182
    #4 0x7ffb89d227fa in blink::WorkerThread::InitializeOnWorkerThread C:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:668
    #5 0x7ffb89d2c030 in base::internal::Invoker<base::internal::BindState<void (blink::WorkerThread::*)(std::Cr::unique_ptr<blink::GlobalScopeCreationParams,std::Cr::default_delete<blink::GlobalScopeCreationParams> >, const absl::optional<blink::WorkerBackingThreadStartupData> &, std::Cr::unique_ptr<blink::WorkerDevToolsParams,std::Cr::default_delete<blink::WorkerDevToolsParams> >),WTF::CrossThreadUnretainedWrapper<blink::WorkerThread>,std::Cr::unique_ptr<blink::GlobalScopeCreationParams,std::Cr::default_delete<blink::GlobalScopeCreationParams> >,absl::optional<blink::WorkerBackingThreadStartupData>,std::Cr::unique_ptr<blink::WorkerDevToolsParams,std::Cr::default_delete<blink::WorkerDevToolsParams> > >,void ()>::RunOnce C:\chromium\src\base\functional\bind_internal.h:871
    #6 0x7ffbf663d9c9 in base::TaskAnnotator::RunTaskImpl C:\chromium\src\base\task\common\task_annotator.cc:133
    #7 0x7ffbf669758b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:441
    #8 0x7ffbf66963dd in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:297
    #9 0x7ffbf64f612e in base::MessagePumpDefault::Run C:\chromium\src\base\message_loop\message_pump_default.cc:40
    #10 0x7ffbf6699ba1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:597
    #11 0x7ffbf65addae in base::RunLoop::Run C:\chromium\src\base\run_loop.cc:141
    #12 0x7ffba39f13f2 in content::`anonymous namespace'::NestedMessageLoopRunnerImpl::Run C:\chromium\src\content\child\blink_platform_impl.cc:87
    #13 0x7ffb89d2b3cb in blink::WorkerThread::PauseOrFreezeOnWorkerThread C:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:903
    #14 0x7ffb89d2694b in blink::WorkerThread::PauseOrFreeze C:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:849
    #15 0x7ffb882c6c6b in blink::WorkerThreadDebugger::runMessageLoopOnPause C:\chromium\src\third_party\blink\renderer\core\inspector\worker_thread_debugger.cc:182
    #16 0x7ffb89d227fa in blink::WorkerThread::InitializeOnWorkerThread C:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:668
    #17 0x7ffb89d2c030 in base::internal::Invoker<base::internal::BindState<void (blink::WorkerThread::*)(std::Cr::unique_ptr<blink::GlobalScopeCreationParams,std::Cr::default_delete<blink::GlobalScopeCreationParams> >, const absl::optional<blink::WorkerBackingThreadStartupData> &, std::Cr::unique_ptr<blink::WorkerDevToolsParams,std::Cr::default_delete<blink::WorkerDevToolsParams> >),WTF::CrossThreadUnretainedWrapper<blink::WorkerThread>,std::Cr::unique_ptr<blink::GlobalScopeCreationParams,std::Cr::default_delete<blink::GlobalScopeCreationParams> >,absl::optional<blink::WorkerBackingThreadStartupData>,std::Cr::unique_ptr<blink::WorkerDevToolsParams,std::Cr::default_delete<blink::WorkerDevToolsParams> > >,void ()>::RunOnce C:\chromium\src\base\functional\bind_internal.h:871
    #18 0x7ffbf663d9c9 in base::TaskAnnotator::RunTaskImpl C:\chromium\src\base\task\common\task_annotator.cc:133
    #19 0x7ffbf669758b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:441
    #20 0x7ffbf66963dd in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:297
    #21 0x7ffbf64f612e in base::MessagePumpDefault::Run C:\chromium\src\base\message_loop\message_pump_default.cc:40
    #22 0x7ffbf6699ba1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:597
    #23 0x7ffbf65addae in base::RunLoop::Run C:\chromium\src\base\run_loop.cc:141
    #24 0x7ffba39f13f2 in content::`anonymous namespace'::NestedMessageLoopRunnerImpl::Run C:\chromium\src\content\child\blink_platform_impl.cc:87
    #25 0x7ffb89d2b3cb in blink::WorkerThread::PauseOrFreezeOnWorkerThread C:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:903
    #26 0x7ffb89d2694b in blink::WorkerThread::PauseOrFreeze C:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:849
    #27 0x7ffb882c6c6b in blink::WorkerThreadDebugger::runMessageLoopOnPause C:\chromium\src\third_party\blink\renderer\core\inspector\worker_thread_debugger.cc:182
    #28 0x7ffb89d227fa in blink::WorkerThread::InitializeOnWorkerThread C:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:668
    #29 0x7ffb89d2c030 in base::internal::Invoker<base::internal::BindState<void (blink::WorkerThread::*)(std::Cr::unique_ptr<blink::GlobalScopeCreationParams,std::Cr::default_delete<blink::GlobalScopeCreationParams> >, const absl::optional<blink::WorkerBackingThreadStartupData> &, std::Cr::unique_ptr<blink::WorkerDevToolsParams,std::Cr::default_delete<blink::WorkerDevToolsParams> >),WTF::CrossThreadUnretainedWrapper<blink::WorkerThread>,std::Cr::unique_ptr<blink::GlobalScopeCreationParams,std::Cr::default_delete<blink::GlobalScopeCreationParams> >,absl::optional<blink::WorkerBackingThreadStartupData>,std::Cr::unique_ptr<blink::WorkerDevToolsParams,std::Cr::default_delete<blink::WorkerDevToolsParams> > >,void ()>::RunOnce C:\chromium\src\base\functional\bind_internal.h:871
    #30 0x7ffbf663d9c9 in base::TaskAnnotator::RunTaskImpl C:\chromium\src\base\task\common\task_annotator.cc:133
    #31 0x7ffbf669758b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:441
    #32 0x7ffbf66963dd in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:297
    #33 0x7ffbf64f612e in base::MessagePumpDefault::Run C:\chromium\src\base\message_loop\message_pump_default.cc:40
    #34 0x7ffbf6699ba1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:597
    #35 0x7ffbf65addae in base::RunLoop::Run C:\chromium\src\base\run_loop.cc:141
    #36 0x7ffba39f13f2 in content::`anonymous namespace'::NestedMessageLoopRunnerImpl::Run C:\chromium\src\content\child\blink_platform_impl.cc:87
    #37 0x7ffb89d2b3cb in blink::WorkerThread::PauseOrFreezeOnWorkerThread C:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:903
    #38 0x7ffb89d2694b in blink::WorkerThread::PauseOrFreeze C:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:849
    #39 0x7ffb882c6c6b in blink::WorkerThreadDebugger::runMessageLoopOnPause C:\chromium\src\third_party\blink\renderer\core\inspector\worker_thread_debugger.cc:182
    #40 0x7ffb89d227fa in blink::WorkerThread::InitializeOnWorkerThread C:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:668
    #41 0x7ffb89d2c030 in base::internal::Invoker<base::internal::BindState<void (blink::WorkerThread::*)(std::Cr::unique_ptr<blink::GlobalScopeCreationParams,std::Cr::default_delete<blink::GlobalScopeCreationParams> >, const absl::optional<blink::WorkerBackingThreadStartupData> &, std::Cr::unique_ptr<blink::WorkerDevToolsParams,std::Cr::default_delete<blink::WorkerDevToolsParams> >),WTF::CrossThreadUnretainedWrapper<blink::WorkerThread>,std::Cr::unique_ptr<blink::GlobalScopeCreationParams,std::Cr::default_delete<blink::GlobalScopeCreationParams> >,absl::optional<blink::WorkerBackingThreadStartupData>,std::Cr::unique_ptr<blink::WorkerDevToolsParams,std::Cr::default_delete<blink::WorkerDevToolsParams> > >,void ()>::RunOnce C:\chromium\src\base\functional\bind_internal.h:871
    #42 0x7ffbf663d9c9 in base::TaskAnnotator::RunTaskImpl C:\chromium\src\base\task\common\task_annotator.cc:133
    #43 0x7ffbf669758b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:441
    #44 0x7ffbf66963dd in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:297
    #45 0x7ffbf64f612e in base::MessagePumpDefault::Run C:\chromium\src\base\message_loop\message_pump_default.cc:40
    #46 0x7ffbf6699ba1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:597
    #47 0x7ffbf65addae in base::RunLoop::Run C:\chromium\src\base\run_loop.cc:141
    #48 0x7ffba39f13f2 in content::`anonymous namespace'::NestedMessageLoopRunnerImpl::Run C:\chromium\src\content\child\blink_platform_impl.cc:87
    #49 0x7ffb89d2b3cb in blink::WorkerThread::PauseOrFreezeOnWorkerThread C:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:903
    #50 0x7ffb89d2694b in blink::WorkerThread::PauseOrFreeze C:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:849
    #51 0x7ffb882c6c6b in blink::WorkerThreadDebugger::runMessageLoopOnPause C:\chromium\src\third_party\blink\renderer\core\inspector\worker_thread_debugger.cc:182
    #52 0x7ffb89d227fa in blink::WorkerThread::InitializeOnWorkerThread C:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:668
    #53 0x7ffb89d2c030 in base::internal::Invoker<base::internal::BindState<void (blink::WorkerThread::*)(std::Cr::unique_ptr<blink::GlobalScopeCreationParams,std::Cr::default_delete<blink::GlobalScopeCreationParams> >, const absl::optional<blink::WorkerBackingThreadStartupData> &, std::Cr::unique_ptr<blink::WorkerDevToolsParams,std::Cr::default_delete<blink::WorkerDevToolsParams> >),WTF::CrossThreadUnretainedWrapper<blink::WorkerThread>,std::Cr::unique_ptr<blink::GlobalScopeCreationParams,std::Cr::default_delete<blink::GlobalScopeCreationParams> >,absl::optional<blink::WorkerBackingThreadStartupData>,std::Cr::unique_ptr<blink::WorkerDevToolsParams,std::Cr::default_delete<blink::WorkerDevToolsParams> > >,void ()>::RunOnce C:\chromium\src\base\functional\bind_internal.h:871
    #54 0x7ffbf663d9c9 in base::TaskAnnotator::RunTaskImpl C:\chromium\src\base\task\common\task_annotator.cc:133
    #55 0x7ffbf669758b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:441
    #56 0x7ffbf66963dd in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:297
    #57 0x7ffbf64f612e in base::MessagePumpDefault::Run C:\chromium\src\base\message_loop\message_pump_default.cc:40
    #58 0x7ffbf6699ba1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:597
    #59 0x7ffbf65addae in base::RunLoop::Run C:\chromium\src\base\run_loop.cc:141
    #60 0x7ffba39f13f2 in content::`anonymous namespace'::NestedMessageLoopRunnerImpl::Run C:\chromium\src\content\child\blink_platform_impl.cc:87
    #61 0x7ffb89d2b3cb in blink::WorkerThread::PauseOrFreezeOnWorkerThread C:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:903
    #62 0x7ffb89d2694b in blink::WorkerThread::PauseOrFreeze C:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:849
    #63 0x7ffb882c6c6b in blink::WorkerThreadDebugger::runMessageLoopOnPause C:\chromium\src\third_party\blink\renderer\core\inspector\worker_thread_debugger.cc:182
    #64 0x7ffb89d227fa in blink::WorkerThread::InitializeOnWorkerThread C:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:668
    #65 0x7ffb89d2c030 in base::internal::Invoker<base::internal::BindState<void (blink::WorkerThread::*)(std::Cr::unique_ptr<blink::GlobalScopeCreationParams,std::Cr::default_delete<blink::GlobalScopeCreationParams> >, const absl::optional<blink::WorkerBackingThreadStartupData> &, std::Cr::unique_ptr<blink::WorkerDevToolsParams,std::Cr::default_delete<blink::WorkerDevToolsParams> >),WTF::CrossThreadUnretainedWrapper<blink::WorkerThread>,std::Cr::unique_ptr<blink::GlobalScopeCreationParams,std::Cr::default_delete<blink::GlobalScopeCreationParams> >,absl::optional<blink::WorkerBackingThreadStartupData>,std::Cr::unique_ptr<blink::WorkerDevToolsParams,std::Cr::default_delete<blink::WorkerDevToolsParams> > >,void ()>::RunOnce C:\chromium\src\base\functional\bind_internal.h:871
    #66 0x7ffbf663d9c9 in base::TaskAnnotator::RunTaskImpl C:\chromium\src\base\task\common\task_annotator.cc:133
    #67 0x7ffbf669758b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:441
    #68 0x7ffbf66963dd in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:297
    #69 0x7ffbf64f612e in base::MessagePumpDefault::Run C:\chromium\src\base\message_loop\message_pump_default.cc:40
    #70 0x7ffbf6699ba1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:597
    #71 0x7ffbf65addae in base::RunLoop::Run C:\chromium\src\base\run_loop.cc:141
    #72 0x7ffba39f13f2 in content::`anonymous namespace'::NestedMessageLoopRunnerImpl::Run C:\chromium\src\content\child\blink_platform_impl.cc:87
    #73 0x7ffb89d2b3cb in blink::WorkerThread::PauseOrFreezeOnWorkerThread C:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:903
    #74 0x7ffb89d2694b in blink::WorkerThread::PauseOrFreeze C:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:849
    #75 0x7ffb882c6c6b in blink::WorkerThreadDebugger::runMessageLoopOnPause C:\chromium\src\third_party\blink\renderer\core\inspector\worker_thread_debugger.cc:182
    #76 0x7ffb89d227fa in blink::WorkerThread::InitializeOnWorkerThread C:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:668
    #77 0x7ffb89d2c030 in base::internal::Invoker<base::internal::BindState<void (blink::WorkerThread::*)(std::Cr::unique_ptr<blink::GlobalScopeCreationParams,std::Cr::default_delete<blink::GlobalScopeCreationParams> >, const absl::optional<blink::WorkerBackingThreadStartupData> &, std::Cr::unique_ptr<blink::WorkerDevToolsParams,std::Cr::default_delete<blink::WorkerDevToolsParams> >),WTF::CrossThreadUnretainedWrapper<blink::WorkerThread>,std::Cr::unique_ptr<blink::GlobalScopeCreationParams,std::Cr::default_delete<blink::GlobalScopeCreationParams> >,absl::optional<blink::WorkerBackingThreadStartupData>,std::Cr::unique_ptr<blink::WorkerDevToolsParams,std::Cr::default_delete<blink::WorkerDevToolsParams> > >,void ()>::RunOnce C:\chromium\src\base\functional\bind_internal.h:871
    #78 0x7ffbf663d9c9 in base::TaskAnnotator::RunTaskImpl C:\chromium\src\base\task\common\task_annotator.cc:133
    #79 0x7ffbf669758b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:441
    #80 0x7ffbf66963dd in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:297
    #81 0x7ffbf64f612e in base::MessagePumpDefault::Run C:\chromium\src\base\message_loop\message_pump_default.cc:40
    #82 0x7ffbf6699ba1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:597
    #83 0x7ffbf65addae in base::RunLoop::Run C:\chromium\src\base\run_loop.cc:141
    #84 0x7ffba39f13f2 in content::`anonymous namespace'::NestedMessageLoopRunnerImpl::Run C:\chromium\src\content\child\blink_platform_impl.cc:87
    #85 0x7ffb89d2b3cb in blink::WorkerThread::PauseOrFreezeOnWorkerThread C:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:903
    #86 0x7ffb89d2694b in blink::WorkerThread::PauseOrFreeze C:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:849
    #87 0x7ffb882c6c6b in blink::WorkerThreadDebugger::runMessageLoopOnPause C:\chromium\src\third_party\blink\renderer\core\inspector\worker_thread_debugger.cc:182
    #88 0x7ffb89d227fa in blink::WorkerThread::InitializeOnWorkerThread C:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:668
    #89 0x7ffb89d2c030 in base::internal::Invoker<base::internal::BindState<void (blink::WorkerThread::*)(std::Cr::unique_ptr<blink::GlobalScopeCreationParams,std::Cr::default_delete<blink::GlobalScopeCreationParams> >, const absl::optional<blink::WorkerBackingThreadStartupData> &, std::Cr::unique_ptr<blink::WorkerDevToolsParams,std::Cr::default_delete<blink::WorkerDevToolsParams> >),WTF::CrossThreadUnretainedWrapper<blink::WorkerThread>,std::Cr::unique_ptr<blink::GlobalScopeCreationParams,std::Cr::default_delete<blink::GlobalScopeCreationParams> >,absl::optional<blink::WorkerBackingThreadStartupData>,std::Cr::unique_ptr<blink::WorkerDevToolsParams,std::Cr::default_delete<blink::WorkerDevToolsParams> > >,void ()>::RunOnce C:\chromium\src\base\functional\bind_internal.h:871
    #90 0x7ffbf663d9c9 in base::TaskAnnotator::RunTaskImpl C:\chromium\src\base\task\common\task_annotator.cc:133
    #91 0x7ffbf669758b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:441
    #92 0x7ffbf66963dd in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:297
    #93 0x7ffbf64f612e in base::MessagePumpDefault::Run C:\chromium\src\base\message_loop\message_pump_default.cc:40
    #94 0x7ffbf6699ba1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:597
    #95 0x7ffbf65addae in base::RunLoop::Run C:\chromium\src\base\run_loop.cc:141
    #96 0x7ffba39f13f2 in content::`anonymous namespace'::NestedMessageLoopRunnerImpl::Run C:\chromium\src\content\child\blink_platform_impl.cc:87
    #97 0x7ffb89d2b3cb in blink::WorkerThread::PauseOrFreezeOnWorkerThread C:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:903
    #98 0x7ffb89d2694b in blink::WorkerThread::PauseOrFreeze C:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:849
    #99 0x7ffb882c6c6b in blink::WorkerThreadDebugger::runMessageLoopOnPause C:\chromium\src\third_party\blink\renderer\core\inspector\worker_thread_debugger.cc:182
    #100 0x7ffb89d227fa in blink::WorkerThread::InitializeOnWorkerThread C:\chromium\src\third_party\blink\renderer\core\workers\worker_thread.cc:668
    #101 0x7ffb89d2c030 in base::internal::Invoker<base::internal::BindState<void (blink::WorkerThread::*)(std::Cr::unique_ptr<blink::GlobalScopeCreationParams,std::Cr::default_delete<blink::GlobalScopeCreationParams> >, const absl::optional<blink::WorkerBackingThreadStartupData> &, std::Cr::unique_ptr<blink::WorkerDevToolsParams,std::Cr::default_delete<blink::WorkerDevToolsParams> >),WTF::CrossThreadUnretainedWrapper<blink::WorkerThread>,std::Cr::unique_ptr<blink::GlobalScopeCreationParams,std::Cr::default_delete<blink::GlobalScopeCreationParams> >,absl::optional<blink::WorkerBackingThreadStartupData>,std::Cr::unique_ptr<blink::WorkerDevToolsParams,std::Cr::default_delete<blink::WorkerDevToolsParams> > >,void ()>::RunOnce C:\chromium\src\base\functional\bind_internal.h:871
    #102 0x7ffbf663d9c9 in base::TaskAnnotator::RunTaskImpl C:\chromium\src\base\task\common\task_annotator.cc:133
    #103 0x7ffbf669758b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:441
    #104 0x7ffbf66963dd in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:297
    #105 0x7ffbf64f612e in base::MessagePumpDefault::Run C:\chromium\src\base\message_loop\message_pump_default.cc:40
    #106 0x7ffbf669996d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:600
    #107 0x7ffbf65addae in base::RunLoop::Run C:\chromium\src\base\run_loop.cc:141
    #108 0x7ffb8292999b in blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run C:\chromium\src\third_party\blink\renderer\platform\scheduler\worker\non_main_thread_impl.cc:173
    #109 0x7ffbf67e24a1 in base::`anonymous namespace'::ThreadFunc C:\chromium\src\base\threading\platform_thread_win.cc:134
    #110 0x7ffbc0cfbc23 in _asan_default_suppressions__dll+0x13c3 (C:\chromium\src\out\asan\clang_rt.asan_dynamic-x86_64.dll+0x18004bc23)
    #111 0x7ffc29b77033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)
    #112 0x7ffc2a5026a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

==27420==First 16 instruction bytes at pc: 8b 91 64 02 00 00 48 81 c1 60 02 00 00 48 8b 00
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: access-violation C:\chromium\src\third_party\blink\renderer\core\workers\worker_or_worklet_global_scope.cc:546 in blink::WorkerOrWorkletGlobalScope::SetDefersLoadingForResourceFetchers



At least it occurs at the same place: WorkerThread::PauseOrFreezeOnWorkerThread

It also took multiple iteration to cause the crash on ASAN. This will take a while.

### dt...@chromium.org (2022-10-12)

[Empty comment from Monorail migration]

### dt...@chromium.org (2022-10-12)

Would something like this work? I think WorkerThread is getting deallocated while on the stack but can't be released because it is in a nested event loop.

-    base::AutoReset<Platform::NestedMessageLoopRunner*> nested_runner_autoreset(
-        &nested_runner_, nested_runner.get());
+    auto weak_this = weak_factory_.GetWeakPtr();
+    nested_runner_ = nested_runner.get();
     nested_runner->Run();
+
+    // Careful `this` may be destroyed.
+    if (!weak_this) {
+      return;
+    }
+    nested_runner_ = nullptr;

### ho...@chromium.org (2022-10-12)

I tried https://crbug.com/chromium/1372695#c27 locally, and it seems to fix ASAN crashes at least. I don't see access violation anymore and the repro finishes 10 iterations without crashing:
https://chromium-review.googlesource.com/c/chromium/src/+/3951149

FWIW I haven't been able to repro UAF yet. All I've seen so far is access violation.

### m....@gmail.com (2022-10-13)

re https://crbug.com/chromium/1372695#c28 Because this is a conditional competition issue, it sometimes appears as a null pointer. In my local test, UAF usually occurs 1 to 2 times in 10 times.

### ho...@chromium.org (2022-10-13)

Re https://crbug.com/chromium/1372695#c29: Yes. That makes sense. We'll be trying out the patch in https://crbug.com/chromium/1372695#c28 and see how it goes.

### ml...@chromium.org (2022-10-13)

Indeed, we do reset the CTPs to nullptrs in raceful way. There's no way to make this a proper synchronization point with CTP and this is merely in place to aid debugging. The thinking was that a nullptr may be easier to debug than a wild pointer.

### dt...@chromium.org (2022-10-13)

I was thinking more like: https://chromium-review.googlesource.com/c/chromium/src/+/3953152

I think the problem in #28 is that the WeakPtrFactory is deallocated on not the worker backing thread.

### ho...@chromium.org (2022-10-13)

Okay then. I feel like now this is out of WebAudio's scope. I can assign to dtapuska@ since there is a well-formed CL already.

Thanks for your advice, dtapuska@ and mlippautz@!

### dt...@chromium.org (2022-10-13)

Fix is posted, waiting on review https://chromium-review.googlesource.com/c/chromium/src/+/3953152

### gi...@appspot.gserviceaccount.com (2022-10-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ff5696ba4bc0f8782e3de40e04685507d9f17fd2

commit ff5696ba4bc0f8782e3de40e04685507d9f17fd2
Author: Dave Tapuska <dtapuska@chromium.org>
Date: Fri Oct 14 21:53:45 2022

Fix PauseOrFreezeOnWorkerThread with nested Worklets.

Worklets can use the same backing thread which means we can have
nested WorkerThreads paused. If a parent WorkerThread gets deallocated
make sure we don't access anything after it is deallocated once the
nested event queue is released.

BUG=1372695

Change-Id: I176b8f750da5a41d19d1b3a623944d9a2ed4a441
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3953152
Commit-Queue: Dave Tapuska <dtapuska@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1059485}

[modify] https://crrev.com/ff5696ba4bc0f8782e3de40e04685507d9f17fd2/third_party/blink/renderer/core/workers/threaded_worklet_test.cc
[modify] https://crrev.com/ff5696ba4bc0f8782e3de40e04685507d9f17fd2/third_party/blink/renderer/core/workers/worker_thread.h
[modify] https://crrev.com/ff5696ba4bc0f8782e3de40e04685507d9f17fd2/third_party/blink/renderer/core/workers/worker_thread.cc


### dt...@chromium.org (2022-10-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-17)

Merge approved: your change passed merge requirements and is auto-approved for M108. Please go ahead and merge the CL to branch 5359 (refs/branch-heads/5359) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-17)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-10-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0b9d47a44986c6e0e47b978e48f2f6c5bff3bca4

commit 0b9d47a44986c6e0e47b978e48f2f6c5bff3bca4
Author: Dave Tapuska <dtapuska@chromium.org>
Date: Mon Oct 17 18:05:03 2022

[m108] Fix PauseOrFreezeOnWorkerThread with nested Worklets.

Worklets can use the same backing thread which means we can have
nested WorkerThreads paused. If a parent WorkerThread gets deallocated
make sure we don't access anything after it is deallocated once the
nested event queue is released.

BUG=1372695

(cherry picked from commit ff5696ba4bc0f8782e3de40e04685507d9f17fd2)

Change-Id: I176b8f750da5a41d19d1b3a623944d9a2ed4a441
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3953152
Commit-Queue: Dave Tapuska <dtapuska@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1059485}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3960430
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5359@{#26}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/0b9d47a44986c6e0e47b978e48f2f6c5bff3bca4/third_party/blink/renderer/core/workers/threaded_worklet_test.cc
[modify] https://crrev.com/0b9d47a44986c6e0e47b978e48f2f6c5bff3bca4/third_party/blink/renderer/core/workers/worker_thread.h
[modify] https://crrev.com/0b9d47a44986c6e0e47b978e48f2f6c5bff3bca4/third_party/blink/renderer/core/workers/worker_thread.cc


### am...@chromium.org (2022-10-24)

This issue appears to have been around since at least M106 if not farther back, updating FoundIn accordingly so that sheriffbot can update the SI and merge labels accordingly. 

### am...@chromium.org (2022-11-02)

Just now realizing now there was human intervention with merge labels in https://crbug.com/chromium/1372695#c36 so sheriffbot would not have intervened when I updated FoundIn last week; adding merge labels and updating SI accordingly so this can go into my the merge review queue for stable and extended stable 

### [Deleted User] (2022-11-02)

Merge review required: M107 is already shipping to stable.

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
Owners: govind (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-02)

Merge review required: M106 is already shipping to stable.

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
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-11-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-03)

Congratulations! The VRP Panel has decided to award you $7,000 for this report. Nice work! Thank you for your efforts in discovering and reporting this issue to us! 

### [Deleted User] (2022-11-03)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=1372695&entry.364066060=External&entry.958145677=Windows&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>GarbageCollection,Blink>WebAudio,Blink>Workers&entry.975983575=dtapuska@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-11-03)

107/stable and 106/extended merges approved, please merge this fix to branches 5304 and 5249 respectively so this fix can be included in the next 107/stable and 106/extended security refreshes

### gi...@appspot.gserviceaccount.com (2022-11-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f5265877233a6285fbce66f03686ab161c5135cb

commit f5265877233a6285fbce66f03686ab161c5135cb
Author: Dave Tapuska <dtapuska@chromium.org>
Date: Thu Nov 03 22:52:54 2022

[m107] Fix PauseOrFreezeOnWorkerThread with nested Worklets.

Worklets can use the same backing thread which means we can have
nested WorkerThreads paused. If a parent WorkerThread gets deallocated
make sure we don't access anything after it is deallocated once the
nested event queue is released.

BUG=1372695

(cherry picked from commit ff5696ba4bc0f8782e3de40e04685507d9f17fd2)

Change-Id: I176b8f750da5a41d19d1b3a623944d9a2ed4a441
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3953152
Commit-Queue: Dave Tapuska <dtapuska@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1059485}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4004560
Cr-Commit-Position: refs/branch-heads/5304@{#1161}
Cr-Branched-From: 5d7b1fc9cb7103d9c82eed647cf4be38cf09738b-refs/heads/main@{#1047731}

[modify] https://crrev.com/f5265877233a6285fbce66f03686ab161c5135cb/third_party/blink/renderer/core/workers/threaded_worklet_test.cc
[modify] https://crrev.com/f5265877233a6285fbce66f03686ab161c5135cb/third_party/blink/renderer/core/workers/worker_thread.h
[modify] https://crrev.com/f5265877233a6285fbce66f03686ab161c5135cb/third_party/blink/renderer/core/workers/worker_thread.cc


### gi...@appspot.gserviceaccount.com (2022-11-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ac4785387fff2efedef9fe784b5cb98bc1fecd04

commit ac4785387fff2efedef9fe784b5cb98bc1fecd04
Author: Dave Tapuska <dtapuska@chromium.org>
Date: Thu Nov 03 23:16:16 2022

[m106] Fix PauseOrFreezeOnWorkerThread with nested Worklets.

Worklets can use the same backing thread which means we can have
nested WorkerThreads paused. If a parent WorkerThread gets deallocated
make sure we don't access anything after it is deallocated once the
nested event queue is released.

BUG=1372695

(cherry picked from commit ff5696ba4bc0f8782e3de40e04685507d9f17fd2)

Change-Id: I176b8f750da5a41d19d1b3a623944d9a2ed4a441
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3953152
Commit-Queue: Dave Tapuska <dtapuska@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1059485}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4004562
Cr-Commit-Position: refs/branch-heads/5249@{#906}
Cr-Branched-From: 4f7bea5de862aaa52e6bde5920755a9ef9db120b-refs/heads/main@{#1036826}

[modify] https://crrev.com/ac4785387fff2efedef9fe784b5cb98bc1fecd04/third_party/blink/renderer/core/workers/threaded_worklet_test.cc
[modify] https://crrev.com/ac4785387fff2efedef9fe784b5cb98bc1fecd04/third_party/blink/renderer/core/workers/worker_thread.h
[modify] https://crrev.com/ac4785387fff2efedef9fe784b5cb98bc1fecd04/third_party/blink/renderer/core/workers/worker_thread.cc


### am...@google.com (2022-11-04)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-11-08)

[Empty comment from Monorail migration]

### am...@google.com (2022-11-08)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1372695?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>GarbageCollection, Blink>WebAudio, Blink>Workers]
[Monorail mergedwith: crbug.com/chromium/1372752]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061275)*
