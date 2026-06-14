# Security:  Out-Of-Bounds Write Vulnerability in Skia

| Field | Value |
|-------|-------|
| **Issue ID** | [40090924](https://issues.chromium.org/issues/40090924) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Reporter** | zh...@gmail.com |
| **Assignee** | re...@google.com |
| **Created** | 2018-03-27 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

This issue was found by fuzzing against a 64-bit asan linux build of filter\_fuzz\_stub.

**VERSION**  

Chrome Version: 66.0.3359.45 beta  

Operating System: Fedora 27 x86\_64

<https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-beta-66.0.3359.45.zip>

**REPRODUCTION CASE**

filter\_fuzz\_stub /tmp/SEGV-memset.fil

# [0327/133958.318030:INFO:filter\_fuzz\_stub.cc(60)] Test case: /tmp/SEGV-memset.fil [0327/133958.318821:INFO:filter\_fuzz\_stub.cc(37)] Valid stream detected. AddressSanitizer:DEADLYSIGNAL

==16342==ERROR: AddressSanitizer: SEGV on unknown address 0x7f7ade37b708 (pc 0x0000007d58d2 bp 0x7ffd9a659710 sp 0x7ffd9a659700 T0)  

==16342==The signal is caused by a WRITE memory access.  

#0 0x7d58d1 in memsetT<unsigned int> third\_party/skia/src/opts/SkUtils\_opts.h:29:23  

#1 0x7d58d1 in sse2::memset32(unsigned int\*, unsigned int, int) third\_party/skia/src/opts/SkUtils\_opts.h:37  

#2 0x8f8c81 in vertline third\_party/skia/src/core/SkScan\_Hairline.cpp:31:18  

#3 0x8f8c81 in SkScan::HairLineRgn(SkPoint const\*, int, SkRegion const\*, SkBlitter\*) third\_party/skia/src/core/SkScan\_Hairline.cpp:140  

#4 0x8fa7ad in void hair\_path<(SkPaint::Cap)0>(SkPath const&, SkRasterClip const&, SkBlitter\*, void (\*)(SkPoint const\*, int, SkRegion const\*, SkBlitter\*)) third\_party/skia/src/core/SkScan\_Hairline.cpp:551:17  

#5 0x719e30 in SkDraw::drawDevPath(SkPath const&, SkPaint const&, bool, SkBlitter\*, bool, SkInitOnceData\*) const third\_party/skia/src/core/SkDraw.cpp:1028:9  

#6 0x71b77b in SkDraw::drawPath(SkPath const&, SkPaint const&, SkMatrix const\*, bool, bool, SkBlitter\*, SkInitOnceData\*) const third\_party/skia/src/core/SkDraw.cpp:1141:11  

#7 0x716ba5 in drawPath third\_party/skia/src/core/SkDraw.h:58:15  

#8 0x716ba5 in SkDraw::drawPoints(SkCanvas::PointMode, unsigned long, SkPoint const\*, SkPaint const&, SkBaseDevice\*) const third\_party/skia/src/core/SkDraw.cpp:663  

#9 0x651832 in SkBitmapDevice::drawPoints(SkCanvas::PointMode, unsigned long, SkPoint const\*, SkPaint const&) third\_party/skia/src/core/SkBitmapDevice.cpp:195:18  

#10 0x6a08d4 in SkCanvas::onDrawPoints(SkCanvas::PointMode, unsigned long, SkPoint const\*, SkPaint const&) third\_party/skia/src/core/SkCanvas.cpp:2004:23  

#11 0x6997e3 in SkCanvas::drawPoints(SkCanvas::PointMode, unsigned long, SkPoint const\*, SkPaint const&) third\_party/skia/src/core/SkCanvas.cpp:1740:11  

#12 0x864c57 in draw[SkRecords::DrawPoints](javascript:void(0);) third\_party/skia/src/core/SkRecordDraw.cpp:117:1  

#13 0x864c57 in operator()[SkRecords::DrawPoints](javascript:void(0);) third\_party/skia/src/core/SkRecordDraw.h:62  

#14 0x864c57 in decltype ({parm#1}((SkRecords::NoOp)())) SkRecord::Record::visit[SkRecords::Draw&](javascript:void(0);)(SkRecords::Draw&) const third\_party/skia/src/core/SkRecord.h:165  

#15 0x862afa in visit<SkRecords::Draw &> third\_party/skia/src/core/SkRecord.h:42:28  

#16 0x862afa in SkRecordDraw(SkRecord const&, SkCanvas\*, SkPicture const\* const\*, SkDrawable\* const\*, int, SkBBoxHierarchy const\*, SkPicture::AbortCallback\*) third\_party/skia/src/core/SkRecordDraw.cpp:52  

#17 0x644acb in SkBigPicture::playback(SkCanvas\*, SkPicture::AbortCallback\*) const third\_party/skia/src/core/SkBigPicture.cpp:33:5  

#18 0x6b401d in SkCanvas::onDrawPicture(SkPicture const\*, SkMatrix const\*, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:2835:14  

#19 0x6b38df in SkCanvas::drawPicture(SkPicture const\*, SkMatrix const\*, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:2815:15  

#20 0xb771ba in drawPicture third\_party/skia/include/core/SkCanvas.h:2127:15  

#21 0xb771ba in drawPicture third\_party/skia/include/core/SkCanvas.h:2139  

#22 0xb771ba in SkPictureImageFilter::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkPictureImageFilter.cpp:118  

#23 0x769a30 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:214:40  

#24 0x76ee00 in SkImageFilter::filterInput(int, SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:513:41  

#25 0xb6192d in SkMergeImageFilter::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkMergeImageFilter.cpp:47:27  

#26 0x769a30 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:214:40  

#27 0x76ee00 in SkImageFilter::filterInput(int, SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:513:41  

#28 0xb11f3b in SkColorFilterImageFilter::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkColorFilterImageFilter.cpp:65:39  

#29 0x769a30 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:214:40  

#30 0x654e64 in SkBitmapDevice::drawSpecial(SkSpecialImage\*, int, int, SkPaint const&, SkImage\*, SkMatrix const&) third\_party/skia/src/core/SkBitmapDevice.cpp:432:33  

#31 0x69099d in SkCanvas::internalDrawDevice(SkBaseDevice\*, int, int, SkPaint const\*, SkImage\*, SkMatrix const&) third\_party/skia/src/core/SkCanvas.cpp:1310:25  

#32 0x68c500 in SkCanvas::internalRestore() third\_party/skia/src/core/SkCanvas.cpp:1198:19  

#33 0x6a7ec6 in ~AutoDrawLooper third\_party/skia/src/core/SkCanvas.cpp:496:22  

#34 0x6a7ec6 in SkCanvas::onDrawBitmap(SkBitmap const&, float, float, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:2318  

#35 0x69c913 in SkCanvas::drawBitmap(SkBitmap const&, float, float, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:1838:11  

#36 0x633d78 in RunTestCase skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:47:13  

#37 0x633d78 in ReadAndRunTestCase skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:66  

#38 0x633d78 in main skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:86  

#39 0x7f7ae8114f29 in \_\_libc\_start\_main (/lib64/libc.so.6+0x20f29)

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: SEGV third\_party/skia/src/opts/SkUtils\_opts.h:29:23 in memsetT<unsigned int>  

==16342==ABORTING

Testcase is in the attachment.

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### el...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

[Monorail components: Internals>Skia]

### in...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-03-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5740614239649792.

### in...@chromium.org (2018-03-27)

Uploaded to filter_fuzz_stub in https://clusterfuzz.com/v2/testcase-detail/5740614239649792
Uploaded to oss-fuzz image_filter_deserialize in https://oss-fuzz.com/v2/testcase-detail/5103681935507456

### in...@chromium.org (2018-03-27)

Weirdly, this is only reproducing on beta, not on tip-of-tree trunk. Might be some of the HairLineRgn fixes w.r.t integer overflow on OSS-Fuzz. Kevin, looks like skia fuzzers already caught this ?

### mm...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-28)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2018-03-28)

Please add affected OSs.

### go...@chromium.org (2018-03-28)

Pls apply appropriate OSs label. Thank you.

### mm...@chromium.org (2018-03-28)

[Empty comment from Monorail migration]

### kj...@chromium.org (2018-03-29)

From my records, this was found and fixed in https://bugs.chromium.org/p/skia/issues/detail?id=7483

### kj...@chromium.org (2018-03-29)

(That is, it was fixed around Jan 17 2018)

### hc...@chromium.org (2018-04-03)

Trying to figure out what to do with this one- the fix should already be in 66 but the reporter saw the bug there.  Our fuzzers are not reproducing now.  Let's remove RBS.  Interested in whether the reporter still sees this?

### zh...@gmail.com (2018-04-04)

It's not just me saw the bug, infe...@chromium.org also comfired that the bug existed in 66.0.3359.45 beta (please see https://bugs.chromium.org/p/chromium/issues/detail?id=826166#c5)

I tested the poc with the latest beta asan build and found the bug still exists.

https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-beta-66.0.3359.66.zip?generation=1522335298641665&alt=media

> sha1sum asan-linux-beta-66.0.3359.66.zip 
ceaf0c37ceca8b51439708608d9610066b2c3960  asan-linux-beta-66.0.3359.66.zip

I think something maybe wrong that led the bug roll back, it maybe hard to figure out the root cause. 

asan-linux-beta-66.0.3359.66 ./filter_fuzz_stub /tmp/SEGV-memset.fil 
[0404/093658.927074:INFO:filter_fuzz_stub.cc(60)] Test case: /tmp/SEGV-memset.fil
[0404/093658.927881:INFO:filter_fuzz_stub.cc(37)] Valid stream detected.
AddressSanitizer:DEADLYSIGNAL
=================================================================
==6896==ERROR: AddressSanitizer: SEGV on unknown address 0x7fe20527b708 (pc 0x0000007d58d2 bp 0x7ffe5cb969b0 sp 0x7ffe5cb969a0 T0)
==6896==The signal is caused by a WRITE memory access.
    #0 0x7d58d1 in memsetT<unsigned int> third_party/skia/src/opts/SkUtils_opts.h:29:23
    #1 0x7d58d1 in sse2::memset32(unsigned int*, unsigned int, int) third_party/skia/src/opts/SkUtils_opts.h:37
    #2 0x8f8c81 in vertline third_party/skia/src/core/SkScan_Hairline.cpp:31:18
    #3 0x8f8c81 in SkScan::HairLineRgn(SkPoint const*, int, SkRegion const*, SkBlitter*) third_party/skia/src/core/SkScan_Hairline.cpp:140
    #4 0x8fa7ad in void hair_path<(SkPaint::Cap)0>(SkPath const&, SkRasterClip const&, SkBlitter*, void (*)(SkPoint const*, int, SkRegion const*, SkBlitter*)) third_party/skia/src/core/SkScan_Hairline.cpp:551:17
    #5 0x719e30 in SkDraw::drawDevPath(SkPath const&, SkPaint const&, bool, SkBlitter*, bool, SkInitOnceData*) const third_party/skia/src/core/SkDraw.cpp:1028:9
    #6 0x71b77b in SkDraw::drawPath(SkPath const&, SkPaint const&, SkMatrix const*, bool, bool, SkBlitter*, SkInitOnceData*) const third_party/skia/src/core/SkDraw.cpp:1141:11
    #7 0x716ba5 in drawPath third_party/skia/src/core/SkDraw.h:58:15
    #8 0x716ba5 in SkDraw::drawPoints(SkCanvas::PointMode, unsigned long, SkPoint const*, SkPaint const&, SkBaseDevice*) const third_party/skia/src/core/SkDraw.cpp:663
    #9 0x651832 in SkBitmapDevice::drawPoints(SkCanvas::PointMode, unsigned long, SkPoint const*, SkPaint const&) third_party/skia/src/core/SkBitmapDevice.cpp:195:18
    #10 0x6a08d4 in SkCanvas::onDrawPoints(SkCanvas::PointMode, unsigned long, SkPoint const*, SkPaint const&) third_party/skia/src/core/SkCanvas.cpp:2004:23
    #11 0x6997e3 in SkCanvas::drawPoints(SkCanvas::PointMode, unsigned long, SkPoint const*, SkPaint const&) third_party/skia/src/core/SkCanvas.cpp:1740:11
    #12 0x864c57 in draw<SkRecords::DrawPoints> third_party/skia/src/core/SkRecordDraw.cpp:117:1
    #13 0x864c57 in operator()<SkRecords::DrawPoints> third_party/skia/src/core/SkRecordDraw.h:62
    #14 0x864c57 in decltype ({parm#1}((SkRecords::NoOp)())) SkRecord::Record::visit<SkRecords::Draw&>(SkRecords::Draw&) const third_party/skia/src/core/SkRecord.h:165
    #15 0x862afa in visit<SkRecords::Draw &> third_party/skia/src/core/SkRecord.h:42:28
    #16 0x862afa in SkRecordDraw(SkRecord const&, SkCanvas*, SkPicture const* const*, SkDrawable* const*, int, SkBBoxHierarchy const*, SkPicture::AbortCallback*) third_party/skia/src/core/SkRecordDraw.cpp:52
    #17 0x644acb in SkBigPicture::playback(SkCanvas*, SkPicture::AbortCallback*) const third_party/skia/src/core/SkBigPicture.cpp:33:5
    #18 0x6b401d in SkCanvas::onDrawPicture(SkPicture const*, SkMatrix const*, SkPaint const*) third_party/skia/src/core/SkCanvas.cpp:2835:14
    #19 0x6b38df in SkCanvas::drawPicture(SkPicture const*, SkMatrix const*, SkPaint const*) third_party/skia/src/core/SkCanvas.cpp:2815:15
    #20 0xb771ba in drawPicture third_party/skia/include/core/SkCanvas.h:2127:15
    #21 0xb771ba in drawPicture third_party/skia/include/core/SkCanvas.h:2139
    #22 0xb771ba in SkPictureImageFilter::onFilterImage(SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const third_party/skia/src/effects/SkPictureImageFilter.cpp:118
    #23 0x769a30 in SkImageFilter::filterImage(SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const third_party/skia/src/core/SkImageFilter.cpp:214:40
    #24 0x76ee00 in SkImageFilter::filterInput(int, SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const third_party/skia/src/core/SkImageFilter.cpp:513:41
    #25 0xb6192d in SkMergeImageFilter::onFilterImage(SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const third_party/skia/src/effects/SkMergeImageFilter.cpp:47:27
    #26 0x769a30 in SkImageFilter::filterImage(SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const third_party/skia/src/core/SkImageFilter.cpp:214:40
    #27 0x76ee00 in SkImageFilter::filterInput(int, SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const third_party/skia/src/core/SkImageFilter.cpp:513:41
    #28 0xb11f3b in SkColorFilterImageFilter::onFilterImage(SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const third_party/skia/src/effects/SkColorFilterImageFilter.cpp:65:39
    #29 0x769a30 in SkImageFilter::filterImage(SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const third_party/skia/src/core/SkImageFilter.cpp:214:40
    #30 0x654e64 in SkBitmapDevice::drawSpecial(SkSpecialImage*, int, int, SkPaint const&, SkImage*, SkMatrix const&) third_party/skia/src/core/SkBitmapDevice.cpp:432:33
    #31 0x69099d in SkCanvas::internalDrawDevice(SkBaseDevice*, int, int, SkPaint const*, SkImage*, SkMatrix const&) third_party/skia/src/core/SkCanvas.cpp:1310:25
    #32 0x68c500 in SkCanvas::internalRestore() third_party/skia/src/core/SkCanvas.cpp:1198:19
    #33 0x6a7ec6 in ~AutoDrawLooper third_party/skia/src/core/SkCanvas.cpp:496:22
    #34 0x6a7ec6 in SkCanvas::onDrawBitmap(SkBitmap const&, float, float, SkPaint const*) third_party/skia/src/core/SkCanvas.cpp:2318
    #35 0x69c913 in SkCanvas::drawBitmap(SkBitmap const&, float, float, SkPaint const*) third_party/skia/src/core/SkCanvas.cpp:1838:11
    #36 0x633d78 in RunTestCase skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:47:13
    #37 0x633d78 in ReadAndRunTestCase skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:66
    #38 0x633d78 in main skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:86
    #39 0x7fe20f072f29 in __libc_start_main (/lib64/libc.so.6+0x20f29)

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV third_party/skia/src/opts/SkUtils_opts.h:29:23 in memsetT<unsigned int>



### kj...@chromium.org (2018-04-04)

I may have been a little hasty with #11 and #12.  It was a similar looking bug, but not the same.

I checked out Skia at chrome/m66, compiled the "fuzz" executable with ASAN and was able to reproduce.  

out/ASAN/fuzz -t filter_fuzz -b ~/Downloads/SEGV-memset.fil

Doing the same with Skia at ToT (master), the fuzz input does not reproduce. 

git bisect pointed the finger at https://github.com/google/skia/commit/b5e1f7558052cc60deaf23ccc2c898d1c6c94c09 as the fix in master.  

That CL references https://github.com/google/skia/commit/c7fbda95404a9422d0dd762d35383d5a61e89440 as a necessary prerequisite.  When I patch both of those to chrome/m66 the fuzz no longer crashes.

Assigning to reed@ as he was the original author of the two CLs that fix this bug.

### kj...@chromium.org (2018-04-04)

One more thing, at chrome/m65 and chrome/m64 the fuzz input does not crash, so I do not believe those two releases to be affected. 

This may be due to a change in the serialization format between m65 and m66, but I am not certain.

### sh...@chromium.org (2018-04-04)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ji...@chromium.org (2018-04-04)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-04-04)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/81fdfc0b797e1acdc40cf09db65f37694c5cc59a

commit 81fdfc0b797e1acdc40cf09db65f37694c5cc59a
Author: Mike Reed <reed@google.com>
Date: Wed Apr 04 19:41:15 2018

chop down huge rects before hairlining

Bug: 826166
Change-Id: I18f4b1dc4f279e37832d4bced0a66b5c356d09c0
Reviewed-on: https://skia-review.googlesource.com/112572
Reviewed-by: Yuqian Li <liyuqian@google.com>
Commit-Queue: Mike Reed <reed@google.com>
(cherry picked from commit c7fbda95404a9422d0dd762d35383d5a61e89440)
Reviewed-on: https://skia-review.googlesource.com/118720
Reviewed-by: Kevin Lubick <kjlubick@google.com>

[modify] https://crrev.com/81fdfc0b797e1acdc40cf09db65f37694c5cc59a/src/core/SkScan_Hairline.cpp


### bu...@chromium.org (2018-04-04)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/773868fdade5f9f0e7697e6d09c9bd80aaa9b402

commit 773868fdade5f9f0e7697e6d09c9bd80aaa9b402
Author: Mike Reed <reed@google.com>
Date: Wed Apr 04 20:08:34 2018

Revert "Revert "add tiler for SkDraw""

This reverts commit 461ef7af88cc966007c464130a971ec86c803f1d.

Prev CL to SkScan_Hairline.cpp fixed the bug that caused the earlier revert.

Bug: 826166
Change-Id: Ifd9a364c7546175be292f726e19465b72196b45e
Reviewed-on: https://skia-review.googlesource.com/112723
Reviewed-by: Mike Reed <reed@google.com>
Commit-Queue: Mike Reed <reed@google.com>
(cherry picked from commit b5e1f7558052cc60deaf23ccc2c898d1c6c94c09)
Reviewed-on: https://skia-review.googlesource.com/118740
Reviewed-by: Kevin Lubick <kjlubick@google.com>

[delete] https://crrev.com/81fdfc0b797e1acdc40cf09db65f37694c5cc59a/tests/DeviceLooperTest.cpp
[modify] https://crrev.com/773868fdade5f9f0e7697e6d09c9bd80aaa9b402/src/core/SkBitmapDevice.h
[delete] https://crrev.com/81fdfc0b797e1acdc40cf09db65f37694c5cc59a/src/core/SkDeviceLooper.cpp
[modify] https://crrev.com/773868fdade5f9f0e7697e6d09c9bd80aaa9b402/gn/tests.gni
[delete] https://crrev.com/81fdfc0b797e1acdc40cf09db65f37694c5cc59a/src/core/SkDeviceLooper.h
[modify] https://crrev.com/773868fdade5f9f0e7697e6d09c9bd80aaa9b402/src/core/SkDraw.cpp
[modify] https://crrev.com/773868fdade5f9f0e7697e6d09c9bd80aaa9b402/gm/hugepath.cpp
[modify] https://crrev.com/773868fdade5f9f0e7697e6d09c9bd80aaa9b402/src/core/SkBitmapDevice.cpp
[modify] https://crrev.com/773868fdade5f9f0e7697e6d09c9bd80aaa9b402/gn/core.gni


### kj...@chromium.org (2018-04-05)

With those two cherry-picks, the original test case no longer repros on the chrome/m66 branch of skia.

### sh...@chromium.org (2018-04-05)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-04-20)

Nice one, zhouzhenster@ - the VRP panel decided to award $3,000 for this report. A member of our finance team will be in touch to arrange payment.

Also, how would you like to be credited in Chrome release notes?

### aw...@chromium.org (2018-04-20)

[Empty comment from Monorail migration]

### zh...@gmail.com (2018-04-21)

[Comment Deleted]

### aw...@google.com (2018-04-23)

Hi Zhen - thanks for the info. I'm sorry to say that we only issue CVEs to bugs found in our stable shipping products. This was found while Chrome 66 was still in Beta, and I don't believe was present in Chrome 65, which was stable at the time. 

### aw...@google.com (2018-04-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-07-12)

This issue was migrated from crbug.com/chromium/826166?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/828707]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090924)*
