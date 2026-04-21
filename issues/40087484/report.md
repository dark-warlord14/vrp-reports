# Heap-buffer-overflow in SkSpecularLightingImageFilter::onFilterImage

| Field | Value |
|-------|-------|
| **Issue ID** | [40087484](https://issues.chromium.org/issues/40087484) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sw...@gmail.com |
| **Assignee** | fm...@chromium.org |
| **Created** | 2017-04-28 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

Please check the ASAN output.

# ./filter\_fuzz\_stub ./poc\_fetch.fil [0428/121026.624422:INFO:filter\_fuzz\_stub.cc(59)] Test case: ./poc\_fetch.fil [0428/121026.624912:INFO:filter\_fuzz\_stub.cc(36)] Valid stream detected.

==32099==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000000cf0 at pc 0x000000e80574 bp 0x7ffcd82a9550 sp 0x7ffcd82a9548  

READ of size 4 at 0x602000000cf0 thread T0  

#0 0xe80573 in Fetch third\_party/skia/src/effects/SkLightingImageFilter.cpp:203:20  

#1 0xe80573 in lightBitmap<SpecularLightingType, SkSpotLight, DecalPixelFetcher> third\_party/skia/src/effects/SkLightingImageFilter.cpp:226  

#2 0xe80573 in lightBitmap<SpecularLightingType, SkSpotLight> third\_party/skia/src/effects/SkLightingImageFilter.cpp:311  

#3 0xe80573 in SkSpecularLightingImageFilter::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkLightingImageFilter.cpp:1516  

#4 0x69ad49 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:216:40  

#5 0xc5f1db in SkBitmapDevice::drawSpecial(SkSpecialImage\*, int, int, SkPaint const&) third\_party/skia/src/core/SkBitmapDevice.cpp:406:49  

#6 0x55ce24 in SkCanvas::internalDrawDevice(SkBaseDevice\*, int, int, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:1330:25  

#7 0x5589c1 in SkCanvas::internalRestore() third\_party/skia/src/core/SkCanvas.cpp:1221:19  

#8 0x5752d9 in ~AutoDrawLooper third\_party/skia/src/core/SkCanvas.cpp:506:22  

#9 0x5752d9 in SkCanvas::onDrawBitmap(SkBitmap const&, float, float, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:2331  

#10 0x4f81d3 in RunTestCase skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:46:13  

#11 0x4f81d3 in ReadAndRunTestCase skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:65  

#12 0x4f81d3 in main skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:84  

#13 0x7f487461682f in \_\_libc\_start\_main /build/glibc-9tT8Do/glibc-2.23/csu/../csu/libc-start.c:291

0x602000000cf1 is located 0 bytes to the right of 1-byte region [0x602000000cf0,0x602000000cf1)  

allocated by thread T0 here:  

#0 0x4ca033 in \_\_interceptor\_malloc (/home/sweetchip/asan-linux-release-467762/filter\_fuzz\_stub+0x4ca033)  

#1 0x11a3750 in base::UncheckedMalloc(unsigned long, void\*\*) base/process/memory\_linux.cc:203:13  

#2 0x11a3648 in base::UncheckedCalloc(unsigned long, unsigned long, void\*\*) base/process/memory.cc:45:8  

#3 0x5269ab in sk\_calloc(unsigned long) skia/ext/SkMemory\_new\_handler.cpp:102:19  

#4 0x6a9dd6 in MakeUsing third\_party/skia/src/core/SkMallocPixelRef.cpp:83:18  

#5 0x6a9dd6 in SkMallocPixelRef::MakeZeroed(SkImageInfo const&, unsigned long, sk\_sp<SkColorTable>) third\_party/skia/src/core/SkMallocPixelRef.cpp:102  

#6 0x7dc61b in SkSpecialSurface::MakeRaster(SkImageInfo const&, SkSurfaceProps const\*) third\_party/skia/src/core/SkSpecialSurface.cpp:101:28  

#7 0x7d6bf0 in SkSpecialImage\_Raster::onMakeSurface(SkImageFilter::OutputProperties const&, SkISize const&, SkAlphaType) const third\_party/skia/src/core/SkSpecialImage.cpp:271:16  

#8 0x7d5570 in SkSpecialImage::makeSurface(SkImageFilter::OutputProperties const&, SkISize const&, SkAlphaType) const third\_party/skia/src/core/SkSpecialImage.cpp:158:26  

#9 0x6d03e8 in SkMatrixImageFilter::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkMatrixImageFilter.cpp:73:41  

#10 0x69ad49 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:216:40  

#11 0x6a091e in SkImageFilter::filterInput(int, SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:495:41  

#12 0xe6c536 in SkSpecularLightingImageFilter::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkLightingImageFilter.cpp:1441:39  

#13 0x69ad49 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:216:40  

#14 0xc5f1db in SkBitmapDevice::drawSpecial(SkSpecialImage\*, int, int, SkPaint const&) third\_party/skia/src/core/SkBitmapDevice.cpp:406:49  

#15 0x55ce24 in SkCanvas::internalDrawDevice(SkBaseDevice\*, int, int, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:1330:25  

#16 0x5589c1 in SkCanvas::internalRestore() third\_party/skia/src/core/SkCanvas.cpp:1221:19  

#17 0x5752d9 in ~AutoDrawLooper third\_party/skia/src/core/SkCanvas.cpp:506:22  

#18 0x5752d9 in SkCanvas::onDrawBitmap(SkBitmap const&, float, float, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:2331  

#19 0x4f81d3 in RunTestCase skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:46:13  

#20 0x4f81d3 in ReadAndRunTestCase skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:65  

#21 0x4f81d3 in main skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:84  

#22 0x7f487461682f in \_\_libc\_start\_main /build/glibc-9tT8Do/glibc-2.23/csu/../csu/libc-start.c:291

SUMMARY: AddressSanitizer: heap-buffer-overflow third\_party/skia/src/effects/SkLightingImageFilter.cpp:203:20 in Fetch  

Shadow bytes around the buggy address:  

0x0c047fff8140: fa fa 00 fa fa fa 00 00 fa fa 00 00 fa fa 00 00  

0x0c047fff8150: fa fa 00 00 fa fa 00 00 fa fa 00 00 fa fa 00 00  

0x0c047fff8160: fa fa 00 00 fa fa 00 fa fa fa 00 00 fa fa 00 00  

0x0c047fff8170: fa fa 00 fa fa fa 00 00 fa fa 00 00 fa fa 00 00  

0x0c047fff8180: fa fa 00 00 fa fa 00 fa fa fa 00 fa fa fa 00 07  

=>0x0c047fff8190: fa fa fd fd fa fa fd fd fa fa fd fd fa fa[01]fa  

0x0c047fff81a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c047fff81b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c047fff81c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c047fff81d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c047fff81e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

==32099==ABORTING

**VERSION**  

Chrome Version: asan-linux-release-467762  

Operating System:

- Ubuntu 16.04.1 LTS 64bit (Server)
- Linux ubuntu 4.4.0-65-generic #86-Ubuntu SMP Thu Feb 23 17:49:58 UTC 2017 x86\_64 x86\_64 x86\_64 GNU/Linux

**REPRODUCTION CASE**  

./filter\_fuzz\_stub ./poc\_fetch.fil

## Attachments

- [poc_fetch.fil](attachments/poc_fetch.fil) (application/octet-stream, 512 B)

## Timeline

### cl...@chromium.org (2017-04-28)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5297163820335104

### cl...@chromium.org (2017-04-28)

Detailed report: https://clusterfuzz.com/testcase?key=5297163820335104

Job Type: linux_asan_filter_fuzz_stub
Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x609000003b00
Crash State:
  SkSpecularLightingImageFilter::onFilterImage
  SkImageFilter::filterImage
  SkBitmapDevice::drawSpecial
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_filter_fuzz_stub&range=423391:423441

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5297163820335104


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.


### sh...@chromium.org (2017-04-28)

[Empty comment from Monorail migration]

### pa...@chromium.org (2017-04-28)

[Empty comment from Monorail migration]

[Monorail components: Internals>Skia]

### sh...@chromium.org (2017-04-29)

[Empty comment from Monorail migration]

### pe...@chromium.org (2017-05-03)

Hi Florin,

Slight chance your CL may be related to this new security bug.  (SkBitmapDevice::drawSpecial)

https://skia.googlesource.com/skia.git/+/53f77bd4fdd76525b66b7f26d1c5c550858120df

Please have a look.  Feel free to transfer if you can find another owner!

Thanks.



### fm...@chromium.org (2017-05-03)

I'll investigate, but the code added in that CL is currently not used at all - so most likely unrelated. 

### bu...@chromium.org (2017-05-03)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/f40b24913a99fc6fcc4b7f60e4dfcda980a16ee1

commit f40b24913a99fc6fcc4b7f60e4dfcda980a16ee1
Author: Florin Malita <fmalita@chromium.org>
Date: Wed May 03 20:02:07 2017

Validate SkSpecialSurface raster info

BUG=chromium:716311

Change-Id: I01ea2e77ba8920f735395dd46ef2cea78a858308
Reviewed-on: https://skia-review.googlesource.com/15230
Reviewed-by: Mike Reed <reed@google.com>
Reviewed-by: Robert Phillips <robertphillips@google.com>
Commit-Queue: Florin Malita <fmalita@chromium.org>

[modify] https://crrev.com/f40b24913a99fc6fcc4b7f60e4dfcda980a16ee1/src/core/SkSurfacePriv.h
[modify] https://crrev.com/f40b24913a99fc6fcc4b7f60e4dfcda980a16ee1/src/image/SkSurface_Raster.cpp
[modify] https://crrev.com/f40b24913a99fc6fcc4b7f60e4dfcda980a16ee1/src/core/SkSpecialSurface.cpp


### fm...@chromium.org (2017-05-03)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-05-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/be67624e633fc0d3bd8a221707eebf0815c3ca8b

commit be67624e633fc0d3bd8a221707eebf0815c3ca8b
Author: skia-deps-roller@chromium.org <skia-deps-roller@chromium.org>
Date: Thu May 04 00:17:06 2017

Roll src/third_party/skia/ ab244f045..6d4b65e9d (11 commits; 2 trivial rolls)

https://skia.googlesource.com/skia.git/+log/ab244f045a07..6d4b65e9dad9

$ git log ab244f045..6d4b65e9d --date=short --no-merges --format='%ad %ae %s'
2017-05-03 bsalomon Revert "Revert "Add a new non-AA rect op that does not inherit from GrLegacyMeshDrawOp.""
2017-05-03 mtklein treat SkPMColor as sRGB in SkPM4f::FromPMColor()
2017-05-03 bsalomon Revert "Add a new non-AA rect op that does not inherit from GrLegacyMeshDrawOp."
2017-05-03 bsalomon Add a new non-AA rect op that does not inherit from GrLegacyMeshDrawOp.
2017-05-03 mtklein fix G3 opt android_arm build?
2017-05-03 mtklein disable test_diagonal on 565
2017-05-03 fmalita Validate SkSpecialSurface raster info
2017-04-05 halcanary headers: fix
2017-05-03 fmalita Add a GM to exercise some complex gradient constructs

Created with:
  roll-dep src/third_party/skia
BUG=716311


Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, see:
http://www.chromium.org/developers/tree-sheriffs/sheriff-details-chromium#TOC-Failures-due-to-DEPS-rolls


CQ_INCLUDE_TRYBOTS=master.tryserver.blink:linux_trusty_blink_rel;master.tryserver.chromium.linux:linux_optional_gpu_tests_rel;master.tryserver.chromium.mac:mac_optional_gpu_tests_rel;master.tryserver.chromium.win:win_optional_gpu_tests_rel;master.tryserver.chromium.android:android_optional_gpu_tests_rel
TBR=scroggo@chromium.org

Change-Id: I0ef3efa6313f3f0815315cf662a0c94729c34b58
Reviewed-on: https://chromium-review.googlesource.com/494969
Reviewed-by: Skia Deps Roller <skia-deps-roller@chromium.org>
Commit-Queue: Skia Deps Roller <skia-deps-roller@chromium.org>
Cr-Commit-Position: refs/heads/master@{#469211}
[modify] https://crrev.com/be67624e633fc0d3bd8a221707eebf0815c3ca8b/DEPS


### cl...@chromium.org (2017-05-04)

ClusterFuzz has detected this issue as fixed in range 469194:469229.

Detailed report: https://clusterfuzz.com/testcase?key=5297163820335104

Job Type: linux_asan_filter_fuzz_stub
Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x609000003b00
Crash State:
  SkSpecularLightingImageFilter::onFilterImage
  SkImageFilter::filterImage
  SkBitmapDevice::drawSpecial
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_filter_fuzz_stub&range=423391:423441
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_filter_fuzz_stub&range=469194:469229

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5297163820335104


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### sh...@chromium.org (2017-05-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-09)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), gkihumba@(ChromeOS), Abdul Syed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2017-05-09)

awhalley@ can you please confirm if this okay to merge to M59 from security perspective?

### aw...@google.com (2017-05-10)

abdulsyed@ - Let's wait until this has spent a couple of days on dev.

### aw...@chromium.org (2017-05-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-15)

Congratulations! The panel decided to award $1,000 for this one!

### aw...@chromium.org (2017-05-15)

abdulsyed@ - good for M59 now.

### sh...@chromium.org (2017-05-15)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), gkihumba@(ChromeOS), Abdul Syed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-05-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-15)

re #21, note that we're only after the "Validate SkSpecialSurface raster info" change, if that can be cherrypicked to avoid a full roll.

### bu...@chromium.org (2017-05-15)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/89bdf7d5b69a0fbee7c1a7da3ef7ae1e15612bef

commit 89bdf7d5b69a0fbee7c1a7da3ef7ae1e15612bef
Author: Florin Malita <fmalita@chromium.org>
Date: Mon May 15 18:06:00 2017

[M59] Validate SkSpecialSurface raster info

Cherry-pick https://skia-review.googlesource.com/c/15230/

BUG=chromium:716311
NOTREECHECKS=true
NOTRY=true
NOPRESUBMIT=true
Change-Id: I01ea2e77ba8920f735395dd46ef2cea78a858308
Reviewed-On: https://skia-review.googlesource.com/15230
Reviewed-By: Mike Reed <reed@google.com>
Reviewed-By: Robert Phillips <robertphillips@google.com>
Commit-Queue: Florin Malita <fmalita@chromium.org>
Reviewed-on: https://skia-review.googlesource.com/16906
Reviewed-by: Florin Malita <fmalita@chromium.org>

[modify] https://crrev.com/89bdf7d5b69a0fbee7c1a7da3ef7ae1e15612bef/src/core/SkSurfacePriv.h
[modify] https://crrev.com/89bdf7d5b69a0fbee7c1a7da3ef7ae1e15612bef/src/image/SkSurface_Raster.cpp
[modify] https://crrev.com/89bdf7d5b69a0fbee7c1a7da3ef7ae1e15612bef/src/core/SkSpecialSurface.cpp


### fm...@chromium.org (2017-05-15)

Sorry, I misread c#20 as approved for m59 and merged already.

Let me know if I should revert.

### go...@chromium.org (2017-05-15)

No need to revert as it is already approved at #20. 
Removing "Merge-Review-59" label as it is already merged at #24. Thank you.

### aw...@chromium.org (2017-05-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-30)

[Empty comment from Monorail migration]

### gk...@google.com (2017-06-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/716311?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087484)*
