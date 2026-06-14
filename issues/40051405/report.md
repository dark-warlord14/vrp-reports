# pdfium (XFA): oob read / use-of-uninitialized-value in CXFA_Node::SetSelectedItems

| Field | Value |
|-------|-------|
| **Issue ID** | [40051405](https://issues.chromium.org/issues/40051405) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pd...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2020-02-01 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.130 Safari/537.36

Steps to reproduce the problem:
ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000028978 at pc 0x5566de033c46 bp 0x7ffc2b6b50a0 sp 0x7ffc2b6b5098
READ of size 8 at 0x602000028978 thread T0
SCARINESS: 23 (8-byte-read-heap-buffer-overflow)

    #0 0x5566de033c45 in std::__1::unique_ptr<fxcrt::StringDataTemplate<wchar_t>, fxcrt::ReleaseDeleter<fxcrt::StringDataTemplate<wchar_t> > >::get() const buildtools/third_party/libc++/trunk/include/memory:2606:19
    #1 0x5566de118c68 in fxcrt::RetainPtr<fxcrt::StringDataTemplate<wchar_t> >::Get() const core/fxcrt/retain_ptr.h:56:34
    #2 0x5566de112a70 in fxcrt::RetainPtr<fxcrt::StringDataTemplate<wchar_t> >::RetainPtr(fxcrt::RetainPtr<fxcrt::StringDataTemplate<wchar_t> > const&) core/fxcrt/retain_ptr.h:33:53
    #3 0x5566de112a58 in fxcrt::WideString::WideString(fxcrt::WideString const&) core/fxcrt/widestring.cpp:327:51
    #4 0x5566e0e29faf in CXFA_Node::SetSelectedItems(std::__1::vector<int, std::__1::allocator<int> > const&, bool, bool, bool) xfa/fxfa/parser/cxfa_node.cpp:4361:36
    #5 0x5566e0c44b60 in CXFA_FFListBox::CommitData() xfa/fxfa/cxfa_fflistbox.cpp:90:12
    #6 0x5566e0c3ed1b in CXFA_FFField::ProcessCommittedData() xfa/fxfa/cxfa_fffield.cpp:649:10
    #7 0x5566e0c4447e in CXFA_FFListBox::OnKillFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_fflistbox.cpp:76:8
    #8 0x5566e0c2ed7a in CXFA_FFDocView::SetFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_ffdocview.cpp:306:26
    #9 0x5566e0eee614 in CPDFXFA_WidgetHandler::OnKillFocus(fxcrt::ObservedPtr<CPDFSDK_Annot>*, unsigned int) fpdfsdk/fpdfxfa/cpdfxfa_widgethandler.cpp:575:31
    #10 0x5566de03b678 in CPDFSDK_AnnotHandlerMgr::Annot_OnKillFocus(fxcrt::ObservedPtr<CPDFSDK_Annot>*, unsigned int) fpdfsdk/cpdfsdk_annothandlermgr.cpp:269:42
    #11 0x5566de07d486 in CPDFSDK_FormFillEnvironment::KillFocusAnnot(unsigned int) fpdfsdk/cpdfsdk_formfillenvironment.cpp:726:23
    #12 0x5566de07e489 in CPDFSDK_FormFillEnvironment::RemovePageView(IPDF_Page*) fpdfsdk/cpdfsdk_formfillenvironment.cpp:646:5
    #13 0x5566de0be813 in FORM_OnBeforeClosePage fpdfsdk/fpdf_formfill.cpp:645:19
    #14 0x5566de022722 in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:812:3
    #15 0x5566de01bab8 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:962:9
    #16 0x5566de0180ea in main samples/pdfium_test.cc:1181:5

0x602000028978 is located 0 bytes to the right of 8-byte region [0x602000028970,0x602000028978)
allocated by thread T0 here:
    #0 0x5566de01517d in operator new(unsigned long) /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x5566de01cd98 in std::__1::__libcpp_allocate(unsigned long, unsigned long) buildtools/third_party/libc++/trunk/include/new:253:10
    #2 0x5566de128023 in std::__1::allocator<fxcrt::WideString>::allocate(unsigned long, void const*) buildtools/third_party/libc++/trunk/include/memory:1853:37
    #3 0x5566de127f1a in std::__1::allocator_traits<std::__1::allocator<fxcrt::WideString> >::allocate(std::__1::allocator<fxcrt::WideString>&, unsigned long) buildtools/third_party/libc++/trunk/include/memory:1570:21
    #4 0x5566de12857d in std::__1::__split_buffer<fxcrt::WideString, std::__1::allocator<fxcrt::WideString>&>::__split_buffer(unsigned long, unsigned long, std::__1::allocator<fxcrt::WideString>&) buildtools/third_party/libc++/trunk/include/__split_buffer:318:29
    #5 0x5566e0e64f5e in void std::__1::vector<fxcrt::WideString, std::__1::allocator<fxcrt::WideString> >::__emplace_back_slow_path<fxcrt::WideString>(fxcrt::WideString&&) buildtools/third_party/libc++/trunk/include/vector:1664:49
    #6 0x5566e0e28092 in void std::__1::vector<fxcrt::WideString, std::__1::allocator<fxcrt::WideString> >::emplace_back<fxcrt::WideString>(fxcrt::WideString&&) buildtools/third_party/libc++/trunk/include/vector:1686:9
    #7 0x5566e0e27f15 in CXFA_Node::GetChoiceListItems(bool) xfa/fxfa/parser/cxfa_node.cpp:4243:17
    #8 0x5566e0e29f09 in CXFA_Node::SetSelectedItems(std::__1::vector<int, std::__1::allocator<int> > const&, bool, bool, bool) xfa/fxfa/parser/cxfa_node.cpp:4358:47
    #9 0x5566e0c44b60 in CXFA_FFListBox::CommitData() xfa/fxfa/cxfa_fflistbox.cpp:90:12
    #10 0x5566e0c3ed1b in CXFA_FFField::ProcessCommittedData() xfa/fxfa/cxfa_fffield.cpp:649:10
    #11 0x5566e0c4447e in CXFA_FFListBox::OnKillFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_fflistbox.cpp:76:8
    #12 0x5566e0c2ed7a in CXFA_FFDocView::SetFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_ffdocview.cpp:306:26
    #13 0x5566e0eee614 in CPDFXFA_WidgetHandler::OnKillFocus(fxcrt::ObservedPtr<CPDFSDK_Annot>*, unsigned int) fpdfsdk/fpdfxfa/cpdfxfa_widgethandler.cpp:575:31
    #14 0x5566de03b678 in CPDFSDK_AnnotHandlerMgr::Annot_OnKillFocus(fxcrt::ObservedPtr<CPDFSDK_Annot>*, unsigned int) fpdfsdk/cpdfsdk_annothandlermgr.cpp:269:42
    #15 0x5566de07d486 in CPDFSDK_FormFillEnvironment::KillFocusAnnot(unsigned int) fpdfsdk/cpdfsdk_formfillenvironment.cpp:726:23
    #16 0x5566de07e489 in CPDFSDK_FormFillEnvironment::RemovePageView(IPDF_Page*) fpdfsdk/cpdfsdk_formfillenvironment.cpp:646:5
    #17 0x5566de0be813 in FORM_OnBeforeClosePage fpdfsdk/fpdf_formfill.cpp:645:19
    #18 0x5566de022722 in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:812:3
    #19 0x5566de01bab8 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:962:9
    #20 0x5566de0180ea in main samples/pdfium_test.cc:1181:5

Shadow bytes around the buggy address:
  0x0c047fffd0d0: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd
  0x0c047fffd0e0: fa fa fd fd fa fa fd fa fa fa fd fd fa fa fd fa
  0x0c047fffd0f0: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fa
  0x0c047fffd100: fa fa fd fd fa fa fd fa fa fa fd fa fa fa fd fa
  0x0c047fffd110: fa fa fd fd fa fa fd fa fa fa fd fa fa fa 00 fa
=>0x0c047fffd120: fa fa 04 fa fa fa fd fa fa fa fd fd fa fa 00[fa]
  0x0c047fffd130: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fffd140: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fffd150: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fffd160: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fffd170: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

Did this work before? N/A 

Chrome version: 78.0.3904.130  Channel: n/a
OS Version: 
Flash Version:

## Attachments

- [chromium-1047914.pdf](attachments/chromium-1047914.pdf) (application/pdf, 991 B)
- [chromium-1047914.evt](attachments/chromium-1047914.evt) (application/octet-stream, 71 B)

## Timeline

### pd...@gmail.com (2020-02-01)

WARNING: MemorySanitizer: use-of-uninitialized-value

    #0 0x558a2d53069b in fxcrt::RetainPtr<fxcrt::StringDataTemplate<wchar_t> >::RetainPtr(fxcrt::StringDataTemplate<wchar_t>*) core/fxcrt/retain_ptr.h:28:9
    #1 0x558a2d52c0fc in fxcrt::RetainPtr<fxcrt::StringDataTemplate<wchar_t> >::RetainPtr(fxcrt::RetainPtr<fxcrt::StringDataTemplate<wchar_t> > const&) core/fxcrt/retain_ptr.h:33:38
    #2 0x558a2d52c078 in fxcrt::WideString::WideString(fxcrt::WideString const&) core/fxcrt/widestring.cpp:327:51
    #3 0x558a3285e4e1 in CXFA_Node::SetSelectedItems(std::__1::vector<int, std::__1::allocator<int> > const&, bool, bool, bool) xfa/fxfa/parser/cxfa_node.cpp:4361:36
    #4 0x558a324b15df in CXFA_FFListBox::CommitData() xfa/fxfa/cxfa_fflistbox.cpp:90:12
    #5 0x558a324a51b3 in CXFA_FFField::ProcessCommittedData() xfa/fxfa/cxfa_fffield.cpp:649:10
    #6 0x558a324b08b7 in CXFA_FFListBox::OnKillFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_fflistbox.cpp:76:8
    #7 0x558a3248689b in CXFA_FFDocView::SetFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_ffdocview.cpp:306:26
    #8 0x558a329d44cf in CPDFXFA_WidgetHandler::OnKillFocus(fxcrt::ObservedPtr<CPDFSDK_Annot>*, unsigned int) fpdfsdk/fpdfxfa/cpdfxfa_widgethandler.cpp:575:31
    #9 0x558a2d38f704 in CPDFSDK_AnnotHandlerMgr::Annot_OnKillFocus(fxcrt::ObservedPtr<CPDFSDK_Annot>*, unsigned int) fpdfsdk/cpdfsdk_annothandlermgr.cpp:269:42
    #10 0x558a2d40ae5e in CPDFSDK_FormFillEnvironment::KillFocusAnnot(unsigned int) fpdfsdk/cpdfsdk_formfillenvironment.cpp:726:23
    #11 0x558a2d40cc90 in CPDFSDK_FormFillEnvironment::RemovePageView(IPDF_Page*) fpdfsdk/cpdfsdk_formfillenvironment.cpp:646:5
    #12 0x558a2d48cdf9 in FORM_OnBeforeClosePage fpdfsdk/fpdf_formfill.cpp:645:19
    #13 0x558a2d35b31f in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:812:3
    #14 0x558a2d34c7c0 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:962:9
    #15 0x558a2d345fad in main samples/pdfium_test.cc:1181:5

  Uninitialized value was stored to memory at
    #0 0x558a2d539d03 in std::__1::__compressed_pair_elem<fxcrt::StringDataTemplate<wchar_t>*, 0, false>::__compressed_pair_elem<fxcrt::StringDataTemplate<wchar_t>*&, void>(fxcrt::StringDataTemplate<wchar_t>*&) buildtools/third_party/libc++/trunk/include/memory:2187:9
    #1 0x558a2d539c1e in std::__1::__compressed_pair<fxcrt::StringDataTemplate<wchar_t>*, fxcrt::ReleaseDeleter<fxcrt::StringDataTemplate<wchar_t> > >::__compressed_pair<fxcrt::StringDataTemplate<wchar_t>*&, true>(fxcrt::StringDataTemplate<wchar_t>*&) buildtools/third_party/libc++/trunk/include/memory:2280:9
    #2 0x558a2d539ae3 in std::__1::unique_ptr<fxcrt::StringDataTemplate<wchar_t>, fxcrt::ReleaseDeleter<fxcrt::StringDataTemplate<wchar_t> > >::unique_ptr<true, void>(fxcrt::StringDataTemplate<wchar_t>*) buildtools/third_party/libc++/trunk/include/memory:2505:48
    #3 0x558a2d53060b in fxcrt::RetainPtr<fxcrt::StringDataTemplate<wchar_t> >::RetainPtr(fxcrt::StringDataTemplate<wchar_t>*) core/fxcrt/retain_ptr.h:27:33
    #4 0x558a2d52c0fc in fxcrt::RetainPtr<fxcrt::StringDataTemplate<wchar_t> >::RetainPtr(fxcrt::RetainPtr<fxcrt::StringDataTemplate<wchar_t> > const&) core/fxcrt/retain_ptr.h:33:38
    #5 0x558a2d52c078 in fxcrt::WideString::WideString(fxcrt::WideString const&) core/fxcrt/widestring.cpp:327:51
    #6 0x558a3285e4e1 in CXFA_Node::SetSelectedItems(std::__1::vector<int, std::__1::allocator<int> > const&, bool, bool, bool) xfa/fxfa/parser/cxfa_node.cpp:4361:36
    #7 0x558a324b15df in CXFA_FFListBox::CommitData() xfa/fxfa/cxfa_fflistbox.cpp:90:12
    #8 0x558a324a51b3 in CXFA_FFField::ProcessCommittedData() xfa/fxfa/cxfa_fffield.cpp:649:10
    #9 0x558a324b08b7 in CXFA_FFListBox::OnKillFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_fflistbox.cpp:76:8
    #10 0x558a3248689b in CXFA_FFDocView::SetFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_ffdocview.cpp:306:26
    #11 0x558a329d44cf in CPDFXFA_WidgetHandler::OnKillFocus(fxcrt::ObservedPtr<CPDFSDK_Annot>*, unsigned int) fpdfsdk/fpdfxfa/cpdfxfa_widgethandler.cpp:575:31
    #12 0x558a2d38f704 in CPDFSDK_AnnotHandlerMgr::Annot_OnKillFocus(fxcrt::ObservedPtr<CPDFSDK_Annot>*, unsigned int) fpdfsdk/cpdfsdk_annothandlermgr.cpp:269:42
    #13 0x558a2d40ae5e in CPDFSDK_FormFillEnvironment::KillFocusAnnot(unsigned int) fpdfsdk/cpdfsdk_formfillenvironment.cpp:726:23
    #14 0x558a2d40cc90 in CPDFSDK_FormFillEnvironment::RemovePageView(IPDF_Page*) fpdfsdk/cpdfsdk_formfillenvironment.cpp:646:5
    #15 0x558a2d48cdf9 in FORM_OnBeforeClosePage fpdfsdk/fpdf_formfill.cpp:645:19
    #16 0x558a2d35b31f in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:812:3
    #17 0x558a2d34c7c0 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:962:9
    #18 0x558a2d345fad in main samples/pdfium_test.cc:1181:5

  Uninitialized value was stored to memory at
    #0 0x558a2d539afa in std::__1::unique_ptr<fxcrt::StringDataTemplate<wchar_t>, fxcrt::ReleaseDeleter<fxcrt::StringDataTemplate<wchar_t> > >::unique_ptr<true, void>(fxcrt::StringDataTemplate<wchar_t>*) buildtools/third_party/libc++/trunk/include/memory
    #1 0x558a2d53060b in fxcrt::RetainPtr<fxcrt::StringDataTemplate<wchar_t> >::RetainPtr(fxcrt::StringDataTemplate<wchar_t>*) core/fxcrt/retain_ptr.h:27:33
    #2 0x558a2d52c0fc in fxcrt::RetainPtr<fxcrt::StringDataTemplate<wchar_t> >::RetainPtr(fxcrt::RetainPtr<fxcrt::StringDataTemplate<wchar_t> > const&) core/fxcrt/retain_ptr.h:33:38
    #3 0x558a2d52c078 in fxcrt::WideString::WideString(fxcrt::WideString const&) core/fxcrt/widestring.cpp:327:51
    #4 0x558a3285e4e1 in CXFA_Node::SetSelectedItems(std::__1::vector<int, std::__1::allocator<int> > const&, bool, bool, bool) xfa/fxfa/parser/cxfa_node.cpp:4361:36
    #5 0x558a324b15df in CXFA_FFListBox::CommitData() xfa/fxfa/cxfa_fflistbox.cpp:90:12
    #6 0x558a324a51b3 in CXFA_FFField::ProcessCommittedData() xfa/fxfa/cxfa_fffield.cpp:649:10
    #7 0x558a324b08b7 in CXFA_FFListBox::OnKillFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_fflistbox.cpp:76:8
    #8 0x558a3248689b in CXFA_FFDocView::SetFocus(CXFA_FFWidget*) xfa/fxfa/cxfa_ffdocview.cpp:306:26
    #9 0x558a329d44cf in CPDFXFA_WidgetHandler::OnKillFocus(fxcrt::ObservedPtr<CPDFSDK_Annot>*, unsigned int) fpdfsdk/fpdfxfa/cpdfxfa_widgethandler.cpp:575:31
    #10 0x558a2d38f704 in CPDFSDK_AnnotHandlerMgr::Annot_OnKillFocus(fxcrt::ObservedPtr<CPDFSDK_Annot>*, unsigned int) fpdfsdk/cpdfsdk_annothandlermgr.cpp:269:42
    #11 0x558a2d40ae5e in CPDFSDK_FormFillEnvironment::KillFocusAnnot(unsigned int) fpdfsdk/cpdfsdk_formfillenvironment.cpp:726:23
    #12 0x558a2d40cc90 in CPDFSDK_FormFillEnvironment::RemovePageView(IPDF_Page*) fpdfsdk/cpdfsdk_formfillenvironment.cpp:646:5
    #13 0x558a2d48cdf9 in FORM_OnBeforeClosePage fpdfsdk/fpdf_formfill.cpp:645:19
    #14 0x558a2d35b31f in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:812:3
    #15 0x558a2d34c7c0 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:962:9
    #16 0x558a2d345fad in main samples/pdfium_test.cc:1181:5

  Uninitialized value was created by a heap deallocation
    #0 0x558a2d344949 in operator delete(void*) /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/msan/msan_new_delete.cpp:74:44
    #1 0x558a2d3572a8 in std::__1::_DeallocateCaller::__do_call(void*) buildtools/third_party/libc++/trunk/include/new:334:12
    #2 0x558a2d357298 in std::__1::_DeallocateCaller::__do_deallocate_handle_size(void*, unsigned long) buildtools/third_party/libc++/trunk/include/new:292:12
    #3 0x558a2d357288 in std::__1::_DeallocateCaller::__do_deallocate_handle_size_align(void*, unsigned long, unsigned long) buildtools/third_party/libc++/trunk/include/new:262:12
    #4 0x558a2d357278 in std::__1::__libcpp_deallocate(void*, unsigned long, unsigned long) buildtools/third_party/libc++/trunk/include/new:340:3
    #5 0x558a2d5541d9 in std::__1::allocator<fxcrt::WideString>::deallocate(fxcrt::WideString*, unsigned long) buildtools/third_party/libc++/trunk/include/memory:1856:10
    #6 0x558a2d553f08 in std::__1::allocator_traits<std::__1::allocator<fxcrt::WideString> >::deallocate(std::__1::allocator<fxcrt::WideString>&, fxcrt::WideString*, unsigned long) buildtools/third_party/libc++/trunk/include/memory:1578:14
    #7 0x558a2d553b6a in std::__1::__vector_base<fxcrt::WideString, std::__1::allocator<fxcrt::WideString> >::~__vector_base() buildtools/third_party/libc++/trunk/include/vector:464:9
    #8 0x558a2d551bbd in std::__1::vector<fxcrt::WideString, std::__1::allocator<fxcrt::WideString> >::~vector() buildtools/third_party/libc++/trunk/include/vector:555:5
    #9 0x558a324afa8d in CXFA_FFListBox::LoadWidget() xfa/fxfa/cxfa_fflistbox.cpp:57:28
    #10 0x558a324d425f in CXFA_FFPageWidgetIterator::GetWidget(CXFA_LayoutItem*) xfa/fxfa/cxfa_ffpageview.cpp:219:19
    #11 0x558a324d4836 in CXFA_FFPageWidgetIterator::MoveToNext() xfa/fxfa/cxfa_ffpageview.cpp:182:34
    #12 0x558a2d4412a8 in CPDFSDK_PageView::LoadFXAnnots() fpdfsdk/cpdfsdk_pageview.cpp:490:55
    #13 0x558a2d4042e4 in CPDFSDK_FormFillEnvironment::GetPageView(IPDF_Page*, bool) fpdfsdk/cpdfsdk_formfillenvironment.cpp:581:14
    #14 0x558a2d48aed5 in (anonymous namespace)::FormHandleToPageView(fpdf_form_handle_t__*, fpdf_page_t__*) fpdfsdk/fpdf_formfill.cpp:171:39
    #15 0x558a2d48cb78 in FORM_OnAfterLoadPage fpdfsdk/fpdf_formfill.cpp:626:37
    #16 0x558a2d3599d9 in (anonymous namespace)::GetPageForIndex(_FPDF_FORMFILLINFO*, fpdf_document_t__*, int) samples/pdfium_test.cc:674:3
    #17 0x558a2d359d46 in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:693:20
    #18 0x558a2d34c7c0 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:962:9
    #19 0x558a2d345fad in main samples/pdfium_test.cc:1181:5


### pd...@gmail.com (2020-02-01)

Requires minor user interaction.

1. Click list field.
2. Click list field (again).

### pd...@gmail.com (2020-02-01)

Note: Chrome doesn't use XFA.

### mm...@chromium.org (2020-02-03)

Thanks for your report.

Tom, I didn't attempt to reproduce this crash myself.

### ts...@chromium.org (2020-02-03)

So it looks like we have a logic botch regarding to which level of the tree a child index is applied. The relevant portion of the document is

   <field anchorType="middleCenter"
      ...
      <items save="1"><integer></integer></items>
      <items><float></float><integer></integer></items>
    </field>

And the second one of the <items> is selected at present, so CXFA_FFListBox::CommitData() is going to call SetSelectedItems([1] ...).
However, in SetSelectedItems, we're going to retrieve an array sized to the children of the item whose save value is 1, namely just the one <integer> element.
Then indexing by one on an array of one element is out-of-bounds (only index 0 would be in bounds).

I have no idea what the right behaviour might be here.


### ts...@chromium.org (2020-02-03)

Ah, rather the two <items>...</items> lists need to be the same size.  One is for display, the other is for setting values (save="1"). 

### th...@chromium.org (2020-02-03)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-04)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/e06acb7de1b8c9e554c1b8dfa4974aca8ac46190

commit e06acb7de1b8c9e554c1b8dfa4974aca8ac46190
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Feb 04 18:23:26 2020

Ensure label item lists are not excessively sized in CXFA_FFListBox.

Truncate any spurious labels which do not correspond to underlying
settable values.

Bug: chromium:1047914
Change-Id: I0ba4cf09fb177f491f835d9f3046dea5df641fc4
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/65930
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>

[add] https://pdfium.googlesource.com/pdfium/+/e06acb7de1b8c9e554c1b8dfa4974aca8ac46190/testing/resources/javascript/xfa_specific/bug_1047914.in
[add] https://pdfium.googlesource.com/pdfium/+/e06acb7de1b8c9e554c1b8dfa4974aca8ac46190/testing/resources/javascript/xfa_specific/bug_1047914.evt
[modify] https://pdfium.googlesource.com/pdfium/+/e06acb7de1b8c9e554c1b8dfa4974aca8ac46190/xfa/fxfa/cxfa_fflistbox.cpp


### ts...@chromium.org (2020-02-04)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/218db6fbed8e5b74808835756b4538972830d282

commit 218db6fbed8e5b74808835756b4538972830d282
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Feb 04 20:19:35 2020

Roll src/third_party/pdfium dc397e0a03e0..e06acb7de1b8 (3 commits)

https://pdfium.googlesource.com/pdfium.git/+log/dc397e0a03e0..e06acb7de1b8

git log dc397e0a03e0..e06acb7de1b8 --date=short --first-parent --format='%ad %ae %s'
2020-02-04 tsepez@chromium.org Ensure label item lists are not excessively sized in CXFA_FFListBox.
2020-02-04 tsepez@chromium.org Remove stray comma from elements.inc table.
2020-02-03 tsepez@chromium.org Tidy cpdfsdk_widget.h

Created with:
  gclient setdep -r src/third_party/pdfium@e06acb7de1b8

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1047914
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I75df28f8d6862d161678e40400d410b825624052
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2037555
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#738309}

[modify] https://crrev.com/218db6fbed8e5b74808835756b4538972830d282/DEPS


### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-10)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-02-11)

Congrats! The Panel decided to award $1,000 for this report!

### na...@google.com (2020-02-11)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-05-13)

This issue was migrated from crbug.com/chromium/1047914?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051405)*
