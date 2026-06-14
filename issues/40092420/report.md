# Security: Skia heap use-after-freed in SkPath::addPath

| Field | Value |
|-------|-------|
| **Issue ID** | [40092420](https://issues.chromium.org/issues/40092420) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2018-09-10 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

There is a heap use-after-free in Skia at SkPath::addPath()  

<https://cs.chromium.org/chromium/src/third_party/skia/src/core/SkPath.cpp?dr&q=addpath&g=0&l=1614>

Root cause:  

"RawIter iter(path);" variable at line  

<https://cs.chromium.org/chromium/src/third_party/skia/src/core/SkPath.cpp?dr&q=addpath&g=0&l=1583>  

has pointer to the element "fConicWeights" of "path".  

If "path" is the same object with current SkPath, it could call "conicTo" function, trigger  

"SkPathRef::Editor::growForVerb" function and realloc "fConicWeights" buffer. But after realloc  

pointer of "fConicWeights" in "iter" have not been updated. That lead to heap use-after-free.

This pattern may exist in some others place.

**REPRODUCTION CASE**

# Build Skia program with ASAN

#include "SkCanvas.h"  

#include "SkPath.h"

int main (int argc, char \* const argv[]) {

SkRect rect = SkRect::MakeEmpty();  

SkPath path;  

path.addOval(rect, SkPath::kCCW\_Direction);

path.addPath(path, 0.707106781f, 0.414213562f);

return 0;  

}

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

=================================================================  

==6152==ERROR: AddressSanitizer: heap-use-after-free on address 0x60300000013c at pc 0x00000065311b bp 0x7fff02b7d530 sp 0x7fff02b7d528  

READ of size 4 at 0x60300000013c thread T0  

#0 0x65311a in SkPathRef::Iter::conicWeight() const /home/monkie/skia-latest/out/asan/../../include/private/SkPathRef.h:138:47  

#1 0x65311a in SkPath::RawIter::conicWeight() const /home/monkie/skia-latest/out/asan/../../include/core/SkPath.h:1558  

#2 0x65311a in SkPath::addPath(SkPath const&, SkMatrix const&, SkPath::AddPathMode) /home/monkie/skia-latest/out/asan/../../src/core/SkPath.cpp:1614  

#3 0x652069 in SkPath::addPath(SkPath const&, float, float, SkPath::AddPathMode) /home/monkie/skia-latest/out/asan/../../src/core/SkPath.cpp:1577:18  

#4 0x63fced in main /home/monkie/skia-latest/out/asan/../../tools/test.cpp:14:11  

#5 0x7f97e7f6082f in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x2082f)  

#6 0x54bd78 in \_start (/home/monkie/skia-latest/out/asan/test+0x54bd78)

0x60300000013c is located 12 bytes inside of 24-byte region [0x603000000130,0x603000000148)  

freed by thread T0 here:  

#0 0x60ef60 in realloc /tmp/tmpFq\_AZD/llvm/out/../projects/compiler-rt/lib/asan/asan\_malloc\_linux.cc:107  

#1 0x680c2d in sk\_realloc\_throw(void\*, unsigned long) /home/monkie/skia-latest/out/asan/../../src/ports/SkMemory\_malloc.cpp:55:35  

#2 0x66c99e in SkTDArray<float>::resizeStorageToAtLeast(int) /home/monkie/skia-latest/out/asan/../../include/private/SkTDArray.h:383:22  

#3 0x66c99e in SkTDArray<float>::setCount(int) /home/monkie/skia-latest/out/asan/../../include/private/SkTDArray.h:149  

#4 0x66c99e in SkTDArray<float>::adjustCount(int) /home/monkie/skia-latest/out/asan/../../include/private/SkTDArray.h:362  

#5 0x66a5ed in SkTDArray<float>::append(int, float const\*) /home/monkie/skia-latest/out/asan/../../include/private/SkTDArray.h:180:19  

#6 0x66a5ed in SkTDArray<float>::append() /home/monkie/skia-latest/out/asan/../../include/private/SkTDArray.h:172  

#7 0x66a5ed in SkPathRef::growForVerb(int, float) /home/monkie/skia-latest/out/asan/../../src/core/SkPathRef.cpp:649  

#8 0x64829b in SkPathRef::Editor::growForVerb(int, float) /home/monkie/skia-latest/out/asan/../../include/private/SkPathRef.h:76:30  

#9 0x64829b in SkPath::conicTo(float, float, float, float, float) /home/monkie/skia-latest/out/asan/../../src/core/SkPath.cpp:841  

#10 0x65294d in SkPath::conicTo(SkPoint const&, SkPoint const&, float) /home/monkie/skia-latest/out/asan/../../include/core/SkPath.h:716:22  

#11 0x65294d in SkPath::addPath(SkPath const&, SkMatrix const&, SkPath::AddPathMode) /home/monkie/skia-latest/out/asan/../../src/core/SkPath.cpp:1614  

#12 0x652069 in SkPath::addPath(SkPath const&, float, float, SkPath::AddPathMode) /home/monkie/skia-latest/out/asan/../../src/core/SkPath.cpp:1577:18  

#13 0x63fced in main /home/monkie/skia-latest/out/asan/../../tools/test.cpp:14:11  

#14 0x7f97e7f6082f in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x2082f)

previously allocated by thread T0 here:  

#0 0x60ef60 in realloc /tmp/tmpFq\_AZD/llvm/out/../projects/compiler-rt/lib/asan/asan\_malloc\_linux.cc:107  

#1 0x680c2d in sk\_realloc\_throw(void\*, unsigned long) /home/monkie/skia-latest/out/asan/../../src/ports/SkMemory\_malloc.cpp:55:35  

#2 0x66c99e in SkTDArray<float>::resizeStorageToAtLeast(int) /home/monkie/skia-latest/out/asan/../../include/private/SkTDArray.h:383:22  

#3 0x66c99e in SkTDArray<float>::setCount(int) /home/monkie/skia-latest/out/asan/../../include/private/SkTDArray.h:149  

#4 0x66c99e in SkTDArray<float>::adjustCount(int) /home/monkie/skia-latest/out/asan/../../include/private/SkTDArray.h:362  

#5 0x66a5ed in SkTDArray<float>::append(int, float const\*) /home/monkie/skia-latest/out/asan/../../include/private/SkTDArray.h:180:19  

#6 0x66a5ed in SkTDArray<float>::append() /home/monkie/skia-latest/out/asan/../../include/private/SkTDArray.h:172  

#7 0x66a5ed in SkPathRef::growForVerb(int, float) /home/monkie/skia-latest/out/asan/../../src/core/SkPathRef.cpp:649  

#8 0x64829b in SkPathRef::Editor::growForVerb(int, float) /home/monkie/skia-latest/out/asan/../../include/private/SkPathRef.h:76:30  

#9 0x64829b in SkPath::conicTo(float, float, float, float, float) /home/monkie/skia-latest/out/asan/../../src/core/SkPath.cpp:841  

#10 0x64d2b9 in SkPath::conicTo(SkPoint const&, SkPoint const&, float) /home/monkie/skia-latest/out/asan/../../include/core/SkPath.h:716:22  

#11 0x64d2b9 in SkPath::addOval(SkRect const&, SkPath::Direction, unsigned int) /home/monkie/skia-latest/out/asan/../../src/core/SkPath.cpp:1286  

#12 0x64e27d in SkPath::addOval(SkRect const&, SkPath::Direction) /home/monkie/skia-latest/out/asan/../../src/core/SkPath.cpp:1253:18  

#13 0x63fcd0 in main /home/monkie/skia-latest/out/asan/../../tools/test.cpp:12:11  

#14 0x7f97e7f6082f in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x2082f)

SUMMARY: AddressSanitizer: heap-use-after-free /home/monkie/skia-latest/out/asan/../../include/private/SkPathRef.h:138:47 in SkPathRef::Iter::conicWeight() const  

Shadow bytes around the buggy address:  

0x0c067fff7fd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c067fff7fe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c067fff7ff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c067fff8000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c067fff8010: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x0c067fff8020: fa fa fa fa fa fa fd[fd]fd fa fa fa fa fa fa fa  

0x0c067fff8030: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c067fff8040: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c067fff8050: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c067fff8060: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c067fff8070: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

==6152==ABORTING

## Timeline

### mp...@google.com (2018-09-10)

Thanks for the report!

Reed@, "git blame" lists you as the author of this code and robertphillips@ as the latest committer of the "growForVerb" code. I assume you are the right person to assign this to; if you are not can you suggest a new owner?

Also, the reporter mentioned this pattern may be present in other areas, can you put some effort in to ensure that it is not?

Thanks!

[Monorail components: Internals>Skia]

### sh...@chromium.org (2018-09-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-09-12)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/c3d8a48f1b27370049aa512019cd726c59354743

commit c3d8a48f1b27370049aa512019cd726c59354743
Author: Mike Reed <reed@google.com>
Date: Wed Sep 12 14:29:18 2018

allow path.add(path) safely

Bug: 882423
Change-Id: Ied2ad2d5dfdf00af8f3ba722b522e9602fea5557
Reviewed-on: https://skia-review.googlesource.com/153260
Commit-Queue: Mike Reed <reed@google.com>
Reviewed-by: Robert Phillips <robertphillips@google.com>

[modify] https://crrev.com/c3d8a48f1b27370049aa512019cd726c59354743/tests/PathTest.cpp
[modify] https://crrev.com/c3d8a48f1b27370049aa512019cd726c59354743/src/core/SkPath.cpp


### kj...@chromium.org (2018-09-12)

+metzman, looks like the path api isn't exercised as well by the fuzzers as we thought.

https://github.com/google/skia/blob/master/fuzz/FuzzCommon.cpp#L12

robertphillips@ said he'd possibly take a look at vamping it up.

### bu...@chromium.org (2018-09-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7f7888a12e1923fce6ffeb876018e141f9de89ce

commit 7f7888a12e1923fce6ffeb876018e141f9de89ce
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Sep 12 17:19:01 2018

Roll src/third_party/skia b2acf0a93927..16322637c477 (4 commits)

https://skia.googlesource.com/skia.git/+log/b2acf0a93927..16322637c477


git log b2acf0a93927..16322637c477 --date=short --no-merges --format='%ad %ae %s'
2018-09-12 fmalita@chromium.org [sksg] Trim down sksg::Matrix size
2018-09-12 reed@google.com remove SK_SUPPORT_LEGACY_TYPEFACE_MAKEFROMSTREAM
2018-09-12 brianosman@google.com Remove raw-data version of createTextureProxy
2018-09-12 reed@google.com allow path.add(path) safely


Created with:
  gclient setdep -r src/third_party/skia@16322637c477

The AutoRoll server is located here: https://autoroll.skia.org/r/skia-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.

CQ_INCLUDE_TRYBOTS=master.tryserver.blink:linux_trusty_blink_rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel

BUG=chromium:882423
TBR=caryclark@chromium.org

Change-Id: I1541aa1f48d76c6ba1ac980f0c1dd37e413a28f2
Reviewed-on: https://chromium-review.googlesource.com/1221967
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#590737}
[modify] https://crrev.com/7f7888a12e1923fce6ffeb876018e141f9de89ce/DEPS


### bu...@chromium.org (2018-09-12)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/5e4e5451ff901ee8a148bd7cc1e6f1f8e29a519e

commit 5e4e5451ff901ee8a148bd7cc1e6f1f8e29a519e
Author: Robert Phillips <robertphillips@google.com>
Date: Wed Sep 12 17:25:25 2018

Expand SkPath fuzzer

Bug: 882423
Change-Id: Ib1599c84798de74b9e7ecefffb47f22fd12f5a8f
Reviewed-on: https://skia-review.googlesource.com/153889
Reviewed-by: Kevin Lubick <kjlubick@google.com>
Commit-Queue: Robert Phillips <robertphillips@google.com>

[modify] https://crrev.com/5e4e5451ff901ee8a148bd7cc1e6f1f8e29a519e/fuzz/FuzzCommon.cpp


### bu...@chromium.org (2018-09-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9b08f99ae803cc937a17a9e15dd08aaf85fe2f98

commit 9b08f99ae803cc937a17a9e15dd08aaf85fe2f98
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Sep 12 20:22:33 2018

Roll src/third_party/skia 16322637c477..b8e125281d50 (6 commits)

https://skia.googlesource.com/skia.git/+log/16322637c477..b8e125281d50


git log 16322637c477..b8e125281d50 --date=short --no-merges --format='%ad %ae %s'
2018-09-12 caryclark@skia.org Revert "remove SK_SUPPORT_LEGACY_TYPEFACE_MAKEFROMSTREAM"
2018-09-12 jcgregorio@google.com Fix container builder command line.
2018-09-12 mtklein@google.com revise p3 GM
2018-09-12 brianosman@google.com Add F16 test-case to all_bitmap_configs
2018-09-12 robertphillips@google.com Expand SkPath fuzzer
2018-09-12 halcanary@google.com SkPDF: do all rasterScale calculations in one place.


Created with:
  gclient setdep -r src/third_party/skia@b8e125281d50

The AutoRoll server is located here: https://autoroll.skia.org/r/skia-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.

CQ_INCLUDE_TRYBOTS=master.tryserver.blink:linux_trusty_blink_rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel

BUG=chromium:882423
TBR=caryclark@chromium.org

Change-Id: I31ff5e314ae0e482f71f49c257c25adac68b6168
Reviewed-on: https://chromium-review.googlesource.com/1222209
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#590804}
[modify] https://crrev.com/9b08f99ae803cc937a17a9e15dd08aaf85fe2f98/DEPS


### bu...@chromium.org (2018-09-13)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/8051d38358293df1e5b8a1a513f8114147ec9fa3

commit 8051d38358293df1e5b8a1a513f8114147ec9fa3
Author: Robert Phillips <robertphillips@google.com>
Date: Thu Sep 13 13:10:33 2018

Fix SkPath::reverseAddPath and fuzzing of SkPath enums

Bug: 882423
Change-Id: I2be2863574a5951b86e4d5e213094efee6081098
Reviewed-on: https://skia-review.googlesource.com/154300
Reviewed-by: Kevin Lubick <kjlubick@google.com>
Reviewed-by: Greg Daniel <egdaniel@google.com>
Commit-Queue: Robert Phillips <robertphillips@google.com>

[modify] https://crrev.com/8051d38358293df1e5b8a1a513f8114147ec9fa3/fuzz/FuzzCommon.cpp
[modify] https://crrev.com/8051d38358293df1e5b8a1a513f8114147ec9fa3/src/core/SkPath.cpp


### bu...@chromium.org (2018-09-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1e75f8f872e92b7b4615df2f0c47359e3e498175

commit 1e75f8f872e92b7b4615df2f0c47359e3e498175
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Sep 13 15:31:24 2018

Roll src/third_party/skia 637c06aec7b1..d2916264aae0 (4 commits)

https://skia.googlesource.com/skia.git/+log/637c06aec7b1..d2916264aae0


git log 637c06aec7b1..d2916264aae0 --date=short --no-merges --format='%ad %ae %s'
2018-09-13 stephana@google.com [infra] Add pubsub emulator to gcloud asset
2018-09-13 brianosman@google.com Defer mip-mapping until lazy proxy instantiation
2018-09-13 mtklein@google.com add a linear gradient to P3 gm
2018-09-13 robertphillips@google.com Fix SkPath::reverseAddPath and fuzzing of SkPath enums


Created with:
  gclient setdep -r src/third_party/skia@d2916264aae0

The AutoRoll server is located here: https://autoroll.skia.org/r/skia-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.

CQ_INCLUDE_TRYBOTS=master.tryserver.blink:linux_trusty_blink_rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel

BUG=chromium:882423
TBR=caryclark@chromium.org

Change-Id: Icc65a9c71f5c9970e104dad2d7e313a4fa2221b3
Reviewed-on: https://chromium-review.googlesource.com/1224591
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#591020}
[modify] https://crrev.com/1e75f8f872e92b7b4615df2f0c47359e3e498175/DEPS


### sh...@chromium.org (2018-09-25)

reed: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2018-09-25)

I think we have addressed this and similar related issues.

### sh...@chromium.org (2018-09-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-01)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-03)

reed@ - could you confirm that the vulnerable code is reachable from Chrome?  Cheers!

### [Deleted User] (2018-10-04)

reed@ can confirm but I believe Chrome could have run afoul of this bug.

### [Deleted User] (2018-10-04)

Well, NewTabButton::GetHitTestMask gets a path from NewTabButton::GetBorderPath (which can add conics to the returned path) and then calls addPath - adding the returned path to its mask path. AFAICT that mask path is always empty though. So, although Chrome comes close, I don't think it would actually trigger this bug.

Still, there is nothing preventing Chrome from using SkPath in a manner that would trigger this bug.

Someone more familiar with Chrome might be able to provide more insight.

### aw...@google.com (2018-10-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-10-15)

Nice one hungtt28k55@! The VRP panel decided to award $1,000 for this bug. A member of our finance team will be in touch to arrange payment. Also, how would you like to be credited in Chrome release notes?

### aw...@chromium.org (2018-10-15)

[Empty comment from Monorail migration]

### hu...@gmail.com (2018-10-15)

Thank all team! Please credit me as Tran Tien Hung (@hungtt28) of Viettel Cyber Security.

Thanks!

### sh...@chromium.org (2018-10-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-26)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-10-26)

(Already in 71)

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/882423?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092420)*
