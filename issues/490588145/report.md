# Heap-use-after-free in VerticalTabDragHandlerImpl::ContinueDrag

| Field | Value |
|-------|-------|
| **Issue ID** | [490588145](https://issues.chromium.org/issues/490588145) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>TopChrome>TabStrip |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 147.0.7725.0 |
| **Reporter** | ch...@gmail.com |
| **Assignee** | al...@google.com |
| **Created** | 2026-03-07 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

Note: Use Chrome in Vertical Tabs mode by enabling chrome://flags/#vertical-tabs

1. Open the testcase
2. Click the button
3. Start dragging the testcase tab out of the tab strip to create a separate window, but keep holding the drag without releasing the tab until the about:blank window closes.

==27679==ERROR: AddressSanitizer: heap-use-after-free on address 0x75a808d167a0 at pc 0x5676b233f3a4 bp 0x7ffdc3be33b0 sp 0x7ffdc3be33a8
READ of size 8 at 0x75a808d167a0 thread T0 (chrome)
==27679==WARNING: invalid path to external symbolizer!
==27679==WARNING: Failed to use and restart external symbolizer!
#0 0x5676b233f3a3 in VerticalTabDragHandlerImpl::ContinueDrag(views::View&, ui::MouseEvent const&) ./gen/third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:285:21
#1 0x5676bd9bd085 in views::View::ProcessMouseDragged(ui::MouseEvent\*) ./../../ui/views/view.cc:3851:9
#2 0x5676b90a9d7a in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:189:12
#3 0x5676b90a87f5 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:138:5
#4 0x5676b90a7e0d in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:84:14
#5 0x5676b90a78c7 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:56:15
#6 0x5676bd9f80c6 in views::internal::RootView::OnMouseDragged(ui::MouseEvent const&) ./../../ui/views/widget/root\_view.cc:614:9
#7 0x5676bda256fe in views::Widget::OnMouseEvent(ui::MouseEvent\*) ./../../ui/views/widget/widget.cc:2185:22
#8 0x5676bdae041a in views::DesktopNativeWidgetAura::OnMouseEvent(ui::MouseEvent\*) ./../../ui/views/widget/desktop\_aura/desktop\_native\_widget\_aura.cc:1445:30
#9 0x5676b90a9d7a in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:189:12
#10 0x5676b90a87f5 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:138:5
#11 0x5676b90a7e0d in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:84:14
#12 0x5676b90a78c7 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:56:15
#13 0x5676bcc02feb in ui::EventProcessor::OnEventFromSource(ui::Event\*) ./../../ui/events/event\_processor.cc:72:19
#14 0x5676b90b041d in ui::EventSource::DeliverEventToSink(ui::Event\*) ./../../ui/events/event\_source.cc:119:16
#15 0x5676b90afa7e in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const\*, ui::EventRewriter const\*) ./../../ui/events/event\_source.cc:134:12
#16 0x5676bdafcd19 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event\*) ./../../ui/aura/window\_tree\_host\_platform.cc:300:38
#17 0x5676bdaf72eb in views::DesktopWindowTreeHostLinux::DispatchEvent(ui::Event\*) ./../../ui/views/widget/desktop\_aura/desktop\_window\_tree\_host\_linux.cc:250:29
#18 0x56769fba99a8 in base::internal::Invoker<base::internal::FunctorTraits<void (ui::PlatformWindowDelegate::*&&)(ui::Event*), ui::PlatformWindowDelegate\*>, base::internal::BindState<true, true, false, void (ui::PlatformWindowDelegate::*)(ui::Event*), base::internal::UnretainedWrapper<ui::PlatformWindowDelegate, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0> >, void (ui::Event\*)>::RunOnce(base::internal::BindStateBase\*, ui::Event\*) ./../../base/functional/bind\_internal.h:740:12
#19 0x5676b90c3c78 in ui::DispatchEventFromNativeUiEvent(ui::Event\* const&, base::OnceCallback<void (ui::Event\*)>) ./../../base/functional/callback.h:155:12
#20 0x56769fc918ee in ui::X11Window::DispatchUiEvent(ui::Event\*, x11::Event const&) ./../../ui/ozone/platform/x11/x11\_window.cc:1421:3
#21 0x56769fc90dd3 in ui::X11Window::DispatchEvent(ui::Event\* const&) ./../../ui/ozone/platform/x11/x11\_window.cc:1372:3
#22 0x56769fc91b92 in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event\* const&) ./../../ui/ozone/platform/x11/x11\_window.cc:0:0
#23 0x5676b8fdcba5 in ui::PlatformEventSource::DispatchEvent(ui::Event\*) ./../../ui/events/platform/platform\_event\_source.cc:93:29
#24 0x5676b973be44 in ui::X11EventSource::OnEvent(x11::Event const&) ./../../ui/events/platform/x11/x11\_event\_source.cc:301:5
#25 0x5676b8ff56cb in *ZN4base12ObserverListIN3x1113EventObserverELb0ELNS\_28ObserverListReentrancyPolicyE1ENS\_8internal24UncheckedObserverAdapterILN15partition\_alloc8internal12RawPtrTraitsE1ELb0EEEE6NotifyIMS2\_FvRKNS1\_5EventEEJSC\_EQsr3stdE9invocableITL0\_\_PT\_DpRKTL0\_0\_EEEvSI\_DpRKT0* ./gen/third\_party/libc++/src/include/\_\_type\_traits/invoke.h:90:27
#26 0x5676b8ff3adf in x11::Connection::ProcessNextEvent() ./../../ui/gfx/x/connection.cc:588:20
#27 0x5676b8ff3012 in x11::Connection::Dispatch() ./../../ui/gfx/x/connection.cc:0

# Problem Description

Heap-use-after-free in VerticalTabDragHandlerImpl::ContinueDrag

# Summary

Heap-use-after-free in VerticalTabDragHandlerImpl::ContinueDrag

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [simplescreenrecorder-2026-03-07_20.24.13.mp4](attachments/simplescreenrecorder-2026-03-07_20.24.13.mp4) (video/mp4, 1.7 MB)
- [testcase.html](attachments/testcase.html) (text/html, 490 B)
- [simplescreenrecorder-2026-03-30_16.26.22.mp4](attachments/simplescreenrecorder-2026-03-30_16.26.22.mp4) (video/mp4, 1.6 MB)

## Timeline

### ch...@gmail.com (2026-03-07)

==27679==ERROR: AddressSanitizer: heap-use-after-free on address 0x75a808d167a0 at pc 0x5676b233f3a4 bp 0x7ffdc3be33b0 sp 0x7ffdc3be33a8
READ of size 8 at 0x75a808d167a0 thread T0 (chrome)
==27679==WARNING: invalid path to external symbolizer!
==27679==WARNING: Failed to use and restart external symbolizer!
    #0 0x5676b233f3a3 in VerticalTabDragHandlerImpl::ContinueDrag(views::View&, ui::MouseEvent const&) ./gen/third_party/libc++/src/include/__memory/unique_ptr.h:285:21
    #1 0x5676bd9bd085 in views::View::ProcessMouseDragged(ui::MouseEvent*) ./../../ui/views/view.cc:3851:9
    #2 0x5676b90a9d7a in ui::EventDispatcher::DispatchEvent(ui::EventHandler*, ui::Event*) ./../../ui/events/event_dispatcher.cc:189:12
    #3 0x5676b90a87f5 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ./../../ui/events/event_dispatcher.cc:138:5
    #4 0x5676b90a7e0d in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ./../../ui/events/event_dispatcher.cc:84:14
    #5 0x5676b90a78c7 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ./../../ui/events/event_dispatcher.cc:56:15
    #6 0x5676bd9f80c6 in views::internal::RootView::OnMouseDragged(ui::MouseEvent const&) ./../../ui/views/widget/root_view.cc:614:9
    #7 0x5676bda256fe in views::Widget::OnMouseEvent(ui::MouseEvent*) ./../../ui/views/widget/widget.cc:2185:22
    #8 0x5676bdae041a in views::DesktopNativeWidgetAura::OnMouseEvent(ui::MouseEvent*) ./../../ui/views/widget/desktop_aura/desktop_native_widget_aura.cc:1445:30
    #9 0x5676b90a9d7a in ui::EventDispatcher::DispatchEvent(ui::EventHandler*, ui::Event*) ./../../ui/events/event_dispatcher.cc:189:12
    #10 0x5676b90a87f5 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ./../../ui/events/event_dispatcher.cc:138:5
    #11 0x5676b90a7e0d in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ./../../ui/events/event_dispatcher.cc:84:14
    #12 0x5676b90a78c7 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ./../../ui/events/event_dispatcher.cc:56:15
    #13 0x5676bcc02feb in ui::EventProcessor::OnEventFromSource(ui::Event*) ./../../ui/events/event_processor.cc:72:19
    #14 0x5676b90b041d in ui::EventSource::DeliverEventToSink(ui::Event*) ./../../ui/events/event_source.cc:119:16
    #15 0x5676b90afa7e in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) ./../../ui/events/event_source.cc:134:12
    #16 0x5676bdafcd19 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event*) ./../../ui/aura/window_tree_host_platform.cc:300:38
    #17 0x5676bdaf72eb in views::DesktopWindowTreeHostLinux::DispatchEvent(ui::Event*) ./../../ui/views/widget/desktop_aura/desktop_window_tree_host_linux.cc:250:29
    #18 0x56769fba99a8 in base::internal::Invoker<base::internal::FunctorTraits<void (ui::PlatformWindowDelegate::*&&)(ui::Event*), ui::PlatformWindowDelegate*>, base::internal::BindState<true, true, false, void (ui::PlatformWindowDelegate::*)(ui::Event*), base::internal::UnretainedWrapper<ui::PlatformWindowDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, void (ui::Event*)>::RunOnce(base::internal::BindStateBase*, ui::Event*) ./../../base/functional/bind_internal.h:740:12
    #19 0x5676b90c3c78 in ui::DispatchEventFromNativeUiEvent(ui::Event* const&, base::OnceCallback<void (ui::Event*)>) ./../../base/functional/callback.h:155:12
    #20 0x56769fc918ee in ui::X11Window::DispatchUiEvent(ui::Event*, x11::Event const&) ./../../ui/ozone/platform/x11/x11_window.cc:1421:3
    #21 0x56769fc90dd3 in ui::X11Window::DispatchEvent(ui::Event* const&) ./../../ui/ozone/platform/x11/x11_window.cc:1372:3
    #22 0x56769fc91b92 in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event* const&) ./../../ui/ozone/platform/x11/x11_window.cc:0:0
    #23 0x5676b8fdcba5 in ui::PlatformEventSource::DispatchEvent(ui::Event*) ./../../ui/events/platform/platform_event_source.cc:93:29
    #24 0x5676b973be44 in ui::X11EventSource::OnEvent(x11::Event const&) ./../../ui/events/platform/x11/x11_event_source.cc:301:5
    #25 0x5676b8ff56cb in _ZN4base12ObserverListIN3x1113EventObserverELb0ELNS_28ObserverListReentrancyPolicyE1ENS_8internal24UncheckedObserverAdapterILN15partition_alloc8internal12RawPtrTraitsE1ELb0EEEE6NotifyIMS2_FvRKNS1_5EventEEJSC_EQsr3stdE9invocableITL0__PT_DpRKTL0_0_EEEvSI_DpRKT0_ ./gen/third_party/libc++/src/include/__type_traits/invoke.h:90:27
    #26 0x5676b8ff3adf in x11::Connection::ProcessNextEvent() ./../../ui/gfx/x/connection.cc:588:20
    #27 0x5676b8ff3012 in x11::Connection::Dispatch() ./../../ui/gfx/x/connection.cc:0:0
    #28 0x5676b97496f8 in ui::(anonymous namespace)::XSourceDispatch(_GSource*, int (*)(void*), void*) ./../../ui/events/platform/x11/x11_event_watcher_glib.cc:57:15
    #29 0x78280bace45d in g_source_query_unix_fd ??:?
    #30 0x78280bb2d976 in g_io_channel_new_file ??:?
    #31 0x78280bacda22 in g_main_context_iteration ??:0:0
    #32 0x5676b5a185b3 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_glib.cc:770:30
    #33 0x5676b586cf27 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #34 0x5676b576f600 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:135:14
    #35 0x5676a95a87bc in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser_main_loop.cc:1106:18
    #36 0x5676a95b0e7c in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser_main_runner_impl.cc:151:15
    #37 0x5676a959f0dc in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser_main.cc:32:28
    #38 0x5676b147a95f in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:696:10
    #39 0x5676b147e950 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content_main_runner_impl.cc:1320:10
    #40 0x5676b147ddda in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1150:12
    #41 0x5676b1477781 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:358:36
    #42 0x5676b1477d7c in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:371:10
    #43 0x56769e081b39 in ChromeMain ./../../chrome/app/chrome_main.cc:191:12
    #44 0x78280a62a1c9 in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #45 0x78280a62a28a in __libc_start_main ./csu/../csu/libc-start.c:360:3
    #46 0x56769dfa7029 in _start ??:0:0

0x75a808d167a0 is located 800 bytes inside of 856-byte region [0x75a808d16480,0x75a808d167d8)
freed by thread T0 (chrome) here:
    #0 0x56769e080c3d in operator delete(void*) ??:0:0
    #1 0x5676ce98e534 in VerticalTabStripRegionView::~VerticalTabStripRegionView() ./gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #2 0x5676ce98f103 in VerticalTabStripRegionView::~VerticalTabStripRegionView() ./../../chrome/browser/ui/views/frame/vertical_tab_strip_region_view.cc:152:59
    #3 0x5676bd9a5339 in views::View::DoRemoveChildView(views::View*, bool, bool, views::View*) ./gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #4 0x5676bd9a560d in views::View::RemoveAllChildViews() ./../../ui/views/view.cc:358:5
    #5 0x5676ce7dcb62 in BrowserView::~BrowserView() ./../../chrome/browser/ui/views/frame/browser_view.cc:1137:3
    #6 0x5676ce7debbd in non-virtual thunk to BrowserView::~BrowserView() ./../../chrome/browser/ui/views/frame/browser_view.cc:1082:29
    #7 0x5676bd9a088b in views::View::~View() ./../../ui/views/view.cc:285:9
    #8 0x5676cf36cf39 in BrowserFrameViewLinuxNative::~BrowserFrameViewLinuxNative() ./../../chrome/browser/ui/views/frame/browser_frame_view_linux_native.cc:51:59
    #9 0x5676bda6644a in views::NonClientView::~NonClientView() ./gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #10 0x5676bda66603 in views::NonClientView::~NonClientView() ./../../ui/views/window/non_client_view.cc:35:33
    #11 0x5676bd9a5339 in views::View::DoRemoveChildView(views::View*, bool, bool, views::View*) ./gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #12 0x5676bd9a560d in views::View::RemoveAllChildViews() ./../../ui/views/view.cc:358:5
    #13 0x5676bda05e80 in views::Widget::~Widget() ./../../ui/views/widget/widget.cc:2553:15
    #14 0x5676ce89fe8d in BrowserWidget::~BrowserWidget() ./../../chrome/browser/ui/views/frame/browser_widget.cc:150:1
    #15 0x5676ce8a0103 in BrowserWidget::~BrowserWidget() ./../../chrome/browser/ui/views/frame/browser_widget.cc:131:33
    #16 0x5676ce802e1d in BrowserView::DeleteBrowserWindow() ./gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #17 0x5676cdde1ccc in Browser::~Browser() ./gen/third_party/libc++/src/include/__memory/unique_ptr.h:288:7
    #18 0x5676cdde383d in non-virtual thunk to Browser::~Browser() ./../../chrome/browser/ui/browser.cc:685:21
    #19 0x5676cde78335 in BrowserManagerService::DeleteBrowser(Browser*) ./gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #20 0x5676cde02c60 in base::internal::Invoker<base::internal::FunctorTraits<void (Browser::*&&)(), base::WeakPtr<Browser>&&>, base::internal::BindState<true, true, false, void (Browser::*)(), base::WeakPtr<Browser> >, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:740:12
    #21 0x5676b57f4066 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/functional/callback.h:155:12
    #22 0x5676b586b819 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/common/task_annotator.h:112:5
    #23 0x5676b586a68a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #24 0x5676b5a17f98 in base::MessagePumpGlib::HandleDispatch() ./../../base/message_loop/message_pump_glib.cc:736:46
    #25 0x5676b5a1b558 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) ./../../base/message_loop/message_pump_glib.cc:355:43
    #26 0x78280bace584 in g_source_query_unix_fd ??:?
    #27 0x78280bb2d976 in g_io_channel_new_file ??:?
    #28 0x78280bacda22 in g_main_context_iteration ??:0:0
    #29 0x5676b5a185b3 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_glib.cc:770:30

previously allocated by thread T0 (chrome) here:
    #0 0x56769e0803fd in operator new(unsigned long) ??:0:0
    #1 0x5676ce99055a in VerticalTabStripRegionView::InitializeTabStrip() ./../../ui/views/view.h:306:3
    #2 0x5676ce80a234 in BrowserView::AddedToWidget() ./../../chrome/browser/ui/views/frame/browser_view.cc:5203:40
    #3 0x5676bd9d0a1d in views::View::PropagateAddNotifications(views::ViewHierarchyChangedDetails const&, bool) ./../../ui/views/view.cc:3395:5
    #4 0x5676bd9cea6d in views::View::AddChildViewAtImpl(views::View*, unsigned long) ./../../ui/views/view.cc:3266:9
    #5 0x5676bda67cdb in views::NonClientView::ViewHierarchyChanged(views::ViewHierarchyChangedDetails const&) ./../../ui/views/window/non_client_view.cc:192:18
    #6 0x5676bd9d0964 in views::View::PropagateAddNotifications(views::ViewHierarchyChangedDetails const&, bool) ./../../ui/views/view.cc:3413:3
    #7 0x5676bd9cea6d in views::View::AddChildViewAtImpl(views::View*, unsigned long) ./../../ui/views/view.cc:3266:9
    #8 0x5676bda0469c in views::Widget::Init(views::Widget::InitParams) ./../../ui/views/widget/widget.cc:559:17
    #9 0x5676ce8a09ff in BrowserWidget::InitBrowserWidget() ./../../chrome/browser/ui/views/frame/browser_widget.cc:210:3
    #10 0x5676ce8cb469 in BrowserWindow::CreateBrowserWindow(Browser*, bool, bool) ./../../chrome/browser/ui/views/frame/browser_window_factory.cc:60:27
    #11 0x5676cdde0e6a in Browser::Browser(Browser::CreateParams const&) ./../../chrome/browser/ui/browser.cc:663:13
    #12 0x5676cdddf6ef in Browser::Create(Browser::CreateParams const&) ./../../chrome/browser/ui/browser.cc:558:59
    #13 0x5676b145d1a1 in StartupBrowserCreatorImpl::OpenTabsInBrowser(Browser*, chrome::startup::IsProcessStartup, std::__Cr::vector<StartupTab, std::__Cr::allocator<StartupTab> > const&, StartupBrowserCreatorImpl::TabOverWrite) ./../../chrome/browser/ui/startup/startup_browser_creator_impl.cc:302:15
    #14 0x5676b145fd52 in StartupBrowserCreatorImpl::RestoreOrCreateBrowser(std::__Cr::vector<StartupTab, std::__Cr::allocator<StartupTab> > const&, StartupBrowserCreatorImpl::BrowserOpenBehavior, unsigned int, chrome::startup::IsProcessStartup, bool) ./../../chrome/browser/ui/startup/startup_browser_creator_impl.cc:705:13
    #15 0x5676b145c1e0 in StartupBrowserCreatorImpl::DetermineURLsAndLaunch(chrome::startup::IsProcessStartup, bool) ./../../chrome/browser/ui/startup/startup_browser_creator_impl.cc:512:22
    #16 0x5676b145b305 in StartupBrowserCreatorImpl::Launch(Profile*, chrome::startup::IsProcessStartup, bool) ./../../chrome/browser/ui/startup/startup_browser_creator_impl.cc:232:3
    #17 0x5676b1454794 in StartupBrowserCreator::LaunchBrowser(base::CommandLine const&, Profile*, base::FilePath const&, chrome::startup::IsProcessStartup, chrome::startup::IsFirstRun, bool) ./../../chrome/browser/ui/startup/startup_browser_creator.cc:729:9
    #18 0x5676b1456191 in StartupBrowserCreator::ProcessLastOpenedProfiles(base::CommandLine const&, base::FilePath const&, chrome::startup::IsProcessStartup, chrome::startup::IsFirstRun, Profile*, std::__Cr::vector<Profile*, std::__Cr::allocator<Profile*> > const&) ./../../chrome/browser/ui/startup/startup_browser_creator.cc:1395:5
    #19 0x5676b145535b in StartupBrowserCreator::LaunchBrowserForLastProfiles(base::CommandLine const&, base::FilePath const&, chrome::startup::IsProcessStartup, chrome::startup::IsFirstRun, StartupProfileInfo, std::__Cr::vector<Profile*, std::__Cr::allocator<Profile*> > const&, bool) ./../../chrome/browser/ui/startup/startup_browser_creator.cc:840:3
    #20 0x5676b145410a in StartupBrowserCreator::ProcessCmdLineImpl(base::CommandLine const&, base::FilePath const&, chrome::startup::IsProcessStartup, StartupProfileInfo, std::__Cr::vector<Profile*, std::__Cr::allocator<Profile*> > const&) ./../../chrome/browser/ui/startup/startup_browser_creator.cc:0:0
    #21 0x5676b145251e in StartupBrowserCreator::Start(base::CommandLine const&, base::FilePath const&, StartupProfileInfo, std::__Cr::vector<Profile*, std::__Cr::allocator<Profile*> > const&) ./../../chrome/browser/ui/startup/startup_browser_creator.cc:683:10
    #22 0x5676b4595ae8 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl() ./../../chrome/browser/chrome_browser_main.cc:2019:25
    #23 0x5676b459414c in ChromeBrowserMainParts::PreMainMessageLoopRun() ./../../chrome/browser/chrome_browser_main.cc:1428:18
    #24 0x5676a95a5b8c in content::BrowserMainLoop::PreMainMessageLoopRun() ./../../content/browser/browser_main_loop.cc:1006:28
    #25 0x5676a95ad191 in base::internal::Invoker<base::internal::FunctorTraits<int (content::BrowserMainLoop::*&&)(), content::BrowserMainLoop*>, base::internal::BindState<true, true, false, int (content::BrowserMainLoop::*)(), base::internal::UnretainedWrapper<content::BrowserMainLoop, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, int ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:740:12
    #26 0x5676ab2884fd in content::StartupTaskRunner::RunAllTasksNow(bool) ./../../base/functional/callback.h:155:12
    #27 0x5676a95a49c5 in content::BrowserMainLoop::CreateStartupTasks() ./../../content/browser/browser_main_loop.cc:912:25
    #28 0x5676a95b057f in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams) ./../../content/browser/browser_main_runner_impl.cc:138:15
    #29 0x5676a959f03a in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser_main.cc:28:32

SUMMARY: AddressSanitizer: heap-use-after-free (/home/lenovo/Downloads/extension/linux-release_asan-linux-release-1595970/chrome+0x252023a3) (BuildId: a526d75601896f6c)
Shadow bytes around the buggy address:
  0x75a808d16500: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x75a808d16580: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x75a808d16600: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x75a808d16680: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x75a808d16700: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x75a808d16780: fd fd fd fd[fd]fd fd fd fd fd fd fa fa fa fa fa
  0x75a808d16800: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x75a808d16880: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x75a808d16900: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x75a808d16980: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x75a808d16a00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==27679==ADDITIONAL INFO

==27679==Note: Please include this section with the ASan report.
Task trace:


Command line: `./chrome -remote-debugging-port=9222 --no-sandbox --user-data-dir=/home/lenovo/Downloads/chrome-profile --flag-switches-begin --flag-switches-end --ozone-platform=x11 --file-url-path-alias=/gen=/home/lenovo/Downloads/extension/linux-release_asan-linux-release-1595970/gen`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.



### jd...@chromium.org (2026-03-09)

I have not reproduced this due to the volume of bugs Chrome Security is presently receiving, but forwarding to dpenning@ to investigate further.

dpenning@: if you can't reproduce this, feel free to close as invalid. Thanks!

### ch...@gmail.com (2026-03-16)

Any update on this bug? Thanks!

### ch...@gmail.com (2026-03-24)

dpenning@ - Friendly ping.

### al...@google.com (2026-03-30)

I believe this should be fixed as of 147.0.7727.24. Please reopen if it still happens on this version or later.

### ch...@gmail.com (2026-03-30)

I am still able to repro this on 148.0.7765.0. 

### dx...@google.com (2026-03-30)

Project: chromium/src  

Branch:  main  

Author:  Kaan Alsan [alsan@chromium.org](mailto:alsan@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7705549>

Protect against use-after-free in VerticalTabDragHandlerImpl

---


Expand for full commit details
```
     
    The TabDragController::Drag method can start a blocking message loop. 
    This loop can lead to the destruction of the VerticalTabDragHandlerImpl 
    instance. Use a WeakPtr to check if the instance is still alive before 
    calling ResetDragState after Drag returns. 
     
    Bug: 490588145, 495973592 
    Change-Id: I9d193a9c0ced4fe698bcec57c5bca3c749d05752 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7705549 
    Commit-Queue: Kaan Alsan <alsan@chromium.org> 
    Reviewed-by: Foromo Daniel Soromou <koretadaniel@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1607358}

```

---

Files:

- M `chrome/browser/ui/views/tabs/vertical/vertical_tab_drag_handler.cc`
- M `chrome/browser/ui/views/tabs/vertical/vertical_tab_drag_handler.h`

---

Hash: [8452c6aaafc5710974c3313967d2dd84aedfa534](https://chromiumdash.appspot.com/commit/8452c6aaafc5710974c3313967d2dd84aedfa534)  

Date: Mon Mar 30 20:51:35 2026


---

### ch...@gmail.com (2026-03-30)

I can now confirm that this UAF is no longer reproducible on 148.0.7765.0 (Build Revision: 1607405).

Thanks for the quick fix!

### ch...@gmail.com (2026-03-31)

Just checking — does this issue require any further work, or is it ready to be marked as fixed?

### al...@google.com (2026-04-01)

Thank you for confirming this is fixed - it seems like this only repro'd on Linux. Marking it as fixed.

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Baseline. Highly mitigated (non-sandboxed)


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/490588145)*
