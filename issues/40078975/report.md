# Heap-use-after-free in WebCore::SVGFontFaceElement::associatedFontElement

| Field | Value |
|-------|-------|
| **Issue ID** | [40078975](https://issues.chromium.org/issues/40078975) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>SVG |
| **Reporter** | at...@gmail.com |
| **Assignee** | ta...@google.com |
| **Created** | 2014-02-24 |
| **Bounty** | $1,000.00 |

## Description


Tested on:

OS: Ubuntu 12.04

Chromium: ASAN 35.0.1851.0 (Developer Build 252405) aura

Repro-file:

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg id="svg-root" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 480 360" baseProfile="basic" version="1.1" xmlns:xlink="http://www.w32.org/1999/xlink">
   <defs><discard />
    <font id="Font1" horiz-adv-x="5121">
     <font-face mathematical="327681" ideographic="-2" font-weight="bold" descent="100.999999999999999999999999999999999999999999999999999999" cap-height="-11" hanging="1" units-per-em="8" alphabetic="-32769" x-height="128" font-family="HappySad" ascent="255"/>
    </font>
    <altGlyphDef id="Ysmile">
      </altGlyphDef>
   </defs>
   <g stroke-width="32" font-size="10241" font-family="HappySad" fill="none">
    <text y="190" x="-2147483648" stroke="fuchsia">
     <altGlyph xlink:href="#Hsmile">H</altGlyph>
     <altGlyph xlink:href="#Asmile">A</altGlyph>
     </text>
    </g>
</svg>

ASAN-trace:

==7086==ERROR: AddressSanitizer: heap-use-after-free on address 0x6100000039f8 at pc 0x7fa764277db0 bp 0x7fff6291d410 sp 0x7fff6291d408
READ of size 8 at 0x6100000039f8 thread T0 (chrome)
    #0 0x7fa764277daf in WebCore::SVGFontFaceElement::associatedFontElement() const /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/svg/SVGFontFaceElement.cpp:266:0
    #1 0x7fa76421f7a8 in WebCore::svgFontAndFontFaceElementForFontData(WebCore::SimpleFontData const*, WebCore::SVGFontFaceElement*&, WebCore::SVGFontElement*&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/svg/SVGTextRunRenderingContext.cpp:52:0
    #2 0x7fa76421ffde in WebCore::SVGTextRunRenderingContext::glyphDataForCharacter(WebCore::Font const&, WebCore::TextRun const&, WebCore::WidthIterator&, int, bool, int, unsigned int&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/svg/SVGTextRunRenderingContext.cpp:215:42
    #3 0x7fa7625144c4 in WebCore::WidthIterator::glyphDataForCharacter(int, bool, int, unsigned int&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/fonts/WidthIterator.cpp:79:0
    #4 0x7fa7625151cf in unsigned int WebCore::WidthIterator::advanceInternal<WebCore::Latin1TextIterator>(WebCore::Latin1TextIterator&, WebCore::GlyphBuffer*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/fonts/WidthIterator.cpp:163:0
    #5 0x7fa7625146bd in WebCore::WidthIterator::advance(int, WebCore::GlyphBuffer*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/fonts/WidthIterator.cpp:327:16
.
.
.
0x6100000039f8 is located 184 bytes inside of 192-byte region [0x610000003940,0x610000003a00)
freed by thread T0 (chrome) here:
    #0 0x7fa75e41aa41 in __interceptor_free _asan_rtl_:0
    #1 0x7fa7621e9eb7 in void WebCore::removeDetachedChildrenInContainer<WebCore::Node, WebCore::ContainerNode>(WebCore::ContainerNode&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/ContainerNodeAlgorithms.h:102:0
    #2 0x7fa7621ea8f0 in WebCore::ContainerNode::~ContainerNode() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:98:0
    #3 0x7fa76a51579e in WebCore::SVGDefsElement::~SVGDefsElement() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/svg/SVGDefsElement.h:29:0
    #4 0x7fa76430dcf2 in derefIfNotNull<WebCore::SVGElement> /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/PassRefPtr.h:57:0
    #5 0x7fa76430dcf2 in ~RefPtr /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/RefPtr.h:51:0
.
.
.


## Timeline

### cl...@chromium.org (2014-02-24)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=6660682581803008

### cl...@chromium.org (2014-02-24)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6660682581803008

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x611000064778
Crash State:
  - crash stack -
  WebCore::SVGFontFaceElement::associatedFontElement
  WebCore::SVGFontData::fillSVGGlyphPage
  - free stack -
  void WebCore::removeDetachedChildrenInContainer<WebCore::Node, WebCore::ContainerNode>
  WebCore::ContainerNode::~ContainerNode
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=251556:251980

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv9681PSSI_bV01cckbsIm3e2z2e841zpMudbm06vZFMGzU5m6c8qRdpA-gxlK-y93YhSTjpDRI9QsKrrl_j85ikav_f5gEFhhjdThvIppJx4j5i4wojJiog8aN-V3dPnn5F6XUwAuY5JvEbsPL_UXjS4EW05wQ



### cl...@chromium.org (2014-02-24)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-02-24)

regression from http://src.chromium.org/viewvc/blink?view=rev&revision=167257

### in...@chromium.org (2014-02-25)

[Empty comment from Monorail migration]

### ta...@google.com (2014-02-25)

Looking


### cl...@chromium.org (2014-02-25)

[Empty comment from Monorail migration]

### ta...@google.com (2014-02-25)

[Empty comment from Monorail migration]

### ta...@google.com (2014-02-25)

I think, this is a bug of RenderSVGInlineText (or some SVG renderer).

void RenderSVGInlineText::styleDidChange(StyleDifference diff, const RenderStyle* oldStyle)
{
...
    // The text metrics may be influenced by style changes.                                                       
    if (RenderSVGText* textRenderer = RenderSVGText::locateRenderSVGTextAncestor(this))
        textRenderer->subtreeStyleDidChange(this); ////// 
}

The above subtreeStyleDidChange touches old RenderStyles.

For example, when running attached test.svg,

RenderView 0xc54b3604010               	#document	0x2c9263620010
  RenderSVGRoot 0xc54b3624010          	svg	0x2c9263630010
    RenderSVGContainer 0xc54b3640010   	g	0x2c926364c118
      RenderSVGText 0xc54b3644010      	text	0x2c9263678010
        RenderSVGTSpan 0xc54b3650010   	altGlyph	0x2c9263688010
(a)     RenderSVGInlineText 0xc54b365c010	#text	0x2c926363c390 "\n     " // not recalced
        RenderSVGTSpan 0xc54b36500c0   	altGlyph	0x2c9263688178
(b)     RenderSVGInlineText 0xc54b365c128	#text	0x2c926363c400 "\n     " // in styleDidChange

during (b)'s styleDidChange, (a)'s old style (which has not been updated) is used.

Since the old style has an old font, i.e. removed SVGFontFaceElement, this crash is caused.

I'm now investigating how to fix this issue.



### ta...@google.com (2014-02-25)

[Empty comment from Monorail migration]

### ta...@google.com (2014-02-25)

pdr, would you help me to solve this issue?

I think, RenderSVGInlineText::styleDidChange should not invoke RenderSVGText::subtreeStyleDidChange if the RenderSVGText's descendants need style recalc (including forced style recalc).

So I have no idea about where we should invoke:
---
  if (RenderSVGText* textRenderer = RenderSVGText::locateRenderSVGTextAncestor(this))
        textRenderer->subtreeStyleDidChange(this);
---


### ta...@google.com (2014-02-25)

I guess, we should do in RenderSVGText::layout...

So I created https://codereview.chromium.org/176853009.


### in...@chromium.org (2014-02-25)

[Empty comment from Monorail migration]

### ts...@chromium.org (2014-02-25)

[Empty comment from Monorail migration]

### ta...@google.com (2014-02-26)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-02-27)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=167993

------------------------------------------------------------------------
r167993 | tasak@google.com | 2014-02-27T08:37:53.212907Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/svg/SVGFontFaceElement.cpp?r1=167993&r2=167992&pathrev=167993
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/svg/RenderSVGInlineText.cpp?r1=167993&r2=167992&pathrev=167993
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/svg/RenderSVGText.cpp?r1=167993&r2=167992&pathrev=167993
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/discard-svg-font-face-crash-expected.svg?r1=167993&r2=167992&pathrev=167993
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/discard-svg-font-face-crash.svg?r1=167993&r2=167992&pathrev=167993
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/svg/RenderSVGText.h?r1=167993&r2=167992&pathrev=167993

Fix crash in SVGFontFaceElement::associatedFontElement crash when removing SVGFontFaceElement.

(1) We need to remove its font-face rule from FontCache when removing SVGFontFaceElement,

(2) We should not use old styles in RenderSVGInlineText::styleDidChange.
Since styleRecalc is done in document-order, we cannot see any styles of next renderer
(obtained by nextInPreOrder).
The old styles might have old fonts which are created by SVGFontFaceElement.

BUG=346192
TEST=fast/dom/discard-svg-font-face-crash.svg

Review URL: https://codereview.chromium.org/176853009
------------------------------------------------------------------------

### in...@chromium.org (2014-02-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-28)

ClusterFuzz has detected this issue as fixed in range 253930:254034.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6660682581803008

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x611000064778
Crash State:
  - crash stack -
  WebCore::SVGFontFaceElement::associatedFontElement
  WebCore::SVGFontData::fillSVGGlyphPage
  - free stack -
  void WebCore::removeDetachedChildrenInContainer<WebCore::Node, WebCore::ContainerNode>
  WebCore::ContainerNode::~ContainerNode
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=251556:251980
Fixed: https://cluster-fuzz.appspot.com/revisions?range=253930:254034

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv9681PSSI_bV01cckbsIm3e2z2e841zpMudbm06vZFMGzU5m6c8qRdpA-gxlK-y93YhSTjpDRI9QsKrrl_j85ikav_f5gEFhhjdThvIppJx4j5i4wojJiog8aN-V3dPnn5F6XUwAuY5JvEbsPL_UXjS4EW05wQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ti...@chromium.org (2014-04-22)

This is already in M35 - no merge required.

### ti...@chromium.org (2014-05-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-05-16)

This bug is a regression and does not impact stable. Removing incorrectly added Release-0-M35 label.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-05-19)

Congrats - $1000 for this one.

### cl...@chromium.org (2014-06-05)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-07-22)

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/346192?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078975)*
