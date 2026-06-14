# Pdfium Heap-buffer-overflow in in opj_t1_decode_cblk

| Field | Value |
|-------|-------|
| **Issue ID** | [348129258](https://issues.chromium.org/issues/348129258) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | PDFium |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ke...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2024-06-19 |
| **Bounty** | $11,000.00 |

## Description

Chrome Version: beta, dev
Operating System: windows, linux

Bisects to : <https://pdfium-review.googlesource.com/c/pdfium/+/119592>

That change disables strict mode when decoding JPEG2000 images, which leads to out-of-bounds reads, writes.

This is also in the latest openjpeg, can be tested with ./opj\_decompress -allow-partial option.

Seems like this option was rarely fuzzed, as i see 20?? different crash locations after few days of fuzzing openjpeg with '-allow-partial', based on only stacktraces.

Not sure if they have the same root cause or not, but the <https://github.com/ispras/casr> tool puts it into ~8 clusters.

Let me know how should i report this many crashes, separately or in one report etc.

But here is one, works with chrome, pdfium\_test after that commit:

For /chromium-127.0.6533.4-linux-asan:

```
Processing PDF file /mnt/f/fuzz/findings/pdfium/jp2k/final/cl1_cblks_mqc.pdf.
Document has invalid cross reference table
=================================================================
==4503==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x50c000016c7d at pc 0x563f550b959b bp 0x7ffc1cedefd0 sp 0x7ffc1cede790
READ of size 60478 at 0x50c000016c7d thread T0
    #0 0x563f550b959a in __asan_memcpy /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors_memintrinsics.cpp:63:3
    #1 0x563f562ced5d in opj_t1_decode_cblk third_party/pdfium/third_party/libopenjpeg/t1.c:2038:13
    #2 0x563f562ced5d in opj_t1_clbl_decode_processor third_party/pdfium/third_party/libopenjpeg/t1.c:1703:26
    #3 0x563f5631eec4 in opj_thread_pool_submit_job third_party/pdfium/third_party/libopenjpeg/thread.c:835:9
    #4 0x563f562ccefd in opj_t1_decode_cblks third_party/pdfium/third_party/libopenjpeg/t1.c:1942:21
    #5 0x563f56315eaf in opj_tcd_t1_decode third_party/pdfium/third_party/libopenjpeg/tcd.c:2076:9
    #6 0x563f56315eaf in opj_tcd_decode_tile third_party/pdfium/third_party/libopenjpeg/tcd.c:1730:11
    #7 0x563f5629bf13 in opj_j2k_decode_tile third_party/pdfium/third_party/libopenjpeg/j2k.c:9902:11
    #8 0x563f562b24a4 in opj_j2k_decode_tiles third_party/pdfium/third_party/libopenjpeg/j2k.c:11773:15
    #9 0x563f562a2697 in opj_j2k_exec third_party/pdfium/third_party/libopenjpeg/j2k.c:9043:33
    #10 0x563f562a2697 in opj_j2k_decode third_party/pdfium/third_party/libopenjpeg/j2k.c:12077:11
    #11 0x563f561b87bf in fxcodec::CJPX_Decoder::StartDecode() third_party/pdfium/core/fxcodec/jpx/cjpx_decoder.cpp:498:11
    #12 0x563f56411607 in CPDF_DIB::LoadJpxBitmap(unsigned char) third_party/pdfium/core/fpdfapi/page/cpdf_dib.cpp:668:17
    #13 0x563f5640a7b6 in CPDF_DIB::CreateDecoder(unsigned char) third_party/pdfium/core/fpdfapi/page/cpdf_dib.cpp:536:23
    #14 0x563f5640cc4e in CPDF_DIB::StartLoadDIBBase(bool, CPDF_Dictionary const*, CPDF_Dictionary const*, bool, CPDF_ColorSpace::Family, bool, CFX_STemplate<int> const&) third_party/pdfium/core/fpdfapi/page/cpdf_dib.cpp:318:31
    #15 0x563f56444665 in CPDF_PageImageCache::Entry::StartGetCachedBitmap(CPDF_PageImageCache*, CPDF_Dictionary const*, CPDF_Dictionary const*, bool, CPDF_ColorSpace::Family, bool, CFX_STemplate<int> const&) third_party/pdfium/core/fpdfapi/page/cpdf_pageimagecache.cpp:272:61
    #16 0x563f56443b0b in CPDF_PageImageCache::StartGetCachedBitmap(fxcrt::RetainPtr<CPDF_Image>, CPDF_Dictionary const*, CPDF_Dictionary const*, bool, CPDF_ColorSpace::Family, bool, CFX_STemplate<int> const&) third_party/pdfium/core/fpdfapi/page/cpdf_pageimagecache.cpp:185:52
    #17 0x563f56435418 in CPDF_ImageLoader::Start(CPDF_ImageObject const*, CPDF_PageImageCache*, CPDF_Dictionary const*, CPDF_Dictionary const*, bool, CPDF_ColorSpace::Family, bool, CFX_STemplate<int> const&) third_party/pdfium/core/fpdfapi/page/cpdf_imageloader.cpp:35:33
    #18 0x563f5649a9ea in CPDF_ImageRenderer::StartLoadDIBBase() third_party/pdfium/core/fpdfapi/render/cpdf_imagerenderer.cpp:68:19
    #19 0x563f564a0dcb in CPDF_ImageRenderer::Start(CPDF_ImageObject*, CFX_Matrix const&, bool, BlendMode) third_party/pdfium/core/fpdfapi/render/cpdf_imagerenderer.cpp:186:7
    #20 0x563f564b6fc5 in CPDF_RenderStatus::ContinueSingleObject(CPDF_PageObject*, CFX_Matrix const&, PauseIndicatorIface*) third_party/pdfium/core/fpdfapi/render/cpdf_renderstatus.cpp:271:26
    #21 0x563f564a4b17 in CPDF_ProgressiveRenderer::Continue(PauseIndicatorIface*) third_party/pdfium/core/fpdfapi/render/cpdf_progressiverenderer.cpp:92:30
    #22 0x563f5516433d in (anonymous namespace)::RenderPageImpl(CPDF_PageRenderContext*, CPDF_Page*, CFX_Matrix const&, FX_RECT const&, int, FPDF_COLORSCHEME_ const*, bool, CPDFSDK_PauseAdapter*) third_party/pdfium/fpdfsdk/cpdfsdk_renderpage.cpp:84:26
    #23 0x563f551646e1 in CPDFSDK_RenderPageWithContext(CPDF_PageRenderContext*, CPDF_Page*, int, int, int, int, int, int, FPDF_COLORSCHEME_ const*, bool, CPDFSDK_PauseAdapter*) third_party/pdfium/fpdfsdk/cpdfsdk_renderpage.cpp:113:3
    #24 0x563f5517d825 in FPDF_RenderPageBitmapWithColorScheme_Start third_party/pdfium/fpdfsdk/fpdf_progressive.cpp:69:3
    #25 0x563f5510d93e in (anonymous namespace)::ProgressiveBitmapPageRenderer::Start() third_party/pdfium/testing/pdfium_test.cc:1076:9
    #26 0x563f55105935 in ProcessPage third_party/pdfium/testing/pdfium_test.cc:1520:17
    #27 0x563f55105935 in ProcessPdf third_party/pdfium/testing/pdfium_test.cc:1690:23
    #28 0x563f55105935 in main third_party/pdfium/testing/pdfium_test.cc:2006:17
    #29 0x7f0518522082 in __libc_start_main /build/glibc-e2p3jK/glibc-2.31/csu/../csu/libc-start.c:308:16

0x50c000016c7d is located 0 bytes after 125-byte region [0x50c000016c00,0x50c000016c7d)
allocated by thread T0 here:
    #0 0x563f550bb7af in malloc /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:68:3
    #1 0x563f56299055 in opj_j2k_read_sod third_party/pdfium/third_party/libopenjpeg/j2k.c:4991:43
    #2 0x563f56299055 in opj_j2k_read_tile_header third_party/pdfium/third_party/libopenjpeg/j2k.c:9731:19
    #3 0x563f562b246f in opj_j2k_decode_tiles third_party/pdfium/third_party/libopenjpeg/j2k.c:11756:19
    #4 0x563f562a2697 in opj_j2k_exec third_party/pdfium/third_party/libopenjpeg/j2k.c:9043:33
    #5 0x563f562a2697 in opj_j2k_decode third_party/pdfium/third_party/libopenjpeg/j2k.c:12077:11
    #6 0x563f561b87bf in fxcodec::CJPX_Decoder::StartDecode() third_party/pdfium/core/fxcodec/jpx/cjpx_decoder.cpp:498:11
    #7 0x563f56411607 in CPDF_DIB::LoadJpxBitmap(unsigned char) third_party/pdfium/core/fpdfapi/page/cpdf_dib.cpp:668:17
    #8 0x563f5640a7b6 in CPDF_DIB::CreateDecoder(unsigned char) third_party/pdfium/core/fpdfapi/page/cpdf_dib.cpp:536:23
    #9 0x563f5640cc4e in CPDF_DIB::StartLoadDIBBase(bool, CPDF_Dictionary const*, CPDF_Dictionary const*, bool, CPDF_ColorSpace::Family, bool, CFX_STemplate<int> const&) third_party/pdfium/core/fpdfapi/page/cpdf_dib.cpp:318:31
    #10 0x563f56444665 in CPDF_PageImageCache::Entry::StartGetCachedBitmap(CPDF_PageImageCache*, CPDF_Dictionary const*, CPDF_Dictionary const*, bool, CPDF_ColorSpace::Family, bool, CFX_STemplate<int> const&) third_party/pdfium/core/fpdfapi/page/cpdf_pageimagecache.cpp:272:61
    #11 0x563f56443b0b in CPDF_PageImageCache::StartGetCachedBitmap(fxcrt::RetainPtr<CPDF_Image>, CPDF_Dictionary const*, CPDF_Dictionary const*, bool, CPDF_ColorSpace::Family, bool, CFX_STemplate<int> const&) third_party/pdfium/core/fpdfapi/page/cpdf_pageimagecache.cpp:185:52
    #12 0x563f56435418 in CPDF_ImageLoader::Start(CPDF_ImageObject const*, CPDF_PageImageCache*, CPDF_Dictionary const*, CPDF_Dictionary const*, bool, CPDF_ColorSpace::Family, bool, CFX_STemplate<int> const&) third_party/pdfium/core/fpdfapi/page/cpdf_imageloader.cpp:35:33
    #13 0x563f5649a9ea in CPDF_ImageRenderer::StartLoadDIBBase() third_party/pdfium/core/fpdfapi/render/cpdf_imagerenderer.cpp:68:19
    #14 0x563f564a0dcb in CPDF_ImageRenderer::Start(CPDF_ImageObject*, CFX_Matrix const&, bool, BlendMode) third_party/pdfium/core/fpdfapi/render/cpdf_imagerenderer.cpp:186:7
    #15 0x563f564b6fc5 in CPDF_RenderStatus::ContinueSingleObject(CPDF_PageObject*, CFX_Matrix const&, PauseIndicatorIface*) third_party/pdfium/core/fpdfapi/render/cpdf_renderstatus.cpp:271:26
    #16 0x563f564a4b17 in CPDF_ProgressiveRenderer::Continue(PauseIndicatorIface*) third_party/pdfium/core/fpdfapi/render/cpdf_progressiverenderer.cpp:92:30
    #17 0x563f5516433d in (anonymous namespace)::RenderPageImpl(CPDF_PageRenderContext*, CPDF_Page*, CFX_Matrix const&, FX_RECT const&, int, FPDF_COLORSCHEME_ const*, bool, CPDFSDK_PauseAdapter*) third_party/pdfium/fpdfsdk/cpdfsdk_renderpage.cpp:84:26
    #18 0x563f551646e1 in CPDFSDK_RenderPageWithContext(CPDF_PageRenderContext*, CPDF_Page*, int, int, int, int, int, int, FPDF_COLORSCHEME_ const*, bool, CPDFSDK_PauseAdapter*) third_party/pdfium/fpdfsdk/cpdfsdk_renderpage.cpp:113:3
    #19 0x563f5517d825 in FPDF_RenderPageBitmapWithColorScheme_Start third_party/pdfium/fpdfsdk/fpdf_progressive.cpp:69:3
    #20 0x563f5510d93e in (anonymous namespace)::ProgressiveBitmapPageRenderer::Start() third_party/pdfium/testing/pdfium_test.cc:1076:9
    #21 0x563f55105935 in ProcessPage third_party/pdfium/testing/pdfium_test.cc:1520:17
    #22 0x563f55105935 in ProcessPdf third_party/pdfium/testing/pdfium_test.cc:1690:23
    #23 0x563f55105935 in main third_party/pdfium/testing/pdfium_test.cc:2006:17
    #24 0x7f0518522082 in __libc_start_main /build/glibc-e2p3jK/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/pdfium/third_party/libopenjpeg/t1.c:2038:13 in opj_t1_decode_cblk
Shadow bytes around the buggy address:
  0x50c000016980: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x50c000016a00: 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x50c000016a80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x50c000016b00: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x50c000016b80: 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
=>0x50c000016c00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00[05]
  0x50c000016c80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x50c000016d00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x50c000016d80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x50c000016e00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x50c000016e80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==4503==ABORTING


```

CREDIT INFORMATION

Reporter credit: soiax

## Attachments

- [cl1_cblks_mqc.pdf](attachments/cl1_cblks_mqc.pdf) (application/pdf, 1.2 KB)
- [poc1.j2k](attachments/poc1.j2k) (application/octet-stream, 608 B)
- [poc2.j2k](attachments/poc2.j2k) (application/octet-stream, 660 B)
- [poc3.j2k](attachments/poc3.j2k) (application/octet-stream, 212 B)

## Timeline

### ke...@gmail.com (2024-06-19)

The strict mode is checked at 2 places, although, one of my crashes never hits any of them, but doesn't crash with stirct mode which is weird.

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/pdfium/third_party/libopenjpeg/j2k.c;l=4968?q=j2k>.

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/pdfium/third_party/libopenjpeg/j2k.c;l=9944?q=j2k>.

### ke...@gmail.com (2024-06-20)

Looked it some more:

at <https://source.chromium.org/chromium/chromium/src/+/main:third_party/pdfium/third_party/libopenjpeg/j2k.c;l=5052?q=j2k>

opj\_stream\_read\_data documentation says "the number of bytes read, or -1 if an error occurred or if the stream is at the end."

It fails SOD marker FF93 is at the end of the stream, and it is never checked if it returned -1, so -1(0xffffffff) is used as l\_tile\_len a few lines later.

That becomes p\_j2k->m\_cp.tcps[x]->m\_data\_size and causes problems.

### th...@chromium.org (2024-06-20)

Thanks for the report. Confirmed this issue repros with PDFium using a commit from today.

### th...@chromium.org (2024-06-20)

<https://pdfium-review.googlesource.com/120793> will revert <https://pdfium-review.googlesource.com/119592> to stop using the problematic code path in OpenJPEG.

Bug reporter: Could you separately report the issue to OpenJPEG, so they can fix the issue on their end?

### ma...@chromium.org (2024-06-20)

looks like the original patch went in chromium 6501 branch which has gone to beta

### ma...@chromium.org (2024-06-20)

medium severity due to being in a renderer process

### ma...@chromium.org (2024-06-20)

(misread initially, should actually be s1 - memory corruption in renderer)

### ke...@gmail.com (2024-06-20)

Reported to Openjpeg <https://github.com/uclouvain/openjpeg/issues/1533>

Tried with a hotfix for the root cause i mentioned in #3, it fixed a bunch of the crashes i found. But still there are 2 more.
Should i just report those also to openjpeg and not here?

### ke...@gmail.com (2024-06-20)

I mean, if it would be still rewardable by google, if i report here

### th...@chromium.org (2024-06-20)

amyressler@ may be able to better reply to [comment #9](https://issues.chromium.org/issues/348129258#comment9) / [comment #10](https://issues.chromium.org/issues/348129258#comment10).

OpenJPEG may have multiple issues within their code base. From the PDFium side, I'm going to fix the issue by avoiding the problematic code path in <https://pdfium-review.googlesource.com/120793>. If you are still finding crashes with <https://pdfium-review.googlesource.com/120793> applied, then I think it would be fair to report the issue both to Chromium/PDFium and to OpenJPEG.

### ap...@google.com (2024-06-20)

Project: pdfium
Branch: main

commit 05adb819cadd57e396f33a76a83551d550c3fde8
Author: Lei Zhang <thestig@chromium.org>
Date:   Thu Jun 20 23:25:06 2024

    Revert "Do not use strict mode when decoding JPEG2000 images"
    
    This reverts commit e97ee6e258c4657747070c876a51206312347e9b.
    
    Reason for revert: Caused decoding problems in OpenJPEG.
    
    Original change's description:
    > Do not use strict mode when decoding JPEG2000 images
    >
    > Acrobat Reader can render the PDF attached to the bug report, while
    > PDFium cannot. This is because PDFium uses libopenjpeg, and in the past
    > libopenjpeg only had strict mode, which rejects the image in the PDF and
    > refuses to do partial rendering. Now opj_decoder_set_strict_mode()
    > exists in libopenjpeg. Use it to unset strict mode, so PDFium can render
    > the PDF in the bug report in the same way as Acrobat Reader.
    >
    > Bug: 42270564
    > Change-Id: I77b1f73659d48252d488a4a1bd170cce20017aff
    > Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/119592
    > Reviewed-by: Tom Sepez <tsepez@chromium.org>
    > Reviewed-by: Thomas Sepez <tsepez@google.com>
    > Commit-Queue: Lei Zhang <thestig@chromium.org>
    
    # Not skipping CQ checks because original CL landed > 1 day ago.
    
    Bug: 42270564, 348129258
    Change-Id: I5a6cff61c89e56bce79365fd6aeeeb12756fc724
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/120793
    Commit-Queue: Lei Zhang <thestig@chromium.org>
    Reviewed-by: Thomas Sepez <tsepez@google.com>

M       core/fxcodec/jpx/cjpx_decoder.cpp

https://pdfium-review.googlesource.com/120793


### ap...@google.com (2024-06-21)

Project: chromium/src
Branch: main

commit 2e14fd69322bf53a18ea4007e0009a27aa07d692
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Fri Jun 21 04:37:59 2024

    Roll PDFium from 31bb397fc446 to f83642893991 (8 revisions)
    
    https://pdfium.googlesource.com/pdfium.git/+log/31bb397fc446..f83642893991
    
    2024-06-21 tsepez@chromium.org Avoid UNSAFE_BUFFERS in CPDFSDK_AppStream
    2024-06-20 thestig@chromium.org Revert "Do not use strict mode when decoding JPEG2000 images"
    2024-06-20 thestig@chromium.org Add GetWidgetOfTypes() helper inside fpdf_annot.cpp
    2024-06-20 tsepez@chromium.org Convert FXSYS_wcstof() to take a WideStringView argument.
    2024-06-20 tsepez@chromium.org Avoid unsafe buffer usage in fpdf_sysfontinfo.cpp
    2024-06-20 thestig@chromium.org Remove CPDF_CrossRefTable::ObjectType::kNull
    2024-06-20 thestig@chromium.org Remove dead code in CPDF_Parser::ProcessCrossRefStreamEntry()
    2024-06-20 thestig@chromium.org Do not hard code the generation number in CPDF_CrossRefTable::SetFree()
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/pdfium-autoroll
    Please CC dhoss@chromium.org,pdfium-deps-rolls@chromium.org,thestig@chromium.org on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in PDFium: https://bugs.chromium.org/p/pdfium/issues/entry
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Bug: chromium:345274934,chromium:348129258,chromium:42270564,chromium:42271176
    Tbr: pdfium-deps-rolls@chromium.org
    Change-Id: I613accf4258da75f49c33ab0d842be896fd4c949
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5647196
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1317767}

M       DEPS
M       third_party/pdfium

https://chromium-review.googlesource.com/5647196


### th...@chromium.org (2024-06-21)

Verified fix with the revert. Since a relatively short-lived CL got reverted, shall we merge to M127?

### pe...@google.com (2024-06-21)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-06-21)

Requesting merge to beta (M127) because latest trunk commit (1317767) appears to be after beta branch point (1313161).
Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [127].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### am...@chromium.org (2024-06-22)

re: c#9 / c#10 -- thanks for the question and for tagging me in, thestig@,

> Reported to Openjpeg <https://github.com/uclouvain/openjpeg/issues/1533>
> Tried with a hotfix for the root cause i mentioned in #3, it fixed a bunch of the crashes i found. But still there are 2 more. Should i just report those also to openjpeg and not here?

Yes, please report to openjpeg. This issue needs to be resolved upstream in openjpeg so not only they can resolve it, but the fix can be included in an openjpeg update and not just a Chromium one. If it impacts Chrome, you can report it upstream in parallel to reporting to us.

> I mean, if it would be still rewardable by google, if i report here

Security issues in third-party dependencies are VPR eligible only if they manifest in / are reachable and exploitable in Chrome. Meaning that any report to us in a Chromium third-party dependency must be presented with a report and testcase / POC that demonstrates that bug in version of Chrome that is part of an active release channel.
But they should also still be reported to the maintainers of a given dependency so that it can be resolved at the source.

### ke...@gmail.com (2024-06-24)

amyressler@ Yeah, i know those general rules, my question was more about this pecific case.

Because in in my report c#1 i mentioned that i have multiple crashes, and i wanted to report all of them, just wasn't sure of the root cause, but i got no answer to that question. Then it was fixed so fast with a revert, that i never reported them. So my question was more about those, if those would still be considered for reward.

Also the fix was just removing that "flag" in the third party component which was switched on before, which kills all of the found bugs in pdfium, but they are still in openjpeg. So if one assumes that pdfium will "revert this revert" and allow that "strict mode off" flag, there is an incentive to sit on those bugs until this lands again in pdfium.

Isn't this similar to (from vrp rules): "Bugs in unlaunched features - in code behind a flag not enabled by default - are generally eligible for the full potential VRP reward..."

### th...@chromium.org (2024-06-24)

pdf\_jpx\_fuzzer running on ClusterFuzz found a bug similar to this in [bug 347071498](https://issues.chromium.org/issues/347071498) about 5 days ago. But that bug report auto-closed due to the actions on this bug. I'm going to tweak pdf\_jpx\_fuzzer to check the problematic code path to help flush out some of the issues.

### ke...@gmail.com (2024-06-24)

I guess i will just add the 2 other cases here as j2k images. You can add to the fuzzer, or check if these were the same what it found.
These crash, even after the one i already reported to openjpeg was fixed.
I'll report them to openjpeg.

### ke...@gmail.com (2024-06-24)

Sorry i think i attached 2 same crashes. Here is the good one.

### th...@chromium.org (2024-06-24)

Thanks. I'll check. For the change mentioned in [comment #19](https://issues.chromium.org/issues/348129258#comment19) - that's <https://pdfium-review.googlesource.com/120930>

### th...@chromium.org (2024-06-24)

I tweaked pdf\_jpx\_fuzzer slightly, so it can process the files in [comment #20](https://issues.chromium.org/issues/348129258#comment20) and [comment #21](https://issues.chromium.org/issues/348129258#comment21).

poc3.j2k is similar to [bug 347071498](https://issues.chromium.org/issues/347071498) in that the stack trace is the same until they reach opj\_t1\_decode\_cblk(). Though the poc3.j2k OOB happens after opj\_realloc(), while that is not the case in [bug 347071498](https://issues.chromium.org/issues/347071498).

### th...@chromium.org (2024-06-24)

Thanks for filing <https://github.com/uclouvain/openjpeg/issues/1535>, BTW. I can also confirm that the fix for <https://github.com/uclouvain/openjpeg/issues/1533> does not fix any of the problems mentioned in [comment #23](https://issues.chromium.org/issues/348129258#comment23).

### am...@chromium.org (2024-06-25)

127 merge approved, please merge this change to branch 6533 by EOD tomorrow (Tuesday, 25 June) so this fix can be included in the next M127 beta update

### th...@chromium.org (2024-06-25)

Uploaded <https://pdfium-review.googlesource.com/121030> for the M127 cherry-pick.

### ke...@gmail.com (2024-06-25)

Looks like the fix for <https://github.com/uclouvain/openjpeg/issues/1535> fixes all the crashes.

### th...@chromium.org (2024-06-25)

Great to hear. Thanks again for working with OpenJPEG upstream to make their library more secure.

### ap...@google.com (2024-06-25)

Project: pdfium
Branch: main

commit 9d981f8dbf9b0b7b282bcc829b94da5f5d0bc4de
Author: Lei Zhang <thestig@chromium.org>
Date:   Tue Jun 25 17:12:53 2024

    Add strict_mode parameter to CJPX_Decoder::Create()
    
    Allow pdf_jpx_fuzzer to exercise the JPEG2000 decoding code, without
    enabling the new code paths exposed by calling
    opj_decoder_set_strict_mode() by default.
    
    Bug: 42270564, 347071498, 348129258
    Change-Id: Iabb7be6e098b322a7c7c916e01fca4a8f55d9633
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/120930
    Reviewed-by: Thomas Sepez <tsepez@google.com>
    Reviewed-by: Tom Sepez <tsepez@chromium.org>
    Commit-Queue: Lei Zhang <thestig@chromium.org>

M       core/fpdfapi/page/cpdf_dib.cpp
M       core/fxcodec/jpx/cjpx_decoder.cpp
M       core/fxcodec/jpx/cjpx_decoder.h
M       testing/fuzzers/pdf_jpx_fuzzer.cc

https://pdfium-review.googlesource.com/120930


### ap...@google.com (2024-06-25)

Project: pdfium
Branch: chromium/6533

commit 6265082af5b2e931c01781befbd93abf39c3d4be
Author: Lei Zhang <thestig@chromium.org>
Date:   Tue Jun 25 18:19:06 2024

    M127: Revert "Do not use strict mode when decoding JPEG2000 images"
    
    This reverts commit e97ee6e258c4657747070c876a51206312347e9b.
    
    Reason for revert: Caused decoding problems in OpenJPEG.
    
    Original change's description:
    > Do not use strict mode when decoding JPEG2000 images
    >
    > Acrobat Reader can render the PDF attached to the bug report, while
    > PDFium cannot. This is because PDFium uses libopenjpeg, and in the past
    > libopenjpeg only had strict mode, which rejects the image in the PDF and
    > refuses to do partial rendering. Now opj_decoder_set_strict_mode()
    > exists in libopenjpeg. Use it to unset strict mode, so PDFium can render
    > the PDF in the bug report in the same way as Acrobat Reader.
    >
    > Bug: 42270564
    > Change-Id: I77b1f73659d48252d488a4a1bd170cce20017aff
    > Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/119592
    > Reviewed-by: Tom Sepez <tsepez@chromium.org>
    > Reviewed-by: Thomas Sepez <tsepez@google.com>
    > Commit-Queue: Lei Zhang <thestig@chromium.org>
    
    # Not skipping CQ checks because original CL landed > 1 day ago.
    
    Bug: 42270564, 348129258
    Change-Id: I5a6cff61c89e56bce79365fd6aeeeb12756fc724
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/120793
    Commit-Queue: Lei Zhang <thestig@chromium.org>
    Reviewed-by: Thomas Sepez <tsepez@google.com>
    (cherry picked from commit 05adb819cadd57e396f33a76a83551d550c3fde8)
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/121030

M       core/fxcodec/jpx/cjpx_decoder.cpp

https://pdfium-review.googlesource.com/121030


### pe...@google.com (2024-06-25)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### th...@chromium.org (2024-06-25)

M120 branched in 2023, so this does not affect M120.

### ap...@google.com (2024-06-26)

Project: pdfium
Branch: main

commit 9b84dbe470bec1a376a026b5e1e41ed9f1e19841
Author: Lei Zhang <thestig@chromium.org>
Date:   Wed Jun 26 00:40:12 2024

    Cherry-pick OpenJPEG patches to fix non-strict mode buffer overflows
    
    Cherry-pick these 2 commits from upstream OpenJPEG:
    
    https://github.com/uclouvain/openjpeg/commit/dea92eea8b6ab55f7eb542ea229b2c2124aa2124
    https://github.com/uclouvain/openjpeg/commit/f3b28c5ee417df9f23ca590b0e949d8a309408a0
    
    Bug: 42270564, 347071498, 348129258
    Change-Id: I8e8812e9b2fa93c9cfe9f3577742a146ae81c423
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/121050
    Reviewed-by: Thomas Sepez <tsepez@google.com>
    Commit-Queue: Lei Zhang <thestig@chromium.org>

A       third_party/libopenjpeg/0047-validate_opj_stream_read_data.patch
A       third_party/libopenjpeg/0048-check_corruption_non_strict_mode.patch
M       third_party/libopenjpeg/README.pdfium
M       third_party/libopenjpeg/j2k.c
M       third_party/libopenjpeg/t1.c
M       third_party/libopenjpeg/t2.c
M       third_party/libopenjpeg/tcd.h

https://pdfium-review.googlesource.com/121050


### ap...@google.com (2024-06-26)

Project: chromium/src
Branch: main

commit b9d2b509599d8ead9cc4bb35cc9ff906384d2d89
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Wed Jun 26 08:24:20 2024

    Roll PDFium from 09635f35dc56 to d0e6c58fe524 (6 revisions)
    
    https://pdfium.googlesource.com/pdfium.git/+log/09635f35dc56..d0e6c58fe524
    
    2024-06-26 tsepez@chromium.org Replace spancpy() with fxcrt::Copy() where possible.
    2024-06-26 thestig@chromium.org Cherry-pick OpenJPEG patches to fix non-strict mode buffer overflows
    2024-06-25 tsepez@chromium.org Avoid integer overflow in CFX_Font::GetBBox()
    2024-06-25 tsepez@chromium.org Convert byteorder.h to use fixed-size span arguments.
    2024-06-25 thestig@chromium.org Add FPDFFlattenEmbedderTest.FlatWithBadFont
    2024-06-25 thestig@chromium.org Add strict_mode parameter to CJPX_Decoder::Create()
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/pdfium-autoroll
    Please CC dhoss@chromium.org,pdfium-deps-rolls@chromium.org,thestig@chromium.org on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in PDFium: https://bugs.chromium.org/p/pdfium/issues/entry
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Bug: chromium:344775293,chromium:347071498,chromium:348129258,chromium:42270564
    Tbr: pdfium-deps-rolls@chromium.org
    Change-Id: I35d3f1f552977fe963de29c7c23fd5a6ddac2df7
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5657416
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1319629}

M       DEPS
M       third_party/pdfium

https://chromium-review.googlesource.com/5657416


### sp...@google.com (2024-06-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
$10,000 for high quality report of memory corruption in a sandboxed process + $1,000 bisect bonus


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-27)

Congratulations soiax! We have decided to award you $10,000 as a high-quality report for rooting the other OpenJPEG we mitigated in Chrome our revert and reporting them upstream to OpenJPEG so they could be resolved. Thank you for your efforts and reporting this issue in detail to us and OpenJPEG -- great work!

### rz...@google.com (2024-06-27)

Labelling it as not applicable for 120, see #32

### pe...@google.com (2024-06-27)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2024-09-09)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2024-09-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### qk...@google.com (2024-10-07)

Labeling it is not applicable for 126 as well. Because the suspected CL[1] was not included in M126.

[1] https://pdfium-review.googlesource.com/c/pdfium/+/119592

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/348129258)*
