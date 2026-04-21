# TypeConfuse in blink::LayoutTable::AddChild layout_table.cc:194

| Field | Value |
|-------|-------|
| **Issue ID** | [40060332](https://issues.chromium.org/issues/40060332) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>CSS |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | ko...@chromium.org |
| **Created** | 2022-07-20 |
| **Bounty** | $5,000.00 |

## Description

**Steps to reproduce the problem:**  

#TestOn  

asan-win32-release\_x64-1025626

#Reproduce

1. chrome --no-sandbox --user-data-dir=test poc.html

**Problem Description:**  

#Type of crash  

render tab

#Analysis  

some as <https://bugs.chromium.org/p/chromium/issues/detail?id=1341619>

When the |child| of the |LayoutTable::AddChild| is a  

|LayoutNGTableSection|, |child->IsTableSection()| is |true|, but  

|To<LayoutTableSection>(child)| causes a TypeConfuse.

#Patch

```
diff --git a/third_party/blink/renderer/core/layout/layout_table.cc b/third_party/blink/renderer/core/layout/layout_table.cc  
index 5317b674..f5c56153 100644  
--- a/third_party/blink/renderer/core/layout/layout_table.cc  
+++ b/third_party/blink/renderer/core/layout/layout_table.cc  
@@ -168,6 +168,10 @@  
     has_col_elements_ = true;  
     wrap_in_anonymous_section = false;  
   } else if (child->IsTableSection()) {  
+    // TODO(): Turn a SECURITY_DCHECK in |To| to a normal crash.  
+    // This happens when |child| is a |LayoutNGTableSection|.  
+    CHECK(IsA<LayoutTableSection>(child));  
+  
     switch (child->StyleRef().Display()) {  
       case EDisplay::kTableHeaderGroup:  
         ResetSectionPointerIfNotBefore(head_, before_child);  
  

```

**Additional Comments:**  

#asan  

[18444:8984:0720/185332.854:FATAL:casting.h(126)] Security DCHECK failed: IsA<Derived>(from).  

Backtrace:  

base::debug::CollectStackTrace [0x00007FF8E41BDA22+18] (C:\b\s\w\ir\cache\builder\src\base\debug\stack\_trace\_win.cc:329)  

base::debug::StackTrace::StackTrace [0x00007FF8E6A55C3A+26] (C:\b\s\w\ir\cache\builder\src\base\debug\stack\_trace.cc:218)  

logging::LogMessage::~LogMessage [0x00007FF8E402E766+662] (C:\b\s\w\ir\cache\builder\src\base\logging.cc:670)  

blink::To[blink::LayoutTableSection,blink::LayoutObject](javascript:void(0);) [0x00007FF8EFCB4C81+497] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\wtf\casting.h:131)  

blink::LayoutTable::AddChild [0x00007FF8EFCB41EF+3439] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_table.cc:194)  

blink::LayoutObject::AddChild [0x00007FF8EC218774+836] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_object.cc:576)  

blink::LayoutBlockFlow::AddChild [0x00007FF8EC752A12+1202] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_block\_flow.cc:2905)  

blink::Element::AttachLayoutTree [0x00007FF8E944FCCF+1199] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:3625)  

blink::Node::ReattachLayoutTree [0x00007FF8E9545A72+370] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\node.cc:1584)  

blink::Element::RebuildLayoutTree [0x00007FF8E9461BE1+817] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:4520)  

blink::ContainerNode::RebuildLayoutTreeForChild [0x00007FF8E97CF7FC+1020] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\container\_node.cc:1404)  

blink::ContainerNode::RebuildChildrenLayoutTrees [0x00007FF8E97CF9C3+99] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\container\_node.cc:1425)  

blink::Element::RebuildLayoutTree [0x00007FF8E9462223+2419] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:4554)  

blink::StyleEngine::RebuildLayoutTree [0x00007FF8E96F1D92+786] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\style\_engine.cc:2886)  

blink::StyleEngine::UpdateStyleAndLayoutTree [0x00007FF8E96F37AA+1386] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\style\_engine.cc:2954)  

blink::Document::UpdateStyle [0x00007FF8E911F1D0+576] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:2260)  

blink::Document::UpdateStyleAndLayoutTreeForThisDocument [0x00007FF8E911D044+1876] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:2209)  

blink::LocalFrameView::UpdateStyleAndLayoutInternal [0x00007FF8E906CCD6+358] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:3250)  

blink::LocalFrameView::UpdateStyleAndLayout [0x00007FF8E9057DA1+593] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:3202)  

blink::LocalFrameView::UpdateStyleAndLayoutIfNeededRecursive [0x00007FF8E90668E5+501] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:3122)  

blink::LocalFrameView::RunStyleAndLayoutLifecyclePhases [0x00007FF8E9062F79+297] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2566)  

blink::LocalFrameView::UpdateLifecyclePhasesInternal [0x00007FF8E9061553+1763] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2389)  

blink::LocalFrameView::UpdateLifecyclePhases [0x00007FF8E905FA2C+2252] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2326)  

blink::LayoutView::HitTest [0x00007FF8E91B7DA6+230] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_view.cc:150)  

blink::Document::PerformMouseEventHitTest [0x00007FF8E913A08D+717] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:4531)  

blink::EventHandler::GetMouseEventTarget [0x00007FF8E9368FD0+1264] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\input\event\_handler.cc:2529)  

blink::EventHandler::HandleMouseMoveOrLeaveEvent [0x00007FF8E936AFC3+2323] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\input\event\_handler.cc:1072)  

blink::EventHandler::HandleMouseMoveEvent [0x00007FF8E936A42B+411] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\input\event\_handler.cc:959)  

blink::WidgetEventHandler::HandleMouseMove [0x00007FF8EC494040+464] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\input\widget\_event\_handler.cc:148)  

blink::WidgetEventHandler::HandleInputEvent [0x00007FF8EC493A29+1769] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\input\widget\_event\_handler.cc:60)  

blink::WebFrameWidgetImpl::HandleInputEvent [0x00007FF8E9027A4D+2189] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\web\_frame\_widget\_impl.cc:2597)  

blink::WidgetBaseInputHandler::HandleInputEvent [0x00007FF8EC4F939E+2926] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\input\widget\_base\_input\_handler.cc:435)  

blink::WidgetInputHandlerManager::HandleInputEvent [0x00007FF8EC497AB1+625] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\input\widget\_input\_handler\_manager.cc:316)  

blink::MainThreadEventQueue::HandleEventOnMainThread [0x00007FF8EC4E13AE+526] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\input\main\_thread\_event\_queue.cc:681)  

blink::QueuedWebInputEvent::Dispatch [0x00007FF8EC4E2651+561] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\input\main\_thread\_event\_queue.cc:156)  

blink::MainThreadEventQueue::DispatchRafAlignedInput [0x00007FF8EC4E0DA0+1840] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\input\main\_thread\_event\_queue.cc:568)  

blink::WidgetBase::BeginMainFrame [0x00007FF8EC43A7CB+315] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\widget\_base.cc:895)  

cc::ProxyMain::BeginMainFrame [0x00007FF8E9BD8ED0+3696] (C:\b\s\w\ir\cache\builder\src\cc\trees\proxy\_main.cc:263)  

base::internal::Invoker<base::internal::BindState<void (cc::ProxyMain::\*)(std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState,std::Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >),base::WeakPtr[cc::ProxyMain](javascript:void(0);),std::Cr::unique\_ptr<cc::BeginMainFrame [0x00007FF8EDF52986+454] (C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:768)  

base::TaskAnnotator::RunTaskImpl [0x00007FF8E41241E5+917] (C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135)  

base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl [0x00007FF8E6E4190A+2666] (C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:428)  

base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork [0x00007FF8E6E40965+421] (C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:298)  

base::MessagePumpDefault::Run [0x00007FF8E6E1EC8B+491] (C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:39)  

base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run [0x00007FF8E6E43987+1095] (C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:581)  

base::RunLoop::Run [0x00007FF8E40BAC80+1328] (C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:143)  

content::RendererMain [0x00007FF8E69015F2+2910] (C:\b\s\w\ir\cache\builder\src\content\renderer\renderer\_main.cc:290)  

content::RunOtherNamedProcessTypeMain [0x00007FF8E3C72450+1313] (C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:720)  

content::ContentMainRunnerImpl::Run [0x00007FF8E3C745C9+1951] (C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1063)  

content::RunContentProcess [0x00007FF8E3C70AB3+3710] (C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:406)  

content::ContentMain [0x00007FF8E3C711E3+403] (C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:434)  

ChromeMain [0x00007FF8D85D14AD+937] (C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:182)  

MainDllLoader::Launch [0x00007FF7B6C35A0F+2047] (C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:162)  

main [0x00007FF7B6C32BD1+7011] (C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:395)  

\_\_scrt\_common\_main\_seh [0x00007FF7B7034140+268] (d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288)  

BaseThreadInitThunk [0x00007FF96A187034+20]  

RtlUserThreadStart [0x00007FF96B3C2651+33]  

Task trace:  

Backtrace:  

cc::ProxyImpl::ScheduledActionSendBeginMainFrame [0x00007FF8EDF4DC22+2578] (C:\b\s\w\ir\cache\builder\src\cc\trees\proxy\_impl.cc:724)  

cc::ProxyMain::BeginMainFrame [0x00007FF8E9BD9305+4773] (C:\b\s\w\ir\cache\builder\src\cc\trees\proxy\_main.cc:308)  

cc::ProxyImpl::ScheduledActionSendBeginMainFrame [0x00007FF8EDF4DC22+2578] (C:\b\s\w\ir\cache\builder\src\cc\trees\proxy\_impl.cc:724)  

cc::ProxyMain::BeginMainFrame [0x00007FF8E9BD9305+4773] (C:\b\s\w\ir\cache\builder\src\cc\trees\proxy\_main.cc:308)  

cc::ProxyImpl::ScheduledActionSendBeginMainFrame [0x00007FF8EDF4DC22+2578] (C:\b\s\w\ir\cache\builder\src\cc\trees\proxy\_impl.cc:724)

\*\*Chrome version: \*\* 103.0.5060.53 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 9.7 KB)
- [patch.diff](attachments/patch.diff) (text/plain, 734 B)
- [poc.html](attachments/poc.html) (text/plain, 1.3 KB)

## Timeline

### [Deleted User] (2022-07-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-07-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5754861578813440.

### cl...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-07-21)

Detailed Report: https://clusterfuzz.com/testcase?key=5754861578813440

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Security DCHECK failure
Crash Address: 
Crash State:
  IsA<Derived>(from) in casting.h
  blink::LayoutTableSection* blink::To<blink::LayoutTableSection, blink::LayoutObj
  blink::LayoutTable::AddChild
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1026459

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5754861578813440

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### rs...@chromium.org (2022-07-21)

Thanks for the report. This only reproduces for me in M105. Seems similar to https://crbug.com/chromium/1341619.

[Monorail components: Blink>Layout>Table]

### [Deleted User] (2022-07-21)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-21)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ko...@chromium.org (2022-07-21)

Yet another one caused by the container query.

[Monorail components: -Blink>Layout>Table Blink>CSS]

### gi...@appspot.gserviceaccount.com (2022-07-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9fa2ccf01a2083ef55eeb346e80027805ca3dabe

commit 9fa2ccf01a2083ef55eeb346e80027805ca3dabe
Author: Koji Ishii <kojii@chromium.org>
Date: Fri Jul 22 04:43:35 2022

Turn a SECURITY_DCHECK in |LayoutTable*::AddChild| to CHECK

Similar to r1021919 crrev.com/c/3750720 that turned the
SECURITY_DCHECK in |LayoutTableRow::AddChild| to CHECK,
this patch applies the same changes to all
|LayoutTable*::AddChild|.

When adding a child to a table, the call flow is:
1. |LayoutTable::AddChild|. If the child is a
   |LayoutTableSection|, this function handles it.
2. |LayoutTableSection::AddChild|. If the child is a
   |LayoutTableRow|, this function handles it.
3. |LayoutTableRow::AddChild|. If the child is not a
   |layoutTableCell|, this function creates an anonymous cell.

Fixed: 1345894
Change-Id: I486e80b5971fe073b729e8c8af197a03704bbf04
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3780566
Commit-Queue: Koji Ishii <kojii@chromium.org>
Auto-Submit: Koji Ishii <kojii@chromium.org>
Reviewed-by: Kent Tamura <tkent@chromium.org>
Commit-Queue: Kent Tamura <tkent@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1027119}

[modify] https://crrev.com/9fa2ccf01a2083ef55eeb346e80027805ca3dabe/third_party/blink/renderer/core/layout/layout_table_row.cc
[modify] https://crrev.com/9fa2ccf01a2083ef55eeb346e80027805ca3dabe/third_party/blink/renderer/core/layout/layout_table_section.cc
[modify] https://crrev.com/9fa2ccf01a2083ef55eeb346e80027805ca3dabe/third_party/blink/renderer/core/layout/layout_table.cc


### [Deleted User] (2022-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-22)

Requesting merge to dev M105 because latest trunk commit (1027119) appears to be after dev branch point (1027018).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2022-07-22)

ClusterFuzz testcase 5754861578813440 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1027107:1027120

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2022-07-25)

Merge approved: your change passed merge requirements and is auto-approved for M105. Please go ahead and merge the CL to branch 5195 (refs/branch-heads/5195) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS),  matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2022-07-25)

Please merge your change to M105 branch 5195 ASAP. Thank you. 

### gi...@appspot.gserviceaccount.com (2022-07-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/77041e86bcb847895afa016b3c9b4c5ab160c659

commit 77041e86bcb847895afa016b3c9b4c5ab160c659
Author: Koji Ishii <kojii@chromium.org>
Date: Mon Jul 25 20:19:45 2022

[Merge M105] Turn a SECURITY_DCHECK in |LayoutTable*::AddChild| to CHECK

Similar to r1021919 crrev.com/c/3750720 that turned the
SECURITY_DCHECK in |LayoutTableRow::AddChild| to CHECK,
this patch applies the same changes to all
|LayoutTable*::AddChild|.

When adding a child to a table, the call flow is:
1. |LayoutTable::AddChild|. If the child is a
   |LayoutTableSection|, this function handles it.
2. |LayoutTableSection::AddChild|. If the child is a
   |LayoutTableRow|, this function handles it.
3. |LayoutTableRow::AddChild|. If the child is not a
   |layoutTableCell|, this function creates an anonymous cell.

(cherry picked from commit 9fa2ccf01a2083ef55eeb346e80027805ca3dabe)

Fixed: 1345894
Change-Id: I486e80b5971fe073b729e8c8af197a03704bbf04
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3780566
Commit-Queue: Koji Ishii <kojii@chromium.org>
Auto-Submit: Koji Ishii <kojii@chromium.org>
Reviewed-by: Kent Tamura <tkent@chromium.org>
Commit-Queue: Kent Tamura <tkent@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1027119}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3779874
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5195@{#16}
Cr-Branched-From: 7aa3f074a7907975b001346cc0288d0214af8451-refs/heads/main@{#1027018}

[modify] https://crrev.com/77041e86bcb847895afa016b3c9b4c5ab160c659/third_party/blink/renderer/core/layout/layout_table_row.cc
[modify] https://crrev.com/77041e86bcb847895afa016b3c9b4c5ab160c659/third_party/blink/renderer/core/layout/layout_table_section.cc
[modify] https://crrev.com/77041e86bcb847895afa016b3c9b4c5ab160c659/third_party/blink/renderer/core/layout/layout_table.cc


### [Deleted User] (2022-07-25)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ko...@chromium.org (2022-07-26)

> 1. Was this issue a regression for the milestone it was found in?
> 2. Is this issue related to a change or feature merged after the latest LTS Milestone?

This is a regression in M105, crbug.com/1145970#c189, so M102 should be fine.

### rz...@google.com (2022-07-26)

Adding the not applicable labels because the regression in M105: https://crbug.com/1345894#c18

### am...@google.com (2022-07-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2022-07-28)

Congratulations! The VRP Panel has decided to award you $5000 for this report. Thank you for your efforts in reporting this issue to us and great work! 

### gi...@appspot.gserviceaccount.com (2022-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5e38e1aa0f83e2f03493f0399210821be4731440

commit 5e38e1aa0f83e2f03493f0399210821be4731440
Author: Rune Lillesveen <futhark@chromium.org>
Date: Thu Jul 28 17:47:04 2022

[@container] Containers forcing legacy for children

For size container queries, we may end up marking a size container
element to force legacy layout without re-attaching the LayoutObject
(since that is not possible during interleaved style/layout).

To make sure child layout objects are forced to legacy, we need to check
the element in addition to the ForceLegacyLayout() flag on the
LayoutObject in order to cover all cases when creating anonymous layout
objects, for instance for anonymous table objects.

Bug: 1345894, 1346969
Change-Id: Ifb3efd1643efd5b048d46dbda570dc4482dd7385
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3789987
Reviewed-by: Ian Kilpatrick <ikilpatrick@chromium.org>
Commit-Queue: Rune Lillesveen <futhark@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1029346}

[modify] https://crrev.com/5e38e1aa0f83e2f03493f0399210821be4731440/third_party/blink/renderer/core/layout/layout_object_child_list.cc
[modify] https://crrev.com/5e38e1aa0f83e2f03493f0399210821be4731440/third_party/blink/renderer/core/layout/layout_object_factory.cc
[modify] https://crrev.com/5e38e1aa0f83e2f03493f0399210821be4731440/third_party/blink/renderer/core/dom/layout_tree_builder.cc
[modify] https://crrev.com/5e38e1aa0f83e2f03493f0399210821be4731440/third_party/blink/renderer/core/layout/layout_object.h
[add] https://crrev.com/5e38e1aa0f83e2f03493f0399210821be4731440/third_party/blink/web_tests/external/wpt/css/css-contain/container-queries/crashtests/chrome-bug-1346969-crash.html
[modify] https://crrev.com/5e38e1aa0f83e2f03493f0399210821be4731440/third_party/blink/renderer/core/dom/element.cc
[modify] https://crrev.com/5e38e1aa0f83e2f03493f0399210821be4731440/third_party/blink/renderer/core/layout/layout_object.cc


### am...@google.com (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1345894?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/1145970]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060332)*
