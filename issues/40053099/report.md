# Security: heap-buffer-overflow in "SkiaState::AdjustClip" function

| Field | Value |
|-------|-------|
| **Issue ID** | [40053099](https://issues.chromium.org/issues/40053099) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pa...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2020-08-16 |
| **Bounty** | $5,000.00 |

## Description

**-------------------------**

**VULNERABILITY DETAILS**  

Hi, our developed fuzzer found a heap-buffer-overflow bug in "SkData::AdjustClip" when fuzzing pdfium\_test.

In

```
 void AdjustClip(int limit) {  
    while (m_clipIndex > limit) {  
      do {  
        --m_clipIndex;  
        ASSERT(m_clipIndex >= 0);  
      } while (m_commands[m_clipIndex] != Clip::kSave); // here m_clipIndex < 0  
      m_pDriver->SkiaCanvas()->restore();  
    }  
...  

```

As I built the pdfium\_test with release version, the check `ASSERT(m_clipIndex>=0)` does not work.

The log of ASAN is

```
==12963==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60300001758c at pc 0x55e97ea55f9a bp 0x7ffc4bd14c90 sp 0x7ffc4bd14c88  
READ of size 4 at 0x60300001758c thread T0  
    #0 0x55e97ea55f99 in SkiaState::AdjustClip(int) core/fxge/skia/fx_skia_device.cpp:1241:16  
    #1 0x55e97ea42106 in SkiaState::Flush() core/fxge/skia/fx_skia_device.cpp:1261:7  
    #2 0x55e97ea42106 in CFX_SkiaDeviceDriver::Flush() core/fxge/skia/fx_skia_device.cpp:1684:13  
    #3 0x55e97ea42106 in CFX_SkiaDeviceDriver::~CFX_SkiaDeviceDriver() core/fxge/skia/fx_skia_device.cpp:1678:3  
    #4 0x55e97ea4257d in CFX_SkiaDeviceDriver::~CFX_SkiaDeviceDriver() core/fxge/skia/fx_skia_device.cpp:1677:47  
    #5 0x55e97ea5599f in CFX_DefaultRenderDevice::~CFX_DefaultRenderDevice() core/fxge/skia/fx_skia_device.cpp:2774:3  
    #6 0x55e97f411b7a in CPDF_RenderStatus::LoadSMask(CPDF_Dictionary\*, FX_RECT\*, CFX_Matrix const\*) core/fpdfapi/render/cpdf_renderstatus.cpp:1475:1  
    #7 0x55e97f407a70 in CPDF_RenderStatus::ProcessTransparency(CPDF_PageObject\*, CFX_Matrix const&) core/fpdfapi/render/cpdf_renderstatus.cpp:701:9  
    #8 0x55e97f40572e in CPDF_RenderStatus::RenderSingleObject(CPDF_PageObject\*, CFX_Matrix const&) core/fpdfapi/render/cpdf_renderstatus.cpp:239:7  
    #9 0x55e97f405388 in CPDF_RenderStatus::RenderObjectList(CPDF_PageObjectHolder const\*, CFX_Matrix const&) core/fpdfapi/render/cpdf_renderstatus.cpp:215:5  
    #10 0x55e97f40deac in CPDF_RenderStatus::ProcessForm(CPDF_FormObject const\*, CFX_Matrix const&) core/fpdfapi/render/cpdf_renderstatus.cpp:390:12  
    #11 0x55e97f408d51 in CPDF_RenderStatus::ProcessObjectNoClip(CPDF_PageObject\*, CFX_Matrix const&) core/fpdfapi/render/cpdf_renderstatus.cpp:315:14  
    #12 0x55e97f409388 in CPDF_RenderStatus::ContinueSingleObject(CPDF_PageObject\*, CFX_Matrix const&, PauseIndicatorIface\*) core/fpdfapi/render/cpdf_renderstatus.cpp:272:5  
    #13 0x55e97f3f1059 in CPDF_ProgressiveRenderer::Continue(PauseIndicatorIface\*) core/fpdfapi/render/cpdf_progressiverenderer.cpp:88:30  
    #14 0x55e97e7c16f7 in (anonymous namespace)::RenderPageImpl(CPDF_PageRenderContext\*, CPDF_Page\*, CFX_Matrix const&, FX_RECT const&, int, FPDF_COLORSCHEME_ const\*, bool, CPDFSDK_PauseAdapter\*) fpdfsdk/cpdfsdk_renderpage.cpp:80:26  
    #15 0x55e97e7c1ad6 in CPDFSDK_RenderPageWithContext(CPDF_PageRenderContext\*, CPDF_Page\*, int, int, int, int, int, int, FPDF_COLORSCHEME_ const\*, bool, CPDFSDK_PauseAdapter\*) fpdfsdk/cpdfsdk_renderpage.cpp:109:3  
    #16 0x55e97e7d8b47 in FPDF_RenderPageBitmapWithColorScheme_Start fpdfsdk/fpdf_progressive.cpp:73:3  
    #17 0x55e97e74e10f in (anonymous namespace)::ProcessPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__\*, fpdf_form_handle_t__\*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest\*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:792:16  
    #18 0x55e97e74e10f in (anonymous namespace)::ProcessPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const\*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:1017:9  
    #19 0x55e97e74e10f in main samples/pdfium_test.cc:1246:5  
    #20 0x7f354ced6b96 in __libc_start_main /build/glibc-2ORdQG/glibc-2.27/csu/../csu/libc-start.c:310  
  
0x60300001758c is located 4 bytes to the left of 24-byte region [0x603000017590,0x6030000175a8)  
allocated by thread T0 here:  
    #0 0x55e97e719379 in realloc /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:164:3  
    #1 0x55e97fd9ed5d in sk_realloc_throw(void\*, unsigned long) third_party/skia/src/ports/SkMemory_malloc.cpp:65:35  
    #2 0x55e97ea594bf in SkTDArray<SkiaState::Clip>::resizeStorageToAtLeast(int) third_party/skia/include/private/SkTDArray.h:375:22  
    #3 0x55e97ea594bf in SkTDArray<SkiaState::Clip>::setCount(int) third_party/skia/include/private/SkTDArray.h:153:19  
    #4 0x55e97ea594bf in SkTDArray<SkiaState::Clip>::adjustCount(int) third_party/skia/include/private/SkTDArray.h:354:15  
    #5 0x55e97ea594bf in SkTDArray<SkiaState::Clip>::append(int, SkiaState::Clip const\*) third_party/skia/include/private/SkTDArray.h:184:19  
    #6 0x55e97ea594bf in SkTDArray<SkiaState::Clip>::append() third_party/skia/include/private/SkTDArray.h:176:22  
    #7 0x55e97ea594bf in SkTDArray<SkiaState::Clip>::push_back(SkiaState::Clip const&) third_party/skia/include/private/SkTDArray.h:274:41  
    #8 0x55e97ea59da0 in SkiaState::SetClip(SkPath const&) core/fxge/skia/fx_skia_device.cpp:1096:18  
    #9 0x55e97ea4883a in SkiaState::SetClipFill(CFX_PathData const\*, CFX_Matrix const\*, CFX_FillRenderOptions const&) core/fxge/skia/fx_skia_device.cpp:1072:12  
    #10 0x55e97ea4765b in CFX_SkiaDeviceDriver::SetClip_PathFill(CFX_PathData const\*, CFX_Matrix const\*, CFX_FillRenderOptions const&) core/fxge/skia/fx_skia_device.cpp:1981:27  
    #11 0x55e97e9d894e in CFX_RenderDevice::SetClip_PathFill(CFX_PathData const\*, CFX_Matrix const\*, CFX_FillRenderOptions const&) core/fxge/cfx_renderdevice.cpp:417:25  
    #12 0x55e97f405aee in CPDF_RenderStatus::ProcessClipPath(CPDF_ClipPath const&, CFX_Matrix const&) core/fpdfapi/render/cpdf_renderstatus.cpp:524:18  
    #13 0x55e97f405719 in CPDF_RenderStatus::RenderSingleObject(CPDF_PageObject\*, CFX_Matrix const&) core/fpdfapi/render/cpdf_renderstatus.cpp:238:3  
    #14 0x55e97f405388 in CPDF_RenderStatus::RenderObjectList(CPDF_PageObjectHolder const\*, CFX_Matrix const&) core/fpdfapi/render/cpdf_renderstatus.cpp:215:5  
    #15 0x55e97f410ec7 in CPDF_RenderStatus::LoadSMask(CPDF_Dictionary\*, FX_RECT\*, CFX_Matrix const\*) core/fpdfapi/render/cpdf_renderstatus.cpp:1433:10  
    #16 0x55e97f407a70 in CPDF_RenderStatus::ProcessTransparency(CPDF_PageObject\*, CFX_Matrix const&) core/fpdfapi/render/cpdf_renderstatus.cpp:701:9  
    #17 0x55e97f40572e in CPDF_RenderStatus::RenderSingleObject(CPDF_PageObject\*, CFX_Matrix const&) core/fpdfapi/render/cpdf_renderstatus.cpp:239:7  
    #18 0x55e97f405388 in CPDF_RenderStatus::RenderObjectList(CPDF_PageObjectHolder const\*, CFX_Matrix const&) core/fpdfapi/render/cpdf_renderstatus.cpp:215:5  
    #19 0x55e97f40deac in CPDF_RenderStatus::ProcessForm(CPDF_FormObject const\*, CFX_Matrix const&) core/fpdfapi/render/cpdf_renderstatus.cpp:390:12  
    #20 0x55e97f408d51 in CPDF_RenderStatus::ProcessObjectNoClip(CPDF_PageObject\*, CFX_Matrix const&) core/fpdfapi/render/cpdf_renderstatus.cpp:315:14  
    #21 0x55e97f409388 in CPDF_RenderStatus::ContinueSingleObject(CPDF_PageObject\*, CFX_Matrix const&, PauseIndicatorIface\*) core/fpdfapi/render/cpdf_renderstatus.cpp:272:5  
    #22 0x55e97f3f1059 in CPDF_ProgressiveRenderer::Continue(PauseIndicatorIface\*) core/fpdfapi/render/cpdf_progressiverenderer.cpp:88:30  
    #23 0x55e97e7c16f7 in (anonymous namespace)::RenderPageImpl(CPDF_PageRenderContext\*, CPDF_Page\*, CFX_Matrix const&, FX_RECT const&, int, FPDF_COLORSCHEME_ const\*, bool, CPDFSDK_PauseAdapter\*) fpdfsdk/cpdfsdk_renderpage.cpp:80:26  
    #24 0x55e97e7c1ad6 in CPDFSDK_RenderPageWithContext(CPDF_PageRenderContext\*, CPDF_Page\*, int, int, int, int, int, int, FPDF_COLORSCHEME_ const\*, bool, CPDFSDK_PauseAdapter\*) fpdfsdk/cpdfsdk_renderpage.cpp:109:3  
    #25 0x55e97e7d8b47 in FPDF_RenderPageBitmapWithColorScheme_Start fpdfsdk/fpdf_progressive.cpp:73:3  
    #26 0x55e97e74e10f in (anonymous namespace)::ProcessPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__\*, fpdf_form_handle_t__\*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest\*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:792:16  
    #27 0x55e97e74e10f in (anonymous namespace)::ProcessPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const\*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:1017:9  
    #28 0x55e97e74e10f in main samples/pdfium_test.cc:1246:5  
    #29 0x7f354ced6b96 in __libc_start_main /build/glibc-2ORdQG/glibc-2.27/csu/../csu/libc-start.c:310  
  
SUMMARY: AddressSanitizer: heap-buffer-overflow core/fxge/skia/fx_skia_device.cpp:1241:16 in SkiaState::AdjustClip(int)  
Shadow bytes around the buggy address:  
  0x0c067fffae60: fd fd fa fa fd fd fd fd fa fa 00 00 00 00 fa fa  
  0x0c067fffae70: fd fd fd fd fa fa 00 00 00 fa fa fa fd fd fd fd  
  0x0c067fffae80: fa fa fd fd fd fd fa fa fd fd fd fd fa fa fd fd  
  0x0c067fffae90: fd fd fa fa fd fd fd fd fa fa fd fd fd fd fa fa  
  0x0c067fffaea0: fd fd fd fd fa fa fd fd fd fa fa fa fd fd fd fa  
=>0x0c067fffaeb0: fa[fa]00 00 00 fa fa fa fd fd fd fa fa fa fd fd  
  0x0c067fffaec0: fd fa fa fa fd fd fd fd fa fa fd fd fd fa fa fa  
  0x0c067fffaed0: fd fd fd fa fa fa fd fd fd fa fa fa fd fd fd fd  
  0x0c067fffaee0: fa fa 00 00 00 fa fa fa fd fd fd fa fa fa fa fa  
  0x0c067fffaef0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
  0x0c067fffaf00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
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
  Shadow gap:              cc  
==12963==ABORTING  

```

**VERSION**  

pdfium version: commit e14f607a5ce7bffb073e5095c8659bbbb2c936d0  

link is <https://pdfium.googlesource.com/pdfium/+/e14f607a5ce7bffb073e5095c8659bbbb2c936d0>

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

LABEL  

Cr-Internals-Plugins-PDF

## Attachments

- [poc_heap_buffer_overlow](attachments/poc_heap_buffer_overlow) (text/plain, 800 B)

## Timeline

### cp...@stevens.edu (2020-08-16)

Integer underflow.

### va...@chromium.org (2020-08-17)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### cl...@chromium.org (2020-08-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5636454629310464.

### cl...@chromium.org (2020-08-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5732716724682752.

### va...@chromium.org (2020-08-17)

pdf_use_skia, so impact: none.

### va...@chromium.org (2020-08-17)

Tentatively adding Security_Severity-Medium, tsepez@ please feel free to change.

### th...@chromium.org (2020-08-17)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### es...@chromium.org (2021-02-24)

hcm@, could you please help find an active owner for this bug?

### ni...@chromium.org (2021-02-24)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### ni...@chromium.org (2021-03-12)

https://pdfium-review.googlesource.com/c/pdfium/+/78570 WIP.

### gi...@appspot.gserviceaccount.com (2021-03-15)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/5a4cc47b4b0b5cccae16ff386a08e4dc6f7e2578

commit 5a4cc47b4b0b5cccae16ff386a08e4dc6f7e2578
Author: Hui Yingst <nigi@chromium.org>
Date: Mon Mar 15 20:06:43 2021

Avoid integer underflow in SkiaState::AdjustClip().

When the current `m_clipIndex` is larger than the given `limit` index,
SkiaState::AdjustClip() looks through the index range below the current
`m_clipIndex` until it finds a save command to restore. If no save
command is found, it reaches an assertion failure due to the index being
negative.

This CL makes sure `m_clipIndex` is non-negative when using it to access
and check command types. If no save command is found, skip restoring
and set `m_clipIndex` to 0, so that all commands below index `limit` can
be processed later. The added pixel test is a minimized version of the
PDF that triggered the assertion failure in crbug.com/1116869.

Bug: chromium:1116869
Change-Id: I47a71918c561c1cb121b91f929d3f0f60b3f22e9
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/78570
Reviewed-by: Daniel Hosseinian <dhoss@chromium.org>
Commit-Queue: Hui Yingst <nigi@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/5a4cc47b4b0b5cccae16ff386a08e4dc6f7e2578/core/fxge/skia/fx_skia_device.cpp
[add] https://pdfium.googlesource.com/pdfium/+/5a4cc47b4b0b5cccae16ff386a08e4dc6f7e2578/testing/resources/pixel/bug_1116869.in
[add] https://pdfium.googlesource.com/pdfium/+/5a4cc47b4b0b5cccae16ff386a08e4dc6f7e2578/testing/resources/pixel/bug_1116869_expected.pdf.0.png


### gi...@appspot.gserviceaccount.com (2021-03-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8ea38e0b1ca661b9198cfc8511495b5cfcbd78b5

commit 8ea38e0b1ca661b9198cfc8511495b5cfcbd78b5
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Mar 15 20:53:37 2021

Roll PDFium from a01468f95684 to 5a4cc47b4b0b (1 revision)

https://pdfium.googlesource.com/pdfium.git/+log/a01468f95684..5a4cc47b4b0b

2021-03-15 nigi@chromium.org Avoid integer underflow in SkiaState::AdjustClip().

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Bug: chromium:1116869
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I865b8563812bd9eb242cc0a8caf7c408bbf4085c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2762240
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#862950}

[modify] https://crrev.com/8ea38e0b1ca661b9198cfc8511495b5cfcbd78b5/DEPS


### ni...@chromium.org (2021-03-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-16)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-24)

Congratulations, Chengbin Pang & Jun Xu! The VRP Panel has decided to award you $5000 for this report. A member of our finance team will be in touch soon to arrange payment. Thanks for this report and good work! 

### am...@google.com (2021-03-25)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-25)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-06-24)

This issue was migrated from crbug.com/chromium/1116869?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053099)*
