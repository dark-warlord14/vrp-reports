# Security: PDFium calls PartitionFree() on heap memory returned by opj_calloc()

| Field | Value |
|-------|-------|
| **Issue ID** | [40088629](https://issues.chromium.org/issues/40088629) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | oc...@chromium.org |
| **Created** | 2017-08-07 |
| **Bounty** | $3,500.00 |

## Description

VULNERABILITY DETAILS
This issue looks like the same as https://crbug.com/chromium/737033 which was addressed in https://pdfium.googlesource.com/pdfium/+/c2a68df83faee582f0d6741f05116505b72b9d5d%5E%21/#F0

In function sycc422_to_rgb of file fx_codec_jpx_opj, we try to use FX_Free to free heap memory which was allocated by fucntion opj_calloc. Here FX_Free redirects to pdfium::base::PartitionFree and opj_calloc redirects to calloc.

static void sycc422_to_rgb(opj_image_t* img) {
  // skipped...
  
  FX_Free(img->comps[0].data);      // --> pdfium::base::PartitionFree
  img->comps[0].data = d0;
  FX_Free(img->comps[1].data);      // --> pdfium::base::PartitionFree
  img->comps[1].data = d1;
  FX_Free(img->comps[2].data);      // --> pdfium::base::PartitionFree
  img->comps[2].data = d2;
  
  // skipped...
}

------------------
Debugging Logs
------------------
(2804.e60): Access violation - code c0000005 (!!! second chance !!!)
eax=08200000 ebx=082beff0 ecx=082d9000 edx=ffe00000 esi=082015e0 edi=0000002f
eip=003de3e5 esp=0029d220 ebp=0029d234 iopl=0         nv up ei pl nz na po nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010202
pdfium_test_exe!FX_Free+0x51:
003de3e5 0fb74610        movzx   eax,word ptr [esi+10h] ds:002b:082015f0=????

0:000> !heap -p -a esi+10
    address 082015f0 found in
    _DPH_HEAP_ROOT @ 2a1000
    in busy allocation (  DPH_HEAP_BLOCK:         UserAddr         UserSize -         VirtAddr         VirtSize)
                                 8170034:          8200ec0              140 -          8200000             2000
    58478e89 verifier!AVrfDebugPageHeapAllocate+0x00000229
    77410f3e ntdll!RtlDebugAllocateHeap+0x00000030
    773cab47 ntdll!RtlpAllocateHeap+0x000000c4
    77373431 ntdll!RtlAllocateHeap+0x0000023a
    00513d21 pdfium_test_exe!_calloc_base+0x00000047 [d:\rs1\minkernel\crts\ucrt\src\appcrt\heap\calloc_base.cpp @ 38]
    0047ef1d pdfium_test_exe!opj_tcd_code_block_dec_allocate+0x00000036 [third_party\libopenjpeg20\tcd.c @ 1134]
    0047ff51 pdfium_test_exe!opj_tcd_init_decode_tile+0x00000957 [third_party\libopenjpeg20\tcd.c @ 1070]
    0047af8c pdfium_test_exe!opj_j2k_read_tile_header+0x0000047c [third_party\libopenjpeg20\j2k.c @ 8034]
    004792c7 pdfium_test_exe!opj_j2k_decode_tiles+0x00000137 [third_party\libopenjpeg20\j2k.c @ 9600]
    004798d9 pdfium_test_exe!opj_j2k_exec+0x00000032 [third_party\libopenjpeg20\j2k.c @ 7304]
    00478d5e pdfium_test_exe!opj_j2k_decode+0x0000004e [third_party\libopenjpeg20\j2k.c @ 9828]
    00475b69 pdfium_test_exe!opj_decode+0x00000026 [third_party\libopenjpeg20\openjpeg.c @ 412]
    00466236 pdfium_test_exe!CJPX_Decoder::Init+0x00000183 [core\fxcodec\codec\fx_codec_jpx_opj.cpp @ 748]
    00465cce pdfium_test_exe!CCodec_JpxModule::CreateDecoder+0x0000002b [core\fxcodec\codec\fx_codec_jpx_opj.cpp @ 879]
    0042f73c pdfium_test_exe!CPDF_DIBSource::LoadJpxBitmap+0x0000004f [core\fpdfapi\render\cpdf_dibsource.cpp @ 633]
    0042e164 pdfium_test_exe!CPDF_DIBSource::CreateDecoder+0x00000052 [core\fpdfapi\render\cpdf_dibsource.cpp @ 511]
    0042fefa pdfium_test_exe!CPDF_DIBSource::StartLoadDIBSource+0x00000176 [core\fpdfapi\render\cpdf_dibsource.cpp @ 288]
    00435a46 pdfium_test_exe!CPDF_ImageCacheEntry::StartGetCachedBitmap+0x0000008b [core\fpdfapi\render\cpdf_imagecacheentry.cpp @ 71]
    00419d45 pdfium_test_exe!CPDF_PageRenderCache::StartGetCachedBitmap+0x00000082 [core\fpdfapi\render\cpdf_pagerendercache.cpp @ 97]
    00443224 pdfium_test_exe!CPDF_ImageLoader::Start+0x0000003a [core\fpdfapi\render\cpdf_imageloader.cpp @ 35]
    0043a94c pdfium_test_exe!CPDF_ImageRenderer::StartLoadDIBSource+0x00000055 [core\fpdfapi\render\cpdf_imagerenderer.cpp @ 62]
    0043a34d pdfium_test_exe!CPDF_ImageRenderer::Start+0x00000079 [core\fpdfapi\render\cpdf_imagerenderer.cpp @ 181]
    0041d718 pdfium_test_exe!CPDF_RenderStatus::ContinueSingleObject+0x000000ab [core\fpdfapi\render\cpdf_renderstatus.cpp @ 1131]
    004082a6 pdfium_test_exe!CPDF_ProgressiveRenderer::Continue+0x000001b9 [core\fpdfapi\render\cpdf_progressiverenderer.cpp @ 81]
    003ded65 pdfium_test_exe!`anonymous namespace'::RenderPageImpl+0x000001ef [fpdfsdk\fpdfview.cpp @ 128]
    003de38b pdfium_test_exe!FPDF_RenderPage_Retail+0x00000058 [fpdfsdk\fpdfview.cpp @ 1240]
    003e2628 pdfium_test_exe!FPDF_RenderPageBitmap_Start+0x000000df [fpdfsdk\fpdf_progressive.cpp @ 67]
    003d433b pdfium_test_exe!`anonymous namespace'::RenderPage+0x000001aa [samples\pdfium_test.cc @ 1259]
    003d4824 pdfium_test_exe!`anonymous namespace'::RenderPdf+0x0000027b [samples\pdfium_test.cc @ 1455]
    003da90d pdfium_test_exe!main+0x00000373 [samples\pdfium_test.cc @ 1616]
    0050327b pdfium_test_exe!__scrt_common_main_seh+0x000000f9 [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 253]
    76c1336a kernel32!BaseThreadInitThunk+0x0000000e


VERSION
Chrome Version: latest pdfium
Operating System: All

REPRODUCTION CASE
The proof-of-concept file was attached.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [tab, browser, etc.]
Crash State: [see link above: stack trace, registers, exception record]
Client ID (if relevant): [see link above]


## Attachments

- deleted (application/octet-stream, 0 B)
- [752829.patch](attachments/752829.patch) (application/octet-stream, 1.7 KB)
- [resolve_malloc_free_mismatch.patch](attachments/resolve_malloc_free_mismatch.patch) (application/octet-stream, 5.4 KB)

## Timeline

### st...@gmail.com (2017-08-07)

The original mismatch of opj_calloc/FX_Free was found in function sycc422_to_rgb. Some similar cases can be found in the following functions.

1. sycc444_to_rgb
2. sycc420_to_rgb
3. color_apply_conversion
4. sycc422_to_rgb (this case)

### el...@chromium.org (2017-08-07)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### st...@gmail.com (2017-08-07)

According to contents of file pdfium/build/config/BUILD.gn, if any of ASAN, LSAN, TSAN, MSAN was enabled, macro MEMORY_TOOL_REPLACES_ALLOCATOR will be defined.

```
  if (is_asan || is_lsan || is_tsan || is_msan) {
    defines += [
      "MEMORY_TOOL_REPLACES_ALLOCATOR",
      "MEMORY_SANITIZER_INITIAL_SIZE",
    ]
  }
```

In such case, PartitionFree will indirect to free.

```
ALWAYS_INLINE void PartitionFree(void* ptr) {
#if defined(MEMORY_TOOL_REPLACES_ALLOCATOR)
  free(ptr);
#else
  PartitionAllocHooks::FreeHookIfEnabled(ptr);
  ptr = PartitionCookieFreePointerAdjust(ptr);
  DCHECK(PartitionPointerIsValid(ptr));
  PartitionPage* page = PartitionPointerToPage(ptr);
  PartitionFreeWithPage(ptr, page);
#endif
}
```

So if you want to reproduce this case, please do not enable ASAN, LSAN, TSAN, or MSAN.

### st...@gmail.com (2017-08-07)

A patch works like https://crbug.com/chromium/737033.

### st...@gmail.com (2017-08-07)

If we applied the patch in https://crbug.com/chromium/752829#c4, pdfium_test will crash in another place due to the FX_Alloc/opj_free mismatch circumstance. I open another case as https://crbug.com/chromium/752840.

To fix both of these two issues, I recommend you to review my new patch attached in this comment. It should fix both issues, and replace `free` with `opj_free` in the patch of https://crbug.com/chromium/737033.

BTW, I use static_cast<int*> to wrapper the pointer returned by opj_calloc, just like FX_Alloc does.

### ts...@chromium.org (2017-08-07)

I'll take this while palmer's out.  Looks like these components come from the library at times, so we should replace them with opj_calloc'd memory per your patch.

### ts...@chromium.org (2017-08-07)

[Empty comment from Monorail migration]

### ts...@chromium.org (2017-08-07)

[Empty comment from Monorail migration]

### ts...@chromium.org (2017-08-07)

Fixed a t https://pdfium.googlesource.com/pdfium/+/ae6c3444c268076a234b567c5d43f0b5363ae66a

### sh...@chromium.org (2017-08-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-08-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-08-09)

Nice one! The VRP panel decided to award $3,500 for this report.

### aw...@chromium.org (2017-08-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-10)

This bug requires manual review: M61 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), ketakid@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-08-10)

Pls apply appropriate OSs. Thank you.

### go...@chromium.org (2017-08-10)

+awhalley@ for M61 merge review.

### pa...@chromium.org (2017-08-10)

[Empty comment from Monorail migration]

### ke...@chromium.org (2017-08-10)

Approving merge to M61 Chrome OS.

### sh...@chromium.org (2017-08-14)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-08-16)

Please merge you change to M61 branch 3163 by 4:00 PM PT tomorrow, Thursday (08/17) so we can take it in for next week Beta release. Thank you.

### sh...@chromium.org (2017-08-17)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-08-17)

Hi ochang@, it looks like tsepez@ is out the rest of the week - mind doing the merge to 61?

### ds...@chromium.org (2017-08-21)

Sorry for the slow reply, I've kicked off the merge at: https://pdfium-review.googlesource.com/c/11510

### ds...@chromium.org (2017-08-21)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-08-21)

M61 merge is done so removing "Merge-Approved-61" label.

### st...@gmail.com (2017-08-31)

Please credit to Ke Liu of Tencent's Xuanwu Lab when you're ready to release the new version. Thank you.

### aw...@google.com (2017-09-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/752829?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/752840]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088629)*
