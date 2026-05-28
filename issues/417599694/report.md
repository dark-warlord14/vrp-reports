# OOB read in skia::BGRAConvolve2D

| Field | Value |
|-------|-------|
| **Issue ID** | [417599694](https://issues.chromium.org/issues/417599694) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Platforms** | Linux, ChromeOS |
| **Chrome Version** | 137.0.7122.0 |
| **Reporter** | vm...@gmail.com |
| **Assignee** | kj...@google.com |
| **Created** | 2025-05-14 |
| **Bounty** | $3,000.00 |

## Description

# Steps to reproduce the problem

1. ./image\_operations\_resize\_fuzzer\_\_better ./out\_better1crash-a849b610d97bc4bf8be154b2d226a4353b8fd93e

# Problem Description

In `skia::ImageOperations::Resize` of `VizCompositorTh` process, `source_byte_row_stride` in `skia::BGRAConvolve2D` can larger than `source_byte_row_stride`, causing heap-buffer-overflow in `skia::Convolve4RowsHorizontally_SSE2`[1] and `skia::ConvolveHorizontally_SSE2`[2]. ImageOperations::Resize is a regular operation in renderer process, and through calling of viz/service/display/software\_renderer.cc:CopyOutputRequest, this can compromise `VizCompositorTh` process.

```
void BGRAConvolve2D(const unsigned char* source_data,
                    int source_byte_row_stride,
                    bool source_has_alpha,
                    const ConvolutionFilter1D& filter_x,
                    const ConvolutionFilter1D& filter_y,
                    int output_byte_row_stride,
                    unsigned char* output,
                    bool use_simd_if_possible) {
  ConvolveProcs simd;
  simd.extra_horizontal_reads = 0;
  simd.convolve_vertically = NULL;
  simd.convolve_4rows_horizontally = NULL;
  simd.convolve_horizontally = NULL;
  if (use_simd_if_possible) {
    SetupSIMD(&simd);
  }

//...

  for (int out_y = 0; out_y < num_output_rows; out_y++) {
    filter_values = filter_y.FilterForValue(out_y,
                                            &filter_offset, &filter_length);

    // Generate output rows until we have enough to run the current filter.
    while (next_x_row < filter_offset + filter_length) {
      if (simd.convolve_4rows_horizontally &&
          next_x_row + 3 < last_filter_offset + last_filter_length -
          avoid_simd_rows) {
        const unsigned char* src[4];
        unsigned char* out_row[4];
        for (int i = 0; i < 4; ++i) {
          src[i] = &source_data[(next_x_row + i) * source_byte_row_stride];                  //<--- [1]
          out_row[i] = row_buffer.AdvanceRow();
        }
        simd.convolve_4rows_horizontally(src, filter_x, out_row);
        next_x_row += 4;
      } else {
        // Check if we need to avoid SSE2 for this row.
        if (simd.convolve_horizontally &&
            next_x_row < last_filter_offset + last_filter_length -
            avoid_simd_rows) {
          simd.convolve_horizontally(                                                       //<--- [2]
              &source_data[next_x_row * source_byte_row_stride],
              filter_x, row_buffer.AdvanceRow(), source_has_alpha);
        } else {

```
```
─── Breakpoints ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
[1] break at 0x00007ffff313874f in ../../skia/ext/convolver.cc:475 for ../../skia/ext/convolver.cc:475 hit 1 time
─── Expressions ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
─── History ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
─── Memory ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
─── Registers ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    rax 0x00007bffe71e7110    rbx 0x00007fffffffcee0       rcx 0x000000000000025d    rdx 0x4000000000000000    rsi 0x003ffff989c3977e
    rdi 0x000055555619ae00    rbp 0x00007fffffffd180       rsp 0x00007fffffffcee0     r8 0x0000010000000000     r9 0x00007fffffffff01
    r10 0x0000000000001f01    r11 0x0000000000000001       r12 0x0000555555624ca0    r13 0x00007fffffffdc50    r14 0x00007c3fe81e08f0
    r15 0x00007bffe72e1a50    rip 0x00007ffff313874f    eflags [ CF PF AF SF IF ]     cs 0x00000033             ss 0x0000002b        
     ds 0x00000000             es 0x00000000                fs 0x00000000             gs 0x00000000        
─── Source ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
Cannot display "convolver.cc"
─── Stack ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
[0] from 0x00007ffff313874f in skia::BGRAConvolve2D(unsigned char const*, int, bool, skia::ConvolutionFilter1D const&, skia::ConvolutionFilter1D const&, int, unsigned char*, bool)+1727 at ../../skia/ext/convolver.cc:475
[1] from 0x00007ffff316c95b in skia::ImageOperations::Resize(SkPixmap const&, skia::ImageOperations::ResizeMethod, int, int, SkIRect const&, SkBitmap::Allocator*)+2731 at ../../skia/ext/image_operations.cc:378
[2] from 0x000055555570c11d in LLVMFuzzerTestOneInput(uint8_t const*, size_t)+1933 at ../../skia/ext/image_operations_resize_fuzzer__better.cc:101
[3] from 0x000055555578d5db in fuzzer::Fuzzer::ExecuteCallback(unsigned char const*, unsigned long)+1147 at ../../third_party/libFuzzer/src/FuzzerLoop.cpp:619
[4] from 0x000055555573bb0c in fuzzer::RunOneTest(fuzzer::Fuzzer*, char const*, unsigned long)+460 ```

# Additional Comments
```patch
diff --git a/skia/ext/convolver.cc b/skia/ext/convolver.cc
index b77fcdb165309..59519fa1ab970 100644
--- a/skia/ext/convolver.cc
+++ b/skia/ext/convolver.cc
@@ -439,6 +439,7 @@ void BGRAConvolve2D(const unsigned char* source_data,
   // Loop over every possible output row, processing just enough horizontal
   // convolutions to run each subsequent vertical convolution.
   SkASSERT(output_byte_row_stride >= filter_x.num_values() * 4);
+  SkASSERT(source_byte_row_stride < output_byte_row_stride);
   int num_output_rows = filter_y.num_values();

```
```
Running: ./out_better1crash-a849b610d97bc4bf8be154b2d226a4353b8fd93e
[0514/161817.940809:FATAL:skia/ext/convolver.cc:442] check(source_byte_row_stride < output_byte_row_stride)
#0 0x5628ff98e806 <unknown>
#1 0x7f5e0acbcd70 <unknown>
#2 0x7f5e0ab9dd62 <unknown>

```
# Summary

OOB read in skia::BGRAConvolve2D

# Custom Questions

#### Type of crash:

VizCompositorTh

#### Crash state:

```
#6526	REDUCE cov: 37 ft: 28 corp: 19/480b lim: 43 exec/s: 0 rss: 121Mb L: 39/39 MS: 2 ChangeASCIIInt-EraseBytes-
#7319	REDUCE cov: 37 ft: 28 corp: 19/479b lim: 48 exec/s: 0 rss: 121Mb L: 38/38 MS: 3 InsertByte-ChangeByte-EraseBytes-
=================================================================
==3824374==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7b787d1071b0 at pc 0x560bb534fd07 bp 0x7ffc8448c700 sp 0x7ffc8448c6f8
READ of size 16 at 0x7b787d1071b0 thread T0
    #0 0x560bb534fd06 in skia::Convolve4RowsHorizontally_SSE2(unsigned char const**, skia::ConvolutionFilter1D const&, unsigned char**) skia/ext/convolver_SSE2.cc:212:7
    #1 0x560bb534b8e6 in skia::BGRAConvolve2D(unsigned char const*, int, bool, skia::ConvolutionFilter1D const&, skia::ConvolutionFilter1D const&, int, unsigned char*, bool) skia/ext/convolver.cc:478:9
    #2 0x560bb5343739 in skia::ImageOperations::Resize(SkPixmap const&, skia::ImageOperations::ResizeMethod, int, int, SkIRect const&, SkBitmap::Allocator*) skia/ext/image_operations.cc:378:3
    #3 0x560bb391933a in LLVMFuzzerTestOneInput skia/ext/image_operations_resize_fuzzer__better.cc:101:7
    #4 0x560bb395866c in fuzzer::Fuzzer::ExecuteCallback(unsigned char const*, unsigned long) third_party/libFuzzer/src/FuzzerLoop.cpp:619:13
    #5 0x560bb3957538 in fuzzer::Fuzzer::RunOne(unsigned char const*, unsigned long, bool, fuzzer::InputInfo*, bool, bool*) third_party/libFuzzer/src/FuzzerLoop.cpp:516:7
    #6 0x560bb395ab67 in fuzzer::Fuzzer::MutateAndTestOne() third_party/libFuzzer/src/FuzzerLoop.cpp:765:19
    #7 0x560bb395c9ba in fuzzer::Fuzzer::Loop(std::__Cr::vector<fuzzer::SizedFile, std::__Cr::allocator<fuzzer::SizedFile>>&) third_party/libFuzzer/src/FuzzerLoop.cpp:910:5
    #8 0x560bb39333a4 in fuzzer::FuzzerDriver(int*, char***, int (*)(unsigned char const*, unsigned long)) third_party/libFuzzer/src/FuzzerDriver.cpp:915:6
    #9 0x560bb39198b5 in main third_party/libFuzzer/src/FuzzerMain.cpp:20:10
    #10 0x7f387de14082 in __libc_start_main /build/glibc-FcRMwW/glibc-2.31/csu/../csu/libc-start.c:308:16

0x7b787d1071b0 is located 242 bytes after 46-byte region [0x7b787d107090,0x7b787d1070be)
allocated by thread T0 here:
    #0 0x560bb3917a0d in operator new[](unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:89:3
    #1 0x560bb3958418 in fuzzer::Fuzzer::ExecuteCallback(unsigned char const*, unsigned long) third_party/libFuzzer/src/FuzzerLoop.cpp:601:23
    #2 0x560bb3957538 in fuzzer::Fuzzer::RunOne(unsigned char const*, unsigned long, bool, fuzzer::InputInfo*, bool, bool*) third_party/libFuzzer/src/FuzzerLoop.cpp:516:7
    #3 0x560bb395ab67 in fuzzer::Fuzzer::MutateAndTestOne() third_party/libFuzzer/src/FuzzerLoop.cpp:765:19
    #4 0x560bb395c9ba in fuzzer::Fuzzer::Loop(std::__Cr::vector<fuzzer::SizedFile, std::__Cr::allocator<fuzzer::SizedFile>>&) third_party/libFuzzer/src/FuzzerLoop.cpp:910:5
    #5 0x560bb39333a4 in fuzzer::FuzzerDriver(int*, char***, int (*)(unsigned char const*, unsigned long)) third_party/libFuzzer/src/FuzzerDriver.cpp:915:6
    #6 0x560bb39198b5 in main third_party/libFuzzer/src/FuzzerMain.cpp:20:10
    #7 0x7f387de14082 in __libc_start_main /build/glibc-FcRMwW/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-buffer-overflow skia/ext/convolver_SSE2.cc:212:7 in skia::Convolve4RowsHorizontally_SSE2(unsigned char const**, skia::ConvolutionFilter1D const&, unsigned char**)
Shadow bytes around the buggy address:
  0x7b787d106f00: fa fa fd fd fd fd fd fa fa fa fd fd fd fd fd fd
  0x7b787d106f80: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fd
  0x7b787d107000: fa fa fd fd fd fd fd fa fa fa fd fd fd fd fd fa
  0x7b787d107080: fa fa 00 00 00 00 00 06 fa fa fa fa fa fa fa fa
  0x7b787d107100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x7b787d107180: fa fa fa fa fa fa[fa]fa fa fa fa fa fa fa fa fa
  0x7b787d107200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b787d107280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b787d107300: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b787d107380: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b787d107400: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==3824374==ABORTING
MS: 1 PersAutoDict- DE: "\034\000\000\000\000\000\000\000"-; base unit: 3acaf8e9917854385c881681874a2b4fa25c52dd
0xa,0xa,0x47,0x47,0x47,0x47,0x47,0x47,0x47,0x0,0xa,0x0,0x4,0x0,0x1c,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0xb6,0x0,0x0,0x0,0x7a,0x98,0x0,0x0,0xd3,0x41,0x0,0x0,0xff,0xff,0x0,0x34,0x2d,0x30,0x47,0x98,0xf7,0x61,
\012\012GGGGGGG\000\012\000\004\000\034\000\000\000\000\000\000\000\000\000\266\000\000\000z\230\000\000\323A\000\000\377\377\0004-0G\230\367a
artifact_prefix='./out_better1'; Test unit written to ./out_better1crash-a849b610d97bc4bf8be154b2d226a4353b8fd93e
Base64: CgpHR0dHR0dHAAoABAAcAAAAAAAAAAAAtgAAAHqYAADTQQAA//8ANC0wR5j3YQ==

```
#### Reporter credit:

/

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- out_better1crash-a849b610d97bc4bf8be154b2d226a4353b8fd93e (application/octet-stream, 46 B)
- image_operations_resize_fuzzer__better (application/x-sharedlib, 8.2 MB)
- image_operations_resize_fuzzer__better.cc (text/x-c++src, 2.0 KB)
- logv142.asan (application/octet-stream, 15.1 KB)
- poc.zip (application/zip, 803.7 KB)
- repro.webm (video/webm, 6.3 MB)

## Timeline

### vm...@gmail.com (2025-05-14)

adding a fuzzer.

### vm...@gmail.com (2025-05-14)

Correcting patch, `*source_subset` should have a length check.

```
https://source.chromium.org/chromium/chromium/src/+/main:skia/ext/image_operations.cc;drc=6b88a2263df38beeedf1ccdd141b698f51405f39;l=368
  // Get a source bitmap encompassing this touched area. We construct the
  // offsets and row strides such that it looks like a new bitmap, while
  // referring to the old data.
  const uint8_t* source_subset =
      reinterpret_cast<const uint8_t*>(source.addr());
(gdb)
372	in ../../skia/ext/image_operations.cc
>>> p source_subset
$5 = (const uint8_t *) 0x7c3fe81e08f0 ""

```

### me...@google.com (2025-05-15)

hcm: Could you PTAL? I haven't reproduced this yet, and the severity level is tentative (OOB read in renderer = medium according to <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md#toc-medium-severity>). Thanks!

### me...@google.com (2025-05-16)

Tentatively setting FoundIn to current stable - I haven't been able to repro. hcm: Please adjust as necessary.

### ch...@google.com (2025-05-16)

Setting milestone because of s2 severity.

### ch...@google.com (2025-05-16)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ma...@google.com (2025-05-28)

[secondary shepherd] I pinged hcm@

### ch...@google.com (2025-06-12)

danieldilan: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### da...@google.com (2025-06-13)

I am able to reproduce the crash with the fuzzer provided by the reporter. I think the reporter is correct in that the issue is that the size in SkImageInfo is larger than memory actually allocated. I can recreate the crash with a test case [1], but given that skia::ImageOperations::Resize() only takes a SkPixmap, we can't verify the amount of data allocated and that must be done higher up in the call stack. @fm...@google.com any idea who would be best for this, or who would be familiar with this code?

[1] https://chromium-review.googlesource.com/c/chromium/src/+/6637899

### fm...@google.com (2025-06-20)

I tend to agree, I'm seeing issues with the fuzzer itself (`image_operations_resize_fuzzer__better.cc`) performing insufficient validation and passing bad inputs.

Values extracted from `out_better1crash-a849b610d97bc4bf8be154b2d226a4353b8fd93e`

```
  data size: 46
  src: [1195837962 1195853639]
  dst: [655431 1835012]
  subset: [0 0 182 39034]`

```

(note the extremely large src dimensions)

 `const size_t rowBytes = srcW * 4;`

This overflows `int`, resulting in `488384552` instead of the expected (u64) `4783351848`.

 `const uint8_t* pixels = data + 256;`

The remaining data payload size after reading the inputs is only 14 bytes here, `pixels` is pointing into random heap space.

So the fuzzer passes invalid row bytes and invalid pixel data to `ImageOperations::Resize`. There should be additional sanity checks to reject these bad fuzzer inputs.

Note that the current `image_operations_resize_fuzzer.cc` [allocates the pixel storage explicitly](https://source.chromium.org/chromium/chromium/src/+/main:skia/ext/image_operations_resize_fuzzer.cc;l=87), which handles both issues: [rejects](https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/image/SkSurface_Raster.cpp;drc=ae6bdc3f8c34c75618c155b77bf065133d9b764a;l=54) oversized/overflowing dimensions and ensures that sufficient storage space is available.

Unless there is evidence that other Chromium code is generating similar invalid inputs, I don't think this fuzzer proves anything other than passing invalid inputs to a low-level API can make it crash.

### vm...@gmail.com (2025-06-23)

Thanks for explaining everything to me, actually I triggered this issue from a top-level ./chrome call, but lacked intermediate debug info because I couldn't reproduce it consistently. I was just wondering if there's a chance that the value of `geometry.sampling_bounds.x()` or `geometry.sampling_bounds.y()` might be bigger than the actual size of the `render_pass_output`, or if the memory managed by the `render_pass_output` has been freed up.

<https://source.chromium.org/chromium/chromium/src/+/main:components/viz/service/display/software_renderer.cc;drc=8d31e62cff76d1b7b4b60f9aef507860e554828e;l=649>

```
SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/xxx/chromium/asan-linux-release-1445652/chrome+0x26af47e3) (BuildId: 93365fde2aac6e94)

==432346==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7bf300847803 at pc 0x55843f6dd7e4 bp 0x7bf3035f98a0 sp 0x7bf3035f9898
READ of size 16 at 0x7bf300847803 thread T6 (VizCompositorTh)
==432346==WARNING: invalid path to external symbolizer!
==432346==WARNING: Failed to use and restart external symbolizer!
    #0 0x55843f6dd7e3 in skia::Convolve4RowsHorizontally_SSE2(unsigned char const**, skia::ConvolutionFilter1D const&, unsigned char**) convolver_SSE2.cc:?
    #1 0x55843f6d3b83 in skia::BGRAConvolve2D(unsigned char const*, int, bool, skia::ConvolutionFilter1D const&, skia::ConvolutionFilter1D const&, int, unsigned char*, bool) convolver.cc:?
    #2 0x55843f6ceeb1 in skia::ImageOperations::Resize(SkPixmap const&, skia::ImageOperations::ResizeMethod, int, int, SkIRect const&, SkBitmap::Allocator*) image_operations.cc:?
    #3 0x5584552f2a19 in viz::SoftwareRenderer::CopyDrawnRenderPass(viz::copy_output::RenderPassGeometry const&, std::__Cr::unique_ptr<viz::CopyOutputRequest, std::__Cr::default_delete<viz::CopyOutputRequest> >) software_renderer.cc:?
    #4 0x5584552aeb9f in viz::DirectRenderer::DrawRenderPassAndExecuteCopyRequests(viz::AggregatedRenderPass*) direct_renderer.cc:?
    #5 0x5584552aaf7d in viz::DirectRenderer::DrawFrame(std::__Cr::vector<std::__Cr::unique_ptr<viz::AggregatedRenderPass, std::__Cr::default_delete<viz::AggregatedRenderPass> >, std::__Cr::allocator<std::__Cr::unique_ptr<viz::AggregatedRenderPass, std::__Cr::default_delete<viz::AggregatedRenderPass> > > >*, float, gfx::Size const&, gfx::DisplayColorSpaces const&, std::__Cr::vector<gfx::Rect, std::__Cr::allocator<gfx::Rect> >) direct_renderer.cc:?
    #6 0x55845523098b in viz::Display::DrawAndSwap(viz::DrawAndSwapParams const&) display.cc:?
    #7 0x5584551bd449 in viz::DisplayScheduler::DrawAndSwap() display_scheduler.cc:?
Shadow bytes around the buggy address:
  0x7bf300847580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf300847600: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf300847680: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf300847700: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bf300847780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7bf300847800:[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf300847880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf300847900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf300847980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf300847a00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bf300847a80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa

```

### jo...@chromium.org (2025-06-26)

This highlights that `SkPixmap(const SkImageInfo& info, const void* addr, size_t rowBytes) : fPixels(addr), fRowBytes(rowBytes), fInfo(info)` currently takes unbounded memory pointer.

We've bee working on porting Chromium to use `base::span` in place of unbounded buffers/arrays. As this adds asserts for OOB access directly. Which will also get us callstacks of paths that trigger these accesses. I think we'd benefit from this in SkPixmap, though this would need to be phased, as there are a lot of references throughout the codebase.

For the `viz::SoftwareRenderer::CopyDrawnRenderPass` example, fortunately that is a fallback path, and not the principle Viz renderer. So scope of impact is small. The CopyOutputRequest path impacted here is: Thumbnails; DevTools; ViewTransitions. With only the last being tied to website usage.

It does look like there is currently not an enforcement of the size of `geometry.sampling_bounds` compared to the data from

```
    SkPixmap render_pass_output;
    if (!current_canvas_->peekPixels(&render_pass_output)

```

### va...@chromium.org (2025-06-26)

`geometry.sampling_bounds()` comes from [here](<https://source.chromium.org/chromium/chromium/src/+/main:components/viz/service/display/direct_renderer.cc;drc=e65323be17a0ba06198d18b0a8bf5ae594e10348;l=633> and shouldn't be bigger than output rect of the render pass. For the non-root render passes, SkCanvas comes from [here](https://source.chromium.org/chromium/chromium/src/+/main:components/viz/service/display/software_renderer.cc;drc=e65323be17a0ba06198d18b0a8bf5ae594e10348;l=249), that comes from SkBitmap created [here](https://source.chromium.org/chromium/chromium/src/+/main:components/viz/service/display/software_renderer.cc;drc=e65323be17a0ba06198d18b0a8bf5ae594e10348;l=1052) and for software renderer should be `output_rect` rounded up to 64 bits [here](https://source.chromium.org/chromium/chromium/src/+/main:components/viz/service/display/direct_renderer.cc;drc=e65323be17a0ba06198d18b0a8bf5ae594e10348;l=1058).

For root render pass it's more convoluted, because it hits a lot of platform specific code, but size presumably should come from [here](https://source.chromium.org/chromium/chromium/src/+/main:components/viz/service/display/direct_renderer.cc;drc=e65323be17a0ba06198d18b0a8bf5ae594e10348;l=278). It's tricky to trace anything beyond that, so I'd assume those sizes might differ and we should intersect our sampling bounds with actually render pass size to ensure correctness.

### kj...@chromium.org (2025-07-02)

Since the consensus seems to be this is not a bug in Skia directly, is there a better owner for this bug or can we mark it as a dupe of a bug tracking the base::span work?

### ch...@google.com (2025-07-11)

danieldilan: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-07-26)

danieldilan: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### da...@google.com (2025-07-30)

From the discussion above and comment #13, I am lowering the priority of this bug. 

### ch...@google.com (2025-08-14)

danieldilan: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-08-29)

danieldilan: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### vm...@gmail.com (2025-09-12)

No need to reply; this is just additional stack info for this issue.

### kj...@google.com (2026-01-14)

To recap - the reporter made a custom fuzzer (which is not currently part of the chrome corpus) which created invalid inputs and caused crashes.

This is not actionable.

If you'd like to make <https://source.chromium.org/chromium/chromium/src/+/main:skia/ext/image_operations_resize_fuzzer.cc> more robust, please send a CL to change that appropriately so it can be reviewed.

### vm...@gmail.com (2026-01-16)

I understand this issue does not appear to be directly fixable within Skia. However, I believe this should not be considered a non-actionable issue created by a custom fuzzer, as the issue persists at the Chrome application level(./chrome), as evidenced by the provided crash log in [#comment12](https://issues.chromium.org/issues/417599694#comment12) and [#comment21](https://issues.chromium.org/issues/417599694#comment21).While the root cause may not be within Skia itself, the crashes are occurring in a real-world usage scenario rather than in a synthetic fuzzing environment.

### vm...@gmail.com (2026-01-21)

deleted

### dx...@google.com (2026-01-21)

Project: chromium/src  

Branch:  main  

Author:  Kaylee Lubick [kjlubick@google.com](mailto:kjlubick@google.com)  

Link:    <https://chromium-review.googlesource.com/7506469>

Add defensive checks for overflow in image resizing

---


Expand for full commit details
```
     
    The attached bug has a stacktrace that appears to be the result 
    of an integer overflow that happened in a full build of chromium, 
    not just a fuzzer. 
     
    This adds some checks that speculatively will protect against 
    that overflow from getting into the convolver. 
     
    Bug: b:417599694 
    Change-Id: I765317b1a6819c9bc68a73d4b83133ee85cdc036 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7506469 
    Reviewed-by: Florin Malita <fmalita@chromium.org> 
    Auto-Submit: Kaylee Lubick <kjlubick@chromium.org> 
    Commit-Queue: Florin Malita <fmalita@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1572546}

```

---

Files:

- M `skia/ext/image_operations.cc`

---

Hash: [40dbd0b8cb414e2ebd654421e25fd20263c306ba](https://chromiumdash.appspot.com/commit/40dbd0b8cb414e2ebd654421e25fd20263c306ba)  

Date: Wed Jan 21 21:41:03 2026


---

### wf...@chromium.org (2026-02-09)

[vrp panel] Thank you for your bug, but I note the comments from the engineers that this might just be an internal API and not a bug exposed by Chrome. Are you able to provide a PoC file that, when opened in Chrome, triggers the ASAN crash? If so, please attach this, along with the version of Chrome that the crash reproduces on. This will allow us to assess the potential of this issue for a reward.

### vm...@gmail.com (2026-02-10)

Attached are the PoC file and reproduction video. This is a raw sample from the fuzzer. Due to the low reproduction rate, I was unable to minimize it, but a complete reproduction log is provided.

### sp...@google.com (2026-03-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Mildly mitigated memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### vm...@gmail.com (2026-03-12)

deleted

### vm...@gmail.com (2026-03-12)

deleted

### ch...@google.com (2026-05-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/417599694)*
