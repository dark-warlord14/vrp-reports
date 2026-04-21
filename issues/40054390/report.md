# Security: PDFIum (XFA) Heap Overflow in RelocateTableRowCells

| Field | Value |
|-------|-------|
| **Issue ID** | [40054390](https://issues.chromium.org/issues/40054390) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | dy...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2021-01-08 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

While running my fuzzer I found the following HeapOverflow crash in pdfium. A minimized testcase to reproduce is attached.

**VERSION**  

built from 4f67a285e22100c9dc9d175e8269c8fed1734f34  

with "pdf\_enable\_xfa=true pdf\_enable\_v8=true pdf\_is\_standalone=true is\_component\_build=false is\_asan=true is\_debug=false"

**REPRODUCTION CASE**  

Run pdfium\_test(XFA enabled) with poc.pdf.

# ASAN output:

==1678247==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60200004c174 at pc 0x55839634006e bp 0x7ffca7901e50 sp 0x7ffca7901e48  

READ of size 4 at 0x60200004c174 thread T0  

#0 0x55839634006d in (anonymous namespace)::RelocateTableRowCells(CXFA\_ContentLayoutItem\*, std::\_\_1::vector<float, std::\_\_1::allocator<float> > const&, XFA\_AttributeValue) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:232:24  

#1 0x55839633db20 in CXFA\_ContentLayoutProcessor::DoLayoutTableContainer(CXFA\_Node\*) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:1329:9  

#2 0x55839633aa29 in CXFA\_ContentLayoutProcessor::DoLayoutInternal(bool, float, float, CXFA\_ContentLayoutProcessor::Context\*) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:2113:11  

#3 0x55839633930f in CXFA\_ContentLayoutProcessor::DoLayoutPositionedContainer(CXFA\_ContentLayoutProcessor::Context\*) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:1096:17  

#4 0x55839633a9c0 in CXFA\_ContentLayoutProcessor::DoLayoutInternal(bool, float, float, CXFA\_ContentLayoutProcessor::Context\*) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:2109:11  

#5 0x558396337dc5 in DoLayout xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:2081:10  

#6 0x558396337dc5 in CXFA\_ContentLayoutProcessor::DoLayoutPageArea(CXFA\_ViewLayoutItem\*) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:1003:17  

#7 0x55839636082a in LayoutPageSetContents xfa/fxfa/layout/cxfa\_viewlayoutprocessor.cpp:1862:60  

#8 0x55839636082a in CXFA\_ViewLayoutProcessor::SyncLayoutData() xfa/fxfa/layout/cxfa\_viewlayoutprocessor.cpp:1870:3  

#9 0x558396352c72 in CXFA\_LayoutProcessor::DoLayout() xfa/fxfa/layout/cxfa\_layoutprocessor.cpp:108:29  

#10 0x5583961b2b73 in CXFA\_FFDocView::DoLayout() xfa/fxfa/cxfa\_ffdocview.cpp:108:43  

#11 0x558396472d2c in CPDFXFA\_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa\_context.cpp:188:18  

#12 0x558393461c16 in FPDF\_LoadXFA fpdfsdk/fpdf\_view.cpp:268:22  

#13 0x5583933d8914 in ProcessPdf samples/pdfium\_test.cc:990:12  

#14 0x5583933d8914 in main samples/pdfium\_test.cc:1271:5  

#15 0x7f03d5c970b2 in \_\_libc\_start\_main /build/glibc-ZN95T4/glibc-2.31/csu/../csu/libc-start.c:308:16

0x60200004c174 is located 0 bytes to the right of 4-byte region [0x60200004c170,0x60200004c174)  

allocated by thread T0 here:  

#0 0x5583933ce15d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:99:3  

#1 0x5583933ef3f6 in \_\_libcpp\_allocate buildtools/third\_party/libc++/trunk/include/new:253:10  

#2 0x5583933ef3f6 in allocate buildtools/third\_party/libc++/trunk/include/memory:1853:37  

#3 0x5583933ef3f6 in allocate buildtools/third\_party/libc++/trunk/include/memory:1570:21  

#4 0x5583933ef3f6 in \_\_split\_buffer buildtools/third\_party/libc++/trunk/include/\_\_split\_buffer:318:29  

#5 0x5583933ef3f6 in void std::\_\_1::vector<float, std::\_\_1::allocator<float> >::\_\_push\_back\_slow\_path<float>(float&&) buildtools/third\_party/libc++/trunk/include/vector:1623:49  

#6 0x55839633d371 in push\_back buildtools/third\_party/libc++/trunk/include/vector:1655:9  

#7 0x55839633d371 in CXFA\_ContentLayoutProcessor::DoLayoutTableContainer(CXFA\_Node\*) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:1289:39  

#8 0x55839633aa29 in CXFA\_ContentLayoutProcessor::DoLayoutInternal(bool, float, float, CXFA\_ContentLayoutProcessor::Context\*) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:2113:11  

#9 0x55839633930f in CXFA\_ContentLayoutProcessor::DoLayoutPositionedContainer(CXFA\_ContentLayoutProcessor::Context\*) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:1096:17  

#10 0x55839633a9c0 in CXFA\_ContentLayoutProcessor::DoLayoutInternal(bool, float, float, CXFA\_ContentLayoutProcessor::Context\*) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:2109:11  

#11 0x558396337dc5 in DoLayout xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:2081:10  

#12 0x558396337dc5 in CXFA\_ContentLayoutProcessor::DoLayoutPageArea(CXFA\_ViewLayoutItem\*) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:1003:17  

#13 0x55839636082a in LayoutPageSetContents xfa/fxfa/layout/cxfa\_viewlayoutprocessor.cpp:1862:60  

#14 0x55839636082a in CXFA\_ViewLayoutProcessor::SyncLayoutData() xfa/fxfa/layout/cxfa\_viewlayoutprocessor.cpp:1870:3  

#15 0x558396352c72 in CXFA\_LayoutProcessor::DoLayout() xfa/fxfa/layout/cxfa\_layoutprocessor.cpp:108:29  

#16 0x5583961b2b73 in CXFA\_FFDocView::DoLayout() xfa/fxfa/cxfa\_ffdocview.cpp:108:43  

#17 0x558396472d2c in CPDFXFA\_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa\_context.cpp:188:18  

#18 0x558393461c16 in FPDF\_LoadXFA fpdfsdk/fpdf\_view.cpp:268:22  

#19 0x5583933d8914 in ProcessPdf samples/pdfium\_test.cc:990:12  

#20 0x5583933d8914 in main samples/pdfium\_test.cc:1271:5  

#21 0x7f03d5c970b2 in \_\_libc\_start\_main /build/glibc-ZN95T4/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-buffer-overflow xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:232:24 in (anonymous namespace)::RelocateTableRowCells(CXFA\_ContentLayoutItem\*, std::\_\_1::vector<float, std::\_\_1::allocator<float> > const&, XFA\_AttributeValue)  

Shadow bytes around the buggy address:  

0x0c04800017d0: fa fa fd fd fa fa 00 00 fa fa fd fa fa fa fd fd  

0x0c04800017e0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fd  

0x0c04800017f0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fd  

0x0c0480001800: fa fa fd fa fa fa fd fa fa fa 00 00 fa fa 00 fa  

0x0c0480001810: fa fa 00 fa fa fa 00 fa fa fa fd fa fa fa 00 fa  

=>0x0c0480001820: fa fa fd fa fa fa fd fa fa fa fd fa fa fa[04]fa  

0x0c0480001830: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0480001840: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0480001850: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0480001860: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0480001870: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

==1678247==ABORTING

**CREDIT INFORMATION**  

Yongil Lee and Wonyoung Jung of Diffense

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 5.7 KB)

## Timeline

### [Deleted User] (2021-01-08)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-01-08)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2021-01-08)

Setting severity medium for read in sandboxed process although lilely may not be exploitable due to the way the result is used in subsequent calculations.

### ts...@chromium.org (2021-01-08)

Probably signed integer oveflow at https://source.chromium.org/chromium/chromium/src/+/master:third_party/pdfium/xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp;drc=2947271fe740e34277112cda6b9c70dc54d3b38b;l=226

leading to invalid bounds check. 


### [Deleted User] (2021-01-08)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-01-08)

Looks like I guessed right, ubsan says:
../../xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:226:24: runtime error: signed integer overflow: 1 + 2147483647 cannot be represented in type 'int'



### ts...@chromium.org (2021-01-08)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-08)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/f3b585e8edf5b271445c1ef7ce07f461e87a038f

commit f3b585e8edf5b271445c1ef7ce07f461e87a038f
Author: Tom Sepez <tsepez@chromium.org>
Date: Fri Jan 08 23:03:37 2021

Avoid integer overflow in RelocateTableRowCells().

-- also add some consts as appropriate.

Bug: chromium:1164158
Change-Id: I3146a8f0fc45e1282548dad136379a8f87a7770d
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/77230
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Daniel Hosseinian <dhoss@chromium.org>

[add] https://pdfium.googlesource.com/pdfium/+/f3b585e8edf5b271445c1ef7ce07f461e87a038f/testing/resources/javascript/xfa_specific/bug_1164158.in
[modify] https://pdfium.googlesource.com/pdfium/+/f3b585e8edf5b271445c1ef7ce07f461e87a038f/xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp


### ts...@chromium.org (2021-01-08)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3febdf47541487d92cfaff5961a50020a7fc00d0

commit 3febdf47541487d92cfaff5961a50020a7fc00d0
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Sat Jan 09 00:09:49 2021

Roll PDFium from 4f67a285e221 to f3b585e8edf5 (1 revision)

https://pdfium.googlesource.com/pdfium.git/+log/4f67a285e221..f3b585e8edf5

2021-01-08 tsepez@chromium.org Avoid integer overflow in RelocateTableRowCells().

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Bug: chromium:1164158
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I41efdd60480e820072c4fcefc6ad6f41bb0b6654
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2618535
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#841719}

[modify] https://crrev.com/3febdf47541487d92cfaff5961a50020a7fc00d0/DEPS


### [Deleted User] (2021-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-14)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### am...@google.com (2021-02-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-02-18)

Congratulation, Yongil Lee and Wonyoung Jung! The VRP Panel has decided to award you $5,000 for this report. Nice work. 

### aw...@google.com (2021-02-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-04-17)

This issue was migrated from crbug.com/chromium/1164158?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054390)*
