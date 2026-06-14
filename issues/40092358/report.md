# Security: heap-buffer-overflow in CPDF_DIBSource::DownSampleScanline8Bit

| Field | Value |
|-------|-------|
| **Issue ID** | [40092358](https://issues.chromium.org/issues/40092358) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | zh...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2018-09-05 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

This issue was found by fuzzing against a 64-bit asan linux build of pdfium\_test.

**VERSION**  

Chrome Version: asan-linux-beta-69.0.3497.23  

Operating System: Fedora 28 x86\_64

**REPRODUCTION CASE**  

./pdfium\_test tests\_f0608b73459fbaa615f295ee9973f3af4e7821c5

# Rendering PDF file tests\_f0608b73459fbaa615f295ee9973f3af4e7821c5.

==26422==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7f24ede1e72a at pc 0x000002bdad75 bp 0x7ffcbae26ee0 sp 0x7ffcbae26ed8  

READ of size 1 at 0x7f24ede1e72a thread T0  

SCARINESS: 12 (1-byte-read-heap-buffer-overflow)  

#0 0x2bdad74 in CPDF\_DIBSource::DownSampleScanline8Bit(int, int, unsigned int, unsigned char const\*, unsigned char\*, int, bool, int, int) const third\_party/pdfium/core/fpdfapi/render/cpdf\_dibsource.cpp:1235:21  

#1 0x2bd9ec9 in CPDF\_DIBSource::DownSampleScanline(int, unsigned char\*, int, int, bool, int, int) const third\_party/pdfium/core/fpdfapi/render/cpdf\_dibsource.cpp:1116:5  

#2 0x2efa5b9 in CFX\_ImageStretcher::ContinueQuickStretch(PauseIndicatorIface\*) third\_party/pdfium/core/fxge/dib/cfx\_imagestretcher.cpp:208:16  

#3 0x2efc440 in CFX\_ImageTransformer::Continue(PauseIndicatorIface\*) third\_party/pdfium/core/fxge/dib/cfx\_imagetransformer.cpp:285:20  

#4 0x2ef3d98 in CFX\_ImageRenderer::Continue(PauseIndicatorIface\*) third\_party/pdfium/core/fxge/dib/cfx\_imagerenderer.cpp:95:23  

#5 0x2c1b72c in CPDF\_ImageRenderer::Continue(PauseIndicatorIface\*) third\_party/pdfium/core/fpdfapi/render/cpdf\_imagerenderer.cpp:546:48  

#6 0x2bee411 in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject\*, CFX\_Matrix const\*, PauseIndicatorIface\*) third\_party/pdfium/core/fpdfapi/render/cpdf\_renderstatus.cpp:1121:27  

#7 0x2be7394 in CPDF\_ProgressiveRenderer::Continue(PauseIndicatorIface\*) third\_party/pdfium/core/fpdfapi/render/cpdf\_progressiverenderer.cpp:93:30  

#8 0x28a8e15 in FPDF\_RenderPage\_Continue third\_party/pdfium/fpdfsdk/fpdf\_progressive.cpp:86:28  

#9 0xb8008a in RenderPage third\_party/pdfium/samples/pdfium\_test.cc:556:14  

#10 0xb8008a in RenderPdf third\_party/pdfium/samples/pdfium\_test.cc:757  

#11 0xb8008a in main third\_party/pdfium/samples/pdfium\_test.cc:924  

#12 0x7f24f593c11a in \_\_libc\_start\_main (/lib64/libc.so.6+0x2311a)  

#13 0xaa4029 in \_start (/home/henices/research/asan-linux-beta-69.0.3497.23/pdfium\_test+0xaa4029)

0x7f24ede1e72a is located 2 bytes to the right of 14417704-byte region [0x7f24ed05e800,0x7f24ede1e728)  

allocated by thread T0 here:  

#0 0xb4bd53 in **interceptor\_malloc /b/swarming/w/ir/kitchen-workdir/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cc:146:3  

#1 0x2ed4578 in PartitionAllocGenericFlags third\_party/pdfium/third\_party/base/allocator/partition\_allocator/partition\_alloc.h:796:18  

#2 0x2ed4578 in FX\_SafeAlloc third\_party/pdfium/core/fxcrt/fx\_memory.h:46  

#3 0x2ed4578 in CFX\_DIBitmap::Create(int, int, FXDIB\_Format, unsigned char\*, unsigned int) third\_party/pdfium/core/fxge/dib/cfx\_dibitmap.cpp:57  

#4 0x2bcec96 in CPDF\_DIBSource::CreateDecoder() third\_party/pdfium/core/fpdfapi/render/cpdf\_dibsource.cpp:464:27  

#5 0x2bd1842 in CPDF\_DIBSource::StartLoadDIBSource(CPDF\_Document\*, CPDF\_Stream const\*, bool, CPDF\_Dictionary const\*, CPDF\_Dictionary\*, bool, unsigned int, bool) third\_party/pdfium/core/fpdfapi/render/cpdf\_dibsource.cpp:263:31  

#6 0x2be513a in CPDF\_ImageCacheEntry::StartGetCachedBitmap(CPDF\_Dictionary const\*, CPDF\_Dictionary\*, bool, unsigned int, bool, CPDF\_RenderStatus\*) third\_party/pdfium/core/fpdfapi/render/cpdf\_imagecacheentry.cpp:72:42  

#7 0x2be0dc5 in CPDF\_PageRenderCache::StartGetCachedBitmap(fxcrt::RetainPtr<CPDF\_Image> const&, bool, unsigned int, bool, CPDF\_RenderStatus\*) third\_party/pdfium/core/fpdfapi/render/cpdf\_pagerendercache.cpp:97:58  

#8 0x2c1bfeb in CPDF\_ImageLoader::Start(CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, bool, unsigned int, bool, CPDF\_RenderStatus\*) third\_party/pdfium/core/fpdfapi/render/cpdf\_imageloader.cpp:34:19  

#9 0x2c12d3e in CPDF\_ImageRenderer::StartLoadDIBSource() third\_party/pdfium/core/fpdfapi/render/cpdf\_imagerenderer.cpp:62:16  

#10 0x2c19b8e in CPDF\_ImageRenderer::Start(CPDF\_RenderStatus\*, CPDF\_ImageObject\*, CFX\_Matrix const\*, bool, int) third\_party/pdfium/core/fpdfapi/render/cpdf\_imagerenderer.cpp:186:7  

#11 0x2bee382 in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject\*, CFX\_Matrix const\*, PauseIndicatorIface\*) third\_party/pdfium/core/fpdfapi/render/cpdf\_renderstatus.cpp:1146:26  

#12 0x2be7394 in CPDF\_ProgressiveRenderer::Continue(PauseIndicatorIface\*) third\_party/pdfium/core/fpdfapi/render/cpdf\_progressiverenderer.cpp:93:30  

#13 0x28ab692 in (anonymous namespace)::RenderPageImpl(CPDF\_PageRenderContext\*, CPDF\_Page\*, CFX\_Matrix const&, FX\_RECT const&, int, bool, IPDFSDK\_PauseAdapter\*) third\_party/pdfium/fpdfsdk/fpdf\_view.cpp:131:26  

#14 0x28ab03d in FPDF\_RenderPage\_Retail(CPDF\_PageRenderContext\*, fpdf\_page\_t**\*, int, int, int, int, int, int, bool, IPDFSDK\_PauseAdapter\*) third\_party/pdfium/fpdfsdk/fpdf\_view.cpp:915:3  

#15 0x28a8aaa in FPDF\_RenderPageBitmap\_Start third\_party/pdfium/fpdfsdk/fpdf\_progressive.cpp:60:3  

#16 0xb8006a in RenderPage third\_party/pdfium/samples/pdfium\_test.cc:553:16  

#17 0xb8006a in RenderPdf third\_party/pdfium/samples/pdfium\_test.cc:757  

#18 0xb8006a in main third\_party/pdfium/samples/pdfium\_test.cc:924  

#19 0x7f24f593c11a in \_\_libc\_start\_main (/lib64/libc.so.6+0x2311a)

SUMMARY: AddressSanitizer: heap-buffer-overflow third\_party/pdfium/core/fpdfapi/render/cpdf\_dibsource.cpp:1235:21 in CPDF\_DIBSource::DownSampleScanline8Bit(int, int, unsigned int, unsigned char const\*, unsigned char\*, int, bool, int, int) const  

Shadow bytes around the buggy address:  

0x0fe51dbbbc90: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fe51dbbbca0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fe51dbbbcb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fe51dbbbcc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fe51dbbbcd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x0fe51dbbbce0: 00 00 00 00 00[fa]fa fa fa fa fa fa fa fa fa fa  

0x0fe51dbbbcf0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0fe51dbbbd00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0fe51dbbbd10: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0fe51dbbbd20: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0fe51dbbbd30: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

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

Shadow gap: cc  

==26422==ABORTING

testcase is the attachment.

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### ts...@chromium.org (2018-09-05)

Repro'd on ToT.

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-09-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6321157396234240.

### cl...@chromium.org (2018-09-12)

Automatically assigning owner based on suspected regression changelist https://pdfium.googlesource.com/pdfium/+/cb391259aefd52f09352d35a1bb5b56c0db6db11 (Use checked large integer in ContinueQuickStretch).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2018-09-12)

Detailed report: https://clusterfuzz.com/testcase?key=6321157396234240

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x7f93e5efc728
Crash State:
  CPDF_DIBBase::DownSampleScanline8Bit
  CPDF_DIBBase::DownSampleScanline
  CFX_ImageStretcher::ContinueQuickStretch
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=556570:556575

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6321157396234240

See https://github.com/google/clusterfuzz-tools for more information.

### th...@chromium.org (2018-09-12)

https://pdfium.googlesource.com/pdfium/+/cb391259aefd52f09352d35a1bb5b56c0db6db11 "regressed" this by fixing the crazy math in ContinueQuickStretch(). Now it calculates the line number correctly, tries to go towards the last line, and goes out of bound.

### th...@chromium.org (2018-09-12)

I think what is causing the confusion is: /BitsPerComponent 8 vs. /ColorSpace /DeviceGray

### th...@chromium.org (2018-09-18)

Actually, that's not it. The real problem is the back filter pipeline. e.g. /Filter [/JBIG2Decode /DCTDecode] is the Unix equivalent of:

cat data | jbig2_decode | dct_decode, which makes no sense. Whereas:

cat data | gunzip | dct_decode

is a valid pipeline.

### th...@chromium.org (2018-09-18)

https://pdfium-review.googlesource.com/c/pdfium/+/42711

### bu...@chromium.org (2018-09-19)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/5f2ea0f6ef587f9f7a2fec9f80dbc82b94c97400

commit 5f2ea0f6ef587f9f7a2fec9f80dbc82b94c97400
Author: Lei Zhang <thestig@chromium.org>
Date: Wed Sep 19 17:26:34 2018

Validate decoder pipelines.

PDF decoders, AKA filters, can be chained together. There can be
an arbitrary number of decoding / decompressing filters in the pipeline,
but there should be at most 1 image decoder, and the image decoder
should only be at the end of the chain.

BUG=chromium:880675

Change-Id: Iffa27c70ec1ed7574e38e0de23413840ee900959
Reviewed-on: https://pdfium-review.googlesource.com/42711
Reviewed-by: Ryan Harrison <rharrison@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[modify] https://crrev.com/5f2ea0f6ef587f9f7a2fec9f80dbc82b94c97400/core/fpdfapi/parser/fpdf_parser_decode.h
[modify] https://crrev.com/5f2ea0f6ef587f9f7a2fec9f80dbc82b94c97400/core/fpdfapi/parser/fpdf_parser_decode.cpp
[modify] https://crrev.com/5f2ea0f6ef587f9f7a2fec9f80dbc82b94c97400/core/fpdfapi/parser/fpdf_parser_decode_unittest.cpp


### bu...@chromium.org (2018-09-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9f2aff260dd058c67ea3f974df1a8c3179997bed

commit 9f2aff260dd058c67ea3f974df1a8c3179997bed
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Sep 19 18:52:29 2018

Roll src/third_party/pdfium c3099d1c6942..174de19776de (2 commits)

https://pdfium.googlesource.com/pdfium.git/+log/c3099d1c6942..174de19776de


git log c3099d1c6942..174de19776de --date=short --no-merges --format='%ad %ae %s'
2018-09-19 thestig@chromium.org Encapsulate CPDF_ImageLoader.
2018-09-19 thestig@chromium.org Validate decoder pipelines.


Created with:
  gclient setdep -r src/third_party/pdfium@174de19776de

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:880675
TBR=dsinclair@chromium.org

Change-Id: I1af59ee6d0a3d3c21cce116d96083947b365ee31
Reviewed-on: https://chromium-review.googlesource.com/1234295
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#592495}
[modify] https://crrev.com/9f2aff260dd058c67ea3f974df1a8c3179997bed/DEPS


### cl...@chromium.org (2018-09-21)

ClusterFuzz has detected this issue as fixed in range 592493:592498.

Detailed report: https://clusterfuzz.com/testcase?key=6321157396234240

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x7f93e5efc728
Crash State:
  CPDF_DIBBase::DownSampleScanline8Bit
  CPDF_DIBBase::DownSampleScanline
  CFX_ImageStretcher::ContinueQuickStretch
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=556570:556575
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=592493:592498

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6321157396234240

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-09-21)

ClusterFuzz testcase 6321157396234240 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-09-21)

[Empty comment from Monorail migration]

### th...@chromium.org (2018-09-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-21)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), geohsu@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2018-09-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-09-21)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/0004bd334b0c485b2e4ece0bfae8812c7f107a0d

commit 0004bd334b0c485b2e4ece0bfae8812c7f107a0d
Author: Lei Zhang <thestig@chromium.org>
Date: Fri Sep 21 21:29:38 2018

M70: Validate decoder pipelines.

PDF decoders, AKA filters, can be chained together. There can be
an arbitrary number of decoding / decompressing filters in the pipeline,
but there should be at most 1 image decoder, and the image decoder
should only be at the end of the chain.

BUG=chromium:880675
TBR=tsepez@chromium.org

Change-Id: Iffa27c70ec1ed7574e38e0de23413840ee900959
Reviewed-on: https://pdfium-review.googlesource.com/42711
Reviewed-by: Ryan Harrison <rharrison@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>
(cherry picked from commit 5f2ea0f6ef587f9f7a2fec9f80dbc82b94c97400)
Reviewed-on: https://pdfium-review.googlesource.com/42970
Reviewed-by: Lei Zhang <thestig@chromium.org>

[modify] https://crrev.com/0004bd334b0c485b2e4ece0bfae8812c7f107a0d/core/fpdfapi/parser/fpdf_parser_decode.h
[modify] https://crrev.com/0004bd334b0c485b2e4ece0bfae8812c7f107a0d/core/fpdfapi/parser/fpdf_parser_decode.cpp
[modify] https://crrev.com/0004bd334b0c485b2e4ece0bfae8812c7f107a0d/core/fpdfapi/parser/fpdf_parser_decode_unittest.cpp


### aw...@chromium.org (2018-09-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-09-28)

Thanks zhouzhenster@! The VRP panel decided to award $1,000 for this report. (And just a reminder about http://g.co/ChromeBugRewards#fuzzerprogram if you've got a fuzzer that we could run on your behalf!)

### aw...@chromium.org (2018-09-28)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-12-28)

This issue was migrated from crbug.com/chromium/880675?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092358)*
