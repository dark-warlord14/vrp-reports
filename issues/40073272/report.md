# Heap-buffer-overflow in SkAAClipBlitter::blitAntiH

| Field | Value |
|-------|-------|
| **Issue ID** | [40073272](https://issues.chromium.org/issues/40073272) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals, Internals>Skia |
| **Reporter** | at...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2012-09-12 |
| **Bounty** | $500.00 |

## Description


Repro-file as attachment.

Chromium 23.0.1263.0 (Developer Build 155968)

ASAN-report:

==5702== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7f68314ff696 at pc 0x7f684807cffa bp 0x7fff5235c140 sp 0x7fff5235c138
READ of size 1 at 0x7f68314ff696 thread T0
    #0 0x7f684807cff9 in SkAAClipBlitter::blitAntiH(int, int, unsigned char const*, short const*) ???:0
    #1 0x7f6847fff15b in vertish(int, int, int, int, SkBlitter*, int) ../../third_party/skia/src/core/SkScan_Antihair.cpp:0
    #2 0x7f6847ffb0a7 in do_anti_hairline(int, int, int, int, SkIRect const*, SkBlitter*) ../../third_party/skia/src/core/SkScan_Antihair.cpp:0
    #3 0x7f6847ffa81d in SkScan::AntiHairLineRgn(SkPoint const&, SkPoint const&, SkRegion const*, SkBlitter*) ???:0
    #4 0x7f6848000d43 in hair_path(SkPath const&, SkRasterClip const&, SkBlitter*, void (*)(SkPoint const&, SkPoint const&, SkRegion const*, SkBlitter*)) ../../third_party/skia/src/core/SkScan_Hairline.cpp:0
    #5 0x7f6847f7a79f in SkDraw::drawPath(SkPath const&, SkPaint const&, SkMatrix const*, bool) const ???:0
    #6 0x7f6847f60b88 in SkCanvas::drawPath(SkPath const&, SkPaint const&) ???:0
    #7 0x7f6848619905 in ui::NativeThemeBase::PaintArrowButton(SkCanvas*, gfx::Rect const&, ui::NativeTheme::Part, ui::NativeTheme::State) const ???:0
    #8 0x7f68486180a7 in ui::NativeThemeBase::Paint(SkCanvas*, ui::NativeTheme::Part, ui::NativeTheme::State, gfx::Rect const&, ui::NativeTheme::ExtraParams const&) const ???:0
    #9 0x7f6849411e51 in webkit_glue::WebThemeEngineImpl::paint(SkCanvas*, WebKit::WebThemeEngine::Part, WebKit::WebThemeEngine::State, WebKit::WebRect const&, WebKit::WebThemeEngine::ExtraParams const*) ???:0
    #10 0x7f6849f81d07 in WebCore::PlatformSupport::paintThemePart(WebCore::GraphicsContext*, WebCore::PlatformSupport::ThemePart, WebCore::PlatformSupport::ThemePaintState, WebCore::IntRect const&, WebCore::PlatformSupport::ThemePaintExtraParams const*) ???:0
.
.
.


## Attachments

- [chrome-heap-buffer-overflow-SkAAClipBlitterblitAntiH-6ba.html](attachments/chrome-heap-buffer-overflow-SkAAClipBlitterblitAntiH-6ba.html) (text/html; charset=us-ascii, 733 B)
- [chrome-heap-buffer-overflow-SkAAClipBlitterblitAntiH-e4a.html](attachments/chrome-heap-buffer-overflow-SkAAClipBlitterblitAntiH-e4a.html) (text/html; charset=us-ascii, 19.9 KB)

## Timeline

### in...@chromium.org (2012-09-12)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=108136450

Uploader: kenrb@chromium.org

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x7fc327d0199e
Crash State:
  - crash stack -
  SkAAClipBlitter::blitAntiH
  vertish
  do_anti_hairline
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=145124:145129

Minimized Testcase (0.33 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv95jc4kOiqMRjneYKxi7vo8ww7YQ29S_Y5wZ3j4GYQac9W_VycPosqKSwEFVrx9uDi1aUqy5Pz5Bs8aFuV9xvW_O3InN1aDxM2MD4D7LlaMmqhLNe7VCIMU_azDYF7R1cDXrOXql13Ln8aDmNQ7vlack50X9_oPTfViYrjnfCBKeufdYTTY
<style>
.r{direction:rtl;</style>
<p class=r>
<input type=checkbox class=x1>
<script> 
var styleSheet0 = document.styleSheets[0];

styleSheet0.insertRule(".r{border-bottom-right-radius:25px; }",styleSheet0.cssRules.length);
styleSheet0.insertRule(".x1,.r{overflow-x:scroll; }",0);

document.body.style.zoom=0.3108934951014817
</script>

### in...@chromium.org (2012-09-12)

[Empty comment from Monorail migration]

### ke...@chromium.org (2012-09-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-10-14)

Mass move from m21 to m22.

### cl...@chromium.org (2012-10-14)

ClusterFuzz has detected this issue as fixed in range 161714:161730.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=108136450

Uploader: kenrb@chromium.org

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x7fc327d0199e
Crash State:
  - crash stack -
  SkAAClipBlitter::blitAntiH
  vertish
  do_anti_hairline
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=145124:145129
Fixed: https://cluster-fuzz.appspot.com/revisions?range=161714:161730

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95jc4kOiqMRjneYKxi7vo8ww7YQ29S_Y5wZ3j4GYQac9W_VycPosqKSwEFVrx9uDi1aUqy5Pz5Bs8aFuV9xvW_O3InN1aDxM2MD4D7LlaMmqhLNe7VCIMU_azDYF7R1cDXrOXql13Ln8aDmNQ7vlack50X9_oPTfViYrjnfCBKeufdYTTY

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### cl...@chromium.org (2012-10-14)

ClusterFuzz has detected this issue as fixed in range 161714:161730.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=108136450

Uploader: kenrb@chromium.org

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x7fc327d0199e
Crash State:
  - crash stack -
  SkAAClipBlitter::blitAntiH
  vertish
  do_anti_hairline
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=145124:145129
Fixed: https://cluster-fuzz.appspot.com/revisions?range=161714:161730

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95jc4kOiqMRjneYKxi7vo8ww7YQ29S_Y5wZ3j4GYQac9W_VycPosqKSwEFVrx9uDi1aUqy5Pz5Bs8aFuV9xvW_O3InN1aDxM2MD4D7LlaMmqhLNe7VCIMU_azDYF7R1cDXrOXql13Ln8aDmNQ7vlack50X9_oPTfViYrjnfCBKeufdYTTY

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2012-10-14)

Attekett, can you still reproduce this ? or you have another repro to trigger this.

From fixed range, i am guessing https://trac.webkit.org/changeset/131202/ fixed it or it might be just hiding the problem.

### at...@gmail.com (2012-10-14)


Didn't reproduce with the repro-file attached in here but one of the other old repro-files still reproduces for me. I added it as an attachment, but didn't minimize it yet.



### in...@chromium.org (2012-10-14)

Thanks Attekett. I just uploaded your repro to ClusterFuzz and it reproduces. 

Elliot, can you please try reproducing using the new repro. CF report in https://cluster-fuzz.appspot.com/testcase?key=126101723



### in...@chromium.org (2012-10-14)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=126101723

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x7f9dc395bd96
Crash State:
  - crash stack -
  SkAAClipBlitter::blitAntiH
  vertish
  do_anti_hairline
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=160096:160110

Minimized Testcase (0.60 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96QbhLRSSa7GgCQaqMdVsd9Vbvqd-vZhsEuTzpypQU8P3afWd81h8CervY6qfcfOCWoRNW87o7_Ibi4NEAo-VrirTdaMxjwZhRx8RONLaPGXgTaD2gb8QEMp6iAFvGcmFvHSrHduovAf0bNim7MPwEZVGGtQraiXYqkJ1NLc4xi9-sFKAo

### in...@chromium.org (2012-10-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-10-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-10-31)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=134149520

Fuzzer: Inferno_twister

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x7f50b93dc4d8
Crash State:
  - crash stack -
  SkAAClipBlitter::blitAntiH
  Vertish_SkAntiHairBlitter::drawCap
  do_anti_hairline
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=160096:160110

Minimized Testcase (2.02 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96kum8R7hdKqdRvD7wQCYB39PxRGmB_fq7JutjBwJhZTFzaonG0w7ZyKGX96TqSUErAs-3bgIIevJGVBzqWYRGvZ9Ati46cH-MOmcYJ76kQHuMSRKoHVB3tykG9OfO8mGh-VpW2jt18kmk6AbZ7arhaPvJFTulYPD0zC0qEMRdslI3T6Lo

Additional requirements: Requires HTTP

### in...@chromium.org (2012-10-31)

Mike, can you please help with an owner for this one. It still reproduces after the other fixes, and is now discovered both internally and externally.

### [Deleted User] (2012-10-31)

elliot, can you assist in trying to repro?

I have a (very) speculative fix in skia rev. 6220.


### cl...@chromium.org (2012-11-02)

ClusterFuzz has detected this issue as fixed in range 165369:165445.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=126101723

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x7f9dc395bd96
Crash State:
  - crash stack -
  SkAAClipBlitter::blitAntiH
  vertish
  do_anti_hairline
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=160096:160110
Fixed: https://cluster-fuzz.appspot.com/revisions?range=165369:165445

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96QbhLRSSa7GgCQaqMdVsd9Vbvqd-vZhsEuTzpypQU8P3afWd81h8CervY6qfcfOCWoRNW87o7_Ibi4NEAo-VrirTdaMxjwZhRx8RONLaPGXgTaD2gb8QEMp6iAFvGcmFvHSrHduovAf0bNim7MPwEZVGGtQraiXYqkJ1NLc4xi9-sFKAo

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### [Deleted User] (2012-11-02)

[Empty comment from Monorail migration]

### ep...@google.com (2012-11-02)

I see 3 clusterfuzz repro cases listed above:

https://cluster-fuzz.appspot.com/testcase?key=108136450 : fixed as of Oct 14

https://cluster-fuzz.appspot.com/testcase?key=126101723 : fixed as of today, probably by https://code.google.com/p/skia/source/detail?r=6220

https://cluster-fuzz.appspot.com/testcase?key=134149520 : not fixed yet

I will focus on reproducing the last one.

### in...@chromium.org (2012-11-02)

Last one might be fixed as well. CF picks up builds to check once per day, so probably it didnt happen yet for https://cluster-fuzz.appspot.com/testcase?key=134149520. I explicitly clicked redo, so we should know the result in 2-3 hrs.

### ep...@google.com (2012-11-02)

Thanks.  I'll get back to working the other fires of the day; I have made a note on my calendar to check in on this Monday.

### cl...@chromium.org (2012-11-02)

ClusterFuzz has detected this issue as fixed in range 165369:165445.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=134149520

Fuzzer: Inferno_twister

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x7f50b93dc4d8
Crash State:
  - crash stack -
  SkAAClipBlitter::blitAntiH
  Vertish_SkAntiHairBlitter::drawCap
  do_anti_hairline
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=160096:160110
Fixed: https://cluster-fuzz.appspot.com/revisions?range=165369:165445

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96kum8R7hdKqdRvD7wQCYB39PxRGmB_fq7JutjBwJhZTFzaonG0w7ZyKGX96TqSUErAs-3bgIIevJGVBzqWYRGvZ9Ati46cH-MOmcYJ76kQHuMSRKoHVB3tykG9OfO8mGh-VpW2jt18kmk6AbZ7arhaPvJFTulYPD0zC0qEMRdslI3T6Lo

Additional requirements: Requires HTTP

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2012-11-02)

https://code.google.com/p/skia/source/detail?r=6220 matches the fixed range - Skia	 r6209:r6227

### ka...@google.com (2012-11-12)

[Empty comment from Monorail migration]

### [Deleted User] (2012-11-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-11-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-11-13)

M23: https://code.google.com/p/skia/source/detail?r=6383
M24: https://code.google.com/p/skia/source/detail?r=6387

### sc...@gmail.com (2012-12-04)

Thanks @attekett - OOB read in Skia => $500 !

### sc...@gmail.com (2012-12-14)

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

This issue was migrated from crbug.com/chromium/148638?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Skia]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40073272)*
