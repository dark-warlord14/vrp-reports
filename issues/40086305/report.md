# heap-buffer-overflow in SkPathRef::Iter::next

| Field | Value |
|-------|-------|
| **Issue ID** | [40086305](https://issues.chromium.org/issues/40086305) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia>Compositing |
| **Platforms** | Linux |
| **Reporter** | sw...@gmail.com |
| **Assignee** | re...@google.com |
| **Created** | 2016-12-23 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

Please check the ASAN output.

# ./filter\_fuzz\_stub crash\_7203851323793818.fil [1223/044019.557471:INFO:filter\_fuzz\_stub.cc(59)] Test case: crash\_7203851323793818.fil [1223/044019.559421:INFO:filter\_fuzz\_stub.cc(36)] Valid stream detected.

==123629==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x612000000038 at pc 0x00000071feed bp 0x7ffc14325db0 sp 0x7ffc14325da8  

READ of size 8 at 0x612000000038 thread T0  

#0 0x71feec in SkPathRef::Iter::next(SkPoint\*) third\_party/skia/src/core/SkPathRef.cpp:644:20  

#1 0x7000c1 in next third\_party/skia/include/core/SkPath.h:1046:36  

#2 0x7000c1 in SkPath::addPath(SkPath const&, SkMatrix const&, SkPath::AddPathMode) third\_party/skia/src/core/SkPath.cpp:1514  

#3 0x6ffd30 in SkPath::addPath(SkPath const&, float, float, SkPath::AddPathMode) third\_party/skia/src/core/SkPath.cpp:1502:11  

#4 0xf76f9d in SkPath1DPathEffect::next(SkPath\*, float, SkPathMeasure&) const third\_party/skia/src/effects/Sk1DPathEffect.cpp:175:22  

#5 0xf75d65 in filterPath third\_party/skia/src/effects/Sk1DPathEffect.cpp:22:36  

#6 0xf75d65 in SkPath1DPathEffect::filterPath(SkPath\*, SkPath const&, SkStrokeRec\*, SkRect const\*) const third\_party/skia/src/effects/Sk1DPathEffect.cpp:70  

#7 0x6ea76a in SkPaint::getFillPath(SkPath const&, SkPath\*, SkRect const\*, float) const third\_party/skia/src/core/SkPaint.cpp:1972:37  

#8 0x61c5f2 in SkDraw::drawPath(SkPath const&, SkPaint const&, SkMatrix const\*, bool, bool, SkBlitter\*) const third\_party/skia/src/core/SkDraw.cpp:1167:25  

#9 0x61902c in drawPath third\_party/skia/include/core/SkDraw.h:54:15  

#10 0x61902c in SkDraw::drawRect(SkRect const&, SkPaint const&, SkMatrix const\*, SkRect const\*) const third\_party/skia/src/core/SkDraw.cpp:824  

#11 0x5a915f in SkCanvas::onDrawRect(SkRect const&, SkPaint const&) third\_party/skia/src/core/SkCanvas.cpp:2153:27  

#12 0x102edbd in SkPaintImageFilter::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkPaintImageFilter.cpp:64:13  

#13 0x63abb9 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:215:40  

#14 0xc999d2 in SkBitmapDevice::drawSpecial(SkDraw const&, SkSpecialImage\*, int, int, SkPaint const&) third\_party/skia/src/core/SkBitmapDevice.cpp:400:49  

#15 0x599d27 in SkCanvas::internalDrawDevice(SkBaseDevice\*, int, int, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:1428:25  

#16 0x594bd7 in SkCanvas::internalRestore() third\_party/skia/src/core/SkCanvas.cpp:1318:19  

#17 0x59d020 in AutoDrawLooper::~AutoDrawLooper() third\_party/skia/src/core/SkCanvas.cpp:516:22  

#18 0x5b3824 in SkCanvas::onDrawBitmap(SkBitmap const&, float, float, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:2460:1  

#19 0x4f69cd in RunTestCase skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:46:13  

#20 0x4f69cd in ReadAndRunTestCase skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:65  

#21 0x4f69cd in main skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:84  

#22 0x7ff66484982f in \_\_libc\_start\_main /build/glibc-t3gR2i/glibc-2.23/csu/../csu/libc-start.c:291

0x612000000038 is located 8 bytes to the left of 312-byte region [0x612000000040,0x612000000178)  

allocated by thread T0 here:  

#0 0x4c900e in \_\_interceptor\_realloc (/home/sweetchip/poc\_test/asan-linux-release-440420/filter\_fuzz\_stub+0x4c900e)  

#1 0x555871 in sk\_realloc\_throw(void\*, unsigned long) skia/ext/SkMemory\_new\_handler.cpp:43:35  

#2 0x71a53f in makeSpace third\_party/skia/include/core/SkPathRef.h:453:46  

#3 0x71a53f in SkPathRef::resetToSize(int, int, int, int, int) third\_party/skia/include/core/SkPathRef.h:402  

#4 0x71addc in SkPathRef::CreateFromBuffer(SkRBuffer\*) third\_party/skia/src/core/SkPathRef.cpp:222:10  

#5 0x708a02 in SkPath::readFromMemory(void const\*, unsigned long) third\_party/skia/src/core/SkPath.cpp:2073:26  

#6 0x7f82ea in SkValidatingReadBuffer::readPath(SkPath\*) third\_party/skia/src/core/SkValidatingReadBuffer.cpp:178:22  

#7 0xf7607d in SkPath1DPathEffect::CreateProc(SkReadBuffer&) third\_party/skia/src/effects/Sk1DPathEffect.cpp:152:16  

#8 0x7f9f18 in SkValidatingReadBuffer::readFlattenable(SkFlattenable::Type) third\_party/skia/src/core/SkValidatingReadBuffer.cpp:289:11  

#9 0x6e8a72 in readFlattenable<SkPathEffect> third\_party/skia/src/core/SkReadBuffer.h:143:35  

#10 0x6e8a72 in readPathEffect third\_party/skia/src/core/SkReadBuffer.h:149  

#11 0x6e8a72 in SkPaint::unflatten(SkReadBuffer&) third\_party/skia/src/core/SkPaint.cpp:1931  

#12 0x102e2fe in SkPaintImageFilter::CreateProc(SkReadBuffer&) third\_party/skia/src/effects/SkPaintImageFilter.cpp:28:12  

#13 0x7f9f18 in SkValidatingReadBuffer::readFlattenable(SkFlattenable::Type) third\_party/skia/src/core/SkValidatingReadBuffer.cpp:289:11  

#14 0x6334cc in SkValidatingDeserializeFlattenable third\_party/skia/src/core/SkFlattenableSerialization.cpp:26:19  

#15 0x6334cc in SkValidatingDeserializeImageFilter(void const\*, unsigned long) third\_party/skia/src/core/SkFlattenableSerialization.cpp:30  

#16 0x4f673a in RunTestCase skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:31:38  

#17 0x4f673a in ReadAndRunTestCase skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:65  

#18 0x4f673a in main skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:84  

#19 0x7ff66484982f in \_\_libc\_start\_main /build/glibc-t3gR2i/glibc-2.23/csu/../csu/libc-start.c:291

SUMMARY: AddressSanitizer: heap-buffer-overflow third\_party/skia/src/core/SkPathRef.cpp:644:20 in SkPathRef::Iter::next(SkPoint\*)  

Shadow bytes around the buggy address:  

0x0c247fff7fb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c247fff7fc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c247fff7fd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c247fff7fe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c247fff7ff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x0c247fff8000: fa fa fa fa fa fa fa[fa]00 00 00 00 00 00 00 00  

0x0c247fff8010: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c247fff8020: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 fa  

0x0c247fff8030: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x0c247fff8040: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c247fff8050: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 fa  

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

==123629==ABORTING

**VERSION**  

Chrome Version: asan-linux-release-440420  

Operating System:

- Ubuntu 16.04.1 LTS 64bit (Server)
- Linux ubuntu 4.4.0-53-generic #74-Ubuntu SMP Fri Dec 2 15:59:10 UTC 2016 x86\_64 x86\_64 x86\_64 GNU/Linux

**REPRODUCTION CASE**

- ./filter\_fuzz\_stub ./crash\_7203851323793818.fil

## Attachments

- [crash_7203851323793818.fil](attachments/crash_7203851323793818.fil) (application/octet-stream, 900 B)

## Timeline

### pe...@chromium.org (2016-12-25)

Hello Heather,

Could you please help triage this security bug?

SkPathRef.cpp hasn't changed in some time, and there are no obvious (recent) culprits in the top of the stack.  There is a repro attached though, so someone on Skia should be able to narrow down what's going wrong in SkDraw/Paint/Path.

https://cs.chromium.org/chromium/src/third_party/skia/src/core/SkPathRef.cpp?q=SkPathRef&sq=package:chromium&l=644

Thanks!

[Monorail components: Internals>Skia>Compositing]

### sh...@chromium.org (2016-12-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-25)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-12-26)

[Empty comment from Monorail migration]

### hc...@chromium.org (2016-12-28)

Let's start with Robert and/or Mike- seems like something invalid is getting through the filter + path effect?

### re...@google.com (2017-01-03)

Is SkPath1DPathEffect accessible in any way from Chrome/Blink? I don't see that it is.

### re...@google.com (2017-01-03)

[Empty comment from Monorail migration]

### re...@google.com (2017-01-03)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-01-03)

The following revision refers to this bug:
  https://skia.googlesource.com/skia.git/+/e3374d68932ce5bd1e6a50b05a6764a543c00c39

commit e3374d68932ce5bd1e6a50b05a6764a543c00c39
Author: Mike Reed <reed@google.com>
Date: Tue Jan 03 18:58:21 2017

validate deserialized path verbs

BUG=676755

Change-Id: Ie9bd70d3a130c53737756587f73c9dce4a6bcb6d
Reviewed-on: https://skia-review.googlesource.com/6529
Commit-Queue: Mike Reed <reed@google.com>
Reviewed-by: Cary Clark <caryclark@google.com>

[modify] https://crrev.com/e3374d68932ce5bd1e6a50b05a6764a543c00c39/src/core/SkPathRef.cpp
[modify] https://crrev.com/e3374d68932ce5bd1e6a50b05a6764a543c00c39/tests/PathTest.cpp


### bu...@chromium.org (2017-01-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/880996d1006558c9bf2cc1399bbee3e51db5a205

commit 880996d1006558c9bf2cc1399bbee3e51db5a205
Author: skia-deps-roller <skia-deps-roller@chromium.org>
Date: Wed Jan 04 02:54:31 2017

Roll src/third_party/skia/ 7551898f8..9ea894b4d (13 commits).

https://skia.googlesource.com/skia.git/+log/7551898f8eba..9ea894b4d030

$ git log 7551898f8..9ea894b4d --date=short --no-merges --format='%ad %ae %s'
2017-01-03 mtklein Revert "trim another instruction off SkRasterPipeline overhead"
2017-01-03 bungeman Specify "/utf-8" with Visual C++.
2017-01-03 senorblanco Quality and performance fixes for AA tessellating path renderer.
2017-01-03 senorblanco Revert "Quality and performance fixes for AA tessellating path renderer."
2017-01-03 senorblanco Quality and performance fixes for AA tessellating path renderer.
2017-01-03 ethannicholas fixed a divide-by-zero bug in skslc
2017-01-03 ethannicholas switched GrVkPipelineStateCache over to use SkLRUCache
2017-01-03 herb Fix: when pos is not finite, text pointer not advanced.
2017-01-03 reed validate deserialized path verbs
2016-12-22 scroggo GIF: Better check for frame dependency
2017-01-03 ethannicholas Force classic locale when parsing floats in skslc.
2016-12-29 ethannicholas fix for Vulkan SPIR-V crash on some systems
2016-12-29 mtklein trim another instruction off SkRasterPipeline overhead

BUG=660893,660893,676755

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, see:
http://www.chromium.org/developers/tree-sheriffs/sheriff-details-chromium#TOC-Failures-due-to-DEPS-rolls

CQ_INCLUDE_TRYBOTS=master.tryserver.blink:linux_trusty_blink_rel
TBR=csmartdalton@google.com

Review-Url: https://codereview.chromium.org/2602323004
Cr-Commit-Position: refs/heads/master@{#441303}

[modify] https://crrev.com/880996d1006558c9bf2cc1399bbee3e51db5a205/DEPS


### aw...@chromium.org (2017-01-17)

Marking as fixed - please re-open if that's not correct.

### sh...@chromium.org (2017-01-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-25)

Hi reed@, re https://crbug.com/chromium/676755#c6: we'd been assuming that bugs that can be reached through filter_fuzz_stub can also be reached from Chrome - is there any reason to believe that's not the case?

### aw...@chromium.org (2017-01-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-27)

Congratulations! The panel decided to award $5,000 for this report!  A member of our finance team will be in touch shortly.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************


### aw...@chromium.org (2017-01-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### is...@google.com (2018-01-22)

This issue was migrated from crbug.com/chromium/676755?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086305)*
