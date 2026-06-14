# Heap UAF in `network::SharedDictionaryOnDisk::SetStat`

| Field | Value |
|-------|-------|
| **Issue ID** | [488585488](https://issues.chromium.org/issues/488585488) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Network |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sh...@gmail.com |
| **Assignee** | ho...@chromium.org |
| **Created** | 2026-03-01 |
| **Bounty** | $15,000.00 |

## Description

## VULNERABILITY DETAILS

`network::SharedDictionaryOnDisk::SetState` has a heap-use-after-free in the callback fanout path (`services/network/shared_dictionary/shared_dictionary_on_disk.cc:129`).

Root cause:

- `SetState` writes `state_` at line 122.
- It iterates moved callbacks.
- Callback side effects can destroy `SharedDictionaryOnDisk`.
- The loop then continues and reads `state_` (`+0x88`) from freed memory at line 129.

Crash log:

```
=================================================================
==3970836==ERROR: AddressSanitizer: heap-use-after-free on address 0x7c86c7456bc8 at pc 0x7f67dde4d3cd bp 0x7b66b8290b50 sp 0x7b66b8290b48
READ of size 4 at 0x7c86c7456bc8 thread T5 (Chrome_ChildIOT)
    #0 0x7f67dde4d3cc in network::SharedDictionaryOnDisk::SetState(network::SharedDictionaryOnDisk::State) services/network/shared_dictionary/shared_dictionary_on_disk.cc:129:9
    #1 0x7f67dde4d835 in network::SharedDictionaryOnDisk::OnDataRead(base::Time, int) services/network/shared_dictionary/shared_dictionary_on_disk.cc:116:3
    #2 0x7f67dde536f2 in void base::internal::DecayedFunctorTraits<void (network::SharedDictionaryOnDisk::*)(base::Time, int), base::WeakPtr<network::SharedDictionaryOnDisk>&&, base::Time&&>::Invoke<void (network::SharedDictionaryOnDisk::*)(base::Time, int), base::WeakPtr<network::SharedDictionaryOnDisk> const&, base::Time, int>(void (network::SharedDictionaryOnDisk::*)(base::Time, int), base::WeakPtr<network::SharedDictionaryOnDisk> const&, base::Time&&, int&&) base/functional/bind_internal.h:740:12
    #3 0x7f67dde535e6 in void base::internal::InvokeHelper<true, base::internal::FunctorTraits<void (network::SharedDictionaryOnDisk::*&&)(base::Time, int), base::WeakPtr<network::SharedDictionaryOnDisk>&&, base::Time&&>, void, 0ul, 1ul>::MakeItSo<void (network::SharedDictionaryOnDisk::*)(base::Time, int), std::__Cr::tuple<base::WeakPtr<network::SharedDictionaryOnDisk>, base::Time>, int>(void (network::SharedDictionaryOnDisk::*&&)(base::Time, int), std::__Cr::tuple<base::WeakPtr<network::SharedDictionaryOnDisk>, base::Time>&&, int&&) base/functional/bind_internal.h:956:5
    #4 0x7f67dde53411 in void base::internal::Invoker<base::internal::FunctorTraits<void (network::SharedDictionaryOnDisk::*&&)(base::Time, int), base::WeakPtr<network::SharedDictionaryOnDisk>&&, base::Time&&>, base::internal::BindState<true, true, false, void (network::SharedDictionaryOnDisk::*)(base::Time, int), base::WeakPtr<network::SharedDictionaryOnDisk>, base::Time>, void (int)>::RunImpl<void (network::SharedDictionaryOnDisk::*)(base::Time, int), std::__Cr::tuple<base::WeakPtr<network::SharedDictionaryOnDisk>, base::Time>, 0ul, 1ul>(void (network::SharedDictionaryOnDisk::*&&)(base::Time, int), std::__Cr::tuple<base::WeakPtr<network::SharedDictionaryOnDisk>, base::Time>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>, int&&) base/functional/bind_internal.h:1069:14
    #5 0x7f67dde53223 in base::internal::Invoker<base::internal::FunctorTraits<void (network::SharedDictionaryOnDisk::*&&)(base::Time, int), base::WeakPtr<network::SharedDictionaryOnDisk>&&, base::Time&&>, base::internal::BindState<true, true, false, void (network::SharedDictionaryOnDisk::*)(base::Time, int), base::WeakPtr<network::SharedDictionaryOnDisk>, base::Time>, void (int)>::RunOnce(base::internal::BindStateBase*, int) base/functional/bind_internal.h:982:12
    #6 0x7f67dd7b2a68 in base::OnceCallback<void (int)>::Run(int) && base/functional/callback.h:155:12
    #7 0x7f67dddc89d7 in base::internal::OnceCallbackHolder<int>::Run(int) base/functional/callback_helpers.h:48:26
    #8 0x7f67dddc96d8 in void base::internal::DecayedFunctorTraits<void (base::internal::OnceCallbackHolder<int>::*)(int), std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<int>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<int>>> const&>::Invoke<void (base::internal::OnceCallbackHolder<int>::*)(int), std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<int>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<int>>> const&, int>(void (base::internal::OnceCallbackHolder<int>::*)(int), std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<int>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<int>>> const&, int&&) base/functional/bind_internal.h:740:12
    #9 0x7f67dddc95cf in void base::internal::InvokeHelper<false, base::internal::FunctorTraits<void (base::internal::OnceCallbackHolder<int>::* const&)(int), std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<int>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<int>>> const&>, void, 0ul>::MakeItSo<void (base::internal::OnceCallbackHolder<int>::* const&)(int), std::__Cr::tuple<std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<int>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<int>>>> const&, int>(void (base::internal::OnceCallbackHolder<int>::* const&)(int), std::__Cr::tuple<std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<int>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<int>>>> const&, int&&) base/functional/bind_internal.h:932:12
    #10 0x7f67dddc942c in void base::internal::Invoker<base::internal::FunctorTraits<void (base::internal::OnceCallbackHolder<int>::* const&)(int), std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<int>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<int>>> const&>, base::internal::BindState<true, true, false, void (base::internal::OnceCallbackHolder<int>::*)(int), std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<int>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<int>>>>, void (int)>::RunImpl<void (base::internal::OnceCallbackHolder<int>::* const&)(int), std::__Cr::tuple<std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<int>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<int>>>> const&, 0ul>(void (base::internal::OnceCallbackHolder<int>::* const&)(int), std::__Cr::tuple<std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<int>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<int>>>> const&, std::__Cr::integer_sequence<unsigned long, 0ul>, int&&) base/functional/bind_internal.h:1069:14
    #11 0x7f67dddc9233 in base::internal::Invoker<base::internal::FunctorTraits<void (base::internal::OnceCallbackHolder<int>::* const&)(int), std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<int>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<int>>> const&>, base::internal::BindState<true, true, false, void (base::internal::OnceCallbackHolder<int>::*)(int), std::__Cr::unique_ptr<base::internal::OnceCallbackHolder<int>, std::__Cr::default_delete<base::internal::OnceCallbackHolder<int>>>>, void (int)>::Run(base::internal::BindStateBase*, int) base/functional/bind_internal.h:989:12
    #12 0x7f6821921b38 in base::OnceCallback<void (int)>::Run(int) && base/functional/callback.h:155:12
    #13 0x7f6821f991ab in void base::internal::DecayedFunctorTraits<base::OnceCallback<void (int)>, int&&>::Invoke<base::OnceCallback<void (int)>, int>(base::OnceCallback<void (int)>&&, int&&) base/functional/bind_internal.h:815:49
    #14 0x7f6821f99029 in void base::internal::InvokeHelper<false, base::internal::FunctorTraits<base::OnceCallback<void (int)>&&, int&&>, void, 0ul>::MakeItSo<base::OnceCallback<void (int)>, std::__Cr::tuple<int>>(base::OnceCallback<void (int)>&&, std::__Cr::tuple<int>&&) base/functional/bind_internal.h:932:12
    #15 0x7f6821f98ed1 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (int)>&&, int&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (int)>, int>, void ()>::RunImpl<base::OnceCallback<void (int)>, std::__Cr::tuple<int>, 0ul>(base::OnceCallback<void (int)>&&, std::__Cr::tuple<int>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/bind_internal.h:1069:14
    #16 0x7f6821f98d78 in base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (int)>&&, int&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (int)>, int>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:982:12
    #17 0x7f6831774112 in base::OnceCallback<void ()>::Run() && base/functional/callback.h:155:12
    #18 0x7f6831ca012e in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:229:34
    #19 0x7f6831dd0557 in void base::TaskAnnotator::RunTask<base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_4>(perfetto::StaticString, base::PendingTask&, base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_4&&) base/task/common/task_annotator.h:112:5
    #20 0x7f6831dcf54e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:23
    #21 0x7f6831dce2ca in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #22 0x7f6831dcfa22 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #23 0x7f683220523c in base::MessagePumpEpoll::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_epoll.cc:224:55
    #24 0x7f6831dd16c2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #25 0x7f6831b280e7 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #26 0x7f6831f4c591 in base::Thread::Run(base::RunLoop*) base/threading/thread.cc:361:13
    #27 0x7f680ce2ca12 in content::(anonymous namespace)::ChildIOThread::Run(base::RunLoop*) content/child/child_process.cc:69:19
    #28 0x7f6831f4d241 in base::Thread::ThreadMain() base/threading/thread.cc:436:3
    #29 0x7f683204d06c in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #30 0x55f744948896 in asan_thread_start(void*) asan_interceptors.cpp

0x7c86c7456bc8 is located 136 bytes inside of 280-byte region [0x7c86c7456b40,0x7c86c7456c58)
freed by thread T5 (Chrome_ChildIOT) here:
    #0 0x55f74498e7c2 in operator delete(void*, unsigned long) (/mnt/lvm_data/chromium/src/out/asan_dbg_symbols/chrome+0xf3a07c2) (BuildId: 3afd3fb7d064a1b6)
    #1 0x7f67dde4c8f6 in network::SharedDictionaryOnDisk::~SharedDictionaryOnDisk() services/network/shared_dictionary/shared_dictionary_on_disk.cc:46:49
    #2 0x7f6822a474a2 in void base::RefCounted<net::SharedDictionary, base::DefaultRefCountedTraits<net::SharedDictionary>>::DeleteInternal<net::SharedDictionary>(net::SharedDictionary const*) base/memory/ref_counted.h:375:5
    #3 0x7f6822a47434 in base::DefaultRefCountedTraits<net::SharedDictionary>::Destruct(net::SharedDictionary const*) base/memory/ref_counted.h:341:5
    #4 0x7f6822a4740b in base::RefCounted<net::SharedDictionary, base::DefaultRefCountedTraits<net::SharedDictionary>>::Release() const base/memory/ref_counted.h:364:7
    #5 0x7f6822a473bd in scoped_refptr<net::SharedDictionary>::Release(net::SharedDictionary*) base/memory/scoped_refptr.h:392:8
    #6 0x7f6822a408d1 in scoped_refptr<net::SharedDictionary>::~scoped_refptr() base/memory/scoped_refptr.h:280:7
    #7 0x7f6822a392c9 in net::SharedDictionaryNetworkTransaction::~SharedDictionaryNetworkTransaction() net/shared_dictionary/shared_dictionary_network_transaction.cc:106:73
    #8 0x7f6822a392f8 in net::SharedDictionaryNetworkTransaction::~SharedDictionaryNetworkTransaction() net/shared_dictionary/shared_dictionary_network_transaction.cc:106:73
    #9 0x7f6822223176 in std::__Cr::default_delete<net::HttpTransaction>::operator()(net::HttpTransaction*) const gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #10 0x7f6822216555 in std::__Cr::unique_ptr<net::HttpTransaction, std::__Cr::default_delete<net::HttpTransaction>>::reset(net::HttpTransaction*) gen/third_party/libc++/src/include/__memory/unique_ptr.h:288:7
    #11 0x7f68222149f8 in std::__Cr::unique_ptr<net::HttpTransaction, std::__Cr::default_delete<net::HttpTransaction>>::~unique_ptr() gen/third_party/libc++/src/include/__memory/unique_ptr.h:254:71
    #12 0x7f68221bfee1 in net::HttpCache::Transaction::~Transaction() net/http/http_cache_transaction.cc:164:1
    #13 0x7f68221c4488 in net::HttpCache::Transaction::~Transaction() net/http/http_cache_transaction.cc:145:40
    #14 0x7f6822223176 in std::__Cr::default_delete<net::HttpTransaction>::operator()(net::HttpTransaction*) const gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #15 0x7f6822216555 in std::__Cr::unique_ptr<net::HttpTransaction, std::__Cr::default_delete<net::HttpTransaction>>::reset(net::HttpTransaction*) gen/third_party/libc++/src/include/__memory/unique_ptr.h:288:7
    #16 0x7f68222149f8 in std::__Cr::unique_ptr<net::HttpTransaction, std::__Cr::default_delete<net::HttpTransaction>>::~unique_ptr() gen/third_party/libc++/src/include/__memory/unique_ptr.h:254:71
    #17 0x7f6822e12a5b in net::URLRequestHttpJob::~URLRequestHttpJob() net/url_request/url_request_http_job.cc:437:1
    #18 0x7f6822e12e18 in net::URLRequestHttpJob::~URLRequestHttpJob() net/url_request/url_request_http_job.cc:433:41
    #19 0x7f6822de0686 in std::__Cr::default_delete<net::URLRequestJob>::operator()(net::URLRequestJob*) const gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #20 0x7f6822dddbf5 in std::__Cr::unique_ptr<net::URLRequestJob, std::__Cr::default_delete<net::URLRequestJob>>::reset(net::URLRequestJob*) gen/third_party/libc++/src/include/__memory/unique_ptr.h:288:7
    #21 0x7f6822dbf58b in net::URLRequest::~URLRequest() net/url_request/url_request.cc:220:8
    #22 0x7f6822dbfc08 in net::URLRequest::~URLRequest() net/url_request/url_request.cc:207:27
    #23 0x7f67ddfacb86 in std::__Cr::default_delete<net::URLRequest>::operator()(net::URLRequest*) const gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #24 0x7f67ddfacaa5 in std::__Cr::unique_ptr<net::URLRequest, std::__Cr::default_delete<net::URLRequest>>::reset(net::URLRequest*) gen/third_party/libc++/src/include/__memory/unique_ptr.h:288:7
    #25 0x7f67ddf9f1c8 in std::__Cr::unique_ptr<net::URLRequest, std::__Cr::default_delete<net::URLRequest>>::~unique_ptr() gen/third_party/libc++/src/include/__memory/unique_ptr.h:254:71
    #26 0x7f67ddf7ab6e in network::URLLoader::~URLLoader() services/network/url_loader.cc:778:1
    #27 0x7f67ddf7b028 in network::URLLoader::~URLLoader() services/network/url_loader.cc:764:25
    #28 0x7f67dd898f26 in std::__Cr::default_delete<network::URLLoader>::operator()(network::URLLoader*) const gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #29 0x7f67dd898eb5 in std::__Cr::unique_ptr<network::URLLoader, std::__Cr::default_delete<network::URLLoader>>::reset(network::URLLoader*) gen/third_party/libc++/src/include/__memory/unique_ptr.h:288:7

previously allocated by thread T5 (Chrome_ChildIOT) here:
    #0 0x55f74498dbbd in operator new(unsigned long) (/mnt/lvm_data/chromium/src/out/asan_dbg_symbols/chrome+0xf39fbbd) (BuildId: 3afd3fb7d064a1b6)
    #1 0x7f67dde78118 in scoped_refptr<network::SharedDictionaryOnDisk> base::MakeRefCounted<network::SharedDictionaryOnDisk, unsigned long, std::__Cr::array<unsigned char, 32ul> const&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, base::UnguessableToken const&, network::SharedDictionaryDiskCache&, base::OnceCallback<void ()>, base::ScopedClosureRunner>(unsigned long&&, std::__Cr::array<unsigned char, 32ul> const&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, base::UnguessableToken const&, network::SharedDictionaryDiskCache&, base::OnceCallback<void ()>&&, base::ScopedClosureRunner&&) base/memory/scoped_refptr.h:151:12
    #2 0x7f67dde71569 in network::SharedDictionaryStorageOnDisk::GetDictionarySyncInternal(GURL const&, network::mojom::RequestDestination) services/network/shared_dictionary/shared_dictionary_storage_on_disk.cc:246:28
    #3 0x7f67dde70597 in network::SharedDictionaryStorageOnDisk::GetDictionarySync(GURL const&, network::mojom::RequestDestination) services/network/shared_dictionary/shared_dictionary_storage_on_disk.cc:132:7
    #4 0x7f67dde720c1 in network::SharedDictionaryStorageOnDisk::GetDictionary(GURL const&, network::mojom::RequestDestination, base::OnceCallback<void (scoped_refptr<net::SharedDictionary>)>) services/network/shared_dictionary/shared_dictionary_storage_on_disk.cc:270:29
    #5 0x7f67dd8457e7 in network::cors::CorsURLLoader::CorsURLLoader(mojo::PendingReceiver<network::mojom::URLLoader>, network::OriginatingProcessId, int, unsigned int, base::OnceCallback<void (network::cors::CorsURLLoader*)>, network::ResourceRequest, bool, bool, mojo::PendingRemote<network::mojom::URLLoaderClient>, net::MutableNetworkTrafficAnnotationTag const&, network::mojom::URLLoaderFactory*, network::URLLoaderFactory*, network::cors::OriginAccessList const*, net::IsolationInfo const&, mojo::PendingRemote<network::mojom::DevToolsObserver>, network::mojom::ClientSecurityState const*, mojo::Remote<network::mojom::URLLoaderNetworkServiceObserver>*, network::CrossOriginEmbedderPolicy const&, scoped_refptr<network::SharedDictionaryStorage>, base::raw_ptr<network::mojom::SharedDictionaryAccessObserver, (partition_alloc::internal::RawPtrTraits)0>, network::NetworkContext*, base::EnumSet<net::CookieSettingOverride, (net::CookieSettingOverride)0, (net::CookieSettingOverride)10>, base::EnumSet<net::CookieSettingOverride, (net::CookieSettingOverride)0, (net::CookieSettingOverride)10>) services/network/cors/cors_url_loader.cc:363:33
    #6 0x7f67dd89102a in std::__Cr::unique_ptr<network::cors::CorsURLLoader, std::__Cr::default_delete<network::cors::CorsURLLoader>> std::__Cr::make_unique<network::cors::CorsURLLoader, mojo::PendingReceiver<network::mojom::URLLoader>, network::OriginatingProcessId const&, int&, unsigned int&, base::OnceCallback<void (network::cors::CorsURLLoader*)>, network::ResourceRequest, bool const&, bool, mojo::PendingRemote<network::mojom::URLLoaderClient>, net::MutableNetworkTrafficAnnotationTag const&, network::mojom::URLLoaderFactory* const&, network::URLLoaderFactory*, base::raw_ptr<network::cors::OriginAccessList const, (partition_alloc::internal::RawPtrTraits)0> const&, net::IsolationInfo const&, mojo::PendingRemote<network::mojom::DevToolsObserver>, network::mojom::ClientSecurityState*, mojo::Remote<network::mojom::URLLoaderNetworkServiceObserver>*, network::CrossOriginEmbedderPolicy const&, scoped_refptr<network::SharedDictionaryStorage>&, network::mojom::SharedDictionaryAccessObserverProxy*, base::raw_ptr<network::NetworkContext, (partition_alloc::internal::RawPtrTraits)0> const&, base::EnumSet<net::CookieSettingOverride, (net::CookieSettingOverride)0, (net::CookieSettingOverride)10> const&, base::EnumSet<net::CookieSettingOverride, (net::CookieSettingOverride)0, (net::CookieSettingOverride)10> const&, 0>(mojo::PendingReceiver<network::mojom::URLLoader>&&, network::OriginatingProcessId const&, int&, unsigned int&, base::OnceCallback<void (network::cors::CorsURLLoader*)>&&, network::ResourceRequest&&, bool const&, bool&&, mojo::PendingRemote<network::mojom::URLLoaderClient>&&, net::MutableNetworkTrafficAnnotationTag const&, network::mojom::URLLoaderFactory* const&, network::URLLoaderFactory*&&, base::raw_ptr<network::cors::OriginAccessList const, (partition_alloc::internal::RawPtrTraits)0> const&, net::IsolationInfo const&, mojo::PendingRemote<network::mojom::DevToolsObserver>&&, network::mojom::ClientSecurityState*&&, mojo::Remote<network::mojom::URLLoaderNetworkServiceObserver>*&&, network::CrossOriginEmbedderPolicy const&, scoped_refptr<network::SharedDictionaryStorage>&, network::mojom::SharedDictionaryAccessObserverProxy*&&, base::raw_ptr<network::NetworkContext, (partition_alloc::internal::RawPtrTraits)0> const&, base::EnumSet<net::CookieSettingOverride, (net::CookieSettingOverride)0, (net::CookieSettingOverride)10> const&, base::EnumSet<net::CookieSettingOverride, (net::CookieSettingOverride)0, (net::CookieSettingOverride)10> const&) gen/third_party/libc++/src/include/__memory/unique_ptr.h:756:30
    #7 0x7f67dd886f98 in network::cors::CorsURLLoaderFactory::CreateLoaderAndStart(mojo::PendingReceiver<network::mojom::URLLoader>, int, unsigned int, network::ResourceRequest&, mojo::PendingRemote<network::mojom::URLLoaderClient>, net::MutableNetworkTrafficAnnotationTag const&) services/network/cors/cors_url_loader_factory.cc:474:45
    #8 0x7f67ddc7bd52 in network::PrefetchMatchingURLLoaderFactory::CreateLoaderAndStart(mojo::PendingReceiver<network::mojom::URLLoader>, int, unsigned int, network::ResourceRequest&, mojo::PendingRemote<network::mojom::URLLoaderClient>, net::MutableNetworkTrafficAnnotationTag const&) services/network/prefetch_matching_url_loader_factory.cc:105:10
    #9 0x7f67dea79cba in network::mojom::URLLoaderFactoryStubDispatch::Accept(network::mojom::URLLoaderFactory*, mojo::Message*) gen/services/network/public/mojom/url_loader_factory.mojom.cc:352:13
    #10 0x7f67dd895406 in network::mojom::URLLoaderFactoryStub<mojo::RawPtrImplRefTraits<network::mojom::URLLoaderFactory>>::Accept(mojo::Message*) gen/services/network/public/mojom/url_loader_factory.mojom.h:139:12
    #11 0x7f6833219b5e in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085:54
    #12 0x7f6833218941 in mojo::InterfaceEndpointClient::HandleIncomingMessageThunk::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:383:18
    #13 0x7f6833257183 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:51:24
    #14 0x7f683321f900 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #15 0x7f6833260de2 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1204:42
    #16 0x7f683325fb26 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:790:7
    #17 0x7f6833257038 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:44:19
    #18 0x7f68331d6463 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) mojo/public/cpp/bindings/lib/connector.cc:568:49
    #19 0x7f68331d803a in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:629:14
    #20 0x7f68331d79d2 in mojo::Connector::OnHandleReadyInternal(unsigned int) mojo/public/cpp/bindings/lib/connector.cc:454:3
    #21 0x7f68331d7845 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int) mojo/public/cpp/bindings/lib/connector.cc:420:3
    #22 0x7f68331e4a65 in void base::internal::DecayedFunctorTraits<void (mojo::Connector::*)(char const*, unsigned int), mojo::Connector*, char const* const&>::Invoke<void (mojo::Connector::*)(char const*, unsigned int), mojo::Connector*, char const*, unsigned int>(void (mojo::Connector::*)(char const*, unsigned int), mojo::Connector*&&, char const*&&, unsigned int&&) base/functional/bind_internal.h:740:12
    #23 0x7f68331e473e in void base::internal::InvokeHelper<false, base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, void, 0ul, 1ul>::MakeItSo<void (mojo::Connector::* const&)(char const*, unsigned int), std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>> const&, unsigned int>(void (mojo::Connector::* const&)(char const*, unsigned int), std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>> const&, unsigned int&&) base/functional/bind_internal.h:932:12
    #24 0x7f68331e4461 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::RunImpl<void (mojo::Connector::* const&)(char const*, unsigned int), std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>> const&, 0ul, 1ul>(void (mojo::Connector::* const&)(char const*, unsigned int), std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>> const&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>, unsigned int&&) base/functional/bind_internal.h:1069:14
    #25 0x7f68331e4243 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int) base/functional/bind_internal.h:989:12
    #26 0x7f68331e2e38 in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & base/functional/callback.h:346:12
    #27 0x7f68331e1fee in mojo::SimpleWatcher::DiscardReadyState(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.h:192:14
    #28 0x7f68331e26d1 in void base::internal::DecayedFunctorTraits<void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>::Invoke<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&>(void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&, unsigned int&&, mojo::HandleSignalsState const&) base/functional/bind_internal.h:673:12
    #29 0x7f68331e2609 in void base::internal::InvokeHelper<false, base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, void, 0ul>::MakeItSo<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)>> const&, unsigned int, mojo::HandleSignalsState const&>(void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)>> const&, unsigned int&&, mojo::HandleSignalsState const&) base/functional/bind_internal.h:932:12

Thread T5 (Chrome_ChildIOT) created by T0 (chrome) here:
    #0 0x55f74492e6c1 in pthread_create (/mnt/lvm_data/chromium/src/out/asan_dbg_symbols/chrome+0xf3406c1) (BuildId: 3afd3fb7d064a1b6)
    #1 0x7f683204bb69 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) base/threading/platform_thread_posix.cc:153:13
    #2 0x7f683204b6c8 in base::PlatformThreadBase::CreateWithType(unsigned long, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) base/threading/platform_thread_posix.cc:322:10
    #3 0x7f6831f49866 in base::Thread::StartWithOptions(base::Thread::Options) base/threading/thread.cc:228:26
    #4 0x7f680ce2a705 in content::ChildProcess::ChildProcess(base::ThreadType, std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>, bool) content/child/child_process.cc:152:21
    #5 0x7f681a3b9149 in content::UtilityMain(content::MainFunctionParams) content/utility/utility_main.cc:459:16
    #6 0x7f681a6e40ad in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:762:14
    #7 0x7f681a6e7956 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1152:10
    #8 0x7f681a6dd7af in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:358:36
    #9 0x7f681a6de625 in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:371:10
    #10 0x55f74498f700 in ChromeMain chrome/app/chrome_main.cc:191:12
    #11 0x55f74498ef61 in main chrome/app/chrome_exe_main_aura.cc:17:10
    #12 0x7f66f0b0ad8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

SUMMARY: AddressSanitizer: heap-use-after-free services/network/shared_dictionary/shared_dictionary_on_disk.cc:129:9 in network::SharedDictionaryOnDisk::SetState(network::SharedDictionaryOnDisk::State)
Shadow bytes around the buggy address:
  0x7c86c7456900: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7c86c7456980: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x7c86c7456a00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7c86c7456a80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa
  0x7c86c7456b00: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
=>0x7c86c7456b80: fd fd fd fd fd fd fd fd fd[fd]fd fd fd fd fd fd
  0x7c86c7456c00: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x7c86c7456c80: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x7c86c7456d00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7c86c7456d80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa
  0x7c86c7456e00: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
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

==3970836==ADDITIONAL INFO

==3970836==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7f6821f7259c in disk_cache::SimpleEntryImpl::EntryOperationComplete(base::OnceCallback<void (int)>, disk_cache::SimpleEntryStat const&, int) net/disk_cache/simple/simple_entry_impl.cc:1558:9
    #1 0x7f6821f5f111 in disk_cache::SimpleEntryImpl::ReadDataInternal(bool, int, long, net::IOBuffer*, int, base::OnceCallback<void (int)>) net/disk_cache/simple/simple_entry_impl.cc:1121:46
    #2 0x7f6821f5f111 in disk_cache::SimpleEntryImpl::ReadDataInternal(bool, int, long, net::IOBuffer*, int, base::OnceCallback<void (int)>) net/disk_cache/simple/simple_entry_impl.cc:1121:46
    #3 0x7f6821f6325d in disk_cache::SimpleEntryImpl::ReturnEntryToCallerAsync(bool, base::OnceCallback<void (disk_cache::EntryResult)>) net/disk_cache/simple/simple_entry_impl.cc:723:7


Command line: `/proc/self/exe --type=utility --utility-sub-type=network.mojom.NetworkService --lang=en-US --service-sandbox-type=network --no-sandbox --disable-dev-shm-usage --use-angle=swiftshader-webgl --crashpad-handler-pid=3792972 --enable-crash-reporter=, --noerrdialogs --user-data-dir=/tmp/chromium-cdp-profile-z9wety95 --change-stack-guard-on-fork=enable --shared-files=network_parent_dirs_pipe:100,v8_context_snapshot_data:101 --field-trial-handle=3,i,8259431885288563424,5192296079784302641,262144 --enable-features=CompressionDictionaryTTL,CompressionDictionaryTransport --disable-features=PaintHolding,RendererSideContentDecoding --variations-seed-version --pseudonymization-salt-handle=7,i,13871194498671416106,3267072129068102504,4 --trace-process-track-uuid=3950869623167788687 --enable-logging=stderr`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==3970836==END OF ADDITIONAL INFO

```
## VERSION

Chrome Version: `146.0.7680.31` + `stable` (Chrome for Testing, Linux64), and `147.0.7703.0` + `dev` (Chrome for Testing, Linux64 preview)
Operating System: Ubuntu 22.04.3 LTS, kernel 5.15.0-151-generic, x86\_64

## REPRODUCTION CASE

Attached local repro files:

- `shared-dictionary-set-state-20260228_033304.html`
- `shared_dictionary_set_state_server.py`
- `compressed.data`
- `test.dict`

Local reproduction steps:

1. Start server:
   `python3 shared_dictionary_set_state_server.py --host 127.0.0.1 --port 8000`. You can run inside Docker.
2. Launch Chrome and open:
   `http://127.0.0.1:8000/shared-dictionary-set-state-20260228_033304.html`

You need to have an ASAN build to trigger the crash.

What it Does:

1. The page repeatedly registers compression dictionaries via /dict.
2. The server answers /dict with Use-As-Dictionary headers and varied dictionary bytes so Chrome stores/updates many dictionary entries.
3. The page then issues many concurrent /target/data fetches with mixed parameters:
   - enc alternates between dcb, dcz, flip.
   - body is often mutated (mut), chunked (chunked=1), and sometimes truncated (trunc=1).
   - Content-Encoding and Content-Length are sometimes intentionally odd/mismatched (hdr modes).
   - requests are frequently aborted after 1–5 ms (AbortController) to force cancellation races.
4. Responses are consumed in different read modes (text, arrayBuffer, blob, stream) to exercise multiple decode/read paths.
5. This combination creates high churn in Shared Dictionary load/read state transitions and repeatedly hits the UAF in:
   - network::SharedDictionaryOnDisk::SetState(...)
   - services/network/shared\_dictionary/shared\_dictionary\_on\_disk.cc:129

Type of crash: utility process memory-safety crash (`network.mojom.NetworkService`, heap-use-after-free).

Crash State: symbolized ASAN top frame `network::SharedDictionaryOnDisk::SetState` at `services/network/shared_dictionary/shared_dictionary_on_disk.cc:129`; free path includes `network::SharedDictionaryOnDisk::~SharedDictionaryOnDisk`.
Client ID (if relevant): N/A

## CREDIT INFORMATION

Reporter credit: heapracer (@heapracer)

## Attachments

- [test.dict](attachments/test.dict) (application/octet-stream, 27 B)
- [compressed.data](attachments/compressed.data) (application/octet-stream, 75 B)
- [shared_dictionary_set_state_server.py](attachments/shared_dictionary_set_state_server.py) (text/x-python, 17.5 KB)
- [shared-dictionary-set-state-20260228_033304.html](attachments/shared-dictionary-set-state-20260228_033304.html) (text/html, 5.5 KB)

## Timeline

### me...@google.com (2026-03-05)

Thanks for the report. I can repro on M145 stable.

### ch...@google.com (2026-03-05)

Setting milestone because of s0/s1 severity.

### dx...@google.com (2026-03-05)

Project: chromium/src  

Branch:  main  

Author:  Tsuyoshi Horo [horo@chromium.org](mailto:horo@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7636772>

shared\_dictionary: Fix Use-After-Free in SharedDictionaryOnDisk

---


Expand for full commit details
```
     
    This CL fixes a Use-After-Free bug in SharedDictionaryOnDisk::SetState. 
    Previously, SetState() accessed the member variable state_ within a loop 
    that executes callbacks. If one of these callbacks resulted in the 
    deletion of the SharedDictionaryOnDisk object, subsequent accesses to 
    state_ would result in a Use-After-Free. 
     
    This CL resolves the issue by using the local 'state' parameter instead 
    of the 'state_' member variable. 
     
    A regression test DeleteInReadAllCallback is added to 
    shared_dictionary_on_disk_unittest.cc to ensure that deleting the 
    dictionary in a ReadAll() callback does not cause a crash. 
     
    Fixed: 488585488 
    Change-Id: I2192458c2d58825bed91f8791604ceeb20b1056b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7636772 
    Commit-Queue: Patrick Meenan <pmeenan@chromium.org> 
    Reviewed-by: Patrick Meenan <pmeenan@chromium.org> 
    Auto-Submit: Tsuyoshi Horo <horo@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1594661}

```

---

Files:

- M `services/network/shared_dictionary/shared_dictionary_on_disk.cc`
- M `services/network/shared_dictionary/shared_dictionary_on_disk_unittest.cc`

---

Hash: [d1fbfa27e826d6e6424c1f73b93a03744c2091fb](https://chromiumdash.appspot.com/commit/d1fbfa27e826d6e6424c1f73b93a03744c2091fb)  

Date: Thu Mar 5 15:09:18 2026


---

### ch...@google.com (2026-03-06)

Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1594661) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1594661) appears to be after beta branch point (1582197).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ho...@google.com (2026-03-06)

1. Which CLs should be backmerged? (Please include Gerrit links.)
   <https://chromium-review.googlesource.com/7636772>
2. Has this fix been verified on Canary to not pose any stability regressions?
   Yes
3. Does this fix pose any potential non-verifiable stability risks?
   No
4. Does this fix pose any known compatibility risks?
   No
5. Does it require manual verification by the test team? If so, please describe required testing.
   No
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2026-03-06)

Merge review required: M146 has already been cut for stable release.

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
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-06)

Merge review required: M145 is already shipping to stable.

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
Owners: andywu (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### dr...@chromium.org (2026-03-07)

No crashes in Canary. Approved to merge to M146. We don't plan another release of M145, so no merge needed there.

### dx...@google.com (2026-03-09)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Tsuyoshi Horo [horo@chromium.org](mailto:horo@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7639032>

[M146] shared\_dictionary: Fix Use-After-Free in SharedDictionaryOnDisk

---


Expand for full commit details
```
     
    This CL fixes a Use-After-Free bug in SharedDictionaryOnDisk::SetState. 
    Previously, SetState() accessed the member variable state_ within a loop 
    that executes callbacks. If one of these callbacks resulted in the 
    deletion of the SharedDictionaryOnDisk object, subsequent accesses to 
    state_ would result in a Use-After-Free. 
     
    This CL resolves the issue by using the local 'state' parameter instead 
    of the 'state_' member variable. 
     
    A regression test DeleteInReadAllCallback is added to 
    shared_dictionary_on_disk_unittest.cc to ensure that deleting the 
    dictionary in a ReadAll() callback does not cause a crash. 
     
    (cherry picked from commit d1fbfa27e826d6e6424c1f73b93a03744c2091fb) 
     
    Fixed: 488585488 
    Change-Id: I2192458c2d58825bed91f8791604ceeb20b1056b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7636772 
    Commit-Queue: Patrick Meenan <pmeenan@chromium.org> 
    Reviewed-by: Patrick Meenan <pmeenan@chromium.org> 
    Auto-Submit: Tsuyoshi Horo <horo@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1594661} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7639032 
    Commit-Queue: Tsuyoshi Horo <horo@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7680@{#2175} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `services/network/shared_dictionary/shared_dictionary_on_disk.cc`
- M `services/network/shared_dictionary/shared_dictionary_on_disk_unittest.cc`

---

Hash: [507efc2613e4ceb93dda370a7a6b0db16ad65e47](https://chromiumdash.appspot.com/commit/507efc2613e4ceb93dda370a7a6b0db16ad65e47)  

Date: Mon Mar 9 02:13:33 2026


---

### pe...@google.com (2026-03-09)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2026-03-11)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-03-11)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7652135
2. Low - There was no conflict.
3. 146
4. Yes, the issue was introduced by the initial CL[1][2], and M138 contains the CLs. 

[1] https://chromium-review.git.corp.google.com/c/chromium/src/+/4512012
[2] https://chromium-review.git.corp.google.com/c/chromium/src/+/4583492

### an...@google.com (2026-03-16)

re:[#comment13](https://issues.chromium.org/issues/488585488#comment13) Delayed until M146 soaked in Stable.

### an...@google.com (2026-04-01)

Merge approved for LTS-138

### dx...@google.com (2026-04-02)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Tsuyoshi Horo [horo@chromium.org](mailto:horo@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7652135>

[M138-LTS] shared\_dictionary: Fix Use-After-Free in SharedDictionaryOnDisk

---


Expand for full commit details
```
     
    This CL fixes a Use-After-Free bug in SharedDictionaryOnDisk::SetState. 
    Previously, SetState() accessed the member variable state_ within a loop 
    that executes callbacks. If one of these callbacks resulted in the 
    deletion of the SharedDictionaryOnDisk object, subsequent accesses to 
    state_ would result in a Use-After-Free. 
     
    This CL resolves the issue by using the local 'state' parameter instead 
    of the 'state_' member variable. 
     
    A regression test DeleteInReadAllCallback is added to 
    shared_dictionary_on_disk_unittest.cc to ensure that deleting the 
    dictionary in a ReadAll() callback does not cause a crash. 
     
    (cherry picked from commit d1fbfa27e826d6e6424c1f73b93a03744c2091fb) 
     
    Fixed: 488585488 
    Change-Id: I2192458c2d58825bed91f8791604ceeb20b1056b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7636772 
    Commit-Queue: Patrick Meenan <pmeenan@chromium.org> 
    Reviewed-by: Patrick Meenan <pmeenan@chromium.org> 
    Auto-Submit: Tsuyoshi Horo <horo@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1594661} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7652135 
    Reviewed-by: Tsuyoshi Horo <horo@chromium.org> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Victor Gabriel Savu <vsavu@google.com> 
    Owners-Override: Victor Gabriel Savu <vsavu@google.com> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3515} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `services/network/shared_dictionary/shared_dictionary_on_disk.cc`
- M `services/network/shared_dictionary/shared_dictionary_on_disk_unittest.cc`

---

Hash: [6d44de4cc7459bf90827ba47d955727ae66944d3](https://chromiumdash.appspot.com/commit/6d44de4cc7459bf90827ba47d955727ae66944d3)  

Date: Thu Apr 2 13:46:40 2026


---

### sp...@google.com (2026-04-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $15000.00 for this report.

Rationale for this decision:
High quality. Memory corruption in a highly privileged process (e.g. GPU, network processes) 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2026-04-17)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-04-17)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7747531
2. Low - There was no conflict.
3. 146
4. Yes, the issue was introduced by the initial CL[1][2], and M144 contains the CLs.

[1] https://chromium-review.git.corp.google.com/c/chromium/src/+/4512012
[2] https://chromium-review.git.corp.google.com/c/chromium/src/+/4583492

### dx...@google.com (2026-04-30)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Tsuyoshi Horo [horo@chromium.org](mailto:horo@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7747531>

[M144-LTS] shared\_dictionary: Fix Use-After-Free in SharedDictionaryOnDisk

---


Expand for full commit details
```
     
    This CL fixes a Use-After-Free bug in SharedDictionaryOnDisk::SetState. 
    Previously, SetState() accessed the member variable state_ within a loop 
    that executes callbacks. If one of these callbacks resulted in the 
    deletion of the SharedDictionaryOnDisk object, subsequent accesses to 
    state_ would result in a Use-After-Free. 
     
    This CL resolves the issue by using the local 'state' parameter instead 
    of the 'state_' member variable. 
     
    A regression test DeleteInReadAllCallback is added to 
    shared_dictionary_on_disk_unittest.cc to ensure that deleting the 
    dictionary in a ReadAll() callback does not cause a crash. 
     
    (cherry picked from commit d1fbfa27e826d6e6424c1f73b93a03744c2091fb) 
     
    Fixed: 488585488 
    Change-Id: I2192458c2d58825bed91f8791604ceeb20b1056b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7636772 
    Commit-Queue: Patrick Meenan <pmeenan@chromium.org> 
    Reviewed-by: Patrick Meenan <pmeenan@chromium.org> 
    Auto-Submit: Tsuyoshi Horo <horo@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1594661} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7747531 
    Owners-Override: Achuith Bhandarkar <achuith@chromium.org> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Tsuyoshi Horo <horo@chromium.org> 
    Reviewed-by: Achuith Bhandarkar <achuith@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4843} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `services/network/shared_dictionary/shared_dictionary_on_disk.cc`
- M `services/network/shared_dictionary/shared_dictionary_on_disk_unittest.cc`

---

Hash: [832ce43a5d2d14b5d01523b265ef81639718e5ca](https://chromiumdash.appspot.com/commit/832ce43a5d2d14b5d01523b265ef81639718e5ca)  

Date: Thu Apr 30 06:54:03 2026


---

### ch...@google.com (2026-06-12)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/488585488)*
