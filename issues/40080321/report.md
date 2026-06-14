# Heap-use-after-free in CFX_BaseSegmentedArray::Iterate

| Field | Value |
|-------|-------|
| **Issue ID** | [40080321](https://issues.chromium.org/issues/40080321) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | at...@gmail.com |
| **Assignee** | bo...@foxitsoftware.com |
| **Created** | 2014-08-28 |
| **Bounty** | $1,000.00 |

## Description



Tested on:

OS: Ubuntu 12.04

pdfium_test: from ASAN Chromium 39.0.2139.0 (Developer Build 0b61f008f6a2)

This bug doesn't reproduce when the file is opened in Chrome, but will reproduce in pdfium_test.

ASAN-trace:

==15466==ERROR: AddressSanitizer: heap-use-after-free on address 0x60400000cb78 at pc 0x0000007d0bfa bp 0x7fffd45ec310 sp 0x7fffd45ec308
READ of size 8 at 0x60400000cb78 thread T0
    #0 0x7d0bf9 in CFX_BaseSegmentedArray::Iterate(int (*)(void*, void*), void*) const /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxcrt/fx_basic_array.cpp:312
    #1 0x7e1f32 in CFX_CMapByteStringToPtr::Lookup(CFX_ByteStringC const&, void*&) const /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxcrt/fx_basic_maps.cpp:507
    #2 0x5a6104 in CPDF_Dictionary::GetElementValue(CFX_ByteStringC const&) const /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_objects.cpp:601
    #3 0x5a6e51 in CPDF_Dictionary::GetDict(CFX_ByteStringC const&) const /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_objects.cpp:692
    #4 0x50ba7e in CPDF_InterForm::CPDF_InterForm(CPDF_Document*, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfdoc/doc_form.cpp:275
    #5 0x4dc5f2 in CPDFSDK_InterForm::CPDFSDK_InterForm(CPDFSDK_Document*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/fpdfsdk/src/fsdk_baseform.cpp:1691
    #6 0x4e6e4a in CPDFSDK_Document::GetInterForm() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/fpdfsdk/src/fsdk_mgr.cpp:474
    #7 0x4c7166 in FPDF_SetFormFieldHighlightColor /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/fpdfsdk/src/fpdfformfill.cpp:292
    #8 0x4c4fe6 in RenderPdf(char const*, char const*, unsigned long, OutputFormat) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/samples/pdfium_test.cc:293
    #9 0x4c5b59 in main /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/samples/pdfium_test.cc:406
    #10 0x7f59a3d4b78c in ?? ??:0
    #11 0x4c441c in _start ??:0

0x60400000cb78 is located 40 bytes inside of 48-byte region [0x60400000cb50,0x60400000cb80)
freed by thread T0 here:
    #0 0x4a6b6b in free ??:0
    #1 0x5a8ca5 in CPDF_IndirectObjects::InsertIndirectObject(unsigned int, CPDF_Object*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_objects.cpp:1281
    #2 0x5b088c in CPDF_Parser::LoadCrossRefV5(long, long&, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:1008
    #3 0x5b80ba in CPDF_Parser::LoadLinearizedAllCrossRefV5(long) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:1617
    #4 0x5b8680 in CPDF_Parser::LoadLinearizedMainXRefTable() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:1658
    #5 0x5c5f80 in CPDF_DataAvail::CheckLinearizedData(IFX_DownloadHints*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:4134
    #6 0x5c79f1 in CPDF_DataAvail::IsFormAvail(IFX_DownloadHints*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:4374
.
.
.

previously allocated by thread T0 here:
    #0 0x4a6deb in malloc ??:0
    #1 0x507d29 in CPDF_Dictionary::Create() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/../../../include/fpdfapi/fpdf_objects.h:428
    #2 0x5b296b in CPDF_SyntaxParser::GetObject(CPDF_IndirectObjects*, unsigned int, unsigned int, int, PARSE_CONTEXT*, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:2154
    #3 0x5b33ab in CPDF_Parser::ParseIndirectObjectAt(CPDF_IndirectObjects*, long, unsigned int, PARSE_CONTEXT*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:1389
    #4 0x5b3c21 in CPDF_Parser::ParseIndirectObject(CPDF_IndirectObjects*, unsigned int, PARSE_CONTEXT*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:1192
    #5 0x5a25a6 in CPDF_IndirectObjects::GetIndirectObject(unsigned int, PARSE_CONTEXT*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_objects.cpp:1216
    #6 0x59edd0 in CPDF_Document::LoadDoc() 
.
.
.


## Attachments

- [CFX_BaseSegmentedArrayIterate.pdf](attachments/CFX_BaseSegmentedArrayIterate.pdf) (application/pdf, 903 B)

## Timeline

### cl...@chromium.org (2014-08-28)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5640013640368128

### in...@chromium.org (2014-08-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-28)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5640013640368128

Uploader: aarya@google.com
Job Type: Linux_asan_pdfium

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60b000007798
Crash State:
  CFX_BaseSegmentedArray::Iterate
  CFX_CMapByteStringToPtr::Lookup
  CPDF_Dictionary::GetDict
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=281908:281997

Minimized Testcase (0.88 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94EBXhOw-ikDlKYGVPyWbQfiQIlz-UdlqebXjwW6UWXlA0RnKwIys3m5TevnsgOj861Y52xkgsdUMySE8BbcgjdkHmaTDgtLSQBD77gbYrdIuS9zB2Z16hWMta66sEmcjfzhspGs2XPm7G1yAw1vip2DkDi7Q



### cl...@chromium.org (2014-08-28)

[Empty comment from Monorail migration]

### bo...@foxitsoftware.com (2014-08-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-31)

[Empty comment from Monorail migration]

### wf...@chromium.org (2014-08-31)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-31)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-01)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-09-08)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-09-15)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### bo...@foxitsoftware.com (2014-09-19)

Fixed in https://pdfium.googlesource.com/pdfium/+/2d282243dbd1edd51d42e13f563903a1a76ce8f8

### cl...@chromium.org (2014-09-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-22)

ClusterFuzz has detected this issue as fixed in range 295856:295875.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5640013640368128

Uploader: aarya@google.com
Job Type: Linux_asan_pdfium

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60b000007798
Crash State:
  CFX_BaseSegmentedArray::Iterate
  CFX_CMapByteStringToPtr::Lookup
  CPDF_Dictionary::GetDict
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=281908:281997
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=295856:295875

Minimized Testcase (0.88 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94EBXhOw-ikDlKYGVPyWbQfiQIlz-UdlqebXjwW6UWXlA0RnKwIys3m5TevnsgOj861Y52xkgsdUMySE8BbcgjdkHmaTDgtLSQBD77gbYrdIuS9zB2Z16hWMta66sEmcjfzhspGs2XPm7G1yAw1vip2DkDi7Q

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ti...@chromium.org (2014-10-03)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-11-17)

Thanks for the report! This one qualified for a $1000 reward.

### ti...@google.com (2014-12-08)

Payment in progress

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-27)

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

This issue was migrated from crbug.com/chromium/408532?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080321)*
