# Security: PDFium OOB Read in CFX_BmpDecompressor::ReadHeader

| Field | Value |
|-------|-------|
| **Issue ID** | [40090419](https://issues.chromium.org/issues/40090419) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Reporter** | st...@gmail.com |
| **Assignee** | rh...@chromium.org |
| **Created** | 2018-02-07 |
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
==11204==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x07947489 at pc 0x03251e14 bp 0x002fc7f8 sp 0x002fc7ec  
READ of size 1 at 0x07947489 thread T0  
==11204==\*\*\* WARNING: Failed to initialize DbgHelp!              \*\*\*  
==11204==\*\*\* Most likely this means that the app is already      \*\*\*  
==11204==\*\*\* using DbgHelp, possibly with incompatible flags.    \*\*\*  
==11204==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  
==11204==\*\*\* or produce wrong results.                           \*\*\*  
    #0 0x3251e13 in CFX_BmpDecompressor::ReadHeader C:\pdfium\core\fxcodec\bmp\cfx_bmpdecompressor.cpp:159  
    #1 0x3241f82 in CCodec_BmpModule::ReadHeader C:\pdfium\core\fxcodec\codec\ccodec_bmpmodule.cpp:39  
    #2 0x3ce8df5 in CCodec_ProgressiveDecoder::BmpDetectImageType C:\pdfium\core\fxcodec\codec\fx_codec_progress.cpp:1043  
    #3 0x3ce892b in CCodec_ProgressiveDecoder::DetectImageType C:\pdfium\core\fxcodec\codec\fx_codec_progress.cpp:1006  
    #4 0x3cec2a0 in CCodec_ProgressiveDecoder::LoadImageInfo C:\pdfium\core\fxcodec\codec\fx_codec_progress.cpp:1303  
    #5 0x39d249c in XFA_LoadImageFromBuffer C:\pdfium\xfa\fxfa\cxfa_ffwidget.cpp:159  
    #6 0x3a6546a in `anonymous namespace'::XFA_LoadImageData C:\pdfium\xfa\fxfa\parser\cxfa_node.cpp:226  
    #7 0x3a498f6 in CXFA_Node::LoadImageImage C:\pdfium\xfa\fxfa\parser\cxfa_node.cpp:3000  
    #8 0x39f4f7d in CXFA_FFImage::LoadWidget C:\pdfium\xfa\fxfa\cxfa_ffimage.cpp:32  
    #9 0x39bdc5e in CXFA_FFPageWidgetIterator::GetWidget C:\pdfium\xfa\fxfa\cxfa_ffpageview.cpp:214  
    #10 0x39bdf5d in CXFA_FFPageWidgetIterator::MoveToNext C:\pdfium\xfa\fxfa\cxfa_ffpageview.cpp:177  
    #11 0x2f6d0ac in CPDFSDK_PageView::LoadFXAnnots C:\pdfium\fpdfsdk\cpdfsdk_pageview.cpp:439  
    #12 0x2f5da67 in CPDFSDK_FormFillEnvironment::GetPageView C:\pdfium\fpdfsdk\cpdfsdk_formfillenvironment.cpp:562  
    #13 0x2f4fd57 in `anonymous namespace'::FormHandleToPageView C:\pdfium\fpdfsdk\fpdfformfill.cpp:120  
    #14 0x2f50ed6 in FORM_OnAfterLoadPage C:\pdfium\fpdfsdk\fpdfformfill.cpp:746  
    #15 0x13d17d6 in `anonymous namespace'::GetPageForIndex C:\pdfium\samples\pdfium_test.cc:999  
    #16 0x13d1c2c in `anonymous namespace'::RenderPage C:\pdfium\samples\pdfium_test.cc:1237  
    #17 0x13b491f in main C:\pdfium\samples\pdfium_test.cc:1633  
    #18 0x3f974fa in __scrt_common_main_seh f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl:283  
    #19 0x75ad3369 in BaseThreadInitThunk+0x11 (C:\Windows\syswow64\kernel32.dll+0x7dd73369)  
    #20 0x774898f1 in RtlInitializeExceptionChain+0x62 (C:\Windows\SysWOW64\ntdll.dll+0x7dea98f1)  
    #21 0x774898c4 in RtlInitializeExceptionChain+0x35 (C:\Windows\SysWOW64\ntdll.dll+0x7dea98c4)  
  
0x07947489 is located 3 bytes to the right of 22-byte region [0x07947470,0x07947486)  
allocated by thread T0 here:  
    #0 0x3f842bc in malloc c:\b\rr\tmp8oruyi\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_malloc_win.cc:60  
    #1 0x3ce88b9 in CCodec_ProgressiveDecoder::DetectImageType C:\pdfium\core\fxcodec\codec\fx_codec_progress.cpp:1000  
    #2 0x3cec2a0 in CCodec_ProgressiveDecoder::LoadImageInfo C:\pdfium\core\fxcodec\codec\fx_codec_progress.cpp:1303  
    #3 0x39d249c in XFA_LoadImageFromBuffer C:\pdfium\xfa\fxfa\cxfa_ffwidget.cpp:159  
    #4 0x3a6546a in `anonymous namespace'::XFA_LoadImageData C:\pdfium\xfa\fxfa\parser\cxfa_node.cpp:226  
    #5 0x3a498f6 in CXFA_Node::LoadImageImage C:\pdfium\xfa\fxfa\parser\cxfa_node.cpp:3000  
    #6 0x39f4f7d in CXFA_FFImage::LoadWidget C:\pdfium\xfa\fxfa\cxfa_ffimage.cpp:32  
    #7 0x39bdc5e in CXFA_FFPageWidgetIterator::GetWidget C:\pdfium\xfa\fxfa\cxfa_ffpageview.cpp:214  
    #8 0x39bdf5d in CXFA_FFPageWidgetIterator::MoveToNext C:\pdfium\xfa\fxfa\cxfa_ffpageview.cpp:177  
    #9 0x2f6d0ac in CPDFSDK_PageView::LoadFXAnnots C:\pdfium\fpdfsdk\cpdfsdk_pageview.cpp:439  
    #10 0x2f5da67 in CPDFSDK_FormFillEnvironment::GetPageView C:\pdfium\fpdfsdk\cpdfsdk_formfillenvironment.cpp:562  
    #11 0x2f4fd57 in `anonymous namespace'::FormHandleToPageView C:\pdfium\fpdfsdk\fpdfformfill.cpp:120  
    #12 0x2f50ed6 in FORM_OnAfterLoadPage C:\pdfium\fpdfsdk\fpdfformfill.cpp:746  
    #13 0x13d17d6 in `anonymous namespace'::GetPageForIndex C:\pdfium\samples\pdfium_test.cc:999  
    #14 0x13d1c2c in `anonymous namespace'::RenderPage C:\pdfium\samples\pdfium_test.cc:1237  
    #15 0x13b491f in main C:\pdfium\samples\pdfium_test.cc:1633  
    #16 0x3f974fa in __scrt_common_main_seh f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl:283  
    #17 0x75ad3369 in BaseThreadInitThunk+0x11 (C:\Windows\syswow64\kernel32.dll+0x7dd73369)  
    #18 0x774898f1 in RtlInitializeExceptionChain+0x62 (C:\Windows\SysWOW64\ntdll.dll+0x7dea98f1)  
    #19 0x774898c4 in RtlInitializeExceptionChain+0x35 (C:\Windows\SysWOW64\ntdll.dll+0x7dea98c4)  
  
SUMMARY: AddressSanitizer: heap-buffer-overflow C:\pdfium\core\fxcodec\bmp\cfx_bmpdecompressor.cpp:159 in CFX_BmpDecompressor::ReadHeader  
Shadow bytes around the buggy address:  
  0x30f28e40: 00 00 00 00 fa fa fd fd fd fa fa fa 00 00 00 fa  
  0x30f28e50: fa fa 00 00 00 fa fa fa 00 00 00 fa fa fa 00 00  
  0x30f28e60: 00 00 fa fa 00 00 00 fa fa fa fd fd fd fa fa fa  
  0x30f28e70: fd fd fd fa fa fa fd fd fd fa fa fa fd fd fd fa  
  0x30f28e80: fa fa fd fd fd fd fa fa 00 00 00 04 fa fa 00 00  
=>0x30f28e90: 06[fa]fa fa 00 00 00 fa fa fa 00 00 00 00 fa fa  
  0x30f28ea0: fd fd fd fd fa fa fd fd fd fa fa fa fd fd fd fd  
  0x30f28eb0: fa fa fd fd fd fd fa fa 00 00 00 04 fa fa 00 00  
  0x30f28ec0: 00 fa fa fa 00 00 04 fa fa fa 00 00 00 fa fa fa  
  0x30f28ed0: 00 00 00 fa fa fa 00 00 00 fa fa fa fd fd fd fa  
  0x30f28ee0: fa fa fd fd fd fa fa fa fd fd fd fa fa fa fd fd  
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
==11204==ABORTING  

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

### el...@chromium.org (2018-02-07)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### rh...@chromium.org (2018-02-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-02-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6400190546968576.

### in...@chromium.org (2018-02-07)

Can't reproduce this on Linux + XFA.

### rh...@chromium.org (2018-02-07)

I was able to reproduce, requires using a local PDFium checkout at HEAD, not the rolled version in Chromium. The roller for PDFium is/was blocked i, so Chromium's third_party is lagging behind.

In future, please mention if you are using a custom PDFium or other third_party repo, when reporting bugs, since it can be critical to reproduction.

### rh...@chromium.org (2018-02-07)

[Empty comment from Monorail migration]

### rh...@chromium.org (2018-02-07)

[Empty comment from Monorail migration]

### rh...@chromium.org (2018-02-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-02-07)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/6c67da092ce8bb384f60e2eae32e18b7283ae76e

commit 6c67da092ce8bb384f60e2eae32e18b7283ae76e
Author: Ryan Harrison <rharrison@chromium.org>
Date: Wed Feb 07 20:00:25 2018

Check that request sizes in ReadData don't overflow

When a very large, bogus value, was being passed in for the number of
bytes to read, this could cause an overflow in the check for if there
is data available.

BUG=chromium:809824

Change-Id: I54af6655b61d39275f3ae6fabb27be2bee3fef05
Reviewed-on: https://pdfium-review.googlesource.com/25871
Reviewed-by: dsinclair <dsinclair@chromium.org>
Commit-Queue: Ryan Harrison <rharrison@chromium.org>

[modify] https://crrev.com/6c67da092ce8bb384f60e2eae32e18b7283ae76e/core/fxcodec/bmp/cfx_bmpdecompressor.cpp


### rh...@chromium.org (2018-02-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-02-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/33c1bd5695eb68439d02ef3dc3452fca4661e082

commit 33c1bd5695eb68439d02ef3dc3452fca4661e082
Author: pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Thu Feb 08 00:14:51 2018

Roll src/third_party/pdfium/ c0c32b0a3..9ad9a5fc8 (6 commits)

https://pdfium.googlesource.com/pdfium.git/+log/c0c32b0a3af1..9ad9a5fc81a3

$ git log c0c32b0a3..9ad9a5fc8 --date=short --no-merges --format='%ad %ae %s'
2018-02-07 tsepez Split creation of ordinary object and bound objects in FXJS.
2018-02-07 rharrison Handle removed fonts correctly in GetFontByCodePage
2018-02-07 thestig Clean up RenderPage methods in EmbedderTest.
2018-02-07 hnakashima Restore assert when GetCharacterInfo is called on an empty edit.
2018-02-07 rharrison Check that request sizes in ReadData don't overflow
2018-02-07 thestig Make xfa_fxfa_parser target jumbo capable.

Created with:
  roll-dep src/third_party/pdfium
BUG=648177,809824


The AutoRoll server is located here: https://pdfium-roll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.


TBR=dsinclair@chromium.org

Change-Id: Icd0571cf6c8cacdf3bd65491e9bcb434ad44ff3d
Reviewed-on: https://chromium-review.googlesource.com/907325
Commit-Queue: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Reviewed-by: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#535206}
[modify] https://crrev.com/33c1bd5695eb68439d02ef3dc3452fca4661e082/DEPS


### sh...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-05-04)

and this one :-)

### aw...@chromium.org (2018-05-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-05-17)

This issue was migrated from crbug.com/chromium/809824?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/62400]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090419)*
