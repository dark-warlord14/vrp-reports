# Heap-use-after-free in TabHoverCardController::UpdateHoverCard

| Field | Value |
|-------|-------|
| **Issue ID** | [495269751](https://issues.chromium.org/issues/495269751) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | UI>Browser>TopChrome>TabStrip |
| **Platforms** | Linux, ChromeOS |
| **Chrome Version** | 148.0.7750.0 |
| **Reporter** | ch...@gmail.com |
| **Assignee** | do...@google.com |
| **Created** | 2026-03-23 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

- Enable Vertical Tabs via chrome://flags/#vertical-tabs and restart the browser.

1. Open the provided testcase.
2. Click the button to open a new tab.
3. Right-click the newly opened tab and select “Add tab to new split view”.
4. Move the cursor over the tab in the right split view and keep it stationary until the hover card is triggered. Do not move the cursor afterward and wait for the browser to crash.

I believe this issue demonstrates a security-relevant use-after-free, similar in nature to previously reported vertical tabs issues (e.g. 489109720, 490588145, 490650365), where tab lifecycle inconsistencies led to dangling View references.

# Problem Description

The browser crashes due to a use-after-free in TabHoverCardController::UpdateHoverCard

# Summary

Heap-use-after-free in TabHoverCardController::UpdateHoverCard

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [testcase.html](attachments/testcase.html) (text/html, 490 B)
- [simplescreenrecorder-2026-03-23_17.25.54.mp4](attachments/simplescreenrecorder-2026-03-23_17.25.54.mp4) (video/mp4, 1.0 MB)
- [simplescreenrecorder-2026-03-24_23.11.00.mp4](attachments/simplescreenrecorder-2026-03-24_23.11.00.mp4) (video/mp4, 670.2 KB)

## Timeline

### ch...@gmail.com (2026-03-23)

=================================================================
==19928==ERROR: AddressSanitizer: heap-use-after-free on address 0x72d8f22731a8 at pc 0x5f8b28f24f4e bp 0x7ffd0c01b570 sp 0x7ffd0c01b568
READ of size 8 at 0x72d8f22731a8 thread T0 (chrome)
==19928==WARNING: invalid path to external symbolizer!
==19928==WARNING: Failed to use and restart external symbolizer!
    #0 0x5f8b28f24f4d in views::View::RemoveObserver(views::ViewObserver*) ./gen/third_party/libc++/src/include/__vector/vector.h:349:57
    #1 0x5f8b3a554053 in TabHoverCardController::UpdateHoverCard(HoverCardAnchorTarget*, TabSlotController::HoverCardUpdateType) ./../../base/scoped_observation_traits.h:74:13
    #2 0x5f8b2810f85f in aura::EventObserverAdapter::OnEvent(ui::Event*) ./../../ui/aura/env.cc:80:18
    #3 0x5f8b2461399a in ui::EventDispatcher::DispatchEvent(ui::EventHandler*, ui::Event*) ./../../ui/events/event_dispatcher.cc:189:12
    #4 0x5f8b246133db in ui::EventDispatcher::DispatchEventToEventHandlers(std::__Cr::vector<base::raw_ptr<ui::EventHandler, (partition_alloc::internal::RawPtrTraits)1>, std::__Cr::allocator<base::raw_ptr<ui::EventHandler, (partition_alloc::internal::RawPtrTraits)1> > >*, ui::Event*) ./../../ui/events/event_dispatcher.cc:176:7
    #5 0x5f8b24612199 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ./../../ui/events/event_dispatcher.cc:124:3
    #6 0x5f8b24611a2d in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ./../../ui/events/event_dispatcher.cc:84:14
    #7 0x5f8b246114e7 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ./../../ui/events/event_dispatcher.cc:56:15
    #8 0x5f8b2815cb7b in ui::EventProcessor::OnEventFromSource(ui::Event*) ./../../ui/events/event_processor.cc:72:19
    #9 0x5f8b2461a03d in ui::EventSource::DeliverEventToSink(ui::Event*) ./../../ui/events/event_source.cc:119:16
    #10 0x5f8b2461969e in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) ./../../ui/events/event_source.cc:134:12
    #11 0x5f8b2905f829 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event*) ./../../ui/aura/window_tree_host_platform.cc:300:38
    #12 0x5f8b29059dfb in views::DesktopWindowTreeHostLinux::DispatchEvent(ui::Event*) ./../../ui/views/widget/desktop_aura/desktop_window_tree_host_linux.cc:250:29
    #13 0x5f8b0ad7f958 in base::internal::Invoker<base::internal::FunctorTraits<void (ui::PlatformWindowDelegate::*&&)(ui::Event*), ui::PlatformWindowDelegate*>, base::internal::BindState<true, true, false, void (ui::PlatformWindowDelegate::*)(ui::Event*), base::internal::UnretainedWrapper<ui::PlatformWindowDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, void (ui::Event*)>::RunOnce(base::internal::BindStateBase*, ui::Event*) ./../../base/functional/bind_internal.h:740:12
    #14 0x5f8b2462d898 in ui::DispatchEventFromNativeUiEvent(ui::Event* const&, base::OnceCallback<void (ui::Event*)>) ./../../base/functional/callback.h:155:12
    #15 0x5f8b0ae69b3e in ui::X11Window::DispatchUiEvent(ui::Event*, x11::Event const&) ./../../ui/ozone/platform/x11/x11_window.cc:1421:3
    #16 0x5f8b0ae69023 in ui::X11Window::DispatchEvent(ui::Event* const&) ./../../ui/ozone/platform/x11/x11_window.cc:1372:3
    #17 0x5f8b0ae69de2 in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event* const&) ./../../ui/ozone/platform/x11/x11_window.cc:0:0
    #18 0x5f8b24544ce5 in ui::PlatformEventSource::DispatchEvent(ui::Event*) ./../../ui/events/platform/platform_event_source.cc:93:29
    #19 0x5f8b24caf624 in ui::X11EventSource::OnEvent(x11::Event const&) ./../../ui/events/platform/x11/x11_event_source.cc:301:5
    #20 0x5f8b2455d80b in _ZN4base12ObserverListIN3x1113EventObserverELb0ELNS_28ObserverListReentrancyPolicyE1ENS_8internal24UncheckedObserverAdapterILN15partition_alloc8internal12RawPtrTraitsE1ELb0EEEE6NotifyIMS2_FvRKNS1_5EventEEJSC_EQsr3stdE9invocableITL0__PT_DpRKTL0_0_EEEvSI_DpRKT0_ ./gen/third_party/libc++/src/include/__type_traits/invoke.h:90:27
    #21 0x5f8b2455bc1f in x11::Connection::ProcessNextEvent() ./../../ui/gfx/x/connection.cc:588:20
    #22 0x5f8b2455b152 in x11::Connection::Dispatch() ./../../ui/gfx/x/connection.cc:0:0
    #23 0x5f8b24cbced8 in ui::(anonymous namespace)::XSourceDispatch(_GSource*, int (*)(void*), void*) ./../../ui/events/platform/x11/x11_event_watcher_glib.cc:57:15
    #24 0x7558f4fd745d in g_source_query_unix_fd ??:?
    #25 0x7558f5036976 in g_io_channel_new_file ??:?
    #26 0x7558f4fd6a22 in g_main_context_iteration ??:0:0
    #27 0x5f8b20f598f3 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_glib.cc:770:30
    #28 0x5f8b20dad437 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #29 0x5f8b20cadc30 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:135:14
    #30 0x5f8b14900b6c in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser_main_loop.cc:1106:18
    #31 0x5f8b1490922c in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser_main_runner_impl.cc:151:15
    #32 0x5f8b148f748c in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser_main.cc:32:28
    #33 0x5f8b1c95be0f in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:696:10
    #34 0x5f8b1c95fe00 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content_main_runner_impl.cc:1320:10
    #35 0x5f8b1c95f28a in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1150:12
    #36 0x5f8b1c958c31 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:358:36
    #37 0x5f8b1c95922c in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:371:10
    #38 0x5f8b09235b39 in ChromeMain ./../../chrome/app/chrome_main.cc:191:12
    #39 0x7558f3a2a1c9 in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #40 0x7558f3a2a28a in __libc_start_main ./csu/../csu/libc-start.c:360:3
    #41 0x5f8b0915b029 in _start ??:0:0

0x72d8f22731a8 is located 296 bytes inside of 816-byte region [0x72d8f2273080,0x72d8f22733b0)
freed by thread T0 (chrome) here:
    #0 0x5f8b09234c3d in operator delete(void*) ??:0:0
    #1 0x5f8b1d7f3fdc in TabCollectionAnimatingLayoutManager::RemoveNonAnimatingPendingDeleteViews() ./gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #2 0x5f8b1d7f25ff in TabCollectionAnimatingLayoutManager::LayoutImpl() ./../../chrome/browser/ui/views/tabs/vertical/tab_collection_animating_layout_manager.cc:223:5
    #3 0x5f8b28ec2f97 in views::LayoutManagerBase::Layout(views::View*) ./../../ui/views/layout/layout_manager_base.cc:116:3
    #4 0x5f8b28f13518 in views::View::Layout(base::NonCopyablePassKey<views::View>) ./../../ui/views/view.cc:953:25
    #5 0x5f8b28f08532 in views::View::LayoutImmediately() ./../../ui/views/view.cc:3786:3
    #6 0x5f8b28f1390c in views::View::Layout(base::NonCopyablePassKey<views::View>) ./../../ui/views/view.cc:969:14
    #7 0x5f8b28f08532 in views::View::LayoutImmediately() ./../../ui/views/view.cc:3786:3
    #8 0x5f8b28f067c4 in views::View::SetBoundsRect(gfx::Rect const&) ./../../ui/views/view.cc:412:7
    #9 0x5f8b28ded629 in views::ScrollView::Layout(base::NonCopyablePassKey<views::View>) ./../../ui/views/controls/scroll_view.cc:836:23
    #10 0x5f8b28f08532 in views::View::LayoutImmediately() ./../../ui/views/view.cc:3786:3
    #11 0x5f8b28f1390c in views::View::Layout(base::NonCopyablePassKey<views::View>) ./../../ui/views/view.cc:969:14
    #12 0x5f8b28f08532 in views::View::LayoutImmediately() ./../../ui/views/view.cc:3786:3
    #13 0x5f8b28ec50fe in views::LayoutManagerBase::ApplyLayout(views::ProposedLayout const&) ./../../ui/views/layout/layout_manager_base.cc:239:21
    #14 0x5f8b28ec498e in views::LayoutManagerBase::LayoutImpl() ./../../ui/views/layout/layout_manager_base.cc:199:3
    #15 0x5f8b28ec2f97 in views::LayoutManagerBase::Layout(views::View*) ./../../ui/views/layout/layout_manager_base.cc:116:3
    #16 0x5f8b28f13518 in views::View::Layout(base::NonCopyablePassKey<views::View>) ./../../ui/views/view.cc:953:25
    #17 0x5f8b39fce6c4 in VerticalTabStripRegionView::Layout(base::NonCopyablePassKey<views::View>) ./../../ui/views/view.h:2018:38
    #18 0x5f8b28f08532 in views::View::LayoutImmediately() ./../../ui/views/view.cc:3786:3
    #19 0x5f8b28f067c4 in views::View::SetBoundsRect(gfx::Rect const&) ./../../ui/views/view.cc:412:7
    #20 0x5f8b39f54fad in BrowserViewLayoutImpl::ProposedLayout::ApplyLayout(views::View*, base::FunctionRef<void (views::View*, bool)>) && ./../../chrome/browser/ui/views/frame/layout/browser_view_layout_impl.cc:89:14
    #21 0x5f8b39f56266 in BrowserViewLayoutImpl::Layout(views::View*) ./../../chrome/browser/ui/views/frame/layout/browser_view_layout_impl.cc:213:35
    #22 0x5f8b28f13518 in views::View::Layout(base::NonCopyablePassKey<views::View>) ./../../ui/views/view.cc:953:25
    #23 0x5f8b39e48917 in BrowserView::Layout(base::NonCopyablePassKey<views::View>) ./../../ui/views/view.h:2018:38
    #24 0x5f8b28f08532 in views::View::LayoutImmediately() ./../../ui/views/view.cc:3786:3
    #25 0x5f8b28f067c4 in views::View::SetBoundsRect(gfx::Rect const&) ./../../ui/views/view.cc:412:7
    #26 0x5f8b28fc71a2 in views::FrameView::Layout(base::NonCopyablePassKey<views::View>) ./../../ui/views/window/frame_view.cc:124:16
    #27 0x5f8b39e1486e in BrowserFrameView::Layout(base::NonCopyablePassKey<views::View>) ./../../ui/views/view.h:2018:38
    #28 0x5f8b3a9c06a6 in BrowserFrameViewLinuxNative::Layout(base::NonCopyablePassKey<views::View>) ./../../ui/views/view.h:2018:38
    #29 0x5f8b28f08532 in views::View::LayoutImmediately() ./../../ui/views/view.cc:3786:3

previously allocated by thread T0 (chrome) here:
    #0 0x5f8b092343fd in operator new(unsigned long) ??:0:0
    #1 0x5f8b1d806309 in TabCollectionNode::CreateViewForNode(TabCollectionNode*) ./../../ui/views/view.h:306:3
    #2 0x5f8b1d80782e in TabCollectionNode::AddNewChild(base::PassKey<TabCollectionNode>, std::__Cr::variant<tabs::TabInterface const*, tabs::TabCollection const*>, unsigned long, bool) ./../../chrome/browser/ui/views/tabs/vertical/tab_collection_node.cc:382:20
    #3 0x5f8b1d7e6154 in RootTabCollectionNode::OnChildrenAdded(tabs::TabCollection::Position const&, std::__Cr::vector<std::__Cr::variant<tabs::SupportsHandles<tabs::TabCollectionHandleFactory>::Handle, tabs::SupportsHandles<tabs::SessionMappedTabHandleFactory>::Handle>, std::__Cr::allocator<std::__Cr::variant<tabs::SupportsHandles<tabs::TabCollectionHandleFactory>::Handle, tabs::SupportsHandles<tabs::SessionMappedTabHandleFactory>::Handle> > > const&, bool) ./../../chrome/browser/ui/views/tabs/vertical/root_tab_collection_node.cc:96:11
    #4 0x5f8b186be8e1 in _ZN4base12ObserverListIN4tabs21TabCollectionObserverELb0ELNS_28ObserverListReentrancyPolicyE1ENS_8internal22CheckedObserverAdapterEE6NotifyIMS2_FvRKNS1_13TabCollection8PositionERKNSt4__Cr6vectorINSC_7variantIJNS1_15SupportsHandlesINS1_26TabCollectionHandleFactoryEE6HandleENSF_INS1_29SessionMappedTabHandleFactoryEE6HandleEEEENSC_9allocatorISM_EEEEbEJS9_SP_bEQsr3stdE9invocableITL0__PT_DpRKTL0_0_EEEvSV_DpRKT0_ ./gen/third_party/libc++/src/include/__type_traits/invoke.h:90:27
    #5 0x5f8b186c390b in base::internal::Invoker<base::internal::FunctorTraits<tabs::TabCollection::NotifyOnChildrenAdded(base::PassKey<tabs::TabCollection>, std::__Cr::vector<std::__Cr::variant<tabs::SupportsHandles<tabs::TabCollectionHandleFactory>::Handle, tabs::SupportsHandles<tabs::SessionMappedTabHandleFactory>::Handle>, std::__Cr::allocator<std::__Cr::variant<tabs::SupportsHandles<tabs::TabCollectionHandleFactory>::Handle, tabs::SupportsHandles<tabs::SessionMappedTabHandleFactory>::Handle> > > const&, tabs::TabCollection::Position const&, tabs::TabCollection*, bool)::$_0&&, std::__Cr::reference_wrapper<base::ObserverList<tabs::TabCollectionObserver, false, (base::ObserverListReentrancyPolicy)1, base::internal::CheckedObserverAdapter> >&&, tabs::TabCollection::Position&&, std::__Cr::vector<std::__Cr::variant<tabs::SupportsHandles<tabs::TabCollectionHandleFactory>::Handle, tabs::SupportsHandles<tabs::SessionMappedTabHandleFactory>::Handle>, std::__Cr::allocator<std::__Cr::variant<tabs::SupportsHandles<tabs::TabCollectionHandleFactory>::Handle, tabs::SupportsHandles<tabs::SessionMappedTabHandleFactory>::Handle> > >&&, bool&&>, base::internal::BindState<false, false, false, tabs::TabCollection::NotifyOnChildrenAdded(base::PassKey<tabs::TabCollection>, std::__Cr::vector<std::__Cr::variant<tabs::SupportsHandles<tabs::TabCollectionHandleFactory>::Handle, tabs::SupportsHandles<tabs::SessionMappedTabHandleFactory>::Handle>, std::__Cr::allocator<std::__Cr::variant<tabs::SupportsHandles<tabs::TabCollectionHandleFactory>::Handle, tabs::SupportsHandles<tabs::SessionMappedTabHandleFactory>::Handle> > > const&, tabs::TabCollection::Position const&, tabs::TabCollection*, bool)::$_0, base::internal::UnretainedRefWrapper<base::ObserverList<tabs::TabCollectionObserver, false, (base::ObserverListReentrancyPolicy)1, base::internal::CheckedObserverAdapter>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, tabs::TabCollection::Position, std::__Cr::vector<std::__Cr::variant<tabs::SupportsHandles<tabs::TabCollectionHandleFactory>::Handle, tabs::SupportsHandles<tabs::SessionMappedTabHandleFactory>::Handle>, std::__Cr::allocator<std::__Cr::variant<tabs::SupportsHandles<tabs::TabCollectionHandleFactory>::Handle, tabs::SupportsHandles<tabs::SessionMappedTabHandleFactory>::Handle> > >, bool>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../components/tabs/impl/tab_collection.cc:388:21
    #6 0x5f8b186b9fb7 in tabs::TabCollection::DispatchPendingNotifications() ./../../base/functional/callback.h:155:12
    #7 0x5f8b1d083518 in TabStripModel::CompleteModelUpdateTransaction() ./../../chrome/browser/ui/tabs/tab_strip_model.cc:4749:19
    #8 0x5f8b1d0a6c62 in TabStripModel::AddToSplitImpl(split_tabs::SplitTabId, std::__Cr::vector<int, std::__Cr::allocator<int> > const&, int, split_tabs::SplitTabVisualData, SplitTabChange::SplitTabAddReason) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:4140:3
    #9 0x5f8b1d0a5522 in TabStripModel::AddToNewSplit(std::__Cr::vector<int, std::__Cr::allocator<int> >, split_tabs::SplitTabVisualData, split_tabs::SplitTabCreatedSource) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:1949:3
    #10 0x5f8b39482ee2 in chrome::NewSplitTab(BrowserWindowInterface*, split_tabs::SplitTabCreatedSource) ./../../chrome/browser/ui/browser_commands.cc:1467:20
    #11 0x5f8b394b8b59 in chrome::BrowserTabStripModelDelegate::NewSplitTab(std::__Cr::vector<int, std::__Cr::allocator<int> >, split_tabs::SplitTabCreatedSource) ./../../chrome/browser/ui/browser_tab_strip_model_delegate.cc:337:5
    #12 0x5f8b1d0d9648 in void base::internal::Invoker<base::internal::FunctorTraits<void (TabStripModelDelegate::*&&)(std::__Cr::vector<int, std::__Cr::allocator<int> >, split_tabs::SplitTabCreatedSource), TabStripModelDelegate*, std::__Cr::vector<int, std::__Cr::allocator<int> >&&, split_tabs::SplitTabCreatedSource&&>, base::internal::BindState<true, true, false, void (TabStripModelDelegate::*)(std::__Cr::vector<int, std::__Cr::allocator<int> >, split_tabs::SplitTabCreatedSource), base::internal::UnretainedWrapper<TabStripModelDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, std::__Cr::vector<int, std::__Cr::allocator<int> >, split_tabs::SplitTabCreatedSource>, void ()>::RunImpl<void (TabStripModelDelegate::*)(std::__Cr::vector<int, std::__Cr::allocator<int> >, split_tabs::SplitTabCreatedSource), std::__Cr::tuple<base::internal::UnretainedWrapper<TabStripModelDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, std::__Cr::vector<int, std::__Cr::allocator<int> >, split_tabs::SplitTabCreatedSource>, 0ul, 1ul, 2ul>(void (TabStripModelDelegate::*&&)(std::__Cr::vector<int, std::__Cr::allocator<int> >, split_tabs::SplitTabCreatedSource), std::__Cr::tuple<base::internal::UnretainedWrapper<TabStripModelDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, std::__Cr::vector<int, std::__Cr::allocator<int> >, split_tabs::SplitTabCreatedSource>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul>) ./../../base/functional/bind_internal.h:740:12
    #13 0x5f8b15d928ff in base::OnceCallback<void ()>::Run() && ./../../base/functional/callback.h:155:12
    #14 0x5f8b1d0b718f in TabStripModel::ExecuteContextMenuCommand(int, TabStripModel::ContextMenuCommand) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:2755:27
    #15 0x5f8b248adcf5 in ui::SimpleMenuModel::ActivatedAt(unsigned long, int) ./../../ui/menus/simple_menu_model.cc:606:14
    #16 0x5f8b28daa411 in views::MenuModelAdapter::ExecuteCommand(int, int) ./../../ui/views/controls/menu/menu_model_adapter.cc:191:10
    #17 0x5f8b28db0491 in views::internal::MenuRunnerImpl::OnMenuClosed(views::internal::MenuControllerDelegate::NotifyType, views::MenuItemView*, int) ./../../ui/views/controls/menu/menu_runner_impl.cc:255:29
    #18 0x5f8b28d6231e in views::MenuController::ExitMenu() ./../../ui/views/controls/menu/menu_controller.cc:3553:13
    #19 0x5f8b28d68733 in views::MenuController::Accept(views::MenuItemView*, int) ./../../ui/views/controls/menu/menu_controller.cc:2183:3
    #20 0x5f8b28d6792f in views::MenuController::OnMouseReleased(views::SubmenuView*, ui::MouseEvent const&) ./../../ui/views/controls/menu/menu_controller.cc:1027:7
    #21 0x5f8b28f85276 in views::Widget::OnMouseEvent(ui::MouseEvent*) ./../../ui/views/widget/widget.cc:2173:20
    #22 0x5f8b29042f5a in views::DesktopNativeWidgetAura::OnMouseEvent(ui::MouseEvent*) ./../../ui/views/widget/desktop_aura/desktop_native_widget_aura.cc:1445:30
    #23 0x5f8b2461399a in ui::EventDispatcher::DispatchEvent(ui::EventHandler*, ui::Event*) ./../../ui/events/event_dispatcher.cc:189:12
    #24 0x5f8b24612415 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ./../../ui/events/event_dispatcher.cc:138:5
    #25 0x5f8b24611a2d in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ./../../ui/events/event_dispatcher.cc:84:14
    #26 0x5f8b246114e7 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ./../../ui/events/event_dispatcher.cc:56:15
    #27 0x5f8b2815cb7b in ui::EventProcessor::OnEventFromSource(ui::Event*) ./../../ui/events/event_processor.cc:72:19
    #28 0x5f8b2461a03d in ui::EventSource::DeliverEventToSink(ui::Event*) ./../../ui/events/event_source.cc:119:16
    #29 0x5f8b2461969e in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) ./../../ui/events/event_source.cc:134:12

SUMMARY: AddressSanitizer: heap-use-after-free (/home/lenovo/Desktop/linux-release_asan-linux-release-1603225/chrome+0x30b2cf4d) (BuildId: ce334a9f13348faf)
Shadow bytes around the buggy address:
  0x72d8f2272f00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x72d8f2272f80: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x72d8f2273000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x72d8f2273080: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x72d8f2273100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x72d8f2273180: fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd
  0x72d8f2273200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x72d8f2273280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x72d8f2273300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x72d8f2273380: fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa fa
  0x72d8f2273400: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
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

==19928==ADDITIONAL INFO

==19928==Note: Please include this section with the ASan report.
Task trace:


Command line: `./chrome -remote-debugging-port=9222 --no-sandbox --js-flags=--expose-gc --autoplay-policy=no-user-gesture-required --user-data-dir=/home/lenovo/Downloads/chrome-profile4 --flag-switches-begin --flag-switches-end --ozone-platform=x11 --file-url-path-alias=/gen=/home/lenovo/Desktop/linux-release_asan-linux-release-1603225/gen`


MiraclePtr Status: MANUAL ANALYSIS REQUIRED
A pointer to the same region was extracted from a raw_ptr<T> object prior to this crash.
To determine the protection status, enable extraction warnings and check whether the raw_ptr<T> object can be destroyed or overwritten between the extraction and use.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.


### sk...@google.com (2026-03-23)

I was not able to reproduce, but will pass along to the team to take a look. Setting a provisional severity and FoundIn

### ag...@google.com (2026-03-23)

Steven, would you be able to look into this UAF and maybe loop in Dominic if it is related to other recent hovercard changes?

### do...@google.com (2026-03-23)

I think this is hover card related so I will take this one. but I cant seem to reproduce the issue with the same stack trace, instead I run into a CHECK failure in the bubble_slide_animator. The issue seems to be related to the TabHoverCardController::EventSniffer since UpdateHoverCard is being triggered from OnEvent, 

### ch...@google.com (2026-03-24)

Setting milestone because of s2 severity.

### ch...@google.com (2026-03-24)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### dx...@google.com (2026-03-24)

Project: chromium/src  

Branch:  main  

Author:  Dominic Austria [dominicaustria@google.com](mailto:dominicaustria@google.com)  

Link:    <https://chromium-review.googlesource.com/7696728>

[Vertical Tabs] Clean up hover card on vertical split tab view reset

---


Expand for full commit details
```
     
    Bug: 495269751 
    Change-Id: I262a316a4d4dc04011c2f3277b4787e7950baa08 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7696728 
    Reviewed-by: Eshwar Stalin <estalin@chromium.org> 
    Commit-Queue: Dominic Austria <dominicaustria@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1604364}

```

---

Files:

- M `chrome/browser/ui/views/tabs/vertical/vertical_split_tab_view.cc`

---

Hash: [bfd39f775b41e808b402c13f92dcaa9db26b0ea9](https://chromiumdash.appspot.com/commit/bfd39f775b41e808b402c13f92dcaa9db26b0ea9)  

Date: Tue Mar 24 20:48:16 2026


---

### ch...@gmail.com (2026-03-24)

Verified on Chromium 148.0.7753.0 (rev 1604390).
The use-after-free condition no longer reproduces under the original steps.
The fix appears effective - Thanks for the quick fix!

### ch...@google.com (2026-03-25)

Merge review required: M147 has already been cut for stable release.

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
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### do...@google.com (2026-03-25)

1. This is a heap-use-after-free security issue
2. https://chromium-review.git.corp.google.com/c/chromium/src/+/7696728
3. Yes
4. No
5. n/a
6. No verification required

### dr...@chromium.org (2026-03-26)

Given the low severity and trouble reproducing, we don't need to merge this from the security side.

### dr...@chromium.org (2026-03-26)

FYI if you simply close a security bug, our bots will automatically request the necessary merges.

### aj...@google.com (2026-04-06)

VRP category browser\_corrupt severity S2. Heap-use-after-free in browser process UI.

Comment created using go/buganizer-mcp-server

### sp...@google.com (2026-06-29)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Highly mitigated browser UAF


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/495269751)*
