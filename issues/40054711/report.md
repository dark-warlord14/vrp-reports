# uaf in CrossOriginEmbedderPolicyReporter(browser)

| Field | Value |
|-------|-------|
| **Issue ID** | [40054711](https://issues.chromium.org/issues/40054711) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>SecurityFeature>OriginPolicy, Blink>Workers |
| **Platforms** | Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | as...@chromium.org |
| **Created** | 2021-02-06 |
| **Bounty** | $15,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36

Steps to reproduce the problem:
Chromium 90.0.4411.0 canary (asan build)
Chromium 90.0.4408.0 dev (asan build)
1.launch simple webserver
python3.8 -m http.server 8000

2. Open browser.
	./chrome --user-data-dir=/tmp/xx http://localhost:8000

3. Click crash.html, and will show popup blocker message.Select "always allow popup from http://localhost:8000".

4. Close the Browser.

5. Directly access http://localhost:8000/crash.html
./chrome --user-data-dir=/tmp/xx http://localhost:8000/crash.html
6. Then will repro uaf crash in browser process.

What is the expected behavior?

What went wrong?
==169889==ERROR: AddressSanitizer: heap-use-after-free on address 0x615000263b10 at pc 0x563555d273ee bp 0x7ffe7f697630 sp 0x7ffe7f697628
READ of size 8 at 0x615000263b10 thread T0 (chrome)
    #0 0x563555d273ed in mojo::ReceiverSetBase<mojo::Receiver<network::mojom::CrossOriginEmbedderPolicyReporter, mojo::RawPtrImplRefTraits<network::mojom::CrossOriginEmbedderPolicyReporter> >, void>::AddImpl(network::mojom::CrossOriginEmbedderPolicyReporter*, mojo::PendingReceiver<network::mojom::CrossOriginEmbedderPolicyReporter>, bool, scoped_refptr<base::SequencedTaskRunner>) ./../../mojo/public/cpp/bindings/receiver_set.h:361:38
    #1 0x563555d266fb in Add ./../../mojo/public/cpp/bindings/receiver_set.h:130:12
    #2 0x563555d266fb in content::CrossOriginEmbedderPolicyReporter::Clone(mojo::PendingReceiver<network::mojom::CrossOriginEmbedderPolicyReporter>) ./../../content/browser/net/cross_origin_embedder_policy_reporter.cc:83:17
    #3 0x563555b21eef in content::DedicatedWorkerHost::BindCacheStorage(mojo::PendingReceiver<blink::mojom::CacheStorage>) ./../../content/browser/worker_host/dedicated_worker_host.cc:504:19
    #4 0x56355477f3b8 in Invoke<void (content::DedicatedWorkerHost::*)(mojo::PendingReceiver<blink::mojom::CacheStorage>), content::DedicatedWorkerHost *, mojo::PendingReceiver<blink::mojom::CacheStorage> > ./../../base/bind_internal.h:498:12
    #5 0x56355477f3b8 in MakeItSo<void (content::DedicatedWorkerHost::*const &)(mojo::PendingReceiver<blink::mojom::CacheStorage>), content::DedicatedWorkerHost *, mojo::PendingReceiver<blink::mojom::CacheStorage> > ./../../base/bind_internal.h:637:12
    #6 0x56355477f3b8 in RunImpl<void (content::DedicatedWorkerHost::*const &)(mojo::PendingReceiver<blink::mojom::CacheStorage>), const std::tuple<base::internal::UnretainedWrapper<content::DedicatedWorkerHost> > &, 0> ./../../base/bind_internal.h:710:12
    #7 0x56355477f3b8 in base::internal::Invoker<base::internal::BindState<void (content::DedicatedWorkerHost::*)(mojo::PendingReceiver<blink::mojom::CacheStorage>), base::internal::UnretainedWrapper<content::DedicatedWorkerHost> >, void (mojo::PendingReceiver<blink::mojom::CacheStorage>)>::Run(base::internal::BindStateBase*, mojo::PendingReceiver<blink::mojom::CacheStorage>&&) ./../../base/bind_internal.h:692:12
    #8 0x563554757507 in Run ./../../base/callback.h:168:12
    #9 0x563554757507 in void mojo::internal::BinderContextTraits<void>::BindGenericReceiver<blink::mojom::CacheStorage>(base::RepeatingCallback<void (mojo::PendingReceiver<blink::mojom::CacheStorage>)> const&, mojo::ScopedHandleBase<mojo::MessagePipeHandle>) ./../../mojo/public/cpp/bindings/lib/binder_map_internal.h:69:12
    #10 0x56355475770c in Invoke<void (*const &)(const base::RepeatingCallback<void (mojo::PendingReceiver<blink::mojom::CacheStorage>)> &, mojo::ScopedHandleBase<mojo::MessagePipeHandle>), const base::RepeatingCallback<void (mojo::PendingReceiver<blink::mojom::CacheStorage>)> &, mojo::ScopedHandleBase<mojo::MessagePipeHandle> > ./../../base/bind_internal.h:393:12
    #11 0x56355475770c in MakeItSo<void (*const &)(const base::RepeatingCallback<void (mojo::PendingReceiver<blink::mojom::CacheStorage>)> &, mojo::ScopedHandleBase<mojo::MessagePipeHandle>), const base::RepeatingCallback<void (mojo::PendingReceiver<blink::mojom::CacheStorage>)> &, mojo::ScopedHandleBase<mojo::MessagePipeHandle> > ./../../base/bind_internal.h:637:12
    #12 0x56355475770c in RunImpl<void (*const &)(const base::RepeatingCallback<void (mojo::PendingReceiver<blink::mojom::CacheStorage>)> &, mojo::ScopedHandleBase<mojo::MessagePipeHandle>), const std::tuple<base::RepeatingCallback<void (mojo::PendingReceiver<blink::mojom::CacheStorage>)> > &, 0> ./../../base/bind_internal.h:710:12
    #13 0x56355475770c in base::internal::Invoker<base::internal::BindState<void (*)(base::RepeatingCallback<void (mojo::PendingReceiver<blink::mojom::CacheStorage>)> const&, mojo::ScopedHandleBase<mojo::MessagePipeHandle>), base::RepeatingCallback<void (mojo::PendingReceiver<blink::mojom::CacheStorage>)> >, void (mojo::ScopedHandleBase<mojo::MessagePipeHandle>)>::Run(base::internal::BindStateBase*, mojo::ScopedHandleBase<mojo::MessagePipeHandle>&&) ./../../base/bind_internal.h:692:12
    #14 0x563551b58c4d in Run ./../../base/callback.h:168:12
    #15 0x563551b58c4d in RunCallback ./../../mojo/public/cpp/bindings/lib/binder_map_internal.h:121:14
    #16 0x563551b58c4d in mojo::internal::GenericCallbackBinderWithContext<void>::BindInterface(mojo::ScopedHandleBase<mojo::MessagePipeHandle>) ./../../mojo/public/cpp/bindings/lib/binder_map_internal.h:109:5
    #17 0x563551b58902 in mojo::BinderMapWithContext<void>::TryBind(mojo::GenericPendingReceiver*) ./../../mojo/public/cpp/bindings/binder_map.h:90:17
    #18 0x563555b238b5 in content::BrowserInterfaceBrokerImpl<content::DedicatedWorkerHost, url::Origin const&>::BindInterface(mojo::GenericPendingReceiver) ./../../content/browser/browser_interface_broker_impl.h:83:22
    #19 0x563555b235ad in content::BrowserInterfaceBrokerImpl<content::DedicatedWorkerHost, url::Origin const&>::GetInterface(mojo::GenericPendingReceiver) ./../../content/browser/browser_interface_broker_impl.h:51:7
    #20 0x5635525e22d0 in blink::mojom::BrowserInterfaceBrokerStubDispatch::Accept(blink::mojom::BrowserInterfaceBroker*, mojo::Message*) ./gen/third_party/blink/public/mojom/browser_interface_broker.mojom.cc:137:13
    #21 0x56355d93d411 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:554:54
    #22 0x56355d94a7c2 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:41:19
    #23 0x56355d95661e in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:955:42
    #24 0x56355d954d36 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:622:38
    #25 0x56355d94a7c2 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:41:19
    #26 0x56355d9365bf in mojo::Connector::DispatchMessage(mojo::Message) ./../../mojo/public/cpp/bindings/lib/connector.cc:508:49
    #27 0x56355d938326 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:566:14
    #28 0x56355d99f896 in Run ./../../base/callback.h:168:12
    #29 0x56355d99f896 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple_watcher.cc:278:14
    #30 0x56355d9a0e10 in Invoke<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> ./../../base/bind_internal.h:498:12
    #31 0x56355d9a0e10 in MakeItSo<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> ./../../base/bind_internal.h:657:5
    #32 0x56355d9a0e10 in RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), std::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0, 1, 2, 3> ./../../base/bind_internal.h:710:12
    #33 0x56355d9a0e10 in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:679:12
    #34 0x56355be76d63 in Run ./../../base/callback.h:101:12
    #35 0x56355be76d63 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:163:33
    #36 0x56355beb6c87 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:351:25
    #37 0x56355beb6440 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:264:36
    #38 0x56355bd761ec in HandleDispatch ./../../base/message_loop/message_pump_glib.cc:374:46
    #39 0x56355bd761ec in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) ./../../base/message_loop/message_pump_glib.cc:124:43
    #40 0x7f697d4a9fbc in g_main_context_dispatch ??:0:0

0x615000263b10 is located 400 bytes inside of 512-byte region [0x615000263980,0x615000263b80)
freed by thread T0 (chrome) here:
    #0 0x56354f6cc50d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160:3
    #1 0x5635553f1079 in operator() ./../../buildtools/third_party/libc++/trunk/include/memory:2378:5
    #2 0x5635553f1079 in reset ./../../buildtools/third_party/libc++/trunk/include/memory:2633:7
    #3 0x5635553f1079 in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/memory:2587:19
    #4 0x5635553f1079 in content::RenderFrameHostImpl::~RenderFrameHostImpl() ./../../content/browser/renderer_host/render_frame_host_impl.cc:1296:1
    #5 0x5635553f516c in content::RenderFrameHostImpl::~RenderFrameHostImpl() ./../../content/browser/renderer_host/render_frame_host_impl.cc:1152:45
    #6 0x5635554a81db in operator() ./../../buildtools/third_party/libc++/trunk/include/memory:2378:5
    #7 0x5635554a81db in reset ./../../buildtools/third_party/libc++/trunk/include/memory:2633:7
    #8 0x5635554a81db in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/memory:2587:19
    #9 0x5635554a81db in content::RenderFrameHostManager::~RenderFrameHostManager() ./../../content/browser/renderer_host/render_frame_host_manager.cc:217:3
    #10 0x5635551be855 in content::FrameTreeNode::~FrameTreeNode() ./../../content/browser/renderer_host/frame_tree_node.cc:231:1
    #11 0x5635551b4da4 in content::FrameTree::~FrameTree() ./../../content/browser/renderer_host/frame_tree.cc:129:3
    #12 0x56355594e20d in content::WebContentsImpl::~WebContentsImpl() ./../../content/browser/web_contents/web_contents_impl.cc:980:1
    #13 0x563555951e1c in content::WebContentsImpl::~WebContentsImpl() ./../../content/browser/web_contents/web_contents_impl.cc:860:37
    #14 0x5635674aa514 in operator() ./../../buildtools/third_party/libc++/trunk/include/memory:2378:5
    #15 0x5635674aa514 in reset ./../../buildtools/third_party/libc++/trunk/include/memory:2633:7
    #16 0x5635674aa514 in TabStripModel::SendDetachWebContentsNotifications(TabStripModel::DetachNotifications*) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:533:21
    #17 0x5635674b0dd3 in TabStripModel::InternalCloseTabs(base::span<content::WebContents* const, 18446744073709551615ul>, unsigned int) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:1756:5
    #18 0x5635674b157d in TabStripModel::CloseWebContentsAt(int, unsigned int) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:731:10
    #19 0x5635559e2665 in content::WebContentsImpl::Close(content::RenderViewHost*) ./../../content/browser/web_contents/web_contents_impl.cc:6820:16
    #20 0x5635524c20d1 in blink::mojom::LocalMainFrameHostStubDispatch::Accept(blink::mojom::LocalMainFrameHost*, mojo::Message*) ./gen/third_party/blink/public/mojom/frame/frame.mojom.cc:16838:13
    #21 0x56355d93d411 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:554:54
    #22 0x56355d94a6d8 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:46:24
    #23 0x56355f327fbd in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnProxyThread(mojo::Message) ./../../ipc/ipc_mojo_bootstrap.cc:945:24
    #24 0x56355f321108 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind_internal.h:498:12
    #25 0x56355f321108 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind_internal.h:637:12
    #26 0x56355f321108 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0, 1> ./../../base/bind_internal.h:710:12
    #27 0x56355f321108 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:679:12
    #28 0x56355be76d63 in Run ./../../base/callback.h:101:12
    #29 0x56355be76d63 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:163:33
    #30 0x56355beb6c87 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:351:25
    #31 0x56355beb6440 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:264:36
    #32 0x56355bd761ec in HandleDispatch ./../../base/message_loop/message_pump_glib.cc:374:46
    #33 0x56355bd761ec in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) ./../../base/message_loop/message_pump_glib.cc:124:43
    #34 0x7f697d4a9fbc in g_main_context_dispatch ??:0:0

previously allocated by thread T0 (chrome) here:
    #0 0x56354f6cbcad in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x56355538c1bb in make_unique<content::CrossOriginEmbedderPolicyReporter, content::StoragePartition *&, GURL &, base::Optional<std::basic_string<char> > &, base::Optional<std::basic_string<char> > &, const net::NetworkIsolationKey &> ./../../buildtools/third_party/libc++/trunk/include/memory:3043:28
    #2 0x56355538c1bb in CreateCoepReporter ./../../content/browser/renderer_host/navigation_request.cc:1849:20
    #3 0x56355538c1bb in content::NavigationRequest::CommitNavigation() ./../../content/browser/renderer_host/navigation_request.cc:3454:3
    #4 0x5635553a2a29 in content::NavigationRequest::OnWillProcessResponseChecksComplete(content::NavigationThrottle::ThrottleCheckResult) ./../../content/browser/renderer_host/navigation_request.cc:3274:3
    #5 0x5635553a6c49 in content::NavigationRequest::OnWillProcessResponseProcessed(content::NavigationThrottle::ThrottleCheckResult) ./../../content/browser/renderer_host/navigation_request.cc:4254:3
    #6 0x5635553a5d32 in content::NavigationRequest::OnNavigationEventProcessed(content::NavigationThrottleRunner::Event, content::NavigationThrottle::ThrottleCheckResult) ./../../content/browser/renderer_host/navigation_request.cc:4146:7
    #7 0x5635553c76c4 in InformDelegate ./../../content/browser/renderer_host/navigation_throttle_runner.cc:214:14
    #8 0x5635553c76c4 in content::NavigationThrottleRunner::ProcessInternal() ./../../content/browser/renderer_host/navigation_throttle_runner.cc:203:3
    #9 0x56355ca582c3 in LookalikeUrlNavigationThrottle::PerformChecksDeferred(std::__1::vector<DomainInfo, std::__1::allocator<DomainInfo> > const&) ./../../chrome/browser/lookalikes/lookalike_url_navigation_throttle.cc:190:5
    #10 0x56355ca5adf9 in Invoke<void (LookalikeUrlNavigationThrottle::*)(const std::vector<DomainInfo> &), base::WeakPtr<LookalikeUrlNavigationThrottle>, const std::vector<DomainInfo> &> ./../../base/bind_internal.h:498:12
    #11 0x56355ca5adf9 in MakeItSo<void (LookalikeUrlNavigationThrottle::*)(const std::vector<DomainInfo> &), base::WeakPtr<LookalikeUrlNavigationThrottle>, const std::vector<DomainInfo> &> ./../../base/bind_internal.h:657:5
    #12 0x56355ca5adf9 in RunImpl<void (LookalikeUrlNavigationThrottle::*)(const std::vector<DomainInfo> &), std::tuple<base::WeakPtr<LookalikeUrlNavigationThrottle> >, 0> ./../../base/bind_internal.h:710:12
    #13 0x56355ca5adf9 in base::internal::Invoker<base::internal::BindState<void (LookalikeUrlNavigationThrottle::*)(std::__1::vector<DomainInfo, std::__1::allocator<DomainInfo> > const&), base::WeakPtr<LookalikeUrlNavigationThrottle> >, void (std::__1::vector<DomainInfo, std::__1::allocator<DomainInfo> > const&)>::RunOnce(base::internal::BindStateBase*, std::__1::vector<DomainInfo, std::__1::allocator<DomainInfo> > const&) ./../../base/bind_internal.h:679:12
    #14 0x56355ca5e304 in Run ./../../base/callback.h:101:12
    #15 0x56355ca5e304 in LookalikeUrlService::OnUpdateEngagedSitesCompleted(std::__1::vector<DomainInfo, std::__1::allocator<DomainInfo> >) ./../../chrome/browser/lookalikes/lookalike_url_service.cc:176:25
    #16 0x56355ca5f2c7 in Invoke<void (LookalikeUrlService::*)(std::vector<DomainInfo>), base::WeakPtr<LookalikeUrlService>, std::vector<DomainInfo> > ./../../base/bind_internal.h:498:12
    #17 0x56355ca5f2c7 in void base::internal::InvokeHelper<true, void>::MakeItSo<void (LookalikeUrlService::*)(std::__1::vector<DomainInfo, std::__1::allocator<DomainInfo> >), base::WeakPtr<LookalikeUrlService>, std::__1::vector<DomainInfo, std::__1::allocator<DomainInfo> > >(void (LookalikeUrlService::*&&)(std::__1::vector<DomainInfo, std::__1::allocator<DomainInfo> >), base::WeakPtr<LookalikeUrlService>&&, std::__1::vector<DomainInfo, std::__1::allocator<DomainInfo> >&&) ./../../base/bind_internal.h:657:5
    #18 0x56355ca5fa45 in Run ./../../base/callback.h:101:12
    #19 0x56355ca5fa45 in void base::internal::ReplyAdapter<std::__1::vector<DomainInfo, std::__1::allocator<DomainInfo> >, std::__1::vector<DomainInfo, std::__1::allocator<DomainInfo> > >(base::OnceCallback<void (std::__1::vector<DomainInfo, std::__1::allocator<DomainInfo> >)>, std::__1::unique_ptr<std::__1::vector<DomainInfo, std::__1::allocator<DomainInfo> >, std::__1::default_delete<std::__1::vector<DomainInfo, std::__1::allocator<DomainInfo> > > >*) ./../../base/post_task_and_reply_with_result_internal.h:30:23
    #20 0x56355ca5ff36 in Invoke<void (*)(base::OnceCallback<void (std::vector<DomainInfo>)>, std::unique_ptr<std::vector<DomainInfo> > *), base::OnceCallback<void (std::vector<DomainInfo>)>, std::unique_ptr<std::vector<DomainInfo> > *> ./../../base/bind_internal.h:393:12
    #21 0x56355ca5ff36 in MakeItSo<void (*)(base::OnceCallback<void (std::vector<DomainInfo>)>, std::unique_ptr<std::vector<DomainInfo> > *), base::OnceCallback<void (std::vector<DomainInfo>)>, std::unique_ptr<std::vector<DomainInfo> > *> ./../../base/bind_internal.h:637:12
    #22 0x56355ca5ff36 in RunImpl<void (*)(base::OnceCallback<void (std::vector<DomainInfo>)>, std::unique_ptr<std::vector<DomainInfo> > *), std::tuple<base::OnceCallback<void (std::vector<DomainInfo>)>, base::internal::OwnedWrapper<std::unique_ptr<std::vector<DomainInfo> > > >, 0, 1> ./../../base/bind_internal.h:710:12
    #23 0x56355ca5ff36 in base::internal::Invoker<base::internal::BindState<void (*)(base::OnceCallback<void (std::__1::vector<DomainInfo, std::__1::allocator<DomainInfo> >)>, std::__1::unique_ptr<std::__1::vector<DomainInfo, std::__1::allocator<DomainInfo> >, std::__1::default_delete<std::__1::vector<DomainInfo, std::__1::allocator<DomainInfo> > > >*), base::OnceCallback<void (std::__1::vector<DomainInfo, std::__1::allocator<DomainInfo> >)>, base::internal::OwnedWrapper<std::__1::unique_ptr<std::__1::vector<DomainInfo, std::__1::allocator<DomainInfo> >, std::__1::default_delete<std::__1::vector<DomainInfo, std::__1::allocator<DomainInfo> > > >, std::__1::default_delete<std::__1::unique_ptr<std::__1::vector<DomainInfo, std::__1::allocator<DomainInfo> >, std::__1::default_delete<std::__1::vector<DomainInfo, std::__1::allocator<DomainInfo> > > > > > >, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:679:12
    #24 0x56355bf0670e in Run ./../../base/callback.h:101:12
    #25 0x56355bf0670e in base::(anonymous namespace)::PostTaskAndReplyRelay::RunReply(base::(anonymous namespace)::PostTaskAndReplyRelay) ./../../base/threading/post_task_and_reply_impl.cc:115:29
    #26 0x56355bf06964 in Invoke<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay> ./../../base/bind_internal.h:393:12
    #27 0x56355bf06964 in MakeItSo<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay> ./../../base/bind_internal.h:637:12
    #28 0x56355bf06964 in RunImpl<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay), std::tuple<base::(anonymous namespace)::PostTaskAndReplyRelay>, 0> ./../../base/bind_internal.h:710:12
    #29 0x56355bf06964 in base::internal::Invoker<base::internal::BindState<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:679:12
    #30 0x56355be76d63 in Run ./../../base/callback.h:101:12
    #31 0x56355be76d63 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:163:33
    #32 0x56355beb6c87 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:351:25
    #33 0x56355beb6440 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:264:36
    #34 0x56355bd753e0 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_glib.cc:404:48
    #35 0x56355beb851c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:460:12
    #36 0x56355bdfd4dd in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:133:14
    #37 0x56355c9364dd in ChromeBrowserMainParts::MainMessageLoopRun(int*) ./../../chrome/browser/chrome_browser_main.cc:1741:15
    #38 0x56355479b55c in content::BrowserMainLoop::RunMainMessageLoopParts() ./../../content/browser/browser_main_loop.cc:970:29
    #39 0x5635547a10d1 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser_main_runner_impl.cc:150:15
    #40 0x563554793a51 in content::BrowserMain(content::MainFunctionParams const&) ./../../content/browser/browser_main.cc:47:28
    #41 0x56355bb4bce3 in RunBrowserProcessMain ./../../content/app/content_main_runner_impl.cc:516:10
    #42 0x56355bb4bce3 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) ./../../content/app/content_main_runner_impl.cc:997:10
    #43 0x56355bb4ae33 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:875:12
    #44 0x56355bb44ad7 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) ./../../content/app/content_main.cc:372:36
    #45 0x56355bb450e8 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:398:10
    #46 0x56354f6cef03 in ChromeMain ./../../chrome/app/chrome_main.cc:141:12
    #47 0x7f697b68c0b2 in __libc_start_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free (/home/pwnexp/Chromium-90.0.4408.0/src/out/release/chrome+0x10c013ed)
Shadow bytes around the buggy address:
  0x0c2a80044710: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a80044720: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2a80044730: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a80044740: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a80044750: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0c2a80044760: fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a80044770: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2a80044780: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a80044790: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a800447a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a800447b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==169889==ABORTING

Did this work before? N/A 

Chrome version: 90.0.4408.0  Channel: n/a
OS Version: 20.04
Flash Version:

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 124 B)
- [cache-ws.js](attachments/cache-ws.js) (text/plain, 20 B)

## Timeline

### [Deleted User] (2021-02-06)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-02-08)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>OriginPolicy]

### yh...@chromium.org (2021-02-09)

> Reporter

Is this reproducible with older binaries?

> asamidoi@

Is this related to your recent change https://crrev.com/c/2650015?

[Monorail components: Blink>Workers]

### yh...@chromium.org (2021-02-09)

[Empty comment from Monorail migration]

### em...@gmail.com (2021-02-09)

It can be reproduced from the latest dev( 90.0.4408.0).

### yh...@chromium.org (2021-02-09)

Yeah, I would like to know if you can reproduce it with older binary than that, because the CL in suspect has been available since 90.0.4408.0.

### yh...@chromium.org (2021-02-09)

https://chromiumdash.appspot.com/commit/15a3b50680c497dd442927fb7033f852b25e0d24

### em...@gmail.com (2021-02-09)

Sorry for my poor english. I mean it  just can  reproduce since 90.0.4408.0. Older versions(Older dev version) will not be reproduced.
90.0.4400.8 Can not repro
90.0.4408.0 repro
90.0.4411.0 repro

### yh...@chromium.org (2021-02-09)

Thank you very much!

### [Deleted User] (2021-02-09)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-02-09)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yh...@chromium.org (2021-02-10)

Resetting milestone information based on the report.

### as...@chromium.org (2021-02-10)

[Empty comment from Monorail migration]

### yh...@chromium.org (2021-02-10)

[Empty comment from Monorail migration]

### as...@chromium.org (2021-02-10)

The issue happens due to the destruction timing between RenderFrameHostImpl and DedicatedWorkerHost. The unique pointer of CrossOriginEmbedderPolicyReporter is stored at RenderFrameHostImpl and it's passed and stored in DedicatedWorkerHost as a raw pointer. When RenderFrameHostImpl is destructed, DedicatedWorkerHost and the raw pointer of CrossOriginEmbedderPolicyReporter in DedicatedWorkerHost should be destructed too, but the destruction of DedicatedWorkerHost is triggered by mojo connection. That leads slightly mismatching destruction timing.

I'm working on this and will fix soon.

### as...@chromium.org (2021-02-12)

[Empty comment from Monorail migration]

### as...@chromium.org (2021-02-19)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3a2af67fabe29fb5ce09b9b47c0450bd62cb2d3e

commit 3a2af67fabe29fb5ce09b9b47c0450bd62cb2d3e
Author: Asami Doi <asamidoi@chromium.org>
Date: Fri Feb 19 19:23:39 2021

Make dedicated worker's COEP reporter

This CL adds worker's COEP reporter and update the raw pointer of
ancestor's COEP reporter to a weak pointer.

Without PlzDedicatedWorker, no behavior changes. Reports are sent to
the ancestor's COEP reporter (same as the current behavior) but it's
not align with the spec. When the ancestor's COEP reporter is used, the
existence of it is checked to make sure the frame is not destructed.

With PlzDedicatedWorker, reports are sent to the creator's COEP reporter
if a worker's script loading fails and sent to the worker's COEP
reporter if fetch inside a worker fails.

Bug: 1175436, 1060837
Change-Id: I2ea6b2d51d381a283b5cc722e4517cfc842967c1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2692088
Commit-Queue: Asami Doi <asamidoi@chromium.org>
Reviewed-by: Matt Falkenhagen <falken@chromium.org>
Reviewed-by: Hiroki Nakagawa <nhiroki@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/heads/master@{#855816}

[modify] https://crrev.com/3a2af67fabe29fb5ce09b9b47c0450bd62cb2d3e/content/browser/net/cross_origin_embedder_policy_reporter.h
[modify] https://crrev.com/3a2af67fabe29fb5ce09b9b47c0450bd62cb2d3e/content/browser/worker_host/dedicated_worker_host_factory_impl.h
[modify] https://crrev.com/3a2af67fabe29fb5ce09b9b47c0450bd62cb2d3e/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/3a2af67fabe29fb5ce09b9b47c0450bd62cb2d3e/content/browser/worker_host/dedicated_worker_host.cc
[modify] https://crrev.com/3a2af67fabe29fb5ce09b9b47c0450bd62cb2d3e/content/browser/worker_host/dedicated_worker_host.h
[modify] https://crrev.com/3a2af67fabe29fb5ce09b9b47c0450bd62cb2d3e/content/browser/worker_host/dedicated_worker_service_impl_unittest.cc
[modify] https://crrev.com/3a2af67fabe29fb5ce09b9b47c0450bd62cb2d3e/content/browser/worker_host/dedicated_worker_host_factory_impl.cc


### as...@chromium.org (2021-02-22)

This should be fixed by the CL at c#18.

### [Deleted User] (2021-02-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-22)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d29947902eb7c221eee970541c85e3681c8816f9

commit d29947902eb7c221eee970541c85e3681c8816f9
Author: Asami Doi <asamidoi@chromium.org>
Date: Wed Feb 24 03:24:35 2021

Revert "Make dedicated worker's COEP reporter"

This reverts commit 3a2af67fabe29fb5ce09b9b47c0450bd62cb2d3e.

Reason for revert: crashes in RenderFrameHostImpl::CreateDedicatedWorkerHostFactory
https://crbug.com/1180505

Original change's description:
> Make dedicated worker's COEP reporter
>
> This CL adds worker's COEP reporter and update the raw pointer of
> ancestor's COEP reporter to a weak pointer.
>
> Without PlzDedicatedWorker, no behavior changes. Reports are sent to
> the ancestor's COEP reporter (same as the current behavior) but it's
> not align with the spec. When the ancestor's COEP reporter is used, the
> existence of it is checked to make sure the frame is not destructed.
>
> With PlzDedicatedWorker, reports are sent to the creator's COEP reporter
> if a worker's script loading fails and sent to the worker's COEP
> reporter if fetch inside a worker fails.
>
> Bug: 1175436, 1060837
> Change-Id: I2ea6b2d51d381a283b5cc722e4517cfc842967c1
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2692088
> Commit-Queue: Asami Doi <asamidoi@chromium.org>
> Reviewed-by: Matt Falkenhagen <falken@chromium.org>
> Reviewed-by: Hiroki Nakagawa <nhiroki@chromium.org>
> Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#855816}

Bug: 1175436
Bug: 1060837
Change-Id: If56ef8f5c5e5230eb34e24a1c0b8f20f75b0dcec
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2716546
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Asami Doi <asamidoi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#857003}

[modify] https://crrev.com/d29947902eb7c221eee970541c85e3681c8816f9/content/browser/net/cross_origin_embedder_policy_reporter.h
[modify] https://crrev.com/d29947902eb7c221eee970541c85e3681c8816f9/content/browser/worker_host/dedicated_worker_host_factory_impl.h
[modify] https://crrev.com/d29947902eb7c221eee970541c85e3681c8816f9/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/d29947902eb7c221eee970541c85e3681c8816f9/content/browser/worker_host/dedicated_worker_host.cc
[modify] https://crrev.com/d29947902eb7c221eee970541c85e3681c8816f9/content/browser/worker_host/dedicated_worker_host.h
[modify] https://crrev.com/d29947902eb7c221eee970541c85e3681c8816f9/content/browser/worker_host/dedicated_worker_service_impl_unittest.cc
[modify] https://crrev.com/d29947902eb7c221eee970541c85e3681c8816f9/content/browser/worker_host/dedicated_worker_host_factory_impl.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d0b30ceb011c5558c81f924810d83c66149be352

commit d0b30ceb011c5558c81f924810d83c66149be352
Author: Asami Doi <asamidoi@chromium.org>
Date: Wed Feb 24 04:56:21 2021

Revert "Make dedicated worker's COEP reporter"

This reverts commit 3a2af67fabe29fb5ce09b9b47c0450bd62cb2d3e.

Reason for revert: crashes in RenderFrameHostImpl::CreateDedicatedWorkerHostFactory
https://crbug.com/1180505

Original change's description:
> Make dedicated worker's COEP reporter
>
> This CL adds worker's COEP reporter and update the raw pointer of
> ancestor's COEP reporter to a weak pointer.
>
> Without PlzDedicatedWorker, no behavior changes. Reports are sent to
> the ancestor's COEP reporter (same as the current behavior) but it's
> not align with the spec. When the ancestor's COEP reporter is used, the
> existence of it is checked to make sure the frame is not destructed.
>
> With PlzDedicatedWorker, reports are sent to the creator's COEP reporter
> if a worker's script loading fails and sent to the worker's COEP
> reporter if fetch inside a worker fails.
>
> Bug: 1175436, 1060837
> Change-Id: I2ea6b2d51d381a283b5cc722e4517cfc842967c1
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2692088
> Commit-Queue: Asami Doi <asamidoi@chromium.org>
> Reviewed-by: Matt Falkenhagen <falken@chromium.org>
> Reviewed-by: Hiroki Nakagawa <nhiroki@chromium.org>
> Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#855816}

(cherry picked from commit d29947902eb7c221eee970541c85e3681c8816f9)

Bug: 1175436
Bug: 1060837
Change-Id: If56ef8f5c5e5230eb34e24a1c0b8f20f75b0dcec
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2716546
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Asami Doi <asamidoi@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#857003}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2717523
Reviewed-by: Srinivas Sista <srinivassista@chromium.org>
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/4427@{#3}
Cr-Branched-From: ce035c6c6238688247130a9b35fbb8e26a1b256c-refs/heads/master@{#856944}

[modify] https://crrev.com/d0b30ceb011c5558c81f924810d83c66149be352/content/browser/net/cross_origin_embedder_policy_reporter.h
[modify] https://crrev.com/d0b30ceb011c5558c81f924810d83c66149be352/content/browser/worker_host/dedicated_worker_host_factory_impl.h
[modify] https://crrev.com/d0b30ceb011c5558c81f924810d83c66149be352/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/d0b30ceb011c5558c81f924810d83c66149be352/content/browser/worker_host/dedicated_worker_host.cc
[modify] https://crrev.com/d0b30ceb011c5558c81f924810d83c66149be352/content/browser/worker_host/dedicated_worker_host.h
[modify] https://crrev.com/d0b30ceb011c5558c81f924810d83c66149be352/content/browser/worker_host/dedicated_worker_service_impl_unittest.cc
[modify] https://crrev.com/d0b30ceb011c5558c81f924810d83c66149be352/content/browser/worker_host/dedicated_worker_host_factory_impl.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/dcbff358f4d675c8012ba5a439306de56f7a3012

commit dcbff358f4d675c8012ba5a439306de56f7a3012
Author: Asami Doi <asamidoi@chromium.org>
Date: Wed Feb 24 06:00:59 2021

Revert "Make dedicated worker's COEP reporter"

This reverts commit 3a2af67fabe29fb5ce09b9b47c0450bd62cb2d3e.

Reason for revert: crashes in RenderFrameHostImpl::CreateDedicatedWorkerHostFactory
https://crbug.com/1180505

Original change's description:
> Make dedicated worker's COEP reporter
>
> This CL adds worker's COEP reporter and update the raw pointer of
> ancestor's COEP reporter to a weak pointer.
>
> Without PlzDedicatedWorker, no behavior changes. Reports are sent to
> the ancestor's COEP reporter (same as the current behavior) but it's
> not align with the spec. When the ancestor's COEP reporter is used, the
> existence of it is checked to make sure the frame is not destructed.
>
> With PlzDedicatedWorker, reports are sent to the creator's COEP reporter
> if a worker's script loading fails and sent to the worker's COEP
> reporter if fetch inside a worker fails.
>
> Bug: 1175436, 1060837
> Change-Id: I2ea6b2d51d381a283b5cc722e4517cfc842967c1
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2692088
> Commit-Queue: Asami Doi <asamidoi@chromium.org>
> Reviewed-by: Matt Falkenhagen <falken@chromium.org>
> Reviewed-by: Hiroki Nakagawa <nhiroki@chromium.org>
> Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#855816}

(cherry picked from commit d29947902eb7c221eee970541c85e3681c8816f9)

Bug: 1175436
Bug: 1060837
Change-Id: If56ef8f5c5e5230eb34e24a1c0b8f20f75b0dcec
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2716546
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Asami Doi <asamidoi@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#857003}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2717211
Reviewed-by: Krishna Govind <govind@chromium.org>
Cr-Commit-Position: refs/branch-heads/4426@{#5}
Cr-Branched-From: f849068ee3219ab607bed944dd4cc768c032c675-refs/heads/master@{#856488}

[modify] https://crrev.com/dcbff358f4d675c8012ba5a439306de56f7a3012/content/browser/net/cross_origin_embedder_policy_reporter.h
[modify] https://crrev.com/dcbff358f4d675c8012ba5a439306de56f7a3012/content/browser/worker_host/dedicated_worker_host_factory_impl.h
[modify] https://crrev.com/dcbff358f4d675c8012ba5a439306de56f7a3012/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/dcbff358f4d675c8012ba5a439306de56f7a3012/content/browser/worker_host/dedicated_worker_host.cc
[modify] https://crrev.com/dcbff358f4d675c8012ba5a439306de56f7a3012/content/browser/worker_host/dedicated_worker_host.h
[modify] https://crrev.com/dcbff358f4d675c8012ba5a439306de56f7a3012/content/browser/worker_host/dedicated_worker_service_impl_unittest.cc
[modify] https://crrev.com/dcbff358f4d675c8012ba5a439306de56f7a3012/content/browser/worker_host/dedicated_worker_host_factory_impl.cc


### ad...@google.com (2021-02-26)

Setting Security_Impact per https://crbug.com/chromium/1175436#c8.

### ad...@google.com (2021-03-03)

Looks to me like this has been reverted and not yet fixed...

### ad...@google.com (2021-03-03)

Assuming this now affects beta.

### as...@chromium.org (2021-03-04)

This is fixed because the original problematic CL was also reverted.

https://chromium-review.googlesource.com/c/chromium/src/+/2650015
This CL caused the UAF issue but it was reverted here: https://chromium-review.googlesource.com/c/chromium/src/+/2717382

### am...@google.com (2021-03-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-10)

Congratulations! The VRP Panel has decided to award you $15,000 for this report. Thanks for your efforts and nice work! 

### am...@google.com (2021-03-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1175436?no_tracker_redirect=1

[Multiple monorail components: Blink>SecurityFeature>OriginPolicy, Blink>Workers]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054711)*
