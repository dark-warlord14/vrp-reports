# Security DCHECK failed at string_view.h: length <= impl.length() - offset

| Field | Value |
|-------|-------|
| **Issue ID** | [367764861](https://issues.chromium.org/issues/367764861) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Layout>Ruby |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ta...@gmail.com |
| **Assignee** | tk...@chromium.org |
| **Created** | 2024-09-18 |
| **Bounty** | $10,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

## VULNERABILITY DETAILS

`string_view.h Security DCHECK failed: length <= impl.length() - offset`

### Initial Considerations

The `Security DCHECK` was recently introduced on Chrome 129.0.6668.42, but the root cause is an `Integer Overflow` introduced on Chrome 127.0.6533.57 (see Bisect part).

### Stack Trace

```
FATAL:string_view.h(351)] Security DCHECK failed: length <= impl.length() - offset.

```
```
#0  0x000055d154e663cc in ImmediateCrash () at ../../base/immediate_crash.h:176
#1  HandleFatal() () at ../../base/logging.cc:1073
#2  0x000055d154e6571e in operator() () at ../../base/logging.cc:773
#3  InvokeCallback () at ../../third_party/abseil-cpp/absl/cleanup/internal/cleanup.h:87
#4  ~Cleanup () at ../../third_party/abseil-cpp/absl/cleanup/cleanup.h:106
#5  Flush() () at ../../base/logging.cc:956
#6  0x000055d154e667d9 in ~LogMessageFatal() () at ../../base/logging.cc:1078
#7  0x000055d162f47b23 in Set () at ../../third_party/blink/renderer/platform/wtf/text/string_view.h:349
#8  StringView () at ../../third_party/blink/renderer/platform/wtf/text/string_view.h:326
#9  StringView () at ../../third_party/blink/renderer/platform/wtf/text/wtf_string.h:734
#10 BuildJustificationText() () at ../../third_party/blink/renderer/core/layout/inline/justification_utils.cc:78
#11 0x000055d162f45bce in ApplyJustificationInternal() () at ../../third_party/blink/renderer/core/layout/inline/justification_utils.cc:299
#12 0x000055d162fd966f in ApplyRubyAlign() () at ../../third_party/blink/renderer/core/layout/inline/ruby_utils.cc:455
#13 0x000055d162fafeed in PlaceRubyAnnotation() () at ../../third_party/blink/renderer/core/layout/inline/logical_line_builder.cc:514
#14 0x000055d162fada02 in PlaceRubyColumn() () at ../../third_party/blink/renderer/core/layout/inline/logical_line_builder.cc:500
#15 0x000055d162fa8d8c in HandleItemResults() () at ../../third_party/blink/renderer/core/layout/inline/logical_line_builder.cc:175
#16 0x000055d162fa809d in CreateLine() () at ../../third_party/blink/renderer/core/layout/inline/logical_line_builder.cc:72
#17 0x000055d162c8eacb in CreateLine() () at ../../third_party/blink/renderer/core/layout/inline/inline_layout_algorithm.cc:393
#18 0x000055d162c98841 in Layout() () at ../../third_party/blink/renderer/core/layout/inline/inline_layout_algorithm.cc:1266
#19 0x000055d162c352d5 in Layout() () at ../../third_party/blink/renderer/core/layout/inline/inline_node.cc:1683
#20 0x000055d162e585e7 in LayoutInflow() () at ../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:125
#21 0x000055d162e57a52 in HandleInflow() () at ../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:2126
#22 0x000055d162e376f2 in Layout() () at ../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:980
#23 0x000055d162e3cbde in LayoutWithSimpleInlineChildLayoutContext() () at ../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:599
#24 0x000055d162e3510a in LayoutInlineChild() () at ../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:592
#25 0x000055d162e34f7d in Layout() () at ../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:530
#26 0x000055d162d4cc29 in operator()<blink::BlockLayoutAlgorithm> () at ../../third_party/blink/renderer/core/layout/block_node.cc:214
#27 CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, (lambda at ../../third_party/blink/renderer/core/layout/block_node.cc:213:28)>(void) () at ../../third_party/blink/renderer/core/layout/block_node.cc:120
#28 0x000055d162d338c1 in LayoutWithAlgorithm () at ../../third_party/blink/renderer/core/layout/block_node.cc:212
#29 Layout() () at ../../third_party/blink/renderer/core/layout/block_node.cc:523
#30 0x000055d162e58683 in LayoutBlockChild () at ../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:113
#31 LayoutInflow() () at ../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:128
#32 0x000055d162e57a52 in HandleInflow() () at ../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:2126
#33 0x000055d162e376f2 in Layout() () at ../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:980
#34 0x000055d162e34f8f in Layout() () at ../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:532
#35 0x000055d162d4cc29 in operator()<blink::BlockLayoutAlgorithm> () at ../../third_party/blink/renderer/core/layout/block_node.cc:214
#36 CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, (lambda at ../../third_party/blink/renderer/core/layout/block_node.cc:213:28)>(void) () at ../../third_party/blink/renderer/core/layout/block_node.cc:120
#37 0x000055d162d338c1 in LayoutWithAlgorithm () at ../../third_party/blink/renderer/core/layout/block_node.cc:212
#38 Layout() () at ../../third_party/blink/renderer/core/layout/block_node.cc:523
#39 0x000055d162e58683 in LayoutBlockChild () at ../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:113
#40 LayoutInflow() () at ../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:128
#41 0x000055d162e57a52 in HandleInflow() () at ../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:2126
#42 0x000055d162e376f2 in Layout() () at ../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:980
#43 0x000055d162e34f8f in Layout() () at ../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:532
#44 0x000055d162d4cc29 in operator()<blink::BlockLayoutAlgorithm> () at ../../third_party/blink/renderer/core/layout/block_node.cc:214
#45 CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, (lambda at ../../third_party/blink/renderer/core/layout/block_node.cc:213:28)>(void) () at ../../third_party/blink/renderer/core/layout/block_node.cc:120
#46 0x000055d162d338c1 in LayoutWithAlgorithm () at ../../third_party/blink/renderer/core/layout/block_node.cc:212
#47 Layout() () at ../../third_party/blink/renderer/core/layout/block_node.cc:523
#48 0x000055d162e49807 in LayoutBlockChild () at ../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:113
#49 LayoutNewFormattingContext() () at ../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1940
#50 0x000055d162e46abd in HandleNewFormattingContext() () at ../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1725
#51 0x000055d162e377dc in Layout() () at ../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:975
#52 0x000055d162e34f8f in Layout() () at ../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:532
#53 0x000055d162d4cc29 in operator()<blink::BlockLayoutAlgorithm> () at ../../third_party/blink/renderer/core/layout/block_node.cc:214
#54 CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, (lambda at ../../third_party/blink/renderer/core/layout/block_node.cc:213:28)>(void) () at ../../third_party/blink/renderer/core/layout/block_node.cc:120
#55 0x000055d162d338c1 in LayoutWithAlgorithm () at ../../third_party/blink/renderer/core/layout/block_node.cc:212
#56 Layout() () at ../../third_party/blink/renderer/core/layout/block_node.cc:523
#57 0x000055d16319de6f in LayoutRoot() () at ../../third_party/blink/renderer/core/layout/layout_view.cc:809
#58 0x000055d161f3df20 in PerformLayout() () at ../../third_party/blink/renderer/core/frame/local_frame_view.cc:783
#59 0x000055d161f40102 in UpdateLayout() () at ../../third_party/blink/renderer/core/frame/local_frame_view.cc:842
#60 0x000055d161f5cda3 in UpdateStyleAndLayoutInternal() () at ../../third_party/blink/renderer/core/frame/local_frame_view.cc:3177
#61 0x000055d161f48f36 in UpdateStyleAndLayout() () at ../../third_party/blink/renderer/core/frame/local_frame_view.cc:3107
#62 0x000055d164e4ac4c in UpdateStyleAndLayout() () at ../../third_party/blink/renderer/core/dom/document.cc:2827
#63 0x000055d164e5f8dc in ImplicitClose() () at ../../third_party/blink/renderer/core/dom/document.cc:3984
#64 0x000055d164e6068c in CheckCompletedInternal() () at ../../third_party/blink/renderer/core/dom/document.cc:4073
#65 0x000055d164e5ee93 in CheckCompleted() () at ../../third_party/blink/renderer/core/dom/document.cc:4035
#66 0x000055d1634a99ca in FinishedParsing() () at ../../third_party/blink/renderer/core/loader/frame_loader.cc:449
#67 0x000055d164e9a370 in FinishedParsing() () at ../../third_party/blink/renderer/core/dom/document.cc:7499
#68 0x000055d16517f773 in end () at ../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:1075
#69 AttemptToRunDeferredScriptsAndEnd () at ../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:1088
#70 PrepareToStopParsing() () at ../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:566
#71 0x000055d16518524a in AttemptToEnd() () at ../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:1112
#72 0x000055d16518011f in PumpTokenizerIfPossible() () at ../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:651
#73 0x000055d1651808fb in DeferredPumpTokenizerIfPossible() () at ../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:620
#74 0x000055d16519ebad in Invoke<void (blink::HTMLDocumentParser::*)(bool, base::TimeTicks), cppgc::internal::BasicPersistent<blink::HTMLDocumentParser, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, bool, base::TimeTicks> () at ../../base/functional/bind_internal.h:738
#75 MakeItSo<void (blink::HTMLDocumentParser::*)(bool, base::TimeTicks), std::__Cr::tuple<cppgc::internal::BasicPersistent<blink::HTMLDocumentParser, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, bool, base::TimeTicks> > () at ../../base/functional/bind_internal.h:930
#76 RunImpl<void (blink::HTMLDocumentParser::*)(bool, base::TimeTicks), std::__Cr::tuple<cppgc::internal::BasicPersistent<blink::HTMLDocumentParser, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, bool, base::TimeTicks>, 0ul, 1ul, 2ul> () at ../../base/functional/bind_internal.h:1067
#77 RunOnce() () at ../../base/functional/bind_internal.h:980
#78 0x000055d154f98f45 in Run () at ../../base/functional/callback.h:156
#79 RunTaskImpl() () at ../../base/task/common/task_annotator.cc:203
#80 0x000055d155001057 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:486:11)> () at ../../base/task/common/task_annotator.h:90
#81 DoWorkImpl() () at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:484
#82 0x000055d154fffdeb in DoWork() () at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346


```
### Reproduction Steps

1. Use any Chromium starting from 129.0.6668.42 ASAN up until trunk.
2. Set up a HTTP Server in the directory of the repro.
3. Launch Chromium with the repro as usual `./chrome URL_TO/security_dcheck_reduced.html`.
4. It should hit the `SECURITY_DCHECK` mentioned on the Stack Trace.

### Root Cause

#### SECURITY\_DCHECK

The evaluation of the `SECURITY_DCHECK` is: `SECURITY_DCHECK(length <= impl.length() - offset)`. The values at the invalid check when using the `security_dcheck_reduced.html` testcase are:

```
length: 0xffffffff
impl.length(): 0x3
offset: 0x1

```

At that moment, `length` has suffered an `Integer Overflow`.

#### The Integer Overflow

```
std::optional<LayoutUnit> ApplyJustificationInternal(
    LayoutUnit space,
    JustificationTarget target,
    const LineInfo& line_info,
    InlineItemResults* results) {

  ...

  unsigned end_offset = line_info.EndOffsetForJustify(); //(A)

  ...

  const unsigned line_text_start_offset =
      line_info.Results().front().StartOffset(); //(B)

  ...

  String line_text = BuildJustificationText(
      text_content, line_info.Results(), line_text_start_offset, end_offset,
      line_info.MayHaveTextCombineOrRubyItem()); //(C)

  ... 

```

The variable `end_offset` (A) is assigned a value of 0, while `line_text_start_offset` (B) is set to 1. Both variables, `end_offset` (A) and `line_text_start_offset` (B), are passed as arguments to the `BuildJustificationText` (C) function.

```
String BuildJustificationText(const String& text_content,
                              const InlineItemResults& results,
                              unsigned line_text_start_offset,
                              unsigned end_offset,
                              bool may_have_text_combine_or_ruby) {

  ...

  } else {
    line_text_builder.Append(StringView(text_content,
                                        line_text_start_offset,
                                        end_offset - line_text_start_offset)); //(D) and (E)
  }

  ...

```

The variables `end_offset` and `line_text_start_offset` are subtracted (D), resulting in a value of -1. As both are `unsigned`, the resulting value of `0xffffffff` is passed to the `StringView` constructor (E).

```
inline StringView::StringView(const StringImpl* impl,
                              unsigned offset,
                              unsigned length) {
  impl ? Set(*impl, offset, length) : Clear(); //(F)
}

```

The parameter `length` of `StringView` is set to `0xffffffff`.

```
inline void StringView::Set(const StringImpl& impl,
                            unsigned offset,
                            unsigned length) { //(G)
  ...

  SECURITY_DCHECK(length <= impl.length() - offset); //(H)
  length_ = length;

  ...
}

```

`StringView::Set` receives it (G), triggering the `SECURITY_DCHECK` (H)

#### Integer Overflow: Root Cause

The `LineInfo` being computed is not updated before executing "Justification" operations, leading to a mismatch between the actions performed and the `LineInfo` involved.

This can be observed following the `text_align_` member of the `LineInfo` being computed on the "Justification" operations. It contains the value of `ETextAlign::kWebkitCenter` but it should be `ETextAlign::kJustify`.

This is proved on `EndOffsetForJustify` method at `line_info.h` file, as the `DCHECK_EQ` (I) is hit by the testcase:

`FATAL:line_info.h(211)] Check failed: text_align_ == ETextAlign::kJustify (-webkit-center vs. justify)`.

```
  unsigned EndOffsetForJustify() const {
    DCHECK_EQ(text_align_, ETextAlign::kJustify); //(I)
    return end_offset_for_justify_;
  }

```

This mismatch begins at `ApplyRubyAlign` function of `ruby_utils.cc` file:

```
std::pair<LayoutUnit, LayoutUnit> ApplyRubyAlign(LayoutUnit available_line_size,
                                                 bool on_start_edge,
                                                 bool on_end_edge,
                                                 LineInfo& line_info) {
  ...
  
  ETextAlign text_align = line_info.TextAlign(); //(J)

  	...

    case ERubyAlign::kSpaceBetween:
      on_start_edge = true;
      on_end_edge = true;
      text_align = ETextAlign::kJustify; //(K)
      break;

    ...

  ...

  if (text_align == ETextAlign::kJustify) {
    
    //(L)
    
    ...

    std::optional<LayoutUnit> inset =
        ApplyJustification(space, target, &line_info); //(M)

```

First, `text_align` (J) starts with the value `ETextAlign::kWebkitCenter`.
Second, `text_align` (K) value is modified, set as `ETextAlign::kJustify`.
Third, `if condition` is taken to peform `Justification` operations (L).
Fourth, a non-updated `line_info` is passed as argument (M), which mismatches with the `Justification` operations to be performed.

Resulting on the `Integer Overflow` described before.

### The Patch

Proposal patch is attached as: `line_info_int_overflow_proposal.patch`

Before jumping into "Justification" operations (via `ApplyJustification` function), `line_info` should be updated by setting `is_ruby_base_` and updating the "Text Align" to set a value to `end_offset_for_justify_`.
This can be performed by adding the calls to the methods: `SetIsRubyBase` (N) and `UpdateTextAlign` (O).

```
std::pair<LayoutUnit, LayoutUnit> ApplyRubyAlign(LayoutUnit available_line_size,
                                                 bool on_start_edge,
                                                 bool on_end_edge,
                                                 LineInfo& line_info) {
    ...

    case ERubyAlign::kSpaceBetween:
      on_start_edge = true;
      on_end_edge = true;
      text_align = ETextAlign::kJustify;
      line_info.SetIsRubyBase(); //(N)
      line_info.UpdateTextAlign(); //(O)
      break;

    ...


```
### Bisect: Introduced Commit

- `SECURITY_DCHECK` introduced at (Branch Base Position: 1340005) <https://chromium.googlesource.com/chromium/src/+/ba40b993a6b700a2ad0fd092e141783fb1f60e70>
- `Integer Overflow` introduced on the `RubyLB Feature` at: (Branch Base Position: 1309784) <https://chromium.googlesource.com/chromium/src/+/4edb29252ec52fade80d54f37c5bd18eedbf98cd> but protected under flags: `--enable-features=RubyLineBreakable,CssRubyAlign,RubyLineEdgeAlignment,RubyShortHeuristics`
- `RubyLB Feature` enabled at (Branch Base Position: 1312396) <https://chromium.googlesource.com/chromium/src/+/71b76b57de06ee85121019c56e0a320dbae03073>

### Bisect: Introduced Major Chrome

`Integer Overflow` - Chrome Stable: 127.0.6533.57

`SECURITY_DCHECK` - Chrome Stable: 129.0.6668.42

## VERSION

Chrome Version: [129.0.6668.42] + [stable]
Operating System: [All]

## REPRODUCTION CASE

Attached: `security_dcheck_reduced.html`

## PATCH

Attached: `line_info_int_overflow_proposal.patch`

## FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: [Browser]

## CREDIT INFORMATION

Reporter credit: Tashita Software Security

## Attachments

- [security_dcheck_reduced.html](attachments/security_dcheck_reduced.html) (text/html, 361 B)
- [line_info_int_overflow_proposal.patch](attachments/line_info_int_overflow_proposal.patch) (text/x-diff, 829 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-09-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5396075288395776.

### ma...@google.com (2024-09-18)

Thank you for the detailed report and root cause analysis, nice work!

Setting Severity High/S1 for memory corruption potentially leading to a renderer compromise.

From what I can tell, the RubyLB feature was enabled, but only for Chromium developer builds and maybe some bots, in <https://chromium.googlesource.com/chromium/src/+/71b76b57de06ee85121019c56e0a320dbae03073>. My understanding is that this is not enabled by default for any of our Chrome Stable population. (However, cautiously setting FoundIn to current Extended Stable for now.)

tkent@, could you PTAL? Does this issue affect stable channel users at all?

### tk...@chromium.org (2024-09-19)

> Does this issue affect stable channel users at all?

Yes. RubyLB was enabled by default for M128. So a fix for this issue should be merged to M128, M129, and M130.

### ap...@google.com (2024-09-19)

Project: chromium/src
Branch: main

commit 56be91796b858a088f67add4e074b9b016f25757
Author: Kent Tamura <tkent@chromium.org>
Date:   Thu Sep 19 03:15:18 2024

    RubyLB: Fix a crash with a parent with a non-default text-align
    
    Update the LineInfo::GetTextAlign() logic so that it align with
    ApplyRubyAlign() behavior.
    
    This CL also removes stale comments.
    
    Bug: 367764861
    Change-Id: Idfe0f3c2f77c7a33ff9317c2b0f36ffa397405d1
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5874482
    Commit-Queue: Koji Ishii <kojii@chromium.org>
    Reviewed-by: Koji Ishii <kojii@chromium.org>
    Auto-Submit: Kent Tamura <tkent@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1357460}

M       third_party/blink/renderer/core/layout/inline/line_info.cc
A       third_party/blink/web_tests/fast/ruby/ruby-align-in-text-align-crash.html

https://chromium-review.googlesource.com/5874482


### pe...@google.com (2024-09-19)

Setting milestone because of s0/s1 severity.

### 24...@project.gserviceaccount.com (2024-09-19)

ClusterFuzz testcase 5396075288395776 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1357458:1357460

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### pe...@google.com (2024-09-20)

**Merge approved:** your change passed merge requirements and is auto-approved for M130. Please go ahead and merge the CL to branch 6723 (refs/branch-heads/6723) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: eakpobaro (Android), eakpobaro (iOS), gmpritchard (ChromeOS), danielyip (Desktop)

### pe...@google.com (2024-09-20)

Merge review required: M129 is already shipping to stable.

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
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

### pe...@google.com (2024-09-20)

Merge review required: M128 is already shipping to stable.

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

### am...@chromium.org (2024-09-23)

merges approved for M129 and M128, please merge this fix (<https://crrev.com/c/5874482>) to M129 / branch 6668 and M128 / branch 6613 at your earliest convenience.

Note: M129 Stable RC for weekly security respin is being cut today at 10am Pacific; if merges cannot be completed until that time, this fix can go into next week's Stable channel update

### ap...@google.com (2024-09-23)

Project: chromium/src
Branch: refs/branch-heads/6613

commit ef8ddcab1d8eda46254ac92614fa53699dda4ef3
Author: Kent Tamura <tkent@chromium.org>
Date:   Mon Sep 23 18:53:40 2024

    RubyLB: Fix a crash with a parent with a non-default text-align
    
    Update the LineInfo::GetTextAlign() logic so that it align with
    ApplyRubyAlign() behavior.
    
    This CL also removes stale comments.
    
    (cherry picked from commit 56be91796b858a088f67add4e074b9b016f25757)
    
    Bug: 367764861
    Change-Id: Idfe0f3c2f77c7a33ff9317c2b0f36ffa397405d1
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5874482
    Commit-Queue: Koji Ishii <kojii@chromium.org>
    Reviewed-by: Koji Ishii <kojii@chromium.org>
    Auto-Submit: Kent Tamura <tkent@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1357460}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5882457
    Owners-Override: Prudhvikumar Bommana <pbommana@google.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Auto-Submit: Prudhvikumar Bommana <pbommana@google.com>
    Commit-Queue: Prudhvikumar Bommana <pbommana@google.com>
    Cr-Commit-Position: refs/branch-heads/6613@{#2032}
    Cr-Branched-From: 03c1799e6f9c7239802827eab5e935b9e14fceae-refs/heads/main@{#1331488}

M       third_party/blink/renderer/core/layout/inline/line_info.cc
A       third_party/blink/web_tests/fast/ruby/ruby-align-in-text-align-crash.html

https://chromium-review.googlesource.com/5882457


### pe...@google.com (2024-09-23)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### sr...@chromium.org (2024-09-23)

I CP'ed and tried to merge, but it had test failures, so please help land it so it can go out next week respin.

### ap...@google.com (2024-09-23)

Project: chromium/src
Branch: refs/branch-heads/6668

commit 9900d924764b82a094b6488c430c69a0867d8ae2
Author: Kent Tamura <tkent@chromium.org>
Date:   Mon Sep 23 23:09:37 2024

    RubyLB: Fix a crash with a parent with a non-default text-align
    
    Update the LineInfo::GetTextAlign() logic so that it align with
    ApplyRubyAlign() behavior.
    
    This CL also removes stale comments.
    
    (cherry picked from commit 56be91796b858a088f67add4e074b9b016f25757)
    
    Bug: 367764861
    Change-Id: Idfe0f3c2f77c7a33ff9317c2b0f36ffa397405d1
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5874482
    Commit-Queue: Koji Ishii <kojii@chromium.org>
    Reviewed-by: Koji Ishii <kojii@chromium.org>
    Auto-Submit: Kent Tamura <tkent@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1357460}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5883637
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Kent Tamura <tkent@chromium.org>
    Owners-Override: Srinivas Sista <srinivassista@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6668@{#1429}
    Cr-Branched-From: 05bc664984ca075216b7f2198c88b9725bfa1b9b-refs/heads/main@{#1343869}

M       third_party/blink/renderer/core/layout/inline/line_info.cc
A       third_party/blink/web_tests/fast/ruby/ruby-align-in-text-align-crash.html

https://chromium-review.googlesource.com/5883637


### ap...@google.com (2024-09-24)

Project: chromium/src
Branch: refs/branch-heads/6723

commit 66a556bd168d36beff7aa351722aa50996fdb2b4
Author: Kent Tamura <tkent@chromium.org>
Date:   Tue Sep 24 00:01:38 2024

    Merge "RubyLB: Fix a crash with a parent with a non-default text-align" to M130 branch
    
    Update the LineInfo::GetTextAlign() logic so that it align with
    ApplyRubyAlign() behavior.
    
    This CL also removes stale comments.
    
    (cherry picked from commit 56be91796b858a088f67add4e074b9b016f25757)
    
    Bug: 367764861
    Change-Id: Idfe0f3c2f77c7a33ff9317c2b0f36ffa397405d1
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5874482
    Commit-Queue: Koji Ishii <kojii@chromium.org>
    Reviewed-by: Koji Ishii <kojii@chromium.org>
    Auto-Submit: Kent Tamura <tkent@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1357460}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5884453
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6723@{#353}
    Cr-Branched-From: 985f2961df230630f9cbd75bd6fe463009855a11-refs/heads/main@{#1356013}

M       third_party/blink/renderer/core/layout/inline/line_info.cc
A       third_party/blink/web_tests/fast/ruby/ruby-align-in-text-align-crash.html

https://chromium-review.googlesource.com/5884453


### qk...@google.com (2024-09-25)

Labeling as LTS-NotApplicable-126 because M126 was not affected according to the author.

### sp...@google.com (2024-09-30)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
high quality report of demonstrated memory corruption in a sandboxed process / the renderer 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-30)

Congratulations Tashita team! Thank you for your efforts and reporting this issue to us!

### ta...@gmail.com (2024-09-30)

Thanks for the quick response and for considering our report as high quality! We really appreciate it!

### pe...@google.com (2024-12-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/367764861)*
