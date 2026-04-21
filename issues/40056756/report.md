# use after free in blink::FrameLoader::DetachDocument

| Field | Value |
|-------|-------|
| **Issue ID** | [40056756](https://issues.chromium.org/issues/40056756) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GarbageCollection, Blink>Internals>WTF, Blink>Loader, UI>Browser>Navigation |
| **Platforms** | Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2021-08-02 |
| **Bounty** | $7,500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36

Steps to reproduce the problem:
Chrome version:
Google Chrome 93.0.4577.8 dev
Chromium 94.0.4596.0
Operating System:
Ubuntu 20.04
1. modify hosts file add 5 fake domain
    sudo vi /etc/hosts
		127.0.0.1       www.localdomain1.com
		127.0.0.1       www.localdomain2.com
		127.0.0.1       www.localdomain3.com
		127.0.0.1       www.localdomain4.com
		127.0.0.1       www.localdomain5.com
	sudo /etc/init.d/networking restart
2. python3.8 -m http.server 8000 

3. /chrome --user-data-dir=/tmp/xx http://localhost:8000/main.html

4. It crashed  about 30 seconds in my local test.

In fact, running crash.html directly can also be reproduced, but it is not stable.

What is the expected behavior?

What went wrong?
==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x6210001e8e90 at pc 0x55e86abe24d6 bp 0x7ffe3a6e82d0 sp 0x7ffe3a6e82c8
READ of size 8 at 0x6210001e8e90 thread T0 (chrome)
==1==WARNING: invalid path to external symbolizer!
==1==WARNING: Failed to use and restart external symbolizer!
    #0 0x55e86abe24d5 in void WTF::Vector<blink::Member<blink::EventTarget>, 0u, blink::HeapAllocator>::AppendSlowCase<blink::UntracedMember<blink::EventTarget> const&>(blink::UntracedMember<blink::EventTarget> const&) ./../../third_party/blink/renderer/platform/heap/impl/member.h:257
    #1 0x55e86abe24d5 in operator blink::EventTarget * ./../../third_party/blink/renderer/platform/heap/impl/member.h:187
    #2 0x55e86abe24d5 in Construct<blink::MemberBase<blink::EventTarget, blink::TracenessMemberConfiguration::kTraced>::AtomicCtorTag, const blink::UntracedMember<blink::EventTarget> &> ./../../third_party/blink/renderer/platform/heap/impl/member.h:509
    #3 0x55e86abe24d5 in ConstructAndNotifyElement<const blink::UntracedMember<blink::EventTarget> &> ./../../third_party/blink/renderer/platform/heap/impl/member.h:519
    #4 0x55e86abe24d5 in AppendSlowCase<const blink::UntracedMember<blink::EventTarget> &> ./../../third_party/blink/renderer/platform/wtf/vector.h:1925
    #5 0x55e86abe24d5 in ?? ??:0
    #6 0x55e86abdfddb in blink::EventHandlerRegistry::DocumentDetached(blink::Document&) ./../../third_party/blink/renderer/platform/wtf/vector.h:1875
    #7 0x55e86abdfddb in DocumentDetached ./../../third_party/blink/renderer/core/frame/event_handler_registry.cc:370
    #8 0x55e86abdfddb in ?? ??:0
    #9 0x55e869d3b889 in blink::Document::Shutdown() ./../../third_party/blink/renderer/core/dom/document.cc:2824
    #10 0x55e869d3b889 in ?? ??:0
    #11 0x55e86bfff90c in blink::FrameLoader::DetachDocument(blink::SecurityOrigin*, absl::optional<blink::Document::UnloadEventTiming>*) ./../../third_party/blink/renderer/core/loader/frame_loader.cc:1158
    #12 0x55e86bfff90c in ?? ??:0
    #13 0x55e86bffe282 in blink::FrameLoader::CommitNavigation(std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> >, std::__1::unique_ptr<blink::WebDocumentLoader::ExtraData, std::__1::default_delete<blink::WebDocumentLoader::ExtraData> >, blink::CommitReason) ./../../third_party/blink/renderer/core/loader/frame_loader.cc:1009
    #14 0x55e86bffe282 in ?? ??:0
    #15 0x55e86e6d7a23 in content::RenderFrameImpl::CommitNavigationWithParams(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, absl::optional<std::__1::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::__1::unique_ptr<content::DocumentState, std::__1::default_delete<content::DocumentState> >, std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> >) ./../../content/renderer/render_frame_impl.cc:2928
    #16 0x55e86e6d7a23 in ?? ??:0
    #17 0x55e86e72ee00 in void base::internal::FunctorTraits<void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, absl::optional<std::__1::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::__1::unique_ptr<content::DocumentState, std::__1::default_delete<content::DocumentState> >, std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> >), void>::Invoke<void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, absl::optional<std::__1::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::__1::unique_ptr<content::DocumentState, std::__1::default_delete<content::DocumentState> >, std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> >), base::WeakPtr<content::RenderFrameImpl>, mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, absl::optional<std::__1::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::__1::unique_ptr<content::DocumentState, std::__1::default_delete<content::DocumentState> >, std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> > >(void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, absl::optional<std::__1::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::__1::unique_ptr<content::DocumentState, std::__1::default_delete<content::DocumentState> >, std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> >), base::WeakPtr<content::RenderFrameImpl>&&, mojo::StructPtr<blink::mojom::CommonNavigationParams>&&, mojo::StructPtr<blink::mojom::CommitNavigationParams>&&, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >&&, absl::optional<std::__1::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >&&, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>&&, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>&&, mojo::PendingRemote<network::mojom::URLLoaderFactory>&&, std::__1::unique_ptr<content::DocumentState, std::__1::default_delete<content::DocumentState> >&&, std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> >&&) ./../../base/bind_internal.h:509
    #18 0x55e86e72ee00 in ?? ??:0
    #19 0x55e86e72e993 in base::internal::Invoker<base::internal::BindState<void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, absl::optional<std::__1::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::__1::unique_ptr<content::DocumentState, std::__1::default_delete<content::DocumentState> >, std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> >), base::WeakPtr<content::RenderFrameImpl>, mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, absl::optional<std::__1::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::__1::unique_ptr<content::DocumentState, std::__1::default_delete<content::DocumentState> > >, void (std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> >)>::RunOnce(base::internal::BindStateBase*, std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> >&&) ./../../base/bind_internal.h:668
    #20 0x55e86e72e993 in RunImpl<void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::unique_ptr<blink::PendingURLLoaderFactoryBundle>, absl::optional<std::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::unique_ptr<content::DocumentState>, std::unique_ptr<blink::WebNavigationParams>), std::tuple<base::WeakPtr<content::RenderFrameImpl>, mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::unique_ptr<blink::PendingURLLoaderFactoryBundle>, absl::optional<std::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::unique_ptr<content::DocumentState> >, 0UL, 1UL, 2UL, 3UL, 4UL, 5UL, 6UL, 7UL, 8UL> ./../../base/bind_internal.h:721
    #21 0x55e86e72e993 in RunOnce ./../../base/bind_internal.h:690
    #22 0x55e86e72e993 in ?? ??:0
    #23 0x55e86e6d45b9 in content::RenderFrameImpl::CommitNavigation(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, mojo::StructPtr<network::mojom::URLLoaderClientEndpoints>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, absl::optional<std::__1::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, base::UnguessableToken const&, mojo::StructPtr<blink::mojom::PolicyContainer>, base::OnceCallback<void (mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>)>) ./../../base/callback.h:98
    #24 0x55e86e6d45b9 in CommitNavigation ./../../content/renderer/render_frame_impl.cc:2794
    #25 0x55e86e6d45b9 in ?? ??:0
    #26 0x55e86f901741 in content::NavigationClient::CommitNavigation(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, mojo::StructPtr<network::mojom::URLLoaderClientEndpoints>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, absl::optional<std::__1::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, base::UnguessableToken const&, mojo::StructPtr<blink::mojom::PolicyContainer>, base::OnceCallback<void (mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>)>) ./../../content/renderer/navigation_client.cc:43
    #27 0x55e86f901741 in ?? ??:0
    #28 0x55e853bba784 in content::mojom::NavigationClientStubDispatch::AcceptWithResponder(content::mojom::NavigationClient*, mojo::Message*, std::__1::unique_ptr<mojo::MessageReceiverWithStatus, std::__1::default_delete<mojo::MessageReceiverWithStatus> >) ./gen/content/common/navigation_client.mojom.cc:1206
    #29 0x55e853bba784 in ?? ??:0
    #30 0x55e85e64cd47 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:860
    #31 0x55e85e64cd47 in ?? ??:0
    #32 0x55e85e65e7e1 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43
    #33 0x55e85e65e7e1 in ?? ??:0
    #34 0x55e85e650ca7 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:655
    #35 0x55e85e650ca7 in ?? ??:0
    #36 0x55e85ff436d9 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ./../../ipc/ipc_mojo_bootstrap.cc:981
    #37 0x55e85ff436d9 in ?? ??:0
    #38 0x55e85ff3bf74 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:509
    #39 0x55e85ff3bf74 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind_internal.h:648
    #40 0x55e85ff3bf74 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> ./../../base/bind_internal.h:721
    #41 0x55e85ff3bf74 in RunOnce ./../../base/bind_internal.h:690
    #42 0x55e85ff3bf74 in ?? ??:0
    #43 0x55e85db64c10 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/callback.h:98
    #44 0x55e85db64c10 in RunTask ./../../base/task/common/task_annotator.cc:178
    #45 0x55e85db64c10 in ?? ??:0
    #46 0x55e85db9ef39 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:360
    #47 0x55e85db9ef39 in ?? ??:0
    #48 0x55e85db9e6aa in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260
    #49 0x55e85db9e6aa in ?? ??:0
    #50 0x55e85db9f8e1 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() thread_controller_with_message_pump_impl.cc:?
    #51 0x55e85db9f8e1 in ?? ??:0
    #52 0x55e85da5d00f in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39
    #53 0x55e85da5d00f in ?? ??:0
    #54 0x55e85db9ffa4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:467
    #55 0x55e85db9ffa4 in ?? ??:0
    #56 0x55e85dae0281 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134
    #57 0x55e85dae0281 in ?? ??:0
    #58 0x55e8718df851 in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:261
    #59 0x55e8718df851 in ?? ??:0
    #60 0x55e85c97d490 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:569
    #61 0x55e85c97d490 in ?? ??:0
    #62 0x55e85c980374 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:955
    #63 0x55e85c980374 in ?? ??:0
    #64 0x55e85c97ac89 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) ./../../content/app/content_main.cc:386
    #65 0x55e85c97ac89 in ?? ??:0
    #66 0x55e85c97b1bc in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:412
    #67 0x55e85c97b1bc in ?? ??:0
    #68 0x55e84f9c265d in ChromeMain ./../../chrome/app/chrome_main.cc:151
    #69 0x55e84f9c265d in ?? ??:0
    #70 0x7ffb452a80b2 in __libc_start_main ??:?
    #71 0x7ffb452a80b2 in ?? ??:0

0x6210001e8e90 is located 400 bytes inside of 4096-byte region [0x6210001e8d00,0x6210001e9d00)
freed by thread T0 (chrome) here:
    #0 0x55e84f994df2 in __interceptor_free /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:111
    #1 0x55e84f994df2 in ?? ??:0
    #2 0x55e86abe0b02 in WTF::HashTable<blink::UntracedMember<blink::EventTarget>, WTF::KeyValuePair<blink::UntracedMember<blink::EventTarget>, unsigned int>, WTF::KeyValuePairKeyExtractor, WTF::MemberHash<blink::EventTarget>, WTF::HashMapValueTraits<WTF::HashTraits<blink::UntracedMember<blink::EventTarget> >, WTF::HashTraits<unsigned int> >, WTF::HashTraits<blink::UntracedMember<blink::EventTarget> >, WTF::PartitionAllocator>::RehashTo(WTF::KeyValuePair<blink::UntracedMember<blink::EventTarget>, unsigned int>*, unsigned int, WTF::KeyValuePair<blink::UntracedMember<blink::EventTarget>, unsigned int>*) ./../../third_party/blink/renderer/platform/wtf/allocator/partition_allocator.h:68
    #3 0x55e86abe0b02 in DeleteAllBucketsAndDeallocate ./../../third_party/blink/renderer/platform/wtf/hash_table.h:1763
    #4 0x55e86abe0b02 in clear ./../../third_party/blink/renderer/platform/wtf/hash_table.h:1969
    #5 0x55e86abe0b02 in RehashTo ./../../third_party/blink/renderer/platform/wtf/hash_table.h:1898
    #6 0x55e86abe0b02 in ?? ??:0
    #7 0x55e86abdc352 in blink::EventHandlerRegistry::UpdateEventHandlerTargets(blink::EventHandlerRegistry::ChangeOperation, blink::EventHandlerRegistry::EventHandlerClass, blink::EventTarget*) ./../../third_party/blink/renderer/platform/wtf/hash_table.h:1945
    #8 0x55e86abdc352 in Shrink ./../../third_party/blink/renderer/platform/wtf/hash_table.h:916
    #9 0x55e86abdc352 in erase ./../../third_party/blink/renderer/platform/wtf/hash_table.h:1632
    #10 0x55e86abdc352 in erase ./../../third_party/blink/renderer/platform/wtf/hash_table.h:1647
    #11 0x55e86abdc352 in erase ./../../third_party/blink/renderer/platform/wtf/hash_map.h:602
    #12 0x55e86abdc352 in RemoveAll ./../../third_party/blink/renderer/platform/wtf/hash_counted_set.h:161
    #13 0x55e86abdc352 in RemoveAll ./../../third_party/blink/renderer/platform/wtf/hash_counted_set.h:101
    #14 0x55e86abdc352 in UpdateEventHandlerTargets ./../../third_party/blink/renderer/core/frame/event_handler_registry.cc:121
    #15 0x55e86abdc352 in ?? ??:0
    #16 0x55e86abdea8b in blink::EventHandlerRegistry::DidRemoveAllEventHandlers(blink::EventTarget&) ./../../third_party/blink/renderer/core/frame/event_handler_registry.cc:132
    #17 0x55e86abdea8b in DidRemoveAllEventHandlers ./../../third_party/blink/renderer/core/frame/event_handler_registry.cc:214
    #18 0x55e86abdea8b in ?? ??:0
    #19 0x55e86abdf48a in blink::EventHandlerRegistry::ProcessCustomWeakness(blink::LivenessBroker const&) ./../../third_party/blink/renderer/core/frame/event_handler_registry.cc:353
    #20 0x55e86abdf48a in ?? ??:0
    #21 0x55e85af89397 in blink::ThreadHeap::WeakProcessing(blink::MarkingVisitor*) ./../../third_party/blink/renderer/platform/heap/impl/heap.cc:610
    #22 0x55e85af89397 in ?? ??:0
    #23 0x55e85afc613b in blink::ThreadState::MarkPhaseEpilogue(blink::BlinkGC::MarkingType) ./../../third_party/blink/renderer/platform/heap/impl/thread_state.cc:1641
    #24 0x55e85afc613b in ?? ??:0
    #25 0x55e85afc5f7c in blink::ThreadState::AtomicPauseMarkEpilogue(blink::BlinkGC::MarkingType) ./../../third_party/blink/renderer/platform/heap/impl/thread_state.cc:1360
    #26 0x55e85afc5f7c in ?? ??:0
    #27 0x55e85afcac3e in blink::UnifiedHeapController::TraceEpilogue(v8::EmbedderHeapTracer::TraceSummary*) ./../../third_party/blink/renderer/platform/heap/impl/unified_heap_controller.cc:87
    #28 0x55e85afcac3e in ?? ??:0
    #29 0x55e8586a8aa2 in v8::internal::LocalEmbedderHeapTracer::TraceEpilogue() ./../../v8/src/heap/embedder-tracing.cc:37
    #30 0x55e8586a8aa2 in ?? ??:0
    #31 0x55e858730873 in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:2244
    #32 0x55e858730873 in ?? ??:0
    #33 0x55e858728488 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:1791
    #34 0x55e858728488 in ?? ??:0
    #35 0x55e85872d506 in v8::internal::Heap::FinalizeIncrementalMarkingAtomically(v8::internal::GarbageCollectionReason) ./../../v8/src/heap/heap.cc:1465
    #36 0x55e85872d506 in FinalizeIncrementalMarkingAtomically ./../../v8/src/heap/heap.cc:3720
    #37 0x55e85872d506 in ?? ??:0
    #38 0x55e85823dd70 in v8::EmbedderHeapTracer::IncreaseAllocatedSize(unsigned long) ./../../v8/src/heap/embedder-tracing.h:107
    #39 0x55e85823dd70 in IncreaseAllocatedSize ./../../v8/src/api/api.cc:9962
    #40 0x55e85823dd70 in ?? ??:0
    #41 0x55e85afcbea1 in non-virtual thunk to blink::UnifiedHeapController::IncreaseAllocatedObjectSize(unsigned long) ./../../third_party/blink/renderer/platform/heap/impl/unified_heap_controller.cc:176
    #42 0x55e85afcbea1 in IncreaseAllocatedObjectSize ./../../third_party/blink/renderer/platform/heap/impl/unified_heap_controller.cc:183
    #43 0x55e85afcbea1 in ?? ??:0
    #44 0x55e85afabb38 in ?? ??:0
    #45 0x55e85afabb38 in blink::ThreadHeapStatsCollector::AllocatedObjectSizeSafepoint() ./../../third_party/blink/renderer/platform/heap/impl/heap_stats_collector.cc:?
    #46 0x55e85afabb38 in ForAllObservers<(lambda at ../../third_party/blink/renderer/platform/heap/impl/heap_stats_collector.cc:64:19)> ./../../third_party/blink/renderer/platform/heap/impl/heap_stats_collector.cc:275
    #47 0x55e85afabb38 in AllocatedObjectSizeSafepointImpl ./../../third_party/blink/renderer/platform/heap/impl/heap_stats_collector.cc:64
    #48 0x55e85afabb38 in AllocatedObjectSizeSafepoint ./../../third_party/blink/renderer/platform/heap/impl/heap_stats_collector.cc:52
    #49 0x55e85afabb38 in ?? ??:0
    #50 0x55e85afa22ea in blink::NormalPageArena::OutOfLineAllocate(unsigned long, unsigned long) ./../../third_party/blink/renderer/platform/heap/impl/heap_page.cc:925
    #51 0x55e85afa22ea in ?? ??:0
    #52 0x55e85af74ce5 in blink::ThreadHeap::AllocateOnArenaIndex(blink::ThreadState*, unsigned long, int, unsigned int, char const*) ./../../third_party/blink/renderer/platform/heap/impl/heap_page.h:1351
    #53 0x55e85af74ce5 in AllocateOnArenaIndex ./../../third_party/blink/renderer/platform/heap/impl/heap.h:619
    #54 0x55e85af74ce5 in ?? ??:0
    #55 0x55e869e6d721 in blink::MakeGarbageCollectedTrait<blink::HeapVectorBacking<blink::Member<blink::EventTarget>, WTF::VectorTraits<blink::Member<blink::EventTarget> > > >::Call(unsigned long) ./../../third_party/blink/renderer/platform/heap/impl/collection_support/heap_vector_backing.h:88
    #56 0x55e869e6d721 in ?? ??:0
    #57 0x55e86a634c2e in WTF::Vector<blink::Member<blink::EventTarget>, 0u, blink::HeapAllocator>::ReallocateBuffer(unsigned int) ./../../third_party/blink/renderer/platform/heap/impl/heap.h:568
    #58 0x55e86a634c2e in AllocateVectorBacking<blink::Member<blink::EventTarget> > ./../../third_party/blink/renderer/platform/heap/impl/heap_allocator_impl.h:48
    #59 0x55e86a634c2e in AllocateBufferNoBarrier ./../../third_party/blink/renderer/platform/wtf/vector.h:492
    #60 0x55e86a634c2e in AllocateTemporaryBuffer ./../../third_party/blink/renderer/platform/wtf/vector.h:552
    #61 0x55e86a634c2e in ReallocateBuffer ./../../third_party/blink/renderer/platform/wtf/vector.h:2217
    #62 0x55e86a634c2e in ?? ??:0
    #63 0x55e86a633b17 in WTF::Vector<blink::Member<blink::EventTarget>, 0u, blink::HeapAllocator>::ReserveCapacity(unsigned int) ./../../third_party/blink/renderer/platform/wtf/vector.h:1810
    #64 0x55e86a633b17 in ?? ??:0
    #65 0x55e86abe219a in void WTF::Vector<blink::Member<blink::EventTarget>, 0u, blink::HeapAllocator>::AppendSlowCase<blink::UntracedMember<blink::EventTarget> const&>(blink::UntracedMember<blink::EventTarget> const&) ./../../third_party/blink/renderer/platform/wtf/vector.h:1723
    #66 0x55e86abe219a in ExpandCapacity<const blink::UntracedMember<blink::EventTarget> > ./../../third_party/blink/renderer/platform/wtf/vector.h:1745
    #67 0x55e86abe219a in AppendSlowCase<const blink::UntracedMember<blink::EventTarget> &> ./../../third_party/blink/renderer/platform/wtf/vector.h:1920
    #68 0x55e86abe219a in ?? ??:0
    #69 0x55e86abdfddb in push_back<const blink::UntracedMember<blink::EventTarget> &> ./../../third_party/blink/renderer/platform/wtf/vector.h:1875
    #70 0x55e86abdfddb in DocumentDetached ./../../third_party/blink/renderer/core/frame/event_handler_registry.cc:370
    #71 0x55e86abdfddb in ?? ??:0
    #72 0x55e869d3b889 in blink::Document::Shutdown() ./../../third_party/blink/renderer/core/dom/document.cc:2824
    #73 0x55e869d3b889 in ?? ??:0
    #74 0x55e86bfff90c in blink::FrameLoader::DetachDocument(blink::SecurityOrigin*, absl::optional<blink::Document::UnloadEventTiming>*) ./../../third_party/blink/renderer/core/loader/frame_loader.cc:1158
    #75 0x55e86bfff90c in ?? ??:0
    #76 0x55e86bffe282 in blink::FrameLoader::CommitNavigation(std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> >, std::__1::unique_ptr<blink::WebDocumentLoader::ExtraData, std::__1::default_delete<blink::WebDocumentLoader::ExtraData> >, blink::CommitReason) ./../../third_party/blink/renderer/core/loader/frame_loader.cc:1009
    #77 0x55e86bffe282 in ?? ??:0
    #78 0x55e86e6d7a23 in content::RenderFrameImpl::CommitNavigationWithParams(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, absl::optional<std::__1::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::__1::unique_ptr<content::DocumentState, std::__1::default_delete<content::DocumentState> >, std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> >) ./../../content/renderer/render_frame_impl.cc:2928
    #79 0x55e86e6d7a23 in ?? ??:0
    #80 0x55e86e72ee00 in void base::internal::FunctorTraits<void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, absl::optional<std::__1::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::__1::unique_ptr<content::DocumentState, std::__1::default_delete<content::DocumentState> >, std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> >), void>::Invoke<void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, absl::optional<std::__1::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::__1::unique_ptr<content::DocumentState, std::__1::default_delete<content::DocumentState> >, std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> >), base::WeakPtr<content::RenderFrameImpl>, mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, absl::optional<std::__1::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::__1::unique_ptr<content::DocumentState, std::__1::default_delete<content::DocumentState> >, std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> > >(void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, absl::optional<std::__1::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::__1::unique_ptr<content::DocumentState, std::__1::default_delete<content::DocumentState> >, std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> >), base::WeakPtr<content::RenderFrameImpl>&&, mojo::StructPtr<blink::mojom::CommonNavigationParams>&&, mojo::StructPtr<blink::mojom::CommitNavigationParams>&&, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >&&, absl::optional<std::__1::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__1::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >&&, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>&&, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>&&, mojo::PendingRemote<network::mojom::URLLoaderFactory>&&, std::__1::unique_ptr<content::DocumentState, std::__1::default_delete<content::DocumentState> >&&, std::__1::unique_ptr<blink::WebNavigationParams, std::__1::default_delete<blink::WebNavigationParams> >&&) ./../../base/bind_internal.h:509
    #81 0x55e86e72ee00 in ?? ??:0
    #82 0x55e86e72e993 in MakeItSo<void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::unique_ptr<blink::PendingURLLoaderFactoryBundle>, absl::optional<std::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::unique_ptr<content::DocumentState>, std::unique_ptr<blink::WebNavigationParams>), base::WeakPtr<content::RenderFrameImpl>, mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::unique_ptr<blink::PendingURLLoaderFactoryBundle>, absl::optional<std::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::unique_ptr<content::DocumentState>, std::unique_ptr<blink::WebNavigationParams> > ./../../base/bind_internal.h:668
    #83 0x55e86e72e993 in RunImpl<void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::unique_ptr<blink::PendingURLLoaderFactoryBundle>, absl::optional<std::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::unique_ptr<content::DocumentState>, std::unique_ptr<blink::WebNavigationParams>), std::tuple<base::WeakPtr<content::RenderFrameImpl>, mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::unique_ptr<blink::PendingURLLoaderFactoryBundle>, absl::optional<std::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::unique_ptr<content::DocumentState> >, 0UL, 1UL, 2UL, 3UL, 4UL, 5UL, 6UL, 7UL, 8UL> ./../../base/bind_internal.h:721
    #84 0x55e86e72e993 in RunOnce ./../../base/bind_internal.h:690
    #85 0x55e86e72e993 in ?? ??:0
    #86 0x55e86e6d45b9 in Run ./../../base/callback.h:98
    #87 0x55e86e6d45b9 in CommitNavigation ./../../content/renderer/render_frame_impl.cc:2794
    #88 0x55e86e6d45b9 in ?? ??:0

previously allocated by thread T0 (chrome) here:
    #0 0x55e84f99505d in __interceptor_malloc /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:129
    #1 0x55e84f99505d in ?? ??:0
    #2 0x55e862c926d8 in WTF::Partitions::BufferMalloc(unsigned long, char const*) ./../../base/allocator/partition_allocator/partition_root.h:1213
    #3 0x55e862c926d8 in AllocFlags ./../../base/allocator/partition_allocator/partition_root.h:1193
    #4 0x55e862c926d8 in Alloc ./../../base/allocator/partition_allocator/partition_root.h:1522
    #5 0x55e862c926d8 in BufferMalloc ./../../third_party/blink/renderer/platform/wtf/allocator/partitions.cc:292
    #6 0x55e862c926d8 in ?? ??:0
    #7 0x55e86abe06e4 in WTF::HashTable<blink::UntracedMember<blink::EventTarget>, WTF::KeyValuePair<blink::UntracedMember<blink::EventTarget>, unsigned int>, WTF::KeyValuePairKeyExtractor, WTF::MemberHash<blink::EventTarget>, WTF::HashMapValueTraits<WTF::HashTraits<blink::UntracedMember<blink::EventTarget> >, WTF::HashTraits<unsigned int> >, WTF::HashTraits<blink::UntracedMember<blink::EventTarget> >, WTF::PartitionAllocator>::Expand(WTF::KeyValuePair<blink::UntracedMember<blink::EventTarget>, unsigned int>*) ./../../third_party/blink/renderer/platform/wtf/allocator/partition_allocator.h:61
    #8 0x55e86abe06e4 in AllocateTable ./../../third_party/blink/renderer/platform/wtf/hash_table.h:1707
    #9 0x55e86abe06e4 in Rehash ./../../third_party/blink/renderer/platform/wtf/hash_table.h:1944
    #10 0x55e86abe06e4 in Expand ./../../third_party/blink/renderer/platform/wtf/hash_table.h:1786
    #11 0x55e86abe06e4 in ?? ??:0
    #12 0x55e86abe0343 in WTF::HashTableAddResult<WTF::HashTable<blink::UntracedMember<blink::EventTarget>, WTF::KeyValuePair<blink::UntracedMember<blink::EventTarget>, unsigned int>, WTF::KeyValuePairKeyExtractor, WTF::MemberHash<blink::EventTarget>, WTF::HashMapValueTraits<WTF::HashTraits<blink::UntracedMember<blink::EventTarget> >, WTF::HashTraits<unsigned int> >, WTF::HashTraits<blink::UntracedMember<blink::EventTarget> >, WTF::PartitionAllocator>, WTF::KeyValuePair<blink::UntracedMember<blink::EventTarget>, unsigned int> > WTF::HashTable<blink::UntracedMember<blink::EventTarget>, WTF::KeyValuePair<blink::UntracedMember<blink::EventTarget>, unsigned int>, WTF::KeyValuePairKeyExtractor, WTF::MemberHash<blink::EventTarget>, WTF::HashMapValueTraits<WTF::HashTraits<blink::UntracedMember<blink::EventTarget> >, WTF::HashTraits<unsigned int> >, WTF::HashTraits<blink::UntracedMember<blink::EventTarget> >, WTF::PartitionAllocator>::insert<WTF::HashMapTranslator<WTF::HashMapValueTraits<WTF::HashTraits<blink::UntracedMember<blink::EventTarget> >, WTF::HashTraits<unsigned int> >, WTF::MemberHash<blink::EventTarget>, WTF::PartitionAllocator>, blink::UntracedMember<blink::EventTarget> const&, int>(blink::UntracedMember<blink::EventTarget> const&, int&&) ./../../third_party/blink/renderer/platform/wtf/hash_table.h:1435
    #13 0x55e86abe0343 in ?? ??:0
    #14 0x55e86abdc0e7 in blink::EventHandlerRegistry::UpdateEventHandlerTargets(blink::EventHandlerRegistry::ChangeOperation, blink::EventHandlerRegistry::EventHandlerClass, blink::EventTarget*) ./../../third_party/blink/renderer/platform/wtf/hash_map.h:537
    #15 0x55e86abdc0e7 in insert<const blink::UntracedMember<blink::EventTarget> &, int> ./../../third_party/blink/renderer/platform/wtf/hash_map.h:577
    #16 0x55e86abdc0e7 in insert ./../../third_party/blink/renderer/platform/wtf/hash_counted_set.h:128
    #17 0x55e86abdc0e7 in insert ./../../third_party/blink/renderer/platform/wtf/hash_counted_set.h:136
    #18 0x55e86abdc0e7 in UpdateEventHandlerTargets ./../../third_party/blink/renderer/core/frame/event_handler_registry.cc:114
    #19 0x55e86abdc0e7 in ?? ??:0
    #20 0x55e86abddd2a in blink::EventHandlerRegistry::DidAddEventHandler(blink::EventTarget&, blink::EventHandlerRegistry::EventHandlerClass) ./../../third_party/blink/renderer/core/frame/event_handler_registry.cc:132
    #21 0x55e86abddd2a in DidAddEventHandler ./../../third_party/blink/renderer/core/frame/event_handler_registry.cc:169
    #22 0x55e86abddd2a in ?? ??:0
    #23 0x55e86afae8ad in blink::SliderContainerElement::UpdateTouchEventHandlerRegistry() ./../../third_party/blink/renderer/core/html/forms/slider_thumb_element.cc:447
    #24 0x55e86afae8ad in ?? ??:0
    #25 0x55e86afae70c in blink::SliderContainerElement::SliderContainerElement(blink::Document&) ./../../third_party/blink/renderer/core/html/forms/slider_thumb_element.cc:317
    #26 0x55e86afae70c in ?? ??:0
    #27 0x55e86af8d322 in blink::RangeInputType::CreateShadowSubtree() ./../../third_party/blink/renderer/platform/heap/impl/heap.h:528
    #28 0x55e86af8d322 in MakeGarbageCollected<blink::SliderContainerElement, blink::Document &> ./../../third_party/blink/renderer/platform/heap/impl/heap.h:568
    #29 0x55e86af8d322 in CreateShadowSubtree ./../../third_party/blink/renderer/core/html/forms/range_input_type.cc:248
    #30 0x55e86af8d322 in ?? ??:0
    #31 0x55e86aeae919 in blink::HTMLInputElement::UpdateType() ./../../third_party/blink/renderer/core/html/forms/html_input_element.cc:1451
    #32 0x55e86aeae919 in UpdateType ./../../third_party/blink/renderer/core/html/forms/html_input_element.cc:467
    #33 0x55e86aeae919 in ?? ??:0
    #34 0x55e86aeb5720 in blink::HTMLInputElement::ParseAttribute(blink::Element::AttributeModificationParams const&) ./../../third_party/blink/renderer/core/html/forms/html_input_element.cc:805
    #35 0x55e86aeb5720 in ?? ??:0
    #36 0x55e869ee448f in blink::Element::AttributeChanged(blink::Element::AttributeModificationParams const&) ./../../third_party/blink/renderer/core/dom/element.cc:2315
    #37 0x55e869ee448f in ?? ??:0
    #38 0x55e86b01bd84 in blink::HTMLElement::AttributeChanged(blink::Element::AttributeModificationParams const&) ./../../third_party/blink/renderer/core/html/html_element.cc:740
    #39 0x55e86b01bd84 in ?? ??:0
    #40 0x55e86ae7e104 in blink::HTMLFormControlElement::AttributeChanged(blink::Element::AttributeModificationParams const&) ./../../third_party/blink/renderer/core/html/forms/html_form_control_element.cc:109
    #41 0x55e86ae7e104 in ?? ??:0
    #42 0x55e869f06d82 in blink::Element::DidAddAttribute(blink::QualifiedName const&, WTF::AtomicString const&) ./../../third_party/blink/renderer/core/dom/element.cc:5762
    #43 0x55e869f06d82 in ?? ??:0
    #44 0x55e869f06518 in blink::Element::AppendAttributeInternal(blink::QualifiedName const&, WTF::AtomicString const&, blink::Element::SynchronizationOfLazyAttribute) ./../../third_party/blink/renderer/core/dom/element.cc:3905
    #45 0x55e869f06518 in ?? ??:0
    #46 0x55e86d5e22ed in blink::Element::setAttribute(blink::QualifiedName const&, WTF::AtomicString const&) ./../../third_party/blink/renderer/core/dom/element-hot.cc:202
    #47 0x55e86d5e22ed in setAttribute ./../../third_party/blink/renderer/core/dom/element-hot.cc:110
    #48 0x55e86d5e22ed in ?? ??:0
    #49 0x55e86e38c621 in blink::MediaControlSliderElement::MediaControlSliderElement(blink::MediaControlsImpl&) ./../../third_party/blink/renderer/modules/media_controls/elements/media_control_slider_element.cc:94
    #50 0x55e86e38c621 in ?? ??:0
    #51 0x55e86e396c6c in blink::MediaControlVolumeSliderElement::MediaControlVolumeSliderElement(blink::MediaControlsImpl&, blink::MediaControlVolumeControlContainerElement*) ./../../third_party/blink/renderer/modules/media_controls/elements/media_control_volume_slider_element.cc:84
    #52 0x55e86e396c6c in ?? ??:0
    #53 0x55e86e313e8a in blink::MediaControlsImpl::InitializeControls() ./../../third_party/blink/renderer/platform/heap/impl/heap.h:528
    #54 0x55e86e313e8a in MakeGarbageCollected<blink::MediaControlVolumeSliderElement, blink::MediaControlsImpl &, blink::MediaControlVolumeControlContainerElement *> ./../../third_party/blink/renderer/platform/heap/impl/heap.h:568
    #55 0x55e86e313e8a in InitializeControls ./../../third_party/blink/renderer/modules/media_controls/media_controls_impl.cc:556
    #56 0x55e86e313e8a in ?? ??:0
    #57 0x55e86e312557 in blink::MediaControlsImpl::Create(blink::HTMLMediaElement&, blink::ShadowRoot&) ./../../third_party/blink/renderer/modules/media_controls/media_controls_impl.cc:414
    #58 0x55e86e312557 in ?? ??:0
    #59 0x55e86f9856ce in blink::ModulesInitializer::CreateMediaControls(blink::HTMLMediaElement&, blink::ShadowRoot&) const ./../../third_party/blink/renderer/modules/modules_initializer.cc:251
    #60 0x55e86f9856ce in ?? ??:0
    #61 0x55e86b12e482 in blink::HTMLMediaElement::UpdateControlsVisibility() ./../../third_party/blink/renderer/core/html/media/html_media_element.cc:4106
    #62 0x55e86b12e482 in UpdateControlsVisibility ./../../third_party/blink/renderer/core/html/media/html_media_element.cc:4125
    #63 0x55e86b12e482 in ?? ??:0
    #64 0x55e869f4a9cc in blink::ContainerNode::DidInsertNodeVector(blink::HeapVector<blink::Member<blink::Node>, 11u> const&, blink::Node*, blink::HeapVector<blink::Member<blink::Node>, 11u> const&) ./../../third_party/blink/renderer/core/dom/container_node.cc:349
    #65 0x55e869f4a9cc in ?? ??:0
    #66 0x55e869f4be71 in blink::ContainerNode::AppendChild(blink::Node*, blink::ExceptionState&) ./../../third_party/blink/renderer/core/dom/container_node.cc:881
    #67 0x55e869f4be71 in ?? ??:0
    #68 0x55e869e87746 in blink::Node::appendChild(blink::Node*, blink::ExceptionState&) ./../../third_party/blink/renderer/core/dom/node.cc:756
    #69 0x55e869e87746 in ?? ??:0
    #70 0x55e86db9ca94 in blink::(anonymous namespace)::v8_node::AppendChildOperationCallbackForMainWorld(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/core/v8/v8_node.cc:476
    #71 0x55e86db9ca94 in ?? ??:0
    #72 0x55e8582d8cd2 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:155
    #73 0x55e8582d8cd2 in ?? ??:0
    #74 0x55e8582d66ee in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:112
    #75 0x55e8582d66ee in ?? ??:0
    #76 0x55e8582d412b in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:142
    #77 0x55e8582d412b in ?? ??:0

SUMMARY: AddressSanitizer: heap-use-after-free (/home/exp11/asan-linux-release/chrome+0x25c984d5)
Shadow bytes around the buggy address:
  0x0c4280035180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c4280035190: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c42800351a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c42800351b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c42800351c0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0c42800351d0: fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c42800351e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c42800351f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c4280035200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c4280035210: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c4280035220: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==1==ABORTING

Did this work before? N/A 

Chrome version: 93.0.4577.8 dev  Channel: dev
OS Version: 20.04

## Attachments

- [main.html](attachments/main.html) (text/plain, 375 B)
- [crash.html](attachments/crash.html) (text/plain, 330 B)

## Timeline

### [Deleted User] (2021-08-02)

[Empty comment from Monorail migration]

### me...@chromium.org (2021-08-02)

Thanks for the report.

japhet: Could you PTAL?

[Monorail components: Blink>Loader UI>Browser>Navigation]

### [Deleted User] (2021-08-02)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-02)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-02)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ja...@chromium.org (2021-08-04)

It's not clear to me that this case is specific to loading/navigation. Based on the clusterfuzz report, it looks to me like a garbage collection is happening inside of a stack-allocated vector's buffer resize, and some of the vector's internal state is being collected, then accessed right after the resize. It's not clear to me if this is a WTF issue, an oilpan issue, or a misuse of HeapVector in EventHandlerRegistry.

yutak@, can I assign to you for input as a wtf/OWNER?

[Monorail components: Blink>Internals>WTF Blink>MemoryAllocator>GarbageCollection]

### pb...@google.com (2021-08-05)

Reminder M93 is already in Beta and Stable cut on Aug-17th(coming soon). Please review this bug and assess if this is indeed a M93 RBS.

If not, please remove the RBS label. If so, please make sure to land the fix and request a merge to M93 release branch(4577)  ASAP. Thank you.

### ja...@chromium.org (2021-08-06)

[Empty comment from Monorail migration]

### ha...@google.com (2021-08-06)

Bartek: Would you triage this in the memory team?

Cc-ing a few oilpan folks. It looks like EventHandlerRegistry::DocumentDetached fails to keep a reference to a HashTable that should be kept alive...?

### ba...@chromium.org (2021-08-06)

Keishi started looking into this, but because I asked him quite late (sorry!) he didn't have much time to find anything interesting. Given the urgency, may I transfer it over to the European timezone for investigation? Japan will be on holiday this Monday.


### ke...@chromium.org (2021-08-06)

I think I figured it out. I see modification while iterating over EventHandlerRegistry::targets_, happening because of ConservativeGC.
This seems serious but event_handler_registry.cc hasn't been modified in a while so the bug might be old.
I will work on a fix.

### om...@chromium.org (2021-08-06)

Interesting. This is actually a side effect of using UntracedMember.

Generally speaking, if we have a GC finalization while iterating over a collection, what happens is that we will conservatively scan the stack (i.e. conservative GC) and find the iterator to the collection (which points to the backing store). This will result in strongifying the backing store (even if it was already traced non-conservatively), which means all references in it are treated as strong references.
We do this to prevent any object referenced by the collection from dying while the collection is being iterated and to prevent the GC from modifying the collection in the middle of iteration.

Because EventHandlerRegistry::targets_ uses HashCountedSet<UntracedMember<...>>, the backing store is not the heap.
Thus the GC doesn't recognize the iterator on the stack, the contents of the collection aren't kept alive and the GC is allowed to modify the collection.

Can this be refactored to not use UntracedMembers?

### om...@chromium.org (2021-08-09)

I think the simplest fix for this issue would be to wrap all iterations over the |targets_| set in a GCForbiddenScope.
That would tell the GC not to finalize during iteration of the set and so it will not run the weak callback during that time.

### am...@google.com (2021-08-09)

[Empty comment from Monorail migration]

### ke...@chromium.org (2021-08-10)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a94b5d9cd12d118a7665d3c25d9c54db4a9ad532

commit a94b5d9cd12d118a7665d3c25d9c54db4a9ad532
Author: Keishi Hattori <keishi@chromium.org>
Date: Tue Aug 10 10:03:13 2021

Avoid GC while iterating over EventHandlerRegistry::targets_

If a GC runs while iterating over EventHandlerRegistry::targets_, the weak processing will try to remove elements from it causing the iterator to break.

Bug: 1235316
Change-Id: Ia29bc139600e039c233059dec0d14400731afa34
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3077922
Commit-Queue: Keishi Hattori <keishi@chromium.org>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Reviewed-by: Omer Katz <omerkatz@chromium.org>
Cr-Commit-Position: refs/heads/master@{#910227}

[modify] https://crrev.com/a94b5d9cd12d118a7665d3c25d9c54db4a9ad532/third_party/blink/renderer/core/frame/event_handler_registry.cc


### gi...@appspot.gserviceaccount.com (2021-08-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/67e92e422acbb54cec539c28063d16b18af7a5dc

commit 67e92e422acbb54cec539c28063d16b18af7a5dc
Author: Arthur Hemery <ahemery@chromium.org>
Date: Tue Aug 10 10:18:36 2021

Revert "Avoid GC while iterating over EventHandlerRegistry::targets_"

This reverts commit a94b5d9cd12d118a7665d3c25d9c54db4a9ad532.

Reason for revert: Suspect of compilation failure on lacros (https://ci.chromium.org/ui/p/chromium/builders/ci/lacros-amd64-generic-binary-size-rel/16160/overview) that led to tree closure.

Original change's description:
> Avoid GC while iterating over EventHandlerRegistry::targets_
>
> If a GC runs while iterating over EventHandlerRegistry::targets_, the weak processing will try to remove elements from it causing the iterator to break.
>
> Bug: 1235316
> Change-Id: Ia29bc139600e039c233059dec0d14400731afa34
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3077922
> Commit-Queue: Keishi Hattori <keishi@chromium.org>
> Reviewed-by: Kentaro Hara <haraken@chromium.org>
> Reviewed-by: Omer Katz <omerkatz@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#910227}

Bug: 1235316
Change-Id: I39888933747b7f7e9bdbed600a13773be0118302
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3085141
Auto-Submit: Arthur Hemery <ahemery@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Arthur Hemery <ahemery@chromium.org>
Owners-Override: Arthur Hemery <ahemery@google.com>
Cr-Commit-Position: refs/heads/master@{#910230}

[modify] https://crrev.com/67e92e422acbb54cec539c28063d16b18af7a5dc/third_party/blink/renderer/core/frame/event_handler_registry.cc


### pb...@google.com (2021-08-10)

Reminder M93 is already in Beta and Stable cut on Aug-17th(coming soon). Please review this bug and assess if this is indeed a M93 RBS.
If not, please remove the RBS label. If so, please make sure to land the fix and request a merge to M93 release branch(4577)  ASAP. Thank you.


### gi...@appspot.gserviceaccount.com (2021-08-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1a40dfdbc733f529d698136c6cc717d3740f4bd2

commit 1a40dfdbc733f529d698136c6cc717d3740f4bd2
Author: Keishi Hattori <keishi@chromium.org>
Date: Thu Aug 12 01:44:07 2021

Reland "Avoid GC while iterating over EventHandlerRegistry::targets_"

This is a reland of a94b5d9cd12d118a7665d3c25d9c54db4a9ad532

It was reverted because of a missing include.

Original change's description:
> Avoid GC while iterating over EventHandlerRegistry::targets_
>
> If a GC runs while iterating over EventHandlerRegistry::targets_, the weak processing will try to remove elements from it causing the iterator to break.
>
> Bug: 1235316
> Change-Id: Ia29bc139600e039c233059dec0d14400731afa34
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3077922
> Commit-Queue: Keishi Hattori <keishi@chromium.org>
> Reviewed-by: Kentaro Hara <haraken@chromium.org>
> Reviewed-by: Omer Katz <omerkatz@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#910227}

Bug: 1235316
Change-Id: I57e8184848abe91d261c2c001ee0c24da2c83e1d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3085693
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Commit-Queue: Keishi Hattori <keishi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#911108}

[modify] https://crrev.com/1a40dfdbc733f529d698136c6cc717d3740f4bd2/third_party/blink/renderer/core/frame/event_handler_registry.cc


### am...@chromium.org (2021-08-16)

hi keishi@, do these relands fully address this UaF? If so, please go ahead and update this as fixed. That would ordinarily kickoff the merge review process. Because cut for 93 beta is today for release tomorrow, there will need to be a manual merge request so we can review this for merge today. As it stands, this issue still appears to be a release blocker. I also realize yesterday was a holiday in Japan, so apologies for the first-thing nag today! 

### ke...@chromium.org (2021-08-17)

Sorry. Yes the reland CL has completely fix the issue for now. I would like to have it merged if possible.

### [Deleted User] (2021-08-17)

[Empty comment from Monorail migration]

### ke...@chromium.org (2021-08-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-17)

This bug requires manual review: We are only 13 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: benmason@(Android), govind@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-08-17)

Thanks, keishi@! Merge approved to M93, please go ahead and merge to branch 4577 at soonest. Thanks! 

### [Deleted User] (2021-08-17)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5a5d48c80610b35684b355eca1cb4f1899ac87ee

commit 5a5d48c80610b35684b355eca1cb4f1899ac87ee
Author: Keishi Hattori <keishi@chromium.org>
Date: Tue Aug 17 22:39:26 2021

Reland "Avoid GC while iterating over EventHandlerRegistry::targets_"

This is a reland of a94b5d9cd12d118a7665d3c25d9c54db4a9ad532

It was reverted because of a missing include.

Original change's description:
> Avoid GC while iterating over EventHandlerRegistry::targets_
>
> If a GC runs while iterating over EventHandlerRegistry::targets_, the weak processing will try to remove elements from it causing the iterator to break.
>
> Bug: 1235316
> Change-Id: Ia29bc139600e039c233059dec0d14400731afa34
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3077922
> Commit-Queue: Keishi Hattori <keishi@chromium.org>
> Reviewed-by: Kentaro Hara <haraken@chromium.org>
> Reviewed-by: Omer Katz <omerkatz@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#910227}

(cherry picked from commit 1a40dfdbc733f529d698136c6cc717d3740f4bd2)

Bug: 1235316
Change-Id: I57e8184848abe91d261c2c001ee0c24da2c83e1d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3085693
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Commit-Queue: Keishi Hattori <keishi@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#911108}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3101545
Auto-Submit: Keishi Hattori <keishi@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4577@{#912}
Cr-Branched-From: 761ddde228655e313424edec06497d0c56b0f3c4-refs/heads/master@{#902210}

[modify] https://crrev.com/5a5d48c80610b35684b355eca1cb4f1899ac87ee/third_party/blink/renderer/core/frame/event_handler_registry.cc


### am...@google.com (2021-08-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-25)

Congratulations! The VRP Panel has decided to award you $7500 for this report. Nice work and thank you! 

### am...@google.com (2021-08-27)

[Empty comment from Monorail migration]

### dt...@chromium.org (2021-09-01)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-09-16)

[Empty comment from Monorail migration]

[Monorail components: -Blink>MemoryAllocator>GarbageCollection Blink>GarbageCollection]

### [Deleted User] (2021-11-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-01-05)

Hello OP/emilykim@, we consider attachments/pocs included with reports to be an integral part of the report (https://bughunters.google.com/about/rules/5745167867576320), so I've undeleted them. Thank you! 

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1235316?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>GarbageCollection, Blink>Internals>WTF, Blink>Loader, UI>Browser>Navigation]
[Monorail mergedwith: crbug.com/chromium/1244341]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056756)*
