# pdfium (XFA): heap-use-after-free in CFX_ReadOnlyMemoryStream::ReadBlockAtOffset

| Field | Value |
|-------|-------|
| **Issue ID** | [40094181](https://issues.chromium.org/issues/40094181) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Reporter** | pd...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-03-01 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.124 Safari/537.36

Steps to reproduce the problem:
==1336==ERROR: AddressSanitizer: heap-use-after-free on address 0x60c00000ab58 at pc 0x55de0d710989 bp 0x7ffe786d52d0 sp 0x7ffe786d4a80
READ of size 100 at 0x60c00000ab58 thread T0
SCARINESS: 54 (multi-byte-read-heap-use-after-free)

    #1 0x55de0d7cc576 in CFX_ReadOnlyMemoryStream::ReadBlockAtOffset(void*, long, unsigned long) core/fxcrt/cfx_readonlymemorystream.cpp:40:3
    #2 0x55de0f4bec25 in CCodec_ProgressiveDecoder::DetectImageType(FXCODEC_IMAGE_TYPE, CFX_DIBAttribute*) core/fxcodec/codec/ccodec_progressivedecoder.cpp:1553:17
    #3 0x55de0f4bfc5c in CCodec_ProgressiveDecoder::LoadImageInfo(fxcrt::RetainPtr<IFX_SeekableReadStream> const&, FXCODEC_IMAGE_TYPE, CFX_DIBAttribute*, bool) core/fxcodec/codec/ccodec_progressivedecoder.cpp:1673:9
    #4 0x55de0fa5e423 in XFA_LoadImageFromBuffer(fxcrt::RetainPtr<IFX_SeekableReadStream> const&, FXCODEC_IMAGE_TYPE, int&, int&) xfa/fxfa/cxfa_ffwidget.cpp:162:24
    #5 0x55de0fc78cb5 in (anonymous namespace)::XFA_LoadImageData(CXFA_FFDoc*, CXFA_Image*, bool&, int&, int&) xfa/fxfa/parser/cxfa_node.cpp:521:7
    #6 0x55de0fbfe778 in CXFA_ImageLayoutData::LoadImageData(CXFA_FFDoc*, CXFA_Node*) xfa/fxfa/parser/cxfa_node.cpp:754:26
    #7 0x55de0fbfbee0 in CXFA_Node::CalculateImageAutoSize(CXFA_FFDoc*, CFX_STemplate<float>*) xfa/fxfa/parser/cxfa_node.cpp:3254:5
    #8 0x55de0fc02608 in CXFA_Node::CalculateAccWidthAndHeight(CXFA_FFDoc*, float) xfa/fxfa/parser/cxfa_node.cpp:3421:7
    #9 0x55de0fc00330 in CXFA_Node::StartWidgetLayout(CXFA_FFDoc*, float*, float*) xfa/fxfa/parser/cxfa_node.cpp:3387:24
    #10 0x55de109e7cb2 in CXFA_ItemLayoutProcessor::DoLayoutField() xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:2107:12
    #11 0x55de109c7229 in CXFA_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA_LayoutContext*) xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:2153:7
    #12 0x55de109e0023 in CXFA_ItemLayoutProcessor::InsertFlowedItem(CXFA_ItemLayoutProcessor*, bool, bool, float, XFA_AttributeValue, unsigned char*, std::__1::vector<CXFA_ContentLayoutItem*, std::__1::allocator<CXFA_ContentLayoutItem*> > (&) [3], bool, float, float, float, float*, float*, float*, bool*, bool*, CXFA_LayoutContext*, bool) xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:2435:29
    #13 0x55de109da98f in CXFA_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA_AttributeValue, float, float, CXFA_LayoutContext*, bool) xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:1870:46
    #14 0x55de109c721c in CXFA_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA_LayoutContext*) xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:2135:18
    #15 0x55de10a05f4b in CXFA_LayoutProcessor::DoLayout() xfa/fxfa/layout/cxfa_layoutprocessor.cpp:74:43
    #16 0x55de0fa620f7 in CXFA_FFDocView::DoLayout() xfa/fxfa/cxfa_ffdocview.cpp:96:30
    #17 0x55de0f9a3ff1 in CPDFXFA_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:135:18
    #18 0x55de0eff0dfa in FPDF_LoadXFA fpdfsdk/fpdf_view.cpp:255:32
    #19 0x55de0d745586 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:798:12
    #20 0x55de0d741cea in main samples/pdfium_test.cc:1013:5

0x60c00000ab58 is located 24 bytes inside of 128-byte region [0x60c00000ab40,0x60c00000abc0)
freed by thread T0 here:

    #1 0x55de0fc78a33 in (anonymous namespace)::XFA_LoadImageData(CXFA_FFDoc*, CXFA_Image*, bool&, int&, int&) xfa/fxfa/parser/cxfa_node.cpp:500:7
    #2 0x55de0fbfe778 in CXFA_ImageLayoutData::LoadImageData(CXFA_FFDoc*, CXFA_Node*) xfa/fxfa/parser/cxfa_node.cpp:754:26
    #3 0x55de0fbfbee0 in CXFA_Node::CalculateImageAutoSize(CXFA_FFDoc*, CFX_STemplate<float>*) xfa/fxfa/parser/cxfa_node.cpp:3254:5
    #4 0x55de0fc02608 in CXFA_Node::CalculateAccWidthAndHeight(CXFA_FFDoc*, float) xfa/fxfa/parser/cxfa_node.cpp:3421:7
    #5 0x55de0fc00330 in CXFA_Node::StartWidgetLayout(CXFA_FFDoc*, float*, float*) xfa/fxfa/parser/cxfa_node.cpp:3387:24
    #6 0x55de109e7cb2 in CXFA_ItemLayoutProcessor::DoLayoutField() xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:2107:12
    #7 0x55de109c7229 in CXFA_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA_LayoutContext*) xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:2153:7
    #8 0x55de109e0023 in CXFA_ItemLayoutProcessor::InsertFlowedItem(CXFA_ItemLayoutProcessor*, bool, bool, float, XFA_AttributeValue, unsigned char*, std::__1::vector<CXFA_ContentLayoutItem*, std::__1::allocator<CXFA_ContentLayoutItem*> > (&) [3], bool, float, float, float, float*, float*, float*, bool*, bool*, CXFA_LayoutContext*, bool) xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:2435:29
    #9 0x55de109da98f in CXFA_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA_AttributeValue, float, float, CXFA_LayoutContext*, bool) xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:1870:46
    #10 0x55de109c721c in CXFA_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA_LayoutContext*) xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:2135:18
    #11 0x55de10a05f4b in CXFA_LayoutProcessor::DoLayout() xfa/fxfa/layout/cxfa_layoutprocessor.cpp:74:43
    #12 0x55de0fa620f7 in CXFA_FFDocView::DoLayout() xfa/fxfa/cxfa_ffdocview.cpp:96:30
    #13 0x55de0f9a3ff1 in CPDFXFA_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:135:18
    #14 0x55de0eff0dfa in FPDF_LoadXFA fpdfsdk/fpdf_view.cpp:255:32
    #15 0x55de0d745586 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:798:12
    #16 0x55de0d741cea in main samples/pdfium_test.cc:1013:5

previously allocated by thread T0 here:

    #1 0x55de0d7bd6d4 in PartitionAllocGenericFlags third_party/base/allocator/partition_allocator/partition_alloc.h:363:48
    #2 0x55de0d7bd6d4 in Alloc third_party/base/allocator/partition_allocator/partition_alloc.h:384
    #3 0x55de0d7bd6d4 in fxcrt::StringDataTemplate<char>::Create(unsigned long) core/fxcrt/string_data_template.h:39
    #4 0x55de0d7c0b0f in fxcrt::ByteString::GetBuffer(unsigned long) core/fxcrt/bytestring.cpp:403:19
    #5 0x55de0d7e9a01 in fxcrt::WideString::ToDefANSI() const core/fxcrt/widestring.cpp:665:40
    #6 0x55de0fc789e4 in (anonymous namespace)::XFA_LoadImageData(CXFA_FFDoc*, CXFA_Image*, bool&, int&, int&) xfa/fxfa/parser/cxfa_node.cpp:501:19
    #7 0x55de0fbfe778 in CXFA_ImageLayoutData::LoadImageData(CXFA_FFDoc*, CXFA_Node*) xfa/fxfa/parser/cxfa_node.cpp:754:26
    #8 0x55de0fbfbee0 in CXFA_Node::CalculateImageAutoSize(CXFA_FFDoc*, CFX_STemplate<float>*) xfa/fxfa/parser/cxfa_node.cpp:3254:5
    #9 0x55de0fc02608 in CXFA_Node::CalculateAccWidthAndHeight(CXFA_FFDoc*, float) xfa/fxfa/parser/cxfa_node.cpp:3421:7
    #10 0x55de0fc00330 in CXFA_Node::StartWidgetLayout(CXFA_FFDoc*, float*, float*) xfa/fxfa/parser/cxfa_node.cpp:3387:24
    #11 0x55de109e7cb2 in CXFA_ItemLayoutProcessor::DoLayoutField() xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:2107:12
    #12 0x55de109c7229 in CXFA_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA_LayoutContext*) xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:2153:7
    #13 0x55de109e0023 in CXFA_ItemLayoutProcessor::InsertFlowedItem(CXFA_ItemLayoutProcessor*, bool, bool, float, XFA_AttributeValue, unsigned char*, std::__1::vector<CXFA_ContentLayoutItem*, std::__1::allocator<CXFA_ContentLayoutItem*> > (&) [3], bool, float, float, float, float*, float*, float*, bool*, bool*, CXFA_LayoutContext*, bool) xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:2435:29
    #14 0x55de109da98f in CXFA_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA_AttributeValue, float, float, CXFA_LayoutContext*, bool) xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:1870:46
    #15 0x55de109c721c in CXFA_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA_LayoutContext*) xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp:2135:18
    #16 0x55de10a05f4b in CXFA_LayoutProcessor::DoLayout() xfa/fxfa/layout/cxfa_layoutprocessor.cpp:74:43
    #17 0x55de0fa620f7 in CXFA_FFDocView::DoLayout() xfa/fxfa/cxfa_ffdocview.cpp:96:30
    #18 0x55de0f9a3ff1 in CPDFXFA_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:135:18
    #19 0x55de0eff0dfa in FPDF_LoadXFA fpdfsdk/fpdf_view.cpp:255:32
    #20 0x55de0d745586 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:798:12
    #21 0x55de0d741cea in main samples/pdfium_test.cc:1013:5

Shadow bytes around the buggy address:
  0x0c187fff9510: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x0c187fff9520: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c187fff9530: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c187fff9540: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x0c187fff9550: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c187fff9560: fa fa fa fa fa fa fa fa fd fd fd[fd]fd fd fd fd
  0x0c187fff9570: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x0c187fff9580: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c187fff9590: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c187fff95a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c187fff95b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
  Shadow gap:              cc

What is the expected behavior?

What went wrong?
^

Did this work before? No 

Chrome version: 70.0.3538.124  Channel: n/a
OS Version: 
Flash Version:

## Attachments

- [chromium-937199.pdf](attachments/chromium-937199.pdf) (application/pdf, 573 B)

## Timeline

### pd...@gmail.com (2019-03-01)

Add more bytes to the image to increase the READ.

### rs...@chromium.org (2019-03-02)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2019-03-06)

Gah, my own blunder while eliminating "redundant" locals. CL at https://pdfium-review.googlesource.com/c/pdfium/+/51590

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-06)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/3df5c7cf7b585025bee1f5e30918dd475e5f4363

commit 3df5c7cf7b585025bee1f5e30918dd475e5f4363
Author: Tom Sepez <tsepez@chromium.org>
Date: Wed Mar 06 18:45:55 2019

Fix temporary going out of scope too early in XFA_LoadImageData()

Bug: chromium:937199
Change-Id: Id65195d32ecbd69b523552251b822d0367489ce8
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/51590
Reviewed-by: Henrique Nakashima <hnakashima@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://crrev.com/3df5c7cf7b585025bee1f5e30918dd475e5f4363/xfa/fxfa/parser/cxfa_node.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f650c896e9f94fa43e90c0f6b4445e45b1ad7845

commit f650c896e9f94fa43e90c0f6b4445e45b1ad7845
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Mar 06 21:50:00 2019

Roll src/third_party/pdfium 9ba187ae4751..3df5c7cf7b58 (1 commits)

https://pdfium.googlesource.com/pdfium.git/+log/9ba187ae4751..3df5c7cf7b58


git log 9ba187ae4751..3df5c7cf7b58 --date=short --no-merges --format='%ad %ae %s'
2019-03-06 tsepez@chromium.org Fix temporary going out of scope too early in XFA_LoadImageData()


Created with:
  gclient setdep -r src/third_party/pdfium@3df5c7cf7b58

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:937199
TBR=dsinclair@chromium.org

Change-Id: I89e3c61b3e366e54de2f5ef32bc6b18d1d339ce2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1506476
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#638291}
[modify] https://crrev.com/f650c896e9f94fa43e90c0f6b4445e45b1ad7845/DEPS


### ts...@chromium.org (2019-03-11)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-12)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-03-14)

Congrats! The Panel decided to reward $1,000 for this report :) 

### aw...@google.com (2019-03-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-06-18)

This issue was migrated from crbug.com/chromium/937199?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094181)*
