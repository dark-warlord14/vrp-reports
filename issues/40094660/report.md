# pdfium (XFA): oob read+write in CFDE_TextOut

| Field | Value |
|-------|-------|
| **Issue ID** | [40094660](https://issues.chromium.org/issues/40094660) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | pd...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2019-04-17 |
| **Bounty** | $7,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86\_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.124 Safari/537.36

Steps to reproduce the problem:  

There are two separate and independent of each other bugs here, which however seem to only reproduce in tandem. The initial ASAN report seems relatively harmless as a 4-byte READ, but it hides a serious bug. (I'll post the full reports in separate comments.) The reports are from the attached minimized PDF.

**(1)**

AddressSanitizer: heap-buffer-overflow on address 0x612000023850  

READ of size 4 at 0x612000023850 thread T0  

SCARINESS: 17 (4-byte-read-heap-buffer-overflow)  

#0 0x55e4f0ae71c2 in CFDE\_TextOut::ReloadLinePiece(CFDE\_TextOut::CFDE\_TTOLine\*, CFX\_RectF const&) xfa/fde/cfde\_textout.cpp:464:47

<https://cs.chromium.org/chromium/src/third_party/pdfium/xfa/fde/cfde_textout.cpp?l=464&rcl=4fcc1f28e25ec78d75e33264f1833336c37a3b3e>

const wchar\_t\* pwsStr = m\_wsText.c\_str();  

...  

while (iPieceIndex < iPieceCount) {  

int32\_t iStar = iStartChar;  

int32\_t iEnd = pPiece->iChars + iStar;  

while (iStar < iEnd) {  

dwBreakStatus = m\_pTxtBreak->AppendChar(\*(pwsStr + iStar)); // <---  

...  

++iStar;  

}  

++iPieceIndex;  

...  

}

Some debug information for the last iteration of the outer while.

m\_wsText.GetLength(): 61  

iStar: 60  

iEnd: 117

So it over-reads 200+ bytes.

To get to the second bug you can either fix this bug by limiting iEnd, or just suppress its ASAN report with **attribute**((no\_sanitize\_address)).

**(2)**

AddressSanitizer: heap-buffer-overflow on address 0x611000007f74  

WRITE of size 4 at 0x611000007f74 thread T0  

SCARINESS: 36 (4-byte-write-heap-buffer-overflow)  

#0 0x55e626670217 in CFDE\_TextOut::RetrievePieces(CFX\_BreakType, bool, CFX\_RectF const&, int\*, int\*) xfa/fde/cfde\_textout.cpp:385:29

<https://cs.chromium.org/chromium/src/third_party/pdfium/xfa/fde/cfde_textout.cpp?l=385&rcl=4fcc1f28e25ec78d75e33264f1833336c37a3b3e>

```
const CFX_BreakPiece\* pPiece = m_pTxtBreak->GetBreakPieceUnstable(i);  
int32_t iPieceChars = pPiece->GetLength();  
int32_t iChar = \*pStartChar;  
...  
int32_t j = 0;  
for (; j < iPieceChars; j++) {  
  const CFX_Char\* pTC = pPiece->GetChar(j);  
  int32_t iCurCharWidth = pTC->m_iCharWidth > 0 ? pTC->m_iCharWidth : 0;  
  if (...) {  
    if (...) {  
      ...  
      break; // not hit  
    }  
  }  
  ...  
  m_CharWidths[iChar++] = iCurCharWidth; // <---  
}  

```

Some debug information.

m\_CharWidths.size(): 61  

iChar: 60  

iPieceChars: 3

So it over-writes 12 bytes past m\_CharWidths.data(). Can be substantially increased by adding more characters to <time> in the PDF. With the initial un-minimized file it was 600+ bytes.

In addition to that, iCurCharWidth can be quite nicely controlled by an attacker, because it's derived from the inherent glyph width of a character and the font size. The characters and font size can be set directly in the PDF. The glyph width of each character is a static value set in the font, which can be easily changed. There's a nice Python library called fontTools to disassemble and re-assemble fonts from and to XML. And the font can be embedded in the PDF and made mandatory. (I'll get to that in the reproduction steps.)

**(3)**

If you also suppress the ASAN report for the second bug, more reports can appear. I observed them during minimization and will only list some briefly, because they're fixed when the second bug is.

AddressSanitizer: heap-use-after-free on address 0x61a000023b84  

READ of size 4 at 0x61a000023b84 thread T0  

SCARINESS: 45 (4-byte-read-heap-use-after-free)  

#0 0x560688675053 in CFX\_TxtBreak::GetDisplayPos(CFX\_TxtBreak::Run const\*, TextCharPos\*) const xfa/fgas/layout/cfx\_txtbreak.cpp:711:16

AddressSanitizer: attempting free on address which was not malloc()-ed: 0x61a00002b880 in thread T0  

SCARINESS: 40 (bad-free)  

#0 0x55651296d302 in operator delete(void\*) compiler-rt/lib/asan/asan\_new\_delete.cc:172:3  

#1 0x556512ac0637 in v8::internal::Heap::TearDown()  

#2 0x556512f00c0a in v8::internal::Isolate::Deinit()  

#3 0x556512f0090c in v8::internal::Isolate::Delete(v8::internal::Isolate\*)  

#4 0x55651375d896 in CJS\_Runtime::~CJS\_Runtime() fxjs/cjs\_runtime.cpp:80:5

What is the expected behavior?

What went wrong?  

^

Did this work before? No

Chrome version: 70.0.3538.124 Channel: n/a  

OS Version:  

Flash Version:

## Attachments

- [chromium-953881.pdf](attachments/chromium-953881.pdf) (application/pdf, 689 B)
- [chromium-953881.ttf](attachments/chromium-953881.ttf) (application/octet-stream, 7.1 KB)
- [chromium-953881-with-font.pdf](attachments/chromium-953881-with-font.pdf) (application/pdf, 10.3 KB)

## Timeline

### pd...@gmail.com (2019-04-17)

The attached regular PDF is unlikely to reproduce on most systems, because of different installed fonts. So there are two ways to reproduce reliably.

(1)

1. Copy the TTF into an empty directory.
2. ./pdfium_test --font-dir=path/to/directory PDF

This makes pdfium ignore other fonts installed on the system.

(2)

That's obviously not useful to an attacker. So I also produced a PDF with the font embedded. pdfium always prefers embedded fonts with a matching name.

Note that the font is named Courier in the PDF because that's currently the default font pdfium wants to use for that element.

https://cs.chromium.org/chromium/src/third_party/pdfium/xfa/fxfa/parser/cxfa_node.cpp?l=3958&rcl=4fcc1f28e25ec78d75e33264f1833336c37a3b3e

However it could have any name, with that name reflected in an additional <font> element in the XFA part.

### pd...@gmail.com (2019-04-17)

And the full reports.

AddressSanitizer: heap-buffer-overflow on address 0x612000023850 at pc 0x55e4f0ae71c3 bp 0x7ffefe0c0b10 sp 0x7ffefe0c0b08
READ of size 4 at 0x612000023850 thread T0
SCARINESS: 17 (4-byte-read-heap-buffer-overflow)
    #0 0x55e4f0ae71c2 in CFDE_TextOut::ReloadLinePiece(CFDE_TextOut::CFDE_TTOLine*, CFX_RectF const&) xfa/fde/cfde_textout.cpp:464:47
    #1 0x55e4f0ae4dc5 in CFDE_TextOut::Reload(CFX_RectF const&) xfa/fde/cfde_textout.cpp:444:7
    #2 0x55e4f0ae41a0 in CFDE_TextOut::DrawLogicText(CFX_RenderDevice*, fxcrt::StringViewTemplate<wchar_t>, CFX_RectF const&) xfa/fde/cfde_textout.cpp:286:3
    #3 0x55e4f03856ae in CXFA_FWLTheme::DrawText(CFWL_ThemeText const&) xfa/fxfa/cxfa_fwltheme.cpp:144:15
    #4 0x55e4f0a95d66 in CFWL_ListBox::DrawItem(CXFA_Graphics*, IFWL_ThemeProvider*, CFWL_ListItem*, int, CFX_RectF const&, CFX_Matrix const*) xfa/fwl/cfwl_listbox.cpp:457:11
    #5 0x55e4f0a952a3 in CFWL_ListBox::DrawItems(CXFA_Graphics*, IFWL_ThemeProvider*, CFX_Matrix const*) xfa/fwl/cfwl_listbox.cpp:396:5
    #6 0x55e4f0a7db39 in CFWL_ListBox::DrawWidget(CXFA_Graphics*, CFX_Matrix const&) xfa/fwl/cfwl_listbox.cpp:107:3
    #7 0x55e4f0a971ac in CFWL_ListBox::OnDrawWidget(CXFA_Graphics*, CFX_Matrix const&) xfa/fwl/cfwl_listbox.cpp:709:3
    #8 0x55e4f036eaf7 in CXFA_FFListBox::OnDrawWidget(CXFA_Graphics*, CFX_Matrix const&) xfa/fxfa/cxfa_fflistbox.cpp:204:19
    #9 0x55e4f036eb1c in non-virtual thunk to CXFA_FFListBox::OnDrawWidget(CXFA_Graphics*, CFX_Matrix const&) xfa/fxfa/cxfa_fflistbox.cpp
    #10 0x55e4f0aad3e7 in CFWL_WidgetMgr::OnDrawWidget(CFWL_Widget*, CXFA_Graphics*, CFX_Matrix const&) xfa/fwl/cfwl_widgetmgr.cpp:344:27
    #11 0x55e4f0364142 in CXFA_FFField::RenderWidget(CXFA_Graphics*, CFX_Matrix const&, CXFA_FFWidget::HighlightOption) xfa/fxfa/cxfa_fffield.cpp:81:32
    #12 0x55e4f0386fe2 in CXFA_RenderContext::DoRender(CXFA_Graphics*) xfa/fxfa/cxfa_rendercontext.cpp:30:18
    #13 0x55e4f0155669 in CPDFSDK_PageView::PageView_OnDraw(CFX_RenderDevice*, CFX_Matrix const&, CPDF_RenderOptions*, FX_RECT const&) fpdfsdk/cpdfsdk_pageview.cpp:89:19
    #14 0x55e4efd9615d in (anonymous namespace)::FFLCommon(fpdf_form_handle_t__*, fpdf_bitmap_t__*, void*, fpdf_page_t__*, int, int, int, int, int, int) fpdfsdk/fpdf_formfill.cpp:219:18
    #15 0x55e4efd95d6c in FPDF_FFLDraw fpdfsdk/fpdf_formfill.cpp:590:3
    #16 0x55e4edda4755 in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:628:5
    #17 0x55e4edd9e17c in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:835:9
    #18 0x55e4edd9b500 in main samples/pdfium_test.cc:1015:5

0x612000023850 is located 0 bytes to the right of 272-byte region [0x612000023740,0x612000023850)
allocated by thread T0 here:
    #0 0x55e4edd6c20d in __interceptor_malloc compiler-rt/lib/asan/asan_malloc_linux.cc:145:3
    #1 0x55e4edde732a in PartitionAllocGenericFlags third_party/base/allocator/partition_allocator/partition_alloc.h:363:48
    #2 0x55e4edde732a in Alloc third_party/base/allocator/partition_allocator/partition_alloc.h:384
    #3 0x55e4edde732a in fxcrt::StringDataTemplate<wchar_t>::Create(unsigned long) core/fxcrt/string_data_template.h:39
    #4 0x55e4edde73f7 in fxcrt::StringDataTemplate<wchar_t>::Create(wchar_t const*, unsigned long) core/fxcrt/string_data_template.h:45:34
    #5 0x55e4eddea51e in fxcrt::WideString::WideString(fxcrt::StringViewTemplate<wchar_t>) core/fxcrt/widestring.cpp:348:19
    #6 0x55e4f0ae4163 in CFDE_TextOut::DrawLogicText(CFX_RenderDevice*, fxcrt::StringViewTemplate<wchar_t>, CFX_RectF const&) xfa/fde/cfde_textout.cpp:285:12
    #7 0x55e4f03856ae in CXFA_FWLTheme::DrawText(CFWL_ThemeText const&) xfa/fxfa/cxfa_fwltheme.cpp:144:15
    #8 0x55e4f0a95d66 in CFWL_ListBox::DrawItem(CXFA_Graphics*, IFWL_ThemeProvider*, CFWL_ListItem*, int, CFX_RectF const&, CFX_Matrix const*) xfa/fwl/cfwl_listbox.cpp:457:11
    #9 0x55e4f0a952a3 in CFWL_ListBox::DrawItems(CXFA_Graphics*, IFWL_ThemeProvider*, CFX_Matrix const*) xfa/fwl/cfwl_listbox.cpp:396:5
    #10 0x55e4f0a7db39 in CFWL_ListBox::DrawWidget(CXFA_Graphics*, CFX_Matrix const&) xfa/fwl/cfwl_listbox.cpp:107:3
    #11 0x55e4f0a971ac in CFWL_ListBox::OnDrawWidget(CXFA_Graphics*, CFX_Matrix const&) xfa/fwl/cfwl_listbox.cpp:709:3
    #12 0x55e4f036eaf7 in CXFA_FFListBox::OnDrawWidget(CXFA_Graphics*, CFX_Matrix const&) xfa/fxfa/cxfa_fflistbox.cpp:204:19
    #13 0x55e4f036eb1c in non-virtual thunk to CXFA_FFListBox::OnDrawWidget(CXFA_Graphics*, CFX_Matrix const&) xfa/fxfa/cxfa_fflistbox.cpp
    #14 0x55e4f0aad3e7 in CFWL_WidgetMgr::OnDrawWidget(CFWL_Widget*, CXFA_Graphics*, CFX_Matrix const&) xfa/fwl/cfwl_widgetmgr.cpp:344:27
    #15 0x55e4f0364142 in CXFA_FFField::RenderWidget(CXFA_Graphics*, CFX_Matrix const&, CXFA_FFWidget::HighlightOption) xfa/fxfa/cxfa_fffield.cpp:81:32
    #16 0x55e4f0386fe2 in CXFA_RenderContext::DoRender(CXFA_Graphics*) xfa/fxfa/cxfa_rendercontext.cpp:30:18
    #17 0x55e4f0155669 in CPDFSDK_PageView::PageView_OnDraw(CFX_RenderDevice*, CFX_Matrix const&, CPDF_RenderOptions*, FX_RECT const&) fpdfsdk/cpdfsdk_pageview.cpp:89:19
    #18 0x55e4efd9615d in (anonymous namespace)::FFLCommon(fpdf_form_handle_t__*, fpdf_bitmap_t__*, void*, fpdf_page_t__*, int, int, int, int, int, int) fpdfsdk/fpdf_formfill.cpp:219:18
    #19 0x55e4efd95d6c in FPDF_FFLDraw fpdfsdk/fpdf_formfill.cpp:590:3
    #20 0x55e4edda4755 in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:628:5
    #21 0x55e4edd9e17c in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:835:9
    #22 0x55e4edd9b500 in main samples/pdfium_test.cc:1015:5

SUMMARY: AddressSanitizer: heap-buffer-overflow xfa/fde/cfde_textout.cpp:464:47 in CFDE_TextOut::ReloadLinePiece(CFDE_TextOut::CFDE_TTOLine*, CFX_RectF const&)
Shadow bytes around the buggy address:
  0x0c247fffc6b0: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x0c247fffc6c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c247fffc6d0: 00 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa
  0x0c247fffc6e0: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x0c247fffc6f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c247fffc700: 00 00 00 00 00 00 00 00 00 00[fa]fa fa fa fa fa
  0x0c247fffc710: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c247fffc720: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c247fffc730: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c247fffc740: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c247fffc750: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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


### pd...@gmail.com (2019-04-17)

AddressSanitizer: heap-buffer-overflow on address 0x611000007f74 at pc 0x55e626670218 bp 0x7ffdff831c30 sp 0x7ffdff831c28
WRITE of size 4 at 0x611000007f74 thread T0
SCARINESS: 36 (4-byte-write-heap-buffer-overflow)
    #0 0x55e626670217 in CFDE_TextOut::RetrievePieces(CFX_BreakType, bool, CFX_RectF const&, int*, int*) xfa/fde/cfde_textout.cpp:385:29
    #1 0x55e626670f06 in CFDE_TextOut::ReloadLinePiece(CFDE_TextOut::CFDE_TTOLine*, CFX_RectF const&) xfa/fde/cfde_textout.cpp:477:5
    #2 0x55e62666edc5 in CFDE_TextOut::Reload(CFX_RectF const&) xfa/fde/cfde_textout.cpp:444:7
    #3 0x55e62666e1a0 in CFDE_TextOut::DrawLogicText(CFX_RenderDevice*, fxcrt::StringViewTemplate<wchar_t>, CFX_RectF const&) xfa/fde/cfde_textout.cpp:286:3
    #4 0x55e625f0f6ae in CXFA_FWLTheme::DrawText(CFWL_ThemeText const&) xfa/fxfa/cxfa_fwltheme.cpp:144:15
    #5 0x55e62661fd66 in CFWL_ListBox::DrawItem(CXFA_Graphics*, IFWL_ThemeProvider*, CFWL_ListItem*, int, CFX_RectF const&, CFX_Matrix const*) xfa/fwl/cfwl_listbox.cpp:457:11
    #6 0x55e62661f2a3 in CFWL_ListBox::DrawItems(CXFA_Graphics*, IFWL_ThemeProvider*, CFX_Matrix const*) xfa/fwl/cfwl_listbox.cpp:396:5
    #7 0x55e626607b39 in CFWL_ListBox::DrawWidget(CXFA_Graphics*, CFX_Matrix const&) xfa/fwl/cfwl_listbox.cpp:107:3
    #8 0x55e6266211ac in CFWL_ListBox::OnDrawWidget(CXFA_Graphics*, CFX_Matrix const&) xfa/fwl/cfwl_listbox.cpp:709:3
    #9 0x55e625ef8af7 in CXFA_FFListBox::OnDrawWidget(CXFA_Graphics*, CFX_Matrix const&) xfa/fxfa/cxfa_fflistbox.cpp:204:19
    #10 0x55e625ef8b1c in non-virtual thunk to CXFA_FFListBox::OnDrawWidget(CXFA_Graphics*, CFX_Matrix const&) xfa/fxfa/cxfa_fflistbox.cpp
    #11 0x55e6266373e7 in CFWL_WidgetMgr::OnDrawWidget(CFWL_Widget*, CXFA_Graphics*, CFX_Matrix const&) xfa/fwl/cfwl_widgetmgr.cpp:344:27
    #12 0x55e625eee142 in CXFA_FFField::RenderWidget(CXFA_Graphics*, CFX_Matrix const&, CXFA_FFWidget::HighlightOption) xfa/fxfa/cxfa_fffield.cpp:81:32
    #13 0x55e625f10fe2 in CXFA_RenderContext::DoRender(CXFA_Graphics*) xfa/fxfa/cxfa_rendercontext.cpp:30:18
    #14 0x55e625cdf669 in CPDFSDK_PageView::PageView_OnDraw(CFX_RenderDevice*, CFX_Matrix const&, CPDF_RenderOptions*, FX_RECT const&) fpdfsdk/cpdfsdk_pageview.cpp:89:19
    #15 0x55e62592015d in (anonymous namespace)::FFLCommon(fpdf_form_handle_t__*, fpdf_bitmap_t__*, void*, fpdf_page_t__*, int, int, int, int, int, int) fpdfsdk/fpdf_formfill.cpp:219:18
    #16 0x55e62591fd6c in FPDF_FFLDraw fpdfsdk/fpdf_formfill.cpp:590:3
    #17 0x55e62392e755 in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:628:5
    #18 0x55e62392817c in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:835:9
    #19 0x55e623925500 in main samples/pdfium_test.cc:1015:5

0x611000007f74 is located 0 bytes to the right of 244-byte region [0x611000007e80,0x611000007f74)
allocated by thread T0 here:
    #0 0x55e62392270d in operator new(unsigned long) compiler-rt/lib/asan/asan_new_delete.cc:105:3
    #1 0x55e623929358 in std::__1::__libcpp_allocate(unsigned long, unsigned long) buildtools/third_party/libc++/trunk/include/new:238:10
    #2 0x55e624463abd in std::__1::__split_buffer<int, std::__1::allocator<int>&>::__split_buffer(unsigned long, unsigned long, std::__1::allocator<int>&) buildtools/third_party/libc++/trunk/include/__split_buffer:311:29
    #3 0x55e62667d84d in std::__1::vector<int, std::__1::allocator<int> >::__append(unsigned long, int const&) buildtools/third_party/libc++/trunk/include/vector:1105:53
    #4 0x55e62666f90d in std::__1::vector<int, std::__1::allocator<int> >::resize(unsigned long, int const&) buildtools/third_party/libc++/trunk/include/vector:2058:15
    #5 0x55e62666e6cb in CFDE_TextOut::LoadText(fxcrt::WideString const&, CFX_RectF const&) xfa/fde/cfde_textout.cpp:321:18
    #6 0x55e62666e175 in CFDE_TextOut::DrawLogicText(CFX_RenderDevice*, fxcrt::StringViewTemplate<wchar_t>, CFX_RectF const&) xfa/fde/cfde_textout.cpp:285:3
    #7 0x55e625f0f6ae in CXFA_FWLTheme::DrawText(CFWL_ThemeText const&) xfa/fxfa/cxfa_fwltheme.cpp:144:15
    #8 0x55e62661fd66 in CFWL_ListBox::DrawItem(CXFA_Graphics*, IFWL_ThemeProvider*, CFWL_ListItem*, int, CFX_RectF const&, CFX_Matrix const*) xfa/fwl/cfwl_listbox.cpp:457:11
    #9 0x55e62661f2a3 in CFWL_ListBox::DrawItems(CXFA_Graphics*, IFWL_ThemeProvider*, CFX_Matrix const*) xfa/fwl/cfwl_listbox.cpp:396:5
    #10 0x55e626607b39 in CFWL_ListBox::DrawWidget(CXFA_Graphics*, CFX_Matrix const&) xfa/fwl/cfwl_listbox.cpp:107:3
    #11 0x55e6266211ac in CFWL_ListBox::OnDrawWidget(CXFA_Graphics*, CFX_Matrix const&) xfa/fwl/cfwl_listbox.cpp:709:3
    #12 0x55e625ef8af7 in CXFA_FFListBox::OnDrawWidget(CXFA_Graphics*, CFX_Matrix const&) xfa/fxfa/cxfa_fflistbox.cpp:204:19
    #13 0x55e625ef8b1c in non-virtual thunk to CXFA_FFListBox::OnDrawWidget(CXFA_Graphics*, CFX_Matrix const&) xfa/fxfa/cxfa_fflistbox.cpp
    #14 0x55e6266373e7 in CFWL_WidgetMgr::OnDrawWidget(CFWL_Widget*, CXFA_Graphics*, CFX_Matrix const&) xfa/fwl/cfwl_widgetmgr.cpp:344:27
    #15 0x55e625eee142 in CXFA_FFField::RenderWidget(CXFA_Graphics*, CFX_Matrix const&, CXFA_FFWidget::HighlightOption) xfa/fxfa/cxfa_fffield.cpp:81:32
    #16 0x55e625f10fe2 in CXFA_RenderContext::DoRender(CXFA_Graphics*) xfa/fxfa/cxfa_rendercontext.cpp:30:18
    #17 0x55e625cdf669 in CPDFSDK_PageView::PageView_OnDraw(CFX_RenderDevice*, CFX_Matrix const&, CPDF_RenderOptions*, FX_RECT const&) fpdfsdk/cpdfsdk_pageview.cpp:89:19
    #18 0x55e62592015d in (anonymous namespace)::FFLCommon(fpdf_form_handle_t__*, fpdf_bitmap_t__*, void*, fpdf_page_t__*, int, int, int, int, int, int) fpdfsdk/fpdf_formfill.cpp:219:18
    #19 0x55e62591fd6c in FPDF_FFLDraw fpdfsdk/fpdf_formfill.cpp:590:3
    #20 0x55e62392e755 in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:628:5
    #21 0x55e62392817c in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:835:9
    #22 0x55e623925500 in main samples/pdfium_test.cc:1015:5

SUMMARY: AddressSanitizer: heap-buffer-overflow xfa/fde/cfde_textout.cpp:385:29 in CFDE_TextOut::RetrievePieces(CFX_BreakType, bool, CFX_RectF const&, int*, int*)
Shadow bytes around the buggy address:
  0x0c227fff8f90: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
  0x0c227fff8fa0: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x0c227fff8fb0: 00 00 00 00 00 00 00 00 fc fc fc fc fc fc fc fc
  0x0c227fff8fc0: fc fc fc fc fc fc fc fc fa fa fa fa fa fa fa fa
  0x0c227fff8fd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c227fff8fe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00[04]fa
  0x0c227fff8ff0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c227fff9000: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c227fff9010: fd fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c227fff9020: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc
  0x0c227fff9030: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc
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


### pd...@gmail.com (2019-04-17)

Note: Chrome doesn't use XFA.

### es...@chromium.org (2019-04-18)

tsepez, could you PTAL?

### ad...@google.com (2019-05-01)

Assuming that the Security_Severity is high (due to OOB write) but, per the previous updates, impact is None because XFA is not used.

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2019-08-22)

[Empty comment from Monorail migration]

### pd...@gmail.com (2019-09-05)

You may have already tried recently, but if not: still reproduces.

### pd...@gmail.com (2019-11-01)

Considering the following commit, I suspect 997588 is a duplicate of this bug.

https://pdfium.googlesource.com/pdfium.git/+/96bfed3112eef90f8e8b41c9430d2e3a21ae71d0

### th...@chromium.org (2020-06-02)

[Empty comment from Monorail migration]

### th...@chromium.org (2020-06-02)

(Very late reply) to https://crbug.com/chromium/953881#c9 - yep!

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-02-24)

So this now hits a hard check, meaning we can treat this as a functional issue, rather than as a security one, given the desire to turn on XFA.
We should send to VRP and fix as time permits - ade?

### ad...@chromium.org (2021-02-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-01)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-04)

Congratulations, pdknsk@! The VRP Panel has decided to reward you $7,000 for this report. Nice work! And thank you for your patience! 

### am...@google.com (2021-03-05)

[Empty comment from Monorail migration]

### th...@chromium.org (2022-07-07)

This is still stuck in my bug queue. Since the report, a fuzzer found a similar issue and reported it as https://crbug.com/chromium/1147125. That got addressed in a much more timely fashion and now chromium-953881-with-font.pdf just triggers a CHECK() crash.

### gi...@appspot.gserviceaccount.com (2022-07-14)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/ceaa31b826614b69a1f8d2f1149186d9491a9ac0

commit ceaa31b826614b69a1f8d2f1149186d9491a9ac0
Author: Lei Zhang <thestig@chromium.org>
Date: Thu Jul 14 17:39:19 2022

Fix a bad array index calculation in CFDE_TextOut::ReloadLinePiece().

ReloadLinePiece() should not assume the pieces being reloaded are
contiguous and in-order.

Bug: chromium:953881
Change-Id: I0677a79f4424be24a4473bba96e5192d2e726b3f
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/95190
Commit-Queue: Lei Zhang <thestig@chromium.org>
Reviewed-by: Nigi <nigi@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/ceaa31b826614b69a1f8d2f1149186d9491a9ac0/xfa/fde/cfde_textout.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/ceaa31b826614b69a1f8d2f1149186d9491a9ac0/xfa/fde/cfde_textout_unittest.cpp


### th...@chromium.org (2022-07-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-14)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-07-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fe70cd6e69a4227de9a49c39b129bdef7dd831e2

commit fe70cd6e69a4227de9a49c39b129bdef7dd831e2
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Jul 14 21:19:21 2022

Roll PDFium from bd10345940d1 to d91ef1738785 (3 revisions)

https://pdfium.googlesource.com/pdfium.git/+log/bd10345940d1..d91ef1738785

2022-07-14 nigi@chromium.org Avoid integer overflow in CPDF_ToUnicodeMap::HandleBeginBFRange()
2022-07-14 thestig@chromium.org Fix a bad array index calculation in CFDE_TextOut::ReloadLinePiece().
2022-07-14 nigi@chromium.org [Skia] Enable 2 embedder tests.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org,huiyingst@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in PDFium: https://bugs.chromium.org/p/pdfium/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1343510,chromium:953881
Tbr: pdfium-deps-rolls@chromium.org,huiyingst@google.com
Change-Id: I941f50cfaa6774e533c104600e1b043a8ddcdfbb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3764361
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1024425}

[modify] https://crrev.com/fe70cd6e69a4227de9a49c39b129bdef7dd831e2/DEPS


### [Deleted User] (2022-10-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2023-07-29)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-29)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-31)

release notes do not need updating for this one (:

### is...@google.com (2023-07-31)

This issue was migrated from crbug.com/chromium/953881?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/997588]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094660)*
