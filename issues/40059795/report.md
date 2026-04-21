# Security: heap-use-after-free in views::DialogDelegate::CancelDialog

| Field | Value |
|-------|-------|
| **Issue ID** | [40059795](https://issues.chromium.org/issues/40059795) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>WebAppProvider |
| **Platforms** | Windows |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ph...@chromium.org |
| **Created** | 2022-05-30 |
| **Bounty** | $3,000.00 |

## Description

I found an asan log, but the reason is not clear. You can analyze it yourself.

=================================================================
==6380==ERROR: AddressSanitizer: heap-use-after-free on address 0x123707cee7a8 at pc 0x7ffe484cfe17 bp 0x0034b87fd870 sp 0x0034b87fd8b8
WRITE of size 1 at 0x123707cee7a8 thread T0
==6380==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ffe484cfe16 in views::DialogDelegate::CancelDialog C:\b\s\w\ir\cache\builder\src\ui\views\window\dialog_delegate.cc:434
    #1 0x7ffe484169e5 in views::Button::NotifyClick C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button.cc:648
    #2 0x7ffe48412e49 in views::Button::DefaultButtonControllerDelegate::NotifyClick C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button.cc:67
    #3 0x7ffe4b27d432 in views::ButtonController::OnMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button_controller.cc:59
    #4 0x7ffe48499580 in views::View::ProcessMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3118
    #5 0x7ffe4e3b71ce in ui::ScopedTargetHandler::OnEvent C:\b\s\w\ir\cache\builder\src\ui\events\scoped_target_handler.cc:28
    #6 0x7ffe49482085 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:190
    #7 0x7ffe494814d7 in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:139
    #8 0x7ffe49480dc1 in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:83
    #9 0x7ffe49480a2b in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:55
    #10 0x7ffe4b23f377 in views::internal::RootView::OnMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\widget\root_view.cc:485
    #11 0x7ffe484c2dc9 in views::Widget::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1565
    #12 0x7ffe49482085 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:190
    #13 0x7ffe494814d7 in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:139
    #14 0x7ffe49480dc1 in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:83
    #15 0x7ffe49480a2b in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:55
    #16 0x7ffe4e3b454e in ui::EventProcessor::OnEventFromSource C:\b\s\w\ir\cache\builder\src\ui\events\event_processor.cc:49
    #17 0x7ffe4b274883 in ui::EventSource::DeliverEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event_source.cc:118
    #18 0x7ffe4b2744dd in ui::EventSource::SendEventToSinkFromRewriter C:\b\s\w\ir\cache\builder\src\ui\events\event_source.cc:143
    #19 0x7ffe4b273fdf in ui::EventSource::SendEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event_source.cc:112
    #20 0x7ffe4e3f5d29 in views::DesktopWindowTreeHostWin::HandleMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_window_tree_host_win.cc:1004
    #21 0x7ffe52500d10 in views::HWNDMessageHandler::HandleMouseEventInternal C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:3239
    #22 0x7ffe524f9d9b in views::HWNDMessageHandler::_ProcessWindowMessage C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.h:360
    #23 0x7ffe524f942d in views::HWNDMessageHandler::OnWndProc C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:1092
    #24 0x7ffe4b9d992c in gfx::WindowImpl::WndProc C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window_impl.cc:306
    #25 0x7ffe4b9d829d in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> C:\b\s\w\ir\cache\builder\src\base\win\wrapped_window_proc.h:74
    #26 0x7ffee7bde9bb in DispatchMessageW+0x7db (C:\WINDOWS\System32\user32.dll+0x18000e9bb)
    #27 0x7ffee7bde3e0 in DispatchMessageW+0x200 (C:\WINDOWS\System32\user32.dll+0x18000e3e0)
    #28 0x7ffe4885678f in base::MessagePumpForUI::ProcessMessageHelper C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:531
    #29 0x7ffe48854473 in base::MessagePumpForUI::ProcessNextWindowsMessage C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:498
    #30 0x7ffe48853d13 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:209
    #31 0x7ffe48852064 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #32 0x7ffe4b6a337a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:542
    #33 0x7ffe48703f57 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:141
    #34 0x7ffe41132b67 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1039
    #35 0x7ffe41137f33 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:157
    #36 0x7ffe4112c0ad in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:30
    #37 0x7ffe482c0e3b in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:660
    #38 0x7ffe482c3fb4 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1167
    #39 0x7ffe482c30e6 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1039
    #40 0x7ffe482bfab3 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:407
    #41 0x7ffe482c023c in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:435
    #42 0x7ffe3ceb14be in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:177
    #43 0x7ff6a3745d62 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:167
    #44 0x7ff6a3742b7d in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:385
    #45 0x7ff6a3b48aaf in __scrt_common_main_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #46 0x7ffee6ec244c in BaseThreadInitThunk+0x1c (C:\WINDOWS\System32\KERNEL32.DLL+0x18001244c)
    #47 0x7ffee846ad27 in RtlUserThreadStart+0x27 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005ad27)

0x123707cee7a8 is located 552 bytes inside of 1424-byte region [0x123707cee580,0x123707ceeb10)
freed by thread T0 here:
    #0 0x7ff6a37f058b in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ffe4d5da679 in WebAppUninstallDialogDelegateView::~WebAppUninstallDialogDelegateView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\web_apps\web_app_uninstall_dialog_view.cc:124
    #2 0x7ffe484cae35 in views::WidgetDelegate::DeleteDelegate C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget_delegate.cc:247
    #3 0x7ffe484c0e93 in views::Widget::OnNativeWidgetDestroyed C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1423
    #4 0x7ffe5251a5b0 in views::DesktopNativeWidgetAura::OnHostClosed C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_native_widget_aura.cc:386
    #5 0x7ffe524f9589 in views::HWNDMessageHandler::OnWndProc C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:1109
    #6 0x7ffe4b9d992c in gfx::WindowImpl::WndProc C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window_impl.cc:306
    #7 0x7ffe4b9d829d in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> C:\b\s\w\ir\cache\builder\src\base\win\wrapped_window_proc.h:74
    #8 0x7ffee7bde9bb in DispatchMessageW+0x7db (C:\WINDOWS\System32\user32.dll+0x18000e9bb)
    #9 0x7ffee7bde5db in DispatchMessageW+0x3fb (C:\WINDOWS\System32\user32.dll+0x18000e5db)
    #10 0x7ffee7bf5b41 in RegisterClipboardFormatW+0x91 (C:\WINDOWS\System32\user32.dll+0x180025b41)
    #11 0x7ffee84b2f73 in KiUserCallbackDispatcher+0x23 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800a2f73)
    #12 0x7ffee5972753 in NtUserDestroyWindow+0x13 (C:\WINDOWS\System32\win32u.dll+0x180002753)
    #13 0x7ffe484b99d9 in views::Widget::CloseNow C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:705
    #14 0x7ffe4b2cda5d in views::`anonymous namespace'::WindowCallbackProc C:\b\s\w\ir\cache\builder\src\ui\views\widget\native_widget_aura.cc:1171
    #15 0x7ffee7bd8c72 in EnumChildWindows+0x1d2 (C:\WINDOWS\System32\user32.dll+0x180008c72)
    #16 0x7ffee7bd8a43 in EnumThreadWindows+0x23 (C:\WINDOWS\System32\user32.dll+0x180008a43)
    #17 0x7ffe4e5aeb60 in BrowserProcessImpl::Unpin C:\b\s\w\ir\cache\builder\src\chrome\browser\browser_process_impl.cc:1407
    #18 0x7ffe43524ee5 in KeepAliveRegistry::OnKeepAliveStateChanged C:\b\s\w\ir\cache\builder\src\components\keep_alive_registry\keep_alive_registry.cc:182
    #19 0x7ffe43525edc in KeepAliveRegistry::Unregister C:\b\s\w\ir\cache\builder\src\components\keep_alive_registry\keep_alive_registry.cc:166
    #20 0x7ffe4adc5eab in base::internal::Invoker<base::internal::BindState<`lambda at ../../chrome/browser/ui/web_applications/web_app_ui_manager_impl.cc:96:24',std::__1::unique_ptr<ScopedKeepAlive,std::__1::default_delete<ScopedKeepAlive> > >,void (bool)>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:747
    #21 0x7ffe4adbf4b4 in web_app::WebAppDialogManager::OnWebAppUninstallDialogClosed C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\web_applications\web_app_dialog_manager.cc:68
    #22 0x7ffe4adbf89a in base::internal::Invoker<base::internal::BindState<void (web_app::WebAppDialogManager::*)(web_app::WebAppUninstallDialog *, base::OnceCallback<void (bool)>, bool),base::internal::UnretainedWrapper<web_app::WebAppDialogManager>,base::internal::UnretainedWrapper<web_app::WebAppUninstallDialog>,base::OnceCallback<void (bool)> >,void (bool)>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:747
    #23 0x7ffe4d5d7f75 in WebAppUninstallDialogDelegateView::OnDialogCanceled C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\web_apps\web_app_uninstall_dialog_view.cc:149
    #24 0x7ffe484cdb15 in views::DialogDelegate::Cancel C:\b\s\w\ir\cache\builder\src\ui\views\window\dialog_delegate.cc:165
    #25 0x7ffe484cfd92 in views::DialogDelegate::CancelDialog C:\b\s\w\ir\cache\builder\src\ui\views\window\dialog_delegate.cc:431
    #26 0x7ffe484169e5 in views::Button::NotifyClick C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button.cc:648
    #27 0x7ffe48412e49 in views::Button::DefaultButtonControllerDelegate::NotifyClick C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button.cc:67

previously allocated by thread T0 here:
    #0 0x7ff6a37f068b in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffe5b9fd3ee in operator new d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
    #2 0x7ffe4d5d9edc in WebAppUninstallDialogViews::OnIconsRead C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\web_apps\web_app_uninstall_dialog_view.cc:264
    #3 0x7ffe4d5dadcc in base::internal::FunctorTraits<void (WebAppUninstallDialogViews::*)(webapps::WebappUninstallSource, std::__1::map<int,SkBitmap,std::__1::less<int>,std::__1::allocator<std::__1::pair<const int,SkBitmap> > >),void>::Invoke<void (WebAppUninstallDialogViews::*)(webapps::WebappUninstallSource, std::__1::map<int,SkBitmap,std::__1::less<int>,std::__1::allocator<std::__1::pair<const int,SkBitmap> > >),base::WeakPtr<WebAppUninstallDialogViews>,webapps::WebappUninstallSource,std::__1::map<int,SkBitmap,std::__1::less<int>,std::__1::allocator<std::__1::pair<const int,SkBitmap> > > > C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:541
    #4 0x7ffe4d5dab21 in base::internal::Invoker<base::internal::BindState<void (WebAppUninstallDialogViews::*)(webapps::WebappUninstallSource, std::__1::map<int,SkBitmap,std::__1::less<int>,std::__1::allocator<std::__1::pair<const int,SkBitmap> > >),base::WeakPtr<WebAppUninstallDialogViews>,webapps::WebappUninstallSource>,void (std::__1::map<int,SkBitmap,std::__1::less<int>,std::__1::allocator<std::__1::pair<const int,SkBitmap> > >)>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:747
    #5 0x7ffe4346c200 in base::OnceCallback<void (std::__1::map<int,SkBitmap,std::__1::less<int>,std::__1::allocator<std::__1::pair<const int,SkBitmap> > >)>::Run C:\b\s\w\ir\cache\builder\src\base\callback.h:143
    #6 0x7ffe4346229c in web_app::`anonymous namespace'::LogErrorsCallCallback<std::__1::map<int,SkBitmap,std::__1::less<int>,std::__1::allocator<std::__1::pair<const int,SkBitmap> > > > C:\b\s\w\ir\cache\builder\src\chrome\browser\web_applications\web_app_icon_manager.cc:76
    #7 0x7ffe43475c4f in base::internal::Invoker<base::internal::BindState<void (*)(base::WeakPtr<web_app::WebAppIconManager>, base::OnceCallback<void (std::__1::map<int,SkBitmap,std::__1::less<int>,std::__1::allocator<std::__1::pair<const int,SkBitmap> > >)>, web_app::(anonymous namespace)::TypedResult<std::__1::map<int,SkBitmap,std::__1::less<int>,std::__1::allocator<std::__1::pair<const int,SkBitmap> > > >),base::WeakPtr<web_app::WebAppIconManager>,base::OnceCallback<void (std::__1::map<int,SkBitmap,std::__1::less<int>,std::__1::allocator<std::__1::pair<const int,SkBitmap> > >)> >,void (web_app::(anonymous namespace)::TypedResult<std::__1::map<int,SkBitmap,std::__1::less<int>,std::__1::allocator<std::__1::pair<const int,SkBitmap> > > >)>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:747
    #8 0x7ffe43476080 in base::internal::ReplyAdapter<web_app::(anonymous namespace)::TypedResult<std::__1::map<int,SkBitmap,std::__1::less<int>,std::__1::allocator<std::__1::pair<const int,SkBitmap> > > >,web_app::(anonymous namespace)::TypedResult<std::__1::map<int,SkBitmap,std::__1::less<int>,std::__1::allocator<std::__1::pair<const int,SkBitmap> > > > > C:\b\s\w\ir\cache\builder\src\base\task\post_task_and_reply_with_result_internal.h:31
    #9 0x7ffe4347519e in base::internal::Invoker<base::internal::BindState<void (*)(base::OnceCallback<void (gfx::ImageSkia)>, std::__1::unique_ptr<gfx::ImageSkia,std::__1::default_delete<gfx::ImageSkia> > *),base::OnceCallback<void (gfx::ImageSkia)>,base::internal::OwnedWrapper<std::__1::unique_ptr<gfx::ImageSkia,std::__1::default_delete<gfx::ImageSkia> >,std::__1::default_delete<std::__1::unique_ptr<gfx::ImageSkia,std::__1::default_delete<gfx::ImageSkia> > > > >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:747
    #10 0x7ffe4b6b310b in base::`anonymous namespace'::PostTaskAndReplyRelay::RunReply C:\b\s\w\ir\cache\builder\src\base\threading\post_task_and_reply_impl.cc:118
    #11 0x7ffe4b6b3363 in base::internal::Invoker<base::internal::BindState<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay),base::(anonymous namespace)::PostTaskAndReplyRelay>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:747
    #12 0x7ffe4879cd94 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135
    #13 0x7ffe4b6a185d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:422
    #14 0x7ffe4b6a0a5a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:300
    #15 0x7ffe48853db6 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:214
    #16 0x7ffe48852064 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #17 0x7ffe4b6a337a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:542
    #18 0x7ffe48703f57 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:141
    #19 0x7ffe41132b67 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1039
    #20 0x7ffe41137f33 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:157
    #21 0x7ffe4112c0ad in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:30
    #22 0x7ffe482c0e3b in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:660
    #23 0x7ffe482c3fb4 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1167
    #24 0x7ffe482c30e6 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1039
    #25 0x7ffe482bfab3 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:407
    #26 0x7ffe482c023c in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:435
    #27 0x7ffe3ceb14be in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:177

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\ui\views\window\dialog_delegate.cc:434 in views::DialogDelegate::CancelDialog
Shadow bytes around the buggy address:
  0x0447e8c1dca0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0447e8c1dcb0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0447e8c1dcc0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0447e8c1dcd0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0447e8c1dce0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0447e8c1dcf0: fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd
  0x0447e8c1dd00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0447e8c1dd10: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0447e8c1dd20: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0447e8c1dd30: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0447e8c1dd40: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==6380==ABORTING

## Attachments

- [demo.mp4](attachments/demo.mp4) (video/mp4, 15.3 MB)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 15.3 MB)

## Timeline

### [Deleted User] (2022-05-30)

[Empty comment from Monorail migration]

### dr...@chromium.org (2022-05-30)

Do you have any kind of PoC? Any reproduction steps? Without knowing how this stack trace can be triggered, it's pretty much impossible for me to triage it.

### ha...@gmail.com (2022-05-30)

See demo video for repro steps.

### ha...@gmail.com (2022-05-30)

See demo video for repro steps.

### [Deleted User] (2022-05-30)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ct...@chromium.org (2022-05-31)

Hi -- unfortunately the video doesn't give us sufficient details to reproduce this ourselves, especially as this appears to require a specific app to be installed in Chrome. Could you (1) upload the proof-of-concept app you are using in case it is doing something critical to reproducing this, and (2) give a short writeup of the required steps starting from a fresh install of Chrome?

### ha...@gmail.com (2022-05-31)

reproduce step
1.open http://www.google.com and add create shortcut
2.then go to chrome://app-service-internals/  and copy the appid
3.chrome --uninstall-app-id=xxxxxxxxxxxxxxx and cancel
4.UAF trigger

### [Deleted User] (2022-05-31)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ct...@chromium.org (2022-06-01)

Thanks for the repro steps!

This appears to be Windows-only as the flag is only checked at startup on windows  [1]

- Testing on ASAN r992738 (roughly current Windows Stable), able to reproduce.
- Testing on ASAN r1009055 (roughly current Windows Canary), able to reproduce.

I only tested this with explicitly specifying a `--user-data-dir=` because of the comment in [1] about the flag expecting a specific profile dir to be set to avoid the profile picker. It may reproduce without specifying it, but I haven't tested.

Adding the WebAppProvider component and FoundIn-102 (current Windows Stable).

For now, I'm setting this as Security_Severity-Medium: this a browser process UAF, but it requires an webapp to be installed and a nonstandard command-line flag to be used to trigger this particular flow. Medium seems reasonable out of an abundance of caution if this might be reachable from the standard "Uninstall" flow under certain conditions.

dmurph@ could you please take a look? Thanks!

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/startup/startup_browser_creator.cc;l=1083;drc=c355d97ccf0dfddaa792094c1627206633bcd13d

[Monorail components: Platform>WebAppProvider]

### ct...@chromium.org (2022-06-01)

Also, to the reporter: If you have any ideas for how an attacker might be able to exploit this UAF, that would be very useful both for prioritization/triage and for evaluation by the VRP panel :-)

### [Deleted User] (2022-06-01)

[Empty comment from Monorail migration]

### dm...@chromium.org (2022-06-01)

Phillis can you PTAL?

### [Deleted User] (2022-06-01)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ph...@chromium.org (2022-06-02)

[Empty comment from Monorail migration]

### ph...@chromium.org (2022-06-03)

[Empty comment from Monorail migration]

### ph...@chromium.org (2022-06-03)

Submitting the fix.
https://chromium-review.googlesource.com/c/chromium/src/+/3688264

### gi...@appspot.gserviceaccount.com (2022-06-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/40316d774f882abb7308931a7fb4a41790efb6ce

commit 40316d774f882abb7308931a7fb4a41790efb6ce
Author: phillis <phillis@chromium.org>
Date: Fri Jun 03 19:48:44 2022

DPWA: fix UAF on launch --uninstall-app-id

`WebAppUninstallDialogDelegateView` is a `DialogDelegate` and is owned by its widget. It was
triggering a callback on `OnDialogCanceled`.
The callback was passed from `WebAppUiManagerImpl` to release a
`ScopedKeepAlive`, which could trigger a browser shutdown and further
attempts to close the dialog widget, which races with the widget &
delegate's destruction managed by views framework.

The fix removes the redundant and too-early callback call on
`OnDialogCanceled` and only call it on destruction.

Bug: 1330289
Change-Id: I660c0af08a460ce6cedace8d0871dcb925ad9d76
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3688264
Commit-Queue: Phillis Tang <phillis@chromium.org>
Reviewed-by: Chase Phillips <cmp@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1010715}

[modify] https://crrev.com/40316d774f882abb7308931a7fb4a41790efb6ce/chrome/browser/ui/views/web_apps/web_app_uninstall_dialog_view.cc
[modify] https://crrev.com/40316d774f882abb7308931a7fb4a41790efb6ce/chrome/browser/ui/views/web_apps/web_app_uninstall_dialog_browsertest.cc


### ph...@chromium.org (2022-06-03)

[Empty comment from Monorail migration]

### ph...@chromium.org (2022-06-03)

I will test again after it's landed on canary and hopefully get approved and merged on next Monday.

### ct...@chromium.org (2022-06-03)

Thanks for the quick fix! Marking as Fixed so sheriffbot can handle the merge requests and such. (Once you verify on Canary feel free to mark this as "Verified".)

### gi...@appspot.gserviceaccount.com (2022-06-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/918794f0b8c2ebb252994ab2ed3bdeb81a841beb

commit 918794f0b8c2ebb252994ab2ed3bdeb81a841beb
Author: Austin Sullivan <asully@chromium.org>
Date: Fri Jun 03 23:06:52 2022

Revert "DPWA: fix UAF on launch --uninstall-app-id"

This reverts commit 40316d774f882abb7308931a7fb4a41790efb6ce.

Reason for revert: breaking Mac11 bots
https://ci.chromium.org/p/chromium/builders/ci/mac11-arm64-rel-tests

Original change's description:
> DPWA: fix UAF on launch --uninstall-app-id
>
> `WebAppUninstallDialogDelegateView` is a `DialogDelegate` and is owned by its widget. It was
> triggering a callback on `OnDialogCanceled`.
> The callback was passed from `WebAppUiManagerImpl` to release a
> `ScopedKeepAlive`, which could trigger a browser shutdown and further
> attempts to close the dialog widget, which races with the widget &
> delegate's destruction managed by views framework.
>
> The fix removes the redundant and too-early callback call on
> `OnDialogCanceled` and only call it on destruction.
>
> Bug: 1330289
> Change-Id: I660c0af08a460ce6cedace8d0871dcb925ad9d76
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3688264
> Commit-Queue: Phillis Tang <phillis@chromium.org>
> Reviewed-by: Chase Phillips <cmp@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1010715}

Bug: 1330289
Change-Id: I2313e8a2910aedd641b6d17a38fdeee01c021662
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3690028
Commit-Queue: Austin Sullivan <asully@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Owners-Override: Austin Sullivan <asully@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1010785}

[modify] https://crrev.com/918794f0b8c2ebb252994ab2ed3bdeb81a841beb/chrome/browser/ui/views/web_apps/web_app_uninstall_dialog_view.cc
[modify] https://crrev.com/918794f0b8c2ebb252994ab2ed3bdeb81a841beb/chrome/browser/ui/views/web_apps/web_app_uninstall_dialog_browsertest.cc


### [Deleted User] (2022-06-03)

Merge review required: a reverted commit was detected after the merge request.

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

### [Deleted User] (2022-06-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-06-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2e1b03403226861708dd9702a92e0faadb1c99b1

commit 2e1b03403226861708dd9702a92e0faadb1c99b1
Author: Phillis Tang <phillis@google.com>
Date: Sun Jun 05 20:53:10 2022

Reland "DPWA: fix UAF on launch --uninstall-app-id"

This is a reland of commit 40316d774f882abb7308931a7fb4a41790efb6ce

The new test is disabled for mac as there is a problem with parent
browser shutdown in mac testing https://crbug.com/1224161. The fix
here is targeting the usage of `--uninstall-app-id` supported only on
Windows.

Original change's description:
> DPWA: fix UAF on launch --uninstall-app-id
>
> `WebAppUninstallDialogDelegateView` is a `DialogDelegate` and is owned by its widget. It was
> triggering a callback on `OnDialogCanceled`.
> The callback was passed from `WebAppUiManagerImpl` to release a
> `ScopedKeepAlive`, which could trigger a browser shutdown and further
> attempts to close the dialog widget, which races with the widget &
> delegate's destruction managed by views framework.
>
> The fix removes the redundant and too-early callback call on
> `OnDialogCanceled` and only call it on destruction.
>
> Bug: 1330289
> Change-Id: I660c0af08a460ce6cedace8d0871dcb925ad9d76
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3688264
> Commit-Queue: Phillis Tang <phillis@chromium.org>
> Reviewed-by: Chase Phillips <cmp@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1010715}

Bug: 1330289
Change-Id: I36eb12258374bac1687f0d836f502160ddb0eb30
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3690231
Commit-Queue: Dibyajyoti Pal <dibyapal@chromium.org>
Reviewed-by: Dibyajyoti Pal <dibyapal@chromium.org>
Auto-Submit: Phillis Tang <phillis@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1010856}

[modify] https://crrev.com/2e1b03403226861708dd9702a92e0faadb1c99b1/chrome/browser/ui/views/web_apps/web_app_uninstall_dialog_view.cc
[modify] https://crrev.com/2e1b03403226861708dd9702a92e0faadb1c99b1/chrome/browser/ui/views/web_apps/web_app_uninstall_dialog_browsertest.cc


### ph...@chromium.org (2022-06-06)



Please answer the following questions so that we can safely process your merge request:
1. Security bug
2. https://chromium-review.googlesource.com/c/chromium/src/+/3690231
3. yes
4. no
5. n/a
6. no

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2022-06-06)

+adetaylor@ and amy@ Security TPM's for merge decision.

### pb...@google.com (2022-06-06)

[Empty comment from Monorail migration]

### ph...@chromium.org (2022-06-08)

adetaylor@ gentle ping on this

### ad...@chromium.org (2022-06-08)

As far as I can see, there is no great urgency for this merge decision since we are aiming at M103 not an M102 refresh. We therefore prefer to have lots of bake time before merging, and it's intentional we haven't replied yet. Specifically Amy will reply but is currently travelling for work. HTH!

### ph...@chromium.org (2022-06-09)

Got it, thanks for explaining the process!

### ph...@chromium.org (2022-06-09)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-06-13)

Hello, merge approved for M103, please merge this fix to branch 5060 as soon as possible and NLT 10am PST tomorrow, Tuesday, 14 June so this fix can be in the stable cut for M103 -- thank you! 

### am...@google.com (2022-06-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### gi...@appspot.gserviceaccount.com (2022-06-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8941fc31a920e57e8b3fd847d45bcb6b33e307fb

commit 8941fc31a920e57e8b3fd847d45bcb6b33e307fb
Author: Phillis Tang <phillis@google.com>
Date: Mon Jun 13 18:12:58 2022

Reland "DPWA: fix UAF on launch --uninstall-app-id"

This is a reland of commit 40316d774f882abb7308931a7fb4a41790efb6ce

The new test is disabled for mac as there is a problem with parent
browser shutdown in mac testing https://crbug.com/1224161. The fix
here is targeting the usage of `--uninstall-app-id` supported only on
Windows.

Original change's description:
> DPWA: fix UAF on launch --uninstall-app-id
>
> `WebAppUninstallDialogDelegateView` is a `DialogDelegate` and is owned by its widget. It was
> triggering a callback on `OnDialogCanceled`.
> The callback was passed from `WebAppUiManagerImpl` to release a
> `ScopedKeepAlive`, which could trigger a browser shutdown and further
> attempts to close the dialog widget, which races with the widget &
> delegate's destruction managed by views framework.
>
> The fix removes the redundant and too-early callback call on
> `OnDialogCanceled` and only call it on destruction.
>
> Bug: 1330289
> Change-Id: I660c0af08a460ce6cedace8d0871dcb925ad9d76
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3688264
> Commit-Queue: Phillis Tang <phillis@chromium.org>
> Reviewed-by: Chase Phillips <cmp@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1010715}

(cherry picked from commit 2e1b03403226861708dd9702a92e0faadb1c99b1)

Bug: 1330289
Change-Id: I36eb12258374bac1687f0d836f502160ddb0eb30
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3690231
Commit-Queue: Dibyajyoti Pal <dibyapal@chromium.org>
Reviewed-by: Dibyajyoti Pal <dibyapal@chromium.org>
Auto-Submit: Phillis Tang <phillis@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1010856}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3691820
Commit-Queue: Phillis Tang <phillis@chromium.org>
Cr-Commit-Position: refs/branch-heads/5060@{#791}
Cr-Branched-From: b83393d0f4038aeaf67f970a024d8101df7348d1-refs/heads/main@{#1002911}

[modify] https://crrev.com/8941fc31a920e57e8b3fd847d45bcb6b33e307fb/chrome/browser/ui/views/web_apps/web_app_uninstall_dialog_view.cc
[modify] https://crrev.com/8941fc31a920e57e8b3fd847d45bcb6b33e307fb/chrome/browser/ui/views/web_apps/web_app_uninstall_dialog_browsertest.cc


### am...@chromium.org (2022-06-13)

Congratulations! The VRP Panel has decided to award you $3,000 for this report based on the mitigations of this issue not being web accessible and requiring sufficient user interaction. Thank you for your efforts and reporting this issue to us! 

### am...@chromium.org (2022-06-13)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-06-14)

credit: Zhihua Yao of Kunlun Lab

### am...@google.com (2022-06-16)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-06-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-06-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2023-08-25)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1330289?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059795)*
