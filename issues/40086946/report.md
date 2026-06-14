# Security: heap-buffer-overflow in FlateUncompress

| Field | Value |
|-------|-------|
| **Issue ID** | [40086946](https://issues.chromium.org/issues/40086946) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Windows |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2017-03-02 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

An integer truncation vulnerability exists in FlateUncompress (in fx\_codec\_flate.cpp) when dealing with large compressed streams(>4gig) leading to the allocation of an insufficiently sized buffer and a subsequent heap buffer overflow.

The latest x64 ASAN build of pdfium\_test crashes as follows when loading the attached testcase:

# Rendering PDF file /dev/shm/dash.pdf.

==18776==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000000931 at pc 0x0000004b6874 bp 0x7ffd9d614530 sp 0x7ffd9d613ce0  

WRITE of size 8349028 at 0x602000000931 thread T0  

#0 0x4b6873 in \_\_asan\_memcpy ??:?  

#1 0x4b6873 in ?? ??:0  

#2 0x27d20df in FlateUncompress /mnt/data/b/c/b/ASAN\_Release/src/out/Release/../../third\_party/pdfium/core/fxcodec/codec/fx\_codec\_flate.cpp:603  

#3 0x27d20df in FlateOrLZWDecode /mnt/data/b/c/b/ASAN\_Release/src/out/Release/../../third\_party/pdfium/core/fxcodec/codec/fx\_codec\_flate.cpp:832  

#4 0x27d20df in ?? ??:0  

#5 0x267cdbd in FPDFAPI\_FlateOrLZWDecode(bool, unsigned char const\*, unsigned int, CPDF\_Dictionary\*, unsigned int, unsigned char\*&, unsigned int&) /mnt/data/b/c/b/ASAN\_Release/src/out/Release/../../third\_party/pdfium/core/fpdfapi/parser/fpdf\_parser\_decode.cpp:320  

#6 0x267cdbd in ?? ??:0  

#7 0x267da23 in PDF\_DataDecode(unsigned char const\*, unsigned int, CPDF\_Dictionary const\*, unsigned char\*&, unsigned int&, CFX\_ByteString&, CPDF\_Dictionary\*&, unsigned int, bool) crtstuff.c:?  

#8 0x267da23 in ?? ??:0  

#9 0x266d054 in CPDF\_StreamAcc::LoadAllData(CPDF\_Stream const\*, bool, unsigned int, bool) /mnt/data/b/c/b/ASAN\_Release/src/out/Release/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_stream\_acc.cpp:47  

#10 0x266d054 in ?? ??:0  

#11 0x26ee16e in CPDF\_ContentParser::Start(CPDF\_Page\*) /mnt/data/b/c/b/ASAN\_Release/src/out/Release/../../third\_party/pdfium/core/fpdfapi/page/cpdf\_contentparser.cpp:59  

#12 0x26ee16e in ?? ??:0  

#13 0x25e35f9 in StartParse /mnt/data/b/c/b/ASAN\_Release/src/out/Release/../../third\_party/pdfium/core/fpdfapi/page/cpdf\_page.cpp:94  

#14 0x25e35f9 in ParseContent /mnt/data/b/c/b/ASAN\_Release/src/out/Release/../../third\_party/pdfium/core/fpdfapi/page/cpdf\_page.cpp:99  

#15 0x25e35f9 in ?? ??:0  

#16 0x24c83b5 in FPDF\_LoadPage /mnt/data/b/c/b/ASAN\_Release/src/out/Release/../../third\_party/pdfium/fpdfsdk/fpdfview.cpp:636  

#17 0x24c83b5 in ?? ??:0  

#18 0x50412a in GetPageForIndex(\_FPDF\_FORMFILLINFO\*, void\*, int) /mnt/data/b/c/b/ASAN\_Release/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:617  

#19 0x50412a in ?? ??:0  

#20 0x5049df in RenderPage(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, void\*, void\*&, FPDF\_FORMFILLINFO\_PDFiumTest&, int, Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) /mnt/data/b/c/b/ASAN\_Release/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:637  

#21 0x5049df in ?? ??:0  

#22 0x507424 in RenderPdf(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, char const\*, unsigned long, Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) /mnt/data/b/c/b/ASAN\_Release/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:862  

#23 0x507424 in ?? ??:0  

#24 0x5089e3 in main /mnt/data/b/c/b/ASAN\_Release/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:1003  

#25 0x5089e3 in ?? ??:0  

#26 0x7faaf0f143f0 in \_\_libc\_start\_main /build/glibc-jxM2Ev/glibc-2.24/csu/../csu/libc-start.c:291  

#27 0x7faaf0f143f0 in ?? ??:0

0x602000000931 is located 0 bytes to the right of 1-byte region [0x602000000930,0x602000000931)  

allocated by thread T0 here:  

#0 0x4ccd83 in \_\_interceptor\_calloc ??:?  

#1 0x4ccd83 in ?? ??:0  

#2 0x27d1d1f in FX\_AllocOrDie /mnt/data/b/c/b/ASAN\_Release/src/out/Release/../../third\_party/pdfium/core/fxcrt/fx\_memory.h:40  

#3 0x27d1d1f in FlateUncompress /mnt/data/b/c/b/ASAN\_Release/src/out/Release/../../third\_party/pdfium/core/fxcodec/codec/fx\_codec\_flate.cpp:595  

#4 0x27d1d1f in FlateOrLZWDecode /mnt/data/b/c/b/ASAN\_Release/src/out/Release/../../third\_party/pdfium/core/fxcodec/codec/fx\_codec\_flate.cpp:832  

#5 0x27d1d1f in ?? ??:0  

#6 0x267cdbd in FPDFAPI\_FlateOrLZWDecode(bool, unsigned char const\*, unsigned int, CPDF\_Dictionary\*, unsigned int, unsigned char\*&, unsigned int&) /mnt/data/b/c/b/ASAN\_Release/src/out/Release/../../third\_party/pdfium/core/fpdfapi/parser/fpdf\_parser\_decode.cpp:320  

#7 0x267cdbd in ?? ??:0  

#8 0x267da23 in PDF\_DataDecode(unsigned char const\*, unsigned int, CPDF\_Dictionary const\*, unsigned char\*&, unsigned int&, CFX\_ByteString&, CPDF\_Dictionary\*&, unsigned int, bool) crtstuff.c:?  

#9 0x267da23 in ?? ??:0  

#10 0x266d054 in CPDF\_StreamAcc::LoadAllData(CPDF\_Stream const\*, bool, unsigned int, bool) /mnt/data/b/c/b/ASAN\_Release/src/out/Release/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_stream\_acc.cpp:47  

#11 0x266d054 in ?? ??:0  

#12 0x26ee16e in CPDF\_ContentParser::Start(CPDF\_Page\*) /mnt/data/b/c/b/ASAN\_Release/src/out/Release/../../third\_party/pdfium/core/fpdfapi/page/cpdf\_contentparser.cpp:59  

#13 0x26ee16e in ?? ??:0  

#14 0x25e35f9 in StartParse /mnt/data/b/c/b/ASAN\_Release/src/out/Release/../../third\_party/pdfium/core/fpdfapi/page/cpdf\_page.cpp:94  

#15 0x25e35f9 in ParseContent /mnt/data/b/c/b/ASAN\_Release/src/out/Release/../../third\_party/pdfium/core/fpdfapi/page/cpdf\_page.cpp:99  

#16 0x25e35f9 in ?? ??:0  

#17 0x24c83b5 in FPDF\_LoadPage /mnt/data/b/c/b/ASAN\_Release/src/out/Release/../../third\_party/pdfium/fpdfsdk/fpdfview.cpp:636  

#18 0x24c83b5 in ?? ??:0  

#19 0x50412a in GetPageForIndex(\_FPDF\_FORMFILLINFO\*, void\*, int) /mnt/data/b/c/b/ASAN\_Release/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:617  

#20 0x50412a in ?? ??:0  

#21 0x5049df in RenderPage(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, void\*, void\*&, FPDF\_FORMFILLINFO\_PDFiumTest&, int, Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) /mnt/data/b/c/b/ASAN\_Release/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:637  

#22 0x5049df in ?? ??:0  

#23 0x507424 in RenderPdf(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, char const\*, unsigned long, Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) /mnt/data/b/c/b/ASAN\_Release/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:862  

#24 0x507424 in ?? ??:0  

#25 0x5089e3 in main /mnt/data/b/c/b/ASAN\_Release/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:1003  

#26 0x5089e3 in ?? ??:0  

#27 0x7faaf0f143f0 in \_\_libc\_start\_main /build/glibc-jxM2Ev/glibc-2.24/csu/../csu/libc-start.c:291  

#28 0x7faaf0f143f0 in ?? ??:0

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/nils/huuuge/asan-linux-release-453840/pdfium\_test+0x4b6873)  

Shadow bytes around the buggy address:  

0x0c047fff80d0: fa fa 01 fa fa fa 04 fa fa fa 01 fa fa fa fd fa  

0x0c047fff80e0: fa fa fd fd fa fa 00 fa fa fa 00 00 fa fa 00 fa  

0x0c047fff80f0: fa fa 00 00 fa fa fd fa fa fa fd fa fa fa fd fd  

0x0c047fff8100: fa fa 00 fa fa fa fd fa fa fa fd fd fa fa 04 fa  

0x0c047fff8110: fa fa 00 fa fa fa fc fc fa fa 00 00 fa fa fd fa  

=>0x0c047fff8120: fa fa fd fd fa fa[01]fa fa fa fa fa fa fa fa fa  

0x0c047fff8130: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c047fff8140: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c047fff8150: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c047fff8160: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c047fff8170: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

==18776==ABORTING

**VERSION**  

Chrome Version: asan-linux-release-453840

**REPRODUCTION CASE**  

attached as crash.pdf

## Attachments

- [crash.pdf](attachments/crash.pdf) (application/pdf, 4.0 MB)

## Timeline

### cl...@chromium.org (2017-03-02)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4731404748587008

### cl...@chromium.org (2017-03-02)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4663211405344768

### va...@chromium.org (2017-03-02)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### va...@chromium.org (2017-03-02)

[Empty comment from Monorail migration]

### va...@chromium.org (2017-03-02)

Setting "Security_Severity-High" based on cluster-fuzz recommendation. Feel free to change.

### ds...@chromium.org (2017-03-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-03)

[Empty comment from Monorail migration]

### va...@chromium.org (2017-03-04)

Not sure about Mac but I guess it happens there too.

### bu...@chromium.org (2017-03-06)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/f6d0146200beec76f3d8676e22562d1acbc83d91

commit f6d0146200beec76f3d8676e22562d1acbc83d91
Author: dan sinclair <dsinclair@chromium.org>
Date: Mon Mar 06 18:55:09 2017

Check size before writting

Before writting to the stream buffer make sure that we won't walk off the end
of the allocated size.

In this specific case the dest_size of the buffer is 0, so we're basically just
looping over to free the temp results.

BUG=chromium:697847

Change-Id: I229eea96179692216cb2685facbb7d5379c501c7
Reviewed-on: https://pdfium-review.googlesource.com/2903
Commit-Queue: dsinclair <dsinclair@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>

[modify] https://crrev.com/f6d0146200beec76f3d8676e22562d1acbc83d91/core/fxcodec/codec/fx_codec_flate.cpp


### ds...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-03-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/65dff8b6da7b33d422b5e02356e58254fded9006

commit 65dff8b6da7b33d422b5e02356e58254fded9006
Author: pdfium-deps-roller <pdfium-deps-roller@chromium.org>
Date: Mon Mar 06 20:42:05 2017

Roll src/third_party/pdfium/ 19fad5742..f6d014620 (2 commits)

https://pdfium.googlesource.com/pdfium.git/+log/19fad5742414..f6d0146200be

$ git log 19fad5742..f6d014620 --date=short --no-merges --format='%ad %ae %s'
2017-03-06 dsinclair Check size before writting
2017-03-06 dsinclair Simplify RTFBreak AppendChar.

Created with:
  roll-dep src/third_party/pdfium
BUG=697847

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, see:
http://www.chromium.org/developers/tree-sheriffs/sheriff-details-chromium#TOC-Failures-due-to-DEPS-rolls

TBR=dsinclair@chromium.org

Review-Url: https://codereview.chromium.org/2731373002
Cr-Commit-Position: refs/heads/master@{#454948}

[modify] https://crrev.com/65dff8b6da7b33d422b5e02356e58254fded9006/DEPS


### sh...@chromium.org (2017-03-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-15)

[Empty comment from Monorail migration]

### aw...@google.com (2017-03-15)

Nice one! The panel awarded $1,000 for this bug - many thanks!

### aw...@chromium.org (2017-03-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-06-13)

This issue was migrated from crbug.com/chromium/697847?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086946)*
