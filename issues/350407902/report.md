# UAF in content::EmbeddedWorkerInstance::ReleaseProcess(Browser Process)

| Field | Value |
|-------|-------|
| **Issue ID** | [350407902](https://issues.chromium.org/issues/350407902) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>ServiceWorker |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | hi...@chromium.org |
| **Created** | 2024-07-01 |
| **Bounty** | $21,000.00 |

## Description


Sorry, I didn't notice it earlier and submitted it as a regular bug（https://issues.chromium.org/issues/350362792）. I have already deleted the relevant attachments and content.
Tested OS:
Ubuntu 22.04
Tested Chrome Version:
Chromium 128.0.6570.0
Chromium 128.0.6559.0
Repro Steps:
1. Start an HTTP service and place sw.js and crash.html in the HTTP service directory.

2. Open the Chrome browser and navigate to http://localhost:8880/crash.html:
./chrome --disable-gpu --user-data-dir=/tmp/xx http://localhost:8880/crash.html

3. The page will redirect to a non-existent page (noexistxxx or any real site,for example, http://www.google.com). Wait for over a minute, and the UAF (Use After Free) issue should reproduce.

4.Reopen the Chrome browser and navigate to http://localhost:8880/crash.html.

5.The page will again redirect to a non-existent page (noexistxxx). Wait for over a minute, and the UAF (Use After Free) issue should reproduce.
The above reproduction steps are stable on my local machine, but there may be some instability on other machines. If the issue does not reproduce, try multiple times or use a script to open multiple browsers for automated testing:
./launcher.sh ~/asan-linux-release/chrome http://localhost:8880/crash.html 5 2>&1 

==9029==ERROR: AddressSanitizer: heap-use-after-free on address 0x5130001f1f78 at pc 0x60d50dbf5f77 bp 0x7ffdc795b350 sp 0x7ffdc795b348
READ of size 8 at 0x5130001f1f78 thread T0 (chrome)
    #0 0x60d50dbf5f76 in swap<blink::mojom::SubresourceLoaderUpdaterProxy *> ./../../third_party/libc++/src/include/__utility/swap.h:43:9
    #1 0x60d50dbf5f76 in swap ./../../third_party/libc++/src/include/__memory/compressed_pair.h:155:5
    #2 0x60d50dbf5f76 in swap ./../../third_party/libc++/src/include/__memory/unique_ptr.h:281:101
    #3 0x60d50dbf5f76 in swap<blink::mojom::SubresourceLoaderUpdaterProxy, std::__Cr::default_delete<blink::mojom::SubresourceLoaderUpdaterProxy>, 0> ./../../third_party/libc++/src/include/__memory/unique_ptr.h:477:7
    #4 0x60d50dbf5f76 in Swap ./../../mojo/public/cpp/bindings/lib/interface_ptr_state.h:194:5
    #5 0x60d50dbf5f76 in reset ./../../mojo/public/cpp/bindings/remote.h:216:21
    #6 0x60d50dbf5f76 in content::EmbeddedWorkerInstance::ReleaseProcess() ./../../content/browser/service_worker/embedded_worker_instance.cc:1012:31
    #7 0x60d50dc05a3f in content::EmbeddedWorkerInstance::OnStopped() ./../../content/browser/service_worker/embedded_worker_instance.cc:709:3
    #8 0x60d506d2b1e5 in blink::mojom::EmbeddedWorkerInstanceHostStubDispatch::Accept(blink::mojom::EmbeddedWorkerInstanceHost*, mojo::Message*) ./gen/third_party/blink/public/mojom/service_worker/embedded_worker.mojom.cc:0:0
    #9 0x60d517b2c913 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1036:54
    #10 0x60d517b49178 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #11 0x60d517b31db5 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:721:20
    #12 0x60d517b56d5d in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:1116:42
    #13 0x60d517b54b6c in mojo::internal::MultiplexRouter::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:729:7
    #14 0x60d517b49178 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #15 0x60d517b2398a in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) ./../../mojo/public/cpp/bindings/lib/connector.cc:562:49
    #16 0x60d517b25595 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:620:14
    #17 0x60d517b24f79 in OnHandleReadyInternal ./../../mojo/public/cpp/bindings/lib/connector.cc:452:3
    #18 0x60d517b24f79 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int) ./../../mojo/public/cpp/bindings/lib/connector.cc:418:3
    #19 0x60d517b26976 in Invoke<void (mojo::Connector::*)(const char *, unsigned int), mojo::Connector *, const char *, unsigned int> ./../../base/functional/bind_internal.h:738:12
    #20 0x60d517b26976 in MakeItSo<void (mojo::Connector::*const &)(const char *, unsigned int), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, unsigned int> ./../../base/functional/bind_internal.h:930:12
    #21 0x60d517b26976 in RunImpl<void (mojo::Connector::*const &)(const char *, unsigned int), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, 0UL, 1UL> ./../../base/functional/bind_internal.h:1067:14
    #22 0x60d517b26976 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int) ./../../base/functional/bind_internal.h:987:12
    #23 0x60d507364de3 in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & ./../../base/functional/callback.h:344:12
    #24 0x60d507364b64 in Invoke<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind_internal.h:671:12
    #25 0x60d507364b64 in MakeItSo<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind_internal.h:930:12
    #26 0x60d507364b64 in RunImpl<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, 0UL> ./../../base/functional/bind_internal.h:1067:14
    #27 0x60d507364b64 in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) ./../../base/functional/bind_internal.h:987:12
    #28 0x60d517bb52db in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & ./../../base/functional/callback.h:344:12
    #29 0x60d517bb4c05 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple_watcher.cc:278:14
    #30 0x60d517bb5e98 in Invoke<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), const base::WeakPtr<mojo::SimpleWatcher> &, int, unsigned int, mojo::HandleSignalsState> ./../../base/functional/bind_internal.h:738:12
    #31 0x60d517bb5e98 in MakeItSo<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> > ./../../base/functional/bind_internal.h:954:5
    #32 0x60d517bb5e98 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>) ./../../base/functional/bind_internal.h:1067:14
    #33 0x60d5161e8d04 in Run ./../../base/functional/callback.h:156:12
    #34 0x60d5161e8d04 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:203:34
    #35 0x60d5162526ca in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:486:11)> ./../../base/task/common/task_annotator.h:90:5
    #36 0x60d5162526ca in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:484:23
    #37 0x60d516251081 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #38 0x60d51625342a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #39 0x60d5163c9d62 in base::MessagePumpGlib::HandleDispatch() ./../../base/message_loop/message_pump_glib.cc:649:46
    #40 0x60d5163cd0c8 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) ./../../base/message_loop/message_pump_glib.cc:274:43
    #41 0x7375b7444d3a in g_main_context_dispatch ??:0:0

0x5130001f1f78 is located 312 bytes inside of 368-byte region [0x5130001f1e40,0x5130001f1fb0)
freed by thread T0 (chrome) here:
    #0 0x60d501ee04ad in operator delete(void*) _asan_rtl_:3
    #1 0x60d50de95578 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:67:5
    #2 0x60d50de95578 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:278:7
    #3 0x60d50de95578 in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:248:71
    #4 0x60d50de95578 in content::ServiceWorkerVersion::~ServiceWorkerVersion() ./../../content/browser/service_worker/service_worker_version.cc:366:1
    #5 0x60d50de95903 in content::ServiceWorkerVersion::~ServiceWorkerVersion() ./../../content/browser/service_worker/service_worker_version.cc:341:47
    #6 0x60d50ddcca61 in DeleteInternal<content::ServiceWorkerVersion> ./../../base/memory/ref_counted.h:365:5
    #7 0x60d50ddcca61 in Destruct ./../../base/memory/ref_counted.h:329:5
    #8 0x60d50ddcca61 in Release ./../../base/memory/ref_counted.h:354:7
    #9 0x60d50ddcca61 in Release ./../../base/memory/scoped_refptr.h:384:8
    #10 0x60d50ddcca61 in ~scoped_refptr ./../../base/memory/scoped_refptr.h:273:7
    #11 0x60d50ddcca61 in content::ServiceWorkerRegistration::~ServiceWorkerRegistration() ./../../content/browser/service_worker/service_worker_registration.cc:102:1
    #12 0x60d50ddccd73 in content::ServiceWorkerRegistration::~ServiceWorkerRegistration() ./../../content/browser/service_worker/service_worker_registration.cc:92:57
    #13 0x60d50dc7255f in DeleteInternal<content::ServiceWorkerRegistration> ./../../base/memory/ref_counted.h:365:5
    #14 0x60d50dc7255f in Destruct ./../../base/memory/ref_counted.h:329:5
    #15 0x60d50dc7255f in Release ./../../base/memory/ref_counted.h:354:7
    #16 0x60d50dc7255f in Release ./../../base/memory/scoped_refptr.h:384:8
    #17 0x60d50dc7255f in ~scoped_refptr ./../../base/memory/scoped_refptr.h:273:7
    #18 0x60d50dc7255f in ~pair ./../../third_party/libc++/src/include/__utility/pair.h:64:29
    #19 0x60d50dc7255f in __destroy_at<std::__Cr::pair<const unsigned long, scoped_refptr<content::ServiceWorkerRegistration> >, 0> ./../../third_party/libc++/src/include/__memory/construct_at.h:67:11
    #20 0x60d50dc7255f in destroy<std::__Cr::pair<const unsigned long, scoped_refptr<content::ServiceWorkerRegistration> >, void, 0> ./../../third_party/libc++/src/include/__memory/allocator_traits.h:340:5
    #21 0x60d50dc7255f in std::__Cr::__tree<std::__Cr::__value_type<unsigned long, scoped_refptr<content::ServiceWorkerRegistration>>, std::__Cr::__map_value_compare<unsigned long, std::__Cr::__value_type<unsigned long, scoped_refptr<content::ServiceWorkerRegistration>>, std::__Cr::less<unsigned long>, true>, std::__Cr::allocator<std::__Cr::__value_type<unsigned long, scoped_refptr<content::ServiceWorkerRegistration>>>>::destroy(std::__Cr::__tree_node<std::__Cr::__value_type<unsigned long, scoped_refptr<content::ServiceWorkerRegistration>>, void*>*) ./../../third_party/libc++/src/include/__tree:1541:5
    #22 0x60d50dc3a226 in clear ./../../third_party/libc++/src/include/__tree:1572:3
    #23 0x60d50dc3a226 in clear ./../../third_party/libc++/src/include/map:1313:58
    #24 0x60d50dc3a226 in RemoveAllMatchingRegistrations ./../../content/browser/service_worker/service_worker_container_host.cc:1564:27
    #25 0x60d50dc3a226 in content::ServiceWorkerClient::~ServiceWorkerClient() ./../../content/browser/service_worker/service_worker_container_host.cc:208:3
    #26 0x60d50dca5ebd in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:67:5
    #27 0x60d50dca5ebd in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:278:7
    #28 0x60d50dca5ebd in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:248:71
    #29 0x60d50dca5ebd in ~pair ./../../third_party/libc++/src/include/__utility/pair.h:64:29
    #30 0x60d50dca5ebd in void std::__Cr::__destroy_at<std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const, std::__Cr::unique_ptr<content::ServiceWorkerClient, std::__Cr::default_delete<content::ServiceWorkerClient>>>, 0>(std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const, std::__Cr::unique_ptr<content::ServiceWorkerClient, std::__Cr::default_delete<content::ServiceWorkerClient>>>*) ./../../third_party/libc++/src/include/__memory/construct_at.h:67:11
    #31 0x60d50dca9509 in destroy<std::__Cr::pair<const std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >, std::__Cr::unique_ptr<content::ServiceWorkerClient, std::__Cr::default_delete<content::ServiceWorkerClient> > >, void, 0> ./../../third_party/libc++/src/include/__memory/allocator_traits.h:340:5
    #32 0x60d50dca9509 in erase ./../../third_party/libc++/src/include/__tree:2043:3
    #33 0x60d50dca9509 in unsigned long std::__Cr::__tree<std::__Cr::__value_type<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::unique_ptr<content::ServiceWorkerClient, std::__Cr::default_delete<content::ServiceWorkerClient>>>, std::__Cr::__map_value_compare<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::__value_type<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::unique_ptr<content::ServiceWorkerClient, std::__Cr::default_delete<content::ServiceWorkerClient>>>, std::__Cr::less<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>, true>, std::__Cr::allocator<std::__Cr::__value_type<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::unique_ptr<content::ServiceWorkerClient, std::__Cr::default_delete<content::ServiceWorkerClient>>>>>::__erase_unique<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&) ./../../third_party/libc++/src/include/__tree:2063:3
    #34 0x60d50dc82017 in erase ./../../third_party/libc++/src/include/map:1309:79
    #35 0x60d50dc82017 in content::ServiceWorkerClientOwner::DestroyServiceWorkerClient(base::WeakPtr<content::ServiceWorkerClient>) ./../../content/browser/service_worker/service_worker_context_core.cc:525:52
    #36 0x60d50dc9dbe1 in content::ScopedServiceWorkerClient::~ScopedServiceWorkerClient() ./../../content/browser/service_worker/service_worker_context_core.cc:1393:35
    #37 0x60d50dd5cb4b in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:67:5
    #38 0x60d50dd5cb4b in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:278:7
    #39 0x60d50dd5cb4b in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:248:71
    #40 0x60d50dd5cb4b in content::ServiceWorkerMainResourceHandle::~ServiceWorkerMainResourceHandle() ./../../content/browser/service_worker/service_worker_main_resource_handle.cc:29:67
    #41 0x60d50e37f6c5 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:67:5
    #42 0x60d50e37f6c5 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:278:7
    #43 0x60d50e37f6c5 in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:248:71
    #44 0x60d50e37f6c5 in content::DedicatedWorkerHost::~DedicatedWorkerHost() ./../../content/browser/worker_host/dedicated_worker_host.cc:159:1
    #45 0x60d50e380552 in RenderProcessExited ./../../content/browser/worker_host/dedicated_worker_host.cc:194:3
    #46 0x60d50e380552 in non-virtual thunk to content::DedicatedWorkerHost::RenderProcessExited(content::RenderProcessHost*, content::ChildProcessTerminationInfo const&) ./../../content/browser/worker_host/dedicated_worker_host.cc:0:0
    #47 0x60d50da85b12 in content::RenderProcessHostImpl::Cleanup() ./../../content/browser/renderer_host/render_process_host_impl.cc:3883:16
    #48 0x60d50da75f0b in content::RenderProcessHostImpl::DecrementWorkerRefCount() ./../../content/browser/renderer_host/render_process_host_impl.cc:2549:5
    #49 0x60d50ddb4e62 in content::ServiceWorkerProcessManager::ReleaseWorkerProcess(int) ./../../content/browser/service_worker/service_worker_process_manager.cc:195:16
    #50 0x60d50dc0d312 in content::EmbeddedWorkerInstance::WorkerProcessHandle::~WorkerProcessHandle() ./../../content/browser/service_worker/embedded_worker_instance.cc:196:23
    #51 0x60d50dbf5cca in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:67:5
    #52 0x60d50dbf5cca in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:278:7
    #53 0x60d50dbf5cca in content::EmbeddedWorkerInstance::ReleaseProcess() ./../../content/browser/service_worker/embedded_worker_instance.cc:1011:19
    #54 0x60d50dc05a3f in content::EmbeddedWorkerInstance::OnStopped() ./../../content/browser/service_worker/embedded_worker_instance.cc:709:3
    #55 0x60d506d2b1e5 in blink::mojom::EmbeddedWorkerInstanceHostStubDispatch::Accept(blink::mojom::EmbeddedWorkerInstanceHost*, mojo::Message*) ./gen/third_party/blink/public/mojom/service_worker/embedded_worker.mojom.cc:0:0
    #56 0x60d517b2c913 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1036:54
    #57 0x60d517b49178 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #58 0x60d517b31db5 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:721:20
    #59 0x60d517b56d5d in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:1116:42
    #60 0x60d517b54b6c in mojo::internal::MultiplexRouter::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:729:7
    #61 0x60d517b49178 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #62 0x60d517b2398a in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) ./../../mojo/public/cpp/bindings/lib/connector.cc:562:49
    #63 0x60d517b25595 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:620:14
    #64 0x60d517b24f79 in OnHandleReadyInternal ./../../mojo/public/cpp/bindings/lib/connector.cc:452:3
    #65 0x60d517b24f79 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int) ./../../mojo/public/cpp/bindings/lib/connector.cc:418:3

previously allocated by thread T0 (chrome) here:
    #0 0x60d501edfc4d in operator new(unsigned long) _asan_rtl_:3
    #1 0x60d50de93d3f in make_unique<content::EmbeddedWorkerInstance, content::ServiceWorkerVersion *> ./../../third_party/libc++/src/include/__memory/unique_ptr.h:620:26
    #2 0x60d50de93d3f in content::ServiceWorkerVersion::ServiceWorkerVersion(content::ServiceWorkerRegistration*, GURL const&, blink::mojom::ScriptType, long, mojo::PendingRemote<storage::mojom::ServiceWorkerLiveVersionRef>, base::WeakPtr<content::ServiceWorkerContextCore>) ./../../content/browser/service_worker/service_worker_version.cc:336:22
    #3 0x60d50de19143 in scoped_refptr<content::ServiceWorkerVersion> base::MakeRefCounted<content::ServiceWorkerVersion, content::ServiceWorkerRegistration*, GURL const&, blink::mojom::ScriptType const&, long const&, mojo::PendingRemote<storage::mojom::ServiceWorkerLiveVersionRef>, base::WeakPtr<content::ServiceWorkerContextCore>>(content::ServiceWorkerRegistration*&&, GURL const&, blink::mojom::ScriptType const&, long const&, mojo::PendingRemote<storage::mojom::ServiceWorkerLiveVersionRef>&&, base::WeakPtr<content::ServiceWorkerContextCore>&&) ./../../base/memory/scoped_refptr.h:150:16
    #4 0x60d50de17f87 in content::ServiceWorkerRegistry::GetOrCreateRegistration(storage::mojom::ServiceWorkerRegistrationData const&, std::__Cr::vector<mojo::StructPtr<storage::mojom::ServiceWorkerResourceRecord>, std::__Cr::allocator<mojo::StructPtr<storage::mojom::ServiceWorkerResourceRecord>>> const&, mojo::PendingRemote<storage::mojom::ServiceWorkerLiveVersionRef>) ./../../content/browser/service_worker/service_worker_registry.cc:1101:15
    #5 0x60d50ddf43c5 in content::ServiceWorkerRegistry::DidFindRegistrationForClientUrl(GURL const&, blink::StorageKey const&, long, base::OnceCallback<void (blink::ServiceWorkerStatusCode, scoped_refptr<content::ServiceWorkerRegistration>)>, storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&) ./../../content/browser/service_worker/service_worker_registry.cc:1250:9
    #6 0x60d50de23f1a in void base::internal::DecayedFunctorTraits<void (content::ServiceWorkerRegistry::*)(GURL const&, blink::StorageKey const&, long, base::OnceCallback<void (blink::ServiceWorkerStatusCode, scoped_refptr<content::ServiceWorkerRegistration>)>, storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&), base::WeakPtr<content::ServiceWorkerRegistry>&&, GURL&&, blink::StorageKey&&, long&&, base::internal::DoNothingCallbackTag&&>::Invoke<void (content::ServiceWorkerRegistry::*)(GURL const&, blink::StorageKey const&, long, base::OnceCallback<void (blink::ServiceWorkerStatusCode, scoped_refptr<content::ServiceWorkerRegistration>)>, storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&), base::WeakPtr<content::ServiceWorkerRegistry> const&, GURL, blink::StorageKey, long, base::internal::DoNothingCallbackTag, storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&>(void (content::ServiceWorkerRegistry::*)(GURL const&, blink::StorageKey const&, long, base::OnceCallback<void (blink::ServiceWorkerStatusCode, scoped_refptr<content::ServiceWorkerRegistration>)>, storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&), base::WeakPtr<content::ServiceWorkerRegistry> const&, GURL&&, blink::StorageKey&&, long&&, base::internal::DoNothingCallbackTag&&, storage::mojom::ServiceWorkerDatabaseStatus&&, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>&&, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&) ./../../base/functional/bind_internal.h:738:12
    #7 0x60d50de23ba5 in MakeItSo<void (content::ServiceWorkerRegistry::*)(const GURL &, const blink::StorageKey &, long, base::OnceCallback<void (blink::ServiceWorkerStatusCode, scoped_refptr<content::ServiceWorkerRegistration>)>, storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, const std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL> > > &), std::__Cr::tuple<base::WeakPtr<content::ServiceWorkerRegistry>, GURL, blink::StorageKey, long, base::internal::DoNothingCallbackTag>, storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, const std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL> > > &> ./../../base/functional/bind_internal.h:954:5
    #8 0x60d50de23ba5 in RunImpl<void (content::ServiceWorkerRegistry::*)(const GURL &, const blink::StorageKey &, long, base::OnceCallback<void (blink::ServiceWorkerStatusCode, scoped_refptr<content::ServiceWorkerRegistration>)>, storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, const std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL> > > &), std::__Cr::tuple<base::WeakPtr<content::ServiceWorkerRegistry>, GURL, blink::StorageKey, long, base::internal::DoNothingCallbackTag>, 0UL, 1UL, 2UL, 3UL, 4UL> ./../../base/functional/bind_internal.h:1067:14
    #9 0x60d50de23ba5 in base::internal::Invoker<base::internal::FunctorTraits<void (content::ServiceWorkerRegistry::*&&)(GURL const&, blink::StorageKey const&, long, base::OnceCallback<void (blink::ServiceWorkerStatusCode, scoped_refptr<content::ServiceWorkerRegistration>)>, storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&), base::WeakPtr<content::ServiceWorkerRegistry>&&, GURL&&, blink::StorageKey&&, long&&, base::internal::DoNothingCallbackTag&&>, base::internal::BindState<true, true, false, void (content::ServiceWorkerRegistry::*)(GURL const&, blink::StorageKey const&, long, base::OnceCallback<void (blink::ServiceWorkerStatusCode, scoped_refptr<content::ServiceWorkerRegistration>)>, storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&), base::WeakPtr<content::ServiceWorkerRegistry>, GURL, blink::StorageKey, long, base::internal::DoNothingCallbackTag>, void (storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&)>::RunOnce(base::internal::BindStateBase*, storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>&&, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&) ./../../base/functional/bind_internal.h:980:12
    #10 0x60d50de37473 in Run ./../../base/functional/callback.h:156:12
    #11 0x60d50de37473 in content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&>::DidReply(storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&) ./../../content/browser/service_worker/service_worker_registry.cc:233:31
    #12 0x60d50de378d2 in Invoke<void (content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, const std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL> > > &>::*)(storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, const std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL> > > &), content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, const std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL> > > &> *, storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, const std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL> > > &> ./../../base/functional/bind_internal.h:738:12
    #13 0x60d50de378d2 in MakeItSo<void (content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, const std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL> > > &>::*)(storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, const std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL> > > &), std::__Cr::tuple<base::internal::UnretainedWrapper<content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, const std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL> > > &>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, const std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL> > > &> ./../../base/functional/bind_internal.h:930:12
    #14 0x60d50de378d2 in void base::internal::Invoker<base::internal::FunctorTraits<void (content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&>::*&&)(storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&), content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&>*>, base::internal::BindState<true, true, false, void (content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&>::*)(storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&), base::internal::UnretainedWrapper<content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&)>::RunImpl<void (content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&>::*)(storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&), std::__Cr::tuple<base::internal::UnretainedWrapper<content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(void (content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&>::*&&)(storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&), std::__Cr::tuple<base::internal::UnretainedWrapper<content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>, storage::mojom::ServiceWorkerDatabaseStatus&&, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>&&, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&) ./../../base/functional/bind_internal.h:1067:14
    #15 0x60d50de37657 in base::internal::Invoker<base::internal::FunctorTraits<void (content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&>::*&&)(storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&), content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&>*>, base::internal::BindState<true, true, false, void (content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&>::*)(storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&), base::internal::UnretainedWrapper<content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&)>::RunOnce(base::internal::BindStateBase*, storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>&&, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&) ./../../base/functional/bind_internal.h:980:12
    #16 0x60d5074b6eb4 in Run ./../../base/functional/callback.h:156:12
    #17 0x60d5074b6eb4 in storage::mojom::ServiceWorkerStorageControl_FindRegistrationForClientUrl_ForwardToCallback::Accept(mojo::Message*) ./gen/components/services/storage/public/mojom/service_worker_storage_control.mojom.cc:6191:26
    #18 0x60d517b2cd0d in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1031:41
    #19 0x60d517b49178 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #20 0x60d517b31db5 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:721:20
    #21 0x60d517b56d5d in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:1116:42
    #22 0x60d517b54b6c in mojo::internal::MultiplexRouter::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:729:7
    #23 0x60d517b49178 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #24 0x60d517b2398a in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) ./../../mojo/public/cpp/bindings/lib/connector.cc:562:49
    #25 0x60d517b25595 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:620:14
    #26 0x60d517b26015 in Invoke<void (mojo::Connector::*)(), const base::WeakPtr<mojo::Connector> &> ./../../base/functional/bind_internal.h:738:12
    #27 0x60d517b26015 in MakeItSo<void (mojo::Connector::*)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector> > > ./../../base/functional/bind_internal.h:954:5
    #28 0x60d517b26015 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::*&&)(), base::WeakPtr<mojo::Connector>&&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector>>, void ()>::RunImpl<void (mojo::Connector::*)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector>>, 0ul>(void (mojo::Connector::*&&)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) ./../../base/functional/bind_internal.h:1067:14
    #29 0x60d5161e8d04 in Run ./../../base/functional/callback.h:156:12
    #30 0x60d5161e8d04 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:203:34
    #31 0x60d5162526ca in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:486:11)> ./../../base/task/common/task_annotator.h:90:5
    #32 0x60d5162526ca in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:484:23
    #33 0x60d516251081 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #34 0x60d51625342a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #35 0x60d5163ca850 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_glib.cc:694:48
    #36 0x60d51625409b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:654:12
    #37 0x60d51617431f in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #38 0x60d50c63dff1 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser_main_loop.cc:1086:18
    #39 0x60d50c645acc in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser_main_runner_impl.cc:159:15
    #40 0x60d50c6346c8 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser_main.cc:34:28

SUMMARY: AddressSanitizer: heap-use-after-free (/home/pwn11/asan-linux-release/chrome+0x1bd9af76) (BuildId: 916211ff17de9fce)
Shadow bytes around the buggy address:
  0x5130001f1c80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x5130001f1d00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x5130001f1d80: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa
  0x5130001f1e00: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x5130001f1e80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x5130001f1f00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]
  0x5130001f1f80: fd fd fd fd fd fd fa fa fa fa fa fa fa fa f7 fa
  0x5130001f2000: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x5130001f2080: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x5130001f2100: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
  0x5130001f2180: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
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

==9029==ADDITIONAL INFO

==9029==Note: Please include this section with the ASan report.
Task trace:
    #0 0x60d517bb5811 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) ./../../mojo/public/cpp/system/simple_watcher.cc:102:13


Command line: `/home/pwn11/asan-linux-release/chrome --disable-gpu --user-data-dir=/tmp/dd1 --flag-switches-begin --flag-switches-end --file-url-path-alias=/gen=/home/pwn11/asan-linux-release/gen http://localhost:8880/crash.html`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==9029==END OF ADDITIONAL INFO
==9029==ABORTING
[0701/205417.958491:ERROR:elf_dynamic_array_reader.h(64)] tag not found
Received signal 6
    #0 0x60d501e528c6 in ___interceptor_backtrace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4364:13
    #1 0x60d516380b71 in base::debug::CollectStackTrace(void const**, unsigned long) ./../../base/debug/stack_trace_posix.cc:1044:7
    #2 0x60d5163444f7 in StackTrace ./../../base/debug/stack_trace.cc:242:20
    #3 0x60d5163444f7 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:237:28
    #4 0x60d51637fb72 in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:463:3
    #5 0x7375b6042520 in __GI___sigaction :?
    #6 0x7375b60969fc in __pthread_kill_implementation ./nptl/pthread_kill.c:43:17
    #7 0x7375b60969fc in __pthread_kill_internal ./nptl/pthread_kill.c:78:10
    #8 0x7375b60969fc in pthread_kill ./nptl/pthread_kill.c:89:10
    #9 0x7375b6042476 in gsignal ./signal/../sysdeps/posix/raise.c:26:13
    #10 0x7375b60287f3 in abort ./stdlib/abort.c:79:7
    #11 0x60d501ec933c in __sanitizer::Abort() /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_posix_libcdep.cpp:163:3
    #12 0x60d501ec7d3e in __sanitizer::Die() /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_termination.cpp:58:5
    #13 0x60d501eae579 in __asan::ScopedInErrorReport::~ScopedInErrorReport() _asan_rtl_:7
    #14 0x60d501eb16b7 in __asan::ReportGenericError(unsigned long, unsigned long, unsigned long, unsigned long, bool, unsigned long, unsigned int, bool) _asan_rtl_:1
    #15 0x60d501eb2596 in __asan_report_load8 _asan_rtl_:1
    #16 0x60d50dbf5f77 in swap<blink::mojom::SubresourceLoaderUpdaterProxy *> ./../../third_party/libc++/src/include/__utility/swap.h:43:9
    #17 0x60d50dbf5f77 in swap ./../../third_party/libc++/src/include/__memory/compressed_pair.h:155:5
    #18 0x60d50dbf5f77 in swap ./../../third_party/libc++/src/include/__memory/unique_ptr.h:281:101
    #19 0x60d50dbf5f77 in swap<blink::mojom::SubresourceLoaderUpdaterProxy, std::__Cr::default_delete<blink::mojom::SubresourceLoaderUpdaterProxy>, 0> ./../../third_party/libc++/src/include/__memory/unique_ptr.h:477:7
    #20 0x60d50dbf5f77 in Swap ./../../mojo/public/cpp/bindings/lib/interface_ptr_state.h:194:5
    #21 0x60d50dbf5f77 in reset ./../../mojo/public/cpp/bindings/remote.h:216:21
    #22 0x60d50dbf5f77 in content::EmbeddedWorkerInstance::ReleaseProcess() ./../../content/browser/service_worker/embedded_worker_instance.cc:1012:31
    #23 0x60d50dc05a40 in content::EmbeddedWorkerInstance::OnStopped() ./../../content/browser/service_worker/embedded_worker_instance.cc:709:3
    #24 0x60d506d2b1e6 in blink::mojom::EmbeddedWorkerInstanceHostStubDispatch::Accept(blink::mojom::EmbeddedWorkerInstanceHost*, mojo::Message*) ./gen/third_party/blink/public/mojom/service_worker/embedded_worker.mojom.cc:0:0
    #25 0x60d517b2c914 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1036:54
    #26 0x60d517b49179 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #27 0x60d517b31db6 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:721:20
    #28 0x60d517b56d5e in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:1116:42
    #29 0x60d517b54b6d in mojo::internal::MultiplexRouter::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:729:7
    #30 0x60d517b49179 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #31 0x60d517b2398b in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) ./../../mojo/public/cpp/bindings/lib/connector.cc:562:49
    #32 0x60d517b25596 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:620:14
    #33 0x60d517b24f7a in OnHandleReadyInternal ./../../mojo/public/cpp/bindings/lib/connector.cc:452:3
    #34 0x60d517b24f7a in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int) ./../../mojo/public/cpp/bindings/lib/connector.cc:418:3
    #35 0x60d517b26977 in Invoke<void (mojo::Connector::*)(const char *, unsigned int), mojo::Connector *, const char *, unsigned int> ./../../base/functional/bind_internal.h:738:12
    #36 0x60d517b26977 in MakeItSo<void (mojo::Connector::*const &)(const char *, unsigned int), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, unsigned int> ./../../base/functional/bind_internal.h:930:12
    #37 0x60d517b26977 in RunImpl<void (mojo::Connector::*const &)(const char *, unsigned int), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, 0UL, 1UL> ./../../base/functional/bind_internal.h:1067:14
    #38 0x60d517b26977 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int) ./../../base/functional/bind_internal.h:987:12
    #39 0x60d507364de4 in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & ./../../base/functional/callback.h:344:12
    #40 0x60d507364b65 in Invoke<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind_internal.h:671:12
    #41 0x60d507364b65 in MakeItSo<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind_internal.h:930:12
    #42 0x60d507364b65 in RunImpl<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, 0UL> ./../../base/functional/bind_internal.h:1067:14
    #43 0x60d507364b65 in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) ./../../base/functional/bind_internal.h:987:12
    #44 0x60d517bb52dc in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & ./../../base/functional/callback.h:344:12
    #45 0x60d517bb4c06 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple_watcher.cc:278:14
    #46 0x60d517bb5e99 in Invoke<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), const base::WeakPtr<mojo::SimpleWatcher> &, int, unsigned int, mojo::HandleSignalsState> ./../../base/functional/bind_internal.h:738:12
    #47 0x60d517bb5e99 in MakeItSo<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> > ./../../base/functional/bind_internal.h:954:5
    #48 0x60d517bb5e99 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>) ./../../base/functional/bind_internal.h:1067:14
    #49 0x60d5161e8d05 in Run ./../../base/functional/callback.h:156:12
    #50 0x60d5161e8d05 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:203:34
    #51 0x60d5162526cb in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:486:11)> ./../../base/task/common/task_annotator.h:90:5
    #52 0x60d5162526cb in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:484:23
    #53 0x60d516251082 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #54 0x60d51625342b in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #55 0x60d5163c9d63 in base::MessagePumpGlib::HandleDispatch() ./../../base/message_loop/message_pump_glib.cc:649:46
    #56 0x60d5163cd0c9 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) ./../../base/message_loop/message_pump_glib.cc:274:43
    #57 0x7375b7444d3b in g_main_context_dispatch ??:0:0
    #58 0x7375b749a2b8 in g_io_channel_new_file ??:?
    #59 0x7375b74423e3 in g_main_context_iteration ??:0:0
    #60 0x60d5163ca460 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_glib.cc:683:30
    #61 0x60d51625409c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:654:12
    #62 0x60d516174320 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #63 0x60d50c63dff2 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser_main_loop.cc:1086:18
    #64 0x60d50c645acd in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser_main_runner_impl.cc:159:15
    #65 0x60d50c6346c9 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser_main.cc:34:28
    #66 0x60d51337a355 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:735:10
    #67 0x60d51337e14c in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content_main_runner_impl.cc:1321:10
    #68 0x60d51337d7fb in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1173:12
    #69 0x60d513377a2f in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:332:36
    #70 0x60d51337800c in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:345:10
    #71 0x60d501ee248c in ChromeMain ./../../chrome/app/chrome_main.cc:228:12
    #72 0x7375b6029d90 in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #73 0x7375b6029e40 in __libc_start_main ./csu/../csu/libc-start.c:392:3
    #74 0x60d501e0e02a in _start ??:0:0
  r8: 00007ffdc795a460  r9: 0000000000000000 r10: 0000000000000008 r11: 0000000000000246
 r12: 0000000000000006 r13: 0000000000000016 r14: 000060d53551c2d8 r15: 0fffff0000000000
  di: 0000000000002345  si: 0000000000002345  bp: 0000000000002345  bx: 00007375b5250540
  dx: 0000000000000006  ax: 0000000000000000  cx: 00007375b60969fc  sp: 00007ffdc795a390
  ip: 00007375b60969fc efl: 0000000000000246 cgf: 002b000000000033 erf: 0000000000000000
 trp: 0000000000000000 msk: 0000000000000000 cr2: 0000000000000000
[end of stack trace]
Aborted

## Attachments

- [crash.html](attachments/crash.html) (text/html, 599 B)
- [sw.js](attachments/sw.js) (text/javascript, 93 B)
- [asan.log](attachments/asan.log) (text/plain, 55.3 KB)
- [launcher.sh](attachments/launcher.sh) (text/x-sh, 612 B)
- [repro.mov](attachments/repro.mov) (video/quicktime, 7.2 MB)

## Timeline

### da...@chromium.org (2024-07-02)

I am not able to reproduce with an ASAN build of M126. Trying M128.

### da...@chromium.org (2024-07-02)

I am not getting it to reproduce with M128 either. Could you please provide some steps or repro that make this more reliable? I tried also running a whole bunch of instances at once (as suggested by the launcher script) but I am not able to reproduce.

### da...@chromium.org (2024-07-02)

Some code analysis.

ServiceWorkerVersion owns EmbeddedWorkerInstance in a unique\_ptr: <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/service_worker/service_worker_version.h;l=1100?q=ServiceWorkerVersion::ServiceWorkerVersion>

ServiceWorkerRegistration owns a bunch of ServiceWorkerVersions in scoped\_refptrs: <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/service_worker/service_worker_registration.h;l=316-318;drc=770f3fce3719ee18c102ad0b1a347d82147fbb1a> ServiceWorkerRegistration is also refcounted itself.

EmbeddedWorkerInstance implements mojom::EmbeddedWorkerInstanceHost which has OnStopped member. It calls ReleaseProcess, which deletes a mojo remote to the other process: `mojo::Remote<blink::mojom::SubresourceLoaderUpdater> subresource_loader_updater_;` <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/service_worker/embedded_worker_instance.cc;l=1012;drc=b0b102b6582fe1fca4a5eb6b156f198113674ec7>

It's not clear to me what the UAF is though. It should not be the `EmbeddedWorkerInstance::subresource_loader_updater_` since other fields are accessed in ReleaseProcess without issue. But the UAF stack reads like it's the use of the proxy\_ field of the subresource\_loader\_updater\_.

I think we need a better reproduction to be able to go further..

### em...@gmail.com (2024-07-02)

It's strange, I'm not quite sure why it can't be reproduced on other machines. I just downloaded the latest ASAN version and can still reproduce it consistently.
I recorded a video to see if it helps.
gs://chromium-browser-asan/linux-release/asan-linux-release-1322326.zip

### pe...@google.com (2024-07-02)

Thank you for providing more feedback. Adding the requester to the CC list.

### da...@chromium.org (2024-07-02)

Sorry but a video does not really help, we need to be able to reproduce it or understand it, and there's not enough here for me to do either yet. I will leave it to you to determine how to make this more reproducible or explain how it's functioning.

### em...@gmail.com (2024-07-03)


I still haven't figured out why it can't be reproduced on other machines. The reproduction steps are exactly as shown in the video.
The use-after-free occurs because EmbeddedWorkerInstance is released at point [0] in the ReleaseProcess method, leading to subresource_loader_updater_ being accessed afterward, which results in the error. This can be observed in the ASan logs indicating the free operation, or it can be made more evident by adding debugging information.

```
void EmbeddedWorkerInstance::ReleaseProcess() {
  // Abort an inflight start task.
  inflight_start_info_.reset();
  // NotifyForegroundServiceWorkerRemoved() may trigger a call to
  // UpdateForegroundPriority(). By setting status_ to kStopping we
  // prevent NotifyForegroundServiceWorkerAdded() from being called
  // from UpdateForegroundPriority() since we don't want it to be
  // re-added at this stage.
  status_ = blink::EmbeddedWorkerStatus::kStopping;
  pause_initializing_global_scope_ = false;
  NotifyForegroundServiceWorkerRemoved();

  instance_host_receiver_.reset();
  devtools_proxy_.reset();
  process_handle_.reset();             --->[0]
  subresource_loader_updater_.reset();
  coep_reporter_.reset();
  status_ = blink::EmbeddedWorkerStatus::kStopped;
  starting_phase_ = NOT_STARTING;
  thread_id_ = ServiceWorkerConsts::kInvalidEmbeddedWorkerThreadId;

  DCHECK(!foreground_notified_);
}
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/service_worker/embedded_worker_instance.cc;drc=9cae81d88d6a428544c2f39c8944fad64663515e;l=1011
```

This is a my log patch:
diff --git a/content/browser/service_worker/embedded_worker_instance.cc b/content/browser/service_worker/embedded_worker_instance.cc
index 432547f21d7b9..b6b2146c48710 100644
--- a/content/browser/service_worker/embedded_worker_instance.cc
+++ b/content/browser/service_worker/embedded_worker_instance.cc
@@ -60,7 +60,6 @@
 #include "third_party/blink/public/mojom/renderer_preference_watcher.mojom.h"
 #include "third_party/blink/public/mojom/service_worker/service_worker_object.mojom.h"
 #include "url/gurl.h"
-
 #if !BUILDFLAG(IS_ANDROID)
 #include "content/browser/hid/hid_service.h"
 #endif
@@ -224,6 +223,7 @@ struct EmbeddedWorkerInstance::StartInfo {

 EmbeddedWorkerInstance::~EmbeddedWorkerInstance() {
   DCHECK_CURRENTLY_ON(BrowserThread::UI);
+  LOG(ERROR) << "EmbeddedWorkerInstance::~EmbeddedWorkerInstance,this:"<<this;
   ReleaseProcess();
 }

@@ -704,6 +704,7 @@ void EmbeddedWorkerInstance::OnStarted(
 }

 void EmbeddedWorkerInstance::OnStopped() {
+  LOG(ERROR) << "EmbeddedWorkerInstance::OnStopped(),this:"<<this;
   DCHECK_CURRENTLY_ON(BrowserThread::UI);
   blink::EmbeddedWorkerStatus old_status = status_;
   ReleaseProcess();
@@ -996,6 +997,7 @@ void EmbeddedWorkerInstance::OnNetworkAccessedForScriptLoad() {

 void EmbeddedWorkerInstance::ReleaseProcess() {
   // Abort an inflight start task.
+  LOG(ERROR) << "EmbeddedWorkerInstance::ReleaseProcess(),this:"<<this;
   inflight_start_info_.reset();
   // NotifyForegroundServiceWorkerRemoved() may trigger a call to
   // UpdateForegroundPriority(). By setting status_ to kStopping we
@@ -1008,7 +1010,9 @@ void EmbeddedWorkerInstance::ReleaseProcess() {

   instance_host_receiver_.reset();
   devtools_proxy_.reset();
+  LOG(ERROR) << "before process_handle_.reset(),this:"<<this;
   process_handle_.reset();
+  LOG(ERROR) << "after process_handle_.reset()";
   subresource_loader_updater_.reset();
   coep_reporter_.reset();
   status_ = blink::EmbeddedWorkerStatus::kStopped;
diff --git a/content/browser/service_worker/service_worker_registration.cc b/content/browser/service_worker/service_worker_registration.cc
index 65c2ee02fd6dc..ec8e8001c1fd6 100644
--- a/content/browser/service_worker/service_worker_registration.cc
+++ b/content/browser/service_worker/service_worker_registration.cc
@@ -99,6 +99,7 @@ ServiceWorkerRegistration::~ServiceWorkerRegistration() {
          "version";
   if (context_)
     context_->RemoveLiveRegistration(registration_id_);
+  LOG(ERROR)<< "ServiceWorkerRegistration::~ServiceWorkerRegistration(),active_version_:" << active_version_ << ",waiting_version_:" << waiting_version_ << ",installing_version_:" << installing_version_;
 }

 void ServiceWorkerRegistration::SetStatus(Status status) {
diff --git a/content/browser/service_worker/service_worker_version.cc b/content/browser/service_worker/service_worker_version.cc
index 768b73de45015..9a7d7fda9764b 100644
--- a/content/browser/service_worker/service_worker_version.cc
+++ b/content/browser/service_worker/service_worker_version.cc
@@ -65,7 +65,6 @@
 #include "third_party/blink/public/common/service_worker/service_worker_type_converters.h"
 #include "third_party/blink/public/common/storage_key/storage_key.h"
 #include "third_party/blink/public/mojom/service_worker/service_worker.mojom.h"
-
 namespace content {
 namespace {

@@ -363,6 +362,7 @@ ServiceWorkerVersion::~ServiceWorkerVersion() {
     context_->RemoveLiveVersion(version_id_);

   embedded_worker_->RemoveObserver(this);
+  LOG(ERROR)<< "~ServiceWorkerVersion(),this:"<<this<<",embedded_worker_:"<<embedded_worker_.get();
 }

 void ServiceWorkerVersion::SetNavigationPreloadState(

The log info as follow:
pwn11@pwn11:~/Desktop$ ~/chromium/src/out/release/chrome --disable-gpu --user-data-dir=/tmp/abxx http://localhost:8605/crash.html
```
[462307:462307:0703/140901.742104:ERROR:embedded_worker_instance.cc(707)] EmbeddedWorkerInstance::OnStopped(),this:0x5130001e3200
[462307:462307:0703/140901.742158:ERROR:embedded_worker_instance.cc(1000)] EmbeddedWorkerInstance::ReleaseProcess(),this:0x5130001e3200
[462307:462307:0703/140901.742420:ERROR:embedded_worker_instance.cc(1013)] before process_handle_.reset(),this:0x5130001e3200
[462307:462307:0703/140901.783922:ERROR:service_worker_registration.cc(102)]   ServiceWorkerRegistration::~ServiceWorkerRegistration(),active_version_:0x51d0000bea80,waiting_version_:(nil),installing_version_:(nil)       
[462307:462307:0703/140901.784105:ERROR:service_worker_version.cc(365)] ~ServiceWorkerVersion(),this:0x51d0000bea80,embedded_worker_:0x5130001e3200
[462307:462307:0703/140901.784806:ERROR:embedded_worker_instance.cc(226)] EmbeddedWorkerInstance::~EmbeddedWorkerInstance,this:0x5130001e3200
[462307:462307:0703/140901.784847:ERROR:embedded_worker_instance.cc(1000)] EmbeddedWorkerInstance::ReleaseProcess(),this:0x5130001e3200
[462307:462307:0703/140901.784892:ERROR:embedded_worker_instance.cc(1013)] before process_handle_.reset(),this:0x5130001e3200
[462307:462307:0703/140901.784936:ERROR:embedded_worker_instance.cc(1015)] after process_handle_.reset()
[462307:462307:0703/140901.785766:ERROR:embedded_worker_instance.cc(1015)] after process_handle_.reset()
=================================================================
==462307==ERROR: AddressSanitizer: heap-use-after-free on address 0x5130001e3338 at pc 0x6124b682f805 bp 0x7fffcf7c7c10 sp 0x7fffcf7c7c08
READ of size 8 at 0x5130001e3338 thread T0 (chrome)

### pe...@google.com (2024-07-03)

Thank you for providing more feedback. Adding the requester to the CC list.

### em...@gmail.com (2024-07-03)

Bisect:
This issue started from the change of https://chromium-review.googlesource.com/c/chromium/src/+/5549004.

### da...@chromium.org (2024-07-03)

Thanks for the bisect. Without a reliable repro I don't think it's fair to call this S0, so I will downgrade it.

### da...@chromium.org (2024-07-03)

hiroshige@ are you able to make sense of the ASAN crash stacks above and understand how this might be happening?

### em...@gmail.com (2024-07-03)

The repro steps I mentioned earlier were slightly incorrect. The issue can be reproduced on the first attempt with approximately 80% probability without needing to reopen the browser. The only scenario where it doesn't reproduce is when EmbeddedWorkerInstance::OnStopped() is not triggered. Could you please check if this function is being triggered?

Before CL[1], the EmbeddedWorkerInstance could be destroyed when ServiceWorkerRegistrationObjectManager::RemoveHost() is triggered. The call chain is as follows:
```
ServiceWorkerRegistrationObjectManager::RemoveHost()
>> content::ServiceWorkerRegistrationObjectHost::~ServiceWorkerRegistrationObjectHost()
>> content::ServiceWorkerRegistration::~ServiceWorkerRegistration()
>> EmbeddedWorkerInstance::~EmbeddedWorkerInstance()
```
However, after CL[1], it is possible that only the reference count of ServiceWorkerRegistration is decremented when RemoveHost() is triggered. The EmbeddedWorkerInstance is released after EmbeddedWorkerInstance::OnStopped() is triggered, which can lead to a UAF.
The new call chain is as follows:
```
ServiceWorkerRegistrationObjectManager::RemoveHost()
>> content::ServiceWorkerRegistrationObjectHost::~ServiceWorkerRegistrationObjectHost()
>> content::EmbeddedWorkerInstance::OnStopped()
>> content::EmbeddedWorkerInstance::ReleaseProcess()
>> process_handle_.reset()   <---[4]
>> ScopedServiceWorkerClient::~ScopedServiceWorkerClient() 
>> ServiceWorkerClient::RemoveAllMatchingRegistrations()  <---[3]Since the reference count of ServiceWorkerRegistration is already 1, ServiceWorkerRegistration will be released.
>> content::ServiceWorkerRegistration::~ServiceWorkerRegistration()
>> EmbeddedWorkerInstance::~EmbeddedWorkerInstance()
>> subresource_loader_updater_.reset()   <---[5] trigger UAF 
```
[0]https://source.chromium.org/chromium/chromium/src/+/main:content/browser/service_worker/embedded_worker_instance.cc;drc=9cae81d88d6a428544c2f39c8944fad64663515e;l=706

[1]https://chromium-review.googlesource.com/c/chromium/src/+/5549004

[2]https://source.chromium.org/chromium/chromium/src/+/main:content/browser/service_worker/service_worker_container_host.cc;drc=10186fca3889b383682f57fac8f7074b59ca8caf;l=943

[3]https://source.chromium.org/chromium/chromium/src/+/main:content/browser/service_worker/service_worker_container_host.cc;drc=10186fca3889b383682f57fac8f7074b59ca8caf;l=1564

[4]https://source.chromium.org/chromium/chromium/src/+/main:content/browser/service_worker/embedded_worker_instance.cc;drc=9cae81d88d6a428544c2f39c8944fad64663515e;l=1011

[5]https://source.chromium.org/chromium/chromium/src/+/main:content/browser/service_worker/embedded_worker_instance.cc;drc=9cae81d88d6a428544c2f39c8944fad64663515e;l=1012


### da...@chromium.org (2024-07-03)

From the bisect this would be in m128 only.

### da...@chromium.org (2024-07-03)

Thank you so much for the additional analysis. Also I realized that I had failed to get the crash at step 3, so I assumed I was not reproducing. When I closed the browser and restarted at the same URL and same user-data-dir, then it did crash eventually while sitting there.

```
=================================================================
==1101805==ERROR: AddressSanitizer: heap-use-after-free on address 0x51300020c1b8 at pc 0x558cef7bff67 bp 0x7ffc007d6290 sp 0x7ffc007d6288
READ of size 8 at 0x51300020c1b8 thread T0 (chrome)
==1101805==WARNING: invalid path to external symbolizer!
==1101805==WARNING: Failed to use and restart external symbolizer!
    #0 0x558cef7bff66 in swap<blink::mojom::SubresourceLoaderUpdaterProxy *> ./../../third_party/libc++/src/include/__utility/swap.h:43:9
    #1 0x558cef7bff66 in swap ./../../third_party/libc++/src/include/__memory/compressed_pair.h:155:5
    #2 0x558cef7bff66 in swap ./../../third_party/libc++/src/include/__memory/unique_ptr.h:281:101
    #3 0x558cef7bff66 in swap<blink::mojom::SubresourceLoaderUpdaterProxy, std::__Cr::default_delete<blink::mojom::SubresourceLoaderUpdaterProxy>, 0> ./../../third_party/libc++/src/include/__memory/unique_ptr.h:477:7
    #4 0x558cef7bff66 in Swap ./../../mojo/public/cpp/bindings/lib/interface_ptr_state.h:194:5
    #5 0x558cef7bff66 in reset ./../../mojo/public/cpp/bindings/remote.h:216:21
    #6 0x558cef7bff66 in content::EmbeddedWorkerInstance::ReleaseProcess() ./../../content/browser/service_worker/embedded_worker_instance.cc:1012:31
    #7 0x558cef7cfa2f in content::EmbeddedWorkerInstance::OnStopped() ./../../content/browser/service_worker/embedded_worker_instance.cc:709:3
    #8 0x558ce89094f5 in blink::mojom::EmbeddedWorkerInstanceHostStubDispatch::Accept(blink::mojom::EmbeddedWorkerInstanceHost*, mojo::Message*) ./gen/third_party/blink/public/mojom/service_worker/embedded_worker.mojom.cc:0:0
    #9 0x558cf96c77f3 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1036:54
    #10 0x558cf96e4058 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #11 0x558cf96ccc95 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:721:20
    #12 0x558cf96f1c5d in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:1120:42
    #13 0x558cf96efa6c in mojo::internal::MultiplexRouter::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:733:7
    #14 0x558cf96e4058 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #15 0x558cf96be86a in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) ./../../mojo/public/cpp/bindings/lib/connector.cc:562:49
    #16 0x558cf96c0475 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:620:14
    #17 0x558cf96bfe59 in OnHandleReadyInternal ./../../mojo/public/cpp/bindings/lib/connector.cc:452:3
    #18 0x558cf96bfe59 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int) ./../../mojo/public/cpp/bindings/lib/connector.cc:418:3
    #19 0x558cf96c1856 in Invoke<void (mojo::Connector::*)(const char *, unsigned int), mojo::Connector *, const char *, unsigned int> ./../../base/functional/bind_internal.h:738:12
    #20 0x558cf96c1856 in MakeItSo<void (mojo::Connector::*const &)(const char *, unsigned int), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, unsigned int> ./../../base/functional/bind_internal.h:930:12
    #21 0x558cf96c1856 in RunImpl<void (mojo::Connector::*const &)(const char *, unsigned int), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, 0UL, 1UL> ./../../base/functional/bind_internal.h:1067:14
    #22 0x558cf96c1856 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int) ./../../base/functional/bind_internal.h:987:12
    #23 0x558ce8f413d3 in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & ./../../base/functional/callback.h:344:12
    #24 0x558ce8f41154 in Invoke<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind_internal.h:671:12
    #25 0x558ce8f41154 in MakeItSo<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind_internal.h:930:12
    #26 0x558ce8f41154 in RunImpl<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, 0UL> ./../../base/functional/bind_internal.h:1067:14
    #27 0x558ce8f41154 in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) ./../../base/functional/bind_internal.h:987:12
    #28 0x558cf97501db in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & ./../../base/functional/callback.h:344:12
    #29 0x558cf974fb05 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple_watcher.cc:278:14
    #30 0x558cf9750d98 in Invoke<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), const base::WeakPtr<mojo::SimpleWatcher> &, int, unsigned int, mojo::HandleSignalsState> ./../../base/functional/bind_internal.h:738:12
    #31 0x558cf9750d98 in MakeItSo<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> > ./../../base/functional/bind_internal.h:954:5
    #32 0x558cf9750d98 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>) ./../../base/functional/bind_internal.h:1067:14
    #33 0x558cf7d854f4 in Run ./../../base/functional/callback.h:156:12
    #34 0x558cf7d854f4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:203:34
    #35 0x558cf7deef9a in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:486:11)> ./../../base/task/common/task_annotator.h:90:5
    #36 0x558cf7deef9a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:484:23
    #37 0x558cf7ded951 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #38 0x558cf7defcfa in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #39 0x558cf7f66682 in base::MessagePumpGlib::HandleDispatch() ./../../base/message_loop/message_pump_glib.cc:649:46
    #40 0x558cf7f699e8 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) ./../../base/message_loop/message_pump_glib.cc:274:43
    #41 0x7fbb74c201f3 in g_clear_list ??:?

0x51300020c1b8 is located 312 bytes inside of 368-byte region [0x51300020c080,0x51300020c1f0)
freed by thread T0 (chrome) here:
    #0 0x558ce3ae34ad in operator delete(void*) _asan_rtl_:3
    #1 0x558cefa5f388 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:67:5
    #2 0x558cefa5f388 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:278:7
    #3 0x558cefa5f388 in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:248:71
    #4 0x558cefa5f388 in content::ServiceWorkerVersion::~ServiceWorkerVersion() ./../../content/browser/service_worker/service_worker_version.cc:366:1
    #5 0x558cefa5f713 in content::ServiceWorkerVersion::~ServiceWorkerVersion() ./../../content/browser/service_worker/service_worker_version.cc:341:47
    #6 0x558cef996871 in DeleteInternal<content::ServiceWorkerVersion> ./../../base/memory/ref_counted.h:365:5
    #7 0x558cef996871 in Destruct ./../../base/memory/ref_counted.h:329:5
    #8 0x558cef996871 in Release ./../../base/memory/ref_counted.h:354:7
    #9 0x558cef996871 in Release ./../../base/memory/scoped_refptr.h:384:8
    #10 0x558cef996871 in ~scoped_refptr ./../../base/memory/scoped_refptr.h:273:7
    #11 0x558cef996871 in content::ServiceWorkerRegistration::~ServiceWorkerRegistration() ./../../content/browser/service_worker/service_worker_registration.cc:102:1
    #12 0x558cef996b83 in content::ServiceWorkerRegistration::~ServiceWorkerRegistration() ./../../content/browser/service_worker/service_worker_registration.cc:92:57
    #13 0x558cef83bdaf in DeleteInternal<content::ServiceWorkerRegistration> ./../../base/memory/ref_counted.h:365:5
    #14 0x558cef83bdaf in Destruct ./../../base/memory/ref_counted.h:329:5
    #15 0x558cef83bdaf in Release ./../../base/memory/ref_counted.h:354:7
    #16 0x558cef83bdaf in Release ./../../base/memory/scoped_refptr.h:384:8
    #17 0x558cef83bdaf in ~scoped_refptr ./../../base/memory/scoped_refptr.h:273:7
    #18 0x558cef83bdaf in ~pair ./../../third_party/libc++/src/include/__utility/pair.h:64:29
    #19 0x558cef83bdaf in __destroy_at<std::__Cr::pair<const unsigned long, scoped_refptr<content::ServiceWorkerRegistration> >, 0> ./../../third_party/libc++/src/include/__memory/construct_at.h:67:11
    #20 0x558cef83bdaf in destroy<std::__Cr::pair<const unsigned long, scoped_refptr<content::ServiceWorkerRegistration> >, void, 0> ./../../third_party/libc++/src/include/__memory/allocator_traits.h:339:5
    #21 0x558cef83bdaf in std::__Cr::__tree<std::__Cr::__value_type<unsigned long, scoped_refptr<content::ServiceWorkerRegistration>>, std::__Cr::__map_value_compare<unsigned long, std::__Cr::__value_type<unsigned long, scoped_refptr<content::ServiceWorkerRegistration>>, std::__Cr::less<unsigned long>, true>, std::__Cr::allocator<std::__Cr::__value_type<unsigned long, scoped_refptr<content::ServiceWorkerRegistration>>>>::destroy(std::__Cr::__tree_node<std::__Cr::__value_type<unsigned long, scoped_refptr<content::ServiceWorkerRegistration>>, void*>*) ./../../third_party/libc++/src/include/__tree:1541:5
    #22 0x558cef8040f6 in clear ./../../third_party/libc++/src/include/__tree:1572:3
    #23 0x558cef8040f6 in clear ./../../third_party/libc++/src/include/map:1315:58
    #24 0x558cef8040f6 in RemoveAllMatchingRegistrations ./../../content/browser/service_worker/service_worker_container_host.cc:1552:27
    #25 0x558cef8040f6 in content::ServiceWorkerClient::~ServiceWorkerClient() ./../../content/browser/service_worker/service_worker_container_host.cc:208:3
    #26 0x558cef86fc2d in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:67:5
    #27 0x558cef86fc2d in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:278:7
    #28 0x558cef86fc2d in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:248:71
    #29 0x558cef86fc2d in ~pair ./../../third_party/libc++/src/include/__utility/pair.h:64:29
    #30 0x558cef86fc2d in void std::__Cr::__destroy_at<std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const, std::__Cr::unique_ptr<content::ServiceWorkerClient, std::__Cr::default_delete<content::ServiceWorkerClient>>>, 0>(std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const, std::__Cr::unique_ptr<content::ServiceWorkerClient, std::__Cr::default_delete<content::ServiceWorkerClient>>>*) ./../../third_party/libc++/src/include/__memory/construct_at.h:67:11
    #31 0x558cef873279 in destroy<std::__Cr::pair<const std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >, std::__Cr::unique_ptr<content::ServiceWorkerClient, std::__Cr::default_delete<content::ServiceWorkerClient> > >, void, 0> ./../../third_party/libc++/src/include/__memory/allocator_traits.h:339:5
    #32 0x558cef873279 in erase ./../../third_party/libc++/src/include/__tree:2043:3
    #33 0x558cef873279 in unsigned long std::__Cr::__tree<std::__Cr::__value_type<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::unique_ptr<content::ServiceWorkerClient, std::__Cr::default_delete<content::ServiceWorkerClient>>>, std::__Cr::__map_value_compare<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::__value_type<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::unique_ptr<content::ServiceWorkerClient, std::__Cr::default_delete<content::ServiceWorkerClient>>>, std::__Cr::less<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>, true>, std::__Cr::allocator<std::__Cr::__value_type<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::unique_ptr<content::ServiceWorkerClient, std::__Cr::default_delete<content::ServiceWorkerClient>>>>>::__erase_unique<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&) ./../../third_party/libc++/src/include/__tree:2063:3
    #34 0x558cef84bd87 in erase ./../../third_party/libc++/src/include/map:1311:79
    #35 0x558cef84bd87 in content::ServiceWorkerClientOwner::DestroyServiceWorkerClient(base::WeakPtr<content::ServiceWorkerClient>) ./../../content/browser/service_worker/service_worker_context_core.cc:525:52
    #36 0x558cef867951 in content::ScopedServiceWorkerClient::~ScopedServiceWorkerClient() ./../../content/browser/service_worker/service_worker_context_core.cc:1393:35
    #37 0x558cef92691b in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:67:5
    #38 0x558cef92691b in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:278:7
    #39 0x558cef92691b in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:248:71
    #40 0x558cef92691b in content::ServiceWorkerMainResourceHandle::~ServiceWorkerMainResourceHandle() ./../../content/browser/service_worker/service_worker_main_resource_handle.cc:29:67
    #41 0x558ceff49a05 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:67:5
    #42 0x558ceff49a05 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:278:7
    #43 0x558ceff49a05 in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:248:71
    #44 0x558ceff49a05 in content::DedicatedWorkerHost::~DedicatedWorkerHost() ./../../content/browser/worker_host/dedicated_worker_host.cc:159:1
    #45 0x558ceff4a892 in RenderProcessExited ./../../content/browser/worker_host/dedicated_worker_host.cc:194:3
    #46 0x558ceff4a892 in non-virtual thunk to content::DedicatedWorkerHost::RenderProcessExited(content::RenderProcessHost*, content::ChildProcessTerminationInfo const&) ./../../content/browser/worker_host/dedicated_worker_host.cc:0:0
    #47 0x558cef64ec12 in content::RenderProcessHostImpl::Cleanup() ./../../content/browser/renderer_host/render_process_host_impl.cc:3878:16
    #48 0x558cef63f00b in content::RenderProcessHostImpl::DecrementWorkerRefCount() ./../../content/browser/renderer_host/render_process_host_impl.cc:2543:5
    #49 0x558cef97ec72 in content::ServiceWorkerProcessManager::ReleaseWorkerProcess(int) ./../../content/browser/service_worker/service_worker_process_manager.cc:195:16
    #50 0x558cef7d7202 in content::EmbeddedWorkerInstance::WorkerProcessHandle::~WorkerProcessHandle() ./../../content/browser/service_worker/embedded_worker_instance.cc:196:23
    #51 0x558cef7bfcba in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:67:5
    #52 0x558cef7bfcba in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:278:7
    #53 0x558cef7bfcba in content::EmbeddedWorkerInstance::ReleaseProcess() ./../../content/browser/service_worker/embedded_worker_instance.cc:1011:19
    #54 0x558cef7cfa2f in content::EmbeddedWorkerInstance::OnStopped() ./../../content/browser/service_worker/embedded_worker_instance.cc:709:3
    #55 0x558ce89094f5 in blink::mojom::EmbeddedWorkerInstanceHostStubDispatch::Accept(blink::mojom::EmbeddedWorkerInstanceHost*, mojo::Message*) ./gen/third_party/blink/public/mojom/service_worker/embedded_worker.mojom.cc:0:0
    #56 0x558cf96c77f3 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1036:54
    #57 0x558cf96e4058 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #58 0x558cf96ccc95 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:721:20
    #59 0x558cf96f1c5d in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:1120:42
    #60 0x558cf96efa6c in mojo::internal::MultiplexRouter::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:733:7
    #61 0x558cf96e4058 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #62 0x558cf96be86a in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) ./../../mojo/public/cpp/bindings/lib/connector.cc:562:49
    #63 0x558cf96c0475 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:620:14
    #64 0x558cf96bfe59 in OnHandleReadyInternal ./../../mojo/public/cpp/bindings/lib/connector.cc:452:3
    #65 0x558cf96bfe59 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int) ./../../mojo/public/cpp/bindings/lib/connector.cc:418:3

previously allocated by thread T0 (chrome) here:
    #0 0x558ce3ae2c4d in operator new(unsigned long) _asan_rtl_:3
    #1 0x558cefa5db4f in make_unique<content::EmbeddedWorkerInstance, content::ServiceWorkerVersion *> ./../../third_party/libc++/src/include/__memory/unique_ptr.h:620:26
    #2 0x558cefa5db4f in content::ServiceWorkerVersion::ServiceWorkerVersion(content::ServiceWorkerRegistration*, GURL const&, blink::mojom::ScriptType, long, mojo::PendingRemote<storage::mojom::ServiceWorkerLiveVersionRef>, base::WeakPtr<content::ServiceWorkerContextCore>) ./../../content/browser/service_worker/service_worker_version.cc:336:22
    #3 0x558cef9e2f53 in scoped_refptr<content::ServiceWorkerVersion> base::MakeRefCounted<content::ServiceWorkerVersion, content::ServiceWorkerRegistration*, GURL const&, blink::mojom::ScriptType const&, long const&, mojo::PendingRemote<storage::mojom::ServiceWorkerLiveVersionRef>, base::WeakPtr<content::ServiceWorkerContextCore>>(content::ServiceWorkerRegistration*&&, GURL const&, blink::mojom::ScriptType const&, long const&, mojo::PendingRemote<storage::mojom::ServiceWorkerLiveVersionRef>&&, base::WeakPtr<content::ServiceWorkerContextCore>&&) ./../../base/memory/scoped_refptr.h:150:16
    #4 0x558cef9e1d97 in content::ServiceWorkerRegistry::GetOrCreateRegistration(storage::mojom::ServiceWorkerRegistrationData const&, std::__Cr::vector<mojo::StructPtr<storage::mojom::ServiceWorkerResourceRecord>, std::__Cr::allocator<mojo::StructPtr<storage::mojom::ServiceWorkerResourceRecord>>> const&, mojo::PendingRemote<storage::mojom::ServiceWorkerLiveVersionRef>) ./../../content/browser/service_worker/service_worker_registry.cc:1101:15
    #5 0x558cef9be1d5 in content::ServiceWorkerRegistry::DidFindRegistrationForClientUrl(GURL const&, blink::StorageKey const&, long, base::OnceCallback<void (blink::ServiceWorkerStatusCode, scoped_refptr<content::ServiceWorkerRegistration>)>, storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&) ./../../content/browser/service_worker/service_worker_registry.cc:1250:9
    #6 0x558cef9edd2a in void base::internal::DecayedFunctorTraits<void (content::ServiceWorkerRegistry::*)(GURL const&, blink::StorageKey const&, long, base::OnceCallback<void (blink::ServiceWorkerStatusCode, scoped_refptr<content::ServiceWorkerRegistration>)>, storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&), base::WeakPtr<content::ServiceWorkerRegistry>&&, GURL&&, blink::StorageKey&&, long&&, base::internal::DoNothingCallbackTag&&>::Invoke<void (content::ServiceWorkerRegistry::*)(GURL const&, blink::StorageKey const&, long, base::OnceCallback<void (blink::ServiceWorkerStatusCode, scoped_refptr<content::ServiceWorkerRegistration>)>, storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&), base::WeakPtr<content::ServiceWorkerRegistry> const&, GURL, blink::StorageKey, long, base::internal::DoNothingCallbackTag, storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&>(void (content::ServiceWorkerRegistry::*)(GURL const&, blink::StorageKey const&, long, base::OnceCallback<void (blink::ServiceWorkerStatusCode, scoped_refptr<content::ServiceWorkerRegistration>)>, storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&), base::WeakPtr<content::ServiceWorkerRegistry> const&, GURL&&, blink::StorageKey&&, long&&, base::internal::DoNothingCallbackTag&&, storage::mojom::ServiceWorkerDatabaseStatus&&, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>&&, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&) ./../../base/functional/bind_internal.h:738:12
    #7 0x558cef9ed9b5 in MakeItSo<void (content::ServiceWorkerRegistry::*)(const GURL &, const blink::StorageKey &, long, base::OnceCallback<void (blink::ServiceWorkerStatusCode, scoped_refptr<content::ServiceWorkerRegistration>)>, storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, const std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL> > > &), std::__Cr::tuple<base::WeakPtr<content::ServiceWorkerRegistry>, GURL, blink::StorageKey, long, base::internal::DoNothingCallbackTag>, storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, const std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL> > > &> ./../../base/functional/bind_internal.h:954:5
    #8 0x558cef9ed9b5 in RunImpl<void (content::ServiceWorkerRegistry::*)(const GURL &, const blink::StorageKey &, long, base::OnceCallback<void (blink::ServiceWorkerStatusCode, scoped_refptr<content::ServiceWorkerRegistration>)>, storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, const std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL> > > &), std::__Cr::tuple<base::WeakPtr<content::ServiceWorkerRegistry>, GURL, blink::StorageKey, long, base::internal::DoNothingCallbackTag>, 0UL, 1UL, 2UL, 3UL, 4UL> ./../../base/functional/bind_internal.h:1067:14
    #9 0x558cef9ed9b5 in base::internal::Invoker<base::internal::FunctorTraits<void (content::ServiceWorkerRegistry::*&&)(GURL const&, blink::StorageKey const&, long, base::OnceCallback<void (blink::ServiceWorkerStatusCode, scoped_refptr<content::ServiceWorkerRegistration>)>, storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&), base::WeakPtr<content::ServiceWorkerRegistry>&&, GURL&&, blink::StorageKey&&, long&&, base::internal::DoNothingCallbackTag&&>, base::internal::BindState<true, true, false, void (content::ServiceWorkerRegistry::*)(GURL const&, blink::StorageKey const&, long, base::OnceCallback<void (blink::ServiceWorkerStatusCode, scoped_refptr<content::ServiceWorkerRegistration>)>, storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&), base::WeakPtr<content::ServiceWorkerRegistry>, GURL, blink::StorageKey, long, base::internal::DoNothingCallbackTag>, void (storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&)>::RunOnce(base::internal::BindStateBase*, storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>&&, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&) ./../../base/functional/bind_internal.h:980:12
    #10 0x558cefa01283 in Run ./../../base/functional/callback.h:156:12
    #11 0x558cefa01283 in content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&>::DidReply(storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&) ./../../content/browser/service_worker/service_worker_registry.cc:233:31
    #12 0x558cefa016e2 in Invoke<void (content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, const std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL> > > &>::*)(storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, const std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL> > > &), content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, const std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL> > > &> *, storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, const std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL> > > &> ./../../base/functional/bind_internal.h:738:12
    #13 0x558cefa016e2 in MakeItSo<void (content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, const std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL> > > &>::*)(storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, const std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL> > > &), std::__Cr::tuple<base::internal::UnretainedWrapper<content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, const std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL> > > &>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, const std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL> > > &> ./../../base/functional/bind_internal.h:930:12
    #14 0x558cefa016e2 in void base::internal::Invoker<base::internal::FunctorTraits<void (content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&>::*&&)(storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&), content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&>*>, base::internal::BindState<true, true, false, void (content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&>::*)(storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&), base::internal::UnretainedWrapper<content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&)>::RunImpl<void (content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&>::*)(storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&), std::__Cr::tuple<base::internal::UnretainedWrapper<content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(void (content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&>::*&&)(storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&), std::__Cr::tuple<base::internal::UnretainedWrapper<content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>, storage::mojom::ServiceWorkerDatabaseStatus&&, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>&&, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&) ./../../base/functional/bind_internal.h:1067:14
    #15 0x558cefa01467 in base::internal::Invoker<base::internal::FunctorTraits<void (content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&>::*&&)(storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&), content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&>*>, base::internal::BindState<true, true, false, void (content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&>::*)(storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&), base::internal::UnretainedWrapper<content::InflightCallWithInvoker<storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&)>::RunOnce(base::internal::BindStateBase*, storage::mojom::ServiceWorkerDatabaseStatus, mojo::StructPtr<storage::mojom::ServiceWorkerFindRegistrationResult>&&, std::__Cr::optional<std::__Cr::vector<GURL, std::__Cr::allocator<GURL>>> const&) ./../../base/functional/bind_internal.h:980:12
    #16 0x558ce9093684 in Run ./../../base/functional/callback.h:156:12
    #17 0x558ce9093684 in storage::mojom::ServiceWorkerStorageControl_FindRegistrationForClientUrl_ForwardToCallback::Accept(mojo::Message*) ./gen/components/services/storage/public/mojom/service_worker_storage_control.mojom.cc:6191:26
    #18 0x558cf96c7bed in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1031:41
    #19 0x558cf96e4058 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #20 0x558cf96ccc95 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:721:20
    #21 0x558cf96f1c5d in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:1120:42
    #22 0x558cf96efa6c in mojo::internal::MultiplexRouter::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:733:7
    #23 0x558cf96e4058 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #24 0x558cf96be86a in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) ./../../mojo/public/cpp/bindings/lib/connector.cc:562:49
    #25 0x558cf96c0475 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:620:14
    #26 0x558cf96c0ef5 in Invoke<void (mojo::Connector::*)(), const base::WeakPtr<mojo::Connector> &> ./../../base/functional/bind_internal.h:738:12
    #27 0x558cf96c0ef5 in MakeItSo<void (mojo::Connector::*)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector> > > ./../../base/functional/bind_internal.h:954:5
    #28 0x558cf96c0ef5 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::*&&)(), base::WeakPtr<mojo::Connector>&&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector>>, void ()>::RunImpl<void (mojo::Connector::*)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector>>, 0ul>(void (mojo::Connector::*&&)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) ./../../base/functional/bind_internal.h:1067:14
    #29 0x558cf7d854f4 in Run ./../../base/functional/callback.h:156:12
    #30 0x558cf7d854f4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:203:34
    #31 0x558cf7deef9a in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:486:11)> ./../../base/task/common/task_annotator.h:90:5
    #32 0x558cf7deef9a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:484:23
    #33 0x558cf7ded951 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #34 0x558cf7defcfa in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #35 0x558cf7f67170 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_glib.cc:694:48
    #36 0x558cf7df096b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:654:12
    #37 0x558cf7d10a8f in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #38 0x558cee208331 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser_main_loop.cc:1085:18
    #39 0x558cee20fe0c in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser_main_runner_impl.cc:159:15
    #40 0x558cee1fea08 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser_main.cc:34:28

SUMMARY: AddressSanitizer: heap-use-after-free (/home/danakj/asan-stable/chrome+0x1bd18f66) (BuildId: 756c1330f989c7ba)
Shadow bytes around the buggy address:
  0x51300020bf00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x51300020bf80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x51300020c000: fd fd fd fd fd fa fa fa fa fa fa fa fa fa f7 fa
  0x51300020c080: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x51300020c100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x51300020c180: fd fd fd fd fd fd fd[fd]fd fd fd fd fd fd fa fa
  0x51300020c200: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x51300020c280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x51300020c300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x51300020c380: fd fd fd fd fa fa fa fa fa fa fa fa fa fa f7 fa
  0x51300020c400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==1101805==ADDITIONAL INFO

==1101805==Note: Please include this section with the ASan report.
Task trace:
    #0 0x558cf9750711 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) ./../../mojo/public/cpp/system/simple_watcher.cc:102:13


Command line: `./chrome --disable-gpu --user-data-dir=user --no-first-run --flag-switches-begin --flag-switches-end --file-url-path-alias=/gen=/home/danakj/asan-stable/gen http://localhost:8000/crash.html`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==1101805==END OF ADDITIONAL INFO
==1101805==ABORTING

```

### da...@chromium.org (2024-07-03)

The crash requires a renderer process shutdown, but the memory corruption comes later and is under much greater control of the attacker. I think this bumps back up to S0. Luckily it is only in the dev channel so far.

### pe...@google.com (2024-07-04)

Setting milestone because of s0/s1 severity.

### da...@chromium.org (2024-07-04)

hiroshige@ appears to be OOO, could one of the reviewers of <https://chromium-review.googlesource.com/c/chromium/src/+/5549004> have a look please?

### wf...@chromium.org (2024-07-09)

[security shepherd] Hello! This is P0/S0. Please revert <https://chromium-review.googlesource.com/c/chromium/src/+/5549004> or land a fix in the next 24 hours.

### nh...@chromium.org (2024-07-09)

hiroshige@ is investigating this.

### nh...@chromium.org (2024-07-09)

The crash stack includes DedicatedWorkerHost. This implies `kPlzDedicatedWorker` is enabled on crashed clients. This feature is now enabled through field trials. This could be the cause of the flakiness on repro.

### nh...@chromium.org (2024-07-09)

```
void EmbeddedWorkerInstance::ReleaseProcess() {
  // ...
  process_handle_.reset();  // <-- Destructs `this`
  subresource_loader_updater_.reset();  // <-- Crash!!

```

We may have to do this !dtor-protect pattern...

```
void ServiceWorkerVersion::OnStoppedInternal(
    blink::EmbeddedWorkerStatus old_status) {
  TRACE_EVENT0("ServiceWorker", "ServiceWorkerVersion::OnStoppedInternal");
  DCHECK_EQ(blink::EmbeddedWorkerStatus::kStopped, running_status());
  scoped_refptr<ServiceWorkerVersion> protect;
  if (!in_dtor_)
    protect = this;

```

### nh...@chromium.org (2024-07-09)

Unfortunately I cannot reproduce the issue on Chrome ASAN Linux.

hiroshige@ is now making a fix.

### hi...@google.com (2024-07-09)

Fix: https://chromium-review.googlesource.com/c/chromium/src/+/5685760

The crash starts occuring in this path after https://chromium-review.googlesource.com/c/chromium/src/+/5549004 because `ScopedServiceWorkerClient` destructs `ServiceWorkerClient` in its destructor synchronously (as mentioned in the commit message).
However, probably the root cause (of not protecting `this` during `ReleaseProcess()`) has been existing since before.

Ideally we can set a clearer destruction timing design around ServiceWorkerVersion that avoid such kind of UaF, but we don't have any immediate plan/design for that, so adding further "protect this" pattern in the fix CL.

### hi...@chromium.org (2024-07-11)

The fix <https://chromium-review.googlesource.com/c/chromium/src/+/5685760> has landed on 128.0.6586.0.

Could someone (the reporter or danakj) check if the UaF is fixed? (as I nor nhiroki couldn't reproduce locally)

### em...@gmail.com (2024-07-11)

I have confirmed that the UaF issue could not be reproduced after applying the patch 

### em...@gmail.com (2024-07-12)

I have also just downloaded and tested the latest version 128.0.6591.0, and as expected, the issue did not repro.

Chromium 128.0.6591.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1326524.zip)

### hi...@chromium.org (2024-07-12)

Thank for confirmation!

Closing as Fixed.

Requesting merging <https://chromium-review.googlesource.com/c/chromium/src/+/5685760> to M-127.

The direct regressing CL <https://chromium-review.googlesource.com/c/chromium/src/+/5549004> was on M-128, but I suspect the root cause has existed since before:
Crash Query:
expanded\_custom\_data.ChromeCrashProto.magic\_signature\_1.name='content::EmbeddedWorkerInstance::ReleaseProcess'
Example crash report ID at the same code location: 11e15655e6a91f2a
Also [Comment #24](https://issues.chromium.org/issues/350407902#comment24)

So I feel it's safer to merge the fix speculatively to M-127.

### pe...@google.com (2024-07-12)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), alonbajayo (ChromeOS), danielyip (Desktop)

### hi...@chromium.org (2024-07-12)

1. Why does your merge fit within the merge criteria for these milestones?

Security fix.
The POC is only applicable to M-128 so the severity might be lower than P0/S0 on M-127, but still potential UaF exists on M-127.

2. What changes specifically would you like to merge? Please link to Gerrit.

<https://chromium-review.googlesource.com/c/chromium/src/+/5685760>

3. Have the changes been released and tested on canary?

Yes ([Comment #27](https://issues.chromium.org/issues/350407902#comment27))

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No.

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No.

### am...@chromium.org (2024-07-12)

<https://crrev.com/c/5685760> approved for merge to M127; please merge this fix to branch 6533 by EOD Monday, 15 July so this fix can be included in M127 final beta being released next week and the M127 Stable RC being cut next week for release the following week

### da...@google.com (2024-07-15)

Reminder: M127 will be promoting to early stable this Wednesday, please ensure your changes land in the M127 branch by COP tomorrow to ensure that your changes are included in the release.

### am...@google.com (2024-07-16)

hiroshige@ -- please merge this fix to M127 / branch 6533 ASAP as M127 Stable RC is being cut tomorrow

### ap...@google.com (2024-07-16)

Project: chromium/src
Branch: refs/branch-heads/6533

commit 3fb1c3e3622f2608caf85fd74e487c8a4d9c1f72
Author: Hiroshige Hayashizaki <hiroshige@chromium.org>
Date:   Tue Jul 16 03:33:30 2024

    [Merge to M127] Protect ServiceWorkerVersion during ReleaseProcess
    
    This CL avoid use-after-free around
    `EmbeddedWorkerInstance::ReleaseProcess()`:
    
    1. During `ReleaseProcess()`:
    This CL protects `ServiceWorkerVersion` and its
    `EmbeddedWorkerInstance` from deletion.
    
    2. In the direct callers of `ReleaseProcess()`:
    This CL early returns if `this` is deleted during `ReleaseProcess()`.
    Skipping `listener_list_` should be fine because `listener_list_`
    is the `owner_version_` (at least in non-test) that is already
    deleted if `this` is deleted.
    This CL also adds explicit comments that the methods calling
    `ReleaseProcess()` may delete `this`.
    
    3. In the callers of 2.:
    As far as I checked, the callers should work even in the case of
    deletion of `ServiceWorkerVersion`.
    
    (cherry picked from commit 76ce1fe94c44257fd3d6480c6a54a5b58e3d6361)
    
    Bug: 350407902
    Change-Id: If59e8354ae9832009b62408a8f0058cb6f6e803f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5685760
    Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
    Commit-Queue: Hiroshige Hayashizaki <hiroshige@chromium.org>
    Reviewed-by: Hiroki Nakagawa <nhiroki@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1324689}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5709510
    Commit-Queue: Hiroki Nakagawa <nhiroki@chromium.org>
    Reviewed-by: Shunya Shishido <sisidovski@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6533@{#1513}
    Cr-Branched-From: 7e0b87ec6b8cb5cb2969e1479fc25776e582721d-refs/heads/main@{#1313161}

M       content/browser/service_worker/embedded_worker_instance.cc
M       content/browser/service_worker/embedded_worker_instance.h

https://chromium-review.googlesource.com/5709510


### pe...@google.com (2024-07-16)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### hi...@chromium.org (2024-07-16)

1. Was this issue a regression for the milestone it was found in?

No - the direct UaF code path was a regression on M-128 (and fixed on M-128), and the underlying cause has existed since before and probably not a recent regression. ([Comment #28](https://issues.chromium.org/issues/350407902#comment28))

2. Is this issue related to a change or feature merged after the latest LTS Milestone?

No.

### sp...@google.com (2024-07-17)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $21000.00 for this report.

Rationale for this decision:
$20,000 for report of memory corruption in a non-sandboxed process + $1,000 bisect bonus 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-17)

Congratulations Cassidy Kim! Thank you for your efforts and reporting this excellent find to us -- nice work!

### pe...@google.com (2024-07-30)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### rz...@google.com (2024-07-30)

1. <https://crrev.com/c/5740901>
2. Low, no conflicts
3. 127
4. Yes

### gm...@google.com (2024-07-30)

@rz...@google.com, I am going to reject the merge for LTS-120 since this was found in 128 and it is a lower priority for 127 per Comment#30.

### pe...@google.com (2024-08-07)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2024-09-04)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### rz...@google.com (2024-09-04)

1. <https://crrev.com/c/5806117> for 126, <https://crrev.com/c/5806117> for 120
2. Low, no conflicts for 126, simple conflict for 120
3. 127
4. Yes

### gm...@google.com (2024-09-04)

@rzanoni, approved for 126, rejected for 120.

### ap...@google.com (2024-09-11)

Project: chromium/src
Branch: refs/branch-heads/6478

commit 010ff578b6c0599508ea996c9266ab8931c7f861
Author: Hiroshige Hayashizaki <hiroshige@chromium.org>
Date:   Wed Sep 11 15:54:34 2024

    [M126-LTS] Protect ServiceWorkerVersion during ReleaseProcess
    
    This CL avoid use-after-free around
    `EmbeddedWorkerInstance::ReleaseProcess()`:
    
    1. During `ReleaseProcess()`:
    This CL protects `ServiceWorkerVersion` and its
    `EmbeddedWorkerInstance` from deletion.
    
    2. In the direct callers of `ReleaseProcess()`:
    This CL early returns if `this` is deleted during `ReleaseProcess()`.
    Skipping `listener_list_` should be fine because `listener_list_`
    is the `owner_version_` (at least in non-test) that is already
    deleted if `this` is deleted.
    This CL also adds explicit comments that the methods calling
    `ReleaseProcess()` may delete `this`.
    
    3. In the callers of 2.:
    As far as I checked, the callers should work even in the case of
    deletion of `ServiceWorkerVersion`.
    
    (cherry picked from commit 76ce1fe94c44257fd3d6480c6a54a5b58e3d6361)
    
    Bug: 350407902
    Change-Id: If59e8354ae9832009b62408a8f0058cb6f6e803f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5685760
    Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
    Commit-Queue: Hiroshige Hayashizaki <hiroshige@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1324689}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5806117
    Auto-Submit: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com>
    Reviewed-by: Hiroshige Hayashizaki <hiroshige@chromium.org>
    Reviewed-by: Shunya Shishido <sisidovski@chromium.org>
    Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com>
    Owners-Override: Artem Sumaneev <asumaneev@google.com>
    Reviewed-by: Artem Sumaneev <asumaneev@google.com>
    Cr-Commit-Position: refs/branch-heads/6478@{#1956}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       content/browser/service_worker/embedded_worker_instance.cc
M       content/browser/service_worker/embedded_worker_instance.h

https://chromium-review.googlesource.com/5806117


### ap...@google.com (2024-09-17)

Project: chromium/src
Branch: refs/branch-heads/6478_182

commit 0e73a41e78235124c1dba68cf0e57078778beaa4
Author: Hiroshige Hayashizaki <hiroshige@chromium.org>
Date:   Tue Sep 17 15:36:54 2024

    [CfM-R126] Protect ServiceWorkerVersion during ReleaseProcess
    
    This CL avoid use-after-free around
    `EmbeddedWorkerInstance::ReleaseProcess()`:
    
    1. During `ReleaseProcess()`:
    This CL protects `ServiceWorkerVersion` and its
    `EmbeddedWorkerInstance` from deletion.
    
    2. In the direct callers of `ReleaseProcess()`:
    This CL early returns if `this` is deleted during `ReleaseProcess()`.
    Skipping `listener_list_` should be fine because `listener_list_`
    is the `owner_version_` (at least in non-test) that is already
    deleted if `this` is deleted.
    This CL also adds explicit comments that the methods calling
    `ReleaseProcess()` may delete `this`.
    
    3. In the callers of 2.:
    As far as I checked, the callers should work even in the case of
    deletion of `ServiceWorkerVersion`.
    
    (cherry picked from commit 76ce1fe94c44257fd3d6480c6a54a5b58e3d6361)
    
    (cherry picked from commit 010ff578b6c0599508ea996c9266ab8931c7f861)
    
    Bug: 350407902
    Change-Id: If59e8354ae9832009b62408a8f0058cb6f6e803f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5685760
    Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
    Commit-Queue: Hiroshige Hayashizaki <hiroshige@chromium.org>
    Cr-Original-Original-Commit-Position: refs/heads/main@{#1324689}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5806117
    Auto-Submit: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com>
    Reviewed-by: Hiroshige Hayashizaki <hiroshige@chromium.org>
    Reviewed-by: Shunya Shishido <sisidovski@chromium.org>
    Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com>
    Owners-Override: Artem Sumaneev <asumaneev@google.com>
    Reviewed-by: Artem Sumaneev <asumaneev@google.com>
    Cr-Original-Commit-Position: refs/branch-heads/6478@{#1956}
    Cr-Original-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5869438
    Owners-Override: Kyle Williams <kdgwill@chromium.org>
    Reviewed-by: Niko Tsirakis <ntsirakis@google.com>
    Commit-Queue: Kyle Williams <kdgwill@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6478_182@{#72}
    Cr-Branched-From: 5b5d8292ddf182f8b2096fa665b473b6317906d5-refs/branch-heads/6478@{#1776}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       content/browser/service_worker/embedded_worker_instance.cc
M       content/browser/service_worker/embedded_worker_instance.h

https://chromium-review.googlesource.com/5869438


### pe...@google.com (2024-10-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### aq...@gmail.com (2024-10-20)

deleted

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/350407902)*
