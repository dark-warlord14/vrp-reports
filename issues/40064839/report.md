# SkPaint::SkPaint - crash

| Field | Value |
|-------|-------|
| **Issue ID** | [40064839](https://issues.chromium.org/issues/40064839) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals, Internals>Skia |
| **Reporter** | sl...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2012-08-26 |
| **Bounty** | $1,000.00 |

## Description

Crashes on windows dev 23.0.1243.2 (153013) and canary 23.0.1245.0 (153342).

Repro:
----- crash1.html -----
<style>
@-webkit-keyframes kf0 {
   to {
      -webkit-mask: -webkit-radial-gradient(#000, #000);
   }
}
</style>
<video src="foo">foo</video>
<span style="-webkit-animation: kf0 1s 1s backwards" >
   <iframe  style="-webkit-mask-box-image: -webkit-radial-gradient(#fff, #fff)">
-----------------------

(2df0.e98): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
eax=0027dda8 ebx=01c65738 ecx=3ff00004 edx=00000001 esi=0027eb8c edi=0027ebd4
eip=56ef5104 esp=0027dd8c ebp=0027dd8c iopl=0         nv up ei pl nz na po nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00010202
chrome_56e90000!SkPaint::SkPaint+0x23:
56ef5104 f00fc111        lock xadd dword ptr [ecx],edx ds:0023:3ff00004=????????

ExceptionAddress: 56ef5104 (chrome_56e90000!SkPaint::SkPaint+0x00000023)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000001
   Parameter[1]: 3ff00004
Attempt to write to address 3ff00004

ChildEBP RetAddr  
0027dd8c 576a9507 chrome_56e90000!SkPaint::SkPaint+0x23
0027de0c 57068479 chrome_56e90000!WebCore::OpaqueRegionSkia::popCanvasLayer+0x3a
0027df24 57067bd7 chrome_56e90000!WebCore::RenderLayer::paintLayerContents+0x87d
0027df58 57067a12 chrome_56e90000!WebCore::RenderLayer::paintLayerContentsAndReflection+0x7c
0027e174 570692c8 chrome_56e90000!WebCore::RenderLayer::paintLayer+0x3ba
0027e1b0 570682b8 chrome_56e90000!WebCore::RenderLayer::paintList+0x5e
0027e2e4 57067bd7 chrome_56e90000!WebCore::RenderLayer::paintLayerContents+0x6bc
0027e318 57067a12 chrome_56e90000!WebCore::RenderLayer::paintLayerContentsAndReflection+0x7c
0027e534 570692c8 chrome_56e90000!WebCore::RenderLayer::paintLayer+0x3ba
0027e570 570682b8 chrome_56e90000!WebCore::RenderLayer::paintList+0x5e
0027e6a4 57067bd7 chrome_56e90000!WebCore::RenderLayer::paintLayerContents+0x6bc
0027e6d8 57067a12 chrome_56e90000!WebCore::RenderLayer::paintLayerContentsAndReflection+0x7c
0027e8f4 57067503 chrome_56e90000!WebCore::RenderLayer::paintLayer+0x3ba
0027e96c 57066f1b chrome_56e90000!WebCore::RenderLayer::paint+0x9a
0027e9d4 582615fb chrome_56e90000!WebCore::FrameView::paintContents+0x276
0027ea04 582744ea chrome_56e90000!WebKit::WebViewImpl::paintRootLayer+0x3e
0027ea40 5767fbc2 chrome_56e90000!WebKit::NonCompositedContentHost::paintContents+0x7a
0027ea88 576839f8 chrome_56e90000!WebCore::GraphicsLayer::paintGraphicsLayerContents+0xff
0027ea98 576af5fd chrome_56e90000!WebCore::GraphicsLayerChromium::paint+0x1f
0027ed38 582889df chrome_56e90000!WebCore::OpaqueRectTrackingContentLayerDelegate::paintContents+0x147
0027ed74 579918ce chrome_56e90000!WebKit::WebContentLayerImpl::paintContents+0x48
0027eda4 56f8ed6e chrome_56e90000!WebCore::ContentLayerPainter::paint+0x2c
0027ede4 56ef102f chrome_56e90000!webkit_glue::WebKitPlatformSupportImpl::monotonicallyIncreasingTime+0xe
0027ee1c 56e94940 chrome_56e90000!SkMetaData::setPtr+0x2a
0027ee34 00000000 chrome_56e90000!tcmalloc::ThreadCache::Deallocate+0x30


## Attachments

- [crash1.html](attachments/crash1.html) (text/plain; charset=us-ascii, 279 B)
- [stack1.txt](attachments/stack1.txt) (text/x-c++; charset=us-ascii, 3.3 KB)

## Timeline

### sc...@gmail.com (2012-08-26)

[Empty comment from Monorail migration]

### pa...@google.com (2012-08-27)

Easy reproducibility on Linux, stable and ToT. Thanks Slaweck!

Weirdly, Cluster Fuzz says it's unreproducible. That's not true, of course. inferno, any ideas as to why?

Depending on what field of SkPaint we are writing, it looks like it might be a small write, or it could be as big as an SkScalar. reed or danakj, any clues?

### da...@chromium.org (2012-08-27)

[Empty comment from Monorail migration]

### da...@chromium.org (2012-08-27)

What are you doing to reproduce on linux? What command line flags?

### pa...@google.com (2012-08-27)

I don't set any command line flags. (At least there are none explicitly entered by me.) Release+ASAN ToT, Debug ToT, and 21 stable all crash immediately and I don't have to tweak anything. FWIW, I cannot repro the problem on 21 for OS X. It does repro on ToT on OS X though. On that build, I get an ASSERT on line 91 of WebCore/platform/graphics/GraphicsContext.cpp (~GraphicsContext).

### da...@chromium.org (2012-08-27)

Ok sounds like the GraphicsContext stack is being popped beyond empty. A non-aura linux build is able to repro the crash for me also (though run-webkit-tests does not either).

### da...@chromium.org (2012-08-27)

This change prevents the crash, the WebCore bug should be tracked down also though.

### da...@chromium.org (2012-08-28)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-28)

http://trac.webkit.org/changeset/126901

### in...@chromium.org (2012-08-28)

[Empty comment from Monorail migration]

### da...@chromium.org (2012-08-28)

This is the underlying issue in WebCore that causes the crash.

### in...@chromium.org (2012-08-28)

Lets reopen this then. m22 needs the fix for the underlying cause.

### bu...@chromium.org (2012-08-28)

https://bugs.webkit.org/show_bug.cgi?id=95240

### da...@chromium.org (2012-08-29)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-31)

We need to merge the good band-aid to m22. Talked to Dana. the long-term fix will take more time and better to just track it as a functional bug.

### sc...@gmail.com (2012-09-05)

M22: http://trac.webkit.org/changeset/127638

### sc...@gmail.com (2012-09-25)

@slaweck: nice discovery! And a $1000 reward.

### sc...@gmail.com (2012-10-11)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/144899?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Skia]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064839)*
