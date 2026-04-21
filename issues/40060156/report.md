# Security: UAF in CloseBubbleOnTabActivationHelper::~CloseBubbleOnTabActivationHelper

| Field | Value |
|-------|-------|
| **Issue ID** | [40060156](https://issues.chromium.org/issues/40060156) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Views, UI>Browser>WebUI |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | yo...@snu.ac.kr |
| **Assignee** | tl...@chromium.org |
| **Created** | 2022-07-04 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/close_bubble_on_tab_activation_helper.h;l=43;drc=add83b6797a5ad031419a9adc0524dd1d83af5bf>

`CloseBubbleOnTabActivationHelper` has a raw pointer of `browser`.

But `CloseBubbleOnTabActivationHelper::~CloseBubbleOnTabActivationHelper` can be called after the `Browser::~Browser` is called.

So it cause a Use-After-Free.

**VERSION**  

Chrome Version: asan-win32-release\_x64-1007777 (104.0.5085.0 (Developer Build) (64-bit))  

Operating System: Windows 10 Version 21H1 (Build 19043.1766)

**REPRODUCTION CASE**

Unfortunately, I can't reproduce it again.

I think some delays are needed for triggering.

So I leave a few behaviors that were trying to trigger this bug.

- make new windows
- make new tabs
- click the tab search UI

Additionally, I used only mouse clicks.

# Type of crash: browser Crash State: C:\Users\user\Downloads\win32-release\_x64\_asan-win32-release\_x64-1007777\asan-win32-release\_x64-1007777>chrome.exe --user-data-dir="C:\data" [52096:75068:0615/195012.115:ERROR:device\_event\_log\_impl.cc(214)] [19:50:12.118] USB: usb\_device\_handle\_win.cc:1048 Failed to read descriptor from node connection: A device attached to the system is not functioning. (0x1F) [52096:75068:0615/195012.125:ERROR:device\_event\_log\_impl.cc(214)] [19:50:12.130] USB: usb\_device\_handle\_win.cc:1048 Failed to read descriptor from node connection: A device attached to the system is not functioning. (0x1F) [52096:75068:0615/195106.875:ERROR:interface\_endpoint\_client.cc(665)] Message 5 rejected by interface blink.mojom.WidgetHost [37712:73136:0615/195208.334:ERROR:gpu\_init.cc(484)] Passthrough is not supported, GL is disabled, ANGLE is [52096:75068:0615/195403.192:ERROR:CONSOLE(1078)] "Uncaught (in promise) TypeError: Cannot read properties of undefined (reading 'height')", source: chrome://tab-search.top-chrome/tab\_search.js (1078)

==52096==ERROR: AddressSanitizer: heap-use-after-free on address 0x11df39136e38 at pc 0x7ff8f06193c3 bp 0x0048763fe570 sp 0x0048763fe5b8  

READ of size 8 at 0x11df39136e38 thread T0  

==52096==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ff8f06193c2 in CloseBubbleOnTabActivationHelper::~CloseBubbleOnTabActivationHelper C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\close\_bubble\_on\_tab\_activation\_helper.cc:22  

#1 0x7ff8f060c403 in WebUIBubbleManager::OnWidgetDestroying C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\bubble\webui\_bubble\_manager.cc:71  

#2 0x7ff8e2705b2a in views::Widget::OnNativeWidgetDestroying C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1413  

#3 0x7ff8e86710c1 in views::DesktopWindowTreeHostWin::HandleDestroying C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_window\_tree\_host\_win.cc:920  

#4 0x7ff8ec7a9b90 in views::HWNDMessageHandler::OnDestroy C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:1750  

#5 0x7ff8ec79e099 in views::HWNDMessageHandler::\_ProcessWindowMessage C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.h:433  

#6 0x7ff8ec799d1d in views::HWNDMessageHandler::OnWndProc C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:1092  

#7 0x7ff8e5c3f240 in gfx::WindowImpl::WndProc C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window\_impl.cc:306  

#8 0x7ff8e5c3dbb1 in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> C:\b\s\w\ir\cache\builder\src\base\win\wrapped\_window\_proc.h:74  

#9 0x7ff9d706e857 in CallWindowProcW+0x3f7 (C:\Windows\System32\user32.dll+0x18000e857)  

#10 0x7ff9d706e3db in DispatchMessageW+0x39b (C:\Windows\System32\user32.dll+0x18000e3db)  

#11 0x7ff9d7080bc2 in SendMessageTimeoutW+0x142 (C:\Windows\System32\user32.dll+0x180020bc2)  

#12 0x7ff9d9090b73 in KiUserCallbackDispatcher+0x23 (C:\Windows\SYSTEM32\ntdll.dll+0x1800a0b73)  

#13 0x7ff9d6c32383 in NtUserDestroyWindow+0x13 (C:\Windows\System32\win32u.dll+0x180002383)  

#14 0x7ff8e29e4ad4 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#15 0x7ff8e59068cd in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:422  

#16 0x7ff8e5905aca in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:300  

#17 0x7ff8e2a9bbf6 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:214  

#18 0x7ff8e2a99ea4 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#19 0x7ff8e59083ea in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:542  

#20 0x7ff8e2948877 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#21 0x7ff8db36bcf7 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1039  

#22 0x7ff8db3710bf in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:157  

#23 0x7ff8db36523d in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#24 0x7ff8e2501b3b in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:660  

#25 0x7ff8e2504cb4 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1167  

#26 0x7ff8e2503de6 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1039  

#27 0x7ff8e25007b3 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:407  

#28 0x7ff8e2500f3c in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:435  

#29 0x7ff8d70d14be in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:177  

#30 0x7ff7da535d52 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:167  

#31 0x7ff7da532b74 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:385  

#32 0x7ff7da93bbdf in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#33 0x7ff9d8257033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#34 0x7ff9d9042650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

0x11df39136e38 is located 440 bytes inside of 1016-byte region [0x11df39136c80,0x11df39137078)  

freed by thread T0 here:  

#0 0x7ff7da5de9bb in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ff8e4fd55f5 in Browser::~Browser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser.cc:575  

#2 0x7ff8e8c00328 in BrowserView::~BrowserView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser\_view.cc:994  

#3 0x7ff8e8c1a615 in BrowserView::`vector deleting destructor'+0x19 (C:\Users\user\Downloads\win32-release\_x64\_asan-win32-release\_x64-1007777\asan-win32-release\_x64-1007777\chrome.dll+0x191b4a615)  

#4 0x7ff8e26c9d14 in views::View::~View C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:254  

#5 0x7ff8f1527743 in GlassBrowserFrameView::~GlassBrowserFrameView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\glass\_browser\_frame\_view.cc:121  

#6 0x7ff8e27181e3 in views::NonClientView::~NonClientView C:\b\s\w\ir\cache\builder\src\ui\views\window\non\_client\_view.cc:169  

#7 0x7ff8e2719f05 in views::NonClientView::~NonClientView C:\b\s\w\ir\cache\builder\src\ui\views\window\non\_client\_view.cc:165  

#8 0x7ff8e26cbee2 in views::View::DoRemoveChildView C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:2682  

#9 0x7ff8e26cc232 in views::View::RemoveAllChildViews C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:329  

#10 0x7ff8e26fa3f9 in views::Widget::DestroyRootView C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1807  

#11 0x7ff8e26f9ffb in views::Widget::~Widget C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:206  

#12 0x7ff8ea70c579 in BrowserFrame::~BrowserFrame C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser\_frame.cc:88  

#13 0x7ff8ec7ba15c in views::DesktopNativeWidgetAura::~DesktopNativeWidgetAura C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_native\_widget\_aura.cc:314  

#14 0x7ff8f2c2eedb in DesktopBrowserFrameAura::~DesktopBrowserFrameAura C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\desktop\_browser\_frame\_aura.cc:39  

#15 0x7ff8ec799e79 in views::HWNDMessageHandler::OnWndProc C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:1109  

#16 0x7ff8e5c3f240 in gfx::WindowImpl::WndProc C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window\_impl.cc:306  

#17 0x7ff8e5c3dbb1 in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> C:\b\s\w\ir\cache\builder\src\base\win\wrapped\_window\_proc.h:74  

#18 0x7ff9d706e857 in CallWindowProcW+0x3f7 (C:\Windows\System32\user32.dll+0x18000e857)  

#19 0x7ff9d706e3db in DispatchMessageW+0x39b (C:\Windows\System32\user32.dll+0x18000e3db)  

#20 0x7ff9d7086a27 in GetLastInputInfo+0x77 (C:\Windows\System32\user32.dll+0x180026a27)  

#21 0x7ff9d9090b73 in KiUserCallbackDispatcher+0x23 (C:\Windows\SYSTEM32\ntdll.dll+0x1800a0b73)  

#22 0x7ff9d6c32383 in NtUserDestroyWindow+0x13 (C:\Windows\System32\win32u.dll+0x180002383)  

#23 0x7ff8e29e4ad4 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#24 0x7ff8e59068cd in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:422  

#25 0x7ff8e5905aca in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:300  

#26 0x7ff8e2a9bbf6 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:214  

#27 0x7ff8e2a99ea4 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78

previously allocated by thread T0 here:  

#0 0x7ff7da5deabb in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ff8f5d2346e in operator new d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ff8e4fc1377 in Browser::Create C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser.cc:456  

#3 0x7ff8ecc00fbb in StartupBrowserCreatorImpl::OpenTabsInBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup\_browser\_creator\_impl.cc:247  

#4 0x7ff8ecc03cc4 in StartupBrowserCreatorImpl::RestoreOrCreateBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup\_browser\_creator\_impl.cc:649  

#5 0x7ff8ecc007f8 in StartupBrowserCreatorImpl::DetermineURLsAndLaunch C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup\_browser\_creator\_impl.cc:445  

#6 0x7ff8ecbffc35 in StartupBrowserCreatorImpl::Launch C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup\_browser\_creator\_impl.cc:170  

#7 0x7ff8e8834fa0 in StartupBrowserCreator::LaunchBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup\_browser\_creator.cc:682  

#8 0x7ff8e8835b82 in StartupBrowserCreator::LaunchBrowserForLastProfiles C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup\_browser\_creator.cc:747  

#9 0x7ff8e883483e in StartupBrowserCreator::ProcessCmdLineImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup\_browser\_creator.cc:1237  

#10 0x7ff8e8832613 in StartupBrowserCreator::Start C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup\_browser\_creator.cc:637  

#11 0x7ff8e560f5a0 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome\_browser\_main.cc:1753  

#12 0x7ff8e560db40 in ChromeBrowserMainParts::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome\_browser\_main.cc:1152  

#13 0x7ff8db36952b in content::BrowserMainLoop::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:959  

#14 0x7ff8dc2a6129 in content::StartupTaskRunner::RunAllTasksNow C:\b\s\w\ir\cache\builder\src\content\browser\startup\_task\_runner.cc:43  

#15 0x7ff8db368966 in content::BrowserMainLoop::CreateStartupTasks C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:870  

#16 0x7ff8db3705c8 in content::BrowserMainRunnerImpl::Initialize C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:136  

#17 0x7ff8db3651e8 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:26  

#18 0x7ff8e2501b3b in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:660  

#19 0x7ff8e2504cb4 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1167  

#20 0x7ff8e2503de6 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1039  

#21 0x7ff8e25007b3 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:407  

#22 0x7ff8e2500f3c in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:435  

#23 0x7ff8d70d14be in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:177  

#24 0x7ff7da535d52 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:167  

#25 0x7ff7da532b74 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:385  

#26 0x7ff7da93bbdf in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#27 0x7ff9d8257033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\close\_bubble\_on\_tab\_activation\_helper.cc:22 in CloseBubbleOnTabActivationHelper::~CloseBubbleOnTabActivationHelper  

Shadow bytes around the buggy address:  

0x03e920226d70: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x03e920226d80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x03e920226d90: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03e920226da0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03e920226db0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x03e920226dc0: fd fd fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd  

0x03e920226dd0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03e920226de0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03e920226df0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03e920226e00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x03e920226e10: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

==52096==ABORTING

**CREDIT INFORMATION**  

Reporter credit: YoungJoo Lee(@ashuu\_lee) of CompSecLab at Seoul National University

## Timeline

### [Deleted User] (2022-07-04)

[Empty comment from Monorail migration]

### yo...@snu.ac.kr (2022-07-04)

I forgot to mention the most important step.
Closing tabs or windows is needed.
So I edited the behaviors.

- make new windows
- make new tabs
- click the tab search UI
- close the tabs or windows

### da...@chromium.org (2022-07-05)

=> ellyjones to triage

~CloseBubbleOnTabActivationHelper is running inside the windows event handler to destroy the window, and after Browser is destructed.

Closing a window is web-accessible, right?

[Monorail components: Internals>Views UI>Browser>WebUI]

### da...@chromium.org (2022-07-05)

The helper has been destroyed in this way, and called into Browser* in the destructor, since:

Commit d6a87dd : yuhengh@chromium.org @ 2020-11-10 9:34 PM
Tab Search: fix CloseBubbleOnTabActivationHelper not reset correctly



### da...@chromium.org (2022-07-05)

[Empty comment from Monorail migration]

### da...@chromium.org (2022-07-05)

yuhengh can you triage?

### [Deleted User] (2022-07-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-05)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2022-07-05)

(auto-cc on security bug)

### tl...@chromium.org (2022-07-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-07-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7c209778702c4f291c6d3b1fb9ac3cc803e0d90a

commit 7c209778702c4f291c6d3b1fb9ac3cc803e0d90a
Author: Tom Lukaszewicz <tluk@chromium.org>
Date: Mon Jul 11 20:53:32 2022

Fix UAF in CloseBubbleOnTabActivationHelper

There are circumstances where a bubble may outlive its hosting
browser window (e.g. the browser is closed before the attached
bubble).

This CL adds an observation on the BrowserList to nullify the
Browser member if the Browser is destroyed before the activation
helper.

Bug: 1341603
Change-Id: Ife3a5072b7009f8b42c6c68098c0245798384451
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3753347
Commit-Queue: Thomas Lukaszewicz <tluk@chromium.org>
Reviewed-by: Elly Fong-Jones <ellyjones@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1022874}

[modify] https://crrev.com/7c209778702c4f291c6d3b1fb9ac3cc803e0d90a/chrome/browser/ui/views/close_bubble_on_tab_activation_helper.cc
[modify] https://crrev.com/7c209778702c4f291c6d3b1fb9ac3cc803e0d90a/chrome/browser/ui/views/close_bubble_on_tab_activation_helper.h


### tl...@chromium.org (2022-07-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-12)

Requesting merge to extended stable M102 because latest trunk commit (1022874) appears to be after extended stable branch point (992738).

Requesting merge to stable M103 because latest trunk commit (1022874) appears to be after stable branch point (1002911).

Requesting merge to beta M104 because latest trunk commit (1022874) appears to be after beta branch point (1012729).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-12)

Merge review required: M104 is already shipping to beta.

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
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-12)

Merge review required: M103 is already shipping to stable.

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

### [Deleted User] (2022-07-12)

Merge review required: M102 is already shipping to stable.

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
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-14)

M104 merge approved, please merge this fix to branch 5112 at your earliest convenience 

M103 and M102 merges approved, please merge this fix to M103/stable (branch 5060) and M102/extended stable (branch 5005) by 12p tomorrow (Friday, 15 July) so this fix can be included in the next stable and extended stable security respins. Thanks! 

### gi...@appspot.gserviceaccount.com (2022-07-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3ef803214059615cfc6bef6fad9ff48644335e68

commit 3ef803214059615cfc6bef6fad9ff48644335e68
Author: Tom Lukaszewicz <tluk@chromium.org>
Date: Fri Jul 15 18:56:19 2022

[M104 Merge]Fix UAF in CloseBubbleOnTabActivationHelper

There are circumstances where a bubble may outlive its hosting
browser window (e.g. the browser is closed before the attached
bubble).

This CL adds an observation on the BrowserList to nullify the
Browser member if the Browser is destroyed before the activation
helper.

(cherry picked from commit 7c209778702c4f291c6d3b1fb9ac3cc803e0d90a)

Bug: 1341603
Change-Id: Ife3a5072b7009f8b42c6c68098c0245798384451
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3753347
Commit-Queue: Thomas Lukaszewicz <tluk@chromium.org>
Reviewed-by: Elly Fong-Jones <ellyjones@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1022874}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3764897
Commit-Queue: Prudhvikumar Bommana <pbommana@google.com>
Owners-Override: Prudhvikumar Bommana <pbommana@google.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5112@{#921}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/3ef803214059615cfc6bef6fad9ff48644335e68/chrome/browser/ui/views/close_bubble_on_tab_activation_helper.cc
[modify] https://crrev.com/3ef803214059615cfc6bef6fad9ff48644335e68/chrome/browser/ui/views/close_bubble_on_tab_activation_helper.h


### [Deleted User] (2022-07-15)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-07-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b8744cd260749f0f85bacbca7b805e21cc527a29

commit b8744cd260749f0f85bacbca7b805e21cc527a29
Author: Tom Lukaszewicz <tluk@chromium.org>
Date: Fri Jul 15 19:12:49 2022

[M103 Merge] Fix UAF in CloseBubbleOnTabActivationHelper

There are circumstances where a bubble may outlive its hosting
browser window (e.g. the browser is closed before the attached
bubble).

This CL adds an observation on the BrowserList to nullify the
Browser member if the Browser is destroyed before the activation
helper.

(cherry picked from commit 7c209778702c4f291c6d3b1fb9ac3cc803e0d90a)

Bug: 1341603
Change-Id: Ife3a5072b7009f8b42c6c68098c0245798384451
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3753347
Commit-Queue: Thomas Lukaszewicz <tluk@chromium.org>
Reviewed-by: Elly Fong-Jones <ellyjones@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1022874}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3764392
Owners-Override: Prudhvikumar Bommana <pbommana@google.com>
Commit-Queue: Prudhvikumar Bommana <pbommana@google.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Prudhvikumar Bommana <pbommana@google.com>
Cr-Commit-Position: refs/branch-heads/5060@{#1236}
Cr-Branched-From: b83393d0f4038aeaf67f970a024d8101df7348d1-refs/heads/main@{#1002911}

[modify] https://crrev.com/b8744cd260749f0f85bacbca7b805e21cc527a29/chrome/browser/ui/views/close_bubble_on_tab_activation_helper.cc
[modify] https://crrev.com/b8744cd260749f0f85bacbca7b805e21cc527a29/chrome/browser/ui/views/close_bubble_on_tab_activation_helper.h


### gi...@appspot.gserviceaccount.com (2022-07-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2997342dbf8711f4dcf89c575cfce5ca95fdc7b9

commit 2997342dbf8711f4dcf89c575cfce5ca95fdc7b9
Author: Tom Lukaszewicz <tluk@chromium.org>
Date: Fri Jul 15 20:38:39 2022

[M102 Merge] Fix UAF in CloseBubbleOnTabActivationHelper

There are circumstances where a bubble may outlive its hosting
browser window (e.g. the browser is closed before the attached
bubble).

This CL adds an observation on the BrowserList to nullify the
Browser member if the Browser is destroyed before the activation
helper.

(cherry picked from commit 7c209778702c4f291c6d3b1fb9ac3cc803e0d90a)

Bug: 1341603
Change-Id: Ife3a5072b7009f8b42c6c68098c0245798384451
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3753347
Commit-Queue: Thomas Lukaszewicz <tluk@chromium.org>
Reviewed-by: Elly Fong-Jones <ellyjones@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1022874}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3766064
Owners-Override: Prudhvikumar Bommana <pbommana@google.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/5005@{#1252}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/2997342dbf8711f4dcf89c575cfce5ca95fdc7b9/chrome/browser/ui/views/close_bubble_on_tab_activation_helper.cc
[modify] https://crrev.com/2997342dbf8711f4dcf89c575cfce5ca95fdc7b9/chrome/browser/ui/views/close_bubble_on_tab_activation_helper.h


### rz...@google.com (2022-07-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-18)

[Empty comment from Monorail migration]

### rz...@google.com (2022-07-19)

[Empty comment from Monorail migration]

### rz...@google.com (2022-07-19)

Already merged to 102

### [Deleted User] (2022-07-19)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-07-19)

1. https://crrev.com/c/3767446
2. Low, no conflicts
3. 102, 103, 104
4. Yes

### gm...@google.com (2022-07-19)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-07-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3ac97b720fd908ce13088abaf84d6ce2fd46f41c

commit 3ac97b720fd908ce13088abaf84d6ce2fd46f41c
Author: Tom Lukaszewicz <tluk@chromium.org>
Date: Wed Jul 20 09:45:23 2022

[M96-LTS] Fix UAF in CloseBubbleOnTabActivationHelper

There are circumstances where a bubble may outlive its hosting
browser window (e.g. the browser is closed before the attached
bubble).

This CL adds an observation on the BrowserList to nullify the
Browser member if the Browser is destroyed before the activation
helper.

(cherry picked from commit 7c209778702c4f291c6d3b1fb9ac3cc803e0d90a)

Bug: 1341603
Change-Id: Ife3a5072b7009f8b42c6c68098c0245798384451
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3753347
Commit-Queue: Thomas Lukaszewicz <tluk@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1022874}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3767446
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Simon Hangl <simonha@google.com>
Owners-Override: Simon Hangl <simonha@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1664}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/3ac97b720fd908ce13088abaf84d6ce2fd46f41c/chrome/browser/ui/views/close_bubble_on_tab_activation_helper.cc
[modify] https://crrev.com/3ac97b720fd908ce13088abaf84d6ce2fd46f41c/chrome/browser/ui/views/close_bubble_on_tab_activation_helper.h


### rz...@google.com (2022-07-20)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2022-07-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-21)

Congratulations, YoungJoo Lee! The VRP Panel has decided to award you $2,000 for this report. The amount decided was based on this issue not being web accessible and mitigated by user interaction. Future issues that do not have a POC, steps to reproduce, or other evidence of exploitability may receive lower reward amounts. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-07-22)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1341603?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Views, UI>Browser>WebUI]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060156)*
