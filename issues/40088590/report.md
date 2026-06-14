# Security: stack-buffer-overflow in SkPoint

| Field | Value |
|-------|-------|
| **Issue ID** | [40088590](https://issues.chromium.org/issues/40088590) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF, Internals>Skia>PDF |
| **Platforms** | Linux |
| **Reporter** | yu...@gmail.com |
| **Assignee** | hn...@chromium.org |
| **Created** | 2017-08-03 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36

Steps to reproduce the problem:
VULNERABILITY DETAILS
==8520:8520==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7fedd59051e8 at pc 0x00000381061d bp 0x7ffd98b1e490 sp 0x7ffd98b1e488
READ of size 4 at 0x7fedd59051e8 thread T0
    #0 0x381061c in operator- third_party/skia/include/core/SkPoint.h:419:24
    #1 0x381061c in IntersectSides third_party/pdfium/core/fxge/skia/fx_skia_device.cpp:462
    #2 0x381061c in ClipAngledGradient third_party/pdfium/core/fxge/skia/fx_skia_device.cpp:536
    #3 0x381061c in CFX_SkiaDeviceDriver::DrawShading(CPDF_ShadingPattern const*, CFX_Matrix const*, FX_RECT const&, int, bool) third_party/pdfium/core/fxge/skia/fx_skia_device.cpp:2073
    #4 0x336ebe9 in CPDF_RenderStatus::DrawShading(CPDF_ShadingPattern*, CFX_Matrix*, FX_RECT&, int, bool) third_party/pdfium/core/fpdfapi/render/cpdf_renderstatus.cpp:2083:37
    #5 0x335fdce in CPDF_RenderStatus::ProcessShading(CPDF_ShadingObject const*, CFX_Matrix const*) third_party/pdfium/core/fpdfapi/render/cpdf_renderstatus.cpp:2185:3
    #6 0x335c6c1 in CPDF_RenderStatus::ProcessObjectNoClip(CPDF_PageObject*, CFX_Matrix const*) third_party/pdfium/core/fpdfapi/render/cpdf_renderstatus.cpp:1179:7
    #7 0x335cca8 in CPDF_RenderStatus::ContinueSingleObject(CPDF_PageObject*, CFX_Matrix const*, IFX_Pause*) third_party/pdfium/core/fpdfapi/render/cpdf_renderstatus.cpp:1137:3
    #8 0x3354252 in CPDF_ProgressiveRenderer::Continue(IFX_Pause*) third_party/pdfium/core/fpdfapi/render/cpdf_progressiverenderer.cpp:81:30
    #9 0x21cebcb in (anonymous namespace)::RenderPageImpl(CPDF_PageRenderContext*, CPDF_Page*, CFX_Matrix const&, FX_RECT const&, int, bool, IFSDK_PAUSE_Adapter*) third_party/pdfium/fpdfsdk/fpdfview.cpp:127:26
    #10 0x21ce47e in FPDF_RenderPage_Retail(CPDF_PageRenderContext*, void*, int, int, int, int, int, int, bool, IFSDK_PAUSE_Adapter*) third_party/pdfium/fpdfsdk/fpdfview.cpp:1182:3
    #11 0x21c03b0 in FPDF_RenderPageBitmap_Start third_party/pdfium/fpdfsdk/fpdf_progressive.cpp:60:3
    #12 0x4fdb42 in RenderPage third_party/pdfium/samples/pdfium_test.cc:1171:16
    #13 0x4fdb42 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) third_party/pdfium/samples/pdfium_test.cc:1367
    #14 0x4f7c00 in main third_party/pdfium/samples/pdfium_test.cc:1526:5
    #15 0x7feddd3d882f in __libc_start_main /build/glibc-bfm8X4/glibc-2.23/csu/../csu/libc-start.c:291

Address 0x7fedd59051e8 is located in stack of thread T0 at offset 488 in frame
    #0 0x380bfff in CFX_SkiaDeviceDriver::DrawShading(CPDF_ShadingPattern const*, CFX_Matrix const*, FX_RECT const&, int, bool) third_party/pdfium/core/fxge/skia/fx_skia_device.cpp:1980

  This frame has 19 object(s):
    [32, 40) 'ref.tmp' (line 1997)
    [64, 80) 'skColors' (line 2002)
    [96, 104) 'ref.tmp73' (line 2027)
    [128, 224) 'paint' (line 2030)
    [256, 296) 'skMatrix' (line 2033)
    [336, 352) 'skRect' (line 2034)
    [368, 384) 'skClip' (line 2036)
    [400, 416) 'skPath' (line 2037)
    [432, 448) 'pts' (line 2043)
    [464, 472) 'agg.tmp'
    [496, 528) 'rectPts' (line 2069) <== Memory access at offset 488 underflows this variable
    [560, 576) 'pts209' (line 2085)
    [592, 600) 'agg.tmp216'
    [624, 664) 'inverse' (line 2099)
    [704, 864) 'stream' (line 2109)
    [928, 1024) 'cubics' (line 2113)
    [1056, 1072) 'colors' (line 2114)
    [1088, 1120) 'tempCubics' (line 2124)
    [1152, 1160) 'point' (line 2134)
HINT: this may be a false positive if your program uses some custom stack unwind mechanism or swapcontext
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow third_party/skia/include/core/SkPoint.h:419:24 in operator-
Shadow bytes around the buggy address:
  0x0ffe3ab189e0: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x0ffe3ab189f0: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x0ffe3ab18a00: f1 f1 f1 f1 f8 f2 f2 f2 00 00 f2 f2 f8 f2 f2 f2
  0x0ffe3ab18a10: 00 00 00 00 00 00 00 00 00 00 00 00 f2 f2 f2 f2
  0x0ffe3ab18a20: 00 00 00 00 00 f2 f2 f2 f2 f2 00 00 f2 f2 00 00
=>0x0ffe3ab18a30: f2 f2 00 00 f2 f2 00 00 f2 f2 00 f2 f2[f2]00 00
  0x0ffe3ab18a40: 00 00 f2 f2 f2 f2 f8 f8 f2 f2 00 f2 f2 f2 f8 f8
  0x0ffe3ab18a50: f8 f8 f8 f2 f2 f2 f2 f2 f8 f8 f8 f8 f8 f8 f8 f8
  0x0ffe3ab18a60: f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f2 f2 f2 f2
  0x0ffe3ab18a70: f2 f2 f2 f2 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8
  0x0ffe3ab18a80: f2 f2 f2 f2 f8 f8 f2 f2 f8 f8 f8 f8 f2 f2 f2 f2
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
==8520:8520==ABORTING

VERSION
commit 224091ca04a0477907b9efb559391f2c5f6c125f
Linux ubuntu 4.10.0-27-generic #30~16.04.2-Ubuntu SMP Thu Jun 29 16:07:46 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux

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
stack-buffer-overflow in SkPoint

Did this work before? N/A 

Chrome version: 60.0.3112.78  Channel: stable
OS Version: 10.0
Flash Version:

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 44.8 KB)

## Timeline

### el...@chromium.org (2017-08-03)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF Internals>Skia>PDF]

### cl...@chromium.org (2017-08-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5565630580523008.

### ts...@chromium.org (2017-08-08)

Requires pdf_use_skia_paths=true => Not shipping (yet).

### ts...@chromium.org (2017-08-08)

Does NOT require XFA, though.  

### ds...@chromium.org (2017-08-08)

[Empty comment from Monorail migration]

### ca...@chromium.org (2017-08-23)

[Empty comment from Monorail migration]

### ca...@google.com (2017-09-11)

Since pdf_use_skia_paths=false, lowering priority, decoupling from milestone

### ca...@google.com (2017-09-19)

[Empty comment from Monorail migration]

### ds...@chromium.org (2017-09-26)

[Empty comment from Monorail migration]

### mb...@chromium.org (2018-07-30)

This no longer seems to reproduce with the gn args specified above. Going to close it out, but if there's reason to suspect that this might not be fixed please reopen.

### th...@chromium.org (2018-07-30)

Fixed by https://pdfium.googlesource.com/pdfium/+/30ef542b6f631f0ffbcd4110857e7c1a304a8a23

### sh...@chromium.org (2018-07-31)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-08-13)

Nice one yuanvi.cn@! The VRP panel decided to award $1,000 for this report. Also, how would you like to be credited in Chrome release notes?

### aw...@google.com (2018-08-13)

[Empty comment from Monorail migration]

### yu...@gmail.com (2018-08-14)

Thanks, please credit to [Wei Yuan of Baidu Security Lab].

### sh...@chromium.org (2018-11-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-11-06)

This issue was migrated from crbug.com/chromium/751921?no_tracker_redirect=1

[Multiple monorail components: Internals>Plugins>PDF, Internals>Skia>PDF]
[Monorail blocking: crbug.com/pdfium/11]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088590)*
