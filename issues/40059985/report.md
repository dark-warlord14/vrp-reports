# Security: heap-use-after-free ash/drag_drop/drag_drop_tracker.cc:111:1 (chromeOS)

| Field | Value |
|-------|-------|
| **Issue ID** | [40059985](https://issues.chromium.org/issues/40059985) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Shell>UIFoundations |
| **Platforms** | ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2022-06-16 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

This bug is happening when dual display extended mode + tablet mode enabled. No crash happen with mirror mode.

when perform ash::DragDropTracker::~DragDropTracker()[1] is holding aura::Window\*. When user holds tabstrip from top chrome then the aura::Window\* get deleted when user open file manager(CreateWebDialogWidget). The aura::Window\* is being recall again to show file manager --> heap UAF.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:ash/drag_drop/drag_drop_tracker.cc;l=103-111?q=ash%2Fdrag_drop%2Fdrag_drop_tracker.cc&ss=chromium%2Fchromium%2Fsrc>

**VERSION**  

Chrome Version: Chromium 105.0.5124.0 dev + sabtle  

Operating System: linux-chromeOS

**REPRODUCTION CASE**  

\*Enable dual display + extended mode  

(1) Open browser and add new tab page  

(2) Drag out one tab and hold then open file manager (CTRL + O)

\*\* will provide html file later with less user interaction \*\*

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

==369827==ERROR: AddressSanitizer: heap-use-after-free on address 0x6150000a21f8 at pc 0x7fc92dd73419 bp 0x7ffcc7018c80 sp 0x7ffcc7018c78  

READ of size 8 at 0x6150000a21f8 thread T0 (chrome)  

SCARINESS: 51 (8-byte-read-heap-use-after-free)  

#0 0x7fc92dd73418 in operator bool base/memory/raw\_ptr.h:806:59  

#1 0x7fc92dd73418 in IsRootWindow ui/aura/window.h:216:40  

#2 0x7fc92dd73418 in GetRootWindow ui/aura/window.cc:340:10  

#3 0x7fc92dd73418 in aura::Window::GetRootWindow() ui/aura/window.cc:336:41  

#4 0x7fc92dd8e9a0 in aura::WindowEventDispatcher::UpdateCapture(aura::Window\*, aura::Window\*) ui/aura/window\_event\_dispatcher.cc:426:35  

#5 0x7fc92ce7752e in wm::CaptureController::SetCapture(aura::Window\*) ui/wm/core/capture\_controller.cc:85:16  

#6 0x7fc92dd7d7d1 in aura::Window::NotifyWindowVisibilityChangedAtReceiver(aura::Window\*, bool) ui/aura/window.cc:1215:14  

#7 0x7fc92dd7d2a8 in aura::Window::NotifyWindowVisibilityChangedDown(aura::Window\*, bool) ui/aura/window.cc:1221:8  

#8 0x7fc92dd7b603 in aura::Window::NotifyWindowVisibilityChanged(aura::Window\*, bool) ui/aura/window.cc:1202:8  

#9 0x7fc92dd73a09 in aura::Window::SetVisibleInternal(bool) ui/aura/window.cc:1018:3  

#10 0x7fc92d46bc6b in views::NativeWidgetAura::Show(ui::WindowShowState, gfx::Rect const&) ui/views/widget/native\_widget\_aura.cc:615:12  

#11 0x7fc92d40a738 in views::Widget::Show() ui/views/widget/widget.cc:726:23  

#12 0x55f933db90c8 in CreateWebDialogWidget chrome/browser/ui/views/chrome\_web\_dialog\_view.cc:37:13  

#13 0x55f933db90c8 in chrome::ShowWebDialogWithParams(aura::Window\*, content::BrowserContext\*, ui::WebDialogDelegate\*, absl::optional[views::Widget::InitParams](javascript:void(0);), bool) chrome/browser/ui/views/chrome\_web\_dialog\_view.cc:76:7  

#14 0x55f933b7a83c in chromeos::SystemWebDialogDelegate::ShowSystemDialogForBrowserContext(content::BrowserContext\*, aura::Window\*) chrome/browser/ui/webui/chromeos/system\_web\_dialog\_delegate.cc:239:20  

#15 0x55f9339ed852 in SelectFileDialogExtension::SelectFileWithFileManagerParams(ui::SelectFileDialog::Type, std::Cr::basic\_string<char16\_t, std::Cr::char\_traits<char16\_t>, std::Cr::allocator<char16\_t>> const&, base::FilePath const&, ui::SelectFileDialog::FileTypeInfo const\*, int, void\*, SelectFileDialogExtension::Owner const&, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const&, bool, bool) chrome/browser/ui/views/select\_file\_dialog\_extension.cc:520:22  

#16 0x55f9339eee0e in SelectFileDialogExtension::SelectFileImpl(ui::SelectFileDialog::Type, std::Cr::basic\_string<char16\_t, std::Cr::char\_traits<char16\_t>, std::Cr::allocator<char16\_t>> const&, base::FilePath const&, ui::SelectFileDialog::FileTypeInfo const\*, int, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const&, aura::Window\*, void\*) chrome/browser/ui/views/select\_file\_dialog\_extension.cc:571:3  

#17 0x7fc91309b1c8 in ui::SelectFileDialog::SelectFile(ui::SelectFileDialog::Type, std::Cr::basic\_string<char16\_t, std::Cr::char\_traits<char16\_t>, std::Cr::allocator<char16\_t>> const&, base::FilePath const&, ui::SelectFileDialog::FileTypeInfo const\*, int, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const&, aura::Window\*, void\*) ui/shell\_dialogs/select\_file\_dialog.cc:124:3  

#18 0x55f93321ccfa in Browser::OpenFile() chrome/browser/ui/browser.cc:1056:24  

#19 0x55f9332331ff in chrome::BrowserCommandController::ExecuteCommandWithDisposition(int, WindowOpenDisposition, base::TimeTicks) chrome/browser/ui/browser\_command\_controller.cc:734:17  

#20 0x55f933e5ab26 in BrowserView::AcceleratorPressed(ui::Accelerator const&) chrome/browser/ui/views/frame/browser\_view.cc:3781:10  

#21 0x7fc92f41408e in TryProcess ui/base/accelerators/accelerator\_manager.cc:153:17  

#22 0x7fc92f41408e in ui::AcceleratorManager::Process(ui::Accelerator const&) ui/base/accelerators/accelerator\_manager.cc:83:27  

#23 0x7fc92d35ad3d in views::FocusManager::ProcessAccelerator(ui::Accelerator const&) ui/views/focus/focus\_manager.cc:537:28  

#24 0x7fc92d359929 in views::FocusManager::OnKeyEvent(ui::KeyEvent const&) ui/views/focus/focus\_manager.cc:114:7  

#25 0x7fc92d4672ba in views::FocusManagerEventHandler::OnKeyEvent(ui::KeyEvent\*) ui/views/widget/focus\_manager\_event\_handler.cc:26:36  

#26 0x7fc92df2bf07 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ui/events/event\_dispatcher.cc:190:12  

#27 0x7fc92df2bc2b in ui::EventDispatcher::DispatchEventToEventHandlers(std::Cr::vector<ui::EventHandler\*, std::Cr::allocator[ui::EventHandler\\*](javascript:void(0);)>\*, ui::Event\*) ui/events/event\_dispatcher.cc:177:7  

#28 0x7fc92df2b22f in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:125:3  

#29 0x7fc92df2aec9 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:83:14  

#30 0x7fc92df2aca4 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:55:15  

#31 0x7fc92df2e2d7 in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:49:17  

#32 0x7fc92ddaebae in aura::WindowTreeHost::DispatchKeyEventPostIME(ui::KeyEvent\*) ui/aura/window\_tree\_host.cc:377:23  

#33 0x7fc92dce38b7 in ui::InputMethodBase::DispatchKeyEventPostIME(ui::KeyEvent\*) const ui/base/ime/input\_method\_base.cc:140:33  

#34 0x7fc91253a677 in ui::InputMethodAsh::ProcessUnfilteredKeyPressEvent(ui::KeyEvent\*) ui/base/ime/ash/input\_method\_ash.cc:614:38  

#35 0x7fc912539e94 in ui::InputMethodAsh::DispatchKeyEvent(ui::KeyEvent\*) ui/base/ime/ash/input\_method\_ash.cc:139:14  

#36 0x7fc92dd92067 in aura::WindowEventDispatcher::PreDispatchKeyEvent(aura::Window\*, ui::KeyEvent\*) ui/aura/window\_event\_dispatcher.cc:1080:54  

#37 0x7fc92dd90a0e in aura::WindowEventDispatcher::PreDispatchEvent(ui::EventTarget\*, ui::Event\*) ui/aura/window\_event\_dispatcher.cc:568:15  

#38 0x7fc92df2ac54 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:51:34  

#39 0x7fc92df2e2d7 in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:49:17  

#40 0x7fc92df30ac4 in ui::EventSource::DeliverEventToSink(ui::Event\*) ui/events/event\_source.cc:118:16  

#41 0x7fc92df30fc4 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:66:14  

#42 0x7fc92df2f681 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#43 0x7fc92afa4140 in ui::EventRewriterChromeOS::RewriteKeyEventInContext(ui::KeyEvent const&, std::Cr::unique\_ptr<ui::Event, std::Cr::default\_delete[ui::Event](javascript:void(0);)>, ui::EventRewriteStatus, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ui/chromeos/events/event\_rewriter\_chromeos.cc  

#44 0x7fc92afa2267 in ui::EventRewriterChromeOS::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ui/chromeos/events/event\_rewriter\_chromeos.cc:752:12  

#45 0x7fc92df30f74 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#46 0x7fc92df2f681 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#47 0x7fc92a0f615c in ash::KeyboardDrivenEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/events/keyboard\_driven\_event\_rewriter.cc:31:12  

#48 0x7fc92df30f74 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#49 0x7fc92df2f681 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#50 0x7fc92a0f1fde in ash::AccessibilityEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/events/accessibility\_event\_rewriter.cc  

#51 0x7fc92df30f74 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#52 0x7fc92df2f681 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#53 0x7fc929ea1a3e in ash::AutoclickDragEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/accessibility/autoclick/autoclick\_drag\_event\_rewriter.cc  

#54 0x7fc92df30f74 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#55 0x7fc92df2f681 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#56 0x7fc929ec433a in ash::FullscreenMagnifierController::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/accessibility/magnifier/fullscreen\_magnifier\_controller.cc  

#57 0x7fc92df30767 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const\*, ui::EventRewriter const\*) ui/events/event\_source.cc:144:29  

#58 0x7fc92ddb6e07 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event\*) ui/aura/window\_tree\_host\_platform.cc:229:38  

#59 0x7fc92a13fffe in ash::AshWindowTreeHostPlatform::DispatchEvent(ui::Event\*) ash/host/ash\_window\_tree\_host\_platform.cc:207:40  

#60 0x7fc92df412ff in Run base/callback.h:143:12  

#61 0x7fc92df412ff in ui::DispatchEventFromNativeUiEvent(ui::Event\* const&, base::OnceCallback<void (ui::Event\*)>) ui/events/ozone/events\_ozone.cc:28:25  

#62 0x7fc92d8b8a7b in ui::X11Window::DispatchUiEvent(ui::Event\*, x11::Event const&) ui/ozone/platform/x11/x11\_window.cc:1359:3  

#63 0x7fc92d8b82cd in ui::X11Window::DispatchEvent(ui::Event\* const&) ui/ozone/platform/x11/x11\_window.cc:1312:3  

#64 0x7fc92d8b8db6 in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event\* const&) ui/ozone/platform/x11/x11\_window.cc  

#65 0x7fc939a821b3 in ui::PlatformEventSource::DispatchEvent(ui::Event\*) ui/events/platform/platform\_event\_source.cc:99:29  

#66 0x7fc8e405e11f in ui::X11EventSource::OnEvent(x11::Event const&) ui/events/platform/x11/x11\_event\_source.cc:287:5  

#67 0x7fc8e3d220b1 in x11::Connection::DispatchEvent(x11::Event const&) ui/gfx/x/connection.cc:457:14  

#68 0x7fc8e3d21dbf in x11::Connection::ProcessNextEvent() ui/gfx/x/connection.cc:508:3  

#69 0x7fc8e3d219c7 in x11::Connection::Dispatch() ui/gfx/x/connection.cc  

#70 0x7fc8e40685d3 in ui::X11EventWatcherFdWatch::OnFileCanReadWithoutBlocking(int) ui/events/platform/x11/x11\_event\_watcher\_fdwatch.cc:64:15  

#71 0x7fc93e8cb29a in base::MessagePumpLibevent::OnLibeventNotification(int, short, void\*) base/message\_loop/message\_pump\_libevent.cc  

#72 0x7fc93e9cb75b in event\_process\_active base/third\_party/libevent/event.c:381:4  

#73 0x7fc93e9cb75b in event\_base\_loop base/third\_party/libevent/event.c:521:4  

#74 0x7fc93e8cbbb6 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_libevent.cc:204:7  

#75 0x7fc93e79fb20 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:535:12  

#76 0x7fc93e6a5eff in base::RunLoop::Run(base::Location const&) base/run\_loop.cc:141:14  

#77 0x7fc92a0e1d33 in ash::DragDropController::StartDragAndDrop(std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);)>, aura::Window\*, aura::Window\*, gfx::Point const&, int, ui::mojom::DragEventSource) ash/drag\_drop/drag\_drop\_controller.cc:245:16  

#78 0x7fc920072ee5 in content::WebContentsViewAura::StartDragging(content::DropData const&, blink::DragOperationsMask, gfx::ImageSkia const&, gfx::Vector2d const&, blink::mojom::DragEventSourceInfo const&, content::RenderWidgetHostImpl\*) content/browser/web\_contents/web\_contents\_view\_aura.cc:1193:15  

#79 0x7fc91fcc9f5e in content::RenderWidgetHostImpl::StartDragging(mojo::StructPtr[blink::mojom::DragData](javascript:void(0);), blink::DragOperationsMask, SkBitmap const&, gfx::Vector2d const&, mojo::StructPtr[blink::mojom::DragEventSourceInfo](javascript:void(0);)) content/browser/renderer\_host/render\_widget\_host\_impl.cc:2849:9  

#80 0x7fc93103b6fc in blink::mojom::FrameWidgetHostStubDispatch::Accept(blink::mojom::FrameWidgetHost\*, mojo::Message\*) gen/third\_party/blink/public/mojom/page/widget.mojom.cc:3102:13  

#81 0x7fc93be0e9f5 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:922:54  

#82 0x7fc93be1da5f in mojo::MessageDispatcher::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#83 0x7fc93be11c64 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:664:20  

#84 0x7fc939a607af in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ipc/ipc\_mojo\_bootstrap.cc:1010:24  

#85 0x7fc939a5a4e2 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind\_internal.h:543:12  

#86 0x7fc939a5a4e2 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind\_internal.h:707:12  

#87 0x7fc939a5a4e2 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), std::Cr::tuple<scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> base/bind\_internal.h:780:12  

#88 0x7fc939a5a4e2 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*) base/bind\_internal.h:749:12  

#89 0x7fc93e754f76 in Run base/callback.h:143:12  

#90 0x7fc93e754f76 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task\_annotator.cc:135:32  

#91 0x7fc93e79e531 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:410:29)> base/task/common/task\_annotator.h:74:5  

#92 0x7fc93e79e531 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:408:21  

#93 0x7fc93e79d938 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:286:41  

#94 0x7fc93e79f301 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc  

#95 0x7fc93e8cbaf9 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_libevent.cc:195:55  

#96 0x7fc93e79fb20 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:535:12  

#97 0x7fc93e6a5eff in base::RunLoop::Run(base::Location const&) base/run\_loop.cc:141:14  

#98 0x7fc91eff0630 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser\_main\_loop.cc:1039:18  

#99 0x7fc91eff4eeb in content::BrowserMainRunnerImpl::Run() content/browser/browser\_main\_runner\_impl.cc:157:15  

#100 0x7fc91efeac9a in content::BrowserMain(content::MainFunctionParams) content/browser/browser\_main.cc:30:28  

#101 0x7fc920f3c8f6 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:678:10  

#102 0x7fc920f3f5b5 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content\_main\_runner\_impl.cc:1188:10  

#103 0x7fc920f3e9f9 in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner\_impl.cc:1059:12  

#104 0x7fc920f38cf1 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) content/app/content\_main.cc:407:36  

#105 0x7fc920f39251 in content::ContentMain(content::ContentMainParams) content/app/content\_main.cc:435:10  

#106 0x55f928a2bd10 in ChromeMain chrome/app/chrome\_main.cc:189:12  

#107 0x7fc8e5648082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

0x6150000a21f8 is located 248 bytes inside of 504-byte region [0x6150000a2100,0x6150000a22f8)  

freed by thread T0 (chrome) here:  

#0 0x55f928a29dad in operator delete(void\*) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:152:3  

#1 0x7fc92a0ea0b3 in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:51:5  

#2 0x7fc92a0ea0b3 in reset buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:308:7  

#3 0x7fc92a0ea0b3 in ~unique\_ptr buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:262:19  

#4 0x7fc92a0ea0b3 in ash::DragDropTracker::~DragDropTracker() ash/drag\_drop/drag\_drop\_tracker.cc:111:1  

#5 0x7fc92a0e011a in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:51:5  

#6 0x7fc92a0e011a in std::Cr::unique\_ptr<ash::DragDropTracker, std::Cr::default\_delete[ash::DragDropTracker](javascript:void(0);)>::reset(ash::DragDropTracker\*) buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:308:7  

#7 0x7fc92a0edc69 in ash::TabDragDropDelegate::~TabDragDropDelegate() ash/drag\_drop/tab\_drag\_drop\_delegate.cc:114:45  

#8 0x7fc92a0e0a52 in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:51:5  

#9 0x7fc92a0e0a52 in reset buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:308:7  

#10 0x7fc92a0e0a52 in ash::DragDropController::Cleanup() ash/drag\_drop/drag\_drop\_controller.cc:769:27  

#11 0x7fc92a0e7d9a in ash::DragDropController::DoDragCancel(base::TimeDelta) ash/drag\_drop/drag\_drop\_controller.cc:697:3  

#12 0x7fc92dd8ec43 in aura::WindowEventDispatcher::UpdateCapture(aura::Window\*, aura::Window\*) ui/aura/window\_event\_dispatcher.cc:438:32  

#13 0x7fc92ce7752e in wm::CaptureController::SetCapture(aura::Window\*) ui/wm/core/capture\_controller.cc:85:16  

#14 0x7fc92dd7d7d1 in aura::Window::NotifyWindowVisibilityChangedAtReceiver(aura::Window\*, bool) ui/aura/window.cc:1215:14  

#15 0x7fc92dd7d2a8 in aura::Window::NotifyWindowVisibilityChangedDown(aura::Window\*, bool) ui/aura/window.cc:1221:8  

#16 0x7fc92dd7b603 in aura::Window::NotifyWindowVisibilityChanged(aura::Window\*, bool) ui/aura/window.cc:1202:8  

#17 0x7fc92dd73a09 in aura::Window::SetVisibleInternal(bool) ui/aura/window.cc:1018:3  

#18 0x7fc92d46bc6b in views::NativeWidgetAura::Show(ui::WindowShowState, gfx::Rect const&) ui/views/widget/native\_widget\_aura.cc:615:12  

#19 0x7fc92d40a738 in views::Widget::Show() ui/views/widget/widget.cc:726:23  

#20 0x55f933db90c8 in CreateWebDialogWidget chrome/browser/ui/views/chrome\_web\_dialog\_view.cc:37:13  

#21 0x55f933db90c8 in chrome::ShowWebDialogWithParams(aura::Window\*, content::BrowserContext\*, ui::WebDialogDelegate\*, absl::optional[views::Widget::InitParams](javascript:void(0);), bool) chrome/browser/ui/views/chrome\_web\_dialog\_view.cc:76:7  

#22 0x55f933b7a83c in chromeos::SystemWebDialogDelegate::ShowSystemDialogForBrowserContext(content::BrowserContext\*, aura::Window\*) chrome/browser/ui/webui/chromeos/system\_web\_dialog\_delegate.cc:239:20  

#23 0x55f9339ed852 in SelectFileDialogExtension::SelectFileWithFileManagerParams(ui::SelectFileDialog::Type, std::Cr::basic\_string<char16\_t, std::Cr::char\_traits<char16\_t>, std::Cr::allocator<char16\_t>> const&, base::FilePath const&, ui::SelectFileDialog::FileTypeInfo const\*, int, void\*, SelectFileDialogExtension::Owner const&, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const&, bool, bool) chrome/browser/ui/views/select\_file\_dialog\_extension.cc:520:22  

#24 0x55f9339eee0e in SelectFileDialogExtension::SelectFileImpl(ui::SelectFileDialog::Type, std::Cr::basic\_string<char16\_t, std::Cr::char\_traits<char16\_t>, std::Cr::allocator<char16\_t>> const&, base::FilePath const&, ui::SelectFileDialog::FileTypeInfo const\*, int, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const&, aura::Window\*, void\*) chrome/browser/ui/views/select\_file\_dialog\_extension.cc:571:3  

#25 0x7fc91309b1c8 in ui::SelectFileDialog::SelectFile(ui::SelectFileDialog::Type, std::Cr::basic\_string<char16\_t, std::Cr::char\_traits<char16\_t>, std::Cr::allocator<char16\_t>> const&, base::FilePath const&, ui::SelectFileDialog::FileTypeInfo const\*, int, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const&, aura::Window\*, void\*) ui/shell\_dialogs/select\_file\_dialog.cc:124:3  

#26 0x55f93321ccfa in Browser::OpenFile() chrome/browser/ui/browser.cc:1056:24  

#27 0x55f9332331ff in chrome::BrowserCommandController::ExecuteCommandWithDisposition(int, WindowOpenDisposition, base::TimeTicks) chrome/browser/ui/browser\_command\_controller.cc:734:17  

#28 0x55f933e5ab26 in BrowserView::AcceleratorPressed(ui::Accelerator const&) chrome/browser/ui/views/frame/browser\_view.cc:3781:10  

#29 0x7fc92f41408e in TryProcess ui/base/accelerators/accelerator\_manager.cc:153:17  

#30 0x7fc92f41408e in ui::AcceleratorManager::Process(ui::Accelerator const&) ui/base/accelerators/accelerator\_manager.cc:83:27  

#31 0x7fc92d35ad3d in views::FocusManager::ProcessAccelerator(ui::Accelerator const&) ui/views/focus/focus\_manager.cc:537:28  

#32 0x7fc92d359929 in views::FocusManager::OnKeyEvent(ui::KeyEvent const&) ui/views/focus/focus\_manager.cc:114:7  

#33 0x7fc92d4672ba in views::FocusManagerEventHandler::OnKeyEvent(ui::KeyEvent\*) ui/views/widget/focus\_manager\_event\_handler.cc:26:36  

#34 0x7fc92df2bf07 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ui/events/event\_dispatcher.cc:190:12  

#35 0x7fc92df2bc2b in ui::EventDispatcher::DispatchEventToEventHandlers(std::Cr::vector<ui::EventHandler\*, std::Cr::allocator[ui::EventHandler\\*](javascript:void(0);)>\*, ui::Event\*) ui/events/event\_dispatcher.cc:177:7  

#36 0x7fc92df2b22f in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:125:3  

#37 0x7fc92df2aec9 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:83:14

previously allocated by thread T0 (chrome) here:  

#0 0x55f928a2954d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:95:3  

#1 0x7fc92a0e9ed8 in make\_unique<aura::Window, aura::WindowDelegate \*&> buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:717:28  

#2 0x7fc92a0e9ed8 in CreateCaptureWindow ash/drag\_drop/drag\_drop\_tracker.cc:88:17  

#3 0x7fc92a0e9ed8 in ash::DragDropTracker::DragDropTracker(aura::Window\*, base::RepeatingCallback<void ()>) ash/drag\_drop/drag\_drop\_tracker.cc:107:11  

#4 0x7fc92a0dfc24 in ash::DragDropCaptureDelegate::TakeCapture(aura::Window\*, aura::Window\*, base::RepeatingCallback<void ()>, ui::TransferTouchesBehavior) ash/drag\_drop/drag\_drop\_capture\_delegate.cc:52:32  

#5 0x7fc92a0e1a02 in ash::DragDropController::StartDragAndDrop(std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);)>, aura::Window\*, aura::Window\*, gfx::Point const&, int, ui::mojom::DragEventSource) ash/drag\_drop/drag\_drop\_controller.cc:212:36  

#6 0x7fc920072ee5 in content::WebContentsViewAura::StartDragging(content::DropData const&, blink::DragOperationsMask, gfx::ImageSkia const&, gfx::Vector2d const&, blink::mojom::DragEventSourceInfo const&, content::RenderWidgetHostImpl\*) content/browser/web\_contents/web\_contents\_view\_aura.cc:1193:15  

#7 0x7fc91fcc9f5e in content::RenderWidgetHostImpl::StartDragging(mojo::StructPtr[blink::mojom::DragData](javascript:void(0);), blink::DragOperationsMask, SkBitmap const&, gfx::Vector2d const&, mojo::StructPtr[blink::mojom::DragEventSourceInfo](javascript:void(0);)) content/browser/renderer\_host/render\_widget\_host\_impl.cc:2849:9  

#8 0x7fc93103b6fc in blink::mojom::FrameWidgetHostStubDispatch::Accept(blink::mojom::FrameWidgetHost\*, mojo::Message\*) gen/third\_party/blink/public/mojom/page/widget.mojom.cc:3102:13  

#9 0x7fc93be0e9f5 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:922:54  

#10 0x7fc93be1da5f in mojo::MessageDispatcher::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#11 0x7fc93be11c64 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:664:20  

#12 0x7fc939a607af in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ipc/ipc\_mojo\_bootstrap.cc:1010:24  

#13 0x7fc939a5a4e2 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind\_internal.h:543:12  

#14 0x7fc939a5a4e2 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind\_internal.h:707:12  

#15 0x7fc939a5a4e2 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), std::Cr::tuple<scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> base/bind\_internal.h:780:12  

#16 0x7fc939a5a4e2 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*) base/bind\_internal.h:749:12  

#17 0x7fc93e754f76 in Run base/callback.h:143:12  

#18 0x7fc93e754f76 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task\_annotator.cc:135:32  

#19 0x7fc93e79e531 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:410:29)> base/task/common/task\_annotator.h:74:5  

#20 0x7fc93e79e531 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:408:21  

#21 0x7fc93e79d938 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:286:41  

#22 0x7fc93e79f301 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc  

#23 0x7fc93e8cbaf9 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_libevent.cc:195:55  

#24 0x7fc93e79fb20 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:535:12  

#25 0x7fc93e6a5eff in base::RunLoop::Run(base::Location const&) base/run\_loop.cc:141:14  

#26 0x7fc91eff0630 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser\_main\_loop.cc:1039:18  

#27 0x7fc91eff4eeb in content::BrowserMainRunnerImpl::Run() content/browser/browser\_main\_runner\_impl.cc:157:15  

#28 0x7fc91efeac9a in content::BrowserMain(content::MainFunctionParams) content/browser/browser\_main.cc:30:28  

#29 0x7fc920f3c8f6 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:678:10  

#30 0x7fc920f3f5b5 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content\_main\_runner\_impl.cc:1188:10  

#31 0x7fc920f3e9f9 in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner\_impl.cc:1059:12  

#32 0x7fc920f38cf1 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) content/app/content\_main.cc:407:36  

#33 0x7fc920f39251 in content::ContentMain(content::ContentMainParams) content/app/content\_main.cc:435:10  

#34 0x55f928a2bd10 in ChromeMain chrome/app/chrome\_main.cc:189:12  

#35 0x7fc8e5648082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free base/memory/raw\_ptr.h:806:59 in operator bool  

Shadow bytes around the buggy address:  

0x0c2a8000c3e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c2a8000c3f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c2a8000c400: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 fa  

0x0c2a8000c410: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c2a8000c420: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x0c2a8000c430: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]  

0x0c2a8000c440: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2a8000c450: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x0c2a8000c460: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c2a8000c470: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c2a8000c480: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

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

==369827==ABORTING

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2022-06-16)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-06-16)

uploading screencast

### xi...@chromium.org (2022-06-16)

Thanks for the report! Reporter, does this reproduce for versions earlier than 105? Tentatively set FoundIn-105.

+aluh@, could you take a look? Thanks!

[Monorail components: UI>Shell>UIFoundations UI>Shell>WindowManager]

### [Deleted User] (2022-06-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-17)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-17)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2022-06-23)

[Empty comment from Monorail migration]

### al...@chromium.org (2022-06-23)

[Empty comment from Monorail migration]

### al...@chromium.org (2022-06-23)

@rhezashan, I'm not able to reproduce this on M105.  Could you show me the command you used to launch the emulator?  Also, are there any other details needed in the repro steps?

### rh...@gmail.com (2022-06-23)

aluh@,

out/chromeOS-Asan/chrome --ash-host-window-bounds="0+0-800x600,800+0-800x600" --force-tablet-mode=touch_view --touch-devices=8 --show-taps.
Make sure the second display is not mirroring,  change the second display to extended display by going to device->display or using --ash-dev-shortcuts (ctrl+shift+m)

### rh...@gmail.com (2022-06-23)

I uploaded new screencast. please skip to ~00:45. Tested on Chromium 105.0.5136.0 / commit 045c4205c69249adaa9207827b32efcf7449395a 

### jo...@chromium.org (2022-07-08)

I pinged Addison offline.

### al...@chromium.org (2022-07-08)

Sorry for the lack of response.  Thanks for the command line.  I'll try to repro this more.

### al...@chromium.org (2022-07-11)

I'm still not able to reproduce this.  What is your arg.gn config?

### rh...@gmail.com (2022-07-11)

x0x0@ubuntu:~/chromium/src$ cat out/chromeOS-asan/args.gn 
dcheck_always_on = false
enable_ipc_fuzzer = false
is_asan = true
is_component_build = true # default false
is_debug = false
is_lsan = true
symbol_level = 1
target_os = "chromeos"
v8_enable_verify_heap = false

### al...@chromium.org (2022-07-11)

I spoke too soon, I tried a few more times and I got it to happen once.  Not sure what the difference was though, but now I can dig more into it.

### rh...@gmail.com (2022-07-11)

Glad you now can repro the issue, hope this bug can fix soon. 

### al...@chromium.org (2022-07-12)

A fix is now in review.

### al...@chromium.org (2022-07-12)

crrev.com/c/3759514

### rh...@gmail.com (2022-07-13)

Thanks Addison for the CL. Really appreciate

### gi...@appspot.gserviceaccount.com (2022-07-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/064506711b4565a5de7d149a9ecec12fff5954fc

commit 064506711b4565a5de7d149a9ecec12fff5954fc
Author: Addison Luh <aluh@chromium.org>
Date: Mon Jul 18 19:32:45 2022

[asan] Fix UAF when capture window is cancelled by UpdateCapture.

During capture, when there are more than one non-mirror display, each host window delegate's UpdateCapture() is called. If an earlier call cancels the capture and destroys the old capture window, subsequent delegates that access the dangling pointer will cause a use-after-free.

The fix is to use a WindowTracker to detect when this happens and set the old capture window to nullptr, so later UpdateCapture() calls can check for it.

#asan

Bug: 1337002
Change-Id: Iee74163ca70e1a2d489ee681e957023b5678d2be
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3759514
Reviewed-by: Mitsuru Oshima <oshima@chromium.org>
Auto-Submit: Addison Luh <aluh@chromium.org>
Commit-Queue: Addison Luh <aluh@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1025368}

[modify] https://crrev.com/064506711b4565a5de7d149a9ecec12fff5954fc/ui/wm/core/capture_controller.cc
[modify] https://crrev.com/064506711b4565a5de7d149a9ecec12fff5954fc/ui/wm/core/capture_controller_unittest.cc


### gi...@appspot.gserviceaccount.com (2022-07-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/62efafb0ab4edb11bb652e285636545edd32d035

commit 62efafb0ab4edb11bb652e285636545edd32d035
Author: Addison Luh <aluh@chromium.org>
Date: Mon Jul 18 21:30:08 2022

Refactor CaptureController WindowTracker.

Follow up from crrev.com/c/3759514.

Bug: 1337002
Change-Id: I8f3b31f46bfbac27dfe2d04f0e63f4319cf34f68
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3768640
Auto-Submit: Addison Luh <aluh@chromium.org>
Commit-Queue: Addison Luh <aluh@chromium.org>
Reviewed-by: Mitsuru Oshima <oshima@chromium.org>
Commit-Queue: Mitsuru Oshima <oshima@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1025414}

[modify] https://crrev.com/62efafb0ab4edb11bb652e285636545edd32d035/ui/wm/core/capture_controller.cc


### al...@chromium.org (2022-07-18)

The UAF should be fixed now.

### al...@chromium.org (2022-07-18)

Thanks for the bug report!

### gi...@appspot.gserviceaccount.com (2022-07-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c31e572fc8ca7996db772cbc93e33d2cdab6e1fd

commit c31e572fc8ca7996db772cbc93e33d2cdab6e1fd
Author: Addison Luh <aluh@chromium.org>
Date: Tue Jul 19 01:52:54 2022

Fix CaptureControllerTest.UpdateCaptureDestroysOldCaptureWindow.

Handle the delegate iteration order being not deterministic.

Bug: 1337002
Change-Id: Ie93314e71491446b4a72edcecef10700a70c73e3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3771010
Commit-Queue: Nancy Wang <nancylingwang@chromium.org>
Owners-Override: Nancy Wang <nancylingwang@chromium.org>
Commit-Queue: Mitsuru Oshima <oshima@chromium.org>
Reviewed-by: Nancy Wang <nancylingwang@chromium.org>
Auto-Submit: Addison Luh <aluh@chromium.org>
Reviewed-by: Mitsuru Oshima <oshima@chromium.org>
Commit-Queue: Addison Luh <aluh@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1025523}

[modify] https://crrev.com/c31e572fc8ca7996db772cbc93e33d2cdab6e1fd/ui/wm/core/capture_controller_unittest.cc


### rh...@gmail.com (2022-07-19)

aluh@,

Thanks for the fix. I can confirm the fix works. I have no longer see the crash.

### al...@chromium.org (2022-07-19)

Great! Thanks for confirming!

### [Deleted User] (2022-07-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-22)

Not requesting merge to dev (M105) because latest trunk commit (1025523) appears to be prior to dev branch point (1027018). If this is incorrect, please replace the Merge-NA-105 label with Merge-Request-105. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-07-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c6bff67c33273f1d07ffb946e2eb4a9bfc10c52c

commit c6bff67c33273f1d07ffb946e2eb4a9bfc10c52c
Author: Addison Luh <aluh@chromium.org>
Date: Mon Jul 25 20:33:23 2022

Remove unused include for capture-controller.

Accidentally left out from crrev.com/c/3768640.

Bug: 1337002
Change-Id: Ie543afad730d9cb903889d173bb14de0441b9b2f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3783231
Reviewed-by: Mitsuru Oshima <oshima@chromium.org>
Commit-Queue: Mitsuru Oshima <oshima@chromium.org>
Auto-Submit: Addison Luh <aluh@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1027940}

[modify] https://crrev.com/c6bff67c33273f1d07ffb946e2eb4a9bfc10c52c/ui/wm/core/capture_controller.cc


### am...@google.com (2022-07-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2022-07-28)

Congratulations, Rheza! The VRP Panel has decided to award you $3,000 for this report. The reward amount was decided on based on this issue being significantly mitigated by it not being remote accessible and the significant user interaction and preconditions required. Thank you for your efforts and reporting this issue to us! 

### rh...@gmail.com (2022-07-28)

Thanks for the rewards.

### am...@google.com (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1337002?no_tracker_redirect=1

[Multiple monorail components: UI>Shell>UIFoundations, UI>Shell>WindowManager]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059985)*
