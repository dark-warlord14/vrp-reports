# Security: pdfium heap BOF in RelocateTableRowCells

| Field | Value |
|-------|-------|
| **Issue ID** | [40093365](https://issues.chromium.org/issues/40093365) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2018-12-10 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

pdfium heap BOF in RelocateTableRowCells (READ of size 4)

**VERSION**  

commit 841c145e2eb1b44fbaf6a0266181e14b75036266  

Date: Sat Dec 8 01:01:57 2018 +0000

**REPRODUCTION CASE**  

Open attached file.

# ADDITIONAL INFORMATION Rendering PDF file /workarea/samplestore/wip/pdfium/victory/victory\_c746d4b1f2ad35a8d9652b8cb327caa0fb5849972dba4eae46672d3de0cc803c.

==16052==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000065820 at pc 0x5555592f3bdc bp 0x7fffffffbcf0 sp 0x7fffffffbce8  

READ of size 4 at 0x602000065820 thread T0  

#0 0x5555592f3bdb in (anonymous namespace)::RelocateTableRowCells(CXFA\_ContentLayoutItem\*, std::\_\_1::vector<float, std::\_\_1::allocator<float> > const&, XFA\_AttributeValue) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:233  

#1 0x5555592f3bdb in ?? ??:0  

#2 0x5555592f0fb9 in CXFA\_ItemLayoutProcessor::DoLayoutTableContainer(CXFA\_Node\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:1416  

#3 0x5555592f0fb9 in ?? ??:0  

#4 0x5555592ea65c in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2261  

#5 0x5555592ea65c in ?? ??:0  

#6 0x5555592fe1e2 in CXFA\_ItemLayoutProcessor::InsertFlowedItem(CXFA\_ItemLayoutProcessor\*, bool, bool, float, XFA\_AttributeValue, unsigned char\*, std::\_\_1::vector<CXFA\_ContentLayoutItem\*, std::\_\_1::allocator<CXFA\_ContentLayoutItem\*> > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_LayoutContext\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2552  

#7 0x5555592fe1e2 in ?? ??:0  

#8 0x5555592f91f9 in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_LayoutContext\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:1983  

#9 0x5555592f91f9 in ?? ??:0  

#10 0x5555592ea643 in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2250  

#11 0x5555592ea643 in ?? ??:0  

#12 0x5555592fe1e2 in CXFA\_ItemLayoutProcessor::InsertFlowedItem(CXFA\_ItemLayoutProcessor\*, bool, bool, float, XFA\_AttributeValue, unsigned char\*, std::\_\_1::vector<CXFA\_ContentLayoutItem\*, std::\_\_1::allocator<CXFA\_ContentLayoutItem\*> > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_LayoutContext\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2552  

#13 0x5555592fe1e2 in ?? ??:0  

#14 0x5555592f91f9 in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_LayoutContext\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:1983  

#15 0x5555592f91f9 in ?? ??:0  

#16 0x5555592ea643 in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2250  

#17 0x5555592ea643 in ?? ??:0  

#18 0x55555931d72c in CXFA\_LayoutProcessor::DoLayout() /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_layoutprocessor.cpp:74  

#19 0x55555931d72c in ?? ??:0  

#20 0x5555593df051 in CXFA\_FFDocView::DoLayout() /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_ffdocview.cpp:94  

#21 0x5555593df051 in ?? ??:0  

#22 0x5555594743d2 in CPDFXFA\_Context::LoadXFADoc() /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../fpdfsdk/fpdfxfa/cpdfxfa\_context.cpp:136  

#23 0x5555594743d2 in ?? ??:0  

#24 0x5555596134c3 in FPDF\_LoadXFA /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../fpdfsdk/fpdf\_view.cpp:255  

#25 0x5555596134c3 in ?? ??:0  

#26 0x55555663c83b in RenderPdf /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../samples/pdfium\_test.cc:790  

#27 0x55555663c83b in main /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../samples/pdfium\_test.cc:1002  

#28 0x55555663c83b in ?? ??:0  

#29 0x7ffff6ee582f in \_\_libc\_start\_main /build/glibc-Cl5G7W/glibc-2.23/csu/../csu/libc-start.c:291  

#30 0x7ffff6ee582f in ?? ??:0

0x602000065820 is located 0 bytes to the right of 16-byte region [0x602000065810,0x602000065820)  

freed by thread T0 here:  

#0 0x555556607342 in \_\_interceptor\_free *asan\_rtl*  

#1 0x555556607342 in ?? ??:0  

#2 0x5555566d8cdd in ft\_mem\_free /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../third\_party/freetype/src/src/base/ftutil.c:174  

#3 0x5555566d8cdd in FT\_Stream\_ExitFrame /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../third\_party/freetype/src/src/base/ftstream.c:342  

#4 0x5555566d8cdd in FT\_Stream\_ReadFields /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../third\_party/freetype/src/src/base/ftstream.c:862  

#5 0x5555566d8cdd in ?? ??:0  

#6 0x5555567a91b1 in check\_table\_dir /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../third\_party/freetype/src/src/sfnt/ttload.c:207  

#7 0x5555567a91b1 in tt\_face\_load\_font\_dir /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../third\_party/freetype/src/src/sfnt/ttload.c:391  

#8 0x5555567a91b1 in ?? ??:0  

#9 0x5555567a19df in sfnt\_init\_face /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../third\_party/freetype/src/src/sfnt/sfobjs.c:943  

#10 0x5555567a19df in ?? ??:0  

#11 0x5555567bad7d in tt\_face\_init /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../third\_party/freetype/src/src/truetype/ttobjs.c:636  

#12 0x5555567bad7d in ?? ??:0  

#13 0x5555566daf52 in open\_face /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../third\_party/freetype/src/src/base/ftobjs.c:1403  

#14 0x5555566daf52 in ?? ??:0  

#15 0x5555566c107b in ft\_open\_face\_internal /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../third\_party/freetype/src/src/base/ftobjs.c:2475  

#16 0x5555566c107b in ?? ??:0  

#17 0x55555924d507 in (anonymous namespace)::LoadFace(fxcrt::RetainPtr<IFX\_SeekableReadStream> const&, int) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fgas/font/cfgas\_fontmgr.cpp:513  

#18 0x55555924d507 in ?? ??:0  

#19 0x555559248bbb in VerifyUnicodeForFontDescriptor /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fgas/font/cfgas\_fontmgr.cpp:529  

#20 0x555559248bbb in GetFontByUnicodeImpl /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fgas/font/cfgas\_fontmgr.cpp:690  

#21 0x555559248bbb in ?? ??:0  

#22 0x55555924f7e5 in CFGAS\_FontMgr::GetFontByUnicode(wchar\_t, unsigned int, wchar\_t const\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fgas/font/cfgas\_fontmgr.cpp:883  

#23 0x55555924f7e5 in ?? ??:0  

#24 0x555559259a67 in CFGAS\_GEFont::GetGlyphIndexAndFont(wchar\_t, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fgas/font/cfgas\_gefont.cpp:242  

#25 0x555559259a67 in ?? ??:0  

#26 0x555559258628 in CFGAS\_GEFont::GetCharWidth(wchar\_t, int\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fgas/font/cfgas\_gefont.cpp:154  

#27 0x555559258628 in ?? ??:0  

#28 0x5555592663de in CFX\_RTFBreak::AppendChar\_Arabic(CFX\_Char\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fgas/layout/cfx\_rtfbreak.cpp:242  

#29 0x5555592663de in ?? ??:0  

#30 0x555559264685 in CFX\_RTFBreak::AppendChar(wchar\_t) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fgas/layout/cfx\_rtfbreak.cpp:109  

#31 0x555559264685 in ?? ??:0  

#32 0x555559438cf9 in CXFA\_TextLayout::AppendChar(fxcrt::WideString const&, float\*, float, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_textlayout.cpp:907  

#33 0x555559438cf9 in ?? ??:0  

#34 0x555559433c33 in CXFA\_TextLayout::LoadRichText(CFX\_XMLNode const\*, float, float\*, fxcrt::RetainPtr<CFX\_CSSComputedStyle> const&, bool, fxcrt::RetainPtr<CXFA\_LinkUserData>, bool, bool, int) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_textlayout.cpp:831  

#35 0x555559433c33 in ?? ??:0  

#36 0x555559431982 in CXFA\_TextLayout::LoadRichText(CFX\_XMLNode const\*, float, float\*, fxcrt::RetainPtr<CFX\_CSSComputedStyle> const&, bool, fxcrt::RetainPtr<CXFA\_LinkUserData>, bool, bool, int) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_textlayout.cpp:852  

#37 0x555559431982 in ?? ??:0  

#38 0x555559431982 in CXFA\_TextLayout::LoadRichText(CFX\_XMLNode const\*, float, float\*, fxcrt::RetainPtr<CFX\_CSSComputedStyle> const&, bool, fxcrt::RetainPtr<CXFA\_LinkUserData>, bool, bool, int) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_textlayout.cpp:852  

#39 0x555559431982 in ?? ??:0  

#40 0x555559431982 in CXFA\_TextLayout::LoadRichText(CFX\_XMLNode const\*, float, float\*, fxcrt::RetainPtr<CFX\_CSSComputedStyle> const&, bool, fxcrt::RetainPtr<CXFA\_LinkUserData>, bool, bool, int) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_textlayout.cpp:852  

#41 0x555559431982 in ?? ??:0  

#42 0x55555942edf2 in CXFA\_TextLayout::Loader(float, float\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_textlayout.cpp:666  

#43 0x55555942edf2 in ?? ??:0  

#44 0x55555942bd2e in CXFA\_TextLayout::CalcSize(CFX\_STemplate<float> const&, CFX\_STemplate<float> const&) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_textlayout.cpp:410  

#45 0x55555942bd2e in ?? ??:0  

#46 0x5555593539d5 in CXFA\_Node::CalcCaptionSize(CXFA\_FFDoc\*, CFX\_STemplate<float>\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_node.cpp:2775  

#47 0x5555593539d5 in ?? ??:0  

#48 0x555559356562 in CXFA\_Node::CalculateTextEditAutoSize(CXFA\_FFDoc\*, CFX\_STemplate<float>\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_node.cpp:2921  

#49 0x555559356562 in ?? ??:0  

#50 0x55555935c5cb in CXFA\_Node::CalculateAccWidthAndHeight(CXFA\_FFDoc\*, float) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_node.cpp:3174  

#51 0x55555935c5cb in ?? ??:0  

#52 0x55555935b230 in CXFA\_Node::StartWidgetLayout(CXFA\_FFDoc\*, float\*, float\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_node.cpp:3143  

#53 0x55555935b230 in ?? ??:0  

#54 0x5555593048ca in CXFA\_ItemLayoutProcessor::DoLayoutField() /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2222  

#55 0x5555593048ca in ?? ??:0  

#56 0x5555592ea2fb in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2268  

#57 0x5555592ea2fb in ?? ??:0  

#58 0x5555592fe1e2 in CXFA\_ItemLayoutProcessor::InsertFlowedItem(CXFA\_ItemLayoutProcessor\*, bool, bool, float, XFA\_AttributeValue, unsigned char\*, std::\_\_1::vector<CXFA\_ContentLayoutItem\*, std::\_\_1::allocator<CXFA\_ContentLayoutItem\*> > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_LayoutContext\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2552  

#59 0x5555592fe1e2 in ?? ??:0  

#60 0x5555592f91f9 in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_LayoutContext\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:1983  

#61 0x5555592f91f9 in ?? ??:0  

#62 0x5555592ea643 in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2250  

#63 0x5555592ea643 in ?? ??:0

previously allocated by thread T0 here:  

#0 0x5555566076c3 in \_\_interceptor\_malloc *asan\_rtl*  

#1 0x5555566076c3 in ?? ??:0  

#2 0x5555566d7366 in ft\_mem\_qalloc /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../third\_party/freetype/src/src/base/ftutil.c:76  

#3 0x5555566d7366 in FT\_Stream\_EnterFrame /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../third\_party/freetype/src/src/base/ftstream.c:272  

#4 0x5555566d7366 in ?? ??:0  

#5 0x5555566d8433 in FT\_Stream\_ReadFields /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../third\_party/freetype/src/src/base/ftstream.c:750  

#6 0x5555566d8433 in ?? ??:0  

#7 0x5555567a91b1 in check\_table\_dir /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../third\_party/freetype/src/src/sfnt/ttload.c:207  

#8 0x5555567a91b1 in tt\_face\_load\_font\_dir /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../third\_party/freetype/src/src/sfnt/ttload.c:391  

#9 0x5555567a91b1 in ?? ??:0  

#10 0x5555567a19df in sfnt\_init\_face /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../third\_party/freetype/src/src/sfnt/sfobjs.c:943  

#11 0x5555567a19df in ?? ??:0  

#12 0x5555567bad7d in tt\_face\_init /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../third\_party/freetype/src/src/truetype/ttobjs.c:636  

#13 0x5555567bad7d in ?? ??:0  

#14 0x5555566daf52 in open\_face /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../third\_party/freetype/src/src/base/ftobjs.c:1403  

#15 0x5555566daf52 in ?? ??:0  

#16 0x5555566c107b in ft\_open\_face\_internal /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../third\_party/freetype/src/src/base/ftobjs.c:2475  

#17 0x5555566c107b in ?? ??:0  

#18 0x55555924d507 in (anonymous namespace)::LoadFace(fxcrt::RetainPtr<IFX\_SeekableReadStream> const&, int) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fgas/font/cfgas\_fontmgr.cpp:513  

#19 0x55555924d507 in ?? ??:0  

#20 0x555559248bbb in VerifyUnicodeForFontDescriptor /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fgas/font/cfgas\_fontmgr.cpp:529  

#21 0x555559248bbb in GetFontByUnicodeImpl /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fgas/font/cfgas\_fontmgr.cpp:690  

#22 0x555559248bbb in ?? ??:0  

#23 0x55555924f7e5 in CFGAS\_FontMgr::GetFontByUnicode(wchar\_t, unsigned int, wchar\_t const\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fgas/font/cfgas\_fontmgr.cpp:883  

#24 0x55555924f7e5 in ?? ??:0  

#25 0x555559259a67 in CFGAS\_GEFont::GetGlyphIndexAndFont(wchar\_t, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fgas/font/cfgas\_gefont.cpp:242  

#26 0x555559259a67 in ?? ??:0  

#27 0x555559258628 in CFGAS\_GEFont::GetCharWidth(wchar\_t, int\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fgas/font/cfgas\_gefont.cpp:154  

#28 0x555559258628 in ?? ??:0  

#29 0x5555592663de in CFX\_RTFBreak::AppendChar\_Arabic(CFX\_Char\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fgas/layout/cfx\_rtfbreak.cpp:242  

#30 0x5555592663de in ?? ??:0  

#31 0x555559264685 in CFX\_RTFBreak::AppendChar(wchar\_t) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fgas/layout/cfx\_rtfbreak.cpp:109  

#32 0x555559264685 in ?? ??:0  

#33 0x555559438cf9 in CXFA\_TextLayout::AppendChar(fxcrt::WideString const&, float\*, float, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_textlayout.cpp:907  

#34 0x555559438cf9 in ?? ??:0  

#35 0x555559433c33 in CXFA\_TextLayout::LoadRichText(CFX\_XMLNode const\*, float, float\*, fxcrt::RetainPtr<CFX\_CSSComputedStyle> const&, bool, fxcrt::RetainPtr<CXFA\_LinkUserData>, bool, bool, int) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_textlayout.cpp:831  

#36 0x555559433c33 in ?? ??:0  

#37 0x555559431982 in CXFA\_TextLayout::LoadRichText(CFX\_XMLNode const\*, float, float\*, fxcrt::RetainPtr<CFX\_CSSComputedStyle> const&, bool, fxcrt::RetainPtr<CXFA\_LinkUserData>, bool, bool, int) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_textlayout.cpp:852  

#38 0x555559431982 in ?? ??:0  

#39 0x555559431982 in CXFA\_TextLayout::LoadRichText(CFX\_XMLNode const\*, float, float\*, fxcrt::RetainPtr<CFX\_CSSComputedStyle> const&, bool, fxcrt::RetainPtr<CXFA\_LinkUserData>, bool, bool, int) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_textlayout.cpp:852  

#40 0x555559431982 in ?? ??:0  

#41 0x555559431982 in CXFA\_TextLayout::LoadRichText(CFX\_XMLNode const\*, float, float\*, fxcrt::RetainPtr<CFX\_CSSComputedStyle> const&, bool, fxcrt::RetainPtr<CXFA\_LinkUserData>, bool, bool, int) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_textlayout.cpp:852  

#42 0x555559431982 in ?? ??:0  

#43 0x55555942edf2 in CXFA\_TextLayout::Loader(float, float\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_textlayout.cpp:666  

#44 0x55555942edf2 in ?? ??:0  

#45 0x55555942bd2e in CXFA\_TextLayout::CalcSize(CFX\_STemplate<float> const&, CFX\_STemplate<float> const&) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/cxfa\_textlayout.cpp:410  

#46 0x55555942bd2e in ?? ??:0  

#47 0x5555593539d5 in CXFA\_Node::CalcCaptionSize(CXFA\_FFDoc\*, CFX\_STemplate<float>\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_node.cpp:2775  

#48 0x5555593539d5 in ?? ??:0  

#49 0x555559356562 in CXFA\_Node::CalculateTextEditAutoSize(CXFA\_FFDoc\*, CFX\_STemplate<float>\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_node.cpp:2921  

#50 0x555559356562 in ?? ??:0  

#51 0x55555935c5cb in CXFA\_Node::CalculateAccWidthAndHeight(CXFA\_FFDoc\*, float) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_node.cpp:3174  

#52 0x55555935c5cb in ?? ??:0  

#53 0x55555935b230 in CXFA\_Node::StartWidgetLayout(CXFA\_FFDoc\*, float\*, float\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_node.cpp:3143  

#54 0x55555935b230 in ?? ??:0  

#55 0x5555593048ca in CXFA\_ItemLayoutProcessor::DoLayoutField() /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2222  

#56 0x5555593048ca in ?? ??:0  

#57 0x5555592ea2fb in CXFA\_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA\_LayoutContext\*) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2268  

#58 0x5555592ea2fb in ?? ??:0  

#59 0x5555592fe1e2 in CXFA\_ItemLayoutProcessor::InsertFlowedItem(CXFA\_ItemLayoutProcessor\*, bool, bool, float, XFA\_AttributeValue, unsigned char\*, std::\_\_1::vector<CXFA\_ContentLayoutItem\*, std::\_\_1::allocator<CXFA\_ContentLayoutItem\*> > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_LayoutContext\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:2552  

#60 0x5555592fe1e2 in ?? ??:0  

#61 0x5555592f91f9 in CXFA\_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_LayoutContext\*, bool) /workarea/fuzz/victimlibs2/chromium/source/pdfium/pdfium/out/coverage/../../xfa/fxfa/parser/cxfa\_itemlayoutprocessor.cpp:1983  

#62 0x5555592f91f9 in ?? ??:0

SUMMARY: AddressSanitizer: heap-buffer-overflow (/workarea/fuzz/bin/pdfium\_coverage/pdfium\_test+0x3d9fbdb)  

Shadow bytes around the buggy address:  

0x0c0480004ab0: fa fa fd fa fa fa fd fd fa fa fd fa fa fa fd fa  

0x0c0480004ac0: fa fa fd fa fa fa fd fd fa fa fd fa fa fa fd fa  

0x0c0480004ad0: fa fa fd fa fa fa fd fa fa fa fd fd fa fa fd fa  

0x0c0480004ae0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa  

0x0c0480004af0: fa fa fd fa fa fa fd fd fa fa fd fd fa fa fd fd  

=>0x0c0480004b00: fa fa fd fd[fa]fa fd fd fa fa fd fd fa fa fd fd  

0x0c0480004b10: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd  

0x0c0480004b20: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd  

0x0c0480004b30: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd  

0x0c0480004b40: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd  

0x0c0480004b50: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa  

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

==16052==ABORTING

**CREDIT INFORMATION**  

Antti Levomäki and Christian Jalio from Forcepoint

## Attachments

- [victory_c746d4b1f2ad35a8d9652b8cb327caa0fb5849972dba4eae46672d3de0cc803c](attachments/victory_c746d4b1f2ad35a8d9652b8cb327caa0fb5849972dba4eae46672d3de0cc803c) (text/plain, 105.6 KB)

## Timeline

### cl...@chromium.org (2018-12-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5182946967027712.

### cl...@chromium.org (2018-12-10)

Testcase 5182946967027712 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5182946967027712.

### cl...@chromium.org (2018-12-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5681307188985856.

### cl...@chromium.org (2018-12-10)

Testcase 5681307188985856 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5681307188985856.

### mm...@chromium.org (2018-12-10)

Reproduced this locally with ToT.

[Monorail components: Internals>Plugins>PDF]

### th...@chromium.org (2018-12-11)

Stack trace looks a bit wonky. Should recheck. XFA is not shipped.

### ds...@chromium.org (2018-12-11)

Over to thestig@ for triage.

### cl...@chromium.org (2018-12-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5883474789269504.

### cl...@chromium.org (2018-12-11)

Detailed report: https://clusterfuzz.com/testcase?key=5883474789269504

Fuzzer: libFuzzer_pdfium_xfa_fuzzer
Fuzz target binary: pdfium_xfa_fuzzer
Job Type: libfuzzer_chrome_msan
Platform Id: linux

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  CXFA_Node::StartWidgetLayout
  RelocateTableRowCells
  CXFA_ItemLayoutProcessor::DoLayoutTableContainer
  
Sanitizer: memory (MSAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_msan&range=577283:577312

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5883474789269504

See https://www.chromium.org/developers/testing/memorysanitizer#TOC-Reproducing-ClusterFuzz-Bugs for more information.

The recommended severity (Security_Severity-Medium) is different from what was assigned to the bug. Please double check the accuracy of the assigned severity.

### th...@chromium.org (2018-12-12)

XFA is not shipped to users.

### th...@chromium.org (2019-02-09)

https://pdfium-review.googlesource.com/50391

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-02-11)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/7abb469ef7ebbce4645165d1d0e1dbb6c8e68461

commit 7abb469ef7ebbce4645165d1d0e1dbb6c8e68461
Author: Lei Zhang <thestig@chromium.org>
Date: Mon Feb 11 22:05:23 2019

Disallow invalid colspan values in RelocateTableRowCells().

BUG=chromium:913561

Change-Id: I5f184eb1a241c6b860d303c59ade3234b05eb7eb
Reviewed-on: https://pdfium-review.googlesource.com/c/50391
Commit-Queue: Lei Zhang <thestig@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>

[modify] https://crrev.com/7abb469ef7ebbce4645165d1d0e1dbb6c8e68461/xfa/fxfa/layout/cxfa_itemlayoutprocessor.cpp


### th...@chromium.org (2019-02-12)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-02-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b6a69427be33da517edbcc0500d3c61e33e4fcd3

commit b6a69427be33da517edbcc0500d3c61e33e4fcd3
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Feb 12 01:58:41 2019

Roll src/third_party/pdfium c05172e4e216..7abb469ef7eb (5 commits)

https://pdfium.googlesource.com/pdfium.git/+log/c05172e4e216..7abb469ef7eb


git log c05172e4e216..7abb469ef7eb --date=short --no-merges --format='%ad %ae %s'
2019-02-11 thestig@chromium.org Disallow invalid colspan values in RelocateTableRowCells().
2019-02-11 thestig@chromium.org Add CJX_Object::GetMeasureInUnit();
2019-02-11 thestig@chromium.org Add FPDF_CONSECUTIVE public flag.
2019-02-11 tsepez@chromium.org Refine tests for CJX_HostPseudoModel.
2019-02-11 thestig@chromium.org Add ScopedFPDFTextFind.


Created with:
  gclient setdep -r src/third_party/pdfium@7abb469ef7eb

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:913561
TBR=dsinclair@chromium.org

Change-Id: I4e201c38abd76f88bc998af03d31ee8454bfb432
Reviewed-on: https://chromium-review.googlesource.com/c/1464255
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#631040}
[modify] https://crrev.com/b6a69427be33da517edbcc0500d3c61e33e4fcd3/DEPS


### sh...@chromium.org (2019-02-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-02-15)

ClusterFuzz has detected this issue as fixed in range 631038:631040.

Detailed report: https://clusterfuzz.com/testcase?key=5883474789269504

Fuzzer: libFuzzer_pdfium_xfa_fuzzer
Fuzz target binary: pdfium_xfa_fuzzer
Job Type: libfuzzer_chrome_msan
Platform Id: linux

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  CXFA_Node::StartWidgetLayout
  RelocateTableRowCells
  CXFA_ItemLayoutProcessor::DoLayoutTableContainer
  
Sanitizer: memory (MSAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_msan&range=577283:577312
Fixed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_msan&range=631038:631040

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5883474789269504

See https://www.chromium.org/developers/testing/memorysanitizer#TOC-Reproducing-ClusterFuzz-Bugs for instructions to reproduce this bug locally.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2019-02-15)

ClusterFuzz testcase 5883474789269504 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### na...@google.com (2019-02-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-02-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2019-02-25)

Thanks for the report! The VRP panel decided to reward $1,000 for this bug (and noted that it should be tracked as a Medium).  Cheers!

### aw...@google.com (2019-03-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-05-21)

This issue was migrated from crbug.com/chromium/913561?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093365)*
