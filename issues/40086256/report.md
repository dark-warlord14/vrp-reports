# Security: heap-buffer-overflow in SkAlphaThresholdFilterImpl::onFilterImage

| Field | Value |
|-------|-------|
| **Issue ID** | [40086256](https://issues.chromium.org/issues/40086256) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Reporter** | sw...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2016-12-17 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The OOB-Read bug exists in SkAlphaThresholdFilterImpl::onFilterImage.

- ASAN ouput  
  
  ===========================================================================================  
  
  ./filter\_fuzz\_stub poc1.fil  
  
  [1217/173144.153389:INFO:filter\_fuzz\_stub.cc(59)] Test case: poc1.fil  
  
  [1217/173144.154211:INFO:filter\_fuzz\_stub.cc(36)] Valid stream detected.  
  
  =================================================================  
  
  ==23992==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x6030000003f0 at pc 0x000000f5806d bp 0x7fff7f065f90 sp 0x7fff7f065f88  
  
  READ of size 4 at 0x6030000003f0 thread T0  
  
  #0 0xf5806c in SkAlphaThresholdFilterImpl::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkAlphaThresholdFilter.cpp:233:33  
  
  #1 0x637f59 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:215:40  
  
  #2 0x63e3b4 in SkImageFilter::filterInput(int, SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:462:41  
  
  #3 0xf556d3 in SkAlphaThresholdFilterImpl::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkAlphaThresholdFilter.cpp:136:39  
  
  #4 0x637f59 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:215:40  
  
  #5 0x63e3b4 in SkImageFilter::filterInput(int, SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:462:41  
  
  #6 0xf556d3 in SkAlphaThresholdFilterImpl::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkAlphaThresholdFilter.cpp:136:39  
  
  #7 0x637f59 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:215:40  
  
  #8 0x63e3b4 in SkImageFilter::filterInput(int, SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:462:41  
  
  #9 0xf556d3 in SkAlphaThresholdFilterImpl::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkAlphaThresholdFilter.cpp:136:39  
  
  #10 0x637f59 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:215:40  
  
  #11 0x63e3b4 in SkImageFilter::filterInput(int, SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:462:41  
  
  #12 0xf556d3 in SkAlphaThresholdFilterImpl::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkAlphaThresholdFilter.cpp:136:39  
  
  #13 0x637f59 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:215:40  
  
  #14 0x63e3b4 in SkImageFilter::filterInput(int, SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:462:41  
  
  #15 0xf556d3 in SkAlphaThresholdFilterImpl::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkAlphaThresholdFilter.cpp:136:39  
  
  #16 0x637f59 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:215:40  
  
  #17 0x63e3b4 in SkImageFilter::filterInput(int, SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:462:41  
  
  #18 0xfc59f8 in (anonymous namespace)::SkSpecularLightingImageFilter::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkLightingImageFilter.cpp:1415:39  
  
  #19 0x637f59 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:215:40  
  
  #20 0x63e3b4 in SkImageFilter::filterInput(int, SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:462:41  
  
  #21 0x100279d in SkOffsetImageFilter::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkOffsetImageFilter.cpp:32:39  
  
  #22 0x637f59 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:215:40  
  
  #23 0x63e3b4 in SkImageFilter::filterInput(int, SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:462:41  
  
  #24 0xf556d3 in SkAlphaThresholdFilterImpl::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkAlphaThresholdFilter.cpp:136:39  
  
  #25 0x637f59 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:215:40  
  
  #26 0x63e3b4 in SkImageFilter::filterInput(int, SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:462:41  
  
  #27 0xf556d3 in SkAlphaThresholdFilterImpl::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkAlphaThresholdFilter.cpp:136:39  
  
  #28 0x637f59 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:215:40  
  
  #29 0x63e3b4 in SkImageFilter::filterInput(int, SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:462:41  
  
  #30 0x100279d in SkOffsetImageFilter::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkOffsetImageFilter.cpp:32:39  
  
  #31 0x637f59 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:215:40  
  
  #32 0x63e3b4 in SkImageFilter::filterInput(int, SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:462:41  
  
  #33 0x102214b in SkTileImageFilter::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkTileImageFilter.cpp:46:39  
  
  #34 0x637f59 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:215:40  
  
  #35 0x63e3b4 in SkImageFilter::filterInput(int, SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:462:41  
  
  #36 0xfe3da7 in SkMagnifierImageFilter::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkMagnifierImageFilter.cpp:284:39  
  
  #37 0x637f59 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:215:40  
  
  #38 0xc6d922 in SkBitmapDevice::drawSpecial(SkDraw const&, SkSpecialImage\*, int, int, SkPaint const&) third\_party/skia/src/core/SkBitmapDevice.cpp:400:49  
  
  #39 0x597523 in SkCanvas::internalDrawDevice(SkBaseDevice\*, int, int, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:1426:25  
  
  #40 0x592387 in SkCanvas::internalRestore() third\_party/skia/src/core/SkCanvas.cpp:1316:19  
  
  #41 0x5b1ecb in ~AutoDrawLooper third\_party/skia/src/core/SkCanvas.cpp:515:22  
  
  #42 0x5b1ecb in SkCanvas::onDrawBitmap(SkBitmap const&, float, float, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:2445  
  
  #43 0x4f5eea in RunTestCase skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:46:13  
  
  #44 0x4f5eea in ReadAndRunTestCase skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:65  
  
  #45 0x4f5eea in main skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:84  
  
  #46 0x7f732211382f in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x2082f)

0x6030000003f0 is located 0 bytes to the right of 32-byte region [0x6030000003d0,0x6030000003f0)  

allocated by thread T0 here:  

#0 0x4c87fc in \_\_interceptor\_malloc (/home/sweetchip/asan-linux-release-437664/filter\_fuzz\_stub+0x4c87fc)  

#1 0x123591e in base::UncheckedMalloc(unsigned long, void\*\*) base/process/memory\_linux.cc:203:13  

#2 0x12357cf in base::UncheckedCalloc(unsigned long, unsigned long, void\*\*) base/process/memory.cc:45:8  

#3 0x552b51 in sk\_calloc(unsigned long) skia/ext/SkMemory\_new\_handler.cpp:102:19  

#4 0x650eb2 in NewUsing third\_party/skia/src/core/SkMallocPixelRef.cpp:82:18  

#5 0x650eb2 in SkMallocPixelRef::NewZeroed(SkImageInfo const&, unsigned long, SkColorTable\*) third\_party/skia/src/core/SkMallocPixelRef.cpp:100  

#6 0x7d8c04 in SkSpecialSurface::MakeRaster(SkImageInfo const&, SkSurfaceProps const\*) third\_party/skia/src/core/SkSpecialSurface.cpp:101:26  

#7 0x7d2cba in SkSpecialImage\_Raster::onMakeSurface(SkImageFilter::OutputProperties const&, SkTSize<int> const&, SkAlphaType) const third\_party/skia/src/core/SkSpecialImage.cpp:283:16  

#8 0x7cf9fe in SkSpecialImage::makeSurface(SkImageFilter::OutputProperties const&, SkTSize<int> const&, SkAlphaType) const third\_party/skia/src/core/SkSpecialImage.cpp:152:26  

#9 0x1007b45 in SkPaintImageFilter::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkPaintImageFilter.cpp:46:42  

#10 0x637f59 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:215:40  

#11 0x63e3b4 in SkImageFilter::filterInput(int, SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:462:41  

#12 0xf556d3 in SkAlphaThresholdFilterImpl::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkAlphaThresholdFilter.cpp:136:39  

#13 0x637f59 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:215:40  

#14 0x63e3b4 in SkImageFilter::filterInput(int, SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:462:41  

#15 0xf556d3 in SkAlphaThresholdFilterImpl::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkAlphaThresholdFilter.cpp:136:39  

#16 0x637f59 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:215:40  

#17 0x63e3b4 in SkImageFilter::filterInput(int, SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:462:41  

#18 0xf556d3 in SkAlphaThresholdFilterImpl::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkAlphaThresholdFilter.cpp:136:39  

#19 0x637f59 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:215:40  

#20 0x63e3b4 in SkImageFilter::filterInput(int, SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:462:41  

#21 0xf556d3 in SkAlphaThresholdFilterImpl::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkAlphaThresholdFilter.cpp:136:39  

#22 0x637f59 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:215:40  

#23 0x63e3b4 in SkImageFilter::filterInput(int, SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:462:41  

#24 0xf556d3 in SkAlphaThresholdFilterImpl::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkAlphaThresholdFilter.cpp:136:39  

#25 0x637f59 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:215:40  

#26 0x63e3b4 in SkImageFilter::filterInput(int, SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:462:41  

#27 0xf556d3 in SkAlphaThresholdFilterImpl::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkAlphaThresholdFilter.cpp:136:39  

#28 0x637f59 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:215:40  

#29 0x63e3b4 in SkImageFilter::filterInput(int, SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:462:41  

#30 0xfc59f8 in (anonymous namespace)::SkSpecularLightingImageFilter::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkLightingImageFilter.cpp:1415:39

# SUMMARY: AddressSanitizer: heap-buffer-overflow third\_party/skia/src/effects/SkAlphaThresholdFilter.cpp:233:33 in SkAlphaThresholdFilterImpl::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const Shadow bytes around the buggy address: 0x0c067fff8020: fd fd fd fd fa fa 00 00 00 00 fa fa 00 00 00 00 0x0c067fff8030: fa fa 00 00 00 00 fa fa 00 00 04 fa fa fa 00 00 0x0c067fff8040: 04 fa fa fa 00 00 05 fa fa fa 00 00 04 fa fa fa 0x0c067fff8050: 00 00 04 fa fa fa fd fd fd fd fa fa fd fd fd fd 0x0c067fff8060: fa fa fd fd fd fd fa fa fd fd fd fd fa fa fd fd =>0x0c067fff8070: fd fd fa fa 00 00 00 00 fa fa 00 00 00 00[fa]fa 0x0c067fff8080: 00 00 00 00 fa fa 00 00 00 00 fa fa fa fa fa fa 0x0c067fff8090: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa 0x0c067fff80a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa 0x0c067fff80b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa 0x0c067fff80c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa Shadow byte legend (one shadow byte represents 8 application bytes): Addressable: 00 Partially addressable: 01 02 03 04 05 06 07 Heap left redzone: fa Freed heap region: fd Stack left redzone: f1 Stack mid redzone: f2 Stack right redzone: f3 Stack after return: f5 Stack use after scope: f8 Global redzone: f9 Global init order: f6 Poisoned by user: f7 Container overflow: fc Array cookie: ac Intra object redzone: bb ASan internal: fe Left alloca redzone: ca Right alloca redzone: cb ==23992==ABORTING

**VERSION**  

Chrome Version: asan-linux-release-437664  

Operating System:

- Ubuntu 16.04.1 LTS 64bit (Server)
- Linux ubuntu 4.4.0-53-generic #74-Ubuntu SMP Fri Dec 2 15:59:10 UTC 2016 x86\_64 x86\_64 x86\_64 GNU/Linux

**REPRODUCTION CASE**

- ./filter\_fuzz\_stub ./poc1.fil

## Attachments

- [poc1.fil](attachments/poc1.fil) (application/octet-stream, 1.0 KB)

## Timeline

### cl...@chromium.org (2016-12-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5593734831144960

### mb...@chromium.org (2016-12-19)

Thanks for the report! I'm able to reproduce it.

robertphillips: Would you mind taking a look?

[Monorail components: Internals>Skia]

### [Deleted User] (2016-12-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-12-20)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5593734831144960

Job Type: linux_asan_filter_fuzz_stub
Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x60a000000d20
Crash State:
  SkAlphaThresholdFilterImpl::onFilterImage
  SkImageFilter::filterImage
  SkImageFilter::filterInput
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub&range=423391:423441

Minimized Testcase (1.02 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96fTKM5xWN55_4ruqMxbb78hqprt2-YaxU__-3NCcT2qhM__vNjkpZhijXBIHAFejfXixpY8QKj8lLHUDEwyPD6KDYsciJ-7zH6XXVOzg0Xeqq7RVJia7POx8W4x4mwEf_-bjAXE8_3x49Z611P2yZetywjiQ?testcase_id=5593734831144960

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### sh...@chromium.org (2016-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-12-20)

The following revision refers to this bug:
  https://skia.googlesource.com/skia.git/+/22c57abe439f200472a14b2341b68ed7c0ce785e

commit 22c57abe439f200472a14b2341b68ed7c0ce785e
Author: Robert Phillips <robertphillips@google.com>
Date: Mon Dec 19 21:51:53 2016

Fix mapping from src to dst image space in SkAlphaThresholdFilter

This CL does 3 things:
   It updates the imagealphathreshold GMs so they would've caught this bug
   It updates SkAlphaImageThresholdFilter to fix the bug
   It updates the imagealphathreshold_surface GM to match the imagealphathreshold_crop GM (which it was, presumably, originally written to do)

The bug in question is that the prior mapping from src to dst space was correct as long as the imageOffset was (0, 0).

BUG=675332

Change-Id: I3aa1f463a2234576fb2277797caa2fc4aba2650d
Reviewed-on: https://skia-review.googlesource.com/6291
Reviewed-by: Brian Osman <brianosman@google.com>
Reviewed-by: Stephan White <senorblanco@chromium.org>
Commit-Queue: Robert Phillips <robertphillips@google.com>

[modify] https://crrev.com/22c57abe439f200472a14b2341b68ed7c0ce785e/gm/imagealphathreshold.cpp
[modify] https://crrev.com/22c57abe439f200472a14b2341b68ed7c0ce785e/src/effects/SkAlphaThresholdFilter.cpp


### bu...@chromium.org (2016-12-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/911fd06007472f0c79e31ba8947d8edf4661daa8

commit 911fd06007472f0c79e31ba8947d8edf4661daa8
Author: skia-deps-roller <skia-deps-roller@chromium.org>
Date: Tue Dec 20 23:38:42 2016

Roll src/third_party/skia/ 86cedfc31..6ad3d2fa3 (11 commits).

https://skia.googlesource.com/skia.git/+log/86cedfc31588..6ad3d2fa3858

$ git log 86cedfc31..6ad3d2fa3 --date=short --no-merges --format='%ad %ae %s'
2016-12-20 halcanary xps.gni
2016-12-20 bsalomon Rename batch->op in GrAuditTrail.
2016-12-20 brianosman Add color space xform to GrMagnifierEffect
2016-12-20 bsalomon Rename files, macros, types, and functions related to GrDrawOp testing.
2016-12-20 bsalomon Remove the last "batch tracker" from AAStrokeRectOp.
2016-12-20 brianosman Add color space xform support to GrDisplacementEffect
2016-12-20 brianosman Add color space xform bits to key for texture domain effect
2016-12-20 robertphillips Fix more Skia filter fuzzer bugs
2016-12-20 caryclark check for empty contours in sortable top
2016-12-20 bsalomon GPU: Fix for fuzzer issue for sw-rendered paths with large bounds.
2016-12-19 robertphillips Fix mapping from src to dst image space in SkAlphaThresholdFilter

BUG=675132,675315,675332

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, see:
http://www.chromium.org/developers/tree-sheriffs/sheriff-details-chromium#TOC-Failures-due-to-DEPS-rolls

CQ_INCLUDE_TRYBOTS=master.tryserver.blink:linux_trusty_blink_rel
TBR=rmistry@google.com

Review-Url: https://codereview.chromium.org/2590913005
Cr-Commit-Position: refs/heads/master@{#439928}

[modify] https://crrev.com/911fd06007472f0c79e31ba8947d8edf4661daa8/DEPS


### cl...@chromium.org (2016-12-22)

ClusterFuzz has detected this issue as fixed in range 439820:440032.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5593734831144960

Job Type: linux_asan_filter_fuzz_stub
Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x60a000000d20
Crash State:
  SkAlphaThresholdFilterImpl::onFilterImage
  SkImageFilter::filterImage
  SkImageFilter::filterInput
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub&range=423391:423441
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub&range=439820:440032

Minimized Testcase (1.02 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96fTKM5xWN55_4ruqMxbb78hqprt2-YaxU__-3NCcT2qhM__vNjkpZhijXBIHAFejfXixpY8QKj8lLHUDEwyPD6KDYsciJ-7zH6XXVOzg0Xeqq7RVJia7POx8W4x4mwEf_-bjAXE8_3x49Z611P2yZetywjiQ?testcase_id=5593734831144960

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2016-12-22)

ClusterFuzz testcase 5593734831144960 is verified as fixed, so closing issue.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2016-12-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-03)

[Empty comment from Monorail migration]

### di...@chromium.org (2017-01-03)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### bu...@google.com (2017-01-03)

Approved for merge into M56 if we can do a cherrypick of the change in #6 https://crrev.com/22c57abe439f200472a14b2341b68ed7c0ce785e

### sh...@chromium.org (2017-01-09)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-01-09)

[Empty comment from Monorail migration]

### aw...@google.com (2017-01-10)

Congratulations! The panel decided to reward $2,000 for this report - thank you!

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-01-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-01-11)

The following revision refers to this bug:
  https://skia.googlesource.com/skia.git/+/9574d668827340e0ff69b5669c3337032d100d61

commit 9574d668827340e0ff69b5669c3337032d100d61
Author: Robert Phillips <robertphillips@google.com>
Date: Wed Jan 11 15:30:08 2017

M56 cherrypick Fix mapping from src to in SkAlphaThresholdFilter

This cherrypicks https://skia-review.googlesource.com/c/6291/ (Fix mapping from src to dst image space in SkAlphaThresholdFilter) to M56

BUG=675332

GOLD_TRYBOT_URL= https://gold.skia.org/search?issue=6880
NOTREECHECKS=true
NOTRY=true
NOPRESUBMIT=true

Change-Id: Id225b462eb91e3d766804392c6986415ad531808
Reviewed-on: https://skia-review.googlesource.com/6880
Reviewed-by: Robert Phillips <robertphillips@google.com>
Commit-Queue: Robert Phillips <robertphillips@google.com>

[modify] https://crrev.com/9574d668827340e0ff69b5669c3337032d100d61/gm/imagealphathreshold.cpp
[modify] https://crrev.com/9574d668827340e0ff69b5669c3337032d100d61/src/effects/SkAlphaThresholdFilter.cpp


### [Deleted User] (2017-01-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/675332?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086256)*
