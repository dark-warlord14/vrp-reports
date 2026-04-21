# TypeConfuse in blink::NGLayoutInputNode::IsEmptyTableSection ng_layout_input_node.cc:87

| Field | Value |
|-------|-------|
| **Issue ID** | [40060394](https://issues.chromium.org/issues/40060394) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>CSS |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | fu...@chromium.org |
| **Created** | 2022-07-25 |
| **Bounty** | $7,500.00 |

## Description

**Steps to reproduce the problem:**  

#TestOn  

asan-win32-release\_x64-1027164

#Reproduce

1. chrome --no-sandbox --user-data-dir=test poc.html

**Problem Description:**  

#Type of crash  

render tab

#Analysis  

LayoutTableSection can also pass the conditional test of IsTableSection()[1], resulting in type confusion

```
bool NGLayoutInputNode::IsEmptyTableSection() const {  
  return box_->IsTableSection() &&							<<[1]  
         To<LayoutNGTableSection>(box_.Get())->IsEmpty();  
}  

```

#Patch

```
diff --git a/third_party/blink/renderer/core/layout/ng/ng_layout_input_node.cc b/third_party/blink/renderer/core/layout/ng/ng_layout_input_node.cc  
index 1c770d0..458b9665 100644  
--- a/third_party/blink/renderer/core/layout/ng/ng_layout_input_node.cc  
+++ b/third_party/blink/renderer/core/layout/ng/ng_layout_input_node.cc  
@@ -83,6 +83,10 @@  
 }  
   
 bool NGLayoutInputNode::IsEmptyTableSection() const {  
+  // TODO().  
+  // |LayoutTableSection| is not a subclass of |LayoutNGTableSection|.  
+  CHECK(IsA<LayoutNGTableSection>(box_.Get()));  
+  
   return box_->IsTableSection() &&  
          To<LayoutNGTableSection>(box_.Get())->IsEmpty();  
 }  
  

```

**Additional Comments:**  

#asan  

[0725/121157.497:FATAL:casting.h(126)] Security DCHECK failed: IsA<Derived>(from).  

Backtrace:  

base::debug::CollectStackTrace [0x00007FFDCC0BA3A2+18] (C:\b\s\w\ir\cache\builder\src\base\debug\stack\_trace\_win.cc:329)  

base::debug::StackTrace::StackTrace [0x00007FFDCE96224A+26] (C:\b\s\w\ir\cache\builder\src\base\debug\stack\_trace.cc:218)  

logging::LogMessage::~LogMessage [0x00007FFDCBF2DF06+662] (C:\b\s\w\ir\cache\builder\src\base\logging.cc:671)  

blink::NGLayoutInputNode::IsEmptyTableSection [0x00007FFDD8FF6FE0+592] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_layout\_input\_node.cc:87)  

blink::NGTableAlgorithmUtils::ComputeColumnConstraints [0x00007FFDDB327CDA+2026] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\table\ng\_table\_layout\_algorithm\_utils.cc:595)  

blink::NGTableNode::GetColumnConstraints [0x00007FFDDAD36FCC+764] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\table\ng\_table\_node.cc:41)  

blink::NGTableLayoutAlgorithm::ComputeTableInlineSize [0x00007FFDD8C36C46+1334] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\table\ng\_table\_layout\_algorithm.cc:502)  

blink::NGTableNode::ComputeTableInlineSize [0x00007FFDDAD372B3+19] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\table\ng\_table\_node.cc:51)  

blink::CalculateInitialFragmentGeometry [0x00007FFDD7E73BAC+2732] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_length\_utils.cc:1471)  

blink::NGBlockNode::Layout [0x00007FFDD50B9C05+1381] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_node.cc:458)  

blink::NGBlockLayoutAlgorithm::LayoutNewFormattingContext [0x00007FFDD8CF4916+3478] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:1586)  

blink::NGBlockLayoutAlgorithm::HandleNewFormattingContext [0x00007FFDD8CF11E1+2817] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:1369)  

blink::NGBlockLayoutAlgorithm::Layout [0x00007FFDD8CE31E3+6851] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:719)  

blink::NGBlockLayoutAlgorithm::Layout [0x00007FFDD8CE12D0+288] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:465)  

blink::NGColumnLayoutAlgorithm::CalculateBalancedColumnBlockSizeInternal [0x00007FFDD8CD52C5+1589] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_column\_layout\_algorithm.cc:1238)  

blink::NGColumnLayoutAlgorithm::LayoutRow [0x00007FFDD8CCCDD2+2434] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_column\_layout\_algorithm.cc:662)  

blink::NGColumnLayoutAlgorithm::LayoutChildren [0x00007FFDD8CC7EF7+3127] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_column\_layout\_algorithm.cc:450)  

blink::NGColumnLayoutAlgorithm::Layout [0x00007FFDD8CC6549+1385] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_column\_layout\_algorithm.cc:273)  

blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::NGColumnLayoutAlgorithm,`lambda at ../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:212:28'> [0x00007FFDD50DB2FA+314] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_node.cc:123)  

blink::NGBlockNode::Layout [0x00007FFDD50BA8EA+4682] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_node.cc:531)  

blink::NGBlockLayoutAlgorithm::LayoutNewFormattingContext [0x00007FFDD8CF4916+3478] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:1586)  

blink::NGBlockLayoutAlgorithm::HandleNewFormattingContext [0x00007FFDD8CF11E1+2817] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:1369)  

blink::NGBlockLayoutAlgorithm::Layout [0x00007FFDD8CE31E3+6851] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:719)  

blink::NGBlockLayoutAlgorithm::Layout [0x00007FFDD8CE12D0+288] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:465)  

blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::NGBlockLayoutAlgorithm,`lambda at ../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:212:28'> [0x00007FFDD50DB79E+318] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_node.cc:123)  

blink::NGBlockNode::Layout [0x00007FFDD50BA8EA+4682] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_node.cc:531)  

blink::`anonymous namespace'::LayoutInflow [0x00007FFDD8CFFDAC+972] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:129) blink::NGBlockLayoutAlgorithm::HandleInflow [0x00007FFDD8CFED3C+1996] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:1737) blink::NGBlockLayoutAlgorithm::Layout [0x00007FFDD8CE32A9+7049] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:723) blink::NGBlockLayoutAlgorithm::Layout [0x00007FFDD8CE12D0+288] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:465) blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::NGBlockLayoutAlgorithm,`lambda at ../../third_party/blink/renderer/core/layout/ng/ng_block_node.cc:212:28'> [0x00007FFDD50DB79E+318] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_node.cc:123) blink::NGBlockNode::Layout [0x00007FFDD50BA8EA+4682] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_node.cc:531) blink::LayoutNGMixin<blink::LayoutRubyAsBlock>::UpdateInFlowBlockLayout [0x00007FFDD8050571+993] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\layout_ng_mixin.cc:416) blink::LayoutNGBlockFlowMixin<blink::LayoutProgress>::UpdateNGBlockLayout [0x00007FFDD8091954+68] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\layout_ng_block_flow_mixin.cc:276) blink::LayoutBlock::UpdateLayout [0x00007FFDD44FFFF9+281] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block.cc:442) blink::LayoutBlockFlow::PositionAndLayoutOnceIfNeeded [0x00007FFDD46533D8+1656] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:832) blink::LayoutBlockFlow::LayoutBlockChild [0x00007FFDD46551D2+1522] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:947) blink::LayoutBlockFlow::LayoutBlockChildren [0x00007FFDD464FD3C+1948] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:1644) blink::LayoutBlockFlow::LayoutChildren [0x00007FFDD464A7A5+1237] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:617) blink::LayoutBlockFlow::UpdateBlockLayout [0x00007FFDD464953F+1199] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:478) blink::LayoutView::UpdateBlockLayout [0x00007FFDD10C829D+2109] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_view.cc:336) blink::LayoutBlock::UpdateLayout [0x00007FFDD44FFFF9+281] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block.cc:442) blink::LayoutView::UpdateLayout [0x00007FFDD10C8B03+1523] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_view.cc:377) blink::LocalFrameView::PerformLayout [0x00007FFDD0F5990B+5019] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:856) blink::LocalFrameView::UpdateLayout [0x00007FFDD0F5BF5C+1436] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:920) blink::LocalFrameView::UpdateStyleAndLayoutInternal [0x00007FFDD0F7980A+586] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:3268) blink::LocalFrameView::UpdateStyleAndLayout [0x00007FFDD0F646B1+593] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:3203) blink::LocalFrameView::UpdateStyleAndLayoutIfNeededRecursive [0x00007FFDD0F732A5+501] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:3123) blink::LocalFrameView::RunStyleAndLayoutLifecyclePhases [0x00007FFDD0F6F889+297] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:2566) blink::LocalFrameView::UpdateLifecyclePhasesInternal [0x00007FFDD0F6DE63+1763] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:2389) blink::LocalFrameView::UpdateLifecyclePhases [0x00007FFDD0F6C33C+2252] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:2326) blink::LocalFrameView::UpdateAllLifecyclePhases [0x00007FFDD0F6B8F6+438] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:2084) blink::PageAnimator::UpdateAllLifecyclePhases [0x00007FFDD41AED7C+332] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\page\page_animator.cc:161) blink::WebFrameWidgetImpl::UpdateLifecycle [0x00007FFDD0F26FD8+392] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\web_frame_widget_impl.cc:1360) blink::WidgetBase::UpdateVisualState [0x00007FFDD4353A5A+314] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\widget\widget_base.cc:883) cc::LayerTreeHost::RequestMainFrameUpdate [0x00007FFDCE99E5C7+279] (C:\b\s\w\ir\cache\builder\src\cc\trees\layer_tree_host.cc:376) cc::ProxyMain::BeginMainFrame [0x00007FFDD1AEA2A2+3922] (C:\b\s\w\ir\cache\builder\src\cc\trees\proxy_main.cc:277) base::internal::Invoker<base::internal::BindState<void (cc::ProxyMain::\*)(std::Cr::unique_ptr<cc::BeginMainFrameAndCommitState,std::Cr::default_delete<cc::BeginMainFrameAndCommitState> >),base::WeakPtr<cc::ProxyMain>,std::Cr::unique_ptr<cc::BeginMainFrame [0x00007FFDD5E6E7C6+454] (C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:791) base::TaskAnnotator::RunTaskImpl [0x00007FFDCC020725+917] (C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135) base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl [0x00007FFDCED4BC3A+2666] (C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:428) base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork [0x00007FFDCED4AC95+421] (C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:298) base::MessagePumpDefault::Run [0x00007FFDCED28FBB+491] (C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:39) base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run [0x00007FFDCED4DCB7+1095] (C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:581) base::RunLoop::Run [0x00007FFDCBFBA480+1328] (C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:143) content::RendererMain [0x00007FFDCE80DB9E+2910] (C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:290) content::RunOtherNamedProcessTypeMain [0x00007FFDCBB71510+1313] (C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:720) content::ContentMainRunnerImpl::Run [0x00007FFDCBB7369B+1985] (C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1064) content::RunContentProcess [0x00007FFDCBB6FB73+3710] (C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:406) content::ContentMain [0x00007FFDCBB702A3+403] (C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:434) headless::`anonymous namespace'::RunContentMain [0x00007FFDCBC9A048+930] (C:\b\s\w\ir\cache\builder\src\headless\app\headless\_shell.cc:177)  

headless::RunChildProcessIfNeeded [0x00007FFDCBC999EB+1070] (C:\b\s\w\ir\cache\builder\src\headless\app\headless\_shell.cc:881)  

headless::HeadlessShellMain [0x00007FFDCBC9651F+1280] (C:\b\s\w\ir\cache\builder\src\headless\app\headless\_shell.cc:694)  

ChromeMain [0x00007FFDC0451485+897] (C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:160)  

MainDllLoader::Launch [0x00007FF611E05A0F+2047] (C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:162)  

main [0x00007FF611E02BD1+7011] (C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:395)  

\_\_scrt\_common\_main\_seh [0x00007FF612201580+268] (d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288)  

BaseThreadInitThunk [0x00007FFE3F3E7034+20]  

RtlUserThreadStart [0x00007FFE3F522651+33]  

Task trace:  

Backtrace:  

cc::ProxyImpl::ScheduledActionSendBeginMainFrame [0x00007FFDD5E69A62+2578] (C:\b\s\w\ir\cache\builder\src\cc\trees\proxy\_impl.cc:724)  

mojo::Connector::PostDispatchNextMessageFromPipe [0x00007FFDCC2F2B02+390] (C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:581)  

mojo::SimpleWatcher::Context::Notify [0x00007FFDCC3475A1+891] (C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple\_watcher.cc:102)

\*\*Chrome version: \*\* 103.0.5060.53 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 13.1 KB)
- [patch.diff](attachments/patch.diff) (text/plain, 636 B)
- [poc.html](attachments/poc.html) (text/plain, 1.2 KB)

## Timeline

### cl...@chromium.org (2022-07-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6310015092850688.

### rs...@chromium.org (2022-07-25)

Are you sure this reproduces on 103.0.5060.53 ? I checked 104.0.5112.0 and 103.0.5060.0 ASan builds and it does not reproduce, but it does on 105.0.5176.0.

[Monorail components: Blink>Layout]

### [Deleted User] (2022-07-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-25)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-07-25)

Only check on recent ASAN versions asan-win32-release_x64-1027164


### [Deleted User] (2022-07-25)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ko...@chromium.org (2022-07-25)

Now you're back, assigning the Container Query issue.

If you want layout to crash, |LayoutNGTable::AddChild| has a DCHECK, so we can turn this to CHECK:
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/layout/ng/table/layout_ng_table.cc;l=136?q=LayoutNGTable::AddChild&ss=chromium

or put a workaround in |NGLayoutInputNode::IsEmptyTableSection| as suggested (this might be a good fix anyway,) but this table-tree NG/legacy mixture looks scary.

[Monorail components: -Blink>Layout Blink>CSS]

### ko...@chromium.org (2022-07-25)

[Empty comment from Monorail migration]

### go...@chromium.org (2022-07-25)

+Amy (Security TPM)



### go...@chromium.org (2022-07-25)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-07-26)

futhark is already working on something similar (or possibly the same).

### fu...@chromium.org (2022-07-26)

[Empty comment from Monorail migration]

### fu...@chromium.org (2022-07-28)

https://chromium-review.googlesource.com/c/chromium/src/+/3789987

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


### fu...@chromium.org (2022-07-28)

[Empty comment from Monorail migration]

### fu...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-29)

Merge approved: your change passed merge requirements and is auto-approved for M105. Please go ahead and merge the CL to branch 5195 (refs/branch-heads/5195) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2022-08-01)

Please merge your change to M105 branch before 11:30 AM PDT today so we can take it in for M105 Beta promotion build. Thank you.

Branch details can be found here: https://chromiumdash.appspot.com/branches

### pb...@google.com (2022-08-01)

[Bulk Edit] Your change has been approved for M105 branch(go/chrome-branches),please go ahead and merge the CL to M105 branch manually by 2PM PST today so that they would be part of tomorrow's(Aug-01st-2022) Dev and the same build would be promoted to Beta later this week on Thursday which is our first M105 Beta.

### fu...@chromium.org (2022-08-01)

It has been merged already, but the merge commit[1] comment ended up in https://crbug.com/chromium/1345894 only, for some reason.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/3794217


### fu...@chromium.org (2022-08-01)

Should I adjust the labels manually?


### go...@chromium.org (2022-08-01)

Yes, please. Thank you. 

### fu...@chromium.org (2022-08-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-01)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fu...@chromium.org (2022-08-01)

> 1. Was this issue a regression for the milestone it was found in?
> 2. Is this issue related to a change or feature merged after the latest LTS Milestone?

This regression is behind a flag prior to M105, no need to merge to any prior releases.


### rz...@google.com (2022-08-02)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-03)

Feature enabled on 105

### am...@google.com (2022-08-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-05)

Congratulations! The VRP Panel has decided to award you $7500 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-08-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1346969?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/1145970]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060394)*
