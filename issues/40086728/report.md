# Security: Heap Buffer OverFlow Vulnerability in Skia

| Field | Value |
|-------|-------|
| **Issue ID** | [40086728](https://issues.chromium.org/issues/40086728) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Reporter** | ku...@gmail.com |
| **Assignee** | re...@google.com |
| **Created** | 2017-02-06 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

Heap Buffer Overflow Vulnerability triggered in Skia.

Analysis done on LINUX System, Only the reporting was done on Windows System.

PoC has been tested on several latest Chrome Linux "asan" builds as of Feb 6 2:28AM PST.

Build links have been shared in the Step 1 of the "Reproduction Case" section.

**VERSION**  

Chrome Version: Latest Linux "asan" release builds.

Operating System: Ubuntu

**REPRODUCTION CASE**

1. Download chrome "asan" build from <https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release-v8-arm%2Fasan-v8-arm-linux-release-448209.zip?generation=1486369017083714&alt=media>  
   
   OR
2. Download chrome "asan" build from <https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-beta-57.0.2987.21.zip?generation=1486245228572145&alt=media>  
   
   OR
3. Download chrome "asan" build from <https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-release-448206.zip?generation=1486365824856220&alt=media>
4. Unzip the downloaded "asan" builds.
5. Change directory to filter\_fuzz\_stub location.
6. Run the filter\_fuzz\_stub binary against the PoC.fil testcase file.
7. Check the crash details in the terminal window.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

Binary crashes due to trigger of Heap Buffer Overflow Vulnerability.

See ASAN Output Below: -

==29217==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xf4000354 at pc 0x085b1674 bp 0xffa33b18 sp 0xffa33b10  

READ of size 4 at 0xf4000354 thread T0  

#0 0x85b1673 in findScanline third\_party/skia/src/core/SkRegionPriv.h:156:26  

#1 0x85b1673 in SkRegion::contains(int, int) const third\_party/skia/src/core/SkRegion.cpp:322  

#2 0x900c4af in SkAlphaThresholdFilterImpl::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/effects/SkAlphaThresholdFilter.cpp:237:25  

#3 0x843266b in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const third\_party/skia/src/core/SkImageFilter.cpp:216:40  

#4 0x8c42fed in SkBitmapDevice::drawSpecial(SkDraw const&, SkSpecialImage\*, int, int, SkPaint const&) third\_party/skia/src/core/SkBitmapDevice.cpp:401:49  

#5 0x822af27 in SkCanvas::onDrawBitmap(SkBitmap const&, float, float, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:2420:27  

#6 0x8218c36 in SkCanvas::drawBitmap(SkBitmap const&, float, float, SkPaint const\*) third\_party/skia/src/core/SkCanvas.cpp:1933:11  

#7 0x813b499 in RunTestCase skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:46:13  

#8 0x813b499 in ReadAndRunTestCase skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:65  

#9 0x813b499 in main skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:84  

#10 0xf69307ad in \_\_libc\_start\_main /build/glibc-xt1eTb/glibc-2.21/csu/libc-start.c:289

0xf4000354 is located 0 bytes to the right of 20-byte region [0xf4000340,0xf4000354)  

allocated by thread T0 here:  

#0 0x810eff6 in \_\_interceptor\_malloc (/home/h4ck3r/Desktop/linux-release-v8-arm-asan-v8-arm-linux-release/asan-v8-arm-linux-release-448209/filter\_fuzz\_stub+0x810eff6)  

#1 0x81bd28c in sk\_malloc\_throw(unsigned int) skia/ext/SkMemory\_new\_handler.cpp:64:66  

#2 0x85b9c4f in Alloc third\_party/skia/src/core/SkRegionPriv.h:70:35  

#3 0x85b9c4f in Alloc third\_party/skia/src/core/SkRegionPriv.h:83  

#4 0x85b9c4f in allocateRuns third\_party/skia/src/core/SkRegion.cpp:103  

#5 0x85b9c4f in SkRegion::readFromMemory(void const\*, unsigned int) third\_party/skia/src/core/SkRegion.cpp:1142  

#6 0x864acd5 in SkValidatingReadBuffer::readRegion(SkRegion\*) third\_party/skia/src/core/SkValidatingReadBuffer.cpp:167:24  

#7 0x9009057 in SkAlphaThresholdFilterImpl::CreateProc(SkReadBuffer&) third\_party/skia/src/effects/SkAlphaThresholdFilter.cpp:82:12  

#8 0x864d0a8 in SkValidatingReadBuffer::readFlattenable(SkFlattenable::Type) third\_party/skia/src/core/SkValidatingReadBuffer.cpp:289:11  

#9 0x8428b47 in SkValidatingDeserializeFlattenable third\_party/skia/src/core/SkFlattenableSerialization.cpp:26:19  

#10 0x8428b47 in SkValidatingDeserializeImageFilter(void const\*, unsigned int) third\_party/skia/src/core/SkFlattenableSerialization.cpp:30  

#11 0x813b154 in RunTestCase skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:31:38  

#12 0x813b154 in ReadAndRunTestCase skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:65  

#13 0x813b154 in main skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:84  

#14 0xf69307ad in \_\_libc\_start\_main /build/glibc-xt1eTb/glibc-2.21/csu/libc-start.c:289

SUMMARY: AddressSanitizer: heap-buffer-overflow third\_party/skia/src/core/SkRegionPriv.h:156:26 in findScanline  

Shadow bytes around the buggy address:  

0x3e800010: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3e800020: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3e800030: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3e800040: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3e800050: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x3e800060: fa fa fd fd fd fd fa fa 00 00[04]fa fa fa fd fd  

0x3e800070: fd fd fa fa 00 00 00 07 fa fa 00 00 00 00 fa fa  

0x3e800080: 00 00 00 00 fa fa 00 00 00 00 fa fa 00 00 00 00  

0x3e800090: fa fa 00 00 00 00 fa fa 00 00 04 fa fa fa 00 00  

0x3e8000a0: 04 fa fa fa 00 00 04 fa fa fa 00 00 04 fa fa fa  

0x3e8000b0: 00 00 04 fa fa fa 00 00 04 fa fa fa 00 00 04 fa  

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

==29217==ABORTING

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### ku...@gmail.com (2017-02-06)

Just checked after filing the report that a new "asan" build(#448219) was released few minutes back.

I would like to confirm that the issue still exists in the latest build.

Thanks & Regards,
~ Kushal.

### xz...@chromium.org (2017-02-06)

[Empty comment from Monorail migration]

[Monorail components: Internals>Skia]

### xz...@chromium.org (2017-02-06)

mbarbella@, how to add skia poc to cluster-fuzz?

### mb...@chromium.org (2017-02-06)

Upload the test case using the linux_asan_filter_fuzz_stub job type.

### sh...@chromium.org (2017-02-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-02-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5539042797289472

### ji...@chromium.org (2017-02-07)

reed@, could you help triage this issue? Thanks!

### cl...@chromium.org (2017-02-07)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5539042797289472

Job Type: linux_asan_filter_fuzz_stub
Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x60a000000954
Crash State:
  SkRegion::contains
  SkAlphaThresholdFilterImpl::onFilterImage
  SkImageFilter::filterImage
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub&range=363565:363834

Reproducer Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94uzYDuNtyaABK7OzWcOC7krQvI5a_i5YGvjvTF69oNRRPAE7A4eE8YUanO06NXgYYf38wF277n6WMb9Ebwki3ELcd-iFE5XSwcbLGmdHDJM4iHV-pxiPI_5BSgMLnL94BKXzyyWWSyDO3M5rVebXKeaYOc1LPL1Itr1W00KZKcitwWgI78nS-nL_0aK80_fLWWixXSHAA7jTqg8nr_HeXuPAyrsy8I_zMVgzodvMSvG-vZPip4vZrbwFLkUBvZBwqkc5m75tdQ-h1s2Al3Ar4YQojZubwqLrtwKiB_S2OUBTg5KOz63wrmZDwvKsUqvyPxjSJSWVwS4nGVa5ECEtHHsZKiHrknle_HI7w1NDJDif1MqclEXGdkk0MHig_8zFmIzVZNwie9kbJx6lCCpgaQY0QSlw?testcase_id=5539042797289472


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

The recommended severity is different from what was assigned to the bug. Please double check the accuracy of the assigned severity.


### ji...@chromium.org (2017-02-07)

+cc senorblanco@, possibly caused by https://chromium.googlesource.com/skia.git/+/c41e7e14f4a0076d277870502168ed870e558dfc  ? 

### ku...@gmail.com (2017-02-07)

Hello xzhou@chromium.org, reed@chromium.org, jialiul@chromium.org, @mbarbella, Google Security Team, 

Good Morning.

I was thinking of how I could help in fixing this vulnerability quickly and I came across a similar previously fixed issue in crbug.com/609260.

I could be wrong but, I think the fix applied at that time(almost 9 months back) might have been incomplete which led to the current vulnerability. No offense meant to the person/team who fixed the issue then.

Hope this small bit of information helps in the current triage phase.

Thanks & Regards,
~ Kushal Shah.

### se...@chromium.org (2017-02-07)

I suspect the SkRegion flattening code has always had this vulnerability, and that it was exposed by https://chromium.googlesource.com/skia.git/+/0745653a677f405bb683b7f7a71b56a7e0dc7921.

Note that this is vulnerability is unlikely to be web-exposed, since SkAlphaThresholdFilter is not web-exposed (AFAIK). It's only seen in filter_fuzz_stub since it fuzzes all image filters, not just the ones which are web-exposed.

### ku...@gmail.com (2017-02-07)

@senorblanco,

Good Afternoon.

AFAIK SkAlphaThresholdFilter is a skia effect filter under the parent SkImageFilter that creates an image filter on a region(SkRegion) of a drawing and could be used for web-purposes also for a given input image/drawing similar to other Skia ImageFilter Effects.

Could you provide any reference/documentation that explicitly states that "SkAlphaThresholdFilter is not web-exposed". 


Thanks & Regards,
~ Kushal Shah.

### ku...@gmail.com (2017-02-09)

No reply on c#14.

Nevertheless, the vulnerability still exists and is similar to previously fixed crbug.com/609260 and once again needs a permanent fix.

Thanks & Regards,
~ Kushal Shah.

### aw...@chromium.org (2017-02-13)

Removing ReleaseBlock-Stable per https://crbug.com/chromium/688987#c13. Please re-apply if SkAlphaThresholdFilter does turn out to be web-exposed.

### sh...@chromium.org (2017-02-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-14)

Going to keep the re-applied ReleaseBlock-Stable for now (thanks sheriffbot!). We're going to assume that anything found via filter_fuzz_stub is web accessible, but I've started a thread to confirm if this is the case or not. 

### sh...@chromium.org (2017-02-15)

[Empty comment from Monorail migration]

### hc...@chromium.org (2017-02-16)

Any confirmation on the web exposure in Chrome?  And Pri-0??  Code here has not changed in years, seems this is something that has been in existence.

Mike & Hal pls help investigate.

### ha...@chromium.org (2017-02-16)

[Empty comment from Monorail migration]

### hc...@chromium.org (2017-02-16)

+Kevin FYI as we'd like to investigate fuzzing regions in Skia

### mb...@chromium.org (2017-02-16)

We weren't assuming that these are web accessible, but rather accessible from a compromised renderer. Reducing severity/priority to be in line with how we usually treat sandbox escapes. It would still be good to get some insight from skia devs more familiar with this, in case that's not correct.

### ha...@chromium.org (2017-02-16)

I have a fix
https://review.skia.org/8496

### go...@chromium.org (2017-02-16)

A friendly reminder that M57 Stable is launch is coming VERY soon! Your bug is labelled as Stable ReleaseBlock, pls make sure to land the fix and get it merged into the release branch (2987) ASAP so it gets enough baking time in Beta (before Stable promotion). Thank you!

### bu...@chromium.org (2017-02-18)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/251bf3e089b7422980e39bff38623c5b726c2ee4

commit 251bf3e089b7422980e39bff38623c5b726c2ee4
Author: Hal Canary <halcanary@google.com>
Date: Sat Feb 18 13:34:30 2017

SkRegion deserialization more robust

BUG=chromium:688987
Change-Id: Ide6d70330c8cd1fce814eb2c445da1fbff498ef6
Reviewed-on: https://skia-review.googlesource.com/8496
Commit-Queue: Hal Canary <halcanary@google.com>
Reviewed-by: Kevin Lubick <kjlubick@google.com>

[modify] https://crrev.com/251bf3e089b7422980e39bff38623c5b726c2ee4/tests/RegionTest.cpp
[modify] https://crrev.com/251bf3e089b7422980e39bff38623c5b726c2ee4/src/core/SkRegion.cpp
[modify] https://crrev.com/251bf3e089b7422980e39bff38623c5b726c2ee4/src/core/SkRegionPriv.h
[modify] https://crrev.com/251bf3e089b7422980e39bff38623c5b726c2ee4/include/core/SkRegion.h


### ha...@chromium.org (2017-02-18)

As soon as the next skia-chromium deps roll lands, you can verify that 251bf3e089 fixes the asan error and we can cherry-pick this to chrome/m57: https://review.skia.org/8694 .

### sh...@chromium.org (2017-02-18)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-02-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d86925891e54a45759226daaa919c6fd50c0e715

commit d86925891e54a45759226daaa919c6fd50c0e715
Author: skia-deps-roller <skia-deps-roller@chromium.org>
Date: Sat Feb 18 17:11:35 2017

Roll src/third_party/skia/ 7fc4a2d2f..f71828f7e (3 commits).

https://skia.googlesource.com/skia.git/+log/7fc4a2d2f0eb..f71828f7e4f4

$ git log 7fc4a2d2f..f71828f7e --date=short --no-merges --format='%ad %ae %s'
2017-02-18 reed all DM to include from src/xml
2017-02-16 halcanary SkRegion deserialization more robust
2017-02-17 mtklein SkJumper: aarch64 and armv7

Created with:
  roll-dep src/third_party/skia
BUG=688987

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, see:
http://www.chromium.org/developers/tree-sheriffs/sheriff-details-chromium#TOC-Failures-due-to-DEPS-rolls

CQ_INCLUDE_TRYBOTS=master.tryserver.blink:linux_trusty_blink_rel
TBR=bungeman@google.com

Review-Url: https://codereview.chromium.org/2704883002
Cr-Commit-Position: refs/heads/master@{#451469}

[modify] https://crrev.com/d86925891e54a45759226daaa919c6fd50c0e715/DEPS


### cl...@chromium.org (2017-02-19)

ClusterFuzz has detected this issue as fixed in range 451463:451487.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5539042797289472

Job Type: linux_asan_filter_fuzz_stub
Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x60a000000954
Crash State:
  SkRegion::contains
  SkAlphaThresholdFilterImpl::onFilterImage
  SkImageFilter::filterImage
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub&range=363565:363834
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub&range=451463:451487

Reproducer Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94uzYDuNtyaABK7OzWcOC7krQvI5a_i5YGvjvTF69oNRRPAE7A4eE8YUanO06NXgYYf38wF277n6WMb9Ebwki3ELcd-iFE5XSwcbLGmdHDJM4iHV-pxiPI_5BSgMLnL94BKXzyyWWSyDO3M5rVebXKeaYOc1LPL1Itr1W00KZKcitwWgI78nS-nL_0aK80_fLWWixXSHAA7jTqg8nr_HeXuPAyrsy8I_zMVgzodvMSvG-vZPip4vZrbwFLkUBvZBwqkc5m75tdQ-h1s2Al3Ar4YQojZubwqLrtwKiB_S2OUBTg5KOz63wrmZDwvKsUqvyPxjSJSWVwS4nGVa5ECEtHHsZKiHrknle_HI7w1NDJDif1MqclEXGdkk0MHig_8zFmIzVZNwie9kbJx6lCCpgaQY0QSlw?testcase_id=5539042797289472


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### sh...@chromium.org (2017-02-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-19)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), ketakid@(cros), govind@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-02-20)

Note that we're only after the "SkRegion deserialization more robust" change, if this can be cherrypicked into a M57 branch, rather than a full DEPS roll.

### ha...@chromium.org (2017-02-20)

awhalley@, https://review.skia.org/8694 is a cherry-pick to Skia's chrome/m57 branch.

### aw...@chromium.org (2017-02-20)

halcanary@ - ah yes - sorry! Thanks!

### bu...@chromium.org (2017-02-20)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/edee1ae9e3b87983ed0ff0ea55b3c49892901260

commit edee1ae9e3b87983ed0ff0ea55b3c49892901260
Author: Kevin Lubick <kjlubick@google.com>
Date: Mon Feb 20 23:18:58 2017

Write SkRegion fuzzer

BUG=688987

Change-Id: I2ad1c53ea01185a77b662d2d86b0c6d36fcb63c7
Reviewed-on: https://skia-review.googlesource.com/8499
Commit-Queue: Kevin Lubick <kjlubick@google.com>
Reviewed-by: Hal Canary <halcanary@google.com>

[modify] https://crrev.com/edee1ae9e3b87983ed0ff0ea55b3c49892901260/src/ports/SkMemory_malloc.cpp
[modify] https://crrev.com/edee1ae9e3b87983ed0ff0ea55b3c49892901260/BUILD.gn
[modify] https://crrev.com/edee1ae9e3b87983ed0ff0ea55b3c49892901260/gn/BUILDCONFIG.gn
[modify] https://crrev.com/edee1ae9e3b87983ed0ff0ea55b3c49892901260/fuzz/fuzz.cpp


### bu...@chromium.org (2017-02-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7b0df7db9fdc7ca5f972059cf0236f4886b4c884

commit 7b0df7db9fdc7ca5f972059cf0236f4886b4c884
Author: skia-deps-roller <skia-deps-roller@chromium.org>
Date: Tue Feb 21 00:36:16 2017

Roll src/third_party/skia/ a3091099f..edee1ae9e (2 commits).

https://skia.googlesource.com/skia.git/+log/a3091099fa19..edee1ae9e3b8

$ git log a3091099f..edee1ae9e --date=short --no-merges --format='%ad %ae %s'
2017-02-20 kjlubick Write SkRegion fuzzer
2017-02-19 robertphillips Remove asTextureRef from SkSpecialImage & update effects accordingly (take 2)

Created with:
  roll-dep src/third_party/skia
BUG=688987

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, see:
http://www.chromium.org/developers/tree-sheriffs/sheriff-details-chromium#TOC-Failures-due-to-DEPS-rolls

CQ_INCLUDE_TRYBOTS=master.tryserver.blink:linux_trusty_blink_rel
TBR=bsalomon@google.com

Review-Url: https://codereview.chromium.org/2703253004
Cr-Commit-Position: refs/heads/master@{#451676}

[modify] https://crrev.com/7b0df7db9fdc7ca5f972059cf0236f4886b4c884/DEPS


### go...@chromium.org (2017-02-21)

+awhalley@ for M57 merge review.

### aw...@chromium.org (2017-02-23)

This is already in M57 per #34 - the commit in 37 is adding a fuzzer (wooo! More fuzzers! Thanks kjlubick@)

### aw...@chromium.org (2017-02-23)

[Empty comment from Monorail migration]

### ha...@google.com (2017-02-24)

awhalley@, that CL has not landed, since I'm waiting on merge approval.

### aw...@chromium.org (2017-02-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-25)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), ketakid@(cros), govind@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-02-25)

 awhalley@, is this change good to take it in for M57?

### aw...@chromium.org (2017-02-25)

govind@ - yep!

### go...@chromium.org (2017-02-25)

OK, approving merge to M57 branch 2987 based on https://crbug.com/chromium/688987#c44 and #45. Please merge before 5:00 PM PT, Monday (02/27) so we can take it for next week beta release. Thank you.

### bu...@chromium.org (2017-02-25)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/7695359876b8f90225bc4be895c20f34fcdfaf2e

commit 7695359876b8f90225bc4be895c20f34fcdfaf2e
Author: Hal Canary <halcanary@google.com>
Date: Sat Feb 25 15:44:57 2017

SkRegion deserialization more robust

BUG=chromium:688987
Change-Id: Ide6d70330c8cd1fce814eb2c445da1fbff498ef6
Reviewed-on: https://skia-review.googlesource.com/8694
Reviewed-by: Kevin Lubick <kjlubick@google.com>

[modify] https://crrev.com/7695359876b8f90225bc4be895c20f34fcdfaf2e/tests/RegionTest.cpp
[modify] https://crrev.com/7695359876b8f90225bc4be895c20f34fcdfaf2e/src/core/SkRegion.cpp
[modify] https://crrev.com/7695359876b8f90225bc4be895c20f34fcdfaf2e/src/core/SkRegionPriv.h
[modify] https://crrev.com/7695359876b8f90225bc4be895c20f34fcdfaf2e/include/core/SkRegion.h


### go...@chromium.org (2017-02-26)

Per https://crbug.com/chromium/688987#c47, this is already merged to M57. If nothing is pending for M57, please remove "Merge-Approved-57" label. Thank you.

### go...@chromium.org (2017-02-27)

Removing "Merge-Approved-57" label based on https://crbug.com/chromium/688987#c47 and #48. Assuming nothing is pending for M57.

### ku...@gmail.com (2017-02-28)

Hello @xzhou, @reed, @jialiul, @mbarbella, @senorblanco, @hcm, @halcanary, @awhalley, @govind, Google Security Team, 

Good Evening.

Firstly I would like to thank you for fixing this vulnerability so quickly, I sincerely appreciate it.

I would like to kindly request you to use 'Kushal Arvind Shah of Fortinet's FortiGuard Labs' as the credit information in the Chrome Security Release.

Also I would like to request for any update on the CVE-ID and Reward for the same.

Eagerly awaiting your reply in earnest.

Thanking You,

Yours Sincerely,
Kushal Arvind Shah.
Fortinet's FortiGuard Labs.

### aw...@chromium.org (2017-02-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-28)

Hello,

Thanks for the inquiry. The panel has awarded $1,000 for this report, downgrading it to a medium severity since it appears to be a READ only. Please let me know if you can demonstrate the ability to write to memory and we can reconsider.

We consider bugs for CVEs when we write release notes for a new Chrome release.  Though note that this bug is currently marked as impacting a beta release, and therefore wouldn't be eligible for a CVE. Can you demonstrate this bug working on a shipping stable version of Chrome?  

Thanks!

awhalley

### aw...@chromium.org (2017-02-28)

[Empty comment from Monorail migration]

### ku...@gmail.com (2017-02-28)

Hello awhalley,

Firstly I would like to thank you for the generous bounty.

Secondly, I checked the PoC on the stable shipping release of chrome and I am able to reproduce the vulnerability.

The current shipping stable version of Google Chrome available for download 
is 56.0.2924.87 and the same version "asan" build is affected by this vulnerability.

Following are the steps I took to confirm the same: -

1) Download the stable version of chrome from the link : https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-stable-56.0.2924.87.zip?generation=1486082469441404&alt=media

2) Unzip the downloaded chrome stable "asan" build.

3) Change directory to filter_fuzz_stub location.

4) Run the PoC.fil against the filter_fuzz_stub binary.

5) Check the crash details in the terminal window.

=================================================================
==23864==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x6030000002c4 at pc 0x0000006a7205 bp 0x7fff0fe513a0 sp 0x7fff0fe51398
READ of size 4 at 0x6030000002c4 thread T0
    #0 0x6a7204  (/home/h4ck3r/Downloads/asan-linux-stable-56.0.2924.87/filter_fuzz_stub+0x6a7204)
    #1 0xc6347a  (/home/h4ck3r/Downloads/asan-linux-stable-56.0.2924.87/filter_fuzz_stub+0xc6347a)
    #2 0x5cc0f7  (/home/h4ck3r/Downloads/asan-linux-stable-56.0.2924.87/filter_fuzz_stub+0x5cc0f7)
    #3 0xa67288  (/home/h4ck3r/Downloads/asan-linux-stable-56.0.2924.87/filter_fuzz_stub+0xa67288)
    #4 0x574511  (/home/h4ck3r/Downloads/asan-linux-stable-56.0.2924.87/filter_fuzz_stub+0x574511)
    #5 0x4f5c1a  (/home/h4ck3r/Downloads/asan-linux-stable-56.0.2924.87/filter_fuzz_stub+0x4f5c1a)
    #6 0x7f6191cb4abf  (/lib/x86_64-linux-gnu/libc.so.6+0x20abf)

0x6030000002c4 is located 0 bytes to the right of 20-byte region [0x6030000002b0,0x6030000002c4)
allocated by thread T0 here:
    #0 0x4c8e7c  (/home/h4ck3r/Downloads/asan-linux-stable-56.0.2924.87/filter_fuzz_stub+0x4c8e7c)
    #1 0x52ea2d  (/home/h4ck3r/Downloads/asan-linux-stable-56.0.2924.87/filter_fuzz_stub+0x52ea2d)
    #2 0x6ac468  (/home/h4ck3r/Downloads/asan-linux-stable-56.0.2924.87/filter_fuzz_stub+0x6ac468)
    #3 0x701d71  (/home/h4ck3r/Downloads/asan-linux-stable-56.0.2924.87/filter_fuzz_stub+0x701d71)
    #4 0xc606b2  (/home/h4ck3r/Downloads/asan-linux-stable-56.0.2924.87/filter_fuzz_stub+0xc606b2)
    #5 0x70339c  (/home/h4ck3r/Downloads/asan-linux-stable-56.0.2924.87/filter_fuzz_stub+0x70339c)
    #6 0x5c733e  (/home/h4ck3r/Downloads/asan-linux-stable-56.0.2924.87/filter_fuzz_stub+0x5c733e)
    #7 0x4f5a59  (/home/h4ck3r/Downloads/asan-linux-stable-56.0.2924.87/filter_fuzz_stub+0x4f5a59)
    #8 0x7f6191cb4abf  (/lib/x86_64-linux-gnu/libc.so.6+0x20abf)

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/h4ck3r/Downloads/asan-linux-stable-56.0.2924.87/filter_fuzz_stub+0x6a7204) 
Shadow bytes around the buggy address:
  0x0c067fff8000: fa fa fd fd fd fd fa fa fd fd fd fd fa fa fd fd
  0x0c067fff8010: fd fd fa fa fd fd fd fd fa fa fd fd fd fa fa fa
  0x0c067fff8020: fd fd fd fd fa fa 00 00 00 00 fa fa 00 00 00 00
  0x0c067fff8030: fa fa 00 00 00 00 fa fa 00 00 04 fa fa fa 00 00
  0x0c067fff8040: 04 fa fa fa 00 00 04 fa fa fa 00 00 04 fa fa fa
=>0x0c067fff8050: 00 00 04 fa fa fa 00 00[04]fa fa fa fa fa fa fa
  0x0c067fff8060: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c067fff8070: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c067fff8080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c067fff8090: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c067fff80a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==23864==ABORTING

Thus, this bug is impacting a stable release as well and I would like to therefore request a CVE-ID for the same. 

Also I understand that the release notes for a new Chrome release contain the CVE-ID and credit information and I am happy to wait for the same. BUT, I would like to request you to use "Kushal Arvind Shah of Fortinet's FortiGuard Labs" for this bug.

Eagerly awaiting your reply in earnest.


Thanking You,

Yours Sincerely,
Kushal Arvind Shah.
Fortinet's FortiGuard Labs.

### aw...@chromium.org (2017-03-01)

Thank you for the update! I've changed the label so this bug will be allocated a CVE in due course.  Cheers.

### aw...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-08)

[Empty comment from Monorail migration]

### ku...@gmail.com (2017-03-15)

Hello @awhalley, Google Security Team,

Any update on the reward? I haven't received any update from Google Finance Team.

Eagerly awaiting your response in earnest.

Thanking You,

Yours Sincerely,
Kushal Arvind Shah.
Fortinet's FortiGuard Labs.

### sh...@chromium.org (2017-05-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/688987?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086728)*
