# Type confuse in blink::To<blink::LayoutTableSection,blink::LayoutObject> layout_table.cc:175

| Field | Value |
|-------|-------|
| **Issue ID** | [40059136](https://issues.chromium.org/issues/40059136) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Layout |
| **Platforms** | Android, Fuchsia, Linux, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | fu...@chromium.org |
| **Created** | 2022-03-18 |
| **Bounty** | $6,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36

Steps to reproduce the problem:
#TestOn
asan-win32-release_x64-982586

#Reproduce
The problem was found by my fuzzer running on CF(CC Security team for access permission https://clusterfuzz.com/testcase-detail/5707595184406528),
The orignal sample cannot be reproduced stably, CF does not automatically report.
By manual review, finally I made a stable reproduction minial sample.

chrome --no-sandbox  --enable-blink-test-features --user-data-dir=test D:\tmp\2022\vulr\clusterfuzz-testcase-5707595184406528\fuzz-00270.html
[--enable-blink-test-features] flag is need for reproduce

What is the expected behavior?

What went wrong?

#Type of crash
render tab

#Analysis
Using the sample I provided to trigger CF again to get more information

#asan
[5060:5580:0318/163210.566:FATAL:casting.h(126)] Security DCHECK failed: IsA<Derived>(from).
Backtrace:
        base::debug::CollectStackTrace [0x00007FFAD5AC57B2+18] (C:\b\s\w\ir\cache\builder\src\base\debug\stack_trace_win.cc:305)
        base::debug::StackTrace::StackTrace [0x00007FFAD58E20AA+26] (C:\b\s\w\ir\cache\builder\src\base\debug\stack_trace.cc:218)
        logging::LogMessage::~LogMessage [0x00007FFAD591A4CA+762] (C:\b\s\w\ir\cache\builder\src\base\logging.cc:600)
        blink::To<blink::LayoutTableSection,blink::LayoutObject> [0x00007FFAE1247F39+505] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\casting.h:131)
        blink::LayoutTable::AddChild [0x00007FFAE12474CE+3070] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_table.cc:175)
        blink::LayoutBlock::AddChildBeforeDescendant [0x00007FFADDD63619+1065] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block.cc:373)
        blink::LayoutBlockFlow::AddChild [0x00007FFADDEE648D+445] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:2969)
        blink::Element::AttachLayoutTree [0x00007FFADAECF8F6+758] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:2697)
        blink::Node::ReattachLayoutTree [0x00007FFADAFA9692+370] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\node.cc:1570)
        blink::Element::RebuildLayoutTree [0x00007FFADAEE22AE+942] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3508)
        blink::ContainerNode::RebuildLayoutTreeForChild [0x00007FFADB21C65C+1020] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1404)
        blink::ContainerNode::RebuildChildrenLayoutTrees [0x00007FFADB21C823+99] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1425)
        blink::Element::RebuildLayoutTree [0x00007FFADAEE2A79+2937] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3542)
        blink::StyleEngine::RebuildLayoutTree [0x00007FFADB16D029+697] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\style_engine.cc:2716)
        blink::StyleEngine::UpdateStyleAndLayoutTreeForContainer [0x00007FFADB16C31F+1455] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\style_engine.cc:2624)
        blink::NGBlockNode::Layout [0x00007FFAE14BAA8E+2702] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_node.cc:469)
        blink::LayoutNGMixin<blink::LayoutProgress>::UpdateInFlowBlockLayout [0x00007FFAE16BBD74+980] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\layout_ng_mixin.cc:409)
        blink::LayoutNGBlockFlowMixin<blink::LayoutProgress>::UpdateNGBlockLayout [0x00007FFAE16FBE35+69] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\layout_ng_block_flow_mixin.cc:275)
        blink::LayoutBlock::UpdateLayout [0x00007FFADDD64794+196] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block.cc:472)
        blink::LayoutBlockFlow::PositionAndLayoutOnceIfNeeded [0x00007FFADDEC9438+1656] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:837)
        blink::LayoutBlockFlow::LayoutBlockChild [0x00007FFADDECB334+1556] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:952)
        blink::LayoutBlockFlow::LayoutBlockChildren [0x00007FFADDEC52B6+1958] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:1649)
        blink::LayoutBlockFlow::LayoutChildren [0x00007FFADDEBF4B5+1237] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:622)
        blink::LayoutBlockFlow::UpdateBlockLayout [0x00007FFADDEBE26F+1183] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:483)
        blink::LayoutView::UpdateBlockLayout [0x00007FFADAC5776D+2509] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_view.cc:335)
        blink::LayoutBlock::UpdateLayout [0x00007FFADDD64794+196] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block.cc:472)
        blink::LayoutView::UpdateLayout [0x00007FFADAC580B5+1589] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_view.cc:376)
        blink::LocalFrameView::PerformLayout [0x00007FFADAAF53D3+5747] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:863)
        blink::LocalFrameView::UpdateLayout [0x00007FFADAAF7BAA+1402] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:926)
        blink::LocalFrameView::UpdateStyleAndLayoutInternal [0x00007FFADAB1C863+1043] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:3272)
        blink::LocalFrameView::UpdateStyleAndLayout [0x00007FFADAB00A81+353] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:3211)
        blink::Document::UpdateStyleAndLayout [0x00007FFADABC24F0+800] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:2529)
        blink::Document::UpdateStyleAndLayoutTree [0x00007FFADABC0F4C+1132] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:2044)
        blink::Document::FinishedParsing [0x00007FFADABFF31B+1291] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:6647)
        blink::HTMLDocumentParser::PrepareToStopParsing [0x00007FFADE238D73+723] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:511)
        blink::HTMLDocumentParser::AttemptToEnd [0x00007FFADE23CBE1+545] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:989)
        blink::HTMLDocumentParser::PumpTokenizerIfPossible [0x00007FFADE23936B+859] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:581)
        blink::HTMLDocumentParser::DeferredPumpTokenizerIfPossible [0x00007FFADE239A87+583] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:555)
        base::TaskAnnotator::RunTaskImpl [0x00007FFAD5A2A9A5+933] (C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135)
        base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl [0x00007FFAD8900D66+1174] (C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:385)
        base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork [0x00007FFAD890035A+410] (C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:290)
        base::MessagePumpDefault::Run [0x00007FFAD88D898B+379] (C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:39)
        base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run [0x00007FFAD89024D1+753] (C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:497)
        base::RunLoop::Run [0x00007FFAD59A8F44+1300] (C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:143)
        content::RendererMain [0x00007FFAD83F2023+2723] (C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:290)
        content::RunOtherNamedProcessTypeMain [0x00007FFAD55DB1AC+1273] (C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:684)
        content::ContentMainRunnerImpl::Run [0x00007FFAD55DCDE8+1148] (C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1044)
        content::RunContentProcess [0x00007FFAD55D97DC+3403] (C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:407)
        content::ContentMain [0x00007FFAD55D9F65+407] (C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:435)
        ChromeMain [0x00007FFACA6514CB+967] (C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:179)
        MainDllLoader::Launch [0x00007FF6D1005B17+945] (C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:167)
        main [0x00007FF6D1002B60+6898] (C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382)
        __scrt_common_main_seh [0x00007FF6D13FE944+268] (d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288)
        BaseThreadInitThunk [0x00007FFB5C247034+20]
        RtlUserThreadStart [0x00007FFB5DC42651+33]

Did this work before? N/A 

Chrome version: 101.0.0.0  Channel: n/a
OS Version: 10.0

## Attachments

- [fuzz-00270.html](attachments/fuzz-00270.html) (text/plain, 148 B)
- [asan.txt](attachments/asan.txt) (text/plain, 8.5 KB)

## Timeline

### m....@gmail.com (2022-03-18)

If you need the original CF report CC security team to associates the issue with CF(https://clusterfuzz.com/testcase-detail/5707595184406528).

Please add  Restrict-View-SecurityEmbargo for this issue.

### [Deleted User] (2022-03-18)

[Empty comment from Monorail migration]

### ma...@chromium.org (2022-03-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-03-18)

Detailed Report: https://clusterfuzz.com/testcase?key=5707595184406528

Fuzzer: b0ring_webidl_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Security DCHECK failure
Crash Address: 
Crash State:
  IsA<Derived>(from) in casting.h
  blink::LayoutTableSection* blink::To<blink::LayoutTableSection, blink::LayoutObj
  blink::LayoutTable::AddChild
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=982586

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5707595184406528

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2022-03-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-03-18)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Layout]

### cl...@chromium.org (2022-03-18)

ClusterFuzz testcase 5707595184406528 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2022-03-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5654298289307648.

### cl...@chromium.org (2022-03-19)

Detailed Report: https://clusterfuzz.com/testcase?key=5654298289307648

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

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=966255:966262

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5654298289307648

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2022-03-19)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/7e006e8b203316c394ea3c992e0827cb8c185813 ([@container] Stop legacy propagation for CQ recalc container).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### ma...@chromium.org (2022-03-21)

Setting impact-none since the repro requires --enable-blink-test-features. Let us know if you think this can be reached with a default configuration.

Assuming this is cross platform.

### ad...@google.com (2022-03-22)

Assuming renderer type confusion => high severity, even if Security_Impact-None because the feature is not currently enabled in production builds.

### fu...@chromium.org (2022-03-31)

Smaller repro:

  <!doctype html>
  <html style="container-type: inline-size">
  <span style="columns: 1; display: table-header-group">Pass if no crash</span>


### fu...@chromium.org (2022-04-01)

The previous repro triggers DCHECKs, but not the security one. Here's a case for that:

  <!doctype html>
  <style>
    html { container-type: inline-size; }
    body, head, span { display: table-header-group; }
  </style>
  <span style="columns: 1">Pass if no crash</span>


### fu...@chromium.org (2022-04-01)

[Empty comment from Monorail migration]

### fu...@chromium.org (2022-04-01)

The security dcheck happens because we get sibling header groups which disagree on NG/legacy. A case which doesn't rely on styling <head>:

  <!doctype html>
  <div style="container-type:inline-size">
    <span style="display:table-header-group;columns:1">Pass if no crash</span>
    <span style="display:table-header-group;"></span>
  </div>

The first span is forced to legacy, but since the force-to-legacy will stop at containers to avoid re-attaching containers being laid out, the container will stay NG, hence the second span will also be NG.


### fu...@chromium.org (2022-04-01)

This is most likely only a problem for anonymous tables.


### cl...@chromium.org (2022-04-08)

ClusterFuzz testcase 5707595184406528 is flaky and no longer crashes, so closing issue.

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### cl...@chromium.org (2022-04-08)

ClusterFuzz testcase 5707595184406528 is closed as invalid, so closing issue.

### m....@gmail.com (2022-04-12)

CF was wrong still reproduce with https://crbug.com/chromium/1307656#c14,has anyone taken over this issue?

### m....@gmail.com (2022-04-19)

@ping~

### fu...@chromium.org (2022-04-19)

[Empty comment from Monorail migration]

### bo...@chromium.org (2022-04-19)

This your friendly Security Marshall checking in since this bug has been open a while without updates. Although the feature is not (yet?) enabled by default - hence the SecurityImpact-None label - we assume it could plausibly be convertible into to remote code execution within the renderer sandbox if shipped, so it does need a fix. 

@futhark, if you are not the right owner, could you please redirect as you see appropriate? CCing Blink's layout OWNERS for greater visibility so this doesn't slip through the cracks. 

Adding ClusterFuzz-Wrong label to keep ClusterFuzz auto-closure at bay. 

### fu...@chromium.org (2022-04-21)

We have concluded It's not worth fixing this issue now because:

1. We will not ship container queries with legacy layout fallback here
2. We don't think there is a simple way to fix this without chasing new clusterfuzz issues for a long time.

I will land a crash test to make sure we will test this when we ship container queries.


### gi...@appspot.gserviceaccount.com (2022-04-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/192db13f8509738079bce25996abe3252b70a0f1

commit 192db13f8509738079bce25996abe3252b70a0f1
Author: Rune Lillesveen <futhark@chromium.org>
Date: Fri Apr 22 08:46:17 2022

[@container] Add crash test for https://crbug.com/chromium/1307656

The combination for legacy fallback for columns on table-row-group,
anonymous table wrapper, and a size container crashes because we end up
mixing NG and legacy table boxes.

Bug: 1307656
Change-Id: I77599e80ef89ce05ca6fa98c619f1d1385ed3d6c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3599034
Reviewed-by: Morten Stenshorne <mstensho@chromium.org>
Commit-Queue: Rune Lillesveen <futhark@chromium.org>
Cr-Commit-Position: refs/heads/main@{#995097}

[modify] https://crrev.com/192db13f8509738079bce25996abe3252b70a0f1/third_party/blink/web_tests/TestExpectations
[add] https://crrev.com/192db13f8509738079bce25996abe3252b70a0f1/third_party/blink/web_tests/external/wpt/css/css-contain/container-queries/crashtests/columns-in-table-002-crash.html


### fu...@chromium.org (2022-04-22)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-04-22)

re c#26 I don't think the WontFix label is appropriate for security, we can CC amyressler for some advice.

### bo...@chromium.org (2022-04-22)

Since this bug is reachable in code that ships to users this report should remain open until the vulnerable code is either removed or fixed. Note that since exposing the vulnerability requires a non-standard flag, severity is limited to Medium (not High as before). The ImpactNone label is still accurate for the same reason: the vulnerability is not exposed in the default shipping configuration. 

### fu...@chromium.org (2022-04-22)

Blocking the container queries issue as another measure to make sure we are aware of this when going to shipping.

### fu...@chromium.org (2022-05-18)

[Empty comment from Monorail migration]

### fu...@chromium.org (2022-06-10)

[Empty comment from Monorail migration]

### fu...@chromium.org (2022-06-10)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-06-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7dcf0da88c74ed4e34edf9f63df39576519e04b2

commit 7dcf0da88c74ed4e34edf9f63df39576519e04b2
Author: Rune Lillesveen <futhark@chromium.org>
Date: Mon Jun 13 10:56:33 2022

[@container] Handle legacy fallback for table-row-groups

If NG table fragmentation support we fall back to legacy with tables
inside multicols. Make sure we mark the query container to force legacy
fallback for its children to avoid mixing NG and legacy table boxes
inside the container when the table box itself is anonymous.

Bug: 1307656
Change-Id: I408676e8dab92bea429ba005a6c418bd07c777b6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3695575
Commit-Queue: Rune Lillesveen <futhark@chromium.org>
Reviewed-by: Morten Stenshorne <mstensho@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1013403}

[modify] https://crrev.com/7dcf0da88c74ed4e34edf9f63df39576519e04b2/third_party/blink/renderer/core/css/style_engine.cc
[modify] https://crrev.com/7dcf0da88c74ed4e34edf9f63df39576519e04b2/third_party/blink/web_tests/TestExpectations
[modify] https://crrev.com/7dcf0da88c74ed4e34edf9f63df39576519e04b2/third_party/blink/renderer/core/dom/element.h
[modify] https://crrev.com/7dcf0da88c74ed4e34edf9f63df39576519e04b2/third_party/blink/renderer/core/html/forms/html_field_set_element.h
[modify] https://crrev.com/7dcf0da88c74ed4e34edf9f63df39576519e04b2/third_party/blink/renderer/core/dom/element.cc
[modify] https://crrev.com/7dcf0da88c74ed4e34edf9f63df39576519e04b2/third_party/blink/renderer/core/css/style_engine.h
[modify] https://crrev.com/7dcf0da88c74ed4e34edf9f63df39576519e04b2/third_party/blink/web_tests/external/wpt/css/css-contain/container-queries/crashtests/columns-in-table-002-crash.html


### fu...@chromium.org (2022-06-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-13)

[Empty comment from Monorail migration]

### am...@google.com (2022-06-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-29)

Congratulations! The VRP Panel has decided to award you $5,000 for this report + $1,000 fuzzer bonus. Thank you for your efforts and nice work! 

### am...@google.com (2022-07-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-12)

RV-SE label clean up based on off-bug discussion with researcher prior that did not occur at the time 

### [Deleted User] (2022-09-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-09-19)

This issue was migrated from crbug.com/chromium/1307656?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/1145970]
[Monorail mergedwith: crbug.com/chromium/1325621]
[Monorail components added to Component Tags custom field.]

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059136)*
