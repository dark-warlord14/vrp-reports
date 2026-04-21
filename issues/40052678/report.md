# Security: heap-buffer-overflow in "SkData::PrivateNewWithCopy" function

| Field | Value |
|-------|-------|
| **Issue ID** | [40052678](https://issues.chromium.org/issues/40052678) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF, Internals>Skia |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | cp...@stevens.edu |
| **Assignee** | th...@chromium.org |
| **Created** | 2020-06-25 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**

Hi, our developed fuzzer found a heap-buffer-overflow bug in "SkData::PrivateNewWithCopy" when fuzzing pdfium\_test.

In this function:  

sk\_sp<SkData> SkData::PrivateNewWithCopy(const void\* srcOrNull, size\_t length) {  

if (0 == length) {  

return SkData::MakeEmpty();  

}

```
const size_t actualLength = length + sizeof(SkData);  
SkASSERT_RELEASE(length < actualLength);  // Check for overflow.  

void\* storage = ::operator new (actualLength);  
sk_sp<SkData> data(new (storage) SkData(length));  
if (srcOrNull) {  
    // heap-buffer-overflow occurs here.  
    // the length of ``srcOrNull" buffer is 68 bytes  
    // while ``length" equals 256  
    memcpy(data->writable_data(), srcOrNull, length);  
}  
return data;  

```

}

The ``length'' is affected by input file.

Here is the log from ASAN:

```
==50070==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x607000000a04 at pc 0x55cc590178a7 bp 0x7ffc007a9ff0 sp 0x7ffc007a97b8  
READ of size 256 at 0x607000000a04 thread T0  
    #0 0x55cc590178a6 in __asan_memcpy /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors_memintrinsics.cpp:22:3  
    #1 0x55cc598cd658 in SkData::PrivateNewWithCopy(void const\*, unsigned long) third_party/skia/src/core/SkData.cpp:79:9  
    #2 0x55cc598cdd2d in SkData::MakeWithCopy(void const\*, unsigned long) third_party/skia/src/core/SkData.cpp:107:12  
    #3 0x55cc5a8f955b in MakeRasterCopyPriv(SkPixmap const&, unsigned int) third_party/skia/src/image/SkImage_Raster.cpp:266:24  
    #4 0x55cc5a8fa72f in SkMakeImageFromRasterBitmapPriv(SkBitmap const&, SkCopyPixelsMode, unsigned int) third_party/skia/src/image/SkImage_Raster.cpp:338:20  
    #5 0x55cc5a8fa930 in SkMakeImageFromRasterBitmap(SkBitmap const&, SkCopyPixelsMode) third_party/skia/src/image/SkImage_Raster.cpp:352:12  
    #6 0x55cc5a8e2f94 in SkImage::MakeFromBitmap(SkBitmap const&) third_party/skia/src/image/SkImage.cpp:219:12  
    #7 0x55cc598323d5 in bitmap_as_image(SkBitmap const&) third_party/skia/src/core/SkCanvas.cpp:2101:12  
    #8 0x55cc598322e6 in SkCanvas::drawBitmap(SkBitmap const&, float, float, SkPaint const\*) third_party/skia/src/core/SkCanvas.cpp:2105:21  
    #9 0x55cc59709005 in CFX_SkiaDeviceDriver::GetDIBits(fxcrt::RetainPtr<CFX_DIBitmap> const&, int, int) core/fxge/skia/fx_skia_device.cpp:2376:10  
    #10 0x55cc596407b1 in CFX_RenderDevice::GetDIBits(fxcrt::RetainPtr<CFX_DIBitmap> const&, int, int) core/fxge/cfx_renderdevice.cpp:724:27  
    #11 0x55cc5bb91801 in CPDF_RenderStatus::ProcessTransparency(CPDF_PageObject\*, CFX_Matrix const&) core/fpdfapi/render/cpdf_renderstatus.cpp:669:16  
    #12 0x55cc5bb8fcdd in CPDF_RenderStatus::RenderSingleObject(CPDF_PageObject\*, CFX_Matrix const&) core/fpdfapi/render/cpdf_renderstatus.cpp:262:7  
    #13 0x55cc5bb8f8e1 in CPDF_RenderStatus::RenderObjectList(CPDF_PageObjectHolder const\*, CFX_Matrix const&) core/fpdfapi/render/cpdf_renderstatus.cpp:238:5  
    #14 0x55cc5bb755b0 in CPDF_RenderContext::Render(CFX_RenderDevice\*, CPDF_PageObject const\*, CPDF_RenderOptions const\*, CFX_Matrix const\*) core/fpdfapi/render/cpdf_rendercontext.cpp:75:12  
    #15 0x55cc5bb75871 in CPDF_RenderContext::Render(CFX_RenderDevice\*, CPDF_RenderOptions const\*, CFX_Matrix const\*) core/fpdfapi/render/cpdf_rendercontext.cpp:55:3  
  
0x607000000a04 is located 0 bytes to the right of 68-byte region [0x6070000009c0,0x607000000a04)  
allocated by thread T0 here:  
    #0 0x55cc590185b2 in calloc /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3  
    #1 0x55cc592b8a31 in pdfium::base::PartitionAllocGenericFlags(pdfium::base::PartitionRootGeneric\*, int, unsigned long, char const\*) third_party/base/allocator/partition_allocator/partition_alloc.h:403:30  
    #2 0x55cc592b808f in internal::Calloc(unsigned long, unsigned long) core/fxcrt/fx_memory.cpp:112:10  
    #3 0x55cc592b871c in internal::CallocOrDie(unsigned long, unsigned long) core/fxcrt/fx_memory.cpp:130:18  
    #4 0x55cc5967451e in CFX_DIBitmap::Create(int, int, FXDIB_Format, unsigned char\*, unsigned int) core/fxge/dib/cfx_dibitmap.cpp:65:11  
    #5 0x55cc59673f5e in CFX_DIBitmap::Create(int, int, FXDIB_Format) core/fxge/dib/cfx_dibitmap.cpp:35:10  
    #6 0x55cc5bba57d9 in (anonymous namespace)::DrawPatternBitmap(CPDF_Document\*, CPDF_PageRenderCache\*, CPDF_TilingPattern\*, CPDF_Form\*, CFX_Matrix const&, int, int, CPDF_RenderOptions::Options const&) core/fpdfapi/render/cpdf_renderstatus.cpp:87:17  
    #7 0x55cc5bba412f in CPDF_RenderStatus::DrawTilingPattern(CPDF_TilingPattern\*, CPDF_PageObject\*, CFX_Matrix const&, bool) core/fpdfapi/render/cpdf_renderstatus.cpp:1307:47  
    #8 0x55cc5bba60aa in CPDF_RenderStatus::DrawPathWithPattern(CPDF_PathObject\*, CFX_Matrix const&, CPDF_Color const\*, bool) core/fpdfapi/render/cpdf_renderstatus.cpp:1396:5  
    #9 0x55cc5bb96676 in CPDF_RenderStatus::ProcessPathPattern(CPDF_PathObject\*, CFX_Matrix const&, int\*, bool\*) core/fpdfapi/render/cpdf_renderstatus.cpp:1418:7  
    #10 0x55cc5bb94b43 in CPDF_RenderStatus::ProcessPath(CPDF_PathObject\*, CFX_Matrix const&) core/fpdfapi/render/cpdf_renderstatus.cpp:427:3  
    #11 0x55cc5bb925ee in CPDF_RenderStatus::ProcessObjectNoClip(CPDF_PageObject\*, CFX_Matrix const&) core/fpdfapi/render/cpdf_renderstatus.cpp:329:14  
    #12 0x55cc5bb91e7b in CPDF_RenderStatus::ProcessTransparency(CPDF_PageObject\*, CFX_Matrix const&) core/fpdfapi/render/cpdf_renderstatus.cpp:710:17  
    #13 0x55cc5bb8fcdd in CPDF_RenderStatus::RenderSingleObject(CPDF_PageObject\*, CFX_Matrix const&) core/fpdfapi/render/cpdf_renderstatus.cpp:262:7  
    #14 0x55cc5bb8f8e1 in CPDF_RenderStatus::RenderObjectList(CPDF_PageObjectHolder const\*, CFX_Matrix const&) core/fpdfapi/render/cpdf_renderstatus.cpp:238:5  
    #15 0x55cc5bb96049 in CPDF_RenderStatus::ProcessForm(CPDF_FormObject const\*, CFX_Matrix const&) core/fpdfapi/render/cpdf_renderstatus.cpp:413:12  
    #16 0x55cc5bb927af in CPDF_RenderStatus::ProcessObjectNoClip(CPDF_PageObject\*, CFX_Matrix const&) core/fpdfapi/render/cpdf_renderstatus.cpp:338:14  
    #17 0x55cc5bb8fd07 in CPDF_RenderStatus::RenderSingleObject(CPDF_PageObject\*, CFX_Matrix const&) core/fpdfapi/render/cpdf_renderstatus.cpp:265:3  
    #18 0x55cc5bb8f8e1 in CPDF_RenderStatus::RenderObjectList(CPDF_PageObjectHolder const\*, CFX_Matrix const&) core/fpdfapi/render/cpdf_renderstatus.cpp:238:5  

```

**VERSION**  

pdfium version: commit 944a78501c664f2d89dc0c1ff23bcc901e2c8537. The link is <https://pdfium.googlesource.com/pdfium/+/944a78501c664f2d89dc0c1ff23bcc901e2c8537>.

Operating System: Ubuntu 18.04, 64 bits

Label: Cr-Internals-Plugins-PDF

**REPRODUCTION CASE**  

I built pdfium with this configuration:

```
# Build arguments go here.  
# See "gn args <out_dir> --list" for available build arguments.  
use_goma = false # Googlers only. Make sure goma is installed and running first.  
is_debug = false # Enable debugging features.  
  
pdf_use_skia = true # Set true to enable experimental skia backend.  
pdf_use_skia_paths = false  # Set true to enable experimental skia backend (paths only).  
  
pdf_enable_xfa = true  # Set false to remove XFA support (implies JS support).  
pdf_enable_v8 = true  # Set false to remove Javascript support.  
pdf_is_standalone = true  # Set for a non-embedded build.  
is_component_build = false # Disable component build (must be false)  
v8_static_library = true  
  
clang_use_chrome_plugins = false  # Currently must be false.  
use_sysroot = false  # Currently must be false on Linux, but entirely omitted on windows.  
  
is_asan = true  
#enable_nacl = true  
optimize_for_fuzzing = true  
symbol_level=1  
~  

```

The poc file is attached. And it is minimized by afl-tmin.  

I reproduced the bug with following command:

```
./pdfium_test ./poc_heap_buffer_overlow  

```

**CREDIT INFORMATION**  

Credit to Chengbin Pang & Jun Xu

## Attachments

- [poc_heap_buffer_overflow](attachments/poc_heap_buffer_overflow) (text/plain, 1.2 KB)

## Timeline

### cl...@chromium.org (2020-06-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5762885067800576.

### bd...@chromium.org (2020-06-26)

@khushalsagar could you take a look at this? it seems that you may have worked with something related to this recently.

I tried using ClusterFuzz to repro but couldn't: https://clusterfuzz.com/testcase-detail/5762885067800576 although I may have missed something here. 



[Monorail components: Internals>Skia]

### ad...@google.com (2020-06-26)

Suspect this could be a PDFIum error so cc tsepez@ too.

[Monorail components: Internals>Plugins>PDF]

### kh...@chromium.org (2020-06-26)

I don't think the error is related to skia here. The error is most likely in the pdfium component.

### th...@chromium.org (2020-06-26)

I'll take a look.

### th...@chromium.org (2020-06-26)

Ya, it's CFX_SkiaDeviceDriver::GetDIBits()'s fault for hardcoding a BPP of 32-bits and then calling Skia.

### th...@chromium.org (2020-06-26)

Hopefully a simple fix. https://pdfium-review.googlesource.com/70933

### cp...@stevens.edu (2020-06-26)

Hi, is this bug eligible for bug bounty?

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-26)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/75875b31461686095cd55d474b6c8765356d5147

commit 75875b31461686095cd55d474b6c8765356d5147
Author: Lei Zhang <thestig@chromium.org>
Date: Fri Jun 26 17:44:14 2020

Use the correct stride in CFX_SkiaDeviceDriver::GetDIBits().

It is incorrect to assume the bitmaps will have a BPP of 32.

Bug: chromium:1099446
Change-Id: Ibdab7fcfd9e0cd5a485396be3fcbb6f00d162426
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/70933
Commit-Queue: Lei Zhang <thestig@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/75875b31461686095cd55d474b6c8765356d5147/core/fxge/skia/fx_skia_device.cpp
[add] https://pdfium.googlesource.com/pdfium/+/75875b31461686095cd55d474b6c8765356d5147/testing/resources/pixel/bug_1099446_expected.pdf.0.png
[add] https://pdfium.googlesource.com/pdfium/+/75875b31461686095cd55d474b6c8765356d5147/testing/resources/pixel/bug_1099446.in


### th...@chromium.org (2020-06-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-26)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ce1dbb9e2e46f5dc0bf2d75faeb0852f8d73630d

commit ce1dbb9e2e46f5dc0bf2d75faeb0852f8d73630d
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Sat Jun 27 10:16:15 2020

Roll PDFium from 89b8527eceaf to 0c55cdde36c8 (6 revisions)

https://pdfium.googlesource.com/pdfium.git/+log/89b8527eceaf..0c55cdde36c8

2020-06-27 thestig@chromium.org Initialize CPWL_ListCtrl in the header.
2020-06-26 thestig@chromium.org Replace most _FX_PLATFORM_LINUX_ usage.
2020-06-26 thestig@chromium.org Add more tests for string assignment operators.
2020-06-26 thestig@chromium.org Initialize CFX_LZWDecompressor members in the header.
2020-06-26 thestig@chromium.org Add test expectations for standard_symbols.pdf.
2020-06-26 thestig@chromium.org Use the correct stride in CFX_SkiaDeviceDriver::GetDIBits().

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Bug: chromium:1099446
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: Ia7714af036202481f33f2691cbb969a304971bfd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2271420
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#783313}

[modify] https://crrev.com/ce1dbb9e2e46f5dc0bf2d75faeb0852f8d73630d/DEPS


### na...@google.com (2020-07-13)

[Empty comment from Monorail migration]

### ad...@google.com (2020-07-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-07-23)

Congratulations! The VRP panel has awarded $2000 for this report. Someone from our finance team will be in touch to arrange payment.

### ad...@google.com (2020-07-23)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pa...@gmail.com (2020-10-09)

Hello, I am Chengbin. Is this bug eligible for requesting a CVE id?

### ad...@chromium.org (2020-11-01)

Sorry we didn't spot your message until now.

This has been marked as Security_Impact-None in https://crbug.com/chromium/1099446#c5 because it is believed not to affect released versions of Chrome. For that reason, we've unable to allocate a CVE.

If you think that's incorrect and that there's a way to exploit this in stable Chrome, please add more details, we'd love to know! :) Thanks!

### is...@google.com (2020-11-01)

This issue was migrated from crbug.com/chromium/1099446?no_tracker_redirect=1

[Multiple monorail components: Internals>Plugins>PDF, Internals>Skia]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052678)*
