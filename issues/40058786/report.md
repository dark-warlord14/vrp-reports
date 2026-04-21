# Security: heap-use-after-free ash/drag_drop/drag_drop_tracker.cc:109

| Field | Value |
|-------|-------|
| **Issue ID** | [40058786](https://issues.chromium.org/issues/40058786) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Shell>UIFoundations |
| **Platforms** | ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2022-02-15 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86\_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36  

Platform: Linux-chromeOS

Steps to reproduce the problem:  

PoC

**(1)** Tested on linux-chromeOS Asan.  

**(2)** Force chromeOS to tablet mode pass in command line --force-tablet-mode=touch\_view --touch-devices=12 (touch-devices=[int] depends on your computer "$ xinput"). This command is to simulate real device( tablet mode) so there's will be no cursor.  

**(3)** Add new desk at least one or two desk.  

(4) Open browser and and new tab.  

(5) Swipe up from button to open split view, and browser on left while desk template showing on right side  

(5) Drag and hold the tab and pick empty desk.  

(6) Back to the previous desk and click browser.

What is the expected behavior?  

not crash

# What went wrong?

==9102==ERROR: AddressSanitizer: heap-use-after-free on address 0x6150001520f8 at pc 0x55c518bfa2b7 bp 0x7fffd35f07a0 sp 0x7fffd35f0798  

READ of size 8 at 0x6150001520f8 thread T0 (chrome)  

#0 0x55c518bfa2b6 in operator bool base/memory/raw\_ptr.h:645:14  

#1 0x55c518bfa2b6 in IsRootWindow ui/aura/window.h:217:40  

#2 0x55c518bfa2b6 in GetRootWindow ui/aura/window.cc:338:10  

#3 0x55c518bfa2b6 in aura::Window::GetRootWindow() ui/aura/window.cc:334:41  

#4 0x55c518c16e54 in CanDispatchToConsumer ui/aura/window\_event\_dispatcher.cc:598:47  

#5 0x55c518c16e54 in non-virtual thunk to aura::WindowEventDispatcher::CanDispatchToConsumer(ui::GestureConsumer\*) ui/aura/window\_event\_dispatcher.cc  

#6 0x55c518bee976 in FindDispatchHelperForConsumer ui/events/gestures/gesture\_recognizer\_impl.cc:415:16  

#7 0x55c518bee976 in ui::GestureRecognizerImpl::CancelActiveTouchesImpl(ui::GestureConsumer\*) ui/events/gestures/gesture\_recognizer\_impl.cc:346:32  

#8 0x55c518bee5d1 in ui::GestureRecognizerImpl::CancelActiveTouchesExceptImpl(ui::GestureConsumer\*) ui/events/gestures/gesture\_recognizer\_impl.cc:342:5  

#9 0x55c518bef0a3 in ui::GestureRecognizerImpl::TransferEventsTo(ui::GestureConsumer\*, ui::GestureConsumer\*, ui::TransferTouchesBehavior) ui/events/gestures/gesture\_recognizer\_impl.cc:152:3  

#10 0x55c5192bd687 in ash::DragDropCaptureDelegate::TakeCapture(aura::Window\*, aura::Window\*, base::RepeatingCallback<void ()>, ui::TransferTouchesBehavior) ash/drag\_drop/drag\_drop\_capture\_delegate.cc:57:51  

#11 0x55c5192bef2c in ash::DragDropController::StartDragAndDrop(std::\_\_1::unique\_ptr<ui::OSExchangeData, std::\_\_1::default\_delete[ui::OSExchangeData](javascript:void(0);) >, aura::Window\*, aura::Window\*, gfx::Point const&, int, ui::mojom::DragEventSource) ash/drag\_drop/drag\_drop\_controller.cc:206:32  

#12 0x55c50ad091a0 in content::WebContentsViewAura::StartDragging(content::DropData const&, blink::DragOperationsMask, gfx::ImageSkia const&, gfx::Vector2d const&, blink::mojom::DragEventSourceInfo const&, content::RenderWidgetHostImpl\*) content/browser/web\_contents/web\_contents\_view\_aura.cc:1179:15  

#13 0x55c50a99db2e in content::RenderWidgetHostImpl::StartDragging(mojo::StructPtr[blink::mojom::DragData](javascript:void(0);), blink::DragOperationsMask, SkBitmap const&, gfx::Vector2d const&, mojo::StructPtr[blink::mojom::DragEventSourceInfo](javascript:void(0);)) content/browser/renderer\_host/render\_widget\_host\_impl.cc:2842:9  

#14 0x55c50845441c in blink::mojom::FrameWidgetHostStubDispatch::Accept(blink::mojom::FrameWidgetHost\*, mojo::Message\*) gen/third\_party/blink/public/mojom/page/widget.mojom.cc:3063:13  

#15 0x55c514a01a5a in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:901:54  

#16 0x55c514a145a7 in mojo::MessageDispatcher::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#17 0x55c514a04926 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:658:20  

#18 0x55c5149c72a9 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ipc/ipc\_mojo\_bootstrap.cc:1008:24  

#19 0x55c5149c0f1b in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind\_internal.h:542:12  

#20 0x55c5149c0f1b in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind\_internal.h:706:12  

#21 0x55c5149c0f1b in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), std::\_\_1::tuple<scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> base/bind\_internal.h:779:12  

#22 0x55c5149c0f1b in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*) base/bind\_internal.h:748:12  

#23 0x55c513239ef6 in Run base/callback.h:142:12  

#24 0x55c513239ef6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task\_annotator.cc:135:32  

#25 0x55c51327ba67 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:387:29)> base/task/common/task\_annotator.h:74:5  

#26 0x55c51327ba67 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:385:21  

#27 0x55c51327b167 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:290:41  

#28 0x55c51327c701 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc  

#29 0x55c5133bb51d in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_libevent.cc:195:55  

#30 0x55c51327cdba in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:497:12  

#31 0x55c5131b3f6c in base::RunLoop::Run(base::Location const&) base/run\_loop.cc:141:14  

#32 0x55c509db81f2 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser\_main\_loop.cc:1056:18  

#33 0x55c509dbc771 in content::BrowserMainRunnerImpl::Run() content/browser/browser\_main\_runner\_impl.cc:155:15  

#34 0x55c509db259a in content::BrowserMain(content::MainFunctionParams) content/browser/browser\_main.cc:30:28  

#35 0x55c512f920af in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:642:10  

#36 0x55c512f94bf8 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content\_main\_runner\_impl.cc:1175:10  

#37 0x55c512f94048 in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner\_impl.cc:1042:12  

#38 0x55c512f8e829 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) content/app/content\_main.cc:401:36  

#39 0x55c512f8eea5 in content::ContentMain(content::ContentMainParams) content/app/content\_main.cc:429:10  

#40 0x55c5051c515a in ChromeMain chrome/app/chrome\_main.cc:176:12  

#41 0x7f84483740b2 in \_\_libc\_start\_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

0x6150001520f8 is located 248 bytes inside of 504-byte region [0x615000152000,0x6150001521f8)  

freed by thread T0 (chrome) here:  

#0 0x55c5051c319d in operator delete(void\*) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:152:3  

#1 0x55c5192c6555 in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:54:5  

#2 0x55c5192c6555 in reset buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:315:7  

#3 0x55c5192c6555 in ~unique\_ptr buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:269:19  

#4 0x55c5192c6555 in ash::DragDropTracker::~DragDropTracker() ash/drag\_drop/drag\_drop\_tracker.cc:114:1  

#5 0x55c5192bd470 in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:54:5  

#6 0x55c5192bd470 in std::\_\_1::unique\_ptr<ash::DragDropTracker, std::\_\_1::default\_delete[ash::DragDropTracker](javascript:void(0);) >::reset(ash::DragDropTracker\*) buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:315:7  

#7 0x55c5192bd437 in ash::DragDropCaptureDelegate::~DragDropCaptureDelegate() ash/drag\_drop/drag\_drop\_capture\_delegate.cc:45:22  

#8 0x55c5192c50a2 in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:54:5  

#9 0x55c5192c50a2 in std::\_\_1::unique\_ptr<ash::TabDragDropDelegate, std::\_\_1::default\_delete[ash::TabDragDropDelegate](javascript:void(0);) >::reset(ash::TabDragDropDelegate\*) buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:315:7  

#10 0x55c5192be0d7 in ash::DragDropController::Cleanup() ash/drag\_drop/drag\_drop\_controller.cc:726:27  

#11 0x55c5192c490d in ash::DragDropController::DoDragCancel(base::TimeDelta) ash/drag\_drop/drag\_drop\_controller.cc:659:3  

#12 0x55c51542ba2b in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ui/events/event\_dispatcher.cc:190:12  

#13 0x55c51542b819 in ui::EventDispatcher::DispatchEventToEventHandlers(std::\_\_1::vector<ui::EventHandler\*, std::\_\_1::allocator[ui::EventHandler\\*](javascript:void(0);) >\*, ui::Event\*) ui/events/event\_dispatcher.cc:177:7  

#14 0x55c51542ae3d in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:125:3  

#15 0x55c51542aac4 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:83:14  

#16 0x55c51542a830 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:55:15  

#17 0x55c518c1b7af in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:49:17  

#18 0x55c518c170cd in aura::WindowEventDispatcher::DispatchSyntheticTouchEvent(ui::TouchEvent\*) ui/aura/window\_event\_dispatcher.cc:610:29  

#19 0x55c518beeab8 in ui::GestureRecognizerImpl::CancelActiveTouchesImpl(ui::GestureConsumer\*) ui/events/gestures/gesture\_recognizer\_impl.cc:356:13  

#20 0x55c518bf84d3 in aura::Window::CleanupGestureState() ui/aura/window.cc:1263:48  

#21 0x55c518bf85be in aura::Window::CleanupGestureState() ui/aura/window.cc:1274:30  

#22 0x55c518c130c7 in aura::WindowEventDispatcher::OnWindowHidden(aura::Window\*, aura::WindowEventDispatcher::WindowHiddenReason) ui/aura/window\_event\_dispatcher.cc:374:14  

#23 0x55c518c178da in aura::WindowEventDispatcher::OnWindowVisibilityChanged(aura::Window\*, bool) ui/aura/window\_event\_dispatcher.cc:681:5  

#24 0x55c518c03c76 in aura::Window::NotifyWindowVisibilityChangedAtReceiver(aura::Window\*, bool) ui/aura/window.cc:1217:14  

#25 0x55c518c037ea in aura::Window::NotifyWindowVisibilityChangedDown(aura::Window\*, bool) ui/aura/window.cc:1223:8  

#26 0x55c518c01c6d in aura::Window::NotifyWindowVisibilityChanged(aura::Window\*, bool) ui/aura/window.cc:1204:8  

#27 0x55c518bfa8ce in aura::Window::SetVisibleInternal(bool) ui/aura/window.cc:1020:3  

#28 0x55c519976732 in ash::Desk::Deactivate(bool) ash/wm/desks/desk.cc:430:40  

#29 0x55c51997fd50 in ash::DesksController::ActivateDeskInternal(ash::Desk const\*, bool) ash/wm/desks/desks\_controller.cc:1212:15  

#30 0x55c51998ac6b in ash::DeskActivationAnimation::PrepareDeskForScreenshot(int) ash/wm/desks/desk\_animation\_impl.cc:299:16  

#31 0x55c51997207f in ash::DeskAnimationBase::OnStartingDeskScreenshotTaken(int) ash/wm/desks/desk\_animation\_base.cc:91:3  

#32 0x55c5199b52e6 in ash::RootWindowDeskSwitchAnimator::CompleteAnimationPhase1WithLayer(std::\_\_1::unique\_ptr<ui::Layer, std::\_\_1::default\_delete[ui::Layer](javascript:void(0);) >) ash/wm/desks/root\_window\_desk\_switch\_animator.cc:467:14  

#33 0x55c5199b5ae7 in ash::RootWindowDeskSwitchAnimator::OnStartingDeskScreenshotTaken(std::\_\_1::unique\_ptr<viz::CopyOutputResult, std::\_\_1::default\_delete[viz::CopyOutputResult](javascript:void(0);) >) ash/wm/desks/root\_window\_desk\_switch\_animator.cc:488:3  

#34 0x55c507e8e881 in base::OnceCallback<void (std::\_\_1::unique\_ptr<viz::CopyOutputResult, std::\_\_1::default\_delete[viz::CopyOutputResult](javascript:void(0);) >)>::Run(std::\_\_1::unique\_ptr<viz::CopyOutputResult, std::\_\_1::default\_delete[viz::CopyOutputResult](javascript:void(0);) >) && base/callback.h:142:12

previously allocated by thread T0 (chrome) here:  

#0 0x55c5051c293d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:95:3  

#1 0x55c5192c6368 in make\_unique<aura::Window, aura::WindowDelegate \*&> buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:725:28  

#2 0x55c5192c6368 in CreateCaptureWindow ash/drag\_drop/drag\_drop\_tracker.cc:90:7  

#3 0x55c5192c6368 in ash::DragDropTracker::DragDropTracker(aura::Window\*, base::RepeatingCallback<void ()>) ash/drag\_drop/drag\_drop\_tracker.cc:109:7  

#4 0x55c5192bd5bd in ash::DragDropCaptureDelegate::TakeCapture(aura::Window\*, aura::Window\*, base::RepeatingCallback<void ()>, ui::TransferTouchesBehavior) ash/drag\_drop/drag\_drop\_capture\_delegate.cc:53:32  

#5 0x55c5192bef2c in ash::DragDropController::StartDragAndDrop(std::\_\_1::unique\_ptr<ui::OSExchangeData, std::\_\_1::default\_delete[ui::OSExchangeData](javascript:void(0);) >, aura::Window\*, aura::Window\*, gfx::Point const&, int, ui::mojom::DragEventSource) ash/drag\_drop/drag\_drop\_controller.cc:206:32  

#6 0x55c50ad091a0 in content::WebContentsViewAura::StartDragging(content::DropData const&, blink::DragOperationsMask, gfx::ImageSkia const&, gfx::Vector2d const&, blink::mojom::DragEventSourceInfo const&, content::RenderWidgetHostImpl\*) content/browser/web\_contents/web\_contents\_view\_aura.cc:1179:15  

#7 0x55c50a99db2e in content::RenderWidgetHostImpl::StartDragging(mojo::StructPtr[blink::mojom::DragData](javascript:void(0);), blink::DragOperationsMask, SkBitmap const&, gfx::Vector2d const&, mojo::StructPtr[blink::mojom::DragEventSourceInfo](javascript:void(0);)) content/browser/renderer\_host/render\_widget\_host\_impl.cc:2842:9  

#8 0x55c50845441c in blink::mojom::FrameWidgetHostStubDispatch::Accept(blink::mojom::FrameWidgetHost\*, mojo::Message\*) gen/third\_party/blink/public/mojom/page/widget.mojom.cc:3063:13  

#9 0x55c514a01a5a in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:901:54  

#10 0x55c514a145a7 in mojo::MessageDispatcher::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#11 0x55c514a04926 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:658:20  

#12 0x55c5149c72a9 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ipc/ipc\_mojo\_bootstrap.cc:1008:24  

#13 0x55c5149c0f1b in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind\_internal.h:542:12  

#14 0x55c5149c0f1b in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind\_internal.h:706:12  

#15 0x55c5149c0f1b in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), std::\_\_1::tuple<scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> base/bind\_internal.h:779:12  

#16 0x55c5149c0f1b in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*) base/bind\_internal.h:748:12  

#17 0x55c513239ef6 in Run base/callback.h:142:12  

#18 0x55c513239ef6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task\_annotator.cc:135:32  

#19 0x55c51327ba67 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:387:29)> base/task/common/task\_annotator.h:74:5  

#20 0x55c51327ba67 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:385:21  

#21 0x55c51327b167 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:290:41  

#22 0x55c51327c701 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc  

#23 0x55c5133bb51d in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_libevent.cc:195:55  

#24 0x55c51327cdba in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:497:12  

#25 0x55c5131b3f6c in base::RunLoop::Run(base::Location const&) base/run\_loop.cc:141:14  

#26 0x55c509db81f2 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser\_main\_loop.cc:1056:18  

#27 0x55c509dbc771 in content::BrowserMainRunnerImpl::Run() content/browser/browser\_main\_runner\_impl.cc:155:15  

#28 0x55c509db259a in content::BrowserMain(content::MainFunctionParams) content/browser/browser\_main.cc:30:28  

#29 0x55c512f920af in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:642:10  

#30 0x55c512f94bf8 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content\_main\_runner\_impl.cc:1175:10  

#31 0x55c512f94048 in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner\_impl.cc:1042:12  

#32 0x55c512f8e829 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) content/app/content\_main.cc:401:36  

#33 0x55c512f8eea5 in content::ContentMain(content::ContentMainParams) content/app/content\_main.cc:429:10  

#34 0x55c5051c515a in ChromeMain chrome/app/chrome\_main.cc:176:12  

#35 0x7f84483740b2 in \_\_libc\_start\_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free base/memory/raw\_ptr.h:645:14 in operator bool  

Shadow bytes around the buggy address:  

0x0c2a800223c0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2a800223d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2a800223e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x0c2a800223f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c2a80022400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x0c2a80022410: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]  

0x0c2a80022420: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2a80022430: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x0c2a80022440: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c2a80022450: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2a80022460: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==9102==ABORTING

Did this work before? N/A

Chrome version: 100.0.4891.0 Channel: dev  

OS Version:

This issue is another UaF after fix was landed from issue #1292271.

It takes one more step to trigger UaF by returning to the previous desk (step 6) to reproduce this issue. While issue #1292271 when selecting a desk it immediately crashes (on step 5).

## Attachments

- [screencast_1297643.webm](attachments/screencast_1297643.webm) (video/webm, 5.1 MB)
- [Screen recording 2022-02-22 2.01.10 PM.webm](attachments/Screen recording 2022-02-22 2.01.10 PM.webm) (video/webm, 2.0 MB)
- [screencast__00014.webm](attachments/screencast_00014.webm) (video/webm, 5.5 MB)
- [screencast__00013.webm](attachments/screencast_00013.webm) (video/webm, 6.7 MB)
- [screencast__00009.webm](attachments/screencast_00009.webm) (video/webm, 3.3 MB)

## Timeline

### [Deleted User] (2022-02-15)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-02-15)

Uploading screen-cast

### al...@google.com (2022-02-22)

[Empty comment from Monorail migration]

### zx...@chromium.org (2022-02-22)

I tried to reproduce on ToT (chrome://version 101.0.4905) but I cannot reproduce the issue.

### rh...@gmail.com (2022-02-22)

Hi,

I uploaded new screen-cast, please take a look for repro.  I suggest use right click for dragging, also with left click is working too.


### be...@google.com (2022-02-25)

[Empty comment from Monorail migration]

[Monorail blocked-on: b/221467158]

### rh...@gmail.com (2022-02-25)

betuls@,

Can you cc xdai@ for this issue please? this issue related with the previous fix issue #1292271 and xdai teams might be the best for this.

### be...@google.com (2022-02-28)

Updated the cc list, thanks!

### be...@google.com (2022-02-28)

Setting the severity to low since this is a denial of service.

### [Deleted User] (2022-02-28)

[Empty comment from Monorail migration]

### xd...@chromium.org (2022-02-28)

Thanks for adding me. 
Looks like this crash happened in https://source.chromium.org/chromium/chromium/src/+/main:ash/drag_drop/drag_drop_capture_delegate.cc;drc=4a9149c03e79776bb35dcbfcaf0aafe5b11c8377;l=57, but at this moment the drag_drop_tracker_->capture_window() is already released during capture is cancelled, thus causing the UAF crash.

This might be the same crash as https://crbug.com/chromium/1297209. So assign to Oshima-san as well. 

### os...@chromium.org (2022-03-03)

can you test on ToT? There are severa changes went in to d&d and I want to make sure that crash is still present with this stack.

### rh...@gmail.com (2022-03-03)

Can you advice which prebuilt version I should test? Eq. Version >97xxxx?

### rh...@gmail.com (2022-03-03)

I'm still able to reproduced this issue on asan-linux-release-976923.zip.


### os...@chromium.org (2022-03-04)

Addition, can you take a look? Let me know if you need a help to start.

[Monorail components: UI>Shell>UIFoundations UI>Shell>WindowManager]

### al...@chromium.org (2022-03-07)

[Empty comment from Monorail migration]

### al...@chromium.org (2022-03-08)

I reproduced this on ToT.  Will investigate.

The repro step that was missing was the user tabbing to the other desk while dragging.  Doing that the 2nd time makes it crash.

### gi...@appspot.gserviceaccount.com (2022-03-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9cab337d20ee22001ea71929b6822455eaff4a2a

commit 9cab337d20ee22001ea71929b6822455eaff4a2a
Author: Addison Luh <aluh@chromium.org>
Date: Fri Mar 18 23:57:27 2022

[asan] Properly clean up state in aura::Window::CleanupGestureState.

A guard was added in commit 5a2a306942bc7e794ec147f685f5eb44e3746111
that exited from CleanupGestureState when the window was destroyed from
the gesture cancellation. However it exited too early, before the
consumer state was cleaned up. This causes later drag and drop gestures
to trigger use-after-free errors.

This change moves the exit condition until after all related states in
the gesture recognizer is cleaned up.

#asan #uaf

Bug: 1297643
Change-Id: I31c82ab3723c379515579cc32d8bed2ec93ec955
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3514815
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Addison Luh <aluh@chromium.org>
Auto-Submit: Addison Luh <aluh@chromium.org>
Cr-Commit-Position: refs/heads/main@{#982965}

[modify] https://crrev.com/9cab337d20ee22001ea71929b6822455eaff4a2a/ui/aura/window.cc
[modify] https://crrev.com/9cab337d20ee22001ea71929b6822455eaff4a2a/ui/aura/window_unittest.cc


### al...@chromium.org (2022-03-21)

FYI, the added test was disabled by crrev.com/c/3538048 due to it revealing a similar case of this issue. I'm fixing that in crrev.com/c/3539978 and re-enabling the test there.

As for this current issue, the fix is still in place, so I consider it fixed.

### al...@chromium.org (2022-03-21)

That other issue is tracked in crbug.com/1308221.

### [Deleted User] (2022-03-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-22)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-11)

Hello, Rheza and thank you for this report. Due to the amount of user interaction to trigger this issue and that this issue isn't web accessible, the VRP Panel has decided to award you $3,000 for this report. We appreciate you efforts and reporting this issue to us. 

### am...@google.com (2022-04-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### is...@google.com (2023-05-24)

This issue was migrated from crbug.com/chromium/1297643?no_tracker_redirect=1

[Multiple monorail components: UI>Shell>UIFoundations, UI>Shell>WindowManager]
[Monorail blocked-on: b/221467158]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058786)*
