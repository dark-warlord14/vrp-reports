# Heap-use-after-free in CPDF_Color::SetValue

| Field | Value |
|-------|-------|
| **Issue ID** | [40080191](https://issues.chromium.org/issues/40080191) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | at...@gmail.com |
| **Assignee** | bo...@foxitsoftware.com |
| **Created** | 2014-08-09 |
| **Bounty** | $3,000.00 |

## Description


Tested on:

OS: Ubuntu 12.04

Chromium: ASAN 	38.0.2118.0 (Developer Build 288412)  


Repro-file as an attachment. The repro-file didn't trigger the crash when loaded directly into Chrome. run.html loads the pdf-file into an iframe and reproduces the crash.

Asan-report:

==3728==ERROR: AddressSanitizer: heap-use-after-free on address 0x6060000fcda8 at pc 0x7fc4b6440b56 bp 0x7fff362d8fc0 sp 0x7fff362d8fb8
READ of size 8 at 0x6060000fcda8 thread T0 (chrome)
    #0 0x7fc4b6440b55 in CPDF_Color::SetValue(CPDF_Pattern*, float*, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_colors.cpp:1318
    #1 0x7fc4b646bb74 in CPDF_Pattern::~CPDF_Pattern() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_pattern.cpp:21
    #2 0x7fc4b646bffa in CPDF_TilingPattern::~CPDF_TilingPattern() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_pattern.cpp:41
    #3 0x7fc4b6442120 in CPDF_DocPageData::Clear(int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_doc.cpp:162
    #4 0x7fc4b6444f3d in CPDF_DocPageData::~CPDF_DocPageData() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_doc.cpp:147
    #5 0x7fc4b6441eaa in CPDF_PageModule::ReleaseDoc(CPDF_Document*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_doc.cpp:70
.
.
.
0x6060000fcda8 is located 8 bytes inside of 56-byte region [0x6060000fcda0,0x6060000fcdd8)
freed by thread T0 (chrome) here:
    #0 0x7fc4c9b8da9b in free ??:0
    #1 0x7fc4b63b712d in CPDF_GraphicStates::~CPDF_GraphicStates() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/../../../include/fpdfapi/fpdf_pageobj.h:435
    #2 0x7fc4b6456156 in CPDF_StreamContentParser::~CPDF_StreamContentParser() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_parser.cpp:72
    #3 0x7fc4b64686d9 in CPDF_ContentParser::Clear() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_parser_old.cpp:913
    #4 0x7fc4b643461c in CPDF_PageObjects::ContinueParse(IFX_Pause*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page.cpp:711
    #5 0x7fc4b645be2e in CPDF_StreamContentParser::AddForm(CPDF_Stream*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_parser.cpp:793
    #6 0x7fc4b645b68c in CPDF_StreamContentParser::Handle_ExecuteXObject() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_parser.cpp:740
.
.
.




## Attachments

- [repro-file.pdf](attachments/repro-file.pdf) (application/pdf, 158.6 KB)
- [run.html](attachments/run.html) (text/html, 273 B)

## Timeline

### cl...@chromium.org (2014-08-09)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5584270422704128

### in...@chromium.org (2014-08-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-10)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5584270422704128

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60c0001e5d88
Crash State:
  - crash stack -
  CPDF_Color::SetValue
  CPDF_TilingPattern::~CPDF_TilingPattern
  - free stack -
  CPDF_GraphicStates::~CPDF_GraphicStates
  CPDF_StreamContentParser::~CPDF_StreamContentParser
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=288030:288271

Minimized Testcase (147.42 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96zcOcSbIzf_u84h8zoh_6TiBhkteVujOsCJtprTZQcUmcOsUicm0Ddy1ZzaHxVhjrFquLMRAhRc2SFPjXrQphuCo-nr4F0wq4IIGk3fztQUV--y9BcbMs3QTFromMqB7M41SklYemMI039l1eIecqbDW6rLMqHoJKwKT7uB2v2ZqowHgM



### in...@chromium.org (2014-08-10)

Jeun@, ccing you since findit project should be nail down using the git regression range to https://pdfium.googlesource.com/pdfium/+/1b9c5c4dc41956b8c5ab17b9a882adf8a2513768. Please make sure it works before handing us findit.

### cl...@chromium.org (2014-08-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-10)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### [Deleted User] (2014-08-12)

Findit can identify this case correctly. Below is the output from the script.

-------------------------------------------
Found these CLs to be potentially responsible.
[
  {
    suspected cl: <a href="https://pdfium.googlesource.com/pdfium.git/+/1b9c5c4dc41956b8c5ab17b9a882adf8a2513768">1b9c5c4dc41956b8c5ab17b9a882adf8a2513768</a>
    component: pdfium
    owner: Jun Fang
    review url: https://codereview.chromium.org/439693002
    reviewers: 'N/A'
    reason:
      Files 
      <a href="https://pdfium.googlesource.com/pdfium.git/+/1b9c5c4dc41956b8c5ab17b9a882adf8a2513768">fpdf_page_colors.cpp</a>
      <a href="https://pdfium.googlesource.com/pdfium.git/+/1b9c5c4dc41956b8c5ab17b9a882adf8a2513768">fpdf_page_pattern.cpp</a>
      are changed in this cl.

  }
]
-------------------------------------------


### mb...@chromium.org (2014-08-12)

Fixing cc list.

### bo...@foxitsoftware.com (2014-08-13)

Fixed in https://pdfium.googlesource.com/pdfium/+/87708e18c8244feecb8e58e9dc8861118061f8de

### cl...@chromium.org (2014-08-13)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-08-14)

ClusterFuzz has detected this issue as fixed in range 289356:289512.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5584270422704128

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60c0001e5d88
Crash State:
  - crash stack -
  CPDF_Color::SetValue
  CPDF_TilingPattern::~CPDF_TilingPattern
  - free stack -
  CPDF_GraphicStates::~CPDF_GraphicStates
  CPDF_StreamContentParser::~CPDF_StreamContentParser
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=288030:288271
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=289356:289512

Minimized Testcase (147.42 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96zcOcSbIzf_u84h8zoh_6TiBhkteVujOsCJtprTZQcUmcOsUicm0Ddy1ZzaHxVhjrFquLMRAhRc2SFPjXrQphuCo-nr4F0wq4IIGk3fztQUV--y9BcbMs3QTFromMqB7M41SklYemMI039l1eIecqbDW6rLMqHoJKwKT7uB2v2ZqowHgM

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### mb...@chromium.org (2014-08-19)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-09-23)

No merge required - this should be in M38 already.

### ti...@chromium.org (2014-10-07)

Congrats Atte - $3000 for this report. Notes from the panel: High quality, looks nasty though no attempt to demonstrate exploitability.

### cl...@chromium.org (2014-11-19)

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

This issue was migrated from crbug.com/chromium/402260?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080191)*
