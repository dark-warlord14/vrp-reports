# Heap-buffer-overflow in opj_j2k_tcp_destroy

| Field | Value |
|-------|-------|
| **Issue ID** | [40080808](https://issues.chromium.org/issues/40080808) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ju...@foxitsoftware.com |
| **Created** | 2014-11-06 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached testcase crashes the latest pdfium\_test ASAN build while reading a pointer as follows:

=================================================================  

==2828==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x61200000b710 at pc 0x0000007303a8 bp 0x7fffb5ad47b0 sp 0x7fffb5ad47a8  

READ of size 8 at 0x61200000b710 thread T0  

#0 0x7303a7 in opj\_j2k\_tcp\_destroy ??:0:0  

#1 0x72f4b7 in opj\_j2k\_destroy ??:0:0  

#2 0x6552af in opj\_jp2\_destroy ??:0:0  

#3 0x650db6 in opj\_destroy\_codec ??:0:0  

#4 0x64a973 in CJPX\_Decoder::~CJPX\_Decoder() ??:0:0  

#5 0x64c7f9 in CCodec\_JpxModule::CreateDecoder(unsigned char const\*, unsigned int, int) ??:0:0  

#6 0x5d8621 in CPDF\_DIBSource::LoadJpxBitmap() ??:0:0  

#7 0x5d428b in CPDF\_DIBSource::CreateDecoder() ??:0:0  

#8 0x5d10f8 in CPDF\_DIBSource::StartLoadDIBSource(CPDF\_Document\*, CPDF\_Stream const\*, int, CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int) ??:0:0  

#9 0x5c3add in CPDF\_ImageCache::StartGetCachedBitmap(CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) ??:0:0  

#10 0x5c3803 in CPDF\_PageRenderCache::StartGetCachedBitmap(CPDF\_Stream\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) ??:0:0  

#11 0x5e0210 in CPDF\_ProgressiveImageLoaderHandle::Start(CPDF\_ImageLoader\*, CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) ??:0:0  

#12 0x5e0c33 in CPDF\_ImageLoader::StartLoadImage(CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, void\*&, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) ??:0:0  

#13 0x5c8499 in CPDF\_ImageRenderer::StartLoadDIBSource() ??:0:0  

#14 0x5c4c6d in CPDF\_ImageRenderer::Start(CPDF\_RenderStatus\*, CPDF\_PageObject const\*, CFX\_Matrix const\*, int, int) ??:0:0  

#15 0x5ba906 in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject const\*, CFX\_Matrix const\*, IFX\_Pause\*) ??:0:0  

#16 0x5c0e35 in CPDF\_ProgressiveRenderer::Continue(IFX\_Pause\*) ??:0:0  

#17 0x4ac6c8 in FPDF\_RenderPage\_Retail(CRenderContext\*, void\*, int, int, int, int, int, int, int, IFSDK\_PAUSE\_Adapter\*) ??:0:0  

#18 0x4aca60 in FPDF\_RenderPageBitmap ??:0:0  

#19 0x4a84e5 in RenderPdf(char const\*, char const\*, unsigned long, OutputFormat) ??:0:0  

#20 0x4a8f99 in main /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:406:7  

#21 0x7fe1d23ccec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

0x61200000b710 is located 16 bytes to the right of 320-byte region [0x61200000b5c0,0x61200000b700)  

allocated by thread T0 here:  

#0 0x48b130 in \_*interceptor\_calloc ??:0:0  

#1 0x72a706 in opj\_j2k\_read\_siz ??:0:0  

#2 0x73bfd0 in opj\_j2k\_read\_header\_procedure ??:0:0  

#3 0x72fba1 in opj\_j2k\_exec ??:0:0  

#4 0x72f99c in opj\_j2k\_read\_header ??:0:0  

#5 0x64adbe in CJPX\_Decoder::Init(unsigned char const\*, int) ??:0:0  

#6 0x64c7e0 in CCodec\_JpxModule::CreateDecoder(unsigned char const\*, unsigned int, int) ??:0:0  

#7 0x5d8621 in CPDF\_DIBSource::LoadJpxBitmap() ??:0:0  

#8 0x5d428b in CPDF\_DIBSource::CreateDecoder() ??:0:0  

#9 0x5d10f8 in CPDF\_DIBSource::StartLoadDIBSource(CPDF\_Document\*, CPDF\_Stream const\*, int, CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int) ??:0:0  

#10 0x5c3add in CPDF\_ImageCache::StartGetCachedBitmap(CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) ??:0:0  

#11 0x5c3803 in CPDF\_PageRenderCache::StartGetCachedBitmap(CPDF\_Stream\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) ??:0:0  

#12 0x5e0210 in CPDF\_ProgressiveImageLoaderHandle::Start(CPDF\_ImageLoader\*, CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) ??:0:0  

#13 0x5e0c33 in CPDF\_ImageLoader::StartLoadImage(CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, void\*&, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) ??:0:0  

#14 0x5c8499 in CPDF\_ImageRenderer::StartLoadDIBSource() ??:0:0  

#15 0x5c4c6d in CPDF\_ImageRenderer::Start(CPDF\_RenderStatus\*, CPDF\_PageObject const\*, CFX\_Matrix const\*, int, int) ??:0:0  

#16 0x5ba906 in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject const\*, CFX\_Matrix const\*, IFX\_Pause\*) ??:0:0  

#17 0x5c0e35 in CPDF\_ProgressiveRenderer::Continue(IFX\_Pause\*) ??:0:0  

#18 0x4ac6c8 in FPDF\_RenderPage\_Retail(CRenderContext\*, void\*, int, int, int, int, int, int, int, IFSDK\_PAUSE\_Adapter\*) ??:0:0  

#19 0x4aca60 in FPDF\_RenderPageBitmap ??:0:0  

#20 0x4a84e5 in RenderPdf(char const\*, char const\*, unsigned long, OutputFormat) ??:0:0  

#21 0x4a8f99 in main /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:406:7  

#22 0x7fe1d23ccec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

SUMMARY: AddressSanitizer: heap-buffer-overflow ??:0 ??  

Shadow bytes around the buggy address:  

0x0c247fff9690: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c247fff96a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c247fff96b0: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x0c247fff96c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c247fff96d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x0c247fff96e0: fa fa[fa]fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x0c247fff96f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c247fff9700: 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa  

0x0c247fff9710: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x0c247fff9720: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c247fff9730: 00 00 00 00 00 00 00 00 00 00 fa fa fa fa fa fa  

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

==2828==ABORTING

**VERSION**  

Chrome Version: asan-symbolized-linux-release-302976  

Operating System: Linux 64-bit

**REPRODUCTION CASE**  

Attached as repro.pdf

## Attachments

- [repro.pdf](attachments/repro.pdf) (application/pdf, 5.7 KB)

## Timeline

### cl...@chromium.org (2014-11-06)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5724506806026240

### in...@chromium.org (2014-11-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-06)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5724506806026240

Uploader: aarya@google.com
Job Type: Linux_asan_pdfium

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x61300000d590
Crash State:
  opj_j2k_tcp_destroy
  opj_j2k_destroy
  opj_jp2_destroy
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=281908:281997

Minimized Testcase (5.74 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94M6Xqx60DMaovLDo1omvtPVa8tl6p6VhqxVaKgOEf7wteLmHe8_yuqWirhSpqfNcPJXcSZmQdOWdWRYJAZodHj3tTaXoU5zTGfnbiK_8LTjHWxz8S8FLMzLt42z1MFihhX_7mJDGq3Cz0CQLMLHR0pD_q_0A



### cl...@chromium.org (2014-11-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-09)

[Empty comment from Monorail migration]

### me...@chromium.org (2014-11-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-10)

[Empty comment from Monorail migration]

### bo...@foxitsoftware.com (2014-11-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-21)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-28)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-06)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-13)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-16)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5724506806026240

Uploader: aarya@google.com
Job Type: Linux_asan_pdfium

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x61300000d590
Crash State:
  opj_j2k_tcp_destroy
  opj_j2k_destroy
  opj_jp2_destroy
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=281908:281997

Minimized Testcase (5.74 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94M6Xqx60DMaovLDo1omvtPVa8tl6p6VhqxVaKgOEf7wteLmHe8_yuqWirhSpqfNcPJXcSZmQdOWdWRYJAZodHj3tTaXoU5zTGfnbiK_8LTjHWxz8S8FLMzLt42z1MFihhX_7mJDGq3Cz0CQLMLHR0pD_q_0A



### cl...@chromium.org (2014-12-18)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 34 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-19)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 35 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-01-02)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 49 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-01-07)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### in...@chromium.org (2015-01-07)

No more M39 patches, moving to M40.

### in...@chromium.org (2015-01-07)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-13)

[Empty comment from Monorail migration]

### bo...@foxitsoftware.com (2015-01-13)

[Empty comment from Monorail migration]

### bo...@foxitsoftware.com (2015-01-23)

Jun will be in charge of these issues.

### cl...@chromium.org (2015-02-13)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5724506806026240

Uploader: aarya@google.com
Job Type: Linux_asan_pdfium

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x61300000d590
Crash State:
  opj_j2k_tcp_destroy
  opj_j2k_destroy
  opj_jp2_destroy
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=281908:281997

Minimized Testcase (5.74 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94M6Xqx60DMaovLDo1omvtPVa8tl6p6VhqxVaKgOEf7wteLmHe8_yuqWirhSpqfNcPJXcSZmQdOWdWRYJAZodHj3tTaXoU5zTGfnbiK_8LTjHWxz8S8FLMzLt42z1MFihhX_7mJDGq3Cz0CQLMLHR0pD_q_0A



### cl...@chromium.org (2015-02-20)

[Empty comment from Monorail migration]

### ju...@foxitsoftware.com (2015-02-24)

It's an openjpeg issue. I raised a bug and provided a patch in http://code.google.com/p/openjpeg/issues/detail?id=477. 

### in...@chromium.org (2015-02-24)

ah! public bug. Openjpeg devs, can you please mark these and any other similar security bugs private.

### ju...@foxitsoftware.com (2015-03-15)

It's fixed in https://pdfium.googlesource.com/pdfium/+/ec61a859344dc6d2a60e4cbcd1555e6d317f2add.

### cl...@chromium.org (2015-03-15)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-03-25)

ClusterFuzz has detected this issue as fixed in range 321780:322012.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5724506806026240

Uploader: aarya@google.com
Job Type: Linux_asan_pdfium

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x61300000d590
Crash State:
  opj_j2k_tcp_destroy
  opj_j2k_destroy
  opj_jp2_destroy
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=281908:281997
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=321780:322012

Minimized Testcase (5.74 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94M6Xqx60DMaovLDo1omvtPVa8tl6p6VhqxVaKgOEf7wteLmHe8_yuqWirhSpqfNcPJXcSZmQdOWdWRYJAZodHj3tTaXoU5zTGfnbiK_8LTjHWxz8S8FLMzLt42z1MFihhX_7mJDGq3Cz0CQLMLHR0pD_q_0A

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ti...@google.com (2015-04-08)

Fix is huge - best to roll in with M43.

### ti...@google.com (2015-04-14)

Congrats - another $2000 for this one.

### ti...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### ti...@google.com (2015-06-03)

Processing via our *new* e-payment system should only take a 7-10 days and the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-06-21)

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

This issue was migrated from crbug.com/chromium/430891?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/467350]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080808)*
