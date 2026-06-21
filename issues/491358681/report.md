# Heap buffer overflow write in libaom AV1 SVC encoding via WebRTC

| Field | Value |
|-------|-------|
| **Issue ID** | [491358681](https://issues.chromium.org/issues/491358681) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>Video |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | ma...@google.com |
| **Created** | 2026-03-10 |
| **Bounty** | $11,000.00 |

## Description

# Heap buffer overflow write in libaom AV1 SVC encoding via WebRTC

## Summary

A heap buffer overflow write exists in libaom's AV1 encoder when encoding video with spatial Scalable Video Coding (SVC) through WebRTC. The `chroma_check` function in `var_based_part.c` uses the LAST\_FRAME reference's scale factors when computing buffer offsets for GOLDEN\_FRAME and ALTREF\_FRAME, which have different resolutions in spatial SVC configurations. This causes `setup_pred_plane` to calculate an out-of-bounds buffer pointer, and subsequent frame copy operations write past the end of the allocated YV12 frame buffer. A web page can trigger this by establishing a WebRTC peer connection with AV1 and the L2T1 scalability mode. The vulnerability affects all platforms where WebRTC AV1 SVC encoding is supported (Windows, Linux, macOS, ChromeOS, Android).

## Bisect

Introducing Commit (GOLDEN path): [`c6a503f`](https://aomedia.googlesource.com/aom/+/c6a503f4b15da2ecef856f917d08473ea788ae00)

- Date: August 18, 2022
- Author: Marco Paniconi ([marpan@google.com](mailto:marpan@google.com))
- Review: <https://aomedia-review.googlesource.com/c/aom/+/161261>
- Subject: "rtc: Fix to color artifacts under high motion"

Extended to ALTREF path: [`555b3aa`](https://aomedia.googlesource.com/aom/+/555b3aae440dc1a23d11723c556d95b172cb259d)

- Date: March 6, 2023
- Author: Marco Paniconi ([marpan@google.com](mailto:marpan@google.com))
- Review: <https://aomedia-review.googlesource.com/c/aom/+/171601>
- Subject: "rtc: Color sensitivity for altref in nonrd"

Both commits are in the upstream aom.git repository. The original `setup_pred_plane` with LAST\_FRAME's scale factors was introduced in commit [`309d0af`](https://aomedia.googlesource.com/aom/+/309d0affc51a621ffafb76cf6fdc8e917c345e8e) (July 27, 2022) for the LAST\_FRAME path, where using LAST's scale factors is correct. When the GOLDEN and ALTREF paths were added in the subsequent commits, they reused the same `sf` variable without obtaining the appropriate scale factors for those reference frames.

## Root Cause

The `chroma_check` function in `var_based_part.c` computes UV chroma SAD values for three reference frames (LAST, GOLDEN, ALTREF) to determine color sensitivity. It retrieves the scale factors once, for LAST\_FRAME only:

```
// av1/encoder/var_based_part.c:1026-1029
// https://aomedia.googlesource.com/aom/+/39606bf4bae/av1/encoder/var_based_part.c#1026
const YV12_BUFFER_CONFIG *yv12_g = get_ref_frame_yv12_buf(cm, GOLDEN_FRAME);
const YV12_BUFFER_CONFIG *yv12_alt = get_ref_frame_yv12_buf(cm, ALTREF_FRAME);
const struct scale_factors *const sf =
    get_ref_scale_factors_const(cm, LAST_FRAME);

```

This `sf` is then passed to `setup_pred_plane` for all three reference frames. For LAST\_FRAME, this is correct. For GOLDEN\_FRAME and ALTREF\_FRAME, it is wrong:

```
// av1/encoder/var_based_part.c:1062-1069
// https://aomedia.googlesource.com/aom/+/39606bf4bae/av1/encoder/var_based_part.c#1062
if (y_sad_g != UINT_MAX) {
    uint8_t *src = (plane == 1) ? yv12_g->u_buffer : yv12_g->v_buffer;
    setup_pred_plane(&dst, xd->mi[0]->bsize, src, yv12_g->uv_crop_width,
                     yv12_g->uv_crop_height, yv12_g->uv_stride, xd->mi_row,
                     xd->mi_col, sf, xd->plane[plane].subsampling_x,
                     xd->plane[plane].subsampling_y);
    uv_sad_g = cpi->ppi->fn_ptr[bs].sdf(p->src.buf, p->src.stride,
                                         dst.buf, dst.stride);
}

```

The `setup_pred_plane` function computes the buffer pointer as `dst->buf = src + scaled_buffer_offset(x, y, stride, scale)`, where `x` and `y` are derived from the current macroblock's `mi_row` and `mi_col`:

```
// av1/common/reconinter.h:386-404
// https://aomedia.googlesource.com/aom/+/39606bf4bae/av1/common/reconinter.h#386
static inline void setup_pred_plane(struct buf_2d *dst, BLOCK_SIZE bsize,
                                    uint8_t *src, int width, int height,
                                    int stride, int mi_row, int mi_col,
                                    const struct scale_factors *scale,
                                    int subsampling_x, int subsampling_y) {
    const int x = (MI_SIZE * mi_col) >> subsampling_x;
    const int y = (MI_SIZE * mi_row) >> subsampling_y;
    dst->buf = src + scaled_buffer_offset(x, y, stride, scale);
}

```

In AV1 spatial SVC, the enhancement layer (e.g., 1280x720) references a lower-resolution base layer (e.g., 640x360) as its GOLDEN frame. LAST\_FRAME, being from the same spatial layer, has identity scale factors (no scaling). When these identity scale factors are applied to `mi_row`/`mi_col` coordinates from the 1280x720 layer while indexing into the 640x360 GOLDEN buffer, the resulting offset exceeds the smaller buffer's allocation. For a 1280x720 frame with 4:2:0 chroma subsampling, the UV plane coordinates can reach up to y=358, but the GOLDEN frame's UV buffer at 640x360 only accommodates rows up to y=179, producing an overflow of approximately 114 rows worth of data.

The ASAN report shows the overflow manifests as a write of 640 bytes immediately past the end of a 688,935-byte allocation in `aom_yv12_copy_v_c`, which copies the V chroma plane row by row using `memcpy`. The overflow occurs because the source or destination frame buffer was allocated for the smaller spatial layer dimensions, while the copy loop iterates over the larger layer's height.

## Reproduce

Configure `out/asan-release/args.gn`:

```
is_asan = true
is_debug = false
dcheck_always_on = false
target_cpu = "x64"
is_component_build = true

```

Then build and run:

```
autoninja -C out/asan-release chrome
ASAN_OPTIONS=detect_odr_violation=0 out/asan-release/chrome --no-sandbox poc.html

```

The PoC opens a WebRTC peer connection with AV1 SVC (L2T1 scalability mode) encoding a 1280x720 canvas stream. The heap-buffer-overflow fires within seconds of encoding.

The ASAN report:

```
=================================================================
==43000==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x1409738e9b27 at pc 0x7ff8de4eb48c bp 0x00e97d7fc8e0 sp 0x00e97d7fc928
WRITE of size 640 at 0x1409738e9b27 thread T5
    #0 0x7ff8de4eb48b  (clang_rt.asan_dynamic-x86_64.dll+0x18004b48b)
    #1 0x7ff8b03c7b9a in aom_yv12_copy_v_c yv12extend.c:313:5
    #2 0x7ff8b07b14f1 in encode_with_recode_loop_and_filter encoder.c:3706:9
    #3 0x7ff8b07a1f41 in av1_encode encoder.c:4611:9
    #4 0x7ff8b0eecde7 in av1_encode_strategy encode_strategy.c:1713:7
    #5 0x7ff8b07a8765 in av1_get_compressed_data encoder.c:5360:22
    #6 0x7ff8b03a627f in encoder_encode av1_cx_iface.c:3620:20
    #7 0x7ff8b03c3dc8 in aom_codec_encode aom_encoder.c:191:11
    #8 0x7ff8afda2f26 in LibaomAv1Encoder::DoEncode libaom_av1_encoder.cc:1101:7
    #9 0x7ff8afd9af17 in LibaomAv1Encoder::Encode libaom_av1_encoder.cc:993:16
    #10 0x7ff8ae3d79d3 in SimulcastEncoderAdapter::Encode simulcast_encoder_adapter.cc:672:23
    #11 0x7ff84aee87fe in StatsCollectingEncoder::Encode stats_collecting_encoder.cc:123:20
    #12 0x7ff8aef38013 in VideoStreamEncoder::EncodeVideoFrame video_stream_encoder.cc:2226:43

0x1409738e9b27 is located 0 bytes after 688935-byte region [0x140973841800,0x1409738e9b27)
allocated by thread T5 here:
    #0 0x7ff8de4ec8df  (clang_rt.asan_dynamic-x86_64.dll+0x18004c8df)
    #1 0x7ff8b07b7dee in aom_memalign aom_mem.c:59:22
    #2 0x7ff8b086bc5a in aom_realloc_frame_buffer yv12config.c:259:12
    #3 0x7ff8b086c2f8 in aom_alloc_frame_buffer yv12config.c:274:12
    #4 0x7ff8b07b143e in encode_with_recode_loop_and_filter encoder.c:3706:9

SUMMARY: AddressSanitizer: heap-buffer-overflow yv12extend.c:313:5 in aom_yv12_copy_v_c

```
## References

- [`chroma_check` (var\_based\_part.c:987)](https://aomedia.googlesource.com/aom/+/39606bf4bae/av1/encoder/var_based_part.c#987) — buggy function, uses LAST's `sf` for GOLDEN/ALTREF
- [`setup_pred_plane` (reconinter.h:386)](https://aomedia.googlesource.com/aom/+/39606bf4bae/av1/common/reconinter.h#386) — computes `dst->buf` via `scaled_buffer_offset`
- [`aom_yv12_copy_v_c` (yv12extend.c:293)](https://aomedia.googlesource.com/aom/+/39606bf4bae/aom_scale/generic/yv12extend.c#293) — crash site, memcpy overflow
- [`LibaomAv1Encoder::DoEncode` (libaom\_av1\_encoder.cc)](https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/modules/video_coding/codecs/av1/libaom_av1_encoder.cc;l=1101) — WebRTC entry point into libaom

## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 22.8 KB)
- [poc.html](attachments/poc.html) (text/html, 4.7 KB)
- [crash.png](attachments/crash.png) (image/png, 358.3 KB)
- [asan.log](attachments/asan_74205606.log) (text/plain, 22.9 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6088584025014272.

### jd...@chromium.org (2026-03-10)

Thanks for the report. This is not reproducing in an ASAN Chrome build on Clusterfuzz. As a result, I'm closing this as not reproducible. If you'd like to submit an updated PoC, feel free to submit a new report. Thanks.

### je...@gmail.com (2026-03-11)

Hi,

I have successfully reproduced the crash on Windows x64, macOS, and Linux ASAN builds, and it triggers within about 1 second of encoding — so this is not a timing-sensitive or flaky issue. I believe the non-reproduction is specific to something in ClusterFuzz's environment.

Manual verification is straightforward — just build or download an ASAN release build on any platform and open the PoC HTML file. No renderer patches or source modifications are required. I'd appreciate it if someone could give it a quick try to confirm whether this is a ClusterFuzz environment issue.

I don't intend to create additional work for the Chrome VRP team. I'd rather not open a new issue since the PoC and report are unchanged — I just want to make sure the original report gets a fair evaluation.

Thank you.

### je...@gmail.com (2026-03-11)

I just tested it on the latest chromium-asan-1597391-mac-arm64 version as well, and confirmed that this issue has not been fixed.

Copying gs://chromium-browser-asan/mac-release-arm64/asan-mac-release-1597391.zip

### aj...@google.com (2026-03-11)

Repros at HEAD with a renderer buffer overflow.

```
=================================================================
==45504==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x1366a0379b27 at pc 0x7ffaaffcb4ec bp 0x00eca99fc9c0 sp 0x00eca99fca08
WRITE of size 640 at 0x1366a0379b27 thread T6
    #0 0x7ffaaffcb4eb  (D:\chromium\src\out\asan\clang_rt.asan_dynamic-x86_64.dll+0x18004b4eb)
    #1 0x7ff9dae5fad3 in aom_yv12_copy_v_c D:\chromium\src\third_party\libaom\source\libaom\aom_scale\generic\yv12extend.c:313:5
    #2 0x7ff9dadddfb4 in encode_with_recode_loop_and_filter D:\chromium\src\third_party\libaom\source\libaom\av1\encoder\encoder.c:3715:9
    #3 0x7ff9dadc9b02 in av1_encode D:\chromium\src\third_party\libaom\source\libaom\av1\encoder\encoder.c:4620:9
    #4 0x7ff9dada05bd in av1_encode_strategy D:\chromium\src\third_party\libaom\source\libaom\av1\encoder\encode_strategy.c:1713:7
    #5 0x7ff9dadd3329 in av1_get_compressed_data D:\chromium\src\third_party\libaom\source\libaom\av1\encoder\encoder.c:5369:22
   

```

### ch...@google.com (2026-03-11)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-11)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### cl...@appspot.gserviceaccount.com (2026-03-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4852667188707328.

### or...@chromium.org (2026-03-11)

That clusterfuzz job ran with the following encoding-related flags:

```
--enable-media-stream --use-gl=angle --use-angle=swiftshader --use-cmd-decoder=passthrough --use-fake-device-for-media-stream --use-fake-ui-for-media-stream

```

One of those might be causing the bug to not repro. I started a clusterfuzz job without them. We'll see if it repros there.

### je...@gmail.com (2026-03-11)

I personally suspect this is related to WebRTC needing to establish a network connection, which may require a network interface, but I'm not sure.

### ma...@google.com (2026-03-11)

Proposed fix is here: https://aomedia-review.git.corp.google.com/c/aom/+/208221



### ma...@google.com (2026-03-11)

Issue seems to happen due to a libaom-speed feature that should be disabled when  psnr_calc is enabled along with spatial layers. Fix is to disable the speed feature for spatial layers.

The psnr_calc feature is from this issue:  https://issues.webrtc.org/issues/388070060. Seems to have been enabled under a field trial. If i run with --disable-field-trial-config I don't get the crash (without the fix).  

sprang@, can you take a look

### dx...@google.com (2026-03-11)

Project: aom  

Branch:  main  

Author:  Marco Paniconi [marpan@google.com](mailto:marpan@google.com)  

Link:    <https://aomedia-review.googlesource.com/208221>

rtc: Disable speed feature use\_rtc\_tf for spatial layers

---


Expand for full commit details
```
     
    It was already disabled for resize and is_psnr_calc_enabled(), 
    disable it always for now for spatial layers. 
     
    Fixes the buffer overflow in issue below. 
     
    Bug: 491358681 
    Change-Id: If2a71249bbf07ff26e55da5905d959d6c1cdda84

```

---

Files:

- M `av1/encoder/speed_features.c`

---

Hash: fb36c205a6e47aab9272d3fd56816bfe8dd157fe  

Date: Wed Mar 11 17:57:15 2026


---

### 24...@project.gserviceaccount.com (2026-03-12)

Detailed Report: https://clusterfuzz.com/testcase?key=4852667188707328

Fuzzer: None
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE {*}
Crash Address: 0x72ffaa3a8b27
Crash State:
  aom_yv12_copy_v_c
  encode_with_recode_loop_and_filter
  av1_encode
  
Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&revision=1597824

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4852667188707328

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### ch...@google.com (2026-03-12)

Setting Priority to P0 to match Severity s0. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### sp...@google.com (2026-03-12)

Re [comment#13](https://issues.chromium.org/issues/491358681#comment13) there are two different finch trials that can trigger psnr code paths: `WebRTC-Video-CalculatePsnr` and indirectly `WebRTC-EncoderSpeed`. I'll roll back the former and update the latter to not use that code path.

### dx...@google.com (2026-03-12)

Project: chromium/src  

Branch:  main  

Author:  Marco Paniconi [marpan@google.com](mailto:marpan@google.com)  

Link:    <https://chromium-review.googlesource.com/7663284>

Roll src/third\_party/libaom/source/libaom/ 98ce0d2a6..0c15af06a (19 commits)

---


Expand for full commit details
```
     
    https://aomedia.googlesource.com/aom.git/+log/98ce0d2a610f..0c15af06af10 
     
    $ git log 98ce0d2a6..0c15af06a --date=short --no-merges --format='%ad %ae %s' 
    2026-03-12 linzhen Gate the VBR changes in 2fed9c3 only when CONFIG_REALTIME_ONLY=0 
    2026-03-11 marpan rtc: Disable speed feature use_rtc_tf for spatial layers 
    2026-03-11 linzhen Gate the VBR changes in 2fed9c3 only when mode!=REALTIME 
    2026-03-04 narayan.kalaburgi lc-dec: Enable low-complexity decode mode for hdres 
    2026-03-09 linzhen Fix a bug when CONFIG_REALTIME_ONLY=1 
    2026-03-09 rohan.baid Fix build issue related to av1_convolve_x_sr_general_avx2() 
    2026-03-07 juliobbv Fix UseFixedQPOffsetsTest uninitialized value 
    2026-03-05 jzern Fix int16_t overflow in CDEF search for frames > 32768 pixels 
    2026-03-06 linzhen Fix BasicRateTargetingVBRLagRealtime after 2fed9c 
    2026-03-06 juliobbv Fix `use_fixed_qp_offsets` comment 
    2026-02-24 juliobbv Introduce `use_fixed_qp_offsets = 2` 
    2026-03-05 jzern enc: always alloc tile data w/tile count change 
    2026-03-06 jzern encode_api_test: add test coverage for issue 487259772 
    2026-03-05 wtc Use enc_row_mt->allocated_tile_cols/rows correctly 
    2026-03-06 rohan.baid Improve av1_convolve_x_sr_general_avx2() 
    2026-03-05 satheesh.kumar Improve av1_convolve_2d_sr_avx2() 
    2026-03-04 yunqingwang Optimization in apply_temporal_filter function 
    2026-02-02 ttwu add high bit depth compound convolve optimization 
    2026-02-25 linzhen Tweak the rate control for GOOD mode. 
     
    Created with: 
      roll-dep src/third_party/libaom/source/libaom 
    R=jzern@google.com 
     
    Bug: 307414544, 489473886, 487259772, 491358676, 491358681 
    Change-Id: Ib736e0fb8061b6441d8ea4249c5feda6e3ea4137 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7663284 
    Reviewed-by: James Zern <jzern@google.com> 
    Reviewed-by: Wan-Teh Chang <wtc@google.com> 
    Commit-Queue: Wan-Teh Chang <wtc@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1598729}

```

---

Files:

- M `DEPS`
- M `third_party/libaom/README.chromium`
- M `third_party/libaom/libaom_srcs.gni`
- M `third_party/libaom/libaom_test_srcs.gni`
- M `third_party/libaom/source/config/config/aom_version.h`
- M `third_party/libaom/source/libaom`

---

Hash: [1e6229834737252efce6266a77c617aea143648f](https://chromiumdash.appspot.com/commit/1e6229834737252efce6266a77c617aea143648f)  

Date: Thu Mar 12 22:36:28 2026


---

### ch...@google.com (2026-03-13)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### dx...@google.com (2026-03-13)

Project: aom  

Branch:  main  

Author:  Wan-Teh Chang [wtc@google.com](mailto:wtc@google.com)  

Link:    <https://aomedia-review.googlesource.com/208421>

Use scale\_factors for GOLDEN\_FRAME & ALTREF\_FRAME

---


Expand for full commit details
```
     
    In chroma_check(), do not use the scale_factors for LAST_FRAME on 
    GOLDEN_FRAME and ALTREF_FRAME. Get the scale_factors specific to those 
    two reference types. 
     
    This change seems to be suggested by the Root Cause analysis in bug 
    491358681 even though it doesn't fix the bug. 
     
    Bug: 491358681 
    Change-Id: I800ed0cb2fb70d54be25fcc9402eedc09d0db5a7

```

---

Files:

- M `av1/encoder/var_based_part.c`

---

Hash: 0d3618b2de374415eeee1a701efebcb4b6bf1b2c  

Date: Fri Mar 13 18:33:39 2026


---

### ch...@google.com (2026-03-14)

Security Merge Request Consideration: Requesting merge to stable (M146) because latest trunk commit (1598729) appears to be after stable branch point (1582197).
Security Merge Request Consideration: Requesting merge to beta (M147) because latest trunk commit (1598729) appears to be after beta branch point (1596535).
Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [146, 147].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dr...@chromium.org (2026-03-15)

No crashes in Canary. Approving merge to M146 and M147.

### ma...@google.com (2026-03-16)

Which CLs should be backmerged? (Please include Gerrit links.)

https://aomedia-review.git.corp.google.com/c/aom/+/208221

Has this fix been verified on Canary to not pose any stability regressions?

Yes

Does this fix pose any potential non-verifiable stability risks?

No

Does this fix pose any known compatibility risks?

No

Does it require manual verification by the test team? If so, please describe required testing.

No

### dx...@google.com (2026-03-16)

Project: aom  

Branch:  m146-7680  

Author:  Marco Paniconi [marpan@google.com](mailto:marpan@google.com)  

Link:    <https://aomedia-review.googlesource.com/208562>

rtc: Disable speed feature use\_rtc\_tf for spatial layers

---


Expand for full commit details
```
     
    It was already disabled for resize and is_psnr_calc_enabled(), 
    disable it always for now for spatial layers. 
     
    Fixes the buffer overflow in issue below. 
     
    Bug: 491358681 
    Change-Id: If2a71249bbf07ff26e55da5905d959d6c1cdda84 
    (cherry picked from commit fb36c205a6e47aab9272d3fd56816bfe8dd157fe)

```

---

Files:

- M `av1/encoder/speed_features.c`

---

Hash: 446588f90da2e3372a9352d3b2ba8ab3f342c8ce  

Date: Wed Mar 11 17:57:15 2026


---

### dx...@google.com (2026-03-16)

Project: aom  

Branch:  m147-7727  

Author:  Marco Paniconi [marpan@google.com](mailto:marpan@google.com)  

Link:    <https://aomedia-review.googlesource.com/208561>

rtc: Disable speed feature use\_rtc\_tf for spatial layers

---


Expand for full commit details
```
     
    It was already disabled for resize and is_psnr_calc_enabled(), 
    disable it always for now for spatial layers. 
     
    Fixes the buffer overflow in issue below. 
     
    Bug: 491358681 
    Change-Id: If2a71249bbf07ff26e55da5905d959d6c1cdda84 
    (cherry picked from commit fb36c205a6e47aab9272d3fd56816bfe8dd157fe)

```

---

Files:

- M `av1/encoder/speed_features.c`

---

Hash: 9dd1b8af51cfd431cbcdeebc95256c0ec6b249eb  

Date: Wed Mar 11 17:57:15 2026


---

### pe...@google.com (2026-03-16)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ma...@google.com (2026-03-16)

1. Was this issue a regression for the milestone it was found in?

Yes

2. Is this issue related to a change or feature merged after the latest LTS Milestone?

No

### dx...@google.com (2026-03-16)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Marco Paniconi [marpan@google.com](mailto:marpan@google.com)  

Link:    <https://chromium-review.googlesource.com/7670982>

Roll src/third\_party/libaom/source/libaom/ 4018d3b63..446588f90 (1 commit)

---


Expand for full commit details
```
     
    https://aomedia.googlesource.com/aom.git/+log/4018d3b63456..446588f90da2 
     
    $ git log 4018d3b63..446588f90 --date=short --no-merges --format='%ad %ae %s' 
    2026-03-11 marpan rtc: Disable speed feature use_rtc_tf for spatial layers 
     
    Created with: 
      roll-dep src/third_party/libaom/source/libaom 
    R=jzern@google.com 
     
    Bug: 491358681 
    Change-Id: I9d61bc49619ce67fcd092ed9809809b1fa64ec71 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7670982 
    Commit-Queue: James Zern <jzern@google.com> 
    Reviewed-by: James Zern <jzern@google.com> 
    Commit-Queue: Marco Paniconi <marpan@google.com> 
    Reviewed-by: Wan-Teh Chang <wtc@google.com> 
    Cr-Commit-Position: refs/branch-heads/7680@{#2685} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `DEPS`
- M `third_party/libaom/README.chromium`
- M `third_party/libaom/source/config/config/aom_version.h`
- M `third_party/libaom/source/libaom`

---

Hash: [4e7424dbb1b2adeef933130048db87793a5d64cb](https://chromiumdash.appspot.com/commit/4e7424dbb1b2adeef933130048db87793a5d64cb)  

Date: Mon Mar 16 22:05:27 2026


---

### dx...@google.com (2026-03-17)

Project: aom  

Branch:  main  

Author:  Wan-Teh Chang [wtc@google.com](mailto:wtc@google.com)  

Link:    <https://aomedia-review.googlesource.com/208321>

Allocate original source buffer for psnr correctly

---


Expand for full commit details
```
     
    Correct the condition for allocating the cpi->orig_source buffer. 
     
    The use_rtc_tf speed feature and the cpi->orig_source buffer were added 
    in https://aomedia-review.git.corp.google.com/c/aom/+/153083. 
     
    The condition for allocating the cpi->orig_source buffer was modified in 
    https://aomedia-review.git.corp.google.com/c/aom/+/186721. The 
    cpi->rc.prev_coded_width and cpi->rc.prev_coded_height variables used in 
    the new condition were added in 
    https://aomedia-review.git.corp.google.com/c/aom/+/167241. 
     
    Bug: 491358681 
    Change-Id: Ibfc88491bc2e293f56394dc201fccab7786de02b

```

---

Files:

- M `av1/encoder/encoder.c`

---

Hash: 34f25197c6e9efef129992bb763aefa6036119fd  

Date: Fri Mar 13 00:58:23 2026


---

### dx...@google.com (2026-03-17)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Marco Paniconi [marpan@google.com](mailto:marpan@google.com)  

Link:    <https://chromium-review.googlesource.com/7671301>

Roll src/third\_party/libaom/source/libaom/ 98ce0d2a6..9dd1b8af5 (1 commit)

---


Expand for full commit details
```
     
    https://aomedia.googlesource.com/aom.git/+log/98ce0d2a610f..9dd1b8af51cf 
     
    $ git log 98ce0d2a6..9dd1b8af5 --date=short --no-merges --format='%ad %ae %s' 
    2026-03-11 marpan rtc: Disable speed feature use_rtc_tf for spatial layers 
     
    Created with: 
      roll-dep src/third_party/libaom/source/libaom 
    R=jzern@gooogle.com 
     
    Bug: 491358681 
    Change-Id: I0467df253b17bd8341600bf3bbe9a9824dfb1da7 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7671301 
    Reviewed-by: Wan-Teh Chang <wtc@google.com> 
    Reviewed-by: James Zern <jzern@google.com> 
    Commit-Queue: James Zern <jzern@google.com> 
    Cr-Commit-Position: refs/branch-heads/7727@{#534} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `DEPS`
- M `third_party/libaom/README.chromium`
- M `third_party/libaom/source/config/config/aom_version.h`
- M `third_party/libaom/source/libaom`

---

Hash: [21f6231a7dc8c542b90fed17c9e5686eed37f87a](https://chromiumdash.appspot.com/commit/21f6231a7dc8c542b90fed17c9e5686eed37f87a)  

Date: Tue Mar 17 02:11:56 2026


---

### dx...@google.com (2026-03-18)

Project: chromium/src  

Branch:  main  

Author:  Wan-Teh Chang [wtc@google.com](mailto:wtc@google.com)  

Link:    <https://chromium-review.googlesource.com/7673900>

Roll src/third\_party/libaom/source/libaom/ 0c15af06a..34f25197c (13 commits)

---


Expand for full commit details
```
     
    https://aomedia.googlesource.com/aom.git/+log/0c15af06af10..34f25197c6e9 
     
    $ git log 0c15af06a..34f25197c --date=short --no-merges --format='%ad %ae %s' 
    2026-03-12 wtc Allocate original source buffer for psnr correctly 
    2026-03-12 diksha.singh Extend sf 'prune_single_ref' to speed 3, 4 
    2026-03-10 deepa.kg Fix sf 'reuse_compound_type_decision' 
    2026-03-12 yunqingwang Make "--enable-overlay" encoder flag work 
    2026-03-09 diksha.singh Enable AVX2 and SSE2 for av1_apply_temporal_filter() 
    2026-03-11 satheesh.kumar Improve av1_convolve_y_sr_general_avx2() 
    2026-03-13 wtc Fix width/height confusion in av1_first_pass_row() 
    2026-03-14 linzhen Fix data race issue in FrameParallelThreadEncodeTest 
    2026-03-13 wtc Correct comment typo: recont_uvoffset has extra t 
    2026-03-13 wtc Use scale_factors for GOLDEN_FRAME & ALTREF_FRAME 
    2026-03-13 linzhen Revert 0c15af0 and fix svc multi-layer test failures 
    2026-03-12 jzern av1_cx_iface.c: move #if outside of macro 
    2026-03-12 yunqingwang Enhance low-complexity test 
     
    Created with: 
      roll-dep src/third_party/libaom/source/libaom 
    R=jzern@google.com,vigneshv@google.com 
     
    Bug: 307414544,491358681 
    Change-Id: I2ac80ea7c0f9d67fbc1e5ecfc5a4aee494a91f84 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7673900 
    Auto-Submit: Wan-Teh Chang <wtc@google.com> 
    Reviewed-by: James Zern <jzern@google.com> 
    Commit-Queue: James Zern <jzern@google.com> 
    Commit-Queue: Wan-Teh Chang <wtc@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1600889}

```

---

Files:

- M `DEPS`
- M `third_party/libaom/README.chromium`
- M `third_party/libaom/source/config/config/aom_version.h`
- M `third_party/libaom/source/libaom`

---

Hash: [cba8219b908f483eb101b6579acccfe7ad9b1a1b](https://chromiumdash.appspot.com/commit/cba8219b908f483eb101b6579acccfe7ad9b1a1b)  

Date: Wed Mar 18 00:06:50 2026


---

### wf...@chromium.org (2026-03-18)

`Command line: "D:\chromium\src\out\asan-release\chrome.exe" --type=renderer`  from asan stack - this is a renderer memory corruption so sev high.

### pe...@google.com (2026-03-20)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-03-20)

1. https://aomedia-review.git.corp.google.com/c/aom/+/209002
2. Low - There was no conflict.
3. 146 and 147
4. Yes, M138 branch has the suspected CLs[1][2]. So the issue can occur in M138.

[1] https://aomedia-review.googlesource.com/c/aom/+/161261
[2] https://aomedia-review.googlesource.com/c/aom/+/171601

### sp...@google.com (2026-03-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
High-quality report of demonstrated memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2026-03-26)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-03-26)

1. https://aomedia-review.git.corp.google.com/c/aom/+/209503
2. Low - There was no conflict.
3. 146 and 147
4. Yes, M144 branch has the suspected CLs[1][2]. So the issue can occur in M144.

[1] https://aomedia-review.googlesource.com/c/aom/+/161261
[2] https://aomedia-review.googlesource.com/c/aom/+/171601

### an...@google.com (2026-03-30)

Merge approved for LTS 138 and 144

### dx...@google.com (2026-04-02)

Project: aom  

Branch:  m138-7204  

Author:  Gyuyoung Kim [qkim@google.com](mailto:qkim@google.com)  

Link:    <https://aomedia-review.googlesource.com/209002>

rtc: Disable speed feature use\_rtc\_tf for spatial layers

---


Expand for full commit details
```
     
    It was already disabled for resize and is_psnr_calc_enabled(), 
    disable it always for now for spatial layers. 
     
    Fixes the buffer overflow in issue below. 
     
    Bug: 491358681 
    Change-Id: I1e7a879136d3c4d9ded9b1e67e98921335c9c66b 
    (cherry picked from commit fb36c205a6e47aab9272d3fd56816bfe8dd157fe)

```

---

Files:

- M `av1/encoder/speed_features.c`

---

Hash: 46de01e66013f35a94fa89f3c19b3d20d7e04e95  

Date: Fri Mar 20 01:44:31 2026


---

### dx...@google.com (2026-04-17)

Project: aom  

Branch:  m144-7559  

Author:  Gyuyoung Kim [qkim@google.com](mailto:qkim@google.com)  

Link:    <https://aomedia-review.googlesource.com/209503>

rtc: Disable speed feature use\_rtc\_tf for spatial layers

---


Expand for full commit details
```
     
    It was already disabled for resize and is_psnr_calc_enabled(), 
    disable it always for now for spatial layers. 
     
    Fixes the buffer overflow in issue below. 
     
    Bug: 491358681 
    Change-Id: Idd8cc7cdebaf7a1ea221de4f62e9c91e6d66e934 
    (cherry picked from commit fb36c205a6e47aab9272d3fd56816bfe8dd157fe)

```

---

Files:

- M `av1/encoder/speed_features.c`

---

Hash: 0939bc9d417d557e89f8138556ec810d3a7b09fc  

Date: Thu Mar 26 04:01:45 2026


---

### ch...@google.com (2026-06-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/491358681)*
