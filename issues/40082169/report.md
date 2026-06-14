# Heap-use-after-free in SkCreateBitmapShader

| Field | Value |
|-------|-------|
| **Issue ID** | [40082169](https://issues.chromium.org/issues/40082169) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Platforms** | Linux |
| **Reporter** | cl...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2015-05-26 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached testcase crashes the latest 64-bit build of filter\_fuzz\_stub as follows:

=================================================================  

==3368==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60400000d9c4 at pc 0x00000053f40f bp 0x7fffb4b08b90 sp 0x7fffb4b08b88  

READ of size 4 at 0x60400000d9c4 thread T0  

#0 0x53f40e in SkColorTable::operator const /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/include/core/SkColorTable.h:43  

#1 0x7f8998 in canUseColorShader(SkBitmap const&, unsigned int\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkBitmapProcShader.cpp:292  

#2 0x7f8316 in SkCreateBitmapShader(SkBitmap const&, SkShader::TileMode, SkShader::TileMode, SkMatrix const\*, SkSmallAllocator<3u, 1024ul>\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkBitmapProcShader.cpp:322  

#3 0x7f10b6 in SkBitmapDevice::drawBitmapRect(SkDraw const&, SkBitmap const&, SkRect const\*, SkRect const&, SkPaint const&, SkCanvas::DrawBitmapRectFlags) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkBitmapDevice.cpp:304  

#4 0x554ae5 in SkCanvas::internalDrawBitmapRect(SkBitmap const&, SkRect const\*, SkRect const&, SkPaint const\*, SkCanvas::DrawBitmapRectFlags) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:2069  

#5 0x554fec in SkCanvas::onDrawBitmapRect(SkBitmap const&, SkRect const\*, SkRect const&, SkPaint const\*, SkCanvas::DrawBitmapRectFlags) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:2079  

#6 0x54ed19 in SkCanvas::drawBitmapRectToRect(SkBitmap const&, SkRect const\*, SkRect const&, SkPaint const\*, SkCanvas::DrawBitmapRectFlags) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:1761  

#7 0x9cb2b0 in SkBitmapSource::onFilterImage(SkImageFilter::Proxy\*, SkBitmap const&, SkImageFilter::Context const&, SkBitmap\*, SkIPoint\*) const /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/SkBitmapSource.cpp:87  

#8 0x5964a9 in SkImageFilter::filterImage(SkImageFilter::Proxy\*, SkBitmap const&, SkImageFilter::Context const&, SkBitmap\*, SkIPoint\*) const /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkImageFilter.cpp:189  

#9 0x546929 in SkCanvas::internalDrawDevice(SkBaseDevice\*, int, int, SkPaint const\*, bool) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:1233  

#10 0x5430ab in SkCanvas::internalRestore() /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:1098  

#11 0x548fc8 in AutoDrawLooper::~AutoDrawLooper() /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:402  

#12 0x547740 in SkCanvas::internalDrawBitmap(SkBitmap const&, SkMatrix const&, SkPaint const\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:1208  

#13 0x55441e in SkCanvas::onDrawBitmap(SkBitmap const&, float, float, SkPaint const\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:2039  

#14 0x54a3d5 in SkCanvas::drawBitmap(SkBitmap const&, float, float, SkPaint const\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:1753  

#15 0x4c9806 in RunTestCase /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:47  

#16 0x4c8bb9 in ReadAndRunTestCase /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:66  

#17 0x4c8713 in main /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:85  

#18 0x7f70894caec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

0x60400000d9c4 is located 12 bytes to the left of 40-byte region [0x60400000d9d0,0x60400000d9f8)  

allocated by thread T0 here:  

#0 0x4a842b in \_\_interceptor\_malloc ??:?  

#1 0x7f708b11a610 in g\_malloc ??:?

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/nils/MonkeyChrome/asan-symbolized-linux-release-331246/filter\_fuzz\_stub+0x53f40e)  

Shadow bytes around the buggy address:  

0x0c087fff9ae0: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fd  

0x0c087fff9af0: fa fa 00 00 00 00 00 fa fa fa 00 00 00 00 00 fa  

0x0c087fff9b00: fa fa 00 00 00 00 00 fa fa fa 00 00 00 00 00 fa  

0x0c087fff9b10: fa fa 00 00 00 00 00 fa fa fa 00 00 00 00 00 fa  

0x0c087fff9b20: fa fa 00 00 00 00 00 fa fa fa 00 00 00 00 00 00  

=>0x0c087fff9b30: fa fa 00 00 00 00 00 fa[fa]fa 00 00 00 00 00 fa  

0x0c087fff9b40: fa fa 00 00 00 00 00 fa fa fa 00 00 00 00 00 fa  

0x0c087fff9b50: fa fa 00 00 00 00 00 fa fa fa 00 00 00 00 00 fa  

0x0c087fff9b60: fa fa 00 00 00 00 00 fa fa fa 00 00 00 00 00 fa  

0x0c087fff9b70: fa fa 00 00 00 00 00 fa fa fa 00 00 00 00 00 fa  

0x0c087fff9b80: fa fa 00 00 00 00 00 fa fa fa 00 00 00 00 00 fa  

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

==3368==ABORTING

**VERSION**  

Chrome Version: asan-symbolized-linux-release-331246

**REPRODUCTION CASE**  

Attached as repro.fil

## Attachments

- [repro.fil](attachments/repro.fil) (application/octet-stream, 184 B)

## Timeline

### cl...@chromium.org (2015-05-26)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5171087403384832

### cl...@chromium.org (2015-05-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-26)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5171087403384832

Uploader: mbarbella@google.com
Job Type: Linux_asan_filter_fuzz_stub

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60b0000095b4
Crash State:
  SkCreateBitmapShader
  SkBitmapDevice::drawBitmapRect
  SkCanvas::internalDrawBitmapRect
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub&range=324625:324677

Minimized Testcase (0.18 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94oHKl96U-EFFIzcnulloHQEuPl7aKJ2qDK4hH4_xMRB0hgBmFZwKmMwfgt7Ai3nG3LA0uOldVAAh23JrfX3j0f6cO5Y1FrzJF2hSv54jsc8Wv-6X0C0Fe5YrJCJ0WdaqCXji66XfurHBUZ91Ed5EpFHZuvfg



### np...@chromium.org (2015-05-27)

The suspected CL does look plausible:
https://chromium.googlesource.com/skia.git/+/25c40d25d75c8ee5d9632608ba09eb2c5fb765d2

Marking security_impact-medium since the read would likely only return a bad ARGB (int32) color.

### cl...@chromium.org (2015-05-27)

[Empty comment from Monorail migration]

### oc...@chromium.org (2015-06-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-03)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### am...@chromium.org (2015-06-03)

Looks like a Linux issue, please add additional platforms if applicable.

### bu...@chromium.org (2015-06-08)

The following revision refers to this bug:
  https://skia.googlesource.com/skia.git/+/28937843f49b3015e9f4c04e04eb2604c3f873cf

commit 28937843f49b3015e9f4c04e04eb2604c3f873cf
Author: robertphillips <robertphillips@google.com>
Date: Mon Jun 08 14:10:49 2015

Cap color index values

In the provided example the color table has 10 entries but some of the pixels in the bitmap overflow. This CL goes through the pixel values and caps them to the max index.

An alternate approach would be to just have the color table always have 256 entries but zero out the unused ones.

BUG=492265

Review URL: https://codereview.chromium.org/1165493003

[modify] http://crrev.com/28937843f49b3015e9f4c04e04eb2604c3f873cf/src/core/SkBitmap.cpp


### in...@chromium.org (2015-06-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-09)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-07-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-09-15)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2016-04-22)

...and $1,000 for this report as well.

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

This issue was migrated from crbug.com/chromium/492265?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082169)*
