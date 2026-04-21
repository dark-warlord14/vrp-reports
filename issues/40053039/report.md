# Security: UaF in views::View::UpdateTooltip

| Field | Value |
|-------|-------|
| **Issue ID** | [40053039](https://issues.chromium.org/issues/40053039) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Payments |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | sa...@chromium.org |
| **Created** | 2020-08-10 |
| **Bounty** | $5,000.00 |

## Description

**VERSION**  

Chrome Version: 86.0.4228.0 (Official Build) canary (x86\_64)  

Operating System: MacOS and Windows

**REPRODUCTION CASE**

1. Go to <https://skilful-reserve-239412.appspot.com/static/apps/max-nonbasiccard/>, click install
2. Go to <https://maxlgu.github.io/pr/max-nonbasiccard/>
3. Click on Buy
4. In payment dialog try to change <http://www.google.com> to <https://lbstyle.github.io/o.html> then click on "Go!" button
5. Click on "Cancel" button

crash/7319f7b352e44b58.

rax=000001f7e5bc0a80 rbx=0000000000000000 rcx=000001f7e34ae8a0  

rdx=000001f7e5eb2401 rsi=000001f7e34ae8a0 rdi=000001f7e5eb2490  

rip=00007ffd77e21e5f rsp=000000eca27fcd30 rbp=000001f7e5cd8180  

r8=000001f7e5904e00 r9=0000000000000001 r10=000001f7e5f70310  

r11=000001f7e560d240 r12=0000000000000000 r13=000001f7dcf20680  

r14=000001f7e5b61860 r15=0000000000000001  

iopl=0 nv up ei pl zr na po nc  

cs=0033 ss=002b ds=002b es=002b fs=0053 gs=002b efl=00010246  

chrome!views::View::UpdateTooltip+0x6 [inlined in chrome!views::View::RemoveAllChildViews+0x4f]:  

00007ffd`77e21e5f ff5050 call qword ptr [rax+50h] ds:000001f7`e5bc0ad0=feeefeeefeeefeee  

0:000> k

# Child-SP RetAddr Call Site

00 (Inline Function) --------`-------- chrome!views::View::UpdateTooltip+0x6 [c:\b\s\w\ir\cache\builder\src\ui\views\view.cc @ 2957] 01 000000ec`a27fcd30 00007ffd`7e848756 chrome!views::View::RemoveAllChildViews+0x4f [c:\b\s\w\ir\cache\builder\src\ui\views\view.cc @ 283] 02 000000ec`a27fcd80 00007ffd`7e849c88 chrome!payments::PaymentRequestSheetController::UpdateHeaderView+0x26 [c:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\payments\payment_request_sheet_controller.cc @ 294] 03 000000ec`a27fcdf0 00007ffd`77c54be9 chrome!payments::PaymentHandlerWebFlowViewController::VisibleSecurityStateChanged+0x18 [c:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\payments\payment_handler_web_flow_view_controller.cc @ 303] 04 000000ec`a27fce30 00007ffd`79397a5f chrome!content::WebContentsImpl::DidChangeVisibleSecurityState+0x29 [c:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc @ 2153] 05 000000ec`a27fce90 00007ffd`793975c3 chrome!safe_browsing::BaseUIManager::RemoveWhitelistUrlSet+0x16f [c:\b\s\w\ir\cache\builder\src\components\safe_browsing\content\base_ui_manager.cc @ 463] 06 000000ec`a27fcf30 00007ffd`7bec9c41 chrome!safe_browsing::BaseUIManager::OnBlockingPageDone+0x123 [c:\b\s\w\ir\cache\builder\src\components\safe_browsing\content\base_ui_manager.cc @ 190] 07 000000ec`a27fd030 00007ffd`79397074 chrome!safe_browsing::SafeBrowsingUIManager::OnBlockingPageDone+0x41 [c:\b\s\w\ir\cache\builder\src\chrome\browser\safe_browsing\ui_manager.cc @ 238] 08 000000ec`a27fd0b0 00007ffd`7bea8e26 chrome!safe_browsing::BaseBlockingPage::OnDontProceedDone+0x84 [c:\b\s\w\ir\cache\builder\src\components\safe_browsing\content\base_blocking_page.cc @ 315] 09 000000ec`a27fd140 00007ffd`78fc526c chrome!safe_browsing::SafeBrowsingBlockingPage::OnInterstitialClosing+0xc6 [c:\b\s\w\ir\cache\builder\src\chrome\browser\safe_browsing\safe_browsing_blocking_page.cc @ 177] 0a 000000ec`a27fd190 00007ffd`78fe0d90 chrome!content::WebContentsImpl::~WebContentsImpl+0xe8c [c:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc @ 903] 0b 000000ec`a27fd290 00007ffd`77b56b27 chrome!content::WebContentsImpl::~WebContentsImpl+0x10 [c:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc @ 791] 0c (Inline Function) --------`-------- chrome!std::\_\_1::default\_delete[content::WebContents](javascript:void(0);)::operator()+0xa [c:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\memory @ 2378]  

0d (Inline Function) --------`-------- chrome!std::__1::unique_ptr<content::WebContents,std::__1::default_delete<content::WebContents> >::reset+0x1a [c:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\memory @ 2633] 0e 000000ec`a27fd2d0 00007ffd`7d01e028 chrome!views::WebView::SetWebContents+0xe7 [c:\b\s\w\ir\cache\builder\src\ui\views\controls\webview\webview.cc @ 95] 0f 000000ec`a27fd370 00007ffd`7d01ebe0 chrome!views::WebView::~WebView+0xb8 [c:\b\s\w\ir\cache\builder\src\ui\views\controls\webview\webview.cc @ 71] 10 000000ec`a27fd3b0 00007ffd`77a1f006 chrome!views::WebView::~WebView+0x10 [c:\b\s\w\ir\cache\builder\src\ui\views\controls\webview\webview.cc @ 68] 11 000000ec`a27fd3f0 00007ffd`7a501e50 chrome!views::View::~View+0x106 [c:\b\s\w\ir\cache\builder\src\ui\views\view.cc @ 206] 12 000000ec`a27fd490 00007ffd`77a1f006 chrome!views::View::~View+0x10 [c:\b\s\w\ir\cache\builder\src\ui\views\view.cc @ 193] 13 000000ec`a27fd4d0 00007ffd`7a501e50 chrome!views::View::~View+0x106 [c:\b\s\w\ir\cache\builder\src\ui\views\view.cc @ 206] 14 000000ec`a27fd570 00007ffd`77a1f006 chrome!views::View::~View+0x10 [c:\b\s\w\ir\cache\builder\src\ui\views\view.cc @ 193] 15 000000ec`a27fd5b0 00007ffd`7a501e50 chrome!views::View::~View+0x106 [c:\b\s\w\ir\cache\builder\src\ui\views\view.cc @ 206] 16 000000ec`a27fd650 00007ffd`77a1f006 chrome!views::View::~View+0x10 [c:\b\s\w\ir\cache\builder\src\ui\views\view.cc @ 193] 17 000000ec`a27fd690 00007ffd`7aeed8d0 chrome!views::View::~View+0x106 [c:\b\s\w\ir\cache\builder\src\ui\views\view.cc @ 206] 18 000000ec`a27fd730 00007ffd`77a1f006 chrome!views::ScrollView::~ScrollView+0x10 [c:\b\s\w\ir\cache\builder\src\ui\views\controls\scroll_view.cc @ 214] 19 000000ec`a27fd770 00007ffd`7e848baa chrome!views::View::~View+0x106 [c:\b\s\w\ir\cache\builder\src\ui\views\view.cc @ 206] 1a (Inline Function) --------`-------- chrome!payments::`anonymous namespace'::SheetView::~SheetView+0xaf [c:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\payments\payment_request_sheet_controller.cc @ 56] 1b 000000ec`a27fd810 00007ffd`7e846e2d chrome!payments::`anonymous namespace'::SheetView::~SheetView+0xba [c:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\payments\payment\_request\_sheet\_controller.cc @ 56]  

1c (Inline Function) --------`-------- chrome!std::__1::default_delete<views::View>::operator()+0xb [c:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\memory @ 2378] 1d (Inline Function) --------`-------- chrome!std::\_\_1::unique\_ptr<views::View,std::\_\_1::default\_delete[views::View](javascript:void(0);) >::reset+0x20 [c:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\memory @ 2633]  

1e (Inline Function) --------`-------- chrome!std::__1::unique_ptr<views::View,std::__1::default_delete<views::View> >::~unique_ptr+0x20 [c:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\memory @ 2587] 1f (Inline Function) --------`-------- chrome!std::\_\_1::allocator<std::\_\_1::unique\_ptr<views::View,std::\_\_1::default\_delete[views::View](javascript:void(0);) > >::destroy+0x20 [c:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\memory @ 1920]  

20 (Inline Function) --------`-------- chrome!std::__1::allocator_traits<std::__1::allocator<std::__1::unique_ptr<views::View,std::__1::default_delete<views::View> > > >::__destroy+0x20 [c:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\memory @ 1782] 21 (Inline Function) --------`-------- chrome!std::\_\_1::allocator\_traits<std::\_\_1::allocator<std::\_\_1::unique\_ptr<views::View,std::\_\_1::default\_delete[views::View](javascript:void(0);) > > >::destroy+0x20 [c:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\memory @ 1619]  

22 (Inline Function) --------`-------- chrome!std::__1::__vector_base<std::__1::unique_ptr<views::View,std::__1::default_delete<views::View> >,std::__1::allocator<std::__1::unique_ptr<views::View,std::__1::default_delete<views::View> > > >::__destruct_at_end+0x2c [c:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\vector @ 426] 23 (Inline Function) --------`-------- chrome!std::\_\_1::\_\_vector\_base<std::\_\_1::unique\_ptr<views::View,std::\_\_1::default\_delete[views::View](javascript:void(0);) >,std::\_\_1::allocator<std::\_\_1::unique\_ptr<views::View,std::\_\_1::default\_delete[views::View](javascript:void(0);) > > >::clear+0x2c [c:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\vector @ 369]  

24 (Inline Function) --------`-------- chrome!std::__1::__vector_base<std::__1::unique_ptr<views::View,std::__1::default_delete<views::View> >,std::__1::allocator<std::__1::unique_ptr<views::View,std::__1::default_delete<views::View> > > >::~__vector_base+0x38 [c:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\vector @ 463] 25 (Inline Function) --------`-------- chrome!std::\_\_1::vector<std::\_\_1::unique\_ptr<views::View,std::\_\_1::default\_delete[views::View](javascript:void(0);) >,std::\_\_1::allocator<std::\_\_1::unique\_ptr<views::View,std::\_\_1::default\_delete[views::View](javascript:void(0);) > > >::~vector+0x38 [c:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\vector @ 555]  

26 000000ec`a27fd850 00007ffd`7e847450 chrome!ViewStack::~ViewStack+0xad [c:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\payments\view\_stack.cc @ 30]  

27 000000ec`a27fd890 00007ffd`7e260ab1 chrome!ViewStack::~ViewStack+0x10 [c:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\payments\view\_stack.cc @ 30]  

28 (Inline Function) --------`-------- chrome!std::__1::default_delete<ViewStack>::operator()+0xe [c:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\memory @ 2378] 29 (Inline Function) --------`-------- chrome!std::\_\_1::unique\_ptr<ViewStack,std::\_\_1::default\_delete<ViewStack> >::reset+0x10 [c:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\memory @ 2633]  

2a (Inline Function) --------`-------- chrome!std::__1::unique_ptr<ViewStack,std::__1::default_delete<ViewStack> >::~unique_ptr+0x10 [c:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\memory @ 2587] 2b 000000ec`a27fd8d0 00007ffd`7aed9490 chrome!payments::PaymentRequestDialogView::OnDialogClosed+0xa1 [c:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\payments\payment_request_dialog_view.cc @ 98] 2c (Inline Function) --------`-------- chrome!base::OnceCallback<void ()>::Run+0x11 [c:\b\s\w\ir\cache\builder\src\base\callback.h @ 99]  

2d (Inline Function) --------`-------- chrome!views::DialogDelegate::RunCloseCallback+0x1d [c:\b\s\w\ir\cache\builder\src\ui\views\window\dialog_delegate.cc @ 161] 2e 000000ec`a27fd920 00007ffd`7aedab6f chrome!views::DialogDelegate::WindowWillClose+0x50 [c:\b\s\w\ir\cache\builder\src\ui\views\window\dialog_delegate.cc @ 211] 2f (Inline Function) --------`-------- chrome!base::OnceCallback<void ()>::Run+0x17 [c:\b\s\w\ir\cache\builder\src\base\callback.h @ 99]  

30 000000ec`a27fd970 00007ffd`7a502f5d chrome!views::WidgetDelegate::WindowWillClose+0x3f [c:\b\s\w\ir\cache\builder\src\ui\views\widget\widget\_delegate.cc @ 178]  

31 000000ec`a27fd9c0 00007ffd`7aee4905 chrome!views::Widget::CloseWithReason+0x36d [c:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc @ 606]  

32 000000ec`a27fda70 00007ffd`7cdbde20 chrome!views::ButtonController::OnMouseReleased+0x85 [c:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button\_controller.cc @ 50]  

33 000000ec`a27fdad0 00007ffd`77b943fe chrome!ui::ScopedTargetHandler::OnEvent+0x40 [c:\b\s\w\ir\cache\builder\src\ui\events\scoped\_target\_handler.cc @ 34]  

34 (Inline Function) --------`-------- chrome!ui::EventDispatcher::DispatchEvent+0x29 [c:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc @ 191] 35 000000ec`a27fdb30 00007ffd`77b93116 chrome!ui::EventDispatcher::ProcessEvent+0xee [c:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc @ 140] 36 (Inline Function) --------`-------- chrome!ui::EventDispatcherDelegate::DispatchEventToTarget+0x35 [c:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc @ 84]  

37 000000ec`a27fdb90 00007ffd`77e2878d chrome!ui::EventDispatcherDelegate::DispatchEvent+0x106 [c:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc @ 56]  

38 000000ec`a27fdc30 00007ffd`77dbfe37 chrome!views::internal::RootView::OnMouseReleased+0x7d [c:\b\s\w\ir\cache\builder\src\ui\views\widget\root\_view.cc @ 470]  

39 000000ec`a27fdd80 00007ffd`77b943fe chrome!views::Widget::OnMouseEvent+0x237 [c:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc @ 1281]  

3a (Inline Function) --------`-------- chrome!ui::EventDispatcher::DispatchEvent+0x29 [c:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc @ 191] 3b 000000ec`a27fde40 00007ffd`77b93116 chrome!ui::EventDispatcher::ProcessEvent+0xee [c:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc @ 140] 3c (Inline Function) --------`-------- chrome!ui::EventDispatcherDelegate::DispatchEventToTarget+0x35 [c:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc @ 84]  

3d 000000ec`a27fdea0 00007ffd`77b91a51 chrome!ui::EventDispatcherDelegate::DispatchEvent+0x106 [c:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc @ 56]  

3e 000000ec`a27fdf40 00007ffd`77b918c7 chrome!ui::EventProcessor::OnEventFromSource+0x151 [c:\b\s\w\ir\cache\builder\src\ui\events\event\_processor.cc @ 49]  

3f 000000ec`a27fdfd0 00007ffd`77b917cd chrome!ui::EventSource::DeliverEventToSink+0x27 [c:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc @ 114]  

40 000000ec`a27fe010 00007ffd`77b91660 chrome!ui::EventSource::SendEventToSinkFromRewriter+0x15d [c:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc @ 141]  

41 000000ec`a27fe0a0 00007ffd`77b91620 chrome!ui::EventSource::SendEventToSink+0x10 [c:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc @ 107]  

42 000000ec`a27fe0d0 00007ffd`77b900f9 chrome!views::DesktopWindowTreeHostWin::HandleMouseEvent+0xd0 [c:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_window\_tree\_host\_win.cc @ 954]  

43 000000ec`a27fe120 00007ffd`779fa8af chrome!views::HWNDMessageHandler::HandleMouseEventInternal+0x409 [c:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc @ 3098]  

44 000000ec`a27fe3d0 00007ffd`779fa4bd chrome!views::HWNDMessageHandler::\_ProcessWindowMessage+0xdf [c:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.h @ 358]  

45 000000ec`a27fe5a0 00007ffd`777bca99 chrome!views::HWNDMessageHandler::OnWndProc+0x10d [c:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc @ 1003]  

46 000000ec`a27fe6a0 00007ffd`777bc9ff chrome!gfx::WindowImpl::WndProc+0x89 [c:\b\s\w\ir\cache\builder\src\ui\gfx\win\window\_impl.cc @ 311]  

47 000000ec`a27fe710 00007ffd`c086e338 chrome!base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc>+0xf [c:\b\s\w\ir\cache\builder\src\base\win\wrapped\_window\_proc.h @ 77]  

48 000000ec`a27fe740 00007ffd`c086dd79 user32!UserCallWinProcCheckWow+0x2f8  

49 000000ec`a27fe8d0 00007ffd`77b8cd0f user32!DispatchMessageWorker+0x249  

4a 000000ec`a27fe950 00007ffd`7a578a03 chrome!base::MessagePumpForUI::ProcessMessageHelper+0x37f [c:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc @ 526]  

4b 000000ec`a27fea30 00007ffd`77b8cc2c chrome!base::MessagePumpForUI::ProcessPumpReplacementMessage+0x113 [c:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc @ 620]  

4c 000000ec`a27feb00 00007ffd`7a57878a chrome!base::MessagePumpForUI::ProcessMessageHelper+0x29c [c:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc @ 518]  

4d 000000ec`a27febe0 00007ffd`778372cd chrome!base::MessagePumpForUI::ProcessNextWindowsMessage+0xaa [c:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc @ 492]  

4e 000000ec`a27feca0 00007ffd`7779388c chrome!base::MessagePumpForUI::DoRunLoop+0x3d [c:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc @ 214]  

4f 000000ec`a27fed20 00007ffd`77724421 chrome!base::MessagePumpWin::Run+0x4c [c:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc @ 77]  

50 000000ec`a27fed70 00007ffd`77723efc chrome!base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0xd1 [c:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc @ 453]  

51 000000ec`a27fedd0 00007ffd`77b8a675 chrome!base::RunLoop::Run+0x19c [c:\b\s\w\ir\cache\builder\src\base\run\_loop.cc @ 126]  

52 000000ec`a27fee80 00007ffd`77b8a57e chrome!ChromeBrowserMainParts::MainMessageLoopRun+0x75 [c:\b\s\w\ir\cache\builder\src\chrome\browser\chrome\_browser\_main.cc @ 1708]  

53 000000ec`a27fef10 00007ffd`77b8a541 chrome!content::BrowserMainLoop::RunMainMessageLoopParts+0x2e [c:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc @ 1004]  

54 000000ec`a27fefa0 00007ffd`777ad112 chrome!content::BrowserMainRunnerImpl::Run+0x11 [c:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc @ 151]  

55 000000ec`a27fefd0 00007ffd`777373b8 chrome!content::BrowserMain+0xc2 [c:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc @ 47]  

56 (Inline Function) --------`-------- chrome!content::RunBrowserProcessMain+0x43 [c:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 525] 57 000000ec`a27ff070 00007ffd`77736ee3 chrome!content::ContentMainRunnerImpl::RunServiceManager+0x478 [c:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 997] 58 000000ec`a27ff1b0 00007ffd`777202d8 chrome!content::ContentMainRunnerImpl::Run+0x123 [c:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 884] 59 000000ec`a27ff250 00007ffd`7771fcae chrome!service_manager::Main+0x558 [c:\b\s\w\ir\cache\builder\src\services\service_manager\embedder\main.cc @ 453] 5a 000000ec`a27ff520 00007ffd`7771537f chrome!content::ContentMain+0x3e [c:\b\s\w\ir\cache\builder\src\content\app\content_main.cc @ 19] 5b 000000ec`a27ff5b0 00007ff7`3d7e253a chrome!ChromeMain+0x11f [c:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc @ 120] 5c 000000ec`a27ff6a0 00007ff7`3d7e1b4b chrome_exe!Ordinal0+0x253a 5d 000000ec`a27ff760 00007ff7`3d916d22 chrome_exe!Ordinal0+0x1b4b 5e 000000ec`a27ffb50 00007ffd`c0af6fd4 chrome_exe!GetHandleVerifier+0xe1572 5f 000000ec`a27ffb90 00007ffd`c0d5cec1 KERNEL32!BaseThreadInitThunk+0x14 60 000000ec`a27ffbc0 00000000`00000000 ntdll!RtlUserThreadStart+0x21

## Attachments

- [screen.mp4](attachments/screen.mp4) (video/mp4, 2.8 MB)
- [fix_crash_after_payment_request_cancellation.mp4](attachments/fix_crash_after_payment_request_cancellation.mp4) (video/mp4, 1.2 MB)

## Timeline

### ch...@gmail.com (2020-08-10)

[Comment Deleted]

### xi...@chromium.org (2020-08-10)

Thanks for the report! It is likely introduced in https://crrev.com/c/2302970. jdragon.bae@, could you take a look? Thanks!

[Monorail components: UI>Browser>Payments]

### ch...@gmail.com (2020-08-11)

I am able to repro this on M85 but with a different call stack (a NULL-dereference because some pointer was NULL).

### [Deleted User] (2020-08-11)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-11)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-11)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jd...@gmail.com (2020-08-12)

chromium.khalil@: Could you share the call stack? :)
I did test on the Version 86.0.4230.0 (Developer Build) (64-bit).
The "https://lbstyle.github.io/o.html" seems to secure.


### ro...@chromium.org (2020-08-12)

I will take a look.

### ro...@chromium.org (2020-08-12)

WIP @ https://crrev.com/c/2351959

### ro...@chromium.org (2020-08-12)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c05e691ae40ab608e7113863a638394158cf10a7

commit c05e691ae40ab608e7113863a638394158cf10a7
Author: Rouslan Solomakhin <rouslan@chromium.org>
Date: Wed Aug 12 16:45:51 2020

[Web Payment] Do not update header view when aborting payment.

Before this patch, navigation to an insecure page would update the
header view and remove the header view at the same time, which could
result in a use-after-free.

This patch updates the header view only when not aborting payment.

After this patch, navigation to an insecure page will remove the header
view and not try updating it, thus avoiding the use-after-free.

Bug: 1114556
Change-Id: I946bed36433e3241c6c19c33d7be759ea23a1478
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2351959
Reviewed-by: Liquan (Max) Gu <maxlg@chromium.org>
Commit-Queue: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Commit-Position: refs/heads/master@{#797294}

[modify] https://crrev.com/c05e691ae40ab608e7113863a638394158cf10a7/chrome/browser/ui/views/payments/payment_handler_web_flow_view_controller.cc


### ro...@chromium.org (2020-08-12)

 chromium.khalil@g & jdragon.bae@ - please help verify that fix.

### ch...@gmail.com (2020-08-12)

I will verify it on the next canary release, which should be available by tomorrow.

### ro...@chromium.org (2020-08-12)

[Empty comment from Monorail migration]

### ch...@gmail.com (2020-08-13)

After that patch, the UAF no longer exists on canary (just verified in 86.0.4232.0), but it still hits a NULL pointer. Crash/d23a0a09dd98a803

### ro...@chromium.org (2020-08-13)

Thank you! I will keep looking.

### ro...@chromium.org (2020-08-13)

[Empty comment from Monorail migration]

### ro...@chromium.org (2020-08-13)

I don't think that I would have enough time until the branch point to investigate these crashes, since they are so tricky and my plate is otherwise full. Therefore, let's revert the set of patches that update the header view for now and reland them with better test coverage that catches crashes before they are shipped :)


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/92658bd8860b104ff4cb8bdd10790ccb4406ba7d

commit 92658bd8860b104ff4cb8bdd10790ccb4406ba7d
Author: Rouslan Solomakhin <rouslan@chromium.org>
Date: Thu Aug 13 13:46:26 2020

[Web Payment] Revert header view changes.

This reverts https://crrev.com/c/2351959, https://crrev.com/c/2345928,
https://crrev.com/c/2302970, and https://crrev.com/c/2257090 because
they are causing hard-to-diagnose crashes in production for a feature
that is supposed to be still turned off. The patches should be relanded
with more test coverage.

TBR=jdragon.bae@gmail.com, manukh@chromium.org, maxlg@chromium.org

Bug: 1114556, 1052493
Change-Id: Ic221c99e28246676d24bcd2185773657abef4781
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2354149
Commit-Queue: Rouslan Solomakhin <rouslan@chromium.org>
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Commit-Position: refs/heads/master@{#797651}

[modify] https://crrev.com/92658bd8860b104ff4cb8bdd10790ccb4406ba7d/chrome/browser/payments/ssl_validity_checker.cc
[modify] https://crrev.com/92658bd8860b104ff4cb8bdd10790ccb4406ba7d/chrome/browser/payments/ssl_validity_checker.h
[modify] https://crrev.com/92658bd8860b104ff4cb8bdd10790ccb4406ba7d/chrome/browser/ui/views/payments/payment_handler_web_flow_view_controller.cc
[modify] https://crrev.com/92658bd8860b104ff4cb8bdd10790ccb4406ba7d/components/omnibox/browser/BUILD.gn
[modify] https://crrev.com/92658bd8860b104ff4cb8bdd10790ccb4406ba7d/components/omnibox/browser/location_bar_model_impl.cc
[delete] https://crrev.com/95ed59d093f8db96d5b57bb6da2df09f4c7a23a8/components/omnibox/browser/location_bar_model_util.cc
[delete] https://crrev.com/95ed59d093f8db96d5b57bb6da2df09f4c7a23a8/components/omnibox/browser/location_bar_model_util.h
[modify] https://crrev.com/92658bd8860b104ff4cb8bdd10790ccb4406ba7d/components/payments/core/features.cc
[modify] https://crrev.com/92658bd8860b104ff4cb8bdd10790ccb4406ba7d/components/payments/core/features.h


### ro...@chromium.org (2020-08-13)

chromium.khalil@g & jdragon.bae@ - please help verify the fix in canary in a day or two.

### ch...@gmail.com (2020-08-14)

I'm still able to repro the crash in canary 86.0.4233.0.

### ro...@chromium.org (2020-08-14)

Too early :-)

https://chromiumdash.appspot.com/commit/92658bd8860b104ff4cb8bdd10790ccb4406ba7d has not been release to Canary yet. Could you wait a bit more, please? :-D

That link will let you know the first Chrome version when the patch is released.

### ch...@gmail.com (2020-08-14)

Great! That’s helpful!

### ch...@gmail.com (2020-08-16)

Unfortunately, the crash still exists in 86.0.4235.0 Canary.

### ro...@chromium.org (2020-08-16)

Very interesting! So this is unrelated to jdragon.bae@'s changes. Let me look into this futher.

### ro...@chromium.org (2020-08-16)

hromium.khalil@ - do you have the latest crash ID and steps to reproduce?

### ro...@chromium.org (2020-08-16)

A bisect would be nice.

### ch...@gmail.com (2020-08-16)

Crash ID: 32a9b48d9904175f.

Steps to repro:

1. Go to https://skilful-reserve-239412.appspot.com/static/apps/max-nonbasiccard/, click install
2. Go to https://maxlgu.github.io/pr/max-nonbasiccard/
3. Click on Buy 
4. In payment dialog try to change http://www.google.com to https://testsafebrowsing.appspot.com/s/malware.html then click on "Go!" button
5. Click on "Cancel" button

### ro...@google.com (2020-08-16)

In step 5, I see the "Close" button. Do you see that as well? I'm able to reproduce when clicking that. crash/2989d7c294ed8e4c

### ro...@google.com (2020-08-16)

This reproduces in Chrome stable 84.0.4147.125. go/crash/01a6272986b0e4d0

### ro...@google.com (2020-08-16)

[Empty comment from Monorail migration]

### ro...@google.com (2020-08-16)

According to the stack trace, when the user clicks the "Close" button, the browser payment sheet starts to destroy the views, which destroys the WebView, which destroys the WebContents, which notifies the interstitial page that it's closing, which notifies the browser payment sheet that the security state is changing, so it attempts to update the views that are currently being destroyed. That results in the use after free.

The correct solution is to stop listening to events when the error message is displayed. 

### jd...@gmail.com (2020-08-16)

rouslan@: I can also find the crash in the same way.

Version 84.0.4147.125 (Official Build) (64-bit)


### jd...@gmail.com (2020-08-16)

rouslan@: I wonder if the code you said has something to do with it here[1][2].

[1] https://source.chromium.org/chromium/chromium/src/+/master:components/security_interstitials/content/security_interstitial_tab_helper.cc;l=47
[2] https://source.chromium.org/chromium/chromium/src/+/master:components/security_interstitials/content/security_interstitial_tab_helper.h;=97

### ro...@google.com (2020-08-16)

Not sure. Here's the stack trace:

view_stack.cc:116 ViewStack::Push(std::__1::unique_ptr<views::View, std::__1::default_delete<views::View> >, bool)
payment_request_dialog_view.cc:123 payments::PaymentRequestDialogView::ShowErrorMessage()
payment_handler_web_flow_view_controller.cc:342 payments::PaymentHandlerWebFlowViewController::AbortPayment()
web_contents_impl.cc:2202 content::WebContentsImpl::DidChangeVisibleSecurityState()
base_ui_manager.cc:462 safe_browsing::BaseUIManager::RemoveWhitelistUrlSet(GURL const&, content::WebContents*, bool)
base_ui_manager.cc:187 safe_browsing::BaseUIManager::OnBlockingPageDone(std::__1::vector<security_interstitials::UnsafeResource, std::__1::allocator<security_interstitials::UnsafeResource> > const&, bool, content::WebContents*, GURL const&, bool)
ui_manager.cc:236 safe_browsing::SafeBrowsingUIManager::OnBlockingPageDone(std::__1::vector<security_interstitials::UnsafeResource, std::__1::allocator<security_interstitials::UnsafeResource> > const&, bool, content::WebContents*, GURL const&, bool)
base_blocking_page.cc:309 safe_browsing::BaseBlockingPage::OnDontProceedDone()
safe_browsing_blocking_page.cc:174 safe_browsing::SafeBrowsingBlockingPage::OnInterstitialClosing()
web_contents_impl.cc:948 content::WebContentsImpl::~WebContentsImpl()
web_contents_impl.cc:835 <name omitted>
memory:2378 views::WebView::SetWebContents(content::WebContents*)
webview.cc:70 views::WebView::~WebView()
webview.cc:68 <name omitted>
view.cc:209 views::View::~View()
view.cc:193 <name omitted>
view.cc:209 views::View::~View()
view.cc:193 <name omitted>
view.cc:209 views::View::~View()
scroll_view.cc:115 <name omitted>
view.cc:209 views::View::~View()
scroll_view.cc:214 <name omitted>
view.cc:209 views::View::~View()
payment_request_sheet_controller.cc:56 <name omitted>
memory:2378 std::__1::__vector_base<std::__1::unique_ptr<views::View, std::__1::default_delete<views::View> >, std::__1::allocator<std::__1::unique_ptr<views::View, std::__1::default_delete<views::View> > > >::~__vector_base()
vector:555 ViewStack::~ViewStack()
view_stack.cc:30 <name omitted>
memory:2378 payments::PaymentRequestDialogView::OnDialogClosed()
callback.h:99 views::DialogDelegate::WindowWillClose()
callback.h:99 views::WidgetDelegate::WindowWillClose()
widget.cc:604 views::Widget::CloseWithReason(views::Widget::ClosedReason)


### ro...@chromium.org (2020-08-16)

Next step is to write a browser test that shows a payment handler window, shows an interstitial page, then closing the browser payment sheet.

### jd...@gmail.com (2020-08-17)

Is there any way to reproduce this crash on none official build?

### ro...@chromium.org (2020-08-17)

Is your "Safe Browsing" section of chrome://settings/security available and set to enabled?

### ro...@chromium.org (2020-08-17)

The chrome://settings/security settings appear to be all correct here and I don't see the interstitials. I've posted a question on https://groups.google.com/u/1/a/chromium.org/g/chromium-dev/c/fao6SkUsX9A and CC-ed both of you.

### da...@chromium.org (2020-08-17)

[Empty comment from Monorail migration]

### sa...@chromium.org (2020-08-17)

I will take this over

### ro...@chromium.org (2020-08-17)

Thank you, Sahel!! 

### sa...@chromium.org (2020-08-17)

I can reproduce the same stack trace in https://crbug.com/chromium/1114556#c35 on ToT using a chromium build with DCHECK turned off.

### sa...@chromium.org (2020-08-17)

The reason of the crash is that OnDialogClosed() destroys the View stack.  Then the payment_handler_web_flow_view_controller which overrides VisibleSecurityStateChanged calls AbortPayment()[1] AbortPayment() via a few other function calls eventually causes the call of PaymentRequestDialogView::showAnErrorMessage(). Finally attempt to push to an already deleted  View stack[2] causes the crash.

[1] https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/payments/payment_handler_web_flow_view_controller.cc;l=271.
 [2] https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/payments/payment_request_dialog_view.cc;l=123;drc=953aea9232834912b2f01c8497bd87cb004cbe06

### ro...@chromium.org (2020-08-17)

sahel@: Could you please share your gn flags for posterity?

### sa...@chromium.org (2020-08-17)

WIP: https://chromium-review.googlesource.com/c/chromium/src/+/2359562

Attached screencast shows the impact of the fix from the WIP cl.

### sa...@chromium.org (2020-08-17)

re https://crbug.com/chromium/1114556#c46:
gn flags:
is_debug = false
is_component_build = false
use_goma = true
enable_nacl = false

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/db7fbe90953f421395b9ec647c26be9ded89c9f7

commit db7fbe90953f421395b9ec647c26be9ded89c9f7
Author: Sahel Sharify <sahel@chromium.org>
Date: Mon Aug 17 22:48:39 2020

[Payments] Do not show error message in dialog view during close.

Attempting to show an error message in payment request dialog view after
PaymentRequestDialogView::OnDialogClosed() call causes a crash. This is
because PaymentRequestDialogView::ShowErrorMessage() creates an error
view and adds it to the view stack[1] while the stack view gets destroyed
upon PaymentRequestDialogView::OnDialogClosed() call.

[1]https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/payments/payment_request_dialog_view.cc;l=123

This cl fixes the crash by early-returning from
PaymentRequestDialogView::ShowErrorMessage() when the dialog is getting
closed (i.e after PaymentRequestDialogView::OnDialogClosed() has been
called.) The screencast of the fix is already attached to the bug.

Bug: 1114556
Change-Id: I10d9478a83913a167e52ed558a6a09cf18fcd6e4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2359562
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Commit-Queue: Sahel Sharify <sahel@chromium.org>
Cr-Commit-Position: refs/heads/master@{#798860}

[modify] https://crrev.com/db7fbe90953f421395b9ec647c26be9ded89c9f7/chrome/browser/ui/views/payments/payment_request_dialog_view.cc
[modify] https://crrev.com/db7fbe90953f421395b9ec647c26be9ded89c9f7/chrome/browser/ui/views/payments/payment_request_dialog_view.h


### ch...@gmail.com (2020-08-18)

Verified on 86.0.4237.0 canary. Fixed. - Thanks Sahel!

### sa...@chromium.org (2020-08-18)

Thanks chromium.khalil@ for verifying the fix.

### sa...@chromium.org (2020-08-18)

Requesting merge to M85 for the fix landed in https://crbug.com/chromium/1114556#c49. The fix has been in 86.0.4237.0 canary and verified by the reporter per https://crbug.com/chromium/1114556#c50.

### [Deleted User] (2020-08-18)

This bug requires manual review: We are only 6 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sa...@chromium.org (2020-08-18)

1. Does your merge fit within the Merge Decision Guidelines?
The fix does not have an automated test coverage but screencast of the fix on ToT is uploaded in https://crbug.com/chromium/1114556#c47; the fix is an xs cl with two lines only, and I am confident that the merge is safe.

2. Links to the CLs you are requesting to merge.
https://chromium-review.googlesource.com/c/chromium/src/+/2359562

3. Has the change landed and been verified on master/ToT?
The fix has been verified on the latest canary (86.0.4237.0) by the reporter (https://crbug.com/chromium/1114556#c50).

4. Why are these changes required in this milestone after branch?
The issue has "Security_Severity-High" and "ReleaseBlock-Stable" labels.

5. Is this a new feature?
No

6. If it is a new feature, is it behind a flag using finch?
N/A

### sr...@google.com (2020-08-18)

Merge approved for M-85 branch:4183 please merge your changes asap before 3pm PT today so it can be included in the stable RC cut build

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5841e3b9c06e635bdecaa391d8f2d11ba07b0939

commit 5841e3b9c06e635bdecaa391d8f2d11ba07b0939
Author: Sahel Sharify <sahel@chromium.org>
Date: Tue Aug 18 20:24:51 2020

[Merge to M85][Payments] Do not show error message in dialog view during close.

Attempting to show an error message in payment request dialog view after
PaymentRequestDialogView::OnDialogClosed() call causes a crash. This is
because PaymentRequestDialogView::ShowErrorMessage() creates an error
view and adds it to the view stack[1] while the stack view gets destroyed
upon PaymentRequestDialogView::OnDialogClosed() call.

[1]https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/payments/payment_request_dialog_view.cc;l=123

This cl fixes the crash by early-returning from
PaymentRequestDialogView::ShowErrorMessage() when the dialog is getting
closed (i.e after PaymentRequestDialogView::OnDialogClosed() has been
called.) The screencast of the fix is already attached to the bug.

(cherry picked from commit db7fbe90953f421395b9ec647c26be9ded89c9f7)

Bug: 1114556
Change-Id: I10d9478a83913a167e52ed558a6a09cf18fcd6e4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2359562
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Commit-Queue: Sahel Sharify <sahel@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#798860}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2363182
Cr-Commit-Position: refs/branch-heads/4183@{#1591}
Cr-Branched-From: 740e9e8a40505392ba5c8e022a8024b3d018ca65-refs/heads/master@{#782793}

[modify] https://crrev.com/5841e3b9c06e635bdecaa391d8f2d11ba07b0939/chrome/browser/ui/views/payments/payment_request_dialog_view.cc
[modify] https://crrev.com/5841e3b9c06e635bdecaa391d8f2d11ba07b0939/chrome/browser/ui/views/payments/payment_request_dialog_view.h


### sa...@chromium.org (2020-08-18)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-21)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-24)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-08-26)

Congratulations! The VRP panel has decided to award $5,000 for this bug.

### ad...@google.com (2020-08-27)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-09-08)

sahel@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-09-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/55db277a8627724ccb36f3df678ec7cd6bc5128e

commit 55db277a8627724ccb36f3df678ec7cd6bc5128e
Author: Jaeyong Bae <jdragon.bae@gmail.com>
Date: Wed Sep 16 17:02:23 2020

[Web Payment] Reland header view changes.

Original code reviews: https://crrev.com/c/2351959
                       https://crrev.com/c/2345928,
                       https://crrev.com/c/2302970
                       https://crrev.com/c/2257090
Reverted in: https://crrev.com/c/2354149
Reason for revert: Suspected of causing the
                   https://crbug.com/1114556 crash.
Reason for reland: The root cause of the crash was determined
                   to be something else. More test coverage
                   is added.

Original change's description:
> [Web Payment] Revert header view changes.
>
> This reverts https://crrev.com/c/2351959, https://crrev.com/c/2345928,
> https://crrev.com/c/2302970, and https://crrev.com/c/2257090 because
> they are causing hard-to-diagnose crashes in production for a feature
> that is supposed to be still turned off. The patches should be
> relanded with more test coverage.
>
> Bug: 1114556, 1052493
> Change-Id: Ic221c99e28246676d24bcd2185773657abef4781
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2354149
> Commit-Queue: Rouslan Solomakhin <rouslan@chromium.org>
> Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#797651}

Bug: 1052493
Change-Id: I4b16ee3d383fd01431498444f8d2ef709b3d6204
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2389860
Commit-Queue: Jaeyong Bae <jdragon.bae@gmail.com>
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Reviewed-by: manuk hovanesian <manukh@chromium.org>
Cr-Commit-Position: refs/heads/master@{#807531}

[modify] https://crrev.com/55db277a8627724ccb36f3df678ec7cd6bc5128e/chrome/browser/payments/ssl_validity_checker.cc
[modify] https://crrev.com/55db277a8627724ccb36f3df678ec7cd6bc5128e/chrome/browser/payments/ssl_validity_checker.h
[add] https://crrev.com/55db277a8627724ccb36f3df678ec7cd6bc5128e/chrome/browser/ui/views/payments/payment_handler_header_view_ui_browsertest.cc
[modify] https://crrev.com/55db277a8627724ccb36f3df678ec7cd6bc5128e/chrome/browser/ui/views/payments/payment_handler_web_flow_view_controller.cc
[modify] https://crrev.com/55db277a8627724ccb36f3df678ec7cd6bc5128e/chrome/browser/ui/views/payments/payment_request_dialog_view_ids.h
[modify] https://crrev.com/55db277a8627724ccb36f3df678ec7cd6bc5128e/chrome/test/BUILD.gn
[modify] https://crrev.com/55db277a8627724ccb36f3df678ec7cd6bc5128e/components/omnibox/browser/BUILD.gn
[modify] https://crrev.com/55db277a8627724ccb36f3df678ec7cd6bc5128e/components/omnibox/browser/location_bar_model_impl.cc
[add] https://crrev.com/55db277a8627724ccb36f3df678ec7cd6bc5128e/components/omnibox/browser/location_bar_model_util.cc
[add] https://crrev.com/55db277a8627724ccb36f3df678ec7cd6bc5128e/components/omnibox/browser/location_bar_model_util.h
[add] https://crrev.com/55db277a8627724ccb36f3df678ec7cd6bc5128e/components/omnibox/browser/location_bar_model_util_unittest.cc
[modify] https://crrev.com/55db277a8627724ccb36f3df678ec7cd6bc5128e/components/payments/core/features.cc
[modify] https://crrev.com/55db277a8627724ccb36f3df678ec7cd6bc5128e/components/payments/core/features.h


### ad...@google.com (2020-10-21)

[Empty comment from Monorail migration]

### na...@google.com (2020-10-23)

[Empty comment from Monorail migration]

[Monorail components: Blink>Payments]

### na...@google.com (2020-10-23)

[Empty comment from Monorail migration]

[Monorail components: -UI>Browser>Payments]

### [Deleted User] (2020-11-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1114556?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1115895]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053039)*
