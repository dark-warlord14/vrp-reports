# Security: Heap-use-after-free in ash::OverviewItem::DestroyPhantomsForDragging

| Field | Value |
|-------|-------|
| **Issue ID** | [40059787](https://issues.chromium.org/issues/40059787) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Shell |
| **Platforms** | ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | sa...@chromium.org |
| **Created** | 2022-05-28 |
| **Bounty** | $3,000.00 |

## Description

**VERSION**  

Chrome Version: linux-release-chromeos\_asan-linux-release-1008401.zip  

Operating System: Linux

**REPRODUCTION CASE**

Run with --force-tablet-mode=touch\_view

1. Get a page in full screen
2. Press F5 and drag the page to the right or left to use slip screen

==39633==ERROR: AddressSanitizer: heap-use-after-free on address 0x614000251d50 at pc 0x561e26b4fc60 bp 0x7ffcbbbf2a60 sp 0x7ffcbbbf2a58  

READ of size 8 at 0x614000251d50 thread T0 (chrome)  

==39633==WARNING: invalid path to external symbolizer!  

==39633==WARNING: Failed to use and restart external symbolizer!  

#0 0x561e26b4fc5f in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:305:28  

#1 0x561e26b4fc5f in ash::OverviewItem::DestroyPhantomsForDragging() ./../../ash/wm/overview/overview\_item.cc:710:26  

#2 0x561e26b6e3ea in ash::OverviewWindowDragController::ResetGesture() ./../../ash/wm/overview/overview\_window\_drag\_controller.cc:426:12  

#3 0x561e26b5e026 in ash::OverviewSession::ResetDraggedWindowGesture() ./../../ash/wm/overview/overview\_session.cc:650:28  

#4 0x561e26b6058b in ash::OverviewSession::OnDisplayMetricsChanged(display::Display const&, unsigned int) ./../../ash/wm/overview/overview\_session.cc:1159:5  

#5 0x561e25d79dfe in display::DisplayManager::NotifyMetricsChanged(display::Display const&, unsigned int) ./../../ui/display/manager/display\_manager.cc:2203:14  

#6 0x561e25d7a3ae in display::DisplayManager::UpdateWorkAreaOfDisplay(long, gfx::Insets const&) ./../../ui/display/manager/display\_manager.cc:508:5  

#7 0x561e26580ced in ash::ShelfLayoutManager::UpdateBoundsAndOpacity(bool) ./../../ash/shelf/shelf\_layout\_manager.cc:1647:25  

#8 0x561e26581d1c in ash::ShelfLayoutManager::SetState(ash::ShelfVisibilityState) ./../../ash/shelf/shelf\_layout\_manager.cc:1352:3  

#9 0x561e2657c8b0 in ash::ShelfLayoutManager::UpdateVisibilityState() ./../../ash/shelf/shelf\_layout\_manager.cc:0:14  

#10 0x561e26c2da3d in UpdateShelfVisibility ./../../ash/wm/workspace/workspace\_layout\_manager.cc:509:37  

#11 0x561e26c2da3d in ash::WorkspaceLayoutManager::OnPostWindowStateTypeChange(ash::WindowState\*, chromeos::WindowStateType) ./../../ash/wm/workspace/workspace\_layout\_manager.cc:386:3  

#12 0x561e26c16a0e in ash::WindowState::NotifyPostStateTypeChange(chromeos::WindowStateType) ./../../ash/wm/window\_state.cc:851:14  

#13 0x561e26c1e29e in ash::DefaultState::EnterToNextState(ash::WindowState\*, chromeos::WindowStateType) ./../../ash/wm/default\_state.cc:473:17  

#14 0x561e26c1dc4d in ash::DefaultState::HandleTransitionEvents(ash::WindowState\*, ash::WMEvent const\*) ./../../ash/wm/default\_state.cc:377:3  

#15 0x561e26c1010d in ash::WindowState::OnWMEvent(ash::WMEvent const\*) ./../../ash/wm/window\_state.cc:455:19  

#16 0x561e26c18f1d in ash::WindowState::OnWindowPropertyChanged(aura::Window\*, void const\*, long) ./../../ash/wm/window\_state.cc:1131:7  

#17 0x561e25c3324a in aura::Window::AfterPropertyChange(void const\*, long) ./../../ui/aura/window.cc:949:14  

#18 0x561e2265e57f in ui::PropertyHandler::SetPropertyInternal(void const\*, char const\*, void (\*)(long), long, long) ./../../ui/base/class\_property.cc:43:3  

#19 0x561e25c1869e in void ui::subtle::PropertyHelper::Set[ui::WindowShowState](javascript:void(0);)(ui::PropertyHandler\*, ui::ClassProperty[ui::WindowShowState](javascript:void(0);) const\*, ui::WindowShowState) ./../../ui/base/class\_property.h:204:28  

#20 0x561e26080f21 in views::Widget::SetFullscreen(bool, long) ./../../ui/views/widget/widget.cc:818:19  

#21 0x561e26c27944 in ash::BackdropController::Layout() ./../../ash/wm/workspace/backdrop\_controller.cc:628:14  

#22 0x561e26c26ad3 in ash::BackdropController::Show() ./../../ash/wm/workspace/backdrop\_controller.cc:534:3  

#23 0x561e26c25e04 in ash::BackdropController::UpdateBackdropInternal() ./../../ash/wm/workspace/backdrop\_controller.cc:0:0  

#24 0x561e26b91695 in ash::SplitViewController::UpdateStateAndNotifyObservers() ./../../ash/wm/splitview/split\_view\_controller.cc:2065:14  

#25 0x561e26b98b18 in ash::SplitViewController::OnWindowSnapped(aura::Window\*) ./../../ash/wm/splitview/split\_view\_controller.cc:2326:3  

#26 0x561e26b9896d in ash::SplitViewController::OnPostWindowStateTypeChange(ash::WindowState\*, chromeos::WindowStateType) ./../../ash/wm/splitview/split\_view\_controller.cc:1659:5  

#27 0x561e26c16a0e in ash::WindowState::NotifyPostStateTypeChange(chromeos::WindowStateType) ./../../ash/wm/window\_state.cc:851:14  

#28 0x561e26bd4f78 in ash::TabletModeWindowState::UpdateWindow(ash::WindowState\*, chromeos::WindowStateType, bool) ./../../ash/wm/tablet\_mode/tablet\_mode\_window\_state.cc:469:17  

#29 0x561e26bd467b in ash::TabletModeWindowState::OnWMEvent(ash::WindowState\*, ash::WMEvent const\*) ./../../ash/wm/tablet\_mode/tablet\_mode\_window\_state.cc:0:0  

#30 0x561e26c1010d in ash::WindowState::OnWMEvent(ash::WMEvent const\*) ./../../ash/wm/window\_state.cc:455:19  

#31 0x561e26b8f431 in ash::SplitViewController::SnapWindow(aura::Window\*, ash::SplitViewController::SnapPosition, bool) ./../../ash/wm/splitview/split\_view\_controller.cc:851:29  

#32 0x561e26b6e298 in ash::OverviewWindowDragController::SnapWindow(ash::SplitViewController\*, ash::SplitViewController::SnapPosition) ./../../ash/wm/overview/overview\_window\_drag\_controller.cc:821:26  

#33 0x561e26b6d2ce in ash::OverviewWindowDragController::CompleteNormalDrag(gfx::PointF const&) ./../../ash/wm/overview/overview\_window\_drag\_controller.cc:691:5  

#34 0x561e26b6ca08 in ash::OverviewWindowDragController::CompleteDrag(gfx::PointF const&) ./../../ash/wm/overview/overview\_window\_drag\_controller.cc:282:16  

#35 0x561e26b5ddb1 in ash::OverviewSession::CompleteDrag(ash::OverviewItem\*, gfx::PointF const&) ./../../ash/wm/overview/overview\_session.cc:614:46  

#36 0x561e26b50b58 in ash::OverviewItem::HandleMouseEvent(ui::MouseEvent const&) ./../../ash/wm/overview/overview\_item.cc:895:7  

#37 0x561e22719689 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:190:12  

#38 0x561e22718bc2 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:139:5  

#39 0x561e22718696 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:83:14  

#40 0x561e22718426 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:55:15  

#41 0x561e26072757 in views::internal::RootView::OnMouseReleased(ui::MouseEvent const&) ./../../ui/views/widget/root\_view.cc:485:9  

#42 0x561e26087e4f in views::Widget::OnMouseEvent(ui::MouseEvent\*) ./../../ui/views/widget/widget.cc:1565:20  

#43 0x561e22719689 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:190:12  

#44 0x561e22718bc2 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:139:5  

#45 0x561e22718696 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:83:14  

#46 0x561e22718426 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:55:15  

#47 0x561e25c4e169 in ui::EventProcessor::OnEventFromSource(ui::Event\*) ./../../ui/events/event\_processor.cc:49:17  

#48 0x561e2271cdee in ui::EventSource::DeliverEventToSink(ui::Event\*) ./../../ui/events/event\_source.cc:118:16  

#49 0x561e2271d2e6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ./../../ui/events/event\_source.cc:66:14  

#50 0x561e2271ba3b in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ./../../ui/events/event\_rewriter.cc:88:39  

#51 0x561e15d4d603 in ui::EventRewriterChromeOS::RewriteMouseButtonEvent(ui::MouseEvent const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ./../../ui/chromeos/events/event\_rewriter\_chromeos.cc:1275:12  

#52 0x561e15d4db43 in ui::EventRewriterChromeOS::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ./../../ui/chromeos/events/event\_rewriter\_chromeos.cc:757:12  

#53 0x561e2271d296 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ./../../ui/events/event\_source.cc:67:32  

#54 0x561e2271ba3b in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ./../../ui/events/event\_rewriter.cc:88:39  

#55 0x561e26358d20 in ash::KeyboardDrivenEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ./../../ash/events/keyboard\_driven\_event\_rewriter.cc:31:12  

#56 0x561e2271d296 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ./../../ui/events/event\_source.cc:67:32  

#57 0x561e2271ba3b in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ./../../ui/events/event\_rewriter.cc:88:39  

#58 0x561e26354d06 in ash::AccessibilityEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ./../../ash/events/accessibility\_event\_rewriter.cc:0:0  

#59 0x561e2271d296 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ./../../ui/events/event\_source.cc:67:32  

#60 0x561e2271ba3b in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ./../../ui/events/event\_rewriter.cc:88:39  

#61 0x561e2612c37e in ash::AutoclickDragEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ./../../ash/accessibility/autoclick/autoclick\_drag\_event\_rewriter.cc:0:0  

#62 0x561e2271d296 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ./../../ui/events/event\_source.cc:67:32  

#63 0x561e2271ba3b in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ./../../ui/events/event\_rewriter.cc:88:39  

#64 0x561e26139dea in ash::FullscreenMagnifierController::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ./../../ash/accessibility/magnifier/fullscreen\_magnifier\_controller.cc:0:0  

#65 0x561e2271ca91 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const\*, ui::EventRewriter const\*) ./../../ui/events/event\_source.cc:144:29  

#66 0x561e2638fa9f in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event\*) ./../../ui/aura/window\_tree\_host\_platform.cc:229:38  

#67 0x561e26397044 in ash::AshWindowTreeHostPlatform::DispatchEvent(ui::Event\*) ./../../ash/host/ash\_window\_tree\_host\_platform.cc:207:40  

#68 0x561e2272b247 in Run ./../../base/callback.h:143:12  

#69 0x561e2272b247 in ui::DispatchEventFromNativeUiEvent(ui::Event\* const&, base::OnceCallback<void (ui::Event\*)>) ./../../ui/events/ozone/events\_ozone.cc:36:25  

#70 0x561e12e7bac1 in ui::X11Window::DispatchUiEvent(ui::Event\*, x11::Event const&) ./../../ui/ozone/platform/x11/x11\_window.cc:1341:3  

#71 0x561e12e7b313 in ui::X11Window::DispatchEvent(ui::Event\* const&) ./../../ui/ozone/platform/x11/x11\_window.cc:1294:3  

#72 0x561e12e7bdfc in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event\* const&) ./../../ui/ozone/platform/x11/x11\_window.cc:0:0  

#73 0x561e226c26a9 in ui::PlatformEventSource::DispatchEvent(ui::Event\*) ./../../ui/events/platform/platform\_event\_source.cc:99:29  

#74 0x561e22e30bef in ui::X11EventSource::OnEvent(x11::Event const&) ./../../ui/events/platform/x11/x11\_event\_source.cc:287:5  

#75 0x561e12a96c35 in x11::Connection::DispatchEvent(x11::Event const&) ./../../ui/gfx/x/connection.cc:457:14  

#76 0x561e12a96943 in x11::Connection::ProcessNextEvent() ./../../ui/gfx/x/connection.cc:508:3  

#77 0x561e12a96413 in x11::Connection::Dispatch() ./../../ui/gfx/x/connection.cc:0:0  

#78 0x561e22e39b03 in ui::X11EventWatcherFdWatch::OnFileCanReadWithoutBlocking(int) ./../../ui/events/platform/x11/x11\_event\_watcher\_fdwatch.cc:64:15  

#79 0x561e20467cda in base::MessagePumpLibevent::OnLibeventNotification(int, short, void\*) ./../../base/message\_loop/message\_pump\_libevent.cc:0:13  

#80 0x561e2078462b in event\_process\_active ./../../base/third\_party/libevent/event.c:381:4  

#81 0x561e2078462b in event\_base\_loop ./../../base/third\_party/libevent/event.c:521:4  

#82 0x561e204685f6 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_libevent.cc:204:7  

#83 0x561e2035c58b in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:542:12  

#84 0x561e2028b62f in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:141:14  

#85 0x561e16a6e0b2 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1039:18  

#86 0x561e16a7249b in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:157:15  

#87 0x561e16a682ba in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:30:28  

#88 0x561e2005ff2b in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:660:10  

#89 0x561e20062a2c in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1167:10  

#90 0x561e20061e76 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1039:12  

#91 0x561e2005b9c6 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:407:36  

#92 0x561e2005cd32 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:435:10  

#93 0x561e11a69e50 in ChromeMain ./../../chrome/app/chrome\_main.cc:177:12  

#94 0x7f450e4c90b2 in \_\_libc\_start\_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16

0x614000251d50 is located 272 bytes inside of 392-byte region [0x614000251c40,0x614000251dc8)  

freed by thread T0 (chrome) here:  

#0 0x561e11a67eed in operator delete(void\*) *asan\_rtl*:3  

#1 0x561e26b2b419 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:51:5  

#2 0x561e26b2b419 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:308:7  

#3 0x561e26b2b419 in ash::OverviewGrid::RemoveItem(ash::OverviewItem\*, bool, bool) ./../../ash/wm/overview/overview\_grid.cc:731:7  

#4 0x561e26b5be52 in ash::OverviewSession::RemoveItem(ash::OverviewItem\*, bool, bool) ./../../ash/wm/overview/overview\_session.cc:557:35  

#5 0x561e26b8fd88 in RemoveSnappingWindowFromOverviewIfApplicable ./../../ash/wm/splitview/split\_view\_controller.cc:232:21  

#6 0x561e26b8fd88 in ash::SplitViewController::AttachSnappingWindow(aura::Window\*, ash::SplitViewController::SnapPosition) ./../../ash/wm/splitview/split\_view\_controller.cc:900:3  

#7 0x561e26c1637b in ash::WindowState::NotifyPreStateTypeChange(chromeos::WindowStateType) ./../../ash/wm/window\_state.cc:844:14  

#8 0x561e26bd4e67 in ash::TabletModeWindowState::UpdateWindow(ash::WindowState\*, chromeos::WindowStateType, bool) ./../../ash/wm/tablet\_mode/tablet\_mode\_window\_state.cc:449:17  

#9 0x561e26bd467b in ash::TabletModeWindowState::OnWMEvent(ash::WindowState\*, ash::WMEvent const\*) ./../../ash/wm/tablet\_mode/tablet\_mode\_window\_state.cc:0:0  

#10 0x561e26c1010d in ash::WindowState::OnWMEvent(ash::WMEvent const\*) ./../../ash/wm/window\_state.cc:455:19  

#11 0x561e26b8f431 in ash::SplitViewController::SnapWindow(aura::Window\*, ash::SplitViewController::SnapPosition, bool) ./../../ash/wm/splitview/split\_view\_controller.cc:851:29  

#12 0x561e26b6e298 in ash::OverviewWindowDragController::SnapWindow(ash::SplitViewController\*, ash::SplitViewController::SnapPosition) ./../../ash/wm/overview/overview\_window\_drag\_controller.cc:821:26  

#13 0x561e26b6d2ce in ash::OverviewWindowDragController::CompleteNormalDrag(gfx::PointF const&) ./../../ash/wm/overview/overview\_window\_drag\_controller.cc:691:5  

#14 0x561e26b6ca08 in ash::OverviewWindowDragController::CompleteDrag(gfx::PointF const&) ./../../ash/wm/overview/overview\_window\_drag\_controller.cc:282:16  

#15 0x561e26b5ddb1 in ash::OverviewSession::CompleteDrag(ash::OverviewItem\*, gfx::PointF const&) ./../../ash/wm/overview/overview\_session.cc:614:46  

#16 0x561e26b50b58 in ash::OverviewItem::HandleMouseEvent(ui::MouseEvent const&) ./../../ash/wm/overview/overview\_item.cc:895:7  

#17 0x561e22719689 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:190:12  

#18 0x561e22718bc2 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:139:5  

#19 0x561e22718696 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:83:14  

#20 0x561e22718426 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:55:15  

#21 0x561e26072757 in views::internal::RootView::OnMouseReleased(ui::MouseEvent const&) ./../../ui/views/widget/root\_view.cc:485:9  

#22 0x561e26087e4f in views::Widget::OnMouseEvent(ui::MouseEvent\*) ./../../ui/views/widget/widget.cc:1565:20  

#23 0x561e22719689 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:190:12  

#24 0x561e22718bc2 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:139:5  

#25 0x561e22718696 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:83:14  

#26 0x561e22718426 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:55:15  

#27 0x561e25c4e169 in ui::EventProcessor::OnEventFromSource(ui::Event\*) ./../../ui/events/event\_processor.cc:49:17  

#28 0x561e2271cdee in ui::EventSource::DeliverEventToSink(ui::Event\*) ./../../ui/events/event\_source.cc:118:16  

#29 0x561e2271d2e6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ./../../ui/events/event\_source.cc:66:14  

#30 0x561e2271ba3b in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ./../../ui/events/event\_rewriter.cc:88:39  

#31 0x561e15d4d603 in ui::EventRewriterChromeOS::RewriteMouseButtonEvent(ui::MouseEvent const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ./../../ui/chromeos/events/event\_rewriter\_chromeos.cc:1275:12  

#32 0x561e15d4db43 in ui::EventRewriterChromeOS::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ./../../ui/chromeos/events/event\_rewriter\_chromeos.cc:757:12

previously allocated by thread T0 (chrome) here:  

#0 0x561e11a6768d in operator new(unsigned long) *asan\_rtl*:3  

#1 0x561e26b221bc in make\_unique<ash::OverviewItem, aura::Window \*&, ash::OverviewSession \*&, ash::OverviewGrid \*> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:717:28  

#2 0x561e26b221bc in ash::OverviewGrid::OverviewGrid(aura::Window\*, std::Cr::vector<aura::Window\*, std::Cr::allocator[aura::Window\\*](javascript:void(0);) > const&, ash::OverviewSession\*) ./../../ash/wm/overview/overview\_grid.cc:450:9  

#3 0x561e26b585e3 in make\_unique<ash::OverviewGrid, aura::Window \*&, const std::Cr::vector<aura::Window \*, std::Cr::allocator<aura::Window \*> > &, ash::OverviewSession \*> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:717:32  

#4 0x561e26b585e3 in ash::OverviewSession::Init(std::Cr::vector<aura::Window\*, std::Cr::allocator[aura::Window\\*](javascript:void(0);) > const&, std::Cr::vector<aura::Window\*, std::Cr::allocator[aura::Window\\*](javascript:void(0);) > const&) ./../../ash/wm/overview/overview\_session.cc:205:17  

#5 0x561e26b1c0c8 in ash::OverviewController::ToggleOverview(ash::OverviewEnterExitType) ./../../ash/wm/overview/overview\_controller.cc:431:24  

#6 0x561e26b1b4c3 in ash::OverviewController::StartOverview(ash::OverviewStartAction, ash::OverviewEnterExitType) ./../../ash/wm/overview/overview\_controller.cc:129:3  

#7 0x561e26116592 in ash::(anonymous namespace)::HandleToggleOverview() ./../../ash/accelerators/accelerator\_controller\_impl.cc:882:26  

#8 0x561e2610db7b in ash::AcceleratorControllerImpl::PerformAction(ash::AcceleratorAction, ui::Accelerator const&) ./../../ash/accelerators/accelerator\_controller\_impl.cc:2467:7  

#9 0x561e2610f257 in ash::AcceleratorControllerImpl::AcceleratorPressed(ui::Accelerator const&) ./../../ash/accelerators/accelerator\_controller\_impl.cc:1729:3  

#10 0x561e25fef22c in TryProcess ./../../ui/base/accelerators/accelerator\_manager.cc:153:17  

#11 0x561e25fef22c in ui::AcceleratorManager::Process(ui::Accelerator const&) ./../../ui/base/accelerators/accelerator\_manager.cc:83:27  

#12 0x561e26609c6f in ash::PreTargetAcceleratorHandler::ProcessAccelerator(ui::KeyEvent const&, ui::Accelerator const&) ./../../ash/accelerators/pre\_target\_accelerator\_handler.cc:74:45  

#13 0x561e2660a2cf in wm::AcceleratorFilter::OnKeyEvent(ui::KeyEvent\*) ./../../ui/wm/core/accelerator\_filter.cc:51:18  

#14 0x561e22719689 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:190:12  

#15 0x561e227193ad in ui::EventDispatcher::DispatchEventToEventHandlers(std::Cr::vector<ui::EventHandler\*, std::Cr::allocator[ui::EventHandler\\*](javascript:void(0);) >\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:177:7  

#16 0x561e22718a0f in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:125:3  

#17 0x561e22718696 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:83:14  

#18 0x561e22718426 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:55:15  

#19 0x561e25c4e169 in ui::EventProcessor::OnEventFromSource(ui::Event\*) ./../../ui/events/event\_processor.cc:49:17  

#20 0x561e25c6512c in aura::WindowTreeHost::DispatchKeyEventPostIME(ui::KeyEvent\*) ./../../ui/aura/window\_tree\_host.cc:373:23  

#21 0x561e22f989b7 in ui::InputMethodBase::DispatchKeyEventPostIME(ui::KeyEvent\*) const ./../../ui/base/ime/input\_method\_base.cc:140:33  

#22 0x561e230e380d in ui::InputMethodAsh::ProcessUnfilteredKeyPressEvent(ui::KeyEvent\*) ./../../ui/base/ime/ash/input\_method\_ash.cc:615:38  

#23 0x561e230e306e in ui::InputMethodAsh::DispatchKeyEvent(ui::KeyEvent\*) ./../../ui/base/ime/ash/input\_method\_ash.cc:139:14  

#24 0x561e25c48c5f in aura::WindowEventDispatcher::PreDispatchKeyEvent(aura::Window\*, ui::KeyEvent\*) ./../../ui/aura/window\_event\_dispatcher.cc:1080:54  

#25 0x561e25c47606 in aura::WindowEventDispatcher::PreDispatchEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/aura/window\_event\_dispatcher.cc:568:15  

#26 0x561e227183d6 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:51:34  

#27 0x561e25c4e169 in ui::EventProcessor::OnEventFromSource(ui::Event\*) ./../../ui/events/event\_processor.cc:49:17  

#28 0x561e2271cdee in ui::EventSource::DeliverEventToSink(ui::Event\*) ./../../ui/events/event\_source.cc:118:16  

#29 0x561e2271bbf7 in ui::EventRewriter::SendEventFinally(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ./../../ui/events/event\_rewriter.cc:94:39  

#30 0x561e15d4f8d4 in ui::EventRewriterChromeOS::RewriteKeyEventInContext(ui::KeyEvent const&, std::Cr::unique\_ptr<ui::Event, std::Cr::default\_delete[ui::Event](javascript:void(0);) >, ui::EventRewriteStatus, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ./../../ui/chromeos/events/event\_rewriter\_chromeos.cc:1837:9  

#31 0x561e15d4dd27 in ui::EventRewriterChromeOS::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ./../../ui/chromeos/events/event\_rewriter\_chromeos.cc:751:12  

#32 0x561e2271d296 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ./../../ui/events/event\_source.cc:67:32

SUMMARY: AddressSanitizer: heap-use-after-free (/home/lbstyle/Desktop/asan-linux-release-1008401/chrome+0x23707c5f) (BuildId: 52c9b48f17789a8e)  

Shadow bytes around the buggy address:  

0x0c2880042350: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2880042360: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2880042370: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa  

0x0c2880042380: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c2880042390: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x0c28800423a0: fd fd fd fd fd fd fd fd fd fd[fd]fd fd fd fd fd  

0x0c28800423b0: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa  

0x0c28800423c0: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x0c28800423d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c28800423e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c28800423f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb

## Attachments

- [screen.webm](attachments/screen.webm) (video/webm, 2.6 MB)

## Timeline

### [Deleted User] (2022-05-28)

[Empty comment from Monorail migration]

### dr...@chromium.org (2022-05-28)

Over to ChromeOS triage

### en...@chromium.org (2022-06-06)

Assigning owner based on the OWENERS file.

[Monorail components: UI>Shell]

### [Deleted User] (2022-06-07)

[Empty comment from Monorail migration]

### sa...@chromium.org (2022-06-07)

think this happens because we snap a window here [1], which would remove the associated item from overview. Snapping triggers some things like removing item from overview. and for fullscreen, updating work area (as shelf go away). I believe the overivew remove is done, then the work area update, then `item` gets set to null [3]. However, the work area update tries to access `item` in between.

[1] https://source.chromium.org/chromium/chromium/src/+/main:ash/wm/overview/overview_window_drag_controller.cc;drc=453ea8a95e523d3c774046c27c3353901c3917e2;l=691

[2]
https://source.chromium.org/chromium/chromium/src/+/main:ash/wm/overview/overview_session.cc;drc=dd98d836e7ed234b13de9ca02045aae7c0530b47;l=1156

[3] https://source.chromium.org/chromium/chromium/src/+/main:ash/wm/overview/overview_window_drag_controller.cc;drc=1946212ac0100668f14eb9e2843bdd846e510a1e;l=823

### gi...@appspot.gserviceaccount.com (2022-06-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cb8d2046dccda41a687b9abe537a2d7361572c57

commit cb8d2046dccda41a687b9abe537a2d7361572c57
Author: Sammie Quon <sammiequon@chromium.org>
Date: Wed Jun 08 19:06:57 2022

overview: Fix u-a-f when snapping a fullscreen window in tablet.

Fixed: 1330042
Test: ash_unittests TabletModeOverviewSessionTest.SnappingFullscreenWindow

Change-Id: I41ae7af0254ca69dc5bfa06bd860ffa62c2c7bef
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3692092
Commit-Queue: Sammie Quon <sammiequon@chromium.org>
Reviewed-by: Xiaoqian Dai <xdai@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1012093}

[modify] https://crrev.com/cb8d2046dccda41a687b9abe537a2d7361572c57/ash/wm/overview/overview_session_unittest.cc
[modify] https://crrev.com/cb8d2046dccda41a687b9abe537a2d7361572c57/ash/wm/overview/overview_session.cc
[modify] https://crrev.com/cb8d2046dccda41a687b9abe537a2d7361572c57/ash/wm/overview/overview_window_drag_controller.cc


### [Deleted User] (2022-06-09)

[Empty comment from Monorail migration]

### ch...@gmail.com (2022-06-09)

What is the severity here?

### [Deleted User] (2022-06-09)

[Empty comment from Monorail migration]

### en...@google.com (2022-06-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-10)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-10)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-10)

Requesting merge to stable M102 because latest trunk commit (1012093) appears to be after stable branch point (992738).

Requesting merge to beta M103 because latest trunk commit (1012093) appears to be after beta branch point (1002911).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-10)

Merge review required: M103 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-10)

Merge review required: M102 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dg...@google.com (2022-06-13)

sammiequon@ - can you please provide the info requested in https://crbug.com/chromium/1330042#c15?

### sa...@chromium.org (2022-06-13)

1. security fix
2. https://chromium-review.googlesource.com/c/chromium/src/+/3692092
3. yes
4. no
5. +dhaddock
6. no

### ce...@google.com (2022-06-13)

This missed our build cutoff (last thursday) for M102s stable respin. We haven't been able to finish auto-test results due to a lab outage, but our manual regression test team has finished their work and moved on to other channels. 

I'm going to mark this merge rejected for 102, since we're ~10days out from 103.

### en...@chromium.org (2022-06-13)

[Empty comment from Monorail migration]

### dg...@google.com (2022-06-13)

Approved for m103 pending LGTM from dhaddock@

### dh...@chromium.org (2022-06-14)

lgtm

### gi...@appspot.gserviceaccount.com (2022-06-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/639f6de5f197741717a2d910b531bd59231dbef8

commit 639f6de5f197741717a2d910b531bd59231dbef8
Author: Sammie Quon <sammiequon@chromium.org>
Date: Tue Jun 14 23:17:07 2022

[merge to 103] overview: Fix u-a-f when snapping a fullscreen window in tablet.

Fixed: 1330042
Test: ash_unittests TabletModeOverviewSessionTest.SnappingFullscreenWindow

(cherry picked from commit cb8d2046dccda41a687b9abe537a2d7361572c57)

Change-Id: I41ae7af0254ca69dc5bfa06bd860ffa62c2c7bef
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3692092
Commit-Queue: Sammie Quon <sammiequon@chromium.org>
Reviewed-by: Xiaoqian Dai <xdai@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1012093}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3705869
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5060@{#852}
Cr-Branched-From: b83393d0f4038aeaf67f970a024d8101df7348d1-refs/heads/main@{#1002911}

[modify] https://crrev.com/639f6de5f197741717a2d910b531bd59231dbef8/ash/wm/overview/overview_session_unittest.cc
[modify] https://crrev.com/639f6de5f197741717a2d910b531bd59231dbef8/ash/wm/overview/overview_session.cc
[modify] https://crrev.com/639f6de5f197741717a2d910b531bd59231dbef8/ash/wm/overview/overview_window_drag_controller.cc


### [Deleted User] (2022-06-14)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-06-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-16)

Congratulations, Khalil on another one. The VRP Panel has decided to award you $3,000 for this report since this issue is not web accessible and is additionally mitigated by requiring user interaction. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-06-16)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-06-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-06-21)

https://crbug.com/chromium/1325023 was an earlier reported version of this issue, that issue should receive any acknowledgement and also considered for potential VRP reward 

### rz...@google.com (2022-06-27)

[Empty comment from Monorail migration]

### rz...@google.com (2022-06-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-27)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-06-27)

1. Just https://crrev.com/c/3726067
2. Low, a conflict on overview_window_drag_controller regarding a call that is present on the CL and not in M96.
3. 103
4. Yes

### gm...@google.com (2022-06-27)

[Empty comment from Monorail migration]

### gm...@google.com (2022-07-01)

Approved for 96. Leaving the LTS-Merge-Candidate label to merge to 102.

### gi...@appspot.gserviceaccount.com (2022-07-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0225901b4d1bcb3e8ebe6c1834f169e189944264

commit 0225901b4d1bcb3e8ebe6c1834f169e189944264
Author: Sammie Quon <sammiequon@chromium.org>
Date: Tue Jul 05 10:27:34 2022

[M96-LTS] overview: Fix u-a-f when snapping a fullscreen window in tablet.

M96 merge issues:
  overview_window_drag_controller.cc:
    set_snap_action_source() isn't called on M96. Kept M96 version and
    applied the fix for item_.

Fixed: 1330042
Test: ash_unittests TabletModeOverviewSessionTest.SnappingFullscreenWindow

(cherry picked from commit cb8d2046dccda41a687b9abe537a2d7361572c57)

Change-Id: I41ae7af0254ca69dc5bfa06bd860ffa62c2c7bef
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3692092
Commit-Queue: Sammie Quon <sammiequon@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1012093}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3726067
Reviewed-by: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1656}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/0225901b4d1bcb3e8ebe6c1834f169e189944264/ash/wm/overview/overview_session_unittest.cc
[modify] https://crrev.com/0225901b4d1bcb3e8ebe6c1834f169e189944264/ash/wm/overview/overview_session.cc
[modify] https://crrev.com/0225901b4d1bcb3e8ebe6c1834f169e189944264/ash/wm/overview/overview_window_drag_controller.cc


### rz...@google.com (2022-07-05)

[Empty comment from Monorail migration]

### gm...@google.com (2022-07-11)

@rzanoni this needs to be merged to 102.

### gm...@google.com (2022-07-11)

[Empty comment from Monorail migration]

### rz...@google.com (2022-07-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-15)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-07-15)

1. https://crrev.com/c/3755551
2. Low, no conflicts
3. 103
4. Yes

### gm...@google.com (2022-07-18)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-07-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1f032498a111ae63e39a66149854e1809857cb82

commit 1f032498a111ae63e39a66149854e1809857cb82
Author: Sammie Quon <sammiequon@chromium.org>
Date: Tue Jul 19 13:30:23 2022

[M102-LTS] overview: Fix u-a-f when snapping a fullscreen window in tablet.

Fixed: 1330042
Test: ash_unittests TabletModeOverviewSessionTest.SnappingFullscreenWindow

(cherry picked from commit cb8d2046dccda41a687b9abe537a2d7361572c57)

Change-Id: I41ae7af0254ca69dc5bfa06bd860ffa62c2c7bef
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3692092
Commit-Queue: Sammie Quon <sammiequon@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1012093}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3755551
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Owners-Override: Simon Hangl <simonha@google.com>
Reviewed-by: Simon Hangl <simonha@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1267}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/1f032498a111ae63e39a66149854e1809857cb82/ash/wm/overview/overview_session_unittest.cc
[modify] https://crrev.com/1f032498a111ae63e39a66149854e1809857cb82/ash/wm/overview/overview_session.cc
[modify] https://crrev.com/1f032498a111ae63e39a66149854e1809857cb82/ash/wm/overview/overview_window_drag_controller.cc


### rz...@google.com (2022-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1330042?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1325023]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059787)*
