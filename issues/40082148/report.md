# Heap-buffer-overflow in convolve4RowsHorizontally_SSE2

| Field | Value |
|-------|-------|
| **Issue ID** | [40082148](https://issues.chromium.org/issues/40082148) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Reporter** | cl...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2015-05-24 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached testcase crashes filter\_fuzz\_stub 32 and 64-bit build. ASAN output on 32-bit below (64-bit attached):

# [0524/111558:INFO:filter\_fuzz\_stub.cc(60)] Test case: repro.fil [0524/111558:INFO:filter\_fuzz\_stub.cc(37)] Valid stream detected.

==17502==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xe2700198 at pc 0x0894fe17 bp 0xffd2c7c8 sp 0xffd2c7c0  

WRITE of size 4 at 0xe2700198 thread T0  

#0 0x894fe16 in convolve4RowsHorizontally\_SSE2(unsigned char const\*\*, SkConvolutionFilter1D const&, unsigned char\*\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/opts/SkBitmapFilter\_opts\_SSE2.cpp:278  

#1 0x854d40b in BGRAConvolve2D(unsigned char const\*, int, bool, SkConvolutionFilter1D const&, SkConvolutionFilter1D const&, int, unsigned char\*, SkConvolutionProcs const&, bool) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkConvolver.cpp:439  

#2 0x850c17e in SkBitmapScaler::Resize(SkBitmap\*, SkBitmap const&, SkBitmapScaler::ResizeMethod, float, float, SkBitmap::Allocator\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkBitmapScaler.cpp:302  

#3 0x84f9256 in SkBitmapProcState::processHQRequest() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkBitmapProcState.cpp:152  

#4 0x84fa33b in SkBitmapProcState::chooseProcs(SkMatrix const&, SkPaint const&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkBitmapProcState.cpp:273  

#5 0x84e23a0 in SkBitmapProcShader::onCreateContext(SkShader::ContextRec const&, void\*) const /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkBitmapProcShader.cpp:101  

#6 0x82fa29c in SkShader::createContext(SkShader::ContextRec const&, void\*) const /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkShader.cpp:92  

#7 0x851765d in SkBlitter::Choose(SkBitmap const&, SkMatrix const&, SkPaint const&, SkSmallAllocator<3u, 1024u>\*, bool) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkBlitter.cpp:927  

#8 0x81f2f04 in SkAutoBlitterChoose::SkAutoBlitterChoose(SkBitmap const&, SkMatrix const&, SkPaint const&, bool) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkDraw.cpp:49  

#9 0x81f960b in SkDraw::drawRect(SkRect const&, SkPaint const&, SkMatrix const\*, SkRect const\*) const /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkDraw.cpp:859  

#10 0x81f858a in SkDraw::drawRect(SkRect const&, SkPaint const&) const /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/include/core/SkDraw.h:40  

#11 0x81fe285 in SkDraw::drawBitmap(SkBitmap const&, SkMatrix const&, SkRect const\*, SkPaint const&) const /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkDraw.cpp:1307  

#12 0x84da959 in SkBitmapDevice::drawBitmap(SkDraw const&, SkBitmap const&, SkMatrix const&, SkPaint const&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkBitmapDevice.cpp:226  

#13 0x81bc041 in SkCanvas::internalDrawBitmap(SkBitmap const&, SkMatrix const&, SkPaint const\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:1204  

#14 0x81cb97d in SkCanvas::onDrawBitmap(SkBitmap const&, float, float, SkPaint const\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:2039  

#15 0x81bf9e2 in SkCanvas::drawBitmap(SkBitmap const&, float, float, SkPaint const\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:1753  

#16 0x82404e0 in SkMatrixImageFilter::onFilterImage(SkImageFilter::Proxy\*, SkBitmap const&, SkImageFilter::Context const&, SkBitmap\*, SkIPoint\*) const /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkMatrixImageFilter.cpp:86  

#17 0x821b2e3 in SkImageFilter::filterImage(SkImageFilter::Proxy\*, SkBitmap const&, SkImageFilter::Context const&, SkBitmap\*, SkIPoint\*) const /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkImageFilter.cpp:189  

#18 0x81bae5a in SkCanvas::internalDrawDevice(SkBaseDevice\*, int, int, SkPaint const\*, bool) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:1233  

#19 0x81b6917 in SkCanvas::internalRestore() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:1098  

#20 0x81be186 in AutoDrawLooper::~AutoDrawLooper() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:402  

#21 0x81bc175 in SkCanvas::internalDrawBitmap(SkBitmap const&, SkMatrix const&, SkPaint const\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:1208  

#22 0x81cb97d in SkCanvas::onDrawBitmap(SkBitmap const&, float, float, SkPaint const\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:2039  

#23 0x81bf9e2 in SkCanvas::drawBitmap(SkBitmap const&, float, float, SkPaint const\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:1753  

#24 0x8123cfd in RunTestCase /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:47  

#25 0x8122f39 in ReadAndRunTestCase /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:66  

#26 0x81229f2 in main /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:85  

#27 0xf6be1a82 in \_\_libc\_start\_main ??:?

0xe2700198 is located 0 bytes to the right of 8-byte region [0xe2700190,0xe2700198)  

allocated by thread T0 here:  

#0 0x80ff393 in **interceptor\_malloc ??:?  

#1 0x897b94b in sk\_malloc\_throw(unsigned int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized*/build/src/out/Release/../../skia/ext/SkMemory\_new\_handler.cpp:50  

#2 0x845d916 in SkTArray<unsigned char, false>::checkRealloc(int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized*/build/src/out/Release/../../third\_party/skia/include/core/SkTArray.h:453  

#3 0x8459b2e in SkTArray<unsigned char, false>::reset(int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/include/core/SkTArray.h:134  

#4 0x854dfd1 in (anonymous namespace)::CircularRowBuffer::CircularRowBuffer(int, int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkConvolver.cpp:40  

#5 0x854cf97 in BGRAConvolve2D(unsigned char const\*, int, bool, SkConvolutionFilter1D const&, SkConvolutionFilter1D const&, int, unsigned char\*, SkConvolutionProcs const&, bool) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkConvolver.cpp:396  

#6 0x850c17e in SkBitmapScaler::Resize(SkBitmap\*, SkBitmap const&, SkBitmapScaler::ResizeMethod, float, float, SkBitmap::Allocator\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkBitmapScaler.cpp:302  

#7 0x84f9256 in SkBitmapProcState::processHQRequest() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkBitmapProcState.cpp:152  

#8 0x84fa33b in SkBitmapProcState::chooseProcs(SkMatrix const&, SkPaint const&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkBitmapProcState.cpp:273  

#9 0x84e23a0 in SkBitmapProcShader::onCreateContext(SkShader::ContextRec const&, void\*) const /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkBitmapProcShader.cpp:101  

#10 0x82fa29c in SkShader::createContext(SkShader::ContextRec const&, void\*) const /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkShader.cpp:92  

#11 0x851765d in SkBlitter::Choose(SkBitmap const&, SkMatrix const&, SkPaint const&, SkSmallAllocator<3u, 1024u>\*, bool) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkBlitter.cpp:927  

#12 0x81f2f04 in SkAutoBlitterChoose::SkAutoBlitterChoose(SkBitmap const&, SkMatrix const&, SkPaint const&, bool) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkDraw.cpp:49  

#13 0x81f960b in SkDraw::drawRect(SkRect const&, SkPaint const&, SkMatrix const\*, SkRect const\*) const /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkDraw.cpp:859  

#14 0x81f858a in SkDraw::drawRect(SkRect const&, SkPaint const&) const /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/include/core/SkDraw.h:40  

#15 0x81fe285 in SkDraw::drawBitmap(SkBitmap const&, SkMatrix const&, SkRect const\*, SkPaint const&) const /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkDraw.cpp:1307  

#16 0x84da959 in SkBitmapDevice::drawBitmap(SkDraw const&, SkBitmap const&, SkMatrix const&, SkPaint const&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkBitmapDevice.cpp:226  

#17 0x81bc041 in SkCanvas::internalDrawBitmap(SkBitmap const&, SkMatrix const&, SkPaint const\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:1204  

#18 0x81cb97d in SkCanvas::onDrawBitmap(SkBitmap const&, float, float, SkPaint const\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:2039  

#19 0x81bf9e2 in SkCanvas::drawBitmap(SkBitmap const&, float, float, SkPaint const\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:1753  

#20 0x82404e0 in SkMatrixImageFilter::onFilterImage(SkImageFilter::Proxy\*, SkBitmap const&, SkImageFilter::Context const&, SkBitmap\*, SkIPoint\*) const /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkMatrixImageFilter.cpp:86  

#21 0x821b2e3 in SkImageFilter::filterImage(SkImageFilter::Proxy\*, SkBitmap const&, SkImageFilter::Context const&, SkBitmap\*, SkIPoint\*) const /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkImageFilter.cpp:189  

#22 0x81bae5a in SkCanvas::internalDrawDevice(SkBaseDevice\*, int, int, SkPaint const\*, bool) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:1233  

#23 0x81b6917 in SkCanvas::internalRestore() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:1098  

#24 0x81be186 in AutoDrawLooper::~AutoDrawLooper() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:402  

#25 0x81bc175 in SkCanvas::internalDrawBitmap(SkBitmap const&, SkMatrix const&, SkPaint const\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:1208  

#26 0x81cb97d in SkCanvas::onDrawBitmap(SkBitmap const&, float, float, SkPaint const\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:2039  

#27 0x81bf9e2 in SkCanvas::drawBitmap(SkBitmap const&, float, float, SkPaint const\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:1753  

#28 0x8123cfd in RunTestCase /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:47  

#29 0x8122f39 in ReadAndRunTestCase /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:66

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/nils/MonkeyChrome/asan-symbolized-v8-arm-linux-release-330758/filter\_fuzz\_stub+0x894fe16)  

Shadow bytes around the buggy address:  

0x3c4dffe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x3c4dfff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x3c4e0000: fa fa 00 fa fa fa 00 fa fa fa 00 fa fa fa 00 fa  

0x3c4e0010: fa fa 00 fa fa fa 00 fa fa fa 00 fa fa fa 00 fa  

0x3c4e0020: fa fa 00 fa fa fa 00 fa fa fa 00 fa fa fa 00 fa  

=>0x3c4e0030: fa fa 00[fa]fa fa 00 fa fa fa 00 fa fa fa fa fa  

0x3c4e0040: fa fa 00 fa fa fa 00 fa fa fa fa fa fa fa 00 fa  

0x3c4e0050: fa fa 00 fa fa fa fa fa fa fa 00 fa fa fa 00 fa  

0x3c4e0060: fa fa 00 fa fa fa 00 fa fa fa 00 fa fa fa 00 fa  

0x3c4e0070: fa fa 00 fa fa fa 00 fa fa fa 00 fa fa fa 00 fa  

0x3c4e0080: fa fa 00 fa fa fa 00 fa fa fa 00 fa fa fa 00 fa  

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

==17502==ABORTING

**VERSION**  

Chrome Version: asan-symbolized-linux-release-331246

**REPRODUCTION CASE**  

Attached as repro.fil

## Attachments

- [repro.fil](attachments/repro.fil) (application/octet-stream, 96 B)
- [debug64.txt](attachments/debug64.txt) (text/plain, 6.2 KB)

## Timeline

### in...@chromium.org (2015-05-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-02)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6242246811189248

### cl...@chromium.org (2015-06-02)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4731848077344768

Uploader: ochang@google.com
Job Type: Linux_asan_filter_fuzz_stub_32bit

Crash Type: Heap-buffer-overflow WRITE 4
Crash Address: 0xe3302cf8
Crash State:
  convolve4RowsHorizontally_SSE2
  BGRAConvolve2D
  SkBitmapScaler::Resize
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97efWGC1twJQJaIVl4T_GF-jKzLzjgJrq-HtMqDIgrq0ZWKOPiNU-Ohn0H1W8Bwm9KxGZbRFR1Dsd8rlpWdcbdQD8H1kvSVfGlXagcJ9HUWS7dnd0OOhB4-XZMUsnmqjDK98mmfegslBDgVkBG2FPXKd3_-Zg


Filer: ochang

### oc...@chromium.org (2015-06-02)

@reed, mtklein@, the crash stack here seems very similar to https://crbug.com/491891, and is reproducing today even after https://codereview.chromium.org/1159793003/. Could you please take a look?

### cl...@chromium.org (2015-06-02)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4731848077344768

Uploader: ochang@google.com
Job Type: Linux_asan_filter_fuzz_stub_32bit

Crash Type: Heap-buffer-overflow WRITE 4
Crash Address: 0xe3302cf8
Crash State:
  convolve4RowsHorizontally_SSE2
  BGRAConvolve2D
  SkBitmapScaler::Resize
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97efWGC1twJQJaIVl4T_GF-jKzLzjgJrq-HtMqDIgrq0ZWKOPiNU-Ohn0H1W8Bwm9KxGZbRFR1Dsd8rlpWdcbdQD8H1kvSVfGlXagcJ9HUWS7dnd0OOhB4-XZMUsnmqjDK98mmfegslBDgVkBG2FPXKd3_-Zg




### cl...@chromium.org (2015-06-02)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4731848077344768

Uploader: ochang@google.com
Job Type: Linux_asan_filter_fuzz_stub_32bit

Crash Type: Heap-buffer-overflow WRITE 4
Crash Address: 0xe3302cf8
Crash State:
  convolve4RowsHorizontally_SSE2
  BGRAConvolve2D
  SkBitmapScaler::Resize
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97efWGC1twJQJaIVl4T_GF-jKzLzjgJrq-HtMqDIgrq0ZWKOPiNU-Ohn0H1W8Bwm9KxGZbRFR1Dsd8rlpWdcbdQD8H1kvSVfGlXagcJ9HUWS7dnd0OOhB4-XZMUsnmqjDK98mmfegslBDgVkBG2FPXKd3_-Zg




### cl...@chromium.org (2015-06-03)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-06-03)

Verified locally that this impacts stable.

### cl...@chromium.org (2015-06-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-07)

mtklein@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ti...@google.com (2015-06-15)

@mtklein - can you please provide an update? (even if that update is no progress).

### [Deleted User] (2015-06-18)

Sorry, got confused by a flurry of these.  Thought this was fixed.  I will start looking at this today.

### [Deleted User] (2015-06-18)

I agree with #5, this looks like the same issue.  Going to dedup the bugs for now while I look at this, assuming they're the same.

### [Deleted User] (2015-06-18)

Actually, let me take that back.  I think the issue in #5 is a somewhat different issue probably fixed by Mike's CL mentioned there.  It was dereferencing a null source bitmap, where this looks like we're running off the end of a temporary buffer we've created.

### [Deleted User] (2015-06-18)

I suspect this is not a recent regression.  I don't see anything obviously wrong, but this code is pretty complicated.  I'm going to start thinking it through ground up to see if I can figure things out that way.  May take a while.

### ti...@google.com (2015-06-18)

No worries - thanks for the update. Good luck!

### bu...@chromium.org (2015-06-18)

The following revision refers to this bug:
  https://skia.googlesource.com/skia.git/+/cd08effd005225915c7516883f658f21dbd82292

commit cd08effd005225915c7516883f658f21dbd82292
Author: mtklein <mtklein@chromium.org>
Date: Thu Jun 18 17:30:32 2015

Plumb through out_row byte length so we can assert we stay underneath it.

Sadly, not asserting for me yet.  Can't hurt.

BUG=chromium:491660

Review URL: https://codereview.chromium.org/1187173005

[modify] http://crrev.com/cd08effd005225915c7516883f658f21dbd82292/src/core/SkConvolver.cpp
[modify] http://crrev.com/cd08effd005225915c7516883f658f21dbd82292/src/core/SkConvolver.h
[modify] http://crrev.com/cd08effd005225915c7516883f658f21dbd82292/src/opts/SkBitmapFilter_opts_SSE2.cpp
[modify] http://crrev.com/cd08effd005225915c7516883f658f21dbd82292/src/opts/SkBitmapFilter_opts_SSE2.h
[modify] http://crrev.com/cd08effd005225915c7516883f658f21dbd82292/src/opts/SkBitmapProcState_arm_neon.cpp


### cl...@chromium.org (2015-07-03)

mtklein@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-07-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-17)

mtklein@: Uh oh! This issue is still open and hasn't been updated in the last 28 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-07-24)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### [Deleted User] (2015-07-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-25)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-08-21)

[Empty comment from Monorail migration]

### ti...@google.com (2015-08-30)

@mtklein - old bug is old. Any luck with the CL in #18? High severity bugs in Stable are not good, and this was reported to us months ago. I understand that this one is tricky, but grateful if you could take another crack at this.


### [Deleted User] (2015-08-31)

To my knowledge the assertions in #18 have not triggered.

I will try to circle around on figuring this out.  Don't know if this will make you feel any better, but this has probably been in stable for years and years.

### ti...@google.com (2015-09-23)

#27: That's what keeps me awake at night :)

Any luck figuring this one out? Anything reasonable we can do help you get to the bottom of it?

### cl...@chromium.org (2015-10-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-13)

ClusterFuzz has detected this issue as fixed in range 351896:351913.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4731848077344768

Uploader: ochang@google.com
Job Type: linux_asan_filter_fuzz_stub_32bit
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE 4
Crash Address: 0xe3302cf8
Crash State:
  convolve4RowsHorizontally_SSE2
  BGRAConvolve2D
  SkBitmapScaler::Resize
  
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=351896:351913

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97efWGC1twJQJaIVl4T_GF-jKzLzjgJrq-HtMqDIgrq0ZWKOPiNU-Ohn0H1W8Bwm9KxGZbRFR1Dsd8rlpWdcbdQD8H1kvSVfGlXagcJ9HUWS7dnd0OOhB4-XZMUsnmqjDK98mmfegslBDgVkBG2FPXKd3_-Zg


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### [Deleted User] (2015-10-14)

(I think that last ClusterFuzz message may be wishful thinking.)

### oc...@chromium.org (2015-10-14)

Have you been able to reproduce this?

### [Deleted User] (2015-10-14)

Haven't tried, but we certainly also haven't done anything to fix it.

### cl...@chromium.org (2015-11-06)

ClusterFuzz has detected this issue as fixed in range 350168:350186.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4731848077344768

Uploader: ochang@google.com
Job Type: linux_asan_filter_fuzz_stub_32bit
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE 4
Crash Address: 0xe3302cf8
Crash State:
  convolve4RowsHorizontally_SSE2
  BGRAConvolve2D
  SkBitmapScaler::Resize
  
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=350168:350186

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97efWGC1twJQJaIVl4T_GF-jKzLzjgJrq-HtMqDIgrq0ZWKOPiNU-Ohn0H1W8Bwm9KxGZbRFR1Dsd8rlpWdcbdQD8H1kvSVfGlXagcJ9HUWS7dnd0OOhB4-XZMUsnmqjDK98mmfegslBDgVkBG2FPXKd3_-Zg


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### in...@chromium.org (2015-11-10)

Cf detected as fixed and we don't see new variants, closing.

### cl...@chromium.org (2015-11-10)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### ti...@google.com (2015-11-23)

Marking speculatively as Release-0-M47 based on CF fixed ranges all being sub r352221

### ti...@google.com (2015-12-01)

Congrats cloudfuzzer - $5000 for this report. We'll start processing payment later this week. 

### ti...@google.com (2015-12-14)

[Empty comment from Monorail migration]

### ti...@google.com (2016-01-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-17)

This security bug has been closed for more than 14 weeks. Removing view restrictions.

- Your friendly ClusterFuzz

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/491660?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082148)*
