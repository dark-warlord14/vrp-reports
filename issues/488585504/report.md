# Heap buffer overflow in CFX_Face::RenderGlyph when expanding MONO bitmap glyphs under LCD anti-aliasing

| Field | Value |
|-------|-------|
| **Issue ID** | [488585504](https://issues.chromium.org/issues/488585504) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | PDFium |
| **Platforms** | Linux, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | ts...@google.com |
| **Created** | 2026-03-01 |
| **Bounty** | $11,000.00 |

## Description

# Heap buffer overflow in CFX\_Face::RenderGlyph when expanding MONO bitmap glyphs under LCD anti-aliasing

## Summary

A heap buffer overflow exists in PDFium's glyph rendering code. When a PDF embeds a bitmap-only TrueType font (containing EBDT/EBLC tables but no glyf outlines), FreeType loads glyphs as monochrome bitmaps regardless of the `FT_LOAD_NO_BITMAP` flag. The subsequent call to `FT_Render_Glyph` silently succeeds without converting the bitmap pixel format. `CFX_Face::RenderGlyph` then expands each monochrome pixel into 3 bytes for LCD anti-aliasing, but the destination buffer was allocated assuming 1 byte per pixel. This causes a write that overflows the heap buffer by approximately `2 * bitmap_width - 4` bytes. The bug affects all platforms where Chrome uses the AGG renderer for PDF text (Linux, Windows, Android), which is the default configuration. No user interaction beyond opening a PDF is required.

## Bisect

Introducing Commit: `5110c4743751145c4ae1934cd1d83bc6c55bb43f`

- Date: 2014-05-17
- Author: John Abd-El-Malek
- Review: Initial PDFium commit

The vulnerable MONO-to-LCD expansion logic has been present since PDFium's initial open-source commit. The code was originally in `CFX_FaceCache::RenderGlyph` (later renamed `CFX_GlyphCache`) and was moved into `CFX_Face::RenderGlyph` in commit `65dc04ddae82f565c0d77dcdefca592b15a2bce4` (2023-12-16, CL <https://pdfium-review.googlesource.com/c/pdfium/+/114790>) by Lei Zhang.

## Root Cause

The vulnerability is in `CFX_Face::RenderGlyph`, which handles the conversion of FreeType glyph bitmaps into PDFium's internal `CFX_GlyphBitmap` format. When the requested anti-aliasing mode is LCD (`FontAntiAliasingMode::kLcd`) but FreeType returns a monochrome bitmap (`FT_PIXEL_MODE_MONO`), the code attempts to expand each source pixel into 3 destination bytes without adjusting the destination buffer width.

The buffer allocation uses the raw bitmap width in pixels, creating a `k8bppMask` format bitmap (1 byte per pixel):

```
// cfx_face.cpp:586-592
int dib_width = bitmap.width;
auto pGlyphBitmap =
    std::make_unique<CFX_GlyphBitmap>(glyph->bitmap_left, glyph->bitmap_top);
const FXDIB_Format format = anti_alias == FontAntiAliasingMode::kMono
                                ? FXDIB_Format::k1bppMask
                                : FXDIB_Format::k8bppMask;
if (!pGlyphBitmap->GetBitmap()->Create(dib_width, bitmap.rows, format)) {

```

For `k8bppMask`, the allocated buffer is `align4(bitmap.width) * bitmap.rows + 4` bytes. However, the MONO expansion loop writes `bitmap.width * 3` bytes per row:

```
// cfx_face.cpp:599-611
if (anti_alias != FontAntiAliasingMode::kMono &&
    bitmap.pixel_mode == FT_PIXEL_MODE_MONO) {
  unsigned int bytes = anti_alias == FontAntiAliasingMode::kLcd ? 3 : 1;
  for (unsigned int i = 0; i < bitmap.rows; i++) {
    for (unsigned int n = 0; n < bitmap.width; n++) {
      uint8_t data =
          (pSrcBuf[i * bitmap.pitch + n / 8] & (0x80 >> (n % 8))) ? 255 : 0;
      for (unsigned int b = 0; b < bytes; b++) {
        pDestBuf[i * dest_pitch + n * bytes + b] = data;  // overflow
      }
    }
  }
}

```

When `bytes == 3`, the write index `n * 3 + b` reaches `bitmap.width * 3 - 1` at the end of each row, but `dest_pitch` is only `align4(bitmap.width)`. Starting from the second row, every row's writes begin at an offset that was calculated using the narrow `dest_pitch`, causing the final rows to write well past the end of the buffer. For a 32-pixel-wide glyph, the total overflow is approximately 60 bytes past the 1028-byte allocation.

Three conditions converge to make this reachable from a crafted PDF:

First, FreeType's `FT_LOAD_NO_BITMAP` flag, which PDFium passes when loading glyphs, is explicitly documented as having no effect on bitmap-only fonts: "Ignore bitmap strikes when loading. Bitmap-only fonts ignore this flag." A bitmap-only TrueType font (one with EBDT/EBLC tables but no glyf outlines, using maxp version 0.5) causes `FT_Load_Glyph` to return a glyph in `FT_GLYPH_FORMAT_BITMAP` format with `pixel_mode == FT_PIXEL_MODE_MONO`.

Second, `FT_Render_Glyph` silently succeeds when it cannot convert the bitmap format. In `FT_Render_Glyph_Internal`, after exhausting all renderers and getting `FT_Err_Cannot_Render_Glyph`, the code explicitly clears the error for bitmap glyphs:

```
// ftobjs.c:4855-4858
/* it is not an error if we cannot render a bitmap glyph */
if ( FT_ERR_EQ( error, Cannot_Render_Glyph ) &&
     slot->format == FT_GLYPH_FORMAT_BITMAP  )
  error = FT_Err_Ok;

```

This means `FT_Render_Glyph` returns success, but the glyph's `pixel_mode` remains `FT_PIXEL_MODE_MONO`, which PDFium does not expect in LCD mode.

Third, Chrome's PDF viewer defaults to the AGG software renderer because the `kPdfUseSkiaRenderer` feature flag is `FEATURE_DISABLED_BY_DEFAULT` in the source code:

```
// pdf/pdf_features.cc:52
BASE_FEATURE(kPdfUseSkiaRenderer, base::FEATURE_DISABLED_BY_DEFAULT);

```

Although `testing/variations/fieldtrial_testing_config.json` enables `PdfUseSkiaRenderer` on all desktop platforms in Chromium development builds:

```
// testing/variations/fieldtrial_testing_config.json:19739-19759
"PdfUseSkiaRenderer": [
    {
        "platforms": ["chromeos", "fuchsia", "linux", "mac", "windows"],
        "experiments": [{ "name": "Enabled", "enable_features": ["PdfUseSkiaRenderer"] }]
    }
],

```

this config is only applied automatically in non-Chrome-branded builds (i.e. Chromium development builds). Chrome-branded release builds require an explicit switch to apply it:

```
// variations/service/variations_field_trial_creator.cc:135-148
bool ShouldUseFieldTrialTestingConfig(const base::CommandLine* command_line) {
  bool is_enable_switch_set = ...;
#if BUILDFLAG(GOOGLE_CHROME_BRANDING)
  return is_enable_switch_set;  // testing config NOT applied by default
#else
  return is_enable_switch_set ||
         (!command_line->HasSwitch(switches::kDisableFieldTrialTestingConfig) &&
          !command_line->HasSwitch(switches::kVariationsServerURL));
#endif
}

```

Production Chrome installs that have not received a Finch-pushed Skia enablement therefore use the AGG renderer. The AGG renderer's `DrawDeviceText` unconditionally returns false on non-Apple platforms, forcing all text rendering through the software bitmap path (`LoadGlyphBitmap` to `RenderGlyph`) where the vulnerability resides. LCD anti-aliasing is selected whenever the display device has 16 or more bits per pixel, which is the common case.

## Reproduce

This bug was tested on Chromium commit `89d6357f16ea411b6aa0fc7891b7d9dd18369823` (2026-02-19), which includes PDFium at revision `beea56eb350ae1a3d4d0a8c487e179d31e285848`. To reproduce, check out that commit with `git checkout 89d6357f16ea411b6aa0fc7891b7d9dd18369823` and run `gclient sync`.

Configure an ASAN build by writing the following to `out/asan-release/args.gn`:

```
is_asan = true
is_debug = false
dcheck_always_on = false
target_cpu = "x64"
is_component_build = true

```

Then build Chrome with `autoninja -C out/asan-release chrome`.

To trigger the crash, place the attached `poc.pdf` in the working directory and launch Chrome. The `--disable-field-trial-config` flag is required because Chromium development builds automatically apply `testing/variations/fieldtrial_testing_config.json`, which enables `PdfUseSkiaRenderer` on all desktop platforms; this overrides the code default (`FEATURE_DISABLED_BY_DEFAULT`) and routes text rendering through Skia, bypassing the vulnerable AGG code path. Disabling the field trial config restores the code default, which uses the AGG renderer, matching the behavior of production Chrome releases where Finch has not enabled Skia for PDF rendering.

```
ASAN_OPTIONS=detect_odr_violation=0 xvfb-run -a out/asan-release/chrome \
  --no-sandbox --disable-field-trial-config \
  --user-data-dir=/tmp/poc-test poc.pdf

```

ASAN reports a heap-buffer-overflow WRITE at `CFX_Face::RenderGlyph` in `cfx_face.cpp`. The full ASAN log is in `asan.log`.

```
=================================================================
==2151182==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7d8f7845f284 at pc 0x7fff881fd09c bp 0x7fffffffb2b0 sp 0x7fffffffb2a8
WRITE of size 1 at 0x7d8f7845f284 thread T0 (chrome)
    #0 0x7fff881fd09b in CFX_Face::RenderGlyph(CFX_Font const*, unsigned int, bool, CFX_Matrix const&, int, FontAntiAliasingMode) third_party/pdfium/core/fxge/cfx_face.cpp:608:54
    #1 0x7fff88213c1e in CFX_GlyphCache::LookUpGlyphBitmap(CFX_Font const*, CFX_Matrix const&, fxcrt::ByteString const&, unsigned int, bool, int, FontAntiAliasingMode) third_party/pdfium/core/fxge/cfx_glyphcache.cpp:128:17
    #2 0x7fff8821366c in CFX_GlyphCache::LoadGlyphBitmap(CFX_Font const*, unsigned int, bool, CFX_Matrix const&, int, FontAntiAliasingMode, CFX_TextRenderOptions*) third_party/pdfium/core/fxge/cfx_glyphcache.cpp:181:12
    #3 0x7fff882085a3 in CFX_Font::LoadGlyphBitmap(unsigned int, bool, CFX_Matrix const&, int, FontAntiAliasingMode, CFX_TextRenderOptions*) const third_party/pdfium/core/fxge/cfx_font.cpp:400:35
    #4 0x7fff882225ac in CFX_RenderDevice::DrawNormalText(pdfium::span<TextCharPos const, 18446744073709551615ul, TextCharPos const*>, CFX_Font*, float, CFX_Matrix const&, unsigned int, CFX_TextRenderOptions const&) third_party/pdfium/core/fxge/cfx_renderdevice.cpp:1183:26
    #5 0x7fff8882d555 in CPDF_TextRenderer::DrawNormalText(CFX_RenderDevice*, pdfium::span<unsigned int const, 18446744073709551615ul, unsigned int const*>, pdfium::span<float const, 18446744073709551615ul, float const*>, CPDF_Font*, float, CFX_Matrix const&, unsigned int, CPDF_RenderOptions const&) third_party/pdfium/core/fpdfapi/render/cpdf_textrenderer.cpp:176:17
    #6 0x7fff8881b097 in CPDF_RenderStatus::ProcessText(CPDF_TextObject*, CFX_Matrix const&, CFX_Path*) third_party/pdfium/core/fpdfapi/render/cpdf_renderstatus.cpp:919:10
    #7 0x7fff8881a2e2 in CPDF_RenderStatus::ProcessObjectNoClip(CPDF_PageObject*, CFX_Matrix const&) third_party/pdfium/core/fpdfapi/render/cpdf_renderstatus.cpp:310:14
    #8 0x7fff8881a90c in CPDF_RenderStatus::ContinueSingleObject(CPDF_PageObject*, CFX_Matrix const&, PauseIndicatorIface*) third_party/pdfium/core/fpdfapi/render/cpdf_renderstatus.cpp:281:5
    #9 0x7fff88806c12 in CPDF_ProgressiveRenderer::Continue(PauseIndicatorIface*) third_party/pdfium/core/fpdfapi/render/cpdf_progressiverenderer.cpp:95:29
    #10 0x7fff882ce4e9 in (anonymous namespace)::RenderPageImpl(CPDF_PageRenderContext*, CPDF_Page*, CFX_Matrix const&, FX_RECT const&, int, FPDF_COLORSCHEME_ const*, bool, CPDFSDK_PauseAdapter*) third_party/pdfium/fpdfsdk/cpdfsdk_renderpage.cpp:87:23
    #11 0x7fff882ce840 in CPDFSDK_RenderPageWithContext(CPDF_PageRenderContext*, CPDF_Page*, int, int, int, int, int, int, FPDF_COLORSCHEME_ const*, bool, CPDFSDK_PauseAdapter*) third_party/pdfium/fpdfsdk/cpdfsdk_renderpage.cpp:117:3
    #12 0x7fff883157e8 in FPDF_RenderPageBitmapWithColorScheme_Start third_party/pdfium/fpdfsdk/fpdf_progressive.cpp:83:3
    #13 0x7fff88315a67 in FPDF_RenderPageBitmap_Start third_party/pdfium/fpdfsdk/fpdf_progressive.cpp:126:10
    #14 0x555562907ffe in chrome_pdf::PDFiumEngine::ContinuePaint(unsigned long, SkBitmap&) pdf/pdfium/pdfium_engine.cc:3574:10
    #15 0x555562907052 in chrome_pdf::PDFiumEngine::Paint(gfx::Rect const&, SkBitmap&, std::__Cr::vector<gfx::Rect, std::__Cr::allocator<gfx::Rect>>&, std::__Cr::vector<gfx::Rect, std::__Cr::allocator<gfx::Rect>>&) pdf/pdfium/pdfium_engine.cc:864:11
    #16 0x55556a59eb20 in chrome_pdf::PdfViewWebPlugin::DoPaint(std::__Cr::vector<gfx::Rect, std::__Cr::allocator<gfx::Rect>> const&, std::__Cr::vector<chrome_pdf::PaintReadyRect, std::__Cr::allocator<chrome_pdf::PaintReadyRect>>&, std::__Cr::vector<gfx::Rect, std::__Cr::allocator<gfx::Rect>>&) pdf/pdf_view_web_plugin.cc:2424:16
    #17 0x55556a59f7bd in non-virtual thunk to chrome_pdf::PdfViewWebPlugin::OnPaint(std::__Cr::vector<gfx::Rect, std::__Cr::allocator<gfx::Rect>> const&, std::__Cr::vector<chrome_pdf::PaintReadyRect, std::__Cr::allocator<chrome_pdf::PaintReadyRect>>&, std::__Cr::vector<gfx::Rect, std::__Cr::allocator<gfx::Rect>>&) pdf/pdf_view_web_plugin.cc:2372:3
    #18 0x5555628e4768 in chrome_pdf::PaintManager::DoPaint() pdf/paint_manager.cc:377:12
    #19 0x5555628e8674 in base::internal::Invoker<...>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #20 0x7ffff6b60c82 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #21 0x7ffff6be216e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #22 0x7ffff6be1146 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #23 0x7ffff6a033f1 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #24 0x7ffff6be37e8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #25 0x7ffff6acb002 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #26 0x7fffec6025e5 in content::RendererMain(content::MainFunctionParams) content/renderer/renderer_main.cc:364:16
    #27 0x7fffeca34c27 in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:664:14
    #28 0x7fffeca35dee in content::RunOtherNamedProcessTypeMain(...) content/app/content_main_runner_impl.cc:771:12
    #29 0x7fffeca3834a in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1150:10
    #30 0x7fffeca32ad3 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:358:36
    #31 0x7fffeca32e5a in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:371:10
    #32 0x55555bd7ff15 in ChromeMain chrome/app/chrome_main.cc:191:12
    #33 0x7fff86429d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

0x7d8f7845f284 is located 0 bytes after 1028-byte region [0x7d8f7845ee80,0x7d8f7845f284)
allocated by thread T0 (chrome) here:
    #0 0x55555bd44f02 in calloc (out/asan-release/chrome+0x67f0f02) (BuildId: 7567412c12a003b9)
    #1 0x7fff882348ed in CFX_DIBitmap::Create(int, int, FXDIB_Format, unsigned char*, unsigned int) third_party/pdfium/core/fxge/dib/cfx_dibitmap.cpp:74:9
    #2 0x7fff881fc910 in CFX_Face::RenderGlyph(CFX_Font const*, unsigned int, bool, CFX_Matrix const&, int, FontAntiAliasingMode) third_party/pdfium/core/fxge/cfx_face.cpp:592:35
    #3 0x7fff88213c1e in CFX_GlyphCache::LookUpGlyphBitmap(CFX_Font const*, CFX_Matrix const&, fxcrt::ByteString const&, unsigned int, bool, int, FontAntiAliasingMode) third_party/pdfium/core/fxge/cfx_glyphcache.cpp:128:17
    #4 0x7fff8821366c in CFX_GlyphCache::LoadGlyphBitmap(CFX_Font const*, unsigned int, bool, CFX_Matrix const&, int, FontAntiAliasingMode, CFX_TextRenderOptions*) third_party/pdfium/core/fxge/cfx_glyphcache.cpp:181:12
    #5 0x7fff882085a3 in CFX_Font::LoadGlyphBitmap(unsigned int, bool, CFX_Matrix const&, int, FontAntiAliasingMode, CFX_TextRenderOptions*) const third_party/pdfium/core/fxge/cfx_font.cpp:400:35
    #6 0x7fff882225ac in CFX_RenderDevice::DrawNormalText(pdfium::span<TextCharPos const, 18446744073709551615ul, TextCharPos const*>, CFX_Font*, float, CFX_Matrix const&, unsigned int, CFX_TextRenderOptions const&) third_party/pdfium/core/fxge/cfx_renderdevice.cpp:1183:26
    #7 0x7fff8882d555 in CPDF_TextRenderer::DrawNormalText(...) third_party/pdfium/core/fpdfapi/render/cpdf_textrenderer.cpp:176:17
    #8 0x7fff8881b097 in CPDF_RenderStatus::ProcessText(CPDF_TextObject*, CFX_Matrix const&, CFX_Path*) third_party/pdfium/core/fpdfapi/render/cpdf_renderstatus.cpp:919:10
    #9 0x7fff8881a2e2 in CPDF_RenderStatus::ProcessObjectNoClip(CPDF_PageObject*, CFX_Matrix const&) third_party/pdfium/core/fpdfapi/render/cpdf_renderstatus.cpp:310:14
    #10 0x7fff8881a90c in CPDF_RenderStatus::ContinueSingleObject(CPDF_PageObject*, CFX_Matrix const&, PauseIndicatorIface*) third_party/pdfium/core/fpdfapi/render/cpdf_renderstatus.cpp:281:5
    #11 0x7fff88806c12 in CPDF_ProgressiveRenderer::Continue(PauseIndicatorIface*) third_party/pdfium/core/fpdfapi/render/cpdf_progressiverenderer.cpp:95:29
    #12 0x7fff882ce4e9 in RenderPageImpl(...) third_party/pdfium/fpdfsdk/cpdfsdk_renderpage.cpp:87:23
    #13 0x7fff882ce840 in CPDFSDK_RenderPageWithContext(...) third_party/pdfium/fpdfsdk/cpdfsdk_renderpage.cpp:117:3
    #14 0x7fff883157e8 in FPDF_RenderPageBitmapWithColorScheme_Start third_party/pdfium/fpdfsdk/fpdf_progressive.cpp:83:3
    #15 0x7fff88315a67 in FPDF_RenderPageBitmap_Start third_party/pdfium/fpdfsdk/fpdf_progressive.cpp:126:10
    #16 0x555562907ffe in chrome_pdf::PDFiumEngine::ContinuePaint(unsigned long, SkBitmap&) pdf/pdfium/pdfium_engine.cc:3574:10
    #17 0x555562907052 in chrome_pdf::PDFiumEngine::Paint(...) pdf/pdfium/pdfium_engine.cc:864:11
    ...
    #26 0x7fffec6025e5 in content::RendererMain(content::MainFunctionParams) content/renderer/renderer_main.cc:364:16
    #32 0x55555bd7ff15 in ChromeMain chrome/app/chrome_main.cc:191:12

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/pdfium/core/fxge/cfx_face.cpp:608:54 in CFX_Face::RenderGlyph(CFX_Font const*, unsigned int, bool, CFX_Matrix const&, int, FontAntiAliasingMode)
==2151182==ABORTING

```
## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 1.8 KB)
- [asan.log](attachments/asan.log) (text/plain, 21.1 KB)
- [readme.md](attachments/readme.md) (text/markdown, 1.5 KB)

## Timeline

### je...@gmail.com (2026-03-01)

## Affected Platforms

The affected platforms are Linux and Windows. Android is not affected because Chrome on Android does not use the built-in PDFium-based PDF viewer; instead, PDFs are downloaded and opened by external applications. macOS is not affected because the AGG renderer's `DrawDeviceText` has a platform-specific implementation in `core/fxge/apple/fx_apple_impl.cpp` that uses Core Graphics to render text directly. When this path succeeds, it returns true and the vulnerable software bitmap path (`LoadGlyphBitmap` to `RenderGlyph`) is never reached. The stub implementation that unconditionally returns false, which forces the fallback to the vulnerable path, is compiled only on non-Apple platforms (`#if !BUILDFLAG(IS_APPLE)`).

### ts...@google.com (2026-03-02)

Repro'd under Chrome 147.0.7703.0 / Linux. Setting found-in to extended stable as this has likely been present since beginning of the code base.

### ts...@google.com (2026-03-02)

(Still searching for flags to reproduce this under pdfium_test).

### dx...@google.com (2026-03-02)

Project: pdfium  

Branch:  main  

Author:  Tom Sepez [tsepez@google.com](mailto:tsepez@google.com)  

Link:    <https://pdfium-review.googlesource.com/144030>

Spanify more of CFX\_Face::RenderGlyph().

---


Expand for full commit details
```
     
    Bug: 488585504 
    Change-Id: I0a7baff50edddb58f5c73193c38ce5e38b6930d3 
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/144030 
    Commit-Queue: Tom Sepez <tsepez@chromium.org> 
    Reviewed-by: Lei Zhang <thestig@chromium.org>

```

---

Files:

- M `core/fxge/cfx_face.cpp`

---

Hash: 1765e514c52f0bbda24041e37fd1c61d09bda831  

Date: Mon Mar 2 20:07:47 2026


---

### ts...@google.com (2026-03-02)

So this is "fixed" in the sense that the new safe code will hit a hard CHECK() rather than OOB, but there is work to make it do something more desirable in this situation.

### dx...@google.com (2026-03-02)

Project: pdfium  

Branch:  main  

Author:  Tom Sepez [tsepez@google.com](mailto:tsepez@google.com)  

Link:    <https://pdfium-review.googlesource.com/144051>

Avoid mismatch between k8bppMask and 3 byte constant.

---


Expand for full commit details
```
     
    Bug: 488585504 
    Change-Id: I01123e3a3566c5f9ffe89dfdfbe8779ad5e7108a 
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/144051 
    Reviewed-by: Lei Zhang <thestig@chromium.org> 
    Commit-Queue: Tom Sepez <tsepez@chromium.org>

```

---

Files:

- M `core/fxge/cfx_face.cpp`

---

Hash: ee83ca8ef7b8804ef7ed735b200a1e27c5285bac  

Date: Mon Mar 2 22:40:57 2026


---

### ts...@google.com (2026-03-02)

And the second CL should make it actually fixed without CHECK().

### dx...@google.com (2026-03-03)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7624394>

Roll PDFium from 0c38b00a3baf to f99c212599bb (4 revisions)

---


Expand for full commit details
```
     
    https://pdfium.googlesource.com/pdfium.git/+log/0c38b00a3baf..f99c212599bb 
     
    2026-03-02 helmut@januschka.com Replace TEXTPOS defines with a typed enum 
    2026-03-02 tsepez@google.com Avoid mismatch between k8bppMask and 3 byte constant. 
    2026-03-02 tsepez@google.com Spanify source data in CFX_Face::RenderGlyph() 
    2026-03-02 tsepez@google.com Spanify more of CFX_Face::RenderGlyph(). 
     
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
     
    Bug: chromium:42270078,chromium:488585504 
    Tbr: akall@google.com 
    Change-Id: I7f2a8c6bbabec6800d5248bc934c237a3320c7a6 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7624394 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1593011}

```

---

Files:

- M `DEPS`
- M `third_party/pdfium`

---

Hash: [f80620bb790afd66b7c5e749c8ba360ada355409](https://chromiumdash.appspot.com/commit/f80620bb790afd66b7c5e749c8ba360ada355409)  

Date: Tue Mar 3 06:25:52 2026


---

### ch...@google.com (2026-03-03)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-03)

Security Merge Request Consideration: Requesting merge to extended stable (M144) because latest trunk commit (1593011) appears to be after extended stable branch point (1552494).
Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1593011) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1593011) appears to be after beta branch point (1582197).
Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [144, 145, 146].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dr...@chromium.org (2026-03-04)

tsepez@ - how much do we want to merge here? I would lean towards just <https://pdfium-review.googlesource.com/144030>, but I don't know how hard it is to cherry-pick outside of a pdfium roll.

### ts...@google.com (2026-03-04)

We should take both.  Cherry-pick should be straightforward.

### dr...@chromium.org (2026-03-04)

Sounds good. I don't see any crashes in Canary, so approving a merge of both CLs to M146.

We don't plan any more M144 or M145 releases, so no need to do those.

### ts...@google.com (2026-03-04)

... And I got merge conflict, so not so straightforward. Stay tuned.

### ts...@google.com (2026-03-04)

https://pdfium-review.git.corp.google.com/c/pdfium/+/144270 is the smallest manual patch I could conceive which will fix the issue.

### dx...@google.com (2026-03-05)

Project: pdfium  

Branch:  chromium/7680  

Author:  Tom Sepez [tsepez@google.com](mailto:tsepez@google.com)  

Link:    <https://pdfium-review.googlesource.com/144270>

[M146] Manually patch logic for k8bppmask and 3 byte constant

---


Expand for full commit details
```
     
    Bug: 488585504 
    Change-Id: I15911d3c40a1533359f13e21813f49af489315b1 
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/144270 
    Reviewed-by: Andy Phan <andyphan@chromium.org>

```

---

Files:

- M `core/fxge/cfx_face.cpp`

---

Hash: bccc616f83aaed08f65d4a707dfe00e24133772b  

Date: Thu Mar 5 19:41:21 2026


---

### pe...@google.com (2026-03-05)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2026-03-10)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-03-10)

1. https://pdfium-review.git.corp.google.com/c/pdfium/+/144350
2. Low - There was a conflict, but it's not complicated.
3. 146
4. Yes, the issue was introduced by the initial commit[1], thus M138 branch also has the issue. 

[1] Introducing Commit: `5110c4743751145c4ae1934cd1d83bc6c55bb43f`
       - Date: 2014-05-17
       - Author: John Abd-El-Malek
       - Review: Initial PDFium commit

### dx...@google.com (2026-03-10)

Project: pdfium  

Branch:  chromium/7204  

Author:  Tom Sepez [tsepez@google.com](mailto:tsepez@google.com)  

Link:    <https://pdfium-review.googlesource.com/144350>

[M138-LTS] Manually patch logic for k8bppmask and 3 byte constant

---


Expand for full commit details
```
     
    Bug: 488585504 
    Change-Id: I15911d3c40a1533359f13e21813f49af489315b1 
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/144270 
    Reviewed-by: Andy Phan <andyphan@chromium.org> 
    (cherry picked from commit bccc616f83aaed08f65d4a707dfe00e24133772b) 
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/144350 
    Reviewed-by: Tom Sepez <tsepez@chromium.org>

```

---

Files:

- M `core/fxge/cfx_face.cpp`

---

Hash: 6b490ca2247fd99fffaf9da344d88a26016cda0e  

Date: Tue Mar 10 16:30:33 2026


---

### an...@google.com (2026-03-16)

re:[#comment20](https://issues.chromium.org/issues/488585504#comment20) Delayed until M146 soaked in Stable.

### an...@google.com (2026-04-01)

Merge approved for LTS-138

### sp...@google.com (2026-04-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
High quality with bisect. Renderer RCE / memory corruption in a sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2026-05-08)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-05-08)

1. <https://pdfium-review.git.corp.google.com/c/pdfium/+/147270>
2. Low - There was a conflict, but it's not complicated.
3. 146
4. Yes, the issue was introduced a long time ago.

### dx...@google.com (2026-05-29)

Project: pdfium  

Branch:  chromium/7559  

Author:  Tom Sepez [tsepez@google.com](mailto:tsepez@google.com)  

Link:    <https://pdfium-review.googlesource.com/147270>

[M144-LTS] Manually patch logic for k8bppmask and 3 byte constant

---


Expand for full commit details
```
     
    Bug: 488585504 
    Change-Id: I15911d3c40a1533359f13e21813f49af489315b1 
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/144270 
    Reviewed-by: Andy Phan <andyphan@chromium.org> 
    (cherry picked from commit bccc616f83aaed08f65d4a707dfe00e24133772b) 
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/147270 
    Reviewed-by: Tom Sepez <tsepez@chromium.org>

```

---

Files:

- M `core/fxge/cfx_face.cpp`

---

Hash: 6bd55c4cfb0dc1dccd547b161a0d56d6de0c6aeb  

Date: Fri May 29 17:22:10 2026


---

### ch...@google.com (2026-06-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/488585504)*
