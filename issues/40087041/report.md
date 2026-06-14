# Security: SEGV on unknown address 0x7f9b9b71c828 in (anonymous namespace)::PixelAccessor

| Field | Value |
|-------|-------|
| **Issue ID** | [40087041](https://issues.chromium.org/issues/40087041) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sw...@gmail.com |
| **Assignee** | he...@google.com |
| **Created** | 2017-03-13 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Please check the ASAN output.

# ./filter\_fuzz\_stub segv\_poc.fil [0313/134257.283049:INFO:filter\_fuzz\_stub.cc(59)] Test case: segv\_poc.fil [0313/134257.283703:INFO:filter\_fuzz\_stub.cc(36)] Valid stream detected. ASAN:DEADLYSIGNAL

==11224==ERROR: AddressSanitizer: SEGV on unknown address 0x7f9b9b71c828 (pc 0x000000d46290 bp 0x7fff50de2050 sp 0x7fff50de2040 T0)  

==11224==The signal is caused by a READ memory access.  

#0 0xd4628f in (anonymous namespace)::PixelAccessor<(SkColorType)3, (SkGammaType)0>::getPixelFromRow(void const\*, int) const third\_party/skia/src/core/SkLinearBitmapPipeline\_sample.h:277:34  

#1 0xd6a01a in getPixelFromRow third\_party/skia/src/core/SkLinearBitmapPipeline\_sample.h:216:32  

#2 0xd6a01a in operator() third\_party/skia/src/core/SkLinearBitmapPipeline\_sample.h:407  

#3 0xd6a01a in spanSlowRate third\_party/skia/src/core/SkLinearBitmapPipeline\_sample.h:418  

#4 0xd6a01a in (anonymous namespace)::NearestNeighborSampler<(anonymous namespace)::PixelAccessorShim, SkLinearBitmapPipeline::BlendProcessorInterface>::pointSpan((anonymous namespace)::Span) third\_party/skia/src/core/SkLinearBitmapPipeline\_sample.h:369  

#5 0xd36dec in bool (anonymous namespace)::XClampStrategy::maybeProcessSpan[SkLinearBitmapPipeline::SampleProcessorInterface](javascript:void(0);)((anonymous namespace)::Span, SkLinearBitmapPipeline::SampleProcessorInterface\*) third\_party/skia/src/core/SkLinearBitmapPipeline\_tile.h  

#6 0xd369c3 in (anonymous namespace)::CombinedTileStage<(anonymous namespace)::XClampStrategy, (anonymous namespace)::YClampStrategy, SkLinearBitmapPipeline::SampleProcessorInterface>::pointSpan((anonymous namespace)::Span) third\_party/skia/src/core/SkLinearBitmapPipeline.cpp:132:25  

#7 0xc9b080 in LinearPipelineContext::shadeSpan(int, int, unsigned int\*, int) third\_party/skia/src/core/SkBitmapProcShader.cpp:140:30  

#8 0xcb8172 in SkARGB32\_Shader\_Blitter::blitRect(int, int, int, int) third\_party/skia/src/core/SkBlitter\_ARGB32.cpp:405:28  

#9 0x7fb45c in blitrect third\_party/skia/src/core/SkScan.cpp:22:14  

#10 0x7fb45c in SkScan::FillIRect(SkIRect const&, SkRegion const\*, SkBlitter\*) third\_party/skia/src/core/SkScan.cpp:37  

#11 0x7fc27a in FillRect third\_party/skia/src/core/SkScan.cpp:68:5  

#12 0x7fc27a in SkScan::FillRect(SkRect const&, SkRasterClip const&, SkBlitter\*) third\_party/skia/src/core/SkScan.cpp:110  

#13 0x6ae1df in SkDraw::drawRect(SkRect const&, SkPaint const&, SkMatrix const\*, SkRect const\*) const third\_party/skia/src/core/SkDraw.cpp:850:21  

#14 0xc968e1 in SkBitmapDevice::drawBitmapRect(SkDraw const&, SkBitmap const&, SkRect const\*, SkRect const&, SkPaint const&, SkCanvas::SrcRectConstraint) third\_party/skia/src/core/SkBitmapDevice.cpp:363:11  

#15 0x6a2584 in SkBaseDevice::drawImageRect(SkDraw const&, SkImage const\*, SkRect const\*, SkRect const&, SkPaint const&, SkCanvas::SrcRectConstraint) third\_party/skia/src/core/SkDevice.cpp:187:15  

#16 0x58a09b in SkCanvas::onDrawImageRect(SkImage const\*, SkRect const\*, SkRect const&, SkPaint const\*, SkCanvas::SrcRectConstraint) third\_party/skia/src/core/SkCanvas.cpp:2461:23  

#17 0xf45a0c in SkImageSource::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkImageSource.cpp:126:13  

#18 0x6cc579 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:216:40  

#19 0xc974c6 in SkBitmapDevice::drawSpecial(SkDraw const&, SkSpecialImage\*, int, int, SkPaint const&) third\_party/skia/src/core/SkBitmapDevice.cpp:417:49  

#20 0x58b1d8 in SkCanvas::onDrawBitmap(SkBitmap const&, float, float, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:2510:27  

#21 0x4fb6a3 in RunTestCase skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:46:13  

#22 0x4fb6a3 in ReadAndRunTestCase skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:65  

#23 0x4fb6a3 in main skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:84  

#24 0x7f9b9e52382f in \_\_libc\_start\_main /build/glibc-t3gR2i/glibc-2.23/csu/../csu/libc-start.c:291

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: SEGV third\_party/skia/src/core/SkLinearBitmapPipeline\_sample.h:277:34 in (anonymous namespace)::PixelAccessor<(SkColorType)3, (SkGammaType)0>::getPixelFromRow(void const\*, int) const  

==11224==ABORTING

**VERSION**  

Chrome Version: asan-linux-release-454783  

Operating System:

- Ubuntu 16.04.1 LTS 64bit (Server)
- Linux ubuntu 4.4.0-53-generic #74-Ubuntu SMP Fri Dec 2 15:59:10 UTC 2016 x86\_64 x86\_64 x86\_64 GNU/Linux

**REPRODUCTION CASE**

- ./filter\_fuzz\_stub ./segv\_poc.fil

## Attachments

- [segv_poc.fil](attachments/segv_poc.fil) (application/octet-stream, 164 B)

## Timeline

### pa...@chromium.org (2017-03-14)

[Empty comment from Monorail migration]

[Monorail components: Internals>Skia]

### ts...@chromium.org (2017-03-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-15)

[Empty comment from Monorail migration]

### hc...@google.com (2017-03-16)

Is this only happening on 57 or also 58-59 builds?

+herb to start

### he...@google.com (2017-03-16)

I see that this goes through Clamp x Clamp tiling. I fixed a couple of bugs in the 57 timeframe 

### he...@google.com (2017-03-16)

Please disregard previous https://crbug.com/chromium/700836#c5. I was really just trying to add Robert.

### he...@google.com (2017-03-16)

[Empty comment from Monorail migration]

### he...@google.com (2017-03-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-03-16)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/a839fc0b63bd68682dcf51abc77078bfea48c1a1

commit a839fc0b63bd68682dcf51abc77078bfea48c1a1
Author: Herb Derby <herb@google.com>
Date: Thu Mar 16 19:25:57 2017

Add Chromium's fuzz_fileter_fuzz to skia.

Move the fuzzer in
chromium/src/skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc
to Skia's fuzzer.

I recommend removing filter_fuzz_stub from chromium and only
using Skia's fuzzer.

BUG=chromium:700836

Change-Id: Ibab1a9b696e54a3042ee61f5524d196c12df2888
Reviewed-on: https://skia-review.googlesource.com/9802
Commit-Queue: Herb Derby <herb@google.com>
Reviewed-by: Kevin Lubick <kjlubick@google.com>

[modify] https://crrev.com/a839fc0b63bd68682dcf51abc77078bfea48c1a1/fuzz/fuzz.cpp


### bu...@chromium.org (2017-03-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b34f3b53e493015117dc3800847ef91013fe1956

commit b34f3b53e493015117dc3800847ef91013fe1956
Author: skia-deps-roller@chromium.org <skia-deps-roller@chromium.org>
Date: Thu Mar 16 20:46:00 2017

Roll src/third_party/skia/ be4eed2ef..a839fc0b6 (6 commits)

https://skia.googlesource.com/skia.git/+log/be4eed2ef77d..a839fc0b63bd

$ git log be4eed2ef..a839fc0b6 --date=short --no-merges --format='%ad %ae %s'
2017-03-16 herb Add Chromium's fuzz_fileter_fuzz to skia.
2017-03-16 bsalomon Revert "Revert "Revert "Detect Chrome either by renderer or version strings."""
2017-03-16 bsalomon Revert "Revert "Detect Chrome either by renderer or version strings.""
2017-03-16 reed Revert[4] "store vertices arrays inline with object""""
2017-03-16 bsalomon Remove GrPipeline from GrDrawOp.
2017-03-16 bsalomon Revert "Detect Chrome either by renderer or version strings."

Created with:
  roll-dep src/third_party/skia
BUG=700836


Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, see:
http://www.chromium.org/developers/tree-sheriffs/sheriff-details-chromium#TOC-Failures-due-to-DEPS-rolls


CQ_INCLUDE_TRYBOTS=master.tryserver.blink:linux_trusty_blink_rel
TBR=borenet@chromium.org

Change-Id: I5fdc28b89065cdb024fd70a36d009071202d06b2
Reviewed-on: https://chromium-review.googlesource.com/456739
Reviewed-by: Skia Deps Roller <skia-deps-roller@chromium.org>
Commit-Queue: Skia Deps Roller <skia-deps-roller@chromium.org>
Cr-Commit-Position: refs/heads/master@{#457541}
[modify] https://crrev.com/b34f3b53e493015117dc3800847ef91013fe1956/DEPS


### he...@google.com (2017-03-16)

The fuzzer created a bitmap more than 32K pixels wide. This caused an overflow while using 16.16 fixed point arithmetic. This caused an overflow in the sampler. The code now uses 48.16 fixed point arithmetic. 

### bu...@chromium.org (2017-03-17)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/2fb3662364829555628196d4913971f933185d81

commit 2fb3662364829555628196d4913971f933185d81
Author: Herb Derby <herb@google.com>
Date: Fri Mar 17 14:39:20 2017

Fix overflow bug in slow span.

Fix an overflow in the address calculation in the sampler.

BUG=chromium:700836

Change-Id: Ifadbdc9541138219e8aec08c1342a241da75705c
Reviewed-on: https://skia-review.googlesource.com/9815
Reviewed-by: Mike Reed <reed@google.com>
Commit-Queue: Herb Derby <herb@google.com>

[modify] https://crrev.com/2fb3662364829555628196d4913971f933185d81/src/core/SkLinearBitmapPipeline_sample.h


### he...@google.com (2017-03-20)

[Empty comment from Monorail migration]

### pa...@chromium.org (2017-03-20)

I think you fixed it, herb. :)

### aw...@google.com (2017-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-23)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2017-03-28)

+ Andrew for approving security merges for M58. 

### am...@chromium.org (2017-03-29)

Approved for 58, please merge soon.

### bu...@chromium.org (2017-03-29)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/4a9b4143baed7ab31d426be12c31cb4082014bd5

commit 4a9b4143baed7ab31d426be12c31cb4082014bd5
Author: herb <herb@google.com>
Date: Wed Mar 29 16:57:15 2017

Fix overflow bug in slow span.

Fix an overflow in the address calculation in the sampler.

BUG=chromium:700836

TBR=hcm@google.com

Change-Id: Ifadbdc9541138219e8aec08c1342a241da75705c
Reviewed-on: https://skia-review.googlesource.com/9815
Reviewed-by: Mike Reed <reed@google.com>
Commit-Queue: Herb Derby <herb@google.com>
Reviewed-on: https://skia-review.googlesource.com/10479
Reviewed-by: Herb Derby <herb@google.com>

[modify] https://crrev.com/4a9b4143baed7ab31d426be12c31cb4082014bd5/src/core/SkLinearBitmapPipeline_sample.h


### he...@google.com (2017-03-29)

This change was added to the head of branch m58, and should be picked up by chrome.

### mb...@chromium.org (2017-03-29)

[Empty comment from Monorail migration]

### aw...@google.com (2017-03-31)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-31)

[Empty comment from Monorail migration]

### aw...@google.com (2017-03-31)

Nice one! The panel decided to award $1,000 for this bug.  Cheers!

### aw...@chromium.org (2017-03-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-03)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### he...@google.com (2017-04-03)

[Empty comment from Monorail migration]

### aw...@google.com (2017-04-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-04-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/700836?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087041)*
