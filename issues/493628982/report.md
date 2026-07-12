# Heap UAF in HTTPS HTTP/2 proxy authentication flow

| Field | Value |
|-------|-------|
| **Issue ID** | [493628982](https://issues.chromium.org/issues/493628982) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>Network>Proxy |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sh...@gmail.com |
| **Assignee** | mm...@chromium.org |
| **Created** | 2026-03-17 |
| **Bounty** | $10,000.00 |

## Description

## VULNERABILITY DETAILS

This issue is a heap-use-after-free in Chrome’s HTTPS HTTP/2 proxy authentication flow, in the `net/socket/transport_client_socket_pool` + `net/http/` `http_proxy_connect_job` + `net/spdy/spdy_proxy_client_socket` path, with the recorded crashing family at `net::TransportClientSocketPool::Group::IsEmpty() const`.

The most likely root cause is a lifetime bug during proxy-auth challenge handling and connection teardown, where a socket-pool group or closely related state is destroyed or invalidated while another path still retains and later dereferences it.

```
=================================================================
==3183368==ERROR: AddressSanitizer: heap-use-after-free on address 0x7cf38a35bad0 at pc 0x7f94e5a76274 bp 0x7b937c7ad4a0 sp 0x7b937c7ad498
READ of size 8 at 0x7cf38a35bad0 thread T5 (Chrome_ChildIOT)
[3183402:3183402:0315/043531.508658:ERROR:content/renderer/render_process_impl.cc:216] WebFrame LEAKED 1 TIMES
    #0 0x7f94e5a76273 in net::TransportClientSocketPool::Group::IsEmpty() const net/socket/transport_client_socket_pool.h:350:14
    #1 0x7f94e5a55d89 in net::TransportClientSocketPool::RequestSocketInternal(net::ClientSocketPool::GroupId const&, net::TransportClientSocketPool::Request const&, base::OnceCallback<void ()>) net/socket/transport_client_socket_pool.cc:495:14
    #2 0x7f94e5a5471d in net::TransportClientSocketPool::RequestSocket(net::ClientSocketPool::GroupId const&, scoped_refptr<net::ClientSocketPool::SocketParams>, std::__Cr::optional<net::NetworkTrafficAnnotationTag> const&, net::RequestPriority, net::SocketTag const&, net::ClientSocketPool::RespectLimits, net::ClientSocketHandle*, base::OnceCallback<void (int)>, base::RepeatingCallback<void (net::HttpResponseInfo const&, net::HttpAuthController*, base::OnceCallback<void ()>)> const&, net::NetLogWithSource const&) net/socket/transport_client_socket_pool.cc:274:7
    #3 0x7f94e593149b in net::ClientSocketHandle::Init(net::ClientSocketPool::GroupId const&, scoped_refptr<net::ClientSocketPool::SocketParams>, std::__Cr::optional<net::NetworkTrafficAnnotationTag> const&, net::RequestPriority, net::SocketTag const&, net::ClientSocketPool::RespectLimits, base::OnceCallback<void (int)>, base::RepeatingCallback<void (net::HttpResponseInfo const&, net::HttpAuthController*, base::OnceCallback<void ()>)> const&, net::ClientSocketPool*, net::NetLogWithSource const&) net/socket/client_socket_handle.cc:51:19
    #4 0x7f94e5940a1e in net::(anonymous namespace)::InitSocketPoolHelper(url::SchemeHostPort, int, net::RequestPriority, net::HttpNetworkSession*, net::ProxyInfo const&, std::__Cr::vector<net::SSLConfig::CertAndStatus, std::__Cr::allocator<net::SSLConfig::CertAndStatus>> const&, net::PrivacyMode, net::NetworkAnonymizationKey, net::SecureDnsPolicy, net::SocketTag const&, net::NetLogWithSource const&, int, net::ClientSocketHandle*, net::HttpNetworkSession::SocketPoolType, base::OnceCallback<void (int)>, base::RepeatingCallback<void (net::HttpResponseInfo const&, net::HttpAuthController*, base::OnceCallback<void ()>)> const&) net/socket/client_socket_pool_manager.cc:131:25
    #5 0x7f94e594009d in net::InitSocketHandleForHttpRequest(url::SchemeHostPort, int, net::RequestPriority, net::HttpNetworkSession*, net::ProxyInfo const&, std::__Cr::vector<net::SSLConfig::CertAndStatus, std::__Cr::allocator<net::SSLConfig::CertAndStatus>> const&, net::PrivacyMode, net::NetworkAnonymizationKey, net::SecureDnsPolicy, net::SocketTag const&, net::NetLogWithSource const&, net::ClientSocketHandle*, base::OnceCallback<void (int)>, base::RepeatingCallback<void (net::HttpResponseInfo const&, net::HttpAuthController*, base::OnceCallback<void ()>)> const&) net/socket/client_socket_pool_manager.cc:226:10
    #6 0x7f94e52d9296 in net::HttpStreamFactory::Job::DoInitConnectionImpl() net/http/http_stream_factory_job.cc:823:10
    #7 0x7f94e52d43dd in net::HttpStreamFactory::Job::DoInitConnection() net/http/http_stream_factory_job.cc:702:16
    #8 0x7f94e52d289b in net::HttpStreamFactory::Job::DoLoop(int) net/http/http_stream_factory_job.cc:630:14
    #9 0x7f94e52d14a5 in net::HttpStreamFactory::Job::RunLoop(int) net/http/http_stream_factory_job.cc:531:12
    #10 0x7f94e52c877e in net::HttpStreamFactory::Job::StartInternal() net/http/http_stream_factory_job.cc:655:3
    #11 0x7f94e52c8553 in net::HttpStreamFactory::Job::Start(net::HttpStreamRequest::StreamType) net/http/http_stream_factory_job.cc:246:3
    #12 0x7f94e5307007 in net::HttpStreamFactory::JobController::DoCreateJobs() net/http/http_stream_factory_job_controller.cc:1026:16
    #13 0x7f94e53027b0 in net::HttpStreamFactory::JobController::DoLoop(int) net/http/http_stream_factory_job_controller.cc:807:14
    #14 0x7f94e52f4629 in net::HttpStreamFactory::JobController::RunLoop(int) net/http/http_stream_factory_job_controller.cc:765:12
    #15 0x7f94e52f41aa in net::HttpStreamFactory::JobController::Start(net::HttpStreamRequest::Delegate*, net::WebSocketHandshakeStreamBase::CreateHelper*, net::NetLogWithSource const&, net::HttpStreamRequest::StreamType, net::RequestPriority) net/http/http_stream_factory_job_controller.cc:232:3
    #16 0x7f94e52bec72 in net::HttpStreamFactory::RequestStreamInternal(net::HttpRequestInfo const&, net::RequestPriority, std::__Cr::vector<net::SSLConfig::CertAndStatus, std::__Cr::allocator<net::SSLConfig::CertAndStatus>> const&, net::HttpStreamRequest::Delegate*, net::WebSocketHandshakeStreamBase::CreateHelper*, net::HttpStreamRequest::StreamType, bool, bool, bool, net::NetLogWithSource const&) net/http/http_stream_factory.cc:232:34
    #17 0x7f94e52be8a7 in net::HttpStreamFactory::RequestStream(net::HttpRequestInfo const&, net::RequestPriority, std::__Cr::vector<net::SSLConfig::CertAndStatus, std::__Cr::allocator<net::SSLConfig::CertAndStatus>> const&, net::HttpStreamRequest::Delegate*, bool, bool, net::NetLogWithSource const&) net/http/http_stream_factory.cc:163:10
    #18 0x7f94e517a039 in net::HttpNetworkTransaction::DoCreateStream() net/http/http_network_transaction.cc:1136:56
    #19 0x7f94e516bc40 in net::HttpNetworkTransaction::DoLoop(int) net/http/http_network_transaction.cc:1009:14
    #20 0x7f94e516add0 in net::HttpNetworkTransaction::Start(net::HttpRequestInfo const*, base::OnceCallback<void (int)>, net::NetLogWithSource const&) net/http/http_network_transaction.cc:426:12
    #21 0x7f94a0e21307 in network::ThrottlingNetworkTransaction::Start(net::HttpRequestInfo const*, base::OnceCallback<void (int)>, net::NetLogWithSource const&) services/network/throttling/throttling_network_transaction.cc:137:34
    #22 0x7f94e5920665 in net::SharedDictionaryNetworkTransaction::Start(net::HttpRequestInfo const*, base::OnceCallback<void (int)>, net::NetLogWithSource const&) net/shared_dictionary/shared_dictionary_network_transaction.cc:114:34
    #23 0x7f94e50c5eeb in net::HttpCache::Transaction::DoSendRequest() net/http/http_cache_transaction.cc:1921:28
    #24 0x7f94e50af243 in net::HttpCache::Transaction::DoLoop(int) net/http/http_cache_transaction.cc:910:14
    #25 0x7f94e50abf1c in net::HttpCache::Transaction::Start(net::HttpRequestInfo const*, base::OnceCallback<void (int)>, net::NetLogWithSource const&) net/http/http_cache_transaction.cc:213:12
    #26 0x7f94e5d00264 in net::URLRequestHttpJob::StartTransactionInternal() net/url_request/url_request_http_job.cc:782:26
    #27 0x7f94e5cff301 in net::URLRequestHttpJob::MaybeStartTransactionInternal(int) net/url_request/url_request_http_job.cc:713:5
    #28 0x7f94e5cfc976 in net::URLRequestHttpJob::StartTransaction() net/url_request/url_request_http_job.cc:692:5
    #29 0x7f94e5cfb3e7 in net::URLRequestHttpJob::OnGotFirstPartySetMetadata(net::FirstPartySetMetadata, net::FirstPartySetsCacheFilter::MatchInfo) net/url_request/url_request_http_job.cc:557:5
    #30 0x7f94e5cfaa48 in net::URLRequestHttpJob::Start() net/url_request/url_request_http_job.cc:493:5
    #31 0x7f94e5cb1a30 in net::URLRequest::StartJob(std::__Cr::unique_ptr<net::URLRequestJob, std::__Cr::default_delete<net::URLRequestJob>>) net/url_request/url_request.cc:761:9
    #32 0x7f94e5cb0910 in net::URLRequest::BeforeRequestComplete(int) net/url_request/url_request.cc:682:5
    #33 0x7f94e5caf6f4 in net::URLRequest::Start() net/url_request/url_request.cc:621:7
    #34 0x7f94a0e60fe1 in network::URLLoader::ScheduleStart() services/network/url_loader.cc:761:19
    #35 0x7f94a0e6041b in network::URLLoader::ProcessOutboundSharedStorageInterceptor() services/network/url_loader.cc:743:3
    #36 0x7f94a0e5cdc2 in network::URLLoader::ProcessOutboundTrustTokenInterceptor(network::ResourceRequest const&) services/network/url_loader.cc:671:5
    #37 0x7f94a0e5ae2c in network::URLLoader::URLLoader(network::URLLoaderContext&, base::OnceCallback<void (network::URLLoader*)>, mojo::PendingReceiver<network::mojom::URLLoader>, int, network::ResourceRequest const&, mojo::PendingRemote<network::mojom::URLLoaderClient>, base::WeakPtr<network::mojom::URLLoaderClient>, net::NetworkTrafficAnnotationTag const&, base::numerics_internal::StrictNumeric<int>, int, base::WeakPtr<network::KeepaliveStatisticsRecorder>, std::__Cr::unique_ptr<network::TrustTokenRequestHelperFactory, std::__Cr::default_delete<network::TrustTokenRequestHelperFactory>>, network::SharedDictionaryManager*, std::__Cr::unique_ptr<network::SharedDictionaryAccessChecker, std::__Cr::default_delete<network::SharedDictionaryAccessChecker>>, network::ObserverWrapper<network::mojom::CookieAccessObserver>, network::ObserverWrapper<network::mojom::TrustTokenAccessObserver>, network::ObserverWrapper<network::mojom::URLLoaderNetworkServiceObserver>, network::ObserverWrapper<network::mojom::DevToolsObserver>, network::ObserverWrapper<network::mojom::DeviceBoundSessionAccessObserver>, mojo::PendingRemote<network::mojom::AcceptCHFrameObserver>, bool, network::SharedResourceChecker&, std::__Cr::unique_ptr<network::DevtoolsDurableMessageWriter, std::__Cr::default_delete<network::DevtoolsDurableMessageWriter>>, mojo::ScopedHandleBase<mojo::DataPipeProducerHandle>) services/network/url_loader.cc:561:3
    #38 0x7f94a0f13b07 in std::__Cr::unique_ptr<network::URLLoader, std::__Cr::default_delete<network::URLLoader>> std::__Cr::make_unique<network::URLLoader, network::URLLoaderFactory&, base::OnceCallback<void (network::URLLoader*)>, mojo::PendingReceiver<network::mojom::URLLoader>, unsigned int&, network::ResourceRequest const&, mojo::PendingRemote<network::mojom::URLLoaderClient>, base::WeakPtr<network::mojom::URLLoaderClient>, net::NetworkTrafficAnnotationTag, int&, int&, base::WeakPtr<network::KeepaliveStatisticsRecorder>, std::__Cr::unique_ptr<network::TrustTokenRequestHelperFactory, std::__Cr::default_delete<network::TrustTokenRequestHelperFactory>>, network::SharedDictionaryManager*, std::__Cr::unique_ptr<network::SharedDictionaryAccessChecker, std::__Cr::default_delete<network::SharedDictionaryAccessChecker>>, network::ObserverWrapper<network::mojom::CookieAccessObserver>, network::ObserverWrapper<network::mojom::TrustTokenAccessObserver>, network::ObserverWrapper<network::mojom::URLLoaderNetworkServiceObserver>, network::ObserverWrapper<network::mojom::DevToolsObserver>, network::ObserverWrapper<network::mojom::DeviceBoundSessionAccessObserver>, mojo::PendingRemote<network::mojom::AcceptCHFrameObserver>, bool const&, network::SharedResourceChecker&, std::__Cr::unique_ptr<network::DevtoolsDurableMessageWriter, std::__Cr::default_delete<network::DevtoolsDurableMessageWriter>>, mojo::ScopedHandleBase<mojo::DataPipeProducerHandle>, 0>(network::URLLoaderFactory&, base::OnceCallback<void (network::URLLoader*)>&&, mojo::PendingReceiver<network::mojom::URLLoader>&&, unsigned int&, network::ResourceRequest const&, mojo::PendingRemote<network::mojom::URLLoaderClient>&&, base::WeakPtr<network::mojom::URLLoaderClient>&&, net::NetworkTrafficAnnotationTag&&, int&, int&, base::WeakPtr<network::KeepaliveStatisticsRecorder>&&, std::__Cr::unique_ptr<network::TrustTokenRequestHelperFactory, std::__Cr::default_delete<network::TrustTokenRequestHelperFactory>>&&, network::SharedDictionaryManager*&&, std::__Cr::unique_ptr<network::SharedDictionaryAccessChecker, std::__Cr::default_delete<network::SharedDictionaryAccessChecker>>&&, network::ObserverWrapper<network::mojom::CookieAccessObserver>&&, network::ObserverWrapper<network::mojom::TrustTokenAccessObserver>&&, network::ObserverWrapper<network::mojom::URLLoaderNetworkServiceObserver>&&, network::ObserverWrapper<network::mojom::DevToolsObserver>&&, network::ObserverWrapper<network::mojom::DeviceBoundSessionAccessObserver>&&, mojo::PendingRemote<network::mojom::AcceptCHFrameObserver>&&, bool const&, network::SharedResourceChecker&, std::__Cr::unique_ptr<network::DevtoolsDurableMessageWriter, std::__Cr::default_delete<network::DevtoolsDurableMessageWriter>>&&, mojo::ScopedHandleBase<mojo::DataPipeProducerHandle>&&) gen/third_party/libc++/src/include/__memory/unique_ptr.h:756:30
    #39 0x7f94a0f0f778 in network::URLLoaderFactory::CreateLoaderAndStartWithSyncClient(mojo::PendingReceiver<network::mojom::URLLoader>, int, unsigned int, network::ResourceRequest const&, mojo::PendingRemote<network::mojom::URLLoaderClient>, base::WeakPtr<network::mojom::URLLoaderClient>, net::MutableNetworkTrafficAnnotationTag const&) services/network/url_loader_factory.cc:393:17
    #40 0x7f94a073a05c in network::cors::CorsURLLoader::StartNetworkRequest() services/network/cors/cors_url_loader.cc:1044:35
    #41 0x7f94a072eefe in network::cors::CorsURLLoader::StartRequest() services/network/cors/cors_url_loader.cc:932:5
    #42 0x7f94a072de66 in network::cors::CorsURLLoader::Start() services/network/cors/cors_url_loader.cc:404:3
    #43 0x7f94a076e054 in network::cors::CorsURLLoaderFactory::CreateLoaderAndStart(mojo::PendingReceiver<network::mojom::URLLoader>, int, unsigned int, network::ResourceRequest&, mojo::PendingRemote<network::mojom::URLLoaderClient>, net::MutableNetworkTrafficAnnotationTag const&) services/network/cors/cors_url_loader_factory.cc:492:17
    #44 0x7f94a0b62d52 in network::PrefetchMatchingURLLoaderFactory::CreateLoaderAndStart(mojo::PendingReceiver<network::mojom::URLLoader>, int, unsigned int, network::ResourceRequest&, mojo::PendingRemote<network::mojom::URLLoaderClient>, net::MutableNetworkTrafficAnnotationTag const&) services/network/prefetch_matching_url_loader_factory.cc:105:10
    #45 0x7f94a1960cba in network::mojom::URLLoaderFactoryStubDispatch::Accept(network::mojom::URLLoaderFactory*, mojo::Message*) gen/services/network/public/mojom/url_loader_factory.mojom.cc:352:13
    #46 0x7f94a077c406 in network::mojom::URLLoaderFactoryStub<mojo::RawPtrImplRefTraits<network::mojom::URLLoaderFactory>>::Accept(mojo::Message*) gen/services/network/public/mojom/url_loader_factory.mojom.h:139:12
    #47 0x7f94f6100b5e in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085:54
    #48 0x7f94f60ff941 in mojo::InterfaceEndpointClient::HandleIncomingMessageThunk::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:383:18
    #49 0x7f94f613e183 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:51:24
    #50 0x7f94f6106900 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #51 0x7f94f6147de2 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1204:42
    #52 0x7f94f6146b26 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:790:7
    #53 0x7f94f613e038 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:44:19
    #54 0x7f94f60bd463 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) mojo/public/cpp/bindings/lib/connector.cc:568:49
    #55 0x7f94f60bf03a in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:629:14
    #56 0x7f94f60be9d2 in mojo::Connector::OnHandleReadyInternal(unsigned int) mojo/public/cpp/bindings/lib/connector.cc:454:3
    #57 0x7f94f60be845 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int) mojo/public/cpp/bindings/lib/connector.cc:420:3
    #58 0x7f94f60cba65 in void base::internal::DecayedFunctorTraits<void (mojo::Connector::*)(char const*, unsigned int), mojo::Connector*, char const* const&>::Invoke<void (mojo::Connector::*)(char const*, unsigned int), mojo::Connector*, char const*, unsigned int>(void (mojo::Connector::*)(char const*, unsigned int), mojo::Connector*&&, char const*&&, unsigned int&&) base/functional/bind_internal.h:740:12
    #59 0x7f94f60cb73e in void base::internal::InvokeHelper<false, base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, void, 0ul, 1ul>::MakeItSo<void (mojo::Connector::* const&)(char const*, unsigned int), std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>> const&, unsigned int>(void (mojo::Connector::* const&)(char const*, unsigned int), std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>> const&, unsigned int&&) base/functional/bind_internal.h:932:12
    #60 0x7f94f60cb461 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::RunImpl<void (mojo::Connector::* const&)(char const*, unsigned int), std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>> const&, 0ul, 1ul>(void (mojo::Connector::* const&)(char const*, unsigned int), std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>> const&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>, unsigned int&&) base/functional/bind_internal.h:1069:14
    #61 0x7f94f60cb243 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int) base/functional/bind_internal.h:989:12
    #62 0x7f94f60c9e38 in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & base/functional/callback.h:346:12
    #63 0x7f94f60c8fee in mojo::SimpleWatcher::DiscardReadyState(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.h:192:14
    #64 0x7f94f60c96d1 in void base::internal::DecayedFunctorTraits<void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>::Invoke<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&>(void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&, unsigned int&&, mojo::HandleSignalsState const&) base/functional/bind_internal.h:673:12
    #65 0x7f94f60c9609 in void base::internal::InvokeHelper<false, base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, void, 0ul>::MakeItSo<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)>> const&, unsigned int, mojo::HandleSignalsState const&>(void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)>> const&, unsigned int&&, mojo::HandleSignalsState const&) base/functional/bind_internal.h:932:12
    #66 0x7f94f60c947c in void base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::RunImpl<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)>> const&, 0ul>(void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)>> const&, std::__Cr::integer_sequence<unsigned long, 0ul>, unsigned int&&, mojo::HandleSignalsState const&) base/functional/bind_internal.h:1069:14
    #67 0x7f94f60c927b in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) base/functional/bind_internal.h:989:12
    #68 0x7f94f1def340 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & base/functional/callback.h:346:12
    #69 0x7f94f1debbfa in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.cc:286:14
    #70 0x7f94f1def72f in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) mojo/public/cpp/system/simple_watcher.cc:97:22
    #71 0x7f94f1dee017 in mojo::SimpleWatcher::Context::CallNotify(MojoTrapEvent const*) mojo/public/cpp/system/simple_watcher.cc:61:14
    #72 0x7f94f1869305 in mojo::core::ipcz_driver::MojoTrap::DispatchEvent(MojoTrapEvent const&) mojo/core/ipcz_driver/mojo_trap.cc:605:3
    #73 0x7f94f18666c0 in mojo::core::ipcz_driver::MojoTrap::DispatchOrQueueEvent(mojo::core::ipcz_driver::MojoTrap::Trigger&, MojoTrapEvent const&) mojo/core/ipcz_driver/mojo_trap.cc:577:5
    #74 0x7f94f186878e in mojo::core::ipcz_driver::MojoTrap::HandleEvent(IpczTrapEvent const&) mojo/core/ipcz_driver/mojo_trap.cc:459:3
    #75 0x7f94f186814c in mojo::core::ipcz_driver::MojoTrap::TrapEventHandler(IpczTrapEvent const*) mojo/core/ipcz_driver/mojo_trap.cc:393:41
    #76 0x7f94f1a74c79 in ipcz::TrapEventDispatcher::DispatchAll() third_party/ipcz/src/ipcz/trap_event_dispatcher.cc:30:5
    #77 0x7f94f1a74a68 in ipcz::TrapEventDispatcher::~TrapEventDispatcher() third_party/ipcz/src/ipcz/trap_event_dispatcher.cc:12:3
    #78 0x7f94f1a44b56 in ipcz::Router::AcceptInboundParcel(std::__Cr::unique_ptr<ipcz::Parcel, std::__Cr::default_delete<ipcz::Parcel>>) third_party/ipcz/src/ipcz/router.cc:272:1
    #79 0x7f94f19a685b in ipcz::NodeLink::AcceptCompleteParcel(ipcz::StrongAlias<ipcz::SublinkIdTag, unsigned long>, std::__Cr::unique_ptr<ipcz::Parcel, std::__Cr::default_delete<ipcz::Parcel>>) third_party/ipcz/src/ipcz/node_link.cc:1082:31
    #80 0x7f94f19aa140 in ipcz::NodeLink::OnAcceptParcel(ipcz::msg::AcceptParcel&) third_party/ipcz/src/ipcz/node_link.cc:666:10
    #81 0x7f94f1a1e7e2 in ipcz::msg::NodeMessageListener::DispatchMessage(ipcz::Message&) third_party/ipcz/src/ipcz/node_messages.cc:914:14
    #82 0x7f94f1a188cd in ipcz::msg::NodeMessageListener::OnMessage(ipcz::Message&) third_party/ipcz/src/ipcz/node_messages.cc:611:10
    #83 0x7f94f1a1b552 in ipcz::msg::NodeMessageListener::OnTransportMessage(ipcz::DriverTransport::RawMessage const&, ipcz::DriverTransport const&, unsigned long) third_party/ipcz/src/ipcz/node_messages.cc:746:16
    #84 0x7f94f192150e in ipcz::DriverTransport::Notify(ipcz::DriverTransport::RawMessage const&, unsigned long) third_party/ipcz/src/ipcz/driver_transport.cc:129:20
    #85 0x7f94f1920e40 in ipcz::(anonymous namespace)::NotifyTransport(unsigned long, void const*, unsigned long, unsigned long const*, unsigned long, unsigned int, IpczTransportActivityOptions const*) third_party/ipcz/src/ipcz/driver_transport.cc:47:11
    #86 0x7f94f188d709 in mojo::core::ipcz_driver::Transport::OnChannelMessage(void const*, unsigned long, std::__Cr::vector<mojo::PlatformHandle, std::__Cr::allocator<mojo::PlatformHandle>>, scoped_refptr<mojo::core::ipcz_driver::Envelope>) mojo/core/ipcz_driver/transport.cc:744:29
    #87 0x7f94f17d3695 in mojo::core::Channel::TryDispatchMessage(base::span<char const, 18446744073709551615ul, char const*>, std::__Cr::optional<std::__Cr::vector<mojo::PlatformHandle, std::__Cr::allocator<mojo::PlatformHandle>>>, scoped_refptr<mojo::core::ipcz_driver::Envelope>, unsigned long*) mojo/core/channel.cc:1210:18
    #88 0x7f94f17d17c4 in mojo::core::Channel::TryDispatchMessage(base::span<char const, 18446744073709551615ul, char const*>, unsigned long*) mojo/core/channel.cc:1122:10
    #89 0x7f94f17d12ba in mojo::core::Channel::OnReadComplete(unsigned long, unsigned long*) mojo/core/channel.cc:1094:29
    #90 0x7f94f18a9d49 in mojo::core::ChannelPosix::OnFdReadable(int) mojo/core/channel_posix.cc:301:12
    #91 0x7f94f47d3949 in base::(anonymous namespace)::MessagePumpForIOFdWatchImpl::OnFileCanReadWithoutBlocking(int) base/message_loop/message_pump.cc:62:18
    #92 0x7f94f50f281d in base::MessagePumpEpoll::FdWatchController::OnFdReadable() base/message_loop/message_pump_epoll.cc:760:13
    #93 0x7f94f50f1dd1 in base::MessagePumpEpoll::HandleEvent(int, bool, bool, base::MessagePumpEpoll::FdWatchController*) base/message_loop/message_pump_epoll.cc:668:17
    #94 0x7f94f50f0e03 in base::MessagePumpEpoll::OnEpollEvent(base::MessagePumpEpoll::EpollEventEntry&, unsigned int) base/message_loop/message_pump_epoll.cc:614:7
    #95 0x7f94f50ed5a8 in base::MessagePumpEpoll::WaitForEpollEvents(base::TimeDelta) base/message_loop/message_pump_epoll.cc:506:7
    #96 0x7f94f50ec36a in base::MessagePumpEpoll::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_epoll.cc:248:12
    #97 0x7f94f4cb86c2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #98 0x7f94f4a0f0e7 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #99 0x7f94f4e33591 in base::Thread::Run(base::RunLoop*) base/threading/thread.cc:361:13
    #100 0x7f94cfd13a12 in content::(anonymous namespace)::ChildIOThread::Run(base::RunLoop*) content/child/child_process.cc:69:19
    #101 0x7f94f4e34241 in base::Thread::ThreadMain() base/threading/thread.cc:436:3
    #102 0x7f94f4f3406c in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #103 0x555f98508896 in asan_thread_start(void*) asan_interceptors.cpp

0x7cf38a35bad0 is located 336 bytes inside of 576-byte region [0x7cf38a35b980,0x7cf38a35bbc0)
freed by thread T5 (Chrome_ChildIOT) here:
    #0 0x555f9854e7c2 in operator delete(void*, unsigned long) (/mnt/lvm_data/chromium/src/out/asan_dbg_symbols/chrome+0xf3a07c2) (BuildId: 3afd3fb7d064a1b6)
    #1 0x7f94e5a691b6 in net::TransportClientSocketPool::Group::~Group() net/socket/transport_client_socket_pool.cc:1499:44
    #2 0x7f94e5a5c8fd in net::TransportClientSocketPool::RemoveGroup(std::__Cr::__map_iterator<std::__Cr::__tree_iterator<std::__Cr::__value_type<net::ClientSocketPool::GroupId, base::raw_ptr<net::TransportClientSocketPool::Group, (partition_alloc::internal::RawPtrTraits)1>>, std::__Cr::__tree_node<std::__Cr::__value_type<net::ClientSocketPool::GroupId, base::raw_ptr<net::TransportClientSocketPool::Group, (partition_alloc::internal::RawPtrTraits)1>>, void*>*, long>>) net/socket/transport_client_socket_pool.cc:995:3
    #3 0x7f94e5a5749a in net::TransportClientSocketPool::RemoveGroup(net::ClientSocketPool::GroupId const&) net/socket/transport_client_socket_pool.cc:990:3
    #4 0x7f94e5a5b13c in net::TransportClientSocketPool::OnAvailableSocketSlot(net::ClientSocketPool::GroupId const&, net::TransportClientSocketPool::Group*) net/socket/transport_client_socket_pool.cc:1172:5
    #5 0x7f94e5a66240 in net::TransportClientSocketPool::OnConnectJobComplete(net::TransportClientSocketPool::Group*, int, net::ConnectJob*) net/socket/transport_client_socket_pool.cc:1401:5
    #6 0x7f94e5a69323 in net::TransportClientSocketPool::Group::OnConnectJobComplete(int, net::ConnectJob*) net/socket/transport_client_socket_pool.cc:1510:24
    #7 0x7f94e594be00 in net::ConnectJob::NotifyDelegateOfCompletion(int) net/socket/connect_job.cc:181:13
    #8 0x7f94e59eea53 in net::SSLConnectJob::OnIOComplete(int) net/socket/ssl_connect_job.cc:187:5
    #9 0x7f94e59ef198 in net::SSLConnectJob::OnConnectJobComplete(int, net::ConnectJob*) net/socket/ssl_connect_job.cc:144:3
    #10 0x7f94e594be00 in net::ConnectJob::NotifyDelegateOfCompletion(int) net/socket/connect_job.cc:181:13
    #11 0x7f94e51e8c63 in net::HttpProxyConnectJob::OnIOComplete(int) net/http/http_proxy_connect_job.cc:400:5
    #12 0x7f94e51feb21 in void base::internal::DecayedFunctorTraits<void (net::HttpProxyConnectJob::*)(int), net::HttpProxyConnectJob*>::Invoke<void (net::HttpProxyConnectJob::*)(int), net::HttpProxyConnectJob*, int>(void (net::HttpProxyConnectJob::*)(int), net::HttpProxyConnectJob*&&, int&&) base/functional/bind_internal.h:740:12
    #13 0x7f94e51fe864 in void base::internal::InvokeHelper<false, base::internal::FunctorTraits<void (net::HttpProxyConnectJob::*&&)(int), net::HttpProxyConnectJob*>, void, 0ul>::MakeItSo<void (net::HttpProxyConnectJob::*)(int), std::__Cr::tuple<base::internal::UnretainedWrapper<net::HttpProxyConnectJob, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, int>(void (net::HttpProxyConnectJob::*&&)(int), std::__Cr::tuple<base::internal::UnretainedWrapper<net::HttpProxyConnectJob, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, int&&) base/functional/bind_internal.h:932:12
    #14 0x7f94e51fe5fc in void base::internal::Invoker<base::internal::FunctorTraits<void (net::HttpProxyConnectJob::*&&)(int), net::HttpProxyConnectJob*>, base::internal::BindState<true, true, false, void (net::HttpProxyConnectJob::*)(int), base::internal::UnretainedWrapper<net::HttpProxyConnectJob, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (int)>::RunImpl<void (net::HttpProxyConnectJob::*)(int), std::__Cr::tuple<base::internal::UnretainedWrapper<net::HttpProxyConnectJob, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(void (net::HttpProxyConnectJob::*&&)(int), std::__Cr::tuple<base::internal::UnretainedWrapper<net::HttpProxyConnectJob, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>, int&&) base/functional/bind_internal.h:1069:14
    #15 0x7f94e51fe433 in base::internal::Invoker<base::internal::FunctorTraits<void (net::HttpProxyConnectJob::*&&)(int), net::HttpProxyConnectJob*>, base::internal::BindState<true, true, false, void (net::HttpProxyConnectJob::*)(int), base::internal::UnretainedWrapper<net::HttpProxyConnectJob, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (int)>::RunOnce(base::internal::BindStateBase*, int) base/functional/bind_internal.h:982:12
    #16 0x7f94e4808b38 in base::OnceCallback<void (int)>::Run(int) && base/functional/callback.h:155:12
    #17 0x7f94e5b3ffe6 in net::SpdyProxyClientSocket::OnClose(int) net/spdy/spdy_proxy_client_socket.cc:634:31
    #18 0x7f94e5c25bfb in net::SpdyStream::OnClose(int) net/spdy/spdy_stream.cc:585:15
    #19 0x7f94e5b7290d in net::SpdySession::DeleteStream(std::__Cr::unique_ptr<net::SpdyStream, std::__Cr::default_delete<net::SpdyStream>>, int) net/spdy/spdy_session.cc:2581:11
    #20 0x7f94e5b65455 in net::SpdySession::CloseActiveStreamIterator(std::__Cr::__map_iterator<std::__Cr::__tree_iterator<std::__Cr::__value_type<unsigned int, net::SpdyStream*>, std::__Cr::__tree_node<std::__Cr::__value_type<unsigned int, net::SpdyStream*>, void*>*, long>>, int) net/spdy/spdy_session.cc:1804:3
    #21 0x7f94e5b68281 in net::SpdySession::StartGoingAway(unsigned int, net::Error) net/spdy/spdy_session.cc:1362:5
    #22 0x7f94e5b5ee7c in net::SpdySession::DoDrainSession(net::Error, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, bool) net/spdy/spdy_session.cc:2680:5
    #23 0x7f94e5b70369 in net::SpdySession::CreateStream(net::SpdyStreamRequest const&, base::WeakPtr<net::SpdyStream>*) net/spdy/spdy_session.cc:1694:5
    #24 0x7f94e5b552c1 in net::SpdySession::TryCreateStream(base::WeakPtr<net::SpdyStreamRequest> const&, base::WeakPtr<net::SpdyStream>*) net/spdy/spdy_session.cc:1663:12
    #25 0x7f94e5b53e98 in net::SpdyStreamRequest::StartRequest(net::SpdyStreamType, base::WeakPtr<net::SpdySession> const&, GURL const&, bool, net::RequestPriority, net::SocketTag const&, net::NetLogWithSource const&, base::OnceCallback<void (int)>, net::NetworkTrafficAnnotationTag const&, bool, base::TimeDelta) net/spdy/spdy_session.cc:617:17
    #26 0x7f94e51ee252 in net::HttpProxyConnectJob::DoSpdyProxyCreateStream() net/http/http_proxy_connect_job.cc:696:32
    #27 0x7f94e51ea44d in net::HttpProxyConnectJob::DoLoop(int) net/http/http_proxy_connect_job.cc:443:14
    #28 0x7f94e51e9c39 in net::HttpProxyConnectJob::ConnectInternal() net/http/http_proxy_connect_job.cc:389:10
    #29 0x7f94e594b2ea in net::ConnectJob::Connect() net/socket/connect_job.cc:130:12

previously allocated by thread T5 (Chrome_ChildIOT) here:
    #0 0x555f9854dbbd in operator new(unsigned long) (/mnt/lvm_data/chromium/src/out/asan_dbg_symbols/chrome+0xf39fbbd) (BuildId: 3afd3fb7d064a1b6)
    #1 0x7f94e5a561ea in net::TransportClientSocketPool::GetOrCreateGroup(net::ClientSocketPool::GroupId const&) net/socket/transport_client_socket_pool.cc:981:18
    #2 0x7f94e5a558df in net::TransportClientSocketPool::RequestSocketInternal(net::ClientSocketPool::GroupId const&, net::TransportClientSocketPool::Request const&, base::OnceCallback<void ()>) net/socket/transport_client_socket_pool.cc:454:11
    #3 0x7f94e5a5471d in net::TransportClientSocketPool::RequestSocket(net::ClientSocketPool::GroupId const&, scoped_refptr<net::ClientSocketPool::SocketParams>, std::__Cr::optional<net::NetworkTrafficAnnotationTag> const&, net::RequestPriority, net::SocketTag const&, net::ClientSocketPool::RespectLimits, net::ClientSocketHandle*, base::OnceCallback<void (int)>, base::RepeatingCallback<void (net::HttpResponseInfo const&, net::HttpAuthController*, base::OnceCallback<void ()>)> const&, net::NetLogWithSource const&) net/socket/transport_client_socket_pool.cc:274:7
    #4 0x7f94e593149b in net::ClientSocketHandle::Init(net::ClientSocketPool::GroupId const&, scoped_refptr<net::ClientSocketPool::SocketParams>, std::__Cr::optional<net::NetworkTrafficAnnotationTag> const&, net::RequestPriority, net::SocketTag const&, net::ClientSocketPool::RespectLimits, base::OnceCallback<void (int)>, base::RepeatingCallback<void (net::HttpResponseInfo const&, net::HttpAuthController*, base::OnceCallback<void ()>)> const&, net::ClientSocketPool*, net::NetLogWithSource const&) net/socket/client_socket_handle.cc:51:19
    #5 0x7f94e5940a1e in net::(anonymous namespace)::InitSocketPoolHelper(url::SchemeHostPort, int, net::RequestPriority, net::HttpNetworkSession*, net::ProxyInfo const&, std::__Cr::vector<net::SSLConfig::CertAndStatus, std::__Cr::allocator<net::SSLConfig::CertAndStatus>> const&, net::PrivacyMode, net::NetworkAnonymizationKey, net::SecureDnsPolicy, net::SocketTag const&, net::NetLogWithSource const&, int, net::ClientSocketHandle*, net::HttpNetworkSession::SocketPoolType, base::OnceCallback<void (int)>, base::RepeatingCallback<void (net::HttpResponseInfo const&, net::HttpAuthController*, base::OnceCallback<void ()>)> const&) net/socket/client_socket_pool_manager.cc:131:25
    #6 0x7f94e594009d in net::InitSocketHandleForHttpRequest(url::SchemeHostPort, int, net::RequestPriority, net::HttpNetworkSession*, net::ProxyInfo const&, std::__Cr::vector<net::SSLConfig::CertAndStatus, std::__Cr::allocator<net::SSLConfig::CertAndStatus>> const&, net::PrivacyMode, net::NetworkAnonymizationKey, net::SecureDnsPolicy, net::SocketTag const&, net::NetLogWithSource const&, net::ClientSocketHandle*, base::OnceCallback<void (int)>, base::RepeatingCallback<void (net::HttpResponseInfo const&, net::HttpAuthController*, base::OnceCallback<void ()>)> const&) net/socket/client_socket_pool_manager.cc:226:10
    #7 0x7f94e52d9296 in net::HttpStreamFactory::Job::DoInitConnectionImpl() net/http/http_stream_factory_job.cc:823:10
    #8 0x7f94e52d43dd in net::HttpStreamFactory::Job::DoInitConnection() net/http/http_stream_factory_job.cc:702:16
    #9 0x7f94e52d289b in net::HttpStreamFactory::Job::DoLoop(int) net/http/http_stream_factory_job.cc:630:14
    #10 0x7f94e52d14a5 in net::HttpStreamFactory::Job::RunLoop(int) net/http/http_stream_factory_job.cc:531:12
    #11 0x7f94e52c877e in net::HttpStreamFactory::Job::StartInternal() net/http/http_stream_factory_job.cc:655:3
    #12 0x7f94e52c8553 in net::HttpStreamFactory::Job::Start(net::HttpStreamRequest::StreamType) net/http/http_stream_factory_job.cc:246:3
    #13 0x7f94e5307007 in net::HttpStreamFactory::JobController::DoCreateJobs() net/http/http_stream_factory_job_controller.cc:1026:16
    #14 0x7f94e53027b0 in net::HttpStreamFactory::JobController::DoLoop(int) net/http/http_stream_factory_job_controller.cc:807:14
    #15 0x7f94e52f4629 in net::HttpStreamFactory::JobController::RunLoop(int) net/http/http_stream_factory_job_controller.cc:765:12
    #16 0x7f94e52f41aa in net::HttpStreamFactory::JobController::Start(net::HttpStreamRequest::Delegate*, net::WebSocketHandshakeStreamBase::CreateHelper*, net::NetLogWithSource const&, net::HttpStreamRequest::StreamType, net::RequestPriority) net/http/http_stream_factory_job_controller.cc:232:3
    #17 0x7f94e52bec72 in net::HttpStreamFactory::RequestStreamInternal(net::HttpRequestInfo const&, net::RequestPriority, std::__Cr::vector<net::SSLConfig::CertAndStatus, std::__Cr::allocator<net::SSLConfig::CertAndStatus>> const&, net::HttpStreamRequest::Delegate*, net::WebSocketHandshakeStreamBase::CreateHelper*, net::HttpStreamRequest::StreamType, bool, bool, bool, net::NetLogWithSource const&) net/http/http_stream_factory.cc:232:34
    #18 0x7f94e52be8a7 in net::HttpStreamFactory::RequestStream(net::HttpRequestInfo const&, net::RequestPriority, std::__Cr::vector<net::SSLConfig::CertAndStatus, std::__Cr::allocator<net::SSLConfig::CertAndStatus>> const&, net::HttpStreamRequest::Delegate*, bool, bool, net::NetLogWithSource const&) net/http/http_stream_factory.cc:163:10
    #19 0x7f94e517a039 in net::HttpNetworkTransaction::DoCreateStream() net/http/http_network_transaction.cc:1136:56
    #20 0x7f94e516bc40 in net::HttpNetworkTransaction::DoLoop(int) net/http/http_network_transaction.cc:1009:14
    #21 0x7f94e516add0 in net::HttpNetworkTransaction::Start(net::HttpRequestInfo const*, base::OnceCallback<void (int)>, net::NetLogWithSource const&) net/http/http_network_transaction.cc:426:12
    #22 0x7f94a0e21307 in network::ThrottlingNetworkTransaction::Start(net::HttpRequestInfo const*, base::OnceCallback<void (int)>, net::NetLogWithSource const&) services/network/throttling/throttling_network_transaction.cc:137:34
    #23 0x7f94e5920665 in net::SharedDictionaryNetworkTransaction::Start(net::HttpRequestInfo const*, base::OnceCallback<void (int)>, net::NetLogWithSource const&) net/shared_dictionary/shared_dictionary_network_transaction.cc:114:34
    #24 0x7f94e50c5eeb in net::HttpCache::Transaction::DoSendRequest() net/http/http_cache_transaction.cc:1921:28
    #25 0x7f94e50af243 in net::HttpCache::Transaction::DoLoop(int) net/http/http_cache_transaction.cc:910:14
    #26 0x7f94e50abf1c in net::HttpCache::Transaction::Start(net::HttpRequestInfo const*, base::OnceCallback<void (int)>, net::NetLogWithSource const&) net/http/http_cache_transaction.cc:213:12
    #27 0x7f94e5d00264 in net::URLRequestHttpJob::StartTransactionInternal() net/url_request/url_request_http_job.cc:782:26
    #28 0x7f94e5cff301 in net::URLRequestHttpJob::MaybeStartTransactionInternal(int) net/url_request/url_request_http_job.cc:713:5
    #29 0x7f94e5cfc976 in net::URLRequestHttpJob::StartTransaction() net/url_request/url_request_http_job.cc:692:5

Thread T5 (Chrome_ChildIOT) created by T0 (chrome) here:
    #0 0x555f984ee6c1 in pthread_create (/mnt/lvm_data/chromium/src/out/asan_dbg_symbols/chrome+0xf3406c1) (BuildId: 3afd3fb7d064a1b6)
    #1 0x7f94f4f32b69 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) base/threading/platform_thread_posix.cc:153:13
    #2 0x7f94f4f326c8 in base::PlatformThreadBase::CreateWithType(unsigned long, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) base/threading/platform_thread_posix.cc:322:10
    #3 0x7f94f4e30866 in base::Thread::StartWithOptions(base::Thread::Options) base/threading/thread.cc:228:26
    #4 0x7f94cfd11705 in content::ChildProcess::ChildProcess(base::ThreadType, std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>, bool) content/child/child_process.cc:152:21
    #5 0x7f94dd2a0149 in content::UtilityMain(content::MainFunctionParams) content/utility/utility_main.cc:459:16
    #6 0x7f94dd5cb0ad in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:762:14
    #7 0x7f94dd5ce956 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1152:10
    #8 0x7f94dd5c47af in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:358:36
    #9 0x7f94dd5c5625 in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:371:10
    #10 0x555f9854f700 in ChromeMain chrome/app/chrome_main.cc:191:12
    #11 0x555f9854ef61 in main chrome/app/chrome_exe_main_aura.cc:17:10
    #12 0x7f93b39f1d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

SUMMARY: AddressSanitizer: heap-use-after-free net/socket/transport_client_socket_pool.h:350:14 in net::TransportClientSocketPool::Group::IsEmpty() const
Shadow bytes around the buggy address:
  0x7cf38a35b800: 00 07 00 06 fc 00 fc fc fc fc fc fc fc fc fc fc
  0x7cf38a35b880: fc fc fc fc fc fc fc fc fa fa fa fa fa fa fa fa
  0x7cf38a35b900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x7cf38a35b980: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7cf38a35ba00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x7cf38a35ba80: fd fd fd fd fd fd fd fd fd fd[fd]fd fd fd fd fd
  0x7cf38a35bb00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7cf38a35bb80: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x7cf38a35bc00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x7cf38a35bc80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7cf38a35bd00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==3183368==ADDITIONAL INFO

==3183368==Note: Please include this section with the ASan report.
Task trace:


Command line: `/proc/self/exe --type=utility --utility-sub-type=network.mojom.NetworkService --lang=en-US --service-sandbox-type=network --host-resolver-rules=MAP * 0.0.0.0,EXCLUDE localhost,EXCLUDE 127.0.0.1 --no-sandbox --ignore-certificate-errors --use-angle=swiftshader-webgl --disable-quic --ignore-certificate-errors --crashpad-handler-pid=3183342 --enable-crash-reporter=, --noerrdialogs --user-data-dir=/home/c/r72exact/profiles/chrome_profile_01emo4h6 --change-stack-guard-on-fork=enable --shared-files=network_parent_dirs_pipe:100,v8_context_snapshot_data:101 --field-trial-handle=3,i,7858556789988091250,7114296443668740500,262144 --enable-features=PaintHolding --variations-seed-version --pseudonymization-salt-handle=7,i,15791728013565851972,9863046745450112241,4 --trace-process-track-uuid=3950953896855098051`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==3183368==END OF ADDITIONAL INFO

==3183368==ABORTING


```
## VERSION

Chrome Version: Chromium 147.0.7703.0 and Chromium 148.0.7729.0 dev ASAN builds  

Operating System: Linux x86\_64 on the two hosts (Ubuntu 22.04.3 LTS class and Ubuntu 25.04 class)

## REPRODUCTION CASE

Primary HTML artifact: `min_poc.html`  

Harness script: `launch_standalone.sh`

Run Chrome with flags (for reliable repro, not root cause of the bugs):
`--proxy-server=https://127.0.0.1:<port> --proxy-bypass-list=localhost;127.0.0.1;[::1] --ignore-certificate-errors --disable-quic --disable-domain-reliability --metrics-recording-only --disable-default-apps --disable-sync --host-resolver-rules=MAP * 0.0.0.0,EXCLUDE localhost,EXCLUDE 127.0.0.1 --headless=new`

### Fast Path

From this directory:

```
export CHROMIUM_PATH=/path/to/chrome
./launch_standalone.sh

```

What this does:

- starts `min_repro.py` in `HELPER_ONLY=1` mode
- binds the local controller server on `CONTROLLER_PORT` (default `8872`)
- binds the local HTTPS H2 proxy on `PROXY_PORT` (default `8873`)
- launches Chrome directly against:
  - `http://127.0.0.1:${CONTROLLER_PORT}/min_poc.html?autorun=1`
- applies the proxy and network flags needed by this PoC

### Manual Equivalent

If you want to launch Chrome yourself instead of using the wrapper:

1. Start the helper:

```
export CONTROLLER_PORT=8872
export PROXY_PORT=8873
HELPER_ONLY=1 python3 min_repro.py

```

2. In another shell, launch Chrome:

```
export CHROMIUM_PATH=/path/to/chrome
"$CHROMIUM_PATH" \
  --no-sandbox \
  --ignore-certificate-errors \
  --disable-background-networking \
  --disable-quic \
  --disable-domain-reliability \
  --metrics-recording-only \
  --disable-default-apps \
  --disable-sync \
  --host-resolver-rules="MAP * 0.0.0.0,EXCLUDE localhost,EXCLUDE 127.0.0.1" \
  --proxy-server="https://127.0.0.1:${PROXY_PORT}" \
  --proxy-bypass-list="localhost;127.0.0.1;[::1]" \
  "http://127.0.0.1:${CONTROLLER_PORT}/min_poc.html?autorun=1"

```
## FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: Network Service utility-process crash
Crash State: Representative callsite family `net::TransportClientSocketPool::Group::IsEmpty() const`; sanitizer log example `asan_heap_uaf_exact.log`
ASAN type: heap-use-after-free

## CREDIT INFORMATION

Reporter credit: heapracer

## Attachments

- [launch_standalone.sh](attachments/launch_standalone.sh) (text/x-sh, 1.5 KB)
- [min_repro.py](attachments/min_repro.py) (text/x-python, 15.9 KB)
- [min_poc.html](attachments/min_poc.html) (text/html, 3.7 KB)
- [utils.py](attachments/utils.py) (text/x-python, 13.3 KB)
- [input_72.html](attachments/input_72.html) (text/html, 9.3 KB)
- [original_exact.py](attachments/original_exact.py) (text/x-python, 20.7 KB)

## Timeline

### es...@chromium.org (2026-03-18)

I haven't reproduced this yet because I'm waiting on an asan build to finish, but I'm going to tentatively triage this as S0 and add owners.

### es...@chromium.org (2026-03-18)

I can't reproduce this on 148.0.7737.0. Reporter, is there any other information you can provide that might help with a repro? Thank you.

### mm...@chromium.org (2026-03-18)

So, presumably, for this to happen, in the lines:

```
  group = GetOrCreateGroup(group_id);
  ...
  int rv = connect_job->Connect();

```

The Connect() call would have to delete the group. There are some other calls, but none of them can delete a group. I guess it's also possible GetOrCreateGroup is returning an invalid object, but that seems unlikely. Connecting a job should not in general be able to tear down a group - it does not call back into the socket pool. HttpProxyConnectJob does access H2/H3 sessions, but I'm unaware of that being able to result in tearing down a connection tunneled through the proxy.

### sh...@gmail.com (2026-03-18)

Hi, it seems that my minimization makes the PoC work only on one host because it requires a proper race condition. Sorry about that. I have attached the original full PoC below, which can reliably reproduce on any host after a few runs. I will keep pushing on the minimization front.

```
while true; do ASAN_OPTIONS=detect_odr_violation=0   CHROMIUM_PATH=/path/to/chrome   python3 original_exact.py; done

```

### es...@chromium.org (2026-03-18)

(adding more cc's, people who touched this code recently)

### es...@chromium.org (2026-03-19)

Ok I repro'ed with the scripts in #5. Thank you! A minimized PoC would still be very helpful as it's hard to understand from utils.py how Chromium is actually being run and whether this could trigger in out-of-the-box Chrome usage.

### es...@chromium.org (2026-03-19)

Reproduces as far back as M145, so not a very recent regression

### ch...@google.com (2026-03-19)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-19)

Setting Priority to P0 to match Severity s0. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### mm...@chromium.org (2026-03-19)

So, looking at the repro, it appears to load HTTPS resources from a localhost HTTP page in groups of 3 from an HTTPS host, then increments the host, and repeats. An HTTPS proxy is configured (which uses H2), so the situation is most like All/HttpNetworkTransactionTest.HttpsProxySpdyConnectHttps/0 (There are also a pair of tests with an H2 proxy and two requests and one/two destination servers in the same file, but those tests don't use auth). The proxy appears to unconditionally send HTTPS auth challenges, even if credentials are required.

So there are a couple interesting things going on there that may be relevant:

1. Multiple connections at once to the same destination through an authenticating H2 proxy.
2. Multiple connections at once to different destinations through an authenticating H2 proxy (possibly with an existing connection to it)
3. Proxy demanding auth again, even if credentials are provided.

I haven't reproduced the issue locally yet. I'm not sure if the crash is the credentials are provided case, or the continue without them case, both, or the crash happens before we reach that point.

### mm...@chromium.org (2026-03-19)

<https://chromium-review.googlesource.com/c/chromium/src/+/1080587> fixed an issue much like this by moving GetOrCreateGroup() after the Connect() call. In a refactor back in 2019 (<https://chromium-review.googlesource.com/c/chromium/src/+/1532825>), I substantially reworked the class, and moved the GetOrCreateGroup() group call back before the Connect() call, which was not caught by the regression test added in the first CL.

The fix was due to a DoH issue, not a proxy issue, and I'm still not setting how H2 proxies could cause the problem, but I do think the fix will be the same - don't hold onto the Group during the Connect() call.

### mm...@chromium.org (2026-03-19)

Note that I haven't confirmed that is actually the cause of these specific crashes, and don't currently have a theory about how the current group is being destroyed.

Current plan of approach is to dig into that DNS test, see why it's not triggering the issue, and if I can't figure out why, only then dig into H2. If I can repro with DNS, I'll write a test and fix it, and then potentially dig into reproducing via H2 afterwards.

### mm...@chromium.org (2026-03-19)

<https://source.chromium.org/chromium/chromium/src/+/main:net/socket/transport_client_socket_pool.cc;l=911> is likely why the regression wasn't noticed - if there are no idle sockets, we now don't bother looking for groups we can clean up. Moreover, due to <https://chromium-review.googlesource.com/c/chromium/src/+/3457644>, it's likely DoH no longer surfaces the issue, so this may be H2 proxy only.

Anyhow, that's where I'm stopping for the day, if anyone else is interested in looking into this in the meantime.

### mm...@chromium.org (2026-03-23)

I'm having trouble understanding how this can happen. Looking at the code, SpdySessions are only deleted from fresh post tasks when there's nothing else on the stack, so it doesn't seem like the connect call is likely deleting a SpdySession, which could invalidate the group. DoH, the other likely culprit, has a PostTask to prevent that from happening as well.

I could just make the code robust against ConnectJob::Connect() deleting the current socket's group, which is independently probably a good thing to do, but without being able to reproduce, I'm not confident that is what the issue here is, nor am I able to write a full regression test, as opposed to just a request with just a mock socket that calls back into the socket pool.

It's possible that the SSL layer is calling back into the socket pools, if the proxy is being used for OCSP requests, but the test uses self-signed certs, so that seems unlikely (as does the fact that the repro needs to use H2 proxy auth).

### mm...@chromium.org (2026-03-23)

Don't have a repro yet, but I believe I understand the issue now. It's a SPDY bug, not a socket pool one, and may not only affect proxies.

Trying to get a non-proxy test to trigger the issue. Fix should be easy.

### mm...@chromium.org (2026-03-24)

So, it actually turns out this is not hit by the main path. The issue is when SpdyStreamRequest::RequestStream() is the first call to notice a SpdySession has a closed socket via Socket::IsConnected(). The main HTTP path uses std::make\_unique<SpdyHttpStream>() instead of SpdyStreamRequest::RequestStream() (A pattern which looks like it bypasses the prioritized per-SpdySession SpdyStream creation queue? There's a TODO to remove that line, probably because of that issue)

So as a result of that potential priority bypass bug, the issue "only" affects H2 proxies, WebSockets, and bidirectional streams, I believe.

### mm...@chromium.org (2026-03-25)

Full description of the issue, for the record:

We have a full negotiated connection through the proxy, with some HttpProxyConnectJobs busy setting up tunnels over it. By the stack trace, SpdyProxyClientSocket has probably tried to send the CONNECT request and is either waiting it to be sent, or waiting on the response headers to verify the tunnel has been created.

Then a new request comes into the proxy socket pool to the same final destination as the connection we're trying to establish. We have fewer than six connections tunneled through the proxy to that destination, so TransportClientSocketPool::RequestSocket tries to make a new one.

It calls "MakeOrCreateGroup" and creates or gets a new group, and makes a HttpProxyConnectJob using it as its delegate. We then tell it to connect. The HttpProxyConnectJob finds the existing proxy session, and tries to create new stream over it. When doing so, SpdySession discovers the socket has been closed, and instantly tears down all the SpdyStreams on the proxy spdy session. That includes the other already connecting HttpProxyConnectJobs, to the same destination. They're torn down, and notice that the group the request is to has no active connection attempts, so it removes the Group. The Group is currently on the stack, as the delegate to the new HttpProxyConnectJob we're creating, so when we work the way back up the stack, we have an invalid pointer to the group.

It is not clear if it's possible to hit this same issue if either all live tunnels are to different destinations, or all other tunnels to the same destination have already been fully established, and passed out of the socket pool. It's also not clear if the network service prioritization CL makes this more likely to happen, by having some requests preempt the pending read error we presumably have on the socket.

So there are two issues here:

1. The SpdySession is synchronously calling into a bunch of stuff when there's another class on the stack. informing all consumers at once of destruction is fine, as long as there SpdySession is on the top of the callstack, but it's absolutely not safe when there's a 3P caller. There may be other places were DoDrainSession() / StartGoingAway() is called from callstacks with external callers on the top of the stack. Ideally we'd make this a safe thing to do.
2. TransportClientSocketPool has a Group on the stack that may be deleted. We've run into issues with this before, with DNS over HTTPS.

We could try to fix 2) by keeping the Group alive while on the stack (Adding the new connection attempt to the group to keep it alive seems risks, since then the ConnectJob could be deleted out from under us as well, so we'd probably just want to set a value in it telling us to keep it around. We can't just recreate the group if destroyed, since it's the ConnectJob's delegate, and the ConnectJob has a raw pointer to it). Allowing reentrancy does seem risky, though. CHECKing when the group is destroyed out from under us, or even just on reentrant calls, might be a better idea.

For trying to generally fix 2), adding PostTasks to prevent that is difficult, because the SpdySession owns the SpdyStreams. We could add post tasks to the classes that use SpdyStreams, but there are 3 (SpdyProxyClientSocket, SpdyHttpStream, and BidirectionalStreamSpdyImpl), and locking them all down seems like a fair bit of effort, and could easily regress, and any new consumer would run into the same issue.

We could just make HttpProxyConnectJob failure async in this case, which would mean that there's still reentrancy from the SpdySession, but we wouldn't get this specific crash...though there may be other cases where we could reenter either with proxy SPDY sessions (e.g., after a connection is established), or with other consumers. We could have HttpProxyConnectJob always start asynchronously, which would be a more robust workaround for issues around HttpProxyConnectJobs specifically, and probably the most robust quick fix I've thought of, but SpdySession would still be reentrant, and we could potentially have UAFs in other cases.

The design of SpdySession owning its SpdyStreams seems to me like the design choice that makes fixing SpdySession hard. If SpdyStreams were owned by their consumers instead, we could (probably) make SpdyStreams defer close notifications, and return read/write errors until the notifications were send out, and call it a day, but since the SpdySession owns them, that's more difficult. We could have it defer deleting of the SpdyStreams, but that seems risky - there's a lot going on in the SpdySession, and adding yet a new state to its state machine seems sufficiently tricky to me as to not be a good place to start fixing this. Admittedly, I may feel differently if I were an expert on the class and its read/write machinery, but I very much am not.

A simpler more limited fix would be to have SpdySession::CreateStream(), when it detects this situation and the SpdySession has any other consumers (if there are no other consumers, we do need to tear down the SpdySession, and nothing is likely reading from the socket, so we'll still need to destroy it. SpdySession lifetime logic seems super finicky to me, unfortunately). When there are other consumers, we could return an error without shutting down the SpdySession. The problem with that is we could theoretically get into a retry loop, since the SpdySession would still be discoverable by new requests. We could try making the SpdySession not discoverable, but still start shutting it down, but that's a new state for the entire SpdySession, and as mentioned, the SpdySession state machinery is scary.

A safer variant of the above would be to post a task to drain asynchronously when we detect this situation. If something else triggers draining in the meantime, we'd be fine. So we wouldn't need to care if there are another other consumers or not. That still runs into the reuse problem. We could potentially avoid reuse loops by calling MakeUnavailable(), and then calling DoDrainSession() asynchronously to actually tear things down, which is save once we have nothing above us on the callstack.

I am leaning towards the last of those, because it looks the simplest and the safest. My main concern with that approach is that nothing does it, currently. MakeUnavailable() is always followed by DoDrainSession() or StartGoingAway(), both of which reentrantly notify consumers, so we can't safely invoke them.

### mm...@chromium.org (2026-03-25)

I've done some more spelunking, and it turns out that we used to have a case where unavailable SpdySessions were not set as going away, in the network change case. That was changed because the SpdySessions were never being destroyed, which would eventually cause new connections to the destination with the eternally extant SpdySessions to hang, waiting for the old SpdySessions to free up socket pool slots. The fix was to make them go away as well.

Since my proposal is to mark them as unavailable and additionally post a task, I think we're fine on that front, so I am going to go ahead and implement an asyn drain call that marks a session as unavailable immediately, and posts a task to actually drain. I am a bit concerned that there may be other places we should be doing this. SpdySession::GetRemoteEndpoint() is the one that looks most problematic, of course. SpdySessionPool::OnSSLConfigForServersChanged() also looks a bit suspicious, as it's actually called indirectly from a number of places in the URLRequest stack, which all look safe-ish, but still seems not great.

There may well be others, I'm just not that familiar with what events are only triggered from reads/writes, and if all reads/writes happen async or not.

### es...@chromium.org (2026-03-26)

mmenke thank you for this excellent investigation!! I'm wondering if I should downgrade the severity on this to S1, as it would be a mitigating factor if the victim needs to have a proxy configured and/or the attacker needs to be in a privileged network position. I'll read through your comments more in detail later to form a more-informed opinion on this, but please let me know if you have an opinion on that.

### mm...@chromium.org (2026-03-27)

It is possible that it could be triggered by WebSockets or BidirectionalStreams without a proxy as well, but they're above the socket pool layer, so the issue would look very different. Unfortunately, it would take yet more investigation to figure out if either of those could cause a crash. Unfortunately, I just don't have the cycles to spend investigating that.

Similarly, it's also possible the `features::kDrainSpdySessionSynchronouslyOnRemoteEndpointDisconnect` experiment could cause the same issue through some rather different callstack, even with normal requests, but that would also require investigation - it's on M147, and without any changes, will be on stable when 147 hits stable, so we can just disable the experiment. That's not my experiment, so not going to dig into that, either.

### dx...@google.com (2026-03-27)

Project: chromium/src  

Branch:  main  

Author:  Matt Menke [mmenke@chromium.org](mailto:mmenke@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7701714>

Make SpdySession::CreateStream() call DoDrainSession() asynchronously.

---


Expand for full commit details
```
     
    Calling it synchronously would tear down all SpdyStreams immediately, 
    informing their consumers of the error. This could have side effects 
    that affect the caller trying to create the stream, so was unsafe. 
     
    This does introduce a state where a SpdySession is going away, but 
    neither DoDrainSession() nor StartGoingAway() was invoked. The 
    SpdySession never reached such a state before this CL, but this state 
    was used before - when there was a network change, we used to move 
    SpdySessions into such a state. This behavior was removed because we 
    ended up never actually closing those sockets, which could effectively 
    blackhole a destination. Since this CL posts a task to drain the 
    session, that shouldn't happen here. 
     
    The code is robust against extra DoDrainSession() calls, so it should 
    be fine if the session discovers through another path it should start 
    draining or otherwise going away, 
     
    Bug: 493628982 
    Change-Id: I23f1517b67fb55edd50d6e8fc8f1b4d8328e8ec5 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7701714 
    Reviewed-by: Kenichi Ishibashi <bashi@chromium.org> 
    Commit-Queue: mmenke <mmenke@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1606281}

```

---

Files:

- M `net/socket/socket_test_util.cc`
- M `net/socket/socket_test_util.h`
- M `net/spdy/spdy_session.cc`
- M `net/spdy/spdy_session.h`
- M `net/spdy/spdy_session_unittest.cc`

---

Hash: [4073d491fb559e9efe56759b92dfe387f490ed5a](https://chromiumdash.appspot.com/commit/4073d491fb559e9efe56759b92dfe387f490ed5a)  

Date: Fri Mar 27 16:19:35 2026


---

### ch...@google.com (2026-03-31)

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to stable (M146) because latest trunk commit (1606281) appears to be after stable branch point (1582197).

Merge review required: M146 is already shipping to stable.

Requesting merge to beta (M147) because latest trunk commit (1606281) appears to be after beta branch point (1596535).

Merge review required: M147 has already been cut for stable release.

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dr...@chromium.org (2026-03-31)

No crashes in Canary after 24 hours. Approved to merge to M146 and M147.

### sp...@google.com (2026-04-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
Mildly mitigated (priviledged process) 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### dr...@chromium.org (2026-04-03)

mmenke@ - friendly ping on the merge to M147 here. We're not planning any more releases of M146, so no need to do that.

### ch...@google.com (2026-04-04)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-04-08)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### mm...@chromium.org (2026-04-08)

[drubery] Sorry, I often do not get emails when Chromium issues are updated, particularly security restricted issues (though sometimes I do get emails, strangely). I've filed multiple bugs about this, with the relevant folks either blaming gmail or saying it's working as intended for "security" purposes. Unfortunately, as a result, the tracker is effectively an unreliable means of communication. I have no idea why this issue only affects a limited number of people (have heard from a couple others with the issue in the path), but have lost any hope of a fix.

Anyhow, I've sent out a merge request.

### dx...@google.com (2026-04-09)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Matt Menke [mmenke@chromium.org](mailto:mmenke@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7736370>

[M147] Make SpdySession::CreateStream() call DoDrainSession() asynchronously.

---


Expand for full commit details
```
     
    Calling it synchronously would tear down all SpdyStreams immediately, 
    informing their consumers of the error. This could have side effects 
    that affect the caller trying to create the stream, so was unsafe. 
     
    This does introduce a state where a SpdySession is going away, but 
    neither DoDrainSession() nor StartGoingAway() was invoked. The 
    SpdySession never reached such a state before this CL, but this state 
    was used before - when there was a network change, we used to move 
    SpdySessions into such a state. This behavior was removed because we 
    ended up never actually closing those sockets, which could effectively 
    blackhole a destination. Since this CL posts a task to drain the 
    session, that shouldn't happen here. 
     
    The code is robust against extra DoDrainSession() calls, so it should 
    be fine if the session discovers through another path it should start 
    draining or otherwise going away, 
     
    (cherry picked from commit 4073d491fb559e9efe56759b92dfe387f490ed5a) 
     
    Bug: 493628982 
    Change-Id: I23f1517b67fb55edd50d6e8fc8f1b4d8328e8ec5 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7701714 
    Reviewed-by: Kenichi Ishibashi <bashi@chromium.org> 
    Commit-Queue: mmenke <mmenke@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1606281} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7736370 
    Reviewed-by: mmenke <mmenke@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7727@{#2503} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `net/socket/socket_test_util.cc`
- M `net/socket/socket_test_util.h`
- M `net/spdy/spdy_session.cc`
- M `net/spdy/spdy_session.h`
- M `net/spdy/spdy_session_unittest.cc`

---

Hash: [f84f4fa22bf36882e059da80352c35c27b34b1dc](https://chromiumdash.appspot.com/commit/f84f4fa22bf36882e059da80352c35c27b34b1dc)  

Date: Thu Apr 9 02:06:51 2026


---

### pe...@google.com (2026-04-09)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2026-04-16)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-04-16)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7749087
2. Low - There was no conflict.
3. 147
4. Yes, the bug seems to be introduced in 2019.

### pe...@google.com (2026-04-16)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-04-16)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7747749
2. Low - There was no conflict.
3. 147
4. Yes, the bug seems to be introduced in 2019.

### dx...@google.com (2026-04-22)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Matt Menke [mmenke@chromium.org](mailto:mmenke@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7749087>

[M144-LTS] Make SpdySession::CreateStream() call DoDrainSession() asynchronously.

---


Expand for full commit details
```
     
    Calling it synchronously would tear down all SpdyStreams immediately, 
    informing their consumers of the error. This could have side effects 
    that affect the caller trying to create the stream, so was unsafe. 
     
    This does introduce a state where a SpdySession is going away, but 
    neither DoDrainSession() nor StartGoingAway() was invoked. The 
    SpdySession never reached such a state before this CL, but this state 
    was used before - when there was a network change, we used to move 
    SpdySessions into such a state. This behavior was removed because we 
    ended up never actually closing those sockets, which could effectively 
    blackhole a destination. Since this CL posts a task to drain the 
    session, that shouldn't happen here. 
     
    The code is robust against extra DoDrainSession() calls, so it should 
    be fine if the session discovers through another path it should start 
    draining or otherwise going away, 
     
    (cherry picked from commit 4073d491fb559e9efe56759b92dfe387f490ed5a) 
     
    Bug: 493628982 
    Change-Id: I23f1517b67fb55edd50d6e8fc8f1b4d8328e8ec5 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7701714 
    Reviewed-by: Kenichi Ishibashi <bashi@chromium.org> 
    Commit-Queue: mmenke <mmenke@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1606281} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7749087 
    Reviewed-by: mmenke <mmenke@chromium.org> 
    Reviewed-by: Giovanni Pezzino <giovax@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4826} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `net/socket/socket_test_util.cc`
- M `net/socket/socket_test_util.h`
- M `net/spdy/spdy_session.cc`
- M `net/spdy/spdy_session.h`
- M `net/spdy/spdy_session_unittest.cc`

---

Hash: [4edec3bc51165fab5053a422503648e0457bd5f1](https://chromiumdash.appspot.com/commit/4edec3bc51165fab5053a422503648e0457bd5f1)  

Date: Wed Apr 22 20:12:51 2026


---

### ch...@google.com (2026-07-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/493628982)*
