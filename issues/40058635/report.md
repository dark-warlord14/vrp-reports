# Security: heap-use-after-free on ash/wm/desks/desks_controller.cc (chromeOS)

| Field | Value |
|-------|-------|
| **Issue ID** | [40058635](https://issues.chromium.org/issues/40058635) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Shell |
| **Platforms** | ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2022-01-29 |
| **Bounty** | $7,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36

Steps to reproduce the problem:
I will post screen-cast and details on next comment

What is the expected behavior?
not crash

What went wrong?
=================================================================
==63195==ERROR: AddressSanitizer: heap-use-after-free on address 0x6150007ad918 at pc 0x56290ad28a98 bp 0x7fff62887070 sp 0x7fff62887068
READ of size 8 at 0x6150007ad918 thread T0 (chrome)
    #0 0x56290ad28a97 in begin buildtools/third_party/libc++/trunk/include/vector:1526:30
    #1 0x56290ad28a97 in aura::WindowTracker::WindowTracker(std::__1::vector<aura::Window*, std::__1::allocator<aura::Window*> > const&) ui/aura/window_tracker.cc:13:23
    #2 0x56290acf34b5 in aura::Window::CleanupGestureState() ui/aura/window.cc:1265:17
    #3 0x56290acf3511 in aura::Window::CleanupGestureState() ui/aura/window.cc:1268:30
    #4 0x56290ad0dbd7 in aura::WindowEventDispatcher::OnWindowHidden(aura::Window*, aura::WindowEventDispatcher::WindowHiddenReason) ui/aura/window_event_dispatcher.cc:374:14
    #5 0x56290ad123ea in aura::WindowEventDispatcher::OnWindowVisibilityChanged(aura::Window*, bool) ui/aura/window_event_dispatcher.cc:681:5
    #6 0x56290acfeb26 in aura::Window::NotifyWindowVisibilityChangedAtReceiver(aura::Window*, bool) ui/aura/window.cc:1218:14
    #7 0x56290acfe69a in aura::Window::NotifyWindowVisibilityChangedDown(aura::Window*, bool) ui/aura/window.cc:1224:8
    #8 0x56290acfcb1d in aura::Window::NotifyWindowVisibilityChanged(aura::Window*, bool) ui/aura/window.cc:1205:8
    #9 0x56290acf577e in aura::Window::SetVisibleInternal(bool) ui/aura/window.cc:1021:3
    #10 0x56290ba5d452 in ash::Desk::Deactivate(bool) ash/wm/desks/desk.cc:430:40
    #11 0x56290ba66a70 in ash::DesksController::ActivateDeskInternal(ash::Desk const*, bool) ash/wm/desks/desks_controller.cc:1210:15
    #12 0x56290ba63808 in ash::DesksController::ActivateDesk(ash::Desk const*, ash::DesksSwitchSource) ash/wm/desks/desks_controller.cc
    #13 0x56290ba658fd in ash::DesksController::RemoveDeskInternal(ash::Desk const*, ash::DesksCreationRemovalSource) ash/wm/desks/desks_controller.cc:1335:5
    #14 0x56290ba64eec in ash::DesksController::RemoveDesk(ash::Desk const*, ash::DesksCreationRemovalSource) ash/wm/desks/desks_controller.cc:452:3
    #15 0x56290b1e88bc in ash::(anonymous namespace)::HandleRemoveCurrentDesk() ash/accelerators/accelerator_controller_impl.cc:366:21
    #16 0x56290b1e45b5 in ash::AcceleratorControllerImpl::PerformAction(ash::AcceleratorAction, ui::Accelerator const&) ash/accelerators/accelerator_controller_impl.cc:2083:7
    #17 0x56290b1e56e7 in ash::AcceleratorControllerImpl::AcceleratorPressed(ui::Accelerator const&) ash/accelerators/accelerator_controller_impl.cc:1700:3
    #18 0x56290b0a3436 in TryProcess ui/base/accelerators/accelerator_manager.cc:153:17
    #19 0x56290b0a3436 in ui::AcceleratorManager::Process(ui::Accelerator const&) ui/base/accelerators/accelerator_manager.cc:83:27
    #20 0x56290b65c21f in wm::AcceleratorFilter::OnKeyEvent(ui::KeyEvent*) ui/wm/core/accelerator_filter.cc:51:18
    #21 0x5629078ceb5b in ui::EventDispatcher::DispatchEvent(ui::EventHandler*, ui::Event*) ui/events/event_dispatcher.cc:190:12
    #22 0x5629078ce949 in ui::EventDispatcher::DispatchEventToEventHandlers(std::__1::vector<ui::EventHandler*, std::__1::allocator<ui::EventHandler*> >*, ui::Event*) ui/events/event_dispatcher.cc:177:7
    #23 0x5629078cdf6d in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:125:3
    #24 0x5629078cdbf4 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:83:14
    #25 0x5629078cd960 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:55:15
    #26 0x56290ad162bf in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #27 0x56290ad2c786 in aura::WindowTreeHost::DispatchKeyEventPostIME(ui::KeyEvent*) ui/aura/window_tree_host.cc:364:23
    #28 0x562907b757f5 in ui::InputMethodBase::DispatchKeyEventPostIME(ui::KeyEvent*) const ui/base/ime/input_method_base.cc:139:33
    #29 0x562907d01b19 in ui::InputMethodAsh::ProcessUnfilteredKeyPressEvent(ui::KeyEvent*) ui/base/ime/ash/input_method_ash.cc:599:38
    #30 0x562907d01379 in ui::InputMethodAsh::DispatchKeyEvent(ui::KeyEvent*) ui/base/ime/ash/input_method_ash.cc:139:14
    #31 0x56290ad111f3 in aura::WindowEventDispatcher::PreDispatchKeyEvent(aura::Window*, ui::KeyEvent*) ui/aura/window_event_dispatcher.cc:1058:54
    #32 0x56290ad0fbe8 in aura::WindowEventDispatcher::PreDispatchEvent(ui::EventTarget*, ui::Event*) ui/aura/window_event_dispatcher.cc:546:15
    #33 0x5629078cd914 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:51:34
    #34 0x56290ad162bf in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #35 0x5629078d20fe in ui::EventSource::DeliverEventToSink(ui::Event*) ui/events/event_source.cc:118:16
    #36 0x5629078d25f6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ui/events/event_source.cc:66:14
    #37 0x5629078d0d1b in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ui/events/event_rewriter.cc:88:39
    #38 0x5628fb441221 in ui::EventRewriterChromeOS::RewriteKeyEventInContext(ui::KeyEvent const&, std::__1::unique_ptr<ui::Event, std::__1::default_delete<ui::Event> >, ui::EventRewriteStatus, base::WeakPtr<ui::EventRewriterContinuation>) ui/chromeos/events/event_rewriter_chromeos.cc
    #39 0x5628fb43f319 in ui::EventRewriterChromeOS::RewriteEvent(ui::Event const&, base::WeakPtr<ui::EventRewriterContinuation>) ui/chromeos/events/event_rewriter_chromeos.cc:752:12
    #40 0x5629078d25a6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ui/events/event_source.cc:67:32
    #41 0x5629078d0d1b in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ui/events/event_rewriter.cc:88:39
    #42 0x56290b3c1100 in ash::KeyboardDrivenEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr<ui::EventRewriterContinuation>) ash/events/keyboard_driven_event_rewriter.cc:31:12
    #43 0x5629078d25a6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ui/events/event_source.cc:67:32
    #44 0x5629078d0d1b in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ui/events/event_rewriter.cc:88:39
    #45 0x56290b3bcd70 in ash::AccessibilityEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr<ui::EventRewriterContinuation>) ash/events/accessibility_event_rewriter.cc
    #46 0x5629078d25a6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ui/events/event_source.cc:67:32
    #47 0x5629078d0d1b in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ui/events/event_rewriter.cc:88:39
    #48 0x56290b1df6ae in ash::AutoclickDragEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr<ui::EventRewriterContinuation>) ash/accessibility/autoclick/autoclick_drag_event_rewriter.cc
    #49 0x5629078d25a6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ui/events/event_source.cc:67:32
    #50 0x5629078d0d1b in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ui/events/event_rewriter.cc:88:39
    #51 0x56290b1c0051 in ash::FullscreenMagnifierController::RewriteEvent(ui::Event const&, base::WeakPtr<ui::EventRewriterContinuation>) ash/accessibility/magnifier/fullscreen_magnifier_controller.cc
    #52 0x5629078d1da6 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) ui/events/event_source.cc:144:29
    #53 0x56290b3f5c43 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event*) ui/aura/window_tree_host_platform.cc:231:38
    #54 0x56290b3fcdae in ash::AshWindowTreeHostPlatform::DispatchEvent(ui::Event*) ash/host/ash_window_tree_host_platform.cc:184:40
    #55 0x5629078dd0ff in Run base/callback.h:142:12
    #56 0x5629078dd0ff in ui::DispatchEventFromNativeUiEvent(ui::Event* const&, base::OnceCallback<void (ui::Event*)>) ui/events/ozone/events_ozone.cc:28:25
    #57 0x5628f8bf8551 in ui::X11Window::DispatchUiEvent(ui::Event*, x11::Event const&) ui/ozone/platform/x11/x11_window.cc:1304:3
    #58 0x5628f8bf7da7 in ui::X11Window::DispatchEvent(ui::Event* const&) ui/ozone/platform/x11/x11_window.cc:1257:3
    #59 0x5628f8bf88a2 in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event* const&) ui/ozone/platform/x11/x11_window.cc
    #60 0x5629071067e7 in ui::PlatformEventSource::DispatchEvent(ui::Event*) ui/events/platform/platform_event_source.cc:100:29
    #61 0x5629079cb191 in ui::X11EventSource::OnEvent(x11::Event const&) ui/events/platform/x11/x11_event_source.cc:287:5
    #62 0x5628f891f78f in x11::Connection::DispatchEvent(x11::Event const&) ui/gfx/x/connection.cc:469:14
    #63 0x5628f891f4b9 in x11::Connection::ProcessNextEvent() ui/gfx/x/connection.cc:520:3
    #64 0x5628f891ef7f in x11::Connection::Dispatch() ui/gfx/x/connection.cc
    #65 0x5628f891f56a in x11::Connection::DispatchAll() ui/gfx/x/connection.cc:457:12
    #66 0x56290532a855 in base::MessagePumpLibevent::OnLibeventNotification(int, short, void*) base/message_loop/message_pump_libevent.cc
    #67 0x5629056a4f0c in event_process_active base/third_party/libevent/event.c:381:4
    #68 0x5629056a4f0c in event_base_loop base/third_party/libevent/event.c:521:4
    #69 0x56290532b369 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_libevent.cc:246:5
    #70 0x5629051edd1a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:468:12
    #71 0x56290512758c in base::RunLoop::Run(base::Location const&) base/run_loop.cc:140:14
    #72 0x56290b3aecad in ash::DragDropController::StartDragAndDrop(std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, aura::Window*, aura::Window*, gfx::Point const&, int, ui::mojom::DragEventSource) ash/drag_drop/drag_drop_controller.cc:230:14
    #73 0x5628fcdbe6de in content::WebContentsViewAura::StartDragging(content::DropData const&, blink::DragOperationsMask, gfx::ImageSkia const&, gfx::Vector2d const&, blink::mojom::DragEventSourceInfo const&, content::RenderWidgetHostImpl*) content/browser/web_contents/web_contents_view_aura.cc:1167:15
    #74 0x5628fca55a5c in content::RenderWidgetHostImpl::StartDragging(mojo::StructPtr<blink::mojom::DragData>, blink::DragOperationsMask, SkBitmap const&, gfx::Vector2d const&, mojo::StructPtr<blink::mojom::DragEventSourceInfo>) content/browser/renderer_host/render_widget_host_impl.cc:2842:9
    #75 0x5628fa56656c in blink::mojom::FrameWidgetHostStubDispatch::Accept(blink::mojom::FrameWidgetHost*, mojo::Message*) ./gen/third_party/blink/public/mojom/page/widget.mojom.cc:3051:13
    #76 0x56290695913a in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:901:54
    #77 0x56290696bc77 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #78 0x56290695c006 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:658:20
    #79 0x56290691e9c9 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ipc/ipc_mojo_bootstrap.cc:1008:24
    #80 0x56290691863b in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind_internal.h:543:12
    #81 0x56290691863b in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind_internal.h:707:12
    #82 0x56290691863b in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::__1::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> base/bind_internal.h:780:12
    #83 0x56290691863b in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:749:12
    #84 0x5629051aca66 in Run base/callback.h:142:12
    #85 0x5629051aca66 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:135:32
    #86 0x5629051ecaa3 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:358:29)> base/task/common/task_annotator.h:74:5
    #87 0x5629051ecaa3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356:21
    #88 0x5629051ec2f2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261:30
    #89 0x5629051ed661 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #90 0x56290532afad in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_libevent.cc:195:55
    #91 0x5629051edd1a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:468:12
    #92 0x56290512758c in base::RunLoop::Run(base::Location const&) base/run_loop.cc:140:14
    #93 0x5628fbe7ba42 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1053:18
    #94 0x5628fbe7ffc5 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:155:15
    #95 0x5628fbe75d9a in content::BrowserMain(content::MainFunctionParams) content/browser/browser_main.cc:30:28
    #96 0x562904f07b2f in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:641:10
    #97 0x562904f0a633 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1165:10
    #98 0x562904f09a0a in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1031:12
    #99 0x562904f042a4 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:399:36
    #100 0x562904f04920 in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:427:10
    #101 0x5628f74be64a in ChromeMain chrome/app/chrome_main.cc:176:12
    #102 0x5628f74be41f in main chrome/app/chrome_exe_main_aura.cc:17:10
    #103 0x7f35a037a0b2 in __libc_start_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

0x6150007ad918 is located 280 bytes inside of 504-byte region [0x6150007ad800,0x6150007ad9f8)
freed by thread T0 (chrome) here:
    #0 0x5628f74bc68d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x56290b3b5f25 in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #2 0x56290b3b5f25 in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #3 0x56290b3b5f25 in ~unique_ptr buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:269:19
    #4 0x56290b3b5f25 in ash::DragDropTracker::~DragDropTracker() ash/drag_drop/drag_drop_tracker.cc:114:1
    #5 0x56290b3acd32 in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #6 0x56290b3acd32 in std::__1::unique_ptr<ash::DragDropTracker, std::__1::default_delete<ash::DragDropTracker> >::reset(ash::DragDropTracker*) buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #7 0x56290b3accf9 in ash::DragDropCaptureDelegate::~DragDropCaptureDelegate() ash/drag_drop/drag_drop_capture_delegate.cc:33:22
    #8 0x56290b3b4a6e in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #9 0x56290b3b4a6e in std::__1::unique_ptr<ash::TabDragDropDelegate, std::__1::default_delete<ash::TabDragDropDelegate> >::reset(ash::TabDragDropDelegate*) buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #10 0x56290b3adc3c in ash::DragDropController::Cleanup() ash/drag_drop/drag_drop_controller.cc:737:27
    #11 0x56290b3b4325 in ash::DragDropController::DoDragCancel(base::TimeDelta) ash/drag_drop/drag_drop_controller.cc:668:3
    #12 0x5629078ceb5b in ui::EventDispatcher::DispatchEvent(ui::EventHandler*, ui::Event*) ui/events/event_dispatcher.cc:190:12
    #13 0x5629078ce949 in ui::EventDispatcher::DispatchEventToEventHandlers(std::__1::vector<ui::EventHandler*, std::__1::allocator<ui::EventHandler*> >*, ui::Event*) ui/events/event_dispatcher.cc:177:7
    #14 0x5629078cdf6d in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:125:3
    #15 0x5629078cdbf4 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:83:14
    #16 0x5629078cd960 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:55:15
    #17 0x56290ad162bf in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #18 0x56290ad11bdd in aura::WindowEventDispatcher::DispatchSyntheticTouchEvent(ui::TouchEvent*) ui/aura/window_event_dispatcher.cc:610:29
    #19 0x56290ace9af8 in ui::GestureRecognizerImpl::CancelActiveTouchesImpl(ui::GestureConsumer*) ui/events/gestures/gesture_recognizer_impl.cc:356:13
    #20 0x56290acf3435 in aura::Window::CleanupGestureState() ui/aura/window.cc:1259:48
    #21 0x56290acf3511 in aura::Window::CleanupGestureState() ui/aura/window.cc:1268:30
    #22 0x56290ad0dbd7 in aura::WindowEventDispatcher::OnWindowHidden(aura::Window*, aura::WindowEventDispatcher::WindowHiddenReason) ui/aura/window_event_dispatcher.cc:374:14
    #23 0x56290ad123ea in aura::WindowEventDispatcher::OnWindowVisibilityChanged(aura::Window*, bool) ui/aura/window_event_dispatcher.cc:681:5
    #24 0x56290acfeb26 in aura::Window::NotifyWindowVisibilityChangedAtReceiver(aura::Window*, bool) ui/aura/window.cc:1218:14
    #25 0x56290acfe69a in aura::Window::NotifyWindowVisibilityChangedDown(aura::Window*, bool) ui/aura/window.cc:1224:8
    #26 0x56290acfcb1d in aura::Window::NotifyWindowVisibilityChanged(aura::Window*, bool) ui/aura/window.cc:1205:8
    #27 0x56290acf577e in aura::Window::SetVisibleInternal(bool) ui/aura/window.cc:1021:3
    #28 0x56290ba5d452 in ash::Desk::Deactivate(bool) ash/wm/desks/desk.cc:430:40
    #29 0x56290ba66a70 in ash::DesksController::ActivateDeskInternal(ash::Desk const*, bool) ash/wm/desks/desks_controller.cc:1210:15
    #30 0x56290ba63808 in ash::DesksController::ActivateDesk(ash::Desk const*, ash::DesksSwitchSource) ash/wm/desks/desks_controller.cc
    #31 0x56290ba658fd in ash::DesksController::RemoveDeskInternal(ash::Desk const*, ash::DesksCreationRemovalSource) ash/wm/desks/desks_controller.cc:1335:5
    #32 0x56290ba64eec in ash::DesksController::RemoveDesk(ash::Desk const*, ash::DesksCreationRemovalSource) ash/wm/desks/desks_controller.cc:452:3
    #33 0x56290b1e88bc in ash::(anonymous namespace)::HandleRemoveCurrentDesk() ash/accelerators/accelerator_controller_impl.cc:366:21
    #34 0x56290b1e45b5 in ash::AcceleratorControllerImpl::PerformAction(ash::AcceleratorAction, ui::Accelerator const&) ash/accelerators/accelerator_controller_impl.cc:2083:7

previously allocated by thread T0 (chrome) here:
    #0 0x5628f74bbe2d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x56290b3b5d38 in make_unique<aura::Window, aura::WindowDelegate *&> buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:725:28
    #2 0x56290b3b5d38 in CreateCaptureWindow ash/drag_drop/drag_drop_tracker.cc:90:7
    #3 0x56290b3b5d38 in ash::DragDropTracker::DragDropTracker(aura::Window*, base::RepeatingCallback<void ()>) ash/drag_drop/drag_drop_tracker.cc:109:7
    #4 0x56290b3ace6b in ash::DragDropCaptureDelegate::TakeCapture(aura::Window*, aura::Window*, base::RepeatingCallback<void ()>, ui::TransferTouchesBehavior) ash/drag_drop/drag_drop_capture_delegate.cc:41:32
    #5 0x56290b3aeb5e in ash::DragDropController::StartDragAndDrop(std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, aura::Window*, aura::Window*, gfx::Point const&, int, ui::mojom::DragEventSource) ash/drag_drop/drag_drop_controller.cc:215:32
    #6 0x5628fcdbe6de in content::WebContentsViewAura::StartDragging(content::DropData const&, blink::DragOperationsMask, gfx::ImageSkia const&, gfx::Vector2d const&, blink::mojom::DragEventSourceInfo const&, content::RenderWidgetHostImpl*) content/browser/web_contents/web_contents_view_aura.cc:1167:15
    #7 0x5628fca55a5c in content::RenderWidgetHostImpl::StartDragging(mojo::StructPtr<blink::mojom::DragData>, blink::DragOperationsMask, SkBitmap const&, gfx::Vector2d const&, mojo::StructPtr<blink::mojom::DragEventSourceInfo>) content/browser/renderer_host/render_widget_host_impl.cc:2842:9
    #8 0x5628fa56656c in blink::mojom::FrameWidgetHostStubDispatch::Accept(blink::mojom::FrameWidgetHost*, mojo::Message*) ./gen/third_party/blink/public/mojom/page/widget.mojom.cc:3051:13
    #9 0x56290695913a in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:901:54
    #10 0x56290696bc77 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #11 0x56290695c006 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:658:20
    #12 0x56290691e9c9 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ipc/ipc_mojo_bootstrap.cc:1008:24
    #13 0x56290691863b in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind_internal.h:543:12
    #14 0x56290691863b in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind_internal.h:707:12
    #15 0x56290691863b in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::__1::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> base/bind_internal.h:780:12
    #16 0x56290691863b in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:749:12
    #17 0x5629051aca66 in Run base/callback.h:142:12
    #18 0x5629051aca66 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:135:32
    #19 0x5629051ecaa3 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:358:29)> base/task/common/task_annotator.h:74:5
    #20 0x5629051ecaa3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356:21
    #21 0x5629051ec2f2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261:30
    #22 0x5629051ed661 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #23 0x56290532afad in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_libevent.cc:195:55
    #24 0x5629051edd1a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:468:12
    #25 0x56290512758c in base::RunLoop::Run(base::Location const&) base/run_loop.cc:140:14
    #26 0x5628fbe7ba42 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1053:18
    #27 0x5628fbe7ffc5 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:155:15
    #28 0x5628fbe75d9a in content::BrowserMain(content::MainFunctionParams) content/browser/browser_main.cc:30:28
    #29 0x562904f07b2f in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:641:10
    #30 0x562904f0a633 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1165:10
    #31 0x562904f09a0a in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1031:12
    #32 0x562904f042a4 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:399:36
    #33 0x562904f04920 in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:427:10
    #34 0x5628f74be64a in ChromeMain chrome/app/chrome_main.cc:176:12
    #35 0x5628f74be41f in main chrome/app/chrome_exe_main_aura.cc:17:10
    #36 0x7f35a037a0b2 in __libc_start_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free buildtools/third_party/libc++/trunk/include/vector:1526:30 in begin
Shadow bytes around the buggy address:
  0x0c2a800edad0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2a800edae0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2a800edaf0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2a800edb00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a800edb10: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0c2a800edb20: fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a800edb30: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa
  0x0c2a800edb40: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2a800edb50: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2a800edb60: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2a800edb70: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==63195==ABORTING

Did this work before? N/A 

Chrome version: 100.0.4858.0  Channel: dev
OS Version: linux-chromeOS

## Attachments

- [screencast_1292271.webm](attachments/screencast_1292271.webm) (video/webm, 5.7 MB)

## Timeline

### [Deleted User] (2022-01-29)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-01-29)

PoC:

(1) Tested on linux-chromeOS Asan.
(2) Force chromeOS to tablet mode pass in command line --force-tablet-mode=touch_view --touch-devices=12 (touch-devices=[int] depends on your computer "$ xinput"). This command is to simulate real device( tablet mode) so there's will be no cursor.
(3) Add new desk at least one or two desk.
(4) Open browser and and new tab.
(5) Swipe up from button to open split view(correct me if I'm wrong).
(5) Drag the new tab to the right side and then remove one desk.

I currently don't own tablet Chromebook, I'm sure this bug effects on real devices.
Please see the screen-cast for visibility.

Thank you

### al...@google.com (2022-01-31)

[Empty comment from Monorail migration]

[Monorail components: UI>Shell]

### th...@chromium.org (2022-01-31)

Not sure why I got CC'd. Presumably because I last touched ui/aura/window_tracker.cc in r885354. But that was just a mechanical refactoring CL.

### al...@google.com (2022-01-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-31)

[Empty comment from Monorail migration]

### al...@google.com (2022-01-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-01)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-01)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-01)

[Empty comment from Monorail migration]

### he...@google.com (2022-02-05)

[Empty comment from Monorail migration]

[Monorail components: -UI>Shell UI>Shell>WindowManager>VirtualDesks]

### mn...@chromium.org (2022-02-08)

This looks more like problem with the drag-and-drop implementation: The offending object appears to be the |capture_window_| member of DragDropTracker.

Adding ash/OWNERS to take a look.

[Monorail components: -UI>Shell>WindowManager>VirtualDesks UI>Shell]

### xi...@chromium.org (2022-02-08)

Looks like CancelActiveTouches() in Window::CleanupGestureState() [1] deleted the window itself and `this` becomes invalid afterwards.

https://source.chromium.org/chromium/chromium/src/+/main:ui/aura/window.cc;l=1259;drc=0e45c020c43b1a9f6d2870ff7f92b30a2f03a458;bpv=1;bpt=0

### af...@chromium.org (2022-02-08)

I don't have cycles for this at the moment. Daniel, can you please take a look? Thanks! :)

### xi...@chromium.org (2022-02-08)

Unrelated to the UAF, but the ownership of `capture_window_` in ash::DragDropTracker seems having problems. ash::DragDropTracker owns it via unique_ptr. But all aura::Window are owned by their parent by default, unless we call set_owned_by_parent(false) to tell it is not the case. It seems CreateCaptureWindow [1] is not doing that. Are we double owning `capture_window_` ?

[1] https://source.chromium.org/chromium/chromium/src/+/main:ash/drag_drop/drag_drop_tracker.cc;l=89;drc=2c63db7ef6a10e2958e4847908ec9b2fd03e8ab2;bpv=0;bpt=0

### [Deleted User] (2022-02-08)

[Empty comment from Monorail migration]

### da...@chromium.org (2022-02-09)

I'm able to repro a UAF, but the stack traces and objects involved look a bit different:

When dropping on a desk mini view, we end up in DragDropController::OnMouseEvent. In this function, `translated_target` will be a VirtualDesksWidget which belongs to a hierarchy ultimately owned by the OverviewSession.

When OnMouseEvent calls DragDropController::Drop, it will trigger a sequence of events that results in the new tab window getting snapped, which exits overview mode. This in turn destroys the hierarchy that VirtualDesksWidget belongs to.

https://source.chromium.org/chromium/chromium/src/+/main:ash/drag_drop/drag_drop_controller.cc;l=347;drc=51970fdd244abed4d6388f864b0e97b5260d390f

We then get to line 356 that calls GetTopLevelWindow on `translated_target` which now points to a destroyed object.

https://source.chromium.org/chromium/chromium/src/+/main:ash/drag_drop/drag_drop_controller.cc;l=356;drc=51970fdd244abed4d6388f864b0e97b5260d390f


I don't know what the fix here is going to look like. One interesting tidbit is that there's code in `OverviewController::ToggleOverview` that (I'm guessing) was added to deal with a similar situation:

    // Don't delete |overview_session_| yet since the stack is still using it.
    base::ThreadTaskRunnerHandle::Get()->DeleteSoon(
        FROM_HERE, overview_session_.release());

however, the widget in question has already been destroyed by `OverviewSession::Shutdown` which is called ~10 lines above.


### af...@chromium.org (2022-02-11)

+xdai@ in case she doesn't have access.

### xd...@chromium.org (2022-02-11)

Re#17: it doesn't seem the crash described in the report and https://crbug.com/chromium/1292271#c2 is the same as what you described in #17 (though we should fix that one if it crashes as well). For the original crash, looks like it happens when dragging a webUI tab to the right side of the screen, and then use keyboard shortcut to remove a desk, in this case it can cause window visibility change, thus calls CleanupGestureState, which then calls CancelActiveTouches to cause the drag being cancelled, thus causes |capture_window_| which is owned by DragDropTracker being destroyed. But CleanupGestureState is still using this window, thus cause the heap-use-after-free crash.

For the fix, I wonder if we can get a weakptr of the window and if it's no longer valid after CancelActiveTouches, then return directly. 


### da...@chromium.org (2022-02-11)

xdai, you are of course correct. I missed the part with using a keyboard shortcut to remove the current desk. I've now been able to reproduce this UAF and I'll file a separate ticket for the other UAF that I described in #17.

### xd...@chromium.org (2022-02-11)

For crash in #17, I think we can prevent the crash by preventing the tab from snapping in split screen if it gets dropped on top of the desk mini view. We should be able to might be able to do some special handing in TabDragDropDelegate::OnNewBrowserWindowCreated [1]. 

[1] https://source.chromium.org/chromium/chromium/src/+/main:ash/drag_drop/tab_drag_drop_delegate.cc;drc=21d12b05a8522de912189db9e4067fff02216ddb;l=152

### xd...@chromium.org (2022-02-11)

+yuhengh@ since it's a crash caused by webui tab drag & drop in #17. 

### rh...@gmail.com (2022-02-11)

xdai@, dandersson@,

Sorry for the interrupting. 
I filled other tickets before this issue, I'm afraid crash https://crbug.com/chromium/1292271#c17 is same with following issue:

https://crbug.com/chromium/1286203 SUMMARY: AddressSanitizer: heap-use-after-free base/memory/raw_ptr.h:664:47 in GetForExtraction
https://crbug.com/chromium/1292272 SUMMARY: AddressSanitizer: heap-use-after-free buildtools/third_party/libc++/trunk/include/__tree:1079:59 in __root
https://crbug.com/chromium/1286921 SUMMARY: AddressSanitizer: heap-use-after-free base/memory/raw_ptr.h:535:14 in operator bool

### yu...@chromium.org (2022-02-11)

As I already mentioned in https://bugs.chromium.org/p/chromium/issues/detail?id=1286203#c20
WebUI tab strip is only available on tablet mode, which should not have any physical keyboard, so I'm not sure if this is a real world issue.

### xd...@chromium.org (2022-02-11)

Re#24: It's possible to have physical keyboard in tablet mode. Tablet mode UI mode is decided by the presence of the input device, not the keyboard. Also the crash in #17 does not involve a keyboard though. It's about dragging a tab and dropping it on top of the desk mini view when splitview is active. 

### yu...@chromium.org (2022-02-12)

Ok, the cash in https://crbug.com/chromium/1292271#c17 is from DragDropController::OnMouseEvent. Does tablet mode has mouse? I haven't seen any mouse cursor in tablet mode, but correct me if I'm wrong.

### rh...@gmail.com (2022-02-14)

Hi xdai@ and dandersson@,

Can you help me to provide stack trace from crash server id below:

Crash from Monday, February 14, 2022 at 6:44:30 PM
Status:	Uploaded
Uploaded Crash Report ID:	62ac2faae9b97fc5
Upload Time:	Monday, February 14, 2022 at 6:56:38 PM

I tested on a real device and it's hard to figure out what the stack trace looks like. If it's still related to this issue, I will prepare a screen-cast ASAP for visibility.

### xd...@chromium.org (2022-02-14)

Re#27 rhezashan@: Thanks! This is the crash with the crash id you provided: https://crash.corp.google.com/browse?stbtiq=62ac2faae9b97fc5#0

0x0000000008ad03c8	(chrome -unique_ptr.h:287)		ash::DragDropCaptureDelegate::TakeCapture(aura::Window*, aura::Window*, base::RepeatingCallback<void ()>, ui::TransferTouchesBehavior)
0x0000000008ad0d0f	(chrome -drag_drop_controller.cc:225)		ash::DragDropController::StartDragAndDrop(std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, aura::Window*, aura::Window*, gfx::Point const&, int, ui::mojom::DragEventSource)
0x00000000042bcc29	(chrome -web_contents_view_aura.cc:1159)		content::WebContentsViewAura::StartDragging(content::DropData const&, blink::DragOperationsMask, gfx::ImageSkia const&, gfx::Vector2d const&, blink::mojom::DragEventSourceInfo const&, content::RenderWidgetHostImpl*)
0x00000000041faa53	(chrome -render_widget_host_impl.cc:2833)		content::RenderWidgetHostImpl::StartDragging(mojo::StructPtr<blink::mojom::DragData>, blink::DragOperationsMask, SkBitmap const&, gfx::Vector2d const&, mojo::StructPtr<blink::mojom::DragEventSourceInfo>)
0x0000000003bc6007	(chrome -widget.mojom.cc:3052)		blink::mojom::FrameWidgetHostStubDispatch::Accept(blink::mojom::FrameWidgetHost*, mojo::Message*)

This looks like a different crash, though it's still related to webui tab dragging. The code history showed that it might be caused by this CL https://chromium.googlesource.com/chromium/src.git/+/55ab85e8e168e9bbaeab47fa2e27df8bdc41f208. It will be helpful if you can provide a repro video for it. To avoid flooding this bug with other different crashes, can you please file a separate bug for it please? Thanks!


Re#26 yuhengh@: good point. We should not have mouse events in tablet mode. dandersson@, wonder how did you get the crash in the first place? Also, it might be good if we can file a separate bug for that and discuss it in a different bug thread. 

### rh...@gmail.com (2022-02-14)

xdai@, Thanks for the stack trace, I filled the issue #1297209. 

Hello Security sheriff, please cc xdai@ and yuhengh@ on issue #1297209, if they can't access there.

### sa...@chromium.org (2022-02-14)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-02-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5a2a306942bc7e794ec147f685f5eb44e3746111

commit 5a2a306942bc7e794ec147f685f5eb44e3746111
Author: Daniel Andersson <dandersson@chromium.org>
Date: Mon Feb 14 21:17:20 2022

Prevent UAF in aura::Window::CleanupGestureState.

Cancelling active touches may, under certain circumstances, end up
destroying the window that it was called from. This change adds code
to detect this and does an early exit if it happens.

Details and reproduction steps in the bug.

Test: Manually verified.
Bug: 1292271
Change-Id: I48934b3e062111544ae0b2782ea1516739e6f851
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3456997
Reviewed-by: Xiaoqian Dai <xdai@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Daniel Andersson <dandersson@chromium.org>
Cr-Commit-Position: refs/heads/main@{#970825}

[modify] https://crrev.com/5a2a306942bc7e794ec147f685f5eb44e3746111/ui/aura/window.cc


### da...@chromium.org (2022-02-14)

[Empty comment from Monorail migration]

### da...@chromium.org (2022-02-14)

Ooops.. still in progress.. fix is landed, but needs to be merged.

### ce...@google.com (2022-02-15)

Merge approved for M99.

### ma...@google.com (2022-02-15)

Approved for M98.  Please merge asap as we plan to qualify tonight's build tomorrow morning.

### ma...@google.com (2022-02-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-02-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/47d058ed961166bc1e5bd4c9dd74598cf215a202

commit 47d058ed961166bc1e5bd4c9dd74598cf215a202
Author: Daniel Andersson <dandersson@chromium.org>
Date: Tue Feb 15 20:55:48 2022

Prevent UAF in aura::Window::CleanupGestureState.

Cancelling active touches may, under certain circumstances, end up
destroying the window that it was called from. This change adds code
to detect this and does an early exit if it happens.

Details and reproduction steps in the bug.

(cherry picked from commit 5a2a306942bc7e794ec147f685f5eb44e3746111)

Test: Manually verified.
Bug: 1292271
Change-Id: I48934b3e062111544ae0b2782ea1516739e6f851
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3456997
Reviewed-by: Xiaoqian Dai <xdai@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Daniel Andersson <dandersson@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#970825}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3466014
Auto-Submit: Daniel Andersson <dandersson@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/branch-heads/4844@{#563}
Cr-Branched-From: 007241ce2e6c8e5a7b306cc36c730cd07cd38825-refs/heads/main@{#961656}

[modify] https://crrev.com/47d058ed961166bc1e5bd4c9dd74598cf215a202/ui/aura/window.cc


### gi...@appspot.gserviceaccount.com (2022-02-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b9793da9aa03f0e99bd4d7de3c25639931c3bb4c

commit b9793da9aa03f0e99bd4d7de3c25639931c3bb4c
Author: Daniel Andersson <dandersson@chromium.org>
Date: Tue Feb 15 21:03:09 2022

Prevent UAF in aura::Window::CleanupGestureState.

Cancelling active touches may, under certain circumstances, end up
destroying the window that it was called from. This change adds code
to detect this and does an early exit if it happens.

Details and reproduction steps in the bug.

(cherry picked from commit 5a2a306942bc7e794ec147f685f5eb44e3746111)

Test: Manually verified.
Bug: 1292271
Change-Id: I48934b3e062111544ae0b2782ea1516739e6f851
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3456997
Reviewed-by: Xiaoqian Dai <xdai@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Daniel Andersson <dandersson@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#970825}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3465006
Auto-Submit: Daniel Andersson <dandersson@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/branch-heads/4758@{#1166}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/b9793da9aa03f0e99bd4d7de3c25639931c3bb4c/ui/aura/window.cc


### da...@chromium.org (2022-02-15)

The fix has been merged to 98 and 99. I'm closing this bug out for now. There's still a TODO about maybe adding a regression test, but it's a bit outside of my current range.

### [Deleted User] (2022-02-15)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-02-16)

[Empty comment from Monorail migration]

### rz...@google.com (2022-02-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-16)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-02-16)

1. Just https://crrev.com/c/3468754
2. Low, no conflicts
3. 98, 99
4. Yes

### [Deleted User] (2022-02-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-16)

[Empty comment from Monorail migration]

### gm...@google.com (2022-02-17)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-02-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6036b79972a3de67737f5b5195d7951fe2ae01bb

commit 6036b79972a3de67737f5b5195d7951fe2ae01bb
Author: Daniel Andersson <dandersson@chromium.org>
Date: Fri Feb 18 18:54:58 2022

[M96-LTS] Prevent UAF in aura::Window::CleanupGestureState.

Cancelling active touches may, under certain circumstances, end up
destroying the window that it was called from. This change adds code
to detect this and does an early exit if it happens.

Details and reproduction steps in the bug.

(cherry picked from commit 5a2a306942bc7e794ec147f685f5eb44e3746111)

Test: Manually verified.
Bug: 1292271
Change-Id: I48934b3e062111544ae0b2782ea1516739e6f851
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3456997
Commit-Queue: Daniel Andersson <dandersson@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#970825}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3468754
Reviewed-by: Michael Ershov <miersh@google.com>
Owners-Override: Michael Ershov <miersh@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1489}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/6036b79972a3de67737f5b5195d7951fe2ae01bb/ui/aura/window.cc


### rz...@google.com (2022-02-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-02-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-03)

Congratulations on another one, Rheza! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us. 

### da...@google.com (2022-03-09)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1292271?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058635)*
