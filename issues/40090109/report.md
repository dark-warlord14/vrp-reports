# heap overflow read in filter_fuzz_stub

| Field | Value |
|-------|-------|
| **Issue ID** | [40090109](https://issues.chromium.org/issues/40090109) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | jo...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2018-01-06 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36

Steps to reproduce the problem:
1. asan-linux-release-527517
2. run ./filter_fuzz_stub path/to/poc

What is the expected behavior?
crashed by asan and report SEGV on unknown address (0x63108001c780)

What went wrong?
In SkMask.cpp: [SkMask::computeImageSize]
==============================================
SkMask::computeImageSize (this=0xffff96b0) at ../../src/third_party/skia/src/core/SkMask.cpp:26
26	    return safeMul32(fBounds.height(), fRowBytes);       <= int overflow
(gdb) p fRowBytes
$62 = 4294967040
(gdb) p fBounds
$63 = {fLeft = -2147483520, fTop = -2147483520, fRight = 2147483520, fBottom = 2147483520}
(gdb) p fBounds.fBottom - fBounds.fTop
$64 = -256
(gdb) p (fBounds.fBottom - fBounds.fTop) * (fRowBytes)
$65 = 65536
(gdb) n
SkLayerRasterizer::onRasterize (this=0x81beca0, path=..., matrix=..., clipBounds=0xffff95f8, 
    mask=0xffff96b0, mode=SkMask::kComputeBoundsAndRenderImage_CreateMode)
    at ../../src/third_party/skia/src/effects/SkLayerRasterizer.cpp:107
107	        if (0 == size) {
(gdb) i r eax
eax            0x10000	65536
(gdb)

==============================================
In SkMask.cpp:[SkMask::getAddr]
...
(gdb) 
91	    char* addr = (char*)fImage;
(gdb) p fRowBytes
$70 = 4294967040
(gdb) p fBounds
$71 = {fLeft = -2147483520, fTop = -2147483520, fRight = 2147483520, fBottom = 2147483520}
(gdb) x/4xw fImage
0x81e3010:	0x00000000	0x00000000	0x00000000	0x00000000
92	    addr += (y - fBounds.fTop) * fRowBytes;
(gdb) n
93	    addr += (x - fBounds.fLeft) << maskFormatToShift(fFormat);
(gdb) x/4xw addr
0x81eb010:	0x00000000	0x00000000	0x00000000	0x00000000
(gdb) n
94	    return addr;
(gdb) x/4xw addr
0x881eaf90:	Cannot access memory at address 0x881eaf90

Did this work before? N/A 

Chrome version: latest build of filter_fuzz_stub  Channel: n/a
OS Version: Ubuntu 16.04 LTS X64
Flash Version: 

[0106/225051.989708:INFO:filter_fuzz_stub.cc(61)] Test case: path/to/poc
[0106/225051.989931:INFO:filter_fuzz_stub.cc(38)] Valid stream detected.
AddressSanitizer:DEADLYSIGNAL
=================================================================
==13347==ERROR: AddressSanitizer: SEGV on unknown address 0x63108001c780 (pc 0x000000ad0b23 bp 0x7fffce345730 sp 0x7fffce345600 T0)
==13347==The signal is caused by a READ memory access.
    #0 0xad0b22 in void (anonymous namespace)::Sk4px::MapDstSrcAlpha<(anonymous namespace)::Sk4px ((anonymous namespace)::Sk4px const&, (anonymous namespace)::Sk4px const&, (anonymous namespace)::Sk4px const&)>(int, unsigned int*, unsigned int const*, unsigned char const*, (anonymous namespace)::Sk4px ( const&)((anonymous namespace)::Sk4px const&, (anonymous namespace)::Sk4px const&, (anonymous namespace)::Sk4px const&)) third_party/skia/src/core/Sk4px.h
    #1 0xa5e7da in SkARGB32_Shader_Blitter::blitMask(SkMask const&, SkIRect const&) third_party/skia/src/core/SkBlitter_ARGB32.cpp:568:19
    #2 0xa4cb24 in SkBlitter::blitMaskRegion(SkMask const&, SkRegion const&) third_party/skia/src/core/SkBlitter.cpp:323:15
    #3 0xa2433e in SkDraw::drawDevMask(SkMask const&, SkPaint const&) const third_party/skia/src/core/SkDraw.cpp:864:14
    #4 0xa25b12 in SkDraw::drawPath(SkPath const&, SkPaint const&, SkMatrix const*, bool, bool, SkBlitter*) const third_party/skia/src/core/SkDraw.cpp:1118:19
    #5 0xa23d2e in drawPath third_party/skia/src/core/SkDraw.h:56:15
    #6 0xa23d2e in draw_rect_as_path(SkDraw const&, SkRect const&, SkPaint const&, SkMatrix const*) third_party/skia/src/core/SkDraw.cpp:732
    #7 0xa22ba5 in SkDraw::drawRect(SkRect const&, SkPaint const&, SkMatrix const*, SkRect const*) const third_party/skia/src/core/SkDraw.cpp:759:9
    #8 0x9d2a8c in drawRect third_party/skia/src/core/SkDraw.h:42:15
    #9 0x9d2a8c in SkBitmapDevice::drawRect(SkRect const&, SkPaint const&) third_party/skia/src/core/SkBitmapDevice.cpp:195
    #10 0x9b96b9 in SkCanvas::onDrawRect(SkRect const&, SkPaint const&) third_party/skia/src/core/SkCanvas.cpp:2029:27
    #11 0x9afa0f in SkCanvas::drawRect(SkRect const&, SkPaint const&) third_party/skia/src/core/SkCanvas.cpp:1710:11
    #12 0xe3aa59 in SkPaintImageFilter::onFilterImage(SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const third_party/skia/src/effects/SkPaintImageFilter.cpp:66:13
    #13 0xa78279 in SkImageFilter::filterImage(SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const third_party/skia/src/core/SkImageFilter.cpp:213:40
    #14 0x9d60dc in SkBitmapDevice::drawSpecial(SkSpecialImage*, int, int, SkPaint const&, SkImage*, SkMatrix const&) third_party/skia/src/core/SkBitmapDevice.cpp:421:33
    #15 0x9a674a in SkCanvas::internalDrawDevice(SkBaseDevice*, int, int, SkPaint const*, SkImage*, SkMatrix const&) third_party/skia/src/core/SkCanvas.cpp:1313:25
    #16 0x9a17ff in SkCanvas::internalRestore() third_party/skia/src/core/SkCanvas.cpp:1201:19
    #17 0x9c13e4 in ~AutoDrawLooper third_party/skia/src/core/SkCanvas.cpp:495:22
    #18 0x9c13e4 in SkCanvas::onDrawBitmap(SkBitmap const&, float, float, SkPaint const*) third_party/skia/src/core/SkCanvas.cpp:2308
    #19 0x9b428f in SkCanvas::drawBitmap(SkBitmap const&, float, float, SkPaint const*) third_party/skia/src/core/SkCanvas.cpp:1831:11
    #20 0x62d3cc in RunTestCase skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:48:13
    #21 0x62d3cc in ReadAndRunTestCase skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:67
    #22 0x62d3cc in main skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:87
    #23 0x7f95dac4282f in __libc_start_main /build/glibc-bfm8X4/glibc-2.23/csu/../csu/libc-start.c:291

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV third_party/skia/src/core/Sk4px.h in void (anonymous namespace)::Sk4px::MapDstSrcAlpha<(anonymous namespace)::Sk4px ((anonymous namespace)::Sk4px const&, (anonymous namespace)::Sk4px const&, (anonymous namespace)::Sk4px const&)>(int, unsigned int*, unsigned int const*, unsigned char const*, (anonymous namespace)::Sk4px ( const&)((anonymous namespace)::Sk4px const&, (anonymous namespace)::Sk4px const&, (anonymous namespace)::Sk4px const&))
==13347==ABORTING

## Attachments

- [poc_01](attachments/poc_01) (text/plain, 360 B)

## Timeline

### jo...@gmail.com (2018-01-06)

I think this issue may also lead to cross-border write operation，if confirmed, I will update analysis and poc file;

### cl...@chromium.org (2018-01-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4573317918097408.

### me...@chromium.org (2018-01-07)

[Empty comment from Monorail migration]

[Monorail components: Internals>Skia]

### cl...@chromium.org (2018-01-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6572413667246080.

### sh...@chromium.org (2018-01-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-07)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-01-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-01-07)

Detailed report: https://clusterfuzz.com/testcase?key=6572413667246080

Job Type: linux_asan_filter_fuzz_stub
Crash Type: UNKNOWN READ
Crash Address: 0x63108001c780
Crash State:
  void Sk4px::MapDstSrcAlpha<Sk4px
  SkARGB32_Shader_Blitter::blitMask
  SkBlitter::blitMaskRegion
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_filter_fuzz_stub&range=526876:526881

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6572413667246080

See https://github.com/google/clusterfuzz-tools for more information.

### cl...@chromium.org (2018-01-07)

Automatically adding ccs based on suspected regression changelists:

Revert "Revert "remove legacy support for old old picture versions"" by reed@google.com - https://skia.googlesource.com/skia/+/c5166a9dcbf2eeb95cb8e2918271132aa34bf5cd

check for irect with overflow width/height by reed@google.com - https://skia.googlesource.com/skia/+/9fc53624a09f6d3378b0a540832571dc1c31fbcd

If this is incorrect, please apply the Test-Predator-Wrong-CLs label.

### re...@google.com (2018-01-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-01-09)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/a766ca9af12e1175cfb01f4b516802da9197ba78

commit a766ca9af12e1175cfb01f4b516802da9197ba78
Author: Mike Reed <reed@google.com>
Date: Tue Jan 09 16:54:52 2018

use 64bit math to compute is a rect is empty

Will work next to try to make isEmpty() private

Bug: skia:7470
Bug:799715
Change-Id: I7b43028ecd86dca68e0c67225712516d2f2f88a2
Reviewed-on: https://skia-review.googlesource.com/92620
Commit-Queue: Mike Reed <reed@google.com>
Reviewed-by: Brian Salomon <bsalomon@google.com>

[modify] https://crrev.com/a766ca9af12e1175cfb01f4b516802da9197ba78/src/core/SkRectPriv.h
[modify] https://crrev.com/a766ca9af12e1175cfb01f4b516802da9197ba78/docs/SkIRect_Reference.bmh
[modify] https://crrev.com/a766ca9af12e1175cfb01f4b516802da9197ba78/include/core/SkRect.h
[modify] https://crrev.com/a766ca9af12e1175cfb01f4b516802da9197ba78/src/core/SkRegion.cpp
[modify] https://crrev.com/a766ca9af12e1175cfb01f4b516802da9197ba78/src/core/SkAAClip.cpp
[modify] https://crrev.com/a766ca9af12e1175cfb01f4b516802da9197ba78/include/core/SkRegion.h


### cl...@chromium.org (2018-01-12)

ClusterFuzz has detected this issue as fixed in range 528693:528695.

Detailed report: https://clusterfuzz.com/testcase?key=6572413667246080

Job Type: linux_asan_filter_fuzz_stub
Crash Type: UNKNOWN READ
Crash Address: 0x63108001c780
Crash State:
  void Sk4px::MapDstSrcAlpha<Sk4px
  SkARGB32_Shader_Blitter::blitMask
  SkBlitter::blitMaskRegion
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_filter_fuzz_stub&range=526876:526881
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_filter_fuzz_stub&range=528693:528695

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6572413667246080

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-01-12)

ClusterFuzz testcase 6572413667246080 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-01-12)

[Empty comment from Monorail migration]

### aw...@google.com (2018-01-16)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-01-29)

Thanks for the report!  The VRP panel decided to award $1,000 for this report. 

Also, how would you like to be credited in the Chrome release notes?

### aw...@chromium.org (2018-01-29)

[Empty comment from Monorail migration]

### jo...@gmail.com (2018-02-03)

Thanks for your information.
Please credit this to Wanglu & Yangkang(@dnpushme) of Qihoo360 Qex Team.

### aw...@chromium.org (2018-02-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-04-20)

This issue was migrated from crbug.com/chromium/799715?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090109)*
