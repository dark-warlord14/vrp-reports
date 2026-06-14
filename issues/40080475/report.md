# Heap-use-after-free in opj_t1_decode_cblks

| Field | Value |
|-------|-------|
| **Issue ID** | [40080475](https://issues.chromium.org/issues/40080475) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | cl...@gmail.com |
| **Assignee** | bo...@foxitsoftware.com |
| **Created** | 2014-09-15 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached testcase crashes the asan build of pdfium\_test as follows:

=================================================================  

==9091==ERROR: AddressSanitizer: heap-use-after-free on address 0x60c00000b5c0 at pc 0x0000007bfe10 bp 0x7fffc6235720 sp 0x7fffc6235718  

READ of size 8 at 0x60c00000b5c0 thread T0  

#0 0x7bfe0f in opj\_t1\_decode\_cblk /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/t1.c:1403:4  

#1 0x7bf010 in opj\_t1\_decode\_cblks /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/t1.c:1288:38  

#2 0x7735ae in opj\_tcd\_t1\_decode /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/tcd.c:1521:34  

#3 0x7732ab in opj\_tcd\_decode\_tile /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/tcd.c:1240:20  

#4 0x74373f in opj\_j2k\_decode\_tile /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:7661:15  

#5 0x7542b0 in opj\_j2k\_decode\_tiles /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:9177:23  

#6 0x7402c1 in opj\_j2k\_exec /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:7048:41  

#7 0x7483a0 in opj\_j2k\_decode /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:9368:15  

#8 0x667d59 in opj\_jp2\_decode /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/jp2.c:1332:8  

#9 0x65d4e1 in CJPX\_Decoder::Init(unsigned char const\*, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:624:15  

#10 0x65eb5f in CCodec\_JpxModule::CreateDecoder(unsigned char const\*, unsigned int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:764:10  

#11 0x5ef8c1 in CPDF\_DIBSource::LoadJpxBitmap() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:643:21  

#12 0x5eba20 in CPDF\_DIBSource::CreateDecoder() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:599:9  

#13 0x5e88ec in CPDF\_DIBSource::StartLoadDIBSource(CPDF\_Document\*, CPDF\_Stream const\*, int, CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:335:15  

#14 0x5dba6d in CPDF\_ImageCache::StartGetCachedBitmap(CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:310:15  

#15 0x5db7b2 in CPDF\_PageRenderCache::StartGetCachedBitmap(CPDF\_Stream\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:131:15  

#16 0x5f6bdf in CPDF\_ProgressiveImageLoaderHandle::Start(CPDF\_ImageLoader\*, CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1489:15  

#17 0x5f75df in CPDF\_ImageLoader::StartLoadImage(CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, void\*&, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1549:19  

#18 0x5e0178 in CPDF\_ImageRenderer::StartLoadDIBSource() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:371:9  

#19 0x5dcbdb in CPDF\_ImageRenderer::Start(CPDF\_RenderStatus\*, CPDF\_PageObject const\*, CFX\_Matrix const\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:525:9  

#20 0x5d2b44 in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject const\*, CFX\_Matrix const\*, IFX\_Pause\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:350:14  

#21 0x5d8fbd in CPDF\_ProgressiveRenderer::Continue(IFX\_Pause\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:1175:21  

#22 0x4c9fd0 in FPDF\_RenderPage\_Retail(CRenderContext\*, void\*, int, int, int, int, int, int, int, IFSDK\_PAUSE\_Adapter\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:772:2  

#23 0x4ca280 in FPDF\_RenderPageBitmap /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:574:2  

#24 0x4c5e55 in RenderPdf(char const\*, char const\*, unsigned long, OutputFormat) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:324:5  

#25 0x4c6879 in main /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:406:7  

#26 0x7f5912726ec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287  

#27 0x4c51cc in \_start ??:0:0

0x60c00000b5c0 is located 0 bytes inside of 128-byte region [0x60c00000b5c0,0x60c00000b640)  

freed by thread T0 here:  

#0 0x4a7e8e in **interceptor\_realloc ??:0:0  

#1 0x7709b2 in opj\_tcd\_init\_decode\_tile /b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/tcd.c:1006:1  

#2 0x741fdf in opj\_j2k\_read\_tile\_header /b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:7612:15  

#3 0x754194 in opj\_j2k\_decode\_tiles /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:9149:23  

#4 0x7402c1 in opj\_j2k\_exec /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:7048:41  

#5 0x7483a0 in opj\_j2k\_decode /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:9368:15  

#6 0x667d59 in opj\_jp2\_decode /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/jp2.c:1332:8  

#7 0x65d4e1 in CJPX\_Decoder::Init(unsigned char const\*, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:624:15  

#8 0x65eb5f in CCodec\_JpxModule::CreateDecoder(unsigned char const\*, unsigned int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:764:10  

#9 0x5ef8c1 in CPDF\_DIBSource::LoadJpxBitmap() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:643:21  

#10 0x5eba20 in CPDF\_DIBSource::CreateDecoder() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:599:9  

#11 0x5e88ec in CPDF\_DIBSource::StartLoadDIBSource(CPDF\_Document\*, CPDF\_Stream const\*, int, CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:335:15  

#12 0x5dba6d in CPDF\_ImageCache::StartGetCachedBitmap(CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:310:15  

#13 0x5db7b2 in CPDF\_PageRenderCache::StartGetCachedBitmap(CPDF\_Stream\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:131:15  

#14 0x5f6bdf in CPDF\_ProgressiveImageLoaderHandle::Start(CPDF\_ImageLoader\*, CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1489:15  

#15 0x5f75df in CPDF\_ImageLoader::StartLoadImage(CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, void\*&, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1549:19  

#16 0x5e0178 in CPDF\_ImageRenderer::StartLoadDIBSource() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:371:9  

#17 0x5dcbdb in CPDF\_ImageRenderer::Start(CPDF\_RenderStatus\*, CPDF\_PageObject const\*, CFX\_Matrix const\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:525:9  

#18 0x5d2b44 in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject const\*, CFX\_Matrix const\*, IFX\_Pause\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:350:14  

#19 0x5d8fbd in CPDF\_ProgressiveRenderer::Continue(IFX\_Pause\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:1175:21  

#20 0x4c9fd0 in FPDF\_RenderPage\_Retail(CRenderContext\*, void\*, int, int, int, int, int, int, int, IFSDK\_PAUSE\_Adapter\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:772:2  

#21 0x4ca280 in FPDF\_RenderPageBitmap /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:574:2  

#22 0x4c5e55 in RenderPdf(char const\*, char const\*, unsigned long, OutputFormat) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:324:5  

#23 0x4c6879 in main /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:406:7  

#24 0x7f5912726ec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

previously allocated by thread T0 here:  

#0 0x4a7e8e in **interceptor\_realloc ??:0:0  

#1 0x7709b2 in opj\_tcd\_init\_decode\_tile /b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/tcd.c:1006:1  

#2 0x741fdf in opj\_j2k\_read\_tile\_header /b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:7612:15  

#3 0x754194 in opj\_j2k\_decode\_tiles /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:9149:23  

#4 0x7402c1 in opj\_j2k\_exec /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:7048:41  

#5 0x7483a0 in opj\_j2k\_decode /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:9368:15  

#6 0x667d59 in opj\_jp2\_decode /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/jp2.c:1332:8  

#7 0x65d4e1 in CJPX\_Decoder::Init(unsigned char const\*, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:624:15  

#8 0x65eb5f in CCodec\_JpxModule::CreateDecoder(unsigned char const\*, unsigned int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:764:10  

#9 0x5ef8c1 in CPDF\_DIBSource::LoadJpxBitmap() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:643:21  

#10 0x5eba20 in CPDF\_DIBSource::CreateDecoder() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:599:9  

#11 0x5e88ec in CPDF\_DIBSource::StartLoadDIBSource(CPDF\_Document\*, CPDF\_Stream const\*, int, CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:335:15  

#12 0x5dba6d in CPDF\_ImageCache::StartGetCachedBitmap(CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:310:15  

#13 0x5db7b2 in CPDF\_PageRenderCache::StartGetCachedBitmap(CPDF\_Stream\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:131:15  

#14 0x5f6bdf in CPDF\_ProgressiveImageLoaderHandle::Start(CPDF\_ImageLoader\*, CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1489:15  

#15 0x5f75df in CPDF\_ImageLoader::StartLoadImage(CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, void\*&, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1549:19  

#16 0x5e0178 in CPDF\_ImageRenderer::StartLoadDIBSource() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:371:9  

#17 0x5dcbdb in CPDF\_ImageRenderer::Start(CPDF\_RenderStatus\*, CPDF\_PageObject const\*, CFX\_Matrix const\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:525:9  

#18 0x5d2b44 in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject const\*, CFX\_Matrix const\*, IFX\_Pause\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:350:14  

#19 0x5d8fbd in CPDF\_ProgressiveRenderer::Continue(IFX\_Pause\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:1175:21  

#20 0x4c9fd0 in FPDF\_RenderPage\_Retail(CRenderContext\*, void\*, int, int, int, int, int, int, int, IFSDK\_PAUSE\_Adapter\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:772:2  

#21 0x4ca280 in FPDF\_RenderPageBitmap /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:574:2  

#22 0x4c5e55 in RenderPdf(char const\*, char const\*, unsigned long, OutputFormat) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:324:5  

#23 0x4c6879 in main /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:406:7  

#24 0x7f5912726ec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

SUMMARY: AddressSanitizer: heap-use-after-free ??:0 ??  

Shadow bytes around the buggy address:  

0x0c187fff9660: 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa  

0x0c187fff9670: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c187fff9680: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c187fff9690: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa  

0x0c187fff96a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x0c187fff96b0: fa fa fa fa fa fa fa fa[fd]fd fd fd fd fd fd fd  

0x0c187fff96c0: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa  

0x0c187fff96d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x0c187fff96e0: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x0c187fff96f0: 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa fa  

0x0c187fff9700: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 fa  

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

==9091==ABORTING

**VERSION**  

Chrome Version: latest asan build of pdfium\_test

**REPRODUCTION CASE**  

Attached in repro.pdf

## Attachments

- [repro.pdf](attachments/repro.pdf) (application/pdf, 35.3 KB)

## Timeline

### in...@chromium.org (2014-09-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-15)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6352457559965696

### cl...@chromium.org (2014-09-16)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6352457559965696

Uploader: aarya@google.com
Job Type: Linux_asan_pdfium

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x610000007280
Crash State:
  opj_t1_decode_cblks
  opj_tcd_decode_tile
  opj_j2k_decode_tile
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=289356:289512

Minimized Testcase (35.32 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97yo_CxatEk9Bp3ang1V7uD4mJ2FYKAFiflUIa_0Hr96VtXNrmKVj6iCIw1qKodDfHLNwqEZU58XmAn8iDZ2COhr4qhSSBX9Kgjxt8Dr6Mhm-RqE25FGEkASRWijsVhvOZY5WtKxs9VtVDaHGZ5qtZQVNc1SA8-6jkv0YIyhj56GZWCv10



### ts...@chromium.org (2014-09-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-09-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-09-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-09-17)

+cc Libopenjpeg devs.

Antonin, Mathieu - can you please take a look at these libopenjpeg high severity security vulnerabilities asap. Feel free to port them to libopenjpeg bug tracker provided you can restrict view them [should not be open to public].

### in...@chromium.org (2014-09-19)

+cc m.darbois

Bo, Jun, what is the easy way to extract the image bits from pdf. Can you please attach them to these 11 bugs.

### cl...@chromium.org (2014-09-23)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-09-30)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-10-08)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-10-15)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### bo...@foxitsoftware.com (2014-10-22)

Fixed in https://pdfium.googlesource.com/pdfium/+/767aebbef641a89498deebc29369a078207b4dcc

### cl...@chromium.org (2014-10-22)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-10-30)

[Empty comment from Monorail migration]

### am...@chromium.org (2014-10-31)

merge approved for m39 branch 2171.  please ensure this is merged by nov 3 - if this will be problematic please e-mail me.

### bo...@foxitsoftware.com (2014-10-31)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-11-03)

Dev/Bug owner, please merge to M-39 branch 2171 asap. We need all these security fixes to go into the first stable.

### in...@chromium.org (2014-11-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-11-05)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-11-17)

Thanks for the report! It qualified for a $1000 reward.

### ti...@google.com (2014-12-08)

Payment in progress

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### ti...@google.com (2014-12-22)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-01-28)

Bulk update: removing view restriction from closed bugs.

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

This issue was migrated from crbug.com/chromium/414504?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080475)*
