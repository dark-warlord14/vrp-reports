# Heap-buffer-overflow in SkAlphaRuns::add

| Field | Value |
|-------|-------|
| **Issue ID** | [40052746](https://issues.chromium.org/issues/40052746) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals, Internals>Skia |
| **Reporter** | ao...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2012-01-13 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

ASan reports a heap buffer overflow when the URL  

data:text/html;,<img src="data:image/svg+xml;,<svg xmlns='http://www.w3.org/2000/svg' width='64919' height='1'> <path d='M 0,0 L 1,0 33,1 z'/> </svg>">

is opened. The page has some SVG which has to be within HTML for the issue to occur. This also happens if the SVG is included as an image, the data url is just a bit easier to test.

The overflow is to the left of the object and can be controlled using the width parameter.

**VERSION**  

Chrome Version: 18.0.1005.0 (Developer Build 117194)  

Operating System: Linux (Debian 6.0.3 x86\_64)

**REPRODUCTION CASE**  

Open the above mentioned URL.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

=================================================================  

==4710== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fc42a56fbae at pc 0x7fc43cb20ee7 bp 0x7fff9b849af0 sp 0x7fff9b849ae8  

READ of size 2 at 0x7fc42a56fbae thread T0  

#0 0x7fc43cb20ee7 in SkAlphaRuns::add(int, unsigned int, int, unsigned int, unsigned int, int) ???:0  

#1 0x7fc43ca8b690 in SuperBlitter::blitH(int, int, int) ???:0  

#2 0x7fc43ca980ce in walk\_convex\_edges(SkEdge\*, SkPath::FillType, SkBlitter\*, int, int, void (\*)(SkBlitter\*, int, bool)) third\_party/skia/src/core/SkScan\_Path.cpp:0  

#3 0x7fc43ca9720c in sk\_fill\_path(SkPath const&, SkIRect const\*, SkBlitter\*, int, int, int, SkRegion const&) ???:0  

#4 0x7fc43ca8d1a8 in SkScan::AntiFillPath(SkPath const&, SkRegion const&, SkBlitter\*, bool) ???:0  

#5 0x7fc43ca8e09d in SkScan::AntiFillPath(SkPath const&, SkRasterClip const&, SkBlitter\*) ???:0  

#6 0x7fc43ca246de in SkDraw::drawPath(SkPath const&, SkPaint const&, SkMatrix const\*, bool) const ???:0  

#7 0x7fc43ca1230f in SkCanvas::drawPath(SkPath const&, SkPaint const&) ???:0  

#8 0x7fc43ebe8a5b in WebCore::GraphicsContext::fillPath(WebCore::Path const&) ???:0  

#9 0x7fc440637d82 in WebCore::RenderSVGResourceSolidColor::postApplyResource(WebCore::RenderObject\*, WebCore::GraphicsContext\*&, unsigned short, WebCore::Path const\*, WebCore::RenderSVGShape const\*) ???:0  

#10 0x7fc44063b95a in WebCore::RenderSVGShape::fillAndStrokePath(WebCore::GraphicsContext\*) ???:0  

#11 0x7fc44063c78a in WebCore::RenderSVGShape::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#12 0x7fc43f9ba557 in WebCore::RenderBox::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#13 0x7fc4403385df in WebCore::RenderSVGRoot::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#14 0x7fc43fa8283e in WebCore::RenderLayer::paintLayerContents(WebCore::RenderLayer\*, WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, WTF::HashMap<WebCore::OverlapTestRequestClient\*, WebCore::IntRect, WTF::PtrHash[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::IntRect](javascript:void(0);) >\*, unsigned int) ???:0  

#15 0x7fc43fa7eda2 in WebCore::RenderLayer::paintLayer(WebCore::RenderLayer\*, WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, WTF::HashMap<WebCore::OverlapTestRequestClient\*, WebCore::IntRect, WTF::PtrHash[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::IntRect](javascript:void(0);) >\*, unsigned int) ???:0  

#16 0x7fc43fa83039 in WebCore::RenderLayer::paintLayerContents(WebCore::RenderLayer\*, WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, WTF::HashMap<WebCore::OverlapTestRequestClient\*, WebCore::IntRect, WTF::PtrHash[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::IntRect](javascript:void(0);) >\*, unsigned int) ???:0  

#17 0x7fc43fa7eda2 in WebCore::RenderLayer::paintLayer(WebCore::RenderLayer\*, WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, WTF::HashMap<WebCore::OverlapTestRequestClient\*, WebCore::IntRect, WTF::PtrHash[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::IntRect](javascript:void(0);) >\*, unsigned int) ???:0  

#18 0x7fc43fa7d77d in WebCore::RenderLayer::paint(WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, unsigned int) ???:0  

#19 0x7fc43f428075 in WebCore::FrameView::paintContents(WebCore::GraphicsContext\*, WebCore::IntRect const&) ???:0  

#20 0x7fc43eabc53c in WebCore::ScrollView::paint(WebCore::GraphicsContext\*, WebCore::IntRect const&) ???:0  

#21 0x7fc4405fe4f9 in WebCore::SVGImage::draw(WebCore::GraphicsContext\*, WebCore::FloatRect const&, WebCore::FloatRect const&, WebCore::ColorSpace, WebCore::CompositeOperator) ???:0  

#22 0x7fc4405fdce6 in WebCore::SVGImage::drawSVGToImageBuffer(WebCore::ImageBuffer\*, WebCore::IntSize const&, float, WebCore::SVGImage::ShouldClearBuffer) ???:0  

#23 0x7fc4405f99e5 in WebCore::SVGImageCache::lookupOrCreateBitmapImageForRenderer(WebCore::RenderObject const\*) ???:0  

#24 0x7fc43f353007 in WebCore::CachedImage::imageForRenderer(WebCore::RenderObject const\*) ???:0  

#25 0x7fc43fa42453 in WebCore::RenderImageResource::image(int, int) const ???:0  

#26 0x7fc43fa3df36 in WebCore::RenderImage::paintReplaced(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#27 0x7fc43fb2154e in WebCore::RenderReplaced::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#28 0x7fc43fa3e6f8 in WebCore::RenderImage::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#29 0x7fc43f8d3694 in WebCore::InlineBox::paint(WebCore::PaintInfo&, WebCore::IntPoint const&, int, int) ???:0  

#30 0x7fc43f8e5b65 in WebCore::InlineFlowBox::paint(WebCore::PaintInfo&, WebCore::IntPoint const&, int, int) ???:0  

#31 0x7fc43fbcf12a in WebCore::RootInlineBox::paint(WebCore::PaintInfo&, WebCore::IntPoint const&, int, int) ???:0  

#32 0x7fc43fac488e in WebCore::RenderLineBoxList::paint(WebCore::RenderBoxModelObject\*, WebCore::PaintInfo&, WebCore::IntPoint const&) const ???:0  

#33 0x7fc43f934d30 in WebCore::RenderBlock::paintContents(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#34 0x7fc43f936326 in WebCore::RenderBlock::paintObject(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#35 0x7fc43f931528 in WebCore::RenderBlock::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#36 0x7fc43f935603 in WebCore::RenderBlock::paintChildren(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#37 0x7fc43f934d40 in WebCore::RenderBlock::paintContents(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#38 0x7fc43f936326 in WebCore::RenderBlock::paintObject(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#39 0x7fc43f931528 in WebCore::RenderBlock::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#40 0x7fc43fa8283e in WebCore::RenderLayer::paintLayerContents(WebCore::RenderLayer\*, WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, WTF::HashMap<WebCore::OverlapTestRequestClient\*, WebCore::IntRect, WTF::PtrHash[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::IntRect](javascript:void(0);) >\*, unsigned int) ???:0  

#41 0x7fc43fa7eda2 in WebCore::RenderLayer::paintLayer(WebCore::RenderLayer\*, WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, WTF::HashMap<WebCore::OverlapTestRequestClient\*, WebCore::IntRect, WTF::PtrHash[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::IntRect](javascript:void(0);) >\*, unsigned int) ???:0  

#42 0x7fc43fa83039 in WebCore::RenderLayer::paintLayerContents(WebCore::RenderLayer\*, WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, WTF::HashMap<WebCore::OverlapTestRequestClient\*, WebCore::IntRect, WTF::PtrHash[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::IntRect](javascript:void(0);) >\*, unsigned int) ???:0  

#43 0x7fc43fa7eda2 in WebCore::RenderLayer::paintLayer(WebCore::RenderLayer\*, WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, WTF::HashMap<WebCore::OverlapTestRequestClient\*, WebCore::IntRect, WTF::PtrHash[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::IntRect](javascript:void(0);) >\*, unsigned int) ???:0  

#44 0x7fc43fa7d77d in WebCore::RenderLayer::paint(WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, unsigned int) ???:0  

#45 0x7fc43f428075 in WebCore::FrameView::paintContents(WebCore::GraphicsContext\*, WebCore::IntRect const&) ???:0  

#46 0x7fc43eabc53c in WebCore::ScrollView::paint(WebCore::GraphicsContext\*, WebCore::IntRect const&) ???:0  

#47 0x7fc43e09aa76 in WebKit::WebFrameImpl::paintWithContext(WebCore::GraphicsContext&, WebKit::WebRect const&) ???:0  

#48 0x7fc43e09adb9 in WebKit::WebFrameImpl::paint(SkCanvas\*, WebKit::WebRect const&) ???:0  

#49 0x7fc43e0e269e in WebKit::WebViewImpl::paint(SkCanvas\*, WebKit::WebRect const&) ???:0  

#50 0x7fc4414b53e8 in RenderWidget::PaintRect(gfx::Rect const&, gfx::Point const&, skia::PlatformCanvas\*) ???:0  

#51 0x7fc4414ba400 in RenderWidget::DoDeferredUpdate() ???:0  

#52 0x7fc4414addf5 in RenderWidget::OnUpdateRectAck() ???:0  

#53 0x7fc4414ac739 in RenderWidget::OnMessageReceived(IPC::Message const&) ???:0  

#54 0x7fc44145b137 in RenderViewImpl::OnMessageReceived(IPC::Message const&) ???:0  

#55 0x7fc43dfa8b88 in MessageRouter::RouteMessage(IPC::Message const&) ???:0  

#56 0x7fc43dfa89f0 in MessageRouter::OnMessageReceived(IPC::Message const&) ???:0  

#57 0x7fc43ded4645 in ChildThread::OnMessageReceived(IPC::Message const&) ???:0  

#58 0x7fc43e01d469 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ???:0  

#59 0x7fc43c8c2cd4 in MessageLoop::RunTask(base::PendingTask const&) ???:0  

#60 0x7fc43c8c3556 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) ???:0  

#61 0x7fc43c8c4841 in MessageLoop::DoWork() ???:0  

#62 0x7fc43c8cf2a7 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ???:0  

#63 0x7fc43c8c18ce in MessageLoop::RunInternal() ???:0  

0x7fc42a56fbae is located 1234 bytes to the left of 194760-byte region [0x7fc42a570080,0x7fc42a59f948)  

allocated by thread T0 here:  

#0 0x7fc442036c54 in malloc ??:0  

#1 0x7fc43cb08519 in sk\_malloc\_throw(unsigned long) ???:0  

#2 0x7fc43ca8d091 in SkScan::AntiFillPath(SkPath const&, SkRegion const&, SkBlitter\*, bool) ???:0  

#3 0x7fc43ca8e09d in SkScan::AntiFillPath(SkPath const&, SkRasterClip const&, SkBlitter\*) ???:0  

#4 0x7fc43ca246de in SkDraw::drawPath(SkPath const&, SkPaint const&, SkMatrix const\*, bool) const ???:0  

#5 0x7fc43ca1230f in SkCanvas::drawPath(SkPath const&, SkPaint const&) ???:0  

#6 0x7fc43ebe8a5b in WebCore::GraphicsContext::fillPath(WebCore::Path const&) ???:0  

#7 0x7fc440637d82 in WebCore::RenderSVGResourceSolidColor::postApplyResource(WebCore::RenderObject\*, WebCore::GraphicsContext\*&, unsigned short, WebCore::Path const\*, WebCore::RenderSVGShape const\*) ???:0  

#8 0x7fc44063b95a in WebCore::RenderSVGShape::fillAndStrokePath(WebCore::GraphicsContext\*) ???:0  

#9 0x7fc44063c78a in WebCore::RenderSVGShape::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#10 0x7fc43f9ba557 in WebCore::RenderBox::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#11 0x7fc4403385df in WebCore::RenderSVGRoot::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#12 0x7fc43fa8283e in WebCore::RenderLayer::paintLayerContents(WebCore::RenderLayer\*, WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, WTF::HashMap<WebCore::OverlapTestRequestClient\*, WebCore::IntRect, WTF::PtrHash[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::IntRect](javascript:void(0);) >\*, unsigned int) ???:0  

#13 0x7fc43fa7eda2 in WebCore::RenderLayer::paintLayer(WebCore::RenderLayer\*, WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, WTF::HashMap<WebCore::OverlapTestRequestClient\*, WebCore::IntRect, WTF::PtrHash[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::IntRect](javascript:void(0);) >\*, unsigned int) ???:0  

#14 0x7fc43fa83039 in WebCore::RenderLayer::paintLayerContents(WebCore::RenderLayer\*, WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, WTF::HashMap<WebCore::OverlapTestRequestClient\*, WebCore::IntRect, WTF::PtrHash[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::IntRect](javascript:void(0);) >\*, unsigned int) ???:0  

#15 0x7fc43fa7eda2 in WebCore::RenderLayer::paintLayer(WebCore::RenderLayer\*, WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, WTF::HashMap<WebCore::OverlapTestRequestClient\*, WebCore::IntRect, WTF::PtrHash[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::IntRect](javascript:void(0);) >\*, unsigned int) ???:0  

#16 0x7fc43fa7d77d in WebCore::RenderLayer::paint(WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, unsigned int) ???:0  

#17 0x7fc43f428075 in WebCore::FrameView::paintContents(WebCore::GraphicsContext\*, WebCore::IntRect const&) ???:0  

#18 0x7fc43eabc53c in WebCore::ScrollView::paint(WebCore::GraphicsContext\*, WebCore::IntRect const&) ???:0  

#19 0x7fc4405fe4f9 in WebCore::SVGImage::draw(WebCore::GraphicsContext\*, WebCore::FloatRect const&, WebCore::FloatRect const&, WebCore::ColorSpace, WebCore::CompositeOperator) ???:0  

#20 0x7fc4405fdce6 in WebCore::SVGImage::drawSVGToImageBuffer(WebCore::ImageBuffer\*, WebCore::IntSize const&, float, WebCore::SVGImage::ShouldClearBuffer) ???:0  

#21 0x7fc4405f99e5 in WebCore::SVGImageCache::lookupOrCreateBitmapImageForRenderer(WebCore::RenderObject const\*) ???:0  

#22 0x7fc43f353007 in WebCore::CachedImage::imageForRenderer(WebCore::RenderObject const\*) ???:0  

==4710== ABORTING  

Stats: 3M malloced (5M for red zones) by 20774 calls  

Stats: 0M realloced by 47 calls  

Stats: 1M freed by 12259 calls  

Stats: 0M really freed by 0 calls  

Stats: 48M (12295 full pages) mmaped in 12 calls  

mmaps by size class: 8:32766; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:256; 15:128; 16:64; 17:32; 18:16;  

mallocs by size class: 8:18147; 9:1266; 10:898; 11:279; 12:69; 13:40; 14:53; 15:9; 16:9; 17:2; 18:2;  

frees by size class: 8:10432; 9:803; 10:768; 11:156; 12:30; 13:21; 14:41; 15:5; 16:3;  

rfrees by size class:  

Stats: malloc large: 4 small slow: 85  

Shadow byte and word:  

0x1ff8854adf75: fa  

0x1ff8854adf70: fa fa fa fa fa fa fa fa  

More shadow bytes:  

0x1ff8854adf50: fa fa fa fa fa fa fa fa  

0x1ff8854adf58: fa fa fa fa fa fa fa fa  

0x1ff8854adf60: fa fa fa fa fa fa fa fa  

0x1ff8854adf68: fa fa fa fa fa fa fa fa  

=>0x1ff8854adf70: fa fa fa fa fa fa fa fa  

0x1ff8854adf78: fa fa fa fa fa fa fa fa  

0x1ff8854adf80: fa fa fa fa fa fa fa fa  

0x1ff8854adf88: fa fa fa fa fa fa fa fa  

0x1ff8854adf90: fa fa fa fa fa fa fa fa

## Attachments

- [test.html](attachments/test.html) (text/plain; charset=us-ascii, 136 B)
- [bof.html](attachments/bof.html) (text/plain; charset=us-ascii, 80 B)
- [butterfly.svg](attachments/butterfly.svg) (image/svg+xml; charset=us-ascii, 30.5 KB)
- [asan.txt](attachments/asan.txt) (text/plain; charset=us-ascii, 14.4 KB)

## Timeline

### [Deleted User] (2012-01-13)

[Empty comment from Monorail migration]

### [Deleted User] (2012-01-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-01-14)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=12075738

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x7f96cf278bae
Crash State:
  - crash stack -
  SkAlphaRuns::add
  SuperBlitter::blitH
  walk_convex_edges
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=109066:109135

Minimized Testcase (0.13 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96VK_SIcvcF58jH44wjiSkElkJL2xT2K-m67oJBNaJY5sfYvVeasIdeSpiT1WxdUJ40uoRTwfWQ6apSS5V0QHLIEVLGPbuwK302McU9q_P1JGlRNyzqaD0WACv-hmAb2PLjRiIzR4eAv4L2dHxHvsAtAuHJJw

### in...@chromium.org (2012-01-14)

Aki, please avoid providing data url as testcases. Just please add the html file as attachment to the bug.

### in...@chromium.org (2012-01-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-01-16)

Mike, from the regression range, it looks like coming from Niko's https://trac.webkit.org/changeset/99539/, but the crash is happening inside Skia. Can you please try to debug to see if it is Skia specific or a svg issue. Thanks a lot.

### js...@chromium.org (2012-01-24)

It's too late for m17 stable, but this needs to make it into the first m16 patch. Reed, can you look into this ASAP (or find someone to)?

### in...@chromium.org (2012-01-26)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-01-26)

This is a straight integer wrap on width 64919 to 16-bit int

void SkAlphaRuns::reset(int width) {
......
    fRuns[0] = SkToS16(width);
    fRuns[width] = 0;

### [Deleted User] (2012-01-26)

[Empty comment from Monorail migration]

### [Deleted User] (2012-01-27)

static void test_giant() {
    SkBitmap bm;
    bm.setConfig(SkBitmap::kARGB_8888_Config, 64919, 1);
    bm.allocPixels();
    SkCanvas canvas(bm);
    canvas.clear(0);
    
    SkPath path;
    path.moveTo(0, 0); path.lineTo(1, 0); path.lineTo(33, 1);
    SkPaint paint;
    paint.setAntiAlias(true);
    canvas.drawPath(path, paint);
}

This function seems to repro the bug. When Skia antialiases, I allocated a scanline buffer the width of the device (even if that is wider than the current path in this case). The buffer stores offsets into that scanline, as signed 16bit values. Since this device's width is > 32767, we hit a bug where the computed offset (64919) looks negative.

1. We can make the buffer unsigned, but I think that only pushes the problem to where the width is 65536+ and then we're stuck again.
2. We can impose a clip at 16bits on the operation, which should fix this, but will mean we can draw beyond that.
3. We can, combined with #2, draw the path in a tile-loop, so that each "tile" never exceeds 32K.

I vote for #2 now and #3 later, but will have to investigate more.


### re...@google.com (2012-01-30)

fixed in skia rev. 3105

### sc...@gmail.com (2012-01-30)

[Empty comment from Monorail migration]

### se...@chromium.org (2012-01-31)

One thing I don't understand:  Chrome is compiled with SK_SCALAR_IS_FLOAT, but this fix only seems to affect SK_SCALAR_IS_FIXED.  Am I missing something?

### re...@google.com (2012-01-31)

3105 is the tail-end of the fix. 3104 contains the meat of the code change.

### se...@chromium.org (2012-01-31)

reed: ahh, thanks for clueing me in.

### sc...@gmail.com (2012-02-05)

Thanks for catching this, Aki! Good regression catch. Unfortunately, Chrome 17 will have the bug but we'll put it down in a Chrome 17 patch a week or so after the initial release.

$1000

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### ao...@gmail.com (2012-02-05)

@scarybeasts excellent, thanks :)

### re...@google.com (2012-02-07)

skia rev. 3104 has the fix to constraint our bounds to 32K

### [Deleted User] (2012-02-07)

[Empty comment from Monorail migration]

### ep...@google.com (2012-02-07)

I landed the cherrypick to Skia's "963a" branch in http://code.google.com/p/skia/source/detail?r=3152 ; I have confirmed that this change is picked up when I sync my M17 (963) chrome branch.

Unfortunately, I was unable to reproduce the original bug on my Mac, and I am having trouble building M17 Chrome on my Linux machine, so I cannot verify that the Skia cherrypick fixes the M17 build.  Can someone please confirm that it does?


### sc...@gmail.com (2012-02-10)

Confirmed good on M17 branch, thanks!! :D

### sc...@gmail.com (2012-02-11)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-02-16)

[Empty comment from Monorail migration]

### ao...@gmail.com (2012-02-23)

Hey, this issue is still turning up for 19.0.1048.0 even though the original repro doesn't trigger it. Attached one triggering it by having the (unmodified) butterfly.svg in a div of specific size.

### sc...@gmail.com (2012-02-23)

Eek! What about the latest stable patch?

Could you file a new bug and include information about whether stable is affected?

### re...@google.com (2012-02-23)

fixed in skia rev. 3240, 3242

### ao...@gmail.com (2012-02-23)

Forgot to link here: http://code.google.com/p/chromium/issues/detail?id=115471 tracks the second overflow. It did affect stable, and reed's patches took care of it here.

### in...@chromium.org (2012-02-23)

done the updates in http://code.google.com/p/chromium/issues/detail?id=115471

### sc...@gmail.com (2012-02-23)

That was really fast Mike, thanks!! :D

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

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

This issue was migrated from crbug.com/chromium/110172?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Skia]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052746)*
