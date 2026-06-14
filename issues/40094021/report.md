# Security: Invalid read. SEGV on CXFA_Graphics::FillPathWithShading

| Field | Value |
|-------|-------|
| **Issue ID** | [40094021](https://issues.chromium.org/issues/40094021) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-02-12 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Invalid read. SEGV on CXFA\_Graphics::FillPathWithShading

**VERSION**  

commit 25d9272255438c45f6d91051a1092b54006eb797

**REPRODUCTION CASE**

Open attached file.

ADDITIONAL INFORMATION

# Rendering PDF file /workarea/samplestore/wip/pdfium/victory/victory\_09c57a954008472cde88f8df1b860e576c0edc4f6ca18d9ebbdd543efde38fc1. AddressSanitizer:DEADLYSIGNAL

==4810==ERROR: AddressSanitizer: SEGV on unknown address 0x7ffdf3cf38a0 (pc 0x555559622d92 bp 0x7fffffffcf10 sp 0x7fffffffcd80 T0)  

==4810==The signal is caused by a READ memory access.  

#0 0x555559622d91 in CXFA\_Graphics::FillPathWithShading(CXFA\_GEPath const\*, int, CFX\_Matrix const&) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxgraphics/cxfa\_graphics.cpp:314  

#1 0x555559622d91 in ?? ??:0  

#2 0x5555596205b8 in CXFA\_Graphics::RenderDeviceFillPath(CXFA\_GEPath const\*, int, CFX\_Matrix const\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxgraphics/cxfa\_graphics.cpp:235  

#3 0x5555596205b8 in ?? ??:0  

#4 0x555559564787 in CXFA\_Linear::Draw(CXFA\_Graphics\*, CXFA\_GEPath\*, unsigned int, CFX\_RectF const&, CFX\_Matrix const&) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_linear.cpp:88  

#5 0x555559564787 in ?? ??:0  

#6 0x55555955879b in DrawLinear /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_fill.cpp:143  

#7 0x55555955879b in Draw /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_fill.cpp:102  

#8 0x55555955879b in ?? ??:0  

#9 0x555559509057 in CXFA\_Box::DrawFill(std::\_\_1::vector<CXFA\_Stroke\*, std::\_\_1::allocator<CXFA\_Stroke\*> > const&, CXFA\_Graphics\*, CFX\_RectF, CFX\_Matrix const&, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_box.cpp:239  

#10 0x555559509057 in ?? ??:0  

#11 0x55555950875a in CXFA\_Box::Draw(CXFA\_Graphics\*, CFX\_RectF const&, CFX\_Matrix const&, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_box.cpp:197  

#12 0x55555950875a in ?? ??:0  

#13 0x555559677c7e in DrawBorder /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_ffwidget.cpp:342  

#14 0x555559677c7e in RenderWidget /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_ffwidget.cpp:314  

#15 0x555559677c7e in ?? ??:0  

#16 0x555559642ebb in CXFA\_FFField::RenderWidget(CXFA\_Graphics\*, CFX\_Matrix const&, unsigned int) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_fffield.cpp:73  

#17 0x555559642ebb in ?? ??:0  

#18 0x555559685965 in CXFA\_RenderContext::DoRender(CXFA\_Graphics\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_rendercontext.cpp:31  

#19 0x555559685965 in ?? ??:0  

#20 0x555556ee5872 in CPDFSDK\_PageView::PageView\_OnDraw(CFX\_RenderDevice\*, CFX\_Matrix const&, CPDF\_RenderOptions\*, FX\_RECT const&) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../fpdfsdk/cpdfsdk\_pageview.cpp:89  

#21 0x555556ee5872 in ?? ??:0  

#22 0x555559830165 in FFLCommon /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../fpdfsdk/fpdf\_formfill.cpp:225  

#23 0x555559830165 in FPDF\_FFLDraw /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../fpdfsdk/fpdf\_formfill.cpp:588  

#24 0x555559830165 in ?? ??:0  

#25 0x555556618bd7 in RenderPage /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../samples/pdfium\_test.cc:625  

#26 0x555556618bd7 in RenderPdf /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../samples/pdfium\_test.cc:832  

#27 0x555556618bd7 in main /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../samples/pdfium\_test.cc:1009  

#28 0x555556618bd7 in ?? ??:0  

#29 0x7ffff6e24b96 in \_\_libc\_start\_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310  

#30 0x7ffff6e24b96 in ?? ??:0

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: SEGV (/workarea/fuzz/bin/pdfium\_coverage/pdfium\_test+0x40ced91)  

==4810==ABORTING

**CREDIT INFORMATION**  

Antti Levomäki and Christian Jalio from Forcepoint

## Attachments

- [victory_09c57a954008472cde88f8df1b860e576c0edc4f6ca18d9ebbdd543efde38fc1](attachments/victory_09c57a954008472cde88f8df1b860e576c0edc4f6ca18d9ebbdd543efde38fc1) (text/plain, 791.2 KB)

## Timeline

### ts...@chromium.org (2019-02-12)

Wild read with index=-2147483648 at
cxfa_graphics.cpp:314: dib_buf[column] = m_info.fillColor.GetShading() >m_argbArray[index];

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2019-02-12)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-02-12)

Because the bounds checks starting at cxfa_graphics.cpp:302 don't handle NaN which happens if we get 0.0/0.0 (as opposed to inf).

### th...@chromium.org (2019-02-12)

tsepez: Sounds like you are already looking at this then?

### ts...@chromium.org (2019-02-12)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-02-12)

Probably sev-low since there isn't a lot of control over what address is used, but leave at medium for now.

### ts...@chromium.org (2019-02-12)

CL at https://pdfium-review.googlesource.com/c/pdfium/+/50552

### ts...@chromium.org (2019-02-12)

probably other gotcha's lurking in this file, as they might go from floating point caclulations to integer indicies in other places without handling all the gotcha's that come with C++ floating arithmetic.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-02-12)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/6b37b6fb3f9308e15f680edd700ea4a2680263af

commit 6b37b6fb3f9308e15f680edd700ea4a2680263af
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Feb 12 18:58:53 2019

Avoid NaN comparison in CFXA_FillPathWithShading() bounds checks.

Because (0.0f / 0.0f) is neither less than 0.0, nor greater
than 1.0, nor safely in the range between the two.

Bug: chromium:931175
Change-Id: Ib0f9a6cf96ebd9a9f4f6550054ff355d6cff296e
Reviewed-on: https://pdfium-review.googlesource.com/c/50552
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://crrev.com/6b37b6fb3f9308e15f680edd700ea4a2680263af/xfa/fxgraphics/cxfa_graphics.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-02-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6ef037f5eadaec258a0f16219c76e2c83412a652

commit 6ef037f5eadaec258a0f16219c76e2c83412a652
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Feb 12 20:18:52 2019

Roll src/third_party/pdfium 025edab2778a..6b37b6fb3f93 (3 commits)

https://pdfium.googlesource.com/pdfium.git/+log/025edab2778a..6b37b6fb3f93


git log 025edab2778a..6b37b6fb3f93 --date=short --no-merges --format='%ad %ae %s'
2019-02-12 tsepez@chromium.org Avoid NaN comparison in CFXA_FillPathWithShading() bounds checks.
2019-02-12 thakis@chromium.org Remove semicolons after JS_STATIC_foo macros, turn on -Wextra-semi
2019-02-12 thestig@chromium.org Simplify CPDF_TextPageFind::FindPrev().


Created with:
  gclient setdep -r src/third_party/pdfium@6b37b6fb3f93

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:931175,chromium:926235
TBR=dsinclair@chromium.org

Change-Id: I81df09ac158069ae0eee0609222d7d1850764896
Reviewed-on: https://chromium-review.googlesource.com/c/1467443
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#631358}
[modify] https://crrev.com/6ef037f5eadaec258a0f16219c76e2c83412a652/DEPS


### ts...@chromium.org (2019-02-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-15)

[Empty comment from Monorail migration]

### na...@google.com (2019-02-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-02-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2019-02-25)

Thanks for the report! The VRP panel decided to award $500, and noted that it would likely be very difficult for an attacker to exploit.  Cheers!

### aw...@google.com (2019-03-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-05-24)

This issue was migrated from crbug.com/chromium/931175?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094021)*
