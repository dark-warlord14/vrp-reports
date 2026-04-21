# uaf in WebRTC_Network

| Field | Value |
|-------|-------|
| **Issue ID** | [40052879](https://issues.chromium.org/issues/40052879) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Linux |
| **Reporter** | ne...@gmail.com |
| **Assignee** | hb...@chromium.org |
| **Created** | 2020-07-17 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36

Steps to reproduce the problem:
1.
2.
Chromium 86.0.4185.0
Chromium 86.0.4206.0
1 node node-server.js
2 google-chrome --enable-experimental-web-platform-features --user-dir=/tmp/nonexist http://127.0.0.1:8000/crash/poc.html

I found that depending on the performance of the machine, the reproduction may be unstable. 
If it can't be reproduced, try to adjust the variable "duration" in poc.html.I haven't thought of a better way yet.

What is the expected behavior?

What went wrong?
==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x60d001822ed0 at pc 0x564b130dad82 bp 0x7f3c9bcb1150 sp 0x7f3c9bcb1148
READ of size 8 at 0x60d001822ed0 thread T15 (WebRTC_Network)
==1==WARNING: invalid path to external symbolizer!
==1==WARNING: Failed to use and restart external symbolizer!
    #0 0x564b130dad81 in blink::FilteringNetworkManager::CheckPermission() ./../../third_party/blink/renderer/platform/p2p/filtering_network_manager.cc:116:22
    #1 0x564b155e2798 in blink::IceTransportAdapterImpl::IceTransportAdapterImpl(blink::IceTransportAdapter::Delegate*, std::__1::unique_ptr<cricket::PortAllocator, std::__1::default_delete<cricket::PortAllocator> >, std::__1::unique_ptr<webrtc::AsyncResolverFactory, std::__1::default_delete<webrtc::AsyncResolverFactory> >) ./../../third_party/blink/renderer/modules/peerconnection/adapters/ice_transport_adapter_impl.cc:29:20
    #2 0x564b15570a8e in make_unique<blink::IceTransportAdapterImpl, blink::IceTransportAdapter::Delegate *&, std::__1::unique_ptr<cricket::PortAllocator, std::__1::default_delete<cricket::PortAllocator> >, std::__1::unique_ptr<webrtc::AsyncResolverFactory, std::__1::default_delete<webrtc::AsyncResolverFactory> > > ./../../buildtools/third_party/libc++/trunk/include/memory:3043:32
    #3 0x564b15570a8e in blink::(anonymous namespace)::DefaultIceTransportAdapterCrossThreadFactory::ConstructOnWorkerThread(blink::IceTransportAdapter::Delegate*) ./../../third_party/blink/renderer/modules/peerconnection/rtc_ice_transport.cc:100:12
    #4 0x564b155b970c in blink::IceTransportHost::Initialize(std::__1::unique_ptr<blink::IceTransportAdapterCrossThreadFactory, std::__1::default_delete<blink::IceTransportAdapterCrossThreadFactory> >) ./../../third_party/blink/renderer/modules/peerconnection/adapters/ice_transport_host.cc:37:33
    #5 0x564b155bf6c3 in Invoke<void (blink::IceTransportHost::*)(std::__1::unique_ptr<blink::IceTransportAdapterCrossThreadFactory, std::__1::default_delete<blink::IceTransportAdapterCrossThreadFactory> >), blink::IceTransportHost *, std::__1::unique_ptr<blink::IceTransportAdapterCrossThreadFactory, std::__1::default_delete<blink::IceTransportAdapterCrossThreadFactory> > > ./../../base/bind_internal.h:498:12
    #6 0x564b155bf6c3 in MakeItSo<void (blink::IceTransportHost::*)(std::__1::unique_ptr<blink::IceTransportAdapterCrossThreadFactory, std::__1::default_delete<blink::IceTransportAdapterCrossThreadFactory> >), blink::IceTransportHost *, std::__1::unique_ptr<blink::IceTransportAdapterCrossThreadFactory, std::__1::default_delete<blink::IceTransportAdapterCrossThreadFactory> > > ./../../base/bind_internal.h:637:12
    #7 0x564b155bf6c3 in RunImpl<void (blink::IceTransportHost::*)(std::__1::unique_ptr<blink::IceTransportAdapterCrossThreadFactory, std::__1::default_delete<blink::IceTransportAdapterCrossThreadFactory> >), std::__1::tuple<WTF::CrossThreadUnretainedWrapper<blink::IceTransportHost>, WTF::PassedWrapper<std::__1::unique_ptr<blink::IceTransportAdapterCrossThreadFactory, std::__1::default_delete<blink::IceTransportAdapterCrossThreadFactory> > > >, 0, 1> ./../../base/bind_internal.h:710:12
    #8 0x564b155bf6c3 in base::internal::Invoker<base::internal::BindState<void (blink::IceTransportHost::*)(std::__1::unique_ptr<blink::IceTransportAdapterCrossThreadFactory, std::__1::default_delete<blink::IceTransportAdapterCrossThreadFactory> >), WTF::CrossThreadUnretainedWrapper<blink::IceTransportHost>, WTF::PassedWrapper<std::__1::unique_ptr<blink::IceTransportAdapterCrossThreadFactory, std::__1::default_delete<blink::IceTransportAdapterCrossThreadFactory> > > >, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:679:12
    #9 0x564b0413a123 in Run ./../../base/callback.h:99:12
    #10 0x564b0413a123 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:142:33
    #11 0x564b04175399 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:333:23
    #12 0x564b04174ca8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:253:36
    #13 0x564b0406f0a0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39:55
    #14 0x564b04176619 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:452:12
    #15 0x564b040e9676 in base::RunLoop::Run() ./../../base/run_loop.cc:124:14
    #16 0x564b041cd217 in base::Thread::ThreadMain() ./../../base/threading/thread.cc:382:3
    #17 0x564b0424d72d in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:81:13
    #18 0x7f3cc275a6da in start_thread /build/glibc-2ORdQG/glibc-2.27/nptl/pthread_create.c:463:0

0x60d001822ed0 is located 0 bytes inside of 136-byte region [0x60d001822ed0,0x60d001822f58)
freed by thread T0 (chrome) here:
    #0 0x564af923070d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160:3
    #1 0x564b13c4e2df in operator() ./../../buildtools/third_party/libc++/trunk/include/memory:2378:5
    #2 0x564b13c4e2df in reset ./../../buildtools/third_party/libc++/trunk/include/memory:2633:7
    #3 0x564b13c4e2df in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/memory:2587:19
    #4 0x564b13c4e2df in content::RenderFrameImpl::~RenderFrameImpl() ./../../content/renderer/render_frame_impl.cc:1930:1
    #5 0x564b13c4f53c in content::RenderFrameImpl::~RenderFrameImpl() ./../../content/renderer/render_frame_impl.cc:1907:37
    #6 0x564b13c832a0 in content::RenderFrameImpl::FrameDetached(blink::WebLocalFrameClient::DetachType) ./../../content/renderer/render_frame_impl.cc:4061:3
    #7 0x564b10b1fbf3 in blink::LocalFrameClientImpl::Detached(blink::FrameDetachType) ./../../third_party/blink/renderer/core/exported/local_frame_client_impl.cc:470:11
    #8 0x564b107aa98d in blink::Frame::Detach(blink::FrameDetachType) ./../../third_party/blink/renderer/core/frame/frame.cc:118:12
    #9 0x564b0efbe6a8 in blink::ChildFrameDisconnector::DisconnectCollectedFrameOwners() ./../../third_party/blink/renderer/core/dom/child_frame_disconnector.cc:59:14
    #10 0x564b0efbdb01 in blink::ChildFrameDisconnector::Disconnect(blink::ChildFrameDisconnector::DisconnectPolicy) ./../../third_party/blink/renderer/core/dom/child_frame_disconnector.cc:32:3
    #11 0x564b10807d7c in blink::LocalFrame::DetachChildren() ./../../third_party/blink/renderer/core/frame/local_frame.cc:643:39
    #12 0x564b11ea2fd6 in blink::FrameLoader::DetachDocument(blink::SecurityOrigin*, base::Optional<blink::Document::UnloadEventTiming>*) ./../../third_party/blink/renderer/core/loader/frame_loader.cc:1113:11
    #13 0x564b11ea0534 in blink::FrameLoader::CommitNavigation(std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> >, std::__1::unique_ptr<blink::WebDocumentLoader::ExtraData, std::__1::default_delete<blink::WebDocumentLoader::ExtraData> >, blink::CommitReason) ./../../third_party/blink/renderer/core/loader/frame_loader.cc:1010:10
    #14 0x564b10b115c5 in blink::WebLocalFrameImpl::CommitNavigation(std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> >, std::__1::unique_ptr<blink::WebDocumentLoader::ExtraData, std::__1::default_delete<blink::WebDocumentLoader::ExtraData> >) ./../../third_party/blink/renderer/core/frame/web_local_frame_impl.cc:2132:24
    #15 0x564b13c70769 in content::RenderFrameImpl::CommitNavigationWithParams(mojo::StructPtr<content::mojom::CommonNavigationParams>, mojo::StructPtr<content::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, base::Optional<std::__1::vector<mojo::StructPtr<content::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<content::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::__1::unique_ptr<content::DocumentState, std::__1::default_delete<content::DocumentState> >, std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> >) ./../../content/renderer/render_frame_impl.cc:3320:11
    #16 0x564b13cd00e0 in void base::internal::FunctorTraits<void (content::RenderFrameImpl::*)(mojo::StructPtr<content::mojom::CommonNavigationParams>, mojo::StructPtr<content::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, base::Optional<std::__1::vector<mojo::StructPtr<content::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<content::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::__1::unique_ptr<content::DocumentState, std::__1::default_delete<content::DocumentState> >, std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> >), void>::Invoke<void (content::RenderFrameImpl::*)(mojo::StructPtr<content::mojom::CommonNavigationParams>, mojo::StructPtr<content::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, base::Optional<std::__1::vector<mojo::StructPtr<content::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<content::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::__1::unique_ptr<content::DocumentState, std::__1::default_delete<content::DocumentState> >, std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> >), base::WeakPtr<content::RenderFrameImpl>, mojo::StructPtr<content::mojom::CommonNavigationParams>, mojo::StructPtr<content::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, base::Optional<std::__1::vector<mojo::StructPtr<content::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<content::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::__1::unique_ptr<content::DocumentState, std::__1::default_delete<content::DocumentState> >, std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> > >(void (content::RenderFrameImpl::*)(mojo::StructPtr<content::mojom::CommonNavigationParams>, mojo::StructPtr<content::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, base::Optional<std::__1::vector<mojo::StructPtr<content::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<content::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::__1::unique_ptr<content::DocumentState, std::__1::default_delete<content::DocumentState> >, std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> >), base::WeakPtr<content::RenderFrameImpl>&&, mojo::StructPtr<content::mojom::CommonNavigationParams>&&, mojo::StructPtr<content::mojom::CommitNavigationParams>&&, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >&&, base::Optional<std::__1::vector<mojo::StructPtr<content::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<content::mojom::TransferrableURLLoader> > > >&&, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>&&, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>&&, mojo::PendingRemote<network::mojom::URLLoaderFactory>&&, std::__1::unique_ptr<content::DocumentState, std::__1::default_delete<content::DocumentState> >&&, std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> >&&) ./../../base/bind_internal.h:498:12
    #17 0x564b13ccfc0f in MakeItSo<void (content::RenderFrameImpl::*)(mojo::StructPtr<content::mojom::CommonNavigationParams>, mojo::StructPtr<content::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, base::Optional<std::__1::vector<mojo::StructPtr<content::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<content::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::__1::unique_ptr<content::DocumentState, std::__1::default_delete<content::DocumentState> >, std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> >), base::WeakPtr<content::RenderFrameImpl>, mojo::StructPtr<content::mojom::CommonNavigationParams>, mojo::StructPtr<content::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, base::Optional<std::__1::vector<mojo::StructPtr<content::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<content::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::__1::unique_ptr<content::DocumentState, std::__1::default_delete<content::DocumentState> >, std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> > > ./../../base/bind_internal.h:657:5
    #18 0x564b13ccfc0f in RunImpl<void (content::RenderFrameImpl::*)(mojo::StructPtr<content::mojom::CommonNavigationParams>, mojo::StructPtr<content::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, base::Optional<std::__1::vector<mojo::StructPtr<content::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<content::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::__1::unique_ptr<content::DocumentState, std::__1::default_delete<content::DocumentState> >, std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> >), std::__1::tuple<base::WeakPtr<content::RenderFrameImpl>, mojo::StructPtr<content::mojom::CommonNavigationParams>, mojo::StructPtr<content::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, base::Optional<std::__1::vector<mojo::StructPtr<content::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<content::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::__1::unique_ptr<content::DocumentState, std::__1::default_delete<content::DocumentState> > >, 0, 1, 2, 3, 4, 5, 6, 7, 8> ./../../base/bind_internal.h:710:12
    #19 0x564b13ccfc0f in base::internal::Invoker<base::internal::BindState<void (content::RenderFrameImpl::*)(mojo::StructPtr<content::mojom::CommonNavigationParams>, mojo::StructPtr<content::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, base::Optional<std::__1::vector<mojo::StructPtr<content::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<content::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::__1::unique_ptr<content::DocumentState, std::__1::default_delete<content::DocumentState> >, std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> >), base::WeakPtr<content::RenderFrameImpl>, mojo::StructPtr<content::mojom::CommonNavigationParams>, mojo::StructPtr<content::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, base::Optional<std::__1::vector<mojo::StructPtr<content::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<content::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::__1::unique_ptr<content::DocumentState, std::__1::default_delete<content::DocumentState> > >, void (std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> >)>::RunOnce(base::internal::BindStateBase*, std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> >&&) ./../../base/bind_internal.h:679:12
    #20 0x564b13c6d910 in Run ./../../base/callback.h:99:12
    #21 0x564b13c6d910 in content::RenderFrameImpl::CommitNavigation(mojo::StructPtr<content::mojom::CommonNavigationParams>, mojo::StructPtr<content::mojom::CommitNavigationParams>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, mojo::StructPtr<network::mojom::URLLoaderClientEndpoints>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, base::Optional<std::__1::vector<mojo::StructPtr<content::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<content::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, base::UnguessableToken const&, base::OnceCallback<void (std::__1::unique_ptr<FrameHostMsg_DidCommitProvisionalLoad_Params, std::__1::default_delete<FrameHostMsg_DidCommitProvisionalLoad_Params> >, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>)>) ./../../content/renderer/render_frame_impl.cc:3188:33
    #22 0x564b13ea0eb3 in content::NavigationClient::CommitNavigation(mojo::StructPtr<content::mojom::CommonNavigationParams>, mojo::StructPtr<content::mojom::CommitNavigationParams>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, mojo::StructPtr<network::mojom::URLLoaderClientEndpoints>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, base::Optional<std::__1::vector<mojo::StructPtr<content::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<content::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, base::UnguessableToken const&, base::OnceCallback<void (std::__1::unique_ptr<FrameHostMsg_DidCommitProvisionalLoad_Params, std::__1::default_delete<FrameHostMsg_DidCommitProvisionalLoad_Params> >, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>)>) ./../../content/renderer/navigation_client.cc:38:18
    #23 0x564afbd15b64 in content::mojom::NavigationClientStubDispatch::AcceptWithResponder(content::mojom::NavigationClient*, mojo::Message*, std::__1::unique_ptr<mojo::MessageReceiverWithStatus, std::__1::default_delete<mojo::MessageReceiverWithStatus> >) ./gen/content/common/navigation_client.mojom.cc:688:13
    #24 0x564b13ea22d8 in content::mojom::NavigationClientStub<mojo::RawPtrImplRefTraits<content::mojom::NavigationClient> >::AcceptWithResponder(mojo::Message*, std::__1::unique_ptr<mojo::MessageReceiverWithStatus, std::__1::default_delete<mojo::MessageReceiverWithStatus> >) ./gen/content/common/navigation_client.mojom.h:159:12
    #25 0x564b046d8ac0 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:528:56
    #26 0x564b046e5712 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:41:19
    #27 0x564b06547682 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnProxyThread(mojo::Message) ./../../ipc/ipc_mojo_bootstrap.cc:934:24
    #28 0x564b065408a8 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind_internal.h:498:12
    #29 0x564b065408a8 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind_internal.h:637:12
    #30 0x564b065408a8 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::__1::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0, 1> ./../../base/bind_internal.h:710:12
    #31 0x564b065408a8 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:679:12
    #32 0x564b0413a123 in Run ./../../base/callback.h:99:12
    #33 0x564b0413a123 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:142:33
    #34 0x564b04175399 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:333:23
    #35 0x564b04174ca8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:253:36
    #36 0x564b0406f0a0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39:55
    #37 0x564b04176619 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:452:12
    #38 0x564b040e9676 in base::RunLoop::Run() ./../../base/run_loop.cc:124:14
    #39 0x564b159b23ae in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:230:16

previously allocated by thread T0 (chrome) here:
    #0 0x564af922fead in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x564b13cba8e1 in content::RenderFrameImpl::GetMediaPermission() ./../../content/renderer/render_frame_impl.cc:6176:40
    #2 0x564b159a7b8c in content::RendererBlinkPlatformImpl::GetWebRTCMediaPermission(blink::WebLocalFrame*) ./../../content/renderer/renderer_blink_platform_impl.cc:591:40
    #3 0x564b130a6614 in blink::PeerConnectionDependencyFactory::CreatePortAllocator(blink::WebLocalFrame*) ./../../third_party/blink/renderer/modules/peerconnection/peer_connection_dependency_factory.cc:436:39
    #4 0x564b155705b3 in blink::(anonymous namespace)::DefaultIceTransportAdapterCrossThreadFactory::InitializeOnMainThread(blink::LocalFrame&) ./../../third_party/blink/renderer/modules/peerconnection/rtc_ice_transport.cc:90:47
    #5 0x564b155bbf1b in blink::IceTransportProxy::IceTransportProxy(blink::LocalFrame&, scoped_refptr<base::SingleThreadTaskRunner>, scoped_refptr<base::SingleThreadTaskRunner>, blink::IceTransportProxy::Delegate*, std::__1::unique_ptr<blink::IceTransportAdapterCrossThreadFactory, std::__1::default_delete<blink::IceTransportAdapterCrossThreadFactory> >) ./../../third_party/blink/renderer/modules/peerconnection/adapters/ice_transport_proxy.cc:40:20
    #6 0x564b155678d1 in make_unique<blink::IceTransportProxy, blink::LocalFrame &, scoped_refptr<base::SingleThreadTaskRunner>, scoped_refptr<base::SingleThreadTaskRunner>, blink::RTCIceTransport *, std::__1::unique_ptr<blink::IceTransportAdapterCrossThreadFactory, std::__1::default_delete<blink::IceTransportAdapterCrossThreadFactory> > > ./../../buildtools/third_party/libc++/trunk/include/memory:3043:32
    #7 0x564b155678d1 in blink::RTCIceTransport::RTCIceTransport(blink::ExecutionContext*, scoped_refptr<base::SingleThreadTaskRunner>, scoped_refptr<base::SingleThreadTaskRunner>, std::__1::unique_ptr<blink::IceTransportAdapterCrossThreadFactory, std::__1::default_delete<blink::IceTransportAdapterCrossThreadFactory> >, blink::RTCPeerConnection*) ./../../third_party/blink/renderer/modules/peerconnection/rtc_ice_transport.cc:169:12
    #8 0x564b15566aed in RTCIceTransport ./../../third_party/blink/renderer/modules/peerconnection/rtc_ice_transport.cc:181:7
    #9 0x564b15566aed in Call<blink::ExecutionContext *&, scoped_refptr<base::SingleThreadTaskRunner>, scoped_refptr<base::SingleThreadTaskRunner>, std::__1::unique_ptr<blink::(anonymous namespace)::DefaultIceTransportAdapterCrossThreadFactory, std::__1::default_delete<blink::(anonymous namespace)::DefaultIceTransportAdapterCrossThreadFactory> > > ./../../third_party/blink/renderer/platform/heap/heap.h:554:32
    #10 0x564b15566aed in MakeGarbageCollected<blink::RTCIceTransport, blink::ExecutionContext *&, scoped_refptr<base::SingleThreadTaskRunner>, scoped_refptr<base::SingleThreadTaskRunner>, std::__1::unique_ptr<blink::(anonymous namespace)::DefaultIceTransportAdapterCrossThreadFactory, std::__1::default_delete<blink::(anonymous namespace)::DefaultIceTransportAdapterCrossThreadFactory> > > ./../../third_party/blink/renderer/platform/heap/heap.h:594:15
    #11 0x564b15566aed in blink::RTCIceTransport::Create(blink::ExecutionContext*) ./../../third_party/blink/renderer/modules/peerconnection/rtc_ice_transport.cc:120:10
    #12 0x564b1557dbc0 in Constructor ./gen/third_party/blink/renderer/bindings/modules/v8/v8_rtc_ice_transport.cc:339:27
    #13 0x564b1557dbc0 in blink::rtc_ice_transport_v8_internal::ConstructorCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_rtc_ice_transport.cc:362:3
    #14 0x564affe0a7bf in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:158:3
    #15 0x564affe073f0 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:111:36
    #16 0x564affe05cd8 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:137:5
    #17 0x564b01eadc57 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit ??:0:0
    #18 0x564b01e3d744 in Builtins_JSBuiltinsConstructStub ??:0:0
    #19 0x564b01f39e4a in Builtins_ConstructHandler ??:0:0
    #20 0x564b01e41994 in Builtins_InterpreterEntryTrampoline ??:0:0
    #21 0x564b01e41994 in Builtins_InterpreterEntryTrampoline ??:0:0
    #22 0x564b01e41994 in Builtins_InterpreterEntryTrampoline ??:0:0
    #23 0x564b01e41994 in Builtins_InterpreterEntryTrampoline ??:0:0
    #24 0x564b01e41994 in Builtins_InterpreterEntryTrampoline ??:0:0
    #25 0x564b01e41994 in Builtins_InterpreterEntryTrampoline ??:0:0
    #26 0x564b01e38c5e in Builtins_ArgumentsAdaptorTrampoline ??:0:0
    #27 0x564b01e41994 in Builtins_InterpreterEntryTrampoline ??:0:0
    #28 0x564b01e38c5e in Builtins_ArgumentsAdaptorTrampoline ??:0:0
    #29 0x564b01ef75d0 in Builtins_PromiseConstructor ??:0:0
    #30 0x564b01e3d76f in Builtins_JSBuiltinsConstructStub ??:0:0
    #31 0x564b01f39e4a in Builtins_ConstructHandler ??:0:0
    #32 0x564b01e41994 in Builtins_InterpreterEntryTrampoline ??:0:0
    #33 0x564b01e38c5e in Builtins_ArgumentsAdaptorTrampoline ??:0:0
    #34 0x564b01ef9297 in Builtins_PromiseFulfillReactionJob ??:0:0

Thread T15 (WebRTC_Network) created by T0 (chrome) here:
    #0 0x564af91f17ea in pthread_create /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:214:3
    #1 0x564b0424c94a in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, base::PlatformThreadHandle*, base::ThreadPriority) ./../../base/threading/platform_thread_posix.cc:120:13
    #2 0x564b041cc0f6 in base::Thread::StartWithOptions(base::Thread::Options const&) ./../../base/threading/thread.cc:186:15
    #3 0x564b041cba97 in base::Thread::Start() ./../../base/threading/thread.cc:139:10
    #4 0x564b130a1ac1 in blink::PeerConnectionDependencyFactory::CreatePeerConnectionFactory() ./../../third_party/blink/renderer/modules/peerconnection/peer_connection_dependency_factory.cc:198:3
    #5 0x564b130a1659 in blink::PeerConnectionDependencyFactory::GetPcFactory() ./../../third_party/blink/renderer/modules/peerconnection/peer_connection_dependency_factory.cc:152:5
    #6 0x564b15566997 in blink::RTCIceTransport::Create(blink::ExecutionContext*) ./../../third_party/blink/renderer/modules/peerconnection/rtc_ice_transport.cc:116:51
    #7 0x564b1557dbc0 in Constructor ./gen/third_party/blink/renderer/bindings/modules/v8/v8_rtc_ice_transport.cc:339:27
    #8 0x564b1557dbc0 in blink::rtc_ice_transport_v8_internal::ConstructorCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_rtc_ice_transport.cc:362:3
    #9 0x564affe0a7bf in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:158:3
    #10 0x564affe073f0 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:111:36
    #11 0x564affe05cd8 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:137:5
    #12 0x564b01eadc57 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit ??:0:0
    #13 0x564b01e3d744 in Builtins_JSBuiltinsConstructStub ??:0:0
    #14 0x564b01f39e4a in Builtins_ConstructHandler ??:0:0
    #15 0x564b01e41994 in Builtins_InterpreterEntryTrampoline ??:0:0
    #16 0x564b01e41994 in Builtins_InterpreterEntryTrampoline ??:0:0
    #17 0x564b01e41994 in Builtins_InterpreterEntryTrampoline ??:0:0
    #18 0x564b01e41994 in Builtins_InterpreterEntryTrampoline ??:0:0
    #19 0x564b01e41994 in Builtins_InterpreterEntryTrampoline ??:0:0
    #20 0x564b01e41994 in Builtins_InterpreterEntryTrampoline ??:0:0
    #21 0x564b01e38c5e in Builtins_ArgumentsAdaptorTrampoline ??:0:0
    #22 0x564b01e41994 in Builtins_InterpreterEntryTrampoline ??:0:0
    #23 0x564b01e38c5e in Builtins_ArgumentsAdaptorTrampoline ??:0:0
    #24 0x564b01ef75d0 in Builtins_PromiseConstructor ??:0:0
    #25 0x564b01e3d76f in Builtins_JSBuiltinsConstructStub ??:0:0
    #26 0x564b01f39e4a in Builtins_ConstructHandler ??:0:0
    #27 0x564b01e41994 in Builtins_InterpreterEntryTrampoline ??:0:0
    #28 0x564b01e38c5e in Builtins_ArgumentsAdaptorTrampoline ??:0:0
    #29 0x564b01ef9297 in Builtins_PromiseFulfillReactionJob ??:0:0
    #30 0x564b01e61cb6 in Builtins_RunMicrotasks ??:0:0
    #31 0x564b01e3f457 in Builtins_JSRunMicrotasksEntry ??:0:0
    #32 0x564b000a1796 in Call ./../../v8/src/execution/simulator.h:142:12
    #33 0x564b000a1796 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:382:33
    #34 0x564b000a517e in v8::internal::(anonymous namespace)::InvokeWithTryCatch(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:427:20
    #35 0x564b000a5619 in v8::internal::Execution::TryRunMicrotasks(v8::internal::Isolate*, v8::internal::MicrotaskQueue*, v8::internal::MaybeHandle<v8::internal::Object>*) ./../../v8/src/execution/execution.cc:504:10
    #36 0x564b00121fb5 in v8::internal::MicrotaskQueue::RunMicrotasks(v8::internal::Isolate*) ./../../v8/src/execution/microtask-queue.cc:165:22
    #37 0x564b00121956 in v8::internal::MicrotaskQueue::PerformCheckpoint(v8::Isolate*) ./../../v8/src/execution/microtask-queue.cc:117:5
    #38 0x564b0e9be7a1 in blink::V8ScriptRunner::RunCompiledScript(v8::Isolate*, v8::Local<v8::Script>, blink::ExecutionContext*) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:359:3
    #39 0x564b10056b1c in blink::ScriptController::ExecuteScriptAndReturnValue(v8::Local<v8::Context>, blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&) ./../../third_party/blink/renderer/bindings/core/v8/script_controller.cc:154:20
    #40 0x564b10059c77 in blink::ScriptController::EvaluateScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&, blink::ScriptController::ExecuteScriptPolicy) ./../../third_party/blink/renderer/bindings/core/v8/script_controller.cc:395:33
    #41 0x564b1005a6be in blink::ScriptController::ExecuteScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&) ./../../third_party/blink/renderer/bindings/core/v8/script_controller.cc:360:3
    #42 0x564b1246e469 in blink::PendingScript::ExecuteScriptBlockInternal(blink::Script*, blink::ScriptElementBase*, bool, bool, bool, base::TimeTicks, bool) ./../../third_party/blink/renderer/core/script/pending_script.cc:264:13
    #43 0x564b1246dd40 in blink::PendingScript::ExecuteScriptBlock(blink::KURL const&) ./../../third_party/blink/renderer/core/script/pending_script.cc:170:3
    #44 0x564b12474076 in blink::ScriptLoader::PrepareScript(WTF::TextPosition const&, blink::ScriptLoader::LegacyTypeSupport) ./../../third_party/blink/renderer/core/script/script_loader.cc:913:9
    #45 0x564b1241f3fb in blink::HTMLParserScriptRunner::ProcessScriptElementInternal(blink::Element*, WTF::TextPosition const&) ./../../third_party/blink/renderer/core/script/html_parser_script_runner.cc:597:20
    #46 0x564b1241ef98 in blink::HTMLParserScriptRunner::ProcessScriptElement(blink::Element*, WTF::TextPosition const&) ./../../third_party/blink/renderer/core/script/html_parser_script_runner.cc:333:3
    #47 0x564b110ba820 in blink::HTMLDocumentParser::RunScriptsForPausedTreeBuilder() ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:510:21
    #48 0x564b110be42a in blink::HTMLDocumentParser::ProcessTokenizedChunkFromBackgroundParser(std::__1::unique_ptr<blink::HTMLDocumentParser::TokenizedChunk, std::__1::default_delete<blink::HTMLDocumentParser::TokenizedChunk> >, bool*) ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:751:9
    #49 0x564b110ba0bd in blink::HTMLDocumentParser::PumpPendingSpeculations() ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:811:34
    #50 0x564b110c9634 in blink::HTMLDocumentParser::ResumeParsingAfterPause() ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:1358:7
    #51 0x564b110ca479 in blink::HTMLDocumentParser::NotifyScriptLoaded(blink::PendingScript*) ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:1417:5
    #52 0x564b0413a123 in Run ./../../base/callback.h:99:12
    #53 0x564b0413a123 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:142:33
    #54 0x564b04175399 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:333:23
    #55 0x564b04174ca8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:253:36
    #56 0x564b0406f0a0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39:55
    #57 0x564b04176619 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:452:12
    #58 0x564b040e9676 in base::RunLoop::Run() ./../../base/run_loop.cc:124:14
    #59 0x564b159b23ae in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:230:16
    #60 0x564b02fca88f in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:502:14
    #61 0x564b02fcddb4 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:882:10
    #62 0x564b031721c6 in service_manager::Main(service_manager::MainParams const&) ./../../services/service_manager/embedder/main.cc:453:29
    #63 0x564b02fc8d16 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:19:10
    #64 0x564af92330c4 in ChromeMain ./../../chrome/app/chrome_main.cc:117:12
    #65 0x7f3cbb27ab96 in __libc_start_main /build/glibc-2ORdQG/glibc-2.27/csu/../csu/libc-start.c:310:0

SUMMARY: AddressSanitizer: heap-use-after-free (/home/cowboy/chromium/src/out/chrome_asan_shared/chrome+0x233ebd81)
Shadow bytes around the buggy address:
  0x0c1a802fc580: fd fd fd fd fa fa fa fa fa fa fa fa fd fd fd fd
  0x0c1a802fc590: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa
  0x0c1a802fc5a0: fa fa fa fa fa fa fd fd fd fd fd fd fd fd fd fd
  0x0c1a802fc5b0: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x0c1a802fc5c0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0c1a802fc5d0: fd fd fa fa fa fa fa fa fa fa[fd]fd fd fd fd fd
  0x0c1a802fc5e0: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x0c1a802fc5f0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c1a802fc600: fd fd fd fd fd fd fa fa fa fa fa fa fa fa fd fd
  0x0c1a802fc610: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa
  0x0c1a802fc620: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1==ABORTING

Did this work before? N/A 

Chrome version: Chromium 86.0.4206.0  Channel: n/a
OS Version: 18.04
Flash Version:

## Attachments

- [poc.zip](attachments/poc.zip) (application/octet-stream, 34.2 KB)

## Timeline

### me...@chromium.org (2020-07-17)

I was unable to reproduce this.

guidou@ tommi@ or steveanton@ could you please take a look at this?

[Monorail components: Blink>WebRTC]

### st...@chromium.org (2020-07-17)

Looks like a race between the main thread tearing down and the WebRTC network thread initializing an object asynchronously.

I think the problem is that even though the FilteringNetworkManager has been like this for ages the RTCPeerConnection always constructed it synchronized with the main thread (via main thread invoking onto the signaling thread which invoked onto the network thread).

Note that this is probably only exposed via the standalone RTCIceTransport which is behind a flag.

### aj...@google.com (2020-07-21)

Assigning to steveanton@, feel free to suggest someone else who can work on fixing this security bug.

Marking as Security_Impact-Stable as this might have been this way for ages.

### [Deleted User] (2020-07-23)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@google.com (2020-07-23)

Ping? Any progress?

I'm marking as None based on https://crbug.com/chromium/1106907#c2.

### to...@chromium.org (2020-07-23)

Adding more folks to cc - Is the "--enable-experimental-web-platform-features" flag necessary to reproduce?

### ht...@chromium.org (2020-07-24)

Adding Taylor to thread, because he knows his way around threading stuff.


### de...@chromium.org (2020-07-24)

Note that it's specifically media_permission_dispatcher_ which is accessed after freeing.

Unfortunately this is all chromium code that's new to me so I wouldn't be much help. Steve's analysis seems correct, and clearly the destruction order needs to be changed somewhere but I don't even know how this is working without the standalone RTCIceTransport. Clearly the PeerConnections are being destroyed somehow on tab closure (through RTCPeerConnection::Dispose?) but I don't really know how that works.

### st...@chromium.org (2020-07-24)

Note specifically the issue is with accessing the media_permission_dispatcher_ during PortAllocator *construction* without being synchronized with the main thread. Once the request has been made, the callback is captured with a WeakPtr which prevents UAF later.

The PeerConnection happens to do all its initialization synchronized because of liberal use of rtc::Thread::Invoke. The main thread will dispatch and block waiting for the initialization to happen on the signaling thread, which in turn will dispatch and block waiting for initialization to happen on the network thread. Note that this means the PortAllocator calls media_permission_dispatcher_ before the main thread event loop is resumed, which is why this UAF doesn't happen with RTCPeerConnection.

Therefore, I believe this only happens with the standalone RTCIceTransport which was designed to do asynchronous initialization. The main thread event loop is resumed before the initialization happens on the network thread which allows for the media_permission_dispatcher_ to be destroyed in the mean time.

Probably the easiest (if somewhat unsatisfying) fix is to block the main thread while the RTCIceTransport is initializing on the network thread. A more comprehensive fix would be to do the media_permission_dispatcher_ query on the main thread when the RTCIceTransport is constructed from JS, then post the results to the network thread later.

Not sure what the priority of fixing this is as it appears to only impact a flag-guarded feature. As far as I know there are no current plans to launch the standalone RTCIceTransport more broadly.

### to...@chromium.org (2020-07-24)

hbos - any chance you could take a look?

I wonder if having the delegate there is the right thing since the network thread seems likely to outlive it. Possibly freeing the delegate reference and subsequently deleting the object asynchronously on the network thread could be an option.

### st...@chromium.org (2020-07-25)

[Empty comment from Monorail migration]

### ti...@chromium.org (2020-07-26)

Is problem in construction of PortAllocator or in the initialization? If it's during construction, then it can be moved from network thread to the signaling one (is it main thread from Chromium terms?), then there won't be any thread hops, which make it's simpler.

### ti...@chromium.org (2020-07-26)

I meant PortAllocator creation inside RTCPeerConnection, not inside standalone RTCIceTransport

### st...@chromium.org (2020-07-28)

The problem is in the initialization of the P2PPortAllocator / FilteringNetworkManager. There's currently an assumption in FilteringNetworkManager that Initialize() is run in the same main thread task that provides the media::MediaPermission pointer.

That works today for RTCPeerConnection since the P2PPortAllocator Initialize() method (which in turn initializes FilteringNetworkManager) is currently Invoked() from the signaling thread (which is in turn Invoked() from the main thread).

But we need to fix that if we want to stop doing the network thread initialization synchronously with the main thread / signaling thread.

### hb...@chromium.org (2020-07-30)

Is there a quick fix for that? I'll be OOO until the end of august but let me know if you want me to take a look when I'm back

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-02-24)

hbos/steveanton: Any update here?

### te...@chromium.org (2021-03-08)

[Empty comment from Monorail migration]

### hb...@chromium.org (2021-03-09)

Given that P2P QUIC was removed in M88, perhaps we should just remove the RTCIceTransport constructor where this UAF can happen? I don't believe there is any reason to create a standalone transport anymore

### te...@chromium.org (2021-03-09)

[Empty comment from Monorail migration]

### te...@chromium.org (2021-03-09)

[Empty comment from Monorail migration]

### hb...@chromium.org (2021-03-09)

[Empty comment from Monorail migration]

### hb...@chromium.org (2021-03-09)

Removing the constructor here: https://chromium-review.googlesource.com/c/chromium/src/+/2744038

### gi...@appspot.gserviceaccount.com (2021-03-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2b6a7ed586f52814f6e3ac478e19ca05c418078d

commit 2b6a7ed586f52814f6e3ac478e19ca05c418078d
Author: Henrik Boström <hbos@chromium.org>
Date: Wed Mar 10 09:34:48 2021

Remove standalone RTCIceTransport constructor.

The only supported use case for constructing an RTCIceTransport as a
standalone object, i.e. that is not associated and constructed by an
RTCPeerConnection, is for use with P2P QUIC. However P2P QUIC with
ICE was an experimental feature that was removed in M88.

As part of further cleanup we're now also removing the standalone
constructor. See also https://crbug.com/1106907 for more reasons why we
don't want to continue to maintain this code.

Bug: chromium:1106907
Change-Id: Ide384ed4db6ca53ef71e82022b868dded052a17d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2744038
Commit-Queue: Henrik Boström <hbos@chromium.org>
Reviewed-by: Tommi <tommi@chromium.org>
Reviewed-by: Steve Anton <steveanton@chromium.org>
Cr-Commit-Position: refs/heads/master@{#861491}

[modify] https://crrev.com/2b6a7ed586f52814f6e3ac478e19ca05c418078d/third_party/blink/renderer/modules/peerconnection/rtc_ice_transport.cc
[modify] https://crrev.com/2b6a7ed586f52814f6e3ac478e19ca05c418078d/third_party/blink/renderer/modules/peerconnection/rtc_ice_transport.h
[modify] https://crrev.com/2b6a7ed586f52814f6e3ac478e19ca05c418078d/third_party/blink/renderer/modules/peerconnection/rtc_ice_transport.idl
[add] https://crrev.com/2b6a7ed586f52814f6e3ac478e19ca05c418078d/third_party/blink/web_tests/external/wpt/webrtc-ice/RTCIceTransport-extension.https-expected.txt
[modify] https://crrev.com/2b6a7ed586f52814f6e3ac478e19ca05c418078d/third_party/blink/web_tests/external/wpt/webrtc/idlharness.https.window-expected.txt
[modify] https://crrev.com/2b6a7ed586f52814f6e3ac478e19ca05c418078d/third_party/blink/web_tests/virtual/webrtc-wpt-plan-b/external/wpt/webrtc/idlharness.https.window-expected.txt


### hb...@chromium.org (2021-03-10)

There we go, fixed by code deletion. It's in M91.

### [Deleted User] (2021-03-10)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-10)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-18)

Congratulations! The VRP Panel has decided to award you $5000 for this report. Thank you for your submission and nice work! 

### am...@google.com (2021-03-18)

[Empty comment from Monorail migration]

### hb...@chromium.org (2021-03-22)

Let's consider backmerging this to M90 at least

### [Deleted User] (2021-03-22)

This bug requires manual review: M90's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: govind@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### hb...@chromium.org (2021-03-22)

1. Yes, we're backmerging a security fix.
2. https://chromium.googlesource.com/chromium/src/+/2b6a7ed586f52814f6e3ac478e19ca05c418078d
3. Yes.
4. I want to backmerge to M90 beta.
5. It's a security fix.
6. No.
7. N/A


### sr...@google.com (2021-03-22)

Merge approved for M90 branch:4430

### gi...@appspot.gserviceaccount.com (2021-03-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c1c8dbde4ebbaa5b391e2b920b7935ad378d9ba2

commit c1c8dbde4ebbaa5b391e2b920b7935ad378d9ba2
Author: Henrik Boström <hbos@chromium.org>
Date: Tue Mar 23 11:35:36 2021

Remove standalone RTCIceTransport constructor.

The only supported use case for constructing an RTCIceTransport as a
standalone object, i.e. that is not associated and constructed by an
RTCPeerConnection, is for use with P2P QUIC. However P2P QUIC with
ICE was an experimental feature that was removed in M88.

As part of further cleanup we're now also removing the standalone
constructor. See also https://crbug.com/1106907 for more reasons why we
don't want to continue to maintain this code.

(cherry picked from commit 2b6a7ed586f52814f6e3ac478e19ca05c418078d)

Bug: chromium:1106907
Change-Id: Ide384ed4db6ca53ef71e82022b868dded052a17d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2744038
Commit-Queue: Henrik Boström <hbos@chromium.org>
Reviewed-by: Tommi <tommi@chromium.org>
Reviewed-by: Steve Anton <steveanton@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#861491}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2780255
Auto-Submit: Henrik Boström <hbos@chromium.org>
Reviewed-by: Markus Handell <handellm@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#678}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/c1c8dbde4ebbaa5b391e2b920b7935ad378d9ba2/third_party/blink/renderer/modules/peerconnection/rtc_ice_transport.cc
[modify] https://crrev.com/c1c8dbde4ebbaa5b391e2b920b7935ad378d9ba2/third_party/blink/renderer/modules/peerconnection/rtc_ice_transport.h
[modify] https://crrev.com/c1c8dbde4ebbaa5b391e2b920b7935ad378d9ba2/third_party/blink/renderer/modules/peerconnection/rtc_ice_transport.idl
[add] https://crrev.com/c1c8dbde4ebbaa5b391e2b920b7935ad378d9ba2/third_party/blink/web_tests/external/wpt/webrtc-ice/RTCIceTransport-extension.https-expected.txt
[add] https://crrev.com/c1c8dbde4ebbaa5b391e2b920b7935ad378d9ba2/third_party/blink/web_tests/external/wpt/webrtc/RTCIceTransport-extension.https-expected.txt
[modify] https://crrev.com/c1c8dbde4ebbaa5b391e2b920b7935ad378d9ba2/third_party/blink/web_tests/external/wpt/webrtc/idlharness.https.window-expected.txt
[modify] https://crrev.com/c1c8dbde4ebbaa5b391e2b920b7935ad378d9ba2/third_party/blink/web_tests/virtual/webrtc-wpt-plan-b/external/wpt/webrtc/idlharness.https.window-expected.txt


### [Deleted User] (2021-06-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-06-29)

This issue was migrated from crbug.com/chromium/1106907?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052879)*
