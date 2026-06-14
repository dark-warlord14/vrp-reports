# Security: heap-use-after-free in PDFium

| Field | Value |
|-------|-------|
| **Issue ID** | [40088558](https://issues.chromium.org/issues/40088558) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Reporter** | yu...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2017-08-01 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36

Steps to reproduce the problem:
VULNERABILITY DETAILS
==95290:95290==ERROR: AddressSanitizer: heap-use-after-free on address 0x60300000cdf0 at pc 0x0000032b4d87 bp 0x7ffcb826d870 sp 0x7ffcb826d868
READ of size 8 at 0x60300000cdf0 thread T0
    #0 0x32b4d86 in CPDF_DataAvail::AreObjectsAvailable(std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&, bool, CPDF_DataAvail::DownloadHints*, std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&) third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:179:26
    #1 0x32b4bb9 in CPDF_DataAvail::AreObjectsAvailable(std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&, bool, CPDF_DataAvail::DownloadHints*, std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&) third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:235:10
    #2 0x32b4bb9 in CPDF_DataAvail::AreObjectsAvailable(std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&, bool, CPDF_DataAvail::DownloadHints*, std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&) third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:235:10
    #3 0x32b4bb9 in CPDF_DataAvail::AreObjectsAvailable(std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&, bool, CPDF_DataAvail::DownloadHints*, std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&) third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:235:10
    #4 0x32b4bb9 in CPDF_DataAvail::AreObjectsAvailable(std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&, bool, CPDF_DataAvail::DownloadHints*, std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&) third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:235:10
    #5 0x32b4bb9 in CPDF_DataAvail::AreObjectsAvailable(std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&, bool, CPDF_DataAvail::DownloadHints*, std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&) third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:235:10
    #6 0x32b4bb9 in CPDF_DataAvail::AreObjectsAvailable(std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&, bool, CPDF_DataAvail::DownloadHints*, std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&) third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:235:10
    #7 0x32b4bb9 in CPDF_DataAvail::AreObjectsAvailable(std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&, bool, CPDF_DataAvail::DownloadHints*, std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&) third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:235:10
    #8 0x32c611d in CPDF_DataAvail::ValidatePage(unsigned int) third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:1683:10
    #9 0x32c6c83 in CheckLinearizedFirstPage third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:1450:8
    #10 0x32c6c83 in CPDF_DataAvail::IsPageAvail(unsigned int, CPDF_DataAvail::DownloadHints*) third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:1475
    #11 0x21bd777 in FPDFAvail_IsPageAvail third_party/pdfium/fpdfsdk/fpdf_dataavail.cpp:177:60
    #12 0x4fb9bd in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) third_party/pdfium/samples/pdfium_test.cc:1359:16
    #13 0x4f7c00 in main third_party/pdfium/samples/pdfium_test.cc:1526:5
    #14 0x7f7cde00382f in __libc_start_main /build/glibc-bfm8X4/glibc-2.23/csu/../csu/libc-start.c:291

0x60300000cdf0 is located 0 bytes inside of 24-byte region [0x60300000cdf0,0x60300000ce08)
freed by thread T0 here:
    #0 0x4f21a2 in operator delete(void*) (/home/chrome/chromium/src/out/pdf/pdfium_test+0x4f21a2)
    #1 0x32ac44f in operator() buildtools/third_party/libc++/trunk/include/memory:2272:5
    #2 0x32ac44f in reset buildtools/third_party/libc++/trunk/include/memory:2585
    #3 0x32ac44f in ~unique_ptr buildtools/third_party/libc++/trunk/include/memory:2539
    #4 0x32ac44f in destroy buildtools/third_party/libc++/trunk/include/memory:1853
    #5 0x32ac44f in __destroy<std::__1::unique_ptr<CPDF_Object, std::__1::default_delete<CPDF_Object> > > buildtools/third_party/libc++/trunk/include/memory:1721
    #6 0x32ac44f in destroy<std::__1::unique_ptr<CPDF_Object, std::__1::default_delete<CPDF_Object> > > buildtools/third_party/libc++/trunk/include/memory:1589
    #7 0x32ac44f in __destruct_at_end buildtools/third_party/libc++/trunk/include/vector:418
    #8 0x32ac44f in __destruct_at_end buildtools/third_party/libc++/trunk/include/vector:804
    #9 0x32ac44f in resize buildtools/third_party/libc++/trunk/include/vector:2004
    #10 0x32ac44f in CPDF_Array::Truncate(unsigned long) third_party/pdfium/core/fpdfapi/parser/cpdf_array.cpp:158
    #11 0x3330e69 in PDF_DataDecode(unsigned char const*, unsigned int, CPDF_Dictionary const*, unsigned int, bool, unsigned char**, unsigned int*, CFX_ByteString*, CPDF_Dictionary**) third_party/pdfium/core/fpdfapi/parser/fpdf_parser_decode.cpp:401:20
    #12 0x331e622 in CPDF_StreamAcc::LoadAllData(bool, unsigned int, bool) third_party/pdfium/core/fpdfapi/parser/cpdf_stream_acc.cpp:45:15
    #13 0x330ca35 in CPDF_Parser::GetObjectStream(unsigned int) third_party/pdfium/core/fpdfapi/parser/cpdf_parser.cpp:1198:15
    #14 0x330b099 in CPDF_Parser::ParseIndirectObject(CPDF_IndirectObjectHolder*, unsigned int) third_party/pdfium/core/fpdfapi/parser/cpdf_parser.cpp:1156:7
    #15 0x32d3e19 in CPDF_Document::ParseIndirectObject(unsigned int) third_party/pdfium/core/fpdfapi/parser/cpdf_document.cpp:363:33
    #16 0x32e7a00 in CPDF_IndirectObjectHolder::GetOrParseIndirectObject(unsigned int) third_party/pdfium/core/fpdfapi/parser/cpdf_indirect_object_holder.cpp:39:42
    #17 0x32b44db in CPDF_DataAvail::AreObjectsAvailable(std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&, bool, CPDF_DataAvail::DownloadHints*, std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&) third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:215:28
    #18 0x32b4bb9 in CPDF_DataAvail::AreObjectsAvailable(std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&, bool, CPDF_DataAvail::DownloadHints*, std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&) third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:235:10
    #19 0x32b4bb9 in CPDF_DataAvail::AreObjectsAvailable(std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&, bool, CPDF_DataAvail::DownloadHints*, std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&) third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:235:10
    #20 0x32b4bb9 in CPDF_DataAvail::AreObjectsAvailable(std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&, bool, CPDF_DataAvail::DownloadHints*, std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&) third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:235:10
    #21 0x32b4bb9 in CPDF_DataAvail::AreObjectsAvailable(std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&, bool, CPDF_DataAvail::DownloadHints*, std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&) third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:235:10
    #22 0x32b4bb9 in CPDF_DataAvail::AreObjectsAvailable(std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&, bool, CPDF_DataAvail::DownloadHints*, std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&) third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:235:10
    #23 0x32b4bb9 in CPDF_DataAvail::AreObjectsAvailable(std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&, bool, CPDF_DataAvail::DownloadHints*, std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&) third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:235:10
    #24 0x32b4bb9 in CPDF_DataAvail::AreObjectsAvailable(std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&, bool, CPDF_DataAvail::DownloadHints*, std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&) third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:235:10
    #25 0x32c611d in CPDF_DataAvail::ValidatePage(unsigned int) third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:1683:10
    #26 0x32c6c83 in CheckLinearizedFirstPage third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:1450:8
    #27 0x32c6c83 in CPDF_DataAvail::IsPageAvail(unsigned int, CPDF_DataAvail::DownloadHints*) third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:1475
    #28 0x21bd777 in FPDFAvail_IsPageAvail third_party/pdfium/fpdfsdk/fpdf_dataavail.cpp:177:60
    #29 0x4fb9bd in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) third_party/pdfium/samples/pdfium_test.cc:1359:16
    #30 0x4f7c00 in main third_party/pdfium/samples/pdfium_test.cc:1526:5
    #31 0x7f7cde00382f in __libc_start_main /build/glibc-bfm8X4/glibc-2.23/csu/../csu/libc-start.c:291

previously allocated by thread T0 here:
    #0 0x4f1582 in operator new(unsigned long) (/home/chrome/chromium/src/out/pdf/pdfium_test+0x4f1582)
    #1 0x3327fd2 in pdfium::internal::MakeUniqueResult<CPDF_Name>::Scalar pdfium::MakeUnique<CPDF_Name, CFX_WeakPtr<CFX_StringPoolTemplate<CFX_ByteString>, std::__1::default_delete<CFX_StringPoolTemplate<CFX_ByteString> > >&, CFX_ByteString>(CFX_WeakPtr<CFX_StringPoolTemplate<CFX_ByteString>, std::__1::default_delete<CFX_StringPoolTemplate<CFX_ByteString> > >&, CFX_ByteString&&) third_party/pdfium/third_party/base/ptr_util.h:56:29
    #2 0x3326add in CPDF_SyntaxParser::GetObject(CPDF_IndirectObjectHolder*, unsigned int, unsigned int, bool) third_party/pdfium/core/fpdfapi/parser/cpdf_syntax_parser.cpp:427:12
    #3 0x3326909 in CPDF_SyntaxParser::GetObject(CPDF_IndirectObjectHolder*, unsigned int, unsigned int, bool) third_party/pdfium/core/fpdfapi/parser/cpdf_syntax_parser.cpp:421:16
    #4 0x332700f in CPDF_SyntaxParser::GetObject(CPDF_IndirectObjectHolder*, unsigned int, unsigned int, bool) third_party/pdfium/core/fpdfapi/parser/cpdf_syntax_parser.cpp:461:11
    #5 0x3309243 in CPDF_Parser::ParseIndirectObjectAt(CPDF_IndirectObjectHolder*, long, unsigned int) third_party/pdfium/core/fpdfapi/parser/cpdf_parser.cpp:1376:18
    #6 0x330ae13 in CPDF_Parser::ParseIndirectObject(CPDF_IndirectObjectHolder*, unsigned int) third_party/pdfium/core/fpdfapi/parser/cpdf_parser.cpp:1150:12
    #7 0x32d3e19 in CPDF_Document::ParseIndirectObject(unsigned int) third_party/pdfium/core/fpdfapi/parser/cpdf_document.cpp:363:33
    #8 0x32e7a00 in CPDF_IndirectObjectHolder::GetOrParseIndirectObject(unsigned int) third_party/pdfium/core/fpdfapi/parser/cpdf_indirect_object_holder.cpp:39:42
    #9 0x32b44db in CPDF_DataAvail::AreObjectsAvailable(std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&, bool, CPDF_DataAvail::DownloadHints*, std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&) third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:215:28
    #10 0x32b4bb9 in CPDF_DataAvail::AreObjectsAvailable(std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&, bool, CPDF_DataAvail::DownloadHints*, std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&) third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:235:10
    #11 0x32b4bb9 in CPDF_DataAvail::AreObjectsAvailable(std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&, bool, CPDF_DataAvail::DownloadHints*, std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&) third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:235:10
    #12 0x32b4bb9 in CPDF_DataAvail::AreObjectsAvailable(std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&, bool, CPDF_DataAvail::DownloadHints*, std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&) third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:235:10
    #13 0x32b4bb9 in CPDF_DataAvail::AreObjectsAvailable(std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&, bool, CPDF_DataAvail::DownloadHints*, std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&) third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:235:10
    #14 0x32c611d in CPDF_DataAvail::ValidatePage(unsigned int) third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:1683:10
    #15 0x32c6c83 in CheckLinearizedFirstPage third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:1450:8
    #16 0x32c6c83 in CPDF_DataAvail::IsPageAvail(unsigned int, CPDF_DataAvail::DownloadHints*) third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:1475
    #17 0x21bd777 in FPDFAvail_IsPageAvail third_party/pdfium/fpdfsdk/fpdf_dataavail.cpp:177:60
    #18 0x4fb9bd in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) third_party/pdfium/samples/pdfium_test.cc:1359:16
    #19 0x4f7c00 in main third_party/pdfium/samples/pdfium_test.cc:1526:5
    #20 0x7f7cde00382f in __libc_start_main /build/glibc-bfm8X4/glibc-2.23/csu/../csu/libc-start.c:291

SUMMARY: AddressSanitizer: heap-use-after-free third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp:179:26 in CPDF_DataAvail::AreObjectsAvailable(std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&, bool, CPDF_DataAvail::DownloadHints*, std::__1::vector<CPDF_Object*, std::__1::allocator<CPDF_Object*> >&)
Shadow bytes around the buggy address:
  0x0c067fff9960: fd fd fa fa fd fd fd fa fa fa fd fd fd fa fa fa
  0x0c067fff9970: fd fd fd fa fa fa fd fd fd fa fa fa fd fd fd fa
  0x0c067fff9980: fa fa 00 00 00 00 fa fa fd fd fd fa fa fa 00 00
  0x0c067fff9990: 00 00 fa fa fd fd fd fa fa fa fd fd fd fa fa fa
  0x0c067fff99a0: fd fd fd fd fa fa 00 00 00 00 fa fa 00 00 00 fa
=>0x0c067fff99b0: fa fa fd fd fd fd fa fa fd fd fd fd fa fa[fd]fd
  0x0c067fff99c0: fd fa fa fa fd fd fd fa fa fa 00 00 00 fa fa fa
  0x0c067fff99d0: fd fd fd fa fa fa fd fd fd fa fa fa fd fd fd fa
  0x0c067fff99e0: fa fa 00 00 00 fa fa fa 00 00 00 fa fa fa fd fd
  0x0c067fff99f0: fd fa fa fa fd fd fd fa fa fa fd fd fd fd fa fa
  0x0c067fff9a00: 00 00 00 fa fa fa 00 00 00 fa fa fa fd fd fd fd
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
==95290:95290==ABORTING

VERSION
commit 224091ca04a0477907b9efb559391f2c5f6c125f

REPRODUCTION CASE
build pdfium_test with these options
```
is_asan = true
is_debug = false

pdf_use_skia_paths = true
pdf_enable_v8 = true
pdf_enable_xfa = true
pdf_enable_xfa_bmp = true
pdf_enable_xfa_gif = true
pdf_enable_xfa_png = true
pdf_enable_xfa_tiff = true
```
./pdfium_test poc.pdf

What is the expected behavior?

What went wrong?
heap-use-after-free in PDFium

Did this work before? N/A 

Chrome version: 58.0.3029.110  Channel: n/a
OS Version: 10.0
Flash Version: Shockwave Flash 26.0 r0

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### cl...@chromium.org (2017-08-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5461827076227072.

### va...@chromium.org (2017-08-01)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### th...@chromium.org (2017-08-01)

FYI, https://pdfium.googlesource.com/pdfium/+/61f8e9c5aeb0d8cb5477e0248b685214746bada7 is where the bug first triggers.

### th...@chromium.org (2017-08-01)

The deletion that causes the free portion of the UAF is from https://pdfium.googlesource.com/pdfium/+/182d129bcee8f7731b9bbfde0064295ad3b37271

### cl...@chromium.org (2017-08-01)

Detailed report: https://clusterfuzz.com/testcase?key=5461827076227072

Job Type: linux_asan_pdfium
Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60a000022220
Crash State:
  CPDF_DataAvail::AreObjectsAvailable
  CPDF_DataAvail::AreObjectsAvailable
  CPDF_DataAvail::AreObjectsAvailable
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_pdfium&range=431183:431197

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5461827076227072


See https://github.com/google/clusterfuzz-tools for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.


### sh...@chromium.org (2017-08-01)

[Empty comment from Monorail migration]

### th...@chromium.org (2017-08-01)

ochang: You asked if this is safe [1] and it looks like the answer is no. My guess is that even without the CL in https://crbug.com/chromium/750993#c3, someone would have been able to exploit the array truncation eventually in some other way.

The part I don't understand is why the truncation is even necessary. Contrary to [2], I see ValidateDictParam() only has a single caller in CPDF_DIBSource::LoadColorInfo(). LoadColorInfo() has 2 callers - CPDF_DIBSource::Load() and CPDF_DIBSource::StartLoadDIBSource(). Both of these methods call LoadColorInfo() first, before CPDF_StreamAcc::LoadAllData(). I removed the CPDF_Array::Truncate() (was RemoveAt()) call and the original test case from https://crbug.com/chromium/552046 still passes.

[1] https://codereview.chromium.org/1406943005#msg17
[2] https://bugs.chromium.org/p/chromium/issues/detail?id=552046#c6

### th...@chromium.org (2017-08-03)

I went back to the commit that fixed https://crbug.com/chromium/552046. I reverted the changes to fpdf_render_loadimage.cpp changes to CPDF_DIBSource::GetScanline() only, and that bug came back. If I revert the pdf_parser_decode.cpp changes to PDF_DataDecode() only, then the bug remains fixed. Based on that in addition to https://crbug.com/chromium/750993#c7, the PDF_DataDecode() change that is causing this bug is probably unnecessary.

### bu...@chromium.org (2017-08-03)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/d24030d54c1fc2a2ae20551c5336335fbb8cd9b7

commit d24030d54c1fc2a2ae20551c5336335fbb8cd9b7
Author: Lei Zhang <thestig@chromium.org>
Date: Thu Aug 03 18:22:22 2017

Do not truncate the filter array in PDF_DataDecode().

It is not needed to fix https://crbug.com/552046 and it causes different
bug.

BUG=chromium:750993

Change-Id: I11627045bd3e73fb439884c3362ab1c26eb95fe3
Reviewed-on: https://pdfium-review.googlesource.com/9990
Reviewed-by: Oliver Chang <ochang@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[modify] https://crrev.com/d24030d54c1fc2a2ae20551c5336335fbb8cd9b7/core/fpdfapi/parser/fpdf_parser_decode.cpp


### bu...@chromium.org (2017-08-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e83863fbf000d2ebe7f147e5b0f21985e39cacbd

commit e83863fbf000d2ebe7f147e5b0f21985e39cacbd
Author: pdfium-deps-roller@chromium.org <pdfium-deps-roller@chromium.org>
Date: Thu Aug 03 21:17:17 2017

Roll src/third_party/pdfium/ d1a8458e6..6c740e296 (3 commits)

https://pdfium.googlesource.com/pdfium.git/+log/d1a8458e6390..6c740e29640c

$ git log d1a8458e6..6c740e296 --date=short --no-merges --format='%ad %ae %s'
2017-08-03 thestig Remove CPDF_Array::Truncate().
2017-08-02 thestig Do not truncate the filter array in PDF_DataDecode().
2017-08-03 npm Roll FreeType to 7e50824288fac5a36c2938fdb3e1c949ea53f982

Created with:
  roll-dep src/third_party/pdfium
BUG=750993


Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, see:
http://www.chromium.org/developers/tree-sheriffs/sheriff-details-chromium#TOC-Failures-due-to-DEPS-rolls


TBR=dsinclair@chromium.org

Change-Id: Ib61110d74872b3efb04880d86ce15d2d95d17ec4
Reviewed-on: https://chromium-review.googlesource.com/600891
Reviewed-by: <pdfium-deps-roller@chromium.org>
Commit-Queue: <pdfium-deps-roller@chromium.org>
Cr-Commit-Position: refs/heads/master@{#491846}
[modify] https://crrev.com/e83863fbf000d2ebe7f147e5b0f21985e39cacbd/DEPS


### th...@chromium.org (2017-08-04)

Not sure why CF didn't get around to verifying the fix yet.

### cl...@chromium.org (2017-08-05)

Detailed report: https://clusterfuzz.com/testcase?key=5461827076227072

Job Type: linux_asan_pdfium
Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60a000022220
Crash State:
  CPDF_DataAvail::AreObjectsAvailable
  CPDF_DataAvail::AreObjectsAvailable
  CPDF_DataAvail::AreObjectsAvailable
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_pdfium&range=431183:431197

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5461827076227072


See https://github.com/google/clusterfuzz-tools for more information.

### cl...@chromium.org (2017-08-05)

ClusterFuzz has detected this issue as fixed in range 491739:492052.

Detailed report: https://clusterfuzz.com/testcase?key=5461827076227072

Job Type: linux_asan_pdfium
Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60a000022220
Crash State:
  CPDF_DataAvail::AreObjectsAvailable
  CPDF_DataAvail::AreObjectsAvailable
  CPDF_DataAvail::AreObjectsAvailable
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_pdfium&range=431183:431197
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_pdfium&range=491739:492052

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5461827076227072


See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2017-08-05)

ClusterFuzz testcase 5461827076227072 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2017-08-05)

[Empty comment from Monorail migration]

### aw...@google.com (2017-08-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-08-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-08-09)

Congratulations yuanvi.cn@, the Chrome VRP panel decided to award $3,000 for this bug. A member of our finance team will be in touch to arrange for payment.

Also, if this appears in Chrome release notes, how would you like to be credited?

### aw...@chromium.org (2017-08-09)

[Empty comment from Monorail migration]

### yu...@gmail.com (2017-08-10)

Please credit to [Wei Yuan of Baidu Security Lab], Thanks.

### yu...@gmail.com (2017-10-12)

[Comment Deleted]

### sh...@chromium.org (2017-11-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-11-11)

This issue was migrated from crbug.com/chromium/750993?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088558)*
