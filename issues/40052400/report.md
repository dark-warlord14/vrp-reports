# Use of uninitialized value in SkAlphaRuns::Break

| Field | Value |
|-------|-------|
| **Issue ID** | [40052400](https://issues.chromium.org/issues/40052400) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Reporter** | mi...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2011-12-25 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use of unitialized value with border styles

**VERSION**  

Chrome Version:

Chromium 18.0.983.0 (Developer Build 115770)  

OS Linux  

WebKit 535.15 (@103658)  

JavaScript V8 3.8.2.1

Operating System: linux 64bit

**REPRODUCTION CASE**

<html>
<head>
<style>
#el2 {
border-radius: 6px;
-webkit-border-after-width: 3px;
-webkit-border-after-style: dashed;
-webkit-border-end-width: 40px;
}
</style>
<script>
function crash(){
el2 = document.createElement('input')
el2.setAttribute('id', 'el2')
document.body.appendChild(el2)
var width = 150
setInterval(function() {
width+=1
el2.style.width=width+'px'
},10)
}
window.onload=crash
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer  

Crash State:

Conditional jump or move depends on uninitialised value(s)  

at 0x10EE930: SkAlphaRuns::Break(short\*, unsigned char\*, int, int) (in chromium/chrome-linux/chromium-browser)  

by 0x10EEA55: SkAlphaRuns::add(int, unsigned int, int, unsigned int, unsigned int, int) (in chromium/chrome-linux/chromium-browser)  

by 0x10BC67B: SuperBlitter::blitH(int, int, int) (in chromium/chrome-linux/chromium-browser)  

by 0x10C0053: walk\_convex\_edges(SkEdge\*, SkPath::FillType, SkBlitter\*, int, int, void (\*)(SkBlitter\*, int, bool)) (in chromium/chrome-linux/chromium-browser)

Address 0x13cdcd67 is 13,623 bytes inside a block of size 24,564 free'd  

Address 0x13c632fc is not stack'd, malloc'd or (recently) free'd

## Attachments

- [sk1.html](attachments/sk1.html) (text/html; charset=us-ascii, 445 B)
- [vg-sk2.txt](attachments/vg-sk2.txt) (text/x-c; charset=us-ascii, 585.8 KB)
- [vg-sk1.txt](attachments/vg-sk1.txt) (text/x-c; charset=us-ascii, 573.2 KB)
- [sk2.html](attachments/sk2.html) (text/html; charset=us-ascii, 488 B)
- [convex.diff](attachments/convex.diff) (text/x-diff; charset=us-ascii, 1023 B)

## Timeline

### in...@chromium.org (2011-12-26)

Mike, can you please help to take a look.

### in...@chromium.org (2012-01-09)

Mike, this is an important security vulnerability that affect Chrome Stable and might be easy to fix since it looks like a straightforward uninitialized value. We have a stable patch release in next week. Can you please help to fix this.

### [Deleted User] (2012-01-09)

I don't seem to have permission to see the issue :(

### js...@chromium.org (2012-01-09)

@reed - You're CC'd as reed@chromium.org. Perhaps you're not logged in with the correct account (which is a common mistake)?

### [Deleted User] (2012-01-09)

Triggers an assert when webkit passes these 4 points to skia, and claims they are convex (which they aint)

+		points[0]	{m_x=341.00000 m_y=10.000000 }	const WebCore::FloatPoint
+		points[1]	{m_x=155.50000 m_y=19.275002 }	const WebCore::FloatPoint
+		points[2]	{m_x=155.50000 m_y=19.087500 }	const WebCore::FloatPoint
+		points[3]	{m_x=341.00000 m_y=33.000000 }	const WebCore::FloatPoint

Stack trace:

 	chrome.dll!SkDebugf_FileLine(const char * file=0x61ab7080, int line=0x000000fa, bool fatal=true, const char * format=0x61ab7060, ...)  Line 25	C++
 	chrome.dll!walk_convex_edges(SkEdge * prevHead=0x0781b770, SkPath::FillType __formal=kWinding_FillType, SkBlitter * blitter=0x0781b808, int start_y=0x00000008, int stop_y=0x00000064, void (SkBlitter *, int, bool)* proc=0x00000000)  Line 250 + 0x2d bytes	C++
 	chrome.dll!sk_fill_path(const SkPath & path={...}, const SkIRect * clipRect=0x00000000, SkBlitter * blitter=0x0781b808, int start_y=0x00000008, int stop_y=0x00000064, int shiftEdgesUp=0x00000002, const SkRegion & clipRgn={...})  Line 473 + 0x20 bytes	C++
 	chrome.dll!SkScan::AntiFillPath(const SkPath & path={...}, const SkRegion & clip={...}, SkBlitter * blitter=0x0781bd2c, bool forceRLE=true)  Line 625 + 0x22 bytes	C++
 	chrome.dll!SkAAClip::setPath(const SkPath & path={...}, const SkRegion * clip=0x0781be74, bool doAA=true)  Line 1284 + 0x16 bytes	C++
 	chrome.dll!SkRasterClip::setPath(const SkPath & path={...}, const SkRegion & clip={...}, bool doAA=true)  Line 76 + 0x18 bytes	C++
 	chrome.dll!clipPathHelper(const SkCanvas * canvas=0x0bd546e0, SkRasterClip * currClip=0x089bf954, const SkPath & devPath={...}, SkRegion::Op op=kIntersect_Op, bool doAA=true)  Line 1021	C++
 	chrome.dll!SkCanvas::clipPath(const SkPath & path={...}, SkRegion::Op op=kIntersect_Op, bool doAA=true)  Line 1060 + 0x20 bytes	C++
 	chrome.dll!WebCore::PlatformContextSkia::clipPathAntiAliased(const SkPath & clipPath={...})  Line 266 + 0x22 bytes	C++
>	chrome.dll!WebCore::GraphicsContext::clipConvexPolygon(unsigned int numPoints=0x00000004, const WebCore::FloatPoint * points=0x0781c2bc, bool antialiased=true)  Line 489	C++
 	chrome.dll!WebCore::RenderBoxModelObject::clipBorderSidePolygon(WebCore::GraphicsContext * graphicsContext=0x0781d95c, const WebCore::RoundedRect & outerBorder={...}, const WebCore::RoundedRect & innerBorder={...}, WebCore::BoxSide side=BSRight, bool firstEdgeMatches=false, bool secondEdgeMatches=false)  Line 2336	C++
 	chrome.dll!WebCore::RenderBoxModelObject::paintOneBorderSide(WebCore::GraphicsContext * graphicsContext=0x0781d95c, const WebCore::RenderStyle * style=0x07ec2a20, const WebCore::RoundedRect & outerBorder={...}, const WebCore::RoundedRect & innerBorder={...}, const WebCore::IntRect & sideRect={...}, WebCore::BoxSide side=BSRight, WebCore::BoxSide adjacentSide1=BSTop, WebCore::BoxSide adjacentSide2=BSBottom, const WebCore::BorderEdge * edges=0x0781c5cc, const WebCore::Path * path=0x0781c460, WebCore::BackgroundBleedAvoidance bleedAvoidance=BackgroundBleedUseTransparencyLayer, bool includeLogicalLeftEdge=true, bool includeLogicalRightEdge=true, bool antialias=false, const WebCore::Color * overrideColor=0x00000000)  Line 1529	C++


### [Deleted User] (2012-01-09)

Proposed patch to webkit attached.

### [Deleted User] (2012-01-10)

inferno, can you confirm that the attached patch fixes the issue? I will work on a formal patch for webkit.

### in...@chromium.org (2012-01-10)

Mike, i am ooo till friday with only access to email. this should be simple test under valgrind - http://dev.chromium.org/developers/how-tos/using-valgrind

### [Deleted User] (2012-01-10)

https://bugs.webkit.org/show_bug.cgi?id=75960

### [Deleted User] (2012-01-10)

webkit fix has landed in r104609

### js...@chromium.org (2012-01-10)

@reed - Thanks.
Landed upstream http://trac.webkit.org/changeset/104609


### js...@chromium.org (2012-01-18)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-01-19)

merged to m16 in r105343, merged to m17 in r105345

### js...@chromium.org (2012-01-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-01-20)

@miaubiz: thanks for the report and please accept a $1000 Chromium Security Reward!

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

### sc...@gmail.com (2012-02-15)

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

This issue was migrated from crbug.com/chromium/108605?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052400)*
