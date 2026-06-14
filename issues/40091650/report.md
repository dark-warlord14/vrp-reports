# Security: negative-size-param in Skia

| Field | Value |
|-------|-------|
| **Issue ID** | [40091650](https://issues.chromium.org/issues/40091650) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | zh...@gmail.com |
| **Assignee** | re...@google.com |
| **Created** | 2018-06-14 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

This issue was found by fuzzing against a 64-bit asan linux build of filter\_fuzz\_stub.

**VERSION**  

Chrome Version: beta-68.0.3440.17  

Operating System: Fedora 28 x86\_64

**REPRODUCTION CASE**

~/asan-linux-beta-68.0.3440.17$ ./filter\_fuzz\_stub /tmp/memset.fil

# [0614/110851.314868:INFO:filter\_fuzz\_stub.cc(60)] Test case: /tmp/memset.fil [0614/110851.361252:INFO:filter\_fuzz\_stub.cc(37)] Valid stream detected.

==3867==ERROR: AddressSanitizer: negative-size-param: (size=-1)  

#0 0x5e8581 in \_\_asan\_memset /b/build/slave/linux\_upload\_clang/build/src/third\_party/llvm/compiler-rt/lib/asan/asan\_interceptors\_memintrinsics.cc:27:3  

#1 0x65c7d9 in SkA8\_Coverage\_Blitter::blitH(int, int, int) third\_party/skia/src/core/SkBlitter\_A8.cpp:44:5  

#2 0x65544c in SkRgnClipBlitter::blitH(int, int, int) third\_party/skia/src/core/SkBlitter.cpp:602:19  

#3 0x8eebe4 in blit\_full\_alpha third\_party/skia/src/core/SkScan\_AAAPath.cpp:692:40  

#4 0x8eebe4 in blit\_trapezoid\_row third\_party/skia/src/core/SkScan\_AAAPath.cpp:860  

#5 0x8eebe4 in aaa\_walk\_edges third\_party/skia/src/core/SkScan\_AAAPath.cpp:1556  

#6 0x8eebe4 in aaa\_fill\_path third\_party/skia/src/core/SkScan\_AAAPath.cpp:1669  

#7 0x8eebe4 in SkScan::AAAFillPath(SkPath const&, SkBlitter\*, SkIRect const&, SkIRect const&, bool) third\_party/skia/src/core/SkScan\_AAAPath.cpp:1709  

#8 0x91af31 in SkScan::AntiFillPath(SkPath const&, SkRegion const&, SkBlitter\*, bool, SkDAARecord\*) third\_party/skia/src/core/SkScan\_AntiPath.cpp:807:9  

#9 0x91c9ca in SkScan::AntiFillPath(SkPath const&, SkRasterClip const&, SkBlitter\*, SkDAARecord\*) third\_party/skia/src/core/SkScan\_AntiPath.cpp:846:9  

#10 0x70f975 in SkDraw::drawDevPath(SkPath const&, SkPaint const&, bool, SkBlitter\*, bool, SkInitOnceData\*) const third\_party/skia/src/core/SkDraw.cpp:1024:9  

#11 0x7114f8 in SkDraw::drawPath(SkPath const&, SkPaint const&, SkMatrix const\*, bool, bool, SkBlitter\*, SkInitOnceData\*) const third\_party/skia/src/core/SkDraw.cpp:1141:11  

#12 0x637c4a in drawPath third\_party/skia/src/core/SkDraw.h:58:15  

#13 0x637c4a in SkBitmapDevice::drawPath(SkPath const&, SkPaint const&, SkMatrix const\*, bool) third\_party/skia/src/core/SkBitmapDevice.cpp:411  

#14 0x6a2181 in SkCanvas::onDrawPath(SkPath const&, SkPaint const&) third\_party/skia/src/core/SkCanvas.cpp:2149:23  

#15 0x697012 in SkCanvas::drawPath(SkPath const&, SkPaint const&) third\_party/skia/src/core/SkCanvas.cpp:1708:11  

#16 0x883298 in draw[SkRecords::DrawPath](javascript:void(0);) third\_party/skia/src/core/SkRecordDraw.cpp:114:1  

#17 0x883298 in operator()[SkRecords::DrawPath](javascript:void(0);) third\_party/skia/src/core/SkRecordDraw.h:62  

#18 0x883298 in decltype ({parm#1}((SkRecords::NoOp)())) SkRecord::Record::visit[SkRecords::Draw&](javascript:void(0);)(SkRecords::Draw&) const third\_party/skia/src/core/SkRecord.h:165  

#19 0x88138a in visit<SkRecords::Draw &> third\_party/skia/src/core/SkRecord.h:42:28  

#20 0x88138a in SkRecordDraw(SkRecord const&, SkCanvas\*, SkPicture const\* const\*, SkDrawable\* const\*, int, SkBBoxHierarchy const\*, SkPicture::AbortCallback\*) third\_party/skia/src/core/SkRecordDraw.cpp:52  

#21 0x62926a in SkBigPicture::playback(SkCanvas\*, SkPicture::AbortCallback\*) const third\_party/skia/src/core/SkBigPicture.cpp:33:5  

#22 0x6b0c2d in SkCanvas::onDrawPicture(SkPicture const\*, SkMatrix const\*, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:2797:14  

#23 0x6b04ea in SkCanvas::drawPicture(SkPicture const\*, SkMatrix const\*, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:2777:15  

#24 0xb3b0d4 in drawPicture third\_party/skia/include/core/SkCanvas.h:2141:15  

#25 0xb3b0d4 in drawPicture third\_party/skia/include/core/SkCanvas.h:2153  

#26 0xb3b0d4 in SkPictureImageFilter::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkPictureImageFilter.cpp:119  

#27 0x75cef3 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:207:40  

#28 0x761b73 in SkImageFilter::filterInput(int, SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:490:41  

#29 0xb253cd in SkMergeImageFilter::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkMergeImageFilter.cpp:48:27  

#30 0x75cef3 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:207:40  

#31 0x761b73 in SkImageFilter::filterInput(int, SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:490:41  

#32 0xad485b in SkColorFilterImageFilter::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkColorFilterImageFilter.cpp:66:39  

#33 0x75cef3 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:207:40  

#34 0x63bde2 in SkBitmapDevice::drawSpecial(SkSpecialImage\*, int, int, SkPaint const&, SkImage\*, SkMatrix const&) third\_party/skia/src/core/SkBitmapDevice.cpp:658:33  

#35 0x68d43d in SkCanvas::internalDrawDevice(SkBaseDevice\*, int, int, SkPaint const\*, SkImage\*, SkMatrix const&) third\_party/skia/src/core/SkCanvas.cpp:1260:25  

#36 0x6891c2 in SkCanvas::internalRestore() third\_party/skia/src/core/SkCanvas.cpp:1148:19  

#37 0x6a52fb in ~AutoDrawLooper third\_party/skia/src/core/SkCanvas.cpp:429:22  

#38 0x6a52fb in SkCanvas::onDrawBitmap(SkBitmap const&, float, float, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:2313  

#39 0x6999dc in SkCanvas::drawBitmap(SkBitmap const&, float, float, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:1817:11  

#40 0x6188b8 in RunTestCase skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:47:13  

#41 0x6188b8 in ReadAndRunTestCase skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:66  

#42 0x6188b8 in main skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:86  

#43 0x7f163071182f in \_\_libc\_start\_main /build/glibc-bfm8X4/glibc-2.23/csu/../csu/libc-start.c:291

0x616000015ce2 is located 98 bytes inside of 576-byte region [0x616000015c80,0x616000015ec0)  

allocated by thread T0 here:  

#0 0x5e9123 in \_\_interceptor\_malloc /b/build/slave/linux\_upload\_clang/build/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cc:98:3  

#1 0x12eda6d in base::UncheckedMalloc(unsigned long, void\*\*) base/process/memory\_linux.cc:105:13  

#2 0x12ed7cd in base::UncheckedCalloc(unsigned long, unsigned long, void\*\*) base/process/memory.cc:45:8  

#3 0xeb865c in calloc\_nothrow skia/ext/SkMemory\_new\_handler.cpp:96:19  

#4 0xeb865c in sk\_malloc\_flags(unsigned long, unsigned int) skia/ext/SkMemory\_new\_handler.cpp:109  

#5 0x77668c in sk\_calloc\_canfail third\_party/skia/include/private/SkMalloc.h:74:12  

#6 0x77668c in MakeUsing third\_party/skia/src/core/SkMallocPixelRef.cpp:76  

#7 0x77668c in SkMallocPixelRef::MakeZeroed(SkImageInfo const&, unsigned long) third\_party/skia/src/core/SkMallocPixelRef.cpp:91  

#8 0x62d2bb in SkBitmap::tryAllocPixelsFlags(SkImageInfo const&, unsigned int) third\_party/skia/src/core/SkBitmap.cpp:256:9  

#9 0x63500a in SkBitmapDevice::Create(SkImageInfo const&, SkSurfaceProps const&, bool, SkRasterHandleAllocator\*) third\_party/skia/src/core/SkBitmapDevice.cpp:300:23  

#10 0x63587b in SkBitmapDevice::onCreateDevice(SkBaseDevice::CreateInfo const&, SkPaint const\*) third\_party/skia/src/core/SkBitmapDevice.cpp:317:12  

#11 0x68baaf in SkCanvas::internalSaveLayer(SkCanvas::SaveLayerRec const&, SkCanvas::SaveLayerStrategy) third\_party/skia/src/core/SkCanvas.cpp:1083:38  

#12 0x68ad14 in SkCanvas::saveLayer(SkCanvas::SaveLayerRec const&) third\_party/skia/src/core/SkCanvas.cpp:951:11  

#13 0x883150 in draw[SkRecords::SaveLayer](javascript:void(0);) third\_party/skia/src/core/SkRecordDraw.cpp:79:1  

#14 0x883150 in operator()[SkRecords::SaveLayer](javascript:void(0);) third\_party/skia/src/core/SkRecordDraw.h:62  

#15 0x883150 in decltype ({parm#1}((SkRecords::NoOp)())) SkRecord::Record::visit[SkRecords::Draw&](javascript:void(0);)(SkRecords::Draw&) const third\_party/skia/src/core/SkRecord.h:165  

#16 0x88138a in visit<SkRecords::Draw &> third\_party/skia/src/core/SkRecord.h:42:28  

#17 0x88138a in SkRecordDraw(SkRecord const&, SkCanvas\*, SkPicture const\* const\*, SkDrawable\* const\*, int, SkBBoxHierarchy const\*, SkPicture::AbortCallback\*) third\_party/skia/src/core/SkRecordDraw.cpp:52  

#18 0x62926a in SkBigPicture::playback(SkCanvas\*, SkPicture::AbortCallback\*) const third\_party/skia/src/core/SkBigPicture.cpp:33:5  

#19 0x6b0c2d in SkCanvas::onDrawPicture(SkPicture const\*, SkMatrix const\*, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:2797:14  

#20 0x6b04ea in SkCanvas::drawPicture(SkPicture const\*, SkMatrix const\*, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:2777:15  

#21 0xb3b0d4 in drawPicture third\_party/skia/include/core/SkCanvas.h:2141:15  

#22 0xb3b0d4 in drawPicture third\_party/skia/include/core/SkCanvas.h:2153  

#23 0xb3b0d4 in SkPictureImageFilter::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkPictureImageFilter.cpp:119  

#24 0x75cef3 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:207:40  

#25 0x761b73 in SkImageFilter::filterInput(int, SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:490:41  

#26 0xb253cd in SkMergeImageFilter::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkMergeImageFilter.cpp:48:27  

#27 0x75cef3 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:207:40  

#28 0x761b73 in SkImageFilter::filterInput(int, SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:490:41  

#29 0xad485b in SkColorFilterImageFilter::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkColorFilterImageFilter.cpp:66:39  

#30 0x75cef3 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:207:40  

#31 0x63bde2 in SkBitmapDevice::drawSpecial(SkSpecialImage\*, int, int, SkPaint const&, SkImage\*, SkMatrix const&) third\_party/skia/src/core/SkBitmapDevice.cpp:658:33  

#32 0x68d43d in SkCanvas::internalDrawDevice(SkBaseDevice\*, int, int, SkPaint const\*, SkImage\*, SkMatrix const&) third\_party/skia/src/core/SkCanvas.cpp:1260:25  

#33 0x6891c2 in SkCanvas::internalRestore() third\_party/skia/src/core/SkCanvas.cpp:1148:19  

#34 0x6a52fb in ~AutoDrawLooper third\_party/skia/src/core/SkCanvas.cpp:429:22  

#35 0x6a52fb in SkCanvas::onDrawBitmap(SkBitmap const&, float, float, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:2313  

#36 0x6999dc in SkCanvas::drawBitmap(SkBitmap const&, float, float, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:1817:11  

#37 0x6188b8 in RunTestCase skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:47:13  

#38 0x6188b8 in ReadAndRunTestCase skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:66  

#39 0x6188b8 in main skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:86  

#40 0x7f163071182f in \_\_libc\_start\_main /build/glibc-bfm8X4/glibc-2.23/csu/../csu/libc-start.c:291

SUMMARY: AddressSanitizer: negative-size-param /b/build/slave/linux\_upload\_clang/build/src/third\_party/llvm/compiler-rt/lib/asan/asan\_interceptors\_memintrinsics.cc:27:3 in \_\_asan\_memset  

==3867==ABORTING

testcase is in the attachment.

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### wf...@chromium.org (2018-06-14)

Thanks for the report.

[Monorail components: Internals>Skia]

### cl...@chromium.org (2018-06-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6612476591079424.

### wf...@chromium.org (2018-06-14)

might be https://skia-review.googlesource.com/122000 ? -> reed

### cl...@chromium.org (2018-06-14)

Detailed report: https://clusterfuzz.com/testcase?key=6612476591079424

Job Type: linux_asan_filter_fuzz_stub
Platform Id: linux

Crash Type: Negative-size-param
Crash Address: 
Crash State:
  SkA8_Coverage_Blitter::blitH
  SkRgnClipBlitter::blitH
  SkScan::AAAFillPath
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_filter_fuzz_stub&range=553756:553758

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6612476591079424

See https://github.com/google/clusterfuzz-tools for more information.

### wf...@chromium.org (2018-06-14)

From CF, skia regression range

https://skia.googlesource.com/skia/+log/27988f76b25eb54a0cce7d802c3e80565783a90f..25af671a3d7d790b31b085172952df3867337431?pretty=fuller&n=10000

confirms it was probably https://skia-review.googlesource.com/122000

### sh...@chromium.org (2018-06-15)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### in...@chromium.org (2018-06-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-06-22)

ClusterFuzz has detected this issue as fixed in range 569482:569487.

Detailed report: https://clusterfuzz.com/testcase?key=6612476591079424

Job Type: linux_asan_filter_fuzz_stub
Platform Id: linux

Crash Type: Negative-size-param
Crash Address: 
Crash State:
  SkA8_Coverage_Blitter::blitH
  SkRgnClipBlitter::blitH
  SkScan::AAAFillPath
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_filter_fuzz_stub&range=553756:553758
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_filter_fuzz_stub&range=569482:569487

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6612476591079424

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-06-22)

ClusterFuzz testcase 6612476591079424 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-06-22)

[Empty comment from Monorail migration]

### zh...@gmail.com (2018-06-25)

Hi team,

This bug was unintentionally fixed, because no commit was refered to the bug. I think we should double check if the root cause was found.



### aw...@chromium.org (2018-06-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-27)

This bug requires manual review: M68 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), kariahda@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2018-06-28)

Seems like nothing to be merged. 

### aw...@chromium.org (2018-06-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-06-29)

Thanks for the report! The VRP panel decided to award $1,000, but noted that they would consider for a higher amount if it could be demonstrated to be exploitable.

### aw...@chromium.org (2018-06-29)

[Empty comment from Monorail migration]

### aw...@google.com (2018-07-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-09-28)

This issue was migrated from crbug.com/chromium/852644?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091650)*
