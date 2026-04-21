# Security: Security DCHECK failed i < length() in WTF::StringView::operator[]

| Field | Value |
|-------|-------|
| **Issue ID** | [40056413](https://issues.chromium.org/issues/40056413) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Layout>Inline |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ho...@gmail.com |
| **Assignee** | ko...@chromium.org |
| **Created** | 2021-07-03 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

Security DCHECK failed.

**VERSION**  

Chrome Version: 93.0.4557.4 dev (x86\_64)  

Revision: c8c3b3a7d7139425f55fe9aa7147ff6b0ed06c78-refs/branch-heads/4557@{#12}  

Operating System: Ubuntu 20.04.2 LTS, Linux-5.4.0-77-generic-x86\_64-with-glibc2.29

**REPRODUCTION CASE**

Open the attached test case with a chrome or content\_shell binary built with DCHECKs enabled (dcheck\_always\_on = true):

<article lang="CY">
Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
<style>
\\* {
-webkit-text-security: disc;
hyphens: auto;
}
</style>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

Backtrace:

[1146009:1146041:0703/232715.491474:FATAL:string\_view.h(161)] Security DCHECK failed: i < length().  

#0 0x56066db3c1cb in backtrace /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/../sanitizer\_common/sanitizer\_common\_interceptors.inc:4205:13  

#1 0x56067ba637d9 in base::debug::CollectStackTrace(void\*\*, unsigned long) ./../../base/debug/stack\_trace\_posix.cc:845:39  

#2 0x56067b770023 in base::debug::StackTrace::StackTrace(unsigned long) ./../../base/debug/stack\_trace.cc:200:12  

#3 0x56067b770023 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack\_trace.cc:197:28  

#4 0x56067b7cc8a1 in logging::LogMessage::~LogMessage() ./../../base/logging.cc:589:29  

#5 0x5606815e6800 in WTF::StringView::operator[](unsigned int) const ./../../third\_party/blink/renderer/platform/wtf/text/string\_view.h:161:5  

#6 0x56068742ad5f in blink::Hyphenation::ShouldHyphenateWord(WTF::StringView const&) const ./../../third\_party/blink/renderer/platform/text/hyphenation.h:42:66  

#7 0x56068742ad5f in blink::HyphenationMinikin::LastHyphenLocation(WTF::StringView const&, unsigned int) const ./../../third\_party/blink/renderer/platform/text/hyphenation/hyphenation\_minikin.cc:145:45  

#8 0x560686ee3c76 in blink::ShapingLineBreaker::Hyphenate(unsigned int, unsigned int, unsigned int, bool) const ./../../third\_party/blink/renderer/platform/fonts/shaping/shaping\_line\_breaker.cc:115:23  

#9 0x560686ee42d5 in blink::ShapingLineBreaker::Hyphenate(unsigned int, unsigned int, bool) const ./../../third\_party/blink/renderer/platform/fonts/shaping/shaping\_line\_breaker.cc:152:30  

#10 0x560686ee4a45 in blink::ShapingLineBreaker::PreviousBreakOpportunity(unsigned int, unsigned int) const ./../../third\_party/blink/renderer/platform/fonts/shaping/shaping\_line\_breaker.cc:176:12  

#11 0x560686ee5b19 in blink::ShapingLineBreaker::ShapeLine(unsigned int, blink::LayoutUnit, unsigned int, blink::ShapingLineBreaker::Result\*) ./../../third\_party/blink/renderer/platform/fonts/shaping/shaping\_line\_breaker.cc:319:13  

#12 0x56068534f6f0 in blink::NGLineBreaker::BreakText(blink::NGInlineItemResult\*, blink::NGInlineItem const&, blink::ShapeResult const&, blink::LayoutUnit, blink::LayoutUnit, blink::NGLineInfo\*) ./../../third\_party/blink/renderer/core/layout/ng/inline/ng\_line\_breaker.cc:1077:65  

#13 0x56068533c278 in blink::NGLineBreaker::HandleText(blink::NGInlineItem const&, blink::ShapeResult const&, blink::NGLineInfo\*) ./../../third\_party/blink/renderer/core/layout/ng/inline/ng\_line\_breaker.cc:875:9  

#14 0x56068533a882 in blink::NGLineBreaker::BreakLine(blink::NGLineInfo\*) ./../../third\_party/blink/renderer/core/layout/ng/inline/ng\_line\_breaker.cc:587:9  

#15 0x560685339907 in blink::NGLineBreaker::NextLine(blink::NGLineInfo\*) ./../../third\_party/blink/renderer/core/layout/ng/inline/ng\_line\_breaker.cc:522:3  

#16 0x5606852fb919 in blink::NGInlineLayoutAlgorithm::Layout() ./../../third\_party/blink/renderer/core/layout/ng/inline/ng\_inline\_layout\_algorithm.cc:1097:18  

#17 0x5606852a5f77 in blink::NGInlineNode::Layout(blink::NGConstraintSpace const&, blink::NGBreakToken const\*, blink::NGInlineChildLayoutContext\*) const ./../../third\_party/blink/renderer/core/layout/ng/inline/ng\_inline\_node.cc:1520:20  

#18 0x56068545afad in blink::(anonymous namespace)::LayoutInflow(blink::NGConstraintSpace const&, blink::NGBreakToken const\*, blink::NGEarlyBreak const\*, blink::NGLayoutInputNode\*, blink::NGInlineChildLayoutContext\*) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:116:25  

#19 0x56068545a653 in blink::NGBlockLayoutAlgorithm::HandleInflow(blink::NGLayoutInputNode, blink::NGBreakToken const\*, blink::NGPreviousInflowPosition\*, blink::NGInlineChildLayoutContext\*, scoped\_refptr<blink::NGInlineBreakToken const>\*) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:1653:7  

#20 0x56068543c748 in blink::NGBlockLayoutAlgorithm::Layout(blink::NGInlineChildLayoutContext\*) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:692:18  

#21 0x56068543f121 in blink::NGBlockLayoutAlgorithm::LayoutWithItemsBuilder(blink::NGInlineNode const&, blink::NGInlineChildLayoutContext\*) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:473:48  

#22 0x560685439dae in blink::NGBlockLayoutAlgorithm::LayoutWithInlineChildLayoutContext(blink::NGLayoutInputNode const&) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:462:10  

#23 0x5606854395cc in blink::NGBlockLayoutAlgorithm::Layout() ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:437:14  

#24 0x5606854262a9 in blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*)::operator()(blink::NGLayoutAlgorithmOperations\*) const ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:207:50  

#25 0x5606854262a9 in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::NGBlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*)>(blink::NGLayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*) const&) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:116:3  

#26 0x5606854236a0 in void blink::(anonymous namespace)::DetermineAlgorithmAndRun<blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*)>(blink::NGLayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*) const&) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:198:5  

#27 0x560685404741 in blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:205:3  

#28 0x560685404741 in blink::NGBlockNode::Layout(blink::NGConstraintSpace const&, blink::NGBlockBreakToken const\*, blink::NGEarlyBreak const\*) const ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:509:21  

#29 0x56068545afd6 in blink::(anonymous namespace)::LayoutBlockChild(blink::NGConstraintSpace const&, blink::NGBreakToken const\*, blink::NGEarlyBreak const\*, blink::NGBlockNode\*) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:105:16  

#30 0x56068545afd6 in blink::(anonymous namespace)::LayoutInflow(blink::NGConstraintSpace const&, blink::NGBreakToken const\*, blink::NGEarlyBreak const\*, blink::NGLayoutInputNode\*, blink::NGInlineChildLayoutContext\*) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:117:10  

#31 0x56068545a653 in blink::NGBlockLayoutAlgorithm::HandleInflow(blink::NGLayoutInputNode, blink::NGBreakToken const\*, blink::NGPreviousInflowPosition\*, blink::NGInlineChildLayoutContext\*, scoped\_refptr<blink::NGInlineBreakToken const>\*) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:1653:7  

#32 0x56068543c748 in blink::NGBlockLayoutAlgorithm::Layout(blink::NGInlineChildLayoutContext\*) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:692:18  

#33 0x5606854395d9 in blink::NGBlockLayoutAlgorithm::Layout() ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:439:14  

#34 0x5606854262a9 in blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*)::operator()(blink::NGLayoutAlgorithmOperations\*) const ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:207:50  

#35 0x5606854262a9 in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::NGBlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*)>(blink::NGLayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*) const&) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:116:3  

#36 0x5606854236a0 in void blink::(anonymous namespace)::DetermineAlgorithmAndRun<blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*)>(blink::NGLayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*) const&) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:198:5  

#37 0x560685404741 in blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:205:3  

#38 0x560685404741 in blink::NGBlockNode::Layout(blink::NGConstraintSpace const&, blink::NGBlockBreakToken const\*, blink::NGEarlyBreak const\*) const ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:509:21  

#39 0x56068545afd6 in blink::(anonymous namespace)::LayoutBlockChild(blink::NGConstraintSpace const&, blink::NGBreakToken const\*, blink::NGEarlyBreak const\*, blink::NGBlockNode\*) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:105:16  

#40 0x56068545afd6 in blink::(anonymous namespace)::LayoutInflow(blink::NGConstraintSpace const&, blink::NGBreakToken const\*, blink::NGEarlyBreak const\*, blink::NGLayoutInputNode\*, blink::NGInlineChildLayoutContext\*) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:117:10  

#41 0x56068545a653 in blink::NGBlockLayoutAlgorithm::HandleInflow(blink::NGLayoutInputNode, blink::NGBreakToken const\*, blink::NGPreviousInflowPosition\*, blink::NGInlineChildLayoutContext\*, scoped\_refptr<blink::NGInlineBreakToken const>\*) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:1653:7  

#42 0x56068543c748 in blink::NGBlockLayoutAlgorithm::Layout(blink::NGInlineChildLayoutContext\*) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:692:18  

#43 0x5606854395d9 in blink::NGBlockLayoutAlgorithm::Layout() ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:439:14  

#44 0x5606854262a9 in blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*)::operator()(blink::NGLayoutAlgorithmOperations\*) const ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:207:50  

#45 0x5606854262a9 in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::NGBlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*)>(blink::NGLayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*) const&) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:116:3  

#46 0x5606854236a0 in void blink::(anonymous namespace)::DetermineAlgorithmAndRun<blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*)>(blink::NGLayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*) const&) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:198:5  

#47 0x560685404741 in blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:205:3  

#48 0x560685404741 in blink::NGBlockNode::Layout(blink::NGConstraintSpace const&, blink::NGBlockBreakToken const\*, blink::NGEarlyBreak const\*) const ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:509:21  

#49 0x5606853bc0e0 in blink::LayoutNGMixin[blink::LayoutBlockFlow](javascript:void(0);)::UpdateInFlowBlockLayout() ./../../third\_party/blink/renderer/core/layout/ng/layout\_ng\_mixin.cc:403:25  

#50 0x56068538a611 in blink::LayoutNGBlockFlowMixin[blink::LayoutBlockFlow](javascript:void(0);)::UpdateNGBlockLayout() ./../../third\_party/blink/renderer/core/layout/ng/layout\_ng\_block\_flow\_mixin.cc:259:24  

#51 0x560684b8c288 in blink::LayoutBlock::UpdateLayout() ./../../third\_party/blink/renderer/core/layout/layout\_block.cc:431:3  

#52 0x560684bf7296 in blink::LayoutBlockFlow::PositionAndLayoutOnceIfNeeded(blink::LayoutBox&, blink::LayoutUnit, blink::BlockChildrenLayoutInfo&) ./../../third\_party/blink/renderer/core/layout/layout\_block\_flow.cc:830:11  

#53 0x560684bf8c00 in blink::LayoutBlockFlow::LayoutBlockChild(blink::LayoutBox&, blink::BlockChildrenLayoutInfo&) ./../../third\_party/blink/renderer/core/layout/layout\_block\_flow.cc:945:7  

#54 0x560684bf29e2 in blink::LayoutBlockFlow::LayoutBlockChildren(bool, blink::SubtreeLayoutScope&, blink::LayoutUnit, blink::LayoutUnit) ./../../third\_party/blink/renderer/core/layout/layout\_block\_flow.cc:1634:5  

#55 0x560684becde9 in blink::LayoutBlockFlow::LayoutChildren(bool, blink::SubtreeLayoutScope&) ./../../third\_party/blink/renderer/core/layout/layout\_block\_flow.cc:615:5  

#56 0x560684beb8c0 in blink::LayoutBlockFlow::UpdateBlockLayout(bool) ./../../third\_party/blink/renderer/core/layout/layout\_block\_flow.cc:476:5  

#57 0x5606850e530d in blink::LayoutView::UpdateBlockLayout(bool) ./../../third\_party/blink/renderer/core/layout/layout\_view.cc:322:20  

#58 0x560684b8c288 in blink::LayoutBlock::UpdateLayout() ./../../third\_party/blink/renderer/core/layout/layout\_block.cc:431:3  

#59 0x5606850e5ef3 in blink::LayoutView::UpdateLayout() ./../../third\_party/blink/renderer/core/layout/layout\_view.cc:363:20  

#60 0x560684093b1f in blink::LocalFrameView::PerformLayout() ./../../third\_party/blink/renderer/core/frame/local\_frame\_view.cc:835:24  

#61 0x56068409662b in blink::LocalFrameView::UpdateLayout() ./../../third\_party/blink/renderer/core/frame/local\_frame\_view.cc:893:3  

#62 0x5606840c4512 in blink::LocalFrameView::UpdateStyleAndLayoutInternal() ./../../third\_party/blink/renderer/core/frame/local\_frame\_view.cc:3317:5  

#63 0x5606840a1a18 in blink::LocalFrameView::UpdateStyleAndLayout() ./../../third\_party/blink/renderer/core/frame/local\_frame\_view.cc:3258:21  

#64 0x56068357c8ce in blink::Document::UpdateStyleAndLayout(blink::DocumentUpdateReason) ./../../third\_party/blink/renderer/core/dom/document.cc:2430:17  

#65 0x5606835918f9 in blink::Document::ImplicitClose() ./../../third\_party/blink/renderer/core/dom/document.cc:3472:5  

#66 0x560683592084 in blink::Document::CheckCompletedInternal() ./../../third\_party/blink/renderer/core/dom/document.cc:3547:5  

#67 0x5606835c4168 in blink::Document::CheckCompleted() ./../../third\_party/blink/renderer/core/dom/document.cc:3521:7  

#68 0x5606835c4168 in blink::Document::DecrementLoadEventDelayCountAndCheckLoadEvent() ./../../third\_party/blink/renderer/core/dom/document.cc:7137:5  

#69 0x5606838cf12e in blink::IncrementLoadEventDelayCount::ClearAndCheckLoadEvent() ./../../third\_party/blink/renderer/core/dom/increment\_load\_event\_delay\_count.cc:26:16  

#70 0x5606846f6c66 in blink::HTMLStyleElement::DispatchPendingEvent(std::\_\_1::unique\_ptr<blink::IncrementLoadEventDelayCount, std::\_\_1::default\_delete[blink::IncrementLoadEventDelayCount](javascript:void(0);) >, bool) ./../../third\_party/blink/renderer/core/html/html\_style\_element.cc:116:10  

#71 0x56067734a82d in base::OnceCallback<void ()>::Run() && ./../../base/callback.h:98:12  

#72 0x56067734a82d in WTF::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>::RunInternal(base::OnceCallback<void ()>\*) ./../../third\_party/blink/renderer/platform/wtf/functional.h:225:33  

#73 0x56067734a82d in WTF::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>::Run() ./../../third\_party/blink/renderer/platform/wtf/functional.h:210:12  

#74 0x56067b916e20 in base::OnceCallback<void ()>::Run() && ./../../base/callback.h:98:12  

#75 0x56067b916e20 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) ./../../base/task/common/task\_annotator.cc:178:33  

#76 0x56067b9768d3 in base::sequence\_manager::internal::ThreadControllerImpl::DoWork(base::sequence\_manager::internal::ThreadControllerImpl::WorkType) ./../../base/task/sequence\_manager/thread\_controller\_impl.cc:199:25  

#77 0x56067b97aec8 in void base::internal::FunctorTraits<void (base::sequence\_manager::internal::ThreadControllerImpl::\*)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), void>::Invoke<void (base::sequence\_manager::internal::ThreadControllerImpl::\*)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), base::WeakPtr[base::sequence\_manager::internal::ThreadControllerImpl](javascript:void(0);) const&, base::sequence\_manager::internal::ThreadControllerImpl::WorkType const&>(void (base::sequence\_manager::internal::ThreadControllerImpl::\*)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), base::WeakPtr[base::sequence\_manager::internal::ThreadControllerImpl](javascript:void(0);) const&, base::sequence\_manager::internal::ThreadControllerImpl::WorkType const&) ./../../base/bind\_internal.h:509:12  

#78 0x56067b97aec8 in void base::internal::InvokeHelper<true, void>::MakeItSo<void (base::sequence\_manager::internal::ThreadControllerImpl::\* const&)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), base::WeakPtr[base::sequence\_manager::internal::ThreadControllerImpl](javascript:void(0);) const&, base::sequence\_manager::internal::ThreadControllerImpl::WorkType const&>(void (base::sequence\_manager::internal::ThreadControllerImpl::\* const&)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), base::WeakPtr[base::sequence\_manager::internal::ThreadControllerImpl](javascript:void(0);) const&, base::sequence\_manager::internal::ThreadControllerImpl::WorkType const&) ./../../base/bind\_internal.h:668:5  

#79 0x56067b97aec8 in void base::internal::Invoker<base::internal::BindState<void (base::sequence\_manager::internal::ThreadControllerImpl::\*)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), base::WeakPtr[base::sequence\_manager::internal::ThreadControllerImpl](javascript:void(0);), base::sequence\_manager::internal::ThreadControllerImpl::WorkType>, void ()>::RunImpl<void (base::sequence\_manager::internal::ThreadControllerImpl::\* const&)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), std::\_\_1::tuple<base::WeakPtr[base::sequence\_manager::internal::ThreadControllerImpl](javascript:void(0);), base::sequence\_manager::internal::ThreadControllerImpl::WorkType> const&, 0ul, 1ul>(void (base::sequence\_manager::internal::ThreadControllerImpl::\* const&)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), std::\_\_1::tuple<base::WeakPtr[base::sequence\_manager::internal::ThreadControllerImpl](javascript:void(0);), base::sequence\_manager::internal::ThreadControllerImpl::WorkType> const&, std::\_\_1::integer\_sequence<unsigned long, 0ul, 1ul>) ./../../base/bind\_internal.h:721:12  

#80 0x56067b97aec8 in base::internal::Invoker<base::internal::BindState<void (base::sequence\_manager::internal::ThreadControllerImpl::\*)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), base::WeakPtr[base::sequence\_manager::internal::ThreadControllerImpl](javascript:void(0);), base::sequence\_manager::internal::ThreadControllerImpl::WorkType>, void ()>::Run(base::internal::BindStateBase\*) ./../../base/bind\_internal.h:703:12  

#81 0x56067b916e20 in base::OnceCallback<void ()>::Run() && ./../../base/callback.h:98:12  

#82 0x56067b916e20 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) ./../../base/task/common/task\_annotator.cc:178:33  

#83 0x56067b98304f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:360:23  

#84 0x56067b981c29 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:260:36  

#85 0x56067b983f62 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#86 0x56067b7ee88d in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_default.cc:39:55  

#87 0x56067b984d4f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:467:12  

#88 0x56067b896d99 in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:134:14  

#89 0x56067ba0b4aa in base::Thread::Run(base::RunLoop\*) ./../../base/threading/thread.cc:325:13  

#90 0x56067ba0bf8a in base::Thread::ThreadMain() ./../../base/threading/thread.cc:396:3  

#91 0x56067bab0b75 in base::(anonymous namespace)::ThreadFunc(void\*) ./../../base/threading/platform\_thread\_posix.cc:96:13  

#92 0x7f42d9f1f609 in start\_thread /build/glibc-eX1tMB/glibc-2.31/nptl/pthread\_create.c:477:8  

#93 0x7f42d80d3293 in clone /build/glibc-eX1tMB/glibc-2.31/misc/../sysdeps/unix/sysv/linux/x86\_64/clone.S:95:0  

Task trace:  

#0 0x5606846f6677 in blink::HTMLStyleElement::NotifyLoadedSheetAndAllCriticalSubresources(blink::Node::LoadedSheetErrorStatus) ./../../third\_party/blink/renderer/core/html/html\_style\_element.cc:131:11  

#1 0x560687820740 in blink::HTMLParserScheduler::ScheduleForUnpause() ./../../third\_party/blink/renderer/core/html/parser/html\_parser\_scheduler.cc:64:50  

#2 0x5606877ab1b2 in blink::HTMLDocumentParser::AppendBytes(char const\*, unsigned long) ./../../third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:1743:9  

#3 0x56067cfcdcf6 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::Accept(mojo::Message\*) ./../../ipc/ipc\_mojo\_bootstrap.cc:938:13  

#4 0x56067c580c1b in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) ./../../mojo/public/cpp/system/simple\_watcher.cc:100:13  

Task trace buffer limit hit, update PendingTask::kTaskBacktraceLength to increase.

Received signal 6  

#0 0x56066db3c1cb in backtrace /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/../sanitizer\_common/sanitizer\_common\_interceptors.inc:4205:13  

#1 0x56067ba637d9 in base::debug::CollectStackTrace(void\*\*, unsigned long) ./../../base/debug/stack\_trace\_posix.cc:845:39  

#2 0x56067b770023 in base::debug::StackTrace::StackTrace(unsigned long) ./../../base/debug/stack\_trace.cc:200:12  

#3 0x56067b770023 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack\_trace.cc:197:28  

#4 0x56067ba621db in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo\_t\*, void\*) ./../../base/debug/stack\_trace\_posix.cc:346:3  

#5 0x7f42d9f2b3c0 in \_\_funlockfile :?  

#6 0x7f42d7ff718b in \_\_libc\_signal\_restore\_set /build/glibc-eX1tMB/glibc-2.31/signal/../sysdeps/unix/sysv/linux/internal-signals.h:86:3  

#7 0x7f42d7ff718b in raise /build/glibc-eX1tMB/glibc-2.31/signal/../sysdeps/unix/sysv/linux/raise.c:48:3  

#8 0x7f42d7fd6859 in abort /build/glibc-eX1tMB/glibc-2.31/stdlib/abort.c:79:7  

#9 0x56067ba5ff6a in base::debug::BreakDebugger() ./../../base/debug/debugger\_posix.cc:326:3  

#10 0x56067b7cd24a in logging::LogMessage::~LogMessage() ./../../base/logging.cc:891:7  

#11 0x5606815e6800 in WTF::StringView::operator[](unsigned int) const ./../../third\_party/blink/renderer/platform/wtf/text/string\_view.h:161:5  

#12 0x56068742ad5f in blink::Hyphenation::ShouldHyphenateWord(WTF::StringView const&) const ./../../third\_party/blink/renderer/platform/text/hyphenation.h:42:66  

#13 0x56068742ad5f in blink::HyphenationMinikin::LastHyphenLocation(WTF::StringView const&, unsigned int) const ./../../third\_party/blink/renderer/platform/text/hyphenation/hyphenation\_minikin.cc:145:45  

#14 0x560686ee3c76 in blink::ShapingLineBreaker::Hyphenate(unsigned int, unsigned int, unsigned int, bool) const ./../../third\_party/blink/renderer/platform/fonts/shaping/shaping\_line\_breaker.cc:115:23  

#15 0x560686ee42d5 in blink::ShapingLineBreaker::Hyphenate(unsigned int, unsigned int, bool) const ./../../third\_party/blink/renderer/platform/fonts/shaping/shaping\_line\_breaker.cc:152:30  

#16 0x560686ee4a45 in blink::ShapingLineBreaker::PreviousBreakOpportunity(unsigned int, unsigned int) const ./../../third\_party/blink/renderer/platform/fonts/shaping/shaping\_line\_breaker.cc:176:12  

#17 0x560686ee5b19 in blink::ShapingLineBreaker::ShapeLine(unsigned int, blink::LayoutUnit, unsigned int, blink::ShapingLineBreaker::Result\*) ./../../third\_party/blink/renderer/platform/fonts/shaping/shaping\_line\_breaker.cc:319:13  

#18 0x56068534f6f0 in blink::NGLineBreaker::BreakText(blink::NGInlineItemResult\*, blink::NGInlineItem const&, blink::ShapeResult const&, blink::LayoutUnit, blink::LayoutUnit, blink::NGLineInfo\*) ./../../third\_party/blink/renderer/core/layout/ng/inline/ng\_line\_breaker.cc:1077:65  

#19 0x56068533c278 in blink::NGLineBreaker::HandleText(blink::NGInlineItem const&, blink::ShapeResult const&, blink::NGLineInfo\*) ./../../third\_party/blink/renderer/core/layout/ng/inline/ng\_line\_breaker.cc:875:9  

#20 0x56068533a882 in blink::NGLineBreaker::BreakLine(blink::NGLineInfo\*) ./../../third\_party/blink/renderer/core/layout/ng/inline/ng\_line\_breaker.cc:587:9  

#21 0x560685339907 in blink::NGLineBreaker::NextLine(blink::NGLineInfo\*) ./../../third\_party/blink/renderer/core/layout/ng/inline/ng\_line\_breaker.cc:522:3  

#22 0x5606852fb919 in blink::NGInlineLayoutAlgorithm::Layout() ./../../third\_party/blink/renderer/core/layout/ng/inline/ng\_inline\_layout\_algorithm.cc:1097:18  

#23 0x5606852a5f77 in blink::NGInlineNode::Layout(blink::NGConstraintSpace const&, blink::NGBreakToken const\*, blink::NGInlineChildLayoutContext\*) const ./../../third\_party/blink/renderer/core/layout/ng/inline/ng\_inline\_node.cc:1520:20  

#24 0x56068545afad in blink::(anonymous namespace)::LayoutInflow(blink::NGConstraintSpace const&, blink::NGBreakToken const\*, blink::NGEarlyBreak const\*, blink::NGLayoutInputNode\*, blink::NGInlineChildLayoutContext\*) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:116:25  

#25 0x56068545a653 in blink::NGBlockLayoutAlgorithm::HandleInflow(blink::NGLayoutInputNode, blink::NGBreakToken const\*, blink::NGPreviousInflowPosition\*, blink::NGInlineChildLayoutContext\*, scoped\_refptr<blink::NGInlineBreakToken const>\*) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:1653:7  

#26 0x56068543c748 in blink::NGBlockLayoutAlgorithm::Layout(blink::NGInlineChildLayoutContext\*) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:692:18  

#27 0x56068543f121 in blink::NGBlockLayoutAlgorithm::LayoutWithItemsBuilder(blink::NGInlineNode const&, blink::NGInlineChildLayoutContext\*) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:473:48  

#28 0x560685439dae in blink::NGBlockLayoutAlgorithm::LayoutWithInlineChildLayoutContext(blink::NGLayoutInputNode const&) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:462:10  

#29 0x5606854395cc in blink::NGBlockLayoutAlgorithm::Layout() ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:437:14  

#30 0x5606854262a9 in blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*)::operator()(blink::NGLayoutAlgorithmOperations\*) const ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:207:50  

#31 0x5606854262a9 in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::NGBlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*)>(blink::NGLayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*) const&) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:116:3  

#32 0x5606854236a0 in void blink::(anonymous namespace)::DetermineAlgorithmAndRun<blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*)>(blink::NGLayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*) const&) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:198:5  

#33 0x560685404741 in blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:205:3  

#34 0x560685404741 in blink::NGBlockNode::Layout(blink::NGConstraintSpace const&, blink::NGBlockBreakToken const\*, blink::NGEarlyBreak const\*) const ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:509:21  

#35 0x56068545afd6 in blink::(anonymous namespace)::LayoutBlockChild(blink::NGConstraintSpace const&, blink::NGBreakToken const\*, blink::NGEarlyBreak const\*, blink::NGBlockNode\*) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:105:16  

#36 0x56068545afd6 in blink::(anonymous namespace)::LayoutInflow(blink::NGConstraintSpace const&, blink::NGBreakToken const\*, blink::NGEarlyBreak const\*, blink::NGLayoutInputNode\*, blink::NGInlineChildLayoutContext\*) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:117:10  

#37 0x56068545a653 in blink::NGBlockLayoutAlgorithm::HandleInflow(blink::NGLayoutInputNode, blink::NGBreakToken const\*, blink::NGPreviousInflowPosition\*, blink::NGInlineChildLayoutContext\*, scoped\_refptr<blink::NGInlineBreakToken const>\*) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:1653:7  

#38 0x56068543c748 in blink::NGBlockLayoutAlgorithm::Layout(blink::NGInlineChildLayoutContext\*) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:692:18  

#39 0x5606854395d9 in blink::NGBlockLayoutAlgorithm::Layout() ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:439:14  

#40 0x5606854262a9 in blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*)::operator()(blink::NGLayoutAlgorithmOperations\*) const ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:207:50  

#41 0x5606854262a9 in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::NGBlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*)>(blink::NGLayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*) const&) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:116:3  

#42 0x5606854236a0 in void blink::(anonymous namespace)::DetermineAlgorithmAndRun<blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*)>(blink::NGLayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*) const&) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:198:5  

#43 0x560685404741 in blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:205:3  

#44 0x560685404741 in blink::NGBlockNode::Layout(blink::NGConstraintSpace const&, blink::NGBlockBreakToken const\*, blink::NGEarlyBreak const\*) const ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:509:21  

#45 0x56068545afd6 in blink::(anonymous namespace)::LayoutBlockChild(blink::NGConstraintSpace const&, blink::NGBreakToken const\*, blink::NGEarlyBreak const\*, blink::NGBlockNode\*) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:105:16  

#46 0x56068545afd6 in blink::(anonymous namespace)::LayoutInflow(blink::NGConstraintSpace const&, blink::NGBreakToken const\*, blink::NGEarlyBreak const\*, blink::NGLayoutInputNode\*, blink::NGInlineChildLayoutContext\*) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:117:10  

#47 0x56068545a653 in blink::NGBlockLayoutAlgorithm::HandleInflow(blink::NGLayoutInputNode, blink::NGBreakToken const\*, blink::NGPreviousInflowPosition\*, blink::NGInlineChildLayoutContext\*, scoped\_refptr<blink::NGInlineBreakToken const>\*) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:1653:7  

#48 0x56068543c748 in blink::NGBlockLayoutAlgorithm::Layout(blink::NGInlineChildLayoutContext\*) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:692:18  

#49 0x5606854395d9 in blink::NGBlockLayoutAlgorithm::Layout() ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:439:14  

#50 0x5606854262a9 in blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*)::operator()(blink::NGLayoutAlgorithmOperations\*) const ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:207:50  

#51 0x5606854262a9 in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::NGBlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*)>(blink::NGLayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*) const&) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:116:3  

#52 0x5606854236a0 in void blink::(anonymous namespace)::DetermineAlgorithmAndRun<blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*)>(blink::NGLayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*) const&) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:198:5  

#53 0x560685404741 in blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&) ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:205:3  

#54 0x560685404741 in blink::NGBlockNode::Layout(blink::NGConstraintSpace const&, blink::NGBlockBreakToken const\*, blink::NGEarlyBreak const\*) const ./../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:509:21  

#55 0x5606853bc0e0 in blink::LayoutNGMixin[blink::LayoutBlockFlow](javascript:void(0);)::UpdateInFlowBlockLayout() ./../../third\_party/blink/renderer/core/layout/ng/layout\_ng\_mixin.cc:403:25  

#56 0x56068538a611 in blink::LayoutNGBlockFlowMixin[blink::LayoutBlockFlow](javascript:void(0);)::UpdateNGBlockLayout() ./../../third\_party/blink/renderer/core/layout/ng/layout\_ng\_block\_flow\_mixin.cc:259:24  

#57 0x560684b8c288 in blink::LayoutBlock::UpdateLayout() ./../../third\_party/blink/renderer/core/layout/layout\_block.cc:431:3  

#58 0x560684bf7296 in blink::LayoutBlockFlow::PositionAndLayoutOnceIfNeeded(blink::LayoutBox&, blink::LayoutUnit, blink::BlockChildrenLayoutInfo&) ./../../third\_party/blink/renderer/core/layout/layout\_block\_flow.cc:830:11  

#59 0x560684bf8c00 in blink::LayoutBlockFlow::LayoutBlockChild(blink::LayoutBox&, blink::BlockChildrenLayoutInfo&) ./../../third\_party/blink/renderer/core/layout/layout\_block\_flow.cc:945:7  

#60 0x560684bf29e2 in blink::LayoutBlockFlow::LayoutBlockChildren(bool, blink::SubtreeLayoutScope&, blink::LayoutUnit, blink::LayoutUnit) ./../../third\_party/blink/renderer/core/layout/layout\_block\_flow.cc:1634:5  

#61 0x560684becde9 in blink::LayoutBlockFlow::LayoutChildren(bool, blink::SubtreeLayoutScope&) ./../../third\_party/blink/renderer/core/layout/layout\_block\_flow.cc:615:5  

#62 0x560684beb8c0 in blink::LayoutBlockFlow::UpdateBlockLayout(bool) ./../../third\_party/blink/renderer/core/layout/layout\_block\_flow.cc:476:5  

#63 0x5606850e530d in blink::LayoutView::UpdateBlockLayout(bool) ./../../third\_party/blink/renderer/core/layout/layout\_view.cc:322:20  

#64 0x560684b8c288 in blink::LayoutBlock::UpdateLayout() ./../../third\_party/blink/renderer/core/layout/layout\_block.cc:431:3  

#65 0x5606850e5ef3 in blink::LayoutView::UpdateLayout() ./../../third\_party/blink/renderer/core/layout/layout\_view.cc:363:20  

#66 0x560684093b1f in blink::LocalFrameView::PerformLayout() ./../../third\_party/blink/renderer/core/frame/local\_frame\_view.cc:835:24  

#67 0x56068409662b in blink::LocalFrameView::UpdateLayout() ./../../third\_party/blink/renderer/core/frame/local\_frame\_view.cc:893:3  

#68 0x5606840c4512 in blink::LocalFrameView::UpdateStyleAndLayoutInternal() ./../../third\_party/blink/renderer/core/frame/local\_frame\_view.cc:3317:5  

#69 0x5606840a1a18 in blink::LocalFrameView::UpdateStyleAndLayout() ./../../third\_party/blink/renderer/core/frame/local\_frame\_view.cc:3258:21  

#70 0x56068357c8ce in blink::Document::UpdateStyleAndLayout(blink::DocumentUpdateReason) ./../../third\_party/blink/renderer/core/dom/document.cc:2430:17  

#71 0x5606835918f9 in blink::Document::ImplicitClose() ./../../third\_party/blink/renderer/core/dom/document.cc:3472:5  

#72 0x560683592084 in blink::Document::CheckCompletedInternal() ./../../third\_party/blink/renderer/core/dom/document.cc:3547:5  

#73 0x5606835c4168 in blink::Document::CheckCompleted() ./../../third\_party/blink/renderer/core/dom/document.cc:3521:7  

#74 0x5606835c4168 in blink::Document::DecrementLoadEventDelayCountAndCheckLoadEvent() ./../../third\_party/blink/renderer/core/dom/document.cc:7137:5  

#75 0x5606838cf12e in blink::IncrementLoadEventDelayCount::ClearAndCheckLoadEvent() ./../../third\_party/blink/renderer/core/dom/increment\_load\_event\_delay\_count.cc:26:16  

#76 0x5606846f6c66 in blink::HTMLStyleElement::DispatchPendingEvent(std::\_\_1::unique\_ptr<blink::IncrementLoadEventDelayCount, std::\_\_1::default\_delete[blink::IncrementLoadEventDelayCount](javascript:void(0);) >, bool) ./../../third\_party/blink/renderer/core/html/html\_style\_element.cc:116:10  

#77 0x56067734a82d in base::OnceCallback<void ()>::Run() && ./../../base/callback.h:98:12  

#78 0x56067734a82d in WTF::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>::RunInternal(base::OnceCallback<void ()>\*) ./../../third\_party/blink/renderer/platform/wtf/functional.h:225:33  

#79 0x56067734a82d in WTF::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>::Run() ./../../third\_party/blink/renderer/platform/wtf/functional.h:210:12  

#80 0x56067b916e20 in base::OnceCallback<void ()>::Run() && ./../../base/callback.h:98:12  

#81 0x56067b916e20 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) ./../../base/task/common/task\_annotator.cc:178:33  

#82 0x56067b9768d3 in base::sequence\_manager::internal::ThreadControllerImpl::DoWork(base::sequence\_manager::internal::ThreadControllerImpl::WorkType) ./../../base/task/sequence\_manager/thread\_controller\_impl.cc:199:25  

#83 0x56067b97aec8 in void base::internal::FunctorTraits<void (base::sequence\_manager::internal::ThreadControllerImpl::\*)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), void>::Invoke<void (base::sequence\_manager::internal::ThreadControllerImpl::\*)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), base::WeakPtr[base::sequence\_manager::internal::ThreadControllerImpl](javascript:void(0);) const&, base::sequence\_manager::internal::ThreadControllerImpl::WorkType const&>(void (base::sequence\_manager::internal::ThreadControllerImpl::\*)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), base::WeakPtr[base::sequence\_manager::internal::ThreadControllerImpl](javascript:void(0);) const&, base::sequence\_manager::internal::ThreadControllerImpl::WorkType const&) ./../../base/bind\_internal.h:509:12  

#84 0x56067b97aec8 in void base::internal::InvokeHelper<true, void>::MakeItSo<void (base::sequence\_manager::internal::ThreadControllerImpl::\* const&)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), base::WeakPtr[base::sequence\_manager::internal::ThreadControllerImpl](javascript:void(0);) const&, base::sequence\_manager::internal::ThreadControllerImpl::WorkType const&>(void (base::sequence\_manager::internal::ThreadControllerImpl::\* const&)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), base::WeakPtr[base::sequence\_manager::internal::ThreadControllerImpl](javascript:void(0);) const&, base::sequence\_manager::internal::ThreadControllerImpl::WorkType const&) ./../../base/bind\_internal.h:668:5  

#85 0x56067b97aec8 in void base::internal::Invoker<base::internal::BindState<void (base::sequence\_manager::internal::ThreadControllerImpl::\*)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), base::WeakPtr[base::sequence\_manager::internal::ThreadControllerImpl](javascript:void(0);), base::sequence\_manager::internal::ThreadControllerImpl::WorkType>, void ()>::RunImpl<void (base::sequence\_manager::internal::ThreadControllerImpl::\* const&)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), std::\_\_1::tuple<base::WeakPtr[base::sequence\_manager::internal::ThreadControllerImpl](javascript:void(0);), base::sequence\_manager::internal::ThreadControllerImpl::WorkType> const&, 0ul, 1ul>(void (base::sequence\_manager::internal::ThreadControllerImpl::\* const&)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), std::\_\_1::tuple<base::WeakPtr[base::sequence\_manager::internal::ThreadControllerImpl](javascript:void(0);), base::sequence\_manager::internal::ThreadControllerImpl::WorkType> const&, std::\_\_1::integer\_sequence<unsigned long, 0ul, 1ul>) ./../../base/bind\_internal.h:721:12  

#86 0x56067b97aec8 in base::internal::Invoker<base::internal::BindState<void (base::sequence\_manager::internal::ThreadControllerImpl::\*)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), base::WeakPtr[base::sequence\_manager::internal::ThreadControllerImpl](javascript:void(0);), base::sequence\_manager::internal::ThreadControllerImpl::WorkType>, void ()>::Run(base::internal::BindStateBase\*) ./../../base/bind\_internal.h:703:12  

#87 0x56067b916e20 in base::OnceCallback<void ()>::Run() && ./../../base/callback.h:98:12  

#88 0x56067b916e20 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) ./../../base/task/common/task\_annotator.cc:178:33  

#89 0x56067b98304f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:360:23  

#90 0x56067b981c29 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:260:36  

#91 0x56067b983f62 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#92 0x56067b7ee88d in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_default.cc:39:55  

#93 0x56067b984d4f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:467:12  

#94 0x56067b896d99 in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:134:14  

#95 0x56067ba0b4aa in base::Thread::Run(base::RunLoop\*) ./../../base/threading/thread.cc:325:13  

#96 0x56067ba0bf8a in base::Thread::ThreadMain() ./../../base/threading/thread.cc:396:3  

#97 0x56067bab0b75 in base::(anonymous namespace)::ThreadFunc(void\*) ./../../base/threading/platform\_thread\_posix.cc:96:13  

#98 0x7f42d9f1f609 in start\_thread /build/glibc-eX1tMB/glibc-2.31/nptl/pthread\_create.c:477:8  

#99 0x7f42d80d3293 in clone /build/glibc-eX1tMB/glibc-2.31/misc/../sysdeps/unix/sysv/linux/x86\_64/clone.S:95:0  

r8: 0000000000000000 r9: 00007f42a60fa220 r10: 0000000000000008 r11: 0000000000000246  

r12: 00000fe8d4ab7200 r13: 00000fe854abf44c r14: 00007f42a55fa250 r15: 00007f42a55fa2d0  

di: 0000000000000002 si: 00007f42a60fa220 bp: 00007f42a60fa470 bx: 00007f42a60ff700  

dx: 0000000000000000 ax: 0000000000000000 cx: 00007f42d7ff718b sp: 00007f42a60fa220  

ip: 00007f42d7ff718b efl: 0000000000000246 cgf: 002b000000000033 erf: 0000000000000000  

trp: 0000000000000000 msk: 0000000000000000 cr2: 0000000000000000  

[end of stack trace]

**CREDIT INFORMATION**  

Reporter credit: Renata Hodovan  

Fuzzing engine: Grammarinator

## Attachments

- [test.html](attachments/test.html) (text/plain, 324 B)

## Timeline

### [Deleted User] (2021-07-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-07-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5110293741764608.

### rs...@chromium.org (2021-07-08)

I can’t reproduce this, nor can Clusterfuzz. Does this reproduce consistently for you? Have you tried on the latest revision?

### ho...@gmail.com (2021-07-08)

@rsesek: I can consistently reproduce this on the latest dev release both with the content_shell and chrome binaries. Now I downloaded an asan debug nightly build from commondatastorage and I can consistently reproduce the failure with the chrome binary, but not with content_shell.

commondatastorage link: https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-debug%2Fasan-linux-debug-899507.zip?generation=1625749006341496&alt=media

Nightly version:
Chromium	93.0.4570.0 (Developer Build) (64-bit)
Revision	1c9da01761726df5a7915407cee82d043ce5c731-refs/heads/master@{#899507}


### rs...@chromium.org (2021-07-08)

Thanks, I was able to reproduce this using asan-linux-debug-899635.

I think this is Sev-Medium because it is at most a 4 byte overread in the first code point of the string: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/text/hyphenation.h;l=42;drc=152b45f49f0a3f53645c3b56036dcf188187cb55

[Monorail components: Blink>Layout]

### [Deleted User] (2021-07-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-07-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0486da85d5253a8b6fa7cb46e408f055bd0910d7

commit 0486da85d5253a8b6fa7cb46e408f055bd0910d7
Author: Koji Ishii <kojii@chromium.org>
Date: Fri Jul 09 08:38:29 2021

Fix ShouldHyphenateWord not to check empty string

|ShouldHyphenateWord| started checking if the first letter is
not uppercase since r895487 <crrev.com/c/2982497>. This patch
fixes the logic not to hyphenate empty strings.

The line breaker does not ask hyphenation points of empty
strings, but when |WordToHyphenate| strips non-letters,
|ShouldHyphenateWord| may see empty strings.

Bug: 1226323
Change-Id: If485ebb4090ad29fe85af7625c8d2a7196783589
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3017631
Commit-Queue: Koji Ishii <kojii@chromium.org>
Commit-Queue: Kent Tamura <tkent@chromium.org>
Auto-Submit: Koji Ishii <kojii@chromium.org>
Reviewed-by: Kent Tamura <tkent@chromium.org>
Cr-Commit-Position: refs/heads/master@{#899920}

[modify] https://crrev.com/0486da85d5253a8b6fa7cb46e408f055bd0910d7/third_party/blink/renderer/platform/text/hyphenation.h
[modify] https://crrev.com/0486da85d5253a8b6fa7cb46e408f055bd0910d7/third_party/blink/renderer/platform/text/hyphenation_test.cc


### ko...@chromium.org (2021-07-09)

[Empty comment from Monorail migration]

[Monorail components: -Blink>Layout Blink>Layout>Inline]

### rs...@chromium.org (2021-07-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-09)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and Security_Impact labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues Impact guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-07-09)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-07-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-10)

Setting milestone and target because of Security_Impact=Head and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-07-10)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-07-10)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-07-22)

Congratulations! The VRP Panel has decided to award you $2,000 for this report. Nice work! 

### am...@google.com (2021-07-23)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-24)

Not requesting merge to dev (M93) because latest trunk commit (899920) appears to be prior to dev branch point (902210). If this is incorrect, please replace the Merge-na label with Merge-Request-93. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1226323?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056413)*
