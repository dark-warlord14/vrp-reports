# Heap-buffer-overflow in opj_tcd_init_decode_tile

| Field | Value |
|-------|-------|
| **Issue ID** | [40080817](https://issues.chromium.org/issues/40080817) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | cl...@gmail.com |
| **Assignee** | bo...@foxitsoftware.com |
| **Created** | 2014-11-07 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

The attached testcase crashes a 32-bit ASAN build of pdfium\_test with ASAN\_OPTIONS="allocator\_may\_return\_null=1" as follows:

# ERROR in tgt\_create while allocating node of the tree WARNING: No incltree created. ERROR in tgt\_create while allocating node of the tree WARNING: No imsbtree created.

==31474==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xf2a03d00 at pc 0x087e3970 bp 0xffb32128 sp 0xffb32120  

READ of size 4 at 0xf2a03d00 thread T0  

#0 0x87e396f in opj\_tcd\_init\_decode\_tile (/home/nils/PdfFarmer/Pdfium20141107/pdfium\_test+0x87e396f)  

#1 0x878d44f in opj\_j2k\_read\_tile\_header (/home/nils/PdfFarmer/Pdfium20141107/pdfium\_test+0x878d44f)  

#2 0x87b3bbe in opj\_j2k\_decode\_tiles (/home/nils/PdfFarmer/Pdfium20141107/pdfium\_test+0x87b3bbe)  

#3 0x878b42e in opj\_j2k\_exec (/home/nils/PdfFarmer/Pdfium20141107/pdfium\_test+0x878b42e)  

#4 0x87990a6 in opj\_j2k\_decode (/home/nils/PdfFarmer/Pdfium20141107/pdfium\_test+0x87990a6)  

#5 0x856aeb1 in opj\_jp2\_decode (/home/nils/PdfFarmer/Pdfium20141107/pdfium\_test+0x856aeb1)  

#6 0x8564029 in opj\_decode (/home/nils/PdfFarmer/Pdfium20141107/pdfium\_test+0x8564029)  

#7 0x8557604 in CJPX\_Decoder::Init(unsigned char const\*, int) (/home/nils/PdfFarmer/Pdfium20141107/pdfium\_test+0x8557604)  

#8 0x8559c81 in CCodec\_JpxModule::CreateDecoder(unsigned char const\*, unsigned int, int) (/home/nils/PdfFarmer/Pdfium20141107/pdfium\_test+0x8559c81)  

#9 0x8456be7 in CPDF\_DIBSource::LoadJpxBitmap() (/home/nils/PdfFarmer/Pdfium20141107/pdfium\_test+0x8456be7)  

#10 0x844f0c8 in CPDF\_DIBSource::CreateDecoder() (/home/nils/PdfFarmer/Pdfium20141107/pdfium\_test+0x844f0c8)  

#11 0x844912d in CPDF\_DIBSource::StartLoadDIBSource(CPDF\_Document\*, CPDF\_Stream const\*, int, CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int) (/home/nils/PdfFarmer/Pdfium20141107/pdfium\_test+0x844912d)  

#12 0x842c53b in CPDF\_ImageCache::StartGetCachedBitmap(CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) (/home/nils/PdfFarmer/Pdfium20141107/pdfium\_test+0x842c53b)  

#13 0x842bf78 in CPDF\_PageRenderCache::StartGetCachedBitmap(CPDF\_Stream\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) (/home/nils/PdfFarmer/Pdfium20141107/pdfium\_test+0x842bf78)  

#14 0x8465df9 in CPDF\_ProgressiveImageLoaderHandle::Start(CPDF\_ImageLoader\*, CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) (/home/nils/PdfFarmer/Pdfium20141107/pdfium\_test+0x8465df9)  

#15 0x84672df in CPDF\_ImageLoader::StartLoadImage(CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, void\*&, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) (/home/nils/PdfFarmer/Pdfium20141107/pdfium\_test+0x84672df)  

#16 0x84362e2 in CPDF\_ImageRenderer::StartLoadDIBSource() (/home/nils/PdfFarmer/Pdfium20141107/pdfium\_test+0x84362e2)  

#17 0x8430527 in CPDF\_ImageRenderer::Start(CPDF\_RenderStatus\*, CPDF\_PageObject const\*, CFX\_Matrix const\*, int, int) (/home/nils/PdfFarmer/Pdfium20141107/pdfium\_test+0x8430527)  

#18 0x8416ad7 in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject const\*, CFX\_Matrix const\*, IFX\_Pause\*) (/home/nils/PdfFarmer/Pdfium20141107/pdfium\_test+0x8416ad7)  

#19 0x8424f8d in CPDF\_ProgressiveRenderer::Continue(IFX\_Pause\*) (/home/nils/PdfFarmer/Pdfium20141107/pdfium\_test+0x8424f8d)  

#20 0x8423da9 in CPDF\_ProgressiveRenderer::Start(CPDF\_RenderContext\*, CFX\_RenderDevice\*, CPDF\_RenderOptions const\*, IFX\_Pause\*, int) (/home/nils/PdfFarmer/Pdfium20141107/pdfium\_test+0x8423da9)  

#21 0x811de99 in FPDF\_RenderPage\_Retail(CRenderContext\*, void\*, int, int, int, int, int, int, int, IFSDK\_PAUSE\_Adapter\*) (/home/nils/PdfFarmer/Pdfium20141107/pdfium\_test+0x811de99)  

#22 0x811e808 in FPDF\_RenderPageBitmap (/home/nils/PdfFarmer/Pdfium20141107/pdfium\_test+0x811e808)  

#23 0x8113e62 in RenderPdf(char const\*, char const\*, unsigned int, OutputFormat) (/home/nils/PdfFarmer/Pdfium20141107/pdfium\_test+0x8113e62)  

#24 0x8114e43 in main (/home/nils/PdfFarmer/Pdfium20141107/pdfium\_test+0x8114e43)  

#25 0xf746ba82 (/lib/i386-linux-gnu/libc.so.6+0x19a82)  

#26 0x807caff in \_start (/home/nils/PdfFarmer/Pdfium20141107/pdfium\_test+0x807caff)

0xf2a03d00 is located 0 bytes to the right of 7168-byte region [0xf2a02100,0xf2a03d00)  

allocated by thread T0 here:  

#0 0x80f0a5b in \_\_interceptor\_malloc /home/bobthebuilder/llvm/llvm/projects/compiler-rt/lib/asan/asan\_malloc\_linux.cc:40:3  

#1 0x87e1e2d in opj\_tcd\_init\_decode\_tile (/home/nils/PdfFarmer/Pdfium20141107/pdfium\_test+0x87e1e2d)

SUMMARY: AddressSanitizer: heap-buffer-overflow ??:0 opj\_tcd\_init\_decode\_tile  

Shadow bytes around the buggy address:  

0x3e540750: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x3e540760: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x3e540770: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x3e540780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x3e540790: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x3e5407a0:[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3e5407b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3e5407c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3e5407d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3e5407e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3e5407f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

==31474==ABORTING

The 64 bit ASAN build always crashes on an ASAN CHECK, even with ASAN\_OPTIONS="allocator\_may\_return\_null=1"

==913==AddressSanitizer CHECK failed: /work/chromium/src/third\_party/llvm/compiler-rt/lib/sanitizer\_common/sanitizer\_posix.cc:121 "(("unable to mmap" && 0)) != (0)" (0x0, 0x0)

Which potentially masks issues as it doesn't reflect the behaviour of a real world allocator.

**VERSION**  

Chrome Version: latest pdfium\_test

**REPRODUCTION CASE**  

Attached as repro.pdf

## Attachments

- [repro.pdf](attachments/repro.pdf) (application/pdf, 1.3 KB)

## Timeline

### cl...@chromium.org (2014-11-07)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4763774396399616

### in...@chromium.org (2014-11-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-07)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4763774396399616

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_v8_arm

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0xd338fd00
Crash State:
  opj_tcd_init_decode_tile
  opj_j2k_read_tile_header
  opj_j2k_decode_tiles
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=299683:299847

Minimized Testcase (1.34 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97jLDhY5LUHoBEVn3DyXTcA-MkD9gD7c6zIejNfzPGWEBTGFcOXp5mAAFl2tmaDWWd_AH7XESnR6d9I2DDBcc-KE28Xr1cd21lVReD_49dh-Y9SdV-NtS0upUEaPxJ3Ki4lSk400SLJi7Gp8aFkzNLlLR_wvA



### cl...@chromium.org (2014-11-08)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-11-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-11)

[Empty comment from Monorail migration]

### bo...@foxitsoftware.com (2014-11-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-21)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### bo...@foxitsoftware.com (2014-11-24)

Fixed in https://pdfium.googlesource.com/pdfium/+/4643533ca3dabe945fd174caf892a3ccb6cf2fd6

### cl...@chromium.org (2014-11-24)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-01)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4763774396399616

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_v8_arm

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0xd338fd00
Crash State:
  opj_tcd_init_decode_tile
  opj_j2k_read_tile_header
  opj_j2k_decode_tiles
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=299683:299847

Minimized Testcase (1.34 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94QjIAcno6dD3TkPwuU6fxsZMGruoe4zD35cu5mZJWR1Kjf7hQfTsFAxuWlCflDsEAZ2aXEidgF4xmcVhcaZB5JqUT2KDWdw248tV9d5t4z8R9C4FxMvx0OR26ZS_LXQUuWv0AXVwe5u4RYzCJKVEnqrEFVqQ



### in...@chromium.org (2014-12-15)

[Empty comment from Monorail migration]

### ma...@google.com (2014-12-15)

[Automated comment] No bugdroid (commit) comments found, couldn't auto-approve, needs manual review.

### [Deleted User] (2014-12-15)

Approved for 40.

### bu...@chromium.org (2014-12-16)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=65928

------------------------------------------------------------------
r65928 | thestig@google.com | 2014-12-16T06:55:04.676426Z

-----------------------------------------------------------------

### cl...@chromium.org (2014-12-16)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4763774396399616

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_v8_arm

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0xd338fd00
Crash State:
  opj_tcd_init_decode_tile
  opj_j2k_read_tile_header
  opj_j2k_decode_tiles
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=299683:299847

Minimized Testcase (1.34 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96RrKVhz4E6ZZoRwOsPV7xqOKsHk95y5imrcxjTlY75GahxudrPLwue7pu2enXW1e0dgf7uXycVhAHSZhPVx22TfMCcJCQIwqoIfCGCRRLyolovLD12vjtGm39RbsffVlK1bAo0QtCMT06MUo-UmTDwGc2h9g



### cl...@chromium.org (2014-12-16)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4763774396399616

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_v8_arm

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0xd338fd00
Crash State:
  opj_tcd_init_decode_tile
  opj_j2k_read_tile_header
  opj_j2k_decode_tiles
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=299683:299847

Minimized Testcase (1.34 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96RrKVhz4E6ZZoRwOsPV7xqOKsHk95y5imrcxjTlY75GahxudrPLwue7pu2enXW1e0dgf7uXycVhAHSZhPVx22TfMCcJCQIwqoIfCGCRRLyolovLD12vjtGm39RbsffVlK1bAo0QtCMT06MUo-UmTDwGc2h9g



### cl...@chromium.org (2014-12-17)

ClusterFuzz has detected this issue as fixed in range 307685:308589.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4763774396399616

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_v8_arm

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0xd338fd00
Crash State:
  opj_tcd_init_decode_tile
  opj_j2k_read_tile_header
  opj_j2k_decode_tiles
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=299683:299847
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=307685:308589

Minimized Testcase (1.34 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96RrKVhz4E6ZZoRwOsPV7xqOKsHk95y5imrcxjTlY75GahxudrPLwue7pu2enXW1e0dgf7uXycVhAHSZhPVx22TfMCcJCQIwqoIfCGCRRLyolovLD12vjtGm39RbsffVlK1bAo0QtCMT06MUo-UmTDwGc2h9g

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ti...@google.com (2015-01-22)

$500 for this report.

### cl...@chromium.org (2015-03-02)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-07)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### in...@chromium.org (2015-04-13)

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

This issue was migrated from crbug.com/chromium/431288?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/437747]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080817)*
