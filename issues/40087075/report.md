# height of <rect> - integer overflow(?)

| Field | Value |
|-------|-------|
| **Issue ID** | [40087075](https://issues.chromium.org/issues/40087075) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | sl...@gmail.com |
| **Assignee** | wj...@chromium.org |
| **Created** | 2011-01-20 |
| **Bounty** | $1,000.00 |

## Description

It's related to https://crbug.com/chromium/64184 but use different way to set 'height'.
I filled new bug report becouse it was(?) fixed and this can be something new.
Crashes on linux 32-bit dev [10.0.634.0 (Build 70875)]

Repro file:
----- crash1.xml -----
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <script type="text/ecmascript"><![CDATA[ 
            function main(){
                obj = window.document.childNodes[0].childNodes[3].childNodes[1].viewBox.baseVal
                obj.height = 3.41e38
            }
    
            window.onload = main;
        ]]></script>
    </head>
    <body>
        <svg version="1.1" xmlns="http://www.w3.org/2000/svg" >
            <rect height="10%" width="100"></rect>
        </svg>
    </body>
</html>
----------------------

Program received signal SIGSEGV, Segmentation fault.
[Switching to Thread 0xb1cddb70 (LWP 3815)]
sk_memset32_SSE2 (dst=0xaa7b5ff0, value=4278190080, count=700) at third_party/skia/src/opts/SkUtils_opts_SSE2.cpp:66
66              _mm_store_si128(d++, value_wide);


#0  sk_memset32_SSE2 (dst=0xaa7b5ff0, value=4278190080, count=700) at third_party/skia/src/opts/SkUtils_opts_SSE2.cpp:66
#1  0x00c4cf32 in Color32_SSE2 (dst=0xaa7a6cb0, src=0xaa7a6cb0, count=16284, color=4278190080) at third_party/skia/src/opts/SkBlitRow_opts_SSE2.cpp:333
#2  0x00c3c6e5 in SkARGB32_Blitter::blitH (this=0xb1cdb4dc, x=108, y=368, width=16284) at third_party/skia/src/core/SkBlitter_ARGB32.cpp:100
#3  0x00c1ad62 in walk_edges (prevHead=<value optimized out>, fillType=<value optimized out>, blitter=0xb1cdb4dc, start_y=8, stop_y=390, proc=0) at third_party/skia/src/core/SkScan_Path.cpp:165
#4  0x00c1b382 in sk_fill_path (path=..., clipRect=0x3a21388, blitter=0xb1cdb4dc, start_y=<value optimized out>, stop_y=<value optimized out>, shiftEdgesUp=<value optimized out>, clipRgn=...) at third_party/skia/src/core/SkScan_Path.cpp:557
#5  0x00c1b53b in SkScan::FillPath (path=..., clip=..., blitter=0xb1cdb4dc) at third_party/skia/src/core/SkScan_Path.cpp:641
#6  0x00c184eb in SkScan::AntiFillPath (path=..., clip=..., blitter=0xb1cdb4dc) at third_party/skia/src/core/SkScan_AntiPath.cpp:387
#7  0x00c0227a in SkDraw::drawPath (this=0xb1cdb718, origSrcPath=..., paint=..., prePathMatrix=0x0, pathIsMutable=false) at third_party/skia/src/core/SkDraw.cpp:917
#8  0x00bfe41a in SkDevice::drawPath (this=0x3897000, draw=..., path=..., paint=..., prePathMatrix=0x0, pathIsMutable=<value optimized out>) at third_party/skia/src/core/SkDevice.cpp:111
#9  0x00bfcc62 in SkCanvas::drawPath (this=0x38e6280, path=..., paint=...) at third_party/skia/src/core/SkCanvas.cpp:1168
#10 0x016c7b68 in WebCore::GraphicsContext::fillPath (this=0xb1cdc9d4, pathToFill=...) at third_party/WebKit/Source/WebCore/platform/graphics/skia/GraphicsContextSkia.cpp:749
#11 0x01c1293e in WebCore::RenderSVGResourceSolidColor::postApplyResource (this=0x38b4510, context=@0xff000000, resourceMode=2, path=0xaa7b5ff0) at third_party/WebKit/Source/WebCore/rendering/RenderSVGResourceSolidColor.cpp:85
#12 0x01cca3fd in WebCore::RenderSVGPath::fillAndStrokePath (this=0x3a8a614, context=0xb1cdc9d4) at third_party/WebKit/Source/WebCore/rendering/svg/RenderSVGPath.cpp:161
#13 0x01ccac8a in WebCore::RenderSVGPath::paint (this=0x3a8a614, paintInfo=...) at third_party/WebKit/Source/WebCore/rendering/svg/RenderSVGPath.cpp:224
#14 0x01a7035d in WebCore::RenderBox::paint (this=0x3a8a550, paintInfo=..., tx=<value optimized out>, ty=0) at third_party/WebKit/Source/WebCore/rendering/RenderBox.cpp:755
#15 0x01cdc8d2 in WebCore::RenderSVGRoot::paint (this=0x3a8a550, paintInfo=..., parentX=8, parentY=8) at third_party/WebKit/Source/WebCore/rendering/RenderSVGRoot.cpp:184
#16 0x01a36c44 in WebCore::InlineBox::paint (this=0x3a8a744, paintInfo=..., tx=8, ty=8) at third_party/WebKit/Source/WebCore/rendering/InlineBox.cpp:184
#17 0x01a3a837 in WebCore::InlineFlowBox::paint (this=0x3a8a768, paintInfo=..., tx=8, ty=8) at third_party/WebKit/Source/WebCore/rendering/InlineFlowBox.cpp:982
#18 0x01b08b40 in WebCore::RootInlineBox::paint (this=0x3a8a768, paintInfo=..., tx=8, ty=8) at third_party/WebKit/Source/WebCore/rendering/RootInlineBox.cpp:180
#19 0x01ab2751 in WebCore::RenderLineBoxList::paint (this=0x3a8a544, renderer=0x3a8a4e0, paintInfo=..., tx=8, ty=8) at third_party/WebKit/Source/WebCore/rendering/RenderLineBoxList.cpp:256
#20 0x01a4c6f9 in WebCore::RenderBlock::paintContents (this=0x3a8a4e0, paintInfo=..., tx=8, ty=8) at third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:2324
#21 0x01a5c565 in WebCore::RenderBlock::paintObject (this=0x3a8a4e0, paintInfo=..., tx=8, ty=8) at third_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:2434
[...]

Dump of assembler code for function _Z16sk_memset32_SSE2Pjji:
   0x00c4d5f0 <+0>: push   %ebp
   0x00c4d5f1 <+1>: mov    %esp,%ebp
   0x00c4d5f3 <+3>: sub    $0x4,%esp
   0x00c4d5f6 <+6>: mov    0x10(%ebp),%eax
   0x00c4d5f9 <+9>: mov    0x8(%ebp),%edx
   0x00c4d5fc <+12>:    mov    0xc(%ebp),%ecx
   0x00c4d5ff <+15>:    cmp    $0xf,%eax
   0x00c4d602 <+18>:    jle    0xc4d64e <_Z16sk_memset32_SSE2Pjji+94>
   0x00c4d604 <+20>:    test   $0xf,%dl
   0x00c4d607 <+23>:    je     0xc4d622 <_Z16sk_memset32_SSE2Pjji+50>
   0x00c4d609 <+25>:    lea    0x0(%esi,%eiz,1),%esi
   0x00c4d610 <+32>:    mov    %ecx,(%edx)
   0x00c4d612 <+34>:    add    $0x4,%edx
   0x00c4d615 <+37>:    sub    $0x1,%eax
   0x00c4d618 <+40>:    test   $0xf,%dl
   0x00c4d61b <+43>:    jne    0xc4d610 <_Z16sk_memset32_SSE2Pjji+32>
   0x00c4d61d <+45>:    cmp    $0xf,%eax
   0x00c4d620 <+48>:    jle    0xc4d64e <_Z16sk_memset32_SSE2Pjji+94>
   0x00c4d622 <+50>:    mov    %ecx,-0x4(%ebp)
   0x00c4d625 <+53>:    movd   -0x4(%ebp),%xmm1
   0x00c4d62a <+58>:    pshufd $0x0,%xmm1,%xmm0
   0x00c4d62f <+63>:    nop
   0x00c4d630 <+64>:    sub    $0x10,%eax
   0x00c4d633 <+67>:    movdqa %xmm0,(%edx)
=> 0x00c4d637 <+71>:    movdqa %xmm0,0x10(%edx)
   0x00c4d63c <+76>:    movdqa %xmm0,0x20(%edx)


eax            0x2bc    700
ecx            0xff000000   -16777216
edx            0xaa7b5ff0   -1434755088
ebx            0x2f4352c    49558828
esp            0xb1cdad44   0xb1cdad44
ebp            0xb1cdad48   0xb1cdad48
esi            0x3f9c   16284
edi            0xaa7a6cb0   -1434817360
eip            0xc4d637 0xc4d637 <sk_memset32_SSE2(unsigned int*, unsigned int, int)+71>
eflags         0x210202 [ IF RF ID ]
cs             0x73 115
ss             0x7b 123
ds             0x7b 123
es             0x7b 123
fs             0x0  0
gs             0x33 51
st0            0    (raw 0x00000000000000000000)
st1            1    (raw 0x3fff8000000000000000)
st2            0    (raw 0x00000000000000000000)
st3            0    (raw 0x00000000000000000000)
st4            8    (raw 0x40028000000000000000)
st5            8    (raw 0x40028000000000000000)
st6            8    (raw 0x40028000000000000000)
st7            8    (raw 0x40028000000000000000)
fctrl          0x37f    895
fstat          0x402f   16431
ftag           0xffff   65535
fiseg          0x0  0
fioff          0x0  0
foseg          0x0  0
fooff          0x0  0
fop            0x0  0
xmm0           {v4_float = {0x0, 0x0, 0x0, 0x0}, v2_double = {0x8000000000000000, 0x8000000000000000}, v16_int8 = {0x0, 0x0, 0x0, 0xff, 0x0, 0x0, 0x0, 0xff, 0x0, 0x0, 0x0, 0xff, 0x0, 0x0, 0x0, 0xff}, v8_int16 = {0x0, 0xff00, 0x0, 0xff00, 0x0, 0xff00, 0x0, 0xff00}, v4_int32 = {0xff000000, 0xff000000, 0xff000000, 0xff000000}, v2_int64 = {0xff000000ff000000, 0xff000000ff000000}, uint128 = 0xff000000ff000000ff000000ff000000}
xmm1           {v4_float = {0x0, 0x0, 0x0, 0x0}, v2_double = {0x0, 0x0}, v16_int8 = {0x0, 0x0, 0x0, 0xff, 0x0 <repeats 12 times>}, v8_int16 = {0x0, 0xff00, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0}, v4_int32 = {0xff000000, 0x0, 0x0, 0x0}, v2_int64 = {0xff000000, 0x0}, uint128 = 0x000000000000000000000000ff000000}
xmm2           {v4_float = {0x0, 0x0, 0x0, 0x0}, v2_double = {0x0, 0x0}, v16_int8 = {0xff, 0x0, 0xff, 0x0, 0xff, 0x0, 0xff, 0x0, 0xff, 0x0, 0xff, 0x0, 0xff, 0x0, 0xff, 0x0}, v8_int16 = {0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff}, v4_int32 = {0xff00ff, 0xff00ff, 0xff00ff, 0xff00ff}, v2_int64 = {0xff00ff00ff00ff, 0xff00ff00ff00ff}, uint128 = 0x00ff00ff00ff00ff00ff00ff00ff00ff}
xmm3           {v4_float = {0x0, 0x0, 0x0, 0x0}, v2_double = {0x8000000000000000, 0x8000000000000000}, v16_int8 = {0x79, 0x79, 0x79, 0xff, 0x79, 0x79, 0x79, 0xff, 0x79, 0x79, 0x79, 0xff, 0x79, 0x79, 0x79, 0xff}, v8_int16 = {0x7979, 0xff79, 0x7979, 0xff79, 0x7979, 0xff79, 0x7979, 0xff79}, v4_int32 = {0xff797979, 0xff797979, 0xff797979, 0xff797979}, v2_int64 = {0xff797979ff797979, 0xff797979ff797979}, uint128 = 0xff797979ff797979ff797979ff797979}
xmm4           {v4_float = {0x0, 0x0, 0x0, 0x0}, v2_double = {0x0, 0x0}, v16_int8 = {0xff, 0x0, 0xff, 0x0, 0xff, 0x0, 0xff, 0x0, 0xff, 0x0, 0xff, 0x0, 0xff, 0x0, 0xff, 0x0}, v8_int16 = {0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff}, v4_int32 = {0xff00ff, 0xff00ff, 0xff00ff, 0xff00ff}, v2_int64 = {0xff00ff00ff00ff, 0xff00ff00ff00ff}, uint128 = 0x00ff00ff00ff00ff00ff00ff00ff00ff}
xmm5           {v4_float = {0x0, 0x0, 0x0, 0x0}, v2_double = {0x0, 0x0}, v16_int8 = {0x0, 0x1, 0x0, 0x1, 0x0, 0x1, 0x0, 0x1, 0x0, 0x1, 0x0, 0x1, 0x0, 0x1, 0x0, 0x1}, v8_int16 = {0x100, 0x100, 0x100, 0x100, 0x100, 0x100, 0x100, 0x100}, v4_int32 = {0x1000100, 0x1000100, 0x1000100, 0x1000100}, v2_int64 = {0x100010001000100, 0x100010001000100}, uint128 = 0x01000100010001000100010001000100}
xmm6           {v4_float = {0x0, 0x0, 0x0, 0x0}, v2_double = {0x0, 0x0}, v16_int8 = {0x1, 0x0, 0x1, 0x0, 0x1, 0x0, 0x1, 0x0, 0x1, 0x0, 0x1, 0x0, 0x1, 0x0, 0x1, 0x0}, v8_int16 = {0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1}, v4_int32 = {0x10001, 0x10001, 0x10001, 0x10001}, v2_int64 = {0x1000100010001, 0x1000100010001}, uint128 = 0x00010001000100010001000100010001}
xmm7           {v4_float = {0x0, 0x0, 0x0, 0x0}, v2_double = {0x0, 0x0}, v16_int8 = {0x0 <repeats 16 times>}, v8_int16 = {0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0}, v4_int32 = {0x0, 0x0, 0x0, 0x0}, v2_int64 = {0x0, 0x0}, uint128 = 0x00000000000000000000000000000000}
mxcsr          0x1fa0   [ PE IM DM ZM OM UM PM ]
mm0            {uint64 = 0x0, v2_int32 = {0x0, 0x0}, v4_int16 = {0x0, 0x0, 0x0, 0x0}, v8_int8 = {0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0}}
mm1            {uint64 = 0x8000000000000000, v2_int32 = {0x0, 0x80000000}, v4_int16 = {0x0, 0x0, 0x0, 0x8000}, v8_int8 = {0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x80}}
mm2            {uint64 = 0x0, v2_int32 = {0x0, 0x0}, v4_int16 = {0x0, 0x0, 0x0, 0x0}, v8_int8 = {0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0}}
mm3            {uint64 = 0x0, v2_int32 = {0x0, 0x0}, v4_int16 = {0x0, 0x0, 0x0, 0x0}, v8_int8 = {0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0}}
mm4            {uint64 = 0x8000000000000000, v2_int32 = {0x0, 0x80000000}, v4_int16 = {0x0, 0x0, 0x0, 0x8000}, v8_int8 = {0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x80}}
mm5            {uint64 = 0x8000000000000000, v2_int32 = {0x0, 0x80000000}, v4_int16 = {0x0, 0x0, 0x0, 0x8000}, v8_int8 = {0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x80}}
mm6            {uint64 = 0x8000000000000000, v2_int32 = {0x0, 0x80000000}, v4_int16 = {0x0, 0x0, 0x0, 0x8000}, v8_int8 = {0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x80}}
mm7            {uint64 = 0x8000000000000000, v2_int32 = {0x0, 0x80000000}, v4_int16 = {0x0, 0x0, 0x0, 0x8000}, v8_int8 = {0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x80}}


(Full backtrace attached - bt1.txt)

## Attachments

- [bt1.txt](attachments/bt1.txt) (text/x-c++; charset=us-ascii, 30.7 KB)
- [crash1.xml](attachments/crash1.xml) (text/html; charset=us-ascii, 511 B)
- [Cr70244.patch](attachments/Cr70244.patch) (text/x-diff; charset=us-ascii, 1.9 KB)

## Timeline

### in...@chromium.org (2011-01-20)

This is bad, write on a non null address. reproduces easily on trunk and canary. does not reproduce on v8 stable. looks like a recent skia regression or another svg issue.

James, can you please take a look.

### wj...@chromium.org (2011-01-20)

OK, will do.

### bu...@chromium.org (2011-01-20)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=71988

------------------------------------------------------------------------
r71988 | estade@chromium.org | Thu Jan 20 12:02:27 PST 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/gtk/status_bubble_gtk.cc?r1=71988&r2=71987&pathrev=71988

[gtk] un-break status bubble.

broken in r71858.

BUG=70244
TEST=manual (in and out of --kiosk)

Review URL: http://codereview.chromium.org/6343003
------------------------------------------------------------------------

### sc...@gmail.com (2011-01-22)

Will we get a fix in before the M10 branch point?

### wj...@chromium.org (2011-01-24)

I am looking at this now ... not sure how long it will take to track down.


### wj...@chromium.org (2011-01-25)

This is a WebKit issue, and definitely something different than http://code.google.com/p/chromium/issues/detail?id=64184 .

In this case, it appears that WebKit does the 'reasonable' thing in response to "obj.height = 3.41e38", which is to set the height of the main SVG tag element to be Inf (this is reasonable since SVG elements encode height using float, and this value is outside the allowed range for float).

The problem occurs with the relative size of the SVG rect. "10%" parses fine, but later when SVGLength::value() is called to get the height to create the stroke path, it outputs a value of 'Inf' which leads to problems further down the road.

I have a simple patch (see below) that seems to get around this without any crashes, although the WebKit community may consider it inappropriate to allow the main viewBox to remain (0 0 0 inf). I will open a WebKit security bug, propose this patch, and see if I can use it for a starting point for discussion on what the best design philosophy is behind a fix.


diff --git a/Source/WebCore/svg/SVGLength.cpp b/Source/WebCore/svg/SVGLength.cpp
index 281ee14..d3c2139 100644
--- a/Source/WebCore/svg/SVGLength.cpp
+++ b/Source/WebCore/svg/SVGLength.cpp
@@ -160,30 +160,40 @@ float SVGLength::value(const SVGElement* context) const
 
 float SVGLength::value(const SVGElement* context, ExceptionCode& ec) const
 {
+    float val = 0;
+
     switch (extractType(m_unit)) {
     case LengthTypeUnknown:
         ec = NOT_SUPPORTED_ERR;
         return 0;
     case LengthTypeNumber:
-        return m_valueInSpecifiedUnits;
+        val = m_valueInSpecifiedUnits;
     case LengthTypePercentage:
-        return convertValueFromPercentageToUserUnits(m_valueInSpecifiedUnits / 100, context, ec);
+        val = convertValueFromPercentageToUserUnits(m_valueInSpecifiedUnits / 100, context, ec);
     case LengthTypeEMS:
-        return convertValueFromEMSToUserUnits(m_valueInSpecifiedUnits, context, ec);
+        val = convertValueFromEMSToUserUnits(m_valueInSpecifiedUnits, context, ec);
     case LengthTypeEXS:
-        return convertValueFromEXSToUserUnits(m_valueInSpecifiedUnits, context, ec);
+        val = convertValueFromEXSToUserUnits(m_valueInSpecifiedUnits, context, ec);
     case LengthTypePX:
-        return m_valueInSpecifiedUnits;
+        val = m_valueInSpecifiedUnits;
     case LengthTypeCM:
-        return m_valueInSpecifiedUnits / 2.54f * cssPixelsPerInch;
+        val = m_valueInSpecifiedUnits / 2.54f * cssPixelsPerInch;
     case LengthTypeMM:
-        return m_valueInSpecifiedUnits / 25.4f * cssPixelsPerInch;
+        val = m_valueInSpecifiedUnits / 25.4f * cssPixelsPerInch;
     case LengthTypeIN:
-        return m_valueInSpecifiedUnits * cssPixelsPerInch;
+        val = m_valueInSpecifiedUnits * cssPixelsPerInch;
     case LengthTypePT:
-        return m_valueInSpecifiedUnits / 72 * cssPixelsPerInch;
+        val = m_valueInSpecifiedUnits / 72 * cssPixelsPerInch;
     case LengthTypePC:
-        return m_valueInSpecifiedUnits / 6 * cssPixelsPerInch;
+        val = m_valueInSpecifiedUnits / 6 * cssPixelsPerInch;
+    }
+
+    static const float max = std::numeric_limits<float>::max();
+    if (val >= -max && val <= max)
+        return val;
+    else {
+        ec = NOT_SUPPORTED_ERR;
+        return 0;
     }
 
     ASSERT_NOT_REACHED();


### wj...@chromium.org (2011-01-25)

[Empty comment from Monorail migration]

### wj...@chromium.org (2011-01-26)

WebKit bug filed: https://bugs.webkit.org/show_bug.cgi?id=53127

### ke...@google.com (2011-01-27)

Move to M11 from M10, as we've now branched.  If you believe this bug was moved in error, please come talk to me.

### js...@chromium.org (2011-01-28)

Moving back to m9.

### wj...@chromium.org (2011-01-31)

My initial attempt to resolve this by preventing SVGLength::value() from returning 'inf' has not been embraced by WebKit reviewers (see comments in https://bugs.webkit.org/show_bug.cgi?id=53127). It has been requested that we find a fix in Skia (or, presumably, in the interface to Skia, GraphicsContextSkia). Looking in GraphicsContextSkia I found code to check value-safety for Skia. It is currently inactive, being controlled by a define ENSURE_VALUE_SAFETY_FOR_SKIA that is currently turned off. Turning this value on does prevent the crash by causing Skia to refuse to continue if an 'inf' coordinate value is found, although the extra error checking involves additional overhead.

This code confirms my belief that Skia does not want to ever encounter 'inf' values (see http://trac.webkit.org/browser/trunk/Source/WebCore/platform/graphics/skia/GraphicsContextSkia.cpp#L96 for example)

I would recommend we turn it on in the short term until some resolution about the philosophy of retaining 'inf' values in WebKit is achieved. If this is acceptible let me know and I will prepare a patch.

### js...@chromium.org (2011-01-31)

The ENSURE_VALUE_SAFETY_FOR_SKIA has been off for about a year, so I'm not sure it would be a good idea to turn it back on (performance issues, unintended breakage, etc.). It does seem like Skia should be at least failing gracefully when we get an inf value.

CC'ing the Skia guys on this, to get a bit more clarification on what we can do here.

### js...@chromium.org (2011-02-01)

@reed, @bsalomon - Any thoughts? Just to put some context here, we need a fix for this landed and merged to stable within the next three weeks. We have a hard requirement of no known high or critical severity security bugs for pwn2pwn in the first week of March.


### bs...@google.com (2011-02-02)

@jschuh, I don't know much about the guts of skia, just the gpu backend. I think you'll need Mike's help with this one. 

### re...@google.com (2011-02-02)

I can work on this next week. I think Skia already has a bottle-neck for this (SkScalarToFixed) which could be modified to explicitly look for overflow, infinities, NaN, and return something pinned rather than wrapping.

### wj...@chromium.org (2011-02-02)

Mike - I've been working on this already, and can work on it now so long as I can get some sense of what the preferred direction of the work is. I can investigate replacing 'inf' with whatever the max representation in Fixed is, if that seems reasonable. What would be an appropriate value to return for NaN?

### wj...@chromium.org (2011-02-03)

I've tried putting checks in SkScalarToFixed (actually SkFloatToFixed), but the crash stills occurs. It doesn't seem to go through this funtion in this particular case.

I've attached a patch for discussion. It does the following:
1) Adds a function SkRect::hasValidCoordinates(), and
2) Calls this function in SkCanvas::quickReject().

It solves *this particular problem* with fairly low overhead. Does this seem reasonable?

I'm running the layout tests now to see if it breaks anything ...

### wj...@chromium.org (2011-02-03)

On linux at least the patch seems to cause relatively little havoc (maybe one layout test?).

### js...@chromium.org (2011-02-03)

@wjmaclean - Excellent. Are you familiar with how to branch Skia and roll to a release channel?

### js...@chromium.org (2011-02-03)

To clarify on c19, I'm asking with respect to the eventual merge after the patch gets landed.

### re...@google.com (2011-02-03)

1. I'm fine with the patch at the moment, as it fixes a critical bug
2. Lets add a unittest to skia (skia/trunk/tests) for this, in case we want to change specifics of the impl later, and/or expand this sort of checking to other primitive types.


### wj...@chromium.org (2011-02-07)

I have added a unittest for the rejection of 'inf' coordinates in SkRects as suggested by Mike. At present it just tests hasValidCoordinates() directly, to avoid instantiating a canvas in the test, although I can add that if desired.

Should I upload this patch to the Skia rietveld review site before committing it, or just directly commit it (given that it's a security bug)? I will proceed as soon as I hear back on this question.

### sc...@gmail.com (2011-02-07)

@wjmaclean -- thanks for your work on this! It's okay to upload to rietveld if you want to; we'd just recommend avoiding "security OMG!!!" in the review text. Maybe something nebulous like "better handling for inf co-ordinate values"? :)

### wj...@chromium.org (2011-02-07)

Patch uploaded as http://codereview.appspot.com/4080060/.

Mike has LGTM'd this, and I've committed it. Since there are other new commits on Skia since the latest DEPS roll, should I leave it to Mike to do the next DEPS roll?

### sc...@gmail.com (2011-02-07)

Yeah, leaving the DEPS roll on trunk to Mike seems fine, as long as it occurs before the M11 branch point (few weeks to go ;-)

The more important fun is merging to M9 and M10. Luckily we already have a Skia branch for M9 (not sure about M10), so we should be able to cherrypick this revision without too much trouble.

http://code.google.com/p/skia/source/detail?r=764

### wj...@chromium.org (2011-02-07)

Sounds good ... cherry-picking shouldn't be too hard since, with the exception of two lines of code in quickReject(), it's all new functions (and thus hopefully orthogonal to the existing codebase).

### sc...@gmail.com (2011-02-13)

@slaweck: thanks for the great report (small repro, good stack trace + register analysis). And congrats on your provisional $1000 Chromium Security Reward :D

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

### js...@chromium.org (2011-02-28)

Merged to m10: http://src.chromium.org/viewvc/chrome?view=rev&revision=76300

### sc...@gmail.com (2011-03-04)

Invoice finalized; payment is in e-payment system.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

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

### bu...@chromium.org (2013-04-06)

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

This issue was migrated from crbug.com/chromium/70244?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087075)*
