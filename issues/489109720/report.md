# heap-use-after-free in VerticalTabDragHandlerImpl::ViewFromTabSlot(TabSlotView*)

| Field | Value |
|-------|-------|
| **Issue ID** | [489109720](https://issues.chromium.org/issues/489109720) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Mobile>TabStrip |
| **Platforms** | Linux, Windows, ChromeOS |
| **Chrome Version** | 144.0.0.0 |
| **Reporter** | ch...@gmail.com |
| **Assignee** | tl...@chromium.org |
| **Created** | 2026-03-03 |
| **Bounty** | $3,000.00 |

## Description

# Steps to reproduce the problem

1)Open Chrome in Vertical Tabs mode by enabling chrome://flags/#vertical-tabs.
2)Open the testcase.
3)Click the button and drag the opened tab while holding it until it closes.

# Problem Description

Dragging a tab in Chrome’s Vertical Tabs mode causes a Use-After-Free (MiraclePtr Status: NOT PROTECTED) crash, resulting in the browser crashing unexpectedly.

# Summary

heap-use-after-free in VerticalTabDragHandlerImpl::ViewFromTabSlot(TabSlotView\*)

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [asan](attachments/asan) (application/octet-stream, 26.5 KB)
- [testcase.html](attachments/testcase.html) (text/html, 490 B)
- [simplescreenrecorder-2026-03-03_05.46.21.mp4](attachments/simplescreenrecorder-2026-03-03_05.46.21.mp4) (video/mp4, 5.9 MB)
- [simplescreenrecorder-2026-03-17_05.53.51.mp4](attachments/simplescreenrecorder-2026-03-17_05.53.51.mp4) (video/mp4, 976.3 KB)

## Timeline

### ch...@gmail.com (2026-03-03)

==36361==ERROR: AddressSanitizer: heap-use-after-free on address 0x724cdd1cf480 at pc 0x5fa41fa11319 bp 0x7ffeb96a19d0 sp 0x7ffeb96a19c8
READ of size 8 at 0x724cdd1cf480 thread T0 (chrome)
==36361==WARNING: invalid path to external symbolizer!
==36361==WARNING: Failed to use and restart external symbolizer!
    #0 0x5fa41fa11318 in VerticalTabDragHandlerImpl::ViewFromTabSlot(TabSlotView*) const ./../../ui/base/metadata/metadata_utils.h:40:42
    #1 0x5fa41fa1013c in VerticalTabDragHandlerImpl::IsViewDragging(views::View const&) const ./../../chrome/browser/ui/views/tabs/vertical/vertical_tab_drag_handler.cc:499:18
    #2 0x5fa41f9c8b55 in TabCollectionAnimatingLayoutManager::InterpolateLayout(double) const ./../../chrome/browser/ui/views/tabs/vertical/tab_collection_animating_layout_manager.cc:339:35
    #3 0x5fa41f9c7c34 in TabCollectionAnimatingLayoutManager::LayoutImpl() ./../../chrome/browser/ui/views/tabs/vertical/tab_collection_animating_layout_manager.cc:171:23
    #4 0x5fa42afdece7 in views::LayoutManagerBase::Layout(views::View*) ./../../ui/views/layout/layout_manager_base.cc:116:3
    #5 0x5fa42b02cde8 in views::View::Layout(base::NonCopyablePassKey<views::View>) ./../../ui/views/view.cc:953:25
    #6 0x5fa42b021e02 in views::View::LayoutImmediately() ./../../ui/views/view.cc:3786:3
    #7 0x5fa42b02d1dc in views::View::Layout(base::NonCopyablePassKey<views::View>) ./../../ui/views/view.cc:969:14
    #8 0x5fa42b021e02 in views::View::LayoutImmediately() ./../../ui/views/view.cc:3786:3
    #9 0x5fa42b020094 in views::View::SetBoundsRect(gfx::Rect const&) ./../../ui/views/view.cc:412:7
    #10 0x5fa42af0d02b in views::ScrollView::Layout(base::NonCopyablePassKey<views::View>) ./../../ui/views/controls/scroll_view.cc:809:23
    #11 0x5fa42b021e02 in views::View::LayoutImmediately() ./../../ui/views/view.cc:3786:3
    #12 0x5fa42b02d1dc in views::View::Layout(base::NonCopyablePassKey<views::View>) ./../../ui/views/view.cc:969:14
    #13 0x5fa42b021e02 in views::View::LayoutImmediately() ./../../ui/views/view.cc:3786:3
    #14 0x5fa42afe0e4e in views::LayoutManagerBase::ApplyLayout(views::ProposedLayout const&) ./../../ui/views/layout/layout_manager_base.cc:239:21
    #15 0x5fa42afe06de in views::LayoutManagerBase::LayoutImpl() ./../../ui/views/layout/layout_manager_base.cc:199:3
    #16 0x5fa42afdece7 in views::LayoutManagerBase::Layout(views::View*) ./../../ui/views/layout/layout_manager_base.cc:116:3
    #17 0x5fa42b02cde8 in views::View::Layout(base::NonCopyablePassKey<views::View>) ./../../ui/views/view.cc:953:25
    #18 0x5fa43c029444 in VerticalTabStripRegionView::Layout(base::NonCopyablePassKey<views::View>) ./../../ui/views/view.h:2020:38
    #19 0x5fa42b021e02 in views::View::LayoutImmediately() ./../../ui/views/view.cc:3786:3
    #20 0x5fa42b020094 in views::View::SetBoundsRect(gfx::Rect const&) ./../../ui/views/view.cc:412:7
    #21 0x5fa43bfaf6bd in BrowserViewLayoutImpl::ProposedLayout::ApplyLayout(views::View*, base::FunctionRef<void (views::View*, bool)>) && ./../../chrome/browser/ui/views/frame/layout/browser_view_layout_impl.cc:89:14
    #22 0x5fa43bfb0976 in BrowserViewLayoutImpl::Layout(views::View*) ./../../chrome/browser/ui/views/frame/layout/browser_view_layout_impl.cc:213:35
    #23 0x5fa42b02cde8 in views::View::Layout(base::NonCopyablePassKey<views::View>) ./../../ui/views/view.cc:953:25
    #24 0x5fa43bea42d7 in BrowserView::Layout(base::NonCopyablePassKey<views::View>) ./../../ui/views/view.h:2020:38
    #25 0x5fa42b021e02 in views::View::LayoutImmediately() ./../../ui/views/view.cc:3786:3
    #26 0x5fa43be84092 in BrowserView::UpdateUIForContents(content::WebContents*, bool) ./../../chrome/browser/ui/views/frame/browser_view.cc:5563:7
    #27 0x5fa43be82dc9 in BrowserView::OnActiveTabChanged(content::WebContents*, content::WebContents*, int, int) ./../../chrome/browser/ui/views/frame/browser_view.cc:1988:3
    #28 0x5fa43b46526e in Browser::OnActiveTabChanged(TabStripModelChange const&, TabStripSelectionChange const&) ./../../chrome/browser/ui/browser.cc:3118:12
    #29 0x5fa43b463b2c in Browser::OnTabStripModelChanged(TabStripModel*, TabStripModelChange const&, TabStripSelectionChange const&) ./../../chrome/browser/ui/browser.cc:1572:3
    #30 0x5fa41f28b25e in TabStripModel::OnChange(TabStripModelChange const&, TabStripSelectionChange const&) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:701:14
    #31 0x5fa41f290537 in TabStripModel::SendDetachWebContentsNotifications(TabStripModel::DetachNotifications*) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:988:5
    #32 0x5fa41f2a7901 in TabStripModel::CloseTabs(base::span<content::WebContents* const, 18446744073709551615ul, content::WebContents* const*>, unsigned int) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:3749:5
    #33 0x5fa41f2a97f9 in TabStripModel::CloseWebContentsAt(int, unsigned int) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:1311:3
    #34 0x5fa43b5071b5 in chrome::CloseWebContents(Browser*, content::WebContents*, bool) ./../../chrome/browser/ui/browser_tabstrip.cc:123:31
    #35 0x5fa418c6cc4a in content::WebContentsImpl::Close() ./../../content/browser/web_contents/web_contents_impl.cc:9462:16
    #36 0x5fa41833c82d in content::RenderFrameHostImpl::ClosePageIgnoringUnloadEvents(content::RenderFrameHostImpl::ClosePageSource, base::RepeatingCallback<void ()>) ./../../content/browser/renderer_host/render_frame_host_impl.cc:7588:14
    #37 0x5fa41833c484 in content::RenderFrameHostImpl::RequestClose() ./../../content/browser/renderer_host/render_frame_host_impl.cc:7452:3
    #38 0x5fa41008a898 in blink::mojom::LocalMainFrameHostStubDispatch::Accept(blink::mojom::LocalMainFrameHost*, mojo::Message*) ./gen/third_party/blink/public/mojom/frame/frame.mojom.cc:0:0
    #39 0x5fa422cab3e9 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085:54
    #40 0x5fa422cc9123 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:51:24
    #41 0x5fa422cb1893 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #42 0x5fa426be1d1d in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ./../../ipc/ipc_mojo_bootstrap.cc:1199:24
    #43 0x5fa426be4191 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:740:12
    #44 0x5fa422ee9b56 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/functional/callback.h:155:12
    #45 0x5fa422f61319 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/common/task_annotator.h:112:5
    #46 0x5fa422f6018a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #47 0x5fa42310db08 in base::MessagePumpGlib::HandleDispatch() ./../../base/message_loop/message_pump_glib.cc:736:46
    #48 0x5fa4231110c8 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) ./../../base/message_loop/message_pump_glib.cc:355:43
    #49 0x74ccdfd8d584 in g_source_query_unix_fd ??:?
    #50 0x74ccdfdec976 in g_io_channel_new_file ??:?
    #51 0x74ccdfd8ca22 in g_main_context_iteration ??:0:0
    #52 0x5fa42310e123 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_glib.cc:770:30
    #53 0x5fa422f62a27 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #54 0x5fa422e650c0 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:135:14
    #55 0x5fa416d8f26c in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser_main_loop.cc:1103:18
    #56 0x5fa416d9792c in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser_main_runner_impl.cc:151:15
    #57 0x5fa416d85b8c in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser_main.cc:32:28
    #58 0x5fa41ebb456f in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:696:10
    #59 0x5fa41ebb8560 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content_main_runner_impl.cc:1320:10
    #60 0x5fa41ebb79ea in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1150:12
    #61 0x5fa41ebb1391 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:358:36
    #62 0x5fa41ebb198c in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:371:10
    #63 0x5fa40b88ab39 in ChromeMain ./../../chrome/app/chrome_main.cc:191:12
    #64 0x74ccde82a1c9 in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #65 0x74ccde82a28a in __libc_start_main ./csu/../csu/libc-start.c:360:3
    #66 0x5fa40b7b0029 in _start ??:0:0

0x724cdd1cf480 is located 0 bytes inside of 832-byte region [0x724cdd1cf480,0x724cdd1cf7c0)
freed by thread T0 (chrome) here:
    #0 0x5fa40b889c3d in operator delete(void*) ??:0:0
    #1 0x5fa41fa16a67 in VerticalTabDragHandlerImpl::OnNodeWillDestroy(TabCollectionNode&) ./gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #2 0x5fa41fa1a8d6 in void base::internal::Invoker<base::internal::FunctorTraits<void (VerticalTabDragHandlerImpl::*&&)(TabCollectionNode&), VerticalTabDragHandlerImpl*, std::__Cr::reference_wrapper<TabCollectionNode>&&>, base::internal::BindState<true, true, false, void (VerticalTabDragHandlerImpl::*)(TabCollectionNode&), base::internal::UnretainedWrapper<VerticalTabDragHandlerImpl, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedRefWrapper<TabCollectionNode, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, void ()>::RunImpl<void (VerticalTabDragHandlerImpl::*)(TabCollectionNode&), std::__Cr::tuple<base::internal::UnretainedWrapper<VerticalTabDragHandlerImpl, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedRefWrapper<TabCollectionNode, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0ul, 1ul>(void (VerticalTabDragHandlerImpl::*&&)(TabCollectionNode&), std::__Cr::tuple<base::internal::UnretainedWrapper<VerticalTabDragHandlerImpl, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedRefWrapper<TabCollectionNode, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>) ./../../base/functional/bind_internal.h:740:12
    #3 0x5fa40e662139 in void base::OnceCallbackList<void ()>::RunCallback<>(std::__Cr::__list_iterator<base::OnceCallback<void ()>, void*>) ./../../base/functional/callback.h:155:12
    #4 0x5fa40e65bc23 in void base::internal::CallbackListBase<base::OnceCallbackList<void ()> >::Notify<>() ./../../base/callback_list.h:229:47
    #5 0x5fa41f9db990 in TabCollectionNode::~TabCollectionNode() ./../../chrome/browser/ui/views/tabs/vertical/tab_collection_node.cc:118:34
    #6 0x5fa41f9dbca3 in TabCollectionNode::~TabCollectionNode() ./../../chrome/browser/ui/views/tabs/vertical/tab_collection_node.cc:117:41
    #7 0x5fa41f9dd38b in TabCollectionNode::RemoveChild(base::PassKey<TabCollectionNode>, std::__Cr::variant<tabs::SupportsHandles<tabs::TabCollectionHandleFactory>::Handle, tabs::SupportsHandles<tabs::SessionMappedTabHandleFactory>::Handle> const&, bool) ./gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #8 0x5fa41f9bf562 in non-virtual thunk to RootTabCollectionNode::OnChildrenRemoved(tabs::TabCollection::Position const&, std::__Cr::vector<std::__Cr::variant<tabs::SupportsHandles<tabs::TabCollectionHandleFactory>::Handle, tabs::SupportsHandles<tabs::SessionMappedTabHandleFactory>::Handle>, std::__Cr::allocator<std::__Cr::variant<tabs::SupportsHandles<tabs::TabCollectionHandleFactory>::Handle, tabs::SupportsHandles<tabs::SessionMappedTabHandleFactory>::Handle> > > const&) ./../../chrome/browser/ui/views/tabs/vertical/root_tab_collection_node.cc:93:18
    #9 0x5fa41aaa0ecb in _ZN4base12ObserverListIN4tabs21TabCollectionObserverELb0ELNS_28ObserverListReentrancyPolicyE1ENS_8internal22CheckedObserverAdapterEE6NotifyIMS2_FvRKNS1_13TabCollection8PositionERKNSt4__Cr6vectorINSC_7variantIJNS1_15SupportsHandlesINS1_26TabCollectionHandleFactoryEE6HandleENSF_INS1_29SessionMappedTabHandleFactoryEE6HandleEEEENSC_9allocatorISM_EEEEEJS9_SP_EQsr3stdE9invocableITL0__PT_DpRKTL0_0_EEEvSV_DpRKT0_ ./gen/third_party/libc++/src/include/__type_traits/invoke.h:90:27
    #10 0x5fa41aaa5888 in base::internal::Invoker<base::internal::FunctorTraits<tabs::TabCollection::NotifyOnChildrenRemoved(base::PassKey<tabs::TabCollection>, tabs::TabCollection::Position const&, std::__Cr::vector<std::__Cr::variant<tabs::SupportsHandles<tabs::TabCollectionHandleFactory>::Handle, tabs::SupportsHandles<tabs::SessionMappedTabHandleFactory>::Handle>, std::__Cr::allocator<std::__Cr::variant<tabs::SupportsHandles<tabs::TabCollectionHandleFactory>::Handle, tabs::SupportsHandles<tabs::SessionMappedTabHandleFactory>::Handle> > > const&, tabs::TabCollection*)::$_0&&, tabs::TabCollection::Position&&, std::__Cr::reference_wrapper<base::ObserverList<tabs::TabCollectionObserver, false, (base::ObserverListReentrancyPolicy)1, base::internal::CheckedObserverAdapter> >&&, std::__Cr::vector<std::__Cr::variant<tabs::SupportsHandles<tabs::TabCollectionHandleFactory>::Handle, tabs::SupportsHandles<tabs::SessionMappedTabHandleFactory>::Handle>, std::__Cr::allocator<std::__Cr::variant<tabs::SupportsHandles<tabs::TabCollectionHandleFactory>::Handle, tabs::SupportsHandles<tabs::SessionMappedTabHandleFactory>::Handle> > >&&>, base::internal::BindState<false, false, false, tabs::TabCollection::NotifyOnChildrenRemoved(base::PassKey<tabs::TabCollection>, tabs::TabCollection::Position const&, std::__Cr::vector<std::__Cr::variant<tabs::SupportsHandles<tabs::TabCollectionHandleFactory>::Handle, tabs::SupportsHandles<tabs::SessionMappedTabHandleFactory>::Handle>, std::__Cr::allocator<std::__Cr::variant<tabs::SupportsHandles<tabs::TabCollectionHandleFactory>::Handle, tabs::SupportsHandles<tabs::SessionMappedTabHandleFactory>::Handle> > > const&, tabs::TabCollection*)::$_0, tabs::TabCollection::Position, base::internal::UnretainedRefWrapper<base::ObserverList<tabs::TabCollectionObserver, false, (base::ObserverListReentrancyPolicy)1, base::internal::CheckedObserverAdapter>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, std::__Cr::vector<std::__Cr::variant<tabs::SupportsHandles<tabs::TabCollectionHandleFactory>::Handle, tabs::SupportsHandles<tabs::SessionMappedTabHandleFactory>::Handle>, std::__Cr::allocator<std::__Cr::variant<tabs::SupportsHandles<tabs::TabCollectionHandleFactory>::Handle, tabs::SupportsHandles<tabs::SessionMappedTabHandleFactory>::Handle> > > >, void ()>::RunOnce(base::internal::BindStateBase*) ./../../components/tabs/impl/tab_collection.cc:419:21
    #11 0x5fa41aa9b607 in tabs::TabCollection::DispatchPendingNotifications() ./../../base/functional/callback.h:155:12
    #12 0x5fa41f297b48 in TabStripModel::CompleteModelUpdateTransaction() ./../../chrome/browser/ui/tabs/tab_strip_model.cc:4843:19
    #13 0x5fa41f2c622e in TabStripModel::TabGroupStateChanged(int, tabs::TabInterface*, std::__Cr::optional<tab_groups::TabGroupId>, std::__Cr::optional<tab_groups::TabGroupId>) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:4795:7
    #14 0x5fa41f29b163 in TabStripModel::RemoveTabFromIndexImpl(int, tabs::TabInterface::DetachReason) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:4650:5
    #15 0x5fa41f28f97c in TabStripModel::DetachTabImpl(int, int, bool, TabRemovedReason, tabs::TabInterface::DetachReason) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:940:7
    #16 0x5fa41f2d80bf in TabStripModel::CloseWebContentses(base::span<content::WebContents* const, 18446744073709551615ul, content::WebContents* const*>, unsigned int, TabStripModel::DetachNotifications*) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:3903:15
    #17 0x5fa41f2a78e1 in TabStripModel::CloseTabs(base::span<content::WebContents* const, 18446744073709551615ul, content::WebContents* const*>, unsigned int) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:3744:7
    #18 0x5fa41f2a97f9 in TabStripModel::CloseWebContentsAt(int, unsigned int) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:1311:3
    #19 0x5fa43b5071b5 in chrome::CloseWebContents(Browser*, content::WebContents*, bool) ./../../chrome/browser/ui/browser_tabstrip.cc:123:31
    #20 0x5fa418c6cc4a in content::WebContentsImpl::Close() ./../../content/browser/web_contents/web_contents_impl.cc:9462:16
    #21 0x5fa41833c82d in content::RenderFrameHostImpl::ClosePageIgnoringUnloadEvents(content::RenderFrameHostImpl::ClosePageSource, base::RepeatingCallback<void ()>) ./../../content/browser/renderer_host/render_frame_host_impl.cc:7588:14
    #22 0x5fa41833c484 in content::RenderFrameHostImpl::RequestClose() ./../../content/browser/renderer_host/render_frame_host_impl.cc:7452:3
    #23 0x5fa41008a898 in blink::mojom::LocalMainFrameHostStubDispatch::Accept(blink::mojom::LocalMainFrameHost*, mojo::Message*) ./gen/third_party/blink/public/mojom/frame/frame.mojom.cc:0:0
    #24 0x5fa422cab3e9 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085:54
    #25 0x5fa422cc9123 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:51:24
    #26 0x5fa422cb1893 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #27 0x5fa426be1d1d in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ./../../ipc/ipc_mojo_bootstrap.cc:1199:24
    #28 0x5fa426be4191 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:740:12
    #29 0x5fa422ee9b56 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/functional/callback.h:155:12

previously allocated by thread T0 (chrome) here:
    #0 0x5fa40b8893fd in operator new(unsigned long) ??:0:0
    #1 0x5fa41fa0ac7f in VerticalTabDragHandlerImpl::GetOrCreateSlotViewForNode(TabCollectionNode&) ./../../ui/views/view.h:307:3
    #2 0x5fa41fa092a6 in VerticalTabDragHandlerImpl::GetDragInitDataForGroupHeaderDrag(TabCollectionNode&) ./../../chrome/browser/ui/views/tabs/vertical/vertical_tab_drag_handler.cc:215:41
    #3 0x5fa41fa078f0 in VerticalTabDragHandlerImpl::InitializeDrag(TabCollectionNode&, ui::MouseEvent const&) ./../../chrome/browser/ui/views/tabs/vertical/vertical_tab_drag_handler.cc:126:24
    #4 0x5fa41fa2a534 in non-virtual thunk to VerticalTabGroupView::InitHeaderDrag(ui::MouseEvent const&) ./../../chrome/browser/ui/views/tabs/vertical/vertical_tab_group_view.cc:451:20
    #5 0x5fa41fa1e8d8 in VerticalTabGroupHeaderView::OnMousePressed(ui::MouseEvent const&) ./../../chrome/browser/ui/views/tabs/vertical/vertical_tab_group_header_view.cc:201:14
    #6 0x5fa42b0367da in views::View::ProcessMousePressed(ui::MouseEvent const&) ./../../ui/views/view.cc:3809:23
    #7 0x5fa42b036164 in views::View::OnMouseEvent(ui::MouseEvent*) ./../../ui/views/view.cc:1749:11
    #8 0x5fa4267898ba in ui::EventDispatcher::DispatchEvent(ui::EventHandler*, ui::Event*) ./../../ui/events/event_dispatcher.cc:189:12
    #9 0x5fa426788335 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ./../../ui/events/event_dispatcher.cc:138:5
    #10 0x5fa42678794d in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ./../../ui/events/event_dispatcher.cc:84:14
    #11 0x5fa426787407 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ./../../ui/events/event_dispatcher.cc:56:15
    #12 0x5fa42b070ce1 in views::internal::RootView::OnMousePressed(ui::MouseEvent const&) ./../../ui/views/widget/root_view.cc:567:9
    #13 0x5fa42b09ee38 in views::Widget::OnMouseEvent(ui::MouseEvent*) ./../../ui/views/widget/widget.cc:2143:35
    #14 0x5fa42b15a03a in views::DesktopNativeWidgetAura::OnMouseEvent(ui::MouseEvent*) ./../../ui/views/widget/desktop_aura/desktop_native_widget_aura.cc:1445:30
    #15 0x5fa4267898ba in ui::EventDispatcher::DispatchEvent(ui::EventHandler*, ui::Event*) ./../../ui/events/event_dispatcher.cc:189:12
    #16 0x5fa426788335 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ./../../ui/events/event_dispatcher.cc:138:5
    #17 0x5fa42678794d in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ./../../ui/events/event_dispatcher.cc:84:14
    #18 0x5fa426787407 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ./../../ui/events/event_dispatcher.cc:56:15
    #19 0x5fa42a28181b in ui::EventProcessor::OnEventFromSource(ui::Event*) ./../../ui/events/event_processor.cc:72:19
    #20 0x5fa42678ff5d in ui::EventSource::DeliverEventToSink(ui::Event*) ./../../ui/events/event_source.cc:119:16
    #21 0x5fa42678f5be in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) ./../../ui/events/event_source.cc:134:12
    #22 0x5fa42b176939 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event*) ./../../ui/aura/window_tree_host_platform.cc:300:38
    #23 0x5fa42b170f0b in views::DesktopWindowTreeHostLinux::DispatchEvent(ui::Event*) ./../../ui/views/widget/desktop_aura/desktop_window_tree_host_linux.cc:250:29
    #24 0x5fa40dfa8748 in base::internal::Invoker<base::internal::FunctorTraits<void (ui::PlatformWindowDelegate::*&&)(ui::Event*), ui::PlatformWindowDelegate*>, base::internal::BindState<true, true, false, void (ui::PlatformWindowDelegate::*)(ui::Event*), base::internal::UnretainedWrapper<ui::PlatformWindowDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, void (ui::Event*)>::RunOnce(base::internal::BindStateBase*, ui::Event*) ./../../base/functional/bind_internal.h:740:12
    #25 0x5fa4267a37b8 in ui::DispatchEventFromNativeUiEvent(ui::Event* const&, base::OnceCallback<void (ui::Event*)>) ./../../base/functional/callback.h:155:12
    #26 0x5fa40e09071e in ui::X11Window::DispatchUiEvent(ui::Event*, x11::Event const&) ./../../ui/ozone/platform/x11/x11_window.cc:1421:3
    #27 0x5fa40e08fc03 in ui::X11Window::DispatchEvent(ui::Event* const&) ./../../ui/ozone/platform/x11/x11_window.cc:1372:3
    #28 0x5fa40e0909c2 in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event* const&) ./../../ui/ozone/platform/x11/x11_window.cc:0:0
    #29 0x5fa4266e4ac5 in ui::PlatformEventSource::DispatchEvent(ui::Event*) ./../../ui/events/platform/platform_event_source.cc:93:29

SUMMARY: AddressSanitizer: heap-use-after-free (/home/lenovo/Desktop/linux-release_asan-linux-release-1592093/chrome+0x24fcf318) (BuildId: 148f6e77389e8ab2)
Shadow bytes around the buggy address:
  0x724cdd1cf200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x724cdd1cf280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x724cdd1cf300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x724cdd1cf380: fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x724cdd1cf400: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
=>0x724cdd1cf480:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x724cdd1cf500: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x724cdd1cf580: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x724cdd1cf600: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x724cdd1cf680: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x724cdd1cf700: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==36361==ADDITIONAL INFO

==36361==Note: Please include this section with the ASan report.
Task trace:
    #0 0x5fa426bdb31b in IPC::ChannelAssociatedGroupController::Accept(mojo::Message*) ./../../ipc/ipc_mojo_bootstrap.cc:1138:13
    #1 0x5fa423b36f73 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) ./../../mojo/public/cpp/system/simple_watcher.cc:103:13


Command line: `./chrome -remote-debugging-port=9222 --no-sandbox --user-data-dir=/home/lenovo/Downloads/chrome-profile --flag-switches-begin --enable-features=VerticalTabs --flag-switches-end --ozone-platform=x11 --file-url-path-alias=/gen=/home/lenovo/Desktop/linux-release_asan-linux-release-1592093/gen`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.


### ch...@gmail.com (2026-03-04)

deleted

### me...@google.com (2026-03-05)

Thanks for the report. I can repro on stable.

tluk: Could you please take a look?

### ch...@google.com (2026-03-05)

Setting milestone because of s0/s1 severity.

### ch...@gmail.com (2026-03-13)

Any update on this bug? Thanks!

### ch...@gmail.com (2026-03-14)

This issue appears to have been fixed by https://chromium-review.googlesource.com/c/chromium/src/+/7662841, which also addresses a buffer overflow tracked in issue 490650365.

### ch...@gmail.com (2026-03-20)

tluk, can you confirm whether this has been fixed?

### ch...@google.com (2026-03-20)

tluk: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### tl...@chromium.org (2026-03-29)

Can confirm that I was able to repro on Linux stable 146.0.7680.164 and can confirm it appears to have been fixed as of [crrev.com/c/7662841](https://crrev.com/c/7662841).

### ch...@google.com (2026-03-29)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@gmail.com (2026-04-01)

Thanks for the verification! I think it would be helpful to add the corresponding CL to the “Fixed By Code Changes” field.

### tl...@google.com (2026-04-06)

Sure, done

### ch...@google.com (2026-04-07)

This is sufficiently serious that it should be merged to M146. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M146. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

This is sufficiently serious that it should be merged to M147. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M147. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

### ch...@google.com (2026-04-07)

**M146** merge request created. **Please update [crbug/500246573](https://crbug.com/500246573) to have this merge reviewed.**

### ch...@google.com (2026-04-07)

**M147** merge request created. **Please update [crbug/500245829](https://crbug.com/500245829) to have this merge reviewed.**

### tl...@google.com (2026-04-08)

The linked fix was already merged into 147 and there is no experiment running in 146 so the merges above are unnecessary (will proceed to close)

### aj...@google.com (2026-05-20)

S2 requires user interaction

### sp...@google.com (2026-05-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline. Moderately mitigated (non-sandboxed) 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/489109720)*
