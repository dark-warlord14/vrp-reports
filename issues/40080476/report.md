# Heap-buffer-overflow in opj_dwt_decode

| Field | Value |
|-------|-------|
| **Issue ID** | [40080476](https://issues.chromium.org/issues/40080476) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | cl...@gmail.com |
| **Assignee** | bo...@foxitsoftware.com |
| **Created** | 2014-09-16 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached testcase crashes the latest asan build of pdfium\_test:

=================================================================  

==27481==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xf1d035d8 at pc 0x08720b00 bp 0xffdad8b8 sp 0xffdad8b0  

WRITE of size 4 at 0xf1d035d8 thread T0  

#0 0x8720aff in opj\_dwt\_interleave\_h /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/dwt.c:248:7 #1 0x8720aff in opj\_dwt\_decode\_tile /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/dwt.c:594:0 #2 0x8720aff in opj\_dwt\_decode /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/dwt.c:475:0  

#3 0x869a60f in opj\_tcd\_dwt\_decode /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/tcd.c:1558:31 #4 0x869a60f in opj\_tcd\_decode\_tile /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/tcd.c:1250:0  

#5 0x864e81f in opj\_j2k\_decode\_tile /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:7661:15  

#6 0x866c541 in opj\_j2k\_decode\_tiles /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:9177:23  

#7 0x8655f4e in opj\_j2k\_exec /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:7048:41 #8 0x8655f4e in opj\_j2k\_decode /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:9368:0  

#9 0x84886cc in opj\_decode /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/openjpeg.c:413:10  

#10 0x847c680 in CJPX\_Decoder::Init(unsigned char const\*, int) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:624:15  

#11 0x847ea08 in CCodec\_JpxModule::CreateDecoder(unsigned char const\*, unsigned int, int) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:764:10  

#12 0x83a350a in CPDF\_DIBSource::LoadJpxBitmap() /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:643:21  

#13 0x839c5ab in CPDF\_DIBSource::CreateDecoder() /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:599:9  

#14 0x83974e8 in CPDF\_DIBSource::StartLoadDIBSource(CPDF\_Document\*, CPDF\_Stream const\*, int, CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:335:15  

#15 0x837ffc9 in CPDF\_ImageCache::StartGetCachedBitmap(CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:310:15  

#16 0x837fa32 in CPDF\_PageRenderCache::StartGetCachedBitmap(CPDF\_Stream\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:131:15  

#17 0x83b06cb in CPDF\_ProgressiveImageLoaderHandle::Start(CPDF\_ImageLoader\*, CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1489:15  

#18 0x83b1919 in CPDF\_ImageLoader::StartLoadImage(CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, void\*&, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1549:19  

#19 0x838786a in CPDF\_ImageRenderer::StartLoadDIBSource() /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:371:9  

#20 0x8381f64 in CPDF\_ImageRenderer::Start(CPDF\_RenderStatus\*, CPDF\_PageObject const\*, CFX\_Matrix const\*, int, int) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:525:9  

#21 0x836eaae in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject const\*, CFX\_Matrix const\*, IFX\_Pause\*) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:350:14  

#22 0x837b028 in CPDF\_ProgressiveRenderer::Continue(IFX\_Pause\*) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:1175:21  

#23 0x8379f57 in CPDF\_ProgressiveRenderer::Start(CPDF\_RenderContext\*, CFX\_RenderDevice\*, CPDF\_RenderOptions const\*, IFX\_Pause\*, int) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:1114:5  

#24 0x811314b in FPDF\_RenderPage\_Retail(CRenderContext\*, void\*, int, int, int, int, int, int, int, IFSDK\_PAUSE\_Adapter\*) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:772:2  

#25 0x81139f8 in FPDF\_RenderPageBitmap /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:574:2  

#26 0x810e656 in RenderPdf(char const\*, char const\*, unsigned int, OutputFormat) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:324:5  

#27 0x810f3b4 in main /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:406:7  

#28 0xf7195a82 in \_\_libc\_start\_main ??:?  

#29 0x810d05b in \_start ??:0:0

0xf1d035d8 is located 4 bytes to the right of 404-byte region [0xf1d03440,0xf1d035d4)  

allocated by thread T0 here:  

#0 0x80ede21 in memalign *asan\_rtl*:3  

#1 0x871f654 in opj\_dwt\_decode\_tile /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/dwt.c:572:2 #2 0x871f654 in opj\_dwt\_decode /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/dwt.c:475:0  

#3 0x869a60f in opj\_tcd\_dwt\_decode /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/tcd.c:1558:31 #4 0x869a60f in opj\_tcd\_decode\_tile /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/tcd.c:1250:0  

#5 0x864e81f in opj\_j2k\_decode\_tile /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:7661:15  

#6 0x866c541 in opj\_j2k\_decode\_tiles /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:9177:23  

#7 0x8655f4e in opj\_j2k\_exec /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:7048:41 #8 0x8655f4e in opj\_j2k\_decode /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:9368:0  

#9 0x84886cc in opj\_decode /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/openjpeg.c:413:10  

#10 0x847c680 in CJPX\_Decoder::Init(unsigned char const\*, int) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:624:15  

#11 0x847ea08 in CCodec\_JpxModule::CreateDecoder(unsigned char const\*, unsigned int, int) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:764:10  

#12 0x83a350a in CPDF\_DIBSource::LoadJpxBitmap() /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:643:21  

#13 0x839c5ab in CPDF\_DIBSource::CreateDecoder() /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:599:9  

#14 0x83974e8 in CPDF\_DIBSource::StartLoadDIBSource(CPDF\_Document\*, CPDF\_Stream const\*, int, CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:335:15  

#15 0x837ffc9 in CPDF\_ImageCache::StartGetCachedBitmap(CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:310:15  

#16 0x837fa32 in CPDF\_PageRenderCache::StartGetCachedBitmap(CPDF\_Stream\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:131:15  

#17 0x83b06cb in CPDF\_ProgressiveImageLoaderHandle::Start(CPDF\_ImageLoader\*, CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1489:15  

#18 0x83b1919 in CPDF\_ImageLoader::StartLoadImage(CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, void\*&, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1549:19  

#19 0x838786a in CPDF\_ImageRenderer::StartLoadDIBSource() /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:371:9  

#20 0x8381f64 in CPDF\_ImageRenderer::Start(CPDF\_RenderStatus\*, CPDF\_PageObject const\*, CFX\_Matrix const\*, int, int) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:525:9  

#21 0x836eaae in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject const\*, CFX\_Matrix const\*, IFX\_Pause\*) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:350:14  

#22 0x837b028 in CPDF\_ProgressiveRenderer::Continue(IFX\_Pause\*) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:1175:21  

#23 0x8379f57 in CPDF\_ProgressiveRenderer::Start(CPDF\_RenderContext\*, CFX\_RenderDevice\*, CPDF\_RenderOptions const\*, IFX\_Pause\*, int) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:1114:5  

#24 0x811314b in FPDF\_RenderPage\_Retail(CRenderContext\*, void\*, int, int, int, int, int, int, int, IFSDK\_PAUSE\_Adapter\*) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:772:2  

#25 0x81139f8 in FPDF\_RenderPageBitmap /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:574:2  

#26 0x810e656 in RenderPdf(char const\*, char const\*, unsigned int, OutputFormat) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:324:5  

#27 0x810f3b4 in main /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:406:7  

#28 0xf7195a82 in \_\_libc\_start\_main ??:?

SUMMARY: AddressSanitizer: heap-buffer-overflow ??:0 ??  

Shadow bytes around the buggy address:  

0x3e3a0660: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3e3a0670: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3e3a0680: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x3e3a0690: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x3e3a06a0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x3e3a06b0: 00 00 00 00 00 00 00 00 00 00 04[fa]fa fa fa fa  

0x3e3a06c0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x3e3a06d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x3e3a06e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x3e3a06f0: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa  

0x3e3a0700: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

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

==27481==ABORTING

**VERSION**  

Chrome Version: latest asan build of pdfium\_test

**REPRODUCTION CASE**  

attached in repro.pdf

## Attachments

- [repro.pdf](attachments/repro.pdf) (application/pdf, 35.2 KB)

## Timeline

### in...@chromium.org (2014-09-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-16)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6035111419052032

### cl...@chromium.org (2014-09-16)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6035111419052032

Uploader: aarya@google.com
Job Type: Linux_asan_pdfium

Crash Type: Heap-buffer-overflow WRITE 4
Crash Address: 0x615000007f18
Crash State:
  opj_dwt_decode
  opj_tcd_decode_tile
  opj_j2k_decode_tile
  

Minimized Testcase (35.20 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97RDIh-12O0ywaud7A9-xwZKgs4RDlPbRvZpVkAtMjLs0dId6t7nuiJuYOXsPidIOMYvPq0eAJoiWL1XaiLv9ddP6Ud6FP3dzh_WSBCRslU_kD355I1q5EKovTiKC_NsmsuxUxiYcwjLDgCINuLVNK4lUk0wbA3oxWxnD6ELGZU-Wahw_Q



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

Fixed in https://pdfium.googlesource.com/pdfium/+/4dc95e74e1acc75f4eab08bc771874cd2a9c3a9b

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

Thanks for the report! It qualified for a $3000 reward.

### ti...@google.com (2014-12-08)

Payment in progress

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### ti...@google.com (2014-12-22)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-01-29)

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

This issue was migrated from crbug.com/chromium/414525?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080476)*
