# Security: PDFium Heap Buffer Overflow Vulnerability in OpenJPEG

| Field | Value |
|-------|-------|
| **Issue ID** | [40088936](https://issues.chromium.org/issues/40088936) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | pa...@chromium.org |
| **Created** | 2017-09-06 |
| **Bounty** | $6,337.00 |

## Description

VULNERABILITY DETAILS
Let's create this issue first. I'll post the details later.

WinDbg information:

(5984.5fb8): Break instruction exception - code 80000003 (!!! second chance !!!)
eax=00000000 ebx=00000000 ecx=5d2f8598 edx=00000000 esi=00170000 edi=00170000
eip=5d2cba58 esp=003ebd68 ebp=003ebd84 iopl=0         nv up ei pl zr na pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00000246
verifier!VerifierStopMessage+0x1f8:
5d2cba58 cc              int     3

0:000> k
ChildEBP RetAddr  
003ebd84 5d2c9e69 verifier!VerifierStopMessage+0x1f8
003ebde8 5d2ca22a verifier!AVrfpDphReportCorruptedBlock+0x239
003ebe44 5d2ca742 verifier!AVrfpDphCheckNormalHeapBlock+0x11a
003ebe64 5d2c90d3 verifier!AVrfpDphNormalHeapFree+0x22
003ebe88 7741170c verifier!AVrfDebugPageHeapFree+0xe3
003ebed0 773ca863 ntdll!RtlDebugFreeHeap+0x2f
003ebfc4 77372bd5 ntdll!RtlpFreeHeap+0x5d
003ebfe4 76c114ad ntdll!RtlFreeHeap+0x142
003ebff8 014922bc kernel32!HeapFree+0x14
003ec00c 01484f83 pdfium_test!_free_base+0x1c [minkernel\crts\ucrt\src\appcrt\heap\free_base.cpp @ 112]
003ec01c 013764d3 pdfium_test!free+0x18 [minkernel\crts\ucrt\src\appcrt\heap\free.cpp @ 30]
(Inline) -------- pdfium_test!`anonymous namespace'::sycc422_to_rgb+0x3a3 [E:\PDFiumDev\repo\pdfium\core\fxcodec\codec\fx_codec_jpx_opj.cpp @ 161]
(Inline) -------- pdfium_test!`anonymous namespace'::color_sycc_to_rgb+0x6d6 [E:\PDFiumDev\repo\pdfium\core\fxcodec\codec\fx_codec_jpx_opj.cpp @ 207]
003ee0d8 013768ef pdfium_test!CJPX_Decoder::Init+0x94b [E:\PDFiumDev\repo\pdfium\core\fxcodec\codec\fx_codec_jpx_opj.cpp @ 526]
003ee0f4 0131dc66 pdfium_test!CCodec_JpxModule::CreateDecoder+0x33 [E:\PDFiumDev\repo\pdfium\core\fxcodec\codec\fx_codec_jpx_opj.cpp @ 622]
003ee154 0131c984 pdfium_test!CPDF_DIBSource::LoadJpxBitmap+0x74 [E:\PDFiumDev\repo\pdfium\core\fpdfapi\render\cpdf_dibsource.cpp @ 634]
003ee188 0131d325 pdfium_test!CPDF_DIBSource::CreateDecoder+0x58 [E:\PDFiumDev\repo\pdfium\core\fpdfapi\render\cpdf_dibsource.cpp @ 511]
003ee1b8 0133bfa3 pdfium_test!CPDF_DIBSource::StartLoadDIBSource+0x197 [E:\PDFiumDev\repo\pdfium\core\fpdfapi\render\cpdf_dibsource.cpp @ 289]
003ee1ec 013288e2 pdfium_test!CPDF_ImageCacheEntry::StartGetCachedBitmap+0xdf [E:\PDFiumDev\repo\pdfium\core\fpdfapi\render\cpdf_imagecacheentry.cpp @ 71]
003ee228 0134d538 pdfium_test!CPDF_PageRenderCache::StartGetCachedBitmap+0x74 [E:\PDFiumDev\repo\pdfium\core\fpdfapi\render\cpdf_pagerendercache.cpp @ 97]
003ee25c 01340fef pdfium_test!CPDF_ImageLoader::Start+0x4e [E:\PDFiumDev\repo\pdfium\core\fpdfapi\render\cpdf_imageloader.cpp @ 34]
003ee2ac 01342365 pdfium_test!CPDF_ImageRenderer::StartLoadDIBSource+0x67 [E:\PDFiumDev\repo\pdfium\core\fpdfapi\render\cpdf_imagerenderer.cpp @ 62]
003ee2c0 0132b1ac pdfium_test!CPDF_ImageRenderer::Start+0x93 [E:\PDFiumDev\repo\pdfium\core\fpdfapi\render\cpdf_imagerenderer.cpp @ 181]
003ee2f0 01310700 pdfium_test!CPDF_RenderStatus::ContinueSingleObject+0xce [E:\PDFiumDev\repo\pdfium\core\fpdfapi\render\cpdf_renderstatus.cpp @ 1132]
003ee368 012def29 pdfium_test!CPDF_ProgressiveRenderer::Continue+0x286 [E:\PDFiumDev\repo\pdfium\core\fpdfapi\render\cpdf_progressiverenderer.cpp @ 93]
003ee38c 012dec18 pdfium_test!`anonymous namespace'::RenderPageImpl+0x1bb [E:\PDFiumDev\repo\pdfium\fpdfsdk\fpdfview.cpp @ 129]
003ee3e0 012e168f pdfium_test!FPDF_RenderPage_Retail+0x64 [E:\PDFiumDev\repo\pdfium\fpdfsdk\fpdfview.cpp @ 1248]
003ee434 012d848b pdfium_test!FPDF_RenderPageBitmap_Start+0x107 [E:\PDFiumDev\repo\pdfium\fpdfsdk\fpdf_progressive.cpp @ 60]
003ee70c 012d1fdf pdfium_test!`anonymous namespace'::RenderPage+0xa86 [E:\PDFiumDev\repo\pdfium\samples\pdfium_test.cc @ 1273]
(Inline) -------- pdfium_test!`anonymous namespace'::RenderPdf+0x6a1 [E:\PDFiumDev\repo\pdfium\samples\pdfium_test.cc @ 1469]
003ef9d8 0147e05b pdfium_test!main+0xfdf [E:\PDFiumDev\repo\pdfium\samples\pdfium_test.cc @ 1630]
(Inline) -------- pdfium_test!invoke_main+0x1d [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 64]
003efa20 76c1336a pdfium_test!__scrt_common_main_seh+0xf9 [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 253]
003efa2c 77379902 kernel32!BaseThreadInitThunk+0xe
003efa6c 773798d5 ntdll!__RtlUserThreadStart+0x70
003efa84 00000000 ntdll!_RtlUserThreadStart+0x1b

VERSION
Chrome Version: [x.x.x.x] + [stable, beta, or dev]
Operating System: [Please indicate OS, version, and service pack level]

REPRODUCTION CASE
Please include a demonstration of the security bug, such as an attached
HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE
make the file as small as possible and remove any content not required to
demonstrate the bug.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [tab, browser, etc.]
Crash State: [see link above: stack trace, registers, exception record]
Client ID (if relevant): [see link above]


## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 1.2 KB)
- [762374.patch](attachments/762374.patch) (application/octet-stream, 5.4 KB)

## Timeline

### st...@gmail.com (2017-09-06)

This issue was caused by the updated version of OpenJPEG. Root cause analysis:

--------------------------------------
(1) opj_alloc_tile_component_data
--------------------------------------
``opj_malloc`` was replaced with ``opj_image_data_alloc`` in function ``opj_alloc_tile_component_data``.

OPJ_BOOL opj_alloc_tile_component_data(opj_tcd_tilecomp_t *l_tilec)
{
    if ((l_tilec->data == 00) ||
            ((l_tilec->data_size_needed > l_tilec->data_size) &&
             (l_tilec->ownsData == OPJ_FALSE))) {
        l_tilec->data = (OPJ_INT32 *) opj_image_data_alloc(l_tilec->data_size_needed);      // --> diff
        if (! l_tilec->data) {
            return OPJ_FALSE;
        }
        /*fprintf(stderr, "tAllocate data of tilec (int): %d x OPJ_UINT32n",l_data_size);*/
        l_tilec->data_size = l_tilec->data_size_needed;
        l_tilec->ownsData = OPJ_TRUE;
    } else if (l_tilec->data_size_needed > l_tilec->data_size) {
        // skipped...
    }
    return OPJ_TRUE;
}

--------------------------------------
(2) opj_image_data_alloc
--------------------------------------
``opj_image_data_alloc`` was implemented by ``opj_aligned_malloc``.

void* OPJ_CALLCONV opj_image_data_alloc(OPJ_SIZE_T size)
{
    void* ret = opj_aligned_malloc(size);
    /* printf("opj_image_data_alloc %p\n", ret); */
    return ret;
}

--------------------------------------
(3) opj_aligned_malloc
--------------------------------------
The actual implementation of function ``opj_aligned_malloc`` depends on environments. The details can be found in file ``opj_malloc.h``.


--------------------------------------
(4) opj_free
--------------------------------------
However, ``opj_free`` never points to ``opj_aligned_free``. Thus, if ``opj_image_data_alloc`` doesn't point to ``opj_malloc`` but ``opj_free`` points to ``free``, the mismatch could crash the process.

void sycc422_to_rgb(opj_image_t* img) {
  // skipped...
  opj_free(img->comps[0].data);
  opj_free(img->comps[1].data);
  opj_free(img->comps[2].data);
  // skipped...
}

### st...@gmail.com (2017-09-06)

``opj_image_data_alloc`` should be paired with ``opj_image_data_free``.
(extracted from openjpeg.h)

/**
 * Allocator for opj_image_t->comps[].data
 * To be paired with opj_image_data_free.
 *
 * @param   size    number of bytes to allocate
 *
 * @return  a new pointer if successful, NULL otherwise.
 * @since 2.2.0
*/
OPJ_API void* OPJ_CALLCONV opj_image_data_alloc(OPJ_SIZE_T size);

/**
 * Destructor for opj_image_t->comps[].data
 * To be paired with opj_image_data_alloc.
 *
 * @param   ptr    Pointer to free
 *
 * @since 2.2.0
*/
OPJ_API void OPJ_CALLCONV opj_image_data_free(void* ptr);


### st...@gmail.com (2017-09-06)

Here the issue exists in fx_codec_jpx_opj.cpp.
The same issue can be found in OpenJPEG's image.c and jp2.c.

To keep the compatibility with OpenJPEG's new API, we should use ``opj_image_data_free`` for all ``opj_image_t->comps[].data``.

I uploaded a patch to address this issue.

### el...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### cl...@chromium.org (2017-09-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4953980643049472.

### ts...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### ts...@chromium.org (2017-09-06)

(There probably needs to be an upstream bug as well).

### st...@gmail.com (2017-09-07)

#5 ClusterFuzz may not be able to reproduce this issue since the behavior of ``opj_aligned_malloc`` depends on concrete environment. I can reproduce it on Windows.

#7 I'll report it to upstream.

### pa...@chromium.org (2017-09-07)

How would you like to be credited in the git commit log entry?

### pa...@chromium.org (2017-09-07)

I can't seem to reproduce the bug on Chrome 60 on Windows, or with pdfium_test or Chrome, tip-of-tree, on Linux, with or without ASan.

How are you reproducing it?

### pa...@chromium.org (2017-09-07)

[Empty comment from Monorail migration]

### st...@gmail.com (2017-09-08)

Hi palmer, the issue was introduced by commit https://pdfium.googlesource.com/pdfium/+/088ca03f25fe1f6d75c0ff3b71e0ad3d018a5e0c

My environments:
OS: Windows 7 x64
Compiler: VS 2015
pdfium_test: x86 version (Release)
PageHeap: enabled within gflags.exe

----------------------
args.gn for ninja
----------------------
use_goma = false
pdf_use_skia = false
pdf_enable_xfa = false
pdf_enable_v8 = false
pdf_is_standalone = true
is_debug = false
target_cpu = "x86"
treat_warnings_as_errors = false

I can confirm that page heap must be enabled to reproduce this issue.

### st...@gmail.com (2017-09-08)

#9 You can credit to Ke Liu of Tencent's Xuanwu Lab if my patch works fine. Thank you.

### st...@gmail.com (2017-09-08)

There's a similar issue that has been fixed in OpenJPEG, the commit record is https://github.com/uclouvain/openjpeg/commit/61fb5dd7f81c2e3dfabbb99f59dc89572d59fa37

Also, I reported this issue to upstream at https://github.com/uclouvain/openjpeg/issues/1014

Pull request: https://github.com/uclouvain/openjpeg/pull/1016

### st...@gmail.com (2017-09-08)

[Comment Deleted]

### st...@gmail.com (2017-09-08)

Hi, my patch has been adopted by upstream. You can find it at https://github.com/uclouvain/openjpeg/commit/b73ce715d2a484d7355639d863d0418a0e5b8858

### pa...@chromium.org (2017-09-08)

I've got the patch up for review now at https://pdfium-review.googlesource.com/13610

### pa...@chromium.org (2017-09-08)

[Empty comment from Monorail migration]

### th...@chromium.org (2017-09-08)

Isn't this M-63 since M-62 is branch 3202 and it branched at r499098? Whereas the OpenJPEG update happened after PDFium branch origin/chromium/3204, and didn't get rolled into Chromium until r499763.

### pa...@chromium.org (2017-09-09)

[Empty comment from Monorail migration]

### pa...@chromium.org (2017-09-11)

Note: https://github.com/uclouvain/openjpeg/commit/b73ce715d2a484d7355639d863d0418a0e5b8858 only patches 1 location in jp2.c, while https://pdfium-review.googlesource.com/13610 (Ke's patch) patches 2 locations in jp2.c.  Do we know why this discrepancy exists?

### bu...@chromium.org (2017-09-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/55dc1f8189d76c7ed7d9d3878c22c08e300669e3

commit 55dc1f8189d76c7ed7d9d3878c22c08e300669e3
Author: pdfium-deps-roller@chromium.org <pdfium-deps-roller@chromium.org>
Date: Mon Sep 11 21:02:51 2017

Roll src/third_party/pdfium/ 131c0eb2e..56ec0818c (1 commit)

https://pdfium.googlesource.com/pdfium.git/+log/131c0eb2e34e..56ec0818c3ed

$ git log 131c0eb2e..56ec0818c --date=short --no-merges --format='%ad %ae %s'
2017-09-11 palmer Use the right allocate and free functions in OpenJPEG.

Created with:
  roll-dep src/third_party/pdfium
BUG=762374


Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, see:
http://www.chromium.org/developers/tree-sheriffs/sheriff-details-chromium#TOC-Failures-due-to-DEPS-rolls


TBR=dsinclair@chromium.org

Change-Id: Id0d43903dbc84611c3aaae9e28ca65896cf40de0
Reviewed-on: https://chromium-review.googlesource.com/660679
Reviewed-by: <pdfium-deps-roller@chromium.org>
Commit-Queue: <pdfium-deps-roller@chromium.org>
Cr-Commit-Position: refs/heads/master@{#501040}
[modify] https://crrev.com/55dc1f8189d76c7ed7d9d3878c22c08e300669e3/DEPS


### pa...@chromium.org (2017-09-11)

[Empty comment from Monorail migration]

### aw...@google.com (2017-09-11)

[Empty comment from Monorail migration]

### st...@gmail.com (2017-09-12)

#21 Hi palmer, the discrepancy was introduced by https://pdfium.googlesource.com/pdfium/+/c37d7d452d6a37c997c8709576dd71406ecff618

In 0022-jp2_apply_pclr_overflow.patch, we use ``if`` statements to check whether ``src`` or ``dst`` point to null, the previously allocated data will be freed immediately once null pointer detected. Thus, we introduced ``opj_free(new_comps[j].data)`` here.

In OpenJPEG, ``assert`` was used instead of ``if``, which could lead to null pointer access in Release version.

That's why we patched 2 locations in jp2.c but OpenJPEG only patched 1.

### sh...@chromium.org (2017-09-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-09-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-09-18)

Nice one stackexploit@! The VRP panel awarded $5,000 and a $1,337 bonus for this bug.

### aw...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-27)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), gkihumba@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-10-27)

+awhalley@ (Security TPM) for M63 merge review

### aw...@chromium.org (2017-10-30)

No M63 merge needed.

### aw...@google.com (2017-12-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-12-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-05)

This issue was migrated from crbug.com/chromium/762374?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### dx...@google.com (2026-05-05)

Project: pdfium  

Branch:  main  

Author:  Nico Weber [thakis@chromium.org](mailto:thakis@chromium.org)  

Link:    <https://pdfium-review.googlesource.com/147090>

Fold 0035-opj\_image\_data\_free.patch into 0022-jp2\_apply\_pclr\_overflow.patch

---


Expand for full commit details
```
     
    Most of the original 0035-opj_image_data_free.patch was upstreamed in 
    https://github.com/uclouvain/openjpeg/commit/b73ce715. One line wasn't, 
    because that line was added downstream in 
    0022-jp2_apply_pclr_overflow.patch. 
     
    Instead of having one patch add a wrong line and then fixing it up in a 
    second patch, get it right in the first patch. See also comment 26 on 
    the linked bug. 
     
    While here, also update README.pdfium to note that 
    0047-opj_j2k_read_sod.patch is a cherry-pick from upstream. 
     
    No behavior change. 
     
    Bug: chromium:40088936 
    Change-Id: I9ec49ef36bd6e4d4c9b8bac7d6a751249618d91d 
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/147090 
    Reviewed-by: Nico Weber <thakis@google.com> 
    Commit-Queue: Nico Weber <thakis@chromium.org> 
    Reviewed-by: Lei Zhang <thestig@chromium.org>

```

---

Files:

- M `third_party/libopenjpeg/0022-jp2_apply_pclr_overflow.patch`
- D `third_party/libopenjpeg/0035-opj_image_data_free.patch`
- M `third_party/libopenjpeg/README.pdfium`

---

Hash: 374edcd2b743d2fa26a680b0933077690ecfdf8c  

Date: Tue May 5 18:32:05 2026


---

### dx...@google.com (2026-05-06)

Project: chromium/src  

Branch:  main  

Author:  [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com) [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7819543>

Roll PDFium from 11b7e080a790 to 096d774ab6b1 (3 revisions)

---


Expand for full commit details
```
     
    https://pdfium.googlesource.com/pdfium.git/+log/11b7e080a790..096d774ab6b1 
     
    2026-05-05 thakis@chromium.org Cherry-pick openjpeg changes to speed up jpeg2000 decoding on arm 
    2026-05-05 thakis@chromium.org Fold 0035-opj_image_data_free.patch into 0022-jp2_apply_pclr_overflow.patch 
    2026-05-05 helmut@januschka.com Persist FPDFPage_InsertObjectAtIndex() ordering on save 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/pdfium-autoroll 
    Please CC andyphan@google.com,dhoss@chromium.org,thestig@chromium.org on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in PDFium: https://bugs.chromium.org/p/pdfium/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Bug: chromium:40088936,chromium:507508112 
    Tbr: andyphan@google.com 
    Change-Id: I81c5253fc2284573ddd746d56610ee02ac2d2d09 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7819543 
    Bot-Commit: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1626029}

```

---

Files:

- M `DEPS`
- M `third_party/pdfium`

---

Hash: [cd0c8fb0f5c748ce2fb6464b2d7df14a5cf4c8e4](https://chromiumdash.appspot.com/commit/cd0c8fb0f5c748ce2fb6464b2d7df14a5cf4c8e4)  

Date: Wed May 6 10:26:40 2026


---

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088936)*
