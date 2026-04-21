# Security: Pdfium heap bof in CFDE_TextOut::RetrievePieces()

| Field | Value |
|-------|-------|
| **Issue ID** | [40060172](https://issues.chromium.org/issues/40060172) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2022-07-05 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

Pdfium heap bof in CFDE\_TextOut::RetrievePieces() at xfa/fde/cfde\_textout.cpp:389.

Offsets are calculated incorrectly, leading to RetrievePieces() overflowing the std::vector m\_CharWidths. In repro.pdf m\_CharWidths size is 402, but the loop "for (; j < iPieceChars; j++)"  

runs iChar from 377 to 532, overflowing at "m\_CharWidths[iChar++] = iCurCharWidth;".

Requires XFA to crash. Triggers in Chromium if XFA is enabled via chrome://flags.

Seems like this could have RCE potential.

**VERSION**  

<https://pdfium.googlesource.com/pdfium.git>

commit b529e7b164c90dceae0d438a904baaf34bbe4237 (HEAD -> origin/main, origin/main, origin/HEAD)  

Date: Sat Jul 2 20:08:51 2022 +0000

**REPRODUCTION CASE**  

pdfium\_test repro.pdf

# Processing PDF file /workarea/fuzz/wip/pdfium/report/retrieve\_pieces\_bof/repro.pdf. Document has invalid cross reference table

==181578==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x61b0000a9bc8 at pc 0x561028b56e73 bp 0x7fff3b4eeb70 sp 0x7fff3b4eeb68  

WRITE of size 4 at 0x61b0000a9bc8 thread T0  

#0 0x561028b56e72 in CFDE\_TextOut::RetrievePieces(CFGAS\_Char::BreakType, bool, CFX\_RectF const&, unsigned long\*, int\*) xfa/fde/cfde\_textout.cpp:389:29  

#1 0x561028b58a10 in CFDE\_TextOut::ReloadLinePiece(CFDE\_TextOut::Line\*, CFX\_RectF const&) xfa/fde/cfde\_textout.cpp:470:9  

#2 0x561028b53c52 in Reload xfa/fde/cfde\_textout.cpp:448:7  

#3 0x561028b53c52 in CFDE\_TextOut::DrawLogicText(CFX\_RenderDevice\*, fxcrt::StringViewTemplate<wchar\_t>, CFX\_RectF const&) xfa/fde/cfde\_textout.cpp:293:3  

#4 0x561028a8f840 in CXFA\_FWLTheme::DrawText(CFWL\_ThemeText const&) xfa/fxfa/cxfa\_fwltheme.cpp:141:15  

#5 0x561028bc4175 in CFWL\_ListBox::DrawItem(CFGAS\_GEGraphics\*, CFWL\_ListBox::Item\*, int, CFX\_RectF const&, CFX\_Matrix const&) xfa/fwl/cfwl\_listbox.cpp:416:11  

#6 0x561028bc0e12 in CFWL\_ListBox::DrawItems(CFGAS\_GEGraphics\*, CFX\_Matrix const&) xfa/fwl/cfwl\_listbox.cpp:360:5  

#7 0x561028bc015c in CFWL\_ListBox::DrawWidget(CFGAS\_GEGraphics\*, CFX\_Matrix const&) xfa/fwl/cfwl\_listbox.cpp:108:3  

#8 0x561028ba02ef in CFWL\_ComboBox::DrawWidget(CFGAS\_GEGraphics\*, CFX\_Matrix const&) xfa/fwl/cfwl\_combobox.cpp:127:17  

#9 0x561028ba469c in CFWL\_ComboBox::OnDrawWidget(CFGAS\_GEGraphics\*, CFX\_Matrix const&) xfa/fwl/cfwl\_combobox.cpp:446:3  

#10 0x561028a34774 in OnDrawWidget xfa/fxfa/cxfa\_ffcombobox.cpp:378:19  

#11 0x561028a34774 in non-virtual thunk to CXFA\_FFComboBox::OnDrawWidget(CFGAS\_GEGraphics\*, CFX\_Matrix const&) xfa/fxfa/cxfa\_ffcombobox.cpp  

#12 0x561028bead13 in CFWL\_WidgetMgr::OnDrawWidget(CFWL\_Widget\*, CFGAS\_GEGraphics\*, CFX\_Matrix const&) xfa/fwl/cfwl\_widgetmgr.cpp:199:27  

#13 0x561028a48d88 in CXFA\_FFField::RenderWidget(CFGAS\_GEGraphics\*, CFX\_Matrix const&, CXFA\_FFWidget::HighlightOption) xfa/fxfa/cxfa\_fffield.cpp:98:32  

#14 0x561028dab579 in CPDFXFA\_Page::DrawFocusAnnot(CFX\_RenderDevice\*, CPDFSDK\_Annot\*, CFX\_Matrix const&, FX\_RECT const&) fpdfsdk/fpdfxfa/cpdfxfa\_page.cpp:313:16  

#15 0x56102538919b in CPDFSDK\_PageView::PageView\_OnDraw(CFX\_RenderDevice\*, CFX\_Matrix const&, CPDF\_RenderOptions\*, FX\_RECT const&) fpdfsdk/cpdfsdk\_pageview.cpp:77:40  

#16 0x5610253af42b in FFLCommon fpdfsdk/fpdf\_formfill.cpp:217:18  

#17 0x5610253af42b in FPDF\_FFLDraw fpdfsdk/fpdf\_formfill.cpp:670:3  

#18 0x561025305b56 in ProcessPage samples/pdfium\_test.cc:815:5  

#19 0x561025305b56 in ProcessPdf samples/pdfium\_test.cc:1045:9  

#20 0x561025305b56 in main samples/pdfium\_test.cc:1300:5  

#21 0x7f220353f0b2 in \_\_libc\_start\_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16

0x61b0000a9bc8 is located 0 bytes to the right of 1608-byte region [0x61b0000a9580,0x61b0000a9bc8)  

allocated by thread T0 here:  

#0 0x5610252fa6fd in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:95:3  

#1 0x561028b5d3fc in \_\_libcpp\_operator\_new<unsigned long> buildtools/third\_party/libc++/trunk/include/new:245:10  

#2 0x561028b5d3fc in \_\_libcpp\_allocate buildtools/third\_party/libc++/trunk/include/new:271:10  

#3 0x561028b5d3fc in allocate buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator.h:105:38  

#4 0x561028b5d3fc in allocate buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator\_traits.h:262:20  

#5 0x561028b5d3fc in \_\_split\_buffer buildtools/third\_party/libc++/trunk/include/\_\_split\_buffer:322:29  

#6 0x561028b5d3fc in std::Cr::vector<int, std::Cr::allocator<int>>::\_\_append(unsigned long, int const&) buildtools/third\_party/libc++/trunk/include/vector:1060:53  

#7 0x561028b54906 in resize buildtools/third\_party/libc++/trunk/include/vector:1923:15  

#8 0x561028b54906 in CFDE\_TextOut::LoadText(fxcrt::WideString const&, CFX\_RectF const&) xfa/fde/cfde\_textout.cpp:325:18  

#9 0x561028b53952 in CFDE\_TextOut::DrawLogicText(CFX\_RenderDevice\*, fxcrt::StringViewTemplate<wchar\_t>, CFX\_RectF const&) xfa/fde/cfde\_textout.cpp:292:3  

#10 0x561028a8f840 in CXFA\_FWLTheme::DrawText(CFWL\_ThemeText const&) xfa/fxfa/cxfa\_fwltheme.cpp:141:15  

#11 0x561028bc4175 in CFWL\_ListBox::DrawItem(CFGAS\_GEGraphics\*, CFWL\_ListBox::Item\*, int, CFX\_RectF const&, CFX\_Matrix const&) xfa/fwl/cfwl\_listbox.cpp:416:11  

#12 0x561028bc0e12 in CFWL\_ListBox::DrawItems(CFGAS\_GEGraphics\*, CFX\_Matrix const&) xfa/fwl/cfwl\_listbox.cpp:360:5  

#13 0x561028bc015c in CFWL\_ListBox::DrawWidget(CFGAS\_GEGraphics\*, CFX\_Matrix const&) xfa/fwl/cfwl\_listbox.cpp:108:3  

#14 0x561028ba02ef in CFWL\_ComboBox::DrawWidget(CFGAS\_GEGraphics\*, CFX\_Matrix const&) xfa/fwl/cfwl\_combobox.cpp:127:17  

#15 0x561028ba469c in CFWL\_ComboBox::OnDrawWidget(CFGAS\_GEGraphics\*, CFX\_Matrix const&) xfa/fwl/cfwl\_combobox.cpp:446:3  

#16 0x561028a34774 in OnDrawWidget xfa/fxfa/cxfa\_ffcombobox.cpp:378:19  

#17 0x561028a34774 in non-virtual thunk to CXFA\_FFComboBox::OnDrawWidget(CFGAS\_GEGraphics\*, CFX\_Matrix const&) xfa/fxfa/cxfa\_ffcombobox.cpp  

#18 0x561028bead13 in CFWL\_WidgetMgr::OnDrawWidget(CFWL\_Widget\*, CFGAS\_GEGraphics\*, CFX\_Matrix const&) xfa/fwl/cfwl\_widgetmgr.cpp:199:27  

#19 0x561028a48d88 in CXFA\_FFField::RenderWidget(CFGAS\_GEGraphics\*, CFX\_Matrix const&, CXFA\_FFWidget::HighlightOption) xfa/fxfa/cxfa\_fffield.cpp:98:32  

#20 0x561028dab579 in CPDFXFA\_Page::DrawFocusAnnot(CFX\_RenderDevice\*, CPDFSDK\_Annot\*, CFX\_Matrix const&, FX\_RECT const&) fpdfsdk/fpdfxfa/cpdfxfa\_page.cpp:313:16  

#21 0x56102538919b in CPDFSDK\_PageView::PageView\_OnDraw(CFX\_RenderDevice\*, CFX\_Matrix const&, CPDF\_RenderOptions\*, FX\_RECT const&) fpdfsdk/cpdfsdk\_pageview.cpp:77:40  

#22 0x5610253af42b in FFLCommon fpdfsdk/fpdf\_formfill.cpp:217:18  

#23 0x5610253af42b in FPDF\_FFLDraw fpdfsdk/fpdf\_formfill.cpp:670:3  

#24 0x561025305b56 in ProcessPage samples/pdfium\_test.cc:815:5  

#25 0x561025305b56 in ProcessPdf samples/pdfium\_test.cc:1045:9  

#26 0x561025305b56 in main samples/pdfium\_test.cc:1300:5  

#27 0x7f220353f0b2 in \_\_libc\_start\_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-buffer-overflow xfa/fde/cfde\_textout.cpp:389:29 in CFDE\_TextOut::RetrievePieces(CFGAS\_Char::BreakType, bool, CFX\_RectF const&, unsigned long\*, int\*)  

Shadow bytes around the buggy address:  

0x0c368000d320: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c368000d330: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c368000d340: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c368000d350: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c368000d360: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x0c368000d370: 00 00 00 00 00 00 00 00 00[fa]fa fa fa fa fa fa  

0x0c368000d380: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c368000d390: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c368000d3a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c368000d3b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c368000d3c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

==181578==ABORTING

**CREDIT INFORMATION**  

Antti Levomäki and Christian Jalio from Forcepoint

## Attachments

- [repro.pdf](attachments/repro.pdf) (application/pdf, 1.6 KB)

## Timeline

### [Deleted User] (2022-07-05)

[Empty comment from Monorail migration]

### da...@chromium.org (2022-07-06)

High Sev for a memory bug in the PDF sandbox.
But impact = None as it requires a flag to be enabled.

[Monorail components: Internals>Plugins>PDF]

### [Deleted User] (2022-07-06)

[Empty comment from Monorail migration]

### th...@chromium.org (2022-07-07)

[Empty comment from Monorail migration]

### th...@chromium.org (2022-07-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-07-12)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/60486000902d39cb18144e8a01b848598b03fa64

commit 60486000902d39cb18144e8a01b848598b03fa64
Author: Lei Zhang <thestig@chromium.org>
Date: Tue Jul 12 20:15:55 2022

Correctly skip characters in CFDE_TextOut::RetrievePieces().

CFDE_TextOut::RetrievePieces() has a parameter that indicates the
character to start with. Handle this parameter correctly and skip that
many characters before continuing to process more characters.

Bug: chromium:1342078
Change-Id: I20ae6f92e3cd72ef832adad6ce5f8b6ba552967b
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/95150
Reviewed-by: Nigi <nigi@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/60486000902d39cb18144e8a01b848598b03fa64/xfa/fde/cfde_textout.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/60486000902d39cb18144e8a01b848598b03fa64/xfa/fde/cfde_textout_unittest.cpp


### th...@chromium.org (2022-07-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-07-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/46f970f743da58007251f508abf371f913644d4b

commit 46f970f743da58007251f508abf371f913644d4b
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Jul 13 06:24:12 2022

Roll PDFium from 9b8ab7d0d124 to b5d64b4d05ed (6 revisions)

https://pdfium.googlesource.com/pdfium.git/+log/9b8ab7d0d124..b5d64b4d05ed

2022-07-12 thestig@chromium.org Change type of `CFDE_TextOut::m_iCurLine` to size_t.
2022-07-12 thestig@chromium.org Remove an impossible check in CXFA_FWLTheme::CalcTextRect().
2022-07-12 thestig@chromium.org Add more tests for FPDFBitmap_CreateEx().
2022-07-12 thestig@chromium.org Make checking out testing/corpus optional.
2022-07-12 thestig@chromium.org Correctly skip characters in CFDE_TextOut::RetrievePieces().
2022-07-12 nigi@chromium.org [Skia] Flush cached drawings before bitmap composition.

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

Bug: chromium:1342078
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I42257d61be071aaa953fcbb2f7c62ea18066ab6a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3758858
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1023596}

[modify] https://crrev.com/46f970f743da58007251f508abf371f913644d4b/DEPS


### [Deleted User] (2022-07-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-13)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-21)

Congratulations Antti and Christian! The VRP Panel has decided to award you $7500 for this report. Thank you for your efforts in reporting this issue to us and nice work! 

### am...@google.com (2022-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-10-19)

This issue was migrated from crbug.com/chromium/1342078?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060172)*
