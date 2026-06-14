# Security: PDFium UAF in CXFA_Document::DoProtoMerge

| Field | Value |
|-------|-------|
| **Issue ID** | [40090361](https://issues.chromium.org/issues/40090361) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | rh...@chromium.org |
| **Created** | 2018-02-02 |
| **Bounty** | $3,000.00 |

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
==7932==ERROR: AddressSanitizer: heap-use-after-free on address 0x0c11b58c at pc 0x03a8242d bp 0x0040dd5c sp 0x0040dd50  
READ of size 1 at 0x0c11b58c thread T0  
==7932==\*\*\* WARNING: Failed to initialize DbgHelp!              \*\*\*  
==7932==\*\*\* Most likely this means that the app is already      \*\*\*  
==7932==\*\*\* using DbgHelp, possibly with incompatible flags.    \*\*\*  
==7932==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  
==7932==\*\*\* or produce wrong results.                           \*\*\*  
    #0 0x3a8242c in CXFA_Document::DoProtoMerge C:\pdfium\xfa\fxfa\parser\cxfa_document.cpp:368  
    #1 0x39dba35 in CXFA_FFDocView::StartLayout C:\pdfium\xfa\fxfa\cxfa_ffdocview.cpp:70  
    #2 0x3987815 in CPDFXFA_Context::LoadXFADoc C:\pdfium\fpdfsdk\fpdfxfa\cpdfxfa_context.cpp:115  
    #3 0x2f5464e in FPDF_LoadXFA C:\pdfium\fpdfsdk\fpdfview.cpp:599  
    #4 0x13c475e in main C:\pdfium\samples\pdfium_test.cc:1630  
    #5 0x3fa87aa in __scrt_common_main_seh f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl:283  
    #6 0x75ad3369 in BaseThreadInitThunk+0x11 (C:\Windows\syswow64\kernel32.dll+0x7dd73369)  
    #7 0x774898f1 in RtlInitializeExceptionChain+0x62 (C:\Windows\SysWOW64\ntdll.dll+0x7dea98f1)  
    #8 0x774898c4 in RtlInitializeExceptionChain+0x35 (C:\Windows\SysWOW64\ntdll.dll+0x7dea98c4)  
  
0x0c11b58c is located 12 bytes inside of 104-byte region [0x0c11b580,0x0c11b5e8)  
freed by thread T0 here:  
    #0 0x3f953c8 in free c:\b\rr\tmp8oruyi\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_malloc_win.cc:44  
    #1 0x2fcea60 in fxcrt::ByteString::~ByteString C:\pdfium\core\fxcrt\bytestring.cpp:221  
    #2 0x3a8172d in CXFA_Document::DoProtoMerge C:\pdfium\xfa\fxfa\parser\cxfa_document.cpp:426  
    #3 0x39dba35 in CXFA_FFDocView::StartLayout C:\pdfium\xfa\fxfa\cxfa_ffdocview.cpp:70  
    #4 0x3987815 in CPDFXFA_Context::LoadXFADoc C:\pdfium\fpdfsdk\fpdfxfa\cpdfxfa_context.cpp:115  
    #5 0x2f5464e in FPDF_LoadXFA C:\pdfium\fpdfsdk\fpdfview.cpp:599  
    #6 0x13c475e in main C:\pdfium\samples\pdfium_test.cc:1630  
    #7 0x3fa87aa in __scrt_common_main_seh f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl:283  
    #8 0x75ad3369 in BaseThreadInitThunk+0x11 (C:\Windows\syswow64\kernel32.dll+0x7dd73369)  
    #9 0x774898f1 in RtlInitializeExceptionChain+0x62 (C:\Windows\SysWOW64\ntdll.dll+0x7dea98f1)  
    #10 0x774898c4 in RtlInitializeExceptionChain+0x35 (C:\Windows\SysWOW64\ntdll.dll+0x7dea98c4)  
  
previously allocated by thread T0 here:  
    #0 0x3f954ac in malloc c:\b\rr\tmp8oruyi\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_malloc_win.cc:60  
    #1 0x2fc80e8 in fxcrt::StringDataTemplate<wchar_t>::Create C:\pdfium\core\fxcrt\string_data_template.h:19  
    #2 0x2fc8216 in fxcrt::WideString::WideString C:\pdfium\core\fxcrt\widestring.cpp:377  
    #3 0x3db970e in CJX_Object::TryCData C:\pdfium\fxjs\xfa\cjx_object.cpp:588  
    #4 0x3dbbb94 in CJX_Object::GetCData C:\pdfium\fxjs\xfa\cjx_object.cpp:446  
    #5 0x3a80cb3 in CXFA_Document::DoProtoMerge C:\pdfium\xfa\fxfa\parser\cxfa_document.cpp:394  
    #6 0x39dba35 in CXFA_FFDocView::StartLayout C:\pdfium\xfa\fxfa\cxfa_ffdocview.cpp:70  
    #7 0x3987815 in CPDFXFA_Context::LoadXFADoc C:\pdfium\fpdfsdk\fpdfxfa\cpdfxfa_context.cpp:115  
    #8 0x2f5464e in FPDF_LoadXFA C:\pdfium\fpdfsdk\fpdfview.cpp:599  
    #9 0x13c475e in main C:\pdfium\samples\pdfium_test.cc:1630  
    #10 0x3fa87aa in __scrt_common_main_seh f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl:283  
    #11 0x75ad3369 in BaseThreadInitThunk+0x11 (C:\Windows\syswow64\kernel32.dll+0x7dd73369)  
    #12 0x774898f1 in RtlInitializeExceptionChain+0x62 (C:\Windows\SysWOW64\ntdll.dll+0x7dea98f1)  
    #13 0x774898c4 in RtlInitializeExceptionChain+0x35 (C:\Windows\SysWOW64\ntdll.dll+0x7dea98c4)  
  
SUMMARY: AddressSanitizer: heap-use-after-free C:\pdfium\xfa\fxfa\parser\cxfa_document.cpp:368 in CXFA_Document::DoProtoMerge  
Shadow bytes around the buggy address:  
  0x31823660: fd fd fd fd fd fd fa fa fa fa fa fa fa fa fd fd  
  0x31823670: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa  
  0x31823680: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  
  0x31823690: fd fa fa fa fa fa fa fa fa fa fd fd fd fd fd fd  
  0x318236a0: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa  
=>0x318236b0: fd[fd]fd fd fd fd fd fd fd fd fd fd fd fa fa fa  
  0x318236c0: fa fa fa fa fa fa fd fd fd fd fd fd fd fd fd fd  
  0x318236d0: fd fd fd fa fa fa fa fa fa fa fa fa fd fd fd fd  
  0x318236e0: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa  
  0x318236f0: fa fa fd fd fd fd fd fd fd fd fd fd fd fd fd fa  
  0x31823700: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  
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
==7932==ABORTING  

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

Might be related to crbug.com/799688

### rh...@chromium.org (2018-02-02)

[Empty comment from Monorail migration]

### pa...@chromium.org (2018-02-02)

[Empty comment from Monorail migration]

### rh...@chromium.org (2018-04-24)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-04-24)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/9afcfa46ee07bc22c94d49942f5a61d6a374fd2d

commit 9afcfa46ee07bc22c94d49942f5a61d6a374fd2d
Author: Ryan Harrison <rharrison@chromium.org>
Date: Tue Apr 24 18:44:29 2018

Switch declaration order to prevent UAF

This is occuring when the variables go out of scope, due to C++s first
in, last out destruction policy.

BUG=chromium:808333

Change-Id: I44f37520a22720bc23df4c8a72ff73994c37eea1
Reviewed-on: https://pdfium-review.googlesource.com/31278
Commit-Queue: Ryan Harrison <rharrison@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>

[modify] https://crrev.com/9afcfa46ee07bc22c94d49942f5a61d6a374fd2d/xfa/fxfa/parser/cxfa_document.cpp


### rh...@chromium.org (2018-04-24)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-04-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4171ca1f41cb4d224e716dbe8a60e143394f860d

commit 4171ca1f41cb4d224e716dbe8a60e143394f860d
Author: pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Tue Apr 24 23:43:09 2018

Roll src/third_party/pdfium/ 6453a67d8..b242943f5 (2 commits)

https://pdfium.googlesource.com/pdfium.git/+log/6453a67d84dc..b242943f5e94

$ git log 6453a67d8..b242943f5 --date=short --no-merges --format='%ad %ae %s'
2018-04-24 dsinclair Remove m_CurNodeType from CFX_XMLParser
2018-04-24 rharrison Switch declaration order to prevent UAF

Created with:
  roll-dep src/third_party/pdfium
BUG=chromium:808333


The AutoRoll server is located here: https://pdfium-roll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.


TBR=dsinclair@chromium.org

Change-Id: Ica15741534c4ee7dcc743f8715fb0271a1dae843
Reviewed-on: https://chromium-review.googlesource.com/1026525
Reviewed-by: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Commit-Queue: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#553368}
[modify] https://crrev.com/4171ca1f41cb4d224e716dbe8a60e143394f860d/DEPS


### sh...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-09-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-09-28)

Thanks stackexploit@! $3,000 for this one.

### aw...@google.com (2018-09-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-09-28)

This issue was migrated from crbug.com/chromium/808333?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/62400]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090361)*
