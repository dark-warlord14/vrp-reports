# Security: pdfium heap buffer overflow in cfx_dibbase.cpp

| Field | Value |
|-------|-------|
| **Issue ID** | [40057422](https://issues.chromium.org/issues/40057422) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2021-09-27 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**

Heap buffer overflow in cfx\_dibbase.cpp.

Memcpy source offset at cfx\_dibbase.cpp:644 is computed as rect.left \* GetBppFromFormat(m\_Format) / 8.  

In the repro pdf a MediaBox causes rect.left to be (int)134217120 with GetBppFromFormat(m\_Format) being 32. This makes rect.left \* 32 negative and the memcpy source 2432 bytes before allocated buffer.

By modifying the MediaBox size in the repro PDF the memcpy source can be tuned down to -268435456 bytes.

Examples:  

MediaBox[-134217124 0 600 4], offset -2432  

MediaBox[-67108862 0 600 4], offset -268435456

**VERSION**  

Version: nightly build asan-linux-release-925225

**REPRODUCTION CASE**

asan-linux-release-925225: pdfium\_test off\_by\_2432.pdf

=================================================================  

==25646==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7f73616eae80 at pc 0x561b89177757 bp 0x7ffd0bdbaef0 sp 0x7ffd0bdba6b8  

READ of size 56 at 0x7f73616eae80 thread T0  

==25646==WARNING: invalid path to external symbolizer!  

==25646==WARNING: Failed to use and restart external symbolizer!  

#0 0x561b89177756 in **asan\_memcpy /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_interceptors\_memintrinsics.cpp:22:3  

#1 0x561b896fb5fa in CFX\_DIBBase::Clone(FX\_RECT const\*) const ./../../third\_party/pdfium/core/fxge/dib/cfx\_dibbase.cpp:646:7  

#2 0x561b8975b47a in pdfium::CFX\_AggDeviceDriver::GetDIBits(fxcrt::RetainPtr<CFX\_DIBitmap> const&, int, int) ./../../third\_party/pdfium/core/fxge/agg/fx\_agg\_driver.cpp:1331:24  

#3 0x561b896ed2d0 in GetDIBits ./../../third\_party/pdfium/core/fxge/cfx\_renderdevice.cpp:885:27  

#4 0x561b896ed2d0 in CFX\_RenderDevice::DrawNormalText(int, TextCharPos const\*, CFX\_Font\*, float, CFX\_Matrix const&, unsigned int, CFX\_TextRenderOptions const&) ./../../third\_party/pdfium/core/fxge/cfx\_renderdevice.cpp:1167:10  

#5 0x561b89bae4ea in CPDF\_TextRenderer::DrawNormalText(CFX\_RenderDevice\*, pdfium::span<unsigned int const>, pdfium::span<float const>, CPDF\_Font\*, float, CFX\_Matrix const&, unsigned int, CPDF\_RenderOptions const&) ./../../third\_party/pdfium/core/fpdfapi/render/cpdf\_textrenderer.cpp:166:17  

#6 0x561b89b94efb in CPDF\_RenderStatus::ProcessText(CPDF\_TextObject\*, CFX\_Matrix const&, CFX\_Path\*) ./../../third\_party/pdfium/core/fpdfapi/render/cpdf\_renderstatus.cpp:902:10  

#7 0x561b89b92eb9 in CPDF\_RenderStatus::ProcessObjectNoClip(CPDF\_PageObject\*, CFX\_Matrix const&) ./../../third\_party/pdfium/core/fpdfapi/render/cpdf\_renderstatus.cpp:308:14  

#8 0x561b89b934b8 in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject\*, CFX\_Matrix const&, PauseIndicatorIface\*) ./../../third\_party/pdfium/core/fpdfapi/render/cpdf\_renderstatus.cpp:277:5  

#9 0x561b89b7b49a in CPDF\_ProgressiveRenderer::Continue(PauseIndicatorIface\*) ./../../third\_party/pdfium/core/fpdfapi/render/cpdf\_progressiverenderer.cpp:88:30  

#10 0x561b89220db5 in (anonymous namespace)::RenderPageImpl(CPDF\_PageRenderContext\*, CPDF\_Page\*, CFX\_Matrix const&, FX\_RECT const&, int, FPDF\_COLORSCHEME* const\*, bool, CPDFSDK\_PauseAdapter\*) ./../../third\_party/pdfium/fpdfsdk/cpdfsdk\_renderpage.cpp:81:26  

#11 0x561b89221186 in CPDFSDK\_RenderPageWithContext(CPDF\_PageRenderContext\*, CPDF\_Page\*, int, int, int, int, int, int, FPDF\_COLORSCHEME* const\*, bool, CPDFSDK\_PauseAdapter\*) ./../../third\_party/pdfium/fpdfsdk/cpdfsdk\_renderpage.cpp:110:3  

#12 0x561b89236b5d in FPDF\_RenderPageBitmapWithColorScheme\_Start ./../../third\_party/pdfium/fpdfsdk/fpdf\_progressive.cpp:73:3  

#13 0x561b891aec31 in ProcessPage ./../../third\_party/pdfium/samples/pdfium\_test.cc:799:16  

#14 0x561b891aec31 in ProcessPdf ./../../third\_party/pdfium/samples/pdfium\_test.cc:1034:9  

#15 0x561b891aec31 in main ./../../third\_party/pdfium/samples/pdfium\_test.cc:1282:5  

#16 0x7f73ea95ab96 in \_\_libc\_start\_main /build/glibc-2ORdQG/glibc-2.27/csu/../csu/libc-start.c:310:0

0x7f73616eae80 is located 2432 bytes to the left of 2147483524-byte region [0x7f73616eb800,0x7f73e16eb784)  

allocated by thread T0 here:  

#0 0x561b891784e2 in \_\_interceptor\_calloc /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cpp:138:3  

#1 0x561b8970d71e in CFX\_DIBitmap::Create(int, int, FXDIB\_Format, unsigned char\*, unsigned int) ./../../third\_party/pdfium/core/fxge/dib/cfx\_dibitmap.cpp:55:9  

#2 0x561b8923a841 in FPDFBitmap\_Create ./../../third\_party/pdfium/fpdfsdk/fpdf\_view.cpp:807:17  

#3 0x561b891ae8f8 in ProcessPage ./../../third\_party/pdfium/samples/pdfium\_test.cc:775:27  

#4 0x561b891ae8f8 in ProcessPdf ./../../third\_party/pdfium/samples/pdfium\_test.cc:1034:9  

#5 0x561b891ae8f8 in main ./../../third\_party/pdfium/samples/pdfium\_test.cc:1282:5  

#6 0x7f73ea95ab96 in \_\_libc\_start\_main /build/glibc-2ORdQG/glibc-2.27/csu/../csu/libc-start.c:310:0

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/dalanath/chrome/asan-linux-release-925225/pdfium\_test+0x12e3756)  

Shadow bytes around the buggy address:  

0x0feeec2d5580: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0feeec2d5590: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0feeec2d55a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0feeec2d55b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0feeec2d55c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x0feeec2d55d0:[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0feeec2d55e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0feeec2d55f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0feeec2d5600: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0feeec2d5610: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0feeec2d5620: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

==25646==ABORTING

**CREDIT INFORMATION**  

Antti Levomäki, Joonas Pihlaja and Christian Jalio from Forcepoint

## Attachments

- [off_by_2432.pdf](attachments/off_by_2432.pdf) (application/pdf, 152 B)
- [asan.trace](attachments/asan.trace) (application/octet-stream, 5.5 KB)

## Timeline

### [Deleted User] (2021-09-27)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-09-27)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2021-09-27)

Nice find, Christian. Lei, do we know if the spec puts any limits on the range of these values? 

### aj...@google.com (2021-09-27)

[Empty comment from Monorail migration]

### th...@chromium.org (2021-09-27)

re: https://crbug.com/chromium/1253399#c3 - There are some page size limits mentioned on https://www.adobe.com/content/dam/acom/en/devnet/pdf/pdfs/PDF32000_2008.pdf#page=658

Though per discussion on https://crbug.com/chromium/1204306, we'd like to avoid placing too many limits within PDFium.

### gi...@appspot.gserviceaccount.com (2021-09-27)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/a8b293732a0160d1bc1d5b0ad5744922f0f820d5

commit a8b293732a0160d1bc1d5b0ad5744922f0f820d5
Author: Tom Sepez <tsepez@chromium.org>
Date: Mon Sep 27 23:53:04 2021

Use more safe arithmetic in CFX_DIBBase

Most of the calculations are "safe" because we know that the DIB
has validated sizes before allocating a buffer, and that calculations
in terms of bytes won't overflow and will be within the buffer. But
calculations in terms of bits might create overflow in temporaries,
so use safe arithmetic there instead.

Re-arranging the order of operations thus converting to bytes first
might be one option, but we want to handle the 1 bpp case.

Test would require large images that might not be possible on
all platforms.

Bug: chromium:1253399
Change-Id: I3c6c5b8b1f1bf3f429c7d377a8a84c5ab53cafd9
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/85510
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/a8b293732a0160d1bc1d5b0ad5744922f0f820d5/core/fxge/dib/cfx_dibbase.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/a8b293732a0160d1bc1d5b0ad5744922f0f820d5/core/fxge/dib/cfx_bitmapcomposer.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/a8b293732a0160d1bc1d5b0ad5744922f0f820d5/core/fxge/dib/cfx_dibitmap.cpp


### [Deleted User] (2021-09-28)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ts...@chromium.org (2021-09-28)

FoundIn-94 is the oldest extended stable at the moment, though the issue goes back to before the beginning, it would seem.

### [Deleted User] (2021-09-28)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d54a58a34f3e3466d821f992859c5d7ff118093a

commit d54a58a34f3e3466d821f992859c5d7ff118093a
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Sep 28 23:27:23 2021

Roll PDFium from 9df3eb753e5f to f10a598baf80 (5 revisions)

https://pdfium.googlesource.com/pdfium.git/+log/9df3eb753e5f..f10a598baf80

2021-09-28 thestig@chromium.org Consistently use Optional instead of pdfium::Optional.
2021-09-28 thestig@chromium.org Fix some build dependencies involving fxjs/cfx_v8.h.
2021-09-28 thestig@chromium.org Remove circular dependency between core/fxcrt and pdfium_base.
2021-09-28 tsepez@chromium.org Small cleanup of ScanlineDecoder methods
2021-09-27 tsepez@chromium.org Use more safe arithmetic in CFX_DIBBase

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To file a bug in PDFium: https://bugs.chromium.org/p/pdfium/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1253399
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: Id17e11dce302ce899345ef0723f2f4c6b3a2c8d7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3192226
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#926007}

[modify] https://crrev.com/d54a58a34f3e3466d821f992859c5d7ff118093a/DEPS


### ts...@chromium.org (2021-09-29)

Closing ... looks like labels requested in c9 are set.  We'll see if the bot thinks so, too.

### [Deleted User] (2021-09-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-29)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-29)

Requesting merge to stable M94 because latest trunk commit (926007) appears to be after stable branch point (911515).

Requesting merge to beta M95 because latest trunk commit (926007) appears to be after beta branch point (920003).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-29)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), None (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-29)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ts...@chromium.org (2021-09-29)

Answers to numbered questions
1. Security Issue
2. Only the three files in https://pdfium-review.googlesource.com/c/pdfium/+/85510 
3. Not yet, should roll out in next canary
4. Not a new feature
5. N/A
6. Verification not needed.

### am...@chromium.org (2021-10-04)

merge approved to M95, please merge to branch 4638 by EOD tomorrow, 5 October, presuming there are no concerns or other issues revealed from canary coverage 

### gi...@appspot.gserviceaccount.com (2021-10-05)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/839d18189fe31cf4c9416d1a745ef06bd2257982

commit 839d18189fe31cf4c9416d1a745ef06bd2257982
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Oct 05 05:14:42 2021

M95: Use more safe arithmetic in CFX_DIBBase

Most of the calculations are "safe" because we know that the DIB
has validated sizes before allocating a buffer, and that calculations
in terms of bytes won't overflow and will be within the buffer. But
calculations in terms of bits might create overflow in temporaries,
so use safe arithmetic there instead.

Re-arranging the order of operations thus converting to bytes first
might be one option, but we want to handle the 1 bpp case.

Test would require large images that might not be possible on
all platforms.

Bug: chromium:1253399
Change-Id: I3c6c5b8b1f1bf3f429c7d377a8a84c5ab53cafd9
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/85510
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>
(cherry picked from commit a8b293732a0160d1bc1d5b0ad5744922f0f820d5)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/85670
Reviewed-by: Daniel Hosseinian <dhoss@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/839d18189fe31cf4c9416d1a745ef06bd2257982/core/fxge/dib/cfx_dibbase.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/839d18189fe31cf4c9416d1a745ef06bd2257982/core/fxge/dib/cfx_bitmapcomposer.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/839d18189fe31cf4c9416d1a745ef06bd2257982/core/fxge/dib/cfx_dibitmap.cpp


### th...@chromium.org (2021-10-05)

Merged here: https://pdfium.googlesource.com/pdfium/+/839d18189fe31cf4c9416d1a745ef06bd2257982

### am...@google.com (2021-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-06)

Congratulations, the VRP Panel has decided to award you $7500 for this report. Nice finding and thank you for your efforts and reporting this issue to us! 

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-10-11)

please also merge to M94, branch 4606, by EOD Friday, 15 October so this fix can be included in the extended stable release next week; thank you! 

### sr...@google.com (2021-10-13)

Pls complete the merges to M94 asap as we would be releasing M94 to extended stable early next week.

### ts...@chromium.org (2021-10-14)

cherry-pick at https://pdfium-review.googlesource.com/c/pdfium/+/85950

### gi...@appspot.gserviceaccount.com (2021-10-14)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/8a822e28adea47068d423a25154b45bdba49f183

commit 8a822e28adea47068d423a25154b45bdba49f183
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu Oct 14 18:29:32 2021

M94: Use more safe arithmetic in CFX_DIBBase

Most of the calculations are "safe" because we know that the DIB
has validated sizes before allocating a buffer, and that calculations
in terms of bytes won't overflow and will be within the buffer. But
calculations in terms of bits might create overflow in temporaries,
so use safe arithmetic there instead.

Re-arranging the order of operations thus converting to bytes first
might be one option, but we want to handle the 1 bpp case.

Test would require large images that might not be possible on
all platforms.

Bug: chromium:1253399
Change-Id: I3c6c5b8b1f1bf3f429c7d377a8a84c5ab53cafd9
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/85510
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>
(cherry picked from commit a8b293732a0160d1bc1d5b0ad5744922f0f820d5)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/85950

[modify] https://pdfium.googlesource.com/pdfium/+/8a822e28adea47068d423a25154b45bdba49f183/core/fxge/dib/cfx_dibbase.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/8a822e28adea47068d423a25154b45bdba49f183/core/fxge/dib/cfx_bitmapcomposer.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/8a822e28adea47068d423a25154b45bdba49f183/core/fxge/dib/cfx_dibitmap.cpp


### am...@chromium.org (2021-10-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-19)

[Empty comment from Monorail migration]

### rz...@google.com (2021-10-20)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-10-21)

extended stable labeling test

### gi...@google.com (2021-10-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-10-28)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/8b91627a75266376e3ca7f8b0d6576fc486242a4

commit 8b91627a75266376e3ca7f8b0d6576fc486242a4
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu Oct 28 23:36:12 2021

[M90-LTS] Use more safe arithmetic in CFX_DIBBase

Most of the calculations are "safe" because we know that the DIB
has validated sizes before allocating a buffer, and that calculations
in terms of bytes won't overflow and will be within the buffer. But
calculations in terms of bits might create overflow in temporaries,
so use safe arithmetic there instead.

Re-arranging the order of operations thus converting to bytes first
might be one option, but we want to handle the 1 bpp case.

Test would require large images that might not be possible on
all platforms.

M90 merge issues:
  cfx_bitmapcomposer.cpp: conflicting includes, and conflicting
  declaration of dest_scan

Bug: chromium:1253399
Change-Id: I3c6c5b8b1f1bf3f429c7d377a8a84c5ab53cafd9
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/85510
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>
(cherry picked from commit a8b293732a0160d1bc1d5b0ad5744922f0f820d5)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/86230

[modify] https://pdfium.googlesource.com/pdfium/+/8b91627a75266376e3ca7f8b0d6576fc486242a4/core/fxge/dib/cfx_dibbase.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/8b91627a75266376e3ca7f8b0d6576fc486242a4/core/fxge/dib/cfx_bitmapcomposer.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/8b91627a75266376e3ca7f8b0d6576fc486242a4/core/fxge/dib/cfx_dibitmap.cpp


### rz...@google.com (2021-10-29)

[Empty comment from Monorail migration]

### am...@google.com (2021-11-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1253399?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057422)*
