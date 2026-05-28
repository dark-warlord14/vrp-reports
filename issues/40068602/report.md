# Security: Heap-use-after-free in blink::ThrottlingURLLoader::OnReceiveResponse

| Field | Value |
|-------|-------|
| **Issue ID** | [40068602](https://issues.chromium.org/issues/40068602) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Loader, Platform>Extensions |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | ho...@chromium.org |
| **Created** | 2023-08-03 |
| **Bounty** | $3,000.00 |

## Description

**REPRODUCTION CASE**  

Found by myfuzzer run on cf(<https://clusterfuzz.com/testcase-detail/6488999759380480>)  

But it cannot be reproduced stably, I manually provide analysis and report

#RCA

1. When ThrottlingURLLoader::OnReceiveResponse get call it will call throttle->WillProcessResponse to process response
2. throttle->WillProcessResponse will call to URLLoader::Context::OnCompletedRequest
3. in URLLoader::Context::OnCompletedRequest if status.error\_code != net::OK client\_->DidFail will be called which finally called to ResourceLoader::HandleError
4. ResourceLoader::HandleError may lead loader\_.reset()[3] which eventually leads to UAF

```
void ThrottlingURLLoader::OnReceiveResponse(  
    network::mojom::URLResponseHeadPtr response_head,  
    mojo::ScopedDataPipeConsumerHandle body,  
    absl::optional<mojo_base::BigBuffer> cached_metadata) {  
  DCHECK_EQ(DEFERRED_NONE, deferred_stage_);  
  DCHECK(!loader_completed_);  
//CUT  
  // Dispatch WillProcessResponse().  
  if (!throttles_.empty()) {  
    bool deferred = false;  
    for (auto& entry : throttles_) {  
      auto\* throttle = entry.throttle.get();  
      bool throttle_deferred = false;  
      base::Time start = base::Time::Now();  
      throttle->WillProcessResponse(response_url_, response_head.get(),			[1]  
                                    &throttle_deferred);  
      RecordExecutionTimeHistogram(GetStageNameForHistogram(DEFERRED_RESPONSE),  
                                   start);  
      if (!HandleThrottleResult(throttle, throttle_deferred, &deferred))		[4]  
        return;  
    }  
  
void URLLoader::Context::OnCompletedRequest(  
    const network::URLLoaderCompletionStatus& status) {  
  int64_t total_transfer_size = status.encoded_data_length;  
  int64_t encoded_body_size = status.encoded_body_length;  
  
  if (client_) {  
    TRACE_EVENT_WITH_FLOW0("loading", "URLLoader::Context::OnCompletedRequest",  
                           this, TRACE_EVENT_FLAG_FLOW_IN);  
  
    if (status.error_code != net::OK) {  
      client_->DidFail(WebURLError::Create(status, url_),						[2]  
                       status.completion_time, total_transfer_size,  
                       encoded_body_size, status.decoded_body_length);  
                         
void ResourceLoader::HandleError(const ResourceError& error) {  
  if (error.CorsErrorStatus() &&  
      error.CorsErrorStatus()  
          ->has_authorization_covered_by_wildcard_on_preflight) {  
    fetcher_->GetUseCounter().CountUse(  
        mojom::WebFeature::kAuthorizationCoveredByWildcard);  
  }  
、、CUT  
  Release(ResourceLoadScheduler::ReleaseOption::kReleaseAndSchedule,  
          ResourceLoadScheduler::TrafficReportHints::InvalidInstance());  
  loader_.reset();																[3]  
    

```

[1]  

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/common/loader/throttling_url_loader.cc;drc=68ba0c7da48fb0c6e1581c956a791b7a0fea86ad;l=741>  

[2]  

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/loader/fetch/url_loader/url_loader.cc;drc=dc7dc6612acdfd24a0f632a774a0d723b8f832b6;l=446>  

[3]  

<https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:third_party/blink/renderer/platform/loader/fetch/resource_loader.cc;drc=b27071598a6b291a7319d99ce7aa4af81ebc060f;l=1405>

```
=================================================================  
==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x51900007f38c at pc 0x5baa2d4cc010 bp 0x7ffe09613710 sp 0x7ffe09613708  
READ of size 1 at 0x51900007f38c thread T0 (chrome)  
SCARINESS: 40 (1-byte-read-heap-use-after-free)  
    #0 0x5baa2d4cc00f in HandleThrottleResult third_party/blink/common/loader/throttling_url_loader.cc:643:7  
    #1 0x5baa2d4cc00f in blink::ThrottlingURLLoader::OnReceiveResponse(mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, absl::optional<mojo_base::BigBuffer>) third_party/blink/common/loader/throttling_url_loader.cc:745:12  
    #2 0x5baa29f178cd in network::mojom::URLLoaderClientStubDispatch::Accept(network::mojom::URLLoaderClient\*, mojo::Message\*) gen/services/network/public/mojom/url_loader.mojom.cc:1207:13  
    #3 0x5baa3c88cd34 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1016:54  
    #4 0x5baa3c8a9b42 in mojo::MessageDispatcher::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19  
    #5 0x5baa3c891cf9 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:701:20  
    #6 0x5baa3c8b846e in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1096:42  
    #7 0x5baa3c8b66e0 in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/multiplex_router.cc:710:7  
    #8 0x5baa3c8a9b42 in mojo::MessageDispatcher::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19  
    #9 0x5baa3c882b8e in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) mojo/public/cpp/bindings/lib/connector.cc:561:49  
    #10 0x5baa3c884ad3 in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:618:14  
    #11 0x5baa3c8844bc in OnHandleReadyInternal mojo/public/cpp/bindings/lib/connector.cc:451:3  
    #12 0x5baa3c8844bc in mojo::Connector::OnWatcherHandleReady(char const\*, unsigned int) mojo/public/cpp/bindings/lib/connector.cc:417:3  
    #13 0x5baa3c8875c7 in Invoke<void (mojo::Connector::\*)(const char \*, unsigned int), mojo::Connector \*, const char \*, unsigned int> base/functional/bind_internal.h:714:12  
    #14 0x5baa3c8875c7 in MakeItSo<void (mojo::Connector::\*const &)(const char \*, unsigned int), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0> > &, unsigned int> base/functional/bind_internal.h:893:12  
    #15 0x5baa3c8875c7 in void base::internal::Invoker<base::internal::BindState<void (mojo::Connector::\*)(char const\*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0>>, void (unsigned int)>::RunImpl<void (mojo::Connector::\* const&)(char const\*, unsigned int), std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0>> const&, 0ul, 1ul>(void (mojo::Connector::\* const&)(char const\*, unsigned int), std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0>> const&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>, unsigned int&&) base/functional/bind_internal.h:993:12  
    #16 0x5baa3c8872b6 in base::internal::Invoker<base::internal::BindState<void (mojo::Connector::\*)(char const\*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase\*, unsigned int) base/functional/bind_internal.h:957:12  
    #17 0x5baa2d4bc7be in Run base/functional/callback.h:333:12  
    #18 0x5baa2d4bc7be in mojo::SimpleWatcher::DiscardReadyState(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.h:192:14  
    #19 0x5baa2d4bc9b8 in Invoke<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &> base/functional/bind_internal.h:632:12  
    #20 0x5baa2d4bc9b8 in MakeItSo<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, unsigned int, const mojo::HandleSignalsState &> base/functional/bind_internal.h:893:12  
    #21 0x5baa2d4bc9b8 in RunImpl<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, 0UL> base/functional/bind_internal.h:993:12  
    #22 0x5baa2d4bc9b8 in base::internal::Invoker<base::internal::BindState<void (\*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase\*, unsigned int, mojo::HandleSignalsState const&) base/functional/bind_internal.h:957:12  
    #23 0x5baa3c914fb7 in Run base/functional/callback.h:333:12  
    #24 0x5baa3c914fb7 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.cc:278:14  
    #25 0x5baa3c915ecf in Invoke<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), const base::WeakPtr<mojo::SimpleWatcher> &, int, unsigned int, mojo::HandleSignalsState> base/functional/bind_internal.h:714:12  
    #26 0x5baa3c915ecf in MakeItSo<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> > base/functional/bind_internal.h:921:5  
    #27 0x5baa3c915ecf in void base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::\*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>) base/functional/bind_internal.h:993:12  
    #28 0x5baa3a4b95c7 in Run base/functional/callback.h:152:12  
    #29 0x5baa3a4b95c7 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:201:34  
    #30 0x5baa3a51b965 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:482:11)> base/task/common/task_annotator.h:89:5  
    #31 0x5baa3a51b965 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:480:23  
    #32 0x5baa3a51a895 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:345:41  
    #33 0x5baa3a51c9a4 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0  
    #34 0x5baa3a3a1883 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message_loop/message_pump_default.cc:40:55  
    #35 0x5baa3a51d779 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:645:12  
    #36 0x5baa3a43edff in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14  
    #37 0x5baa52036045 in content::RendererMain(content::MainFunctionParams) content/renderer/renderer_main.cc:339:16  
    #38 0x5baa375d6957 in content::RunZygote(content::ContentMainDelegate\*) content/app/content_main_runner_impl.cc:654:14  
    #39 0x5baa375d80ef in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate\*) content/app/content_main_runner_impl.cc:754:12  
    #40 0x5baa375db3cc in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1118:10  
    #41 0x5baa375d41f8 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) content/app/content_main.cc:326:36  
    #42 0x5baa375d4e39 in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:343:10  
    #43 0x5baa2858c8bd in ChromeMain chrome/app/chrome_main.cc:187:12  
    #44 0x7be2ef5ae082 in __libc_start_main /build/glibc-SzIz7B/glibc-2.31/csu/libc-start.c:308:16  
0x51900007f38c is located 12 bytes inside of 904-byte region [0x51900007f380,0x51900007f708)  
freed by thread T0 (chrome) here:  
    #0 0x5baa2858aa9d in operator delete(void\*) third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3  
    #1 0x5baa36ad1689 in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:65:5  
    #2 0x5baa36ad1689 in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:297:7  
    #3 0x5baa36ad1689 in blink::ResourceRequestSender::DeletePendingRequest(scoped_refptr<base::SingleThreadTaskRunner>) third_party/blink/renderer/platform/loader/fetch/url_loader/resource_request_sender.cc:326:29  
    #4 0x5baa36ad0c57 in blink::ResourceRequestSender::Cancel(scoped_refptr<base::SingleThreadTaskRunner>) third_party/blink/renderer/platform/loader/fetch/url_loader/resource_request_sender.cc:284:3  
    #5 0x5baa36add415 in blink::URLLoader::Context::Cancel() third_party/blink/renderer/platform/loader/fetch/url_loader/url_loader.cc:231:31  
    #6 0x5baa36ae28af in Cancel third_party/blink/renderer/platform/loader/fetch/url_loader/url_loader.cc:590:15  
    #7 0x5baa36ae28af in ~URLLoader third_party/blink/renderer/platform/loader/fetch/url_loader/url_loader.cc:485:3  
    #8 0x5baa36ae28af in blink::URLLoader::~URLLoader() third_party/blink/renderer/platform/loader/fetch/url_loader/url_loader.cc:484:25  
    #9 0x5baa36a42de3 in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:65:5  
    #10 0x5baa36a42de3 in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:297:7  
    #11 0x5baa36a42de3 in blink::ResourceLoader::HandleError(blink::ResourceError const&) third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:1405:11  
    #12 0x5baa36a3dbdf in blink::ResourceLoader::DidFail(blink::WebURLError const&, base::TimeTicks, long, unsigned long, long) third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:1360:3  
    #13 0x5baa36ae18b6 in blink::URLLoader::Context::OnCompletedRequest(network::URLLoaderCompletionStatus const&) third_party/blink/renderer/platform/loader/fetch/url_loader/url_loader.cc:446:16  
    #14 0x5baa36ad46ce in blink::ResourceRequestSender::OnRequestComplete(network::URLLoaderCompletionStatus const&) third_party/blink/renderer/platform/loader/fetch/url_loader/resource_request_sender.cc:569:11  
    #15 0x5baa2d4d34fe in CancelWithExtendedError third_party/blink/common/loader/throttling_url_loader.cc:954:23  
    #16 0x5baa2d4d34fe in blink::ThrottlingURLLoader::ForwardingThrottleDelegate::CancelWithExtendedError(int, int, std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>) third_party/blink/common/loader/throttling_url_loader.cc:155:14  
    #17 0x5baa38cc9cc1 in extensions::ExtensionLocalizationThrottle::WillProcessResponse(GURL const&, network::mojom::URLResponseHead\*, bool\*) extensions/renderer/extension_localization_throttle.cc:220:16  
    #18 0x5baa2d4cb533 in blink::ThrottlingURLLoader::OnReceiveResponse(mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, absl::optional<mojo_base::BigBuffer>) third_party/blink/common/loader/throttling_url_loader.cc:741:17  
    #19 0x5baa29f178cd in network::mojom::URLLoaderClientStubDispatch::Accept(network::mojom::URLLoaderClient\*, mojo::Message\*) gen/services/network/public/mojom/url_loader.mojom.cc:1207:13  
    #20 0x5baa3c88cd34 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1016:54  
    #21 0x5baa3c8a9b42 in mojo::MessageDispatcher::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19  
    #22 0x5baa3c891cf9 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:701:20  
    #23 0x5baa3c8b846e in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1096:42  
    #24 0x5baa3c8b66e0 in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/multiplex_router.cc:710:7  
    #25 0x5baa3c8a9b42 in mojo::MessageDispatcher::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19  
    #26 0x5baa3c882b8e in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) mojo/public/cpp/bindings/lib/connector.cc:561:49  
    #27 0x5baa3c884ad3 in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:618:14  
    #28 0x5baa3c8844bc in OnHandleReadyInternal mojo/public/cpp/bindings/lib/connector.cc:451:3  
    #29 0x5baa3c8844bc in mojo::Connector::OnWatcherHandleReady(char const\*, unsigned int) mojo/public/cpp/bindings/lib/connector.cc:417:3  
    #30 0x5baa3c8875c7 in Invoke<void (mojo::Connector::\*)(const char \*, unsigned int), mojo::Connector \*, const char \*, unsigned int> base/functional/bind_internal.h:714:12  
    #31 0x5baa3c8875c7 in MakeItSo<void (mojo::Connector::\*const &)(const char \*, unsigned int), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0> > &, unsigned int> base/functional/bind_internal.h:893:12  
    #32 0x5baa3c8875c7 in void base::internal::Invoker<base::internal::BindState<void (mojo::Connector::\*)(char const\*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0>>, void (unsigned int)>::RunImpl<void (mojo::Connector::\* const&)(char const\*, unsigned int), std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0>> const&, 0ul, 1ul>(void (mojo::Connector::\* const&)(char const\*, unsigned int), std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0>> const&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>, unsigned int&&) base/functional/bind_internal.h:993:12  
    #33 0x5baa3c8872b6 in base::internal::Invoker<base::internal::BindState<void (mojo::Connector::\*)(char const\*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase\*, unsigned int) base/functional/bind_internal.h:957:12  
    #34 0x5baa2d4bc7be in Run base/functional/callback.h:333:12  
    #35 0x5baa2d4bc7be in mojo::SimpleWatcher::DiscardReadyState(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.h:192:14  
    #36 0x5baa2d4bc9b8 in Invoke<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &> base/functional/bind_internal.h:632:12  
    #37 0x5baa2d4bc9b8 in MakeItSo<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, unsigned int, const mojo::HandleSignalsState &> base/functional/bind_internal.h:893:12  
    #38 0x5baa2d4bc9b8 in RunImpl<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, 0UL> base/functional/bind_internal.h:993:12  
    #39 0x5baa2d4bc9b8 in base::internal::Invoker<base::internal::BindState<void (\*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase\*, unsigned int, mojo::HandleSignalsState const&) base/functional/bind_internal.h:957:12  
    #40 0x5baa3c914fb7 in Run base/functional/callback.h:333:12  
    #41 0x5baa3c914fb7 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.cc:278:14  
    #42 0x5baa3c915ecf in Invoke<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), const base::WeakPtr<mojo::SimpleWatcher> &, int, unsigned int, mojo::HandleSignalsState> base/functional/bind_internal.h:714:12  
    #43 0x5baa3c915ecf in MakeItSo<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> > base/functional/bind_internal.h:921:5  
    #44 0x5baa3c915ecf in void base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::\*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>) base/functional/bind_internal.h:993:12  
    #45 0x5baa3a4b95c7 in Run base/functional/callback.h:152:12  
    #46 0x5baa3a4b95c7 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:201:34  
    #47 0x5baa3a51b965 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:482:11)> base/task/common/task_annotator.h:89:5  
    #48 0x5baa3a51b965 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:480:23  
previously allocated by thread T0 (chrome) here:  
    #0 0x5baa2858a23d in operator new(unsigned long) third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3  
    #1 0x5baa2d4c143f in blink::ThrottlingURLLoader::CreateLoaderAndStart(scoped_refptr<network::SharedURLLoaderFactory>, std::__Cr::vector<std::__Cr::unique_ptr<blink::URLLoaderThrottle, std::__Cr::default_delete<blink::URLLoaderThrottle>>, std::__Cr::allocator<std::__Cr::unique_ptr<blink::URLLoaderThrottle, std::__Cr::default_delete<blink::URLLoaderThrottle>>>>, int, unsigned int, network::ResourceRequest\*, network::mojom::URLLoaderClient\*, net::NetworkTrafficAnnotationTag const&, scoped_refptr<base::SingleThreadTaskRunner>, absl::optional<std::__Cr::vector<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::allocator<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>>>) third_party/blink/common/loader/throttling_url_loader.cc:331:47  
    #2 0x5baa36ad03ad in blink::ResourceRequestSender::SendAsync(std::__Cr::unique_ptr<network::ResourceRequest, std::__Cr::default_delete<network::ResourceRequest>>, scoped_refptr<base::SingleThreadTaskRunner>, net::NetworkTrafficAnnotationTag const&, unsigned int, WTF::Vector<WTF::String, 0u, WTF::PartitionAllocator> const&, scoped_refptr<blink::ResourceRequestClient>, scoped_refptr<network::SharedURLLoaderFactory>, blink::WebVector<std::__Cr::unique_ptr<blink::URLLoaderThrottle, std::__Cr::default_delete<blink::URLLoaderThrottle>>>, std::__Cr::unique_ptr<blink::ResourceLoadInfoNotifierWrapper, std::__Cr::default_delete<blink::ResourceLoadInfoNotifierWrapper>>, blink::BackForwardCacheLoaderHelper\*) third_party/blink/renderer/platform/loader/fetch/url_loader/resource_request_sender.cc:260:7  
    #3 0x5baa36adf08a in blink::URLLoader::Context::Start(std::__Cr::unique_ptr<network::ResourceRequest, std::__Cr::default_delete<network::ResourceRequest>>, scoped_refptr<blink::WebURLRequestExtraData>, bool, bool, base::TimeDelta, blink::SyncLoadResponse\*, std::__Cr::unique_ptr<blink::ResourceLoadInfoNotifierWrapper, std::__Cr::default_delete<blink::ResourceLoadInfoNotifierWrapper>>) third_party/blink/renderer/platform/loader/fetch/url_loader/url_loader.cc:338:43  
    #4 0x5baa36ae3d47 in blink::URLLoader::LoadAsynchronously(std::__Cr::unique_ptr<network::ResourceRequest, std::__Cr::default_delete<network::ResourceRequest>>, scoped_refptr<blink::WebURLRequestExtraData>, bool, std::__Cr::unique_ptr<blink::ResourceLoadInfoNotifierWrapper, std::__Cr::default_delete<blink::ResourceLoadInfoNotifierWrapper>>, blink::URLLoaderClient\*) third_party/blink/renderer/platform/loader/fetch/url_loader/url_loader.cc:582:13  
    #5 0x5baa36a3ed7d in blink::ResourceLoader::RequestAsynchronously(blink::ResourceRequestHead const&) third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:1528:12  
    #6 0x5baa36a3b674 in blink::ResourceLoader::StartWith(blink::ResourceRequestHead const&) third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:688:5  
    #7 0x5baa36a2caee in blink::ResourceLoadScheduler::Run(unsigned long, blink::ResourceLoadSchedulerClient\*, bool, blink::WebURLRequest::Priority) third_party/blink/renderer/platform/loader/fetch/resource_load_scheduler.cc:384:11  
    #8 0x5baa36a2c21d in blink::ResourceLoadScheduler::Request(blink::ResourceLoadSchedulerClient\*, blink::ResourceLoadScheduler::ThrottleOption, blink::WebURLRequest::Priority, int, unsigned long\*) third_party/blink/renderer/platform/loader/fetch/resource_load_scheduler.cc:165:5  
    #9 0x5baa36a3a001 in blink::ResourceLoader::Start() third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:593:15  
    #10 0x5baa369eb130 in blink::ResourceFetcher::StartLoad(blink::Resource\*, blink::ResourceRequestBody, blink::ResourceFetcher::ImageLoadBlockingPolicy, blink::RenderBlockingBehavior) third_party/blink/renderer/platform/loader/fetch/resource_fetcher.cc:2450:11  
    #11 0x5baa369e3b81 in blink::ResourceFetcher::RequestResource(blink::FetchParameters&, blink::ResourceFactory const&, blink::ResourceClient\*) third_party/blink/renderer/platform/loader/fetch/resource_fetcher.cc:1437:10  
    #12 0x5baa48dd6276 in blink::CSSStyleSheetResource::Fetch(blink::FetchParameters&, blink::ResourceFetcher\*, blink::ResourceClient\*) third_party/blink/renderer/core/loader/resource/css_style_sheet_resource.cc:62:16  
    #13 0x5baa48dc81c8 in blink::PreloadHelper::StartPreload(blink::ResourceType, blink::FetchParameters&, blink::Document&) third_party/blink/renderer/core/loader/preload_helper.cc:925:11  
    #14 0x5baa4a8d71ec in blink::PreloadRequest::Start(blink::Document\*) third_party/blink/renderer/core/html/parser/preload_request.cc:177:10  
    #15 0x5baa4a8579ca in blink::HTMLResourcePreloader::Preload(std::__Cr::unique_ptr<blink::PreloadRequest, std::__Cr::default_delete<blink::PreloadRequest>>) third_party/blink/renderer/core/html/parser/html_resource_preloader.cc:77:12  
    #16 0x5baa4a8d7b04 in blink::ResourcePreloader::TakeAndPreload(WTF::Vector<std::__Cr::unique_ptr<blink::PreloadRequest, std::__Cr::default_delete<blink::PreloadRequest>>, 0u, WTF::PartitionAllocator>&) third_party/blink/renderer/core/html/parser/resource_preloader.cc:17:5  
    #17 0x5baa4a7b38fa in blink::HTMLDocumentParser::FetchQueuedPreloads() third_party/blink/renderer/core/html/parser/html_document_parser.cc:1374:17  
    #18 0x5baa4a7b49e0 in blink::HTMLDocumentParser::ProcessPreloadData(std::__Cr::unique_ptr<blink::PendingPreloadData, std::__Cr::default_delete<blink::PendingPreloadData>>) third_party/blink/renderer/core/html/parser/html_document_parser.cc:1364:3  
    #19 0x5baa4a7a9b1c in blink::HTMLDocumentParser::ScanAndPreload(blink::HTMLPreloadScanner\*) third_party/blink/renderer/core/html/parser/html_document_parser.cc:1316:3  
    #20 0x5baa4a7aca96 in blink::HTMLDocumentParser::Append(WTF::String const&) third_party/blink/renderer/core/html/parser/html_document_parser.cc:929:7  
    #21 0x5baa47e10822 in UpdateDocument third_party/blink/renderer/core/dom/decoded_data_document_parser.cc:99:3  
    #22 0x5baa47e10822 in blink::DecodedDataDocumentParser::AppendBytes(char const\*, unsigned long) third_party/blink/renderer/core/dom/decoded_data_document_parser.cc:63:3  
    #23 0x5baa4a7b2bdd in blink::HTMLDocumentParser::AppendBytes(char const\*, unsigned long) third_party/blink/renderer/core/html/parser/html_document_parser.cc:1256:30  
    #24 0x5baa48ca2d20 in blink::DocumentLoader::CommitData(blink::DocumentLoader::BodyData&) third_party/blink/renderer/core/loader/document_loader.cc:1378:8  
    #25 0x5baa48c9f639 in blink::DocumentLoader::ProcessDataBuffer(blink::DocumentLoader::BodyData\*) third_party/blink/renderer/core/loader/document_loader.cc:1603:5  
    #26 0x5baa48c9e191 in blink::DocumentLoader::BodyDataReceivedImpl(blink::DocumentLoader::BodyData&) third_party/blink/renderer/core/loader/document_loader.cc:1117:3  
    #27 0x5baa48c9e74c in BodyDataReceived third_party/blink/renderer/core/loader/document_loader.cc:1065:3  
    #28 0x5baa48c9e74c in non-virtual thunk to blink::DocumentLoader::BodyDataReceived(base::span<char const, 18446744073709551615ul>) third_party/blink/renderer/core/loader/document_loader.cc:0  
    #29 0x5baa36ac6153 in blink::NavigationBodyLoader::MainThreadBodyReader::DataReceived(char const\*, unsigned long) third_party/blink/renderer/platform/loader/fetch/url_loader/navigation_body_loader.cc:317:23  
    #30 0x5baa36abfae4 in blink::(anonymous namespace)::ReadFromDataPipeImpl(blink::(anonymous namespace)::BodyReader&, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>&, mojo::SimpleWatcher&) third_party/blink/renderer/platform/loader/fetch/url_loader/navigation_body_loader.cc:113:17  
    #31 0x5baa36abec5f in blink::NavigationBodyLoader::ReadFromDataPipe() third_party/blink/renderer/platform/loader/fetch/url_loader/navigation_body_loader.cc:520:3  
SUMMARY: AddressSanitizer: heap-use-after-free (/mnt/scratch0/clusterfuzz/bot/builds/chromium-browser-asan_linux-release_4392242b7f59878a2775b4607420a2b37e17ff13/revisions/asan-linux-release-1178329/chrome+0x1384c00f) (BuildId: 80680b4c8302fcaa)  
Shadow bytes around the buggy address:  
  0x51900007f100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  
  0x51900007f180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  
  0x51900007f200: fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa fa  
  0x51900007f280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
  0x51900007f300: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
=>0x51900007f380: fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd  
  0x51900007f400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  
  0x51900007f480: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  
  0x51900007f500: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  
  0x51900007f580: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  
  0x51900007f600: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  
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
==1==ADDITIONAL INFO  
==1==Note: Please include this section with the ASan report.  
Task trace:  
    #0 0x5baa3c9158d6 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) mojo/public/cpp/system/simple_watcher.cc:102:13  
==1==END OF ADDITIONAL INFO  
==1==ABORTING  

```

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 29.9 KB)
- [patch4rep.diff](attachments/patch4rep.diff) (text/plain, 680 B)
- [clusterfuzz-testcase-6488999759380480.zip](attachments/clusterfuzz-testcase-6488999759380480.zip) (application/octet-stream, 161.1 KB)

## Timeline

### [Deleted User] (2023-08-03)

[Comment Deleted]

### m....@gmail.com (2023-08-03)

bisect:
https://chromium-review.googlesource.com/c/chromium/src/+/4257812

### ts...@chromium.org (2023-08-03)

Sorry, no PoC so I couldn't try to reproduce. Perhaps there is enough information in the report to take action.
Assigning per author of claimed bisected CL, though without a PoC I haven't been able to verity the bisect.
Tentatively setting foundin based on above.



[Monorail components: Blink>Loader Platform>Extensions]

### [Deleted User] (2023-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-03)

[Empty comment from Monorail migration]

### m....@gmail.com (2023-08-04)

You can get the original poc by visiting the CF(https://clusterfuzz.com/testcase-detail/6488999759380480)

#REPRODUCE
1. apply patch4rep.diff to simulate create_pipe_result != MOJO_RESULT_OK condition
2. unzip clusterfuzz-testcase-6488999759380480.zip and find fuzz-00395.html
3. chrome --js-flags="--expose-gc --allow-natives-syntax" --no-sandbox --disable-extensions --user-data-dir=test--enable-logging=stderr fuzz-00395.html

### ho...@chromium.org (2023-08-04)

I can reproduce it by loading an extension with a css file after patching patch4rep.diff.

I created a cl to fix this issue.
https://chromium-review.googlesource.com/c/chromium/src/+/4751579

### ho...@chromium.org (2023-08-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-04)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-04)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-08-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6bb386bf2a6462eb2a33100833d564a2fd0f8225

commit 6bb386bf2a6462eb2a33100833d564a2fd0f8225
Author: Tsuyoshi Horo <horo@chromium.org>
Date: Tue Aug 08 01:33:05 2023

Fix ExtensionLocalizationThrottle::WillProcessResponse

Synchronous call of `delegate_->CancelWithError()` inside
blink::URLLoaderThrottle::WillProcessResponse() in Blink can cause UAF.
To fix this, this CL change ExtensionLocalizationThrottle::
WillProcessResponse() to set `defer` to true, and asynchronously call
`delegate_->CancelWithError()`.

Bug: 1469754
Change-Id: Ic129ba4b39a9c1ab00eb6609db824b065296e66d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4751579
Reviewed-by: David Bertoni <dbertoni@chromium.org>
Commit-Queue: Tsuyoshi Horo <horo@chromium.org>
Reviewed-by: Adam Rice <ricea@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1180638}

[modify] https://crrev.com/6bb386bf2a6462eb2a33100833d564a2fd0f8225/extensions/renderer/extension_localization_throttle.h
[modify] https://crrev.com/6bb386bf2a6462eb2a33100833d564a2fd0f8225/extensions/renderer/extension_localization_throttle.cc
[modify] https://crrev.com/6bb386bf2a6462eb2a33100833d564a2fd0f8225/extensions/renderer/extension_localization_throttle_unittest.cc


### ho...@chromium.org (2023-08-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-09)

Requesting merge to extended stable M114 because latest trunk commit (1180638) appears to be after extended stable branch point (1135570).

Requesting merge to stable M115 because latest trunk commit (1180638) appears to be after stable branch point (1148114).

Requesting merge to beta M116 because latest trunk commit (1180638) appears to be after beta branch point (1160321).

Merge review required: M114 is already shipping to stable.

Merge review required: M115 is already shipping to stable.

Merge review required: M116 has already been cut for stable release.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115, 116].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-10)

Requesting merge to extended stable M114 because latest trunk commit (1180638) appears to be after extended stable branch point (1135570).

Requesting merge to other stable M115 because latest trunk commit (1180638) appears to be after other stable branch point (1148114).

Requesting merge to stable M116 because latest trunk commit (1180638) appears to be after stable branch point (1160321).

Not requesting merge to dev (M117) because latest trunk commit (1180638) appears to be prior to dev branch point (1181205). If this is incorrect, please replace the Merge-NA-117 label with Merge-Request-117. If other changes are required to fix this bug completely, please request a merge if necessary.

Merge approved: your change passed merge requirements and is auto-approved for M117. Please go ahead and merge the CL to branch 5938 (refs/branch-heads/5938) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: harrysouders (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

Merge review required: M114 is already shipping to stable.

Merge review required: M115 is already shipping to stable.

Merge review required: M116 has already been cut for stable release.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115, 116].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-14)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-08-14)

116 merge approved for https://crrev.com/c/4751579; please merge this fix to branch 5845 at your earliest convenience so this fix can be included in the first M116/ Stable security refresh

This fix landed on 117 so no merge needed for 117, nor for 115 and 114 as there are no further planned releases of either

### gi...@appspot.gserviceaccount.com (2023-08-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/28759f24f051b5e79b2ae75f4f39ff63e5607119

commit 28759f24f051b5e79b2ae75f4f39ff63e5607119
Author: Tsuyoshi Horo <horo@chromium.org>
Date: Tue Aug 15 03:13:52 2023

[M116] Fix ExtensionLocalizationThrottle::WillProcessResponse

Synchronous call of `delegate_->CancelWithError()` inside
blink::URLLoaderThrottle::WillProcessResponse() in Blink can cause UAF.
To fix this, this CL change ExtensionLocalizationThrottle::
WillProcessResponse() to set `defer` to true, and asynchronously call
`delegate_->CancelWithError()`.

(cherry picked from commit 6bb386bf2a6462eb2a33100833d564a2fd0f8225)

Bug: 1469754
Change-Id: Ic129ba4b39a9c1ab00eb6609db824b065296e66d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4751579
Reviewed-by: David Bertoni <dbertoni@chromium.org>
Commit-Queue: Tsuyoshi Horo <horo@chromium.org>
Reviewed-by: Adam Rice <ricea@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1180638}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4777752
Commit-Queue: David Bertoni <dbertoni@chromium.org>
Auto-Submit: Tsuyoshi Horo <horo@chromium.org>
Reviewed-by: Tsuyoshi Horo <horo@chromium.org>
Cr-Commit-Position: refs/branch-heads/5845@{#1471}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/28759f24f051b5e79b2ae75f4f39ff63e5607119/extensions/renderer/extension_localization_throttle.h
[modify] https://crrev.com/28759f24f051b5e79b2ae75f4f39ff63e5607119/extensions/renderer/extension_localization_throttle.cc
[modify] https://crrev.com/28759f24f051b5e79b2ae75f4f39ff63e5607119/extensions/renderer/extension_localization_throttle_unittest.cc


### [Deleted User] (2023-08-15)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ho...@chromium.org (2023-08-15)

> 1. Was this issue a regression for the milestone it was found in?

Yes, this regression was introduced at 113.0.5616.0 by https://crrev.com/c/4751579

> 2. Is this issue related to a change or feature merged after the latest LTS Milestone?

No. This was just a refactoring CL.

### am...@google.com (2023-08-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-16)

Congratulations! The VRP Panel has decided to award you $2,000 for this report of a significantly mitigated security bug -- mitigated by the memory conditions required to exploit this issue, which appear difficult to achieve in a reliable fashion -- + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### vo...@google.com (2023-08-17)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-08-18)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-18)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-22)

[Empty comment from Monorail migration]

### vo...@google.com (2023-08-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-24)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2023-08-24)

1. One https://crrev.com/c/4807952
2. Low - small change, no conflicts
3. M116
4. Yes

### gm...@google.com (2023-08-24)

[Empty comment from Monorail migration]

### vo...@google.com (2023-08-29)

[Empty comment from Monorail migration]

### gm...@google.com (2023-09-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-09-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8b1ec2333a31d4d18f6a6b56f8dd9bd9944ca787

commit 8b1ec2333a31d4d18f6a6b56f8dd9bd9944ca787
Author: Tsuyoshi Horo <horo@chromium.org>
Date: Mon Sep 11 13:20:38 2023

[M114-LTS] Fix ExtensionLocalizationThrottle::WillProcessResponse

Synchronous call of `delegate_->CancelWithError()` inside
blink::URLLoaderThrottle::WillProcessResponse() in Blink can cause UAF.
To fix this, this CL change ExtensionLocalizationThrottle::
WillProcessResponse() to set `defer` to true, and asynchronously call
`delegate_->CancelWithError()`.

(cherry picked from commit 6bb386bf2a6462eb2a33100833d564a2fd0f8225)

(cherry picked from commit 28759f24f051b5e79b2ae75f4f39ff63e5607119)

Bug: 1469754
Change-Id: Ic129ba4b39a9c1ab00eb6609db824b065296e66d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4751579
Commit-Queue: Tsuyoshi Horo <horo@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/main@{#1180638}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4777752
Commit-Queue: David Bertoni <dbertoni@chromium.org>
Auto-Submit: Tsuyoshi Horo <horo@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/5845@{#1471}
Cr-Original-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4807952
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Reviewed-by: Tsuyoshi Horo <horo@chromium.org>
Commit-Queue: Zakhar Voit <voit@google.com>
Cr-Commit-Position: refs/branch-heads/5735@{#1595}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/8b1ec2333a31d4d18f6a6b56f8dd9bd9944ca787/extensions/renderer/extension_localization_throttle.h
[modify] https://crrev.com/8b1ec2333a31d4d18f6a6b56f8dd9bd9944ca787/extensions/renderer/extension_localization_throttle.cc
[modify] https://crrev.com/8b1ec2333a31d4d18f6a6b56f8dd9bd9944ca787/extensions/renderer/extension_localization_throttle_unittest.cc


### vo...@google.com (2023-09-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1469754?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Loader, Platform>Extensions]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40068602)*
