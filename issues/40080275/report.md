# Heap-buffer-overflow in CPDF_DIBSource::GetScanline

| Field | Value |
|-------|-------|
| **Issue ID** | [40080275](https://issues.chromium.org/issues/40080275) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | at...@gmail.com |
| **Assignee** | bo...@foxitsoftware.com |
| **Created** | 2014-08-22 |
| **Bounty** | $500.00 |

## Description


Tested on:

OS: Ubuntu 12.04

Chromium: ASAN 39.0.2133.0 (Developer Build 291392)


ASAN-trace:

==15996==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x6240000ade84 at pc 0x0000005ef832 bp 0x7fffa186ec40 sp 0x7fffa186ec38
READ of size 1 at 0x6240000ade84 thread T0
    #0 0x5ef831 in _GetBits8(unsigned char const*, int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_loadimage.cpp:18
    #1 0x5f0357 in CPDF_DIBSource::GetScanline(int) const /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_loadimage.cpp:1109
    #2 0x871f29 in CFX_DIBSource::Clone(FX_RECT const*) const /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxge/dib/fx_dib_main.cpp:194
    #3 0x5d9a17 in CPDF_ImageCache::ContinueGetCachedBitmap() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_cache.cpp:331
    #4 0x5d9445 in CPDF_ImageCache::Continue(IFX_Pause*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_cache.cpp:374
    #5 0x5d9267 in CPDF_PageRenderCache::Continue(IFX_Pause*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_cache.cpp:146
    #6 0x5f40bd in CPDF_ProgressiveImageLoaderHandle::Continue(IFX_Pause*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_loadimage.cpp:1478
.
.
.

## Attachments

- [repro-file-GetBits8unsigne.pdf](attachments/repro-file-GetBits8unsigne.pdf) (application/pdf, 1.5 MB)

## Timeline

### in...@chromium.org (2014-08-22)

you rock!

### cl...@chromium.org (2014-08-22)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=6626505099575296

### in...@chromium.org (2014-08-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-08-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-23)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6626505099575296

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x624000165e84
Crash State:
  CPDF_DIBSource::GetScanline
  CFX_DIBSource::Clone
  CPDF_ImageCache::ContinueGetCachedBitmap
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=281908:281997

Minimized Testcase (1515.15 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94aNzylEzcLI3TAHbRok4YnwvlpBmQlwl_aaw1bfFcNvyZbEXCGzI00MJZbw_qdklfdsFo5CicbFwnsN9G9GyIaH7bJirzI9TFtpZ1ekHP6yxEBP48p70bzF7N1UQICoTddZ4FoJTp-WDS9nQ7ZXIssFzHAa6z7N1JUh1e2CzGSqpvjhF0



### cl...@chromium.org (2014-08-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-08-24)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-08-24)

[Empty comment from Monorail migration]

### bo...@foxitsoftware.com (2014-08-24)

depending on https://codereview.chromium.org/497733005/

### bo...@foxitsoftware.com (2014-08-25)

Fixed in https://codereview.chromium.org/497733005/

### cl...@chromium.org (2014-08-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-27)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6626505099575296

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x624000165e84
Crash State:
  CPDF_DIBSource::GetScanline
  CFX_DIBSource::Clone
  CPDF_ImageCache::ContinueGetCachedBitmap
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=281908:281997

Minimized Testcase (1515.15 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94aNzylEzcLI3TAHbRok4YnwvlpBmQlwl_aaw1bfFcNvyZbEXCGzI00MJZbw_qdklfdsFo5CicbFwnsN9G9GyIaH7bJirzI9TFtpZ1ekHP6yxEBP48p70bzF7N1UQICoTddZ4FoJTp-WDS9nQ7ZXIssFzHAa6z7N1JUh1e2CzGSqpvjhF0



### cl...@chromium.org (2014-08-27)

ClusterFuzz has detected this issue as fixed in range 291998:292010.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6626505099575296

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x624000165e84
Crash State:
  CPDF_DIBSource::GetScanline
  CFX_DIBSource::Clone
  CPDF_ImageCache::ContinueGetCachedBitmap
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=281908:281997
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=291998:292010

Minimized Testcase (1515.15 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94aNzylEzcLI3TAHbRok4YnwvlpBmQlwl_aaw1bfFcNvyZbEXCGzI00MJZbw_qdklfdsFo5CicbFwnsN9G9GyIaH7bJirzI9TFtpZ1ekHP6yxEBP48p70bzF7N1UQICoTddZ4FoJTp-WDS9nQ7ZXIssFzHAa6z7N1JUh1e2CzGSqpvjhF0

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2014-12-02)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-01-22)

$500 for this report. Panel notes: "Out of bounds read on src, not clear if destination buffer is always large enough".

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

This issue was migrated from crbug.com/chromium/406600?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080275)*
