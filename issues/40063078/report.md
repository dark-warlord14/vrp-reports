# Heap-buffer-overflow in SkA8_Blitter::blitAntiH

| Field | Value |
|-------|-------|
| **Issue ID** | [40063078](https://issues.chromium.org/issues/40063078) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals, Internals>Skia |
| **Reporter** | at...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2012-08-09 |
| **Bounty** | $500.00 |

## Description

Repro-file as attachment.

Chrome version: ASAN Chromium 23.0.1232.0

==7974== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7f1cb02f82f9 at pc 0x7f1cc6a4a445 bp 0x7fffb9207570 sp 0x7fffb9207568
READ of size 1 at 0x7f1cb02f82f9 thread T0
    #0 0x7f1cc6a4a444 in SkA8_Blitter::blitAntiH(int, int, unsigned char const*, short const*) ???:0
    #1 0x7f1cc6905b5b in vertish(int, int, int, int, SkBlitter*, int) ../../third_party/skia/src/core/SkScan_Antihair.cpp:0
    #2 0x7f1cc6901a70 in do_anti_hairline(int, int, int, int, SkIRect const*, SkBlitter*) ../../third_party/skia/src/core/SkScan_Antihair.cpp:0
    #3 0x7f1cc690126f in SkScan::AntiHairLineRgn(SkPoint const&, SkPoint const&, SkRegion const*, SkBlitter*) ???:0
    #4 0x7f1cc6908d9e in hairquad(SkPoint const*, SkRegion const*, SkBlitter*, int, void (*)(SkPoint const&, SkPoint const&, SkRegion const*, SkBlitter*)) ../../third_party/skia/src/core/SkScan_Hairline.cpp:0
    #5 0x7f1cc6908d7b in hairquad(SkPoint const*, SkRegion const*, SkBlitter*, int, void (*)(SkPoint const&, SkPoint const&, SkRegion const*, SkBlitter*)) ../../third_party/skia/src/core/SkScan_Hairline.cpp:0
    #6 0x7f1cc6908d7b in hairquad(SkPoint const*, SkRegion const*, SkBlitter*, int, void (*)(SkPoint const&, SkPoint const&, SkRegion const*, SkBlitter*)) ../../third_party/skia/src/core/SkScan_Hairline.cpp:0
    #7 0x7f1cc6908d7b in hairquad(SkPoint const*, SkRegion const*, SkBlitter*, int, void (*)(SkPoint const&, SkPoint const&, SkRegion const*, SkBlitter*)) ../../third_party/skia/src/core/SkScan_Hairline.cpp:0
    #8 0x7f1cc6908d7b in hairquad(SkPoint const*, SkRegion const*, SkBlitter*, int, void (*)(SkPoint const&, SkPoint const&, SkRegion const*, SkBlitter*)) ../../third_party/skia/src/core/SkScan_Hairline.cpp:0
    #9 0x7f1cc69078dd in hair_path(SkPath const&, SkRasterClip const&, SkBlitter*, void (*)(SkPoint const&, SkPoint const&, SkRegion const*, SkBlitter*)) ../../third_party/skia/src/core/SkScan_Hairline.cpp:0
    #10 0x7f1cc688cc1c in SkDraw::drawPath(SkPath const&, SkPaint const&, SkMatrix const*, bool) const ???:0

## Attachments

- [chrome-heap-buffer-overflow-SkA8BlitterblitAntiH-075.html](attachments/chrome-heap-buffer-overflow-SkA8BlitterblitAntiH-075.html) (text/html; charset=us-ascii, 996 B)

## Timeline

### in...@chromium.org (2012-08-09)

[Empty comment from Monorail migration]

### [Deleted User] (2012-08-09)

https://cluster-fuzz.appspot.com/testcase?key=91685698

### [Deleted User] (2012-08-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-09)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=91685698

Uploader: cdn@chromium.org

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x7fd5ffd41af9
Crash State:
  - crash stack -
  SkA8_Blitter::blitAntiH
  vertish
  do_anti_hairline
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=137386:137400

Minimized Testcase (0.58 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97clSdWfr8TJN5rOrav-DIxAfVs1DQlfnFAqPy8pcd_2xdL7naPnudJYS-lwmJ091hbNmj3uqNO5w-b_1qKhPuSHSGZD_ciYrPdiZTjlPf1WB1DiB_hXlRHlj78tpqse4xJvQGnKkNyjXcpn3eJ4W4no7cTwZcPlAYqy4cLOYcd1EXKO8Y

### in...@chromium.org (2012-08-09)

Mike, this looks very similar to the ones you fixed recently.

### [Deleted User] (2012-08-09)

I can catch this in the debugger with the repo case (thanks!).

The path has infinities in its points, but my isFinite() check in SkCanvas::drawPath() somehow didn't catch it (isFinite is returning true when I call it from gdb). So, the bug must be that there is some codepath earlier where we introduce the infinities but such that I don't catch it. I'll keep looking...

### [Deleted User] (2012-08-09)

Have potential fix, will try it against the repro case tomorrow.

https://codereview.appspot.com/6449125

### [Deleted User] (2012-08-10)

canvas.setAttribute("width",386)
canvas.setAttribute("height",464)
try{ctx.quadraticCurveTo( 157,366 , 286,208 );}catch(e){}
try{ctx.arcTo( 37,442 , 315,163 ,957494590897113);}catch(e){}
try{ctx.scale(442800394259393,346);}catch(e){}
try{ctx.shadowColor="#B29";}catch(e){}
try{ctx.scale(0x67A676D03A9C9BC5708,436);}catch(e){}
try{ctx.lineTo( 175,397 );}catch(e){}
try{ctx.stroke()}catch(e){};
try{ctx.fill()}catch(e){};
try{ctx.setTransform(0.42717719334177673,0.5997530829627067,-0.6888179976958781,0.4600594050716609, 304,122 );}catch(e){}
try{ctx.arcTo( 243,266 , 92,262 ,438);}catch(e){}
try{ctx.fill()}catch(e){};
try{ctx.arcTo( 57,101 , 52,397 ,-605775655480101);}catch(e){}
try{ctx.shadowBlur="7600";}catch(e){}
try{ctx.translate(38, 122.5);}catch(e){}
try{ctx.closePath();ctx.stroke();}catch(e){}


### in...@chromium.org (2012-08-10)

[Empty comment from Monorail migration]

### to...@chromium.org (2012-08-10)

Mike wrote a patch for this before he headed out; we'll verify, land, and roll it today.

### in...@chromium.org (2012-08-10)

Looks like landed in skia and should go into chromium in the next roll. Awesome!

TomH	
2 hours, 20 minutes ago #4
Landed as r5042.

### cl...@chromium.org (2012-08-11)

ClusterFuzz has detected this issue as fixed in range 151058:151092.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=91685698

Uploader: cdn@chromium.org

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x7fd5ffd41af9
Crash State:
  - crash stack -
  SkA8_Blitter::blitAntiH
  vertish
  do_anti_hairline
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=137386:137400
Fixed: https://cluster-fuzz.appspot.com/revisions?range=151058:151092

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97clSdWfr8TJN5rOrav-DIxAfVs1DQlfnFAqPy8pcd_2xdL7naPnudJYS-lwmJ091hbNmj3uqNO5w-b_1qKhPuSHSGZD_ciYrPdiZTjlPf1WB1DiB_hXlRHlj78tpqse4xJvQGnKkNyjXcpn3eJ4W4no7cTwZcPlAYqy4cLOYcd1EXKO8Y

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-08-16)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-08-20)

OOB read in Skia, $500, thanks!

### [Deleted User] (2012-08-30)

scarybeasts- should this be merged into M21 and/or M22?

### in...@chromium.org (2012-08-30)

to m22 only. m21, we can skip.

### sc...@gmail.com (2012-09-12)

[Empty comment from Monorail migration]

### [Deleted User] (2012-09-17)

Fix merged into Skia's chrome/m22_1229 branch as https://code.google.com/p/skia/source/detail?r=5571

### sc...@gmail.com (2012-09-17)

Great stuff, thanks!

### [Deleted User] (2012-11-26)

CCing David Belcher from RIM to determine whether they are affected.

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

This issue was migrated from crbug.com/chromium/141651?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Skia]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063078)*
