# Type Confuse Security DCHECK failed: !node || IsTextControl(*node) text_control_element.h(268) 

| Field | Value |
|-------|-------|
| **Issue ID** | [40058345](https://issues.chromium.org/issues/40058345) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Forms>Text, Blink>Layout |
| **Platforms** | Android, Linux, Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | fu...@chromium.org |
| **Created** | 2021-12-26 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4761.0 Safari/537.36

Steps to reproduce the problem:
#TestOn
Windows NT 10.0; Win64; x64
gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-953544.zip

#Reproduce
3. chrome --js-flags='--expose_gc --allow-natives-syntax' --no-sandbox --enable-blink-test-features --user-data-dir=notexits fuzz-01.html

What is the expected behavior?

What went wrong?
Type of crash
render tab

#Minicase
Come soon

#Analysis
Come soon

#Patch
Not yet

#asan
[5308:3392:1227/000611.965:FATAL:text_control_element.h(268)] Security DCHECK failed: !node || IsTextControl(*node).
Backtrace:
base::debug::CollectStackTrace [0x00007FFBF55630B2+18] (C:\b\s\w\ir\cache\builder\src\base\debug\stack_trace_win.cc:305)
base::debug::StackTrace::StackTrace [0x00007FFBF538955A+26] (C:\b\s\w\ir\cache\builder\src\base\debug\stack_trace.cc:197)
logging::LogMessage::~LogMessage [0x00007FFBF53C163C+860] (C:\b\s\w\ir\cache\builder\src\base\logging.cc:587)
blink::ToTextControl [0x00007FFBFA26D756+710] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\forms\text_control_element.h:268)
blink::LayoutTextControl::InnerEditorElement [0x00007FFC008B0CD3+67] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_text_control.cc:51)
blink::LayoutTextControlSingleLine::UpdateLayout [0x00007FFC010A1DE7+455] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_text_control_single_line.cc:74)
blink::LayoutBlockFlow::LayoutInlineChildren [0x00007FFBFD819615+5333] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow_line.cc:2046)
blink::LayoutBlockFlow::LayoutChildren [0x00007FFBFD31B338+1272] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:620)
blink::LayoutBlockFlow::UpdateBlockLayout [0x00007FFBFD31A0DF+1183] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:483)
blink::LayoutBlock::UpdateLayout [0x00007FFBFD1D4F24+196] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block.cc:461)
blink::LayoutBlockFlow::PositionAndLayoutOnceIfNeeded [0x00007FFBFD324F05+1653] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:837)
blink::LayoutBlockFlow::LayoutBlockChild [0x00007FFBFD326D37+1559] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:952)
blink::LayoutBlockFlow::LayoutBlockChildren [0x00007FFBFD321031+1953] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:1649)
blink::LayoutBlockFlow::LayoutChildren [0x00007FFBFD31B320+1248] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:622)
blink::LayoutBlockFlow::UpdateBlockLayout [0x00007FFBFD31A0DF+1183] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:483)
blink::LayoutBlock::UpdateLayout [0x00007FFBFD1D4F24+196] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block.cc:461)
blink::LayoutBlockFlow::PositionAndLayoutOnceIfNeeded [0x00007FFBFD324F05+1653] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:837)
blink::LayoutBlockFlow::LayoutBlockChild [0x00007FFBFD326D37+1559] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:952)
blink::LayoutBlockFlow::LayoutBlockChildren [0x00007FFBFD321031+1953] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:1649)
blink::LayoutBlockFlow::LayoutChildren [0x00007FFBFD31B320+1248] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:622)
blink::LayoutBlockFlow::UpdateBlockLayout [0x00007FFBFD31A0DF+1183] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:483)
blink::LayoutBlock::UpdateLayout [0x00007FFBFD1D4F24+196] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block.cc:461)
blink::LayoutBlockFlow::PositionAndLayoutOnceIfNeeded [0x00007FFBFD324F05+1653] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:837)
blink::LayoutBlockFlow::LayoutBlockChild [0x00007FFBFD326D37+1559] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:952)
blink::LayoutBlockFlow::LayoutBlockChildren [0x00007FFBFD321031+1953] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:1649)
blink::LayoutBlockFlow::LayoutChildren [0x00007FFBFD31B320+1248] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:622)
blink::LayoutBlockFlow::UpdateBlockLayout [0x00007FFBFD31A0DF+1183] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:483)
blink::LayoutView::UpdateBlockLayout [0x00007FFBFA15D18D+2477] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_view.cc:333)
blink::LayoutBlock::UpdateLayout [0x00007FFBFD1D4F24+196] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block.cc:461)
blink::LayoutView::UpdateLayout [0x00007FFBFA15DB41+1697] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_view.cc:374)
blink::LocalFrameView::PerformLayout [0x00007FFBFA001E85+4437] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:831)
blink::LocalFrameView::UpdateLayout [0x00007FFBFA00483D+1197] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:892)
blink::LocalFrameView::UpdateStyleAndLayoutInternal [0x00007FFBFA0279AE+1038] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:3224)
blink::LocalFrameView::UpdateStyleAndLayout [0x00007FFBFA00CCE4+340] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:3164)
blink::Document::UpdateStyleAndLayout [0x00007FFBFA0C87A1+801] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:2477)
blink::Document::ImplicitClose [0x00007FFBFA0D85FA+1306] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:3499)
blink::Document::CheckCompletedInternal [0x00007FFBFA0D8F05+757] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:3574)
blink::Document::LoadEventDelayTimerFired [0x00007FFBFA0B02A5+21] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:7160)
blink::FrameLoader::FinishedParsing [0x00007FFBFA211EFE+1070] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\frame_loader.cc:382)
blink::Document::FinishedParsing [0x00007FFBFA1045FC+1260] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:6631)
blink::HTMLDocumentParser::end [0x00007FFBFD6A50B2+402] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:1369)
blink::HTMLDocumentParser::PrepareToStopParsing [0x00007FFBFD6923ED+653] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:552)
blink::HTMLDocumentParser::EndIfDelayed [0x00007FFBFD69386E+702] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:1422)
blink::HTMLDocumentParser::DeferredPumpTokenizerIfPossible [0x00007FFBFD692F38+552] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:592)
base::TaskAnnotator::RunTaskImpl [0x00007FFBF54D3255+933] (C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135)
base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl [0x00007FFBF8015E56+1206] (C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:356)
base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork [0x00007FFBF8015529+377] (C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:261)
base::MessagePumpDefault::Run [0x00007FFBF7FEE458+712] (C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:38)
base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run [0x00007FFBF8017522+754] (C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:468)
base::RunLoop::Run [0x00007FFBF5451DC4+1300] (C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:142)
content::RendererMain [0x00007FFBF7AE60E3+2723] (C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:283)
content::RunOtherNamedProcessTypeMain [0x00007FFBF11023EE+927] (C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:678)
content::ContentMainRunnerImpl::Run [0x00007FFBF1103FC4+896] (C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1028)
content::RunContentProcess [0x00007FFBF1100242+1125] (C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:398)
content::ContentMain [0x00007FFBF11012CD+255] (C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:426)
ChromeMain [0x00007FFBEA9C148F+907] (C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:180)
MainDllLoader::Launch [0x00007FF776F45B86+1056] (C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169)
main [0x00007FF776F42B60+6898] (C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382)
__scrt_common_main_seh [0x00007FF777347440+268] (d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288)
BaseThreadInitThunk [0x00007FFC8CC37034+20]
RtlUserThreadStart [0x00007FFC8D7DCEC1+33]

Did this work before? N/A 

Chrome version: 99.0.4761.0  Channel: n/a
OS Version: 10.0

I previously reported a similar issue (https://bugs.chromium.org/p/chromium/issues/detail?id=1277004) and then ClusterFuzz said it was fixed and closed the case and dup to a non-secure report (I think VRP may need to consider whether it is correct), but I found that the new sample can reproduce the same problem, so I opened a new case.

## Attachments

- [fuzz-01.html](attachments/fuzz-01.html) (text/plain, 1.1 KB)
- [h1.js](attachments/h1.js) (text/plain, 3.5 KB)

## Timeline

### m....@gmail.com (2021-12-26)

[Comment Deleted]

### [Deleted User] (2021-12-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-12-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5099347894927360.

### cl...@chromium.org (2021-12-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-12-30)

[Empty comment from Monorail migration]

### ke...@chromium.org (2021-12-30)

Thanks for the report. It looks like the test case on https://crbug.com/chromium/1277004 might have stopped reproducing even though the bug was still valid. Thank you for finding another one.

Assigning to masonf@, who was the last owner of the previous bug, for investigation.

[Monorail components: Blink>Forms>Text]

### [Deleted User] (2021-12-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-30)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2021-12-30)

Detailed Report: https://clusterfuzz.com/testcase?key=5099347894927360

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Security DCHECK failure
Crash Address: 
Crash State:
  !node || IsTextControl(*node) in text_control_element.h
  blink::ToTextControl
  blink::LayoutTextControl::InnerEditorElement
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=947262:947266

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5099347894927360

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### [Deleted User] (2021-12-30)

[Empty comment from Monorail migration]

### ma...@chromium.org (2021-12-30)

Thanks! Looks like clusterfuzz found this as the culprit:

https://chromium.googlesource.com/chromium/src/+/e33c1fbb5c53d72c08dc07203084183f002ab158

Over to futhark to confirm.

### cl...@chromium.org (2021-12-30)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Layout]

### fu...@chromium.org (2022-01-05)

[Empty comment from Monorail migration]

### fu...@chromium.org (2022-01-05)

Feature disabled by default

### fu...@chromium.org (2022-01-06)

https://chromium-review.googlesource.com/c/chromium/src/+/3370281

### gi...@appspot.gserviceaccount.com (2022-01-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/809b8358c1c2ba4971990e56b728203b36298bf2

commit 809b8358c1c2ba4971990e56b728203b36298bf2
Author: Rune Lillesveen <futhark@chromium.org>
Date: Thu Jan 06 17:23:22 2022

[@container] Don't establish containers in legacy tree

Container Queries and legacy layout don't work together. Don't skip
style recalc or create a query evaluator for the cases we know we are
in a legacy tree.

Bug: 1282782
Change-Id: Ibcebf427a5eff583da1f73fb990239da99305fec
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3370281
Reviewed-by: Morten Stenshorne <mstensho@chromium.org>
Commit-Queue: Rune Lillesveen <futhark@chromium.org>
Cr-Commit-Position: refs/heads/main@{#956150}

[modify] https://crrev.com/809b8358c1c2ba4971990e56b728203b36298bf2/third_party/blink/renderer/core/css/style_recalc_change.cc
[modify] https://crrev.com/809b8358c1c2ba4971990e56b728203b36298bf2/third_party/blink/renderer/core/css/container_query_evaluator.cc
[modify] https://crrev.com/809b8358c1c2ba4971990e56b728203b36298bf2/third_party/blink/renderer/core/dom/document.cc
[modify] https://crrev.com/809b8358c1c2ba4971990e56b728203b36298bf2/third_party/blink/renderer/core/style/computed_style.h
[add] https://crrev.com/809b8358c1c2ba4971990e56b728203b36298bf2/third_party/blink/web_tests/external/wpt/css/css-contain/container-queries/input-column-group-container-crash.html
[modify] https://crrev.com/809b8358c1c2ba4971990e56b728203b36298bf2/third_party/blink/renderer/core/dom/element.cc
[modify] https://crrev.com/809b8358c1c2ba4971990e56b728203b36298bf2/third_party/blink/renderer/core/style/computed_style.cc


### fu...@chromium.org (2022-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-01-08)

ClusterFuzz testcase 5099347894927360 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=956149:956151

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### am...@google.com (2022-01-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-13)

Congratulations! The VRP Panel had decided to award you $5000 for this report. Thank you for your report and nice work! 

### am...@google.com (2022-01-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-02-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1282782?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Forms>Text, Blink>Layout]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058345)*
