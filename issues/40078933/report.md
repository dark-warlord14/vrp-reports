# Heap-use-after-free in WebCore::SVGImage::setContainerSize

| Field | Value |
|-------|-------|
| **Issue ID** | [40078933](https://issues.chromium.org/issues/40078933) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>SVG |
| **Reporter** | at...@gmail.com |
| **Assignee** | pd...@chromium.org |
| **Created** | 2014-02-18 |
| **Bounty** | $1,000.00 |

## Description



Tested on:

OS: Ubuntu 12.04

Chromium: ASAN 34.0.1837.0 (Developer Build 250634)


To reproduce the issue, create a small HTML that loads the attached SVG-file into an image-tag like this:

<html>
<img id="boom" src=./chrome-heap-use-after-free-WebCoreRenderSVGRootsetContainerSize.svg width=5 height=5></img>
<script>

setInterval(function(){
boom.width=10
boom.height=20
},10)
setInterval(function(){
boom.width=100
boom.height=200
},5)

</script>
</html>



ASAN-trace:

==13907==ERROR: AddressSanitizer: heap-use-after-free on address 0x61300057ca78 at pc 0x7f544d62c45d bp 0x7fffbcd64150 sp 0x7fffbcd64148
WRITE of size 8 at 0x61300057ca78 thread T0 (chrome)
    #0 0x7f544d62c45c in WebCore::RenderSVGRoot::setContainerSize(WebCore::IntSize const&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/svg/RenderSVGRoot.h:56:0
    #1 0x7f544d62bf39 in WebCore::SVGImage::setContainerSize(WebCore::IntSize const&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/svg/graphics/SVGImage.cpp:133:0
    #2 0x7f544d62c620 in WebCore::SVGImage::drawForContainer(WebCore::GraphicsContext*, WebCore::FloatSize, float, WebCore::FloatRect const&, WebCore::FloatRect const&, WebCore::CompositeOperator, blink::WebBlendMode) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/svg/graphics/SVGImage.cpp:180:0
    #3 0x7f544b8b2672 in WebCore::GraphicsContext::drawImage(WebCore::Image*, WebCore::FloatRect const&, WebCore::FloatRect const&, WebCore::CompositeOperator, blink::WebBlendMode, WebCore::RespectImageOrientationEnum, bool) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/graphics/GraphicsContext.cpp:1136:0
    #4 0x7f544b8b2339 in WebCore::GraphicsContext::drawImage(WebCore::Image*, WebCore::FloatRect const&, WebCore::FloatRect const&, WebCore::CompositeOperator, WebCore::RespectImageOrientationEnum, bool) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/graphics/GraphicsContext.cpp:1115:0
    #5 0x7f544b8b2509 in WebCore::GraphicsContext::drawImage(WebCore::Image*, WebCore::IntRect const&, WebCore::CompositeOperator, WebCore::RespectImageOrientationEnum, bool) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/graphics/GraphicsContext.cpp:1105:0
    #6 0x7f544d2510a4 in WebCore::RenderImage::paintIntoRect(WebCore::GraphicsContext*, WebCore::LayoutRect const&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/RenderImage.cpp:473:0
    #7 0x7f544d250043 in WebCore::RenderImage::paintReplaced(WebCore::PaintInfo&, WebCore::LayoutPoint const&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/RenderImage.cpp:385:0
    #8 0x7f544d33f602 in WebCore::RenderReplaced::paint(WebCore::PaintInfo&, WebCore::LayoutPoint const&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/RenderReplaced.cpp:166:0
    #9 0x7f544d25124e in WebCore::RenderImage::paint(WebCore::PaintInfo&, WebCore::LayoutPoint const&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/RenderImage.cpp:394:0
    #10 0x7f544d0c387d in WebCore::RenderBlock::paintAsInlineBlock(WebCore::RenderObject*, WebCore::PaintInfo&, WebCore::LayoutPoint const&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/RenderBlock.cpp:2128:0
.
.
.
0x61300057ca78 is located 184 bytes inside of 352-byte region [0x61300057c9c0,0x61300057cb20)
freed by thread T0 (chrome) here:
    #0 0x7f54477014c1 in __interceptor_free _asan_rtl_:0
    #1 0x7f544b6363cf in WebCore::Node::detach(WebCore::Node::AttachContext const&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Node.cpp:1023:0
    #2 0x7f544b5d8156 in WebCore::Element::detach(WebCore::Node::AttachContext const&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1483:0
    #3 0x7f544b63623c in WebCore::Node::reattach(WebCore::Node::AttachContext const&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Node.cpp:990:0
    #4 0x7f544b5d9631 in WebCore::Element::recalcOwnStyle(WebCore::StyleRecalcChange) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1607:0
    #5 0x7f544b5d92f3 in WebCore::Element::recalcStyle(WebCore::StyleRecalcChange, WebCore::Text*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1574:0
    #6 0x7f544b54b316 in WebCore::Document::updateStyleIfNeeded() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Document.cpp:1801:0
    #7 0x7f544ca72e08 in WebCore::FrameView::performPreLayoutTasks() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/frame/FrameView.cpp:752:0
    #8 0x7f544ca747ea in WebCore::FrameView::layout(bool) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/frame/FrameView.cpp:867:0
    #9 0x7f544ca7dcd1 in WebCore::FrameView::scrollbarExistenceDidChange() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/frame/FrameView.cpp:1757:0
    #10 0x7f544b971275 in WebCore::ScrollView::updateScrollbars(WebCore::IntSize const&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/scroll/ScrollView.cpp:344:0
.
.
.


## Attachments

- [chrome-heap-use-after-free-WebCoreRenderSVGRootsetContainerSize.svg](attachments/chrome-heap-use-after-free-WebCoreRenderSVGRootsetContainerSize.svg) (image/svg+xml, 2.0 KB)

## Timeline

### cl...@chromium.org (2014-02-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-20)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=6251748243013632

### cl...@chromium.org (2014-02-21)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=6125882347356160

### cl...@chromium.org (2014-02-21)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5696103424983040

### cl...@chromium.org (2014-02-21)

schenney@: Can you please take a look or find someone else to own it.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-02-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-25)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=6192826962411520

### cl...@chromium.org (2014-02-25)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=4993867514380288

### in...@chromium.org (2014-02-25)

ah! i was reading the comment wrong. in future, please include everything in a zip archive. like run.html for the main file and then any dependencies like test.svg or whatever with it.

### in...@chromium.org (2014-02-25)

Looks to regress from philip's change - http://src.chromium.org/viewvc/blink/trunk/Source/core/svg/graphics/SVGImage.cpp?r1=142764&r2=142765&

### in...@chromium.org (2014-02-25)

[Empty comment from Monorail migration]

### at...@gmail.com (2014-02-25)

Will do. :)
Thanks for the tip.

### cl...@chromium.org (2014-02-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-25)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4993867514380288

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free WRITE 8
Crash Address: 0x614000042738
Crash State:
  - crash stack -
  WebCore::SVGImage::setContainerSize
  WebCore::SVGImage::drawForContainer
  - free stack -
  WebCore::Node::detach
  WebCore::ContainerNode::detach
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=183765:184307

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96kNTWF-4xsBgQ3DMNB-mtQIZndYT3mACytxvykQpUafPVZkpkC-9dwPshzaMrLp6Sv0H6LT0YOQe5_ii1lHLS7CINhJyo9WFIt3czgBqkGncLenDvfLFM67nR890rQLl-oeNhgUXAbmN0IhJVSe6774YOzUQ



### cl...@chromium.org (2014-02-25)

[Empty comment from Monorail migration]

### pd...@chromium.org (2014-02-26)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-02-26)

[Empty comment from Monorail migration]

### pd...@chromium.org (2014-02-27)

Patch up: https://codereview.chromium.org/178043006

The code change is trivial but I'll need a day to get to my linux box to create a reliable testcase.

### in...@chromium.org (2014-02-27)

We are cutting m33 patch 1 on 5 pm friday (for pwnium). We should try to get this in before that.

### bu...@chromium.org (2014-02-28)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=168113

------------------------------------------------------------------------
r168113 | pdr@chromium.org | 2014-02-28T09:33:50.925221Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/custom/resources/draw-image-crash.svg?r1=168113&r2=168112&pathrev=168113
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/custom/draw-image-crash-expected.txt?r1=168113&r2=168112&pathrev=168113
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/custom/draw-image-crash.html?r1=168113&r2=168112&pathrev=168113
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/svg/graphics/SVGImage.cpp?r1=168113&r2=168112&pathrev=168113

Fix crash when resizing a view destroys the render tree

This is a simple fix for not holding a renderer across FrameView
resizes. Calling view->resize() can destroy renderers so this patch
updates SVGImage::setContainerSize to query the renderer after the
resize is complete. A similar issue does not exist for the dom tree
which is not destroyed.

BUG=344492

Review URL: https://codereview.chromium.org/178043006
------------------------------------------------------------------------

### in...@chromium.org (2014-02-28)

Safe code change. Please merge to m33, m34. Build i getting cut at 5pm.

### bu...@chromium.org (2014-02-28)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=168152

------------------------------------------------------------------------
r168152 | chrome-bot@google.com | 2014-02-28T18:55:06.809281Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/1750/LayoutTests/svg/custom/resources/draw-image-crash.svg?r1=168152&r2=168151&pathrev=168152
   A http://src.chromium.org/viewvc/blink/branches/chromium/1750/LayoutTests/svg/custom/draw-image-crash-expected.txt?r1=168152&r2=168151&pathrev=168152
   A http://src.chromium.org/viewvc/blink/branches/chromium/1750/LayoutTests/svg/custom/draw-image-crash.html?r1=168152&r2=168151&pathrev=168152
   M http://src.chromium.org/viewvc/blink/branches/chromium/1750/Source/core/svg/graphics/SVGImage.cpp?r1=168152&r2=168151&pathrev=168152

Merge 168113 "Fix crash when resizing a view destroys the render..."

> Fix crash when resizing a view destroys the render tree
> 
> This is a simple fix for not holding a renderer across FrameView
> resizes. Calling view->resize() can destroy renderers so this patch
> updates SVGImage::setContainerSize to query the renderer after the
> resize is complete. A similar issue does not exist for the dom tree
> which is not destroyed.
> 
> BUG=344492
> 
> Review URL: https://codereview.chromium.org/178043006

TBR=pdr@chromium.org
BUG=344492

Review URL: https://codereview.chromium.org/180773004
------------------------------------------------------------------------

### bu...@chromium.org (2014-02-28)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=168153

------------------------------------------------------------------------
r168153 | pdr@chromium.org | 2014-02-28T18:53:02.696559Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1847/Source/core/svg/graphics/SVGImage.cpp?r1=168153&r2=168152&pathrev=168153
   A http://src.chromium.org/viewvc/blink/branches/chromium/1847/LayoutTests/svg/custom/resources/draw-image-crash.svg?r1=168153&r2=168152&pathrev=168153
   A http://src.chromium.org/viewvc/blink/branches/chromium/1847/LayoutTests/svg/custom/draw-image-crash-expected.txt?r1=168153&r2=168152&pathrev=168153
   A http://src.chromium.org/viewvc/blink/branches/chromium/1847/LayoutTests/svg/custom/draw-image-crash.html?r1=168153&r2=168152&pathrev=168153

Merge 168113 "Fix crash when resizing a view destroys the render..."

> Fix crash when resizing a view destroys the render tree
> 
> This is a simple fix for not holding a renderer across FrameView
> resizes. Calling view->resize() can destroy renderers so this patch
> updates SVGImage::setContainerSize to query the renderer after the
> resize is complete. A similar issue does not exist for the dom tree
> which is not destroyed.
> 
> BUG=344492
> 
> Review URL: https://codereview.chromium.org/178043006

TBR=pdr@chromium.org
BUG=344492

Review URL: https://codereview.chromium.org/184853002
------------------------------------------------------------------------

### bu...@chromium.org (2014-02-28)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=168154

------------------------------------------------------------------------
r168154 | pdr@chromium.org | 2014-02-28T18:57:46.989178Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/1862/LayoutTests/svg/custom/draw-image-crash-expected.txt?r1=168154&r2=168153&pathrev=168154
   A http://src.chromium.org/viewvc/blink/branches/chromium/1862/LayoutTests/svg/custom/draw-image-crash.html?r1=168154&r2=168153&pathrev=168154
   M http://src.chromium.org/viewvc/blink/branches/chromium/1862/Source/core/svg/graphics/SVGImage.cpp?r1=168154&r2=168153&pathrev=168154
   A http://src.chromium.org/viewvc/blink/branches/chromium/1862/LayoutTests/svg/custom/resources/draw-image-crash.svg?r1=168154&r2=168153&pathrev=168154

Merge 168113 "Fix crash when resizing a view destroys the render..."

> Fix crash when resizing a view destroys the render tree
> 
> This is a simple fix for not holding a renderer across FrameView
> resizes. Calling view->resize() can destroy renderers so this patch
> updates SVGImage::setContainerSize to query the renderer after the
> resize is complete. A similar issue does not exist for the dom tree
> which is not destroyed.
> 
> BUG=344492
> 
> Review URL: https://codereview.chromium.org/178043006

TBR=pdr@chromium.org
BUG=344492

Review URL: https://codereview.chromium.org/184873002
------------------------------------------------------------------------

### dh...@google.com (2014-02-28)

[Empty comment from Monorail migration]

### dh...@google.com (2014-02-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-01)

ClusterFuzz has detected this issue as fixed in range 254148:254228.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4993867514380288

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free WRITE 8
Crash Address: 0x614000042738
Crash State:
  - crash stack -
  WebCore::SVGImage::setContainerSize
  WebCore::SVGImage::drawForContainer
  - free stack -
  WebCore::Node::detach
  WebCore::ContainerNode::detach
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=183765:184307
Fixed: https://cluster-fuzz.appspot.com/revisions?range=254148:254228

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96kNTWF-4xsBgQ3DMNB-mtQIZndYT3mACytxvykQpUafPVZkpkC-9dwPshzaMrLp6Sv0H6LT0YOQe5_ii1lHLS7CINhJyo9WFIt3czgBqkGncLenDvfLFM67nR890rQLl-oeNhgUXAbmN0IhJVSe6774YOzUQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### mb...@chromium.org (2014-03-04)

Thanks for the report! This one qualifies for a $1000 reward. It did not qualify at a higher reward level because there does not appear to be control between the free and use, and the freed object is in a heap partition.

### cl...@chromium.org (2014-03-09)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-14)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-23)

Processing via our e-payment system can take up to 30 days, but reward should be on its way to you. Thanks again for your help!


### cl...@chromium.org (2014-06-06)

Bulk update: removing view restriction from closed bugs.

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/344492?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078933)*
