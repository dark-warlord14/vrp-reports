# AddressSanitizer: heap-use-after-free components/history/core/browser/history_backend.cc:2542:22 in history::HistoryBackend::KillHistoryDatabase()

| Field | Value |
|-------|-------|
| **Issue ID** | [40059105](https://issues.chromium.org/issues/40059105) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>History |
| **Platforms** | Linux, Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | sk...@chromium.org |
| **Created** | 2022-03-15 |
| **Bounty** | $15,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4942.0 Safari/537.36

Steps to reproduce the problem:
The problem was found by my fuzzer running on CF(CC Security team for access permission https://clusterfuzz.com/testcase-detail/5136386931621888),
It appears frequently on CF, But it cannot be reproduced stably, CF may not automatically report.
By manual review, it is found that the window time triggered by the vulnerability is very short, so it cannot be reproduced stably.

What is the expected behavior?

What went wrong?
Type of crash
browser process(Sandbox escape)

#Analysis
1. When HistoryBackend::DatabaseErrorCallback get called,it will post a task(a) with this raw pointer without observing its lifecycle
2. When HistoryService::Cleanup get called, it will post a task(b) and associate the life cycle of history_backend_ to the task
3. If there are [b, a] in the task queue, the execution of b before a will cause the this(HistoryBackend) pointer in a to be released, resulting in UAF
```
//components/history/core/browser/history_backend.cc:2523
void HistoryBackend::DatabaseErrorCallback(int error, sql::Statement* stmt) {
  if (!scheduled_kill_db_ && sql::IsErrorCatastrophic(error)) {
    scheduled_kill_db_ = true;

    db_diagnostics_ = db_->GetDiagnosticInfo(error, stmt);

    // Don't just do the close/delete here, as we are being called by `db` and
    // that seems dangerous.
    // TODO(https://crbug.com/854258): It is also dangerous to kill the database
    // by a posted task: tasks that run before KillHistoryDatabase still can try
    // to use the broken database. Consider protecting against other tasks using
    // the DB or consider changing KillHistoryDatabase() to use RazeAndClose()
    // (then it can be cleared immediately).
    task_runner_->PostTask(
        FROM_HERE, base::BindOnce(&HistoryBackend::KillHistoryDatabase, this));		<<[1]
  }
}

//components/history/core/browser/history_service.cc:1081
void HistoryService::Cleanup() {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
...CUT...
  // Unload the backend.
  if (history_backend_) {
    // Get rid of the in-memory backend.
    in_memory_backend_.reset();

    ScheduleTask(PRIORITY_NORMAL, base::BindOnce(&HistoryBackend::Closing,
                                                 std::move(history_backend_)));		<<[2]
  }

  // Clear `backend_task_runner_` to make sure it's not used after Cleanup().
  backend_task_runner_ = nullptr;
}
```

#Patch
Not yet

#asan
=================================================================
==205644==ERROR: AddressSanitizer: heap-use-after-free on address 0x61700002f540 at pc 0x560428d8e6d7 bp 0x7fa6f02fe260 sp 0x7fa6f02fe258
WRITE of size 1 at 0x61700002f540 thread T7 (ThreadPoolForeg)
SCARINESS: 41 (1-byte-write-heap-use-after-free)
    #0 0x560428d8e6d6 in history::HistoryBackend::KillHistoryDatabase() components/history/core/browser/history_backend.cc:2542:22
    #1 0x560422353463 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/callback.h:142:12
    #2 0x5604223bec4a in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::SequenceToken const&) base/task/common/task_annotator.h:74:5
    #3 0x5604223bfc96 in base::internal::TaskTracker::RunBlockShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::SequenceToken const&) base/task/thread_pool/task_tracker.cc:700:3
    #4 0x5604223be399 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) base/task/thread_pool/task_tracker.cc:725:7
    #5 0x560422475ecc in base::internal::TaskTrackerPosix::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) base/task/thread_pool/task_tracker_posix.cc:22:16
    #6 0x5604223bd896 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) base/task/thread_pool/task_tracker.cc:467:5
    #7 0x5604223d5dea in base::internal::WorkerThread::RunWorker() base/task/thread_pool/worker_thread.cc:380:34
    #8 0x5604223d5361 in base::internal::WorkerThread::RunPooledWorker() base/task/thread_pool/worker_thread.cc:267:3
    #9 0x5604224772df in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:99:13
    #10 0x7fa7051616b9 in start_thread /build/glibc-LK5gWL/glibc-2.23/nptl/pthread_create.c:333

0x61700002f540 is located 64 bytes inside of 536-byte region [0x61700002f500,0x61700002f718)
freed by thread T7 (ThreadPoolForeg) here:
    #0 0x5604137184ad in operator delete(void*) third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x560428d693d1 in base::internal::BindState<void (history::HistoryBackend::*)(), scoped_refptr<history::HistoryBackend> >::Destroy(base::internal::BindStateBase const*) base/memory/ref_counted.h:418:5
    #2 0x56042235346b in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/callback.h:143:3
    #3 0x5604223bec4a in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::SequenceToken const&) base/task/common/task_annotator.h:74:5
    #4 0x5604223bfc96 in base::internal::TaskTracker::RunBlockShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::SequenceToken const&) base/task/thread_pool/task_tracker.cc:700:3
    #5 0x5604223be399 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) base/task/thread_pool/task_tracker.cc:725:7
    #6 0x560422475ecc in base::internal::TaskTrackerPosix::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) base/task/thread_pool/task_tracker_posix.cc:22:16
    #7 0x5604223bd896 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) base/task/thread_pool/task_tracker.cc:467:5
    #8 0x5604223d5dea in base::internal::WorkerThread::RunWorker() base/task/thread_pool/worker_thread.cc:380:34
    #9 0x5604223d5361 in base::internal::WorkerThread::RunPooledWorker() base/task/thread_pool/worker_thread.cc:267:3
    #10 0x5604224772df in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:99:13
    #11 0x7fa7051616b9 in start_thread /build/glibc-LK5gWL/glibc-2.23/nptl/pthread_create.c:333

previously allocated by thread T0 (chrome) here:
[205644:205701:0314/203614.023341:VERBOSE1:shutdown_signal_handlers_posix.cc(150)] Handling shutdown for signal 15.
    #0 0x560413717c4d in operator new(unsigned long) third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x560428d60c1e in history::HistoryService::Init(bool, history::HistoryDatabaseParams const&) base/memory/scoped_refptr.h:98:12
    #2 0x560421415360 in (anonymous namespace)::BuildHistoryService(content::BrowserContext*) components/history/core/browser/history_service.h:105:12
    #3 0x560426a5c73b in KeyedServiceFactory::GetServiceForContext(void*, bool) components/keyed_service/core/keyed_service_factory.cc:80:15
    #4 0x560421414ca5 in HistoryServiceFactory::GetForProfile(Profile*, ServiceAccessType) chrome/browser/history/history_service_factory.cc:49:22
    #5 0x5604214f7f0d in ukm::UkmBackgroundRecorderFactory::BuildServiceInstanceFor(content::BrowserContext*) const chrome/browser/metrics/ukm_background_recorder_service.cc:21:24
    #6 0x560426a5c73b in KeyedServiceFactory::GetServiceForContext(void*, bool) components/keyed_service/core/keyed_service_factory.cc:80:15
    #7 0x5604218261ac in ContentIndexProviderImpl::ContentIndexProviderImpl(Profile*) chrome/browser/content_index/content_index_provider_impl.cc:107:16
    #8 0x560421825f79 in ContentIndexProviderFactory::BuildServiceInstanceFor(content::BrowserContext*) const chrome/browser/content_index/content_index_provider_factory.cc:40:14
    #9 0x560426a5c73b in KeyedServiceFactory::GetServiceForContext(void*, bool) components/keyed_service/core/keyed_service_factory.cc:80:15
    #10 0x5604217f07e8 in ProfileImpl::GetContentIndexProvider() chrome/browser/profiles/profile_impl.cc:1328:10
    #11 0x560418c2bd8d in content::ContentIndexContextImpl::ContentIndexContextImpl(content::BrowserContext*, scoped_refptr<content::ServiceWorkerContextWrapper>) content/browser/content_index/content_index_context_impl.cc:19:34
    #12 0x560419c860e7 in content::StoragePartitionImpl::Initialize(content::StoragePartitionImpl*) base/memory/scoped_refptr.h:98:16
    #13 0x560419cb8ae8 in content::StoragePartitionImplMap::Get(content::StoragePartitionConfig const&, bool) content/browser/storage_partition_impl_map.cc:351:14
    #14 0x560418a61b9a in content::BrowserContext::GetDefaultStoragePartition() content/browser/browser_context.cc:137:52
    #15 0x5604215624dd in OptimizationGuideKeyedService::Initialize() chrome/browser/optimization_guide/optimization_guide_keyed_service.cc:177:35
    #16 0x560421562161 in OptimizationGuideKeyedServiceFactory::BuildServiceInstanceFor(content::BrowserContext*) const chrome/browser/optimization_guide/optimization_guide_keyed_service_factory.cc:59:14
    #17 0x560426a5c73b in KeyedServiceFactory::GetServiceForContext(void*, bool) components/keyed_service/core/keyed_service_factory.cc:80:15
    #18 0x560426a556e7 in DependencyManager::CreateContextServices(void*, bool) components/keyed_service/core/dependency_manager.cc
    #19 0x56042abce1f3 in BrowserContextDependencyManager::CreateBrowserContextServices(content::BrowserContext*) components/keyed_service/content/browser_context_dependency_manager.cc:46:22
    #20 0x5604217efd91 in ProfileImpl::OnLocaleReady(Profile::CreateMode) chrome/browser/profiles/profile_impl.cc:1107:51
    #21 0x5604217e8aac in ProfileImpl::OnPrefsLoaded(Profile::CreateMode, bool) chrome/browser/profiles/profile_impl.cc:1148:3
    #22 0x5604217e77a1 in ProfileImpl::ProfileImpl(base::FilePath const&, Profile::Delegate*, Profile::CreateMode, base::Time, scoped_refptr<base::SequencedTaskRunner>) chrome/browser/profiles/profile_impl.cc:531:5
    #23 0x5604217e4129 in Profile::CreateProfile(base::FilePath const&, Profile::Delegate*, Profile::CreateMode) chrome/browser/profiles/profile_impl.cc:368:59
    #24 0x560421835222 in ProfileManager::CreateAndInitializeProfile(base::FilePath const&) chrome/browser/profiles/profile_manager.cc:1871:38
    #25 0x560421831877 in ProfileManager::GetProfile(base::FilePath const&) chrome/browser/profiles/profile_manager.cc:778:10
    #26 0x56042d0f1455 in GetStartupProfile(base::FilePath const&, base::CommandLine const&) chrome/browser/ui/startup/startup_browser_creator.cc:1430:39
    #27 0x560421320d4d in (anonymous namespace)::CreateInitialProfile(content::MainFunctionParams const&, base::FilePath const&, base::CommandLine const&) chrome/browser/chrome_browser_main.cc:421:18
    #28 0x56042131dc90 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl() chrome/browser/chrome_browser_main.cc:1552:37
    #29 0x56042131d1e4 in ChromeBrowserMainParts::PreMainMessageLoopRun() chrome/browser/chrome_browser_main.cc:1139:18

Thread T7 (ThreadPoolForeg) created by T0 (chrome) here:
    #0 0x5604136cfc7c in pthread_create third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:208:3
    #1 0x5604224765ce in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, base::PlatformThreadHandle*, base::ThreadPriority) base/threading/platform_thread_posix.cc:142:13
    #2 0x5604223d466f in base::internal::WorkerThread::Start(base::WorkerThreadObserver*) base/task/thread_pool/worker_thread.cc:110:3
    #3 0x5604223cf985 in void base::internal::ThreadGroupImpl::ScopedCommandsExecutor::WorkerContainer::ForEachWorker<base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl()::'lambda0'(base::internal::WorkerThread*)>(base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl()::'lambda0'(base::internal::WorkerThread*)) base/task/thread_pool/thread_group_impl.cc:185:15
    #4 0x5604223cf4ef in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl() base/task/thread_pool/thread_group_impl.cc:184:23
    #5 0x5604223c6958 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::~ScopedCommandsExecutor() base/task/thread_pool/thread_group_impl.cc:103:31
    #6 0x5604223c7c44 in base::internal::ThreadGroupImpl::PushTaskSourceAndWakeUpWorkers(base::internal::TransactionWithRegisteredTaskSource) base/task/thread_pool/thread_group_impl.cc:460:1
    #7 0x5604223aafb0 in base::internal::ThreadPoolImpl::PostTaskWithSequenceNow(base::internal::Task, scoped_refptr<base::internal::Sequence>) base/task/thread_pool/thread_pool_impl.cc:422:38
    #8 0x5604223ab4bd in base::internal::ThreadPoolImpl::PostTaskWithSequence(base::internal::Task, scoped_refptr<base::internal::Sequence>) base/task/thread_pool/thread_pool_impl.cc:448:12
    #9 0x5604223d318c in base::internal::PooledSequencedTaskRunner::PostDelayedTask(base::Location const&, base::OnceCallback<void ()>, base::TimeDelta) base/task/thread_pool/pooled_sequenced_task_runner.cc:35:40
    #10 0x5604223a565c in base::TaskRunner::PostTask(base::Location const&, base::OnceCallback<void ()>) base/task/task_runner.cc:47:10
    #11 0x56042702df0d in power_scheduler::PowerModeArbiter::OnTaskRunnerAvailable(scoped_refptr<base::SequencedTaskRunner>, int) components/power_scheduler/power_mode_arbiter.cc:166:16
    #12 0x56042702dc8c in power_scheduler::PowerModeArbiter::OnThreadPoolAvailable() components/power_scheduler/power_mode_arbiter.cc:126:3
    #13 0x56042113c04b in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1143:55
    #14 0x56042113b877 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1042:12
    #15 0x560421135378 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:407:36
    #16 0x560421135a5c in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:435:10
    #17 0x56041371a496 in ChromeMain chrome/app/chrome_main.cc:176:12
    #18 0x7fa6fe6d582f in __libc_start_main /build/glibc-LK5gWL/glibc-2.23/csu/../csu/libc-start.c:291
SUMMARY: AddressSanitizer: heap-use-after-free components/history/core/browser/history_backend.cc:2542:22 in history::HistoryBackend::KillHistoryDatabase()

Shadow bytes around the buggy address:
  0x0c2e7fffde50: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2e7fffde60: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2e7fffde70: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x0c2e7fffde80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2e7fffde90: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x0c2e7fffdea0: fd fd fd fd fd fd fd fd[fd]fd fd fd fd fd fd fd
  0x0c2e7fffdeb0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2e7fffdec0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2e7fffded0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2e7fffdee0: fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2e7fffdef0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:00
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
==205644==ABORTING

Did this work before? N/A 

Chrome version: 101.0.4942.0  Channel: n/a
OS Version: 10.0

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 13.1 KB)

## Timeline

### [Deleted User] (2022-03-15)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-03-15)

CC security team to associates the problem with CF(https://clusterfuzz.com/testcase-detail/5136386931621888).
The problem reproduce frequently on CF, there may be some good test samples. 

Also please add  Restrict-View-SecurityEmbargo for this issue.

### cl...@chromium.org (2022-03-16)

Detailed Report: https://clusterfuzz.com/testcase?key=5136386931621888

Fuzzer: b0ring_webidl_fuzzer
Job Type: linux_lsan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free WRITE 1
Crash Address: 0x61700002f540
Crash State:
  history::HistoryBackend::KillHistoryDatabase
  base::internal::TaskTracker::RunTaskImpl
  base::internal::TaskTracker::RunBlockShutdown
  
Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Crash Revision: https://clusterfuzz.com/revisions?job=linux_lsan_chrome_mp&revision=980650

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5136386931621888

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2022-03-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-03-16)

This crash occurs very frequently on linux platform and is likely preventing the fuzzer b0ring_webidl_fuzzer from making much progress. Fixing this will allow more bugs to be found.

Marking this bug as a blocker for next Beta release.

If this is incorrect, please add the ClusterFuzz-Wrong label and remove the ReleaseBlock-Beta label.

### cl...@chromium.org (2022-03-16)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>TaskScheduling Internals>ThreadPool]

### cl...@chromium.org (2022-03-16)

ClusterFuzz testcase 5136386931621888 appears to be flaky, updating reproducibility label.

### dc...@chromium.org (2022-03-18)

Just to be clear:

>1. When HistoryBackend::DatabaseErrorCallback get called,it will post a task(a) with this raw pointer without observing its lifecycle

`this` is a raw pointer, but it should *not* be bound as a raw pointer. base::BindOnce() has a feature that the receiver object of a non-static method must either be a ref-countable type (in which case refcounting is *supposed* to automatically be used), a WeakPtr, or a raw pointer explicitly annotated with base::Unretained().

It would be interesting to inspect base::BindOnce's internal state to see what template instantiation path it's going through, but I don't know of an easy way to do that... the UaF would pretty clearly seem to indicate that logic is not working though.



[Monorail components: -Internals>TaskScheduling -Internals>ThreadPool UI>Browser>History]

### ma...@chromium.org (2022-03-18)

Adding Restrict-View-SecurityEmbargo per https://crbug.com/chromium/1306507#c2.

### sk...@chromium.org (2022-03-18)

Agree with dcheng the post task should not be using a raw pointer, but using refcounted. HistoryBackend extends RefCountedThreadSafe too, as HistoryBackend is created on the main thread, then used on a task sequence.

### dc...@chromium.org (2022-03-18)

My current thinking is this is high severity but not critical despite being a browser process UaF, since I *think* this is a crash at profile shutdown.

It would still be good to understand what's going on here though--why is this apparently refcounted object not being refcounted?

1. I looked if there were other BindOnce calls using base::Unretained() with KillHistoryDatabase(), and I couldn't find any.
2. We can see that BindOnce() does appear to be capturing by scoped_refptr, at least here:
#1 0x560428d693d1 in base::internal::BindState<void (history::HistoryBackend::*)(), scoped_refptr<history::HistoryBackend> >::Destroy(base::internal::BindStateBase const*) base/memory/ref_counted.h:418:5
The BindState specialization is a HistoryBackend method pointer and a scoped_refptr for the HistoryBackend receiver itself.
3. And I believe it's not a cross-thread race, because the free stack and the use-after-free stack are on the same sequence.

### sk...@chromium.org (2022-03-18)

I would also say that in order to trigger this, you would have to get the history db to generate an error.

I have a theory on this. Will upload a patch shortly.

### sk...@chromium.org (2022-03-19)

https://chromium-review.googlesource.com/c/chromium/src/+/3538001 dcheng, will add you once bots are green.

### [Deleted User] (2022-03-19)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### m....@gmail.com (2022-03-21)

Thank you for correcting my initial analysis.
I found that there is indeed a race condition issue here causing the UAF.

1. DatabaseErrorCallback[1,2] called by db on thread a uses base::Unretained(this) with out inc refcount
2. HistoryBackend[3] free it self on thead b
3. HistoryBackend is RefCountedThreadSafe, but it only safe for refcount it self not for this[4]
4. When the destructor is called on thread b and executed to [4], and thread a is executed to [2],
even if the reference count is incremented at [2], the object cannot be prevented from being destroyed,
resulting in UAF even the free stack and the use-after-free stack are on the same sequence.
```
components/history/core/browser/history_backend.cc:868
void HistoryBackend::InitImpl(
    const HistoryDatabaseParams& history_database_params) {
  DCHECK(!db_) << "Initializing HistoryBackend twice";
...CUT...
  // Unretained to avoid a ref loop with db_.
  db_->set_error_callback(base::BindRepeating(
      &HistoryBackend::DatabaseErrorCallback, base::Unretained(this)));			<<[1]
      
components/history/core/browser/history_backend.cc:2523
void HistoryBackend::DatabaseErrorCallback(int error, sql::Statement* stmt) {
  if (!scheduled_kill_db_ && sql::IsErrorCatastrophic(error)) {
    scheduled_kill_db_ = true;
...CUT...
    task_runner_->PostTask(
        FROM_HERE, base::BindOnce(&HistoryBackend::KillHistoryDatabase, this));	<<[2]
  }
}

//components/history/core/browser/history_service.cc:1081
void HistoryService::Cleanup() {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
...CUT...
  // Unload the backend.
  if (history_backend_) {
    // Get rid of the in-memory backend.
    in_memory_backend_.reset();

    ScheduleTask(PRIORITY_NORMAL, base::BindOnce(&HistoryBackend::Closing,
                                                 std::move(history_backend_)));		<<[3]
  }

  // Clear `backend_task_runner_` to make sure it's not used after Cleanup().
  backend_task_runner_ = nullptr;
}

base/memory/ref_counted.h:404
void Release() const {
if (subtle::RefCountedThreadSafeBase::Release()) {
  ANALYZER_SKIP_THIS_PATH();
  Traits::Destruct(static_cast<const T*>(this));									<<[4]
}
}
```

### sk...@chromium.org (2022-03-21)

> 1. DatabaseErrorCallback[1,2] called by db on thread a uses base::Unretained(this) with out inc refcount

2 does increment the refcount, but you are right that 1 does not.

> 2. HistoryBackend[3] free it self on thead b
> 3. HistoryBackend is RefCountedThreadSafe, but it only safe for refcount it self not for this[4]
> 4. When the destructor is called on thread b and executed to [4], and thread a is executed to [2],
> even if the reference count is incremented at [2], the object cannot be prevented from being destroyed,
> resulting in UAF even the free stack and the use-after-free stack are on the same sequence.

The sequence that leads to this is:
~HistoryBackend
  CloseAllDatabases();
    this does a db operation that triggers an error
    HistoryBackend::DatabaseErrorCallback
    post task, that increments ref count, but it doesn't matter because already in destructor
<post task runs>
HistoryBackend::KillHistoryDatabase
use-after-free because historybackend was deleted.

This could happen anytime a profile is being shutdown.

### gi...@appspot.gserviceaccount.com (2022-03-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/72315bbaa74a0ffe110b33adfebb5252f283b8ce

commit 72315bbaa74a0ffe110b33adfebb5252f283b8ce
Author: Scott Violet <sky@chromium.org>
Date: Mon Mar 21 20:57:58 2022

history: don't handle db error during destruction

Handling of db errors is delayed using a posttask. ~HistoryBackend
closes all the dbs. If closing the db results in an error, then
a PostTask() is scheduled with a HistoryBackend that is part way
through deletion. When the PostTask() runs, we get a uaf.

This patch resets the error callback in ~HistoryBackend to ensure
this doesn't happen. This means a db error is effectively ignored
during shutdown. Presumably if the error is fatal, it'll be handled
when the HistoryBackend is created again.

BUG=1306507
TEST=none

Change-Id: Ic158589a43e7bc2fd1f602fb2798ab500dc8d6d7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3538001
Reviewed-by: Victor Costan <pwnall@chromium.org>
Commit-Queue: Victor Costan <pwnall@chromium.org>
Commit-Queue: Scott Violet <sky@chromium.org>
Cr-Commit-Position: refs/heads/main@{#983478}

[modify] https://crrev.com/72315bbaa74a0ffe110b33adfebb5252f283b8ce/components/history/core/browser/history_backend.cc
[modify] https://crrev.com/72315bbaa74a0ffe110b33adfebb5252f283b8ce/components/history/core/browser/history_database.h


### sk...@chromium.org (2022-03-21)

[Empty comment from Monorail migration]

### ad...@google.com (2022-03-21)

sky@ thanks for the fix. Could you confirm that this isn't a recent regression? (i.e. this has existed since M98 or earlier)? Just so we can label up the bug fully to keep the bots happy.

### [Deleted User] (2022-03-21)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sk...@chromium.org (2022-03-22)

+pwnall . The code this impacts in history has been around for a very long time. What I'm unsure of is if the sql side of this may have changed to trigger error callbacks in more scenarios. I suspect not, but Victor will know that for sure.

### sk...@chromium.org (2022-03-22)

[Empty comment from Monorail migration]

### ad...@google.com (2022-03-22)

Thanks, based on https://crbug.com/chromium/1306507#c21 assuming this impacts extended stable onwards, but Victor please let me know if that's not correct.

Adding merge requests that Sheriffbot would normally add under these circumstances.

### [Deleted User] (2022-03-22)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-22)

[Empty comment from Monorail migration]

### ad...@google.com (2022-03-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-22)

Merge approved: your change passed merge requirements and is auto-approved for M101. Please go ahead and merge the CL to branch 4951 (refs/branch-heads/4951) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: benmason (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-22)

Merge review required: M100 has already been cut for stable release.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-22)

Merge review required: M99 is already shipping to stable.

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
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-22)

Merge review required: M98 is already shipping to stable.

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

### [Deleted User] (2022-03-23)

[Empty comment from Monorail migration]

### pb...@google.com (2022-03-28)

[Bulk Edit] Your change has been approved for M101 branch,please go ahead and merge the CL's to M101 branch manually asap(Refer to go/chrome-branches for branch info) so that they would be part of this week's first M101 Dev/Beta release.

### sk...@chromium.org (2022-03-28)

The following holds for all merge requests:

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?

Merge requested because of potential security issue.

2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/chromium/src/+/3538001

3. Have the changes been released and tested on canary?

Yes.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No.



### [Deleted User] (2022-03-28)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-03-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f568cb24548668be8f89353e4aabbf03795bc00e

commit f568cb24548668be8f89353e4aabbf03795bc00e
Author: Scott Violet <sky@chromium.org>
Date: Mon Mar 28 18:28:29 2022

[M101 merge] history: don't handle db error during destruction

Handling of db errors is delayed using a posttask. ~HistoryBackend
closes all the dbs. If closing the db results in an error, then
a PostTask() is scheduled with a HistoryBackend that is part way
through deletion. When the PostTask() runs, we get a uaf.

This patch resets the error callback in ~HistoryBackend to ensure
this doesn't happen. This means a db error is effectively ignored
during shutdown. Presumably if the error is fatal, it'll be handled
when the HistoryBackend is created again.

BUG=1306507
TEST=none

(cherry picked from commit 72315bbaa74a0ffe110b33adfebb5252f283b8ce)

Change-Id: Ic158589a43e7bc2fd1f602fb2798ab500dc8d6d7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3538001
Reviewed-by: Victor Costan <pwnall@chromium.org>
Commit-Queue: Victor Costan <pwnall@chromium.org>
Commit-Queue: Scott Violet <sky@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#983478}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3554357
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4951@{#192}
Cr-Branched-From: 27de6227ca357da0d57ae2c7b18da170c4651438-refs/heads/main@{#982481}

[modify] https://crrev.com/f568cb24548668be8f89353e4aabbf03795bc00e/components/history/core/browser/history_backend.cc
[modify] https://crrev.com/f568cb24548668be8f89353e4aabbf03795bc00e/components/history/core/browser/history_database.h


### am...@chromium.org (2022-03-31)

M100 merge approved, please merge this fix to branch 4896 at your earliest convenience so this fix can be included in the next M100 security respin 

merge-na 98/99 as M100 is not Stable channel 

### am...@google.com (2022-03-31)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-31)

Congratulations on another one! The VRP Panel has decided to award you $15,000 for this report + $1,000 patch bonus as you were able to get this issue discovered via clusterfuzz. Thanks for all your efforts in the reporting and analysis of this one! 

(removing RV-SE as discussed off-bug, please feel free to reach out directly if you need this re-added) 

### gi...@appspot.gserviceaccount.com (2022-03-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/724972b1812f86215f1559cd560df4e71ce8f190

commit 724972b1812f86215f1559cd560df4e71ce8f190
Author: Scott Violet <sky@chromium.org>
Date: Thu Mar 31 22:24:40 2022

[M100 merge] history: don't handle db error during destruction

Handling of db errors is delayed using a posttask. ~HistoryBackend
closes all the dbs. If closing the db results in an error, then
a PostTask() is scheduled with a HistoryBackend that is part way
through deletion. When the PostTask() runs, we get a uaf.

This patch resets the error callback in ~HistoryBackend to ensure
this doesn't happen. This means a db error is effectively ignored
during shutdown. Presumably if the error is fatal, it'll be handled
when the HistoryBackend is created again.

BUG=1306507
TEST=none

(cherry picked from commit 72315bbaa74a0ffe110b33adfebb5252f283b8ce)

Change-Id: Ic158589a43e7bc2fd1f602fb2798ab500dc8d6d7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3538001
Reviewed-by: Victor Costan <pwnall@chromium.org>
Commit-Queue: Victor Costan <pwnall@chromium.org>
Commit-Queue: Scott Violet <sky@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#983478}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3564503
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4896@{#996}
Cr-Branched-From: 1f63ff4bc27570761b35ffbc7f938f6586f7bee8-refs/heads/main@{#972766}

[modify] https://crrev.com/724972b1812f86215f1559cd560df4e71ce8f190/components/history/core/browser/history_backend.cc
[modify] https://crrev.com/724972b1812f86215f1559cd560df4e71ce8f190/components/history/core/browser/history_database.h


### am...@google.com (2022-04-01)

[Empty comment from Monorail migration]

### ad...@google.com (2022-04-11)

It looks like we already shipped this fix in M100 - it made it into the branch just in time for the 100.0.4896.75 release. amyressler@ labelling this for a retrospective CVE allocation and release notes update.

### sk...@chromium.org (2022-05-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2022-11-04)

[Empty comment from Monorail migration]

### pg...@google.com (2023-01-02)

release notes updated here: https://chromereleases.googleblog.com/2022/04/stable-channel-update-for-desktop.html

### pg...@google.com (2023-01-02)

[Empty comment from Monorail migration]

### is...@google.com (2023-01-02)

This issue was migrated from crbug.com/chromium/1306507?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1323569]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059105)*
