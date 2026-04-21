# Security: heap-use-after-free in views::View::GetEffectiveViewTargeter

| Field | Value |
|-------|-------|
| **Issue ID** | [40059390](https://issues.chromium.org/issues/40059390) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Views |
| **Platforms** | Windows |
| **Reporter** | st...@gmail.com |
| **Assignee** | bh...@google.com |
| **Created** | 2022-04-15 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

Right-clicking a blocked item in the download bubble causes a UAF.

**VERSION**  

Chrome Version: 103.0.5006.0  

Operating System: Windows 10

**REPRODUCTION CASE**  

Uses the new download bubble UI which can be enabled via #download-bubble

1. Open poc.html
2. Right-click the download item

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: browser Crash State:

==17700==ERROR: AddressSanitizer: heap-use-after-free on address 0x117c69c1bad0 at pc 0x7ffc5067b5f2 bp 0x00136a3fdae0 sp 0x00136a3fdb28  

READ of size 8 at 0x117c69c1bad0 thread T0  

==17700==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ffc5067b5f1 in views::View::GetEffectiveViewTargeter C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:1511  

#1 0x7ffc5067bc83 in views::View::HitTestPoint C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:1362  

#2 0x7ffc5067cfad in views::View::ProcessMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3109  

#3 0x7ffc5a51e416 in ui::ScopedTargetHandler::OnEvent C:\b\s\w\ir\cache\builder\src\ui\events\scoped\_target\_handler.cc:28  

#4 0x7ffc516701e9 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:190  

#5 0x7ffc5166f709 in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:139  

#6 0x7ffc5166eff3 in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:83  

#7 0x7ffc5166ec34 in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:55  

#8 0x7ffc5344a841 in views::internal::RootView::OnMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\widget\root\_view.cc:485  

#9 0x7ffc506a681e in views::Widget::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1567  

#10 0x7ffc516701e9 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:190  

#11 0x7ffc5166f709 in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:139  

#12 0x7ffc5166eff3 in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:83  

#13 0x7ffc5166ec34 in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:55  

#14 0x7ffc56547736 in ui::EventProcessor::OnEventFromSource C:\b\s\w\ir\cache\builder\src\ui\events\event\_processor.cc:49  

#15 0x7ffc5343cdff in ui::EventSource::DeliverEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:118  

#16 0x7ffc5343ca59 in ui::EventSource::SendEventToSinkFromRewriter C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:143  

#17 0x7ffc5343c55b in ui::EventSource::SendEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:112  

#18 0x7ffc56545243 in views::DesktopWindowTreeHostWin::HandleMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_window\_tree\_host\_win.cc:1004  

#19 0x7ffc5a58d3bc in views::HWNDMessageHandler::HandleMouseEventInternal C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:3174  

#20 0x7ffc5a5864a3 in views::HWNDMessageHandler::\_ProcessWindowMessage C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.h:358  

#21 0x7ffc5a585b33 in views::HWNDMessageHandler::OnWndProc C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:1027  

#22 0x7ffc53b68412 in gfx::WindowImpl::WndProc C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window\_impl.cc:306  

#23 0x7ffc53b66d2d in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> C:\b\s\w\ir\cache\builder\src\base\win\wrapped\_window\_proc.h:74  

#24 0x7ffd0759e857 in CallWindowProcW+0x3f7 (C:\WINDOWS\System32\user32.dll+0x18000e857)  

#25 0x7ffd0759e298 in DispatchMessageW+0x258 (C:\WINDOWS\System32\user32.dll+0x18000e298)  

#26 0x7ffc50a179fd in base::MessagePumpForUI::ProcessMessageHelper C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:531  

#27 0x7ffc50a15a05 in base::MessagePumpForUI::ProcessNextWindowsMessage C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:498  

#28 0x7ffc50a152f3 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:209  

#29 0x7ffc50a136d8 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#30 0x7ffc53826190 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:498  

#31 0x7ffc508dd587 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#32 0x7ffc491eb08b in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1067  

#33 0x7ffc491f0513 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:155  

#34 0x7ffc491e44e9 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#35 0x7ffc50509bf3 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:640  

#36 0x7ffc5050cd6c in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1147  

#37 0x7ffc5050be9e in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1019  

#38 0x7ffc5050886b in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:407  

#39 0x7ffc50508ff4 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:435  

#40 0x7ffc452614ca in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:176  

#41 0x7ff7d7b65b16 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:167  

#42 0x7ff7d7b62b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#43 0x7ff7d7f5fafb in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#44 0x7ffd06b77033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#45 0x7ffd077c2650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

0x117c69c1bad0 is located 592 bytes inside of 1872-byte region [0x117c69c1b880,0x117c69c1bfd0)  

freed by thread T0 here:  

#0 0x7ff7d7c0e82b in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ffc6006f1d7 in DownloadBubbleRowView::~DownloadBubbleRowView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\download\bubble\download\_bubble\_row\_view.cc:182  

#2 0x7ffc50667777 in views::View::~View C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:254  

#3 0x7ffc5069097b in views::View::~View C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:227  

#4 0x7ffc50667777 in views::View::~View C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:254  

#5 0x7ffc5069097b in views::View::~View C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:227  

#6 0x7ffc50667777 in views::View::~View C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:254  

#7 0x7ffc5342601b in views::ScrollView::~ScrollView C:\b\s\w\ir\cache\builder\src\ui\views\controls\scroll\_view.cc:244  

#8 0x7ffc50669831 in views::View::DoRemoveChildView C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:2678  

#9 0x7ffc50669bba in views::View::RemoveAllChildViews C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:329  

#10 0x7ffc5e102a9a in DownloadToolbarButtonView::OpenSecurityDialog C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\download\bubble\download\_toolbar\_button\_view.cc:200  

#11 0x7ffc6006cdeb in DownloadBubbleRowView::OnMainButtonPressed C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\download\bubble\download\_bubble\_row\_view.cc:320  

#12 0x7ffc5063e03b in base::internal::Invoker<base::internal::BindState<`lambda at ../../ui/views/controls/button/button.cc:111:31',base::RepeatingCallback<void ()> >,void (const ui::Event &)>::Run C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:761  

#13 0x7ffc600bc2cf in HoverButtonController::OnMouseReleased C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\hover\_button\_controller.cc:55  

#14 0x7ffc5067cfa1 in views::View::ProcessMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3108  

#15 0x7ffc5a51e416 in ui::ScopedTargetHandler::OnEvent C:\b\s\w\ir\cache\builder\src\ui\events\scoped\_target\_handler.cc:28  

#16 0x7ffc516701e9 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:190  

#17 0x7ffc5166f709 in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:139  

#18 0x7ffc5166eff3 in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:83  

#19 0x7ffc5166ec34 in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:55  

#20 0x7ffc5344a841 in views::internal::RootView::OnMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\widget\root\_view.cc:485  

#21 0x7ffc506a681e in views::Widget::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1567  

#22 0x7ffc516701e9 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:190  

#23 0x7ffc5166f709 in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:139  

#24 0x7ffc5166eff3 in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:83  

#25 0x7ffc5166ec34 in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:55  

#26 0x7ffc56547736 in ui::EventProcessor::OnEventFromSource C:\b\s\w\ir\cache\builder\src\ui\events\event\_processor.cc:49  

#27 0x7ffc5343cdff in ui::EventSource::DeliverEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:118

previously allocated by thread T0 here:  

#0 0x7ff7d7c0e92b in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffc635e615e in operator new d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ffc5e1023f4 in DownloadToolbarButtonView::CreateRowListView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\download\bubble\download\_toolbar\_button\_view.cc:271  

#3 0x7ffc5e101cb5 in DownloadToolbarButtonView::GetPrimaryView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\download\bubble\download\_toolbar\_button\_view.cc:178  

#4 0x7ffc5e1012e7 in DownloadToolbarButtonView::ShowDetails C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\download\bubble\download\_toolbar\_button\_view.cc:144  

#5 0x7ffc5e6aefc1 in DownloadBubbleUIController::OnNewItem C:\b\s\w\ir\cache\builder\src\chrome\browser\download\bubble\download\_bubble\_controller.cc:172  

#6 0x7ffc5b5b8c28 in `anonymous namespace'::DownloadBubbleUIControllerDelegate::OnNewDownloadReady C:\b\s\w\ir\cache\builder\src\chrome\browser\download\download\_ui\_controller.cc:163  

#7 0x7ffc5b5b8719 in DownloadUIController::OnDownloadUpdated C:\b\s\w\ir\cache\builder\src\chrome\browser\download\download\_ui\_controller.cc:290  

#8 0x7ffc48e0d3ad in download::DownloadItemImpl::UpdateObservers C:\b\s\w\ir\cache\builder\src\components\download\internal\common\download\_item\_impl.cc:511  

#9 0x7ffc48e1eca3 in download::DownloadItemImpl::OnTargetResolved C:\b\s\w\ir\cache\builder\src\components\download\internal\common\download\_item\_impl.cc:1916  

#10 0x7ffc48e060f6 in base::internal::Invoker<base::internal::BindState<base::OnceCallback<void (download::DownloadInterruptReason, const base::FilePath &)>,download::DownloadInterruptReason,base::FilePath>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:748  

#11 0x7ffc50961314 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#12 0x7ffc538249d5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:386  

#13 0x7ffc53823fa9 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:291  

#14 0x7ffc50a15396 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:214  

#15 0x7ffc50a136d8 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#16 0x7ffc53826190 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:498  

#17 0x7ffc508dd587 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#18 0x7ffc491eb08b in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1067  

#19 0x7ffc491f0513 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:155  

#20 0x7ffc491e44e9 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#21 0x7ffc50509bf3 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:640  

#22 0x7ffc5050cd6c in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1147  

#23 0x7ffc5050be9e in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1019  

#24 0x7ffc5050886b in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:407  

#25 0x7ffc50508ff4 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:435  

#26 0x7ffc452614ca in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:176  

#27 0x7ff7d7b65b16 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:167

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:1511 in views::View::GetEffectiveViewTargeter  

Shadow bytes around the buggy address:  

0x0373f6c83700: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0373f6c83710: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0373f6c83720: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0373f6c83730: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0373f6c83740: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x0373f6c83750: fd fd fd fd fd fd fd fd fd fd[fd]fd fd fd fd fd  

0x0373f6c83760: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0373f6c83770: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0373f6c83780: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0373f6c83790: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0373f6c837a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==17700==ABORTING

**CREDIT INFORMATION**  

Reporter credit: Thomas Orlita

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 91 B)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 489.4 KB)

## Timeline

### [Deleted User] (2022-04-15)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-04-19)

probably same crash as 1315395, but with repo steps here.

[Monorail components: Internals>Views]

### ad...@google.com (2022-04-19)

(auto-cc on security bug)

### [Deleted User] (2022-04-20)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ts...@chromium.org (2022-04-22)

DNR on linux so unsure of how far back this goes.

### bh...@google.com (2022-04-22)

This should be fixed with https://crrev.com/c/3597896. It is restricted to DownloadBubble, which is going for a 1% experiment in M102

### gi...@appspot.gserviceaccount.com (2022-04-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9f58d3a3f748dee62757252f80f7a15b807bf9c2

commit 9f58d3a3f748dee62757252f80f7a15b807bf9c2
Author: Rohit Bhatia <bhatiarohit@google.com>
Date: Sat Apr 23 00:02:21 2022

[DownloadBubble] Use visibility instead of construction/destruction

When showing the main or the security subpage, use visibility instead
of construction/destruction. Added methods to update subpage.

Bug: 1316740
Bug: 1315395
Change-Id: I970016445e169b472ed02e7cd294099bc4a3e64e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3597896
Reviewed-by: Xinghui Lu <xinghuilu@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Rohit Bhatia <bhatiarohit@google.com>
Cr-Commit-Position: refs/heads/main@{#995434}

[modify] https://crrev.com/9f58d3a3f748dee62757252f80f7a15b807bf9c2/chrome/browser/ui/views/download/bubble/download_bubble_row_view.cc
[modify] https://crrev.com/9f58d3a3f748dee62757252f80f7a15b807bf9c2/chrome/browser/ui/views/download/bubble/download_bubble_row_view.h
[modify] https://crrev.com/9f58d3a3f748dee62757252f80f7a15b807bf9c2/chrome/browser/ui/views/download/bubble/download_toolbar_button_view.cc
[modify] https://crrev.com/9f58d3a3f748dee62757252f80f7a15b807bf9c2/chrome/browser/ui/views/download/bubble/download_bubble_security_view.cc
[modify] https://crrev.com/9f58d3a3f748dee62757252f80f7a15b807bf9c2/chrome/browser/ui/views/download/bubble/download_toolbar_button_view.h
[modify] https://crrev.com/9f58d3a3f748dee62757252f80f7a15b807bf9c2/chrome/browser/ui/views/download/bubble/download_bubble_security_view.h


### bh...@google.com (2022-04-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-25)

Merge approved: your change passed merge requirements and is auto-approved for M102. Please go ahead and merge the CL to branch 5005 (refs/branch-heads/5005) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2022-04-26)

Setting Impact=None as this is in a feature disabled by default.

### gi...@appspot.gserviceaccount.com (2022-04-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ede52e5a39ba9c732b8bc509a0993ac94f7f9a05

commit ede52e5a39ba9c732b8bc509a0993ac94f7f9a05
Author: Rohit Bhatia <bhatiarohit@google.com>
Date: Tue Apr 26 18:40:17 2022

[M102][DownloadBubble] Use visibility instead of construction/destruction

When showing the main or the security subpage, use visibility instead
of construction/destruction. Added methods to update subpage.

(cherry picked from commit 9f58d3a3f748dee62757252f80f7a15b807bf9c2)

Bug: 1316740
Bug: 1315395
Change-Id: I970016445e169b472ed02e7cd294099bc4a3e64e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3597896
Reviewed-by: Xinghui Lu <xinghuilu@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Rohit Bhatia <bhatiarohit@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#995434}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3605901
Auto-Submit: Rohit Bhatia <bhatiarohit@google.com>
Commit-Queue: Peter Kasting <pkasting@chromium.org>
Cr-Commit-Position: refs/branch-heads/5005@{#177}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/ede52e5a39ba9c732b8bc509a0993ac94f7f9a05/chrome/browser/ui/views/download/bubble/download_bubble_row_view.cc
[modify] https://crrev.com/ede52e5a39ba9c732b8bc509a0993ac94f7f9a05/chrome/browser/ui/views/download/bubble/download_bubble_row_view.h
[modify] https://crrev.com/ede52e5a39ba9c732b8bc509a0993ac94f7f9a05/chrome/browser/ui/views/download/bubble/download_toolbar_button_view.cc
[modify] https://crrev.com/ede52e5a39ba9c732b8bc509a0993ac94f7f9a05/chrome/browser/ui/views/download/bubble/download_bubble_security_view.cc
[modify] https://crrev.com/ede52e5a39ba9c732b8bc509a0993ac94f7f9a05/chrome/browser/ui/views/download/bubble/download_toolbar_button_view.h
[modify] https://crrev.com/ede52e5a39ba9c732b8bc509a0993ac94f7f9a05/chrome/browser/ui/views/download/bubble/download_bubble_security_view.h


### bh...@google.com (2022-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-27)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-06)

Thank you for this report, Thomas. The VRP Panel has decided to award you $5,000 for this report. While the user gesture is required, it is minimal and is standard for this workflow; however, there is an existing crash report which precedes your report (https://crbug.com/chromium/1315395). Given the steps to reproduce and the stack trace to provide additional amplification of this security bug, we have decided in making this eligible for a reward and the specified reward amount of $5,000. Thank you for your efforts and taking the time to discover and report this issue to us!

### st...@gmail.com (2022-05-06)

Thank you, I appreciate it!

### am...@google.com (2022-05-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-08-03)

This issue was migrated from crbug.com/chromium/1316740?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059390)*
