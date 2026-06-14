# Security: PDFium Heap Buffer Overflow in CXFA_LayoutPageMgr::FinishPaginatedPageSets

| Field | Value |
|-------|-------|
| **Issue ID** | [40093873](https://issues.chromium.org/issues/40093873) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2019-01-28 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

This issue affects the lastest version of PDFium ( <https://pdfium.googlesource.com/pdfium/+/refs/heads/master> ). When enabling XFA and ASAN, pdfium\_test.exe shows the following log.

# Rendering PDF file C:\poc.pdf. Document has invalid cross reference table

==19924==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x0ce0bb74 at pc 0x0289f30b bp 0x0432e9fc sp 0x0432e9f0  

READ of size 4 at 0x0ce0bb74 thread T0  

#0 0x289f30a in CXFA\_LayoutPageMgr::FinishPaginatedPageSets C:\pdfium\xfa\fxfa\parser\cxfa\_layoutpagemgr.cpp:708  

#1 0x28a86fe in CXFA\_LayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_layoutprocessor.cpp:88  

#2 0x2942164 in CXFA\_FFDocView::DoLayout C:\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp:94  

#3 0x29b7124 in CPDFXFA\_Context::LoadXFADoc C:\pdfium\fpdfsdk\fpdfxfa\cpdfxfa\_context.cpp:136  

#4 0x29d0c1b in FPDF\_LoadXFA C:\pdfium\fpdfsdk\fpdf\_view.cpp:255  

#5 0xb4b15 in main C:\pdfium\samples\pdfium\_test.cc:1005  

#6 0x2e667aa in \_\_scrt\_common\_main\_seh d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#7 0x7730343c in BaseThreadInitThunk+0x11 (C:\Windows\syswow64\kernel32.dll+0x7dd7343c)  

#8 0x77a69801 in RtlInitializeExceptionChain+0x62 (C:\Windows\SysWOW64\ntdll.dll+0x7dea9801)  

#9 0x77a697d4 in RtlInitializeExceptionChain+0x35 (C:\Windows\SysWOW64\ntdll.dll+0x7dea97d4)

0x0ce0bb74 is located 0 bytes to the right of 4-byte region [0x0ce0bb70,0x0ce0bb74)  

allocated by thread T0 here:  

#0 0x2e5020c in malloc c:\b\rr\tmpoxo5hi\w\src\third\_party\llvm\projects\compiler-rt\lib\asan\asan\_malloc\_win.cc:69  

#1 0x2e63764 in operator new d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0xe148c in std::vector<const tagENHMETARECORD \*,std::allocator<const tagENHMETARECORD \*> >::\_Emplace\_reallocate<const tagENHMETARECORD \*const &> C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.16.27023\include\vector:956  

#3 0xe12e1 in std::vector<const tagENHMETARECORD \*,std::allocator<const tagENHMETARECORD \*> >::emplace\_back<const tagENHMETARECORD \*const &> C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.16.27023\include\vector:922  

#4 0x289e800 in CXFA\_LayoutPageMgr::FinishPaginatedPageSets C:\pdfium\xfa\fxfa\parser\cxfa\_layoutpagemgr.cpp:693  

#5 0x28a86fe in CXFA\_LayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_layoutprocessor.cpp:88  

#6 0x2942164 in CXFA\_FFDocView::DoLayout C:\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp:94  

#7 0x29b7124 in CPDFXFA\_Context::LoadXFADoc C:\pdfium\fpdfsdk\fpdfxfa\cpdfxfa\_context.cpp:136  

#8 0x29d0c1b in FPDF\_LoadXFA C:\pdfium\fpdfsdk\fpdf\_view.cpp:255  

#9 0xb4b15 in main C:\pdfium\samples\pdfium\_test.cc:1005  

#10 0x2e667aa in \_\_scrt\_common\_main\_seh d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#11 0x7730343c in BaseThreadInitThunk+0x11 (C:\Windows\syswow64\kernel32.dll+0x7dd7343c)  

#12 0x77a69801 in RtlInitializeExceptionChain+0x62 (C:\Windows\SysWOW64\ntdll.dll+0x7dea9801)  

#13 0x77a697d4 in RtlInitializeExceptionChain+0x35 (C:\Windows\SysWOW64\ntdll.dll+0x7dea97d4)

SUMMARY: AddressSanitizer: heap-buffer-overflow C:\pdfium\xfa\fxfa\parser\cxfa\_layoutpagemgr.cpp:708 in CXFA\_LayoutPageMgr::FinishPaginatedPageSets  

Shadow bytes around the buggy address:  

0x319c1710: fa fa fd fd fa fa fd fd fa fa fd fa fa fa fd fd  

0x319c1720: fa fa fd fa fa fa 00 fa fa fa fd fd fa fa fd fd  

0x319c1730: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fd  

0x319c1740: fa fa fd fd fa fa fd fa fa fa fd fa fa fa fd fd  

0x319c1750: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa  

=>0x319c1760: fa fa fd fa fa fa fd fa fa fa fd fa fa fa[04]fa  

0x319c1770: fa fa 00 04 fa fa 00 fa fa fa 00 04 fa fa 00 04  

0x319c1780: fa fa fd fa fa fa 00 04 fa fa 00 04 fa fa 00 04  

0x319c1790: fa fa 04 fa fa fa 04 fa fa fa 00 00 fa fa 00 00  

0x319c17a0: fa fa 00 00 fa fa 00 00 fa fa 00 00 fa fa 00 00  

0x319c17b0: fa fa 00 00 fa fa 00 fa fa fa fd fd fa fa 00 00  

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

==19924==ABORTING

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

### cl...@chromium.org (2019-01-28)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5482770541445120.

### cl...@chromium.org (2019-01-28)

Testcase 5482770541445120 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5482770541445120.

### li...@chromium.org (2019-01-28)

Might want to cross-reference with https://crbug.com/chromium/925788 since they seem possibly related. thestig@, are you able to help take a look? Thanks!

[Monorail components: Internals>Plugins>PDF]

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

### th...@chromium.org (2019-01-30)

https://pdfium-review.googlesource.com/49474

### cl...@chromium.org (2019-04-03)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-09)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/26de1a62e3178d7a3e90f4eb857da3ebb3aa8edc

commit 26de1a62e3178d7a3e90f4eb857da3ebb3aa8edc
Author: Lei Zhang <thestig@chromium.org>
Date: Tue Apr 09 21:27:46 2019

Prevent out of bound access inside CXFA_LayoutPageMgr.

BUG=chromium:925787

Change-Id: I8f4dd73d61561ed1e767e071ab9021c26d955c0c
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/49474
Commit-Queue: Lei Zhang <thestig@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>

[modify] https://crrev.com/26de1a62e3178d7a3e90f4eb857da3ebb3aa8edc/xfa/fxfa/layout/cxfa_layoutpagemgr.cpp


### th...@chromium.org (2019-04-09)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f51633370fa45b09487fa231b74e331a3795321d

commit f51633370fa45b09487fa231b74e331a3795321d
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Apr 09 23:16:45 2019

Roll src/third_party/pdfium c75ce35aa1a7..44034bca7d3e (5 commits)

https://pdfium.googlesource.com/pdfium.git/+log/c75ce35aa1a7..44034bca7d3e


git log c75ce35aa1a7..44034bca7d3e --date=short --no-merges --format='%ad %ae %s'
2019-04-09 tsepez@chromium.org Make CXFA_TraverseStrategy_ViewLayoutItem private to cxfa_layoutpagemgr.cpp.
2019-04-09 thestig@chromium.org Prevent out of bound access inside CXFA_LayoutPageMgr.
2019-04-09 tsepez@chromium.org Rename CXFA_ContainerLayoutItem to CXFA_ViewLayoutItem.
2019-04-09 thestig@chromium.org Switch from vector to deque for some CXFA_FFDocView members.
2019-04-08 tsepez@chromium.org Correct hierarchy description in xfa/fxfa/README.md


Created with:
  gclient setdep -r src/third_party/pdfium@44034bca7d3e

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:925787
TBR=dsinclair@chromium.org

Change-Id: I2b1c7473324b228a52aff4aada9295baa0c10833
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1560393
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#649321}
[modify] https://crrev.com/f51633370fa45b09487fa231b74e331a3795321d/DEPS


### sh...@chromium.org (2019-04-10)

[Empty comment from Monorail migration]

### na...@google.com (2019-04-10)

[Empty comment from Monorail migration]

### na...@google.com (2019-04-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-04-10)

Congrats! The Panel decided to reward $1,000 for this report! 

### na...@google.com (2019-04-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/925787?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093873)*
