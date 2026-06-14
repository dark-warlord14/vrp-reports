# pdfium (XFA): invalid-vptr in CXFA_FFTextEdit::UpdateFWLData

| Field | Value |
|-------|-------|
| **Issue ID** | [40050755](https://issues.chromium.org/issues/40050755) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pd...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-11-21 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.101 Safari/537.36

Steps to reproduce the problem:
xfa/fxfa/cxfa_fftextedit.cpp:277:18: runtime error: downcast of address 0x5583fdc14890 which does not point to an object of type 'CXFA_Barcode'
0x5583fdc14890: note: object is of type 'CXFA_Field'
 00 00 00 00  18 6d e5 fa 83 55 00 00  50 dc b6 fd 83 55 00 00  08 00 00 00 5c 00 00 00  68 c4 1f f7
              ^~~~~~~~~~~~~~~~~~~~~~~
              vptr for 'CXFA_Field'

xfa/fxfa/cxfa_fftextedit.cpp:278:24: runtime error: member call on address 0x5583fdc14890 which does not point to an object of type 'CXFA_Barcode'
0x5583fdc14890: note: object is of type 'CXFA_Field'
 00 00 00 00  18 6d e5 fa 83 55 00 00  50 dc b6 fd 83 55 00 00  08 00 00 00 5c 00 00 00  68 c4 1f f7
              ^~~~~~~~~~~~~~~~~~~~~~~
              vptr for 'CXFA_Field'

    #0 0x5583fa49997c in CXFA_FFTextEdit::UpdateFWLData() xfa/fxfa/cxfa_fftextedit.cpp:278:24
    #1 0x5583fa497f17 in CXFA_FFTextEdit::OnSetFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_fftextedit.cpp:157:5
    #2 0x5583fa44b888 in CXFA_FFDocView::SetFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_ffdocview.cpp:296:23
    #3 0x5583fa4a2ef4 in CXFA_FFWidgetHandler::OnLButtonDown(CXFA_FFWidget*, unsigned int, CFX_PTemplate<float> const&) xfa/fxfa/cxfa_ffwidgethandler.cpp:53:21
    #4 0x5583fa7a36c1 in CPDFXFA_WidgetHandler::OnLButtonDown(CPDFSDK_PageView*, fxcrt::ObservedPtr<CPDFSDK_Annot>*, unsigned int, CFX_PTemplate<float> const&) fpdfsdk/fpdfxfa/cpdfxfa_widgethandler.cpp:407:26
    #5 0x5583f89db17d in CPDFSDK_AnnotHandlerMgr::Annot_OnLButtonDown(CPDFSDK_PageView*, fxcrt::ObservedPtr<CPDFSDK_Annot>*, unsigned int, CFX_PTemplate<float> const&) fpdfsdk/cpdfsdk_annothandlermgr.cpp:147:9
    #6 0x5583f8a3f0d5 in CPDFSDK_PageView::OnLButtonDown(CFX_PTemplate<float> const&, unsigned int) fpdfsdk/cpdfsdk_pageview.cpp:294:26
    #7 0x5583f8a6e54a in FORM_OnLButtonDown fpdfsdk/fpdf_formfill.cpp:386:21
    #8 0x5583f89c8eca in (anonymous namespace)::SendMouseDownEvent(fpdf_form_handle_t__*, fpdf_page_t__*, std::__1::vector<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::allocator<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > > > const&) samples/pdfium_test_event_helper.cc:67:5
    #9 0x5583f89c8b23 in SendPageEvents(fpdf_form_handle_t__*, fpdf_page_t__*, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test_event_helper.cc:138:7
    #10 0x5583f89c04be in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:669:5
    #11 0x5583f89b80c6 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:929:9
    #12 0x5583f89b59b9 in main samples/pdfium_test.cc:1138:5

What is the expected behavior?

What went wrong?
^

Did this work before? N/A 

Chrome version: 78.0.3904.101  Channel: n/a
OS Version: 
Flash Version:

## Attachments

- [chromium-1026918.pdf](attachments/chromium-1026918.pdf) (application/pdf, 609 B)
- [chromium-1026918.evt](attachments/chromium-1026918.evt) (application/octet-stream, 32 B)

## Timeline

### pd...@gmail.com (2019-11-21)

Triggering this requires minimal user interaction, namely a single click (or otherwise giving focus). I've attached the event file to use with pdfium_test.

### pd...@gmail.com (2019-11-21)

Note: Chrome doesn't use XFA.

### me...@chromium.org (2019-11-21)

Tom, PTAL?

[Monorail components: Internals>Plugins>PDF]

### me...@chromium.org (2019-11-21)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-11-21)

Repros, but fortunately not likely to be exploitable, in that we call only the non-virtual GetDataLength() method which in turn calls only the  common superclass method JSObject() which winds up with a valid |this| as a result. 

### ts...@chromium.org (2019-11-21)

CL at https://pdfium-review.googlesource.com/c/pdfium/+/62670

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-22)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/e87972e30da4cb87f0620baf32cea698f43dd093

commit e87972e30da4cb87f0620baf32cea698f43dd093
Author: Tom Sepez <tsepez@chromium.org>
Date: Fri Nov 22 18:01:32 2019

Fix downcast in CXFA_FFTextEdit.

The |ff_widget_type_| of a CXFA_Node may reflect the type of its
UI child node if it is of widget type |kNone|, so even if it claims
to be of a particular type, it is only safe to downcast its UI
child to that particular type.

Bug: chromium:1026918
Change-Id: I5daef3c6436ada6d31126ddb380f6420651b47e5
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/62670
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>

[add] https://pdfium.googlesource.com/pdfium/+/e87972e30da4cb87f0620baf32cea698f43dd093/testing/resources/pixel/xfa_specific/bug_1026918.evt
[add] https://pdfium.googlesource.com/pdfium/+/e87972e30da4cb87f0620baf32cea698f43dd093/testing/resources/pixel/xfa_specific/bug_1026918_expected.pdf.0.png
[modify] https://pdfium.googlesource.com/pdfium/+/e87972e30da4cb87f0620baf32cea698f43dd093/xfa/fxfa/cxfa_fftextedit.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/e87972e30da4cb87f0620baf32cea698f43dd093/xfa/fxfa/parser/cxfa_node.h
[add] https://pdfium.googlesource.com/pdfium/+/e87972e30da4cb87f0620baf32cea698f43dd093/testing/resources/pixel/xfa_specific/bug_1026918.in


### ts...@chromium.org (2019-11-22)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0d855887fb818122128df1352063bfa390782a91

commit 0d855887fb818122128df1352063bfa390782a91
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Nov 22 21:30:37 2019

Roll src/third_party/pdfium 26b030de1b76..e87972e30da4 (1 commits)

https://pdfium.googlesource.com/pdfium.git/+log/26b030de1b76..e87972e30da4

git log 26b030de1b76..e87972e30da4 --date=short --no-merges --format='%ad %ae %s'
2019-11-22 tsepez@chromium.org Fix downcast in CXFA_FFTextEdit.

Created with:
  gclient setdep -r src/third_party/pdfium@e87972e30da4

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1026918
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I99f2443f4efdb0ab23268e332a4e8036b5ceec75
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1931163
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#718287}

[modify] https://crrev.com/0d855887fb818122128df1352063bfa390782a91/DEPS


### sh...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### na...@google.com (2019-12-02)

[Empty comment from Monorail migration]

### na...@google.com (2019-12-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-05)

Congrats! The Panel decided to reward $2,000 for this report!

### na...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-02-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-02-29)

This issue was migrated from crbug.com/chromium/1026918?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050755)*
