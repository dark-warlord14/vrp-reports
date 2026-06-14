# use-after-poison on address  thread T0

| Field | Value |
|-------|-------|
| **Issue ID** | [475893566](https://issues.chromium.org/issues/475893566) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Speed>Tracing |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | mu...@gmail.com |
| **Assignee** | et...@chromium.org |
| **Created** | 2026-01-14 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description

attempting free on address which was not malloc

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

- Case 1:

```
ASAN_OPTIONS=external_symbolizer_path=$(which llvm-symbolizer) ./tools/get_asan_chrome/chromium-145.0.7620.2-linux-asan/chrome   --enable-features=SharedArrayBuffer   --no-sandbox  --enable-tracing  --enable-logging=stderr --v=1   http://localhost:9090/testing.html

```
```
=================================================================
==280781==ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed: 0x7b4350010140 in thread T9 (ThreadPoolForeg)
    #0 0x55e2d0ec40b6 in free (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-145.0.7620.2-linux-asan/chrome+0x1095f0b6) (BuildId: a374629589b9fed1)
    #1 0x55e2d6a387be in deallocate v8/src/common/code-memory-access.h:240:39
    #2 0x55e2d6a387be in deallocate gen/third_party/libc++/src/include/__memory/allocator_traits.h:289:9
    #3 0x55e2d6a387be in erase gen/third_party/libc++/src/include/__tree:2058:3
    #4 0x55e2d6a387be in std::__Cr::__tree<std::__Cr::__value_type<unsigned long, v8::internal::ThreadIsolation::JitAllocation>, std::__Cr::__map_value_compare<unsigned long, std::__Cr::pair<unsigned long const, v8::internal::ThreadIsolation::JitAllocation>, std::__Cr::less<unsigned long>>, v8::internal::ThreadIsolation::StlAllocator<std::__Cr::pair<unsigned long const, v8::internal::ThreadIsolation::JitAllocation>>>::erase(std::__Cr::__tree_const_iterator<std::__Cr::__value_type<unsigned long, v8::internal::ThreadIsolation::JitAllocation>, std::__Cr::__tree_node<std::__Cr::__value_type<unsigned long, v8::internal::ThreadIsolation::JitAllocation>, void*>*, long>, std::__Cr::__tree_const_iterator<std::__Cr::__value_type<unsigned long, v8::internal::ThreadIsolation::JitAllocation>, std::__Cr::__tree_node<std::__Cr::__value_type<unsigned long, v8::internal::ThreadIsolation::JitAllocation>, void*>*, long>) gen/third_party/libc++/src/include/__tree:2066:11
    #5 0x55e2d7138e39 in FreeRange v8/src/common/code-memory-access-inl.h:294:13
    #6 0x55e2d7138e39 in FreeInternal<true> v8/src/heap/paged-spaces-inl.h:95:45
    #7 0x55e2d7138e39 in FreeDuringSweep v8/src/heap/paged-spaces-inl.h:124:10
    #8 0x55e2d7138e39 in FreeAndProcessFreedMemory v8/src/heap/sweeper.cc:1003:59
    #9 0x55e2d7138e39 in v8::internal::Sweeper::RawSweep(v8::internal::PageMetadata*, v8::internal::FreeSpaceTreatmentMode, v8::internal::Sweeper::SweepingMode, bool) v8/src/heap/sweeper.cc:1219:7
    #10 0x55e2d7166606 in ParallelSweepPage v8/src/heap/sweeper.cc:432:15
    #11 0x55e2d7166606 in v8::internal::Sweeper::ConcurrentMajorSweeper::ConcurrentSweepSpace(v8::internal::AllocationSpace, v8::JobDelegate*) v8/src/heap/sweeper.cc:83:22
    #12 0x55e2d7165cd7 in v8::internal::Sweeper::MajorSweeperJob::RunImpl(v8::JobDelegate*, bool) v8/src/heap/sweeper.cc:198:31
    #13 0x55e2ef640c6f in operator() gin/v8_platform.cc:306:23
    #14 0x55e2ef640c6f in Invoke<const (lambda at ../../gin/v8_platform.cc:303:11) &, const std::__Cr::unique_ptr<v8::JobTask, std::__Cr::default_delete<v8::JobTask> > &, base::JobDelegate *> base/functional/bind_internal.h:648:12
    #15 0x55e2ef640c6f in MakeItSo<const (lambda at ../../gin/v8_platform.cc:303:11) &, const std::__Cr::tuple<std::__Cr::unique_ptr<v8::JobTask, std::__Cr::default_delete<v8::JobTask> > > &, base::JobDelegate *> base/functional/bind_internal.h:922:12
    #16 0x55e2ef640c6f in RunImpl<const (lambda at ../../gin/v8_platform.cc:303:11) &, const std::__Cr::tuple<std::__Cr::unique_ptr<v8::JobTask, std::__Cr::default_delete<v8::JobTask> > > &, 0UL> base/functional/bind_internal.h:1059:14
    #17 0x55e2ef640c6f in base::internal::Invoker<base::internal::FunctorTraits<gin::V8Platform::CreateJobImpl(v8::TaskPriority, std::__Cr::unique_ptr<v8::JobTask, std::__Cr::default_delete<v8::JobTask>>, v8::SourceLocation const&)::$_0 const&, std::__Cr::unique_ptr<v8::JobTask, std::__Cr::default_delete<v8::JobTask>> const&>, base::internal::BindState<false, false, false, gin::V8Platform::CreateJobImpl(v8::TaskPriority, std::__Cr::unique_ptr<v8::JobTask, std::__Cr::default_delete<v8::JobTask>>, v8::SourceLocation const&)::$_0, std::__Cr::unique_ptr<v8::JobTask, std::__Cr::default_delete<v8::JobTask>>>, void (base::JobDelegate*)>::Run(base::internal::BindStateBase*, base::JobDelegate*) base/functional/bind_internal.h:979:12
    #18 0x55e2e8094b1f in base::RepeatingCallback<void (base::JobDelegate*)>::Run(base::JobDelegate*) const & base/functional/callback.h:343:12
    #19 0x55e2e80963c9 in operator() base/task/thread_pool/job_task_source.cc:111:32
    #20 0x55e2e80963c9 in Invoke<const (lambda at ../../base/task/thread_pool/job_task_source.cc:107:11) &, base::internal::JobTaskSource *> base/functional/bind_internal.h:648:12
    #21 0x55e2e80963c9 in MakeItSo<const (lambda at ../../base/task/thread_pool/job_task_source.cc:107:11) &, const std::__Cr::tuple<base::internal::UnretainedWrapper<base::internal::JobTaskSource, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &> base/functional/bind_internal.h:922:12
    #22 0x55e2e80963c9 in RunImpl<const (lambda at ../../base/task/thread_pool/job_task_source.cc:107:11) &, const std::__Cr::tuple<base::internal::UnretainedWrapper<base::internal::JobTaskSource, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, 0UL> base/functional/bind_internal.h:1059:14
    #23 0x55e2e80963c9 in base::internal::Invoker<base::internal::FunctorTraits<base::internal::JobTaskSource::JobTaskSource(base::Location const&, base::TaskTraits const&, base::RepeatingCallback<void (base::JobDelegate*)>, base::RepeatingCallback<unsigned long (unsigned long)>, base::internal::PooledTaskRunnerDelegate*)::$_0 const&, base::internal::JobTaskSource*>, base::internal::BindState<false, false, false, base::internal::JobTaskSource::JobTaskSource(base::Location const&, base::TaskTraits const&, base::RepeatingCallback<void (base::JobDelegate*)>, base::RepeatingCallback<unsigned long (unsigned long)>, base::internal::PooledTaskRunnerDelegate*)::$_0, base::internal::UnretainedWrapper<base::internal::JobTaskSource, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::Run(base::internal::BindStateBase*) base/functional/bind_internal.h:979:12
    #24 0x55e2e8000416 in Run base/functional/callback.h:155:12
    #25 0x55e2e8000416 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:229:34
    #26 0x55e2e809e402 in RunTask<(lambda at ../../base/task/thread_pool/task_tracker.cc:688:35)> base/task/common/task_annotator.h:112:5
    #27 0x55e2e809e402 in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:687:19
    #28 0x55e2e809e64c in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:672:3
    #29 0x55e2e809cc8a in RunTaskWithShutdownBehavior base/task/thread_pool/task_tracker.cc:702:7
    #30 0x55e2e809cc8a in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) base/task/thread_pool/task_tracker.cc:502:5
    #31 0x55e2e809bf59 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) base/task/thread_pool/task_tracker.cc:392:5
    #32 0x55e2e80de8a3 in base::internal::WorkerThread::RunWorker() base/task/thread_pool/worker_thread.cc:473:36
    #33 0x55e2e80dd9e4 in base::internal::WorkerThread::RunPooledWorker() base/task/thread_pool/worker_thread.cc:359:3
    #34 0x55e2e80dd44b in base::internal::WorkerThread::ThreadMain() base/task/thread_pool/worker_thread.cc:339:7
    #35 0x55e2e81629a3 in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #36 0x55e2d0ec1c46 in asan_thread_start(void*) asan_interceptors.cpp

Address 0x7b4350010140 is a wild pointer inside of access range of size 0x000000000001.
SUMMARY: AddressSanitizer: bad-free (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-145.0.7620.2-linux-asan/chrome+0x1095f0b6) (BuildId: a374629589b9fed1) in free
Thread T9 (ThreadPoolForeg) created by T6 (ThreadPoolForeg) here:
    #0 0x55e2d0ea7a01 in pthread_create (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-145.0.7620.2-linux-asan/chrome+0x10942a01) (BuildId: a374629589b9fed1)
    #1 0x55e2e8161ff2 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) base/threading/platform_thread_posix.cc:153:13
    #2 0x55e2e80dc194 in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*) base/task/thread_pool/worker_thread.cc:185:3
    #3 0x55e2e80a0817 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush() base/task/thread_pool/thread_group.cc:90:13
    #4 0x55e2e80a0510 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor() base/task/thread_pool/thread_group.cc:81:3
    #5 0x55e2e80d1a41 in ~ScopedCommandsExecutor base/task/thread_pool/thread_group_impl.cc:43:3
    #6 0x55e2e80d1a41 in base::internal::ThreadGroupImpl::WorkerDelegate::GetWork(base::internal::WorkerThread*) base/task/thread_pool/thread_group_impl.cc:465:1
    #7 0x55e2e80de6c8 in base::internal::WorkerThread::RunWorker() base/task/thread_pool/worker_thread.cc:460:52
    #8 0x55e2e80dd9e4 in base::internal::WorkerThread::RunPooledWorker() base/task/thread_pool/worker_thread.cc:359:3
    #9 0x55e2e80dd44b in base::internal::WorkerThread::ThreadMain() base/task/thread_pool/worker_thread.cc:339:7
    #10 0x55e2e81629a3 in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #11 0x55e2d0ec1c46 in asan_thread_start(void*) asan_interceptors.cpp

Thread T6 (ThreadPoolForeg) created by T4 (ThreadPoolForeg) here:
    #0 0x55e2d0ea7a01 in pthread_create (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-145.0.7620.2-linux-asan/chrome+0x10942a01) (BuildId: a374629589b9fed1)
    #1 0x55e2e8161ff2 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) base/threading/platform_thread_posix.cc:153:13
    #2 0x55e2e80dc194 in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*) base/task/thread_pool/worker_thread.cc:185:3
    #3 0x55e2e80a0817 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush() base/task/thread_pool/thread_group.cc:90:13
    #4 0x55e2e80a0510 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor() base/task/thread_pool/thread_group.cc:81:3
    #5 0x55e2e80d1a41 in ~ScopedCommandsExecutor base/task/thread_pool/thread_group_impl.cc:43:3
    #6 0x55e2e80d1a41 in base::internal::ThreadGroupImpl::WorkerDelegate::GetWork(base::internal::WorkerThread*) base/task/thread_pool/thread_group_impl.cc:465:1
    #7 0x55e2e80de6c8 in base::internal::WorkerThread::RunWorker() base/task/thread_pool/worker_thread.cc:460:52
    #8 0x55e2e80dd9e4 in base::internal::WorkerThread::RunPooledWorker() base/task/thread_pool/worker_thread.cc:359:3
    #9 0x55e2e80dd44b in base::internal::WorkerThread::ThreadMain() base/task/thread_pool/worker_thread.cc:339:7
    #10 0x55e2e81629a3 in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #11 0x55e2d0ec1c46 in asan_thread_start(void*) asan_interceptors.cpp

Thread T4 (ThreadPoolForeg) created by T0 (chrome) here:
    #0 0x55e2d0ea7a01 in pthread_create (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-145.0.7620.2-linux-asan/chrome+0x10942a01) (BuildId: a374629589b9fed1)
    #1 0x55e2e8161ff2 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) base/threading/platform_thread_posix.cc:153:13
    #2 0x55e2e80dc194 in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*) base/task/thread_pool/worker_thread.cc:185:3
    #3 0x55e2e80a0817 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush() base/task/thread_pool/thread_group.cc:90:13
    #4 0x55e2e80a0510 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor() base/task/thread_pool/thread_group.cc:81:3
    #5 0x55e2e80cf673 in ~ScopedCommandsExecutor base/task/thread_pool/thread_group_impl.cc:43:3
    #6 0x55e2e80cf673 in base::internal::ThreadGroupImpl::Start(unsigned long, unsigned long, base::TimeDelta, scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*, base::internal::ThreadGroup::WorkerEnvironment, bool, std::__Cr::optional<base::TimeDelta>) base/task/thread_pool/thread_group_impl.cc:252:3
    #7 0x55e2e80ad19b in base::internal::ThreadPoolImpl::Start(base::ThreadPoolInstance::InitParams const&, base::WorkerThreadObserver*) base/task/thread_pool/thread_pool_impl.cc:198:35
    #8 0x55e2f3eb7759 in content::ChildProcess::ChildProcess(base::ThreadType, std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>, bool) content/child/child_process.cc:113:20
    #9 0x55e2f403ab00 in content::RenderProcess::RenderProcess(std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>) content/renderer/render_process.cc:18:7
    #10 0x55e2f403a3c8 in content::RenderProcessImpl::RenderProcessImpl() content/renderer/render_process_impl.cc:98:7
    #11 0x55e2f403a8e0 in content::RenderProcessImpl::Create() content/renderer/render_process_impl.cc:216:31
    #12 0x55e2f40d64e7 in content::RendererMain(content::MainFunctionParams) content/renderer/renderer_main.cc:281:53
    #13 0x55e2e3d2be6c in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:673:14
    #14 0x55e2e3d2cfa6 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:780:12
    #15 0x55e2e3d2fa2e in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1137:10
    #16 0x55e2e3d299a1 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:358:36
    #17 0x55e2e3d29f9c in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:371:10
    #18 0x55e2d0eff149 in ChromeMain chrome/app/chrome_main.cc:191:12
    #19 0x7f476ea34ca7 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16


==280781==ADDITIONAL INFO

==280781==Note: Please include this section with the ASan report.
Task trace:
    #0 0x55e2ef62a51f in gin::V8ToBaseLocation(v8::SourceLocation const&) gin/converter.cc:289:10
    #1 0x55e2ef62a51f in gin::V8ToBaseLocation(v8::SourceLocation const&) gin/converter.cc:289:10
    #2 0x55e2ef62a51f in gin::V8ToBaseLocation(v8::SourceLocation const&) gin/converter.cc:289:10
    #3 0x55e2e7db8928 in PostDispatchNextMessageFromPipe mojo/public/cpp/bindings/lib/connector.cc:589:7


Command line: `/proc/self/exe --type=renderer --crashpad-handler-pid=280709 --enable-crash-reporter=, --change-stack-guard-on-fork=enable --no-sandbox --file-url-path-alias=/gen=/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-145.0.7620.2-linux-asan/gen --ozone-platform=wayland --lang=en-US --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1768413058870414 --launch-time-ticks=11680168631 --shared-files=v8_context_snapshot_data:100 --metrics-shmem-handle=4,i,15616693684411908740,6467688484948836529,2097152 --field-trial-handle=3,i,16887591402123923352,888776599351663266,262144 --enable-features=SharedArrayBuffer --disable-features=EyeDropper --variations-seed-version --trace-config-handle=5,i,14747122687651454898,3073227884130036937,128 --trace-buffer-handle=6,i,13702298388982980450,4616719318018359172,4194304 --trace-process-track-uuid=3190708990997080739 --enable-logging=stderr --v=1`


==280781==END OF ADDITIONAL INFO

==280781==ABORTING

```

- Case 2:

```
ASAN_OPTIONS=external_symbolizer_path=$(which llvm-symbolizer) ./tools/get_asan_chrome/chromium-145.0.7620.2-linux-asan/chrome   --enable-features=SharedArrayBuffer   --no-sandbox  --enable-logging=stderr --v=1   http://localhost:9090/testing.html

```
```
=================================================================
==281335==ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed: 0x7b6b20010140 in thread T12 (ThreadPoolForeg)
    #0 0x564eeb2940b6 in free (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-145.0.7620.2-linux-asan/chrome+0x1095f0b6) (BuildId: a374629589b9fed1)
    #1 0x564ef0e087be in deallocate v8/src/common/code-memory-access.h:240:39
    #2 0x564ef0e087be in deallocate gen/third_party/libc++/src/include/__memory/allocator_traits.h:289:9
    #3 0x564ef0e087be in erase gen/third_party/libc++/src/include/__tree:2058:3
    #4 0x564ef0e087be in std::__Cr::__tree<std::__Cr::__value_type<unsigned long, v8::internal::ThreadIsolation::JitAllocation>, std::__Cr::__map_value_compare<unsigned long, std::__Cr::pair<unsigned long const, v8::internal::ThreadIsolation::JitAllocation>, std::__Cr::less<unsigned long>>, v8::internal::ThreadIsolation::StlAllocator<std::__Cr::pair<unsigned long const, v8::internal::ThreadIsolation::JitAllocation>>>::erase(std::__Cr::__tree_const_iterator<std::__Cr::__value_type<unsigned long, v8::internal::ThreadIsolation::JitAllocation>, std::__Cr::__tree_node<std::__Cr::__value_type<unsigned long, v8::internal::ThreadIsolation::JitAllocation>, void*>*, long>, std::__Cr::__tree_const_iterator<std::__Cr::__value_type<unsigned long, v8::internal::ThreadIsolation::JitAllocation>, std::__Cr::__tree_node<std::__Cr::__value_type<unsigned long, v8::internal::ThreadIsolation::JitAllocation>, void*>*, long>) gen/third_party/libc++/src/include/__tree:2066:11
    #5 0x564ef1508e39 in FreeRange v8/src/common/code-memory-access-inl.h:294:13
    #6 0x564ef1508e39 in FreeInternal<true> v8/src/heap/paged-spaces-inl.h:95:45
    #7 0x564ef1508e39 in FreeDuringSweep v8/src/heap/paged-spaces-inl.h:124:10
    #8 0x564ef1508e39 in FreeAndProcessFreedMemory v8/src/heap/sweeper.cc:1003:59
    #9 0x564ef1508e39 in v8::internal::Sweeper::RawSweep(v8::internal::PageMetadata*, v8::internal::FreeSpaceTreatmentMode, v8::internal::Sweeper::SweepingMode, bool) v8/src/heap/sweeper.cc:1219:7
    #10 0x564ef1536606 in ParallelSweepPage v8/src/heap/sweeper.cc:432:15
    #11 0x564ef1536606 in v8::internal::Sweeper::ConcurrentMajorSweeper::ConcurrentSweepSpace(v8::internal::AllocationSpace, v8::JobDelegate*) v8/src/heap/sweeper.cc:83:22
    #12 0x564ef1535cd7 in v8::internal::Sweeper::MajorSweeperJob::RunImpl(v8::JobDelegate*, bool) v8/src/heap/sweeper.cc:198:31
    #13 0x564f09a10c6f in operator() gin/v8_platform.cc:306:23
    #14 0x564f09a10c6f in Invoke<const (lambda at ../../gin/v8_platform.cc:303:11) &, const std::__Cr::unique_ptr<v8::JobTask, std::__Cr::default_delete<v8::JobTask> > &, base::JobDelegate *> base/functional/bind_internal.h:648:12
    #15 0x564f09a10c6f in MakeItSo<const (lambda at ../../gin/v8_platform.cc:303:11) &, const std::__Cr::tuple<std::__Cr::unique_ptr<v8::JobTask, std::__Cr::default_delete<v8::JobTask> > > &, base::JobDelegate *> base/functional/bind_internal.h:922:12
    #16 0x564f09a10c6f in RunImpl<const (lambda at ../../gin/v8_platform.cc:303:11) &, const std::__Cr::tuple<std::__Cr::unique_ptr<v8::JobTask, std::__Cr::default_delete<v8::JobTask> > > &, 0UL> base/functional/bind_internal.h:1059:14
    #17 0x564f09a10c6f in base::internal::Invoker<base::internal::FunctorTraits<gin::V8Platform::CreateJobImpl(v8::TaskPriority, std::__Cr::unique_ptr<v8::JobTask, std::__Cr::default_delete<v8::JobTask>>, v8::SourceLocation const&)::$_0 const&, std::__Cr::unique_ptr<v8::JobTask, std::__Cr::default_delete<v8::JobTask>> const&>, base::internal::BindState<false, false, false, gin::V8Platform::CreateJobImpl(v8::TaskPriority, std::__Cr::unique_ptr<v8::JobTask, std::__Cr::default_delete<v8::JobTask>>, v8::SourceLocation const&)::$_0, std::__Cr::unique_ptr<v8::JobTask, std::__Cr::default_delete<v8::JobTask>>>, void (base::JobDelegate*)>::Run(base::internal::BindStateBase*, base::JobDelegate*) base/functional/bind_internal.h:979:12
    #18 0x564f02464b1f in base::RepeatingCallback<void (base::JobDelegate*)>::Run(base::JobDelegate*) const & base/functional/callback.h:343:12
    #19 0x564f024663c9 in operator() base/task/thread_pool/job_task_source.cc:111:32
    #20 0x564f024663c9 in Invoke<const (lambda at ../../base/task/thread_pool/job_task_source.cc:107:11) &, base::internal::JobTaskSource *> base/functional/bind_internal.h:648:12
    #21 0x564f024663c9 in MakeItSo<const (lambda at ../../base/task/thread_pool/job_task_source.cc:107:11) &, const std::__Cr::tuple<base::internal::UnretainedWrapper<base::internal::JobTaskSource, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &> base/functional/bind_internal.h:922:12
    #22 0x564f024663c9 in RunImpl<const (lambda at ../../base/task/thread_pool/job_task_source.cc:107:11) &, const std::__Cr::tuple<base::internal::UnretainedWrapper<base::internal::JobTaskSource, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, 0UL> base/functional/bind_internal.h:1059:14
    #23 0x564f024663c9 in base::internal::Invoker<base::internal::FunctorTraits<base::internal::JobTaskSource::JobTaskSource(base::Location const&, base::TaskTraits const&, base::RepeatingCallback<void (base::JobDelegate*)>, base::RepeatingCallback<unsigned long (unsigned long)>, base::internal::PooledTaskRunnerDelegate*)::$_0 const&, base::internal::JobTaskSource*>, base::internal::BindState<false, false, false, base::internal::JobTaskSource::JobTaskSource(base::Location const&, base::TaskTraits const&, base::RepeatingCallback<void (base::JobDelegate*)>, base::RepeatingCallback<unsigned long (unsigned long)>, base::internal::PooledTaskRunnerDelegate*)::$_0, base::internal::UnretainedWrapper<base::internal::JobTaskSource, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::Run(base::internal::BindStateBase*) base/functional/bind_internal.h:979:12
    #24 0x564f023d0416 in Run base/functional/callback.h:155:12
    #25 0x564f023d0416 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:229:34
    #26 0x564f0246e402 in RunTask<(lambda at ../../base/task/thread_pool/task_tracker.cc:688:35)> base/task/common/task_annotator.h:112:5
    #27 0x564f0246e402 in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:687:19
    #28 0x564f0246e64c in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:672:3
    #29 0x564f0246cc8a in RunTaskWithShutdownBehavior base/task/thread_pool/task_tracker.cc:702:7
    #30 0x564f0246cc8a in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) base/task/thread_pool/task_tracker.cc:502:5
    #31 0x564f0246bf59 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) base/task/thread_pool/task_tracker.cc:392:5
    #32 0x564f024ae8a3 in base::internal::WorkerThread::RunWorker() base/task/thread_pool/worker_thread.cc:473:36
    #33 0x564f024ad9e4 in base::internal::WorkerThread::RunPooledWorker() base/task/thread_pool/worker_thread.cc:359:3
    #34 0x564f024ad44b in base::internal::WorkerThread::ThreadMain() base/task/thread_pool/worker_thread.cc:339:7
    #35 0x564f025329a3 in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #36 0x564eeb291c46 in asan_thread_start(void*) asan_interceptors.cpp

Address 0x7b6b20010140 is a wild pointer inside of access range of size 0x000000000001.
SUMMARY: AddressSanitizer: bad-free (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-145.0.7620.2-linux-asan/chrome+0x1095f0b6) (BuildId: a374629589b9fed1) in free
Thread T12 (ThreadPoolForeg) created by T6 (ThreadPoolForeg) here:
    #0 0x564eeb277a01 in pthread_create (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-145.0.7620.2-linux-asan/chrome+0x10942a01) (BuildId: a374629589b9fed1)
    #1 0x564f02531ff2 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) base/threading/platform_thread_posix.cc:153:13
    #2 0x564f024ac194 in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*) base/task/thread_pool/worker_thread.cc:185:3
    #3 0x564f02470817 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush() base/task/thread_pool/thread_group.cc:90:13
    #4 0x564f02470510 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor() base/task/thread_pool/thread_group.cc:81:3
    #5 0x564f024a1a41 in ~ScopedCommandsExecutor base/task/thread_pool/thread_group_impl.cc:43:3
    #6 0x564f024a1a41 in base::internal::ThreadGroupImpl::WorkerDelegate::GetWork(base::internal::WorkerThread*) base/task/thread_pool/thread_group_impl.cc:465:1
    #7 0x564f024ae6c8 in base::internal::WorkerThread::RunWorker() base/task/thread_pool/worker_thread.cc:460:52
    #8 0x564f024ad9e4 in base::internal::WorkerThread::RunPooledWorker() base/task/thread_pool/worker_thread.cc:359:3
    #9 0x564f024ad44b in base::internal::WorkerThread::ThreadMain() base/task/thread_pool/worker_thread.cc:339:7
    #10 0x564f025329a3 in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #11 0x564eeb291c46 in asan_thread_start(void*) asan_interceptors.cpp

Thread T6 (ThreadPoolForeg) created by T4 (ThreadPoolForeg) here:
    #0 0x564eeb277a01 in pthread_create (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-145.0.7620.2-linux-asan/chrome+0x10942a01) (BuildId: a374629589b9fed1)
    #1 0x564f02531ff2 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) base/threading/platform_thread_posix.cc:153:13
    #2 0x564f024ac194 in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*) base/task/thread_pool/worker_thread.cc:185:3
    #3 0x564f02470817 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush() base/task/thread_pool/thread_group.cc:90:13
    #4 0x564f02470510 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor() base/task/thread_pool/thread_group.cc:81:3
    #5 0x564f024a1a41 in ~ScopedCommandsExecutor base/task/thread_pool/thread_group_impl.cc:43:3
    #6 0x564f024a1a41 in base::internal::ThreadGroupImpl::WorkerDelegate::GetWork(base::internal::WorkerThread*) base/task/thread_pool/thread_group_impl.cc:465:1
    #7 0x564f024ae6c8 in base::internal::WorkerThread::RunWorker() base/task/thread_pool/worker_thread.cc:460:52
    #8 0x564f024ad9e4 in base::internal::WorkerThread::RunPooledWorker() base/task/thread_pool/worker_thread.cc:359:3
    #9 0x564f024ad44b in base::internal::WorkerThread::ThreadMain() base/task/thread_pool/worker_thread.cc:339:7
    #10 0x564f025329a3 in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #11 0x564eeb291c46 in asan_thread_start(void*) asan_interceptors.cpp

Thread T4 (ThreadPoolForeg) created by T0 (chrome) here:
    #0 0x564eeb277a01 in pthread_create (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-145.0.7620.2-linux-asan/chrome+0x10942a01) (BuildId: a374629589b9fed1)
    #1 0x564f02531ff2 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) base/threading/platform_thread_posix.cc:153:13
    #2 0x564f024ac194 in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*) base/task/thread_pool/worker_thread.cc:185:3
    #3 0x564f02470817 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush() base/task/thread_pool/thread_group.cc:90:13
    #4 0x564f02470510 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor() base/task/thread_pool/thread_group.cc:81:3
    #5 0x564f0249f673 in ~ScopedCommandsExecutor base/task/thread_pool/thread_group_impl.cc:43:3
    #6 0x564f0249f673 in base::internal::ThreadGroupImpl::Start(unsigned long, unsigned long, base::TimeDelta, scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*, base::internal::ThreadGroup::WorkerEnvironment, bool, std::__Cr::optional<base::TimeDelta>) base/task/thread_pool/thread_group_impl.cc:252:3
    #7 0x564f0247d19b in base::internal::ThreadPoolImpl::Start(base::ThreadPoolInstance::InitParams const&, base::WorkerThreadObserver*) base/task/thread_pool/thread_pool_impl.cc:198:35
    #8 0x564f0e287759 in content::ChildProcess::ChildProcess(base::ThreadType, std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>, bool) content/child/child_process.cc:113:20
    #9 0x564f0e40ab00 in content::RenderProcess::RenderProcess(std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>) content/renderer/render_process.cc:18:7
    #10 0x564f0e40a3c8 in content::RenderProcessImpl::RenderProcessImpl() content/renderer/render_process_impl.cc:98:7
    #11 0x564f0e40a8e0 in content::RenderProcessImpl::Create() content/renderer/render_process_impl.cc:216:31
    #12 0x564f0e4a64e7 in content::RendererMain(content::MainFunctionParams) content/renderer/renderer_main.cc:281:53
    #13 0x564efe0fbe6c in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:673:14
    #14 0x564efe0fcfa6 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:780:12
    #15 0x564efe0ffa2e in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1137:10
    #16 0x564efe0f99a1 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:358:36
    #17 0x564efe0f9f9c in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:371:10
    #18 0x564eeb2cf149 in ChromeMain chrome/app/chrome_main.cc:191:12
    #19 0x7f6f37c34ca7 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16


==281335==ADDITIONAL INFO

==281335==Note: Please include this section with the ASan report.
Task trace:
    #0 0x564f099fa51f in gin::V8ToBaseLocation(v8::SourceLocation const&) gin/converter.cc:289:10
    #1 0x564f099fa51f in gin::V8ToBaseLocation(v8::SourceLocation const&) gin/converter.cc:289:10
    #2 0x564f099fa51f in gin::V8ToBaseLocation(v8::SourceLocation const&) gin/converter.cc:289:10
    #3 0x564f02f987f3 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) mojo/public/cpp/system/simple_watcher.cc:103:13


Command line: `/proc/self/exe --type=renderer --crashpad-handler-pid=281261 --enable-crash-reporter=, --change-stack-guard-on-fork=enable --no-sandbox --file-url-path-alias=/gen=/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-145.0.7620.2-linux-asan/gen --ozone-platform=wayland --lang=en-US --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1768413058870414 --launch-time-ticks=11933584748 --shared-files=v8_context_snapshot_data:100 --metrics-shmem-handle=4,i,6873764498450833188,15208632084318771308,2097152 --field-trial-handle=3,i,6211455694761719018,8609949838832315594,262144 --enable-features=SharedArrayBuffer --disable-features=EyeDropper --variations-seed-version --trace-process-track-uuid=3190708990997080739 --enable-logging=stderr --v=1`


==281335==END OF ADDITIONAL INFO

==281335==ABORTING


```
#### Impact analysis

free

---

### The cause

#### What version of Chrome have you found the security issue in?

145.0.7620.0 (Developer Build) (64-bit)

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

## Attachments

- [testing.html](attachments/testing.html) (text/html, 4.4 KB)

## Timeline

### wf...@chromium.org (2026-01-14)

I get a different crash which is

```
==17520==ERROR: AddressSanitizer: use-after-poison on address 0x7e9400524298 at pc 0x7ffc7ca92a3d bp 0x00ac323fed30 sp 0x00ac323fed78
READ of size 8 at 0x7e9400524298 thread T0
    #0 0x7ffc7ca92a3c in [thunk]: xml_ffi::XmlCallbacks::`vcall'{32, {flat}} (c:\src\asan\chromium-146.0.7633.0-win64-asan\chrome.dll+0x1838e2a3c)
    #1 0x7ffc8d05b481 in base::internal::DecayedFunctorTraits<void (*)(void (perfetto::TrackEventSessionObserver::*)(const perfetto::DataSourceBase::SetupArgs &), const perfetto::DataSourceBase::SetupArgs &, perfetto::TrackEventSessionObserver *),void (perfetto::TrackEventSessionObserver::*const &)(const perfetto::DataSourceBase::SetupArgs &),const perfetto::DataSourceBase::SetupArgs &>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:663
    #2 0x7ffc8d05b481 in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (*const &)(void (perfetto::TrackEventSessionObserver::*)(const perfetto::DataSourceBase::SetupArgs &), const perfetto::DataSourceBase::SetupArgs &, perfetto::TrackEventSessionObserver *),void (perfetto::TrackEventSessionObserver::*const &)(const perfetto::DataSourceBase::SetupArgs &),const perfetto::DataSourceBase::SetupArgs &>,void,0,1>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:922
    #3 0x7ffc8d05b481 in base::internal::Invoker<base::internal::FunctorTraits<void (*const &)(void (perfetto::TrackEventSessionObserver::*)(const perfetto::DataSourceBase::SetupArgs &), const perfetto::DataSourceBase::SetupArgs &, perfetto::TrackEventSessionObserver *),void (perfetto::TrackEventSessionObserver::*const &)(const perfetto::DataSourceBase::SetupArgs &),const perfetto::DataSourceBase::SetupArgs &>,base::internal::BindState<0,1,0,void (*)(void (perfetto::TrackEventSessionObserver::*)(const perfetto::DataSourceBase::SetupArgs &), const perfetto::DataSourceBase::SetupArgs &, perfetto::TrackEventSessionObserver *),void (perfetto::TrackEventSessionObserver::*)(const perfetto::DataSourceBase::SetupArgs &),perfetto::DataSourceBase::SetupArgs>,void (perfetto::TrackEventSessionObserver *)>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1059
    #4 0x7ffc8d05b481 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl *const &)(void (__cdecl perfetto::TrackEventSessionObserver::*)(class perfetto::DataSourceBase::StartArgs const &), class perfetto::DataSourceBase::StartArgs const &, class perfetto::TrackEventSessionObserver *), void (__cdecl perfetto::TrackEventSessionObserver::*const &)(class perfetto::DataSourceBase::StartArgs const &), class perfetto::DataSourceBase::StartArgs const &>, struct base::internal::BindState<0, 1, 0, void (__cdecl *)(void (__cdecl perfetto::TrackEventSessionObserver::*)(class perfetto::DataSourceBase::StartArgs const &), class perfetto::DataSourceBase::StartArgs const &, class perfetto::TrackEventSessionObserver *), void (__cdecl perfetto::TrackEventSessionObserver::*)(class perfetto::DataSourceBase::StartArgs const &), class perfetto::DataSourceBase::StartArgs>, (class perfetto::TrackEventSessionObserver *)>::Run(class base::internal::BindStateBase *, class perfetto::TrackEventSessionObserver *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:979:12
    #5 0x7ffc8d059602 in base::RepeatingCallback<void (perfetto::TrackEventSessionObserver *)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:343
    #6 0x7ffc8d059602 in base::ObserverListThreadSafe<class perfetto::TrackEventSessionObserver, 1>::NotifyWrapper(class base::raw_ptr<class perfetto::TrackEventSessionObserver, 1>, struct base::ObserverListThreadSafe<class perfetto::TrackEventSessionObserver, 1>::NotificationData const &) C:\b\s\w\ir\cache\builder\src\base\observer_list_threadsafe.h:295:25
    #7 0x7ffc8d05a5ae in base::internal::DecayedFunctorTraits<void (base::ObserverListThreadSafe<perfetto::TrackEventSessionObserver,1>::*)(base::raw_ptr<perfetto::TrackEventSessionObserver,1>, const base::ObserverListThreadSafe<perfetto::TrackEventSessionObserver,1>::NotificationData &),base::ObserverListThreadSafe<perfetto::TrackEventSessionObserver,1> *&&,base::raw_ptr<perfetto::TrackEventSessionObserver,1>,base::ObserverListThreadSafe<perfetto::TrackEventSessionObserver,1>::NotificationData &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:730
    #8 0x7ffc8d05a5ae in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (base::ObserverListThreadSafe<perfetto::TrackEventSessionObserver,1>::*&&)(base::raw_ptr<perfetto::TrackEventSessionObserver,1>, const base::ObserverListThreadSafe<perfetto::TrackEventSessionObserver,1>::NotificationData &),base::ObserverListThreadSafe<perfetto::TrackEventSessionObserver,1> *&&,base::raw_ptr<perfetto::TrackEventSessionObserver,1>,base::ObserverListThreadSafe<perfetto::TrackEventSessionObserver,1>::NotificationData &&>,void,0,1,2>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:922
    #9 0x7ffc8d05a5ae in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl base::ObserverListThreadSafe<class perfetto::TrackEventSessionObserver, 1>::*&&)(class base::raw_ptr<class perfetto::TrackEventSessionObserver, 1>, struct base::ObserverListThreadSafe<class perfetto::TrackEventSessionObserver, 1>::NotificationData const &), class base::ObserverListThreadSafe<class perfetto::TrackEventSessionObserver, 1> *&&, class base::raw_ptr<class perfetto::TrackEventSessionObserver, 1>, struct base::ObserverListThreadSafe<class perfetto::TrackEventSessionObserver, 1>::NotificationData &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl base::ObserverListThreadSafe<class perfetto::TrackEventSessionObserver, 1>::*)(class base::raw_ptr<class perfetto::TrackEventSessionObserver, 1>, struct base::ObserverListThreadSafe<class perfetto::TrackEventSessionObserver, 1>::NotificationData const &), class scoped_refptr<class base::ObserverListThreadSafe<class perfetto::TrackEventSessionObserver, 1>>, class base::internal::UnretainedWrapper<class perfetto::TrackEventSessionObserver, struct base::unretained_traits::MayDangle, 0>, struct base::ObserverListThreadSafe<class perfetto::TrackEventSessionObserver, 1>::NotificationData>, (void)>::RunImpl<void (__cdecl base::ObserverListThreadSafe<class perfetto::TrackEventSessionObserver, 1>::*)(class base::raw_ptr<class perfetto::TrackEventSessionObserver, 1>, struct base::ObserverListThreadSafe<class perfetto::TrackEventSessionObserver, 1>::NotificationData const &), class std::__Cr::tuple<class scoped_refptr<class base::ObserverListThreadSafe<class perfetto::TrackEventSessionObserver, 1>>, class base::internal::UnretainedWrapper<class perfetto::TrackEventSessionObserver, struct base::unretained_traits::MayDangle, 0>, struct base::ObserverListThreadSafe<class perfetto::TrackEventSessionObserver, 1>::NotificationData>, 0, 1, 2>(void (__cdecl base::ObserverListThreadSafe<class perfetto::TrackEventSessionObserver, 1>::*&&)(class base::raw_ptr<class perfetto::TrackEventSessionObserver, 1>, struct base::ObserverListThreadSafe<class perfetto::TrackEventSessionObserver, 1>::NotificationData const &), class std::__Cr::tuple<class scoped_refptr<class base::ObserverListThreadSafe<class perfetto::TrackEventSessionObserver, 1>>, class base::internal::UnretainedWrapper<class perfetto::TrackEventSessionObserver, struct base::unretained_traits::MayDangle, 0>, struct base::ObserverListThreadSafe<class perfetto::TrackEventSessionObserver, 1>::NotificationData> &&, struct std::__Cr::integer_sequence<unsigned __int64, 0, 1, 2>) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1059:14
    #10 0x7ffc8d1713e8 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:155
    #11 0x7ffc8d1713e8 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:229:34
    #12 0x7ffc8d141966 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:112
    #13 0x7ffc8d141966 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:472:23
    #14 0x7ffc8d1407f3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:346:40
    #15 0x7ffc8d2a98ee in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:42:55
    #16 0x7ffc8d14366f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:647:12
    #17 0x7ffc8d1e75bc in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:135:14
    #18 0x7ffc9757b30d in content::RendererMain(struct content::MainFunctionParams) C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:360:16
    #19 0x7ffc88e8912d in content::RunOtherNamedProcessTypeMain(class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>> const &, struct content::MainFunctionParams, class content::ContentMainDelegate *) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:771:14
    #20 0x7ffc88e8b5e8 in content::ContentMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1137:10
    #21 0x7ffc88e7f69f in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:358:36
    #22 0x7ffc88e7fe42 in content::ContentMain(struct content::ContentMainParams) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:371:10
    #23 0x7ffc791b2b06 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:191:12
    #24 0x7ff62e404807 in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:201:12
    #25 0x7ff62e402074 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:351:20
    #26 0x7ff62e8e7f5f in invoke_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #27 0x7ff62e8e7f5f in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #28 0x7ffd6244e8d6  (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #29 0x7ffd646ec53b  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18008c53b)

```

could this bug be the same as [issue 475613896](https://issues.chromium.org/issues/475613896) ?

### sa...@gmail.com (2026-01-15)

After analyzing the issue on Windows, it appears to be the same root cause as in [475613896](https://issues.chromium.org/issues/475613896). However, the impact differs between Linux and Windows. Would it make sense to consolidate this report into [475613896](https://issues.chromium.org/issues/475613896)?

### pe...@google.com (2026-01-15)

Thank you for providing more feedback. Adding the requester to the CC list.

### ch...@google.com (2026-01-15)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### sa...@gmail.com (2026-01-15)

I am reproducing this issue on Debian GNU/Linux 13 (amd64), kernel 6.12.63 (x86\_64).

```
Linux localhost 6.12.63+deb13-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.63-1 (2025-12-30) x86_64 GNU/Linux

```

### ch...@google.com (2026-05-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/475893566)*
