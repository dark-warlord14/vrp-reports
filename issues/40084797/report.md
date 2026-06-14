# Security: Arbitrary memory write in v8::internal::GlobalHandles::IterateNewSpaceWeakUnmodifiedRoots()

| Field | Value |
|-------|-------|
| **Issue ID** | [40084797](https://issues.chromium.org/issues/40084797) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>GarbageCollection |
| **Platforms** | Linux, Windows |
| **Reporter** | lo...@gmail.com |
| **Assignee** | ha...@chromium.org |
| **Created** | 2016-07-09 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Steps to reproduce:

```
1.Open repro UAP_IterateNewSpaceWeakUnmodifiedRoots_Repro.html in Chrome browser ASAN build.  
2. ASAN reports a use-after-poison in v8::internal::GlobalHandles::IterateNewSpaceWeakUnmodifiedRoots():  

	==278300==ERROR: AddressSanitizer: use-after-poison on address 0x0dc959a0 at pc 0x82689225 bp 0xdeadbeef sp 0x049fc92c  
	WRITE of size 4 at 0x0dc959a0 thread T0  

```

**VERSION**  

Chrome Version: 54.0.2790.0 (Developer Build) (32-bit)  

<https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/win32-release%2Fasan-coverage-win32-release-403906.zip?generation=1467827800967000&alt=media>

```
Operating System: Windows 10  

```

**REPRODUCTION CASE**  

UAP\_IterateNewSpaceWeakUnmodifiedRoots\_Repro.html.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

=================================================================  

==246068==ERROR: AddressSanitizer: use-after-poison on address 0x5857eb90 at pc 0x82689225 bp 0xdeadbeef sp 0x0116cb2c  

WRITE of size 4 at 0x5857eb90 thread T0  

#0 0x82689224 in v8::internal::GlobalHandles::IterateNewSpaceWeakUnmodifiedRoots+0x3c4 (E:\ChromeBuilds\asan-win32-release-403906\chrome\_child.dll+0x2699224)  

#1 0x8cd88036 in v8::internal::Heap::Scavenge+0x44c6 (E:\ChromeBuilds\asan-win32-release-403906\chrome\_child.dll+0xcd98036)  

#2 0x8cd7e9db in v8::internal::Heap::PerformGarbageCollection+0x104b (E:\ChromeBuilds\asan-win32-release-403906\chrome\_child.dll+0xcd8e9db)  

#3 0x8cd7be52 in v8::internal::Heap::CollectGarbage+0x792 (E:\ChromeBuilds\asan-win32-release-403906\chrome\_child.dll+0xcd8be52)  

#4 0x8f18923b in v8::internal::ScavengeJob::IdleTask::RunInternal+0x2bb (E:\ChromeBuilds\asan-win32-release-403906\chrome\_child.dll+0xf19923b)  

#5 0x8e280c54 in scheduler::WebSchedulerImpl::runIdleTask+0x104 (E:\ChromeBuilds\asan-win32-release-403906\chrome\_child.dll+0xe290c54)  

#6 0x8e261cc5 in base::internal::FunctorTraits<void (\_\_cdecl\*)(std::unique\_ptr<blink::WebThread::IdleTask,std::default\_delete[blink::WebThread::IdleTask](javascript:void(0);) >,base::TimeTicks)>::Invoke<std::unique\_ptr<blink::WebThread::IdleTask,std::default\_delete[blink::WebThread::IdleTask](javascript:void(0);) >,base::TimeTicks>+0xc5 (E:\ChromeBuilds\asan-win32-release-403906\chrome\_child.dll+0xe271cc5)  

#7 0x8e2619db in base::internal::Invoker<base::internal::BindState<void (\_\_cdecl\*)(std::unique\_ptr<blink::WebThread::IdleTask,std::default\_delete[blink::WebThread::IdleTask](javascript:void(0);) >,base::TimeTicks),base::internal::PassedWrapper<std::unique\_ptr<blink::WebThread::IdleTask,std::default\_delete[blink::WebThread::IdleTask](javascript:void(0);) > > >,void \_\_cdecl(base::TimeTicks)>::Run+0x14b (E:\ChromeBuilds\asan-win32-release-403906\chrome\_child.dll+0xe2719db)  

#8 0x8e283d70 in scheduler::SingleThreadIdleTaskRunner::RunTask+0x430 (E:\ChromeBuilds\asan-win32-release-403906\chrome\_child.dll+0xe293d70)  

#9 0x8e284ec4 in base::internal::FunctorTraits<void (\_\_thiscall scheduler::SingleThreadIdleTaskRunner::\*)(base::Callback<void \_\_cdecl(base::TimeTicks),1>)>::Invoke<base::WeakPtr[scheduler::SingleThreadIdleTaskRunner](javascript:void(0);),base::Callback<void \_\_cdecl(base::TimeTicks),1> const &>+0x74 (E:\ChromeBuilds\asan-win32-release-403906\chrome\_child.dll+0xe294ec4)  

#10 0x8e284cd2 in base::internal::Invoker<base::internal::BindState<void (\_\_thiscall scheduler::SingleThreadIdleTaskRunner::\*)(base::Callback<void \_\_cdecl(base::TimeTicks),1>),base::WeakPtr[scheduler::SingleThreadIdleTaskRunner](javascript:void(0);),base::Callback<void \_\_cdecl(base::TimeTicks),1> >,void \_\_cdecl(void)>::RunImpl<void (\_\_thiscall scheduler::SingleThreadIdleTaskRunner::\*const &)(base::Callback<void \_\_cdecl(base::TimeTicks),1>),std::tuple<base::WeakPtr[scheduler::SingleThreadIdleTaskRunner](javascript:void(0);),base::Callback<void \_\_cdecl(base::TimeTicks),1> > const &,0,1>+0x1c2 (E:\ChromeBuilds\asan-win32-release-403906\chrome\_child.dll+0xe294cd2)  

#11 0x8e284ac0 in base::internal::Invoker<base::internal::BindState<void (\_\_thiscall scheduler::SingleThreadIdleTaskRunner::\*)(base::Callback<void \_\_cdecl(base::TimeTicks),1>),base::WeakPtr[scheduler::SingleThreadIdleTaskRunner](javascript:void(0);),base::Callback<void \_\_cdecl(base::TimeTicks),1> >,void \_\_cdecl(void)>::Run+0x80 (E:\ChromeBuilds\asan-win32-release-403906\chrome\_child.dll+0xe294ac0)  

#12 0x805e34c1 in base::debug::TaskAnnotator::RunTask+0x3f1 (E:\ChromeBuilds\asan-win32-release-403906\chrome\_child.dll+0x5f34c1)  

#13 0x8e2ac183 in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue+0x993 (E:\ChromeBuilds\asan-win32-release-403906\chrome\_child.dll+0xe2bc183)  

#14 0x8e2a6bdb in scheduler::TaskQueueManager::DoWork+0x54b (E:\ChromeBuilds\asan-win32-release-403906\chrome\_child.dll+0xe2b6bdb)  

#15 0x8e2b3962 in base::internal::Invoker<base::internal::BindState<void (\_\_thiscall scheduler::TaskQueueManager::\*)(base::TimeTicks,bool),base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);),base::TimeTicks,bool>,void \_\_cdecl(void)>::RunImpl<void (\_\_thiscall scheduler::TaskQueueManager::\*const &)(base::TimeTicks,bool),std::tuple<base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);),base::TimeTicks,bool> const &,0,1,2>+0x222 (E:\ChromeBuilds\asan-win32-release-403906\chrome\_child.dll+0xe2c3962)  

#16 0x8e2b36f0 in base::internal::Invoker<base::internal::BindState<void (\_\_thiscall scheduler::TaskQueueManager::\*)(base::TimeTicks,bool),base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);),base::TimeTicks,bool>,void \_\_cdecl(void)>::Run+0x80 (E:\ChromeBuilds\asan-win32-release-403906\chrome\_child.dll+0xe2c36f0)  

#17 0x805e34c1 in base::debug::TaskAnnotator::RunTask+0x3f1 (E:\ChromeBuilds\asan-win32-release-403906\chrome\_child.dll+0x5f34c1)  

#18 0x8049f43b in base::MessageLoop::RunTask+0x6eb (E:\ChromeBuilds\asan-win32-release-403906\chrome\_child.dll+0x4af43b)  

#19 0x804a12c5 in base::MessageLoop::DoWork+0x675 (E:\ChromeBuilds\asan-win32-release-403906\chrome\_child.dll+0x4b12c5)  

#20 0x805ec1f8 in base::MessagePumpDefault::Run+0x378 (E:\ChromeBuilds\asan-win32-release-403906\chrome\_child.dll+0x5fc1f8)  

#21 0x8049e4b5 in base::MessageLoop::RunHandler+0x45 (E:\ChromeBuilds\asan-win32-release-403906\chrome\_child.dll+0x4ae4b5)  

#22 0x805ec86f in base::RunLoop::Run+0x1df (E:\ChromeBuilds\asan-win32-release-403906\chrome\_child.dll+0x5fc86f)  

#23 0x874cde47 in content::RendererMain+0x567 (E:\ChromeBuilds\asan-win32-release-403906\chrome\_child.dll+0x74dde47)  

#24 0x8035e907 in content::RunNamedProcessTypeMain+0x557 (E:\ChromeBuilds\asan-win32-release-403906\chrome\_child.dll+0x36e907)  

#25 0x80360836 in content::ContentMainRunnerImpl::Run+0x2c6 (E:\ChromeBuilds\asan-win32-release-403906\chrome\_child.dll+0x370836)  

#26 0x8035da24 in content::ContentMain+0x74 (E:\ChromeBuilds\asan-win32-release-403906\chrome\_child.dll+0x36da24)  

#27 0x7fff1130 in ChromeMain+0x130 (E:\ChromeBuilds\asan-win32-release-403906\chrome\_child.dll+0x1130)  

#28 0x124cba5 in MainDllLoader::Launch+0x485 (E:\ChromeBuilds\asan-win32-release-403906\chrome.exe+0xcba5)  

#29 0x1242589 in main+0x1299 (E:\ChromeBuilds\asan-win32-release-403906\chrome.exe+0x2589)  

#30 0x2828a6c in \_\_scrt\_common\_main\_seh f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl:255  

#31 0x749d38f3 in BaseThreadInitThunk+0x23 (C:\WINDOWS\SYSTEM32\KERNEL32.DLL+0x138f3)  

#32 0x77cb5de2 in RtlUnicodeStringToInteger+0x252 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x65de2)  

#33 0x77cb5dad in RtlUnicodeStringToInteger+0x21d (C:\WINDOWS\SYSTEM32\ntdll.dll+0x65dad)

AddressSanitizer can not describe address in more detail (wild memory access suspected).  

SUMMARY: AddressSanitizer: use-after-poison (E:\ChromeBuilds\asan-win32-release-403906\chrome\_child.dll+0x2699224) in v8::internal::GlobalHandles::IterateNewSpaceWeakUnmodifiedRoots+0x3c4  

Shadow bytes around the buggy address:  

0x3b0afd20: 00 00 00 00 00 00 00 00 00 04 00 00 00 00 00 00  

0x3b0afd30: 00 00 00 00 00 00 00 04 f7 f7 f7 f7 f7 f7 f7 f7  

0x3b0afd40: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x3b0afd50: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x3b0afd60: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

=>0x3b0afd70: f7 f7[f7]f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 00 00 00  

0x3b0afd80: 00 00 00 00 00 00 00 04 f7 f7 f7 f7 f7 f7 f7 f7  

0x3b0afd90: f7 00 00 00 00 00 00 00 00 00 00 00 04 00 00 00  

0x3b0afda0: 00 00 00 00 00 00 00 00 00 04 00 00 00 00 00 00  

0x3b0afdb0: 00 00 04 00 00 00 00 00 00 00 00 00 00 04 f7 f7  

0x3b0afdc0: f7 f7 f7 f7 f7 f7 f7 f7 f7 00 00 00 00 00 00 00  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Heap right redzone: fb  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack partial redzone: f4  

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

==246068==ABORTING

## Attachments

- [UAP_IterateNewSpaceWeakUnmodifiedRoots_Repro.html](attachments/UAP_IterateNewSpaceWeakUnmodifiedRoots_Repro.html) (text/plain, 2.1 KB)
- [UAP_Repro2.html](attachments/UAP_Repro2.html) (text/plain, 4.2 KB)

## Timeline

### lo...@gmail.com (2016-07-11)

Ran the exact same test case in Linux Asan build, I got:

Chromium	53.0.2763.0 (Developer Build) (64-bit)
=================================================================
==17785==ERROR: AddressSanitizer: use-after-poison on address 0x7e821e66fea0 at pc 0x7f06666b1498 bp 0x7ffccff7fb50 sp 0x7ffccff7fb48
READ of size 8 at 0x7e821e66fea0 thread T0 (chrome)
    #0 0x7f06666b1497 in IsEmpty v8/include/v8.h:501:43
    #1 0x7f06666b1497 in Reset v8/include/v8.h:7695
    #2 0x7f06666b1497 in blink::ScopedPersistent<v8::Value>::clear() third_party/WebKit/Source/bindings/core/v8/ScopedPersistent.h:98
    #3 0x7f066592cb32 in v8::internal::GlobalHandles::PendingPhantomCallback::Invoke(v8::internal::Isolate*) v8/src/global-handles.cc:1096:3
    #4 0x7f066592deaf in v8::internal::GlobalHandles::DispatchPendingPhantomCallbacks(bool) v8/src/global-handles.cc:1061:17
    #5 0x7f066592e86b in v8::internal::GlobalHandles::PostGarbageCollectionProcessing(v8::internal::GarbageCollector, v8::GCCallbackFlags) v8/src/global-handles.cc:1117:18
    #6 0x7f0665947e46 in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::GCCallbackFlags) v8/src/heap/heap.cc:1328:37
    #7 0x7f066594656b in v8::internal::Heap::CollectGarbage(v8::internal::GarbageCollector, char const*, char const*, v8::GCCallbackFlags) v8/src/heap/heap.cc:1009:11
    #8 0x7f066538d051 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, char const*, v8::GCCallbackFlags) v8/src/heap/heap-inl.h:575:10
    #9 0x7f067253ca1d in scheduler::WebSchedulerImpl::runIdleTask(std::__1::unique_ptr<blink::WebThread::IdleTask, std::__1::default_delete<blink::WebThread::IdleTask> >, base::TimeTicks) components/scheduler/child/web_scheduler_impl.cc:45:9
    #10 0x7f0672509d1a in void base::internal::RunnableAdapter<void (*)(std::__1::unique_ptr<blink::WebThread::IdleTask, std::__1::default_delete<blink::WebThread::IdleTask> >, base::TimeTicks)>::Run<std::__1::unique_ptr<blink::WebThread::IdleTask, std::__1::default_delete<blink::WebThread::IdleTask> >, base::TimeTicks>(std::__1::unique_ptr<blink::WebThread::IdleTask, std::__1::default_delete<blink::WebThread::IdleTask> >&&, base::TimeTicks&&) base/bind_internal.h:160:12
    #11 0x7f0672509a3c in base::internal::Invoker<base::IndexSequence<0ul>, base::internal::BindState<base::internal::RunnableAdapter<void (*)(std::__1::unique_ptr<blink::WebThread::IdleTask, std::__1::default_delete<blink::WebThread::IdleTask> >, base::TimeTicks)>, void (std::__1::unique_ptr<blink::WebThread::IdleTask, std::__1::default_delete<blink::WebThread::IdleTask> >, base::TimeTicks), base::internal::PassedWrapper<std::__1::unique_ptr<blink::WebThread::IdleTask, std::__1::default_delete<blink::WebThread::IdleTask> > > >, false, void (base::TimeTicks)>::Run(base::internal::BindStateBase*, base::TimeTicks&&) base/bind_internal.h:364:12
    #12 0x7f0670c8bb15 in base::Callback<void (base::TimeTicks), (base::internal::CopyMode)1>::Run(base::TimeTicks) const base/callback.h:397:12
    #13 0x7f0672504a02 in scheduler::SingleThreadIdleTaskRunner::RunTask(base::Callback<void (base::TimeTicks), (base::internal::CopyMode)1>) components/scheduler/child/single_thread_idle_task_runner.cc:79:13
    #14 0x7f0672505ed7 in void base::internal::RunnableAdapter<void (scheduler::SingleThreadIdleTaskRunner::*)(base::Callback<void (base::TimeTicks), (base::internal::CopyMode)1>)>::Run<scheduler::SingleThreadIdleTaskRunner*, base::Callback<void (base::TimeTicks), (base::internal::CopyMode)1> const&>(scheduler::SingleThreadIdleTaskRunner*&&, base::Callback<void (base::TimeTicks), (base::internal::CopyMode)1> const&) base/bind_internal.h:187:12
    #15 0x7f0672505bc8 in void base::internal::InvokeHelper<true, void>::MakeItSo<base::internal::RunnableAdapter<void (scheduler::SingleThreadIdleTaskRunner::*)(base::Callback<void (base::TimeTicks), (base::internal::CopyMode)1>)>&, base::WeakPtr<scheduler::SingleThreadIdleTaskRunner>, base::Callback<void (base::TimeTicks), (base::internal::CopyMode)1> const&>(base::internal::RunnableAdapter<void (scheduler::SingleThreadIdleTaskRunner::*)(base::Callback<void (base::TimeTicks), (base::internal::CopyMode)1>)>&, base::WeakPtr<scheduler::SingleThreadIdleTaskRunner>, base::Callback<void (base::TimeTicks), (base::internal::CopyMode)1> const&) base/bind_internal.h:325:38
    #16 0x7f0672505a58 in base::internal::Invoker<base::IndexSequence<0ul, 1ul>, base::internal::BindState<base::internal::RunnableAdapter<void (scheduler::SingleThreadIdleTaskRunner::*)(base::Callback<void (base::TimeTicks), (base::internal::CopyMode)1>)>, void (scheduler::SingleThreadIdleTaskRunner*, base::Callback<void (base::TimeTicks), (base::internal::CopyMode)1>), base::WeakPtr<scheduler::SingleThreadIdleTaskRunner>&, base::Callback<void (base::TimeTicks), (base::internal::CopyMode)1> const&>, true, void ()>::Run(base::internal::BindStateBase*) base/bind_internal.h:364:12
    #17 0x7f06624148c6 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask const&) base/debug/task_annotator.cc:51:21
    #18 0x7f0672559604 in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(scheduler::internal::WorkQueue*, scheduler::internal::TaskQueueImpl::Task*) components/scheduler/base/task_queue_manager.cc:289:19
    #19 0x7f0672556303 in scheduler::TaskQueueManager::DoWork(base::TimeTicks, bool) components/scheduler/base/task_queue_manager.cc:201:13
    #20 0x7f067255c6ae in void base::internal::InvokeHelper<true, void>::MakeItSo<base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::*)(base::TimeTicks, bool)>&, base::WeakPtr<scheduler::TaskQueueManager>, base::TimeTicks const&, bool const&>(base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::*)(base::TimeTicks, bool)>&, base::WeakPtr<scheduler::TaskQueueManager>, base::TimeTicks const&, bool const&) base/bind_internal.h:325:38
    #21 0x7f067255f3dc in base::internal::Invoker<base::IndexSequence<0ul, 1ul, 2ul>, base::internal::BindState<base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::*)(base::TimeTicks, bool)>, void (scheduler::TaskQueueManager*, base::TimeTicks, bool), base::WeakPtr<scheduler::TaskQueueManager>, base::TimeTicks&, bool>, true, void ()>::Run(base::internal::BindStateBase*) base/bind_internal.h:364:12
    #22 0x7f06624148c6 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask const&) base/debug/task_annotator.cc:51:21
    #23 0x7f06622b0879 in base::MessageLoop::RunTask(base::PendingTask const&) base/message_loop/message_loop.cc:475:19
    #24 0x7f06622b14cd in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) base/message_loop/message_loop.cc:484:5
    #25 0x7f06622b2b29 in base::MessageLoop::DoDelayedWork(base::TimeTicks*) base/message_loop/message_loop.cc:639:10
    #26 0x7f06622bdf51 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:37:27
    #27 0x7f06622afeae in base::MessageLoop::RunHandler() base/message_loop/message_loop.cc:439:10
    #28 0x7f066231cda4 in base::RunLoop::Run() base/run_loop.cc:35:10
    #29 0x7f06622ad9c8 in base::MessageLoop::Run() base/message_loop/message_loop.cc:294:12
    #30 0x7f066d197343 in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer_main.cc:199:37
    #31 0x7f066217bf40 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) content/app/content_main_runner.cc:345:14
    #32 0x7f0662180387 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner.cc:787:12
    #33 0x7f066217b1ef in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:20:28
    #34 0x7f066103b18a in ChromeMain chrome/app/chrome_main.cc:84:12
    #35 0x7f06562f9ec4 in __libc_start_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

AddressSanitizer can not describe address in more detail (wild memory access suspected).
SUMMARY: AddressSanitizer: use-after-poison v8/include/v8.h:501:43 in IsEmpty
Shadow bytes around the buggy address:
  0x0fd0c3cc5f80: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd0c3cc5f90: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd0c3cc5fa0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd0c3cc5fb0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd0c3cc5fc0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
=>0x0fd0c3cc5fd0: f7 f7 f7 f7[f7]f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd0c3cc5fe0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd0c3cc5ff0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd0c3cc6000: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 00 00 00 00
  0x0fd0c3cc6010: 00 00 00 00 00 00 00 00 00 00 00 f7 f7 f7 f7 f7
  0x0fd0c3cc6020: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Heap right redzone:      fb
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack partial redzone:   f4
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
==17785==ABORTING



### lo...@gmail.com (2016-07-11)

BTW. why there is no update to Linux ASAN builds?
The latest build from https://commondatastorage.googleapis.com/chromium-browser-asan/index.html?prefix=linux-release/ was generated on 2016-06-08:  

 asan-symbolized-linux-release-398598.zip 2016-06-08 23:40:24 753.06MB  

### cl...@chromium.org (2016-07-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5053383581106176

### aa...@google.com (2016-07-11)

Ignore the -symbolized- ones, just use asan-linux-release-*

### cl...@chromium.org (2016-07-11)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6024578866610176

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: 
Crash Address: 
Crash State:
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv967peL5CWrsCZzJRi-l0ISc_AZZn2igc60OUwXhgtR7PdTvk8QP7BtKbghvBE5nC7I9AjT1xg3eTzm8mI7mCobpzS3swPZr-sjPRa2pNmWqFwh1HiAwzdeqbaUurDrrUPlbu4HJgkkjVnzglQzVo1bDjYqWUA?testcase_id=6024578866610176


Filer: calamity

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### ca...@chromium.org (2016-07-11)

ClusterFuzz isn't bringing anything up for the given test case.

palmer@, any idea about the asan builds?

### cl...@chromium.org (2016-07-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6358274471624704

### aa...@google.com (2016-07-11)

ah, didn't see this was for windows, reuploaded.

### ta...@google.com (2016-07-13)

[Empty comment from Monorail migration]

[Monorail components: Infra>Client>V8]

### cl...@chromium.org (2016-07-13)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6185592694243328

Fuzzer: phoglund_webrtc_peerconnection
Job Type: android_asan_chrome_x86
Platform Id: android:gce_x86:m

Crash Type: Use-after-poison WRITE 4
Crash Address: 0x4a50d428
Crash State:
  v8::internal::GlobalHandles::IterateNewSpaceWeakUnmodifiedRoots
  v8::internal::Heap::Scavenge
  v8::internal::Heap::PerformGarbageCollection
  
Recommended Security Severity: High


Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95XQti6daRttUYATJaNL2C3oyHFkV7vRgvyzQeyTWIyQ1C0nlYGZip7GiXzsgGZ0m_iBNVpKk70Ag-gcCNPMMm9BK7LJNGbSCTN5wOOq2a40jnXEISfG9d9fZnt80W6hWGypSYesKWX1CJaH7B23ynCD3pVzt5-iV8F7rXPihiTEZo1eGw?testcase_id=6185592694243328


Additional requirements: Requires HTTP

Filer: inferno

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2016-07-13)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4781287437238272

Fuzzer: phoglund_webrtc_peerconnection
Job Type: mac_asan_chrome
Platform Id: mac

Crash Type: Use-after-poison WRITE 8
Crash Address: 0x7ed21387e618
Crash State:
  v8::internal::GlobalHandles::IterateNewSpaceWeakUnmodifiedRoots
  v8::internal::Heap::Scavenge
  v8::internal::Heap::PerformGarbageCollection
  
Recommended Security Severity: High


Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95YMBbOEb7M8cR-ogmeVbAN4Wcswf_JtnYzA90qzvMZQT6-yHliXKTgvHe0PeetoE7OUtqVOugNCBxXfZ3h6R2pSfiBplFlNFb4d5ydM4-wyfKYOs5TmHFKWmDh0pR709qR5WwQuccTdgAam6FTXNSHpg5cc68XERELaPk0jr52QdD73yA?testcase_id=4781287437238272


Additional requirements: Requires HTTP

Filer: inferno

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### in...@chromium.org (2016-07-13)

Ok, this is an unreliable repro, similar to the ones we see at ClusterFuzz as well. c#10, c#11. Looks like a recent regression. Jaroslav, can you please take a look.

[Monorail components: -Infra>Client>V8 Blink>JavaScript]

### ja...@chromium.org (2016-07-13)

Assigning to the current memory sheriff.

### ml...@chromium.org (2016-07-13)

[Empty comment from Monorail migration]

### ml...@chromium.org (2016-07-13)

[Empty comment from Monorail migration]

### ml...@chromium.org (2016-07-13)

Reproduced on Linux 64bit tip of tree debug build using the mac testcase in a way that seems related (DCHECK).

~RTCVoidRequestPromiseImpl() checks whether its requester has already been cleared upon destruction. Since it is a DCHECK and it does not actually clear the handle, the next time a V8 GC visits the handle it will read/write to garbage. There seems to be a path to destruction without clearing the handle.

Re-assigning based on initial commit https://codereview.chromium.org/1661493002. If you think that's wrong, just throw it back.

Stacktrace:
[1:1:0713/101654:FATAL:RTCVoidRequestPromiseImpl.cpp(29)] Check failed: !m_requester. 
#0 0x7f59e885dff1 __interceptor_backtrace
#1 0x7f59e61d65be base::debug::StackTrace::StackTrace()
#2 0x7f59e631179f logging::LogMessage::~LogMessage()
#3 0x7f59a77145b3 blink::RTCVoidRequestPromiseImpl::~RTCVoidRequestPromiseImpl()
#4 0x7f59a7712a0a blink::GarbageCollectedFinalized<>::finalizeGarbageCollectedObject()
#5 0x7f59a7712995 blink::FinalizerTraitImpl<>::finalize()
#6 0x7f59a7712975 blink::FinalizerTrait<>::finalize()
#7 0x7f59c10564e9 blink::HeapObjectHeader::finalize()
#8 0x7f59c105fa85 blink::NormalPage::sweep()
#9 0x7f59c1058c83 blink::BaseArena::sweepUnsweptPage()
#10 0x7f59c10592fe blink::BaseArena::completeSweep()
#11 0x7f59c106ecaf blink::ThreadState::completeSweep()
#12 0x7f59c105dcec blink::NormalPageArena::outOfLineAllocate()
#13 0x7f59ac350046 blink::NormalPageArena::allocateObject()
#14 0x7f59ac34eeb2 blink::ThreadHeap::allocateOnArenaIndex()
#15 0x7f59ac44b9e8 blink::ThreadHeap::allocate<>()
#16 0x7f59ac44b965 blink::GarbageCollected<>::allocateObject()
#17 0x7f59ac44b937 blink::GarbageCollected<>::operator new()
#18 0x7f59ac572e44 blink::V8EventListener::create()
#19 0x7f59ac57189d blink::V8EventListenerList::findOrCreateWrapper<>()
#20 0x7f59ac570a71 blink::V8EventListenerList::getEventListener()
#21 0x7f59a8853870 blink::RTCPeerConnectionV8Internal::onicecandidateAttributeSetter()
#22 0x7f59a884df6d blink::RTCPeerConnectionV8Internal::onicecandidateAttributeSetterCallback()
#23 0x7f59c8f7c205 v8::internal::FunctionCallbackArguments::Call()
#24 0x7f59c92a6f02 v8::internal::(anonymous namespace)::HandleApiCallHelper<>()
#25 0x7f59c92a5fa7 v8::internal::Builtins::InvokeApiFunction()
#26 0x7f59ca849372 v8::internal::Object::SetPropertyWithAccessor()
#27 0x7f59ca882a84 v8::internal::Object::SetPropertyInternal()
#28 0x7f59ca880eaf v8::internal::Object::SetProperty()
#29 0x7f59ca5e8339 v8::internal::StoreIC::Store()
#30 0x7f59ca5fd986 v8::internal::__RT_impl_Runtime_StoreIC_Miss()
#31 0x7f59ca5fc631 v8::internal::Runtime_StoreIC_Miss()
#32 0x7f597ae063a7 <unknown>

Received signal 6
#0 0x7f59e885dff1 [31579:31611:0713/101654:WARNING:video_capture_device_client.cc(142)] Failed to reserve I420 output buffer.
__interceptor_backtrace
#1 0x7f59e61d65be base::debug::StackTrace::StackTrace()
#2 0x7f59e61d5279 base::debug::(anonymous namespace)::StackDumpSignalHandler()
#3 0x7f59ba72b330 <unknown>
#4 0x7f59b8b29c37 gsignal
#5 0x7f59b8b2d028 abort
#6 0x7f59e61cb91b base::debug::(anonymous namespace)::DebugBreak()
#7 0x7f59e61cb8f8 base::debug::BreakDebugger()
#8 0x7f59e6312736 logging::LogMessage::~LogMessage()
#9 0x7f59a77145b3 blink::RTCVoidRequestPromiseImpl::~RTCVoidRequestPromiseImpl()
#10 0x7f59a7712a0a blink::GarbageCollectedFinalized<>::finalizeGarbageCollectedObject()
#11 0x7f59a7712995 blink::FinalizerTraitImpl<>::finalize()
#12 0x7f59a7712975 blink::FinalizerTrait<>::finalize()
#13 0x7f59c10564e9 blink::HeapObjectHeader::finalize()
#14 0x7f59c105fa85 blink::NormalPage::sweep()
#15 0x7f59c1058c83 blink::BaseArena::sweepUnsweptPage()
#16 0x7f59c10592fe blink::BaseArena::completeSweep()
#17 0x7f59c106ecaf [31579:31611:0713/101654:WARNING:video_capture_device_client.cc(142)] Failed to reserve I420 output buffer.
blink::ThreadState::completeSweep()
#18 0x7f59c105dcec blink::NormalPageArena::outOfLineAllocate()
#19 0x7f59ac350046 blink::NormalPageArena::allocateObject()
#20 0x7f59ac34eeb2 blink::ThreadHeap::allocateOnArenaIndex()
#21 0x7f59ac44b9e8 blink::ThreadHeap::allocate<>()
#22 0x7f59ac44b965 blink::GarbageCollected<>::allocateObject()
#23 0x7f59ac44b937 blink::GarbageCollected<>::operator new()
#24 0x7f59ac572e44 [31579:31611:0713/101654:WARNING:video_capture_device_client.cc(142)] Failed to reserve I420 output buffer.
blink::V8EventListener::create()
#25 0x7f59ac57189d blink::V8EventListenerList::findOrCreateWrapper<>()
#26 0x7f59ac570a71 blink::V8EventListenerList::getEventListener()
#27 0x7f59a8853870 blink::RTCPeerConnectionV8Internal::onicecandidateAttributeSetter()
#28 0x7f59a884df6d blink::RTCPeerConnectionV8Internal::onicecandidateAttributeSetterCallback()
#29 0x7f59c8f7c205 v8::internal::FunctionCallbackArguments::Call()
#30 0x7f59c92a6f02 v8::internal::(anonymous namespace)::HandleApiCallHelper<>()
#31 0x7f59c92a5fa7 v8::internal::Builtins::InvokeApiFunction()
#32 0x7f59ca849372 v8::internal::Object::SetPropertyWithAccessor()
#33 0x7f59ca882a84 v8::internal::Object::SetPropertyInternal()
#34 0x7f59ca880eaf [31579:31611:0713/101655:WARNING:video_capture_device_client.cc(142)] Failed to reserve I420 output buffer.
v8::internal::Object::SetProperty()
#35 0x7f59ca5e8339 v8::internal::StoreIC::Store()
#36 0x7f59ca5fd986 v8::internal::__RT_impl_Runtime_StoreIC_Miss()
#37 0x7f59ca5fc631 v8::internal::Runtime_StoreIC_Miss()
#38 0x7f597ae063a7 <unknown>
  r8: f2f2f2f200000000  r9: 00000000f1f1f1f1 r10: 0000000000000008 r11: 0000000000000202
 r12: 00000febb3fe6800 r13: 00007f59e6a224ad r14: 00007f599ff74020 r15: 00000000f1f1f1f1
  di: 0000000000000001  si: 0000000000000001  bp: 00007ffc35902b80  bx: 00007ffc35902ba0
  dx: 0000000000000006  ax: 0000000000000000  cx: ffffffffffffffff  sp: 00007ffc35902a48
  ip: 00007f59b8b29c37 efl: 0000000000000202 cgf: 0000000000000033 erf: 0000000000000000
 trp: 0000000000000000 msk: 0000000000000000 cr2: 0000000000000000
[end of stack trace]


[Monorail components: -Blink>JavaScript Blink>WebRTC]

### lo...@gmail.com (2016-07-13)

RE https://crbug.com/chromium/626893#c12

The attached minimized test case UAP_IterateNewSpaceWeakUnmodifiedRoots_Repro.html is very reliable in Windows ASAN build downloaded from https://commondatastorage.googleapis.com/chromium-browser-asan/index.html?prefix=win32-release/ per my test, not very reliable in Linux ASAN build  asan-symbolized-linux-release-398598.zip on my machine though.

However, before the test case being minimized, it's very reliable in asan-symbolized-linux-release-398598.zip.

### gu...@chromium.org (2016-07-13)

I can reliably reproduce the DCHECK in RTCVoidRequestPromiseImpl.
My conclusion is that the DCHECK is wrong and occurs because the test reloads the document repeatedly and the RTCVoidRequestPromiseImpl may be destroyed before it gets a reply.
I will remove the DCHECK so that it doesn't continue producing bogus crashes.
However, this is not the root cause of the use-after-poison in the original report. 
Assigning back to mlippautz@

### ml...@chromium.org (2016-07-13)

[Empty comment from Monorail migration]

### ml...@chromium.org (2016-07-13)

The symptom is that V8 reads/writes a weak reference that has not been cleared.

The theory is that we are missing a destructor call on the blink side that would clear the reference.

### sh...@chromium.org (2016-07-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-13)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2016-07-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/eb281fc3c0ad655e0a9b4381e70b3cefa535935d

commit eb281fc3c0ad655e0a9b4381e70b3cefa535935d
Author: guidou <guidou@chromium.org>
Date: Wed Jul 13 14:33:08 2016

Remove incorrect DCHECKS from RTC*RequestPromiseImpl

These DCHECKS sometimes cause crashes in tests.
A request may be destroyed before receiving a reply (e.g., if the
document is reloaded in the middle of a reply)

BUG=626893

Review-Url: https://codereview.chromium.org/2151443002
Cr-Commit-Position: refs/heads/master@{#405144}

[modify] https://crrev.com/eb281fc3c0ad655e0a9b4381e70b3cefa535935d/third_party/WebKit/Source/modules/peerconnection/RTCSessionDescriptionRequestPromiseImpl.cpp
[modify] https://crrev.com/eb281fc3c0ad655e0a9b4381e70b3cefa535935d/third_party/WebKit/Source/modules/peerconnection/RTCVoidRequestPromiseImpl.cpp


### pa...@chromium.org (2016-07-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-14)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ml...@chromium.org (2016-07-15)

This is not fixed. The CL merely removes a DCHECK that was crashing on the way for debug builds.


[Monorail components: -Blink>WebRTC Blink>JavaScript>GC]

### sh...@chromium.org (2016-07-15)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-07-16)

[Empty comment from Monorail migration]

### ul...@chromium.org (2016-07-18)

Reopening (not sure why bots insists that it is fixed) and taking over from Michael since Michael is on vacation.

### sh...@chromium.org (2016-07-19)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ul...@chromium.org (2016-07-19)

[Empty comment from Monorail migration]

### ul...@chromium.org (2016-07-19)

re #17: loobenyang@, could you please share asan options and command line for linux repro?

Do you get the following error in devtools console?﻿
"UAP_IterateNewSpaceWeakUnmodifiedRoots_Repro.html:24 Uncaught (in promise) DOMException: cannot resume a closed AudioContext"

### ul...@chromium.org (2016-07-19)

loobenyang@, how long do you wait for crash?

### go...@chromium.org (2016-07-19)

M53 beta launch is next week.Your bug is labelled as Beta ReleaseBlock, pls make sure to land the fix before 6:00 PM PST, Friday (07/22/16). Thank you.

### lo...@gmail.com (2016-07-20)

RE https://crbug.com/chromium/626893#c32

Yes, can see this kind of error in console when running the test case:
UAP_Repro2.html:94 Uncaught (in promise) DOMException: cannot resume a closed AudioContext(anonymous function) @ UAP_Repro2.html:94

When running the test case in Linux with ASAN build, the command line i used was "./chrome --no-sandbox".

With Windows ASAN build, i just run it in Windbg, no command line option.
 
Would you try test case UAP_Repro2.html with Windows ASAN build?

To run the test case in Linux ASAN build, i have to change the refresh timer in the test case to a larger value, like "setTimeout(function(){location.reload()},800);" because the virtual machine is slow and may take 30 min or more to trigger.

I ran UAP_Repro2.html against ASAN build in Windows, it crashed in 1 minute.

=================================================================
==18840==ERROR: AddressSanitizer: use-after-poison on address 0x0d69ed70 at pc 0x8cf09f75 bp 0xdeadbeef sp 0x041ec90c
WRITE of size 4 at 0x0d69ed70 thread T0
==18840==WARNING: Failed to use and restart external symbolizer!
==18840==*** WARNING: Failed to initialize DbgHelp!              ***
==18840==*** Most likely this means that the app is already      ***
==18840==*** using DbgHelp, possibly with incompatible flags.    ***
==18840==*** Due to technical reasons, symbolization might crash ***
==18840==*** or produce wrong results.                           ***
    #0 0x8cf09f74 in v8::internal::GlobalHandles::IterateNewSpaceWeakUnmodifiedRoots+0x3c4 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xcf19f74)
    #1 0x8c4a1116 in v8::internal::Heap::Scavenge+0x44c6 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xc4b1116)
    #2 0x8c496a3b in v8::internal::Heap::PerformGarbageCollection+0x104b (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xc4a6a3b)
    #3 0x8c493eb2 in v8::internal::Heap::CollectGarbage+0x792 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xc4a3eb2)
    #4 0x8cb01f1b in v8::internal::ScavengeJob::IdleTask::RunInternal+0x2bb (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xcb11f1b)
    #5 0x8e4a1344 in scheduler::WebSchedulerImpl::runIdleTask+0x104 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xe4b1344)
    #6 0x8e485115 in base::internal::FunctorTraits<void (__cdecl*)(std::unique_ptr<blink::WebThread::IdleTask,std::default_delete<blink::WebThread::IdleTask> >,base::TimeTicks),void>::Invoke<std::unique_ptr<blink::WebThread::IdleTask,std::default_delete<blink::WebThread::IdleTask> >,base::TimeTicks>+0xc5 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xe495115)
    #7 0x8e484e2b in base::internal::Invoker<base::internal::BindState<void (__cdecl*)(std::unique_ptr<blink::WebThread::IdleTask,std::default_delete<blink::WebThread::IdleTask> >,base::TimeTicks),base::internal::PassedWrapper<std::unique_ptr<blink::WebThread::IdleTask,std::default_delete<blink::WebThread::IdleTask> > > >,void __cdecl(base::TimeTicks)>::Run+0x14b (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xe494e2b)
    #8 0x8e4a43e0 in scheduler::SingleThreadIdleTaskRunner::RunTask+0x430 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xe4b43e0)
    #9 0x8e4a5534 in base::internal::FunctorTraits<void (__thiscall scheduler::SingleThreadIdleTaskRunner::*)(base::Callback<void __cdecl(base::TimeTicks),1>),void>::Invoke<base::WeakPtr<scheduler::SingleThreadIdleTaskRunner>,base::Callback<void __cdecl(base::TimeTicks),1> const &>+0x74 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xe4b5534)
    #10 0x8e4a5342 in base::internal::Invoker<base::internal::BindState<void (__thiscall scheduler::SingleThreadIdleTaskRunner::*)(base::Callback<void __cdecl(base::TimeTicks),1>),base::WeakPtr<scheduler::SingleThreadIdleTaskRunner>,base::Callback<void __cdecl(base::TimeTicks),1> >,void __cdecl(void)>::RunImpl<void (__thiscall scheduler::SingleThreadIdleTaskRunner::*const &)(base::Callback<void __cdecl(base::TimeTicks),1>),std::tuple<base::WeakPtr<scheduler::SingleThreadIdleTaskRunner>,base::Callback<void __cdecl(base::TimeTicks),1> > const &,0,1>+0x1c2 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xe4b5342)
    #11 0x8e4a5130 in base::internal::Invoker<base::internal::BindState<void (__thiscall scheduler::SingleThreadIdleTaskRunner::*)(base::Callback<void __cdecl(base::TimeTicks),1>),base::WeakPtr<scheduler::SingleThreadIdleTaskRunner>,base::Callback<void __cdecl(base::TimeTicks),1> >,void __cdecl(void)>::Run+0x80 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xe4b5130)
    #12 0x805de041 in base::debug::TaskAnnotator::RunTask+0x3f1 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0x5ee041)
    #13 0x8e4cdeb3 in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue+0x993 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xe4ddeb3)
    #14 0x8e4c82fb in scheduler::TaskQueueManager::DoWork+0x6cb (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xe4d82fb)
    #15 0x8e4d5632 in base::internal::Invoker<base::internal::BindState<void (__thiscall scheduler::TaskQueueManager::*)(base::TimeTicks,bool),base::WeakPtr<scheduler::TaskQueueManager>,base::TimeTicks,bool>,void __cdecl(void)>::RunImpl<void (__thiscall scheduler::TaskQueueManager::*const &)(base::TimeTicks,bool),std::tuple<base::WeakPtr<scheduler::TaskQueueManager>,base::TimeTicks,bool> const &,0,1,2>+0x222 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xe4e5632)
    #16 0x8e4d53c0 in base::internal::Invoker<base::internal::BindState<void (__thiscall scheduler::TaskQueueManager::*)(base::TimeTicks,bool),base::WeakPtr<scheduler::TaskQueueManager>,base::TimeTicks,bool>,void __cdecl(void)>::Run+0x80 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xe4e53c0)
    #17 0x805de041 in base::debug::TaskAnnotator::RunTask+0x3f1 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0x5ee041)
    #18 0x804960ab in base::MessageLoop::RunTask+0x6eb (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0x4a60ab)
    #19 0x80497c9c in base::MessageLoop::DoWork+0x75c (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0x4a7c9c)
    #20 0x805e6f18 in base::MessagePumpDefault::Run+0x378 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0x5f6f18)
    #21 0x80495125 in base::MessageLoop::RunHandler+0x45 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0x4a5125)
    #22 0x805e754f in base::RunLoop::Run+0x1df (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0x5f754f)
    #23 0x878c12f7 in content::RendererMain+0x567 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0x78d12f7)
    #24 0x80355c57 in content::RunNamedProcessTypeMain+0x557 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0x365c57)
    #25 0x80357c26 in content::ContentMainRunnerImpl::Run+0x2c6 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0x367c26)
    #26 0x80354d74 in content::ContentMain+0x74 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0x364d74)
    #27 0x7fff1130 in ChromeMain+0x130 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0x1130)
    #28 0x16cc25 in MainDllLoader::Launch+0x485 (D:\ChromeBuilds\asan-win32-release-405185\chrome.exe+0xcc25)
    #29 0x162589 in main+0x1299 (D:\ChromeBuilds\asan-win32-release-405185\chrome.exe+0x2589)
    #30 0x1730c68 in __scrt_common_main_seh f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl:255
    #31 0x75c038f3 in BaseThreadInitThunk+0x23 (C:\WINDOWS\SYSTEM32\KERNEL32.DLL+0x138f3)
    #32 0x77875de2 in RtlUnicodeStringToInteger+0x252 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x65de2)
    #33 0x77875dad in RtlUnicodeStringToInteger+0x21d (C:\WINDOWS\SYSTEM32\ntdll.dll+0x65dad)

AddressSanitizer can not describe address in more detail (wild memory access suspected).
SUMMARY: AddressSanitizer: use-after-poison (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xcf19f74) in v8::internal::GlobalHandles::IterateNewSpaceWeakUnmodifiedRoots+0x3c4
Shadow bytes around the buggy address:
  0x31ad3d50: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x31ad3d60: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x31ad3d70: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x31ad3d80: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x31ad3d90: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
=>0x31ad3da0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7[f7]f7
  0x31ad3db0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x31ad3dc0: f7 f7 f7 00 00 00 00 00 00 00 00 00 00 04 f7 f7
  0x31ad3dd0: f7 f7 f7 f7 f7 f7 f7 00 00 00 00 00 00 00 00 00
  0x31ad3de0: 00 00 04 00 00 00 00 00 00 00 00 00 00 00 00 04
  0x31ad3df0: 00 00 00 00 00 00 00 00 04 f7 f7 f7 f7 f7 f7 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Heap right redzone:      fb
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack partial redzone:   f4
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
==18840==ABORTING
=================================================================
==18840==ERROR: AddressSanitizer: use-after-poison on address 0x0d69ed70 at pc 0x8cf09f75 bp 0xdeadbeef sp 0x041ec90c
WRITE of size 4 at 0x0d69ed70 thread T0
==18840==WARNING: Failed to use and restart external symbolizer!
==18840==*** WARNING: Failed to initialize DbgHelp!              ***
==18840==*** Most likely this means that the app is already      ***
==18840==*** using DbgHelp, possibly with incompatible flags.    ***
==18840==*** Due to technical reasons, symbolization might crash ***
==18840==*** or produce wrong results.                           ***
    #0 0x8cf09f74 in v8::internal::GlobalHandles::IterateNewSpaceWeakUnmodifiedRoots+0x3c4 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xcf19f74)
    #1 0x8c4a1116 in v8::internal::Heap::Scavenge+0x44c6 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xc4b1116)
    #2 0x8c496a3b in v8::internal::Heap::PerformGarbageCollection+0x104b (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xc4a6a3b)
    #3 0x8c493eb2 in v8::internal::Heap::CollectGarbage+0x792 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xc4a3eb2)
    #4 0x8cb01f1b in v8::internal::ScavengeJob::IdleTask::RunInternal+0x2bb (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xcb11f1b)
    #5 0x8e4a1344 in scheduler::WebSchedulerImpl::runIdleTask+0x104 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xe4b1344)
    #6 0x8e485115 in base::internal::FunctorTraits<void (__cdecl*)(std::unique_ptr<blink::WebThread::IdleTask,std::default_delete<blink::WebThread::IdleTask> >,base::TimeTicks),void>::Invoke<std::unique_ptr<blink::WebThread::IdleTask,std::default_delete<blink::WebThread::IdleTask> >,base::TimeTicks>+0xc5 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xe495115)
    #7 0x8e484e2b in base::internal::Invoker<base::internal::BindState<void (__cdecl*)(std::unique_ptr<blink::WebThread::IdleTask,std::default_delete<blink::WebThread::IdleTask> >,base::TimeTicks),base::internal::PassedWrapper<std::unique_ptr<blink::WebThread::IdleTask,std::default_delete<blink::WebThread::IdleTask> > > >,void __cdecl(base::TimeTicks)>::Run+0x14b (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xe494e2b)
    #8 0x8e4a43e0 in scheduler::SingleThreadIdleTaskRunner::RunTask+0x430 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xe4b43e0)
    #9 0x8e4a5534 in base::internal::FunctorTraits<void (__thiscall scheduler::SingleThreadIdleTaskRunner::*)(base::Callback<void __cdecl(base::TimeTicks),1>),void>::Invoke<base::WeakPtr<scheduler::SingleThreadIdleTaskRunner>,base::Callback<void __cdecl(base::TimeTicks),1> const &>+0x74 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xe4b5534)
    #10 0x8e4a5342 in base::internal::Invoker<base::internal::BindState<void (__thiscall scheduler::SingleThreadIdleTaskRunner::*)(base::Callback<void __cdecl(base::TimeTicks),1>),base::WeakPtr<scheduler::SingleThreadIdleTaskRunner>,base::Callback<void __cdecl(base::TimeTicks),1> >,void __cdecl(void)>::RunImpl<void (__thiscall scheduler::SingleThreadIdleTaskRunner::*const &)(base::Callback<void __cdecl(base::TimeTicks),1>),std::tuple<base::WeakPtr<scheduler::SingleThreadIdleTaskRunner>,base::Callback<void __cdecl(base::TimeTicks),1> > const &,0,1>+0x1c2 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xe4b5342)
    #11 0x8e4a5130 in base::internal::Invoker<base::internal::BindState<void (__thiscall scheduler::SingleThreadIdleTaskRunner::*)(base::Callback<void __cdecl(base::TimeTicks),1>),base::WeakPtr<scheduler::SingleThreadIdleTaskRunner>,base::Callback<void __cdecl(base::TimeTicks),1> >,void __cdecl(void)>::Run+0x80 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xe4b5130)
    #12 0x805de041 in base::debug::TaskAnnotator::RunTask+0x3f1 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0x5ee041)
    #13 0x8e4cdeb3 in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue+0x993 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xe4ddeb3)
    #14 0x8e4c82fb in scheduler::TaskQueueManager::DoWork+0x6cb (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xe4d82fb)
    #15 0x8e4d5632 in base::internal::Invoker<base::internal::BindState<void (__thiscall scheduler::TaskQueueManager::*)(base::TimeTicks,bool),base::WeakPtr<scheduler::TaskQueueManager>,base::TimeTicks,bool>,void __cdecl(void)>::RunImpl<void (__thiscall scheduler::TaskQueueManager::*const &)(base::TimeTicks,bool),std::tuple<base::WeakPtr<scheduler::TaskQueueManager>,base::TimeTicks,bool> const &,0,1,2>+0x222 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xe4e5632)
    #16 0x8e4d53c0 in base::internal::Invoker<base::internal::BindState<void (__thiscall scheduler::TaskQueueManager::*)(base::TimeTicks,bool),base::WeakPtr<scheduler::TaskQueueManager>,base::TimeTicks,bool>,void __cdecl(void)>::Run+0x80 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xe4e53c0)
    #17 0x805de041 in base::debug::TaskAnnotator::RunTask+0x3f1 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0x5ee041)
    #18 0x804960ab in base::MessageLoop::RunTask+0x6eb (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0x4a60ab)
    #19 0x80497c9c in base::MessageLoop::DoWork+0x75c (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0x4a7c9c)
    #20 0x805e6f18 in base::MessagePumpDefault::Run+0x378 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0x5f6f18)
    #21 0x80495125 in base::MessageLoop::RunHandler+0x45 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0x4a5125)
    #22 0x805e754f in base::RunLoop::Run+0x1df (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0x5f754f)
    #23 0x878c12f7 in content::RendererMain+0x567 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0x78d12f7)
    #24 0x80355c57 in content::RunNamedProcessTypeMain+0x557 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0x365c57)
    #25 0x80357c26 in content::ContentMainRunnerImpl::Run+0x2c6 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0x367c26)
    #26 0x80354d74 in content::ContentMain+0x74 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0x364d74)
    #27 0x7fff1130 in ChromeMain+0x130 (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0x1130)
    #28 0x16cc25 in MainDllLoader::Launch+0x485 (D:\ChromeBuilds\asan-win32-release-405185\chrome.exe+0xcc25)
    #29 0x162589 in main+0x1299 (D:\ChromeBuilds\asan-win32-release-405185\chrome.exe+0x2589)
    #30 0x1730c68 in __scrt_common_main_seh f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl:255
    #31 0x75c038f3 in BaseThreadInitThunk+0x23 (C:\WINDOWS\SYSTEM32\KERNEL32.DLL+0x138f3)
    #32 0x77875de2 in RtlUnicodeStringToInteger+0x252 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x65de2)
    #33 0x77875dad in RtlUnicodeStringToInteger+0x21d (C:\WINDOWS\SYSTEM32\ntdll.dll+0x65dad)

AddressSanitizer can not describe address in more detail (wild memory access suspected).
SUMMARY: AddressSanitizer: use-after-poison (D:\ChromeBuilds\asan-win32-release-405185\chrome_child.dll+0xcf19f74) in v8::internal::GlobalHandles::IterateNewSpaceWeakUnmodifiedRoots+0x3c4
Shadow bytes around the buggy address:
  0x31ad3d50: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x31ad3d60: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x31ad3d70: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x31ad3d80: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x31ad3d90: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
=>0x31ad3da0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7[f7]f7
  0x31ad3db0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x31ad3dc0: f7 f7 f7 00 00 00 00 00 00 00 00 00 00 04 f7 f7
  0x31ad3dd0: f7 f7 f7 f7 f7 f7 f7 00 00 00 00 00 00 00 00 00
  0x31ad3de0: 00 00 04 00 00 00 00 00 00 00 00 00 00 00 00 04
  0x31ad3df0: 00 00 00 00 00 00 00 00 04 f7 f7 f7 f7 f7 f7 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Heap right redzone:      fb
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack partial redzone:   f4
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
==18840==ABORTING



### sh...@chromium.org (2016-07-20)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ul...@chromium.org (2016-07-21)

loobenyang@, thank you for UAP_Repro2.html, it worked well on Windows with ASAN.

The issue seems to be a false positive caused by too eager poisoning of unmarked objects in Oilpan heap before lazy sweeping is finished:
https://cs.chromium.org/chromium/src/third_party/WebKit/Source/platform/heap/ThreadState.cpp?rcl=0&l=1016

Here is what happens:
1. We have a PromiseRejectionEvent, which has a phantom-weak ScopedPersistent<v8::Value> m_reason.
2. The PromiseRejectionEvent becomes unreachable for Oilpan (unmarked).
3. After eagear sweeping but before lazy sweeping Oilpan poisons all unmarked objects (this is the bug).
4. V8 GC runs.
5. the m_reason of the PromiseRejectionEvent is unreachable for V8, so V8 tries to clear the phantom-weak reference by resetting the handle, which resides in poisoned PromiseRejectionEvent.
6. ASAN catches write to poisoned memory and crashes.

haraken@, could you please take a look into Oilpan heap poisoning and remove the security/release-block flags if you agree with my conclusion?


### sh...@chromium.org (2016-07-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-21)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2016-07-27)

[Empty comment from Monorail migration]

### ul...@chromium.org (2016-07-29)

Kentaro, could you please take a look at my assessment in #37?

### ha...@chromium.org (2016-07-29)

Thanks, ulan! The assessment in #37 looks correct. Removing release-block & security bugs.

Sigbjorn: What's a right way to fix this? Should we mark PromiseRejectionEvent as EARGERLY_FINALIZED? I'm wondering why other classes that hold ScopedPersistent (e.g., V8AbstractEventListener, V8ScrollStateCallback) don't hit the issue.


### [Deleted User] (2016-07-29)

Marking it as such sounds reasonable & simple (along with using DECLARE_EAGER_FINALIZATION_OPERATOR_NEW()).

Step 4 doesn't happen before 2 & 3 because of an idle Oilpan GC, presumably. The other two objects mentioned would have associated wrapper objects, i think.

### ha...@chromium.org (2016-07-29)

> The other two objects mentioned would have associated wrapper objects, i think.

Hmm, interesting.

ulan@: Would you help me understand when the Persistent handle is dropped from the global handle list? (i.e., when does the Persistent handle stop being traced by PersistentVisitor?) Is it when the V8 GC runs? Or is it when the phantom-weak callback is called?

(I'm asking this because Oilpan's GC keeps alive wrappers traced by PersistentVisitor.)


### sh...@chromium.org (2016-07-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-29)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aa...@google.com (2016-07-29)

Removed the merge labels, this should prevent sheriffbot from marking this as fixed.

### ul...@chromium.org (2016-07-29)

> ulan@: Would you help me understand when the Persistent handle is dropped from the global handle list? (i.e., when does the Persistent handle stop being traced by PersistentVisitor?) Is it when the V8 GC runs? Or is it when the phantom-weak callback is called?
We remove the global handle node whenever the corresponding persistent handle is reset. For phantom-weak handles without a callback this happens during V8 GC. For phantom-weak handles with a callback, this happens inside the callback.



### ha...@chromium.org (2016-07-29)

Thanks, ulan. Then this problem wouldn't be limited to objects that don't have wrappers.
 
class X {
  X() { m_y.setPhantom(); }
  ScopedPersistent<Y> m_y;
};

Regardless of whether X has a wrapper or not, the following scenario can happen:

1) X becomes unreachable.
2) An Oilpan GC is triggered. It poisons m_y.
3) Y becomes unreachable.
4) A V8 GC is triggered. It calls the phantom callback for m_y and crashes.

One solution would be to move ScopedPersistent to Oilpan's heap and mark it as eagerly-finalized. I'll think about it a bit more.



### bu...@chromium.org (2016-07-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/07d2ad752c2749ca67adb8051bf5591f57e06046

commit 07d2ad752c2749ca67adb8051bf5591f57e06046
Author: haraken <haraken@chromium.org>
Date: Fri Jul 29 21:05:51 2016

Add a pre-finalizer to PromiseRejectionEvent

We need to clear ScopedPersistents so that V8 doesn't call phantom callbacks
after Oilpan starts lazy sweeping.

BUG=626893

Review-Url: https://codereview.chromium.org/2196543003
Cr-Commit-Position: refs/heads/master@{#408742}

[modify] https://crrev.com/07d2ad752c2749ca67adb8051bf5591f57e06046/third_party/WebKit/Source/core/events/PromiseRejectionEvent.cpp
[modify] https://crrev.com/07d2ad752c2749ca67adb8051bf5591f57e06046/third_party/WebKit/Source/core/events/PromiseRejectionEvent.h


### go...@chromium.org (2016-08-03)

M53 Stable launch is coming soon.Your bug is labelled as Stable ReleaseBlock, pls make sure to land the fix asap so it gets chance to bake in beta before stable promotion. Thank you.

### oc...@chromium.org (2016-08-11)

What's left here? Does the CL in #52 address this bug, or are there more to come?

### ha...@chromium.org (2016-08-11)

There may remain some potential bugs around here (as I commented in #51), but I think this specific bug has already been fixed.


### aw...@chromium.org (2016-08-11)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-08-11)

Your change meets the bar and is auto-approved for M53 (branch: 2785)

### go...@chromium.org (2016-08-11)

Please merge your change to M53 branch 2785 latest by Friday 5:00 PM PT so we can take it in for next week Beta release. Thank you.

### bu...@chromium.org (2016-08-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/89fa8a4e8f4d77745e86b5176608b5d97204cf39

commit 89fa8a4e8f4d77745e86b5176608b5d97204cf39
Author: Kentaro Hara <haraken@chromium.org>
Date: Fri Aug 12 01:06:05 2016

Add a pre-finalizer to PromiseRejectionEvent

We need to clear ScopedPersistents so that V8 doesn't call phantom callbacks
after Oilpan starts lazy sweeping.

BUG=626893

Review-Url: https://codereview.chromium.org/2196543003
Cr-Commit-Position: refs/heads/master@{#408742}
(cherry picked from commit 07d2ad752c2749ca67adb8051bf5591f57e06046)

Review URL: https://codereview.chromium.org/2244533002 .

Cr-Commit-Position: refs/branch-heads/2785@{#571}
Cr-Branched-From: 68623971be0cfc492a2cb0427d7f478e7b214c24-refs/heads/master@{#403382}

[modify] https://crrev.com/89fa8a4e8f4d77745e86b5176608b5d97204cf39/third_party/WebKit/Source/core/events/PromiseRejectionEvent.cpp
[modify] https://crrev.com/89fa8a4e8f4d77745e86b5176608b5d97204cf39/third_party/WebKit/Source/core/events/PromiseRejectionEvent.h


### aw...@chromium.org (2016-08-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-08)

Groovy! The panel has decided to reward $3,000 for this bug.  A member of our finance team will be in touch shortly.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### lo...@gmail.com (2016-09-20)

Almost two weeks but no contact, do you have my email?

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2016-11-17)

This issue was migrated from crbug.com/chromium/626893?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084797)*
