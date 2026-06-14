# Heap-buffer-overflow in color_sycc_to_rgb

| Field | Value |
|-------|-------|
| **Issue ID** | [40080553](https://issues.chromium.org/issues/40080553) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | cl...@gmail.com |
| **Assignee** | bo...@foxitsoftware.com |
| **Created** | 2014-09-30 |
| **Bounty** | $1,000.00 |

## Description

# **VULNERABILITY DETAILS** The attached testcase crashes the latest ASAN build of pdfium\_test as follows:

==30705==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7f766c24f700 at pc 0x00000064758c bp 0x7fff8f76e330 sp 0x7fff8f76e328  

READ of size 4 at 0x7f766c24f700 thread T0  

#0 0x64758b in sycc422\_to\_rgb(opj\_image\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:171:13  

#1 0x645c84 in color\_sycc\_to\_rgb(opj\_image\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:294:9  

#2 0x64824f in CJPX\_Decoder::Init(unsigned char const\*, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:644:9  

#3 0x649980 in CCodec\_JpxModule::CreateDecoder(unsigned char const\*, unsigned int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:764:10  

#4 0x5d5f41 in CPDF\_DIBSource::LoadJpxBitmap() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:643:21  

#5 0x5d1bab in CPDF\_DIBSource::CreateDecoder() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:599:9  

#6 0x5cea18 in CPDF\_DIBSource::StartLoadDIBSource(CPDF\_Document\*, CPDF\_Stream const\*, int, CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:335:15  

#7 0x5c13fd in CPDF\_ImageCache::StartGetCachedBitmap(CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:310:15  

#8 0x5c1123 in CPDF\_PageRenderCache::StartGetCachedBitmap(CPDF\_Stream\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:131:15  

#9 0x5ddb20 in CPDF\_ProgressiveImageLoaderHandle::Start(CPDF\_ImageLoader\*, CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1489:15  

#10 0x5de543 in CPDF\_ImageLoader::StartLoadImage(CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, void\*&, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1549:19  

#11 0x5c5db9 in CPDF\_ImageRenderer::StartLoadDIBSource() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:371:9  

#12 0x5c258d in CPDF\_ImageRenderer::Start(CPDF\_RenderStatus\*, CPDF\_PageObject const\*, CFX\_Matrix const\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:525:9  

#13 0x5b81f6 in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject const\*, CFX\_Matrix const\*, IFX\_Pause\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:350:14  

#14 0x5be755 in CPDF\_ProgressiveRenderer::Continue(IFX\_Pause\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:1175:21  

#15 0x4aaa58 in FPDF\_RenderPage\_Retail(CRenderContext\*, void\*, int, int, int, int, int, int, int, IFSDK\_PAUSE\_Adapter\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:789:2  

#16 0x4aadf0 in FPDF\_RenderPageBitmap /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:586:2  

#17 0x4a6875 in RenderPdf(char const\*, char const\*, unsigned long, OutputFormat) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:324:5  

#18 0x4a7329 in main /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:406:7  

#19 0x7f766e9aaec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287  

#20 0x42299c in \_start ??:0:0

0x7f766c24f700 is located 0 bytes to the right of 1195776-byte region [0x7f766c12b800,0x7f766c24f700)  

allocated by thread T0 here:  

#0 0x4898f0 in **interceptor\_calloc ??:0:0  

#1 0x737521 in opj\_j2k\_update\_image\_data /b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:7748:62  

#2 0x738500 in opj\_j2k\_decode\_tiles /b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:9184:23  

#3 0x72ccd1 in opj\_j2k\_exec /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:7048:41  

#4 0x7354a0 in opj\_j2k\_decode /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:9368:15  

#5 0x650ae9 in opj\_jp2\_decode /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/jp2.c:1332:8  

#6 0x64808a in CJPX\_Decoder::Init(unsigned char const\*, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:624:15  

#7 0x649980 in CCodec\_JpxModule::CreateDecoder(unsigned char const\*, unsigned int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:764:10  

#8 0x5d5f41 in CPDF\_DIBSource::LoadJpxBitmap() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:643:21  

#9 0x5d1bab in CPDF\_DIBSource::CreateDecoder() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:599:9  

#10 0x5cea18 in CPDF\_DIBSource::StartLoadDIBSource(CPDF\_Document\*, CPDF\_Stream const\*, int, CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:335:15  

#11 0x5c13fd in CPDF\_ImageCache::StartGetCachedBitmap(CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:310:15  

#12 0x5c1123 in CPDF\_PageRenderCache::StartGetCachedBitmap(CPDF\_Stream\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:131:15  

#13 0x5ddb20 in CPDF\_ProgressiveImageLoaderHandle::Start(CPDF\_ImageLoader\*, CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1489:15  

#14 0x5de543 in CPDF\_ImageLoader::StartLoadImage(CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, void\*&, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1549:19  

#15 0x5c5db9 in CPDF\_ImageRenderer::StartLoadDIBSource() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:371:9  

#16 0x5c258d in CPDF\_ImageRenderer::Start(CPDF\_RenderStatus\*, CPDF\_PageObject const\*, CFX\_Matrix const\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:525:9  

#17 0x5b81f6 in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject const\*, CFX\_Matrix const\*, IFX\_Pause\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:350:14  

#18 0x5be755 in CPDF\_ProgressiveRenderer::Continue(IFX\_Pause\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:1175:21  

#19 0x4aaa58 in FPDF\_RenderPage\_Retail(CRenderContext\*, void\*, int, int, int, int, int, int, int, IFSDK\_PAUSE\_Adapter\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:789:2  

#20 0x4aadf0 in FPDF\_RenderPageBitmap /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:586:2  

#21 0x4a6875 in RenderPdf(char const\*, char const\*, unsigned long, OutputFormat) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:324:5  

#22 0x4a7329 in main /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:406:7  

#23 0x7f766e9aaec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

SUMMARY: AddressSanitizer: heap-buffer-overflow ??:0 ??  

Shadow bytes around the buggy address:  

0x0fef4d841e90: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fef4d841ea0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fef4d841eb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fef4d841ec0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fef4d841ed0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x0fef4d841ee0:[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0fef4d841ef0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0fef4d841f00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0fef4d841f10: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0fef4d841f20: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0fef4d841f30: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Heap right redzone: fb  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack partial redzone: f4  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

ASan internal: fe  

==30705==ABORTING

**VERSION**  

Chrome Version: latest asan build of pdfium\_test

**REPRODUCTION CASE**  

Attached in repro.pdf

## Attachments

- [repro.pdf](attachments/repro.pdf) (application/pdf, 56.4 KB)

## Timeline

### cl...@chromium.org (2014-09-30)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5822145306296320

### cl...@chromium.org (2014-09-30)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5822145306296320

Uploader: felt@chromium.org
Job Type: Linux_asan_pdfium

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x7f4208c0b700
Crash State:
  color_sycc_to_rgb
  CJPX_Decoder::Init
  CCodec_JpxModule::CreateDecoder
  

Minimized Testcase (56.44 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95vOPd9lclBxOFd7_7IWmT-_mn7MxpcgmlDnqUaJeNOye40HwdRu_ysoExLy-dGjMft8erUv5h6I5imxf4uJ494I5pxlJRtCugVOCvyhc5I6evBhImIkTtBnDjQTp6_hY9izIxSFPLlFm51CTzNWuH_XgCooSdQfoBnod89V1dD-np9zIU



### cl...@chromium.org (2014-09-30)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-09-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-30)

[Empty comment from Monorail migration]

### fe...@chromium.org (2014-10-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-09)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### bo...@foxitsoftware.com (2014-10-09)

@antonin, can you take a look at this one. The crash is not inside jp2, but it looks like the image from opj_read_header or opj_decode has invalid member values.

### bo...@foxitsoftware.com (2014-10-09)

[Empty comment from Monorail migration]

### bo...@foxitsoftware.com (2014-10-10)

Fixed in https://pdfium.googlesource.com/pdfium/+/6cf012af4954807255ce7cdb5b92a20f74d34e6d

### cl...@chromium.org (2014-10-11)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-10-30)

let it roll into m40.

### in...@chromium.org (2014-11-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-17)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-01-22)

Congratulations - $1000 for this report.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-07)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/418881?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080553)*
