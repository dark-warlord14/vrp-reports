# Security: PDFium OOB Read in BMPDecompressor::ReadHeader

| Field | Value |
|-------|-------|
| **Issue ID** | [40090364](https://issues.chromium.org/issues/40090364) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | rh...@chromium.org |
| **Created** | 2018-02-02 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached pdf file could crash PDFium when XFA and ASAN was enabled on Windows.

```
is_asan = true  
pdf_enable_xfa = true  
pdf_enable_v8 = true  

```

The following error log was produced by AddressSanitizer.

```
=================================================================  
==8184==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x07b0d881 at pc 0x03132463 bp 0x0031cc58 sp 0x0031cc4c  
READ of size 1 at 0x07b0d881 thread T0  
==8184==\*\*\* WARNING: Failed to initialize DbgHelp!              \*\*\*  
==8184==\*\*\* Most likely this means that the app is already      \*\*\*  
==8184==\*\*\* using DbgHelp, possibly with incompatible flags.    \*\*\*  
==8184==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  
==8184==\*\*\* or produce wrong results.                           \*\*\*  
    #0 0x3132462 in BMPDecompressor::ReadHeader C:\pdfium\core\fxcodec\lbmp\fx_bmp.cpp:101  
    #1 0x3122ef2 in CCodec_BmpModule::ReadHeader C:\pdfium\core\fxcodec\codec\ccodec_bmpmodule.cpp:46  
    #2 0x3bcc0e5 in CCodec_ProgressiveDecoder::BmpDetectImageType C:\pdfium\core\fxcodec\codec\fx_codec_progress.cpp:1043  
    #3 0x3bcbc1b in CCodec_ProgressiveDecoder::DetectImageType C:\pdfium\core\fxcodec\codec\fx_codec_progress.cpp:1006  
    #4 0x3bcf590 in CCodec_ProgressiveDecoder::LoadImageInfo C:\pdfium\core\fxcodec\codec\fx_codec_progress.cpp:1303  
    #5 0x38b5bbc in XFA_LoadImageFromBuffer C:\pdfium\xfa\fxfa\cxfa_ffwidget.cpp:159  
    #6 0x394895a in `anonymous namespace'::XFA_LoadImageData C:\pdfium\xfa\fxfa\parser\cxfa_node.cpp:226  
    #7 0x392cdf6 in CXFA_Node::LoadImageImage C:\pdfium\xfa\fxfa\parser\cxfa_node.cpp:3002  
    #8 0x38d866d in CXFA_FFImage::LoadWidget C:\pdfium\xfa\fxfa\cxfa_ffimage.cpp:32  
    #9 0x38a122e in CXFA_FFPageWidgetIterator::GetWidget C:\pdfium\xfa\fxfa\cxfa_ffpageview.cpp:214  
    #10 0x38a152d in CXFA_FFPageWidgetIterator::MoveToNext C:\pdfium\xfa\fxfa\cxfa_ffpageview.cpp:177  
    #11 0x2e4cedc in CPDFSDK_PageView::LoadFXAnnots C:\pdfium\fpdfsdk\cpdfsdk_pageview.cpp:439  
    #12 0x2e3db97 in CPDFSDK_FormFillEnvironment::GetPageView C:\pdfium\fpdfsdk\cpdfsdk_formfillenvironment.cpp:562  
    #13 0x2e2fa97 in `anonymous namespace'::FormHandleToPageView C:\pdfium\fpdfsdk\fpdfformfill.cpp:120  
    #14 0x2e30c16 in FORM_OnAfterLoadPage C:\pdfium\fpdfsdk\fpdfformfill.cpp:746  
    #15 0x12b16ed in `anonymous namespace'::GetPageForIndex C:\pdfium\samples\pdfium_test.cc:995  
    #16 0x12b1aec in `anonymous namespace'::RenderPage C:\pdfium\samples\pdfium_test.cc:1234  
    #17 0x1294907 in main C:\pdfium\samples\pdfium_test.cc:1630  
    #18 0x3e787aa in __scrt_common_main_seh f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl:283  
    #19 0x75ad3369 in BaseThreadInitThunk+0x11 (C:\Windows\syswow64\kernel32.dll+0x7dd73369)  
    #20 0x774898f1 in RtlInitializeExceptionChain+0x62 (C:\Windows\SysWOW64\ntdll.dll+0x7dea98f1)  
    #21 0x774898c4 in RtlInitializeExceptionChain+0x35 (C:\Windows\SysWOW64\ntdll.dll+0x7dea98c4)  
  
0x07b0d881 is located 3 bytes to the right of 14-byte region [0x07b0d870,0x07b0d87e)  
allocated by thread T0 here:  
    #0 0x3e654ac in malloc c:\b\rr\tmp8oruyi\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_malloc_win.cc:60  
    #1 0x3bcbba9 in CCodec_ProgressiveDecoder::DetectImageType C:\pdfium\core\fxcodec\codec\fx_codec_progress.cpp:1000  
    #2 0x3bcf590 in CCodec_ProgressiveDecoder::LoadImageInfo C:\pdfium\core\fxcodec\codec\fx_codec_progress.cpp:1303  
    #3 0x38b5bbc in XFA_LoadImageFromBuffer C:\pdfium\xfa\fxfa\cxfa_ffwidget.cpp:159  
    #4 0x394895a in `anonymous namespace'::XFA_LoadImageData C:\pdfium\xfa\fxfa\parser\cxfa_node.cpp:226  
    #5 0x392cdf6 in CXFA_Node::LoadImageImage C:\pdfium\xfa\fxfa\parser\cxfa_node.cpp:3002  
    #6 0x38d866d in CXFA_FFImage::LoadWidget C:\pdfium\xfa\fxfa\cxfa_ffimage.cpp:32  
    #7 0x38a122e in CXFA_FFPageWidgetIterator::GetWidget C:\pdfium\xfa\fxfa\cxfa_ffpageview.cpp:214  
    #8 0x38a152d in CXFA_FFPageWidgetIterator::MoveToNext C:\pdfium\xfa\fxfa\cxfa_ffpageview.cpp:177  
    #9 0x2e4cedc in CPDFSDK_PageView::LoadFXAnnots C:\pdfium\fpdfsdk\cpdfsdk_pageview.cpp:439  
    #10 0x2e3db97 in CPDFSDK_FormFillEnvironment::GetPageView C:\pdfium\fpdfsdk\cpdfsdk_formfillenvironment.cpp:562  
    #11 0x2e2fa97 in `anonymous namespace'::FormHandleToPageView C:\pdfium\fpdfsdk\fpdfformfill.cpp:120  
    #12 0x2e30c16 in FORM_OnAfterLoadPage C:\pdfium\fpdfsdk\fpdfformfill.cpp:746  
    #13 0x12b16ed in `anonymous namespace'::GetPageForIndex C:\pdfium\samples\pdfium_test.cc:995  
    #14 0x12b1aec in `anonymous namespace'::RenderPage C:\pdfium\samples\pdfium_test.cc:1234  
    #15 0x1294907 in main C:\pdfium\samples\pdfium_test.cc:1630  
    #16 0x3e787aa in __scrt_common_main_seh f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl:283  
    #17 0x75ad3369 in BaseThreadInitThunk+0x11 (C:\Windows\syswow64\kernel32.dll+0x7dd73369)  
    #18 0x774898f1 in RtlInitializeExceptionChain+0x62 (C:\Windows\SysWOW64\ntdll.dll+0x7dea98f1)  
    #19 0x774898c4 in RtlInitializeExceptionChain+0x35 (C:\Windows\SysWOW64\ntdll.dll+0x7dea98c4)  
  
SUMMARY: AddressSanitizer: heap-buffer-overflow C:\pdfium\core\fxcodec\lbmp\fx_bmp.cpp:101 in BMPDecompressor::ReadHeader  
Shadow bytes around the buggy address:  
  0x30f61ac0: fa fa fd fd fa fa fd fa fa fa fd fa fa fa fd fa  
  0x30f61ad0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa  
  0x30f61ae0: fa fa fd fd fa fa fd fa fa fa fd fa fa fa fd fd  
  0x30f61af0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa  
  0x30f61b00: fa fa fd fa fa fa fd fa fa fa fd fa fa fa 00 06  
=>0x30f61b10:[fa]fa 04 fa fa fa fd fd fa fa fd fd fa fa fd fa  
  0x30f61b20: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa  
  0x30f61b30: fa fa fd fd fa fa fd fa fa fa fd fa fa fa fd fa  
  0x30f61b40: fa fa fd fa fa fa fd fa fa fa fd fd fa fa fd fd  
  0x30f61b50: fa fa fd fa fa fa fd fd fa fa fd fd fa fa fd fd  
  0x30f61b60: fa fa fd fd fa fa fd fd fa fa fd fa fa fa fd fd  
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
==8184==ABORTING  

```

**VERSION**  

Chrome Version: PDFium with JS / XFA / ASAN enabled.  

Operating System: Windows

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug.**

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### el...@chromium.org (2018-02-02)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### rh...@chromium.org (2018-02-02)

[Empty comment from Monorail migration]

### rh...@chromium.org (2018-02-02)

[Empty comment from Monorail migration]

### pa...@chromium.org (2018-02-02)

[Empty comment from Monorail migration]

### rh...@chromium.org (2018-02-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-02-06)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/980beeb5b06facc5bf178c03394ad9487b9b4b69

commit 980beeb5b06facc5bf178c03394ad9487b9b4b69
Author: Ryan Harrison <rharrison@chromium.org>
Date: Tue Feb 06 14:41:14 2018

Changing the member naming style in BMPDecompressor

Currently there is no indication in the name of it being a member
variable and the capitalization is inconsistent. This CL brings them
all into line with Chromium style.

BUG=chromium:808336

Change-Id: Iaed0272b69350f316371a67eb513934a0169f451
Reviewed-on: https://pdfium-review.googlesource.com/25430
Reviewed-by: Henrique Nakashima <hnakashima@chromium.org>
Commit-Queue: Ryan Harrison <rharrison@chromium.org>

[modify] https://crrev.com/980beeb5b06facc5bf178c03394ad9487b9b4b69/core/fxcodec/lbmp/fx_bmp.cpp
[modify] https://crrev.com/980beeb5b06facc5bf178c03394ad9487b9b4b69/core/fxcodec/lbmp/fx_bmp.h
[modify] https://crrev.com/980beeb5b06facc5bf178c03394ad9487b9b4b69/core/fxcodec/codec/ccodec_bmpmodule.cpp


### bu...@chromium.org (2018-02-06)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/b105152222f9dfb387efa6a70dedf3dd0ceb2cd5

commit b105152222f9dfb387efa6a70dedf3dd0ceb2cd5
Author: Ryan Harrison <rharrison@chromium.org>
Date: Tue Feb 06 15:31:04 2018

Move core/fxcodec/lbmp/ -> core/fxcodec/bmp/

BUG=chromium:808336

Change-Id: Id721787dd77d1bcac6daf6e3c149f79e8d1d9fe4
Reviewed-on: https://pdfium-review.googlesource.com/25610
Reviewed-by: dsinclair <dsinclair@chromium.org>
Commit-Queue: Ryan Harrison <rharrison@chromium.org>

[modify] https://crrev.com/b105152222f9dfb387efa6a70dedf3dd0ceb2cd5/BUILD.gn
[rename] https://crrev.com/b105152222f9dfb387efa6a70dedf3dd0ceb2cd5/core/fxcodec/bmp/fx_bmp.h
[rename] https://crrev.com/b105152222f9dfb387efa6a70dedf3dd0ceb2cd5/core/fxcodec/bmp/fx_bmp.cpp
[modify] https://crrev.com/b105152222f9dfb387efa6a70dedf3dd0ceb2cd5/core/fxcodec/gif/cfx_lzwdecompressor.cpp
[modify] https://crrev.com/b105152222f9dfb387efa6a70dedf3dd0ceb2cd5/core/fxcodec/codec/ccodec_bmpmodule.cpp


### bu...@chromium.org (2018-02-06)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/41441c9da88210376a87c4d03d71232b390b7cee

commit 41441c9da88210376a87c4d03d71232b390b7cee
Author: Ryan Harrison <rharrison@chromium.org>
Date: Tue Feb 06 16:53:14 2018

Convert BMP class name style to match other codecs

BMPDecompressor -> CFX_BmpDecompressor
CBmpContext -> CFX_BmpContext

BUG=chromium:808336

Change-Id: If8ef5294171e3619ae1d7c5175ddf23b7673ec78
Reviewed-on: https://pdfium-review.googlesource.com/25611
Reviewed-by: Henrique Nakashima <hnakashima@chromium.org>
Commit-Queue: Ryan Harrison <rharrison@chromium.org>

[modify] https://crrev.com/41441c9da88210376a87c4d03d71232b390b7cee/core/fxcodec/bmp/fx_bmp.h
[modify] https://crrev.com/41441c9da88210376a87c4d03d71232b390b7cee/core/fxcodec/bmp/fx_bmp.cpp
[modify] https://crrev.com/41441c9da88210376a87c4d03d71232b390b7cee/core/fxcodec/codec/ccodec_bmpmodule.cpp


### bu...@chromium.org (2018-02-06)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/b5a2d14e21c0f149be49e06141549b185a5c7993

commit b5a2d14e21c0f149be49e06141549b185a5c7993
Author: Ryan Harrison <rharrison@chromium.org>
Date: Tue Feb 06 16:55:14 2018

Extract classes in fx_bmp.h into their own files

BUG=chromium:808336

Change-Id: I3201805a374b5403149eca701714ef4369a2e337
Reviewed-on: https://pdfium-review.googlesource.com/25630
Reviewed-by: Henrique Nakashima <hnakashima@chromium.org>
Commit-Queue: Ryan Harrison <rharrison@chromium.org>

[add] https://crrev.com/b5a2d14e21c0f149be49e06141549b185a5c7993/core/fxcodec/bmp/cfx_bmpdecompressor.h
[add] https://crrev.com/b5a2d14e21c0f149be49e06141549b185a5c7993/core/fxcodec/bmp/cfx_bmpcontext.cpp
[modify] https://crrev.com/b5a2d14e21c0f149be49e06141549b185a5c7993/core/fxcodec/codec/ccodec_bmpmodule.cpp
[modify] https://crrev.com/b5a2d14e21c0f149be49e06141549b185a5c7993/core/fxcodec/bmp/fx_bmp.h
[add] https://crrev.com/b5a2d14e21c0f149be49e06141549b185a5c7993/core/fxcodec/bmp/cfx_bmpdecompressor.cpp
[modify] https://crrev.com/b5a2d14e21c0f149be49e06141549b185a5c7993/BUILD.gn
[add] https://crrev.com/b5a2d14e21c0f149be49e06141549b185a5c7993/core/fxcodec/bmp/cfx_bmpcontext.h
[modify] https://crrev.com/b5a2d14e21c0f149be49e06141549b185a5c7993/core/fxcodec/bmp/fx_bmp.cpp


### bu...@chromium.org (2018-02-06)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/cdaf802ceafcfb2e547ffe96729445c0f1c6154a

commit cdaf802ceafcfb2e547ffe96729445c0f1c6154a
Author: Ryan Harrison <rharrison@chromium.org>
Date: Tue Feb 06 16:58:55 2018

Account for skip size before getting image ifh size

BUG=chromium:808336

Change-Id: I84443a00e2ebaf0a1e8590464486ec92bcb0e3b5
Reviewed-on: https://pdfium-review.googlesource.com/25690
Reviewed-by: Henrique Nakashima <hnakashima@chromium.org>
Commit-Queue: Ryan Harrison <rharrison@chromium.org>

[modify] https://crrev.com/cdaf802ceafcfb2e547ffe96729445c0f1c6154a/core/fxcodec/bmp/cfx_bmpdecompressor.cpp


### rh...@chromium.org (2018-02-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-02-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/05e1f89eef2295c0db4bec845ff32b76f2df06a6

commit 05e1f89eef2295c0db4bec845ff32b76f2df06a6
Author: pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Wed Feb 07 18:13:38 2018

Roll src/third_party/pdfium/ 1ea9f3f92..b3a3eaab0 (27 commits)

https://pdfium.googlesource.com/pdfium.git/+log/1ea9f3f92f25..b3a3eaab0471

$ git log 1ea9f3f92..b3a3eaab0 --date=short --no-merges --format='%ad %ae %s'
2018-02-07 dsinclair Revert "[v8-platform] Store the platform in a unique_ptr"
2018-02-07 thestig More GetPageNumbers() clean up in fpdf_ppo.cpp.
2018-02-06 xlou Change MakeXObject to update reference from the root of the source page.
2018-02-06 rharrison Use temporary iterator to avoid potential OOB
2018-02-06 hnakashima Fix caret not appearing in XFA Edits.
2018-02-06 tsepez Avoid needless malloc for v8:Global array.
2018-02-06 tsepez Remove unused FreeObjectPrivate() overload.
2018-02-06 reed IWYU
2018-02-06 dsinclair Make the CXFA_Node parent pointer Unowned
2018-02-06 rharrison Break unneeded dep on Bmp codec in Gif codec
2018-02-06 rharrison Account for skip size before getting image ifh size
2018-02-06 rharrison Extract classes in fx_bmp.h into their own files
2018-02-06 rharrison Convert BMP class name style to match other codecs
2018-02-06 rharrison Move core/fxcodec/lbmp/ -> core/fxcodec/bmp/
2018-02-06 rharrison Changing the member naming style in BMPDecompressor
2018-02-06 thestig Fix an infinite recursion in pdfium_test.
2018-02-06 xlou Add rendering embeddertests for FPDF_ImportNPagesToOne.
2018-02-05 hnakashima Limit dest buffer to 1GB in FlateOrLZWDecode.
2018-02-05 dsinclair Fold CJS_EmbedObj classes into CJS_Object classes
2018-02-05 dsinclair Remove the CJS_EmbedObj template param from JSConstructor.
2018-02-05 thestig Make EmbedderTest class member style consistent.
2018-02-05 thestig Fix testing.cpp build with v8_use_external_startup_data=false.
2018-02-05 tsepez Use unique pointer in CFXJS_PerObjectData.
2018-02-05 thestig Fix some formcalc constant naming.
2018-02-05 ahaas [v8-platform] Store the platform in a unique_ptr
2018-02-05 thestig Add FPDFAnnotationDeleter for use with std::unique_ptr.
2018-02-05 dsinclair [XFA] dot_accessor may not provide a valid object.

Created with:
  roll-dep src/third_party/pdfium
BUG=648177,808336,808336,808336,808336,808336,808898,808269


The AutoRoll server is located here: https://pdfium-roll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.


TBR=dsinclair@chromium.org

Change-Id: I1ce04168b70e67d18145e08378a12f571727c4f9
Reviewed-on: https://chromium-review.googlesource.com/906916
Commit-Queue: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Reviewed-by: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#535062}
[modify] https://crrev.com/05e1f89eef2295c0db4bec845ff32b76f2df06a6/DEPS


### sh...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-05-04)

And $1,000 for this one...

### aw...@chromium.org (2018-05-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-05-16)

This issue was migrated from crbug.com/chromium/808336?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/62400]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090364)*
