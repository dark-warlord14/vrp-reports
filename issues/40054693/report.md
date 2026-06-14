# Heap-use-after-free in WebCore::GraphicsContext::paintingDisabled

| Field | Value |
|-------|-------|
| **Issue ID** | [40054693](https://issues.chromium.org/issues/40054693) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>SVG |
| **Reporter** | at...@gmail.com |
| **Assignee** | sc...@chromium.org |
| **Created** | 2012-03-08 |
| **Bounty** | $1,000.00 |

## Description

Repro-file as attachment.

**VERSION**  

Chrome Version: ASAn build 19.0.1063.0  

Operating System: Ubuntu 11.04 x86\_64

=================================================================  

==13338== ERROR: AddressSanitizer heap-use-after-free on address 0x7f57a75f86ec at pc 0x7f57b6d0e08a bp 0x7fff8803f000 sp 0x7fff8803eff8  

READ of size 1 at 0x7f57a75f86ec thread T0  

#0 0x7f57b6d0e08a in WebCore::GraphicsContext::paintingDisabled() const ???:0  

#1 0x7f57b6debc73 in WebCore::GraphicsContext::concatCTM(WebCore::AffineTransform const&) ???:0  

#2 0x7f57b85c3018 in WebCore::SVGImageBufferTools::clipToImageBuffer(WebCore::GraphicsContext\*, WebCore::AffineTransform const&, WebCore::FloatRect const&, WTF::OwnPtr[WebCore::ImageBuffer](javascript:void(0);)&) ???:0  

#3 0x7f57b889c8c9 in WebCore::RenderSVGResourceClipper::applyClippingToContext(WebCore::RenderObject\*, WebCore::FloatRect const&, WebCore::FloatRect const&, WebCore::GraphicsContext\*) ???:0  

#4 0x7f57b889c28a in WebCore::RenderSVGResourceClipper::applyResource(WebCore::RenderObject\*, WebCore::RenderStyle\*, WebCore::GraphicsContext\*&, unsigned short) ???:0  

#5 0x7f57b85cb130 in WebCore::SVGRenderSupport::prepareToRenderSVGContent(WebCore::RenderObject\*, WebCore::PaintInfo&) ???:0  

#6 0x7f57b88babff in WebCore::RenderSVGShape::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#7 0x7f57b85c2bff in WebCore::SVGImageBufferTools::renderSubtreeToImageBuffer(WebCore::ImageBuffer\*, WebCore::RenderObject\*, WebCore::AffineTransform const&) ???:0  

#8 0x7f57b889dc07 in WebCore::RenderSVGResourceClipper::drawContentIntoMaskImage(WebCore::ClipperData\*, WebCore::FloatRect const&) ???:0  

#9 0x7f57b889c80c in WebCore::RenderSVGResourceClipper::applyClippingToContext(WebCore::RenderObject\*, WebCore::FloatRect const&, WebCore::FloatRect const&, WebCore::GraphicsContext\*) ???:0  

#10 0x7f57b889c28a in WebCore::RenderSVGResourceClipper::applyResource(WebCore::RenderObject\*, WebCore::RenderStyle\*, WebCore::GraphicsContext\*&, unsigned short) ???:0  

#11 0x7f57b85cb130 in WebCore::SVGRenderSupport::prepareToRenderSVGContent(WebCore::RenderObject\*, WebCore::PaintInfo&) ???:0  

#12 0x7f57b88babff in WebCore::RenderSVGShape::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#13 0x7f57b85c2bff in WebCore::SVGImageBufferTools::renderSubtreeToImageBuffer(WebCore::ImageBuffer\*, WebCore::RenderObject\*, WebCore::AffineTransform const&) ???:0  

#14 0x7f57b889dc07 in WebCore::RenderSVGResourceClipper::drawContentIntoMaskImage(WebCore::ClipperData\*, WebCore::FloatRect const&) ???:0  

#15 0x7f57b889c80c in WebCore::RenderSVGResourceClipper::applyClippingToContext(WebCore::RenderObject\*, WebCore::FloatRect const&, WebCore::FloatRect const&, WebCore::GraphicsContext\*) ???:0  

#16 0x7f57b889c28a in WebCore::RenderSVGResourceClipper::applyResource(WebCore::RenderObject\*, WebCore::RenderStyle\*, WebCore::GraphicsContext\*&, unsigned short) ???:0  

#17 0x7f57b85cb130 in WebCore::SVGRenderSupport::prepareToRenderSVGContent(WebCore::RenderObject\*, WebCore::PaintInfo&) ???:0  

#18 0x7f57b88babff in WebCore::RenderSVGShape::paint(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#19 0x7f57b85c2bff in WebCore::SVGImageBufferTools::renderSubtreeToImageBuffer(WebCore::ImageBuffer\*, WebCore::RenderObject\*, WebCore::AffineTransform const&) ???:0  

.  

.  

.  

#54 0x7f57b487f04a in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) ???:0  

#55 0x7f57b309db87 in ChromeMain ??:0  

#56 0x7f57b309dadb in main ???:0  

#57 0x7f57ac49eeff in \_\_libc\_start\_main /build/buildd/eglibc-2.13/csu/libc-start.c:258  

0x7f57a75f86ec is located -625874310 bytes to the rightASAN:SIGSEGV  

==13338== ERROR: AddressSanitizer crashed on unknown address 0x00003a9c5d73 (pc 0x7f57ba942a9f sp 0x7fff8803cb60 bp 0x00003a9c5d73 T0)  

AddressSanitizer can not provide additional info. ABORTING  

#0 0x7f57ba942a9f in \_\_asan::VSNPrintf(char\*, int, char const\*, \_\_va\_list\_tag\*) /usr/local/google/chrome/src/third\_party/llvm/projects/compiler-rt/lib/asan/asan\_printf.cc:0  

Stats: 4M malloced (7M for red zones) by 24994 calls  

Stats: 0M realloced by 73 calls  

Stats: 2M freed by 12217 calls  

Stats: 0M really freed by 0 calls  

Stats: 44M (11270 full pages) mmaped in 11 calls  

mmaps by size class: 8:32766; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:256; 15:128; 16:64; 17:32;  

mallocs by size class: 8:21617; 9:1648; 10:1098; 11:395; 12:76; 13:34; 14:86; 15:20; 16:18; 17:2;  

frees by size class: 8:9724; 9:1148; 10:934; 11:251; 12:39; 13:18; 14:77; 15:17; 16:9;  

rfrees by size class:  

Stats: malloc large: 2 small slow: 107

## Attachments

- [home-heap-use-after-free-08a.svg](attachments/home-heap-use-after-free-08a.svg) (text/plain; charset=us-ascii, 809 B)
- [117471_asan.txt](attachments/117471_asan.txt) (text/x-c; charset=us-ascii, 21.1 KB)

## Timeline

### kc...@chromium.org (2012-03-09)

Interesting. asan has crashed in the middle of reporting a bug. 
I can see a more usual and complete use-after-free report (attached). 

### in...@chromium.org (2012-03-09)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=24898069

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x7fae3a425eec
Crash State:
  - crash stack -
  WebCore::GraphicsContext::paintingDisabled
  WebCore::GraphicsContext::concatCTM
  - free stack -
  WebCore::ImageBuffer::~ImageBuffer
  WebCore::SVGImageBufferTools::clipToImageBuffer
  

Minimized Testcase (0.56 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv95nZd4zeXXDDc1V69y9uNmMp7V6sHi3X_5NKVSX5tWdECThkCcsS80zMrHEPjRIWGdbTGWMzF0tWtozVQN2V9BKSsvLsT_tDoyWDbTHz9TlfV6T6NVZa22FEymHHq6TcWLn9VLXDpTFjyKR16Zww1PNlNiemw
<svg xmlns="http://www.w3.org/2000/svg">
<defs>
    <clipPath id="clip0">
        <rect width="1" height="1" clip-path="url(#clip)" />
 
    </clipPath>

    <clipPath id="clip2">
        <rect width="100" height="100" clip-path="url(#clip0)"/>
    </clipPath>

    <clipPath id="clip">
        <rect width="1" height="1" clip-path="url(#clip2)"/>
    </clipPath>

    <mask id="mask1" x="0" y="0" width="1" height="1" maskContentUnits="objectBoundingBox">
        <rect width="1" height="1" clip-path="url(#clip)" />
    </mask>
</defs>

<circle r="50" mask="url(#mask1)"/>

### in...@chromium.org (2012-03-09)

Stephen, need help with triage.

### in...@chromium.org (2012-03-09)

tracking bug - https://bugs.webkit.org/show_bug.cgi?id=80669

### sc...@chromium.org (2012-03-09)

It's definitely an SVG issue, and the fix is almost certainly needed in SVG code. Given the circular clip references, I'm not terribly surprised. I'll deal with it after I handle the couple of release blocking bugs I already have (unless someone else gets there first).

### sc...@chromium.org (2012-03-13)

Fixed upstream: http://trac.webkit.org/changeset/110563

I believe this will merge back into previous releases. I'll check now.

### in...@chromium.org (2012-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-14)

Very interesting bug! Thanks for finding it.
$1000 reward.

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

### sc...@gmail.com (2012-03-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-21)

Not a clean merge to M17. We'll put it in M18.

### sc...@gmail.com (2012-03-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-21)

M18: http://trac.webkit.org/changeset/111490

### sc...@gmail.com (2012-03-25)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-27)

[Empty comment from Monorail migration]

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

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

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

This issue was migrated from crbug.com/chromium/117471?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>SVG]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054693)*
