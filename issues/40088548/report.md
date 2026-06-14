# Heap-buffer-overflow in ClipRestore

| Field | Value |
|-------|-------|
| **Issue ID** | [40088548](https://issues.chromium.org/issues/40088548) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Reporter** | zh...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2017-07-31 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS
This issue was found by fuzzing against a 64-bit asan linux build of pdfium_test

The attached file crashes pdfium_test as follows:

Rendering PDF file /tmp/poc.
=================================================================
==19852==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x606000002e3c at pc 0x0000017256b6 bp 0x7ffc82af21e0 sp 0x7ffc82af21d8
READ of size 4 at 0x606000002e3c thread T0
    #0 0x17256b5 in ClipRestore core/fxge/skia/fx_skia_device.cpp:958:27
    #1 0x17256b5 in CFX_SkiaDeviceDriver::RestoreState(bool) core/fxge/skia/fx_skia_device.cpp:1540
    #2 0x170fba5 in CFX_RenderDevice::RestoreState(bool) core/fxge/ge/cfx_renderdevice.cpp:412:22
    #3 0x13087b0 in CPDF_RenderStatus::ProcessClipPath(CPDF_ClipPath, CFX_Matrix const*) core/fpdfapi/render/cpdf_renderstatus.cpp:1408:14
    #4 0x130bb8b in CPDF_RenderStatus::ContinueSingleObject(CPDF_PageObject*, CFX_Matrix const*, IFX_Pause*) core/fpdfapi/render/cpdf_renderstatus.cpp:1130:3
    #5 0x1303f68 in CPDF_ProgressiveRenderer::Continue(IFX_Pause*) core/fpdfapi/render/cpdf_progressiverenderer.cpp:83:30
    #6 0x5371ee in (anonymous namespace)::RenderPageImpl(CPDF_PageRenderContext*, CPDF_Page*, CFX_Matrix const&, FX_RECT const&, int, bool, IFSDK_PAUSE_Adapter*) fpdfsdk/fpdfview.cpp:120:26
    #7 0x5369a0 in FPDF_RenderPage_Retail fpdfsdk/fpdfview.cpp:1164:3
    #8 0x5369a0 in FPDF_RenderPageBitmap fpdfsdk/fpdfview.cpp:904
    #9 0x4fabbe in RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, void*, void*, FPDF_FORMFILLINFO_PDFiumTest&, int, Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:938:5
    #10 0x4fcc0f in RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:1166:9
    #11 0x4fde7d in main samples/pdfium_test.cc:1307:5
    #12 0x7f2100896f44 in __libc_start_main /build/eglibc-SvCtMH/eglibc-2.19/csu/libc-start.c:287

0x606000002e3c is located 4 bytes to the left of 52-byte region [0x606000002e40,0x606000002e74)
allocated by thread T0 here:
    #0 0x4ca445 in __interceptor_realloc (/home/henices/repo/pdfium/out/asan/pdfium_test+0x4ca445)
    #1 0x6be2dd in sk_realloc_throw(void*, unsigned long) third_party/skia/src/ports/SkMemory_malloc.cpp:63:35
    #2 0x17251b7 in resizeStorageToAtLeast third_party/skia/include/pathops/../private/SkTDArray.h:384:22
    #3 0x17251b7 in setCount third_party/skia/include/pathops/../private/SkTDArray.h:156
    #4 0x17251b7 in adjustCount third_party/skia/include/pathops/../private/SkTDArray.h:369
    #5 0x17251b7 in append third_party/skia/include/pathops/../private/SkTDArray.h:182
    #6 0x17251b7 in append third_party/skia/include/pathops/../private/SkTDArray.h:174
    #7 0x17251b7 in push third_party/skia/include/pathops/../private/SkTDArray.h:291
    #8 0x17251b7 in SkiaState::ClipSave() core/fxge/skia/fx_skia_device.cpp:947
    #9 0x1724cd3 in CFX_SkiaDeviceDriver::SaveState() core/fxge/skia/fx_skia_device.cpp:1516:18
    #10 0x1323978 in CPDF_RenderStatus::DrawTilingPattern(CPDF_TilingPattern*, CPDF_PageObject*, CFX_Matrix const*, bool) core/fpdfapi/render/cpdf_renderstatus.cpp:2206:35
    #11 0x130f7f2 in DrawPathWithPattern core/fpdfapi/render/cpdf_renderstatus.cpp:2396:5
    #12 0x130f7f2 in CPDF_RenderStatus::ProcessPathPattern(CPDF_PathObject*, CFX_Matrix const*, int&, bool&) core/fpdfapi/render/cpdf_renderstatus.cpp:2415
    #13 0x130dc31 in CPDF_RenderStatus::ProcessPath(CPDF_PathObject*, CFX_Matrix const*) core/fpdfapi/render/cpdf_renderstatus.cpp:1296:3
    #14 0x130b861 in CPDF_RenderStatus::ProcessObjectNoClip(CPDF_PageObject*, CFX_Matrix const*) core/fpdfapi/render/cpdf_renderstatus.cpp:1182:14
    #15 0x130bcad in CPDF_RenderStatus::ContinueSingleObject(CPDF_PageObject*, CFX_Matrix const*, IFX_Pause*) core/fpdfapi/render/cpdf_renderstatus.cpp:1146:3
    #16 0x1303f68 in CPDF_ProgressiveRenderer::Continue(IFX_Pause*) core/fpdfapi/render/cpdf_progressiverenderer.cpp:83:30
    #17 0x5371ee in (anonymous namespace)::RenderPageImpl(CPDF_PageRenderContext*, CPDF_Page*, CFX_Matrix const&, FX_RECT const&, int, bool, IFSDK_PAUSE_Adapter*) fpdfsdk/fpdfview.cpp:120:26
    #18 0x5369a0 in FPDF_RenderPage_Retail fpdfsdk/fpdfview.cpp:1164:3
    #19 0x5369a0 in FPDF_RenderPageBitmap fpdfsdk/fpdfview.cpp:904
    #20 0x4fabbe in RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, void*, void*, FPDF_FORMFILLINFO_PDFiumTest&, int, Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:938:5
    #21 0x4fcc0f in RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:1166:9
    #22 0x4fde7d in main samples/pdfium_test.cc:1307:5
    #23 0x7f2100896f44 in __libc_start_main /build/eglibc-SvCtMH/eglibc-2.19/csu/libc-start.c:287

SUMMARY: AddressSanitizer: heap-buffer-overflow core/fxge/skia/fx_skia_device.cpp:958:27 in ClipRestore
Shadow bytes around the buggy address:
  0x0c0c7fff8570: fa fa fa fa fd fd fd fd fd fd fd fd fa fa fa fa
  0x0c0c7fff8580: 00 00 00 00 00 00 00 fa fa fa fa fa 00 00 00 00
  0x0c0c7fff8590: 00 00 00 fa fa fa fa fa fd fd fd fd fd fd fd fa
  0x0c0c7fff85a0: fa fa fa fa fd fd fd fd fd fd fd fa fa fa fa fa
  0x0c0c7fff85b0: fd fd fd fd fd fd fd fa fa fa fa fa fd fd fd fd
=>0x0c0c7fff85c0: fd fd fd fa fa fa fa[fa]00 00 00 00 00 00 04 fa
  0x0c0c7fff85d0: fa fa fa fa fd fd fd fd fd fd fd fa fa fa fa fa
  0x0c0c7fff85e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c0c7fff85f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c0c7fff8600: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c0c7fff8610: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==19852==ABORTING

VERSION
latest asan build of pdfium_test (64-bit linux)

REPRODUCTION CASE
Attached in poc

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### cl...@chromium.org (2017-07-31)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5554371139207168.

### va...@chromium.org (2017-07-31)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### va...@chromium.org (2017-07-31)

[Empty comment from Monorail migration]

### th...@chromium.org (2017-07-31)

[Empty comment from Monorail migration]

### ts...@chromium.org (2017-08-08)

Skia => Not Shipping.

### ds...@chromium.org (2017-08-08)

[Empty comment from Monorail migration]

### ca...@google.com (2017-09-11)

Since pdf_use_skia_paths=false, lowering priority, decoupling from milestone

### ca...@google.com (2017-09-19)

[Empty comment from Monorail migration]

### ds...@chromium.org (2017-09-26)

[Empty comment from Monorail migration]

### mb...@chromium.org (2018-07-30)

This no longer seems to reproduce with pdf_use_skia_paths, so closing. Please reopen if there's reason to suspect that this isn't fixed.

### th...@chromium.org (2018-07-30)

I couldn't get this to repro. I tried these commits:

https://pdfium.googlesource.com/pdfium/+/95e5ac2a
https://pdfium.googlesource.com/pdfium/+/bde6f35d

with this build config:

is_debug = true
pdf_use_skia_paths = true
pdf_enable_xfa = true
pdf_enable_v8 = true
pdf_is_standalone = true
is_component_build = false
is_asan = true

### sh...@chromium.org (2018-07-31)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-08-13)

Thanks for the report, the VRP panel award $1,000. Cheers!

### aw...@google.com (2018-08-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-11-06)

This issue was migrated from crbug.com/chromium/750561?no_tracker_redirect=1

[Monorail blocking: crbug.com/pdfium/11]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088548)*
