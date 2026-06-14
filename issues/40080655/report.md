# UNKNOWN in opj_read_bytes_LE

| Field | Value |
|-------|-------|
| **Issue ID** | [40080655](https://issues.chromium.org/issues/40080655) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | at...@gmail.com |
| **Assignee** | bo...@foxitsoftware.com |
| **Created** | 2014-10-16 |
| **Bounty** | $1,000.00 |

## Description




Tested on:

OS: Ubuntu 12.04

Chromium: ASAN 40.0.2192.0 (Developer Build)
Revision:	27e78ad7c43bd01d607d414552cffdfe92e9dece-refs/heads/master@{#299905}

ASAN-trace: 

=================================================================
==18383==ERROR: AddressSanitizer: SEGV on unknown address 0x62210000d91c (pc 0x7f2f31ca4896 bp 0x7fffd1126bd0 sp 0x7fffd1126bb0 T0)
    #0 0x7f2f31ca4895 in opj_read_bytes_LE /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/src/../libopenjpeg20/cio.c:87:3
    #1 0x7f2f31cb2af6 in opj_jp2_read_boxhdr_char /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/src/../libopenjpeg20/jp2.c:2237:2
    #2 0x7f2f31cab495 in opj_jp2_read_jp2h /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/src/../libopenjpeg20/jp2.c:2184:9
    #3 0x7f2f31cb1ef4 in opj_jp2_read_header_procedure /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/src/../libopenjpeg20/jp2.c:1874:10
    #4 0x7f2f31cb05f1 in opj_jp2_exec /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/src/../libopenjpeg20/jp2.c:1925:26
    #5 0x7f2f31cb0de0 in opj_jp2_read_header /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/src/../libopenjpeg20/jp2.c:2306:8
    #6 0x7f2f31ca28ce in CJPX_Decoder::Init(unsigned char const*, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxcodec/codec/fx_codec_jpx_opj.cpp:601:10
    #7 0x7f2f31ca42f0 in CCodec_JpxModule::CreateDecoder(unsigned char const*, unsigned int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxcodec/codec/fx_codec_jpx_opj.cpp:760:10
.
.
.


## Attachments

- [surku-17.pdf](attachments/surku-17.pdf) (application/pdf, 264.6 KB)

## Timeline

### cl...@chromium.org (2014-10-16)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5667037064986624

### cl...@chromium.org (2014-10-16)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5667037064986624

Uploader: mdempsky@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x62210000911c
Crash State:
  opj_read_bytes_LE
  opj_jp2_read_jp2h
  opj_jp2_read_header_procedure
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=299683:299856

Minimized Testcase (264.60 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94ndDzCa8lkrWYj1RyhaylQp4SdWLeMa33gFAVJl2iUxrfvNCHKPdlqHcyTWsV_EPzq9LCspTFnTuCV1_Cwj8YE0t0j9Y7OuMq99BnlTFsZ--8LMiJTtYx-xwP54TIBIyFNG3pAsV_btu-nT6q8aK5mIKKlg22GmY4hon78uijuTfFS_sI



### ts...@chromium.org (2014-10-16)

Regression range indicates the pdfium roll that introduced the libopenjpeg roll at chromium r299722.

### md...@chromium.org (2014-10-16)

[Empty comment from Monorail migration]

### ts...@chromium.org (2014-10-16)

Looks like this was fixed locally in pdfium, but never upstreamed.  See the diff of jp2.c at https://codereview.chromium.org/589243004, where we lost this snippet of code:

 2228                 //BUGID:0055999	
 2229                 //test file: fuzz-signal_sigsegv_6b88de_1123_2509.pdf	
 2230                 if (box.length < l_box_size) return OPJ_FALSE;	

Bo, can you submit this change up to the libopenjpeg folks?

### bo...@foxitsoftware.com (2014-10-16)

@antonin, can you look at this issue? We fixed this before, but lost during the latest upgrade. Please see comments in #5.

Can you merge this upstream? Thanks.

### cl...@chromium.org (2014-10-17)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### an...@gmail.com (2014-10-21)

@bo: could you cc m.darbois ?

### in...@chromium.org (2014-10-21)

[Empty comment from Monorail migration]

### bo...@foxitsoftware.com (2014-10-21)

@tsepez, @m.darbois, seems this regression has been fixed in the latest openjpeg upgrade of r2908

### bo...@foxitsoftware.com (2014-10-21)

Fixed in https://pdfium.googlesource.com/pdfium/+/767aebbef641a89498deebc29369a078207b4dcc

### cl...@chromium.org (2014-10-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-22)

ClusterFuzz has detected this issue as fixed in range 300581:300635.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5667037064986624

Uploader: mdempsky@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x62210000911c
Crash State:
  opj_read_bytes_LE
  opj_jp2_read_jp2h
  opj_jp2_read_header_procedure
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=299683:299856
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=300581:300635

Minimized Testcase (264.60 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94ndDzCa8lkrWYj1RyhaylQp4SdWLeMa33gFAVJl2iUxrfvNCHKPdlqHcyTWsV_EPzq9LCspTFnTuCV1_Cwj8YE0t0j9Y7OuMq99BnlTFsZ--8LMiJTtYx-xwP54TIBIyFNG3pAsV_btu-nT6q8aK5mIKKlg22GmY4hon78uijuTfFS_sI

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2014-11-05)

[Empty comment from Monorail migration]

### ti...@google.com (2015-01-22)

$1000 reward for this report. Panel notes: "Although fixed upstream in openjpeg, chromium didn't have it yet".

### cl...@chromium.org (2015-01-27)

Bulk update: removing view restriction from closed bugs.

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

This issue was migrated from crbug.com/chromium/424331?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080655)*
