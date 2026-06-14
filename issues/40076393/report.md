# Heap-use-after-free in WebCore::RenderLayerBacking::paintIntoLayer

| Field | Value |
|-------|-------|
| **Issue ID** | [40076393](https://issues.chromium.org/issues/40076393) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Internals>Media>Video, Internals>Skia |
| **Reporter** | at...@gmail.com |
| **Assignee** | en...@chromium.org |
| **Created** | 2012-10-04 |
| **Bounty** | $1,000.00 |

## Description

Steps to reproduce the problem:
Open attached file with Chrome, might need few refresh. This issue needs page-heap /full to reproduce. This issue didn't reproduce on Ubuntu 12.04 x86_64 and ASAN Chromium 24.0.1287.0 (Developer Build 160116)

What is the expected behavior?

What went wrong?

Windbg report from dump-file:

FAULTING_IP: 
chrome_5d780000!WebCore::RenderLayerBacking::paintIntoLayer+c1 [c:\b\build\slave\win\build\src\third_party\webkit\source\webcore\rendering\renderlayerbacking.cpp @ 1425]
5e23d7e1 8b7f04          mov     edi,dword ptr [edi+4]

EXCEPTION_RECORD:  ffffffff -- (.exr 0xffffffffffffffff)
.exr 0xffffffffffffffff
ExceptionAddress: 5e23d7e1 (chrome_5d780000!WebCore::RenderLayerBacking::paintIntoLayer+0x000000c1)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000000
   Parameter[1]: 12005fbc
Attempt to read from address 12005fbc

STACK_TEXT:  
0040e8b0 5e23da4b 10adc444 0040e9d0 00000007 chrome_5d780000!WebCore::RenderLayerBacking::paintIntoLayer+0xc1 [c:\b\build\slave\win\build\src\third_party\webkit\source\webcore\rendering\renderlayerbacking.cpp @ 1425]
0040e900 5dfa8ef2 12003e10 0040e9d0 00000007 chrome_5d780000!WebCore::RenderLayerBacking::paintContents+0x1fb [c:\b\build\slave\win\build\src\third_party\webkit\source\webcore\rendering\renderlayerbacking.cpp @ 1464]
0040e950 5dfacd40 0040e9d0 0040e98c 0040ec10 chrome_5d780000!WebCore::GraphicsLayer::paintGraphicsLayerContents+0xc6 [c:\b\build\slave\win\build\src\third_party\webkit\source\webcore\platform\graphics\graphicslayer.cpp @ 322]
0040e960 5dfdb334 0040e9d0 0040e98c 5f91805c chrome_5d780000!WebCore::GraphicsLayerChromium::paint+0x1f [c:\b\build\slave\win\build\src\third_party\webkit\source\webcore\platform\graphics\chromium\graphicslayerchromium.cpp @ 867]
0040ec10 5f1b781b 130d0ea0 0040ec3c 0040ec4c chrome_5d780000!WebCore::OpaqueRectTrackingContentLayerDelegate::paintContents+0x15d [c:\b\build\slave\win\build\src\third_party\webkit\source\webcore\platform\graphics\chromium\opaquerecttrackingcontentlayerdelegate.cpp @ 71]
0040ec5c 5f1ba421 130d0ea0 0040ed90 0040ed80 chrome_5d780000!WebKit::WebContentLayerImpl::paintContents+0x3e [c:\b\build\slave\win\build\src\webkit\compositor_bindings\webcontentlayerimpl.cpp @ 77]
0040ec8c 5f1d9e6b 130d0ea0 0040ed90 0040ed80 chrome_5d780000!cc::ContentLayerPainter::paint+0x24 [c:\b\build\slave\win\build\src\cc\contentlayerchromium.cpp @ 37]
0040edd0 5f1c4616 130d0ea0 0040efd0 3f800000 chrome_5d780000!cc::CanvasLayerTextureUpdater::paintContents+0x249 [c:\b\build\slave\win\build\src\cc\canvaslayertextureupdater.cpp @ 59]
0040ee04 5f1c350a 0040efd0 0040eee4 3f800000 chrome_5d780000!cc::BitmapCanvasLayerTextureUpdater::prepareToUpdate+0x7b [c:\b\build\slave\win\build\src\cc\bitmapcanvaslayertextureupdater.cpp @ 67]
0040ef9c 5f1c397b 0040efd0 00000000 00000000 chrome_5d780000!cc::TiledLayerChromium::updateTileTextures+0x156 [c:\b\build\slave\win\build\src\cc\tiledlayerchromium.cpp @ 484]
.
.
.

Did this work before? N/A 

Chrome version: Chrome 24.0.1285.0 (159856) canary
OS Version: 7 x64

UserAgent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1

## Attachments

- [Canvas-repro-10.html](attachments/Canvas-repro-10.html) (text/html; charset=us-ascii, 1.2 KB)
- [Invalid_pointer_read_paintIntoLayer.html](attachments/Invalid_pointer_read_paintIntoLayer.html) (text/html; charset=us-ascii, 1.2 KB)

## Timeline

### in...@chromium.org (2012-10-04)

[Empty comment from Monorail migration]

### at...@gmail.com (2012-10-04)

This issue seems to affect 22.0.1229.79 (Official Build 158531) m on Windows 7 x64

This issue is reproducible without page-heap but it is little harder. I modified the testcase to reproduce automatically on my laptop, I haven't verified it with other machines so I don't know if the timeouts need adjusting on other machines. I attached the modified testcase. 

Interesting thing is that with the new testcase and without page-heap the issue appears as null+offset read with Canary-chrome and with stable chrome windbg says the following:

FAULTING_IP: 
+313827
6f2e63f4 ??              ???

EXCEPTION_RECORD:  ffffffff -- (.exr 0xffffffffffffffff)
ExceptionAddress: 6f2e63f4
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000008
   Parameter[1]: 6f2e63f4
Attempt to execute non-executable address 6f2e63f4

FOLLOWUP_IP: 
chrome_63e30000!RelaunchChromeBrowserWithNewCommandLineIfNeeded+313827
64693ed7 5d              pop     ebp

On stable release with page-heap I get:

FAULTING_IP: 
chrome_57840000!RelaunchChromeBrowserWithNewCommandLineIfNeeded+51efdd
582af68d 8b4604          mov     eax,dword ptr [esi+4]

EXCEPTION_RECORD:  ffffffff -- (.exr 0xffffffffffffffff)
ExceptionAddress: 582af68d (chrome_57840000!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0x0051efdd)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000000
   Parameter[1]: 0b124fc4
Attempt to read from address 0b124fc4

FOLLOWUP_IP: 
chrome_57840000!RelaunchChromeBrowserWithNewCommandLineIfNeeded+51efdd
582af68d 8b4604          mov     eax,dword ptr [esi+4]


Symbol server doesn't give symbols to stable chrome so the stack trace and followup_ip doesn't have much useful information.


### pa...@chromium.org (2012-10-04)

Good News, Everybody. I can reproduce attekett's second repro in #2 on Linux, 22 beta. In a Debug build, I hit this ASSERT:

ASSERTION FAILED: !renderer()->frame()->page() || !renderer()->frame()->page()->isPainting()
../../third_party/WebKit/Source/WebCore/rendering/RenderLayerBacking.cpp(1516) : virtual void WebCore::RenderLayerBacking::verifyNotPainting()

1513 #ifndef NDEBUG
1514 void RenderLayerBacking::verifyNotPainting()
1515 {
1516     ASSERT(!renderer()->frame()->page() || !renderer()->frame()->page()->isPainting());
1517 }
1518 #endif

Weirdly, an ASAN build of 23 cannot repro the bug. With an abundance of caution, calling it Pri-1/SecSeverity-High based on attekett's observation of a wild EIP. We might decide later it's really Pri-2/Medium if it's really only a limited read AV or EIP is not attacker-controllable, but...

Ccing fsamuel since they own that ASSERT.

ClusterFuzz report and WebKit upstream coming soon...

### pa...@chromium.org (2012-10-04)

Upstreamed: https://bugs.webkit.org/show_bug.cgi?id=98449

### pa...@google.com (2012-10-04)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=120559799

Uploader: palmer@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f95d06a3888
Crash State:
  - crash stack -
  WebCore::RenderLayerBacking::paintIntoLayer
  WebCore::RenderLayerBacking::paintContents
  - free stack -
  WebCore::RenderLayer::clearBacking
  WebCore::RenderLayerCompositor::updateBacking
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=150627:150709

Minimized Testcase (1.09 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97TFmfztNhM34wnfY2applm9ruNEroGuSgEyj-zb4IRBrQI1n3XcfZHaZFkPIASHOH0aCnaKt6BKe3-JLaHlmftzyGJIQ6xjjx1I-sp25VzcchafwCBb0Cs1e1b9P_uwPJhKWColUZXTjs0ZwqPhHePGSj1NnLErbD5ZBcviTJ-fm--AeY

### pa...@chromium.org (2012-10-09)

[Empty comment from Monorail migration]

### pa...@chromium.org (2012-10-09)

The repros from http://code.google.com/p/chromium/issues/detail?id=154348 are more reliable (cross-platform, no PageHeap needed), and I think they are probably the same bug. Mike, perhaps a Skia issue?

### [Deleted User] (2012-10-09)

I am unable to read http://code.google.com/p/chromium/issues/detail?id=154348 do I need to be added to the cc?

### gl...@chromium.org (2012-10-09)

[Empty comment from Monorail migration]

### ju...@chromium.org (2012-10-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-10-16)

There are several media patches in the regression range. ccing a couple of folks to triage.

### sc...@chromium.org (2012-10-17)

+jamesr, enne for compositing knowledge

If the clusterfuzz report in #5 is to be believed this appears to be a use-after-free with a compositor backing texture.

RenderLayerBacking.cpp @ WK r130391:
   1400 void RenderLayerBacking::paintIntoLayer(RenderLayer* rootLayer, GraphicsContext* context,
   1401                     const IntRect& paintDirtyRect, // In the coords of rootLayer.
   1402                     PaintBehavior paintBehavior, GraphicsLayerPaintingPhase paintingPhase,
   1403                     RenderObject* paintingRoot)
   1404 {
   1405     if (paintsIntoWindow() || paintsIntoCompositedAncestor()) {
   1406         ASSERT_NOT_REACHED();
   1407         return;
   1408     }
   1409 
   1410     FontCachePurgePreventer fontCachePurgePreventer;
   1411     
   1412     RenderLayer::PaintLayerFlags paintFlags = 0;
   1413     if (paintingPhase & GraphicsLayerPaintBackground)
   1414         paintFlags |= RenderLayer::PaintLayerPaintingCompositingBackgroundPhase;
   1415     if (paintingPhase & GraphicsLayerPaintForeground)
   1416         paintFlags |= RenderLayer::PaintLayerPaintingCompositingForegroundPhase;
   1417     if (paintingPhase & GraphicsLayerPaintMask)
   1418         paintFlags |= RenderLayer::PaintLayerPaintingCompositingMaskPhase;
   1419     if (paintingPhase & GraphicsLayerPaintOverflowContents)
   1420         paintFlags |= RenderLayer::PaintLayerPaintingOverflowContents;
   1421     
   1422     // FIXME: GraphicsLayers need a way to split for RenderRegions.
   1423     m_owningLayer->paintLayerContents(rootLayer, context, paintDirtyRect, LayoutSize(), paintBehavior, paintingRoot, 0, 0, paintFlags);
   1424 
   1425     if (m_owningLayer->containsDirtyOverlayScrollbars())
   1426         m_owningLayer->paintOverlayScrollbars(context, paintDirtyRect, paintBehavior, paintingRoot);
   1427 
   1428     ASSERT(!m_owningLayer->m_usedTransparency);
   1429 }

The report says the backing layer is freed due to the call on line 1423. The UAF occurs on line 1425, which looks a bit suspect.

None of the Chromium changes seem to line up (mostly audio-related changes, nothing to do w/ rendering).

The only potential WebKit change I can spot is http://trac.webkit.org/changeset/125052 ... but it uses the poster attribute which the clusterfuzz test cases doesn't use.

### in...@chromium.org (2012-10-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-10-23)

Adrienne, can you please help to take a look.

### en...@chromium.org (2012-10-24)

Stack trace of ASAN reduction from ToT Linux Debug, running with --ignore-gpu-blacklist --no-sandbox

	base::debug::StackTrace::StackTrace() [0x7ffc2111c69e]
	base::(anonymous namespace)::StackDumpSignalHandler() [0x7ffc21196c44]
	0x7ffc11f9e4a0
	WebCore::RenderLayerBacking::verifyNotPainting() [0x7ffc1d1f3256]
	WebCore::GraphicsLayer::willBeDestroyed() [0x7ffc1d9c2983]
	WebCore::GraphicsLayerChromium::willBeDestroyed() [0x7ffc1d9ec494]
	WebCore::GraphicsLayerChromium::~GraphicsLayerChromium() [0x7ffc1d9ec330]
	WebCore::GraphicsLayerChromium::~GraphicsLayerChromium() [0x7ffc1d9ec259]
	WTF::deleteOwnedPtr<>() [0x7ffc1cc4da1e]
	WTF::OwnPtr<>::clear() [0x7ffc1cc56567]
	WTF::OwnPtr<>::operator=() [0x7ffc1cc56229]
	WebCore::RenderLayerBacking::destroyGraphicsLayers() [0x7ffc1d1ec899]
	WebCore::RenderLayerBacking::~RenderLayerBacking() [0x7ffc1d1ebb94]
	WebCore::RenderLayerBacking::~RenderLayerBacking() [0x7ffc1d1ebae9]
	WTF::deleteOwnedPtr<>() [0x7ffc1d1e586e]
	WTF::OwnPtr<>::clear() [0x7ffc1d1e2a27]
	WebCore::RenderLayer::clearBacking() [0x7ffc1d1c62da]
	WebCore::RenderLayerCompositor::updateBacking() [0x7ffc1d1faf13]
	WebCore::RenderLayerCompositor::updateLayerCompositingState() [0x7ffc1d1fb373]
	WebCore::RenderLayer::contentChanged() [0x7ffc1d1c63f8]
	WebCore::RenderBoxModelObject::contentChanged() [0x7ffc1d1532b6]
	WebCore::RenderVideo::updatePlayer() [0x7ffc1d2c107b]
	WebCore::RenderVideo::paintReplaced() [0x7ffc1d2c0d6c]
	WebCore::RenderReplaced::paint() [0x7ffc1d262f99]
	WebCore::RenderImage::paint() [0x7ffc1d1b635a]
	WebCore::RenderLayer::paintLayerContents() [0x7ffc1d1d6949]
	WebCore::RenderLayerBacking::paintIntoLayer() [0x7ffc1d1f286d]
	WebCore::RenderLayerBacking::paintContents() [0x7ffc1d1f2b63]
	WebCore::GraphicsLayer::paintGraphicsLayerContents() [0x7ffc1d9c36b0]
	WebCore::GraphicsLayerChromium::paint() [0x7ffc1d9efeb6]
	WebCore::GraphicsLayerChromium::paint() [0x7ffc1d9efef7]

I think this is identical to https://bugs.webkit.org/show_bug.cgi?id=100265.  If I apply that patch, I can't repro this anymore.

### bu...@chromium.org (2012-10-24)

https://bugs.webkit.org/show_bug.cgi?id=100265
http://trac.webkit.org/changeset/132398

### fi...@chromium.org (2012-10-24)

@enne: I'm really happy for you, and Imma let you finish crediting me with a fix for this security bug, but I'm horrified at the connection.

@security-folk: this bug is marked m22; anyone want to take a crack at at least backporting the fix to m23?  (note that the backport should just be deleting the line http://trac.webkit.org/browser/branches/chromium/1271/Source/WebCore/rendering/RenderVideo.cpp#L204 - the rest of the patch is Debug-only defensiveness)

### in...@chromium.org (2012-10-25)

Thanks for the fix. Chris will merge the fix probably to the last m23 beta.

### cl...@chromium.org (2012-10-25)

ClusterFuzz has detected this issue as fixed in range 163899:163922.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=120559799

Uploader: palmer@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f95d06a3888
Crash State:
  - crash stack -
  WebCore::RenderLayerBacking::paintIntoLayer
  WebCore::RenderLayerBacking::paintContents
  - free stack -
  WebCore::RenderLayer::clearBacking
  WebCore::RenderLayerCompositor::updateBacking
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=150627:150709
Fixed: https://cluster-fuzz.appspot.com/revisions?range=163899:163922

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97TFmfztNhM34wnfY2applm9ruNEroGuSgEyj-zb4IRBrQI1n3XcfZHaZFkPIASHOH0aCnaKt6BKe3-JLaHlmftzyGJIQ6xjjx1I-sp25VzcchafwCBb0Cs1e1b9P_uwPJhKWColUZXTjs0ZwqPhHePGSj1NnLErbD5ZBcviTJ-fm--AeY

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-10-29)

M23: http://trac.webkit.org/changeset/132817

### sc...@gmail.com (2012-10-29)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-10-29)

$1000 !!!!

### [Deleted User] (2012-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2012-11-16)

Just wanted to check if the fix for this is released for M24 (24.0.1312.14)?

### fi...@chromium.org (2012-11-16)

@vikasmarwaha: m24 branched webkit at 132834 so it contains the fix (which was webkit 132398).

### sc...@gmail.com (2012-12-14)

Payment in system as part of $3000 batch.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-05)

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/154055?no_tracker_redirect=1

[Multiple monorail components: Blink, Internals>Media>Video, Internals>Skia]
[Monorail mergedwith: crbug.com/chromium/154348]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076393)*
