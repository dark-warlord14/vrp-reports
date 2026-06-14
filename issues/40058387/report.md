# Security: UAF in heap-use-after-free inin DevToolsWindow::Show(browser process)

| Field | Value |
|-------|-------|
| **Issue ID** | [40058387](https://issues.chromium.org/issues/40058387) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Editing>Command, Platform>DevTools |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | wo...@chromium.org |
| **Created** | 2022-01-01 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

When enable the Toggle Commander(Ctrl+Space) function, the `Merge Current Window into` command will send the undock devtools to the tabs.This will bypass the prohibition of show as tab function.

PS: Someone has submitted the similar issue and I found the function `show as tab` is prohibited. However the the Toggle Commander function will bypass the restriction.

**VERSION**  

Chrome Version: Version 98.0.4758.9 (Official Build) dev (64-bit)  

Operating System: Windows 10

**REPRODUCTION CASE**  

0. Enable chrome://flags/#commander

1. Open the devtools as a undocked separate window
2. Enter `Ctrl+Space` in the devtools window and enter `Merge Current Window into` to send the devtools window to a tab.  
   
   3.1 Enter F12 in the debugged page will triger the crash 1.  
   
   3.2 Edit the element in the devtools window will triger the crash 2.

See the poc.gif

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [browser]

# Crash 1:

==8664==ERROR: AddressSanitizer: heap-use-after-free on address 0x12188a1930f0 at pc 0x7fff03a91086 bp 0x00925fdfd240 sp 0x00925fdfd288  

READ of size 8 at 0x12188a1930f0 thread T0  

==8664==WARNING: Failed to use and restart external symbolizer!  

#0 0x7fff03a91085 in DevToolsWindow::Show C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\devtools\_window.cc:942  

#1 0x7fff03a8cbbe in DevToolsWindow::ScheduleShow C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\devtools\_window.cc:872  

#2 0x7fff03a8d53b in DevToolsWindow::ToggleDevToolsWindow C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\devtools\_window.cc:796  

#3 0x7fff03a8f588 in DevToolsWindow::ToggleDevToolsWindow C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\devtools\_window.cc:671  

#4 0x7fff059bbb5a in chrome::ToggleDevToolsWindow C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser\_commands.cc:1535  

#5 0x7fff05992c9f in chrome::BrowserCommandController::ExecuteCommandWithDisposition C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser\_command\_controller.cc:698  

#6 0x7fff06d42697 in BrowserView::AcceleratorPressed C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser\_view.cc:3428  

#7 0x7fff067f562f in ui::AcceleratorManager::Process C:\b\s\w\ir\cache\builder\src\ui\base\accelerators\accelerator\_manager.cc:83  

#8 0x7fff038b8198 in views::FocusManager::ProcessAccelerator C:\b\s\w\ir\cache\builder\src\ui\views\focus\focus\_manager.cc:536  

#9 0x7fff0af8b100 in views::UnhandledKeyboardEventHandler::HandleKeyboardEvent C:\b\s\w\ir\cache\builder\src\ui\views\controls\webview\unhandled\_keyboard\_event\_handler.cc:45  

#10 0x7ffefb207b33 in content::WebContentsImpl::HandleKeyboardEvent C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:3260  

#11 0x7ffefaf032fc in content::RenderWidgetHostImpl::OnKeyboardEventAck C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_widget\_host\_impl.cc:2501  

#12 0x7ffefabeaf15 in content::InputRouterImpl::KeyboardEventHandled C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\input\input\_router\_impl.cc:592  

#13 0x7ffefabf2c58 in base::internal::FunctorTraits<void (content::InputRouterImpl::\*)(const content::EventWithLatencyInfo[blink::WebMouseEvent](javascript:void(0);) &, base::OnceCallback<void (const content::EventWithLatencyInfo[blink::WebMouseEvent](javascript:void(0);) &, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)>, blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);)),void>::Invoke<void (content::InputRouterImpl::\*)(const content::EventWithLatencyInfo[blink::WebMouseEvent](javascript:void(0);) &, base::OnceCallback<void (const content::EventWithLatencyInfo[blink::WebMouseEvent](javascript:void(0);) &, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)>, blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);)),base::WeakPtr[content::InputRouterImpl](javascript:void(0);),content::EventWithLatencyInfo[blink::WebMouseEvent](javascript:void(0);),base::OnceCallback<void (const content::EventWithLatencyInfo[blink::WebMouseEvent](javascript:void(0);) &, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)>,blink::mojom::InputEventResultSource,const ui::LatencyInfo &,blink::mojom::InputEventResultState,mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);),mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);) > C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:535  

#14 0x7ffefabf294b in base::internal::Invoker<base::internal::BindState<void (content::InputRouterImpl::\*)(const content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) &, base::OnceCallback<void (const content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) &, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)>, blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);)),base::WeakPtr[content::InputRouterImpl](javascript:void(0);),content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);),base::OnceCallback<void (const content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) &, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)> >,void (blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);))>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:741  

#15 0x7ffef920617a in base::OnceCallback<void (blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);))>::Run C:\b\s\w\ir\cache\builder\src\base\callback.h:142  

#16 0x7ffefabf6a09 in base::internal::Invoker<base::internal::BindState<`lambda at ../../content/browser/renderer\_host/input/input\_router\_impl.cc:544:13',base::OnceCallback<void (blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);))>,base::WeakPtr[content::InputRouterImpl](javascript:void(0);) >,void (blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);))>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:741  

#17 0x7ffef920617a in base::OnceCallback<void (blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);))>::Run C:\b\s\w\ir\cache\builder\src\base\callback.h:142  

#18 0x7ffef9205ad7 in blink::mojom::WidgetInputHandler\_DispatchEvent\_ForwardToCallback::Accept C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\third\_party\blink\public\mojom\input\input\_handler.mojom.cc:5428  

#19 0x7fff014c449d in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:895  

#20 0x7fff03deb632 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#21 0x7fff014c7e34 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:657  

#22 0x7fff014dbc85 in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:1104  

#23 0x7fff014daa57 in mojo::internal::MultiplexRouter::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:724  

#24 0x7fff03deb632 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#25 0x7fff014bf8fc in mojo::Connector::DispatchMessageW C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:556  

#26 0x7fff014c11ed in mojo::Connector::ReadAllAvailableMessages C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:614  

#27 0x7fff01514fc2 in mojo::SimpleWatcher::OnHandleReady C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple\_watcher.cc:278  

#28 0x7fff01176e94 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#29 0x7fff03ca4b55 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  

#30 0x7fff03ca4228 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#31 0x7fff0121f9e6 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#32 0x7fff0121dc78 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#33 0x7fff03ca6221 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:468  

#34 0x7fff010f5a03 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#35 0x7ffefa30f3f1 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1048  

#36 0x7ffefa314811 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:153  

#37 0x7ffefa308a79 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#38 0x7ffefcd9a143 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:646  

#39 0x7ffefcd9d183 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1160  

#40 0x7ffefcd9c2b6 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1026  

#41 0x7ffefcd9858d in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:398  

#42 0x7ffefcd99618 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:426  

#43 0x7ffef665148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:177  

#44 0x7ff62dee5b85 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:169  

#45 0x7ff62dee2b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#46 0x7ff62e2e753f in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#47 0x7fffc8a77033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#48 0x7fffca462650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

0x12188a1930f0 is located 368 bytes inside of 968-byte region [0x12188a192f80,0x12188a193348)  

freed by thread T0 here:  

#0 0x7ff62df923fb in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7fff0346a8ed in Browser::~Browser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser.cc:562  

#2 0x7fff06d2d2e8 in BrowserView::~BrowserView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser\_view.cc:856  

#3 0x7fff06d45a4b in BrowserView::`vector deleting destructor'+0x19 (C:\chromium\_version\asan-win32-release\_x64-954424\chrome.dll+0x1906f5a4b)  

#4 0x7fff00eaaa5d in views::View::~View C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:253  

#5 0x7fff0ebfd0ff in GlassBrowserFrameView::~GlassBrowserFrameView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\glass\_browser\_frame\_view.cc:134  

#6 0x7fff00ef28cd in views::NonClientView::~NonClientView C:\b\s\w\ir\cache\builder\src\ui\views\window\non\_client\_view.cc:168  

#7 0x7fff00ef4683 in views::NonClientView::~NonClientView C:\b\s\w\ir\cache\builder\src\ui\views\window\non\_client\_view.cc:164  

#8 0x7fff00eacb1d in views::View::DoRemoveChildView C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:2638  

#9 0x7fff00eacea6 in views::View::RemoveAllChildViews C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:328  

#10 0x7fff00ed9165 in views::Widget::DestroyRootView C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1766  

#11 0x7fff00ed8d67 in views::Widget::~Widget C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:208  

#12 0x7fff087ae939 in BrowserFrame::~BrowserFrame C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser\_frame.cc:87  

#13 0x7fff0a725824 in views::DesktopNativeWidgetAura::~DesktopNativeWidgetAura C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_native\_widget\_aura.cc:304  

#14 0x7fff1025a64f in DesktopBrowserFrameAura::~DesktopBrowserFrameAura C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\desktop\_browser\_frame\_aura.cc:39  

#15 0x7fff0a704d12 in views::HWNDMessageHandler::OnWndProc C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:1036  

#16 0x7fff040031c6 in gfx::WindowImpl::WndProc C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window\_impl.cc:306  

#17 0x7fff04001ae1 in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> C:\b\s\w\ir\cache\builder\src\base\win\wrapped\_window\_proc.h:74  

#18 0x7fffc8b9e7e7 in CallWindowProcW+0x3f7 (C:\Windows\System32\user32.dll+0x18000e7e7)  

#19 0x7fffc8b9e36b in DispatchMessageW+0x39b (C:\Windows\System32\user32.dll+0x18000e36b)  

#20 0x7fffc8bb6ef7 in GetLastInputInfo+0x77 (C:\Windows\System32\user32.dll+0x180026ef7)  

#21 0x7fffca4b0ba3 in KiUserCallbackDispatcher+0x23 (C:\Windows\SYSTEM32\ntdll.dll+0x1800a0ba3)  

#22 0x7fffc8022383 in NtUserDestroyWindow+0x13 (C:\Windows\System32\win32u.dll+0x180002383)  

#23 0x7fff01176e94 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#24 0x7fff03ca4b55 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  

#25 0x7fff03ca4228 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#26 0x7fff0121f9e6 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#27 0x7fff0121dc78 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78

previously allocated by thread T0 here:  

#0 0x7ff62df924fb in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7fff139384be in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7fff03456e39 in Browser::Create C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser.cc:446  

#3 0x7fff03a923c9 in DevToolsWindow::CreateDevToolsBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\devtools\_window.cc:1677  

#4 0x7fff03a90cf5 in DevToolsWindow::Show C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\devtools\_window.cc:933  

#5 0x7fff03a9802c in DevToolsWindow::LoadCompleted C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\devtools\_window.cc:1741  

#6 0x7fff03a97dac in DevToolsWindow::SetIsDocked C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\devtools\_window.cc:1473  

#7 0x7fff06b517ed in DevToolsUIBindings::SetIsDocked C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\devtools\_ui\_bindings.cc:800  

#8 0x7fff0ace0598 in base::internal::Invoker<base::internal::BindState<void (DevToolsEmbedderMessageDispatcher::Delegate::\*)(base::OnceCallback<void (const base::Value \*)>, bool),base::internal::UnretainedWrapper<DevToolsEmbedderMessageDispatcher::Delegate> >,void (base::OnceCallback<void (const base::Value \*)>, bool)>::Run C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:754  

#9 0x7fff0ace0337 in `anonymous namespace'::ParseAndHandleWithCallback<bool> C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\devtools_embedder_message_dispatcher.cc:133 #10 0x7fff0acdee57 in base::internal::Invoker<base::internal::BindState<bool (\*)(const base::RepeatingCallback<void (const std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > &, const RegisterOptions &)> &, base::OnceCallback<void (const base::Value \*)>, const std::__1::vector<base::Value,std::__1::allocator<base::Value> > &),base::RepeatingCallback<void (const std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > &, const RegisterOptions &)> >,bool (base::OnceCallback<void (const base::Value \*)>, const std::__1::vector<base::Value,std::__1::allocator<base::Value> > &)>::Run C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:754 #11 0x7fff0acde614 in DispatcherImpl::Dispatch C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\devtools_embedder_message_dispatcher.cc:155 #12 0x7fff06b4f3c7 in DevToolsUIBindings::HandleMessageFromDevToolsFrontend C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\devtools_ui_bindings.cc:715 #13 0x7fff06b67e2a in base::internal::Invoker<base::internal::BindState<void (DevToolsUIBindings::\*)(base::Value),base::internal::UnretainedWrapper<DevToolsUIBindings> >,void (base::Value)>::Run C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:754 #14 0x7ffefb4f72ae in content::DevToolsFrontendHostImpl::DispatchEmbedderMessage C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools_frontend_host_impl.cc:92 #15 0x7ffef9186a1a in blink::mojom::DevToolsFrontendHostStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\public\mojom\devtools\devtools_frontend.mojom.cc:370 #16 0x7fff014c4629 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:900 #17 0x7fff03deb632 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43 #18 0x7fff014c7e34 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:657 #19 0x7fff01d47f0b in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread C:\b\s\w\ir\cache\builder\src\ipc\ipc\_mojo\_bootstrap.cc:1008  

#20 0x7fff01d41b27 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:741  

#21 0x7fff01176e94 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#22 0x7fff03ca4b55 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  

#23 0x7fff03ca4228 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#24 0x7fff0121f9e6 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#25 0x7fff0121dc78 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#26 0x7fff03ca6221 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:468  

#27 0x7fff010f5a03 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\devtools\_window.cc:942 in DevToolsWindow::Show  

Shadow bytes around the buggy address:  

0x04299b1b25c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x04299b1b25d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x04299b1b25e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x04299b1b25f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04299b1b2600: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x04299b1b2610: fd fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd  

0x04299b1b2620: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04299b1b2630: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04299b1b2640: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04299b1b2650: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04299b1b2660: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa  

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

==8664==ABORTING

Crash 2:  

==18792==ERROR: AddressSanitizer: heap-use-after-free on address 0x11e8b6d7b9f0 at pc 0x7fff05257462 bp 0x00b58ddfe290 sp 0x00b58ddfe2d8  

READ of size 8 at 0x11e8b6d7b9f0 thread T0  

==18792==WARNING: Failed to use and restart external symbolizer!  

#0 0x7fff05257461 in DevToolsWindow::ActivateWindow C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\devtools\_window.cc:1427  

#1 0x7fff0c49ed0a in `anonymous namespace'::ParseAndHandle<> C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\devtools_embedder_message_dispatcher.cc:121 #2 0x7fff0c49ee57 in base::internal::Invoker<base::internal::BindState<bool (\*)(const base::RepeatingCallback<void (const std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > &, const RegisterOptions &)> &, base::OnceCallback<void (const base::Value \*)>, const std::__1::vector<base::Value,std::__1::allocator<base::Value> > &),base::RepeatingCallback<void (const std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > &, const RegisterOptions &)> >,bool (base::OnceCallback<void (const base::Value \*)>, const std::__1::vector<base::Value,std::__1::allocator<base::Value> > &)>::Run C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:754 #3 0x7fff0c49e614 in DispatcherImpl::Dispatch C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\devtools_embedder_message_dispatcher.cc:155 #4 0x7fff0830f3c7 in DevToolsUIBindings::HandleMessageFromDevToolsFrontend C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\devtools_ui_bindings.cc:715 #5 0x7fff08327e2a in base::internal::Invoker<base::internal::BindState<void (DevToolsUIBindings::\*)(base::Value),base::internal::UnretainedWrapper<DevToolsUIBindings> >,void (base::Value)>::Run C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:754 #6 0x7ffefccb72ae in content::DevToolsFrontendHostImpl::DispatchEmbedderMessage C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools_frontend_host_impl.cc:92 #7 0x7ffefa946a1a in blink::mojom::DevToolsFrontendHostStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\public\mojom\devtools\devtools_frontend.mojom.cc:370 #8 0x7fff02c84629 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:900 #9 0x7fff055ab632 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43 #10 0x7fff02c87e34 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:657 #11 0x7fff03507f0b in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread C:\b\s\w\ir\cache\builder\src\ipc\ipc\_mojo\_bootstrap.cc:1008  

#12 0x7fff03501b27 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:741  

#13 0x7fff02936e94 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#14 0x7fff05464b55 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  

#15 0x7fff05464228 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#16 0x7fff029df9e6 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#17 0x7fff029ddc78 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#18 0x7fff05466221 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:468  

#19 0x7fff028b5a03 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#20 0x7ffefbacf3f1 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1048  

#21 0x7ffefbad4811 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:153  

#22 0x7ffefbac8a79 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#23 0x7ffefe55a143 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:646  

#24 0x7ffefe55d183 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1160  

#25 0x7ffefe55c2b6 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1026  

#26 0x7ffefe55858d in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:398  

#27 0x7ffefe559618 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:426  

#28 0x7ffef7e1148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:177  

#29 0x7ff62dee5b85 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:169  

#30 0x7ff62dee2b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#31 0x7ff62e2e753f in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#32 0x7fffc8a77033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#33 0x7fffca462650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

0x11e8b6d7b9f0 is located 368 bytes inside of 968-byte region [0x11e8b6d7b880,0x11e8b6d7bc48)  

freed by thread T0 here:  

#0 0x7ff62df923fb in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7fff04c2a8ed in Browser::~Browser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser.cc:562  

#2 0x7fff084ed2e8 in BrowserView::~BrowserView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser\_view.cc:856  

#3 0x7fff08505a4b in BrowserView::`vector deleting destructor'+0x19 (C:\chromium\_version\asan-win32-release\_x64-954424\chrome.dll+0x1906f5a4b)  

#4 0x7fff0266aa5d in views::View::~View C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:253  

#5 0x7fff103bd0ff in GlassBrowserFrameView::~GlassBrowserFrameView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\glass\_browser\_frame\_view.cc:134  

#6 0x7fff026b28cd in views::NonClientView::~NonClientView C:\b\s\w\ir\cache\builder\src\ui\views\window\non\_client\_view.cc:168  

#7 0x7fff026b4683 in views::NonClientView::~NonClientView C:\b\s\w\ir\cache\builder\src\ui\views\window\non\_client\_view.cc:164  

#8 0x7fff0266cb1d in views::View::DoRemoveChildView C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:2638  

#9 0x7fff0266cea6 in views::View::RemoveAllChildViews C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:328  

#10 0x7fff02699165 in views::Widget::DestroyRootView C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1766  

#11 0x7fff02698d67 in views::Widget::~Widget C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:208  

#12 0x7fff09f6e939 in BrowserFrame::~BrowserFrame C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser\_frame.cc:87  

#13 0x7fff0bee5824 in views::DesktopNativeWidgetAura::~DesktopNativeWidgetAura C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_native\_widget\_aura.cc:304  

#14 0x7fff11a1a64f in DesktopBrowserFrameAura::~DesktopBrowserFrameAura C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\desktop\_browser\_frame\_aura.cc:39  

#15 0x7fff0bec4d12 in views::HWNDMessageHandler::OnWndProc C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:1036  

#16 0x7fff057c31c6 in gfx::WindowImpl::WndProc C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window\_impl.cc:306  

#17 0x7fff057c1ae1 in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> C:\b\s\w\ir\cache\builder\src\base\win\wrapped\_window\_proc.h:74  

#18 0x7fffc8b9e7e7 in CallWindowProcW+0x3f7 (C:\Windows\System32\user32.dll+0x18000e7e7)  

#19 0x7fffc8b9e36b in DispatchMessageW+0x39b (C:\Windows\System32\user32.dll+0x18000e36b)  

#20 0x7fffc8bb6ef7 in GetLastInputInfo+0x77 (C:\Windows\System32\user32.dll+0x180026ef7)  

#21 0x7fffca4b0ba3 in KiUserCallbackDispatcher+0x23 (C:\Windows\SYSTEM32\ntdll.dll+0x1800a0ba3)  

#22 0x7fffc8022383 in NtUserDestroyWindow+0x13 (C:\Windows\System32\win32u.dll+0x180002383)  

#23 0x7fff02936e94 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#24 0x7fff05464b55 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  

#25 0x7fff05464228 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#26 0x7fff029df9e6 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#27 0x7fff029ddc78 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78

previously allocated by thread T0 here:  

#0 0x7ff62df924fb in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7fff150f84be in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7fff04c16e39 in Browser::Create C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser.cc:446  

#3 0x7fff052523c9 in DevToolsWindow::CreateDevToolsBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\devtools\_window.cc:1677  

#4 0x7fff05250cf5 in DevToolsWindow::Show C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\devtools\_window.cc:933  

#5 0x7fff05257e36 in DevToolsWindow::SetIsDocked C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\devtools\_window.cc:1501  

#6 0x7fff083117ed in DevToolsUIBindings::SetIsDocked C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\devtools\_ui\_bindings.cc:800  

#7 0x7fff0c4a0598 in base::internal::Invoker<base::internal::BindState<void (DevToolsEmbedderMessageDispatcher::Delegate::\*)(base::OnceCallback<void (const base::Value \*)>, bool),base::internal::UnretainedWrapper<DevToolsEmbedderMessageDispatcher::Delegate> >,void (base::OnceCallback<void (const base::Value \*)>, bool)>::Run C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:754  

#8 0x7fff0c4a0337 in `anonymous namespace'::ParseAndHandleWithCallback<bool> C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\devtools_embedder_message_dispatcher.cc:133 #9 0x7fff0c49ee57 in base::internal::Invoker<base::internal::BindState<bool (\*)(const base::RepeatingCallback<void (const std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > &, const RegisterOptions &)> &, base::OnceCallback<void (const base::Value \*)>, const std::__1::vector<base::Value,std::__1::allocator<base::Value> > &),base::RepeatingCallback<void (const std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > &, const RegisterOptions &)> >,bool (base::OnceCallback<void (const base::Value \*)>, const std::__1::vector<base::Value,std::__1::allocator<base::Value> > &)>::Run C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:754 #10 0x7fff0c49e614 in DispatcherImpl::Dispatch C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\devtools_embedder_message_dispatcher.cc:155 #11 0x7fff0830f3c7 in DevToolsUIBindings::HandleMessageFromDevToolsFrontend C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\devtools_ui_bindings.cc:715 #12 0x7fff08327e2a in base::internal::Invoker<base::internal::BindState<void (DevToolsUIBindings::\*)(base::Value),base::internal::UnretainedWrapper<DevToolsUIBindings> >,void (base::Value)>::Run C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:754 #13 0x7ffefccb72ae in content::DevToolsFrontendHostImpl::DispatchEmbedderMessage C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools_frontend_host_impl.cc:92 #14 0x7ffefa946a1a in blink::mojom::DevToolsFrontendHostStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\public\mojom\devtools\devtools_frontend.mojom.cc:370 #15 0x7fff02c84629 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:900 #16 0x7fff055ab632 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43 #17 0x7fff02c87e34 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:657 #18 0x7fff03507f0b in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread C:\b\s\w\ir\cache\builder\src\ipc\ipc\_mojo\_bootstrap.cc:1008  

#19 0x7fff03501b27 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:741  

#20 0x7fff02936e94 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#21 0x7fff05464b55 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  

#22 0x7fff05464228 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#23 0x7fff029df9e6 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#24 0x7fff029ddc78 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#25 0x7fff05466221 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:468  

#26 0x7fff028b5a03 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#27 0x7ffefbacf3f1 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1048

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\devtools\_window.cc:1427 in DevToolsWindow::ActivateWindow  

Shadow bytes around the buggy address:  

0x03f3cd72f6e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03f3cd72f6f0: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa  

0x03f3cd72f700: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x03f3cd72f710: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03f3cd72f720: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x03f3cd72f730: fd fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd  

0x03f3cd72f740: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03f3cd72f750: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03f3cd72f760: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03f3cd72f770: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03f3cd72f780: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa  

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

==18792==ABORTING

## Attachments

- [poc.gif](attachments/poc.gif) (image/gif, 7.3 MB)

## Timeline

### [Deleted User] (2022-01-01)

[Empty comment from Monorail migration]

### dr...@chromium.org (2022-01-04)

Commander is disabled by default, so setting Impact-None. This has pretty strict user gesture requirements, so setting Severity-Medium.

ellyjones@ - I think the fix here will be for Commander to disallow "Merge Current Window into", the same way "Show as tab" is disabled. Can you take a look?

[Monorail components: Blink>Editing>Command Platform>DevTools]

### el...@chromium.org (2022-01-04)

Sorry, I know virtually nothing about Commander's implementation and am not on that team any more. If the bug isn't urgent I would wait for lgrey@ to return from OOO.

### ya...@google.com (2022-01-04)

Wolfgang, please take a look. You previously fixed the "show as tab" issue.

### gi...@appspot.gserviceaccount.com (2022-01-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/696ee6c4096cd65e6584103bee4c2e234bcdd399

commit 696ee6c4096cd65e6584103bee4c2e234bcdd399
Author: Wolfgang Beyer <wolfi@chromium.org>
Date: Wed Jan 05 17:08:53 2022

[DevTools] Prevent Commander's 'Merge into...' for DevTools windows

When DevTools is opened as a separate Window and the commander is
enabled, there is a 'Merge current window into...' option which allows
turning DevTools into a regular browser tab. This can lead to unintended
behaviour which is why this CL disallows this command for DevTools
windows.

See also previous CL: https://crrev.com/c/3298125

Fixed: 1283681
Change-Id: I70d658e31735960331e79047fb6c6f58902d2438
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3367268
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Wolfgang Beyer <wolfi@chromium.org>
Cr-Commit-Position: refs/heads/main@{#955753}

[modify] https://crrev.com/696ee6c4096cd65e6584103bee4c2e234bcdd399/chrome/browser/ui/commander/window_command_source.cc


### [Deleted User] (2022-01-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-05)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-11)

Thank you for reporting this issue to us. The VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts! 

### am...@google.com (2022-02-14)

[Empty comment from Monorail migration]

### ds...@chromium.org (2022-02-15)

[Empty comment from Monorail migration]

### ds...@chromium.org (2022-02-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-04-13)

This issue was migrated from crbug.com/chromium/1283681?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Editing>Command, Platform>DevTools]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058387)*
