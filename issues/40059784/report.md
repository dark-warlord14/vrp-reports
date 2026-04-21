# Security: Heap-use-after-free in ash::TabletModeBrowserWindowDragSessionWindowsHider::~TabletModeBrowserWindowDragSessionWindowsHider

| Field | Value |
|-------|-------|
| **Issue ID** | [40059784](https://issues.chromium.org/issues/40059784) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Shell |
| **Platforms** | ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | yu...@chromium.org |
| **Created** | 2022-05-28 |
| **Bounty** | $3,000.00 |

## Description

Chrome Version: linux-release-chromeos\_asan-linux-release-1008401.zip  

Operating System: Linux

**REPRODUCTION CASE**

Run chromeOS with --disable-popup-blocking --top-chrome-touch-ui=enabled

1. Open <https://lbstyle.github.io/alert.html> in two different desks (as in <https://crbug.com/chromium/1317746>)
2. Drag and drop a tab into the other desk

==32170==ERROR: AddressSanitizer: heap-use-after-free on address 0x615000103590 at pc 0x56020cff5f9c bp 0x7ffdf49447a0 sp 0x7ffdf4944798  

READ of size 8 at 0x615000103590 thread T0 (chrome)  

==32170==WARNING: invalid path to external symbolizer!  

==32170==WARNING: Failed to use and restart external symbolizer!  

#0 0x56020cff5f9b in begin ./../../buildtools/third\_party/libc++/trunk/include/vector:1427:30  

#1 0x56020cff5f9b in begin<std::Cr::vector<base::internal::CheckedObserverAdapter, std::Cr::allocator[base::internal::CheckedObserverAdapter](javascript:void(0);) > &> ./../../base/ranges/ranges.h:44:37  

#2 0x56020cff5f9b in begin<std::Cr::vector<base::internal::CheckedObserverAdapter, std::Cr::allocator[base::internal::CheckedObserverAdapter](javascript:void(0);) > &> ./../../base/ranges/ranges.h:105:10  

#3 0x56020cff5f9b in find\_if<std::Cr::vector<base::internal::CheckedObserverAdapter, std::Cr::allocator[base::internal::CheckedObserverAdapter](javascript:void(0);) > &, (lambda at ../../base/observer\_list.h:287:21), base::identity, std::Cr::random\_access\_iterator\_tag> ./../../base/ranges/algorithm.h:483:26  

#4 0x56020cff5f9b in base::ObserverList<aura::WindowObserver, true, true, base::internal::CheckedObserverAdapter>::RemoveObserver(aura::WindowObserver const\*) ./../../base/observer\_list.h:286:21  

#5 0x56020df8005a in ash::TabletModeBrowserWindowDragSessionWindowsHider::~TabletModeBrowserWindowDragSessionWindowsHider() ./../../ash/wm/tablet\_mode/tablet\_mode\_browser\_window\_drag\_session\_windows\_hider.cc:74:18  

#6 0x56020df802fd in ash::TabletModeBrowserWindowDragSessionWindowsHider::~TabletModeBrowserWindowDragSessionWindowsHider() ./../../ash/wm/tablet\_mode/tablet\_mode\_browser\_window\_drag\_session\_windows\_hider.cc:67:55  

#7 0x56020d7159da in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:51:5  

#8 0x56020d7159da in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:308:7  

#9 0x56020d7159da in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:262:19  

#10 0x56020d7159da in ash::TabDragDropDelegate::~TabDragDropDelegate() ./../../ash/drag\_drop/tab\_drag\_drop\_delegate.cc:123:1  

#11 0x56020d715bfd in ash::TabDragDropDelegate::~TabDragDropDelegate() ./../../ash/drag\_drop/tab\_drag\_drop\_delegate.cc:114:45  

#12 0x56020d717047 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:51:5  

#13 0x56020d717047 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:308:7  

#14 0x56020d717047 in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:262:19  

#15 0x56020d717047 in ~OwnedWrapper ./../../base/bind\_internal.h:142:7  

#16 0x56020d717047 in ~\_\_tuple\_leaf ./../../buildtools/third\_party/libc++/trunk/include/tuple:222:7  

#17 0x56020d717047 in ~tuple ./../../buildtools/third\_party/libc++/trunk/include/tuple:482:28  

#18 0x56020d717047 in ~BindState ./../../base/bind\_internal.h:977:24  

#19 0x56020d717047 in base::internal::BindState<void (ash::TabDragDropDelegate::\*)(gfx::Point const&, aura::Window\*), base::internal::OwnedWrapper<ash::TabDragDropDelegate, std::Cr::default\_delete[ash::TabDragDropDelegate](javascript:void(0);) >, gfx::Point>::Destroy(base::internal::BindStateBase const\*) ./../../base/bind\_internal.h:980:5  

#20 0x5602142408a2 in Run ./../../base/callback.h:144:3  

#21 0x5602142408a2 in ChromeNewWindowClient::NewWindowForDetachingTab(aura::Window\*, ui::OSExchangeData const&, base::OnceCallback<void (aura::Window\*)>) ./../../chrome/browser/ui/ash/chrome\_new\_window\_client.cc:286:24  

#22 0x56020d7168e9 in ash::TabDragDropDelegate::DropAndDeleteSelf(gfx::Point const&, ui::OSExchangeData const&) ./../../ash/drag\_drop/tab\_drag\_drop\_delegate.cc:162:36  

#23 0x56020d710261 in ash::DragDropController::PerformDrop(gfx::Point, ui::DropTargetEvent, std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);) >, base::OnceCallback<void (std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);) >, ui::mojom::DragOperation&)>, std::Cr::unique\_ptr<ash::TabDragDropDelegate, std::Cr::default\_delete[ash::TabDragDropDelegate](javascript:void(0);) >, base::ScopedClosureRunner) ./../../ash/drag\_drop/drag\_drop\_controller.cc:794:39  

#24 0x56020d7125a2 in void base::internal::FunctorTraits<void (ash::DragDropController::\*)(gfx::Point, ui::DropTargetEvent, std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);) >, base::OnceCallback<void (std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);) >, ui::mojom::DragOperation&)>, std::Cr::unique\_ptr<ash::TabDragDropDelegate, std::Cr::default\_delete[ash::TabDragDropDelegate](javascript:void(0);) >, base::ScopedClosureRunner), void>::Invoke<void (ash::DragDropController::\*)(gfx::Point, ui::DropTargetEvent, std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);) >, base::OnceCallback<void (std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);) >, ui::mojom::DragOperation&)>, std::Cr::unique\_ptr<ash::TabDragDropDelegate, std::Cr::default\_delete[ash::TabDragDropDelegate](javascript:void(0);) >, base::ScopedClosureRunner), base::WeakPtr[ash::DragDropController](javascript:void(0);), gfx::Point, ui::DropTargetEvent, std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);) >, base::OnceCallback<void (std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);) >, ui::mojom::DragOperation&)>, std::Cr::unique\_ptr<ash::TabDragDropDelegate, std::Cr::default\_delete[ash::TabDragDropDelegate](javascript:void(0);) >, base::ScopedClosureRunner>(void (ash::DragDropController::\*)(gfx::Point, ui::DropTargetEvent, std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);) >, base::OnceCallback<void (std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);) >, ui::mojom::DragOperation&)>, std::Cr::unique\_ptr<ash::TabDragDropDelegate, std::Cr::default\_delete[ash::TabDragDropDelegate](javascript:void(0);) >, base::ScopedClosureRunner), base::WeakPtr[ash::DragDropController](javascript:void(0);)&&, gfx::Point&&, ui::DropTargetEvent&&, std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);) >&&, base::OnceCallback<void (std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);) >, ui::mojom::DragOperation&)>&&, std::Cr::unique\_ptr<ash::TabDragDropDelegate, std::Cr::default\_delete[ash::TabDragDropDelegate](javascript:void(0);) >&&, base::ScopedClosureRunner&&) ./../../base/bind\_internal.h:541:12  

#25 0x56020d7122a8 in MakeItSo<void (ash::DragDropController::\*)(gfx::Point, ui::DropTargetEvent, std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);) >, base::OnceCallback<void (std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);) >, ui::mojom::DragOperation &)>, std::Cr::unique\_ptr<ash::TabDragDropDelegate, std::Cr::default\_delete[ash::TabDragDropDelegate](javascript:void(0);) >, base::ScopedClosureRunner), base::WeakPtr[ash::DragDropController](javascript:void(0);), gfx::Point, ui::DropTargetEvent, std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);) >, base::OnceCallback<void (std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);) >, ui::mojom::DragOperation &)>, std::Cr::unique\_ptr<ash::TabDragDropDelegate, std::Cr::default\_delete[ash::TabDragDropDelegate](javascript:void(0);) >, base::ScopedClosureRunner> ./../../base/bind\_internal.h:725:5  

#26 0x56020d7122a8 in RunImpl<void (ash::DragDropController::\*)(gfx::Point, ui::DropTargetEvent, std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);) >, base::OnceCallback<void (std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);) >, ui::mojom::DragOperation &)>, std::Cr::unique\_ptr<ash::TabDragDropDelegate, std::Cr::default\_delete[ash::TabDragDropDelegate](javascript:void(0);) >, base::ScopedClosureRunner), std::Cr::tuple<base::WeakPtr[ash::DragDropController](javascript:void(0);), gfx::Point, ui::DropTargetEvent, std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);) >, base::OnceCallback<void (std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);) >, ui::mojom::DragOperation &)>, std::Cr::unique\_ptr<ash::TabDragDropDelegate, std::Cr::default\_delete[ash::TabDragDropDelegate](javascript:void(0);) >, base::ScopedClosureRunner>, 0UL, 1UL, 2UL, 3UL, 4UL, 5UL, 6UL> ./../../base/bind\_internal.h:778:12  

#27 0x56020d7122a8 in base::internal::Invoker<base::internal::BindState<void (ash::DragDropController::\*)(gfx::Point, ui::DropTargetEvent, std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);) >, base::OnceCallback<void (std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);) >, ui::mojom::DragOperation&)>, std::Cr::unique\_ptr<ash::TabDragDropDelegate, std::Cr::default\_delete[ash::TabDragDropDelegate](javascript:void(0);) >, base::ScopedClosureRunner), base::WeakPtr[ash::DragDropController](javascript:void(0);), gfx::Point, ui::DropTargetEvent, std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);) >, base::OnceCallback<void (std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);) >, ui::mojom::DragOperation&)>, std::Cr::unique\_ptr<ash::TabDragDropDelegate, std::Cr::default\_delete[ash::TabDragDropDelegate](javascript:void(0);) >, base::ScopedClosureRunner>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/bind\_internal.h:747:12  

#28 0x56020d70f7e6 in Run ./../../base/callback.h:143:12  

#29 0x56020d70f7e6 in DropIfAllowed ./../../ash/drag\_drop/drag\_drop\_controller.cc:87:24  

#30 0x56020d70f7e6 in ash::DragDropController::Drop(aura::Window\*, ui::LocatedEvent const&) ./../../ash/drag\_drop/drag\_drop\_controller.cc:621:3  

#31 0x56020d70c8e3 in ash::DragDropController::OnMouseEvent(ui::MouseEvent\*) ./../../ash/drag\_drop/drag\_drop\_controller.cc:0:7  

#32 0x560209ade689 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:190:12  

#33 0x560209ade3ad in ui::EventDispatcher::DispatchEventToEventHandlers(std::Cr::vector<ui::EventHandler\*, std::Cr::allocator[ui::EventHandler\\*](javascript:void(0);) >\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:177:7  

#34 0x560209adda0f in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:125:3  

#35 0x560209add696 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:83:14  

#36 0x560209add426 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:55:15  

#37 0x56020d013169 in ui::EventProcessor::OnEventFromSource(ui::Event\*) ./../../ui/events/event\_processor.cc:49:17  

#38 0x560209ae1dee in ui::EventSource::DeliverEventToSink(ui::Event\*) ./../../ui/events/event\_source.cc:118:16  

#39 0x560209ae22e6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ./../../ui/events/event\_source.cc:66:14  

#40 0x560209ae0a3b in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ./../../ui/events/event\_rewriter.cc:88:39  

#41 0x5601fd112603 in ui::EventRewriterChromeOS::RewriteMouseButtonEvent(ui::MouseEvent const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ./../../ui/chromeos/events/event\_rewriter\_chromeos.cc:1275:12  

#42 0x5601fd112b43 in ui::EventRewriterChromeOS::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ./../../ui/chromeos/events/event\_rewriter\_chromeos.cc:757:12  

#43 0x560209ae2296 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ./../../ui/events/event\_source.cc:67:32  

#44 0x560209ae0a3b in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ./../../ui/events/event\_rewriter.cc:88:39  

#45 0x56020d71dd20 in ash::KeyboardDrivenEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ./../../ash/events/keyboard\_driven\_event\_rewriter.cc:31:12  

#46 0x560209ae2296 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ./../../ui/events/event\_source.cc:67:32  

#47 0x560209ae0a3b in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ./../../ui/events/event\_rewriter.cc:88:39  

#48 0x56020d719d06 in ash::AccessibilityEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ./../../ash/events/accessibility\_event\_rewriter.cc:0:0  

#49 0x560209ae2296 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ./../../ui/events/event\_source.cc:67:32  

#50 0x560209ae0a3b in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ./../../ui/events/event\_rewriter.cc:88:39  

#51 0x56020d4f137e in ash::AutoclickDragEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ./../../ash/accessibility/autoclick/autoclick\_drag\_event\_rewriter.cc:0:0  

#52 0x560209ae2296 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ./../../ui/events/event\_source.cc:67:32  

#53 0x560209ae0a3b in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ./../../ui/events/event\_rewriter.cc:88:39  

#54 0x56020d4fedea in ash::FullscreenMagnifierController::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ./../../ash/accessibility/magnifier/fullscreen\_magnifier\_controller.cc:0:0  

#55 0x560209ae1a91 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const\*, ui::EventRewriter const\*) ./../../ui/events/event\_source.cc:144:29  

#56 0x56020d754a9f in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event\*) ./../../ui/aura/window\_tree\_host\_platform.cc:229:38  

#57 0x56020d75c044 in ash::AshWindowTreeHostPlatform::DispatchEvent(ui::Event\*) ./../../ash/host/ash\_window\_tree\_host\_platform.cc:207:40  

#58 0x560209af0247 in Run ./../../base/callback.h:143:12  

#59 0x560209af0247 in ui::DispatchEventFromNativeUiEvent(ui::Event\* const&, base::OnceCallback<void (ui::Event\*)>) ./../../ui/events/ozone/events\_ozone.cc:36:25  

#60 0x5601fa240ac1 in ui::X11Window::DispatchUiEvent(ui::Event\*, x11::Event const&) ./../../ui/ozone/platform/x11/x11\_window.cc:1341:3  

#61 0x5601fa240313 in ui::X11Window::DispatchEvent(ui::Event\* const&) ./../../ui/ozone/platform/x11/x11\_window.cc:1294:3  

#62 0x5601fa240dfc in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event\* const&) ./../../ui/ozone/platform/x11/x11\_window.cc:0:0  

#63 0x560209a876a9 in ui::PlatformEventSource::DispatchEvent(ui::Event\*) ./../../ui/events/platform/platform\_event\_source.cc:99:29  

#64 0x56020a1f5bef in ui::X11EventSource::OnEvent(x11::Event const&) ./../../ui/events/platform/x11/x11\_event\_source.cc:287:5  

#65 0x5601f9e5bc35 in x11::Connection::DispatchEvent(x11::Event const&) ./../../ui/gfx/x/connection.cc:457:14  

#66 0x5601f9e5b943 in x11::Connection::ProcessNextEvent() ./../../ui/gfx/x/connection.cc:508:3  

#67 0x5601f9e5b413 in x11::Connection::Dispatch() ./../../ui/gfx/x/connection.cc:0:0  

#68 0x56020a1feb03 in ui::X11EventWatcherFdWatch::OnFileCanReadWithoutBlocking(int) ./../../ui/events/platform/x11/x11\_event\_watcher\_fdwatch.cc:64:15  

#69 0x56020782ccda in base::MessagePumpLibevent::OnLibeventNotification(int, short, void\*) ./../../base/message\_loop/message\_pump\_libevent.cc:0:13  

#70 0x560207b4962b in event\_process\_active ./../../base/third\_party/libevent/event.c:381:4  

#71 0x560207b4962b in event\_base\_loop ./../../base/third\_party/libevent/event.c:521:4  

#72 0x56020782d5f6 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_libevent.cc:204:7  

#73 0x56020772158b in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:542:12  

#74 0x56020765062f in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:141:14  

#75 0x56020d70b079 in ash::DragDropController::StartDragAndDrop(std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);) >, aura::Window\*, aura::Window\*, gfx::Point const&, int, ui::mojom::DragEventSource) ./../../ash/drag\_drop/drag\_drop\_controller.cc:245:16  

#76 0x5601fee38067 in content::WebContentsViewAura::StartDragging(content::DropData const&, blink::DragOperationsMask, gfx::ImageSkia const&, gfx::Vector2d const&, blink::mojom::DragEventSourceInfo const&, content::RenderWidgetHostImpl\*) ./../../content/browser/web\_contents/web\_contents\_view\_aura.cc:1191:15  

#77 0x5601feaa94e0 in content::RenderWidgetHostImpl::StartDragging(mojo::StructPtr[blink::mojom::DragData](javascript:void(0);), blink::DragOperationsMask, SkBitmap const&, gfx::Vector2d const&, mojo::StructPtr[blink::mojom::DragEventSourceInfo](javascript:void(0);)) ./../../content/browser/renderer\_host/render\_widget\_host\_impl.cc:2849:9  

#78 0x5601fbfd3c88 in blink::mojom::FrameWidgetHostStubDispatch::Accept(blink::mojom::FrameWidgetHost\*, mojo::Message\*) ./gen/third\_party/blink/public/mojom/page/widget.mojom.cc:3102:13  

#79 0x56020987904d in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:922:54  

#80 0x56020988c467 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#81 0x56020987c318 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:664:20  

#82 0x560208dc4ea1 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ./../../ipc/ipc\_mojo\_bootstrap.cc:1010:24  

#83 0x560208dbecd4 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind\_internal.h:541:12  

#84 0x560208dbecd4 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind\_internal.h:705:12  

#85 0x560208dbecd4 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), std::Cr::tuple<scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> ./../../base/bind\_internal.h:778:12  

#86 0x560208dbecd4 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/bind\_internal.h:747:12  

#87 0x5602076debc6 in Run ./../../base/callback.h:143:12  

#88 0x5602076debc6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:135:32  

#89 0x56020771fef1 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:424:29)> ./../../base/task/common/task\_annotator.h:74:5  

#90 0x56020771fef1 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:422:21  

#91 0x56020771f2f8 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:300:41  

#92 0x560207720cc1 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#93 0x56020782d539 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_libevent.cc:195:55  

#94 0x56020772158b in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:542:12  

#95 0x56020765062f in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:141:14  

#96 0x5601fde330b2 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1039:18  

#97 0x5601fde3749b in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:157:15  

#98 0x5601fde2d2ba in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:30:28  

#99 0x560207424f2b in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:660:10  

#100 0x560207427a2c in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1167:10  

#101 0x560207426e76 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1039:12  

#102 0x5602074209c6 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:407:36  

#103 0x560207421d32 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:435:10  

#104 0x5601f8e2ee50 in ChromeMain ./../../chrome/app/chrome\_main.cc:177:12  

#105 0x7f3382ba30b2 in \_\_libc\_start\_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16

0x615000103590 is located 400 bytes inside of 504-byte region [0x615000103400,0x6150001035f8)  

freed by thread T0 (chrome) here:  

#0 0x5601f8e2ceed in operator delete(void\*) *asan\_rtl*:3  

#1 0x5601fee33b27 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:51:5  

#2 0x5601fee33b27 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:308:7  

#3 0x5601fee33b27 in content::WebContentsViewAura::~WebContentsViewAura() ./../../content/browser/web\_contents/web\_contents\_view\_aura.cc:703:11  

#4 0x5601fee33daf in content::WebContentsViewAura::~WebContentsViewAura() ./../../content/browser/web\_contents/web\_contents\_view\_aura.cc:695:45  

#5 0x5601fedbd792 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:51:5  

#6 0x5601fedbd792 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:308:7  

#7 0x5601fedbd792 in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:262:19  

#8 0x5601fedbd792 in content::WebContentsImpl::~WebContentsImpl() ./../../content/browser/web\_contents/web\_contents\_impl.cc:1087:1  

#9 0x5601fedbeed1 in content::WebContentsImpl::~WebContentsImpl() ./../../content/browser/web\_contents/web\_contents\_impl.cc:989:37  

#10 0x560213cfc258 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:51:5  

#11 0x560213cfc258 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:308:7  

#12 0x560213cfc258 in TabStripModel::SendDetachWebContentsNotifications(TabStripModel::DetachNotifications\*) ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:569:27  

#13 0x560213d01f5a in TabStripModel::CloseTabs(base::span<content::WebContents\* const, 18446744073709551615ul>, unsigned int) ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:1927:5  

#14 0x560213d02d38 in TabStripModel::CloseWebContentsAt(int, unsigned int) ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:787:10  

#15 0x5601fbf60fb7 in blink::mojom::LocalMainFrameHostStubDispatch::Accept(blink::mojom::LocalMainFrameHost\*, mojo::Message\*) ./gen/third\_party/blink/public/mojom/frame/frame.mojom.cc:0:0  

#16 0x56020987904d in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:922:54  

#17 0x56020988c382 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:48:24  

#18 0x56020987c318 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:664:20  

#19 0x560208dc4ea1 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ./../../ipc/ipc\_mojo\_bootstrap.cc:1010:24  

#20 0x560208dbecd4 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind\_internal.h:541:12  

#21 0x560208dbecd4 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind\_internal.h:705:12  

#22 0x560208dbecd4 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), std::Cr::tuple<scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> ./../../base/bind\_internal.h:778:12  

#23 0x560208dbecd4 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/bind\_internal.h:747:12  

#24 0x5602076debc6 in Run ./../../base/callback.h:143:12  

#25 0x5602076debc6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:135:32  

#26 0x56020771fef1 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:424:29)> ./../../base/task/common/task\_annotator.h:74:5  

#27 0x56020771fef1 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:422:21  

#28 0x56020771f2f8 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:300:41  

#29 0x560207720cc1 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#30 0x56020782d539 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_libevent.cc:195:55  

#31 0x56020772158b in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:542:12  

#32 0x56020765062f in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:141:14  

#33 0x56020d70b079 in ash::DragDropController::StartDragAndDrop(std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);) >, aura::Window\*, aura::Window\*, gfx::Point const&, int, ui::mojom::DragEventSource) ./../../ash/drag\_drop/drag\_drop\_controller.cc:245:16  

#34 0x5601fee38067 in content::WebContentsViewAura::StartDragging(content::DropData const&, blink::DragOperationsMask, gfx::ImageSkia const&, gfx::Vector2d const&, blink::mojom::DragEventSourceInfo const&, content::RenderWidgetHostImpl\*) ./../../content/browser/web\_contents/web\_contents\_view\_aura.cc:1191:15  

#35 0x5601feaa94e0 in content::RenderWidgetHostImpl::StartDragging(mojo::StructPtr[blink::mojom::DragData](javascript:void(0);), blink::DragOperationsMask, SkBitmap const&, gfx::Vector2d const&, mojo::StructPtr[blink::mojom::DragEventSourceInfo](javascript:void(0);)) ./../../content/browser/renderer\_host/render\_widget\_host\_impl.cc:2849:9  

#36 0x5601fbfd3c88 in blink::mojom::FrameWidgetHostStubDispatch::Accept(blink::mojom::FrameWidgetHost\*, mojo::Message\*) ./gen/third\_party/blink/public/mojom/page/widget.mojom.cc:3102:13  

#37 0x56020987904d in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:922:54  

#38 0x56020988c467 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#39 0x56020987c318 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:664:20  

#40 0x560208dc4ea1 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ./../../ipc/ipc\_mojo\_bootstrap.cc:1010:24  

#41 0x560208dbecd4 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind\_internal.h:541:12  

#42 0x560208dbecd4 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind\_internal.h:705:12  

#43 0x560208dbecd4 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), std::Cr::tuple<scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> ./../../base/bind\_internal.h:778:12  

#44 0x560208dbecd4 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/bind\_internal.h:747:12

previously allocated by thread T0 (chrome) here:  

#0 0x5601f8e2c68d in operator new(unsigned long) *asan\_rtl*:3  

#1 0x5601fee36421 in make\_unique<aura::Window, content::WebContentsViewAura \*, aura::client::WindowType> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:717:28  

#2 0x5601fee36421 in content::WebContentsViewAura::CreateAuraWindow(aura::Window\*) ./../../content/browser/web\_contents/web\_contents\_view\_aura.cc:985:7  

#3 0x5601fee36977 in content::WebContentsViewAura::CreateView(aura::Window\*) ./../../content/browser/web\_contents/web\_contents\_view\_aura.cc:1030:3  

#4 0x5601fedd58ca in content::WebContentsImpl::Init(content::WebContents::CreateParams const&, blink::FramePolicy) ./../../content/browser/web\_contents/web\_contents\_impl.cc:3043:10  

#5 0x5601fedb8673 in content::WebContentsImpl::CreateWithOpener(content::WebContents::CreateParams const&, content::RenderFrameHostImpl\*) ./../../content/browser/web\_contents/web\_contents\_impl.cc:1140:17  

#6 0x5601feddd6b0 in content::WebContentsImpl::CreateNewWindow(content::RenderFrameHostImpl\*, content::mojom::CreateNewWindowParams const&, bool, bool, content::SessionStorageNamespace\*) ./../../content/browser/web\_contents/web\_contents\_impl.cc:3934:20  

#7 0x5601fe987245 in content::RenderFrameHostImpl::CreateNewWindow(mojo::StructPtr[content::mojom::CreateNewWindowParams](javascript:void(0);), base::OnceCallback<void (content::mojom::CreateNewWindowStatus, mojo::StructPtr[content::mojom::CreateNewWindowReply](javascript:void(0);))>) ./../../content/browser/renderer\_host/render\_frame\_host\_impl.cc:7087:18  

#8 0x5601fd1e28bd in content::mojom::FrameHostStubDispatch::AcceptWithResponder(content::mojom::FrameHost\*, mojo::Message\*, std::Cr::unique\_ptr<mojo::MessageReceiverWithStatus, std::Cr::default\_delete[mojo::MessageReceiverWithStatus](javascript:void(0);) >) ./gen/content/common/frame.mojom.cc:6302:13  

#9 0x560209878fe1 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:884:56  

#10 0x56020988c382 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:48:24  

#11 0x56020987c318 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:664:20  

#12 0x560208dc47de in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptSyncMessage(unsigned int, unsigned int) ./../../ipc/ipc\_mojo\_bootstrap.cc:1050:24  

#13 0x5602076debc6 in Run ./../../base/callback.h:143:12  

#14 0x5602076debc6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:135:32  

#15 0x56020771fef1 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:424:29)> ./../../base/task/common/task\_annotator.h:74:5  

#16 0x56020771fef1 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:422:21  

#17 0x56020771f2f8 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:300:41  

#18 0x560207720cc1 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#19 0x56020782d539 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_libevent.cc:195:55  

#20 0x56020772158b in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:542:12  

#21 0x56020765062f in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:141:14  

#22 0x56020d70b079 in ash::DragDropController::StartDragAndDrop(std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);) >, aura::Window\*, aura::Window\*, gfx::Point const&, int, ui::mojom::DragEventSource) ./../../ash/drag\_drop/drag\_drop\_controller.cc:245:16  

#23 0x5601fee38067 in content::WebContentsViewAura::StartDragging(content::DropData const&, blink::DragOperationsMask, gfx::ImageSkia const&, gfx::Vector2d const&, blink::mojom::DragEventSourceInfo const&, content::RenderWidgetHostImpl\*) ./../../content/browser/web\_contents/web\_contents\_view\_aura.cc:1191:15  

#24 0x5601feaa94e0 in content::RenderWidgetHostImpl::StartDragging(mojo::StructPtr[blink::mojom::DragData](javascript:void(0);), blink::DragOperationsMask, SkBitmap const&, gfx::Vector2d const&, mojo::StructPtr[blink::mojom::DragEventSourceInfo](javascript:void(0);)) ./../../content/browser/renderer\_host/render\_widget\_host\_impl.cc:2849:9  

#25 0x5601fbfd3c88 in blink::mojom::FrameWidgetHostStubDispatch::Accept(blink::mojom::FrameWidgetHost\*, mojo::Message\*) ./gen/third\_party/blink/public/mojom/page/widget.mojom.cc:3102:13  

#26 0x56020987904d in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:922:54  

#27 0x56020988c467 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#28 0x56020987c318 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:664:20  

#29 0x560208dc4ea1 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ./../../ipc/ipc\_mojo\_bootstrap.cc:1010:24  

#30 0x560208dbecd4 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind\_internal.h:541:12  

#31 0x560208dbecd4 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind\_internal.h:705:12  

#32 0x560208dbecd4 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), std::Cr::tuple<scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> ./../../base/bind\_internal.h:778:12  

#33 0x560208dbecd4 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/bind\_internal.h:747:12  

#34 0x5602076debc6 in Run ./../../base/callback.h:143:12  

#35 0x5602076debc6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:135:32  

#36 0x56020771fef1 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:424:29)> ./../../base/task/common/task\_annotator.h:74:5  

#37 0x56020771fef1 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:422:21

SUMMARY: AddressSanitizer: heap-use-after-free (/home/lbstyle/Desktop/asan-linux-release-1008401/chrome+0x227e8f9b) (BuildId: 52c9b48f17789a8e)  

Shadow bytes around the buggy address:  

0x0c2a80018660: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa  

0x0c2a80018670: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c2a80018680: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2a80018690: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2a800186a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x0c2a800186b0: fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x0c2a800186c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c2a800186d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2a800186e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2a800186f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2a80018700: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

- [screen.webm](attachments/screen.webm) (video/webm, 4.6 MB)
- [screen.webm](attachments/screen.webm) (video/webm, 4.1 MB)
- [cast (1).webm](attachments/cast (1).webm) (video/webm, 6.8 MB)
- [screen.webm](attachments/screen.webm) (video/webm, 2.2 MB)
- [Screen Recording 2022-07-27 at 5.23.16 PM.mov](attachments/Screen Recording 2022-07-27 at 5.23.16 PM.mov) (video/quicktime, 7.1 MB)
- [screen.webm](attachments/screen.webm) (video/webm, 3.9 MB)
- [crash](attachments/crash) (text/plain, 37.8 KB)

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

### ch...@gmail.com (2022-06-16)

Any update on this bug? Thanks!

### sa...@chromium.org (2022-06-16)

[Empty comment from Monorail migration]

### xd...@chromium.org (2022-06-17)

The crash happened when dragging the webui tab. yuhengh@, can you help take a look? thanks!

### jo...@chromium.org (2022-07-08)

UAF in ash gets High until we can convince ourselves this is not easily reachable.

### [Deleted User] (2022-07-09)

yuhengh: Uh oh! This issue still open and hasn't been updated in the last 42 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@gmail.com (2022-07-18)

yuhengh@, Friendly ping :)

### yu...@chromium.org (2022-07-19)

[Empty comment from Monorail migration]

### yu...@chromium.org (2022-07-19)

@chromium.khalil I suspect the following CL should have fixed this issue. Can you verify?
https://chromium-review.googlesource.com/c/chromium/src/+/3747280

Also --top-chrome-touch-ui=enabled  is not official supported and will not run on any devices.
You should try with --force-tablet-mode=touch_view --touch-devices=YOUR_POINTER_DEVICE_FROM_XINPUT to see if it's still reproducible.
otherwise this bug should be Security_Impact=None

### ch...@gmail.com (2022-07-20)

I am still able to repro this with --force-tablet-mode=touch_view flag. 

### yu...@chromium.org (2022-07-20)

[Empty comment from Monorail migration]

### yu...@chromium.org (2022-07-20)

@chromium.khalil I don't think tablet mode supports multiple desktops. Are there any ways to use multiple desktops in tablet mode on a real device? If not I don't think it's a real world issue worth looking into.

### ch...@gmail.com (2022-07-20)

[Comment Deleted]

### ch...@gmail.com (2022-07-20)

[Comment Deleted]

### ch...@gmail.com (2022-07-21)

I'm now able to reproduce this using two chrome windows instead of multiple desktops, I wasn't expecting it would work.

### [Deleted User] (2022-07-27)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@chromium.org (2022-07-27)

Hi, chromium.khalil

I'm not able to reproduce your problem. Could you post your reproduce steps and stack trace? Also make sure your version is >= 106.0.5205 since we did fix an issue recently per https://crbug.com/chromium/1330038#c12.

### yu...@chromium.org (2022-07-27)

[Empty comment from Monorail migration]

### ch...@gmail.com (2022-07-27)

What you see on your screen, you didn't open https://lbstyle.github.io/bin.html in two windows, this requires having two windows to repro the crash.

Test on 106.0.5204.0 (I will verify on 106.0.5205 later today).


=8177==ERROR: AddressSanitizer: heap-use-after-free on address 0x6150000dc710 at pc 0x55e1a66f5af8 bp 0x7ffd608959e0 sp 0x7ffd608959d8
READ of size 8 at 0x6150000dc710 thread T0 (chrome)
==8177==WARNING: invalid path to external symbolizer!
==8177==WARNING: Failed to use and restart external symbolizer!
    #0 0x55e1a66f5af7 in begin ./../../buildtools/third_party/libc++/trunk/include/vector:1372:33
    #1 0x55e1a66f5af7 in begin<std::Cr::vector<base::internal::CheckedObserverAdapter, std::Cr::allocator<base::internal::CheckedObserverAdapter> > &> ./../../base/ranges/ranges.h:44:37
    #2 0x55e1a66f5af7 in begin<std::Cr::vector<base::internal::CheckedObserverAdapter, std::Cr::allocator<base::internal::CheckedObserverAdapter> > &> ./../../base/ranges/ranges.h:105:10
    #3 0x55e1a66f5af7 in find_if<std::Cr::vector<base::internal::CheckedObserverAdapter, std::Cr::allocator<base::internal::CheckedObserverAdapter> > &, (lambda at ../../base/observer_list.h:287:21), base::identity, std::Cr::random_access_iterator_tag> ./../../base/ranges/algorithm.h:483:26
    #4 0x55e1a66f5af7 in base::ObserverList<aura::WindowObserver, true, true, base::internal::CheckedObserverAdapter>::RemoveObserver(aura::WindowObserver const*) ./../../base/observer_list.h:286:21
    #5 0x55e1a76c88fa in ash::TabletModeBrowserWindowDragSessionWindowsHider::~TabletModeBrowserWindowDragSessionWindowsHider() ./../../ash/wm/tablet_mode/tablet_mode_browser_window_drag_session_windows_hider.cc:74:18
    #6 0x55e1a76c8b9d in ash::TabletModeBrowserWindowDragSessionWindowsHider::~TabletModeBrowserWindowDragSessionWindowsHider() ./../../ash/wm/tablet_mode/tablet_mode_browser_window_drag_session_windows_hider.cc:67:55
    #7 0x55e1a6e1482d in operator() ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:48:5
    #8 0x55e1a6e1482d in reset ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:305:7
    #9 0x55e1a6e1482d in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:259:19
    #10 0x55e1a6e1482d in ash::TabDragDropDelegate::~TabDragDropDelegate() ./../../ash/drag_drop/tab_drag_drop_delegate.cc:126:1
    #11 0x55e1a6e14a65 in ash::TabDragDropDelegate::~TabDragDropDelegate() ./../../ash/drag_drop/tab_drag_drop_delegate.cc:114:45
    #12 0x55e1a6e0efc5 in operator() ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:48:5
    #13 0x55e1a6e0efc5 in reset ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:305:7
    #14 0x55e1a6e0efc5 in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:259:19
    #15 0x55e1a6e0efc5 in ash::DragDropController::PerformDrop(gfx::Point, ui::DropTargetEvent, std::Cr::unique_ptr<ui::OSExchangeData, std::Cr::default_delete<ui::OSExchangeData> >, base::OnceCallback<void (std::Cr::unique_ptr<ui::OSExchangeData, std::Cr::default_delete<ui::OSExchangeData> >, ui::mojom::DragOperation&)>, std::Cr::unique_ptr<ash::TabDragDropDelegate, std::Cr::default_delete<ash::TabDragDropDelegate> >, base::ScopedClosureRunner) ./../../ash/drag_drop/drag_drop_controller.cc:816:1
    #16 0x55e1a6e112e2 in void base::internal::FunctorTraits<void (ash::DragDropController::*)(gfx::Point, ui::DropTargetEvent, std::Cr::unique_ptr<ui::OSExchangeData, std::Cr::default_delete<ui::OSExchangeData> >, base::OnceCallback<void (std::Cr::unique_ptr<ui::OSExchangeData, std::Cr::default_delete<ui::OSExchangeData> >, ui::mojom::DragOperation&)>, std::Cr::unique_ptr<ash::TabDragDropDelegate, std::Cr::default_delete<ash::TabDragDropDelegate> >, base::ScopedClosureRunner), void>::Invoke<void (ash::DragDropController::*)(gfx::Point, ui::DropTargetEvent, std::Cr::unique_ptr<ui::OSExchangeData, std::Cr::default_delete<ui::OSExchangeData> >, base::OnceCallback<void (std::Cr::unique_ptr<ui::OSExchangeData, std::Cr::default_delete<ui::OSExchangeData> >, ui::mojom::DragOperation&)>, std::Cr::unique_ptr<ash::TabDragDropDelegate, std::Cr::default_delete<ash::TabDragDropDelegate> >, base::ScopedClosureRunner), base::WeakPtr<ash::DragDropController>, gfx::Point, ui::DropTargetEvent, std::Cr::unique_ptr<ui::OSExchangeData, std::Cr::default_delete<ui::OSExchangeData> >, base::OnceCallback<void (std::Cr::unique_ptr<ui::OSExchangeData, std::Cr::default_delete<ui::OSExchangeData> >, ui::mojom::DragOperation&)>, std::Cr::unique_ptr<ash::TabDragDropDelegate, std::Cr::default_delete<ash::TabDragDropDelegate> >, base::ScopedClosureRunner>(void (ash::DragDropController::*)(gfx::Point, ui::DropTargetEvent, std::Cr::unique_ptr<ui::OSExchangeData, std::Cr::default_delete<ui::OSExchangeData> >, base::OnceCallback<void (std::Cr::unique_ptr<ui::OSExchangeData, std::Cr::default_delete<ui::OSExchangeData> >, ui::mojom::DragOperation&)>, std::Cr::unique_ptr<ash::TabDragDropDelegate, std::Cr::default_delete<ash::TabDragDropDelegate> >, base::ScopedClosureRunner), base::WeakPtr<ash::DragDropController>&&, gfx::Point&&, ui::DropTargetEvent&&, std::Cr::unique_ptr<ui::OSExchangeData, std::Cr::default_delete<ui::OSExchangeData> >&&, base::OnceCallback<void (std::Cr::unique_ptr<ui::OSExchangeData, std::Cr::default_delete<ui::OSExchangeData> >, ui::mojom::DragOperation&)>&&, std::Cr::unique_ptr<ash::TabDragDropDelegate, std::Cr::default_delete<ash::TabDragDropDelegate> >&&, base::ScopedClosureRunner&&) ./../../base/bind_internal.h:580:12
    #17 0x55e1a6e10fe8 in MakeItSo<void (ash::DragDropController::*)(gfx::Point, ui::DropTargetEvent, std::Cr::unique_ptr<ui::OSExchangeData, std::Cr::default_delete<ui::OSExchangeData> >, base::OnceCallback<void (std::Cr::unique_ptr<ui::OSExchangeData, std::Cr::default_delete<ui::OSExchangeData> >, ui::mojom::DragOperation &)>, std::Cr::unique_ptr<ash::TabDragDropDelegate, std::Cr::default_delete<ash::TabDragDropDelegate> >, base::ScopedClosureRunner), base::WeakPtr<ash::DragDropController>, gfx::Point, ui::DropTargetEvent, std::Cr::unique_ptr<ui::OSExchangeData, std::Cr::default_delete<ui::OSExchangeData> >, base::OnceCallback<void (std::Cr::unique_ptr<ui::OSExchangeData, std::Cr::default_delete<ui::OSExchangeData> >, ui::mojom::DragOperation &)>, std::Cr::unique_ptr<ash::TabDragDropDelegate, std::Cr::default_delete<ash::TabDragDropDelegate> >, base::ScopedClosureRunner> ./../../base/bind_internal.h:769:5
    #18 0x55e1a6e10fe8 in RunImpl<void (ash::DragDropController::*)(gfx::Point, ui::DropTargetEvent, std::Cr::unique_ptr<ui::OSExchangeData, std::Cr::default_delete<ui::OSExchangeData> >, base::OnceCallback<void (std::Cr::unique_ptr<ui::OSExchangeData, std::Cr::default_delete<ui::OSExchangeData> >, ui::mojom::DragOperation &)>, std::Cr::unique_ptr<ash::TabDragDropDelegate, std::Cr::default_delete<ash::TabDragDropDelegate> >, base::ScopedClosureRunner), std::Cr::tuple<base::WeakPtr<ash::DragDropController>, gfx::Point, ui::DropTargetEvent, std::Cr::unique_ptr<ui::OSExchangeData, std::Cr::default_delete<ui::OSExchangeData> >, base::OnceCallback<void (std::Cr::unique_ptr<ui::OSExchangeData, std::Cr::default_delete<ui::OSExchangeData> >, ui::mojom::DragOperation &)>, std::Cr::unique_ptr<ash::TabDragDropDelegate, std::Cr::default_delete<ash::TabDragDropDelegate> >, base::ScopedClosureRunner>, 0UL, 1UL, 2UL, 3UL, 4UL, 5UL, 6UL> ./../../base/bind_internal.h:822:12
    #19 0x55e1a6e10fe8 in base::internal::Invoker<base::internal::BindState<void (ash::DragDropController::*)(gfx::Point, ui::DropTargetEvent, std::Cr::unique_ptr<ui::OSExchangeData, std::Cr::default_delete<ui::OSExchangeData> >, base::OnceCallback<void (std::Cr::unique_ptr<ui::OSExchangeData, std::Cr::default_delete<ui::OSExchangeData> >, ui::mojom::DragOperation&)>, std::Cr::unique_ptr<ash::TabDragDropDelegate, std::Cr::default_delete<ash::TabDragDropDelegate> >, base::ScopedClosureRunner), base::WeakPtr<ash::DragDropController>, gfx::Point, ui::DropTargetEvent, std::Cr::unique_ptr<ui::OSExchangeData, std::Cr::default_delete<ui::OSExchangeData> >, base::OnceCallback<void (std::Cr::unique_ptr<ui::OSExchangeData, std::Cr::default_delete<ui::OSExchangeData> >, ui::mojom::DragOperation&)>, std::Cr::unique_ptr<ash::TabDragDropDelegate, std::Cr::default_delete<ash::TabDragDropDelegate> >, base::ScopedClosureRunner>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:791:12
    #20 0x55e1a6e0e43a in Run ./../../base/callback.h:145:12
    #21 0x55e1a6e0e43a in DropIfAllowed ./../../ash/drag_drop/drag_drop_controller.cc:87:24
    #22 0x55e1a6e0e43a in ash::DragDropController::Drop(aura::Window*, ui::LocatedEvent const&) ./../../ash/drag_drop/drag_drop_controller.cc:625:3
    #23 0x55e1a6e0b4a9 in ash::DragDropController::OnMouseEvent(ui::MouseEvent*) ./../../ash/drag_drop/drag_drop_controller.cc:0:7
    #24 0x55e1a341cad9 in ui::EventDispatcher::DispatchEvent(ui::EventHandler*, ui::Event*) ./../../ui/events/event_dispatcher.cc:190:12
    #25 0x55e1a341c809 in ui::EventDispatcher::DispatchEventToEventHandlers(std::Cr::vector<ui::EventHandler*, std::Cr::allocator<ui::EventHandler*> >*, ui::Event*) ./../../ui/events/event_dispatcher.cc:177:7
    #26 0x55e1a341be9f in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ./../../ui/events/event_dispatcher.cc:125:3
    #27 0x55e1a341bb26 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ./../../ui/events/event_dispatcher.cc:83:14
    #28 0x55e1a341b8b6 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ./../../ui/events/event_dispatcher.cc:55:15
    #29 0x55e1a67130b9 in ui::EventProcessor::OnEventFromSource(ui::Event*) ./../../ui/events/event_processor.cc:49:17
    #30 0x55e1a342041e in ui::EventSource::DeliverEventToSink(ui::Event*) ./../../ui/events/event_source.cc:118:16
    #31 0x55e1a3420916 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ./../../ui/events/event_source.cc:66:14
    #32 0x55e1a341f063 in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ./../../ui/events/event_rewriter.cc:88:39
    #33 0x55e1965baf03 in ui::EventRewriterChromeOS::RewriteMouseButtonEvent(ui::MouseEvent const&, base::WeakPtr<ui::EventRewriterContinuation>) ./../../ui/chromeos/events/event_rewriter_chromeos.cc:1276:12
    #34 0x55e1965bb443 in ui::EventRewriterChromeOS::RewriteEvent(ui::Event const&, base::WeakPtr<ui::EventRewriterContinuation>) ./../../ui/chromeos/events/event_rewriter_chromeos.cc:758:12
    #35 0x55e1a34208c6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ./../../ui/events/event_source.cc:67:32
    #36 0x55e1a341f063 in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ./../../ui/events/event_rewriter.cc:88:39
    #37 0x55e1a6e1cb20 in ash::KeyboardDrivenEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr<ui::EventRewriterContinuation>) ./../../ash/events/keyboard_driven_event_rewriter.cc:31:12
    #38 0x55e1a34208c6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ./../../ui/events/event_source.cc:67:32
    #39 0x55e1a341f063 in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ./../../ui/events/event_rewriter.cc:88:39
    #40 0x55e1a6e18d30 in ash::AccessibilityEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr<ui::EventRewriterContinuation>) ./../../ash/events/accessibility_event_rewriter.cc:0:0
    #41 0x55e1a34208c6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ./../../ui/events/event_source.cc:67:32
    #42 0x55e1a341f063 in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ./../../ui/events/event_rewriter.cc:88:39
    #43 0x55e1a6be8f1e in ash::AutoclickDragEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr<ui::EventRewriterContinuation>) ./../../ash/accessibility/autoclick/autoclick_drag_event_rewriter.cc:0:0
    #44 0x55e1a34208c6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ./../../ui/events/event_source.cc:67:32
    #45 0x55e1a341f063 in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ./../../ui/events/event_rewriter.cc:88:39
    #46 0x55e1a6bf6bca in ash::FullscreenMagnifierController::RewriteEvent(ui::Event const&, base::WeakPtr<ui::EventRewriterContinuation>) ./../../ash/accessibility/magnifier/fullscreen_magnifier_controller.cc:0:0
    #47 0x55e1a34200c1 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) ./../../ui/events/event_source.cc:144:29
    #48 0x55e1a6e530f1 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event*) ./../../ui/aura/window_tree_host_platform.cc:229:38
    #49 0x55e1a6e5a5e8 in ash::AshWindowTreeHostPlatform::DispatchEvent(ui::Event*) ./../../ash/host/ash_window_tree_host_platform.cc:207:40
    #50 0x55e1a342ab1c in Run ./../../base/callback.h:145:12
    #51 0x55e1a342ab1c in ui::DispatchEventFromNativeUiEvent(ui::Event* const&, base::OnceCallback<void (ui::Event*)>) ./../../ui/events/ozone/events_ozone.cc:36:25
    #52 0x55e193467a5f in ui::X11Window::DispatchUiEvent(ui::Event*, x11::Event const&) ./../../ui/ozone/platform/x11/x11_window.cc:1362:3
    #53 0x55e1934672b1 in ui::X11Window::DispatchEvent(ui::Event* const&) ./../../ui/ozone/platform/x11/x11_window.cc:1315:3
    #54 0x55e193467d9a in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event* const&) ./../../ui/ozone/platform/x11/x11_window.cc:0:0
    #55 0x55e1a33c4d61 in ui::PlatformEventSource::DispatchEvent(ui::Event*) ./../../ui/events/platform/platform_event_source.cc:99:29
    #56 0x55e1a3b127cf in ui::X11EventSource::OnEvent(x11::Event const&) ./../../ui/events/platform/x11/x11_event_source.cc:287:5
    #57 0x55e1930855dd in x11::Connection::DispatchEvent(x11::Event const&) ./../../ui/gfx/x/connection.cc:457:14
    #58 0x55e1930852eb in x11::Connection::ProcessNextEvent() ./../../ui/gfx/x/connection.cc:508:3
    #59 0x55e193084dbb in x11::Connection::Dispatch() ./../../ui/gfx/x/connection.cc:0:0
    #60 0x55e1a3b1b86b in ui::X11EventWatcherFdWatch::OnFileCanReadWithoutBlocking(int) ./../../ui/events/platform/x11/x11_event_watcher_fdwatch.cc:64:15
    #61 0x55e1a1140f07 in base::MessagePumpLibevent::OnLibeventNotification(int, short, void*) ./../../base/message_loop/message_pump_libevent.cc:0:13
    #62 0x55e1a1472f1b in event_process_active ./../../third_party/libevent/event.c:381:4
    #63 0x55e1a1472f1b in event_base_loop ./../../third_party/libevent/event.c:521:4
    #64 0x55e1a11418c3 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_libevent.cc:316:5
    #65 0x55e1a102f315 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:581:12
    #66 0x55e1a0f7d032 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:141:14
    #67 0x55e1a6e09edc in ash::DragDropController::StartDragAndDrop(std::Cr::unique_ptr<ui::OSExchangeData, std::Cr::default_delete<ui::OSExchangeData> >, aura::Window*, aura::Window*, gfx::Point const&, int, ui::mojom::DragEventSource) ./../../ash/drag_drop/drag_drop_controller.cc:245:16
    #68 0x55e1983921f7 in content::WebContentsViewAura::StartDragging(content::DropData const&, blink::DragOperationsMask, gfx::ImageSkia const&, gfx::Vector2d const&, blink::mojom::DragEventSourceInfo const&, content::RenderWidgetHostImpl*) ./../../content/browser/web_contents/web_contents_view_aura.cc:1192:15
    #69 0x55e198010080 in content::RenderWidgetHostImpl::StartDragging(mojo::StructPtr<blink::mojom::DragData>, blink::DragOperationsMask, SkBitmap const&, gfx::Vector2d const&, mojo::StructPtr<blink::mojom::DragEventSourceInfo>) ./../../content/browser/renderer_host/render_widget_host_impl.cc:2849:9
    #70 0x55e1952c8ce0 in blink::mojom::FrameWidgetHostStubDispatch::Accept(blink::mojom::FrameWidgetHost*, mojo::Message*) ./gen/third_party/blink/public/mojom/page/widget.mojom.cc:3630:13
    #71 0x55e1a31b636d in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:935:54
    #72 0x55e1a31c9b37 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #73 0x55e1a31b962a in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:666:20
    #74 0x55e1a270b9f5 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ./../../ipc/ipc_mojo_bootstrap.cc:1010:24
    #75 0x55e1a2705876 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind_internal.h:580:12
    #76 0x55e1a2705876 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind_internal.h:749:12
    #77 0x55e1a2705876 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::Cr::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> ./../../base/bind_internal.h:822:12
    #78 0x55e1a2705876 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:791:12
    #79 0x55e1a0fe908c in Run ./../../base/callback.h:145:12
    #80 0x55e1a0fe908c in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:135:32
    #81 0x55e1a102d88d in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:430:29)> ./../../base/task/common/task_annotator.h:74:5
    #82 0x55e1a102d88d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:428:21
    #83 0x55e1a102cb62 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:298:41
    #84 0x55e1a102e864 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #85 0x55e1a1141868 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_libevent.cc:294:55
    #86 0x55e1a102f315 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:581:12
    #87 0x55e1a0f7d032 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:141:14
    #88 0x55e1973258ec in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser_main_loop.cc:1042:18
    #89 0x55e19732a67b in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser_main_runner_impl.cc:157:15
    #90 0x55e19731fdfa in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser_main.cc:30:28
    #91 0x55e1a0d40066 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:678:10
    #92 0x55e1a0d426c9 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content_main_runner_impl.cc:1197:10
    #93 0x55e1a0d420f3 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1062:12
    #94 0x55e1a0d3c56b in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:406:36
    #95 0x55e1a0d3cbc1 in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:434:10
    #96 0x55e191fe2bd0 in ChromeMain ./../../chrome/app/chrome_main.cc:182:12
    #97 0x7fcd5aaf80b2 in __libc_start_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16

0x6150000dc710 is located 400 bytes inside of 504-byte region [0x6150000dc580,0x6150000dc778)
freed by thread T0 (chrome) here:
    #0 0x55e191fe0c6d in operator delete(void*) _asan_rtl_:3
    #1 0x55e19838dcb7 in operator() ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:48:5
    #2 0x55e19838dcb7 in reset ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:305:7
    #3 0x55e19838dcb7 in content::WebContentsViewAura::~WebContentsViewAura() ./../../content/browser/web_contents/web_contents_view_aura.cc:704:11
    #4 0x55e19838df3f in content::WebContentsViewAura::~WebContentsViewAura() ./../../content/browser/web_contents/web_contents_view_aura.cc:696:45
    #5 0x55e198318426 in operator() ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:48:5
    #6 0x55e198318426 in reset ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:305:7
    #7 0x55e198318426 in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:259:19
    #8 0x55e198318426 in content::WebContentsImpl::~WebContentsImpl() ./../../content/browser/web_contents/web_contents_impl.cc:1095:1
    #9 0x55e198319b65 in content::WebContentsImpl::~WebContentsImpl() ./../../content/browser/web_contents/web_contents_impl.cc:997:37
    #10 0x55e1ad381479 in operator() ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:48:5
    #11 0x55e1ad381479 in reset ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:305:7
    #12 0x55e1ad381479 in TabStripModel::SendDetachWebContentsNotifications(TabStripModel::DetachNotifications*) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:573:27
    #13 0x55e1ad387429 in TabStripModel::CloseTabs(base::span<content::WebContents* const, 18446744073709551615ul>, unsigned int) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:1881:5
    #14 0x55e1ad387e9a in TabStripModel::CloseWebContentsAt(int, unsigned int) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:750:10
    #15 0x55e1ad2ab193 in chrome::CloseWebContents(Browser*, content::WebContents*, bool) ./../../chrome/browser/ui/browser_tabstrip.cc:97:31
    #16 0x55e19524bd17 in blink::mojom::LocalMainFrameHostStubDispatch::Accept(blink::mojom::LocalMainFrameHost*, mojo::Message*) ./gen/third_party/blink/public/mojom/frame/frame.mojom.cc:0:0
    #17 0x55e1a31b636d in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:935:54
    #18 0x55e1a31c9a52 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:48:24
    #19 0x55e1a31b962a in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:666:20
    #20 0x55e1a270b9f5 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ./../../ipc/ipc_mojo_bootstrap.cc:1010:24
    #21 0x55e1a2705876 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind_internal.h:580:12
    #22 0x55e1a2705876 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind_internal.h:749:12
    #23 0x55e1a2705876 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::Cr::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> ./../../base/bind_internal.h:822:12
    #24 0x55e1a2705876 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:791:12
    #25 0x55e1a0fe908c in Run ./../../base/callback.h:145:12
    #26 0x55e1a0fe908c in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:135:32
    #27 0x55e1a102d88d in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:430:29)> ./../../base/task/common/task_annotator.h:74:5
    #28 0x55e1a102d88d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:428:21
    #29 0x55e1a102cb62 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:298:41
    #30 0x55e1a102e864 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #31 0x55e1a1141868 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_libevent.cc:294:55
    #32 0x55e1a102f315 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:581:12
    #33 0x55e1a0f7d032 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:141:14
    #34 0x55e1a6e09edc in ash::DragDropController::StartDragAndDrop(std::Cr::unique_ptr<ui::OSExchangeData, std::Cr::default_delete<ui::OSExchangeData> >, aura::Window*, aura::Window*, gfx::Point const&, int, ui::mojom::DragEventSource) ./../../ash/drag_drop/drag_drop_controller.cc:245:16
    #35 0x55e1983921f7 in content::WebContentsViewAura::StartDragging(content::DropData const&, blink::DragOperationsMask, gfx::ImageSkia const&, gfx::Vector2d const&, blink::mojom::DragEventSourceInfo const&, content::RenderWidgetHostImpl*) ./../../content/browser/web_contents/web_contents_view_aura.cc:1192:15
    #36 0x55e198010080 in content::RenderWidgetHostImpl::StartDragging(mojo::StructPtr<blink::mojom::DragData>, blink::DragOperationsMask, SkBitmap const&, gfx::Vector2d const&, mojo::StructPtr<blink::mojom::DragEventSourceInfo>) ./../../content/browser/renderer_host/render_widget_host_impl.cc:2849:9
    #37 0x55e1952c8ce0 in blink::mojom::FrameWidgetHostStubDispatch::Accept(blink::mojom::FrameWidgetHost*, mojo::Message*) ./gen/third_party/blink/public/mojom/page/widget.mojom.cc:3630:13
    #38 0x55e1a31b636d in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:935:54
    #39 0x55e1a31c9b37 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #40 0x55e1a31b962a in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:666:20
    #41 0x55e1a270b9f5 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ./../../ipc/ipc_mojo_bootstrap.cc:1010:24

previously allocated by thread T0 (chrome) here:
    #0 0x55e191fe040d in operator new(unsigned long) _asan_rtl_:3
    #1 0x55e1983905b1 in make_unique<aura::Window, content::WebContentsViewAura *, aura::client::WindowType> ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:714:28
    #2 0x55e1983905b1 in content::WebContentsViewAura::CreateAuraWindow(aura::Window*) ./../../content/browser/web_contents/web_contents_view_aura.cc:986:7
    #3 0x55e198390b07 in content::WebContentsViewAura::CreateView(aura::Window*) ./../../content/browser/web_contents/web_contents_view_aura.cc:1031:3
    #4 0x55e19832f9a4 in content::WebContentsImpl::Init(content::WebContents::CreateParams const&, blink::FramePolicy) ./../../content/browser/web_contents/web_contents_impl.cc:3098:10
    #5 0x55e198313353 in content::WebContentsImpl::CreateWithOpener(content::WebContents::CreateParams const&, content::RenderFrameHostImpl*) ./../../content/browser/web_contents/web_contents_impl.cc:1148:17
    #6 0x55e198337a7d in content::WebContentsImpl::CreateNewWindow(content::RenderFrameHostImpl*, content::mojom::CreateNewWindowParams const&, bool, bool, content::SessionStorageNamespace*) ./../../content/browser/web_contents/web_contents_impl.cc:4002:20
    #7 0x55e197eeccd4 in content::RenderFrameHostImpl::CreateNewWindow(mojo::StructPtr<content::mojom::CreateNewWindowParams>, base::OnceCallback<void (content::mojom::CreateNewWindowStatus, mojo::StructPtr<content::mojom::CreateNewWindowReply>)>) ./../../content/browser/renderer_host/render_frame_host_impl.cc:7421:18
    #8 0x55e19668c621 in content::mojom::FrameHostStubDispatch::AcceptWithResponder(content::mojom::FrameHost*, mojo::Message*, std::Cr::unique_ptr<mojo::MessageReceiverWithStatus, std::Cr::default_delete<mojo::MessageReceiverWithStatus> >) ./gen/content/common/frame.mojom.cc:5765:13
    #9 0x55e1a31b6301 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:897:56
    #10 0x55e1a31c9a52 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:48:24
    #11 0x55e1a31b962a in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:666:20
    #12 0x55e1a270b332 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptSyncMessage(unsigned int, unsigned int) ./../../ipc/ipc_mojo_bootstrap.cc:1050:24
    #13 0x55e1a0fe908c in Run ./../../base/callback.h:145:12
    #14 0x55e1a0fe908c in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:135:32
    #15 0x55e1a102d88d in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:430:29)> ./../../base/task/common/task_annotator.h:74:5
    #16 0x55e1a102d88d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:428:21
    #17 0x55e1a102cb62 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:298:41
    #18 0x55e1a102e864 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #19 0x55e1a1141868 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_libevent.cc:294:55
    #20 0x55e1a102f315 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:581:12
    #21 0x55e1a0f7d032 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:141:14
    #22 0x55e1a6e09edc in ash::DragDropController::StartDragAndDrop(std::Cr::unique_ptr<ui::OSExchangeData, std::Cr::default_delete<ui::OSExchangeData> >, aura::Window*, aura::Window*, gfx::Point const&, int, ui::mojom::DragEventSource) ./../../ash/drag_drop/drag_drop_controller.cc:245:16
    #23 0x55e1983921f7 in content::WebContentsViewAura::StartDragging(content::DropData const&, blink::DragOperationsMask, gfx::ImageSkia const&, gfx::Vector2d const&, blink::mojom::DragEventSourceInfo const&, content::RenderWidgetHostImpl*) ./../../content/browser/web_contents/web_contents_view_aura.cc:1192:15
    #24 0x55e198010080 in content::RenderWidgetHostImpl::StartDragging(mojo::StructPtr<blink::mojom::DragData>, blink::DragOperationsMask, SkBitmap const&, gfx::Vector2d const&, mojo::StructPtr<blink::mojom::DragEventSourceInfo>) ./../../content/browser/renderer_host/render_widget_host_impl.cc:2849:9
    #25 0x55e1952c8ce0 in blink::mojom::FrameWidgetHostStubDispatch::Accept(blink::mojom::FrameWidgetHost*, mojo::Message*) ./gen/third_party/blink/public/mojom/page/widget.mojom.cc:3630:13
    #26 0x55e1a31b636d in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:935:54
    #27 0x55e1a31c9b37 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #28 0x55e1a31b962a in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:666:20
    #29 0x55e1a270b9f5 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ./../../ipc/ipc_mojo_bootstrap.cc:1010:24
    #30 0x55e1a2705876 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind_internal.h:580:12
    #31 0x55e1a2705876 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind_internal.h:749:12
    #32 0x55e1a2705876 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::Cr::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> ./../../base/bind_internal.h:822:12
    #33 0x55e1a2705876 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:791:12
    #34 0x55e1a0fe908c in Run ./../../base/callback.h:145:12
    #35 0x55e1a0fe908c in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:135:32
    #36 0x55e1a102d88d in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:430:29)> ./../../base/task/common/task_annotator.h:74:5
    #37 0x55e1a102d88d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:428:21

SUMMARY: AddressSanitizer: heap-use-after-free (/home/lbstyle/Desktop/asan-linux-release-1028528/chrome+0x219ccaf7) (BuildId: ccbf71079052b598)
Shadow bytes around the buggy address:
  0x0c2a80013890: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x0c2a800138a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2a800138b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a800138c0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a800138d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0c2a800138e0: fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fa
  0x0c2a800138f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2a80013900: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a80013910: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a80013920: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a80013930: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa
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


### yu...@chromium.org (2022-07-28)

Ok, I think I'm able to reproduce the problem. However looking at the stack track it's related to mouse events(...OnMouseEvent), which isn't supported by tablet mode on Chrome OS. Are you able to reproduce the problem only using touch event? You can simulate touch event using mouse by passing the following command line arguments.
--force-tablet-mode=touch_view --touch-devices=YOUR_POINTER_DEVICE_FROM_XINPUT to see if it's still reproducible.

Here's a video example of simulating touch events with mouse. Notice when your mouse hover over the window the mouse disappear, which is equivalent to tapping on a tablet enabled ChromeOS device.



### ch...@gmail.com (2022-07-28)

Unfortunately, my device is non touchscreen.

### yu...@chromium.org (2022-07-28)

My device is not as well, but you can simulate touch event using mouse by passing the right command line flag mentioned in https://crbug.com/chromium/1330038#c23.

### ch...@gmail.com (2022-07-28)

Sorry for the misunderstanding. I am able to repro this using touch event.

1. Open https://lbstyle.github.io/bin.html >> Click on the button 
2. Open https://lbstyle.github.io/bin.html in incognito window >> Click on the button and wait 
3. Drag and drop any tab 

### ch...@gmail.com (2022-07-28)

(Incognito window is not necessary to repro this, you can just open another window via chrome menu and not through keyboard shortcut).

### yu...@chromium.org (2022-07-28)

Thanks for the videos, I will take a look shortly.

### gi...@appspot.gserviceaccount.com (2022-08-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e75368a53b794eb192c09bfcbf4f71f275b7f173

commit e75368a53b794eb192c09bfcbf4f71f275b7f173
Author: Yuheng Huang <yuhengh@chromium.org>
Date: Tue Aug 02 16:37:33 2022

WebUI tab strip: fix uaf in TabletModeBrowserWindowDragSessionWindowsHider

This CL fixes an UAF issue where a new window is created and shown during drag session. According the API definition, the window object in aura::WindowObserver::OnWindowVisibilityChanged is not necessarily the one that's being observed. The CL makes sure it does not add them to the observer map when the window is not observed.

Bug: 1330038
Change-Id: I849863db2fe5fc8fd268081af070c6a651658fca
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3800400
Reviewed-by: Mitsuru Oshima <oshima@chromium.org>
Commit-Queue: Yuheng Huang <yuhengh@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1030603}

[modify] https://crrev.com/e75368a53b794eb192c09bfcbf4f71f275b7f173/ash/BUILD.gn
[modify] https://crrev.com/e75368a53b794eb192c09bfcbf4f71f275b7f173/ash/wm/tablet_mode/tablet_mode_browser_window_drag_session_windows_hider.cc
[add] https://crrev.com/e75368a53b794eb192c09bfcbf4f71f275b7f173/ash/wm/tablet_mode/tablet_mode_browser_window_drag_session_windows_hider_unittest.cc
[modify] https://crrev.com/e75368a53b794eb192c09bfcbf4f71f275b7f173/ash/wm/tablet_mode/tablet_mode_browser_window_drag_session_windows_hider.h


### ch...@gmail.com (2022-08-03)

I just virified this bug on linux-release-chromeos_asan-linux-release-1030692. seems like fixed.

Thanks for the fix! 

### yu...@chromium.org (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-11)

Congratulations, Khalil! The VRP Panel has decided to award you $3,000 for this report. The reward amount was decided on as this issue is moderately mitigated by not being remote exploitable and the user interaction required. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### is...@google.com (2023-05-24)

This issue was migrated from crbug.com/chromium/1330038?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059784)*
