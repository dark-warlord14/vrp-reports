# UNKNOWN in sk_memset32_SSE2

| Field | Value |
|-------|-------|
| **Issue ID** | [40081608](https://issues.chromium.org/issues/40081608) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Linux |
| **Reporter** | ao...@gmail.com |
| **Assignee** | re...@chromium.org |
| **Created** | 2015-03-13 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2331.0 Safari/537.36

Steps to reproduce the problem:
1. $ tar -zxvf ch-unknown-sep_upsample.tar.gz
2. $ cd ch-unknown-sep_upsample
3. $ chrome-asan loader-jpeg.html

What is the expected behavior?

What went wrong?
==7==ERROR: AddressSanitizer: SEGV on unknown address 0x7fd5bb5a5500 (pc 0x7fd75cb7c153 bp 0x7fd5d34f3eb0 sp 0x7fd5d34f3e28 T7)
    #0 0x7fd75cb7c152 in ?? simd/jdcolss2-64.asm:?
    #1 0xc520004d93e  (<unknown module>)
    #1 0x7fd75cb5af37 in sep_upsample /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/libjpeg_turbo/jdsample.c:133
    #2 0x7fd75cbeb454 in process_data_simple_main /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/libjpeg_turbo/jdmainct.c:370
    #3 0x7fd75cb25350 in chromium_jpeg_read_scanlines /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/libjpeg_turbo/jdapistd.c:176
    #4 0x7fd75dcf3a14 in blink::JPEGImageDecoder::outputScanlines() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/image-decoders/jpeg/JPEGImageDecoder.cpp:960
    #5 0x7fd75dcf758a in blink::JPEGImageReader::decode(blink::SharedBuffer const&, bool) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/image-decoders/jpeg/JPEGImageDecoder.cpp:563
    #6 0x7fd75dcf1ea1 in blink::JPEGImageDecoder::decode(bool) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/image-decoders/jpeg/JPEGImageDecoder.cpp:1007
    #7 0x7fd75dcf2f89 in blink::JPEGImageDecoder::frameBufferAtIndex(unsigned long) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/image-decoders/jpeg/JPEGImageDecoder.cpp:777
    #8 0x7fd75ddb5f7b in blink::ImageFrameGenerator::decode(unsigned long, blink::ImageDecoder**, SkBitmap*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/graphics/ImageFrameGenerator.cpp:298
    #9 0x7fd75ddb3b7c in blink::ImageFrameGenerator::tryToResumeDecode(SkTSize<int> const&, unsigned long) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/graphics/ImageFrameGenerator.cpp:201
    #10 0x7fd75ddb3461 in blink::ImageFrameGenerator::decodeAndScale(SkImageInfo const&, unsigned long, void*, unsigned long) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/graphics/ImageFrameGenerator.cpp:131
    #11 0x7fd75dddaa60 in onGetPixels /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/graphics/DecodingImageGenerator.cpp:87
    #12 0x7fd75c62a461 in SkImageGenerator::getPixels(SkImageInfo const&, void*, unsigned long, unsigned int*, int*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/core/SkImageGenerator.cpp:43
    #13 0x7fd75c608cb8 in SkDiscardablePixelRef::onNewLockPixels(SkPixelRef::LockRec*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/lazy/SkDiscardablePixelRef.cpp:74
    #14 0x7fd75c342b1f in SkPixelRef::lockPixels(SkPixelRef::LockRec*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/core/SkPixelRef.cpp:164
    #15 0x7fd75c342d95 in SkPixelRef::lockPixels() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/core/SkPixelRef.cpp:177
    #16 0x7fd75d81ae42 in cc::(anonymous namespace)::ImageDecodeTaskImpl::RunOnWorkerThread() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../cc/resources/tile_manager.cc:149
    #17 0x7fd75da765cb in RunTaskWithLockAcquired /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../cc/resources/task_graph_runner.cc:423
    #18 0x7fd75da75bb8 in Run /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../cc/resources/task_graph_runner.cc:366
    #19 0x7fd75b4dc983 in base::DelegateSimpleThread::Run() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/threading/simple_thread.cc:81
    #20 0x7fd75b4dc719 in ThreadMain /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/threading/simple_thread.cc:60
    #21 0x7fd75b4cd48a in base::(anonymous namespace)::ThreadFunc(void*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/threading/platform_thread_posix.cc:80
    #22 0x7fd750fe3181 in start_thread /build/buildd/eglibc-2.19/nptl/pthread_create.c:312 (discriminator 2)

Did this work before? N/A 

Chrome version: 43.0.2331.0  Channel: n/a
OS Version: 
Flash Version:

## Attachments

- [ch-unknown-sep_upsample.tar.gz](attachments/ch-unknown-sep_upsample.tar.gz) (application/x-gzip, 2.5 MB)

## Timeline

### cl...@chromium.org (2015-03-13)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5763872108052480

### cl...@chromium.org (2015-03-13)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5763872108052480

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x7f68b0242000
Crash State:
  sk_memset32_SSE2
  SkBitmap::internalErase
  SkBitmap::eraseARGB
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94LMDAYSLVNaa2p1b0bnHnqVdqwXsPTRF5zSJ4JYqzbaVAJbDo59Qt7h8KEVznbu2JqoHBWNHvHC6UhRMh3EeneUI6jq9b2Qq_tDq9Gi5Y-4ryHQDd88-a-iP5Q8qvBHzvYUC7CkmCbHyKQ0fQDFkLG7JYK_lbKUOuZQXf3qTBKMB1Rt20




### aa...@google.com (2015-03-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-19)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6478505005547520

Fuzzer: Cdiehl_peach
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x7fcf1eeb8000
Crash State:
  sk_memset32_SSE2
  SkBitmap::internalErase
  SkBitmap::eraseARGB
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95bYQSZjia9YiEAyKCY2GBeSymBkOjkosR2_toENr70sGLKu5kyMhHX2ZKkxcgkMNRUftkbEBfbuI0ALthEvTTeSXsiBq76s0ph0SenJypjS5KlF---38zjPrSIoVP4n81puEOc4fEoAE-3cgIusYtiEad8Ig


Additional requirements: Requires Gestures

Filer: inferno

### in...@chromium.org (2015-03-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-20)

[Empty comment from Monorail migration]

### ke...@chromium.org (2015-03-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-21)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### in...@chromium.org (2015-03-23)

Sugoi@ does not have bandwidth for skia bug fixes. Reed@, please help with owners for these.

### dx...@chromium.org (2015-03-24)

heather, can you help triage?

### cl...@chromium.org (2015-03-25)

ClusterFuzz has detected this issue as fixed in range 321780:322012.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6478505005547520

Fuzzer: Cdiehl_peach
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x7fc71325b000
Crash State:
  sk_memset32_SSE2
  SkBitmap::internalErase
  SkBitmap::eraseARGB
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=320909:321088
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=321780:322012

Minimized Testcase (0.30 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95SHSwmmSJ79p-RjwvKoYBcDOe7XPmQWfQnUiiRJEzAeZ7OUV2aIIw_xYmaBrUVzCptEUhdTICSm6cW3c3eVcCmn4Im2Zxj_ZNdzSgiCNTef4v9NvVbYBjreDJdimfIbssx9Z_sQ-zjjhw9dkZZoZslSRiI5g

Additional requirements: Requires Gestures

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2015-03-25)

This is not fixed, https://cluster-fuzz.appspot.com/testcase?key=6478505005547520 still reproduces.

### [Deleted User] (2015-03-26)

Greg, would you talk a look?

==7==ERROR: AddressSanitizer: SEGV on unknown address 0x7f88e13c3c60 (pc 0x7f8ab5fd3fd4 bp 0x7f8931ffce50 sp 0x7f8931ffcce0 T4)
    #0 0x7f8ab5fd3fd3 in convolve4RowsHorizontally_SSE2(unsigned char const**, SkConvolutionFilter1D const&, unsigned char**) third_party/skia/src/opts/SkBitmapFilter_opts_SSE2.cpp:234:13
    #1 0x7f8ab5d4bc50 in BGRAConvolve2D(unsigned char const*, int, bool, SkConvolutionFilter1D const&, SkConvolutionFilter1D const&, int, unsigned char*, SkConvolutionProcs const&, bool) third_party/skia/src/core/SkConvolver.cpp:439:17
    #2 0x7f8ab5d0f1ac in SkBitmapScaler::Resize(SkBitmap*, SkBitmap const&, SkBitmapScaler::ResizeMethod, float, float, SkBitmap::Allocator*) third_party/skia/src/core/SkBitmapScaler.cpp:302:3
    #3 0x7f8ab5cff258 in SkBitmapProcState::processHQRequest() third_party/skia/src/core/SkBitmapProcState.cpp:178:14
    #4 0x7f8ab5d00170 in SkBitmapProcState::chooseProcs(SkMatrix const&, SkPaint const&) third_party/skia/src/core/SkBitmapProcState.cpp:295:9
    #5 0x7f8ab5ce9978 in SkBitmapProcShader::onCreateContext(SkShader::ContextRec const&, void*) const third_party/skia/src/core/SkBitmapProcShader.cpp:101:10


### hc...@chromium.org (2015-03-26)

Dxie, FWIW for impact/triage I think we're addressing multiple bugs here- the original looks like it may be resolved, now focused on the crash the report in https://crbug.com/chromium/466967#c14.

### in...@chromium.org (2015-03-26)

If you are sure, let use a new bug for the new crash in c#14.

### hc...@chromium.org (2015-03-26)

Agreed, opened https://crbug.com/chromium/470980 for the second crash reported in this bug, which does look like it may be Skia.

The original does not seem to be, more on Blink side of the house perhaps, but no longer repros?

### ts...@chromium.org (2015-03-27)

Back to reed@ - close if this no longer repro's.

### ao...@gmail.com (2015-03-30)

I assumed this was a single race/uaf from threaded image decoding with multiple traces depending on what is providing the pixel data. E.g. WebP had and still has:

=================================================================
==1==ERROR: AddressSanitizer: SEGV on unknown address 0x7f69b232e988 (pc 0x7f6b4db8d4bd bp 0x7f69ec091be0 sp 0x7f69ec091bc0 T2)
    #0 0x7f6b4db8d4bc in VP8YuvToBgr /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/libwebp/dsp/./yuv.h:115
    #1 0x7f6b4db8d594 in VP8YuvToBgra /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/libwebp/dsp/./yuv.h:230
    #2 0x7f6b4db8bb0e in UpsampleBgraLinePair /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/libwebp/dsp/upsampling_sse2.c:175
    #3 0x7f6b4db397a5 in EmitFancyRGB /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/libwebp/dec/io.c:108
    #4 0x7f6b4db3784c in CustomPut /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/libwebp/dec/io.c:622
    #5 0x7f6b4db5a270 in FinishRow /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/libwebp/dec/frame.c:325
    #6 0x7f6b4db5753e in VP8ProcessRow /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/libwebp/dec/frame.c:3
[...]

Should those be filed separately?

### hc...@chromium.org (2015-03-30)

aohelin, thanks for the info.

I need Chromium/Blink help to get this to the right place for decoding experts.  reed@ shouldn't be the owner.. he finished his triage for Skia (and is also out).  Though there was an earlier comment about "skia bug fixes" AFAIK, Chromium is using its own set of decoders vs those in Skia... so trying to help this along but don't think we (Skia) can do much here.

### js...@chromium.org (2015-03-31)

reveman@ - This appears to be fallout from multithreading in the compositor. I'm adding you based on recent git blame in the stack. If you wouldn't be a good owner, maybe you have suggestions on who would be?

### re...@chromium.org (2015-03-31)

The crash report in #14 looks like https://crbug.com/chromium/468785 and 471246. Those issues have been fixed in ToT. Not sure about the crash reported in #20 yet. I'll try to reproduce that using the steps in the description of the bug.

### re...@chromium.org (2015-03-31)

I was not able to reproduce this with ToT using the instructions in the description.

### re...@chromium.org (2015-03-31)

I'm seeing this log message each time I load that page:
Warning: unknown JFIF revision number 215.215

and I saw this once:
Corrupt JPEG data: bad Huffman code

### ao...@gmail.com (2015-03-31)

reveman@ could be a timing issue, if this is a race. Here are some other traces that pop up frequently when trying to load corrupt images like in the original repro. The repros are usually fairly repeatable. There seems to be a clear pattern of trying to fill in computed pixel data to an unknown (at least for asan) address. The log messages look similar to what I see. I can save send over a larger set that usually triggers one of these, of necessary.

=================================================================
==1==ERROR: AddressSanitizer: SEGV on unknown address 0x7f8b64e8a408 (pc 0x7f8ceec2bde8 bp 0x7f8b8e744d70 sp 0x7f8b8e744d10 T2)
    #0 0x7f8ceec2bde7 in S32_alpha_D32_filter_DX_SSE2(SkBitmapProcState const&, unsigned int const*, int, unsigned int*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/opts/SkBitmapProcState_opts_SSE2.cpp:166
    #1 0x7f8cee949fd7 in SkBitmapProcShader::BitmapProcShaderContext::shadeSpan(int, int, unsigned int*, int) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/core/SkBitmapProcShader.cpp:214
    #2 0x7f8cee99012b in SkARGB32_Shader_Blitter::blitRect(int, int, int, int) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/core/SkBlitter_ARGB32.cpp:398
    #3 0x7f8cee73e6bf in antifilldot8(int, int, int, int, SkBlitter*, bool) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/core/SkScan_Antihair.cpp:750
    #4 0x7f8cee73c9ea in antifillrect(SkRect const&, SkBlitter*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/core/SkScan_Antihair.cpp:837
    #5 0x7f8cee73c665 in SkScan::AntiFillRect(SkRect const&, SkRegion const*, SkBlitter*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/core/SkScan_Antihair.cpp:860


==1==ERROR: AddressSanitizer: SEGV on unknown address 0x7fa4e5aebda0 (pc 0x7fa66f9dca96 bp 0x7fa50e1c3ac0 sp 0x7fa50e1c3980 T3)
    #0 0x7fa66f9dca95 in S32A_Opaque_BlitRow32_SSE2(unsigned int*, unsigned int const*, int, unsigned int) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/opts/SkBlitRow_opts_SSE2.cpp:154
    #1 0x7fa66f795058 in Sprite_D32_S32::blitRect(int, int, int, int) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/core/SkSpriteBlitter_ARGB32.cpp:48
    #2 0x7fa66f4df4d1 in SkScan::FillIRect(SkIRect const&, SkRegion const*, SkBlitter*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/core/SkScan.cpp:30
    #3 0x7fa66f4dfdb0 in SkScan::FillIRect(SkIRect const&, SkRasterClip const&, SkBlitter*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/core/SkScan.cpp:73
    #4 0x7fa66f3f4045 in SkDraw::drawBitmap(SkBitmap const&, SkMatrix const&, SkRect const*, SkPaint const&) const /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/core/SkDraw.cpp:1291
    #5 0x7fa66f6ef2e2 in SkBitmapDevice::drawBitmapRect(SkDraw const&, SkBitmap const&, SkRect const*, SkRect const&, SkPaint const&, SkCanvas::DrawBitmapRectFlags) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/core/SkBitmapDevice.cpp:294
    #6 0x7fa66f3c9865 in SkCanvas::internalDrawBitmapRect(SkBitmap const&, SkRect const*, SkRect const&, SkPaint const*, SkCanvas::DrawBitmapRectFlags) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/core/SkCanvas.cpp:1909


==1==ERROR: AddressSanitizer: SEGV on unknown address 0x7ff6a1e3e000 (pc 0x7ff83066a60d bp 0x7ff6cd9bbd60 sp 0x7ff6cd9bbd30 T3)
    #0 0x7ff83066a60c in blink::ImageFrame::setRGBAPremultiply(unsigned int*, unsigned int, unsigned int, unsigned int, unsigned int) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/image-decoders/ImageFrame.h:188
    #1 0x7ff830695a19 in blink::PNGImageDecoder::rowAvailable(unsigned char*, unsigned int, int) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/image-decoders/png/PNGImageDecoder.cpp:491
    #2 0x7ff82f415db8 in wk_png_push_have_row /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/libpng/pngpread.c:1731
    #3 0x7ff82f41462a in wk_png_push_process_row /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/libpng/pngpread.c:1133
    #4 0x7ff82f413972 in wk_png_process_IDAT_data /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/libpng/pngpread.c:916
    #5 0x7ff82f411c80 in wk_png_push_read_IDAT /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/libpng/pngpread.c:810
    #6 0x7ff82f40fe8e in wk_png_process_some_data /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/libpng/pngpread.c:70
    #7 0x7ff82f40fbe4 in wk_png_process_data /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/libpng/pngpread.c:41



### cl...@chromium.org (2015-04-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-15)

reveman@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### re...@chromium.org (2015-04-28)

This was fixed by https://codereview.chromium.org/1057493005

### am...@chromium.org (2015-04-28)

Is there a merge required here?

### re...@chromium.org (2015-04-28)

Nope. Fix landed before branch point.

### cl...@chromium.org (2015-04-28)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-04-28)

No m42 merge needed ??

### re...@chromium.org (2015-04-29)

M42 uses the old ashmem implemenation so this problem doesn't affect it.

### ti...@google.com (2015-05-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-06-14)

Congratulations - $1000 for this report.

We'll start payment via our new process, which should take 1-2 weeks. That 1-2 week period payment time frame starts from when you see the "reward-inprocess" label on this bug.

### ti...@google.com (2015-06-25)

[Empty comment from Monorail migration]

### ti...@google.com (2015-07-24)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

(Note: sorry for the delay here - it turns out in the new payment system, these payments were waiting for a second approval from me).

### cl...@chromium.org (2015-08-04)

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

This issue was migrated from crbug.com/chromium/466967?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081608)*
