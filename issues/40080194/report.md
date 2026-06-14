# Heap-use-after-free in blink::RenderLayerScrollableArea::updateCompositingLayersAfterScroll

| Field | Value |
|-------|-------|
| **Issue ID** | [40080194](https://issues.chromium.org/issues/40080194) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ha...@chromium.org |
| **Created** | 2014-08-11 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached testcase crashes stable Chrome on Windows and the latest ASAN build.

The freed object doesn't seem to be protected by Partition Alloc.

**VERSION**  

Chrome Version: stable and dev  

Operating System: Linux and Windows

**REPRODUCTION CASE**  

Attached in crash.zip as it requires multiple files to repro.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: ASAN output attached in debug.txt

## Attachments

- [crash.zip](attachments/crash.zip) (application/zip, 1.3 KB)
- [debug.txt](attachments/debug.txt) (text/plain, 16.5 KB)

## Timeline

### cl...@chromium.org (2014-08-11)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5781213245603840

### in...@chromium.org (2014-08-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-11)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=4833017560301568

### cl...@chromium.org (2014-08-11)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4833017560301568

Uploader: inferno@chromium.org
Job Type: Windows_asan_chrome

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x03c346b4
Crash State:
  - crash stack -
  blink::RenderLayerScrollableArea::updateCompositingLayersAfterScroll
  blink::RenderLayerScrollableArea::setScrollOffset
  - free stack -
  blink::RenderLayerScrollableArea::`scalar
  blink::RenderLayer::~RenderLayer
  

Minimized Testcase (1.05 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94xssa_2eNjF6kRaZIY0KQPzCqVL7xk7ZqWRSmM6vIwCw64K-DfAshAivh9rM0eSuLnSyJJspMyUEtIkF2R8nrGRPBwB53jsGbY0-j2BrBftywEUc3QfJ67BlhVIZvwhJMfrSYzWQgaqpb8O-a_l3TTZhxDYw



### ke...@chromium.org (2014-08-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-11)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5781213245603840

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6110000ce9c0
Crash State:
  - crash stack -
  blink::RenderLayerScrollableArea::updateCompositingLayersAfterScroll
  blink::RenderLayerScrollableArea::setScrollOffset
  - free stack -
  blink::RenderLayer::~RenderLayer
  blink::RenderLayerModelObject::destroyLayer
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=160579:160581

Minimized Testcase (1.07 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94gkA73VAhFDhzdgEm6EPgUniV5wm6jvInoqh6Sd4uDOkSZOxoOwfRfC-4G8zKUS4WR0WDdehCCcux_pJ_S3nICAVzzTvt_FYEhzs05kGVV-SE9m1_npXFHpkF0nWtd8THvotPRKqXrP_coap8iJZrMO2veiQ



### ke...@chromium.org (2014-08-11)

Dana: This is a RenderLayer use-after-free bug, can you please help us find somebody to investigate?

### cl...@chromium.org (2014-08-11)

[Empty comment from Monorail migration]

### da...@chromium.org (2014-08-12)

[Empty comment from Monorail migration]

### ha...@chromium.org (2014-08-12)

After a bit of investigation, here's what I think is happening. Here's a stack trace, with an explanation further down...



#0  blink::ScrollAnimator::~ScrollAnimator (this=<optimized out>) at ../../third_party/WebKit/Source/platform/scroll/ScrollAnimator.cpp:54
#1  0x00007fffee6bb182 in blink::ScrollAnimator::~ScrollAnimator (this=<optimized out>) at ../../third_party/WebKit/Source/platform/scroll/ScrollAnimator.cpp:53
#2  0x00007fffee7386ed in WTF::OwnedPtrDeleter<blink::ScrollAnimator>::deletePtr (ptr=<optimized out>) at ../../third_party/WebKit/Source/wtf/OwnPtrCommon.h:52
#3  0x00007fffee739015 in WTF::OwnPtr<blink::ScrollAnimator>::~OwnPtr (this=<optimized out>) at ../../third_party/WebKit/Source/wtf/OwnPtr.h:67
#4  0x00007fffee738c86 in blink::ScrollableArea::ScrollableAreaAnimators::~ScrollableAreaAnimators (this=<optimized out>) at ../../third_party/WebKit/Source/platform/scroll/ScrollableArea.h:267
#5  0x00007fffee738ad1 in WTF::OwnedPtrDeleter<blink::ScrollableArea::ScrollableAreaAnimators>::deletePtr (ptr=<optimized out>) at ../../third_party/WebKit/Source/wtf/OwnPtrCommon.h:52
#6  0x00007fffee733875 in WTF::OwnPtr<blink::ScrollableArea::ScrollableAreaAnimators>::~OwnPtr (this=<optimized out>) at ../../third_party/WebKit/Source/wtf/OwnPtr.h:67
#7  0x00007fffee725305 in blink::ScrollableArea::~ScrollableArea (this=<optimized out>) at ../../third_party/WebKit/Source/platform/scroll/ScrollableArea.cpp:86
#8  0x00007fffc9e1880e in blink::RenderLayerScrollableArea::~RenderLayerScrollableArea (this=<optimized out>) at ../../third_party/WebKit/Source/core/rendering/RenderLayerScrollableArea.cpp:144
#9  0x00007fffc9e18f32 in blink::RenderLayerScrollableArea::~RenderLayerScrollableArea (this=<optimized out>) at ../../third_party/WebKit/Source/core/rendering/RenderLayerScrollableArea.cpp:107
#10 0x00007fffc9dd1d9d in WTF::OwnedPtrDeleter<blink::RenderLayerScrollableArea>::deletePtr (ptr=<optimized out>) at ../../third_party/WebKit/Source/wtf/OwnPtrCommon.h:52
#11 0x00007fffc9daeb05 in WTF::OwnPtr<blink::RenderLayerScrollableArea>::~OwnPtr (this=<optimized out>) at ../../third_party/WebKit/Source/wtf/OwnPtr.h:67
#12 0x00007fffc9d4d38a in blink::RenderLayer::~RenderLayer (this=<optimized out>) at ../../third_party/WebKit/Source/core/rendering/RenderLayer.cpp:178
#13 0x00007fffc9e0fa81 in WTF::OwnedPtrDeleter<blink::RenderLayer>::deletePtr (ptr=<optimized out>) at ../../third_party/WebKit/Source/wtf/OwnPtrCommon.h:52
#14 0x00007fffc9e0ff04 in WTF::OwnPtr<blink::RenderLayer>::clear (this=<optimized out>) at ../../third_party/WebKit/Source/wtf/OwnPtr.h:135
#15 0x00007fffc9e0dc02 in WTF::OwnPtr<blink::RenderLayer>::operator=(decltype(nullptr)) (this=<optimized out>) at ../../third_party/WebKit/Source/wtf/OwnPtr.h:89
#16 0x00007fffc9e09ad7 in blink::RenderLayerModelObject::destroyLayer (this=<optimized out>) at ../../third_party/WebKit/Source/core/rendering/RenderLayerModelObject.cpp:51
#17 0x00007fffc9d6934e in blink::RenderLayer::removeOnlyThisLayer (this=<optimized out>) at ../../third_party/WebKit/Source/core/rendering/RenderLayer.cpp:1349
#18 0x00007fffc9e0b46d in blink::RenderLayerModelObject::styleDidChange (this=<optimized out>, diff=..., oldStyle=<optimized out>) at ../../third_party/WebKit/Source/core/rendering/RenderLayerModelObject.cpp:128
#19 0x00007fffc98e4c33 in blink::RenderBox::styleDidChange (this=<optimized out>, diff=..., oldStyle=<optimized out>) at ../../third_party/WebKit/Source/core/rendering/RenderBox.cpp:182
#20 0x00007fffc964f24b in blink::RenderBlock::styleDidChange (this=<optimized out>, diff=..., oldStyle=<optimized out>) at ../../third_party/WebKit/Source/core/rendering/RenderBlock.cpp:346
#21 0x00007fffc980435e in blink::RenderBlockFlow::styleDidChange (this=<optimized out>, diff=..., oldStyle=<optimized out>) at ../../third_party/WebKit/Source/core/rendering/RenderBlockFlow.cpp:1949
#22 0x00007fffc9fa23c7 in blink::RenderObject::setStyle (this=<optimized out>, style=...) at ../../third_party/WebKit/Source/core/rendering/RenderObject.cpp:2068
#23 0x00007fffc4955be1 in blink::Element::recalcOwnStyle (this=0x60b00000c0c0, change=blink::NoChange) at ../../third_party/WebKit/Source/core/dom/Element.cpp:1533
#24 0x00007fffc49548de in blink::Element::recalcStyle (this=<optimized out>, change=<optimized out>, nextTextSibling=<optimized out>) at ../../third_party/WebKit/Source/core/dom/Element.cpp:1486
#25 0x00007fffc495754d in blink::Element::recalcChildStyle (this=<optimized out>, change=<optimized out>) at ../../third_party/WebKit/Source/core/dom/Element.cpp:1589
#26 0x00007fffc4954a8b in blink::Element::recalcStyle (this=<optimized out>, change=<optimized out>, nextTextSibling=<optimized out>) at ../../third_party/WebKit/Source/core/dom/Element.cpp:1492
#27 0x00007fffc495754d in blink::Element::recalcChildStyle (this=<optimized out>, change=<optimized out>) at ../../third_party/WebKit/Source/core/dom/Element.cpp:1589
#28 0x00007fffc4954a8b in blink::Element::recalcStyle (this=<optimized out>, change=<optimized out>, nextTextSibling=<optimized out>) at ../../third_party/WebKit/Source/core/dom/Element.cpp:1492
#29 0x00007fffc468e495 in blink::Document::updateStyle (this=<optimized out>, change=<optimized out>) at ../../third_party/WebKit/Source/core/dom/Document.cpp:1892
#30 0x00007fffc468cdc3 in blink::Document::updateRenderTree (this=<optimized out>, change=<optimized out>) at ../../third_party/WebKit/Source/core/dom/Document.cpp:1830
#31 0x00007fffb9a6d27f in blink::Document::updateRenderTreeIfNeeded (this=<optimized out>) at ../../third_party/WebKit/Source/core/dom/Document.h:459
#32 0x00007fffc80f51b4 in blink::FrameView::performPreLayoutTasks (this=<optimized out>) at ../../third_party/WebKit/Source/core/frame/FrameView.cpp:735
#33 0x00007fffc80f8caa in blink::FrameView::layout (this=<optimized out>, allowSubtree=<optimized out>) at ../../third_party/WebKit/Source/core/frame/FrameView.cpp:826
#34 0x00007fffc81382c6 in blink::FrameView::forceLayoutParentViewIfNeeded (this=<optimized out>) at ../../third_party/WebKit/Source/core/frame/FrameView.cpp:702
#35 0x00007fffc80f6a9b in blink::FrameView::performLayout (this=<optimized out>, rootForThisLayout=<optimized out>, inSubtreeLayout=<optimized out>) at ../../third_party/WebKit/Source/core/frame/FrameView.cpp:756
#36 0x00007fffc80fa9a8 in blink::FrameView::layout (this=<optimized out>, allowSubtree=<optimized out>) at ../../third_party/WebKit/Source/core/frame/FrameView.cpp:914
#37 0x00007fffca3148e7 in blink::RenderWidget::updateWidgetPosition (this=<optimized out>) at ../../third_party/WebKit/Source/core/rendering/RenderWidget.cpp:291
#38 0x00007fffc8101967 in blink::FrameView::updateWidgetPositions (this=<optimized out>) at ../../third_party/WebKit/Source/core/frame/FrameView.cpp:1068
#39 0x00007fffc9e22dc1 in blink::RenderLayerScrollableArea::setScrollOffset (this=<optimized out>, newScrollOffset=...) at ../../third_party/WebKit/Source/core/rendering/RenderLayerScrollableArea.cpp:372
#40 0x00007fffee728a48 in blink::ScrollableArea::scrollPositionChanged (this=<optimized out>, position=...) at ../../third_party/WebKit/Source/platform/scroll/ScrollableArea.cpp:193
#41 0x00007fffee72adcc in blink::ScrollableArea::setScrollOffsetFromAnimation (this=<optimized out>, offset=...) at ../../third_party/WebKit/Source/platform/scroll/ScrollableArea.cpp:254
#42 0x00007fffee6bfa09 in blink::ScrollAnimator::notifyPositionChanged (this=<optimized out>) at ../../third_party/WebKit/Source/platform/scroll/ScrollAnimator.cpp:144
#43 0x00007fffee6bcfda in blink::ScrollAnimator::scrollToOffsetWithoutAnimation (this=<optimized out>, offset=...) at ../../third_party/WebKit/Source/platform/scroll/ScrollAnimator.cpp:74
#44 0x00007fffee7275ed in blink::ScrollableArea::scrollToOffsetWithoutAnimation (this=<optimized out>, offset=...) at ../../third_party/WebKit/Source/platform/scroll/ScrollableArea.cpp:163
#45 0x00007fffc9e2b7b5 in blink::RenderLayerScrollableArea::scrollToOffset (this=<optimized out>, scrollOffset=..., clamp=<optimized out>) at ../../third_party/WebKit/Source/core/rendering/RenderLayerScrollableArea.cpp:571
#46 0x00007fffc9e476b0 in blink::RenderLayerScrollableArea::exposeRect (this=<optimized out>, rect=..., alignX=..., alignY=...) at ../../third_party/WebKit/Source/core/rendering/RenderLayerScrollableArea.cpp:1386
#47 0x00007fffc98edfbf in blink::RenderBox::scrollRectToVisible (this=<optimized out>, rect=..., alignX=..., alignY=...) at ../../third_party/WebKit/Source/core/rendering/RenderBox.cpp:468
#48 0x00007fffc98f1648 in blink::RenderBox::scrollRectToVisible (this=<optimized out>, rect=..., alignX=..., alignY=...) at ../../third_party/WebKit/Source/core/rendering/RenderBox.cpp:518
#49 0x00007fffc98f1648 in blink::RenderBox::scrollRectToVisible (this=<optimized out>, rect=..., alignX=..., alignY=...) at ../../third_party/WebKit/Source/core/rendering/RenderBox.cpp:518
#50 0x00007fffc98f1648 in blink::RenderBox::scrollRectToVisible (this=<optimized out>, rect=..., alignX=..., alignY=...) at ../../third_party/WebKit/Source/core/rendering/RenderBox.cpp:518
#51 0x00007fffc98f1648 in blink::RenderBox::scrollRectToVisible (this=<optimized out>, rect=..., alignX=..., alignY=...) at ../../third_party/WebKit/Source/core/rendering/RenderBox.cpp:518
#52 0x00007fffc98f1648 in blink::RenderBox::scrollRectToVisible (this=<optimized out>, rect=..., alignX=..., alignY=...) at ../../third_party/WebKit/Source/core/rendering/RenderBox.cpp:518
#53 0x00007fffc9f5961c in blink::RenderObject::scrollRectToVisible (this=<optimized out>, rect=..., alignX=..., alignY=...) at ../../third_party/WebKit/Source/core/rendering/RenderObject.cpp:576
#54 0x00007fffc810a562 in blink::FrameView::scrollToAnchor (this=<optimized out>) at ../../third_party/WebKit/Source/core/frame/FrameView.cpp:1855
#55 0x00007fffc8109f36 in blink::FrameView::maintainScrollPositionAtAnchor (this=<optimized out>, anchorNode=<optimized out>) at ../../third_party/WebKit/Source/core/frame/FrameView.cpp:1421
#56 0x00007fffc8109a43 in blink::FrameView::scrollToAnchor (this=<optimized out>, name=...) at ../../third_party/WebKit/Source/core/frame/FrameView.cpp:1398
#57 0x00007fffc8108ef9 in blink::FrameView::scrollToFragment (this=<optimized out>, url=...) at ../../third_party/WebKit/Source/core/frame/FrameView.cpp:1360
#58 0x00007fffc8cbabed in blink::FrameLoader::scrollToFragmentWithParentBoundary (this=<optimized out>, url=...) at ../../third_party/WebKit/Source/core/loader/FrameLoader.cpp:1218
#59 0x00007fffc8cbe387 in blink::FrameLoader::loadInSameDocument (this=<optimized out>, url=..., stateObject=..., type=<optimized out>, clientRedirect=<optimized out>) at ../../third_party/WebKit/Source/core/loader/FrameLoader.cpp:582
#60 0x00007fffc8cc1c55 in blink::FrameLoader::load (this=<optimized out>, passedRequest=...) at ../../third_party/WebKit/Source/core/loader/FrameLoader.cpp:759
#61 0x00007fffc8d21640 in blink::NavigationScheduler::scheduleLocationChange (this=<optimized out>, originDocument=<optimized out>, url=..., referrer=..., lockBackForwardList=false) at ../../third_party/WebKit/Source/core/loader/NavigationScheduler.c
pp:316
#62 0x00007fffc81f3420 in blink::LocalDOMWindow::setLocation (this=<optimized out>, urlString=..., callingWindow=<optimized out>, enteredWindow=<optimized out>, locking=<optimized out>) at ../../third_party/WebKit/Source/core/frame/LocalDOMWindow.cp
#63 0x00007fffc82802e1 in blink::Location::setLocation (this=<optimized out>, url=..., callingWindow=<optimized out>, enteredWindow=<optimized out>) at ../../third_party/WebKit/Source/core/frame/Location.cpp:251
#64 0x00007fffc82826b2 in blink::Location::setHash (this=<optimized out>, callingWindow=<optimized out>, enteredWindow=<optimized out>, hash=...) at ../../third_party/WebKit/Source/core/frame/Location.cpp:218
#65 0x00007fffbf554eac in blink::LocationV8Internal::hashAttributeSetter (v8Value=..., info=...) at gen/blink/bindings/core/v8/V8Location.cpp:272
#66 0x00007fffbf55234f in blink::LocationV8Internal::hashAttributeSetterCallback (v8Value=..., info=...) at gen/blink/bindings/core/v8/V8Location.cpp:278
#67 0x00007fffeb69e550 in v8::internal::PropertyCallbackArguments::Call (this=<optimized out>, f=<optimized out>, arg1=..., arg2=...) at ../../v8/src/arguments.cc:89
#68 0x00007fffebf66aab in v8::internal::Object::SetPropertyWithAccessor (receiver=..., name=..., value=..., holder=..., structure=..., strict_mode=<optimized out>) at ../../v8/src/objects.cc:506
#69 0x00007fffebfa66b0 in v8::internal::Object::SetProperty (it=<optimized out>, value=..., strict_mode=<optimized out>, store_mode=<optimized out>) at ../../v8/src/objects.cc:3015
#70 0x00007fffebfa56ce in v8::internal::Object::SetProperty (object=..., name=..., value=..., strict_mode=<optimized out>, store_mode=<optimized out>) at ../../v8/src/objects.cc:2945
#71 0x00007fffebde7779 in v8::internal::StoreIC::Store (this=<optimized out>, object=..., name=..., value=..., store_mode=<optimized out>) at ../../v8/src/ic.cc:1423
#72 0x00007fffebdf5ec7 in __RT_impl_StoreIC_Miss (args=..., isolate=<optimized out>) at ../../v8/src/ic.cc:2155
#73 v8::internal::StoreIC_Miss (args_length=<optimized out>, args_object=<optimized out>, isolate=<optimized out>) at ../../v8/src/ic.cc:2146


In frame 39 above, a RenderLayerScrollableArea (call it R), in setScrollOffset, calls into updateWidgetPosition, which goes through some FrameView/Document/Element layout/style update code, which causes a RenderLayer to destruct in frames ~12-16. This RenderLayer, I believe, is the owner of our RenderLayerScrollableArea, R (I'll work on confirming this). It of course ends up destructing R and R's ScrollAnimator.

After all that, style and layout finish, and the stack unwinds back up to frame 39, where the now nonexistent R continues to try to execute code. It calls into UpdateCompositingLayersAfterScroll (https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/core/rendering/RenderLayerScrollableArea.cpp&sq=package:chromium&type=cs&l=372), and ASAN catches it trying to access its layer's RenderBox here https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/core/rendering/RenderLayerScrollableArea.cpp&sq=package:chromium&type=cs&l=518


Overall, this is uncannily reminiscent of https://code.google.com/p/chromium/issues/detail?id=322891#c8

### cl...@chromium.org (2014-08-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-19)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5781213245603840

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6110000ce9c0
Crash State:
  blink::RenderLayerScrollableArea::updateCompositingLayersAfterScroll
  blink::RenderLayerScrollableArea::setScrollOffset
  - free stack -
  blink::RenderLayer::~RenderLayer
  blink::RenderLayerModelObject::destroyLayer
  

Minimized Testcase (1.07 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94gkA73VAhFDhzdgEm6EPgUniV5wm6jvInoqh6Sd4uDOkSZOxoOwfRfC-4G8zKUS4WR0WDdehCCcux_pJ_S3nICAVzzTvt_FYEhzs05kGVV-SE9m1_npXFHpkF0nWtd8THvotPRKqXrP_coap8iJZrMO2veiQ



### ha...@chromium.org (2014-08-19)

To fix this, I'm proposing that we defer the call to updateWidgetPositions() so that we can call it directly from FrameView, outside of the render tree.

I have a working CL up here https://codereview.chromium.org/490473003, if anyone has an opinion on this approach, I'd be glad to hear it.

Also, I believe that FrameView::updateLayoutAndStyleForPainting(), which is where I put the deferred call to updateWidgetPositions(), gets called every frame. I'm basing that on the fact that it's where the compositing updates are initiated from, but I haven't been able to convince myself 100% that the call will be guaranteed. Can anyone confirm whether or not FrameView::updateLayoutAndStyleForPainting() is guaranteed to be called every frame?

### ab...@chromium.org (2014-08-19)

> Can anyone confirm whether or not FrameView::updateLayoutAndStyleForPainting() is guaranteed to be called every frame?

Yes, it is called every frame.  It's the main hammer for cleaning out the system and preparing it to commit to CC.

### ha...@chromium.org (2014-08-19)

Great, thanks, Adam.

### bu...@chromium.org (2014-08-20)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=180681

------------------------------------------------------------------
r180681 | hartmanng@chromium.org | 2014-08-20T20:09:23.038557Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/compositing/overflow/do-not-crash-use-after-free-update-widget-positions-expected.txt?r1=180681&r2=180680&pathrev=180681
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/compositing/overflow/resources/do-not-crash-use-after-free-update-widget-positions-iframe.html?r1=180681&r2=180680&pathrev=180681
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/frame/FrameView.cpp?r1=180681&r2=180680&pathrev=180681
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/compositing/overflow/do-not-crash-use-after-free-update-widget-positions.html?r1=180681&r2=180680&pathrev=180681
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/frame/FrameView.h?r1=180681&r2=180680&pathrev=180681
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/RenderLayerScrollableArea.cpp?r1=180681&r2=180680&pathrev=180681
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/compositing/overflow/resources/do-not-crash-use-after-free-update-widget-positions.svg?r1=180681&r2=180680&pathrev=180681

Defer call to updateWidgetPositions() outside of RenderLayerScrollableArea.

updateWidgetPositions() can destroy the render tree, so it should never
be called from inside RenderLayerScrollableArea. Leaving it there allows
for the potential of use-after-free bugs.

BUG=402407
R=vollick@chromium.org

Review URL: https://codereview.chromium.org/490473003
-----------------------------------------------------------------

### in...@chromium.org (2014-08-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-21)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5781213245603840

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6110000ce9c0
Crash State:
  blink::RenderLayerScrollableArea::updateCompositingLayersAfterScroll
  blink::RenderLayerScrollableArea::setScrollOffset
  - free stack -
  blink::RenderLayer::~RenderLayer
  blink::RenderLayerModelObject::destroyLayer
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=231811:231820

Minimized Testcase (1.07 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94gkA73VAhFDhzdgEm6EPgUniV5wm6jvInoqh6Sd4uDOkSZOxoOwfRfC-4G8zKUS4WR0WDdehCCcux_pJ_S3nICAVzzTvt_FYEhzs05kGVV-SE9m1_npXFHpkF0nWtd8THvotPRKqXrP_coap8iJZrMO2veiQ



### cl...@chromium.org (2014-08-21)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-08-22)

ClusterFuzz has detected this issue as fixed in range 291041:291212.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4833017560301568

Uploader: inferno@chromium.org
Job Type: Windows_asan_chrome

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x03c346b4
Crash State:
  blink::RenderLayerScrollableArea::updateCompositingLayersAfterScroll
  blink::RenderLayerScrollableArea::setScrollOffset
  - free stack -
  blink::RenderLayerScrollableArea::`scalar
  blink::RenderLayer::~RenderLayer
  
Fixed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome&range=291041:291212

Minimized Testcase (1.05 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94xssa_2eNjF6kRaZIY0KQPzCqVL7xk7ZqWRSmM6vIwCw64K-DfAshAivh9rM0eSuLnSyJJspMyUEtIkF2R8nrGRPBwB53jsGbY0-j2BrBftywEUc3QfJ67BlhVIZvwhJMfrSYzWQgaqpb8O-a_l3TTZhxDYw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2014-08-22)

ClusterFuzz has detected this issue as fixed in range 291041:291230.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5781213245603840

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6110000ce9c0
Crash State:
  blink::RenderLayerScrollableArea::updateCompositingLayersAfterScroll
  blink::RenderLayerScrollableArea::setScrollOffset
  - free stack -
  blink::RenderLayer::~RenderLayer
  blink::RenderLayerModelObject::destroyLayer
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=231811:231820
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=291041:291230

Minimized Testcase (1.07 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94gkA73VAhFDhzdgEm6EPgUniV5wm6jvInoqh6Sd4uDOkSZOxoOwfRfC-4G8zKUS4WR0WDdehCCcux_pJ_S3nICAVzzTvt_FYEhzs05kGVV-SE9m1_npXFHpkF0nWtd8THvotPRKqXrP_coap8iJZrMO2veiQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ha...@chromium.org (2014-08-25)

This has been in canary since Friday with no known negative effects. ClusterFuzz has also confirmed it fixed as of Saturday. Requesting merge for m38 branch.

### [Deleted User] (2014-08-26)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-08-26)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=180914

------------------------------------------------------------------
r180914 | hartmanng@chromium.org | 2014-08-26T17:57:47.453486Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/2125/LayoutTests/compositing/overflow/do-not-crash-use-after-free-update-widget-positions.html?r1=180914&r2=180913&pathrev=180914
   M http://src.chromium.org/viewvc/blink/branches/chromium/2125/Source/core/frame/FrameView.h?r1=180914&r2=180913&pathrev=180914
   M http://src.chromium.org/viewvc/blink/branches/chromium/2125/Source/core/rendering/RenderLayerScrollableArea.cpp?r1=180914&r2=180913&pathrev=180914
   A http://src.chromium.org/viewvc/blink/branches/chromium/2125/LayoutTests/compositing/overflow/resources/do-not-crash-use-after-free-update-widget-positions.svg?r1=180914&r2=180913&pathrev=180914
   A http://src.chromium.org/viewvc/blink/branches/chromium/2125/LayoutTests/compositing/overflow/do-not-crash-use-after-free-update-widget-positions-expected.txt?r1=180914&r2=180913&pathrev=180914
   A http://src.chromium.org/viewvc/blink/branches/chromium/2125/LayoutTests/compositing/overflow/resources/do-not-crash-use-after-free-update-widget-positions-iframe.html?r1=180914&r2=180913&pathrev=180914
   M http://src.chromium.org/viewvc/blink/branches/chromium/2125/Source/core/frame/FrameView.cpp?r1=180914&r2=180913&pathrev=180914

Merge 180681 "Defer call to updateWidgetPositions() outside of R..."

> Defer call to updateWidgetPositions() outside of RenderLayerScrollableArea.
> 
> updateWidgetPositions() can destroy the render tree, so it should never
> be called from inside RenderLayerScrollableArea. Leaving it there allows
> for the potential of use-after-free bugs.
> 
> BUG=402407
> R=vollick@chromium.org
> 
> Review URL: https://codereview.chromium.org/490473003

TBR=hartmanng@chromium.org

Review URL: https://codereview.chromium.org/502413003
-----------------------------------------------------------------

### ha...@chromium.org (2014-09-02)

This has now also been in dev since Friday with no negative effects. Requesting merge into m27.

### ha...@chromium.org (2014-09-03)

Just noticed a typo in #26...

Should read "Requesting merge into m37", _not_ m27.

### in...@chromium.org (2014-09-03)

Merge requested for m37, removing m38 label since it is already merged to m38.

### aa...@google.com (2014-09-03)

Fix only a week old, risky for stable, punting release to m38.

### dh...@chromium.org (2014-09-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2014-09-18)

Only taking P0's at this point for 37, reapplying 38 milestone.

### am...@chromium.org (2014-09-18)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-10-07)

Congratulations - $3000 for this under our new reward pricing structure. Notes from the panel: "Use-after-free not protected by partition alloc"

### cl...@chromium.org (2014-11-26)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2014-12-08)

Payment in progress

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### ti...@google.com (2014-12-22)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/402407?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080194)*
