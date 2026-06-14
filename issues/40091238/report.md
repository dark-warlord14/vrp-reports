# Security: CXFA_Node::FindSplitPos container overflow

| Field | Value |
|-------|-------|
| **Issue ID** | [40091238](https://issues.chromium.org/issues/40091238) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2018-04-27 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Container overflow in pdfium.

**VERSION**  

pdfium\_test  

commit 575f238334d13ab7bc7920eee23c108ef3b0bbed  

Date: Fri Apr 27 01:44:15 2018 +0000

**REPRODUCTION CASE**  

Open attached file.

ADDITIONAL INFORMATION

# Rendering PDF file /workarea/samplestore/wip/pdfium/victory\_todo/victory\_8f4fb392bc9defbb61ae7abe30c90fa9a1c9176d24e0c12d6dbfca25d40ef914.raw.

==31009==ERROR: AddressSanitizer: container-overflow on address 0x61d00005ce54 at pc 0x000003ce83a0 bp 0x7fffffffcf30 sp 0x7fffffffcf28  

READ of size 4 at 0x61d00005ce54 thread T0  

#0 0x3ce839f in CXFA\_Node::FindSplitPos(CXFA\_FFDocView\*, int, float&) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../xfa/fxfa/parser/cxfa\_node.cpp:3221  

#1 0x3ce839f in ?? ??:0  

#2 0x3c6c34b in (anonymous namespace)::FindLayoutItemSplitPos(CXFA\_ContentLayoutItem\*, float, float\*, bool\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:496  

#3 0x3c6c34b in ?? ??:0  

#4 0x3c85661 in FindSplitPos /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:667  

#5 0x3c85661 in InsertFlowedItem /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2656  

#6 0x3c85661 in ?? ??:0  

#7 0x3c7fab0 in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeEnum, float, float, CXFA\_LayoutContext\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:1951  

#8 0x3c7fab0 in ?? ??:0  

#9 0x3c718f1 in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2217  

#10 0x3c718f1 in ?? ??:0  

#11 0x3c8d4d6 in CXFA\_LayoutProcessor::DoLayout() /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../xfa/fxfa/parser/cxfa\_layoutprocessor.cpp:74  

#12 0x3c8d4d6 in ?? ??:0  

#13 0x38d12a1 in CXFA\_FFDocView::DoLayout() /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../xfa/fxfa/cxfa\_ffdocview.cpp:94  

#14 0x38d12a1 in ?? ??:0  

#15 0x37bcb51 in CPDFXFA\_Context::LoadXFADoc() /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../fpdfsdk/fpdfxfa/cpdfxfa\_context.cpp:118  

#16 0x37bcb51 in ?? ??:0  

#17 0x2987fcd in FPDF\_LoadXFA /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../fpdfsdk/fpdf\_view.cpp:259  

#18 0x2987fcd in ?? ??:0  

#19 0xbb7366 in RenderPdf /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../samples/pdfium\_test.cc:709  

#20 0xbb7366 in main /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../samples/pdfium\_test.cc:911  

#21 0xbb7366 in ?? ??:0  

#22 0x7ffff6c0e82f in \_\_libc\_start\_main /build/glibc-Cl5G7W/glibc-2.23/csu/../csu/libc-start.c:291  

#23 0x7ffff6c0e82f in ?? ??:0

0x61d00005ce54 is located 1492 bytes inside of 2048-byte region [0x61d00005c880,0x61d00005d080)  

allocated by thread T0 here:  

#0 0xbaf362 in operator new(unsigned long) *asan\_rtl*  

#1 0xbaf362 in ?? ??:0  

#2 0x29764ba in \_\_libcpp\_allocate /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../buildtools/third\_party/libc++/trunk/include/new:259  

#3 0x29764ba in allocate /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../buildtools/third\_party/libc++/trunk/include/memory:1799  

#4 0x29764ba in allocate /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../buildtools/third\_party/libc++/trunk/include/memory:1548  

#5 0x29764ba in \_\_split\_buffer /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../buildtools/third\_party/libc++/trunk/include/\_\_split\_buffer:311  

#6 0x29764ba in \_\_push\_back\_slow\_path<float> /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../buildtools/third\_party/libc++/trunk/include/vector:1578  

#7 0x29764ba in ?? ??:0  

#8 0x3ce6f2b in push\_back /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../buildtools/third\_party/libc++/trunk/include/vector:1619  

#9 0x3ce6f2b in CXFA\_Node::FindSplitPos(CXFA\_FFDocView\*, int, float&) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../xfa/fxfa/parser/cxfa\_node.cpp:3302  

#10 0x3ce6f2b in ?? ??:0  

#11 0x3c6c34b in (anonymous namespace)::FindLayoutItemSplitPos(CXFA\_ContentLayoutItem\*, float, float\*, bool\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:496  

#12 0x3c6c34b in ?? ??:0  

#13 0x3c85661 in FindSplitPos /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:667  

#14 0x3c85661 in InsertFlowedItem /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2656  

#15 0x3c85661 in ?? ??:0  

#16 0x3c7fab0 in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeEnum, float, float, CXFA\_LayoutContext\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:1951  

#17 0x3c7fab0 in ?? ??:0  

#18 0x3c718f1 in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2217  

#19 0x3c718f1 in ?? ??:0  

#20 0x3c8d4d6 in CXFA\_LayoutProcessor::DoLayout() /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../xfa/fxfa/parser/cxfa\_layoutprocessor.cpp:74  

#21 0x3c8d4d6 in ?? ??:0  

#22 0x38d12a1 in CXFA\_FFDocView::DoLayout() /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../xfa/fxfa/cxfa\_ffdocview.cpp:94  

#23 0x38d12a1 in ?? ??:0  

#24 0x37bcb51 in CPDFXFA\_Context::LoadXFADoc() /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../fpdfsdk/fpdfxfa/cpdfxfa\_context.cpp:118  

#25 0x37bcb51 in ?? ??:0  

#26 0x2987fcd in FPDF\_LoadXFA /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../fpdfsdk/fpdf\_view.cpp:259  

#27 0x2987fcd in ?? ??:0  

#28 0xbb7366 in RenderPdf /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../samples/pdfium\_test.cc:709  

#29 0xbb7366 in main /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/dbg/../../samples/pdfium\_test.cc:911  

#30 0xbb7366 in ?? ??:0  

#31 0x7ffff6c0e82f in \_\_libc\_start\_main /build/glibc-Cl5G7W/glibc-2.23/csu/../csu/libc-start.c:291  

#32 0x7ffff6c0e82f in ?? ??:0

HINT: if you don't care about these errors you may set ASAN\_OPTIONS=detect\_container\_overflow=0.  

If you suspect a false positive see also: <https://github.com/google/sanitizers/wiki/AddressSanitizerContainerOverflow>.  

SUMMARY: AddressSanitizer: container-overflow (/workarea/fuzz/bin/pdfium\_asan/pdfium\_test+0x3ce839f)  

Shadow bytes around the buggy address:  

0x0c3a80003970: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c3a80003980: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c3a80003990: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c3a800039a0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c3a800039b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x0c3a800039c0: 00 00 00 00 00 00 00 00 00 00[fc]fc fc fc fc fc  

0x0c3a800039d0: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc  

0x0c3a800039e0: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc  

0x0c3a800039f0: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc  

0x0c3a80003a00: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc  

0x0c3a80003a10: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

==31009==ABORTING

## Attachments

- [findsplitpos_container_overflow.sample](attachments/findsplitpos_container_overflow.sample) (application/octet-stream, 74.2 KB)
- [findsplitpos_container_overflow.asan](attachments/findsplitpos_container_overflow.asan) (application/octet-stream, 8.1 KB)

## Timeline

### el...@chromium.org (2018-04-27)

Another issue in XFA code, which isn't enabled for Chrome. Please assign as appropriate. Thanks!

[Monorail components: Internals>Plugins>PDF]

### ds...@chromium.org (2018-04-30)

[Empty comment from Monorail migration]

### ts...@chromium.org (2018-05-02)

[Empty comment from Monorail migration]

### ds...@chromium.org (2018-05-03)

[Empty comment from Monorail migration]

### ds...@chromium.org (2018-05-03)

https://pdfium-review.googlesource.com/c/pdfium/+/32051

### bu...@chromium.org (2018-05-03)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/c5c0eebe863bb4fad86b43f62fa81d89f07c9011

commit c5c0eebe863bb4fad86b43f62fa81d89f07c9011
Author: Dan Sinclair <dsinclair@chromium.org>
Date: Thu May 03 18:20:53 2018

[xfa] Verify field count before accessing

When processing items for layout it's possible for the iBlockIndex*3
value could be larger then the field split count. If this is the case
we'll walk off the end of the split array.

This CL verifys that we have enough data before attempting to walk the
splits and returns early if we don't have enough data.

Bug: chromium:837585
Change-Id: I534298b4ee354ce079442d893202f811431155a0
Reviewed-on: https://pdfium-review.googlesource.com/32051
Commit-Queue: Ryan Harrison <rharrison@chromium.org>
Reviewed-by: Ryan Harrison <rharrison@chromium.org>

[modify] https://crrev.com/c5c0eebe863bb4fad86b43f62fa81d89f07c9011/xfa/fxfa/parser/cxfa_node.cpp


### ds...@chromium.org (2018-05-03)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-05-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5cee59c3852ed3c5e078ae0c23fce23a77983bcb

commit 5cee59c3852ed3c5e078ae0c23fce23a77983bcb
Author: pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Fri May 04 01:01:19 2018

Roll src/third_party/pdfium/ 525147a1f..ad1788557 (5 commits)

https://pdfium.googlesource.com/pdfium.git/+log/525147a1f6d6..ad178855775d

$ git log 525147a1f..ad1788557 --date=short --no-merges --format='%ad %ae %s'
2018-05-03 rharrison Invalidate GIF input buffer when moving file cursor backwards
2018-05-03 tsepez Prove that the memory was good at FPDFBitmap_CreateEx() create time.
2018-05-03 hnakashima Use pointers instead of refs in CXFA_TextLayout params.
2018-05-03 dsinclair [xfa] Verify we can get a font manager before setting up XFA
2018-05-03 dsinclair [xfa] Verify field count before accessing

Created with:
  roll-dep src/third_party/pdfium
BUG=chromium:839348,chromium:839361,chromium:838886,chromium:835693,chromium:837585


The AutoRoll server is located here: https://pdfium-roll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.


TBR=dsinclair@chromium.org

Change-Id: I06ec60f0a34b13f864be053ffe512402c4c8ad7a
Reviewed-on: https://chromium-review.googlesource.com/1043278
Reviewed-by: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Commit-Queue: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#555941}
[modify] https://crrev.com/5cee59c3852ed3c5e078ae0c23fce23a77983bcb/DEPS


### sh...@chromium.org (2018-05-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-11-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-11-12)

Hi christian.jalio@ - Many thanks for the report. The Chrome VRP panel decided to award $1,000 for this report. A member of our finance team will be in touch to arrange payment. Also, how would you like to be credited in Chrome release notes?

### aw...@google.com (2018-11-12)

[Empty comment from Monorail migration]

### aw...@google.com (2018-11-12)

[Empty comment from Monorail migration]

### ch...@gmail.com (2018-11-13)

awhalley: This is a pleasant surprise. Yes, we'd like to be credited: Antti Levomäki and Christian Jalio from Forcepoint. Thanks.

### is...@google.com (2018-11-13)

This issue was migrated from crbug.com/chromium/837585?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/62400]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091238)*
