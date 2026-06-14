# Heap-double-free in j2k_read_ppm_v3

| Field | Value |
|-------|-------|
| **Issue ID** | [40082226](https://issues.chromium.org/issues/40082226) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ju...@foxitsoftware.com |
| **Created** | 2015-06-05 |
| **Bounty** | $3,000.00 |

## Description

attempting double-free in j2k\_read\_ppm\_v3

**VULNERABILITY DETAILS**  

This issue was found by fuzzing jpeg2000 in pdfs against a 32-bit build of pdfium\_test

The attached file crashes pdfium\_test as follows:

# Rendering PDF file repro.pdf. Non-linearized path...

==14084==ERROR: AddressSanitizer: attempting double-free on 0xe1602f50 in thread T0:  

#0 0x81019c3 in **interceptor\_free ??:0:0  

#1 0x839d61f in j2k\_read\_ppm\_v3 /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:3735:33  

#2 0x83b9d4a in opj\_j2k\_read\_header\_procedure /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:7250:23  

#3 0x83a464f in opj\_j2k\_exec /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:7318:41  

#4 0x83a419c in opj\_j2k\_read\_header /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:6813:15  

#5 0x8209a09 in opj\_jp2\_read\_header /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/jp2.c:2522:9  

#6 0x8200957 in opj\_read\_header /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/openjpeg.c:391:10  

#7 0x81f5713 in CJPX\_Decoder::Init(unsigned char const\*, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:648:10  

#8 0x81f8a08 in CCodec\_JpxModule::CreateDecoder(unsigned char const\*, unsigned int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:791:10  

#9 0x863bb2f in CPDF\_DIBSource::LoadJpxBitmap() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:635:21  

#10 0x8633d08 in CPDF\_DIBSource::CreateDecoder() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:595:9  

#11 0x862eb8c in CPDF\_DIBSource::StartLoadDIBSource(CPDF\_Document\*, CPDF\_Stream const\*, int, CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:329:15  

#12 0x8618427 in CPDF\_ImageCache::StartGetCachedBitmap(CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:293:15  

#13 0x8617ef7 in CPDF\_PageRenderCache::StartGetCachedBitmap(CPDF\_Stream\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:131:15  

#14 0x8649b38 in CPDF\_ProgressiveImageLoaderHandle::Start(CPDF\_ImageLoader\*, CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1440:15  

#15 0x864ac2c in CPDF\_ImageLoader::StartLoadImage(CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, void\*&, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1499:19  

#16 0x8620282 in CPDF\_ImageRenderer::StartLoadDIBSource() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:327:9  

#17 0x861a489 in CPDF\_ImageRenderer::Start(CPDF\_RenderStatus\*, CPDF\_PageObject const\*, CFX\_Matrix const\*, int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:453:9  

#18 0x8608b3e in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject const\*, CFX\_Matrix const\*, IFX\_Pause\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:335:14  

#19 0x86134b9 in CPDF\_ProgressiveRenderer::Continue(IFX\_Pause\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:1130:21  

#20 0x861260a in CPDF\_ProgressiveRenderer::Start(CPDF\_RenderContext\*, CFX\_RenderDevice\*, CPDF\_RenderOptions const\*, IFX\_Pause\*, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:1073:5  

#21 0x817110d in FPDF\_RenderPage\_Retail(CRenderContext\*, void\*, int, int, int, int, int, int, int, IFSDK\_PAUSE\_Adapter\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:737:2  

#22 0x8171c2d in FPDF\_RenderPageBitmap /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:527:2  

#23 0x812defd in RenderPdf(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::**1::allocator<char> > const&, char const\*, unsigned int, Options const&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:514:5  

#24 0x81302a8 in main /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:618:5  

#25 0xf6f4872d in \_\_libc\_start\_main ??:0:0

0xe1602f50 is located 0 bytes inside of 1-byte region [0xe1602f50,0xe1602f51)  

freed by thread T0 here:  

#0 0x81020c3 in realloc ??:0:0  

#1 0x839cf0e in j2k\_read\_ppm\_v3 /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:3733:53  

#2 0x83b9d4a in opj\_j2k\_read\_header\_procedure /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:7250:23  

#3 0x83a464f in opj\_j2k\_exec /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:7318:41  

#4 0x83a419c in opj\_j2k\_read\_header /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:6813:15  

#5 0x8209a09 in opj\_jp2\_read\_header /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/jp2.c:2522:9  

#6 0x8200957 in opj\_read\_header /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/openjpeg.c:391:10  

#7 0x81f5713 in CJPX\_Decoder::Init(unsigned char const\*, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:648:10  

#8 0x81f8a08 in CCodec\_JpxModule::CreateDecoder(unsigned char const\*, unsigned int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:791:10  

#9 0x863bb2f in CPDF\_DIBSource::LoadJpxBitmap() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:635:21  

#10 0x8633d08 in CPDF\_DIBSource::CreateDecoder() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:595:9  

#11 0x862eb8c in CPDF\_DIBSource::StartLoadDIBSource(CPDF\_Document\*, CPDF\_Stream const\*, int, CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:329:15  

#12 0x8618427 in CPDF\_ImageCache::StartGetCachedBitmap(CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:293:15  

#13 0x8617ef7 in CPDF\_PageRenderCache::StartGetCachedBitmap(CPDF\_Stream\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:131:15  

#14 0x8649b38 in CPDF\_ProgressiveImageLoaderHandle::Start(CPDF\_ImageLoader\*, CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1440:15  

#15 0x864ac2c in CPDF\_ImageLoader::StartLoadImage(CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, void\*&, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1499:19  

#16 0x8620282 in CPDF\_ImageRenderer::StartLoadDIBSource() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:327:9  

#17 0x861a489 in CPDF\_ImageRenderer::Start(CPDF\_RenderStatus\*, CPDF\_PageObject const\*, CFX\_Matrix const\*, int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:453:9  

#18 0x8608b3e in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject const\*, CFX\_Matrix const\*, IFX\_Pause\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:335:14  

#19 0x86134b9 in CPDF\_ProgressiveRenderer::Continue(IFX\_Pause\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:1130:21  

#20 0x861260a in CPDF\_ProgressiveRenderer::Start(CPDF\_RenderContext\*, CFX\_RenderDevice\*, CPDF\_RenderOptions const\*, IFX\_Pause\*, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:1073:5  

#21 0x817110d in FPDF\_RenderPage\_Retail(CRenderContext\*, void\*, int, int, int, int, int, int, int, IFSDK\_PAUSE\_Adapter\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:737:2  

#22 0x8171c2d in FPDF\_RenderPageBitmap /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:527:2  

#23 0x812defd in RenderPdf(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::**1::allocator<char> > const&, char const\*, unsigned int, Options const&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:514:5  

#24 0x81302a8 in main /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:618:5  

#25 0xf6f4872d in \_\_libc\_start\_main ??:0:0

previously allocated by thread T0 here:  

#0 0x81020c3 in realloc ??:0:0  

#1 0x839c82d in j2k\_read\_ppm\_v3 /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:3668:61  

#2 0x83b9d4a in opj\_j2k\_read\_header\_procedure /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:7250:23  

#3 0x83a464f in opj\_j2k\_exec /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:7318:41  

#4 0x83a419c in opj\_j2k\_read\_header /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:6813:15  

#5 0x8209a09 in opj\_jp2\_read\_header /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/jp2.c:2522:9  

#6 0x8200957 in opj\_read\_header /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/openjpeg.c:391:10  

#7 0x81f5713 in CJPX\_Decoder::Init(unsigned char const\*, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:648:10  

#8 0x81f8a08 in CCodec\_JpxModule::CreateDecoder(unsigned char const\*, unsigned int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:791:10  

#9 0x863bb2f in CPDF\_DIBSource::LoadJpxBitmap() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:635:21  

#10 0x8633d08 in CPDF\_DIBSource::CreateDecoder() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:595:9  

#11 0x862eb8c in CPDF\_DIBSource::StartLoadDIBSource(CPDF\_Document\*, CPDF\_Stream const\*, int, CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:329:15  

#12 0x8618427 in CPDF\_ImageCache::StartGetCachedBitmap(CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:293:15  

#13 0x8617ef7 in CPDF\_PageRenderCache::StartGetCachedBitmap(CPDF\_Stream\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:131:15  

#14 0x8649b38 in CPDF\_ProgressiveImageLoaderHandle::Start(CPDF\_ImageLoader\*, CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1440:15  

#15 0x864ac2c in CPDF\_ImageLoader::StartLoadImage(CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, void\*&, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1499:19  

#16 0x8620282 in CPDF\_ImageRenderer::StartLoadDIBSource() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:327:9  

#17 0x861a489 in CPDF\_ImageRenderer::Start(CPDF\_RenderStatus\*, CPDF\_PageObject const\*, CFX\_Matrix const\*, int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:453:9  

#18 0x8608b3e in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject const\*, CFX\_Matrix const\*, IFX\_Pause\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:335:14  

#19 0x86134b9 in CPDF\_ProgressiveRenderer::Continue(IFX\_Pause\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:1130:21  

#20 0x861260a in CPDF\_ProgressiveRenderer::Start(CPDF\_RenderContext\*, CFX\_RenderDevice\*, CPDF\_RenderOptions const\*, IFX\_Pause\*, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:1073:5  

#21 0x817110d in FPDF\_RenderPage\_Retail(CRenderContext\*, void\*, int, int, int, int, int, int, int, IFSDK\_PAUSE\_Adapter\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:737:2  

#22 0x8171c2d in FPDF\_RenderPageBitmap /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:527:2  

#23 0x812defd in RenderPdf(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::**1::allocator<char> > const&, char const\*, unsigned int, Options const&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:514:5  

#24 0x81302a8 in main /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:618:5  

#25 0xf6f4872d in \_\_libc\_start\_main ??:0:0

SUMMARY: AddressSanitizer: double-free (/home/nils/MonkeyChrome/asan-symbolized-v8-arm-linux-release-332881/pdfium\_test+0x81019c3)  

==14084==ABORTING

**VERSION**  

Chrome Version: asan-symbolized-v8-arm-linux-release-332881

**REPRODUCTION CASE**  

Attached as repro.pdf

## Attachments

- [repro.pdf](attachments/repro.pdf) (application/pdf, 1.1 KB)

## Timeline

### cl...@chromium.org (2015-06-05)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6649075911360512

### oc...@chromium.org (2015-06-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-05)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6649075911360512

Uploader: ochang@google.com
Job Type: Linux_asan_pdfium

Crash Type: Heap-double-free
Crash Address: 0x6090000097d0
Crash State:
  j2k_read_ppm_v3
  opj_j2k_read_header_procedure
  opj_j2k_read_header
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=289356:289512

Minimized Testcase (1.07 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96qtFq8_aDLCMID_ApyPSZl9MOoX1UWeLRuh5ZVXJymsu4zIeB-otcZ3XAH5n-vhrkZnFPnJSn8emUMtRCrNsLqI0f9gcwMKZeUnoEJA2A3RA0XyQAquPynFcNIK6nnWpkZSZeMJirJcxOlmd1fN0uGfYqEeg



### in...@chromium.org (2015-07-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-07-02)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-07-02)

[Empty comment from Monorail migration]

### th...@chromium.org (2015-09-08)

ochang: (ditto) Since we own the PDFium code based, this shouldn't be ExternalDependency.

### cl...@chromium.org (2015-09-08)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### in...@chromium.org (2015-09-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-09-09)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6128543371624448

Fuzzer: aohelin_ni
Job Type: linux_asan_chrome_v8_arm
Platform Id: linux

Crash Type: Heap-double-free
Crash Address: 0xce31e680
Crash State:
  j2k_read_ppm_v3
  opj_j2k_read_header_procedure
  opj_j2k_read_header
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=341606:341714

Minimized Testcase (1.07 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94Ldd-s3J-qg3OAnAoUrQrJ77xuHRgKPxXnIRwWgs9F45x-4e53hwrAcJwi0phjyeIPAPIl0yD0_UPFnTn-m7xjp66aIqv0De5nVe9gHkwUG_fTS4uUhFwHcs_m2MgqglhowcCirJ_XFhgVXMyJIRTx_Z46Ng

Filer: inferno

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### th...@chromium.org (2015-09-09)

In j2k_read_ppm_v3(), |l_cp->ppm_len| and |l_N_ppm| are both 0. So realloc() is freeing the pointer and returning NULL as it should. Then the error handler frees it again. Upstream openjpeg completely refactored this function 2 months ago in https://github.com/uclouvain/openjpeg/commit/c887df12a38ff1a2721d0c8a93b74fe1d02701a2 so it looks like the problem does not exist there anymore.

BTW, we have a separate email thread discussing the status of the open PDFium security bugs. Hopefully we can resolve these soon.

### ju...@foxitsoftware.com (2015-09-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-02)

[Empty comment from Monorail migration]

### ju...@foxitsoftware.com (2015-10-13)

Fixed in https://pdfium.googlesource.com/pdfium/+/c212b684cb028a5d98e57f711c9eed931b853a44.

### cl...@chromium.org (2015-10-13)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### bu...@chromium.org (2015-10-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e7df2d7d0c7a185834722cea42589caefd44da96

commit e7df2d7d0c7a185834722cea42589caefd44da96
Author: thestig <thestig@chromium.org>
Date: Wed Oct 14 00:11:11 2015

Roll PDFium 3acb1ef..24c1eec

https://pdfium.googlesource.com/pdfium.git/+log/3acb1ef..24c1eec

BUG=457480,497355
TBR=tsepez@chromium.org

Review URL: https://codereview.chromium.org/1397173005

Cr-Commit-Position: refs/heads/master@{#353919}

[modify] http://crrev.com/e7df2d7d0c7a185834722cea42589caefd44da96/DEPS


### cl...@chromium.org (2015-10-14)

ClusterFuzz has detected this issue as fixed in range 353893:353966.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6649075911360512

Uploader: ochang@google.com
Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: Heap-double-free
Crash Address: 0x6090000097d0
Crash State:
  j2k_read_ppm_v3
  opj_j2k_read_header_procedure
  opj_j2k_read_header
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=289356:289512
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=353893:353966

Minimized Testcase (1.07 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96qtFq8_aDLCMID_ApyPSZl9MOoX1UWeLRuh5ZVXJymsu4zIeB-otcZ3XAH5n-vhrkZnFPnJSn8emUMtRCrNsLqI0f9gcwMKZeUnoEJA2A3RA0XyQAquPynFcNIK6nnWpkZSZeMJirJcxOlmd1fN0uGfYqEeg

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### th...@chromium.org (2015-10-14)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-14)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### ss...@google.com (2015-10-15)

Merge approved for M47 (branch 2526)

### bu...@chromium.org (2015-10-16)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=79611

------------------------------------------------------------------
r79611 | thestig@google.com | 2015-10-16T01:59:05.738658Z

-----------------------------------------------------------------

### th...@chromium.org (2015-10-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-16)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### ti...@chromium.org (2015-10-19)

Merge approved for M46 stable refresh (branch 2490). Pls merge asap.

### bu...@chromium.org (2015-10-19)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=79724

------------------------------------------------------------------
r79724 | thestig@google.com | 2015-10-19T23:17:35.296815Z

-----------------------------------------------------------------

### th...@chromium.org (2015-11-05)

[Empty comment from Monorail migration]

### ti...@google.com (2015-11-10)

[Empty comment from Monorail migration]

### ti...@google.com (2015-11-28)

Adding reward-topanel for consideration under the Chrome Reward Program. Details here: https://www.google.com/about/appsecurity/chrome-rewards/

### cl...@chromium.org (2016-01-19)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2016-04-22)

Congrats - $3,000 for this report.

### ti...@google.com (2016-04-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-06-09)

ClusterFuzz has detected this issue as fixed in range 353786:353966.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6128543371624448

Fuzzer: aohelin_ni
Job Type: linux_asan_chrome_v8_arm
Platform Id: linux

Crash Type: Heap-double-free
Crash Address: 0xce31e6b0
Crash State:
  j2k_read_ppm_v3
  opj_j2k_read_header_procedure
  opj_j2k_read_header
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=281908:281997
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=353786:353966

Minimized Testcase (1.07 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96DuDv8A3M0-efv6KYS8M2z67FY6_J4aRqvL1x_b_OrYdVnzwGV96E0s3hBP0YH_k3rKWq25CEQdAcBboClCtsN5Jh_juQRWwyhIhwVeKj0vxDHp31pdgF1_5c8xTI4PX8ylaeV8kb3vmFWPTc-kqGeUZwjoQ

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/497355?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/506637]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082226)*
