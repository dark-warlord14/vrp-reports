# AddressSanitizer: heap-buffer-overflow

| Field | Value |
|-------|-------|
| **Issue ID** | [352467338](https://issues.chromium.org/issues/352467338) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Platforms** | Linux |
| **Reporter** | ta...@gmail.com |
| **Assignee** | tk...@chromium.org |
| **Created** | 2024-07-11 |
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

## Summary Behaviour:

126.0.6478.126 Latest Chrome Release Official Build (Linux):

- Testcase heap-buffer-overflow.html: `Render Process Crash`.
- Testcase vector-overflow-variant.html: `Render Process Crash`.

127.0.6533.2 Developer Build Debug (Linux):

- Testcase heap-buffer-overflow.html: `vector.h(1190) Check failed: i < size() (2863311530 vs. 2)`
- Testcase vector-overflow-variant.html: `vector.h(1190) Check failed: i < size() (2 vs. 2)`

128.0.6588.0 Developer Build ASAN (Linux):

- Testcase heap-buffer-overflow.html: `AddressSanitizer: heap-buffer-overflow`
- Testcase vector-overflow-variant.html: `vector.h(1182) Check failed: i < size() (2 vs. 2)`

## Vulnerability Details:

### Analysis of the testcase: heap-buffer-overflow.html

Version and OS: 127.0.6533.2 (Developer Build) (64-bit) (Linux) DEBUG

Multiple DChecks:

1)

```
[1353857:1:0711/111512.736019:FATAL:ruby_utils.cc(1053)] Check failed: false.  LogicalLineItems::size()=2 LogicalRubyColumn::start_index=2863311530

```
```
void UpdateRubyColumnInlinePositions(
    const LogicalLineItems& line_items,
    LayoutUnit inline_size,
    HeapVector<Member<LogicalRubyColumn>>& column_list) {
  DCHECK(RuntimeEnabledFeatures::RubyLineBreakableEnabled());
  for (auto& column : column_list) {
    LayoutUnit inline_offset;
    wtf_size_t start_index = column->start_index; // [1] column->start_index is 0xaaaaaaaa (2863311530)
    if (start_index < line_items.size()) {
      inline_offset = line_items[start_index].rect.offset.inline_offset;
    } else if (start_index == line_items.size()) {
      if (line_items.size() > 0) {
        const LogicalLineItem& last_item = line_items[start_index - 1];
        inline_offset = last_item.rect.offset.inline_offset +
                        last_item.rect.InlineEndOffset();
      } else {
        inline_offset = inline_size;
      }
    } else {
      NOTREACHED_IN_MIGRATION()
          << " LogicalLineItems::size()=" << line_items.size()
          << " LogicalRubyColumn::start_index=" << start_index;
    }
    // TODO(crbug.com/324111880): Handle overhang.
    column->annotation_items->MoveInInlineDirection(inline_offset);
    column->state_stack.MoveBoxDataInInlineDirection(inline_offset);
    UpdateRubyColumnInlinePositions(*column->annotation_items, inline_size,
                                    column->RubyColumnList());
  }
}

```

The function `UpdateRubyColumnInlinePositions` is called 3 times before hitting the `NOTREACHED_IN_MIGRATION` Assert. The message printed is:

```
Check failed: false.  LogicalLineItems::size()=2 LogicalRubyColumn::start_index=2863311530

```

After debugging, it seems the first item of the `HeapVector column_list` is not properly initialized as at [1], `start_index` is set as `0xaaaaaaaa` value which breaks the logic and leading to multiple Debug Checks/Segmentation Faults, and as demostrated on 128.0.6588.0 to a Heap-Buffer-Overflow.

Under observations, it could be that the decompression of `column->start_index` fails and sets the default value `0xaaaaaaaa` of the Debug Build.

The argument `column_list` receives the value of `HeapVector<Member<LogicalRubyColumn>> ruby_column_list_;` declared at `inline_box_state.h`.

---

### Analysis of the testcase: vector-overflow-variant.html

Version and OS: 127.0.6533.2 (Developer Build) (64-bit) (Linux) DEBUG

Multiple DChecks:

1)

```
[FATAL:vector.h(1190)] Check failed: i < size() (2 vs. 2)

```

This testcase affects the code in the function:

```
void InlineLayoutStateStack::ApplyRelativePositioning(
    const ConstraintSpace& space,
    LogicalLineItems* line_box,
    const LogicalOffset* parent_offset) {

  ...
  ...

  for (auto& logical_column : ruby_column_list_) {
    logical_column->state_stack.ApplyRelativePositioning(
        space, logical_column->annotation_items,
        &accumulated_offsets[logical_column->start_index]); // [1]
  }
}

```

`logical_column->start_index` ([1]) returns a value that is outside the Vector, ending on a Check. `logical_column` is an item of `ruby_column_list_`. The problem points to the `ruby_column_list_` seen in the previous testcase analysis.

---

NOTE:

We believe the Heap-Buffer-Overflow could be also reached by a crafted testcase on Chrome >= 127.x.x.x. The commit `1e3eda9848f805762eaaa0258d1d2531d0c29db1` introduced the code in the function `LogicalLineBuilder::BidiReorder` where the overflow happens.

VERSION
Chrome Version: >= 126.0.6478.127 (release) until the latest commit.
Operating System: Tested on Linux. Other OS could be potentially affected

REPRODUCTION CASE

- heap-buffer-overflow.html
- vector-overflow-variant.html

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash:

- Signal 11. Segmentation Fault
- Vector OOB Check
- AddressSanitizer: HeapOverflow

## Full Logs:

126.0.6478.126 (Official Build) (64-bit) (Linux)

heap-buffer-overflow.html

Render Process Crash.

--

vector-overflow-variant.html

Render Process Crash.

---

127.0.6533.2 (Developer Build) (64-bit) (Linux) DEBUG

heap-buffer-overflow.html

```
[1348590:1:0710/191205.927618:FATAL:vector.h(1190)] Check failed: i < size() (2863311530 vs. 2)
#0 0x7f0b3d7c411c base::debug::CollectStackTrace() [../../base/debug/stack_trace_posix.cc:1044:7]
#1 0x7f0b3d7760cb base::debug::StackTrace::StackTrace() [../../base/debug/stack_trace.cc:242:20]
#2 0x7f0b3d776065 base::debug::StackTrace::StackTrace() [../../base/debug/stack_trace.cc:237:28]
#3 0x7f0b3d4a7b0f logging::LogMessage::Flush() [../../base/logging.cc:714:29]
#4 0x7f0b3d4a7a37 logging::LogMessage::~LogMessage() [../../base/logging.cc:702:3]
#5 0x7f0b3d450ca5 logging::(anonymous namespace)::CheckLogMessage::~CheckLogMessage() [../../base/check.cc:186:3]
#6 0x7f0b3d450cc9 logging::(anonymous namespace)::CheckLogMessage::~CheckLogMessage() [../../base/check.cc:181:31]
#7 0x7f0b3d451d78 std::__Cr::default_delete<>::operator()() [../../third_party/libc++/src/include/__memory/unique_ptr.h:67:5]
#8 0x7f0b3d4512f6 std::__Cr::unique_ptr<>::reset() [../../third_party/libc++/src/include/__memory/unique_ptr.h:278:7]
#9 0x7f0b3d45093d logging::CheckError::~CheckError() [../../base/check.cc:350:16]
#10 0x7f0b025ca541 WTF::Vector<>::at() [../../third_party/blink/renderer/platform/wtf/vector.h:1190:5]
#11 0x7f0b025bb68b WTF::Vector<>::operator[]() [../../third_party/blink/renderer/platform/wtf/vector.h:1198:40]
#12 0x7f0b025b4de3 blink::InlineLayoutStateStack::ApplyRelativePositioning() [../../third_party/blink/renderer/core/layout/inline/inline_box_state.cc:907:10]
#13 0x7f0b0260bcdb blink::InlineLayoutAlgorithm::CreateLine() [../../third_party/blink/renderer/core/layout/inline/inline_layout_algorithm.cc:535:16]
#14 0x7f0b0260fae1 blink::InlineLayoutAlgorithm::Layout() [../../third_party/blink/renderer/core/layout/inline/inline_layout_algorithm.cc:1245:5]
#15 0x7f0b026230cd blink::InlineNode::Layout() [../../third_party/blink/renderer/core/layout/inline/inline_node.cc:1673:20]
#16 0x7f0b023e9bfb blink::(anonymous namespace)::LayoutInflow() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:125:25]
#17 0x7f0b023e9b05 blink::BlockLayoutAlgorithm::HandleInflow() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:2040:7]
#18 0x7f0b023f07e8 blink::BlockLayoutAlgorithm::Layout() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:921:18]
#19 0x7f0b023e0bf3 blink::BlockLayoutAlgorithm::LayoutWithSimpleInlineChildLayoutContext() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:568:32]
#20 0x7f0b023dfe5f blink::BlockLayoutAlgorithm::LayoutInlineChild() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:561:10]
#21 0x7f0b023dfd2a blink::BlockLayoutAlgorithm::Layout() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:499:14]
#22 0x7f0b02411e61 _ZZN5blink12_GLOBAL__N_119LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEENKUlTyPT_E_clINS_20BlockLayoutAlgorithmEEEDaS5_ [../../third_party/blink/renderer/core/layout/block_node.cc:209:50]
#23 0x7f0b02411369 _ZN5blink12_GLOBAL__N_121CreateAlgorithmAndRunINS_20BlockLayoutAlgorithmEZNS0_19LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEEUlTyPT_E_EEvS5_RKT0_ [../../third_party/blink/renderer/core/layout/block_node.cc:117:3]
#24 0x7f0b024109c2 _ZN5blink12_GLOBAL__N_124DetermineAlgorithmAndRunIZNS0_19LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEEUlTyPT_E_EEvS4_RKS5_ [../../third_party/blink/renderer/core/layout/block_node.cc:200:5]
#25 0x7f0b0240a7d7 blink::(anonymous namespace)::LayoutWithAlgorithm() [../../third_party/blink/renderer/core/layout/block_node.cc:207:3]
#26 0x7f0b02408f81 blink::BlockNode::Layout() [../../third_party/blink/renderer/core/layout/block_node.cc:464:21]
#27 0x7f0b023e9417 blink::(anonymous namespace)::LayoutBlockChild() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:113:16]
#28 0x7f0b023e9c42 blink::(anonymous namespace)::LayoutInflow() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:128:10]
#29 0x7f0b023e9b05 blink::BlockLayoutAlgorithm::HandleInflow() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:2040:7]
#30 0x7f0b023f07e8 blink::BlockLayoutAlgorithm::Layout() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:921:18]
#31 0x7f0b023dfd3d blink::BlockLayoutAlgorithm::Layout() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:501:14]
#32 0x7f0b02411e61 _ZZN5blink12_GLOBAL__N_119LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEENKUlTyPT_E_clINS_20BlockLayoutAlgorithmEEEDaS5_ [../../third_party/blink/renderer/core/layout/block_node.cc:209:50]
#33 0x7f0b02411369 _ZN5blink12_GLOBAL__N_121CreateAlgorithmAndRunINS_20BlockLayoutAlgorithmEZNS0_19LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEEUlTyPT_E_EEvS5_RKT0_ [../../third_party/blink/renderer/core/layout/block_node.cc:117:3]
#34 0x7f0b024109c2 _ZN5blink12_GLOBAL__N_124DetermineAlgorithmAndRunIZNS0_19LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEEUlTyPT_E_EEvS4_RKS5_ [../../third_party/blink/renderer/core/layout/block_node.cc:200:5]
#35 0x7f0b0240a7d7 blink::(anonymous namespace)::LayoutWithAlgorithm() [../../third_party/blink/renderer/core/layout/block_node.cc:207:3]
#36 0x7f0b02408f81 blink::BlockNode::Layout() [../../third_party/blink/renderer/core/layout/block_node.cc:464:21]
#37 0x7f0b023e9417 blink::(anonymous namespace)::LayoutBlockChild() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:113:16]
#38 0x7f0b023e66a1 blink::BlockLayoutAlgorithm::LayoutNewFormattingContext() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1854:41]
#39 0x7f0b023e4ee3 blink::BlockLayoutAlgorithm::HandleNewFormattingContext() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1646:39]
#40 0x7f0b023f0796 blink::BlockLayoutAlgorithm::Layout() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:916:18]
#41 0x7f0b023dfd3d blink::BlockLayoutAlgorithm::Layout() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:501:14]
#42 0x7f0b02411e61 _ZZN5blink12_GLOBAL__N_119LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEENKUlTyPT_E_clINS_20BlockLayoutAlgorithmEEEDaS5_ [../../third_party/blink/renderer/core/layout/block_node.cc:209:50]
#43 0x7f0b02411369 _ZN5blink12_GLOBAL__N_121CreateAlgorithmAndRunINS_20BlockLayoutAlgorithmEZNS0_19LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEEUlTyPT_E_EEvS5_RKT0_ [../../third_party/blink/renderer/core/layout/block_node.cc:117:3]
#44 0x7f0b024109c2 _ZN5blink12_GLOBAL__N_124DetermineAlgorithmAndRunIZNS0_19LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEEUlTyPT_E_EEvS4_RKS5_ [../../third_party/blink/renderer/core/layout/block_node.cc:200:5]
#45 0x7f0b0240a7d7 blink::(anonymous namespace)::LayoutWithAlgorithm() [../../third_party/blink/renderer/core/layout/block_node.cc:207:3]
#46 0x7f0b02408f81 blink::BlockNode::Layout() [../../third_party/blink/renderer/core/layout/block_node.cc:464:21]
#47 0x7f0b027bf254 blink::LayoutView::LayoutRoot() [../../third_party/blink/renderer/core/layout/layout_view.cc:810:19]
#48 0x7f0b0193a171 blink::LocalFrameView::PerformLayout() [../../third_party/blink/renderer/core/frame/local_frame_view.cc:783:24]
#49 0x7f0b0193b37f blink::LocalFrameView::UpdateLayout() [../../third_party/blink/renderer/core/frame/local_frame_view.cc:842:3]
#50 0x7f0b0194e846 blink::LocalFrameView::UpdateStyleAndLayoutInternal() [../../third_party/blink/renderer/core/frame/local_frame_view.cc:3171:7]
#51 0x7f0b01940070 blink::LocalFrameView::UpdateStyleAndLayout() [../../third_party/blink/renderer/core/frame/local_frame_view.cc:3101:18]
#52 0x7f0b03550c2f blink::Document::UpdateStyleAndLayout() [../../third_party/blink/renderer/core/dom/document.cc:2821:17]
#53 0x7f0b0355ad2f blink::Document::ImplicitClose() [../../third_party/blink/renderer/core/dom/document.cc:3986:7]
#54 0x7f0b0355b2b4 blink::Document::CheckCompletedInternal() [../../third_party/blink/renderer/core/dom/document.cc:4075:5]
#55 0x7f0b0355aa69 blink::Document::CheckCompleted() [../../third_party/blink/renderer/core/dom/document.cc:4037:7]
#56 0x7f0b029e94e4 blink::FrameLoader::FinishedParsing() [../../third_party/blink/renderer/core/loader/frame_loader.cc:448:26]
#57 0x7f0b03571e69 blink::Document::FinishedParsing() [../../third_party/blink/renderer/core/dom/document.cc:7485:21]
#58 0x7f0b036925a1 blink::HTMLConstructionSite::FinishedParsing() [../../third_party/blink/renderer/core/html/parser/html_construction_site.cc:757:14]
#59 0x7f0b0373a82d blink::HTMLTreeBuilder::Finished() [../../third_party/blink/renderer/core/html/parser/html_tree_builder.cc:3162:9]
#60 0x7f0b036ae500 blink::HTMLDocumentParser::end() [../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:1075:18]
#61 0x7f0b036a8347 blink::HTMLDocumentParser::AttemptToRunDeferredScriptsAndEnd() [../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:1088:3]
#62 0x7f0b036a7a28 blink::HTMLDocumentParser::PrepareToStopParsing() [../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:566:3]
#63 0x7f0b036ab39b blink::HTMLDocumentParser::AttemptToEnd() [../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:1112:3]
#64 0x7f0b036a7fd5 blink::HTMLDocumentParser::PumpTokenizerIfPossible() [../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:651:5]
#65 0x7f0b036a8a4a blink::HTMLDocumentParser::DeferredPumpTokenizerIfPossible() [../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:620:7]

```

--

vector-overflow-variant.html

```
[1348659:1:0710/191318.499065:FATAL:vector.h(1190)] Check failed: i < size() (2 vs. 2)
#0 0x7f0b3d7c411c base::debug::CollectStackTrace() [../../base/debug/stack_trace_posix.cc:1044:7]
#1 0x7f0b3d7760cb base::debug::StackTrace::StackTrace() [../../base/debug/stack_trace.cc:242:20]
#2 0x7f0b3d776065 base::debug::StackTrace::StackTrace() [../../base/debug/stack_trace.cc:237:28]
#3 0x7f0b3d4a7b0f logging::LogMessage::Flush() [../../base/logging.cc:714:29]
#4 0x7f0b3d4a7a37 logging::LogMessage::~LogMessage() [../../base/logging.cc:702:3]
#5 0x7f0b3d450ca5 logging::(anonymous namespace)::CheckLogMessage::~CheckLogMessage() [../../base/check.cc:186:3]
#6 0x7f0b3d450cc9 logging::(anonymous namespace)::CheckLogMessage::~CheckLogMessage() [../../base/check.cc:181:31]
#7 0x7f0b3d451d78 std::__Cr::default_delete<>::operator()() [../../third_party/libc++/src/include/__memory/unique_ptr.h:67:5]
#8 0x7f0b3d4512f6 std::__Cr::unique_ptr<>::reset() [../../third_party/libc++/src/include/__memory/unique_ptr.h:278:7]
#9 0x7f0b3d45093d logging::CheckError::~CheckError() [../../base/check.cc:350:16]
#10 0x7f0b025ca541 WTF::Vector<>::at() [../../third_party/blink/renderer/platform/wtf/vector.h:1190:5]
#11 0x7f0b025bb68b WTF::Vector<>::operator[]() [../../third_party/blink/renderer/platform/wtf/vector.h:1198:40]
#12 0x7f0b025b4de3 blink::InlineLayoutStateStack::ApplyRelativePositioning() [../../third_party/blink/renderer/core/layout/inline/inline_box_state.cc:907:10]
#13 0x7f0b0260bcdb blink::InlineLayoutAlgorithm::CreateLine() [../../third_party/blink/renderer/core/layout/inline/inline_layout_algorithm.cc:535:16]
#14 0x7f0b0260fae1 blink::InlineLayoutAlgorithm::Layout() [../../third_party/blink/renderer/core/layout/inline/inline_layout_algorithm.cc:1245:5]
#15 0x7f0b026230cd blink::InlineNode::Layout() [../../third_party/blink/renderer/core/layout/inline/inline_node.cc:1673:20]
#16 0x7f0b023e9bfb blink::(anonymous namespace)::LayoutInflow() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:125:25]
#17 0x7f0b023e9b05 blink::BlockLayoutAlgorithm::HandleInflow() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:2040:7]
#18 0x7f0b023f07e8 blink::BlockLayoutAlgorithm::Layout() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:921:18]
#19 0x7f0b023e0bf3 blink::BlockLayoutAlgorithm::LayoutWithSimpleInlineChildLayoutContext() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:568:32]
#20 0x7f0b023dfe5f blink::BlockLayoutAlgorithm::LayoutInlineChild() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:561:10]
#21 0x7f0b023dfd2a blink::BlockLayoutAlgorithm::Layout() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:499:14]
#22 0x7f0b02411e61 _ZZN5blink12_GLOBAL__N_119LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEENKUlTyPT_E_clINS_20BlockLayoutAlgorithmEEEDaS5_ [../../third_party/blink/renderer/core/layout/block_node.cc:209:50]
#23 0x7f0b02411369 _ZN5blink12_GLOBAL__N_121CreateAlgorithmAndRunINS_20BlockLayoutAlgorithmEZNS0_19LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEEUlTyPT_E_EEvS5_RKT0_ [../../third_party/blink/renderer/core/layout/block_node.cc:117:3]
#24 0x7f0b024109c2 _ZN5blink12_GLOBAL__N_124DetermineAlgorithmAndRunIZNS0_19LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEEUlTyPT_E_EEvS4_RKS5_ [../../third_party/blink/renderer/core/layout/block_node.cc:200:5]
#25 0x7f0b0240a7d7 blink::(anonymous namespace)::LayoutWithAlgorithm() [../../third_party/blink/renderer/core/layout/block_node.cc:207:3]
#26 0x7f0b02408f81 blink::BlockNode::Layout() [../../third_party/blink/renderer/core/layout/block_node.cc:464:21]
#27 0x7f0b023e9417 blink::(anonymous namespace)::LayoutBlockChild() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:113:16]
#28 0x7f0b023e9c42 blink::(anonymous namespace)::LayoutInflow() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:128:10]
#29 0x7f0b023e9b05 blink::BlockLayoutAlgorithm::HandleInflow() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:2040:7]
#30 0x7f0b023f07e8 blink::BlockLayoutAlgorithm::Layout() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:921:18]
#31 0x7f0b023dfd3d blink::BlockLayoutAlgorithm::Layout() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:501:14]
#32 0x7f0b02411e61 _ZZN5blink12_GLOBAL__N_119LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEENKUlTyPT_E_clINS_20BlockLayoutAlgorithmEEEDaS5_ [../../third_party/blink/renderer/core/layout/block_node.cc:209:50]
#33 0x7f0b02411369 _ZN5blink12_GLOBAL__N_121CreateAlgorithmAndRunINS_20BlockLayoutAlgorithmEZNS0_19LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEEUlTyPT_E_EEvS5_RKT0_ [../../third_party/blink/renderer/core/layout/block_node.cc:117:3]
#34 0x7f0b024109c2 _ZN5blink12_GLOBAL__N_124DetermineAlgorithmAndRunIZNS0_19LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEEUlTyPT_E_EEvS4_RKS5_ [../../third_party/blink/renderer/core/layout/block_node.cc:200:5]
#35 0x7f0b0240a7d7 blink::(anonymous namespace)::LayoutWithAlgorithm() [../../third_party/blink/renderer/core/layout/block_node.cc:207:3]
#36 0x7f0b02408f81 blink::BlockNode::Layout() [../../third_party/blink/renderer/core/layout/block_node.cc:464:21]
#37 0x7f0b023e9417 blink::(anonymous namespace)::LayoutBlockChild() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:113:16]
#38 0x7f0b023e66a1 blink::BlockLayoutAlgorithm::LayoutNewFormattingContext() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1854:41]
#39 0x7f0b023e4ee3 blink::BlockLayoutAlgorithm::HandleNewFormattingContext() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1646:39]
#40 0x7f0b023f0796 blink::BlockLayoutAlgorithm::Layout() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:916:18]
#41 0x7f0b023dfd3d blink::BlockLayoutAlgorithm::Layout() [../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:501:14]
#42 0x7f0b02411e61 _ZZN5blink12_GLOBAL__N_119LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEENKUlTyPT_E_clINS_20BlockLayoutAlgorithmEEEDaS5_ [../../third_party/blink/renderer/core/layout/block_node.cc:209:50]
#43 0x7f0b02411369 _ZN5blink12_GLOBAL__N_121CreateAlgorithmAndRunINS_20BlockLayoutAlgorithmEZNS0_19LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEEUlTyPT_E_EEvS5_RKT0_ [../../third_party/blink/renderer/core/layout/block_node.cc:117:3]
#44 0x7f0b024109c2 _ZN5blink12_GLOBAL__N_124DetermineAlgorithmAndRunIZNS0_19LayoutWithAlgorithmERKNS_21LayoutAlgorithmParamsEEUlTyPT_E_EEvS4_RKS5_ [../../third_party/blink/renderer/core/layout/block_node.cc:200:5]
#45 0x7f0b0240a7d7 blink::(anonymous namespace)::LayoutWithAlgorithm() [../../third_party/blink/renderer/core/layout/block_node.cc:207:3]
#46 0x7f0b02408f81 blink::BlockNode::Layout() [../../third_party/blink/renderer/core/layout/block_node.cc:464:21]
#47 0x7f0b027bf254 blink::LayoutView::LayoutRoot() [../../third_party/blink/renderer/core/layout/layout_view.cc:810:19]
#48 0x7f0b0193a171 blink::LocalFrameView::PerformLayout() [../../third_party/blink/renderer/core/frame/local_frame_view.cc:783:24]
#49 0x7f0b0193b37f blink::LocalFrameView::UpdateLayout() [../../third_party/blink/renderer/core/frame/local_frame_view.cc:842:3]
#50 0x7f0b0194e846 blink::LocalFrameView::UpdateStyleAndLayoutInternal() [../../third_party/blink/renderer/core/frame/local_frame_view.cc:3171:7]
#51 0x7f0b01940070 blink::LocalFrameView::UpdateStyleAndLayout() [../../third_party/blink/renderer/core/frame/local_frame_view.cc:3101:18]
#52 0x7f0b03550c2f blink::Document::UpdateStyleAndLayout() [../../third_party/blink/renderer/core/dom/document.cc:2821:17]
#53 0x7f0b0355ad2f blink::Document::ImplicitClose() [../../third_party/blink/renderer/core/dom/document.cc:3986:7]
#54 0x7f0b0355b2b4 blink::Document::CheckCompletedInternal() [../../third_party/blink/renderer/core/dom/document.cc:4075:5]
#55 0x7f0b0355aa69 blink::Document::CheckCompleted() [../../third_party/blink/renderer/core/dom/document.cc:4037:7]
#56 0x7f0b029e94e4 blink::FrameLoader::FinishedParsing() [../../third_party/blink/renderer/core/loader/frame_loader.cc:448:26]
#57 0x7f0b03571e69 blink::Document::FinishedParsing() [../../third_party/blink/renderer/core/dom/document.cc:7485:21]
#58 0x7f0b036925a1 blink::HTMLConstructionSite::FinishedParsing() [../../third_party/blink/renderer/core/html/parser/html_construction_site.cc:757:14]
#59 0x7f0b0373a82d blink::HTMLTreeBuilder::Finished() [../../third_party/blink/renderer/core/html/parser/html_tree_builder.cc:3162:9]
#60 0x7f0b036ae500 blink::HTMLDocumentParser::end() [../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:1075:18]
#61 0x7f0b036a8347 blink::HTMLDocumentParser::AttemptToRunDeferredScriptsAndEnd() [../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:1088:3]
#62 0x7f0b036a7a28 blink::HTMLDocumentParser::PrepareToStopParsing() [../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:566:3]
#63 0x7f0b036ab39b blink::HTMLDocumentParser::AttemptToEnd() [../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:1112:3]
#64 0x7f0b036a7fd5 blink::HTMLDocumentParser::PumpTokenizerIfPossible() [../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:651:5]
#65 0x7f0b036a8a4a blink::HTMLDocumentParser::DeferredPumpTokenizerIfPossible() [../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:620:7]

```

---

128.0.6588.0 ASAN (Developer Build) (Linux) (64-bit)

Link Download Chromium ASAN binary: <https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-release-1325359.zip?generation=1720603707765920&alt=media>

heap-buffer-overflow.html

```
==1346450==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x50200004eed8 at pc 0x5601ea0c8365 bp 0x7ffe66315430 sp 0x7ffe66315428
READ of size 4 at 0x50200004eed8 thread T0 (chrome)
    #0 0x5601ea0c8364 in blink::LogicalLineBuilder::BidiReorder(blink::TextDirection, blink::LogicalLineItems*, blink::HeapVector<cppgc::internal::BasicMember<blink::LogicalRubyColumn, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 0u>&) third_party/blink/renderer/core/layout/inline/logical_line_builder.cc:644:29
    #1 0x5601ea0c5249 in blink::LogicalLineBuilder::CreateLine(blink::LineInfo*, blink::LogicalLineItems*, blink::InlineLayoutAlgorithm*) third_party/blink/renderer/core/layout/inline/logical_line_builder.cc:84:5
    #2 0x5601e9dc48ca in blink::InlineLayoutAlgorithm::CreateLine(blink::LineLayoutOpportunity const&, blink::LineInfo*, blink::LogicalLineContainer*) third_party/blink/renderer/core/layout/inline/inline_layout_algorithm.cc:381:16
    #3 0x5601e9dce5e0 in blink::InlineLayoutAlgorithm::Layout() third_party/blink/renderer/core/layout/inline/inline_layout_algorithm.cc:1242:5
    #4 0x5601e9d6b044 in blink::InlineNode::Layout(blink::ConstraintSpace const&, blink::BreakToken const*, blink::ColumnSpannerPath const*, blink::InlineChildLayoutContext*) const third_party/blink/renderer/core/layout/inline/inline_node.cc:1679:20
    #5 0x5601e9f79926 in blink::(anonymous namespace)::LayoutInflow(blink::ConstraintSpace const&, blink::BreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*, blink::LayoutInputNode*, blink::InlineChildLayoutContext*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:124:25
    #6 0x5601e9f78d8c in blink::BlockLayoutAlgorithm::HandleInflow(blink::LayoutInputNode, blink::BreakToken const*, blink::PreviousInflowPosition*, blink::InlineChildLayoutContext*, blink::InlineBreakToken const**) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:2071:7
    #7 0x5601e9f5b167 in blink::BlockLayoutAlgorithm::Layout(blink::InlineChildLayoutContext*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:934:18
    #8 0x5601e9f6057d in blink::BlockLayoutAlgorithm::LayoutWithSimpleInlineChildLayoutContext(blink::InlineNode const&) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:567:32
    #9 0x5601e9f58cdc in blink::BlockLayoutAlgorithm::Layout() third_party/blink/renderer/core/layout/block_layout_algorithm.cc:498:14
    #10 0x5601e9e79d23 in operator()<blink::BlockLayoutAlgorithm> third_party/blink/renderer/core/layout/block_node.cc:209:50
    #11 0x5601e9e79d23 in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*) const&) third_party/blink/renderer/core/layout/block_node.cc:117:3
    #12 0x5601e9e62657 in LayoutWithAlgorithm third_party/blink/renderer/core/layout/block_node.cc:207:3
    #13 0x5601e9e62657 in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*) const third_party/blink/renderer/core/layout/block_node.cc:466:21
    #14 0x5601e9f799c2 in LayoutBlockChild third_party/blink/renderer/core/layout/block_layout_algorithm.cc:112:16
    #15 0x5601e9f799c2 in blink::(anonymous namespace)::LayoutInflow(blink::ConstraintSpace const&, blink::BreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*, blink::LayoutInputNode*, blink::InlineChildLayoutContext*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:127:10
    #16 0x5601e9f78d8c in blink::BlockLayoutAlgorithm::HandleInflow(blink::LayoutInputNode, blink::BreakToken const*, blink::PreviousInflowPosition*, blink::InlineChildLayoutContext*, blink::InlineBreakToken const**) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:2071:7
    #17 0x5601e9f5b167 in blink::BlockLayoutAlgorithm::Layout(blink::InlineChildLayoutContext*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:934:18
    #18 0x5601e9f58cee in blink::BlockLayoutAlgorithm::Layout() third_party/blink/renderer/core/layout/block_layout_algorithm.cc:500:14
    #19 0x5601e9e79d23 in operator()<blink::BlockLayoutAlgorithm> third_party/blink/renderer/core/layout/block_node.cc:209:50
    #20 0x5601e9e79d23 in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*) const&) third_party/blink/renderer/core/layout/block_node.cc:117:3
    #21 0x5601e9e62657 in LayoutWithAlgorithm third_party/blink/renderer/core/layout/block_node.cc:207:3
    #22 0x5601e9e62657 in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*) const third_party/blink/renderer/core/layout/block_node.cc:466:21
    #23 0x5601e9f6ceb3 in LayoutBlockChild third_party/blink/renderer/core/layout/block_layout_algorithm.cc:112:16
    #24 0x5601e9f6ceb3 in blink::BlockLayoutAlgorithm::LayoutNewFormattingContext(blink::LayoutInputNode, blink::BlockBreakToken const*, blink::InflowChildData const&, blink::BfcOffset, bool, blink::BfcOffset*, blink::BoxStrut*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1885:41
    #25 0x5601e9f6a1a2 in blink::BlockLayoutAlgorithm::HandleNewFormattingContext(blink::LayoutInputNode, blink::BlockBreakToken const*, blink::PreviousInflowPosition*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1677:39
    #26 0x5601e9f5b254 in blink::BlockLayoutAlgorithm::Layout(blink::InlineChildLayoutContext*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:929:18
    #27 0x5601e9f58cee in blink::BlockLayoutAlgorithm::Layout() third_party/blink/renderer/core/layout/block_layout_algorithm.cc:500:14
    #28 0x5601e9e79d23 in operator()<blink::BlockLayoutAlgorithm> third_party/blink/renderer/core/layout/block_node.cc:209:50
    #29 0x5601e9e79d23 in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*) const&) third_party/blink/renderer/core/layout/block_node.cc:117:3
    #30 0x5601e9e62657 in LayoutWithAlgorithm third_party/blink/renderer/core/layout/block_node.cc:207:3
    #31 0x5601e9e62657 in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*) const third_party/blink/renderer/core/layout/block_node.cc:466:21
    #32 0x5601ea2bfeae in blink::LayoutView::LayoutRoot() third_party/blink/renderer/core/layout/layout_view.cc:810:19
    #33 0x5601e908db08 in blink::LocalFrameView::PerformLayout() third_party/blink/renderer/core/frame/local_frame_view.cc:783:24
    #34 0x5601e908fcee in blink::LocalFrameView::UpdateLayout() third_party/blink/renderer/core/frame/local_frame_view.cc:842:3
    #35 0x5601e90acdf2 in blink::LocalFrameView::UpdateStyleAndLayoutInternal() third_party/blink/renderer/core/frame/local_frame_view.cc:3170:7
    #36 0x5601e9098f85 in blink::LocalFrameView::UpdateStyleAndLayout() third_party/blink/renderer/core/frame/local_frame_view.cc:3100:18
    #37 0x5601ebef2d1b in blink::Document::UpdateStyleAndLayout(blink::DocumentUpdateReason) third_party/blink/renderer/core/dom/document.cc:2837:17
    #38 0x5601ebf07ccb in blink::Document::ImplicitClose() third_party/blink/renderer/core/dom/document.cc:4004:7
    #39 0x5601ebf08a6b in blink::Document::CheckCompletedInternal() third_party/blink/renderer/core/dom/document.cc:4093:5
    #40 0x5601ebf072b2 in blink::Document::CheckCompleted() third_party/blink/renderer/core/dom/document.cc:4055:7
    #41 0x5601ea5c32b9 in blink::FrameLoader::FinishedParsing() third_party/blink/renderer/core/loader/frame_loader.cc:448:26
    #42 0x5601ebf4293f in blink::Document::FinishedParsing() third_party/blink/renderer/core/dom/document.cc:7510:21
    #43 0x5601ec22dab2 in end third_party/blink/renderer/core/html/parser/html_document_parser.cc:1075:18
    #44 0x5601ec22dab2 in AttemptToRunDeferredScriptsAndEnd third_party/blink/renderer/core/html/parser/html_document_parser.cc:1088:3
    #45 0x5601ec22dab2 in blink::HTMLDocumentParser::PrepareToStopParsing() third_party/blink/renderer/core/html/parser/html_document_parser.cc:566:3
    #46 0x5601ec233449 in blink::HTMLDocumentParser::AttemptToEnd() third_party/blink/renderer/core/html/parser/html_document_parser.cc:1112:3
    #47 0x5601ec22e45e in blink::HTMLDocumentParser::PumpTokenizerIfPossible() third_party/blink/renderer/core/html/parser/html_document_parser.cc:651:5
    #48 0x5601ec22ec3a in blink::HTMLDocumentParser::DeferredPumpTokenizerIfPossible(bool, base::TimeTicks) third_party/blink/renderer/core/html/parser/html_document_parser.cc:620:7
    #49 0x5601ec24cf3c in Invoke<void (blink::HTMLDocumentParser::*)(bool, base::TimeTicks), cppgc::internal::BasicPersistent<blink::HTMLDocumentParser, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, bool, base::TimeTicks> base/functional/bind_internal.h:738:12
    #50 0x5601ec24cf3c in MakeItSo<void (blink::HTMLDocumentParser::*)(bool, base::TimeTicks), std::__Cr::tuple<cppgc::internal::BasicPersistent<blink::HTMLDocumentParser, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, bool, base::TimeTicks> > base/functional/bind_internal.h:930:12
    #51 0x5601ec24cf3c in RunImpl<void (blink::HTMLDocumentParser::*)(bool, base::TimeTicks), std::__Cr::tuple<cppgc::internal::BasicPersistent<blink::HTMLDocumentParser, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, bool, base::TimeTicks>, 0UL, 1UL, 2UL> base/functional/bind_internal.h:1067:14
    #52 0x5601ec24cf3c in base::internal::Invoker<base::internal::FunctorTraits<void (blink::HTMLDocumentParser::*&&)(bool, base::TimeTicks), cppgc::internal::BasicPersistent<blink::HTMLDocumentParser, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>&&, bool&&, base::TimeTicks&&>, base::internal::BindState<true, true, false, void (blink::HTMLDocumentParser::*)(bool, base::TimeTicks), cppgc::internal::BasicPersistent<blink::HTMLDocumentParser, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, bool, base::TimeTicks>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:980:12
    #53 0x5601dbf904b4 in Run base/functional/callback.h:156:12
    #54 0x5601dbf904b4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:203:34
    #55 0x5601dbff4d06 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:486:11)> base/task/common/task_annotator.h:90:5
    #56 0x5601dbff4d06 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:484:23
    #57 0x5601dbff3c20 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #58 0x5601dbff5a4a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #59 0x5601dbe7fadd in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:40:55
    #60 0x5601dbff66b6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:654:12
    #61 0x5601dbf1c3af in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #62 0x5601f3951668 in content::RendererMain(content::MainFunctionParams) content/renderer/renderer_main.cc:359:16
    #63 0x5601d933bea6 in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:703:14
    #64 0x5601d933d58a in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:807:12
    #65 0x5601d9340061 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1175:10
    #66 0x5601d933a041 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:332:36
    #67 0x5601d933a6cb in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:345:10
    #68 0x5601c8b6548b in ChromeMain chrome/app/chrome_main.cc:228:12
    #69 0x7f3c2da29d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

0x50200004eed8 is located 0 bytes after 8-byte region [0x50200004eed0,0x50200004eed8)
allocated by thread T0 (chrome) here:
    #0 0x5601c8b2c7af in malloc /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:68:3
    #1 0x5601dc1e10fb in AllocInternal<(partition_alloc::internal::AllocFlags)0> base/allocator/partition_allocator/src/partition_alloc/partition_root.h:2104:51
    #2 0x5601dc1e10fb in AllocInline<(partition_alloc::internal::AllocFlags)0> base/allocator/partition_allocator/src/partition_alloc/partition_root.h:536:12
    #3 0x5601dc1e10fb in void* partition_alloc::PartitionRoot::Alloc<(partition_alloc::internal::AllocFlags)0>(unsigned long, char const*) base/allocator/partition_allocator/src/partition_alloc/partition_root.h:530:12
    #4 0x5601ea0c7b70 in AllocateVectorBacking<unsigned int> third_party/blink/renderer/platform/wtf/allocator/partition_allocator.h:40:9
    #5 0x5601ea0c7b70 in AllocateBufferNoBarrier third_party/blink/renderer/platform/wtf/vector.h:523:9
    #6 0x5601ea0c7b70 in AllocateBuffer third_party/blink/renderer/platform/wtf/vector.h:420:5
    #7 0x5601ea0c7b70 in VectorBuffer third_party/blink/renderer/platform/wtf/vector.h:548:7
    #8 0x5601ea0c7b70 in Vector third_party/blink/renderer/platform/wtf/vector.h:1531:7
    #9 0x5601ea0c7b70 in blink::LogicalLineBuilder::BidiReorder(blink::TextDirection, blink::LogicalLineItems*, blink::HeapVector<cppgc::internal::BasicMember<blink::LogicalRubyColumn, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 0u>&) third_party/blink/renderer/core/layout/inline/logical_line_builder.cc:630:26
    #10 0x5601ea0c5249 in blink::LogicalLineBuilder::CreateLine(blink::LineInfo*, blink::LogicalLineItems*, blink::InlineLayoutAlgorithm*) third_party/blink/renderer/core/layout/inline/logical_line_builder.cc:84:5
    #11 0x5601e9dc48ca in blink::InlineLayoutAlgorithm::CreateLine(blink::LineLayoutOpportunity const&, blink::LineInfo*, blink::LogicalLineContainer*) third_party/blink/renderer/core/layout/inline/inline_layout_algorithm.cc:381:16
    #12 0x5601e9dce5e0 in blink::InlineLayoutAlgorithm::Layout() third_party/blink/renderer/core/layout/inline/inline_layout_algorithm.cc:1242:5
    #13 0x5601e9d6b044 in blink::InlineNode::Layout(blink::ConstraintSpace const&, blink::BreakToken const*, blink::ColumnSpannerPath const*, blink::InlineChildLayoutContext*) const third_party/blink/renderer/core/layout/inline/inline_node.cc:1679:20
    #14 0x5601e9f79926 in blink::(anonymous namespace)::LayoutInflow(blink::ConstraintSpace const&, blink::BreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*, blink::LayoutInputNode*, blink::InlineChildLayoutContext*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:124:25
    #15 0x5601e9f78d8c in blink::BlockLayoutAlgorithm::HandleInflow(blink::LayoutInputNode, blink::BreakToken const*, blink::PreviousInflowPosition*, blink::InlineChildLayoutContext*, blink::InlineBreakToken const**) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:2071:7
    #16 0x5601e9f5b167 in blink::BlockLayoutAlgorithm::Layout(blink::InlineChildLayoutContext*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:934:18
    #17 0x5601e9f6057d in blink::BlockLayoutAlgorithm::LayoutWithSimpleInlineChildLayoutContext(blink::InlineNode const&) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:567:32
    #18 0x5601e9f58cdc in blink::BlockLayoutAlgorithm::Layout() third_party/blink/renderer/core/layout/block_layout_algorithm.cc:498:14
    #19 0x5601e9e79d23 in operator()<blink::BlockLayoutAlgorithm> third_party/blink/renderer/core/layout/block_node.cc:209:50
    #20 0x5601e9e79d23 in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*) const&) third_party/blink/renderer/core/layout/block_node.cc:117:3
    #21 0x5601e9e62657 in LayoutWithAlgorithm third_party/blink/renderer/core/layout/block_node.cc:207:3
    #22 0x5601e9e62657 in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*) const third_party/blink/renderer/core/layout/block_node.cc:466:21
    #23 0x5601e9f799c2 in LayoutBlockChild third_party/blink/renderer/core/layout/block_layout_algorithm.cc:112:16
    #24 0x5601e9f799c2 in blink::(anonymous namespace)::LayoutInflow(blink::ConstraintSpace const&, blink::BreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*, blink::LayoutInputNode*, blink::InlineChildLayoutContext*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:127:10
    #25 0x5601e9f78d8c in blink::BlockLayoutAlgorithm::HandleInflow(blink::LayoutInputNode, blink::BreakToken const*, blink::PreviousInflowPosition*, blink::InlineChildLayoutContext*, blink::InlineBreakToken const**) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:2071:7
    #26 0x5601e9f5b167 in blink::BlockLayoutAlgorithm::Layout(blink::InlineChildLayoutContext*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:934:18
    #27 0x5601e9f58cee in blink::BlockLayoutAlgorithm::Layout() third_party/blink/renderer/core/layout/block_layout_algorithm.cc:500:14
    #28 0x5601e9e79d23 in operator()<blink::BlockLayoutAlgorithm> third_party/blink/renderer/core/layout/block_node.cc:209:50
    #29 0x5601e9e79d23 in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*) const&) third_party/blink/renderer/core/layout/block_node.cc:117:3
    #30 0x5601e9e62657 in LayoutWithAlgorithm third_party/blink/renderer/core/layout/block_node.cc:207:3
    #31 0x5601e9e62657 in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*) const third_party/blink/renderer/core/layout/block_node.cc:466:21
    #32 0x5601e9f6ceb3 in LayoutBlockChild third_party/blink/renderer/core/layout/block_layout_algorithm.cc:112:16
    #33 0x5601e9f6ceb3 in blink::BlockLayoutAlgorithm::LayoutNewFormattingContext(blink::LayoutInputNode, blink::BlockBreakToken const*, blink::InflowChildData const&, blink::BfcOffset, bool, blink::BfcOffset*, blink::BoxStrut*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1885:41
    #34 0x5601e9f6a1a2 in blink::BlockLayoutAlgorithm::HandleNewFormattingContext(blink::LayoutInputNode, blink::BlockBreakToken const*, blink::PreviousInflowPosition*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1677:39
    #35 0x5601e9f5b254 in blink::BlockLayoutAlgorithm::Layout(blink::InlineChildLayoutContext*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:929:18
    #36 0x5601e9f58cee in blink::BlockLayoutAlgorithm::Layout() third_party/blink/renderer/core/layout/block_layout_algorithm.cc:500:14
    #37 0x5601e9e79d23 in operator()<blink::BlockLayoutAlgorithm> third_party/blink/renderer/core/layout/block_node.cc:209:50
    #38 0x5601e9e79d23 in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*) const&) third_party/blink/renderer/core/layout/block_node.cc:117:3
    #39 0x5601e9e62657 in LayoutWithAlgorithm third_party/blink/renderer/core/layout/block_node.cc:207:3
    #40 0x5601e9e62657 in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*) const third_party/blink/renderer/core/layout/block_node.cc:466:21
    #41 0x5601ea2bfeae in blink::LayoutView::LayoutRoot() third_party/blink/renderer/core/layout/layout_view.cc:810:19
    #42 0x5601e908db08 in blink::LocalFrameView::PerformLayout() third_party/blink/renderer/core/frame/local_frame_view.cc:783:24
    #43 0x5601e908fcee in blink::LocalFrameView::UpdateLayout() third_party/blink/renderer/core/frame/local_frame_view.cc:842:3
    #44 0x5601e90acdf2 in blink::LocalFrameView::UpdateStyleAndLayoutInternal() third_party/blink/renderer/core/frame/local_frame_view.cc:3170:7

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/blink/renderer/core/layout/inline/logical_line_builder.cc:644:29 in blink::LogicalLineBuilder::BidiReorder(blink::TextDirection, blink::LogicalLineItems*, blink::HeapVector<cppgc::internal::BasicMember<blink::LogicalRubyColumn, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 0u>&)
Shadow bytes around the buggy address:
  0x50200004ec00: f7 fa fd fd f7 fa 00 00 f7 fa fd fd f7 fa 01 fa
  0x50200004ec80: f7 fa fd fd f7 fa 00 00 f7 fa fd fa f7 fa fd fd
  0x50200004ed00: f7 fa fd fa f7 fa fd fd f7 fa fd fd f7 fa fd fa
  0x50200004ed80: f7 fa fd fa f7 fa fd fa f7 fa 04 fa f7 fa 00 04
  0x50200004ee00: f7 fa fd fd f7 fa 01 fa f7 fa fd fd f7 fa 00 00
=>0x50200004ee80: f7 fa 02 fa f7 fa 00 fa f7 fa 00[fa]fa fa fa fa
  0x50200004ef00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x50200004ef80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x50200004f000: f7 fa fd fa f7 fa fd fd f7 fa fd fd f7 fa fd fa
  0x50200004f080: f7 fa fd fa f7 fa fd fd f7 fa fd fa f7 fa fd fd
  0x50200004f100: f7 fa fd fd f7 fa fd fa f7 fa fd fd f7 fa fd fa
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

==1346450==ADDITIONAL INFO


```

---

vector-overflow-variant.html

```
[1347640:1347640:0710/190635.610824:FATAL:vector.h(1182)] Check failed: i < size() (2 vs. 2)

```

CREDIT INFORMATION
Reporter credit: Tashita Software Security

## Attachments

- [heap-buffer-overflow.html](attachments/heap-buffer-overflow.html) (text/html, 1.4 KB)
- [vector-overflow-variant.html](attachments/vector-overflow-variant.html) (text/html, 1.4 KB)
- [LogicalLineBuilder_BidiReorder_HeapBufferOverflow_ASAN.html](attachments/LogicalLineBuilder_BidiReorder_HeapBufferOverflow_ASAN.html) (text/html, 998 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-07-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5171017800417280.

### 24...@project.gserviceaccount.com (2024-07-11)

This crash occurs very frequently on mac platform and is likely preventing the fuzzer None from making much progress. Fixing this will allow more bugs to be found.

Marking this bug as a blocker for next Beta release.

If this is incorrect, please add the hotlistid:5433040 and remove the hotlistid:ReleaseBlock-Beta.

### fl...@google.com (2024-07-12)

Hey there,

It looks like this is a pretty big regression in terms of stability.

However, the lines the code is choking on are CHECKs, not DCHECKs, so there's not a security implication here—the program should terminate.

Thank you for the report, though, and definitely send us reports in the future, particularly if you're able to find DCHECKs with security implications.

### pe...@google.com (2024-07-16)

This issue is marked as a release blocker with no milestone associated. Please add an appropriate milestone.

All release blocking issues should have milestones associated to it, so that the issue can tracked and the fixes can be pushed promptly.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-07-22)

This issue is marked as a release blocker with no milestone associated. Please add an appropriate milestone.

All release blocking issues should have milestones associated to it, so that the issue can tracked and the fixes can be pushed promptly.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ta...@gmail.com (2024-07-27)

Hello,

Based on this same bug, we have managed to create a new testcase that hits a Heap-Buffer-Overflow, affecting the latest official Chromium release 127.0.6533.72 launched few days ago.

This is the ASAN report generated:

```
==2055359==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x5020000fe754 at pc 0x55f73fb35b15 bp 0x7ffcb65a2430 sp 0x7ffcb65a2428
READ of size 4 at 0x5020000fe754 thread T0 (chrome)
    #0 0x55f73fb35b14 in blink::LogicalLineBuilder::BidiReorder(blink::TextDirection, blink::LogicalLineItems*, blink::HeapVector<cppgc::internal::BasicMember<blink::LogicalRubyColumn, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 0u>&) third_party/blink/renderer/core/layout/inline/logical_line_builder.cc:639:29
    #1 0x55f73fb329e9 in blink::LogicalLineBuilder::CreateLine(blink::LineInfo*, blink::LogicalLineItems*, blink::InlineLayoutAlgorithm*) third_party/blink/renderer/core/layout/inline/logical_line_builder.cc:79:5
    #2 0x55f73f842d05 in blink::InlineLayoutAlgorithm::CreateLine(blink::LineLayoutOpportunity const&, blink::LineInfo*, blink::LogicalLineContainer*) third_party/blink/renderer/core/layout/inline/inline_layout_algorithm.cc:384:16
    #3 0x55f73f84ca60 in blink::InlineLayoutAlgorithm::Layout() third_party/blink/renderer/core/layout/inline/inline_layout_algorithm.cc:1245:5
    #4 0x55f73f7e98f0 in blink::InlineNode::Layout(blink::ConstraintSpace const&, blink::BreakToken const*, blink::ColumnSpannerPath const*, blink::InlineChildLayoutContext*) const third_party/blink/renderer/core/layout/inline/inline_node.cc:1673:20
    #5 0x55f73f9f1da6 in blink::(anonymous namespace)::LayoutInflow(blink::ConstraintSpace const&, blink::BreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*, blink::LayoutInputNode*, blink::InlineChildLayoutContext*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:125:25
    #6 0x55f73f9f120d in blink::BlockLayoutAlgorithm::HandleInflow(blink::LayoutInputNode, blink::BreakToken const*, blink::PreviousInflowPosition*, blink::InlineChildLayoutContext*, blink::InlineBreakToken const**) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:2040:7
    #7 0x55f73f9d4a29 in blink::BlockLayoutAlgorithm::Layout(blink::InlineChildLayoutContext*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:921:18
    #8 0x55f73f9d934d in blink::BlockLayoutAlgorithm::LayoutWithSimpleInlineChildLayoutContext(blink::InlineNode const&) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:568:32
    #9 0x55f73f9d297c in blink::BlockLayoutAlgorithm::Layout() third_party/blink/renderer/core/layout/block_layout_algorithm.cc:499:14
    #10 0x55f73f8f56f3 in operator()<blink::BlockLayoutAlgorithm> third_party/blink/renderer/core/layout/block_node.cc:209:50
    #11 0x55f73f8f56f3 in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*) const&) third_party/blink/renderer/core/layout/block_node.cc:117:3
    #12 0x55f73f8de8c3 in LayoutWithAlgorithm third_party/blink/renderer/core/layout/block_node.cc:207:3
    #13 0x55f73f8de8c3 in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*) const third_party/blink/renderer/core/layout/block_node.cc:464:21
    #14 0x55f73f9f1e42 in LayoutBlockChild third_party/blink/renderer/core/layout/block_layout_algorithm.cc:113:16
    #15 0x55f73f9f1e42 in blink::(anonymous namespace)::LayoutInflow(blink::ConstraintSpace const&, blink::BreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*, blink::LayoutInputNode*, blink::InlineChildLayoutContext*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:128:10
    #16 0x55f73f9f120d in blink::BlockLayoutAlgorithm::HandleInflow(blink::LayoutInputNode, blink::BreakToken const*, blink::PreviousInflowPosition*, blink::InlineChildLayoutContext*, blink::InlineBreakToken const**) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:2040:7
    #17 0x55f73f9d4a29 in blink::BlockLayoutAlgorithm::Layout(blink::InlineChildLayoutContext*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:921:18
    #18 0x55f73f9d298e in blink::BlockLayoutAlgorithm::Layout() third_party/blink/renderer/core/layout/block_layout_algorithm.cc:501:14
    #19 0x55f73f8f56f3 in operator()<blink::BlockLayoutAlgorithm> third_party/blink/renderer/core/layout/block_node.cc:209:50
    #20 0x55f73f8f56f3 in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*) const&) third_party/blink/renderer/core/layout/block_node.cc:117:3
    #21 0x55f73f8de8c3 in LayoutWithAlgorithm third_party/blink/renderer/core/layout/block_node.cc:207:3
    #22 0x55f73f8de8c3 in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*) const third_party/blink/renderer/core/layout/block_node.cc:464:21
    #23 0x55f73f9e5c04 in LayoutBlockChild third_party/blink/renderer/core/layout/block_layout_algorithm.cc:113:16
    #24 0x55f73f9e5c04 in blink::BlockLayoutAlgorithm::LayoutNewFormattingContext(blink::LayoutInputNode, blink::BlockBreakToken const*, blink::InflowChildData const&, blink::BfcOffset, bool, blink::BfcOffset*, blink::BoxStrut*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1854:41
    #25 0x55f73f9e31c8 in blink::BlockLayoutAlgorithm::HandleNewFormattingContext(blink::LayoutInputNode, blink::BlockBreakToken const*, blink::PreviousInflowPosition*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1646:39
    #26 0x55f73f9d4b1d in blink::BlockLayoutAlgorithm::Layout(blink::InlineChildLayoutContext*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:916:18
    #27 0x55f73f9d298e in blink::BlockLayoutAlgorithm::Layout() third_party/blink/renderer/core/layout/block_layout_algorithm.cc:501:14
    #28 0x55f73f8f56f3 in operator()<blink::BlockLayoutAlgorithm> third_party/blink/renderer/core/layout/block_node.cc:209:50
    #29 0x55f73f8f56f3 in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*) const&) third_party/blink/renderer/core/layout/block_node.cc:117:3
    #30 0x55f73f8de8c3 in LayoutWithAlgorithm third_party/blink/renderer/core/layout/block_node.cc:207:3
    #31 0x55f73f8de8c3 in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*) const third_party/blink/renderer/core/layout/block_node.cc:464:21
    #32 0x55f73fd2b2a6 in blink::LayoutView::LayoutRoot() third_party/blink/renderer/core/layout/layout_view.cc:810:19
    #33 0x55f73eb16c58 in blink::LocalFrameView::PerformLayout() third_party/blink/renderer/core/frame/local_frame_view.cc:783:24
    #34 0x55f73eb18e7e in blink::LocalFrameView::UpdateLayout() third_party/blink/renderer/core/frame/local_frame_view.cc:842:3
    #35 0x55f73eb360a2 in blink::LocalFrameView::UpdateStyleAndLayoutInternal() third_party/blink/renderer/core/frame/local_frame_view.cc:3171:7
    #36 0x55f73eb22125 in blink::LocalFrameView::UpdateStyleAndLayout() third_party/blink/renderer/core/frame/local_frame_view.cc:3101:18
    #37 0x55f7419272a9 in blink::Document::UpdateStyleAndLayout(blink::DocumentUpdateReason) third_party/blink/renderer/core/dom/document.cc:2821:17
    #38 0x55f74193bffb in blink::Document::ImplicitClose() third_party/blink/renderer/core/dom/document.cc:3986:7
    #39 0x55f74193cd9b in blink::Document::CheckCompletedInternal() third_party/blink/renderer/core/dom/document.cc:4075:5
    #40 0x55f74193b5e2 in blink::Document::CheckCompleted() third_party/blink/renderer/core/dom/document.cc:4037:7
    #41 0x55f74001d619 in blink::FrameLoader::FinishedParsing() third_party/blink/renderer/core/loader/frame_loader.cc:448:26
    #42 0x55f741976a8a in blink::Document::FinishedParsing() third_party/blink/renderer/core/dom/document.cc:7485:21
    #43 0x55f741c5fc52 in end third_party/blink/renderer/core/html/parser/html_document_parser.cc:1075:18
    #44 0x55f741c5fc52 in AttemptToRunDeferredScriptsAndEnd third_party/blink/renderer/core/html/parser/html_document_parser.cc:1088:3
    #45 0x55f741c5fc52 in blink::HTMLDocumentParser::PrepareToStopParsing() third_party/blink/renderer/core/html/parser/html_document_parser.cc:566:3
    #46 0x55f741c655b9 in blink::HTMLDocumentParser::AttemptToEnd() third_party/blink/renderer/core/html/parser/html_document_parser.cc:1112:3
    #47 0x55f741c605fe in blink::HTMLDocumentParser::PumpTokenizerIfPossible() third_party/blink/renderer/core/html/parser/html_document_parser.cc:651:5
    #48 0x55f741c60dda in blink::HTMLDocumentParser::DeferredPumpTokenizerIfPossible(bool, base::TimeTicks) third_party/blink/renderer/core/html/parser/html_document_parser.cc:620:7
    #49 0x55f741c7ffdc in Invoke<void (blink::HTMLDocumentParser::*)(bool, base::TimeTicks), cppgc::internal::BasicPersistent<blink::HTMLDocumentParser, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, bool, base::TimeTicks> base/functional/bind_internal.h:738:12
    #50 0x55f741c7ffdc in MakeItSo<void (blink::HTMLDocumentParser::*)(bool, base::TimeTicks), std::__Cr::tuple<cppgc::internal::BasicPersistent<blink::HTMLDocumentParser, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, bool, base::TimeTicks> > base/functional/bind_internal.h:930:12
    #51 0x55f741c7ffdc in RunImpl<void (blink::HTMLDocumentParser::*)(bool, base::TimeTicks), std::__Cr::tuple<cppgc::internal::BasicPersistent<blink::HTMLDocumentParser, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, bool, base::TimeTicks>, 0UL, 1UL, 2UL> base/functional/bind_internal.h:1067:14
    #52 0x55f741c7ffdc in base::internal::Invoker<base::internal::FunctorTraits<void (blink::HTMLDocumentParser::*&&)(bool, base::TimeTicks), cppgc::internal::BasicPersistent<blink::HTMLDocumentParser, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>&&, bool&&, base::TimeTicks&&>, base::internal::BindState<true, true, false, void (blink::HTMLDocumentParser::*)(bool, base::TimeTicks), cppgc::internal::BasicPersistent<blink::HTMLDocumentParser, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, bool, base::TimeTicks>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:980:12
    #53 0x55f731f32894 in Run base/functional/callback.h:156:12
    #54 0x55f731f32894 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:203:34
    #55 0x55f731f95a46 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:486:11)> base/task/common/task_annotator.h:90:5
    #56 0x55f731f95a46 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:484:23
    #57 0x55f731f94960 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #58 0x55f731f9678a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #59 0x55f731e2c18d in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:40:55
    #60 0x55f731f973f6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:654:12
    #61 0x55f731ec5b3f in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #62 0x55f7491c904a in content::RendererMain(content::MainFunctionParams) content/renderer/renderer_main.cc:359:16
    #63 0x55f72f5bc98b in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:689:14
    #64 0x55f72f5bdeee in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:793:12
    #65 0x55f72f5c0c18 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1156:10
    #66 0x55f72f5bac90 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:332:36
    #67 0x55f72f5bb31b in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:345:10
    #68 0x55f71f2543c8 in ChromeMain chrome/app/chrome_main.cc:192:12
    #69 0x7fc8a8029d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

0x5020000fe754 is located 0 bytes after 4-byte region [0x5020000fe750,0x5020000fe754)
allocated by thread T0 (chrome) here:
    #0 0x55f71f21b7af in malloc /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:68:3
    #1 0x55f73217aaab in AllocInternal<(partition_alloc::internal::AllocFlags)0> base/allocator/partition_allocator/src/partition_alloc/partition_root.h:2110:51
    #2 0x55f73217aaab in AllocInline<(partition_alloc::internal::AllocFlags)0> base/allocator/partition_allocator/src/partition_alloc/partition_root.h:528:12
    #3 0x55f73217aaab in void* partition_alloc::PartitionRoot::Alloc<(partition_alloc::internal::AllocFlags)0>(unsigned long, char const*) base/allocator/partition_allocator/src/partition_alloc/partition_root.h:522:12
    #4 0x55f73fb35320 in AllocateVectorBacking<unsigned int> third_party/blink/renderer/platform/wtf/allocator/partition_allocator.h:40:9
    #5 0x55f73fb35320 in AllocateBufferNoBarrier third_party/blink/renderer/platform/wtf/vector.h:517:9
    #6 0x55f73fb35320 in AllocateBuffer third_party/blink/renderer/platform/wtf/vector.h:414:5
    #7 0x55f73fb35320 in VectorBuffer third_party/blink/renderer/platform/wtf/vector.h:542:7
    #8 0x55f73fb35320 in Vector third_party/blink/renderer/platform/wtf/vector.h:1539:7
    #9 0x55f73fb35320 in blink::LogicalLineBuilder::BidiReorder(blink::TextDirection, blink::LogicalLineItems*, blink::HeapVector<cppgc::internal::BasicMember<blink::LogicalRubyColumn, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 0u>&) third_party/blink/renderer/core/layout/inline/logical_line_builder.cc:625:26
    #10 0x55f73fb329e9 in blink::LogicalLineBuilder::CreateLine(blink::LineInfo*, blink::LogicalLineItems*, blink::InlineLayoutAlgorithm*) third_party/blink/renderer/core/layout/inline/logical_line_builder.cc:79:5
    #11 0x55f73f842d05 in blink::InlineLayoutAlgorithm::CreateLine(blink::LineLayoutOpportunity const&, blink::LineInfo*, blink::LogicalLineContainer*) third_party/blink/renderer/core/layout/inline/inline_layout_algorithm.cc:384:16
    #12 0x55f73f84ca60 in blink::InlineLayoutAlgorithm::Layout() third_party/blink/renderer/core/layout/inline/inline_layout_algorithm.cc:1245:5
    #13 0x55f73f7e98f0 in blink::InlineNode::Layout(blink::ConstraintSpace const&, blink::BreakToken const*, blink::ColumnSpannerPath const*, blink::InlineChildLayoutContext*) const third_party/blink/renderer/core/layout/inline/inline_node.cc:1673:20
    #14 0x55f73f9f1da6 in blink::(anonymous namespace)::LayoutInflow(blink::ConstraintSpace const&, blink::BreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*, blink::LayoutInputNode*, blink::InlineChildLayoutContext*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:125:25
    #15 0x55f73f9f120d in blink::BlockLayoutAlgorithm::HandleInflow(blink::LayoutInputNode, blink::BreakToken const*, blink::PreviousInflowPosition*, blink::InlineChildLayoutContext*, blink::InlineBreakToken const**) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:2040:7
    #16 0x55f73f9d4a29 in blink::BlockLayoutAlgorithm::Layout(blink::InlineChildLayoutContext*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:921:18
    #17 0x55f73f9d934d in blink::BlockLayoutAlgorithm::LayoutWithSimpleInlineChildLayoutContext(blink::InlineNode const&) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:568:32
    #18 0x55f73f9d297c in blink::BlockLayoutAlgorithm::Layout() third_party/blink/renderer/core/layout/block_layout_algorithm.cc:499:14
    #19 0x55f73f8f56f3 in operator()<blink::BlockLayoutAlgorithm> third_party/blink/renderer/core/layout/block_node.cc:209:50
    #20 0x55f73f8f56f3 in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*) const&) third_party/blink/renderer/core/layout/block_node.cc:117:3
    #21 0x55f73f8de8c3 in LayoutWithAlgorithm third_party/blink/renderer/core/layout/block_node.cc:207:3
    #22 0x55f73f8de8c3 in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*) const third_party/blink/renderer/core/layout/block_node.cc:464:21
    #23 0x55f73f9f1e42 in LayoutBlockChild third_party/blink/renderer/core/layout/block_layout_algorithm.cc:113:16
    #24 0x55f73f9f1e42 in blink::(anonymous namespace)::LayoutInflow(blink::ConstraintSpace const&, blink::BreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*, blink::LayoutInputNode*, blink::InlineChildLayoutContext*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:128:10
    #25 0x55f73f9f120d in blink::BlockLayoutAlgorithm::HandleInflow(blink::LayoutInputNode, blink::BreakToken const*, blink::PreviousInflowPosition*, blink::InlineChildLayoutContext*, blink::InlineBreakToken const**) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:2040:7
    #26 0x55f73f9d4a29 in blink::BlockLayoutAlgorithm::Layout(blink::InlineChildLayoutContext*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:921:18
    #27 0x55f73f9d298e in blink::BlockLayoutAlgorithm::Layout() third_party/blink/renderer/core/layout/block_layout_algorithm.cc:501:14
    #28 0x55f73f8f56f3 in operator()<blink::BlockLayoutAlgorithm> third_party/blink/renderer/core/layout/block_node.cc:209:50
    #29 0x55f73f8f56f3 in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*) const&) third_party/blink/renderer/core/layout/block_node.cc:117:3
    #30 0x55f73f8de8c3 in LayoutWithAlgorithm third_party/blink/renderer/core/layout/block_node.cc:207:3
    #31 0x55f73f8de8c3 in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*) const third_party/blink/renderer/core/layout/block_node.cc:464:21
    #32 0x55f73f9e5c04 in LayoutBlockChild third_party/blink/renderer/core/layout/block_layout_algorithm.cc:113:16
    #33 0x55f73f9e5c04 in blink::BlockLayoutAlgorithm::LayoutNewFormattingContext(blink::LayoutInputNode, blink::BlockBreakToken const*, blink::InflowChildData const&, blink::BfcOffset, bool, blink::BfcOffset*, blink::BoxStrut*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1854:41
    #34 0x55f73f9e31c8 in blink::BlockLayoutAlgorithm::HandleNewFormattingContext(blink::LayoutInputNode, blink::BlockBreakToken const*, blink::PreviousInflowPosition*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1646:39
    #35 0x55f73f9d4b1d in blink::BlockLayoutAlgorithm::Layout(blink::InlineChildLayoutContext*) third_party/blink/renderer/core/layout/block_layout_algorithm.cc:916:18
    #36 0x55f73f9d298e in blink::BlockLayoutAlgorithm::Layout() third_party/blink/renderer/core/layout/block_layout_algorithm.cc:501:14
    #37 0x55f73f8f56f3 in operator()<blink::BlockLayoutAlgorithm> third_party/blink/renderer/core/layout/block_node.cc:209:50
    #38 0x55f73f8f56f3 in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*) const&) third_party/blink/renderer/core/layout/block_node.cc:117:3
    #39 0x55f73f8de8c3 in LayoutWithAlgorithm third_party/blink/renderer/core/layout/block_node.cc:207:3
    #40 0x55f73f8de8c3 in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*) const third_party/blink/renderer/core/layout/block_node.cc:464:21
    #41 0x55f73fd2b2a6 in blink::LayoutView::LayoutRoot() third_party/blink/renderer/core/layout/layout_view.cc:810:19
    #42 0x55f73eb16c58 in blink::LocalFrameView::PerformLayout() third_party/blink/renderer/core/frame/local_frame_view.cc:783:24
    #43 0x55f73eb18e7e in blink::LocalFrameView::UpdateLayout() third_party/blink/renderer/core/frame/local_frame_view.cc:842:3
    #44 0x55f73eb360a2 in blink::LocalFrameView::UpdateStyleAndLayoutInternal() third_party/blink/renderer/core/frame/local_frame_view.cc:3171:7

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/blink/renderer/core/layout/inline/logical_line_builder.cc:639:29 in blink::LogicalLineBuilder::BidiReorder(blink::TextDirection, blink::LogicalLineItems*, blink::HeapVector<cppgc::internal::BasicMember<blink::LogicalRubyColumn, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 0u>&)
Shadow bytes around the buggy address:
  0x5020000fe480: f7 fa fa fa f7 fa fa fa f7 fa fa fa f7 fa fa fa
  0x5020000fe500: f7 fa fa fa f7 fa fa fa f7 fa fa fa f7 fa fa fa
  0x5020000fe580: f7 fa fa fa f7 fa fa fa f7 fa fa fa f7 fa fa fa
  0x5020000fe600: f7 fa fa fa f7 fa fa fa f7 fa fa fa f7 fa fa fa
  0x5020000fe680: f7 fa fa fa f7 fa fa fa f7 fa fa fa f7 fa fd fa
=>0x5020000fe700: f7 fa 04 fa f7 fa fa fa f7 fa[04]fa f7 fa fd fd
  0x5020000fe780: f7 fa 01 fa f7 fa 00 00 f7 fa fd fd f7 fa 01 fa
  0x5020000fe800: f7 fa fd fd f7 fa fd fa f7 fa fd fa f7 fa fd fa
  0x5020000fe880: f7 fa fd fd f7 fa fd fa f7 fa fd fa f7 fa fd fd
  0x5020000fe900: f7 fa fd fa f7 fa fd fd f7 fa 00 00 f7 fa fd fa
  0x5020000fe980: f7 fa fd fd f7 fa fd fa f7 fa fd fa f7 fa fd fd
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

==2055359==ADDITIONAL INFO

==2055359==Note: Please include this section with the ASan report.
Task trace:
    #0 0x55f741c659f5 in blink::HTMLDocumentParser::ScheduleEndIfDelayed() third_party/blink/renderer/core/html/parser/html_document_parser.cc:905:9
    #1 0x55f734464e92 in IPC::ChannelAssociatedGroupController::Accept(mojo::Message*) ipc/ipc_mojo_bootstrap.cc:1160:13


==2055359==END OF ADDITIONAL INFO
==2055359==ABORTING

```

Initially, it also hits a DCHECK with (possibly) potential security implications:

```
DCheck 1) [2069223:1:0727/160059.471368:FATAL:ruby_utils.cc(1053)] Check failed: false.  LogicalLineItems::size()=1 LogicalRubyColumn::start_index=2863311530

```

Please find the new testcase attached. Thank you!

### ad...@google.com (2024-07-31)

Reclassifying as a vulnerability to assess [#comment7](https://issues.chromium.org/issues/352467338#comment7). (Also, it looks to me like the original report did contain one heap buffer overflow as well as the CHECK failures).

### cl...@appspot.gserviceaccount.com (2024-08-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5100434815385600.

### dc...@chromium.org (2024-08-01)

I'm not sure if this is still a security bug; there is some recent spanification work that means this is now failing in checked iterators.

Unfortunately, I think the underlying bug is probably still there, and prior to spanification, it seems likely that this is a security bug. I'm hoping clusterfuzz will be able to provide a regression range, despite the change in the crash signature.

### dc...@chromium.org (2024-08-01)

The spanification CLs in question: <https://chromium-review.googlesource.com/c/chromium/src/+/5711110> and <https://chromium-review.googlesource.com/c/chromium/src/+/5692639>

### tk...@chromium.org (2024-08-02)

dcheng@ is right.

I confirmed heap-buffer-overflow.html, vector-overflow-variant.html, and LogicalLineBuilder\_BidiReorder\_HeapBufferOverflow\_ASAN.html had runtime CHECK failures, and didn't have security issues with ToT.

The fix CL is in M128 branch. We should merge it to M127 branch, and of course we should fix CHECK failures.

### pe...@google.com (2024-08-02)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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

### tk...@chromium.org (2024-08-02)

Re: #13

1. A fix for a security issue
2. <https://chromium-review.googlesource.com/c/chromium/src/+/5692639>
3. Yes
4. No
5. N/A
6. No manual verification needed.

### pe...@google.com (2024-08-02)

Dear owner, thanks for fixing this bug. We've reopened it because security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security> Thanks for your time!

### am...@chromium.org (2024-08-02)

It's unclear to me what the foundin- should have actually been here but this doesn't seem to be specifically introduced in M127, but I could be wrong.

Why this matters is that this as a heap buffer overflow in the renderer is high severity should be backmerged to both Stable (M127) and Extended Stable (M126).

That being said, <https://crrev.com/c/+/5692639> has had a ton of time on Canary (and dev, and some on beta), so there appear to be no issues there preventing backmerge. It would be helpful to understand if this fix should not be backmerged to M126, so I am going to go ahead and approve that in advance, just in case it should be.

### tk...@chromium.org (2024-08-04)

Re: [#comment16](https://issues.chromium.org/issues/352467338#comment16)

I think we don't need to merge the fix to M126.

The crashing code was introduced by [r1294820](https://chromiumdash.appspot.com/commit/1e3eda9848f805762eaaa0258d1d2531d0c29db1). So M126 contains it.

- But it is guarded by a runtime flag. For M126, users needs to specify `--enable-blink-features=RubyLineBreakable` command-line flag to use the code path.
- I think it started to crash after [r1302421](https://chromiumdash.appspot.com/commit/1786fbc1466286e500b3c1f102b4b1b86c3787eb), which M126 doesn't contain.

### ap...@google.com (2024-08-05)

Project: chromium/src
Branch: refs/branch-heads/6533

commit 8b0190f8d23706a6ea012bbcabd49136627bcf03
Author: Kent Tamura <tkent@chromium.org>
Date:   Mon Aug 05 03:34:22 2024

    Merge "spanification: justification_utils.cc and logical_line_builder.cc" to M127 branch
    
    This CL removes `#pragma allow_unsafe_buffers` from
    justification_utils.cc and logical_line_builder.cc.
    
    Introduces Vector::MakeSpan() and LogicalLineItem::MakeSpan().
    
    This CL should have no behavior changes.
    
    (cherry picked from commit ea0ad868840c7219af0f1abae60e839b7ee94d26)
    
    Bug: 352467338
    Change-Id: Ie0fdbfb6ce5839c59b239a4fff43a3c0fe62e00c
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5692639
    Auto-Submit: Kent Tamura <tkent@chromium.org>
    Reviewed-by: Koji Ishii <kojii@chromium.org>
    Commit-Queue: Koji Ishii <kojii@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1325910}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5759068
    Cr-Commit-Position: refs/branch-heads/6533@{#1896}
    Cr-Branched-From: 7e0b87ec6b8cb5cb2969e1479fc25776e582721d-refs/heads/main@{#1313161}

M       third_party/blink/renderer/core/layout/inline/justification_utils.cc
M       third_party/blink/renderer/core/layout/inline/justification_utils.h
M       third_party/blink/renderer/core/layout/inline/logical_line_builder.cc
M       third_party/blink/renderer/core/layout/inline/logical_line_item.h
M       third_party/blink/renderer/platform/wtf/vector.h

https://chromium-review.googlesource.com/5759068


### am...@chromium.org (2024-08-05)

Thanks for taking care of the merge and the update about this being behind a flag in M126; removed the approval label for M126 since no merge to Extended Stable is needed.

### ap...@google.com (2024-08-05)

Project: chromium/src
Branch: main

commit 14ce1a8697aa91b83cb0f81b90514b83298b4dbc
Author: Kent Tamura <tkent@chromium.org>
Date:   Mon Aug 05 22:20:05 2024

    RubyLB: Fix a crash by RTL + zero-available-width + break-spaces
    
    LineBreaker should not produce an empty LineInfo for ruby-base.
    
    Bug: 352467338
    Change-Id: Ifaa9f300ef9fa22e7697896d8434506f50257dc4
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5759423
    Commit-Queue: Kent Tamura <tkent@chromium.org>
    Reviewed-by: Koji Ishii <kojii@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1337535}

M       third_party/blink/renderer/core/layout/inline/line_breaker.cc
A       third_party/blink/web_tests/external/wpt/css/css-ruby/break-within-bases/break-spaces-crash.html

https://chromium-review.googlesource.com/5759423


### 24...@project.gserviceaccount.com (2024-08-06)

ClusterFuzz testcase 5171017800417280 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1337524:1337540

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### sp...@google.com (2024-08-14)

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

### am...@chromium.org (2024-08-14)

Congratulations on another on Tashita team. Thank you for your efforts and reporting this issue to us!

### ta...@gmail.com (2024-08-16)

Thanks to you, and for the effort you all put into this!

### pe...@google.com (2024-11-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/352467338)*
