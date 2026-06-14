# Security: PDFium Heap Buffer Overflow in CXFA_TextLayout::DoLayout

| Field | Value |
|-------|-------|
| **Issue ID** | [40093874](https://issues.chromium.org/issues/40093874) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Reporter** | st...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2019-01-28 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

This issue affects the lastest version of PDFium ( <https://pdfium.googlesource.com/pdfium/+/refs/heads/master> ). When enabling XFA and ASAN, pdfium\_test.exe shows the following log.

# Rendering PDF file C:\poc.pdf. Document has invalid cross reference table

==22020==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x0ce01e54 at pc 0x0348e1cc bp 0x001cdc5c sp 0x001cdc50  

READ of size 4 at 0x0ce01e54 thread T0  

#0 0x348e1cb in CXFA\_TextLayout::DoLayout C:\pdfium\xfa\fxfa\cxfa\_textlayout.cpp:356  

#1 0x33e6dc0 in CXFA\_Node::FindSplitPos C:\pdfium\xfa\fxfa\parser\cxfa\_node.cpp:3474  

#2 0x338d9e2 in `anonymous namespace'::FindLayoutItemSplitPos C:\pdfium\xfa\fxfa\parser\cxfa_itemlayoutprocessor.cpp:501 #3 0x338db15 in` anonymous namespace'::FindLayoutItemSplitPos C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:523  

#4 0x338db15 in `anonymous namespace'::FindLayoutItemSplitPos C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:523  

#5 0x338d4c1 in CXFA\_ItemLayoutProcessor::FindSplitPos C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:674  

#6 0x339fddf in CXFA\_ItemLayoutProcessor::InsertFlowedItem C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2670  

#7 0x339bcde in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:1960  

#8 0x33918dc in CXFA\_ItemLayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2226  

#9 0x33b85cf in CXFA\_LayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_layoutprocessor.cpp:74  

#10 0x3452164 in CXFA\_FFDocView::DoLayout C:\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp:94  

#11 0x34c7124 in CPDFXFA\_Context::LoadXFADoc C:\pdfium\fpdfsdk\fpdfxfa\cpdfxfa\_context.cpp:136  

#12 0x34e0c1b in FPDF\_LoadXFA C:\pdfium\fpdfsdk\fpdf\_view.cpp:255  

#13 0xbc4b15 in main C:\pdfium\samples\pdfium\_test.cc:1005  

#14 0x39767aa in \_\_scrt\_common\_main\_seh d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#15 0x7730343c in BaseThreadInitThunk+0x11 (C:\Windows\syswow64\kernel32.dll+0x7dd7343c)  

#16 0x77a69801 in RtlInitializeExceptionChain+0x62 (C:\Windows\SysWOW64\ntdll.dll+0x7dea9801)  

#17 0x77a697d4 in RtlInitializeExceptionChain+0x35 (C:\Windows\SysWOW64\ntdll.dll+0x7dea97d4)

0x0ce01e54 is located 0 bytes to the right of 52-byte region [0x0ce01e20,0x0ce01e54)  

allocated by thread T0 here:  

#0 0x396020c in malloc c:\b\rr\tmpoxo5hi\w\src\third\_party\llvm\projects\compiler-rt\lib\asan\asan\_malloc\_win.cc:69  

#1 0x3973764 in operator new d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0xbf148c in std::vector<const tagENHMETARECORD \*,std::allocator<const tagENHMETARECORD \*> >::\_Emplace\_reallocate<const tagENHMETARECORD \*const &> C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.16.27023\include\vector:956  

#3 0xbf12e1 in std::vector<const tagENHMETARECORD \*,std::allocator<const tagENHMETARECORD \*> >::emplace\_back<const tagENHMETARECORD \*const &> C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.16.27023\include\vector:922  

#4 0x348e5fe in CXFA\_TextLayout::DoLayout C:\pdfium\xfa\fxfa\cxfa\_textlayout.cpp:383  

#5 0x33e6dc0 in CXFA\_Node::FindSplitPos C:\pdfium\xfa\fxfa\parser\cxfa\_node.cpp:3474  

#6 0x338d9e2 in `anonymous namespace'::FindLayoutItemSplitPos C:\pdfium\xfa\fxfa\parser\cxfa_itemlayoutprocessor.cpp:501 #7 0x338db15 in` anonymous namespace'::FindLayoutItemSplitPos C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:523  

#8 0x338db15 in `anonymous namespace'::FindLayoutItemSplitPos C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:523  

#9 0x338d4c1 in CXFA\_ItemLayoutProcessor::FindSplitPos C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:674  

#10 0x339fddf in CXFA\_ItemLayoutProcessor::InsertFlowedItem C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2670  

#11 0x339bcde in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:1960  

#12 0x33918dc in CXFA\_ItemLayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_itemlayoutprocessor.cpp:2226  

#13 0x33b85cf in CXFA\_LayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_layoutprocessor.cpp:74  

#14 0x3452164 in CXFA\_FFDocView::DoLayout C:\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp:94  

#15 0x34c7124 in CPDFXFA\_Context::LoadXFADoc C:\pdfium\fpdfsdk\fpdfxfa\cpdfxfa\_context.cpp:136  

#16 0x34e0c1b in FPDF\_LoadXFA C:\pdfium\fpdfsdk\fpdf\_view.cpp:255  

#17 0xbc4b15 in main C:\pdfium\samples\pdfium\_test.cc:1005  

#18 0x39767aa in \_\_scrt\_common\_main\_seh d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#19 0x7730343c in BaseThreadInitThunk+0x11 (C:\Windows\syswow64\kernel32.dll+0x7dd7343c)  

#20 0x77a69801 in RtlInitializeExceptionChain+0x62 (C:\Windows\SysWOW64\ntdll.dll+0x7dea9801)  

#21 0x77a697d4 in RtlInitializeExceptionChain+0x35 (C:\Windows\SysWOW64\ntdll.dll+0x7dea97d4)

SUMMARY: AddressSanitizer: heap-buffer-overflow C:\pdfium\xfa\fxfa\cxfa\_textlayout.cpp:356 in CXFA\_TextLayout::DoLayout  

Shadow bytes around the buggy address:  

0x319c0370: fd fd fd fd fd fd fd fa fa fa fa fa fd fd fd fd  

0x319c0380: fd fd fd fa fa fa fa fa fd fd fd fd fd fd fd fa  

0x319c0390: fa fa fa fa fd fd fd fd fd fd fd fd fa fa fa fa  

0x319c03a0: fd fd fd fd fd fd fd fa fa fa fa fa fd fd fd fd  

0x319c03b0: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fa  

=>0x319c03c0: fa fa fa fa 00 00 00 00 00 00[04]fa fa fa fa fa  

0x319c03d0: 00 00 00 00 00 00 04 fa fa fa fa fa 00 00 00 00  

0x319c03e0: 00 00 00 fa fa fa fa fa fd fd fd fd fd fd fd fa  

0x319c03f0: fa fa fa fa 00 00 00 00 00 00 00 fa fa fa fa fa  

0x319c0400: 00 00 00 00 00 00 00 fa fa fa fa fa fd fd fd fd  

0x319c0410: fd fd fd fa fa fa fa fa 00 00 00 00 00 00 00 00  

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

==22020==ABORTING

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

Might want to cross-reference with https://crbug.com/chromium/925787 since they seem possibly related. thestig@, are you able to help take a look? Thanks!

[Monorail components: Internals>Plugins>PDF]

### li...@chromium.org (2019-01-28)

Actually assigning this time

### sh...@chromium.org (2019-01-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-29)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-01-29)

[Empty comment from Monorail migration]

### th...@chromium.org (2019-01-29)

XFA = not shipped.

### th...@chromium.org (2019-04-10)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-10)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/52c673122691a1ed26c664db9c0d8c613a566fbb

commit 52c673122691a1ed26c664db9c0d8c613a566fbb
Author: Lei Zhang <thestig@chromium.org>
Date: Wed Apr 10 17:27:59 2019

Prevent an out of bound access in CXFA_TextLayout::DoLayout().

BUG=chromium:925788

Change-Id: I46b910001f6d789e8dca48fdb18d1f86c9bd7592
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/49496
Commit-Queue: Lei Zhang <thestig@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>

[modify] https://crrev.com/52c673122691a1ed26c664db9c0d8c613a566fbb/xfa/fxfa/cxfa_textlayout.cpp


### th...@chromium.org (2019-04-10)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f0fd07109ffd224c579307e686e263db4b127805

commit f0fd07109ffd224c579307e686e263db4b127805
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Apr 10 22:04:41 2019

Roll src/third_party/pdfium 44034bca7d3e..b9516868546e (9 commits)

https://pdfium.googlesource.com/pdfium.git/+log/44034bca7d3e..b9516868546e


git log 44034bca7d3e..b9516868546e --date=short --no-merges --format='%ad %ae %s'
2019-04-10 thestig@chromium.org Convert |CXFA_FFDocView::m_IndexChangedSubforms| to a deque.
2019-04-10 thestig@chromium.org Add a test to exercise FPDF_FFLDraw() with FPDF_REVERSE_BYTE_ORDER.
2019-04-10 tsepez@chromium.org Separate CXFA_FFWidget from CXFA_ContentLayoutItem.
2019-04-10 thestig@chromium.org Use early returns in CXFA_Node.
2019-04-10 thestig@chromium.org Give CXFA_FFDocView* params proper names in CXFA_Node.
2019-04-10 thestig@chromium.org Return Optional<float> from CXFA_Node::FindSplitPos().
2019-04-10 thestig@chromium.org Add CXFA_LayoutPageMgr::ShouldGetNextPageArea().
2019-04-10 thestig@chromium.org Add CXFA_LayoutPageMgr::HasCurrentViewRecord().
2019-04-10 thestig@chromium.org Prevent an out of bound access in CXFA_TextLayout::DoLayout().


Created with:
  gclient setdep -r src/third_party/pdfium@b9516868546e

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:932900,chromium:925788
TBR=dsinclair@chromium.org

Change-Id: I368f5bf1b393923a8002ecab848b75b702eb16b3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1562493
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#649672}
[modify] https://crrev.com/f0fd07109ffd224c579307e686e263db4b127805/DEPS


### sh...@chromium.org (2019-04-11)

[Empty comment from Monorail migration]

### na...@google.com (2019-04-15)

[Empty comment from Monorail migration]

### na...@google.com (2019-04-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### pa...@chromium.org (2019-04-18)

Congrats! The Panel decided to reward $1,000 for this report!

### aw...@google.com (2019-04-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/925788?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/944793]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093874)*
