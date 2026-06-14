# Security:  stack-buffer-overflow in Break

| Field | Value |
|-------|-------|
| **Issue ID** | [40091589](https://issues.chromium.org/issues/40091589) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | zh...@gmail.com |
| **Assignee** | re...@google.com |
| **Created** | 2018-06-07 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

This issue was found by fuzzing against a 64-bit asan linux build of filter\_fuzz\_stub.

**VERSION**  

Chrome Version: beta-67.0.3396.62  

Operating System: Fedora 28 x86\_64

<https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-beta-67.0.3396.62.zip>

**REPRODUCTION CASE**

# filter\_fuzz\_stub /tmp/id:013145,RUWLKAE0MPVZ [0607/085808.175722:INFO:filter\_fuzz\_stub.cc(60)] Test case: /tmp/id:013145,RUWLKAE0MPVZ [0607/085808.214440:INFO:filter\_fuzz\_stub.cc(37)] Valid stream detected.

==14542==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7f92def3793e at pc 0x000000623b73 bp 0x7ffe61dc7390 sp 0x7ffe61dc7388  

WRITE of size 1 at 0x7f92def3793e thread T0  

#0 0x623b72 in Break third\_party/skia/src/core/SkAntiRun.h:154:26  

#1 0x623b72 in SkRgnClipBlitter::blitAntiH(int, int, unsigned char const\*, short const\*) third\_party/skia/src/core/SkBlitter.cpp:556  

#2 0x5f5680 in SkBlitter::blitAntiH2(int, int, unsigned int, unsigned int) third\_party/skia/src/core/SkBlitter.h:96:15  

#3 0x8bbf6a in aaa\_walk\_convex\_edges third\_party/skia/src/core/SkScan\_AAAPath.cpp  

#4 0x8bbf6a in aaa\_fill\_path third\_party/skia/src/core/SkScan\_AAAPath.cpp:1670  

#5 0x8bbf6a in SkScan::AAAFillPath(SkPath const&, SkBlitter\*, SkIRect const&, SkIRect const&, bool) third\_party/skia/src/core/SkScan\_AAAPath.cpp:1714  

#6 0x8e5265 in SkScan::AntiFillPath(SkPath const&, SkRegion const&, SkBlitter\*, bool, SkDAARecord\*) third\_party/skia/src/core/SkScan\_AntiPath.cpp:807:9  

#7 0x8e6cca in SkScan::AntiFillPath(SkPath const&, SkRasterClip const&, SkBlitter\*, SkDAARecord\*) third\_party/skia/src/core/SkScan\_AntiPath.cpp:846:9  

#8 0x6e1204 in SkDraw::drawDevPath(SkPath const&, SkPaint const&, bool, SkBlitter\*, bool, SkInitOnceData\*) const third\_party/skia/src/core/SkDraw.cpp:1022:9  

#9 0x6e2b4d in SkDraw::drawPath(SkPath const&, SkPaint const&, SkMatrix const\*, bool, bool, SkBlitter\*, SkInitOnceData\*) const third\_party/skia/src/core/SkDraw.cpp:1136:11  

#10 0x6e01e8 in drawPath third\_party/skia/src/core/SkDraw.h:58:15  

#11 0x6e01e8 in draw\_rect\_as\_path(SkDraw const&, SkRect const&, SkPaint const&, SkMatrix const\*) third\_party/skia/src/core/SkDraw.cpp:739  

#12 0x6df505 in SkDraw::drawRect(SkRect const&, SkPaint const&, SkMatrix const\*, SkRect const\*) const third\_party/skia/src/core/SkDraw.cpp:766:9  

#13 0x6e51de in SkDraw::drawBitmap(SkBitmap const&, SkMatrix const&, SkRect const\*, SkPaint const&) const third\_party/skia/src/core/SkDraw.h  

#14 0x6081cc in SkBitmapDevice::drawBitmap(SkBitmap const&, SkMatrix const&, SkRect const\*, SkPaint const&) third\_party/skia/src/core/SkBitmapDevice.cpp:352:5  

#15 0x607ee4 in SkBitmapDevice::drawBitmap(SkBitmap const&, float, float, SkPaint const&) third\_party/skia/src/core/SkBitmapDevice.cpp:347:11  

#16 0x6cf45b in SkBaseDevice::drawImage(SkImage const\*, float, float, SkPaint const&) third\_party/skia/src/core/SkDevice.cpp:188:15  

#17 0x66d5ff in SkCanvas::onDrawImage(SkImage const\*, float, float, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:2177:27  

#18 0x661b70 in SkCanvas::drawImage(SkImage const\*, float, float, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:1691:11  

#19 0x854284 in draw[SkRecords::DrawImage](javascript:void(0);) third\_party/skia/src/core/SkRecordDraw.cpp:96:1  

#20 0x854284 in operator()[SkRecords::DrawImage](javascript:void(0);) third\_party/skia/src/core/SkRecordDraw.h:62  

#21 0x854284 in decltype ({parm#1}((SkRecords::NoOp)())) SkRecord::Record::visit[SkRecords::Draw&](javascript:void(0);)(SkRecords::Draw&) const third\_party/skia/src/core/SkRecord.h:165  

#22 0x85243a in visit<SkRecords::Draw &> third\_party/skia/src/core/SkRecord.h:42:28  

#23 0x85243a in SkRecordDraw(SkRecord const&, SkCanvas\*, SkPicture const\* const\*, SkDrawable\* const\*, int, SkBBoxHierarchy const\*, SkPicture::AbortCallback\*) third\_party/skia/src/core/SkRecordDraw.cpp:52  

#24 0x5f9d2f in SkBigPicture::playback(SkCanvas\*, SkPicture::AbortCallback\*) const third\_party/skia/src/core/SkBigPicture.cpp:33:5  

#25 0x67b2dd in SkCanvas::onDrawPicture(SkPicture const\*, SkMatrix const\*, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:2771:14  

#26 0x67ab9f in SkCanvas::drawPicture(SkPicture const\*, SkMatrix const\*, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:2751:15  

#27 0xafd3ea in drawPicture third\_party/skia/include/core/SkCanvas.h:2128:15  

#28 0xafd3ea in drawPicture third\_party/skia/include/core/SkCanvas.h:2140  

#29 0xafd3ea in SkPictureImageFilter::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkPictureImageFilter.cpp:118  

#30 0x731e30 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:213:40  

#31 0x737390 in SkImageFilter::filterInput(int, SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:514:41  

#32 0xae7bed in SkMergeImageFilter::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkMergeImageFilter.cpp:47:27  

#33 0x731e30 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:213:40  

#34 0x737390 in SkImageFilter::filterInput(int, SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:514:41  

#35 0xa9854b in SkColorFilterImageFilter::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkColorFilterImageFilter.cpp:65:39  

#36 0x731e30 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:213:40  

#37 0x60aea4 in SkBitmapDevice::drawSpecial(SkSpecialImage\*, int, int, SkPaint const&, SkImage\*, SkMatrix const&) third\_party/skia/src/core/SkBitmapDevice.cpp:550:33  

#38 0x657b0d in SkCanvas::internalDrawDevice(SkBaseDevice\*, int, int, SkPaint const\*, SkImage\*, SkMatrix const&) third\_party/skia/src/core/SkCanvas.cpp:1237:25  

#39 0x653a90 in SkCanvas::internalRestore() third\_party/skia/src/core/SkCanvas.cpp:1125:19  

#40 0x66f21b in ~AutoDrawLooper third\_party/skia/src/core/SkCanvas.cpp:429:22  

#41 0x66f21b in SkCanvas::onDrawBitmap(SkBitmap const&, float, float, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:2259  

#42 0x663a83 in SkCanvas::drawBitmap(SkBitmap const&, float, float, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:1765:11  

#43 0x5e9008 in RunTestCase skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:47:13  

#44 0x5e9008 in ReadAndRunTestCase skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:66  

#45 0x5e9008 in main skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:86  

#46 0x7f92e2e8a82f in \_\_libc\_start\_main /build/glibc-bfm8X4/glibc-2.23/csu/../csu/libc-start.c:291

Address 0x7f92def3793e is located in stack of thread T0 at offset 62 in frame  

#0 0x5f54ff in SkBlitter::blitAntiH2(int, int, unsigned int, unsigned int) third\_party/skia/src/core/SkBlitter.h:87

This frame has 2 object(s):  

[32, 38) 'runs' (line 88)  

[64, 66) 'aa' (line 89) <== Memory access at offset 62 underflows this variable  

HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork  

(longjmp and C++ exceptions \*are\* supported)  

SUMMARY: AddressSanitizer: stack-buffer-overflow third\_party/skia/src/core/SkAntiRun.h:154:26 in Break  

Shadow bytes around the buggy address:  

0x0ff2dbddeed0: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x0ff2dbddeee0: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x0ff2dbddeef0: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x0ff2dbddef00: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x0ff2dbddef10: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

=>0x0ff2dbddef20: f1 f1 f1 f1 06 f2 f2[f2]02 f3 f3 f3 00 00 00 00  

0x0ff2dbddef30: f1 f1 f1 f1 00 00 00 f2 f2 f2 f2 f2 04 f2 04 f3  

0x0ff2dbddef40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0ff2dbddef50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0ff2dbddef60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0ff2dbddef70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

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

==14542==ABORTING

## Attachments

- [id:013145,RUWLKAE0MPVZ](attachments/id_013145,RUWLKAE0MPVZ) (text/plain, 2.6 KB)

## Timeline

### zh...@gmail.com (2018-06-07)

Confirmed it also affect latest stable release.

https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-stable-67.0.3396.62.zip



### aa...@google.com (2018-06-07)

[Empty comment from Monorail migration]

[Monorail components: Internals>Skia]

### cl...@chromium.org (2018-06-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4786318371192832.

### pa...@chromium.org (2018-06-07)

[Empty comment from Monorail migration]

### kj...@chromium.org (2018-06-07)

reed@ is working on a fix. 

I confirmed it repros recently, although it doesn't after https://skia-review.googlesource.com/c/skia/+/130543 because the serialized format changes slightly.

### zh...@gmail.com (2018-06-12)

Confirmed it also affect latest stable release.

https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-stable-67.0.3396.79.zip

### zh...@gmail.com (2018-06-12)

It also affect the latest beta asan release.

https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-beta-68.0.3440.17.zip

~/asan-linux-beta-68.0.3440.17$ ./filter_fuzz_stub id:013145,RUWLKAE0MPVZ

[0612/155345.022292:INFO:filter_fuzz_stub.cc(60)] Test case: /tmp/id:013145,RUWLKAE0MPVZ
[0612/155345.041367:INFO:filter_fuzz_stub.cc(37)] Valid stream detected.
=================================================================
==18047==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7f5d4b27963e at pc 0x000000655c54 bp 0x7fffa60c0bb0 sp 0x7fffa60c0ba8
WRITE of size 1 at 0x7f5d4b27963e thread T0
    #0 0x655c53 in Break third_party/skia/src/core/SkAntiRun.h:154:26
    #1 0x655c53 in SkRgnClipBlitter::blitAntiH(int, int, unsigned char const*, short const*) third_party/skia/src/core/SkBlitter.cpp:619
    #2 0x625170 in SkBlitter::blitAntiH2(int, int, unsigned int, unsigned int) third_party/skia/src/core/SkBlitter.h:95:15
    #3 0x8f1d44 in aaa_walk_convex_edges third_party/skia/src/core/SkScan_AAAPath.cpp
    #4 0x8f1d44 in aaa_fill_path third_party/skia/src/core/SkScan_AAAPath.cpp:1658
    #5 0x8f1d44 in SkScan::AAAFillPath(SkPath const&, SkBlitter*, SkIRect const&, SkIRect const&, bool) third_party/skia/src/core/SkScan_AAAPath.cpp:1702
    #6 0x91af31 in SkScan::AntiFillPath(SkPath const&, SkRegion const&, SkBlitter*, bool, SkDAARecord*) third_party/skia/src/core/SkScan_AntiPath.cpp:807:9
    #7 0x91c9ca in SkScan::AntiFillPath(SkPath const&, SkRasterClip const&, SkBlitter*, SkDAARecord*) third_party/skia/src/core/SkScan_AntiPath.cpp:846:9
    #8 0x70f975 in SkDraw::drawDevPath(SkPath const&, SkPaint const&, bool, SkBlitter*, bool, SkInitOnceData*) const third_party/skia/src/core/SkDraw.cpp:1024:9
    #9 0x7114f8 in SkDraw::drawPath(SkPath const&, SkPaint const&, SkMatrix const*, bool, bool, SkBlitter*, SkInitOnceData*) const third_party/skia/src/core/SkDraw.cpp:1141:11
    #10 0x70e215 in drawPath third_party/skia/src/core/SkDraw.h:58:15
    #11 0x70e215 in draw_rect_as_path(SkDraw const&, SkRect const&, SkPaint const&, SkMatrix const*) third_party/skia/src/core/SkDraw.cpp:739
    #12 0x70d4c8 in SkDraw::drawRect(SkRect const&, SkPaint const&, SkMatrix const*, SkRect const*) const third_party/skia/src/core/SkDraw.cpp:766:9
    #13 0x713bd9 in SkDraw::drawBitmap(SkBitmap const&, SkMatrix const&, SkRect const*, SkPaint const&) const third_party/skia/src/core/SkDraw.h
    #14 0x63871c in SkBitmapDevice::drawBitmap(SkBitmap const&, SkMatrix const&, SkRect const*, SkPaint const&) third_party/skia/src/core/SkBitmapDevice.cpp:437:5
    #15 0x63819e in SkBitmapDevice::drawBitmap(SkBitmap const&, float, float, SkPaint const&) third_party/skia/src/core/SkBitmapDevice.cpp:419:11
    #16 0x6fcd8b in SkBaseDevice::drawImage(SkImage const*, float, float, SkPaint const&) third_party/skia/src/core/SkDevice.cpp:186:15
    #17 0x6a36df in SkCanvas::onDrawImage(SkImage const*, float, float, SkPaint const*) third_party/skia/src/core/SkCanvas.cpp:2231:27
    #18 0x69749e in SkCanvas::drawImage(SkImage const*, float, float, SkPaint const*) third_party/skia/src/core/SkCanvas.cpp:1714:11
    #19 0x883450 in draw<SkRecords::DrawImage> third_party/skia/src/core/SkRecordDraw.cpp:96:1
    #20 0x883450 in operator()<SkRecords::DrawImage> third_party/skia/src/core/SkRecordDraw.h:62
    #21 0x883450 in decltype ({parm#1}((SkRecords::NoOp)())) SkRecord::Record::visit<SkRecords::Draw&>(SkRecords::Draw&) const third_party/skia/src/core/SkRecord.h:165
    #22 0x88138a in visit<SkRecords::Draw &> third_party/skia/src/core/SkRecord.h:42:28
    #23 0x88138a in SkRecordDraw(SkRecord const&, SkCanvas*, SkPicture const* const*, SkDrawable* const*, int, SkBBoxHierarchy const*, SkPicture::AbortCallback*) third_party/skia/src/core/SkRecordDraw.cpp:52
    #24 0x62926a in SkBigPicture::playback(SkCanvas*, SkPicture::AbortCallback*) const third_party/skia/src/core/SkBigPicture.cpp:33:5
    #25 0x6b0c2d in SkCanvas::onDrawPicture(SkPicture const*, SkMatrix const*, SkPaint const*) third_party/skia/src/core/SkCanvas.cpp:2797:14
    #26 0x6b04ea in SkCanvas::drawPicture(SkPicture const*, SkMatrix const*, SkPaint const*) third_party/skia/src/core/SkCanvas.cpp:2777:15
    #27 0xb3b0d4 in drawPicture third_party/skia/include/core/SkCanvas.h:2141:15
    #28 0xb3b0d4 in drawPicture third_party/skia/include/core/SkCanvas.h:2153
    #29 0xb3b0d4 in SkPictureImageFilter::onFilterImage(SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const third_party/skia/src/effects/SkPictureImageFilter.cpp:119
    #30 0x75cef3 in SkImageFilter::filterImage(SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const third_party/skia/src/core/SkImageFilter.cpp:207:40
    #31 0x761b73 in SkImageFilter::filterInput(int, SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const third_party/skia/src/core/SkImageFilter.cpp:490:41
    #32 0xb253cd in SkMergeImageFilter::onFilterImage(SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const third_party/skia/src/effects/SkMergeImageFilter.cpp:48:27
    #33 0x75cef3 in SkImageFilter::filterImage(SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const third_party/skia/src/core/SkImageFilter.cpp:207:40
    #34 0x761b73 in SkImageFilter::filterInput(int, SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const third_party/skia/src/core/SkImageFilter.cpp:490:41
    #35 0xad485b in SkColorFilterImageFilter::onFilterImage(SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const third_party/skia/src/effects/SkColorFilterImageFilter.cpp:66:39
    #36 0x75cef3 in SkImageFilter::filterImage(SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const third_party/skia/src/core/SkImageFilter.cpp:207:40
    #37 0x63bde2 in SkBitmapDevice::drawSpecial(SkSpecialImage*, int, int, SkPaint const&, SkImage*, SkMatrix const&) third_party/skia/src/core/SkBitmapDevice.cpp:658:33
    #38 0x68d43d in SkCanvas::internalDrawDevice(SkBaseDevice*, int, int, SkPaint const*, SkImage*, SkMatrix const&) third_party/skia/src/core/SkCanvas.cpp:1260:25
    #39 0x6891c2 in SkCanvas::internalRestore() third_party/skia/src/core/SkCanvas.cpp:1148:19
    #40 0x6a52fb in ~AutoDrawLooper third_party/skia/src/core/SkCanvas.cpp:429:22
    #41 0x6a52fb in SkCanvas::onDrawBitmap(SkBitmap const&, float, float, SkPaint const*) third_party/skia/src/core/SkCanvas.cpp:2313
    #42 0x6999dc in SkCanvas::drawBitmap(SkBitmap const&, float, float, SkPaint const*) third_party/skia/src/core/SkCanvas.cpp:1817:11
    #43 0x6188b8 in RunTestCase skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:47:13
    #44 0x6188b8 in ReadAndRunTestCase skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:66
    #45 0x6188b8 in main skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:86
    #46 0x7f5d4ec2b82f in __libc_start_main /build/glibc-bfm8X4/glibc-2.23/csu/../csu/libc-start.c:291

Address 0x7f5d4b27963e is located in stack of thread T0 at offset 62 in frame
    #0 0x624fef in SkBlitter::blitAntiH2(int, int, unsigned int, unsigned int) third_party/skia/src/core/SkBlitter.h:86

  This frame has 2 object(s):
    [32, 38) 'runs' (line 87)
    [64, 66) 'aa' (line 88) <== Memory access at offset 62 underflows this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow third_party/skia/src/core/SkAntiRun.h:154:26 in Break
Shadow bytes around the buggy address:
  0x0fec29647270: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x0fec29647280: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x0fec29647290: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x0fec296472a0: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x0fec296472b0: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
=>0x0fec296472c0: f1 f1 f1 f1 06 f2 f2[f2]02 f3 f3 f3 00 00 00 00
  0x0fec296472d0: f1 f1 f1 f1 00 00 00 f2 f2 f2 f2 f2 04 f2 04 f3
  0x0fec296472e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fec296472f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fec29647300: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fec29647310: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==18047==ABORTING

### zh...@gmail.com (2018-06-14)

Hi team,

One week has passed, how are things going on.

### kj...@chromium.org (2018-06-14)

We have a reproducing patch.  https://skia-review.googlesource.com/c/skia/+/133062

reed@ is OOO this week, who would primarily fix it, although he gave it a good look before he left and said a fix is nontrivial.

mtklein@, would you be able to look or delegate?

### zh...@gmail.com (2018-06-21)

Hi team，

Two weeks have passed，how are the things going on.

Does reed@ in the office this week ? :)

One more thing, this issue also affect beta release （see https://crbug.com/chromium/850350#c7）, so maybe we should add Security_Impact_Beta and ReleaseBlock-Stable label first.

### sh...@chromium.org (2018-06-21)

reed: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2018-06-21)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/9ffe3dc24560297982002234c3e3a03a941f46a9

commit 9ffe3dc24560297982002234c3e3a03a941f46a9
Author: Mike Reed <reed@google.com>
Date: Thu Jun 21 16:37:33 2018

add test for wacky conic edges (disabled for now)

Bug: 850350
Change-Id: Ib73c27da14a74ec6e3b5c04c2f5c9dd7e2462f1c
Reviewed-on: https://skia-review.googlesource.com/136601
Reviewed-by: Mike Reed <reed@google.com>
Commit-Queue: Mike Reed <reed@google.com>

[modify] https://crrev.com/9ffe3dc24560297982002234c3e3a03a941f46a9/tests/RegionTest.cpp


### bu...@chromium.org (2018-06-21)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/1e259cda4fb7f12e98dd611bd651f40ebef2d14a

commit 1e259cda4fb7f12e98dd611bd651f40ebef2d14a
Author: Mike Reed <reed@google.com>
Date: Thu Jun 21 16:47:42 2018

use double to compute root to avoid overflow

Bug: 850350
Change-Id: Iac04fc62e69f51b68c5fc7f55ac1be930133cc74
Reviewed-on: https://skia-review.googlesource.com/136597
Reviewed-by: Mike Reed <reed@google.com>
Commit-Queue: Mike Reed <reed@google.com>

[modify] https://crrev.com/1e259cda4fb7f12e98dd611bd651f40ebef2d14a/src/core/SkGeometry.cpp


### bu...@chromium.org (2018-06-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b58ab39968453638f48200dfe5eb78b2233fde5d

commit b58ab39968453638f48200dfe5eb78b2233fde5d
Author: skia-chromium-autoroll <skia-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Fri Jun 22 01:16:00 2018

Roll src/third_party/skia 61582510eeb8..9457546761a4 (28 commits)

https://skia.googlesource.com/skia.git/+log/61582510eeb8..9457546761a4


git log 61582510eeb8..9457546761a4 --date=short --no-merges --format='%ad %ae %s'
2018-06-21 bsalomon@google.com Alternative fix for stale MIP maps on texture export/import.
2018-06-21 bungeman@google.com Revert "SkRefCnt, SkTypes: fix includes for clients"
2018-06-21 herb@google.com Revert "Add SkGlyphRunList"
2018-06-21 herb@google.com Use local strike caches to avoid flaky test behavior
2018-06-21 herb@google.com Make SkStrikeCache::Validate call non global version
2018-06-21 skcms-skia-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com Roll skia/third_party/skcms 78ef7c5c81fb..97bcdb1d73a1 (1 commits)
2018-06-21 herb@google.com Add SkGlyphRunList
2018-06-21 benjaminwagner@google.com Revert "[infra] Enable retries for Windows compiles"
2018-06-21 egdaniel@google.com Fix vulkan copy resolve.
2018-06-21 swiftshader-skia-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com Roll third_party/externals/swiftshader 20eea3cd3b2d..050ef946947a (1 commits)
2018-06-21 caryclark@skia.org make includes available for flutter
2018-06-21 benjaminwagner@google.com Add Perf NoGPUThreads jobs.
2018-06-21 herb@google.com Expand ExclusiveStrikePtr with StrikeCache
2018-06-21 ruiqimao@google.com fixed NIMA deformed vertices rendering
2018-06-21 skcms-skia-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com Roll skia/third_party/skcms eb7de4255855..78ef7c5c81fb (1 commits)
2018-06-21 borenet@google.com [recipes] Housekeeper-PerCommit-BundleRecipes needs vpython
2018-06-21 fmalita@chromium.org [skottie] Simplify AttachMask
2018-06-21 allanmac@google.com OpenGL interop is simplified when the cl_context is not created by SKC.
2018-06-21 robertphillips@google.com Switch to swap in moveOpListsToDDL for SkTArray
2018-06-21 reed@google.com use double to compute root to avoid overflow
2018-06-21 robertphillips@google.com Move taskgroup initialization closer to where it is used
2018-06-21 caryclark@skia.org abort really big path fuzzing
2018-06-21 reed@google.com add test for wacky conic edges (disabled for now)
2018-06-21 halcanary@google.com Mark all deleted methods private
2018-06-21 brucewang@google.com Implement onMakeClone(const SkFontArguments& args) in class SkTypeface_AndroidSystem.
2018-06-21 herb@google.com Allow access to global glyph cache
2018-06-21 bsalomon@google.com Blacklist ReimportImageTextureWithMipLevels on AndroidOne
2018-06-21 stephana@google.com [infra] Remove PixelC bot


Created with:
  gclient setdep -r src/third_party/skia@9457546761a4

The AutoRoll server is located here: https://autoroll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.

CQ_INCLUDE_TRYBOTS=master.tryserver.blink:linux_trusty_blink_rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel

BUG=chromium:850617,chromium:850350,chromium:850350
TBR=kjlubick@chromium.org

Change-Id: I1e29242736d9855813ae91a481d5564ce97adc76
Reviewed-on: https://chromium-review.googlesource.com/1111157
Reviewed-by: skia-chromium-autoroll <skia-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Commit-Queue: skia-chromium-autoroll <skia-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#569487}
[modify] https://crrev.com/b58ab39968453638f48200dfe5eb78b2233fde5d/DEPS


### bu...@chromium.org (2018-06-22)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/73be50da2a1fe8944f2623a511fda1957eed708a

commit 73be50da2a1fe8944f2623a511fda1957eed708a
Author: Mike Reed <reed@google.com>
Date: Fri Jun 22 21:13:57 2018

flush to zero tiny radii

Bug: 850350
Change-Id: If1f8efdb02782d520195a6b66bd159628c89f811
Reviewed-on: https://skia-review.googlesource.com/137220
Reviewed-by: Kevin Lubick <kjlubick@google.com>
Auto-Submit: Mike Reed <reed@google.com>
Commit-Queue: Mike Reed <reed@google.com>

[modify] https://crrev.com/73be50da2a1fe8944f2623a511fda1957eed708a/tests/RegionTest.cpp
[modify] https://crrev.com/73be50da2a1fe8944f2623a511fda1957eed708a/src/core/SkRRect.cpp


### bu...@chromium.org (2018-06-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/44982312083ebb2b3d2ccc713046add5fe458e73

commit 44982312083ebb2b3d2ccc713046add5fe458e73
Author: skia-chromium-autoroll <skia-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Sat Jun 23 00:22:03 2018

Roll src/third_party/skia c5c3df66430a..73be50da2a1f (6 commits)

https://skia.googlesource.com/skia.git/+log/c5c3df66430a..73be50da2a1f


git log c5c3df66430a..73be50da2a1f --date=short --no-merges --format='%ad %ae %s'
2018-06-22 reed@google.com flush to zero tiny radii
2018-06-22 bungeman@google.com Reland "Implement onMakeClone(const SkFontArguments& args) in class SkTypeface_fontconfig."
2018-06-22 kjlubick@google.com Revert "Implement onMakeClone(const SkFontArguments& args) in class SkTypeface_fontconfig."
2018-06-22 recipe-roller@chromium.org Roll recipe dependencies (trivial).
2018-06-22 swiftshader-skia-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com Roll third_party/externals/swiftshader 932640b2d9cd..41b7748432ef (1 commits)
2018-06-22 csmartdalton@google.com ccpr: Cache paths with >=50% visibility


Created with:
  gclient setdep -r src/third_party/skia@73be50da2a1f

The AutoRoll server is located here: https://autoroll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.

CQ_INCLUDE_TRYBOTS=master.tryserver.blink:linux_trusty_blink_rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel

BUG=chromium:850350
TBR=kjlubick@chromium.org

Change-Id: If796430eb5b441f4e984e7e76df09b731eb35e33
Reviewed-on: https://chromium-review.googlesource.com/1112230
Reviewed-by: skia-chromium-autoroll <skia-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Commit-Queue: skia-chromium-autoroll <skia-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#569853}
[modify] https://crrev.com/44982312083ebb2b3d2ccc713046add5fe458e73/DEPS


### zh...@gmail.com (2018-06-29)

Hi team,

Thank you for making patches for this issue. 

Any update for the status? The status is remain assign, does it need more work to make it fixed.

One more thing, as I tested the latest beta release, this vulnerability is still exists.

Thank you again.

### in...@chromium.org (2018-06-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-02)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), kariahda@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2018-07-02)

Reed@ can you please confirm specifically what needs to be merged?

### ab...@google.com (2018-07-03)

[Empty comment from Monorail migration]

### cm...@chromium.org (2018-07-11)

Ping!

### zh...@gmail.com (2018-07-12)

Ping!

@awhalley I wonder this report is elegant for the bug bounty program? 

### re...@google.com (2018-07-12)

I think this CL was the key one

https://skia-review.googlesource.com/c/skia/+/137220

### aw...@chromium.org (2018-07-12)

zhouzhenster@ - the panel has taken a few weeks off recently, but we'll look at it in an upcoming session.

### zh...@gmail.com (2018-07-12)

[Comment Deleted]

### zh...@gmail.com (2018-07-12)

awhalley@   thank you for that information

### ab...@google.com (2018-07-13)

How safe is this merge and how critical is this?

### re...@google.com (2018-07-13)

I think its pretty isolated, so a merge wouldn't be high risk.

### ab...@google.com (2018-07-13)

Approved- branch:3440

### sh...@chromium.org (2018-07-17)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2018-07-17)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/73d6ab7591233267978a6205b3d72efcff3519c9

commit 73d6ab7591233267978a6205b3d72efcff3519c9
Author: Mike Reed <reed@google.com>
Date: Tue Jul 17 17:06:25 2018

flush to zero tiny radii

No-Tree-Checks: true
No-Try: true
No-Presubmit: true
Bug: 850350
Change-Id: If1f8efdb02782d520195a6b66bd159628c89f811
Reviewed-On: https://skia-review.googlesource.com/137220
Reviewed-By: Kevin Lubick <kjlubick@google.com>
Auto-Submit: Mike Reed <reed@google.com>
Commit-Queue: Mike Reed <reed@google.com>
Reviewed-on: https://skia-review.googlesource.com/141826
Reviewed-by: Mike Reed <reed@google.com>

[modify] https://crrev.com/73d6ab7591233267978a6205b3d72efcff3519c9/tests/RegionTest.cpp
[modify] https://crrev.com/73d6ab7591233267978a6205b3d72efcff3519c9/src/core/SkRRect.cpp


### ab...@google.com (2018-07-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-07-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-07-23)

Nice one zhouzhenster@! The VRP panel decided to award $5,000 for this report :-)

### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### is...@google.com (2019-01-04)

This issue was migrated from crbug.com/chromium/850350?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091589)*
