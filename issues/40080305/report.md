# Heap-buffer-overflow in CPDF_LabCS::TranslateImageLine

| Field | Value |
|-------|-------|
| **Issue ID** | [40080305](https://issues.chromium.org/issues/40080305) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | cl...@gmail.com |
| **Assignee** | bo...@foxitsoftware.com |
| **Created** | 2014-08-27 |
| **Bounty** | $3,000.00 |

## Description

# **VULNERABILITY DETAILS**

==54031==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x6160000179ee at pc 0x0000005671ab bp 0x7ffff7330030 sp 0x7ffff7330028  

WRITE of size 1 at 0x6160000179ee thread T0  

#0 0x5671aa in TranslateImageLine /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_page/fpdf\_page\_colors.cpp:514  

#1 0x5f003c in TranslateScanline24bpp /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:997 (discriminator 4)  

#2 0x5f1534 in GetScanline /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1181  

#2 0x872ca9 in Clone /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxge/dib/fx\_dib\_main.cpp:194  

#3 0x5da567 in ContinueGetCachedBitmap /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:331  

#4 0x5d9cf5 in StartGetCachedBitmap /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:319  

#16 0x5d99c2 in StartGetCachedBitmap /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:131  

#17 0x5f48ef in Start /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1485  

#18 0x5f52ef in StartLoadImage /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1545  

#19 0x5de388 in StartLoadDIBSource /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:371  

#20 0x5dadeb in Start /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:525  

#21 0x5d0d54 in ContinueSingleObject /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:350  

#22 0x5d71cd in Continue /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:1175  

#23 0x4c9860 in FPDF\_RenderPage\_Retail /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:772  

#24 0x4c9b10 in FPDF\_RenderPageBitmap /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:574  

#25 0x4c5135 in RenderPdf /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:324  

#26 0x4c5b59 in main /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:406  

#17 0x7f0534eb17d4 (/lib64/libc.so.6+0x217d4)  

#28 0x4c441c in \_start ??:?

0x6160000179ee is located 0 bytes to the right of 622-byte region [0x616000017780,0x6160000179ee)  

allocated by thread T0 here:  

#0 0x4a6f40 in **interceptor\_calloc ??:?  

#1 0x5ec773 in ContinueToLoadMask /b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:278  

#2 0x5e6c53 in StartLoadDIBSource /b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:357  

#15 0x5d9c7d in StartGetCachedBitmap /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:310  

#16 0x5d99c2 in StartGetCachedBitmap /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:131  

#17 0x5f48ef in Start /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1485  

#18 0x5f52ef in StartLoadImage /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1545  

#19 0x5de388 in StartLoadDIBSource /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:371  

#20 0x5dadeb in Start /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:525  

#21 0x5d0d54 in ContinueSingleObject /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:350  

#22 0x5d71cd in Continue /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:1175  

#23 0x4c9860 in FPDF\_RenderPage\_Retail /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:772  

#24 0x4c9b10 in FPDF\_RenderPageBitmap /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:574  

#25 0x4c5135 in RenderPdf /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:324  

#26 0x4c5b59 in main /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:406  

#15 0x7f0534eb17d4 (/lib64/libc.so.6+0x217d4)

SUMMARY: AddressSanitizer: heap-buffer-overflow ??:0 ??  

Shadow bytes around the buggy address:  

0x0c2c7fffaee0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c2c7fffaef0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c2c7fffaf00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c2c7fffaf10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c2c7fffaf20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x0c2c7fffaf30: 00 00 00 00 00 00 00 00 00 00 00 00 00[06]fa fa  

0x0c2c7fffaf40: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c2c7fffaf50: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2c7fffaf60: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2c7fffaf70: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2c7fffaf80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==54031==ABORTING

**VERSION**  

Chrome Version: asan-symbolized-linux-release-292094

**REPRODUCTION CASE**  

attached in repro.pdf

## Attachments

- [repro.pdf](attachments/repro.pdf) (application/pdf, 89.6 KB)

## Timeline

### in...@chromium.org (2014-08-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-27)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=6625920178716672

### in...@chromium.org (2014-08-27)

Cloudfuzzer@, in the future, can you please specify whether you are using chrome or pdfium_test :)

### cl...@chromium.org (2014-08-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-27)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6625920178716672

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow WRITE 1
Crash Address: 0x61600004e2ee
Crash State:
  CPDF_LabCS::TranslateImageLine
  CPDF_DIBSource::TranslateScanline24bpp
  CPDF_DIBSource::GetScanline
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=291998:292010

Minimized Testcase (89.62 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96Fx9c4JBULKFDa7CnzE5QbjmYNovNRC106DgkSSeUbYopffXMCq3Wl-PsAog1EzBMweDexgvdYuaQtNdUMSpnxAgyll7_KMJQSAon_jAxRkfRaawOqwNMfheKp-Sv4vrfvqkycashRX4Ixk9_HroQHl0-CswhhlXK1haCFUaqTzMIX1VQ



### bo...@foxitsoftware.com (2014-08-27)

[Empty comment from Monorail migration]

### bo...@foxitsoftware.com (2014-08-27)

Fixed in https://pdfium.googlesource.com/pdfium/+/405478d3870693fbaf8f17758a760abfd276b2ee

### cl...@chromium.org (2014-08-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-30)

ClusterFuzz has detected this issue as fixed in range 292300:292693.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6625920178716672

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow WRITE 1
Crash Address: 0x61600004e2ee
Crash State:
  CPDF_LabCS::TranslateImageLine
  CPDF_DIBSource::TranslateScanline24bpp
  CPDF_DIBSource::GetScanline
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=291998:292010
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=292300:292693

Minimized Testcase (89.62 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96Fx9c4JBULKFDa7CnzE5QbjmYNovNRC106DgkSSeUbYopffXMCq3Wl-PsAog1EzBMweDexgvdYuaQtNdUMSpnxAgyll7_KMJQSAon_jAxRkfRaawOqwNMfheKp-Sv4vrfvqkycashRX4Ixk9_HroQHl0-CswhhlXK1haCFUaqTzMIX1VQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ti...@chromium.org (2014-10-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-03)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-01-22)

$3000 here as well. 

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-07)

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

This issue was migrated from crbug.com/chromium/408141?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/408147, crbug.com/chromium/408148, crbug.com/chromium/408150, crbug.com/chromium/408157, crbug.com/chromium/408163]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080305)*
