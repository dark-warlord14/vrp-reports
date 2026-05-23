# Security: heap-use-after-free C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\media_router\web_contents_display_observer_view.cc:56:22 in media_router::WebContentsDisplayObserverView::OnBrowserSetLastActive(class Browser *)

| Field | Value |
|-------|-------|
| **Issue ID** | [40057153](https://issues.chromium.org/issues/40057153) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Cast>UI |
| **Platforms** | Windows |
| **Reporter** | rh...@gmail.com |
| **Assignee** | mu...@google.com |
| **Created** | 2021-09-03 |
| **Bounty** | $15,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36

Steps to reproduce the problem:
1. Download mojo_notification.html and poc2.html into a folder "poc"
2. While in "poc/mojo", run "python copy_mojo_js_bindings.py path/to/out/Debug/gen" (script is attached, note the lack of trailing slash)
3. While in "poc", run "python3 -m http.server"
4. Run Chrome with flags "--enable-blink-features=MojoJS --enable-features=GlobalMediaControlsCastStartStop", navigate to localhost:8000, open mojo_notification.html click accept notification, then poc2.html.

when I comment on my own thread (one++ hour ago) at https://bugs.chromium.org/p/chromium/issues/detail?id=1243535#c19 , I saw the new security bug listed on https://bugs.chromium.org/p/chromium/issues/detail?id=1208264 and I did try his poc.html combining with mojo_notification.html.

I'm using dual monitor. After the poc2.html launch, hit "click me" then select another display. On the browser in the next monitor, hover to address bar with left hand hit enter , while the right hand (mice) clicking at same time.

the different security bug with https://bugs.chromium.org/p/chromium/issues/detail?id=1208264 were on the snippet error code below: 
    #25 0x7ff99fabe289 in views::DesktopWindowTreeHostWin::HandleMouseEvent(class ui::MouseEvent *) C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_window_tree_host_win.cc:1006:3
    #26 0x7ff9a3ab4e4d in views::HWNDMessageHandler::HandleMouseEventInternal(unsigned int, unsigned __int64, __int64, bool) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:3143:26
    #27 0x7ff9a3aae29f in views::HWNDMessageHandler::OnMouseRange C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:1972
    #28 0x7ff9a3aae29f in views::HWNDMessageHandler::_ProcessWindowMessage(struct HWND__*, unsigned int, 
unsigned __int64, __int64, __int64 &, unsigned long) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.h:356:5

Please see the attached video and I tested on toprice@ 918020 and the lower version @897847 .

What is the expected behavior?
NA

What went wrong?
==22300==ERROR: AddressSanitizer: heap-use-after-free on address 0x1260f4e2aa80 at pc 0x7ff9a71e4b94 bp 0x008b773fe6e0 sp 0x008b773fe728
READ of size 8 at 0x1260f4e2aa80 thread T0
    #0 0x7ff9a71e4b93 in media_router::WebContentsDisplayObserverView::OnBrowserSetLastActive(class Browser *) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\media_router\web_contents_display_observer_view.cc:56:22
    #1 0x7ff99c7f3f9c in BrowserList::SetLastActive(class Browser *) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser_list.cc:317:14
    #2 0x7ff99fff7edf in BrowserView::OnWidgetActivationChanged(class views::Widget *, bool) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_view.cc:2757:7
    #3 0x7ff99a39412d in views::Widget::OnNativeWidgetActivationChanged(bool) C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1350:14
    #4 0x7ff9a3acf768 in views::DesktopNativeWidgetAura::HandleActivationChanged(bool) C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_native_widget_aura.cc:393:33
    #5 0x7ff9a3ab3b50 in views::HWNDMessageHandler::PostProcessActivateMessage(int, bool, struct HWND__*) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:1311:16
    #6 0x7ff9a3aadafb in views::HWNDMessageHandler::OnWndProc(unsigned int, unsigned __int64, __int64) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:1039:5
    #7 0x7ff99d3400ea in gfx::WindowImpl::WndProc(struct HWND__*, unsigned int, unsigned __int64, __int64) C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window_impl.cc:306:18
    #8 0x7ff99d33ea05 in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc(struct HWND__*, unsigned 
int, unsigned __int64, __int64)>(struct HWND__*, unsigned int, unsigned __int64, __int64) C:\b\s\w\ir\cache\builder\src\base\win\wrapped_window_proc.h:74:10
    #9 0x7ffa1b35e857  (C:\WINDOWS\System32\user32.dll+0x18000e857)
    #10 0x7ffa1b35e3db  (C:\WINDOWS\System32\user32.dll+0x18000e3db)
    #11 0x7ffa1b370bc2  (C:\WINDOWS\System32\user32.dll+0x180020bc2)
    #12 0x7ffa1bdb0c53  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800a0c53)
    #13 0x7ffa194a2383  (C:\WINDOWS\System32\win32u.dll+0x180002383)
    #14 0x7ff99a623b9a in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\callback.h:100
    #15 0x7ff99a623b9a in base::TaskAnnotator::RunTask(char const *, struct base::PendingTask *) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178:33
    #16 0x7ff99d003842 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence_manager::LazyNow *) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:360:23
    #17 0x7ff99d002ea2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:260:36
    #18 0x7ff99a6c8666 in base::MessagePumpForUI::DoRunLoop(void) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:220:67
    #19 0x7ff99a6c68b8 in base::MessagePumpWin::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78:3
    #20 0x7ff99d004d45 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:467:12
    #21 0x7ff99a5a6623 in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134:14
    #22 0x7ff993ac38df in content::BrowserMainLoop::RunMainMessageLoop(void) C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:988:18
    #23 0x7ff993ac8c59 in content::BrowserMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:152:15
    #24 0x7ff993abcf56 in content::BrowserMain(struct content::MainFunctionParams const &) C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:49:28
    #25 0x7ff996429ef4 in content::RunBrowserProcessMain(struct content::MainFunctionParams const &, class content::ContentMainDelegate *) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:608:10
    #26 0x7ff99642c790 in content::ContentMainRunnerImpl::RunBrowser(struct content::MainFunctionParams &, bool) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1104:10
    #27 0x7ff99642b977 in content::ContentMainRunnerImpl::Run(bool) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:971:12
    #28 0x7ff9964283fa in content::RunContentProcess(struct content::ContentMainParams const &, class content::ContentMainRunner *) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:390:36
    #29 0x7ff99642943c in content::ContentMain(struct content::ContentMainParams const &) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:418:10
    #30 0x7ff98ff5148c in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:172:12      
    #31 0x7ff760755b74 in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169:12
    #32 0x7ff760752be8 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382:20    
    #33 0x7ff760b44b0f in invoke_main d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #34 0x7ff760b44b0f in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #35 0x7ffa19d97033  (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)
    #36 0x7ffa1bd62650  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

0x1260f4e2aa80 is located 0 bytes inside of 2968-byte region [0x1260f4e2aa80,0x1260f4e2b618)
freed by thread T0 here:
    #0 0x7ff7607f6edb in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ff9949faf57 in content::WebContentsImpl::`scalar deleting dtor'(unsigned int) C:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.h:912
    #2 0x7ff99c809327 in std::__1::default_delete<content::WebContents>::operator() C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h:54
    #3 0x7ff99c809327 in std::__1::unique_ptr<content::WebContents,std::__1::default_delete<content::WebContents> >::reset C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h:315
    #4 0x7ff99c809327 in TabStripModel::SendDetachWebContentsNotifications(struct TabStripModel::DetachNotifications *) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:556:27
    #5 0x7ff99c80f7bf in TabStripModel::CloseTabs(class base::span<class content::WebContents *const, -1>, unsigned int) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:1798:5
    #6 0x7ff99c810681 in TabStripModel::CloseWebContentsAt(int, unsigned int) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:767:10
    #7 0x7ff9949e4aff in content::WebContentsImpl::Close(class content::RenderViewHost *) C:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc:7101:16
    #8 0x7ff9927a9a11 in blink::mojom::LocalMainFrameHostStubDispatch::Accept(class blink::mojom::LocalMainFrameHost *, class mojo::Message *) C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\public\mojom\frame\frame.mojom.cc:19229:13
    #9 0x7ff99a96d7ed in mojo::InterfaceEndpointClient::HandleValidatedMessage(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:898:54
    #10 0x7ff99d147ec9 in mojo::MessageDispatcher::Accept(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:48:24
    #11 0x7ff99a971078 in mojo::InterfaceEndpointClient::HandleIncomingMessage(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:655:20
    #12 0x7ff99b1e1948 in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread C:\b\s\w\ir\cache\builder\src\ipc\ipc_mojo_bootstrap.cc:981:24
    #13 0x7ff99b1db83d in base::internal::FunctorTraits<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message),void>::Invoke C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:509    #14 0x7ff99b1db83d in base::internal::InvokeHelper<0,void>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:648
    #15 0x7ff99b1db83d in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message),scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:721
    #16 0x7ff99b1db83d in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message),scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:690:12
    #17 0x7ff99a623b9a in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\callback.h:100
    #18 0x7ff99a623b9a in base::TaskAnnotator::RunTask(char const *, struct base::PendingTask *) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178:33
    #19 0x7ff99d003842 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence_manager::LazyNow *) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:360:23
    #20 0x7ff99d002ea2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:260:36
    #21 0x7ff99a6c8666 in base::MessagePumpForUI::DoRunLoop(void) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:220:67
    #22 0x7ff99a6c68b8 in base::MessagePumpWin::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78:3
    #23 0x7ff99d004d45 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:467:12
    #24 0x7ff99a5a6623 in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134:14
    #25 0x7ff993ac38df in content::BrowserMainLoop::RunMainMessageLoop(void) C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:988:18
    #26 0x7ff993ac8c59 in content::BrowserMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:152:15
    #27 0x7ff993abcf56 in content::BrowserMain(struct content::MainFunctionParams const &) C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:49:28
    #28 0x7ff996429ef4 in content::RunBrowserProcessMain(struct content::MainFunctionParams const &, class content::ContentMainDelegate *) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:608:10
    #29 0x7ff99642c790 in content::ContentMainRunnerImpl::RunBrowser(struct content::MainFunctionParams &, bool) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1104:10
    #30 0x7ff99642b977 in content::ContentMainRunnerImpl::Run(bool) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:971:12
    #31 0x7ff9964283fa in content::RunContentProcess(struct content::ContentMainParams const &, class content::ContentMainRunner *) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:390:36
    #32 0x7ff99642943c in content::ContentMain(struct content::ContentMainParams const &) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:418:10
    #33 0x7ff98ff5148c in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:172:12      

previously allocated by thread T0 here:
    #0 0x7ff7607f6fdb in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ff9acbdf46a in operator new(unsigned __int64) d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
    #2 0x7ff9949801ea in content::WebContentsImpl::CreateWithOpener(struct content::WebContents::CreateParams const &, class content::RenderFrameHostImpl *) C:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc:1022:7
    #3 0x7ff994980038 in content::WebContentsImpl::Create(struct content::WebContents::CreateParams const &) C:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc:513:10
    #4 0x7ff99497ff41 in content::WebContents::Create(struct content::WebContents::CreateParams const &) 
C:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc:508:10
    #5 0x7ff99c7f9aa0 in `anonymous namespace'::CreateTargetContents C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser_navigator.cc:461
    #6 0x7ff99c7f9aa0 in Navigate(struct NavigateParams *) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser_navigator.cc:643:28
    #7 0x7ff99c7e9d66 in Browser::OpenURLFromTab(class content::WebContents *, struct content::OpenURLParams const &) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser.cc:1589:3
    #8 0x7ff9949b7d22 in content::WebContentsImpl::OpenURL(struct content::OpenURLParams const &) C:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc:4452:42
    #9 0x7ff99fd6e4f7 in RenderViewContextMenuBase::OpenURLWithExtraHeaders(class GURL const &, class GURL const &, enum WindowOpenDisposition, enum ui::PageTransition, class std::__1::basic_string<char, struct std::__1::char_traits<char>, class std::__1::allocator<char>> const &, bool) C:\b\s\w\ir\cache\builder\src\components\renderer_context_menu\render_view_context_menu_base.cc:490:25
    #10 0x7ff9a3fdec03 in RenderViewContextMenu::ExecuteCommand(int, int) C:\b\s\w\ir\cache\builder\src\chrome\browser\renderer_context_menu\render_view_context_menu.cc:2459:7
    #11 0x7ff9a6e49fa1 in views::MenuModelAdapter::ExecuteCommand(int, int) C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu_model_adapter.cc:170:12
    #12 0x7ff99fa849c3 in views::internal::MenuRunnerImpl::OnMenuClosed(enum views::internal::MenuControllerDelegate::NotifyType, class views::MenuItemView *, int) C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu_runner_impl.cc:245:29
    #13 0x7ff9a3a4eb22 in views::MenuController::ExitMenu(void) C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu_controller.cc:3154:13
    #14 0x7ff9a3a53f43 in views::MenuController::Accept(class views::MenuItemView *, int) C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu_controller.cc:1780:3
    #15 0x7ff9a3a534d7 in views::MenuController::OnMouseReleased(class views::SubmenuView *, class ui::MouseEvent const &) C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu_controller.cc:827:7
    #16 0x7ff99a397951 in views::Widget::OnMouseEvent(class ui::MouseEvent *) C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1548:20
    #17 0x7ff99b27e2b7 in ui::EventDispatcher::DispatchEvent(class ui::EventHandler *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:191:12
    #18 0x7ff99b27d7d7 in ui::EventDispatcher::ProcessEvent(class ui::EventTarget *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:140:5
    #19 0x7ff99b27d1c0 in ui::EventDispatcherDelegate::DispatchEventToTarget(class ui::EventTarget *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:84:14
    #20 0x7ff99b27ce04 in ui::EventDispatcherDelegate::DispatchEvent(class ui::EventTarget *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:56:15
    #21 0x7ff99fac08ac in ui::EventProcessor::OnEventFromSource(class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_processor.cc:49:17
    #22 0x7ff99cc195f3 in ui::EventSource::DeliverEventToSink(class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_source.cc:113:16
    #23 0x7ff99cc1924d in ui::EventSource::SendEventToSinkFromRewriter(class ui::Event const *, class ui::EventRewriter const *) C:\b\s\w\ir\cache\builder\src\ui\events\event_source.cc:138:12
    #24 0x7ff99cc18d4f in ui::EventSource::SendEventToSink(class ui::Event const *) C:\b\s\w\ir\cache\builder\src\ui\events\event_source.cc:107:10
    #25 0x7ff99fabe289 in views::DesktopWindowTreeHostWin::HandleMouseEvent(class ui::MouseEvent *) C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_window_tree_host_win.cc:1006:3
    #26 0x7ff9a3ab4e4d in views::HWNDMessageHandler::HandleMouseEventInternal(unsigned int, unsigned __int64, __int64, bool) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:3143:26
    #27 0x7ff9a3aae29f in views::HWNDMessageHandler::OnMouseRange C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:1972
    #28 0x7ff9a3aae29f in views::HWNDMessageHandler::_ProcessWindowMessage(struct HWND__*, unsigned int, 
unsigned __int64, __int64, __int64 &, unsigned long) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.h:356:5
    #29 0x7ff9a3aad93e in views::HWNDMessageHandler::OnWndProc(unsigned int, unsigned __int64, __int64) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:1017:7

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\media_router\web_contents_display_observer_view.cc:56:22 in media_router::WebContentsDisplayObserverView::OnBrowserSetLastActive(class Browser *)
Shadow bytes around the buggy address:
  0x046f13645500: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x046f13645510: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x046f13645520: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x046f13645530: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x046f13645540: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x046f13645550:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x046f13645560: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x046f13645570: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x046f13645580: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x046f13645590: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x046f136455a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==22300==ABORTING

Did this work before? N/A 

Chrome version: 93.0.4577.63  Channel: dev
OS Version: 10.0

## Attachments

- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 512 B)
- [mojo_notification.html](attachments/mojo_notification.html) (text/plain, 3.2 KB)
- [poc2.html](attachments/poc2.html) (text/plain, 563 B)
- [bandicam 2021-09-03 21-16-33-484.mp4](attachments/bandicam 2021-09-03 21-16-33-484.mp4) (video/mp4, 4.8 MB)
- [asan_897847_log.txt](attachments/asan_897847_log.txt) (text/plain, 65.3 KB)
- [asan_918020_log.txt](attachments/asan_918020_log.txt) (text/plain, 20.8 KB)
- [chrome-stable-windows.mp4](attachments/chrome-stable-windows.mp4) (video/mp4, 3.3 MB)
- [chrome-canary-windows.mp4](attachments/chrome-canary-windows.mp4) (video/mp4, 3.3 MB)
- [chrome-dev-windows.mp4](attachments/chrome-dev-windows.mp4) (video/mp4, 5.7 MB)
- [chrome_debug-canary.log](attachments/chrome_debug-canary.log) (text/plain, 109.6 KB)
- [chrome_debug-dev.log](attachments/chrome_debug-dev.log) (text/plain, 86.1 KB)
- [error.log](attachments/error.log) (text/plain, 14.9 KB)
- [google-asan-toprice-ubuntu.webm](attachments/google-asan-toprice-ubuntu.webm) (video/webm, 9.1 MB)
- [google-dev-ubuntu.webm](attachments/google-dev-ubuntu.webm) (video/webm, 4.1 MB)
- [google-stable-official.webm](attachments/google-stable-official.webm) (video/webm, 3.0 MB)
- [asan-release-windows-without-flags.txt](attachments/asan-release-windows-without-flags.txt) (text/plain, 21.4 KB)
- [windows-asan-toprice-without-flag.mp4](attachments/windows-asan-toprice-without-flag.mp4) (video/mp4, 3.9 MB)
- [bandicam 2021-09-09 10-54-45-150.mp4](attachments/bandicam 2021-09-09 10-54-45-150.mp4) (video/mp4, 2.2 MB)
- [bandicam 2021-09-11 08-46-52-313.mp4](attachments/bandicam 2021-09-11 08-46-52-313.mp4) (video/mp4, 3.2 MB)
- [asan_log_media_notification_device_selector_view.txt](attachments/asan_log_media_notification_device_selector_view.txt) (text/plain, 25.2 KB)
- [Recording #4.mp4](attachments/Recording #4.mp4) (video/mp4, 2.3 MB)

## Timeline

### rh...@gmail.com (2021-09-03)

uploading asan log.

### [Deleted User] (2021-09-03)

[Empty comment from Monorail migration]

### ct...@google.com (2021-09-03)

Thanks for the report. Adding folks from https://crbug.com/chromium/1208264 -- this is a similar crash as was occurring there. I don't currently have a multi-display setup available for testing, but let me know if you need any assistance reproducing this or triaging.

Setting some security labels:

- Security_Severity-High: This is a browser memory corruption, but it requires a compromised renderer.
- Security_Impact-Beta: The GlobalMediaControlsCastStartStop flag is disabled by default, but it appears to be enabled at 50% Beta currently via Finch (per https://crbug.com/chromium/1107158)


[Monorail components: Internals>Cast>UI]

### [Deleted User] (2021-09-04)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rh...@gmail.com (2021-09-04)

Added screen record on Chrome stable Windows, Chrome Canary Windows, Chrome Dev Windows

### rh...@gmail.com (2021-09-04)

Added screen record on Chrome stable ubuntu, Chrome Dev ubuntu, Chrome asan-release-918379 .


### rh...@gmail.com (2021-09-04)

Another testing on windows asan-win32-release_x64-918020 without flag #GlobalMediaControlsCastStartStop

### [Deleted User] (2021-09-07)

This issue is marked as a release blocker with no milestone associated. Please add an appropriate milestone.

All release blocking issues should have milestones associated to it, so that the issue can tracked and the fixes can be pushed promptly.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-09-07)

Setting FoundIn to match https://crbug.com/chromium/1246394#c3. I haven't done additional testing.

### rh...@gmail.com (2021-09-07)

FYI, only reproduce on Windows. I hope someone could to test on multi-display.  

### [Deleted User] (2021-09-08)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ta...@chromium.org (2021-09-08)

In https://crbug.com/chromium/1246394#c5 I see that the crash is occurring on the stable channel with GlobalMediaControlsCastStartStop disabled, is that right? Then it's not related to GlobalMediaControlsCastStartStop.

### sr...@google.com (2021-09-08)

pls note this is marked as RBS for M94 and we are cutting stable RC for M94 next tuesday ( 9/14), pls help get the fix landed on trunk and ready for merge before 9/14.

### mf...@chromium.org (2021-09-08)

The PoC requires the user to interact with the Cast dialog and select a secondary monitor as a cast target, so a compromised renderer (by itself) is not sufficient to trigger this.  Not sure if that affects the triage here.


### mu...@google.com (2021-09-09)

Hi rhezashan@,

It looks like you've found two different bugs:
(1) The first bug is an UaF error, which has been fixed in https://crbug.com/chromium/1208264. The videos posted in the issue description and https://crbug.com/chromium/1246394#c7 are related this bug. I noticed that you were testing on M89 and M91. The fix was landed in M92. Could you please verify that the issue has been fixed in the latest build?

(2) The second bug is a chrome crash issue when clicking on the address bar on the other display. Your videos in https://crbug.com/chromium/1246394#c5 and #6 are related to this issue. 
I was not able to reproduce this bug locally since it requires dual-monitor set up. Since this is a separate crash issue, I filed https://crbug.com/chromium/1247899 to track it.




### [Deleted User] (2021-09-09)

[Empty comment from Monorail migration]

### rh...@gmail.com (2021-09-09)

Hi muyaoxu@,

I'm trying to answer your questions correctly:

Answer for question point (1):
1. I tested Asan build from https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/win32-release_x64%2Fasan-win32-release_x64-918020.zip?generation=1630662300145562&alt=media, (Fri Sep 03 08:49:45 2021) , Chrome Version 95.0.4632.0 (Developer Build) (64-bit) 
2. While https://crbug.com/chromium/1208264 were tested on Chrome Version: 92.0.4504.0 (Official Build) canary (x86_64) and fixed on https://chromium.googlesource.com/chromium/src/+/8f7f373eae000caeafabe17ceee433469b291767 (Mon May 24 17:26:51 2021)
3. https://crbug.com/chromium/1208264 is not required a user click. While on my found issue, user click is required to select (cast) another monitor as https://crbug.com/chromium/1246394#c14.
4.  From my limited knowledge the bug UAF exist on 
  views::Widget* new_widget = views::Widget::GetWidgetForNativeWindow(
      web_contents_->GetTopLevelNativeWindow());
  if (new_widget != widget_) {
    widget_->RemoveObserver(this);
    widget_ = new_widget;
    if (widget_) {
      widget_->AddObserver(this);
      CheckForDisplayChange();
    }
  }
}
5. I'm providing you the latest video I made 10 minutes ago. Tested on Asan build 918020.zip

Answer on question point(2):
1. Yes you are correct. After cast to another display, when user click and type address bar  on second screen, the chrome crash. It's maybe functional bug.

------------
My question: Do you want me to test what asan version, the latest asan build is https://crrev.com/919600 (Thu Sep 09 03:20:17 2021)?


### rh...@gmail.com (2021-09-09)

Another answer, https://crbug.com/chromium/1208264 reproduce on linux and macOs. While my issue reproduce on Windows. I can not test on MacOs, I don't have the MacOs currently.

### rh...@gmail.com (2021-09-09)

Hi muyaoxu@,

I apologize if not understood correctly. 
There is no files on https://commondatastorage.googleapis.com/chromium-browser-asan/index.html?prefix=win32-release_x64/asan-win32-release_x64-92. Do you have suggestion where I must download and test? or should I build chrome from scratch https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/windows_build_instructions.md?

### mu...@google.com (2021-09-09)

Hi rhezashan@,

Thanks for the quick response.
Sorry I made a mistake about the chrome versions that you were testing on. There is no need for additional testings. 

### [Deleted User] (2021-09-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7f8325b9eb0203f3b6dbdef1489d5e5f23ddba4a

commit 7f8325b9eb0203f3b6dbdef1489d5e5f23ddba4a
Author: Muyao Xu <muyaoxu@google.com>
Date: Fri Sep 10 01:07:32 2021

Fix UaF in WebContentsDisplayObserverView::SetBrowserLastActive

The WebContentsDisplayObserverView is a WebContentsObserver but it has
not been observing the |web_contents_|. As a result it does not null out
the |web_contents_| when it is deleted, and get an UaF error in
SetBrowserLastActive().

Bug: b/199183534, 1246394
Change-Id: I47f4214b576d3a031c2e339621d0e22db4dbae4f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3152044
Commit-Queue: Muyao Xu <muyaoxu@google.com>
Reviewed-by: Takumi Fujimoto <takumif@chromium.org>
Cr-Commit-Position: refs/heads/main@{#920052}

[modify] https://crrev.com/7f8325b9eb0203f3b6dbdef1489d5e5f23ddba4a/chrome/browser/ui/views/media_router/web_contents_display_observer_view.cc


### rh...@gmail.com (2021-09-10)

Hi muyaoxu@,

Thank you for the fixing the issue.
I will verify the changes later tonight.

### rh...@gmail.com (2021-09-11)

Hello muyaoxu@,

The patch works for web_contents_display_observer_view.cc and UAF doesn't exist anymore but another UAF occurs on chrome\browser\ui\views\global_media_controls\media_notification_device_selector_view.cc:520:34
I was testing on latest asan-win32-release-920443.zip. Please see videos attached. 

I'm happy for another testing anytime after new patch . Please do not hesitate ping me 

### rh...@gmail.com (2021-09-11)

upload asan-log

### mu...@google.com (2021-09-13)

Hi rhezashan@,

Thanks for the testing! The new issue you found has been fixed. You can verify it in the latest Chrome build (later than 930529).
I'll make this as fixed since the UaF issue in WebContentsDisplayObserverView no longer reproduced.

### [Deleted User] (2021-09-13)

This bug requires manual review: We are only 7 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), harrysouders@(iOS), matthewjoseph@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mu...@google.com (2021-09-13)

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
Yes.

2. Links to the CLs you are requesting to merge.
https://chromium-review.googlesource.com/c/chromium/src/+/3152044

3. Has the change landed and been verified on ToT?
Yes.

4. Does this change need to be merged into other active release branches (M-1, M+1)?
M94 and M95.

5. Why are these changes required in this milestone after branch?
This is a Security issue.

6. Is this a new feature?
This issue is caused by a new feature.

7. If it is a new feature, is it behind a flag using finch?
The new feature is hidden behind the flag: global-media-controls-cast-start-stop. The flag is currently enabled 50% in Beta.

### sr...@google.com (2021-09-13)

Merge approved for M94 pls merge asap

### rh...@gmail.com (2021-09-13)

Hello muyaoxu@,

Thank you for your quick response. I have a questions and I need to understand to improve my report in the future.
1. As your comment https://crbug.com/chromium/1246394#c26 Chrome build (later than 930529). I really have no idea what chrome 930529 is it? The latest asan-win32-release_x64-92 is "920800" version 96, Please tell me how to verify your patch.
2. Your patch https://crbug.com/chromium/1246394#c22, https://chromium.googlesource.com/chromium/src/+/7f8325b9eb0203f3b6dbdef1489d5e5f23ddba4a (Fri Sep 10 01:07:32 2021) and I tested with https://chromium.googlesource.com/chromium/src/+/caf69bf7f10fd303ce9be13084e22a603bbd2c07 (Sat Sep 11 00:21:48 2021)  with asan-win32-release-920443.zip on https://crbug.com/chromium/1246394#c24. The new UaF occur within  chrome\browser\ui\views\global_media_controls\media_notification_device_selector_view.cc:520:34

Today the latest asan-win32-release_x64 developer is https://crrev.com/920800. Do you want me to verify with this build?
I need to understand well. Please tell me

### rh...@gmail.com (2021-09-13)

[Comment Deleted]

### rh...@gmail.com (2021-09-13)

I appreciate if someone can answer the questions on https://crbug.com/chromium/1246394#c30 or make it easier for me to understand.

Thanks

### mu...@google.com (2021-09-13)

Hi rhezashan@, sorry I made a typo. I meant 920529 or laterwser-asan/index.html?prefix=win32-release_x64/asan-win32-release_x64-920529

### sr...@google.com (2021-09-13)

Please complete your merges to M94 asap .we are cutting stable RC build tomorrow morning at 2pm PST, so all merges should be in before that time. 

### rh...@gmail.com (2021-09-13)

Hi muyaoxu@,

Yes it's fixed and no longer reproduced on asan/index.html?prefix=win32-release_x64/asan-win32-release_x64-920800. Glad you're fixed the root issues.

### gi...@appspot.gserviceaccount.com (2021-09-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ee43a9e9f6593c065db5c32b62155a431bd164e1

commit ee43a9e9f6593c065db5c32b62155a431bd164e1
Author: Muyao Xu <muyaoxu@google.com>
Date: Mon Sep 13 21:37:00 2021

Fix UaF in WebContentsDisplayObserverView::SetBrowserLastActive

The WebContentsDisplayObserverView is a WebContentsObserver but it has
not been observing the |web_contents_|. As a result it does not null out
the |web_contents_| when it is deleted, and get an UaF error in
SetBrowserLastActive().

(cherry picked from commit 7f8325b9eb0203f3b6dbdef1489d5e5f23ddba4a)

Bug: b/199183534, 1246394
Change-Id: I47f4214b576d3a031c2e339621d0e22db4dbae4f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3152044
Commit-Queue: Muyao Xu <muyaoxu@google.com>
Reviewed-by: Takumi Fujimoto <takumif@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#920052}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3158317
Auto-Submit: Muyao Xu <muyaoxu@google.com>
Commit-Queue: Takumi Fujimoto <takumif@chromium.org>
Cr-Commit-Position: refs/branch-heads/4606@{#1004}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/ee43a9e9f6593c065db5c32b62155a431bd164e1/chrome/browser/ui/views/media_router/web_contents_display_observer_view.cc


### mu...@google.com (2021-09-13)

Thanks for testing rhezashan@!

### rh...@gmail.com (2021-09-14)

My pleasure muyaoxu@ and can you confirm I found two issues and the issues has been fixed and no longer reproduced on the latest chrome version. Below the summary :

MediaNotificationDeviceSelectorView::DoStartCastSession UaF https://crbug.com/chromium/1246394#c1 - fixed on https://crrev.com/920052

WebContentsDisplayObserverView::OnBrowserSetLastActive UaF https://crbug.com/chromium/1246394#c25- fixed on https://crrev.com/920529

Thank you for fixing and confirmation.

### [Deleted User] (2021-09-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-14)

[Empty comment from Monorail migration]

### mu...@google.com (2021-09-14)

Hi rhezashan@,

It looks like you made a typo in function names. 
The UaF you found in WebContentsDisplayObserverView::OnBrowserSetLastActive (described in https://crbug.com/chromium/1246394#c1) was fixed by https://crrev.com/920052

The Uaf issue in WebContentsDisplayObserverView::OnBrowserSetLastActive was discovered (https://crbug.com/chromium/1248628) and fixed (https://crrev.com/920529) before you tested in https://crbug.com/chromium/1246394#c25. 

### rh...@gmail.com (2021-09-14)

Hi muyaoxu@,

Yes you're correct. My mistake for typo.

### am...@google.com (2021-09-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-23)

Congratulations! The VRP Panel has decided to award you $15,000 for this report. A member of our finance team will be in touch soon to arrange payment. 
In the meantime, please let us know to whom (which name or a handle) you would like us to attribute this issue in our public security fix release notes. 
Thank you for reporting this issue to us! 

### rh...@gmail.com (2021-09-23)

Thank you for all chromium security team, please add credit to "@ginggilBesel"


### am...@google.com (2021-09-24)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1246394?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057153)*
