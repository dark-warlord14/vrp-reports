# Security: Little-CMS (lcms) Heap Buffer Overflow in AllocateDataSet

| Field | Value |
|-------|-------|
| **Issue ID** | [40092129](https://issues.chromium.org/issues/40092129) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | qu...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2018-08-08 |
| **Bounty** | $3,500.00 |

## Description

**VULNERABILITY DETAILS**

IT8 is a set of ANSI standards for color communications and control specifications. I have audited source code of lcms library and I have founded a vulnerability in AllocateDataSet function (cmscgats.c). The attached it8 could crash lcms when ASAN was enabled on Linux.
 
```
void AllocateDataSet(cmsIT8* it8)
{
    TABLE* t = GetTable(it8);

    if (t -> Data) return;    // Already allocated

    t-> nSamples   = atoi(cmsIT8GetProperty(it8, "NUMBER_OF_FIELDS"));
    t-> nPatches   = atoi(cmsIT8GetProperty(it8, "NUMBER_OF_SETS"));

    t-> Data = (char**)AllocChunk (it8, ((cmsUInt32Number) t->nSamples + 1) * ((cmsUInt32Number) t->nPatches + 1) *sizeof (char*)); // <<------ Vuln here 
    if (t->Data == NULL) {

        SynError(it8, "AllocateDataSet: Unable to allocate data array");
    }
}
```

if `nSamples` is 2 and `nPatches` is 0x55555555, `((cmsUInt32Number) t->nSamples + 1) * ((cmsUInt32Number) t->nPatches + 1) *sizeof (char*)` is larger than the maximum representable value (0xffffffff). The result of an overflow is that the least significant representable bits of the result are stored. `Data` will point to a small memory region and can not use to store large data.


**VERSION**

Chrome Version: All

Operating System: All

**REPRODUCTION CASE**

Following code will trigger crash
```
cmsIT8LoadFromFile(NULL, "AllocateDataSet.crash.IT8");
```

ASAN Log:
```
=================================================================
==12907==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x62a000005200 at pc 0x000000592bc5 bp 0x7ffd5f5c46c0 sp 0x7ffd5f5c46b8
WRITE of size 8 at 0x62a000005200 thread T0
    #0 0x592bc4 in SetData /root/lcms2/lcms2-asan/src/cmscgats.c:1549:45
    #1 0x5986e3 in DataSection /root/lcms2/lcms2-asan/src/cmscgats.c:1894:18
    #2 0x590259 in ParseIT8 /root/lcms2/lcms2-asan/src/cmscgats.c:2070:26
    #3 0x5915e6 in cmsIT8LoadFromFile /root/lcms2/lcms2-asan/src/cmscgats.c:2365:10
    #4 0x4eb86b in main /root/lcms2/test.c:7:5
    #5 0x7f9a0b6b682f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)
    #6 0x41abb8 in _start (/root/lcms2/test+0x41ab68)

0x62a000005200 is located 0 bytes to the right of 20480-byte region [0x62a000000200,0x62a000005200)
allocated by thread T0 here:
    #0 0x4bb2e3 in __interceptor_malloc /tmp/final/llvm.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cc:88:3
    #1 0x4ebca8 in _cmsMallocZero /root/lcms2/lcms2-asan/src/cmserr.c:88:15
    #2 0x59474c in AllocBigBlock /root/lcms2/lcms2-asan/src/cmscgats.c:1053:17
    #3 0x58b62c in AllocChunk /root/lcms2/lcms2-asan/src/cmscgats.c:1095:52
    #4 0x58af66 in cmsIT8Alloc /root/lcms2/lcms2-asan/src/cmscgats.c:1310:35
    #5 0x5913e2 in cmsIT8LoadFromFile /root/lcms2/lcms2-asan/src/cmscgats.c:2349:13
    #6 0x4eb86b in main /root/lcms2/test.c:7:5
    #7 0x7f9a0b6b682f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)

SUMMARY: AddressSanitizer: heap-buffer-overflow /root/lcms2/lcms2-asan/src/cmscgats.c:1549:45 in SetData
Shadow bytes around the buggy address:
  0x0c547fff89f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c547fff8a00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c547fff8a10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c547fff8a20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c547fff8a30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c547fff8a40:[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c547fff8a50: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c547fff8a60: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c547fff8a70: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c547fff8a80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c547fff8a90: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==12907==ABORTING
```

**PATCH**
```
--- a/src/cmscgats.c
+++ b/src/cmscgats.c
@@ -1504,6 +1504,16 @@
     t-> nSamples   = atoi(cmsIT8GetProperty(it8, "NUMBER_OF_FIELDS"));
     t-> nPatches   = atoi(cmsIT8GetProperty(it8, "NUMBER_OF_SETS"));
 
+#if (UINT_MAX == 4294967295U)
+    const cmsUInt32Number UInt32Max = UINT_MAX;
+#elif (ULONG_MAX == 4294967295U)
+    const cmsUInt32Number UInt32Max = ULONG_MAX;
+#endif
+    if (((cmsUInt32Number) t->nSamples + 1) >  (UInt32Max / sizeof (char*)) / ((cmsUInt32Number) t->nPatches + 1)) {
+        SynError(it8, "AllocateDataSet: Unable to allocate data array");
+        return;
+    }
+
     t-> Data = (char**)AllocChunk (it8, ((cmsUInt32Number) t->nSamples + 1) * ((cmsUInt32Number) t->nPatches + 1) *sizeof (char*));
     if (t->Data == NULL) {
```

I have checked the lastest version of LCMS. The vulnerability still exists. 

https://github.com/mm2/Little-CMS/blob/master/src/cmscgats.c#L1509

## Attachments

- [AllocateDataSet.crash.IT8](attachments/AllocateDataSet.crash.IT8) (application/octet-stream, 16.3 KB)

## Timeline

### ji...@chromium.org (2018-08-08)

Thanks for reporting! 
Sounds like this vulnerability happens inside the lcms library. Could you report this issue directly to them?  
Chrome will patch their fixes once they fixed this problem upstream. 

Thanks! 

[Monorail components: Internals>Plugins>PDF]

### th...@chromium.org (2018-08-08)

Can |nSamples| and |nPatches| be set to UInt32Max? Those will also cause integer overflows. If |nPatches| overflows back to 0, your proposed patch will case a divide by 0 crash.

Don't forget to report https://crbug.com/chromium/864932 upstream as well.

### qu...@gmail.com (2018-08-08)

Oh! Thank thestig@! I forget to check this case.

### ts...@chromium.org (2018-08-28)

[Empty comment from Monorail migration]

### ts...@chromium.org (2018-08-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-29)

[Empty comment from Monorail migration]

### ts...@chromium.org (2018-08-29)

[Empty comment from Monorail migration]

### qu...@gmail.com (2018-08-30)

I created an issue in main project repository (https://github.com/mm2/Little-CMS/issues/171). The author of project has fixed it. Everything looks good :) 

https://github.com/mm2/Little-CMS/commit/768f70ca405cd3159d990e962d54456773bb8cf8

### th...@chromium.org (2018-08-30)

Great. I'll pull in the relevant bits from upstream.

### bu...@chromium.org (2018-08-30)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/81a3c2408a1fb3e3cc4b06d659cce19157ee0a91

commit 81a3c2408a1fb3e3cc4b06d659cce19157ee0a91
Author: Lei Zhang <thestig@chromium.org>
Date: Thu Aug 30 20:15:34 2018

Add check on CGATS memory allocation in littlecms.

This pull in the relevant bits from upstream commit 768f70ca.

BUG=chromium:872189

Change-Id: I6a970a00ff322768cddc2825e4b6e3e12400d43d
Reviewed-on: https://pdfium-review.googlesource.com/41671
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[modify] https://crrev.com/81a3c2408a1fb3e3cc4b06d659cce19157ee0a91/third_party/lcms/README.pdfium
[add] https://crrev.com/81a3c2408a1fb3e3cc4b06d659cce19157ee0a91/third_party/lcms/0032-cgats-allocation.patch
[modify] https://crrev.com/81a3c2408a1fb3e3cc4b06d659cce19157ee0a91/third_party/lcms/src/cmscgats.c


### th...@chromium.org (2018-08-30)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-08-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6486b858d8c49db25df193a817b808d4dcea1f75

commit 6486b858d8c49db25df193a817b808d4dcea1f75
Author: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Thu Aug 30 22:10:40 2018

Roll src/third_party/pdfium 678f5418d36f..b6e7d49ad5f3 (3 commits)

https://pdfium.googlesource.com/pdfium.git/+log/678f5418d36f..b6e7d49ad5f3


git log 678f5418d36f..b6e7d49ad5f3 --date=short --no-merges --format='%ad %ae %s'
2018-08-30 thestig@chromium.org Roll v8 to 19afaa14
2018-08-30 thestig@chromium.org Stop using deprecated V8 APIs in CFXJSE_Value.
2018-08-30 thestig@chromium.org Add check on CGATS memory allocation in littlecms.


Created with:
  gclient setdep -r src/third_party/pdfium@b6e7d49ad5f3

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:872189
TBR=dsinclair@chromium.org

Change-Id: I3b08c657e82321c78a6dee42ac3cf2801ecb2020
Reviewed-on: https://chromium-review.googlesource.com/1197290
Reviewed-by: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Commit-Queue: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#587804}
[modify] https://crrev.com/6486b858d8c49db25df193a817b808d4dcea1f75/DEPS


### sh...@chromium.org (2018-08-31)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### th...@chromium.org (2018-09-06)

awhalley: Shall we merge the fix to M69?

### aw...@chromium.org (2018-09-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-09-11)

Thanks for the report! The VRP panel decided to award $3,000 for the bug and $500 for helping with the patch. Cheers!

### qu...@gmail.com (2018-09-11)

I highly appreciate. Thanks a million. 

### aw...@chromium.org (2018-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-14)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), geohsu@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2018-09-14)

Lei - does this change need to be merged to 70?

### th...@chromium.org (2018-09-14)

Yes, we should. I will do this shortly.

### th...@chromium.org (2018-09-14)

It turns out I don't actually need to merge. I don't know why sheriffbot decided it was necessary. r587804 is in 70.0.3538.0, so it just barely beat the branch cut at r587811.

The real question is in https://crbug.com/chromium/872189#c15 - do we merge for M69?

### aw...@google.com (2018-10-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-12-07)

This issue was migrated from crbug.com/chromium/872189?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092129)*
