# pdfium (XFA): oob read+write in CFDE_TextEditEngine::AdjustGap

| Field | Value |
|-------|-------|
| **Issue ID** | [40050839](https://issues.chromium.org/issues/40050839) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pd...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-11-29 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.101 Safari/537.36

Steps to reproduce the problem:
Note that ASAN stops on the first report by default, which is a READ. To get to the WRITE (and a few additional lesser reports) export ASAN_OPTIONS=halt_on_error=0 first. I'm adding the complete reports in a separate comment.

ERROR: AddressSanitizer: heap-buffer-overflow on address 0x61900003c054
WRITE of size 560 at 0x61900003c054 thread T0
SCARINESS: 55 (multi-byte-write-heap-buffer-overflow-far-from-bounds)

    #0 0x55b04d1ac804 in __asan_memmove /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors_memintrinsics.cpp:30:3
    #1 0x55b04fc5c674 in CFDE_TextEditEngine::AdjustGap(unsigned long, unsigned long) xfa/fde/cfde_texteditengine.cpp:213:5
    #2 0x55b04fc5d3f9 in CFDE_TextEditEngine::Insert(unsigned long, fxcrt::WideString const&, CFDE_TextEditEngine::RecordOperation) xfa/fde/cfde_texteditengine.cpp:317:3

What is the expected behavior?

What went wrong?
^

Did this work before? N/A 

Chrome version: 78.0.3904.101  Channel: n/a
OS Version: 
Flash Version:

## Attachments

- [chromium-1029437.pdf](attachments/chromium-1029437.pdf) (application/pdf, 838 B)
- [chromium-1029437.evt](attachments/chromium-1029437.evt) (application/octet-stream, 47 B)
- [chromium-1029437-1.pdf](attachments/chromium-1029437-1.pdf) (application/pdf, 700 B)
- [chromium-1029437-1.evt](attachments/chromium-1029437-1.evt) (application/octet-stream, 47 B)
- [chromium-1029437-2.pdf](attachments/chromium-1029437-2.pdf) (application/pdf, 746 B)
- [chromium-1029437-2.evt](attachments/chromium-1029437-2.evt) (application/octet-stream, 47 B)

## Timeline

### pd...@gmail.com (2019-11-29)

Triggering this requires minor user interaction.

1. Click text field.
2. Enter character.

I'm attaching the event file to use with pdfium_test.

### pd...@gmail.com (2019-11-29)

And the reports.

(1)

ERROR: AddressSanitizer: container-overflow on address 0x61900003c284 at pc 0x55b04d1ac74f bp 0x7ffdc979c4b0 sp 0x7ffdc979bc78
READ of size 560 at 0x61900003c284 thread T0
SCARINESS: 26 (multi-byte-read-container-overflow)

    #0 0x55b04d1ac74e in __asan_memmove /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors_memintrinsics.cpp:30:3
    #1 0x55b04fc5c674 in CFDE_TextEditEngine::AdjustGap(unsigned long, unsigned long) xfa/fde/cfde_texteditengine.cpp:213:5
    #2 0x55b04fc5d3f9 in CFDE_TextEditEngine::Insert(unsigned long, fxcrt::WideString const&, CFDE_TextEditEngine::RecordOperation) xfa/fde/cfde_texteditengine.cpp:317:3
    #3 0x55b04fcc0b08 in CFWL_Edit::OnChar(CFWL_MessageKey*) xfa/fwl/cfwl_edit.cpp:1266:19
    #4 0x55b04fcbf274 in CFWL_Edit::OnProcessMessage(CFWL_Message*) xfa/fwl/cfwl_edit.cpp:1040:9
    #5 0x55b04fc021f0 in CXFA_FFTextEdit::OnProcessMessage(CFWL_Message*) xfa/fxfa/cxfa_fftextedit.cpp:328:19
    #6 0x55b04fc0221c in non-virtual thunk to CXFA_FFTextEdit::OnProcessMessage(CFWL_Message*) xfa/fxfa/cxfa_fftextedit.cpp
    #7 0x55b04fcd93cc in CFWL_NoteDriver::DispatchMessage(CFWL_Message*, CFWL_Widget*) xfa/fwl/cfwl_notedriver.cpp:148:16
    #8 0x55b04fcd928d in CFWL_NoteDriver::ProcessMessage(std::__1::unique_ptr<CFWL_Message, std::__1::default_delete<CFWL_Message> >) xfa/fwl/cfwl_notedriver.cpp:108:8
    #9 0x55b04fce9865 in CFWL_WidgetMgr::OnProcessMessageToForm(std::__1::unique_ptr<CFWL_Message, std::__1::default_delete<CFWL_Message> >) xfa/fwl/cfwl_widgetmgr.cpp:320:16
    #10 0x55b04fbd3ace in CXFA_FFField::SendMessageToFWLWidget(std::__1::unique_ptr<CFWL_Message, std::__1::default_delete<CFWL_Message> >) xfa/fxfa/cxfa_fffield.cpp:712:32
    #11 0x55b04fbd6d1e in CXFA_FFField::OnChar(unsigned int, unsigned int) xfa/fxfa/cxfa_fffield.cpp:546:3
    #12 0x55b04fc07834 in CXFA_FFWidgetHandler::OnChar(CXFA_FFWidget*, unsigned int, unsigned int) xfa/fxfa/cxfa_ffwidgethandler.cpp:146:24
    #13 0x55b04fe80cbe in CPDFXFA_WidgetHandler::OnChar(CPDFSDK_Annot*, unsigned int, unsigned int) fpdfsdk/fpdfxfa/cpdfxfa_widgethandler.cpp:532:26
    #14 0x55b04d1fdace in CPDFSDK_AnnotHandlerMgr::Annot_OnChar(CPDFSDK_Annot*, unsigned int, unsigned int) fpdfsdk/cpdfsdk_annothandlermgr.cpp:230:35
    #15 0x55b04d257cd5 in CPDFSDK_PageView::OnChar(int, unsigned int) fpdfsdk/cpdfsdk_pageview.cpp:461:30
    #16 0x55b04d27b102 in FORM_OnChar fpdfsdk/fpdf_formfill.cpp:479:21
    #17 0x55b04d1eb65c in (anonymous namespace)::SendCharCodeEvent(fpdf_form_handle_t__*, fpdf_page_t__*, std::__1::vector<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::allocator<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > > > const&) samples/pdfium_test_event_helper.cc:26:3
    #18 0x55b04d1eb39f in SendPageEvents(fpdf_form_handle_t__*, fpdf_page_t__*, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test_event_helper.cc:134:7
    #19 0x55b04d1e2dff in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:674:5
    #20 0x55b04d1dca19 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:934:9
    #21 0x55b04d1d963d in main samples/pdfium_test.cc:1145:5

0x61900003c4b0 is located 0 bytes to the right of 1072-byte region [0x61900003c080,0x61900003c4b0)
allocated by thread T0 here:
    #0 0x55b04d1d63ed in operator new(unsigned long) /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x55b04d1ddc68 in std::__1::__libcpp_allocate(unsigned long, unsigned long) buildtools/third_party/libc++/trunk/include/new:238:10
    #2 0x55b04d28aea3 in std::__1::allocator<wchar_t>::allocate(unsigned long, void const*) buildtools/third_party/libc++/trunk/include/memory:1813:37
    #3 0x55b04d28ac9a in std::__1::allocator_traits<std::__1::allocator<wchar_t> >::allocate(std::__1::allocator<wchar_t>&, unsigned long) buildtools/third_party/libc++/trunk/include/memory:1546:21
    #4 0x55b04fc67b7d in std::__1::__split_buffer<wchar_t, std::__1::allocator<wchar_t>&>::__split_buffer(unsigned long, unsigned long, std::__1::allocator<wchar_t>&) buildtools/third_party/libc++/trunk/include/__split_buffer:311:29
    #5 0x55b04fc6758d in std::__1::vector<wchar_t, std::__1::allocator<wchar_t> >::__append(unsigned long) buildtools/third_party/libc++/trunk/include/vector:1091:53
    #6 0x55b04fc5bf04 in std::__1::vector<wchar_t, std::__1::allocator<wchar_t> >::resize(unsigned long) buildtools/third_party/libc++/trunk/include/vector:2052:15
    #7 0x55b04fc5c5e4 in CFDE_TextEditEngine::AdjustGap(unsigned long, unsigned long) xfa/fde/cfde_texteditengine.cpp:211:14
    #8 0x55b04fc5d3f9 in CFDE_TextEditEngine::Insert(unsigned long, fxcrt::WideString const&, CFDE_TextEditEngine::RecordOperation) xfa/fde/cfde_texteditengine.cpp:317:3
    #9 0x55b04fcb9d8d in CFWL_Edit::SetTextSkipNotify(fxcrt::WideString const&) xfa/fwl/cfwl_edit.cpp:172:15
    #10 0x55b04fc01a07 in CXFA_FFTextEdit::UpdateFWLData() xfa/fxfa/cxfa_fftextedit.cpp:289:12
    #11 0x55b04fc00cc3 in CXFA_FFTextEdit::OnSetFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_fftextedit.cpp:157:5
    #12 0x55b04fbc865c in CXFA_FFDocView::SetFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_ffdocview.cpp:296:23
    #13 0x55b04fc06a3a in CXFA_FFWidgetHandler::OnLButtonDown(CXFA_FFWidget*, unsigned int, CFX_PTemplate<float> const&) xfa/fxfa/cxfa_ffwidgethandler.cpp:53:21
    #14 0x55b04fe808fb in CPDFXFA_WidgetHandler::OnLButtonDown(CPDFSDK_PageView*, fxcrt::ObservedPtr<CPDFSDK_Annot>*, unsigned int, CFX_PTemplate<float> const&) fpdfsdk/fpdfxfa/cpdfxfa_widgethandler.cpp:407:26
    #15 0x55b04d1fd6e8 in CPDFSDK_AnnotHandlerMgr::Annot_OnLButtonDown(CPDFSDK_PageView*, fxcrt::ObservedPtr<CPDFSDK_Annot>*, unsigned int, CFX_PTemplate<float> const&) fpdfsdk/cpdfsdk_annothandlermgr.cpp:147:9
    #16 0x55b04d2571ea in CPDFSDK_PageView::OnLButtonDown(CFX_PTemplate<float> const&, unsigned int) fpdfsdk/cpdfsdk_pageview.cpp:294:26
    #17 0x55b04d27abeb in FORM_OnLButtonDown fpdfsdk/fpdf_formfill.cpp:386:21
    #18 0x55b04d1eb8ed in (anonymous namespace)::SendMouseDownEvent(fpdf_form_handle_t__*, fpdf_page_t__*, std::__1::vector<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::allocator<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > > > const&) samples/pdfium_test_event_helper.cc:67:5
    #19 0x55b04d1eb40e in SendPageEvents(fpdf_form_handle_t__*, fpdf_page_t__*, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test_event_helper.cc:138:7
    #20 0x55b04d1e2dff in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:674:5
    #21 0x55b04d1dca19 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:934:9
    #22 0x55b04d1d963d in main samples/pdfium_test.cc:1145:5

Shadow bytes around the buggy address:
  0x0c327ffff800: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c327ffff810: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c327ffff820: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c327ffff830: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c327ffff840: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c327ffff850:[04]fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc
  0x0c327ffff860: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc
  0x0c327ffff870: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc
  0x0c327ffff880: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc
  0x0c327ffff890: fc fc fc fc fc fc fa fa fa fa fa fa fa fa fa fa
  0x0c327ffff8a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

(2)

ERROR: AddressSanitizer: heap-buffer-overflow on address 0x61900003c054 at pc 0x55b04d1ac805 bp 0x7ffdc979c4b0 sp 0x7ffdc979bc78
WRITE of size 560 at 0x61900003c054 thread T0
SCARINESS: 55 (multi-byte-write-heap-buffer-overflow-far-from-bounds)

    #0 0x55b04d1ac804 in __asan_memmove /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors_memintrinsics.cpp:30:3
    #1 0x55b04fc5c674 in CFDE_TextEditEngine::AdjustGap(unsigned long, unsigned long) xfa/fde/cfde_texteditengine.cpp:213:5
    #2 0x55b04fc5d3f9 in CFDE_TextEditEngine::Insert(unsigned long, fxcrt::WideString const&, CFDE_TextEditEngine::RecordOperation) xfa/fde/cfde_texteditengine.cpp:317:3
    #3 0x55b04fcc0b08 in CFWL_Edit::OnChar(CFWL_MessageKey*) xfa/fwl/cfwl_edit.cpp:1266:19
    #4 0x55b04fcbf274 in CFWL_Edit::OnProcessMessage(CFWL_Message*) xfa/fwl/cfwl_edit.cpp:1040:9
    #5 0x55b04fc021f0 in CXFA_FFTextEdit::OnProcessMessage(CFWL_Message*) xfa/fxfa/cxfa_fftextedit.cpp:328:19
    #6 0x55b04fc0221c in non-virtual thunk to CXFA_FFTextEdit::OnProcessMessage(CFWL_Message*) xfa/fxfa/cxfa_fftextedit.cpp
    #7 0x55b04fcd93cc in CFWL_NoteDriver::DispatchMessage(CFWL_Message*, CFWL_Widget*) xfa/fwl/cfwl_notedriver.cpp:148:16
    #8 0x55b04fcd928d in CFWL_NoteDriver::ProcessMessage(std::__1::unique_ptr<CFWL_Message, std::__1::default_delete<CFWL_Message> >) xfa/fwl/cfwl_notedriver.cpp:108:8
    #9 0x55b04fce9865 in CFWL_WidgetMgr::OnProcessMessageToForm(std::__1::unique_ptr<CFWL_Message, std::__1::default_delete<CFWL_Message> >) xfa/fwl/cfwl_widgetmgr.cpp:320:16
    #10 0x55b04fbd3ace in CXFA_FFField::SendMessageToFWLWidget(std::__1::unique_ptr<CFWL_Message, std::__1::default_delete<CFWL_Message> >) xfa/fxfa/cxfa_fffield.cpp:712:32
    #11 0x55b04fbd6d1e in CXFA_FFField::OnChar(unsigned int, unsigned int) xfa/fxfa/cxfa_fffield.cpp:546:3
    #12 0x55b04fc07834 in CXFA_FFWidgetHandler::OnChar(CXFA_FFWidget*, unsigned int, unsigned int) xfa/fxfa/cxfa_ffwidgethandler.cpp:146:24
    #13 0x55b04fe80cbe in CPDFXFA_WidgetHandler::OnChar(CPDFSDK_Annot*, unsigned int, unsigned int) fpdfsdk/fpdfxfa/cpdfxfa_widgethandler.cpp:532:26
    #14 0x55b04d1fdace in CPDFSDK_AnnotHandlerMgr::Annot_OnChar(CPDFSDK_Annot*, unsigned int, unsigned int) fpdfsdk/cpdfsdk_annothandlermgr.cpp:230:35
    #15 0x55b04d257cd5 in CPDFSDK_PageView::OnChar(int, unsigned int) fpdfsdk/cpdfsdk_pageview.cpp:461:30
    #16 0x55b04d27b102 in FORM_OnChar fpdfsdk/fpdf_formfill.cpp:479:21
    #17 0x55b04d1eb65c in (anonymous namespace)::SendCharCodeEvent(fpdf_form_handle_t__*, fpdf_page_t__*, std::__1::vector<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::allocator<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > > > const&) samples/pdfium_test_event_helper.cc:26:3
    #18 0x55b04d1eb39f in SendPageEvents(fpdf_form_handle_t__*, fpdf_page_t__*, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test_event_helper.cc:134:7
    #19 0x55b04d1e2dff in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:674:5
    #20 0x55b04d1dca19 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:934:9
    #21 0x55b04d1d963d in main samples/pdfium_test.cc:1145:5

0x61900003c054 is located 44 bytes to the left of 1072-byte region [0x61900003c080,0x61900003c4b0)
allocated by thread T0 here:
    #0 0x55b04d1d63ed in operator new(unsigned long) /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x55b04d1ddc68 in std::__1::__libcpp_allocate(unsigned long, unsigned long) buildtools/third_party/libc++/trunk/include/new:238:10
    #2 0x55b04d28aea3 in std::__1::allocator<wchar_t>::allocate(unsigned long, void const*) buildtools/third_party/libc++/trunk/include/memory:1813:37
    #3 0x55b04d28ac9a in std::__1::allocator_traits<std::__1::allocator<wchar_t> >::allocate(std::__1::allocator<wchar_t>&, unsigned long) buildtools/third_party/libc++/trunk/include/memory:1546:21
    #4 0x55b04fc67b7d in std::__1::__split_buffer<wchar_t, std::__1::allocator<wchar_t>&>::__split_buffer(unsigned long, unsigned long, std::__1::allocator<wchar_t>&) buildtools/third_party/libc++/trunk/include/__split_buffer:311:29
    #5 0x55b04fc6758d in std::__1::vector<wchar_t, std::__1::allocator<wchar_t> >::__append(unsigned long) buildtools/third_party/libc++/trunk/include/vector:1091:53
    #6 0x55b04fc5bf04 in std::__1::vector<wchar_t, std::__1::allocator<wchar_t> >::resize(unsigned long) buildtools/third_party/libc++/trunk/include/vector:2052:15
    #7 0x55b04fc5c5e4 in CFDE_TextEditEngine::AdjustGap(unsigned long, unsigned long) xfa/fde/cfde_texteditengine.cpp:211:14
    #8 0x55b04fc5d3f9 in CFDE_TextEditEngine::Insert(unsigned long, fxcrt::WideString const&, CFDE_TextEditEngine::RecordOperation) xfa/fde/cfde_texteditengine.cpp:317:3
    #9 0x55b04fcb9d8d in CFWL_Edit::SetTextSkipNotify(fxcrt::WideString const&) xfa/fwl/cfwl_edit.cpp:172:15
    #10 0x55b04fc01a07 in CXFA_FFTextEdit::UpdateFWLData() xfa/fxfa/cxfa_fftextedit.cpp:289:12
    #11 0x55b04fc00cc3 in CXFA_FFTextEdit::OnSetFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_fftextedit.cpp:157:5
    #12 0x55b04fbc865c in CXFA_FFDocView::SetFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_ffdocview.cpp:296:23
    #13 0x55b04fc06a3a in CXFA_FFWidgetHandler::OnLButtonDown(CXFA_FFWidget*, unsigned int, CFX_PTemplate<float> const&) xfa/fxfa/cxfa_ffwidgethandler.cpp:53:21
    #14 0x55b04fe808fb in CPDFXFA_WidgetHandler::OnLButtonDown(CPDFSDK_PageView*, fxcrt::ObservedPtr<CPDFSDK_Annot>*, unsigned int, CFX_PTemplate<float> const&) fpdfsdk/fpdfxfa/cpdfxfa_widgethandler.cpp:407:26
    #15 0x55b04d1fd6e8 in CPDFSDK_AnnotHandlerMgr::Annot_OnLButtonDown(CPDFSDK_PageView*, fxcrt::ObservedPtr<CPDFSDK_Annot>*, unsigned int, CFX_PTemplate<float> const&) fpdfsdk/cpdfsdk_annothandlermgr.cpp:147:9
    #16 0x55b04d2571ea in CPDFSDK_PageView::OnLButtonDown(CFX_PTemplate<float> const&, unsigned int) fpdfsdk/cpdfsdk_pageview.cpp:294:26
    #17 0x55b04d27abeb in FORM_OnLButtonDown fpdfsdk/fpdf_formfill.cpp:386:21
    #18 0x55b04d1eb8ed in (anonymous namespace)::SendMouseDownEvent(fpdf_form_handle_t__*, fpdf_page_t__*, std::__1::vector<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::allocator<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > > > const&) samples/pdfium_test_event_helper.cc:67:5
    #19 0x55b04d1eb40e in SendPageEvents(fpdf_form_handle_t__*, fpdf_page_t__*, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test_event_helper.cc:138:7
    #20 0x55b04d1e2dff in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:674:5
    #21 0x55b04d1dca19 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:934:9
    #22 0x55b04d1d963d in main samples/pdfium_test.cc:1145:5

Shadow bytes around the buggy address:
  0x0c327ffff7b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c327ffff7c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c327ffff7d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c327ffff7e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c327ffff7f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x0c327ffff800: fa fa fa fa fa fa fa fa fa fa[fa]fa fa fa fa fa
  0x0c327ffff810: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c327ffff820: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c327ffff830: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c327ffff840: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c327ffff850: 04 fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc
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

(3)

ERROR: AddressSanitizer: heap-buffer-overflow on address 0x61900003c054 at pc 0x55b04d1ac2ea bp 0x7ffdc979c340 sp 0x7ffdc979bb08
READ of size 560 at 0x61900003c054 thread T0
SCARINESS: 36 (multi-byte-read-heap-buffer-overflow-far-from-bounds)

    #0 0x55b04d1ac2e9 in __asan_memcpy /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors_memintrinsics.cpp:22:3
    #1 0x55b04d2ca44d in fxcrt::StringDataTemplate<wchar_t>::CopyContents(wchar_t const*, unsigned long) core/fxcrt/string_data_template.h:70:5
    #2 0x55b04d2ca418 in fxcrt::StringDataTemplate<wchar_t>::Create(wchar_t const*, unsigned long) core/fxcrt/string_data_template.h:46:13
    #3 0x55b04d2cdbfc in fxcrt::WideString::Concat(wchar_t const*, unsigned long) core/fxcrt/widestring.cpp:616:19
    #4 0x55b04d2ce08c in fxcrt::WideString::operator+=(fxcrt::StringViewTemplate<wchar_t>) core/fxcrt/widestring.cpp:441:5
    #5 0x55b04fc5dd79 in CFDE_TextEditEngine::GetText() const xfa/fde/cfde_texteditengine.cpp:926:9
    #6 0x55b04fc5d799 in CFDE_TextEditEngine::Insert(unsigned long, fxcrt::WideString const&, CFDE_TextEditEngine::RecordOperation) xfa/fde/cfde_texteditengine.cpp:361:21
    #7 0x55b04fcc0b08 in CFWL_Edit::OnChar(CFWL_MessageKey*) xfa/fwl/cfwl_edit.cpp:1266:19
    #8 0x55b04fcbf274 in CFWL_Edit::OnProcessMessage(CFWL_Message*) xfa/fwl/cfwl_edit.cpp:1040:9
    #9 0x55b04fc021f0 in CXFA_FFTextEdit::OnProcessMessage(CFWL_Message*) xfa/fxfa/cxfa_fftextedit.cpp:328:19
    #10 0x55b04fc0221c in non-virtual thunk to CXFA_FFTextEdit::OnProcessMessage(CFWL_Message*) xfa/fxfa/cxfa_fftextedit.cpp
    #11 0x55b04fcd93cc in CFWL_NoteDriver::DispatchMessage(CFWL_Message*, CFWL_Widget*) xfa/fwl/cfwl_notedriver.cpp:148:16
    #12 0x55b04fcd928d in CFWL_NoteDriver::ProcessMessage(std::__1::unique_ptr<CFWL_Message, std::__1::default_delete<CFWL_Message> >) xfa/fwl/cfwl_notedriver.cpp:108:8
    #13 0x55b04fce9865 in CFWL_WidgetMgr::OnProcessMessageToForm(std::__1::unique_ptr<CFWL_Message, std::__1::default_delete<CFWL_Message> >) xfa/fwl/cfwl_widgetmgr.cpp:320:16
    #14 0x55b04fbd3ace in CXFA_FFField::SendMessageToFWLWidget(std::__1::unique_ptr<CFWL_Message, std::__1::default_delete<CFWL_Message> >) xfa/fxfa/cxfa_fffield.cpp:712:32
    #15 0x55b04fbd6d1e in CXFA_FFField::OnChar(unsigned int, unsigned int) xfa/fxfa/cxfa_fffield.cpp:546:3
    #16 0x55b04fc07834 in CXFA_FFWidgetHandler::OnChar(CXFA_FFWidget*, unsigned int, unsigned int) xfa/fxfa/cxfa_ffwidgethandler.cpp:146:24
    #17 0x55b04fe80cbe in CPDFXFA_WidgetHandler::OnChar(CPDFSDK_Annot*, unsigned int, unsigned int) fpdfsdk/fpdfxfa/cpdfxfa_widgethandler.cpp:532:26
    #18 0x55b04d1fdace in CPDFSDK_AnnotHandlerMgr::Annot_OnChar(CPDFSDK_Annot*, unsigned int, unsigned int) fpdfsdk/cpdfsdk_annothandlermgr.cpp:230:35
    #19 0x55b04d257cd5 in CPDFSDK_PageView::OnChar(int, unsigned int) fpdfsdk/cpdfsdk_pageview.cpp:461:30
    #20 0x55b04d27b102 in FORM_OnChar fpdfsdk/fpdf_formfill.cpp:479:21
    #21 0x55b04d1eb65c in (anonymous namespace)::SendCharCodeEvent(fpdf_form_handle_t__*, fpdf_page_t__*, std::__1::vector<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::allocator<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > > > const&) samples/pdfium_test_event_helper.cc:26:3
    #22 0x55b04d1eb39f in SendPageEvents(fpdf_form_handle_t__*, fpdf_page_t__*, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test_event_helper.cc:134:7
    #23 0x55b04d1e2dff in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:674:5
    #24 0x55b04d1dca19 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:934:9
    #25 0x55b04d1d963d in main samples/pdfium_test.cc:1145:5

0x61900003c054 is located 212 bytes to the right of 1024-byte region [0x61900003bb80,0x61900003bf80)
allocated by thread T0 here:
    #0 0x55b04d1d63ed in operator new(unsigned long) /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x55b04d1ddc68 in std::__1::__libcpp_allocate(unsigned long, unsigned long) buildtools/third_party/libc++/trunk/include/new:238:10
    #2 0x55b04fc697f3 in std::__1::allocator<std::__1::unique_ptr<CFDE_TextEditEngine::Operation, std::__1::default_delete<CFDE_TextEditEngine::Operation> > >::allocate(unsigned long, void const*) buildtools/third_party/libc++/trunk/include/memory:1813:37
    #3 0x55b04fc6975a in std::__1::allocator_traits<std::__1::allocator<std::__1::unique_ptr<CFDE_TextEditEngine::Operation, std::__1::default_delete<CFDE_TextEditEngine::Operation> > > >::allocate(std::__1::allocator<std::__1::unique_ptr<CFDE_TextEditEngine::Operation, std::__1::default_delete<CFDE_TextEditEngine::Operation> > >&, unsigned long) buildtools/third_party/libc++/trunk/include/memory:1546:21
    #4 0x55b04fc68d8d in std::__1::__split_buffer<std::__1::unique_ptr<CFDE_TextEditEngine::Operation, std::__1::default_delete<CFDE_TextEditEngine::Operation> >, std::__1::allocator<std::__1::unique_ptr<CFDE_TextEditEngine::Operation, std::__1::default_delete<CFDE_TextEditEngine::Operation> > >&>::__split_buffer(unsigned long, unsigned long, std::__1::allocator<std::__1::unique_ptr<CFDE_TextEditEngine::Operation, std::__1::default_delete<CFDE_TextEditEngine::Operation> > >&) buildtools/third_party/libc++/trunk/include/__split_buffer:311:29
    #5 0x55b04fc6879d in std::__1::vector<std::__1::unique_ptr<CFDE_TextEditEngine::Operation, std::__1::default_delete<CFDE_TextEditEngine::Operation> >, std::__1::allocator<std::__1::unique_ptr<CFDE_TextEditEngine::Operation, std::__1::default_delete<CFDE_TextEditEngine::Operation> > > >::__append(unsigned long) buildtools/third_party/libc++/trunk/include/vector:1091:53
    #6 0x55b04fc5bf64 in std::__1::vector<std::__1::unique_ptr<CFDE_TextEditEngine::Operation, std::__1::default_delete<CFDE_TextEditEngine::Operation> >, std::__1::allocator<std::__1::unique_ptr<CFDE_TextEditEngine::Operation, std::__1::default_delete<CFDE_TextEditEngine::Operation> > > >::resize(unsigned long) buildtools/third_party/libc++/trunk/include/vector:2052:15
    #7 0x55b04fc5bd30 in CFDE_TextEditEngine::CFDE_TextEditEngine() xfa/fde/cfde_texteditengine.cpp:165:21
    #8 0x55b04fcb6477 in CFWL_Edit::CFWL_Edit(CFWL_App const*, std::__1::unique_ptr<CFWL_WidgetProperties, std::__1::default_delete<CFWL_WidgetProperties> >, CFWL_Widget*) xfa/fwl/cfwl_edit.cpp:49:12
    #9 0x55b04fbeb8f2 in pdfium::internal::MakeUniqueResult<CFWL_Edit>::Scalar pdfium::MakeUnique<CFWL_Edit, CFWL_App const*, std::__1::unique_ptr<CFWL_WidgetProperties, std::__1::default_delete<CFWL_WidgetProperties> >, std::nullptr_t>(CFWL_App const*&&, std::__1::unique_ptr<CFWL_WidgetProperties, std::__1::default_delete<CFWL_WidgetProperties> >&&, std::nullptr_t&&) third_party/base/ptr_util.h:56:33
    #10 0x55b04fbff984 in CXFA_FFTextEdit::LoadWidget() xfa/fxfa/cxfa_fftextedit.cpp:45:21
    #11 0x55b04fbed9a9 in CXFA_FFPageWidgetIterator::GetWidget(CXFA_LayoutItem*) xfa/fxfa/cxfa_ffpageview.cpp:218:19
    #12 0x55b04fbedbf7 in CXFA_FFPageWidgetIterator::MoveToNext() xfa/fxfa/cxfa_ffpageview.cpp:181:34
    #13 0x55b04d25808c in CPDFSDK_PageView::LoadFXAnnots() fpdfsdk/cpdfsdk_pageview.cpp:500:55
    #14 0x55b04d23c345 in CPDFSDK_FormFillEnvironment::GetPageView(IPDF_Page*, bool) fpdfsdk/cpdfsdk_formfillenvironment.cpp:577:14
    #15 0x55b04d27a996 in (anonymous namespace)::FormHandleToPageView(fpdf_form_handle_t__*, fpdf_page_t__*) fpdfsdk/fpdf_formfill.cpp:171:39
    #16 0x55b04d27b8a1 in FORM_OnAfterLoadPage fpdfsdk/fpdf_formfill.cpp:619:37
    #17 0x55b04d1e29fc in (anonymous namespace)::GetPageForIndex(_FPDF_FORMFILLINFO*, fpdf_document_t__*, int) samples/pdfium_test.cc:651:3
    #18 0x55b04d1e2db9 in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:670:20
    #19 0x55b04d1dca19 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:934:9
    #20 0x55b04d1d963d in main samples/pdfium_test.cc:1145:5

Shadow bytes around the buggy address:
  0x0c327ffff7b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c327ffff7c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c327ffff7d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c327ffff7e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c327ffff7f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x0c327ffff800: fa fa fa fa fa fa fa fa fa fa[fa]fa fa fa fa fa
  0x0c327ffff810: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c327ffff820: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c327ffff830: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c327ffff840: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c327ffff850: 04 fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc
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

(4)

ERROR: AddressSanitizer: heap-buffer-overflow on address 0x61900003c054 at pc 0x55b04d2c63bf bp 0x7ffdc979c420 sp 0x7ffdc979c418
READ of size 1 at 0x61900003c054 thread T0
SCARINESS: 22 (1-byte-read-heap-buffer-overflow-far-from-bounds)

    #0 0x55b04d2c63be in fxcrt::UnownedPtr<unsigned int const>::ProbeForLowSeverityLifetimeIssue() core/fxcrt/unowned_ptr.h:113:7
    #1 0x55b04d2c6378 in fxcrt::UnownedPtr<unsigned int const>::~UnownedPtr() core/fxcrt/unowned_ptr.h:60:19
    #2 0x55b04d2c6332 in pdfium::span<unsigned int const>::~span() third_party/base/span.h:220:3
    #3 0x55b04d2c5a78 in fxcrt::StringViewTemplate<wchar_t>::~StringViewTemplate() core/fxcrt/string_view_template.h:29:7
    #4 0x55b04fc5dd81 in CFDE_TextEditEngine::GetText() const xfa/fde/cfde_texteditengine.cpp:926:5
    #5 0x55b04fc5d799 in CFDE_TextEditEngine::Insert(unsigned long, fxcrt::WideString const&, CFDE_TextEditEngine::RecordOperation) xfa/fde/cfde_texteditengine.cpp:361:21
    #6 0x55b04fcc0b08 in CFWL_Edit::OnChar(CFWL_MessageKey*) xfa/fwl/cfwl_edit.cpp:1266:19
    #7 0x55b04fcbf274 in CFWL_Edit::OnProcessMessage(CFWL_Message*) xfa/fwl/cfwl_edit.cpp:1040:9
    #8 0x55b04fc021f0 in CXFA_FFTextEdit::OnProcessMessage(CFWL_Message*) xfa/fxfa/cxfa_fftextedit.cpp:328:19
    #9 0x55b04fc0221c in non-virtual thunk to CXFA_FFTextEdit::OnProcessMessage(CFWL_Message*) xfa/fxfa/cxfa_fftextedit.cpp
    #10 0x55b04fcd93cc in CFWL_NoteDriver::DispatchMessage(CFWL_Message*, CFWL_Widget*) xfa/fwl/cfwl_notedriver.cpp:148:16
    #11 0x55b04fcd928d in CFWL_NoteDriver::ProcessMessage(std::__1::unique_ptr<CFWL_Message, std::__1::default_delete<CFWL_Message> >) xfa/fwl/cfwl_notedriver.cpp:108:8
    #12 0x55b04fce9865 in CFWL_WidgetMgr::OnProcessMessageToForm(std::__1::unique_ptr<CFWL_Message, std::__1::default_delete<CFWL_Message> >) xfa/fwl/cfwl_widgetmgr.cpp:320:16
    #13 0x55b04fbd3ace in CXFA_FFField::SendMessageToFWLWidget(std::__1::unique_ptr<CFWL_Message, std::__1::default_delete<CFWL_Message> >) xfa/fxfa/cxfa_fffield.cpp:712:32
    #14 0x55b04fbd6d1e in CXFA_FFField::OnChar(unsigned int, unsigned int) xfa/fxfa/cxfa_fffield.cpp:546:3
    #15 0x55b04fc07834 in CXFA_FFWidgetHandler::OnChar(CXFA_FFWidget*, unsigned int, unsigned int) xfa/fxfa/cxfa_ffwidgethandler.cpp:146:24
    #16 0x55b04fe80cbe in CPDFXFA_WidgetHandler::OnChar(CPDFSDK_Annot*, unsigned int, unsigned int) fpdfsdk/fpdfxfa/cpdfxfa_widgethandler.cpp:532:26
    #17 0x55b04d1fdace in CPDFSDK_AnnotHandlerMgr::Annot_OnChar(CPDFSDK_Annot*, unsigned int, unsigned int) fpdfsdk/cpdfsdk_annothandlermgr.cpp:230:35
    #18 0x55b04d257cd5 in CPDFSDK_PageView::OnChar(int, unsigned int) fpdfsdk/cpdfsdk_pageview.cpp:461:30
    #19 0x55b04d27b102 in FORM_OnChar fpdfsdk/fpdf_formfill.cpp:479:21
    #20 0x55b04d1eb65c in (anonymous namespace)::SendCharCodeEvent(fpdf_form_handle_t__*, fpdf_page_t__*, std::__1::vector<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::allocator<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > > > const&) samples/pdfium_test_event_helper.cc:26:3
    #21 0x55b04d1eb39f in SendPageEvents(fpdf_form_handle_t__*, fpdf_page_t__*, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test_event_helper.cc:134:7
    #22 0x55b04d1e2dff in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:674:5
    #23 0x55b04d1dca19 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:934:9
    #24 0x55b04d1d963d in main samples/pdfium_test.cc:1145:5

0x61900003c054 is located 212 bytes to the right of 1024-byte region [0x61900003bb80,0x61900003bf80)
allocated by thread T0 here:
    #0 0x55b04d1d63ed in operator new(unsigned long) /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x55b04d1ddc68 in std::__1::__libcpp_allocate(unsigned long, unsigned long) buildtools/third_party/libc++/trunk/include/new:238:10
    #2 0x55b04fc697f3 in std::__1::allocator<std::__1::unique_ptr<CFDE_TextEditEngine::Operation, std::__1::default_delete<CFDE_TextEditEngine::Operation> > >::allocate(unsigned long, void const*) buildtools/third_party/libc++/trunk/include/memory:1813:37
    #3 0x55b04fc6975a in std::__1::allocator_traits<std::__1::allocator<std::__1::unique_ptr<CFDE_TextEditEngine::Operation, std::__1::default_delete<CFDE_TextEditEngine::Operation> > > >::allocate(std::__1::allocator<std::__1::unique_ptr<CFDE_TextEditEngine::Operation, std::__1::default_delete<CFDE_TextEditEngine::Operation> > >&, unsigned long) buildtools/third_party/libc++/trunk/include/memory:1546:21
    #4 0x55b04fc68d8d in std::__1::__split_buffer<std::__1::unique_ptr<CFDE_TextEditEngine::Operation, std::__1::default_delete<CFDE_TextEditEngine::Operation> >, std::__1::allocator<std::__1::unique_ptr<CFDE_TextEditEngine::Operation, std::__1::default_delete<CFDE_TextEditEngine::Operation> > >&>::__split_buffer(unsigned long, unsigned long, std::__1::allocator<std::__1::unique_ptr<CFDE_TextEditEngine::Operation, std::__1::default_delete<CFDE_TextEditEngine::Operation> > >&) buildtools/third_party/libc++/trunk/include/__split_buffer:311:29
    #5 0x55b04fc6879d in std::__1::vector<std::__1::unique_ptr<CFDE_TextEditEngine::Operation, std::__1::default_delete<CFDE_TextEditEngine::Operation> >, std::__1::allocator<std::__1::unique_ptr<CFDE_TextEditEngine::Operation, std::__1::default_delete<CFDE_TextEditEngine::Operation> > > >::__append(unsigned long) buildtools/third_party/libc++/trunk/include/vector:1091:53
    #6 0x55b04fc5bf64 in std::__1::vector<std::__1::unique_ptr<CFDE_TextEditEngine::Operation, std::__1::default_delete<CFDE_TextEditEngine::Operation> >, std::__1::allocator<std::__1::unique_ptr<CFDE_TextEditEngine::Operation, std::__1::default_delete<CFDE_TextEditEngine::Operation> > > >::resize(unsigned long) buildtools/third_party/libc++/trunk/include/vector:2052:15
    #7 0x55b04fc5bd30 in CFDE_TextEditEngine::CFDE_TextEditEngine() xfa/fde/cfde_texteditengine.cpp:165:21
    #8 0x55b04fcb6477 in CFWL_Edit::CFWL_Edit(CFWL_App const*, std::__1::unique_ptr<CFWL_WidgetProperties, std::__1::default_delete<CFWL_WidgetProperties> >, CFWL_Widget*) xfa/fwl/cfwl_edit.cpp:49:12
    #9 0x55b04fbeb8f2 in pdfium::internal::MakeUniqueResult<CFWL_Edit>::Scalar pdfium::MakeUnique<CFWL_Edit, CFWL_App const*, std::__1::unique_ptr<CFWL_WidgetProperties, std::__1::default_delete<CFWL_WidgetProperties> >, std::nullptr_t>(CFWL_App const*&&, std::__1::unique_ptr<CFWL_WidgetProperties, std::__1::default_delete<CFWL_WidgetProperties> >&&, std::nullptr_t&&) third_party/base/ptr_util.h:56:33
    #10 0x55b04fbff984 in CXFA_FFTextEdit::LoadWidget() xfa/fxfa/cxfa_fftextedit.cpp:45:21
    #11 0x55b04fbed9a9 in CXFA_FFPageWidgetIterator::GetWidget(CXFA_LayoutItem*) xfa/fxfa/cxfa_ffpageview.cpp:218:19
    #12 0x55b04fbedbf7 in CXFA_FFPageWidgetIterator::MoveToNext() xfa/fxfa/cxfa_ffpageview.cpp:181:34
    #13 0x55b04d25808c in CPDFSDK_PageView::LoadFXAnnots() fpdfsdk/cpdfsdk_pageview.cpp:500:55
    #14 0x55b04d23c345 in CPDFSDK_FormFillEnvironment::GetPageView(IPDF_Page*, bool) fpdfsdk/cpdfsdk_formfillenvironment.cpp:577:14
    #15 0x55b04d27a996 in (anonymous namespace)::FormHandleToPageView(fpdf_form_handle_t__*, fpdf_page_t__*) fpdfsdk/fpdf_formfill.cpp:171:39
    #16 0x55b04d27b8a1 in FORM_OnAfterLoadPage fpdfsdk/fpdf_formfill.cpp:619:37
    #17 0x55b04d1e29fc in (anonymous namespace)::GetPageForIndex(_FPDF_FORMFILLINFO*, fpdf_document_t__*, int) samples/pdfium_test.cc:651:3
    #18 0x55b04d1e2db9 in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:670:20
    #19 0x55b04d1dca19 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:934:9
    #20 0x55b04d1d963d in main samples/pdfium_test.cc:1145:5

Shadow bytes around the buggy address:
  0x0c327ffff7b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c327ffff7c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c327ffff7d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c327ffff7e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c327ffff7f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x0c327ffff800: fa fa fa fa fa fa fa fa fa fa[fa]fa fa fa fa fa
  0x0c327ffff810: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c327ffff820: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c327ffff830: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c327ffff840: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c327ffff850: 04 fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc
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


### pd...@gmail.com (2019-11-29)

Note: Chrome doesn't use XFA.

### pd...@gmail.com (2019-12-01)

[Comment Deleted]

### pd...@gmail.com (2019-12-01)

There is another, lesser, bug here for text.GetLength() <= kGapSize.

ERROR: AddressSanitizer: negative-size-param: (size=-4)
SCARINESS: 10 (negative-size-param)
    #0 0x5653f3335287 in __asan_memcpy /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors_memintrinsics.cpp:22:3
    #1 0x5653f5de6806 in CFDE_TextEditEngine::Insert(unsigned long, fxcrt::WideString const&, CFDE_TextEditEngine::RecordOperation) xfa/fde/cfde_texteditengine.cpp:365:3

### pa...@chromium.org (2019-12-02)

Thanks for the report! :)

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2020-01-16)

CL at https://pdfium-review.googlesource.com/c/pdfium/+/65190

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-16)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/f133db638bd2da0eebdf434b4d157c2e5dacd63c

commit f133db638bd2da0eebdf434b4d157c2e5dacd63c
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu Jan 16 21:32:27 2020

Avoid underflow before calling CFDE_TextEditEngine::AdjustGap().

The text by itself may already exceed the limit if it was previously
granted an exemption. Increasing the limit maintains the invariant
that |text_length_| <= |character_limit_|.

-- Add the link to the explainer dsinclair suggested

Bug: chromium:1029437
Change-Id: I7962522dc8253f6070524c3342b65bd3aefca5bf
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/65190
Reviewed-by: Lei Zhang <thestig@chromium.org>
Reviewed-by: dsinclair <dsinclair@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/f133db638bd2da0eebdf434b4d157c2e5dacd63c/xfa/fde/cfde_texteditengine.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/f133db638bd2da0eebdf434b4d157c2e5dacd63c/xfa/fde/cfde_texteditengine.h
[modify] https://pdfium.googlesource.com/pdfium/+/f133db638bd2da0eebdf434b4d157c2e5dacd63c/xfa/fde/cfde_texteditengine_unittest.cpp


### ts...@chromium.org (2020-01-16)

[Empty comment from Monorail migration]

### pd...@gmail.com (2020-01-17)

Trigger for the new CHECK.

* thread #1, name = 'pdfium_test', stop reason = signal SIGTRAP
    frame #0: 0x00005555571684dd pdfium_test`CFDE_TextEditEngine::Insert(unsigned long, fxcrt::WideString const&, CFDE_TextEditEngine::RecordOperation)::$_0::operator()() const at cfde_texteditengine.cpp:317:7
   314        character_limit_ = text_length_ + length;
   315      } else {
   316        // Trucate the text to comply with the limit.
-> 317        CHECK(text_length_ <= character_limit_);
   318        length = character_limit_ - text_length_;
   319        exceeded_limit = true;
   320      }

### pd...@gmail.com (2020-01-17)

I have half-posted this on the pdfium tracker, but switched here. Your choice.

https://crbug.com/pdfium/1458

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1f115b5af5f5f1b76a362e56085ff432484def6d

commit 1f115b5af5f5f1b76a362e56085ff432484def6d
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Jan 17 04:53:34 2020

Roll src/third_party/pdfium c86e356c31a9..7891b46fd46e (4 commits)

https://pdfium.googlesource.com/pdfium.git/+log/c86e356c31a9..7891b46fd46e

git log c86e356c31a9..7891b46fd46e --date=short --first-parent --format='%ad %ae %s'
2020-01-16 dhoss@chromium.org Add nullptr checks prior to accesses of CPDF_Document::GetDocExtension()
2020-01-16 tsepez@chromium.org Remove unused one-arg form of IsAppearanceValid().
2020-01-16 tsepez@chromium.org Add test for growing gap in CFDE_TextEditEngine::AdjustGap().
2020-01-16 tsepez@chromium.org Avoid underflow before calling CFDE_TextEditEngine::AdjustGap().

Created with:
  gclient setdep -r src/third_party/pdfium@7891b46fd46e

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1029437
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I9219e3f50942bdc59bd2c03d723e85040948ef14
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2006611
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#732722}

[modify] https://crrev.com/1f115b5af5f5f1b76a362e56085ff432484def6d/DEPS


### sh...@chromium.org (2020-01-17)

[Empty comment from Monorail migration]

### ts...@chromium.org (2020-01-17)

C10 - not surprising, I was leery of the arithmetic in this code, which I why I added the CHECK().  We can track this follow-up on https://crbug.com/pdfium/1458 since a CHECK() isn't a security issue per-se (It's annoying, but it can't be used by an adversary to launch an exploit obtaining information to which they are not entitled).

### na...@google.com (2020-01-21)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-01-23)

Congrats the Panel decided to reward $5,000 for this report!

### na...@google.com (2020-01-23)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-04-24)

This issue was migrated from crbug.com/chromium/1029437?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050839)*
