# Security: Little-CMS (lcms) Heap Buffer Overflow

| Field | Value |
|-------|-------|
| **Issue ID** | [40091957](https://issues.chromium.org/issues/40091957) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | qu...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2018-07-18 |
| **Bounty** | $2,500.00 |

## Description

**VULNERABILITY DETAILS**
 
 Little-CMS third-party library is used in PDFium to support ICC profile. I have audited source code of lcms library and I have founded a vulnerability in cmsReadTag function. The attached icc profile could crash lcms when ASAN was enabled on Linux.
 
 ```
 =================================================================
==37311==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x606000000058 at pc 0x00000053bc7b bp 0x7ffcd1988bd0 sp 0x7ffcd1988bc8
READ of size 8 at 0x606000000058 thread T0
    #0 0x53bc7a in Type_S15Fixed16_Write /root/fuzzer/lcms2/Little-CMS/src/cmstypes.c:558:43
    #1 0x4f9769 in cmsReadRawTag /root/fuzzer/lcms2/Little-CMS/src/cmsio0.c:1873:10
    #2 0x4eae5b in ReadAllRAWTags /root/fuzzer/lcms2/Little-CMS/fuzz/fuzz.c:23:9
    #3 0x4eaf05 in main /root/fuzzer/lcms2/Little-CMS/fuzz/fuzz.c:31:4
    #4 0x7f5d4f0c082f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)
    #5 0x41aa78 in _start (/root/fuzzer/lcms2/Little-CMS/fuzz/fuzz+0x41aa78)

0x606000000058 is located 0 bytes to the right of 56-byte region [0x606000000020,0x606000000058)
allocated by thread T0 here:
    #0 0x4bb1a3 in __interceptor_malloc /tmp/final/llvm.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cc:88:3
    #1 0x57fac4 in FXMEM_DefaultAlloc /root/fuzzer/lcms2/Little-CMS/src/cmserr.c:33:9
    #2 0x57fe18 in _cmsMallocZero /root/fuzzer/lcms2/Little-CMS/src/cmserr.c:97:15
    #3 0x57feb9 in _cmsCalloc /root/fuzzer/lcms2/Little-CMS/src/cmserr.c:109:12
    #4 0x53bae0 in Type_S15Fixed16_Read /root/fuzzer/lcms2/Little-CMS/src/cmstypes.c:534:40
    #5 0x4f65d3 in cmsReadTag /root/fuzzer/lcms2/Little-CMS/src/cmsio0.c:1597:25
    #6 0x4eadc5 in ReadAllTags /root/fuzzer/lcms2/Little-CMS/fuzz/fuzz.c:11:13
    #7 0x4eaefc in main /root/fuzzer/lcms2/Little-CMS/fuzz/fuzz.c:30:4
    #8 0x7f5d4f0c082f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)

SUMMARY: AddressSanitizer: heap-buffer-overflow /root/fuzzer/lcms2/Little-CMS/src/cmstypes.c:558:43 in Type_S15Fixed16_Write
Shadow bytes around the buggy address:
  0x0c0c7fff7fb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c0c7fff7fc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c0c7fff7fd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c0c7fff7fe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c0c7fff7ff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c0c7fff8000: fa fa fa fa 00 00 00 00 00 00 00[fa]fa fa fa fa
  0x0c0c7fff8010: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c0c7fff8020: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c0c7fff8030: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c0c7fff8040: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c0c7fff8050: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==37311==ABORTING
```

**VERSION**

Chrome Version: All

Operating System: All

Following code will trigger crash

```
#include <stdio.h>
#include <lcms2.h>

void ReadAllTags(cmsHPROFILE h) {
    cmsInt32Number i, n;
    cmsTagSignature sig;

    n = cmsGetTagCount(h);
    for (i=0; i < n; i++) {
        sig = cmsGetTagSignature(h, i);
        if (cmsReadTag(h, sig) == NULL) return;
    }
}

// Read all tags on a profile given by its handle
void ReadAllRAWTags(cmsHPROFILE h) {
    cmsInt32Number i, n;
    cmsTagSignature sig;

    n = cmsGetTagCount(h);
    for (i=0; i < n; i++) {
        sig = cmsGetTagSignature(h, i);
        cmsReadRawTag(h, sig, NULL, 0);
    }
}

int main(int argc, char* argv[]) {
   cmsHPROFILE h = cmsOpenProfileFromFile(argv[1], "rb");
   if (h == NULL) return 1;
   ReadAllTags(h);
   ReadAllRAWTags(h);
   cmsCloseProfile(h);
   return 0;
}
```
 
 
**ANALYSIS**

There are many tag types which are supported in lcms: https://cs.chromium.org/chromium/src/third_party/pdfium/third_party/lcms/src/cmstypes.c?type=cs&l=5418


```
// This is the list of built-in tags
static _cmsTagLinkedList SupportedTags[] = {
   //  .....
    { cmsSigChromaticAdaptationTag, { 9, 1, { cmsSigS15Fixed16ArrayType }, NULL}, &SupportedTags[15]},
   //  .....
};
```

Each type has `ElemCount`: https://cs.chromium.org/chromium/src/third_party/pdfium/third_party/lcms/include/lcms2_plugin.h?type=cs&g=0&l=425

```
// This is the tag plugin, which identifies tags. For writing, a pointer to function is provided.
// This function should return the desired type for this tag, given the version of profile
// and the data being serialized.
typedef struct {

    cmsUInt32Number     ElemCount;          // If this tag needs an array, how many elements should keep

    // For reading.
    cmsUInt32Number     nSupportedTypes;    // In how many types this tag can come (MAX_TYPES_IN_LCMS_PLUGIN maximum)
    cmsTagTypeSignature SupportedTypes[MAX_TYPES_IN_LCMS_PLUGIN];

    // For writting
    cmsTagTypeSignature (* DecideType)(cmsFloat64Number ICCVersion, const void *Data);

} cmsTagDescriptor;
```

Let's see cmsReadTag: https://cs.chromium.org/chromium/src/third_party/pdfium/third_party/lcms/src/cmsio0.c?l=1519

The number of elements, which is calculated from data, may be less than `ElemCount`: https://cs.chromium.org/chromium/src/third_party/pdfium/third_party/lcms/src/cmsio0.c?l=1612
```
// This is a weird error that may be a symptom of something more serious, the number of
    // stored item is actually less than the number of required elements.
    if (ElemCount < TagDescriptor ->ElemCount) {

        char String[5];

        _cmsTagSignature2String(String, sig);
        cmsSignalError(Icc ->ContextID, cmsERROR_CORRUPTION_DETECTED, "'%s' Inconsistent number of items: expected %d, got %d",
            String, TagDescriptor ->ElemCount, ElemCount);
    }
```
if ElemCount is less than TagDescriptor ->ElemCount, it is a malformed tag and it MUST be ignored.


## Attachments

- [crash-cmsReadTag_min](attachments/crash-cmsReadTag_min) (text/plain, 180 B)

## Timeline

### qu...@gmail.com (2018-07-18)

Patch for this issue: 
```
diff --git a/third_party/lcms/src/cmsio0.c b/third_party/lcms/src/cmsio0.c
index cc5f89064..63e4105d1 100644
--- a/third_party/lcms/src/cmsio0.c
+++ b/third_party/lcms/src/cmsio0.c
@@ -1616,6 +1616,7 @@ void* CMSEXPORT cmsReadTag(cmsHPROFILE hProfile, cmsTagSignature sig)
         _cmsTagSignature2String(String, sig);
         cmsSignalError(Icc ->ContextID, cmsERROR_CORRUPTION_DETECTED, "'%s' Inconsistent number of items: expected %d, got %d",
             String, TagDescriptor ->ElemCount, ElemCount);
+               goto Error;
     }


```

### ct...@chromium.org (2018-07-18)

Thank you for the detailed writeup and for including a patch :-)

Setting some labels. If I understand correctly, this is a limited out-of-bounds write, so applying Sev-Medium.

thestig@ Could you take a look? You had the most recent patch to lcms/.

[Monorail components: Internals>Plugins>PDF]

### th...@chromium.org (2018-07-18)

[Empty comment from Monorail migration]

### th...@chromium.org (2018-07-18)

Yes, it looks like cmsReadTag() is missing the goto statement to handle the error. We'll patch it up. Have you reported the issue upstream to lcms?

### th...@chromium.org (2018-07-18)

https://pdfium-review.googlesource.com/c/pdfium/+/38270

### bu...@chromium.org (2018-07-18)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/649815d0d6e57f3a551e73ae464589b0dedf913d

commit 649815d0d6e57f3a551e73ae464589b0dedf913d
Author: Lei Zhang <thestig@chromium.org>
Date: Wed Jul 18 20:27:59 2018

Handle wrong tag element count in littlecms.

BUG=chromium:864932

Change-Id: I7e87ba6e0fc6e2bdefcee29cbc0b60cb9ec9e316
Reviewed-on: https://pdfium-review.googlesource.com/38270
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[modify] https://crrev.com/649815d0d6e57f3a551e73ae464589b0dedf913d/third_party/lcms/README.pdfium
[add] https://crrev.com/649815d0d6e57f3a551e73ae464589b0dedf913d/third_party/lcms/0031-wrong-tag-element-count.patch
[modify] https://crrev.com/649815d0d6e57f3a551e73ae464589b0dedf913d/third_party/lcms/src/cmsio0.c


### th...@chromium.org (2018-07-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-18)

This bug requires manual review: We are only 5 days from stable.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), kariahda@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2018-07-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/30ce134f3d94e8addd51f007a468af9ac626af9f

commit 30ce134f3d94e8addd51f007a468af9ac626af9f
Author: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Thu Jul 19 02:04:36 2018

Roll src/third_party/pdfium f22b4e2f6682..c15c0b3a1e9a (3 commits)

https://pdfium.googlesource.com/pdfium.git/+log/f22b4e2f6682..c15c0b3a1e9a


git log f22b4e2f6682..c15c0b3a1e9a --date=short --no-merges --format='%ad %ae %s'
2018-07-18 thestig@chromium.org Roll third_party/skia/ af7700265..588f87967 (1391 commits; 41 trivial rolls)
2018-07-18 thestig@chromium.org Handle wrong tag element count in littlecms.
2018-07-18 tsepez@chromium.org Add pdfium::span::as_bytes() and as_writable_bytes().


Created with:
  gclient setdep -r src/third_party/pdfium@c15c0b3a1e9a

The AutoRoll server is located here: https://pdfium-roll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:864932
TBR=dsinclair@chromium.org

Change-Id: If7555664cbb89a71e68d034eacbb6b6be0e87415
Reviewed-on: https://chromium-review.googlesource.com/1142172
Reviewed-by: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Commit-Queue: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#576322}
[modify] https://crrev.com/30ce134f3d94e8addd51f007a468af9ac626af9f/DEPS


### qu...@gmail.com (2018-07-19)

Thank you for reviewing the issue. Do you reward for this report?

### th...@chromium.org (2018-07-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-19)

[Empty comment from Monorail migration]

### aw...@google.com (2018-07-19)

quangnh89@, this will go to a future meetings of the VRP panel, we'll see what they say.

### ab...@google.com (2018-07-19)

My recommendation is to target this for M69, since M68 stable is next week. Rejecting merge for M68. Awhalley@/thestig@ - please confirm if this is absolutely critical. 

### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### wf...@chromium.org (2018-08-01)

lcms v2.9 seems to be out [1], and we are on 2.8 [2] - is it worth updating?

[1] https://github.com/mm2/Little-CMS/blob/master/ChangeLog
[2] https://cs.chromium.org/chromium/src/third_party/pdfium/third_party/lcms/README.pdfium

### th...@chromium.org (2018-08-01)

wfh: Thanks for pointing that out. https://bugs.chromium.org/p/pdfium/issues/detail?id=1128

### qu...@gmail.com (2018-08-02)

I have checked lcms v2.9. The vulnerability still exists.
If you update lcms, please patch it :)

https://github.com/mm2/Little-CMS/blob/master/src/cmsio0.c#L1601

### th...@chromium.org (2018-08-02)

Thanks for mention that. When we upgrade a third party library, we usually re-evaluate all the patches to see which ones are still relevant.

### aw...@chromium.org (2018-08-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-08-06)

Thanks for the report, quangnh89@! The VRP panel decided to award $2,000 for the report, and $500 for supplying the patch we used. They also noted that they'd be open to considering a higher amount if you could show how this might lead to memory corruption rather than just being an information leak.  Cheers!  A member of our finance team will be in touch to arrange for payment.

### aw...@chromium.org (2018-08-06)

[Empty comment from Monorail migration]

### qu...@gmail.com (2018-08-07)

Thank you so much for the reward! That means so much to me! Your thoughtfulness encourage me to do my best. :) Have a nice day!

### aw...@google.com (2018-08-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### st...@gmail.com (2018-10-26)

Hello, can you tell me how to reproduce this issue under pdfium? Thanks.

### is...@google.com (2018-10-26)

This issue was migrated from crbug.com/chromium/864932?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091957)*
