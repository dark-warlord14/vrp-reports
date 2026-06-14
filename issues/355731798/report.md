# Heap-Buffer-Overflow on Blink Renderer leads to Segmentation Fault

| Field | Value |
|-------|-------|
| **Issue ID** | [355731798](https://issues.chromium.org/issues/355731798) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Fonts |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ta...@gmail.com |
| **Assignee** | ko...@chromium.org |
| **Created** | 2024-07-27 |
| **Bounty** | $7,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

VULNERABILITY DETAILS

## Bug Type

Heap-Buffer-Overflow on Blink Renderer leads to Segmentation Fault: Received signal 11 SEGV\_ACCERR 36a0002be000

## Version Tests

Chromium 127.0.6533.43 (Developer Build) (64-bit) Linux
Chrome 127.0.6533.72 (Official Build) (64-bit) Linux

## Initial Considerations

The following analysis is performed by using the testcase attached: `segmentation-fault-UTF16TextIterator.html` on `Chromium 127.0.6533.43 (Developer Build) Linux`

The testcase `chrome_official_127.0.6533.72_segfault.html` is attached as well because its severity as it crashes Official Latest Chrome Build 127.0.6533.72 on a Segmentation Fault while accessing to an Out-Of-Bounds memory due the Heap-Buffer-Overflow.

`segmentation-fault-UTF16TextIterator.html` hits multiple DCHECKs (12 in total) before crashing on a Segmentation Fault on data access. Because of the high number of DCHECKs hit, by modifiying the testcase, multiple other paths can be taken with invalid values which could lead to other potential memory corruptions.

AddressSanitizer establishes the bug as `use-after-poison` but it can be converted into a `heap-buffer-overflow` by modifying the line: `<any_html id="id_6">Z Z</any_html>` into `<any_html id="id_6">ZZ ZZZ</any_html>`

```

With: <any_html id="id_6">ZZ ZZZ</any_html>

==2007456==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x5040000b2232 at pc 0x55d00003a39f bp 0x7ffc7c5506d0 sp 0x7ffc7c5506c8
READ of size 2 at 0x5040000b2232 thread T0 (chrome)
    #0 0x55d00003a39e in Consume third_party/blink/renderer/platform/fonts/utf16_text_iterator.h:54:17
    #1 0x55d00003a39e in blink::HarfBuzzShaper::CollectFallbackHintChars(WTF::Deque<blink::ReshapeQueueItem, 0u, WTF::PartitionAllocator> const&, bool, WTF::Vector<int, 16u, WTF::PartitionAllocator>&) const third_party/blink/renderer/platform/fonts/shaping/harfbuzz_shaper.cc:722:21
    #2 0x55d00003b475 in blink::HarfBuzzShaper::ShapeSegment(blink::RangeContext*, blink::RunSegmenter::RunSegmenterRange const&, blink::ShapeResult*) const third_party/blink/renderer/platform/fonts/shaping/harfbuzz_shaper.cc:887:12

```
## AddressSanitizer (Release)

```
==2004788==ERROR: AddressSanitizer: use-after-poison on address 0x5030000bc57c at pc 0x55eb46a3039f bp 0x7ffc3285d450 sp 0x7ffc3285d448
READ of size 2 at 0x5030000bc57c thread T0 (chrome)
    #0 0x55eb46a3039e in Consume third_party/blink/renderer/platform/fonts/utf16_text_iterator.h:54:17
    #1 0x55eb46a3039e in blink::HarfBuzzShaper::CollectFallbackHintChars(WTF::Deque<blink::ReshapeQueueItem, 0u, WTF::PartitionAllocator> const&, bool, WTF::Vector<int, 16u, WTF::PartitionAllocator>&) const third_party/blink/renderer/platform/fonts/shaping/harfbuzz_shaper.cc:722:21
    #2 0x55eb46a31475 in blink::HarfBuzzShaper::ShapeSegment(blink::RangeContext*, blink::RunSegmenter::RunSegmenterRange const&, blink::ShapeResult*) const third_party/blink/renderer/platform/fonts/shaping/harfbuzz_shaper.cc:887:12
    #3 0x55eb46a349e0 in blink::HarfBuzzShaper::Shape(blink::Font const*, blink::TextDirection, unsigned int, unsigned int, blink::RunSegmenter::RunSegmenterRange, blink::ShapeOptions) const third_party/blink/renderer/platform/fonts/shaping/harfbuzz_shaper.cc:1113:3
    #4 0x55eb453e54d6 in blink::LineBreaker::ShapeText(blink::InlineItem const&, unsigned int, unsigned int, blink::ShapeOptions) third_party/blink/renderer/core/layout/inline/line_breaker.cc:2060:28
    #5 0x55eb46aa0cd9 in blink::ShapingLineBreaker::ShapeLineAt(unsigned int, unsigned int) third_party/blink/renderer/platform/fonts/shaping/shaping_line_breaker.cc:671:25
    #6 0x55eb453e2bb9 in blink::LineBreaker::BreakTextAt(blink::InlineItemResult*, blink::InlineItem const&, blink::ShapingLineBreaker&, blink::LineInfo*) third_party/blink/renderer/core/layout/inline/line_breaker.cc:1682:51
    #7 0x55eb453df445 in blink::LineBreaker::BreakText(blink::InlineItemResult*, blink::InlineItem const&, blink::ShapeResult const&, blink::LayoutUnit, blink::LayoutUnit, blink::LineInfo*) third_party/blink/renderer/core/layout/inline/line_breaker.cc:1567:9
    #8 0x55eb453d0cc2 in blink::LineBreaker::HandleText(blink::InlineItem const&, blink::ShapeResult const&, blink::LineInfo*) third_party/blink/renderer/core/layout/inline/line_breaker.cc:1312:9
    #9 0x55eb453ca709 in blink::LineBreaker::BreakLine(blink::LineInfo*) third_party/blink/renderer/core/layout/inline/line_breaker.cc:959:9
    #10 0x55eb453c63e7 in blink::LineBreaker::NextLine(blink::LineInfo*) third_party/blink/renderer/core/layout/inline/line_breaker.cc:849:3
    #11 0x55eb451323dc in blink::InlineLayoutAlgorithm::Layout() third_party/blink/renderer/core/layout/inline/inline_layout_algorithm.cc:1160:20
    #12 0x55eb450cf8f0 in blink::InlineNode::Layout(blink::ConstraintSpace const&, blink::BreakToken const*, blink::ColumnSpannerPath const*, blink::InlineChildLayoutContext*) const third_party/blink/renderer/core/layout/inline/inline_node.cc:1673:20
    #13 0x55eb452d7da6 in blink::(anonymous namespace)::LayoutInflow(blink::ConstraintSpace const&, blink::BreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*, blink::LayoutInputNode*, blink::InlineChildLayoutContext*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:125:25
    #14 0x55eb452d720d in blink::BlockLayoutAlgorithm::HandleInflow(blink::LayoutInputNode, blink::BreakToken const*, blink::PreviousInflowPosition*, blink::InlineChildLayoutContext*, blink::InlineBreakToken const**) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:2040:7
    #15 0x55eb452baa29 in blink::BlockLayoutAlgorithm::Layout(blink::InlineChildLayoutContext*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:921:18
    #16 0x55eb452bf086 in blink::LayoutResult const* blink::BlockLayoutAlgorithm::LayoutWithOptimalInlineChildLayoutContext<6u>(blink::InlineNode const&) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:577:32
    #17 0x55eb452b897c in blink::BlockLayoutAlgorithm::Layout() third_party/blink/renderer/core/layout/block_layout_algorithm.cc:499:14
    #18 0x55eb451db6f3 in operator()<blink::BlockLayoutAlgorithm> third_party/blink/renderer/core/layout/block_node.cc:209:50
    #19 0x55eb451db6f3 in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*) const&) third_party/blink/renderer/core/layout/block_node.cc:117:3
    #20 0x55eb451c48c3 in LayoutWithAlgorithm third_party/blink/renderer/core/layout/block_node.cc:207:3
    #21 0x55eb451c48c3 in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*) const third_party/blink/renderer/core/layout/block_node.cc:464:21
    #22 0x55eb458171ea in ComputeMinimumRowBlockSize<(lambda at ../../third_party/blink/renderer/core/layout/table/table_layout_utils.cc:1526:23)> third_party/blink/renderer/core/layout/table/table_layout_utils.cc:234:46
    #23 0x55eb458171ea in blink::ComputeSectionMinimumRowBlockSizes(blink::BlockNode const&, blink::LayoutUnit, bool, WTF::Vector<blink::TableColumnLocation, 0u, WTF::PartitionAllocator> const&, blink::TableBorders const&, blink::LayoutUnit, unsigned int, bool, WTF::Vector<blink::TableTypes::Section, 0u, WTF::PartitionAllocator>*, WTF::Vector<blink::TableTypes::Row, 0u, WTF::PartitionAllocator>*, WTF::Vector<blink::TableTypes::CellBlockConstraint, 0u, WTF::PartitionAllocator>*) third_party/blink/renderer/core/layout/table/table_layout_utils.cc:1550:38
    #24 0x55eb457dd36e in blink::TableLayoutAlgorithm::ComputeRows(blink::LayoutUnit, blink::TableGroupedChildren const&, WTF::Vector<blink::TableColumnLocation, 0u, WTF::PartitionAllocator> const&, blink::TableBorders const&, blink::LogicalSize const&, blink::BoxStrut const&, blink::LayoutUnit, WTF::Vector<blink::TableTypes::Row, 0u, WTF::PartitionAllocator>*, WTF::Vector<blink::TableTypes::CellBlockConstraint, 0u, WTF::PartitionAllocator>*, WTF::Vector<blink::TableTypes::Section, 0u, WTF::PartitionAllocator>*, blink::LayoutUnit*) third_party/blink/renderer/core/layout/table/table_layout_algorithm.cc:771:7
    #25 0x55eb457dc041 in blink::TableLayoutAlgorithm::Layout() third_party/blink/renderer/core/layout/table/table_layout_algorithm.cc:625:3
    #26 0x55eb451d9aa6 in operator()<blink::TableLayoutAlgorithm> third_party/blink/renderer/core/layout/block_node.cc:209:50
    #27 0x55eb451d9aa6 in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::TableLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*) const&) third_party/blink/renderer/core/layout/block_node.cc:117:3
    #28 0x55eb451c48c3 in LayoutWithAlgorithm third_party/blink/renderer/core/layout/block_node.cc:207:3
    #29 0x55eb451c48c3 in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*) const third_party/blink/renderer/core/layout/block_node.cc:464:21
    #30 0x55eb452cbc04 in LayoutBlockChild third_party/blink/renderer/core/layout/block_layout_algorithm.cc:113:16
    #31 0x55eb452cbc04 in blink::BlockLayoutAlgorithm::LayoutNewFormattingContext(blink::LayoutInputNode, blink::BlockBreakToken const*, blink::InflowChildData const&, blink::BfcOffset, bool, blink::BfcOffset*, blink::BoxStrut*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1854:41
    #32 0x55eb452c91c8 in blink::BlockLayoutAlgorithm::HandleNewFormattingContext(blink::LayoutInputNode, blink::BlockBreakToken const*, blink::PreviousInflowPosition*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1646:39
    #33 0x55eb452bab1d in blink::BlockLayoutAlgorithm::Layout(blink::InlineChildLayoutContext*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:916:18
    #34 0x55eb452b898e in blink::BlockLayoutAlgorithm::Layout() third_party/blink/renderer/core/layout/block_layout_algorithm.cc:501:14
    #35 0x55eb451db6f3 in operator()<blink::BlockLayoutAlgorithm> third_party/blink/renderer/core/layout/block_node.cc:209:50
    #36 0x55eb451db6f3 in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*) const&) third_party/blink/renderer/core/layout/block_node.cc:117:3
    #37 0x55eb451c48c3 in LayoutWithAlgorithm third_party/blink/renderer/core/layout/block_node.cc:207:3
    #38 0x55eb451c48c3 in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*) const third_party/blink/renderer/core/layout/block_node.cc:464:21
    #39 0x55eb452d7e42 in LayoutBlockChild third_party/blink/renderer/core/layout/block_layout_algorithm.cc:113:16
    #40 0x55eb452d7e42 in blink::(anonymous namespace)::LayoutInflow(blink::ConstraintSpace const&, blink::BreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*, blink::LayoutInputNode*, blink::InlineChildLayoutContext*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:128:10
    #41 0x55eb452d720d in blink::BlockLayoutAlgorithm::HandleInflow(blink::LayoutInputNode, blink::BreakToken const*, blink::PreviousInflowPosition*, blink::InlineChildLayoutContext*, blink::InlineBreakToken const**) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:2040:7
    #42 0x55eb452baa29 in blink::BlockLayoutAlgorithm::Layout(blink::InlineChildLayoutContext*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:921:18
    #43 0x55eb452b898e in blink::BlockLayoutAlgorithm::Layout() third_party/blink/renderer/core/layout/block_layout_algorithm.cc:501:14
    #44 0x55eb451db6f3 in operator()<blink::BlockLayoutAlgorithm> third_party/blink/renderer/core/layout/block_node.cc:209:50
    #45 0x55eb451db6f3 in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*) const&) third_party/blink/renderer/core/layout/block_node.cc:117:3
    #46 0x55eb451c48c3 in LayoutWithAlgorithm third_party/blink/renderer/core/layout/block_node.cc:207:3
    #47 0x55eb451c48c3 in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*) const third_party/blink/renderer/core/layout/block_node.cc:464:21
    #48 0x55eb452cbc04 in LayoutBlockChild third_party/blink/renderer/core/layout/block_layout_algorithm.cc:113:16
    #49 0x55eb452cbc04 in blink::BlockLayoutAlgorithm::LayoutNewFormattingContext(blink::LayoutInputNode, blink::BlockBreakToken const*, blink::InflowChildData const&, blink::BfcOffset, bool, blink::BfcOffset*, blink::BoxStrut*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1854:41
    #50 0x55eb452c91c8 in blink::BlockLayoutAlgorithm::HandleNewFormattingContext(blink::LayoutInputNode, blink::BlockBreakToken const*, blink::PreviousInflowPosition*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1646:39
    #51 0x55eb452bab1d in blink::BlockLayoutAlgorithm::Layout(blink::InlineChildLayoutContext*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:916:18
    #52 0x55eb452b898e in blink::BlockLayoutAlgorithm::Layout() third_party/blink/renderer/core/layout/block_layout_algorithm.cc:501:14
    #53 0x55eb451db6f3 in operator()<blink::BlockLayoutAlgorithm> third_party/blink/renderer/core/layout/block_node.cc:209:50
    #54 0x55eb451db6f3 in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*) const&) third_party/blink/renderer/core/layout/block_node.cc:117:3
    #55 0x55eb451c48c3 in LayoutWithAlgorithm third_party/blink/renderer/core/layout/block_node.cc:207:3
    #56 0x55eb451c48c3 in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*) const third_party/blink/renderer/core/layout/block_node.cc:464:21
    #57 0x55eb456112a6 in blink::LayoutView::LayoutRoot() third_party/blink/renderer/core/layout/layout_view.cc:810:19
    #58 0x55eb443fcc58 in blink::LocalFrameView::PerformLayout() third_party/blink/renderer/core/frame/local_frame_view.cc:783:24
    #59 0x55eb443fee7e in blink::LocalFrameView::UpdateLayout() third_party/blink/renderer/core/frame/local_frame_view.cc:842:3
    #60 0x55eb4441c0a2 in blink::LocalFrameView::UpdateStyleAndLayoutInternal() third_party/blink/renderer/core/frame/local_frame_view.cc:3171:7
    #61 0x55eb44408125 in blink::LocalFrameView::UpdateStyleAndLayout() third_party/blink/renderer/core/frame/local_frame_view.cc:3101:18
    #62 0x55eb4720d2a9 in blink::Document::UpdateStyleAndLayout(blink::DocumentUpdateReason) third_party/blink/renderer/core/dom/document.cc:2821:17
    #63 0x55eb47221ffb in blink::Document::ImplicitClose() third_party/blink/renderer/core/dom/document.cc:3986:7
    #64 0x55eb47222d9b in blink::Document::CheckCompletedInternal() third_party/blink/renderer/core/dom/document.cc:4075:5
    #65 0x55eb472215e2 in blink::Document::CheckCompleted() third_party/blink/renderer/core/dom/document.cc:4037:7
    #66 0x55eb45903619 in blink::FrameLoader::FinishedParsing() third_party/blink/renderer/core/loader/frame_loader.cc:448:26
    #67 0x55eb4725ca8a in blink::Document::FinishedParsing() third_party/blink/renderer/core/dom/document.cc:7485:21
    #68 0x55eb47545c52 in end third_party/blink/renderer/core/html/parser/html_document_parser.cc:1075:18
    #69 0x55eb47545c52 in AttemptToRunDeferredScriptsAndEnd third_party/blink/renderer/core/html/parser/html_document_parser.cc:1088:3
    #70 0x55eb47545c52 in blink::HTMLDocumentParser::PrepareToStopParsing() third_party/blink/renderer/core/html/parser/html_document_parser.cc:566:3
    #71 0x55eb4754b5b9 in blink::HTMLDocumentParser::AttemptToEnd() third_party/blink/renderer/core/html/parser/html_document_parser.cc:1112:3
    #72 0x55eb475465fe in blink::HTMLDocumentParser::PumpTokenizerIfPossible() third_party/blink/renderer/core/html/parser/html_document_parser.cc:651:5
    #73 0x55eb47546dda in blink::HTMLDocumentParser::DeferredPumpTokenizerIfPossible(bool, base::TimeTicks) third_party/blink/renderer/core/html/parser/html_document_parser.cc:620:7
    #74 0x55eb47565fdc in Invoke<void (blink::HTMLDocumentParser::*)(bool, base::TimeTicks), cppgc::internal::BasicPersistent<blink::HTMLDocumentParser, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, bool, base::TimeTicks> base/functional/bind_internal.h:738:12
    #75 0x55eb47565fdc in MakeItSo<void (blink::HTMLDocumentParser::*)(bool, base::TimeTicks), std::__Cr::tuple<cppgc::internal::BasicPersistent<blink::HTMLDocumentParser, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, bool, base::TimeTicks> > base/functional/bind_internal.h:930:12
    #76 0x55eb47565fdc in RunImpl<void (blink::HTMLDocumentParser::*)(bool, base::TimeTicks), std::__Cr::tuple<cppgc::internal::BasicPersistent<blink::HTMLDocumentParser, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, bool, base::TimeTicks>, 0UL, 1UL, 2UL> base/functional/bind_internal.h:1067:14
    #77 0x55eb47565fdc in base::internal::Invoker<base::internal::FunctorTraits<void (blink::HTMLDocumentParser::*&&)(bool, base::TimeTicks), cppgc::internal::BasicPersistent<blink::HTMLDocumentParser, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>&&, bool&&, base::TimeTicks&&>, base::internal::BindState<true, true, false, void (blink::HTMLDocumentParser::*)(bool, base::TimeTicks), cppgc::internal::BasicPersistent<blink::HTMLDocumentParser, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, bool, base::TimeTicks>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:980:12
    #78 0x55eb37818894 in Run base/functional/callback.h:156:12
    #79 0x55eb37818894 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:203:34
    #80 0x55eb3787ba46 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:486:11)> base/task/common/task_annotator.h:90:5
    #81 0x55eb3787ba46 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:484:23
    #82 0x55eb3787a960 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #83 0x55eb3787c78a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #84 0x55eb3771218d in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:40:55
    #85 0x55eb3787d3f6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:654:12
    #86 0x55eb377abb3f in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #87 0x55eb4eaaf04a in content::RendererMain(content::MainFunctionParams) content/renderer/renderer_main.cc:359:16
    #88 0x55eb34ea298b in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:689:14
    #89 0x55eb34ea3eee in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:793:12
    #90 0x55eb34ea6c18 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1156:10
    #91 0x55eb34ea0c90 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:332:36
    #92 0x55eb34ea131b in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:345:10
    #93 0x55eb24b3a3c8 in ChromeMain chrome/app/chrome_main.cc:192:12
    #94 0x7f0f6b029d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

0x5030000bc57c is located 0 bytes after 28-byte region [0x5030000bc560,0x5030000bc57c)
allocated by thread T0 (chrome) here:
    #0 0x55eb24b017af in malloc /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:68:3
    #1 0x55eb37a60aab in AllocInternal<(partition_alloc::internal::AllocFlags)0> base/allocator/partition_allocator/src/partition_alloc/partition_root.h:2110:51
    #2 0x55eb37a60aab in AllocInline<(partition_alloc::internal::AllocFlags)0> base/allocator/partition_allocator/src/partition_alloc/partition_root.h:528:12
    #3 0x55eb37a60aab in void* partition_alloc::PartitionRoot::Alloc<(partition_alloc::internal::AllocFlags)0>(unsigned long, char const*) base/allocator/partition_allocator/src/partition_alloc/partition_root.h:522:12
    #4 0x55eb3dd25f16 in CreateUninitialized third_party/blink/renderer/platform/wtf/text/string_impl.cc:145:49
    #5 0x55eb3dd25f16 in WTF::StringImpl::Create(char16_t const*, unsigned int) third_party/blink/renderer/platform/wtf/text/string_impl.cc:250:38
    #6 0x55eb3dd849b3 in WTF::String::String(char16_t const*, unsigned int) third_party/blink/renderer/platform/wtf/text/wtf_string.cc:57:26
    #7 0x55eb3dd1a85a in void WTF::StringBuilder::BuildString<WTF::String>() third_party/blink/renderer/platform/wtf/text/string_builder.h:264:17
    #8 0x55eb3dd1bb12 in WTF::StringBuilder::ToString() third_party/blink/renderer/platform/wtf/text/string_builder.cc:53:5
    #9 0x55eb451058e8 in ToString third_party/blink/renderer/core/layout/inline/inline_items_builder.cc:67:16
    #10 0x55eb451058e8 in blink::InlineItemsBuilderTemplate<blink::EmptyOffsetMappingBuilder>::DidFinishCollectInlines(blink::InlineNodeData*) third_party/blink/renderer/core/layout/inline/inline_items_builder.cc:1650:24
    #11 0x55eb450b9e7f in blink::InlineNode::CollectInlines(blink::InlineNodeData*, blink::InlineNodeData*) const third_party/blink/renderer/core/layout/inline/inline_node.cc:1080:11
    #12 0x55eb450b9359 in blink::InlineNode::PrepareLayout(blink::InlineNodeData*) const third_party/blink/renderer/core/layout/inline/inline_node.cc:597:3
    #13 0x55eb450b8f7a in blink::InlineNode::PrepareLayoutIfNeeded() const third_party/blink/renderer/core/layout/inline/inline_node.cc:583:3
    #14 0x55eb450c28a3 in blink::InlineNode::EnsureData() const third_party/blink/renderer/core/layout/inline/inline_node.cc:963:3
    #15 0x55eb451d1df5 in IsBlockLevel third_party/blink/renderer/core/layout/inline/inline_node.h:102:32
    #16 0x55eb451d1df5 in blink::BlockNode::FirstChild() const third_party/blink/renderer/core/layout/block_node.cc:1053:20
    #17 0x55eb456333ca in blink::CalculateMinMaxSizesIgnoringChildren(blink::BlockNode const&, blink::BoxStrut const&) third_party/blink/renderer/core/layout/length_utils.cc:1724:56
    #18 0x55eb452b6d9b in blink::BlockLayoutAlgorithm::ComputeMinMaxSizes(blink::MinMaxSizesFloatInput const&) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:308:11
    #19 0x55eb451e4874 in operator()<blink::BlockLayoutAlgorithm> third_party/blink/renderer/core/layout/block_node.cc:220:25
    #20 0x55eb451e4874 in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, blink::(anonymous namespace)::ComputeMinMaxSizesWithAlgorithm(blink::LayoutAlgorithmParams const&, blink::MinMaxSizesFloatInput const&)::'lambda'<typename $T>($T*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::ComputeMinMaxSizesWithAlgorithm(blink::LayoutAlgorithmParams const&, blink::MinMaxSizesFloatInput const&)::'lambda'<typename $T>($T*) const&) third_party/blink/renderer/core/layout/block_node.cc:117:3
    #21 0x55eb451cd9c4 in ComputeMinMaxSizesWithAlgorithm third_party/blink/renderer/core/layout/block_node.cc:218:3
    #22 0x55eb451cd9c4 in blink::BlockNode::ComputeMinMaxSizes(blink::WritingMode, blink::MinMaxSizesType, blink::ConstraintSpace const&, blink::MinMaxSizesFloatInput) const third_party/blink/renderer/core/layout/block_node.cc:971:30
    #23 0x55eb4580a5ef in blink::TableTypes::CreateCellInlineConstraint(blink::BlockNode const&, blink::WritingDirectionMode, bool, blink::BoxStrut const&, blink::BoxStrut const&)::$_0::operator()() const third_party/blink/renderer/core/layout/table/table_layout_algorithm_types.cc:159:16
    #24 0x55eb45809386 in blink::TableTypes::CreateCellInlineConstraint(blink::BlockNode const&, blink::WritingDirectionMode, bool, blink::BoxStrut const&, blink::BoxStrut const&) third_party/blink/renderer/core/layout/table/table_layout_algorithm_types.cc:175:9
    #25 0x55eb45814e74 in ComputeSectionInlineConstraints third_party/blink/renderer/core/layout/table/table_layout_utils.cc:435:13
    #26 0x55eb45814e74 in blink::ComputeColumnConstraints(blink::BlockNode const&, blink::TableGroupedChildren const&, blink::TableBorders const&, blink::BoxStrut const&) third_party/blink/renderer/core/layout/table/table_layout_utils.cc:1495:7
    #27 0x55eb4583d19e in blink::TableNode::GetColumnConstraints(blink::TableGroupedChildren const&, blink::BoxStrut const&) const third_party/blink/renderer/core/layout/table/table_node.cc:40:26
    #28 0x55eb457d8136 in blink::TableLayoutAlgorithm::ComputeTableInlineSize(blink::TableNode const&, blink::ConstraintSpace const&, blink::BoxStrut const&) third_party/blink/renderer/core/layout/table/table_layout_algorithm.cc:515:13
    #29 0x55eb45625e31 in blink::ComputeInlineSizeForFragment(blink::ConstraintSpace const&, blink::BlockNode const&, blink::BoxStrut const&, base::FunctionRef<blink::MinMaxSizesResult (blink::MinMaxSizesType)>) third_party/blink/renderer/core/layout/length_utils.cc:505:32
    #30 0x55eb456304ea in blink::CalculateInitialFragmentGeometry(blink::ConstraintSpace const&, blink::BlockNode const&, blink::BlockBreakToken const*, base::FunctionRef<blink::MinMaxSizesResult (blink::MinMaxSizesType)>, bool) third_party/blink/renderer/core/layout/length_utils.cc:1493:22
    #31 0x55eb45630f4b in blink::CalculateInitialFragmentGeometry(blink::ConstraintSpace const&, blink::BlockNode const&, blink::BlockBreakToken const*, bool) third_party/blink/renderer/core/layout/length_utils.cc:1534:10
    #32 0x55eb451c3ca3 in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*) const third_party/blink/renderer/core/layout/block_node.cc:394:9
    #33 0x55eb452cbc04 in LayoutBlockChild third_party/blink/renderer/core/layout/block_layout_algorithm.cc:113:16
    #34 0x55eb452cbc04 in blink::BlockLayoutAlgorithm::LayoutNewFormattingContext(blink::LayoutInputNode, blink::BlockBreakToken const*, blink::InflowChildData const&, blink::BfcOffset, bool, blink::BfcOffset*, blink::BoxStrut*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1854:41
    #35 0x55eb452c91c8 in blink::BlockLayoutAlgorithm::HandleNewFormattingContext(blink::LayoutInputNode, blink::BlockBreakToken const*, blink::PreviousInflowPosition*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1646:39
    #36 0x55eb452bab1d in blink::BlockLayoutAlgorithm::Layout(blink::InlineChildLayoutContext*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:916:18
    #37 0x55eb452b898e in blink::BlockLayoutAlgorithm::Layout() third_party/blink/renderer/core/layout/block_layout_algorithm.cc:501:14
    #38 0x55eb451db6f3 in operator()<blink::BlockLayoutAlgorithm> third_party/blink/renderer/core/layout/block_node.cc:209:50
    #39 0x55eb451db6f3 in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*) const&) third_party/blink/renderer/core/layout/block_node.cc:117:3

SUMMARY: AddressSanitizer: use-after-poison third_party/blink/renderer/platform/fonts/utf16_text_iterator.h:54:17 in Consume
Shadow bytes around the buggy address:
  0x5030000bc280: f7 fa 00 00 00 fa f7 fa fd fd fd fa f7 fa fd fd
  0x5030000bc300: fd fa f7 fa 00 00 00 fa f7 fa fd fd fd fd f7 fa
  0x5030000bc380: 00 00 00 03 f7 fa 00 00 04 fa f7 fa fd fd fd fd
  0x5030000bc400: f7 fa fd fd fd fd f7 fa fd fd fd fd f7 fa fd fd
  0x5030000bc480: fd fa f7 fa 00 00 00 00 f7 fa 00 00 00 fa f7 fa
=>0x5030000bc500: fd fd fd fd f7 fa fd fd fd fa f7 fa 00 00 00[04]
  0x5030000bc580: f7 fa fd fd fd fa f7 fa 00 00 00 fa f7 fa fd fd
  0x5030000bc600: fd fa f7 fa 00 00 00 fc f7 fa 00 00 00 00 f7 fa
  0x5030000bc680: 00 00 00 00 f7 fa fd fd fd fd f7 fa fd fd fd fa
  0x5030000bc700: f7 fa fd fd fd fd f7 fa fd fd fd fd f7 fa 00 00
  0x5030000bc780: 00 00 fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb

==2004788==ADDITIONAL INFO

==2004788==Note: Please include this section with the ASan report.
Task trace:
    #0 0x55eb4754b9f5 in blink::HTMLDocumentParser::ScheduleEndIfDelayed() third_party/blink/renderer/core/html/parser/html_document_parser.cc:905:9
    #1 0x55eb39d4ae92 in IPC::ChannelAssociatedGroupController::Accept(mojo::Message*) ipc/ipc_mojo_bootstrap.cc:1160:13


==2004788==END OF ADDITIONAL INFO
==2004788==ABORTING

```
## Without AddressSanitizer (Release)

```
Received signal 11 SEGV_ACCERR 11bc002be000
#0 0x7fdf7a5c411c base::debug::CollectStackTrace() [../../base/debug/stack_trace_posix.cc:1044:7]
#1 0x7fdf7a5760cb base::debug::StackTrace::StackTrace() [../../base/debug/stack_trace.cc:242:20]
#2 0x7fdf7a576065 base::debug::StackTrace::StackTrace() [../../base/debug/stack_trace.cc:237:28]
#3 0x7fdf7a5c3a85 base::debug::(anonymous namespace)::StackDumpSignalHandler() [../../base/debug/stack_trace_posix.cc:463:3]
#4 0x7fdf28442520 (/usr/lib/x86_64-linux-gnu/libc.so.6+0x4251f)
#5 0x7fdf37fa8a5d blink::UTF16TextIterator::Consume() [../../third_party/blink/renderer/platform/fonts/utf16_text_iterator.h:54:18]
#6 0x7fdf38034c6d blink::SmallCapsIterator::Consume() [../../third_party/blink/renderer/platform/fonts/small_caps_iterator.cc:24:26]
#7 0x7fdf37fd140c blink::(anonymous namespace)::SplitUntilNextCaseChange() [../../third_party/blink/renderer/platform/fonts/shaping/harfbuzz_shaper.cc:761:23]
#8 0x7fdf37fd0a11 blink::HarfBuzzShaper::ShapeSegment() [../../third_party/blink/renderer/platform/fonts/shaping/harfbuzz_shaper.cc:921:9]
#9 0x7fdf37fd2f4c blink::HarfBuzzShaper::Shape() [../../third_party/blink/renderer/platform/fonts/shaping/harfbuzz_shaper.cc:1113:3]
#10 0x7fdf3f467de4 blink::LineBreaker::ShapeText() [../../third_party/blink/renderer/core/layout/inline/line_breaker.cc:2060:28]
#11 0x7fdf3f46f891 blink::LineBreaker::BreakText()::ShapingLineBreakerImpl::Shape() [../../third_party/blink/renderer/core/layout/inline/line_breaker.cc:1546:29]
#12 0x7fdf3802b175 blink::ShapingLineBreaker::ShapeLineAt() [../../third_party/blink/renderer/platform/fonts/shaping/shaping_line_breaker.cc:671:25]
#13 0x7fdf3f4662a6 blink::LineBreaker::BreakTextAt() [../../third_party/blink/renderer/core/layout/inline/line_breaker.cc:1682:51]
#14 0x7fdf3f463c91 blink::LineBreaker::BreakText() [../../third_party/blink/renderer/core/layout/inline/line_breaker.cc:1567:9]
#15 0x7fdf3f45c255 blink::LineBreaker::HandleText() [../../third_party/blink/renderer/core/layout/inline/line_breaker.cc:1312:9]
#16 0x7fdf3f45861a blink::LineBreaker::BreakLine() [../../third_party/blink/renderer/core/layout/inline/line_breaker.cc:959:9]
#17 0x7fdf3f456c53 blink::LineBreaker::NextLine() [../../third_party/blink/renderer/core/layout/inline/line_breaker.cc:849:3]
#18 0x7fdf3f4155eb blink::InlineLayoutAlgorithm::Layout() [../../third_party/blink/renderer/core/layout/inline/inline_layout_algorithm.cc:1160:20]
#19 0x7fdf3f42918d blink::InlineNode::Layout() [../../third_party/blink/renderer/core/layout/inline/inline_node.cc:1673:20]
#20 0x7fdf3f1ef85b blink::(anonymous namespace)::LayoutInflow() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:125:25]
#21 0x7fdf3f1ef765 blink::BlockLayoutAlgorithm::HandleInflow() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:2040:7]
#22 0x7fdf3f1f6448 blink::BlockLayoutAlgorithm::Layout() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:921:18]
#23 0x7fdf3f1f70b3 blink::BlockLayoutAlgorithm::LayoutWithOptimalInlineChildLayoutContext<>() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:577:32]
#24 0x7fdf3f1e5aa8 blink::BlockLayoutAlgorithm::LayoutInlineChild() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:557:14]
#25 0x7fdf3f1e598a blink::BlockLayoutAlgorithm::Layout() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:499:14]
#26 0x7fdf3f217ac1 _ZZN5blink12_GLOBAL__N_119LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEENKUlTyPT_E_clINS_20BlockLayoutAlgorithmEEEDaS5_ [../../third_party/blink/renderer/core/layout/block_node.cc:209:50]
#27 0x7fdf3f216fc9 _ZN5blink12_GLOBAL__N_121CreateAlgorithmAndRunINS_20BlockLayoutAlgorithmEZNS0_19LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEEUlTyPT_E_EEvS5_RKT0_ [../../third_party/blink/renderer/core/layout/block_node.cc:117:3]
#28 0x7fdf3f216622 _ZN5blink12_GLOBAL__N_124DetermineAlgorithmAndRunIZNS0_19LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEEUlTyPT_E_EEvS4_RKS5_ [../../third_party/blink/renderer/core/layout/block_node.cc:200:5]
#29 0x7fdf3f210437 blink::(anonymous namespace)::LayoutWithAlgorithm() [../../third_party/blink/renderer/core/layout/block_node.cc:207:3]
#30 0x7fdf3f20ebe1 blink::BlockNode::Layout() [../../third_party/blink/renderer/core/layout/block_node.cc:464:21]
#31 0x7fdf3f7203bc blink::(anonymous namespace)::ComputeMinimumRowBlockSize<>() [../../third_party/blink/renderer/core/layout/table/table_layout_utils.cc:234:46]
#32 0x7fdf3f71fbf9 blink::ComputeSectionMinimumRowBlockSizes() [../../third_party/blink/renderer/core/layout/table/table_layout_utils.cc:1550:38]
#33 0x7fdf3f7079a8 blink::TableLayoutAlgorithm::ComputeRows() [../../third_party/blink/renderer/core/layout/table/table_layout_algorithm.cc:771:7]
#34 0x7fdf3f706f44 blink::TableLayoutAlgorithm::Layout() [../../third_party/blink/renderer/core/layout/table/table_layout_algorithm.cc:625:3]
#35 0x7fdf3f217061 _ZZN5blink12_GLOBAL__N_119LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEENKUlTyPT_E_clINS_20TableLayoutAlgorithmEEEDaS5_ [../../third_party/blink/renderer/core/layout/block_node.cc:209:50]
#36 0x7fdf3f216749 _ZN5blink12_GLOBAL__N_121CreateAlgorithmAndRunINS_20TableLayoutAlgorithmEZNS0_19LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEEUlTyPT_E_EEvS5_RKT0_ [../../third_party/blink/renderer/core/layout/block_node.cc:117:3]
#37 0x7fdf3f21647b _ZN5blink12_GLOBAL__N_124DetermineAlgorithmAndRunIZNS0_19LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEEUlTyPT_E_EEvS4_RKS5_ [../../third_party/blink/renderer/core/layout/block_node.cc:173:5]
#38 0x7fdf3f210437 blink::(anonymous namespace)::LayoutWithAlgorithm() [../../third_party/blink/renderer/core/layout/block_node.cc:207:3]
#39 0x7fdf3f20ebe1 blink::BlockNode::Layout() [../../third_party/blink/renderer/core/layout/block_node.cc:464:21]
#40 0x7fdf3f1ef077 blink::(anonymous namespace)::LayoutBlockChild() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:113:16]
#41 0x7fdf3f1ec301 blink::BlockLayoutAlgorithm::LayoutNewFormattingContext() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1854:41]
#42 0x7fdf3f1eab43 blink::BlockLayoutAlgorithm::HandleNewFormattingContext() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1646:39]
#43 0x7fdf3f1f63f6 blink::BlockLayoutAlgorithm::Layout() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:916:18]
#44 0x7fdf3f1e599d blink::BlockLayoutAlgorithm::Layout() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:501:14]
#45 0x7fdf3f217ac1 _ZZN5blink12_GLOBAL__N_119LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEENKUlTyPT_E_clINS_20BlockLayoutAlgorithmEEEDaS5_ [../../third_party/blink/renderer/core/layout/block_node.cc:209:50]
#46 0x7fdf3f216fc9 _ZN5blink12_GLOBAL__N_121CreateAlgorithmAndRunINS_20BlockLayoutAlgorithmEZNS0_19LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEEUlTyPT_E_EEvS5_RKT0_ [../../third_party/blink/renderer/core/layout/block_node.cc:117:3]
#47 0x7fdf3f216622 _ZN5blink12_GLOBAL__N_124DetermineAlgorithmAndRunIZNS0_19LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEEUlTyPT_E_EEvS4_RKS5_ [../../third_party/blink/renderer/core/layout/block_node.cc:200:5]
#48 0x7fdf3f210437 blink::(anonymous namespace)::LayoutWithAlgorithm() [../../third_party/blink/renderer/core/layout/block_node.cc:207:3]
#49 0x7fdf3f20ebe1 blink::BlockNode::Layout() [../../third_party/blink/renderer/core/layout/block_node.cc:464:21]
#50 0x7fdf3f1ef077 blink::(anonymous namespace)::LayoutBlockChild() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:113:16]
#51 0x7fdf3f1ef8a2 blink::(anonymous namespace)::LayoutInflow() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:128:10]
#52 0x7fdf3f1ef765 blink::BlockLayoutAlgorithm::HandleInflow() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:2040:7]
#53 0x7fdf3f1f6448 blink::BlockLayoutAlgorithm::Layout() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:921:18]
#54 0x7fdf3f1e599d blink::BlockLayoutAlgorithm::Layout() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:501:14]
#55 0x7fdf3f217ac1 _ZZN5blink12_GLOBAL__N_119LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEENKUlTyPT_E_clINS_20BlockLayoutAlgorithmEEEDaS5_ [../../third_party/blink/renderer/core/layout/block_node.cc:209:50]
#56 0x7fdf3f216fc9 _ZN5blink12_GLOBAL__N_121CreateAlgorithmAndRunINS_20BlockLayoutAlgorithmEZNS0_19LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEEUlTyPT_E_EEvS5_RKT0_ [../../third_party/blink/renderer/core/layout/block_node.cc:117:3]
#57 0x7fdf3f216622 _ZN5blink12_GLOBAL__N_124DetermineAlgorithmAndRunIZNS0_19LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEEUlTyPT_E_EEvS4_RKS5_ [../../third_party/blink/renderer/core/layout/block_node.cc:200:5]
#58 0x7fdf3f210437 blink::(anonymous namespace)::LayoutWithAlgorithm() [../../third_party/blink/renderer/core/layout/block_node.cc:207:3]
#59 0x7fdf3f20ebe1 blink::BlockNode::Layout() [../../third_party/blink/renderer/core/layout/block_node.cc:464:21]
#60 0x7fdf3f1ef077 blink::(anonymous namespace)::LayoutBlockChild() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:113:16]
#61 0x7fdf3f1ec301 blink::BlockLayoutAlgorithm::LayoutNewFormattingContext() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1854:41]
#62 0x7fdf3f1eab43 blink::BlockLayoutAlgorithm::HandleNewFormattingContext() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1646:39]
#63 0x7fdf3f1f63f6 blink::BlockLayoutAlgorithm::Layout() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:916:18]
#64 0x7fdf3f1e599d blink::BlockLayoutAlgorithm::Layout() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:501:14]
#65 0x7fdf3f217ac1 _ZZN5blink12_GLOBAL__N_119LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEENKUlTyPT_E_clINS_20BlockLayoutAlgorithmEEEDaS5_ [../../third_party/blink/renderer/core/layout/block_node.cc:209:50]
#66 0x7fdf3f216fc9 _ZN5blink12_GLOBAL__N_121CreateAlgorithmAndRunINS_20BlockLayoutAlgorithmEZNS0_19LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEEUlTyPT_E_EEvS5_RKT0_ [../../third_party/blink/renderer/core/layout/block_node.cc:117:3]
#67 0x7fdf3f216622 _ZN5blink12_GLOBAL__N_124DetermineAlgorithmAndRunIZNS0_19LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEEUlTyPT_E_EEvS4_RKS5_ [../../third_party/blink/renderer/core/layout/block_node.cc:200:5]
#68 0x7fdf3f210437 blink::(anonymous namespace)::LayoutWithAlgorithm() [../../third_party/blink/renderer/core/layout/block_node.cc:207:3]
#69 0x7fdf3f20ebe1 blink::BlockNode::Layout() [../../third_party/blink/renderer/core/layout/block_node.cc:464:21]
#70 0x7fdf3f5c4f54 blink::LayoutView::LayoutRoot() [../../third_party/blink/renderer/core/layout/layout_view.cc:810:19]
#71 0x7fdf3e73d531 blink::LocalFrameView::PerformLayout() [../../third_party/blink/renderer/core/frame/local_frame_view.cc:783:24]
#72 0x7fdf3e73e73f blink::LocalFrameView::UpdateLayout() [../../third_party/blink/renderer/core/frame/local_frame_view.cc:842:3]
#73 0x7fdf3e751c06 blink::LocalFrameView::UpdateStyleAndLayoutInternal() [../../third_party/blink/renderer/core/frame/local_frame_view.cc:3171:7]
#74 0x7fdf3e743430 blink::LocalFrameView::UpdateStyleAndLayout() [../../third_party/blink/renderer/core/frame/local_frame_view.cc:3101:18]
#75 0x7fdf4035803f blink::Document::UpdateStyleAndLayout() [../../third_party/blink/renderer/core/dom/document.cc:2821:17]
#76 0x7fdf4036213f blink::Document::ImplicitClose() [../../third_party/blink/renderer/core/dom/document.cc:3986:7]
#77 0x7fdf403626c4 blink::Document::CheckCompletedInternal() [../../third_party/blink/renderer/core/dom/document.cc:4075:5]
#78 0x7fdf40361e79 blink::Document::CheckCompleted() [../../third_party/blink/renderer/core/dom/document.cc:4037:7]
#79 0x7fdf3f7ef834 blink::FrameLoader::FinishedParsing() [../../third_party/blink/renderer/core/loader/frame_loader.cc:448:26]
#80 0x7fdf40379279 blink::Document::FinishedParsing() [../../third_party/blink/renderer/core/dom/document.cc:7485:21]
#81 0x7fdf404999f1 blink::HTMLConstructionSite::FinishedParsing() [../../third_party/blink/renderer/core/html/parser/html_construction_site.cc:757:14]
#82 0x7fdf40541c7d blink::HTMLTreeBuilder::Finished() [../../third_party/blink/renderer/core/html/parser/html_tree_builder.cc:3162:9]
#83 0x7fdf404b5950 blink::HTMLDocumentParser::end() [../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:1075:18]
#84 0x7fdf404af797 blink::HTMLDocumentParser::AttemptToRunDeferredScriptsAndEnd() [../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:1088:3]
#85 0x7fdf404aee78 blink::HTMLDocumentParser::PrepareToStopParsing() [../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:566:3]
#86 0x7fdf404b27eb blink::HTMLDocumentParser::AttemptToEnd() [../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:1112:3]
#87 0x7fdf404af425 blink::HTMLDocumentParser::PumpTokenizerIfPossible() [../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:651:5]
#88 0x7fdf404afe9a blink::HTMLDocumentParser::DeferredPumpTokenizerIfPossible() [../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:620:7]
#89 0x7fdf404c7e5b base::internal::DecayedFunctorTraits<>::Invoke<>() [../../base/functional/bind_internal.h:738:12]
#90 0x7fdf404c7dab base::internal::InvokeHelper<>::MakeItSo<>() [../../base/functional/bind_internal.h:930:12]
#91 0x7fdf404c7d0d base::internal::Invoker<>::RunImpl<>() [../../base/functional/bind_internal.h:1067:14]
#92 0x7fdf404c7c77 base::internal::Invoker<>::RunOnce() [../../base/functional/bind_internal.h:980:12]
#93 0x7fdf3d679dd6 base::OnceCallback<>::Run() [../../base/functional/callback.h:156:12]
#94 0x7fdf3d679d05 WTF::ThreadCheckingCallbackWrapper<>::RunInternal() [../../third_party/blink/renderer/platform/wtf/functional.h:242:33]
#95 0x7fdf3d678a03 WTF::ThreadCheckingCallbackWrapper<>::Run() [../../third_party/blink/renderer/platform/wtf/functional.h:227:12]
#96 0x7fdf3d6795e8 base::internal::DecayedFunctorTraits<>::Invoke<>() [../../base/functional/bind_internal.h:738:12]
#97 0x7fdf3d679569 base::internal::InvokeHelper<>::MakeItSo<>() [../../base/functional/bind_internal.h:930:12]
#98 0x7fdf3d6794fd base::internal::Invoker<>::RunImpl<>() [../../base/functional/bind_internal.h:1067:14]
#99 0x7fdf3d679487 base::internal::Invoker<>::RunOnce() [../../base/functional/bind_internal.h:980:12]
#100 0x7fdf7a246bb6 base::OnceCallback<>::Run() [../../base/functional/callback.h:156:12]
#101 0x7fdf7a415651 base::TaskAnnotator::RunTaskImpl() [../../base/task/common/task_annotator.cc:203:34]
#102 0x7fdf7a47ee20 base::TaskAnnotator::RunTask<>() [../../base/task/common/task_annotator.h:90:5]
#103 0x7fdf7a47e8f8 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl() [../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:484:23]
#104 0x7fdf7a47de00 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() [../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40]
#105 0x7fdf7a47eb73 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
#106 0x7fdf7a2cd31d base::MessagePumpDefault::Run() [../../base/message_loop/message_pump_default.cc:40:55]
#107 0x7fdf7a47f52b base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run() [../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:654:12]
#108 0x7fdf7a394d27 base::RunLoop::Run() [../../base/run_loop.cc:134:14]
#109 0x7fdf77adab63 content::RendererMain() [../../content/renderer/renderer_main.cc:359:16]
#110 0x7fdf77ea5130 content::RunZygote() [../../content/app/content_main_runner_impl.cc:689:14]
#111 0x7fdf77ea58fe content::RunOtherNamedProcessTypeMain() [../../content/app/content_main_runner_impl.cc:793:12]
#112 0x7fdf77ea6d38 content::ContentMainRunnerImpl::Run() [../../content/app/content_main_runner_impl.cc:1156:10]
#113 0x7fdf77ea31a9 content::RunContentProcess() [../../content/app/content_main.cc:332:36]
#114 0x7fdf77ea37f6 content::ContentMain() [../../content/app/content_main.cc:345:10]
#115 0x56170d27758d ChromeMain [../../chrome/app/chrome_main.cc:192:12]
#116 0x56170d2772b2 main
#117 0x7fdf28429d90 (/usr/lib/x86_64-linux-gnu/libc.so.6+0x29d8f)
#118 0x7fdf28429e40 __libc_start_main
#119 0x56170d2771ca _start
  r8: 0000000000000001  r9: 0000000000000001 r10: 00007fdf54e31a26 r11: 00007fdf54e29ab2
 r12: 00007ffe6f70aab8 r13: 000056170d277290 r14: 6f70060000007f00 r15: 00007ffe6f700d90
  di: 00007ffe6f6f23d8  si: 00007ffe6f6f23fc  bp: 00007ffe6f6f2370  bx: 00007ffe6f6f4550
  dx: 0000000000000002  ax: 00007ffe6f6f23d8  cx: 000011bc002be000  sp: 00007ffe6f6f2350
  ip: 00007fdf37fa8a5d efl: 0000000000010217 cgf: 002b000000000033 erf: 0000000000000004
 trp: 000000000000000e msk: 0000000000000000 cr2: 000011bc002be000
[end of stack trace]

```
## Debug DChecks

```
DCheck 1) [2005566:1:0718/173543.238525:FATAL:inline_node.cc(2039)] Check failed: (*max_size_out)->Round() == content_size.Round() (20024 vs. 20016)0x110400223a30:LayoutTableCell (anonymous, children-inline)
DCheck 2) [1992698:1:0718/153328.633009:FATAL:line_breaker.cc(1671)] Check failed: current_.text_offset <= break_at_.end.text_offset (4 vs. 2)
DCheck 3) [1993290:1:0718/153648.682803:FATAL:text_offset_range.h(26)] Check failed: end >= start (2 vs. 4)
DCheck 4) [1994327:1:0718/154500.563445:FATAL:shaping_line_breaker.cc(648)] Check failed: end > start (2 vs. 4)
DCheck 5) [1994640:1:0718/154618.035666:FATAL:shape_result.cc(2218)] Check failed: start_index_ <= offset (3 vs. 2)
DCheck 6) [1994915:1:0718/154833.461139:FATAL:shape_result.cc(2222)] Check failed: adjusted_offset <= length (4294967295 vs. 6)
DCheck 7) [1995229:1:0718/155028.137693:FATAL:harfbuzz_shaper.cc(1104)] Check failed: end >= start (2 vs. 9)
DCheck 8) [1995533:1:0718/155149.030505:FATAL:harfbuzz_shaper.cc(230)] Check failed: end >= start (2 vs. 9)
DCheck 9) [1995799:1:0718/155259.399759:FATAL:harfbuzz_shaper.cc(944)] Check failed: shape_end > shape_start (2 vs. 9)
DCheck 10) [1996064:1:0718/155412.164470:FATAL:han_kerning.cc(205)] Check failed: end > start (2 vs. 9)
DCheck 11) [1996451:1:0718/155556.349269:FATAL:harfbuzz_shaper.cc(90)] Check failed: start <= end (9 vs. 2)
DCheck 12) [1996718:1:0718/155700.662632:FATAL:line_breaker.cc(2433)] Check failed: current_.text_offset >= item.StartOffset() (2 vs. 3)

```

The initial DCHECK points to the following code:

```
#if EXPENSIVE_DCHECKS_ARE_ON()
    // Check the max size matches to the value computed from 2 pass.
    LayoutUnit content_size = ComputeContentSize(
        node, container_writing_mode, space, float_input,
        LineBreakerMode::kMaxContent, max_size_cache, nullptr, nullptr);
    bool values_might_be_saturated =
        (*max_size_out)->MightBeSaturated() || content_size.MightBeSaturated();
    if (!values_might_be_saturated) {
      DCHECK_EQ((*max_size_out)->Round(), content_size.Round())
          << node.GetLayoutBox(); //[1] (20024 vs. 20016)
    }
#endif

```

At [1], `(*max_size_out)->Round()` is 20024 while `content_size.Round()` is 20016. This generates a "Size Mismatch" bug which starts triggering multiple other DCHECKs, related with checking the sizes and positions of the buffer involved.

This ends on a Segmentation Fault when trying to read from `characters_` at `inline bool Consume(UChar32& character)`. See [2]

```
  inline bool Consume(UChar32& character) {
    if (offset_ >= size_) {
      return false;
    }

    character = *characters_; //[2]
    current_glyph_length_ = 1;
    if (!U16_IS_SURROGATE(character))
      return true;

    return ConsumeSurrogatePair(character);
  }

```

At the Segmentation Fault moment, the Registers and the Code are:

```
Stopped reason: SIGSEGV
0x00007f230f5a8a5d in blink::UTF16TextIterator::Consume (this=0x7ffd92ad8238, character=@0x7ffd92ad825c: 0x0) at ../../third_party/blink/renderer/platform/fonts/utf16_text_iterator.h:54

rax            0x7ffd92ad8238      0x7ffd92ad8238
rbx            0x7ffd92ada3b0      0x7ffd92ada3b0
rcx            0x3be0002be000      0x3be0002be000
rdx            0x2                 0x2
rsi            0x7ffd92ad825c      0x7ffd92ad825c
rdi            0x7ffd92ad8238      0x7ffd92ad8238
rbp            0x7ffd92ad81d0      0x7ffd92ad81d0
rsp            0x7ffd92ad81b0      0x7ffd92ad81b0
r8             0x1                 0x1
r9             0x1                 0x1
r10            0x7f232c431a26      0x7f232c431a26
r11            0x7f232c429ab2      0x7f232c429ab2
r12            0x7ffd92af0918      0x7ffd92af0918
r13            0x55b7855ba290      0x55b7855ba290
r14            0x92ae650000007f00  0x92ae650000007f00
r15            0x7ffd92ae6bf0      0x7ffd92ae6bf0
rip            0x7f230f5a8a5d      0x7f230f5a8a5d <blink::UTF16TextIterator::Consume(int&)+45>
eflags         0x10203             [ CF IF RF ]
cs             0x33                0x33
ss             0x2b                0x2b
ds             0x0                 0x0
es             0x0                 0x0
fs             0x0                 0x0
gs             0x0                 0x0

   0x7f230f5a8a54 <_ZN5blink17UTF16TextIterator7ConsumeERi+36>:	jmp    0x7f230f5a8a97 <_ZN5blink17UTF16TextIterator7ConsumeERi+103>
   0x7f230f5a8a56 <_ZN5blink17UTF16TextIterator7ConsumeERi+38>:	mov    rax,QWORD PTR [rbp-0x20]
   0x7f230f5a8a5a <_ZN5blink17UTF16TextIterator7ConsumeERi+42>:	mov    rcx,QWORD PTR [rax]
=> 0x7f230f5a8a5d <_ZN5blink17UTF16TextIterator7ConsumeERi+45>:	movzx  edx,WORD PTR [rcx]
   0x7f230f5a8a60 <_ZN5blink17UTF16TextIterator7ConsumeERi+48>:	mov    rcx,QWORD PTR [rbp-0x18]
   0x7f230f5a8a64 <_ZN5blink17UTF16TextIterator7ConsumeERi+52>:	mov    DWORD PTR [rcx],edx
   0x7f230f5a8a66 <_ZN5blink17UTF16TextIterator7ConsumeERi+54>:	mov    DWORD PTR [rax+0x18],0x1
   0x7f230f5a8a6d <_ZN5blink17UTF16TextIterator7ConsumeERi+61>:	mov    rax,QWORD PTR [rbp-0x18]

```

Where `rcx` points to an unmapped memory area.

Printing the "this" object of `UTF16TextIterator` class at the crash moment, it can be observed that the `size_` could have suffered an integer overflow.

```
p *this
$2 = {
  characters_ = 0x3be0002be000 u"",
  characters_end_ = 0x3be2002a3992 u"",
  offset_ = 0xd03a,
  size_ = 0xfffffd03,
  current_glyph_length_ = 0x1
}


```

The testase `chrome_official_127.0.6533.72_segfault.html` crashes `127.0.6533.72 (Official Build) (64-bit) stable` in this way:

```
rax            0x12400918dd4       0x12400918dd4
rbx            0x1a4               0x1a4
rcx            0xffffff8c          0xffffff8c
rdx            0x3116              0x3116
rsi            0xffff009f          0xffff009f
rdi            0xffffcfe0          0xffffcfe0
rbp            0x7ffd409b3a70      0x7ffd409b3a70
rsp            0x7ffd409b3970      0x7ffd409b3970
r8             0x101               0x101
r9             0x2d2400287230      0x2d2400287230
r10            0x7ffd409b3e00      0x7ffd409b3e00
r11            0x0                 0x0
r12            0x0                 0x0
r13            0x2d240015e280      0x2d240015e280
r14            0x2d2400287230      0x2d2400287230
r15            0x130               0x130
rip            0x560e68f2d930      0x560e68f2d930
eflags         0x10202             [ IF RF ]
cs             0x33                0x33
ss             0x2b                0x2b
ds             0x0                 0x0
es             0x0                 0x0
fs             0x0                 0x0
gs             0x0                 0x0

   0x560e68f2d91c:	adc    ecx,0x0
   0x560e68f2d91f:	xor    edx,edx
   0x560e68f2d921:	data16 data16 data16 data16 data16 cs nop WORD PTR [rax+rax*1+0x0]
=> 0x560e68f2d930:	movzx  esi,WORD PTR [rax+rdx*2]
   0x560e68f2d934:	lea    edi,[rsi-0x3020]
   0x560e68f2d93a:	cmp    edi,0xffffeff7
   0x560e68f2d940:	ja     0x560e68f2d957
   0x560e68f2d942:	add    esi,0xffff009f

gdb$ x/10xg $rax+$rdx*2
0x1240091f000:	0x0000000000000000	0x0000000000000000
0x1240091f010:	0x0000000000000000	0x0000000000000000
0x1240091f020:	0x0000000000000000	0x0000000000000000
0x1240091f030:	0x0000000000000000	0x0000000000000000
0x1240091f040:	0x0000000000000000	0x0000000000000000

gdb$ info proc mapping
...
       0x12400918000      0x1240091f000     0x7000        0x0  rw-p   [anon:partition_alloc]
       0x1240091f000      0x12400a01000    0xe2000        0x0  ---p   [anon:partition_alloc] ===> Not initialized. Accessing there because the Heap Buffer Overflow.
       0x12400a01000      0x12400a02000     0x1000        0x0  rw-p   [anon:partition_alloc]
...

```

VERSION
Chrome Version: 127.0.6533.72 (Official Build) (64-bit) stable
Operating System: Tested on Linux.

REPRODUCTION CASE

- segmentation-fault-UTF16TextIterator.html
- chrome\_official\_127.0.6533.72\_segfault.html

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: Tab Crash (Render Process)

CREDIT INFORMATION
Reporter credit: Tashita Software Security

## Attachments

- [chrome_official_127.0.6533.72_segfault.html](attachments/chrome_official_127.0.6533.72_segfault.html) (text/html, 2.3 KB)
- [segmentation-fault-UTF16TextIterator.html](attachments/segmentation-fault-UTF16TextIterator.html) (text/html, 1.4 KB)

## Timeline

### ti...@chromium.org (2024-07-29)

[Security shepherd] Looking into this.

### ti...@chromium.org (2024-07-29)

I can reproduce this with the latest Linux ASAN release build: <https://storage.cloud.google.com/chromium-browser-asan/linux-release/asan-linux-release-1334260.zip>

```
=================================================================
==3242==ERROR: AddressSanitizer: use-after-poison on address 0x50300008f3fc at pc 0x566af4bbafc3 bp 0x7ffd07c73a10 sp 0x7ffd07c73a08
READ of size 2 at 0x50300008f3fc thread T0 (chrome)
==3242==WARNING: invalid path to external symbolizer!
==3242==WARNING: Failed to use and restart external symbolizer!
    #0 0x566af4bbafc2  (/home/titouan/chrome-release-1334260/chrome+0x31be8fc2) (BuildId: 7780549714cf8f52)
    #1 0x566af4bbc115  (/home/titouan/chrome-release-1334260/chrome+0x31bea115) (BuildId: 7780549714cf8f52)
    #2 0x566af4bbf6c0  (/home/titouan/chrome-release-1334260/chrome+0x31bed6c0) (BuildId: 7780549714cf8f52)
    #3 0x566af3541926  (/home/titouan/chrome-release-1334260/chrome+0x3056f926) (BuildId: 7780549714cf8f52)
    #4 0x566af4c2ab29  (/home/titouan/chrome-release-1334260/chrome+0x31c58b29) (BuildId: 7780549714cf8f52)
    #5 0x566af353eff9  (/home/titouan/chrome-release-1334260/chrome+0x3056cff9) (BuildId: 7780549714cf8f52)
    #6 0x566af353b722  (/home/titouan/chrome-release-1334260/chrome+0x30569722) (BuildId: 7780549714cf8f52)
    #7 0x566af352cdf2  (/home/titouan/chrome-release-1334260/chrome+0x3055adf2) (BuildId: 7780549714cf8f52)
    #8 0x566af352656f  (/home/titouan/chrome-release-1334260/chrome+0x3055456f) (BuildId: 7780549714cf8f52)
    #9 0x566af3521fd7  (/home/titouan/chrome-release-1334260/chrome+0x3054ffd7) (BuildId: 7780549714cf8f52)
    #10 0x566af326b44c  (/home/titouan/chrome-release-1334260/chrome+0x3029944c) (BuildId: 7780549714cf8f52)
    #11 0x566af3208204  (/home/titouan/chrome-release-1334260/chrome+0x30236204) (BuildId: 7780549714cf8f52)
    #12 0x566af3428746  (/home/titouan/chrome-release-1334260/chrome+0x30456746) (BuildId: 7780549714cf8f52)
    #13 0x566af3427bac  (/home/titouan/chrome-release-1334260/chrome+0x30455bac) (BuildId: 7780549714cf8f52)
    #14 0x566af3408f51  (/home/titouan/chrome-release-1334260/chrome+0x30436f51) (BuildId: 7780549714cf8f52)
    #15 0x566af340e206  (/home/titouan/chrome-release-1334260/chrome+0x3043c206) (BuildId: 7780549714cf8f52)
    #16 0x566af340676c  (/home/titouan/chrome-release-1334260/chrome+0x3043476c) (BuildId: 7780549714cf8f52)
    #17 0x566af331c688  (/home/titouan/chrome-release-1334260/chrome+0x3034a688) (BuildId: 7780549714cf8f52)
    #18 0x566af33038d0  (/home/titouan/chrome-release-1334260/chrome+0x303318d0) (BuildId: 7780549714cf8f52)
    #19 0x566af3987eca  (/home/titouan/chrome-release-1334260/chrome+0x309b5eca) (BuildId: 7780549714cf8f52)
    #20 0x566af394c2be  (/home/titouan/chrome-release-1334260/chrome+0x3097a2be) (BuildId: 7780549714cf8f52)
    #21 0x566af394afcc  (/home/titouan/chrome-release-1334260/chrome+0x30978fcc) (BuildId: 7780549714cf8f52)
    #22 0x566af331a9dd  (/home/titouan/chrome-release-1334260/chrome+0x303489dd) (BuildId: 7780549714cf8f52)
    #23 0x566af33038d0  (/home/titouan/chrome-release-1334260/chrome+0x303318d0) (BuildId: 7780549714cf8f52)
    #24 0x566af341b1f3  (/home/titouan/chrome-release-1334260/chrome+0x304491f3) (BuildId: 7780549714cf8f52)
    #25 0x566af34184e2  (/home/titouan/chrome-release-1334260/chrome+0x304464e2) (BuildId: 7780549714cf8f52)
    #26 0x566af340903b  (/home/titouan/chrome-release-1334260/chrome+0x3043703b) (BuildId: 7780549714cf8f52)
    #27 0x566af340677e  (/home/titouan/chrome-release-1334260/chrome+0x3043477e) (BuildId: 7780549714cf8f52)
    #28 0x566af331c688  (/home/titouan/chrome-release-1334260/chrome+0x3034a688) (BuildId: 7780549714cf8f52)
    #29 0x566af33038d0  (/home/titouan/chrome-release-1334260/chrome+0x303318d0) (BuildId: 7780549714cf8f52)
    #30 0x566af34287e2  (/home/titouan/chrome-release-1334260/chrome+0x304567e2) (BuildId: 7780549714cf8f52)
    #31 0x566af3427bac  (/home/titouan/chrome-release-1334260/chrome+0x30455bac) (BuildId: 7780549714cf8f52)
    #32 0x566af3408f51  (/home/titouan/chrome-release-1334260/chrome+0x30436f51) (BuildId: 7780549714cf8f52)
    #33 0x566af340677e  (/home/titouan/chrome-release-1334260/chrome+0x3043477e) (BuildId: 7780549714cf8f52)
    #34 0x566af331c688  (/home/titouan/chrome-release-1334260/chrome+0x3034a688) (BuildId: 7780549714cf8f52)
    #35 0x566af33038d0  (/home/titouan/chrome-release-1334260/chrome+0x303318d0) (BuildId: 7780549714cf8f52)
    #36 0x566af341b1f3  (/home/titouan/chrome-release-1334260/chrome+0x304491f3) (BuildId: 7780549714cf8f52)
    #37 0x566af34184e2  (/home/titouan/chrome-release-1334260/chrome+0x304464e2) (BuildId: 7780549714cf8f52)
    #38 0x566af340903b  (/home/titouan/chrome-release-1334260/chrome+0x3043703b) (BuildId: 7780549714cf8f52)
    #39 0x566af340677e  (/home/titouan/chrome-release-1334260/chrome+0x3043477e) (BuildId: 7780549714cf8f52)
    #40 0x566af331c688  (/home/titouan/chrome-release-1334260/chrome+0x3034a688) (BuildId: 7780549714cf8f52)
    #41 0x566af33038d0  (/home/titouan/chrome-release-1334260/chrome+0x303318d0) (BuildId: 7780549714cf8f52)
    #42 0x566af376e5ee  (/home/titouan/chrome-release-1334260/chrome+0x3079c5ee) (BuildId: 7780549714cf8f52)
    #43 0x566af2522f68  (/home/titouan/chrome-release-1334260/chrome+0x2f550f68) (BuildId: 7780549714cf8f52)
    #44 0x566af252514e  (/home/titouan/chrome-release-1334260/chrome+0x2f55314e) (BuildId: 7780549714cf8f52)
    #45 0x566af2541e02  (/home/titouan/chrome-release-1334260/chrome+0x2f56fe02) (BuildId: 7780549714cf8f52)
    #46 0x566af252df65  (/home/titouan/chrome-release-1334260/chrome+0x2f55bf65) (BuildId: 7780549714cf8f52)
    #47 0x566af53bfc7b  (/home/titouan/chrome-release-1334260/chrome+0x323edc7b) (BuildId: 7780549714cf8f52)
    #48 0x566af53d4cbb  (/home/titouan/chrome-release-1334260/chrome+0x32402cbb) (BuildId: 7780549714cf8f52)
    #49 0x566af53d5a5b  (/home/titouan/chrome-release-1334260/chrome+0x32403a5b) (BuildId: 7780549714cf8f52)
    #50 0x566af53d42a2  (/home/titouan/chrome-release-1334260/chrome+0x324022a2) (BuildId: 7780549714cf8f52)
    #51 0x566af3a76a99  (/home/titouan/chrome-release-1334260/chrome+0x30aa4a99) (BuildId: 7780549714cf8f52)
    #52 0x566af540f91f  (/home/titouan/chrome-release-1334260/chrome+0x3243d91f) (BuildId: 7780549714cf8f52)
    #53 0x566af56fbfd2  (/home/titouan/chrome-release-1334260/chrome+0x32729fd2) (BuildId: 7780549714cf8f52)
    #54 0x566af5701969  (/home/titouan/chrome-release-1334260/chrome+0x3272f969) (BuildId: 7780549714cf8f52)
    #55 0x566af56fc97e  (/home/titouan/chrome-release-1334260/chrome+0x3272a97e) (BuildId: 7780549714cf8f52)
    #56 0x566af56fd15a  (/home/titouan/chrome-release-1334260/chrome+0x3272b15a) (BuildId: 7780549714cf8f52)
    #57 0x566af571b2dc  (/home/titouan/chrome-release-1334260/chrome+0x327492dc) (BuildId: 7780549714cf8f52)
    #58 0x566ae569ac24  (/home/titouan/chrome-release-1334260/chrome+0x226c8c24) (BuildId: 7780549714cf8f52)
    #59 0x566ae5701e86  (/home/titouan/chrome-release-1334260/chrome+0x2272fe86) (BuildId: 7780549714cf8f52)
    #60 0x566ae5700da0  (/home/titouan/chrome-release-1334260/chrome+0x2272eda0) (BuildId: 7780549714cf8f52)
    #61 0x566ae5702bca  (/home/titouan/chrome-release-1334260/chrome+0x22730bca) (BuildId: 7780549714cf8f52)
    #62 0x566ae558941d  (/home/titouan/chrome-release-1334260/chrome+0x225b741d) (BuildId: 7780549714cf8f52)
    #63 0x566ae5703836  (/home/titouan/chrome-release-1334260/chrome+0x22731836) (BuildId: 7780549714cf8f52)
    #64 0x566ae5629aef  (/home/titouan/chrome-release-1334260/chrome+0x22657aef) (BuildId: 7780549714cf8f52)
    #65 0x566afc92fd7c  (/home/titouan/chrome-release-1334260/chrome+0x3995dd7c) (BuildId: 7780549714cf8f52)
    #66 0x566ae2e50af8  (/home/titouan/chrome-release-1334260/chrome+0x1fe7eaf8) (BuildId: 7780549714cf8f52)
    #67 0x566ae2e51bf9  (/home/titouan/chrome-release-1334260/chrome+0x1fe7fbf9) (BuildId: 7780549714cf8f52)
    #68 0x566ae2e544df  (/home/titouan/chrome-release-1334260/chrome+0x1fe824df) (BuildId: 7780549714cf8f52)
    #69 0x566ae2e4edd5  (/home/titouan/chrome-release-1334260/chrome+0x1fe7cdd5) (BuildId: 7780549714cf8f52)
    #70 0x566ae2e4f3cb  (/home/titouan/chrome-release-1334260/chrome+0x1fe7d3cb) (BuildId: 7780549714cf8f52)
    #71 0x566ad23a8483  (/home/titouan/chrome-release-1334260/chrome+0xf3d6483) (BuildId: 7780549714cf8f52)
    #72 0x733db4e2a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: 08134323d00289185684a4cd177d202f39c2a5f3)
    #73 0x733db4e2a28a  (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: 08134323d00289185684a4cd177d202f39c2a5f3)
    #74 0x566ad22d4029  (/home/titouan/chrome-release-1334260/chrome+0xf302029) (BuildId: 7780549714cf8f52)

0x50300008f3fc is located 0 bytes after 28-byte region [0x50300008f3e0,0x50300008f3fc)
allocated by thread T0 (chrome) here:
    #0 0x566ad236f7af  (/home/titouan/chrome-release-1334260/chrome+0xf39d7af) (BuildId: 7780549714cf8f52)
    #1 0x566ae58e6d4b  (/home/titouan/chrome-release-1334260/chrome+0x22914d4b) (BuildId: 7780549714cf8f52)
    #2 0x566aebca5b86  (/home/titouan/chrome-release-1334260/chrome+0x28cd3b86) (BuildId: 7780549714cf8f52)
    #3 0x566aebd047e3  (/home/titouan/chrome-release-1334260/chrome+0x28d327e3) (BuildId: 7780549714cf8f52)
    #4 0x566aebc9a23a  (/home/titouan/chrome-release-1334260/chrome+0x28cc823a) (BuildId: 7780549714cf8f52)
    #5 0x566aebc9b4f2  (/home/titouan/chrome-release-1334260/chrome+0x28cc94f2) (BuildId: 7780549714cf8f52)
    #6 0x566af323e7a8  (/home/titouan/chrome-release-1334260/chrome+0x3026c7a8) (BuildId: 7780549714cf8f52)
    #7 0x566af31f2acf  (/home/titouan/chrome-release-1334260/chrome+0x30220acf) (BuildId: 7780549714cf8f52)
    #8 0x566af31f1fa0  (/home/titouan/chrome-release-1334260/chrome+0x3021ffa0) (BuildId: 7780549714cf8f52)
    #9 0x566af31f1ada  (/home/titouan/chrome-release-1334260/chrome+0x3021fada) (BuildId: 7780549714cf8f52)
    #10 0x566af31fb593  (/home/titouan/chrome-release-1334260/chrome+0x30229593) (BuildId: 7780549714cf8f52)
    #11 0x566af33116b5  (/home/titouan/chrome-release-1334260/chrome+0x3033f6b5) (BuildId: 7780549714cf8f52)
    #12 0x566af37903ef  (/home/titouan/chrome-release-1334260/chrome+0x307be3ef) (BuildId: 7780549714cf8f52)
    #13 0x566af3404b6b  (/home/titouan/chrome-release-1334260/chrome+0x30432b6b) (BuildId: 7780549714cf8f52)
    #14 0x566af332592a  (/home/titouan/chrome-release-1334260/chrome+0x3035392a) (BuildId: 7780549714cf8f52)
    #15 0x566af330d00f  (/home/titouan/chrome-release-1334260/chrome+0x3033b00f) (BuildId: 7780549714cf8f52)
    #16 0x566af397b320  (/home/titouan/chrome-release-1334260/chrome+0x309a9320) (BuildId: 7780549714cf8f52)
    #17 0x566af397a0bf  (/home/titouan/chrome-release-1334260/chrome+0x309a80bf) (BuildId: 7780549714cf8f52)
    #18 0x566af3985b84  (/home/titouan/chrome-release-1334260/chrome+0x309b3b84) (BuildId: 7780549714cf8f52)
    #19 0x566af39ae28e  (/home/titouan/chrome-release-1334260/chrome+0x309dc28e) (BuildId: 7780549714cf8f52)
    #20 0x566af3946f41  (/home/titouan/chrome-release-1334260/chrome+0x30974f41) (BuildId: 7780549714cf8f52)
    #21 0x566af3783241  (/home/titouan/chrome-release-1334260/chrome+0x307b1241) (BuildId: 7780549714cf8f52)
    #22 0x566af378d851  (/home/titouan/chrome-release-1334260/chrome+0x307bb851) (BuildId: 7780549714cf8f52)
    #23 0x566af378e43b  (/home/titouan/chrome-release-1334260/chrome+0x307bc43b) (BuildId: 7780549714cf8f52)
    #24 0x566af3302b13  (/home/titouan/chrome-release-1334260/chrome+0x30330b13) (BuildId: 7780549714cf8f52)
    #25 0x566af341b1f3  (/home/titouan/chrome-release-1334260/chrome+0x304491f3) (BuildId: 7780549714cf8f52)
    #26 0x566af34184e2  (/home/titouan/chrome-release-1334260/chrome+0x304464e2) (BuildId: 7780549714cf8f52)
    #27 0x566af340903b  (/home/titouan/chrome-release-1334260/chrome+0x3043703b) (BuildId: 7780549714cf8f52)
    #28 0x566af340677e  (/home/titouan/chrome-release-1334260/chrome+0x3043477e) (BuildId: 7780549714cf8f52)
    #29 0x566af331c688  (/home/titouan/chrome-release-1334260/chrome+0x3034a688) (BuildId: 7780549714cf8f52)

SUMMARY: AddressSanitizer: use-after-poison (/home/titouan/chrome-release-1334260/chrome+0x31be8fc2) (BuildId: 7780549714cf8f52) 
Shadow bytes around the buggy address:
  0x50300008f100: f7 fa 00 00 00 fc f7 fa 00 00 00 fa f7 fa 00 00
  0x50300008f180: 00 fa f7 fa 00 00 00 fa f7 fa fd fd fd fd f7 fa
  0x50300008f200: 00 00 00 03 f7 fa 00 00 04 fa f7 fa fd fd fd fd
  0x50300008f280: f7 fa fd fd fd fd f7 fa fd fd fd fd f7 fa fd fd
  0x50300008f300: fd fa f7 fa 00 00 00 00 f7 fa 00 00 00 fa f7 fa
=>0x50300008f380: fd fd fd fd f7 fa fd fd fd fa f7 fa 00 00 00[04]
  0x50300008f400: f7 fa 00 00 00 fa f7 fa fd fd fd fa f7 fa 00 00
  0x50300008f480: 00 fc f7 fa 00 00 00 00 f7 fa 00 00 00 00 f7 fa
  0x50300008f500: fd fd fd fd f7 fa fd fd fd fa f7 fa fd fd fd fd
  0x50300008f580: f7 fa fd fd fd fd f7 fa 00 00 00 00 fa fa fa fa
  0x50300008f600: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb

==3242==ADDITIONAL INFO

==3242==Note: Please include this section with the ASan report.
Task trace:
    #0 0x566af5701da5  (/home/titouan/chrome-release-1334260/chrome+0x3272fda5) (BuildId: 7780549714cf8f52)
    #1 0x566ae78a4422  (/home/titouan/chrome-release-1334260/chrome+0x248d2422) (BuildId: 7780549714cf8f52)


Command line: `/proc/self/exe --type=renderer --crashpad-handler-pid=3181 --enable-crash-reporter=, --no-subproc-heap-profiling --change-stack-guard-on-fork=enable --no-sandbox --file-url-path-alias=/gen=/home/titouan/chrome-release-1334260/gen --ozone-platform=x11 --lang=en-US --num-raster-threads=1 --renderer-client-id=5 --time-ticks-at-unix-epoch=-1722274097575376 --launch-time-ticks=1858623331 --shared-files=v8_context_snapshot_data:100 --metrics-shmem-handle=4,i,7882098020481586580,10296666056802235153,2097152 --field-trial-handle=3,i,9783592846204200015,2607435722666139535,262144 --variations-seed-version`


==3242==END OF ADDITIONAL INFO
==3242==ABORTING

```

### ti...@chromium.org (2024-07-29)

And with the official build from `https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb` on Linux.

### cl...@appspot.gserviceaccount.com (2024-07-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6323920070180864.

### cl...@appspot.gserviceaccount.com (2024-07-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5999087214067712.

### ti...@chromium.org (2024-07-29)

ClusterFuzz can reproduce too. It's going to slowly bisect the regression range.

### mo...@google.com (2024-07-30)

@drott could you please have a look? Could it be related to the performance optimisation work for symbols iterator that you were doing, i.e. crrev.com/c/5317569 and crrev.com/c/5317649?

### pe...@google.com (2024-07-30)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-07-30)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ar...@chromium.org (2024-08-06)

Hi @drott,

I'm following up on this security bug. We aim to have a fix available to all users within 60 days, which would necessitate landing a fix within the first week or two. Could you please take a look at #8?

Secondary Security Shepherd

### dr...@chromium.org (2024-08-06)

> Could it be related to the performance optimisation work for symbols iterator that you were doing, i.e. [crrev.com/c/5317569](https://crrev.com/c/5317569) and [crrev.com/c/5317649](https://crrev.com/c/5317649)?

Work was done to improve `UTF16RagelIterator`, but the crash site and suspected integer overflow happens in `UTF16TextIterator` which is a different class. The detailed crash analysis (thank you, reporter!) also indicates the source of the problem is within the saturation / text overflow computation in `InlineNode`. Requesting layout folks to have a look.

Ian, Koji, Kent - could you take a look?

Titouan wrote:

> ClusterFuzz can reproduce too. It's going to slowly bisect the regression range.

The triggered ClusterFuzz analysis in <https://clusterfuzz.com/testcase-detail/5999087214067712> seems to have run into the DCHECK in HanKerning, which I filed as separate [issue 357622693](https://issues.chromium.org/issues/357622693).

### ko...@chromium.org (2024-08-08)

The DCHECK failure is about the optimized logic produces the same result as the unoptimized logic, and it firing for saturated coordinate values is ok. It shouldn't be the cause for a string heap-buffer-overflow.

The stack indicates it's within [this function](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/fonts/shaping/harfbuzz_shaper.h;l=83-88?q=harfbuzzshaper&ss=chromium%2Fchromium%2Fsrc):

```
  ShapeResult* Shape(const Font*,
                     TextDirection,
                     unsigned start,
                     unsigned end,
                     const Vector<RunSegmenter::RunSegmenterRange>&,
                     ShapeOptions = ShapeOptions()) const;

```

The layout engine may be passing bad `start` or `end`, that will be a bug in layout if so.

Separately, I think `HarfBuzzShaper` ending up with heap-buffer-overflow should be avoided even for such cases. How about adding `CHECK`s to `HarfBuzzShaper` for such cases?

FYI, we have a code health rotation to replace raw pointers to `base::span` ([issue 351564777](https://issues.chromium.org/issues/351564777)). In a long run, it might be good to apply that to `HarfBuzzShaper`.

### dr...@chromium.org (2024-08-08)

> Separately, I think HarfBuzzShaper ending up with heap-buffer-overflow should be avoided even for such cases. How about adding CHECKs to HarfBuzzShaper for such cases?

The crash is in `UTF16TextIterator` and size checks are in place, so I do agree with your other suggested possibility:

> The layout engine may be passing bad start or end, that will be a bug in layout if so.

Yes, that was my understanding of what is going on here:

For several reasons:

> `DCheck 1) [2005566:1:0718/173543.238525:FATAL:inline_node.cc(2039)] Check failed: (*max_size_out)->Round() == content_size.Round() (20024 vs. 20016)0x110400223a30:LayoutTableCell (anonymous, children-inline)`
> `DCheck 2) [1992698:1:0718/153328.633009:FATAL:line_breaker.cc(1671)] Check failed: current_.text_offset <= break_at_.end.text_offset (4 vs. 2)`
> `DCheck 3) [1993290:1:0718/153648.682803:FATAL:text_offset_range.h(26)] Check failed: end >= start (2 vs. 4)`
> `DCheck 4) [1994327:1:0718/154500.563445:FATAL:shaping_line_breaker.cc(648)] Check failed: end > start (2 vs. 4)`
> `DCheck 5) [1994640:1:0718/154618.035666:FATAL:shape_result.cc(2218)] Check failed: start_index_ <= offset (3 vs. 2)`
> `DCheck 6) [1994915:1:0718/154833.461139:FATAL:shape_result.cc(2222)] Check failed: adjusted_offset <= length (4294967295 vs. 6)`

1. Several DCHECKS in layout code seem to fail with offset / length problems before the text is passed down to shaping.

> The DCHECK failure is about the optimized logic produces the same result as the unoptimized logic, and it firing for saturated coordinate values is ok. It shouldn't be the cause for a string heap-buffer-overflow.

2. I am at least surprised that the two code paths would disagree?
3. The reporter looked at the size value in `UTF16TextIterator`, see above:

> Printing the "this" object of UTF16TextIterator class at the crash moment, it can be observed that the size\_ could have suffered an integer overflow.

The size value

```
size_ = 0xfffffd03,

```

would indicate a 4.295GB text content size, which seems very unlikely.

So yes, my assumption is that the size computation is wrong and this can't be corrected at the shaping stage and needs fixing in layout.

Whether the value is passed as an extra length argument or as a span has coding safety benefits, but would not address this issue either.

### ap...@google.com (2024-08-09)

Project: chromium/src
Branch: main

commit 59c286e8419f07143ce859342f0fe9ddea36392d
Author: Koji Ishii <kojii@chromium.org>
Date:   Fri Aug 09 08:47:58 2024

    Fix a range `CHECK` for when it overflows
    
    This patch fixes a `CHECK` for a range of a string when
    `offset + length` overflows the `unsigned`.
    
    Bug: 355731798
    Change-Id: If04222f10f2b73b6dcd6b412cf4d82fa5b71bbe2
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5776342
    Commit-Queue: Kent Tamura <tkent@chromium.org>
    Auto-Submit: Koji Ishii <kojii@chromium.org>
    Reviewed-by: Kent Tamura <tkent@chromium.org>
    Commit-Queue: Koji Ishii <kojii@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1339526}

M       third_party/blink/renderer/platform/fonts/shaping/harfbuzz_shaper.cc
M       third_party/blink/renderer/platform/fonts/shaping/harfbuzz_shaper.h

https://chromium-review.googlesource.com/5776342


### ap...@google.com (2024-08-10)

Project: chromium/src
Branch: main

commit ef6f7b4521bb9e8d0235550c93acf885e198abdb
Author: Koji Ishii <kojii@chromium.org>
Date:   Sat Aug 10 03:04:39 2024

    Check string range in `ShapeSegment`
    
    crrev.com/c/5776342 fixed a range `CHECK` in
    `CollectFallbackHintChars`, but depends on the CSS and font
    configurations, it's possible that the code doesn't go to
    `CollectFallbackHintChars` and the following code may hit
    the same issue.
    
    This patch adds another `CHECK` for the case.
    
    Bug: 355731798, 357622693
    Change-Id: Ieb4ada7699c80564e8a4b866cb6a6ffbc665ebc7
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5776204
    Commit-Queue: Kent Tamura <tkent@chromium.org>
    Auto-Submit: Koji Ishii <kojii@chromium.org>
    Reviewed-by: Kent Tamura <tkent@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1340006}

M       third_party/blink/renderer/platform/fonts/shaping/harfbuzz_shaper.cc
M       third_party/blink/renderer/platform/fonts/shaping/harfbuzz_shaper.h

https://chromium-review.googlesource.com/5776204


### ap...@google.com (2024-08-10)

Project: chromium/src
Branch: main

commit ba40b993a6b700a2ad0fd092e141783fb1f60e70
Author: Koji Ishii <kojii@chromium.org>
Date:   Sat Aug 10 03:03:21 2024

    Fix `StringView` to crash when `offset + length` overflows
    
    This patch fixes `SECURITY_DCHECK` in `StringView` for when
    `offset + length` overflows the `unsigned`.
    
    Bug: 357622693, 355731798
    Change-Id: I5a7a7979192fe132496661b1272c5902cdbdb09a
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5775486
    Auto-Submit: Koji Ishii <kojii@chromium.org>
    Commit-Queue: Kent Tamura <tkent@chromium.org>
    Reviewed-by: Kent Tamura <tkent@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1340005}

M       third_party/blink/renderer/platform/wtf/text/string_view.h
M       third_party/blink/renderer/platform/wtf/text/string_view_test.cc

https://chromium-review.googlesource.com/5775486


### pe...@google.com (2024-08-10)

Requesting merge to stable (M127) because latest trunk commit (1340005) appears to be after stable branch point (1313161).
Requesting merge to beta (M128) because latest trunk commit (1340005) appears to be after beta branch point (1331488).
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### 24...@project.gserviceaccount.com (2024-08-10)

ClusterFuzz testcase 5999087214067712 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1339525:1339536

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### pe...@google.com (2024-08-11)

Merge review required: M128 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), pbommana (Desktop)

### pe...@google.com (2024-08-11)

Merge review required: M127 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), alonbajayo (ChromeOS), danielyip (Desktop)

### ap...@google.com (2024-08-11)

Project: chromium/src
Branch: main

commit fc736580458741f5ef3d59d748644190213b7ba7
Author: Alan Cutter <alancutter@google.com>
Date:   Sun Aug 11 23:19:19 2024

    Revert "Fix `StringView` to crash when `offset + length` overflows"
    
    This reverts commit ba40b993a6b700a2ad0fd092e141783fb1f60e70.
    
    Reason for revert: New tests failing on CI.
    First failure https://ci.chromium.org/ui/p/chromium/builders/ci/mac11-arm64-rel-tests/43562/blamelist
    History: https://ci.chromium.org/ui/test/chromium/ninja%3A%2F%2Fthird_party%2Fblink%2Frenderer%2Fplatform%2Fwtf%3Awtf_unittests%2FStringViewTest.OverflowInConstructor
    
    Original change's description:
    > Fix `StringView` to crash when `offset + length` overflows
    >
    > This patch fixes `SECURITY_DCHECK` in `StringView` for when
    > `offset + length` overflows the `unsigned`.
    >
    > Bug: 357622693, 355731798
    > Change-Id: I5a7a7979192fe132496661b1272c5902cdbdb09a
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5775486
    > Auto-Submit: Koji Ishii <kojii@chromium.org>
    > Commit-Queue: Kent Tamura <tkent@chromium.org>
    > Reviewed-by: Kent Tamura <tkent@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#1340005}
    
    Bug: 357622693, 355731798
    Fixed: 358851173
    Change-Id: I6e8a44ce0fa279252268e8064e969c736a0cf11e
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5776005
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Owners-Override: Alan Cutter <alancutter@google.com>
    Commit-Queue: Alan Cutter <alancutter@google.com>
    Cr-Commit-Position: refs/heads/main@{#1340202}

M       third_party/blink/renderer/platform/wtf/text/string_view.h
M       third_party/blink/renderer/platform/wtf/text/string_view_test.cc

https://chromium-review.googlesource.com/5776005


### am...@chromium.org (2024-08-12)

The fix for the overflow related to the security DCHECK for this issue appears to have been reverted, so opening back up to assigned.

### bb...@google.com (2024-08-12)

In addition to the possibility that offset + length could overflow, Do you also have a problem here?

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/wtf/text/string_view.h;l=305?q=blink%2Frenderer%2Fplatform%2Fwtf%2Ftext%2Fstring_view.h&ss=chromium#:~:text=304-,305,-306>

Since I *think* view.Characters16() returns a pointer to a two byte base type, pointer arithmetic will move the pointer forward by twice as many bytes as "offset".

(Edit: Ignore this, I got confused reading the other bits around this - I see you are dealing with offsets in number of characters, not bytes)

### ap...@google.com (2024-08-13)

Project: chromium/src
Branch: main

commit 5fe8d13101707cfe668bab004fe705241a12b11d
Author: Koji Ishii <kojii@chromium.org>
Date:   Tue Aug 13 06:38:43 2024

    Reland "Fix `StringView` to crash when `offset + length` overflows"
    
    This is a reland of commit ba40b993a6b700a2ad0fd092e141783fb1f60e70
    
    The original change failed on mac11-arm64-rel and reverted at
    crrev.com/c/5776005. This is because the unit tests assumed
    that the `SECURITY_DCHECK` is always enabled, but it's
    actually enabled only for DCHECK-enabled builds.
    
    This patch fixes it by wrapping the unit tests by `#if`.
    
    Original change's description:
    > Fix `StringView` to crash when `offset + length` overflows
    >
    > This patch fixes `SECURITY_DCHECK` in `StringView` for when
    > `offset + length` overflows the `unsigned`.
    >
    > Bug: 357622693, 355731798
    > Change-Id: I5a7a7979192fe132496661b1272c5902cdbdb09a
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5775486
    > Auto-Submit: Koji Ishii <kojii@chromium.org>
    > Commit-Queue: Kent Tamura <tkent@chromium.org>
    > Reviewed-by: Kent Tamura <tkent@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#1340005}
    
    Bug: 357622693, 355731798
    Change-Id: I5402234a5fe54bf8dec2c986ab0ab388e1bc783d
    Cq-Include-Trybots: luci.chromium.try:mac11-arm64-rel
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5782718
    Commit-Queue: Koji Ishii <kojii@chromium.org>
    Auto-Submit: Koji Ishii <kojii@chromium.org>
    Reviewed-by: Kentaro Hara <haraken@chromium.org>
    Commit-Queue: Kentaro Hara <haraken@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1340817}

M       third_party/blink/renderer/platform/wtf/text/string_view.h
M       third_party/blink/renderer/platform/wtf/text/string_view_test.cc

https://chromium-review.googlesource.com/5782718


### ko...@chromium.org (2024-08-13)

> 1. Why does your merge fit within the merge criteria for these milestones?

The issue was found after the milestones.

> 2. What changes specifically would you like to merge? Please link to Gerrit.

<https://chromium-review.googlesource.com/c/chromium/src/+/5776342>
<https://chromium-review.googlesource.com/c/chromium/src/+/5776204>
<https://chromium-review.googlesource.com/c/chromium/src/+/5782718>

Note, the last one is a reland after a revert ([comment #22](https://issues.chromium.org/issues/355731798#comment22)), but only unit test code is changed from the original CL ([comment #17](https://issues.chromium.org/issues/355731798#comment17)).

> 3. Have the changes been released and tested on canary?

Yes.

> 4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No.

> 5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>

No.

> 6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No.

### pb...@google.com (2024-08-13)

Approving the Cl to M128 branch, please refer to go/chromebranches for details 

### ap...@google.com (2024-08-13)

Project: chromium/src
Branch: refs/branch-heads/6613

commit 29db4ea6db8b048d8d9db19c1d9043de08f39e8b
Author: Koji Ishii <kojii@chromium.org>
Date:   Tue Aug 13 20:50:58 2024

    [M128] Fix a range `CHECK` for when it overflows
    
    This patch fixes a `CHECK` for a range of a string when
    `offset + length` overflows the `unsigned`.
    
    (cherry picked from commit 59c286e8419f07143ce859342f0fe9ddea36392d)
    
    Bug: 355731798
    Change-Id: If04222f10f2b73b6dcd6b412cf4d82fa5b71bbe2
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5776342
    Commit-Queue: Kent Tamura <tkent@chromium.org>
    Auto-Submit: Koji Ishii <kojii@chromium.org>
    Reviewed-by: Kent Tamura <tkent@chromium.org>
    Commit-Queue: Koji Ishii <kojii@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1339526}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5786215
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6613@{#1022}
    Cr-Branched-From: 03c1799e6f9c7239802827eab5e935b9e14fceae-refs/heads/main@{#1331488}

M       third_party/blink/renderer/platform/fonts/shaping/harfbuzz_shaper.cc
M       third_party/blink/renderer/platform/fonts/shaping/harfbuzz_shaper.h

https://chromium-review.googlesource.com/5786215


### am...@chromium.org (2024-08-13)

Hi -- trying to understand what happened here. It looks like release approved this backmerge of a security fix to M128, but also not all the changes were backmerged to 128 yet so this would not be considered fixed in 128 at this time.

### am...@chromium.org (2024-08-13)

I'm removing review-127 since there are no further planned releases of M127 Stable; re-adding review-128 since the other two CLs need to be reviewed for backporting to M127

### pe...@google.com (2024-08-13)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ap...@google.com (2024-08-13)

Project: chromium/src
Branch: refs/branch-heads/6613

commit 2a8a4af8db4d5f9d4038b16a8f8b5a9932ff0e56
Author: Koji Ishii <kojii@chromium.org>
Date:   Tue Aug 13 22:32:55 2024

    [M128] Check string range in `ShapeSegment`
    
    crrev.com/c/5776342 fixed a range `CHECK` in
    `CollectFallbackHintChars`, but depends on the CSS and font
    configurations, it's possible that the code doesn't go to
    `CollectFallbackHintChars` and the following code may hit
    the same issue.
    
    This patch adds another `CHECK` for the case.
    
    (cherry picked from commit ef6f7b4521bb9e8d0235550c93acf885e198abdb)
    
    Bug: 355731798, 357622693
    Change-Id: Ieb4ada7699c80564e8a4b866cb6a6ffbc665ebc7
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5776204
    Commit-Queue: Kent Tamura <tkent@chromium.org>
    Auto-Submit: Koji Ishii <kojii@chromium.org>
    Reviewed-by: Kent Tamura <tkent@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1340006}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5782722
    Commit-Queue: Koji Ishii <kojii@chromium.org>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6613@{#1030}
    Cr-Branched-From: 03c1799e6f9c7239802827eab5e935b9e14fceae-refs/heads/main@{#1331488}

M       third_party/blink/renderer/platform/fonts/shaping/harfbuzz_shaper.cc
M       third_party/blink/renderer/platform/fonts/shaping/harfbuzz_shaper.h

https://chromium-review.googlesource.com/5782722


### ap...@google.com (2024-08-13)

Project: chromium/src
Branch: refs/branch-heads/6613

commit d0ee2ea9b55f406ce6a298bd2e8b7576b1ee03dc
Author: Koji Ishii <kojii@chromium.org>
Date:   Tue Aug 13 22:57:14 2024

    [M128] Reland "Fix `StringView` to crash when `offset + length` overflows"
    
    This is a reland of commit ba40b993a6b700a2ad0fd092e141783fb1f60e70
    
    The original change failed on mac11-arm64-rel and reverted at
    crrev.com/c/5776005. This is because the unit tests assumed
    that the `SECURITY_DCHECK` is always enabled, but it's
    actually enabled only for DCHECK-enabled builds.
    
    This patch fixes it by wrapping the unit tests by `#if`.
    
    Original change's description:
    > Fix `StringView` to crash when `offset + length` overflows
    >
    > This patch fixes `SECURITY_DCHECK` in `StringView` for when
    > `offset + length` overflows the `unsigned`.
    >
    > Bug: 357622693, 355731798
    > Change-Id: I5a7a7979192fe132496661b1272c5902cdbdb09a
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5775486
    > Auto-Submit: Koji Ishii <kojii@chromium.org>
    > Commit-Queue: Kent Tamura <tkent@chromium.org>
    > Reviewed-by: Kent Tamura <tkent@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#1340005}
    
    (cherry picked from commit 5fe8d13101707cfe668bab004fe705241a12b11d)
    
    Bug: 357622693, 355731798
    Change-Id: I5402234a5fe54bf8dec2c986ab0ab388e1bc783d
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5782718
    Commit-Queue: Koji Ishii <kojii@chromium.org>
    Auto-Submit: Koji Ishii <kojii@chromium.org>
    Reviewed-by: Kentaro Hara <haraken@chromium.org>
    Commit-Queue: Kentaro Hara <haraken@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1340817}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5785423
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6613@{#1032}
    Cr-Branched-From: 03c1799e6f9c7239802827eab5e935b9e14fceae-refs/heads/main@{#1331488}

M       third_party/blink/renderer/platform/wtf/text/string_view.h
M       third_party/blink/renderer/platform/wtf/text/string_view_test.cc

https://chromium-review.googlesource.com/5785423


### ko...@chromium.org (2024-08-14)

All 3 CLs merged to M128.

> Was this issue a regression for the milestone it was found in?

No.

> Is this issue related to a change or feature merged after the latest LTS Milestone?

No.

### sp...@google.com (2024-08-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
report of memory corruption in a sandboxed process / the renderer


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-16)

Congratulations on another one Tashita team! Thank you for your efforts and reporting this issue to us.

### ta...@gmail.com (2024-08-16)

Thanks to all of you for the effort!

### pe...@google.com (2024-08-30)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### pe...@google.com (2024-08-30)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### rz...@google.com (2024-08-30)

1.
For 120:
<https://crrev.com/c/5804714>
<https://crrev.com/c/5807278>
<https://crrev.com/c/5807080>

For 126:
<https://crrev.com/c/5804713>
<https://crrev.com/c/5806849>
<https://crrev.com/c/5807454>

2. Low, no conflicts
3. 128
4. Yes

### ap...@google.com (2024-09-12)

Project: chromium/src
Branch: refs/branch-heads/6099

commit 9d1abeb3ca5059abfbc589b3054b0befa936114a
Author: Koji Ishii <kojii@chromium.org>
Date:   Thu Sep 12 05:42:18 2024

    [M120-LTS] Fix a range `CHECK` for when it overflows
    
    This patch fixes a `CHECK` for a range of a string when
    `offset + length` overflows the `unsigned`.
    
    (cherry picked from commit 59c286e8419f07143ce859342f0fe9ddea36392d)
    
    Bug: 355731798
    Change-Id: If04222f10f2b73b6dcd6b412cf4d82fa5b71bbe2
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5776342
    Commit-Queue: Kent Tamura <tkent@chromium.org>
    Auto-Submit: Koji Ishii <kojii@chromium.org>
    Commit-Queue: Koji Ishii <kojii@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1339526}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5804714
    Auto-Submit: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com>
    Reviewed-by: Koji Ishii <kojii@chromium.org>
    Reviewed-by: Fahad Mansoor <fahadmansoor@google.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#2072}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

M       third_party/blink/renderer/platform/fonts/shaping/harfbuzz_shaper.cc
M       third_party/blink/renderer/platform/fonts/shaping/harfbuzz_shaper.h

https://chromium-review.googlesource.com/5804714


### ap...@google.com (2024-09-12)

Project: chromium/src
Branch: refs/branch-heads/6478

commit 523bb6a799c8ee5a6c419e395125de8c9ae0a323
Author: Koji Ishii <kojii@chromium.org>
Date:   Thu Sep 12 05:51:00 2024

    [M126-LTS] Fix a range `CHECK` for when it overflows
    
    This patch fixes a `CHECK` for a range of a string when
    `offset + length` overflows the `unsigned`.
    
    (cherry picked from commit 59c286e8419f07143ce859342f0fe9ddea36392d)
    
    Bug: 355731798
    Change-Id: If04222f10f2b73b6dcd6b412cf4d82fa5b71bbe2
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5776342
    Commit-Queue: Kent Tamura <tkent@chromium.org>
    Auto-Submit: Koji Ishii <kojii@chromium.org>
    Commit-Queue: Koji Ishii <kojii@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1339526}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5804713
    Reviewed-by: Koji Ishii <kojii@chromium.org>
    Reviewed-by: Fahad Mansoor <fahadmansoor@google.com>
    Auto-Submit: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com>
    Cr-Commit-Position: refs/branch-heads/6478@{#1958}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       third_party/blink/renderer/platform/fonts/shaping/harfbuzz_shaper.cc
M       third_party/blink/renderer/platform/fonts/shaping/harfbuzz_shaper.h

https://chromium-review.googlesource.com/5804713


### ap...@google.com (2024-09-12)

Project: chromium/src
Branch: refs/branch-heads/6478

commit edb5557256cd5e2632e223405557969b7a8fd3b2
Author: Koji Ishii <kojii@chromium.org>
Date:   Thu Sep 12 06:00:02 2024

    [M126-LTS] Check string range in `ShapeSegment`
    
    crrev.com/c/5776342 fixed a range `CHECK` in
    `CollectFallbackHintChars`, but depends on the CSS and font
    configurations, it's possible that the code doesn't go to
    `CollectFallbackHintChars` and the following code may hit
    the same issue.
    
    This patch adds another `CHECK` for the case.
    
    (cherry picked from commit ef6f7b4521bb9e8d0235550c93acf885e198abdb)
    
    Bug: 355731798, 357622693
    Change-Id: Ieb4ada7699c80564e8a4b866cb6a6ffbc665ebc7
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5776204
    Commit-Queue: Kent Tamura <tkent@chromium.org>
    Auto-Submit: Koji Ishii <kojii@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1340006}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5806849
    Auto-Submit: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com>
    Commit-Queue: Koji Ishii <kojii@chromium.org>
    Reviewed-by: Fernando Serboncini <fserb@chromium.org>
    Reviewed-by: Fahad Mansoor <fahadmansoor@google.com>
    Reviewed-by: Koji Ishii <kojii@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6478@{#1959}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       third_party/blink/renderer/platform/fonts/shaping/harfbuzz_shaper.cc
M       third_party/blink/renderer/platform/fonts/shaping/harfbuzz_shaper.h

https://chromium-review.googlesource.com/5806849


### ap...@google.com (2024-09-12)

Project: chromium/src
Branch: refs/branch-heads/6478

commit 58e0db4c9fcfde64e46b659202b4a979bd0e68b9
Author: Koji Ishii <kojii@chromium.org>
Date:   Thu Sep 12 06:17:42 2024

    [M126-LTS] Reland "Fix `StringView` to crash when `offset + length` overflows"
    
    This is a reland of commit ba40b993a6b700a2ad0fd092e141783fb1f60e70
    
    The original change failed on mac11-arm64-rel and reverted at
    crrev.com/c/5776005. This is because the unit tests assumed
    that the `SECURITY_DCHECK` is always enabled, but it's
    actually enabled only for DCHECK-enabled builds.
    
    This patch fixes it by wrapping the unit tests by `#if`.
    
    Original change's description:
    > Fix `StringView` to crash when `offset + length` overflows
    >
    > This patch fixes `SECURITY_DCHECK` in `StringView` for when
    > `offset + length` overflows the `unsigned`.
    >
    > Bug: 357622693, 355731798
    > Change-Id: I5a7a7979192fe132496661b1272c5902cdbdb09a
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5775486
    > Auto-Submit: Koji Ishii <kojii@chromium.org>
    > Commit-Queue: Kent Tamura <tkent@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#1340005}
    
    (cherry picked from commit 5fe8d13101707cfe668bab004fe705241a12b11d)
    
    Bug: 357622693, 355731798
    Change-Id: I5402234a5fe54bf8dec2c986ab0ab388e1bc783d
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5782718
    Commit-Queue: Koji Ishii <kojii@chromium.org>
    Auto-Submit: Koji Ishii <kojii@chromium.org>
    Commit-Queue: Kentaro Hara <haraken@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1340817}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5807454
    Auto-Submit: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com>
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
    Reviewed-by: Fahad Mansoor <fahadmansoor@google.com>
    Reviewed-by: Koji Ishii <kojii@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6478@{#1960}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       third_party/blink/renderer/platform/wtf/text/string_view.h
M       third_party/blink/renderer/platform/wtf/text/string_view_test.cc

https://chromium-review.googlesource.com/5807454


### ap...@google.com (2024-09-12)

Project: chromium/src
Branch: refs/branch-heads/6099

commit 19d9307f10c2729047d1120b34f256e13f042af0
Author: Koji Ishii <kojii@chromium.org>
Date:   Thu Sep 12 11:33:16 2024

    [M120-LTS] Reland "Fix `StringView` to crash when `offset + length` overflows"
    
    This is a reland of commit ba40b993a6b700a2ad0fd092e141783fb1f60e70
    
    The original change failed on mac11-arm64-rel and reverted at
    crrev.com/c/5776005. This is because the unit tests assumed
    that the `SECURITY_DCHECK` is always enabled, but it's
    actually enabled only for DCHECK-enabled builds.
    
    This patch fixes it by wrapping the unit tests by `#if`.
    
    Original change's description:
    > Fix `StringView` to crash when `offset + length` overflows
    >
    > This patch fixes `SECURITY_DCHECK` in `StringView` for when
    > `offset + length` overflows the `unsigned`.
    >
    > Bug: 357622693, 355731798
    > Change-Id: I5a7a7979192fe132496661b1272c5902cdbdb09a
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5775486
    > Auto-Submit: Koji Ishii <kojii@chromium.org>
    > Commit-Queue: Kent Tamura <tkent@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#1340005}
    
    (cherry picked from commit 5fe8d13101707cfe668bab004fe705241a12b11d)
    
    Bug: 357622693, 355731798
    Change-Id: I5402234a5fe54bf8dec2c986ab0ab388e1bc783d
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5782718
    Commit-Queue: Koji Ishii <kojii@chromium.org>
    Auto-Submit: Koji Ishii <kojii@chromium.org>
    Commit-Queue: Kentaro Hara <haraken@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1340817}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5807080
    Reviewed-by: Fahad Mansoor <fahadmansoor@google.com>
    Reviewed-by: Koji Ishii <kojii@chromium.org>
    Reviewed-by: Kentaro Hara <haraken@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099@{#2074}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

M       third_party/blink/renderer/platform/wtf/text/string_view.h
M       third_party/blink/renderer/platform/wtf/text/string_view_test.cc

https://chromium-review.googlesource.com/5807080


### ap...@google.com (2024-09-12)

Project: chromium/src
Branch: refs/branch-heads/6099

commit 99c4b54620413d363cb138f78e3d5576848a873b
Author: Koji Ishii <kojii@chromium.org>
Date:   Thu Sep 12 11:33:07 2024

    [M120-LTS] Check string range in `ShapeSegment`
    
    crrev.com/c/5776342 fixed a range `CHECK` in
    `CollectFallbackHintChars`, but depends on the CSS and font
    configurations, it's possible that the code doesn't go to
    `CollectFallbackHintChars` and the following code may hit
    the same issue.
    
    This patch adds another `CHECK` for the case.
    
    (cherry picked from commit ef6f7b4521bb9e8d0235550c93acf885e198abdb)
    
    Bug: 355731798, 357622693
    Change-Id: Ieb4ada7699c80564e8a4b866cb6a6ffbc665ebc7
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5776204
    Commit-Queue: Kent Tamura <tkent@chromium.org>
    Auto-Submit: Koji Ishii <kojii@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1340006}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5807278
    Reviewed-by: Fahad Mansoor <fahadmansoor@google.com>
    Reviewed-by: Koji Ishii <kojii@chromium.org>
    Auto-Submit: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com>
    Commit-Queue: Koji Ishii <kojii@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099@{#2073}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

M       third_party/blink/renderer/platform/fonts/shaping/harfbuzz_shaper.cc
M       third_party/blink/renderer/platform/fonts/shaping/harfbuzz_shaper.h

https://chromium-review.googlesource.com/5807278


### ap...@google.com (2024-09-17)

Project: chromium/src
Branch: refs/branch-heads/6478_182

commit 7b42385f48a64d6e20b09f5fb178c39c6f30095a
Author: Koji Ishii <kojii@chromium.org>
Date:   Tue Sep 17 15:39:10 2024

    [CfM-R126] Reland "Fix `StringView` to crash when `offset + length` overflows"
    
    This is a reland of commit ba40b993a6b700a2ad0fd092e141783fb1f60e70
    
    The original change failed on mac11-arm64-rel and reverted at
    crrev.com/c/5776005. This is because the unit tests assumed
    that the `SECURITY_DCHECK` is always enabled, but it's
    actually enabled only for DCHECK-enabled builds.
    
    This patch fixes it by wrapping the unit tests by `#if`.
    
    Original change's description:
    > Fix `StringView` to crash when `offset + length` overflows
    >
    > This patch fixes `SECURITY_DCHECK` in `StringView` for when
    > `offset + length` overflows the `unsigned`.
    >
    > Bug: 357622693, 355731798
    > Change-Id: I5a7a7979192fe132496661b1272c5902cdbdb09a
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5775486
    > Auto-Submit: Koji Ishii <kojii@chromium.org>
    > Commit-Queue: Kent Tamura <tkent@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#1340005}
    
    (cherry picked from commit 5fe8d13101707cfe668bab004fe705241a12b11d)
    
    (cherry picked from commit 58e0db4c9fcfde64e46b659202b4a979bd0e68b9)
    
    Bug: 357622693, 355731798
    Change-Id: I5402234a5fe54bf8dec2c986ab0ab388e1bc783d
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5782718
    Commit-Queue: Koji Ishii <kojii@chromium.org>
    Auto-Submit: Koji Ishii <kojii@chromium.org>
    Commit-Queue: Kentaro Hara <haraken@chromium.org>
    Cr-Original-Original-Commit-Position: refs/heads/main@{#1340817}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5807454
    Auto-Submit: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com>
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
    Reviewed-by: Fahad Mansoor <fahadmansoor@google.com>
    Reviewed-by: Koji Ishii <kojii@chromium.org>
    Cr-Original-Commit-Position: refs/branch-heads/6478@{#1960}
    Cr-Original-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5869442
    Owners-Override: Kyle Williams <kdgwill@chromium.org>
    Commit-Queue: Kyle Williams <kdgwill@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6478_182@{#76}
    Cr-Branched-From: 5b5d8292ddf182f8b2096fa665b473b6317906d5-refs/branch-heads/6478@{#1776}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       third_party/blink/renderer/platform/wtf/text/string_view.h
M       third_party/blink/renderer/platform/wtf/text/string_view_test.cc

https://chromium-review.googlesource.com/5869442


### ap...@google.com (2024-09-17)

Project: chromium/src
Branch: refs/branch-heads/6478_182

commit 8fc707e39a242c56459b18d0fe5aead57de5c776
Author: Koji Ishii <kojii@chromium.org>
Date:   Tue Sep 17 15:38:18 2024

    [CfM-R126] Check string range in `ShapeSegment`
    
    crrev.com/c/5776342 fixed a range `CHECK` in
    `CollectFallbackHintChars`, but depends on the CSS and font
    configurations, it's possible that the code doesn't go to
    `CollectFallbackHintChars` and the following code may hit
    the same issue.
    
    This patch adds another `CHECK` for the case.
    
    (cherry picked from commit ef6f7b4521bb9e8d0235550c93acf885e198abdb)
    
    (cherry picked from commit edb5557256cd5e2632e223405557969b7a8fd3b2)
    
    Bug: 355731798, 357622693
    Change-Id: Ieb4ada7699c80564e8a4b866cb6a6ffbc665ebc7
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5776204
    Commit-Queue: Kent Tamura <tkent@chromium.org>
    Auto-Submit: Koji Ishii <kojii@chromium.org>
    Cr-Original-Original-Commit-Position: refs/heads/main@{#1340006}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5806849
    Auto-Submit: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com>
    Commit-Queue: Koji Ishii <kojii@chromium.org>
    Reviewed-by: Fernando Serboncini <fserb@chromium.org>
    Reviewed-by: Fahad Mansoor <fahadmansoor@google.com>
    Reviewed-by: Koji Ishii <kojii@chromium.org>
    Cr-Original-Commit-Position: refs/branch-heads/6478@{#1959}
    Cr-Original-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5869441
    Commit-Queue: Kyle Williams <kdgwill@chromium.org>
    Owners-Override: Kyle Williams <kdgwill@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6478_182@{#75}
    Cr-Branched-From: 5b5d8292ddf182f8b2096fa665b473b6317906d5-refs/branch-heads/6478@{#1776}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       third_party/blink/renderer/platform/fonts/shaping/harfbuzz_shaper.cc
M       third_party/blink/renderer/platform/fonts/shaping/harfbuzz_shaper.h

https://chromium-review.googlesource.com/5869441


### ap...@google.com (2024-09-17)

Project: chromium/src
Branch: refs/branch-heads/6478_182

commit 1ad61cc6c14ef78a7c8fd589dcb759654fab6e47
Author: Koji Ishii <kojii@chromium.org>
Date:   Tue Sep 17 15:38:02 2024

    [CfM-R126] Fix a range `CHECK` for when it overflows
    
    This patch fixes a `CHECK` for a range of a string when
    `offset + length` overflows the `unsigned`.
    
    (cherry picked from commit 59c286e8419f07143ce859342f0fe9ddea36392d)
    
    (cherry picked from commit 523bb6a799c8ee5a6c419e395125de8c9ae0a323)
    
    Bug: 355731798
    Change-Id: If04222f10f2b73b6dcd6b412cf4d82fa5b71bbe2
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5776342
    Commit-Queue: Kent Tamura <tkent@chromium.org>
    Auto-Submit: Koji Ishii <kojii@chromium.org>
    Commit-Queue: Koji Ishii <kojii@chromium.org>
    Cr-Original-Original-Commit-Position: refs/heads/main@{#1339526}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5804713
    Reviewed-by: Koji Ishii <kojii@chromium.org>
    Reviewed-by: Fahad Mansoor <fahadmansoor@google.com>
    Auto-Submit: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com>
    Cr-Original-Commit-Position: refs/branch-heads/6478@{#1958}
    Cr-Original-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5869440
    Owners-Override: Kyle Williams <kdgwill@chromium.org>
    Commit-Queue: Kyle Williams <kdgwill@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6478_182@{#74}
    Cr-Branched-From: 5b5d8292ddf182f8b2096fa665b473b6317906d5-refs/branch-heads/6478@{#1776}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       third_party/blink/renderer/platform/fonts/shaping/harfbuzz_shaper.cc
M       third_party/blink/renderer/platform/fonts/shaping/harfbuzz_shaper.h

https://chromium-review.googlesource.com/5869440


### pe...@google.com (2024-11-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/355731798)*
