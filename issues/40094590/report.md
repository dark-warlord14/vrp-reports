# pdfium (XFA): oob array read in CXFA_Graphics::FillPathWithShading

| Field | Value |
|-------|-------|
| **Issue ID** | [40094590](https://issues.chromium.org/issues/40094590) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pd...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-04-12 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.124 Safari/537.36

Steps to reproduce the problem:
xfa/fxgraphics/cxfa_graphics.cpp:377:29: runtime error: index -2147483648 out of bounds for type 'FX_ARGB [256]'

    #0 0x55fc91f3c0f2 in CXFA_Graphics::FillPathWithShading(CXFA_GEPath const*, int, CFX_Matrix const&) xfa/fxgraphics/cxfa_graphics.cpp:377:29
    #1 0x55fc91f39f22 in CXFA_Graphics::RenderDeviceFillPath(CXFA_GEPath const*, int, CFX_Matrix const*) xfa/fxgraphics/cxfa_graphics.cpp:235:7
    #2 0x55fc91f39de1 in CXFA_Graphics::FillPath(CXFA_GEPath*, int, CFX_Matrix const*) xfa/fxgraphics/cxfa_graphics.cpp:179:5
    #3 0x55fc916b4e58 in CXFA_Radial::Draw(CXFA_Graphics*, CXFA_GEPath*, unsigned int, CFX_RectF const&, CFX_Matrix const&) xfa/fxfa/parser/cxfa_radial.cpp:72:8
    #4 0x55fc9162cf7d in CXFA_Fill::DrawRadial(CXFA_Graphics*, CXFA_GEPath*, CFX_RectF const&, CFX_Matrix const&) xfa/fxfa/parser/cxfa_fill.cpp:133:13
    #5 0x55fc9162cb99 in CXFA_Fill::Draw(CXFA_Graphics*, CXFA_GEPath*, CFX_RectF const&, CFX_Matrix const&) xfa/fxfa/parser/cxfa_fill.cpp:96:7
    #6 0x55fc915fa6ca in CXFA_Box::DrawFill(std::__1::vector<CXFA_Stroke*, std::__1::allocator<CXFA_Stroke*> > const&, CXFA_Graphics*, CFX_RectF, CFX_Matrix const&, bool) xfa/fxfa/parser/cxfa_box.cpp:239:9
    #7 0x55fc915f9f63 in CXFA_Box::Draw(CXFA_Graphics*, CFX_RectF const&, CFX_Matrix const&, bool) xfa/fxfa/parser/cxfa_box.cpp:197:3
    #8 0x55fc915404f3 in CXFA_FFWidget::DrawBorder(CXFA_Graphics*, CXFA_Box*, CFX_RectF const&, CFX_Matrix const&) xfa/fxfa/cxfa_ffwidget.cpp:337:10
    #9 0x55fc915442b8 in CXFA_FFWidget::RenderWidget(CXFA_Graphics*, CFX_Matrix const&, CXFA_FFWidget::HighlightOption) xfa/fxfa/cxfa_ffwidget.cpp:309:3
    #10 0x55fc915a4879 in CXFA_RenderContext::DoRender(CXFA_Graphics*) xfa/fxfa/cxfa_rendercontext.cpp:30:18
    #11 0x55fc912dd971 in CPDFSDK_PageView::PageView_OnDraw(CFX_RenderDevice*, CFX_Matrix const&, CPDF_RenderOptions*, FX_RECT const&) fpdfsdk/cpdfsdk_pageview.cpp:89:19
    #12 0x55fc90ecf7f3 in (anonymous namespace)::FFLCommon(fpdf_form_handle_t__*, fpdf_bitmap_t__*, void*, fpdf_page_t__*, int, int, int, int, int, int) fpdfsdk/fpdf_formfill.cpp:219:18
    #13 0x55fc90ecf4b1 in FPDF_FFLDraw fpdfsdk/fpdf_formfill.cpp:590:3
    #14 0x55fc8fdca7d3 in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:628:5
    #15 0x55fc8fdc259a in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:835:9
    #16 0x55fc8fdc04d8 in main samples/pdfium_test.cc:1015:5

https://cs.chromium.org/chromium/src/third_party/pdfium/xfa/fxgraphics/cxfa_graphics.cpp?l=340&rcl=763affaf6625e4670c172aa19fba8e1a3d23fab5

After a few iterations, a, b and c are 0, and s becomes NaN.

https://cs.chromium.org/chromium/src/third_party/pdfium/xfa/fxgraphics/cxfa_graphics.cpp?l=376&rcl=763affaf6625e4670c172aa19fba8e1a3d23fab5

What is the expected behavior?

What went wrong?
^

Did this work before? N/A 

Chrome version: 70.0.3538.124  Channel: n/a
OS Version: 
Flash Version:

## Attachments

- [chromium-952301.pdf](attachments/chromium-952301.pdf) (application/pdf, 584 B)

## Timeline

### pd...@gmail.com (2019-04-12)

Note: Chrome doesn't use XFA.

### ct...@chromium.org (2019-04-12)

Looks similar to https://crbug.com/chromium/951712. thestig@ or tsepez@ could you take a look to confirm?

[Monorail components: Internals>Plugins>PDF]

### th...@chromium.org (2019-04-13)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-23)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/84275ef0971e22ca194989a4b19844edd7ac6cc3

commit 84275ef0971e22ca194989a4b19844edd7ac6cc3
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Apr 23 16:56:40 2019

Check for nan in another place in cxfa_graphics.cpp

Bug: chromium:952301
Change-Id: I47b23a3696381d251c043e0b77f3d6a3b8941cd3
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/53311
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>

[modify] https://crrev.com/84275ef0971e22ca194989a4b19844edd7ac6cc3/xfa/fxgraphics/cxfa_graphics.cpp


### ts...@chromium.org (2019-04-23)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/51cf7325ca071d2291619829505e640229f8c69f

commit 51cf7325ca071d2291619829505e640229f8c69f
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Apr 23 19:05:58 2019

Roll src/third_party/pdfium 0f35a9ee0be1..e9fa6a97fea6 (6 commits)

https://pdfium.googlesource.com/pdfium.git/+log/0f35a9ee0be1..e9fa6a97fea6


git log 0f35a9ee0be1..e9fa6a97fea6 --date=short --no-merges --format='%ad %ae %s'
2019-04-23 tsepez@chromium.org Check for possibility of inf value from FXSYS_wcstof()
2019-04-23 tsepez@chromium.org Fix integer underflow in cfgas_stringformatter.cpp, part 2
2019-04-23 tsepez@chromium.org Check for nan in another place in cxfa_graphics.cpp
2019-04-23 thestig@chromium.org Update the email address for an AUTHORS entry.
2019-04-23 thestig@chromium.org Use std::make_unsigned<OPJ_OFF_T>::type in JPX code.
2019-04-23 thestig@chromium.org Roll third_party/skia/ 1383a38e1..e2aa08bf1 (1 commit)


Created with:
  gclient setdep -r src/third_party/pdfium@e9fa6a97fea6

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:951712,chromium:947188,chromium:952301
TBR=dsinclair@chromium.org

Change-Id: Id6586e32a8bfc712bd1425a9dbe1b6997ba880d5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1577629
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#653295}
[modify] https://crrev.com/51cf7325ca071d2291619829505e640229f8c69f/DEPS


### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### na...@google.com (2019-04-29)

[Empty comment from Monorail migration]

### na...@google.com (2019-05-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### pa...@chromium.org (2019-05-01)

Congrats! The Panel rewarded $1,000 for this report :)

### aw...@google.com (2019-05-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-07-31)

This issue was migrated from crbug.com/chromium/952301?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094590)*
