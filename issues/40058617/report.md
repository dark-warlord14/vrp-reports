# Security: heap-use-after-free in base::ObserverList::RemoveObserver

| Field | Value |
|-------|-------|
| **Issue ID** | [40058617](https://issues.chromium.org/issues/40058617) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Cast |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | mu...@google.com |
| **Created** | 2022-01-27 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**  

Clicking the Cast button while having an extension popup with media open causes a UAF in the browser process.

**VERSION**  

Chrome Version: 100.0.4857.0 + all channels  

Operating System: Windows 10

**REPRODUCTION CASE**

1. Install the extension
2. Open the extension popup
3. Click the Cast button

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: browser Crash State:

==3832==ERROR: AddressSanitizer: heap-use-after-free on address 0x122836ee5928 at pc 0x7ffc0f24f882 bp 0x00362e9fda50 sp 0x00362e9fda98  

READ of size 8 at 0x122836ee5928 thread T0  

==3832==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ffc0f24f881 in base::ObserverList[net::ResolveContext,1,0,base::internal::CheckedObserverAdapter](javascript:void(0);)::RemoveObserver C:\b\s\w\ir\cache\builder\src\base\observer\_list.h:284  

#1 0x7ffc267c102c in media\_router::WebContentsDisplayObserverView::~WebContentsDisplayObserverView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\media\_router\web\_contents\_display\_observer\_view.cc:43  

#2 0x7ffc267c1617 in media\_router::WebContentsDisplayObserverView::~WebContentsDisplayObserverView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\media\_router\web\_contents\_display\_observer\_view.cc:41  

#3 0x7ffc2350816e in media\_router::MediaRouterUI::~MediaRouterUI C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\media\_router\media\_router\_ui.cc:144  

#4 0x7ffc2351541d in media\_router::MediaRouterUI::~MediaRouterUI C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\media\_router\media\_router\_ui.cc:116  

#5 0x7ffc2679ac30 in MediaItemUIDeviceSelectorView::~MediaItemUIDeviceSelectorView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\global\_media\_controls\media\_item\_ui\_device\_selector\_view.cc:251  

#6 0x7ffc267a0a79 in MediaItemUIDeviceSelectorView::~MediaItemUIDeviceSelectorView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\global\_media\_controls\media\_item\_ui\_device\_selector\_view.cc:240  

#7 0x7ffc19892109 in views::View::~View C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:253  

#8 0x7ffc267a8f71 in global\_media\_controls::MediaItemUIView::~MediaItemUIView C:\b\s\w\ir\cache\builder\src\components\global\_media\_controls\public\views\media\_item\_ui\_view.cc:169  

#9 0x7ffc267ab375 in global\_media\_controls::MediaItemUIView::~MediaItemUIView C:\b\s\w\ir\cache\builder\src\components\global\_media\_controls\public\views\media\_item\_ui\_view.cc:166  

#10 0x7ffc2678e2f6 in global\_media\_controls::MediaItemUIListView::HideItem C:\b\s\w\ir\cache\builder\src\components\global\_media\_controls\public\views\media\_item\_ui\_list\_view.cc:99  

#11 0x7ffc234fc3b8 in MediaDialogView::HideMediaItem C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\global\_media\_controls\media\_dialog\_view.cc:169  

#12 0x7ffc2677f85e in global\_media\_controls::MediaSessionItemProducer::RemoveItem C:\b\s\w\ir\cache\builder\src\components\global\_media\_controls\public\media\_session\_item\_producer.cc:385  

#13 0x7ffc2677ebd9 in global\_media\_controls::MediaSessionItemProducer::OnRequestIdReleased C:\b\s\w\ir\cache\builder\src\components\global\_media\_controls\public\media\_session\_item\_producer.cc:322  

#14 0x7ffc112bdaa2 in media\_session::mojom::AudioFocusObserverStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\services\media\_session\public\mojom\audio\_focus.mojom.cc:388  

#15 0x7ffc19eaef2e in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:901  

#16 0x7ffc1c82938c in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#17 0x7ffc19eb2744 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:658  

#18 0x7ffc19ec65f1 in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:1104  

#19 0x7ffc19ec5383 in mojo::internal::MultiplexRouter::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:724  

#20 0x7ffc1c82938c in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#21 0x7ffc19eaa204 in mojo::Connector::DispatchMessageW C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:556  

#22 0x7ffc19eabaf7 in mojo::Connector::ReadAllAvailableMessages C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:614  

#23 0x7ffc19b5f474 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#24 0x7ffc1c6e1235 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  

#25 0x7ffc1c6e0962 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#26 0x7ffc19c0a7f6 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#27 0x7ffc19c08a88 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#28 0x7ffc1c6e2901 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:468  

#29 0x7ffc19adf233 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#30 0x7ffc12bd03db in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1053  

#31 0x7ffc12bd581f in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:155  

#32 0x7ffc12bc9a45 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#33 0x7ffc156a8223 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:637  

#34 0x7ffc156ab3fd in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1152  

#35 0x7ffc156aa4fa in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1018  

#36 0x7ffc156a6ea6 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:399  

#37 0x7ffc156a762a in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:427  

#38 0x7ffc0eed148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:176  

#39 0x7ff779415b16 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:167  

#40 0x7ff779412b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#41 0x7ff77981257f in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#42 0x7ffcd8167033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#43 0x7ffcd8f82650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

0x122836ee5928 is located 168 bytes inside of 536-byte region [0x122836ee5880,0x122836ee5a98)  

freed by thread T0 here:  

#0 0x7ff7794c275b in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82 #1 0x7ffc198d3831 in views::Widget::~Widget C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:187  

#2 0x7ffc23143350 in views::DesktopNativeWidgetAura::~DesktopNativeWidgetAura C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_native\_widget\_aura.cc:304  

#3 0x7ffc2314ba53 in views::DesktopNativeWidgetAura::~DesktopNativeWidgetAura C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_native\_widget\_aura.cc:302  

#4 0x7ffc23144080 in views::DesktopNativeWidgetAura::OnHostClosed C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_native\_widget\_aura.cc:378  

#5 0x7ffc231228ba in views::HWNDMessageHandler::OnWndProc C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:1037  

#6 0x7ffc1ca41010 in gfx::WindowImpl::WndProc C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window\_impl.cc:306  

#7 0x7ffc1ca3f931 in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> C:\b\s\w\ir\cache\builder\src\base\win\wrapped\_window\_proc.h:74  

#8 0x7ffcd82ae7e7 in CallWindowProcW+0x3f7 (C:\WINDOWS\System32\user32.dll+0x18000e7e7)  

#9 0x7ffcd82ae36b in DispatchMessageW+0x39b (C:\WINDOWS\System32\user32.dll+0x18000e36b)  

#10 0x7ffcd82c6ef7 in GetLastInputInfo+0x77 (C:\WINDOWS\System32\user32.dll+0x180026ef7)  

#11 0x7ffcd8fd0ba3 in KiUserCallbackDispatcher+0x23 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800a0ba3)  

#12 0x7ffcd67a2383 in NtUserDestroyWindow+0x13 (C:\WINDOWS\System32\win32u.dll+0x180002383)  

#13 0x7ffc19b5f474 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#14 0x7ffc1c6e1235 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  

#15 0x7ffc1c6e0962 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#16 0x7ffc19c0a7f6 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#17 0x7ffc19c08a88 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#18 0x7ffc1c6e2901 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:468  

#19 0x7ffc19adf233 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#20 0x7ffc12bd03db in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1053  

#21 0x7ffc12bd581f in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:155  

#22 0x7ffc12bc9a45 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#23 0x7ffc156a8223 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:637  

#24 0x7ffc156ab3fd in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1152  

#25 0x7ffc156aa4fa in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1018  

#26 0x7ffc156a6ea6 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:399  

#27 0x7ffc156a762a in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:427

previously allocated by thread T0 here:  

#0 0x7ff7794c285b in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffc2c30a17e in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ffc1f955bdb in views::BubbleDialogDelegate::CreateBubble C:\b\s\w\ir\cache\builder\src\ui\views\bubble\bubble\_dialog\_delegate\_view.cc:427  

#3 0x7ffc1f956b2e in views::BubbleDialogDelegateView::CreateBubble C:\b\s\w\ir\cache\builder\src\ui\views\bubble\bubble\_dialog\_delegate\_view.cc:444  

#4 0x7ffc299d2cea in ExtensionPopup::ShowPopup C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\extensions\extension\_popup.cc:42  

#5 0x7ffc28c72e1c in ExtensionActionPlatformDelegateViews::ShowPopup C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\extensions\extension\_action\_platform\_delegate\_views.cc:87  

#6 0x7ffc275fcd01 in ExtensionActionViewController::ShowPopup C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\extensions\extension\_action\_view\_controller.cc:418  

#7 0x7ffc275fd0d4 in base::internal::Invoker<base::internal::BindState<void (ExtensionActionViewController::\*)(std::\_\_1::unique\_ptr<extensions::ExtensionViewHost,std::\_\_1::default\_delete[extensions::ExtensionViewHost](javascript:void(0);) >, bool, ExtensionActionViewController::PopupShowAction),base::WeakPtr<ExtensionActionViewController>,std::\_\_1::unique\_ptr<extensions::ExtensionViewHost,std::\_\_1::default\_delete[extensions::ExtensionViewHost](javascript:void(0);) >,bool,ExtensionActionViewController::PopupShowAction>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:749  

#8 0x7ffc26aeed25 in views::AnimatingLayoutManager::RunQueuedActions C:\b\s\w\ir\cache\builder\src\ui\views\layout\animating\_layout\_manager.cc:699  

#9 0x7ffc19b5f474 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#10 0x7ffc1c6e1235 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  

#11 0x7ffc1c6e0962 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#12 0x7ffc19c0a7f6 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#13 0x7ffc19c08a88 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#14 0x7ffc1c6e2901 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:468  

#15 0x7ffc19adf233 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#16 0x7ffc12bd03db in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1053  

#17 0x7ffc12bd581f in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:155  

#18 0x7ffc12bc9a45 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#19 0x7ffc156a8223 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:637  

#20 0x7ffc156ab3fd in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1152  

#21 0x7ffc156aa4fa in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1018  

#22 0x7ffc156a6ea6 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:399  

#23 0x7ffc156a762a in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:427  

#24 0x7ffc0eed148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:176  

#25 0x7ff779415b16 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:167  

#26 0x7ff779412b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#27 0x7ff77981257f in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\base\observer\_list.h:284 in base::ObserverList[net::ResolveContext,1,0,base::internal::CheckedObserverAdapter](javascript:void(0);)::RemoveObserver  

Shadow bytes around the buggy address:  

0x04413d55cad0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04413d55cae0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04413d55caf0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa  

0x04413d55cb00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x04413d55cb10: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x04413d55cb20: fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd  

0x04413d55cb30: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04413d55cb40: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04413d55cb50: fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x04413d55cb60: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x04413d55cb70: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==3832==ABORTING

**CREDIT INFORMATION**  

Reporter credit: Thomas Orlita

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 157 B)
- [popup.html](attachments/popup.html) (text/plain, 153 B)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 782.0 KB)
- [popup.html](attachments/popup.html) (text/plain, 187 B)
- [popup.js](attachments/popup.js) (text/plain, 165 B)
- [background.js](attachments/background.js) (text/plain, 28 B)
- [manifest.json](attachments/manifest.json) (text/plain, 221 B)
- [poc-new.mp4](attachments/poc-new.mp4) (video/mp4, 692.1 KB)

## Timeline

### [Deleted User] (2022-01-27)

[Empty comment from Monorail migration]

### ca...@chromium.org (2022-01-28)

I was able to reproduce this myself too in M100. Triaging as high since this a UaF in the browser process but requires significant interaction (might even be a medium due to that, but keeping as high to stay on the safe side). Not setting FoundIn yet since I will check if this reproduces on an earlier version first.

muyaoxu: Can you please take a look and further triage? Feel free to reassign as appropriate. Thanks

[Monorail components: Internals>Cast]

### ca...@chromium.org (2022-01-28)

I can reproduce in 97 too

### [Deleted User] (2022-01-28)

[Empty comment from Monorail migration]

### mu...@google.com (2022-01-29)

This looks like an issue with using raw_ptr in WebContentsDisplayObserverView I will look into it.

steimel@, is it supposed to show local media notifications for media playing from the extension?

### st...@gmail.com (2022-01-30)

Opening the media dialog can be done programmatically using a PresentationRequest, decreasing the user interaction needed. On dev channels, the browser popup can be opened programmatically as well.

1. Install the extension
2. (non-dev channels only): Open the popup
3. Click in the popup

### [Deleted User] (2022-01-30)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-30)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mu...@google.com (2022-01-31)

When the extension pop up is closed, views::WidgetObserver::OnWidgetDestroying() is called instead of views::WidgetObserver::OnWidgetClosing(). The latter API is being deprecated (tracking bug: 1240365). I will put up a patch to fix it.

### gi...@appspot.gserviceaccount.com (2022-01-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4535fe2334d0713535adb52b641a8cb34e11333c

commit 4535fe2334d0713535adb52b641a8cb34e11333c
Author: Muyao Xu <muyaoxu@google.com>
Date: Mon Jan 31 23:58:23 2022

Replace WidgetObserver::OnWidgetClosing() with OnWidgetDestroying()

In some cases, OnWidgetClosing() is not called when the widget is
closed, resulting an invalid pointer |widget_| stored in
WebContentsDisplayObserverView.

This CL replaces OnWidgetClosing() with OnWidgetDestroying(), which
is recommended in crbug.com/1240365

Bug: 1291728
Change-Id: I64fef8b30930f60220008809ee00f4385d6c3520
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3425473
Auto-Submit: Muyao Xu <muyaoxu@google.com>
Reviewed-by: Takumi Fujimoto <takumif@chromium.org>
Commit-Queue: Takumi Fujimoto <takumif@chromium.org>
Cr-Commit-Position: refs/heads/main@{#965431}

[modify] https://crrev.com/4535fe2334d0713535adb52b641a8cb34e11333c/chrome/browser/ui/views/media_router/web_contents_display_observer_view.cc
[modify] https://crrev.com/4535fe2334d0713535adb52b641a8cb34e11333c/chrome/browser/ui/views/media_router/web_contents_display_observer_view.h


### mu...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

Merge approved: your change passed merge requirements and is auto-approved for M99. Please go ahead and merge the CL to branch 4844 (refs/branch-heads/4844) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: benmason (Android), harrysouders (iOS), cindyb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-02-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d636ddca68f281417383bf26f7a2e6a35369c865

commit d636ddca68f281417383bf26f7a2e6a35369c865
Author: Muyao Xu <muyaoxu@google.com>
Date: Wed Feb 02 18:57:48 2022

Replace WidgetObserver::OnWidgetClosing() with OnWidgetDestroying()

In some cases, OnWidgetClosing() is not called when the widget is
closed, resulting an invalid pointer |widget_| stored in
WebContentsDisplayObserverView.

This CL replaces OnWidgetClosing() with OnWidgetDestroying(), which
is recommended in crbug.com/1240365

(cherry picked from commit 4535fe2334d0713535adb52b641a8cb34e11333c)

Bug: 1291728
Change-Id: I64fef8b30930f60220008809ee00f4385d6c3520
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3425473
Auto-Submit: Muyao Xu <muyaoxu@google.com>
Reviewed-by: Takumi Fujimoto <takumif@chromium.org>
Commit-Queue: Takumi Fujimoto <takumif@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#965431}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3428150
Cr-Commit-Position: refs/branch-heads/4844@{#193}
Cr-Branched-From: 007241ce2e6c8e5a7b306cc36c730cd07cd38825-refs/heads/main@{#961656}

[modify] https://crrev.com/d636ddca68f281417383bf26f7a2e6a35369c865/chrome/browser/ui/views/media_router/web_contents_display_observer_view.cc
[modify] https://crrev.com/d636ddca68f281417383bf26f7a2e6a35369c865/chrome/browser/ui/views/media_router/web_contents_display_observer_view.h


### [Deleted User] (2022-02-02)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mu...@google.com (2022-02-02)

1. No
2. No

### rz...@google.com (2022-02-03)

[Empty comment from Monorail migration]

### rz...@google.com (2022-02-03)

[Empty comment from Monorail migration]

### rz...@google.com (2022-02-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-03)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-02-03)

1. Number of CLs needed for this fix and links to them.
1 CL, https://crrev.com/c/3435985

2. Level of complexity (High, Medium, Low - Explain)
Low, no conflicts

3. Has this been merged to a stable release? beta release?
99

4. Overall Recommendation (Yes, No)
Yes

### gm...@google.com (2022-02-03)

We will delay the approval of this merge until the next respin so the bug can go to 99 beta first.

### am...@google.com (2022-02-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-11)

Congratulations on another one, Thomas! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and nice work! 

### am...@google.com (2022-02-14)

[Empty comment from Monorail migration]

### gm...@google.com (2022-02-17)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-02-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1887414c016d19e48e18ac998684f7b2f90d8898

commit 1887414c016d19e48e18ac998684f7b2f90d8898
Author: Muyao Xu <muyaoxu@google.com>
Date: Thu Feb 17 16:23:29 2022

[M96-LTS] Replace WidgetObserver::OnWidgetClosing() with OnWidgetDestroying()

In some cases, OnWidgetClosing() is not called when the widget is
closed, resulting an invalid pointer |widget_| stored in
WebContentsDisplayObserverView.

This CL replaces OnWidgetClosing() with OnWidgetDestroying(), which
is recommended in crbug.com/1240365

(cherry picked from commit 4535fe2334d0713535adb52b641a8cb34e11333c)

Bug: 1291728
Change-Id: I64fef8b30930f60220008809ee00f4385d6c3520
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3425473
Auto-Submit: Muyao Xu <muyaoxu@google.com>
Commit-Queue: Takumi Fujimoto <takumif@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#965431}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3435985
Reviewed-by: Michael Ershov <miersh@google.com>
Owners-Override: Michael Ershov <miersh@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1480}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/1887414c016d19e48e18ac998684f7b2f90d8898/chrome/browser/ui/views/media_router/web_contents_display_observer_view.cc
[modify] https://crrev.com/1887414c016d19e48e18ac998684f7b2f90d8898/chrome/browser/ui/views/media_router/web_contents_display_observer_view.h


### rz...@google.com (2022-02-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-02-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-03-03)

Hi Thomas, in re-assessing the second POC you provided, we have decided to increase the reward amount by an additional $3,000 for a total of $10,000 for this report. Congratulations and thank again for your efforts and this report! 

### am...@google.com (2022-03-04)

[Empty comment from Monorail migration]

### ta...@chromium.org (2022-03-22)

[Empty comment from Monorail migration]

### at...@google.com (2022-03-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1291728?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058617)*
