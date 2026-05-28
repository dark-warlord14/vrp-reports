# Security: heap-after-free on ash/wm/splitview/split_view_controller.cc (chromeOS)

| Field | Value |
|-------|-------|
| **Issue ID** | [40059657](https://issues.chromium.org/issues/40059657) |
| **Status** | Accepted |
| **Severity** | Unknown |
| **Priority** | P4 |
| **Component** | UI>Shell |
| **Platforms** | ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | af...@chromium.org |
| **Created** | 2022-05-12 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

This Uaf occurs on tablet mode + extended display and use a crafted html.  

Without a crafted html given, I'm sure the crash will not happen. So I believe the crafted html file that run in the browser can trigger a crash and is very much needed.

Tested with Chrome or Lacros.

**VERSION**  

Chrome Version: Chromium 103.0.5058.0  

Operating System: Linux-chromeOS

**REPRODUCTION CASE**  

(\*) Enable tablet mode + extended display.  

(0) Navigate to <https://rhezashan.github.io/pocs/poc2.html>.  

(1) Click me and select display 2.  

(2) Drag the video window and release.

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

==2310997==ERROR: AddressSanitizer: heap-use-after-free on address 0x614000451950 at pc 0x7f1b4485ba9a bp 0x7ffdaf29e400 sp 0x7ffdaf29e3f8  

READ of size 8 at 0x614000451950 thread T0 (chrome)  

SCARINESS: 51 (8-byte-read-heap-use-after-free)  

#0 0x7f1b4485ba99 in reset buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:312:28  

#1 0x7f1b4485ba99 in ash::OverviewItem::DestroyPhantomsForDragging() ash/wm/overview/overview\_item.cc:716:26  

#2 0x7f1b44876590 in ash::OverviewWindowDragController::ResetGesture() ash/wm/overview/overview\_window\_drag\_controller.cc:426:12  

#3 0x7f1b448670bc in ash::OverviewSession::ResetDraggedWindowGesture() ash/wm/overview/overview\_session.cc:650:28  

#4 0x7f1b448696fb in ash::OverviewSession::OnDisplayMetricsChanged(display::Display const&, unsigned int) ash/wm/overview/overview\_session.cc:1159:5  

#5 0x7f1b47a6c866 in display::DisplayManager::NotifyMetricsChanged(display::Display const&, unsigned int) ui/display/manager/display\_manager.cc:2202:14  

#6 0x7f1b47a6ce74 in display::DisplayManager::UpdateWorkAreaOfDisplay(long, gfx::Insets const&) ui/display/manager/display\_manager.cc:507:5  

#7 0x7f1b442f7336 in ash::ShelfLayoutManager::UpdateBoundsAndOpacity(bool) ash/shelf/shelf\_layout\_manager.cc:1639:25  

#8 0x7f1b442f83f9 in ash::ShelfLayoutManager::SetState(ash::ShelfVisibilityState) ash/shelf/shelf\_layout\_manager.cc:1344:3  

#9 0x7f1b442f2f0a in ash::ShelfLayoutManager::UpdateVisibilityState() ash/shelf/shelf\_layout\_manager.cc  

#10 0x7f1b44947f83 in UpdateShelfVisibility ash/wm/workspace/workspace\_layout\_manager.cc:509:37  

#11 0x7f1b44947f83 in ash::WorkspaceLayoutManager::OnPostWindowStateTypeChange(ash::WindowState\*, chromeos::WindowStateType) ash/wm/workspace/workspace\_layout\_manager.cc:386:3  

#12 0x7f1b449280e8 in ash::WindowState::NotifyPostStateTypeChange(chromeos::WindowStateType) ash/wm/window\_state.cc:852:14  

#13 0x7f1b44770d52 in ash::DefaultState::EnterToNextState(ash::WindowState\*, chromeos::WindowStateType) ash/wm/default\_state.cc:473:17  

#14 0x7f1b447706ef in ash::DefaultState::HandleTransitionEvents(ash::WindowState\*, ash::WMEvent const\*) ash/wm/default\_state.cc:377:3  

#15 0x7f1b44921521 in ash::WindowState::OnWMEvent(ash::WMEvent const\*) ash/wm/window\_state.cc:453:19  

#16 0x7f1b4492a2b5 in ash::WindowState::OnWindowPropertyChanged(aura::Window\*, void const\*, long) ash/wm/window\_state.cc:1121:7  

#17 0x7f1b47c77bca in aura::Window::AfterPropertyChange(void const\*, long) ui/aura/window.cc:949:14  

#18 0x7f1b4928fdcd in ui::PropertyHandler::SetPropertyInternal(void const\*, char const\*, void (\*)(long), long, long) ui/base/class\_property.cc:43:3  

#19 0x7f1b47c59904 in void ui::subtle::PropertyHelper::Set[ui::WindowShowState](javascript:void(0);)(ui::PropertyHandler\*, ui::ClassProperty[ui::WindowShowState](javascript:void(0);) const\*, ui::WindowShowState) ui/base/class\_property.h:204:28  

#20 0x7f1b46da0813 in wm::SetWindowFullscreen(aura::Window\*, bool) ui/wm/core/window\_util.cc:119:13  

#21 0x7f1b4731ff55 in views::Widget::SetFullscreen(bool, long) ui/views/widget/widget.cc:818:19  

#22 0x7f1b44934e2c in ash::BackdropController::Layout() ash/wm/workspace/backdrop\_controller.cc:628:14  

#23 0x7f1b44933fbb in ash::BackdropController::Show() ash/wm/workspace/backdrop\_controller.cc:534:3  

#24 0x7f1b44932ede in ash::BackdropController::UpdateBackdropInternal() ash/wm/workspace/backdrop\_controller.cc  

#25 0x7f1b4489d8b9 in ash::SplitViewController::UpdateStateAndNotifyObservers() ash/wm/splitview/split\_view\_controller.cc:2065:14  

#26 0x7f1b448a4dda in ash::SplitViewController::OnWindowSnapped(aura::Window\*) ash/wm/splitview/split\_view\_controller.cc:2326:3  

#27 0x7f1b448a4c2f in ash::SplitViewController::OnPostWindowStateTypeChange(ash::WindowState\*, chromeos::WindowStateType) ash/wm/splitview/split\_view\_controller.cc:1659:5  

#28 0x7f1b449280e8 in ash::WindowState::NotifyPostStateTypeChange(chromeos::WindowStateType) ash/wm/window\_state.cc:852:14  

#29 0x7f1b448e5108 in ash::TabletModeWindowState::UpdateWindow(ash::WindowState\*, chromeos::WindowStateType, bool) ash/wm/tablet\_mode/tablet\_mode\_window\_state.cc:469:17  

#30 0x7f1b448e480b in ash::TabletModeWindowState::OnWMEvent(ash::WindowState\*, ash::WMEvent const\*) ash/wm/tablet\_mode/tablet\_mode\_window\_state.cc  

#31 0x7f1b44921521 in ash::WindowState::OnWMEvent(ash::WMEvent const\*) ash/wm/window\_state.cc:453:19  

#32 0x7f1b4489b655 in ash::SplitViewController::SnapWindow(aura::Window\*, ash::SplitViewController::SnapPosition, bool) ash/wm/splitview/split\_view\_controller.cc:851:29  

#33 0x7f1b4487643e in ash::OverviewWindowDragController::SnapWindow(ash::SplitViewController\*, ash::SplitViewController::SnapPosition) ash/wm/overview/overview\_window\_drag\_controller.cc:821:26  

#34 0x7f1b448753a4 in ash::OverviewWindowDragController::CompleteNormalDrag(gfx::PointF const&) ash/wm/overview/overview\_window\_drag\_controller.cc:691:5  

#35 0x7f1b44874ae0 in ash::OverviewWindowDragController::CompleteDrag(gfx::PointF const&) ash/wm/overview/overview\_window\_drag\_controller.cc:282:16  

#36 0x7f1b44866e47 in ash::OverviewSession::CompleteDrag(ash::OverviewItem\*, gfx::PointF const&) ash/wm/overview/overview\_session.cc:614:46  

#37 0x7f1b4485c3c2 in ash::OverviewItem::HandleGestureEventForTabletModeLayout(ui::GestureEvent\*) ash/wm/overview/overview\_item.cc:871:9  

#38 0x7f1b4485cb34 in ash::OverviewItem::HandleGestureEvent(ui::GestureEvent\*) ash/wm/overview/overview\_item.cc:920:5  

#39 0x7f1b4486077a in ash::OverviewItemView::OnGestureEvent(ui::GestureEvent\*) ash/wm/overview/overview\_item\_view.cc:302:19  

#40 0x7f1b47e288f5 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ui/events/event\_dispatcher.cc:190:12  

#41 0x7f1b47e27dd0 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:139:5  

#42 0x7f1b47e278b7 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:83:14  

#43 0x7f1b47e2766e in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:55:15  

#44 0x7f1b47e2acc7 in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:49:17  

#45 0x7f1b47e2d4b4 in ui::EventSource::DeliverEventToSink(ui::Event\*) ui/events/event\_source.cc:118:16  

#46 0x7f1b47e2d1b0 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const\*, ui::EventRewriter const\*) ui/events/event\_source.cc:143:12  

#47 0x7f1b47e288f5 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ui/events/event\_dispatcher.cc:190:12  

#48 0x7f1b47e27dd0 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:139:5  

#49 0x7f1b47e278b7 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:83:14  

#50 0x7f1b47e2766e in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:55:15  

#51 0x7f1b47c8a00b in aura::WindowEventDispatcher::ProcessGestures(aura::Window\*, std::\_\_Cr::vector<std::\_\_Cr::unique\_ptr<ui::GestureEvent, std::\_\_Cr::default\_delete[ui::GestureEvent](javascript:void(0);) >, std::\_\_Cr::allocator<std::\_\_Cr::unique\_ptr<ui::GestureEvent, std::\_\_Cr::default\_delete[ui::GestureEvent](javascript:void(0);) > > >) ui/aura/window\_event\_dispatcher.cc:352:15  

#52 0x7f1b47c8f53e in aura::WindowEventDispatcher::PostDispatchEvent(ui::EventTarget\*, ui::Event const&) ui/aura/window\_event\_dispatcher.cc:606:16  

#53 0x7f1b47e276c2 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:59:15  

#54 0x7f1b47e2acc7 in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:49:17  

#55 0x7f1b47e2d4b4 in ui::EventSource::DeliverEventToSink(ui::Event\*) ui/events/event\_source.cc:118:16  

#56 0x7f1b47e2d9b4 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:66:14  

#57 0x7f1b47e2c071 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#58 0x7f1b44f1e02c in ui::EventRewriterChromeOS::RewriteTouchEvent(ui::TouchEvent const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ui/chromeos/events/event\_rewriter\_chromeos.cc:1314:12  

#59 0x7f1b44f1b57a in ui::EventRewriterChromeOS::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ui/chromeos/events/event\_rewriter\_chromeos.cc:766:12  

#60 0x7f1b47e2d964 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#61 0x7f1b47e2c071 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#62 0x7f1b440af0fc in ash::KeyboardDrivenEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/events/keyboard\_driven\_event\_rewriter.cc:31:12  

#63 0x7f1b47e2d964 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#64 0x7f1b47e2c071 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#65 0x7f1b440aad58 in ash::AccessibilityEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/events/accessibility\_event\_rewriter.cc  

#66 0x7f1b47e2d964 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#67 0x7f1b47e2c071 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#68 0x7f1b43e61c1e in ash::AutoclickDragEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/accessibility/autoclick/autoclick\_drag\_event\_rewriter.cc  

#69 0x7f1b47e2d964 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#70 0x7f1b47e2c071 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#71 0x7f1b43e84c70 in ash::FullscreenMagnifierController::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/accessibility/magnifier/fullscreen\_magnifier\_controller.cc  

#72 0x7f1b47e2d157 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const\*, ui::EventRewriter const\*) ui/events/event\_source.cc:144:29  

#73 0x7f1b47cb3bab in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event\*) ui/aura/window\_tree\_host\_platform.cc:229:38  

#74 0x7f1b440faf92 in ash::AshWindowTreeHostPlatform::DispatchEvent(ui::Event\*) ash/host/ash\_window\_tree\_host\_platform.cc:207:40  

#75 0x7f1b47e3e037 in Run base/callback.h:143:12  

#76 0x7f1b47e3e037 in ui::DispatchEventFromNativeUiEvent(ui::Event\* const&, base::OnceCallback<void (ui::Event\*)>) ui/events/ozone/events\_ozone.cc:40:25  

#77 0x7f1b477bd7c5 in ui::X11Window::DispatchUiEvent(ui::Event\*, x11::Event const&) ui/ozone/platform/x11/x11\_window.cc:1294:3  

#78 0x7f1b477bd017 in ui::X11Window::DispatchEvent(ui::Event\* const&) ui/ozone/platform/x11/x11\_window.cc:1247:3  

#79 0x7f1b477bdb00 in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event\* const&) ui/ozone/platform/x11/x11\_window.cc  

#80 0x7f1b53913387 in ui::PlatformEventSource::DispatchEvent(ui::Event\*) ui/events/platform/platform\_event\_source.cc:99:29  

#81 0x7f1aff18d1c5 in ui::X11EventSource::OnEvent(x11::Event const&) ui/events/platform/x11/x11\_event\_source.cc:287:5  

#82 0x7f1afee4ef5d in x11::Connection::DispatchEvent(x11::Event const&) ui/gfx/x/connection.cc:457:14  

#83 0x7f1afee4ec6b in x11::Connection::ProcessNextEvent() ui/gfx/x/connection.cc:508:3  

#84 0x7f1afee4e873 in x11::Connection::Dispatch() ui/gfx/x/connection.cc  

#85 0x7f1aff197793 in ui::X11EventWatcherFdWatch::OnFileCanReadWithoutBlocking(int) ui/events/platform/x11/x11\_event\_watcher\_fdwatch.cc:64:15  

#86 0x7f1b58770ffa in base::MessagePumpLibevent::OnLibeventNotification(int, short, void\*) base/message\_loop/message\_pump\_libevent.cc  

#87 0x7f1b58866e5b in event\_process\_active base/third\_party/libevent/event.c:381:4  

#88 0x7f1b58866e5b in event\_base\_loop base/third\_party/libevent/event.c:521:4  

#89 0x7f1b58771916 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_libevent.cc:204:7  

#90 0x7f1b586484cb in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:497:12  

#91 0x7f1b5855f2ef in base::RunLoop::Run(base::Location const&) base/run\_loop.cc:141:14  

#92 0x7f1b39b005a0 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser\_main\_loop.cc:1055:18  

#93 0x7f1b39b04e0b in content::BrowserMainRunnerImpl::Run() content/browser/browser\_main\_runner\_impl.cc:157:15  

#94 0x7f1b39afac0a in content::BrowserMain(content::MainFunctionParams) content/browser/browser\_main.cc:30:28  

#95 0x7f1b3ba15ac9 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:658:10  

#96 0x7f1b3ba185ca in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content\_main\_runner\_impl.cc:1165:10  

#97 0x7f1b3ba17a14 in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner\_impl.cc:1037:12  

#98 0x7f1b3ba11522 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) content/app/content\_main.cc:407:36  

#99 0x7f1b3ba12714 in content::ContentMain(content::ContentMainParams) content/app/content\_main.cc:435:10  

#100 0x55909d764420 in ChromeMain chrome/app/chrome\_main.cc:177:12  

#101 0x7f1b00578082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

0x614000451950 is located 272 bytes inside of 392-byte region [0x614000451840,0x6140004519c8)  

freed by thread T0 (chrome) here:  

#0 0x55909d7624bd in operator delete(void\*) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:152:3  

#1 0x7f1b4483aee1 in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:54:5  

#2 0x7f1b4483aee1 in reset buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:315:7  

#3 0x7f1b4483aee1 in ash::OverviewGrid::RemoveItem(ash::OverviewItem\*, bool, bool) ash/wm/overview/overview\_grid.cc:731:7  

#4 0x7f1b44865b28 in ash::OverviewSession::RemoveItem(ash::OverviewItem\*, bool, bool) ash/wm/overview/overview\_session.cc:557:35  

#5 0x7f1b4489bfac in RemoveSnappingWindowFromOverviewIfApplicable ash/wm/splitview/split\_view\_controller.cc:232:21  

#6 0x7f1b4489bfac in ash::SplitViewController::AttachSnappingWindow(aura::Window\*, ash::SplitViewController::SnapPosition) ash/wm/splitview/split\_view\_controller.cc:900:3  

#7 0x7f1b44927a55 in ash::WindowState::NotifyPreStateTypeChange(chromeos::WindowStateType) ash/wm/window\_state.cc:845:14  

#8 0x7f1b448e4ff7 in ash::TabletModeWindowState::UpdateWindow(ash::WindowState\*, chromeos::WindowStateType, bool) ash/wm/tablet\_mode/tablet\_mode\_window\_state.cc:449:17  

#9 0x7f1b448e480b in ash::TabletModeWindowState::OnWMEvent(ash::WindowState\*, ash::WMEvent const\*) ash/wm/tablet\_mode/tablet\_mode\_window\_state.cc  

#10 0x7f1b44921521 in ash::WindowState::OnWMEvent(ash::WMEvent const\*) ash/wm/window\_state.cc:453:19  

#11 0x7f1b4489b655 in ash::SplitViewController::SnapWindow(aura::Window\*, ash::SplitViewController::SnapPosition, bool) ash/wm/splitview/split\_view\_controller.cc:851:29  

#12 0x7f1b4487643e in ash::OverviewWindowDragController::SnapWindow(ash::SplitViewController\*, ash::SplitViewController::SnapPosition) ash/wm/overview/overview\_window\_drag\_controller.cc:821:26  

#13 0x7f1b448753a4 in ash::OverviewWindowDragController::CompleteNormalDrag(gfx::PointF const&) ash/wm/overview/overview\_window\_drag\_controller.cc:691:5  

#14 0x7f1b44874ae0 in ash::OverviewWindowDragController::CompleteDrag(gfx::PointF const&) ash/wm/overview/overview\_window\_drag\_controller.cc:282:16  

#15 0x7f1b44866e47 in ash::OverviewSession::CompleteDrag(ash::OverviewItem\*, gfx::PointF const&) ash/wm/overview/overview\_session.cc:614:46  

#16 0x7f1b4485c3c2 in ash::OverviewItem::HandleGestureEventForTabletModeLayout(ui::GestureEvent\*) ash/wm/overview/overview\_item.cc:871:9  

#17 0x7f1b4485cb34 in ash::OverviewItem::HandleGestureEvent(ui::GestureEvent\*) ash/wm/overview/overview\_item.cc:920:5  

#18 0x7f1b4486077a in ash::OverviewItemView::OnGestureEvent(ui::GestureEvent\*) ash/wm/overview/overview\_item\_view.cc:302:19  

#19 0x7f1b47e288f5 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ui/events/event\_dispatcher.cc:190:12  

#20 0x7f1b47e27dd0 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:139:5  

#21 0x7f1b47e278b7 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:83:14  

#22 0x7f1b47e2766e in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:55:15  

#23 0x7f1b47e2acc7 in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:49:17  

#24 0x7f1b47e2d4b4 in ui::EventSource::DeliverEventToSink(ui::Event\*) ui/events/event\_source.cc:118:16  

#25 0x7f1b47e2d1b0 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const\*, ui::EventRewriter const\*) ui/events/event\_source.cc:143:12  

#26 0x7f1b47e288f5 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ui/events/event\_dispatcher.cc:190:12  

#27 0x7f1b47e27dd0 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:139:5  

#28 0x7f1b47e278b7 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:83:14  

#29 0x7f1b47e2766e in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:55:15  

#30 0x7f1b47c8a00b in aura::WindowEventDispatcher::ProcessGestures(aura::Window\*, std::\_\_Cr::vector<std::\_\_Cr::unique\_ptr<ui::GestureEvent, std::\_\_Cr::default\_delete[ui::GestureEvent](javascript:void(0);) >, std::\_\_Cr::allocator<std::\_\_Cr::unique\_ptr<ui::GestureEvent, std::\_\_Cr::default\_delete[ui::GestureEvent](javascript:void(0);) > > >) ui/aura/window\_event\_dispatcher.cc:352:15  

#31 0x7f1b47c8f53e in aura::WindowEventDispatcher::PostDispatchEvent(ui::EventTarget\*, ui::Event const&) ui/aura/window\_event\_dispatcher.cc:606:16  

#32 0x7f1b47e276c2 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:59:15

previously allocated by thread T0 (chrome) here:  

#0 0x55909d761c5d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:95:3  

#1 0x7f1b44832476 in make\_unique<ash::OverviewItem, aura::Window \*&, ash::OverviewSession \*&, ash::OverviewGrid \*> buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:725:28  

#2 0x7f1b44832476 in ash::OverviewGrid::OverviewGrid(aura::Window\*, std::\_\_Cr::vector<aura::Window\*, std::\_\_Cr::allocator[aura::Window\\*](javascript:void(0);) > const&, ash::OverviewSession\*) ash/wm/overview/overview\_grid.cc:450:9  

#3 0x7f1b448622b9 in make\_unique<ash::OverviewGrid, aura::Window \*&, const std::\_\_Cr::vector<aura::Window \*, std::\_\_Cr::allocator<aura::Window \*> > &, ash::OverviewSession \*> buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:725:32  

#4 0x7f1b448622b9 in ash::OverviewSession::Init(std::\_\_Cr::vector<aura::Window\*, std::\_\_Cr::allocator[aura::Window\\*](javascript:void(0);) > const&, std::\_\_Cr::vector<aura::Window\*, std::\_\_Cr::allocator[aura::Window\\*](javascript:void(0);) > const&) ash/wm/overview/overview\_session.cc:205:17  

#5 0x7f1b4482c962 in ash::OverviewController::ToggleOverview(ash::OverviewEnterExitType) ash/wm/overview/overview\_controller.cc:431:24  

#6 0x7f1b4482bd5d in ash::OverviewController::StartOverview(ash::OverviewStartAction, ash::OverviewEnterExitType) ash/wm/overview/overview\_controller.cc:129:3  

#7 0x7f1b43e11d7a in ash::(anonymous namespace)::HandleToggleOverview() ash/accelerators/accelerator\_controller\_impl.cc:882:26  

#8 0x7f1b43e0914f in ash::AcceleratorControllerImpl::PerformAction(ash::AcceleratorAction, ui::Accelerator const&) ash/accelerators/accelerator\_controller\_impl.cc:2469:7  

#9 0x7f1b43e0a7b5 in ash::AcceleratorControllerImpl::AcceleratorPressed(ui::Accelerator const&) ash/accelerators/accelerator\_controller\_impl.cc:1733:3  

#10 0x7f1b492fd69e in TryProcess ui/base/accelerators/accelerator\_manager.cc:153:17  

#11 0x7f1b492fd69e in ui::AcceleratorManager::Process(ui::Accelerator const&) ui/base/accelerators/accelerator\_manager.cc:83:27  

#12 0x7f1b43e26c35 in ash::PreTargetAcceleratorHandler::ProcessAccelerator(ui::KeyEvent const&, ui::Accelerator const&) ash/accelerators/pre\_target\_accelerator\_handler.cc:74:45  

#13 0x7f1b46d791b5 in wm::AcceleratorFilter::OnKeyEvent(ui::KeyEvent\*) ui/wm/core/accelerator\_filter.cc:51:18  

#14 0x7f1b47e288f5 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ui/events/event\_dispatcher.cc:190:12  

#15 0x7f1b47e28619 in ui::EventDispatcher::DispatchEventToEventHandlers(std::\_\_Cr::vector<ui::EventHandler\*, std::\_\_Cr::allocator[ui::EventHandler\\*](javascript:void(0);) >\*, ui::Event\*) ui/events/event\_dispatcher.cc:177:7  

#16 0x7f1b47e27c1d in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:125:3  

#17 0x7f1b47e278b7 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:83:14  

#18 0x7f1b47e2766e in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:55:15  

#19 0x7f1b47e2acc7 in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:49:17  

#20 0x7f1b47cabd48 in aura::WindowTreeHost::DispatchKeyEventPostIME(ui::KeyEvent\*) ui/aura/window\_tree\_host.cc:373:23  

#21 0x7f1b47be0711 in ui::InputMethodBase::DispatchKeyEventPostIME(ui::KeyEvent\*) const ui/base/ime/input\_method\_base.cc:140:33  

#22 0x7f1b2d1fd769 in ui::InputMethodAsh::ProcessUnfilteredKeyPressEvent(ui::KeyEvent\*) ui/base/ime/ash/input\_method\_ash.cc:616:38  

#23 0x7f1b2d1fcf86 in ui::InputMethodAsh::DispatchKeyEvent(ui::KeyEvent\*) ui/base/ime/ash/input\_method\_ash.cc:139:14  

#24 0x7f1b47c8f085 in aura::WindowEventDispatcher::PreDispatchKeyEvent(aura::Window\*, ui::KeyEvent\*) ui/aura/window\_event\_dispatcher.cc:1080:54  

#25 0x7f1b47c8da2c in aura::WindowEventDispatcher::PreDispatchEvent(ui::EventTarget\*, ui::Event\*) ui/aura/window\_event\_dispatcher.cc:568:15  

#26 0x7f1b47e27622 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:51:34  

#27 0x7f1b47e2acc7 in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:49:17  

#28 0x7f1b47e2d4b4 in ui::EventSource::DeliverEventToSink(ui::Event\*) ui/events/event\_source.cc:118:16  

#29 0x7f1b47e2c22d in ui::EventRewriter::SendEventFinally(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:94:39  

#30 0x7f1b44f1d204 in ui::EventRewriterChromeOS::RewriteKeyEventInContext(ui::KeyEvent const&, std::\_\_Cr::unique\_ptr<ui::Event, std::\_\_Cr::default\_delete[ui::Event](javascript:void(0);) >, ui::EventRewriteStatus, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ui/chromeos/events/event\_rewriter\_chromeos.cc:1837:9  

#31 0x7f1b44f1b657 in ui::EventRewriterChromeOS::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ui/chromeos/events/event\_rewriter\_chromeos.cc:751:12  

#32 0x7f1b47e2d964 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32

SUMMARY: AddressSanitizer: heap-use-after-free buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:312:28 in reset  

Shadow bytes around the buggy address:  

0x0c28800822d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c28800822e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c28800822f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 fa fa  

0x0c2880082300: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c2880082310: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x0c2880082320: fd fd fd fd fd fd fd fd fd fd[fd]fd fd fd fd fd  

0x0c2880082330: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa  

0x0c2880082340: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c2880082350: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2880082360: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2880082370: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa  

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

==2310997==ABORTING

## Attachments

- [screencast_1325023.webm](attachments/screencast_1325023.webm) (video/webm, 6.4 MB)
- [after-1012093.webm](attachments/after-1012093.webm) (video/webm, 3.9 MB)
- [before-1012093.webm](attachments/before-1012093.webm) (video/webm, 10.0 MB)

## Timeline

### [Deleted User] (2022-05-12)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-05-12)

hello thank you for your report. This is in ChromeOS so I'm passing it to the ChromeOS security bug triage team.

### rh...@gmail.com (2022-05-12)

uploading screencast

### mo...@chromium.org (2022-05-24)

[Empty comment from Monorail migration]

[Monorail components: UI>Shell]

### [Deleted User] (2022-05-24)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-06-08)

Hello Afakhry and Security team,

I think this issue was fixed by https://chromium.googlesource.com/chromium/src/+/cb8d2046dccda41a687b9abe537a2d7361572c57 (issue #1330042). I did test before and after version r1012093. Please refer the screencast.

One question, since this https://crbug.com/chromium/1325023 submitted earlier than issue #1330042, can you asses set up appropriate? 

### rh...@gmail.com (2022-06-09)

the repro steps in video `before-1012093.webm` is different from step in https://crbug.com/chromium/1325023#c0, but the stack trace is identically same. Screencast `before-1012093.webm` doesn't need external display and fewer steps than steps in https://crbug.com/chromium/1325023#c0.

### rh...@gmail.com (2022-06-14)

Can someone help me on this issue?  Please see https://crbug.com/chromium/1325023#c6 and https://crbug.com/chromium/1325023#c7, while this crash no longer happen after version 1012093 https://chromium.googlesource.com/chromium/src/+/cb8d2046dccda41a687b9abe537a2d7361572c57 (issue #1330042).

### am...@chromium.org (2022-06-16)

Hi Sammie, could you PTAL at this one? Looks like https://chromium-review.googlesource.com/c/chromium/src/+/3692092 may have resolved this issue and the stack traces for this and https://crbug.com/chromium/1330042 appear to be similar, if not identical. Can you confirm if https://crbug.com/chromium/1330042 is indeed a duplicate of this issue? 


If this issue is indeed a duplicate we cannot merge that issue into this one, since the fix commit landed there and we will need to manually ensure this issue goes to VRP Panel for an assessment of a potential reward. 
Thank you. 

### sa...@chromium.org (2022-06-16)

yup this is a duplicate (or the other is a duplicate of this)

### am...@chromium.org (2022-06-21)

This is being merged into https://crbug.com/chromium/1330042, because the fix CL was landed on that issue. This is earlier reported version of that issue and should be considered for VRP evaluation for potential VRP reward. 

### am...@chromium.org (2022-06-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-06-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-24)

Congratulations! The VRP Panel has decided to award you $3,000 for this report due to that this issue is substantially mitigated by user interactions required to trigger this issue. Thank you for your efforts and reporting this issue to us!

### am...@google.com (2022-07-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-11-21)

Hello, we consider attachments/POCs included with reports to be an integral part of the report (https://g.co/chrome/vrp), so I've undeleted them.

### is...@google.com (2022-11-21)

This issue was migrated from crbug.com/chromium/1325023?no_tracker_redirect=1

[Monorail mergedinto: crbug.com/chromium/1330042]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059657)*
