# AddressSanitizer: heap-buffer-overflow on address 0x7f4a13edc800 

| Field | Value |
|-------|-------|
| **Issue ID** | [40084395](https://issues.chromium.org/issues/40084395) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Reporter** | ma...@gmail.com |
| **Assignee** | oc...@chromium.org |
| **Created** | 2016-05-26 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36

Steps to reproduce the problem:
1. Build pdf_xml_fuzzer
2. Open crash1.xml

What is the expected behavior?

What went wrong?
./pdf_xml_fuzzer: Running 1 inputs 1 time(s) each.
crash1.xml ... =================================================================
==3228==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7f1e3805f800 at pc 0x000003e5b16a bp 0x7ffcec1e0ae0 sp 0x7ffcec1e0ad8
READ of size 4 at 0x7f1e3805f800 thread T0
    #0 0x3e5b169  (/home/mtowalski/chromium/src/out/libfuzzer/pdf_xml_fuzzer+0x3e5b169)
    #1 0x3e4e508  (/home/mtowalski/chromium/src/out/libfuzzer/pdf_xml_fuzzer+0x3e4e508)
    #2 0x3e82038  (/home/mtowalski/chromium/src/out/libfuzzer/pdf_xml_fuzzer+0x3e82038)
    #3 0x3e4131d  (/home/mtowalski/chromium/src/out/libfuzzer/pdf_xml_fuzzer+0x3e4131d)
    #4 0x4e7665  (/home/mtowalski/chromium/src/out/libfuzzer/pdf_xml_fuzzer+0x4e7665)
    #5 0x525334  (/home/mtowalski/chromium/src/out/libfuzzer/pdf_xml_fuzzer+0x525334)
    #6 0x524206  (/home/mtowalski/chromium/src/out/libfuzzer/pdf_xml_fuzzer+0x524206)
    #7 0x4e9a73  (/home/mtowalski/chromium/src/out/libfuzzer/pdf_xml_fuzzer+0x4e9a73)
    #8 0x4ed617  (/home/mtowalski/chromium/src/out/libfuzzer/pdf_xml_fuzzer+0x4ed617)
    #9 0x4e9c64  (/home/mtowalski/chromium/src/out/libfuzzer/pdf_xml_fuzzer+0x4e9c64)
    #10 0x565989  (/home/mtowalski/chromium/src/out/libfuzzer/pdf_xml_fuzzer+0x565989)
    #11 0x7f1e386e0ec4  (/lib/x86_64-linux-gnu/libc.so.6+0x21ec4)

0x7f1e3805f800 is located 0 bytes to the right of 131072-byte region [0x7f1e3803f800,0x7f1e3805f800)
allocated by thread T0 here:
    #0 0x4b8e24  (/home/mtowalski/chromium/src/out/libfuzzer/pdf_xml_fuzzer+0x4b8e24)
    #1 0x4e85bb  (/home/mtowalski/chromium/src/out/libfuzzer/pdf_xml_fuzzer+0x4e85bb)
    #2 0x3e40c29  (/home/mtowalski/chromium/src/out/libfuzzer/pdf_xml_fuzzer+0x3e40c29)
    #3 0x3e81a80  (/home/mtowalski/chromium/src/out/libfuzzer/pdf_xml_fuzzer+0x3e81a80)
    #4 0x4e7136  (/home/mtowalski/chromium/src/out/libfuzzer/pdf_xml_fuzzer+0x4e7136)
    #5 0x525334  (/home/mtowalski/chromium/src/out/libfuzzer/pdf_xml_fuzzer+0x525334)
    #6 0x524206  (/home/mtowalski/chromium/src/out/libfuzzer/pdf_xml_fuzzer+0x524206)
    #7 0x4e9a73  (/home/mtowalski/chromium/src/out/libfuzzer/pdf_xml_fuzzer+0x4e9a73)
    #8 0x4ed617  (/home/mtowalski/chromium/src/out/libfuzzer/pdf_xml_fuzzer+0x4ed617)
    #9 0x4e9c64  (/home/mtowalski/chromium/src/out/libfuzzer/pdf_xml_fuzzer+0x4e9c64)
    #10 0x565989  (/home/mtowalski/chromium/src/out/libfuzzer/pdf_xml_fuzzer+0x565989)
    #11 0x7f1e386e0ec4  (/lib/x86_64-linux-gnu/libc.so.6+0x21ec4)

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/mtowalski/chromium/src/out/libfuzzer/pdf_xml_fuzzer+0x3e5b169)
Shadow bytes around the buggy address:
  0x0fe447003eb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe447003ec0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe447003ed0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe447003ee0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe447003ef0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0fe447003f00:[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0fe447003f10: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0fe447003f20: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0fe447003f30: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0fe447003f40: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0fe447003f50: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Heap right redzone:      fb
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack partial redzone:   f4
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
==3228==ABORTING
DEATH:

Did this work before? N/A 

Chrome version: 50.0.2661.102  Channel: n/a
OS Version: 14.04 LTS x64
Flash Version: Shockwave Flash 21.0 r0

## Attachments

- [crash1.xml](attachments/crash1.xml) (text/plain, 32.5 KB)

## Timeline

### me...@chromium.org (2016-05-26)

Oliver, can you please triage? I believe XFA isn't enabled yet, so I'm not sure about the security impact of this.

[Monorail components: Internals>Plugins>PDF]

### oc...@chromium.org (2016-05-26)

XFA is enabled on HEAD. Symbolized stack trace:

==26413==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7f2328c3c800 at pc 0x000003e5c1da bp 0x7fffb4efe2e0 sp 0x7fffb4efe2d8
READ of size 4 at 0x7f2328c3c800 thread T0
    #0 0x3e5c1d9 in FX_wcsnicmp(wchar_t const*, wchar_t const*, unsigned long) out/Fuzzer/../../third_party/pdfium/xfa/fgas/crt/fgas_system.cpp:30:33
    #1 0x3e4f578 in CFDE_XMLSyntaxParser::DoSyntaxParse() out/Fuzzer/../../third_party/pdfium/xfa/fde/xml/fde_xml_imp.cpp:1889:15
    #2 0x3e830a8 in CXFA_XMLParser::DoParser(IFX_Pause*) out/Fuzzer/../../third_party/pdfium/xfa/fxfa/parser/xfa_parser_imp.cpp:1430:28
    #3 0x3e4238d in CFDE_XMLDoc::DoLoad(IFX_Pause*) out/Fuzzer/../../third_party/pdfium/xfa/fde/xml/fde_xml_imp.cpp:934:22
    #4 0x4e7665 in LLVMFuzzerTestOneInput out/Fuzzer/../../third_party/pdfium/testing/libfuzzer/pdf_xml_fuzzer.cc:64:25
    #5 0x525334 in fuzzer::Fuzzer::ExecuteCallback(unsigned char const*, unsigned long) out/Fuzzer/../../third_party/libFuzzer/src/FuzzerLoop.cpp:465:13
    #6 0x524206 in fuzzer::Fuzzer::RunOne(unsigned char const*, unsigned long) out/Fuzzer/../../third_party/libFuzzer/src/FuzzerLoop.cpp:398:3
    #7 0x4e9a73 in fuzzer::RunOneTest(fuzzer::Fuzzer*, char const*) out/Fuzzer/../../third_party/libFuzzer/src/FuzzerDriver.cpp:256:3
    #8 0x4ed617 in fuzzer::FuzzerDriver(std::__1::vector<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::allocator<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > > > const&, int (*)(unsigned char const*, unsigned long)) out/Fuzzer/../../third_party/libFuzzer/src/FuzzerDriver.cpp:372:9
    #9 0x4e9c64 in fuzzer::FuzzerDriver(int, char**, int (*)(unsigned char const*, unsigned long)) out/Fuzzer/../../third_party/libFuzzer/src/FuzzerDriver.cpp:421:10
    #10 0x565989 in main out/Fuzzer/../../third_party/libFuzzer/src/FuzzerMain.cpp:25:10
    #11 0x7f23292c9ec4 in __libc_start_main /build/eglibc-3GlaMS/eglibc-2.19/csu/libc-start.c:287

0x7f2328c3c800 is located 0 bytes to the right of 131072-byte region [0x7f2328c1c800,0x7f2328c3c800)
allocated by thread T0 here:
    #0 0x4b8e24 in __interceptor_calloc (/mnt/ssd/chromium2/src/out/Fuzzer/pdf_xml_fuzzer+0x4b8e24)
    #1 0x4e85bb in FX_AllocOrDie(unsigned long, unsigned long) out/Fuzzer/../../third_party/pdfium/core/fxcrt/include/fx_memory.h:39:22
    #2 0x3e41c99 in CFDE_XMLSyntaxParser::Init(IFX_Stream*, int, int) out/Fuzzer/../../third_party/pdfium/xfa/fde/xml/fde_xml_imp.cpp:1477:15
    #3 0x3e82af0 in CXFA_XMLParser::CXFA_XMLParser(CFDE_XMLNode*, IFX_Stream*) out/Fuzzer/../../third_party/pdfium/xfa/fxfa/parser/xfa_parser_imp.cpp:1412:3
    #4 0x4e7136 in LLVMFuzzerTestOneInput out/Fuzzer/../../third_party/pdfium/testing/libfuzzer/pdf_xml_fuzzer.cc:59:11
    #5 0x525334 in fuzzer::Fuzzer::ExecuteCallback(unsigned char const*, unsigned long) out/Fuzzer/../../third_party/libFuzzer/src/FuzzerLoop.cpp:465:13
    #6 0x524206 in fuzzer::Fuzzer::RunOne(unsigned char const*, unsigned long) out/Fuzzer/../../third_party/libFuzzer/src/FuzzerLoop.cpp:398:3
    #7 0x4e9a73 in fuzzer::RunOneTest(fuzzer::Fuzzer*, char const*) out/Fuzzer/../../third_party/libFuzzer/src/FuzzerDriver.cpp:256:3
    #8 0x4ed617 in fuzzer::FuzzerDriver(std::__1::vector<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::allocator<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > > > const&, int (*)(unsigned char const*, unsigned long)) out/Fuzzer/../../third_party/libFuzzer/src/FuzzerDriver.cpp:372:9
    #9 0x4e9c64 in fuzzer::FuzzerDriver(int, char**, int (*)(unsigned char const*, unsigned long)) out/Fuzzer/../../third_party/libFuzzer/src/FuzzerDriver.cpp:421:10
    #10 0x565989 in main out/Fuzzer/../../third_party/libFuzzer/src/FuzzerMain.cpp:25:10
    #11 0x7f23292c9ec4 in __libc_start_main /build/eglibc-3GlaMS/eglibc-2.19/csu/libc-start.c:287


### sh...@chromium.org (2016-05-27)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-05-27)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium.git/+/816ff7b92ff0f94e4ffaafc975b08d2c4c1a6417

commit 816ff7b92ff0f94e4ffaafc975b08d2c4c1a6417
Author: ochang <ochang@chromium.org>
Date: Fri May 27 17:16:12 2016

Make sure CFDE_XMLSyntaxParser's buffer is null terminated.

BUG=chromium:614962

Review-Url: https://codereview.chromium.org/2017803002

[modify] https://crrev.com/816ff7b92ff0f94e4ffaafc975b08d2c4c1a6417/xfa/fde/xml/fde_xml_imp.cpp


### bu...@chromium.org (2016-05-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/cc5a500413f69e6dd7d89404f662e13fb2071e90

commit cc5a500413f69e6dd7d89404f662e13fb2071e90
Author: ochang <ochang@chromium.org>
Date: Fri May 27 21:43:45 2016

Roll PDFium 490d612..d23df55

https://pdfium.googlesource.com/pdfium.git/+log/490d612..d23df55

BUG=615424,614962
TBR=thestig@chromium.org

Review-Url: https://codereview.chromium.org/2016983003
Cr-Commit-Position: refs/heads/master@{#396569}

[modify] https://crrev.com/cc5a500413f69e6dd7d89404f662e13fb2071e90/DEPS


### me...@chromium.org (2016-05-27)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-27)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### go...@chromium.org (2016-05-27)

Before we approve merge to M51, Could you please confirm whether this change is baked/verified in Canary and safe to merge?


### ti...@google.com (2016-05-27)

@meacer - does this even need to go to stable? XFA is only enabled on head, so can this roll with M52?

### me...@chromium.org (2016-05-27)

Sure, that makes sense.

### ti...@google.com (2016-05-27)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### ti...@google.com (2016-05-27)

Thanks @meacer.

Krishna - please approve for M52 / 2743

### go...@chromium.org (2016-05-27)

Approved for M52 branch 2743 based on https://crbug.com/chromium/614962#c12.

### bu...@chromium.org (2016-05-27)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=88327

------------------------------------------------------------------
r88327 | ochang@google.com | 2016-05-27T23:37:29.119216Z

-----------------------------------------------------------------

### sh...@chromium.org (2016-05-28)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-31)

Thanks for your report. We'll consider your report under the Chrome Reward Program for a security cash reward - full details here: https://www.google.com/about/appsecurity/chrome-rewards/

We'll update you once we have a decision. Feel free to check in with me in a few weeks if you haven't heard back, either by updating this bug or reaching out to me at timwillis@

### aw...@chromium.org (2016-08-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-30)

Congratulations, the panel has decided to award $1,000 for this bug.  A member of our finance team will be in touch shortly.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2016-09-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/614962?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084395)*
