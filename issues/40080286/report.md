# Heap-buffer-overflow in CPDF_DIBSource::TranslateScanline24bpp

| Field | Value |
|-------|-------|
| **Issue ID** | [40080286](https://issues.chromium.org/issues/40080286) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | cl...@gmail.com |
| **Assignee** | bo...@foxitsoftware.com |
| **Created** | 2014-08-24 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Very similar to 406600 and 406895 but crashing in a different function.

=================================================================  

==50349==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x61300001376a at pc 0x0000005ef5f9 bp 0x7fff34b11330 sp 0x7fff34b11328  

READ of size 1 at 0x61300001376a thread T0  

#0 0x5ef5f8 in TranslateScanline24bpp /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:950  

#1 0x5f08a9 in GetScanline /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1152  

#2 0x871f29 in Clone /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxge/dib/fx\_dib\_main.cpp:194  

#3 0x5d9a17 in ContinueGetCachedBitmap /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:331  

#4 0x5d91a5 in StartGetCachedBitmap /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:319  

#5 0x5d8e72 in StartGetCachedBitmap /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:131  

#6 0x5f3c2f in Start /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1456  

#7 0x5f462f in StartLoadImage /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1516  

#8 0x5dd838 in StartLoadDIBSource /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:371  

#9 0x5da29b in Start /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:525  

#10 0x5d0204 in ContinueSingleObject /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:350  

#10 0x5d667d in Continue /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:1175  

#11 0x4c97e0 in FPDF\_RenderPage\_Retail /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:772  

#12 0x4c9a90 in FPDF\_RenderPageBitmap /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:574  

#13 0x4c50e7 in RenderPdf /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:314  

#16 0x4c5ad9 in main /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:393  

#16 0x7f4107a887d4 (/lib64/libc.so.6+0x217d4)  

#18 0x4c441c in \_start ??:?

0x61300001376a is located 2 bytes to the right of 360-byte region [0x613000013600,0x613000013768)  

allocated by thread T0 here:  

#0 0x4a6f40 in **interceptor\_calloc ??:?  

#1 0x643170 in Create /b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec.cpp:335  

#2 0x643be8 in CreateRunLengthDecoder /b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec.cpp:440  

#3 0x5e9f1d in CreateDecoder /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:601  

#3 0x5e6044 in StartLoadDIBSource /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:344  

#4 0x5d912d in StartGetCachedBitmap /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:310  

#5 0x5d8e72 in StartGetCachedBitmap /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:131  

#6 0x5f3c2f in Start /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1456  

#7 0x5f462f in StartLoadImage /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1516  

#8 0x5dd838 in StartLoadDIBSource /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:371  

#9 0x5da29b in Start /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:525  

#10 0x5d0204 in ContinueSingleObject /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:350  

#10 0x5d667d in Continue /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:1175  

#11 0x4c97e0 in FPDF\_RenderPage\_Retail /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:772  

#12 0x4c9a90 in FPDF\_RenderPageBitmap /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:574  

#13 0x4c50e7 in RenderPdf /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:314  

#16 0x4c5ad9 in main /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:393  

#17 0x7f4107a887d4 (/lib64/libc.so.6+0x217d4)

SUMMARY: AddressSanitizer: heap-buffer-overflow ??:0 ??  

Shadow bytes around the buggy address:  

0x0c267fffa690: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c267fffa6a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c267fffa6b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c267fffa6c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c267fffa6d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x0c267fffa6e0: 00 00 00 00 00 00 00 00 00 00 00 00 00[fa]fa fa  

0x0c267fffa6f0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c267fffa700: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c267fffa710: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c267fffa720: fd fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c267fffa730: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==50349==ABORTING

**VERSION**  

Chrome Version: asan-symbolized-linux-release-291576

**REPRODUCTION CASE**  

Attached as repro.pdf

## Attachments

- [repro.pdf](attachments/repro.pdf) (application/pdf, 17.6 KB)

## Timeline

### cl...@chromium.org (2014-08-24)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5770158011318272

### in...@chromium.org (2014-08-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-24)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5770158011318272

Uploader: aarya@google.com
Job Type: Linux_asan_pdfium

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x61400001d9ea
Crash State:
  CPDF_DIBSource::TranslateScanline24bpp
  CPDF_DIBSource::GetScanline
  CFX_DIBSource::Clone
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=281908:281997

Minimized Testcase (17.58 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96R4bR0ddNUp5fUYSHuMGBz30WNjgxv7JwKSwwwS2P4qXfAXEO6b16ykGlVc8E8w6qoUv-3ZI54wEgY-1B4ehCinVkCGBaLfULUD-lte3G7pmaKdJH9wQpE3m-KPQheetDkBruDs5zqIrYMVE8iOnhuJY0326bglvRv4Jlz0OD2mIsm35g



### bo...@foxitsoftware.com (2014-08-25)

depending on patch at https://codereview.chromium.org/504673002/

### bo...@foxitsoftware.com (2014-08-25)

Fixed in https://codereview.chromium.org/504673002/

### cl...@chromium.org (2014-08-26)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-08-26)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5770158011318272

Uploader: aarya@google.com
Job Type: Linux_asan_pdfium

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x61400001d9ea
Crash State:
  CPDF_DIBSource::TranslateScanline24bpp
  CPDF_DIBSource::GetScanline
  CFX_DIBSource::Clone
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=281908:281997

Minimized Testcase (17.58 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96R4bR0ddNUp5fUYSHuMGBz30WNjgxv7JwKSwwwS2P4qXfAXEO6b16ykGlVc8E8w6qoUv-3ZI54wEgY-1B4ehCinVkCGBaLfULUD-lte3G7pmaKdJH9wQpE3m-KPQheetDkBruDs5zqIrYMVE8iOnhuJY0326bglvRv4Jlz0OD2mIsm35g



### cl...@chromium.org (2014-08-27)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5770158011318272

Uploader: aarya@google.com
Job Type: Linux_asan_pdfium

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x61400001d9ea
Crash State:
  CPDF_DIBSource::TranslateScanline24bpp
  CPDF_DIBSource::GetScanline
  CFX_DIBSource::Clone
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=281908:281997

Minimized Testcase (17.58 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96R4bR0ddNUp5fUYSHuMGBz30WNjgxv7JwKSwwwS2P4qXfAXEO6b16ykGlVc8E8w6qoUv-3ZI54wEgY-1B4ehCinVkCGBaLfULUD-lte3G7pmaKdJH9wQpE3m-KPQheetDkBruDs5zqIrYMVE8iOnhuJY0326bglvRv4Jlz0OD2mIsm35g



### cl...@chromium.org (2014-08-27)

ClusterFuzz has detected this issue as fixed in range 291998:292010.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5770158011318272

Uploader: aarya@google.com
Job Type: Linux_asan_pdfium

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x61400001d9ea
Crash State:
  CPDF_DIBSource::TranslateScanline24bpp
  CPDF_DIBSource::GetScanline
  CFX_DIBSource::Clone
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=281908:281997
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=291998:292010

Minimized Testcase (17.58 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96R4bR0ddNUp5fUYSHuMGBz30WNjgxv7JwKSwwwS2P4qXfAXEO6b16ykGlVc8E8w6qoUv-3ZI54wEgY-1B4ehCinVkCGBaLfULUD-lte3G7pmaKdJH9wQpE3m-KPQheetDkBruDs5zqIrYMVE8iOnhuJY0326bglvRv4Jlz0OD2mIsm35g

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ti...@chromium.org (2014-09-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-02)

Bulk update: removing view restriction from closed bugs.

### in...@chromium.org (2015-01-13)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-16)

Removing reward-topanel as report collided with #3. 

### mb...@chromium.org (2015-07-16)

c#3 was an upload from the test case in this report, right? Re-adding reward-topanel.

### in...@chromium.org (2015-07-16)

Yes looks like it, has similar testcase name.

### ti...@google.com (2015-10-09)

Found this when doing a sweep for old issues. $1000 for this report.

### ti...@google.com (2015-10-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-29)

Payment is on its way - should arrive in ~7 days. Thanks again for your report!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/406908?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080286)*
