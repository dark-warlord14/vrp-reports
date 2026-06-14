# heap-buffer-overflow in SkAAClip::quickContains

| Field | Value |
|-------|-------|
| **Issue ID** | [40090013](https://issues.chromium.org/issues/40090013) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | Internals>Skia |
| **Platforms** | Linux |
| **Reporter** | m....@gmail.com |
| **Assignee** | re...@google.com |
| **Created** | 2017-12-29 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36

Steps to reproduce the problem:
1. build https://chromium.googlesource.com/chromium/src/+/65.0.3298.3/
2. run ./filter_fuzz_stub ./poc 

What is the expected behavior?

What went wrong?
const uint8_t* SkAAClip::findX(const uint8_t data[], int x, int* initialCount) const {
    SkASSERT(x_in_rect(x, fBounds));
    x -= fBounds.x();           <<----[1]

    // first skip up to X
    for (;;) {
        int n = data[0];            <<---[2]
        if (x < n) {
            if (initialCount) {
                *initialCount = n - x;
            }
            break;
        }
        data += 2;
        x -= n;
    }
    return data;
}

Debug log
Breakpoint 4, SkAAClip::quickContains (this=0x1ffe18df4d08, left=0x0, top=0x0, right=0x11, bottom=0x1f) at ../src/third_party/skia/src/core/SkAAClip.cpp:908
908	    if (this->isEmpty()) {

gdb$ p fBounds
$9 = {fLeft = 0x80414000, fTop = 0x0, fRight = 0x3030303, fBottom = 0x3030312}

AT[1] We can see that fBounds.fLeft is negative integer, so x will be very lager.
AT[2] There is no check data buffer size cause an oob read

Patch

I think fBounds structure needs more stringent verification

Did this work before? N/A 

Chrome version: 65.0.3298.3  Channel: dev
OS Version: 16.04
Flash Version: 

[1229/174105.584953:INFO:filter_fuzz_stub.cc(61)] Test case: ./poc
[1229/174105.586477:INFO:filter_fuzz_stub.cc(38)] Valid stream detected.
=================================================================
==26009==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60300000068a at pc 0x00000098bcd3 bp 0x7ffcb4db01c0 sp 0x7ffcb4db01b8
READ of size 1 at 0x60300000068a thread T0
    #0 0x98bcd2 in findX src/third_party/skia/src/core/SkAAClip.cpp:894:17
    #1 0x98bcd2 in SkAAClip::quickContains(int, int, int, int) const src/third_party/skia/src/core/SkAAClip.cpp:927
    #2 0x98efc5 in quickContains src/third_party/skia/src/core/SkAAClip.h:65:22
    #3 0x98efc5 in SkAAClip::op(SkIRect const&, SkRegion::Op) src/third_party/skia/src/core/SkAAClip.cpp:1768
    #4 0xa90ef5 in SkRasterClip::op(SkIRect const&, SkRegion::Op) src/third_party/skia/src/core/SkRasterClip.cpp:308:36
    #5 0x9389d0 in trimIfExpanding src/third_party/skia/src/core/SkRasterClipStack.h:168:21
    #6 0x9389d0 in clipRegion src/third_party/skia/src/core/SkRasterClipStack.h:121
    #7 0x9389d0 in SkBitmapDevice::onClipRegion(SkRegion const&, SkClipOp) src/third_party/skia/src/core/SkBitmapDevice.cpp:564
    #8 0x911c0e in clipRegion src/third_party/skia/src/core/SkDevice.h:116:15
    #9 0x911c0e in SkCanvas::onClipRegion(SkRegion const&, SkClipOp) src/third_party/skia/src/core/SkCanvas.cpp:1496
    #10 0xaa7ca2 in draw<SkRecords::ClipRegion> src/third_party/skia/src/core/SkRecordDraw.cpp:92:1
    #11 0xaa7ca2 in operator()<SkRecords::ClipRegion> src/third_party/skia/src/core/SkRecordDraw.h:62
    #12 0xaa7ca2 in decltype ({parm#1}((SkRecords::NoOp)())) SkRecord::Record::visit<SkRecords::Draw&>(SkRecords::Draw&) const src/third_party/skia/src/core/SkRecord.h:165
    #13 0xaa5daa in visit<SkRecords::Draw &> src/third_party/skia/src/core/SkRecord.h:42:28
    #14 0xaa5daa in SkRecordDraw(SkRecord const&, SkCanvas*, SkPicture const* const*, SkDrawable* const*, int, SkBBoxHierarchy const*, SkPicture::AbortCallback*) src/third_party/skia/src/core/SkRecordDraw.cpp:52
    #15 0xa6733b in SkBigPicture::playback(SkCanvas*, SkPicture::AbortCallback*) const src/third_party/skia/src/core/SkBigPicture.cpp:33:5
    #16 0x92f590 in SkCanvas::onDrawPicture(SkPicture const*, SkMatrix const*, SkPaint const*) src/third_party/skia/src/core/SkCanvas.cpp:2824:14
    #17 0x92edc2 in SkCanvas::drawPicture(SkPicture const*, SkMatrix const*, SkPaint const*) src/third_party/skia/src/core/SkCanvas.cpp:2804:15
    #18 0xd2bdb7 in drawPicture src/third_party/skia/include/core/SkCanvas.h:2132:15
    #19 0xd2bdb7 in drawPicture src/third_party/skia/include/core/SkCanvas.h:2144
    #20 0xd2bdb7 in SkPictureImageFilter::onFilterImage(SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const src/third_party/skia/src/effects/SkPictureImageFilter.cpp:126
    #21 0x9bf387 in SkImageFilter::filterImage(SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const src/third_party/skia/src/core/SkImageFilter.cpp:213:40
    #22 0x9c46b7 in SkImageFilter::filterInput(int, SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const src/third_party/skia/src/core/SkImageFilter.cpp:512:41
    #23 0xd7dfb5 in SkMatrixConvolutionImageFilter::onFilterImage(SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const src/third_party/skia/src/effects/SkMatrixConvolutionImageFilter.cpp:290:39
    #24 0x9bf387 in SkImageFilter::filterImage(SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const src/third_party/skia/src/core/SkImageFilter.cpp:213:40
    #25 0x935e13 in SkBitmapDevice::drawSpecial(SkSpecialImage*, int, int, SkPaint const&, SkImage*, SkMatrix const&) src/third_party/skia/src/core/SkBitmapDevice.cpp:421:33
    #26 0x90be7d in SkCanvas::internalDrawDevice(SkBaseDevice*, int, int, SkPaint const*, SkImage*, SkMatrix const&) src/third_party/skia/src/core/SkCanvas.cpp:1313:25
    #27 0x907d58 in SkCanvas::internalRestore() src/third_party/skia/src/core/SkCanvas.cpp:1201:19
    #28 0x923188 in ~AutoDrawLooper src/third_party/skia/src/core/SkCanvas.cpp:495:22
    #29 0x923188 in SkCanvas::onDrawBitmap(SkBitmap const&, float, float, SkPaint const*) src/third_party/skia/src/core/SkCanvas.cpp:2308
    #30 0x917e6f in SkCanvas::drawBitmap(SkBitmap const&, float, float, SkPaint const*) src/third_party/skia/src/core/SkCanvas.cpp:1831:11
    #31 0x62051f in RunTestCase src/skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:48:13
    #32 0x62051f in ReadAndRunTestCase src/skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:67
    #33 0x62051f in main src/skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:87
    #34 0x7f165e6b482f in __libc_start_main /build/glibc-bfm8X4/glibc-2.23/csu/../csu/libc-start.c:291

0x60300000068a is located 0 bytes to the right of 26-byte region [0x603000000670,0x60300000068a)
allocated by thread T0 here:
    #0 0x5f2d33 in __interceptor_malloc /b/build/slave/linux_upload_clang/build/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cc:88:3
    #1 0x8ea1bd in sk_malloc_throw(unsigned long) src/skia/ext/SkMemory_new_handler.cpp:64:66
    #2 0x988ddf in Alloc src/third_party/skia/src/core/SkAAClip.cpp:77:35
    #3 0x988ddf in AllocRect src/third_party/skia/src/core/SkAAClip.cpp:99
    #4 0x988ddf in SkAAClip::setRect(SkIRect const&) src/third_party/skia/src/core/SkAAClip.cpp:721
    #5 0x98aa79 in SkAAClip::setRegion(SkRegion const&) src/third_party/skia/src/core/SkAAClip.cpp:788:22
    #6 0xa91023 in SkRasterClip::op(SkRegion const&, SkRegion::Op) src/third_party/skia/src/core/SkRasterClip.cpp:319:13
    #7 0x9389a1 in clipRegion src/third_party/skia/src/core/SkRasterClipStack.h:120:29
    #8 0x9389a1 in SkBitmapDevice::onClipRegion(SkRegion const&, SkClipOp) src/third_party/skia/src/core/SkBitmapDevice.cpp:564
    #9 0x911c0e in clipRegion src/third_party/skia/src/core/SkDevice.h:116:15
    #10 0x911c0e in SkCanvas::onClipRegion(SkRegion const&, SkClipOp) src/third_party/skia/src/core/SkCanvas.cpp:1496
    #11 0xaa7ca2 in draw<SkRecords::ClipRegion> src/third_party/skia/src/core/SkRecordDraw.cpp:92:1
    #12 0xaa7ca2 in operator()<SkRecords::ClipRegion> src/third_party/skia/src/core/SkRecordDraw.h:62
    #13 0xaa7ca2 in decltype ({parm#1}((SkRecords::NoOp)())) SkRecord::Record::visit<SkRecords::Draw&>(SkRecords::Draw&) const src/third_party/skia/src/core/SkRecord.h:165
    #14 0xaa5daa in visit<SkRecords::Draw &> src/third_party/skia/src/core/SkRecord.h:42:28
    #15 0xaa5daa in SkRecordDraw(SkRecord const&, SkCanvas*, SkPicture const* const*, SkDrawable* const*, int, SkBBoxHierarchy const*, SkPicture::AbortCallback*) src/third_party/skia/src/core/SkRecordDraw.cpp:52
    #16 0xa6733b in SkBigPicture::playback(SkCanvas*, SkPicture::AbortCallback*) const src/third_party/skia/src/core/SkBigPicture.cpp:33:5
    #17 0x92f590 in SkCanvas::onDrawPicture(SkPicture const*, SkMatrix const*, SkPaint const*) src/third_party/skia/src/core/SkCanvas.cpp:2824:14
    #18 0x92edc2 in SkCanvas::drawPicture(SkPicture const*, SkMatrix const*, SkPaint const*) src/third_party/skia/src/core/SkCanvas.cpp:2804:15
    #19 0xd2bdb7 in drawPicture src/third_party/skia/include/core/SkCanvas.h:2132:15
    #20 0xd2bdb7 in drawPicture src/third_party/skia/include/core/SkCanvas.h:2144
    #21 0xd2bdb7 in SkPictureImageFilter::onFilterImage(SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const src/third_party/skia/src/effects/SkPictureImageFilter.cpp:126
    #22 0x9bf387 in SkImageFilter::filterImage(SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const src/third_party/skia/src/core/SkImageFilter.cpp:213:40
    #23 0x9c46b7 in SkImageFilter::filterInput(int, SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const src/third_party/skia/src/core/SkImageFilter.cpp:512:41
    #24 0xd7dfb5 in SkMatrixConvolutionImageFilter::onFilterImage(SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const src/third_party/skia/src/effects/SkMatrixConvolutionImageFilter.cpp:290:39
    #25 0x9bf387 in SkImageFilter::filterImage(SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const src/third_party/skia/src/core/SkImageFilter.cpp:213:40
    #26 0x935e13 in SkBitmapDevice::drawSpecial(SkSpecialImage*, int, int, SkPaint const&, SkImage*, SkMatrix const&) src/third_party/skia/src/core/SkBitmapDevice.cpp:421:33
    #27 0x90be7d in SkCanvas::internalDrawDevice(SkBaseDevice*, int, int, SkPaint const*, SkImage*, SkMatrix const&) src/third_party/skia/src/core/SkCanvas.cpp:1313:25
    #28 0x907d58 in SkCanvas::internalRestore() src/third_party/skia/src/core/SkCanvas.cpp:1201:19
    #29 0x923188 in ~AutoDrawLooper src/third_party/skia/src/core/SkCanvas.cpp:495:22
    #30 0x923188 in SkCanvas::onDrawBitmap(SkBitmap const&, float, float, SkPaint const*) src/third_party/skia/src/core/SkCanvas.cpp:2308
    #31 0x917e6f in SkCanvas::drawBitmap(SkBitmap const&, float, float, SkPaint const*) src/third_party/skia/src/core/SkCanvas.cpp:1831:11
    #32 0x62051f in RunTestCase src/skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:48:13
    #33 0x62051f in ReadAndRunTestCase src/skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:67
    #34 0x62051f in main src/skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:87
    #35 0x7f165e6b482f in __libc_start_main /build/glibc-bfm8X4/glibc-2.23/csu/../csu/libc-start.c:291

SUMMARY: AddressSanitizer: heap-buffer-overflow src/third_party/skia/src/core/SkAAClip.cpp:894:17 in findX
Shadow bytes around the buggy address:
  0x0c067fff8080: fd fd fd fd fa fa fd fd fd fd fa fa fd fd fd fd
  0x0c067fff8090: fa fa fd fd fd fd fa fa 00 00 04 fa fa fa 00 00
  0x0c067fff80a0: 04 fa fa fa 00 00 04 fa fa fa fd fd fd fd fa fa
  0x0c067fff80b0: fd fd fd fa fa fa 00 00 00 00 fa fa fd fd fd fd
  0x0c067fff80c0: fa fa 00 00 00 00 fa fa fd fd fd fd fa fa 00 00
=>0x0c067fff80d0: 00[02]fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c067fff80e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c067fff80f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c067fff8100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c067fff8110: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c067fff8120: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==26009==ABORTING

## Attachments

- [poc](attachments/poc) (text/plain, 744 B)

## Timeline

### ct...@chromium.org (2017-12-29)

[Empty comment from Monorail migration]

[Monorail components: Internals>Skia]

### cl...@chromium.org (2017-12-31)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5906319537340416.

### cl...@chromium.org (2018-01-01)

Detailed report: https://clusterfuzz.com/testcase?key=5906319537340416

Job Type: linux_asan_filter_fuzz_stub
Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x60a00000171a
Crash State:
  SkAAClip::quickContains
  SkAAClip::op
  SkRasterClip::op
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_filter_fuzz_stub&range=522280:522288

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5906319537340416

See https://github.com/google/clusterfuzz-tools for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.


### sh...@chromium.org (2018-01-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-01)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-01-01)

[Empty comment from Monorail migration]

### rs...@chromium.org (2018-01-02)

[Empty comment from Monorail migration]

### rs...@chromium.org (2018-01-02)

reed: Can you take a look or help route?

Skia changelog: https://skia.googlesource.com/skia/+log/cad08c855e2373df3f0c53e943bad29dbd371d9c..409506c4c978ef116e9324b96ebf1d9f7e7da137?pretty=fuller&n=10000

### [Deleted User] (2018-01-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-01-03)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/9fc53624a09f6d3378b0a540832571dc1c31fbcd

commit 9fc53624a09f6d3378b0a540832571dc1c31fbcd
Author: Mike Reed <reed@google.com>
Date: Wed Jan 03 21:01:54 2018

check for irect with overflow width/height

Bug:798066
Change-Id: Iac324ac5a32fae241a528751c84279ce60ac4baf
Reviewed-on: https://skia-review.googlesource.com/90544
Reviewed-by: Mike Klein <mtklein@google.com>
Commit-Queue: Mike Reed <reed@google.com>

[modify] https://crrev.com/9fc53624a09f6d3378b0a540832571dc1c31fbcd/src/core/SkAAClip.cpp
[modify] https://crrev.com/9fc53624a09f6d3378b0a540832571dc1c31fbcd/tests/AAClipTest.cpp
[add] https://crrev.com/9fc53624a09f6d3378b0a540832571dc1c31fbcd/src/core/SkRectPriv.h
[modify] https://crrev.com/9fc53624a09f6d3378b0a540832571dc1c31fbcd/include/core/SkRect.h
[add] https://crrev.com/9fc53624a09f6d3378b0a540832571dc1c31fbcd/include/private/SkPedanticMath.h


### cl...@chromium.org (2018-01-04)

ClusterFuzz has detected this issue as fixed in range 526815:526830.

Detailed report: https://clusterfuzz.com/testcase?key=5906319537340416

Job Type: linux_asan_filter_fuzz_stub
Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x60a00000171a
Crash State:
  SkAAClip::quickContains
  SkAAClip::op
  SkRasterClip::op
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_filter_fuzz_stub&range=522280:522288
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_filter_fuzz_stub&range=526815:526830

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5906319537340416

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-01-04)

ClusterFuzz testcase 5906319537340416 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-01-04)

[Empty comment from Monorail migration]

### aw...@google.com (2018-01-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-01-12)

The VRP Panel decided to reward $500 for this report, due to the bug being of low value to an attacker.

### aw...@chromium.org (2018-01-12)

[Empty comment from Monorail migration]

### m....@gmail.com (2018-01-12)

[Comment Deleted]

### me...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-02-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/798066?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/798080]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090013)*
