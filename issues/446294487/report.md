# heap-use-after-free C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\page_info\page_info_infobar_dele

| Field | Value |
|-------|-------|
| **Issue ID** | [446294487](https://issues.chromium.org/issues/446294487) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Bubbles>PageInfo |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 142.0.0.0 |
| **Reporter** | pu...@gmail.com |
| **Assignee** | fm...@google.com |
| **Created** | 2025-09-20 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

1. i will be updating soon

# Problem Description

=================================================================
==11072==ERROR: AddressSanitizer: heap-use-after-free on address 0x11f90ac4a4f0 at pc 0x7ffdc8b6a9fc bp 0x0021f1ffab70 sp 0x0021f1ffabb8
WRITE of size 4 at 0x11f90ac4a4f0 thread T0
#0 0x7ffdc8b6a9fb in PageInfoInfoBarDelegate::set\_reload\_type C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\page\_info\page\_info\_infobar\_delegate.h:31
#1 0x7ffdc8b6a9fb in ChromePageInfoDelegate::CreateInfoBarDelegate(enum content::ReloadType) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\page\_info\chrome\_page\_info\_delegate.cc:226:15
#2 0x7ffde101ffb0 in PageInfo::OnUIClosing(bool *) C:\b\s\w\ir\cache\builder\src\components\page\_info\page\_info.cc:796:20
#3 0x7ffdc94f5841 in PageInfoBubbleView::OnWidgetDestroying(class views::Widget *) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\page\_info\page\_info\_bubble\_view.cc:352:17
#4 0x7ffdcaecbb91 in std::\_\_Cr::\_\_invoke C:\b\s\w\ir\cache\builder\src\third\_party\libc++\src\include\_\_type\_traits\invoke.h:203
#5 0x7ffdcaecbb91 in std::\_\_Cr::invoke C:\b\s\w\ir\cache\builder\src\third\_party\libc++\src\include\_\_functional\invoke.h:29
#6 0x7ffdcaecbb91 in base::ObserverList<class views::WidgetObserver, 0, 1, class base::internal::CheckedObserverAdapter>::Notify<void (\_\_cdecl views::WidgetObserver::*)(class views::Widget *), class views::Widget *>(void (\_\_cdecl views::WidgetObserver::*)(class views::Widget *), class views::Widget *const &) C:\b\s\w\ir\cache\builder\src\base\observer\_list.h:398:7
#7 0x7ffdcaec04ab in views::Widget::HandleWidgetDestroying(void) C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:2719:14
#8 0x7ffdcadeff52 in views::DesktopWindowTreeHostWin::HandleDestroying(void) C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_window\_tree\_host\_win.cc:1052:30
#9 0x7ffdcae80324 in views::HWNDMessageHandler::OnDestroy(void) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:1891:14
#10 0x7ffdcae74182 in views::HWNDMessageHandler::*ProcessWindowMessage(struct HWND*\_*, unsigned int, unsigned \_\_int64, \_\_int64, \_\_int64 &, unsigned long) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.h:468:5
#11 0x7ffdcae7151d in views::HWNDMessageHandler::OnWndProc(unsigned int, unsigned \_\_int64, **int64) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:1178:7
#12 0x7ffdcf592d7c in gfx::WindowImpl::WndProc(struct HWND***, unsigned int, unsigned \_\_int64, **int64) C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window\_impl.cc:313:18
#13 0x7ffdcf59185e in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc(struct HWND***, unsigned int, unsigned \_\_int64, **int64)>(struct HWND***, unsigned int, unsigned \_\_int64, \_\_int64) C:\b\s\w\ir\cache\builder\src\base\win\wrapped\_window\_proc.h:74:10
#14 0x7ffedc787cf5 (C:\WINDOWS\System32\USER32.dll+0x180017cf5)
#15 0x7ffedc78757b (C:\WINDOWS\System32\USER32.dll+0x18001757b)
#16 0x7ffedc7b8562 (C:\WINDOWS\System32\USER32.dll+0x180048562)
#17 0x7ffeddb47253 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180167253)
#18 0x7ffedb182543 (C:\WINDOWS\System32\win32u.dll+0x180002543)
#19 0x7ffdcae8c07f in base::internal::DecayedFunctorTraits<void (HWNDMessageHandler::*)(),base::WeakPtr[views::HWNDMessageHandler](javascript:void(0);) &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:731
#20 0x7ffdcae8c07f in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (HWNDMessageHandler::*&&)(),base::WeakPtr[views::HWNDMessageHandler](javascript:void(0);) &&>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:947
#21 0x7ffdcae8c07f in base::internal::Invoker<base::internal::FunctorTraits<void (HWNDMessageHandler::*&&)(),base::WeakPtr[views::HWNDMessageHandler](javascript:void(0);) &&>,base::internal::BindState<1,1,0,void (HWNDMessageHandler::*)(),base::WeakPtr[views::HWNDMessageHandler](javascript:void(0);) >,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:1060
#22 0x7ffdcae8c07f in base::internal::Invoker<struct base::internal::FunctorTraits<void (\_\_cdecl views::HWNDMessageHandler::*&&)(void), class base::WeakPtr<class views::HWNDMessageHandler> &&>, struct base::internal::BindState<1, 1, 0, void (\_\_cdecl views::HWNDMessageHandler::*)(void), class base::WeakPtr<class views::HWNDMessageHandler>>, (void)>::RunOnce(class base::internal::BindStateBase \*) C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:973:12
#23 0x7ffdcc859cb3 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
#24 0x7ffdcc859cb3 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:207:34
#25 0x7ffdcc82ceb9 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.h:104
#26 0x7ffdcc82ceb9 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow \*) C:\b\s\

# Summary

heap-use-after-free C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\page\_info\page\_info\_infobar\_dele

# Custom Questions

#### Reporter credit:

Puf

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 24.5 KB)
- deleted (application/octet-stream, 0 B)
- [ufff.mp4](attachments/ufff.mp4) (video/mp4, 1.1 MB)
- deleted (application/octet-stream, 0 B)
- [Repro.mp4](attachments/Repro.mp4) (video/mp4, 1.1 MB)

## Timeline

### pu...@gmail.com (2025-09-20)

```
ERROR: AddressSanitizer: heap-use-after-free on address 0x11f90ac4a4f0 at pc 0x7ffdc8b6a9fc bp 0x0021f1ffab70 sp 0x0021f1ffabb8
WRITE of size 4 at 0x11f90ac4a4f0 thread T0
    #0 0x7ffdc8b6a9fb in PageInfoInfoBarDelegate::set_reload_type C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\page_info\page_info_infobar_delegate.h:31
    #1 0x7ffdc8b6a9fb in ChromePageInfoDelegate::CreateInfoBarDelegate(enum content::ReloadType) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\page_info\chrome_page_info_delegate.cc:226:15
    #2 0x7ffde101ffb0 in PageInfo::OnUIClosing(bool *) C:\b\s\w\ir\cache\builder\src\components\page_info\page_info.cc:796:20
    #3 0x7ffdc94f5841 in PageInfoBubbleView::OnWidgetDestroying(class views::Widget *) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\page_info\page_info_bubble_view.cc:352:17
    #4 0x7ffdcaecbb91 in std::__Cr::__invoke C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__type_traits\invoke.h:203
    #5 0x7ffdcaecbb91 in std::__Cr::invoke C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__functional\invoke.h:29
    #6 0x7ffdcaecbb91 in base::ObserverList<class views::WidgetObserver, 0, 1, class base::internal::CheckedObserverAdapter>::Notify<void (__cdecl views::WidgetObserver::*)(class views::Widget *), class views::Widget *>(void (__cdecl views::WidgetObserver::*)(class views::Widget *), class views::Widget *const &) C:\b\s\w\ir\cache\builder\src\base\observer_list.h:398:7
    #7 0x7ffdcaec04ab in views::Widget::HandleWidgetDestroying(void) C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:2719:14
    #8 0x7ffdcadeff52 in views::DesktopWindowTreeHostWin::HandleDestroying(void) C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_window_tree_host_win.cc:1052:30
    #9 0x7ffdcae80324 in views::HWNDMessageHandler::OnDestroy(void) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:1891:14
    #10 0x7ffdcae74182 in views::HWNDMessageHandler::_ProcessWindowMessage(struct HWND__*, unsigned int, unsigned __int64, __int64, __int64 &, unsigned long) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.h:468:5
    #11 0x7ffdcae7151d in views::HWNDMessageHandler::OnWndProc(unsigned int, unsigned __int64, __int64) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:1178:7
    #12 0x7ffdcf592d7c in gfx::WindowImpl::WndProc(struct HWND__*, unsigned int, unsigned __int64, __int64) C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window_impl.cc:313:18
    #13 0x7ffdcf59185e in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc(struct HWND__*, unsigned int, unsigned __int64, __int64)>(struct HWND__*, unsigned int, unsigned __int64, __int64) C:\b\s\w\ir\cache\builder\src\base\win\wrapped_window_proc.h:74:10
    #14 0x7ffedc787cf5  (C:\WINDOWS\System32\USER32.dll+0x180017cf5)
    #15 0x7ffedc78757b  (C:\WINDOWS\System32\USER32.dll+0x18001757b)
    #16 0x7ffedc7b8562  (C:\WINDOWS\System32\USER32.dll+0x180048562)
    #17 0x7ffeddb47253  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180167253)
    #18 0x7ffedb182543  (C:\WINDOWS\System32\win32u.dll+0x180002543)
    #19 0x7ffdcae8c07f in base::internal::DecayedFunctorTraits<void (HWNDMessageHandler::*)(),base::WeakPtr<views::HWNDMessageHandler> &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:731
    #20 0x7ffdcae8c07f in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (HWNDMessageHandler::*&&)(),base::WeakPtr<views::HWNDMessageHandler> &&>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:947
    #21 0x7ffdcae8c07f in base::internal::Invoker<base::internal::FunctorTraits<void (HWNDMessageHandler::*&&)(),base::WeakPtr<views::HWNDMessageHandler> &&>,base::internal::BindState<1,1,0,void (HWNDMessageHandler::*)(),base::WeakPtr<views::HWNDMessageHandler> >,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1060
    #22 0x7ffdcae8c07f in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl views::HWNDMessageHandler::*&&)(void), class base::WeakPtr<class views::HWNDMessageHandler> &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl views::HWNDMessageHandler::*)(void), class base::WeakPtr<class views::HWNDMessageHandler>>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:973:12
    #23 0x7ffdcc859cb3 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
    #24 0x7ffdcc859cb3 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:207:34
    #25 0x7ffdcc82ceb9 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:104
    #26 0x7ffdcc82ceb9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:465:23
    #27 0x7ffdcc82bd5f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:339:40
    #28 0x7ffdcc6c8760 in base::MessagePumpForUI::DoRunLoop(void) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:260:67
    #29 0x7ffdcc6c6128 in base::MessagePumpWin::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:87:3
    #30 0x7ffdcc82ebf1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:638:12
    #31 0x7ffdcc8cb8be in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134:14
    #32 0x7ffdc28a4bcd in content::BrowserMainLoop::RunMainMessageLoop(void) C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1109:18
    #33 0x7ffdc28ac849 in content::BrowserMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:156:15
    #34 0x7ffdc289b3ec in content::BrowserMain(struct content::MainFunctionParams) C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:32:28
    #35 0x7ffdc8bd6e82 in content::RunBrowserProcessMain(struct content::MainFunctionParams, class content::ContentMainDelegate *) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:701:10
    #36 0x7ffdc8bd9fcf in content::ContentMainRunnerImpl::RunBrowser(struct content::MainFunctionParams, bool) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1278:10
    #37 0x7ffdc8bd97de in content::ContentMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1127:12
    #38 0x7ffdc8bcd6b8 in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:361:36
    #39 0x7ffdc8bce27d in content::ContentMain(struct content::ContentMainParams) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:374:10
    #40 0x7ffdb98b2b0b in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:222:12
    #41 0x7ff75c55479b in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:201:12
    #42 0x7ff75c55200c in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:352:20
    #43 0x7ff75ca0f77b in invoke_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #44 0x7ff75ca0f77b in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #45 0x7ffedc26e8d6  (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #46 0x7ffedd9e8d9b  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180008d9b)

0x11f90ac4a4f0 is located 80 bytes inside of 88-byte region [0x11f90ac4a4a0,0x11f90ac4a4f8)
freed by thread T0 here:
    #0 0x7ffe4defc584  (D:\win64-release_d8-asan-win64-release-v8-component-100000\clang_rt.asan_dynamic-x86_64.dll+0x18005c584)
    #1 0x7ffdc8b71050 in PageInfoInfoBarDelegate::`scalar deleting dtor'(unsigned int) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\page_info\page_info_infobar_delegate.cc:30:51
    #2 0x7ffdd5563f0b in std::__Cr::default_delete<infobars::InfoBarDelegate>::operator() C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:77
    #3 0x7ffdd5563f0b in std::__Cr::unique_ptr<infobars::InfoBarDelegate,std::__Cr::default_delete<infobars::InfoBarDelegate> >::reset C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:290
    #4 0x7ffdd5563f0b in std::__Cr::unique_ptr<infobars::InfoBarDelegate,std::__Cr::default_delete<infobars::InfoBarDelegate> >::~unique_ptr C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:259
    #5 0x7ffdd5563f0b in infobars::InfoBar::~InfoBar(void) C:\b\s\w\ir\cache\builder\src\components\infobars\core\infobar.cc:38:1
    #6 0x7ffdc9b49f73 in ConfirmInfoBar::~ConfirmInfoBar C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\infobars\confirm_infobar.cc:74
    #7 0x7ffdc9b49f73 in ConfirmInfoBar::`scalar deleting dtor'(unsigned int) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\infobars\confirm_infobar.cc:74:33
    #8 0x7ffdd555d85e in std::__Cr::default_delete<infobars::InfoBar>::operator() C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:77
    #9 0x7ffdd555d85e in std::__Cr::unique_ptr<infobars::InfoBar,std::__Cr::default_delete<infobars::InfoBar> >::reset C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:290
    #10 0x7ffdd555d85e in std::__Cr::unique_ptr<infobars::InfoBar,std::__Cr::default_delete<infobars::InfoBar> >::~unique_ptr C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:259
    #11 0x7ffdd555d85e in infobars::InfoBarManager::AddInfoBarInternal(class std::__Cr::unique_ptr<class infobars::InfoBar, struct std::__Cr::default_delete<class infobars::InfoBar>>, bool) C:\b\s\w\ir\cache\builder\src\components\infobars\core\infobar_manager.cc:77:1
    #12 0x7ffdc8b70db1 in infobars::InfoBarManager::AddInfoBar C:\b\s\w\ir\cache\builder\src\components\infobars\core\infobar_manager.h:64
    #13 0x7ffdc8b70db1 in PageInfoInfoBarDelegate::Create(class infobars::ContentInfoBarManager *) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\page_info\page_info_infobar_delegate.cc:23:20
    #14 0x7ffdc8b6a9c5 in ChromePageInfoDelegate::CreateInfoBarDelegate(enum content::ReloadType) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\page_info\chrome_page_info_delegate.cc:225:22
    #15 0x7ffde101ffb0 in PageInfo::OnUIClosing(bool *) C:\b\s\w\ir\cache\builder\src\components\page_info\page_info.cc:796:20
    #16 0x7ffdc94f5841 in PageInfoBubbleView::OnWidgetDestroying(class views::Widget *) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\page_info\page_info_bubble_view.cc:352:17
    #17 0x7ffdcaecbb91 in std::__Cr::__invoke C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__type_traits\invoke.h:203
    #18 0x7ffdcaecbb91 in std::__Cr::invoke C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__functional\invoke.h:29
    #19 0x7ffdcaecbb91 in base::ObserverList<class views::WidgetObserver, 0, 1, class base::internal::CheckedObserverAdapter>::Notify<void (__cdecl views::WidgetObserver::*)(class views::Widget *), class views::Widget *>(void (__cdecl views::WidgetObserver::*)(class views::Widget *), class views::Widget *const &) C:\b\s\w\ir\cache\builder\src\base\observer_list.h:398:7
    #20 0x7ffdcaec04ab in views::Widget::HandleWidgetDestroying(void) C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:2719:14
    #21 0x7ffdcadeff52 in views::DesktopWindowTreeHostWin::HandleDestroying(void) C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_window_tree_host_win.cc:1052:30
    #22 0x7ffdcae80324 in views::HWNDMessageHandler::OnDestroy(void) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:1891:14
    #23 0x7ffdcae74182 in views::HWNDMessageHandler::_ProcessWindowMessage(struct HWND__*, unsigned int, unsigned __int64, __int64, __int64 &, unsigned long) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.h:468:5
    #24 0x7ffdcae7151d in views::HWNDMessageHandler::OnWndProc(unsigned int, unsigned __int64, __int64) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:1178:7
    #25 0x7ffdcf592d7c in gfx::WindowImpl::WndProc(struct HWND__*, unsigned int, unsigned __int64, __int64) C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window_impl.cc:313:18
    #26 0x7ffdcf59185e in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc(struct HWND__*, unsigned int, unsigned __int64, __int64)>(struct HWND__*, unsigned int, unsigned __int64, __int64) C:\b\s\w\ir\cache\builder\src\base\win\wrapped_window_proc.h:74:10
    #27 0x7ffedc787cf5  (C:\WINDOWS\System32\USER32.dll+0x180017cf5)
    #28 0x7ffedc78757b  (C:\WINDOWS\System32\USER32.dll+0x18001757b)
    #29 0x7ffedc7b8562  (C:\WINDOWS\System32\USER32.dll+0x180048562)
    #30 0x7ffeddb47253  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180167253)
    #31 0x7ffedb182543  (C:\WINDOWS\System32\win32u.dll+0x180002543)
    #32 0x7ffdcae8c07f in base::internal::DecayedFunctorTraits<void (HWNDMessageHandler::*)(),base::WeakPtr<views::HWNDMessageHandler> &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:731
    #33 0x7ffdcae8c07f in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (HWNDMessageHandler::*&&)(),base::WeakPtr<views::HWNDMessageHandler> &&>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:947
    #34 0x7ffdcae8c07f in base::internal::Invoker<base::internal::FunctorTraits<void (HWNDMessageHandler::*&&)(),base::WeakPtr<views::HWNDMessageHandler> &&>,base::internal::BindState<1,1,0,void (HWNDMessageHandler::*)(),base::WeakPtr<views::HWNDMessageHandler> >,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1060
    #35 0x7ffdcae8c07f in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl views::HWNDMessageHandler::*&&)(void), class base::WeakPtr<class views::HWNDMessageHandler> &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl views::HWNDMessageHandler::*)(void), class base::WeakPtr<class views::HWNDMessageHandler>>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:973:12
    #36 0x7ffdcc859cb3 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
    #37 0x7ffdcc859cb3 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:207:34
    #38 0x7ffdcc82ceb9 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:104
    #39 0x7ffdcc82ceb9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:465:23
    #40 0x7ffdcc82bd5f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:339:40
    #41 0x7ffdcc6c8760 in base::MessagePumpForUI::DoRunLoop(void) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:260:67
    #42 0x7ffdcc6c6128 in base::MessagePumpWin::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:87:3

previously allocated by thread T0 here:
    #0 0x7ffe4defb99d  (D:\win64-release_d8-asan-win64-release-v8-component-100000\clang_rt.asan_dynamic-x86_64.dll+0x18005b99d)
    #1 0x7ffdc8b70d10 in PageInfoInfoBarDelegate::Create(class infobars::ContentInfoBarManager *) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\page_info\page_info_infobar_delegate.cc:22:20
    #2 0x7ffdc8b6a9c5 in ChromePageInfoDelegate::CreateInfoBarDelegate(enum content::ReloadType) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\page_info\chrome_page_info_delegate.cc:225:22
    #3 0x7ffde101ffb0 in PageInfo::OnUIClosing(bool *) C:\b\s\w\ir\cache\builder\src\components\page_info\page_info.cc:796:20
    #4 0x7ffdc94f5841 in PageInfoBubbleView::OnWidgetDestroying(class views::Widget *) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\page_info\page_info_bubble_view.cc:352:17
    #5 0x7ffdcaecbb91 in std::__Cr::__invoke C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__type_traits\invoke.h:203
    #6 0x7ffdcaecbb91 in std::__Cr::invoke C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__functional\invoke.h:29
    #7 0x7ffdcaecbb91 in base::ObserverList<class views::WidgetObserver, 0, 1, class base::internal::CheckedObserverAdapter>::Notify<void (__cdecl views::WidgetObserver::*)(class views::Widget *), class views::Widget *>(void (__cdecl views::WidgetObserver::*)(class views::Widget *), class views::Widget *const &) C:\b\s\w\ir\cache\builder\src\base\observer_list.h:398:7
    #8 0x7ffdcaec04ab in views::Widget::HandleWidgetDestroying(void) C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:2719:14
    #9 0x7ffdcadeff52 in views::DesktopWindowTreeHostWin::HandleDestroying(void) C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_window_tree_host_win.cc:1052:30
    #10 0x7ffdcae80324 in views::HWNDMessageHandler::OnDestroy(void) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:1891:14
    #11 0x7ffdcae74182 in views::HWNDMessageHandler::_ProcessWindowMessage(struct HWND__*, unsigned int, unsigned __int64, __int64, __int64 &, unsigned long) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.h:468:5
    #12 0x7ffdcae7151d in views::HWNDMessageHandler::OnWndProc(unsigned int, unsigned __int64, __int64) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:1178:7
    #13 0x7ffdcf592d7c in gfx::WindowImpl::WndProc(struct HWND__*, unsigned int, unsigned __int64, __int64) C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window_impl.cc:313:18
    #14 0x7ffdcf59185e in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc(struct HWND__*, unsigned int, unsigned __int64, __int64)>(struct HWND__*, unsigned int, unsigned __int64, __int64) C:\b\s\w\ir\cache\builder\src\base\win\wrapped_window_proc.h:74:10
    #15 0x7ffedc787cf5  (C:\WINDOWS\System32\USER32.dll+0x180017cf5)
    #16 0x7ffedc78757b  (C:\WINDOWS\System32\USER32.dll+0x18001757b)
    #17 0x7ffedc7b8562  (C:\WINDOWS\System32\USER32.dll+0x180048562)
    #18 0x7ffeddb47253  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180167253)
    #19 0x7ffedb182543  (C:\WINDOWS\System32\win32u.dll+0x180002543)
    #20 0x7ffdcae8c07f in base::internal::DecayedFunctorTraits<void (HWNDMessageHandler::*)(),base::WeakPtr<views::HWNDMessageHandler> &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:731
    #21 0x7ffdcae8c07f in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (HWNDMessageHandler::*&&)(),base::WeakPtr<views::HWNDMessageHandler> &&>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:947
    #22 0x7ffdcae8c07f in base::internal::Invoker<base::internal::FunctorTraits<void (HWNDMessageHandler::*&&)(),base::WeakPtr<views::HWNDMessageHandler> &&>,base::internal::BindState<1,1,0,void (HWNDMessageHandler::*)(),base::WeakPtr<views::HWNDMessageHandler> >,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1060
    #23 0x7ffdcae8c07f in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl views::HWNDMessageHandler::*&&)(void), class base::WeakPtr<class views::HWNDMessageHandler> &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl views::HWNDMessageHandler::*)(void), class base::WeakPtr<class views::HWNDMessageHandler>>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:973:12
    #24 0x7ffdcc859cb3 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
    #25 0x7ffdcc859cb3 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:207:34
    #26 0x7ffdcc82ceb9 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:104
    #27 0x7ffdcc82ceb9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:465:23
    #28 0x7ffdcc82bd5f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:339:40
    #29 0x7ffdcc6c8760 in base::MessagePumpForUI::DoRunLoop(void) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:260:67
    #30 0x7ffdcc6c6128 in base::MessagePumpWin::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:87:3
    #31 0x7ffdcc82ebf1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:638:12
    #32 0x7ffdcc8cb8be in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134:14
    #33 0x7ffdc28a4bcd in content::BrowserMainLoop::RunMainMessageLoop(void) C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1109:18
    #34 0x7ffdc28ac849 in content::BrowserMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:156:15

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\page_info\page_info_infobar_delegate.h:31 in PageInfoInfoBarDelegate::set_reload_type
Shadow bytes around the buggy address:
  0x11f90ac4a200: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x11f90ac4a280: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x11f90ac4a300: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x11f90ac4a380: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x11f90ac4a400: fa fa f7 fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x11f90ac4a480: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd[fd]fa
  0x11f90ac4a500: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x11f90ac4a580: fa fa f7 fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x11f90ac4a600: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x11f90ac4a680: fa fa f7 fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x11f90ac4a700: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
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

==11072==ADDITIONAL INFO

==11072==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffdcae698f0 in views::HWNDMessageHandler::Close(void) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:519:9
    #1 0x7ffdd1b69b4c in cc::SingleThreadProxy::ScheduledActionSendBeginMainFrame(struct viz::BeginFrameArgs const &) C:\b\s\w\ir\cache\builder\src\cc\trees\single_thread_proxy.cc:1058:7
    #2 0x7ffdccd70e78 in mojo::SimpleWatcher::Context::Notify(unsigned int, struct MojoHandleSignalsState, unsigned int) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc:102:13


Command line: `chrome.exe --flag-switches-begin --flag-switches-end --file-url-path-alias="/gen=D:\win64-release_d8-asan-win64-release-v8-component-100000\gen"`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==11072==END OF ADDITIONAL INFO
==11072==ABORTING

```

### pu...@gmail.com (2025-09-21)

AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\page\_info\page\_info\_infobar\_delegate.h:31 in PageInfoInfoBarDelegate::set\_reload\_type

The bug is located in the code that handles the Page Info UI (the pop-up that appears when you click the lock icon in the address bar to view site security, permissions, etc.).

This bug is triggered by a common user action (closing a UI element).
during the process of closing the Page Info dialog.

NOT PROTECTED by MiraclePtr,

**Steps to reproduce the problem**

1. Open poc.html in Chrome & Click the button.
2. A permission prompt will appear (select "Allow" or "Block").
3. Open the site information Icon
4. Click Reset permission , then close the dialog box.
5. Open the site information panel again.
6. Locate the permission and select Allow.
7. Close the panel or click anywhere on the screen

The UAF will be triggered

**VERSION**

Verified Version 141.0.7344.0 (Developer Build)

Verified Version 141.0.7390.30 (Beta)

**Type of crash:**

browser

**Crash state:**

See asan

### dr...@chromium.org (2025-09-22)

[security triage] I can reproduce this in M140. But I found the user gestures fairly difficult to follow. The crucial thing is that you modify the permission again after getting the "reload this page" infobar. A browser-process UAF is typically Critical severity, but the weird user gestures here downgrade us to High. Setting High severity and Found-In 140.

### dr...@chromium.org (2025-09-22)

Triaging to some page\_info owners. I'm not entirely clear if the root cause is in page info or in infobars, so feel free to reassign if I've guessed incorrectly.

### ch...@google.com (2025-09-23)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-09-23)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pu...@gmail.com (2025-09-30)

Hi , Friendly ping

### ei...@google.com (2025-10-05)

looks like this was introduced in https://chromium-review.googlesource.com/c/chromium/src/+/6766553

### dx...@google.com (2025-10-07)

Project: chromium/src  

Branch:  main  

Author:  Fiona Macintosh [fmacintosh@google.com](mailto:fmacintosh@google.com)  

Link:    <https://chromium-review.googlesource.com/7008715>

[Page Info] Fix use-after-free in infobar delegate

---


Expand for full commit details
```
     
    Bug: 446294487 
    Change-Id: Ica9a2077b88c019664b498f03d162802d44c7049 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7008715 
    Auto-Submit: Fiona Macintosh <fmacintosh@google.com> 
    Reviewed-by: Christian Dullweber <dullweber@chromium.org> 
    Commit-Queue: Fiona Macintosh <fmacintosh@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1526366}

```

---

Files:

- M `chrome/browser/ui/page_info/chrome_page_info_delegate.cc`
- M `chrome/browser/ui/page_info/page_info_infobar_delegate.cc`
- M `chrome/browser/ui/page_info/page_info_infobar_delegate.h`

---

Hash: [90a4060a92d135f1789056c943cf7e535fa8603b](https://chromiumdash.appspot.com/commit/90a4060a92d135f1789056c943cf7e535fa8603b)  

Date: Tue Oct 7 16:57:32 2025


---

### ch...@google.com (2025-10-09)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: andywu (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2025-10-09)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2025-10-09)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### fm...@google.com (2025-10-09)

1. Merge is for high severity security bug
2. Requesting to merge <https://chromium-review.googlesource.com/c/chromium/src/+/7008715>
3. Yes
4. Not a new feature
5. No, this doesn't seem relevant
6. Manual testing not required

### ts...@google.com (2025-10-09)

I'm going to reject a merge to m141 to avoid disrupting stable, as the steps involved to reproduce require significant user interaction, and the window between the free and the use is tight and does not provide a lot of opportunity for attacker control.
Please merge to m142 beta (7444) by Tues 11-Oct.

### dx...@google.com (2025-10-09)

Project: chromium/src  

Branch:  refs/branch-heads/7444  

Author:  Fiona Macintosh [fmacintosh@google.com](mailto:fmacintosh@google.com)  

Link:    <https://chromium-review.googlesource.com/7028311>

[Page Info] Fix use-after-free in infobar delegate

---


Expand for full commit details
```
     
    (cherry picked from commit 90a4060a92d135f1789056c943cf7e535fa8603b) 
     
    Bug: 446294487 
    Change-Id: Ica9a2077b88c019664b498f03d162802d44c7049 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7008715 
    Auto-Submit: Fiona Macintosh <fmacintosh@google.com> 
    Reviewed-by: Christian Dullweber <dullweber@chromium.org> 
    Commit-Queue: Fiona Macintosh <fmacintosh@google.com> 
    Cr-Original-Commit-Position: refs/heads/main@{#1526366} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7028311 
    Commit-Queue: Christian Dullweber <dullweber@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7444@{#629} 
    Cr-Branched-From: 29907d3c18078029695f458b42fb8e6fda3e493d-refs/heads/main@{#1522585}

```

---

Files:

- M `chrome/browser/ui/page_info/chrome_page_info_delegate.cc`
- M `chrome/browser/ui/page_info/page_info_infobar_delegate.cc`
- M `chrome/browser/ui/page_info/page_info_infobar_delegate.h`

---

Hash: [1e95f134b92524b1c136afe7323a89020cba11d8](https://chromiumdash.appspot.com/commit/1e95f134b92524b1c136afe7323a89020cba11d8)  

Date: Thu Oct 9 18:05:43 2025


---

### pe...@google.com (2025-10-09)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### fm...@google.com (2025-10-09)

Not applicable for merge into M138 as the issue was introduced in M140 and a fix has been merged into M142

### sp...@google.com (2025-10-17)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
highly mitigated memory corruption in a non-sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-01-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/446294487)*
