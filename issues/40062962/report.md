# Security: Security DCHECK failed: IsA<Derived>(from) blink::LayoutMultiColumnFlowThread::ComputeSize layout_multi_column_flow_thread.cc:1666

| Field | Value |
|-------|-------|
| **Issue ID** | [40062962](https://issues.chromium.org/issues/40062962) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | tk...@chromium.org |
| **Created** | 2023-02-08 |
| **Bounty** | $7,000.00 |

## Description

**VERSION**  

WIN10 X64  

asan-win32-release\_x64-1102058

**REPRODUCTION CASE**  

chrome --no-sandbox --user-data-dir=test --enable-blink-test-features poc.html

Type of crash: [tab]

Minicase  

Coming soon

RCA  

same as 1412020  

<https://chromium-review.googlesource.com/c/chromium/src/+/4216291>

ASAN  

[3656:7536:0208/063801.211:FATAL:casting.h(115)] Security DCHECK failed: IsA<Derived>(from).  

Backtrace:  

base::debug::CollectStackTrace [0x00007FFCF8A07C32+18] (C:\b\s\w\ir\cache\builder\src\base\debug\stack\_trace\_win.cc:329)  

base::debug::StackTrace::StackTrace [0x00007FFCFB86E68A+26] (C:\b\s\w\ir\cache\builder\src\base\debug\stack\_trace.cc:218)  

logging::LogMessage::~LogMessage [0x00007FFCF8840DEB+747] (C:\b\s\w\ir\cache\builder\src\base\logging.cc:731)  

blink::LayoutMultiColumnFlowThread::ComputeSize [0x00007FFD064E6C09+1929] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_multi\_column\_flow\_thread.cc:1666)  

blink::LayoutMultiColumnFlowThread::Size [0x00007FFD064E6284+404] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_multi\_column\_flow\_thread.cc:1649)  

blink::LayoutBox::ClientHeight [0x00007FFD017EF0AD+285] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_box.cc:1120)  

blink::ComputedStyle::CalculatePointAndTangentOnRay [0x00007FFCFE33F0F2+1586] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\style\computed\_style.cc:1485)  

blink::ComputedStyle::ApplyMotionPathTransform [0x00007FFCFE33E608+1016] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\style\computed\_style.cc:1546)  

blink::ComputedStyle::ApplyTransform [0x00007FFCFE33DDD9+1865] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\style\computed\_style.cc:1409)  

blink::ComputedStyle::ApplyTransform [0x00007FFCFE33D5D9+377] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\style\computed\_style.cc:1351)  

blink::PaintLayer::UpdateTransform [0x00007FFD01A8A2EC+636] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\paint\paint\_layer.cc:333)  

blink::LayoutBox::UpdateAfterLayout [0x00007FFD017F44DC+364] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_box.cc:1295)  

blink::NGBlockNode::CopyFragmentDataToLayoutBox [0x00007FFD02A15BCF+3871] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_node.cc:1425)  

blink::NGBlockNode::FinishLayout [0x00007FFD02A1068E+3246] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_node.cc:973)  

blink::NGBlockNode::Layout [0x00007FFD02A08105+5029] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_node.cc:570)  

blink::NGBlockLayoutAlgorithm::LayoutNewFormattingContext [0x00007FFD07042093+4723] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:1642)  

blink::NGBlockLayoutAlgorithm::HandleNewFormattingContext [0x00007FFD0703E1B5+2965] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:1420)  

blink::NGBlockLayoutAlgorithm::Layout [0x00007FFD0702F77D+7549] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:755)  

blink::NGBlockLayoutAlgorithm::Layout [0x00007FFD0702D625+293] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:466)  

blink::NGColumnLayoutAlgorithm::ResolveColumnAutoBlockSizeInternal [0x00007FFD070207EA+1610] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_column\_layout\_algorithm.cc:1297)  

blink::NGColumnLayoutAlgorithm::LayoutRow [0x00007FFD07016B68+2840] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_column\_layout\_algorithm.cc:689)  

blink::NGColumnLayoutAlgorithm::LayoutChildren [0x00007FFD07010A07+3159] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_column\_layout\_algorithm.cc:453)  

blink::NGColumnLayoutAlgorithm::Layout [0x00007FFD0700EF50+1472] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_column\_layout\_algorithm.cc:275)  

blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::NGColumnLayoutAlgorithm,`lambda at ../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:209:28'> [0x00007FFD02A30459+313] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_node.cc:117)  

blink::NGBlockNode::Layout [0x00007FFD02A0802D+4813] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_node.cc:558)  

blink::NGBlockLayoutAlgorithm::LayoutNewFormattingContext [0x00007FFD07042093+4723] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:1642)  

blink::NGBlockLayoutAlgorithm::HandleNewFormattingContext [0x00007FFD0703E1B5+2965] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:1420)  

blink::NGBlockLayoutAlgorithm::Layout [0x00007FFD0702F77D+7549] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:755)  

blink::NGBlockLayoutAlgorithm::Layout [0x00007FFD0702D625+293] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:466)  

blink::NGColumnLayoutAlgorithm::ResolveColumnAutoBlockSizeInternal [0x00007FFD070207EA+1610] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_column\_layout\_algorithm.cc:1297)  

blink::NGColumnLayoutAlgorithm::LayoutRow [0x00007FFD07016B68+2840] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_column\_layout\_algorithm.cc:689)  

blink::NGColumnLayoutAlgorithm::LayoutChildren [0x00007FFD07010A07+3159] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_column\_layout\_algorithm.cc:453)  

blink::NGColumnLayoutAlgorithm::Layout [0x00007FFD0700EF50+1472] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_column\_layout\_algorithm.cc:275)  

blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::NGColumnLayoutAlgorithm,`lambda at ../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:209:28'> [0x00007FFD02A30459+313] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_node.cc:117)  

blink::NGBlockNode::Layout [0x00007FFD02A0802D+4813] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_node.cc:558)  

blink::NGBlockLayoutAlgorithm::LayoutNewFormattingContext [0x00007FFD07042093+4723] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:1642)  

blink::NGBlockLayoutAlgorithm::HandleNewFormattingContext [0x00007FFD0703E1B5+2965] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:1420)  

blink::NGBlockLayoutAlgorithm::Layout [0x00007FFD0702F77D+7549] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:755)  

blink::NGBlockLayoutAlgorithm::Layout [0x00007FFD0702D625+293] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:466)  

blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::NGBlockLayoutAlgorithm,`lambda at ../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:209:28'> [0x00007FFD02A308F9+313] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_node.cc:117)  

blink::NGBlockNode::Layout [0x00007FFD02A0802D+4813] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_node.cc:558)  

blink::LayoutNGView::UpdateBlockLayout [0x00007FFD0685F1B9+1513] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\layout\_ng\_view.cc:50)  

blink::LayoutBlock::UpdateLayout [0x00007FFD0222B16C+284] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_block.cc:448)  

blink::LayoutView::UpdateLayout [0x00007FFCFE0B642F+1631] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_view.cc:387)  

blink::LocalFrameView::PerformLayout [0x00007FFCFDEF6D28+5784] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:863)  

blink::LocalFrameView::UpdateLayout [0x00007FFCFDEF9C88+1528] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:926)  

blink::LocalFrameView::UpdateStyleAndLayoutInternal [0x00007FFCFDF1E5BC+1052] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:3301)  

blink::LocalFrameView::UpdateStyleAndLayout [0x00007FFCFDF049B5+1077] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:3233)  

blink::LocalFrameView::UpdateStyleAndLayoutIfNeededRecursive [0x00007FFCFDF16698+472] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:3156)  

blink::LocalFrameView::RunStyleAndLayoutLifecyclePhases [0x00007FFCFDF126FD+301] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2620)  

blink::LocalFrameView::UpdateLifecyclePhasesInternal [0x00007FFCFDF108DF+2303] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2399)  

blink::LocalFrameView::UpdateLifecyclePhases [0x00007FFCFDF0E86F+2479] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2332)  

blink::LocalFrameView::UpdateAllLifecyclePhases [0x00007FFCFDF0DCB5+549] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2095)  

blink::PageAnimator::UpdateAllLifecyclePhases [0x00007FFD016731F0+368] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\page\page\_animator.cc:157)  

blink::WebFrameWidgetImpl::UpdateLifecycle [0x00007FFCFDEB91CE+478] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\web\_frame\_widget\_impl.cc:1394)  

blink::WidgetBase::UpdateVisualState [0x00007FFD018DE19C+316] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\widget\_base.cc:884)  

cc::LayerTreeHost::RequestMainFrameUpdate [0x00007FFCFB8B1564+308] (C:\b\s\w\ir\cache\builder\src\cc\trees\layer\_tree\_host.cc:376)  

cc::ProxyMain::BeginMainFrame [0x00007FFCFF1CB08C+5212] (C:\b\s\w\ir\cache\builder\src\cc\trees\proxy\_main.cc:285)  

base::internal::Invoker<base::internal::BindState<void (cc::ProxyMain::\*)(std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState,std::Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >),base::WeakPtr[cc::ProxyMain](javascript:void(0);),std::Cr::unique\_ptr<cc::BeginMainFrame [0x00007FFD0425ACED+477] (C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:970)  

base::TaskAnnotator::RunTaskImpl [0x00007FFCF8966268+936] (C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:165)  

base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl [0x00007FFCFBD1A968+3624] (C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:489)  

base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork [0x00007FFCFBD19484+564] (C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:340)  

base::MessagePumpDefault::Run [0x00007FFCFBCE8034+468] (C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:48)  

base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run [0x00007FFCFBD1D2D8+1128] (C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:649)  

base::RunLoop::Run [0x00007FFCF88E8A92+1490] (C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:142)  

content::RendererMain [0x00007FFCFB5F4AB5+3085] (C:\b\s\w\ir\cache\builder\src\content\renderer\renderer\_main.cc:339)  

content::RunOtherNamedProcessTypeMain [0x00007FFCF716D6EC+1456] (C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:760)  

content::ContentMainRunnerImpl::Run [0x00007FFCF717044D+2731] (C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1122)  

content::RunContentProcess [0x00007FFCF716AF1D+3061] (C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:335)  

content::ContentMain [0x00007FFCF716BE0D+471] (C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:363)  

ChromeMain [0x00007FFCEB67169A+1430] (C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:190)

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 13.2 KB)
- [minipoc.html](attachments/minipoc.html) (text/plain, 225 B)
- [poc2.html](attachments/poc2.html) (text/plain, 1.1 KB)
- [tc.html](attachments/tc.html) (text/plain, 249 B)

## Timeline

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### m....@gmail.com (2023-02-08)

chrome --no-sandbox --user-data-dir=test --enable-blink-test-features minipoc.html

### m....@gmail.com (2023-02-08)

bisect:
https://chromium-review.googlesource.com/c/chromium/src/+/4198602

### ma...@google.com (2023-02-09)

Nice work.

tkent@, could you PTAL at this one as well?

(Same labels as 1412020, but later FoundIn based on https://crbug.com/chromium/1413945#c2.)

[Monorail components: Blink>Layout]

### ma...@google.com (2023-02-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-02-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5193181766549504.

### tk...@chromium.org (2023-02-09)

I couldn't reproduce this locally.

>	blink::LayoutBox::ClientHeight [0x00007FFD017EF0AD+285] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_box.cc:1120)
>	blink::ComputedStyle::CalculatePointAndTangentOnRay [0x00007FFCFE33F0F2+1586] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\style\computed_style.cc:1485)
>	blink::ComputedStyle::ApplyMotionPathTransform [0x00007FFCFE33E608+1016] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\style\computed_style.cc:1546)

This code path was removed by https://chromium-review.googlesource.com/c/chromium/src/+/4234498 


### m....@gmail.com (2023-02-09)

It seems that the original POC can no longer be triggered in the latest version, but I found a POC that can be triggered in the latest version, which will be provided later

### m....@gmail.com (2023-02-09)

It may not be caused by the same bug, because poc2 can be triggered without --enable-blink-test-features, but minipoc needs

TESTON asan-win32-release_x64-1103074
chrome --no-sandbox --user-data-dir=test poc2.html

### ms...@chromium.org (2023-02-09)

#3 0x7fd6f7d33b94 blink::LayoutMultiColumnFlowThread::ComputeSize()
#4 0x7fd6f7d33730 blink::LayoutMultiColumnFlowThread::Size()
#5 0x7fd6f7c5d327 blink::LayoutBox::PhysicalLocationInternal()
#6 0x7fd6f7cae9eb blink::LayoutBox::OffsetFromContainerInternal()
#7 0x7fd6f7d5088c blink::LayoutObject::MapLocalToAncestor()
#8 0x7fd6f7d50ae9 blink::LayoutObject::MapLocalToAncestor()
#9 0x7fd6f7d51de2 blink::LayoutObject::LocalToAncestorQuad()
#10 0x7fd6f8232170 blink::PaintLayerScrollableArea::LocalToVisibleContentQuad()
#11 0x7fd6f800e36e blink::RelativeBounds()
#12 0x7fd6f800dd07 blink::ScrollAnchor::Examine()
#13 0x7fd6f800ecac blink::ScrollAnchor::FindAnchorRecursive()
#14 0x7fd6f800ed84 blink::ScrollAnchor::FindAnchorRecursive()
#15 0x7fd6f800ed84 blink::ScrollAnchor::FindAnchorRecursive()
#16 0x7fd6f800ed84 blink::ScrollAnchor::FindAnchorRecursive()
#17 0x7fd6f800ea36 blink::ScrollAnchor::FindAnchor()
#18 0x7fd6f800fd57 blink::ScrollAnchor::NotifyBeforeLayout()
#19 0x7fd6f7f4f2a0 blink::NGBlockNode::PrepareForLayout()
#20 0x7fd6f7f4d38d blink::NGBlockNode::Layout()
#21 0x7fd6f7f57753 blink::NGBlockNode::LayoutAtomicInline()

I think we should add https://chromium-review.googlesource.com/c/chromium/src/+/4216291/1 , for good measure. The ScrollAnchor machinery walks up the layout tree during layout, which is bad. It probably requires a complete rewrite.

The layout object tree when the DHCECK fails:

LayoutNGView 0x3e1500101c20            	#document
  LayoutNGBlockFlow 0x3e1500101dc8     	HTML
    LayoutNGBlockFlow 0x3e1500101f08   	BODY
      LayoutNGBlockFlow 0x3e15001020f8 	RTC id="id125" class="cs6 cs7 cs25"
*       LayoutMultiColumnFlowThread (anonymous) 0x3e15001022d8
          LayoutNGBlockFlow (anonymous) 0x3e1500102430
            LayoutText 0x3e1500102238  	#text "\n\t\t\">\n\n\n"
        LayoutMultiColumnSet (anonymous) 0x3e1500102518
      LayoutEmbeddedObject 0x3e1500102648	EMBED

The fragment tree from the previously completed layout pass:

.:: LayoutNG Physical Fragment Tree ::.
* Box (out-of-flow-positioned block-flow)(self paint) offset:unplaced size:1569x1073 LayoutNGView #document
    Box (block-flow-root block-flow)(self paint) offset:0,0 size:1569x34 LayoutNGBlockFlow HTML
      Box (block-flow children-inline) offset:8,8 size:1553x18 LayoutNGBlockFlow BODY
        NGPhysicalLineBoxFragment offset:0,0 size:0x18
          Box (atomic-inline block-flow children-inline)(self paint) offset:0,14 size:0x0 LayoutNGBlockFlow RTC id='id125' class='cs6 cs7 cs25'
            NGPhysicalLineBoxFragment offset:0,0 size:0x0
              DEAD LAYOUT OBJECT!

### ms...@chromium.org (2023-02-09)

The simplified attached test crashes like that with --enable-blink-features=LayoutNGNoCopyBack

### [Deleted User] (2023-02-09)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-09)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-09)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tk...@chromium.org (2023-02-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-02-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b02f91847b06461b03d2c65c90645d154bbbf517

commit b02f91847b06461b03d2c65c90645d154bbbf517
Author: Kent Tamura <tkent@chromium.org>
Date: Fri Feb 10 09:05:30 2023

ScrollAnchor: Do not search never-laid-out LayoutObjects for candidates

We had a crash in LayoutMultiColumnFlowThread::ComputeSize() on a box
became a multi-column container dynamically.

- ScrollAnchor doesn't need to search LayoutObject subtrees which are
  not laid out yet.
- LayoutMultiColumnFlowThread::Size() should not call ComputeSize()
  if it has never been laid out.

Either of them is necessary to fix crbug.com/1413945. This CL applies
both because the former improves performance, and we can avoid similar
issues by the latter.

Bug: 1413945
Change-Id: I7c7fceb912239dce70341deb4ad05568ef9ae44f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4234939
Reviewed-by: Morten Stenshorne <mstensho@chromium.org>
Commit-Queue: Morten Stenshorne <mstensho@chromium.org>
Auto-Submit: Kent Tamura <tkent@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1103722}

[modify] https://crrev.com/b02f91847b06461b03d2c65c90645d154bbbf517/third_party/blink/renderer/core/layout/scroll_anchor.cc
[modify] https://crrev.com/b02f91847b06461b03d2c65c90645d154bbbf517/third_party/blink/renderer/core/layout/scroll_anchor_test.cc
[modify] https://crrev.com/b02f91847b06461b03d2c65c90645d154bbbf517/third_party/blink/renderer/core/layout/layout_multi_column_flow_thread.cc


### tk...@chromium.org (2023-02-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-13)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-17)

Congratulations! The VRP Panel has decided to award you $7,000 for this report + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-02-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-25)

Not requesting merge to dev (M112) because latest trunk commit (1103722) appears to be prior to dev branch point (1109224). If this is incorrect, please replace the Merge-NA-112 label with Merge-Request-112. If other changes are required to fix this bug completely, please request a merge if necessary.

Merge approved: your change passed merge requirements and is auto-approved for M112. Please go ahead and merge the CL to branch 5615 (refs/branch-heads/5615) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), govind (iOS), obenedict (ChromeOS), srinivassista (Desktop)

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-01)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tk...@chromium.org (2023-03-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1413945?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062962)*
