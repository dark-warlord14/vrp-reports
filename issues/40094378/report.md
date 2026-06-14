# UAF in IndexedDB

| Field | Value |
|-------|-------|
| **Issue ID** | [40094378](https://issues.chromium.org/issues/40094378) |
| **Status** | New |
| **Severity** | S4-Minimal |
| **Priority** | P0 |
| **Component** | Blink>Storage>IndexedDB |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2019-03-25 |
| **Bounty** | $8,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36

Steps to reproduce the problem:
Chromium 75.0.3745.0
OS:Ubuntu 18.04
Steps to reproduce the problem:
1. new build with asan.
2. Run ./chrome  crash.html 

What is the expected behavior?

What went wrong?
Can stably get UAF crash.

Did this work before? N/A 

Chrome version: 75.0.3745.0   Channel: canary
OS Version: 18.04
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [crash.html](attachments/crash.html) (text/plain, 847 B)

## Timeline

### cd...@gmail.com (2019-03-25)

==21378==ERROR: AddressSanitizer: heap-use-after-free on address 0x6130006b3208 at pc 0x560e85ed4943 bp 0x7fed68029b30 sp 0x7fed68029b28
READ of size 4 at 0x6130006b3208 thread T15 (TaskSchedulerFo)
    #0 0x560e85ed4942 in base::subtle::RefCountedBase::AddRefImpl() const /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/memory/ref_counted.cc:43:3
    #1 0x560e7ffd9ba4 in AddRef /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/memory/ref_counted.h:67:5
    #2 0x560e7ffd9ba4 in AddRef /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/memory/ref_counted.h:331:0
    #3 0x560e7ffd9ba4 in AddRef /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/memory/scoped_refptr.h:291:0
    #4 0x560e7ffd9ba4 in scoped_refptr /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/memory/scoped_refptr.h:177:0
    #5 0x560e7ffd9ba4 in std::__1::__unique_if<content::IndexedDBDatabase::DeleteRequest>::__unique_single std::__1::make_unique<content::IndexedDBDatabase::DeleteRequest, content::IndexedDBDatabase*, scoped_refptr<content::IndexedDBCallbacks>&>(content::IndexedDBDatabase*&&, scoped_refptr<content::IndexedDBCallbacks>&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../buildtools/third_party/libc++/trunk/include/memory:3131:0
    #6 0x560e7ffd993c in content::IndexedDBDatabase::DeleteDatabase(scoped_refptr<content::IndexedDBCallbacks>, bool) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/indexed_db/indexed_db_database.cc:1945:17
    #7 0x560e8000829c in content::IndexedDBFactoryImpl::DeleteDatabase(std::__1::basic_string<unsigned short, base::string16_internals::string16_char_traits, std::__1::allocator<unsigned short> > const&, scoped_refptr<content::IndexedDBCallbacks>, url::Origin const&, base::FilePath const&, bool) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/indexed_db/indexed_db_factory_impl.cc:511:17
    #8 0x560e7fff8748 in content::IndexedDBDispatcherHost::DeleteDatabase(mojo::AssociatedInterfacePtrInfo<blink::mojom::IDBCallbacks>, std::__1::basic_string<unsigned short, base::string16_internals::string16_char_traits, std::__1::allocator<unsigned short> > const&, bool) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/indexed_db/indexed_db_dispatcher_host.cc:202:41
    #9 0x560e7e446e14 in blink::mojom::IDBFactoryStubDispatch::Accept(blink::mojom::IDBFactory*, mojo::Message*) /home/cowboy/chromium/src/out/chrome_asan_shared/gen/third_party/blink/public/mojom/indexeddb/indexeddb.mojom.cc:6412:13
    #10 0x560e861ecd84 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:433:32
    #11 0x560e861ff36f in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/multiplex_router.cc:873:42
    #12 0x560e861fdb0f in mojo::internal::MultiplexRouter::Accept(mojo::Message*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/multiplex_router.cc:594:38
    #13 0x560e861e495a in mojo::Connector::DispatchMessage(mojo::Message) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/connector.cc:525:49
    #14 0x560e861e6799 in mojo::Connector::ReadAllAvailableMessages() /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/connector.cc:600:12
    #15 0x560e8623cacd in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:136:12
    #16 0x560e8623cacd in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/system/simple_watcher.cc:293:0
    #17 0x560e85f9644f in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:97:12
    #18 0x560e85f9644f in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/common/task_annotator.cc:119:0
    #19 0x560e8600d768 in base::internal::TaskTracker::RunBlockShutdown(base::internal::Task*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/task_tracker.cc:944:19
    #20 0x560e8600ba5b in RunTaskWithShutdownBehavior /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/task_tracker.cc:959:7
    #21 0x560e8600ba5b in base::internal::TaskTracker::RunOrSkipTask(base::internal::Task, base::internal::Sequence*, base::TaskTraits const&, bool) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/task_tracker.cc:643:0
    #22 0x560e860f793f in base::internal::TaskTrackerPosix::RunOrSkipTask(base::internal::Task, base::internal::Sequence*, base::TaskTraits const&, bool) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/task_tracker_posix.cc:24:16
    #23 0x560e86009dec in base::internal::TaskTracker::RunAndPopNextTask(scoped_refptr<base::internal::Sequence>, base::internal::CanScheduleSequenceObserver*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/task_tracker.cc:494:3
    #24 0x560e85ffc725 in base::internal::SchedulerWorker::RunWorker() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker.cc:341:24
    #25 0x560e85ffbc90 in base::internal::SchedulerWorker::RunPooledWorker() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker.cc:233:3
    #26 0x560e860f924d in base::(anonymous namespace)::ThreadFunc(void*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/platform_thread_posix.cc:81:13
    #27 0x7fed8d7e06da in start_thread ??:0:0

0x6130006b3208 is located 8 bytes inside of 328-byte region [0x6130006b3200,0x6130006b3348)
freed by thread T17 (TaskSchedulerFo) here:
    #0 0x560e7c749d1d in operator delete(void*) _asan_rtl_:3
    #1 0x560e7fff1869 in DeleteInternal<content::IndexedDBDatabase> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/memory/ref_counted.h:352:5
    #2 0x560e7fff1869 in Destruct /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/memory/ref_counted.h:318:0
    #3 0x560e7fff1869 in Release /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/memory/ref_counted.h:341:0
    #4 0x560e7fff1869 in Release /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/memory/scoped_refptr.h:297:0
    #5 0x560e7fff1869 in ~scoped_refptr /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/memory/scoped_refptr.h:209:0
    #6 0x560e7fff1869 in RequestComplete /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/indexed_db/indexed_db_database.cc:1891:0
    #7 0x560e7fff1869 in content::IndexedDBDatabase::DeleteRequest::DoDelete(std::__1::vector<content::ScopeLock, std::__1::allocator<content::ScopeLock> >) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/indexed_db/indexed_db_database.cc:396:0
    #8 0x560e7fff1d3e in Invoke<void (content::IndexedDBDatabase::DeleteRequest::*)(std::__1::vector<content::ScopeLock, std::__1::allocator<content::ScopeLock> >), base::WeakPtr<content::IndexedDBDatabase::DeleteRequest>, std::__1::vector<content::ScopeLock, std::__1::allocator<content::ScopeLock> > > /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:499:12
    #9 0x560e7fff1d3e in void base::internal::InvokeHelper<true, void>::MakeItSo<void (content::IndexedDBDatabase::DeleteRequest::*)(std::__1::vector<content::ScopeLock, std::__1::allocator<content::ScopeLock> >), base::WeakPtr<content::IndexedDBDatabase::DeleteRequest>, std::__1::vector<content::ScopeLock, std::__1::allocator<content::ScopeLock> > >(void (content::IndexedDBDatabase::DeleteRequest::*&&)(std::__1::vector<content::ScopeLock, std::__1::allocator<content::ScopeLock> >), base::WeakPtr<content::IndexedDBDatabase::DeleteRequest>&&, std::__1::vector<content::ScopeLock, std::__1::allocator<content::ScopeLock> >&&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:619:0
    #10 0x560e80097034 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:97:12
    #11 0x560e80097034 in operator() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/indexed_db/scopes/disjoint_range_lock_manager.cc:71:0
    #12 0x560e80097034 in Invoke<(lambda at ../../content/browser/indexed_db/scopes/disjoint_range_lock_manager.cc:69:17), base::OnceCallback<void (std::__1::vector<content::ScopeLock, std::__1::allocator<content::ScopeLock> >)>, std::__1::unique_ptr<std::__1::vector<content::ScopeLock, std::__1::allocator<content::ScopeLock> >, std::__1::default_delete<std::__1::vector<content::ScopeLock, std::__1::allocator<content::ScopeLock> > > > > /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:386:0
    #13 0x560e80097034 in MakeItSo<(lambda at ../../content/browser/indexed_db/scopes/disjoint_range_lock_manager.cc:69:17), base::OnceCallback<void (std::__1::vector<content::ScopeLock, std::__1::allocator<content::ScopeLock> >)>, std::__1::unique_ptr<std::__1::vector<content::ScopeLock, std::__1::allocator<content::ScopeLock> >, std::__1::default_delete<std::__1::vector<content::ScopeLock, std::__1::allocator<content::ScopeLock> > > > > /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:599:0
    #14 0x560e80097034 in RunImpl<(lambda at ../../content/browser/indexed_db/scopes/disjoint_range_lock_manager.cc:69:17), std::__1::tuple<base::OnceCallback<void (std::__1::vector<content::ScopeLock, std::__1::allocator<content::ScopeLock> >)>, std::__1::unique_ptr<std::__1::vector<content::ScopeLock, std::__1::allocator<content::ScopeLock> >, std::__1::default_delete<std::__1::vector<content::ScopeLock, std::__1::allocator<content::ScopeLock> > > > >, 0, 1> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:672:0
    #15 0x560e80097034 in base::internal::Invoker<base::internal::BindState<content::DisjointRangeLockManager::AcquireLocks(base::internal::flat_tree<content::ScopesLockManager::ScopeLockRequest, content::ScopesLockManager::ScopeLockRequest, base::internal::GetKeyFromValueIdentity<content::ScopesLockManager::ScopeLockRequest>, std::__1::less<void> >, base::OnceCallback<void (std::__1::vector<content::ScopeLock, std::__1::allocator<content::ScopeLock> >)>)::$_0, base::OnceCallback<void (std::__1::vector<content::ScopeLock, std::__1::allocator<content::ScopeLock> >)>, std::__1::unique_ptr<std::__1::vector<content::ScopeLock, std::__1::allocator<content::ScopeLock> >, std::__1::default_delete<std::__1::vector<content::ScopeLock, std::__1::allocator<content::ScopeLock> > > > >, void ()>::RunOnce(base::internal::BindStateBase*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:641:0
    #16 0x560e85e6e543 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:97:12
    #17 0x560e85e6e543 in base::(anonymous namespace)::BarrierInfo::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/barrier_closure.cc:34:0
    #18 0x560e8009783e in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:97:12
    #19 0x560e8009783e in operator() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/indexed_db/scopes/disjoint_range_lock_manager.cc:82:0
    #20 0x560e8009783e in Invoke<(lambda at ../../content/browser/indexed_db/scopes/disjoint_range_lock_manager.cc:78:25), std::__1::vector<content::ScopeLock, std::__1::allocator<content::ScopeLock> > *, base::RepeatingCallback<void ()>, content::ScopeLock> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:386:0
    #21 0x560e8009783e in MakeItSo<(lambda at ../../content/browser/indexed_db/scopes/disjoint_range_lock_manager.cc:78:25), std::__1::vector<content::ScopeLock, std::__1::allocator<content::ScopeLock> > *, base::RepeatingCallback<void ()>, content::ScopeLock> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:599:0
    #22 0x560e8009783e in RunImpl<(lambda at ../../content/browser/indexed_db/scopes/disjoint_range_lock_manager.cc:78:25), std::__1::tuple<base::internal::UnretainedWrapper<std::__1::vector<content::ScopeLock, std::__1::allocator<content::ScopeLock> > >, base::RepeatingCallback<void ()> >, 0, 1> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:672:0
    #23 0x560e8009783e in base::internal::Invoker<base::internal::BindState<content::DisjointRangeLockManager::AcquireLocks(base::internal::flat_tree<content::ScopesLockManager::ScopeLockRequest, content::ScopesLockManager::ScopeLockRequest, base::internal::GetKeyFromValueIdentity<content::ScopesLockManager::ScopeLockRequest>, std::__1::less<void> >, base::OnceCallback<void (std::__1::vector<content::ScopeLock, std::__1::allocator<content::ScopeLock> >)>)::$_1, base::internal::UnretainedWrapper<std::__1::vector<content::ScopeLock, std::__1::allocator<content::ScopeLock> > >, base::RepeatingCallback<void ()> >, void (content::ScopeLock)>::RunOnce(base::internal::BindStateBase*, content::ScopeLock&&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:641:0
    #24 0x560e8009ae16 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:97:12
    #25 0x560e8009ae16 in Invoke<base::OnceCallback<void (content::ScopeLock)>, content::ScopeLock> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:560:0
    #26 0x560e8009ae16 in MakeItSo<base::OnceCallback<void (content::ScopeLock)>, content::ScopeLock> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:599:0
    #27 0x560e8009ae16 in RunImpl<base::OnceCallback<void (content::ScopeLock)>, std::__1::tuple<content::ScopeLock>, 0> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:672:0
    #28 0x560e8009ae16 in base::internal::Invoker<base::internal::BindState<base::OnceCallback<void (content::ScopeLock)>, content::ScopeLock>, void ()>::RunOnce(base::internal::BindStateBase*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:641:0
    #29 0x560e85f9644f in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:97:12
    #30 0x560e85f9644f in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/common/task_annotator.cc:119:0
    #31 0x560e8600d768 in base::internal::TaskTracker::RunBlockShutdown(base::internal::Task*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/task_tracker.cc:944:19
    #32 0x560e8600ba5b in RunTaskWithShutdownBehavior /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/task_tracker.cc:959:7
    #33 0x560e8600ba5b in base::internal::TaskTracker::RunOrSkipTask(base::internal::Task, base::internal::Sequence*, base::TaskTraits const&, bool) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/task_tracker.cc:643:0
    #34 0x560e860f793f in base::internal::TaskTrackerPosix::RunOrSkipTask(base::internal::Task, base::internal::Sequence*, base::TaskTraits const&, bool) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/task_tracker_posix.cc:24:16
    #35 0x560e86009dec in base::internal::TaskTracker::RunAndPopNextTask(scoped_refptr<base::internal::Sequence>, base::internal::CanScheduleSequenceObserver*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/task_tracker.cc:494:3
    #36 0x560e85ffc725 in base::internal::SchedulerWorker::RunWorker() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker.cc:341:24
    #37 0x560e85ffbc90 in base::internal::SchedulerWorker::RunPooledWorker() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker.cc:233:3
    #38 0x560e860f924d in base::(anonymous namespace)::ThreadFunc(void*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/platform_thread_posix.cc:81:13
    #39 0x7fed8d7e06da in start_thread ??:0:0

previously allocated by thread T15 (TaskSchedulerFo) here:
    #0 0x560e7c7494bd in operator new(unsigned long) _asan_rtl_:3
    #1 0x560e7ff9d3ba in content::IndexedDBClassFactory::CreateIndexedDBDatabase(std::__1::basic_string<unsigned short, base::string16_internals::string16_char_traits, std::__1::allocator<unsigned short> > const&, scoped_refptr<content::IndexedDBBackingStore>, scoped_refptr<content::IndexedDBFactory>, std::__1::unique_ptr<content::IndexedDBMetadataCoding, std::__1::default_delete<content::IndexedDBMetadataCoding> >, std::__1::pair<url::Origin, std::__1::basic_string<unsigned short, base::string16_internals::string16_char_traits, std::__1::allocator<unsigned short> > > const&, content::ScopesLockManager*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/indexed_db/indexed_db_class_factory.cc:40:10
    #2 0x560e7ffbd38e in content::IndexedDBDatabase::Create(std::__1::basic_string<unsigned short, base::string16_internals::string16_char_traits, std::__1::allocator<unsigned short> > const&, scoped_refptr<content::IndexedDBBackingStore>, scoped_refptr<content::IndexedDBFactory>, std::__1::unique_ptr<content::IndexedDBMetadataCoding, std::__1::default_delete<content::IndexedDBMetadataCoding> >, std::__1::pair<url::Origin, std::__1::basic_string<unsigned short, base::string16_internals::string16_char_traits, std::__1::allocator<unsigned short> > > const&, content::ScopesLockManager*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/indexed_db/indexed_db_database.cc:425:37
    #3 0x560e8000d928 in content::IndexedDBFactoryImpl::Open(std::__1::basic_string<unsigned short, base::string16_internals::string16_char_traits, std::__1::allocator<unsigned short> > const&, std::__1::unique_ptr<content::IndexedDBPendingConnection, std::__1::default_delete<content::IndexedDBPendingConnection> >, url::Origin const&, base::FilePath const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/indexed_db/indexed_db_factory_impl.cc:801:27
    #4 0x560e7fff7bb5 in content::IndexedDBDispatcherHost::Open(mojo::AssociatedInterfacePtrInfo<blink::mojom::IDBCallbacks>, mojo::AssociatedInterfacePtrInfo<blink::mojom::IDBDatabaseCallbacks>, std::__1::basic_string<unsigned short, base::string16_internals::string16_char_traits, std::__1::allocator<unsigned short> > const&, long, mojo::AssociatedInterfaceRequest<blink::mojom::IDBTransaction>, long) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/indexed_db/indexed_db_dispatcher_host.cc:187:41
    #5 0x560e7e4470a2 in blink::mojom::IDBFactoryStubDispatch::Accept(blink::mojom::IDBFactory*, mojo::Message*) /home/cowboy/chromium/src/out/chrome_asan_shared/gen/third_party/blink/public/mojom/indexeddb/indexeddb.mojom.cc:6369:13
    #6 0x560e861ecd84 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:433:32
    #7 0x560e861ff36f in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/multiplex_router.cc:873:42
    #8 0x560e861fdb0f in mojo::internal::MultiplexRouter::Accept(mojo::Message*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/multiplex_router.cc:594:38
    #9 0x560e861e495a in mojo::Connector::DispatchMessage(mojo::Message) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/connector.cc:525:49
    #10 0x560e861e6799 in mojo::Connector::ReadAllAvailableMessages() /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/connector.cc:600:12
    #11 0x560e8623cacd in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:136:12
    #12 0x560e8623cacd in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/system/simple_watcher.cc:293:0
    #13 0x560e85f9644f in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:97:12
    #14 0x560e85f9644f in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/common/task_annotator.cc:119:0
    #15 0x560e8600d768 in base::internal::TaskTracker::RunBlockShutdown(base::internal::Task*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/task_tracker.cc:944:19
    #16 0x560e8600ba5b in RunTaskWithShutdownBehavior /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/task_tracker.cc:959:7
    #17 0x560e8600ba5b in base::internal::TaskTracker::RunOrSkipTask(base::internal::Task, base::internal::Sequence*, base::TaskTraits const&, bool) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/task_tracker.cc:643:0
    #18 0x560e860f793f in base::internal::TaskTrackerPosix::RunOrSkipTask(base::internal::Task, base::internal::Sequence*, base::TaskTraits const&, bool) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/task_tracker_posix.cc:24:16
    #19 0x560e86009dec in base::internal::TaskTracker::RunAndPopNextTask(scoped_refptr<base::internal::Sequence>, base::internal::CanScheduleSequenceObserver*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/task_tracker.cc:494:3
    #20 0x560e85ffc725 in base::internal::SchedulerWorker::RunWorker() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker.cc:341:24
    #21 0x560e85ffbc90 in base::internal::SchedulerWorker::RunPooledWorker() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker.cc:233:3
    #22 0x560e860f924d in base::(anonymous namespace)::ThreadFunc(void*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/platform_thread_posix.cc:81:13
    #23 0x7fed8d7e06da in start_thread ??:0:0

Thread T15 (TaskSchedulerFo) created by T5 (TaskSchedulerFo) here:
    #0 0x560e7c706f6a in __interceptor_pthread_create _asan_rtl_:3
    #1 0x560e860f841a in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, base::PlatformThreadHandle*, base::ThreadPriority) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/platform_thread_posix.cc:120:13
    #2 0x560e85ffaff7 in base::internal::SchedulerWorker::Start(base::SchedulerWorkerObserver*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker.cc:79:3
    #3 0x560e85ff8664 in operator() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker_pool_impl.cc:187:15
    #4 0x560e85ff8664 in ForEachWorker<(lambda at ../../base/task/task_scheduler/scheduler_worker_pool_impl.cc:186:37)> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker_pool_impl.cc:152:0
    #5 0x560e85ff8664 in base::internal::SchedulerWorkerPoolImpl::ScopedWorkersExecutor::FlushImpl() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker_pool_impl.cc:186:0
    #6 0x560e85ff36fa in Flush /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker_pool_impl.cc:124:5
    #7 0x560e85ff36fa in base::internal::SchedulerWorkerPoolImpl::SchedulerWorkerDelegateImpl::GetWork(base::internal::SchedulerWorker*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker_pool_impl.cc:624:0
    #8 0x560e85ffc687 in base::internal::SchedulerWorker::RunWorker() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker.cc:328:51
    #9 0x560e85ffbc90 in base::internal::SchedulerWorker::RunPooledWorker() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker.cc:233:3
    #10 0x560e860f924d in base::(anonymous namespace)::ThreadFunc(void*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/platform_thread_posix.cc:81:13
    #11 0x7fed8d7e06da in start_thread ??:0:0

Thread T5 (TaskSchedulerFo) created by T3 (TaskSchedulerFo) here:
    #0 0x560e7c706f6a in __interceptor_pthread_create _asan_rtl_:3
    #1 0x560e860f841a in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, base::PlatformThreadHandle*, base::ThreadPriority) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/platform_thread_posix.cc:120:13
    #2 0x560e85ffaff7 in base::internal::SchedulerWorker::Start(base::SchedulerWorkerObserver*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker.cc:79:3
    #3 0x560e85ff8664 in operator() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker_pool_impl.cc:187:15
    #4 0x560e85ff8664 in ForEachWorker<(lambda at ../../base/task/task_scheduler/scheduler_worker_pool_impl.cc:186:37)> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker_pool_impl.cc:152:0
    #5 0x560e85ff8664 in base::internal::SchedulerWorkerPoolImpl::ScopedWorkersExecutor::FlushImpl() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker_pool_impl.cc:186:0
    #6 0x560e85ff36fa in Flush /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker_pool_impl.cc:124:5
    #7 0x560e85ff36fa in base::internal::SchedulerWorkerPoolImpl::SchedulerWorkerDelegateImpl::GetWork(base::internal::SchedulerWorker*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker_pool_impl.cc:624:0
    #8 0x560e85ffc687 in base::internal::SchedulerWorker::RunWorker() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker.cc:328:51
    #9 0x560e85ffbc90 in base::internal::SchedulerWorker::RunPooledWorker() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker.cc:233:3
    #10 0x560e860f924d in base::(anonymous namespace)::ThreadFunc(void*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/platform_thread_posix.cc:81:13
    #11 0x7fed8d7e06da in start_thread ??:0:0

Thread T3 (TaskSchedulerFo) created by T0 (chrome) here:
    #0 0x560e7c706f6a in __interceptor_pthread_create _asan_rtl_:3
    #1 0x560e860f841a in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, base::PlatformThreadHandle*, base::ThreadPriority) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/platform_thread_posix.cc:120:13
    #2 0x560e85ffaff7 in base::internal::SchedulerWorker::Start(base::SchedulerWorkerObserver*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker.cc:79:3
    #3 0x560e85ff8664 in operator() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker_pool_impl.cc:187:15
    #4 0x560e85ff8664 in ForEachWorker<(lambda at ../../base/task/task_scheduler/scheduler_worker_pool_impl.cc:186:37)> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker_pool_impl.cc:152:0
    #5 0x560e85ff8664 in base::internal::SchedulerWorkerPoolImpl::ScopedWorkersExecutor::FlushImpl() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker_pool_impl.cc:186:0
    #6 0x560e85ff1447 in base::internal::SchedulerWorkerPoolImpl::ScopedWorkersExecutor::~ScopedWorkersExecutor() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker_pool_impl.cc:105:30
    #7 0x560e85ff1251 in base::internal::SchedulerWorkerPoolImpl::Start(base::SchedulerWorkerPoolParams const&, int, scoped_refptr<base::TaskRunner>, base::SchedulerWorkerObserver*, base::internal::SchedulerWorkerPoolImpl::WorkerEnvironment, base::Optional<base::TimeDelta>) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker_pool_impl.cc:435:1
    #8 0x560e85fdc976 in base::internal::TaskSchedulerImpl::Start(base::TaskScheduler::InitParams const&, base::SchedulerWorkerObserver*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/task_scheduler_impl.cc:142:21
    #9 0x560e7f9cd52c in content::StartBrowserTaskScheduler() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/startup_helper.cc:95:39
    #10 0x560e84fb6748 in content::ContentMainRunnerImpl::RunServiceManager(content::MainFunctionParams&, bool) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:924:7
    #11 0x560e84fb612f in content::ContentMainRunnerImpl::Run(bool) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:878:12
    #12 0x560e850e1004 in service_manager::Main(service_manager::MainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../services/service_manager/embedder/main.cc:415:29
    #13 0x560e84fb102c in content::ContentMain(content::ContentMainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main.cc:19:10
    #14 0x560e7c74c2a3 in ChromeMain /home/cowboy/chromium/src/out/chrome_asan_shared/../../chrome/app/chrome_main.cc:103:12
    #15 0x7fed86518b96 in __libc_start_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310:0

Thread T17 (TaskSchedulerFo) created by T0 (chrome) here:
    #0 0x560e7c706f6a in __interceptor_pthread_create _asan_rtl_:3
    #1 0x560e860f841a in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, base::PlatformThreadHandle*, base::ThreadPriority) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/platform_thread_posix.cc:120:13
    #2 0x560e85ffaff7 in base::internal::SchedulerWorker::Start(base::SchedulerWorkerObserver*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker.cc:79:3
    #3 0x560e85ff8664 in operator() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker_pool_impl.cc:187:15
    #4 0x560e85ff8664 in ForEachWorker<(lambda at ../../base/task/task_scheduler/scheduler_worker_pool_impl.cc:186:37)> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker_pool_impl.cc:152:0
    #5 0x560e85ff8664 in base::internal::SchedulerWorkerPoolImpl::ScopedWorkersExecutor::FlushImpl() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker_pool_impl.cc:186:0
    #6 0x560e85ff1447 in base::internal::SchedulerWorkerPoolImpl::ScopedWorkersExecutor::~ScopedWorkersExecutor() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker_pool_impl.cc:105:30
    #7 0x560e85ff235e in base::internal::SchedulerWorkerPoolImpl::PushSequenceAndWakeUpWorkers(base::internal::SequenceAndTransaction) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker_pool_impl.cc:456:1
    #8 0x560e85fe517d in base::internal::SchedulerWorkerPool::OnCanScheduleSequence(scoped_refptr<base::internal::Sequence>) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker_pool.cc:75:3
    #9 0x560e86007e8b in SchedulePreemptedSequence /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/task_tracker.cc:751:34
    #10 0x560e86007e8b in base::internal::TaskTracker::SetMaxNumScheduledSequences(int, base::TaskPriority) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/task_tracker.cc:722:0
    #11 0x560e7f8a8389 in operator() /home/cowboy/chromium/src/out/chrome_asan_shared/../../buildtools/third_party/libc++/trunk/include/memory:2338:5
    #12 0x560e7f8a8389 in reset /home/cowboy/chromium/src/out/chrome_asan_shared/../../buildtools/third_party/libc++/trunk/include/memory:2651:0
    #13 0x560e7f8a8389 in content::BrowserMainLoop::CreateThreads() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/browser_main_loop.cc:939:0
    #14 0x560e8080faf5 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:136:12
    #15 0x560e8080faf5 in content::StartupTaskRunner::RunAllTasksNow() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/startup_task_runner.cc:41:0
    #16 0x560e7f8a7fa6 in content::BrowserMainLoop::CreateStartupTasks() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/browser_main_loop.cc:908:25
    #17 0x560e7f8b2a3a in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/browser_main_runner_impl.cc:144:15
    #18 0x560e7f8a2bbe in content::BrowserMain(content::MainFunctionParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/browser_main.cc:43:32
    #19 0x560e84fb6d5c in RunBrowserProcessMain /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:555:10
    #20 0x560e84fb6d5c in content::ContentMainRunnerImpl::RunServiceManager(content::MainFunctionParams&, bool) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:982:0
    #21 0x560e84fb612f in content::ContentMainRunnerImpl::Run(bool) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:878:12
    #22 0x560e850e1004 in service_manager::Main(service_manager::MainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../services/service_manager/embedder/main.cc:415:29
    #23 0x560e84fb102c in content::ContentMain(content::ContentMainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main.cc:19:10
    #24 0x560e7c74c2a3 in ChromeMain /home/cowboy/chromium/src/out/chrome_asan_shared/../../chrome/app/chrome_main.cc:103:12
    #25 0x7fed86518b96 in __libc_start_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310:0

SUMMARY: AddressSanitizer: heap-use-after-free (/home/cowboy/chromium/src/out/chrome_asan_shared/chrome+0x11fff942)
Shadow bytes around the buggy address:
  0x0c26800ce5f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa
  0x0c26800ce600: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c26800ce610: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c26800ce620: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c26800ce630: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
=>0x0c26800ce640: fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c26800ce650: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c26800ce660: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa
  0x0c26800ce670: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c26800ce680: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c26800ce690: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
  Shadow gap:              cc
==21378==ABORTING
Received signal 6
    #0 0x560e7c6dbeeb in __interceptor_backtrace /b/swarming/w/ir/k/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4065:13
    #1 0x560e860c2234 in base::debug::CollectStackTrace(void**, unsigned long) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/stack_trace_posix.cc:818:39
    #2 0x560e85e7fbd2 in StackTrace /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/stack_trace.cc:206:12
    #3 0x560e85e7fbd2 in base::debug::StackTrace::StackTrace() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/stack_trace.cc:203:0
    #4 0x560e860c126a in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/stack_trace_posix.cc:341:3
    #5 0x7fed8d7eb890 in __funlockfile ??:?
    #6 0x7fed8d7eb890 in ?? ??:0
    #7 0x7fed86535e97 in __libc_signal_restore_set /build/glibc-OTsEL5/glibc-2.27/signal/../sysdeps/unix/sysv/linux/nptl-signals.h:80:0
    #8 0x7fed86535e97 in gsignal /build/glibc-OTsEL5/glibc-2.27/signal/../sysdeps/unix/sysv/linux/raise.c:48:0
    #9 0x7fed86537801 in abort /build/glibc-OTsEL5/glibc-2.27/stdlib/abort.c:79:0
    #10 0x560e7c737fa7 in __sanitizer::Abort() /b/swarming/w/ir/k/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_posix_libcdep.cc:154:3
    #11 0x560e7c7369b1 in __sanitizer::Die() /b/swarming/w/ir/k/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_termination.cc:58:5
    #12 0x560e7c722c99 in __asan::ScopedInErrorReport::~ScopedInErrorReport() _asan_rtl_:7
    #13 0x560e7c722196 in __asan::ReportGenericError(unsigned long, unsigned long, unsigned long, unsigned long, bool, unsigned long, unsigned int, bool) _asan_rtl_:1
    #14 0x560e7c722f48 in __asan_report_load4 _asan_rtl_:1
    #15 0x560e85ed4943 in base::subtle::RefCountedBase::AddRefImpl() const /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/memory/ref_counted.cc:43:3
    #16 0x560e7ffd9ba5 in AddRef /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/memory/ref_counted.h:67:5
    #17 0x560e7ffd9ba5 in AddRef /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/memory/ref_counted.h:331:0
    #18 0x560e7ffd9ba5 in AddRef /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/memory/scoped_refptr.h:291:0
    #19 0x560e7ffd9ba5 in scoped_refptr /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/memory/scoped_refptr.h:177:0
    #20 0x560e7ffd9ba5 in std::__1::__unique_if<content::IndexedDBDatabase::DeleteRequest>::__unique_single std::__1::make_unique<content::IndexedDBDatabase::DeleteRequest, content::IndexedDBDatabase*, scoped_refptr<content::IndexedDBCallbacks>&>(content::IndexedDBDatabase*&&, scoped_refptr<content::IndexedDBCallbacks>&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../buildtools/third_party/libc++/trunk/include/memory:3131:0
    #21 0x560e7ffd993d in content::IndexedDBDatabase::DeleteDatabase(scoped_refptr<content::IndexedDBCallbacks>, bool) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/indexed_db/indexed_db_database.cc:1945:17
    #22 0x560e8000829d in content::IndexedDBFactoryImpl::DeleteDatabase(std::__1::basic_string<unsigned short, base::string16_internals::string16_char_traits, std::__1::allocator<unsigned short> > const&, scoped_refptr<content::IndexedDBCallbacks>, url::Origin const&, base::FilePath const&, bool) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/indexed_db/indexed_db_factory_impl.cc:511:17
    #23 0x560e7fff8749 in content::IndexedDBDispatcherHost::DeleteDatabase(mojo::AssociatedInterfacePtrInfo<blink::mojom::IDBCallbacks>, std::__1::basic_string<unsigned short, base::string16_internals::string16_char_traits, std::__1::allocator<unsigned short> > const&, bool) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/indexed_db/indexed_db_dispatcher_host.cc:202:41
    #24 0x560e7e446e15 in blink::mojom::IDBFactoryStubDispatch::Accept(blink::mojom::IDBFactory*, mojo::Message*) /home/cowboy/chromium/src/out/chrome_asan_shared/gen/third_party/blink/public/mojom/indexeddb/indexeddb.mojom.cc:6412:13
    #25 0x560e861ecd85 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:433:32
    #26 0x560e861ff370 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/multiplex_router.cc:873:42
    #27 0x560e861fdb10 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/multiplex_router.cc:594:38
    #28 0x560e861e495b in mojo::Connector::DispatchMessage(mojo::Message) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/connector.cc:525:49
    #29 0x560e861e679a in mojo::Connector::ReadAllAvailableMessages() /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/connector.cc:600:12
    #30 0x560e8623cace in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:136:12
    #31 0x560e8623cace in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/system/simple_watcher.cc:293:0
    #32 0x560e85f96450 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:97:12
    #33 0x560e85f96450 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/common/task_annotator.cc:119:0
    #34 0x560e8600d769 in base::internal::TaskTracker::RunBlockShutdown(base::internal::Task*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/task_tracker.cc:944:19
    #35 0x560e8600ba5c in RunTaskWithShutdownBehavior /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/task_tracker.cc:959:7
    #36 0x560e8600ba5c in base::internal::TaskTracker::RunOrSkipTask(base::internal::Task, base::internal::Sequence*, base::TaskTraits const&, bool) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/task_tracker.cc:643:0
    #37 0x560e860f7940 in base::internal::TaskTrackerPosix::RunOrSkipTask(base::internal::Task, base::internal::Sequence*, base::TaskTraits const&, bool) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/task_tracker_posix.cc:24:16
    #38 0x560e86009ded in base::internal::TaskTracker::RunAndPopNextTask(scoped_refptr<base::internal::Sequence>, base::internal::CanScheduleSequenceObserver*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/task_tracker.cc:494:3
    #39 0x560e85ffc726 in base::internal::SchedulerWorker::RunWorker() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker.cc:341:24
    #40 0x560e85ffbc91 in base::internal::SchedulerWorker::RunPooledWorker() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/task_scheduler/scheduler_worker.cc:233:3
    #41 0x560e860f924e in base::(anonymous namespace)::ThreadFunc(void*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/platform_thread_posix.cc:81:13
    #42 0x7fed8d7e06db in start_thread ??:0:0
    #43 0x7fed8661888f in clone /build/glibc-OTsEL5/glibc-2.27/misc/../sysdeps/unix/sysv/linux/x86_64/clone.S:95:0
  r8: 0000000000000000  r9: 00007fed68028b70 r10: 0000000000000008 r11: 0000000000000246
 r12: 00007fed68029b30 r13: 00007fed68029b28 r14: 00007fed68029ad0 r15: 0000560e99187d18
  di: 0000000000000002  si: 00007fed68028b70  bp: 00007fed68029b00  bx: 0000560e990f57f0
  dx: 0000000000000000  ax: 0000000000000000  cx: 00007fed86535e97  sp: 00007fed68028b70
  ip: 00007fed86535e97 efl: 0000000000000246 cgf: 002b000000000033 erf: 0000000000000000
 trp: 0000000000000000 msk: 0000000000000000 cr2: 0000000000000000
[end of stack trace]
Calling _exit(1). Core file will not be generated.


### cl...@chromium.org (2019-03-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5757447200440320.

### wf...@chromium.org (2019-03-25)

[Empty comment from Monorail migration]

[Monorail components: Blink>Storage>IndexedDB]

### ke...@chromium.org (2019-03-25)

Thanks for the report. Cluster-fuzz can repro, just working on the regression range now.

### dm...@chromium.org (2019-03-25)

[Comment Deleted]

### cl...@chromium.org (2019-03-25)

Detailed report: https://clusterfuzz.com/testcase?key=5757447200440320

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x6140000c6e88
Crash State:
  base::subtle::RefCountedBase::AddRefImpl
  content::IndexedDBDatabase::OpenConnection
  content::IndexedDBFactoryImpl::Open
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=642148:642166

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5757447200440320

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

### ke...@chromium.org (2019-03-25)

CF has revision 642156 in the regression range.

### ke...@chromium.org (2019-03-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-26)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dm...@chromium.org (2019-03-26)

Uploaded a human-readable version of the crash testcase. Interesting tidbit here - the index is set up in an invalid way (null keypath), and this is required to get it to crash.

### dm...@chromium.org (2019-03-26)

I reduced the test case a big (and made it legible), and it seems to be:
1. Deleting a database
2. Opening a database
3. Queueing a delete
4. doing a 'put' on the database infinitely, but it is invalid due to the index setup - important?
5. go to step 1.

The cause is that the DisjointRangeLockManager posts a task when the lock is released, so the lock acquisition in DoDelete doesn't happen synchronously. This causes problems in the 'Close' code [1], where it assumes that the request will happen right away if it is a delete request, where the active request will be destroyed when there are no connections.

Ways to fix this are:
1. Stop asking for locks when calling DoDelete. Since the code already waits until all connections are closed, we know that there are no more locks being held.
2. Stop assuming here [1] that OnConnectionClosed will synchronously execute Delete & then delete the active request here.
3. Refactor all of this code into the factory & clean this logic up.

The easiest to do is #1, so this will be done & merged.

[1] https://cs.chromium.org/chromium/src/content/browser/indexed_db/indexed_db_database.cc?g=0&l=2001


### wf...@chromium.org (2019-03-26)

Memory corruption in unsandboxed process via webpage is pri-0 critical.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8008668d66a9b9e45dd38a03f69530e734d9208c

commit 8008668d66a9b9e45dd38a03f69530e734d9208c
Author: Daniel Murphy <dmurph@chromium.org>
Date: Wed Mar 27 02:12:41 2019

[IndexedDB] Stop requesting locks in the Delete request.

Locks were assumed to be granted synchronously when all previous locks
were destructed. This isn't the case when there is a chain of dependent
locks, as granting a lock posts a task.

Since the delete code doesn't need a transaction to work (yet), remove
the locks here, and refactor this area for the new Scopes integration.

R=pwnall@chromium.org

Bug: 945370
Change-Id: Ifce3163852db6b2eae2127ee7062e788a19b9546
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1539211
Reviewed-by: Victor Costan <pwnall@chromium.org>
Commit-Queue: Victor Costan <pwnall@chromium.org>
Cr-Commit-Position: refs/heads/master@{#644653}
[modify] https://crrev.com/8008668d66a9b9e45dd38a03f69530e734d9208c/content/browser/indexed_db/indexed_db_database.cc


### cl...@chromium.org (2019-03-27)

ClusterFuzz has detected this issue as fixed in range 644652:644654.

Detailed report: https://clusterfuzz.com/testcase?key=5757447200440320

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x6140000c6e88
Crash State:
  base::subtle::RefCountedBase::AddRefImpl
  content::IndexedDBDatabase::OpenConnection
  content::IndexedDBFactoryImpl::Open
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=642148:642166
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=644652:644654

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5757447200440320

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2019-03-27)

ClusterFuzz testcase 5757447200440320 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### dm...@chromium.org (2019-03-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-27)

This bug requires manual review: We don't branch M75 until 2019-04-18.
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), geohsu@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-03-27)

This bug requires manual review: M74 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), dgagnon@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-03-27)

M75 is not branched yet, so no merge needed. Removing "Merge-Review-75" label.

+adetaylor@ for M74 merge review,

### ad...@chromium.org (2019-03-27)

M74 merge approved: critical security bug.

### go...@chromium.org (2019-03-27)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f5a603711e1cdd3dbfafdaa98f821c27c6a2dec4

commit f5a603711e1cdd3dbfafdaa98f821c27c6a2dec4
Author: Daniel Murphy <dmurph@chromium.org>
Date: Wed Mar 27 21:29:08 2019

[IndexedDB] Stop requesting locks in the Delete request.

Locks were assumed to be granted synchronously when all previous locks
were destructed. This isn't the case when there is a chain of dependent
locks, as granting a lock posts a task.

Since the delete code doesn't need a transaction to work (yet), remove
the locks here, and refactor this area for the new Scopes integration.

R=​pwnall@chromium.org

Bug: 945370
Change-Id: Ifce3163852db6b2eae2127ee7062e788a19b9546
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1539211
Reviewed-by: Victor Costan <pwnall@chromium.org>
Commit-Queue: Victor Costan <pwnall@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#644653}(cherry picked from commit 8008668d66a9b9e45dd38a03f69530e734d9208c)
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1542035
Reviewed-by: Daniel Murphy <dmurph@chromium.org>
Cr-Commit-Position: refs/branch-heads/3729@{#496}
Cr-Branched-From: d4a8972e30b604f090aeda5dfff68386ae656267-refs/heads/master@{#638880}
[modify] https://crrev.com/f5a603711e1cdd3dbfafdaa98f821c27c6a2dec4/content/browser/indexed_db/indexed_db_database.cc


### cr...@appspot.gserviceaccount.com (2019-03-27)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/f5a603711e1cdd3dbfafdaa98f821c27c6a2dec4

Commit: f5a603711e1cdd3dbfafdaa98f821c27c6a2dec4
Author: dmurph@chromium.org
Commiter: dmurph@chromium.org
Date: 2019-03-27 21:29:08 +0000 UTC

[IndexedDB] Stop requesting locks in the Delete request.

Locks were assumed to be granted synchronously when all previous locks
were destructed. This isn't the case when there is a chain of dependent
locks, as granting a lock posts a task.

Since the delete code doesn't need a transaction to work (yet), remove
the locks here, and refactor this area for the new Scopes integration.

R=​pwnall@chromium.org

Bug: 945370
Change-Id: Ifce3163852db6b2eae2127ee7062e788a19b9546
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1539211
Reviewed-by: Victor Costan <pwnall@chromium.org>
Commit-Queue: Victor Costan <pwnall@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#644653}(cherry picked from commit 8008668d66a9b9e45dd38a03f69530e734d9208c)
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1542035
Reviewed-by: Daniel Murphy <dmurph@chromium.org>
Cr-Commit-Position: refs/branch-heads/3729@{#496}
Cr-Branched-From: d4a8972e30b604f090aeda5dfff68386ae656267-refs/heads/master@{#638880}

### sh...@chromium.org (2019-03-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-04-03)

[Empty comment from Monorail migration]

### na...@google.com (2019-04-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-04-10)

Congrats! The Panel decided to reward $8,000 for this report. 


### na...@google.com (2019-04-10)

[Empty comment from Monorail migration]

### dm...@chromium.org (2019-04-23)

[Empty comment from Monorail migration]

### aw...@google.com (2019-05-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-07-04)

This issue was migrated from crbug.com/chromium/945370?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094378)*
