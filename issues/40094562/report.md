# Security: pdfium SEGV on unknown address in CXFA_Graphics::FillPathWithShading

| Field | Value |
|-------|-------|
| **Issue ID** | [40094562](https://issues.chromium.org/issues/40094562) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-04-11 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

Pdfium SEGV on unknown address in CXFA\_Graphics::FillPathWithShading

**VERSION**  

commit 9cf260b9d7f4491833bd5fd997a286ce6926678e  

Date: Thu Apr 11 00:22:00 2019 +0000

**REPRODUCTION CASE**

Open attached file.

ADDITIONAL INFORMATION

# Rendering PDF file /workarea/samplestore/wip/pdfium/victory\_tmp/victory\_3a24f8fc2aa1da096a48281c0f633027e8a800038052226feecd7957ca25ee72.pdf. Document has invalid cross reference table AddressSanitizer:DEADLYSIGNAL

==9791==ERROR: AddressSanitizer: SEGV on unknown address 0x7ffdf3cc58a0 (pc 0x55555969313c bp 0x7fffffffced0 sp 0x7fffffffcd40 T0)  

==9791==The signal is caused by a READ memory access.  

#0 0x55555969313b in CXFA\_Graphics::FillPathWithShading(CXFA\_GEPath const\*, int, CFX\_Matrix const&) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxgraphics/cxfa\_graphics.cpp:316  

#1 0x55555969313b in ?? ??:0  

#2 0x555559690948 in CXFA\_Graphics::RenderDeviceFillPath(CXFA\_GEPath const\*, int, CFX\_Matrix const\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxgraphics/cxfa\_graphics.cpp:235  

#3 0x555559690948 in ?? ??:0  

#4 0x5555595d43c7 in CXFA\_Linear::Draw(CXFA\_Graphics\*, CXFA\_GEPath\*, unsigned int, CFX\_RectF const&, CFX\_Matrix const&) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_linear.cpp:88  

#5 0x5555595d43c7 in ?? ??:0  

#6 0x5555595c83db in DrawLinear /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_fill.cpp:143  

#7 0x5555595c83db in Draw /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_fill.cpp:102  

#8 0x5555595c83db in ?? ??:0  

#9 0x555559578ea4 in CXFA\_Box::DrawFill(std::\_\_1::vector<CXFA\_Stroke\*, std::\_\_1::allocator<CXFA\_Stroke\*> > const&, CXFA\_Graphics\*, CFX\_RectF, CFX\_Matrix const&, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_box.cpp:239  

#10 0x555559578ea4 in ?? ??:0  

#11 0x5555595785da in CXFA\_Box::Draw(CXFA\_Graphics\*, CFX\_RectF const&, CFX\_Matrix const&, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_box.cpp:197  

#12 0x5555595785da in ?? ??:0  

#13 0x5555596ea602 in DrawBorder /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_ffwidget.cpp:337  

#14 0x5555596ea602 in RenderWidget /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_ffwidget.cpp:309  

#15 0x5555596ea602 in ?? ??:0  

#16 0x5555596b5d9d in CXFA\_FFField::RenderWidget(CXFA\_Graphics\*, CFX\_Matrix const&, unsigned int) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_fffield.cpp:73  

#17 0x5555596b5d9d in ?? ??:0  

#18 0x5555596f84a5 in CXFA\_RenderContext::DoRender(CXFA\_Graphics\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_rendercontext.cpp:31  

#19 0x5555596f84a5 in ?? ??:0  

#20 0x555556ed9232 in CPDFSDK\_PageView::PageView\_OnDraw(CFX\_RenderDevice\*, CFX\_Matrix const&, CPDF\_RenderOptions\*, FX\_RECT const&) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../fpdfsdk/cpdfsdk\_pageview.cpp:89  

#21 0x555556ed9232 in ?? ??:0  

#22 0x5555598aafe5 in FFLCommon /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../fpdfsdk/fpdf\_formfill.cpp:219  

#23 0x5555598aafe5 in FPDF\_FFLDraw /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../fpdfsdk/fpdf\_formfill.cpp:590  

#24 0x5555598aafe5 in ?? ??:0  

#25 0x555556603464 in RenderPage /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../samples/pdfium\_test.cc:625  

#26 0x555556603464 in RenderPdf /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../samples/pdfium\_test.cc:832  

#27 0x555556603464 in main /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../samples/pdfium\_test.cc:1012  

#28 0x555556603464 in ?? ??:0  

#29 0x7ffff6e24b96 in \_\_libc\_start\_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310  

#30 0x7ffff6e24b96 in ?? ??:0

**CREDIT INFORMATION**  

Antti Levomäki and Christian Jalio from Forcepoint

## Attachments

- [victory_3a24f8fc2aa1da096a48281c0f633027e8a800038052226feecd7957ca25ee72.pdf](attachments/victory_3a24f8fc2aa1da096a48281c0f633027e8a800038052226feecd7957ca25ee72.pdf) (application/pdf, 17.0 KB)

## Timeline

### cl...@chromium.org (2019-04-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4764645324357632.

### cl...@chromium.org (2019-04-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-04-11)

Testcase 4764645324357632 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=4764645324357632.

### ct...@chromium.org (2019-04-11)

tsepez could you take a look? Clusterfuzz is having difficulty repro-ing in the standard linux_asan_chrome_mp job but I might be holding it wrong for pdfium bugs.

[Monorail components: Internals>Plugins>PDF]

### ct...@chromium.org (2019-04-11)

[Empty comment from Monorail migration]

### ct...@chromium.org (2019-04-11)

[Empty comment from Monorail migration]

### th...@chromium.org (2019-04-12)

Security_Impact-None since it's XFA-only.

### ts...@chromium.org (2019-04-16)

I'm getting a segv given an XFA-enabled pdfium_test at version 4fcc1f2.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-23)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/e9fa6a97fea60fcacb3088a6f012fb4dd218095e

commit e9fa6a97fea60fcacb3088a6f012fb4dd218095e
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Apr 23 17:45:40 2019

Check for possibility of inf value from FXSYS_wcstof()

Bug: chromium:951712
Change-Id: I9a4572aa9879e2c4ba374e78d37d9a959752318f
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/53310
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://crrev.com/e9fa6a97fea60fcacb3088a6f012fb4dd218095e/core/fxcrt/css/cfx_cssdeclaration.cpp
[modify] https://crrev.com/e9fa6a97fea60fcacb3088a6f012fb4dd218095e/core/fxcrt/fx_extension_unittest.cpp
[modify] https://crrev.com/e9fa6a97fea60fcacb3088a6f012fb4dd218095e/xfa/fxfa/parser/cxfa_measurement.cpp
[modify] https://crrev.com/e9fa6a97fea60fcacb3088a6f012fb4dd218095e/xfa/fxgraphics/cxfa_graphics.cpp
[modify] https://crrev.com/e9fa6a97fea60fcacb3088a6f012fb4dd218095e/core/fxcrt/fx_system.cpp


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

This issue was migrated from crbug.com/chromium/951712?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094562)*
