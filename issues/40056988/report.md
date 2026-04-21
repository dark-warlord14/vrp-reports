# Security: heap-buffer-overflow in TabStripModel::MoveWebContentsAtImpl

| Field | Value |
|-------|-------|
| **Issue ID** | [40056988](https://issues.chromium.org/issues/40056988) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>TopChrome>TabStrip>ThumbnailTabStrip |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | tl...@chromium.org |
| **Created** | 2021-08-23 |
| **Bounty** | $10,000.00 |

## Description

**VERSION**  

Chrome Version: 95.0.4619.2 (Official Build) canary (64-bit) (cohort: Clang-64)  

Operating System: Windows and Linux

**REPRODUCTION CASE**

1. Open two tabs
2. Open an incognito window and add it to a new group
3. Drag a tab to the incognito window
4. Drag the group to the right

==3228==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x122861a2f8a8 at pc 0x7ffe4804383b bp 0x00d60f9fe100 sp 0x00d60f9fe148  

READ of size 8 at 0x122861a2f8a8 thread T0  

==3228==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ffe4804383a in std::\_\_1::vector<std::\_\_1::unique\_ptr<web\_app::WebAppInstallTask,std::\_\_1::default\_delete<web\_app::WebAppInstallTask> >,std::\_\_1::allocator<std::\_\_1::unique\_ptr<web\_app::WebAppInstallTask,std::\_\_1::default\_delete<web\_app::WebAppInstallTask> > > >::\_\_move\_range C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\vector:1758  

#1 0x7ffe4eac4789 in std::\_\_1::vector<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData,std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) >,std::\_\_1::allocator<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData,std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) > > >::insert C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\vector:1821  

#2 0x7ffe4eaafe02 in TabStripModel::MoveWebContentsAtImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:2034  

#3 0x7ffe4eab1379 in TabStripModel::MoveGroupTo C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:696  

#4 0x7ffe563196a9 in TabStripPageHandler::MoveGroup C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\webui\tab\_strip\tab\_strip\_page\_handler.cc:642  

#5 0x7ffe4847cb57 in tab\_strip::mojom::PageHandlerStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\chrome\browser\ui\webui\tab\_strip\tab\_strip.mojom.cc:1890  

#6 0x7ffe4cc50d1d in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:898  

#7 0x7ffe4f3e2e7e in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#8 0x7ffe4cc545a8 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:655  

#9 0x7ffe4cc68a1d in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:1099  

#10 0x7ffe4cc677af in mojo::internal::MultiplexRouter::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:719  

#11 0x7ffe4f3e2e7e in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#12 0x7ffe4cc4bade in mojo::Connector::DispatchMessageW C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:546  

#13 0x7ffe4cc4d32b in mojo::Connector::ReadAllAvailableMessages C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:604  

#14 0x7ffe4cc9d446 in mojo::SimpleWatcher::OnHandleReady C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple\_watcher.cc:278  

#15 0x7ffe4c90685a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:178  

#16 0x7ffe4f29ed32 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:360  

#17 0x7ffe4f29e392 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:260  

#18 0x7ffe4c9ad136 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#19 0x7ffe4c9ab378 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#20 0x7ffe4f2a022e in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:467  

#21 0x7ffe4c889153 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:134  

#22 0x7ffe45dc0589 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:988  

#23 0x7ffe45dc5905 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:152  

#24 0x7ffe45db9bee in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:49  

#25 0x7ffe486efab4 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:608  

#26 0x7ffe486f2350 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1104  

#27 0x7ffe486f1537 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:971  

#28 0x7ffe486edfba in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:390  

#29 0x7ffe486eeffc in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:418  

#30 0x7ffe422a148c in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:172  

#31 0x7ff7f6a95b74 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:169  

#32 0x7ff7f6a92be8 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#33 0x7ff7f6e86e8f in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#34 0x7ffee5df7033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#35 0x7ffee73e2650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

0x122861a2f8a8 is located 8 bytes to the left of 8-byte region [0x122861a2f8b0,0x122861a2f8b8)  

allocated by thread T0 here:  

#0 0x7ff7f6b36edb in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffe5ee31a2a in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ffe4eac48c7 in std::\_\_1::vector<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData,std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) >,std::\_\_1::allocator<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData,std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) > > >::insert C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\vector:1828  

#3 0x7ffe4eaa8e0d in TabStripModel::InsertWebContentsAtImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:1752  

#4 0x7ffe4eab7c4d in TabStripModel::AddWebContents C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:1030  

#5 0x7ffe4ea9d73b in Navigate C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser\_navigator.cc:698  

#6 0x7ffe50e6847c in chrome::AddTabAt C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser\_tabstrip.cc:40  

#7 0x7ffe50e33391 in chrome::OpenEmptyWindow C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser\_commands.cc:492  

#8 0x7ffe50e33051 in chrome::NewEmptyWindow C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser\_commands.cc:467  

#9 0x7ffe50e176d0 in chrome::BrowserCommandController::ExecuteCommandWithDisposition C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser\_command\_controller.cc:410  

#10 0x7ffe5962d8c6 in AppMenuModel::ExecuteCommand C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\toolbar\app\_menu\_model.cc:383  

#11 0x7ffe5962345f in AppMenu::ExecuteCommand C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\toolbar\app\_menu.cc:1028  

#12 0x7ffe51c78f4f in views::internal::MenuRunnerImpl::OnMenuClosed C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_runner\_impl.cc:245  

#13 0x7ffe55b1dd32 in views::MenuController::ExitMenu C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_controller.cc:3154  

#14 0x7ffe55b23153 in views::MenuController::Accept C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_controller.cc:1780  

#15 0x7ffe55b226e7 in views::MenuController::OnMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_controller.cc:827  

#16 0x7ffe4c67c8b1 in views::Widget::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1548  

#17 0x7ffe4d54d3ef in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:191  

#18 0x7ffe4d54c90f in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:140  

#19 0x7ffe4d54c2f8 in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:84  

#20 0x7ffe4d54bf3c in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:56  

#21 0x7ffe51cb4d4c in ui::EventProcessor::OnEventFromSource C:\b\s\w\ir\cache\builder\src\ui\events\event\_processor.cc:49  

#22 0x7ffe4eeb4b6f in ui::EventSource::DeliverEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:113  

#23 0x7ffe4eeb47c9 in ui::EventSource::SendEventToSinkFromRewriter C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:138  

#24 0x7ffe4eeb42cb in ui::EventSource::SendEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:107  

#25 0x7ffe51cb2729 in views::DesktopWindowTreeHostWin::HandleMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_window\_tree\_host\_win.cc:1006  

#26 0x7ffe55b84021 in views::HWNDMessageHandler::HandleMouseEventInternal C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:3143  

#27 0x7ffe55b7d473 in views::HWNDMessageHandler::\_ProcessWindowMessage C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.h:356

SUMMARY: AddressSanitizer: heap-buffer-overflow C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\vector:1758 in std::\_\_1::vector<std::\_\_1::unique\_ptr<web\_app::WebAppInstallTask,std::\_\_1::default\_delete<web\_app::WebAppInstallTask> >,std::\_\_1::allocator<std::\_\_1::unique\_ptr<web\_app::WebAppInstallTask,std::\_\_1::default\_delete<web\_app::WebAppInstallTask> > > >::\_\_move\_range  

Shadow bytes around the buggy address:  

0x04696d745ec0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fd  

0x04696d745ed0: fa fa fd fd fa fa fd fa fa fa fd fa fa fa fd fa  

0x04696d745ee0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa  

0x04696d745ef0: fa fa fd fa fa fa fd fd fa fa fd fd fa fa fd fd  

0x04696d745f00: fa fa fd fa fa fa fd fa fa fa fd fd fa fa fd fd  

=>0x04696d745f10: fa fa fd fa fa[fa]00 fa fa fa fd fa fa fa fd fa  

0x04696d745f20: fa fa 04 fa fa fa fd fa fa fa fd fd fa fa 00 fa  

0x04696d745f30: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa  

0x04696d745f40: fa fa 00 fa fa fa 00 fa fa fa 00 fa fa fa 00 00  

0x04696d745f50: fa fa 00 00 fa fa 00 00 fa fa 00 00 fa fa 00 00  

0x04696d745f60: fa fa 00 00 fa fa 00 00 fa fa 00 00 fa fa fd fd  

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

==3228==ABORTING

## Attachments

- [screen.mp4](attachments/screen.mp4) (video/mp4, 1.7 MB)

## Timeline

### [Deleted User] (2021-08-23)

[Empty comment from Monorail migration]

### ch...@gmail.com (2021-08-24)

Enable #top-chrome-touch-ui


### dr...@chromium.org (2021-08-24)

This does crash as described. Due to the user gesture requirement, marking Medium Severity. cyan@, dfried@ - as a chrome/browser/ui/tabs/ OWNER, can you take a look?

[Monorail components: UI>Browser>TopChrome>TabStrip>ThumbnailTabStrip]

### [Deleted User] (2021-08-24)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-25)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-25)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cy...@chromium.org (2021-08-25)

[Empty comment from Monorail migration]

### em...@chromium.org (2021-08-30)

[Empty comment from Monorail migration]

### dp...@chromium.org (2021-08-31)

Looks like this is another issue with the thumbnailtabstrip assigning tluk@

### tl...@chromium.org (2021-09-01)

Fix ready

https://crrev.com/c/3138877

### gi...@appspot.gserviceaccount.com (2021-09-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4d9faf797b93cf6d5dc363de75a7dc444b80193b

commit 4d9faf797b93cf6d5dc363de75a7dc444b80193b
Author: Tom <tluk@chromium.org>
Date: Wed Sep 01 23:56:51 2021

[tab strip] Move WebContentsDelegate logic to the TabStripPageHandler

This CL moves the WebContentsDelegate::CanDragEnter logic out of the
WebUITabStripWebView and into the TabStripPageHandler.

Currently the delegate is being set twice (once in Views code and
again in the WebUI code). This resulted in the CanDragEnter logic
not firing as intended causing issues when dragging between
windows with unrelated profiles.

Bug: 1242742
Change-Id: I64db3bc32e826a698dd4d259630052b2fc2ac8fe
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3138877
Reviewed-by: Collin Baker <collinbaker@chromium.org>
Commit-Queue: Thomas Lukaszewicz <tluk@chromium.org>
Cr-Commit-Position: refs/heads/main@{#917464}

[modify] https://crrev.com/4d9faf797b93cf6d5dc363de75a7dc444b80193b/chrome/browser/ui/views/frame/webui_tab_strip_container_view.cc
[modify] https://crrev.com/4d9faf797b93cf6d5dc363de75a7dc444b80193b/chrome/browser/ui/views/frame/webui_tab_strip_container_view_unittest.cc
[modify] https://crrev.com/4d9faf797b93cf6d5dc363de75a7dc444b80193b/chrome/browser/ui/webui/tab_strip/tab_strip_page_handler.cc
[modify] https://crrev.com/4d9faf797b93cf6d5dc363de75a7dc444b80193b/chrome/browser/ui/webui/tab_strip/tab_strip_page_handler.h
[modify] https://crrev.com/4d9faf797b93cf6d5dc363de75a7dc444b80193b/chrome/browser/ui/webui/tab_strip/tab_strip_page_handler_unittest.cc


### tl...@chromium.org (2021-09-02)

[Empty comment from Monorail migration]

### ch...@gmail.com (2021-09-02)

[Comment Deleted]

### tl...@chromium.org (2021-09-02)

Will do thanks!

### [Deleted User] (2021-09-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-03)

This bug requires manual review: M94's targeted beta branch promotion date has already passed, so this requires manual review
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

### tl...@google.com (2021-09-03)

1. Does your merge fit within the Merge Decision Guidelines?
Yes

2. Links to the CLs you are requesting to merge.
https://crrev.com/c/3138877

3. Has the change landed and been verified on ToT?
Yes

4. Does this change need to be merged into other active release branches (M-1, M+1)?
Yes, M93

5. Why are these changes required in this milestone after branch?
Security vulnerability

6. Is this a new feature?
Yes

7. If it is a new feature, is it behind a flag using finch?
Yes

### sr...@google.com (2021-09-03)

Merge approved for M94 branch:4606 please merege asap

### gi...@appspot.gserviceaccount.com (2021-09-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6a0dcdd58c494bb23ec663f57b8e7985eb1f4785

commit 6a0dcdd58c494bb23ec663f57b8e7985eb1f4785
Author: Tom <tluk@chromium.org>
Date: Fri Sep 03 18:54:27 2021

[M94 Merge][tab strip] Move WebContentsDelegate logic to the TabStripPageHandler

This CL moves the WebContentsDelegate::CanDragEnter logic out of the
WebUITabStripWebView and into the TabStripPageHandler.

Currently the delegate is being set twice (once in Views code and
again in the WebUI code). This resulted in the CanDragEnter logic
not firing as intended causing issues when dragging between
windows with unrelated profiles.

(cherry picked from commit 4d9faf797b93cf6d5dc363de75a7dc444b80193b)

Bug: 1242742
Change-Id: I64db3bc32e826a698dd4d259630052b2fc2ac8fe
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3138877
Reviewed-by: Collin Baker <collinbaker@chromium.org>
Commit-Queue: Thomas Lukaszewicz <tluk@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#917464}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3139501
Reviewed-by: Thomas Lukaszewicz <tluk@chromium.org>
Cr-Commit-Position: refs/branch-heads/4606@{#704}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/6a0dcdd58c494bb23ec663f57b8e7985eb1f4785/chrome/browser/ui/views/frame/webui_tab_strip_container_view.cc
[modify] https://crrev.com/6a0dcdd58c494bb23ec663f57b8e7985eb1f4785/chrome/browser/ui/views/frame/webui_tab_strip_container_view_unittest.cc
[modify] https://crrev.com/6a0dcdd58c494bb23ec663f57b8e7985eb1f4785/chrome/browser/ui/webui/tab_strip/tab_strip_page_handler.cc
[modify] https://crrev.com/6a0dcdd58c494bb23ec663f57b8e7985eb1f4785/chrome/browser/ui/webui/tab_strip/tab_strip_page_handler.h
[modify] https://crrev.com/6a0dcdd58c494bb23ec663f57b8e7985eb1f4785/chrome/browser/ui/webui/tab_strip/tab_strip_page_handler_unittest.cc


### tl...@chromium.org (2021-09-03)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-09-07)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-09-07)

Updated FoundIn and SI accordingly. For future reference, when these are accurately applied/updated, Sherrifbot will handle the merge review labeling accordingly once the issue is marked Fixed. :) 
Merge approved to M93, please merge to branch 4577 at your earliest convenience so this fix can be included in next week's M93 security refresh. Thank you.

### gi...@appspot.gserviceaccount.com (2021-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/eb0598ab1010f70d14ad3c7700ed687d22278ec2

commit eb0598ab1010f70d14ad3c7700ed687d22278ec2
Author: tom <tluk@chromium.org>
Date: Wed Sep 08 05:15:44 2021

[M93 Merge][tab strip] Move WebContentsDelegate logic to the TabStripPageHandler

This CL moves the WebContentsDelegate::CanDragEnter logic out of the
WebUITabStripWebView and into the TabStripPageHandler.

Currently the delegate is being set twice (once in Views code and
again in the WebUI code). This resulted in the CanDragEnter logic
not firing as intended causing issues when dragging between
windows with unrelated profiles.

(cherry picked from commit 4d9faf797b93cf6d5dc363de75a7dc444b80193b)

Bug: 1242742
Change-Id: I64db3bc32e826a698dd4d259630052b2fc2ac8fe
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3138877
Reviewed-by: Collin Baker <collinbaker@chromium.org>
Commit-Queue: Thomas Lukaszewicz <tluk@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#917464}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3142270
Cr-Commit-Position: refs/branch-heads/4577@{#1199}
Cr-Branched-From: 761ddde228655e313424edec06497d0c56b0f3c4-refs/heads/master@{#902210}

[modify] https://crrev.com/eb0598ab1010f70d14ad3c7700ed687d22278ec2/chrome/browser/ui/views/frame/webui_tab_strip_container_view.cc
[modify] https://crrev.com/eb0598ab1010f70d14ad3c7700ed687d22278ec2/chrome/browser/ui/views/frame/webui_tab_strip_container_view_unittest.cc
[modify] https://crrev.com/eb0598ab1010f70d14ad3c7700ed687d22278ec2/chrome/browser/ui/webui/tab_strip/tab_strip_ui_handler.cc
[modify] https://crrev.com/eb0598ab1010f70d14ad3c7700ed687d22278ec2/chrome/browser/ui/webui/tab_strip/tab_strip_ui_handler.h
[modify] https://crrev.com/eb0598ab1010f70d14ad3c7700ed687d22278ec2/chrome/browser/ui/webui/tab_strip/tab_strip_ui_handler_unittest.cc


### am...@google.com (2021-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-06)

Congratulations, Khalil! The VRP Panel has decided to award you $10,000 for this report. Nice work! 

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### vo...@google.com (2021-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1242742?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056988)*
