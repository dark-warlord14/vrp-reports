# heap-buffer-overflow in SkMatrix::setRSXform

| Field | Value |
|-------|-------|
| **Issue ID** | [40088576](https://issues.chromium.org/issues/40088576) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF, Internals>Skia>PDF |
| **Platforms** | Linux |
| **Reporter** | yu...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2017-08-02 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36

Steps to reproduce the problem:
VULNERABILITY DETAILS
==18940:18940==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x610000008300 at pc 0x00000223ffb4 bp 0x7fff7e7e7f30 sp 0x7fff7e7e7f28
READ of size 4 at 0x610000008300 thread T0
    #0 0x223ffb3 in SkMatrix::setRSXform(SkRSXform const&) third_party/skia/src/core/SkMatrix.cpp:452:29
    #1 0x22fcea5 in SkBaseDevice::drawTextRSXform(void const*, unsigned long, SkRSXform const*, SkPaint const&) third_party/skia/src/core/SkDevice.cpp:480:16
    #2 0x22b1929 in SkCanvas::onDrawTextRSXform(void const*, unsigned long, SkRSXform const*, SkRect const*, SkPaint const&) third_party/skia/src/core/SkCanvas.cpp:2524:23
    #3 0x22b4311 in SkCanvas::drawTextRSXform(void const*, unsigned long, SkRSXform const*, SkRect const*, SkPaint const&) third_party/skia/src/core/SkCanvas.cpp:2598:15
    #4 0x38169f0 in SkiaState::FlushText() third_party/pdfium/core/fxge/skia/fx_skia_device.cpp:934:17
    #5 0x3804c2f in Flush third_party/pdfium/core/fxge/skia/fx_skia_device.cpp:1171:52
    #6 0x3804c2f in SkiaState::DrawText(int, FXTEXT_CHARPOS const*, CFX_Font*, CFX_Matrix const*, float, unsigned int) third_party/pdfium/core/fxge/skia/fx_skia_device.cpp:845
    #7 0x38017b9 in CFX_SkiaDeviceDriver::DrawDeviceText(int, FXTEXT_CHARPOS const*, CFX_Font*, CFX_Matrix const*, float, unsigned int) third_party/pdfium/core/fxge/skia/fx_skia_device.cpp:1556:17
    #8 0x378e420 in CFX_RenderDevice::DrawNormalText(int, FXTEXT_CHARPOS const*, CFX_Font*, float, CFX_Matrix const*, unsigned int, unsigned int) third_party/pdfium/core/fxge/cfx_renderdevice.cpp:875:26
    #9 0x3387972 in CPDF_TextRenderer::DrawNormalText(CFX_RenderDevice*, std::__1::vector<unsigned int, std::__1::allocator<unsigned int> > const&, std::__1::vector<float, std::__1::allocator<float> > const&, CPDF_Font*, float, CFX_Matrix const*, unsigned int, CPDF_RenderOptions const*) third_party/pdfium/core/fpdfapi/render/cpdf_textrenderer.cpp:156:19
    #10 0x335e7b5 in CPDF_RenderStatus::ProcessText(CPDF_TextObject*, CFX_Matrix const*, CFX_PathData*) third_party/pdfium/core/fpdfapi/render/cpdf_renderstatus.cpp:1813:10
    #11 0x335c527 in CPDF_RenderStatus::ProcessObjectNoClip(CPDF_PageObject*, CFX_Matrix const*) third_party/pdfium/core/fpdfapi/render/cpdf_renderstatus.cpp:1170:14
    #12 0x335cca8 in CPDF_RenderStatus::ContinueSingleObject(CPDF_PageObject*, CFX_Matrix const*, IFX_Pause*) third_party/pdfium/core/fpdfapi/render/cpdf_renderstatus.cpp:1137:3
    #13 0x3354252 in CPDF_ProgressiveRenderer::Continue(IFX_Pause*) third_party/pdfium/core/fpdfapi/render/cpdf_progressiverenderer.cpp:81:30
    #14 0x21cebcb in (anonymous namespace)::RenderPageImpl(CPDF_PageRenderContext*, CPDF_Page*, CFX_Matrix const&, FX_RECT const&, int, bool, IFSDK_PAUSE_Adapter*) third_party/pdfium/fpdfsdk/fpdfview.cpp:127:26
    #15 0x21ce47e in FPDF_RenderPage_Retail(CPDF_PageRenderContext*, void*, int, int, int, int, int, int, bool, IFSDK_PAUSE_Adapter*) third_party/pdfium/fpdfsdk/fpdfview.cpp:1182:3
    #16 0x21c03b0 in FPDF_RenderPageBitmap_Start third_party/pdfium/fpdfsdk/fpdf_progressive.cpp:60:3
    #17 0x4fdb42 in RenderPage third_party/pdfium/samples/pdfium_test.cc:1171:16
    #18 0x4fdb42 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) third_party/pdfium/samples/pdfium_test.cc:1367
    #19 0x4f7c00 in main third_party/pdfium/samples/pdfium_test.cc:1526:5
    #20 0x7f021657782f in __libc_start_main /build/glibc-bfm8X4/glibc-2.23/csu/../csu/libc-start.c:291

0x610000008300 is located 0 bytes to the right of 192-byte region [0x610000008240,0x610000008300)
allocated by thread T0 here:
    #0 0x4c9237 in __interceptor_realloc (/home/chrome/chromium/src/out/pdf/pdfium_test+0x4c9237)
    #1 0x2278af3 in sk_realloc_throw(void*, unsigned long) skia/ext/SkMemory_new_handler.cpp:43:35
    #2 0x3804109 in resizeStorageToAtLeast third_party/skia/include/pathops/../private/SkTDArray.h:384:22
    #3 0x3804109 in setCount third_party/skia/include/pathops/../private/SkTDArray.h:156
    #4 0x3804109 in SkiaState::DrawText(int, FXTEXT_CHARPOS const*, CFX_Font*, CFX_Matrix const*, float, unsigned int) third_party/pdfium/core/fxge/skia/fx_skia_device.cpp:862
    #5 0x38017b9 in CFX_SkiaDeviceDriver::DrawDeviceText(int, FXTEXT_CHARPOS const*, CFX_Font*, CFX_Matrix const*, float, unsigned int) third_party/pdfium/core/fxge/skia/fx_skia_device.cpp:1556:17
    #6 0x378e420 in CFX_RenderDevice::DrawNormalText(int, FXTEXT_CHARPOS const*, CFX_Font*, float, CFX_Matrix const*, unsigned int, unsigned int) third_party/pdfium/core/fxge/cfx_renderdevice.cpp:875:26
    #7 0x3387a92 in CPDF_TextRenderer::DrawNormalText(CFX_RenderDevice*, std::__1::vector<unsigned int, std::__1::allocator<unsigned int> > const&, std::__1::vector<float, std::__1::allocator<float> > const&, CPDF_Font*, float, CFX_Matrix const*, unsigned int, CPDF_RenderOptions const*) third_party/pdfium/core/fpdfapi/render/cpdf_textrenderer.cpp:165:17
    #8 0x335e7b5 in CPDF_RenderStatus::ProcessText(CPDF_TextObject*, CFX_Matrix const*, CFX_PathData*) third_party/pdfium/core/fpdfapi/render/cpdf_renderstatus.cpp:1813:10
    #9 0x335c527 in CPDF_RenderStatus::ProcessObjectNoClip(CPDF_PageObject*, CFX_Matrix const*) third_party/pdfium/core/fpdfapi/render/cpdf_renderstatus.cpp:1170:14
    #10 0x335cca8 in CPDF_RenderStatus::ContinueSingleObject(CPDF_PageObject*, CFX_Matrix const*, IFX_Pause*) third_party/pdfium/core/fpdfapi/render/cpdf_renderstatus.cpp:1137:3
    #11 0x3354252 in CPDF_ProgressiveRenderer::Continue(IFX_Pause*) third_party/pdfium/core/fpdfapi/render/cpdf_progressiverenderer.cpp:81:30
    #12 0x21cebcb in (anonymous namespace)::RenderPageImpl(CPDF_PageRenderContext*, CPDF_Page*, CFX_Matrix const&, FX_RECT const&, int, bool, IFSDK_PAUSE_Adapter*) third_party/pdfium/fpdfsdk/fpdfview.cpp:127:26
    #13 0x21ce47e in FPDF_RenderPage_Retail(CPDF_PageRenderContext*, void*, int, int, int, int, int, int, bool, IFSDK_PAUSE_Adapter*) third_party/pdfium/fpdfsdk/fpdfview.cpp:1182:3
    #14 0x21c03b0 in FPDF_RenderPageBitmap_Start third_party/pdfium/fpdfsdk/fpdf_progressive.cpp:60:3
    #15 0x4fdb42 in RenderPage third_party/pdfium/samples/pdfium_test.cc:1171:16
    #16 0x4fdb42 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) third_party/pdfium/samples/pdfium_test.cc:1367
    #17 0x4f7c00 in main third_party/pdfium/samples/pdfium_test.cc:1526:5
    #18 0x7f021657782f in __libc_start_main /build/glibc-bfm8X4/glibc-2.23/csu/../csu/libc-start.c:291

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/skia/src/core/SkMatrix.cpp:452:29 in SkMatrix::setRSXform(SkRSXform const&)
Shadow bytes around the buggy address:
  0x0c207fff9010: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa
  0x0c207fff9020: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c207fff9030: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c207fff9040: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x0c207fff9050: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c207fff9060:[fa]fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x0c207fff9070: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 fa
  0x0c207fff9080: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c207fff9090: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c207fff90a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c207fff90b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==18940:18940==ABORTING

VERSION
commit 224091ca04a0477907b9efb559391f2c5f6c125f

REPRODUCTION CASE
build pdfium_test with these options
```
is_asan = true
is_debug = false

pdf_use_skia_paths = true
pdf_enable_v8 = true
pdf_enable_xfa = true
pdf_enable_xfa_bmp = true
pdf_enable_xfa_gif = true
pdf_enable_xfa_png = true
pdf_enable_xfa_tiff = true
```
./pdfium_test poc.pdf

What is the expected behavior?

What went wrong?
heap-buffer-overflow in SkMatrix::setRSXform

Did this work before? N/A 

Chrome version: 60.0.3112.78  Channel: stable
OS Version: 10.0
Flash Version:

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 13.7 KB)

## Timeline

### yu...@gmail.com (2017-08-03)

Sorry for my mistake, i test this case on Linux, not Windows.

Linux ubuntu 4.10.0-27-generic #30~16.04.2-Ubuntu SMP Thu Jun 29 16:07:46 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux

### el...@chromium.org (2017-08-03)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF Internals>Skia>PDF]

### cl...@chromium.org (2017-08-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6291417440976896.

### ts...@chromium.org (2017-08-08)

Requires pdf_use_skia_paths=true => Not shipping (yet).
Does NOT require XFA.

### ca...@chromium.org (2017-08-23)

[Empty comment from Monorail migration]

### ca...@google.com (2017-09-11)

Since pdf_use_skia_paths=false, lowering priority, decoupling from milestone

### ca...@google.com (2017-09-19)

[Empty comment from Monorail migration]

### ds...@chromium.org (2017-09-26)

[Empty comment from Monorail migration]

### mm...@chromium.org (2017-11-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-07-30)

Testcase 6291417440976896 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6291417440976896.

### aa...@google.com (2018-07-30)

[Empty comment from Monorail migration]

### th...@chromium.org (2018-07-30)

https://pdfium-review.googlesource.com/c/pdfium/+/39153

### mb...@chromium.org (2018-07-30)

Looks like the Security_Impact label was switched incorrectly.

### bu...@chromium.org (2018-08-02)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/7c43678627e7797aefd3f74e0446f4dd0fea67cf

commit 7c43678627e7797aefd3f74e0446f4dd0fea67cf
Author: Lei Zhang <thestig@chromium.org>
Date: Thu Aug 02 23:21:38 2018

Skia Path: Fix text/xform size mismatch when calling drawTextRSXform().

BUG=chromium:751423

Change-Id: I2fcc46b80e89cb651e255bd1fd2d6883a05cf9c7
Reviewed-on: https://pdfium-review.googlesource.com/39153
Reviewed-by: Cary Clark <caryclark@google.com>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[modify] https://crrev.com/7c43678627e7797aefd3f74e0446f4dd0fea67cf/core/fxge/skia/fx_skia_device.cpp


### th...@chromium.org (2018-08-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-08-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/cde09d49aec4ad82c55d54fa2dda99c4b5caf4b1

commit cde09d49aec4ad82c55d54fa2dda99c4b5caf4b1
Author: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Fri Aug 03 04:04:25 2018

Roll src/third_party/pdfium 95340100f95f..2958a8faf500 (3 commits)

https://pdfium.googlesource.com/pdfium.git/+log/95340100f95f..2958a8faf500


git log 95340100f95f..2958a8faf500 --date=short --no-merges --format='%ad %ae %s'
2018-08-02 tsepez@chromium.org Use more helper macros/methods in JBig2_Image.cpp.
2018-08-02 thestig@chromium.org Fix some nits in SkiaState.
2018-08-02 thestig@chromium.org Skia Path: Fix text/xform size mismatch when calling drawTextRSXform().


Created with:
  gclient setdep -r src/third_party/pdfium@2958a8faf500

The AutoRoll server is located here: https://pdfium-roll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:751423
TBR=dsinclair@chromium.org

Change-Id: I57dc7b1e7ab52e06e0b3ad22952be79cd6d6561b
Reviewed-on: https://chromium-review.googlesource.com/1161345
Reviewed-by: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Commit-Queue: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#580446}
[modify] https://crrev.com/cde09d49aec4ad82c55d54fa2dda99c4b5caf4b1/DEPS


### sh...@chromium.org (2018-08-03)

[Empty comment from Monorail migration]

### aw...@google.com (2018-11-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-11-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-11-12)

Thanks for the report, yuanvi.cn@. The Chrome VRP panel decided to award $500 for this, noting that this code path is very unlikely to ship to users.


### aw...@google.com (2018-11-12)

[Empty comment from Monorail migration]

### is...@google.com (2018-11-12)

This issue was migrated from crbug.com/chromium/751423?no_tracker_redirect=1

[Multiple monorail components: Internals>Plugins>PDF, Internals>Skia>PDF]
[Monorail blocking: crbug.com/pdfium/11]
[Monorail mergedwith: crbug.com/chromium/786263]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088576)*
