# Security: Heap-use-after-free in ui::EventDispatcher::DispatchEventToEventHandlers

| Field | Value |
|-------|-------|
| **Issue ID** | [40057069](https://issues.chromium.org/issues/40057069) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Mobile |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ju...@google.com |
| **Created** | 2021-08-29 |
| **Bounty** | $15,000.00 |

## Description

Chrome Version: 95.0.4625.2 (Official Build) canary (64-bit) (cohort: Clang-64)  

Operating System: Windows 10

**REPRODUCTION CASE**

1. Open the test case and click on the button
2. On the PDF page, right-click and select 'Search part of the page with Google lens' and wait

==9620==ERROR: AddressSanitizer: heap-use-after-free on address 0x125d9eacc140 at pc 0x7ff8bc02107e bp 0x00453c3fdb10 sp 0x00453c3fdb58  

READ of size 8 at 0x125d9eacc140 thread T0  

==9620==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ff8bc02107d in base::circular\_deque<ui::EventDispatcher \*>::ExpandCapacityIfNecessary C:\b\s\w\ir\cache\builder\src\base\containers\circular\_deque.h:963  

#1 0x7ff8bc020ed7 in base::circular\_deque<ui::EventDispatcher \*>::emplace\_back<ui::EventDispatcher \*> C:\b\s\w\ir\cache\builder\src\base\containers\circular\_deque.h:853  

#2 0x7ff8bc020934 in ui::EventDispatcher::DispatchEventToEventHandlers C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:166  

#3 0x7ff8bc02010a in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:126  

#4 0x7ff8bc01fca8 in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:84  

#5 0x7ff8bc01f8ec in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:56  

#6 0x7ff8c078b160 in ui::EventProcessor::OnEventFromSource C:\b\s\w\ir\cache\builder\src\ui\events\event\_processor.cc:49  

#7 0x7ff8bd9886b7 in ui::EventSource::DeliverEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:113  

#8 0x7ff8bd988311 in ui::EventSource::SendEventToSinkFromRewriter C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:138  

#9 0x7ff8bd987e13 in ui::EventSource::SendEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:107  

#10 0x7ff8c0788b3d in views::DesktopWindowTreeHostWin::HandleMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_window\_tree\_host\_win.cc:1006  

#11 0x7ff8c465e341 in views::HWNDMessageHandler::HandleMouseEventInternal C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:3143  

#12 0x7ff8c465da5a in views::HWNDMessageHandler::HandleMouseMessage C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:1087  

#13 0x7ff8b594f1df in content::LegacyRenderWidgetHostHWND::OnMouseRange C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\legacy\_render\_widget\_host\_win.cc:318  

#14 0x7ff8b595205e in content::LegacyRenderWidgetHostHWND::\_ProcessWindowMessage C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\legacy\_render\_widget\_host\_win.h:88  

#15 0x7ff8b5950b53 in content::LegacyRenderWidgetHostHWND::ProcessWindowMessage C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\legacy\_render\_widget\_host\_win.h:81  

#16 0x7ff8b59532a4 in ATL::CWindowImplBaseT<ATL::CWindow,ATL::CWinTraits<1073741824,0> >::WindowProc C:\b\s\w\ir\cache\builder\src\third\_party\depot\_tools\win\_toolchain\vs\_files\3bda71a11e\VC\Tools\MSVC\14.26.28801\atlmfc\include\atlwin.h:3567  

#17 0x7ff979b51087 (C:\Windows\SYSTEM32\atlthunk.dll+0x180001087)  

#18 0x7ff97e8fe857 in CallWindowProcW+0x3f7 (C:\Windows\System32\user32.dll+0x18000e857)  

#19 0x7ff97e8fe298 in DispatchMessageW+0x258 (C:\Windows\System32\user32.dll+0x18000e298)  

#20 0x7ff8bb4839ba in base::MessagePumpForUI::ProcessMessageHelper C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:542  

#21 0x7ff8bb4819e9 in base::MessagePumpForUI::ProcessNextWindowsMessage C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:504  

#22 0x7ff8bb4812e3 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:215  

#23 0x7ff8bb47f5d8 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#24 0x7ff8bdd73945 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:467  

#25 0x7ff8bb35e373 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:134  

#26 0x7ff8b48910eb in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:988  

#27 0x7ff8b4896465 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:152  

#28 0x7ff8b488a762 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:49  

#29 0x7ff8b71c0c2c in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:608  

#30 0x7ff8b71c34c8 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1104  

#31 0x7ff8b71c26af in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:971  

#32 0x7ff8b71bf116 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:390  

#33 0x7ff8b71c0176 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:418  

#34 0x7ff8b0d5148c in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:172  

#35 0x7ff7ea035b74 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:169  

#36 0x7ff7ea032be8 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#37 0x7ff7ea4250ef in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#38 0x7ff980557033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#39 0x7ff9808e2650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

0x125d9eacc140 is located 32 bytes inside of 168-byte region [0x125d9eacc120,0x125d9eacc1c8)  

freed by thread T0 here:  

#0 0x7ff7ea0d6edb in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ff8c619456f in image\_editor::ScreenshotFlow::~ScreenshotFlow C:\b\s\w\ir\cache\builder\src\chrome\browser\image\_editor\screenshot\_flow.cc:46  

#2 0x7ff8c4b7171d in std::\_\_1::unique\_ptr<lens::LensRegionSearchController,std::\_\_1::default\_delete[lens::LensRegionSearchController](javascript:void(0);) >::reset C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_memory\unique\_ptr.h:315  

#3 0x7ff8c4b58ad5 in RenderViewContextMenu::~RenderViewContextMenu C:\b\s\w\ir\cache\builder\src\chrome\browser\renderer\_context\_menu\render\_view\_context\_menu.cc:672  

#4 0x7ff8c0a32f43 in RenderViewContextMenuViews::~RenderViewContextMenuViews C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\renderer\_context\_menu\render\_view\_context\_menu\_views.cc:116  

#5 0x7ff8bda91f07 in ChromeWebContentsViewDelegateViews::~ChromeWebContentsViewDelegateViews C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tab\_contents\chrome\_web\_contents\_view\_delegate\_views.cc:29  

#6 0x7ff8bda928f1 in ChromeWebContentsViewDelegateViews::~ChromeWebContentsViewDelegateViews C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tab\_contents\chrome\_web\_contents\_view\_delegate\_views.cc:29  

#7 0x7ff8b57d59d1 in content::WebContentsViewChildFrame::~WebContentsViewChildFrame C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_view\_child\_frame.cc:31  

#8 0x7ff8b5746d91 in content::WebContentsImpl::~WebContentsImpl C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:1012  

#9 0x7ff8b57bab03 in content::WebContentsImpl::~WebContentsImpl C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:913  

#10 0x7ff8b5744a6b in content::WebContentsImpl::WebContentsTreeNode::OnFrameTreeNodeDestroyed C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:777  

#11 0x7ff8b5146b58 in content::FrameTreeNode::~FrameTreeNode C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\frame\_tree\_node.cc:197  

#12 0x7ff8b534592d in content::RenderFrameHostImpl::RemoveChild C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:3794  

#13 0x7ff8b357dcab in blink::mojom::RemoteFrameHostStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\third\_party\blink\public\mojom\frame\frame.mojom.cc:13721  

#14 0x7ff8bb725151 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:898  

#15 0x7ff8bdeb6706 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#16 0x7ff8bb7289dc in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:655  

#17 0x7ff8bbf84a70 in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread C:\b\s\w\ir\cache\builder\src\ipc\ipc\_mojo\_bootstrap.cc:981  

#18 0x7ff8bbf7e965 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:690  

#19 0x7ff8bb3dbbca in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:178  

#20 0x7ff8bdd72442 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:360  

#21 0x7ff8bdd71aa2 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:260  

#22 0x7ff8bb481386 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#23 0x7ff8bb47f5d8 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#24 0x7ff8bdd73945 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:467  

#25 0x7ff8bb35e373 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:134  

#26 0x7ff8b48910eb in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:988  

#27 0x7ff8b4896465 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:152

previously allocated by thread T0 here:  

#0 0x7ff7ea0d6fdb in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ff8cd91f3aa in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ff8c7e991c2 in lens::LensRegionSearchController::LensRegionSearchController C:\b\s\w\ir\cache\builder\src\chrome\browser\lens\region\_search\lens\_region\_search\_controller.cc:22  

#3 0x7ff8c4b6d678 in RenderViewContextMenu::ExecLensRegionSearch C:\b\s\w\ir\cache\builder\src\chrome\browser\renderer\_context\_menu\render\_view\_context\_menu.cc:3307  

#4 0x7ff8c4b6ae67 in RenderViewContextMenu::ExecuteCommand C:\b\s\w\ir\cache\builder\src\chrome\browser\renderer\_context\_menu\render\_view\_context\_menu.cc:2520  

#5 0x7ff8c7a15c1d in views::MenuModelAdapter::ExecuteCommand C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_model\_adapter.cc:170  

#6 0x7ff8c074f3ab in views::internal::MenuRunnerImpl::OnMenuClosed C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_runner\_impl.cc:245  

#7 0x7ff8c45f8052 in views::MenuController::ExitMenu C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_controller.cc:3154  

#8 0x7ff8c45fd473 in views::MenuController::Accept C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_controller.cc:1780  

#9 0x7ff8c45fca07 in views::MenuController::OnMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_controller.cc:827  

#10 0x7ff8bb150b81 in views::Widget::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1548  

#11 0x7ff8bc020d9f in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:191  

#12 0x7ff8bc0202bf in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:140  

#13 0x7ff8bc01fca8 in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:84  

#14 0x7ff8bc01f8ec in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:56  

#15 0x7ff8c078b160 in ui::EventProcessor::OnEventFromSource C:\b\s\w\ir\cache\builder\src\ui\events\event\_processor.cc:49  

#16 0x7ff8bd9886b7 in ui::EventSource::DeliverEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:113  

#17 0x7ff8bd988311 in ui::EventSource::SendEventToSinkFromRewriter C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:138  

#18 0x7ff8bd987e13 in ui::EventSource::SendEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:107  

#19 0x7ff8c0788b3d in views::DesktopWindowTreeHostWin::HandleMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_window\_tree\_host\_win.cc:1006  

#20 0x7ff8c465e341 in views::HWNDMessageHandler::HandleMouseEventInternal C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:3143  

#21 0x7ff8c4657793 in views::HWNDMessageHandler::\_ProcessWindowMessage C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.h:356  

#22 0x7ff8c4656e32 in views::HWNDMessageHandler::OnWndProc C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:1017  

#23 0x7ff8be0ae92a in gfx::WindowImpl::WndProc C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window\_impl.cc:306  

#24 0x7ff8be0ad245 in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> C:\b\s\w\ir\cache\builder\src\base\win\wrapped\_window\_proc.h:74  

#25 0x7ff97e8fe857 in CallWindowProcW+0x3f7 (C:\Windows\System32\user32.dll+0x18000e857)  

#26 0x7ff97e8fe298 in DispatchMessageW+0x258 (C:\Windows\System32\user32.dll+0x18000e298)  

#27 0x7ff8bb4839ba in base::MessagePumpForUI::ProcessMessageHelper C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:542

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\base\containers\circular\_deque.h:963 in base::circular\_deque<ui::EventDispatcher \*>::ExpandCapacityIfNecessary  

Shadow bytes around the buggy address:  

0x048b525d97d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x048b525d97e0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x048b525d97f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa  

0x048b525d9800: fa fa fa fa fa fa fd fd fd fd fd fd fd fd fd fd  

0x048b525d9810: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa  

=>0x048b525d9820: fa fa fa fa fd fd fd fd[fd]fd fd fd fd fd fd fd  

0x048b525d9830: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa  

0x048b525d9840: fa fa fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x048b525d9850: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa  

0x048b525d9860: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x048b525d9870: fd fd fd fd fd fd fa fa fa fa fa fa fa fa fd fd  

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

==9620==ABORTING

## Attachments

- [screen.mp4](attachments/screen.mp4) (video/mp4, 1.4 MB)
- [testcase.html](attachments/testcase.html) (text/plain, 250 B)
- [chromeUrls.pdf](attachments/chromeUrls.pdf) (application/pdf, 7.9 KB)

## Timeline

### [Deleted User] (2021-08-29)

[Empty comment from Monorail migration]

### dr...@chromium.org (2021-08-30)

I was able to reproduce this crash after enabling the enable-lens-region-search flag. Assigning High Severity since it's browser memory corruption with significant user gesture requirements.

[Monorail components: UI>Browser>Mobile]

### be...@google.com (2021-08-30)

[Empty comment from Monorail migration]

### be...@google.com (2021-08-30)

[Empty comment from Monorail migration]

### st...@google.com (2021-08-30)

[Empty comment from Monorail migration]

### dr...@chromium.org (2021-08-30)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/59326cb3d3e8446f09d8f5470197b0571ec3122d

commit 59326cb3d3e8446f09d8f5470197b0571ec3122d
Author: Juan Mojica <juanmojica@google.com>
Date: Tue Sep 14 18:25:35 2021

Disable Lens Region Search on PDFs and URLs with Chrome UI scheme.

Also, adds unit tests for Chrome UI scheme.

Bug: 1234592, 1244348, b/197746903
Change-Id: I292a9a40533a538ef61600286792e24c986fa27e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3159009
Commit-Queue: Juan Mojica <juanmojica@google.com>
Reviewed-by: Ben Goldberger <benwgold@google.com>
Reviewed-by: Colin Blundell <blundell@chromium.org>
Cr-Commit-Position: refs/heads/main@{#921328}

[modify] https://crrev.com/59326cb3d3e8446f09d8f5470197b0571ec3122d/chrome/browser/renderer_context_menu/render_view_context_menu.cc
[modify] https://crrev.com/59326cb3d3e8446f09d8f5470197b0571ec3122d/chrome/browser/renderer_context_menu/render_view_context_menu_unittest.cc


### ju...@google.com (2021-09-14)

The above change should have disabled this menu item on PDFs. Please let me know if this bug can still be reproduced. We are also planning to merge this change into M95 to disable on PDFs.

### ch...@gmail.com (2021-09-15)

Fixed on Canary 96.0.4643.0.


### ju...@google.com (2021-09-15)

Marking as fixed per https://crbug.com/chromium/1244348#c9.

### [Deleted User] (2021-09-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-16)

[Empty comment from Monorail migration]

### st...@google.com (2021-09-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-20)

Merge approved: your change passed merge requirements and is auto-approved for M95. Please go ahead and merge the CL to branch 4638 (refs/branch-heads/4638) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: benmason (Android), harrysouders (iOS), None (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-09-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/92615e91a9952db579ce9e244818f893eb4910b7

commit 92615e91a9952db579ce9e244818f893eb4910b7
Author: Juan Mojica <juanmojica@google.com>
Date: Tue Sep 21 16:04:19 2021

[M95] Disable Lens Region Search on PDFs and URLs with Chrome UI scheme.

Also, adds unit tests for Chrome UI scheme.

(cherry picked from commit 59326cb3d3e8446f09d8f5470197b0571ec3122d)

Bug: 1234592, 1244348, b/197746903
Change-Id: I292a9a40533a538ef61600286792e24c986fa27e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3159009
Commit-Queue: Juan Mojica <juanmojica@google.com>
Reviewed-by: Ben Goldberger <benwgold@google.com>
Reviewed-by: Colin Blundell <blundell@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#921328}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3171754
Cr-Commit-Position: refs/branch-heads/4638@{#200}
Cr-Branched-From: 159257cab5585bc8421abf347984bb32fdfe9eb9-refs/heads/main@{#920003}

[modify] https://crrev.com/92615e91a9952db579ce9e244818f893eb4910b7/chrome/browser/renderer_context_menu/render_view_context_menu.cc
[modify] https://crrev.com/92615e91a9952db579ce9e244818f893eb4910b7/chrome/browser/renderer_context_menu/render_view_context_menu_unittest.cc


### am...@google.com (2021-09-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-23)

Congratulations, Khalil - the VRP Panel has decided to award you $15,000 for this report! Well done! 

### am...@google.com (2021-09-24)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-12-23)

This issue was migrated from crbug.com/chromium/1244348?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057069)*
