# Security: Potential UaF in TabStripModel (chromeOS)

| Field | Value |
|-------|-------|
| **Issue ID** | [40058468](https://issues.chromium.org/issues/40058468) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>TopChrome>TabStrip>ThumbnailTabStrip |
| **Platforms** | ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | yu...@chromium.org |
| **Created** | 2022-01-11 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Similar with issue #1242742 but effects only on chromeOS

**VERSION**  

ChromeOS Beta: 98.0.4758.46  

Google\_Atlas.11827.169.0

**REPRODUCTION CASE**  

enable-flags #top-chrome-touch-ui,webui-tab-strip.  

The flags expires on version 99.

(1) Open 3 tabs and join them all.  

(2) Drag the group tab out from the browser.  

(3) close the browser with ctrl + w

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser crash  

Crash ID: crash/67b546c83ba7740d

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [uaf_1286203_tablet_mode.log](attachments/uaf_1286203_tablet_mode.log) (text/plain, 28.0 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [asan_1286203_noMouseEvent.log](attachments/asan_1286203_noMouseEvent.log) (text/plain, 34.8 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [newTab.html](attachments/newTab.html) (text/plain, 326 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [Screen recording 2022-02-27 6.09.25 PM.webm](attachments/Screen recording 2022-02-27 6.09.25 PM.webm) (video/webm, 11.5 MB)
- deleted (application/octet-stream, 0 B)
- [lacros-1286203-asan.log](attachments/lacros-1286203-asan.log) (text/plain, 7.1 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2022-01-11)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-01-11)

Please add one more flags:

#webui-tab-strip-tab-drag-integration
crash/92aa0be4287f5bec
crash/8455f8359f628f3e
crash/c561612132c56bdb

### rh...@gmail.com (2022-01-12)

Hi,

I've tested on 99.0.4825.0 {#958056}

==51067==ERROR: AddressSanitizer: heap-use-after-free on address 0x61500062bf08 at pc 0x55f7201268ce bp 0x7ffde69ca390 sp 0x7ffde69ca388
READ of size 8 at 0x61500062bf08 thread T0 (chrome)
    #0 0x55f7201268cd in GetForExtraction base/memory/raw_ptr.h:664:47
    #1 0x55f7201268cd in operator aura::WindowDelegate * base/memory/raw_ptr.h:554:56
    #2 0x55f7201268cd in delegate ui/aura/window.h:199:39
    #3 0x55f7201268cd in aura::Window::GetToplevelWindow() ui/aura/window.cc:789:17
    #4 0x55f7207cf848 in ash::DragDropController::OnMouseEvent(ui::MouseEvent*) ash/drag_drop/drag_drop_controller.cc:378:38
    #5 0x55f71ccd4eeb in ui::EventDispatcher::DispatchEvent(ui::EventHandler*, ui::Event*) ui/events/event_dispatcher.cc:190:12
    #6 0x55f71ccd4cd9 in ui::EventDispatcher::DispatchEventToEventHandlers(std::__1::vector<ui::EventHandler*, std::__1::allocator<ui::EventHandler*> >*, ui::Event*) ui/events/event_dispatcher.cc:177:7
    #7 0x55f71ccd42fd in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:125:3
    #8 0x55f71ccd3f84 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:83:14
    #9 0x55f71ccd3cf0 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:55:15
    #10 0x55f72014158f in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #11 0x55f71ccd859e in ui::EventSource::DeliverEventToSink(ui::Event*) ui/events/event_source.cc:118:16
    #12 0x55f71ccd8a96 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ui/events/event_source.cc:66:14
    #13 0x55f71ccd71bb in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ui/events/event_rewriter.cc:88:39
    #14 0x55f7109bcf6d in ui::EventRewriterChromeOS::RewriteMouseButtonEvent(ui::MouseEvent const&, base::WeakPtr<ui::EventRewriterContinuation>) ui/chromeos/events/event_rewriter_chromeos.cc:1274:12
    #15 0x55f7109bd4ad in ui::EventRewriterChromeOS::RewriteEvent(ui::Event const&, base::WeakPtr<ui::EventRewriterContinuation>) ui/chromeos/events/event_rewriter_chromeos.cc:758:12
    #16 0x55f71ccd8a46 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ui/events/event_source.cc:67:32
    #17 0x55f71ccd71bb in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ui/events/event_rewriter.cc:88:39
    #18 0x55f7207e0780 in ash::KeyboardDrivenEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr<ui::EventRewriterContinuation>) ash/events/keyboard_driven_event_rewriter.cc:31:12
    #19 0x55f71ccd8a46 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ui/events/event_source.cc:67:32
    #20 0x55f71ccd71bb in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ui/events/event_rewriter.cc:88:39
    #21 0x55f7207dc3f0 in ash::AccessibilityEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr<ui::EventRewriterContinuation>) ash/events/accessibility_event_rewriter.cc
    #22 0x55f71ccd8a46 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ui/events/event_source.cc:67:32
    #23 0x55f71ccd71bb in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ui/events/event_rewriter.cc:88:39
    #24 0x55f72060262e in ash::AutoclickDragEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr<ui::EventRewriterContinuation>) ash/accessibility/autoclick/autoclick_drag_event_rewriter.cc
    #25 0x55f71ccd8a46 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ui/events/event_source.cc:67:32
    #26 0x55f71ccd71bb in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ui/events/event_rewriter.cc:88:39
    #27 0x55f7205e2fe9 in ash::FullscreenMagnifierController::RewriteEvent(ui::Event const&, base::WeakPtr<ui::EventRewriterContinuation>) ash/accessibility/magnifier/fullscreen_magnifier_controller.cc
    #28 0x55f71ccd8246 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) ui/events/event_source.cc:144:29
    #29 0x55f7208130ab in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event*) ui/aura/window_tree_host_platform.cc:230:38
    #30 0x55f72081a1fe in ash::AshWindowTreeHostPlatform::DispatchEvent(ui::Event*) ash/host/ash_window_tree_host_platform.cc:184:40
    #31 0x55f71cce1327 in Run base/callback.h:142:12
    #32 0x55f71cce1327 in ui::DispatchEventFromNativeUiEvent(ui::Event* const&, base::OnceCallback<void (ui::Event*)>) ui/events/ozone/events_ozone.cc:36:25
    #33 0x55f71d166d11 in ui::X11Window::DispatchUiEvent(ui::Event*, x11::Event const&) ui/platform_window/x11/x11_window.cc:1304:3
    #34 0x55f71d166567 in ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc:1257:3
    #35 0x55f71d167062 in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc
    #36 0x55f71c5273b7 in ui::PlatformEventSource::DispatchEvent(ui::Event*) ui/events/platform/platform_event_source.cc:100:29
    #37 0x55f71cdcec51 in ui::X11EventSource::OnEvent(x11::Event const&) ui/events/platform/x11/x11_event_source.cc:287:5
    #38 0x55f70df76f5b in x11::Connection::DispatchEvent(x11::Event const&) ui/gfx/x/connection.cc:469:14
    #39 0x55f70df76c85 in x11::Connection::ProcessNextEvent() ui/gfx/x/connection.cc:520:3
    #40 0x55f70df7674b in x11::Connection::Dispatch() ui/gfx/x/connection.cc
    #41 0x55f70df76d36 in x11::Connection::DispatchAll() ui/gfx/x/connection.cc:457:12
    #42 0x55f71a7651e5 in base::MessagePumpLibevent::OnLibeventNotification(int, short, void*) base/message_loop/message_pump_libevent.cc
    #43 0x55f71aad7b14 in event_process_active base/third_party/libevent/event.c:381:4
    #44 0x55f71aad7b14 in event_base_loop base/third_party/libevent/event.c:521:4
    #45 0x55f71a765cf9 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_libevent.cc:246:5
    #46 0x55f71a62a49a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:468:12
    #47 0x55f71a5656cc in base::RunLoop::Run(base::Location const&) base/run_loop.cc:140:14
    #48 0x55f7207ce22d in ash::DragDropController::StartDragAndDrop(std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, aura::Window*, aura::Window*, gfx::Point const&, int, ui::mojom::DragEventSource) ash/drag_drop/drag_drop_controller.cc:240:14
    #49 0x55f71236ad3f in content::WebContentsViewAura::StartDragging(content::DropData const&, blink::DragOperationsMask, gfx::ImageSkia const&, gfx::Vector2d const&, blink::mojom::DragEventSourceInfo const&, content::RenderWidgetHostImpl*) content/browser/web_contents/web_contents_view_aura.cc:1167:15
    #50 0x55f7120011ec in content::RenderWidgetHostImpl::StartDragging(mojo::StructPtr<blink::mojom::DragData>, blink::DragOperationsMask, SkBitmap const&, gfx::Vector2d const&, mojo::StructPtr<blink::mojom::DragEventSourceInfo>) content/browser/renderer_host/render_widget_host_impl.cc:2833:9
    #51 0x55f70fb80ba1 in blink::mojom::FrameWidgetHostStubDispatch::Accept(blink::mojom::FrameWidgetHost*, mojo::Message*) gen/third_party/blink/public/mojom/page/widget.mojom.cc:3052:13
    #52 0x55f71bd84cea in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:901:54
    #53 0x55f71bd97837 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #54 0x55f71bd87bb4 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:658:20
    #55 0x55f71bd4a359 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ipc/ipc_mojo_bootstrap.cc:1008:24
    #56 0x55f71bd43fcb in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind_internal.h:535:12
    #57 0x55f71bd43fcb in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind_internal.h:699:12
    #58 0x55f71bd43fcb in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::__1::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> base/bind_internal.h:772:12
    #59 0x55f71bd43fcb in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:741:12
    #60 0x55f71a5eae16 in Run base/callback.h:142:12
    #61 0x55f71a5eae16 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:135:32
    #62 0x55f71a629223 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:358:29)> base/task/common/task_annotator.h:74:5
    #63 0x55f71a629223 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356:21
    #64 0x55f71a628a72 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261:30
    #65 0x55f71a629de1 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #66 0x55f71a76593d in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_libevent.cc:195:55
    #67 0x55f71a62a49a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:468:12
    #68 0x55f71a5656cc in base::RunLoop::Run(base::Location const&) base/run_loop.cc:140:14
    #69 0x55f7114332b8 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1048:18
    #70 0x55f7114377ff in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:153:15
    #71 0x55f71142d61a in content::BrowserMain(content::MainFunctionParams) content/browser/browser_main.cc:30:28
    #72 0x55f71a344bdf in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:646:10
    #73 0x55f71a3476e1 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1160:10
    #74 0x55f71a346ab8 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1026:12
    #75 0x55f71a341354 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:399:36
    #76 0x55f71a3419d0 in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:427:10
    #77 0x55f70cb3046a in ChromeMain chrome/app/chrome_main.cc:177:12
    #78 0x7fe84c7290b2 in __libc_start_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

0x61500062bf08 is located 264 bytes inside of 504-byte region [0x61500062be00,0x61500062bff8)
freed by thread T0 (chrome) here:
    #0 0x55f70cb2e4ad in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x55f7205b3f54 in views::NativeWidgetAura::~NativeWidgetAura() ui/views/widget/native_widget_aura.cc
    #2 0x55f7205b41d1 in views::NativeWidgetAura::~NativeWidgetAura() ui/views/widget/native_widget_aura.cc:1132:39
    #3 0x55f7205601b8 in views::Widget::~Widget() ui/views/widget/widget.cc:193:5
    #4 0x55f7205607cb in views::Widget::~Widget() ui/views/widget/widget.cc:189:19
    #5 0x55f720f16477 in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #6 0x55f720f16477 in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #7 0x55f720f16477 in ash::OverviewItem::Shutdown() ash/wm/overview/overview_item.cc:295:16
    #8 0x55f720ef42e1 in ash::OverviewGrid::Shutdown(ash::OverviewEnterExitType) ash/wm/overview/overview_grid.cc:474:13
    #9 0x55f720f28243 in ash::OverviewSession::Shutdown() ash/wm/overview/overview_session.cc:342:20
    #10 0x55f720eed924 in ash::OverviewController::ToggleOverview(ash::OverviewEnterExitType) ash/wm/overview/overview_controller.cc:341:24
    #11 0x55f720eee211 in ash::OverviewController::EndOverview(ash::OverviewEndAction, ash::OverviewEnterExitType) ash/wm/overview/overview_controller.cc:143:3
    #12 0x55f720f687a1 in ash::SplitViewController::AutoSnapController::AutoSnapWindowIfNeeded(aura::Window*) ash/wm/splitview/split_view_controller.cc:521:44
    #13 0x55f720a75269 in wm::FocusController::SetActiveWindow(wm::ActivationChangeObserver::ActivationReason, aura::Window*, aura::Window*, bool) ui/wm/core/focus_controller.cc:390:25
    #14 0x55f720a73085 in wm::FocusController::FocusAndActivateWindow(wm::ActivationChangeObserver::ActivationReason, aura::Window*, bool) ui/wm/core/focus_controller.cc:234:10
    #15 0x55f7205aff33 in views::NativeWidgetAura::Activate() ui/views/widget/native_widget_aura.cc:652:56
    #16 0x55f7205afc46 in views::NativeWidgetAura::Show(ui::WindowShowState, gfx::Rect const&) ui/views/widget/native_widget_aura.cc:620:7
    #17 0x55f720565662 in views::Widget::Show() ui/views/widget/widget.cc:720:23
    #18 0x55f72720c9d1 in BrowserView::Show() chrome/browser/ui/views/frame/browser_view.cc:1057:11
    #19 0x55f726c22971 in ChromeNewWindowClient::NewWindowForDetachingTab(aura::Window*, ui::OSExchangeData const&, base::OnceCallback<void (aura::Window*)>) chrome/browser/ui/ash/chrome_new_window_client.cc:429:22
    #20 0x55f7207d90fb in ash::TabDragDropDelegate::DropAndDeleteSelf(gfx::Point const&, ui::OSExchangeData const&) ash/drag_drop/tab_drag_drop_delegate.cc:148:36
    #21 0x55f7207d2d7c in ash::DragDropController::PerformDrop(gfx::Point, ui::DropTargetEvent, std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, base::OnceCallback<void (ui::DropTargetEvent const&, std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, ui::mojom::DragOperation&)>, std::__1::unique_ptr<ash::TabDragDropDelegate, std::__1::default_delete<ash::TabDragDropDelegate> >, base::ScopedClosureRunner) ash/drag_drop/drag_drop_controller.cc:763:39
    #22 0x55f7207d4e42 in void base::internal::FunctorTraits<void (ash::DragDropController::*)(gfx::Point, ui::DropTargetEvent, std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, base::OnceCallback<void (ui::DropTargetEvent const&, std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, ui::mojom::DragOperation&)>, std::__1::unique_ptr<ash::TabDragDropDelegate, std::__1::default_delete<ash::TabDragDropDelegate> >, base::ScopedClosureRunner), void>::Invoke<void (ash::DragDropController::*)(gfx::Point, ui::DropTargetEvent, std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, base::OnceCallback<void (ui::DropTargetEvent const&, std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, ui::mojom::DragOperation&)>, std::__1::unique_ptr<ash::TabDragDropDelegate, std::__1::default_delete<ash::TabDragDropDelegate> >, base::ScopedClosureRunner), base::WeakPtr<ash::DragDropController>, gfx::Point, ui::DropTargetEvent, std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, base::OnceCallback<void (ui::DropTargetEvent const&, std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, ui::mojom::DragOperation&)>, std::__1::unique_ptr<ash::TabDragDropDelegate, std::__1::default_delete<ash::TabDragDropDelegate> >, base::ScopedClosureRunner>(void (ash::DragDropController::*)(gfx::Point, ui::DropTargetEvent, std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, base::OnceCallback<void (ui::DropTargetEvent const&, std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, ui::mojom::DragOperation&)>, std::__1::unique_ptr<ash::TabDragDropDelegate, std::__1::default_delete<ash::TabDragDropDelegate> >, base::ScopedClosureRunner), base::WeakPtr<ash::DragDropController>&&, gfx::Point&&, ui::DropTargetEvent&&, std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >&&, base::OnceCallback<void (ui::DropTargetEvent const&, std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, ui::mojom::DragOperation&)>&&, std::__1::unique_ptr<ash::TabDragDropDelegate, std::__1::default_delete<ash::TabDragDropDelegate> >&&, base::ScopedClosureRunner&&) base/bind_internal.h:535:12
    #23 0x55f7207d4c0e in MakeItSo<void (ash::DragDropController::*)(gfx::Point, ui::DropTargetEvent, std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, base::OnceCallback<void (const ui::DropTargetEvent &, std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, ui::mojom::DragOperation &)>, std::__1::unique_ptr<ash::TabDragDropDelegate, std::__1::default_delete<ash::TabDragDropDelegate> >, base::ScopedClosureRunner), base::WeakPtr<ash::DragDropController>, gfx::Point, ui::DropTargetEvent, std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, base::OnceCallback<void (const ui::DropTargetEvent &, std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, ui::mojom::DragOperation &)>, std::__1::unique_ptr<ash::TabDragDropDelegate, std::__1::default_delete<ash::TabDragDropDelegate> >, base::ScopedClosureRunner> base/bind_internal.h:719:5
    #24 0x55f7207d4c0e in RunImpl<void (ash::DragDropController::*)(gfx::Point, ui::DropTargetEvent, std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, base::OnceCallback<void (const ui::DropTargetEvent &, std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, ui::mojom::DragOperation &)>, std::__1::unique_ptr<ash::TabDragDropDelegate, std::__1::default_delete<ash::TabDragDropDelegate> >, base::ScopedClosureRunner), std::__1::tuple<base::WeakPtr<ash::DragDropController>, gfx::Point, ui::DropTargetEvent, std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, base::OnceCallback<void (const ui::DropTargetEvent &, std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, ui::mojom::DragOperation &)>, std::__1::unique_ptr<ash::TabDragDropDelegate, std::__1::default_delete<ash::TabDragDropDelegate> >, base::ScopedClosureRunner>, 0UL, 1UL, 2UL, 3UL, 4UL, 5UL, 6UL> base/bind_internal.h:772:12
    #25 0x55f7207d4c0e in base::internal::Invoker<base::internal::BindState<void (ash::DragDropController::*)(gfx::Point, ui::DropTargetEvent, std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, base::OnceCallback<void (ui::DropTargetEvent const&, std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, ui::mojom::DragOperation&)>, std::__1::unique_ptr<ash::TabDragDropDelegate, std::__1::default_delete<ash::TabDragDropDelegate> >, base::ScopedClosureRunner), base::WeakPtr<ash::DragDropController>, gfx::Point, ui::DropTargetEvent, std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, base::OnceCallback<void (ui::DropTargetEvent const&, std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, ui::mojom::DragOperation&)>, std::__1::unique_ptr<ash::TabDragDropDelegate, std::__1::default_delete<ash::TabDragDropDelegate> >, base::ScopedClosureRunner>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:741:12
    #26 0x55f7207d26fa in Run base/callback.h:142:12
    #27 0x55f7207d26fa in DropIfAllowed ash/drag_drop/drag_drop_controller.cc:94:24
    #28 0x55f7207d26fa in ash::DragDropController::Drop(aura::Window*, ui::LocatedEvent const&) ash/drag_drop/drag_drop_controller.cc:609:3
    #29 0x55f7207cf81f in ash::DragDropController::OnMouseEvent(ui::MouseEvent*) ash/drag_drop/drag_drop_controller.cc
    #30 0x55f71ccd4eeb in ui::EventDispatcher::DispatchEvent(ui::EventHandler*, ui::Event*) ui/events/event_dispatcher.cc:190:12
    #31 0x55f71ccd4cd9 in ui::EventDispatcher::DispatchEventToEventHandlers(std::__1::vector<ui::EventHandler*, std::__1::allocator<ui::EventHandler*> >*, ui::Event*) ui/events/event_dispatcher.cc:177:7
    #32 0x55f71ccd42fd in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:125:3
    #33 0x55f71ccd3f84 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:83:14
    #34 0x55f71ccd3cf0 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:55:15
    #35 0x55f72014158f in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17

previously allocated by thread T0 (chrome) here:
    #0 0x55f70cb2dc4d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x55f7205ab5bb in views::NativeWidgetAura::NativeWidgetAura(views::internal::NativeWidgetDelegate*) ui/views/widget/native_widget_aura.cc:106:15
    #2 0x55f7205b4303 in views::internal::NativeWidgetPrivate::CreateNativeWidget(views::internal::NativeWidgetDelegate*) ui/views/widget/native_widget_aura.cc:1198:14
    #3 0x55f72055f269 in CreateNativeWidget ui/views/widget/widget.cc:87:10
    #4 0x55f72055f269 in views::Widget::Init(views::Widget::InitParams) ui/views/widget/widget.cc:381:20
    #5 0x55f720f14dbe in ash::OverviewItem::CreateItemWidget() ash/wm/overview/overview_item.cc:1245:17
    #6 0x55f720f148c0 in ash::OverviewItem::OverviewItem(aura::Window*, ash::OverviewSession*, ash::OverviewGrid*) ash/wm/overview/overview_item.cc:193:3
    #7 0x55f720ef3487 in make_unique<ash::OverviewItem, aura::Window *&, ash::OverviewSession *&, ash::OverviewGrid *> buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:725:32
    #8 0x55f720ef3487 in ash::OverviewGrid::OverviewGrid(aura::Window*, std::__1::vector<aura::Window*, std::__1::allocator<aura::Window*> > const&, ash::OverviewSession*) ash/wm/overview/overview_grid.cc:448:9
    #9 0x55f720f266f5 in make_unique<ash::OverviewGrid, aura::Window *&, const std::__1::vector<aura::Window *, std::__1::allocator<aura::Window *> > &, ash::OverviewSession *> buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:725:32
    #10 0x55f720f266f5 in ash::OverviewSession::Init(std::__1::vector<aura::Window*, std::__1::allocator<aura::Window*> > const&, std::__1::vector<aura::Window*, std::__1::allocator<aura::Window*> > const&) ash/wm/overview/overview_session.cc:202:17
    #11 0x55f720eed31e in ash::OverviewController::ToggleOverview(ash::OverviewEnterExitType) ash/wm/overview/overview_controller.cc:432:24
    #12 0x55f720eec729 in ash::OverviewController::StartOverview(ash::OverviewStartAction, ash::OverviewEnterExitType) ash/wm/overview/overview_controller.cc:129:3
    #13 0x55f72060f887 in ash::(anonymous namespace)::HandleToggleOverview() ash/accelerators/accelerator_controller_impl.cc:841:26
    #14 0x55f720607d93 in ash::AcceleratorControllerImpl::PerformAction(ash::AcceleratorAction, ui::Accelerator const&) ash/accelerators/accelerator_controller_impl.cc:2414:7
    #15 0x55f720608608 in ash::AcceleratorControllerImpl::AcceleratorPressed(ui::Accelerator const&) ash/accelerators/accelerator_controller_impl.cc:1688:3
    #16 0x55f7204c6cee in TryProcess ui/base/accelerators/accelerator_manager.cc:153:17
    #17 0x55f7204c6cee in ui::AcceleratorManager::Process(ui::Accelerator const&) ui/base/accelerators/accelerator_manager.cc:83:27
    #18 0x55f720a78a5f in ash::PreTargetAcceleratorHandler::ProcessAccelerator(ui::KeyEvent const&, ui::Accelerator const&) ash/accelerators/pre_target_accelerator_handler.cc:74:45
    #19 0x55f720a790bf in wm::AcceleratorFilter::OnKeyEvent(ui::KeyEvent*) ui/wm/core/accelerator_filter.cc:51:18
    #20 0x55f71ccd4eeb in ui::EventDispatcher::DispatchEvent(ui::EventHandler*, ui::Event*) ui/events/event_dispatcher.cc:190:12
    #21 0x55f71ccd4cd9 in ui::EventDispatcher::DispatchEventToEventHandlers(std::__1::vector<ui::EventHandler*, std::__1::allocator<ui::EventHandler*> >*, ui::Event*) ui/events/event_dispatcher.cc:177:7
    #22 0x55f71ccd42fd in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:125:3
    #23 0x55f71ccd3f84 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:83:14
    #24 0x55f71ccd3cf0 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:55:15
    #25 0x55f72014158f in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #26 0x55f720157aa6 in aura::WindowTreeHost::DispatchKeyEventPostIME(ui::KeyEvent*) ui/aura/window_tree_host.cc:363:23
    #27 0x55f71cf85d15 in ui::InputMethodBase::DispatchKeyEventPostIME(ui::KeyEvent*) const ui/base/ime/input_method_base.cc:139:33
    #28 0x55f71d1119a9 in ui::InputMethodAsh::ProcessUnfilteredKeyPressEvent(ui::KeyEvent*) ui/base/ime/ash/input_method_ash.cc:599:38
    #29 0x55f71d111209 in ui::InputMethodAsh::DispatchKeyEvent(ui::KeyEvent*) ui/base/ime/ash/input_method_ash.cc:139:14
    #30 0x55f72013c4b9 in aura::WindowEventDispatcher::PreDispatchKeyEvent(aura::Window*, ui::KeyEvent*) ui/aura/window_event_dispatcher.cc:1058:54
    #31 0x55f72013aeac in aura::WindowEventDispatcher::PreDispatchEvent(ui::EventTarget*, ui::Event*) ui/aura/window_event_dispatcher.cc:546:15
    #32 0x55f71ccd3ca4 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:51:34
    #33 0x55f72014158f in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17

SUMMARY: AddressSanitizer: heap-use-after-free base/memory/raw_ptr.h:664:47 in GetForExtraction
Shadow bytes around the buggy address:
  0x0c2a800bd790: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a800bd7a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a800bd7b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2a800bd7c0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a800bd7d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0c2a800bd7e0: fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a800bd7f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa
  0x0c2a800bd800: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2a800bd810: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a800bd820: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a800bd830: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==51067==ABORTING


### rh...@gmail.com (2022-01-12)

Sorry for pointing issue #1242742 is not correct, TabStrip works well.
This UaF from the stack trace given is probably caused by desk_bar, look like similar from other fixed bug issue #1274641

Thanks


### rh...@gmail.com (2022-01-12)

clarify the PoC:

(1) Open 2 tab.
(2) Drag one tab out from the browser.


### ct...@chromium.org (2022-01-12)

Thanks for the report!

Setting some security labels: Severity-High (UaF in browser process but requiring a fairly specific user interaction with browser UI) and FoundIn-98 (so Impact-Beta).

The report requires specific flags to be set:

- #top-chrome-touch-ui is a testing flag to emulate a touch device so I believe the same would be triggerable on a different ChromeOS device without force-enabling the flag (this is just to make testing/triggering easier)
- #webui-tab-strip is currently enabled via a field trial to at least some real world clients
- #webui-tab-strip and #webui-tab-strip-tab-drag-integration are both enabled in fieldtrial_testing_config.json

So despite requiring a few flags to be manually enabled, I believe this bug affects real clients in the wild. My understanding is that some of these flags have already fully launched. If I'm mistaken and this configuration is not enabled on any clients, then this would instead be Security_Impact-None.

Reporter: Have you tried to reproduce this bug on ChromeOS 97 (Stable) or ChromeOS 99 (Dev)? For later versions, I believe the flags expired as the feature has already launched.

johntlee@ it looks like you owned the implementation bug for at least part of this (https://crbug.com/chromium/989131) -- could you take a look or help find an owner for this bug? https://crbug.com/chromium/1286858 is a similar looking bug that I will also send your way -- feel free to dupe that one into this bug if they have the same root cause.

[Monorail components: UI>Browser>TopChrome>TabStrip>ThumbnailTabStrip]

### ct...@chromium.org (2022-01-12)

Sorry that I missed your updates in the meantime -- thanks for testing on M99 as well!

### [Deleted User] (2022-01-12)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-01-13)

It does not repro on stable

### rh...@gmail.com (2022-01-13)

Please merge the https://crbug.com/chromium/1286858 into this issue. It's me on separate account. I didn't use my main email account on pixelbook.
I'm providing new video in order to find root cause for this issue. From my perspective it's related overview_item.cc[1,2] code. Maybe the afakhry@chromium.org or 
sammiequon@chromium.org can take a look this issue.


[1] https://source.chromium.org/chromium/chromium/src/+/main:ash/wm/overview/overview_item.cc;drc=b5f8ae060f677210962b7d726327b990a2ec2e2e;l=1253
[2] https://source.chromium.org/chromium/chromium/src/+/main:ash/wm/overview/overview_item.cc;drc=b5f8ae060f677210962b7d726327b990a2ec2e2e;l=196


### [Deleted User] (2022-01-13)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-13)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@chromium.org (2022-01-13)

Re-assigning to yuhengh@ to triage since he has done more work with it recently.

### yu...@chromium.org (2022-01-13)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-01-13)

Hello security sheriff and owners,

Please take a look into my another report issue #1286921, I think it can be fixed together.

### yu...@chromium.org (2022-01-18)

[Empty comment from Monorail migration]

### yu...@chromium.org (2022-01-18)

@rhezashan Thanks for the report. To echo on #16, we don't use #top-chrome-touch-ui to test on Chrome OS  and there are other issues with that (i.e. caption button overlap with toolbar)
We usually enable #webui-tab-strip and #webui-tab-strip-tab-drag-integratio and enter tablet mode for testing.
If your device does not support entering tablet mode (i.e. running Chrome OS on Linux build), you may pass in --top-chrome-touch-ui=enabled from command line.

I'm not able to reproduce this bug using the either --top-chrome-touch-ui or --top-chrome-touch-ui=enabled on 99.0.4837. And I think we only care about the --top-chrome-touch-ui=enabled case. Are you able to reproduce with --top-chrome-touch-ui=enabled?

### rh...@gmail.com (2022-01-19)

Hello developer,

Sorry for interrupting. I had to clarify the steps in https://crbug.com/chromium/1286203#c5 as follow:
(1) Open 2 tab.
(2) F5
(3) Drag one tab out from the browser.

Yes the --top-chrome-touch-ui=enabled may pass in command line if test from linux-chromeOS.
I've uploaded new screen cast for visibility.


### yu...@chromium.org (2022-01-20)

Sorry, I pasted the wrong command line from #17, it should be --force-tablet-mode=touch_view, not --top-chrome-touch-ui=enabled.
We use the following command line to test on linux-chromeos build. (--touch-devices specifies your pointer device from command line "xinput" to emulate touch rather than mouse)
out_linux_ash/Release/chrome --force-tablet-mode=touch_view --touch-devices=4 --show-tabs
Is it still reproducible with this setting?

### yu...@chromium.org (2022-01-20)

Okay, I think I can reproduce the same error when using
out_linux_ash/Release/chrome --force-tablet-mode=touch_view --touch-devices=4 --show-tabs
with your steps on https://crbug.com/chromium/1286203#c18. However when testing on device, entering tablet mode will disable the physical keyboard.
Since this feature is only available on tablet mode, I supposed it is not reproducible on real device? If you can please let us know.

### rh...@gmail.com (2022-01-20)

Hi,

re: https://crbug.com/chromium/1286203#c20
> I think I can reproduce the same error when using out_linux_ash/Release/chrome --force-tablet-mode=touch_view --touch-devices=4 --show-tabs

I don't think it's necessary for pass command as you provided. The simplest should be 
~/asan/chromeOS/asan-linux-release-961374/chrome --user-data-dir=/tmp/chromeos --flag-switches-begin --top-chrome-touch-ui=enabled --enable-features=WebuiTabStrip --flag-switches-end

> However when testing on device, entering tablet mode will disable the physical keyboard. 
This is happens because you're passing   --force-tablet-mode=touch_view --touch-devices=4 in command line.  You can try in your side by command in linux-chromeOS "--flag-switches-begin --top-chrome-touch-ui=enabled --enable-features=WebuiTabStrip --flag-switches-end". The command enables two flags top-chrome-touch-ui and WebuiTabStrip. (please refer to issue #1242742,  issue  #1228557,  issue #1239057 for convenience and those issues aren't in tablet mode.)

>Since this feature is only available on tablet mode, I supposed it is not reproducible on real device? 
This is incorrect, in https://crbug.com/chromium/1286203#c0 on the video shows the real device without tablet mode on. I tested on pixelbook and top-chrome-touch-ui and WebuiTabStrip were enabled (see attachment).

Anyway my assumption, the UaF caused by outlives web-tab-strip that being dragged into "overview_screen(F5)" as my previous comment https://crbug.com/chromium/1286203#c10.




### yu...@chromium.org (2022-01-21)

As it's already mentioned in https://crbug.com/chromium/1286203#c17, we won't turn on #top-chrome-touch-ui to any users unless they opted in manually. This flag is for testing purpose only and it does not work well with WebUI tab strip because WebUI tab strip always assumes users are in tablet mode. If you can reproduce the issue ONLY with #webui-tab-strip and #webui-tab-strip-tab-drag-integration on a real device, or
with #webui-tab-strip and #webui-tab-strip-tab-drag-integration and --force-tablet-mode=touch_view --touch-devices=4 on linux-chromeos build, then I believe it's a real world issue worth looking into.


### rh...@gmail.com (2022-01-21)

Hi,

>As it's already mentioned in https://crbug.com/chromium/1286203#c17, 
Yes, I'm sorry, I didn't read carefully, and thank you for the --force-tablet-mode=touch_view --touch-devices=4, I was looking for a long time to enter the tablet mode on linux-chromeOS, but I had no luck. Today you give me those command and very helpful. Thanks a lot.

Unfortunately, I was able to repro the UaF with command --force-tablet-mode=touch_view --touch-devices=4 as described on https://crbug.com/chromium/1286203#c22.

I'm uploading a video and this is an express experiments. This video is unedited, and more experiments are steps on video. The point was to find UaF (please skip video to 00:55 - 01:10. 
I can re-upload a new video later if necessary. 



### am...@chromium.org (2022-01-21)

based on https://crbug.com/chromium/1286203#c22, this does not appear to be a release blocking issue, this seems to potentially be a security_impact-None, but I'll leave this as is as researcher attempts to reproduce this issue with the necessary preconditions to demonstrate this issue as being exploitable on a configuration that would affect users / a real device or the necessary preconditions for it to prove that using a Chrome for Chrome OS on linux 

### rh...@gmail.com (2022-01-22)

re https://crbug.com/chromium/1286203#c24:
> the necessary preconditions for it to prove that using a Chrome for Chrome OS on linux
I've tested on linux-chromeOS with the command --force-tablet-mode=touch_view --touch-devices=4 as described on https://crbug.com/chromium/1286203#c22 in the video given on https://crbug.com/chromium/1286203#c23 shows UaF occurs without #top-chrome-touch-ui.  The UaF stack trace with #top-chrome-touch-ui or without #top-chrome-touch-ui (--force-tablet-mode=touch_view --touch-devices=4 enabled from command line) are actually same and I totally agree with comment https://crbug.com/chromium/1286203#c6 "(this is just to make testing/triggering easier)" it's true.

 

### [Deleted User] (2022-01-22)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-24)

This ReleaseBlock issue's priority is being increased in accordance with go/cros-bug-slo-guidelines#release-blockers.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@chromium.org (2022-01-24)

[Comment Deleted]

### yu...@chromium.org (2022-01-24)

@rhezashan thanks for the follow up. I think https://crbug.com/chromium/1286203#c23 is valuable. However I'm not able to reproduce it on latest trunk (99.0.4843). Do you have a way to reproduce it on latest trunk since we have some WebUI tab strip drag and drop fix landed recently? (in your video it's not reliably reproducible as well). If you do please update the steps in the CL description. I will look into it ASAP if I can reproduce the issue.

Lower to P1 for now since I'm not able to reproduce it.

### [Deleted User] (2022-01-24)

This ReleaseBlock issue's priority is being increased in accordance with go/cros-bug-slo-guidelines#release-blockers.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-01-24)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-01-25)

hi yuhengh@,

Sorry for delayed response. 

> Do you have a way to reproduce it on latest trunk since we have some WebUI tab strip drag and drop fix landed recently?
I'm not clear about this question, if I'm not mistaken you meant latest version? 
I've downloaded pre-built linux-release-chromeos_asan-linux-release-962393.zip (r962393 version 100.0.4850.0)  and tested just now and I could repro as well.

Let me brief some techniques how to repro this issue and use example as follow
Copied from comment https://crbug.com/chromium/1286203#c18 with #top-chrome-touch-ui:
(1) Open 2 tab.
(2) F5 <<--
(3) Drag one tab out from the browser.

since we need to pass --force-tablet-mode=touch_view --touch-devices=4 in command line,the fact we don't have a physical keyboard and so there's no F5 button
(1) Open browser and add new 3 tabs == totally 4 tabs.
(2) Open [tab] button near [+] button and drag out 2 tabs to left side.
(3) The window splits two side, left and right.
(4) Close one browser on left side.
----- after browser is closed, this similar like F5 function (overview mode) and only one browser remaining on the left window -----
(5) Drag one tab from right side to left window and move tab around for a while (to right window and then to left window).
(6) Crash!.
 
Hope this helps, please let me know if you have any questions.

### yu...@chromium.org (2022-01-25)

Okay, I see the problem now. I'm looking at your stack trace, the error happens on ash::DragDropController::OnMouseEvent
because you're passing the wrong number into --touch-devices.

In my case 

$ xinput
⎡ Virtual core pointer                    	id=2	[master pointer  (3)]
⎜   ↳ Virtual core XTEST pointer              	id=4	[slave  pointer  (2)]
⎜   ↳ Xvfb mouse                              	id=6	[slave  pointer  (2)]
⎣ Virtual core keyboard                   	id=3	[master keyboard (2)]
    ↳ Virtual core XTEST keyboard             	id=5	[slave  keyboard (3)]
    ↳ Xvfb keyboard                           	id=7	[slave  keyboard (3)]

4 is the right number for me but likely not on your computer. In the video, your mouse is still sending mouse events instead of the touch events.
The goal of this argument is to simulate touch events using mouse.
If you pass in the right number, you won't see the mouse when you cursor is inside the chromeos viewport and you won't hit this error since no mouse events are emitted. Please try with only touch events and let me know if you can still reproduce.


### rh...@gmail.com (2022-01-25)

Hi,

Thanks for the info.

>4 is the right number for me but likely not on your computer. In the video, your mouse is still sending mouse events instead of the touch events.

Okay
>The goal of this argument is to simulate touch events using mouse.

Okay

>Please try with only touch events and let me know if you can still reproduce

I will try later, I can't access my computer right now.

Thanks

### jo...@chromium.org (2022-01-25)

Re: https://bugs.chromium.org/p/chromium/issues/detail?id=1286203#c33, shouldn't the code be resilient against an invalid value passed in the command line?

### yu...@chromium.org (2022-01-26)

@jorgelo I agree we should fix this. However if it's not affecting any public users then it's probably a P3 bug.

### jo...@chromium.org (2022-01-26)

Isn't it a blocker for getting this out of behind the flag though? If you mark it as a P3 I doubt it'll happen before this ships.

### yu...@chromium.org (2022-01-26)

Which flag are you talking about? Both #touch-devices and #top-chrome-touch-ui are only used for internal testing and they are essential to reproduce this bug(correct me if I'm wrong). We never ship these flags to public users.

### jo...@chromium.org (2022-01-26)

Oh good. If we never plan to take this functionality from behind these flags P3 probably makes sense here.

### rh...@gmail.com (2022-01-28)

Hi yuhengh@,

Sorry for the delayed response.

I want to inform you that I could not reproduce this bug with --force-tablet-mode=touch_view  --touch-devices=12 (my xinput). 
If I'm not wrong, when both flags pass in the command line, the tab is not drag-able and can only move up and down. 

Anyway, thank you for looking into this issue, and I was pleased to hear that bug will be fixed.

Thanks

### yu...@chromium.org (2022-01-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-28)

Based on https://crbug.com/chromium/1286203#c38, this appears to be security_impact-none so adjusting accordingly 

### [Deleted User] (2022-01-28)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-01-30)

Hi yuhengh@,

I was testing this bug for more than two days, and I could repro this bug without MouseEvent.

re comment https://crbug.com/chromium/1286203#c20 : However, when testing on device, entering tablet mode will disable the physical keyboard.
I use ctrl + w to close the page on the repro video; however, if in the actual device, the user can close a page by dragging up the tab while dragging another tab ( This is my assuming). For convenience, I will purchase Chromebook Tablet and do a test soon.

Let me know what do you think?


### rh...@gmail.com (2022-01-30)

Hello,

Here's another screencast for this bug with a plugin installed with no mouseEvent and no Ctrl + W. 

Another potential bug is opening a new window with open a tab then, the HTML javascript `window.close()` for all pages. I currently have no clue how to pass open chrome with URL from the command line, and I'm sure it could be accessible to repro without a plugin.

for example if running: 
(1) chrome on linux (~/chrome --user-data-dir=/tmp/xxx http://localhost:8000/open.html)
(2) chrome on window (c:\chrome.exe --user-data-dir=c:\tmp\xxx http://localhost:8000/open.html)

But for linux-chromeOS, I can not pass http://localhost:8000/open.html on the command line.

Conclusion: I could repro this bug with the plugin installed. If the security sheriff watched the new screencast, I would appreciate it if this bug's Impact and Priority could be adjusted accordingly. I also would like to say, please disregard my comment https://crbug.com/chromium/1286203#c40 for convenience.

### rh...@gmail.com (2022-02-05)

Hello,

FYI, I was able to repro this issue without (MouseEvent, Plugin, shortcut ctrl +w). 
Please host newTab.html and run local web server.

run: ~/asan/chromeOS/asan-linux-release-966287/chrome --force-tablet-mode=touch_view --touch-devices=9 --disable-popup-blocking --user-data-dir=/tmp/chromeos --bwsi --login-user='$guest' --login-profile=user http://localhost:8000/newTab.html

I always hit issue #1286921 on the experiment  in the screencast given and finally I found the exactly same UaF for this issue without MousEvent or ctrl + w. Please refer to the new screencast.



### yu...@chromium.org (2022-02-07)

[Empty comment from Monorail migration]

### yu...@chromium.org (2022-02-07)

Bump to p2 since it can also happen on touch mode for website with deliberate script.

### mn...@chromium.org (2022-02-08)

[Empty comment from Monorail migration]

### os...@chromium.org (2022-02-10)

isn't this dup of 1282480?

### yu...@chromium.org (2022-02-10)

crbug.com/1282480 seems to be related to the original bug description. But https://crbug.com/chromium/1286203#c46 is a separate issue since TabDragDropDelegate also caches the source window
https://source.chromium.org/chromium/chromium/src/+/main:ash/drag_drop/tab_drag_drop_delegate.cc;l=89
We may need to observe source window similar to DragDropController does for TabDragDropDelegate in order to fix it.

### rh...@gmail.com (2022-02-15)

Uploading new screen-cast, I've tested on Stable version in real device. The new screen-cast could answer for following statements:

>> https://crbug.com/chromium/1286203#c22: "then I believe it's a real world issue worth looking into"
>> https://crbug.com/chromium/1286203#c24: "this seems to potentially be a security_impact-None"
>> https://crbug.com/chromium/1286203#c36: "However if it's not affecting any public users then it's probably a P3 bug" or P2  bug

Thanks 



### os...@chromium.org (2022-02-15)

If this is new issue, could you please file a new bug? Adding new case to existing bug makes it difficult to keep track of.

### rh...@gmail.com (2022-02-15)

Sorry, it was not a new issue. Video provided to show that this issue has an impact on real users.

### os...@chromium.org (2022-02-17)

then I'm a bit confused by the https://crbug.com/chromium/1286203#c51 by  yuhengh@

> crbug.com/1282480 seems to be related to the original bug description. But https://crbug.com/chromium/1286203#c46 is a separate issue since ..

and it looks like the repro step is very different. In any case, can you test on ToT(or at least m100)? I coudn't repro locally.



### os...@chromium.org (2022-02-18)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-02-18)

Oshima@,

Were you asking to me in https://crbug.com/chromium/1286203#c54?
>> and it looks like the repro step is very different. In any case, can you test on ToT(or at least m100)? I coudn't repro locally. 

I can repro at M100, I suggest use pre-built asan for repro.

### rh...@gmail.com (2022-02-18)

[Comment Deleted]

### os...@chromium.org (2022-02-19)

Oh, sorry I thought this is lacros issue. (removing lacros)
I couldn't repro with prebuild either although I had to use different gl impl (swiftshader) Can you test it with use-gl=swiftshader ?


### rh...@gmail.com (2022-02-19)

[Comment Deleted]

### os...@chromium.org (2022-02-28)

here you go

### rh...@gmail.com (2022-02-28)

thanks for the video. 

Please click the button from the link http://rhezashan.github.io/pocs/newTab.html and do not add the tab manually. If you click the button, it spawns a new tab, drags it outside the browser, and wait until pages closed. The javascript from the link closes the page automatically.


### yu...@chromium.org (2022-02-28)

@oshima I believe this is a WebUI tab strip issue. I will try to find a solution some time this week and let you know if I need any help. Sounds good?

### os...@chromium.org (2022-02-28)

so it looks like the when is deleted, the browser doesn't cancel the drag, unlike what happens during d&d session inside normal web contents, 
and it ends up with DragDropController::OnWindowDestroying, which calls into DragDropDelegate associated with the drag window.

I guess its either the delegate is deleted or the delegate is not handling the shutdown correctly.

#0  0x00007ffff0c4ffa8 in content::WebContentsImpl::GetRenderViewHost() () from /usr/local/google/home/oshima/chrome-git/src/out/cros/libcontent.so
#1  0x00007ffff0c6d6bc in content::WebContentsViewAura::CompleteDragExit() () from /usr/local/google/home/oshima/chrome-git/src/out/cros/libcontent.so
#2  0x00007ffff201f108 in ash::DragDropController::OnWindowDestroying(aura::Window*) () from /usr/local/google/home/oshima/chrome-git/src/out/cros/libash.so
#3  0x00007ffff2bdcbec in aura::Window::~Window() () from /usr/local/google/home/oshima/chrome-git/src/out/cros/libaura.so
#4  0x00007ffff2bdd398 in aura::Window::~Window() () from /usr/local/google/home/oshima/chrome-git/src/out/cros/libaura.so
#5  0x00007ffff0b4a20c in content::RenderWidgetHostImpl::Destroy(bool) () from /usr/local/google/home/oshima/chrome-git/src/out/cros/libcontent.so

I think you can just look into the code, add log and find the point that crashes.

### ad...@google.com (2022-03-10)

[Empty comment from Monorail migration]

### os...@chromium.org (2022-03-18)

yuhengh@, do you think you can work on this soon?
xdai@ let me know if someone in your team can work on it, and I can help.

### yu...@chromium.org (2022-03-21)

@oshima, sorry for the delay, looking into this now

### os...@chromium.org (2022-03-29)

[Empty comment from Monorail migration]

### np...@chromium.org (2022-03-29)

crbug.com/1310994 still repro's on my corp Chromebox even after I disable #webui-tab-strip (was on via Finch). Is there another workaround? 

### rh...@gmail.com (2022-04-01)

Hi yuhengh@ and oshima@,

I tested on ChromeOS Lacros Chromium 102.0.4967.0  the issue is reproduced. Maybe setting a Lacros label is better.

Sorry for another question, I'm also wondering about Security_Impact-None. Why the impact is None since this issue repro on tablet mode. I appreciate if you can elaborate.

For convenience, I tested this issue in Lenovo Duet 5 2 in 1 stable channel WITHOUT #top-chrome-touch-ui,webui-tab-strip . I detach the keyboard so the device transformed into tablet mode.  

I'm using the plugin from issue https://bugs.chromium.org/p/chromium/issues/detail?id=1286921#c7. Since the issue #1286921 has been merged into this issue because the same root problem.

If you have time, please see the video on the link below:
https://drive.google.com/file/d/1NhMbrVY8WisJayFsdHQUik2qrgK0WAKp/view?usp=sharing

Once again sorry.

### yu...@chromium.org (2022-04-01)

I filed another bug crbug.com/1312505, it's the easiest way to reproduce (without needing to enable webui tab strip and tablet mode)
The root cause is mostly the same and a fix is on the way.

### rh...@gmail.com (2022-04-01)

Thank you for fixing the issue!

### gi...@appspot.gserviceaccount.com (2022-04-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a49b599158fca8ac1e89d515c1314b884689e592

commit a49b599158fca8ac1e89d515c1314b884689e592
Author: Yuheng Huang <yuhengh@chromium.org>
Date: Thu Apr 07 17:04:49 2022

Fix ash browser crashes when the current tab closes during drag and drop

Bug: 1312505,1286203
Change-Id: I01db702539c1e72e6da57f71e1305ed09b8c020a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3553428
Reviewed-by: Mitsuru Oshima <oshima@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Yuheng Huang <yuhengh@chromium.org>
Cr-Commit-Position: refs/heads/main@{#989981}

[modify] https://crrev.com/a49b599158fca8ac1e89d515c1314b884689e592/chrome/browser/ui/views/drag_and_drop_interactive_uitest.cc
[modify] https://crrev.com/a49b599158fca8ac1e89d515c1314b884689e592/content/browser/web_contents/web_contents_view_aura.cc


### rh...@gmail.com (2022-04-07)

yuhengh@,

Thanks for fixing this issue. I've tested on 989995 and the UaF is still happening, the stack trace are same as https://crbug.com/chromium/1286921 

### yu...@chromium.org (2022-04-07)

This is just the 1st part of the fix. I will close the bug once all the parts are landed so you can test again. Thanks.

### rh...@gmail.com (2022-04-07)

Sorry, thanks

### gi...@appspot.gserviceaccount.com (2022-05-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1b2d340171481f0e5140104d536c3c67c1b0ad4e

commit 1b2d340171481f0e5140104d536c3c67c1b0ad4e
Author: Yuheng Huang <yuhengh@chromium.org>
Date: Thu May 12 17:24:39 2022

WebUI tab strip: fix crash when the dragging WebContents closes itself
during drag session

When WebUI tab strip is enabled, it's possible the dragging tab is
closed during a drag session. This CL prevents this scenario leading to
a crash.

Bug: 1286203
Change-Id: I800da37146058c5a01c7bb92eb8331a8ddc4d5c9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3539212
Commit-Queue: Yuheng Huang <yuhengh@chromium.org>
Reviewed-by: Mitsuru Oshima <oshima@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1002699}

[modify] https://crrev.com/1b2d340171481f0e5140104d536c3c67c1b0ad4e/ash/drag_drop/tab_drag_drop_delegate.h
[modify] https://crrev.com/1b2d340171481f0e5140104d536c3c67c1b0ad4e/ash/drag_drop/tab_drag_drop_delegate_unittest.cc
[modify] https://crrev.com/1b2d340171481f0e5140104d536c3c67c1b0ad4e/ash/drag_drop/tab_drag_drop_delegate.cc


### gi...@appspot.gserviceaccount.com (2022-05-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4b9d8f1fdbc8a56dfc69a64fa22eef9581b0ab88

commit 4b9d8f1fdbc8a56dfc69a64fa22eef9581b0ab88
Author: Yuheng Huang <yuhengh@chromium.org>
Date: Mon May 16 19:19:08 2022

WebUI tab strip: gracefully handle tab id not found cases after drop

We should not assume that the dragging tab is always available after
the tab is dropped since the tab can be closed during the drag session.
This CL handles some of the edge cases similar to the mentioned bug.

Bug: 1286203
Change-Id: If74ce82ec23d40e1bb3801a740ae4946cb1f1f6c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3646770
Reviewed-by: Thomas Lukaszewicz <tluk@chromium.org>
Commit-Queue: Yuheng Huang <yuhengh@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1003871}

[modify] https://crrev.com/4b9d8f1fdbc8a56dfc69a64fa22eef9581b0ab88/chrome/browser/ui/webui/tab_strip/tab_strip_page_handler.cc


### rh...@gmail.com (2022-06-08)

Friendly ping, Can you update on the status of this bug? 


### yu...@chromium.org (2022-06-09)

@rhezashan Sorry for the delay. I believe this is fixed. Can you confirm? I'm referring to the reproduce step with touch event in https://crbug.com/chromium/1286203#c62 since it's a real world issue.

### rh...@gmail.com (2022-06-09)

Yuhengh@,

Sorry but CL in #73,77,78 still not complete fixes, the crash is happening on r1012099. Please refer to screencast

### rh...@gmail.com (2022-06-09)

The stack trace UaF in screen cast are exactly same with issue #1286921 that has been merged into this issue.

=================================================================
==6233==ERROR: AddressSanitizer: heap-use-after-free on address 0x61500024d778 at pc 0x563d6c9f7655 bp 0x7ffffe81b2e0 sp 0x7ffffe81b2d8
READ of size 8 at 0x61500024d778 thread T0 (chrome)
SCARINESS: 51 (8-byte-read-heap-use-after-free)
    #0 0x563d6c9f7654 in operator bool base/memory/raw_ptr.h:806:59
    #1 0x563d6c9f7654 in IsRootWindow ui/aura/window.h:216:40
    #2 0x563d6c9f7654 in aura::Window::GetRootWindow() const ui/aura/window.cc:340:10
    #3 0x563d6d2b8df0 in ash::RootWindowController::ForWindow(aura::Window const*) ash/root_window_controller.cc:521:40
    #4 0x563d6d970d50 in ash::SplitViewController::Get(aura::Window const*) ash/wm/splitview/split_view_controller.cc:718:10
    #5 0x563d6d11fc5b in ash::TabDragDropDelegate::ShouldPreventSnapToTheEdge(gfx::Point const&) ash/drag_drop/tab_drag_drop_delegate.cc:266:7
    #6 0x563d6d11fb0e in ash::TabDragDropDelegate::DragUpdate(gfx::Point const&) ash/drag_drop/tab_drag_drop_delegate.cc:142:7
    #7 0x563d6d118647 in ash::DragDropController::DragUpdate(aura::Window*, ui::LocatedEvent const&) ash/drag_drop/drag_drop_controller.cc:581:30
    #8 0x563d6d11709a in ash::DragDropController::OnGestureEvent(ui::GestureEvent*) ash/drag_drop/drag_drop_controller.cc
    #9 0x563d694e33a9 in ui::EventDispatcher::DispatchEvent(ui::EventHandler*, ui::Event*) ui/events/event_dispatcher.cc:190:12
    #10 0x563d694e30cd in ui::EventDispatcher::DispatchEventToEventHandlers(std::Cr::vector<ui::EventHandler*, std::Cr::allocator<ui::EventHandler*>>*, ui::Event*) ui/events/event_dispatcher.cc:177:7
    #11 0x563d694e272f in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:125:3
    #12 0x563d694e23b6 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:83:14
    #13 0x563d694e2146 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:55:15
    #14 0x563d6ca0f993 in aura::WindowEventDispatcher::ProcessGestures(aura::Window*, std::Cr::vector<std::Cr::unique_ptr<ui::GestureEvent, std::Cr::default_delete<ui::GestureEvent>>, std::Cr::allocator<std::Cr::unique_ptr<ui::GestureEvent, std::Cr::default_delete<ui::GestureEvent>>>>) ui/aura/window_event_dispatcher.cc:352:15
    #15 0x563d6ca14bad in aura::WindowEventDispatcher::PostDispatchEvent(ui::EventTarget*, ui::Event const&) ui/aura/window_event_dispatcher.cc:606:16
    #16 0x563d694e2199 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:59:15
    #17 0x563d6ca19c19 in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #18 0x563d694e6b0e in ui::EventSource::DeliverEventToSink(ui::Event*) ui/events/event_source.cc:118:16
    #19 0x563d694e7006 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ui/events/event_source.cc:66:14
    #20 0x563d694e575b in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ui/events/event_rewriter.cc:88:39
    #21 0x563d5c9c293e in ui::EventRewriterChromeOS::RewriteEvent(ui::Event const&, base::WeakPtr<ui::EventRewriterContinuation>) ui/chromeos/events/event_rewriter_chromeos.cc:775:10
    #22 0x563d694e6fb6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ui/events/event_source.cc:67:32
    #23 0x563d694e575b in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ui/events/event_rewriter.cc:88:39
    #24 0x563d6d127a70 in ash::KeyboardDrivenEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr<ui::EventRewriterContinuation>) ash/events/keyboard_driven_event_rewriter.cc:31:12
    #25 0x563d694e6fb6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ui/events/event_source.cc:67:32
    #26 0x563d694e575b in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ui/events/event_rewriter.cc:88:39
    #27 0x563d6d123a56 in ash::AccessibilityEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr<ui::EventRewriterContinuation>) ash/events/accessibility_event_rewriter.cc
    #28 0x563d694e6fb6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ui/events/event_source.cc:67:32
    #29 0x563d694e575b in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ui/events/event_rewriter.cc:88:39
    #30 0x563d6cef812e in ash::AutoclickDragEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr<ui::EventRewriterContinuation>) ash/accessibility/autoclick/autoclick_drag_event_rewriter.cc
    #31 0x563d694e6fb6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ui/events/event_source.cc:67:32
    #32 0x563d694e575b in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ui/events/event_rewriter.cc:88:39
    #33 0x563d6cf05b9a in ash::FullscreenMagnifierController::RewriteEvent(ui::Event const&, base::WeakPtr<ui::EventRewriterContinuation>) ash/accessibility/magnifier/fullscreen_magnifier_controller.cc
    #34 0x563d694e67b1 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) ui/events/event_source.cc:144:29
    #35 0x563d6d15e85f in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event*) ui/aura/window_tree_host_platform.cc:229:38
    #36 0x563d6d165e28 in ash::AshWindowTreeHostPlatform::DispatchEvent(ui::Event*) ash/host/ash_window_tree_host_platform.cc:207:40
    #37 0x563d694f51b7 in Run base/callback.h:143:12
    #38 0x563d694f51b7 in ui::DispatchEventFromNativeUiEvent(ui::Event* const&, base::OnceCallback<void (ui::Event*)>) ui/events/ozone/events_ozone.cc:40:25
    #39 0x563d59a855e1 in ui::X11Window::DispatchUiEvent(ui::Event*, x11::Event const&) ui/ozone/platform/x11/x11_window.cc:1342:3
    #40 0x563d59a84e33 in ui::X11Window::DispatchEvent(ui::Event* const&) ui/ozone/platform/x11/x11_window.cc:1295:3
    #41 0x563d59a8591c in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event* const&) ui/ozone/platform/x11/x11_window.cc
    #42 0x563d6948bfa9 in ui::PlatformEventSource::DispatchEvent(ui::Event*) ui/events/platform/platform_event_source.cc:99:29
    #43 0x563d69c01a1f in ui::X11EventSource::OnEvent(x11::Event const&) ui/events/platform/x11/x11_event_source.cc:287:5
    #44 0x563d59697d85 in x11::Connection::DispatchEvent(x11::Event const&) ui/gfx/x/connection.cc:457:14
    #45 0x563d59697a93 in x11::Connection::ProcessNextEvent() ui/gfx/x/connection.cc:508:3
    #46 0x563d59697563 in x11::Connection::Dispatch() ui/gfx/x/connection.cc
    #47 0x563d69c0a933 in ui::X11EventWatcherFdWatch::OnFileCanReadWithoutBlocking(int) ui/events/platform/x11/x11_event_watcher_fdwatch.cc:64:15
    #48 0x563d672329aa in base::MessagePumpLibevent::OnLibeventNotification(int, short, void*) base/message_loop/message_pump_libevent.cc
    #49 0x563d6754f8cb in event_process_active base/third_party/libevent/event.c:381:4
    #50 0x563d6754f8cb in event_base_loop base/third_party/libevent/event.c:521:4
    #51 0x563d672332c6 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_libevent.cc:204:7
    #52 0x563d671289ab in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:542:12
    #53 0x563d67057c3f in base::RunLoop::Run(base::Location const&) base/run_loop.cc:141:14
    #54 0x563d6d114dc9 in ash::DragDropController::StartDragAndDrop(std::Cr::unique_ptr<ui::OSExchangeData, std::Cr::default_delete<ui::OSExchangeData>>, aura::Window*, aura::Window*, gfx::Point const&, int, ui::mojom::DragEventSource) ash/drag_drop/drag_drop_controller.cc:245:16
    #55 0x563d5e79e787 in content::WebContentsViewAura::StartDragging(content::DropData const&, blink::DragOperationsMask, gfx::ImageSkia const&, gfx::Vector2d const&, blink::mojom::DragEventSourceInfo const&, content::RenderWidgetHostImpl*) content/browser/web_contents/web_contents_view_aura.cc:1191:15
    #56 0x563d5e407fd0 in content::RenderWidgetHostImpl::StartDragging(mojo::StructPtr<blink::mojom::DragData>, blink::DragOperationsMask, SkBitmap const&, gfx::Vector2d const&, mojo::StructPtr<blink::mojom::DragEventSourceInfo>) content/browser/renderer_host/render_widget_host_impl.cc:2849:9
    #57 0x563d5b828808 in blink::mojom::FrameWidgetHostStubDispatch::Accept(blink::mojom::FrameWidgetHost*, mojo::Message*) gen/third_party/blink/public/mojom/page/widget.mojom.cc:3102:13
    #58 0x563d6927ddad in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:922:54
    #59 0x563d692911c7 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #60 0x563d69281078 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:664:20
    #61 0x563d687c8301 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ipc/ipc_mojo_bootstrap.cc:1010:24
    #62 0x563d687c2134 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind_internal.h:541:12
    #63 0x563d687c2134 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind_internal.h:705:12
    #64 0x563d687c2134 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::Cr::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> base/bind_internal.h:778:12
    #65 0x563d687c2134 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:747:12
    #66 0x563d670e5f46 in Run base/callback.h:143:12
    #67 0x563d670e5f46 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:135:32
    #68 0x563d67127311 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:424:29)> base/task/common/task_annotator.h:74:5
    #69 0x563d67127311 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:422:21
    #70 0x563d67126718 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:300:41
    #71 0x563d671280e1 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #72 0x563d67233209 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_libevent.cc:195:55
    #73 0x563d671289ab in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:542:12
    #74 0x563d67057c3f in base::RunLoop::Run(base::Location const&) base/run_loop.cc:141:14
    #75 0x563d5d78d912 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1039:18
    #76 0x563d5d791cfb in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:157:15
    #77 0x563d5d787b1a in content::BrowserMain(content::MainFunctionParams) content/browser/browser_main.cc:30:28
    #78 0x563d66e2b174 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:678:10
    #79 0x563d66e2dcd5 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1188:10
    #80 0x563d66e2d12d in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1059:12
    #81 0x563d66e26a76 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:407:36
    #82 0x563d66e27de2 in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:435:10
    #83 0x563d58651eb0 in ChromeMain chrome/app/chrome_main.cc:177:12
    #84 0x7f621fbb7082 in __libc_start_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

0x61500024d778 is located 248 bytes inside of 504-byte region [0x61500024d680,0x61500024d878)
freed by thread T0 (chrome) here:
    #0 0x563d5864ff4d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x563d670e5f46 in Run base/callback.h:143:12
    #2 0x563d670e5f46 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:135:32
    #3 0x563d67127311 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:424:29)> base/task/common/task_annotator.h:74:5
    #4 0x563d67127311 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:422:21
    #5 0x563d67126718 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:300:41
    #6 0x563d671280e1 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #7 0x563d67233209 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_libevent.cc:195:55
    #8 0x563d671289ab in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:542:12
    #9 0x563d67057c3f in base::RunLoop::Run(base::Location const&) base/run_loop.cc:141:14
    #10 0x563d6d114dc9 in ash::DragDropController::StartDragAndDrop(std::Cr::unique_ptr<ui::OSExchangeData, std::Cr::default_delete<ui::OSExchangeData>>, aura::Window*, aura::Window*, gfx::Point const&, int, ui::mojom::DragEventSource) ash/drag_drop/drag_drop_controller.cc:245:16
    #11 0x563d5e79e787 in content::WebContentsViewAura::StartDragging(content::DropData const&, blink::DragOperationsMask, gfx::ImageSkia const&, gfx::Vector2d const&, blink::mojom::DragEventSourceInfo const&, content::RenderWidgetHostImpl*) content/browser/web_contents/web_contents_view_aura.cc:1191:15
    #12 0x563d5e407fd0 in content::RenderWidgetHostImpl::StartDragging(mojo::StructPtr<blink::mojom::DragData>, blink::DragOperationsMask, SkBitmap const&, gfx::Vector2d const&, mojo::StructPtr<blink::mojom::DragEventSourceInfo>) content/browser/renderer_host/render_widget_host_impl.cc:2849:9
    #13 0x563d5b828808 in blink::mojom::FrameWidgetHostStubDispatch::Accept(blink::mojom::FrameWidgetHost*, mojo::Message*) gen/third_party/blink/public/mojom/page/widget.mojom.cc:3102:13
    #14 0x563d6927ddad in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:922:54
    #15 0x563d692911c7 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #16 0x563d69281078 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:664:20
    #17 0x563d687c8301 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ipc/ipc_mojo_bootstrap.cc:1010:24
    #18 0x563d687c2134 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind_internal.h:541:12
    #19 0x563d687c2134 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind_internal.h:705:12
    #20 0x563d687c2134 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::Cr::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> base/bind_internal.h:778:12
    #21 0x563d687c2134 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:747:12
    #22 0x563d670e5f46 in Run base/callback.h:143:12
    #23 0x563d670e5f46 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:135:32
    #24 0x563d67127311 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:424:29)> base/task/common/task_annotator.h:74:5
    #25 0x563d67127311 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:422:21
    #26 0x563d67126718 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:300:41
    #27 0x563d671280e1 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #28 0x563d67233209 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_libevent.cc:195:55
    #29 0x563d671289ab in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:542:12
    #30 0x563d67057c3f in base::RunLoop::Run(base::Location const&) base/run_loop.cc:141:14
    #31 0x563d5d78d912 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1039:18
    #32 0x563d5d791cfb in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:157:15
    #33 0x563d5d787b1a in content::BrowserMain(content::MainFunctionParams) content/browser/browser_main.cc:30:28
    #34 0x563d66e2b174 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:678:10
    #35 0x563d66e2dcd5 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1188:10
    #36 0x563d66e2d12d in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1059:12

previously allocated by thread T0 (chrome) here:
    #0 0x563d5864f6ed in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x563d6ce91c30 in views::NativeWidgetAura::NativeWidgetAura(views::internal::NativeWidgetDelegate*) ui/views/widget/native_widget_aura.cc:105:15
    #2 0x563d743e2711 in BrowserFrameAsh::BrowserFrameAsh(BrowserFrame*, BrowserView*) chrome/browser/ui/views/frame/browser_frame_ash.cc:75:7
    #3 0x563d743e25f2 in NativeBrowserFrameFactory::Create(BrowserFrame*, BrowserView*) chrome/browser/ui/views/frame/native_browser_frame_factory_chromeos.cc:12:14
    #4 0x563d742f280f in BrowserFrame::InitBrowserFrame() chrome/browser/ui/views/frame/browser_frame.cc:92:7
    #5 0x563d743dca50 in BrowserWindow::CreateBrowserWindow(std::Cr::unique_ptr<Browser, std::Cr::default_delete<Browser>>, bool, bool) chrome/browser/ui/views/frame/browser_window_factory.cc:55:18
    #6 0x563d73634c99 in CreateBrowserWindow chrome/browser/ui/browser.cc:317:10
    #7 0x563d73634c99 in Browser::Browser(Browser::CreateParams const&) chrome/browser/ui/browser.cc:543:29
    #8 0x563d7363383c in Browser::Create(Browser::CreateParams const&) chrome/browser/ui/browser.cc:456:14
    #9 0x563d737440d3 in StartupBrowserCreatorImpl::OpenTabsInBrowser(Browser*, chrome::startup::IsProcessStartup, std::Cr::vector<StartupTab, std::Cr::allocator<StartupTab>> const&) chrome/browser/ui/startup/startup_browser_creator_impl.cc:247:15
    #10 0x563d73746788 in StartupBrowserCreatorImpl::RestoreOrCreateBrowser(std::Cr::vector<StartupTab, std::Cr::allocator<StartupTab>> const&, StartupBrowserCreatorImpl::BrowserOpenBehavior, unsigned int, chrome::startup::IsProcessStartup, bool) chrome/browser/ui/startup/startup_browser_creator_impl.cc:649:13
    #11 0x563d73743a49 in StartupBrowserCreatorImpl::DetermineURLsAndLaunch(chrome::startup::IsProcessStartup) chrome/browser/ui/startup/startup_browser_creator_impl.cc:445:22
    #12 0x563d737430bc in StartupBrowserCreatorImpl::Launch(Profile*, chrome::startup::IsProcessStartup, std::Cr::unique_ptr<LaunchModeRecorder, std::Cr::default_delete<LaunchModeRecorder>>) chrome/browser/ui/startup/startup_browser_creator_impl.cc:170:32
    #13 0x563d7373e005 in StartupBrowserCreator::LaunchBrowser(base::CommandLine const&, Profile*, base::FilePath const&, chrome::startup::IsProcessStartup, chrome::startup::IsFirstRun, std::Cr::unique_ptr<LaunchModeRecorder, std::Cr::default_delete<LaunchModeRecorder>>) chrome/browser/ui/startup/startup_browser_creator.cc:682:9
    #14 0x563d7373ea02 in StartupBrowserCreator::LaunchBrowserForLastProfiles(base::CommandLine const&, base::FilePath const&, chrome::startup::IsProcessStartup, chrome::startup::IsFirstRun, StartupProfileInfo, std::Cr::vector<Profile*, std::Cr::allocator<Profile*>> const&) chrome/browser/ui/startup/startup_browser_creator.cc:747:7
    #15 0x563d7373d882 in StartupBrowserCreator::ProcessCmdLineImpl(base::CommandLine const&, base::FilePath const&, chrome::startup::IsProcessStartup, StartupProfileInfo, std::Cr::vector<Profile*, std::Cr::allocator<Profile*>> const&) chrome/browser/ui/startup/startup_browser_creator.cc:1264:3
    #16 0x563d7373c1fc in StartupBrowserCreator::Start(base::CommandLine const&, base::FilePath const&, StartupProfileInfo, std::Cr::vector<Profile*, std::Cr::allocator<Profile*>> const&) chrome/browser/ui/startup/startup_browser_creator.cc:637:10
    #17 0x563d6e85cc1f in ChromeBrowserMainParts::PreMainMessageLoopRunImpl() chrome/browser/chrome_browser_main.cc:1758:25
    #18 0x563d6e85b7b6 in ChromeBrowserMainParts::PreMainMessageLoopRun() chrome/browser/chrome_browser_main.cc:1157:18
    #19 0x563d60a49896 in ash::ChromeBrowserMainPartsAsh::PreMainMessageLoopRun() chrome/browser/ash/chrome_browser_main_parts_ash.cc:808:39
    #20 0x563d5d78b881 in content::BrowserMainLoop::PreMainMessageLoopRun() content/browser/browser_main_loop.cc:959:28
    #21 0x563d5e695e92 in Run base/callback.h:143:12
    #22 0x563d5e695e92 in content::StartupTaskRunner::RunAllTasksNow() content/browser/startup_task_runner.cc:43:29
    #23 0x563d5d78aeb6 in content::BrowserMainLoop::CreateStartupTasks() content/browser/browser_main_loop.cc:870:25
    #24 0x563d5d7914f1 in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams) content/browser/browser_main_runner_impl.cc:136:15
    #25 0x563d5d787adb in content::BrowserMain(content::MainFunctionParams) content/browser/browser_main.cc:26:32
    #26 0x563d66e2b174 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:678:10
    #27 0x563d66e2dcd5 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1188:10
    #28 0x563d66e2d12d in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1059:12
    #29 0x563d66e26a76 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:407:36
    #30 0x563d66e27de2 in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:435:10
    #31 0x563d58651eb0 in ChromeMain chrome/app/chrome_main.cc:177:12

SUMMARY: AddressSanitizer: heap-use-after-free base/memory/raw_ptr.h:806:59 in operator bool
Shadow bytes around the buggy address:
  0x0c2a80041a90: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a80041aa0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a80041ab0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa
  0x0c2a80041ac0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2a80041ad0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0c2a80041ae0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]
  0x0c2a80041af0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a80041b00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa
  0x0c2a80041b10: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2a80041b20: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a80041b30: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==6233==ABORTING


### yu...@chromium.org (2022-06-15)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-06-30)

yuhengh@,

Would it be possible to get an update?


### yu...@chromium.org (2022-06-30)

Sorry for the delay on this. We could set the source_window_ at [1] to nullptr when the source window is closed in this case and check it every time we use it.
This should get rid of a bunch of these uaf issues when the source window is closed during drag. I will prepare a fix later this week.

[1] https://source.chromium.org/chromium/chromium/src/+/main:ash/drag_drop/tab_drag_drop_delegate.h;l=99

### am...@chromium.org (2022-07-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-01)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-01)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### to...@igalia.com (2022-07-05)

Thanks for looping me in, yuhengh@

Trying to replicate locally based on the gn args in https://crbug.com/chromium/1286203#c58 and the launch command line shared by rhezashan@

### to...@igalia.com (2022-07-05)

The reported scenario does not seem to crash to me with ash/chrome tip of trunk, BUT I see this message on console stdout:

> 2022-07-05T15:49:58.840480Z INFO chrome[3826735:3826735]: [CONSOLE(12)] "Scripts may close only the windows that were opened by them.", source: https://rhezashan.github.io/pocs/newTab.html (12)

.. which might be preventing the window to actually being closed/destroyed.


### to...@igalia.com (2022-07-05)

Ok, I believe I got to reproduce the bug with Ash/Chrome web browser, after forcibly allowing 

> blink::WebSettings::SetAllowScriptsToCloseWindows()

with `true` in //third_party/blink/renderer/core/exported/web_view_impl.cc:

==3831314==ERROR: AddressSanitizer: heap-use-after-free on address 0x6150003438f8 at pc 0x55d173acc5c3 bp 0x7ffde07978e0 sp 0x7ffde07978d8
READ of size 8 at 0x6150003438f8 thread T0 (chrome)
LLVM Profile Warning: Unable to merge profile data: source profile file is not compatible.
LLVM Profile Error: Profile Merging of file default.profraw failed: Success
LLVM Profile Error: Failed to write file "default.profraw": Success
    #0 0x55d173acc5c2 in operator bool base/memory/raw_ptr.h:833:59
    #1 0x55d173acc5c2 in IsRootWindow ui/aura/window.h:216:40
    #2 0x55d173acc5c2 in aura::Window::GetRootWindow() const ui/aura/window.cc:340:10
    #3 0x55d174714304 in ash::RootWindowController::ForWindow(aura::Window const*) ash/root_window_controller.cc:521:40
    #4 0x55d17504f6dc in ash::SplitViewController::Get(aura::Window const*) ash/wm/splitview/split_view_controller.cc:718:10
    #5 0x55d1744dc163 in ash::TabDragDropDelegate::ShouldPreventSnapToTheEdge(gfx::Point const&) ash/drag_drop/tab_drag_drop_delegate.cc:268:7
    #6 0x55d1744dbee5 in ash::TabDragDropDelegate::DragUpdate(gfx::Point const&) ash/drag_drop/tab_drag_drop_delegate.cc:144:7
    #7 0x55d1744d2eae in ash::DragDropController::DragUpdate(aura::Window*, ui::LocatedEvent const&) ash/drag_drop/drag_drop_controller.cc:590:30
    #8 0x55d1744d1251 in ash::DragDropController::OnGestureEvent(ui::GestureEvent*) ash/drag_drop/drag_drop_controller.cc



rhezashan@ by chance, did you enable that setting so that web contents/JS is allowed to close windows?





### rh...@gmail.com (2022-07-05)

tonik...@, 

Thanks for looking this issue. 

>>Scripts may close only the windows that were opened by them.

chrome in normal chromeOS,Win,Linux,Mac and etc will not close the current page if user typed crafted HTML in the address bar. Need to pass from command line. 

In chromeOS, if want to open crafted HTML automatically, we need to enter guest mode. Please use following as below:

--- 1. less user interactions ---
chrome --force-tablet-mode=touch_view --touch-devices=9 --use-angle=swiftshader --ash-host-window-bounds="300+400-1200x800" --disable-popup-blocking --show-taps --user-data-dir=/tmp/chromeos --bwsi --login-user='$guest' --login-profile=user http://rhezashan.github.io/pocs/tabFlood.html

(*) after HTML launch, please hold one tab and wait for the crash. 

--- 2. lot user interactions ---
(1) open two tabs
(2) hold one tab
(3) close tabs with CTRL + W (2 times) 

Why there are two options to repro this issue (less/lot user interactions)? Because google VRP reduced the reward if reporter uses lot user interactions. I recommend use option 2 for testing locally. The stack of crash are identically same between those options. 

### rh...@gmail.com (2022-07-05)

I didnt read your previous comments in meantime, I was replaying your https://crbug.com/chromium/1286203#c92.

I didnt use any command you mentioned "rhezashan@ by chance, did you enable that setting so that web contents/JS is allowed to close windows"

Please see my https://crbug.com/chromium/1286203#c94

### to...@igalia.com (2022-07-05)

rhezashan@ I believe to have a CL locally that fixes the crash.

For the record, in the scenarios you uploaded the videos for, the expected behavior is that both the original/source window, and the detached one (dragged tab) get destroyed smoothly, and no crash is observed, right?

### rh...@gmail.com (2022-07-05)

tonik...@

Thanks for fixing the issue. 

Did you mean:
(1) open two tabs
(2) drag and hold second tab and move somewhere
(3) ctrl + w second tab. <-- no crash. 
(4) ctrl + w last one tab. <-- crash. 

If you Were asking for point three, yes no crash at all. It needs to destroy all tabs to get crashes. 

### to...@igalia.com (2022-07-05)

Finishing the unittest..

### jo...@chromium.org (2022-07-08)

How are we doing here folks?

### gi...@appspot.gserviceaccount.com (2022-07-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0012f7cb19971971f1d956a5b7aaf6a773091f85

commit 0012f7cb19971971f1d956a5b7aaf6a773091f85
Author: Antonio Gomes <tonikitoo@igalia.com>
Date: Fri Jul 08 19:28:59 2022

[WebUITabStrip] Crash @TabDragDropDelegate::ShouldPreventSnapToTheEdge()

When performing a tab dragging, with WebUITabStrip ON, an instance
of TabDragDropDelegate is created. The logic in this class relies
heavily on a valid |source_window_| class member, passed in as ctor
parameter.
When, during a drag drop operation, this |source_window_ object
is destroyed, UAF crashes can happen in many places in
TabDragDropDelegate.

This CL makes use of a WindowObserver installed in DragDropController
to cease the operation of its TabDragDropDelegate instance, when
the respective |source_window_| is destroyed.

BUG=1286203
R=oshima@chromium.org

Change-Id: I3d59017945d5b3e01eaf31de7d38b2898e660d62
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3747280
Reviewed-by: Mitsuru Oshima <oshima@chromium.org>
Commit-Queue: Antonio Gomes <tonikitoo@igalia.com>
Cr-Commit-Position: refs/heads/main@{#1022261}

[modify] https://crrev.com/0012f7cb19971971f1d956a5b7aaf6a773091f85/ash/drag_drop/tab_drag_drop_delegate.cc
[modify] https://crrev.com/0012f7cb19971971f1d956a5b7aaf6a773091f85/ash/drag_drop/drag_drop_controller.cc
[modify] https://crrev.com/0012f7cb19971971f1d956a5b7aaf6a773091f85/ash/drag_drop/drag_drop_controller_unittest.cc


### to...@igalia.com (2022-07-08)

Update: https://crbug.com/chromium/1286203#c100 is an attempt to fix the issue mentioned in https://crbug.com/chromium/1286203#c81

rhezashan@ I kindly ask for your verification.

### rh...@gmail.com (2022-07-10)

Hi tonik..@,

Sorry for late replying.
Thanks for fixing this issue, unfortunately I was OOO until 20th July and I currently don't have ubuntu workstation in hand, I will check the fix later if you don't mind.

### gi...@appspot.gserviceaccount.com (2022-07-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d13b578913ba7afbe401c22e7818721de16c7b6c

commit d13b578913ba7afbe401c22e7818721de16c7b6c
Author: Antonio Gomes <tonikitoo@igalia.com>
Date: Sun Jul 17 10:36:00 2022

fixup! [WebUITabStrip] Crash @TabDragDropDelegate::ShouldPreventSnapToTheEdge()

This CL is a follow up of [1], as per oshima@ remark.

It makes use of DragDropController::SetLoopClosureForTesting() API
rather than set_should_block_during_drag_drop() and task posting.

[1] https://crrev.com/c/3747280

BUG=1286203
R=oshima@chromium.org

Change-Id: Id9b9174d4c68a447462afa01dd3ef9874ac364d0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3755470
Commit-Queue: Antonio Gomes <tonikitoo@igalia.com>
Reviewed-by: Mitsuru Oshima <oshima@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1025076}

[modify] https://crrev.com/d13b578913ba7afbe401c22e7818721de16c7b6c/ash/drag_drop/drag_drop_controller_unittest.cc


### rh...@gmail.com (2022-07-18)

Hi tonik..@,

Sorry for the delay. Re your https://crbug.com/chromium/1286203#c101, I can confirm and tested ~4 times and I see no crash happened. Seems the CL works!

Thanks for the fix

### to...@igalia.com (2022-07-18)

[Comment Deleted]

### to...@igalia.com (2022-07-19)

Closing as FIXED as per https://crbug.com/chromium/1286203#c104. yuhengh@ feel free to reopen, if there is further work left.

### to...@igalia.com (2022-07-19)

Thanks for checking rhezashan@.

1) The bug has the "target-102" label, but only the CL in https://crbug.com/chromium/1286203#c73 is present in this release branch.
Missing CLs on 102.0.5005.164 branch: https://crbug.com/chromium/1286203#c77, https://crbug.com/chromium/1286203#c78 and https://crbug.com/chromium/1286203#c100.

2) OTOH, branch 103.0.5060.132 contains CLs in https://crbug.com/chromium/1286203#c73 and https://crbug.com/chromium/1286203#c77.
Missing CLs on 103.0.5060.132 branch: https://crbug.com/chromium/1286203#c78 and https://crbug.com/chromium/1286203#c100.

3) Last, branch 104.0.5112.53 contains CLs in https://crbug.com/chromium/1286203#c73, https://crbug.com/chromium/1286203#c77 and https://crbug.com/chromium/1286203#c78.
Missing CL on 104.0.5112.53 branch:  https://crbug.com/chromium/1286203#c100.

What release branch should we aim for here, for cherry-picking proposes?


### [Deleted User] (2022-07-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-20)

Requesting merge to extended stable M102 because latest trunk commit (1025076) appears to be after extended stable branch point (992738).

Requesting merge to stable M103 because latest trunk commit (1025076) appears to be after stable branch point (1002911).

Requesting merge to beta M104 because latest trunk commit (1025076) appears to be after beta branch point (1012729).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-20)

Merge review required: M104 is already shipping to beta.

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
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-20)

Merge review required: M103 is already shipping to stable.

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

### [Deleted User] (2022-07-20)

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

### am...@chromium.org (2022-07-25)

Apologies for stepping out of my swimlane some here, as this issue Chrome OS specific, but wanted to tag in some Chrome OS release and security folks given the M104 stable cut deadline tomorrow and given the time since questions in https://crbug.com/chromium/1286203#c107. Adding obenedict@ as Chrome OS M104 milestone owner and chmiel@ as Chrome OS security TPM 

There are no further planned releases of M103/stable or M102/Extended, so I will remove the merge labels for those. This issue should be reviewed for backmerge to M104 given this is a >medium severity security bug. 

### ob...@google.com (2022-07-26)

[Comment Deleted]

### ob...@google.com (2022-07-26)

Please complete the questions generated by the bot for an M104 approval. See below:

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

### jo...@chromium.org (2022-07-26)

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
Security fix

2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/3747280
https://chromium-review.googlesource.com/c/chromium/src/+/3755470

3. Have the changes been released and tested on canary?
Yes.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
Probably not.

### [Deleted User] (2022-07-26)

Merge review required: M104 has already been cut for stable release.

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
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### to...@igalia.com (2022-07-26)

re (https://crbug.com/chromium/1286203#c117 by jorgelo@chromium.org):

I believe only https://chromium-review.googlesource.com/c/chromium/src/+/3747280 needs approval for m104 merging (the other CL is a cosmetics followup)

### jo...@chromium.org (2022-07-26)

Ah, good to know. Makes things easier.

### gi...@appspot.gserviceaccount.com (2022-07-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a9c8f7ccbb014aabdc457dff61f2b9ea689e86ae

commit a9c8f7ccbb014aabdc457dff61f2b9ea689e86ae
Author: Antonio Gomes <tonikitoo@igalia.com>
Date: Tue Jul 26 18:48:24 2022

[m104][WebUITabStrip] Crash @TabDragDropDelegate::ShouldPreventSnapToTheEdge()

When performing a tab dragging, with WebUITabStrip ON, an instance
of TabDragDropDelegate is created. The logic in this class relies
heavily on a valid |source_window_| class member, passed in as ctor
parameter.
When, during a drag drop operation, this |source_window_ object
is destroyed, UAF crashes can happen in many places in
TabDragDropDelegate.

This CL makes use of a WindowObserver installed in DragDropController
to cease the operation of its TabDragDropDelegate instance, when
the respective |source_window_| is destroyed.

BUG=1286203
R=​oshima@chromium.org

(cherry picked from commit 0012f7cb19971971f1d956a5b7aaf6a773091f85)

Change-Id: I3d59017945d5b3e01eaf31de7d38b2898e660d62
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3747280
Reviewed-by: Mitsuru Oshima <oshima@chromium.org>
Commit-Queue: Antonio Gomes <tonikitoo@igalia.com>
Cr-Original-Commit-Position: refs/heads/main@{#1022261}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3788041
Auto-Submit: Jorge Lucangeli Obes <jorgelo@chromium.org>
Commit-Queue: Mitsuru Oshima <oshima@chromium.org>
Cr-Commit-Position: refs/branch-heads/5112@{#1215}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/a9c8f7ccbb014aabdc457dff61f2b9ea689e86ae/ash/drag_drop/tab_drag_drop_delegate.cc
[modify] https://crrev.com/a9c8f7ccbb014aabdc457dff61f2b9ea689e86ae/ash/drag_drop/drag_drop_controller.cc
[modify] https://crrev.com/a9c8f7ccbb014aabdc457dff61f2b9ea689e86ae/ash/drag_drop/drag_drop_controller_unittest.cc


### [Deleted User] (2022-07-26)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2022-07-27)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2022-07-28)

Congratulations, Rheza! The VRP Panel has decided to award you $3,000 for this report. The reward amount was decided based on this issue being significantly mitigated by not being remote exploitable and user interaction. Thank you for your efforts and reporting this issue to us. 

### rh...@gmail.com (2022-07-28)

Thanks for the rewards.

### rz...@google.com (2022-07-28)

[Empty comment from Monorail migration]

### ob...@google.com (2022-07-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-02)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-04)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-08-04)

1. 3, https://crrev.com/c/3793784/2, https://crrev.com/c/3793828/3, https://crrev.com/c/3794210/3
2. Low, just minor conflicts with missing checks
3. 104
4. Yes

### rz...@google.com (2022-08-10)

[Empty comment from Monorail migration]

### gm...@google.com (2022-08-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-11)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-08-11)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-11)

1. 3 CLs https://chromium-review.googlesource.com/q/topic:1286203_5005
2. Low, no conflicts
3. 104
4. Yes

### [Deleted User] (2022-08-11)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gm...@google.com (2022-08-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-11)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gm...@google.com (2022-08-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/398ca5deed9da726494bff01b1613c6640fcddd1

commit 398ca5deed9da726494bff01b1613c6640fcddd1
Author: Yuheng Huang <yuhengh@chromium.org>
Date: Fri Aug 12 10:48:52 2022

[M96-LTS] Fix ash browser crashes when the current tab closes during drag and drop

(cherry picked from commit a49b599158fca8ac1e89d515c1314b884689e592)

Bug: 1312505,1286203
Change-Id: I01db702539c1e72e6da57f71e1305ed09b8c020a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3553428
Commit-Queue: Yuheng Huang <yuhengh@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#989981}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3793784
Owners-Override: Oleh Lamzin <lamzin@google.com>
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1675}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/398ca5deed9da726494bff01b1613c6640fcddd1/chrome/browser/ui/views/drag_and_drop_interactive_uitest.cc
[modify] https://crrev.com/398ca5deed9da726494bff01b1613c6640fcddd1/content/browser/web_contents/web_contents_view_aura.cc


### gi...@appspot.gserviceaccount.com (2022-08-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2fe0fd46fb541dc107de446b7d75a88eed176295

commit 2fe0fd46fb541dc107de446b7d75a88eed176295
Author: Yuheng Huang <yuhengh@chromium.org>
Date: Fri Aug 12 13:59:33 2022

[M102-LTS] WebUI tab strip: fix crash when the dragging WebContents closes itself
during drag session

When WebUI tab strip is enabled, it's possible the dragging tab is
closed during a drag session. This CL prevents this scenario leading to
a crash.

(cherry picked from commit 1b2d340171481f0e5140104d536c3c67c1b0ad4e)

Bug: 1286203
Change-Id: I800da37146058c5a01c7bb92eb8331a8ddc4d5c9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3539212
Commit-Queue: Yuheng Huang <yuhengh@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1002699}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3823066
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Owners-Override: Oleh Lamzin <lamzin@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1297}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/2fe0fd46fb541dc107de446b7d75a88eed176295/ash/drag_drop/tab_drag_drop_delegate.h
[modify] https://crrev.com/2fe0fd46fb541dc107de446b7d75a88eed176295/ash/drag_drop/tab_drag_drop_delegate_unittest.cc
[modify] https://crrev.com/2fe0fd46fb541dc107de446b7d75a88eed176295/ash/drag_drop/tab_drag_drop_delegate.cc


### rz...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/83634e12c21c9b174b16d2c20d4cd2c4649eb717

commit 83634e12c21c9b174b16d2c20d4cd2c4649eb717
Author: Yuheng Huang <yuhengh@chromium.org>
Date: Fri Aug 12 16:55:33 2022

[M102-LTS] WebUI tab strip: gracefully handle tab id not found cases after drop

We should not assume that the dragging tab is always available after
the tab is dropped since the tab can be closed during the drag session.
This CL handles some of the edge cases similar to the mentioned bug.

(cherry picked from commit 4b9d8f1fdbc8a56dfc69a64fa22eef9581b0ab88)

Bug: 1286203
Change-Id: If74ce82ec23d40e1bb3801a740ae4946cb1f1f6c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3646770
Commit-Queue: Yuheng Huang <yuhengh@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1003871}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3822589
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Owners-Override: Oleh Lamzin <lamzin@google.com>
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1301}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/83634e12c21c9b174b16d2c20d4cd2c4649eb717/chrome/browser/ui/webui/tab_strip/tab_strip_page_handler.cc


### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6d8deb4643cc481ebbff03eb719f63118b5c2238

commit 6d8deb4643cc481ebbff03eb719f63118b5c2238
Author: Antonio Gomes <tonikitoo@igalia.com>
Date: Sat Aug 13 09:46:07 2022

[M102-LTS][WebUITabStrip] Crash @TabDragDropDelegate::ShouldPreventSnapToTheEdge()

When performing a tab dragging, with WebUITabStrip ON, an instance
of TabDragDropDelegate is created. The logic in this class relies
heavily on a valid |source_window_| class member, passed in as ctor
parameter.
When, during a drag drop operation, this |source_window_ object
is destroyed, UAF crashes can happen in many places in
TabDragDropDelegate.

This CL makes use of a WindowObserver installed in DragDropController
to cease the operation of its TabDragDropDelegate instance, when
the respective |source_window_| is destroyed.

BUG=1286203
R=​oshima@chromium.org

(cherry picked from commit 0012f7cb19971971f1d956a5b7aaf6a773091f85)

Change-Id: I3d59017945d5b3e01eaf31de7d38b2898e660d62
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3747280
Commit-Queue: Antonio Gomes <tonikitoo@igalia.com>
Cr-Original-Commit-Position: refs/heads/main@{#1022261}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3823163
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Owners-Override: Oleh Lamzin <lamzin@google.com>
Reviewed-by: Antonio Gomes <tonikitoo@igalia.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1303}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/6d8deb4643cc481ebbff03eb719f63118b5c2238/ash/drag_drop/tab_drag_drop_delegate.cc
[modify] https://crrev.com/6d8deb4643cc481ebbff03eb719f63118b5c2238/ash/drag_drop/drag_drop_controller.cc
[modify] https://crrev.com/6d8deb4643cc481ebbff03eb719f63118b5c2238/ash/drag_drop/drag_drop_controller_unittest.cc


### rz...@google.com (2022-08-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1286203?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1286858, crbug.com/chromium/1286921, crbug.com/chromium/1292272, crbug.com/chromium/1310994]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058468)*
