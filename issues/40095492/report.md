# Security: pdfium heap-use-after-free in CXFA_ItemLayoutProcessor::InsertFlowedItem

| Field | Value |
|-------|-------|
| **Issue ID** | [40095492](https://issues.chromium.org/issues/40095492) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-06-24 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

pdfium heap-use-after-free in CXFA\_ItemLayoutProcessor::InsertFlowedItem

**VERSION**  

commit 9d1193b591c5ac53cf1680c80692911f7dd26607  

Date: Fri Jun 21 21:32:51 2019 +0000

**REPRODUCTION CASE**  

Open attached file.

# ADDITIONAL INFORMATION Rendering PDF file /workarea/samplestore/wip/pdfium/victory/victory\_62f854c0627d7e44c640c74be74dd0a3df5c5711c5bc5f7d4cb1eea6e024d1ea.raw. Document has invalid cross reference table

==568==ERROR: AddressSanitizer: heap-use-after-free on address 0x60b0000c4798 at pc 0x5555598e17c4 bp 0x7fffffffb640 sp 0x7fffffffb638  

READ of size 8 at 0x60b0000c4798 thread T0  

#0 0x5555598e17c3 in RemoveChild ./../../core/fxcrt/tree\_node.h:106  

#1 0x5555598e17c3 in RemoveSelfIfParented ./../../core/fxcrt/tree\_node.h:130  

#2 0x5555598e17c3 in ExtractLayoutItem ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:824  

#3 0x5555598e17c3 in ?? ??:0  

#4 0x5555598fb4cd in CXFA\_ItemLayoutProcessor::InsertFlowedItem(CXFA\_ItemLayoutProcessor\*, bool, bool, float, XFA\_AttributeValue, unsigned char\*, std::\_\_1::vector<CXFA\_ContentLayoutItem\*, std::\_\_1::allocator<CXFA\_ContentLayoutItem\*> > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_LayoutContext\*, bool) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:2430  

#5 0x5555598fb4cd in ?? ??:0  

#6 0x5555598f5201 in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_LayoutContext\*, bool) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:1793  

#7 0x5555598f5201 in ?? ??:0  

#8 0x5555598e5dd9 in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:2057  

#9 0x5555598e5dd9 in ?? ??:0  

#10 0x5555598fa3d0 in CXFA\_ItemLayoutProcessor::InsertFlowedItem(CXFA\_ItemLayoutProcessor\*, bool, bool, float, XFA\_AttributeValue, unsigned char\*, std::\_\_1::vector<CXFA\_ContentLayoutItem\*, std::\_\_1::allocator<CXFA\_ContentLayoutItem\*> > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_LayoutContext\*, bool) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:2341  

#11 0x5555598fa3d0 in ?? ??:0  

#12 0x5555598f5201 in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_LayoutContext\*, bool) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:1793  

#13 0x5555598f5201 in ?? ??:0  

#14 0x5555598e5dd9 in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:2057  

#15 0x5555598e5dd9 in ?? ??:0  

#16 0x5555598fa3d0 in CXFA\_ItemLayoutProcessor::InsertFlowedItem(CXFA\_ItemLayoutProcessor\*, bool, bool, float, XFA\_AttributeValue, unsigned char\*, std::\_\_1::vector<CXFA\_ContentLayoutItem\*, std::\_\_1::allocator<CXFA\_ContentLayoutItem\*> > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_LayoutContext\*, bool) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:2341  

#17 0x5555598fa3d0 in ?? ??:0  

#18 0x5555598f5201 in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_LayoutContext\*, bool) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:1793  

#19 0x5555598f5201 in ?? ??:0  

#20 0x5555598e5dd9 in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:2057  

#21 0x5555598e5dd9 in ?? ??:0  

#22 0x5555598fa3d0 in CXFA\_ItemLayoutProcessor::InsertFlowedItem(CXFA\_ItemLayoutProcessor\*, bool, bool, float, XFA\_AttributeValue, unsigned char\*, std::\_\_1::vector<CXFA\_ContentLayoutItem\*, std::\_\_1::allocator<CXFA\_ContentLayoutItem\*> > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_LayoutContext\*, bool) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:2341  

#23 0x5555598fa3d0 in ?? ??:0  

#24 0x5555598f5201 in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_LayoutContext\*, bool) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:1793  

#25 0x5555598f5201 in ?? ??:0  

#26 0x5555598e5dd9 in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:2057  

#27 0x5555598e5dd9 in ?? ??:0  

#28 0x55555991a09b in CXFA\_LayoutProcessor::DoLayout() ./../../xfa/fxfa/layout/cxfa\_layoutprocessor.cpp:79  

#29 0x55555991a09b in ?? ??:0  

#30 0x55555986a615 in CXFA\_FFDocView::RunLayout() ./../../xfa/fxfa/cxfa\_ffdocview.cpp:449  

#31 0x55555986a615 in ?? ??:0  

#32 0x555559869e69 in CXFA\_FFDocView::StopLayout() ./../../xfa/fxfa/cxfa\_ffdocview.cpp:135  

#33 0x555559869e69 in ?? ??:0  

#34 0x55555991ca57 in CPDFXFA\_Context::LoadXFADoc() ./../../fpdfsdk/fpdfxfa/cpdfxfa\_context.cpp:132  

#35 0x55555991ca57 in ?? ??:0  

#36 0x5555566ba6c3 in FPDF\_LoadXFA ./../../fpdfsdk/fpdf\_view.cpp:270  

#37 0x5555566ba6c3 in ?? ??:0  

#38 0x555556645285 in RenderPdf ./../../samples/pdfium\_test.cc:819  

#39 0x555556645285 in main ./../../samples/pdfium\_test.cc:1039  

#40 0x555556645285 in ?? ??:0  

#41 0x7ffff6e24b96 in \_\_libc\_start\_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310  

#42 0x7ffff6e24b96 in ?? ??:0

0x60b0000c4798 is located 24 bytes inside of 112-byte region [0x60b0000c4780,0x60b0000c47f0)  

freed by thread T0 here:  

#0 0x55555663d6cd in operator delete(void\*) *asan\_rtl*  

#1 0x55555663d6cd in ?? ??:0  

#2 0x5555598e16e4 in CXFA\_ItemLayoutProcessor::ExtractLayoutItem() ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:825  

#3 0x5555598e16e4 in ?? ??:0  

#4 0x5555598fb4cd in CXFA\_ItemLayoutProcessor::InsertFlowedItem(CXFA\_ItemLayoutProcessor\*, bool, bool, float, XFA\_AttributeValue, unsigned char\*, std::\_\_1::vector<CXFA\_ContentLayoutItem\*, std::\_\_1::allocator<CXFA\_ContentLayoutItem\*> > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_LayoutContext\*, bool) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:2430  

#5 0x5555598fb4cd in ?? ??:0  

#6 0x5555598f5201 in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_LayoutContext\*, bool) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:1793  

#7 0x5555598f5201 in ?? ??:0  

#8 0x5555598e5dd9 in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:2057  

#9 0x5555598e5dd9 in ?? ??:0  

#10 0x5555598fa3d0 in CXFA\_ItemLayoutProcessor::InsertFlowedItem(CXFA\_ItemLayoutProcessor\*, bool, bool, float, XFA\_AttributeValue, unsigned char\*, std::\_\_1::vector<CXFA\_ContentLayoutItem\*, std::\_\_1::allocator<CXFA\_ContentLayoutItem\*> > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_LayoutContext\*, bool) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:2341  

#11 0x5555598fa3d0 in ?? ??:0  

#12 0x5555598f5201 in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_LayoutContext\*, bool) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:1793  

#13 0x5555598f5201 in ?? ??:0  

#14 0x5555598e5dd9 in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:2057  

#15 0x5555598e5dd9 in ?? ??:0  

#16 0x5555598fa3d0 in CXFA\_ItemLayoutProcessor::InsertFlowedItem(CXFA\_ItemLayoutProcessor\*, bool, bool, float, XFA\_AttributeValue, unsigned char\*, std::\_\_1::vector<CXFA\_ContentLayoutItem\*, std::\_\_1::allocator<CXFA\_ContentLayoutItem\*> > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_LayoutContext\*, bool) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:2341  

#17 0x5555598fa3d0 in ?? ??:0  

#18 0x5555598f5201 in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_LayoutContext\*, bool) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:1793  

#19 0x5555598f5201 in ?? ??:0  

#20 0x5555598e5dd9 in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:2057  

#21 0x5555598e5dd9 in ?? ??:0  

#22 0x5555598fa3d0 in CXFA\_ItemLayoutProcessor::InsertFlowedItem(CXFA\_ItemLayoutProcessor\*, bool, bool, float, XFA\_AttributeValue, unsigned char\*, std::\_\_1::vector<CXFA\_ContentLayoutItem\*, std::\_\_1::allocator<CXFA\_ContentLayoutItem\*> > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_LayoutContext\*, bool) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:2341  

#23 0x5555598fa3d0 in ?? ??:0  

#24 0x5555598f5201 in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_LayoutContext\*, bool) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:1793  

#25 0x5555598f5201 in ?? ??:0  

#26 0x5555598e5dd9 in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:2057  

#27 0x5555598e5dd9 in ?? ??:0  

#28 0x55555991a09b in CXFA\_LayoutProcessor::DoLayout() ./../../xfa/fxfa/layout/cxfa\_layoutprocessor.cpp:79  

#29 0x55555991a09b in ?? ??:0  

#30 0x55555986a615 in CXFA\_FFDocView::RunLayout() ./../../xfa/fxfa/cxfa\_ffdocview.cpp:449  

#31 0x55555986a615 in ?? ??:0  

#32 0x555559869e69 in CXFA\_FFDocView::StopLayout() ./../../xfa/fxfa/cxfa\_ffdocview.cpp:135  

#33 0x555559869e69 in ?? ??:0  

#34 0x55555991ca57 in CPDFXFA\_Context::LoadXFADoc() ./../../fpdfsdk/fpdfxfa/cpdfxfa\_context.cpp:132  

#35 0x55555991ca57 in ?? ??:0  

#36 0x5555566ba6c3 in FPDF\_LoadXFA ./../../fpdfsdk/fpdf\_view.cpp:270  

#37 0x5555566ba6c3 in ?? ??:0  

#38 0x555556645285 in RenderPdf ./../../samples/pdfium\_test.cc:819  

#39 0x555556645285 in main ./../../samples/pdfium\_test.cc:1039  

#40 0x555556645285 in ?? ??:0  

#41 0x7ffff6e24b96 in \_\_libc\_start\_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310  

#42 0x7ffff6e24b96 in ?? ??:0

previously allocated by thread T0 here:  

#0 0x55555663ce6d in operator new(unsigned long) *asan\_rtl*  

#1 0x55555663ce6d in ?? ??:0  

#2 0x5555598dd4a1 in MakeUnique<CXFA\_ContentLayoutItem, CXFA\_Node \*&, std::\_\_1::unique\_ptr<CXFA\_FFWidget, std::\_\_1::default\_delete<CXFA\_FFWidget> > > ./../../third\_party/base/ptr\_util.h:56  

#3 0x5555598dd4a1 in CreateContentLayoutItem ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:645  

#4 0x5555598dd4a1 in ?? ??:0  

#5 0x5555598fe571 in CXFA\_ItemLayoutProcessor::CalculateRowChildPosition(std::\_\_1::vector<CXFA\_ContentLayoutItem\*, std::\_\_1::allocator<CXFA\_ContentLayoutItem\*> > (&) [3], XFA\_AttributeValue, bool, bool, float\*, float\*, float\*, float, float, bool) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:1900  

#6 0x5555598fe571 in ?? ??:0  

#7 0x5555598f580c in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_LayoutContext\*, bool) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:1833  

#8 0x5555598f580c in ?? ??:0  

#9 0x5555598e5dd9 in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:2057  

#10 0x5555598e5dd9 in ?? ??:0  

#11 0x5555598fa3d0 in CXFA\_ItemLayoutProcessor::InsertFlowedItem(CXFA\_ItemLayoutProcessor\*, bool, bool, float, XFA\_AttributeValue, unsigned char\*, std::\_\_1::vector<CXFA\_ContentLayoutItem\*, std::\_\_1::allocator<CXFA\_ContentLayoutItem\*> > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_LayoutContext\*, bool) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:2341  

#12 0x5555598fa3d0 in ?? ??:0  

#13 0x5555598f5201 in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_LayoutContext\*, bool) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:1793  

#14 0x5555598f5201 in ?? ??:0  

#15 0x5555598e5dd9 in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:2057  

#16 0x5555598e5dd9 in ?? ??:0  

#17 0x5555598fa3d0 in CXFA\_ItemLayoutProcessor::InsertFlowedItem(CXFA\_ItemLayoutProcessor\*, bool, bool, float, XFA\_AttributeValue, unsigned char\*, std::\_\_1::vector<CXFA\_ContentLayoutItem\*, std::\_\_1::allocator<CXFA\_ContentLayoutItem\*> > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_LayoutContext\*, bool) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:2341  

#18 0x5555598fa3d0 in ?? ??:0  

#19 0x5555598f5201 in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_LayoutContext\*, bool) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:1793  

#20 0x5555598f5201 in ?? ??:0  

#21 0x5555598e5dd9 in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:2057  

#22 0x5555598e5dd9 in ?? ??:0  

#23 0x5555598fa3d0 in CXFA\_ItemLayoutProcessor::InsertFlowedItem(CXFA\_ItemLayoutProcessor\*, bool, bool, float, XFA\_AttributeValue, unsigned char\*, std::\_\_1::vector<CXFA\_ContentLayoutItem\*, std::\_\_1::allocator<CXFA\_ContentLayoutItem\*> > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_LayoutContext\*, bool) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:2341  

#24 0x5555598fa3d0 in ?? ??:0  

#25 0x5555598f5201 in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_LayoutContext\*, bool) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:1793  

#26 0x5555598f5201 in ?? ??:0  

#27 0x5555598e5dd9 in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:2057  

#28 0x5555598e5dd9 in ?? ??:0  

#29 0x5555598fa3d0 in CXFA\_ItemLayoutProcessor::InsertFlowedItem(CXFA\_ItemLayoutProcessor\*, bool, bool, float, XFA\_AttributeValue, unsigned char\*, std::\_\_1::vector<CXFA\_ContentLayoutItem\*, std::\_\_1::allocator<CXFA\_ContentLayoutItem\*> > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_LayoutContext\*, bool) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:2341  

#30 0x5555598fa3d0 in ?? ??:0  

#31 0x5555598f5201 in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_LayoutContext\*, bool) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:1793  

#32 0x5555598f5201 in ?? ??:0  

#33 0x5555598e5dd9 in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) ./../../xfa/fxfa/layout/cxfa\_itemlayoutprocessor.cpp:2057  

#34 0x5555598e5dd9 in ?? ??:0  

#35 0x55555991a09b in CXFA\_LayoutProcessor::DoLayout() ./../../xfa/fxfa/layout/cxfa\_layoutprocessor.cpp:79  

#36 0x55555991a09b in ?? ??:0  

#37 0x5555598690e1 in CXFA\_FFDocView::DoLayout() ./../../xfa/fxfa/cxfa\_ffdocview.cpp:97  

#38 0x5555598690e1 in ?? ??:0  

#39 0x55555991ca3c in CPDFXFA\_Context::LoadXFADoc() ./../../fpdfsdk/fpdfxfa/cpdfxfa\_context.cpp:131  

#40 0x55555991ca3c in ?? ??:0  

#41 0x5555566ba6c3 in FPDF\_LoadXFA ./../../fpdfsdk/fpdf\_view.cpp:270  

#42 0x5555566ba6c3 in ?? ??:0  

#43 0x555556645285 in RenderPdf ./../../samples/pdfium\_test.cc:819  

#44 0x555556645285 in main ./../../samples/pdfium\_test.cc:1039  

#45 0x555556645285 in ?? ??:0  

#46 0x7ffff6e24b96 in \_\_libc\_start\_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310  

#47 0x7ffff6e24b96 in ?? ??:0

SUMMARY: AddressSanitizer: heap-use-after-free (/workarea/fuzz/bin/pdfium\_coverage/pdfium\_test+0x438d7c3)  

Shadow bytes around the buggy address:  

0x0c16800108a0: 00 00 00 00 00 00 fa fa fa fa fa fa fa fa fd fd  

0x0c16800108b0: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa  

0x0c16800108c0: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c16800108d0: 00 00 fa fa fa fa fa fa fa fa 00 00 00 00 00 00  

0x0c16800108e0: 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa fa  

=>0x0c16800108f0: fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd fa fa  

0x0c1680010900: fa fa fa fa fa fa 00 00 00 00 00 00 00 00 00 00  

0x0c1680010910: 00 00 00 00 fa fa fa fa fa fa fa fa 00 00 00 00  

0x0c1680010920: 00 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa  

0x0c1680010930: fa fa fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c1680010940: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

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

==568==ABORTING

**CREDIT INFORMATION**  

Antti Levomäki and Christian Jalio from Forcepoint

## Attachments

- [victory_62f854c0627d7e44c640c74be74dd0a3df5c5711c5bc5f7d4cb1eea6e024d1ea.raw](attachments/victory_62f854c0627d7e44c640c74be74dd0a3df5c5711c5bc5f7d4cb1eea6e024d1ea.raw) (application/octet-stream, 90.5 KB)

## Timeline

### cl...@chromium.org (2019-06-24)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5766977930526720.

### me...@chromium.org (2019-06-24)

thestig@ could you please take a look?

[Monorail components: Internals>Plugins>PDF]

### cl...@chromium.org (2019-06-24)

Detailed report: https://clusterfuzz.com/testcase?key=5766977930526720

Fuzzer: libFuzzer_pdfium_xfa_fuzzer
Fuzz target binary: pdfium_xfa_fuzzer
Job Type: libfuzzer_chrome_asan
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60f000067658
Crash State:
  fxcrt::TreeNode<CXFA_LayoutItem>::RemoveChild
  CXFA_ItemLayoutProcessor::ExtractLayoutItem
  CXFA_ItemLayoutProcessor::InsertFlowedItem
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=662013:662027

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5766977930526720

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

### th...@chromium.org (2019-06-24)

It's in the queue, but we have a backlog of XFA bugs.

### th...@chromium.org (2019-07-19)

I think https://pdfium-review.googlesource.com/c/pdfium/+/54190 will solve this. Need to put that in my code review queue.

### ts...@chromium.org (2019-07-30)

Confirm fixed in  12bc1c4dae87f by above CL.

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-07-31)

ClusterFuzz testcase 5766977930526720 is verified as fixed in https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=682443:682470

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### na...@google.com (2019-08-12)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-08-14)

Congrats! The Panel decided to reward $500 for this report!

### na...@google.com (2019-08-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-11-06)

This issue was migrated from crbug.com/chromium/977989?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095492)*
