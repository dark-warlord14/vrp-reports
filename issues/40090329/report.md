# Security: global-buffer-overflow in CFX_GetCSSPropertyByName

| Field | Value |
|-------|-------|
| **Issue ID** | [40090329](https://issues.chromium.org/issues/40090329) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | zh...@gmail.com |
| **Assignee** | rh...@chromium.org |
| **Created** | 2018-01-30 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

This issue was found by fuzzing against a 64-bit asan linux build of pdfium\_test with XFA enabled.

**VERSION**  

Operating System: Fedora 27 x86\_64

**REPRODUCTION CASE**

Get the latest chromium source code, build pdfium\_test with the following args.gn (command: ninja -C out/default pdfium\_test)

---

## enable\_nacl=false is\_debug=false is\_asan=true pdf\_use\_skia = false pdf\_use\_skia\_paths = false pdf\_enable\_xfa = true pdf\_enable\_v8 = true pdf\_enable\_xfa\_bmp = true pdf\_enable\_xfa\_gif = true pdf\_enable\_xfa\_png = true pdf\_enable\_xfa\_tiff = true symbol\_level=2

./pdfium\_test /tmp/pdf\_crashes/global-buffer-overflow-poc

# Rendering PDF file /tmp/pdf\_crashes/global-buffer-overflow-poc.

==10316==ERROR: AddressSanitizer: global-buffer-overflow on address 0x000003aa70b0 at pc 0x00000353bd0e bp 0x7ffd2637fd70 sp 0x7ffd2637fd68  

READ of size 4 at 0x000003aa70b0 thread T0  

#0 0x353bd0d in CFX\_GetCSSPropertyByName(fxcrt::StringViewTemplate<wchar\_t> const&) third\_party/pdfium/core/fxcrt/css/cfx\_cssdatatable.cpp:133:39  

#1 0x354f152 in CFX\_CSSStyleSelector::AppendInlineStyle(CFX\_CSSDeclaration\*, fxcrt::WideString const&) third\_party/pdfium/core/fxcrt/css/cfx\_cssstyleselector.cpp:152:15  

#2 0x354eccc in CFX\_CSSStyleSelector::ComputeStyle(std::\_\_1::vector<CFX\_CSSDeclaration const\*, std::\_\_1::allocator<CFX\_CSSDeclaration const\*> > const&, fxcrt::WideString const&, fxcrt::WideString const&, CFX\_CSSComputedStyle\*) third\_party/pdfium/core/fxcrt/css/cfx\_cssstyleselector.cpp:91:7  

#3 0x35361f1 in CXFA\_TextParser::ParseRichText(CFX\_XMLNode\*, CFX\_CSSComputedStyle\*) third\_party/pdfium/xfa/fxfa/cxfa\_textparser.cpp:235:20  

#4 0x353674d in CXFA\_TextParser::ParseRichText(CFX\_XMLNode\*, CFX\_CSSComputedStyle\*) third\_party/pdfium/xfa/fxfa/cxfa\_textparser.cpp:251:5  

#5 0x3535c76 in CXFA\_TextParser::DoParse(CFX\_XMLNode\*, CXFA\_TextProvider\*) third\_party/pdfium/xfa/fxfa/cxfa\_textparser.cpp:214:3  

#6 0x351bddb in CXFA\_TextLayout::Loader(float, float&, bool) third\_party/pdfium/xfa/fxfa/cxfa\_textlayout.cpp:639:22  

#7 0x35193c4 in CXFA\_TextLayout::CalcSize(CFX\_STemplate<float> const&, CFX\_STemplate<float> const&) third\_party/pdfium/xfa/fxfa/cxfa\_textlayout.cpp:392:3  

#8 0x3519a15 in CXFA\_TextLayout::StartLayout(float) third\_party/pdfium/xfa/fxfa/cxfa\_textlayout.cpp:294:21  

#9 0x362a2f9 in CXFA\_Node::StartTextLayout(CXFA\_FFDoc\*, float&, float&) third\_party/pdfium/xfa/fxfa/parser/cxfa\_node.cpp:3449:63  

#10 0x362965c in CXFA\_Node::StartWidgetLayout(CXFA\_FFDoc\*, float&, float&) third\_party/pdfium/xfa/fxfa/parser/cxfa\_node.cpp:3080:5  

#11 0x35e4081 in CXFA\_ItemLayoutProcessor::DoLayoutField() third\_party/pdfium/xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2757:12  

#12 0x35cc6ff in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) third\_party/pdfium/xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2802:7  

#13 0x35cdaf5 in CXFA\_ItemLayoutProcessor::DoLayoutPositionedContainer(CXFA\_LayoutContext\*) third\_party/pdfium/xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:1711:17  

#14 0x35cc7ff in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) third\_party/pdfium/xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2791:11  

#15 0x35cdaf5 in CXFA\_ItemLayoutProcessor::DoLayoutPositionedContainer(CXFA\_LayoutContext\*) third\_party/pdfium/xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:1711:17  

#16 0x35cc7ff in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) third\_party/pdfium/xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2791:11  

#17 0x35ddd32 in (anonymous namespace)::InsertFlowedItem(CXFA\_ItemLayoutProcessor\*, CXFA\_ItemLayoutProcessor\*, bool, bool, float, XFA\_AttributeEnum, unsigned char\*, std::\_\_1::vector<CXFA\_ContentLayoutItem\*, std::\_\_1::allocator<CXFA\_ContentLayoutItem\*> > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_LayoutContext\*, bool) third\_party/pdfium/xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:715:29  

#18 0x35d9fa1 in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeEnum, float, float, CXFA\_LayoutContext\*, bool) third\_party/pdfium/xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2510:46  

#19 0x35cc8b5 in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) third\_party/pdfium/xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2784:18  

#20 0x35e5e9a in CXFA\_LayoutProcessor::DoLayout() third\_party/pdfium/xfa/fxfa/parser/cxfa\_layoutprocessor.cpp:74:43  

#21 0x32c8224 in CXFA\_FFDocView::DoLayout() third\_party/pdfium/xfa/fxfa/cxfa\_ffdocview.cpp:94:30  

#22 0x31cfffe in CPDFXFA\_Context::LoadXFADoc() third\_party/pdfium/fpdfsdk/fpdfxfa/cpdfxfa\_context.cpp:121:18  

#23 0x270393d in FPDF\_LoadXFA third\_party/pdfium/fpdfsdk/fpdfview.cpp:599:63  

#24 0xbd7725 in (anonymous namespace)::RenderPdf(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, char const\*, unsigned long, (anonymous namespace)::Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) third\_party/pdfium/samples/pdfium\_test.cc:1435:10  

#25 0xbd4ec8 in main third\_party/pdfium/samples/pdfium\_test.cc:1630:5  

#26 0x7f3c3bb35009 in \_\_libc\_start\_main (/lib64/libc.so.6+0x21009)

0x000003aa70b0 is located 16 bytes to the right of global variable 'g\_CFX\_CSSProperties' defined in '../../third\_party/pdfium/core/fxcrt/css/cfx\_cssdatatable.cpp:16:35' (0x3aa6ce0) of size 960  

SUMMARY: AddressSanitizer: global-buffer-overflow third\_party/pdfium/core/fxcrt/css/cfx\_cssdatatable.cpp:133:39 in CFX\_GetCSSPropertyByName(fxcrt::StringViewTemplate<wchar\_t> const&)  

Shadow bytes around the buggy address:  

0x00008074cdc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x00008074cdd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x00008074cde0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x00008074cdf0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x00008074ce00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x00008074ce10: 00 00 00 00 f9 f9[f9]f9 f9 f9 f9 f9 f9 f9 f9 f9  

0x00008074ce20: f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9  

0x00008074ce30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x00008074ce40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x00008074ce50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x00008074ce60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

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

==10316==ABORTING

Testcase is in the attachment.

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### el...@chromium.org (2018-01-30)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### ds...@chromium.org (2018-01-30)

[Empty comment from Monorail migration]

### hn...@chromium.org (2018-01-30)

[Empty comment from Monorail migration]

### rh...@chromium.org (2018-01-30)

I have been able to reproduce this locally

### pa...@chromium.org (2018-01-30)

Since we don't ship XFA yet, I wonder if I should mark this Security_Impact-None? tsepez, what do you think?

### ds...@chromium.org (2018-01-30)

That's what we usually do, remove the milestone, set impact to None and leave Severity alone.

### bu...@chromium.org (2018-01-30)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/802eaea7696e2e1aa8d6d76d1fee39fbe1c7794b

commit 802eaea7696e2e1aa8d6d76d1fee39fbe1c7794b
Author: Ryan Harrison <rharrison@chromium.org>
Date: Tue Jan 30 20:24:50 2018

Clean up CSS Data Table entries and access

This cleans up the entries in the table to no longer have a marker for
size, and also removes a hand rolled search. This prevents an out of
bounds issue that had been reported and addresses another potential
out of bounds issue.

BUG=chromium:807214

Change-Id: I3d3ab5a3a174dd4dcec56fa7ee7a0e6c2805bfaa
Reviewed-on: https://pdfium-review.googlesource.com/24690
Reviewed-by: Ryan Harrison <rharrison@chromium.org>
Reviewed-by: dsinclair <dsinclair@chromium.org>
Commit-Queue: dsinclair <dsinclair@chromium.org>
Commit-Queue: Ryan Harrison <rharrison@chromium.org>

[modify] https://crrev.com/802eaea7696e2e1aa8d6d76d1fee39fbe1c7794b/core/fxcrt/css/cfx_css.h
[modify] https://crrev.com/802eaea7696e2e1aa8d6d76d1fee39fbe1c7794b/core/fxcrt/css/cfx_cssdatatable.h
[modify] https://crrev.com/802eaea7696e2e1aa8d6d76d1fee39fbe1c7794b/core/fxcrt/css/cfx_cssdatatable.cpp


### rh...@chromium.org (2018-01-30)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-01-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/18f244635e321ec2e54862186f5727cb29ce8309

commit 18f244635e321ec2e54862186f5727cb29ce8309
Author: pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Wed Jan 31 01:02:34 2018

Roll src/third_party/pdfium/ 1917cdd8c..233466005 (15 commits)

https://pdfium.googlesource.com/pdfium.git/+log/1917cdd8c90b..2334660053e0

$ git log 1917cdd8c..233466005 --date=short --no-merges --format='%ad %ae %s'
2018-01-30 npm Use unsigned for char width
2018-01-30 dsinclair Shuffle more code out of CXFA_Node
2018-01-30 dsinclair Move CheckButton code from CXFA_Node to CXFA_CheckButton
2018-01-30 rharrison Clean up CSS Data Table entries and access
2018-01-30 tsepez Remove bare new from JS_Define.h
2018-01-30 hnakashima Check if opj_image_data_alloc returned null.
2018-01-30 dsinclair Cleanup some param passing code
2018-01-30 hnakashima Guard usages of tellp(). It may return -1 in error cases.
2018-01-30 dsinclair Cleanup duplicate RunScript code
2018-01-30 thestig Remove not reachable branch in fxge code.
2018-01-30 thestig Use anonymous namespace in gdiplus code.
2018-01-30 dsinclair Cleanup some SDK code
2018-01-30 tsepez Revert "Revert "Use UnownedPtr instead of T* in MaybeOwned.""
2018-01-30 tsepez Revert "Use UnownedPtr instead of T* in MaybeOwned."
2018-01-30 tsepez Use UnownedPtr instead of T* in MaybeOwned.

Created with:
  roll-dep src/third_party/pdfium
BUG=807214,805881


The AutoRoll server is located here: https://pdfium-roll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.


TBR=dsinclair@chromium.org

Change-Id: Iccd05c3211b080fc7392a482d0c2be722c1ec683
Reviewed-on: https://chromium-review.googlesource.com/894482
Reviewed-by: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Commit-Queue: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#533128}
[modify] https://crrev.com/18f244635e321ec2e54862186f5727cb29ce8309/DEPS


### sh...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-11-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-11-12)

Hi zhouzhenster@, the VRP panel chose to track this as medium severity, and award $1,000 for the report - thanks!

### aw...@google.com (2018-11-12)

[Empty comment from Monorail migration]

### is...@google.com (2018-11-12)

This issue was migrated from crbug.com/chromium/807214?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/62400]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090329)*
