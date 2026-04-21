# Security: heap-buffer-overflow in TableView

| Field | Value |
|-------|-------|
| **Issue ID** | [40060426](https://issues.chromium.org/issues/40060426) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | UI>TaskManager |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | yo...@snu.ac.kr |
| **Assignee** | pk...@chromium.org |
| **Created** | 2022-07-28 |
| **Bounty** | $4,000.00 |

## Description

**VULNERABILITY DETAILS**

This commit is a cause of this vulnerability : <https://chromium-review.googlesource.com/c/chromium/src/+/3747422>

```
void TableView::Select(absl::optional<size_t> model_row) {  
  if (!model_)  
    return;  
  
  SelectByViewIndex(model_row.has_value()  
                        ? absl::make_optional(ModelToView(model_row.value()))  
                        : absl::nullopt);  
}  

```

In the case of `TableView::Select`, `model_row` can be -1.

```
void TableView::SelectByViewIndex(absl::optional<size_t> view_index) {  
  ui::ListSelectionModel new_selection;  
  if (view_index.has_value()) {  
    SelectRowsInRangeFrom(view_index.value(), true, &new_selection);  
    new_selection.set_anchor(ViewToModel(view_index.value()));  
    new_selection.set_active(ViewToModel(view_index.value()));  
  }  
  
  SetSelectionModel(std::move(new_selection));  
}  

```

But there is no check for `view_index`. That check was removed by the above commit.

```
void TaskManagerView::SelectTaskOfActiveTab(Browser\* browser) {  
  if (browser) {  
    tab_table_->Select(table_model_->GetRowForWebContents(  
        browser->tab_strip_model()->GetActiveWebContents()));  
  }  
}  

```

It leads to Heap-buffer-overflow in TaskManagerView::SelectTaskOfActiveTab. Because GetRowForWebContents can return the -1.

\* Patch Suggestion

```
void TableView::SelectByViewIndex(absl::optional<size_t> view_index) {  
  ui::ListSelectionModel new_selection;  
  if (view_index.has_value() && view_index.value() != -1) {  
    SelectRowsInRangeFrom(view_index.value(), true, &new_selection);  
    new_selection.set_anchor(ViewToModel(view_index.value()));  
    new_selection.set_active(ViewToModel(view_index.value()));  
  }  
  
  SetSelectionModel(std::move(new_selection));  
}  

```

Add a check for view\_index. (view\_index.value() != -1)

**VERSION**  

Chrome Version: asan-win32-release\_x64-1028585  

Operating System: Windows 10

**REPRODUCTION CASE**

To trigger this bug, an attacker should kill the renderer by some ways.  

I used “chrome://memory-exhaust” to demonstrate this vulnerability. ("chrome://kill" can also be used.)  

BUT this bug can also be reproduced by V8 OOM. So It can be intended by an attacker. (I attached the asan log using V8 OOM)

1. kill renderer (tab chrome://memory-exhaust)
2. open TaskManager (shift + esc or click)

I attached the PoC video.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

=================================================================  

==8976==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x12b032731b88 at pc 0x7ffcc77ff41c bp 0x00e8701fd400 sp 0x00e8701fd448  

READ of size 8 at 0x12b032731b88 thread T0  

==8976==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ffcc77ff41b in task\_manager::TaskManagerTableModel::GetRowsGroupRange C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\task\_manager\task\_manager\_table\_model.cc:645  

#1 0x7ffcc6fc4348 in views::TableView::SelectRowsInRangeFrom C:\b\s\w\ir\cache\builder\src\ui\views\controls\table\table\_view.cc:1422  

#2 0x7ffcc6fb50a9 in views::TableView::SelectByViewIndex C:\b\s\w\ir\cache\builder\src\ui\views\controls\table\table\_view.cc:1313  

#3 0x7ffcc6fb4e67 in views::TableView::Select C:\b\s\w\ir\cache\builder\src\ui\views\controls\table\table\_view.cc:300  

#4 0x7ffcc31d6cfd in task\_manager::TaskManagerView::SelectTaskOfActiveTab C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\task\_manager\_view.cc:383  

#5 0x7ffcc31d698f in task\_manager::TaskManagerView::Show C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\task\_manager\_view.cc:99  

#6 0x7ffcc1cea393 in chrome::OpenTaskManager C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser\_commands.cc:1558  

#7 0x7ffcc1cb454d in chrome::BrowserCommandController::ExecuteCommandWithDisposition C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser\_command\_controller.cc:772  

#8 0x7ffccad9fbd8 in AppMenuModel::ExecuteCommand C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\toolbar\app\_menu\_model.cc:391  

#9 0x7ffccad952a2 in AppMenu::ExecuteCommand C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\toolbar\app\_menu.cc:1014  

#10 0x7ffcc2befdb4 in views::internal::MenuRunnerImpl::OnMenuClosed C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_runner\_impl.cc:233  

#11 0x7ffcc6f84e02 in views::MenuController::ExitMenu C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_controller.cc:3167  

#12 0x7ffcc6f89eef in views::MenuController::Accept C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_controller.cc:1773  

#13 0x7ffcc6f89590 in views::MenuController::OnMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_controller.cc:829  

#14 0x7ffcbced5335 in views::Widget::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1565  

#15 0x7ffcbde27c78 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:190  

#16 0x7ffcbde270cf in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:139  

#17 0x7ffcbde2697c in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:83  

#18 0x7ffcbde266b0 in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:55  

#19 0x7ffcc2bd86dc in ui::EventProcessor::OnEventFromSource C:\b\s\w\ir\cache\builder\src\ui\events\event\_processor.cc:49  

#20 0x7ffcbfa946ab in ui::EventSource::DeliverEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:118  

#21 0x7ffcbfa942f2 in ui::EventSource::SendEventToSinkFromRewriter C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:143  

#22 0x7ffcbfa93dd3 in ui::EventSource::SendEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:112  

#23 0x7ffcc2c1b9d7 in views::DesktopWindowTreeHostWin::HandleMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_window\_tree\_host\_win.cc:1004  

#24 0x7ffcc6fdff34 in views::HWNDMessageHandler::HandleMouseEventInternal C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:3276  

#25 0x7ffcc6fd8dc7 in views::HWNDMessageHandler::\_ProcessWindowMessage C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.h:360  

#26 0x7ffcc6fd8409 in views::HWNDMessageHandler::OnWndProc C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:1092  

#27 0x7ffcc020468c in gfx::WindowImpl::WndProc C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window\_impl.cc:306  

#28 0x7ffcc0202ffe in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> C:\b\s\w\ir\cache\builder\src\base\win\wrapped\_window\_proc.h:74  

#29 0x7ffd2a48e857 in CallWindowProcW+0x3f7 (C:\Windows\System32\user32.dll+0x18000e857)  

#30 0x7ffd2a48e298 in DispatchMessageW+0x258 (C:\Windows\System32\user32.dll+0x18000e298)  

#31 0x7ffcbd227fef in base::MessagePumpForUI::ProcessMessageHelper C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:531  

#32 0x7ffcbd225fa5 in base::MessagePumpForUI::ProcessNextWindowsMessage C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:498  

#33 0x7ffcbd2257df in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:209  

#34 0x7ffcbd22397b in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#35 0x7ffcbfec849b in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:581  

#36 0x7ffcbd10bf52 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#37 0x7ffcb58826b5 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1042  

#38 0x7ffcb5888017 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:157  

#39 0x7ffcb587b809 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#40 0x7ffcbccc17df in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:678  

#41 0x7ffcbccc4720 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1197  

#42 0x7ffcbccc4008 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1062  

#43 0x7ffcbccc04b2 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:406  

#44 0x7ffcbccc0be2 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:434  

#45 0x7ffcb15314ac in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:182  

#46 0x7ff6a4315a0e in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:162  

#47 0x7ff6a4312bd0 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:395  

#48 0x7ff6a471795f in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#49 0x7ffd2a147033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#50 0x7ffd2b5e2650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

0x12b032731b88 is located 8 bytes to the left of 40-byte region [0x12b032731b90,0x12b032731bb8)  

allocated by thread T0 here:  

#0 0x7ff6a43ba42c in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffcd048246e in operator new d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ffcb1607b6d in std::Cr::vector<perfetto::trace\_processor::GlobalNodeGraph::Edge \*,std::Cr::allocator<perfetto::trace\_processor::GlobalNodeGraph::Edge \*> >::\_\_vallocate C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\vector:673  

#3 0x7ffcb1914918 in std::Cr::vector<unsigned long long,std::Cr::allocator<unsigned long long> >::assign<unsigned long long \*> C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\vector:1339  

#4 0x7ffcc77ff518 in task\_manager::TaskManagerTableModel::OnTaskAdded C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\task\_manager\task\_manager\_table\_model.cc:670  

#5 0x7ffcbfd35e5a in task\_manager::TaskManagerInterface::NotifyObserversOnTaskAdded C:\b\s\w\ir\cache\builder\src\chrome\browser\task\_manager\task\_manager\_interface.cc:131  

#6 0x7ffcc32340de in task\_manager::TaskManagerImpl::TaskAdded C:\b\s\w\ir\cache\builder\src\chrome\browser\task\_manager\sampling\task\_manager\_impl.cc:511  

#7 0x7ffcc78a66b4 in task\_manager::FallbackTaskProvider::ShowTask C:\b\s\w\ir\cache\builder\src\chrome\browser\task\_manager\providers\fallback\_task\_provider.cc:137  

#8 0x7ffcc78a6b4a in task\_manager::FallbackTaskProvider::OnTaskAddedBySource C:\b\s\w\ir\cache\builder\src\chrome\browser\task\_manager\providers\fallback\_task\_provider.cc:173  

#9 0x7ffcc78a750a in task\_manager::FallbackTaskProvider::SubproviderSource::TaskAdded C:\b\s\w\ir\cache\builder\src\chrome\browser\task\_manager\providers\fallback\_task\_provider.cc:217  

#10 0x7ffcc789b1c1 in task\_manager::SpareRenderProcessHostTaskProvider::SpareRenderProcessHostTaskChanged C:\b\s\w\ir\cache\builder\src\chrome\browser\task\_manager\providers\spare\_render\_process\_host\_task\_provider.cc:67  

#11 0x7ffcb65770f5 in content::RenderProcessHost::RegisterSpareRenderProcessHostChangedCallback C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_process\_host\_impl.cc:2998  

#12 0x7ffcc789ae06 in task\_manager::SpareRenderProcessHostTaskProvider::StartUpdating C:\b\s\w\ir\cache\builder\src\chrome\browser\task\_manager\providers\spare\_render\_process\_host\_task\_provider.cc:40  

#13 0x7ffcc78a56f2 in task\_manager::FallbackTaskProvider::StartUpdating C:\b\s\w\ir\cache\builder\src\chrome\browser\task\_manager\providers\fallback\_task\_provider.cc:74  

#14 0x7ffcc323573f in task\_manager::TaskManagerImpl::StartUpdating C:\b\s\w\ir\cache\builder\src\chrome\browser\task\_manager\sampling\task\_manager\_impl.cc:647  

#15 0x7ffcbfd34572 in task\_manager::TaskManagerInterface::AddObserver C:\b\s\w\ir\cache\builder\src\chrome\browser\task\_manager\task\_manager\_interface.cc:74  

#16 0x7ffcc77f87fc in task\_manager::TaskManagerTableModel::StartUpdating C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\task\_manager\task\_manager\_table\_model.cc:907  

#17 0x7ffcc77f8720 in task\_manager::TaskManagerTableModel::TaskManagerTableModel C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\task\_manager\task\_manager\_table\_model.cc:324  

#18 0x7ffcc31d8aaa in task\_manager::TaskManagerView::Init C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\task\_manager\_view.cc:335  

#19 0x7ffcc31d7184 in task\_manager::TaskManagerView::TaskManagerView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\task\_manager\_view.cc:312  

#20 0x7ffcc31d665c in task\_manager::TaskManagerView::Show C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\task\_manager\_view.cc:78  

#21 0x7ffcc1cea393 in chrome::OpenTaskManager C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser\_commands.cc:1558  

#22 0x7ffcc1cb454d in chrome::BrowserCommandController::ExecuteCommandWithDisposition C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser\_command\_controller.cc:772  

#23 0x7ffccad9fbd8 in AppMenuModel::ExecuteCommand C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\toolbar\app\_menu\_model.cc:391  

#24 0x7ffccad952a2 in AppMenu::ExecuteCommand C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\toolbar\app\_menu.cc:1014  

#25 0x7ffcc2befdb4 in views::internal::MenuRunnerImpl::OnMenuClosed C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_runner\_impl.cc:233  

#26 0x7ffcc6f84e02 in views::MenuController::ExitMenu C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_controller.cc:3167  

#27 0x7ffcc6f89eef in views::MenuController::Accept C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_controller.cc:1773

SUMMARY: AddressSanitizer: heap-buffer-overflow C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\task\_manager\task\_manager\_table\_model.cc:645 in task\_manager::TaskManagerTableModel::GetRowsGroupRange  

Shadow bytes around the buggy address:  

0x04fe38366320: f7 fa 00 00 00 00 00 fa f7 fa fd fd fd fd fd fd  

0x04fe38366330: f7 fa 00 00 00 00 00 00 f7 fa 00 00 00 00 00 fa  

0x04fe38366340: f7 fa 00 00 00 00 00 00 f7 fa 00 00 00 00 00 00  

0x04fe38366350: f7 fa 00 00 00 00 00 00 f7 fa fd fd fd fd fd fa  

0x04fe38366360: f7 fa 00 00 00 00 00 fa f7 fa fd fd fd fd fd fa  

=>0x04fe38366370: f7[fa]00 00 00 00 00 fa f7 fa 00 00 00 00 00 00  

0x04fe38366380: f7 fa fd fd fd fd fd fd f7 fa fd fd fd fd fd fd  

0x04fe38366390: f7 fa 00 00 00 00 00 00 f7 fa 00 00 00 00 00 fa  

0x04fe383663a0: f7 fa fd fd fd fd fd fa f7 fa 00 00 00 00 00 fa  

0x04fe383663b0: f7 fa fd fd fd fd fd fa f7 fa 00 00 00 00 00 fa  

0x04fe383663c0: f7 fa fd fd fd fd fd fa f7 fa 00 00 00 00 00 fa  

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

==8976==ABORTING

**CREDIT INFORMATION**  

Reporter credit: YoungJoo Lee(@ashuu\_lee) of CompSec Lab at Seoul National University

## Attachments

- [poc_07_28.mp4](attachments/poc_07_28.mp4) (video/mp4, 2.0 MB)
- [v8oom_heapoverflow_asan_log.txt](attachments/v8oom_heapoverflow_asan_log.txt) (text/plain, 40.3 KB)

## Timeline

### [Deleted User] (2022-07-28)

[Empty comment from Monorail migration]

### bh...@google.com (2022-07-28)

Thanks for the detailed report and analysis. Marking high severity although it requires action to go to the task manager.

Peter, should we have GetRowForWebContents return an optional too?



[Monorail components: Security UI>TaskManager]

### bh...@google.com (2022-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-29)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-29)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pk...@chromium.org (2022-07-29)

Yes, the right fix is for TaskManagerTableModel::GetRowForWebContents() to return an optional<size_t>.

### pk...@chromium.org (2022-08-01)

[Empty comment from Monorail migration]

### bh...@google.com (2022-08-02)

[Empty comment from Monorail migration]

### bh...@google.com (2022-08-02)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5b6a7b0636718a14bc9988f0863c78b7e935e3cd

commit 5b6a7b0636718a14bc9988f0863c78b7e935e3cd
Author: Peter Kasting <pkasting@chromium.org>
Date: Tue Aug 02 01:12:41 2022

Fix API usage mismatch.

Bug: 1348082
Change-Id: Ic90e0ed8ee02a8b71edaec04bd4ff7580cc2ee85
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3803591
Commit-Queue: Peter Kasting <pkasting@chromium.org>
Reviewed-by: Ahmed Fakhry <afakhry@chromium.org>
Commit-Queue: Ahmed Fakhry <afakhry@chromium.org>
Auto-Submit: Peter Kasting <pkasting@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1030357}

[modify] https://crrev.com/5b6a7b0636718a14bc9988f0863c78b7e935e3cd/chrome/browser/ui/task_manager/task_manager_table_model.cc
[modify] https://crrev.com/5b6a7b0636718a14bc9988f0863c78b7e935e3cd/chrome/browser/ui/task_manager/task_manager_table_model.h


### pk...@chromium.org (2022-08-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-08-02)

ClusterFuzz testcase 6414072967004160 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mojo&range=1030355:1030363

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2022-08-03)

Merge approved: your change passed merge requirements and is auto-approved for M105. Please go ahead and merge the CL to branch 5195 (refs/branch-heads/5195) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-08-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8a21bf0f51a4f8a8096850cf7c541520d6f1c86b

commit 8a21bf0f51a4f8a8096850cf7c541520d6f1c86b
Author: Peter Kasting <pkasting@chromium.org>
Date: Thu Aug 04 16:17:25 2022

Fix API usage mismatch.

(cherry picked from commit 5b6a7b0636718a14bc9988f0863c78b7e935e3cd)

Bug: 1348082
Change-Id: Ic90e0ed8ee02a8b71edaec04bd4ff7580cc2ee85
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3803591
Commit-Queue: Peter Kasting <pkasting@chromium.org>
Reviewed-by: Ahmed Fakhry <afakhry@chromium.org>
Commit-Queue: Ahmed Fakhry <afakhry@chromium.org>
Auto-Submit: Peter Kasting <pkasting@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1030357}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3809311
Cr-Commit-Position: refs/branch-heads/5195@{#225}
Cr-Branched-From: 7aa3f074a7907975b001346cc0288d0214af8451-refs/heads/main@{#1027018}

[modify] https://crrev.com/8a21bf0f51a4f8a8096850cf7c541520d6f1c86b/chrome/browser/ui/task_manager/task_manager_table_model.cc
[modify] https://crrev.com/8a21bf0f51a4f8a8096850cf7c541520d6f1c86b/chrome/browser/ui/task_manager/task_manager_table_model.h


### [Deleted User] (2022-08-04)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-08-05)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-05)

The CL that caused the issue landed in 105 https://crrev.com/c/3747422

### am...@google.com (2022-08-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-11)

Congratulations on another one YoungJoo Lee! The VRP Panel has decided to award you $4,000 for this report. The reward amount was based on this issue being mildly mitigated by not being remote exploitable and the user interaction required. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### yo...@snu.ac.kr (2022-08-30)

Thank you! Can I get CVE for this?

### am...@chromium.org (2022-08-31)

You're welcome, thanks again for your report!

>Can I get CVE for this?
This issue was introduced from a CL landed 6 July and at the time of reporting this issue would have impacted head and soon early dev. As this issue was resolved before impacting Stable channel, it would not receive a CVE. 

### [Deleted User] (2022-11-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1348082?no_tracker_redirect=1

[Multiple monorail components: Security, UI>TaskManager]
[Monorail mergedwith: crbug.com/chromium/1342854, crbug.com/chromium/1348947]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060426)*
