# Integer overflow in HarfBuzz apply_stch() causes heap OOB write via crafted font + Arabic text

| Field | Value |
|-------|-------|
| **Issue ID** | [491516670](https://issues.chromium.org/issues/491516670) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Fonts |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 147.0.7697.0 |
| **Reporter** | pw...@gmail.com |
| **Assignee** | ko...@chromium.org |
| **Created** | 2026-03-11 |
| **Bounty** | $10,000.00 |

## Description

# Steps to reproduce the problem

1. Download poc.html
2. Download win32-release\_x64\_asan-win32-release\_x64-1596789.zip(<https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/win32-release_x64%2Fasan-win32-release_x64-1596789.zip>)
3. In cmd, run `chrome.exe --no-sandbox poc.html`

# Problem Description

### Overview

HarfBuzz's Arabic shaper function `apply_stch()` in `third_party/harfbuzz-ng/src/src/hb-ot-shaper-arabic.cc` has an integer overflow that causes a heap out-of-bounds write. The function uses a 32-bit `unsigned int` to accumulate the number of extra glyphs needed across all "stch" (stretching) spans. By crafting a font with specific glyph advances and supplying Arabic text with enough spans, an attacker can make this counter wrap to zero at exactly 2^32, causing the buffer to not be enlarged. The subsequent copy pass then writes past the buffer boundary.

The vulnerability has existed since HarfBuzz 1.1.0 (November 2015, commit 6e6f82b6f) and affects all Chromium versions shipping HarfBuzz with the `stch` feature enabled.

### Root Cause

`apply_stch()` implements a two-pass algorithm:

MEASURE pass — iterates over all stch spans and accumulates extra glyphs needed:

```
unsigned int extra_glyphs_needed = 0;          // line 498: 32-bit
// per span:
extra_glyphs_needed += n_copies * n_repeating; // line 587: no overflow check

```

Buffer allocation — uses the (now-zero) counter:

```
buffer->ensure(count + extra_glyphs_needed);   // line 632: ensure(count + 0)

```

CUT pass — copies glyphs including n\_copies duplicates per span. The write index `j` (unsigned int) starts at `count` and decrements. After `count` decrements it reaches 0, then wraps to 0xFFFFFFFF. The write `info[0xFFFFFFFF]` accesses memory out of the buffer, hitting unmapped memory and causing SIGSEGV.

### Crafted Font Design

The font uses `upem=16384` (power of 2) to ensure exact arithmetic with Chromium's 16.16 fixed-point scaling (`SkiaScalarToHarfBuzzPosition()` in `skia_text_metrics.cc`):

- ALEF (U+0627): advance = 16384 -> HB position = 1,048,576 (at 16px)
- REPEATING tile: advance = 1 -> HB position = 64
- GSUB `stch` feature: MultipleSubst substitutes BEH -> [FIXED, REPEATING]

Per span (BEH + 1024 ALEFs + TEH):

- `w_total = 1024 × 1,048,576 + 64 = 1,073,741,888` (fits int32)
- `n_copies = 1,073,741,888 / 64 - 1 = 16,777,216`

256 spans: `256 × 16,777,216 = 4,294,967,296 = 2^32 -> wraps to 0`

### Attack Vector

A malicious web page can trigger this by:

1. Embedding a crafted font via `@font-face` (passes OTS validation)
2. Rendering Arabic text with the specific character pattern

No user interaction beyond visiting the page is required. The font passes OTS validation because the `stch` GSUB feature and MultipleSubst lookups are valid OpenType structures.

# Summary

Integer overflow in HarfBuzz apply\_stch() causes heap OOB write via crafted font + Arabic text

# Custom Questions

#### Type of crash:

tab

#### Crash state:

# [24344:18108:0311/102150.774:ERROR:components\device\_event\_log\device\_event\_log\_impl.cc:202] [10:21:50.775] USB: usb\_device\_win.cc:66 Failed to open \?\usb#root\_hub30#4&5375334&0&0#{f18a0e88-c30c-11d0-8815-00a0c906bed8}: Access is denied. (0x5) [24344:20808:0311/102151.566:ERROR:google\_apis\gcm\engine\registration\_request.cc:291] Registration response error message: DEPRECATED\_ENDPOINT

==25032==ERROR: AddressSanitizer: access-violation on unknown address 0x12b8fa1e17ec (pc 0x7ffc610cdc31 bp 0x00b6c8dfa660 sp 0x00b6c8dfa5d8 T0)
==25032==The signal is caused by a WRITE memory access.
==25032==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*
==25032==\*\*\* Most likely this means that the app is already \*\*\*
==25032==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*
==25032==\*\*\* Due to technical reasons, symbolization might crash \*\*\*
==25032==\*\*\* or produce wrong results. \*\*\*
#0 0x7ffc610cdc30 (C:\WINDOWS\System32\ucrtbase.dll+0x1800edc30)
#1 0x7ffbf2a0b4d2 (C:\Users\winwin\Desktop\win32-release\_x64\_asan-win32-release\_x64-1587431\clang\_rt.asan\_dynamic-x86\_64.dll+0x18004b4d2)
#2 0x7ffb84d95e77 in apply\_stch C:\b\s\w\ir\cache\builder\src\third\_party\harfbuzz-ng\src\src\hb-ot-shaper-arabic.cc:616
#3 0x7ffb84d95e77 in postprocess\_glyphs\_arabic C:\b\s\w\ir\cache\builder\src\third\_party\harfbuzz-ng\src\src\hb-ot-shaper-arabic.cc:652:3
#4 0x7ffb84de3846 in hb\_ot\_substitute\_post C:\b\s\w\ir\cache\builder\src\third\_party\harfbuzz-ng\src\src\hb-ot-shape.cc:967
#5 0x7ffb84de3846 in hb\_ot\_shape\_internal C:\b\s\w\ir\cache\builder\src\third\_party\harfbuzz-ng\src\src\hb-ot-shape.cc:1199
#6 0x7ffb84de3846 in \_hb\_ot\_shape C:\b\s\w\ir\cache\builder\src\third\_party\harfbuzz-ng\src\src\hb-ot-shape.cc:1217:3
#7 0x7ffb84ddb182 in \_hb\_shape\_plan\_execute\_internal C:\b\s\w\ir\cache\builder\src\third\_party\harfbuzz-ng\src\src\hb-shaper-list.hh:47
#8 0x7ffb84ddb182 in hb\_shape\_plan\_execute C:\b\s\w\ir\cache\builder\src\third\_party\harfbuzz-ng\src\src\hb-shape-plan.cc:452:14
#9 0x7ffb860c240a in hb\_shape\_full C:\b\s\w\ir\cache\builder\src\third\_party\harfbuzz-ng\src\src\hb-shape.cc:150:19
#10 0x7ffb860c24a1 in hb\_shape C:\b\s\w\ir\cache\builder\src\third\_party\harfbuzz-ng\src\src\hb-shape.cc:194:3
#11 0x7ffb91e3acf4 in blink::`anonymous namespace'::ShapeRange C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\fonts\shaping\harfbuzz_shaper.cc:339:3 #12 0x7ffb91e38805 in blink::HarfBuzzShaper::ShapeSegment(struct blink::RangeContext *, struct blink::RunSegmenter::RunSegmenterRange const &, class blink::ShapeResult *) const C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\fonts\shaping\harfbuzz_shaper.cc:1024:10 #13 0x7ffb91e3cb05 in blink::HarfBuzzShaper::Shape(class blink::Font const *, enum blink::TextDirection, unsigned int, unsigned int, struct blink::RunSegmenter::RunSegmenterRange, struct blink::ShapeOptions) const C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\fonts\shaping\harfbuzz_shaper.cc:1148:3 #14 0x7ffb8eaa0e91 in blink::`anonymous namespace'::ReusingTextShaper::Reshape C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\inline\inline\_node.cc:308
#15 0x7ffb8eaa0e91 in blink::`anonymous namespace'::ReusingTextShaper::ShapeWithoutCache C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\inline\inline_node.cc:186 #16 0x7ffb8eaa0e91 in blink::`anonymous namespace'::ReusingTextShaper::Shape::<lambda\_1>::operator() C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\inline\inline\_node.cc:169:14
#17 0x7ffb8ea84d91 in blink::NGShapeCache::GetOrCreate C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\fonts\shaping\ng\_shape\_cache.h:112
#18 0x7ffb8ea84d91 in blink::`anonymous namespace'::ReusingTextShaper::Shape C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\inline\inline_node.cc:172 #19 0x7ffb8ea84d91 in blink::InlineNode::ShapeText(struct blink::InlineItemsData *, class blink::String const *, class blink::BasicHeapVector<1, class cppgc::internal::BasicMember<class blink::InlineItem, class cppgc::internal::StrongMemberTag, struct cppgc::internal::DijkstraWriteBarrierPolicy, class cppgc::internal::DisabledCheckingPolicy, class cppgc::internal::CompressedPointer>, 0> const *, class blink::Font const *) const C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\inline\inline_node.cc:1658:16 #20 0x7ffb8ea71512 in blink::InlineNode::ShapeTextIncludingFirstLine(struct blink::InlineNodeData *, class blink::String const *, class blink::BasicHeapVector<1, class cppgc::internal::BasicMember<class blink::InlineItem, class cppgc::internal::StrongMemberTag, struct cppgc::internal::DijkstraWriteBarrierPolicy, class cppgc::internal::DisabledCheckingPolicy, class cppgc::internal::CompressedPointer>, 0> const *) const C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\inline\inline_node.cc:1803:3 #21 0x7ffb8ea70134 in blink::InlineNode::PrepareLayout(struct blink::InlineNodeData *) const C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\inline\inline_node.cc:664:3 #22 0x7ffb8ea6fae5 in blink::InlineNode::PrepareLayoutIfNeeded(void) const C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\inline\inline_node.cc:648:3 #23 0x7ffb8ea7a476 in blink::InlineNode::EnsureData(void) const C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\inline\inline_node.cc:1042:3 #24 0x7ffb8ef6f0af in blink::InlineNode::IsBlockLevel C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\inline\inline_node.h:106 #25 0x7ffb8ef6f0af in blink::BlockNode::FirstChild(void) const C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:1156:20 #26 0x7ffb8ef70313 in blink::BlockNode::IsInlineFormattingContextRoot(class blink::InlineNode *) const C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:1303:35 #27 0x7ffb8ef8d7e1 in blink::BlockLayoutAlgorithm::Layout(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_layout_algorithm.cc:599:14 #28 0x7ffb8ef768ae in blink::`anonymous namespace'::LayoutWithAlgorithm::<lambda\_1>::operator() C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\block\_node.cc:197
#29 0x7ffb8ef768ae in blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm,`lambda at ....\third\_party\blink\renderer\core\layout\block\_node.cc:196:28'> C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\block\_node.cc:109:3
#30 0x7ffb8ef61ddc in blink::`anonymous namespace'::LayoutWithAlgorithm C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:195 #31 0x7ffb8ef61ddc in blink::BlockNode::Layout(class blink::ConstraintSpace const &, class blink::BlockBreakToken const *, class blink::EarlyBreak const *, class blink::ColumnSpannerPath const *) const C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:553:21 #32 0x7ffb8efa1448 in blink::`anonymous namespace'::LayoutBlockChild C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\block\_layout\_algorithm.cc:119
#33 0x7ffb8efa1448 in blink::BlockLayoutAlgorithm::LayoutNewFormattingContext(class blink::LayoutInputNode, class blink::BlockBreakToken const \*, struct blink::InflowChildData const &, struct blink::BfcOffset, bool, struct blink::BfcOffset \*, struct blink::BoxStrut \*) C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\block\_layout\_algorithm.cc:2166:41
#34 0x7ffb8ef9e7e4 in blink::BlockLayoutAlgorithm::HandleNewFormattingContext(class blink::LayoutInputNode, class blink::BlockBreakToken const \*, struct blink::PreviousInflowPosition \*) C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\block\_layout\_algorithm.cc:1941:39
#35 0x7ffb8ef8ff56 in blink::BlockLayoutAlgorithm::Layout(class blink::InlineChildLayoutContext \*) C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\block\_layout\_algorithm.cc:1084:18
#36 0x7ffb8ef8d801 in blink::BlockLayoutAlgorithm::Layout(void) C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\block\_layout\_algorithm.cc:602:14
#37 0x7ffb8ef768ae in blink::`anonymous namespace'::LayoutWithAlgorithm::<lambda_1>::operator() C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:197 #38 0x7ffb8ef768ae in blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm,`lambda at ..\..\third_party\blink\renderer\core\layout\block_node.cc:196:28'> C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:109:3 #39 0x7ffb8ef61ddc in blink::`anonymous namespace'::LayoutWithAlgorithm C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\block\_node.cc:195
#40 0x7ffb8ef61ddc in blink::BlockNode::Layout(class blink::ConstraintSpace const &, class blink::BlockBreakToken const \*, class blink::EarlyBreak const \*, class blink::ColumnSpannerPath const \*) const C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\block\_node.cc:553:21
#41 0x7ffb8efb0aae in blink::`anonymous namespace'::LayoutBlockChild C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_layout_algorithm.cc:119 #42 0x7ffb8efb0aae in blink::`anonymous namespace'::LayoutInflow C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\block\_layout\_algorithm.cc:134:10
#43 0x7ffb8efafd47 in blink::BlockLayoutAlgorithm::HandleInflow(class blink::LayoutInputNode, class blink::BreakToken const \*, struct blink::PreviousInflowPosition \*, class blink::InlineChildLayoutContext \*, class blink::InlineBreakToken const \*\*) C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\block\_layout\_algorithm.cc:2350:7
#44 0x7ffb8ef8ffca in blink::BlockLayoutAlgorithm::Layout(class blink::InlineChildLayoutContext \*) C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\block\_layout\_algorithm.cc:1089:18
#45 0x7ffb8ef8d801 in blink::BlockLayoutAlgorithm::Layout(void) C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\block\_layout\_algorithm.cc:602:14
#46 0x7ffb8ef768ae in blink::`anonymous namespace'::LayoutWithAlgorithm::<lambda_1>::operator() C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:197 #47 0x7ffb8ef768ae in blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm,`lambda at ..\..\third_party\blink\renderer\core\layout\block_node.cc:196:28'> C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:109:3 #48 0x7ffb8ef61ddc in blink::`anonymous namespace'::LayoutWithAlgorithm C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\block\_node.cc:195
#49 0x7ffb8ef61ddc in blink::BlockNode::Layout(class blink::ConstraintSpace const &, class blink::BlockBreakToken const \*, class blink::EarlyBreak const \*, class blink::ColumnSpannerPath const \*) const C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\block\_node.cc:553:21
#50 0x7ffb8efb0aae in blink::`anonymous namespace'::LayoutBlockChild C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_layout_algorithm.cc:119 #51 0x7ffb8efb0aae in blink::`anonymous namespace'::LayoutInflow C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\block\_layout\_algorithm.cc:134:10
#52 0x7ffb8efafd47 in blink::BlockLayoutAlgorithm::HandleInflow(class blink::LayoutInputNode, class blink::BreakToken const \*, struct blink::PreviousInflowPosition \*, class blink::InlineChildLayoutContext \*, class blink::InlineBreakToken const \*\*) C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\block\_layout\_algorithm.cc:2350:7
#53 0x7ffb8ef8ffca in blink::BlockLayoutAlgorithm::Layout(class blink::InlineChildLayoutContext \*) C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\block\_layout\_algorithm.cc:1089:18
#54 0x7ffb8ef8d801 in blink::BlockLayoutAlgorithm::Layout(void) C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\block\_layout\_algorithm.cc:602:14
#55 0x7ffb8ef768ae in blink::`anonymous namespace'::LayoutWithAlgorithm::<lambda_1>::operator() C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:197 #56 0x7ffb8ef768ae in blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm,`lambda at ..\..\third_party\blink\renderer\core\layout\block_node.cc:196:28'> C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:109:3 #57 0x7ffb8ef61ddc in blink::`anonymous namespace'::LayoutWithAlgorithm C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\block\_node.cc:195
#58 0x7ffb8ef61ddc in blink::BlockNode::Layout(class blink::ConstraintSpace const &, class blink::BlockBreakToken const \*, class blink::EarlyBreak const \*, class blink::ColumnSpannerPath const \*) const C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\block\_node.cc:553:21
#59 0x7ffb8efa1448 in blink::`anonymous namespace'::LayoutBlockChild C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_layout_algorithm.cc:119 #60 0x7ffb8efa1448 in blink::BlockLayoutAlgorithm::LayoutNewFormattingContext(class blink::LayoutInputNode, class blink::BlockBreakToken const *, struct blink::InflowChildData const &, struct blink::BfcOffset, bool, struct blink::BfcOffset *, struct blink::BoxStrut *) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_layout_algorithm.cc:2166:41 #61 0x7ffb8ef9e7e4 in blink::BlockLayoutAlgorithm::HandleNewFormattingContext(class blink::LayoutInputNode, class blink::BlockBreakToken const *, struct blink::PreviousInflowPosition *) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_layout_algorithm.cc:1941:39 #62 0x7ffb8ef8ff56 in blink::BlockLayoutAlgorithm::Layout(class blink::InlineChildLayoutContext *) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_layout_algorithm.cc:1084:18 #63 0x7ffb8ef8d801 in blink::BlockLayoutAlgorithm::Layout(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_layout_algorithm.cc:602:14 #64 0x7ffb8ef768ae in blink::`anonymous namespace'::LayoutWithAlgorithm::<lambda\_1>::operator() C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\block\_node.cc:197
#65 0x7ffb8ef768ae in blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm,`lambda at ....\third\_party\blink\renderer\core\layout\block\_node.cc:196:28'> C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\block\_node.cc:109:3
#66 0x7ffb8ef61ddc in blink::`anonymous namespace'::LayoutWithAlgorithm C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:195 #67 0x7ffb8ef61ddc in blink::BlockNode::Layout(class blink::ConstraintSpace const &, class blink::BlockBreakToken const *, class blink::EarlyBreak const *, class blink::ColumnSpannerPath const *) const C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:553:21 #68 0x7ffb8e80155b in blink::LayoutView::LayoutRoot(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_view.cc:908:19 #69 0x7ffb8fdc83b1 in blink::LocalFrameView::PerformLayout(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:791:24 #70 0x7ffb8fdca936 in blink::LocalFrameView::UpdateLayout(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:848:3 #71 0x7ffb8fdea028 in blink::LocalFrameView::UpdateStyleAndLayoutInternal(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:3427:7 #72 0x7ffb8fdd43ef in blink::LocalFrameView::UpdateStyleAndLayout(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:3353:18 #73 0x7ffb927f7f7d in blink::Document::UpdateStyleAndLayout(enum blink::DocumentUpdateReason) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:3092:17 #74 0x7ffb9043baca in blink::FrameSelection::SetSelectionFromNone(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\frame_selection.cc:1291:17 #75 0x7ffb9043b572 in blink::FrameSelection::FocusedOrActiveStateChanged(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\frame_selection.cc:1065:5 #76 0x7ffb7bf0c9d2 in blink::mojom::blink::FrameWidgetStubDispatch::Accept(class blink::mojom::blink::FrameWidget *, class mojo::Message *) C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\third_party\blink\public\mojom\page\widget.mojom-blink.cc:2608:13 #77 0x7ffb82f170f4 in mojo::InterfaceEndpointClient::HandleValidatedMessage(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:1085:54 #78 0x7ffb82f13e3d in mojo::MessageDispatcher::Accept(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:44:19 #79 0x7ffb82f1d7de in mojo::InterfaceEndpointClient::HandleIncomingMessage(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:747:20 #80 0x7ffb8694a5f6 in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread C:\b\s\w\ir\cache\builder\src\ipc\ipc_mojo_bootstrap.cc:1199:24 #81 0x7ffb8694cb11 in base::internal::DecayedFunctorTraits<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::`anonymous namespace'::ScopedUrgentMessageNotification),IPC::ChannelAssociatedGroupController \*&&,mojo::Message &&,IPC::`anonymous namespace'::ScopedUrgentMessageNotification &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:740 #82 0x7ffb8694cb11 in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::`anonymous namespace'::ScopedUrgentMessageNotification),IPC::ChannelAssociatedGroupController \*&&,mojo::Message &&,IPC::`anonymous namespace'::ScopedUrgentMessageNotification &&>,void,0,1,2>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:932 #83 0x7ffb8694cb11 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::`anonymous namespace'::ScopedUrgentMessageNotification),IPC::ChannelAssociatedGroupController \*&&,mojo::Message &&,IPC::`anonymous namespace'::ScopedUrgentMessageNotification &&>,base::internal::BindState<1,1,0,void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::`anonymous namespace'::ScopedUrgentMessageNotification),scoped\_refptr[IPC::ChannelAssociatedGroupController](javascript:void(0);),mojo::Message,IPC::`anonymous namespace'::ScopedUrgentMessageNotification>,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1069 #84 0x7ffb8694cb11 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::`anonymous namespace'::ScopedUrgentMessageNotification),IPC::ChannelAssociatedGroupController \*&&,mojo::Message &&,IPC::`anonymous namespace'::ScopedUrgentMessageNotification &&>,base::internal::BindState<1,1,0,void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::`anonymous namespace'::ScopedUrgentMessageNotification),scoped\_refptr[IPC::ChannelAssociatedGroupController](javascript:void(0);),mojo::Message,IPC::`anonymous namespace'::ScopedUrgentMessageNotification>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:982:12
#85 0x7ffb831ef9d8 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:155
#86 0x7ffb831ef9d8 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:229:34
#87 0x7ffb831bfe21 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.h:112
#88 0x7ffb831bfe21 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow \*) C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:475:23
#89 0x7ffb831bec83 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:346:40
#90 0x7ffb83329920 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:42:55
#91 0x7ffb831c1b6f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:650:12
#92 0x7ffb832675fc in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:135:14
#93 0x7ffb8d7baa93 in content::RendererMain(struct content::MainFunctionParams) C:\b\s\w\ir\cache\builder\src\content\renderer\renderer\_main.cc:364:16
#94 0x7ffb7edf6a16 in content::RunOtherNamedProcessTypeMain(class std::\_\_Cr::basic\_string<char, struct std::\_\_Cr::char\_traits<char>, class std::**Cr::allocator<char>> const &, struct content::MainFunctionParams, class content::ContentMainDelegate \*) C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:762:14
#95 0x7ffb7edf917b in content::ContentMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1152:10
#96 0x7ffb7edecf7f in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner \*) C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:358:36
#97 0x7ffb7eded722 in content::ContentMain(struct content::ContentMainParams) C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:371:10
#98 0x7ffb6ed42b06 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:191:12
#99 0x7ff6fcd24807 in MainDllLoader::Launch(struct HINSTANCE***, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:204:12
#100 0x7ff6fcd22074 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:351:20
#101 0x7ff6fd21ce7f in invoke\_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:78
#102 0x7ff6fd21ce7f in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288
#103 0x7ffc62f6e8d6 (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
#104 0x7ffc6478c40b (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18008c40b)

==25032==Register values:
rax = 12b8fa1e17ec rbx = 12b8fa1e17ec rcx = 12b8fa1e17ec rdx = 12a4fa6e53d8
rdi = 12a4fa6e53d8 rsi = 14 rbp = b6c8dfa660 rsp = b6c8dfa5d8
r8 = 14 r9 = 2571f43c2ff r10 = 7ffc60fe0000 r11 = 0
r12 = 1000000 r13 = 12a4fad053d8 r14 = ffffffff r15 = ffffffffffffffd3
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: access-violation (C:\WINDOWS\System32\ucrtbase.dll+0x1800edc30)

==25032==ADDITIONAL INFO

==25032==Note: Please include this section with the ASan report.
Task trace:
#0 0x7ffb86944419 in IPC::ChannelAssociatedGroupController::Accept(class mojo::Message \*) C:\b\s\w\ir\cache\builder\src\ipc\ipc\_mojo\_bootstrap.cc:1138:13

Command line: `"C:\Users\winwin\Desktop\win32-release_x64_asan-win32-release_x64-1587431\chrome.exe" --type=renderer --unsafely-treat-insecure-origin-as-secure=http://172.30.1.200:8888 --no-pre-read-main-dll --no-sandbox --enable-unsafe-webgpu --file-url-path-alias="/gen=C:\Users\winwin\Desktop\win32-release_x64_asan-win32-release_x64-1587431\gen" --video-capture-use-gpu-memory-buffer --lang=en-US --device-scale-factor=1 --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=8 --time-ticks-at-unix-epoch=-1772769509573503 --launch-time-ticks=422601159186 --metrics-shmem-handle=4316,i,16590150145926551397,3420061095256368019,2097152 --field-trial-handle=1848,i,9800470822139892438,6761809189957616281,262144 --variations-seed-version --pseudonymization-salt-handle=2040,i,8348267116812909868,17333413211753954901,4 --trace-process-track-uuid=3190708993808206286 --mojo-platform-channel-handle=4036 /prefetch:1`

==25032==END OF ADDITIONAL INFO

==25032==ABORTING

#### Reporter credit:

pwn2addr

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [poc.html](attachments/poc.html) (text/html, 3.7 KB)
- [reproduce.webm](attachments/reproduce.webm) (video/webm, 2.1 MB)

## Timeline

### pw...@gmail.com (2026-03-11)

Due to Markdown formatting, I am reattaching the backtrace below.

```
[24344:18108:0311/102150.774:ERROR:components\device_event_log\device_event_log_impl.cc:202] [10:21:50.775] USB: usb_device_win.cc:66 Failed to open \\?\usb#root_hub30#4&5375334&0&0#{f18a0e88-c30c-11d0-8815-00a0c906bed8}: Access is denied. (0x5)
[24344:20808:0311/102151.566:ERROR:google_apis\gcm\engine\registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
=================================================================
==25032==ERROR: AddressSanitizer: access-violation on unknown address 0x12b8fa1e17ec (pc 0x7ffc610cdc31 bp 0x00b6c8dfa660 sp 0x00b6c8dfa5d8 T0)
==25032==The signal is caused by a WRITE memory access.
==25032==*** WARNING: Failed to initialize DbgHelp!              ***
==25032==*** Most likely this means that the app is already      ***
==25032==*** using DbgHelp, possibly with incompatible flags.    ***
==25032==*** Due to technical reasons, symbolization might crash ***
==25032==*** or produce wrong results.                           ***
    #0 0x7ffc610cdc30  (C:\WINDOWS\System32\ucrtbase.dll+0x1800edc30)
    #1 0x7ffbf2a0b4d2  (C:\Users\winwin\Desktop\win32-release_x64_asan-win32-release_x64-1587431\clang_rt.asan_dynamic-x86_64.dll+0x18004b4d2)
    #2 0x7ffb84d95e77 in apply_stch C:\b\s\w\ir\cache\builder\src\third_party\harfbuzz-ng\src\src\hb-ot-shaper-arabic.cc:616
    #3 0x7ffb84d95e77 in postprocess_glyphs_arabic C:\b\s\w\ir\cache\builder\src\third_party\harfbuzz-ng\src\src\hb-ot-shaper-arabic.cc:652:3
    #4 0x7ffb84de3846 in hb_ot_substitute_post C:\b\s\w\ir\cache\builder\src\third_party\harfbuzz-ng\src\src\hb-ot-shape.cc:967
    #5 0x7ffb84de3846 in hb_ot_shape_internal C:\b\s\w\ir\cache\builder\src\third_party\harfbuzz-ng\src\src\hb-ot-shape.cc:1199
    #6 0x7ffb84de3846 in _hb_ot_shape C:\b\s\w\ir\cache\builder\src\third_party\harfbuzz-ng\src\src\hb-ot-shape.cc:1217:3
    #7 0x7ffb84ddb182 in _hb_shape_plan_execute_internal C:\b\s\w\ir\cache\builder\src\third_party\harfbuzz-ng\src\src\hb-shaper-list.hh:47
    #8 0x7ffb84ddb182 in hb_shape_plan_execute C:\b\s\w\ir\cache\builder\src\third_party\harfbuzz-ng\src\src\hb-shape-plan.cc:452:14
    #9 0x7ffb860c240a in hb_shape_full C:\b\s\w\ir\cache\builder\src\third_party\harfbuzz-ng\src\src\hb-shape.cc:150:19
    #10 0x7ffb860c24a1 in hb_shape C:\b\s\w\ir\cache\builder\src\third_party\harfbuzz-ng\src\src\hb-shape.cc:194:3
    #11 0x7ffb91e3acf4 in blink::`anonymous namespace'::ShapeRange C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\fonts\shaping\harfbuzz_shaper.cc:339:3
    #12 0x7ffb91e38805 in blink::HarfBuzzShaper::ShapeSegment(struct blink::RangeContext *, struct blink::RunSegmenter::RunSegmenterRange const &, class blink::ShapeResult *) const C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\fonts\shaping\harfbuzz_shaper.cc:1024:10
    #13 0x7ffb91e3cb05 in blink::HarfBuzzShaper::Shape(class blink::Font const *, enum blink::TextDirection, unsigned int, unsigned int, struct blink::RunSegmenter::RunSegmenterRange, struct blink::ShapeOptions) const C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\fonts\shaping\harfbuzz_shaper.cc:1148:3
    #14 0x7ffb8eaa0e91 in blink::`anonymous namespace'::ReusingTextShaper::Reshape C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\inline\inline_node.cc:308
    #15 0x7ffb8eaa0e91 in blink::`anonymous namespace'::ReusingTextShaper::ShapeWithoutCache C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\inline\inline_node.cc:186
    #16 0x7ffb8eaa0e91 in blink::`anonymous namespace'::ReusingTextShaper::Shape::<lambda_1>::operator() C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\inline\inline_node.cc:169:14
    #17 0x7ffb8ea84d91 in blink::NGShapeCache::GetOrCreate C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\fonts\shaping\ng_shape_cache.h:112
    #18 0x7ffb8ea84d91 in blink::`anonymous namespace'::ReusingTextShaper::Shape C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\inline\inline_node.cc:172
    #19 0x7ffb8ea84d91 in blink::InlineNode::ShapeText(struct blink::InlineItemsData *, class blink::String const *, class blink::BasicHeapVector<1, class cppgc::internal::BasicMember<class blink::InlineItem, class cppgc::internal::StrongMemberTag, struct cppgc::internal::DijkstraWriteBarrierPolicy, class cppgc::internal::DisabledCheckingPolicy, class cppgc::internal::CompressedPointer>, 0> const *, class blink::Font const *) const C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\inline\inline_node.cc:1658:16
    #20 0x7ffb8ea71512 in blink::InlineNode::ShapeTextIncludingFirstLine(struct blink::InlineNodeData *, class blink::String const *, class blink::BasicHeapVector<1, class cppgc::internal::BasicMember<class blink::InlineItem, class cppgc::internal::StrongMemberTag, struct cppgc::internal::DijkstraWriteBarrierPolicy, class cppgc::internal::DisabledCheckingPolicy, class cppgc::internal::CompressedPointer>, 0> const *) const C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\inline\inline_node.cc:1803:3
    #21 0x7ffb8ea70134 in blink::InlineNode::PrepareLayout(struct blink::InlineNodeData *) const C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\inline\inline_node.cc:664:3
    #22 0x7ffb8ea6fae5 in blink::InlineNode::PrepareLayoutIfNeeded(void) const C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\inline\inline_node.cc:648:3
    #23 0x7ffb8ea7a476 in blink::InlineNode::EnsureData(void) const C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\inline\inline_node.cc:1042:3
    #24 0x7ffb8ef6f0af in blink::InlineNode::IsBlockLevel C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\inline\inline_node.h:106
    #25 0x7ffb8ef6f0af in blink::BlockNode::FirstChild(void) const C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:1156:20
    #26 0x7ffb8ef70313 in blink::BlockNode::IsInlineFormattingContextRoot(class blink::InlineNode *) const C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:1303:35
    #27 0x7ffb8ef8d7e1 in blink::BlockLayoutAlgorithm::Layout(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_layout_algorithm.cc:599:14
    #28 0x7ffb8ef768ae in blink::`anonymous namespace'::LayoutWithAlgorithm::<lambda_1>::operator() C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:197
    #29 0x7ffb8ef768ae in blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm,`lambda at ..\..\third_party\blink\renderer\core\layout\block_node.cc:196:28'> C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:109:3
    #30 0x7ffb8ef61ddc in blink::`anonymous namespace'::LayoutWithAlgorithm C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:195
    #31 0x7ffb8ef61ddc in blink::BlockNode::Layout(class blink::ConstraintSpace const &, class blink::BlockBreakToken const *, class blink::EarlyBreak const *, class blink::ColumnSpannerPath const *) const C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:553:21
    #32 0x7ffb8efa1448 in blink::`anonymous namespace'::LayoutBlockChild C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_layout_algorithm.cc:119
    #33 0x7ffb8efa1448 in blink::BlockLayoutAlgorithm::LayoutNewFormattingContext(class blink::LayoutInputNode, class blink::BlockBreakToken const *, struct blink::InflowChildData const &, struct blink::BfcOffset, bool, struct blink::BfcOffset *, struct blink::BoxStrut *) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_layout_algorithm.cc:2166:41
    #34 0x7ffb8ef9e7e4 in blink::BlockLayoutAlgorithm::HandleNewFormattingContext(class blink::LayoutInputNode, class blink::BlockBreakToken const *, struct blink::PreviousInflowPosition *) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_layout_algorithm.cc:1941:39
    #35 0x7ffb8ef8ff56 in blink::BlockLayoutAlgorithm::Layout(class blink::InlineChildLayoutContext *) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_layout_algorithm.cc:1084:18
    #36 0x7ffb8ef8d801 in blink::BlockLayoutAlgorithm::Layout(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_layout_algorithm.cc:602:14
    #37 0x7ffb8ef768ae in blink::`anonymous namespace'::LayoutWithAlgorithm::<lambda_1>::operator() C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:197
    #38 0x7ffb8ef768ae in blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm,`lambda at ..\..\third_party\blink\renderer\core\layout\block_node.cc:196:28'> C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:109:3
    #39 0x7ffb8ef61ddc in blink::`anonymous namespace'::LayoutWithAlgorithm C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:195
    #40 0x7ffb8ef61ddc in blink::BlockNode::Layout(class blink::ConstraintSpace const &, class blink::BlockBreakToken const *, class blink::EarlyBreak const *, class blink::ColumnSpannerPath const *) const C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:553:21
    #41 0x7ffb8efb0aae in blink::`anonymous namespace'::LayoutBlockChild C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_layout_algorithm.cc:119
    #42 0x7ffb8efb0aae in blink::`anonymous namespace'::LayoutInflow C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_layout_algorithm.cc:134:10
    #43 0x7ffb8efafd47 in blink::BlockLayoutAlgorithm::HandleInflow(class blink::LayoutInputNode, class blink::BreakToken const *, struct blink::PreviousInflowPosition *, class blink::InlineChildLayoutContext *, class blink::InlineBreakToken const **) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_layout_algorithm.cc:2350:7
    #44 0x7ffb8ef8ffca in blink::BlockLayoutAlgorithm::Layout(class blink::InlineChildLayoutContext *) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_layout_algorithm.cc:1089:18
    #45 0x7ffb8ef8d801 in blink::BlockLayoutAlgorithm::Layout(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_layout_algorithm.cc:602:14
    #46 0x7ffb8ef768ae in blink::`anonymous namespace'::LayoutWithAlgorithm::<lambda_1>::operator() C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:197
    #47 0x7ffb8ef768ae in blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm,`lambda at ..\..\third_party\blink\renderer\core\layout\block_node.cc:196:28'> C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:109:3
    #48 0x7ffb8ef61ddc in blink::`anonymous namespace'::LayoutWithAlgorithm C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:195
    #49 0x7ffb8ef61ddc in blink::BlockNode::Layout(class blink::ConstraintSpace const &, class blink::BlockBreakToken const *, class blink::EarlyBreak const *, class blink::ColumnSpannerPath const *) const C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:553:21
    #50 0x7ffb8efb0aae in blink::`anonymous namespace'::LayoutBlockChild C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_layout_algorithm.cc:119
    #51 0x7ffb8efb0aae in blink::`anonymous namespace'::LayoutInflow C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_layout_algorithm.cc:134:10
    #52 0x7ffb8efafd47 in blink::BlockLayoutAlgorithm::HandleInflow(class blink::LayoutInputNode, class blink::BreakToken const *, struct blink::PreviousInflowPosition *, class blink::InlineChildLayoutContext *, class blink::InlineBreakToken const **) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_layout_algorithm.cc:2350:7
    #53 0x7ffb8ef8ffca in blink::BlockLayoutAlgorithm::Layout(class blink::InlineChildLayoutContext *) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_layout_algorithm.cc:1089:18
    #54 0x7ffb8ef8d801 in blink::BlockLayoutAlgorithm::Layout(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_layout_algorithm.cc:602:14
    #55 0x7ffb8ef768ae in blink::`anonymous namespace'::LayoutWithAlgorithm::<lambda_1>::operator() C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:197
    #56 0x7ffb8ef768ae in blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm,`lambda at ..\..\third_party\blink\renderer\core\layout\block_node.cc:196:28'> C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:109:3
    #57 0x7ffb8ef61ddc in blink::`anonymous namespace'::LayoutWithAlgorithm C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:195
    #58 0x7ffb8ef61ddc in blink::BlockNode::Layout(class blink::ConstraintSpace const &, class blink::BlockBreakToken const *, class blink::EarlyBreak const *, class blink::ColumnSpannerPath const *) const C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:553:21
    #59 0x7ffb8efa1448 in blink::`anonymous namespace'::LayoutBlockChild C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_layout_algorithm.cc:119
    #60 0x7ffb8efa1448 in blink::BlockLayoutAlgorithm::LayoutNewFormattingContext(class blink::LayoutInputNode, class blink::BlockBreakToken const *, struct blink::InflowChildData const &, struct blink::BfcOffset, bool, struct blink::BfcOffset *, struct blink::BoxStrut *) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_layout_algorithm.cc:2166:41
    #61 0x7ffb8ef9e7e4 in blink::BlockLayoutAlgorithm::HandleNewFormattingContext(class blink::LayoutInputNode, class blink::BlockBreakToken const *, struct blink::PreviousInflowPosition *) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_layout_algorithm.cc:1941:39
    #62 0x7ffb8ef8ff56 in blink::BlockLayoutAlgorithm::Layout(class blink::InlineChildLayoutContext *) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_layout_algorithm.cc:1084:18
    #63 0x7ffb8ef8d801 in blink::BlockLayoutAlgorithm::Layout(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_layout_algorithm.cc:602:14
    #64 0x7ffb8ef768ae in blink::`anonymous namespace'::LayoutWithAlgorithm::<lambda_1>::operator() C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:197
    #65 0x7ffb8ef768ae in blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm,`lambda at ..\..\third_party\blink\renderer\core\layout\block_node.cc:196:28'> C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:109:3
    #66 0x7ffb8ef61ddc in blink::`anonymous namespace'::LayoutWithAlgorithm C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:195
    #67 0x7ffb8ef61ddc in blink::BlockNode::Layout(class blink::ConstraintSpace const &, class blink::BlockBreakToken const *, class blink::EarlyBreak const *, class blink::ColumnSpannerPath const *) const C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\block_node.cc:553:21
    #68 0x7ffb8e80155b in blink::LayoutView::LayoutRoot(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_view.cc:908:19
    #69 0x7ffb8fdc83b1 in blink::LocalFrameView::PerformLayout(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:791:24
    #70 0x7ffb8fdca936 in blink::LocalFrameView::UpdateLayout(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:848:3
    #71 0x7ffb8fdea028 in blink::LocalFrameView::UpdateStyleAndLayoutInternal(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:3427:7
    #72 0x7ffb8fdd43ef in blink::LocalFrameView::UpdateStyleAndLayout(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:3353:18
    #73 0x7ffb927f7f7d in blink::Document::UpdateStyleAndLayout(enum blink::DocumentUpdateReason) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:3092:17
    #74 0x7ffb9043baca in blink::FrameSelection::SetSelectionFromNone(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\frame_selection.cc:1291:17
    #75 0x7ffb9043b572 in blink::FrameSelection::FocusedOrActiveStateChanged(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\frame_selection.cc:1065:5
    #76 0x7ffb7bf0c9d2 in blink::mojom::blink::FrameWidgetStubDispatch::Accept(class blink::mojom::blink::FrameWidget *, class mojo::Message *) C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\third_party\blink\public\mojom\page\widget.mojom-blink.cc:2608:13
    #77 0x7ffb82f170f4 in mojo::InterfaceEndpointClient::HandleValidatedMessage(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:1085:54
    #78 0x7ffb82f13e3d in mojo::MessageDispatcher::Accept(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:44:19
    #79 0x7ffb82f1d7de in mojo::InterfaceEndpointClient::HandleIncomingMessage(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:747:20
    #80 0x7ffb8694a5f6 in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread C:\b\s\w\ir\cache\builder\src\ipc\ipc_mojo_bootstrap.cc:1199:24
    #81 0x7ffb8694cb11 in base::internal::DecayedFunctorTraits<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::`anonymous namespace'::ScopedUrgentMessageNotification),IPC::ChannelAssociatedGroupController *&&,mojo::Message &&,IPC::`anonymous namespace'::ScopedUrgentMessageNotification &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:740
    #82 0x7ffb8694cb11 in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::`anonymous namespace'::ScopedUrgentMessageNotification),IPC::ChannelAssociatedGroupController *&&,mojo::Message &&,IPC::`anonymous namespace'::ScopedUrgentMessageNotification &&>,void,0,1,2>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:932
    #83 0x7ffb8694cb11 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::`anonymous namespace'::ScopedUrgentMessageNotification),IPC::ChannelAssociatedGroupController *&&,mojo::Message &&,IPC::`anonymous namespace'::ScopedUrgentMessageNotification &&>,base::internal::BindState<1,1,0,void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::`anonymous namespace'::ScopedUrgentMessageNotification),scoped_refptr<IPC::ChannelAssociatedGroupController>,mojo::Message,IPC::`anonymous namespace'::ScopedUrgentMessageNotification>,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1069
    #84 0x7ffb8694cb11 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::`anonymous namespace'::ScopedUrgentMessageNotification),IPC::ChannelAssociatedGroupController *&&,mojo::Message &&,IPC::`anonymous namespace'::ScopedUrgentMessageNotification &&>,base::internal::BindState<1,1,0,void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::`anonymous namespace'::ScopedUrgentMessageNotification),scoped_refptr<IPC::ChannelAssociatedGroupController>,mojo::Message,IPC::`anonymous namespace'::ScopedUrgentMessageNotification>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:982:12
    #85 0x7ffb831ef9d8 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:155
    #86 0x7ffb831ef9d8 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:229:34
    #87 0x7ffb831bfe21 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:112
    #88 0x7ffb831bfe21 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:475:23
    #89 0x7ffb831bec83 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:346:40
    #90 0x7ffb83329920 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:42:55
    #91 0x7ffb831c1b6f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:650:12
    #92 0x7ffb832675fc in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:135:14
    #93 0x7ffb8d7baa93 in content::RendererMain(struct content::MainFunctionParams) C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:364:16
    #94 0x7ffb7edf6a16 in content::RunOtherNamedProcessTypeMain(class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>> const &, struct content::MainFunctionParams, class content::ContentMainDelegate *) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:762:14
    #95 0x7ffb7edf917b in content::ContentMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1152:10
    #96 0x7ffb7edecf7f in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:358:36
    #97 0x7ffb7eded722 in content::ContentMain(struct content::ContentMainParams) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:371:10
    #98 0x7ffb6ed42b06 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:191:12
    #99 0x7ff6fcd24807 in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:204:12
    #100 0x7ff6fcd22074 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:351:20
    #101 0x7ff6fd21ce7f in invoke_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #102 0x7ff6fd21ce7f in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #103 0x7ffc62f6e8d6  (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #104 0x7ffc6478c40b  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18008c40b)

==25032==Register values:
rax = 12b8fa1e17ec  rbx = 12b8fa1e17ec  rcx = 12b8fa1e17ec  rdx = 12a4fa6e53d8
rdi = 12a4fa6e53d8  rsi = 14  rbp = b6c8dfa660  rsp = b6c8dfa5d8
r8  = 14  r9  = 2571f43c2ff  r10 = 7ffc60fe0000  r11 = 0
r12 = 1000000  r13 = 12a4fad053d8  r14 = ffffffff  r15 = ffffffffffffffd3
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: access-violation (C:\WINDOWS\System32\ucrtbase.dll+0x1800edc30)

==25032==ADDITIONAL INFO

==25032==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffb86944419 in IPC::ChannelAssociatedGroupController::Accept(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\ipc\ipc_mojo_bootstrap.cc:1138:13

Command line: `"C:\Users\winwin\Desktop\win32-release_x64_asan-win32-release_x64-1587431\chrome.exe" --type=renderer --unsafely-treat-insecure-origin-as-secure=http://172.30.1.200:8888 --no-pre-read-main-dll --no-sandbox --enable-unsafe-webgpu --file-url-path-alias="/gen=C:\Users\winwin\Desktop\win32-release_x64_asan-win32-release_x64-1587431\gen" --video-capture-use-gpu-memory-buffer --lang=en-US --device-scale-factor=1 --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=8 --time-ticks-at-unix-epoch=-1772769509573503 --launch-time-ticks=422601159186 --metrics-shmem-handle=4316,i,16590150145926551397,3420061095256368019,2097152 --field-trial-handle=1848,i,9800470822139892438,6761809189957616281,262144 --variations-seed-version --pseudonymization-salt-handle=2040,i,8348267116812909868,17333413211753954901,4 --trace-process-track-uuid=3190708993808206286 --mojo-platform-channel-handle=4036 /prefetch:1`

==25032==END OF ADDITIONAL INFO

==25032==ABORTING

```

### aj...@google.com (2026-03-11)

Thanks - note you can include just the important snippet of the asan stack inline and attach the full trace as `asan.log`.

This repros a renderer access violation write on Win asan and in a Canary & Stable release build:

```
0:000> k
 # Child-SP          RetAddr               Call Site
0a (Inline Function) --------`--------     chrome!apply_stch+0x309 [C:\b\s\w\ir\cache\builder\src\third_party\harfbuzz-ng\src\src\hb-ot-shaper-arabic.cc @ 616] 
0b 000000fb`9edf5540 00007ffa`499d53bd     chrome!postprocess_glyphs_arabic+0x31c [C:\b\s\w\ir\cache\builder\src\third_party\harfbuzz-ng\src\src\hb-ot-shaper-arabic.cc @ 652] 
0c (Inline Function) --------`--------     chrome!hb_ot_substitute_post+0x13cc ...
12 (Inline Function) --------`--------     chrome!blink::`anonymous namespace'::ShapeRange+0x411 [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\fonts\shaping\harfbuzz_shaper.cc @ 339] 
...
0:000> .excr
rax=0000000000000060 rbx=0000002c01004000 rcx=000000002e7ee030
rdx=0000000001000000 rsi=0000002c02907bd8 rdi=00000000000402ff
rip=00007ffa4eb2e3cc rsp=000000fb9edf5540 rbp=0000000009000007
 r8=0000002c01507bd8  r9=0000000000000000 r10=00000000ffffffa0
r11=00000000000402fe r12=00000013ffffffec r13=000000002e7ee030
r14=00000000ffffffff r15=0000000000000000
iopl=0         nv up ei pl nz na po nc
cs=0033  ss=0000  ds=0000  es=0000  fs=0053  gs=002b             efl=00010206
chrome!apply_stch+0x309 [inlined in chrome!postprocess_glyphs_arabic+0x31c]:
00007ffa`4eb2e3cc 42896c2310      mov     dword ptr [rbx+r12+10h],ebp ds:00000040`01003ffc=????????
0:000> .exr -1
ExceptionAddress: 00007ffa4eb2e3cc (chrome!apply_stch+0x0000000000000309)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 0000000000000001
   Parameter[1]: 0000004001003ffc
Attempt to write to address 0000004001003ffc

```

### aj...@google.com (2026-03-11)

goto/crash/5ed98ca9d3acc436 once it processes

### ch...@google.com (2026-03-11)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-11)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dr...@chromium.org (2026-03-11)

Behdad is aware of the issue in HarfBuzz and looking into a fix.

### be...@gmail.com (2026-03-11)

PR at https://github.com/harfbuzz/harfbuzz/pull/5823

### dr...@chromium.org (2026-03-12)

Roll commit in <https://chromium-review.git.corp.google.com/c/chromium/src/+/7660223>

### dx...@google.com (2026-03-12)

Project: chromium/src  

Branch:  main  

Author:  Dominik Röttsches [drott@chromium.org](mailto:drott@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7660223>

Roll src/third\_party/harfbuzz-ng/src/ fa2908bf1..5d4e96ad8 (627 commits)

---


Expand for full commit details
```
     
    Contains fix for integer overflow and OOB read in apply_stch(). 
     
    https://chromium.googlesource.com/external/github.com/harfbuzz/harfbuzz.git/+log/fa2908bf16d2..5d4e96ad8d00 
     
    $ git log fa2908bf1..5d4e96ad8 --date=short --no-merges --format='%ad %ae %s' 
    2026-03-12 behdad [meson] Add raster/vector feature macros 
    2026-03-10 behdad [docs] Add Assisted-by trailer guidance to AI conduct policy 
    2026-03-10 behdad [docs] Clarify commit message formatting 
    2026-03-10 behdad [docs] Add AI contribution policy 
    2026-03-12 behdad [svg] Keep zlib private to raster and vector SVG decoding 
    2026-03-12 behdad [test] Add vector coverage for handwriting color fonts 
    2026-03-12 behdad [vector] Allow duplicate SVG refs during subsetting 
    2026-03-11 grieger For the CFF overflow fix use remaining instead of total bytes to avoid any possible overflow in the total bytes count. (#5826) 
    2026-03-11 behdad [util] Move shared ANSI image helpers out of Cairo wrapper 
    2026-03-11 behdad [vector] Keep extracted root SVG overflow visible 
    2026-03-11 behdad [svg] Use em-square root viewport fallback 
    2026-03-11 behdad [svg] Share svgz normalization across raster and vector 
    2026-03-11 grieger Fix potential buffer overwrite in CFF/CFF2. (#5825) 
    2026-03-11 behdad [docs] Allow CI-only commits without tests 
    2026-03-11 behdad [ci] Install raster image dependencies on Linux 
    2026-03-11 behdad [docs] Allow docs-only commits without tests 
    2026-03-11 behdad [docs] Clarify local agent rules 
    2026-03-11 behdad [raster] Simplify SVG render cleanup 
    2026-03-11 behdad [meson] Report zlib in raster dependency summary 
    2026-03-11 behdad [raster] Support gzip-compressed SVG documents 
    2026-03-11 behdad [arabic] Cap stch expansion per run (#5823) 
    2026-03-11 behdad [docs] Require full test run before commits 
    2026-03-11 khaled Don’t build raster and vector fuzzers if the library is disabled 
    2026-03-11 heftig util: Add missing chafa_dep to hb-raster 
    2026-03-11 khaled 13.1.0 
    2026-03-10 grieger Add fuzzer seed for malformed axis ranges. 
    2026-03-10 behdad [subset] Validate rebasing axis limits locally 
    2026-03-10 behdad [subset] Allow avar2 pinned normalized points 
    2026-03-10 behdad [subset] Reject malformed normalized axis ranges 
    2026-03-09 khaled [subset/cff1] Fix subsetting font dicts with old_to_new_glyph_mapping 
    2026-03-10 behdad [raster] Reduce buffer size cap 
    2026-03-10 behdad [raster] Bound temporary clip mask buffers 
    2026-03-10 behdad [raster] Bound SVG path parsing work 
    2026-03-10 behdad [vector] Propagate paint init failures 
    2026-03-10 behdad [vector] Guard paint render after init failure 
    2026-03-10 behdad [vector] Fix OOM handling in SVG subset id collection 
    2026-03-10 behdad [vector] Avoid double-free in draw blob creation 
    2026-03-10 behdad [vector] Avoid double-free on blob creation failure 
    2026-03-10 behdad [cplusplus] Add raster and vector vtables 
    2026-03-10 behdad [vector] Avoid OOM leak in paint initialization 
    2026-03-10 behdad [fuzzing] Guard raster/vector create_or_fail results 
    2026-03-10 behdad [check] Simplify list 
    2026-03-10 behdad [svg] Gate SVG table processing under HB_NO_SVG (#5814) 
    2026-03-10 behdad [AGENTS.md] Refine commit message guidance 
    2026-03-10 behdad [AGENTS.md] Tighten repository guide 
    2026-03-10 behdad [AGENTS.md] Encode commit message conventions 
    2026-03-10 behdad AGENTS.md: add guidance from recent commit history 
    2026-03-10 behdad AGENTS.md: reorganize repository guide 
    2026-03-10 behdad AGENTS.md: address PR review feedback 
    2026-03-09 behdad [AGENTS.md] Expand repo map, debug flags, options, and change-specific advice 
    (...) 
    2026-02-09 49699333+dependabot[bot] Bump github/codeql-action from 4.32.0 to 4.32.2 
    2026-02-08 behdad [hb-view] Make rainbow colors slightly translucent 
    2026-02-08 behdad [hb-view] Add --stroke= 
    2026-02-08 behdad [hb-view] Add --foreground color list and --rainbow 
    2026-02-08 behdad [hb-view] Add --logical counterpart to --ink 
    2026-02-08 behdad [hb-view] Add --ink 
    2026-02-06 behdad [hb-svg-compare] Write out error with %g, not %.5f 
    2026-02-06 behdad [VARC] TCenter really is parsed after Skew according to spec 
    2026-02-06 behdad [VARC] Convert a division to mult 
    2026-02-06 behdad More accurate HB_PI 
    2026-02-06 behdad [hb-draw-compare] Print out debug info from hb-view 
    2026-02-06 behdad [VARC] More speculation 
    2026-02-06 behdad [VARC] Another shot 
    2026-02-06 behdad [VARC] Another shot in the dark 
    2026-02-06 behdad Revert "[VARC] Another long shot" 
    2026-02-06 behdad [VARC] Another long shot 
    2026-02-05 behdad [VARC] Try fixing double scaling 
    2026-02-05 behdad [VARC] A couple more rounding issues 
    2026-02-05 behdad [VARC] Process axes in forward order 
    2026-02-05 behdad [VARC] Don't round transform components for division 
    2026-02-05 behdad [gvar] Remove unused variable assignment 
    2026-02-05 behdad Revert "[rust] Use HarfBuzz-style glyph outline" 
    2026-02-05 behdad [rust] Use HarfBuzz-style glyph outline 
    2026-02-05 behdad [gvar] Speed up by using a fused delta application codepath (#5730) 
    2026-02-05 behdad [VARC] Implement lazy skipping 
    2026-02-04 behdad [rust] Add a couple of compiler flags (#5729) 
    2026-02-03 behdad [rust] Use panic="abort" in debugoptimized builds as well 
    2026-02-03 behdad [scalar-cache] Enlarge, and adjust scratch logic (#5728) 
    2026-02-02 49699333+dependabot[bot] Bump github/codeql-action from 4.31.11 to 4.32.0 
    2026-01-26 49699333+dependabot[bot] Bump actions/setup-python from 6.1.0 to 6.2.0 
    2026-01-26 49699333+dependabot[bot] Bump setuptools from 80.9.0 to 80.10.2 in /.ci 
    2026-01-26 49699333+dependabot[bot] Bump github/codeql-action from 4.31.10 to 4.31.11 
    2026-01-26 49699333+dependabot[bot] Bump actions/checkout from 6.0.1 to 6.0.2 
    2026-01-24 khaled Typo [ci skip] 
    2026-01-24 khaled 12.3.2 
    2026-01-24 khaled Minor [ci skip] 
    2026-01-23 qxliu fix fuzzer issue: https://oss-fuzz.com/testcase-detail/6005602106277888 
    2026-01-22 behdad [cmap] Another null check 
    2026-01-22 behdad [gvar] Fix padding size calcs (#5718) 
    2026-01-21 48925186+qxliu76 Fix fuzzer found heap-use-after-free crash (#5717) 
    2026-01-20 qxliu [subset] fix padding in gvar table 
    2026-01-20 khaled 12.3.1 
    2026-01-19 49699333+dependabot[bot] Bump meson from 1.10.0 to 1.10.1 in /.ci 
    2026-01-19 49699333+dependabot[bot] Bump github/codeql-action from 4.31.9 to 4.31.10 
    2026-01-12 behdad [benchmark-shape] Fix unused-var under NDEBUG 
    2026-01-10 behdad Fix some unused-var warnings under NDEBUG 
    2026-01-10 behdad [rust] Roll to new HarfRust 
    2026-01-10 baskerville GCC 4.9.4: Keep template names unique (#5713) 
    2026-01-09 behdad Remove use of std::is_trivially_copyable (#5711) 
    2026-01-09 behdad [cmap] malloc fail test (#5710) 
     
    Created with: 
      roll-dep src/third_party/harfbuzz-ng/src 
     
    R=behdad@chromium.org,bungeman@chromium.org,drott@chromium.org,jshin@chromium.org,kojii@chromium.org 
     
    Fixed: 491516670 
    Change-Id: Id81604a497ade940b3bbaa0876489cff0858efcc 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7660223 
    Auto-Submit: Dominik Röttsches <drott@chromium.org> 
    Commit-Queue: Anders Hartvoll Ruud <andruud@chromium.org> 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1598298}

```

---

Files:

- M `DEPS`
- M `third_party/harfbuzz-ng/BUILD.gn`
- M `third_party/harfbuzz-ng/README.chromium`
- M `third_party/harfbuzz-ng/src`

---

Hash: [4151e38fc8c91f9cacab2026e44e80720f9f779f](https://chromiumdash.appspot.com/commit/4151e38fc8c91f9cacab2026e44e80720f9f779f)  

Date: Thu Mar 12 09:43:30 2026


---

### ch...@google.com (2026-03-13)

Security Merge Request Consideration: Requesting merge to stable (M146) because latest trunk commit (1598298) appears to be after stable branch point (1582197).
Security Merge Request Consideration: Requesting merge to beta (M147) because latest trunk commit (1598298) appears to be after beta branch point (1596535).
Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [146, 147].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dr...@chromium.org (2026-03-15)

No crashes in Canary. Approved to merge to M146 and M147.

### dr...@chromium.org (2026-03-16)

M147 merge in <https://chromium-review.git.corp.google.com/c/chromium/src/+/7666226> -

For M146, I am trying to do a cherry-pick of recent changes to `hb-ot-shaper-arabic.cc` to keep the backport minimal, but I am having trouble creating a branch in HarfBuzz gerrit repo.

### dx...@google.com (2026-03-16)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Dominik Röttsches [drott@chromium.org](mailto:drott@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7666226>

Roll src/third\_party/harfbuzz-ng/src/ fa2908bf1..5d4e96ad8 (627 commits)

---


Expand for full commit details
```
     
    Contains fix for integer overflow and OOB read in apply_stch(). 
     
    https://chromium.googlesource.com/external/github.com/harfbuzz/harfbuzz.git/+log/fa2908bf16d2..5d4e96ad8d00 
     
    $ git log fa2908bf1..5d4e96ad8 --date=short --no-merges --format='%ad %ae %s' 
    2026-03-12 behdad [meson] Add raster/vector feature macros 
    2026-03-10 behdad [docs] Add Assisted-by trailer guidance to AI conduct policy 
    2026-03-10 behdad [docs] Clarify commit message formatting 
    2026-03-10 behdad [docs] Add AI contribution policy 
    2026-03-12 behdad [svg] Keep zlib private to raster and vector SVG decoding 
    2026-03-12 behdad [test] Add vector coverage for handwriting color fonts 
    2026-03-12 behdad [vector] Allow duplicate SVG refs during subsetting 
    2026-03-11 grieger For the CFF overflow fix use remaining instead of total bytes to avoid any possible overflow in the total bytes count. (#5826) 
    2026-03-11 behdad [util] Move shared ANSI image helpers out of Cairo wrapper 
    2026-03-11 behdad [vector] Keep extracted root SVG overflow visible 
    2026-03-11 behdad [svg] Use em-square root viewport fallback 
    2026-03-11 behdad [svg] Share svgz normalization across raster and vector 
    2026-03-11 grieger Fix potential buffer overwrite in CFF/CFF2. (#5825) 
    2026-03-11 behdad [docs] Allow CI-only commits without tests 
    2026-03-11 behdad [ci] Install raster image dependencies on Linux 
    2026-03-11 behdad [docs] Allow docs-only commits without tests 
    2026-03-11 behdad [docs] Clarify local agent rules 
    2026-03-11 behdad [raster] Simplify SVG render cleanup 
    2026-03-11 behdad [meson] Report zlib in raster dependency summary 
    2026-03-11 behdad [raster] Support gzip-compressed SVG documents 
    2026-03-11 behdad [arabic] Cap stch expansion per run (#5823) 
    2026-03-11 behdad [docs] Require full test run before commits 
    2026-03-11 khaled Don’t build raster and vector fuzzers if the library is disabled 
    2026-03-11 heftig util: Add missing chafa_dep to hb-raster 
    2026-03-11 khaled 13.1.0 
    2026-03-10 grieger Add fuzzer seed for malformed axis ranges. 
    2026-03-10 behdad [subset] Validate rebasing axis limits locally 
    2026-03-10 behdad [subset] Allow avar2 pinned normalized points 
    2026-03-10 behdad [subset] Reject malformed normalized axis ranges 
    2026-03-09 khaled [subset/cff1] Fix subsetting font dicts with old_to_new_glyph_mapping 
    2026-03-10 behdad [raster] Reduce buffer size cap 
    2026-03-10 behdad [raster] Bound temporary clip mask buffers 
    2026-03-10 behdad [raster] Bound SVG path parsing work 
    2026-03-10 behdad [vector] Propagate paint init failures 
    2026-03-10 behdad [vector] Guard paint render after init failure 
    2026-03-10 behdad [vector] Fix OOM handling in SVG subset id collection 
    2026-03-10 behdad [vector] Avoid double-free in draw blob creation 
    2026-03-10 behdad [vector] Avoid double-free on blob creation failure 
    2026-03-10 behdad [cplusplus] Add raster and vector vtables 
    2026-03-10 behdad [vector] Avoid OOM leak in paint initialization 
    2026-03-10 behdad [fuzzing] Guard raster/vector create_or_fail results 
    2026-03-10 behdad [check] Simplify list 
    2026-03-10 behdad [svg] Gate SVG table processing under HB_NO_SVG (#5814) 
    2026-03-10 behdad [AGENTS.md] Refine commit message guidance 
    2026-03-10 behdad [AGENTS.md] Tighten repository guide 
    2026-03-10 behdad [AGENTS.md] Encode commit message conventions 
    2026-03-10 behdad AGENTS.md: add guidance from recent commit history 
    2026-03-10 behdad AGENTS.md: reorganize repository guide 
    2026-03-10 behdad AGENTS.md: address PR review feedback 
    2026-03-09 behdad [AGENTS.md] Expand repo map, debug flags, options, and change-specific advice 
    (...) 
    2026-02-09 49699333+dependabot[bot] Bump github/codeql-action from 4.32.0 to 4.32.2 
    2026-02-08 behdad [hb-view] Make rainbow colors slightly translucent 
    2026-02-08 behdad [hb-view] Add --stroke= 
    2026-02-08 behdad [hb-view] Add --foreground color list and --rainbow 
    2026-02-08 behdad [hb-view] Add --logical counterpart to --ink 
    2026-02-08 behdad [hb-view] Add --ink 
    2026-02-06 behdad [hb-svg-compare] Write out error with %g, not %.5f 
    2026-02-06 behdad [VARC] TCenter really is parsed after Skew according to spec 
    2026-02-06 behdad [VARC] Convert a division to mult 
    2026-02-06 behdad More accurate HB_PI 
    2026-02-06 behdad [hb-draw-compare] Print out debug info from hb-view 
    2026-02-06 behdad [VARC] More speculation 
    2026-02-06 behdad [VARC] Another shot 
    2026-02-06 behdad [VARC] Another shot in the dark 
    2026-02-06 behdad Revert "[VARC] Another long shot" 
    2026-02-06 behdad [VARC] Another long shot 
    2026-02-05 behdad [VARC] Try fixing double scaling 
    2026-02-05 behdad [VARC] A couple more rounding issues 
    2026-02-05 behdad [VARC] Process axes in forward order 
    2026-02-05 behdad [VARC] Don't round transform components for division 
    2026-02-05 behdad [gvar] Remove unused variable assignment 
    2026-02-05 behdad Revert "[rust] Use HarfBuzz-style glyph outline" 
    2026-02-05 behdad [rust] Use HarfBuzz-style glyph outline 
    2026-02-05 behdad [gvar] Speed up by using a fused delta application codepath (#5730) 
    2026-02-05 behdad [VARC] Implement lazy skipping 
    2026-02-04 behdad [rust] Add a couple of compiler flags (#5729) 
    2026-02-03 behdad [rust] Use panic="abort" in debugoptimized builds as well 
    2026-02-03 behdad [scalar-cache] Enlarge, and adjust scratch logic (#5728) 
    2026-02-02 49699333+dependabot[bot] Bump github/codeql-action from 4.31.11 to 4.32.0 
    2026-01-26 49699333+dependabot[bot] Bump actions/setup-python from 6.1.0 to 6.2.0 
    2026-01-26 49699333+dependabot[bot] Bump setuptools from 80.9.0 to 80.10.2 in /.ci 
    2026-01-26 49699333+dependabot[bot] Bump github/codeql-action from 4.31.10 to 4.31.11 
    2026-01-26 49699333+dependabot[bot] Bump actions/checkout from 6.0.1 to 6.0.2 
    2026-01-24 khaled Typo [ci skip] 
    2026-01-24 khaled 12.3.2 
    2026-01-24 khaled Minor [ci skip] 
    2026-01-23 qxliu fix fuzzer issue: https://oss-fuzz.com/testcase-detail/6005602106277888 
    2026-01-22 behdad [cmap] Another null check 
    2026-01-22 behdad [gvar] Fix padding size calcs (#5718) 
    2026-01-21 48925186+qxliu76 Fix fuzzer found heap-use-after-free crash (#5717) 
    2026-01-20 qxliu [subset] fix padding in gvar table 
    2026-01-20 khaled 12.3.1 
    2026-01-19 49699333+dependabot[bot] Bump meson from 1.10.0 to 1.10.1 in /.ci 
    2026-01-19 49699333+dependabot[bot] Bump github/codeql-action from 4.31.9 to 4.31.10 
    2026-01-12 behdad [benchmark-shape] Fix unused-var under NDEBUG 
    2026-01-10 behdad Fix some unused-var warnings under NDEBUG 
    2026-01-10 behdad [rust] Roll to new HarfRust 
    2026-01-10 baskerville GCC 4.9.4: Keep template names unique (#5713) 
    2026-01-09 behdad Remove use of std::is_trivially_copyable (#5711) 
    2026-01-09 behdad [cmap] malloc fail test (#5710) 
     
    Created with: 
      roll-dep src/third_party/harfbuzz-ng/src 
     
    R=behdad@chromium.org,bungeman@chromium.org,drott@chromium.org,jshin@chromium.org,kojii@chromium.org 
     
    (cherry picked from commit 4151e38fc8c91f9cacab2026e44e80720f9f779f) 
     
    Fixed: 491516670 
    Change-Id: Id81604a497ade940b3bbaa0876489cff0858efcc 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7660223 
    Auto-Submit: Dominik Röttsches <drott@chromium.org> 
    Commit-Queue: Anders Hartvoll Ruud <andruud@chromium.org> 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1598298} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7666226 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Dominik Röttsches <drott@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7727@{#459} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `DEPS`
- M `third_party/harfbuzz-ng/BUILD.gn`
- M `third_party/harfbuzz-ng/README.chromium`
- M `third_party/harfbuzz-ng/src`

---

Hash: [855db79c3f945dc51592d54c1c7e4c86dc6f8541](https://chromiumdash.appspot.com/commit/855db79c3f945dc51592d54c1c7e4c86dc6f8541)  

Date: Mon Mar 16 13:14:23 2026


---

### pe...@google.com (2026-03-16)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2026-03-18)

Project: external/github.com/harfbuzz/harfbuzz  

Branch:  chromium/m146  

Author:  Dominik Röttsches [drott@chromium.org](mailto:drott@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7673379>

[Cherry-pick] Cherry-pick 3 Arabic, stch fixes to M146 branch.

---


Expand for full commit details
```
     
    [arabic] Cap stch expansion per run (#5823) 
     
    Cap each stch run to at most 256 output glyphs. 
     
    This keeps pathological stretch runs from expanding to unbounded 
    sizes, and switches the repeat-count math to 64-bit intermediates so 
    the cap is applied before 32-bit arithmetic can wrap. 
     
    The existing checked accumulation and buffer growth logic stays in 
    place, covering both the per-run overflow and multi-run accumulation 
    cases reported in the recent stch advisories. 
     
    Tested: meson test -C build --suite shape 
    Assisted-by: OpenAI Codex 
     
    [arabic] Improve stch measurement pass (#5808) 
     
    Use checked arithmetic when calculating the number of extra glyphs 
    needed during stch processing. Includes a new hb_unsigned_add_overflows 
    helper in hb-algs.hh. 
     
    Co-authored-by: Codex (AI assistant) 
    Co-authored-by: Gemini (AI assistant) 
     
    [arabic] Change a couple enum values 
     
    No semantic change. 
     
    Bug: 491516670 
    Fixed: 493132380 
    Change-Id: I27bdce361f56fb01eb499e445677049c2e104153

```

---

Files:

- M `src/hb-algs.hh`
- M `src/hb-ot-shaper-arabic.cc`

---

Hash: [c24f6a29e5912332e269891fbdb1ac771d543a08](https://chromiumdash.appspot.com/commit/c24f6a29e5912332e269891fbdb1ac771d543a08)  

Date: Tue Mar 17 12:25:06 2026


---

### dr...@chromium.org (2026-03-18)

M146 merge in <https://chromium-review.git.corp.google.com/c/chromium/src/+/7679870>

### dx...@google.com (2026-03-18)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Dominik Röttsches [drott@chromium.org](mailto:drott@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7679870>

[cherry-pick] Fix HarfBuzz apply\_stch()

---


Expand for full commit details
```
     
    Cherry-pick 3 upstream fixes for issue 491516670, compare: 
    https://crrev.com/c/7673379 
     
    Bug: 491516670 
    Change-Id: I1b527723e6416abbdf62ade2e2bf1943d63a57ce 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7679870 
    Commit-Queue: Dominik Röttsches <drott@chromium.org> 
    Reviewed-by: Rune Lillesveen <futhark@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7680@{#2789} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `DEPS`
- M `third_party/harfbuzz-ng/src`

---

Hash: [5627d2e7b9c5963108d336dd98ceb756617e6f60](https://chromiumdash.appspot.com/commit/5627d2e7b9c5963108d336dd98ceb756617e6f60)  

Date: Wed Mar 18 14:42:52 2026


---

### vi...@google.com (2026-03-18)

Hi. In [comment#13](https://issues.chromium.org/issues/491516670#comment13) mentions that M147 and M146 were previously using HarfBuzz version `12.3.0-20`. For either branch it was needed to roll at least 627 commits to obtain a newer HarfBuzz with the fixes for this current bug. On the other hand, M138 is way behind using HarfBuzz version `11.0.0-97` which would require an even larger rework. Therefore, I’m labeling it as `LTS-NotApplicable-138` due to the potential instability that the fixes could bring in.

### be...@gmail.com (2026-03-18)

The change can easily be cherry-picked as it doesn't touch a part of the code that has been changed in a decade.

### dr...@chromium.org (2026-03-19)

vignatti@, see <https://crrev.com/c/7673379> - this is cherry-picking 3 changes to `src/hb-ot-shaper-arabic.cc` which should be quite minimal and potentially applicable to M138. For 147 and 148 I merged the whole roll, for 146 which is currently stable, I merged only the cherry-pick. See [issue 493132380](https://issues.chromium.org/issues/493132380) if you need a branch for m138 on the HarfBuzz mirror repo.

### dx...@google.com (2026-03-20)

Project: external/github.com/harfbuzz/harfbuzz  

Branch:  chromium/m138  

Author:  Tiago Vignatti [vignatti@google.com](mailto:vignatti@google.com)  

Link:    <https://chromium-review.googlesource.com/7687651>

[Cherry-pick] Cherry-pick 3 Arabic, stch fixes to M138 branch.

---


Expand for full commit details
```
     
    [arabic] Cap stch expansion per run (#5823) 
     
    Cap each stch run to at most 256 output glyphs. 
     
    This keeps pathological stretch runs from expanding to unbounded 
    sizes, and switches the repeat-count math to 64-bit intermediates so 
    the cap is applied before 32-bit arithmetic can wrap. 
     
    The existing checked accumulation and buffer growth logic stays in 
    place, covering both the per-run overflow and multi-run accumulation 
    cases reported in the recent stch advisories. 
     
    Tested: meson test -C build --suite shape 
    Assisted-by: OpenAI Codex 
     
    [arabic] Improve stch measurement pass (#5808) 
     
    Use checked arithmetic when calculating the number of extra glyphs 
    needed during stch processing. Includes a new hb_unsigned_add_overflows 
    helper in hb-algs.hh. 
     
    Co-authored-by: Codex (AI assistant) 
    Co-authored-by: Gemini (AI assistant) 
     
    [arabic] Change a couple enum values 
     
    No semantic change. 
     
    Bug: 491516670 
    Change-Id: I721974ff5792006655e19a0dad1567a5268ad6a2 
    Fixed: 493132380

```

---

Files:

- M `src/hb-algs.hh`
- M `src/hb-ot-shaper-arabic.cc`

---

Hash: [15fdcf0395ff49d36069b808828fa5f06d7ec4d9](https://chromiumdash.appspot.com/commit/15fdcf0395ff49d36069b808828fa5f06d7ec4d9)  

Date: Fri Mar 20 13:19:22 2026


---

### vi...@google.com (2026-03-20)

Thanks Behdad for the comment. With the help of Dominik (for branching HarfBuzz gerrit repo), I've managed to cherry pick similar changes from M146 to keep the backport to M138 minimal.

### pe...@google.com (2026-03-20)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vi...@google.com (2026-03-20)

1. it's a simple CL in Chromium to update the revision (<https://chromium-review.git.corp.google.com/c/chromium/src/+/7687790>), in which cherry-picks 3 CLs in Harfbuzz containing the actual fixes (<https://chromium-review.git.corp.google.com/c/external/github.com/harfbuzz/harfbuzz/+/7687651>)
2. Medium - there were no conflicts, but it required changes in the third party component HarfBuzz.
3. M147 and M146
4. Yes. Although I initially thought it would require rolling a new version of the third part component, in the end it was a minimal change there and that was already applied in another stable release (M146).

### pw...@gmail.com (2026-03-24)

Hello,

The credit listed in the Stable Channel Update for Desktop is different from the requested credit (pwn2addr). Could you please update it?

### an...@google.com (2026-03-31)

Merge approved for LTS-138

### dx...@google.com (2026-04-08)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Tiago Vignatti [vignatti@google.com](mailto:vignatti@google.com)  

Link:    <https://chromium-review.googlesource.com/7687790>

[M138-LTS][cherry-pick] Fix HarfBuzz apply\_stch()

---


Expand for full commit details
```
     
    This is based on the changes made for M146 (https://crrev.com/c/7679870) 
    but this one is meant for M138. 
     
    Cherry-pick 3 upstream fixes for issue 491516670, compare: 
    https://crrev.com/c/7687651 
     
    Bug: 491516670 
    Change-Id: I396baa9d84c1e203f974385f9e1f4715a180102e 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7687790 
    Reviewed-by: Victor Gabriel Savu <vsavu@google.com> 
    Reviewed-by: Dominik Röttsches <drott@chromium.org> 
    Commit-Queue: Tiago Vignatti (xWF) <vignatti@google.com> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3531} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `DEPS`
- M `third_party/harfbuzz-ng/src`

---

Hash: [93bb0326da639c34dbb10ec4369ec3ca7dc38f7c](https://chromiumdash.appspot.com/commit/93bb0326da639c34dbb10ec4369ec3ca7dc38f7c)  

Date: Wed Apr 8 14:35:13 2026


---

### sp...@google.com (2026-04-16)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
High quality with bisect. Renderer RCE / memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### dr...@chromium.org (2026-04-29)

There is an additional advisory in HarfBuzz with a local harness reproducer <https://github.com/harfbuzz/harfbuzz/security/advisories/GHSA-5xrh-8c3h-7c49> which suggests an additional line of code is required for a full fix. This needs more investigation. A roll with that fix is prepared in <https://crrev.com/c/7799984> - we need to decide if this needs additional backporting.

### dr...@chromium.org (2026-05-04)

Re #30, this is tracked in [issue 503425922](https://issues.chromium.org/issues/503425922).

### pe...@google.com (2026-05-04)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vi...@google.com (2026-05-05)

1. <https://chromium-review.git.corp.google.com/c/external/github.com/harfbuzz/harfbuzz/+/7808512> and also the Chromium side to cherry-pick the 4 fixes
2. Low. There were no conflicts
3. As I understand it, of the four necessary fixes, [the fourth one](https://chromium-review.git.corp.google.com/c/external/github.com/harfbuzz/harfbuzz/+/7807098) is [still awaiting a merge in stable releases](https://issues.chromium.org/issues/503425922). The remaining three have already been successfully merged into versions 138, 146, and 147.
4. Yes

### dx...@google.com (2026-05-06)

Project: external/github.com/harfbuzz/harfbuzz  

Branch:  chromium/m144  

Author:  Tiago Vignatti [vignatti@google.com](mailto:vignatti@google.com)  

Link:    <https://chromium-review.googlesource.com/7808512>

[Cherry-pick] Cherry-pick 4 Arabic, stch fixes to M144 branch.

---


Expand for full commit details
```
     
    [arabic] Fix overflow handling in apply_stch (#5929) 
     
    [arabic] Cap stch expansion per run (#5823) 
     
    Cap each stch run to at most 256 output glyphs. 
     
    This keeps pathological stretch runs from expanding to unbounded 
    sizes, and switches the repeat-count math to 64-bit intermediates so 
    the cap is applied before 32-bit arithmetic can wrap. 
     
    The existing checked accumulation and buffer growth logic stays in 
    place, covering both the per-run overflow and multi-run accumulation 
    cases reported in the recent stch advisories. 
     
    Tested: meson test -C build --suite shape 
    Assisted-by: OpenAI Codex 
     
    [arabic] Improve stch measurement pass (#5808) 
     
    Use checked arithmetic when calculating the number of extra glyphs 
    needed during stch processing. Includes a new hb_unsigned_add_overflows 
    helper in hb-algs.hh. 
     
    Co-authored-by: Codex (AI assistant) 
    Co-authored-by: Gemini (AI assistant) 
     
    [arabic] Change a couple enum values 
     
    No semantic change. 
     
    Bug: 491516670 
    Change-Id: If1df7a4452cdd214195558084160ef15a21b8248 
    Fixed: 493132380

```

---

Files:

- M `src/hb-algs.hh`
- M `src/hb-ot-shaper-arabic.cc`

---

Hash: [7280ac1730d54a0d33f80ae2a436e5cac0ccd811](https://chromiumdash.appspot.com/commit/7280ac1730d54a0d33f80ae2a436e5cac0ccd811)  

Date: Tue May 5 18:08:12 2026


---

### an...@google.com (2026-05-06)

Delaying merge from [#comment33](https://issues.chromium.org/issues/491516670#comment33)

### ch...@google.com (2026-06-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/491516670)*
