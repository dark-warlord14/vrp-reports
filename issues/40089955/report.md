# Heap-buffer-overflow in SkUTF8_NextUnichar

| Field | Value |
|-------|-------|
| **Issue ID** | [40089955](https://issues.chromium.org/issues/40089955) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Platforms** | Linux |
| **Reporter** | jo...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2017-12-20 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36

Steps to reproduce the problem:
1. build https://chromium.googlesource.com/chromium/src/+/65.0.3294.5
2. run ./filter_fuzz_stub path/to/poc

What is the expected behavior?
crashed by asan and report heap-buffer-overflow

What went wrong?
in SkPaint.cpp: 2268
====================
bool SkTextToPathIter::next(const SkPath** path, SkScalar* xpos) {
    if (fText < fStop) {                                            <====== It check fText with fStop
        const SkGlyph& glyph = fGlyphCacheProc(fCache, &fText);
====================
......
<some function calls>
......
in SkUtils.cpp
====================
SkUnichar SkUTF8_NextUnichar(const char** ptr) {
    SkASSERT(ptr && *ptr);

    const uint8_t*  p = (const uint8_t*)*ptr;
    int             c = *p;
    int             hic = c << 24;

    assert_utf8_leadingbyte(c);

    if (hic < 0) {
        uint32_t mask = (uint32_t)~0x3F;
        hic = SkLeftShift(hic, 1);
        do {
            c = (c << 6) | (*++p & 0x3F);                         <====== In order to read a complete Unichar，p increased without check, it may exceed the limit of fStop above 
            mask <<= 5;
        } while ((hic = SkLeftShift(hic, 1)) < 0);
        c &= ~mask;
    }
    *ptr = (char*)p + 1;
    return c;
}
====================

Did this work before? N/A 

Chrome version: 65.0.3294.5  Channel: dev
OS Version: ubuntu 16.04.3 x64
Flash Version: 28.0.0.126

[1219/180554.251616:INFO:filter_fuzz_stub.cc(61)] Test case: path/to/poc
[1219/180554.251929:INFO:filter_fuzz_stub.cc(38)] Valid stream detected.
=================================================================
==15898==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x611000000f00 at pc 0x000000971104 bp 0x7ffea55374e0 sp 0x7ffea55374d8
READ of size 1 at 0x611000000f00 thread T0
    #0 0x971103 in _Z18SkUTF8_NextUnicharPPKc /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkUtils.cpp:177:29
    #1 0x8a6990 in _ZL23sk_getMetrics_utf8_nextP12SkGlyphCachePPKc /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkPaint.cpp:568:37
    #2 0x8aa4bd in _ZN16SkTextToPathIter4nextEPPK6SkPathPf /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkPaint.cpp:2270:32
    #3 0x845b20 in _ZNK6SkDraw16drawText_asPathsEPKcmffRK7SkPaint /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkDraw.cpp:1384:17
    #4 0x845e17 in _ZNK6SkDraw8drawTextEPKcmffRK7SkPaintPK14SkSurfaceProps /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkDraw.cpp:1539:15
    #5 0xe95fb0 in _ZN14SkBitmapDevice8drawTextEPKvmffRK7SkPaint /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkBitmapDevice.cpp:358:18
    #6 0x7f8175 in _ZN8SkCanvas10onDrawTextEPKvmffRK7SkPaint /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkCanvas.cpp:2466:23
    #7 0x7fb049 in _ZN8SkCanvas8drawTextEPKvmffRK7SkPaint /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkCanvas.cpp:2571:15
    #8 0x8f3372 in draw<SkRecords::DrawText> /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkRecordDraw.cpp:123:1
    #9 0x8f3372 in operator()<SkRecords::DrawText> /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkRecordDraw.h:62:0
    #10 0x8f3372 in _ZNK8SkRecord6Record5visitIRN9SkRecords4DrawEEEDTclfp_cvNS2_4NoOpE_EEEOT_ /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkRecord.h:165:0
    #11 0x8f109a in visit<SkRecords::Draw &> /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkRecord.h:42:28
    #12 0x8f109a in _Z12SkRecordDrawRK8SkRecordP8SkCanvasPKPK9SkPicturePKP10SkDrawableiPK15SkBBoxHierarchyPNS4_13AbortCallbackE /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkRecordDraw.cpp:52:0
    #13 0xe8cdab in _ZNK12SkBigPicture8playbackEP8SkCanvasPN9SkPicture13AbortCallbackE /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkBigPicture.cpp:33:5
    #14 0x8004e0 in _ZN8SkCanvas13onDrawPictureEPK9SkPicturePK8SkMatrixPK7SkPaint /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkCanvas.cpp:2824:14
    #15 0x7ffd12 in _ZN8SkCanvas11drawPictureEPK9SkPicturePK8SkMatrixPK7SkPaint /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkCanvas.cpp:2804:15
    #16 0x1033c77 in drawPicture /media/eins/Repo/chrome_all/test/../src/third_party/skia/include/core/SkCanvas.h:2132:15
    #17 0x1033c77 in drawPicture /media/eins/Repo/chrome_all/test/../src/third_party/skia/include/core/SkCanvas.h:2144:0
    #18 0x1033c77 in _ZNK20SkPictureImageFilter13onFilterImageEP14SkSpecialImageRKN13SkImageFilter7ContextEP8SkIPoint /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/effects/SkPictureImageFilter.cpp:126:0
    #19 0x8565f7 in _ZNK13SkImageFilter11filterImageEP14SkSpecialImageRKNS_7ContextEP8SkIPoint /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkImageFilter.cpp:213:40
    #20 0xe96f43 in _ZN14SkBitmapDevice11drawSpecialEP14SkSpecialImageiiRK7SkPaintP7SkImageRK8SkMatrix /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkBitmapDevice.cpp:421:33
    #21 0x7f3f38 in _ZN8SkCanvas12onDrawBitmapERK8SkBitmapffPK7SkPaint /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkCanvas.cpp:2298:27
    #22 0x7e8dbf in _ZN8SkCanvas10drawBitmapERK8SkBitmapffPK7SkPaint /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkCanvas.cpp:1831:11
    #23 0x4f16df in RunTestCase /media/eins/Repo/chrome_all/test/../src/skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:48:13
    #24 0x4f16df in ReadAndRunTestCase /media/eins/Repo/chrome_all/test/../src/skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:67:0
    #25 0x4f16df in main /media/eins/Repo/chrome_all/test/../src/skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:87:0
    #26 0x7fee3154b82f in __libc_start_main /build/glibc-bfm8X4/glibc-2.23/csu/../csu/libc-start.c:291:0

0x611000000f00 is located 0 bytes to the right of 256-byte region [0x611000000e00,0x611000000f00)
allocated by thread T0 here:
    #0 0x4edfc2 in _Znam _asan_rtl_:3
    #1 0x84ffa1 in _ZN12SkArenaAlloc11ensureSpaceEjj /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkArenaAlloc.cpp:141:22
    #2 0x9097fa in allocObject /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkArenaAlloc.h:165:19
    #3 0x9097fa in commonArrayAlloc<RawBytes> /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkArenaAlloc.h:181:0
    #4 0x9097fa in makeArrayDefault<RawBytes> /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkArenaAlloc.h:118:0
    #5 0x9097fa in alloc<SkRecords::DrawOval> /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkRecord.h:62:0
    #6 0x9097fa in allocCommand<SkRecords::DrawOval> /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkRecord.h:138:0
    #7 0x9097fa in append<SkRecords::DrawOval> /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkRecord.h:72:0
    #8 0x9097fa in _ZN10SkRecorder10onDrawOvalERK6SkRectRK7SkPaint /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkRecorder.cpp:153:0
    #9 0x7e57d6 in _ZN8SkCanvas8drawOvalERK6SkRectRK7SkPaint /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkCanvas.cpp:1730:11
    #10 0xf2ecbb in _ZN17SkPicturePlayback8handleOpEP12SkReadBuffer8DrawTypejP8SkCanvasRK8SkMatrix /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkPicturePlayback.cpp:403:25
    #11 0xf2b40b in _ZN17SkPicturePlayback4drawEP8SkCanvasPN9SkPicture13AbortCallbackEP12SkReadBuffer /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkPicturePlayback.cpp:116:15
    #12 0xf2193c in Forwardport /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkPicture.cpp:142:14
    #13 0xf2193c in _ZN9SkPicture14MakeFromBufferER12SkReadBuffer /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkPicture.cpp:239:0
    #14 0x1032cda in _ZN20SkPictureImageFilter10CreateProcER12SkReadBuffer /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/effects/SkPictureImageFilter.cpp:63:23
    #15 0x8edb15 in _ZN12SkReadBuffer15readFlattenableEN13SkFlattenable4TypeE /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkReadBuffer.cpp:444:15
    #16 0x8509ff in _ZN13SkFlattenable11DeserializeENS_4TypeEPKvmPK15SkDeserialProcs /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkFlattenable.cpp:145:40
    #17 0x850c7f in _Z34SkValidatingDeserializeImageFilterPKvm /media/eins/Repo/chrome_all/test/../src/third_party/skia/src/core/SkFlattenableSerialization.cpp:22:17
    #18 0x4f14b0 in RunTestCase /media/eins/Repo/chrome_all/test/../src/skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:33:38
    #19 0x4f14b0 in ReadAndRunTestCase /media/eins/Repo/chrome_all/test/../src/skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:67:0
    #20 0x4f14b0 in main /media/eins/Repo/chrome_all/test/../src/skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:87:0
    #21 0x7fee3154b82f in __libc_start_main /build/glibc-bfm8X4/glibc-2.23/csu/../csu/libc-start.c:291:0

SUMMARY: AddressSanitizer: heap-buffer-overflow (/media/eins/Repo/chrome_all/test/filter_fuzz_stub+0x971103)
Shadow bytes around the buggy address:
  0x0c227fff8190: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x0c227fff81a0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c227fff81b0: 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa
  0x0c227fff81c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c227fff81d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c227fff81e0:[fa]fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c227fff81f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c227fff8200: fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c227fff8210: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c227fff8220: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa
  0x0c227fff8230: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:   == SIGABRT ==
        00
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
==15898==ABORTING

## Attachments

- [crash_poc](attachments/crash_poc) (text/plain, 252 B)

## Timeline

### jo...@gmail.com (2017-12-20)

I report this issue to Type Bug before:
  https://bugs.chromium.org/p/chromium/issues/detail?id=796116
but I don't known how to change the Type from Bug to Bug-Security!!

### in...@chromium.org (2017-12-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-12-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4988509252485120.

### el...@chromium.org (2017-12-20)

[Empty comment from Monorail migration]

[Monorail components: Internals>Skia]

### cl...@chromium.org (2017-12-20)

Detailed report: https://clusterfuzz.com/testcase?key=4988509252485120

Job Type: linux_asan_filter_fuzz_stub
Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x612000001080
Crash State:
  SkUTF8_NextUnichar
  sk_getMetrics_utf8_next
  SkTextToPathIter::next
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_filter_fuzz_stub&range=522280:522288

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4988509252485120

See https://github.com/google/clusterfuzz-tools for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.


### sh...@chromium.org (2017-12-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-21)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-12-21)

[Empty comment from Monorail migration]

### [Deleted User] (2017-12-21)

[Empty comment from Monorail migration]

### [Deleted User] (2017-12-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-12-21)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/889d521d8715f4934accb630097bc09bf7ad1a32

commit 889d521d8715f4934accb630097bc09bf7ad1a32
Author: Mike Reed <reed@google.com>
Date: Thu Dec 21 21:06:44 2017

validate text during deserialization

Bug: 796473
Change-Id: I7b6a6c698a5b53c915ef6564852fa51ce7410a3e
Reviewed-on: https://skia-review.googlesource.com/88520
Commit-Queue: Mike Reed <reed@google.com>
Reviewed-by: Hal Canary <halcanary@google.com>

[modify] https://crrev.com/889d521d8715f4934accb630097bc09bf7ad1a32/src/core/SkPaint.cpp
[modify] https://crrev.com/889d521d8715f4934accb630097bc09bf7ad1a32/tests/UtilsTest.cpp
[modify] https://crrev.com/889d521d8715f4934accb630097bc09bf7ad1a32/src/core/SkFont.cpp
[modify] https://crrev.com/889d521d8715f4934accb630097bc09bf7ad1a32/src/core/SkPicturePlayback.cpp
[modify] https://crrev.com/889d521d8715f4934accb630097bc09bf7ad1a32/src/xps/SkXPSDevice.cpp
[modify] https://crrev.com/889d521d8715f4934accb630097bc09bf7ad1a32/src/core/SkPaintPriv.cpp
[modify] https://crrev.com/889d521d8715f4934accb630097bc09bf7ad1a32/src/core/SkUtils.h
[modify] https://crrev.com/889d521d8715f4934accb630097bc09bf7ad1a32/src/core/SkPaintPriv.h
[modify] https://crrev.com/889d521d8715f4934accb630097bc09bf7ad1a32/src/core/SkUtils.cpp


### cl...@chromium.org (2017-12-22)

ClusterFuzz has detected this issue as fixed in range 525905:525906.

Detailed report: https://clusterfuzz.com/testcase?key=4988509252485120

Job Type: linux_asan_filter_fuzz_stub
Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x612000001080
Crash State:
  SkUTF8_NextUnichar
  sk_getMetrics_utf8_next
  SkTextToPathIter::next
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_filter_fuzz_stub&range=522280:522288
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_filter_fuzz_stub&range=525905:525906

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4988509252485120

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2017-12-22)

ClusterFuzz testcase 4988509252485120 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2017-12-22)

[Empty comment from Monorail migration]

### aw...@google.com (2018-01-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-01-05)

Hi jonaluwang@ - the Chrome VRP panel decided to award $1,000 for this report!  A member of our finance team will be in touch next week to arrange payment.

Also, how would you like to be credited in release notes?


### aw...@chromium.org (2018-01-06)

[Empty comment from Monorail migration]

### jo...@gmail.com (2018-01-08)

Thanks for your information.
Please credit this to Wanglu & Yangkang(@dnpushme) of Qihoo360 Qex Team.

### me...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-02-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-03-30)

This issue was migrated from crbug.com/chromium/796473?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/796116]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089955)*
