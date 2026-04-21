# Security: heap-use-after-free worker_thread.cc:671 in blink::WorkerThread::InitializeOnWorkerThread

| Field | Value |
|-------|-------|
| **Issue ID** | [40063209](https://issues.chromium.org/issues/40063209) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Workers |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2023-02-23 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**  

heap-use-after-free worker\_thread.cc:671 in blink::WorkerThread::InitializeOnWorkerThread

**VERSION**  

WIN10 X64

asan-win32-release\_x64-1108236

**REPRODUCTION CASE**  

working on minipoc coming soon.

Type of crash: [tab]

#RCA  

coming soon

# #ASAN

==15820==ERROR: AddressSanitizer: heap-use-after-free on address 0x11f40384d450 at pc 0x7ffea97ef833 bp 0x006a795fedc0 sp 0x006a795fee08  

READ of size 8 at 0x11f40384d450 thread T40  

==15820==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ffea97ef832 in blink::WorkerThread::InitializeOnWorkerThread C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\workers\worker\_thread.cc:671  

#1 0x7ffea97f975f in base::internal::Invoker<base::internal::BindState<void (blink::WorkerThread::\*)(std::Cr::unique\_ptr<blink::GlobalScopeCreationParams,std::Cr::default\_delete[blink::GlobalScopeCreationParams](javascript:void(0);) >, const absl::optional[blink::WorkerBackingThreadStartupData](javascript:void(0);) &, std::Cr::unique\_ptr<blink::WorkerDevToolsParams,std::Cr::default\_delete[blink::WorkerDevToolsParams](javascript:void(0);) >),WTF::CrossThreadUnretainedWrapper[blink::WorkerThread](javascript:void(0);),std::Cr::unique\_ptr<blink::GlobalScopeCreationParams,std::Cr::default\_delete[blink::GlobalScopeCreationParams](javascript:void(0);) >,absl::optional[blink::WorkerBackingThreadStartupData](javascript:void(0);),std::Cr::unique\_ptr<blink::WorkerDevToolsParams,std::Cr::default\_delete[blink::WorkerDevToolsParams](javascript:void(0);) > >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:989  

#2 0x7ffe9bf1177a in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:165  

#3 0x7ffe9f38f7f8 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:490  

#4 0x7ffe9f38e2b3 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:340  

#5 0x7ffe9f3afbb3 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:48  

#6 0x7ffe9f392177 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:649  

#7 0x7ffe9bf8a471 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#8 0x7ffe99e7d0cb in blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\scheduler\worker\non\_main\_thread\_impl.cc:169  

#9 0x7ffe9be0b5c1 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:134  

#10 0x7ff63aaf5b53 in \_\_asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_thread.cpp:277  

#11 0x7fff0b0c7613 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017613)  

#12 0x7fff0bbe26a0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800526a0)

0x11f40384d450 is located 208 bytes inside of 352-byte region [0x11f40384d380,0x11f40384d4e0)  

freed by thread T0 here:  

#0 0x7ff63aaff04d in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ffeb0664a29 in blink::RealtimeAudioWorkletThread::~RealtimeAudioWorkletThread C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\webaudio\realtime\_audio\_worklet\_thread.cc:62  

#2 0x7ffead98d67e in blink::ThreadedMessagingProxyBase::WorkerThreadTerminated C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\workers\threaded\_messaging\_proxy\_base.cc:141  

#3 0x7ffeaf235610 in base::internal::InvokeHelper<1,void,0>::MakeItSo<void (blink::ThreadedMessagingProxyBase::\*)(),std::Cr::tuple<cppgc::internal::BasicCrossThreadPersistent[blink::ThreadedMessagingProxyBase,cppgc::internal::WeakCrossThreadPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy](javascript:void(0);) > > C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:966  

#4 0x7ffeaf2353e3 in base::internal::Invoker<base::internal::BindState<void (blink::ThreadedMessagingProxyBase::\*)(),cppgc::internal::BasicCrossThreadPersistent[blink::ThreadedMessagingProxyBase,cppgc::internal::WeakCrossThreadPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:989  

#5 0x7ffe9bf1177a in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:165  

#6 0x7ffe9f38f7f8 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:490  

#7 0x7ffe9f38e2b3 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:340  

#8 0x7ffe9f3afbb3 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:48  

#9 0x7ffe9f392177 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:649  

#10 0x7ffe9bf8a471 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#11 0x7ffe9ebf0c81 in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer\_main.cc:336  

#12 0x7ffe9a710dfa in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:761  

#13 0x7ffe9a713b93 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1135  

#14 0x7ffe9a70e8b4 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:335  

#15 0x7ffe9a70f504 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:363  

#16 0x7ffe8ec81699 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:190  

#17 0x7ff63aa46378 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:166  

#18 0x7ff63aa42bb1 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:390  

#19 0x7ff63ae68f5b in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#20 0x7fff0b0c7613 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017613)  

#21 0x7fff0bbe26a0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800526a0)

previously allocated by thread T0 here:  

#0 0x7ff63aaff14d in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffeb18cd71e in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ffeaf9cb442 in blink::AudioWorkletMessagingProxy::CreateWorkletThreadWithConstraints C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\webaudio\audio\_worklet\_messaging\_proxy.cc:115  

#3 0x7ffeaf9cb3d9 in blink::AudioWorkletMessagingProxy::CreateWorkerThread C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\webaudio\audio\_worklet\_messaging\_proxy.cc:105  

#4 0x7ffead98c519 in blink::ThreadedMessagingProxyBase::InitializeWorkerThread C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\workers\threaded\_messaging\_proxy\_base.cc:76  

#5 0x7ffeaf73cbd6 in blink::ThreadedWorkletMessagingProxy::Initialize C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\workers\threaded\_worklet\_messaging\_proxy.cc:98  

#6 0x7ffeaf9a0863 in blink::AudioWorklet::CreateGlobalScope C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\webaudio\audio\_worklet.cc:82  

#7 0x7ffeaa525736 in blink::Worklet::FetchAndInvokeScript C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\workers\worklet.cc:168  

#8 0x7ffeaa529567 in base::internal::Invoker<base::internal::BindState<void (blink::Worklet::\*)(const blink::KURL &, const WTF::String &, blink::WorkletPendingTasks \*),cppgc::internal::BasicPersistent[blink::Worklet,cppgc::internal::StrongPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy](javascript:void(0);),blink::KURL,blink::V8RequestCredentials,cppgc::internal::BasicPersistent[blink::WorkletPendingTasks,cppgc::internal::StrongPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:989  

#9 0x7ffe9bf1177a in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:165  

#10 0x7ffe9f38f7f8 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:490  

#11 0x7ffe9f38e2b3 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:340  

#12 0x7ffe9f3afbb3 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:48  

#13 0x7ffe9f392177 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:649  

#14 0x7ffe9bf8a471 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#15 0x7ffe9ebf0c81 in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer\_main.cc:336  

#16 0x7ffe9a710dfa in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:761  

#17 0x7ffe9a713b93 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1135  

#18 0x7ffe9a70e8b4 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:335  

#19 0x7ffe9a70f504 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:363  

#20 0x7ffe8ec81699 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:190  

#21 0x7ff63aa46378 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:166  

#22 0x7ff63aa42bb1 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:390  

#23 0x7ff63ae68f5b in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#24 0x7fff0b0c7613 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017613)  

#25 0x7fff0bbe26a0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800526a0)

Thread T40 created by T0 here:  

#0 0x7ff63aaf4632 in \_\_asan\_wrap\_CreateThread C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_win.cpp:146  

#1 0x7ffe9be0a3bf in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:199  

#2 0x7ffe9beb6519 in base::SimpleThread::StartAsync C:\b\s\w\ir\cache\builder\src\base\threading\simple\_thread.cc:54  

#3 0x7ffe99e7b0b8 in blink::NonMainThread::CreateThread C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\scheduler\worker\non\_main\_thread\_impl.cc:36  

#4 0x7ffea74c218b in blink::WorkerBackingThread::WorkerBackingThread C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\workers\worker\_backing\_thread.cc:59  

#5 0x7ffeb0662d94 in blink::WorkletThreadHolder[blink::RealtimeAudioWorkletThread](javascript:void(0);)::EnsureInstance C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\workers\worklet\_thread\_holder.h:36  

#6 0x7ffeb0664294 in blink::RealtimeAudioWorkletThread::RealtimeAudioWorkletThread C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\webaudio\realtime\_audio\_worklet\_thread.cc:58  

#7 0x7ffeaf9cb45a in blink::AudioWorkletMessagingProxy::CreateWorkletThreadWithConstraints C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\webaudio\audio\_worklet\_messaging\_proxy.cc:121  

#8 0x7ffeaf9cb3d9 in blink::AudioWorkletMessagingProxy::CreateWorkerThread C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\webaudio\audio\_worklet\_messaging\_proxy.cc:105  

#9 0x7ffead98c519 in blink::ThreadedMessagingProxyBase::InitializeWorkerThread C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\workers\threaded\_messaging\_proxy\_base.cc:76  

#10 0x7ffeaf73cbd6 in blink::ThreadedWorkletMessagingProxy::Initialize C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\workers\threaded\_worklet\_messaging\_proxy.cc:98  

#11 0x7ffeaf9a0863 in blink::AudioWorklet::CreateGlobalScope C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\webaudio\audio\_worklet.cc:82  

#12 0x7ffeaa525736 in blink::Worklet::FetchAndInvokeScript C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\workers\worklet.cc:168  

#13 0x7ffeaa529567 in base::internal::Invoker<base::internal::BindState<void (blink::Worklet::\*)(const blink::KURL &, const WTF::String &, blink::WorkletPendingTasks \*),cppgc::internal::BasicPersistent[blink::Worklet,cppgc::internal::StrongPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy](javascript:void(0);),blink::KURL,blink::V8RequestCredentials,cppgc::internal::BasicPersistent[blink::WorkletPendingTasks,cppgc::internal::StrongPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:989  

#14 0x7ffe9bf1177a in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:165  

#15 0x7ffe9f38f7f8 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:490  

#16 0x7ffe9f38e2b3 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:340  

#17 0x7ffe9f3afbb3 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:48  

#18 0x7ffe9f392177 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:649  

#19 0x7ffe9bf8a471 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#20 0x7ffe9ebf0c81 in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer\_main.cc:336  

#21 0x7ffe9a710dfa in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:761  

#22 0x7ffe9a713b93 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1135  

#23 0x7ffe9a70e8b4 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:335  

#24 0x7ffe9a70f504 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:363  

#25 0x7ffe8ec81699 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:190  

#26 0x7ff63aa46378 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:166  

#27 0x7ff63aa42bb1 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:390  

#28 0x7ff63ae68f5b in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#29 0x7fff0b0c7613 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017613)  

#30 0x7fff0bbe26a0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800526a0)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\workers\worker\_thread.cc:671 in blink::WorkerThread::InitializeOnWorkerThread  

Shadow bytes around the buggy address:  

0x11f40384d180: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x11f40384d200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11f40384d280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11f40384d300: fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x11f40384d380: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x11f40384d400: fd fd fd fd fd fd fd fd fd fd[fd]fd fd fd fd fd  

0x11f40384d480: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa  

0x11f40384d500: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x11f40384d580: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11f40384d600: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11f40384d680: fd fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 17.8 KB)
- [dummy-processor-globalthis.js](attachments/dummy-processor-globalthis.js) (text/plain, 253 B)
- [load.js](attachments/load.js) (text/plain, 4.4 KB)
- [poc3.html](attachments/poc3.html) (text/plain, 560 B)

## Timeline

### [Deleted User] (2023-02-23)

[Empty comment from Monorail migration]

### m....@gmail.com (2023-02-23)

#RCA
Same as this one https://bugs.chromium.org/p/chromium/issues/detail?id=1372695

WorkerThread owns global_scope_ through CrossThreadPersistent[1], 
but CrossThreadPersistent does not guarantee that global_scope_ is valid in some cases[2], 
such as thread termination causing UAF.

```
void WorkerThread::Start(
    std::unique_ptr<GlobalScopeCreationParams> global_scope_creation_params,
    const absl::optional<WorkerBackingThreadStartupData>& thread_startup_data,
    std::unique_ptr<WorkerDevToolsParams> devtools_params) {
  DCHECK_CALLED_ON_VALID_THREAD(parent_thread_checker_);
  devtools_worker_token_ = devtools_params->devtools_worker_token;

...CUT...
  PostCrossThreadTask(
      *GetWorkerBackingThread().BackingThread().GetTaskRunner(), FROM_HERE,
      CrossThreadBindOnce(&WorkerThread::InitializeOnWorkerThread,
                          CrossThreadUnretained(this),						<<[1]
                          std::move(global_scope_creation_params),
                          thread_startup_data, std::move(devtools_params)));
}


https://source.chromium.org/chromium/chromium/src/+/main:v8/include/cppgc/cross-thread-persistent.h;drc=8d399817282e3c12ed54eb23ec42a5e418298ec6;l=18
// Wrapper around PersistentBase that allows accessing poisoned memory when
// using ASAN. This is needed as the GC of the heap that owns the value
// of a CTP, may clear it (heap termination, weakness) while the object		<<[2]
// holding the CTP may be poisoned as itself may be deemed dead.
class CrossThreadPersistentBase : public PersistentBase {


```

### sr...@google.com (2023-02-23)

Thanks! You said you're working on a poc to share right? Marking as Needs-Feedback until then.

### m....@gmail.com (2023-02-24)

install node
install puppeteer-core
node load.js chrome_bin_path http://localhost/poc3.html

--single-process can make minipoc more stable and reproducible, it's not an indispensable condition

The problem may crash at other points, ch.test will cycle the test ten times to ensure that the UAF problem occurs steadily


### [Deleted User] (2023-02-24)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### m....@gmail.com (2023-02-24)

Introduce by this CL

https://chromium-review.googlesource.com/c/chromium/src/+/4073064
Canary 112 112.0.5602.0

stable not affect

Also the poc provided by https://crbug.com/chromium/1372695 can also trigger this UAF.
https://bugs.chromium.org/p/chromium/issues/detail?id=1372695


### sr...@google.com (2023-02-25)

[Empty comment from Monorail migration]

[Monorail components: Blink>Workers]

### [Deleted User] (2023-02-25)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-25)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-25)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2023-02-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-03-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/55833c5dfa38b94859bf6bc41b6aa43e4ebc6ddb

commit 55833c5dfa38b94859bf6bc41b6aa43e4ebc6ddb
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Thu Mar 02 21:24:46 2023

Move GlobalScope::WillBeginLoading() call to locked section of InitializeOnWorkerThread

Bug: 1418561
Change-Id: I03cd6a8fee3bfbc139b63e1c96e7f63092074c61
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4300139
Reviewed-by: Nate Chapin <japhet@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1112437}

[modify] https://crrev.com/55833c5dfa38b94859bf6bc41b6aa43e4ebc6ddb/third_party/blink/renderer/core/workers/worker_thread.cc


### ca...@chromium.org (2023-03-03)

 m.cooolie@, I couldn't reproduce the failure locally unfortunately, so the fix is somewhat specualtive. May I ask you to verify that the fix works in your environment?


### [Deleted User] (2023-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-03)

Requesting merge to dev M112 because latest trunk commit (1112437) appears to be after dev branch point (1109224).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-03)

Merge approved: your change passed merge requirements and is auto-approved for M112. Please go ahead and merge the CL to branch 5615 (refs/branch-heads/5615) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), govind (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### m....@gmail.com (2023-03-04)

tested on asan-win32-release_x64-1113104 no longer reproduce

### [Deleted User] (2023-03-04)

[Empty comment from Monorail migration]

### ca...@chromium.org (2023-03-06)

m.cooolie@, thank you very much!

### gi...@appspot.gserviceaccount.com (2023-03-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c95a6e3d4d2ccc9c493213473016f11f5b94f4d3

commit c95a6e3d4d2ccc9c493213473016f11f5b94f4d3
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Tue Mar 07 01:39:07 2023

[m112] Move GlobalScope::WillBeginLoading() call to locked section of InitializeOnWorkerThread

(cherry picked from commit 55833c5dfa38b94859bf6bc41b6aa43e4ebc6ddb)

Bug: 1418561
Change-Id: I03cd6a8fee3bfbc139b63e1c96e7f63092074c61
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4300139
Reviewed-by: Nate Chapin <japhet@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1112437}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4313062
Cr-Commit-Position: refs/branch-heads/5615@{#251}
Cr-Branched-From: 9c6408ef696e83a9936b82bbead3d41c93c82ee4-refs/heads/main@{#1109224}

[modify] https://crrev.com/c95a6e3d4d2ccc9c493213473016f11f5b94f4d3/third_party/blink/renderer/core/workers/worker_thread.cc


### [Deleted User] (2023-03-07)

LTS Milestone M108

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-03-07)

WillBeginLoading() isn't called after WaitForDebuggerIfNeeded() in 102/108

### am...@google.com (2023-03-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-09)

Congratulations! The VRP Panel has decided to award you $7,000 for this report + $1,000 bisect bonus. Thank you for your efforts in discovering and reporting this issue to us -- nice work! 

### am...@google.com (2023-03-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1418561?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063209)*
