# pdfium: signed-integer-overflow in AdjustGlyphSpace / CFX_DIBBase::GetOverlapRect

| Field | Value |
|-------|-------|
| **Issue ID** | [40093443](https://issues.chromium.org/issues/40093443) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Reporter** | pd...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2018-12-13 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.71 Safari/537.36

Steps to reproduce the problem:
I'm tentatively filing this as a security bug, as the code path doesn't seem to be used in Chrome easily.

https://cs.chromium.org/chromium/src/third_party/pdfium/core/fxge/cfx_renderdevice.cpp?l=952&rcl=4c91b17ead5c401472e4253169b66ffb017a9b57

A simple way is to add flag FPDF_RENDER_NO_SMOOTHTEXT to FPDF_RenderPageBitmap in pdfium_test.cc.

core/fxge/cfx_renderdevice.cpp:52:22: runtime error: signed integer overflow: -2147483648 + -1 cannot be represented in type 'int'

    #0 0x7f111318c93d in (anonymous namespace)::AdjustGlyphSpace(std::__1::vector<FXTEXT_GLYPHPOS, std::__1::allocator<FXTEXT_GLYPHPOS> >*) core/fxge/cfx_renderdevice.cpp:52:22
    #1 0x7f111318a150 in CFX_RenderDevice::DrawNormalText(int, FXTEXT_CHARPOS const*, CFX_Font*, float, CFX_Matrix const*, unsigned int, unsigned int) core/fxge/cfx_renderdevice.cpp:953:5
    #2 0x7f1112f95837 in CPDF_TextRenderer::DrawNormalText(CFX_RenderDevice*, std::__1::vector<unsigned int, std::__1::allocator<unsigned int> > const&, std::__1::vector<float, std::__1::allocator<float> > const&, CPDF_Font*, float, CFX_Matrix const*, unsigned int, CPDF_RenderOptions const*) core/fpdfapi/render/cpdf_textrenderer.cpp:160:17
    #3 0x7f1112f8a6a7 in CPDF_RenderStatus::ProcessText(CPDF_TextObject*, CFX_Matrix const&, CFX_PathData*) core/fpdfapi/render/cpdf_renderstatus.cpp:1779:10
    #4 0x7f1112f891ff in CPDF_RenderStatus::ProcessObjectNoClip(CPDF_PageObject*, CFX_Matrix const&) core/fpdfapi/render/cpdf_renderstatus.cpp:1139:14
    #5 0x7f1112f84e6e in CPDF_RenderStatus::ContinueSingleObject(CPDF_PageObject*, CFX_Matrix const&, PauseIndicatorIface*) core/fpdfapi/render/cpdf_renderstatus.cpp:1108:5
    #6 0x7f1112f833fd in CPDF_ProgressiveRenderer::Continue(PauseIndicatorIface*) core/fpdfapi/render/cpdf_progressiverenderer.cpp:95:30
    #7 0x7f1112d0e16d in (anonymous namespace)::RenderPageImpl(CPDF_PageRenderContext*, CPDF_Page*, CFX_Matrix const&, FX_RECT const&, int, bool, IPDFSDK_PauseAdapter*) fpdfsdk/fpdf_view.cpp:120:26
    #8 0x7f1112d09a3d in RenderPageWithContext(CPDF_PageRenderContext*, fpdf_page_t__*, int, int, int, int, int, int, bool, IPDFSDK_PauseAdapter*) fpdfsdk/fpdf_view.cpp:900:3
    #9 0x7f1112d09205 in FPDF_RenderPageBitmap_Start fpdfsdk/fpdf_progressive.cpp:59:3
    #10 0x7f1111801bfe in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:615:16
    #11 0x7f11117f8beb in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:825:9
    #12 0x7f11117f5446 in main samples/pdfium_test.cc:1002:5

core/fxge/cfx_renderdevice.cpp:48:29: runtime error: signed integer overflow: 2147483647 - -2147483648 cannot be represented in type 'int'

    #0 0x7f111318c92a in (anonymous namespace)::AdjustGlyphSpace(std::__1::vector<FXTEXT_GLYPHPOS, std::__1::allocator<FXTEXT_GLYPHPOS> >*) core/fxge/cfx_renderdevice.cpp:48:29
    #1 0x7f111318a150 in CFX_RenderDevice::DrawNormalText(int, FXTEXT_CHARPOS const*, CFX_Font*, float, CFX_Matrix const*, unsigned int, unsigned int) core/fxge/cfx_renderdevice.cpp:953:5
    #2 0x7f1112f95837 in CPDF_TextRenderer::DrawNormalText(CFX_RenderDevice*, std::__1::vector<unsigned int, std::__1::allocator<unsigned int> > const&, std::__1::vector<float, std::__1::allocator<float> > const&, CPDF_Font*, float, CFX_Matrix const*, unsigned int, CPDF_RenderOptions const*) core/fpdfapi/render/cpdf_textrenderer.cpp:160:17
    #3 0x7f1112f8a6a7 in CPDF_RenderStatus::ProcessText(CPDF_TextObject*, CFX_Matrix const&, CFX_PathData*) core/fpdfapi/render/cpdf_renderstatus.cpp:1779:10
    #4 0x7f1112f891ff in CPDF_RenderStatus::ProcessObjectNoClip(CPDF_PageObject*, CFX_Matrix const&) core/fpdfapi/render/cpdf_renderstatus.cpp:1139:14
    #5 0x7f1112f84e6e in CPDF_RenderStatus::ContinueSingleObject(CPDF_PageObject*, CFX_Matrix const&, PauseIndicatorIface*) core/fpdfapi/render/cpdf_renderstatus.cpp:1108:5
    #6 0x7f1112f833fd in CPDF_ProgressiveRenderer::Continue(PauseIndicatorIface*) core/fpdfapi/render/cpdf_progressiverenderer.cpp:95:30
    #7 0x7f1112d0e16d in (anonymous namespace)::RenderPageImpl(CPDF_PageRenderContext*, CPDF_Page*, CFX_Matrix const&, FX_RECT const&, int, bool, IPDFSDK_PauseAdapter*) fpdfsdk/fpdf_view.cpp:120:26
    #8 0x7f1112d09a3d in RenderPageWithContext(CPDF_PageRenderContext*, fpdf_page_t__*, int, int, int, int, int, int, bool, IPDFSDK_PauseAdapter*) fpdfsdk/fpdf_view.cpp:900:3
    #9 0x7f1112d09205 in FPDF_RenderPageBitmap_Start fpdfsdk/fpdf_progressive.cpp:59:3
    #10 0x7f1111801bfe in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:615:16
    #11 0x7f11117f8beb in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:825:9
    #12 0x7f11117f5446 in main samples/pdfium_test.cc:1002:5

core/fxge/dib/cfx_dibbase.cpp:890:24: runtime error: signed integer overflow: 0 - -2147483648 cannot be represented in type 'int'

    #0 0x7f111319af15 in CFX_DIBBase::GetOverlapRect(int&, int&, int&, int&, int, int, int&, int&, CFX_ClipRgn const*) core/fxge/dib/cfx_dibbase.cpp:890:24
    #1 0x7f111318ce27 in CFX_DIBitmap::TransferBitmap(int, int, int, int, fxcrt::RetainPtr<CFX_DIBBase> const&, int, int) core/fxge/dib/cfx_dibitmap.cpp:193:3
    #2 0x7f111318acda in CFX_RenderDevice::DrawNormalText(int, FXTEXT_CHARPOS const*, CFX_Font*, float, CFX_Matrix const*, unsigned int, unsigned int) core/fxge/cfx_renderdevice.cpp:973:15
    #3 0x7f1112f95837 in CPDF_TextRenderer::DrawNormalText(CFX_RenderDevice*, std::__1::vector<unsigned int, std::__1::allocator<unsigned int> > const&, std::__1::vector<float, std::__1::allocator<float> > const&, CPDF_Font*, float, CFX_Matrix const*, unsigned int, CPDF_RenderOptions const*) core/fpdfapi/render/cpdf_textrenderer.cpp:160:17
    #4 0x7f1112f8a6a7 in CPDF_RenderStatus::ProcessText(CPDF_TextObject*, CFX_Matrix const&, CFX_PathData*) core/fpdfapi/render/cpdf_renderstatus.cpp:1779:10
    #5 0x7f1112f891ff in CPDF_RenderStatus::ProcessObjectNoClip(CPDF_PageObject*, CFX_Matrix const&) core/fpdfapi/render/cpdf_renderstatus.cpp:1139:14
    #6 0x7f1112f84e6e in CPDF_RenderStatus::ContinueSingleObject(CPDF_PageObject*, CFX_Matrix const&, PauseIndicatorIface*) core/fpdfapi/render/cpdf_renderstatus.cpp:1108:5
    #7 0x7f1112f833fd in CPDF_ProgressiveRenderer::Continue(PauseIndicatorIface*) core/fpdfapi/render/cpdf_progressiverenderer.cpp:95:30
    #8 0x7f1112d0e16d in (anonymous namespace)::RenderPageImpl(CPDF_PageRenderContext*, CPDF_Page*, CFX_Matrix const&, FX_RECT const&, int, bool, IPDFSDK_PauseAdapter*) fpdfsdk/fpdf_view.cpp:120:26
    #9 0x7f1112d09a3d in RenderPageWithContext(CPDF_PageRenderContext*, fpdf_page_t__*, int, int, int, int, int, int, bool, IPDFSDK_PauseAdapter*) fpdfsdk/fpdf_view.cpp:900:3
    #10 0x7f1112d09205 in FPDF_RenderPageBitmap_Start fpdfsdk/fpdf_progressive.cpp:59:3
    #11 0x7f1111801bfe in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:615:16
    #12 0x7f11117f8beb in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:825:9
    #13 0x7f11117f5446 in main samples/pdfium_test.cc:1002:5

What is the expected behavior?

What went wrong?
^

Did this work before? N/A 

Chrome version: 70.0.3538.71  Channel: stable
OS Version: 
Flash Version:

## Attachments

- [chromium-914983.pdf](attachments/chromium-914983.pdf) (application/pdf, 417 B)
- [chromium-914983-2.pdf](attachments/chromium-914983-2.pdf) (application/pdf, 412 B)

## Timeline

### pd...@gmail.com (2018-12-13)

[Empty comment from Monorail migration]

### th...@chromium.org (2018-12-14)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### ca...@chromium.org (2018-12-14)

Running this on clusterfuzz (https://clusterfuzz.com/testcase-detail/6373157046583296). I typed in a mistaken bug number so the update won't automatically show up here though.

### cl...@chromium.org (2018-12-14)

Testcase 6373157046583296 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6373157046583296.

### cl...@chromium.org (2018-12-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6375896514297856.

### cl...@chromium.org (2018-12-14)

Testcase 6373157046583296 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6373157046583296.

### cl...@chromium.org (2018-12-14)

Testcase 6375896514297856 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6375896514297856.

### th...@chromium.org (2018-12-14)

I can reproduce this if I add the FPDF_RENDER_NO_SMOOTHTEXT option. It's definitely not used by Chromium and I'm not sure if any embedder is actually using it, as text smoothing is usually a desirable feature.

### th...@chromium.org (2018-12-14)

FWIW, I can't reproduce the integer overflow in AdjustGlyphSpace().

### pd...@gmail.com (2018-12-14)

It seems there are at least a few other paths to get less than FXFT_RENDER_MODE_LCD.

https://cs.chromium.org/chromium/src/third_party/pdfium/core/fxge/cfx_renderdevice.cpp?l=900&rcl=623e636edcd5d8582f7358f7b2f9a4f9636a899e

> FWIW, I can't reproduce the integer overflow in AdjustGlyphSpace().

Might depend on installed fonts? I don't know.

### ca...@chromium.org (2018-12-14)

Assigning high severity and impact stable out of an abundance of caution, but this would be impact none if the code is indeed unreachable from Chrome.

thestig: Can you help find an owner for this? Thanks

### th...@chromium.org (2018-12-14)

Yep, there are several rendering options, with 2^N combinations, and we don't test them all.

I'll try to fix the AdjustGlyphSpace() issue blindly too.

### bu...@chromium.org (2018-12-14)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/41ca949d4cedf9eb1ad3dca26c4ccba4cbf3609e

commit 41ca949d4cedf9eb1ad3dca26c4ccba4cbf3609e
Author: Lei Zhang <thestig@chromium.org>
Date: Fri Dec 14 23:59:45 2018

Fix integer overflow in CFX_DIBBase::GetOverlapRect().

BUG=chromium:914983

Change-Id: I2c248c7af1c19b419925c87341491a2b98beea66
Reviewed-on: https://pdfium-review.googlesource.com/c/47271
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[modify] https://crrev.com/41ca949d4cedf9eb1ad3dca26c4ccba4cbf3609e/core/fxge/dib/cfx_dibbase.cpp


### bu...@chromium.org (2018-12-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0ada588cc118f459067de0d9bad1b1f76b2eaa7f

commit 0ada588cc118f459067de0d9bad1b1f76b2eaa7f
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Sat Dec 15 04:41:15 2018

Roll src/third_party/pdfium 3de08dd61026..a0c36804be26 (12 commits)

https://pdfium.googlesource.com/pdfium.git/+log/3de08dd61026..a0c36804be26


git log 3de08dd61026..a0c36804be26 --date=short --no-merges --format='%ad %ae %s'
2018-12-15 thestig@chromium.org Split part of xfa/fgas/BUILD.gn into xfa/fgas/layout/BUILD.gn.
2018-12-15 thestig@chromium.org Fix nits in CFX_TxtBreak and related code.
2018-12-15 thestig@chromium.org Avoid unnecessary list initialization in CJX_Object.
2018-12-15 thestig@chromium.org Remove most non-const reference parameters in CJX_Object.
2018-12-14 thestig@chromium.org Fix integer overflow in CFX_DIBBase::GetOverlapRect().
2018-12-14 thestig@chromium.org Give CFX_DIBBase::GetOverlapRect() a return value.
2018-12-14 thestig@chromium.org Break circular dependency between formfiller and pwl.
2018-12-14 thestig@chromium.org Remove non-const parameter in CXFA_ItemLayoutProcessor.
2018-12-14 thestig@chromium.org Merge CPWL_FontMap into CBA_FontMap.
2018-12-14 thestig@chromium.org Add CXFA_ItemLayoutProcessor::GotoNextContainerNodeSimple().
2018-12-14 thestig@chromium.org Get rid of some #defines in XFA code.
2018-12-14 tsepez@chromium.org XFA: Avoid infinite recursion when deleting a ThisProxy object property.


Created with:
  gclient setdep -r src/third_party/pdfium@a0c36804be26

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:914983,chromium:913566
TBR=dsinclair@chromium.org

Change-Id: Iec871196c04a7950c8d11dc53ef7bd2f59af2427
Reviewed-on: https://chromium-review.googlesource.com/c/1378840
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#616951}
[modify] https://crrev.com/0ada588cc118f459067de0d9bad1b1f76b2eaa7f/DEPS


### sh...@chromium.org (2018-12-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-29)

thestig: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pd...@gmail.com (2019-01-07)

To reproduce in Chromium the PDF needs to be rendered without subpixel-rendering (LCD). In addition to the path in https://crbug.com/chromium/914983#c10 I noticed #lcd-text-aa in chrome://flags which disables exactly that. I don't know if that's actually passed down to pdfium. So I assume it can reproduce in Chromium, but only with uncommon configurations.

Also I can't reproduce AdjustGlyphSpace either now. The integer has changed to -2140733312 from -2147483648. I assume there were some unrelated changes along the way. Anyway, I'm attaching an update case that does reproduce with 92770e8072cd3a38597966116045147c78b5a359.

### sh...@chromium.org (2019-01-12)

thestig: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### th...@chromium.org (2019-02-07)

https://pdfium-review.googlesource.com/c/pdfium/+/50112

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-02-07)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/3548a6b6fbd37b727a2c0a5fac2a6b22ddef92d5

commit 3548a6b6fbd37b727a2c0a5fac2a6b22ddef92d5
Author: Lei Zhang <thestig@chromium.org>
Date: Thu Feb 07 18:45:58 2019

Check for integer overflows in AdjustGlyphSpace().

BUG=chromium:914983

Change-Id: I90f0ae85e547efbe52a27d32a06af10ed65d6722
Reviewed-on: https://pdfium-review.googlesource.com/c/50112
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[modify] https://crrev.com/3548a6b6fbd37b727a2c0a5fac2a6b22ddef92d5/core/fxge/cfx_renderdevice.cpp


### th...@chromium.org (2019-02-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-10)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-02-11)

[Empty comment from Monorail migration]

### na...@google.com (2019-02-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-02-13)

Congrats! The Panel decided to reward $500 for this report :) 

### aw...@chromium.org (2019-02-14)

abdulsyed@ - good for 73

### ab...@google.com (2019-02-15)

branch:3683

### th...@chromium.org (2019-02-15)

https://pdfium-review.googlesource.com/c/pdfium/+/50892

### aw...@google.com (2019-02-20)

[Empty comment from Monorail migration]

### aw...@google.com (2019-03-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-05-22)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/914983?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093443)*
