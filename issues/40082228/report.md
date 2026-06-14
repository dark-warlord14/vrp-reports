# Heap-buffer-overflow in color_sycc_to_rgb

| Field | Value |
|-------|-------|
| **Issue ID** | [40082228](https://issues.chromium.org/issues/40082228) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ju...@foxitsoftware.com |
| **Created** | 2015-06-05 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

This issue was found by fuzzing jpeg2000 in pdfs against a 32-bit build of pdfium\_test

The attached file crashes pdfium\_test as follows:

# Rendering PDF file repro.pdf. Non-linearized path...

==18205==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xda0b4540 at pc 0x081f392b bp 0xffe4e178 sp 0xffe4e170  

READ of size 4 at 0xda0b4540 thread T0  

#0 0x81f392a in sycc420\_to\_rgb(opj\_image\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:290:42  

#1 0x81f13b0 in color\_sycc\_to\_rgb(opj\_image\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:332:9  

#2 0x81f5d48 in CJPX\_Decoder::Init(unsigned char const\*, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:686:9  

#3 0x81f8a08 in CCodec\_JpxModule::CreateDecoder(unsigned char const\*, unsigned int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:791:10  

#4 0x863bb2f in CPDF\_DIBSource::LoadJpxBitmap() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:635:21  

#5 0x8633d08 in CPDF\_DIBSource::CreateDecoder() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:595:9  

#6 0x862eb8c in CPDF\_DIBSource::StartLoadDIBSource(CPDF\_Document\*, CPDF\_Stream const\*, int, CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:329:15  

#7 0x8618427 in CPDF\_ImageCache::StartGetCachedBitmap(CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:293:15  

#8 0x8617ef7 in CPDF\_PageRenderCache::StartGetCachedBitmap(CPDF\_Stream\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:131:15  

#9 0x8649b38 in CPDF\_ProgressiveImageLoaderHandle::Start(CPDF\_ImageLoader\*, CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1440:15  

#10 0x864ac2c in CPDF\_ImageLoader::StartLoadImage(CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, void\*&, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1499:19  

#11 0x8620282 in CPDF\_ImageRenderer::StartLoadDIBSource() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:327:9  

#12 0x861a489 in CPDF\_ImageRenderer::Start(CPDF\_RenderStatus\*, CPDF\_PageObject const\*, CFX\_Matrix const\*, int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:453:9  

#13 0x8608b3e in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject const\*, CFX\_Matrix const\*, IFX\_Pause\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:335:14  

#14 0x86134b9 in CPDF\_ProgressiveRenderer::Continue(IFX\_Pause\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:1130:21  

#15 0x861260a in CPDF\_ProgressiveRenderer::Start(CPDF\_RenderContext\*, CFX\_RenderDevice\*, CPDF\_RenderOptions const\*, IFX\_Pause\*, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:1073:5  

#16 0x817110d in FPDF\_RenderPage\_Retail(CRenderContext\*, void\*, int, int, int, int, int, int, int, IFSDK\_PAUSE\_Adapter\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:737:2  

#17 0x8171c2d in FPDF\_RenderPageBitmap /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:527:2  

#18 0x812defd in RenderPdf(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::**1::allocator<char> > const&, char const\*, unsigned int, Options const&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:514:5  

#19 0x81302a8 in main /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:618:5  

#20 0xf6f3f72d in \_\_libc\_start\_main ??:0:0

0xda0b4540 is located 0 bytes to the right of 1912128-byte region [0xd9ee1800,0xda0b4540)  

allocated by thread T0 here:  

#0 0x8101eb9 in calloc ??:0:0  

#1 0x83be2c2 in opj\_j2k\_update\_image\_data /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:8042:58  

#2 0x83bd77a in opj\_j2k\_decode\_tiles /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:9482:23  

#3 0x83a464f in opj\_j2k\_exec /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:7318:41  

#4 0x83b3ad6 in opj\_j2k\_decode /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:9666:15  

#5 0x8205532 in opj\_jp2\_decode /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/jp2.c:1406:8  

#6 0x8200b2b in opj\_decode /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/openjpeg.c:412:10  

#7 0x81f5995 in CJPX\_Decoder::Init(unsigned char const\*, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:666:15  

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

#25 0xf6f3f72d in \_\_libc\_start\_main ??:0:0

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/nils/MonkeyChrome/asan-symbolized-v8-arm-linux-release-332881/pdfium\_test+0x81f392a)  

Shadow bytes around the buggy address:  

0x3b416850: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x3b416860: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x3b416870: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x3b416880: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x3b416890: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x3b4168a0: 00 00 00 00 00 00 00 00[fa]fa fa fa fa fa fa fa  

0x3b4168b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3b4168c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3b4168d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3b4168e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3b4168f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

==18205==ABORTING

**VERSION**  

Chrome Version: asan-symbolized-v8-arm-linux-release-332881

**REPRODUCTION CASE**  

Attached as repro.pdf

## Attachments

- [repro.pdf](attachments/repro.pdf) (application/pdf, 237.5 KB)

## Timeline

### cl...@chromium.org (2015-06-05)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5994374182207488

### cl...@chromium.org (2015-06-05)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5994374182207488

Uploader: ochang@google.com
Job Type: Linux_asan_pdfium

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x7f230c66e540
Crash State:
  color_sycc_to_rgb
  CJPX_Decoder::Init
  CCodec_JpxModule::CreateDecoder
  

Minimized Testcase (237.46 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96Mw82iCzZeWoh0qNbsyTgTQAsiwTqxKWuoIEeJ0iBARqXhUpVwcICGR7E_GZv3ALC2uZEqWob0xcTYk6KTX5X-i79OfoGl4m8mTjVqZxA3Hc_2X-HVifQaY3F0SjaWgd5OQk-VfULsI_PqGf6wxbE0NP5LFJGtcGNIfZs8CqX3zzvqCxk



### oc...@chromium.org (2015-06-05)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-07-01)

[Empty comment from Monorail migration]

### th...@chromium.org (2015-07-13)

Guessing this should be labeled M-44?

### th...@chromium.org (2015-09-08)

ochang: Since we own the PDFium code based, this shouldn't be ExternalDependency.

### cl...@chromium.org (2015-09-08)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### ju...@foxitsoftware.com (2015-09-09)

[Empty comment from Monorail migration]

### ju...@foxitsoftware.com (2015-09-14)

It's pending in https://codereview.chromium.org/1342683002/.

### cl...@chromium.org (2015-10-02)

[Empty comment from Monorail migration]

### th...@chromium.org (2015-10-09)

[Empty comment from Monorail migration]

### ju...@foxitsoftware.com (2015-10-09)

Fixed in https://pdfium.googlesource.com/pdfium/+/f1f19f1fff801c9970af627e050becc2f13f82e7 and https://pdfium.googlesource.com/pdfium/+/3ea79bbba24a1c0918ea42368e746097dab40663.

### cl...@chromium.org (2015-10-09)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### bu...@chromium.org (2015-10-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1ef74c77625095af2d15ef993859b93157750447

commit 1ef74c77625095af2d15ef993859b93157750447
Author: thestig <thestig@chromium.org>
Date: Fri Oct 09 22:22:20 2015

Roll PDFium a398ca6..3acb1ef

https://pdfium.googlesource.com/pdfium.git/+log/a398ca6..3acb1ef

BUG=497357,541323,514891
TBR=tsepez@chromium.org

Review URL: https://codereview.chromium.org/1403563002

Cr-Commit-Position: refs/heads/master@{#353405}

[modify] http://crrev.com/1ef74c77625095af2d15ef993859b93157750447/DEPS


### th...@chromium.org (2015-10-10)

I'll take care the merging on Monday.

### ti...@google.com (2015-10-10)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### ss...@google.com (2015-10-10)

Merge approved for M47 (branch 2526)

### ti...@google.com (2015-10-12)

Leaving Merge-Triage as a potential M-46 post stable merging candidate.

### ss...@google.com (2015-10-12)

Reminder to please go ahead and merge into M47. The merge into M47 has been approved.

### bu...@chromium.org (2015-10-13)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=79500

------------------------------------------------------------------
r79500 | thestig@google.com | 2015-10-13T00:47:19.614731Z

-----------------------------------------------------------------

### th...@chromium.org (2015-10-13)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-13)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### ti...@chromium.org (2015-10-15)

Merge approved for M46 stable refresh (branch 2490). Pls merge asap.

### bu...@chromium.org (2015-10-15)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=79571

------------------------------------------------------------------
r79571 | thestig@google.com | 2015-10-15T02:58:33.332885Z

-----------------------------------------------------------------

### th...@chromium.org (2015-11-05)

[Empty comment from Monorail migration]

### ti...@google.com (2015-11-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-15)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2016-04-22)

Our panel decided on $1,000 for this report.

Panel notes: It doesn't look like this can lead to a write. If you can demonstrate it does, we're happy to reassess the reward.

I'll add it to your other reports for the payment run.

### ti...@google.com (2016-04-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/497357?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/541325]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082228)*
