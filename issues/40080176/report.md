# Heap-use-after-free in CPDF_IndexedCS::~CPDF_IndexedCS

| Field | Value |
|-------|-------|
| **Issue ID** | [40080176](https://issues.chromium.org/issues/40080176) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | at...@gmail.com |
| **Assignee** | bo...@foxitsoftware.com |
| **Created** | 2014-08-07 |
| **Bounty** | $3,000.00 |

## Description


Tested on:

OS: Ubuntu 12.04

Chromium: ASAN 38.0.2114.0 (Developer Build 287379) 


Repro-file as an attachment. The repro-file is little needy so I made a small html-file(run.html) that, at least for me, triggers the crash easily.


ASAN-report:

==11286==ERROR: AddressSanitizer: heap-use-after-free on address 0x60700005dd48 at pc 0x7fa1d4a098fc bp 0x7fffef261060 sp 0x7fffef261058
READ of size 8 at 0x60700005dd48 thread T0 (chrome)
    #0 0x7fa1d4a098fb in CPDF_IndexedCS::~CPDF_IndexedCS() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_colors.cpp:759
    #1 0x7fa1d4a0994a in CPDF_IndexedCS::~CPDF_IndexedCS() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_colors.cpp:753
    #2 0x7fa1d4a0ebd9 in CPDF_DocPageData::Clear(int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_doc.cpp:202
    #3 0x7fa1d4a1163a in CPDF_DocPageData::~CPDF_DocPageData() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_doc.cpp:148
    #4 0x7fa1d4a0e59a in CPDF_PageModule::ReleaseDoc(CPDF_Document*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_doc.cpp:70
    #5 0x7fa1d4a3fc2b in CPDF_Document::~CPDF_Document() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_document.cpp:102
.
.
.
0x60700005dd48 is located 24 bytes inside of 80-byte region [0x60700005dd30,0x60700005dd80)
freed by thread T0 (chrome) here:
    #0 0x7fa1e802cebb in free ??:0
    #1 0x7fa1d4a0ebd9 in CPDF_DocPageData::Clear(int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_doc.cpp:202
    #2 0x7fa1d4a1163a in CPDF_DocPageData::~CPDF_DocPageData() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_doc.cpp:148
    #3 0x7fa1d4a0e59a in CPDF_PageModule::ReleaseDoc(CPDF_Document*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_doc.cpp:70
    #4 0x7fa1d4a3fc2b in CPDF_Document::~CPDF_Document() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_document.cpp:102
    #5 0x7fa1d4a51a59 in CPDF_Parser::CloseParser(int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:73
.
.
.


## Attachments

- [run.html](attachments/run.html) (text/html, 273 B)
- [repro-file.pdf](attachments/repro-file.pdf) (application/pdf, 192.0 KB)

## Timeline

### cl...@chromium.org (2014-08-07)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5363850184491008

### in...@chromium.org (2014-08-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-07)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5363850184491008

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60d00007a2a8
Crash State:
  - crash stack -
  CPDF_IndexedCS::~CPDF_IndexedCS
  CPDF_IndexedCS::~CPDF_IndexedCS
  - free stack -
  CPDF_DocPageData::Clear
  CPDF_DocPageData::~CPDF_DocPageData
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=287661:287842

Minimized Testcase (163.38 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94oIck7BipE7mkbstlhrpM2C-OLvxNB-JHWCLVzwVmjJnLq_-MtWf7wjWuCXn83EcHtOGOHTGHWb_7W01XdVrbtwOsmS36mXajJE6GtoURMUoYEIHU9Mt8hze5W2jNCuPLIFiszH-NgxjBMPbgsW_TCHlwxmY1Iu972dUbsJ9vC-x5MXmo



### cl...@chromium.org (2014-08-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-09)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-08-09)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5363850184491008

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60d00007a2a8
Crash State:
  - crash stack -
  CPDF_IndexedCS::~CPDF_IndexedCS
  CPDF_IndexedCS::~CPDF_IndexedCS
  - free stack -
  CPDF_DocPageData::Clear
  CPDF_DocPageData::~CPDF_DocPageData
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=287661:287842

Minimized Testcase (163.38 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94oIck7BipE7mkbstlhrpM2C-OLvxNB-JHWCLVzwVmjJnLq_-MtWf7wjWuCXn83EcHtOGOHTGHWb_7W01XdVrbtwOsmS36mXajJE6GtoURMUoYEIHU9Mt8hze5W2jNCuPLIFiszH-NgxjBMPbgsW_TCHlwxmY1Iu972dUbsJ9vC-x5MXmo



### bo...@foxitsoftware.com (2014-08-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-18)

[Empty comment from Monorail migration]

### bo...@foxitsoftware.com (2014-08-18)

Fixed in https://pdfium.googlesource.com/pdfium/+/489d483090167a45b26cf5f4ec3304dc1e1cc064

### bu...@chromium.org (2014-08-18)

Is there a merge required here?

### cl...@chromium.org (2014-08-18)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### bu...@chromium.org (2014-08-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6e684515500e6470dd4c4fa3499414bc4a8d9a97

commit 6e684515500e6470dd4c4fa3499414bc4a8d9a97
Author: thakis@chromium.org <thakis@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Mon Aug 18 19:45:47 2014

Roll pdfium. This brings in:

635e82e  Fix tzHour usage on systems where char is unsigned.
489d483  No need to release m_pBaseCS in CPDF_IndexedCS and CPDF_PatternCS
d726307  Fix buffer size offset error in PNG_Predictor
368ed46  Add FX_OVERRIDE and use it for virtual functions of FX_FINAL classes.

BUG=393602,401372,395832
TBR=tsepez@chromium.org

Review URL: https://codereview.chromium.org/485803002

Cr-Commit-Position: refs/heads/master@{#290339}
git-svn-id: svn://svn.chromium.org/chrome/trunk/src@290339 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-08-18)

------------------------------------------------------------------
r290339 | thakis@chromium.org | 2014-08-18T19:45:47.193913Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/DEPS?r1=290339&r2=290338&pathrev=290339

Roll pdfium. This brings in:

635e82e  Fix tzHour usage on systems where char is unsigned.
489d483  No need to release m_pBaseCS in CPDF_IndexedCS and CPDF_PatternCS
d726307  Fix buffer size offset error in PNG_Predictor
368ed46  Add FX_OVERRIDE and use it for virtual functions of FX_FINAL classes.

BUG=393602,401372,395832
TBR=tsepez@chromium.org

Review URL: https://codereview.chromium.org/485803002
-----------------------------------------------------------------

### in...@chromium.org (2014-08-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-08-23)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-09-23)

Matthew - Merge Requested for M38 (branch 2125)

### [Deleted User] (2014-09-24)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-09-24)

Bo - please merge to M38 / branch 2125

### bo...@foxitsoftware.com (2014-09-25)

Merge done

### ma...@google.com (2014-09-26)

Please process the merge approval if you haven't.

### bo...@foxitsoftware.com (2014-09-26)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-09-29)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-10-07)

Atte - $3000 for this one as well!

### cl...@chromium.org (2014-11-24)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2014-12-08)

Payment in progress

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-12-16)

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

This issue was migrated from crbug.com/chromium/401372?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/406664]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080176)*
