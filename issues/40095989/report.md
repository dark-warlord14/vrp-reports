# Security: pdfium XFA m_pFocusWidget Use After Free

| Field | Value |
|-------|-------|
| **Issue ID** | [40095989](https://issues.chromium.org/issues/40095989) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-08-14 |
| **Bounty** | $5,000.00 |

## Description

Security: pdfium XFA m\_pFocusWidget Use After Free

**VERSION**  

Operating System: Ubuntu 16.04

**REPRODUCTION CASE**

Build pdfium with XFA enabled, ASAN enabled  

Run ./pdfium\_test bug\_40.pdf

**VULNERABILITY DETAILS**

m\_pFocusWidget defined as UnownedPtr  

cxfa\_ffdocview.h

```
  UnownedPtr<CXFA_FFWidget> m_pFocusWidget;  

```

cxfa\_contentlayoutprocessor.cpp

```
    for (auto& item : keepLayoutItems) {  
      m_pLayoutItem->RemoveChild(item);  
      \*fContentCurRowY -= item->m_sSize.height;  
      m_ArrayKeepItems.push_back(item);  
    }  
	...  
      if (ExistContainerKeep(pProcessor->GetFormNode(), false) &&  
          pProcessor->GetFormNode()->GetIntact() == XFA_AttributeValue::None) {  
        m_ArrayKeepItems.push_back(pChildLayoutItem);  
      } else {  
        m_ArrayKeepItems.clear();	// <== trigger free  
      }  

```

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

=================================================================  

==30753==ERROR: AddressSanitizer: heap-use-after-free on address 0x60d000028ff0 at pc 0x5620464d2dc4 bp 0x7ffc00ae0530 sp 0x7ffc00ae0528  

READ of size 1 at 0x60d000028ff0 thread T0  

#0 0x5620464d2dc3 in fxcrt::UnownedPtr<CXFA\_FFWidget>::ProbeForLowSeverityLifetimeIssue() core/fxcrt/unowned\_ptr.h:110:7  

#1 0x5620464ccbf4 in fxcrt::UnownedPtr<CXFA\_FFWidget>::~UnownedPtr() core/fxcrt/unowned\_ptr.h:60:19  

#2 0x5620464c6d5f in CXFA\_FFDocView::~CXFA\_FFDocView() xfa/fxfa/cxfa\_ffdocview.cpp:64:36  

#3 0x5620464c02ba in std::\_\_1::default\_delete<CXFA\_FFDocView>::operator()(CXFA\_FFDocView\*) const buildtools/third\_party/libc++/trunk/include/memory:2338:5  

#4 0x5620464bc928 in std::\_\_1::unique\_ptr<CXFA\_FFDocView, std::\_\_1::default\_delete<CXFA\_FFDocView> >::reset(CXFA\_FFDocView\*) buildtools/third\_party/libc++/trunk/include/memory:2651:7  

#5 0x5620464b9cf2 in CXFA\_FFDoc::~CXFA\_FFDoc() xfa/fxfa/cxfa\_ffdoc.cpp:99:15  

#6 0x5620464bea4a in std::\_\_1::default\_delete<CXFA\_FFDoc>::operator()(CXFA\_FFDoc\*) const buildtools/third\_party/libc++/trunk/include/memory:2338:5  

#7 0x5620464be9d8 in std::\_\_1::unique\_ptr<CXFA\_FFDoc, std::\_\_1::default\_delete<CXFA\_FFDoc> >::reset(CXFA\_FFDoc\*) buildtools/third\_party/libc++/trunk/include/memory:2651:7  

#8 0x562046961b94 in CPDFXFA\_Context::CloseXFADoc() fpdfsdk/fpdfxfa/cpdfxfa\_context.cpp:78:13  

#9 0x562046961927 in CPDFXFA\_Context::~CPDFXFA\_Context() fpdfsdk/fpdfxfa/cpdfxfa\_context.cpp:60:3  

#10 0x562046961bdb in CPDFXFA\_Context::~CPDFXFA\_Context() fpdfsdk/fpdfxfa/cpdfxfa\_context.cpp:56:37  

#11 0x5620422892af in std::\_\_1::default\_delete<CPDF\_Document::Extension>::operator()(CPDF\_Document::Extension\*) const buildtools/third\_party/libc++/trunk/include/memory:2338:5  

#12 0x562042289128 in std::\_\_1::unique\_ptr<CPDF\_Document::Extension, std::\_\_1::default\_delete<CPDF\_Document::Extension> >::reset(CPDF\_Document::Extension\*) buildtools/third\_party/libc++/trunk/include/memory:2651:7  

#13 0x562042288d78 in std::\_\_1::unique\_ptr<CPDF\_Document::Extension, std::\_\_1::default\_delete<CPDF\_Document::Extension> >::~unique\_ptr() buildtools/third\_party/libc++/trunk/include/memory:2605:19  

#14 0x5620428cbe0d in CPDF\_Document::~CPDF\_Document() core/fpdfapi/parser/cpdf\_document.cpp:73:31  

#15 0x5620428cbf0b in CPDF\_Document::~CPDF\_Document() core/fpdfapi/parser/cpdf\_document.cpp:73:31  

#16 0x562042289b2f in std::\_\_1::default\_delete<CPDF\_Document>::operator()(CPDF\_Document\*) const buildtools/third\_party/libc++/trunk/include/memory:2338:5  

#17 0x562042289a68 in std::\_\_1::unique\_ptr<CPDF\_Document, std::\_\_1::default\_delete<CPDF\_Document> >::reset(CPDF\_Document\*) buildtools/third\_party/libc++/trunk/include/memory:2651:7  

#18 0x562042288e48 in std::**1::unique\_ptr<CPDF\_Document, std::1::default\_delete<CPDF\_Document> >::~unique\_ptr() buildtools/third\_party/libc++/trunk/include/memory:2605:19  

#19 0x562042314c97 in FPDF\_CloseDocument fpdfsdk/fpdf\_view.cpp:741:3  

#20 0x56204217cc08 in FPDFDocumentDeleter::operator()(fpdf\_document\_t\*) public/cpp/fpdf\_deleters.h:39:47  

#21 0x56204217c548 in std::1::unique\_ptr<fpdf\_document\_t, FPDFDocumentDeleter>::reset(fpdf\_document\_t**\*) buildtools/third\_party/libc++/trunk/include/memory:2651:7  

#22 0x56204217c848 in std::**1::unique\_ptr<fpdf\_document\_t**, FPDFDocumentDeleter>::~unique\_ptr() buildtools/third\_party/libc++/trunk/include/memory:2605:19  

#23 0x562042170da0 in (anonymous namespace)::RenderPdf(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, char const\*, unsigned long, (anonymous namespace)::Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) samples/pdfium\_test.cc:888:1  

#24 0x56204216bf01 in main samples/pdfium\_test.cc:1068:5  

#25 0x7f0e465ca82f in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x2082f)

0x60d000028ff0 is located 0 bytes inside of 136-byte region [0x60d000028ff0,0x60d000029078)  

freed by thread T0 here:  

#0 0x56204216914d in operator delete(void\*) /b/swarming/w/ir/k/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cc:166:3  

#1 0x56204652c447 in CXFA\_FFTextEdit::~CXFA\_FFTextEdit() xfa/fxfa/cxfa\_fftextedit.cpp:37:37  

#2 0x562046500d9f in std::\_\_1::default\_delete<CXFA\_FFWidget>::operator()(CXFA\_FFWidget\*) const buildtools/third\_party/libc++/trunk/include/memory:2338:5  

#3 0x562046500cd8 in std::\_\_1::unique\_ptr<CXFA\_FFWidget, std::\_\_1::default\_delete<CXFA\_FFWidget> >::reset(CXFA\_FFWidget\*) buildtools/third\_party/libc++/trunk/include/memory:2651:7  

#4 0x5620464f9a08 in std::\_\_1::unique\_ptr<CXFA\_FFWidget, std::\_\_1::default\_delete<CXFA\_FFWidget> >::~unique\_ptr() buildtools/third\_party/libc++/trunk/include/memory:2605:19  

#5 0x56204671e9c1 in CXFA\_ContentLayoutItem::~CXFA\_ContentLayoutItem() xfa/fxfa/layout/cxfa\_contentlayoutitem.cpp:29:1  

#6 0x56204671eaeb in CXFA\_ContentLayoutItem::~CXFA\_ContentLayoutItem() xfa/fxfa/layout/cxfa\_contentlayoutitem.cpp:24:51  

#7 0x562046747e5d in fxcrt::RetainedTreeNode<CXFA\_LayoutItem>::Release() core/fxcrt/retained\_tree\_node.h:71:7  

#8 0x56204674803b in fxcrt::ReleaseDeleter<CXFA\_LayoutItem>::operator()(CXFA\_LayoutItem\*) const core/fxcrt/retain\_ptr.h:20:47  

#9 0x562046747fd8 in std::\_\_1::unique\_ptr<CXFA\_LayoutItem, fxcrt::ReleaseDeleter<CXFA\_LayoutItem> >::reset(CXFA\_LayoutItem\*) buildtools/third\_party/libc++/trunk/include/memory:2651:7  

#10 0x562046747f28 in std::\_\_1::unique\_ptr<CXFA\_LayoutItem, fxcrt::ReleaseDeleter<CXFA\_LayoutItem> >::~unique\_ptr() buildtools/third\_party/libc++/trunk/include/memory:2605:19  

#11 0x562046743484 in fxcrt::RetainPtr<CXFA\_LayoutItem>::~RetainPtr() core/fxcrt/retain\_ptr.h:25:7  

#12 0x5620467562ff in fxcrt::RetainedTreeNode<CXFA\_LayoutItem>::~RetainedTreeNode() core/fxcrt/retained\_tree\_node.h:54:7  

#13 0x562046755b92 in CXFA\_LayoutItem::~CXFA\_LayoutItem() xfa/fxfa/layout/cxfa\_layoutitem.cpp:43:1  

#14 0x56204671e9f1 in CXFA\_ContentLayoutItem::~CXFA\_ContentLayoutItem() xfa/fxfa/layout/cxfa\_contentlayoutitem.cpp:29:1  

#15 0x56204671eaeb in CXFA\_ContentLayoutItem::~CXFA\_ContentLayoutItem() xfa/fxfa/layout/cxfa\_contentlayoutitem.cpp:24:51  

#16 0x562046747e5d in fxcrt::RetainedTreeNode<CXFA\_LayoutItem>::Release() core/fxcrt/retained\_tree\_node.h:71:7  

#17 0x562046747ceb in fxcrt::ReleaseDeleter<CXFA\_ContentLayoutItem>::operator()(CXFA\_ContentLayoutItem\*) const core/fxcrt/retain\_ptr.h:20:47  

#18 0x562046747c88 in std::\_\_1::unique\_ptr<CXFA\_ContentLayoutItem, fxcrt::ReleaseDeleter<CXFA\_ContentLayoutItem> >::reset(CXFA\_ContentLayoutItem\*) buildtools/third\_party/libc++/trunk/include/memory:2651:7  

#19 0x562046747bd8 in std::\_\_1::unique\_ptr<CXFA\_ContentLayoutItem, fxcrt::ReleaseDeleter<CXFA\_ContentLayoutItem> >::~unique\_ptr() buildtools/third\_party/libc++/trunk/include/memory:2605:19  

#20 0x562046742ee4 in fxcrt::RetainPtr<CXFA\_ContentLayoutItem>::~RetainPtr() core/fxcrt/retain\_ptr.h:25:7  

#21 0x562046749d78 in std::\_\_1::allocator<fxcrt::RetainPtr<CXFA\_ContentLayoutItem> >::destroy(fxcrt::RetainPtr<CXFA\_ContentLayoutItem>\*) buildtools/third\_party/libc++/trunk/include/memory:1880:64  

#22 0x562046749d4c in void std::\_\_1::allocator\_traits<std::\_\_1::allocator<fxcrt::RetainPtr<CXFA\_ContentLayoutItem> > >::\_\_destroy<fxcrt::RetainPtr<CXFA\_ContentLayoutItem> >(std::\_\_1::integral\_constant<bool, true>, std::\_\_1::allocator<fxcrt::RetainPtr<CXFA\_ContentLayoutItem> >&, fxcrt::RetainPtr<CXFA\_ContentLayoutItem>\*) buildtools/third\_party/libc++/trunk/include/memory:1742:18  

#23 0x562046749cbe in void std::\_\_1::allocator\_traits<std::\_\_1::allocator<fxcrt::RetainPtr<CXFA\_ContentLayoutItem> > >::destroy<fxcrt::RetainPtr<CXFA\_ContentLayoutItem> >(std::\_\_1::allocator<fxcrt::RetainPtr<CXFA\_ContentLayoutItem> >&, fxcrt::RetainPtr<CXFA\_ContentLayoutItem>\*) buildtools/third\_party/libc++/trunk/include/memory:1595:14  

#24 0x562046749b7b in std::\_\_1::\_\_vector\_base<fxcrt::RetainPtr<CXFA\_ContentLayoutItem>, std::\_\_1::allocator<fxcrt::RetainPtr<CXFA\_ContentLayoutItem> > >::\_\_destruct\_at\_end(fxcrt::RetainPtr<CXFA\_ContentLayoutItem>\*) buildtools/third\_party/libc++/trunk/include/vector:426:9  

#25 0x562046749a7f in std::\_\_1::\_\_vector\_base<fxcrt::RetainPtr<CXFA\_ContentLayoutItem>, std::\_\_1::allocator<fxcrt::RetainPtr<CXFA\_ContentLayoutItem> > >::clear() buildtools/third\_party/libc++/trunk/include/vector:369:29  

#26 0x56204674400b in std::\_\_1::vector<fxcrt::RetainPtr<CXFA\_ContentLayoutItem>, std::\_\_1::allocator<fxcrt::RetainPtr<CXFA\_ContentLayoutItem> > >::clear() buildtools/third\_party/libc++/trunk/include/vector:772:17  

#27 0x56204673bf1c in CXFA\_ContentLayoutProcessor::InsertFlowedItem(CXFA\_ContentLayoutProcessor\*, bool, bool, float, XFA\_AttributeValue, unsigned char\*, std::\_\_1::vector<fxcrt::RetainPtr<CXFA\_ContentLayoutItem>, std::\_\_1::allocator<fxcrt::RetainPtr<CXFA\_ContentLayoutItem> > > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_ContentLayoutProcessor::Context\*, bool) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:2449:26  

#28 0x56204673773c in CXFA\_ContentLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_ContentLayoutProcessor::Context\*, bool) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:1795:23  

#29 0x56204672b168 in CXFA\_ContentLayoutProcessor::DoLayoutInternal(bool, float, float, CXFA\_ContentLayoutProcessor::Context\*) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:2066:18  

#30 0x56204672820c in CXFA\_ContentLayoutProcessor::DoLayout(bool, float, float) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:2045:10  

#31 0x562046757097 in CXFA\_LayoutProcessor::DoLayout() xfa/fxfa/layout/cxfa\_layoutprocessor.cpp:80:36  

#32 0x5620464c8f2e in CXFA\_FFDocView::RunLayout() xfa/fxfa/cxfa\_ffdocview.cpp:459:22  

#33 0x5620464c882f in CXFA\_FFDocView::StopLayout() xfa/fxfa/cxfa\_ffdocview.cpp:136:7  

#34 0x562046962129 in CPDFXFA\_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa\_context.cpp:130:18  

#35 0x56204231174e in FPDF\_LoadXFA fpdfsdk/fpdf\_view.cpp:260:32  

#36 0x562042170842 in (anonymous namespace)::RenderPdf(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, char const\*, unsigned long, (anonymous namespace)::Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) samples/pdfium\_test.cc:841:12  

#37 0x56204216bf01 in main samples/pdfium\_test.cc:1068:5  

#38 0x7f0e465ca82f in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x2082f)

previously allocated by thread T0 here:  

#0 0x5620421688ed in operator new(unsigned long) /b/swarming/w/ir/k/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cc:105:3  

#1 0x5620464f8af3 in pdfium::internal::MakeUniqueResult<CXFA\_FFTextEdit>::Scalar pdfium::MakeUnique<CXFA\_FFTextEdit, CXFA\_Node\*&>(CXFA\_Node\*&) third\_party/base/ptr\_util.h:56:29  

#2 0x5620464f4e40 in CXFA\_FFNotify::OnCreateContentLayoutItem(CXFA\_Node\*) xfa/fxfa/cxfa\_ffnotify.cpp:172:17  

#3 0x5620467203b7 in CXFA\_ContentLayoutProcessor::CreateContentLayoutItem(CXFA\_Node\*) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:644:27  

#4 0x562046740a57 in CXFA\_ContentLayoutProcessor::DoLayoutField() xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:2024:19  

#5 0x56204672b261 in CXFA\_ContentLayoutProcessor::DoLayoutInternal(bool, float, float, CXFA\_ContentLayoutProcessor::Context\*) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:2084:7  

#6 0x562046729651 in CXFA\_ContentLayoutProcessor::DoLayoutPositionedContainer(CXFA\_ContentLayoutProcessor::Context\*) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:1079:17  

#7 0x56204672b192 in CXFA\_ContentLayoutProcessor::DoLayoutInternal(bool, float, float, CXFA\_ContentLayoutProcessor::Context\*) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:2073:11  

#8 0x56204673b0b1 in CXFA\_ContentLayoutProcessor::InsertFlowedItem(CXFA\_ContentLayoutProcessor\*, bool, bool, float, XFA\_AttributeValue, unsigned char\*, std::\_\_1::vector<fxcrt::RetainPtr<CXFA\_ContentLayoutItem>, std::\_\_1::allocator<fxcrt::RetainPtr<CXFA\_ContentLayoutItem> > > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_ContentLayoutProcessor::Context\*, bool) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:2354:29  

#9 0x56204673773c in CXFA\_ContentLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_ContentLayoutProcessor::Context\*, bool) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:1795:23  

#10 0x56204672b168 in CXFA\_ContentLayoutProcessor::DoLayoutInternal(bool, float, float, CXFA\_ContentLayoutProcessor::Context\*) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:2066:18  

#11 0x56204672820c in CXFA\_ContentLayoutProcessor::DoLayout(bool, float, float) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:2045:10  

#12 0x562046757097 in CXFA\_LayoutProcessor::DoLayout() xfa/fxfa/layout/cxfa\_layoutprocessor.cpp:80:36  

#13 0x5620464c8614 in CXFA\_FFDocView::DoLayout() xfa/fxfa/cxfa\_ffdocview.cpp:98:30  

#14 0x56204696210b in CPDFXFA\_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa\_context.cpp:129:18  

#15 0x56204231174e in FPDF\_LoadXFA fpdfsdk/fpdf\_view.cpp:260:32  

#16 0x562042170842 in (anonymous namespace)::RenderPdf(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, char const\*, unsigned long, (anonymous namespace)::Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) samples/pdfium\_test.cc:841:12  

#17 0x56204216bf01 in main samples/pdfium\_test.cc:1068:5  

#18 0x7f0e465ca82f in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x2082f)

SUMMARY: AddressSanitizer: heap-use-after-free core/fxcrt/unowned\_ptr.h:110:7 in fxcrt::UnownedPtr<CXFA\_FFWidget>::ProbeForLowSeverityLifetimeIssue()  

Shadow bytes around the buggy address:  

0x0c1a7fffd1a0: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa  

0x0c1a7fffd1b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c1a7fffd1c0: fd fd fa fa fa fa fa fa fa fa fd fd fd fd fd fd  

0x0c1a7fffd1d0: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa  

0x0c1a7fffd1e0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x0c1a7fffd1f0: fd fd fd fd fd fd fa fa fa fa fa fa fa fa[fd]fd  

0x0c1a7fffd200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x0c1a7fffd210: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c1a7fffd220: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa  

0x0c1a7fffd230: fa fa fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c1a7fffd240: fd fd fd fd fa fa fa fa fa fa fa fa fd fd fd fd  

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

==30753==ABORTING

## Attachments

- [bug_40.pdf](attachments/bug_40.pdf) (application/pdf, 1.9 KB)
- [bug_40_2.pdf](attachments/bug_40_2.pdf) (application/pdf, 1.5 KB)

## Timeline

### cl...@chromium.org (2019-08-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6213086844682240.

### cl...@chromium.org (2019-08-14)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Plugins>PDF]

### cl...@chromium.org (2019-08-14)

Automatically assigning owner based on suspected regression changelist https://pdfium.googlesource.com/pdfium/+/12bc1c4dae87f210dc1b379d658a7f329c74d469 (Use RetainableTreeNode for LayoutItems.).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2019-08-14)

Detailed Report: https://clusterfuzz.com/testcase?key=6213086844682240

Fuzzing Engine: libFuzzer
Fuzz Target: pdfium_xfa_fuzzer
Job Type: libfuzzer_chrome_asan
Platform Id: linux

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x61100000d8c0
Crash State:
  fxcrt::UnownedPtr<CXFA_FFWidget>::ProbeForLowSeverityLifetimeIssue
  CXFA_FFDocView::~CXFA_FFDocView
  CXFA_FFDoc::~CXFA_FFDoc
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=682443:682470

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6213086844682240

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### ts...@chromium.org (2019-08-14)

[Empty comment from Monorail migration]

### hu...@gmail.com (2019-08-15)


I submit a case that could trigger this bug by javascript

Build pdfium with XFA enabled, ASAN enabled
Run ./pdfium_test bug_40_2.pdf


=================================================================
==1021==ERROR: AddressSanitizer: heap-use-after-free on address 0x60d00001c280 at pc 0x5612279f4e61 bp 0x7ffffe41db10 sp 0x7ffffe41db08
READ of size 8 at 0x60d00001c280 thread T0
    #0 0x5612279f4e60 in fxcrt::UnownedPtr<CXFA_ContentLayoutItem>::Get() const core/fxcrt/unowned_ptr.h:91:36
    #1 0x5612279f4afd in CXFA_FFWidget::GetLayoutItem() const xfa/fxfa/cxfa_ffwidget.h:133:72
    #2 0x56122bba0c82 in CXFA_FFDocView::SetFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_ffdocview.cpp:278:48
    #3 0x56122bb9f158 in CXFA_FFDocView::SetFocusNode(CXFA_Node*) xfa/fxfa/cxfa_ffdocview.cpp:316:8
    #4 0x56122bbcbc48 in CXFA_FFNotify::SetFocusWidgetNode(CXFA_Node*) xfa/fxfa/cxfa_ffnotify.cpp:302:13
    #5 0x561228caf96a in CJX_HostPseudoModel::setFocus(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_hostpseudomodel.cpp:461:12
    #6 0x561228cb2b4b in CJX_HostPseudoModel::setFocus_static(CJX_Object*, CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_hostpseudomodel.h:39:3
    #7 0x561228cce855 in CJX_Object::RunMethod(fxcrt::WideString const&, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_object.cpp:177:10
    #8 0x561228c00921 in CFXJSE_Engine::NormalMethodCall(v8::FunctionCallbackInfo<v8::Value> const&, fxcrt::WideString const&) fxjs/xfa/cfxjse_engine.cpp:459:31
    #9 0x561228beb686 in (anonymous namespace)::DynPropGetterAdapter_MethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) fxjs/xfa/cfxjse_class.cpp:112:7
    #10 0x561228fce8a5 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api-arguments-inl.h:157:3
    #11 0x561228fcafe6 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36
    #12 0x561228fc761a in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:139:5
    #13 0x561228fc68ee in v8::internal::Builtin_HandleApiCall(int, unsigned long*, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:127:1
    #14 0x56122b6fd6bf in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit (/media/monkie/storage/pdfium/out/asan-2019-08-12/pdfium_test+0x59f66bf)
    #15 0x56122b4852b4 in Builtins_InterpreterEntryTrampoline (/media/monkie/storage/pdfium/out/asan-2019-08-12/pdfium_test+0x577e2b4)
    #16 0x56122b46eb9b in Builtins_ArgumentsAdaptorTrampoline (/media/monkie/storage/pdfium/out/asan-2019-08-12/pdfium_test+0x5767b9b)
    #17 0x56122b4852b4 in Builtins_InterpreterEntryTrampoline (/media/monkie/storage/pdfium/out/asan-2019-08-12/pdfium_test+0x577e2b4)
    #18 0x56122b46eb9b in Builtins_ArgumentsAdaptorTrampoline (/media/monkie/storage/pdfium/out/asan-2019-08-12/pdfium_test+0x5767b9b)
    #19 0x56122b47b0fc in Builtins_JSEntryTrampoline (/media/monkie/storage/pdfium/out/asan-2019-08-12/pdfium_test+0x57740fc)
    #20 0x56122b47aed7 in Builtins_JSEntry (/media/monkie/storage/pdfium/out/asan-2019-08-12/pdfium_test+0x5773ed7)
    #21 0x5612293eec3e in Call v8/src/simulator.h:138:12
    #22 0x5612293eec3e in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution.cc:266
    #23 0x5612293ee021 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution.cc:358:10
    #24 0x561228daacb9 in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) v8/src/api.cc:4954:7
    #25 0x561228bf48fe in CFXJSE_Context::ExecuteScript(char const*, CFXJSE_Value*, CFXJSE_Value*) fxjs/xfa/cfxjse_context.cpp:300:21
    #26 0x561228c03ff3 in CFXJSE_Engine::RunScript(CXFA_Script::Type, fxcrt::StringViewTemplate<wchar_t>, CFXJSE_Value*, CXFA_Object*) fxjs/xfa/cfxjse_engine.cpp:153:23
    #27 0x56122bf062c3 in CXFA_Node::ExecuteBoolScript(CXFA_FFDocView*, CXFA_Script*, CXFA_EventParam*) xfa/fxfa/parser/cxfa_node.cpp:2696:22
    #28 0x56122bbcb50d in CXFA_FFNotify::RunScript(CXFA_Script*, CXFA_Node*) xfa/fxfa/cxfa_ffnotify.cpp:220:32
    #29 0x56122be3703f in (anonymous namespace)::RunBreakTestScript(CXFA_Script*) xfa/fxfa/layout/cxfa_viewlayoutprocessor.cpp:264:51
    #30 0x56122be31af0 in CXFA_ViewLayoutProcessor::ExecuteBreakBeforeOrAfter(CXFA_Node const*, bool) xfa/fxfa/layout/cxfa_viewlayoutprocessor.cpp:799:23
    #31 0x56122be37d33 in CXFA_ViewLayoutProcessor::ProcessBreakBeforeOrAfter(CXFA_Node const*, bool) xfa/fxfa/layout/cxfa_viewlayoutprocessor.cpp:871:26
    #32 0x56122be37b48 in CXFA_ViewLayoutProcessor::ProcessBreakBefore(CXFA_Node const*) xfa/fxfa/layout/cxfa_viewlayoutprocessor.cpp:856:10
    #33 0x56122be0b770 in CXFA_ContentLayoutProcessor::DoLayoutFlowedContainer(bool, XFA_AttributeValue, float, float, CXFA_ContentLayoutProcessor::Context*, bool) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:1625:39
    #34 0x56122be01168 in CXFA_ContentLayoutProcessor::DoLayoutInternal(bool, float, float, CXFA_ContentLayoutProcessor::Context*) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:2066:18
    #35 0x56122bdfe20c in CXFA_ContentLayoutProcessor::DoLayout(bool, float, float) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:2045:10
    #36 0x56122be2d097 in CXFA_LayoutProcessor::DoLayout() xfa/fxfa/layout/cxfa_layoutprocessor.cpp:80:36
    #37 0x56122bb9ef2e in CXFA_FFDocView::RunLayout() xfa/fxfa/cxfa_ffdocview.cpp:459:22
    #38 0x56122bb9e82f in CXFA_FFDocView::StopLayout() xfa/fxfa/cxfa_ffdocview.cpp:136:7
    #39 0x56122c038129 in CPDFXFA_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:130:18
    #40 0x5612279e774e in FPDF_LoadXFA fpdfsdk/fpdf_view.cpp:260:32
    #41 0x561227846842 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:841:12
    #42 0x561227841f01 in main samples/pdfium_test.cc:1068:5
    #43 0x7f8e7437482f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)

0x60d00001c280 is located 32 bytes inside of 136-byte region [0x60d00001c260,0x60d00001c2e8)
freed by thread T0 here:
    #0 0x56122783f14d in operator delete(void*) /b/swarming/w/ir/k/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cc:166:3
    #1 0x56122bc02447 in CXFA_FFTextEdit::~CXFA_FFTextEdit() xfa/fxfa/cxfa_fftextedit.cpp:37:37
    #2 0x56122bbd6d9f in std::__1::default_delete<CXFA_FFWidget>::operator()(CXFA_FFWidget*) const buildtools/third_party/libc++/trunk/include/memory:2338:5
    #3 0x56122bbd6cd8 in std::__1::unique_ptr<CXFA_FFWidget, std::__1::default_delete<CXFA_FFWidget> >::reset(CXFA_FFWidget*) buildtools/third_party/libc++/trunk/include/memory:2651:7
    #4 0x56122bbcfa08 in std::__1::unique_ptr<CXFA_FFWidget, std::__1::default_delete<CXFA_FFWidget> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2605:19
    #5 0x56122bdf49c1 in CXFA_ContentLayoutItem::~CXFA_ContentLayoutItem() xfa/fxfa/layout/cxfa_contentlayoutitem.cpp:29:1
    #6 0x56122bdf4aeb in CXFA_ContentLayoutItem::~CXFA_ContentLayoutItem() xfa/fxfa/layout/cxfa_contentlayoutitem.cpp:24:51
    #7 0x56122be1de5d in fxcrt::RetainedTreeNode<CXFA_LayoutItem>::Release() core/fxcrt/retained_tree_node.h:71:7
    #8 0x56122be1e03b in fxcrt::ReleaseDeleter<CXFA_LayoutItem>::operator()(CXFA_LayoutItem*) const core/fxcrt/retain_ptr.h:20:47
    #9 0x56122be1dfd8 in std::__1::unique_ptr<CXFA_LayoutItem, fxcrt::ReleaseDeleter<CXFA_LayoutItem> >::reset(CXFA_LayoutItem*) buildtools/third_party/libc++/trunk/include/memory:2651:7
    #10 0x56122be1df28 in std::__1::unique_ptr<CXFA_LayoutItem, fxcrt::ReleaseDeleter<CXFA_LayoutItem> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2605:19
    #11 0x56122be19484 in fxcrt::RetainPtr<CXFA_LayoutItem>::~RetainPtr() core/fxcrt/retain_ptr.h:25:7
    #12 0x56122be2c2ff in fxcrt::RetainedTreeNode<CXFA_LayoutItem>::~RetainedTreeNode() core/fxcrt/retained_tree_node.h:54:7
    #13 0x56122be2bb92 in CXFA_LayoutItem::~CXFA_LayoutItem() xfa/fxfa/layout/cxfa_layoutitem.cpp:43:1
    #14 0x56122bdf49f1 in CXFA_ContentLayoutItem::~CXFA_ContentLayoutItem() xfa/fxfa/layout/cxfa_contentlayoutitem.cpp:29:1
    #15 0x56122bdf4aeb in CXFA_ContentLayoutItem::~CXFA_ContentLayoutItem() xfa/fxfa/layout/cxfa_contentlayoutitem.cpp:24:51
    #16 0x56122be1de5d in fxcrt::RetainedTreeNode<CXFA_LayoutItem>::Release() core/fxcrt/retained_tree_node.h:71:7
    #17 0x56122be1dceb in fxcrt::ReleaseDeleter<CXFA_ContentLayoutItem>::operator()(CXFA_ContentLayoutItem*) const core/fxcrt/retain_ptr.h:20:47
    #18 0x56122be1dc88 in std::__1::unique_ptr<CXFA_ContentLayoutItem, fxcrt::ReleaseDeleter<CXFA_ContentLayoutItem> >::reset(CXFA_ContentLayoutItem*) buildtools/third_party/libc++/trunk/include/memory:2651:7
    #19 0x56122be1dbd8 in std::__1::unique_ptr<CXFA_ContentLayoutItem, fxcrt::ReleaseDeleter<CXFA_ContentLayoutItem> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2605:19
    #20 0x56122be18ee4 in fxcrt::RetainPtr<CXFA_ContentLayoutItem>::~RetainPtr() core/fxcrt/retain_ptr.h:25:7
    #21 0x56122be1fd78 in std::__1::allocator<fxcrt::RetainPtr<CXFA_ContentLayoutItem> >::destroy(fxcrt::RetainPtr<CXFA_ContentLayoutItem>*) buildtools/third_party/libc++/trunk/include/memory:1880:64
    #22 0x56122be1fd4c in void std::__1::allocator_traits<std::__1::allocator<fxcrt::RetainPtr<CXFA_ContentLayoutItem> > >::__destroy<fxcrt::RetainPtr<CXFA_ContentLayoutItem> >(std::__1::integral_constant<bool, true>, std::__1::allocator<fxcrt::RetainPtr<CXFA_ContentLayoutItem> >&, fxcrt::RetainPtr<CXFA_ContentLayoutItem>*) buildtools/third_party/libc++/trunk/include/memory:1742:18
    #23 0x56122be1fcbe in void std::__1::allocator_traits<std::__1::allocator<fxcrt::RetainPtr<CXFA_ContentLayoutItem> > >::destroy<fxcrt::RetainPtr<CXFA_ContentLayoutItem> >(std::__1::allocator<fxcrt::RetainPtr<CXFA_ContentLayoutItem> >&, fxcrt::RetainPtr<CXFA_ContentLayoutItem>*) buildtools/third_party/libc++/trunk/include/memory:1595:14
    #24 0x56122be1fb7b in std::__1::__vector_base<fxcrt::RetainPtr<CXFA_ContentLayoutItem>, std::__1::allocator<fxcrt::RetainPtr<CXFA_ContentLayoutItem> > >::__destruct_at_end(fxcrt::RetainPtr<CXFA_ContentLayoutItem>*) buildtools/third_party/libc++/trunk/include/vector:426:9
    #25 0x56122be1fa7f in std::__1::__vector_base<fxcrt::RetainPtr<CXFA_ContentLayoutItem>, std::__1::allocator<fxcrt::RetainPtr<CXFA_ContentLayoutItem> > >::clear() buildtools/third_party/libc++/trunk/include/vector:369:29
    #26 0x56122be1a00b in std::__1::vector<fxcrt::RetainPtr<CXFA_ContentLayoutItem>, std::__1::allocator<fxcrt::RetainPtr<CXFA_ContentLayoutItem> > >::clear() buildtools/third_party/libc++/trunk/include/vector:772:17
    #27 0x56122be11f1c in CXFA_ContentLayoutProcessor::InsertFlowedItem(CXFA_ContentLayoutProcessor*, bool, bool, float, XFA_AttributeValue, unsigned char*, std::__1::vector<fxcrt::RetainPtr<CXFA_ContentLayoutItem>, std::__1::allocator<fxcrt::RetainPtr<CXFA_ContentLayoutItem> > > (&) [3], bool, float, float, float, float*, float*, float*, bool*, bool*, CXFA_ContentLayoutProcessor::Context*, bool) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:2449:26
    #28 0x56122be0d73c in CXFA_ContentLayoutProcessor::DoLayoutFlowedContainer(bool, XFA_AttributeValue, float, float, CXFA_ContentLayoutProcessor::Context*, bool) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:1795:23
    #29 0x56122be01168 in CXFA_ContentLayoutProcessor::DoLayoutInternal(bool, float, float, CXFA_ContentLayoutProcessor::Context*) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:2066:18

previously allocated by thread T0 here:
    #0 0x56122783e8ed in operator new(unsigned long) /b/swarming/w/ir/k/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cc:105:3
    #1 0x56122bbceaf3 in pdfium::internal::MakeUniqueResult<CXFA_FFTextEdit>::Scalar pdfium::MakeUnique<CXFA_FFTextEdit, CXFA_Node*&>(CXFA_Node*&) third_party/base/ptr_util.h:56:29
    #2 0x56122bbcae40 in CXFA_FFNotify::OnCreateContentLayoutItem(CXFA_Node*) xfa/fxfa/cxfa_ffnotify.cpp:172:17
    #3 0x56122bdf63b7 in CXFA_ContentLayoutProcessor::CreateContentLayoutItem(CXFA_Node*) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:644:27
    #4 0x56122be16a57 in CXFA_ContentLayoutProcessor::DoLayoutField() xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:2024:19
    #5 0x56122be01261 in CXFA_ContentLayoutProcessor::DoLayoutInternal(bool, float, float, CXFA_ContentLayoutProcessor::Context*) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:2084:7
    #6 0x56122bdff651 in CXFA_ContentLayoutProcessor::DoLayoutPositionedContainer(CXFA_ContentLayoutProcessor::Context*) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:1079:17
    #7 0x56122be01192 in CXFA_ContentLayoutProcessor::DoLayoutInternal(bool, float, float, CXFA_ContentLayoutProcessor::Context*) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:2073:11
    #8 0x56122be110b1 in CXFA_ContentLayoutProcessor::InsertFlowedItem(CXFA_ContentLayoutProcessor*, bool, bool, float, XFA_AttributeValue, unsigned char*, std::__1::vector<fxcrt::RetainPtr<CXFA_ContentLayoutItem>, std::__1::allocator<fxcrt::RetainPtr<CXFA_ContentLayoutItem> > > (&) [3], bool, float, float, float, float*, float*, float*, bool*, bool*, CXFA_ContentLayoutProcessor::Context*, bool) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:2354:29
    #9 0x56122be0d73c in CXFA_ContentLayoutProcessor::DoLayoutFlowedContainer(bool, XFA_AttributeValue, float, float, CXFA_ContentLayoutProcessor::Context*, bool) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:1795:23
    #10 0x56122be01168 in CXFA_ContentLayoutProcessor::DoLayoutInternal(bool, float, float, CXFA_ContentLayoutProcessor::Context*) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:2066:18
    #11 0x56122bdfe20c in CXFA_ContentLayoutProcessor::DoLayout(bool, float, float) xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp:2045:10
    #12 0x56122be2d097 in CXFA_LayoutProcessor::DoLayout() xfa/fxfa/layout/cxfa_layoutprocessor.cpp:80:36
    #13 0x56122bb9e614 in CXFA_FFDocView::DoLayout() xfa/fxfa/cxfa_ffdocview.cpp:98:30
    #14 0x56122c03810b in CPDFXFA_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:129:18
    #15 0x5612279e774e in FPDF_LoadXFA fpdfsdk/fpdf_view.cpp:260:32
    #16 0x561227846842 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:841:12
    #17 0x561227841f01 in main samples/pdfium_test.cc:1068:5
    #18 0x7f8e7437482f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)

SUMMARY: AddressSanitizer: heap-use-after-free core/fxcrt/unowned_ptr.h:91:36 in fxcrt::UnownedPtr<CXFA_ContentLayoutItem>::Get() const
Shadow bytes around the buggy address:
  0x0c1a7fffb800: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c1a7fffb810: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x0c1a7fffb820: 00 00 00 00 00 00 00 00 00 00 fa fa fa fa fa fa
  0x0c1a7fffb830: fa fa 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c1a7fffb840: 00 00 00 fa fa fa fa fa fa fa fa fa fd fd fd fd
=>0x0c1a7fffb850:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa
  0x0c1a7fffb860: fa fa fa fa fa fa fd fd fd fd fd fd fd fd fd fd
  0x0c1a7fffb870: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x0c1a7fffb880: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c1a7fffb890: fd fd fa fa fa fa fa fa fa fa fd fd fd fd fd fd
  0x0c1a7fffb8a0: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
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
==1021==ABORTING

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-15)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/931dd1b56c0398258c68500fff04f04330bde73b

commit 931dd1b56c0398258c68500fff04f04330bde73b
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu Aug 15 18:36:39 2019

Observe m_pFocusWidget across m_ArrayKeepItems.clear()

Bug: chromium:993771
Change-Id: I24d2d0cb2ea1779b8aa1def9aa6a1dd639284a85
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/59332
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/931dd1b56c0398258c68500fff04f04330bde73b/xfa/fxfa/cxfa_ffdocview.h
[modify] https://pdfium.googlesource.com/pdfium/+/931dd1b56c0398258c68500fff04f04330bde73b/xfa/fxfa/cxfa_ffdocview.cpp
[add] https://pdfium.googlesource.com/pdfium/+/931dd1b56c0398258c68500fff04f04330bde73b/testing/resources/javascript/xfa_specific/bug_993771.in
[add] https://pdfium.googlesource.com/pdfium/+/931dd1b56c0398258c68500fff04f04330bde73b/testing/resources/javascript/xfa_specific/bug_993771_expected.txt


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b1a7675a9ca7ba8489f47243c410a0468028b820

commit b1a7675a9ca7ba8489f47243c410a0468028b820
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Aug 15 22:50:12 2019

Roll src/third_party/pdfium 8b351b9d4749..d3e3a4051984 (6 commits)

https://pdfium.googlesource.com/pdfium.git/+log/8b351b9d4749..d3e3a4051984

git log 8b351b9d4749..d3e3a4051984 --date=short --no-merges --format='%ad %ae %s'
2019-08-15 thestig@chromium.org Fix nits in Harness() in a Skia test.
2019-08-15 tsepez@chromium.org Replace PDF_ENABLE_XFA with an interface in CFXJS_Engine.
2019-08-15 asweintraub@google.com Fix ClangTidy warning.
2019-08-15 tsepez@chromium.org Remove some CXFA_FFWidget usage from fpdfsdk.
2019-08-15 tsepez@chromium.org Observe m_pFocusWidget across m_ArrayKeepItems.clear()
2019-08-15 tsepez@chromium.org Observe pNewWidget across OnKillFocus

Created with:
  gclient setdep -r src/third_party/pdfium@d3e3a4051984

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.


TBR=pdfium-deps-rolls@chromium.org

Bug: chromium:993771,chromium:991899
Change-Id: Ib1964318dc2d27b34b0b5856bc40f5eb67b5345c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1756810
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#687458}

[modify] https://crrev.com/b1a7675a9ca7ba8489f47243c410a0468028b820/DEPS


### cl...@chromium.org (2019-08-16)

ClusterFuzz testcase 6213086844682240 is verified as fixed in https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=687457:687463

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2019-08-17)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-19)

[Empty comment from Monorail migration]

### pa...@chromium.org (2019-08-21)

Congrats! The Panel decided to reward $5,000 for this report!

### pa...@chromium.org (2019-08-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-08-21)

[Comment Deleted]

### na...@google.com (2019-08-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-11-23)

This issue was migrated from crbug.com/chromium/993771?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095989)*
