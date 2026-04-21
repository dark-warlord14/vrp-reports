# Security: heap-use-after-free in ui::EventTarget::RemovePreTargetHandler

| Field | Value |
|-------|-------|
| **Issue ID** | [40058989](https://issues.chromium.org/issues/40058989) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Forms>Color, Blink>Portals |
| **Platforms** | Fuchsia, Linux, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | mc...@chromium.org |
| **Created** | 2022-03-05 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**  

Selecting a color from an eye dropper initiated in a portal predecessor that has been adopted causes a UAF.

**VERSION**  

Chrome Version: 101.0.4911.0 + stable  

Operating System: Windows 10

**REPRODUCTION CASE**

1. python3 -m http.server 9000
2. chrome --enable-features=Portals <http://localhost:9000/poc.html>
3. Click in the page

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: browser Crash State:

==7044==ERROR: AddressSanitizer: heap-use-after-free on address 0x11d1382d1ce0 at pc 0x7ffac4bac486 bp 0x005c9f1fd680 sp 0x005c9f1fd6c8  

READ of size 8 at 0x11d1382d1ce0 thread T0  

==7044==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ffac4bac485 in ui::EventTarget::RemovePreTargetHandler C:\b\s\w\ir\cache\builder\src\ui\events\event\_target.cc:54  

#1 0x7fface2a5b8c in EyeDropperView::PreEventDispatchHandler::KeyboardHandler::~KeyboardHandler C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\eye\_dropper\eye\_dropper\_view\_aura.cc:38  

#2 0x7fface2a587f in EyeDropperView::PreEventDispatchHandler::~PreEventDispatchHandler C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\eye\_dropper\eye\_dropper\_view\_aura.cc:65  

#3 0x7fface2a5bc9 in EyeDropperView::PreEventDispatchHandler::~PreEventDispatchHandler C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\eye\_dropper\eye\_dropper\_view\_aura.cc:63  

#4 0x7ffac3c0f43d in views::Widget::OnNativeWidgetDestroying C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1393  

#5 0x7ffac993eed5 in views::DesktopWindowTreeHostWin::HandleDestroying C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_window\_tree\_host\_win.cc:920  

#6 0x7ffacd8835f0 in views::HWNDMessageHandler::OnDestroy C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:1670  

#7 0x7ffacd877c29 in views::HWNDMessageHandler::\_ProcessWindowMessage C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.h:431  

#8 0x7ffacd8738ba in views::HWNDMessageHandler::OnWndProc C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:1027  

#9 0x7ffac6fe9896 in gfx::WindowImpl::WndProc C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window\_impl.cc:307  

#10 0x7ffac6fe81b1 in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> C:\b\s\w\ir\cache\builder\src\base\win\wrapped\_window\_proc.h:74  

#11 0x7ffb9471e857 in CallWindowProcW+0x3f7 (C:\WINDOWS\System32\user32.dll+0x18000e857)  

#12 0x7ffb9471e3db in DispatchMessageW+0x39b (C:\WINDOWS\System32\user32.dll+0x18000e3db)  

#13 0x7ffb94730bc2 in SendMessageTimeoutW+0x142 (C:\WINDOWS\System32\user32.dll+0x180020bc2)  

#14 0x7ffb953f0ba3 in KiUserCallbackDispatcher+0x23 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800a0ba3)  

#15 0x7ffb92ba2383 in NtUserDestroyWindow+0x13 (C:\WINDOWS\System32\win32u.dll+0x180002383)  

#16 0x7ffac3c08579 in views::Widget::CloseNow C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:700  

#17 0x7ffad141c600 in EyeDropperView::~EyeDropperView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\eye\_dropper\eye\_dropper\_view.cc:193  

#18 0x7ffad141e91d in EyeDropperView::~EyeDropperView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\eye\_dropper\eye\_dropper\_view.cc:191  

#19 0x7ffabd05a54c in content::EyeDropperChooserImpl::ColorSelected C:\b\s\w\ir\cache\builder\src\content\browser\eye\_dropper\_chooser\_impl.cc:68  

#20 0x7ffad141e017 in EyeDropperView::OnColorSelected C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\eye\_dropper\eye\_dropper\_view.cc:322  

#21 0x7fface2a591d in EyeDropperView::PreEventDispatchHandler::OnMouseEvent C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\eye\_dropper\eye\_dropper\_view\_aura.cc:74  

#22 0x7ffac4ba9d61 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:190  

#23 0x7ffac4ba9b12 in ui::EventDispatcher::DispatchEventToEventHandlers C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:177  

#24 0x7ffac4ba90cc in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:125  

#25 0x7ffac4ba8b6b in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:83  

#26 0x7ffac4ba87ac in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:55  

#27 0x7ffac9941c66 in ui::EventProcessor::OnEventFromSource C:\b\s\w\ir\cache\builder\src\ui\events\event\_processor.cc:49  

#28 0x7ffac68b5d77 in ui::EventSource::DeliverEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:118  

#29 0x7ffac68b59d1 in ui::EventSource::SendEventToSinkFromRewriter C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:143  

#30 0x7ffac68b54d3 in ui::EventSource::SendEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:112  

#31 0x7ffac993f771 in views::DesktopWindowTreeHostWin::HandleMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_window\_tree\_host\_win.cc:1004  

#32 0x7ffacd87adea in views::HWNDMessageHandler::HandleMouseEventInternal C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:3159  

#33 0x7ffacd87421b in views::HWNDMessageHandler::\_ProcessWindowMessage C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.h:358  

#34 0x7ffacd8738ba in views::HWNDMessageHandler::OnWndProc C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:1027  

#35 0x7ffac6fe9896 in gfx::WindowImpl::WndProc C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window\_impl.cc:307  

#36 0x7ffac6fe81b1 in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> C:\b\s\w\ir\cache\builder\src\base\win\wrapped\_window\_proc.h:74  

#37 0x7ffb9471e857 in CallWindowProcW+0x3f7 (C:\WINDOWS\System32\user32.dll+0x18000e857)  

#38 0x7ffb9471e298 in DispatchMessageW+0x258 (C:\WINDOWS\System32\user32.dll+0x18000e298)  

#39 0x7ffac3f74378 in base::MessagePumpForUI::ProcessMessageHelper C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:542  

#40 0x7ffac3f723a9 in base::MessagePumpForUI::ProcessNextWindowsMessage C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:504  

#41 0x7ffac3f71ca3 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:215  

#42 0x7ffac3f6ffd8 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#43 0x7ffac6c8eee0 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:497  

#44 0x7ffac3e42d43 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#45 0x7ffabccd350d in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1073  

#46 0x7ffabccd8b77 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:155  

#47 0x7ffabcccca09 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#48 0x7ffac3a7744b in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:642  

#49 0x7ffac3a7a5b6 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1175  

#50 0x7ffac3a796f6 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1042  

#51 0x7ffac3a760c7 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:401  

#52 0x7ffac3a7684b in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:429  

#53 0x7ffab8ce14ca in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:176  

#54 0x7ff6ff735b16 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:167  

#55 0x7ff6ff732b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#56 0x7ff6ffb2d2a3 in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#57 0x7ffb93b67033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#58 0x7ffb953a2650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

0x11d1382d1ce0 is located 96 bytes inside of 504-byte region [0x11d1382d1c80,0x11d1382d1e78)  

freed by thread T0 here:  

#0 0x7ff6ff7dd28b in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ffac560981f in aura::Window::~Window C:\b\s\w\ir\cache\builder\src\ui\aura\window.cc:183  

#2 0x7ffabdc67287 in content::WebContentsViewAura::~WebContentsViewAura C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_view\_aura.cc:705  

#3 0x7ffabdc747f7 in content::WebContentsViewAura::~WebContentsViewAura C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_view\_aura.cc:697  

#4 0x7ffabdbf8b5a in content::WebContentsImpl::AttachInnerWebContents C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:2446  

#5 0x7ffabd501aa6 in content::Portal::CreateProxyAndAttachPortal C:\b\s\w\ir\cache\builder\src\content\browser\portal\portal.cc:169  

#6 0x7ffabd7fd7c3 in content::RenderFrameHostImpl::AdoptPortal C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:6976  

#7 0x7ffabbf06711 in content::mojom::FrameHostStubDispatch::AcceptWithResponder C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\content\common\frame.mojom.cc:6117  

#8 0x7ffabd847c72 in content::mojom::FrameHostStub<mojo::RawPtrImplRefTraits[content::mojom::FrameHost](javascript:void(0);) >::AcceptWithResponder C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\content\common\frame.mojom.h:702  

#9 0x7ffac41f7e67 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:884  

#10 0x7ffac6dcf15d in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:48  

#11 0x7ffac41fbaea in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:664  

#12 0x7ffac4b0d2b0 in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptSyncMessage C:\b\s\w\ir\cache\builder\src\ipc\ipc\_mojo\_bootstrap.cc:1050  

#13 0x7ffac3ec3074 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#14 0x7ffac6c8d7b5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:385  

#15 0x7ffac6c8cd89 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:290  

#16 0x7ffac3f71d46 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#17 0x7ffac3f6ffd8 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#18 0x7ffac6c8eee0 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:497  

#19 0x7ffac3e42d43 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#20 0x7ffabccd350d in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1073  

#21 0x7ffabccd8b77 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:155  

#22 0x7ffabcccca09 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#23 0x7ffac3a7744b in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:642  

#24 0x7ffac3a7a5b6 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1175  

#25 0x7ffac3a796f6 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1042  

#26 0x7ffac3a760c7 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:401  

#27 0x7ffac3a7684b in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:429

previously allocated by thread T0 here:  

#0 0x7ff6ff7dd38b in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffad667db9e in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ffabdc6a05d in content::WebContentsViewAura::CreateAuraWindow C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_view\_aura.cc:976  

#3 0x7ffabdc6a616 in content::WebContentsViewAura::CreateView C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_view\_aura.cc:1021  

#4 0x7ffabdc01af5 in content::WebContentsImpl::Init C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:3054  

#5 0x7ffabdbdf62b in content::WebContents::CreateWithSessionStorage C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:598  

#6 0x7ffacb9e35ba in chrome::`anonymous namespace'::CreateRestoredTab C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser\_tabrestore.cc:80  

#7 0x7ffacb9e2f7e in chrome::AddRestoredTab C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser\_tabrestore.cc:238  

#8 0x7ffacb994024 in SessionRestoreImpl::RestoreTab C:\b\s\w\ir\cache\builder\src\chrome\browser\sessions\session\_restore.cc:806  

#9 0x7ffacb991347 in SessionRestoreImpl::RestoreTabsToBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\sessions\session\_restore.cc:755  

#10 0x7ffacb98f1b9 in SessionRestoreImpl::ProcessSessionWindows C:\b\s\w\ir\cache\builder\src\chrome\browser\sessions\session\_restore.cc:601  

#11 0x7ffacb98c714 in SessionRestoreImpl::ProcessSessionWindowsAndNotify C:\b\s\w\ir\cache\builder\src\chrome\browser\sessions\session\_restore.cc:488  

#12 0x7ffacb98d18c in SessionRestoreImpl::ProcessSessionWindowsIfReady C:\b\s\w\ir\cache\builder\src\chrome\browser\sessions\session\_restore.cc:463  

#13 0x7ffac3ec3074 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#14 0x7ffac6c8d7b5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:385  

#15 0x7ffac6c8cd89 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:290  

#16 0x7ffac3f71d46 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#17 0x7ffac3f6ffd8 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#18 0x7ffac6c8eee0 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:497  

#19 0x7ffac3e42d43 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#20 0x7ffabccd350d in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1073  

#21 0x7ffabccd8b77 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:155  

#22 0x7ffabcccca09 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#23 0x7ffac3a7744b in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:642  

#24 0x7ffac3a7a5b6 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1175  

#25 0x7ffac3a796f6 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1042  

#26 0x7ffac3a760c7 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:401  

#27 0x7ffac3a7684b in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:429

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\ui\events\event\_target.cc:54 in ui::EventTarget::RemovePreTargetHandler  

Shadow bytes around the buggy address:  

0x03e15f15a340: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x03e15f15a350: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x03e15f15a360: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x03e15f15a370: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 fa fa  

0x03e15f15a380: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x03e15f15a390: fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd fd fd  

0x03e15f15a3a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03e15f15a3b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03e15f15a3c0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x03e15f15a3d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x03e15f15a3e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==7044==ABORTING

**CREDIT INFORMATION**  

Reporter credit: Thomas Orlita

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 212 B)
- [portal.html](attachments/portal.html) (text/plain, 163 B)
- [uaf.mp4](attachments/uaf.mp4) (video/mp4, 480.2 KB)

## Timeline

### [Deleted User] (2022-03-05)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-03-08)

I'm not sure how to repro this in Clusterfuzz since it requires a click. But I was able to reproduce locally.

High because browser use-after-free, but impact none since the feature is (as far as I know) off by default.

Marking as FoundIn-

[Monorail components: Blink>Forms>Color Blink>Portals]

### dc...@chromium.org (2022-03-08)

Oops, forgot to finish the comment. Marked as FoundIn-94 because this was likely introduced by https://chromium-review.googlesource.com/c/chromium/src/+/3042977.

(mcnee, feel free to hand this off, but since this is related to a tricky bit of portals activation, I think it might help if the portals team helped find a good pattern for this)

### xi...@chromium.org (2022-03-18)

Raising to P1 since it's high severity security bug.

### mc...@chromium.org (2022-03-30)

CL: https://chromium-review.googlesource.com/c/chromium/src/+/3561542

Note that the eye dropper has issues with normal navigations as well, though fortunately not in a way that causes memory safety issues. I've filed https://crbug.com/chromium/1311751 for that. A fix for 1311751 would be more robust for portals as well (at least with an MPArch implementation), but this CL addresses the immediate issue.

Also this issue is aura specific.

### gi...@appspot.gserviceaccount.com (2022-03-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/27e89c3e879feebba252928d16ed8c1f4860444d

commit 27e89c3e879feebba252928d16ed8c1f4860444d
Author: Kevin McNee <mcnee@chromium.org>
Date: Wed Mar 30 19:56:09 2022

Ensure EyeDropperView does not access a destroyed window

In its current multi-WebContents architecture, portal adoption destroys
the aura::Window of the navigated away from page. If the eye dropper is
closed after this point, it would dereference the destroyed
aura::Window. We now confirm the window still exists.

Note that the eye dropper experiences issues with regular navigations as
well, though fortunately not in a way that is a memory safety issue.
I've filed https://crbug.com/chromium/1311751 for that.

Bug: 1303330
Change-Id: I7856f867e9bfd72ee3904bc2bdcb0ee92289d277
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3561542
Commit-Queue: Kevin McNee <mcnee@chromium.org>
Auto-Submit: Kevin McNee <mcnee@chromium.org>
Reviewed-by: Ionel Popescu <iopopesc@microsoft.com>
Commit-Queue: Ionel Popescu <iopopesc@microsoft.com>
Cr-Commit-Position: refs/heads/main@{#987128}

[modify] https://crrev.com/27e89c3e879feebba252928d16ed8c1f4860444d/chrome/browser/ui/views/eye_dropper/eye_dropper_view_aura.cc


### mc...@chromium.org (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-31)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-11)

Congratulations, Thomas! The VRP Panel has decided to award you $15,000 for this report. Thank you for your efforts and great work! 

### am...@google.com (2022-04-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-07-07)

This issue was migrated from crbug.com/chromium/1303330?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Forms>Color, Blink>Portals]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058989)*
