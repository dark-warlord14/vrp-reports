# Pdfium heap-buffer-overflow in sycc422_to_rgb

| Field | Value |
|-------|-------|
| **Issue ID** | [40083208](https://issues.chromium.org/issues/40083208) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **CVE IDs** | CVE-2016-1619 |
| **Reporter** | ke...@gmail.com |
| **Assignee** | oc...@chromium.org |
| **Created** | 2015-11-17 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

With a PDF file containing a malformed JPEG2000 image, it is possible to cause an out-of-bounds read in the openjpeg library used in pdfium.  

The code in question, shortened for brevity (from fx\_codec\_jpx\_opj.cpp:216):

for (i = 0; i < maxh; ++i) {  

for (j = 0; (OPJ\_UINT32)j < (maxw & ~(OPJ\_UINT32)1); j += 2) {  

sycc\_to\_rgb(offset, upb, \*y, \*cb, \*cr, r, g, b);

```
	<<SNIP>>  
	++cr;  
}  

```

}  

The ASAN failure says: heap-buffer-overflow on address 0x7f00c6b6404c . The dereferencing of cr is the offending instruction. Without ASAN, the loop continues to read from outside the heap-buffer.  

(gdb) p cr  

$9 = (const int \*) 0x7f00c6b6404c

ASAN report (top 10 frames):

==18448==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7f00c6b6404c at pc 0x00000056947c bp 0x7fff85ade6d0 sp 0x7fff85ade6c8  

READ of size 4 at 0x7f00c6b6404c thread T0  

#0 0x56947b in sycc422\_to\_rgb third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:217:36  

#1 0x56947b in color\_sycc\_to\_rgb(opj\_image\*) third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:416  

#2 0x569c8e in CJPX\_Decoder::Init(unsigned char const\*, int) third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:757:5  

#3 0x56afe6 in CCodec\_JpxModule::CreateDecoder(unsigned char const\*, unsigned int, int) third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.  

cpp:870:8  

#4 0x8848dd in context third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:75:28  

#5 0x8848dd in CPDF\_DIBSource::LoadJpxBitmap() third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:709  

#6 0x87fb95 in CPDF\_DIBSource::CreateDecoder() third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:655:5  

#7 0x87c45b in CPDF\_DIBSource::StartLoadDIBSource(CPDF\_Document\*, CPDF\_Stream const\*, int, CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, i  

nt) third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:371:13  

#8 0x86cfad in CPDF\_ImageCache::StartGetCachedBitmap(CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) thir  

d\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:308:7  

#9 0x86cc51 in CPDF\_PageRenderCache::StartGetCachedBitmap(CPDF\_Stream\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) third\_party/pdfium/co  

re/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:143:13  

#10 0x88cf8d in CPDF\_ProgressiveImageLoaderHandle::Start(CPDF\_ImageLoader\*, CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, int, unsigned int, int,  

CPDF\_RenderStatus\*, int, int) third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1559:11

0x7f00c6b6404c is located 0 bytes to the right of 8656972-byte region [0x7f00c6322800,0x7f00c6b6404c)  

allocated by thread T0 here:  

#0 0x4adc74 in \_\_interceptor\_calloc (/home/keve/src/chromium/asan-linux-stable-46.0.2490.86/pdfium\_test+0x4adc74)  

#1 0x6c24c5 in opj\_j2k\_update\_image\_data third\_party/pdfium/third\_party/libopenjpeg20/j2k.c:8157:57  

#2 0x6c1ea8 in opj\_j2k\_decode\_tiles third\_party/pdfium/third\_party/libopenjpeg20/j2k.c:9603:23  

#3 0x6b36a7 in opj\_j2k\_exec third\_party/pdfium/third\_party/libopenjpeg20/j2k.c:7286:41  

#4 0x6b36a7 in opj\_j2k\_decode third\_party/pdfium/third\_party/libopenjpeg20/j2k.c:9796  

#5 0x6c7019 in opj\_jp2\_decode third\_party/pdfium/third\_party/libopenjpeg20/jp2.c:1483:8  

#6 0x569ada in CJPX\_Decoder::Init(unsigned char const\*, int) third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:736:11  

#7 0x56afe6 in CCodec\_JpxModule::CreateDecoder(unsigned char const\*, unsigned int, int) third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.  

cpp:870:8  

#8 0x8848dd in context third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:75:28  

#9 0x8848dd in CPDF\_DIBSource::LoadJpxBitmap() third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:709  

#10 0x87fb95 in CPDF\_DIBSource::CreateDecoder() third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:655:5

**VERSION**  

pdfium\_test from asan-linux-stable-46.0.2490.86

**REPRODUCTION CASE**  

Attached file crashes pdfium\_test on linux 64-bit.

## Attachments

- [cr.pdf](attachments/cr.pdf) (application/pdf, 1.8 KB)

## Timeline

### cl...@chromium.org (2015-11-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6512736541868032

### wf...@chromium.org (2015-11-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-17)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6512736541868032

Uploader: wfh@chromium.org
Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x7fe64ad7004c
Crash State:
  color_sycc_to_rgb
  CJPX_Decoder::Init
  CCodec_JpxModule::CreateDecoder
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=299683:299856

Minimized Testcase (1.80 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95rpKmIUA4UvW-ESy9DlhWhESf8V4jRyB_lbmuBhJRcRlNVG9xOtfeoT46tetf3S8kyPrNTl7mU2cFbAVeZ0jI_j74pYPdCbp77UGtbPwZL0OSCiXldA2TTgyOYC1bwf7grBx6Gjx9A0TkhE_7sdZ305RUsQQ

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### wf...@chromium.org (2015-11-17)

[Empty comment from Monorail migration]

### th...@chromium.org (2015-11-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-12-02)

jun_fang@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### oc...@chromium.org (2015-12-10)

Patch out for review: https://codereview.chromium.org/1512833008

### oc...@chromium.org (2015-12-11)

Fixed in https://pdfium.googlesource.com/pdfium/+/08750d0400f1635ac33c3234cb11b192f31a1eeb.

### cl...@chromium.org (2015-12-11)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### bu...@chromium.org (2015-12-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ae8a013d59e8216f3fb67b6a458070212ac603c1

commit ae8a013d59e8216f3fb67b6a458070212ac603c1
Author: thestig <thestig@chromium.org>
Date: Sat Dec 12 04:45:47 2015

Roll PDFium 94edf0c..ebc7695

https://pdfium.googlesource.com/pdfium.git/+log/94edf0c..ebc7695

BUG=554129,557223,569271
TBR=ochang@chromium.org

Review URL: https://codereview.chromium.org/1515263004

Cr-Commit-Position: refs/heads/master@{#364909}

[modify] http://crrev.com/ae8a013d59e8216f3fb67b6a458070212ac603c1/DEPS


### th...@chromium.org (2015-12-12)

[Empty comment from Monorail migration]

### ti...@google.com (2015-12-12)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### cl...@chromium.org (2015-12-14)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6512736541868032

Uploader: wfh@chromium.org
Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x7fe64ad7004c
Crash State:
  color_sycc_to_rgb
  CJPX_Decoder::Init
  CCodec_JpxModule::CreateDecoder
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=299683:299856

Minimized Testcase (1.80 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95rpKmIUA4UvW-ESy9DlhWhESf8V4jRyB_lbmuBhJRcRlNVG9xOtfeoT46tetf3S8kyPrNTl7mU2cFbAVeZ0jI_j74pYPdCbp77UGtbPwZL0OSCiXldA2TTgyOYC1bwf7grBx6Gjx9A0TkhE_7sdZ305RUsQQ

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2015-12-15)

ClusterFuzz has detected this issue as fixed in range 364779:365132.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6512736541868032

Uploader: wfh@chromium.org
Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x7fe64ad7004c
Crash State:
  color_sycc_to_rgb
  CJPX_Decoder::Init
  CCodec_JpxModule::CreateDecoder
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=299683:299856
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=364779:365132

Minimized Testcase (1.80 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95rpKmIUA4UvW-ESy9DlhWhESf8V4jRyB_lbmuBhJRcRlNVG9xOtfeoT46tetf3S8kyPrNTl7mU2cFbAVeZ0jI_j74pYPdCbp77UGtbPwZL0OSCiXldA2TTgyOYC1bwf7grBx6Gjx9A0TkhE_7sdZ305RUsQQ

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### ti...@google.com (2015-12-16)

Merge approved for M48 (branch 2564). Pls go ahead merge.

### bu...@chromium.org (2015-12-17)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=82047

------------------------------------------------------------------
r82047 | ochang@google.com | 2015-12-17T00:06:56.292216Z

-----------------------------------------------------------------

### ti...@google.com (2016-01-19)

[Empty comment from Monorail migration]

### ti...@google.com (2016-01-20)

Hi Keve - our reward panel reviewed this issue and decided to award you $500 for bringing this issue to our attention. 

Notes from reward panel: Not a high severity issue, appears to be just a read/info leak. Reward would be significantly higher if more than a read.

We'll list your name in the Chrome release notes as "Keve Nagy". If you'd like me to update it to another name, please let me know.

Someone from our finance team should be in contact within 7 days to collect some details for payment. If that doesn't happen, please either update the bug or contact me at timwillis@

I'll update this bug shortly with a CVE ID for your records. Thanks again for helping secure chrome and happy bug hunting!

### ti...@google.com (2016-01-20)

[Empty comment from Monorail migration]

### ti...@google.com (2016-01-20)

CVE-2016-1619

### ti...@google.com (2016-02-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-03-18)

This security bug has been closed for more than 14 weeks. Removing view restrictions.

For more details visit https://sites.google.com/a/chromium.org/dev/issue-tracking/autotriage - Your friendly Sheriffbot

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

This issue was migrated from crbug.com/chromium/557223?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083208)*
