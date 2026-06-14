# UAF in net::QuicChromiumClientSession::StreamRequest

| Field | Value |
|-------|-------|
| **Issue ID** | [327687950](https://issues.chromium.org/issues/327687950) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Network>QUIC |
| **Platforms** | Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | ba...@chromium.org |
| **Created** | 2024-03-01 |
| **Bounty** | $10,000.00 |

## Description

tested os:
-   ubuntu 22.04
tested chrome version:
-   stable & beta & dev

repro steps:
This issue can be reproduced in a single browser, but the probability of reproduction is relatively low. Therefore, I wrote a script to test in headless mode by opening multiple browsers simultaneously. On my local machine, the issue can be reproduced quite quickly.

Depending on the actual situation, it's necessary to modify the path and the number of browsers, as well as the --user-data-dir luanch flag.

/launcher.sh  2>&1 |grep -E 'heap-use'
==547540==ERROR: AddressSanitizer: heap-use-after-free on address 0x50800002abb0 at pc 0x5632a3af573a bp 0x7ff6ce5587d0 sp 0x7ff6ce5587c8
READ of size 8 at 0x50800002abb0 thread T23 (NetworkService)
    #0 0x5632a3af5739 in operator bool ./../../base/memory/scoped_refptr.h:311:43
    #1 0x5632a3af5739 in is_null ./../../base/functional/callback_internal.h:140:34
    #2 0x5632a3af5739 in operator bool ./../../base/functional/callback_internal.h:141:44
    #3 0x5632a3af5739 in operator bool ./../../base/functional/callback.h:111:45
    #4 0x5632a3af5739 in net::QuicChromiumClientSession::StreamRequest::OnRequestCompleteFailure(int) ./../../net/quic/quic_chromium_client_session.cc:627:7
    #5 0x5632a3afc61c in net::QuicChromiumClientSession::CancelAllRequests(int) ./../../net/quic/quic_chromium_client_session.cc:2878:14
    #6 0x5632a3afa7ff in net::QuicChromiumClientSession::~QuicChromiumClientSession() ./../../net/quic/quic_chromium_client_session.cc:1008:5
    #7 0x5632a3afcb23 in net::QuicChromiumClientSession::~QuicChromiumClientSession() ./../../net/quic/quic_chromium_client_session.cc:995:57
    #8 0x5632a3b6a0a6 in net::QuicSessionPool::OnSessionClosed(net::QuicChromiumClientSession*) ./../../net/quic/quic_session_pool.cc:633:3
    #9 0x5632a3b2294d in Invoke<void (net::QuicChromiumClientSession::*)(), const base::WeakPtr<net::QuicChromiumClientSession> &> ./../../base/functional/bind_internal.h:738:12
    #10 0x5632a3b2294d in MakeItSo<void (net::QuicChromiumClientSession::*)(), std::__Cr::tuple<base::WeakPtr<net::QuicChromiumClientSession> > > ./../../base/functional/bind_internal.h:954:5
    #11 0x5632a3b2294d in void base::internal::Invoker<base::internal::FunctorTraits<void (net::QuicChromiumClientSession::*&&)(), base::WeakPtr<net::QuicChromiumClientSession>&&>, base::internal::BindState<true, true, false, void (net::QuicChromiumClientSession::*)(), base::WeakPtr<net::QuicChromiumClientSession>>, void ()>::RunImpl<void (net::QuicChromiumClientSession::*)(), std::__Cr::tuple<base::WeakPtr<net::QuicChromiumClientSession>>, 0ul>(void (net::QuicChromiumClientSession::*&&)(), std::__Cr::tuple<base::WeakPtr<net::QuicChromiumClientSession>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) ./../../base/functional/bind_internal.h:1067:14
    #12 0x5632a2bf3df4 in Run ./../../base/functional/callback.h:156:12
    #13 0x5632a2bf3df4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:202:34
    #14 0x5632a2c556df in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:11)> ./../../base/task/common/task_annotator.h:89:5
    #15 0x5632a2c556df in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #16 0x5632a2c546c9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:40
    #17 0x5632a2c5649a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #18 0x5632a2da281f in base::MessagePumpEpoll::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_epoll.cc:95:55
    #19 0x5632a2d9a950 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_libevent.cc:274:18
    #20 0x5632a2c571df in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:641:12
    #21 0x5632a2b87e2f in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #22 0x5632a2cdb7cc in base::Thread::Run(base::RunLoop*) ./../../base/threading/thread.cc:338:13
    #23 0x5632a2cdbd31 in base::Thread::ThreadMain() ./../../base/threading/thread.cc:410:3
    #24 0x5632a2d25bf7 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:103:13
    #25 0x5632912096a8 in asan_thread_start(void*) _asan_rtl_:28

0x50800002abb0 is located 16 bytes inside of 88-byte region [0x50800002aba0,0x50800002abf8)
freed by thread T23 (NetworkService) here:
    #0 0x56329123ff6d in operator delete(void*) _asan_rtl_:3
    #1 0x5632a3af034b in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:68:5
    #2 0x5632a3af034b in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:279:7
    #3 0x5632a3af034b in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:249:71
    #4 0x5632a3af034b in net::QuicChromiumClientSession::Handle::~Handle() ./../../net/quic/quic_chromium_client_session.cc:387:1
    #5 0x5632a3af0483 in net::QuicChromiumClientSession::Handle::~Handle() ./../../net/quic/quic_chromium_client_session.cc:383:46
    #6 0x5632a3b52f50 in net::QuicHttpStream::~QuicHttpStream() ./../../net/quic/quic_http_stream.cc:47:1
    #7 0x5632a3b53153 in net::QuicHttpStream::~QuicHttpStream() ./../../net/quic/quic_http_stream.cc:44:35
    #8 0x5632a8fdfc8f in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:68:5
    #9 0x5632a8fdfc8f in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:279:7
    #10 0x5632a8fdfc8f in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:249:71
    #11 0x5632a8fdfc8f in net::HttpNetworkTransaction::~HttpNetworkTransaction() ./../../net/http/http_network_transaction.cc:205:1
    #12 0x5632a8fe0d53 in net::HttpNetworkTransaction::~HttpNetworkTransaction() ./../../net/http/http_network_transaction.cc:172:51
    #13 0x5632a91a11d9 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:68:5
    #14 0x5632a91a11d9 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:279:7
    #15 0x5632a91a11d9 in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:249:71
    #16 0x5632a91a11d9 in network::ThrottlingNetworkTransaction::~ThrottlingNetworkTransaction() ./../../services/network/throttling/throttling_network_transaction.cc:34:1
    #17 0x5632a91a1473 in network::ThrottlingNetworkTransaction::~ThrottlingNetworkTransaction() ./../../services/network/throttling/throttling_network_transaction.cc:31:63
    #18 0x5632a913764b in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:68:5
    #19 0x5632a913764b in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:279:7
    #20 0x5632a913764b in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:249:71
    #21 0x5632a913764b in network::SharedDictionaryNetworkTransaction::~SharedDictionaryNetworkTransaction() ./../../services/network/shared_dictionary/shared_dictionary_network_transaction.cc:109:73
    #22 0x5632a9137993 in network::SharedDictionaryNetworkTransaction::~SharedDictionaryNetworkTransaction() ./../../services/network/shared_dictionary/shared_dictionary_network_transaction.cc:109:73
    #23 0x5632a39cbb57 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:68:5
    #24 0x5632a39cbb57 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:279:7
    #25 0x5632a39cbb57 in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:249:71
    #26 0x5632a39cbb57 in net::HttpCache::Transaction::~Transaction() ./../../net/http/http_cache_transaction.cc:205:1
    #27 0x5632a39ce143 in net::HttpCache::Transaction::~Transaction() ./../../net/http/http_cache_transaction.cc:190:40
    #28 0x5632a8ff9e30 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:68:5
    #29 0x5632a8ff9e30 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:279:7
    #30 0x5632a8ff9e30 in net::URLRequestHttpJob::DestroyTransaction() ./../../net/url_request/url_request_http_job.cc:556:16
    #31 0x5632a8ff9bb5 in net::URLRequestHttpJob::Kill() ./../../net/url_request/url_request_http_job.cc:456:5
    #32 0x5632a3d09d49 in net::URLRequest::DoCancel(int, net::SSLInfo const&) ./../../net/url_request/url_request.cc:745:11
    #33 0x5632a3d026f1 in Cancel ./../../net/url_request/url_request.cc:706:10
    #34 0x5632a3d026f1 in net::URLRequest::~URLRequest() ./../../net/url_request/url_request.cc:185:3
    #35 0x5632a3d03353 in net::URLRequest::~URLRequest() ./../../net/url_request/url_request.cc:182:27
    #36 0x5632a91c7880 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:68:5
    #37 0x5632a91c7880 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:279:7
    #38 0x5632a91c7880 in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:249:71
    #39 0x5632a91c7880 in network::URLLoader::~URLLoader() ./../../services/network/url_loader.cc:1122:1
    #40 0x5632a91c7fd3 in network::URLLoader::~URLLoader() ./../../services/network/url_loader.cc:1107:25
    #41 0x5632a905000d in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:68:5
    #42 0x5632a905000d in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:279:7
    #43 0x5632a905000d in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:249:71
    #44 0x5632a905000d in __destroy_at<std::__Cr::unique_ptr<network::URLLoader, std::__Cr::default_delete<network::URLLoader> >, 0> ./../../third_party/libc++/src/include/__memory/construct_at.h:67:11
    #45 0x5632a905000d in destroy<std::__Cr::unique_ptr<network::URLLoader, std::__Cr::default_delete<network::URLLoader> >, void, 0> ./../../third_party/libc++/src/include/__memory/allocator_traits.h:340:5
    #46 0x5632a905000d in erase ./../../third_party/libc++/src/include/__tree:2048:3
    #47 0x5632a905000d in erase ./../../third_party/libc++/src/include/set:768:77
    #48 0x5632a905000d in void network::cors::CorsURLLoaderFactory::DestroyLoader<network::URLLoader>(network::URLLoader*, std::__Cr::set<std::__Cr::unique_ptr<network::URLLoader, std::__Cr::default_delete<network::URLLoader>>, base::UniquePtrComparator, std::__Cr::allocator<std::__Cr::unique_ptr<network::URLLoader, std::__Cr::default_delete<network::URLLoader>>>>&) ./../../services/network/cors/cors_url_loader_factory.h:144:13
    #49 0x5632a92051ff in Invoke<void (network::cors::CorsURLLoaderFactory::*)(network::URLLoader *), network::cors::CorsURLLoaderFactory *, network::URLLoader *> ./../../base/functional/bind_internal.h:738:12
    #50 0x5632a92051ff in MakeItSo<void (network::cors::CorsURLLoaderFactory::*)(network::URLLoader *), std::__Cr::tuple<base::internal::UnretainedWrapper<network::cors::CorsURLLoaderFactory, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, network::URLLoader *> ./../../base/functional/bind_internal.h:930:12
    #51 0x5632a92051ff in RunImpl<void (network::cors::CorsURLLoaderFactory::*)(network::URLLoader *), std::__Cr::tuple<base::internal::UnretainedWrapper<network::cors::CorsURLLoaderFactory, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> ./../../base/functional/bind_internal.h:1067:14
    #52 0x5632a92051ff in base::internal::Invoker<base::internal::FunctorTraits<void (network::cors::CorsURLLoaderFactory::*&&)(network::URLLoader*), network::cors::CorsURLLoaderFactory*>, base::internal::BindState<true, true, false, void (network::cors::CorsURLLoaderFactory::*)(network::URLLoader*), base::internal::UnretainedWrapper<network::cors::CorsURLLoaderFactory, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (network::URLLoader*)>::RunOnce(base::internal::BindStateBase*, network::URLLoader*) ./../../base/functional/bind_internal.h:980:12
    #53 0x5632a91c2c31 in Run ./../../base/functional/callback.h:156:12
    #54 0x5632a91c2c31 in DeleteSelf ./../../services/network/url_loader.cc:2309:31
    #55 0x5632a91c2c31 in network::URLLoader::NotifyCompleted(int) ./../../services/network/url_loader.cc:2288:3
    #56 0x5632a91db1f3 in Invoke<void (network::URLLoader::*)(), network::URLLoader *> ./../../base/functional/bind_internal.h:738:12
    #57 0x5632a91db1f3 in MakeItSo<void (network::URLLoader::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<network::URLLoader, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > ./../../base/functional/bind_internal.h:930:12
    #58 0x5632a91db1f3 in RunImpl<void (network::URLLoader::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<network::URLLoader, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> ./../../base/functional/bind_internal.h:1067:14
    #59 0x5632a91db1f3 in base::internal::Invoker<base::internal::FunctorTraits<void (network::URLLoader::*&&)(), network::URLLoader*>, base::internal::BindState<true, true, false, void (network::URLLoader::*)(), base::internal::UnretainedWrapper<network::URLLoader, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:980:12
    #60 0x5632a429e052 in Run ./../../base/functional/callback.h:156:12
    #61 0x5632a429e052 in mojo::InterfaceEndpointClient::NotifyError(std::__Cr::optional<mojo::DisconnectReason> const&) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:744:31
    #62 0x5632a42c44f6 in mojo::internal::MultiplexRouter::ProcessNotifyErrorTask(mojo::internal::MultiplexRouter::Task*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:1010:13
    #63 0x5632a42bb9b4 in mojo::internal::MultiplexRouter::ProcessTasks(mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:923:15
    #64 0x5632a42b7319 in mojo::internal::MultiplexRouter::OnPipeConnectionError(bool) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:833:3
    #65 0x5632a42c6919 in Invoke<void (mojo::internal::MultiplexRouter::*)(bool), mojo::internal::MultiplexRouter *, bool> ./../../base/functional/bind_internal.h:738:12
    #66 0x5632a42c6919 in MakeItSo<void (mojo::internal::MultiplexRouter::*)(bool), std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::internal::MultiplexRouter, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, bool> > ./../../base/functional/bind_internal.h:930:12
    #67 0x5632a42c6919 in RunImpl<void (mojo::internal::MultiplexRouter::*)(bool), std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::internal::MultiplexRouter, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, bool>, 0UL, 1UL> ./../../base/functional/bind_internal.h:1067:14
    #68 0x5632a42c6919 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::internal::MultiplexRouter::*&&)(bool), mojo::internal::MultiplexRouter*, bool&&>, base::internal::BindState<true, true, false, void (mojo::internal::MultiplexRouter::*)(bool), base::internal::UnretainedWrapper<mojo::internal::MultiplexRouter, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, bool>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:980:12
    #69 0x5632a428eba1 in Run ./../../base/functional/callback.h:156:12
    #70 0x5632a428eba1 in mojo::Connector::HandleError(bool, bool) ./../../mojo/public/cpp/bindings/lib/connector.cc:681:44

previously allocated by thread T23 (NetworkService) here:
    #0 0x56329123f70d in operator new(unsigned long) _asan_rtl_:3
    #1 0x5632a3af14b8 in net::QuicChromiumClientSession::Handle::RequestStream(bool, base::OnceCallback<void (int)>, net::NetworkTrafficAnnotationTag const&) ./../../net/quic/quic_chromium_client_session.cc:484:7
    #2 0x5632a3b59ddf in net::QuicHttpStream::DoRequestStream() ./../../net/quic/quic_http_stream.cc:469:26
    #3 0x5632a3b54074 in net::QuicHttpStream::DoLoop(int) ./../../net/quic/quic_http_stream.cc:423:14
    #4 0x5632a3b537ac in net::QuicHttpStream::InitializeStream(bool, net::RequestPriority, net::NetLogWithSource const&, base::OnceCallback<void (int)>) ./../../net/quic/quic_http_stream.cc:113:12
    #5 0x5632a8fe1fa7 in DoInitStream ./../../net/http/http_network_transaction.cc:928:19
    #6 0x5632a8fe1fa7 in net::HttpNetworkTransaction::DoLoop(int) ./../../net/http/http_network_transaction.cc:781:14
    #7 0x5632a8fe6a71 in OnIOComplete ./../../net/http/http_network_transaction.cc:755:12
    #8 0x5632a8fe6a71 in net::HttpNetworkTransaction::OnStreamReady(net::ProxyInfo const&, std::__Cr::unique_ptr<net::HttpStream, std::__Cr::default_delete<net::HttpStream>>) ./../../net/http/http_network_transaction.cc:636:3
    #9 0x5632a3a93d56 in net::HttpStreamFactory::JobController::OnStreamReady(net::HttpStreamFactory::Job*) ./../../net/http/http_stream_factory_job_controller.cc:329:14
    #10 0x5632a3a8b8dd in Invoke<void (net::HttpStreamFactory::Job::*)(), const base::WeakPtr<net::HttpStreamFactory::Job> &> ./../../base/functional/bind_internal.h:738:12
    #11 0x5632a3a8b8dd in MakeItSo<void (net::HttpStreamFactory::Job::*)(), std::__Cr::tuple<base::WeakPtr<net::HttpStreamFactory::Job> > > ./../../base/functional/bind_internal.h:954:5
    #12 0x5632a3a8b8dd in void base::internal::Invoker<base::internal::FunctorTraits<void (net::HttpStreamFactory::Job::*&&)(), base::WeakPtr<net::HttpStreamFactory::Job>&&>, base::internal::BindState<true, true, false, void (net::HttpStreamFactory::Job::*)(), base::WeakPtr<net::HttpStreamFactory::Job>>, void ()>::RunImpl<void (net::HttpStreamFactory::Job::*)(), std::__Cr::tuple<base::WeakPtr<net::HttpStreamFactory::Job>>, 0ul>(void (net::HttpStreamFactory::Job::*&&)(), std::__Cr::tuple<base::WeakPtr<net::HttpStreamFactory::Job>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) ./../../base/functional/bind_internal.h:1067:14
    #13 0x5632a2bf3df4 in Run ./../../base/functional/callback.h:156:12
    #14 0x5632a2bf3df4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:202:34
    #15 0x5632a2c556df in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:11)> ./../../base/task/common/task_annotator.h:89:5
    #16 0x5632a2c556df in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #17 0x5632a2c546c9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:40
    #18 0x5632a2c5649a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #19 0x5632a2da281f in base::MessagePumpEpoll::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_epoll.cc:95:55
    #20 0x5632a2d9a950 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_libevent.cc:274:18
    #21 0x5632a2c571df in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:641:12
    #22 0x5632a2b87e2f in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #23 0x5632a2cdb7cc in base::Thread::Run(base::RunLoop*) ./../../base/threading/thread.cc:338:13
    #24 0x5632a2cdbd31 in base::Thread::ThreadMain() ./../../base/threading/thread.cc:410:3
    #25 0x5632a2d25bf7 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:103:13
    #26 0x5632912096a8 in asan_thread_start(void*) _asan_rtl_:28

Thread T23 (NetworkService) created by T0 (chrome) here:
    #0 0x5632911f1981 in ___interceptor_pthread_create _asan_rtl_:3
    #1 0x5632a2d25150 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) ./../../base/threading/platform_thread_posix.cc:148:13
    #2 0x5632a2cdaae3 in base::Thread::StartWithOptions(base::Thread::Options) ./../../base/threading/thread.cc:211:26
    #3 0x56329b156ea2 in CreateInProcessNetworkService ./../../content/browser/network_service_instance_impl.cc:349:40
    #4 0x56329b156ea2 in content::GetNetworkService() ./../../content/browser/network_service_instance_impl.cc:596:11
    #5 0x5632a186cb17 in Invoke<network::mojom::NetworkService *(*const &)()> ./../../base/functional/bind_internal.h:671:12
    #6 0x5632a186cb17 in MakeItSo<network::mojom::NetworkService *(*const &)(), const std::__Cr::tuple<> &> ./../../base/functional/bind_internal.h:930:12
    #7 0x5632a186cb17 in RunImpl<network::mojom::NetworkService *(*const &)(), const std::__Cr::tuple<> &> ./../../base/functional/bind_internal.h:1067:14
    #8 0x5632a186cb17 in base::internal::Invoker<base::internal::FunctorTraits<network::mojom::NetworkService* (* const&)()>, base::internal::BindState<false, true, false, network::mojom::NetworkService* (*)()>, network::mojom::NetworkService* ()>::Run(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:987:12
    #9 0x5632a4fb5934 in base::RepeatingCallback<network::mojom::NetworkService* ()>::Run() const & ./../../base/functional/callback.h:344:12
    #10 0x5632a4fb2919 in network::NetworkQualityTracker::InitializeMojoChannel() ./../../services/network/public/cpp/network_quality_tracker.cc:157:37
    #11 0x5632a4fb2716 in network::NetworkQualityTracker::NetworkQualityTracker(base::RepeatingCallback<network::mojom::NetworkService* ()>) ./../../services/network/public/cpp/network_quality_tracker.cc:24:3
    #12 0x5632a1866130 in make_unique<network::NetworkQualityTracker, base::RepeatingCallback<network::mojom::NetworkService *()> > ./../../third_party/libc++/src/include/__memory/unique_ptr.h:621:30
    #13 0x5632a1866130 in BrowserProcessImpl::network_quality_tracker() ./../../chrome/browser/browser_process_impl.cc:792:32
    #14 0x5632a186afe5 in CreateNetworkQualityObserver ./../../chrome/browser/browser_process_impl.cc:1182:45
    #15 0x5632a186afe5 in BrowserProcessImpl::PreMainMessageLoopRun() ./../../chrome/browser/browser_process_impl.cc:1273:3
    #16 0x5632a1859a62 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl() ./../../chrome/browser/chrome_browser_main.cc:1466:21
    #17 0x5632a185957f in ChromeBrowserMainParts::PreMainMessageLoopRun() ./../../chrome/browser/chrome_browser_main.cc:1232:18
    #18 0x56329a625cbc in content::BrowserMainLoop::PreMainMessageLoopRun() ./../../content/browser/browser_main_loop.cc:1013:28
    #19 0x56329a62cea3 in Invoke<int (content::BrowserMainLoop::*)(), content::BrowserMainLoop *> ./../../base/functional/bind_internal.h:738:12
    #20 0x56329a62cea3 in MakeItSo<int (content::BrowserMainLoop::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<content::BrowserMainLoop, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > ./../../base/functional/bind_internal.h:930:12
    #21 0x56329a62cea3 in RunImpl<int (content::BrowserMainLoop::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<content::BrowserMainLoop, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> ./../../base/functional/bind_internal.h:1067:14
    #22 0x56329a62cea3 in base::internal::Invoker<base::internal::FunctorTraits<int (content::BrowserMainLoop::*&&)(), content::BrowserMainLoop*>, base::internal::BindState<true, true, false, int (content::BrowserMainLoop::*)(), base::internal::UnretainedWrapper<content::BrowserMainLoop, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, int ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:980:12
    #23 0x56329bdd10e9 in Run ./../../base/functional/callback.h:156:12
    #24 0x56329bdd10e9 in content::StartupTaskRunner::RunAllTasksNow() ./../../content/browser/startup_task_runner.cc:42:29
    #25 0x56329a624d90 in content::BrowserMainLoop::CreateStartupTasks() ./../../content/browser/browser_main_loop.cc:917:25
    #26 0x56329a62faea in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams) ./../../content/browser/browser_main_runner_impl.cc:140:15
    #27 0x56329a61f80f in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser_main.cc:30:32
    #28 0x5632a0314860 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:708:10
    #29 0x5632a0318292 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content_main_runner_impl.cc:1299:10
    #30 0x5632a031793e in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1144:12
    #31 0x5632a0311d00 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:335:36
    #32 0x5632a031237b in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:348:10
    #33 0x563291241de8 in ChromeMain ./../../chrome/app/chrome_main.cc:192:12
    #34 0x7ff6efe29d8f in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16

SUMMARY: AddressSanitizer: heap-use-after-free (/home/pwn11/asan-linux-release/chrome+0x20e12739) (BuildId: 206d0f62f4f77ad4)
Shadow bytes around the buggy address:
  0x50800002a900: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x50800002a980: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x50800002aa00: fa fa f7 fa 00 00 00 00 00 00 00 00 00 00 00 00
  0x50800002aa80: fa fa f7 fa 00 00 00 00 00 00 00 00 00 00 00 fa
  0x50800002ab00: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
=>0x50800002ab80: fa fa f7 fa fd fd[fd]fd fd fd fd fd fd fd fd fa
  0x50800002ac00: fa fa f7 fa 00 00 00 00 00 00 fc fc fc fc fc fc
  0x50800002ac80: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x50800002ad00: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x50800002ad80: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x50800002ae00: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
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

==547540==ADDITIONAL INFO

==547540==Note: Please include this section with the ASan report.
Task trace:
    #0 0x5632a3b0a805 in net::QuicChromiumClientSession::NotifyFactoryOfSessionClosedLater() ./../../net/quic/quic_chromium_client_session.cc:3583:7
    #1 0x5632a3a822dc in net::HttpStreamFactory::Job::RunLoop(int) ./../../net/http/http_stream_factory_job.cc:683:13
    #2 0x5632a4318857 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) ./../../mojo/public/cpp/system/simple_watcher.cc:102:13


MiraclePtr Status: MANUAL ANALYSIS REQUIRED
A pointer to the same region was extracted from a raw_ptr<T> object prior to this crash.
To determine the protection status, enable extraction warnings and check whether the raw_ptr<T> object can be destroyed or overwritten between the extraction and use.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==547540==END OF ADDITIONAL INFO
==547540==ABORTING



## Attachments

- [crash.html](attachments/crash.html) (text/html, 782 B)
- [launcher.sh](attachments/launcher.sh) (text/x-sh, 2.3 KB)
- [asan.log](attachments/asan.log) (text/plain, 27.6 KB)
- asan.log (text/plain, 41.2 KB)
- launcher.sh (text/x-sh, 1.7 KB)

## Timeline

### ti...@chromium.org (2024-03-04)

[Security shepherd] Attempting reproduction, though I don't think my simple `python -m http.server` server will trigger the crashing quic codepath.

### em...@gmail.com (2024-03-04)

I reproduced it using 'python3 -m http.server 8000 |path|'.

It's just that the code in the script needs to be accessed 'https://picsum.photo'.

### ti...@chromium.org (2024-03-04)

> It's just that the code in the script needs to be accessed '<https://picsum.photo>'.

Ah, right! Thanks :)

In the meantime, I reproduced at HEAD! Commit: `195be11b6b2f714bb9a38c5d749b78aa94135ac6`

Edited the launcher script to make it easier to change paths, see attached.

It crashed for me after I gave up waiting and ctrl-c'd the launcher script, but only the first time. It did not crash the second time.

So far, it seems from my testing that this triggers at shutdown, but judging from stack traces it's not obvious that's required. Setting severity high - if it indeed is only triggerable at shutdown, this should be downgraded to medium.

### ti...@chromium.org (2024-03-04)

Setting Found In to 124 to reflect HEAD, but I have not attempted bisection (too many other bugs to look at).

### em...@gmail.com (2024-03-04)

In my local testing, there is no need for a shutdown operation and it will be repro soon.

### ti...@chromium.org (2024-03-04)

Assigning to bashi@ who has touched `net/quic/quic_chromium_client_session.h` recently. CC-ing all OWNERS of `net/quic`.

### ti...@chromium.org (2024-03-04)

bashi@, could you please take a look? I have not bisected, and have only managed to reproduce once. See [comment #4](https://issues.chromium.org/issues/327687950#comment4).

### ti...@chromium.org (2024-03-04)

In particular, please set Found In correctly once you determine the root cause and/or bisect.

### ba...@chromium.org (2024-03-05)

I was able to reproduce it without shutting down.

Looks like `QuicChromiumClientSession::stream_requests_` could have a dangling pointer to QuicChromiumClientSession::StreamRequest. I skimmed through the code and found no obvious bugs. The destructor of StreamRequest calls QuicChromiumClientSession::Handle::CancelRequest(), which should remove the pointer to the StreamRequest from `QuicChromiumClientSession::stream_requests_`.

I didn't see any recent changes in the code so I guess the UAF is not a regression but exists for a while.

### ba...@chromium.org (2024-03-05)

QuicChromiumClientSession::Handle::CancelRequest() is called but `session_` is [null](https://source.chromium.org/chromium/chromium/src/+/main:net/quic/quic_chromium_client_session.cc;l=507;drc=de9ce1844e5024a8b9a822fa8321f59a05fb990c) because QuicChromiumClientSession::Handle::OnSessionClosed() is called before and `session_` is cleared [here](https://source.chromium.org/chromium/chromium/src/+/main:net/quic/quic_chromium_client_session.cc;l=402;drc=de9ce1844e5024a8b9a822fa8321f59a05fb990c). This results in a dangling pointer in `QuicChromiumClientSession::stream_requests_`.

I tried to reset `QuicChromiumClientSession::Handle::stream_request_` before `session_ = nullptr` but it didn't fix the UAF.

### ba...@chromium.org (2024-03-05)

Adding liza@ since this looks similar to [issue 41491379](https://issues.chromium.org/issues/41491379).

### pe...@google.com (2024-03-05)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-03-05)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2024-03-05)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ba...@chromium.org (2024-03-08)

I think I found the root cause.

`QuicChromiumClientSession::TryCreateStream()` calls `CanOpenNextOutgoingBidirectionalStream()`. This can end up calling `QuicChromiumClientSession::Handle::OnSessionClosed()` when the QuicConnection is closed during the call:

```
net::QuicChromiumClientSession::Handle::OnSessionClosed()
net::QuicChromiumClientSession::CloseAllHandles()
net::QuicChromiumClientSession::OnConnectionClosed()
quic::QuicConnection::TearDownLocalConnectionState()
quic::QuicConnection::TearDownLocalConnectionState()
quic::QuicConnection::CloseConnection()
quic::QuicControlFrameManager::WriteOrBufferQuicFrame()
quic::QuicControlFrameManager::WriteOrBufferStreamsBlocked()
quic::QuicSession::CanOpenNextOutgoingBidirectionalStream()
net::QuicChromiumClientSession::TryCreateStream()
net::QuicChromiumClientSession::Handle::TryCreateStream()

```

If this happens, `QuicChromiumClientSession::Handle::session_` becomes nullptr ([code](https://source.chromium.org/chromium/chromium/src/+/main:net/quic/quic_chroQuicChromiumClientSession::Handle::CancelRequestmium_client_session.cc;l=402;drc=339c4b44e95633d9c2b4a97484ad05e368b730c1)), but we insert `request` [here](https://source.chromium.org/chromium/chromium/src/+/main:net/quic/quic_chromium_client_session.cc;l=1227;drc=339c4b44e95633d9c2b4a97484ad05e368b730c1) into `stream_requests_`. Since `session_` became nullptr, `QuicChromiumClientSession::Handle::CancelRequest()` won't erase the `request` from `stream_requests_`. This leads to cause the UAF in `QuicChromiumClientSession::CancelAllRequests()`.

I created a fix (<https://crrev.com/c/5355170>). I don't observe the UAF with the fix.

### ap...@google.com (2024-03-08)

Project: chromium/src
Branch: main

commit 89990158ae7b2f54d724cc6d56f121f4d6f6f3ee
Author: Kenichi Ishibashi <bashi@chromium.org>
Date:   Fri Mar 08 22:33:20 2024

    [quic] Check if connection is closed after stream id allocation check
    
    QuicSession::CanOpenNextOutgoingBidirectionalStream() could close the
    connection. When the connection is closed, stream creation should fail
    instead of being pending.
    
    Bug: 327687950
    Change-Id: I9704b6ddbc7a647de394d6c33650fa45d34e4a2b
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5355170
    Commit-Queue: Kenichi Ishibashi <bashi@chromium.org>
    Reviewed-by: Ryan Hamilton <rch@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1270425}

M       net/quic/quic_chromium_client_session.cc

https://chromium-review.googlesource.com/5355170


### am...@google.com (2024-03-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-03-14)

Congratulations Cassidy Kim! The Chrome VRP Panel has decided to award you $10,000 for this report of a network process memory corruption. Thank you for your efforts and reporting this issue to us -- nice work!

### pe...@google.com (2024-03-20)

Not requesting merge to dev (M124) because latest trunk commit (1270425) appears to be prior to dev branch point (1274542). If this is incorrect please remove NA-124 from the 'Merge' field and add 124 to the 'Merge-Request' field If other changes are required to fix this bug completely please request a merge if necessary.
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### pe...@google.com (2024-06-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/327687950)*
