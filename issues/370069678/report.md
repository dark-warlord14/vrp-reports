# Heap-use-after-free in · content::CacheStorageScheduler::CompleteOperationAndRunNext

| Field | Value |
|-------|-------|
| **Issue ID** | [370069678](https://issues.chromium.org/issues/370069678) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>CacheStorage |
| **Platforms** | Android, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | es...@chromium.org |
| **Created** | 2024-09-28 |
| **Bounty** | $6,000.00 |

## Description

# VULNERABILITY DETAILS

Please provide a brief explanation of the security issue.

# BISECT

<https://chromium-review.googlesource.com/c/chromium/src/+/5871445>

# REPRODUCTION CASE

found by myfuzzer run on cf

<https://clusterfuzz.com/testcase-detail/4855330047459328>

> I will provide a more stable PoC ASAP.

# Type of crash:

[browser]

# RCA

As the comment says that next\_operation is likely to be freed on the next iteration.

and accessing pending\_operations\_ will cause a UAF.

```
void CacheStorageScheduler::DispatchOperationTask(base::OnceClosure task) {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
  std::move(task).Run();
}

void CacheStorageScheduler::MaybeRunOperation() {
...
  while (!pending_operations_.empty()) {
    base::WeakPtr<CacheStorageOperation> next_operation =
        pending_operations_.front()->AsWeakPtr();

...CUT...

    DispatchOperationTask(
        base::BindOnce(&CacheStorageOperation::Run, next_operation));
    // `next_operation` may be null at this point.
  }

```

1. <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/cache_storage/cache_storage_scheduler.cc;l=145-187;drc=f522344e45882da4c7f7cb1b3a0a7bd747d654bb?q=content%2Fbrowser%2Fcache_storage%2Fcache_storage_scheduler.cc&ss=chromium%2Fchromium%2Fsrc>

# ASAN

```
=================================================================
==382468==ERROR: AddressSanitizer: heap-use-after-free on address 0x7522a1cfdba0 at pc 0x5b4d119a6fec bp 0x747298cf1030 sp 0x747298cf1028
READ of size 8 at 0x7522a1cfdba0 thread T5 (ThreadPoolForeg)
SCARINESS: 51 (8-byte-read-heap-use-after-free)
    #0 0x5b4d119a6feb in empty third_party/libc++/src/include/vector:640:18
    #1 0x5b4d119a6feb in content::CacheStorageScheduler::MaybeRunOperation() content/browser/cache_storage/cache_storage_scheduler.cc:145:31
    #2 0x5b4d119a7456 in content::CacheStorageScheduler::CompleteOperationAndRunNext(long) content/browser/cache_storage/cache_storage_scheduler.cc:116:3
    #3 0x5b4d11948548 in void content::CacheStorageScheduler::RunNextContinuation<>(long, base::OnceCallback<void ()>) content/browser/cache_storage/cache_storage_scheduler.h:102:7
    #4 0x5b4d1194891d in Invoke<void (content::CacheStorageScheduler::*)(long, base::OnceCallback<void ()>), const base::WeakPtr<content::CacheStorageScheduler> &, long, base::OnceCallback<void ()> > base/functional/bind_internal.h:738:12
    #5 0x5b4d1194891d in MakeItSo<void (content::CacheStorageScheduler::*)(long, base::OnceCallback<void ()>), std::__Cr::tuple<base::WeakPtr<content::CacheStorageScheduler>, long, base::OnceCallback<void ()> > > base/functional/bind_internal.h:954:5
    #6 0x5b4d1194891d in void base::internal::Invoker<base::internal::FunctorTraits<void (content::CacheStorageScheduler::*&&)(long, base::OnceCallback<void ()>), base::WeakPtr<content::CacheStorageScheduler>&&, long&&, base::OnceCallback<void ()>&&>, base::internal::BindState<true, true, false, void (content::CacheStorageScheduler::*)(long, base::OnceCallback<void ()>), base::WeakPtr<content::CacheStorageScheduler>, long, base::OnceCallback<void ()>>, void ()>::RunImpl<void (content::CacheStorageScheduler::*)(long, base::OnceCallback<void ()>), std::__Cr::tuple<base::WeakPtr<content::CacheStorageScheduler>, long, base::OnceCallback<void ()>>, 0ul, 1ul, 2ul>(void (content::CacheStorageScheduler::*&&)(long, base::OnceCallback<void ()>), std::__Cr::tuple<base::WeakPtr<content::CacheStorageScheduler>, long, base::OnceCallback<void ()>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul>) base/functional/bind_internal.h:1067:14
    #7 0x5b4d1194f704 in Run base/functional/callback.h:156:12
    #8 0x5b4d1194f704 in base::internal::OnceCallbackHolder<>::Run() base/functional/callback_helpers.h:67:26
    #9 0x5b4d1194fa54 in Invoke<void (base::internal::OnceCallbackHolder<>::*)(), const std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<> > > &> base/functional/bind_internal.h:738:12
    #10 0x5b4d1194fa54 in MakeItSo<void (base::internal::OnceCallbackHolder<>::*const &)(), const std::__Cr::tuple<std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<> > > > &> base/functional/bind_internal.h:930:12
    #11 0x5b4d1194fa54 in RunImpl<void (base::internal::OnceCallbackHolder<>::*const &)(), const std::__Cr::tuple<std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<> > > > &, 0UL> base/functional/bind_internal.h:1067:14
    #12 0x5b4d1194fa54 in base::internal::Invoker<base::internal::FunctorTraits<void (base::internal::OnceCallbackHolder<>::* const&)(), std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<>>> const&>, base::internal::BindState<true, true, false, void (base::internal::OnceCallbackHolder<>::*)(), std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<>>>>, void ()>::Run(base::internal::BindStateBase*) base/functional/bind_internal.h:987:12
    #13 0x5b4d11924316 in Run base/functional/callback.h:156:12
    #14 0x5b4d11924316 in content::CacheStorageCache::InitGotCacheSizeAndPadding(base::OnceCallback<void ()>, blink::mojom::CacheStorageError, long, long) content/browser/cache_storage/cache_storage_cache.cc:2634:23
    #15 0x5b4d119231d4 in content::CacheStorageCache::InitGotCacheSize(base::OnceCallback<void ()>, blink::mojom::CacheStorageError, long) content/browser/cache_storage/cache_storage_cache.cc:0
    #16 0x5b4d119463d3 in Invoke<void (content::CacheStorageCache::*)(base::OnceCallback<void ()>, blink::mojom::CacheStorageError, long), const base::WeakPtr<content::CacheStorageCache> &, base::OnceCallback<void ()>, blink::mojom::CacheStorageError, long> base/functional/bind_internal.h:738:12
    #17 0x5b4d119463d3 in MakeItSo<void (content::CacheStorageCache::*)(base::OnceCallback<void ()>, blink::mojom::CacheStorageError, long), std::__Cr::tuple<base::WeakPtr<content::CacheStorageCache>, base::OnceCallback<void ()>, blink::mojom::CacheStorageError>, long> base/functional/bind_internal.h:954:5
    #18 0x5b4d119463d3 in void base::internal::Invoker<base::internal::FunctorTraits<void (content::CacheStorageCache::*&&)(base::OnceCallback<void ()>, blink::mojom::CacheStorageError, long), base::WeakPtr<content::CacheStorageCache>&&, base::OnceCallback<void ()>&&, blink::mojom::CacheStorageError&&>, base::internal::BindState<true, true, false, void (content::CacheStorageCache::*)(base::OnceCallback<void ()>, blink::mojom::CacheStorageError, long), base::WeakPtr<content::CacheStorageCache>, base::OnceCallback<void ()>, blink::mojom::CacheStorageError>, void (long)>::RunImpl<void (content::CacheStorageCache::*)(base::OnceCallback<void ()>, blink::mojom::CacheStorageError, long), std::__Cr::tuple<base::WeakPtr<content::CacheStorageCache>, base::OnceCallback<void ()>, blink::mojom::CacheStorageError>, 0ul, 1ul, 2ul>(void (content::CacheStorageCache::*&&)(base::OnceCallback<void ()>, blink::mojom::CacheStorageError, long), std::__Cr::tuple<base::WeakPtr<content::CacheStorageCache>, base::OnceCallback<void ()>, blink::mojom::CacheStorageError>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul>, long&&) base/functional/bind_internal.h:1067:14
    #19 0x5b4d11946125 in base::internal::Invoker<base::internal::FunctorTraits<void (content::CacheStorageCache::*&&)(base::OnceCallback<void ()>, blink::mojom::CacheStorageError, long), base::WeakPtr<content::CacheStorageCache>&&, base::OnceCallback<void ()>&&, blink::mojom::CacheStorageError&&>, base::internal::BindState<true, true, false, void (content::CacheStorageCache::*)(base::OnceCallback<void ()>, blink::mojom::CacheStorageError, long), base::WeakPtr<content::CacheStorageCache>, base::OnceCallback<void ()>, blink::mojom::CacheStorageError>, void (long)>::RunOnce(base::internal::BindStateBase*, long) base/functional/bind_internal.h:980:12
    #20 0x5b4d1bf4f6ae in Run base/functional/callback.h:156:12
    #21 0x5b4d1bf4f6ae in disk_cache::SimpleBackendImpl::IndexReadyForSizeCalculation(base::OnceCallback<void (long)>, int) net/disk_cache/simple/simple_backend_impl.cc:701:23
    #22 0x5b4d1bf56777 in Invoke<void (disk_cache::SimpleBackendImpl::*)(base::OnceCallback<void (long)>, int), const base::WeakPtr<disk_cache::SimpleBackendImpl> &, base::OnceCallback<void (long)>, int> base/functional/bind_internal.h:738:12
    #23 0x5b4d1bf56777 in MakeItSo<void (disk_cache::SimpleBackendImpl::*)(base::OnceCallback<void (long)>, int), std::__Cr::tuple<base::WeakPtr<disk_cache::SimpleBackendImpl>, base::OnceCallback<void (long)> >, int> base/functional/bind_internal.h:954:5
    #24 0x5b4d1bf56777 in void base::internal::Invoker<base::internal::FunctorTraits<void (disk_cache::SimpleBackendImpl::*&&)(base::OnceCallback<void (long)>, int), base::WeakPtr<disk_cache::SimpleBackendImpl>&&, base::OnceCallback<void (long)>&&>, base::internal::BindState<true, true, false, void (disk_cache::SimpleBackendImpl::*)(base::OnceCallback<void (long)>, int), base::WeakPtr<disk_cache::SimpleBackendImpl>, base::OnceCallback<void (long)>>, void (int)>::RunImpl<void (disk_cache::SimpleBackendImpl::*)(base::OnceCallback<void (long)>, int), std::__Cr::tuple<base::WeakPtr<disk_cache::SimpleBackendImpl>, base::OnceCallback<void (long)>>, 0ul, 1ul>(void (disk_cache::SimpleBackendImpl::*&&)(base::OnceCallback<void (long)>, int), std::__Cr::tuple<base::WeakPtr<disk_cache::SimpleBackendImpl>, base::OnceCallback<void (long)>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>, int&&) base/functional/bind_internal.h:1067:14
    #25 0x5b4d1bf564e4 in base::internal::Invoker<base::internal::FunctorTraits<void (disk_cache::SimpleBackendImpl::*&&)(base::OnceCallback<void (long)>, int), base::WeakPtr<disk_cache::SimpleBackendImpl>&&, base::OnceCallback<void (long)>&&>, base::internal::BindState<true, true, false, void (disk_cache::SimpleBackendImpl::*)(base::OnceCallback<void (long)>, int), base::WeakPtr<disk_cache::SimpleBackendImpl>, base::OnceCallback<void (long)>>, void (int)>::RunOnce(base::internal::BindStateBase*, int) base/functional/bind_internal.h:980:12
    #26 0x5b4d118879fe in Run base/functional/callback.h:156:12
    #27 0x5b4d118879fe in Invoke<base::OnceCallback<void (int)>, net::Error> base/functional/bind_internal.h:813:49
    #28 0x5b4d118879fe in MakeItSo<base::OnceCallback<void (int)>, std::__Cr::tuple<net::Error> > base/functional/bind_internal.h:930:12
    #29 0x5b4d118879fe in RunImpl<base::OnceCallback<void (int)>, std::__Cr::tuple<net::Error>, 0UL> base/functional/bind_internal.h:1067:14
    #30 0x5b4d118879fe in base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (int)>&&, net::Error&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (int)>, net::Error>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:980:12
    #31 0x5b4d1b2660a4 in Run base/functional/callback.h:156:12
    #32 0x5b4d1b2660a4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:202:34
    #33 0x5b4d1b2efcab in RunTask<(lambda at ../../base/task/thread_pool/task_tracker.cc:678:35)> base/task/common/task_annotator.h:90:5
    #34 0x5b4d1b2efcab in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:677:19
    #35 0x5b4d1b2efefc in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:662:3
    #36 0x5b4d1b2ef104 in RunTaskWithShutdownBehavior base/task/thread_pool/task_tracker.cc:692:7
    #37 0x5b4d1b2ef104 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) base/task/thread_pool/task_tracker.cc:520:5
    #38 0x5b4d1b2edfe4 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) base/task/thread_pool/task_tracker.cc:415:5
    #39 0x5b4d1b326a23 in base::internal::WorkerThread::RunWorker() base/task/thread_pool/worker_thread.cc:493:36
    #40 0x5b4d1b325b57 in base::internal::WorkerThread::RunPooledWorker() base/task/thread_pool/worker_thread.cc:379:3
    #41 0x5b4d1b32563e in base::internal::WorkerThread::ThreadMain() base/task/thread_pool/worker_thread.cc:359:7
    #42 0x5b4d1b392439 in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:101:13
    #43 0x5b4d0741f416 in asan_thread_start(void*) third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:239:28
    #44 0x7872a4e2c608 in start_thread /build/glibc-LcI20x/glibc-2.31/nptl/pthread_create.c:477:8
    #45 0x7872a3678352 in __clone /build/glibc-LcI20x/glibc-2.31/sysdeps/unix/sysv/linux/x86_64/clone.S:95
0x7522a1cfdba0 is located 16 bytes inside of 112-byte region [0x7522a1cfdb90,0x7522a1cfdc00)
freed by thread T5 (ThreadPoolForeg) here:
    #0 0x5b4d0745957d in operator delete(void*) third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:143:3
    #1 0x5b4d119a564f in content::CacheStorageScheduler::~CacheStorageScheduler() content/browser/cache_storage/cache_storage_scheduler.cc:69:49
    #2 0x5b4d1190446f in operator() third_party/libc++/src/include/__memory/unique_ptr.h:69:5
    #3 0x5b4d1190446f in reset third_party/libc++/src/include/__memory/unique_ptr.h:285:7
    #4 0x5b4d1190446f in ~unique_ptr third_party/libc++/src/include/__memory/unique_ptr.h:254:71
    #5 0x5b4d1190446f in content::CacheStorageCache::~CacheStorageCache() content/browser/cache_storage/cache_storage_cache.cc:1044:39
    #6 0x5b4d11904a23 in content::CacheStorageCache::~CacheStorageCache() content/browser/cache_storage/cache_storage_cache.cc:1044:39
    #7 0x5b4d118c55d0 in operator() third_party/libc++/src/include/__memory/unique_ptr.h:69:5
    #8 0x5b4d118c55d0 in reset third_party/libc++/src/include/__memory/unique_ptr.h:285:7
    #9 0x5b4d118c55d0 in ReleaseUnreferencedCaches content/browser/cache_storage/cache_storage.cc:932:20
    #10 0x5b4d118c55d0 in content::CacheStorage::DropHandleRef() content/browser/cache_storage/cache_storage.cc:652:5
    #11 0x5b4d118f82c3 in content::CacheStorageRef<content::CacheStorage>::~CacheStorageRef() content/browser/cache_storage/cache_storage_ref.h:45:16
    #12 0x5b4d118f8591 in content::CacheStorageCache::DropHandleRef() content/browser/cache_storage/cache_storage_cache.cc:676:3
    #13 0x5b4d118d19d3 in content::CacheStorageRef<content::CacheStorageCache>::~CacheStorageRef() content/browser/cache_storage/cache_storage_ref.h:45:16
    #14 0x5b4d11949ca0 in void base::internal::DecayedFunctorTraits<void (content::CacheStorageCache::*)(content::CacheStorageRef<content::CacheStorageCache>, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>, blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>), base::WeakPtr<content::CacheStorageCache>&&, content::CacheStorageRef<content::CacheStorageCache>&&, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>&&>::Invoke<void (content::CacheStorageCache::*)(content::CacheStorageRef<content::CacheStorageCache>, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>, blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>), base::WeakPtr<content::CacheStorageCache> const&, content::CacheStorageRef<content::CacheStorageCache>, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>, blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>>(void (content::CacheStorageCache::*)(content::CacheStorageRef<content::CacheStorageCache>, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>, blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>), base::WeakPtr<content::CacheStorageCache> const&, content::CacheStorageRef<content::CacheStorageCache>&&, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>&&, blink::mojom::CacheStorageError&&, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>&&) base/functional/bind_internal.h:738:5
    #15 0x5b4d11949945 in MakeItSo<void (content::CacheStorageCache::*)(content::CacheStorageRef<content::CacheStorageCache>, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse> > >)>, blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse> > >), std::__Cr::tuple<base::WeakPtr<content::CacheStorageCache>, content::CacheStorageRef<content::CacheStorageCache>, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse> > >)> >, blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse> > > > base/functional/bind_internal.h:954:5
    #16 0x5b4d11949945 in RunImpl<void (content::CacheStorageCache::*)(content::CacheStorageRef<content::CacheStorageCache>, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse> > >)>, blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse> > >), std::__Cr::tuple<base::WeakPtr<content::CacheStorageCache>, content::CacheStorageRef<content::CacheStorageCache>, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse> > >)> >, 0UL, 1UL, 2UL> base/functional/bind_internal.h:1067:14
    #17 0x5b4d11949945 in base::internal::Invoker<base::internal::FunctorTraits<void (content::CacheStorageCache::*&&)(content::CacheStorageRef<content::CacheStorageCache>, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>, blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>), base::WeakPtr<content::CacheStorageCache>&&, content::CacheStorageRef<content::CacheStorageCache>&&, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>&&>, base::internal::BindState<true, true, false, void (content::CacheStorageCache::*)(content::CacheStorageRef<content::CacheStorageCache>, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>, blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>), base::WeakPtr<content::CacheStorageCache>, content::CacheStorageRef<content::CacheStorageCache>, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>>, void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>::RunOnce(base::internal::BindStateBase*, blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>&&) base/functional/bind_internal.h:980:12
    #18 0x5b4d1190f5bb in Run base/functional/callback.h:156:12
    #19 0x5b4d1190f5bb in content::CacheStorageCache::MatchAllDidQueryCache(base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>, long, blink::mojom::CacheStorageError, std::__Cr::unique_ptr<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>, std::__Cr::default_delete<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>>>) content/browser/cache_storage/cache_storage_cache.cc:1523:23
    #20 0x5b4d11939d19 in Invoke<void (content::CacheStorageCache::*)(base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse> > >)>, long, blink::mojom::CacheStorageError, std::__Cr::unique_ptr<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult> >, std::__Cr::default_delete<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult> > > >), const base::WeakPtr<content::CacheStorageCache> &, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse> > >)>, long, blink::mojom::CacheStorageError, std::__Cr::unique_ptr<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult> >, std::__Cr::default_delete<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult> > > > > base/functional/bind_internal.h:738:12
    #21 0x5b4d11939d19 in MakeItSo<void (content::CacheStorageCache::*)(base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse> > >)>, long, blink::mojom::CacheStorageError, std::__Cr::unique_ptr<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult> >, std::__Cr::default_delete<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult> > > >), std::__Cr::tuple<base::WeakPtr<content::CacheStorageCache>, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse> > >)>, long>, blink::mojom::CacheStorageError, std::__Cr::unique_ptr<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult> >, std::__Cr::default_delete<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult> > > > > base/functional/bind_internal.h:954:5
    #22 0x5b4d11939d19 in RunImpl<void (content::CacheStorageCache::*)(base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse> > >)>, long, blink::mojom::CacheStorageError, std::__Cr::unique_ptr<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult> >, std::__Cr::default_delete<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult> > > >), std::__Cr::tuple<base::WeakPtr<content::CacheStorageCache>, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse> > >)>, long>, 0UL, 1UL, 2UL> base/functional/bind_internal.h:1067:14
    #23 0x5b4d11939d19 in base::internal::Invoker<base::internal::FunctorTraits<void (content::CacheStorageCache::*&&)(base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>, long, blink::mojom::CacheStorageError, std::__Cr::unique_ptr<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>, std::__Cr::default_delete<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>>>), base::WeakPtr<content::CacheStorageCache>&&, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>&&, long&&>, base::internal::BindState<true, true, false, void (content::CacheStorageCache::*)(base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>, long, blink::mojom::CacheStorageError, std::__Cr::unique_ptr<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>, std::__Cr::default_delete<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>>>), base::WeakPtr<content::CacheStorageCache>, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>, long>, void (blink::mojom::CacheStorageError, std::__Cr::unique_ptr<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>, std::__Cr::default_delete<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>>>)>::RunOnce(base::internal::BindStateBase*, blink::mojom::CacheStorageError, std::__Cr::unique_ptr<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>, std::__Cr::default_delete<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>>>&&) base/functional/bind_internal.h:980:12
    #24 0x5b4d119067c5 in base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::unique_ptr<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>, std::__Cr::default_delete<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>>>)>::Run(blink::mojom::CacheStorageError, std::__Cr::unique_ptr<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>, std::__Cr::default_delete<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>>>) && base/functional/callback.h:156:12
    #25 0x5b4d1190730f in content::CacheStorageCache::QueryCacheDidOpenFastPath(std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext>>, disk_cache::EntryResult) content/browser/cache_storage/cache_storage_cache.cc:1150:10
    #26 0x5b4d1192e710 in void base::internal::DecayedFunctorTraits<void (content::CacheStorageCache::*)(std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext>>, disk_cache::EntryResult), base::WeakPtr<content::CacheStorageCache>&&, std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext>>&&>::Invoke<void (content::CacheStorageCache::*)(std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext>>, disk_cache::EntryResult), base::WeakPtr<content::CacheStorageCache> const&, std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext>>, disk_cache::EntryResult>(void (content::CacheStorageCache::*)(std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext>>, disk_cache::EntryResult), base::WeakPtr<content::CacheStorageCache> const&, std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext>>&&, disk_cache::EntryResult&&) base/functional/bind_internal.h:738:12
    #27 0x5b4d1192e4db in MakeItSo<void (content::CacheStorageCache::*)(std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext> >, disk_cache::EntryResult), std::__Cr::tuple<base::WeakPtr<content::CacheStorageCache>, std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext> > >, disk_cache::EntryResult> base/functional/bind_internal.h:954:5
    #28 0x5b4d1192e4db in RunImpl<void (content::CacheStorageCache::*)(std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext> >, disk_cache::EntryResult), std::__Cr::tuple<base::WeakPtr<content::CacheStorageCache>, std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext> > >, 0UL, 1UL> base/functional/bind_internal.h:1067:14
    #29 0x5b4d1192e4db in base::internal::Invoker<base::internal::FunctorTraits<void (content::CacheStorageCache::*&&)(std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext>>, disk_cache::EntryResult), base::WeakPtr<content::CacheStorageCache>&&, std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext>>&&>, base::internal::BindState<true, true, false, void (content::CacheStorageCache::*)(std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext>>, disk_cache::EntryResult), base::WeakPtr<content::CacheStorageCache>, std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext>>>, void (disk_cache::EntryResult)>::RunOnce(base::internal::BindStateBase*, disk_cache::EntryResult&&) base/functional/bind_internal.h:980:12
    #30 0x5b4d11948faa in Run base/functional/callback.h:156:12
    #31 0x5b4d11948faa in base::internal::OnceCallbackHolder<disk_cache::EntryResult>::Run(disk_cache::EntryResult) base/functional/callback_helpers.h:67:26
    #32 0x5b4d1194930c in Invoke<void (base::internal::OnceCallbackHolder<disk_cache::EntryResult>::*)(disk_cache::EntryResult), const std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<disk_cache::EntryResult>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<disk_cache::EntryResult> > > &, disk_cache::EntryResult> base/functional/bind_internal.h:738:12
    #33 0x5b4d1194930c in MakeItSo<void (base::internal::OnceCallbackHolder<disk_cache::EntryResult>::*const &)(disk_cache::EntryResult), const std::__Cr::tuple<std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<disk_cache::EntryResult>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<disk_cache::EntryResult> > > > &, disk_cache::EntryResult> base/functional/bind_internal.h:930:12
    #34 0x5b4d1194930c in RunImpl<void (base::internal::OnceCallbackHolder<disk_cache::EntryResult>::*const &)(disk_cache::EntryResult), const std::__Cr::tuple<std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<disk_cache::EntryResult>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<disk_cache::EntryResult> > > > &, 0UL> base/functional/bind_internal.h:1067:14
    #35 0x5b4d1194930c in base::internal::Invoker<base::internal::FunctorTraits<void (base::internal::OnceCallbackHolder<disk_cache::EntryResult>::* const&)(disk_cache::EntryResult), std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<disk_cache::EntryResult>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<disk_cache::EntryResult>>> const&>, base::internal::BindState<true, true, false, void (base::internal::OnceCallbackHolder<disk_cache::EntryResult>::*)(disk_cache::EntryResult), std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<disk_cache::EntryResult>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<disk_cache::EntryResult>>>>, void (disk_cache::EntryResult)>::Run(base::internal::BindStateBase*, disk_cache::EntryResult&&) base/functional/bind_internal.h:987:12
    #36 0x5b4d11906260 in Run base/functional/callback.h:156:12
    #37 0x5b4d11906260 in content::CacheStorageCache::QueryCache(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, int, content::CacheStorageSchedulerPriority, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::unique_ptr<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>, std::__Cr::default_delete<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>>>)>) content/browser/cache_storage/cache_storage_cache.cc:1136:40
    #38 0x5b4d118fa2ff in content::CacheStorageCache::MatchAllImpl(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, long, content::CacheStorageSchedulerPriority, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>) content/browser/cache_storage/cache_storage_cache.cc:1493:3
    #39 0x5b4d118f9316 in content::CacheStorageCache::MatchImpl(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, long, content::CacheStorageSchedulerPriority, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>) content/browser/cache_storage/cache_storage_cache.cc:1447:3
    #40 0x5b4d119250f7 in void base::internal::DecayedFunctorTraits<void (content::CacheStorageCache::*)(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, long, content::CacheStorageSchedulerPriority, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>), base::WeakPtr<content::CacheStorageCache>&&, mojo::StructPtr<blink::mojom::FetchAPIRequest>&&, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>&&, long&&, content::CacheStorageSchedulerPriority&&, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>&&>::Invoke<void (content::CacheStorageCache::*)(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, long, content::CacheStorageSchedulerPriority, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>), base::WeakPtr<content::CacheStorageCache> const&, mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, long, content::CacheStorageSchedulerPriority, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>>(void (content::CacheStorageCache::*)(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, long, content::CacheStorageSchedulerPriority, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>), base::WeakPtr<content::CacheStorageCache> const&, mojo::StructPtr<blink::mojom::FetchAPIRequest>&&, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>&&, long&&, content::CacheStorageSchedulerPriority&&, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>&&) base/functional/bind_internal.h:738:12
    #41 0x5b4d11924d70 in MakeItSo<void (content::CacheStorageCache::*)(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, long, content::CacheStorageSchedulerPriority, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>), std::__Cr::tuple<base::WeakPtr<content::CacheStorageCache>, mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, long, content::CacheStorageSchedulerPriority, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)> > > base/functional/bind_internal.h:954:5
    #42 0x5b4d11924d70 in RunImpl<void (content::CacheStorageCache::*)(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, long, content::CacheStorageSchedulerPriority, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>), std::__Cr::tuple<base::WeakPtr<content::CacheStorageCache>, mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, long, content::CacheStorageSchedulerPriority, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)> >, 0UL, 1UL, 2UL, 3UL, 4UL, 5UL> base/functional/bind_internal.h:1067:14
    #43 0x5b4d11924d70 in base::internal::Invoker<base::internal::FunctorTraits<void (content::CacheStorageCache::*&&)(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, long, content::CacheStorageSchedulerPriority, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>), base::WeakPtr<content::CacheStorageCache>&&, mojo::StructPtr<blink::mojom::FetchAPIRequest>&&, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>&&, long&&, content::CacheStorageSchedulerPriority&&, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>&&>, base::internal::BindState<true, true, false, void (content::CacheStorageCache::*)(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, long, content::CacheStorageSchedulerPriority, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>), base::WeakPtr<content::CacheStorageCache>, mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, long, content::CacheStorageSchedulerPriority, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:980:12
    #44 0x5b4d119a3c86 in Run base/functional/callback.h:156:12
    #45 0x5b4d119a3c86 in content::CacheStorageOperation::Run() content/browser/cache_storage/cache_storage_operation.cc:37:23
    #46 0x5b4d119a8a3d in Invoke<void (content::CacheStorageOperation::*)(), const base::WeakPtr<content::CacheStorageOperation> &> base/functional/bind_internal.h:738:12
    #47 0x5b4d119a8a3d in MakeItSo<void (content::CacheStorageOperation::*)(), std::__Cr::tuple<base::WeakPtr<content::CacheStorageOperation> > > base/functional/bind_internal.h:954:5
    #48 0x5b4d119a8a3d in void base::internal::Invoker<base::internal::FunctorTraits<void (content::CacheStorageOperation::*&&)(), base::WeakPtr<content::CacheStorageOperation>&&>, base::internal::BindState<true, true, false, void (content::CacheStorageOperation::*)(), base::WeakPtr<content::CacheStorageOperation>>, void ()>::RunImpl<void (content::CacheStorageOperation::*)(), std::__Cr::tuple<base::WeakPtr<content::CacheStorageOperation>>, 0ul>(void (content::CacheStorageOperation::*&&)(), std::__Cr::tuple<base::WeakPtr<content::CacheStorageOperation>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/bind_internal.h:1067:14
    #49 0x5b4d119a76d7 in Run base/functional/callback.h:156:12
    #50 0x5b4d119a76d7 in content::CacheStorageScheduler::DispatchOperationTask(base::OnceCallback<void ()>) content/browser/cache_storage/cache_storage_scheduler.cc:131:19
    #51 0x5b4d119a6873 in content::CacheStorageScheduler::MaybeRunOperation() content/browser/cache_storage/cache_storage_scheduler.cc:184:5
    #52 0x5b4d119a7456 in content::CacheStorageScheduler::CompleteOperationAndRunNext(long) content/browser/cache_storage/cache_storage_scheduler.cc:116:3
    #53 0x5b4d11948548 in void content::CacheStorageScheduler::RunNextContinuation<>(long, base::OnceCallback<void ()>) content/browser/cache_storage/cache_storage_scheduler.h:102:7
    #54 0x5b4d1194891d in Invoke<void (content::CacheStorageScheduler::*)(long, base::OnceCallback<void ()>), const base::WeakPtr<content::CacheStorageScheduler> &, long, base::OnceCallback<void ()> > base/functional/bind_internal.h:738:12
    #55 0x5b4d1194891d in MakeItSo<void (content::CacheStorageScheduler::*)(long, base::OnceCallback<void ()>), std::__Cr::tuple<base::WeakPtr<content::CacheStorageScheduler>, long, base::OnceCallback<void ()> > > base/functional/bind_internal.h:954:5
    #56 0x5b4d1194891d in void base::internal::Invoker<base::internal::FunctorTraits<void (content::CacheStorageScheduler::*&&)(long, base::OnceCallback<void ()>), base::WeakPtr<content::CacheStorageScheduler>&&, long&&, base::OnceCallback<void ()>&&>, base::internal::BindState<true, true, false, void (content::CacheStorageScheduler::*)(long, base::OnceCallback<void ()>), base::WeakPtr<content::CacheStorageScheduler>, long, base::OnceCallback<void ()>>, void ()>::RunImpl<void (content::CacheStorageScheduler::*)(long, base::OnceCallback<void ()>), std::__Cr::tuple<base::WeakPtr<content::CacheStorageScheduler>, long, base::OnceCallback<void ()>>, 0ul, 1ul, 2ul>(void (content::CacheStorageScheduler::*&&)(long, base::OnceCallback<void ()>), std::__Cr::tuple<base::WeakPtr<content::CacheStorageScheduler>, long, base::OnceCallback<void ()>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul>) base/functional/bind_internal.h:1067:14
previously allocated by thread T5 (ThreadPoolForeg) here:
    #0 0x5b4d07458d1d in operator new(unsigned long) third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:86:3
    #1 0x5b4d11904d2d in content::CacheStorageCache::CacheStorageCache(storage::BucketLocator const&, storage::mojom::CacheStorageOwner, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, base::FilePath const&, content::CacheStorage*, scoped_refptr<base::SequencedTaskRunner>, scoped_refptr<storage::QuotaManagerProxy>, scoped_refptr<content::BlobStorageContextWrapper>, long, long) content/browser/cache_storage/cache_storage_cache.cc:1070:18
    #2 0x5b4d118f7649 in content::CacheStorageCache::CreatePersistentCache(storage::BucketLocator const&, storage::mojom::CacheStorageOwner, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::CacheStorage*, base::FilePath const&, scoped_refptr<base::SequencedTaskRunner>, scoped_refptr<storage::QuotaManagerProxy>, scoped_refptr<content::BlobStorageContextWrapper>, long, long) content/browser/cache_storage/cache_storage_cache.cc:639:34
    #3 0x5b4d118d869a in content::CacheStorage::SimpleCacheLoader::CreateCache(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, long, long) content/browser/cache_storage/cache_storage.cc:263:12
    #4 0x5b4d118d17dd in content::CacheStorage::GetLoadedCache(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&) content/browser/cache_storage/cache_storage.cc:1363:67
    #5 0x5b4d118cc641 in content::CacheStorage::MatchAllCachesImpl(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, content::CacheStorageSchedulerPriority, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>) content/browser/cache_storage/cache_storage.cc:1276:44
    #6 0x5b4d118e3ca6 in void base::internal::DecayedFunctorTraits<void (content::CacheStorage::*)(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, content::CacheStorageSchedulerPriority, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>), base::WeakPtr<content::CacheStorage>&&, mojo::StructPtr<blink::mojom::FetchAPIRequest>&&, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>&&, content::CacheStorageSchedulerPriority&&, long&&, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>&&>::Invoke<void (content::CacheStorage::*)(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, content::CacheStorageSchedulerPriority, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>), base::WeakPtr<content::CacheStorage> const&, mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, content::CacheStorageSchedulerPriority, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>>(void (content::CacheStorage::*)(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, content::CacheStorageSchedulerPriority, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>), base::WeakPtr<content::CacheStorage> const&, mojo::StructPtr<blink::mojom::FetchAPIRequest>&&, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>&&, content::CacheStorageSchedulerPriority&&, long&&, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>&&) base/functional/bind_internal.h:738:12
    #7 0x5b4d118e3920 in MakeItSo<void (content::CacheStorage::*)(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, content::CacheStorageSchedulerPriority, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>), std::__Cr::tuple<base::WeakPtr<content::CacheStorage>, mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, content::CacheStorageSchedulerPriority, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)> > > base/functional/bind_internal.h:954:5
    #8 0x5b4d118e3920 in RunImpl<void (content::CacheStorage::*)(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, content::CacheStorageSchedulerPriority, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>), std::__Cr::tuple<base::WeakPtr<content::CacheStorage>, mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, content::CacheStorageSchedulerPriority, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)> >, 0UL, 1UL, 2UL, 3UL, 4UL, 5UL> base/functional/bind_internal.h:1067:14
    #9 0x5b4d118e3920 in base::internal::Invoker<base::internal::FunctorTraits<void (content::CacheStorage::*&&)(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, content::CacheStorageSchedulerPriority, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>), base::WeakPtr<content::CacheStorage>&&, mojo::StructPtr<blink::mojom::FetchAPIRequest>&&, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>&&, content::CacheStorageSchedulerPriority&&, long&&, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>&&>, base::internal::BindState<true, true, false, void (content::CacheStorage::*)(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, content::CacheStorageSchedulerPriority, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>), base::WeakPtr<content::CacheStorage>, mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, content::CacheStorageSchedulerPriority, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:980:12
    #10 0x5b4d119a3c86 in Run base/functional/callback.h:156:12
    #11 0x5b4d119a3c86 in content::CacheStorageOperation::Run() content/browser/cache_storage/cache_storage_operation.cc:37:23
    #12 0x5b4d119a8a3d in Invoke<void (content::CacheStorageOperation::*)(), const base::WeakPtr<content::CacheStorageOperation> &> base/functional/bind_internal.h:738:12
    #13 0x5b4d119a8a3d in MakeItSo<void (content::CacheStorageOperation::*)(), std::__Cr::tuple<base::WeakPtr<content::CacheStorageOperation> > > base/functional/bind_internal.h:954:5
    #14 0x5b4d119a8a3d in void base::internal::Invoker<base::internal::FunctorTraits<void (content::CacheStorageOperation::*&&)(), base::WeakPtr<content::CacheStorageOperation>&&>, base::internal::BindState<true, true, false, void (content::CacheStorageOperation::*)(), base::WeakPtr<content::CacheStorageOperation>>, void ()>::RunImpl<void (content::CacheStorageOperation::*)(), std::__Cr::tuple<base::WeakPtr<content::CacheStorageOperation>>, 0ul>(void (content::CacheStorageOperation::*&&)(), std::__Cr::tuple<base::WeakPtr<content::CacheStorageOperation>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/bind_internal.h:1067:14
    #15 0x5b4d119a76d7 in Run base/functional/callback.h:156:12
    #16 0x5b4d119a76d7 in content::CacheStorageScheduler::DispatchOperationTask(base::OnceCallback<void ()>) content/browser/cache_storage/cache_storage_scheduler.cc:131:19
    #17 0x5b4d119a6873 in content::CacheStorageScheduler::MaybeRunOperation() content/browser/cache_storage/cache_storage_scheduler.cc:184:5
    #18 0x5b4d119a5a97 in content::CacheStorageScheduler::ScheduleOperation(long, content::CacheStorageSchedulerMode, content::CacheStorageSchedulerOp, content::CacheStorageSchedulerPriority, base::OnceCallback<void ()>) content/browser/cache_storage/cache_storage_scheduler.cc:94:3
    #19 0x5b4d118cbe0a in content::CacheStorage::MatchAllCaches(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, content::CacheStorageSchedulerPriority, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>) content/browser/cache_storage/cache_storage.cc:789:15
    #20 0x5b4d119784e3 in content::CacheStorageDispatcherHost::CacheStorageImpl::Match(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, bool, long, base::OnceCallback<void (mojo::StructPtr<blink::mojom::MatchResult>)>)::'lambda'(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>, content::CacheStorage*)::operator()(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>, content::CacheStorage*) const content/browser/cache_storage/cache_storage_dispatcher_host.cc:939:28
    #21 0x5b4d11977fae in void base::internal::DecayedFunctorTraits<content::CacheStorageDispatcherHost::CacheStorageImpl::Match(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, bool, long, base::OnceCallback<void (mojo::StructPtr<blink::mojom::MatchResult>)>)::'lambda'(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>, content::CacheStorage*), mojo::StructPtr<blink::mojom::FetchAPIRequest>&&, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>&&, bool&&, long&&, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>&&>::Invoke<content::CacheStorageDispatcherHost::CacheStorageImpl::Match(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, bool, long, base::OnceCallback<void (mojo::StructPtr<blink::mojom::MatchResult>)>)::'lambda'(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>, content::CacheStorage*), mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>, content::CacheStorage*>(content::CacheStorageDispatcherHost::CacheStorageImpl::Match(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, bool, long, base::OnceCallback<void (mojo::StructPtr<blink::mojom::MatchResult>)>)::'lambda'(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>, content::CacheStorage*)&&, mojo::StructPtr<blink::mojom::FetchAPIRequest>&&, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>&&, bool&&, long&&, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>&&, content::CacheStorage*&&) base/functional/bind_internal.h:656:12
    #22 0x5b4d11977d78 in MakeItSo<(lambda at ../../content/browser/cache_storage/cache_storage_dispatcher_host.cc:923:9), std::__Cr::tuple<mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)> >, content::CacheStorage *> base/functional/bind_internal.h:930:12
    #23 0x5b4d11977d78 in RunImpl<(lambda at ../../content/browser/cache_storage/cache_storage_dispatcher_host.cc:923:9), std::__Cr::tuple<mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)> >, 0UL, 1UL, 2UL, 3UL, 4UL> base/functional/bind_internal.h:1067:14
    #24 0x5b4d11977d78 in base::internal::Invoker<base::internal::FunctorTraits<content::CacheStorageDispatcherHost::CacheStorageImpl::Match(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, bool, long, base::OnceCallback<void (mojo::StructPtr<blink::mojom::MatchResult>)>)::'lambda'(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>, content::CacheStorage*)&&, mojo::StructPtr<blink::mojom::FetchAPIRequest>&&, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>&&, bool&&, long&&, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>&&>, base::internal::BindState<false, false, false, content::CacheStorageDispatcherHost::CacheStorageImpl::Match(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, bool, long, base::OnceCallback<void (mojo::StructPtr<blink::mojom::MatchResult>)>)::'lambda'(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>, content::CacheStorage*), mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>>, void (content::CacheStorage*)>::RunOnce(base::internal::BindStateBase*, content::CacheStorage*) base/functional/bind_internal.h:980:12
    #25 0x5b4d1196aac3 in Run base/functional/callback.h:156:12
    #26 0x5b4d1196aac3 in content::CacheStorageDispatcherHost::CacheStorageImpl::GetOrCreateCacheStorage(base::OnceCallback<void (content::CacheStorage*)>) content/browser/cache_storage/cache_storage_dispatcher_host.cc:1091:25
    #27 0x5b4d1196cfd5 in content::CacheStorageDispatcherHost::CacheStorageImpl::Match(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, bool, long, base::OnceCallback<void (mojo::StructPtr<blink::mojom::MatchResult>)>) content/browser/cache_storage/cache_storage_dispatcher_host.cc:922:5
    #28 0x5b4d0c0ad117 in blink::mojom::CacheStorageStubDispatch::AcceptWithResponder(blink::mojom::CacheStorage*, mojo::Message*, std::__Cr::unique_ptr<mojo::MessageReceiverWithStatus, std::__Cr::default_delete<mojo::MessageReceiverWithStatus>>) gen/third_party/blink/public/mojom/cache_storage/cache_storage.mojom.cc:3680:13
    #29 0x5b4d1b06a1dc in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1005:56
    #30 0x5b4d1b08604d in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:48:24
    #31 0x5b4d1b06fb35 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:724:20
    #32 0x5b4d1b094b31 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1121:42
    #33 0x5b4d1b092dab in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:734:7
    #34 0x5b4d1b08614a in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #35 0x5b4d1b0614c1 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) mojo/public/cpp/bindings/lib/connector.cc:562:49
    #36 0x5b4d1b062e00 in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:620:14
    #37 0x5b4d1b062829 in OnHandleReadyInternal mojo/public/cpp/bindings/lib/connector.cc:452:3
    #38 0x5b4d1b062829 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int) mojo/public/cpp/bindings/lib/connector.cc:418:3
    #39 0x5b4d1b06412a in Invoke<void (mojo::Connector::*)(const char *, unsigned int), mojo::Connector *, const char *, unsigned int> base/functional/bind_internal.h:738:12
    #40 0x5b4d1b06412a in MakeItSo<void (mojo::Connector::*const &)(const char *, unsigned int), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, unsigned int> base/functional/bind_internal.h:930:12
    #41 0x5b4d1b06412a in RunImpl<void (mojo::Connector::*const &)(const char *, unsigned int), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, 0UL, 1UL> base/functional/bind_internal.h:1067:14
    #42 0x5b4d1b06412a in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int) base/functional/bind_internal.h:987:12
Thread T5 (ThreadPoolForeg) created by T0 (chrome) here:
    #0 0x5b4d074022f1 in ___interceptor_pthread_create third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:250:3
    #1 0x5b4d1b391958 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) base/threading/platform_thread_posix.cc:146:13
    #2 0x5b4d1b32467d in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*) base/task/thread_pool/worker_thread.cc:207:3
    #3 0x5b4d1b2f251c in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush() base/task/thread_pool/thread_group.cc:92:13
    #4 0x5b4d1b2f203f in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor() base/task/thread_pool/thread_group.cc:83:3
    #5 0x5b4d1b319b55 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::~ScopedCommandsExecutor() base/task/thread_pool/thread_group_impl.cc:49:3
    #6 0x5b4d1b319668 in base::internal::ThreadGroupImpl::Start(unsigned long, unsigned long, base::TimeDelta, scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*, base::internal::ThreadGroup::WorkerEnvironment, bool, std::__Cr::optional<base::TimeDelta>) base/task/thread_pool/thread_group_impl.cc:248:1
    #7 0x5b4d1b2fe006 in base::internal::ThreadPoolImpl::Start(base::ThreadPoolInstance::InitParams const&, base::WorkerThreadObserver*) base/task/thread_pool/thread_pool_impl.cc:190:35
    #8 0x5b4d1310f9c6 in content::StartBrowserThreadPool() content/browser/startup_helper.cc:100:36
    #9 0x5b4d1857844d in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1243:5
    #10 0x5b4d1857797c in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1162:12
    #11 0x5b4d18572675 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:356:36
    #12 0x5b4d18572c8b in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:369:10
    #13 0x5b4d0745b563 in ChromeMain chrome/app/chrome_main.cc:231:12
    #14 0x7872a357d082 in __libc_start_main /build/glibc-LcI20x/glibc-2.31/csu/libc-start.c:308:16
SUMMARY: AddressSanitizer: heap-use-after-free (/mnt/scratch0/clusterfuzz/bot/builds/chromium-browser-asan_linux-release-media_eb660d5ee526c9c1c1608a71fcbe7a713c490533/revisions/chrome+0x19932feb) (BuildId: e876de8902f8a99d)
Shadow bytes around the buggy address:
  0x7522a1cfd900: fd fd fd fd fd fd fd fa fa fa fa fa fa fa f7 fa
  0x7522a1cfd980: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa
  0x7522a1cfda00: fa fa fa fa f7 fa fd fd fd fd fd fd fd fd fd fd
  0x7522a1cfda80: fd fd fd fa fa fa fa fa fa fa f7 fa fd fd fd fd
  0x7522a1cfdb00: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa
=>0x7522a1cfdb80: f7 fa fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd
  0x7522a1cfdc00: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x7522a1cfdc80: fd fd fd fd fd fa fa fa fa fa fa fa f7 fa fd fd
  0x7522a1cfdd00: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x7522a1cfdd80: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x7522a1cfde00: fd fa fa fa fa fa fa fa f7 fa fd fd fd fd fd fd
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
==382468==ADDITIONAL INFO
==382468==Note: Please include this section with the ASan report.
Task trace:
    #0 0x5b4d1bf94d0b in disk_cache::SimpleIndex::MergeInitializingSet(std::__Cr::unique_ptr<disk_cache::SimpleIndexLoadResult, std::__Cr::default_delete<disk_cache::SimpleIndexLoadResult>>) net/disk_cache/simple/simple_index.cc:600:28
    #1 0x5b4d1bfa6487 in disk_cache::SimpleIndexFile::LoadIndexEntries(base::Time, base::OnceCallback<void ()>, disk_cache::SimpleIndexLoadResult*) net/disk_cache/simple/simple_index_file.cc:377:33
    #2 0x5b4d1bfa6487 in disk_cache::SimpleIndexFile::LoadIndexEntries(base::Time, base::OnceCallback<void ()>, disk_cache::SimpleIndexLoadResult*) net/disk_cache/simple/simple_index_file.cc:377:33
    #3 0x5b4d1bf44493 in disk_cache::SimpleBackendImpl::Init(base::OnceCallback<void (int)>) net/disk_cache/simple/simple_backend_impl.cc:272:7
Command line: `/mnt/scratch0/clusterfuzz/bot/builds/chromium-browser-asan_linux-release-media_eb660d5ee526c9c1c1608a71fcbe7a713c490533/revisions/chrome --user-data-dir=/mnt/scratch0/tmp/user_profile_0 --enable-logging=stderr --v=1 --ignore-gpu-blacklist --allow-file-access-from-files --disable-gesture-requirement-for-media-playback --disable-click-to-play --disable-hang-monitor --dns-prefetch-disable --disable-default-apps --disable-component-update --safebrowsing-disable-auto-update --metrics-recording-only --disable-gpu-watchdog --disable-metrics --disable-popup-blocking --disable-prompt-on-repost --enable-experimental-extension-apis --enable-extension-apps --force-internal-pdf --js-flags=--expose-gc --verify-heap --new-window --no-default-browser-check --no-first-run --no-process-singleton-dialog --use-gl=angle --use-angle=swiftshader --enable-shadow-dom --enable-media-stream --enable-mp3-stream-parser --disable-in-process-stack-traces --enable-features=WebMachineLearningNeuralNetwork --flag-switches-begin --flag-switches-end /mnt/scratch0/clusterfuzz/bot/inputs/fuzzer-testcases/fuzz-00089.html`
MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

```

## Attachments

- [patch_for_reproduce.diff](attachments/patch_for_reproduce.diff) (text/x-diff, 967 B)
- [h1.js](attachments/h1.js) (text/javascript, 3.7 KB)
- [poc.html](attachments/poc.html) (text/html, 197.3 KB)
- [worklet-reftest.js](attachments/worklet-reftest.js) (text/javascript, 1.2 KB)
- [min.html](attachments/min.html) (text/html, 2.4 KB)
- [Video.webm](attachments/Video.webm) (video/webm, 6.1 MB)
- [h1.js](attachments/h1.js) (text/javascript, 3.7 KB)
- [poc.html](attachments/poc.html) (text/html, 197.4 KB)
- [Video2.webm](attachments/Video2.webm) (video/webm, 5.6 MB)
- [min.html](attachments/min.html) (text/html, 1.5 KB)

## Timeline

### m....@gmail.com (2024-09-29)

# RCA

Correct my previous analysis. The key issue is only with the operation while (!pending\_operations\_.empty()), because there is no guarantee that the current this is still valid.

Upon analysis, i was found that the key is to make the logic at[1] take effect. Here, I am providing a patch. After applying the patch, the issue can be reproduced consistently.

# Reproduce

chrome --user-data-dir=test --allow-file-access-from-files --no-default-browser-check --no-first-run poc.html

1. <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/cache_storage/cache_storage.cc;l=1354-1368;drc=f522344e45882da4c7f7cb1b3a0a7bd747d654bb?q=cache_storage.cc&ss=chromium%2Fchromium%2Fsrc>

### m....@gmail.com (2024-09-30)

Minimal POC for Reproduction

### th...@chromium.org (2024-09-30)

Hi reporter, I applied the patch locally from [#comment2](https://issues.chromium.org/issues/370069678#comment2) on Linux and ran `out/asan/chrome --user-data-dir=test --allow-file-access-from-files --no-default-browser-check --no-first-run poc.html` (using min.html from [#comment3](https://issues.chromium.org/issues/370069678#comment3)), but I am not able to reproduce this. I tried it 5 times and consistently saw this error:

```
[3945390:3945504:0930/184020.087358:FATAL:cache_storage.mojom.cc(3287)] Check failed: !connected. CacheStorage::MatchCallback was destroyed without first either being run or its corresponding binding being closed. It is an error to drop response callbacks which still correspond to an open interface pipe.

```

I did change the patch slightly to also comment out the `}` at the bottom of the if block.

I also tried it without the patch once and did not reproduce the UAF. Are there any other changes I should make to be able to reproduce this?

### m....@gmail.com (2024-10-01)

I only have a Windows machine and no Linux machine on hand to test with.

I can provide a reproduction video.

Please check if there are any differences in the steps."

### pe...@google.com (2024-10-01)

Thank you for providing more feedback. Adding the requester to the CC list.

### pe...@google.com (2024-10-01)

The NextAction date has arrived: 2024-10-01
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### th...@chromium.org (2024-10-01)

Thanks for that video. Unfortunately I am still not able to reproduce this (I am getting the same error I mentioned in [#comment4](https://issues.chromium.org/issues/370069678#comment4)). My initial repro attempts were from a Sept 27 build, and the attempts just now were from an Oct 1 build.

I will triage this speculatively based on the ASAN track trace and the bisect CL. Found In 131 from the bisect CL, and Critical severity from the stack trace (UAF in the browser process). Assigning to estade@ from the bisect CL.

estade@: Could you PTAL at this issue? Please also comment if the patch does not seem like a valid way to make the issue be easier to reproduce.

### es...@chromium.org (2024-10-01)

> Please also comment if the patch does not seem like a valid way to make the issue be easier to reproduce.

That patch is definitely not valid, but the stack trace does look plausible. [Fix](https://chromium-review.googlesource.com/c/chromium/src/+/5902125)

### pe...@google.com (2024-10-02)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-10-02)

Setting Priority to P0 to match Severity s0. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ap...@google.com (2024-10-02)

Project: chromium/src  

Branch: main  

Author: Evan Stade <[estade@chromium.org](mailto:estade@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5902125>

CacheStorage: fix UAF.

---


Expand for full commit details
```
CacheStorage: fix UAF.

Bug: 370069678
Change-Id: I4c2ddc242131ef07daf6f848c2103e8b66181f6f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5902125
Reviewed-by: Mike Wasserman <msw@chromium.org>
Reviewed-by: Ayu Ishii <ayui@chromium.org>
Commit-Queue: Evan Stade <estade@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1363358}

```

---

Files:

- M `content/browser/cache_storage/cache_storage_scheduler.cc`
- M `content/browser/cache_storage/cache_storage_scheduler_unittest.cc`

---

Hash: 338585c1031a32e1002a982371bb000ec297adf1  

Date:  Wed Oct 02 22:50:31 2024


---

### m....@gmail.com (2024-10-03)

re #c08
It seems you triggered a DCHECK, but DCHECK is not effective in the release version. So can you try disabling the DCHECK(dcheck\_always\_on = false) check and see if it works?

### th...@chromium.org (2024-10-03)

Thanks! I think that is a reasonable change to the gn args. With that change, I am able to reproduce this. (Though it is with the patch that [#comment9](https://issues.chromium.org/issues/370069678#comment9) says is invalid.)

### th...@chromium.org (2024-10-03)

estade@: if [#comment12](https://issues.chromium.org/issues/370069678#comment12) fixes this bug, could you please close out this issue as Fixed?

### es...@chromium.org (2024-10-03)

Yea, the bug should be fixed. However I still don't think we know of a reproduction. `DCHECK` is not the same as a crash. Even when `DCHECK` is treated as `CHECK`, it's not a vulnerability (i.e. it is a "safe" way to crash).

### th...@chromium.org (2024-10-03)

Right, though the gn args change was to make DCHECK *not* crash. Let me rephrase my [#comment14](https://issues.chromium.org/issues/370069678#comment14):

I think that adding `dcheck_always_on = false` is a reasonable change to the gn args. With that change, I am able to reproduce the heap-use-after-free. (Though it still requires the patch that [#comment9](https://issues.chromium.org/issues/370069678#comment9) says is invalid.)

### es...@chromium.org (2024-10-03)

Got it. Yea, not DCHECKing is reasonable.

The fuzzer link doesn't work for me. Do we know what that fuzzer is doing? Is there a way to get access for the link?

### th...@chromium.org (2024-10-03)

I am not sure of a way to make the fuzzer link work for you if you're not already able to access it. I will share the contents directly with you off-bug.

### m....@gmail.com (2024-10-04)

re #18 Access to the fuzzer link can be authorized through the security team, but it's no longer important now since I have already provided the minimal POC in [#comment3](https://issues.chromium.org/issues/370069678#comment3).

### sp...@google.com (2024-10-09)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $6000.00 for this report.

Rationale for this decision:
$5,000 for report of moderately-mildly mitigated memory corruption in a non-sandboxed process + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-10-09)

Congratulations! This wasn't able to be reproduced in a way that demonstrate reliable or remote exploitability and appear to be fairly mitigated. As such, we have awarded this issue accordingly. If you are able to demonstrate this in a more reliable way that demonstrates non-mitigated remote exploitability we'd be happy to revisit this issue. Thanks for your effort and reporting this issue to us.

### m....@gmail.com (2024-10-12)

re #22
This provided POC can reliably reproduce the SBX issue without using a patch.

chrome --user-data-dir=test --allow-file-access-from-files --no-default-browser-check --no-first-run poc.html poc.html poc.html poc.html poc.html poc.html poc.html poc.html poc.html

### m....@gmail.com (2024-10-12)

This is a reproduction video on version gs://chromium-browser-asan/win32-release\_x64/asan-win32-release\_x64-1361692.zip

### m....@gmail.com (2024-10-14)

re #c22 More concise and minimal POC, can be reliably reproduced stability in local testing.
chrome --user-data-dir=test --allow-file-access-from-files --no-default-browser-check --no-first-run min.html

### th...@chromium.org (2024-10-14)

Thanks for providing that. With that POC (#comment25), I can reliably reproduce the UAF using ASAN release build: linux-release/asan-linux-release-1360763 (HEAD on Sept 26). It's pretty immediate. Side note since I was wondering, I do not need the args `--allow-file-access-from-files --no-default-browser-check --no-first-run` to reproduce this.

### am...@chromium.org (2024-10-14)

Thank you, OP, for supplying the new POC and thank you, thefrog@ for verifying the repro so quickly. If you wouldn't mind dropping the stack trace from this repro on bug, that would be appreciated.

OP, there's no VRP panel this week due to the team being split attending internal/external events, so we'll review this at a future VRP panel session.

### th...@chromium.org (2024-10-15)

thefrog@thefrog-cloudtop:~/Downloads/linux-release_asan-linux-release-1360763$ ./chrome --user-data-dir=test-10-14-10-31am ~/security-sheriffing/poc-370069678/min.html 2>&1 | ~/cr/c3/src/tools/valgrind/asan/asan_symbolize.py
MESA: error: ZINK: failed to choose pdev
glx: failed to create drisw screen
[2387473:2387473:1014/143211.487742:ERROR:viz_main_impl.cc(181)] Exiting GPU process due to errors during initialization
[2387434:2387434:1014/143212.507076:ERROR:secret_portal_key_provider.cc(200)] Keyring unlock cancelled: 2
[2387434:2387434:1014/143212.546995:ERROR:object_proxy.cc(576)] Failed to call method: org.freedesktop.ScreenSaver.GetActive: object_path= /org/freedesktop/ScreenSaver: org.freedesktop.DBus.Error.NotSupported: This method is not implemented
MESA: error: ZINK: failed to choose pdev
glx: failed to create drisw screen
[2387434:2387434:1014/143212.718311:ERROR:object_proxy.cc(576)] Failed to call method: org.gnome.ScreenSaver.GetActive: object_path= /org/gnome/ScreenSaver: org.freedesktop.DBus.Error.ServiceUnknown: The name org.gnome.Shell.ScreenShield was not provided by any .service files
[2387587:2387587:1014/143212.856794:ERROR:viz_main_impl.cc(181)] Exiting GPU process due to errors during initialization
[2387565:7:1014/143213.164971:ERROR:command_buffer_proxy_impl.cc(131)] ContextResult::kTransientFailure: Failed to send GpuControl.CreateCommandBuffer.
=================================================================
==2387434==ERROR: AddressSanitizer: heap-use-after-free on address 0x7bd4ba6d0560 at pc 0x55b63ae2b6fc bp 0x7b24b07fcf90 sp 0x7b24b07fcf88
READ of size 8 at 0x7bd4ba6d0560 thread T5 (ThreadPoolForeg)
==2387434==WARNING: invalid path to external symbolizer!
==2387434==WARNING: Failed to use and restart external symbolizer!
    #0 0x55b63ae2b6fb in empty ./../../third_party/libc++/src/include/vector:654:18
    #1 0x55b63ae2b6fb in content::CacheStorageScheduler::MaybeRunOperation() ./../../content/browser/cache_storage/cache_storage_scheduler.cc:145:31
    #2 0x55b63ae2bb66 in content::CacheStorageScheduler::CompleteOperationAndRunNext(long) ./../../content/browser/cache_storage/cache_storage_scheduler.cc:116:3
    #3 0x55b63adccc58 in void content::CacheStorageScheduler::RunNextContinuation<>(long, base::OnceCallback<void ()>) ./../../content/browser/cache_storage/cache_storage_scheduler.h:102:7
    #4 0x55b63adcd02d in Invoke<void (content::CacheStorageScheduler::*)(long, base::OnceCallback<void ()>), const base::WeakPtr<content::CacheStorageScheduler> &, long, base::OnceCallback<void ()> > ./../../base/functional/bind_internal.h:738:12
    #5 0x55b63adcd02d in MakeItSo<void (content::CacheStorageScheduler::*)(long, base::OnceCallback<void ()>), std::__Cr::tuple<base::WeakPtr<content::CacheStorageScheduler>, long, base::OnceCallback<void ()> > > ./../../base/functional/bind_internal.h:954:5
    #6 0x55b63adcd02d in void base::internal::Invoker<base::internal::FunctorTraits<void (content::CacheStorageScheduler::*&&)(long, base::OnceCallback<void ()>), base::WeakPtr<content::CacheStorageScheduler>&&, long&&, base::OnceCallback<void ()>&&>, base::internal::BindState<true, true, false, void (content::CacheStorageScheduler::*)(long, base::OnceCallback<void ()>), base::WeakPtr<content::CacheStorageScheduler>, long, base::OnceCallback<void ()>>, void ()>::RunImpl<void (content::CacheStorageScheduler::*)(long, base::OnceCallback<void ()>), std::__Cr::tuple<base::WeakPtr<content::CacheStorageScheduler>, long, base::OnceCallback<void ()>>, 0ul, 1ul, 2ul>(void (content::CacheStorageScheduler::*&&)(long, base::OnceCallback<void ()>), std::__Cr::tuple<base::WeakPtr<content::CacheStorageScheduler>, long, base::OnceCallback<void ()>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul>) ./../../base/functional/bind_internal.h:1067:14
    #7 0x55b63add3e14 in Run ./../../base/functional/callback.h:156:12
    #8 0x55b63add3e14 in base::internal::OnceCallbackHolder<>::Run() ./../../base/functional/callback_helpers.h:67:26
    #9 0x55b63add4164 in Invoke<void (base::internal::OnceCallbackHolder<>::*)(), const std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<> > > &> ./../../base/functional/bind_internal.h:738:12
    #10 0x55b63add4164 in MakeItSo<void (base::internal::OnceCallbackHolder<>::*const &)(), const std::__Cr::tuple<std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<> > > > &> ./../../base/functional/bind_internal.h:930:12
    #11 0x55b63add4164 in RunImpl<void (base::internal::OnceCallbackHolder<>::*const &)(), const std::__Cr::tuple<std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<> > > > &, 0UL> ./../../base/functional/bind_internal.h:1067:14
    #12 0x55b63add4164 in base::internal::Invoker<base::internal::FunctorTraits<void (base::internal::OnceCallbackHolder<>::* const&)(), std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<>>> const&>, base::internal::BindState<true, true, false, void (base::internal::OnceCallbackHolder<>::*)(), std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<>>>>, void ()>::Run(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:987:12
    #13 0x55b63ada96e6 in Run ./../../base/functional/callback.h:156:12
    #14 0x55b63ada96e6 in content::CacheStorageCache::InitGotCacheSizeAndPadding(base::OnceCallback<void ()>, blink::mojom::CacheStorageError, long, long) ./../../content/browser/cache_storage/cache_storage_cache.cc:2634:23
    #15 0x55b63ada85a4 in content::CacheStorageCache::InitGotCacheSize(base::OnceCallback<void ()>, blink::mojom::CacheStorageError, long) ./../../content/browser/cache_storage/cache_storage_cache.cc:0:0
    #16 0x55b63adcaae3 in Invoke<void (content::CacheStorageCache::*)(base::OnceCallback<void ()>, blink::mojom::CacheStorageError, long), const base::WeakPtr<content::CacheStorageCache> &, base::OnceCallback<void ()>, blink::mojom::CacheStorageError, long> ./../../base/functional/bind_internal.h:738:12
    #17 0x55b63adcaae3 in MakeItSo<void (content::CacheStorageCache::*)(base::OnceCallback<void ()>, blink::mojom::CacheStorageError, long), std::__Cr::tuple<base::WeakPtr<content::CacheStorageCache>, base::OnceCallback<void ()>, blink::mojom::CacheStorageError>, long> ./../../base/functional/bind_internal.h:954:5
    #18 0x55b63adcaae3 in void base::internal::Invoker<base::internal::FunctorTraits<void (content::CacheStorageCache::*&&)(base::OnceCallback<void ()>, blink::mojom::CacheStorageError, long), base::WeakPtr<content::CacheStorageCache>&&, base::OnceCallback<void ()>&&, blink::mojom::CacheStorageError&&>, base::internal::BindState<true, true, false, void (content::CacheStorageCache::*)(base::OnceCallback<void ()>, blink::mojom::CacheStorageError, long), base::WeakPtr<content::CacheStorageCache>, base::OnceCallback<void ()>, blink::mojom::CacheStorageError>, void (long)>::RunImpl<void (content::CacheStorageCache::*)(base::OnceCallback<void ()>, blink::mojom::CacheStorageError, long), std::__Cr::tuple<base::WeakPtr<content::CacheStorageCache>, base::OnceCallback<void ()>, blink::mojom::CacheStorageError>, 0ul, 1ul, 2ul>(void (content::CacheStorageCache::*&&)(base::OnceCallback<void ()>, blink::mojom::CacheStorageError, long), std::__Cr::tuple<base::WeakPtr<content::CacheStorageCache>, base::OnceCallback<void ()>, blink::mojom::CacheStorageError>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul>, long&&) ./../../base/functional/bind_internal.h:1067:14
    #19 0x55b63adca835 in base::internal::Invoker<base::internal::FunctorTraits<void (content::CacheStorageCache::*&&)(base::OnceCallback<void ()>, blink::mojom::CacheStorageError, long), base::WeakPtr<content::CacheStorageCache>&&, base::OnceCallback<void ()>&&, blink::mojom::CacheStorageError&&>, base::internal::BindState<true, true, false, void (content::CacheStorageCache::*)(base::OnceCallback<void ()>, blink::mojom::CacheStorageError, long), base::WeakPtr<content::CacheStorageCache>, base::OnceCallback<void ()>, blink::mojom::CacheStorageError>, void (long)>::RunOnce(base::internal::BindStateBase*, long) ./../../base/functional/bind_internal.h:980:12
    #20 0x55b645486dee in Run ./../../base/functional/callback.h:156:12
    #21 0x55b645486dee in disk_cache::SimpleBackendImpl::IndexReadyForSizeCalculation(base::OnceCallback<void (long)>, int) ./../../net/disk_cache/simple/simple_backend_impl.cc:701:23
    #22 0x55b64548deb7 in Invoke<void (disk_cache::SimpleBackendImpl::*)(base::OnceCallback<void (long)>, int), const base::WeakPtr<disk_cache::SimpleBackendImpl> &, base::OnceCallback<void (long)>, int> ./../../base/functional/bind_internal.h:738:12
    #23 0x55b64548deb7 in MakeItSo<void (disk_cache::SimpleBackendImpl::*)(base::OnceCallback<void (long)>, int), std::__Cr::tuple<base::WeakPtr<disk_cache::SimpleBackendImpl>, base::OnceCallback<void (long)> >, int> ./../../base/functional/bind_internal.h:954:5
    #24 0x55b64548deb7 in void base::internal::Invoker<base::internal::FunctorTraits<void (disk_cache::SimpleBackendImpl::*&&)(base::OnceCallback<void (long)>, int), base::WeakPtr<disk_cache::SimpleBackendImpl>&&, base::OnceCallback<void (long)>&&>, base::internal::BindState<true, true, false, void (disk_cache::SimpleBackendImpl::*)(base::OnceCallback<void (long)>, int), base::WeakPtr<disk_cache::SimpleBackendImpl>, base::OnceCallback<void (long)>>, void (int)>::RunImpl<void (disk_cache::SimpleBackendImpl::*)(base::OnceCallback<void (long)>, int), std::__Cr::tuple<base::WeakPtr<disk_cache::SimpleBackendImpl>, base::OnceCallback<void (long)>>, 0ul, 1ul>(void (disk_cache::SimpleBackendImpl::*&&)(base::OnceCallback<void (long)>, int), std::__Cr::tuple<base::WeakPtr<disk_cache::SimpleBackendImpl>, base::OnceCallback<void (long)>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>, int&&) ./../../base/functional/bind_internal.h:1067:14
    #25 0x55b64548dc24 in base::internal::Invoker<base::internal::FunctorTraits<void (disk_cache::SimpleBackendImpl::*&&)(base::OnceCallback<void (long)>, int), base::WeakPtr<disk_cache::SimpleBackendImpl>&&, base::OnceCallback<void (long)>&&>, base::internal::BindState<true, true, false, void (disk_cache::SimpleBackendImpl::*)(base::OnceCallback<void (long)>, int), base::WeakPtr<disk_cache::SimpleBackendImpl>, base::OnceCallback<void (long)>>, void (int)>::RunOnce(base::internal::BindStateBase*, int) ./../../base/functional/bind_internal.h:980:12
    #26 0x55b63ad0cdce in Run ./../../base/functional/callback.h:156:12
    #27 0x55b63ad0cdce in Invoke<base::OnceCallback<void (int)>, net::Error> ./../../base/functional/bind_internal.h:813:49
    #28 0x55b63ad0cdce in MakeItSo<base::OnceCallback<void (int)>, std::__Cr::tuple<net::Error> > ./../../base/functional/bind_internal.h:930:12
    #29 0x55b63ad0cdce in RunImpl<base::OnceCallback<void (int)>, std::__Cr::tuple<net::Error>, 0UL> ./../../base/functional/bind_internal.h:1067:14
    #30 0x55b63ad0cdce in base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (int)>&&, net::Error&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (int)>, net::Error>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:980:12
    #31 0x55b6447a07c4 in Run ./../../base/functional/callback.h:156:12
    #32 0x55b6447a07c4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:202:34
    #33 0x55b64482a3ab in RunTask<(lambda at ../../base/task/thread_pool/task_tracker.cc:678:35)> ./../../base/task/common/task_annotator.h:90:5
    #34 0x55b64482a3ab in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) ./../../base/task/thread_pool/task_tracker.cc:677:19
    #35 0x55b64482a5fc in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) ./../../base/task/thread_pool/task_tracker.cc:662:3
    #36 0x55b644829804 in RunTaskWithShutdownBehavior ./../../base/task/thread_pool/task_tracker.cc:692:7
    #37 0x55b644829804 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) ./../../base/task/thread_pool/task_tracker.cc:520:5
    #38 0x55b6448286e4 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) ./../../base/task/thread_pool/task_tracker.cc:415:5
    #39 0x55b644861123 in base::internal::WorkerThread::RunWorker() ./../../base/task/thread_pool/worker_thread.cc:493:36
    #40 0x55b644860257 in base::internal::WorkerThread::RunPooledWorker() ./../../base/task/thread_pool/worker_thread.cc:379:3
    #41 0x55b64485fd3e in base::internal::WorkerThread::ThreadMain() ./../../base/task/thread_pool/worker_thread.cc:359:7
    #42 0x55b6448c9d29 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:101:13
    #43 0x55b630a83416 in asan_thread_start(void*) _asan_rtl_:28

0x7bd4ba6d0560 is located 16 bytes inside of 112-byte region [0x7bd4ba6d0550,0x7bd4ba6d05c0)
freed by thread T5 (ThreadPoolForeg) here:
    #0 0x55b630abd57d in operator delete(void*) _asan_rtl_:3
    #1 0x55b63ae29d5f in content::CacheStorageScheduler::~CacheStorageScheduler() ./../../content/browser/cache_storage/cache_storage_scheduler.cc:69:49
    #2 0x55b63ad8983f in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:69:5
    #3 0x55b63ad8983f in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:285:7
    #4 0x55b63ad8983f in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:254:71
    #5 0x55b63ad8983f in content::CacheStorageCache::~CacheStorageCache() ./../../content/browser/cache_storage/cache_storage_cache.cc:1044:39
    #6 0x55b63ad89df3 in content::CacheStorageCache::~CacheStorageCache() ./../../content/browser/cache_storage/cache_storage_cache.cc:1044:39
    #7 0x55b63ad4a9a0 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:69:5
    #8 0x55b63ad4a9a0 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:285:7
    #9 0x55b63ad4a9a0 in ReleaseUnreferencedCaches ./../../content/browser/cache_storage/cache_storage.cc:932:20
    #10 0x55b63ad4a9a0 in content::CacheStorage::DropHandleRef() ./../../content/browser/cache_storage/cache_storage.cc:652:5
    #11 0x55b63ad7d693 in content::CacheStorageRef<content::CacheStorage>::~CacheStorageRef() ./../../content/browser/cache_storage/cache_storage_ref.h:45:16
    #12 0x55b63ad7d961 in content::CacheStorageCache::DropHandleRef() ./../../content/browser/cache_storage/cache_storage_cache.cc:676:3
    #13 0x55b63ad56da3 in content::CacheStorageRef<content::CacheStorageCache>::~CacheStorageRef() ./../../content/browser/cache_storage/cache_storage_ref.h:45:16
    #14 0x55b63adce3b0 in void base::internal::DecayedFunctorTraits<void (content::CacheStorageCache::*)(content::CacheStorageRef<content::CacheStorageCache>, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>, blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>), base::WeakPtr<content::CacheStorageCache>&&, content::CacheStorageRef<content::CacheStorageCache>&&, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>&&>::Invoke<void (content::CacheStorageCache::*)(content::CacheStorageRef<content::CacheStorageCache>, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>, blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>), base::WeakPtr<content::CacheStorageCache> const&, content::CacheStorageRef<content::CacheStorageCache>, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>, blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>>(void (content::CacheStorageCache::*)(content::CacheStorageRef<content::CacheStorageCache>, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>, blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>), base::WeakPtr<content::CacheStorageCache> const&, content::CacheStorageRef<content::CacheStorageCache>&&, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>&&, blink::mojom::CacheStorageError&&, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>&&) ./../../base/functional/bind_internal.h:738:5
    #15 0x55b63adce055 in MakeItSo<void (content::CacheStorageCache::*)(content::CacheStorageRef<content::CacheStorageCache>, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse> > >)>, blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse> > >), std::__Cr::tuple<base::WeakPtr<content::CacheStorageCache>, content::CacheStorageRef<content::CacheStorageCache>, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse> > >)> >, blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse> > > > ./../../base/functional/bind_internal.h:954:5
    #16 0x55b63adce055 in RunImpl<void (content::CacheStorageCache::*)(content::CacheStorageRef<content::CacheStorageCache>, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse> > >)>, blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse> > >), std::__Cr::tuple<base::WeakPtr<content::CacheStorageCache>, content::CacheStorageRef<content::CacheStorageCache>, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse> > >)> >, 0UL, 1UL, 2UL> ./../../base/functional/bind_internal.h:1067:14
    #17 0x55b63adce055 in base::internal::Invoker<base::internal::FunctorTraits<void (content::CacheStorageCache::*&&)(content::CacheStorageRef<content::CacheStorageCache>, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>, blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>), base::WeakPtr<content::CacheStorageCache>&&, content::CacheStorageRef<content::CacheStorageCache>&&, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>&&>, base::internal::BindState<true, true, false, void (content::CacheStorageCache::*)(content::CacheStorageRef<content::CacheStorageCache>, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>, blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>), base::WeakPtr<content::CacheStorageCache>, content::CacheStorageRef<content::CacheStorageCache>, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>>, void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>::RunOnce(base::internal::BindStateBase*, blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>&&) ./../../base/functional/bind_internal.h:980:12
    #18 0x55b63ad9498b in Run ./../../base/functional/callback.h:156:12
    #19 0x55b63ad9498b in content::CacheStorageCache::MatchAllDidQueryCache(base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>, long, blink::mojom::CacheStorageError, std::__Cr::unique_ptr<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>, std::__Cr::default_delete<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>>>) ./../../content/browser/cache_storage/cache_storage_cache.cc:1523:23
    #20 0x55b63adbe429 in Invoke<void (content::CacheStorageCache::*)(base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse> > >)>, long, blink::mojom::CacheStorageError, std::__Cr::unique_ptr<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult> >, std::__Cr::default_delete<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult> > > >), const base::WeakPtr<content::CacheStorageCache> &, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse> > >)>, long, blink::mojom::CacheStorageError, std::__Cr::unique_ptr<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult> >, std::__Cr::default_delete<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult> > > > > ./../../base/functional/bind_internal.h:738:12
    #21 0x55b63adbe429 in MakeItSo<void (content::CacheStorageCache::*)(base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse> > >)>, long, blink::mojom::CacheStorageError, std::__Cr::unique_ptr<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult> >, std::__Cr::default_delete<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult> > > >), std::__Cr::tuple<base::WeakPtr<content::CacheStorageCache>, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse> > >)>, long>, blink::mojom::CacheStorageError, std::__Cr::unique_ptr<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult> >, std::__Cr::default_delete<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult> > > > > ./../../base/functional/bind_internal.h:954:5
    #22 0x55b63adbe429 in RunImpl<void (content::CacheStorageCache::*)(base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse> > >)>, long, blink::mojom::CacheStorageError, std::__Cr::unique_ptr<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult> >, std::__Cr::default_delete<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult> > > >), std::__Cr::tuple<base::WeakPtr<content::CacheStorageCache>, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse> > >)>, long>, 0UL, 1UL, 2UL> ./../../base/functional/bind_internal.h:1067:14
    #23 0x55b63adbe429 in base::internal::Invoker<base::internal::FunctorTraits<void (content::CacheStorageCache::*&&)(base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>, long, blink::mojom::CacheStorageError, std::__Cr::unique_ptr<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>, std::__Cr::default_delete<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>>>), base::WeakPtr<content::CacheStorageCache>&&, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>&&, long&&>, base::internal::BindState<true, true, false, void (content::CacheStorageCache::*)(base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>, long, blink::mojom::CacheStorageError, std::__Cr::unique_ptr<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>, std::__Cr::default_delete<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>>>), base::WeakPtr<content::CacheStorageCache>, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>, long>, void (blink::mojom::CacheStorageError, std::__Cr::unique_ptr<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>, std::__Cr::default_delete<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>>>)>::RunOnce(base::internal::BindStateBase*, blink::mojom::CacheStorageError, std::__Cr::unique_ptr<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>, std::__Cr::default_delete<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>>>&&) ./../../base/functional/bind_internal.h:980:12
    #24 0x55b63ad8bb95 in base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::unique_ptr<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>, std::__Cr::default_delete<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>>>)>::Run(blink::mojom::CacheStorageError, std::__Cr::unique_ptr<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>, std::__Cr::default_delete<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>>>) && ./../../base/functional/callback.h:156:12
    #25 0x55b63ad8c6df in content::CacheStorageCache::QueryCacheDidOpenFastPath(std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext>>, disk_cache::EntryResult) ./../../content/browser/cache_storage/cache_storage_cache.cc:1150:10
    #26 0x55b63adb3690 in void base::internal::DecayedFunctorTraits<void (content::CacheStorageCache::*)(std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext>>, disk_cache::EntryResult), base::WeakPtr<content::CacheStorageCache>&&, std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext>>&&>::Invoke<void (content::CacheStorageCache::*)(std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext>>, disk_cache::EntryResult), base::WeakPtr<content::CacheStorageCache> const&, std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext>>, disk_cache::EntryResult>(void (content::CacheStorageCache::*)(std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext>>, disk_cache::EntryResult), base::WeakPtr<content::CacheStorageCache> const&, std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext>>&&, disk_cache::EntryResult&&) ./../../base/functional/bind_internal.h:738:12
    #27 0x55b63adb345b in MakeItSo<void (content::CacheStorageCache::*)(std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext> >, disk_cache::EntryResult), std::__Cr::tuple<base::WeakPtr<content::CacheStorageCache>, std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext> > >, disk_cache::EntryResult> ./../../base/functional/bind_internal.h:954:5
    #28 0x55b63adb345b in RunImpl<void (content::CacheStorageCache::*)(std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext> >, disk_cache::EntryResult), std::__Cr::tuple<base::WeakPtr<content::CacheStorageCache>, std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext> > >, 0UL, 1UL> ./../../base/functional/bind_internal.h:1067:14
    #29 0x55b63adb345b in base::internal::Invoker<base::internal::FunctorTraits<void (content::CacheStorageCache::*&&)(std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext>>, disk_cache::EntryResult), base::WeakPtr<content::CacheStorageCache>&&, std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext>>&&>, base::internal::BindState<true, true, false, void (content::CacheStorageCache::*)(std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext>>, disk_cache::EntryResult), base::WeakPtr<content::CacheStorageCache>, std::__Cr::unique_ptr<content::CacheStorageCache::QueryCacheContext, std::__Cr::default_delete<content::CacheStorageCache::QueryCacheContext>>>, void (disk_cache::EntryResult)>::RunOnce(base::internal::BindStateBase*, disk_cache::EntryResult&&) ./../../base/functional/bind_internal.h:980:12
    #30 0x55b63adcd6ba in Run ./../../base/functional/callback.h:156:12
    #31 0x55b63adcd6ba in base::internal::OnceCallbackHolder<disk_cache::EntryResult>::Run(disk_cache::EntryResult) ./../../base/functional/callback_helpers.h:67:26
    #32 0x55b63adcda1c in Invoke<void (base::internal::OnceCallbackHolder<disk_cache::EntryResult>::*)(disk_cache::EntryResult), const std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<disk_cache::EntryResult>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<disk_cache::EntryResult> > > &, disk_cache::EntryResult> ./../../base/functional/bind_internal.h:738:12
    #33 0x55b63adcda1c in MakeItSo<void (base::internal::OnceCallbackHolder<disk_cache::EntryResult>::*const &)(disk_cache::EntryResult), const std::__Cr::tuple<std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<disk_cache::EntryResult>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<disk_cache::EntryResult> > > > &, disk_cache::EntryResult> ./../../base/functional/bind_internal.h:930:12
    #34 0x55b63adcda1c in RunImpl<void (base::internal::OnceCallbackHolder<disk_cache::EntryResult>::*const &)(disk_cache::EntryResult), const std::__Cr::tuple<std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<disk_cache::EntryResult>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<disk_cache::EntryResult> > > > &, 0UL> ./../../base/functional/bind_internal.h:1067:14
    #35 0x55b63adcda1c in base::internal::Invoker<base::internal::FunctorTraits<void (base::internal::OnceCallbackHolder<disk_cache::EntryResult>::* const&)(disk_cache::EntryResult), std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<disk_cache::EntryResult>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<disk_cache::EntryResult>>> const&>, base::internal::BindState<true, true, false, void (base::internal::OnceCallbackHolder<disk_cache::EntryResult>::*)(disk_cache::EntryResult), std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<disk_cache::EntryResult>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<disk_cache::EntryResult>>>>, void (disk_cache::EntryResult)>::Run(base::internal::BindStateBase*, disk_cache::EntryResult&&) ./../../base/functional/bind_internal.h:987:12
    #36 0x55b63ad8b630 in Run ./../../base/functional/callback.h:156:12
    #37 0x55b63ad8b630 in content::CacheStorageCache::QueryCache(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, int, content::CacheStorageSchedulerPriority, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::unique_ptr<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>, std::__Cr::default_delete<std::__Cr::vector<content::CacheStorageCache::QueryCacheResult, std::__Cr::allocator<content::CacheStorageCache::QueryCacheResult>>>>)>) ./../../content/browser/cache_storage/cache_storage_cache.cc:1136:40
    #38 0x55b63ad7f6cf in content::CacheStorageCache::MatchAllImpl(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, long, content::CacheStorageSchedulerPriority, base::OnceCallback<void (blink::mojom::CacheStorageError, std::__Cr::vector<mojo::StructPtr<blink::mojom::FetchAPIResponse>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::FetchAPIResponse>>>)>) ./../../content/browser/cache_storage/cache_storage_cache.cc:1493:3
    #39 0x55b63ad7e6e6 in content::CacheStorageCache::MatchImpl(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, long, content::CacheStorageSchedulerPriority, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>) ./../../content/browser/cache_storage/cache_storage_cache.cc:1447:3
    #40 0x55b63adaa4c7 in void base::internal::DecayedFunctorTraits<void (content::CacheStorageCache::*)(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, long, content::CacheStorageSchedulerPriority, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>), base::WeakPtr<content::CacheStorageCache>&&, mojo::StructPtr<blink::mojom::FetchAPIRequest>&&, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>&&, long&&, content::CacheStorageSchedulerPriority&&, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>&&>::Invoke<void (content::CacheStorageCache::*)(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, long, content::CacheStorageSchedulerPriority, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>), base::WeakPtr<content::CacheStorageCache> const&, mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, long, content::CacheStorageSchedulerPriority, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>>(void (content::CacheStorageCache::*)(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, long, content::CacheStorageSchedulerPriority, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>), base::WeakPtr<content::CacheStorageCache> const&, mojo::StructPtr<blink::mojom::FetchAPIRequest>&&, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>&&, long&&, content::CacheStorageSchedulerPriority&&, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>&&) ./../../base/functional/bind_internal.h:738:12
    #41 0x55b63adaa140 in MakeItSo<void (content::CacheStorageCache::*)(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, long, content::CacheStorageSchedulerPriority, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>), std::__Cr::tuple<base::WeakPtr<content::CacheStorageCache>, mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, long, content::CacheStorageSchedulerPriority, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)> > > ./../../base/functional/bind_internal.h:954:5
    #42 0x55b63adaa140 in RunImpl<void (content::CacheStorageCache::*)(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, long, content::CacheStorageSchedulerPriority, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>), std::__Cr::tuple<base::WeakPtr<content::CacheStorageCache>, mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, long, content::CacheStorageSchedulerPriority, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)> >, 0UL, 1UL, 2UL, 3UL, 4UL, 5UL> ./../../base/functional/bind_internal.h:1067:14
    #43 0x55b63adaa140 in base::internal::Invoker<base::internal::FunctorTraits<void (content::CacheStorageCache::*&&)(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, long, content::CacheStorageSchedulerPriority, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>), base::WeakPtr<content::CacheStorageCache>&&, mojo::StructPtr<blink::mojom::FetchAPIRequest>&&, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>&&, long&&, content::CacheStorageSchedulerPriority&&, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>&&>, base::internal::BindState<true, true, false, void (content::CacheStorageCache::*)(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, long, content::CacheStorageSchedulerPriority, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>), base::WeakPtr<content::CacheStorageCache>, mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, long, content::CacheStorageSchedulerPriority, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:980:12
    #44 0x55b63ae28396 in Run ./../../base/functional/callback.h:156:12
    #45 0x55b63ae28396 in content::CacheStorageOperation::Run() ./../../content/browser/cache_storage/cache_storage_operation.cc:37:23
    #46 0x55b63ae2d14d in Invoke<void (content::CacheStorageOperation::*)(), const base::WeakPtr<content::CacheStorageOperation> &> ./../../base/functional/bind_internal.h:738:12
    #47 0x55b63ae2d14d in MakeItSo<void (content::CacheStorageOperation::*)(), std::__Cr::tuple<base::WeakPtr<content::CacheStorageOperation> > > ./../../base/functional/bind_internal.h:954:5
    #48 0x55b63ae2d14d in void base::internal::Invoker<base::internal::FunctorTraits<void (content::CacheStorageOperation::*&&)(), base::WeakPtr<content::CacheStorageOperation>&&>, base::internal::BindState<true, true, false, void (content::CacheStorageOperation::*)(), base::WeakPtr<content::CacheStorageOperation>>, void ()>::RunImpl<void (content::CacheStorageOperation::*)(), std::__Cr::tuple<base::WeakPtr<content::CacheStorageOperation>>, 0ul>(void (content::CacheStorageOperation::*&&)(), std::__Cr::tuple<base::WeakPtr<content::CacheStorageOperation>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) ./../../base/functional/bind_internal.h:1067:14
    #49 0x55b63ae2bde7 in Run ./../../base/functional/callback.h:156:12
    #50 0x55b63ae2bde7 in content::CacheStorageScheduler::DispatchOperationTask(base::OnceCallback<void ()>) ./../../content/browser/cache_storage/cache_storage_scheduler.cc:131:19
    #51 0x55b63ae2af83 in content::CacheStorageScheduler::MaybeRunOperation() ./../../content/browser/cache_storage/cache_storage_scheduler.cc:184:5
    #52 0x55b63ae2bb66 in content::CacheStorageScheduler::CompleteOperationAndRunNext(long) ./../../content/browser/cache_storage/cache_storage_scheduler.cc:116:3
    #53 0x55b63adccc58 in void content::CacheStorageScheduler::RunNextContinuation<>(long, base::OnceCallback<void ()>) ./../../content/browser/cache_storage/cache_storage_scheduler.h:102:7
    #54 0x55b63adcd02d in Invoke<void (content::CacheStorageScheduler::*)(long, base::OnceCallback<void ()>), const base::WeakPtr<content::CacheStorageScheduler> &, long, base::OnceCallback<void ()> > ./../../base/functional/bind_internal.h:738:12
    #55 0x55b63adcd02d in MakeItSo<void (content::CacheStorageScheduler::*)(long, base::OnceCallback<void ()>), std::__Cr::tuple<base::WeakPtr<content::CacheStorageScheduler>, long, base::OnceCallback<void ()> > > ./../../base/functional/bind_internal.h:954:5
    #56 0x55b63adcd02d in void base::internal::Invoker<base::internal::FunctorTraits<void (content::CacheStorageScheduler::*&&)(long, base::OnceCallback<void ()>), base::WeakPtr<content::CacheStorageScheduler>&&, long&&, base::OnceCallback<void ()>&&>, base::internal::BindState<true, true, false, void (content::CacheStorageScheduler::*)(long, base::OnceCallback<void ()>), base::WeakPtr<content::CacheStorageScheduler>, long, base::OnceCallback<void ()>>, void ()>::RunImpl<void (content::CacheStorageScheduler::*)(long, base::OnceCallback<void ()>), std::__Cr::tuple<base::WeakPtr<content::CacheStorageScheduler>, long, base::OnceCallback<void ()>>, 0ul, 1ul, 2ul>(void (content::CacheStorageScheduler::*&&)(long, base::OnceCallback<void ()>), std::__Cr::tuple<base::WeakPtr<content::CacheStorageScheduler>, long, base::OnceCallback<void ()>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul>) ./../../base/functional/bind_internal.h:1067:14

previously allocated by thread T5 (ThreadPoolForeg) here:
    #0 0x55b630abcd1d in operator new(unsigned long) _asan_rtl_:3
    #1 0x55b63ad8a0fd in content::CacheStorageCache::CacheStorageCache(storage::BucketLocator const&, storage::mojom::CacheStorageOwner, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, base::FilePath const&, content::CacheStorage*, scoped_refptr<base::SequencedTaskRunner>, scoped_refptr<storage::QuotaManagerProxy>, scoped_refptr<content::BlobStorageContextWrapper>, long, long) ./../../content/browser/cache_storage/cache_storage_cache.cc:1070:18
    #2 0x55b63ad7ca19 in content::CacheStorageCache::CreatePersistentCache(storage::BucketLocator const&, storage::mojom::CacheStorageOwner, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::CacheStorage*, base::FilePath const&, scoped_refptr<base::SequencedTaskRunner>, scoped_refptr<storage::QuotaManagerProxy>, scoped_refptr<content::BlobStorageContextWrapper>, long, long) ./../../content/browser/cache_storage/cache_storage_cache.cc:639:34
    #3 0x55b63ad5da6a in content::CacheStorage::SimpleCacheLoader::CreateCache(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, long, long) ./../../content/browser/cache_storage/cache_storage.cc:263:12
    #4 0x55b63ad56bad in content::CacheStorage::GetLoadedCache(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&) ./../../content/browser/cache_storage/cache_storage.cc:1363:67
    #5 0x55b63ad51a11 in content::CacheStorage::MatchAllCachesImpl(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, content::CacheStorageSchedulerPriority, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>) ./../../content/browser/cache_storage/cache_storage.cc:1276:44
    #6 0x55b63ad69076 in void base::internal::DecayedFunctorTraits<void (content::CacheStorage::*)(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, content::CacheStorageSchedulerPriority, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>), base::WeakPtr<content::CacheStorage>&&, mojo::StructPtr<blink::mojom::FetchAPIRequest>&&, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>&&, content::CacheStorageSchedulerPriority&&, long&&, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>&&>::Invoke<void (content::CacheStorage::*)(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, content::CacheStorageSchedulerPriority, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>), base::WeakPtr<content::CacheStorage> const&, mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, content::CacheStorageSchedulerPriority, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>>(void (content::CacheStorage::*)(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, content::CacheStorageSchedulerPriority, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>), base::WeakPtr<content::CacheStorage> const&, mojo::StructPtr<blink::mojom::FetchAPIRequest>&&, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>&&, content::CacheStorageSchedulerPriority&&, long&&, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>&&) ./../../base/functional/bind_internal.h:738:12
    #7 0x55b63ad68cf0 in MakeItSo<void (content::CacheStorage::*)(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, content::CacheStorageSchedulerPriority, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>), std::__Cr::tuple<base::WeakPtr<content::CacheStorage>, mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, content::CacheStorageSchedulerPriority, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)> > > ./../../base/functional/bind_internal.h:954:5
    #8 0x55b63ad68cf0 in RunImpl<void (content::CacheStorage::*)(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, content::CacheStorageSchedulerPriority, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>), std::__Cr::tuple<base::WeakPtr<content::CacheStorage>, mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, content::CacheStorageSchedulerPriority, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)> >, 0UL, 1UL, 2UL, 3UL, 4UL, 5UL> ./../../base/functional/bind_internal.h:1067:14
    #9 0x55b63ad68cf0 in base::internal::Invoker<base::internal::FunctorTraits<void (content::CacheStorage::*&&)(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, content::CacheStorageSchedulerPriority, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>), base::WeakPtr<content::CacheStorage>&&, mojo::StructPtr<blink::mojom::FetchAPIRequest>&&, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>&&, content::CacheStorageSchedulerPriority&&, long&&, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>&&>, base::internal::BindState<true, true, false, void (content::CacheStorage::*)(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, content::CacheStorageSchedulerPriority, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>), base::WeakPtr<content::CacheStorage>, mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, content::CacheStorageSchedulerPriority, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:980:12
    #10 0x55b63ae28396 in Run ./../../base/functional/callback.h:156:12
    #11 0x55b63ae28396 in content::CacheStorageOperation::Run() ./../../content/browser/cache_storage/cache_storage_operation.cc:37:23
    #12 0x55b63ae2d14d in Invoke<void (content::CacheStorageOperation::*)(), const base::WeakPtr<content::CacheStorageOperation> &> ./../../base/functional/bind_internal.h:738:12
    #13 0x55b63ae2d14d in MakeItSo<void (content::CacheStorageOperation::*)(), std::__Cr::tuple<base::WeakPtr<content::CacheStorageOperation> > > ./../../base/functional/bind_internal.h:954:5
    #14 0x55b63ae2d14d in void base::internal::Invoker<base::internal::FunctorTraits<void (content::CacheStorageOperation::*&&)(), base::WeakPtr<content::CacheStorageOperation>&&>, base::internal::BindState<true, true, false, void (content::CacheStorageOperation::*)(), base::WeakPtr<content::CacheStorageOperation>>, void ()>::RunImpl<void (content::CacheStorageOperation::*)(), std::__Cr::tuple<base::WeakPtr<content::CacheStorageOperation>>, 0ul>(void (content::CacheStorageOperation::*&&)(), std::__Cr::tuple<base::WeakPtr<content::CacheStorageOperation>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) ./../../base/functional/bind_internal.h:1067:14
    #15 0x55b63ae2bde7 in Run ./../../base/functional/callback.h:156:12
    #16 0x55b63ae2bde7 in content::CacheStorageScheduler::DispatchOperationTask(base::OnceCallback<void ()>) ./../../content/browser/cache_storage/cache_storage_scheduler.cc:131:19
    #17 0x55b63ae2af83 in content::CacheStorageScheduler::MaybeRunOperation() ./../../content/browser/cache_storage/cache_storage_scheduler.cc:184:5
    #18 0x55b63ae2a1a7 in content::CacheStorageScheduler::ScheduleOperation(long, content::CacheStorageSchedulerMode, content::CacheStorageSchedulerOp, content::CacheStorageSchedulerPriority, base::OnceCallback<void ()>) ./../../content/browser/cache_storage/cache_storage_scheduler.cc:94:3
    #19 0x55b63ad511da in content::CacheStorage::MatchAllCaches(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::InlinedStructPtr<blink::mojom::CacheQueryOptions>, content::CacheStorageSchedulerPriority, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>) ./../../content/browser/cache_storage/cache_storage.cc:789:15
    #20 0x55b63adfcbf3 in content::CacheStorageDispatcherHost::CacheStorageImpl::Match(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, bool, long, base::OnceCallback<void (mojo::StructPtr<blink::mojom::MatchResult>)>)::'lambda'(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>, content::CacheStorage*)::operator()(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>, content::CacheStorage*) const ./../../content/browser/cache_storage/cache_storage_dispatcher_host.cc:939:28
    #21 0x55b63adfc6be in void base::internal::DecayedFunctorTraits<content::CacheStorageDispatcherHost::CacheStorageImpl::Match(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, bool, long, base::OnceCallback<void (mojo::StructPtr<blink::mojom::MatchResult>)>)::'lambda'(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>, content::CacheStorage*), mojo::StructPtr<blink::mojom::FetchAPIRequest>&&, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>&&, bool&&, long&&, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>&&>::Invoke<content::CacheStorageDispatcherHost::CacheStorageImpl::Match(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, bool, long, base::OnceCallback<void (mojo::StructPtr<blink::mojom::MatchResult>)>)::'lambda'(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>, content::CacheStorage*), mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>, content::CacheStorage*>(content::CacheStorageDispatcherHost::CacheStorageImpl::Match(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, bool, long, base::OnceCallback<void (mojo::StructPtr<blink::mojom::MatchResult>)>)::'lambda'(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>, content::CacheStorage*)&&, mojo::StructPtr<blink::mojom::FetchAPIRequest>&&, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>&&, bool&&, long&&, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>&&, content::CacheStorage*&&) ./../../base/functional/bind_internal.h:656:12
    #22 0x55b63adfc488 in MakeItSo<(lambda at ../../content/browser/cache_storage/cache_storage_dispatcher_host.cc:923:9), std::__Cr::tuple<mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)> >, content::CacheStorage *> ./../../base/functional/bind_internal.h:930:12
    #23 0x55b63adfc488 in RunImpl<(lambda at ../../content/browser/cache_storage/cache_storage_dispatcher_host.cc:923:9), std::__Cr::tuple<mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)> >, 0UL, 1UL, 2UL, 3UL, 4UL> ./../../base/functional/bind_internal.h:1067:14
    #24 0x55b63adfc488 in base::internal::Invoker<base::internal::FunctorTraits<content::CacheStorageDispatcherHost::CacheStorageImpl::Match(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, bool, long, base::OnceCallback<void (mojo::StructPtr<blink::mojom::MatchResult>)>)::'lambda'(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>, content::CacheStorage*)&&, mojo::StructPtr<blink::mojom::FetchAPIRequest>&&, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>&&, bool&&, long&&, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>&&>, base::internal::BindState<false, false, false, content::CacheStorageDispatcherHost::CacheStorageImpl::Match(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, bool, long, base::OnceCallback<void (mojo::StructPtr<blink::mojom::MatchResult>)>)::'lambda'(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>, content::CacheStorage*), mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, long, base::OnceCallback<void (blink::mojom::CacheStorageError, mojo::StructPtr<blink::mojom::FetchAPIResponse>)>>, void (content::CacheStorage*)>::RunOnce(base::internal::BindStateBase*, content::CacheStorage*) ./../../base/functional/bind_internal.h:980:12
    #25 0x55b63adef1d3 in Run ./../../base/functional/callback.h:156:12
    #26 0x55b63adef1d3 in content::CacheStorageDispatcherHost::CacheStorageImpl::GetOrCreateCacheStorage(base::OnceCallback<void (content::CacheStorage*)>) ./../../content/browser/cache_storage/cache_storage_dispatcher_host.cc:1091:25
    #27 0x55b63adf16e5 in content::CacheStorageDispatcherHost::CacheStorageImpl::Match(mojo::StructPtr<blink::mojom::FetchAPIRequest>, mojo::StructPtr<blink::mojom::MultiCacheQueryOptions>, bool, bool, long, base::OnceCallback<void (mojo::StructPtr<blink::mojom::MatchResult>)>) ./../../content/browser/cache_storage/cache_storage_dispatcher_host.cc:922:5
    #28 0x55b63554eb17 in blink::mojom::CacheStorageStubDispatch::AcceptWithResponder(blink::mojom::CacheStorage*, mojo::Message*, std::__Cr::unique_ptr<mojo::MessageReceiverWithStatus, std::__Cr::default_delete<mojo::MessageReceiverWithStatus>>) ./gen/third_party/blink/public/mojom/cache_storage/cache_storage.mojom.cc:3680:13
    #29 0x55b6445a5e7c in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1005:56
    #30 0x55b6445c1c8d in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:48:24
    #31 0x55b6445ab7d5 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:724:20
    #32 0x55b6445d076a in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:1121:42
    #33 0x55b6445cea1c in mojo::internal::MultiplexRouter::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:734:7
    #34 0x55b6445c1d8a in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #35 0x55b64459d0ba in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) ./../../mojo/public/cpp/bindings/lib/connector.cc:562:49
    #36 0x55b64459ead0 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:620:14
    #37 0x55b64459e4f9 in OnHandleReadyInternal ./../../mojo/public/cpp/bindings/lib/connector.cc:452:3
    #38 0x55b64459e4f9 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int) ./../../mojo/public/cpp/bindings/lib/connector.cc:418:3
    #39 0x55b64459fdfa in Invoke<void (mojo::Connector::*)(const char *, unsigned int), mojo::Connector *, const char *, unsigned int> ./../../base/functional/bind_internal.h:738:12
    #40 0x55b64459fdfa in MakeItSo<void (mojo::Connector::*const &)(const char *, unsigned int), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, unsigned int> ./../../base/functional/bind_internal.h:930:12
    #41 0x55b64459fdfa in RunImpl<void (mojo::Connector::*const &)(const char *, unsigned int), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, 0UL, 1UL> ./../../base/functional/bind_internal.h:1067:14
    #42 0x55b64459fdfa in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int) ./../../base/functional/bind_internal.h:987:12

Thread T5 (ThreadPoolForeg) created by T0 (chrome) here:
    #0 0x55b630a662f1 in ___interceptor_pthread_create _asan_rtl_:3
    #1 0x55b6448c9248 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) ./../../base/threading/platform_thread_posix.cc:146:13
    #2 0x55b64485ed7d in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*) ./../../base/task/thread_pool/worker_thread.cc:207:3
    #3 0x55b64482cc1c in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush() ./../../base/task/thread_pool/thread_group.cc:92:13
    #4 0x55b64482c73f in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor() ./../../base/task/thread_pool/thread_group.cc:83:3
    #5 0x55b644854255 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::~ScopedCommandsExecutor() ./../../base/task/thread_pool/thread_group_impl.cc:49:3
    #6 0x55b644853d68 in base::internal::ThreadGroupImpl::Start(unsigned long, unsigned long, base::TimeDelta, scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*, base::internal::ThreadGroup::WorkerEnvironment, bool, std::__Cr::optional<base::TimeDelta>) ./../../base/task/thread_pool/thread_group_impl.cc:248:1
    #7 0x55b644838706 in base::internal::ThreadPoolImpl::Start(base::ThreadPoolInstance::InitParams const&, base::WorkerThreadObserver*) ./../../base/task/thread_pool/thread_pool_impl.cc:190:35
    #8 0x55b63c598556 in content::StartBrowserThreadPool() ./../../content/browser/startup_helper.cc:100:36
    #9 0x55b641a5410d in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content_main_runner_impl.cc:1243:5
    #10 0x55b641a5363c in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1162:12
    #11 0x55b641a4e335 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:356:36
    #12 0x55b641a4e94b in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:369:10
    #13 0x55b630abf563 in ChromeMain ./../../chrome/app/chrome_main.cc:231:12
    #14 0x7f24bc643b89 in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16

SUMMARY: AddressSanitizer: heap-use-after-free (/usr/local/google/home/thefrog/Downloads/linux-release_asan-linux-release-1360763/chrome+0x197216fb) (BuildId: 1c0cb5021dd75ec5)
Shadow bytes around the buggy address:
  0x7bd4ba6d0280: f7 fa fd fd fd fd fd fd fd fd fd fd fd fd fd fa
  0x7bd4ba6d0300: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x7bd4ba6d0380: fd fd fd fd fd fa fa fa fa fa fa fa f7 fa fd fd
  0x7bd4ba6d0400: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x7bd4ba6d0480: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
=>0x7bd4ba6d0500: fd fd fa fa fa fa fa fa f7 fa fd fd[fd]fd fd fd
  0x7bd4ba6d0580: fd fd fd fd fd fd fd fd fa fa fa fa fa fa f7 fa
  0x7bd4ba6d0600: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa
  0x7bd4ba6d0680: fa fa fa fa f7 fa fd fd fd fd fd fd fd fd fd fd
  0x7bd4ba6d0700: fd fd fd fa fa fa fa fa fa fa f7 fa fd fd fd fd
  0x7bd4ba6d0780: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa
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

==2387434==ADDITIONAL INFO

==2387434==Note: Please include this section with the ASan report.
Task trace:
    #0 0x55b6454cc44b in disk_cache::SimpleIndex::MergeInitializingSet(std::__Cr::unique_ptr<disk_cache::SimpleIndexLoadResult, std::__Cr::default_delete<disk_cache::SimpleIndexLoadResult>>) ./../../net/disk_cache/simple/simple_index.cc:600:28
    #1 0x55b6454db1e7 in disk_cache::SimpleIndexFile::LoadIndexEntries(base::Time, base::OnceCallback<void ()>, disk_cache::SimpleIndexLoadResult*) ./../../net/disk_cache/simple/simple_index_file.cc:377:33
    #2 0x55b6454db1e7 in disk_cache::SimpleIndexFile::LoadIndexEntries(base::Time, base::OnceCallback<void ()>, disk_cache::SimpleIndexLoadResult*) ./../../net/disk_cache/simple/simple_index_file.cc:377:33
    #3 0x55b64547bbd3 in disk_cache::SimpleBackendImpl::Init(base::OnceCallback<void (int)>) ./../../net/disk_cache/simple/simple_backend_impl.cc:272:7


Command line: `./chrome --user-data-dir=test-10-14-10-31am --flag-switches-begin --flag-switches-end --file-url-path-alias=/gen=/usr/local/google/home/thefrog/Downloads/linux-release_asan-linux-release-1360763/gen /usr/local/google/home/thefrog/security-sheriffing/poc-370069678/min.html`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==2387434==END OF ADDITIONAL INFO
==2387434==ABORTING


### pe...@google.com (2024-10-16)

Security Merge Request Consideration: Not requesting merge to dev (M131) because latest trunk commit (1363358) appears to be prior to dev branch point (1368529). If this is incorrect please remove NA-131 from the 'Merge' field and add 131 to the 'Merge-Request' field If other changes are required to fix this bug completely please request a merge if necessary.
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### am...@chromium.org (2024-11-08)

Thank you for the additional information. While we appreciate the new POC that demonstrates the UAF in a reliable manner without the patch, we have assessed the reward is sufficient with the information provided in the initial report that lead to the investigation and resolution of this issue.

While we want to incentivize the earlier reporting of security issues, unless there are exceptional circumstances (or a newly provided functional exploit), the criteria for VRP reward decisions is generally the information provided leading up to and before resolution of the bug to ensure we have the most pertinent information to efficiently and effectively triage and fix the bug.

Since the new POC did not alter the resolution or investigation of this issue, we are unable to consider a change in the VRP reward.

### m....@gmail.com (2024-11-08)

Thank you for your new response, but the reasons provided do not seem convincing.

I need to provide a new POC because the initial VRP review conclusion was based on the incorrect assumption that "This wasn't able to be reproduced in a way that demonstrates reliability." 
This was not due to the initial information I provided being insufficient to help the developers accurately identify and fix the issue.
In fact, the information I initially provided accurately pinpointed the root cause of the problem.

I understand that the VRP reward principle is to award the highest possible bounty.
I have seen this principle followed in some cases, but it is clear that it was not adhered to in this particular case.
Therefore, I hope you can correct the incorrect assumption from the first review and reconsider this case.

### am...@chromium.org (2024-11-08)

> This was not due to the initial information I provided being insufficient to help the developers accurately identify and fix the issue.
> In fact, the information I initially provided accurately pinpointed the root cause of the problem.

While the information you initially provided did allow for identifying and resolving the root cause, it did not do so in a way that was reliably reproducible and demonstrating remote exploitability without mitigations. You were able to demonstrate this, however, it was through a new POC and information that was provided after resolution. This new POC and information did not contribute to the root cause investigation or swift resolution of the bug.

Therefore, the VRP reward decision was made based on the information provided leading up to the resolution, which was that of mitigated memory corruption and a VRP reward consistent with that.

> I understand that the VRP reward principle is to award the highest possible bounty.

The VRP reward principle is to award the highest possible bounty *based on classification and demonstration of the security impact and exploitability presented in the report and contributing to resolution of the security issue*.
This is the reward criteria applied here, with the reward amount being consistent with the information provided before and up to the fix and Chrome VRP reward decision.

### pe...@google.com (2025-01-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/370069678)*
