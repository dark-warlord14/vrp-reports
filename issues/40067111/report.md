# memory corruption in perfetto

| Field | Value |
|-------|-------|
| **Issue ID** | [40067111](https://issues.chromium.org/issues/40067111) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Speed>Tracing |
| **Platforms** | Linux, Windows |
| **Reporter** | em...@gmail.com |
| **Assignee** | kh...@google.com |
| **Created** | 2023-07-09 |
| **Bounty** | $2,000.00 |

## Description

**Steps to reproduce the problem:**  

tested os:  

ubuntu 22.04  

tested chrome version:  

Chromium 113.0.5624.0 ~ Chromium 117.0.5878.0（Due to the sudden decrease in internet speed today, I am unable to confirm earlier versions.）  

repro steps:  

./chrome --no-sandbox --no-zygote --trace-config-file --disable-gpu --user-data-dir=/tmp/xx1 --incognito <http://localhost:8000/poc.html>

The flags '--no-zygote' and '--disable-gpu' are used to increase the reproducibility probability, but they are not necessary.  

However, the issue is not consistently reproducible. There are two other methods that can increase the repro probability:

method 1: Use the "launcher.sh" script provided in the attachment (modify the chrome path and the path to poc.html). This script will automatically launch multiple chrome processes to increase the reproducibility probability.  

Execute the following command:  

./launcher.sh 2>&1 | grep -E 'AddressSanitizer'  

If the browser doesn't crash after startup, press Ctrl+C and execute the above command again. Repetition of the command around 3-4 times should reproduce the issue.

method 2: Use the "test.js" script provided in the attachment (modify the chrome path and the path to poc.html). This script will automatically start and close multiple chrome processes indefinitely. The crash should be observed within 1-2 minutes.  

Instructions:

- Install Node.js and Puppeteer (<https://www.browserstack.com/guide/install-and-setup-puppeteer-with-npm-nodejs>).
- Execute the following command:  
  
  node ./test.js 2>&1 | grep -E 'AddressSanitizer'

**Problem Description:**  

==3608042==ERROR: AddressSanitizer: use-after-poison on address 0x7ef3005c2100 at pc 0x5635122ca0b8 bp 0x7ffbd75fc7b0 sp 0x7ffbd75fc7a8  

READ of size 8 at 0x7ef3005c2100 thread T2 (ThreadPoolForeg)  

#0 0x5635122ca0b7 in base::trace\_event::TraceLog::OnStop(perfetto::DataSourceBase::StopArgs const&) ./../../base/trace\_event/trace\_log.cc:2219:9  

#1 0x5635003ad693 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_functional/function.h:854:16  

#2 0x5635003ad693 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_functional/function.h:1168:12  

#3 0x5635003ad693 in ForEachObserverForRegistry ./../../third\_party/perfetto/src/tracing/internal/track\_event\_internal.cc:88:9  

#4 0x5635003ad693 in perfetto::internal::TrackEventInternal::OnStop(perfetto::internal::TrackEventCategoryRegistry const&, perfetto::DataSourceBase::StopArgs const&) ./../../third\_party/perfetto/src/tracing/internal/track\_event\_internal.cc:230:53  

#5 0x5635122b6591 in perfetto::internal::TrackEventDataSource<base::perfetto\_track\_event::TrackEvent, &base::perfetto\_track\_event::internal::kCategoryRegistry>::OnStop(perfetto::DataSourceBase::StopArgs const&) ./../../third\_party/perfetto/include/perfetto/tracing/internal/track\_event\_data\_source.h:267:5  

#6 0x56350038c331 in perfetto::internal::TracingMuxerImpl::StopDataSource\_AsyncBeginImpl(perfetto::internal::TracingMuxerImpl::FindDataSourceRes const&) ./../../third\_party/perfetto/src/tracing/internal/tracing\_muxer\_impl.cc:1496:37  

#7 0x563500391f50 in perfetto::internal::TracingMuxerImpl::AbortStartupTracingSession(unsigned long, perfetto::BackendType) ./../../third\_party/perfetto/src/tracing/internal/tracing\_muxer\_impl.cc:2520:11  

#8 0x5635122f8094 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_functional/function.h:854:16  

#9 0x5635122f8094 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_functional/function.h:1168:12  

#10 0x5635122f8094 in operator() ./../../base/tracing/perfetto\_task\_runner.cc:60:13  

#11 0x5635122f8094 in Invoke<(lambda at ../../base/tracing/perfetto\_task\_runner.cc:47:11), std::\_\_Cr::function<void ()> > ./../../base/functional/bind\_internal.h:621:12  

#12 0x5635122f8094 in MakeItSo<(lambda at ../../base/tracing/perfetto\_task\_runner.cc:47:11), std::\_\_Cr::tuple<std::\_\_Cr::function<void ()> > > ./../../base/functional/bind\_internal.h:925:12  

#13 0x5635122f8094 in RunImpl<(lambda at ../../base/tracing/perfetto\_task\_runner.cc:47:11), std::\_\_Cr::tuple<std::\_\_Cr::function<void ()> >, 0UL> ./../../base/functional/bind\_internal.h:1025:12  

#14 0x5635122f8094 in base::internal::Invoker<base::internal::BindState<base::tracing::PerfettoTaskRunner::PostDelayedTask(std::\_\_Cr::function<void ()>, unsigned int)::$\_0, std::\_\_Cr::function<void ()>>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:976:12  

#15 0x56351209fce7 in Run ./../../base/functional/callback.h:152:12  

#16 0x56351209fce7 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:186:34  

#17 0x5635121276bd in RunTask<(lambda at ../../base/task/thread\_pool/task\_tracker.cc:644:35)> ./../../base/task/common/task\_annotator.h:88:5  

#18 0x5635121276bd in RunTaskImpl ./../../base/task/thread\_pool/task\_tracker.cc:643:19  

#19 0x5635121276bd in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource\*, base::SequenceToken const&) ./../../base/task/thread\_pool/task\_tracker.cc:628:3  

#20 0x56351212678d in RunTaskWithShutdownBehavior ./../../base/task/thread\_pool/task\_tracker.cc:658:7  

#21 0x56351212678d in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource\*, base::TaskTraits const&) ./../../base/task/thread\_pool/task\_tracker.cc:485:5  

#22 0x563512125906 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) ./../../base/task/thread\_pool/task\_tracker.cc:400:5  

#23 0x56351215e4a8 in base::internal::WorkerThread::RunWorker() ./../../base/task/thread\_pool/worker\_thread.cc:480:34  

#24 0x56351215d751 in base::internal::WorkerThread::RunPooledWorker() ./../../base/task/thread\_pool/worker\_thread.cc:356:3  

#25 0x56351215d174 in base::internal::WorkerThread::ThreadMain() ./../../base/task/thread\_pool/worker\_thread.cc:336:7  

#26 0x5635121d836c in base::(anonymous namespace)::ThreadFunc(void\*) ./../../base/threading/platform\_thread\_posix.cc:101:13  

#27 0x5635001fbeda in asan\_thread\_start(void\*) *asan\_rtl*:31

Address 0x7ef3005c2100 is a wild pointer inside of access range of size 0x000000000008.  

SUMMARY: AddressSanitizer: use-after-poison (/home/pwn11/asan-linux-release/chrome+0x203a90b7) (BuildId: 893bcada95bb137a)  

Shadow bytes around the buggy address:  

0x7ef3005c1e80: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x7ef3005c1f00: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x7ef

**Additional Comments:**

\*\*Chrome version: \*\* 113.0.5624.0 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 161 B)
- [launcher.sh](attachments/launcher.sh) (text/plain, 1.4 KB)
- [test.js](attachments/test.js) (text/plain, 1011 B)
- [asan1-use-after-poison.log](attachments/asan1-use-after-poison.log) (text/plain, 10.5 KB)
- [asan2-unknown-crash.log](attachments/asan2-unknown-crash.log) (text/plain, 10.4 KB)
- [poc2.html](attachments/poc2.html) (text/plain, 219 B)

## Timeline

### [Deleted User] (2023-07-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-07-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5253995360354304.

### cl...@chromium.org (2023-07-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4973281423327232.

### cl...@chromium.org (2023-07-10)

[Empty comment from Monorail migration]

### pa...@chromium.org (2023-07-10)

I could not reproduce this unfortunately. However, the stack trace could be enough to spot an issue maybe? Setting sev-medium because this is a UaP, and impact none because this requires --trace-config-file.
@ddiproietto@google.com could you help triage this?

[Monorail components: Speed>Tracing]

### pa...@chromium.org (2023-07-10)

[Empty comment from Monorail migration]

### dd...@google.com (2023-07-10)

[Empty comment from Monorail migration]

### kh...@google.com (2023-07-11)

The stack trace points to this line [1] where observers are notified about the end of tracing. So we can guess that some observer was deleted without unregistering it from TraceLog. Unfortunately, I can't reproduce this issue locally, so can't tell which observer it was.

[1] https://source.chromium.org/chromium/chromium/src/+/main:base/trace_event/trace_log.cc;l=2244?q=OnTraceLogDisabled%20f:trace_log&ss=chromium%2Fchromium%2Fsrc

### kh...@google.com (2023-07-11)

I looked through all the classes that implement TraceLog::EnabledStateObserver and didn't find any obvious problems. So I'm pretty puzzled at the moment.

### em...@gmail.com (2023-07-11)

I'm sorry for not being able to provide a stable POC。I'm not sure why it couldn't repro on other machines. I have tried 3 machines here that can reproduce stably. Or can you try my new poc?

I insert a printf  in worker_inspector_controller.cc, and  found that the crash address was the same as the 'this' pointer of the WorkerInspectorController.
diff --git a/third_party/blink/renderer/core/inspector/worker_inspector_controller.cc b/third_party/blink/renderer/core/inspector/worker_inspector_controller.cc
index 0110ebf75d6fc..e757138283c87 100644
--- a/third_party/blink/renderer/core/inspector/worker_inspector_controller.cc
+++ b/third_party/blink/renderer/core/inspector/worker_inspector_controller.cc
@@ -107,6 +107,7 @@ WorkerInspectorController::WorkerInspectorController(

 WorkerInspectorController::~WorkerInspectorController() {
   DCHECK(!thread_);
+  printf("WorkerInspectorController::~WorkerInspectorController(),%p,%s\n", this, url_.GetString().Utf8().data());
   trace_event::RemoveEnabledStateObserver(this);
 }

log:
 ```
 ...
WorkerInspectorController::~WorkerInspectorController(),0x7e9f00342100,http://localhost:8000/crash2/poc.html
WorkerInspectorController::~WorkerInspectorController(),0x7ee100342100,http://localhost:8000/crash2/poc.html
WorkerInspectorController::~WorkerInspectorController(),0x7ef700342100,http://localhost:8000/crash2/poc.html
...
WorkerInspectorController::~WorkerInspectorController(),0x7ec900342100,http://localhost:8000/crash2/poc.html
WorkerInspectorController::~WorkerInspectorController(),0x7e9f00342100,http://localhost:8000/crash2/poc.html
WorkerInspectorController::~WorkerInspectorController(),0x7ee100342100,http://localhost:8000/crash2/poc.html
WorkerInspectorController::~WorkerInspectorController(),0x7ef700342100,http://localhost:8000/crash2/poc.html
...
WorkerInspectorController::~WorkerInspectorController(),0x7ec900342100,http://localhost:8000/crash2/poc.html
WorkerInspectorController::~WorkerInspectorController(),0x7e9f00342100,http://localhost:8000/crash2/poc.html
...
WorkerInspectorController::~WorkerInspectorController(),0x7ec900342100,http://localhost:8000/crash2/poc.html
WorkerInspectorController::~WorkerInspectorController(),0x7e9f00342100,http://localhost:8000/crash2/poc.html <<-
==3264827==ERROR: AddressSanitizer: unknown-crash on address 0x7e9f00342100 at pc 0x5561fdc2cbbb bp 0x7f41750f1d10 sp 0x7f41750f1d08
READ of size 8 at 0x7e9f00342100 thread T3 (ThreadPoolForeg)
```


### kh...@google.com (2023-07-11)

Still no luck reproducing.

From your last experiment though, it seems that there's some kind of data race between destruction of WorkerInspectorController and poisoning the memory that it occupies. Can you add another printf after 

trace_event::RemoveEnabledStateObserver(this);

and try to reproduce this again? Just to make sure that the crash happens while the destructor is still running.

### em...@gmail.com (2023-07-11)

[Comment Deleted]

### em...@gmail.com (2023-07-11)

Alternatively, you can try opening multiple tabs in one browser. I can reproduce it about 5,6 times locally.
For example,  open 10 browsers, if  didn't crash immediately, close all browsers and reopen again.
~/chromium/src/out/chrome_asan_shared/chrome  --no-sandbox --no-zygote --trace-config-file --disable-gpu --user-data-dir=/tmp/xx1 --incognito http://localhost:8000/crash2/poc.html   http://localhost:8000/crash2/poc.html   http://localhost:8000/crash2/poc.html http://localhost:8000/crash2/poc.html http://localhost:8000/crash2/poc.html http://localhost:8000/crash2/poc.html  http://localhost:8000/crash2/poc.html http://localhost:8000/crash2/poc.html http://localhost:8000/crash2/poc.html http://localhost:8000/crash2/poc.html http://localhost:8000/crash2/poc.html
This is the new log, please check it.If you have any problems, please feel free to contact me. Thank you!
...
[after]WorkerInspectorController::~WorkerInspectorController(),0x7ecd00482100,http://localhost:8000/crash2/poc.html
[before]WorkerInspectorController::~WorkerInspectorController(),0x7ea300482100,http://localhost:8000/crash2/poc.html
[after]WorkerInspectorController::~WorkerInspectorController(),0x7ea300482100,http://localhost:8000/crash2/poc.html
[before]WorkerInspectorController::~WorkerInspectorController(),0x7ee100482100,http://localhost:8000/crash2/poc.html
[after]WorkerInspectorController::~WorkerInspectorController(),0x7ee100482100,http://localhost:8000/crash2/poc.html
[before]WorkerInspectorController::~WorkerInspectorController(),0x7e8300482100,http://localhost:8000/crash2/poc.html  <<---
[after]WorkerInspectorController::~WorkerInspectorController(),0x7e8300482100,http://localhost:8000/crash2/poc.html   <<--
[before]WorkerInspectorController::~WorkerInspectorController(),0x7ed300482100,http://localhost:8000/crash2/poc.html
[after]WorkerInspectorController::~WorkerInspectorController(),0x7ed300482100,http://localhost:8000/crash2/poc.html
[before]WorkerInspectorController::~WorkerInspectorController(),0x7eb900482100,http://localhost:8000/crash2/poc.html
[after]WorkerInspectorController::~WorkerInspectorController(),0x7eb900482100,http://localhost:8000/crash2/poc.html
[before]WorkerInspectorController::~WorkerInspectorController(),0x7eff00482100,http://localhost:8000/crash2/poc.html
[after]WorkerInspectorController::~WorkerInspectorController(),0x7eff00482100,http://localhost:8000/crash2/poc.html
[before]WorkerInspectorController::~WorkerInspectorController(),0x7ee500482100,http://localhost:8000/crash2/poc.html
[after]WorkerInspectorController::~WorkerInspectorController(),0x7ee500482100,http://localhost:8000/crash2/poc.html
[before]WorkerInspectorController::~WorkerInspectorController(),0x7e9500482100,http://localhost:8000/crash2/poc.html
[after]WorkerInspectorController::~WorkerInspectorController(),0x7e9500482100,http://localhost:8000/crash2/poc.html
[before]WorkerInspectorController::~WorkerInspectorController(),0x7ed500482100,http://localhost:8000/crash2/poc.html
[after]WorkerInspectorController::~WorkerInspectorController(),0x7ed500482100,http://localhost:8000/crash2/poc.html
[before]WorkerInspectorController::~WorkerInspectorController(),0x7ec300482100,http://localhost:8000/crash2/poc.html
[after]WorkerInspectorController::~WorkerInspectorController(),0x7ec300482100,http://localhost:8000/crash2/poc.html
[before]WorkerInspectorController::~WorkerInspectorController(),0x7ecd00482100,http://localhost:8000/crash2/poc.html
[after]WorkerInspectorController::~WorkerInspectorController(),0x7ecd00482100,http://localhost:8000/crash2/poc.html
[before]WorkerInspectorController::~WorkerInspectorController(),0x7ea300482100,http://localhost:8000/crash2/poc.html
[after]WorkerInspectorController::~WorkerInspectorController(),0x7ea300482100,http://localhost:8000/crash2/poc.html
[before]WorkerInspectorController::~WorkerInspectorController(),0x7ee100482100,http://localhost:8000/crash2/poc.html
[after]WorkerInspectorController::~WorkerInspectorController(),0x7ee100482100,http://localhost:8000/crash2/poc.html <<--
=================================================================
[before]WorkerInspectorController::~WorkerInspectorController(),0x7e8300482100,http://localhost:8000/crash2/poc.html
==3778898==ERROR: AddressSanitizer: unknown-crash on address 0x7e8300482100 at pc 0x55857b3a4ba8 bp 0x7f52330f1d10 sp 0x7f52330f1d08
READ of size 8 at 0x7e8300482100 thread T3 (ThreadPoolForeg)

### em...@gmail.com (2023-07-11)

I'm sorry, the "<<--" label in the last message was placed incorrectly. It should be on the next line.

### kh...@google.com (2023-07-11)

Thanks for the log, this is perfect! From what I can tell, it confirms the hypothesis. While the destructor is waiting on the lock in RemoveEnabledStateObserver(), the memory has been freed already. Unfortunately, I know very little about garbage collection in Chrome, so can't triage this further.

@bikineev, can you please confirm if it's a possible situation that memory deallocation races against the destructor of WorkerInspectorController? And help triage this issue in general.

### cl...@chromium.org (2023-07-16)

This crash occurs very frequently on linux platform and is likely preventing the fuzzer None from making much progress. Fixing this will allow more bugs to be found.

Marking this bug as a blocker for next Beta release.

If this is incorrect, please add the ClusterFuzz-Wrong label and remove the ReleaseBlock-Beta label.

### [Deleted User] (2023-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-07-19)

[Empty comment from Monorail migration]

### dr...@chromium.org (2023-08-04)

[security shepherd]  bikineev@ appears to use a chromium email in most places, trying that instead and adding haraken@ as well for the question in #15.

### kh...@google.com (2023-08-07)

[Empty comment from Monorail migration]

### bi...@chromium.org (2023-08-07)

> Thanks for the log, this is perfect! From what I can tell, it confirms the hypothesis. While the destructor is waiting on the lock in RemoveEnabledStateObserver(), the memory has been freed already. Unfortunately, I know very little about garbage collection in Chrome, so can't triage this further.

Oilpan frees memory after running destructors, so it's unlikely the case. However, on the TSAN builds we poison all unreachable objects before destruction to make sure that a destructor doesn't touch another destructed object (since there is no ordering guarantees). I wonder if this could be the case here.

### is...@google.com (2023-08-07)

This issue was migrated from crbug.com/chromium/1463295?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1464779]
[Monorail components added to Component Tags custom field.]

### es...@google.com (2024-06-04)

> However, on the TSAN builds we poison all unreachable objects before destruction to make sure that a destructor doesn't touch another destructed object (since there is no ordering guarantees). I wonder if this could be the case here.

This would make sense. I assume there's a race here between the GC and destruction of the WorkerInspectorController and TraceLog::OnStop.

How is this poisoning acceptable in practice though? Doesn't this mean that the destructors of GarbageCollected objects can't touch any of the properties of the object?

Assuming we can't change this behavior, is there a way for a GC'd object to be informed when it is marked as unreachable and its memory is about to be poisoned? If so, we could use this signal to unregister the observer.

### ph...@chromium.org (2025-01-02)

[Secondary security shepherd] Hi bikineev@, could you provide some updates for this medium severity security bug please? Is there anything we can do to move this bug forward? [Will ping directly too per https://chromium.googlesource.com/chromium/src/+/main/docs/security/shepherd.md#Check-in-on-triaged-issues]

### bi...@chromium.org (2025-01-02)

> How is this poisoning acceptable in practice though? Doesn't this mean that the destructors of GarbageCollected objects can't touch any of the properties of the object?

A destructor of a GCed object cannot access *other* GCed objects, since by the time the destructor is called, other objects may already be destructed (Oilpan object destruction has no ordering guarantees). The destructor of an object is still allowed to access any local non-GCed data. You may refer to [1] for more documentation.

Having said that, I'm not sure if that's the case here. The dangling pointer is accessed from the `OnStop` handler, not from the Oilpan sweeper. It looks more like the dangling pointer refers to an object belonging to a different thread. Could it be allocated on one Oilpan thread and then be escaped into another thread? Note that Oilpan is not multithreaded and is not aware of references from the other threads (unless `CrossThreadPersistent` is used, see the doc).

[1] <https://chromium.googlesource.com/chromium/src/+/master/third_party/blink/renderer/platform/heap/BlinkGCAPIReference.md#garbagecollected>

### es...@google.com (2025-01-06)

I see, so IIUC:

- A ThreadPool thread is executing TraceLog::OnStop, which iterates all EnabledStateObservers.
- At the same time, a WorkerInspectorController is destroyed by Oilpan (presumably on the main thread), which is in the list of EnabledStateObservers that is concurrently being iterated by TraceLog::OnStop.
- The WorkerInspectorController tries to remove itself from TraceLog's list of EnabledStateObservers before its destructor has completed. The destructor's RemoveEnabledStateObserver will block until ThreadPool is finished with its iteration.
- However, it is already impossible to access the WorkerInspectorController's reference from the thread pool thread before the destructor (and RemoveEnabledStateObserver()) runs, as the WorkerInspectorController's memory is already poisoned.
- When the ThreadPool threads tries to call into the WorkerInspectorController, we see the poison crash.

Not quite sure: Maybe before the SDK migration, TraceLog::OnStop ran on the main thread and thus this wasn't an issue? But it definitely doesn't run there today.

I wonder if we should move WorkerInspectorController to become an AsyncEnabledStateObserver. Mika, wdyt?

### kh...@google.com (2025-01-08)

Making it AsyncEnabledStateObserver is not straightforward, since we can't have weak pointers to garbage-collected objects.

Maybe we can just remove the observer earlier, before the poisoning happens? Looking at existing methods, [WorkerInspectorController::Dispose](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/inspector/worker_inspector_controller.cc;l=168?q=WorkerInspectorController::Dispose&sq=&ss=chromium) seems like something that should happen when the object is no longer needed but before the poisoning.

I tentatively sent [crrev.com/c/6157377](https://crrev.com/c/6157377). @bikineev could you PTAL if this makes sense to you?

### bi...@chromium.org (2025-01-08)

> However, it is already impossible to access the WorkerInspectorController's reference from the thread pool thread before the destructor (and RemoveEnabledStateObserver()) runs, as the WorkerInspectorController's memory is already poisoned.

While WorkerInspectorController::~WorkerInspectorController() is executed (waiting on a lock as you mentioned a bullet above), the object's memory is unpoisoned (see [1]). Could it be that the destructor had already been executed and the memory was again poisoned [2] before the worker thread has called TraceLog::OnStop()?

[1] <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/heap/cppgc/heap-object-header.cc;l=32>
[2] <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/heap/cppgc/sweeper.cc;l=271>

### kh...@google.com (2025-01-08)

Does it mean that the object's memory is actually poisoned twice, like this:

1. Object is marked for garbage collection and its memory is poisoned
2. The memory is unpoisoned before running the destructor
3. Destructor runs
4. The memory is poisoned again

?

If so, then any EnabledStateObserver callbacks executed between 1 and 2 will cause an access to poisoned memory. We need to unregister the observer before 1 to fix this. Do you think [crrev.com/c/6157377](https://crrev.com/c/6157377) is the right way to do this?

### bi...@chromium.org (2025-01-08)

> If so, then any EnabledStateObserver callbacks executed between 1 and 2 will cause an access to poisoned memory. We need to unregister the observer before 1 to fix this. Do you think [crrev.com/c/6157377](https://crrev.com/c/6157377) is the right way to do this?

Is WorkerInspectorController::Dispose() called from the main thread? If not, then it's not safe, since any cross-thread reference to a GCed object is unsafe, since the GC is not aware of references from other threads. (unless CrossThread(Weak)Persistent is used).

You don't generally know when garbage collection (1) is triggered. So you cannot reliably unregister the observer from a different thread.

### kh...@google.com (2025-01-08)

> Is WorkerInspectorController::Dispose() called from the main thread?

Do you know anyone who can answer this question? It would be nice to get their opinion.

> You don't generally know when garbage collection (1) is triggered. So you cannot reliably unregister the observer from a different thread.

Unregistering the observer doesn't involve accessing the WorkerInspectorController object. It only modifies the TraceLog object, which is thread-safe. So it should be okay, or do I misunderstand something?

### bi...@chromium.org (2025-01-09)

> Unregistering the observer doesn't involve accessing the WorkerInspectorController object. It only modifies the TraceLog object, which is thread-safe. So it should be okay, or do I misunderstand something?

As long as the object is not accessed, it should be fine.

### kh...@google.com (2025-01-09)

Okay, so I'm submitting [crrev.com/c/6157377](https://crrev.com/c/6157377) as a speculative fix then.

### ap...@google.com (2025-01-09)

Project: chromium/src  

Branch: main  

Author: Mikhail Khokhlov <[khokhlov@google.com](mailto:khokhlov@google.com)>  

Link:      <https://chromium-review.googlesource.com/6157377>

Remove tracing observer in WorkerInspectorController::Dispose

---


Expand for full commit details
```
Remove tracing observer in WorkerInspectorController::Dispose 
 
To avoid races between calling EnabledStateObserver methods and memory 
poisoning, remove WorkerInspectorController from the list of observers 
ealier. 
 
Bug: 40067111 
Change-Id: I8bc7e15099b961adc8ee91302947f211330dd4b1 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6157377 
Reviewed-by: Alex Rudenko <alexrudenko@chromium.org> 
Commit-Queue: Mikhail Khokhlov <khokhlov@google.com> 
Cr-Commit-Position: refs/heads/main@{#1404068}

```

---

Files:

- M `third_party/blink/renderer/core/inspector/worker_inspector_controller.cc`

---

Hash: d181687ebf2a8d48c8e42a5d76d2a5b00c352929  

Date:  Thu Jan 09 02:33:55 2025


---

### kh...@google.com (2025-01-09)

[crrev.com/c/6157377](https://crrev.com/c/6157377) landed. If somebody can verify this fixes the issue, it would be great, because I can't reproduce it locally.

### em...@gmail.com (2025-01-10)

#37
I have conducted the following tests:

Testing on the Latest Version (Unpatched)
I tested the issue on the latest version, but was unable to reproduce the problem even without applying the patch. It is unclear whether other changes have affected the ability to reproduce the issue, especially considering the considerable amount of time that has passed.

Testing on the Older Version
Therefore, I applied the relevant patch to the older version (the version initially reported: Chromium 117.0.5878.0) and conducted testing. The results show that the issue did not reproduce after applying this CL.

If you need further information or have any other questions, please feel free to contact me.

### es...@google.com (2025-01-10)

Thanks [emilykim8708@gmail.com](mailto:emilykim8708@gmail.com)! We'll close this out as assumed-fixed then :)

### sp...@google.com (2025-01-17)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
reward for moderately mitigated memory corruption in a sandboxed process / renderer 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-01-17)

Thank you for your efforts and reporting this issue to us!

### ch...@google.com (2025-04-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> reward for moderately mitigated memory corruption in a sandboxed process / renderer

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067111)*
