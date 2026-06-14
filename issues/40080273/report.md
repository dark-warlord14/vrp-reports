# Heap-buffer-overflow in CPDF_SyntaxParser::SearchWord

| Field | Value |
|-------|-------|
| **Issue ID** | [40080273](https://issues.chromium.org/issues/40080273) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | at...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2014-08-22 |
| **Bounty** | $500.00 |

## Description



Tested on:

OS: Ubuntu 12.04

Chromium: ASAN 39.0.2133.0 (Developer Build 291392)


ASAN-trace:

==21325==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x61500000f2fc at pc 0x0000005b8dc1 bp 0x7fff4bc87890 sp 0x7fff4bc87888
READ of size 1 at 0x61500000f2fc thread T0
    #0 0x5b8dc0 in CPDF_SyntaxParser::GetCharAtBackward(long, unsigned char&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:1739
    #1 0x5aac11 in CPDF_SyntaxParser::SearchWord(CFX_ByteStringC const&, int, int, long) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:2565
    #2 0x5a9e6f in CPDF_Parser::StartParse(IFX_FileRead*, int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:170
    #3 0x5b78c2 in CPDF_Parser::StartAsynParse(IFX_FileRead*, int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:1531
    #4 0x4cb4a7 in FPDFAvail_GetDocument /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/fpdfsdk/src/fpdf_dataavail.cpp:128
    #5 0x4c4f68 in RenderPdf(char const*, char const*, unsigned long, OutputFormat) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/samples/pdfium_test.cc:282
    #6 0x4c5ad9 in main /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/samples/pdfium_test.cc:393
    #7 0x7f187dea078c in ?? ??:0
    #8 0x4c441c in _start ??:0

0x61500000f2fc is located 4 bytes to the left of 512-byte region [0x61500000f300,0x61500000f500)
allocated by thread T0 here:
    #0 0x4a6f40 in calloc ??:0
    #1 0x5aa711 in CPDF_SyntaxParser::InitParser(IFX_FileRead*, unsigned int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:2498
    #2 0x5a9cc7 in CPDF_Parser::StartParse(IFX_FileRead*, int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:159
    #3 0x5b78c2 in CPDF_Parser::StartAsynParse(IFX_FileRead*, int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:1531
    #4 0x4cb4a7 in FPDFAvail_GetDocument /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/fpdfsdk/src/fpdf_dataavail.cpp:128
    #5 0x4c4f68 in RenderPdf(char const*, char const*, unsigned long, OutputFormat) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/samples/pdfium_test.cc:282
    #6 0x4c5ad9 in main /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/samples/pdfium_test.cc:393
    #7 0x7f187dea078c in ?? ??:0
.
.
.



## Attachments

- [repro-file-CPDFSyntaxParse.pdf](attachments/repro-file-CPDFSyntaxParse.pdf) (application/pdf, 5 B)

## Timeline

### cl...@chromium.org (2014-08-22)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=6107030742892544

### in...@chromium.org (2014-08-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-08-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-22)

[Empty comment from Monorail migration]

### ts...@chromium.org (2014-08-22)

First problem is a failure to check return value from GetCharAt(5, ch) around fpdf_parser_parser.cpp:161.  We just assume that it worked, which isn't the case with this 5 char repro file.

### cl...@chromium.org (2014-08-23)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6107030742892544

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x61500003f4fc
Crash State:
  CPDF_SyntaxParser::SearchWord
  CPDF_Parser::StartParse
  FPDF_LoadCustomDocument
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=281908:281997

Minimized Testcase (0.00 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94BLsaen-3iBW1QWgqi5fJueiLaZw3HuoI4ZtM7wEMoUJQ15W0s8gR_6cuT9csCZVZb_XwNjHY9juGYdKACkNk4wtSVHO8tqYh9Lv23Kq55zomH3phxt4Uoh0f0DX-l1slhkKp2o2F-OxgTWEwkm3tdMUo68w



### cl...@chromium.org (2014-08-23)

[Empty comment from Monorail migration]

### ts...@chromium.org (2014-08-25)

I'll cobble up a patch for this one.

### ts...@chromium.org (2014-08-25)

CL at https://codereview.chromium.org/501823003/

### ts...@chromium.org (2014-08-25)

[Empty comment from Monorail migration]

### ts...@chromium.org (2014-08-25)

Fixed in https://pdfium.googlesource.com/pdfium/+/a3c7215

### cl...@chromium.org (2014-08-25)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6107030742892544

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x61500003f4fc
Crash State:
  CPDF_SyntaxParser::SearchWord
  CPDF_Parser::StartParse
  FPDF_LoadCustomDocument
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=281908:281997

Minimized Testcase (0.00 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94BLsaen-3iBW1QWgqi5fJueiLaZw3HuoI4ZtM7wEMoUJQ15W0s8gR_6cuT9csCZVZb_XwNjHY9juGYdKACkNk4wtSVHO8tqYh9Lv23Kq55zomH3phxt4Uoh0f0DX-l1slhkKp2o2F-OxgTWEwkm3tdMUo68w



### cl...@chromium.org (2014-08-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-27)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6107030742892544

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x61500003f4fc
Crash State:
  CPDF_SyntaxParser::SearchWord
  CPDF_Parser::StartParse
  FPDF_LoadCustomDocument
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=281908:281997

Minimized Testcase (0.00 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94BLsaen-3iBW1QWgqi5fJueiLaZw3HuoI4ZtM7wEMoUJQ15W0s8gR_6cuT9csCZVZb_XwNjHY9juGYdKACkNk4wtSVHO8tqYh9Lv23Kq55zomH3phxt4Uoh0f0DX-l1slhkKp2o2F-OxgTWEwkm3tdMUo68w



### cl...@chromium.org (2014-08-27)

ClusterFuzz has detected this issue as fixed in range 291998:292010.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6107030742892544

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x61500003f4fc
Crash State:
  CPDF_SyntaxParser::SearchWord
  CPDF_Parser::StartParse
  FPDF_LoadCustomDocument
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=281908:281997
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=291998:292010

Minimized Testcase (0.00 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94BLsaen-3iBW1QWgqi5fJueiLaZw3HuoI4ZtM7wEMoUJQ15W0s8gR_6cuT9csCZVZb_XwNjHY9juGYdKACkNk4wtSVHO8tqYh9Lv23Kq55zomH3phxt4Uoh0f0DX-l1slhkKp2o2F-OxgTWEwkm3tdMUo68w

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2014-12-02)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-01-22)

$500 for this report.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-15)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/406591?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080273)*
