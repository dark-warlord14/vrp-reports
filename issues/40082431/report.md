# stack-use-after-return in opj_pi_next_rpcl

| Field | Value |
|-------|-------|
| **Issue ID** | [40082431](https://issues.chromium.org/issues/40082431) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Reporter** | wm...@gmail.com |
| **Assignee** | ju...@foxitsoftware.com |
| **Created** | 2015-07-03 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

The attached test case crashes the asan build of pdfium\_test as follows:

=================================================================  

==20548==ERROR: AddressSanitizer: stack-use-after-return on address 0x7faf80a47824 at pc 0x00000075dbc8 bp 0x7ffcad0a8810 sp 0x7ffcad0a8808  

READ of size 2 at 0x7faf80a47824 thread T0  

#0 0x75dbc7 in opj\_pi\_next\_rpcl /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/third\_party/libopenjpeg20/pi.c:381:12  

#1 0x75b65e in opj\_pi\_next /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/third\_party/libopenjpeg20/pi.c:1867:11  

#2 0x783e9e in opj\_t2\_decode\_packets /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/third\_party/libopenjpeg20/t2.c:406:24  

#3 0x76926b in opj\_tcd\_t2\_decode /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/third\_party/libopenjpeg20/tcd.c:1562:15  

#4 0x768f74 in opj\_tcd\_decode\_tile /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/third\_party/libopenjpeg20/tcd.c:1302:15  

#5 0x736346 in opj\_j2k\_decode\_tile /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/third\_party/libopenjpeg20/j2k.c:7950:15  

#6 0x7460ee in opj\_j2k\_decode\_tiles /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/third\_party/libopenjpeg20/j2k.c:9475:23  

#7 0x730b35 in opj\_j2k\_exec /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/third\_party/libopenjpeg20/j2k.c:7318:41  

#8 0x73d857 in opj\_j2k\_decode /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/third\_party/libopenjpeg20/j2k.c:9666:15  

#9 0x74db84 in opj\_jp2\_decode /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/third\_party/libopenjpeg20/jp2.c:1406:8  

#10 0x71f6d6 in opj\_decode /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/third\_party/libopenjpeg20/openjpeg.c:412:10  

#11 0x5864d5 in CJPX\_Decoder::Init(unsigned char const\*, int) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:659:  

15  

#12 0x58931d in CCodec\_JpxModule::CreateDecoder(unsigned char const\*, unsigned int, int) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/code  

c/fx\_codec\_jpx\_opj.cpp:785:10  

#13 0x949ebc in CPDF\_DIBSource::LoadJpxBitmap() /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:675:26  

#14 0x943253 in CPDF\_DIBSource::CreateDecoder() /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:634:9  

#15 0x93ee00 in CPDF\_DIBSource::StartLoadDIBSource(CPDF\_Document\*, CPDF\_Stream const\*, int, CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build  

/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:369:15  

#16 0x92a903 in CPDF\_ImageCache::StartGetCachedBitmap(CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out  

/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:291:15  

#17 0x92a4fb in CPDF\_PageRenderCache::StartGetCachedBitmap(CPDF\_Stream\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../th  

ird\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:134:15  

#18 0x957c9f in CPDF\_ProgressiveImageLoaderHandle::Start(CPDF\_ImageLoader\*, CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /mnt/data/b/build/slave/ASAN\_  

Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1486:15  

#19 0x9588a3 in CPDF\_ImageLoader::StartLoadImage(CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, void\*&, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized  

*/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1545:19  

#20 0x9314fc in CPDF\_ImageRenderer::StartLoadDIBSource() /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:32  

8:9  

#21 0x92c252 in CPDF\_ImageRenderer::Start(CPDF\_RenderStatus\*, CPDF\_PageObject const\*, CFX\_Matrix const\*, int, int) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pd  

fium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:454:9  

#22 0x91c0ac in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject const\*, CFX\_Matrix const\*, IFX\_Pause\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium  

/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:330:14  

#23 0x924e10 in CPDF\_ProgressiveRenderer::Continue(IFX\_Pause\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:11  

19:21  

#24 0x923ee9 in CPDF\_ProgressiveRenderer::Start(CPDF\_RenderContext\*, CFX\_RenderDevice\*, CPDF\_RenderOptions const\*, IFX\_Pause\*, int) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../  

../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:1062:5  

#25 0x510c9f in FPDF\_RenderPage\_Retail(CRenderContext\*, void\*, int, int, int, int, int, int, int, IFSDK\_PAUSE\_Adapter\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_par  

ty/pdfium/fpdfsdk/src/fpdfview.cpp:727:2  

#26 0x51146c in FPDF\_RenderPageBitmap /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:518:2  

#27 0x4d2dd9 in RenderPdf(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::**1::allocator<char> > const&, char const\*, unsigned long, Options const&) /mnt/data/b/build/slave/ASAN\_Release\_\_symbo  

lized*/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:514:5  

#28 0x4d49c8 in main /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:618:5  

#29 0x7fb0cc1f1ec4 in \_\_libc\_start\_main ??:0:0

Address 0x7faf80a47824 is located in stack of thread T0 at offset 36 in frame  

#0 0x7845af in opj\_t2\_decode\_packet /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/third\_party/libopenjpeg20/t2.c:522:0

This frame has 2 object(s):  

[32, 36) 'l\_read\_data' <== Memory access at offset 36 overflows this variable  

[48, 52) 'l\_nb\_bytes\_read'  

HINT: this may be a false positive if your program uses some custom stack unwind mechanism or swapcontext  

(longjmp and C++ exceptions \*are\* supported)  

SUMMARY: AddressSanitizer: stack-use-after-return (/root/syno\_share/chrome/asan-symbolized-linux-release-337268/pdfium\_test+0x75dbc7)  

Shadow bytes around the buggy address:  

0x0ff670140eb0: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x0ff670140ec0: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x0ff670140ed0: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x0ff670140ee0: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x0ff670140ef0: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

=>0x0ff670140f00: f5 f5 f5 f5[f5]f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x0ff670140f10: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x0ff670140f20: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x0ff670140f30: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x0ff670140f40: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x0ff670140f50: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

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

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

==20548==ABORTING

**VERSION**  

Chrome Version: asan-symbolized-linux-release-337268  

Operating System: ubuntu-x64 14.04

**REPRODUCTION CASE**  

Load the attached repro.pdf with pdfium\_test

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### in...@chromium.org (2015-07-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-03)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6182784891092992

### cl...@chromium.org (2015-07-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-03)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### am...@google.com (2015-07-06)

[Empty comment from Monorail migration]

### am...@chromium.org (2015-07-08)

jun_fang, this will need to be fixed very soon, what's your status here?

### cl...@chromium.org (2015-07-10)

[Empty comment from Monorail migration]

### ju...@foxitsoftware.com (2015-07-10)

[Empty comment from Monorail migration]

### ju...@foxitsoftware.com (2015-07-11)

It's pending in https://codereview.chromium.org/1231933008/.

### ju...@foxitsoftware.com (2015-07-13)

Fixed in https://codereview.chromium.org/1231933008/.

### ju...@foxitsoftware.com (2015-07-13)

[Empty comment from Monorail migration]

### am...@chromium.org (2015-07-13)

Is there a merge required here?

### th...@chromium.org (2015-07-14)

We should merge this to M-44, but the fix just landed today and we may want to let it bake for a day or two.

### pe...@chromium.org (2015-07-14)

Yup, let is soak for verification.  It can always go in the next stable refresh.

### cl...@chromium.org (2015-07-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-07-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ca576a0e1156d39477551e2d0580ebe5d440114a

commit ca576a0e1156d39477551e2d0580ebe5d440114a
Author: thestig <thestig@chromium.org>
Date: Tue Jul 14 03:03:24 2015

Roll DEPS for PDFium to d1b0a8d

d1b0a8d Fix an integer overflow issue in openJpeg
1f4c2f2 Fix a crashier due to incorrect type conversion

BUG=506763
TBR=tsepez@chromium.org

Review URL: https://codereview.chromium.org/1229813009

Cr-Commit-Position: refs/heads/master@{#338627}

[modify] http://crrev.com/ca576a0e1156d39477551e2d0580ebe5d440114a/DEPS


### wm...@gmail.com (2015-07-14)

a question is here
what is the criterion to assign a CVE id for a Bug-Security case ?
since i noticed that some of them have, some of them do not have

i'm not sure where or who i should ask
since this is my first time to send security case

### in...@chromium.org (2015-07-14)

Any low,med,high,critical severity externally reported bug should get a cve. this one will also get one once we are close to the release and merges are done.

### mb...@chromium.org (2015-07-16)

[Empty comment from Monorail migration]

### th...@chromium.org (2015-07-20)

It's been a week, shall we try merging https://pdfium.googlesource.com/pdfium/+/d1b0a8d9dc71c67b4ce67f148cebc01d66d1d983 to M44 and roll DEPS?

### pe...@google.com (2015-07-20)

[Automated comment] Less than 2 weeks to go before stable on M44, manual review required.

### pe...@chromium.org (2015-07-20)

ok let's do it.  Let me know what the new pdfium m44 branch hash is after you merge!

### th...@chromium.org (2015-07-21)

Oh, we need to merge to M45 as well. I'll go ahead and do both.

### th...@chromium.org (2015-07-21)

M45: https://pdfium.googlesource.com/pdfium/+/0c1ad5da8affcfa0b74244bf54429f36bfe7513d
M44: https://pdfium.googlesource.com/pdfium/+/3ecc289ce0d1a639a9b3f6c59d10952269692d04

### pe...@chromium.org (2015-07-21)

Updated both official DEPS.  Merges done.

https://pdfium.googlesource.com/pdfium/+log/refs/heads/chromium/2403
https://pdfium.googlesource.com/pdfium/+log/refs/heads/chromium/2454

### cl...@chromium.org (2015-10-20)

Bulk update: removing view restriction from closed bugs.

### wm...@gmail.com (2016-02-24)

any progress about cve assign and/or reward ?

### th...@chromium.org (2016-02-24)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-30)

#27 - Apologies for the delay. We found some old bugs that weren't voted on and took them to the reward panel last week. This was one of them.

Our reward panel decided to award you $500 for this report. 

Panel notes: Appears to be a 2-byte read infoleak, so lower reward amount.

Our finance team should be in touch within 7 days to collect payment details. If that doesn't happen, please contact me directly at timwillis@

Thanks for your report!


### aw...@chromium.org (2016-07-01)

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

This issue was migrated from crbug.com/chromium/506763?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082431)*
