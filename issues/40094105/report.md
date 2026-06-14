# Use-of-uninitialized-value in avx::store_NUMBER

| Field | Value |
|-------|-------|
| **Issue ID** | [40094105](https://issues.chromium.org/issues/40094105) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | mt...@google.com |
| **Created** | 2019-02-21 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=5968280726667264

Fuzzer: jesse_avalanche
Job Type: linux_msan_chrome
Platform Id: linux

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  avx::store_NUMBER
  avx::start_pipeline
  SkMaskFilterBase::filterPath
  
Sanitizer: memory (MSAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_msan_chrome&range=541609:541620

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5968280726667264

Issue filed automatically.

See https://www.chromium.org/developers/testing/memorysanitizer#TOC-Reproducing-ClusterFuzz-Bugs for instructions to reproduce this bug locally.

## Timeline

### sh...@chromium.org (2019-02-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-21)

[Empty comment from Monorail migration]

### va...@chromium.org (2019-02-22)

[Empty comment from Monorail migration]

[Monorail components: Internals>Skia]

### sh...@chromium.org (2019-03-07)

hcm: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-03-22)

hcm: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### hc...@chromium.org (2019-04-12)

This appeared to be introduced in a set of changes to our raster pipeline/avx code, though looks to be a memory issue coming from upstack. To Mike for a look...

### mt...@google.com (2019-04-12)

Yeah, this makes sense to have been "regressed" by "make SkJumper stages normal Skia code", which  converted this part of the code base from assembly to C++, allowing MSAN to instrument it for the first time.

Usually when we see this sort of use-of-uninitialized diagnosis crop up in any of these store_ stages, it's because MSAN considers conversion from float to int as an interesting use of the data, but it's kind of... not.  It's really hard to say exactly how uninitialized data got into the pipeline; could be as simple as someone blending over an uninitialized buffer.

I'll have a looksee if I can reproduce this and figure out what's uninitialized, but don't get your hopes up.

### mt...@google.com (2019-04-12)

I think I can repro locally:

  Uninitialized value was created by a heap allocation
    #0 0x55e251fc84fd in __interceptor_malloc /b/swarming/w/ir/k/src/third_party/llvm/compiler-rt/lib/msan/msan_interceptors.cc:911:3
    #1 0x55e25e463dc6 in base::UncheckedMalloc(unsigned long, void**) ./../../base/process/memory_linux.cc:133:13
    #2 0x55e25f25deb7 in malloc_nothrow ./../../skia/ext/SkMemory_new_handler.cpp:84:19
    #3 0x55e25f25deb7 in sk_malloc_flags(unsigned long, unsigned int) ./../../skia/ext/SkMemory_new_handler.cpp:123:0
    #4 0x55e252295de0 in sk_malloc_canfail ./../../third_party/skia/include/private/SkMalloc.h:93:12
    #5 0x55e252295de0 in MakeUsing ./../../third_party/skia/src/core/SkMallocPixelRef.cpp:76:0
    #6 0x55e252295de0 in SkMallocPixelRef::MakeAllocate(SkImageInfo const&, unsigned long) ./../../third_party/skia/src/core/SkMallocPixelRef.cpp:86:0
    #7 0x55e25208b717 in SkBitmap::HeapAllocator::allocPixelRef(SkBitmap*) ./../../third_party/skia/src/core/SkBitmap.cpp:376:28
    #8 0x55e25208775f in tryAllocPixels ./../../third_party/skia/src/core/SkBitmap.cpp:219:23
    #9 0x55e25208775f in allocPixels ./../../third_party/skia/src/core/SkBitmap.cpp:239:0
    #10 0x55e25208775f in SkBitmap::allocPixels() ./../../third_party/skia/src/core/SkBitmap.cpp:235:0
    #11 0x55e252612ab5 in SkSurface_Raster::onCopyOnWrite(SkSurface::ContentChangeMode) ./../../third_party/skia/src/image/SkSurface_Raster.cpp:145:21
    #12 0x55e25260d3c8 in SkSurface_Base::aboutToDraw(SkSurface::ContentChangeMode) ./../../third_party/skia/src/image/SkSurface.cpp:104:19
    #13 0x55e252142686 in predrawNotify ./../../third_party/skia/src/core/SkCanvas.cpp:169:23
    #14 0x55e252142686 in predrawNotify ./../../third_party/skia/include/core/SkCanvas.h:2552:0
    #15 0x55e252142686 in SkCanvas::onDrawRect(SkRect const&, SkPaint const&) ./../../third_party/skia/src/core/SkCanvas.cpp:2097:0
    #16 0x55e25212454f in SkCanvas::drawRect(SkRect const&, SkPaint const&) ./../../third_party/skia/src/core/SkCanvas.cpp:1710:11
    #17 0x55e26294e105 in RasterWithFlags ./../../cc/paint/paint_op_buffer.cc:1357:11
    #18 0x55e26294e105 in RasterWithFlags ./../../cc/paint/paint_op_buffer.cc:125:0
    #19 0x55e26294e105 in operator() ./../../cc/paint/paint_op_buffer.cc:160:0
    #20 0x55e26294e105 in cc::$_43::__invoke(cc::PaintOp const*, cc::PaintFlags const*, SkCanvas*, cc::PlaybackParams const&) ./../../cc/paint/paint_op_buffer.cc:160:0
    #21 0x55e262945e5a in RasterWithFlags ./../../cc/paint/paint_op_buffer.cc:2078:3
    #22 0x55e262945e5a in cc::PaintOpBuffer::Playback(SkCanvas*, cc::PlaybackParams const&, std::__1::vector<unsigned long, std::__1::allocator<unsigned long> > const*) const ./../../cc/paint/paint_op_buffer.cc:2435:0
    #23 0x55e2629dcf97 in cc::SkiaPaintCanvas::drawPicture(sk_sp<cc::PaintOpBuffer const>, base::RepeatingCallback<void (SkCanvas*, unsigned int)>) ./../../cc/paint/skia_paint_canvas.cc:352:11
    #24 0x55e2629dca1b in cc::SkiaPaintCanvas::drawPicture(sk_sp<cc::PaintOpBuffer const>) ./../../cc/paint/skia_paint_canvas.cc:309:3
    #25 0x55e26b27710d in blink::Canvas2DLayerBridge::FlushRecording() ./../../third_party/blink/renderer/platform/graphics/canvas_2d_layer_bridge.cc:491:13
    #26 0x55e26b28098f in blink::Canvas2DLayerBridge::NewImageSnapshot(blink::AccelerationHint) ./../../third_party/blink/renderer/platform/graphics/canvas_2d_layer_bridge.cc:672:3
    #27 0x55e26b24eca8 in blink::HTMLCanvasElement::Paint(blink::GraphicsContext&, blink::LayoutRect const&) ./../../third_party/blink/renderer/core/html/canvas/html_canvas_element.cc:752:35
    #28 0x55e26d6180c9 in blink::HTMLCanvasPainter::PaintReplaced(blink::PaintInfo const&, blink::LayoutPoint const&) ./../../third_party/blink/renderer/core/paint/html_canvas_painter.cc:62:11
    #29 0x55e26c80ba73 in blink::LayoutHTMLCanvas::PaintReplaced(blink::PaintInfo const&, blink::LayoutPoint const&) const ./../../third_party/blink/renderer/core/layout/layout_html_canvas.cc:48:28
    #30 0x55e26d88423c in blink::ReplacedPainter::Paint(blink::PaintInfo const&) ./../../third_party/blink/renderer/core/paint/replaced_painter.cc:158:22


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-15)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/930c29511f036196f8877c56858177559bb34a9f

commit 930c29511f036196f8877c56858177559bb34a9f
Author: Mike Klein <mtklein@google.com>
Date: Mon Apr 15 15:50:58 2019

always zero SkMallocPixelRefs

I'm getting tired of trying to figure out where
clients screw up and forget to clear these buffers,
and I'd like a safer safety net for our own screw ups.

Bug: chromium:934161, many more
Change-Id: I6ada4c821da6dd173e54c6402c17d6946ff05fdf
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/207857
Reviewed-by: Mike Reed <reed@google.com>
Commit-Queue: Mike Klein <mtklein@google.com>

[modify] https://crrev.com/930c29511f036196f8877c56858177559bb34a9f/src/core/SkMallocPixelRef.cpp
[modify] https://crrev.com/930c29511f036196f8877c56858177559bb34a9f/src/core/SkBitmap.cpp
[modify] https://crrev.com/930c29511f036196f8877c56858177559bb34a9f/include/core/SkBitmap.h
[modify] https://crrev.com/930c29511f036196f8877c56858177559bb34a9f/include/core/SkMallocPixelRef.h
[modify] https://crrev.com/930c29511f036196f8877c56858177559bb34a9f/src/image/SkSurface_Raster.cpp
[modify] https://crrev.com/930c29511f036196f8877c56858177559bb34a9f/src/core/SkSpecialSurface.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/093bd2a62e3a2714a83bfeecc7f037cd291cbcb6

commit 093bd2a62e3a2714a83bfeecc7f037cd291cbcb6
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Apr 15 18:34:57 2019

Roll src/third_party/skia be2062c4305f..930c29511f03 (3 commits)

https://skia.googlesource.com/skia.git/+log/be2062c4305f..930c29511f03


git log be2062c4305f..930c29511f03 --date=short --no-merges --format='%ad %ae %s'
2019-04-15 mtklein@google.com always zero SkMallocPixelRefs
2019-04-15 benjaminwagner@google.com Add LenovoYogaC630 (Win arm64 bot)
2019-04-15 reed@google.com removed localmatrix getter


Created with:
  gclient setdep -r src/third_party/skia@930c29511f03

The AutoRoll server is located here: https://autoroll.skia.org/r/skia-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.

CQ_INCLUDE_TRYBOTS=luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux-blink-rel;luci.chromium.try:linux-chromeos-compile-dbg;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel

BUG=chromium:934161,chromium:many more
TBR=herb@chromium.org

Change-Id: I6c4e2fe0d3c5a7fb40ea356419f0b326b42656a9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1567827
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#650883}
[modify] https://crrev.com/093bd2a62e3a2714a83bfeecc7f037cd291cbcb6/DEPS


### cl...@chromium.org (2019-04-16)

ClusterFuzz has detected this issue as fixed in range 650882:650884.

Detailed report: https://clusterfuzz.com/testcase?key=5968280726667264

Fuzzer: jesse_avalanche
Job Type: linux_msan_chrome
Platform Id: linux

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  avx::store_NUMBER
  avx::start_pipeline
  SkMaskFilterBase::filterPath
  
Sanitizer: memory (MSAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_msan_chrome&range=541609:541620
Fixed: https://clusterfuzz.com/revisions?job=linux_msan_chrome&range=650882:650884

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5968280726667264

See https://www.chromium.org/developers/testing/memorysanitizer#TOC-Reproducing-ClusterFuzz-Bugs for instructions to reproduce this bug locally.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2019-04-16)

ClusterFuzz testcase 5968280726667264 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2019-04-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-17)

Requesting merge to M74 even though there is no obvious trunk commit here. Perhaps it was fixed in another ticket; please investigate.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-04-17)

This bug requires manual review: We are only 5 days from stable.
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), dgagnon@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2019-04-17)

+adetaylor

Rejecting merge since it's a medium severity bug, and we're only a few days away from M74 stable. Re-request if you disagree. 

### mt...@google.com (2019-04-17)

I'd also suggest not merging this fix, because it's very much on the wide-ranging hammer end of the scale rather than a precision fix.  While I don't anticipate any correctness issue or risk from it, it does affect quite a lot of how Skia works, and could end up being something we want to revert if there turns out to be too much performance impact.

### ad...@chromium.org (2019-04-17)

Fine with me FWIW. Also, I need to look into why Sheriffbot didn't spot the trunk commit.

### aw...@google.com (2019-04-17)

[Empty comment from Monorail migration]

### na...@google.com (2019-05-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### mt...@google.com (2019-05-01)

Hey, in case I wasn't clear in https://crbug.com/chromium/934161#c7, this is a situation where MSAN is being over-sensitive.  I don't believe this diagnosis of use-of-uninitialized value is useful, or that the binary before or after the "fix" was doing anything interesting with that uninitialized value in the "use".

### pa...@chromium.org (2019-05-01)

Congrats! The Panel awarded $1,500 for this report :) 

### aw...@google.com (2019-05-01)

[Empty comment from Monorail migration]

### aw...@google.com (2019-06-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/934161?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094105)*
