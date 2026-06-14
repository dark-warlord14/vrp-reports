# Heap-use-after-free in CPDF_Color::~CPDF_Color

| Field | Value |
|-------|-------|
| **Issue ID** | [40080331](https://issues.chromium.org/issues/40080331) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | at...@gmail.com |
| **Assignee** | bo...@foxitsoftware.com |
| **Created** | 2014-08-30 |
| **Bounty** | $1,000.00 |

## Description



Tested on:

OS: Ubuntu 12.04

Chromium: ASAN 39.0.2141.0 (Developer Build 1113badb8206)

Crashes on pdfium_test and chromium.


ASAN-trace:

=================================================================
==18604==ERROR: AddressSanitizer: heap-use-after-free on address 0x60c000049f48 at pc 0x7fe0d8a75cda bp 0x7fff40bcbbf0 sp 0x7fff40bcbbe8
READ of size 8 at 0x60c000049f48 thread T0 (chrome)
    #0 0x7fe0d8a75cd9 in CPDF_Color::ReleaseBuffer() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_colors.cpp:1295
    #1 0x7fe0d8a75b5a in CPDF_Color::~CPDF_Color() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_colors.cpp:1284
    #2 0x7fe0d89ee8fb in CFX_CountRef<CPDF_ColorStateData>::~CFX_CountRef() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/../../../include/fpdfapi/../fxcrt/fx_basic.h:1254
    #3 0x7fe0d89ee65d in CPDF_GraphicStates::~CPDF_GraphicStates() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/../../../include/fpdfapi/fpdf_pageobj.h:437
    #4 0x7fe0d8aa078a in CPDF_PathObject::~CPDF_PathObject() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/../../../include/fpdfapi/fpdf_pageobj.h:629
    #5 0x7fe0d8a69d47 in CPDF_Form::~CPDF_Form() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page.cpp:696
.
.
.
0x60c000049f48 is located 72 bytes inside of 128-byte region [0x60c000049f00,0x60c000049f80)
freed by thread T0 (chrome) here:
    #0 0x7fe0ec29433b in free ??:0
    #1 0x7fe0d8a77830 in CPDF_DocPageData::Clear(int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_doc.cpp:164
    #2 0x7fe0d8a7a579 in CPDF_DocPageData::~CPDF_DocPageData() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_doc.cpp:149
    #3 0x7fe0d8a7757a in CPDF_PageModule::ReleaseDoc(CPDF_Document*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_doc.cpp:70
    #4 0x7fe0d8aa8238 in CPDF_Document::~CPDF_Document() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_document.cpp:102
    #5 0x7fe0d8ab9b09 in CPDF_Parser::CloseParser(int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:74
.
.
.

## Attachments

- [CPDF_ColorReleaseBuffer.pdf](attachments/CPDF_ColorReleaseBuffer.pdf) (application/pdf, 107.6 KB)

## Timeline

### cl...@chromium.org (2014-08-31)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5612784688562176

### wf...@chromium.org (2014-08-31)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-31)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5612784688562176

Uploader: wfh@chromium.org
Job Type: Linux_asan_pdfium

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6100000198c8
Crash State:
  CPDF_Color::~CPDF_Color
  CPDF_GraphicStates::~CPDF_GraphicStates
  CPDF_PathObject::~CPDF_PathObject
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=281908:281997

Minimized Testcase (107.64 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95zwakk2h5AwQ8FoXHgKC6KQNtnDtH7XHuFaM27Y9-G0t8fFgQFPyHpWDTOm5L4CBTSAGQcMNr3xR7GnZo0RLB7X2QMsNdlYR4-vIOhG4jK39F1t5Tvpxv16m88cC0oHKryteiGqejj2cdsaZIPjYPMZGfSAinV1Clj7ZgigomsSo1g5m8



### cl...@chromium.org (2014-08-31)

[Empty comment from Monorail migration]

### wf...@chromium.org (2014-09-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-01)

[Empty comment from Monorail migration]

### bo...@foxitsoftware.com (2014-09-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-02)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### bo...@foxitsoftware.com (2014-09-02)

Fixed in https://pdfium.googlesource.com/pdfium/+/1d7dc1baba517bbf862e7d144e121b2ea4ffd33b

### cl...@chromium.org (2014-09-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-04)

ClusterFuzz has detected this issue as fixed in range 293090:293185.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5612784688562176

Uploader: wfh@chromium.org
Job Type: Linux_asan_pdfium

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6100000198c8
Crash State:
  CPDF_Color::~CPDF_Color
  CPDF_GraphicStates::~CPDF_GraphicStates
  CPDF_PathObject::~CPDF_PathObject
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=281908:281997
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=293090:293185

Minimized Testcase (107.64 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95zwakk2h5AwQ8FoXHgKC6KQNtnDtH7XHuFaM27Y9-G0t8fFgQFPyHpWDTOm5L4CBTSAGQcMNr3xR7GnZo0RLB7X2QMsNdlYR4-vIOhG4jK39F1t5Tvpxv16m88cC0oHKryteiGqejj2cdsaZIPjYPMZGfSAinV1Clj7ZgigomsSo1g5m8

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ti...@chromium.org (2014-10-03)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-11-17)

Thanks for the report! This one qualified for a $1000 reward.

### ti...@google.com (2014-12-08)

Payment in progress

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-09)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/409373?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/409521]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080331)*
