# Security: Use-After-Free in WebUIBubbleDialogView::ClearContentsWrapper

| Field | Value |
|-------|-------|
| **Issue ID** | [40060325](https://issues.chromium.org/issues/40060325) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Bubbles |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | yo...@snu.ac.kr |
| **Assignee** | tl...@chromium.org |
| **Created** | 2022-07-19 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

I found a UAF that has a similar root-cause with 1343686, 1344028.

But I am not sure whether this vulnerability is related to them.

Because I can't find other logs like 1343686 or 1344028.

It is triggered by `BubbleContentsWrapperT<TabSearchUI>::BubbleContentsWrapperT` object.

I will attach the asan log and poc video.

**VERSION**  

Chrome Version: 104.0.5107 (win32-release\_x64\_asan-win32-release\_x64-1011400)  

Operating System: Windows 10 Version 21H2 (Build 19044.1826)

**REPRODUCTION CASE**

1. Click "Customize Profile".
2. Click theme colors and "Search Tabs".
3. Close the window.

In my opinion, if there is a way to delete the "View" that has a BubbleContentsWrapperT<TabSearchUI>, this vulnerability can be triggered without clicking theme colors.

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: browser Crash State:

==6740==ERROR: AddressSanitizer: heap-use-after-free on address 0x123f5534cb90 at pc 0x7ffb5269816e bp 0x00a6553fe660 sp 0x00a6553fe6a8  

READ of size 8 at 0x123f5534cb90 thread T0  

==6740==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ffb5269816d in WebUIBubbleDialogView::ClearContentsWrapper C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\bubble\webui\_bubble\_dialog\_view.cc:79  

#1 0x7ffb52697e79 in WebUIBubbleDialogView::~WebUIBubbleDialogView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\bubble\webui\_bubble\_dialog\_view.cc:70  

#2 0x7ffb52698eb8 in WebUIBubbleDialogView::`vector deleting destructor'+0x16 (C:\fuzz\chrome\chrome.dll+0x1995b8eb8)  

#3 0x7ffb447da0c3 in views::WidgetDelegate::DeleteDelegate C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget\_delegate.cc:247  

#4 0x7ffb447d017f in views::Widget::OnNativeWidgetDestroyed C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1423  

#5 0x7ffb4e867263 in views::DesktopNativeWidgetAura::OnHostClosed C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_native\_widget\_aura.cc:388  

#6 0x7ffb4e846229 in views::HWNDMessageHandler::OnWndProc C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:1109  

#7 0x7ffb47d05350 in gfx::WindowImpl::WndProc C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window\_impl.cc:306  

#8 0x7ffb47d03cc1 in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> C:\b\s\w\ir\cache\builder\src\base\win\wrapped\_window\_proc.h:74  

#9 0x7ffbad06e857 in CallWindowProcW+0x3f7 (C:\Windows\System32\user32.dll+0x18000e857)  

#10 0x7ffbad06e3db in DispatchMessageW+0x39b (C:\Windows\System32\user32.dll+0x18000e3db)  

#11 0x7ffbad086a27 in GetLastInputInfo+0x77 (C:\Windows\System32\user32.dll+0x180026a27)  

#12 0x7ffbadc90d73 in KiUserCallbackDispatcher+0x23 (C:\Windows\SYSTEM32\ntdll.dll+0x1800a0d73)  

#13 0x7ffbab412383 in NtUserDestroyWindow+0x13 (C:\Windows\System32\win32u.dll+0x180002383)  

#14 0x7ffb44aae1d4 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#15 0x7ffb479cc8dd in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:422  

#16 0x7ffb479cbada in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:300  

#17 0x7ffb44b63016 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:214  

#18 0x7ffb44b612c4 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#19 0x7ffb479ce3fa in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:542  

#20 0x7ffb44a12087 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#21 0x7ffb3d3b1ae7 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1039  

#22 0x7ffb3d3b6ecb in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:157  

#23 0x7ffb3d3ab02d in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#24 0x7ffb445cb1bf in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:678  

#25 0x7ffb445ce515 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1188  

#26 0x7ffb445cd633 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1059  

#27 0x7ffb445c9e37 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:407  

#28 0x7ffb445ca5c0 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:435  

#29 0x7ffb390e14be in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:177  

#30 0x7ff6315d5d52 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:167  

#31 0x7ff6315d2b74 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:385  

#32 0x7ff6319dbbbf in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#33 0x7ffbac587033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#34 0x7ffbadc42650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

0x123f5534cb90 is located 80 bytes inside of 224-byte region [0x123f5534cb40,0x123f5534cc20)  

freed by thread T0 here:  

#0 0x7ff63167e13b in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82 #1 0x7ffb4f249484 in BubbleContentsWrapperT<TabSearchUI>::~BubbleContentsWrapperT C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\bubble\bubble\_contents\_wrapper.h:107  

#2 0x7ffb52694e53 in WebUIBubbleManager::~WebUIBubbleManager C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\bubble\webui\_bubble\_manager.cc:27  

#3 0x7ffb4f247f88 in TabSearchBubbleHost::~TabSearchBubbleHost C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tab\_search\_bubble\_host.cc:70  

#4 0x7ffb4f248ca1 in TabSearchBubbleHost::~TabSearchBubbleHost C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tab\_search\_bubble\_host.cc:70  

#5 0x7ffb55b39a7f in Windows10TabSearchCaptionButton::~Windows10TabSearchCaptionButton C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\windows\_10\_tab\_search\_caption\_button.cc:30  

#6 0x7ffb55b39ffb in Windows10TabSearchCaptionButton::~Windows10TabSearchCaptionButton C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\windows\_10\_tab\_search\_caption\_button.cc:30  

#7 0x7ffb44793ccc in views::View::~View C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:254  

#8 0x7ffb54cbac47 in GlassBrowserCaptionButtonContainer::~GlassBrowserCaptionButtonContainer C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\glass\_browser\_caption\_button\_container.cc:94  

#9 0x7ffb44793ccc in views::View::~View C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:254  

#10 0x7ffb5358ad6d in GlassBrowserFrameView::~GlassBrowserFrameView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\glass\_browser\_frame\_view.cc:121  

#11 0x7ffb447e238e in views::NonClientView::SetFrameView C:\b\s\w\ir\cache\builder\src\ui\views\window\non\_client\_view.cc:185  

#12 0x7ffb447e274a in views::NonClientView::UpdateFrame C:\b\s\w\ir\cache\builder\src\ui\views\window\non\_client\_view.cc:209  

#13 0x7ffb4e844bdb in views::HWNDMessageHandler::PerformDwmTransition C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:3449  

#14 0x7ffb4e86a8bb in views::DesktopNativeWidgetAura::FrameTypeChanged C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_native\_widget\_aura.cc:698  

#15 0x7ffb49840991 in ThemeService::NotifyThemeChanged C:\b\s\w\ir\cache\builder\src\chrome\browser\themes\theme\_service.cc:937  

#16 0x7ffb4983cb7d in ThemeService::UseDefaultTheme C:\b\s\w\ir\cache\builder\src\chrome\browser\themes\theme\_service.cc:668  

#17 0x7ffb3ece105e in customize\_themes::mojom::CustomizeThemesHandlerStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\ui\webui\resources\cr\_components\customize\_themes\customize\_themes.mojom.cc:1053  

#18 0x7ffb44d9e62c in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:922  

#19 0x7ffb47affe6a in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#20 0x7ffb44da23c8 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:664  

#21 0x7ffb44db67ec in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:1096  

#22 0x7ffb44db5660 in mojo::internal::MultiplexRouter::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:716  

#23 0x7ffb47affe6a in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#24 0x7ffb44d9941b in mojo::Connector::DispatchMessageW C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:561  

#25 0x7ffb44d9ac3b in mojo::Connector::ReadAllAvailableMessages C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:618  

#26 0x7ffb44def2a8 in mojo::SimpleWatcher::OnHandleReady C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple\_watcher.cc:278  

#27 0x7ffb44aae1d4 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135

previously allocated by thread T0 here:  

#0 0x7ff63167e23b in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffb57d8fc2e in operator new d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ffb4f248f76 in WebUIBubbleManagerT<TabSearchUI>::CreateWebUIBubbleDialog C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\bubble\webui\_bubble\_manager.h:148  

#3 0x7ffb52695058 in WebUIBubbleManager::ShowBubble C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\bubble\webui\_bubble\_manager.cc:36  

#4 0x7ffb4f2487e8 in TabSearchBubbleHost::ShowTabSearchBubble C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tab\_search\_bubble\_host.cc:127  

#5 0x7ffb4f247e42 in TabSearchBubbleHost::ButtonPressed C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tab\_search\_bubble\_host.cc:155  

#6 0x7ffb4f237012 in views::MenuButtonController::Activate C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\menu\_button\_controller.cc:257  

#7 0x7ffb4f236b3e in views::MenuButtonController::OnMousePressed C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\menu\_button\_controller.cc:109  

#8 0x7ffb447a80be in views::View::ProcessMousePressed C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3054  

#9 0x7ffb447a7c36 in views::View::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:1440  

#10 0x7ffb4a6da926 in ui::ScopedTargetHandler::OnEvent C:\b\s\w\ir\cache\builder\src\ui\events\scoped\_target\_handler.cc:28  

#11 0x7ffb45792ae9 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:190  

#12 0x7ffb45791f3b in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:139  

#13 0x7ffb45791825 in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:83  

#14 0x7ffb4579148f in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:55  

#15 0x7ffb475618c5 in views::internal::RootView::OnMousePressed C:\b\s\w\ir\cache\builder\src\ui\views\widget\root\_view.cc:418  

#16 0x7ffb447d1c77 in views::Widget::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1543  

#17 0x7ffb45792ae9 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:190  

#18 0x7ffb45791f3b in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:139  

#19 0x7ffb45791825 in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:83  

#20 0x7ffb4579148f in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:55  

#21 0x7ffb4a6d7ca6 in ui::EventProcessor::OnEventFromSource C:\b\s\w\ir\cache\builder\src\ui\events\event\_processor.cc:49  

#22 0x7ffb47597bef in ui::EventSource::DeliverEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:118  

#23 0x7ffb47597849 in ui::EventSource::SendEventToSinkFromRewriter C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:143  

#24 0x7ffb4759734b in ui::EventSource::SendEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:112  

#25 0x7ffb4a71901d in views::DesktopWindowTreeHostWin::HandleMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_window\_tree\_host\_win.cc:1004  

#26 0x7ffb4e84d9b0 in views::HWNDMessageHandler::HandleMouseEventInternal C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:3239  

#27 0x7ffb4e846a3b in views::HWNDMessageHandler::\_ProcessWindowMessage C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.h:360

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\bubble\webui\_bubble\_dialog\_view.cc:79 in WebUIBubbleDialogView::ClearContentsWrapper  

Shadow bytes around the buggy address:  

0x04653f869920: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04653f869930: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa  

0x04653f869940: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04653f869950: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04653f869960: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

=>0x04653f869970: fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04653f869980: fd fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa  

0x04653f869990: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04653f8699a0: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa  

0x04653f8699b0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x04653f8699c0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==6740==ABORTING

**CREDIT INFORMATION**  

Reporter credit: YoungJoo Lee(@ashuu\_lee) of CompSec Lab at Seoul National University

## Attachments

- [poc.mp4](attachments/poc.mp4) (video/mp4, 3.7 MB)

## Timeline

### [Deleted User] (2022-07-19)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-07-19)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-07-19)

I'm not able to repro—probably it depends on a race somewhere. But based on what I've learned about views, this seems like a plausible use-after-free: closing a view has a sync and an async portion (when the view is *really* destroyed), and if the BubbleContentsWrapper is destroyed in the meantime by something else, then this is a use-after-free.

While the repro is on Windows, I'm guessing this is used on Mac+Linux+CrOS as well. tluk@, please feel free to clear those flags if this analysis is wrong.

[Monorail components: UI>Browser>Bubbles]

### [Deleted User] (2022-07-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-20)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-02)

tluk: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### tl...@chromium.org (2022-08-04)

[Empty comment from Monorail migration]

### tl...@chromium.org (2022-08-04)

Fix in flight https://crrev.com/c/3809511

### gi...@appspot.gserviceaccount.com (2022-08-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8608c31f253cbbf56988afa78d3b530106146f3e

commit 8608c31f253cbbf56988afa78d3b530106146f3e
Author: Tom Lukaszewicz <tluk@chromium.org>
Date: Fri Aug 05 23:04:37 2022

[webui bubble] Fix UAF during manager teardown

The WebUIBubbleManager manages and provides resources to a WebUI
bubble. There are destruction orders that may cause the bubble
manager to be destroyed before its bubble, which can potentially
result in UAFs.

This CL ensures that the managed bubble is synchronously closed
during destruction of the manager if it has not already been
destroyed.

This CL also fixes a broken browsertest that was written with the
persistent renderer flag enabled - but was intending to test the
default functionality. This incorrect configuration was causing the
miss-configured test to fail as the content wrapper service would
persist the web contents' native window beyond the lifetime of the
AuraTestHelper's context.

Bug: 1345546
Change-Id: I547c0df01cdd7fb83cad63f77686f44d32043d66
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3809511
Commit-Queue: Thomas Lukaszewicz <tluk@chromium.org>
Reviewed-by: Elly Fong-Jones <ellyjones@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1032157}

[modify] https://crrev.com/8608c31f253cbbf56988afa78d3b530106146f3e/chrome/browser/ui/views/bubble/webui_bubble_manager_unittest.cc
[modify] https://crrev.com/8608c31f253cbbf56988afa78d3b530106146f3e/chrome/browser/ui/views/bubble/webui_bubble_manager.cc
[modify] https://crrev.com/8608c31f253cbbf56988afa78d3b530106146f3e/chrome/browser/ui/views/bubble/webui_bubble_manager_browsertest.cc


### tl...@chromium.org (2022-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-06)

Merge review required: M105 is already shipping to beta.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tl...@chromium.org (2022-08-08)

1. Why does your merge fit within the merge criteria for these milestones?
Low risk crashfix

2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/3809511

3. Have the changes been released and tested on canary?
Yes

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
This feature is behind a feature flag

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
No manual verification required

### am...@chromium.org (2022-08-09)

this issue is behind a feature flag and not enabled by default, talking to tluk@ off-bug, they would like to begin experiments in 105/beta so merging this fix is appropriate for that. 
M105 merge approved, please merge this fix to branch 5195 ASAP, as M105 beta update is being released tomorrow -- thank you 

### am...@google.com (2022-08-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-11)

Congratulations, YoungJoo! The VRP Panel has decided to award you $3,000 for this report. The reward amount was decided upon based on this issue being moderately significantly by not being remote exploitable, user interaction required, and browser shutdown. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-15)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2022-08-16)

[Bulk Edit] Your change as been approved for M105 Branch:Refer to go/chrome-branches for branch info, Please goahead and get the changes cherrypick asap, Plan is to cut M105 Beta RC build later this afternoon around 2Pm PST and would request to get all approved changes merged to M105 Branch asap so that it would be part of tomorrow's beta release.

### gi...@appspot.gserviceaccount.com (2022-08-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/616ca44cb8e7f7c70d53adb443b18fa77bd06030

commit 616ca44cb8e7f7c70d53adb443b18fa77bd06030
Author: Tom Lukaszewicz <tluk@chromium.org>
Date: Tue Aug 16 18:34:07 2022

[M105 Merge][webui bubble] Fix UAF during manager teardown

The WebUIBubbleManager manages and provides resources to a WebUI
bubble. There are destruction orders that may cause the bubble
manager to be destroyed before its bubble, which can potentially
result in UAFs.

This CL ensures that the managed bubble is synchronously closed
during destruction of the manager if it has not already been
destroyed.

This CL also fixes a broken browsertest that was written with the
persistent renderer flag enabled - but was intending to test the
default functionality. This incorrect configuration was causing the
miss-configured test to fail as the content wrapper service would
persist the web contents' native window beyond the lifetime of the
AuraTestHelper's context.

(cherry picked from commit 8608c31f253cbbf56988afa78d3b530106146f3e)

Bug: 1345546
Change-Id: I547c0df01cdd7fb83cad63f77686f44d32043d66
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3809511
Commit-Queue: Thomas Lukaszewicz <tluk@chromium.org>
Reviewed-by: Elly Fong-Jones <ellyjones@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1032157}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3832070
Commit-Queue: Prudhvikumar Bommana <pbommana@google.com>
Cr-Commit-Position: refs/branch-heads/5195@{#610}
Cr-Branched-From: 7aa3f074a7907975b001346cc0288d0214af8451-refs/heads/main@{#1027018}

[modify] https://crrev.com/616ca44cb8e7f7c70d53adb443b18fa77bd06030/chrome/browser/ui/views/bubble/webui_bubble_manager_unittest.cc
[modify] https://crrev.com/616ca44cb8e7f7c70d53adb443b18fa77bd06030/chrome/browser/ui/views/bubble/webui_bubble_manager.cc
[modify] https://crrev.com/616ca44cb8e7f7c70d53adb443b18fa77bd06030/chrome/browser/ui/views/bubble/webui_bubble_manager_browsertest.cc


### [Deleted User] (2022-08-16)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-08-18)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-18)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-18)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-08-18)

1. Just https://crrev.com/c/3836443
2. Low, no conflicts
3. 105
4. Yes

### rz...@google.com (2022-08-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-18)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-08-18)

1. Just https://crrev.com/c/3835694
2. Low, no conflicts
3. 105
4. Yes

### gm...@google.com (2022-08-18)

[Empty comment from Monorail migration]

### gm...@google.com (2022-09-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-09-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f41f21970277ff01c4286c8884b585a0cfbde578

commit f41f21970277ff01c4286c8884b585a0cfbde578
Author: Tom Lukaszewicz <tluk@chromium.org>
Date: Tue Sep 13 13:33:28 2022

[M96-LTS][webui bubble] Fix UAF during manager teardown

The WebUIBubbleManager manages and provides resources to a WebUI
bubble. There are destruction orders that may cause the bubble
manager to be destroyed before its bubble, which can potentially
result in UAFs.

This CL ensures that the managed bubble is synchronously closed
during destruction of the manager if it has not already been
destroyed.

This CL also fixes a broken browsertest that was written with the
persistent renderer flag enabled - but was intending to test the
default functionality. This incorrect configuration was causing the
miss-configured test to fail as the content wrapper service would
persist the web contents' native window beyond the lifetime of the
AuraTestHelper's context.

(cherry picked from commit 8608c31f253cbbf56988afa78d3b530106146f3e)

Bug: 1345546
Change-Id: I547c0df01cdd7fb83cad63f77686f44d32043d66
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3809511
Commit-Queue: Thomas Lukaszewicz <tluk@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1032157}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3835694
Owners-Override: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1696}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/f41f21970277ff01c4286c8884b585a0cfbde578/chrome/browser/ui/views/bubble/webui_bubble_manager_unittest.cc
[modify] https://crrev.com/f41f21970277ff01c4286c8884b585a0cfbde578/chrome/browser/ui/views/bubble/webui_bubble_manager.cc
[modify] https://crrev.com/f41f21970277ff01c4286c8884b585a0cfbde578/chrome/browser/ui/views/bubble/webui_bubble_manager_browsertest.cc


### gi...@appspot.gserviceaccount.com (2022-09-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bb3c97484f453d253765d6f6eb189d7415779279

commit bb3c97484f453d253765d6f6eb189d7415779279
Author: Tom Lukaszewicz <tluk@chromium.org>
Date: Wed Sep 14 13:21:59 2022

[M102-LTS][webui bubble] Fix UAF during manager teardown

The WebUIBubbleManager manages and provides resources to a WebUI
bubble. There are destruction orders that may cause the bubble
manager to be destroyed before its bubble, which can potentially
result in UAFs.

This CL ensures that the managed bubble is synchronously closed
during destruction of the manager if it has not already been
destroyed.

This CL also fixes a broken browsertest that was written with the
persistent renderer flag enabled - but was intending to test the
default functionality. This incorrect configuration was causing the
miss-configured test to fail as the content wrapper service would
persist the web contents' native window beyond the lifetime of the
AuraTestHelper's context.

(cherry picked from commit 8608c31f253cbbf56988afa78d3b530106146f3e)

Bug: 1345546
Change-Id: I547c0df01cdd7fb83cad63f77686f44d32043d66
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3809511
Commit-Queue: Thomas Lukaszewicz <tluk@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1032157}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3836443
Owners-Override: Oleh Lamzin <lamzin@google.com>
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1350}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/bb3c97484f453d253765d6f6eb189d7415779279/chrome/browser/ui/views/bubble/webui_bubble_manager_unittest.cc
[modify] https://crrev.com/bb3c97484f453d253765d6f6eb189d7415779279/chrome/browser/ui/views/bubble/webui_bubble_manager.cc
[modify] https://crrev.com/bb3c97484f453d253765d6f6eb189d7415779279/chrome/browser/ui/views/bubble/webui_bubble_manager_browsertest.cc


### rz...@google.com (2022-09-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1345546?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1343686]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060325)*
