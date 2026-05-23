# UAF in content::RenderFrameImpl::CommitSameDocumentNavigation(with puppeteer)

| Field | Value |
|-------|-------|
| **Issue ID** | [333024273](https://issues.chromium.org/issues/333024273) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2024-04-05 |
| **Bounty** | Confirmed (amount unknown) |

## Description

tested os:

- ubuntu 22.04
  tested browser:
  Chromium 125.0.6399.0
  Chromium 116.0.5805.0

repro steps:

1. install node,puppeteer-core
2. node ./test.js chrome\_path poc\_path 2>&1 |grep -E 'heap-use'
   (the test.js will open 6 browser instances to ensure that the crash occurs stably)
3. The UAF will trigger immediately.

```
==556841==ERROR: AddressSanitizer: heap-use-after-free on address 0x50e00010e5f0 at pc 0x600d64255f66 bp 0x7fff03ec81f0 sp 0x7fff03ec81e8
READ of size 8 at 0x50e00010e5f0 thread T0 (chrome)
    #0 0x600d64255f65 in get ./../../third_party/libc++/src/include/__memory/unique_ptr.h:260:101
    #1 0x600d64255f65 in navigation_state ./../../content/renderer/document_state.h:64:66
    #2 0x600d64255f65 in content::RenderFrameImpl::CommitSameDocumentNavigation(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, base::OnceCallback<void (blink::mojom::CommitResult)>) ./../../content/renderer/render_frame_impl.cc:3312:39
    #3 0x600d405c711b in content::mojom::FrameStubDispatch::AcceptWithResponder(content::mojom::Frame*, mojo::Message*, std::__Cr::unique_ptr<mojo::MessageReceiverWithStatus, std::__Cr::default_delete<mojo::MessageReceiverWithStatus>>) ./gen/content/common/frame.mojom.cc:2990:13
    #4 0x600d4e8c8884 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:975:56
    #5 0x600d4e8e4987 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #6 0x600d4e8cd885 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:706:20
    #7 0x600d4f6989cf in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ./../../ipc/ipc_mojo_bootstrap.cc:1181:24
    #8 0x600d4f69a0b3 in Invoke<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> ./../../base/functional/bind_internal.h:738:12
    #9 0x600d4f69a0b3 in MakeItSo<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> > ./../../base/functional/bind_internal.h:930:12
    #10 0x600d4f69a0b3 in RunImpl<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, 0UL, 1UL, 2UL> ./../../base/functional/bind_internal.h:1067:14
    #11 0x600d4f69a0b3 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:980:12
    #12 0x600d4d2062b4 in Run ./../../base/functional/callback.h:156:12
    #13 0x600d4d2062b4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:203:34
    #14 0x600d4d267a1f in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:11)> ./../../base/task/common/task_annotator.h:90:5
    #15 0x600d4d267a1f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #16 0x600d4d266a09 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:40
    #17 0x600d4d2687da in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #18 0x600d4d0ffc9c in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #19 0x600d4d26951f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:641:12
    #20 0x600d4d198c5f in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #21 0x600d644a045a in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:367:16
    #22 0x600d4a97dd28 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:676:14
    #23 0x600d4a97f251 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:780:12
    #24 0x600d4a981c8f in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1146:10
    #25 0x600d4a97c080 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:328:36
    #26 0x600d4a97c6fb in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:341:10
    #27 0x600d4bdda3bf in HeadlessChildMain ./../../headless/app/headless_shell.cc:195:12
    #28 0x600d4bdda3bf in headless::HeadlessShellMain(content::ContentMainParams) ./../../headless/app/headless_shell.cc:256:5
    #29 0x600d3b442da5 in ChromeMain ./../../chrome/app/chrome_main.cc:178:14
    #30 0x75b66c629d8f in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16

0x50e00010e5f0 is located 144 bytes inside of 152-byte region [0x50e00010e560,0x50e00010e5f8)
freed by thread T0 (chrome) here:
    #0 0x600d3b440f6d in operator delete(void*) _asan_rtl_:3
    #1 0x600d5af40828 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:68:5
    #2 0x600d5af40828 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:279:7
    #3 0x600d5af40828 in blink::DocumentLoader::DetachFromFrame(bool) ./../../third_party/blink/renderer/core/loader/document_loader.cc:1795:15
    #4 0x600d5afbe55d in DetachDocumentLoader ./../../third_party/blink/renderer/core/loader/frame_loader.cc:504:11
    #5 0x600d5afbe55d in blink::FrameLoader::DetachDocument() ./../../third_party/blink/renderer/core/loader/frame_loader.cc:1286:3
    #6 0x600d5afbc8cb in blink::FrameLoader::CommitNavigation(std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>, std::__Cr::unique_ptr<blink::WebDocumentLoader::ExtraData, std::__Cr::default_delete<blink::WebDocumentLoader::ExtraData>>, blink::CommitReason) ./../../third_party/blink/renderer/core/loader/frame_loader.cc:1105:10
    #7 0x600d59d4b3a7 in blink::WebLocalFrameImpl::CommitNavigation(std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>, std::__Cr::unique_ptr<blink::WebDocumentLoader::ExtraData, std::__Cr::default_delete<blink::WebDocumentLoader::ExtraData>>) ./../../third_party/blink/renderer/core/frame/web_local_frame_impl.cc:2678:24
    #8 0x600d6424e3ac in content::RenderFrameImpl::CommitNavigationWithParams(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>) ./../../content/renderer/render_frame_impl.cc:2999:11
    #9 0x600d6429ffc1 in void base::internal::DecayedFunctorTraits<void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>), base::WeakPtr<content::RenderFrameImpl>&&, mojo::StructPtr<blink::mojom::CommonNavigationParams>&&, mojo::StructPtr<blink::mojom::CommitNavigationParams>&&, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>&&, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>&&, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>&&, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>&&, mojo::PendingRemote<network::mojom::URLLoaderFactory>&&, mojo::PendingRemote<network::mojom::URLLoaderFactory>&&, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>&&, mojo::PendingRemote<blink::mojom::CodeCacheHost>&&, mojo::PendingRemote<blink::mojom::CodeCacheHost>&&, mojo::StructPtr<content::mojom::CookieManagerInfo>&&, mojo::StructPtr<content::mojom::StorageInfo>&&, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>&&>::Invoke<void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>), base::WeakPtr<content::RenderFrameImpl> const&, mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>>(void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>), base::WeakPtr<content::RenderFrameImpl> const&, mojo::StructPtr<blink::mojom::CommonNavigationParams>&&, mojo::StructPtr<blink::mojom::CommitNavigationParams>&&, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>&&, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>&&, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>&&, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>&&, mojo::PendingRemote<network::mojom::URLLoaderFactory>&&, mojo::PendingRemote<network::mojom::URLLoaderFactory>&&, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>&&, mojo::PendingRemote<blink::mojom::CodeCacheHost>&&, mojo::PendingRemote<blink::mojom::CodeCacheHost>&&, mojo::StructPtr<content::mojom::CookieManagerInfo>&&, mojo::StructPtr<content::mojom::StorageInfo>&&, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>&&, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>&&) ./../../base/functional/bind_internal.h:738:12
    #10 0x600d6429fa6f in MakeItSo<void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle> >, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState> >, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams> >), std::__Cr::tuple<base::WeakPtr<content::RenderFrameImpl>, mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle> >, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState> > >, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams> > > ./../../base/functional/bind_internal.h:954:5
    #11 0x600d6429fa6f in RunImpl<void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle> >, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState> >, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams> >), std::__Cr::tuple<base::WeakPtr<content::RenderFrameImpl>, mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle> >, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState> > >, 0UL, 1UL, 2UL, 3UL, 4UL, 5UL, 6UL, 7UL, 8UL, 9UL, 10UL, 11UL, 12UL, 13UL, 14UL> ./../../base/functional/bind_internal.h:1067:14
    #12 0x600d6429fa6f in base::internal::Invoker<base::internal::FunctorTraits<void (content::RenderFrameImpl::*&&)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>), base::WeakPtr<content::RenderFrameImpl>&&, mojo::StructPtr<blink::mojom::CommonNavigationParams>&&, mojo::StructPtr<blink::mojom::CommitNavigationParams>&&, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>&&, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>&&, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>&&, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>&&, mojo::PendingRemote<network::mojom::URLLoaderFactory>&&, mojo::PendingRemote<network::mojom::URLLoaderFactory>&&, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>&&, mojo::PendingRemote<blink::mojom::CodeCacheHost>&&, mojo::PendingRemote<blink::mojom::CodeCacheHost>&&, mojo::StructPtr<content::mojom::CookieManagerInfo>&&, mojo::StructPtr<content::mojom::StorageInfo>&&, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>&&>, base::internal::BindState<true, true, false, void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>), base::WeakPtr<content::RenderFrameImpl>, mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>>, void (std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>)>::RunOnce(base::internal::BindStateBase*, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>&&) ./../../base/functional/bind_internal.h:980:12
    #13 0x600d6424f48d in base::OnceCallback<void (std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>)>::Run(std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>) && ./../../base/functional/callback.h:156:12
    #14 0x600d6424a342 in content::RenderFrameImpl::CommitNavigation(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, mojo::StructPtr<network::mojom::URLLoaderClientEndpoints>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, base::TokenType<blink::DocumentTokenTypeMarker> const&, base::UnguessableToken const&, base::Uuid const&, std::__Cr::optional<std::__Cr::vector<blink::ParsedPermissionsPolicyDeclaration, std::__Cr::allocator<blink::ParsedPermissionsPolicyDeclaration>>> const&, mojo::StructPtr<blink::mojom::PolicyContainer>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, base::OnceCallback<void (mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>)>) ./../../content/renderer/render_frame_impl.cc:2863:33
    #15 0x600d643a9f32 in content::NavigationClient::CommitNavigation(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, mojo::StructPtr<network::mojom::URLLoaderClientEndpoints>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, base::TokenType<blink::DocumentTokenTypeMarker> const&, base::UnguessableToken const&, base::Uuid const&, std::__Cr::optional<std::__Cr::vector<blink::ParsedPermissionsPolicyDeclaration, std::__Cr::allocator<blink::ParsedPermissionsPolicyDeclaration>>> const&, mojo::StructPtr<blink::mojom::PolicyContainer>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, base::OnceCallback<void (mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>)>) ./../../content/renderer/navigation_client.cc:64:18
    #16 0x600d4061c42a in content::mojom::NavigationClientStubDispatch::AcceptWithResponder(content::mojom::NavigationClient*, mojo::Message*, std::__Cr::unique_ptr<mojo::MessageReceiverWithStatus, std::__Cr::default_delete<mojo::MessageReceiverWithStatus>>) ./gen/content/common/navigation_client.mojom.cc:1519:13
    #17 0x600d4e8c8884 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:975:56
    #18 0x600d4e8e4987 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #19 0x600d4e8cd885 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:706:20
    #20 0x600d4f6989cf in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ./../../ipc/ipc_mojo_bootstrap.cc:1181:24
    #21 0x600d4f69a0b3 in Invoke<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> ./../../base/functional/bind_internal.h:738:12
    #22 0x600d4f69a0b3 in MakeItSo<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> > ./../../base/functional/bind_internal.h:930:12
    #23 0x600d4f69a0b3 in RunImpl<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, 0UL, 1UL, 2UL> ./../../base/functional/bind_internal.h:1067:14
    #24 0x600d4f69a0b3 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:980:12
    #25 0x600d4d2062b4 in Run ./../../base/functional/callback.h:156:12
    #26 0x600d4d2062b4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:203:34
    #27 0x600d4d267a1f in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:11)> ./../../base/task/common/task_annotator.h:90:5
    #28 0x600d4d267a1f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #29 0x600d4d266a09 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:40
    #30 0x600d4d2687da in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #31 0x600d4d0ffc9c in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #32 0x600d4d26962e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:638:12
    #33 0x600d4d198c5f in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #34 0x600d6445de93 in content::(anonymous namespace)::NestedMessageLoopRunnerImpl::Run() ./../../content/child/blink_platform_impl.cc:88:14
    #35 0x600d5d1d18b1 in blink::ClientMessageLoopAdapter::RunLoop(blink::WebLocalFrameImpl*) ./../../third_party/blink/renderer/core/exported/web_dev_tools_agent_impl.cc:271:20
    #36 0x600d5d1cdfd4 in RunForPageWait ./../../third_party/blink/renderer/core/exported/web_dev_tools_agent_impl.cc:205:7
    #37 0x600d5d1cdfd4 in PauseForPageWait ./../../third_party/blink/renderer/core/exported/web_dev_tools_agent_impl.cc:149:18
    #38 0x600d5d1cdfd4 in WaitForDebugger ./../../third_party/blink/renderer/core/exported/web_dev_tools_agent_impl.cc:555:3
    #39 0x600d5d1cdfd4 in blink::WebDevToolsAgentImpl::DidShowNewWindow() ./../../third_party/blink/renderer/core/exported/web_dev_tools_agent_impl.cc:547:3
    #40 0x600d5d2617c4 in blink::WebViewImpl::Show(base::TokenType<blink::LocalFrameTokenTypeMarker> const&, blink::NavigationPolicy, gfx::Rect const&, gfx::Rect const&, bool) ./../../third_party/blink/renderer/core/exported/web_view_impl.cc:3053:33
    #41 0x600d5b1b015a in blink::ChromeClientImpl::Show(blink::LocalFrame&, blink::LocalFrame&, blink::NavigationPolicy, bool) ./../../third_party/blink/renderer/core/page/chrome_client_impl.cc:430:14
    #42 0x600d5b2de546 in blink::CreateNewWindow(blink::LocalFrame&, blink::FrameLoadRequest&, WTF::AtomicString const&) ./../../third_party/blink/renderer/core/page/create_window.cc:377:27

previously allocated by thread T0 (chrome) here:
    #0 0x600d3b44070d in operator new(unsigned long) _asan_rtl_:3
    #1 0x600d6424aee7 in content::(anonymous namespace)::BuildDocumentStateFromParams(blink::mojom::CommonNavigationParams const&, blink::mojom::CommitNavigationParams const&, base::OnceCallback<void (mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>)>, std::__Cr::unique_ptr<content::NavigationClient, std::__Cr::default_delete<content::NavigationClient>>, int, bool) ./../../content/renderer/render_frame_impl.cc:918:49
    #2 0x600d64248bfd in content::RenderFrameImpl::CommitNavigation(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, mojo::StructPtr<network::mojom::URLLoaderClientEndpoints>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, base::TokenType<blink::DocumentTokenTypeMarker> const&, base::UnguessableToken const&, base::Uuid const&, std::__Cr::optional<std::__Cr::vector<blink::ParsedPermissionsPolicyDeclaration, std::__Cr::allocator<blink::ParsedPermissionsPolicyDeclaration>>> const&, mojo::StructPtr<blink::mojom::PolicyContainer>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, base::OnceCallback<void (mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>)>) ./../../content/renderer/render_frame_impl.cc:2727:51
    #3 0x600d643a9f32 in content::NavigationClient::CommitNavigation(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, mojo::StructPtr<network::mojom::URLLoaderClientEndpoints>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, base::TokenType<blink::DocumentTokenTypeMarker> const&, base::UnguessableToken const&, base::Uuid const&, std::__Cr::optional<std::__Cr::vector<blink::ParsedPermissionsPolicyDeclaration, std::__Cr::allocator<blink::ParsedPermissionsPolicyDeclaration>>> const&, mojo::StructPtr<blink::mojom::PolicyContainer>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, base::OnceCallback<void (mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>)>) ./../../content/renderer/navigation_client.cc:64:18
    #4 0x600d4061c42a in content::mojom::NavigationClientStubDispatch::AcceptWithResponder(content::mojom::NavigationClient*, mojo::Message*, std::__Cr::unique_ptr<mojo::MessageReceiverWithStatus, std::__Cr::default_delete<mojo::MessageReceiverWithStatus>>) ./gen/content/common/navigation_client.mojom.cc:1519:13
    #5 0x600d4e8c8884 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:975:56
    #6 0x600d4e8e4987 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #7 0x600d4e8cd885 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:706:20
    #8 0x600d4f6989cf in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ./../../ipc/ipc_mojo_bootstrap.cc:1181:24
    #9 0x600d4f69a0b3 in Invoke<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> ./../../base/functional/bind_internal.h:738:12
    #10 0x600d4f69a0b3 in MakeItSo<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> > ./../../base/functional/bind_internal.h:930:12
    #11 0x600d4f69a0b3 in RunImpl<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, 0UL, 1UL, 2UL> ./../../base/functional/bind_internal.h:1067:14
    #12 0x600d4f69a0b3 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:980:12
    #13 0x600d4d2062b4 in Run ./../../base/functional/callback.h:156:12
    #14 0x600d4d2062b4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:203:34
    #15 0x600d4d267a1f in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:11)> ./../../base/task/common/task_annotator.h:90:5
    #16 0x600d4d267a1f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #17 0x600d4d266a09 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:40
    #18 0x600d4d2687da in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #19 0x600d4d0ffc9c in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #20 0x600d4d26962e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:638:12
    #21 0x600d4d198c5f in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #22 0x600d6445de93 in content::(anonymous namespace)::NestedMessageLoopRunnerImpl::Run() ./../../content/child/blink_platform_impl.cc:88:14
    #23 0x600d5d1d18b1 in blink::ClientMessageLoopAdapter::RunLoop(blink::WebLocalFrameImpl*) ./../../third_party/blink/renderer/core/exported/web_dev_tools_agent_impl.cc:271:20
    #24 0x600d5d1cdfd4 in RunForPageWait ./../../third_party/blink/renderer/core/exported/web_dev_tools_agent_impl.cc:205:7
    #25 0x600d5d1cdfd4 in PauseForPageWait ./../../third_party/blink/renderer/core/exported/web_dev_tools_agent_impl.cc:149:18
    #26 0x600d5d1cdfd4 in WaitForDebugger ./../../third_party/blink/renderer/core/exported/web_dev_tools_agent_impl.cc:555:3
    #27 0x600d5d1cdfd4 in blink::WebDevToolsAgentImpl::DidShowNewWindow() ./../../third_party/blink/renderer/core/exported/web_dev_tools_agent_impl.cc:547:3
    #28 0x600d5d2617c4 in blink::WebViewImpl::Show(base::TokenType<blink::LocalFrameTokenTypeMarker> const&, blink::NavigationPolicy, gfx::Rect const&, gfx::Rect const&, bool) ./../../third_party/blink/renderer/core/exported/web_view_impl.cc:3053:33
    #29 0x600d5b1b015a in blink::ChromeClientImpl::Show(blink::LocalFrame&, blink::LocalFrame&, blink::NavigationPolicy, bool) ./../../third_party/blink/renderer/core/page/chrome_client_impl.cc:430:14
    #30 0x600d5b2de546 in blink::CreateNewWindow(blink::LocalFrame&, blink::FrameLoadRequest&, WTF::AtomicString const&) ./../../third_party/blink/renderer/core/page/create_window.cc:377:27
    #31 0x600d5b30aef1 in blink::FrameTree::FindOrCreateFrameForNavigation(blink::FrameLoadRequest&, WTF::AtomicString const&) const ./../../third_party/blink/renderer/core/page/frame_tree.cc:218:13
    #32 0x600d59a44469 in blink::LocalDOMWindow::open(v8::Isolate*, WTF::String const&, WTF::AtomicString const&, WTF::String const&, blink::ExceptionState&) ./../../third_party/blink/renderer/core/frame/local_dom_window.cc:2265:26
    #33 0x600d5de0355f in blink::(anonymous namespace)::v8_window::OpenOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_window.cc:15495:39
    #34 0x600d442960ce in Builtins_CallApiCallbackGeneric setup-isolate-deserialize.cc:0:0
    #35 0x600d44293d66 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc:0:0
    #36 0x600d44293d66 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc:0:0
    #37 0x600d442d3141 in Builtins_AsyncFunctionAwaitResolveClosure setup-isolate-deserialize.cc:0:0

SUMMARY: AddressSanitizer: heap-use-after-free (/home/pwn11/asan-linux-release/chrome+0x37538f65) (BuildId: 3e128b81aad38c2b)
Shadow bytes around the buggy address:
  0x50e00010e300: 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa fa
  0x50e00010e380: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 00
  0x50e00010e400: 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa
  0x50e00010e480: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x50e00010e500: fd fd fd fd fa fa fa fa fa fa fa fa fd fd fd fd
=>0x50e00010e580: fd fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]fa
  0x50e00010e600: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x50e00010e680: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
  0x50e00010e700: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x50e00010e780: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x50e00010e800: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==556841==ADDITIONAL INFO

==556841==Note: Please include this section with the ASan report.
Task trace:
    #0 0x600d4f68c9a3 in IPC::ChannelAssociatedGroupController::Accept(mojo::Message*) ./../../ipc/ipc_mojo_bootstrap.cc:1120:13


==556841==END OF ADDITIONAL INFO
==556841==ABORTING

```

## Attachments

- [test.js](attachments/test.js) (text/javascript, 1.1 KB)
- [crash.html](attachments/crash.html) (text/html, 1.1 KB)
- [asan.log](attachments/asan.log) (text/plain, 46.5 KB)
- [crash2.html](attachments/crash2.html) (text/html, 968 B)

## Timeline

### ar...@chromium.org (2024-04-08)

Thanks!

**Needs-Feedback**:
I am able to run the reproducer, but it does **not** able to reproduce. Is there anything else that might be relevant?

The StackTrace is still very useful. I see [rakina@chromium.org](mailto:rakina@chromium.org) and @ja...@chromium.org authored and cherry-picked [the commit](https://chromium-review.googlesource.com/c/chromium/src/+/4375397) where this read after free is happening. This is likely relevant.
Could you please take a look and try to reproduce it?

- **severity**: S2 (read after free in the sandbox).
- **Found-In**: Extended-Stable, based on @reporter claims that I wasn't able to verify.

### em...@gmail.com (2024-04-08)

On my machine, the above steps are reproducible stably, and I am not sure about other factors that may affect reproduction.
How about modifying the number of browser instances in test.js and trying again?
for example:
const nums=6;
-->
const nums=Math.floor(Math.random()*10)+1;

### pe...@google.com (2024-04-08)

Thank you for providing more feedback. Adding the requester to the CC list.

### pe...@google.com (2024-04-09)

Setting milestone because of s2 severity.

### pe...@google.com (2024-04-09)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### cr...@chromium.org (2024-04-15)

[Navigation triage]
@japhet, are you able to take a look to try to repro and fix this? Sounds like it's related to your earlier fix for <https://crbug.com/1427449>.

I'll add it to the Available hotlist to remove it from the Untriaged state, but I'll leave the Unconfirmed hotlist until someone is able to repro it. Also CC'ing @rakina per [comment #2](https://issues.chromium.org/issues/333024273#comment2).

### ja...@chromium.org (2024-04-15)

Nested messages loops!

My logic clearly isn't tolerant to DocumentState potentially getting deleted while on the stack. That appears to *only* be possible with a nested message loop running during a same document commit, and a second navigation coming in and clobbering the DocumentState before the nested message loop exits.

I haven't figured out the trick to repro this without puppeteer, but it ought to be possible. I'll keep trying.

### pe...@google.com (2024-04-30)

japhet: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-05-15)

japhet: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### em...@gmail.com (2024-06-07)

The original PoC seems to be unstable in the latest version. I made a simple modification, and using Puppeteer, it reproduces the issue immediately.
tested version:
Chromium 127.0.6526.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1311720.zip)

### ts...@google.com (2024-10-31)

Trying Rakina per C2, might you be able to help chase down this very old bug? Thanks!

### na...@chromium.org (2025-05-23)

[Navigation Triage] rakina@, have you had a chance to take a look at this one? Maybe you can find someone to help with reproducing this to double check that it still is an issue?

### ra...@chromium.org (2026-02-09)

I can't seem to repro this with [#comment11](https://issues.chromium.org/issues/333024273#comment11). But from what I gathered from the stack trace and comments, it looks like this is only possible if we somehow pause a same-document commit via puppeteer (maybe when the navigate event is triggered), then a cross-document commit navigation happens while the same-document commit is paused (wow didn't know this was possible), then the same-document commit continues. The RenderFrameImpl stays the same (same-origin nav without RenderDocument) but the DocumentLoader & DocumentState used by the same-document commit is already deleted. The WeakPtr check for the RenderFrameImpl doesn't protect from the UAF, so we accessed the already deleted DocumentState. I think maybe we should just add another WeakPtr check but for the DocumentState to avoid this.

Let me assign to japhet@ to check if that makes sense :)

### ja...@google.com (2026-02-09)

I think that's more or less correct, rakina@.

On the one hand, a UAF is a UAF, and it should be addressed. OTOH, it's been a couple years and we've only seen evidence that this is possible with a non-standard configruation, so this isn't a practical security issue in the wild.

I think it's worth putting a defensive WeakPtr here if you think that's likely to resolve the problem, but I'm not sure this is worth any effort beyond that.

rakina@: Do you want to prep the CL, or should I?

### dx...@google.com (2026-02-12)

Project: chromium/src  

Branch:  main  

Author:  Nate Chapin [japhet@chromium.org](mailto:japhet@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7562935>

Early-exit in RenderFrameImpl::CommitSameDocumentNavigation when DocumentState gets overwritten

---


Expand for full commit details
```
     
    In non-standard configurations, a nested event loop inside navigation 
    commit can lead to the DocumentState getting clobbered. 
     
    Fixed: 333024273 
    Change-Id: I44983fcca1d867e360c9033c9267e5a7a3a2dcc0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7562935 
    Commit-Queue: Nate Chapin <japhet@chromium.org> 
    Reviewed-by: Rakina Zata Amni <rakina@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1584160}

```

---

Files:

- M `content/renderer/document_state.h`
- M `content/renderer/render_frame_impl.cc`

---

Hash: [8a9374b1a3b3bcb265e05e3193cf91932ac8f277](https://chromiumdash.appspot.com/commit/8a9374b1a3b3bcb265e05e3193cf91932ac8f277)  

Date: Thu Feb 12 19:49:36 2026


---

### sp...@google.com (2026-03-11)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

Never reproduced without Puppeteer

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### ch...@google.com (2026-05-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Never reproduced without Puppeteer
> 
> 
> Note that the fact that this issue is not being rewarded does not mean
> that the product team won't fix the issue. We have filed a bug with the product
> team and they will review your report and decide if a fix is required. We'll
> let you know if the issue was fixed.
> 
> Regards, \
> Google Security Bot
> 
> *How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/333024273)*
