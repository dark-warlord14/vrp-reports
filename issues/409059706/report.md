# Use After Free in CompressedPointer::Load inside WorkerThread::DidProcessTask

| Field | Value |
|-------|-------|
| **Issue ID** | [409059706](https://issues.chromium.org/issues/409059706) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Workers |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** |  135.0.7049.41 |
| **Reporter** | [Deleted User] |
| **Assignee** | yy...@chromium.org |
| **Created** | 2025-04-07 |
| **Bounty** | $1,000.00 |

## Description

deleted

## Attachments

- [UAF_WorkerThread.js](attachments/UAF_WorkerThread.js) (text/javascript, 2.0 KB)
- [worker0.js](attachments/worker0.js) (text/javascript, 428 B)
- [em_worker.js](attachments/em_worker.js) (text/javascript, 40 B)
- [index.html](attachments/index.html) (text/html, 281 B)

## Timeline

### [Deleted User] (2025-04-07)

deleted

### cl...@appspot.gserviceaccount.com (2025-04-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5086183180664832.

### ma...@google.com (2025-04-09)

Attaching original PoC split into individual files that can be served from localhost with `python3 -m http.server`

### cl...@appspot.gserviceaccount.com (2025-04-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4646660487446528.

### ma...@google.com (2025-04-09)

FoundIn / Severity provisional. Over to V8 sheriff for triage. 

### sr...@google.com (2025-04-10)

This sounds like a bug in blink to me, not in V8.

### ml...@chromium.org (2025-04-10)

On first sight, this doesn't look like a GC issue but rather an issue with the usage in Blink worker code. After a heap was destroyed you are not allowed to access any objects any further.

During worker shutdown the heap is explicit destroyed after which we are not allowed to access objects on the managed heap any longer as teardown will unconditionally reclaim objects. Member won't keep alive any object in this phase.

Destruction was reordered a little bit in <https://chromium-review.googlesource.com/c/chromium/src/+/6234236/4/third_party/blink/renderer/core/workers/worker_backing_thread.cc>. This calls shutdown now after V8 was destroyed which destroyed the CppHeap. Shutdown closes the scheduler which claims that there's no tasks run after that.

Since this involves a CrossThreadPersistent this may just be an existing race on the worker code. I can help debug this.

### ml...@chromium.org (2025-04-10)

Thank you martinkr@ for splitting the POC. I could not yet reproduce on my fresh Chrome build but could repro on stable.

Crash: <https://crash.corp.google.com/browse?q=reportid=%278d0df30158caf7bf%27>

Based on the sample reports this issue probably exists for a very long time and is unrelated to any refactorings that happened in M135: <https://crash.corp.google.com/browse?q=expanded_custom_data.ChromeCrashProto.magic_signature_1.name%3D%27blink%3A%3AExecutionContext%3A%3AGetAgent%27#samplereports>

### ml...@chromium.org (2025-04-10)

fwiw, comment #0 claims that this is *not* a fixed offset from 0. However, comment #0 shows it's fixed from 0 (at 0x138) and crash/ reports also show fixed offset from 0.

Looking at the code I see:

- The crashing code is in `WorkerThread::DidProcessTask()` at `GlobalScope()->GetAgent()->event_loop()->PerformMicrotaskCheckpoint();` [1](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/workers/worker_thread.cc;l=311;drc=10d39cde3307a7249d2dd106684cf5467692f8de?q=blink::WorkerThread::DidProcessTask&ss=chromium).
- `GlobalScope()` retrives a `CrossThreadPersistent<WorkerOrWorkletGlobalScope>`.
- `CppHeap` explicitly nulls out all these references on teardown [2](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/heap/cppgc/heap-base.cc;l=250;drc=10d39cde3307a7249d2dd106684cf5467692f8de) before it reclaims the objects.

Now, whether the other thread always observes 0 or a stale value depends on synchronization protocols used: `Reset()` uses a release-store but the load using `GetValue()` isn't atomic because the type was never designed for true concurrency.

Being precise here this probably just a fixed offset from 0 on any CPU with strong ordering (x86 and friends) and in theory a UAF on weakly ordered CPUs (arm and friends). However, based on what I see here this seems a very narrow timing that's very hard to exploit. Also, there's no retry as an unsuccessful attempt would crash around 0, as op already noted.

### ml...@chromium.org (2025-04-10)

I managed to reproduce a crash with a DCHECK build. Seems like we manage to confuse the state machine involved with managing worker tear down [3](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/workers/worker_thread.cc;l=779?q=third_party%2Fblink%2Frenderer%2Fcore%2Fworkers%2Fworker_thread.cc:779&ss=chromium).

Moving this to Workers component. I am happy to help further but an expert in the worker code is probably better suited to handle this.

gn args

```
is_debug = false
is_component_build = false
enable_nacl = false
use_remoteexec = true
use_siso = true
dcheck_always_on = true

```

Stack trace:

```
[194530:33:0410/103533.094625:FATAL:third_party/blink/renderer/core/workers/worker_thread.cc:779] DCHECK failed: ThreadState::kReadyToShutdown == thread_state_ (2 vs. 1)
#0 0x55ac8be51882 base::debug::CollectStackTrace()
#1 0x55ac8be398b1 base::debug::StackTrace::StackTrace()
#2 0x55ac8bd37e5a logging::LogMessage::Flush()
#3 0x55ac8bd37d2c logging::LogMessage::~LogMessage()
#4 0x55ac8bd1b7b1 logging::(anonymous namespace)::DCheckLogMessage::~DCheckLogMessage()
#5 0x55ac8bd1b0f3 logging::CheckError::~CheckError()
#6 0x55ac91e255cd blink::WorkerThread::PerformShutdownOnWorkerThread()
#7 0x55ac91e26324 blink::WorkerThread::ChildThreadTerminatedOnWorkerThread()
#8 0x55ac91e06d89 blink::ThreadedMessagingProxyBase::WorkerThreadTerminated()
#9 0x55ac91df3d2a base::internal::Invoker<>::RunOnce()
#10 0x55ac848f47a1 base::OnceCallback<>::Run()
#11 0x55ac8bda764d base::TaskAnnotator::RunTaskImpl()
#12 0x55ac8bddd1eb base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl()
#13 0x55ac8bddc57b base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
#14 0x55ac8bddd985 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
#15 0x55ac8bd42b06 base::MessagePumpDefault::Run()
#16 0x55ac8bdde331 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run()
#17 0x55ac8bd7f266 base::RunLoop::Run()
#18 0x55ac8a6635ac blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run()

```

### ch...@google.com (2025-04-10)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-04-10)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### nh...@chromium.org (2025-04-10)

Thanks for reporting and debugging!

@yy...@chromium.org Can you take a look or forward this?

### yy...@chromium.org (2025-04-11)

Sure.
Reading the thread.  I first supposed that we need to check the `thread_state_` before accessing `GlobalScope()`, or we might access the local field in the shutdown procedure has started.
However, I still do not understand the possible execution path on prepareshutdown and proceedshutdown.
Let me take another look next week.

### yy...@chromium.org (2025-04-14)

A regular path to make this shutdown might be calling terminate().  However, as mentioned, GC can also trigger the shutdown procedure.  There might be race condition for the procedure.

Shutdown procedure expects the methods are executed in this order.
PrepareForShutdownOnWorkerThread() -> PerformShutdownOnWorkerThread().
However, if PerformShutdownOnWorkerThread() is called without PrepareForShutdownOnWorkerThread(), the check mentioned in #comment11 hit.


PerformShutdownOnWorkerThread() can be called in the following ways:
1. ThreadedMessagingProxyBase::ParentObjectDestroyed() is called while worker_thread_ is nullptr. This is called by DedicatedWorker Dispose(), and Dispose() is a part of dedicated worker pre-finalizer.
2. ThreadedObjectProxyBase::DidTerminateWorkerThread() is called.

PrepareForShutdownOnWorkerThread() can be called in the following ways:
1. WorkerThread::Terminate() is called.
2. GlobalScope is closing or task is force terminated before WorkerThread::DidProcessTask()
3. the thread has already been terminated at WorkerThread::InitializeOnWorkerThread().

I assume #comment9 is that GlobalScope() get freed before WorkerThread::DidProcessTask().  maybe while processing the task?


### yy...@chromium.org (2025-04-14)

For #comment10, I closed up:
#5 0x55ac8bd1b0f3 logging::CheckError::~CheckError()
#6 0x55ac91e255cd blink::WorkerThread::PerformShutdownOnWorkerThread()
#7 0x55ac91e26324 blink::WorkerThread::ChildThreadTerminatedOnWorkerThread()
#8 0x55ac91e06d89 blink::ThreadedMessagingProxyBase::WorkerThreadTerminated()
#9 0x55ac91df3d2a base::internal::Invoker<>::RunOnce()

blink::ThreadedMessagingProxyBase::WorkerThreadTerminated() should be:
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/workers/threaded_messaging_proxy_base.cc;l=131;drc=f26c656c77f508d1a40ab16489eff1b6f72bff8b

third_party/blink/renderer/modules/shared_storage/shared_storage_worklet_messaging_proxy.cc might not be the caller of this because the code seems not use SharedStorageWorklet, the caller should be:
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/workers/threaded_messaging_proxy_base.cc;l=127;drc=5e01cdc5efe08fe9bedf7cc1523b8094b626559d
It means ThreadedMessagingProxyBase::ParentObjectDestroyed() has been called while worker_thread_ is nullptr.

Then, the way to cause this is:
1. the function was called after worker_thread_ gets nullptr, which is https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/workers/threaded_messaging_proxy_base.cc;l=146;drc=5e01cdc5efe08fe9bedf7cc1523b8094b626559d
2. the function was called before worker_thread_ was set, which is before ThreadedMessagingProxyBase::InitializeWorkerThread() https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/workers/threaded_messaging_proxy_base.cc;l=77;drc=5e01cdc5efe08fe9bedf7cc1523b8094b626559d

But stepping back, if worker_thread_ is nullptr at this time, ChildThreadTerminatedOnWorkerThread() won't be called and the crash wont happen. 
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/workers/threaded_messaging_proxy_base.cc;l=157;drc=5e01cdc5efe08fe9bedf7cc1523b8094b626559d

Then, we must assume worker_thread_ exist at this time.
Hmm, then I should assume possible race on worker_thread_ ?

### yy...@chromium.org (2025-04-14)

@mlippautz@mlippautz@chromium.org Can I ask you advice on what is happening there?

### yy...@chromium.org (2025-04-14)

The question here is where prefinalizer run?
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/workers/dedicated_worker.h;l=65;drc=463fb6ad0f17051c4088bbcab4b528545c3c4df7

My best guess is that the prefinalizer run on the other thread and there can be a possible race on worker_thread_ state.
Dispose() has been called before worker_thread_ gets initialized.
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/workers/threaded_messaging_proxy_base.cc;l=122;drc=5e01cdc5efe08fe9bedf7cc1523b8094b626559d

However, worker_thread_ sets set before moving(worker_thread_).
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/workers/threaded_messaging_proxy_base.cc;l=146;drc=5e01cdc5efe08fe9bedf7cc1523b8094b626559d

Then, WorkerThread::ChildThreadTerminatedOnWorkerThread() can be called for this case.
Short workaround is adding a field that is protected by a lock, to tell the Dispose() had run or not.


### ml...@chromium.org (2025-04-14)

> My best guess is that the prefinalizer run on the other thread and there can be a possible race on worker\_thread\_ state.

Pre-finalizer is always run on the thread that allocated the object and owns the heap for the object. If the object is allocated on the main thread, then this gets run on the main thread and not the worker.

### yy...@chromium.org (2025-04-14)

DedicatedWorker is created at:
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/workers/dedicated_worker.cc;l=92;drc=5e01cdc5efe08fe9bedf7cc1523b8094b626559d

WorkerThread is created at:
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/workers/threaded_messaging_proxy_base.cc;l=77;drc=5e01cdc5efe08fe9bedf7cc1523b8094b626559d

PostCrossThreadTask is here:
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/workers/worker_thread.cc;l=176;drc=5e01cdc5efe08fe9bedf7cc1523b8094b626559d

Then, I assume they are in the same thread?  I got puzzled.

### ma...@google.com (2025-04-14)

Oof, apologies for misrouting this, my bad.

Assigning to yyanagisawa@ per [#comment15](https://issues.chromium.org/issues/409059706#comment15)

### dx...@google.com (2025-04-15)

Project: chromium/src  

Branch: main  

Author: Yoshisato Yanagisawa [yyanagisawa@chromium.org](mailto:yyanagisawa@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6456965>

Ensure ParentObjectDestroyed() is in the same sequence of initialization

---


Expand for full commit details
```
     
    To understand if crbug.com/409059706#comment19 is true, let me add a 
    sequence checker to ensure DedicatedWorker::Dispose() is executed with 
    the same sequence with the worker thread initialization. 
     
    Bug: 409059706 
    Change-Id: I123f989fb946f7b46e65ac7b46f274c36a081963 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6456965 
    Commit-Queue: Hiroki Nakagawa <nhiroki@chromium.org> 
    Reviewed-by: Keita Suzuki <suzukikeita@chromium.org> 
    Reviewed-by: Hiroki Nakagawa <nhiroki@chromium.org> 
    Auto-Submit: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1446916}

```

---

Files:

- M `third_party/blink/renderer/core/workers/threaded_messaging_proxy_base.cc`
- M `third_party/blink/renderer/core/workers/threaded_messaging_proxy_base.h`

---

Hash: eb3fcdb5935488c81c227a7d65b4b995db31c618  

Date:  Tue Apr 15 03:51:23 2025


---

### th...@chromium.org (2025-04-25)

[secondary shepherd] yyanagisawa@: If this issue is resolved, could you please mark it as fixed?

If it's not resolved, could you please comment summarizing what work is remaining?

### yy...@chromium.org (2025-04-28)

To mark this fixed, we need to identify the root cause of this issue and resolve the root cause.
In #comment19, I assumed that the root cause of this issue is prefinalizer run with the different thread of InitializeWorkerThread.
However, upon #comment21, it sounds not, but I am not confident.  I have added a sequence checker to verify the comment19 in #comment23.

There might not be a crash caused by the sequence check yet?  My guess might be wrong.  I need help to decide what to investigate next.

### ch...@google.com (2025-05-12)

yyanagisawa: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### yy...@chromium.org (2025-05-13)

DCHECK failed: ThreadState::kReadyToShutdown == thread_state_ (2 vs. 1) still exist but a sequence checker do not hit.

### yy...@chromium.org (2025-05-13)

If is_debug = false, this DCHECK failure won't happen.

The question I have had is if PostCrossThreadTask() is guaranteed.
I saw a crash like:
#5 0x55f11f09af33 logging::CheckError::~CheckError()
#6 0x55f124b5cacd blink::WorkerThread::PerformShutdownOnWorkerThread()
#7 0x55f124b5d824 blink::WorkerThread::ChildThreadTerminatedOnWorkerThread()
#8 0x55f124b3e886 blink::ThreadedMessagingProxyBase::WorkerThreadTerminated()
#9 0x55f124b2b9cc base::internal::Invoker<>::RunOnce()
#9 0x55f124b2b9cc base::internal::Invoker<>::RunOnce()
#10 0x55f117b851f1 base::OnceCallback<>::Run()
#11 0x55f11f1233dd base::TaskAnnotator::RunTaskImpl()
#12 0x55f11f158eeb base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl()
#13 0x55f11f15827b base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
#14 0x55f11f159695 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
#15 0x55f11f0be316 base::MessagePumpDefault::Run()
#16 0x55f11f15a04a base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run()
#17 0x55f11f0faec6 base::RunLoop::Run()
#18 0x55f11d189c9c blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run()
#19 0x55f11f1aa5e3 base::(anonymous namespace)::ThreadFunc()
#20 0x7f944bc68b7b (/usr/lib/x86_64-linux-gnu/libc.so.6+0x92b7a)
#21 0x7f944bce65f0 __clone
Task trace:
#0 0x55f124b3fcd4 blink::ThreadedObjectProxyBase::DidTerminateWorkerThread()
#1 0x55f124b5c28c blink::WorkerThread::Terminate()
#2 0x55f11f06edcd mojo::Connector::PostDispatchNextMessageFromPipe()
#3 0x55f11f582dd5 mojo::SimpleWatcher::Context::Notify()

blink::WorkerThread::Terminate()
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/workers/worker_thread.cc;l=262;drc=d225ba1d27141f2f431f62f31decee7e7bcd4f4d

blink::ThreadedObjectProxyBase::DidTerminateWorkerThread()
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/workers/worker_thread.cc;l=812;drc=c4d16e4480885ba044064093bc1b83e15136b9fa
(it is called by  WorkerThread::PerformShutdownOnWorkerThread())

PostCrossThreadTask here.
ThreadedMessagingProxyBase::WorkerThreadTerminated()
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/workers/threaded_messaging_proxy_base.cc;l=134;drc=c4d16e4480885ba044064093bc1b83e15136b9fa
It will eventually reach:
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/workers/worker_thread.cc;l=776;drc=c4d16e4480885ba044064093bc1b83e15136b9fa



### yy...@chromium.org (2025-05-13)

In <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/workers/worker_thread.cc;l=262;drc=d225ba1d27141f2f431f62f31decee7e7bcd4f4d>

```
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
}

```

WorkerThread::PrepareForShutdownOnWorkerThread looks executed before.
It changes the state to ready to shutdown:
<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/workers/worker_thread.cc;l=740;drc=c4d16e4480885ba044064093bc1b83e15136b9fa>

However, if the order is flipped, state\_ should not be guaranteed to be executed in this order.

### yy...@chromium.org (2025-05-13)

I wrote a proof of concept and I stopped to see the DCHECK since then. Then, I should think the execution order flipped by the PostCrossThreadTask() above?

```
$ git diff
diff --git a/third_party/blink/renderer/core/workers/worker_thread.cc b/third_party/blink/renderer/core/workers/worker_thread.cc
index e4d70bc0f5778..04cb81dbc5fcb 100644
--- a/third_party/blink/renderer/core/workers/worker_thread.cc
+++ b/third_party/blink/renderer/core/workers/worker_thread.cc
@@ -281,10 +281,12 @@ void WorkerThread::Terminate() {
       *task_runner, FROM_HERE,
       CrossThreadBindOnce(&WorkerThread::PrepareForShutdownOnWorkerThread,
                           CrossThreadUnretained(this)));
+#if 0
   PostCrossThreadTask(
       *task_runner, FROM_HERE,
       CrossThreadBindOnce(&WorkerThread::PerformShutdownOnWorkerThread,
                           CrossThreadUnretained(this)));
+#endif
 }
 
 void WorkerThread::TerminateForTesting() {
@@ -815,6 +817,14 @@ void WorkerThread::PerformShutdownOnWorkerThread() {
   // to clear the worker backing thread and stop thread execution in the system
   // level.
   shutdown_event->Signal();
+  bool requested_to_terminate = false;
+  {
+    base::AutoLock locker(lock_);
+    requested_to_terminate = requested_to_terminate_;
+  }
+  if (requested_to_terminate) {
+    PerformShutdownOnWorkerThread();
+  }
 }
 
 void WorkerThread::SetThreadState(ThreadState next_thread_state) {

```

### yy...@chromium.org (2025-05-14)

Hmm, #comment30 should not be the fix, it just stop calling PerformShutdownOnWorkerThread() from WorkerThread::Terminate().  If I made it called, I started to see the mismatch again X(

### yy...@chromium.org (2025-05-14)

I started to understand the situation.
In this code, a worker is created and nested workers are created.
When all nested workers are terminated, the worker should also be terminated.
https://chromium-review.googlesource.com/c/chromium/src/+/996554 has been introduced to ensure child workers are terminated before parents workers.

Then, the following stack trace might mean:
#6 0x55f124b5cacd blink::WorkerThread::PerformShutdownOnWorkerThread()
#7 0x55f124b5d824 blink::WorkerThread::ChildThreadTerminatedOnWorkerThread()
#8 0x55f124b3e886 blink::ThreadedMessagingProxyBase::WorkerThreadTerminated()
(snip)
Task trace:
#0 0x55f124b3fcd4 blink::ThreadedObjectProxyBase::DidTerminateWorkerThread()
#1 0x55f124b5c28c blink::WorkerThread::Terminate()
#2 0x55f11f06edcd mojo::Connector::PostDispatchNextMessageFromPipe()

blink::WorkerThread::Terminate() to terminate the last child.
blink::ThreadedObjectProxyBase::DidTerminateWorkerThread() to notify the last child destruction child.
blink::ThreadedMessagingProxyBase::WorkerThreadTerminated() run on parent execution context
blink::WorkerThread::ChildThreadTerminatedOnWorkerThread() runs in parents context to erase the child thread, since no other child while Terminate() has been executed, sequentially calls blink::WorkerThread::PerformShutdownOnWorkerThread().
At this time, race might happen.

https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/workers/worker_thread.cc;l=268;drc=d225ba1d27141f2f431f62f31decee7e7bcd4f4d to `requested_to_terminate_ = true;` has finished.
However, WorkerThread::PrepareForShutdownOnWorkerThread has never been executed (yeah, thread hope to the parent thread might have been set in the different thread via cross thread post task, but waiting for the current execution finishes.  The current execution just executed PerformShutdownOnWorkerThread() because the flag has been set.



### yy...@chromium.org (2025-05-14)

The question here is that WorkerThread::PerformShutdownOnWorkerThread() would eventually been executed if requested_to_terminate_ is set.  Then, why do we need a manual execution in https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/workers/worker_thread.cc;l=437;drc=4a1f2646209c5ecc0aae120e3654feb6d3f393f3?

The other thought is that the issue happened because requested_to_terminate_ = true before PrepareForShutdownOnWorkerThread().  Is it possible to postpone setting requested_to_terminate_.

Since PrepareForShutdownOnWorkerThread() looks not re-entrant.  Is it safe to call PrepareForShutdownOnWorkerThread() twice?

Considering https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/workers/worker_thread.cc;l=785;drc=4a1f2646209c5ecc0aae120e3654feb6d3f393f3, the function call may return without doing the shutdown procedure.

1. Terminate() may run the prepare and perform shutdown of the thread.
2. perform shutdown does nothing if there are child processes.
3. perform shutdown will be called if Terminate() was called and no child processes.

Expectation.
#child_process = 0 & Terminate is called -> perform shutdown.
shutdown should be executed in the following procedure. prepare -> perform.
i.e. prepare should be executed before perform.
prepare is re-entrant, if it is executed twice, latter is just ignored. ... why we cannot take a strategy that prepare every time before perform?


### yy...@chromium.org (2025-05-14)

Terminate consideration.
Option A.
1. requested_to_terminate_ 
2. Prepare
3. Perform
(Other thread see the flag after 1 and DCHECK fail, which we observe now)

Option B.
1. prepare
2.  requested_to_terminate_ 
3. Perform
When other thread see the flag, it should always be after prepare.  The DCHECK failure won't happen.
Since it is other thread, actual prepare task may run before requested_to_terminate_ is set.
Technically, WorkerThread::Terminate() can be called multiple times, and procedure until 2 may run multiple times.

Option C.
1. prepare
2. Perform
3.  requested_to_terminate_ 
Same issue with Option B.

Option D.
1. yet another reentrant prevention flag or enum to explain the phase is set.
2. prepare
3.  requested_to_terminate_ 
4. Perform
Option B issue can be prevented because step 1 tells the Terminate() is under execution.
When the other thread see requested_to_terminate_ , it can understand that it is before prepare step, and not ready to go.
However, perform can still be executed twice if there is a lag between 3 and 4? Just after 3 to run perform, and 4 is also added.

Option E.
1. yet another reentrant prevention flag or enum to explain the phase is set.
2. prepare
3. Perform
4.  requested_to_terminate_ 
Option B issue can be prevented because step 1 tells the Terminate() is under execution.
When the other thread see requested_to_terminate_ , it can understand that it is before prepare step, and not ready to go.
Still perform may run twice?

### yy...@chromium.org (2025-05-14)

Upon a discussion with mikt@, and I started to think that the function does not care the number of children can be a problem.
1. lock and reentrant prevention flag is set.
2. prepare
3. lock
3-1. ensure the flag is not termination owner.
3-2. flip the flag to ready to terminate
3-3 if #child process = 0 -> I own the termination.
3-3-1. set the flag to termination owner.
3-3-2. Perform terminate
3-4. not owner, just returns.

#children=0 check thread
1. lock
2. #child process is 0 and the flag is ready to terminate
2-1. set the flag to termination owner.
2-1-1. unlock and perform terminate
2-2. not owner, just returns



### yy...@chromium.org (2025-05-14)

Just calling 2. prepare should not be prepared because it can be inflight, and #children=0 check thread may run before prepare task run.
Will revisit the case tomorrow, but I started to think that we can directly call prepared for the case.

### yy...@chromium.org (2025-05-15)

Re: #comment36
It should be wrong.  The call MUST be serialized after PrepareShutdownOnWorkerThread() because no WorkerThread fields can be accessed after successful PerformShutdownOnWorkerThread().  Therefore, 
#children=0 check thread
2-1-1. unlock and perform terminate should be just post tasked to make Perform queued after the Prepare.
Or, Prepare may cause use-after-free.

### dx...@google.com (2025-05-22)

Project: chromium/src  

Branch: main  

Author: Yoshisato Yanagisawa [yyanagisawa@chromium.org](mailto:yyanagisawa@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6543412>

Enforce SharedWorker::Terminate() procedure order

---


Expand for full commit details
```
     
    During the investigation of crbug.com/409059706, we observed that 
    PerformShutdownOnWorkerThread() is called during the status is 
    running. 
     
    I suppose the root cause is race condition between `Terminate()` 
    procedure and a child process termination procedure in different 
    thread.  WorkerThread can be terminated if two conditions are met; 
    `Terminate()` is called and all child worker threads have been 
    terminated.  Both `Terminate()` and the child process termination 
    procedure may call `PerformShutdownOnWorkerThread()`, and former 
    is executed regardless of two conditions are met.  The latter 
    is called if `Terminate()` is called and no child processes. 
    To be clear, "`Terminate()` is called" does not mean 
    `PrepareForShutdownOnWorkerThread()` is executed.  `Terminate()` 
    queues it after the flag to tell `Terminate()` call.  And, when 
    the issue happen, I am quite sure the flag is set but, 
    `PrepareForShutdownOnWorkerThread()` won't be executed yet. 
     
    The fix is that: 
    1. The "Terminate() is called" flag to be multi staged. 
       The flag is used for two purpose; a. avoid re-enter of 
      `Terminate()`, and b. `PrepareForShutdownOnWorkerThread()` is 
      in flight. The CL changed the flag to enum to represent 
      the stage properly. 
    2. `PerformShutdownOnWorkerThread()` is queued even if it is 
       called within the child process termination procedure. 
       It avoid the execution order flip between 
       `PrepareForShutdownOnWorkerThread()` and 
       `PerformShutdownOnWorkerThread()`. 
     
    In addition, this change ensures `PerformShutdownOnWorkerThread()` 
    is called once.  While `PerformShutdownOnWorkerThread()` touches 
    fields inside, the fields must not be touched at some point within 
    the function, the function is actually not re-entrant when it reaches 
    to the end.  Upon mikt@ suggestion, I made 
    `PerformShutdownOnWorkerThread()` is called only when two conditions 
    are fulfilled. i.e. `Terminate()` is called and the number of child 
    threads is 0.  Also, the CL uses the enum to show 
    `PerformShutdownOnWorkerThread()` is in-flight to avoid re-entrance 
    in this level. 
     
    Bug: 409059706 
    Change-Id: I81a1c3b1a34e827fa75ec2d1a9b37023965dbe27 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6543412 
    Reviewed-by: Hiroki Nakagawa <nhiroki@chromium.org> 
    Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1463892}

```

---

Files:

- M `third_party/blink/common/features.cc`
- M `third_party/blink/public/common/features.h`
- M `third_party/blink/renderer/core/workers/worker_thread.cc`
- M `third_party/blink/renderer/core/workers/worker_thread.h`

---

Hash: f1e6422a355c016e5f2c22619181f7f121d1f511  

Date:  Thu May 22 06:25:12 2025


---

### yy...@chromium.org (2025-05-22)

With #comment38 CL, both the UAF and termination step race mentioned in #comment11 have been fixed.

### ch...@google.com (2025-05-22)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### [Deleted User] (2025-05-22)

deleted

### ch...@google.com (2025-05-22)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M136. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M137. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [136, 137].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### yy...@chromium.org (2025-05-23)

Re: #comment41

I confirmed destruction state won't go wrong with the test vector in #comment4.  However, please feel free to try the patch.  Rollout of the canary with the change may take time.

Re: #comment42

1. Which CLs should be backmerged? (Please include Gerrit links.)

https://chromium-review.googlesource.com/c/chromium/src/+/6543412

2. Has this fix been verified on Canary to not pose any stability regressions?

The change is included in 138.0.7195.0.

3. Does this fix pose any potential non-verifiable stability risks?

I do not think so.

4. Does this fix pose any known compatibility risks?

I do not think so.

5. Does it require manual verification by the test team? If so, please describe required testing.

It is not mandatory.  If the manual verifier can follow #comment4 and #comment11, it might be good.

6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

done.
I assume this may affect OSes using Blink.

### am...@chromium.org (2025-05-27)

reviewed Canary data for this change landed 21 May, no issues related to this fix have manifested
M137 merge approved for https://crrev.com/c/6543412, please merge this fix to branch 7151 at your earliest convenience / by EOD Thursday so this fix can be included in next week's M137 Stable update 

please hold off on merging to M136 at this time; the first release of M136 Extended Stable has not yet shipped, so this should only be backmerged after that happens
someone will review this later in the week and update with approval at that time

### dx...@google.com (2025-05-28)

Project: chromium/src  

Branch: refs/branch-heads/7151  

Author: Yoshisato Yanagisawa [yyanagisawa@chromium.org](mailto:yyanagisawa@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6595647>

[M137] Enforce SharedWorker::Terminate() procedure order

---


Expand for full commit details
```
     
    During the investigation of crbug.com/409059706, we observed that 
    PerformShutdownOnWorkerThread() is called during the status is 
    running. 
     
    I suppose the root cause is race condition between `Terminate()` 
    procedure and a child process termination procedure in different 
    thread.  WorkerThread can be terminated if two conditions are met; 
    `Terminate()` is called and all child worker threads have been 
    terminated.  Both `Terminate()` and the child process termination 
    procedure may call `PerformShutdownOnWorkerThread()`, and former 
    is executed regardless of two conditions are met.  The latter 
    is called if `Terminate()` is called and no child processes. 
    To be clear, "`Terminate()` is called" does not mean 
    `PrepareForShutdownOnWorkerThread()` is executed.  `Terminate()` 
    queues it after the flag to tell `Terminate()` call.  And, when 
    the issue happen, I am quite sure the flag is set but, 
    `PrepareForShutdownOnWorkerThread()` won't be executed yet. 
     
    The fix is that: 
    1. The "Terminate() is called" flag to be multi staged. 
       The flag is used for two purpose; a. avoid re-enter of 
      `Terminate()`, and b. `PrepareForShutdownOnWorkerThread()` is 
      in flight. The CL changed the flag to enum to represent 
      the stage properly. 
    2. `PerformShutdownOnWorkerThread()` is queued even if it is 
       called within the child process termination procedure. 
       It avoid the execution order flip between 
       `PrepareForShutdownOnWorkerThread()` and 
       `PerformShutdownOnWorkerThread()`. 
     
    In addition, this change ensures `PerformShutdownOnWorkerThread()` 
    is called once.  While `PerformShutdownOnWorkerThread()` touches 
    fields inside, the fields must not be touched at some point within 
    the function, the function is actually not re-entrant when it reaches 
    to the end.  Upon mikt@ suggestion, I made 
    `PerformShutdownOnWorkerThread()` is called only when two conditions 
    are fulfilled. i.e. `Terminate()` is called and the number of child 
    threads is 0.  Also, the CL uses the enum to show 
    `PerformShutdownOnWorkerThread()` is in-flight to avoid re-entrance 
    in this level. 
     
    (cherry picked from commit f1e6422a355c016e5f2c22619181f7f121d1f511) 
     
    Bug: 409059706 
    Change-Id: I81a1c3b1a34e827fa75ec2d1a9b37023965dbe27 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6543412 
    Reviewed-by: Hiroki Nakagawa <nhiroki@chromium.org> 
    Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1463892} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6595647 
    Auto-Submit: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Commit-Queue: Hiroki Nakagawa <nhiroki@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7151@{#1844} 
    Cr-Branched-From: 8e0d32ed6e49a2415b16e5ed402957cac2349ce2-refs/heads/main@{#1453031}

```

---

Files:

- M `third_party/blink/common/features.cc`
- M `third_party/blink/public/common/features.h`
- M `third_party/blink/renderer/core/workers/worker_thread.cc`
- M `third_party/blink/renderer/core/workers/worker_thread.h`

---

Hash: 9fb5e8af020a54fc74258e65b5d8453b494c241e  

Date:  Wed May 28 03:11:06 2025


---

### pe...@google.com (2025-05-28)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### yy...@chromium.org (2025-05-28)

Re: #comment46

1. Was this issue a regression for the milestone it was found in?

No.  I guess the behavior has been introduced as a part of https://issues.chromium.org/issues/40570188
It has been implemented in 2018 (almost 7 years ago).

2. Is this issue related to a change or feature merged after the latest LTS Milestone?

No.  It is a fix for the bug implemented in 2018.

### am...@chromium.org (2025-05-28)

Downgrading to medium severity as this issue is pretty significantly mitigated and would be difficult to exploit in a real world scenario, especially referencing [comment #10](https://issues.chromium.org/issues/409059706#comment10), `Being precise here this probably just a fixed offset from 0 on any CPU with strong ordering (x86 and friends) and in theory a UAF on weakly ordered CPUs (arm and friends). However, based on what I see here this seems a very narrow timing that's very hard to exploit. Also, there's no retry as an unsuccessful attempt would crash around 0, as op already noted.`

Declining backmerge to extended stable / 136

### sp...@google.com (2025-05-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of highly mitigated memory corruption in a sandboxed process / renderer


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-05-29)

Thank you for your efforts and reporting this issue to us! I've re-cc'ed you as it appears you may have inadvertently removed yourself from access to this issue.

### [Deleted User] (2025-05-29)

deleted

### yy...@chromium.org (2025-05-29)

I suggest to pause the merge process because we are observing CHECK error at https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/workers/worker_thread.cc;l=452;drc=f1e6422a355c016e5f2c22619181f7f121d1f511
I believe it unlikely, and am trying to understand why.

### pe...@google.com (2025-05-30)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-05-30)

According to #52, I wait to merge this CL to M132 LTS until the CHECK error issue is solved.

### yy...@chromium.org (2025-06-02)

The CHECK error has been fixed in https://chromium-review.googlesource.com/c/chromium/src/+/6600912.
Waiting for its merge approval.

### yy...@chromium.org (2025-06-02)

Got approved for M138.

### yy...@chromium.org (2025-06-03)

Got rejected for M137 because of too few crash rate on M137.

### qk...@google.com (2025-06-19)

> Got rejected for M137 because of too few crash rate on M137.

@yy...@google.com, I'm considering merging the fix[1] to M132. Do you think  https://chromium-review.googlesource.com/c/chromium/src/+/6600912 should be merged to M132 as well? Because it was rejected for M137.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/6600489

### yy...@google.com (2025-06-19)

Re: #comment58
I recommend that because majority (>=95%) of the CHECK failure (crbug.com/420993774) is now coming from M137.
Of course the CHECK failure per day increased since it was rejected.

### qk...@google.com (2025-06-20)

Ok, then let me merge the fix for the CHECK failure to M132 as well. Thanks.

### pe...@google.com (2025-06-20)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-06-20)

1. https://chromium-review.googlesource.com/c/chromium/src/+/6600489 and https://chromium-review.googlesource.com/c/chromium/src/+/6656545
2. Low - There were a few conflicts.
3. 137
4. Yes. According to comment #47, the issue was introduced as a part of the implementation of https://issues.chromium.org/issues/40570188
implemented in 2018.

### gm...@google.com (2025-06-24)

@qk...@google.com I can approve the first Cl, I cannot approve the second one because it was only merge to 138 and we need to wait. I'll add the label approved but we need to add the Merge REquest again for the second CL until we can approve it.

### dx...@google.com (2025-06-25)

Project: chromium/src  

Branch: refs/branch-heads/6834  

Author: Yoshisato Yanagisawa [yyanagisawa@chromium.org](mailto:yyanagisawa@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6600489>

[M132-LTS] Enforce SharedWorker::Terminate() procedure order

---


Expand for full commit details
```
     
    During the investigation of crbug.com/409059706, we observed that 
    PerformShutdownOnWorkerThread() is called during the status is 
    running. 
     
    I suppose the root cause is race condition between `Terminate()` 
    procedure and a child process termination procedure in different 
    thread.  WorkerThread can be terminated if two conditions are met; 
    `Terminate()` is called and all child worker threads have been 
    terminated.  Both `Terminate()` and the child process termination 
    procedure may call `PerformShutdownOnWorkerThread()`, and former 
    is executed regardless of two conditions are met.  The latter 
    is called if `Terminate()` is called and no child processes. 
    To be clear, "`Terminate()` is called" does not mean 
    `PrepareForShutdownOnWorkerThread()` is executed.  `Terminate()` 
    queues it after the flag to tell `Terminate()` call.  And, when 
    the issue happen, I am quite sure the flag is set but, 
    `PrepareForShutdownOnWorkerThread()` won't be executed yet. 
     
    The fix is that: 
    1. The "Terminate() is called" flag to be multi staged. 
       The flag is used for two purpose; a. avoid re-enter of 
      `Terminate()`, and b. `PrepareForShutdownOnWorkerThread()` is 
      in flight. The CL changed the flag to enum to represent 
      the stage properly. 
    2. `PerformShutdownOnWorkerThread()` is queued even if it is 
       called within the child process termination procedure. 
       It avoid the execution order flip between 
       `PrepareForShutdownOnWorkerThread()` and 
       `PerformShutdownOnWorkerThread()`. 
     
    In addition, this change ensures `PerformShutdownOnWorkerThread()` 
    is called once.  While `PerformShutdownOnWorkerThread()` touches 
    fields inside, the fields must not be touched at some point within 
    the function, the function is actually not re-entrant when it reaches 
    to the end.  Upon mikt@ suggestion, I made 
    `PerformShutdownOnWorkerThread()` is called only when two conditions 
    are fulfilled. i.e. `Terminate()` is called and the number of child 
    threads is 0.  Also, the CL uses the enum to show 
    `PerformShutdownOnWorkerThread()` is in-flight to avoid re-entrance 
    in this level. 
     
    (cherry picked from commit f1e6422a355c016e5f2c22619181f7f121d1f511) 
     
    Bug: 409059706 
    Change-Id: I81a1c3b1a34e827fa75ec2d1a9b37023965dbe27 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6543412 
    Reviewed-by: Hiroki Nakagawa <nhiroki@chromium.org> 
    Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1463892} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6600489 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Owners-Override: Mohamed Omar <mohamedaomar@google.com> 
    Reviewed-by: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Reviewed-by: Mohamed Omar <mohamedaomar@google.com> 
    Cr-Commit-Position: refs/branch-heads/6834@{#5587} 
    Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```

---

Files:

- M `third_party/blink/common/features.cc`
- M `third_party/blink/public/common/features.h`
- M `third_party/blink/renderer/core/workers/worker_thread.cc`
- M `third_party/blink/renderer/core/workers/worker_thread.h`

---

Hash: a3e246f147808a8e1e42b170277c7403a3f6e04d  

Date:  Wed Jun 25 03:13:30 2025


---

### pe...@google.com (2025-06-25)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-06-25)

1. https://chromium-review.googlesource.com/c/chromium/src/+/6656545
2. Low - There was no conflict.
3. 138
4. Yes. As we decided in the comment #68, we needed to wait until the second CL is approved.


### ch...@google.com (2025-08-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of highly mitigated memory corruption in a sandboxed process / renderer

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/409059706)*
