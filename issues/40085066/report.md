# Security: heap-buffer-overflow in SkColorSpace

| Field | Value |
|-------|-------|
| **Issue ID** | [40085066](https://issues.chromium.org/issues/40085066) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Reporter** | [Deleted User] |
| **Assignee** | ms...@chromium.org |
| **Created** | 2016-08-10 |
| **Bounty** | $3,500.00 |

## Description

**VULNERABILITY DETAILS**

There is a heap buffer overflow vulnerability in Skia.

This bug exists in the deserialisation routines for SkImageFilter, which can be triggered on the host process from a renderer through IPC.

## File src/core/SkColorSpace\_ICC.cpp, line 1005:

```
size_t allocSize = sizeof(SkGammas) + gamma_alloc_size(rType, rData)     <--- Integer Overflow (32bit builds only)  
                                    + gamma_alloc_size(gType, gData)  
                                    + gamma_alloc_size(bType, bData);  
void\* memory = sk_malloc_throw(allocSize);  
gammas = sk_sp<SkGammas>(new (memory) SkGammas());  

uint32_t offset = 0;  
gammas->fRedType = rType;  
offset += load_gammas(memory, offset, rType, &rData, rParams,  
                      r->addr(base));  

```

---

In my testcase, the function `gamma_alloc_size` will return 0x5555554C.

Therefore, `0x24+0x5555554C+0x5555554C+0x5555554C` will integer overflow.

`sk_malloc_throw` call will allocate a buffer too small.

## File src/core/SkColorSpace\_ICC.cpp, line 584:

static size\_t load\_gammas(void\* memory, size\_t offset, SkGammas::Type type,  

SkGammas::Data\* data, const SkGammas::Params& params,  

const uint8\_t\* src) {  

void\* storage = SkTAddOffset<void>(memory, offset + sizeof(SkGammas));

```
switch (type) {  
    ...  
    case SkGammas::Type::kTable_Type: {  
        data->fTable.fOffset = offset;  

        float\* outTable = (float\*) storage;  
        const uint16_t\* inTable = (const uint16_t\*) (src + 12);  
        for (int i = 0; i < data->fTable.fSize; i++) {  
            outTable[i] = (read_big_endian_u16((const uint8_t\*) &inTable[i])) / 65535.0f;  <--- out-of-bounds write with user-controlled input.  
        }  

        return sizeof(float) \* data->fTable.fSize;  
    }  

```

---

**VERSION**  

Chrome Version: 32-bit build of Chrome (All)  

Operating System: All

**REPRODUCTION CASE**  

Attached as `pocgen.py`

1. Download and Run python script for generating poc(poc.fil).
2. Use 32-bit build of filter\_fuzz\_stub to reproduce.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Attached as `asan_trace.log`, `windbg_trace.log`

(170c.20d0): Access violation - code c0000005 (!!! second chance !!!)  

\*\*\* WARNING: Unable to verify checksum for c:\G\chromium\src\out\Release\_x86\skia.dll  

eax=0000c141 ebx=0026f000 ecx=00004b51 edx=0069a2bc esi=00000008 edi=0040109b  

eip=10129712 esp=0019e498 ebp=0019e4ac iopl=0 nv up ei pl nz na po nc  

cs=0023 ss=002b ds=002b es=002b fs=0053 gs=002b efl=00010202  

skia!load\_gammas+0xa2:  

10129712 f30f11048a movss dword ptr [edx+ecx\*4],xmm0 ds:002b:006ad000=????????  

\*\*\* WARNING: Unable to verify checksum for c:\G\chromium\src\out\Release\_x86\filter\_fuzz\_stub.exe  

0:000> u  

skia!load\_gammas+0xa2 [c:\g\chromium\src\third\_party\skia\src\core\skcolorspace\_icc.cpp @ 600]:  

10129712 f30f11048a movss dword ptr [edx+ecx\*4],xmm0  

10129717 ebbe jmp skia!load\_gammas+0x67 (101296d7)  

10129719 8b4514 mov eax,dword ptr [ebp+14h]  

1012971c 8b4004 mov eax,dword ptr [eax+4]  

1012971f c1e002 shl eax,2  

10129722 eb65 jmp skia!load\_gammas+0x119 (10129789)  

10129724 8b4d14 mov ecx,dword ptr [ebp+14h]  

10129727 8b550c mov edx,dword ptr [ebp+0Ch]  

0:000> dd edx+ecx\*4-31  

006acfcf 4141c13f 4141c13f 4141c13f 4141c13f  

006acfdf 4141c13f 4141c13f 4141c13f 4141c13f  

006acfef 4141c13f 4141c13f 4141c13f 4141c13f  

006acfff ???????? ???????? ???????? ????????

## Attachments

- [pocgen.py](attachments/pocgen.py) (text/plain, 2.6 KB)
- [asan_trace.log](attachments/asan_trace.log) (text/plain, 4.7 KB)
- [windbg_trace.log](attachments/windbg_trace.log) (text/plain, 4.3 KB)
- [poc.png](attachments/poc.png) (image/png, 678.7 KB)
- [trace.log](attachments/trace.log) (text/plain, 3.9 KB)

## Timeline

### [Deleted User] (2016-08-10)

Suggested Patch: https://codereview.chromium.org/2230163002

### oc...@chromium.org (2016-08-10)

Thanks for the report. However, it looks like the PoC is 700MB, so I'm not sure if this can actually be sent via IPC from the renderer to the browser (maybe this has regressed with the move to Mojo). Tentatively assigning severity disregarding this fact.

msarett, are you the right person to take this? It looks like it was introduced in https://skia.googlesource.com/skia/+/1b93bd1e6eba3d14593490e4e24a34546638c8da



[Monorail components: Internals>Skia]

### ms...@chromium.org (2016-08-10)

Yes, I'm the right person.  Would be nice to have the test case, but I think the bug is clear.

### [Deleted User] (2016-08-11)

#2, Ok. I will check in detail this weekend.

### sh...@chromium.org (2016-08-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-11)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-08-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-08-14)

The following revision refers to this bug:
  https://skia.googlesource.com/skia.git/+/40ff5fe59b77b0b3e34467cc2f8666e4e88356f9

commit 40ff5fe59b77b0b3e34467cc2f8666e4e88356f9
Author: gogil <gogil@stealien.com>
Date: Sun Aug 14 09:12:40 2016

Prevent overflows when using gamma_alloc_size

BUG=636268
GOLD_TRYBOT_URL= https://gold.skia.org/search?issue=2230163002

Review-Url: https://codereview.chromium.org/2230163002

[modify] https://crrev.com/40ff5fe59b77b0b3e34467cc2f8666e4e88356f9/AUTHORS
[modify] https://crrev.com/40ff5fe59b77b0b3e34467cc2f8666e4e88356f9/src/core/SkColorSpace_ICC.cpp


### bu...@chromium.org (2016-08-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b2829e82cb128f78a045735ba9ec61fe698a66c6

commit b2829e82cb128f78a045735ba9ec61fe698a66c6
Author: skia-deps-roller <skia-deps-roller@chromium.org>
Date: Sun Aug 14 11:47:31 2016

Roll src/third_party/skia/ 1e4a389db..40ff5fe59 (1 commit).

https://chromium.googlesource.com/skia.git/+log/1e4a389dbf7e..40ff5fe59b77

$ git log 1e4a389db..40ff5fe59 --date=short --no-merges --format='%ad %ae %s'
2016-08-14 gogil Prevent overflows when using gamma_alloc_size

BUG=636268

CQ_INCLUDE_TRYBOTS=master.tryserver.blink:linux_precise_blink_rel
TBR=robertphillips@google.com

Review-Url: https://codereview.chromium.org/2244963002
Cr-Commit-Position: refs/heads/master@{#411916}

[modify] https://crrev.com/b2829e82cb128f78a045735ba9ec61fe698a66c6/DEPS


### [Deleted User] (2016-08-14)

I found the other way to reproduce.

SkColorSpace::NewICC can be called from different places.
https://skia.googlesource.com/skia/+/master/src/core/SkColorSpace.cpp#316
https://chromium.googlesource.com/chromium/src/+/master/third_party/WebKit/Source/platform/image-decoders/ImageDecoder.cpp#341
https://skia.googlesource.com/skia/+/master/src/codec/SkJpegCodec.cpp#232
https://skia.googlesource.com/skia/+/master/src/codec/SkPngCodec.cpp#261

There is no limit to the size of the image. (Actually, Image can be compressed.)
https://bugs.chromium.org/p/skia/issues/detail?id=3617

I attached a good testcase.
This bug can be reproduced using the DM.

### ms...@chromium.org (2016-08-14)

Thanks for this test case!

### bu...@chromium.org (2016-08-15)

The following revision refers to this bug:
  https://skia.googlesource.com/skia.git/+/bcae9d3d15d34a59d279c34e187e6101975500c0

commit bcae9d3d15d34a59d279c34e187e6101975500c0
Author: msarett <msarett@google.com>
Date: Mon Aug 15 16:41:59 2016

Add regression test

Original bug fix was in:
https://codereview.chromium.org/2230163002

BUG:636268
GOLD_TRYBOT_URL= https://gold.skia.org/search?issue=2243143002

Review-Url: https://codereview.chromium.org/2243143002

[add] https://crrev.com/bcae9d3d15d34a59d279c34e187e6101975500c0/resources/invalid_images/crbug636268.png
[modify] https://crrev.com/bcae9d3d15d34a59d279c34e187e6101975500c0/tests/ColorSpaceTest.cpp


### ms...@chromium.org (2016-08-15)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-08-16)

The following revision refers to this bug:
  https://skia.googlesource.com/skia.git/+/c5064d9c3d54816e441402c48c60325b6749bba2

commit c5064d9c3d54816e441402c48c60325b6749bba2
Author: msarett <msarett@google.com>
Date: Tue Aug 16 11:54:19 2016

Revert of Add regression test (patchset #2 id:20001 of https://codereview.chromium.org/2243143002/ )

Reason for revert:
Nexus 9 and Nexus Player failures.

Original issue's description:
> Add regression test
>
> Original bug fix was in:
> https://codereview.chromium.org/2230163002
>
> BUG:636268
> GOLD_TRYBOT_URL= https://gold.skia.org/search?issue=2243143002
>
> Committed: https://skia.googlesource.com/skia/+/bcae9d3d15d34a59d279c34e187e6101975500c0

TBR=reed@google.com,gogil@stealien.com
# Skipping CQ checks because original CL landed less than 1 days ago.
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true

Review-Url: https://codereview.chromium.org/2243403003

[delete] https://crrev.com/36c38cbb29744e0b5390a38367e47c0c74287c2d/resources/invalid_images/crbug636268.png
[modify] https://crrev.com/c5064d9c3d54816e441402c48c60325b6749bba2/tests/ColorSpaceTest.cpp


### sh...@chromium.org (2016-08-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-23)

The panel awarded $3,500 for this bug.  Cheers!

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### is...@google.com (2018-01-22)

This issue was migrated from crbug.com/chromium/636268?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085066)*
