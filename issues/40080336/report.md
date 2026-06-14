# Heap-buffer-overflow in CPDF_DIBSource::GetScanline

| Field | Value |
|-------|-------|
| **Issue ID** | [40080336](https://issues.chromium.org/issues/40080336) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | cl...@gmail.com |
| **Assignee** | bo...@foxitsoftware.com |
| **Created** | 2014-08-31 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Stack is equivalent to #406895, however this testcase is still crashing despite the original testcase being fixed in the latest builds.

=================================================================  

==14550==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60300005c337 at pc 0x00000048f92a bp 0x7fff8790d390 sp 0x7fff8790cb48  

WRITE of size 158 at 0x60300005c337 thread T0  

#0 0x48f929 in **asan\_memcpy ??:0:0  

#1 0x5f067f in CPDF\_DIBSource::GetScanline(int) const /b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1137:13  

#2 0x872ad9 in CFX\_DIBSource::Clone(FX\_RECT const\*) const /b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/core/src/fxge/dib/fx\_dib\_main.cpp:194:35  

#3 0x5da4c7 in CPDF\_ImageCache::ContinueGetCachedBitmap() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:331:27  

#4 0x5d9c55 in CPDF\_ImageCache::StartGetCachedBitmap(CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:319:5  

#5 0x5d9922 in CPDF\_PageRenderCache::StartGetCachedBitmap(CPDF\_Stream\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:131:15  

#6 0x5f467f in CPDF\_ProgressiveImageLoaderHandle::Start(CPDF\_ImageLoader\*, CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1490:15  

#7 0x5f507f in CPDF\_ImageLoader::StartLoadImage(CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, void\*&, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1550:19  

#8 0x5de2e8 in CPDF\_ImageRenderer::StartLoadDIBSource() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:371:9  

#9 0x5dad4b in CPDF\_ImageRenderer::Start(CPDF\_RenderStatus\*, CPDF\_PageObject const\*, CFX\_Matrix const\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:525:9  

#10 0x5d0cb4 in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject const\*, CFX\_Matrix const\*, IFX\_Pause\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:350:14  

#11 0x5d712d in CPDF\_ProgressiveRenderer::Continue(IFX\_Pause\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:1175:21  

#12 0x4c9860 in FPDF\_RenderPage\_Retail(CRenderContext\*, void\*, int, int, int, int, int, int, int, IFSDK\_PAUSE\_Adapter\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:772:2  

#13 0x4c9b10 in FPDF\_RenderPageBitmap /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:574:2  

#14 0x4c5135 in RenderPdf(char const\*, char const\*, unsigned long, OutputFormat) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:324:5  

#15 0x4c5b59 in main /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:406:7  

#16 0x7f0394bdcec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287  

#17 0x4c441c in \_start ??:0:0

0x60300005c337 is located 0 bytes to the right of 23-byte region [0x60300005c320,0x60300005c337)  

allocated by thread T0 here:  

#0 0x4a6f40 in **interceptor\_calloc ??:0:0  

#1 0x5ec548 in CPDF\_DIBSource::ContinueToLoadMask() /b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:279:18  

#2 0x5e6bb3 in CPDF\_DIBSource::StartLoadDIBSource(CPDF\_Document\*, CPDF\_Stream const\*, int, CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int) /b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:358:10  

#3 0x5d9bdd in CPDF\_ImageCache::StartGetCachedBitmap(CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:310:15  

#4 0x5d9922 in CPDF\_PageRenderCache::StartGetCachedBitmap(CPDF\_Stream\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:131:15  

#5 0x5f467f in CPDF\_ProgressiveImageLoaderHandle::Start(CPDF\_ImageLoader\*, CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1490:15  

#6 0x5f507f in CPDF\_ImageLoader::StartLoadImage(CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, void\*&, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1550:19  

#7 0x5de2e8 in CPDF\_ImageRenderer::StartLoadDIBSource() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:371:9  

#8 0x5dad4b in CPDF\_ImageRenderer::Start(CPDF\_RenderStatus\*, CPDF\_PageObject const\*, CFX\_Matrix const\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:525:9  

#9 0x5d0cb4 in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject const\*, CFX\_Matrix const\*, IFX\_Pause\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:350:14  

#10 0x5d712d in CPDF\_ProgressiveRenderer::Continue(IFX\_Pause\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:1175:21  

#11 0x4c9860 in FPDF\_RenderPage\_Retail(CRenderContext\*, void\*, int, int, int, int, int, int, int, IFSDK\_PAUSE\_Adapter\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:772:2  

#12 0x4c9b10 in FPDF\_RenderPageBitmap /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:574:2  

#13 0x4c5135 in RenderPdf(char const\*, char const\*, unsigned long, OutputFormat) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:324:5  

#14 0x4c5b59 in main /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:406:7  

#15 0x7f0394bdcec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

SUMMARY: AddressSanitizer: heap-buffer-overflow ??:0 ??  

Shadow bytes around the buggy address:  

0x0c0680003810: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0680003820: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0680003830: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0680003840: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0680003850: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x0c0680003860: fa fa fa fa 00 00[07]fa fa fa 00 00 00 00 fa fa  

0x0c0680003870: fd fd fd fd fa fa fd fd fd fa fa fa fd fd fd fa  

0x0c0680003880: fa fa fd fd fd fa fa fa fd fd fd fa fa fa fd fd  

0x0c0680003890: fd fa fa fa 00 00 00 04 fa fa 00 00 00 fa fa fa  

0x0c06800038a0: fd fd fd fd fa fa 00 00 04 fa fa fa 00 00 04 fa  

0x0c06800038b0: fa fa 00 00 00 00 fa fa 00 00 00 00 fa fa 00 00  

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

ASan internal: fe  

==14550==ABORTING

**VERSION**  

Chrome Version: asan-symbolized-linux-release-292818

**REPRODUCTION CASE**  

Using pdfium\_test to reproduce. Testcase attached as repro.pdf

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace, registers, exception record]**  

**Client ID (if relevant): [see link above]**

## Attachments

- [repro.pdf](attachments/repro.pdf) (application/pdf, 18.0 KB)

## Timeline

### cl...@chromium.org (2014-08-31)

[Empty comment from Monorail migration]

### wf...@chromium.org (2014-09-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-01)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5748743623147520

### wf...@chromium.org (2014-09-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-01)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5748743623147520

Uploader: wfh@chromium.org
Job Type: Linux_asan_pdfium

Crash Type: Heap-buffer-overflow WRITE {*}
Crash Address: 0x60a000116a17
Crash State:
  CPDF_DIBSource::GetScanline
  CFX_DIBSource::Clone
  CPDF_ImageCache::ContinueGetCachedBitmap
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=291998:292010

Minimized Testcase (18.02 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97PT2C4J308b-AwF24YFKNqpE-UxlRCxunVHoT44ZtCS5QWmE65HicJSlmUuduNSlSCyUE4JGyqos-TnH3IdrTGHZTKQQD2ajKPtBEwqLIOb9QOO0TszexKHdqXmvfEB8MZ-kyn3hC7-yN8RzwWfLqxNHK2jywvs16OKiXj86VfoA6XemA



### cl...@chromium.org (2014-09-01)

[Empty comment from Monorail migration]

### bo...@foxitsoftware.com (2014-09-01)

Fixed in https://pdfium.googlesource.com/pdfium/+/9f810e7216c2dbb1a1ab090f1bee4207ecd871c0

### cl...@chromium.org (2014-09-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-04)

ClusterFuzz has detected this issue as fixed in range 293090:293185.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5748743623147520

Uploader: wfh@chromium.org
Job Type: Linux_asan_pdfium

Crash Type: Heap-buffer-overflow WRITE {*}
Crash Address: 0x60a000116a17
Crash State:
  CPDF_DIBSource::GetScanline
  CFX_DIBSource::Clone
  CPDF_ImageCache::ContinueGetCachedBitmap
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=291998:292010
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=293090:293185

Minimized Testcase (18.02 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97PT2C4J308b-AwF24YFKNqpE-UxlRCxunVHoT44ZtCS5QWmE65HicJSlmUuduNSlSCyUE4JGyqos-TnH3IdrTGHZTKQQD2ajKPtBEwqLIOb9QOO0TszexKHdqXmvfEB8MZ-kyn3hC7-yN8RzwWfLqxNHK2jywvs16OKiXj86VfoA6XemA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ti...@chromium.org (2014-10-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-08)

Bulk update: removing view restriction from closed bugs.

### in...@chromium.org (2015-01-05)

[Empty comment from Monorail migration]

### ti...@google.com (2015-01-22)

$3000 here as well. Make it rain.

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/409475?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080336)*
