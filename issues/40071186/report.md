# Security: Pdfium heap-buffer-overflow in downsample_3_2()

| Field | Value |
|-------|-------|
| **Issue ID** | [40071186](https://issues.chromium.org/issues/40071186) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | d1...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2023-09-01 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**

Pdfium heap buffer overflow read in downsample\_3\_2 at third\_party\skia\src\core\SkMipmap.cpp:331:8.

In function CPDF\_DIB::CreateDecoder at core/fpdfapi/page/cpdf\_dib.cpp:517:5, the program allocates a bitmap buffer when creating JBIG2Decoder.

```
  if (decoder == "JBIG2Decode") {  
    m_pCachedBitmap = pdfium::MakeRetain<CFX_DIBitmap>();  
    if (!m_pCachedBitmap->Create(  
            m_Width, m_Height,  
            m_bImageMask ? FXDIB_Format::k1bppMask : FXDIB_Format::k1bppRgb)) {  
      m_pCachedBitmap.Reset();  
      return LoadState::kFail;  
    }  
    m_Status = LoadState::kSuccess;  
    return LoadState::kContinue;  
  }  

```

The size of the buffer is `23887876`, where `pitch=8192`. And `m_Format=FXDIB_Format::k1bppRgb`.

However, due to the existence of the `Mask` key, `m_Format` is changed to `FXDIB_Format::kArgb`, and `pitch=262132`.  

as shown in function CPDF\_DIB::ContinueInternal at core/fpdfapi/page/cpdf\_dib.cpp:258:5

```
  if (m_bColorKey) {  
    m_Format = FXDIB_Format::kArgb;  
    pitch = fxge::CalculatePitch32(GetBppFromFormat(m_Format), m_Width);  
    if (!pitch.has_value())  
      return false;  
    m_MaskBuf = DataVector<uint8_t>(pitch.value());  
  }  

```

Crash due to pitch=8192 when allocating memory and pitch=262132 when reading memory.  

as shown in function SkMipmap::Build at third\_party\skia\src\core\SkMipmap.cpp:653:16

```
        const SkPixmap& dstPM = levels[i].fPixmap;  
        if (computeContents) {  
            const void\* srcBasePtr = srcPM.addr();  
            void\* dstBasePtr = dstPM.writable_addr();  
  
            const size_t srcRB = srcPM.rowBytes();  
            for (int y = 0; y < height; y++) {  
                proc(dstBasePtr, srcBasePtr, srcRB, width);  
                srcBasePtr = (char\*)srcBasePtr + srcRB \* 2; // jump two rows  
                dstBasePtr = (char\*)dstBasePtr + dstPM.rowBytes();  
            }  
        }  
        srcPM = dstPM;  
        addr += height \* rowBytes;  

```

In this case /Height=2916 and /Width=65533  

Different height and width combinations will crash in different functions, such as  

/Height=2916 and /Width=65534 crash in function downsample\_2\_2  

/Height=2917 and /Width=65534 crash in function downsample\_2\_3  

/Height=2917 and /Width=65533 crash in function downsample\_3\_3

**VERSION**

repo: <https://pdfium.googlesource.com/pdfium>

commit: <https://pdfium.googlesource.com/pdfium/+/96be44fbcb9125fc32c67722be5935e5a58bbcf2>

**REPRODUCTION CASE**

gn args

```
use_goma = false  
is_debug = true  
  
pdf_use_skia = true  
  
pdf_enable_xfa = true  
pdf_enable_v8 = true  
pdf_is_standalone = true  
is_component_build = true  
  
symbol_level = 2  

```

I'm not sure whether the crash can only be triggered under skia, because the cause of the vulnerability does not seem to be caused by skia.

run in windbg

```
(230.434c): Access violation - code c0000005 (first chance)  
First chance exceptions are reported before any exception handling.  
This exception may be expected and handled.  
\*\*\* WARNING: Unable to verify checksum for D:\Code\chromium\repo\pdfium\out\skia\skia.dll  
skia!downsample_3_2<ColorTypeFilter_8888>+0x181:  
00007ffb`8886bef1 8b5004          mov     edx,dword ptr [rax+4] ds:000013d0`01ccd000=????????  
0:000> r  
rax=000013d001cccffc rbx=0000000000000000 rcx=c9c9be0784050000  
rdx=00ff00ff00ff00ff rsi=00000070dfcfc330 rdi=00000070dfcfe8d0  
rip=00007ffb8886bef1 rsp=00000070dfcfafb0 rbp=0000000000000000  
 r8=0000000000000003  r9=0000000000007ffe r10=0000c9b961c82ba5  
r11=00007ffb9c0e1b94 r12=0000000000000000 r13=0000000000000000  
r14=0000000000000000 r15=0000000000000000  
iopl=0         nv up ei pl nz na pe nc  
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010202  
skia!downsample_3_2<ColorTypeFilter_8888>+0x181:  
00007ffb`8886bef1 8b5004          mov     edx,dword ptr [rax+4] ds:000013d0`01ccd000=????????  
0:000> kp  
 # Child-SP          RetAddr               Call Site  
00 00000070`dfcfafb0 00007ffb`8886b0d1     skia!downsample_3_2<ColorTypeFilter_8888>(void \* dst = 0x000001e3`48c609b8, void \* src = 0x000013d0`01c83bc8, unsigned int64 srcRB = 0x3fff4, int count = 0n32766)+0x181 [D:\Code\chromium\repo\pdfium\third_party\skia\src\core\SkMipmap.cpp @ 331]   
01 00000070`dfcfb0a0 00007ffb`8887927e     skia!SkMipmap::Build(class SkPixmap \* src = 0x00000070`dfcfb2f8, <function> \* fact = 0x00007ffb`88253d10, bool computeContents = true)+0xfc1 [D:\Code\chromium\repo\pdfium\third_party\skia\src\core\SkMipmap.cpp @ 654]   
02 00000070`dfcfb2b0 00007ffb`887150aa     skia!SkMipmap::Build(class SkBitmap \* src = 0x00000070`dfcfb3b8, <function> \* fact = 0x00007ffb`88253d10)+0x7e [D:\Code\chromium\repo\pdfium\third_party\skia\src\core\SkMipmap.cpp @ 806]   
03 00000070`dfcfb330 00007ffb`8887d71d     skia!SkMipmapCache::AddAndRef(class SkImage_Base \* image = 0x000001e3`459c5f80, class SkResourceCache \* localCache = 0x00000000`00000000)+0xaa [D:\Code\chromium\repo\pdfium\third_party\skia\src\core\SkBitmapCache.cpp @ 304]   
04 00000070`dfcfb400 00007ffb`8887d23e     skia!try_load_mips(class SkImage_Base \* image = 0x000001e3`459c5f80)+0xbd [D:\Code\chromium\repo\pdfium\third_party\skia\src\core\SkMipmapAccessor.cpp @ 30]   
05 00000070`dfcfb480 00007ffb`8887ddd3     skia!SkMipmapAccessor::SkMipmapAccessor(class SkImage_Base \* image = 0x000001e3`459c5f80, class SkMatrix \* inv = 0x00000070`dfcfbb68, SkMipmapMode requestedMode = kLinear (0n2))+0x2ce [D:\Code\chromium\repo\pdfium\third_party\skia\src\core\SkMipmapAccessor.cpp @ 80]   
06 00000070`dfcfb5c0 00007ffb`8887dd4d     skia!SkArenaAlloc::make<SkMipmapAccessor,const SkImage_Base \*,const SkMatrix &,SkMipmapMode &>::<lambda_1>::operator()(void \* objStart = 0x00000070`dfcfc4d0)+0x33 [D:\Code\chromium\repo\pdfium\third_party\skia\src\base\SkArenaAlloc.h @ 153]   
07 00000070`dfcfb600 00007ffb`8887da24     skia!SkArenaAlloc::make<`lambda at ..\..\third_party\skia\src\base\SkArenaAlloc.h:152:27'>(class SkArenaAlloc::make<SkMipmapAccessor,const SkImage_Base \*,const SkMatrix &,SkMipmapMode &>::<lambda_1> \* ctor = 0x00000070`dfcfb6c8)+0x10d [D:\Code\chromium\repo\pdfium\third_party\skia\src\base\SkArenaAlloc.h @ 147]   
08 00000070`dfcfb680 00007ffb`8887d972     skia!SkArenaAlloc::make<SkMipmapAccessor,const SkImage_Base \*,const SkMatrix &,SkMipmapMode &>(class SkImage_Base \*\* args = 0x00000070`dfcfb750, class SkMatrix \* args = 0x00000070`dfcfbb68, SkMipmapMode \* args = 0x00000070`dfcfb75c)+0x54 [D:\Code\chromium\repo\pdfium\third_party\skia\src\base\SkArenaAlloc.h @ 152]   
09 00000070`dfcfb6f0 00007ffb`88a5cf36     skia!SkMipmapAccessor::Make(class SkArenaAlloc \* alloc = 0x00000070`dfcfd1c8, class SkImage \* image = 0x000001e3`459c5f80, class SkMatrix \* inv = 0x00000070`dfcfbb68, SkMipmapMode mipmap = kLinear (0n2))+0x72 [D:\Code\chromium\repo\pdfium\third_party\skia\src\core\SkMipmapAccessor.cpp @ 113]   
0a 00000070`dfcfb770 00007ffb`88a63006     skia!SkImageShader::appendStages(struct SkStageRec \* rec = 0x00000070`dfcfbd38, class SkShaders::MatrixRec \* mRec = 0x00000070`dfcfbbf4)+0x276 [D:\Code\chromium\repo\pdfium\third_party\skia\src\shaders\SkImageShader.cpp @ 482]   
0b 00000070`dfcfbba0 00007ffb`8899124c     skia!SkShaderBase::appendRootStages(struct SkStageRec \* rec = 0x00000070`dfcfbd38, class SkMatrix \* ctm = 0x00000070`dfcfd1f0)+0x56 [D:\Code\chromium\repo\pdfium\third_party\skia\src\shaders\SkShaderBase.cpp @ 139]   
0c 00000070`dfcfbc80 00007ffb`887415ff     skia!SkCreateRasterPipelineBlitter(class SkPixmap \* dst = 0x00000070`dfcfe2b8, class SkPaint \* paint = 0x00000070`dfcfd318, class SkMatrix \* ctm = 0x00000070`dfcfd1f0, class SkArenaAlloc \* alloc = 0x00000070`dfcfd1c8, class sk_sp<SkShader> \* clipShader = 0x00000070`dfcfbf68, class SkSurfaceProps \* props = 0x00000070`dfcfc33c)+0x2fc [D:\Code\chromium\repo\pdfium\third_party\skia\src\core\SkRasterPipelineBlitter.cpp @ 129]   
0d 00000070`dfcfbef0 00007ffb`88741181     skia!SkBlitter::Choose::<lambda_0>::operator()(void)+0x9f [D:\Code\chromium\repo\pdfium\third_party\skia\src\core\SkBlitter.cpp @ 738]   
0e 00000070`dfcfbf80 00007ffb`887995a5     skia!SkBlitter::Choose(class SkPixmap \* device = 0x00000070`dfcfe2b8, class SkMatrix \* ctm = 0x00000070`dfcfd1f0, class SkPaint \* origPaint = 0x00000070`dfcfd318, class SkArenaAlloc \* alloc = 0x00000070`dfcfd1c8, bool drawCoverage = false, class sk_sp<SkShader> \* clipShader = 0x00000070`dfcfc330, class SkSurfaceProps \* props = 0x00000070`dfcfc33c)+0x7e1 [D:\Code\chromium\repo\pdfium\third_party\skia\src\core\SkBlitter.cpp @ 767]   
0f 00000070`dfcfc280 00007ffb`88798007     skia!SkAutoBlitterChoose::choose(class SkDrawBase \* draw = 0x00000070`dfcfe2b0, class SkMatrix \* ctm = 0x00000070`dfcfd1f0, class SkPaint \* paint = 0x00000070`dfcfd318, bool drawCoverage = false)+0x195 [D:\Code\chromium\repo\pdfium\third_party\skia\src\core\SkAutoBlitterChoose.h @ 38]   
10 00000070`dfcfc360 00007ffb`8879a908     skia!SkAutoBlitterChoose::SkAutoBlitterChoose(class SkDrawBase \* draw = 0x00000070`dfcfe2b0, class SkMatrix \* ctm = 0x00000070`dfcfd1f0, class SkPaint \* paint = 0x00000070`dfcfd318, bool drawCoverage = false)+0x67 [D:\Code\chromium\repo\pdfium\third_party\skia\src\core\SkAutoBlitterChoose.h @ 29]   
11 00000070`dfcfc3c0 00007ffb`88798771     skia!SkDrawBase::drawRect(struct SkRect \* prePaintRect = 0x00000070`dfcfd308, class SkPaint \* paint = 0x00000070`dfcfd318, class SkMatrix \* paintMatrix = 0x00000070`dfcfe578, struct SkRect \* postPaintRect = 0x00000070`dfcfe8d0)+0x4d8 [D:\Code\chromium\repo\pdfium\third_party\skia\src\core\SkDrawBase.cpp @ 217]   
12 00000070`dfcfd230 00007ffb`88717e12     skia!SkDraw::drawBitmap(class SkBitmap \* bitmap = 0x00000070`dfcfe4d0, class SkMatrix \* prematrix = 0x00000070`dfcfe578, struct SkRect \* dstBounds = 0x00000070`dfcfe8d0, struct SkSamplingOptions \* sampling = 0x00000070`dfcfe698, class SkPaint \* origPaint = 0x00000070`dfcfe630)+0x691 [D:\Code\chromium\repo\pdfium\third_party\skia\src\core\SkDraw.cpp @ 370]   
13 00000070`dfcfe1c0 00007ffb`887184bd     skia!SkBitmapDevice::drawBitmap(class SkBitmap \* bitmap = 0x00000070`dfcfe4d0, class SkMatrix \* matrix = 0x00000070`dfcfe578, struct SkRect \* dstOrNull = 0x00000070`dfcfe8d0, struct SkSamplingOptions \* sampling = 0x00000070`dfcfe698, class SkPaint \* paint = 0x00000070`dfcfe630)+0x222 [D:\Code\chromium\repo\pdfium\third_party\skia\src\core\SkBitmapDevice.cpp @ 407]   
14 00000070`dfcfe390 00007ffb`8876abcd     skia!SkBitmapDevice::drawImageRect(class SkImage \* image = 0x000001e3`459c1f80, struct SkRect \* src = 0x00000070`dfcfe8c0, struct SkRect \* dst = 0x00000070`dfcfe8d0, struct SkSamplingOptions \* sampling = 0x00000070`dfcfe698, class SkPaint \* paint = 0x00000070`dfcfe630, SkCanvas::SrcRectConstraint constraint = kFast_SrcRectConstraint (0n1))+0x65d [D:\Code\chromium\repo\pdfium\third_party\skia\src\core\SkBitmapDevice.cpp @ 512]   
15 00000070`dfcfe5b0 00007ffb`88768013     skia!SkCanvas::onDrawImageRect2(class SkImage \* image = 0x000001e3`459c1f80, struct SkRect \* src = 0x00000070`dfcfe8c0, struct SkRect \* dst = 0x00000070`dfcfe8d0, struct SkSamplingOptions \* sampling = 0x00000070`dfcfe8f8, class SkPaint \* paint = 0x00000070`dfcfe910, SkCanvas::SrcRectConstraint constraint = kFast_SrcRectConstraint (0n1))+0x25d [D:\Code\chromium\repo\pdfium\third_party\skia\src\core\SkCanvas.cpp @ 2169]   
16 00000070`dfcfe720 00007ff6`faeec769     skia!SkCanvas::drawImageRect(class SkImage \* image = 0x000001e3`459c1f80, struct SkRect \* src = 0x00000070`dfcfe8c0, struct SkRect \* dst = 0x00000070`dfcfe8d0, struct SkSamplingOptions \* sampling = 0x00000070`dfcfe8f8, class SkPaint \* paint = 0x00000070`dfcfe910, SkCanvas::SrcRectConstraint constraint = kFast_SrcRectConstraint (0n1))+0xc3 [D:\Code\chromium\repo\pdfium\third_party\skia\src\core\SkCanvas.cpp @ 2200]   
17 00000070`dfcfe790 00007ff6`faeeb08e     pdfium_test!SkCanvas::drawImageRect(class sk_sp<SkImage> \* image = 0x00000070`dfcfe970, struct SkRect \* src = 0x00000070`dfcfe8c0, struct SkRect \* dst = 0x00000070`dfcfe8d0, struct SkSamplingOptions \* sampling = 0x00000070`dfcfe8f8, class SkPaint \* paint = 0x00000070`dfcfe910, SkCanvas::SrcRectConstraint constraint = kFast_SrcRectConstraint (0n1))+0xb9 [D:\Code\chromium\repo\pdfium\third_party\skia\include\core\SkCanvas.h @ 1487]   
18 00000070`dfcfe820 00007ff6`faeeb506     pdfium_test!CFX_SkiaDeviceDriver::StartDIBitsSkia(class fxcrt::RetainPtr<CFX_DIBBase> \* pSource = 0x000001e3`45999f88, struct FX_RECT \* src_rect = 0x00000070`dfcfea38, int bitmap_alpha = 0n255, unsigned int color = 0, class CFX_Matrix \* matrix = 0x000001e3`45999fa8, struct FXDIB_ResampleOptions \* options = 0x000001e3`45999fe8, BlendMode blend_type = kNormal (0n0))+0x46e [D:\Code\chromium\repo\pdfium\core\fxge\skia\fx_skia_device.cpp @ 1614]   
19 00000070`dfcfe9b0 00007ff6`fae9e486     pdfium_test!CFX_SkiaDeviceDriver::StartDIBits(class fxcrt::RetainPtr<CFX_DIBBase> \* pSource = 0x000001e3`45999f88, int bitmap_alpha = 0n255, unsigned int color = 0, class CFX_Matrix \* matrix = 0x000001e3`45999fa8, struct FXDIB_ResampleOptions \* options = 0x000001e3`45999fe8, class std::__Cr::unique_ptr<CFX_ImageRenderer,std::__Cr::default_delete<CFX_ImageRenderer> > \* handle = 0x000001e3`45999fd0 empty, BlendMode blend_type = kNormal (0n0))+0x116 [D:\Code\chromium\repo\pdfium\core\fxge\skia\fx_skia_device.cpp @ 1436]   
1a 00000070`dfcfea60 00007ff6`fb287d4b     pdfium_test!CFX_RenderDevice::StartDIBitsWithBlend(class fxcrt::RetainPtr<CFX_DIBBase> \* pBitmap = 0x000001e3`45999f88, int bitmap_alpha = 0n255, unsigned int argb = 0, class CFX_Matrix \* matrix = 0x000001e3`45999fa8, struct FXDIB_ResampleOptions \* options = 0x000001e3`45999fe8, class std::__Cr::unique_ptr<CFX_ImageRenderer,std::__Cr::default_delete<CFX_ImageRenderer> > \* handle = 0x000001e3`45999fd0 empty, BlendMode blend_mode = kNormal (0n0))+0x96 [D:\Code\chromium\repo\pdfium\core\fxge\cfx_renderdevice.cpp @ 986]   
1b 00000070`dfcfead0 00007ff6`fb28607b     pdfium_test!CPDF_ImageRenderer::StartDIBBase(void)+0x1ab [D:\Code\chromium\repo\pdfium\core\fpdfapi\render\cpdf_imagerenderer.cpp @ 398]   
1c 00000070`dfcfec20 00007ff6`fb2895df     pdfium_test!CPDF_ImageRenderer::StartRenderDIBBase(void)+0x80b [D:\Code\chromium\repo\pdfium\core\fpdfapi\render\cpdf_imagerenderer.cpp @ 151]   
1d 00000070`dfcfedb0 00007ff6`fb289108     pdfium_test!CPDF_ImageRenderer::ContinueDefault(class PauseIndicatorIface \* pPause = 0x00000070`dfcff0a0)+0x4f [D:\Code\chromium\repo\pdfium\core\fpdfapi\render\cpdf_imagerenderer.cpp @ 545]   
1e 00000070`dfcfee00 00007ff6`fb2991ee     pdfium_test!CPDF_ImageRenderer::Continue(class PauseIndicatorIface \* pPause = 0x00000070`dfcff0a0)+0x58 [D:\Code\chromium\repo\pdfium\core\fpdfapi\render\cpdf_imagerenderer.cpp @ 533]   
1f 00000070`dfcfee50 00007ff6`fb28b1e5     pdfium_test!CPDF_RenderStatus::ContinueSingleObject(class CPDF_PageObject \* pObj = 0x000001e3`4593af50, class CFX_Matrix \* mtObj2Device = 0x000001e3`4598bfd8, class PauseIndicatorIface \* pPause = 0x00000070`dfcff0a0)+0x6e [D:\Code\chromium\repo\pdfium\core\fpdfapi\render\cpdf_renderstatus.cpp @ 238]   
20 00000070`dfcfeee0 00007ff6`facd573a     pdfium_test!CPDF_ProgressiveRenderer::Continue(class PauseIndicatorIface \* pPause = 0x00000070`dfcff0a0)+0x675 [D:\Code\chromium\repo\pdfium\core\fpdfapi\render\cpdf_progressiverenderer.cpp @ 88]   
21 00000070`dfcff040 00007ff6`fac21a20     pdfium_test!FPDF_RenderPage_Continue(struct fpdf_page_t__ \* page = 0x000001e3`45807fd0, struct _IFSDK_PAUSE \* pause = 0x000001e3`45953fd0)+0x10a [D:\Code\chromium\repo\pdfium\fpdfsdk\fpdf_progressive.cpp @ 118]   
22 00000070`dfcff0c0 00007ff6`fac194e0     pdfium_test!`anonymous namespace'::ProgressiveBitmapPageRenderer::Continue(void)+0x40 [D:\Code\chromium\repo\pdfium\samples\pdfium_test.cc @ 1085]   
23 00000070`dfcff100 00007ff6`fac14d08     pdfium_test!`anonymous namespace'::PdfProcessor::ProcessPage(int page_index = 0n0)+0xb80 [D:\Code\chromium\repo\pdfium\samples\pdfium_test.cc @ 1511]   
24 00000070`dfcff500 00007ff6`fac118a0     pdfium_test!`anonymous namespace'::Processor::ProcessPdf(class std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > \* name = 0x000001e2`c38d4fe0 "D:\Vuln\pdfium_2023_09_01\poc.pdf", char \* buf = 0x000001e3`45698e10 "%PDF-1.3..1 0 obj.<<./Kids [ 3 0 R ]./Type /Pages./Count 1.>>.endobj..3 0 obj.<<./Parent 1 0 R./Contents 14 0 R./Resources <<./XObject <<./I1 15 0 R.>>.>>.>>.endobj..13 0 obj.<<./Type /Catalog./Pages 1 0 R.>>.endobj..14 0 obj.<<./Length 10.>>.stream..q./I1 Do.Q..endstream.endobj..15 0 obj.<<./Filter /JBIG2Decode./Type /XObject./Subtype /Image./ColorSpace /DeviceGray./Length 10./Height 2916./Width 65533./Mask [ 255 255 ]..>>.stream..3 Tr..endstream.endobj...trailer.<<./Root 13 0 R.>>???", unsigned int64 len = 0x1e7, class std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > \* events = 0x00000070`dfcff910 "")+0xb28 [D:\Code\chromium\repo\pdfium\samples\pdfium_test.cc @ 1681]   
25 00000070`dfcff830 00007ff6`fb8a4679     pdfium_test!main(int argc = 0n2, char \*\* argv = 0x000001e2`bf834f80)+0xa90 [D:\Code\chromium\repo\pdfium\samples\pdfium_test.cc @ 2000]   
26 00000070`dfcffbf0 00007ff6`fb8a47ae     pdfium_test!invoke_main(void)+0x39 [D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 79]   
27 00000070`dfcffc40 00007ff6`fb8a482e     pdfium_test!__scrt_common_main_seh(void)+0x12e [D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 288]   
28 00000070`dfcffcb0 00007ff6`fb8a484e     pdfium_test!__scrt_common_main(void)+0xe [D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 331]   
29 00000070`dfcffce0 00007ffc`1ec47614     pdfium_test!mainCRTStartup(void \* __formal = 0x00000070`dfb2c000)+0xe [D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_main.cpp @ 17]   
2a 00000070`dfcffd10 00007ffc`1f3426b1     KERNEL32!BaseThreadInitThunk+0x14  
2b 00000070`dfcffd40 00000000`00000000     ntdll!RtlUserThreadStart+0x21  

```

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 487 B)

## Timeline

### [Deleted User] (2023-09-01)

[Empty comment from Monorail migration]

### ts...@chromium.org (2023-09-05)

Lei, do we need to reallocate both the image and mask buffers here? Also why is the mask only pitch wide instead of pitch * height?

[Monorail components: Internals>Plugins>PDF]

### ke...@chromium.org (2023-09-05)

I've reproduced the buffer overflow, but the problem does seem to be in Skia code.

thestig@ or tsepez@, is this reachable in production Chrome?

### th...@chromium.org (2023-09-05)

In Chromium, this is gated on chrome://flags/#pdf-use-skia-renderer. The associated Finch experiment recently got turned off, but the goal is to launch to 100% Stable.

### th...@chromium.org (2023-09-07)

FWIW, in PDFium, this bisects to https://pdfium-review.googlesource.com/108651, but I can take the issue.

### th...@chromium.org (2023-09-07)

Looks like the situation involves 2 bitmap objects that share the same buffer. It was originally allocated with format FXDIB_Format::k1bppRgb, but the second bitmap is treating the buffer as FXDIB_Format::kArgb.

### th...@chromium.org (2023-09-07)

I realized some of this is in the initial analysis, but I oftentimes like to trace the steps for myself.

### th...@chromium.org (2023-09-07)

We are aware of the fact that CPDF_DIB::GetBuffer() is problematic and tried to stop using it in https://pdfium-review.googlesource.com/108850, but that CL got reverted. I've been trying to re-do that in https://pdfium-review.googlesource.com/111434, and getting rid of CPDF_DIB::GetBuffer() should fix this. However, I'm trying to see if I can alternatively fix this by making CPDF_DIB's internal state more consistent.

### th...@chromium.org (2023-09-07)

Fix with test case here: https://pdfium-review.googlesource.com/111710 - the image has to be bigger than kHugeImageSize to trigger this issue.

### gi...@appspot.gserviceaccount.com (2023-09-16)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/b22fc9a07d0c8f2cec0425090d3891f7423ad22b

commit b22fc9a07d0c8f2cec0425090d3891f7423ad22b
Author: Lei Zhang <thestig@chromium.org>
Date: Sat Sep 16 01:24:58 2023

Don't implement CPDF_DIB::GetBuffer() (try 2)

The first try [1] to just return an empty span in CPDF_DIB::GetBuffer()
did not work. This CL goes further and deletes CFX_DIBBase::GetBuffer()
altogether. Instead, only implement a non-virtual
CFX_DIBBitmap::GetBuffer(). To make this work, get rid of all
CFX_DIBBase::GetBuffer() callers:

- Switch to calling CFX_DIBBitmap::GetBuffer() when it easy to do so.
- Make CFX_DIBBase::RealizeIfNeeded() virtual, and change the default
  implementation to just call Realize().
- Make RealizeIfNeeded() available for Skia-builds and use it in
  CreateSkiaImageFromDib().
- Change CreateSkiaImageFromTransformedDib() to only use scanlines.

Fix other issues to make sure everything works:

- Avoid calling RealizeIfNeeded() on `CPDF_DIB::m_pCachedBitmap`, as
  that gives the wrong answer, just like CPDF_DIB::GetBuffer().
- Make sure CreateSkiaImageFromDib() does not fail and leak memory.
- Give up on avoiding the CachedImage::SkipToScanline() call.
- Add a test case for a related bug.

[1] https://pdfium-review.googlesource.com/108850

Bug: chromium:1478366,pdfium:2050,pdfium:2051
Change-Id: Ia20d4d257d441dd971ee0a912733f48f29dafad1
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/111434
Reviewed-by: Nigi <nigi@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/b22fc9a07d0c8f2cec0425090d3891f7423ad22b/core/fxge/skia/cfx_dibbase_skia.cpp
[add] https://pdfium.googlesource.com/pdfium/+/b22fc9a07d0c8f2cec0425090d3891f7423ad22b/testing/resources/pixel/bug_1478366_expected_skia.pdf.0.png
[modify] https://pdfium.googlesource.com/pdfium/+/b22fc9a07d0c8f2cec0425090d3891f7423ad22b/core/fpdfapi/page/cpdf_pageimagecache.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/b22fc9a07d0c8f2cec0425090d3891f7423ad22b/core/fxge/win32/cgdi_plus_ext.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/b22fc9a07d0c8f2cec0425090d3891f7423ad22b/core/fxge/dib/cfx_dibbase.h
[modify] https://pdfium.googlesource.com/pdfium/+/b22fc9a07d0c8f2cec0425090d3891f7423ad22b/core/fpdfapi/page/cpdf_dib.h
[modify] https://pdfium.googlesource.com/pdfium/+/b22fc9a07d0c8f2cec0425090d3891f7423ad22b/core/fxge/dib/cfx_dibbase.cpp
[add] https://pdfium.googlesource.com/pdfium/+/b22fc9a07d0c8f2cec0425090d3891f7423ad22b/testing/resources/pixel/bug_1478366_expected.pdf.0.png
[modify] https://pdfium.googlesource.com/pdfium/+/b22fc9a07d0c8f2cec0425090d3891f7423ad22b/core/fxge/dib/cfx_dibitmap.h
[add] https://pdfium.googlesource.com/pdfium/+/b22fc9a07d0c8f2cec0425090d3891f7423ad22b/testing/resources/pixel/bug_1478366.in
[modify] https://pdfium.googlesource.com/pdfium/+/b22fc9a07d0c8f2cec0425090d3891f7423ad22b/core/fpdfapi/page/cpdf_dib.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/b22fc9a07d0c8f2cec0425090d3891f7423ad22b/core/fxge/dib/cfx_dibitmap.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/b22fc9a07d0c8f2cec0425090d3891f7423ad22b/core/fxge/win32/cgdi_device_driver.cpp


### gi...@appspot.gserviceaccount.com (2023-09-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/05a984c5c0fb2d84d98f9be46d39fb84ce862e21

commit 05a984c5c0fb2d84d98f9be46d39fb84ce862e21
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Sat Sep 16 04:03:40 2023

Roll PDFium from 1e1e17305dbb to b22fc9a07d0c (8 revisions)

https://pdfium.googlesource.com/pdfium.git/+log/1e1e17305dbb..b22fc9a07d0c

2023-09-16 thestig@chromium.org Don't implement CPDF_DIB::GetBuffer() (try 2)
2023-09-16 thestig@chromium.org Use fxge::CalculatePitch8() in more places
2023-09-16 thestig@chromium.org Make graphics resource names share-on-write
2023-09-16 thestig@chromium.org Avoid another PartitionAlloc allocator shim incompatibility
2023-09-15 nigi@chromium.org Add an embedder test for crbug.com/pdfium/1893
2023-09-15 thestig@chromium.org Update third_party/base/sys_byteorder.h
2023-09-15 thestig@chromium.org Remove some NOTREACHED() usage in core/fpdfapi/parser directory
2023-09-15 thestig@chromium.org Rename CPDF_ImageLoader::HandleFailure() to Finish()

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC dhoss@chromium.org,pdfium-deps-rolls@chromium.org,thestig@chromium.org on the revert to ensure that a human
is aware of the problem.

To file a bug in PDFium: https://bugs.chromium.org/p/pdfium/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1477279,chromium:1478366
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: Ie803bf15af0655542debeffcbd1f67e6e4c873a6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4869346
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1197490}

[modify] https://crrev.com/05a984c5c0fb2d84d98f9be46d39fb84ce862e21/third_party/pdfium
[modify] https://crrev.com/05a984c5c0fb2d84d98f9be46d39fb84ce862e21/DEPS


### th...@chromium.org (2023-09-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-16)

[Empty comment from Monorail migration]

### am...@google.com (2023-09-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-21)

[Comment Deleted]

### am...@chromium.org (2023-09-21)

Congratulations! The Chrome VRP Panel has decided to award you $2,000 for this report of an OOB read / information leak! 
A member of our finance team will be in touch with you soon to arrange payment. In the meantime, please let us know to what name / identifier we should use in acknowledging you for findings and future reports. 
Thank you for your efforts and reporting this issue to us!

### am...@chromium.org (2023-09-21)

Since this is an OOB read in a sandboxed process, the appropriate severity is Medium. Updating accordingly. 

OP / reporter, if you can demonstrate that a write is achievable, we would be happy to reassess this for a potentially higher reward. 

### am...@google.com (2023-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-12-23)

This issue was migrated from crbug.com/chromium/1478366?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40071186)*
