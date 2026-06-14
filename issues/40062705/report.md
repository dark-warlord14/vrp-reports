# Heap-buffer-overflow in SkA8_Blitter::blitH

| Field | Value |
|-------|-------|
| **Issue ID** | [40062705](https://issues.chromium.org/issues/40062705) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals, Internals>Skia |
| **Reporter** | at...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2012-08-06 |
| **Bounty** | $1,000.00 |

## Description

Repro-file as attachment.

ASAN Chromium 22.0.1228.0 

ASAN-report:
==2861== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7f553684113a at pc 0x7f554e128838 bp 0x7ffff1766c40 sp 0x7ffff1766c38
WRITE of size 1 at 0x7f553684113a thread T0
    #0 0x7f554e128837 in SkA8_Blitter::blitH(int, int, int) ???:0
    #1 0x7f554dfec235 in sk_fill_path(SkPath const&, SkIRect const*, SkBlitter*, int, int, int, SkRegion const&) ???:0
    #2 0x7f554dfee45e in SkScan::FillPath(SkPath const&, SkRegion const&, SkBlitter*) ???:0
    #3 0x7f554dfe1a9a in SkScan::AntiFillPath(SkPath const&, SkRegion const&, SkBlitter*, bool) ???:0
    #4 0x7f554dfe2af7 in SkScan::AntiFillPath(SkPath const&, SkRasterClip const&, SkBlitter*) ???:0
    #5 0x7f554df6becc in SkDraw::drawPath(SkPath const&, SkPaint const&, SkMatrix const*, bool) const ???:0
    #6 0x7f554dfdc43c in SkScalerContext::getImage(SkGlyph const&) ???:0
    #7 0x7f554df7ef88 in SkGlyphCache::findImage(SkGlyph const&) ???:0
.
.
.

## Attachments

- [chrome-heap-buffer-overflow-SkA8BlitterblitH-afb.html](attachments/chrome-heap-buffer-overflow-SkA8BlitterblitH-afb.html) (text/html; charset=utf-8, 533 B)

## Timeline

### in...@chromium.org (2012-08-06)

Mike, you just fixed a similar bug in this code area. looks like we missed some place ?

### in...@chromium.org (2012-08-06)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-06)

looks similar to http://code.google.com/p/chromium/issues/detail?id=138238. clusterfuzz report coming https://cluster-fuzz.appspot.com/testcase?key=90585092

### [Deleted User] (2012-08-06)

II see an assert in the debug build, where I have overflowing a coefficient .6 -> .16. Am pondering a solution.

### in...@chromium.org (2012-08-06)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=90585092

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow WRITE 1
Crash Address: 0x7f9ae016aa49
Crash State:
  - crash stack -
  SkA8_Blitter::blitH
  sk_fill_path
  SkScan::FillPath
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=116541:116563

Minimized Testcase (0.37 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96WrRSrQgpRHwh7wExW9-jxQ8cccZH3IIA--_Lb8tpNw9_4gEO_QOl4TSwXyOO0CZ5ZYIVzthPrtCvvZkTo0SZJbxDCbEVkWscnzdEg4QO8arMYwkx00AQ3zF2LA50WyypWryUFBhlzczZA0c05Lh3nGCChsAPlJ7Ihbfb31M93iVen1Ck
</body>
<script>var canvas=document.body.appendChild(document.createElement("canvas"));
var ctx=canvas.getContext("2d")
try{ctx.lineWidth="700";}catch(e){}
try{ctx.font="italic normal 300 larger/196 Courier New";}catch(e){}
try{ctx.setTransform(0.1,1,-0.7,5,4,6);}catch(e){}
try{ctx.transform(1,6,-0.9,0.7,1,4);}catch(e){}
try{ctx.strokeText("���", 1,1,1);}catch(e){};


</script>

### in...@chromium.org (2012-08-06)

sorry this is sec-high.

### [Deleted User] (2012-08-06)

fixed in skia rev. 4960

### in...@chromium.org (2012-08-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2012-08-07)

ClusterFuzz has detected this issue as fixed in range 150333:150342.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=90585092

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow WRITE 1
Crash Address: 0x7f9ae016aa49
Crash State:
  - crash stack -
  SkA8_Blitter::blitH
  sk_fill_path
  SkScan::FillPath
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=116541:116563
Fixed: https://cluster-fuzz.appspot.com/revisions?range=150333:150342

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96WrRSrQgpRHwh7wExW9-jxQ8cccZH3IIA--_Lb8tpNw9_4gEO_QOl4TSwXyOO0CZ5ZYIVzthPrtCvvZkTo0SZJbxDCbEVkWscnzdEg4QO8arMYwkx00AQ3zF2LA50WyypWryUFBhlzczZA0c05Lh3nGCChsAPlJ7Ihbfb31M93iVen1Ck

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### ke...@google.com (2012-08-08)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-09)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2012-09-12)

[Empty comment from Monorail migration]

### ep...@google.com (2012-09-12)

Fix merged into Skia's chrome/m22_1229 branch as https://code.google.com/p/skia/source/detail?r=5510

Do we still need to merge this into M21 also?

### in...@chromium.org (2012-09-12)

no, we don't need it for m21.

### sc...@gmail.com (2012-09-25)

OOB write. $1000. Thx.

### sc...@gmail.com (2012-10-12)

[Empty comment from Monorail migration]

### [Deleted User] (2012-11-26)

CCing David Belcher from RIM so that they can assess whether they are affected.

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/140803?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Skia]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062705)*
