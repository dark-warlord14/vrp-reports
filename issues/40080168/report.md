# Heap-use-after-free in CPDF_TextStateData::~CPDF_TextStateData

| Field | Value |
|-------|-------|
| **Issue ID** | [40080168](https://issues.chromium.org/issues/40080168) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | at...@gmail.com |
| **Assignee** | ju...@foxitsoftware.com |
| **Created** | 2014-08-06 |
| **Bounty** | $2,000.00 |

## Description



Tested on:

OS: Ubuntu 12.04

Chromium: ASAN 38.0.2114.0 (Developer Build 287379) 


Repro-file as an attachment. After loading the repro-file, you might need to hit refresh couple of times to reproduce the issue.( or just make a HTML file that reloads the repro-file in an iframe with 100ms interval.)

ASAN-report:

==24781==ERROR: AddressSanitizer: heap-use-after-free on address 0x623000018908 at pc 0x7fda14d90ea4 bp 0x7fff07a684b0 sp 0x7fff07a684a8
READ of size 8 at 0x623000018908 thread T0 (chrome)
    #0 0x7fda14d90ea3 in CPDF_TextStateData::~CPDF_TextStateData() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_graph_state.cpp:307
    #1 0x7fda14cf3b2b in CFX_CountRef<CPDF_TextStateData>::~CFX_CountRef() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/../../../include/fpdfapi/../fxcrt/fx_basic.h:1254
    #2 0x7fda14cf38a4 in CPDF_GraphicStates::~CPDF_GraphicStates() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/../../../include/fpdfapi/fpdf_pageobj.h:435
    #3 0x7fda14d6c66a in CPDF_TextObject::~CPDF_TextObject() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page.cpp:107
    #4 0x7fda14d70c37 in CPDF_Form::~CPDF_Form() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page.cpp:700
    #5 0x7fda14d59d27 in CPDF_Type3Char::~CPDF_Type3Char() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_font/fpdf_font.cpp:1765
    #6 0x7fda14d58652 in CPDF_Type3Font::~CPDF_Type3Font() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_font/fpdf_font.cpp:1627
    #7 0x7fda14d5887a in CPDF_Type3Font::~CPDF_Type3Font() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_font/fpdf_font.cpp:1622
.
.
.
0x623000018908 is located 8 bytes inside of 6008-byte region [0x623000018900,0x62300001a078)
freed by thread T0 (chrome) here:
    #0 0x7fda2839cebb in free ??:0
    #1 0x7fda14d7e95e in CPDF_DocPageData::Clear(int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_doc.cpp:175
    #2 0x7fda14d8163a in CPDF_DocPageData::~CPDF_DocPageData() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_doc.cpp:148
    #3 0x7fda14d7e59a in CPDF_PageModule::ReleaseDoc(CPDF_Document*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_doc.cpp:70
    #4 0x7fda14dafc2b in CPDF_Document::~CPDF_Document() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_document.cpp:102
    #5 0x7fda14dc1a59 in CPDF_Parser::CloseParser(int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:73
    #6 0x7fda14dc181f in CPDF_Parser::~CPDF_Parser() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:58
.
.
.


## Attachments

- [chrome-heap-use-after-free-CPDFTextStateDataCPDFTextStateData9.pdf](attachments/chrome-heap-use-after-free-CPDFTextStateDataCPDFTextStateData9.pdf) (application/pdf, 41.8 KB)

## Timeline

### cl...@chromium.org (2014-08-06)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5638135385948160

### in...@chromium.org (2014-08-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-06)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5638135385948160

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x623000005508
Crash State:
  - crash stack -
  CPDF_TextStateData::~CPDF_TextStateData
  CPDF_GraphicStates::~CPDF_GraphicStates
  - free stack -
  CPDF_DocPageData::Clear
  CPDF_DocPageData::~CPDF_DocPageData
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=281908:281997

Minimized Testcase (41.78 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95Q7akuMlpvfOob5n42pEZbmxXWUSkjsrFoB5L1tR1x1EhO3UC69aLQmiCJs7itWhoWUGYDnZDU-Amas3Oirr8JezaUEDZTwsQr-gnYrxVRxHYiu7R2knlyv13g4_F4PMtNxR3RcrcCRphM1lwoMU0NHwXPYTwrQJlhwwUU_35elCEkF3s



### ts...@chromium.org (2014-08-06)

[Empty comment from Monorail migration]

### ju...@foxitsoftware.com (2014-08-06)

I'll handle this one.

### cl...@chromium.org (2014-08-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-09)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-08-09)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5638135385948160

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x623000005508
Crash State:
  - crash stack -
  CPDF_TextStateData::~CPDF_TextStateData
  CPDF_GraphicStates::~CPDF_GraphicStates
  - free stack -
  CPDF_DocPageData::Clear
  CPDF_DocPageData::~CPDF_DocPageData
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=281908:281997

Minimized Testcase (41.78 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95Q7akuMlpvfOob5n42pEZbmxXWUSkjsrFoB5L1tR1x1EhO3UC69aLQmiCJs7itWhoWUGYDnZDU-Amas3Oirr8JezaUEDZTwsQr-gnYrxVRxHYiu7R2knlyv13g4_F4PMtNxR3RcrcCRphM1lwoMU0NHwXPYTwrQJlhwwUU_35elCEkF3s



### ju...@foxitsoftware.com (2014-08-16)

It's pending in the review https://codereview.chromium.org/477323002/.

### ju...@foxitsoftware.com (2014-08-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-18)

[Empty comment from Monorail migration]

### ju...@foxitsoftware.com (2014-08-18)

It's fixed in https://pdfium.googlesource.com/pdfium/+/2d55db1.

### bu...@chromium.org (2014-08-18)

Is there a merge required here?

### cl...@chromium.org (2014-08-19)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5638135385948160

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x623000005508
Crash State:
  CPDF_TextStateData::~CPDF_TextStateData
  CPDF_GraphicStates::~CPDF_GraphicStates
  CPDF_TextObject::~CPDF_TextObject
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=281908:281997

Minimized Testcase (41.78 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95Q7akuMlpvfOob5n42pEZbmxXWUSkjsrFoB5L1tR1x1EhO3UC69aLQmiCJs7itWhoWUGYDnZDU-Amas3Oirr8JezaUEDZTwsQr-gnYrxVRxHYiu7R2knlyv13g4_F4PMtNxR3RcrcCRphM1lwoMU0NHwXPYTwrQJlhwwUU_35elCEkF3s



### cl...@chromium.org (2014-08-19)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-08-21)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5638135385948160

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x623000005508
Crash State:
  CPDF_TextStateData::~CPDF_TextStateData
  CPDF_GraphicStates::~CPDF_GraphicStates
  CPDF_TextObject::~CPDF_TextObject
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=281908:281997

Minimized Testcase (41.78 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95Q7akuMlpvfOob5n42pEZbmxXWUSkjsrFoB5L1tR1x1EhO3UC69aLQmiCJs7itWhoWUGYDnZDU-Amas3Oirr8JezaUEDZTwsQr-gnYrxVRxHYiu7R2knlyv13g4_F4PMtNxR3RcrcCRphM1lwoMU0NHwXPYTwrQJlhwwUU_35elCEkF3s



### ts...@chromium.org (2014-08-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-27)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5638135385948160

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x623000005508
Crash State:
  CPDF_TextStateData::~CPDF_TextStateData
  CPDF_GraphicStates::~CPDF_GraphicStates
  CPDF_TextObject::~CPDF_TextObject
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=281908:281997

Minimized Testcase (41.78 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95Q7akuMlpvfOob5n42pEZbmxXWUSkjsrFoB5L1tR1x1EhO3UC69aLQmiCJs7itWhoWUGYDnZDU-Amas3Oirr8JezaUEDZTwsQr-gnYrxVRxHYiu7R2knlyv13g4_F4PMtNxR3RcrcCRphM1lwoMU0NHwXPYTwrQJlhwwUU_35elCEkF3s



### cl...@chromium.org (2014-08-27)

ClusterFuzz has detected this issue as fixed in range 291998:292010.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5638135385948160

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x623000005508
Crash State:
  CPDF_TextStateData::~CPDF_TextStateData
  CPDF_GraphicStates::~CPDF_GraphicStates
  CPDF_TextObject::~CPDF_TextObject
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=281908:281997
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=291998:292010

Minimized Testcase (41.78 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95Q7akuMlpvfOob5n42pEZbmxXWUSkjsrFoB5L1tR1x1EhO3UC69aLQmiCJs7itWhoWUGYDnZDU-Amas3Oirr8JezaUEDZTwsQr-gnYrxVRxHYiu7R2knlyv13g4_F4PMtNxR3RcrcCRphM1lwoMU0NHwXPYTwrQJlhwwUU_35elCEkF3s

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2014-08-27)

Attekett, are you still able to reproduce this from latest trunk build ?

### ti...@chromium.org (2014-09-23)

Matthew - Merge Requested for M38 (Branch 2125). Regression prior to branch point.

### [Deleted User] (2014-09-24)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-09-24)

Jun - please merge to M38 / branch 2125

### ju...@foxitsoftware.com (2014-09-25)

merge done.

### ma...@google.com (2014-09-26)

Please process the merge approval if you haven't.

### ti...@chromium.org (2014-09-29)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-10-07)

Atte - $2000 for this report. Notes from the panel: Does not seem like there is control between use and free - too many common stack frames.

### cl...@chromium.org (2014-11-25)

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/400996?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/406823]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080168)*
