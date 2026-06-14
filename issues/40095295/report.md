# Stale canvas used in WebCore::PlatformContextSkia::save()

| Field | Value |
|-------|-------|
| **Issue ID** | [40095295](https://issues.chromium.org/issues/40095295) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | sl...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2011-09-19 |
| **Bounty** | $1,000.00 |

## Description

Crashes on windows dev [15.0.874.15 (101261)] and canary [16.0.883.0 (101461)].

Possible crashes depend on reproduction way (and lucky :):
Attempt to execute non-executable address 00000000
Attempt to execute non-executable address 00000001
Attempt to execute non-executable address 72756f73
Attempt to execute non-executable address 00822794

and catched while reducing testcase:
Attempt to read from address 00000004
Attempt to execute non-executable address 006e0061

Ways to reproduce:
1. just open c1.html in browser and wait a moment for refresh. In most of cases it will crash with "Attempt to execute non-executable address 00000000"
2. open browser, open webdeveloper tools (Shift+Ctrl+l), open c1.html. Should crash with "Attempt to execute non-executable address 72756f73"
3. open c1.html in browser and after load file but before first refresh open webdeveloper tools and wait for refresh - "Attempt to execute non-executable address 00822794"

(4cc.1434): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
eax=00810c80 ebx=03ce1e70 ecx=00887b40 edx=00000000 esi=03ce1e78 edi=002fef58
eip=00822794 esp=002fef40 ebp=002fefdc iopl=0         nv up ei pl nz ac po nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00010212
00822794 0000            add     byte ptr [eax],al          ds:0023:00810c80=00

ExceptionAddress: 00822794
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000008
   Parameter[1]: 00822794
Attempt to execute non-executable address 00822794

ChildEBP RetAddr  
WARNING: Frame IP not in any known module. Following frames may be wrong.
002fef3c 62711a48 0x822794
002fefdc 62716e3f chrome_61cb0000!WebCore::PlatformContextSkia::save+0xa8
002feff4 6255ce1d chrome_61cb0000!WebCore::GraphicsContext::save+0x4b
002ff000 6255d396 chrome_61cb0000!WebCore::setClip+0x17
002ff1ac 6255cdb5 chrome_61cb0000!WebCore::RenderLayer::paintLayer+0x414
002ff1fc 62639264 chrome_61cb0000!WebCore::RenderLayer::paint+0x3a
002ff234 61d4666e chrome_61cb0000!WebCore::FrameView::paintContents+0x14a
002ff254 6273fdaa chrome_61cb0000!WebKit::WebViewImplContentPainter::paint+0x36
002ff260 6274badd chrome_61cb0000!WebCore::NonCompositedContentHost::paintContents+0x10
002ff2a0 6275b6a7 chrome_61cb0000!WebCore::ContentLayerPainter::paint+0x54
002ff2c8 6275b7c8 chrome_61cb0000!WebCore::LayerTextureUpdaterCanvas::paintContents+0x5b
002ff2f4 6275b273 chrome_61cb0000!WebCore::LayerTextureUpdaterBitmap::prepareToUpdate+0x57
002ff348 6274bc28 chrome_61cb0000!WebCore::TiledLayerChromium::prepareToUpdate+0x1b8
002ff398 6270dcbb chrome_61cb0000!WebCore::ContentLayerChromium::paintContentsIfDirty+0x7e
002ff438 6270db21 chrome_61cb0000!WebCore::CCLayerTreeHost::paintLayerContents+0x162
002ff4f8 6273fc99 chrome_61cb0000!WebCore::CCLayerTreeHost::updateLayers+0x120
002ff510 61d44326 chrome_61cb0000!WebCore::CCSingleThreadProxy::commitIfNeeded+0x3f
002ff51c 61cda42d chrome_61cb0000!WebKit::WebViewImpl::composite+0x36
002ff734 61cd9de4 chrome_61cb0000!RenderWidget::DoDeferredUpdate+0x62b
002ff748 61cd9dbe chrome_61cb0000!RenderWidget::DoDeferredUpdateAndSendInputAck+0x10
002ff768 61cdc51f chrome_61cb0000!RenderWidget::InvalidationCallback+0x91
002ff784 61eb983c chrome_61cb0000!RunnableMethod<RenderWidget,void (__thiscall RenderWidget::*)(void),Tuple0>::Run+0x2b
002ff78c 61eaac8a chrome_61cb0000!base::subtle::TaskClosureAdapter::Run+0xb
002ff7b8 61eaacf6 chrome_61cb0000!MessageLoop::RunTask+0x71
[...]

Attached some different stacktraces.
If it's not duplicate I will try to reduce another testcase, maybe easy to reproduce.

## Attachments

- [stack3.txt](attachments/stack3.txt) (text/x-c++; charset=us-ascii, 6.7 KB)
- [stack5.txt](attachments/stack5.txt) (text/x-c++; charset=us-ascii, 6.8 KB)
- [c1.html](attachments/c1.html) (application/octet-stream; charset=binary, 603 B)
- [stack4.txt](attachments/stack4.txt) (text/x-c++; charset=us-ascii, 6.7 KB)
- [stack1.txt](attachments/stack1.txt) (text/x-c++; charset=us-ascii, 6.7 KB)
- [stack2.txt](attachments/stack2.txt) (text/x-c++; charset=us-ascii, 6.8 KB)
- [stack6.txt](attachments/stack6.txt) (text/x-c++; charset=us-ascii, 7.5 KB)

## Timeline

### in...@chromium.org (2011-09-19)

recent regression, reproduce on canary, debug build on windows, does not reproduce on stable.

Adrienne, will you have some time to look into this. Or can you please help with an owner.

### ja...@chromium.org (2011-09-19)

FYI, this is the same as http://code.google.com/p/chromium/issues/detail?id=96595 and http://code.google.com/p/chromium/issues/detail?id=96711 which I've been investigating (fruitlessly thus far).

### in...@chromium.org (2011-09-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-09-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-09-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-09-19)

Thanks Slaweck for this awesome repro, it help us track down this crash.

### sl...@gmail.com (2011-09-19)

I tried other testcases but, unfortunately, all of them, after reduce, looks like c1.html - <video>,<source> and some js which works as sleep().

### ka...@google.com (2011-09-19)

[Empty comment from Monorail migration]

### ja...@chromium.org (2011-09-19)

the TextureUpdater is null.  I probably broke this with the setLayerTreeHost() changes http://trac.webkit.org/changeset/94431. continuing to investigate...

### ja...@chromium.org (2011-09-19)

Aha, we're disabling compositing during paint, which ends up destroying the ContentLayerChromium::m_textureUpdater before paint returns.  Relevant stacks:

updater goes away here:

#0  WebCore::TiledLayerChromium::setLayerTreeHost (this=0x7ffff0c40400, 
    host=0x0)
    at ../../third_party/WebKit/Source/WebCore/platform/graphics/chromium/TiledLayerChromium.cpp:139
#1  0x00007ffff3b3012d in WebCore::NonCompositedContentHost::setRootLayer (
    this=0x7ffff0c87600, layer=0x0)
    at ../../third_party/WebKit/Source/WebCore/platform/graphics/chromium/NonCompositedContentHost.cpp:59
#2  0x00007ffff3848a07 in WebKit::WebViewImpl::setRootGraphicsLayer (
    this=0x7fffe43f8000, layer=0x0)
    at ../../third_party/WebKit/Source/WebKit/chromium/src/WebViewImpl.cpp:2569
#3  0x00007ffff385eda5 in WebKit::ChromeClientImpl::attachRootGraphicsLayer (
    this=0x7fffe43f8050, frame=0x7ffff0c89000, graphicsLayer=0x0)
    at ../../third_party/WebKit/Source/WebKit/chromium/src/ChromeClientImpl.cpp:853
#4  0x00007ffff4f19c38 in WebCore::RenderLayerCompositor::detachRootLayer (
    this=0x7ffff0c3de70)
    at ../../third_party/WebKit/Source/WebCore/rendering/RenderLayerCompositor.cpp:1855
#5  0x00007ffff4f195a3 in WebCore::RenderLayerCompositor::destroyRootLayer (
    this=0x7ffff0c3de70)
    at ../../third_party/WebKit/Source/WebCore/rendering/RenderLayerCompositor.cpp:1764
---Type <return> to continue, or q <return> to quit---
#6  0x00007ffff4f136c3 in WebCore::RenderLayerCompositor::enableCompositingMode
    (this=0x7ffff0c3de70, enable=false)
    at ../../third_party/WebKit/Source/WebCore/rendering/RenderLayerCompositor.cpp:127
#7  0x00007ffff4f15d17 in WebCore::RenderLayerCompositor::computeCompositingRequirements (this=0x7ffff0c3de70, layer=0x7fffe43496f8, 
    overlapMap=0x7fffffff9e00, compositingState=..., 
    layersChanged=@0x7fffffff9dfc)
    at ../../third_party/WebKit/Source/WebCore/rendering/RenderLayerCompositor.cpp:775
#8  0x00007ffff4f13df7 in WebCore::RenderLayerCompositor::updateCompositingLayers (this=0x7ffff0c3de70, 
    updateType=WebCore::CompositingUpdateOnPaitingOrHitTest, 
    updateRoot=0x7fffe43496f8)
    at ../../third_party/WebKit/Source/WebCore/rendering/RenderLayerCompositor.cpp:293
#9  0x00007ffff4f03e4d in WebCore::RenderLayer::updateCompositingAndLayerListsIfNeeded (this=0x7fffe43496f8)
    at ../../third_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:4016
#10 0x00007ffff4efd993 in WebCore::RenderLayer::paintLayer (
    this=0x7fffe43496f8, rootLayer=0x7fffe43496f8, p=0x7fffe343d280, 
    paintDirtyRect=..., paintBehavior=0, paintingRoot=0x0, 
    overlapTestRequests=0x7fffffffa2d0, paintFlags=0)
---Type <return> to continue, or q <return> to quit---
    at ../../third_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:2724
#11 0x00007ffff4efcc5f in WebCore::RenderLayer::paint (this=0x7fffe43496f8, 
    p=0x7fffe343d280, damageRect=..., paintBehavior=0, paintingRoot=0x0)
    at ../../third_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:2542
#12 0x00007ffff4863587 in WebCore::FrameView::paintContents (
    this=0x7ffff0bc2d00, p=0x7fffe343d280, rect=...)
    at ../../third_party/WebKit/Source/WebCore/page/FrameView.cpp:2702
#13 0x00007ffff384b050 in WebKit::WebViewImplContentPainter::paint (
    this=0x7fffe4356d80, context=..., contentRect=...)
    at ../../third_party/WebKit/Source/WebKit/chromium/src/WebViewImpl.cpp:2623
#14 0x00007ffff3b30318 in WebCore::NonCompositedContentHost::paintContents (
    this=0x7ffff0c87600, context=..., clipRect=...)
    at ../../third_party/WebKit/Source/WebCore/platform/graphics/chromium/NonCompositedContentHost.cpp:95
#15 0x00007ffff3bb9970 in WebCore::GraphicsLayer::paintGraphicsLayerContents (
    this=0x7fffe3424000, context=..., clip=...)
    at ../../third_party/WebKit/Source/WebCore/platform/graphics/GraphicsLayer.cpp:272
#16 0x00007ffff3b270b9 in WebCore::GraphicsLayerChromium::paintContents (
    this=0x7fffe3424000, context=..., clip=...)
    at ../../third_party/WebKit/Source/WebCore/platform/graphics/chromium/GraphicsLayerChromium.cpp:681
#17 0x00007ffff3bc06ac in WebCore::ContentLayerPainter::paint (


and since that destroys everything underneath the GraphicsContext the rest of the paint fails.

We need to hold the updater alive across this call somehow, I think. On the plus side, we finally have a fairly reliable test case for compositing-turns-off-inside-paint.

### ja...@chromium.org (2011-09-19)

Patch up: https://bugs.webkit.org/show_bug.cgi?id=68405.  Still working on trying to get a reliable test case for this to use on the bots.

### ja...@chromium.org (2011-09-20)

http://trac.webkit.org/changeset/95506 should be merged to 874.  Can haz merge bits?

### in...@chromium.org (2011-09-20)

We will merge it to 874 for the next beta. this beta already got cut by 7. Thanks a lot James for the lightning fast turnaround on this.

### ja...@chromium.org (2011-09-20)

http://trac.webkit.org/changeset/95552

### in...@chromium.org (2011-09-20)

Thanks James for merging. Closing bug since it does not affect m14.

### in...@chromium.org (2011-09-27)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-09-27)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### sc...@gmail.com (2011-10-19)

@slaweck: thank you! We were already aware of this bug (from crash reports) when you filed this but your repro enabled us to get to the bottom of it. Previously we were struggling. So a $1000 Chromium Security Reward, thanks :D

### sc...@gmail.com (2011-10-28)

Payment in system, can take up to a couple of weeks.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/97092?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/96595, crbug.com/chromium/96711, crbug.com/chromium/98141]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095295)*
