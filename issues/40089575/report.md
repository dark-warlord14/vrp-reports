# signed integer overflow in blink::WebGLRenderingContextBase::ValidateTexImageSubRectangle<blink::Image>

| Field | Value |
|-------|-------|
| **Issue ID** | [40089575](https://issues.chromium.org/issues/40089575) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>WebGL |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | tk...@googlemail.com |
| **Assignee** | zm...@chromium.org |
| **Created** | 2017-11-12 |
| **Bounty** | $4,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36

Steps to reproduce the problem:
VULNERABILITY DETAILS

A signed integer overflow vulnerability allows to bypass a validation check in ValidateTexImageSubRectangle(), which later on leads to a heap buffer underflow (out-of-bounds read). This out-of-bounds read can be used to reveal heap memory contents (information leak).

The attached testcase (testcase.html) crashes the latest ASAN build of Chrome on Windows 10 as follows (the complete stack trace can be found in asan.txt):

=================================================================
==8908==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x26600000 at pc 0x1c64dd73 bp 0x001daac4 sp 0x001daab8
READ of size 16 at 0x26600000 thread T0
    #0 0x1c64dd72 in blink::`anonymous namespace'::Unpack<18,unsigned char,unsigned char> C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\platform\graphics\gpu\WebGLImageConversion.cpp:468:1
    #1 0x1c64f0fe in blink::`anonymous namespace'::FormatConverter::Convert<blink::WebGLImageConversion::DataFormat::kDataFormatBGRA8> C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\platform\graphics\gpu\WebGLImageConversion.cpp:2373:3
    #2 0x1c63e72e in blink::WebGLImageConversion::PackPixels(unsigned char const *,enum blink::WebGLImageConversion::DataFormat,unsigned int,unsigned int,class blink::IntRect const &,int,unsigned int,int,unsigned int,unsigned int,enum blink::WebGLImageConversion::AlphaOp,void *,bool) C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\platform\graphics\gpu\WebGLImageConversion.cpp:3124:5
..

I have also developed a proof-of-concept exploit to demonstrate that exploitation of this vulnerability is very likely (for details, please refer to the attached file poc.html).

Relevant source code snippets:

See https://cs.chromium.org/chromium/src/third_party/WebKit/Source/modules/webgl/WebGLRenderingContextBase.h:

..
1040  template <typename T>
1041  bool ValidateTexImageSubRectangle(const char* function_name,
1042                                    TexImageFunctionID function_id,
1043                                    T* image,
1044                                    const IntRect& sub_rect,
1045                                    GLsizei depth,
1046                                    GLint unpack_image_height,
1047                                    bool* selecting_sub_rectangle) {
..
1052    int image_height = static_cast<int>(image->height());
..
1066    if (sub_rect.X() < 0 || sub_rect.Y() < 0 || sub_rect.MaxX() > image_width ||
1067        sub_rect.MaxY() > image_height || sub_rect.Width() < 0 ||
1068        sub_rect.Height() < 0) {
1069      SynthesizeGLError(GL_INVALID_OPERATION, function_name,
1070                        "source sub-rectangle specified via pixel unpack "
1071                        "parameters is invalid");
1072      return false;
1073    }
..

The function sub_rect.MaxY() (see line 1067) adds the value of the 2nd parameter of gl.pixelStorei (in testcase.html this value is set to 0x7fffff00) to the value of the 5th parameter of gl.texImage2D (in testcase.html this value is set to 0x3e8) and returns the sum as a signed integer value. The calculation can be expressed as this: 0x7fffff00 + 0x3e8 = 0x800002e8. This results in a signed integer overflow that causes the value to wrap and become negative (the value 0x800002e8 represents -2147482904 if interpreted as a signed integer value). It is then checked if -2147482904 > image_height (see also line 1067). The image in testcase.html (see ImageData) has a height and a width of 100 pixels, so the comparison -2147482904 > 100 returns a false result which bypasses the validation check.

See https://cs.chromium.org/chromium/src/third_party/WebKit/Source/platform/graphics/gpu/WebGLImageConversion.cpp:

..
2451 template <WebGLImageConversion::DataFormat SrcFormat,
2452           WebGLImageConversion::DataFormat DstFormat,
2453           WebGLImageConversion::AlphaOp alphaOp>
2454 void FormatConverter::Convert() {
..
2516   const SrcType* src_row_start =
2517       static_cast<const SrcType*>(static_cast<const void*>(
2518           static_cast<const uint8_t*>(src_start_) +
2519           ((src_stride_ * src_sub_rectangle_.Y()) + src_row_offset_))); 
..
2543   } else if (kTrivialPack) {
2544     for (int d = 0; d < depth_; ++d) {
2545       for (int i = 0; i < src_sub_rectangle_.Height(); ++i) {
2546         Unpack<SrcFormat>(src_row_start, dst_row_start,
2547                           src_sub_rectangle_.Width());
..

Then in FormatConverter::Convert(), a pointer called src_row_start is initialized with the address of the image source data (src_start_) plus an offset (see lines 2516-2519). The offset is calculated by multiplying the value of src_stride_ (which in this example is the result of 'image width * 4' or '100 * 4') with the return value of src_sub_rectangle_.Y(), which corresponds to the value of the 2nd parameter of gl.pixelStorei (which is set to the value 0x7fffff00 in testcase.html). Next, the value of src_row_offset_ (which in this example is 0) is added to the result. The calculation can be expressed as this: ((400 * 0x7fffff00) + 0) = 0xfffe7000. The variables src_stride_ and src_row_offset_ as well as the return value of src_sub_rectangle_.Y() are of the type signed int. Therefore, the result of the calculation becomes negative (the value 0xfffe7000 represents -102400 if interpreted as a signed integer value). This results in a negative offset: src_row_start = src_start_ - 102400. In consequence, src_row_start references a memory location prior to the beginning of the image source data (src_start_). Later on, src_row_start is passed as the first parameter to a function called Unpack() (see line 2546).

See https://cs.chromium.org/chromium/src/third_party/WebKit/Source/platform/graphics/gpu/WebGLImageConversion.cpp:

..
439 template <>
440 void Unpack<WebGLImageConversion::kDataFormatBGRA8, uint8_t, uint8_t>(
441     const uint8_t* source,
442     uint8_t* destination,
443     unsigned pixels_per_row) {
444   const uint32_t* source32 = reinterpret_cast_ptr<const uint32_t*>(source);
445   uint32_t* destination32 = reinterpret_cast_ptr<uint32_t*>(destination);
446
447 #if defined(ARCH_CPU_X86_FAMILY)
448   SIMD::UnpackOneRowOfBGRA8LittleToRGBA8(source32, destination32,
449                                          pixels_per_row);
450 #endif
..

In Unpack(), the function SIMD::UnpackOneRowOfBGRA8LittleToRGBA8() is called with the previously initialized pointer (src_row_start) as the first parameter (provided that the system is based on Intel's x86 family of CPUs, see lines 447 and 448).

See https://cs.chromium.org/chromium/src/third_party/WebKit/Source/platform/graphics/cpu/x86/WebGLImageConversionSSE.h:

119 ALWAYS_INLINE void UnpackOneRowOfBGRA8LittleToRGBA8(const uint32_t*& source,
120                                                     uint32_t*& destination,
121                                                     unsigned& pixels_per_row) {
122   __m128i bgra, rgba;
123   __m128i br_mask = _mm_set1_epi32(0x00ff00ff);
124   __m128i ga_mask = _mm_set1_epi32(0xff00ff00);
125   unsigned pixels_per_row_trunc = (pixels_per_row / 4) * 4;
126
127   for (unsigned i = 0; i < pixels_per_row_trunc; i += 4) {
128     bgra = _mm_loadu_si128((const __m128i*)(source));
129     rgba = _mm_shufflehi_epi16(_mm_shufflelo_epi16(bgra, 0xB1), 0xB1);
130
131     rgba = _mm_or_si128(_mm_and_si128(rgba, br_mask),
132                         _mm_and_si128(bgra, ga_mask));
133     _mm_storeu_si128((__m128i*)(destination), rgba);
134
135     source += 4;
136     destination += 4;
137   }
138
139   pixels_per_row -= pixels_per_row_trunc;
140 }

In UnpackOneRowOfBGRA8LittleToRGBA8(), the data pointed to by the previously initialized pointer (src_row_start) is copied to the destination buffer (WebGL framebuffer). This leads to a heap buffer underflow (out-of-bounds read) as src_row_start references a memory location prior to the beginning of the image source data. This out-of-bounds read can be used to reveal heap memory contents (information leak; for more details, please refer to the attached files WinDbg_Chrome_Stable.txt and poc.html).

VERSION

Tested on: 

- Chrome Stable Version 62.0.3202.89 (64-Bit, Windows 10)
- asan-win32-release-514498

REPRODUCTION CASE

Provided files:

- testcase.html            -- Minimal testcase to trigger the issue.
- asan.txt                 -- Detailed ASAN output (Windows 10).
- WinDbg_Chrome_Stable.txt -- Further debugging information (Chrome Stable on Windows 10).
- poc.html                 -- Proof-of-Concept exploit to demonstrate that exploitation of this vulnerability is very likely.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: tab

What is the expected behavior?

What went wrong?
See VULNERABILITY DETAILS

Did this work before? N/A 

Chrome version: 62.0.3202.89  Channel: stable
OS Version: 10.0
Flash Version:

## Attachments

- [testcase.html](attachments/testcase.html) (text/plain, 4.7 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 10.3 KB)
- [WinDbg_Chrome_Stable.txt](attachments/WinDbg_Chrome_Stable.txt) (text/plain, 9.9 KB)
- [poc.html](attachments/poc.html) (text/plain, 17.6 KB)

## Timeline

### dt...@chromium.org (2017-11-12)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebGL]

### cl...@chromium.org (2017-11-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4644978960891904.

### cl...@chromium.org (2017-11-12)

Detailed report: https://clusterfuzz.com/testcase?key=4644978960891904

Job Type: windows_asan_chrome
Crash Type: Heap-buffer-overflow READ 16
Crash Address: 0x0f6e7400
Crash State:
  blink::Unpack<18,unsigned
  blink::FormatConverter::Convert<blink::WebGLImageConversion::DataFormat::kDataFo
  blink::WebGLImageConversion::PackPixels
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=495526:495536

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4644978960891904

See https://github.com/google/clusterfuzz-tools for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.


### es...@chromium.org (2017-11-12)

sugoi, kbr could you please take a look at this security bug? Thanks!

### sh...@chromium.org (2017-11-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-13)

[Empty comment from Monorail migration]

### kb...@chromium.org (2017-11-14)

Mo, is it possible for you to help with this?


### zm...@chromium.org (2017-11-14)

Sure!

### pa...@chromium.org (2017-11-29)

Any updates? I strongly recommend that you use the base/numerics templates and helper functions to resolve this class of bug. (https://chromium.googlesource.com/chromium/src/+/master/base/numerics/README.md)

Expect to find similarly vulnerable call sites in nearby code; it's rarely just a single call-site that has the problem.

Thanks!

### sh...@chromium.org (2017-11-29)

zmo: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### zm...@chromium.org (2017-11-29)

Sorry, I have multiple P1 bugs in queue. Will try to get to this as soon as I can.

### zm...@chromium.org (2017-12-06)

https://chromium-review.googlesource.com/c/chromium/src/+/811826

### bu...@chromium.org (2017-12-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3298d3abf47b3a7a10e44c07d821c68a5c8aa935

commit 3298d3abf47b3a7a10e44c07d821c68a5c8aa935
Author: Zhenyao Mo <zmo@chromium.org>
Date: Wed Dec 06 21:57:45 2017

Tighten about IntRect use in WebGL with overflow detection

BUG=784183
TEST=test case in the bug in ASAN build
R=kbr@chromium.org

Cq-Include-Trybots: master.tryserver.chromium.android:android_optional_gpu_tests_rel;master.tryserver.chromium.linux:linux_optional_gpu_tests_rel;master.tryserver.chromium.mac:mac_optional_gpu_tests_rel;master.tryserver.chromium.win:win_optional_gpu_tests_rel
Change-Id: Ie25ca328af99de7828e28e6a6e3d775f1bebc43f
Reviewed-on: https://chromium-review.googlesource.com/811826
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Commit-Queue: Zhenyao Mo <zmo@chromium.org>
Cr-Commit-Position: refs/heads/master@{#522213}
[modify] https://crrev.com/3298d3abf47b3a7a10e44c07d821c68a5c8aa935/third_party/WebKit/Source/modules/webgl/WebGLRenderingContextBase.cpp
[modify] https://crrev.com/3298d3abf47b3a7a10e44c07d821c68a5c8aa935/third_party/WebKit/Source/modules/webgl/WebGLRenderingContextBase.h
[modify] https://crrev.com/3298d3abf47b3a7a10e44c07d821c68a5c8aa935/third_party/WebKit/Source/platform/geometry/IntRect.cpp
[modify] https://crrev.com/3298d3abf47b3a7a10e44c07d821c68a5c8aa935/third_party/WebKit/Source/platform/geometry/IntRect.h


### zm...@chromium.org (2017-12-06)

I guess M-63 is too late to merge?

### cl...@chromium.org (2017-12-07)

ClusterFuzz has detected this issue as fixed in range 522195:522230.

Detailed report: https://clusterfuzz.com/testcase?key=4644978960891904

Job Type: windows_asan_chrome
Crash Type: Heap-buffer-overflow READ 16
Crash Address: 0x0f6e7400
Crash State:
  blink::Unpack<18,unsigned
  blink::FormatConverter::Convert<blink::WebGLImageConversion::DataFormat::kDataFo
  blink::WebGLImageConversion::PackPixels
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=495526:495536
Fixed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=522195:522230

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4644978960891904

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2017-12-07)

ClusterFuzz testcase 4644978960891904 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2017-12-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-07)

Your change meets the bar and is auto-approved for M64. Please go ahead and merge the CL to branch 3282 manually. Please contact milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-12-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0b9674777ea33938a4eddb1d600c030756948b6b

commit 0b9674777ea33938a4eddb1d600c030756948b6b
Author: Zhenyao Mo <zmo@chromium.org>
Date: Thu Dec 07 22:57:53 2017

Tighten about IntRect use in WebGL with overflow detection

BUG=784183
TEST=test case in the bug in ASAN build
R=​kbr@chromium.org

Cq-Include-Trybots: master.tryserver.chromium.android:android_optional_gpu_tests_rel;master.tryserver.chromium.linux:linux_optional_gpu_tests_rel;master.tryserver.chromium.mac:mac_optional_gpu_tests_rel;master.tryserver.chromium.win:win_optional_gpu_tests_rel
Change-Id: Ie25ca328af99de7828e28e6a6e3d775f1bebc43f
Reviewed-on: https://chromium-review.googlesource.com/811826
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Commit-Queue: Zhenyao Mo <zmo@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#522213}(cherry picked from commit 3298d3abf47b3a7a10e44c07d821c68a5c8aa935)
Reviewed-on: https://chromium-review.googlesource.com/815775
Reviewed-by: Zhenyao Mo <zmo@chromium.org>
Cr-Commit-Position: refs/branch-heads/3282@{#80}
Cr-Branched-From: 5fdc0fab22ce7efd32532ee989b223fa12f8171e-refs/heads/master@{#520840}
[modify] https://crrev.com/0b9674777ea33938a4eddb1d600c030756948b6b/third_party/WebKit/Source/modules/webgl/WebGLRenderingContextBase.cpp
[modify] https://crrev.com/0b9674777ea33938a4eddb1d600c030756948b6b/third_party/WebKit/Source/modules/webgl/WebGLRenderingContextBase.h
[modify] https://crrev.com/0b9674777ea33938a4eddb1d600c030756948b6b/third_party/WebKit/Source/platform/geometry/IntRect.cpp
[modify] https://crrev.com/0b9674777ea33938a4eddb1d600c030756948b6b/third_party/WebKit/Source/platform/geometry/IntRect.h


### aw...@google.com (2017-12-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-12-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-12-14)

Nice one! The VRP Panel decided to award $4,000 for this report - thanks!

### aw...@chromium.org (2017-12-14)

[Empty comment from Monorail migration]

### tk...@googlemail.com (2018-01-06)

Thanks! Please credit me as "Tobias Klein (www.trapkit.de)".

### aw...@google.com (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-05)

This issue was migrated from crbug.com/chromium/784183?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089575)*
