# Heap-use-after-free in CPDF_Object::Release

| Field | Value |
|-------|-------|
| **Issue ID** | [40080281](https://issues.chromium.org/issues/40080281) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | at...@gmail.com |
| **Assignee** | bo...@foxitsoftware.com |
| **Created** | 2014-08-23 |
| **Bounty** | $1,500.00 |

## Description


Tested on:

OS: Ubuntu 12.04

pdfium_test: The one from ASAN Chrome 39.0.2133.0 (Developer Build 291444)

The repro-file causes clean crash in the pdfium_test, but if you open the repro-file in Chrome, Chrome fails to render the file but no crash occurs.

I would guess you guys still want to check if the issue is reachable in Chrome. 

ASAN-trace:

==16065==ERROR: AddressSanitizer: heap-use-after-free on address 0x60400000dd94 at pc 0x0000005a1d95 bp 0x7fff47d8d550 sp 0x7fff47d8d548
READ of size 4 at 0x60400000dd94 thread T0
    #0 0x5a1d94 in CPDF_Object::Release() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_objects.cpp:10
    #1 0x5a957e in CPDF_Parser::CloseParser(int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:105
    #2 0x5a9bfb in CPDF_Parser::StartParse(IFX_FileRead*, int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:148
    #3 0x5b78c2 in CPDF_Parser::StartAsynParse(IFX_FileRead*, int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:1531
    #4 0x4cb4a7 in FPDFAvail_GetDocument /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/fpdfsdk/src/fpdf_dataavail.cpp:128
    #5 0x4c4f68 in RenderPdf(char const*, char const*, unsigned long, OutputFormat) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/samples/pdfium_test.cc:282
    #6 0x4c5ad9 in main /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/samples/pdfium_test.cc:393
    #7 0x7fafb288978c in ?? ??:0
    #8 0x4c441c in _start ??:0

0x60400000dd94 is located 4 bytes inside of 48-byte region [0x60400000dd90,0x60400000ddc0)
freed by thread T0 here:
    #0 0x4a6b6b in free ??:0
    #1 0x5b7498 in CPDF_Parser::IsLinearizedFile(IFX_FileRead*, unsigned int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:1499
    #2 0x5b776e in CPDF_Parser::StartAsynParse(IFX_FileRead*, int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:1529
    #3 0x4cb4a7 in FPDFAvail_GetDocument /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/fpdfsdk/src/fpdf_dataavail.cpp:128
    #4 0x4c4f68 in RenderPdf(char const*, char const*, unsigned long, OutputFormat) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/samples/pdfium_test.cc:282
    #5 0x4c5ad9 in main /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/samples/pdfium_test.cc:393
    #6 0x7fafb288978c in ?? ??:0

previously allocated by thread T0 here:
    #0 0x4a6deb in malloc ??:0
    #1 0x507d09 in CPDF_Dictionary::Create() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/../../../include/fpdfapi/fpdf_objects.h:428
    #2 0x5b265b in CPDF_SyntaxParser::GetObject(CPDF_IndirectObjects*, unsigned int, unsigned int, int, PARSE_CONTEXT*, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:2141
    #3 0x5b71aa in CPDF_Parser::IsLinearizedFile(IFX_FileRead*, unsigned int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:1491
    #4 0x5b776e in CPDF_Parser::StartAsynParse(IFX_FileRead*, int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:1529
    #5 0x4cb4a7 in FPDFAvail_GetDocument /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/fpdfsdk/src/fpdf_dataavail.cpp:128
    #6 0x4c4f68 in RenderPdf(char const*, char const*, unsigned long, OutputFormat) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/samples/pdfium_test.cc:282
    #7 0x4c5ad9 in main /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/samples/pdfium_test.cc:393
    #8 0x7fafb288978c in ?? ??:0
.
.
.



## Attachments

- [repro-file.pdf](attachments/repro-file.pdf) (application/pdf, 634 B)

## Timeline

### cl...@chromium.org (2014-08-23)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5654766467153920

### in...@chromium.org (2014-08-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-08-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-23)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5654766467153920

Uploader: aarya@google.com
Job Type: Linux_asan_pdfium

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60b00000a9a4
Crash State:
  CPDF_Object::Release
  CPDF_Parser::CloseParser
  CPDF_Parser::StartParse
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=281908:281997

Minimized Testcase (0.62 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96Sj8yxh10JYdaGuxbDeS-5yBb6HJ0jZlE3sqR2xO0JVln3SaaEnsnlSK7DXl13yVW0Qo2E7gav7uyEuVlXAuwKXoqhDSoT-JkaLGOeWnotdHYPQIb1nM9PcQ_9hpxHeAeWCt53F4YPR3lyC9ukwrl598nZWQ



### bo...@foxitsoftware.com (2014-08-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-24)

[Empty comment from Monorail migration]

### bo...@foxitsoftware.com (2014-08-25)

Fixed in https://codereview.chromium.org/504993002/

### cl...@chromium.org (2014-08-26)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-08-27)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5654766467153920

Uploader: aarya@google.com
Job Type: Linux_asan_pdfium

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60b00000a9a4
Crash State:
  CPDF_Object::Release
  CPDF_Parser::CloseParser
  CPDF_Parser::StartParse
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=281908:281997

Minimized Testcase (0.62 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96Sj8yxh10JYdaGuxbDeS-5yBb6HJ0jZlE3sqR2xO0JVln3SaaEnsnlSK7DXl13yVW0Qo2E7gav7uyEuVlXAuwKXoqhDSoT-JkaLGOeWnotdHYPQIb1nM9PcQ_9hpxHeAeWCt53F4YPR3lyC9ukwrl598nZWQ



### cl...@chromium.org (2014-08-27)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5654766467153920

Uploader: aarya@google.com
Job Type: Linux_asan_pdfium

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60b00000a9a4
Crash State:
  CPDF_Object::Release
  CPDF_Parser::CloseParser
  CPDF_Parser::StartParse
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=281908:281997

Minimized Testcase (0.62 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96Sj8yxh10JYdaGuxbDeS-5yBb6HJ0jZlE3sqR2xO0JVln3SaaEnsnlSK7DXl13yVW0Qo2E7gav7uyEuVlXAuwKXoqhDSoT-JkaLGOeWnotdHYPQIb1nM9PcQ_9hpxHeAeWCt53F4YPR3lyC9ukwrl598nZWQ



### cl...@chromium.org (2014-08-27)

ClusterFuzz has detected this issue as fixed in range 291998:292010.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5654766467153920

Uploader: aarya@google.com
Job Type: Linux_asan_pdfium

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60b00000a9a4
Crash State:
  CPDF_Object::Release
  CPDF_Parser::CloseParser
  CPDF_Parser::StartParse
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=281908:281997
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=291998:292010

Minimized Testcase (0.62 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96Sj8yxh10JYdaGuxbDeS-5yBb6HJ0jZlE3sqR2xO0JVln3SaaEnsnlSK7DXl13yVW0Qo2E7gav7uyEuVlXAuwKXoqhDSoT-JkaLGOeWnotdHYPQIb1nM9PcQ_9hpxHeAeWCt53F4YPR3lyC9ukwrl598nZWQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ti...@chromium.org (2014-09-23)

According to CF, appears to have regressed prior to M38 and fixed after branch point. (inferno@ please double-check)

Matthew - Merge Requested for M38 (branch 2125)



### [Deleted User] (2014-09-24)

[Empty comment from Monorail migration]

### bo...@foxitsoftware.com (2014-09-26)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-09-29)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-10-30)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-11-17)

Thanks for the report! It qualified for a $1500 reward.

### cl...@chromium.org (2014-12-02)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2014-12-08)

Payment in progress

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/406868?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080281)*
