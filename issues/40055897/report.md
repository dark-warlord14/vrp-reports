# uaf in browser process DestroyURLLoader(network::cors::CorsURLLoaderFactory) 

| Field | Value |
|-------|-------|
| **Issue ID** | [40055897](https://issues.chromium.org/issues/40055897) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network, Internals>Services>Network |
| **Platforms** | Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | mm...@chromium.org |
| **Created** | 2021-05-17 |
| **Bounty** | $15,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36

Steps to reproduce the problem:

I submitted a main process issue a month ago. 
But this issue(https://bugs.chromium.org/p/chromium/issues/detail?id=1202056) was closed. I found out that the new version could still be reproduced.
CF should not be able to reproduce and requires manual testing. Can anyone confirm it?

Tested version:
Chromium 91.0.4464.5 
Chromium 92.0.4511.0

1 ./chrome -user-data-dir=/tmp/xx http://localhost:8000/crash.html
2 Allow popup window
3 And Press "ctril + C" repeatedly to force close the browser.
4.the asan log looks similar to https://bugs.chromium.org/p/chromium/issues/detail?id=1174943

What is the expected behavior?

What went wrong?
=================================================================
==1787713==ERROR: AddressSanitizer: heap-use-after-free on address 0x60400006ea58 at pc 0x5624518d363c bp 0x7f74862c06d0 sp 0x7f74862c06c8
READ of size 8 at 0x60400006ea58 thread T3 (Chrome_ChildIOT)
==1787713==WARNING: invalid path to external symbolizer!
==1787713==WARNING: Failed to use and restart external symbolizer!
error: unknown argument '--demangle=True'
    #0 0x5624518d363b in std::__1::__tree<std::__1::unique_ptr<network::mojom::URLLoader, std::__1::default_delete<network::mojom::URLLoader> >, base::UniquePtrComparator, std::__1::allocator<std::__1::unique_ptr<network::mojom::URLLoader, std::__1::default_delete<network::mojom::URLLoader> > > >::destroy(std::__1::__tree_node<std::__1::unique_ptr<network::mojom::URLLoader, std::__1::default_delete<network::mojom::URLLoader> >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/__tree:1799
    #1 0x5624518d363b in ?? ??:0
    #2 0x5624518cec08 in network::cors::CorsURLLoaderFactory::~CorsURLLoaderFactory() ./../../buildtools/third_party/libc++/trunk/include/__tree:1789
    #3 0x5624518cec08 in ~set ./../../buildtools/third_party/libc++/trunk/include/set:605
    #4 0x5624518cec08 in ~CorsURLLoaderFactory ./../../services/network/cors/cors_url_loader_factory.cc:212
    #5 0x5624518cec08 in ?? ??:0
    #6 0x56245180bd24 in std::__1::__tree<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> >, base::UniquePtrComparator, std::__1::allocator<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> > > >::destroy(std::__1::__tree_node<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/memory:1335
    #7 0x56245180bd24 in reset ./../../buildtools/third_party/libc++/trunk/include/memory:1596
    #8 0x56245180bd24 in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/memory:1550
    #9 0x56245180bd24 in destroy<std::unique_ptr<network::cors::CorsURLLoaderFactory>, void, void> ./../../buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:317
    #10 0x56245180bd24 in destroy ./../../buildtools/third_party/libc++/trunk/include/__tree:1801
    #11 0x56245180bd24 in ?? ??:0
    #12 0x56245180bcf9 in std::__1::__tree<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> >, base::UniquePtrComparator, std::__1::allocator<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> > > >::destroy(std::__1::__tree_node<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/__tree:1799
    #13 0x56245180bcf9 in ?? ??:0
    #14 0x56245180bcd9 in std::__1::__tree<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> >, base::UniquePtrComparator, std::__1::allocator<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> > > >::destroy(std::__1::__tree_node<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/__tree:1798
    #15 0x56245180bcd9 in ?? ??:0
    #16 0x56245180bcd9 in std::__1::__tree<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> >, base::UniquePtrComparator, std::__1::allocator<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> > > >::destroy(std::__1::__tree_node<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/__tree:1798
    #17 0x56245180bcd9 in ?? ??:0
    #18 0x56245180bcd9 in std::__1::__tree<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> >, base::UniquePtrComparator, std::__1::allocator<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> > > >::destroy(std::__1::__tree_node<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/__tree:1798
    #19 0x56245180bcd9 in ?? ??:0
    #20 0x56245180bcd9 in std::__1::__tree<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> >, base::UniquePtrComparator, std::__1::allocator<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> > > >::destroy(std::__1::__tree_node<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/__tree:1798
    #21 0x56245180bcd9 in ?? ??:0
    #22 0x5624517f27f2 in network::NetworkContext::~NetworkContext() ./../../buildtools/third_party/libc++/trunk/include/__tree:1789
    #23 0x5624517f27f2 in ~set ./../../buildtools/third_party/libc++/trunk/include/set:605
    #24 0x5624517f27f2 in ~NetworkContext ./../../services/network/network_context.cc:533
    #25 0x5624517f27f2 in ?? ??:0
    #26 0x5624517f386d in network::NetworkContext::~NetworkContext() ./../../services/network/network_context.cc:491
    #27 0x5624517f386d in ?? ??:0
    #28 0x5624517d1d6d in std::__1::__tree<std::__1::unique_ptr<network::NetworkContext, std::__1::default_delete<network::NetworkContext> >, base::UniquePtrComparator, std::__1::allocator<std::__1::unique_ptr<network::NetworkContext, std::__1::default_delete<network::NetworkContext> > > >::destroy(std::__1::__tree_node<std::__1::unique_ptr<network::NetworkContext, std::__1::default_delete<network::NetworkContext> >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/memory:1335
    #29 0x5624517d1d6d in reset ./../../buildtools/third_party/libc++/trunk/include/memory:1596
    #30 0x5624517d1d6d in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/memory:1550
    #31 0x5624517d1d6d in destroy<std::unique_ptr<network::NetworkContext>, void, void> ./../../buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:317
    #32 0x5624517d1d6d in destroy ./../../buildtools/third_party/libc++/trunk/include/__tree:1801
    #33 0x5624517d1d6d in ?? ??:0
    #34 0x5624517d1d21 in std::__1::__tree<std::__1::unique_ptr<network::NetworkContext, std::__1::default_delete<network::NetworkContext> >, base::UniquePtrComparator, std::__1::allocator<std::__1::unique_ptr<network::NetworkContext, std::__1::default_delete<network::NetworkContext> > > >::destroy(std::__1::__tree_node<std::__1::unique_ptr<network::NetworkContext, std::__1::default_delete<network::NetworkContext> >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/__tree:1799
    #35 0x5624517d1d21 in ?? ??:0
    #36 0x5624517ca0e1 in network::NetworkService::~NetworkService() ./../../buildtools/third_party/libc++/trunk/include/__tree:1838
    #37 0x5624517ca0e1 in clear ./../../buildtools/third_party/libc++/trunk/include/set:695
    #38 0x5624517ca0e1 in DestroyNetworkContexts ./../../services/network/network_service.cc:773
    #39 0x5624517ca0e1 in ~NetworkService ./../../services/network/network_service.cc:358
    #40 0x5624517ca0e1 in ?? ??:0
    #41 0x5624517ca9fd in network::NetworkService::~NetworkService() ./../../services/network/network_service.cc:351
    #42 0x5624517ca9fd in ?? ??:0
    #43 0x56244b8aa18e in mojo::ServiceFactory::InstanceHolder<network::mojom::NetworkService>::~InstanceHolder() ./../../buildtools/third_party/libc++/trunk/include/memory:1335
    #44 0x56244b8aa18e in reset ./../../buildtools/third_party/libc++/trunk/include/memory:1596
    #45 0x56244b8aa18e in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/memory:1550
    #46 0x56244b8aa18e in ~InstanceHolder ./../../mojo/public/cpp/bindings/service_factory.h:127
    #47 0x56244b8aa18e in ~InstanceHolder ./../../mojo/public/cpp/bindings/service_factory.h:127
    #48 0x56244b8aa18e in ?? ??:0
    #49 0x56244d61e682 in std::__1::vector<std::__1::unique_ptr<mojo::ServiceFactory::InstanceHolderBase, std::__1::default_delete<mojo::ServiceFactory::InstanceHolderBase> >, std::__1::allocator<std::__1::unique_ptr<mojo::ServiceFactory::InstanceHolderBase, std::__1::default_delete<mojo::ServiceFactory::InstanceHolderBase> > > >::erase(std::__1::__wrap_iter<std::__1::unique_ptr<mojo::ServiceFactory::InstanceHolderBase, std::__1::default_delete<mojo::ServiceFactory::InstanceHolderBase> > const*>, std::__1::__wrap_iter<std::__1::unique_ptr<mojo::ServiceFactory::InstanceHolderBase, std::__1::default_delete<mojo::ServiceFactory::InstanceHolderBase> > const*>) ./../../buildtools/third_party/libc++/trunk/include/memory:1335
    #50 0x56244d61e682 in reset ./../../buildtools/third_party/libc++/trunk/include/memory:1596
    #51 0x56244d61e682 in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/memory:1550
    #52 0x56244d61e682 in destroy ./../../buildtools/third_party/libc++/trunk/include/memory:829
    #53 0x56244d61e682 in destroy<std::unique_ptr<mojo::ServiceFactory::InstanceHolderBase>, void> ./../../buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:307
    #54 0x56244d61e682 in __destruct_at_end ./../../buildtools/third_party/libc++/trunk/include/vector:428
    #55 0x56244d61e682 in __destruct_at_end ./../../buildtools/third_party/libc++/trunk/include/vector:835
    #56 0x56244d61e682 in erase ./../../buildtools/third_party/libc++/trunk/include/vector:1739
    #57 0x56244d61e682 in ?? ??:0
    #58 0x56244d61c63d in base::internal::Invoker<base::internal::BindState<void (mojo::ServiceFactory::*)(mojo::ServiceFactory::InstanceHolderBase*), base::WeakPtr<mojo::ServiceFactory>, mojo::ServiceFactory::InstanceHolderBase*>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:509
    #59 0x56244d61c63d in MakeItSo<void (mojo::ServiceFactory::*)(mojo::ServiceFactory::InstanceHolderBase *), base::WeakPtr<mojo::ServiceFactory>, mojo::ServiceFactory::InstanceHolderBase *> ./../../base/bind_internal.h:668
    #60 0x56244d61c63d in RunImpl<void (mojo::ServiceFactory::*)(mojo::ServiceFactory::InstanceHolderBase *), std::tuple<base::WeakPtr<mojo::ServiceFactory>, mojo::ServiceFactory::InstanceHolderBase *>, 0, 1> ./../../base/bind_internal.h:721
    #61 0x56244d61c63d in RunOnce ./../../base/bind_internal.h:690
    #62 0x56244d61c63d in ?? ??:0
    #63 0x56244d61c901 in base::internal::Invoker<base::internal::BindState<base::internal::ThenHelper<base::OnceCallback<void ()>, base::OnceCallback<void ()> >::CreateTrampoline()::{lambda(base::OnceCallback<void ()>, base::OnceCallback<void ()>)#1}, base::OnceCallback<void ()>, base::OnceCallback<void ()> >, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/callback.h:101
    #64 0x56244d61c901 in operator() ./../../base/callback_internal.h:211
    #65 0x56244d61c901 in Invoke<(lambda at ../../base/callback_internal.h:209:12), base::OnceCallback<void ()>, base::OnceCallback<void ()> > ./../../base/bind_internal.h:390
    #66 0x56244d61c901 in MakeItSo<(lambda at ../../base/callback_internal.h:209:12), base::OnceCallback<void ()>, base::OnceCallback<void ()> > ./../../base/bind_internal.h:648
    #67 0x56244d61c901 in RunImpl<(lambda at ../../base/callback_internal.h:209:12), std::tuple<base::OnceCallback<void ()>, base::OnceCallback<void ()> >, 0, 1> ./../../base/bind_internal.h:721
    #68 0x56244d61c901 in RunOnce ./../../base/bind_internal.h:690
    #69 0x56244d61c901 in ?? ??:0
    #70 0x56244d61bce8 in mojo::ServiceFactory::InstanceHolderBase::OnPipeSignaled(unsigned int, mojo::HandleSignalsState const&) ./../../base/callback.h:101
    #71 0x56244d61bce8 in OnPipeSignaled ./../../mojo/public/cpp/bindings/service_factory.cc:80
    #72 0x56244d61bce8 in ?? ??:0
    #73 0x56244d647f9d in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../base/callback.h:169
    #74 0x56244d647f9d in OnHandleReady ./../../mojo/public/cpp/system/simple_watcher.cc:278
    #75 0x56244d647f9d in ?? ??:0
    #76 0x56244d648cb3 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) ./../../mojo/public/cpp/system/simple_watcher.cc:94
    #77 0x56244d648cb3 in ?? ??:0
    #78 0x56244d64614a in mojo::SimpleWatcher::Context::CallNotify(MojoTrapEvent const*) ./../../mojo/public/cpp/system/simple_watcher.cc:59
    #79 0x56244d64614a in ?? ??:0
    #80 0x56244300e545 in mojo::core::WatcherDispatcher::InvokeWatchCallback(unsigned long, unsigned int, mojo::core::HandleSignalsState const&, unsigned int) ./../../mojo/core/watcher_dispatcher.cc:94
    #81 0x56244300e545 in ?? ??:0
    #82 0x56244300d30a in mojo::core::Watch::InvokeCallback(unsigned int, mojo::core::HandleSignalsState const&, unsigned int) ./../../mojo/core/watch.cc:78
    #83 0x56244300d30a in ?? ??:0
    #84 0x562443001f38 in mojo::core::RequestContext::~RequestContext() ./../../mojo/core/request_context.cc:72
    #85 0x562443001f38 in ?? ??:0
    #86 0x562442fe226b in mojo::core::NodeChannel::OnChannelError(mojo::core::Channel::Error) ./../../mojo/core/node_channel.cc:847
    #87 0x562442fe226b in ?? ??:0
    #88 0x5624430228d6 in mojo::core::ChannelPosix::OnFileCanReadWithoutBlocking(int) channel_posix.cc:?
    #89 0x5624430228d6 in ?? ??:0
    #90 0x56244be02fe7 in base::MessagePumpLibevent::OnLibeventNotification(int, short, void*) ./../../base/message_loop/message_pump_libevent.cc:?
    #91 0x56244be02fe7 in ?? ??:0
    #92 0x56244c1b6fac in event_process_active ./../../base/third_party/libevent/event.c:381
    #93 0x56244c1b6fac in event_base_loop ./../../base/third_party/libevent/event.c:521
    #94 0x56244c1b6fac in ?? ??:0
    #95 0x56244be039ca in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_libevent.cc:258
    #96 0x56244be039ca in ?? ??:0
    #97 0x56244bccfdfc in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:460
    #98 0x56244bccfdfc in ?? ??:0
    #99 0x56244bc14f41 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:133
    #100 0x56244bc14f41 in ?? ??:0
    #101 0x56244bd22ec2 in base::Thread::Run(base::RunLoop*) ./../../base/threading/thread.cc:312
    #102 0x56244bd22ec2 in ?? ??:0
    #103 0x56244bd233c7 in base::Thread::ThreadMain() ./../../base/threading/thread.cc:383
    #104 0x56244bd233c7 in ?? ??:0
    #105 0x56244bdb1485 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:87
    #106 0x56244bdb1485 in ?? ??:0
error: unknown argument '--demangle=True'
    #107 0x7f748fecf608 in start_thread /build/glibc-ZN95T4/glibc-2.31/nptl/pthread_create.c:477
    #108 0x7f748fecf608 in ?? ??:0

0x60400006ea58 is located 8 bytes inside of 40-byte region [0x60400006ea50,0x60400006ea78)
freed by thread T3 (Chrome_ChildIOT) here:
    #0 0x56243e77a62d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160
    #1 0x56243e77a62d in ?? ??:0
    #2 0x5624518cf539 in network::cors::CorsURLLoaderFactory::DestroyURLLoader(network::mojom::URLLoader*) ./../../buildtools/third_party/libc++/trunk/include/new:245
    #3 0x5624518cf539 in __do_deallocate_handle_size<> ./../../buildtools/third_party/libc++/trunk/include/new:269
    #4 0x5624518cf539 in __libcpp_deallocate ./../../buildtools/third_party/libc++/trunk/include/new:279
    #5 0x5624518cf539 in deallocate ./../../buildtools/third_party/libc++/trunk/include/memory:787
    #6 0x5624518cf539 in deallocate ./../../buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:280
    #7 0x5624518cf539 in erase ./../../buildtools/third_party/libc++/trunk/include/__tree:2424
    #8 0x5624518cf539 in erase ./../../buildtools/third_party/libc++/trunk/include/set:687
    #9 0x5624518cf539 in DestroyURLLoader ./../../services/network/cors/cors_url_loader_factory.cc:226
    #10 0x5624518cf539 in ?? ??:0
    #11 0x562451995151 in network::URLLoader::NotifyCompleted(int) ./../../base/callback.h:101
    #12 0x562451995151 in DeleteSelf ./../../services/network/url_loader.cc:1914
    #13 0x562451995151 in NotifyCompleted ./../../services/network/url_loader.cc:1893
    #14 0x562451995151 in ?? ??:0
    #15 0x5624519a0d46 in network::URLLoader::OnResponseStarted(net::URLRequest*, int) ./../../services/network/url_loader.cc:1333
    #16 0x5624519a0d46 in ?? ??:0
    #17 0x562451895dee in net::URLRequestHttpJob::OnStartCompleted(int) ./../../net/url_request/url_request_http_job.cc:969
    #18 0x562451895dee in ?? ??:0
    #19 0x56244dae5fb2 in net::HttpCache::Transaction::DoLoop(int) ./../../base/callback.h:101
    #20 0x56244dae5fb2 in DoLoop ./../../net/http/http_cache_transaction.cc:1005
    #21 0x56244dae5fb2 in ?? ??:0
    #22 0x56244dafe22b in base::internal::Invoker<base::internal::BindState<void (net::HttpCache::Transaction::*)(int), base::WeakPtr<net::HttpCache::Transaction> >, void (int)>::Run(base::internal::BindStateBase*, int) ./../../base/bind_internal.h:509
    #23 0x56244dafe22b in MakeItSo<void (net::HttpCache::Transaction::*const &)(int), const base::WeakPtr<net::HttpCache::Transaction> &, int> ./../../base/bind_internal.h:668
    #24 0x56244dafe22b in RunImpl<void (net::HttpCache::Transaction::*const &)(int), const std::tuple<base::WeakPtr<net::HttpCache::Transaction> > &, 0> ./../../base/bind_internal.h:721
    #25 0x56244dafe22b in Run ./../../base/bind_internal.h:703
    #26 0x56244dafe22b in ?? ??:0
    #27 0x56244dad2b85 in net::HttpCache::ProcessEntryFailure(net::HttpCache::ActiveEntry*) ./../../base/callback.h:169
    #28 0x56244dad2b85 in ProcessEntryFailure ./../../net/http/http_cache.cc:1058
    #29 0x56244dad2b85 in ?? ??:0
    #30 0x56244dad254e in net::HttpCache::DoneWithEntry(net::HttpCache::ActiveEntry*, net::HttpCache::Transaction*, bool, bool) ./../../net/http/http_cache.cc:?
    #31 0x56244dad254e in ?? ??:0
    #32 0x56244dae2783 in net::HttpCache::Transaction::DoneWithEntry(bool) ./../../net/http/http_cache_transaction.cc:3189
    #33 0x56244dae2783 in ?? ??:0
    #34 0x56244dae03e8 in net::HttpCache::Transaction::~Transaction() ./../../net/http/http_cache_transaction.cc:216
    #35 0x56244dae03e8 in ?? ??:0
    #36 0x56244dae29cd in net::HttpCache::Transaction::~Transaction() ./../../net/http/http_cache_transaction.cc:206
    #37 0x56244dae29cd in ?? ??:0
    #38 0x562451892535 in net::URLRequestHttpJob::DestroyTransaction() ./../../buildtools/third_party/libc++/trunk/include/memory:1335
    #39 0x562451892535 in reset ./../../buildtools/third_party/libc++/trunk/include/memory:1596
    #40 0x562451892535 in DestroyTransaction ./../../net/url_request/url_request_http_job.cc:373
    #41 0x562451892535 in ?? ??:0
    #42 0x5624518922f9 in net::URLRequestHttpJob::Kill() ./../../net/url_request/url_request_http_job.cc:309
    #43 0x5624518922f9 in ?? ??:0
    #44 0x56244dd8fd5f in net::URLRequest::DoCancel(int, net::SSLInfo const&) ./../../net/url_request/url_request.cc:724
    #45 0x56244dd8fd5f in ?? ??:0
    #46 0x56244dd874c9 in net::URLRequest::~URLRequest() ./../../net/url_request/url_request.cc:685
    #47 0x56244dd874c9 in ~URLRequest ./../../net/url_request/url_request.cc:179
    #48 0x56244dd874c9 in ?? ??:0
    #49 0x56244dd8824d in net::URLRequest::~URLRequest() ./../../net/url_request/url_request.cc:170
    #50 0x56244dd8824d in ?? ??:0
    #51 0x56245199844f in network::URLLoader::~URLLoader() ./../../buildtools/third_party/libc++/trunk/include/memory:1335
    #52 0x56245199844f in reset ./../../buildtools/third_party/libc++/trunk/include/memory:1596
    #53 0x56245199844f in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/memory:1550
    #54 0x56245199844f in ~URLLoader ./../../services/network/url_loader.cc:979
    #55 0x56245199844f in ?? ??:0
    #56 0x56245199879d in network::URLLoader::~URLLoader() ./../../services/network/url_loader.cc:973
    #57 0x56245199879d in ?? ??:0
    #58 0x5624518d361d in std::__1::__tree<std::__1::unique_ptr<network::mojom::URLLoader, std::__1::default_delete<network::mojom::URLLoader> >, base::UniquePtrComparator, std::__1::allocator<std::__1::unique_ptr<network::mojom::URLLoader, std::__1::default_delete<network::mojom::URLLoader> > > >::destroy(std::__1::__tree_node<std::__1::unique_ptr<network::mojom::URLLoader, std::__1::default_delete<network::mojom::URLLoader> >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/memory:1335
    #59 0x5624518d361d in reset ./../../buildtools/third_party/libc++/trunk/include/memory:1596
    #60 0x5624518d361d in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/memory:1550
    #61 0x5624518d361d in destroy<std::unique_ptr<network::mojom::URLLoader>, void, void> ./../../buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:317
    #62 0x5624518d361d in std::__1::__tree<std::__1::unique_ptr<network::mojom::URLLoader, std::__1::default_delete<network::mojom::URLLoader> >, base::UniquePtrComparator, std::__1::allocator<std::__1::unique_ptr<network::mojom::URLLoader, std::__1::default_delete<network::mojom::URLLoader> > > >::destroy(std::__1::__tree_node<std::__1::unique_ptr<network::mojom::URLLoader, std::__1::default_delete<network::mojom::URLLoader> >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/__tree:1801
    #63 0x5624518d361d in ?? ??:0
    #64 0x5624518d35b1 in std::__1::__tree<std::__1::unique_ptr<network::mojom::URLLoader, std::__1::default_delete<network::mojom::URLLoader> >, base::UniquePtrComparator, std::__1::allocator<std::__1::unique_ptr<network::mojom::URLLoader, std::__1::default_delete<network::mojom::URLLoader> > > >::destroy(std::__1::__tree_node<std::__1::unique_ptr<network::mojom::URLLoader, std::__1::default_delete<network::mojom::URLLoader> >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/__tree:1798
    #65 0x5624518d35b1 in ?? ??:0
    #66 0x5624518cec08 in ~__tree ./../../buildtools/third_party/libc++/trunk/include/__tree:1789
    #67 0x5624518cec08 in ~set ./../../buildtools/third_party/libc++/trunk/include/set:605
    #68 0x5624518cec08 in ~CorsURLLoaderFactory ./../../services/network/cors/cors_url_loader_factory.cc:212
    #69 0x5624518cec08 in ?? ??:0
    #70 0x56245180bd24 in operator() ./../../buildtools/third_party/libc++/trunk/include/memory:1335
    #71 0x56245180bd24 in reset ./../../buildtools/third_party/libc++/trunk/include/memory:1596
    #72 0x56245180bd24 in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/memory:1550
    #73 0x56245180bd24 in destroy<std::unique_ptr<network::cors::CorsURLLoaderFactory>, void, void> ./../../buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:317
    #74 0x56245180bd24 in std::__1::__tree<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> >, base::UniquePtrComparator, std::__1::allocator<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> > > >::destroy(std::__1::__tree_node<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/__tree:1801
    #75 0x56245180bd24 in ?? ??:0
    #76 0x56245180bcf9 in std::__1::__tree<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> >, base::UniquePtrComparator, std::__1::allocator<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> > > >::destroy(std::__1::__tree_node<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/__tree:1799
    #77 0x56245180bcf9 in ?? ??:0
    #78 0x56245180bcd9 in std::__1::__tree<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> >, base::UniquePtrComparator, std::__1::allocator<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> > > >::destroy(std::__1::__tree_node<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/__tree:1798
    #79 0x56245180bcd9 in ?? ??:0
    #80 0x56245180bcd9 in std::__1::__tree<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> >, base::UniquePtrComparator, std::__1::allocator<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> > > >::destroy(std::__1::__tree_node<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/__tree:1798
    #81 0x56245180bcd9 in ?? ??:0
    #82 0x56245180bcd9 in std::__1::__tree<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> >, base::UniquePtrComparator, std::__1::allocator<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> > > >::destroy(std::__1::__tree_node<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/__tree:1798
    #83 0x56245180bcd9 in ?? ??:0
    #84 0x56245180bcd9 in std::__1::__tree<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> >, base::UniquePtrComparator, std::__1::allocator<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> > > >::destroy(std::__1::__tree_node<std::__1::unique_ptr<network::cors::CorsURLLoaderFactory, std::__1::default_delete<network::cors::CorsURLLoaderFactory> >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/__tree:1798
    #85 0x56245180bcd9 in ?? ??:0
    #86 0x5624517f27f2 in ~__tree ./../../buildtools/third_party/libc++/trunk/include/__tree:1789
    #87 0x5624517f27f2 in ~set ./../../buildtools/third_party/libc++/trunk/include/set:605
    #88 0x5624517f27f2 in ~NetworkContext ./../../services/network/network_context.cc:533
    #89 0x5624517f27f2 in ?? ??:0
    #90 0x5624517f386d in network::NetworkContext::~NetworkContext() ./../../services/network/network_context.cc:491
    #91 0x5624517f386d in ?? ??:0

previously allocated by thread T3 (Chrome_ChildIOT) here:
 ca5dcd)
    #92 0x5624518cf0af in network::cors::CorsURLLoaderFactory::OnLoaderCreated(std::__1::unique_ptr<network::mojom::URLLoader, std::__1::default_delete<network::mojom::URLLoader> >) ./../../buildtools/third_party/libc++/trunk/include/new:235
    #93 0x5624518cf0af in __libcpp_allocate ./../../buildtools/third_party/libc++/trunk/include/new:261
    #94 0x5624518cf0af in allocate ./../../buildtools/third_party/libc++/trunk/include/memory:778
    #95 0x5624518cf0af in allocate ./../../buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:260
    #96 0x5624518cf0af in __construct_node<std::unique_ptr<network::mojom::URLLoader> > ./../../buildtools/third_party/libc++/trunk/include/__tree:2133
    #97 0x5624518cf0af in __emplace_unique_key_args<std::unique_ptr<network::mojom::URLLoader>, std::unique_ptr<network::mojom::URLLoader> > ./../../buildtools/third_party/libc++/trunk/include/__tree:2096
    #98 0x5624518cf0af in __insert_unique ./../../buildtools/third_party/libc++/trunk/include/__tree:1260
    #99 0x5624518cf0af in insert ./../../buildtools/third_party/libc++/trunk/include/set:675
    #100 0x5624518cf0af in OnLoaderCreated ./../../services/network/cors/cors_url_loader_factory.cc:218
    #101 0x5624518cf0af in ?? ??:0
    #102 0x5624519c443c in network::URLLoaderFactory::CreateLoaderAndStart(mojo::PendingReceiver<network::mojom::URLLoader>, int, unsigned int, network::ResourceRequest const&, mojo::PendingRemote<network::mojom::URLLoaderClient>, net::MutableNetworkTrafficAnnotationTag const&) ./../../services/network/url_loader_factory.cc:299
    #103 0x5624519c443c in ?? ??:0
    #104 0x5624518cfe72 in network::cors::CorsURLLoaderFactory::CreateLoaderAndStart(mojo::PendingReceiver<network::mojom::URLLoader>, int, unsigned int, network::ResourceRequest const&, mojo::PendingRemote<network::mojom::URLLoaderClient>, net::MutableNetworkTrafficAnnotationTag const&) ./../../services/network/cors/cors_url_loader_factory.cc:292
    #105 0x5624518cfe72 in ?? ??:0
    #106 0x5624401bf1e3 in network::mojom::URLLoaderFactoryStubDispatch::Accept(network::mojom::URLLoaderFactory*, mojo::Message*) ./gen/services/network/public/mojom/url_loader_factory.mojom.cc:237
    #107 0x5624401bf1e3 in ?? ??:0
    #108 0x56244d5e6653 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:850
    #109 0x56244d5e6653 in ?? ??:0
    #110 0x56244d5f67ba in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:48
    #111 0x56244d5f67ba in ?? ??:0
    #112 0x56244d602519 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:1023
    #113 0x56244d602519 in ?? ??:0
    #114 0x56244d600c7b in mojo::internal::MultiplexRouter::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:690
    #115 0x56244d600c7b in ?? ??:0
    #116 0x56244d5f68a1 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43
    #117 0x56244d5f68a1 in ?? ??:0
    #118 0x56244d5dfb05 in mojo::Connector::DispatchMessage(mojo::Message) ./../../mojo/public/cpp/bindings/lib/connector.cc:522
    #119 0x56244d5dfb05 in ?? ??:0
    #120 0x56244d5e1530 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:580
    #121 0x56244d5e1530 in ?? ??:0
    #122 0x56244d647f9d in Run ./../../base/callback.h:169
    #123 0x56244d647f9d in OnHandleReady ./../../mojo/public/cpp/system/simple_watcher.cc:278
    #124 0x56244d647f9d in ?? ??:0
    #125 0x56244d648cb3 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) ./../../mojo/public/cpp/system/simple_watcher.cc:94
    #126 0x56244d648cb3 in ?? ??:0
    #127 0x56244d64614a in mojo::SimpleWatcher::Context::CallNotify(MojoTrapEvent const*) ./../../mojo/public/cpp/system/simple_watcher.cc:59
    #128 0x56244d64614a in ?? ??:0
    #129 0x56244300e545 in mojo::core::WatcherDispatcher::InvokeWatchCallback(unsigned long, unsigned int, mojo::core::HandleSignalsState const&, unsigned int) ./../../mojo/core/watcher_dispatcher.cc:94
    #130 0x56244300e545 in ?? ??:0
    #131 0x56244300d30a in mojo::core::Watch::InvokeCallback(unsigned int, mojo::core::HandleSignalsState const&, unsigned int) ./../../mojo/core/watch.cc:78
    #132 0x56244300d30a in ?? ??:0
    #133 0x562443001f38 in mojo::core::RequestContext::~RequestContext() ./../../mojo/core/request_context.cc:72
    #134 0x562443001f38 in ?? ??:0
    #135 0x562442fe14ad in mojo::core::NodeChannel::OnChannelMessage(void const*, unsigned long, std::__1::vector<mojo::PlatformHandle, std::__1::allocator<mojo::PlatformHandle> >) ./../../mojo/core/node_channel.cc:828
    #136 0x562442fe14ad in ?? ??:0
    #137 0x562442fb3109 in mojo::core::Channel::TryDispatchMessage(base::span<char const, 18446744073709551615ul>, unsigned long*) ./../../mojo/core/channel.cc:722
    #138 0x562442fb3109 in ?? ??:0
    #139 0x562442fb27c2 in mojo::core::Channel::OnReadComplete(unsigned long, unsigned long*) ./../../mojo/core/channel.cc:619
    #140 0x562442fb27c2 in ?? ??:0
    #141 0x562443022615 in mojo::core::ChannelPosix::OnFileCanReadWithoutBlocking(int) ./../../mojo/core/channel_posix.cc:319
    #142 0x562443022615 in ?? ??:0
    #143 0x56244be02fe7 in base::MessagePumpLibevent::OnLibeventNotification(int, short, void*) message_pump_libevent.cc:?
    #144 0x56244be02fe7 in ?? ??:0
    #145 0x56244c1b6fac in event_process_active ./../../base/third_party/libevent/event.c:381
    #146 0x56244c1b6fac in event_base_loop ./../../base/third_party/libevent/event.c:521
    #147 0x56244c1b6fac in ?? ??:0
    #148 0x56244be036d2 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_libevent.cc:216
    #149 0x56244be036d2 in ?? ??:0
    #150 0x56244bccfdfc in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:460
    #151 0x56244bccfdfc in ?? ??:0
    #152 0x56244bc14f41 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:133
    #153 0x56244bc14f41 in ?? ??:0
    #154 0x56244bd22ec2 in base::Thread::Run(base::RunLoop*) ./../../base/threading/thread.cc:312
    #155 0x56244bd22ec2 in ?? ??:0
    #156 0x56244bd233c7 in base::Thread::ThreadMain() ./../../base/threading/thread.cc:383
    #157 0x56244bd233c7 in ?? ??:0
    #158 0x56244bdb1485 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:87
    #159 0x56244bdb1485 in ?? ??:0

Thread T3 (Chrome_ChildIOT) created by T0 (chrome) here:
    #0 0x56243e739c5c in __interceptor_pthread_create /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:207
    #1 0x56243e739c5c in ?? ??:0
    #2 0x56244bdb06ee in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, base::PlatformThreadHandle*, base::ThreadPriority) ./../../base/threading/platform_thread_posix.cc:126
    #3 0x56244bdb06ee in ?? ??:0
    #4 0x56244bd222c0 in base::Thread::StartWithOptions(base::Thread::Options const&) ./../../base/threading/thread.cc:187
    #5 0x56244bd222c0 in ?? ??:0
    #6 0x5624584fa354 in content::ChildProcess::ChildProcess(base::ThreadPriority, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::unique_ptr<base::ThreadPoolInstance::InitParams, std::__1::default_delete<base::ThreadPoolInstance::InitParams> >) ./../../content/child/child_process.cc:111
    #7 0x5624584fa354 in ?? ??:0
    #8 0x56244b8aeb63 in content::UtilityMain(content::MainFunctionParams const&) ./../../content/utility/utility_main.cc:141
    #9 0x56244b8aeb63 in ?? ??:0
    #10 0x56244b969e9e in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:958
    #11 0x56244b969e9e in ?? ??:0
    #12 0x56244b9644a6 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) ./../../content/app/content_main.cc:372
    #13 0x56244b9644a6 in ?? ??:0
    #14 0x56244b9649fc in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:398
    #15 0x56244b9649fc in ?? ??:0
    #16 0x56243e77ca6b in ChromeMain ./../../chrome/app/chrome_main.cc:151
    #17 0x56243e77ca6b in ?? ??:0
error: unknown argument '--demangle=True'
    #18 0x7f748df590b2 in __libc_start_main ??:?
    #19 0x7f748df590b2 in ?? ??:0

SUMMARY: AddressSanitizer: heap-use-after-free (/home/exp11/asan-linux-release-875559/chrome+0x1ddff63b)
Shadow bytes around the buggy address:
  0x0c0880005cf0: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fd
  0x0c0880005d00: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fd
  0x0c0880005d10: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fd
  0x0c0880005d20: fa fa fd fd fd fd fd fa fa fa fd fd fd fd fd fa
  0x0c0880005d30: fa fa fd fd fd fd fd fa fa fa fd fd fd fd fd fd
=>0x0c0880005d40: fa fa fd fd fd fd fd fd fa fa fd[fd]fd fd fd fa
  0x0c0880005d50: fa fa fd fd fd fd fd fa fa fa fd fd fd fd fd fa
  0x0c0880005d60: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fa
  0x0c0880005d70: fa fa fd fd fd fd fd fa fa fa fd fd fd fd fd fd
  0x0c0880005d80: fa fa fd fd fd fd fd fa fa fa fd fd fd fd fd fa
  0x0c0880005d90: fa fa fd fd fd fd fd fa fa fa fd fd fd fd fd fd
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
==1787713==ABORTING

Did this work before? N/A 

Chrome version:  92.0.4511.0  Channel: dev
OS Version: 20.0.4
Flash Version:

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 770 B)

## Timeline

### [Deleted User] (2021-05-17)

[Empty comment from Monorail migration]

### xi...@chromium.org (2021-05-17)

Thanks for the report! +lukasza to take a look again. Would it be possible it is regressed in M91/M92? From my reading in https://crbug.com/1174943, it seems that CF cannot reproduce the issue.

[Monorail components: Internals>Network]

### xi...@chromium.org (2021-05-17)

+Tools>Stability>ClusterFuzz for the answer to the original question in https://crbug.com/1174943#c8:

do we need to make sure (in this bug?  in a follow-up?) that this kind of a scenario is covered by ClusterFuzz or other such testing infrastructure? This crash is only reproducible by pressing "ctril + C" repeatedly to force close the browser, would CF support it?

### xi...@chromium.org (2021-05-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-18)

Setting milestone and target because of Security_Impact=Beta and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-18)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-18)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### lu...@chromium.org (2021-05-18)

I have trouble understanding what is going on here.  It seems that free happened in thread T3 at the following callstack:

    ...
    #2 CorsURLLoaderFactory::DestroyURLLoader(network::mojom::URLLoader*) 
    ...
    #9 DestroyURLLoader services/network/cors/cors_url_loader_factory.cc:226
    ...
    #12 DeleteSelf services/network/url_loader.cc:1914
    #13 NotifyCompleted services/network/url_loader.cc:1893
    ...
    #15 network::URLLoader::OnResponseStarted(net::URLRequest*, int) 
    ...
    #17 0x562451895dee in net::URLRequestHttpJob::OnStartCompleted(int) 
    ...

The line numbers from callstack frame #9 match the following:

    221 void CorsURLLoaderFactory::DestroyURLLoader(mojom::URLLoader* loader) {
    222   if (context_)
    223     context_->LoaderDestroyed(process_id_);
    224   auto it = loaders_.find(loader);
    225   DCHECK(it != loaders_.end());
    226   loaders_.erase(it);  // <=== HERE ===
    227
    228   DeleteIfNeeded();
    229 }

So far so good - nothing unexpected above AFAICT.  An important thing to note is that the freed loader has been removed from the `loaders_` set on line 226.

But then, if the loader has been removed from the `loaders_` set above, then how can it be Used-after-Free when the set and CorsURLLoaderFactory is destroyed (on the same thread - T3):

    ...
    #3 ~set
    #4 ~CorsURLLoaderFactory
    ...
    #26 network::NetworkContext::~NetworkContext
    ...
    #38 DestroyNetworkContexts
    #39 ~NetworkService
    ...

AFAICT the callstack frame #3 above is trying to destroy contents of the following set:

    121   std::set<std::unique_ptr<mojom::URLLoader>, base::UniquePtrComparator>
    122       loaders_;



### lu...@chromium.org (2021-05-18)

+mpdenton@ to see if they can help understand this bug.  FWIW, r610459 and r852311 were fixing other UaF in this code area.

[Monorail components: Internals>Services>Network]

### ad...@google.com (2021-05-18)

Dicsussed with Łukasz, and he says it's a pre-existing problem so setting Security_Impact=Stable.

### mp...@google.com (2021-05-19)

This is modification of the |loaders_| set during destruction of that set.

You can see from the free stack trace that the NetworkService is being destructed in response to something, probably a Mojo pipe from the browser process is closing. That leads to the destruction of |loaders_|. While recursing through the tree (of |loaders_|), destroying the left node (stack frame #64 0x5624518d35b1) causes a chain of callbacks that looks roughly like this:
    #8 0x5624518cf539 in erase ./../../buildtools/third_party/libc++/trunk/include/set:687
    #9 0x5624518cf539 in DestroyURLLoader ./../../services/network/cors/cors_url_loader_factory.cc:226
    #11 0x562451995151 in network::URLLoader::NotifyCompleted(int) ./../../base/callback.h:101
    #12 0x562451995151 in DeleteSelf ./../../services/network/url_loader.cc:1914
    #13 0x562451995151 in NotifyCompleted ./../../services/network/url_loader.cc:1893
    #15 0x5624519a0d46 in network::URLLoader::OnResponseStarted(net::URLRequest*, int) ./../../services/network/url_loader.cc:1333
    #17 0x562451895dee in net::URLRequestHttpJob::OnStartCompleted(int) ./../../net/url_request/url_request_http_job.cc:969
    #20 0x56244dae5fb2 in DoLoop ./../../net/http/http_cache_transaction.cc:1005
    #28 0x56244dad2b85 in ProcessEntryFailure ./../../net/http/http_cache.cc:1058
    #30 0x56244dad254e in net::HttpCache::DoneWithEntry(net::HttpCache::ActiveEntry*, net::HttpCache::Transaction*, bool, bool) ./../../net/http/http_cache.cc:?
    #32 0x56244dae2783 in net::HttpCache::Transaction::DoneWithEntry(bool) ./../../net/http/http_cache_transaction.cc:3189
    #34 0x56244dae03e8 in net::HttpCache::Transaction::~Transaction() ./../../net/http/http_cache_transaction.cc:216
    #40 0x562451892535 in DestroyTransaction ./../../net/url_request/url_request_http_job.cc:373
    #42 0x5624518922f9 in net::URLRequestHttpJob::Kill() ./../../net/url_request/url_request_http_job.cc:309
    #44 0x56244dd8fd5f in net::URLRequest::DoCancel(int, net::SSLInfo const&) ./../../net/url_request/url_request.cc:724
    #46 0x56244dd874c9 in net::URLRequest::~URLRequest() ./../../net/url_request/url_request.cc:685
    #54 0x56245199844f in ~URLLoader ./../../services/network/url_loader.cc:979

I.e. the CorsURLLoaderFactory then modifies |loaders_|, erasing a loader from the set. This may or may not corrupt the set, but it certainly modifies it. So when we return to the set::destroy function and try to destroy the right node of the tree (stack frame #0 0x5624518d363b), our current node has apparently already been destroyed.

I'm not sure what conditions lead to this happening. When I tried to reproduce, I ran into this DCHECK: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/loader/document_loader.cc;l=901;bpv=1

### mp...@google.com (2021-05-19)

(important to note that the free and use stack traces mostly overlap, with 0x5624518cec08 the code address where the free and use stack traces diverge.)

### lu...@chromium.org (2021-05-19)

RE: https://crbug.com/chromium/1209769#c11: mpdenton@:

Thanks!  Your comment helped a lot.

I am struggling a bit with writing a regression test for this problem.  Specifically, I have trouble making HttpCache::DoneWithEntry call into ProcessEntryFailure (trigerring the double-free shown in https://crbug.com/chromium/1209769#c11).  I am not sure what test steps are needed to ensure that an ActiveEntry associated with a destroyed network::URLLoader will either 1) have a non-empty `done_headers_queue` or 2) be in the headers phase.  My WIP CL is at https://crrev.com/c/2907872 - this reaches frame #32 from https://crbug.com/chromium/1209769#c11, but doesn't go further...

FWIW, it seems to me that the cleanest fix would be to "reset" `delete_callback_` when network::URLLoader's destructor runs.  In our case, the `delete_callback_` is CorsURLLoaderFactory::DestroyURLLoader which triggers the 2nd destruction of the same URLLoader object.

Alternatively, we could tweak CorsURLLoaderFactory::DestroyURLLoader to become a no-op after CorsURLLoaderFactory's destructor has  run.  Or yet another alternative would be to "move" the loaders out of `loaders_` in CorsURLLoaderFactory's destructor (and make sure that CorsURLLoaderFactory::DestroyURLLoader can handle a situation where it doesn't find the loader in the set).  Both of these seem a bit icky.

### lu...@chromium.org (2021-05-19)

mmenke@, could you please help with figuring out how to add a regression test for this?  (see my troubles in https://crbug.com/chromium/1209769#c13)

### mm...@chromium.org (2021-05-20)

[shivanisha]:  Are you familiar with HttpCache::DoneWithEntry?

### mm...@chromium.org (2021-05-20)

I think HttpCache::Transaction should not be calling into URLRequestHttpJob on destruction - net classes, in general, never call into their owner when their owner destroys them.  So I think the right fix is at the cache layer, not the services/network layer.

### lu...@chromium.org (2021-05-20)

RE: https://crbug.com/chromium/1209769#c16: mmenke@:

Thanks for the feedback.  Would you mind if I reassigned to you?  I have very little experience working with the //net code... :-/

### mm...@chromium.org (2021-05-20)

[Empty comment from Monorail migration]

### mm...@chromium.org (2021-05-24)

I think the issue is that destroying one HttpCache::Transaction during teardown can call into another HttpCache::Transaction, so what we're seeing is not a single transaction, but two of them...And calling back into an std::set while its tearing down its elements can result in a crash.

[Shivanisha]:  Is there any case where HttpCache::Transaction::~Transaction() can call into HttpCache::ProcessEntryFailure and then call into a callback for the HttpCache::Transaction currently being destroyed?

### mm...@chromium.org (2021-05-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2021-05-25)

Re https://crbug.com/chromium/1209769#c19
Transaction 1's HttpCache::Transaction::~Transaction() calls DoneWithEntry (if it's not a transaction in add_to_entry_queue) which can then call into HttpCache::ProcessEntryFailure() which can call into other transactions' callbacks (headers_transaction or add_to_entry_queue or done_headers_queue transactions) but not into transaction 1's callback since DoneWithEntry would have first removed the transaction from headers_transaction and done_headers_queue. 

### mm...@chromium.org (2021-05-25)

[shivanisha, morlovich] I can't figure out how to reproduce this.  Using an in memory cache (and issue requests/deleting them synchronously), and making a bunch of requests for the same URL, I can get a non-empty list of queued_transactions, but all of them that are called with CACHE_RACE immediately restart, find the existing entry in DoOpenOrCreateEntry(), and then get ERR_IO_PENDING in DoAddToEntry()'s AddTransactionToEntry call.

I think the only way for there to be an error is for DoOpenOrCreateEntry() to not get an entry, and to fail synchronously (maybe by using LOAD_READ_ONLY_FROM_CACHE?).

I've tried using an on-disk cache, pausing after creating a first request for a hanging URL, and then making a bunch of other requests for the same URL, but whenever I do that, whether I pause or wait a bit first, there are never any queued transactions.

Any pointers?

At the moment, I'm leaning towards just making mock URLRequests, and have the first URLRequest that's destroyed cause the other two to invoke their callbacks.  That seems a bit synthetic, and doesn't really verify the issue has been fixed (And relies heavily on the assumption the transaction being destroyed is calling into other transactions, instead of itself, though maybe that's self-evident)

### mo...@chromium.org (2021-05-25)

OK, so you are quite a few steps ahead of me...

I would probably start with the tests with Parallel in their name in http_cache_unittest.cc, since they're good at timing things... huh, lots of those cover recovery from a deleted transaction and handing over responsibility elsewhere.

Looking at https://source.chromium.org/chromium/chromium/src/+/main:net/http/http_cache.cc;drc=74689f88041bdfe4c3c8233254d662092acb90e0;l=901, it needs to happen early, and in that case ERR_CACHE_RACE is indeed what's expected to happen --- basically the logic is that nothing is actually in-progress yet, so do it the easy way... So what I guess happens is that the restart gets to whatever state in the state machine calls out to net::URLRequestHttpJob::OnStartCompleted with an error code, and that aborts, while your experience is that it actually happens asynchronously. 

Then we would normally go DoHeadersPhaseCannotProceed -> DoGetBackend -> DoGetBackendComplete all synchronously. 

Looking at it, LOAD_ONLY_FROM_CACHE seems like a good bet, yes, since you can get ERR_CACHE_MISS synchronously from that. I am not sure how you can get mode_ = READ transactions to play together with the shared stuff, since they normally can't join other things --- maybe if it's too early for us to notice?

Hmm, the testcase has fonts, I think those might involve external validation from blink?


### mo...@chromium.org (2021-05-25)

External validation triggers mode_ = UPDATE, here:
https://source.chromium.org/chromium/chromium/src/+/main:net/http/http_cache_transaction.cc;drc=74689f88041bdfe4c3c8233254d662092acb90e0;l=1045

... which I think is parallelizable, but which will trigger and Open, not OpenOrCreate, which can synchronously fail in both memory and simple cache....


### gi...@appspot.gserviceaccount.com (2021-05-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2f49a3c69a2184c95f43a395e4f33a3959cb8dbc

commit 2f49a3c69a2184c95f43a395e4f33a3959cb8dbc
Author: Matt Menke <mmenke@chromium.org>
Date: Fri May 28 20:30:47 2021

Fix URLLoader cleanup on CorsURLLoaderFactory destruction.

Destroying one URLLoader can result in other URLLoaders getting errors,
due to to cache interconnectedness. CorsURLLoaderFactory's destructor
was not taking that into account.

Also fix a bonus bug:  HttpCache::Transaction::response_ wasn't being
cleared in HttpCache::Transaction::DoHeadersPhaseCannotProceed(), which
could result in DCHECKs when calling GetResponseInfo() when a
transaction that was waiting on a cached response from another
transaction ended up failing.

Bug: 1209769
Change-Id: I2c18caa488767a29011aca1e1b0bace24c1ba8fc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2922826
Reviewed-by: Maksim Orlovich <morlovich@chromium.org>
Commit-Queue: Matt Menke <mmenke@chromium.org>
Cr-Commit-Position: refs/heads/master@{#887522}

[modify] https://crrev.com/2f49a3c69a2184c95f43a395e4f33a3959cb8dbc/net/http/http_cache_transaction.cc
[modify] https://crrev.com/2f49a3c69a2184c95f43a395e4f33a3959cb8dbc/services/network/cors/cors_url_loader_factory.cc
[modify] https://crrev.com/2f49a3c69a2184c95f43a395e4f33a3959cb8dbc/services/network/cors/cors_url_loader_factory_unittest.cc


### mm...@chromium.org (2021-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-01)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-01)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-01)

Requesting merge to beta M91 because latest trunk commit (887522) appears to be after beta branch point (870763).

Requesting merge to future beta M92 because latest trunk commit (887522) appears to be after future beta branch point (56).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-06-01)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-06-02)

Your change meets the bar and is auto-approved for M92. Please go ahead and merge the CL to branch 4515 (refs/branch-heads/4515) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-06-03)

Approving merge to M92 - please merge to branch 4515 - and also to M91 - please merge to branch 4472 - assuming no problems have shown up in Canary.

### pb...@google.com (2021-06-03)

Your change has been approved for M91. Please go ahead and merge the CL to M91 branch : 4472 (refs/branch-heads/4472) manually asap.

### gi...@appspot.gserviceaccount.com (2021-06-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/33103b41f0d5ad35f8839455b1f28f1a3cab9cc4

commit 33103b41f0d5ad35f8839455b1f28f1a3cab9cc4
Author: Matt Menke <mmenke@chromium.org>
Date: Thu Jun 03 19:58:13 2021

[M92] Fix URLLoader cleanup on CorsURLLoaderFactory destruction.

Destroying one URLLoader can result in other URLLoaders getting errors,
due to to cache interconnectedness. CorsURLLoaderFactory's destructor
was not taking that into account.

Also fix a bonus bug:  HttpCache::Transaction::response_ wasn't being
cleared in HttpCache::Transaction::DoHeadersPhaseCannotProceed(), which
could result in DCHECKs when calling GetResponseInfo() when a
transaction that was waiting on a cached response from another
transaction ended up failing.

(cherry picked from commit 2f49a3c69a2184c95f43a395e4f33a3959cb8dbc)

Bug: 1209769
Change-Id: I2c18caa488767a29011aca1e1b0bace24c1ba8fc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2922826
Reviewed-by: Maksim Orlovich <morlovich@chromium.org>
Commit-Queue: Matt Menke <mmenke@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#887522}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2937517
Auto-Submit: Matt Menke <mmenke@chromium.org>
Commit-Queue: Maksim Orlovich <morlovich@chromium.org>
Cr-Commit-Position: refs/branch-heads/4515@{#295}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/33103b41f0d5ad35f8839455b1f28f1a3cab9cc4/net/http/http_cache_transaction.cc
[modify] https://crrev.com/33103b41f0d5ad35f8839455b1f28f1a3cab9cc4/services/network/cors/cors_url_loader_factory.cc
[modify] https://crrev.com/33103b41f0d5ad35f8839455b1f28f1a3cab9cc4/services/network/cors/cors_url_loader_factory_unittest.cc


### mm...@chromium.org (2021-06-03)

M91 tryjobs are failing due to bogus failures.  I'll keep trying, but no promises.

### mm...@chromium.org (2021-06-03)

https://ci.chromium.org/p/chromium-m91/builders/try/mac-rel - current state of M91 mac-rel is not good. :(

### gi...@appspot.gserviceaccount.com (2021-06-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/baf23e3c5b1394982cff718a0e055d4f239245ad

commit baf23e3c5b1394982cff718a0e055d4f239245ad
Author: Matt Menke <mmenke@chromium.org>
Date: Fri Jun 04 01:19:18 2021

[M91] Fix URLLoader cleanup on CorsURLLoaderFactory destruction.

Destroying one URLLoader can result in other URLLoaders getting errors,
due to to cache interconnectedness. CorsURLLoaderFactory's destructor
was not taking that into account.

Also fix a bonus bug:  HttpCache::Transaction::response_ wasn't being
cleared in HttpCache::Transaction::DoHeadersPhaseCannotProceed(), which
could result in DCHECKs when calling GetResponseInfo() when a
transaction that was waiting on a cached response from another
transaction ended up failing.

(cherry picked from commit 2f49a3c69a2184c95f43a395e4f33a3959cb8dbc)

Bug: 1209769
Change-Id: I2c18caa488767a29011aca1e1b0bace24c1ba8fc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2922826
Reviewed-by: Maksim Orlovich <morlovich@chromium.org>
Commit-Queue: Matt Menke <mmenke@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#887522}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2935241
Auto-Submit: Matt Menke <mmenke@chromium.org>
Cr-Commit-Position: refs/branch-heads/4472@{#1433}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/baf23e3c5b1394982cff718a0e055d4f239245ad/net/http/http_cache_transaction.cc
[modify] https://crrev.com/baf23e3c5b1394982cff718a0e055d4f239245ad/services/network/cors/cors_url_loader_factory.cc
[modify] https://crrev.com/baf23e3c5b1394982cff718a0e055d4f239245ad/services/network/cors/cors_url_loader_factory_unittest.cc


### am...@chromium.org (2021-06-08)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-08)

[Empty comment from Monorail migration]

### vs...@google.com (2021-06-09)

[Empty comment from Monorail migration]

### gi...@google.com (2021-06-09)

[Empty comment from Monorail migration]

### gi...@google.com (2021-06-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-06-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cdd1e87a933f094b3036c958c5a2c257a7e7dce4

commit cdd1e87a933f094b3036c958c5a2c257a7e7dce4
Author: Matt Menke <mmenke@chromium.org>
Date: Thu Jun 10 07:05:24 2021

[M86-LTS] Fix URLLoader cleanup on CorsURLLoaderFactory destruction.

Destroying one URLLoader can result in other URLLoaders getting errors,
due to to cache interconnectedness. CorsURLLoaderFactory's destructor
was not taking that into account.

Also fix a bonus bug:  HttpCache::Transaction::response_ wasn't being
cleared in HttpCache::Transaction::DoHeadersPhaseCannotProceed(), which
could result in DCHECKs when calling GetResponseInfo() when a
transaction that was waiting on a cached response from another
transaction ended up failing.

[M86] Used older API in cors_url_loader_factory_unittest.cc
      Added AddDefaultHandlers to EmbeddedTestServer

(cherry picked from commit 2f49a3c69a2184c95f43a395e4f33a3959cb8dbc)

(cherry picked from commit baf23e3c5b1394982cff718a0e055d4f239245ad)

Bug: 1209769
Change-Id: I2c18caa488767a29011aca1e1b0bace24c1ba8fc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2922826
Reviewed-by: Maksim Orlovich <morlovich@chromium.org>
Commit-Queue: Matt Menke <mmenke@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#887522}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2935241
Auto-Submit: Matt Menke <mmenke@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4472@{#1433}
Cr-Original-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2949089
Reviewed-by: Matt Menke <mmenke@chromium.org>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1662}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/cdd1e87a933f094b3036c958c5a2c257a7e7dce4/net/http/http_cache_transaction.cc
[modify] https://crrev.com/cdd1e87a933f094b3036c958c5a2c257a7e7dce4/net/test/embedded_test_server/embedded_test_server.cc
[modify] https://crrev.com/cdd1e87a933f094b3036c958c5a2c257a7e7dce4/net/test/embedded_test_server/embedded_test_server.h
[modify] https://crrev.com/cdd1e87a933f094b3036c958c5a2c257a7e7dce4/services/network/cors/cors_url_loader_factory.cc
[modify] https://crrev.com/cdd1e87a933f094b3036c958c5a2c257a7e7dce4/services/network/cors/cors_url_loader_factory_unittest.cc


### gi...@appspot.gserviceaccount.com (2021-06-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/910e9e40d3767d416a888d9c12b4c9d8a017750c

commit 910e9e40d3767d416a888d9c12b4c9d8a017750c
Author: Matt Menke <mmenke@chromium.org>
Date: Thu Jun 10 07:05:07 2021

[M90-LTS] Fix URLLoader cleanup on CorsURLLoaderFactory destruction.

Destroying one URLLoader can result in other URLLoaders getting errors,
due to to cache interconnectedness. CorsURLLoaderFactory's destructor
was not taking that into account.

Also fix a bonus bug:  HttpCache::Transaction::response_ wasn't being
cleared in HttpCache::Transaction::DoHeadersPhaseCannotProceed(), which
could result in DCHECKs when calling GetResponseInfo() when a
transaction that was waiting on a cached response from another
transaction ended up failing.

[M90]: Fixed trivial conflict

(cherry picked from commit 2f49a3c69a2184c95f43a395e4f33a3959cb8dbc)

(cherry picked from commit baf23e3c5b1394982cff718a0e055d4f239245ad)

Bug: 1209769
Change-Id: I2c18caa488767a29011aca1e1b0bace24c1ba8fc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2922826
Reviewed-by: Maksim Orlovich <morlovich@chromium.org>
Commit-Queue: Matt Menke <mmenke@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#887522}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2935241
Auto-Submit: Matt Menke <mmenke@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4472@{#1433}
Cr-Original-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2948654
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Reviewed-by: Matt Menke <mmenke@chromium.org>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1513}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/910e9e40d3767d416a888d9c12b4c9d8a017750c/net/http/http_cache_transaction.cc
[modify] https://crrev.com/910e9e40d3767d416a888d9c12b4c9d8a017750c/services/network/cors/cors_url_loader_factory.cc
[modify] https://crrev.com/910e9e40d3767d416a888d9c12b4c9d8a017750c/services/network/cors/cors_url_loader_factory_unittest.cc


### gi...@appspot.gserviceaccount.com (2021-06-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cdd1e87a933f094b3036c958c5a2c257a7e7dce4

commit cdd1e87a933f094b3036c958c5a2c257a7e7dce4
Author: Matt Menke <mmenke@chromium.org>
Date: Thu Jun 10 07:05:24 2021

[M86-LTS] Fix URLLoader cleanup on CorsURLLoaderFactory destruction.

Destroying one URLLoader can result in other URLLoaders getting errors,
due to to cache interconnectedness. CorsURLLoaderFactory's destructor
was not taking that into account.

Also fix a bonus bug:  HttpCache::Transaction::response_ wasn't being
cleared in HttpCache::Transaction::DoHeadersPhaseCannotProceed(), which
could result in DCHECKs when calling GetResponseInfo() when a
transaction that was waiting on a cached response from another
transaction ended up failing.

[M86] Used older API in cors_url_loader_factory_unittest.cc
      Added AddDefaultHandlers to EmbeddedTestServer

(cherry picked from commit 2f49a3c69a2184c95f43a395e4f33a3959cb8dbc)

(cherry picked from commit baf23e3c5b1394982cff718a0e055d4f239245ad)

Bug: 1209769
Change-Id: I2c18caa488767a29011aca1e1b0bace24c1ba8fc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2922826
Reviewed-by: Maksim Orlovich <morlovich@chromium.org>
Commit-Queue: Matt Menke <mmenke@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#887522}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2935241
Auto-Submit: Matt Menke <mmenke@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4472@{#1433}
Cr-Original-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2949089
Reviewed-by: Matt Menke <mmenke@chromium.org>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1662}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/cdd1e87a933f094b3036c958c5a2c257a7e7dce4/net/http/http_cache_transaction.cc
[modify] https://crrev.com/cdd1e87a933f094b3036c958c5a2c257a7e7dce4/net/test/embedded_test_server/embedded_test_server.cc
[modify] https://crrev.com/cdd1e87a933f094b3036c958c5a2c257a7e7dce4/net/test/embedded_test_server/embedded_test_server.h
[modify] https://crrev.com/cdd1e87a933f094b3036c958c5a2c257a7e7dce4/services/network/cors/cors_url_loader_factory.cc
[modify] https://crrev.com/cdd1e87a933f094b3036c958c5a2c257a7e7dce4/services/network/cors/cors_url_loader_factory_unittest.cc


### vs...@google.com (2021-06-10)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-15)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-06-23)

Congratulations! The VRP Panel has decided to award you $15,000 for this report. Excellent work! 

### am...@google.com (2021-06-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1209769?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Network, Internals>Services>Network]
[Monorail mergedwith: crbug.com/chromium/1209770]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055897)*
