# Security: Task Scheduling - Use After Free in TaskQueueImpl::CreateTaskRunner().

| Field | Value |
|-------|-------|
| **Issue ID** | [40052809](https://issues.chromium.org/issues/40052809) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Workers, Internals>TaskScheduling |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | lo...@gmail.com |
| **Assignee** | nh...@chromium.org |
| **Created** | 2020-07-10 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

Specifically crafted HTML file and shared worker script can cause Use After Free of a TaskQueueImpl object in task scheduling code TaskQueueImpl::CreateTaskRunner(). This bug may be exploited to achieve one click remote code execution in renderer process.

```
TaskQueue owns the underlying implementation TaskQueueImpl:  
    std::unique_ptr<internal::TaskQueueImpl> impl_;  
  
The creation and deletion of  TaskQueueImpl happens in SequenceManager/SequenceManagerImpl.   
  
If task queue is shut down gracefully, the ownership of TaskQueueImpl is transfered (it's moved in TakeTaskQueueImpl() )when  TaskQueue is being destructed. So in this case TaskQueue does not outlive TaskQueueImpl.  
  
    TaskQueue::~TaskQueue()   
      TaskQueue::ShutdownTaskQueueGracefully()  
        impl_->sequence_manager()->ShutdownTaskQueueGracefully(TakeTaskQueueImpl());  
        SequenceManagerImpl::ShutdownTaskQueueGracefully(std::unique_ptr<internal::TaskQueueImpl> task_queue)  
            main_thread_only().queues_to_gracefully_shutdown[task_queue.get()] = std::move(task_queue);  
  
  
However, if close() method is called with the worker global scope inside the worker script, task queue is shut down forcefully. The ownership of TaskQueueImpl is transfered when TaskQueue::ShutdownTaskQueue() is called.  
  
  
    WebSharedWorkerImpl::DidCloseWorkerGlobalScope()  
      WebSharedWorkerImpl::TerminateWorkerThread()  
        WorkerThread::Terminate()  
        ...  
          WorkerThread::PrepareForShutdownOnWorkerThread()  
            WorkerScheduler::Dispose()  
              TaskQueue::ShutdownTaskQueue()  
                sequence_manager_->UnregisterTaskQueueImpl(TakeTaskQueueImpl());  
                SequenceManagerImpl::UnregisterTaskQueueImpl(std::unique_ptr<internal::TaskQueueImpl> task_queue)  
                  main_thread_only().queues_to_delete[task_queue.get()] = std::move(task_queue);  
              
Then TaskQueueImpl is destroyed asynchronously in CleanUpQueues():   

    SequenceManagerImpl::CleanUpQueues()      
      main_thread_only().queues_to_delete.clear()  
    
In this case TaskQueue can outlives TaskQueueImpl. On the surface, because impl_ (TaskQueueImpl) is managed by a std::unique_ptr, impl_ would become null cleanly after the TaskQueueImpl object is freed. It's true if the code runs in a single thread or sequential environment.  

However, worker related code runs in multiple threads. Some runs in renderer main thread, some runs in worker thread.  
To make sure the access to impl_ is thread safe, TaskQueue has a lock impl_lock_:  
   
   mutable base::internal::CheckedLock impl_lock_{base::internal::UniversalPredecessor{}};  
     
Unfortunately, the assumptions about what code runs on main thread and in which case the access needs lock are not always true.    
  
  
According to the following comment in sequence_manager.h, CreateTaskQueueWithType (to create TaskQueueImpl) should be called on main thread only:  
  
  // Creates a task queue with the given type, |spec| and args.  
  // Must be called on the main thread.  
  template <typename TaskQueueType, typename... Args>  
  scoped_refptr<TaskQueueType> CreateTaskQueueWithType(  
      const TaskQueue::Spec& spec,  
      Args&&... args) {  
    return WrapRefCounted(new TaskQueueType(CreateTaskQueueImpl(spec), spec,  
                                            std::forward<Args>(args)...));  
   
But it actually can be called from worker thread when worker scheduler is initialized:  
  
    WorkerThread::InitializeSchedulerOnWorkerThread()  
      WorkerScheduler::WorkerScheduler()  
        NonMainThreadSchedulerImpl::CreateTaskQueue()  
          NonMainThreadSchedulerHelper::NewTaskQueue()  
            SequenceManager::CreateTaskQueueWithType()  
                SequenceManagerImpl::CreateTaskQueueImpl()  
  
The TaskQueueImpl object created from worker thread can also be freed by worker thread:  
  
    WorkerThread::SimpleThreadImpl::Run()  
      ...  
        SequenceManagerImpl::DidRunTask()  
           SequenceManagerImpl::CleanUpQueues()  
        
Therefore, when impl_ (TaskQueueImpl) is accessed from main thread, the lock is actually needed to secure the access. The comment ("We only need to lock if we're not on the main thread") inside TaskQueue::CreateTaskRunner() is wrong  
  
    scoped_refptr<SingleThreadTaskRunner> TaskQueue::CreateTaskRunner(  
        TaskType task_type) {  
      // We only need to lock if we're not on the main thread.  
      base::internal::CheckedAutoLockMaybe lock(IsOnMainThread() ? &impl_lock_  
                                                                 : nullptr);  
      if (!impl_)  
        return CreateNullTaskRunner();  
      return impl_->CreateTaskRunner(task_type);  
    }  

The above code is misleading. The comment says only lock on non main thread; According to the function name IsOnMainThread(), there would be lock when it runs on main thread; But the function IsOnMainThread() actually returns false when it runs on main thread.   
  
IsOnMainThread() can only check if it's bound to the current thread:  
    bool TaskQueue::IsOnMainThread() const {  
      return associated_thread_->IsBoundToCurrentThread();  
    }      
      
If TaskQueue is created from worker thread as noted above, it's not bound to the main thread. So no lock in this case and it's subject to race condition.  

  
When shared worker is constructed in javascript, there are two mojo events that the renderer stub needs to process: "CreateSharedWorker" to create the worker thread and worker scheduler etc; and "Connect" to connect the document to the shared worker.  
  
    var worker = new SharedWorker("sharedworker.js");  
  
If the shared worker script has close() method call, as noted above the TaskQueueImpl object (associated with WorkerScheduler::pausable_task_queue_ ) is freed in worker thread. But the Connect logic is processed in renderer main thread, and it calls TaskQueue::CreateTaskRunner():  
  
    EmbeddedSharedWorkerStub::WorkerScriptEvaluated()  
      EmbeddedSharedWorkerStub::ConnectToChannel()  
        WebSharedWorkerImpl::Connect()  
          WorkerScheduler::GetTaskRunner()  
            TaskQueue::CreateTaskRunner()  
              TaskQueueImpl::CreateTaskRunner()  
                
There is a small window: address of impl_ (TaskQueueImpl) is copied in main thread; then the TaskQueueImpl object is freed in worker thread; then TaskQueueImpl::CreateTaskRunner() is executed in main thread. It leads to a Use After Free of the TaskQueueImpl object.  
  
The "feeefeeefeeefeee" memory patterns in the following crash state indicates a clear Use After Free. I also attached an ASAN report runs on a local ASAN build for your easy assessment.  
Please let the PoC runs for a while. In my testing on my machine with Xeon CPU, the race could be triggered from a few minutes to half an hour or so.  

```

**VERSION**  

Google Chrome 85.0.4183.16 (Official Build) dev (64-bit) (cohort: Dev-nonPGO)  

Revision e5f41a80568bb5f51f3468c3fbb92aac2fceab70-refs/branch-heads/4183@{#226}  

OS Windows 10 OS Version 1909 (Build 18363.900)  

JavaScript V8 8.5.210.8

**REPRODUCTION CASE** (The whole server code in combined in UAF\_CreateTaskRunner\_PoC.js)  

Main page code:  

<html><body><iframe id = "iframe0" ></iframe></body>  

<script>  

var iframe0 = document.getElementById("iframe0");  

iframe0.src = "iframe0.html";\n';  

setTimeout(function(){location.reload()},1200);  

</script></html>

```
iFrame code:  
    <script>  
    var worker = new SharedWorker("sharedworker.js");  
    setTimeout(function(){location.reload()},15);  
    </script>     

Shared worker code:  
    close();  

```

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

```
(7fa8.48d4): Access violation - code c0000005 (first chance)  
First chance exceptions are reported before any exception handling.  
This exception may be expected and handled.  
chrome!std::__1::__cxx_atomic_fetch_add [inlined in chrome!base::sequence_manager::internal::TaskQueueImpl::CreateTaskRunner+0x29]:  
00007ffb`4916a719 f083450001      lock add dword ptr [rbp],1 ss:feeefeee`feeefeee=????????  
8:154> r  
rax=0000024b59a40bb0 rbx=0000024b599f3c20 rcx=000000007ffe0380  
rdx=0000000000000001 rsi=0000008cc5bfeab8 rdi=0000024b59a40bb0  
rip=00007ffb4916a719 rsp=0000008cc5bfe9c0 rbp=feeefeeefeeefeee  
 r8=0000024b59a40bb0  r9=0000000000000000 r10=0000024b56ba0000  
r11=0000008cc5bfe920 r12=0000024b56bb2601 r13=0000000000000000  
r14=0000000050ae0501 r15=00007ffb502f1de2  
iopl=0         nv up ei ng nz na po nc  
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010286  
chrome!std::__1::__cxx_atomic_fetch_add [inlined in chrome!base::sequence_manager::internal::TaskQueueImpl::CreateTaskRunner+0x29]:  
00007ffb`4916a719 f083450001      lock add dword ptr [rbp],1 ss:feeefeee`feeefeee=????????  
8:154> k  
 # Child-SP          RetAddr           Call Site  
00 (Inline Function) --------`-------- chrome!std::__1::__cxx_atomic_fetch_add [c:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\atomic @ 1014]   
01 (Inline Function) --------`-------- chrome!std::__1::__atomic_base<int,1>::fetch_add [c:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\atomic @ 1575]   
02 (Inline Function) --------`-------- chrome!base::AtomicRefCount::Increment [c:\b\s\w\ir\cache\builder\src\base\atomic_ref_count.h @ 28]   
03 (Inline Function) --------`-------- chrome!base::AtomicRefCount::Increment [c:\b\s\w\ir\cache\builder\src\base\atomic_ref_count.h @ 23]   
04 (Inline Function) --------`-------- chrome!base::subtle::RefCountedThreadSafeBase::AddRefImpl [c:\b\s\w\ir\cache\builder\src\base\memory\ref_counted.h @ 199]   
05 (Inline Function) --------`-------- chrome!base::subtle::RefCountedThreadSafeBase::AddRef [c:\b\s\w\ir\cache\builder\src\base\memory\ref_counted.h @ 171]   
06 (Inline Function) --------`-------- chrome!base::RefCountedThreadSafe<base::sequence_manager::internal::AssociatedThreadId,base::DefaultRefCountedThreadSafeTraits<base::sequence_manager::internal::AssociatedThreadId> >::AddRefImpl [c:\b\s\w\ir\cache\builder\src\base\memory\ref_counted.h @ 415]   
07 (Inline Function) --------`-------- chrome!base::RefCountedThreadSafe<base::sequence_manager::internal::AssociatedThreadId,base::DefaultRefCountedThreadSafeTraits<base::sequence_manager::internal::AssociatedThreadId> >::AddRef [c:\b\s\w\ir\cache\builder\src\base\memory\ref_counted.h @ 395]   
08 (Inline Function) --------`-------- chrome!scoped_refptr<base::sequence_manager::internal::AssociatedThreadId>::AddRef [c:\b\s\w\ir\cache\builder\src\base\memory\scoped_refptr.h @ 316]   
09 (Inline Function) --------`-------- chrome!scoped_refptr<base::sequence_manager::internal::AssociatedThreadId>::scoped_refptr+0x5 [c:\b\s\w\ir\cache\builder\src\base\memory\scoped_refptr.h @ 192]   
0a (Inline Function) --------`-------- chrome!scoped_refptr<base::sequence_manager::internal::AssociatedThreadId>::scoped_refptr+0x9 [c:\b\s\w\ir\cache\builder\src\base\memory\scoped_refptr.h @ 197]   
0b (Inline Function) --------`-------- chrome!base::MakeRefCounted+0x16 [c:\b\s\w\ir\cache\builder\src\base\memory\scoped_refptr.h @ 99]   
0c 0000008c`c5bfe9c0 00007ffb`4b9c76cc chrome!base::sequence_manager::internal::TaskQueueImpl::CreateTaskRunner+0x29 [c:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\task_queue_impl.cc @ 172]   
0d 0000008c`c5bfea10 00007ffb`4b6425b6 chrome!base::sequence_manager::TaskQueue::CreateTaskRunner+0x4c [c:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\task_queue.cc @ 192]   
0e (Inline Function) --------`-------- chrome!scoped_refptr<blink::scheduler::NonMainThreadTaskQueue>::operator->+0xc [c:\b\s\w\ir\cache\builder\src\base\memory\scoped_refptr.h @ 236]   
0f 0000008c`c5bfea60 00007ffb`4f23fbff chrome!blink::scheduler::WorkerScheduler::GetTaskRunner+0x2e [c:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\scheduler\worker\worker_scheduler.cc @ 218]   
10 (Inline Function) --------`-------- chrome!blink::WorkerThread::GetTaskRunner+0x11 [c:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\worker_thread.h @ 233]   
11 0000008c`c5bfea90 00007ffb`4ee81795 chrome!blink::WebSharedWorkerImpl::Connect+0x9f [c:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\exported\web_shared_worker_impl.cc @ 152]   
12 0000008c`c5bfeb40 00007ffb`4ee81700 chrome!content::EmbeddedSharedWorkerStub::ConnectToChannel+0x45 [c:\b\s\w\ir\cache\builder\src\content\renderer\worker\embedded_shared_worker_stub.cc @ 205]   
13 0000008c`c5bfeba0 00007ffb`49175e90 chrome!content::EmbeddedSharedWorkerStub::WorkerScriptEvaluated+0x50 [c:\b\s\w\ir\cache\builder\src\content\renderer\worker\embedded_shared_worker_stub.cc @ 152]   
14 (Inline Function) --------`-------- chrome!base::OnceCallback<void ()>::Run+0x12 [c:\b\s\w\ir\cache\builder\src\base\callback.h @ 99]   
15 0000008c`c5bfec00 00007ffb`4c2bb8f7 chrome!base::TaskAnnotator::RunTask+0x130 [c:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc @ 142]   
16 0000008c`c5bfed10 00007ffb`4c2bb656 chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl+0x167 [c:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 334]   
17 0000008c`c5bfee70 00007ffb`49173cac chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork+0x96 [c:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 255]   
18 0000008c`c5bfeef0 00007ffb`49173bb8 chrome!base::MessagePumpDefault::Run+0x7c [c:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc @ 41]   
19 0000008c`c5bfef70 00007ffb`4917361a chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0xb8 [c:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 460]   
1a 0000008c`c5bfefd0 00007ffb`4c1b9f58 chrome!base::RunLoop::Run+0x1aa [c:\b\s\w\ir\cache\builder\src\base\run_loop.cc @ 126]   
1b 0000008c`c5bff070 00007ffb`4918583d chrome!content::RendererMain+0x324 [c:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc @ 231]   
1c 0000008c`c5bff210 00007ffb`4916f4bf chrome!content::ContentMainRunnerImpl::Run+0x111 [c:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 882]   
1d 0000008c`c5bff2b0 00007ffb`4916ef3f chrome!service_manager::Main+0x4c7 [c:\b\s\w\ir\cache\builder\src\services\service_manager\embedder\main.cc @ 453]   
1e 0000008c`c5bff580 00007ffb`49163a12 chrome!content::ContentMain+0x3e [c:\b\s\w\ir\cache\builder\src\content\app\content_main.cc @ 19]   
1f 0000008c`c5bff610 00007ff7`afde253c chrome!ChromeMain+0x10a [c:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc @ 121]   
20 0000008c`c5bff700 00007ff7`afde19be chrome_exe!MainDllLoader::Launch+0x13c [c:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc @ 164]   
21 0000008c`c5bff790 00007ff7`afeff3a2 chrome_exe!wWinMain+0x9be [c:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc @ 271]   
22 (Inline Function) --------`-------- chrome_exe!invoke_main+0x21 [d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 118]   
23 0000008c`c5bffb60 00007ffb`e47f7bd4 chrome_exe!__scrt_common_main_seh+0x106 [d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 288]   
24 0000008c`c5bffba0 00007ffb`e56ace51 KERNEL32!BaseThreadInitThunk+0x14  
25 0000008c`c5bffbd0 00000000`00000000 ntdll!RtlUserThreadStart+0x21  
8:154> dv  
            __a = 0xfeeefeee`feeefeee  
        __delta = <value unavailable>  
        __order = <value unavailable>  
8:154> dx Debugger.Sessions[0].Processes[32680].Threads[18644].Stack.Frames[12].SwitchTo();dv /t /v  
Debugger.Sessions[0].Processes[32680].Threads[18644].Stack.Frames[12].SwitchTo()  
@rbx              class base::sequence_manager::internal::TaskQueueImpl \* this = 0x0000024b`599f3c20  
@r14b             unsigned char task_type = 0x01 ''  
8:154> dv  
           this = 0x0000024b`599f3c20  
      task_type = 0x01 ''  
8:154> dx -id 0,8 -r1 ((chrome!base::sequence_manager::internal::TaskQueueImpl \*)0x24b599f3c20)  
Error: Unable to find type 'base::sequence_manager::internal::TaskQueueImpl \*' for cast.  
8:154> dp 0x24b599f3c20  
0000024b`599f3c20  0000024b`59a13f80 0000024b`597b9780  
0000024b`599f3c30  feeefeee`feeefeee feeefeee`feeefeee  
0000024b`599f3c40  feeefeee`feeefeee feeefeee`feeefeee  
0000024b`599f3c50  feeefeee`feeefeee feeefeee`feeefeee  
0000024b`599f3c60  feeefeee`feeefeee feeefeee`feeefeee  
0000024b`599f3c70  feeefeee`feeefeee feeefeee`feeefeee  
0000024b`599f3c80  feeefeee`feeefeee feeefeee`feeefeee  
0000024b`599f3c90  feeefeee`feeefeee feeefeee`feeefeee  

```

## Attachments

- [UAF_CreateTaskRunner_PoC.js](attachments/UAF_CreateTaskRunner_PoC.js) (text/plain, 1.3 KB)
- [UAF_CreateTaskRunner_ASAN.txt](attachments/UAF_CreateTaskRunner_ASAN.txt) (text/plain, 16.7 KB)

## Timeline

### lo...@gmail.com (2020-07-10)

Please run the PoC in NodeJS:

node UAF_CreateTaskRunner_PoC.js

### cl...@chromium.org (2020-07-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5642562680979456.

### cl...@chromium.org (2020-07-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5699571252002816.

### mm...@chromium.org (2020-07-11)

Ok, let me try running it locally for a while...

### lo...@gmail.com (2020-07-13)

The bug affects stable channel:


Google Chrome	83.0.4103.116 (Official Build) (64-bit) (cohort: Stable)
Revision	8f0c18b4dca9b6699eb629be0f51810c24fb6428-refs/branch-heads/4103@{#716}
OS	Windows 10 OS Version 1909 (Build 18363.900)
JavaScript	V8 8.3.110.13

(14a0.4e58): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
chrome!std::__1::__cxx_atomic_fetch_add [inlined in chrome!base::sequence_manager::internal::TaskQueueImpl::CreateTaskRunner+0x29]:
00007ffb`7395ab09 f083450001      lock add dword ptr [rbp],1 ss:feeefeee`feeefeee=????????
8:109> r
rax=000001c7659dd490 rbx=000001c7659de110 rcx=000000007ffe0380
rdx=0000000000000001 rsi=000000b80fdfea88 rdi=000001c7659dd490
rip=00007ffb7395ab09 rsp=000000b80fdfe990 rbp=feeefeeefeeefeee
 r8=000001c7659dd490  r9=0000000000000000 r10=000001c75eb00000
r11=000000b80fdfe8f0 r12=0000000000000000 r13=0000000000000000
r14=000000007b046e01 r15=00007ffb7a86e852
iopl=0         nv up ei ng nz na po nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010286
chrome!std::__1::__cxx_atomic_fetch_add [inlined in chrome!base::sequence_manager::internal::TaskQueueImpl::CreateTaskRunner+0x29]:
00007ffb`7395ab09 f083450001      lock add dword ptr [rbp],1 ss:feeefeee`feeefeee=????????
8:109> k
 # Child-SP          RetAddr           Call Site
00 (Inline Function) --------`-------- chrome!std::__1::__cxx_atomic_fetch_add [c:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\atomic @ 1014] 
01 (Inline Function) --------`-------- chrome!std::__1::__atomic_base<int,1>::fetch_add [c:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\atomic @ 1575] 
02 (Inline Function) --------`-------- chrome!base::AtomicRefCount::Increment [c:\b\s\w\ir\cache\builder\src\base\atomic_ref_count.h @ 28] 
03 (Inline Function) --------`-------- chrome!base::AtomicRefCount::Increment [c:\b\s\w\ir\cache\builder\src\base\atomic_ref_count.h @ 23] 
04 (Inline Function) --------`-------- chrome!base::subtle::RefCountedThreadSafeBase::AddRefImpl [c:\b\s\w\ir\cache\builder\src\base\memory\ref_counted.h @ 208] 
05 (Inline Function) --------`-------- chrome!base::subtle::RefCountedThreadSafeBase::AddRef [c:\b\s\w\ir\cache\builder\src\base\memory\ref_counted.h @ 180] 
06 (Inline Function) --------`-------- chrome!base::RefCountedThreadSafe<base::sequence_manager::internal::AssociatedThreadId,base::DefaultRefCountedThreadSafeTraits<base::sequence_manager::internal::AssociatedThreadId>>::AddRefImpl [c:\b\s\w\ir\cache\builder\src\base\memory\ref_counted.h @ 422] 
07 (Inline Function) --------`-------- chrome!base::RefCountedThreadSafe<base::sequence_manager::internal::AssociatedThreadId,base::DefaultRefCountedThreadSafeTraits<base::sequence_manager::internal::AssociatedThreadId>>::AddRef [c:\b\s\w\ir\cache\builder\src\base\memory\ref_counted.h @ 402] 
08 (Inline Function) --------`-------- chrome!scoped_refptr<base::sequence_manager::internal::AssociatedThreadId>::AddRef [c:\b\s\w\ir\cache\builder\src\base\memory\scoped_refptr.h @ 316] 
09 (Inline Function) --------`-------- chrome!scoped_refptr<base::sequence_manager::internal::AssociatedThreadId>::scoped_refptr+0x5 [c:\b\s\w\ir\cache\builder\src\base\memory\scoped_refptr.h @ 192] 
0a (Inline Function) --------`-------- chrome!scoped_refptr<base::sequence_manager::internal::AssociatedThreadId>::scoped_refptr+0x9 [c:\b\s\w\ir\cache\builder\src\base\memory\scoped_refptr.h @ 197] 
0b (Inline Function) --------`-------- chrome!base::MakeRefCounted+0x16 [c:\b\s\w\ir\cache\builder\src\base\memory\scoped_refptr.h @ 99] 
0c 000000b8`0fdfe990 00007ffb`760b093c chrome!base::sequence_manager::internal::TaskQueueImpl::CreateTaskRunner+0x29 [c:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\task_queue_impl.cc @ 170] 
0d 000000b8`0fdfe9e0 00007ffb`75d3fb8a chrome!base::sequence_manager::TaskQueue::CreateTaskRunner+0x4c [c:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\task_queue.cc @ 192] 
0e (Inline Function) --------`-------- chrome!scoped_refptr<blink::scheduler::NonMainThreadTaskQueue>::operator->+0xc [c:\b\s\w\ir\cache\builder\src\base\memory\scoped_refptr.h @ 236] 
0f 000000b8`0fdfea30 00007ffb`797d629f chrome!blink::scheduler::WorkerScheduler::GetTaskRunner+0x2e [c:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\scheduler\worker\worker_scheduler.cc @ 218] 
10 (Inline Function) --------`-------- chrome!blink::WorkerThread::GetTaskRunner+0x11 [c:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\worker_thread.h @ 229] 
11 000000b8`0fdfea60 00007ffb`7941328f chrome!blink::WebSharedWorkerImpl::Connect+0x9f [c:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\exported\web_shared_worker_impl.cc @ 151] 
12 000000b8`0fdfeb10 00007ffb`794131fa chrome!content::EmbeddedSharedWorkerStub::ConnectToChannel+0x45 [c:\b\s\w\ir\cache\builder\src\content\renderer\worker\embedded_shared_worker_stub.cc @ 201] 
13 000000b8`0fdfeb70 00007ffb`739670d1 chrome!content::EmbeddedSharedWorkerStub::WorkerScriptEvaluated+0x50 [c:\b\s\w\ir\cache\builder\src\content\renderer\worker\embedded_shared_worker_stub.cc @ 148] 
14 (Inline Function) --------`-------- chrome!base::OnceCallback<void ()>::Run+0x12 [c:\b\s\w\ir\cache\builder\src\base\callback.h @ 98] 
15 000000b8`0fdfebd0 00007ffb`73964329 chrome!base::TaskAnnotator::RunTask+0x121 [c:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc @ 142] 
16 000000b8`0fdfecd0 00007ffb`769641b0 chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl+0x139 [c:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 325] 
17 000000b8`0fdfee10 00007ffb`7396418c chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork+0xa0 [c:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 250] 
18 000000b8`0fdfeea0 00007ffb`73964098 chrome!base::MessagePumpDefault::Run+0x7c [c:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc @ 41] 
19 000000b8`0fdfef20 00007ffb`73963afa chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0xb8 [c:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 437] 
1a 000000b8`0fdfef80 00007ffb`7686d6b0 chrome!base::RunLoop::Run+0x1aa [c:\b\s\w\ir\cache\builder\src\base\run_loop.cc @ 126] 
1b 000000b8`0fdff020 00007ffb`7397791d chrome!content::RendererMain+0x328 [c:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc @ 227] 
1c 000000b8`0fdff1c0 00007ffb`7395f6fb chrome!content::ContentMainRunnerImpl::Run+0x111 [c:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 882] 
1d 000000b8`0fdff260 00007ffb`7395f16f chrome!service_manager::Main+0x4d3 [c:\b\s\w\ir\cache\builder\src\services\service_manager\embedder\main.cc @ 454] 
1e 000000b8`0fdff530 00007ffb`739539b2 chrome!content::ContentMain+0x3e [c:\b\s\w\ir\cache\builder\src\content\app\content_main.cc @ 19] 
1f 000000b8`0fdff5c0 00007ff6`f66d256e chrome!ChromeMain+0x10a [c:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc @ 113] 
20 000000b8`0fdff6b0 00007ff6`f66d199c chrome_exe!MainDllLoader::Launch+0x146 [c:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc @ 177] 
21 000000b8`0fdff740 00007ff6`f67d5422 chrome_exe!wWinMain+0x99c [c:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc @ 271] 
22 (Inline Function) --------`-------- chrome_exe!invoke_main+0x21 [d:\agent\_work\3\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 118] 
23 000000b8`0fdffb20 00007ffb`e47f7bd4 chrome_exe!__scrt_common_main_seh+0x106 [d:\agent\_work\3\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 288] 
24 000000b8`0fdffb60 00007ffb`e56ace51 KERNEL32!BaseThreadInitThunk+0x14
25 000000b8`0fdffb90 00000000`00000000 ntdll!RtlUserThreadStart+0x21
8:109> dx Debugger.Sessions[0].Processes[5280].Threads[20056].Stack.Frames[12].SwitchTo();dv /t /v
Debugger.Sessions[0].Processes[5280].Threads[20056].Stack.Frames[12].SwitchTo()
@rbx              class base::sequence_manager::internal::TaskQueueImpl * this = 0x000001c7`659de110
@r14b             unsigned char task_type = 0x01 ''
8:109> dx -id 0,8 -r1 ((chrome!base::sequence_manager::internal::TaskQueueImpl *)0x1c7659de110)
Error: Unable to find type 'base::sequence_manager::internal::TaskQueueImpl *' for cast.
8:109> dp 0x1c7659de110
000001c7`659de110  000001c7`61988650 000001c7`659dafd0
000001c7`659de120  feeefeee`feeefeee feeefeee`feeefeee
000001c7`659de130  feeefeee`feeefeee feeefeee`feeefeee
000001c7`659de140  feeefeee`feeefeee feeefeee`feeefeee
000001c7`659de150  feeefeee`feeefeee feeefeee`feeefeee
000001c7`659de160  feeefeee`feeefeee feeefeee`feeefeee
000001c7`659de170  feeefeee`feeefeee feeefeee`feeefeee
000001c7`659de180  feeefeee`feeefeee feeefeee`feeefeee


### mm...@google.com (2020-07-13)

I was finally able to reproduce it

### mm...@chromium.org (2020-07-13)

nhiroki@, since you've fixed https://crbug.com/chromium/944424, could you please take a look into this one too? Or help route this please!

[Monorail components: Blink>Workers Internals>TaskScheduling]

### al...@chromium.org (2020-07-14)

Thanks for the report here! (To clarify a bit: in the scheduler code "main thread" refers to the "thread this SequenceManager is bound to" and for SequenceManager controlling the worker thread it's worker thread itself).

Yes, WorkerScheduler::GetTaskRunner is not thread-safe and should be called only from the worker thread. I believe that we had some logic which ensured that the task runners are initialised once on the worker thread and then stored later. Did we lose it at some point?

### [Deleted User] (2020-07-14)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-15)

[Empty comment from Monorail migration]

### fa...@chromium.org (2020-07-16)

Adding more workers.

### nh...@chromium.org (2020-07-20)

IIUC, WorkerScheduler::GetTaskRunner() is thread-safe but must not be accessed after worker thread termination starts. See this header comment:
https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/core/workers/worker_thread.h;l=230;drc=d712a91008849e605a7827d58ab0aa84dc9efc51

  // Returns a task runner bound to the per-global-scope scheduler's task queue.
  // You don't have to care about the lifetime of the associated global scope
  // and underlying thread. After the global scope is destroyed, queued tasks
  // are discarded and PostTask on the returned task runner just fails. This
  // function can be called on both the main thread and the worker thread.
  // You must not call this after Terminate() is called.
  scoped_refptr<base::SingleThreadTaskRunner> GetTaskRunner(TaskType type) {
    DCHECK(worker_scheduler_);
    return worker_scheduler_->GetTaskRunner(type);
  }

(Caution: This comment was written by me, so it can be wrong in the first place :p)

Regarding WebSharedWorkerImpl::Connect(), when shared worker termination is initiated from the main thread (e.g., when all connecting documents are gone), that obeys this rule by checking if termination has already started before calling WorkerScheduler::GetTaskRunner():
https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/core/exported/web_shared_worker_impl.cc;l=146;drc=d712a91008849e605a7827d58ab0aa84dc9efc51

void WebSharedWorkerImpl::Connect(MessagePortChannel web_channel) {
  DCHECK(IsMainThread());
  if (asked_to_terminate_)
    return;
  // The HTML spec requires to queue a connect event using the DOM manipulation
  // task source.
  // https://html.spec.whatwg.org/C/#shared-workers-and-the-sharedworker-interface
  PostCrossThreadTask(
      *GetWorkerThread()->GetTaskRunner(TaskType::kDOMManipulation), FROM_HERE,
      CrossThreadBindOnce(&WebSharedWorkerImpl::ConnectTaskOnWorkerThread,
                          WTF::CrossThreadUnretained(this),
                          WTF::Passed(std::move(web_channel))));
}

On the other hand, when SharedWorkerGlobalScope::close() is called from JS on the worker, this rule could be violated. In this case, WorkerThread::DidProcessTask() calls WorkerThread::PrepareForShutdownOnWorkerThread() that calls WorkerScheduler::Dispose(). Also, DidProcessTask() asynchronously calls WebSharedWorkerImpl::TerminateWorkerThread() that sets |asked_to_terminate_| on the main thread. Race condition can happen during this period. If connection request comes after WorkerScheduler::Dispose() on the worker thread and before WebSharedWorkerImpl::TerminateWorkerThread() on the main thread, WebSharedWorkerImpl::Connect() calls WorkerScheduler::GetTaskRunner() and results in the crash.

We could avoid this by adding some state check mechanism in WebSharedWorkerImpl and WorkerThread, but instead of that directly routing the Connect mojo message to SharedWorkerGlobalScope would be better solution here.

### nh...@chromium.org (2020-07-20)

> We could avoid this by adding some state check mechanism in WebSharedWorkerImpl and WorkerThread, but instead of that directly routing the Connect mojo message to SharedWorkerGlobalScope would be better solution here.

Probably the simple state check mechanism doesn't work. WebSharedWorkerImpl::Connect() needs to keep locking WorkerThread to prevent it from calling WorkerScheduler::Dispose().

### nh...@chromium.org (2020-07-20)

I suspect this could also happen on dedicated workers that provide close() JS API.

### nh...@chromium.org (2020-07-20)

As a stopgap, we could avoid the race condition by capturing the task runner between starting a worker thread (initializing WorkerScheduler) and posting a task to evaluate worker scripts that may call close().

### nh...@chromium.org (2020-07-21)

Reg https://crbug.com/chromium/1104046#c15, CL is now under review: https://chromium-review.googlesource.com/c/chromium/src/+/2308550

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c7bbec3e595c4359e36e5472b7265c4b6d047f2c

commit c7bbec3e595c4359e36e5472b7265c4b6d047f2c
Author: Hiroki Nakagawa <nhiroki@chromium.org>
Date: Tue Jul 21 07:13:34 2020

Worker: Fix a race condition on task runner handling

WebSharedWorkerImpl accesses WorkerScheduler from the main thread to
take a task runner, and then dispatches a connect event to
SharedWorkerGlobalScope using the task runner.

This causes a race condition if close() is called on the global scope
on the worker thread while the task runner is being taken on the main
thread: close() call disposes of WorkerScheduler, and accessing the
scheduler after that is not allowed. See the issue for details.

To fix this, this CL makes WebSharedWorkerImpl capture the task runner
between starting a worker thread (initializing WorkerScheduler) and
posting a task to evaluate worker scripts that may call close(). This
ensures that WebSharedWorkerImpl accesses WorkerScheduler before the
scheduler is disposed of.

Bug: 1104046
Change-Id: I145cd39f706019c33220fcb01ed81f76963ffff0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2308550
Commit-Queue: Hiroki Nakagawa <nhiroki@chromium.org>
Reviewed-by: Kenichi Ishibashi <bashi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#790284}

[modify] https://crrev.com/c7bbec3e595c4359e36e5472b7265c4b6d047f2c/third_party/blink/renderer/core/exported/web_shared_worker_impl.cc
[modify] https://crrev.com/c7bbec3e595c4359e36e5472b7265c4b6d047f2c/third_party/blink/renderer/core/exported/web_shared_worker_impl.h


### al...@chromium.org (2020-07-21)

Re #12: it's technically true that GetTaskRunner is thread-safe is we somehow synchronise to ensure that it's not accessed after the worker thread shutdown, but I think it would be much easier to use something similar to ParentExecutionContextTaskRunners, where we store the const references to SingleThreadTaskRunners we need which then can be safely accessed from any thread. 

### lo...@gmail.com (2020-07-27)

Thanks team for the prompt fix. Will the fix be merged to release channels?

### nh...@chromium.org (2020-07-31)

Sorry for no updates for a while.

loobenyang@: Could you check if the fix works on your environment? If it works well, I'll ask about merge.

altimin@: I cannot remember clearly, but I chatted with someone about the idea to capture the all task runner types on worker startup before and we decided not to do that maybe because of the cost of initializing unused task runner types. Anyway, now I think the idea should be safer and the cost should be negligible. I'll file a separate issue.

### al...@chromium.org (2020-07-31)

There is going to be some associated cost, but +1 to it being small enough and stability benefits being quite clear.

### lo...@gmail.com (2020-08-03)

Just tested it. I could not reproduce it on the latest dev channel build anymore:


Google Chrome	86.0.4214.2 (Official Build) dev (64-bit) (cohort: Dev)
Revision	e546911b21d22a6405093a0baff0566a04ac09fd-refs/branch-heads/4214@{#5}
OS	Windows 10 OS Version 2004 (Build 19041.388)
JavaScript	V8 8.6.238



### nh...@chromium.org (2020-08-03)

Thank you for checking it! For reference, the fix was landed in 86.0.4209.0 (sorry I should have mentioned this first).

Filed https://crbug.com/chromium/1112191 for capturing worker task runners.

### nh...@chromium.org (2020-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-03)

This bug requires manual review: M85's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### nh...@chromium.org (2020-08-03)

1. Does your merge fit within the Merge Decision Guidelines?

Yes.

2. Links to the CLs you are requesting to merge.

https://chromium-review.googlesource.com/c/chromium/src/+/2308550

3. Has the change landed and been verified on master/ToT?

Yes (see https://crbug.com/chromium/1104046#c22)

4. Why are these changes required in this milestone after branch?

This is marked as Security_Impact-Stable and Security_Severity-High. It should be better to deliver the fix as soon as possible.

5. Is this a new feature?

No. 

6. If it is a new feature, is it behind a flag using finch?

No.

### sr...@google.com (2020-08-03)

Merge approved for M85 branch:4183 please merge asap

### ad...@google.com (2020-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-03)

[Empty comment from Monorail migration]

### sr...@google.com (2020-08-03)

Please complete your merges to M85 branch before 2pm PST tuesday Aug 4th 2020, so they can be included in this week's beta release.

### ad...@google.com (2020-08-03)

Tomorrow Sheriffbot will request merge to M84 as well so I'll beat it to it. nhiroki@ please could you comment on any stability risks of the fix? It looks like a nice clear case where we're just adding a ref count, so presumably it's very low risk? If so we'll merge it to M84 late this week for release in next week's stable refresh.

### nh...@chromium.org (2020-08-04)

https://crbug.com/chromium/1104046#c30: Thanks! I'll land a merge CL soon.

https://crbug.com/chromium/1104046#c31: Yes, that should be low risk. It's great if we can merge it to M84 as well.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f30409143525e1127a48fb88e82457e907ba3506

commit f30409143525e1127a48fb88e82457e907ba3506
Author: Hiroki Nakagawa <nhiroki@chromium.org>
Date: Tue Aug 04 07:36:06 2020

[Merge to M85] Worker: Fix a race condition on task runner handling

WebSharedWorkerImpl accesses WorkerScheduler from the main thread to
take a task runner, and then dispatches a connect event to
SharedWorkerGlobalScope using the task runner.

This causes a race condition if close() is called on the global scope
on the worker thread while the task runner is being taken on the main
thread: close() call disposes of WorkerScheduler, and accessing the
scheduler after that is not allowed. See the issue for details.

To fix this, this CL makes WebSharedWorkerImpl capture the task runner
between starting a worker thread (initializing WorkerScheduler) and
posting a task to evaluate worker scripts that may call close(). This
ensures that WebSharedWorkerImpl accesses WorkerScheduler before the
scheduler is disposed of.

(cherry picked from commit c7bbec3e595c4359e36e5472b7265c4b6d047f2c)

Bug: 1104046
Change-Id: I145cd39f706019c33220fcb01ed81f76963ffff0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2308550
Commit-Queue: Hiroki Nakagawa <nhiroki@chromium.org>
Reviewed-by: Kenichi Ishibashi <bashi@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#790284}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2336315
Cr-Commit-Position: refs/branch-heads/4183@{#1190}
Cr-Branched-From: 740e9e8a40505392ba5c8e022a8024b3d018ca65-refs/heads/master@{#782793}

[modify] https://crrev.com/f30409143525e1127a48fb88e82457e907ba3506/third_party/blink/renderer/core/exported/web_shared_worker_impl.cc
[modify] https://crrev.com/f30409143525e1127a48fb88e82457e907ba3506/third_party/blink/renderer/core/exported/web_shared_worker_impl.h


### mm...@chromium.org (2020-08-05)

nhiroki@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### ad...@google.com (2020-08-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-08-05)

Congratulations! The VRP panel decided to award $7,500 for this report.

### ad...@google.com (2020-08-06)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-06)

Approving merge to M84, branch 4147, assuming this is still looking good in Canary.

### nh...@chromium.org (2020-08-07)

Thanks! I'm now making a merge CL to M84:
https://chromium-review.googlesource.com/c/chromium/src/+/2342337

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/72ee7c437c88cbdf6248c677d1c7505a0b29abe3

commit 72ee7c437c88cbdf6248c677d1c7505a0b29abe3
Author: Hiroki Nakagawa <nhiroki@chromium.org>
Date: Fri Aug 07 15:27:06 2020

[Merge to M84] Worker: Fix a race condition on task runner handling

WebSharedWorkerImpl accesses WorkerScheduler from the main thread to
take a task runner, and then dispatches a connect event to
SharedWorkerGlobalScope using the task runner.

This causes a race condition if close() is called on the global scope
on the worker thread while the task runner is being taken on the main
thread: close() call disposes of WorkerScheduler, and accessing the
scheduler after that is not allowed. See the issue for details.

To fix this, this CL makes WebSharedWorkerImpl capture the task runner
between starting a worker thread (initializing WorkerScheduler) and
posting a task to evaluate worker scripts that may call close(). This
ensures that WebSharedWorkerImpl accesses WorkerScheduler before the
scheduler is disposed of.

(cherry picked from commit c7bbec3e595c4359e36e5472b7265c4b6d047f2c)

Bug: 1104046
Change-Id: I145cd39f706019c33220fcb01ed81f76963ffff0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2308550
Commit-Queue: Hiroki Nakagawa <nhiroki@chromium.org>
Reviewed-by: Kenichi Ishibashi <bashi@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#790284}
Tbr: bashi@chromium.org
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2342337
Reviewed-by: Hiroki Nakagawa <nhiroki@chromium.org>
Cr-Commit-Position: refs/branch-heads/4147@{#1050}
Cr-Branched-From: 16307825352720ae04d898f37efa5449ad68b606-refs/heads/master@{#768962}

[modify] https://crrev.com/72ee7c437c88cbdf6248c677d1c7505a0b29abe3/third_party/blink/renderer/core/exported/web_shared_worker_impl.cc
[modify] https://crrev.com/72ee7c437c88cbdf6248c677d1c7505a0b29abe3/third_party/blink/renderer/core/exported/web_shared_worker_impl.h


### ad...@google.com (2020-08-07)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-07)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1104046?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Workers, Internals>TaskScheduling]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052809)*
