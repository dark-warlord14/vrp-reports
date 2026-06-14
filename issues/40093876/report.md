# Security: PDFium Use After Free in CXFA_ItemLayoutProcessor::ExtractLayoutItem

| Field | Value |
|-------|-------|
| **Issue ID** | [40093876](https://issues.chromium.org/issues/40093876) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Reporter** | st...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2019-01-28 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

This issue affects the lastest version of PDFium ( <https://pdfium.googlesource.com/pdfium/+/refs/heads/master> ). When enabling XFA and ASAN, pdfium\_test.exe shows the following log.

# Rendering PDF file C:\poc.pdf. Document has invalid cross reference table

==21628==ERROR: AddressSanitizer: heap-use-after-free on address 0x0d0044ec at pc 0x028ff6d8 bp 0x043dd878 sp 0x043dd86c  

READ of size 4 at 0x0d0044ec thread T0  

#0 0x28ff6d7 in CXFA\_ItemLayoutProcessor::ExtractLayoutItem C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:830  

#1 0x291098a in CXFA\_ItemLayoutProcessor::InsertFlowedItem C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2723  

#2 0x290bcde in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:1960  

#3 0x29018dc in CXFA\_ItemLayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2226  

#4 0x290f4e5 in CXFA\_ItemLayoutProcessor::InsertFlowedItem C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2532  

#5 0x290bcde in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:1960  

#6 0x29018dc in CXFA\_ItemLayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2226  

#7 0x29285cf in CXFA\_LayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_layoutprocessor.cpp:74  

#8 0x29c2959 in CXFA\_FFDocView::RunLayout C:\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp:450  

#9 0x29c22a9 in CXFA\_FFDocView::StopLayout C:\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp:132  

#10 0x2a37139 in CPDFXFA\_Context::LoadXFADoc C:\pdfium\fpdfsdk\fpdfxfa\cpdfxfa\_context.cpp:137  

#11 0x2a50c1b in FPDF\_LoadXFA C:\pdfium\fpdfsdk\fpdf\_view.cpp:255  

#12 0x134b15 in main C:\pdfium\samples\pdfium\_test.cc:1005  

#13 0x2ee67aa in \_\_scrt\_common\_main\_seh d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#14 0x7730343c in BaseThreadInitThunk+0x11 (C:\Windows\syswow64\kernel32.dll+0x7dd7343c)  

#15 0x77a69801 in RtlInitializeExceptionChain+0x62 (C:\Windows\SysWOW64\ntdll.dll+0x7dea9801)  

#16 0x77a697d4 in RtlInitializeExceptionChain+0x35 (C:\Windows\SysWOW64\ntdll.dll+0x7dea97d4)

0x0d0044ec is located 28 bytes inside of 80-byte region [0x0d0044d0,0x0d004520)  

freed by thread T0 here:  

#0 0x2ed0108 in free c:\b\rr\tmpoxo5hi\w\src\third\_party\llvm\projects\compiler-rt\lib\asan\asan\_malloc\_win.cc:53  

#1 0x29b0630 in CXFA\_FFArc::~CXFA\_FFArc C:\pdfium\xfa\fxfa\cxfa\_ffarc.cpp:14  

#2 0x28ff4ce in CXFA\_ItemLayoutProcessor::ExtractLayoutItem C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:835  

#3 0x291098a in CXFA\_ItemLayoutProcessor::InsertFlowedItem C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2723  

#4 0x290bcde in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:1960  

#5 0x29018dc in CXFA\_ItemLayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2226  

#6 0x290f4e5 in CXFA\_ItemLayoutProcessor::InsertFlowedItem C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2532  

#7 0x290bcde in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:1960  

#8 0x29018dc in CXFA\_ItemLayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2226  

#9 0x29285cf in CXFA\_LayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_layoutprocessor.cpp:74  

#10 0x29c2959 in CXFA\_FFDocView::RunLayout C:\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp:450  

#11 0x29c22a9 in CXFA\_FFDocView::StopLayout C:\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp:132  

#12 0x2a37139 in CPDFXFA\_Context::LoadXFADoc C:\pdfium\fpdfsdk\fpdfxfa\cpdfxfa\_context.cpp:137  

#13 0x2a50c1b in FPDF\_LoadXFA C:\pdfium\fpdfsdk\fpdf\_view.cpp:255  

#14 0x134b15 in main C:\pdfium\samples\pdfium\_test.cc:1005  

#15 0x2ee67aa in \_\_scrt\_common\_main\_seh d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#16 0x7730343c in BaseThreadInitThunk+0x11 (C:\Windows\syswow64\kernel32.dll+0x7dd7343c)  

#17 0x77a69801 in RtlInitializeExceptionChain+0x62 (C:\Windows\SysWOW64\ntdll.dll+0x7dea9801)  

#18 0x77a697d4 in RtlInitializeExceptionChain+0x35 (C:\Windows\SysWOW64\ntdll.dll+0x7dea97d4)

previously allocated by thread T0 here:  

#0 0x2ed020c in malloc c:\b\rr\tmpoxo5hi\w\src\third\_party\llvm\projects\compiler-rt\lib\asan\asan\_malloc\_win.cc:69  

#1 0x2ee3764 in operator new d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x29d54e7 in CXFA\_FFNotify::OnCreateContentLayoutItem C:\pdfium\xfa\fxfa\cxfa\_ffnotify.cpp:190  

#3 0x28fd084 in CXFA\_ItemLayoutProcessor::CreateContentLayoutItem C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:651  

#4 0x28fe0cf in CXFA\_ItemLayoutProcessor::SplitLayoutItem C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp  

#5 0x2910639 in CXFA\_ItemLayoutProcessor::InsertFlowedItem C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2700  

#6 0x290bcde in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:1960  

#7 0x29018dc in CXFA\_ItemLayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2226  

#8 0x290f4e5 in CXFA\_ItemLayoutProcessor::InsertFlowedItem C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2532  

#9 0x290bcde in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:1960  

#10 0x29018dc in CXFA\_ItemLayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2226  

#11 0x29285cf in CXFA\_LayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_layoutprocessor.cpp:74  

#12 0x29c2164 in CXFA\_FFDocView::DoLayout C:\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp:94  

#13 0x2a37124 in CPDFXFA\_Context::LoadXFADoc C:\pdfium\fpdfsdk\fpdfxfa\cpdfxfa\_context.cpp:136  

#14 0x2a50c1b in FPDF\_LoadXFA C:\pdfium\fpdfsdk\fpdf\_view.cpp:255  

#15 0x134b15 in main C:\pdfium\samples\pdfium\_test.cc:1005  

#16 0x2ee67aa in \_\_scrt\_common\_main\_seh d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#17 0x7730343c in BaseThreadInitThunk+0x11 (C:\Windows\syswow64\kernel32.dll+0x7dd7343c)  

#18 0x77a69801 in RtlInitializeExceptionChain+0x62 (C:\Windows\SysWOW64\ntdll.dll+0x7dea9801)  

#19 0x77a697d4 in RtlInitializeExceptionChain+0x35 (C:\Windows\SysWOW64\ntdll.dll+0x7dea97d4)

SUMMARY: AddressSanitizer: heap-use-after-free C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:830 in CXFA\_ItemLayoutProcessor::ExtractLayoutItem  

Shadow bytes around the buggy address:  

0x31a00840: fd fd fa fa fa fa fd fd fd fd fd fd fd fd fd fa  

0x31a00850: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 fa fa  

0x31a00860: fa fa 00 00 00 00 00 00 00 00 00 00 fa fa fa fa  

0x31a00870: fd fd fd fd fd fd fd fd fd fd fa fa fa fa 00 00  

0x31a00880: 00 00 00 00 00 00 00 00 fa fa fa fa 00 00 00 00  

=>0x31a00890: 00 00 00 00 00 00 fa fa fa fa fd fd fd[fd]fd fd  

0x31a008a0: fd fd fd fd fa fa fa fa 00 00 00 00 00 00 00 00  

0x31a008b0: 00 00 fa fa fa fa 00 00 00 00 00 00 00 00 00 00  

0x31a008c0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fa fa  

0x31a008d0: fa fa 00 00 00 00 00 00 00 00 00 00 fa fa fa fa  

0x31a008e0: 00 00 00 00 00 00 00 00 00 00 fa fa fa fa fd fd  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

Shadow gap: cc  

==21628==ABORTING

**VERSION**  

Chrome Version: pdfium master  

Operating System: All

**REPRODUCTION CASE**  

A minimized POC was attached.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

**Reporter credit: [goes here]**

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### li...@chromium.org (2019-01-28)

Tentatively setting some labels. Possibly related to https://crbug.com/chromium/925789. thestig@, would you be able to help take a look?

[Monorail components: Internals>Plugins>PDF]

### li...@chromium.org (2019-01-28)

Actually going to close this as a duplicate of https://crbug.com/chromium/913564.

### ts...@chromium.org (2019-01-28)

Nice. Circular list of pOldLayoutItem->m_pNext while walking down the list freeing objects.  

This one may be easier to diagnose with than the dup'd case.

### st...@gmail.com (2019-01-28)

According to https://crbug.com/chromium/925790#c3, I have a question that is it really a duplicate one? Could you please help me confirm? Thanks.

### ts...@chromium.org (2019-01-29)

https://pdfium-review.googlesource.com/c/pdfium/+/49350 fixes this issue (at least locally, and the fuzzer will confirm it is the same cause as 913564 after it lands).

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-01-29)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/3c908922cc1836ecb795bc7d4ed62ef9fe7aa7df

commit 3c908922cc1836ecb795bc7d4ed62ef9fe7aa7df
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Jan 29 19:18:27 2019

Prevent cxfa_contentlayoutitem linked lists from getting entangled.

Implement the basic linked-list primitives, and use them
consistently. Currently the code is doing ad-hoc manipulations
of these pointers, and creating circular lists somewhere. This
causes re-frees as we walk down the list freeing every item.

Use UnownedPtr<> to try to catch any future botches.

Tested against the test case in 925790 (CF fuzzer will subsequently
verify 913564).

Bug: chromium:913564, chromium:925790
Change-Id: I2b735b3137aa715e5bb6b1c4472a1d2fd68ae286
Reviewed-on: https://pdfium-review.googlesource.com/c/49350
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://crrev.com/3c908922cc1836ecb795bc7d4ed62ef9fe7aa7df/xfa/fxfa/parser/cxfa_contentlayoutitem.cpp
[modify] https://crrev.com/3c908922cc1836ecb795bc7d4ed62ef9fe7aa7df/xfa/fxfa/parser/cxfa_contentlayoutitem.h
[modify] https://crrev.com/3c908922cc1836ecb795bc7d4ed62ef9fe7aa7df/xfa/fxfa/parser/cxfa_itemlayoutprocessor.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-01-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6206d8123bce7501089b44d4f12b64d82a9e11fc

commit 6206d8123bce7501089b44d4f12b64d82a9e11fc
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Jan 29 22:14:42 2019

Roll src/third_party/pdfium 01ab0dcc9303..8b6b33c3b8fc (7 commits)

https://pdfium.googlesource.com/pdfium.git/+log/01ab0dcc9303..8b6b33c3b8fc


git log 01ab0dcc9303..8b6b33c3b8fc --date=short --no-merges --format='%ad %ae %s'
2019-01-29 tsepez@chromium.org Remove unused FWL stretch handler mechanism.
2019-01-29 thestig@chromium.org Split XFA_FFWidgetType into its own header file.
2019-01-29 tsepez@chromium.org Prevent cxfa_contentlayoutitem linked lists from getting entangled.
2019-01-29 thestig@chromium.org Initialize CFX_GifContext members in the header.
2019-01-29 thestig@chromium.org Use std::move() inside CBC_OneDimWriter::RenderVerticalBars().
2019-01-29 thestig@chromium.org Make pAttribute parameter required in LoadImageInfo().
2019-01-29 thestig@chromium.org Remove effectively unused CFX_DIBAttribute members.


Created with:
  gclient setdep -r src/third_party/pdfium@8b6b33c3b8fc

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:913564,chromium:925790,chromium:925415
TBR=dsinclair@chromium.org

Change-Id: Ie8197749d6c5b6af69b8c463fa049eba67504863
Reviewed-on: https://chromium-review.googlesource.com/c/1444174
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#627177}
[modify] https://crrev.com/6206d8123bce7501089b44d4f12b64d82a9e11fc/DEPS


### ts...@chromium.org (2019-01-29)

I'm going to mark this as a non-duplicate, as the associated reproduces despite correcting this corruption (which fixed this bug).

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### na...@google.com (2019-02-04)

[Empty comment from Monorail migration]

### na...@google.com (2019-02-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-02-07)

Congrats! The Panel has decided to reward $3000 for this report :) 

### na...@google.com (2019-02-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/925790?no_tracker_redirect=1

[Monorail mergedinto: crbug.com/chromium/913564]
[Monorail components added to Component Tags custom field.]

### dt...@google.com (2025-02-13)

Bulk update of issues accidentally marked as duplicate in issue tracker migration (b/325072672)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093876)*
