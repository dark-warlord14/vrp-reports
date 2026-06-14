# Security: Invalid read. SEGV on CXFA_Radial::Draw.

| Field | Value |
|-------|-------|
| **Issue ID** | [40094199](https://issues.chromium.org/issues/40094199) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-03-04 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Invalid read. SEGV on CXFA\_Radial::Draw.

**VERSION**  

commit 3b55bdf8dc4c1d795bb66216a7ebcc421e490a55 (HEAD -> master, origin/master, origin/HEAD)  

Date: Sat Mar 2 03:36:59 2019 +0000

**REPRODUCTION CASE**  

Open attached file.

# ADDITIONAL INFORMATION Rendering PDF file victory\_9ddc1135b11176c1a7efd033f23cecf9812a4f580b87cf94683689f0e40ad56e.pdf. AddressSanitizer:DEADLYSIGNAL

==6418==ERROR: AddressSanitizer: SEGV on unknown address 0x7ffdf3cef060 (pc 0x55555961e5c7 bp 0x7fffffffd430 sp 0x7fffffffd2a0 T0)  

==6418==The signal is caused by a READ memory access.  

#0 0x55555961e5c6 in CXFA\_Graphics::FillPathWithShading(CXFA\_GEPath const\*, int, CFX\_Matrix const&) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxgraphics/cxfa\_graphics.cpp:377  

#1 0x55555961e5c6 in ?? ??:0  

#2 0x55555961c1a8 in CXFA\_Graphics::RenderDeviceFillPath(CXFA\_GEPath const\*, int, CFX\_Matrix const\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxgraphics/cxfa\_graphics.cpp:235  

#3 0x55555961c1a8 in ?? ??:0  

#4 0x5555595db2af in CXFA\_Radial::Draw(CXFA\_Graphics\*, CXFA\_GEPath\*, unsigned int, CFX\_RectF const&, CFX\_Matrix const&) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_radial.cpp:72  

#5 0x5555595db2af in ?? ??:0  

#6 0x555559555d16 in DrawRadial /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_fill.cpp:133  

#7 0x555559555d16 in Draw /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_fill.cpp:96  

#8 0x555559555d16 in ?? ??:0  

#9 0x555559506607 in CXFA\_Box::DrawFill(std::\_\_1::vector<CXFA\_Stroke\*, std::\_\_1::allocator<CXFA\_Stroke\*> > const&, CXFA\_Graphics\*, CFX\_RectF, CFX\_Matrix const&, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_box.cpp:239  

#10 0x555559506607 in ?? ??:0  

#11 0x555559505d0a in CXFA\_Box::Draw(CXFA\_Graphics\*, CFX\_RectF const&, CFX\_Matrix const&, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_box.cpp:197  

#12 0x555559505d0a in ?? ??:0  

#13 0x5555596738ae in DrawBorder /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_ffwidget.cpp:342  

#14 0x5555596738ae in RenderWidget /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_ffwidget.cpp:314  

#15 0x5555596738ae in ?? ??:0  

#16 0x55555963eadb in CXFA\_FFField::RenderWidget(CXFA\_Graphics\*, CFX\_Matrix const&, unsigned int) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_fffield.cpp:73  

#17 0x55555963eadb in ?? ??:0  

#18 0x555559681595 in CXFA\_RenderContext::DoRender(CXFA\_Graphics\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_rendercontext.cpp:31  

#19 0x555559681595 in ?? ??:0  

#20 0x555556ee4602 in CPDFSDK\_PageView::PageView\_OnDraw(CFX\_RenderDevice\*, CFX\_Matrix const&, CPDF\_RenderOptions\*, FX\_RECT const&) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../fpdfsdk/cpdfsdk\_pageview.cpp:89  

#21 0x555556ee4602 in ?? ??:0  

#22 0x55555982d7c5 in FFLCommon /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../fpdfsdk/fpdf\_formfill.cpp:219  

#23 0x55555982d7c5 in FPDF\_FFLDraw /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../fpdfsdk/fpdf\_formfill.cpp:590  

#24 0x55555982d7c5 in ?? ??:0  

#25 0x555556616c12 in RenderPage /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../samples/pdfium\_test.cc:625  

#26 0x555556616c12 in RenderPdf /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../samples/pdfium\_test.cc:832  

#27 0x555556616c12 in main /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../samples/pdfium\_test.cc:1012  

#28 0x555556616c12 in ?? ??:0  

#29 0x7ffff6e24b96 in \_\_libc\_start\_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310  

#30 0x7ffff6e24b96 in ?? ??:0

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: SEGV (/workarea/fuzz/bin/pdfium\_coverage/pdfium\_test+0x40ca5c6)  

==6418==ABORTING

**CREDIT INFORMATION**  

Antti Levomäki and Christian Jalio from Forcepoint

## Attachments

- [victory_010af185c9afd037c22e7b2af763e05c1fd172f8b45ba7cf698b9561ce80428f](attachments/victory_010af185c9afd037c22e7b2af763e05c1fd172f8b45ba7cf698b9561ce80428f) (text/plain, 186.5 KB)

## Timeline

### rs...@chromium.org (2019-03-04)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-05)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/f28eb5a9d5b8ae3c16d11120cf5622ab671b4b0d

commit f28eb5a9d5b8ae3c16d11120cf5622ab671b4b0d
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Mar 05 21:56:56 2019

ExtractLayoutItem() breaks when current item found in old list.

The current item probably shouldn't be in the old list,
but this avoids dangling references otherwise.

Bug: chromium:937799
Change-Id: Ic4fef5f171f2ba4bc396deb30f26d299673f01d9
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/51470
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://crrev.com/f28eb5a9d5b8ae3c16d11120cf5622ab671b4b0d/xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b23a1cd81d7f2d5b64f9f19234d74ef4432e931d

commit b23a1cd81d7f2d5b64f9f19234d74ef4432e931d
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Mar 06 10:19:02 2019

Roll src/third_party/pdfium 9384947f47f2..ed5dc24c07a3 (15 commits)

https://pdfium.googlesource.com/pdfium.git/+log/9384947f47f2..ed5dc24c07a3


git log 9384947f47f2..ed5dc24c07a3 --date=short --no-merges --format='%ad %ae %s'
2019-03-06 tsepez@chromium.org Spin in CFGAS_FormatString::ParseNum.
2019-03-05 tsepez@chromium.org Make members private in CXFA_LayoutItem, adding accessors.
2019-03-05 thestig@chromium.org Minimize simple_xfa.pdf.
2019-03-05 thestig@chromium.org Fix error in testing/resources/xfa_catalog_1_0.fragment.
2019-03-05 tsepez@chromium.org Tidy cxfa_itemlayoutprocessor.h
2019-03-05 tsepez@chromium.org ExtractLayoutItem() breaks when current item found in old list.
2019-03-05 rycsmith@google.com Add GetNumberValue function to fpdf_annot.
2019-03-05 thestig@chromium.org Fail early for data matrix barcode input that is too long.
2019-03-05 thestig@chromium.org Add CBC_DataMatrixWriterTest tests for encoding limits.
2019-03-05 thestig@chromium.org Avoid nullptr crash in CJS_App::get_active_docs().
2019-03-05 bungeman@google.com Roll third_party/freetype/src/ 6d65c60fc..31757f969 (2 commits)
2019-03-05 thestig@chromium.org Speed up DetermineConsecutiveDigitCount() in debug builds.
2019-03-05 manojb@microsoft.com Add tests for device to page and page to device coordinate conversions
2019-03-04 thestig@chromium.org Update Skia owner in the OWNERS file.
2019-03-04 thestig@chromium.org Roll tools/clang/ b23f5a073..257c91cc4 (9 commits)


Created with:
  gclient setdep -r src/third_party/pdfium@ed5dc24c07a3

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:937799,chromium:b/127345911,chromium:930394,chromium:930394,chromium:937572,chromium:930394
TBR=dsinclair@chromium.org

Change-Id: I08e30b280eab683713d0b33c0973e38ae8ef631e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1504801
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#638062}
[modify] https://crrev.com/b23a1cd81d7f2d5b64f9f19234d74ef4432e931d/DEPS


### ts...@chromium.org (2019-03-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-07)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-11)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-20)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-03-20)

Congrats the Panel decided to reward $3,000 for this report! 

### aw...@google.com (2019-03-21)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-05-13)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-05-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2019-07-19)

[Empty comment from Monorail migration]

### is...@google.com (2019-07-19)

This issue was migrated from crbug.com/chromium/937799?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/931174]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094199)*
