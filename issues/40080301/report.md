# Heap-buffer-overflow in opj_t2_read_packet_header

| Field | Value |
|-------|-------|
| **Issue ID** | [40080301](https://issues.chromium.org/issues/40080301) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | at...@gmail.com |
| **Assignee** | bo...@foxitsoftware.com |
| **Created** | 2014-08-27 |
| **Bounty** | $1,000.00 |

## Description



Tested on:

OS: Ubuntu 12.04

Chromium: 39.0.2137.0 (Developer Build bce0267e0d1a) 


ASAN-trace:

Error : expected SOP marker
=================================================================
==16208==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x63300008b3ce at pc 0x0000007c8e17 bp 0x7fff74299870 sp 0x7fff74299868
READ of size 1 at 0x63300008b3ce thread T0
    #0 0x7c8e16 in opj_t2_read_packet_header /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/src/../libopenjpeg20/t2.c:1050
    #1 0x7c6edb in opj_t2_decode_packet /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/src/../libopenjpeg20/t2.c:513
    #2 0x7c68b5 in opj_t2_decode_packets /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/src/../libopenjpeg20/t2.c:399
    #3 0x770895 in opj_tcd_t2_decode /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/src/../libopenjpeg20/tcd.c:1487
    #4 0x7706dc in opj_tcd_decode_tile /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/src/../libopenjpeg20/tcd.c:1230
    #5 0x740b7f in opj_j2k_decode_tile /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/src/../libopenjpeg20/j2k.c:7661
    #6 0x7516f0 in opj_j2k_decode_tiles /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/src/../libopenjpeg20/j2k.c:9177
    #7 0x73d701 in opj_j2k_exec /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/src/../libopenjpeg20/j2k.c:7048
    #8 0x7457e0 in opj_j2k_decode /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/src/../libopenjpeg20/j2k.c:9368
    #9 0x6651a9 in opj_jp2_decode /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/src/../libopenjpeg20/jp2.c:1332
    #10 0x65a949 in CJPX_Decoder::Init(unsigned char const*, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxcodec/codec/fx_codec_jpx_opj.cpp:630
    #11 0x65bfaf in CCodec_JpxModule::CreateDecoder(unsigned char const*, unsigned int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxcodec/codec/fx_codec_jpx_opj.cpp:770
.
.
.


## Attachments

- [radamsa-0.2.3-1.pdf](attachments/radamsa-0.2.3-1.pdf) (application/pdf, 240.3 KB)
- [4c8a2de6e30405d3e98f3aa06d2ce828cf7921b1.pdf](attachments/4c8a2de6e30405d3e98f3aa06d2ce828cf7921b1.pdf) (application/pdf, 7.5 KB)
- [repro-file.pdf](attachments/repro-file.pdf) (application/pdf, 7.5 KB)
- [extractjp2.py](attachments/extractjp2.py) (text/plain, 627 B)
- [0.jp2](attachments/0.jp2) (application/octet-stream, 107.9 KB)

## Timeline

### in...@chromium.org (2014-08-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-27)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5638134541844480

### cl...@chromium.org (2014-08-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-27)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5638134541844480

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x63300008b3ce
Crash State:
  opj_t2_read_packet_header
  opj_t2_decode_packets
  opj_tcd_decode_tile
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=281908:281997

Minimized Testcase (240.29 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95mn1ytrxoo2vHsBoVk0J0t8iIEkw_AI2Kcav6-_uZjUtsSpUmRw-jgsF09LhKAtxSG_21SwTNeR18JoW84XDAHDvaFEhbbER_FgJJnE5HxMU6j01uZK5XdrBgRikYmcTZJFLM38-1UvbitDCid4ERBKlpj82MY1g4w0ly1ZfibO_YQsC8



### cl...@chromium.org (2014-08-27)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5638134541844480

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x63300008b3ce
Crash State:
  opj_t2_read_packet_header
  opj_t2_decode_packets
  opj_tcd_decode_tile
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=281908:281997

Minimized Testcase (240.29 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95mn1ytrxoo2vHsBoVk0J0t8iIEkw_AI2Kcav6-_uZjUtsSpUmRw-jgsF09LhKAtxSG_21SwTNeR18JoW84XDAHDvaFEhbbER_FgJJnE5HxMU6j01uZK5XdrBgRikYmcTZJFLM38-1UvbitDCid4ERBKlpj82MY1g4w0ly1ZfibO_YQsC8



### wf...@chromium.org (2014-08-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-30)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-09-06)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### bo...@foxitsoftware.com (2014-09-09)

@attekett, can you upload the original, un-corrupted file?

### at...@gmail.com (2014-09-09)

I couldn't find the original file for that repro-file, but here is a new repro-file and the original file for it.

### ts...@chromium.org (2014-09-11)

[Empty comment from Monorail migration]

### ts...@chromium.org (2014-09-11)

Also see the analysis in https://code.google.com/p/chromium/issues/detail?id=413375

### ts...@chromium.org (2014-09-11)

[Empty comment from Monorail migration]

### ts...@chromium.org (2014-09-11)

[Empty comment from Monorail migration]

### cl...@gmail.com (2014-09-11)

Pretty sure this issue is different to the one in 413375. For the following reasons:

- Crash line and function are different.
- The issue in 413375 should only affect 32-bit builds, while this was found using a 64-bit build.
- This issue looks like a read off-by-one, while https://crbug.com/chromium/413375 looks like a write well past an allocated buffer 

### ts...@chromium.org (2014-09-11)

@cloudfuzzer - fair enough.
@bo - can you tell if these are separate issues?  Thanks.

### bo...@foxitsoftware.com (2014-09-11)

I don't have access to 413375. Can you give me that?

### in...@chromium.org (2014-09-11)

[Empty comment from Monorail migration]

### ts...@chromium.org (2014-09-12)

@bo - FYI, looks like inferno just added you to 413375

### bo...@foxitsoftware.com (2014-09-12)

@tsepez, this one and some other open jpeg related issues are purely due to the openjpeg. When part of the stream is corrupted, the buffer size, decoding process causes Asan crash.

I would think open jpeg group https://code.google.com/p/openjpeg/ should have deeper understanding of these bugs, since it's purely from the corruption of decoded stream. Would it possible to report these bugs to them?

### in...@chromium.org (2014-09-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-09-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-09-17)

+cc Libopenjpeg devs.

Antonin, Mathieu - can you please take a look at these libopenjpeg high severity security vulnerabilities asap. Feel free to port them to libopenjpeg bug tracker provided you can restrict view them [should not be open to public].

### an...@gmail.com (2014-09-19)

Could you extract the JP2/JPX codestream from the pdf file and send it to us ? Or give us an easy way to do so ? I tried mupdf but no success.

$ mutool extract ~/data/opj/issues/issue389/4c8a2de6e30405d3e98f3aa06d2ce828cf7921b1.pdf
error: object out of range (0 0 R); xref size 15
error: cannot load object (0 0 R) into cache
uncaught exception: cannot load object (0 0 R) into cache

And could you add m.darbois_at_gmail.com in cc of all the issues you sent us so that Matthieu from our CoreTeam can access them ?

Thanks

### in...@chromium.org (2014-09-19)

+cc m.darbois

Bo, Jun, what is the easy way to extract the image bits from pdf. Can you please attach them to these 11 bugs.

### ma...@gmail.com (2014-09-19)

antonin, I updated openjpeg wiki to describe what to do with corrupted PDF:

http://code.google.com/p/openjpeg/wiki/TestSuiteDocumentation#pdf_extraction_(difficult)

This is a small tool I wrote during my previous bug hunting work. It is not working for the attached PDF file. I'll try to see if I can get it to work with the syntax contained in the PDF file.

cheers

### cl...@gmail.com (2014-09-19)

I have written a similar tool to extract jp2 from PDFs to extend my fuzzing input set. The python script is attached and should also be able to extract multiple jp2 streams from a pdf. Although it is a dirty hack it works for this testcase, find the jp2 stream attached as well.
 
use like this:
create ex directory.
python extractjp2.py <pdf file>

This will create one or multiple .jp2 files in the ex directory.


### bo...@foxitsoftware.com (2014-09-19)

Thanks @cloudfuzzer. I briefly looked at the script, it makes sense to me. @mathieu, please let me know if you still have trouble with these cases.

### bo...@foxitsoftware.com (2014-09-19)

In some previous bugs I saw /Length in the stream dictionary is arbitrarily changed and does not match the actual stream length. In this scenario, PDFium should count the actual length and ignore the dictionary value. I see the script from @cloudfuzzer does no rely on the dictionary, which is what we want.

But still, here we are relying on "endstream" keyword, which maybe corrupted and cause issues, or maybe not.

### an...@gmail.com (2014-09-22)

WIP : reproduced on openjpeg side, working on a patch

### cl...@chromium.org (2014-09-27)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-09-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-29)

[Empty comment from Monorail migration]

### bo...@foxitsoftware.com (2014-09-30)

Depend on https://codereview.chromium.org/589243004/

### bo...@foxitsoftware.com (2014-09-30)

Fixed in https://pdfium.googlesource.com/pdfium/+/d53e6fdb0a86ca1ddb12876a60f7f2d7508b5349

### am...@google.com (2014-09-30)

Is there a merge required here?

### cl...@chromium.org (2014-09-30)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-10-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-10-30)

[Empty comment from Monorail migration]

### am...@chromium.org (2014-10-30)

merge approved for m39 branch 2171.  please ensure merge occurs in advance of nov 3, please email me with any issues.

### bo...@foxitsoftware.com (2014-10-31)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-11-03)

Dev/Bug owner, please merge to M-39 branch 2171 asap. We need all these security fixes to go into the first stable.

### in...@chromium.org (2014-11-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-03)

This bug is a regression and does not impact stable. Removing incorrectly added Release-0-M39 label.

- Your friendly ClusterFuzz

### mb...@chromium.org (2014-11-17)

Thanks for the report! This one qualified for a $1000 reward.

### ti...@google.com (2014-12-08)

Payment in progress

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-06)

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

This issue was migrated from crbug.com/chromium/407964?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080301)*
