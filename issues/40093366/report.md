# Security: pdfium heap use after free in cxfa_layoutitem

| Field | Value |
|-------|-------|
| **Issue ID** | [40093366](https://issues.chromium.org/issues/40093366) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2018-12-10 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

pdfium heap use after free in cxfa\_layoutitem (READ of size 8)

**VERSION**  

commit 841c145e2eb1b44fbaf6a0266181e14b75036266  

Date: Sat Dec 8 01:01:57 2018 +0000

**REPRODUCTION CASE**  

Open attached file.

# ADDITIONAL INFORMATION Rendering PDF file /workarea/samplestore/wip/pdfium/victory/victory\_42b261df645ff0840e2392720915bccae701c70b0fe3d3232d28f2d5b0c840bc.

==22170==ERROR: AddressSanitizer: heap-use-after-free on address 0x60c0000326a8 at pc 0x55555930429c bp 0x7fffffffb610 sp 0x7fffffffb608  

READ of size 8 at 0x60c0000326a8 thread T0  

#0 0x55555930429b in Get /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../core/fxcrt/unowned\_ptr.h:91  

#1 0x55555930429b in GetFormNode /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_layoutitem.h:28  

#2 0x55555930429b in CalculateRowChildPosition /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2081  

#3 0x55555930429b in ?? ??:0  

#4 0x5555592f9698 in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_LayoutContext\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2024  

#5 0x5555592f9698 in ?? ??:0  

#6 0x5555592ea643 in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2250  

#7 0x5555592ea643 in ?? ??:0  

#8 0x5555592fe1e2 in CXFA\_ItemLayoutProcessor::InsertFlowedItem(CXFA\_ItemLayoutProcessor\*, bool, bool, float, XFA\_AttributeValue, unsigned char\*, std::\_\_1::vector<CXFA\_ContentLayoutItem\*, std::\_\_1::allocator<CXFA\_ContentLayoutItem\*> > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_LayoutContext\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2552  

#9 0x5555592fe1e2 in ?? ??:0  

#10 0x5555592f91f9 in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_LayoutContext\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:1983  

#11 0x5555592f91f9 in ?? ??:0  

#12 0x5555592ea643 in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2250  

#13 0x5555592ea643 in ?? ??:0  

#14 0x5555592fe1e2 in CXFA\_ItemLayoutProcessor::InsertFlowedItem(CXFA\_ItemLayoutProcessor\*, bool, bool, float, XFA\_AttributeValue, unsigned char\*, std::\_\_1::vector<CXFA\_ContentLayoutItem\*, std::\_\_1::allocator<CXFA\_ContentLayoutItem\*> > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_LayoutContext\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2552  

#15 0x5555592fe1e2 in ?? ??:0  

#16 0x5555592f91f9 in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_LayoutContext\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:1983  

#17 0x5555592f91f9 in ?? ??:0  

#18 0x5555592ea643 in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2250  

#19 0x5555592ea643 in ?? ??:0  

#20 0x5555592fe1e2 in CXFA\_ItemLayoutProcessor::InsertFlowedItem(CXFA\_ItemLayoutProcessor\*, bool, bool, float, XFA\_AttributeValue, unsigned char\*, std::\_\_1::vector<CXFA\_ContentLayoutItem\*, std::\_\_1::allocator<CXFA\_ContentLayoutItem\*> > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_LayoutContext\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2552  

#21 0x5555592fe1e2 in ?? ??:0  

#22 0x5555592f91f9 in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_LayoutContext\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:1983  

#23 0x5555592f91f9 in ?? ??:0  

#24 0x5555592ea643 in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2250  

#25 0x5555592ea643 in ?? ??:0  

#26 0x55555931d72c in CXFA\_LayoutProcessor::DoLayout() /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_layoutprocessor.cpp:74  

#27 0x55555931d72c in ?? ??:0  

#28 0x5555593e0535 in CXFA\_FFDocView::RunLayout() /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_ffdocview.cpp:450  

#29 0x5555593e0535 in ?? ??:0  

#30 0x5555593dfe50 in CXFA\_FFDocView::StopLayout() /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_ffdocview.cpp:132  

#31 0x5555593dfe50 in ?? ??:0  

#32 0x5555594743ec in CPDFXFA\_Context::LoadXFADoc() /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../fpdfsdk/fpdfxfa/cpdfxfa\_context.cpp:137  

#33 0x5555594743ec in ?? ??:0  

#34 0x5555596134c3 in FPDF\_LoadXFA /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../fpdfsdk/fpdf\_view.cpp:255  

#35 0x5555596134c3 in ?? ??:0  

#36 0x55555663c83b in RenderPdf /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../samples/pdfium\_test.cc:790  

#37 0x55555663c83b in main /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../samples/pdfium\_test.cc:1002  

#38 0x55555663c83b in ?? ??:0  

#39 0x7ffff6ee582f in \_\_libc\_start\_main /build/glibc-Cl5G7W/glibc-2.23/csu/../csu/libc-start.c:291  

#40 0x7ffff6ee582f in ?? ??:0

0x60c0000326a8 is located 40 bytes inside of 128-byte region [0x60c000032680,0x60c000032700)  

freed by thread T0 here:  

#0 0x555556634852 in operator delete(void\*) *asan\_rtl*  

#1 0x555556634852 in ?? ??:0  

#2 0x5555592e72ef in CXFA\_ItemLayoutProcessor::ExtractLayoutItem() /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:844  

#3 0x5555592e72ef in ?? ??:0  

#4 0x5555592fef75 in CXFA\_ItemLayoutProcessor::InsertFlowedItem(CXFA\_ItemLayoutProcessor\*, bool, bool, float, XFA\_AttributeValue, unsigned char\*, std::\_\_1::vector<CXFA\_ContentLayoutItem\*, std::\_\_1::allocator<CXFA\_ContentLayoutItem\*> > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_LayoutContext\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2641  

#5 0x5555592fef75 in ?? ??:0  

#6 0x5555592f91f9 in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_LayoutContext\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:1983  

#7 0x5555592f91f9 in ?? ??:0  

#8 0x5555592ea643 in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2250  

#9 0x5555592ea643 in ?? ??:0  

#10 0x5555592fe1e2 in CXFA\_ItemLayoutProcessor::InsertFlowedItem(CXFA\_ItemLayoutProcessor\*, bool, bool, float, XFA\_AttributeValue, unsigned char\*, std::\_\_1::vector<CXFA\_ContentLayoutItem\*, std::\_\_1::allocator<CXFA\_ContentLayoutItem\*> > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_LayoutContext\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2552  

#11 0x5555592fe1e2 in ?? ??:0  

#12 0x5555592f91f9 in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_LayoutContext\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:1983  

#13 0x5555592f91f9 in ?? ??:0  

#14 0x5555592ea643 in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2250  

#15 0x5555592ea643 in ?? ??:0  

#16 0x5555592fe1e2 in CXFA\_ItemLayoutProcessor::InsertFlowedItem(CXFA\_ItemLayoutProcessor\*, bool, bool, float, XFA\_AttributeValue, unsigned char\*, std::\_\_1::vector<CXFA\_ContentLayoutItem\*, std::\_\_1::allocator<CXFA\_ContentLayoutItem\*> > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_LayoutContext\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2552  

#17 0x5555592fe1e2 in ?? ??:0  

#18 0x5555592f91f9 in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_LayoutContext\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:1983  

#19 0x5555592f91f9 in ?? ??:0  

#20 0x5555592ea643 in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2250  

#21 0x5555592ea643 in ?? ??:0  

#22 0x5555592fe1e2 in CXFA\_ItemLayoutProcessor::InsertFlowedItem(CXFA\_ItemLayoutProcessor\*, bool, bool, float, XFA\_AttributeValue, unsigned char\*, std::\_\_1::vector<CXFA\_ContentLayoutItem\*, std::\_\_1::allocator<CXFA\_ContentLayoutItem\*> > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_LayoutContext\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2552  

#23 0x5555592fe1e2 in ?? ??:0  

#24 0x5555592f91f9 in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_LayoutContext\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:1983  

#25 0x5555592f91f9 in ?? ??:0  

#26 0x5555592ea643 in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2250  

#27 0x5555592ea643 in ?? ??:0  

#28 0x55555931d72c in CXFA\_LayoutProcessor::DoLayout() /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_layoutprocessor.cpp:74  

#29 0x55555931d72c in ?? ??:0  

#30 0x5555593e0535 in CXFA\_FFDocView::RunLayout() /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_ffdocview.cpp:450  

#31 0x5555593e0535 in ?? ??:0  

#32 0x5555593dfe50 in CXFA\_FFDocView::StopLayout() /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_ffdocview.cpp:132  

#33 0x5555593dfe50 in ?? ??:0  

#34 0x5555594743ec in CPDFXFA\_Context::LoadXFADoc() /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../fpdfsdk/fpdfxfa/cpdfxfa\_context.cpp:137  

#35 0x5555594743ec in ?? ??:0  

#36 0x5555596134c3 in FPDF\_LoadXFA /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../fpdfsdk/fpdf\_view.cpp:255  

#37 0x5555596134c3 in ?? ??:0  

#38 0x55555663c83b in RenderPdf /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../samples/pdfium\_test.cc:790  

#39 0x55555663c83b in main /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../samples/pdfium\_test.cc:1002  

#40 0x55555663c83b in ?? ??:0  

#41 0x7ffff6ee582f in \_\_libc\_start\_main /build/glibc-Cl5G7W/glibc-2.23/csu/../csu/libc-start.c:291  

#42 0x7ffff6ee582f in ?? ??:0

previously allocated by thread T0 here:  

#0 0x555556633c12 in operator new(unsigned long) *asan\_rtl*  

#1 0x555556633c12 in ?? ??:0  

#2 0x5555593fa2f1 in MakeUnique<CXFA\_FFWidget, CXFA\_Node \*&> /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../third\_party/base/ptr\_util.h:56  

#3 0x5555593fa2f1 in OnCreateContentLayoutItem /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_ffnotify.cpp:190  

#4 0x5555593fa2f1 in ?? ??:0  

#5 0x5555592e57b3 in CreateContentLayoutItem /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:657  

#6 0x5555592e57b3 in SplitLayoutItem /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:721  

#7 0x5555592e57b3 in ?? ??:0  

#8 0x5555592e6050 in CXFA\_ItemLayoutProcessor::SplitLayoutItem(CXFA\_ContentLayoutItem\*, CXFA\_ContentLayoutItem\*, float) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:805  

#9 0x5555592e6050 in ?? ??:0  

#10 0x5555592e6050 in CXFA\_ItemLayoutProcessor::SplitLayoutItem(CXFA\_ContentLayoutItem\*, CXFA\_ContentLayoutItem\*, float) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:805  

#11 0x5555592e6050 in ?? ??:0  

#12 0x555559300245 in SplitLayoutItem /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:815  

#13 0x555559300245 in CXFA\_ItemLayoutProcessor::InsertFlowedItem(CXFA\_ItemLayoutProcessor\*, bool, bool, float, XFA\_AttributeValue, unsigned char\*, std::\_\_1::vector<CXFA\_ContentLayoutItem\*, std::\_\_1::allocator<CXFA\_ContentLayoutItem\*> > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_LayoutContext\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2723  

#14 0x555559300245 in ?? ??:0  

#15 0x5555592f91f9 in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_LayoutContext\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:1983  

#16 0x5555592f91f9 in ?? ??:0  

#17 0x5555592ea643 in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2250  

#18 0x5555592ea643 in ?? ??:0  

#19 0x5555592fe1e2 in CXFA\_ItemLayoutProcessor::InsertFlowedItem(CXFA\_ItemLayoutProcessor\*, bool, bool, float, XFA\_AttributeValue, unsigned char\*, std::\_\_1::vector<CXFA\_ContentLayoutItem\*, std::\_\_1::allocator<CXFA\_ContentLayoutItem\*> > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_LayoutContext\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2552  

#20 0x5555592fe1e2 in ?? ??:0  

#21 0x5555592f91f9 in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_LayoutContext\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:1983  

#22 0x5555592f91f9 in ?? ??:0  

#23 0x5555592ea643 in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2250  

#24 0x5555592ea643 in ?? ??:0  

#25 0x55555931d72c in CXFA\_LayoutProcessor::DoLayout() /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_layoutprocessor.cpp:74  

#26 0x55555931d72c in ?? ??:0  

#27 0x5555593e0535 in CXFA\_FFDocView::RunLayout() /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_ffdocview.cpp:450  

#28 0x5555593e0535 in ?? ??:0  

#29 0x5555593dfe50 in CXFA\_FFDocView::StopLayout() /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_ffdocview.cpp:132  

#30 0x5555593dfe50 in ?? ??:0  

#31 0x5555594743ec in CPDFXFA\_Context::LoadXFADoc() /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../fpdfsdk/fpdfxfa/cpdfxfa\_context.cpp:137  

#32 0x5555594743ec in ?? ??:0  

#33 0x5555596134c3 in FPDF\_LoadXFA /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../fpdfsdk/fpdf\_view.cpp:255  

#34 0x5555596134c3 in ?? ??:0  

#35 0x55555663c83b in RenderPdf /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../samples/pdfium\_test.cc:790  

#36 0x55555663c83b in main /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../samples/pdfium\_test.cc:1002  

#37 0x55555663c83b in ?? ??:0  

#38 0x7ffff6ee582f in \_\_libc\_start\_main /build/glibc-Cl5G7W/glibc-2.23/csu/../csu/libc-start.c:291  

#39 0x7ffff6ee582f in ?? ??:0

SUMMARY: AddressSanitizer: heap-use-after-free (/workarea/fuzz/bin/pdfium\_coverage/pdfium\_test+0x3db029b)  

Shadow bytes around the buggy address:  

0x0c187fffe480: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c187fffe490: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa  

0x0c187fffe4a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c187fffe4b0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c187fffe4c0: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa  

=>0x0c187fffe4d0: fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd  

0x0c187fffe4e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c187fffe4f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c187fffe500: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c187fffe510: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c187fffe520: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

==22170==ABORTING

**CREDIT INFORMATION**  

Antti Levomäki and Christian Jalio from Forcepoint

## Attachments

- [victory_42b261df645ff0840e2392720915bccae701c70b0fe3d3232d28f2d5b0c840bc](attachments/victory_42b261df645ff0840e2392720915bccae701c70b0fe3d3232d28f2d5b0c840bc) (text/plain, 200.8 KB)

## Timeline

### cl...@chromium.org (2018-12-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5650103781818368.

### cl...@chromium.org (2018-12-10)

Testcase 5650103781818368 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5650103781818368.

### cl...@chromium.org (2018-12-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5977975989993472.

### cl...@chromium.org (2018-12-10)

Testcase 5977975989993472 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5977975989993472.

### mm...@chromium.org (2018-12-10)

Reproduced locally as well.

[Monorail components: Internals>Plugins>PDF]

### mm...@chromium.org (2018-12-10)

[Empty comment from Monorail migration]

### th...@chromium.org (2018-12-11)

XFA code is not shipped.

tsepez: Do you want to take a look?

### ds...@chromium.org (2018-12-11)

Over to thestig@ for triage.

### cl...@chromium.org (2018-12-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4906234907721728.

### cl...@chromium.org (2018-12-11)

Detailed report: https://clusterfuzz.com/testcase?key=4906234907721728

Fuzzer: libFuzzer_pdfium_xfa_fuzzer
Fuzz target binary: pdfium_xfa_fuzzer
Job Type: libfuzzer_chrome_asan
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61000000c9a8
Crash State:
  fxcrt::UnownedPtr<CXFA_Node>::Get
  CXFA_ItemLayoutProcessor::CalculateRowChildPosition
  CXFA_ItemLayoutProcessor::DoLayoutFlowedContainer
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=577293:577299

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4906234907721728

See https://github.com/google/clusterfuzz-tools for more information.

### th...@chromium.org (2018-12-12)

XFA is not shipped to users.

### cl...@chromium.org (2018-12-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6373157046583296.

### li...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### li...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-01-29)

CL at https://pdfium-review.googlesource.com/c/pdfium/+/49350

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

And this now appears to be giving a fixed offset null segv after the patch.

### cl...@chromium.org (2019-01-30)

ClusterFuzz has detected this issue as fixed in range 627168:627186.

Detailed report: https://clusterfuzz.com/testcase?key=4906234907721728

Fuzzer: libFuzzer_pdfium_xfa_fuzzer
Fuzz target binary: pdfium_xfa_fuzzer
Job Type: libfuzzer_chrome_asan
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61000000c9a8
Crash State:
  fxcrt::UnownedPtr<CXFA_Node>::Get
  CXFA_ItemLayoutProcessor::CalculateRowChildPosition
  CXFA_ItemLayoutProcessor::DoLayoutFlowedContainer
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=577293:577299
Fixed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=627168:627186

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4906234907721728

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2019-01-30)

ClusterFuzz testcase 4906234907721728 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2019-01-31)

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

### sh...@chromium.org (2019-05-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-05-09)

This issue was migrated from crbug.com/chromium/913564?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/925789, crbug.com/chromium/925790]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093366)*
