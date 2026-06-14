# Heap-buffer-overflow in SI8_opaque_D32_nofilter_DX

| Field | Value |
|-------|-------|
| **Issue ID** | [40082159](https://issues.chromium.org/issues/40082159) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Platforms** | Linux |
| **Reporter** | cl...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2015-05-25 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached testcase crashes the 64-bit build of filter\_fuzz\_stub as follows:

=================================================================  

==15196==ERROR: AddressSanitizer: heap-use-after-free on address 0x60400000d754 at pc 0x00000080037d bp 0x7fff56350700 sp 0x7fff563506f8  

READ of size 4 at 0x60400000d754 thread T0  

#0 0x80037c in SI8\_opaque\_D32\_nofilter\_DX(SkBitmapProcState const&, unsigned int const\*, int, unsigned int\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkBitmapProcState\_sample.h:119  

#1 0x7f7757 in SkBitmapProcShader::BitmapProcShaderContext::shadeSpan(int, int, unsigned int\*, int) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkBitmapProcShader.cpp:214  

#2 0x83ebf8 in SkARGB32\_Shader\_Blitter::blitRect(int, int, int, int) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkBlitter\_ARGB32.cpp:431  

#3 0x63d341 in SkScan::FillIRect(SkIRect const&, SkRegion const\*, SkBlitter\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkScan.cpp:43  

#4 0x63daf5 in SkScan::FillRect(SkRect const&, SkRegion const\*, SkBlitter\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkScan.cpp:61  

#5 0x63e230 in SkScan::FillRect(SkRect const&, SkRasterClip const&, SkBlitter\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkScan.cpp:103  

#6 0x57a583 in SkDraw::drawRect(SkRect const&, SkPaint const&, SkMatrix const\*, SkRect const\*) const /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkDraw.cpp:875  

#7 0x57e2a4 in SkDraw::drawBitmap(SkBitmap const&, SkMatrix const&, SkRect const\*, SkPaint const&) const /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkDraw.cpp:1307  

#8 0x7f1092 in SkBitmapDevice::drawBitmapRect(SkDraw const&, SkBitmap const&, SkRect const\*, SkRect const&, SkPaint const&, SkCanvas::DrawBitmapRectFlags) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkBitmapDevice.cpp:299  

#9 0x554ae5 in SkCanvas::internalDrawBitmapRect(SkBitmap const&, SkRect const\*, SkRect const&, SkPaint const\*, SkCanvas::DrawBitmapRectFlags) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:2069  

#10 0x554fec in SkCanvas::onDrawBitmapRect(SkBitmap const&, SkRect const\*, SkRect const&, SkPaint const\*, SkCanvas::DrawBitmapRectFlags) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:2079  

#11 0x54ed19 in SkCanvas::drawBitmapRectToRect(SkBitmap const&, SkRect const\*, SkRect const&, SkPaint const\*, SkCanvas::DrawBitmapRectFlags) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:1761  

#12 0x9cb2b0 in SkBitmapSource::onFilterImage(SkImageFilter::Proxy\*, SkBitmap const&, SkImageFilter::Context const&, SkBitmap\*, SkIPoint\*) const /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/SkBitmapSource.cpp:87  

#13 0x5964a9 in SkImageFilter::filterImage(SkImageFilter::Proxy\*, SkBitmap const&, SkImageFilter::Context const&, SkBitmap\*, SkIPoint\*) const /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkImageFilter.cpp:189  

#14 0x546929 in SkCanvas::internalDrawDevice(SkBaseDevice\*, int, int, SkPaint const\*, bool) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:1233  

#15 0x5430ab in SkCanvas::internalRestore() /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:1098  

#16 0x548fc8 in AutoDrawLooper::~AutoDrawLooper() /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:402  

#17 0x547740 in SkCanvas::internalDrawBitmap(SkBitmap const&, SkMatrix const&, SkPaint const\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:1208  

#18 0x55441e in SkCanvas::onDrawBitmap(SkBitmap const&, float, float, SkPaint const\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:2039  

#19 0x54a3d5 in SkCanvas::drawBitmap(SkBitmap const&, float, float, SkPaint const\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:1753  

#20 0x4c9806 in RunTestCase /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:47  

#21 0x4c8bb9 in ReadAndRunTestCase /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:66  

#22 0x4c8713 in main /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:85  

#23 0x7f7e68c6aec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

0x60400000d754 is located 4 bytes inside of 48-byte region [0x60400000d750,0x60400000d780)  

freed by thread T0 here:  

#0 0x4c7d4b in operator delete(void\*) ??:?  

#1 0x7f7e6960dac2 in **deallocate /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../buildtools/third\_party/libc++/trunk/include/new:164  

#2 0x7f7e6960cb32 in push\_back /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../buildtools/third\_party/libc++/trunk/include/string:2642  

#3 0x4d2dbe in overflow /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../buildtools/third\_party/libc++/trunk/include/sstream:528  

#4 0x7f7e694f09d3 in xsputn /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../buildtools/third\_party/libc++/trunk/include/streambuf:543  

#5 0x4ca3af in sputn /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../buildtools/third\_party/libc++/trunk/include/streambuf:360  

#6 0x4c9da4 in \_*put\_character\_sequence<char, std::**1::char\_traits<char> > /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../buildtools/third\_party/libc++/trunk/include/ostream:743  

#7 0x4c8b66 in ReadAndRunTestCase /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:60  

#8 0x4c8713 in main /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:85  

#9 0x7f7e68c6aec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

previously allocated by thread T0 here:  

#0 0x4c778b in operator new(unsigned long) ??:?  

#1 0x7f7e6960d9bd in **allocate /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../buildtools/third\_party/libc++/trunk/include/new:156  

#2 0x7f7e6960cb32 in push\_back /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../buildtools/third\_party/libc++/trunk/include/string:2642  

#3 0x4d2dbe in overflow /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../buildtools/third\_party/libc++/trunk/include/sstream:528  

#4 0x7f7e694f09d3 in xsputn /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../buildtools/third\_party/libc++/trunk/include/streambuf:543  

#5 0x7f7e69519ed2 in sputn /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../buildtools/third\_party/libc++/trunk/include/streambuf:360  

#6 0x4db6fa in base::operator<<(std::\_\_1::basic\_ostream<char, std::\_\_1::char\_traits<char> >&, base::BasicStringPiece<std::\_*1::basic\_string<char, std::**1::char\_traits<char>, std::**1::allocator<char> > > const&) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../base/strings/string\_piece.cc:47  

#7 0x4d614f in Init /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../base/logging.cc:683  

#8 0x4d59a6 in LogMessage /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../base/logging.cc:521  

#9 0x4c8b4f in ReadAndRunTestCase /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:60 (discriminator 1)  

#10 0x4c8713 in main /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:85  

#11 0x7f7e68c6aec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

SUMMARY: AddressSanitizer: heap-use-after-free (/home/nils/MonkeyChrome/asan-symbolized-linux-release-331246/filter\_fuzz\_stub+0x80037c)  

Shadow bytes around the buggy address:  

0x0c087fff9a90: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c087fff9aa0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c087fff9ab0: fa fa fa fa fa fa fa fa fa fa fd fd fd fd fd fd  

0x0c087fff9ac0: fa fa fd fd fd fd fd fd fa fa 00 00 00 00 00 fa  

0x0c087fff9ad0: fa fa 00 00 00 00 00 fa fa fa fd fd fd fd fd fd  

=>0x0c087fff9ae0: fa fa fd fd fd fd fd fd fa fa[fd]fd fd fd fd fd  

0x0c087fff9af0: fa fa 00 00 00 00 00 fa fa fa 00 00 00 00 00 fa  

0x0c087fff9b00: fa fa 00 00 00 00 00 fa fa fa 00 00 00 00 00 fa  

0x0c087fff9b10: fa fa 00 00 00 00 00 fa fa fa 00 00 00 00 00 fa  

0x0c087fff9b20: fa fa 00 00 00 00 00 fa fa fa 00 00 00 00 00 00  

0x0c087fff9b30: fa fa 00 00 00 00 00 fa fa fa 00 00 00 00 00 fa  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Heap right redzone: fb  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack partial redzone: f4  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

==15196==ABORTING

**VERSION**  

Chrome Version: asan-symbolized-linux-release-331246

**REPRODUCTION CASE**  

attached as repro.fil

## Attachments

- [repro.fil](attachments/repro.fil) (application/octet-stream, 164 B)

## Timeline

### cl...@chromium.org (2015-05-25)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6684471944806400

### cl...@chromium.org (2015-05-26)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6684471944806400

Uploader: mbarbella@google.com
Job Type: Linux_asan_filter_fuzz_stub

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x60b000009344
Crash State:
  SI8_opaque_D32_nofilter_DX
  SkBitmapProcShader::BitmapProcShaderContext::shadeSpan
  SkARGB32_Shader_Blitter::blitRect
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub&range=324625:324677

Minimized Testcase (0.16 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95RP_QGlBE7S7G9P3wG2lBvsGxsQ47OZ6J_qjqCuuWu1WqViCJwU-mqfLGNEljVKgrroaqcgkpjhvzEqMcKFMxrxEcHJ-prfkmvxF5Swe0qTeWzTruZx9cXSKKt9eAbovmRJue58_H6ATAuwGGx7U84AOb_iw



### cl...@chromium.org (2015-05-26)

[Empty comment from Monorail migration]

### rs...@chromium.org (2015-05-28)

mtklein: Could this be from https://chromium.googlesource.com/skia/+/c5e0891029bed0f9619d67281a81f13983a9687b ?

### cl...@chromium.org (2015-05-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-28)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### am...@chromium.org (2015-05-29)

Looks like this is Linux at least, please add additional OSes if applicable.

### [Deleted User] (2015-05-29)

possible fix : https://codereview.chromium.org/1155403003/

### bu...@chromium.org (2015-05-29)

The following revision refers to this bug:
  https://skia.googlesource.com/skia.git/+/f941a68126d8fe647eaea902c244c466568b7809

commit f941a68126d8fe647eaea902c244c466568b7809
Author: reed <reed@google.com>
Date: Fri May 29 18:39:14 2015

add asserts around results from requestLock and lockPixels, ensuring that true always means we have non-null pixels (and non-null colortable if that matches the colortype)

BUG= 491975
TBR=

Review URL: https://codereview.chromium.org/1155403003

[modify] http://crrev.com/f941a68126d8fe647eaea902c244c466568b7809/include/core/SkPixelRef.h
[modify] http://crrev.com/f941a68126d8fe647eaea902c244c466568b7809/src/core/SkPixelRef.cpp


### bu...@chromium.org (2015-05-29)

The following revision refers to this bug:
  https://skia.googlesource.com/skia.git/+/3953d360417655b8000df0951699121383db45c3

commit 3953d360417655b8000df0951699121383db45c3
Author: reed <reed@google.com>
Date: Fri May 29 21:22:05 2015

Revert of add asserts around results from requestLock (patchset #3 id:40001 of https://codereview.chromium.org/1155403003/)

Reason for revert:
asserts in ui/gfx unittests (need to investigate why)

[ RUN      ] RenderTextTest.SelectionKeepsLigatures
[14602:14602:0529/134016:16779526944:INFO:SkPixelRef.cpp(164)] ../../third_party/skia/src/core/SkPixelRef.cpp:164: failed assertion "pixels"

Original issue's description:
> add asserts around results from requestLock and lockPixels, ensuring that true always means we have non-null pixels (and non-null colortable if that matches the colortype)
>
> BUG= 491975
> TBR=
>
> Committed: https://skia.googlesource.com/skia/+/f941a68126d8fe647eaea902c244c466568b7809

TBR=scroggo@google.com
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG= 491975

Review URL: https://codereview.chromium.org/1159013006

[modify] http://crrev.com/3953d360417655b8000df0951699121383db45c3/include/core/SkPixelRef.h
[modify] http://crrev.com/3953d360417655b8000df0951699121383db45c3/src/core/SkPixelRef.cpp


### cl...@chromium.org (2015-06-09)

ClusterFuzz has detected this issue as fixed in range 333258:333283.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6684471944806400

Uploader: mbarbella@google.com
Job Type: Linux_asan_filter_fuzz_stub

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x60b000009344
Crash State:
  SI8_opaque_D32_nofilter_DX
  SkBitmapProcShader::BitmapProcShaderContext::shadeSpan
  SkARGB32_Shader_Blitter::blitRect
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub&range=324625:324677
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub&range=333258:333283

Minimized Testcase (0.16 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95RP_QGlBE7S7G9P3wG2lBvsGxsQ47OZ6J_qjqCuuWu1WqViCJwU-mqfLGNEljVKgrroaqcgkpjhvzEqMcKFMxrxEcHJ-prfkmvxF5Swe0qTeWzTruZx9cXSKKt9eAbovmRJue58_H6ATAuwGGx7U84AOb_iw

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### in...@chromium.org (2015-06-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-09)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-07-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-09-15)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2016-04-22)

Another $1,000 here (if you can demonstrate that this can lead to a write, we're happy to take it back through the panel).

### ti...@google.com (2016-04-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### is...@google.com (2018-01-22)

This issue was migrated from crbug.com/chromium/491975?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082159)*
