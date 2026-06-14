# UNKNOWN in libc.so.6

| Field | Value |
|-------|-------|
| **Issue ID** | [40080448](https://issues.chromium.org/issues/40080448) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | cl...@gmail.com |
| **Assignee** | bo...@foxitsoftware.com |
| **Created** | 2014-09-13 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached testcase crashes the asan build of pdfium test

# ASAN:SIGSEGV

==1589==ERROR: AddressSanitizer: SEGV on unknown address 0x7f3688ce92f0 (pc 0x7f368f5d20ce bp 0x7fff35ec1f70 sp 0x7fff35ec1708 T0)  

#0 0x7f368f5d20cd in **nss\_hosts\_lookup /build/buildd/eglibc-2.19/string/../sysdeps/x86\_64/multiarch/memcpy-ssse3-back.S:1260  

#1 0x490723 in **asan\_memcpy ??:0:0  

#2 0x736a30 in j2k\_read\_ppm\_v3 /b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:3714:17  

#3 0x753b19 in opj\_j2k\_read\_header\_procedure /b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:6993:23  

#4 0x73f051 in opj\_j2k\_exec /b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:7048:41  

#5 0x73ee4c in opj\_j2k\_read\_header /b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:6580:15  

#6 0x65bff6 in CJPX\_Decoder::Init(unsigned char const\*, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:608:10  

#7 0x65d8ff in CCodec\_JpxModule::CreateDecoder(unsigned char const\*, unsigned int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:764:10  

#8 0x5ee341 in CPDF\_DIBSource::LoadJpxBitmap() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:643:21  

#9 0x5ea460 in CPDF\_DIBSource::CreateDecoder() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:599:9  

#10 0x5e717c in CPDF\_DIBSource::StartLoadDIBSource(CPDF\_Document\*, CPDF\_Stream const\*, int, CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:335:15  

#11 0x5da2fd in CPDF\_ImageCache::StartGetCachedBitmap(CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:310:15  

#12 0x5da042 in CPDF\_PageRenderCache::StartGetCachedBitmap(CPDF\_Stream\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:131:15  

#13 0x5f565f in CPDF\_ProgressiveImageLoaderHandle::Start(CPDF\_ImageLoader\*, CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1489:15  

#14 0x5f605f in CPDF\_ImageLoader::StartLoadImage(CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, void\*&, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1549:19  

#15 0x5dea08 in CPDF\_ImageRenderer::StartLoadDIBSource() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:371:9  

#16 0x5db46b in CPDF\_ImageRenderer::Start(CPDF\_RenderStatus\*, CPDF\_PageObject const\*, CFX\_Matrix const\*, int, int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:525:9  

#17 0x5d13d4 in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject const\*, CFX\_Matrix const\*, IFX\_Pause\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:350:14  

#18 0x5d784d in CPDF\_ProgressiveRenderer::Continue(IFX\_Pause\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:1175:21  

#19 0x4c9fd0 in FPDF\_RenderPage\_Retail(CRenderContext\*, void\*, int, int, int, int, int, int, int, IFSDK\_PAUSE\_Adapter\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:772:2  

#20 0x4ca280 in FPDF\_RenderPageBitmap /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:574:2  

#21 0x4c5e55 in RenderPdf(char const\*, char const\*, unsigned long, OutputFormat) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:324:5  

#22 0x4c6879 in main /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:406:7  

#23 0x7f368f4a1ec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287  

#24 0x4c51cc in \_start ??:0:0

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: SEGV ??:0 ??  

==1589==ABORTING

**VERSION**  

Chrome Version: latest asan build of pdfium\_test

**REPRODUCTION CASE**  

Attached in repro.pdf

## Attachments

- [repro.pdf](attachments/repro.pdf) (application/pdf, 276.9 KB)

## Timeline

### cl...@chromium.org (2014-09-14)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6728695185145856

### aa...@google.com (2014-09-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-14)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6728695185145856

Uploader: aarya@google.com
Job Type: Linux_asan_pdfium

Crash Type: UNKNOWN
Crash Address: 0x7fb00069f2f0
Crash State:
  libc.so.6
  j2k_read_ppm_v3
  opj_j2k_read_header_procedure
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=289356:289512

Minimized Testcase (276.92 Kb): https://cluster-fuzz.appspot.com/download/AMIfv947FV6npdvFMvbLlVgo94jy0kI_t0RT5od4Pq5D6HAQJIwnmuKeh0Tgdx7tOtsKEiIAseq_HzYkn1X77i3NuxA-FY1CILaJ4MedzgaycjOwkBwLiGuwaf0EkLSNSu6sNyGJrlRl3XVpm2Xy1n7-pDMSa84pY0nnC1WiWP7UWDQWF3bhm30



### ts...@chromium.org (2014-09-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-09-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-09-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-09-17)

+cc Libopenjpeg devs.

Antonin, Mathieu - can you please take a look at these libopenjpeg high severity security vulnerabilities asap. Feel free to port them to libopenjpeg bug tracker provided you can restrict view them [should not be open to public].

### in...@chromium.org (2014-09-19)

+cc m.darbois

Bo, Jun, what is the easy way to extract the image bits from pdf. Can you please attach them to these 11 bugs.

### cl...@chromium.org (2014-09-22)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### [Deleted User] (2014-09-25)

Punting to 39, feel free to merge request back to 38 if a fix is available.

### cl...@chromium.org (2014-09-29)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-10-07)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-10-14)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-10-22)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-10-29)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### bo...@foxitsoftware.com (2014-10-30)

Fixed in https://pdfium.googlesource.com/pdfium/+/2b327f83ffcceca1911479c4afddafe51f0e37ba

### am...@google.com (2014-10-30)

Is there a merge required here?

### cl...@chromium.org (2014-10-30)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-11-05)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-11-17)

Thanks for the report! This one qualified for a $2000 reward.

### ti...@google.com (2014-12-08)

Payment in progress

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-12-15)

[Empty comment from Monorail migration]

### ma...@google.com (2014-12-15)

[Automated comment] No bugdroid (commit) comments found, couldn't auto-approve, needs manual review.

### [Deleted User] (2014-12-15)

Approved for 40.

### th...@chromium.org (2014-12-17)

I'll merge this today.

### ti...@google.com (2014-12-22)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### in...@chromium.org (2015-01-02)

Please merges these fixes to M40 (branch: 2214) asap. The branch will be cut soon for M40 release.

### th...@chromium.org (2015-01-07)

Two weeks ago, I did the merge here: https://codereview.chromium.org/788983004 and rolled DEPS for M40 here: https://chromereviews.googleplex.com/135797013 so we should be all set.

### in...@chromium.org (2015-01-07)

Thanks!

### cl...@chromium.org (2015-02-06)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/414036?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080448)*
