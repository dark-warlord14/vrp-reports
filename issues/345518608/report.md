# Pdfium Out-Of-Bounds Read in CPDF_DIB::LoadJpxBitmap

| Field | Value |
|-------|-------|
| **Issue ID** | [345518608](https://issues.chromium.org/issues/345518608) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | PDFium |
| **Platforms** | Linux, Windows |
| **Reporter** | ke...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2024-06-06 |
| **Bounty** | $7,000.00 |

## Description

The attached testcase crashes asan builds of pdfium/chrome on linux/windows:

Output of chromium-127.0.6521.0-win64-asan\pdfium\_test.exe:

```
==34504==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x12be0a234a04 at pc 0x7ff6bae2dbdc bp 0x0074deb1deb0 sp 0x0074deb1def8
READ of size 3 at 0x12be0a234a04 thread T0
==34504==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ff6bae2dbdb in __asan_memcpy C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_interceptors_memintrinsics.cpp:63
    #1 0x7ff6b7449f90 in CPDF_DIB::LoadJpxBitmap C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_dib.cpp:778
    #2 0x7ff6b74427f2 in CPDF_DIB::CreateDecoder C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_dib.cpp:529
    #3 0x7ff6b7444f56 in CPDF_DIB::StartLoadDIBBase C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_dib.cpp:311
    #4 0x7ff6b7479878 in CPDF_PageImageCache::Entry::StartGetCachedBitmap C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_pageimagecache.cpp:272
    #5 0x7ff6b7478f6c in CPDF_PageImageCache::StartGetCachedBitmap C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_pageimagecache.cpp:185
    #6 0x7ff6b746a941 in CPDF_ImageLoader::Start C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_imageloader.cpp:35
    #7 0x7ff6b74c27e2 in CPDF_ImageRenderer::StartLoadDIBBase C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\render\cpdf_imagerenderer.cpp:68
    #8 0x7ff6b74c8804 in CPDF_ImageRenderer::Start C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\render\cpdf_imagerenderer.cpp:186
    #9 0x7ff6b74de7c3 in CPDF_RenderStatus::ContinueSingleObject C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\render\cpdf_renderstatus.cpp:271
    #10 0x7ff6b74cc1e5 in CPDF_ProgressiveRenderer::Continue C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\render\cpdf_progressiverenderer.cpp:92
    #11 0x7ff6b679dd3b in `anonymous namespace'::RenderPageImpl C:\b\s\w\ir\cache\builder\src\third_party\pdfium\fpdfsdk\cpdfsdk_renderpage.cpp:84
    #12 0x7ff6b679e0ff in CPDFSDK_RenderPageWithContext C:\b\s\w\ir\cache\builder\src\third_party\pdfium\fpdfsdk\cpdfsdk_renderpage.cpp:113
    #13 0x7ff6b67b56e5 in FPDF_RenderPageBitmapWithColorScheme_Start C:\b\s\w\ir\cache\builder\src\third_party\pdfium\fpdfsdk\fpdf_progressive.cpp:69
    #14 0x7ff6b674bfec in `anonymous namespace'::ProgressiveBitmapPageRenderer::Start C:\b\s\w\ir\cache\builder\src\third_party\pdfium\testing\pdfium_test.cc:1076
    #15 0x7ff6b6743f79 in main C:\b\s\w\ir\cache\builder\src\third_party\pdfium\testing\pdfium_test.cc:2006
    #16 0x7ff6bb8422e7 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #17 0x7ffc5bc27343 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017343)
    #18 0x7ffc5c8a26b0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526b0)

0x12be0a234a04 is located 0 bytes after 82436-byte region [0x12be0a220800,0x12be0a234a04)
allocated by thread T0 here:
    #0 0x7ff6bae2c484 in calloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:114
    #1 0x7ff6b6c53222 in CFX_DIBitmap::Create C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fxge\dib\cfx_dibitmap.cpp:66
    #2 0x7ff6b6c52db9 in CFX_DIBitmap::Create C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fxge\dib\cfx_dibitmap.cpp:38
    #3 0x7ff6b7449790 in CPDF_DIB::LoadJpxBitmap C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_dib.cpp:731
    #4 0x7ff6b74427f2 in CPDF_DIB::CreateDecoder C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_dib.cpp:529
    #5 0x7ff6b7444f56 in CPDF_DIB::StartLoadDIBBase C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_dib.cpp:311
    #6 0x7ff6b7479878 in CPDF_PageImageCache::Entry::StartGetCachedBitmap C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_pageimagecache.cpp:272
    #7 0x7ff6b7478f6c in CPDF_PageImageCache::StartGetCachedBitmap C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_pageimagecache.cpp:185
    #8 0x7ff6b746a941 in CPDF_ImageLoader::Start C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_imageloader.cpp:35
    #9 0x7ff6b74c27e2 in CPDF_ImageRenderer::StartLoadDIBBase C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\render\cpdf_imagerenderer.cpp:68
    #10 0x7ff6b74c8804 in CPDF_ImageRenderer::Start C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\render\cpdf_imagerenderer.cpp:186
    #11 0x7ff6b74de7c3 in CPDF_RenderStatus::ContinueSingleObject C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\render\cpdf_renderstatus.cpp:271
    #12 0x7ff6b74cc1e5 in CPDF_ProgressiveRenderer::Continue C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\render\cpdf_progressiverenderer.cpp:92
    #13 0x7ff6b679dd3b in `anonymous namespace'::RenderPageImpl C:\b\s\w\ir\cache\builder\src\third_party\pdfium\fpdfsdk\cpdfsdk_renderpage.cpp:84
    #14 0x7ff6b679e0ff in CPDFSDK_RenderPageWithContext C:\b\s\w\ir\cache\builder\src\third_party\pdfium\fpdfsdk\cpdfsdk_renderpage.cpp:113
    #15 0x7ff6b67b56e5 in FPDF_RenderPageBitmapWithColorScheme_Start C:\b\s\w\ir\cache\builder\src\third_party\pdfium\fpdfsdk\fpdf_progressive.cpp:69
    #16 0x7ff6b674bfec in `anonymous namespace'::ProgressiveBitmapPageRenderer::Start C:\b\s\w\ir\cache\builder\src\third_party\pdfium\testing\pdfium_test.cc:1076
    #17 0x7ff6b6743f79 in main C:\b\s\w\ir\cache\builder\src\third_party\pdfium\testing\pdfium_test.cc:2006
    #18 0x7ff6bb8422e7 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #19 0x7ffc5bc27343 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017343)
    #20 0x7ffc5c8a26b0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526b0)

SUMMARY: AddressSanitizer: heap-buffer-overflow C:\b\s\w\ir\cache\builder\src\third_party\pdfium\core\fpdfapi\page\cpdf_dib.cpp:778 in CPDF_DIB::LoadJpxBitmap
Shadow bytes around the buggy address:
  0x12be0a234780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x12be0a234800: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x12be0a234880: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x12be0a234900: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x12be0a234980: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x12be0a234a00:[04]fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x12be0a234a80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x12be0a234b00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x12be0a234b80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x12be0a234c00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x12be0a234c80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==34504==ABORTING

```

Chrome Version: tested asan builds of 125, 127

Operating System: windows, linux

Attached minimized testcase

Type of crash: tab

Reporter credit: soiax

## Attachments

- [test11.pdf](attachments/test11.pdf) (application/pdf, 1.1 KB)

## Timeline

### li...@chromium.org (2024-06-07)

I noticed that there is an UNSAFE\_TODO LoadJpxBitmap so assigning to tsepez to bump up the priority of investigating this particular TODO :)

Marking this as medium severity as an OOB read, and found-in to 125 since I repro'd it up to 125 as well.

### th...@chromium.org (2024-06-07)

I tried using the Quick Upload button on <https://clusterfuzz.com/upload-testcase>, but it says "ERROR: You are not privileged to update existing issues."

### th...@chromium.org (2024-06-07)

So I'll bisect this locally and see when this started.

### cl...@appspot.gserviceaccount.com (2024-06-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5089888977223680.

### th...@chromium.org (2024-06-07)

Bisects to <https://pdfium-review.googlesource.com/104031>

### li...@chromium.org (2024-06-07)

Strange that Quick Upload didn't work for you, I did get an upload going at least. Did you use your chromium or google account?

### th...@chromium.org (2024-06-07)

re: [comment #7](https://issues.chromium.org/issues/345518608#comment7) - Chromium account.

### ti...@chromium.org (2024-06-10)

Looked into the upload issue - it's because ClusterFuzz only allows some privileged users to associate testcases with existing bugs. I think we should relax this constraint, filed [issue 346264213](https://issues.chromium.org/issues/346264213) to track that FR.

### pe...@google.com (2024-06-11)

Setting milestone because of s2 severity.

### th...@chromium.org (2024-06-11)

This CL turns the out-of-bounds read into a hard crash: <https://pdfium.googlesource.com/pdfium/+/876b8f0695e745876356f2291be27ab997597a18>

This CL will prevent the crash: <https://pdfium-review.googlesource.com/120331>

### ap...@google.com (2024-06-12)

Project: pdfium
Branch: main

commit 1135cbda250cc83d15fdf53fe5fc32674ac7079e
Author: Lei Zhang <thestig@chromium.org>
Date:   Wed Jun 12 05:08:41 2024

    Tolerate extra JPEG2000 image channels in CPDF_DIB::LoadJpxBitmap()
    
    JPEG2000 images can have more color channels than the number of color
    components. Thus checking for exactly 4 channels may be too strict. In
    the case where the `JpxDecodeAction::kConvertArgbToRgb` action is in
    use, remove the channel check when selecting the output image format.
    Instead, use CHECK_GE() to make sure the code that chose to use
    `kConvertArgbToRgb` only did that when there are 4 or more channels.
    
    Bug: 345518608
    Change-Id: I3574d82a0d74c6e50da929c6cabb2b0da7ebb208
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/120331
    Reviewed-by: Thomas Sepez <tsepez@google.com>
    Reviewed-by: Tom Sepez <tsepez@chromium.org>
    Commit-Queue: Lei Zhang <thestig@chromium.org>

M       core/fpdfapi/page/cpdf_dib.cpp

https://pdfium-review.googlesource.com/120331


### ap...@google.com (2024-06-13)

Project: chromium/src
Branch: main

commit e06752a5a007a813484b5108169c8bde7293b935
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Thu Jun 13 00:37:15 2024

    Roll PDFium from 33ece3a42388 to 51d856c2ff01 (13 revisions)
    
    https://pdfium.googlesource.com/pdfium.git/+log/33ece3a42388..51d856c2ff01
    
    2024-06-12 thestig@chromium.org Avoid another call to free resources during CPDF_Document destruction
    2024-06-12 thestig@chromium.org Restore previous transparency rendering behavior
    2024-06-12 thestig@chromium.org Roll third_party/skia/ ba0db3c0a..51eabd0d1 (249 commits; 1 trivial rolls)
    2024-06-12 thestig@chromium.org Rewrite comments in CJPX_Decoder::StartDecode()
    2024-06-12 thestig@chromium.org Tolerate extra JPEG2000 image channels in CPDF_DIB::LoadJpxBitmap()
    2024-06-12 thestig@chromium.org Use std::unique_ptr in CJPX_Decoder
    2024-06-12 tsepez@chromium.org Avoid UNSAFE_TODO() in CPDF_Bookmark.
    2024-06-11 tsepez@chromium.org Remove last usage of #pragma allow_unsafe_buffers
    2024-06-11 brkfstmnchr@gmail.com Add test for colorspace handling of regenerated streams
    2024-06-11 thestig@chromium.org Remove some UNSAFE_TODOs in CFX_DIBitmap
    2024-06-11 tsepez@chromium.org Avoid a few UNSAFE_TODO()s in CPDF_CIDFont.
    2024-06-11 tsepez@chromium.org Avoid unsafe iteration and string construction in cpdf_font.cpp
    2024-06-11 thestig@chromium.org Avoid addition calls to free resources during CPDF_Document destruction
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/pdfium-autoroll
    Please CC dhoss@chromium.org,pdfium-deps-rolls@chromium.org,thestig@chromium.org on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in PDFium: https://bugs.chromium.org/p/pdfium/issues/entry
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Bug: chromium:345518608,chromium:346598551,chromium:346606150,chromium:42271122,chromium:42271133,chromium:42271176,chromium:42271776
    Tbr: pdfium-deps-rolls@chromium.org
    Change-Id: Ide9229fce14cc1fd89720550574c7f959fa98e0d
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5628374
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1314370}

M       DEPS
M       third_party/pdfium

https://chromium-review.googlesource.com/5628374


### sp...@google.com (2024-06-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
report of memory corruption in the renderer / sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-28)

Congratulations soiax! Thank you for your efforts and reporting this issue to us -- nice work! 

### pe...@google.com (2024-09-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/345518608)*
