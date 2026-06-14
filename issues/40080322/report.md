# Heap-buffer-overflow in CPDF_DIBSource::GetScanline

| Field | Value |
|-------|-------|
| **Issue ID** | [40080322](https://issues.chromium.org/issues/40080322) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | at...@gmail.com |
| **Assignee** | bo...@foxitsoftware.com |
| **Created** | 2014-08-28 |
| **Bounty** | $3,000.00 |

## Description

Tested on:

OS: Ubuntu 12.04

Chromium:  ASAN Chromium 39.0.2139.0 (Developer Build 0b61f008f6a2)


ASAN-trace:

==26602==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x61700000b955 at pc 0x0000005f01eb bp 0x7fff5fdfb0b0 sp 0x7fff5fdfb0a8
WRITE of size 1 at 0x61700000b955 thread T0
    #0 0x5f01ea in CPDF_DIBSource::TranslateScanline24bpp(unsigned char*, unsigned char const*) const /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_loadimage.cpp:970
    #1 0x5f1534 in CPDF_DIBSource::GetScanline(int) const /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_loadimage.cpp:1181
    #2 0x872ca9 in CFX_DIBSource::Clone(FX_RECT const*) const /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxge/dib/fx_dib_main.cpp:194
    #3 0x5da567 in CPDF_ImageCache::ContinueGetCachedBitmap() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_cache.cpp:331
    #4 0x5d9cf5 in CPDF_ImageCache::StartGetCachedBitmap(CPDF_Dictionary*, CPDF_Dictionary*, int, unsigned int, int, CPDF_RenderStatus*, int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_cache.cpp:319
    #5 0x5d99c2 in CPDF_PageRenderCache::StartGetCachedBitmap(CPDF_Stream*, int, unsigned int, int, CPDF_RenderStatus*, int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_cache.cpp:131
    #6 0x5f48ef in CPDF_ProgressiveImageLoaderHandle::Start(CPDF_ImageLoader*, CPDF_ImageObject const*, CPDF_PageRenderCache*, int, unsigned int, int, CPDF_RenderStatus*, int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_loadimage.cpp:1485
.
.
.

0x61700000b955 is located 0 bytes to the right of 725-byte region [0x61700000b680,0x61700000b955)
allocated by thread T0 here:
    #0 0x4a6f40 in calloc ??:0
    #1 0x5ec773 in CPDF_DIBSource::ContinueToLoadMask() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_loadimage.cpp:278
    #2 0x5e6c53 in CPDF_DIBSource::StartLoadDIBSource(CPDF_Document*, CPDF_Stream const*, int, CPDF_Dictionary*, CPDF_Dictionary*, int, unsigned int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_loadimage.cpp:357
    #3 0x5d9c7d in CPDF_ImageCache::StartGetCachedBitmap(CPDF_Dictionary*, CPDF_Dictionary*, int, unsigned int, int, CPDF_RenderStatus*, int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_cache.cpp:310
    #4 0x5d99c2 in CPDF_PageRenderCache::StartGetCachedBitmap(CPDF_Stream*, int, unsigned int, int, CPDF_RenderStatus*, int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_cache.cpp:131
    #5 0x5f48ef in CPDF_ProgressiveImageLoaderHandle::Start(CPDF_ImageLoader*, CPDF_ImageObject const*, CPDF_PageRenderCache*, int, unsigned int, int, CPDF_RenderStatus*, int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_loadimage.cpp:1485
    #6 0x5f52ef in CPDF_ImageLoader::StartLoadImage(CPDF_ImageObject const*, CPDF_PageRenderCache*, void*&, int, unsigned int, int, CPDF_RenderStatus*, int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_loadimage.cpp:1545
.
.
.

## Attachments

- [CPDF_DIBSourceTranslateScanline24bpp.pdf](attachments/CPDF_DIBSourceTranslateScanline24bpp.pdf) (application/pdf, 58.0 KB)
- [asan_memcpy.pdf](attachments/asan_memcpy.pdf) (application/pdf, 941.6 KB)

## Timeline

### at...@gmail.com (2014-08-28)


Second repro-file that causes almost identical stack. Just a lot larger write.


ASAN-trace:

==21417==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60f00003164d at pc 0x00000048f92a bp 0x7fff2e050e30 sp 0x7fff2e0505e8
WRITE of size 1356 at 0x60f00003164d thread T0
    #0 0x48f929 in __asan_memcpy ??:0
    #1 0x5f089f in CPDF_DIBSource::GetScanline(int) const /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_loadimage.cpp:1132
    #2 0x872ca9 in CFX_DIBSource::Clone(FX_RECT const*) const /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxge/dib/fx_dib_main.cpp:194
    #3 0x5da567 in CPDF_ImageCache::ContinueGetCachedBitmap() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_cache.cpp:331
    #4 0x5d9cf5 in CPDF_ImageCache::StartGetCachedBitmap(CPDF_Dictionary*, CPDF_Dictionary*, int, unsigned int, int, CPDF_RenderStatus*, int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_cache.cpp:319
    #5 0x5d99c2 in CPDF_PageRenderCache::StartGetCachedBitmap(CPDF_Stream*, int, unsigned int, int, CPDF_RenderStatus*, int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_cache.cpp:131
    #6 0x5f48ef in CPDF_ProgressiveImageLoaderHandle::Start(CPDF_ImageLoader*, CPDF_ImageObject const*, CPDF_PageRenderCache*, int, unsigned int, int, CPDF_RenderStatus*, int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_loadimage.cpp:1485
.
.
.
0x60f00003164d is located 0 bytes to the right of 173-byte region [0x60f0000315a0,0x60f00003164d)
allocated by thread T0 here:
    #0 0x4a6f40 in calloc ??:0
    #1 0x5ec773 in CPDF_DIBSource::ContinueToLoadMask() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_loadimage.cpp:278
    #2 0x5e6c53 in CPDF_DIBSource::StartLoadDIBSource(CPDF_Document*, CPDF_Stream const*, int, CPDF_Dictionary*, CPDF_Dictionary*, int, unsigned int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_loadimage.cpp:357
    #3 0x5d9c7d in CPDF_ImageCache::StartGetCachedBitmap(CPDF_Dictionary*, CPDF_Dictionary*, int, unsigned int, int, CPDF_RenderStatus*, int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_cache.cpp:310
    #4 0x5d99c2 in CPDF_PageRenderCache::StartGetCachedBitmap(CPDF_Stream*, int, unsigned int, int, CPDF_RenderStatus*, int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_cache.cpp:131
    #5 0x5f48ef in CPDF_ProgressiveImageLoaderHandle::Start(CPDF_ImageLoader*, CPDF_ImageObject const*, CPDF_PageRenderCache*, int, unsigned int, int, CPDF_RenderStatus*, int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_loadimage.cpp:1485
    #6 0x5f52ef in CPDF_ImageLoader::StartLoadImage(CPDF_ImageObject const*, CPDF_PageRenderCache*, void*&, int, unsigned int, int, CPDF_RenderStatus*, int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_loadimage.cpp:1545
.
.
.


### in...@chromium.org (2014-08-28)

i think this is a dup. Bo, feel free to dup it out.

### in...@chromium.org (2014-08-28)

Bo, make sure to check on pdfium_test trunk before duping. The line numbers seem different on this one.

### bo...@foxitsoftware.com (2014-08-28)

I can repro the test case "asan_memcyp.pdf" on pdfium trunk.

### cl...@chromium.org (2014-08-28)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5421386198679552

### cl...@chromium.org (2014-08-28)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5421386198679552

Uploader: aarya@google.com
Job Type: Linux_asan_pdfium

Crash Type: Heap-buffer-overflow WRITE {*}
Crash Address: 0x6110001549ed
Crash State:
  CPDF_DIBSource::GetScanline
  CFX_DIBSource::Clone
  CPDF_ImageCache::ContinueGetCachedBitmap
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=291998:292010

Minimized Testcase (941.65 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94LU1KA_p2Cr28Hd6XP7xGAwJ-VELxRSOZYT7U8N4DUxZh2Anazpws3NaOKWNvfUXmxOTG98j6ADrW15hXBs5WFlcItW81A98h2z7ZTCUE5zhqTl7AHQ59GEvuHY_xAzppiMdb0bELm4dT0bXgHRXqqWhtBbFyLbTemtCUqFm0Mr4VVi44



### cl...@chromium.org (2014-08-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-31)

[Empty comment from Monorail migration]

### bo...@foxitsoftware.com (2014-09-01)

Fixed in https://pdfium.googlesource.com/pdfium/+/9f810e7216c2dbb1a1ab090f1bee4207ecd871c0

### cl...@chromium.org (2014-09-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-04)

ClusterFuzz has detected this issue as fixed in range 293090:293185.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5421386198679552

Uploader: aarya@google.com
Job Type: Linux_asan_pdfium

Crash Type: Heap-buffer-overflow WRITE {*}
Crash Address: 0x6110001549ed
Crash State:
  CPDF_DIBSource::GetScanline
  CFX_DIBSource::Clone
  CPDF_ImageCache::ContinueGetCachedBitmap
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=291998:292010
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=293090:293185

Minimized Testcase (941.65 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94LU1KA_p2Cr28Hd6XP7xGAwJ-VELxRSOZYT7U8N4DUxZh2Anazpws3NaOKWNvfUXmxOTG98j6ADrW15hXBs5WFlcItW81A98h2z7ZTCUE5zhqTl7AHQ59GEvuHY_xAzppiMdb0bELm4dT0bXgHRXqqWhtBbFyLbTemtCUqFm0Mr4VVi44

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### bo...@foxitsoftware.com (2014-09-26)

@matthewyuan, can we merge this issue too? Some other to-be-merged issues depend on the CL of this one.

### ti...@chromium.org (2014-09-29)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-09-29)

Matthew - we need to that this along as it's blocking 409692 which was merged to M38. Grateful for your merge approval ASAP.

### ti...@chromium.org (2014-09-29)

bo_xu@ made some changes, so we don't need this to come along anymore. Removing merge request and resetting the labels.

### ti...@chromium.org (2014-10-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-08)

Bulk update: removing view restriction from closed bugs.

### in...@chromium.org (2015-01-05)

[Empty comment from Monorail migration]

### ti...@google.com (2015-01-22)

Congrats - $3000 for this report.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-15)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/408541?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/409692]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080322)*
