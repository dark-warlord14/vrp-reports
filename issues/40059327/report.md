# Security: heap-use-after-free in PDFium CPDFSDK_AppStream::Write

| Field | Value |
|-------|-------|
| **Issue ID** | [40059327](https://issues.chromium.org/issues/40059327) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | mu...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2022-04-08 |
| **Bounty** | $5,000.00 |

## Description

# VULNERABILITY DETAILS

heap-use-after-free in PDFium

# VERSION

commit: 268f21c9d342b6bfd66621eb3940f9a1902898f9  

repo: <https://pdfium.googlesource.com/pdfium>

# REPRODUCTION CASE

gn args:

```
is_debug = false  
pdf_enable_xfa = true  
pdf_enable_v8 = true  
pdf_is_standalone = true  
is_component_build = false  
v8_static_library = true  
clang_use_chrome_plugins = false  
use_sysroot = false  
is_asan = true  
symbol_level=2  

```

pdfium\_test ./crash\_4\_6

```
Processing PDF file ./crash_4_6.  
Document has invalid cross reference table  
=================================================================  
==56422==ERROR: AddressSanitizer: heap-use-after-free on address 0x6060000221f0 at pc 0x5555569be235 bp 0x7fffffffdfc0 sp 0x7fffffffdfb8  
READ of size 8 at 0x6060000221f0 thread T0  
    #0 0x5555569be234 in std::__1::__tree<std::__1::__value_type<fxcrt::ByteString, fxcrt::RetainPtr<CPDF_Object> >, std::__1::__map_value_compare<fxcrt::ByteString, std::__1::__value_type<fxcrt::ByteString, fxcrt::RetainPtr<CPDF_Object> >, std::__1::less<fxcrt::ByteString>, true>, std::__1::allocator<std::__1::__value_type<fxcrt::ByteString, fxcrt::RetainPtr<CPDF_Object> > > >::__root() const buildtools/third_party/libc++/trunk/include/__tree:1079:59  
    #1 0x5555569be234 in std::__1::__tree_const_iterator<std::__1::__value_type<fxcrt::ByteString, fxcrt::RetainPtr<CPDF_Object> >, std::__1::__tree_node<std::__1::__value_type<fxcrt::ByteString, fxcrt::RetainPtr<CPDF_Object> >, void\*>\*, long> std::__1::__tree<std::__1::__value_type<fxcrt::ByteString, fxcrt::RetainPtr<CPDF_Object> >, std::__1::__map_value_compare<fxcrt::ByteString, std::__1::__value_type<fxcrt::ByteString, fxcrt::RetainPtr<CPDF_Object> >, std::__1::less<fxcrt::ByteString>, true>, std::__1::allocator<std::__1::__value_type<fxcrt::ByteString, fxcrt::RetainPtr<CPDF_Object> > > >::find<fxcrt::ByteString>(fxcrt::ByteString const&) const buildtools/third_party/libc++/trunk/include/__tree:2477:45  
    #2 0x5555569be234 in std::__1::map<fxcrt::ByteString, fxcrt::RetainPtr<CPDF_Object>, std::__1::less<fxcrt::ByteString>, std::__1::allocator<std::__1::pair<fxcrt::ByteString const, fxcrt::RetainPtr<CPDF_Object> > > >::find(fxcrt::ByteString const&) const buildtools/third_party/libc++/trunk/include/map:1393:68  
    #3 0x5555569be234 in CPDF_Dictionary::GetObjectFor(fxcrt::ByteString const&) const core/fpdfapi/parser/cpdf_dictionary.cpp:87:19  
    #4 0x5555569be234 in CPDF_Dictionary::GetDirectObjectFor(fxcrt::ByteString const&) const core/fpdfapi/parser/cpdf_dictionary.cpp:98:26  
    #5 0x5555569be234 in CPDF_Dictionary::GetDictFor(fxcrt::ByteString const&) const core/fpdfapi/parser/cpdf_dictionary.cpp:153:26  
    #6 0x55555666c19d in CPDFSDK_AppStream::Write(fxcrt::ByteString const&, fxcrt::ByteString const&, fxcrt::ByteString const&) fpdfsdk/cpdfsdk_appstream.cpp:1880:54  
    #7 0x555556675f7b in CPDFSDK_AppStream::SetAsComboBox(absl::optional<fxcrt::WideString>) fpdfsdk/cpdfsdk_appstream.cpp:1589:3  
    #8 0x5555566b6857 in CPDFSDK_Widget::ResetAppearance(absl::optional<fxcrt::WideString>, CPDFSDK_Widget::ValueChanged) fpdfsdk/cpdfsdk_widget.cpp:650:17  
    #9 0x5555566b984f in CPDFSDK_Widget::OnLoad() fpdfsdk/cpdfsdk_widget.cpp:881:7  
    #10 0x5555566b016d in CPDFSDK_PageView::LoadFXAnnots() fpdfsdk/cpdfsdk_pageview.cpp:604:29  
    #11 0x555556695889 in CPDFSDK_FormFillEnvironment::GetOrCreatePageView(IPDF_Page\*) fpdfsdk/cpdfsdk_formfillenvironment.cpp:642:14  
    #12 0x5555566c8f12 in (anonymous namespace)::FormHandleToPageView(fpdf_form_handle_t__\*, fpdf_page_t__\*) fpdfsdk/fpdf_formfill.cpp:172:39  
    #13 0x5555566c8f12 in FORM_OnAfterLoadPage fpdfsdk/fpdf_formfill.cpp:737:37  
    #14 0x555556642b6f in (anonymous namespace)::GetPageForIndex(_FPDF_FORMFILLINFO\*, fpdf_document_t__\*, int) samples/pdfium_test.cc:809:3  
    #15 0x55555663bd6f in (anonymous namespace)::ProcessPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__\*, fpdf_form_handle_t__\*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest\*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::function<void ()> const&) samples/pdfium_test.cc:829:20  
    #16 0x55555663bd6f in (anonymous namespace)::ProcessPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const\*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::function<void ()> const&) samples/pdfium_test.cc:1120:9  
    #17 0x55555663bd6f in main samples/pdfium_test.cc:1373:5  
    #18 0x7ffff7c4b0b2 in __libc_start_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16  
  
0x6060000221f0 is located 48 bytes inside of 64-byte region [0x6060000221c0,0x606000022200)  
freed by thread T0 here:  
    #0 0x555556633dfd in operator delete(void\*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3  
    #1 0x555556a08123 in fxcrt::Retainable::Release() const core/fxcrt/retain_ptr.h:134:7  
    #2 0x555556a08123 in fxcrt::ReleaseDeleter<CPDF_Dictionary>::operator()(CPDF_Dictionary\*) const core/fxcrt/retain_ptr.h:22:47  
    #3 0x555556a08123 in std::__1::unique_ptr<CPDF_Dictionary, fxcrt::ReleaseDeleter<CPDF_Dictionary> >::reset(CPDF_Dictionary\*) buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7  
    #4 0x555556a08123 in std::__1::unique_ptr<CPDF_Dictionary, fxcrt::ReleaseDeleter<CPDF_Dictionary> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:269:19  
    #5 0x555556a08123 in fxcrt::RetainPtr<CPDF_Dictionary>::~RetainPtr() core/fxcrt/retain_ptr.h:27:7  
    #6 0x555556a08123 in CPDF_Stream::~CPDF_Stream() core/fpdfapi/parser/cpdf_stream.cpp:55:1  
    #7 0x555556a081ed in CPDF_Stream::~CPDF_Stream() core/fpdfapi/parser/cpdf_stream.cpp:51:29  
    #8 0x5555569bf247 in fxcrt::Retainable::Release() const core/fxcrt/retain_ptr.h:134:7  
    #9 0x5555569bf247 in fxcrt::ReleaseDeleter<CPDF_Object>::operator()(CPDF_Object\*) const core/fxcrt/retain_ptr.h:22:47  
    #10 0x5555569bf247 in std::__1::unique_ptr<CPDF_Object, fxcrt::ReleaseDeleter<CPDF_Object> >::reset(CPDF_Object\*) buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7  
    #11 0x5555569bf247 in fxcrt::RetainPtr<CPDF_Object>::operator=(fxcrt::RetainPtr<CPDF_Object>&&) core/fxcrt/retain_ptr.h:75:12  
    #12 0x5555569bf247 in CPDF_Dictionary::SetFor(fxcrt::ByteString const&, fxcrt::RetainPtr<CPDF_Object>) core/fpdfapi/parser/cpdf_dictionary.cpp:221:27  
    #13 0x555556680a0c in std::__1::enable_if<!(CanInternStrings<CPDF_Reference>::value), CPDF_Reference\*>::type CPDF_Dictionary::SetNewFor<CPDF_Reference, CPDF_Document\*&, unsigned int>(fxcrt::ByteString const&, CPDF_Document\*&, unsigned int&&) core/fpdfapi/parser/cpdf_dictionary.h:91:9  
    #14 0x55555666bcd1 in CPDFSDK_AppStream::Write(fxcrt::ByteString const&, fxcrt::ByteString const&, fxcrt::ByteString const&) fpdfsdk/cpdfsdk_appstream.cpp:1867:18  
    #15 0x555556675f7b in CPDFSDK_AppStream::SetAsComboBox(absl::optional<fxcrt::WideString>) fpdfsdk/cpdfsdk_appstream.cpp:1589:3  
    #16 0x5555566b6857 in CPDFSDK_Widget::ResetAppearance(absl::optional<fxcrt::WideString>, CPDFSDK_Widget::ValueChanged) fpdfsdk/cpdfsdk_widget.cpp:650:17  
    #17 0x5555566b984f in CPDFSDK_Widget::OnLoad() fpdfsdk/cpdfsdk_widget.cpp:881:7  
    #18 0x5555566b016d in CPDFSDK_PageView::LoadFXAnnots() fpdfsdk/cpdfsdk_pageview.cpp:604:29  
    #19 0x555556695889 in CPDFSDK_FormFillEnvironment::GetOrCreatePageView(IPDF_Page\*) fpdfsdk/cpdfsdk_formfillenvironment.cpp:642:14  
    #20 0x5555566c8f12 in (anonymous namespace)::FormHandleToPageView(fpdf_form_handle_t__\*, fpdf_page_t__\*) fpdfsdk/fpdf_formfill.cpp:172:39  
    #21 0x5555566c8f12 in FORM_OnAfterLoadPage fpdfsdk/fpdf_formfill.cpp:737:37  
    #22 0x555556642b6f in (anonymous namespace)::GetPageForIndex(_FPDF_FORMFILLINFO\*, fpdf_document_t__\*, int) samples/pdfium_test.cc:809:3  
    #23 0x55555663bd6f in (anonymous namespace)::ProcessPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__\*, fpdf_form_handle_t__\*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest\*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::function<void ()> const&) samples/pdfium_test.cc:829:20  
    #24 0x55555663bd6f in (anonymous namespace)::ProcessPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const\*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::function<void ()> const&) samples/pdfium_test.cc:1120:9  
    #25 0x55555663bd6f in main samples/pdfium_test.cc:1373:5  
    #26 0x7ffff7c4b0b2 in __libc_start_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16  
  
previously allocated by thread T0 here:  
    #0 0x55555663359d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3  
    #1 0x555556a14109 in fxcrt::RetainPtr<CPDF_Dictionary> pdfium::MakeRetain<CPDF_Dictionary, fxcrt::WeakPtr<fxcrt::StringPoolTemplate<fxcrt::ByteString>, std::__1::default_delete<fxcrt::StringPoolTemplate<fxcrt::ByteString> > >&>(fxcrt::WeakPtr<fxcrt::StringPoolTemplate<fxcrt::ByteString>, std::__1::default_delete<fxcrt::StringPoolTemplate<fxcrt::ByteString> > >&) core/fxcrt/retain_ptr.h:164:23  
    #2 0x555556a12ac9 in CPDF_SyntaxParser::GetObjectBodyInternal(CPDF_IndirectObjectHolder\*, CPDF_SyntaxParser::ParseType) core/fpdfapi/parser/cpdf_syntax_parser.cpp:558:9  
    #3 0x555556a12dd2 in CPDF_SyntaxParser::GetObjectBodyInternal(CPDF_IndirectObjectHolder\*, CPDF_SyntaxParser::ParseType) core/fpdfapi/parser/cpdf_syntax_parser.cpp:581:11  
    #4 0x555556a12dd2 in CPDF_SyntaxParser::GetObjectBodyInternal(CPDF_IndirectObjectHolder\*, CPDF_SyntaxParser::ParseType) core/fpdfapi/parser/cpdf_syntax_parser.cpp:581:11  
    #5 0x555556a165f3 in CPDF_SyntaxParser::GetIndirectObject(CPDF_IndirectObjectHolder\*, CPDF_SyntaxParser::ParseType) core/fpdfapi/parser/cpdf_syntax_parser.cpp:635:33  
    #6 0x5555569ee587 in CPDF_Parser::ParseIndirectObjectAt(long, unsigned int) core/fpdfapi/parser/cpdf_parser.cpp:975:28  
    #7 0x5555569efeec in CPDF_Parser::ParseIndirectObject(unsigned int) core/fpdfapi/parser/cpdf_parser.cpp:923:12  
    #8 0x5555569c191c in CPDF_Document::ParseIndirectObject(unsigned int) core/fpdfapi/parser/cpdf_document.cpp:132:33  
    #9 0x5555569ceb12 in CPDF_IndirectObjectHolder::GetOrParseIndirectObject(unsigned int) core/fpdfapi/parser/cpdf_indirect_object_holder.cpp:49:36  
    #10 0x5555569976a2 in CPDF_Array::GetDirectObjectAt(unsigned long) core/fpdfapi/parser/cpdf_array.cpp:117:23  
    #11 0x5555569976a2 in CPDF_Array::GetDictAt(unsigned long) core/fpdfapi/parser/cpdf_array.cpp:157:20  
    #12 0x5555569c4fda in (anonymous namespace)::CountPages(CPDF_Dictionary\*, std::__1::set<CPDF_Dictionary\*, std::__1::less<CPDF_Dictionary\*>, std::__1::allocator<CPDF_Dictionary\*> >\*) core/fpdfapi/parser/cpdf_document.cpp:40:39  
    #13 0x5555569c2824 in CPDF_Document::RetrievePageCount() core/fpdfapi/parser/cpdf_document.cpp:369:10  
    #14 0x5555569c1d6c in CPDF_Document::LoadPages() core/fpdfapi/parser/cpdf_document.cpp:168:23  
    #15 0x5555569c1ac9 in CPDF_Document::TryInit() core/fpdfapi/parser/cpdf_document.cpp:142:3  
    #16 0x5555569e390f in CPDF_Parser::StartParseInternal() core/fpdfapi/parser/cpdf_parser.cpp:246:40  
    #17 0x5555569e363d in CPDF_Parser::StartParse(fxcrt::RetainPtr<IFX_SeekableReadStream> const&, fxcrt::ByteString const&) core/fpdfapi/parser/cpdf_parser.cpp:217:10  
    #18 0x5555569c2321 in CPDF_Document::LoadDoc(fxcrt::RetainPtr<IFX_SeekableReadStream> const&, fxcrt::ByteString const&) core/fpdfapi/parser/cpdf_document.cpp:152:38  
    #19 0x5555566cfade in (anonymous namespace)::LoadDocumentImpl(fxcrt::RetainPtr<IFX_SeekableReadStream> const&, char const\*) fpdfsdk/fpdf_view.cpp:163:41  
    #20 0x5555566d0466 in FPDF_LoadCustomDocument fpdfsdk/fpdf_view.cpp:297:10  
    #21 0x55555663b546 in (anonymous namespace)::ProcessPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const\*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::function<void ()> const&) samples/pdfium_test.cc:1025:17  
    #22 0x55555663b546 in main samples/pdfium_test.cc:1373:5  
    #23 0x7ffff7c4b0b2 in __libc_start_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16  
  
SUMMARY: AddressSanitizer: heap-use-after-free buildtools/third_party/libc++/trunk/include/__tree:1079:59 in std::__1::__tree<std::__1::__value_type<fxcrt::ByteString, fxcrt::RetainPtr<CPDF_Object> >, std::__1::__map_value_compare<fxcrt::ByteString, std::__1::__value_type<fxcrt::ByteString, fxcrt::RetainPtr<CPDF_Object> >, std::__1::less<fxcrt::ByteString>, true>, std::__1::allocator<std::__1::__value_type<fxcrt::ByteString, fxcrt::RetainPtr<CPDF_Object> > > >::__root() const  
Shadow bytes around the buggy address:  
  0x0c0c7fffc3e0: fa fa fa fa 00 00 00 00 00 00 00 00 fa fa fa fa  
  0x0c0c7fffc3f0: 00 00 00 00 00 00 00 00 fa fa fa fa 00 00 00 00  
  0x0c0c7fffc400: 00 00 00 00 fa fa fa fa 00 00 00 00 00 00 00 00  
  0x0c0c7fffc410: fa fa fa fa 00 00 00 00 00 00 00 00 fa fa fa fa  
  0x0c0c7fffc420: 00 00 00 00 00 00 00 00 fa fa fa fa 00 00 00 00  
=>0x0c0c7fffc430: 00 00 00 00 fa fa fa fa fd fd fd fd fd fd[fd]fd  
  0x0c0c7fffc440: fa fa fa fa fd fd fd fd fd fd fd fd fa fa fa fa  
  0x0c0c7fffc450: 00 00 00 00 00 fc fc fc fa fa fa fa 00 00 00 00  
  0x0c0c7fffc460: 00 00 00 fa fa fa fa fa 00 00 00 00 00 00 00 fa  
  0x0c0c7fffc470: fa fa fa fa fd fd fd fd fd fd fd fd fa fa fa fa  
  0x0c0c7fffc480: 00 00 00 00 00 00 00 fa fa fa fa fa fd fd fd fd  
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
==56422==ABORTING  

```

**CREDIT INFORMATION**  

Xu Hanyu

## Attachments

- [crash_4_6](attachments/crash_4_6) (text/plain, 232 B)

## Timeline

### [Deleted User] (2022-04-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-04-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6732178096193536.

### ts...@chromium.org (2022-04-08)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### rs...@chromium.org (2022-04-08)

Thanks for the report. Clusterfuzz is able to reproduce this and is working on the regression and impact range.

### rs...@chromium.org (2022-04-08)

Collision detected!

### th...@chromium.org (2022-04-08)

I think this may have regressed recently. Bisecting...

### th...@chromium.org (2022-04-08)

And it's because I fixed a bug, which caused a regression, which required another fix, which caused this regression in https://pdfium-review.googlesource.com/c/pdfium/+/91670

### th...@chromium.org (2022-04-08)

https://pdfium-review.googlesource.com/92430

### th...@chromium.org (2022-04-08)

Since https://crbug.com/chromium/1308739  targets M101, this bug has not reached stable channel yet.

### ts...@chromium.org (2022-04-08)

Setting some labels, hopefully CF will set found-in, but I am pretty sure this goes back to the beginning of time.

### ts...@chromium.org (2022-04-08)

Shows what I know, looks to be a recent regression.

### ts...@chromium.org (2022-04-08)

CL at https://pdfium-review.googlesource.com/c/pdfium/+/92432?forceReload=true

### th...@chromium.org (2022-04-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-04-08)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/45333887dc93ce27ae3c54a2c541ae1c8c987824

commit 45333887dc93ce27ae3c54a2c541ae1c8c987824
Author: Tom Sepez <tsepez@chromium.org>
Date: Fri Apr 08 22:06:11 2022

Retain original dictionary in CPDFSDK_AppStream::Write().

Bug: chromium:1314658
Change-Id: Iad1db4fc2285492e31b8bb535a0b078b07fb73ef
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/92432
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/45333887dc93ce27ae3c54a2c541ae1c8c987824/fpdfsdk/cpdfsdk_appstream.cpp
[add] https://pdfium.googlesource.com/pdfium/+/45333887dc93ce27ae3c54a2c541ae1c8c987824/testing/resources/javascript/bug_1314658.in
[add] https://pdfium.googlesource.com/pdfium/+/45333887dc93ce27ae3c54a2c541ae1c8c987824/testing/resources/javascript/bug_1314658_expected.txt


### gi...@appspot.gserviceaccount.com (2022-04-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/379115ab511037ec38413071cac38d344182df23

commit 379115ab511037ec38413071cac38d344182df23
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Apr 08 23:21:32 2022

Roll PDFium from 268f21c9d342 to 946bf0f664a7 (9 revisions)

https://pdfium.googlesource.com/pdfium.git/+log/268f21c9d342..946bf0f664a7

2022-04-08 tsepez@chromium.org Remove CPDFSDK_ActionHandler.
2022-04-08 tsepez@chromium.org Retain original dictionary in CPDFSDK_AppStream::Write().
2022-04-08 thestig@chromium.org Remove ToBAAnnot() and reduce ToXFAWidget() usage.
2022-04-08 thestig@chromium.org Remove CPDFSDK_AnnotHandlerMgr and IPDFSDK_AnnotHandler.
2022-04-08 thestig@chromium.org Remove most remaining virtual methods from IPDFSDK_AnnotHandler.
2022-04-08 thestig@chromium.org Remove keyboard event, focus and drawing code from IPDFSDK_AnnotHandler.
2022-04-08 thestig@chromium.org Remove KeyUp event handling code.
2022-04-08 thestig@chromium.org Remove mouse event code from IPDFSDK_AnnotHandler.
2022-04-08 kmoon@chromium.org [xfa] Fix image data positions in the GIF decoder

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To file a bug in PDFium: https://bugs.chromium.org/p/pdfium/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1314658
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I26283fe17150ccc3474fe5e0f46b43f4fba86587
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3580027
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#990646}

[modify] https://crrev.com/379115ab511037ec38413071cac38d344182df23/DEPS


### cl...@chromium.org (2022-04-09)

Detailed Report: https://clusterfuzz.com/testcase?key=6732178096193536

Fuzzer: None
Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60c0001109f0
Crash State:
  CPDFSDK_AppStream::Write
  CPDFSDK_AppStream::SetAsComboBox
  CPDFSDK_Widget::ResetAppearance
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_pdfium&range=983471:983477

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6732178096193536

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### [Deleted User] (2022-04-09)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-09)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2022-04-09)

ClusterFuzz testcase 6732178096193536 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_pdfium&range=990641:990658

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### th...@chromium.org (2022-04-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-11)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2022-04-11)

thestig@ hello. According to https://crbug.com/chromium/1314658#c16 this was introduced in 98347x, which is after M102 branch point. In https://crbug.com/chromium/1314658#c19 you ask for M101 merge - do you know something that ClusterFuzz doesn't know?

### [Deleted User] (2022-04-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-11)

[Empty comment from Monorail migration]

### th...@chromium.org (2022-04-11)

The CL that caused this issue is a fix for another regression, and that got merged to M101: https://pdfium.googlesource.com/pdfium/+/42c9b9b87a372cda22d4db328282d970b97c5294

### th...@chromium.org (2022-04-12)

+adetaylor@ ^

### ad...@google.com (2022-04-12)

Ah right. Thanks very much. That's useful information for amyressler@ as she considers the merge requests.

### am...@chromium.org (2022-04-12)

Thanks for the context above all and to thestig@ for manual intervention with merge labels here
m101 merge approved, please merge to branch 4951 ASAP so this fix can be included in next beta release tomorrow 

### th...@chromium.org (2022-04-12)

Merge in progress: https://pdfium-review.googlesource.com/92550

### gi...@appspot.gserviceaccount.com (2022-04-12)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/f4c62094abe20ade3a29328bc370238b7e7812b2

commit f4c62094abe20ade3a29328bc370238b7e7812b2
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Apr 12 18:56:02 2022

M101: Retain original dictionary in CPDFSDK_AppStream::Write().

Bug: chromium:1314658
Change-Id: Iad1db4fc2285492e31b8bb535a0b078b07fb73ef
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/92432
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>
(cherry picked from commit 45333887dc93ce27ae3c54a2c541ae1c8c987824)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/92550
Reviewed-by: Nigi <nigi@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/f4c62094abe20ade3a29328bc370238b7e7812b2/fpdfsdk/cpdfsdk_appstream.cpp
[add] https://pdfium.googlesource.com/pdfium/+/f4c62094abe20ade3a29328bc370238b7e7812b2/testing/resources/javascript/bug_1314658.in
[add] https://pdfium.googlesource.com/pdfium/+/f4c62094abe20ade3a29328bc370238b7e7812b2/testing/resources/javascript/bug_1314658_expected.txt


### am...@google.com (2022-04-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-13)

Congratulations! The VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-04-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-27)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-05-30)

[Empty comment from Monorail migration]

### rz...@google.com (2022-05-30)

Fixed code doesn't exist in M96 branch

### rz...@google.com (2022-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-31)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gm...@google.com (2022-07-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1314658?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059327)*
