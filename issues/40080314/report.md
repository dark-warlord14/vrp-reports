# Heap-use-after-free in CPDF_ShadingObject::~CPDF_ShadingObject

| Field | Value |
|-------|-------|
| **Issue ID** | [40080314](https://issues.chromium.org/issues/40080314) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | cl...@gmail.com |
| **Assignee** | bo...@foxitsoftware.com |
| **Created** | 2014-08-27 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

==22021==ERROR: AddressSanitizer: heap-use-after-free on address 0x60e000009a88 at pc 0x00000055fad2 bp 0x7fff36992850 sp 0x7fff36992848  

READ of size 8 at 0x60e000009a88 thread T0  

#0 0x55fad1 in ~CPDF\_ShadingObject /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_page/fpdf\_page.cpp:610 (discriminator 1)  

#1 0x55fafa in ~CPDF\_ShadingObject /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_page/fpdf\_page.cpp:608  

#2 0x560a37 in ~CPDF\_PageObjects /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_page/fpdf\_page.cpp:700  

#3 0x5983e5 in ~CPDF\_TilingPattern /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_page/fpdf\_page\_pattern.cpp:43 (discriminator 1)  

#4 0x59845a in ~CPDF\_TilingPattern /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_page/fpdf\_page\_pattern.cpp:41  

#5 0x56e710 in Clear /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_page/fpdf\_page\_doc.cpp:164 (discriminator 1)  

#6 0x571459 in ~CPDF\_DocPageData /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_page/fpdf\_page\_doc.cpp:149  

#7 0x56e45a in ReleaseDoc /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_page/fpdf\_page\_doc.cpp:70 (discriminator 1)  

#8 0x59f8c8 in ~CPDF\_Document /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_parser/fpdf\_parser\_document.cpp:102  

#9 0x5a95e9 in CloseParser /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_parser/fpdf\_parser\_parser.cpp:74 (discriminator 1)  

#10 0x5a942e in ~CPDF\_Parser /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_parser/fpdf\_parser\_parser.cpp:59  

#11 0x4c9c20 in FPDF\_CloseDocument /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:598 (discriminator 1)  

#12 0x4c521d in RenderPdf /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:359  

#26 0x4c5b59 in main /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:406  

#14 0x7f89dc8707d4 (/lib64/libc.so.6+0x217d4)  

#28 0x4c441c in \_start ??:?

0x60e000009a88 is located 72 bytes inside of 152-byte region [0x60e000009a40,0x60e000009ad8)  

freed by thread T0 here:  

#0 0x4a6b6b in **interceptor\_free ??:?  

#5 0x56e710 in Clear /b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_page/fpdf\_page\_doc.cpp:164 (discriminator 1)  

#6 0x571459 in ~CPDF\_DocPageData /b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_page/fpdf\_page\_doc.cpp:149  

#7 0x56e45a in ReleaseDoc /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_page/fpdf\_page\_doc.cpp:70 (discriminator 1)  

#8 0x59f8c8 in ~CPDF\_Document /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_parser/fpdf\_parser\_document.cpp:102  

#9 0x5a95e9 in CloseParser /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_parser/fpdf\_parser\_parser.cpp:74 (discriminator 1)  

#10 0x5a942e in ~CPDF\_Parser /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_parser/fpdf\_parser\_parser.cpp:59  

#11 0x4c9c20 in FPDF\_CloseDocument /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:598 (discriminator 1)  

#12 0x4c521d in RenderPdf /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:359  

#26 0x4c5b59 in main /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:406  

#10 0x7f89dc8707d4 (/lib64/libc.so.6+0x217d4)

previously allocated by thread T0 here:  

#0 0x4a6deb in **interceptor\_malloc ??:?  

#1 0x57036d in GetPattern /b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_page/fpdf\_page\_doc.cpp:476  

#2 0x58b0c0 in FindPattern /b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_page/fpdf\_page\_parser.cpp:1352  

#3 0x58b57d in Handle\_ShadeFill /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_page/fpdf\_page\_parser.cpp:1212  

#4 0x58419d in OnOperator /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_page/fpdf\_page\_parser.cpp:380 (discriminator 4)  

#5 0x58eac3 in Parse /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_page/fpdf\_page\_parser\_old.cpp:52  

#6 0x59684a in Continue /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_page/fpdf\_page\_parser\_old.cpp:1082  

#7 0x560c0b in ContinueParse /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_page/fpdf\_page.cpp:708  

#8 0x598762 in Load /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_page/fpdf\_page\_pattern.cpp:64  

#9 0x5fbd67 in DrawTilingPattern /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_pattern.cpp:924  

#17 0x5fe4b0 in ProcessPathPattern /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_pattern.cpp:1107  

#18 0x5d1d3f in ProcessPath /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:533  

#19 0x5d0981 in ProcessObjectNoClip /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:423  

#20 0x5d0d83 in ContinueSingleObject /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:365  

#22 0x5d71cd in Continue /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:1175  

#23 0x4c9860 in FPDF\_RenderPage\_Retail /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:772  

#24 0x4c9b10 in FPDF\_RenderPageBitmap /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:574  

#25 0x4c5135 in RenderPdf /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:324  

#26 0x4c5b59 in main /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:406  

#19 0x7f89dc8707d4 (/lib64/libc.so.6+0x217d4)

SUMMARY: AddressSanitizer: heap-use-after-free ??:0 ??  

Shadow bytes around the buggy address:  

0x0c1c7fff9300: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa  

0x0c1c7fff9310: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c1c7fff9320: fd fd fd fa fa fa fa fa fa fa fa fa fd fd fd fd  

0x0c1c7fff9330: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x0c1c7fff9340: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

=>0x0c1c7fff9350: fd[fd]fd fd fd fd fd fd fd fd fd fa fa fa fa fa  

0x0c1c7fff9360: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c1c7fff9370: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa  

0x0c1c7fff9380: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c1c7fff9390: fd fd fd fa fa fa fa fa fa fa fa fa fd fd fd fd  

0x0c1c7fff93a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Heap right redzone: fb  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack partial redzone: f4  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

ASan internal: fe  

==22021==ABORTING

**VERSION**  

Chrome Version: asan-symbolized-linux-release-292094

**REPRODUCTION CASE**  

attached in repro.pdf

## Attachments

- [repro.pdf](attachments/repro.pdf) (application/pdf, 37.4 KB)

## Timeline

### in...@chromium.org (2014-08-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-27)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5763499805376512

### cl...@chromium.org (2014-08-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-27)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5763499805376512

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6110000b5d88
Crash State:
  CPDF_ShadingObject::~CPDF_ShadingObject
  CPDF_PageObjects::~CPDF_PageObjects
  CPDF_TilingPattern::~CPDF_TilingPattern
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=281908:281997

Minimized Testcase (37.40 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94u-iJr_h0d5Xhr21gR6CFZtnP004UMHtFu8UJuxyV-w5YDRK5TZ2rTw5Uexkqol61BZ8MsYVR0rrfb-kYKUmM_OfJ2GykVuq6mvPgYJdjVSS9_mRijIxPWoN_rwjdkKTrrF6lry66PPd50AEL5Pp-VNozsaQcu4XaxT2ULZmf9AvbtiEI



### bo...@foxitsoftware.com (2014-08-28)

[Empty comment from Monorail migration]

### bo...@foxitsoftware.com (2014-08-28)

Depending on CL: https://codereview.chromium.org/513063003/

### bo...@foxitsoftware.com (2014-08-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-30)

ClusterFuzz has detected this issue as fixed in range 292300:292693.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5763499805376512

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6110000b5d88
Crash State:
  CPDF_ShadingObject::~CPDF_ShadingObject
  CPDF_PageObjects::~CPDF_PageObjects
  CPDF_TilingPattern::~CPDF_TilingPattern
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=281908:281997
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=292300:292693

Minimized Testcase (37.40 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94u-iJr_h0d5Xhr21gR6CFZtnP004UMHtFu8UJuxyV-w5YDRK5TZ2rTw5Uexkqol61BZ8MsYVR0rrfb-kYKUmM_OfJ2GykVuq6mvPgYJdjVSS9_mRijIxPWoN_rwjdkKTrrF6lry66PPd50AEL5Pp-VNozsaQcu4XaxT2ULZmf9AvbtiEI

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2014-12-05)

Bulk update: removing view restriction from closed bugs.

### in...@chromium.org (2015-01-13)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-09)

Congrats - $1000 for this bug.

Notes from reward panel: "appears to be very limited control between use and free"/

### ti...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### ti...@google.com (2015-06-03)

Processing via our *new* e-payment system should only take a 7-10 days and the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/408164?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080314)*
