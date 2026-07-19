# VP9 alpha plane use-after-free via show_existing_frame reuse of FrameBufferPool storage

| Field | Value |
|-------|-------|
| **Issue ID** | [500066234](https://issues.chromium.org/issues/500066234) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>Codecs |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | eu...@chromium.org |
| **Created** | 2026-04-07 |
| **Bounty** | $8,000.00 |

## Description

# VP9 alpha plane use-after-free via show\_existing\_frame reuse of FrameBufferPool storage

## Summary

A use-after-free read of VP9 alpha plane data occurs when a crafted WebM triggers VP9's `show_existing_frame` mechanism while alternating the alpha side-stream's bit depth. The `FrameBufferPool` stores alpha data keyed by `fb_priv`, and `show_existing_frame` causes consecutive output frames to share the same `fb_priv`. When a subsequent frame's alpha plane requires a larger allocation (due to a bit-depth change from 8-bit to 10-bit), the pool frees the old alpha buffer while a previously emitted `VideoFrame` still holds a dangling `base::span` into it. The compositor thread then reads 92160 bytes from freed memory during YUV texture upload. The vulnerability is not mitigated by MiraclePtr. It affects all desktop platforms (Linux, macOS, Windows) and requires no special GPU or hardware.

## Bisect

Introducing Commit: `f12d64fb2c759a2e62653b08b663a79299f63d4c`

- Date: 2016-06-29
- Author: vigneshv
- Review: <https://codereview.chromium.org/2096813002>

This commit introduced VP9 alpha channel support by adding per-`fb_priv` alpha storage to the decoder's memory pool. The design assumed that each `fb_priv` would only be associated with one live output frame at a time, which is violated by `show_existing_frame`.

## Root Cause

Chrome's VP9 decoder uses libvpx's external frame buffer API. Each decoded frame carries an opaque `fb_priv` pointer identifying its backing `FrameBuffer` in the `FrameBufferPool`. When a VP9 bitstream signals `show_existing_frame`, libvpx does not allocate a new buffer; it increments the reference count on an existing reference frame buffer and returns the same `fb_priv`:

```
// third_party/libvpx/source/libvpx/vp9/decoder/vp9_decodeframe.c
cm->show_existing_frame = vpx_rb_read_bit(rb);
if (cm->show_existing_frame) {
  const int frame_to_show = cm->ref_frame_map[vpx_rb_read_literal(rb, 3)];
  ref_cnt_fb(frame_bufs, &cm->new_fb_idx, frame_to_show);
}

```

Chrome handles VP9 alpha as a separate side-stream whose decoded pixels are stored per `fb_priv` in the pool's `alpha_data` field. In `VpxVideoDecoder::CopyVpxImageToVideoFrame`, the alpha plane size is computed from the alpha image's stride and height, then passed to `AllocateAlphaPlaneForFrameBuffer` using the main image's `fb_priv` as the key:

```
// media/filters/vpx_video_decoder.cc:580-598
size_t alpha_plane_size =
    vpx_image_alpha->stride[VPX_PLANE_Y] * vpx_image_alpha->d_h;
auto alpha_plane = memory_pool_->AllocateAlphaPlaneForFrameBuffer(
    alpha_plane_size, vpx_image->fb_priv);
libyuv::CopyPlane(vpx_image_alpha->planes[VPX_PLANE_Y],
                  vpx_image_alpha->stride[VPX_PLANE_Y],
                  alpha_plane.data(),
                  vpx_image_alpha->stride[VPX_PLANE_Y],
                  vpx_image_alpha->d_w, vpx_image_alpha->d_h);
*video_frame = VideoFrame::WrapExternalYuvaData(
    codec_format, coded_size, gfx::Rect(visible_size), natural_size,
    ..., alpha_plane, kNoTimestamp);

```

The resulting `VideoFrame` stores the alpha plane pointer as a `base::span<const uint8_t>` in its `data_` array, which is a raw span with no reference-counting or lifetime tracking on the underlying buffer.

When the pool sees a request for a larger alpha allocation on the same `fb_priv`, it frees the old buffer and allocates a new one:

```
// media/base/frame_buffer_pool.cc:158-174
base::span<uint8_t> FrameBufferPool::AllocateAlphaPlaneForFrameBuffer(
    size_t min_size, void* fb_priv) {
  base::AutoLock lock(lock_);
  auto* frame_buffer = static_cast<FrameBuffer*>(fb_priv);
  if (frame_buffer->alpha_data.size() < min_size) {
    frame_buffer->alpha_data = {};   // frees the old buffer
    frame_buffer->alpha_data = AllocateMemory(min_size, ...);
  }
  return frame_buffer->alpha_data;
}

```

The `held_by_frame` counter on the `FrameBuffer` only protects the `FrameBuffer` struct itself from deletion; it does not prevent `alpha_data` from being freed and reallocated. At the point of reallocation, `held_by_frame` is 1 (the previous `VideoFrame` is still alive in the rendering pipeline), yet the old alpha buffer is freed unconditionally.

The PoC constructs a WebM with a VP9 keyframe paired with 8-bit alpha (stride 384, alpha size 92160 bytes), followed by `show_existing_frame` entries paired with 10-bit alpha (stride 768, alpha size 184320 bytes). Because `show_existing_frame` reuses the same `fb_priv`, the second decode call hits the `alpha_data.size() < min_size` path and frees the 92160-byte buffer. The first `VideoFrame`, still queued for compositing, holds a dangling span into the freed region.

The freed alpha buffer is then read on the `VideoFrameCompositor` thread when the compositor uploads the stale frame's YUV planes to a GPU texture. In `WriteYUVPixelsForAllPlanesToTexture`, each plane's data is accessed through a raw `const uint8_t*` returned by `video_frame->data(plane)`:

```
// media/renderers/video_resource_updater.cc:1075-1078
const uint8_t* pixels;
if (!needs_conversion) {
    pixels = video_frame->data(frame_planes[plane_index]);
    ...
}

```

This pointer is not wrapped in `raw_ptr<T>`, so MiraclePtr/BackupRefPtr does not observe the access. Furthermore, at the time the alpha buffer is freed, no `raw_ptr` references it (the `VideoFrame` stores it in a `base::span`), so PartitionAlloc's BRP quarantine mechanism does not engage and the memory is returned to the allocator immediately. ASAN confirms `MiraclePtr Status: NOT PROTECTED`.

## Reproduce

Tested at commit `5e60c832cb8d7cddd0bc4f84d3c8864c80649afb` on Linux x86\_64.

Build with `is_asan = true` and `is_debug = false`. Serve the attached `poc.html` and `poc.webm` from the same directory over HTTP. Launch:

```
ASAN_OPTIONS=detect_odr_violation=0 ~/chromium/src/out/asan-release/chrome \
  --no-sandbox \
  --user-data-dir=/tmp/poc-$(date +%s) \
  http://localhost:8899/poc.html

```

Click the page to start playback if autoplay is blocked. The renderer crashes within seconds. ASAN reports:

```
==2816922==ERROR: AddressSanitizer: heap-use-after-free on address 0x7eea6a240800
READ of size 92160 at 0x7eea6a240800 thread T12 (VideoFrameCompo)
    #0 __asan_memcpy
    #1 gpu::raster::RasterImplementation::WritePixelsYUV gpu/command_buffer/client/raster_implementation.cc:1317
    #2 media::VideoResourceUpdater::WriteYUVPixelsForAllPlanesToTexture media/renderers/video_resource_updater.cc:1166

freed by thread T11 (Media):
    #0 free
    #1 media::FrameBufferPool::AllocateAlphaPlaneForFrameBuffer
    #2 media::VpxVideoDecoder::CopyVpxImageToVideoFrame media/filters/vpx_video_decoder.cc:589

previously allocated by thread T11 (Media):
    #0 calloc
    #1 base::UncheckedCalloc
    #2 media::AllocateMemory media/base/frame_buffer_pool.cc:78
    #3 media::FrameBufferPool::AllocateAlphaPlaneForFrameBuffer media/base/frame_buffer_pool.cc:181

MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.

```

The complete ASAN log is in the attached `asan.log`.

## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [poc.html](attachments/poc.html) (text/html, 1.8 KB)
- [poc.webm](attachments/poc.webm) (video/webm, 8.0 KB)
- [asan.log](attachments/asan.log) (text/plain, 11.5 KB)

## Timeline

### ch...@google.com (2026-04-08)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-08)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-04-09)

Project: chromium/src  

Branch:  main  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7737984>

media: Zero-copy VP9 alpha decoding in VpxVideoDecoder

---


Expand for full commit details
```
     
    Configures the VP9 alpha decoder to use `memory_pool_` for external 
    frame buffers, eliminating the need for `libyuv::CopyPlane`. 
     
    The `VideoFrame` now wraps the alpha data directly from the pool using 
    a second destruction observer. `AllocateAlphaPlaneForFrameBuffer` and 
    `alpha_data` tracking are removed from `FrameBufferPool`. 
     
    Bug: 500066234 
    Change-Id: I6e7cf13bcc8a5a1759acfd51961859c4c57fcbf2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7737984 
    Reviewed-by: Ted (Chromium) Meyer <tmathmeyer@chromium.org> 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1611919}

```

---

Files:

- M `media/base/frame_buffer_pool.cc`
- M `media/base/frame_buffer_pool.h`
- M `media/base/frame_buffer_pool_unittest.cc`
- M `media/filters/vpx_video_decoder.cc`
- M `media/filters/vpx_video_decoder.h`
- M `media/filters/vpx_video_decoder_unittest.cc`

---

Hash: [fc79e8cc2dfcc8f7ec8ee9cf0acf0993f32aec27](https://chromiumdash.appspot.com/commit/fc79e8cc2dfcc8f7ec8ee9cf0acf0993f32aec27)  

Date: Thu Apr 9 01:32:31 2026


---

### ch...@google.com (2026-04-10)

Requesting merge to M146 because latest trunk commit (1611919) appears to be after M146 branch point (1582197).

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M147 because latest trunk commit (1611919) appears to be after M147 branch point (1596535).

Requesting merge to M148 because latest trunk commit (1611919) appears to be after M148 branch point (1610480).

### ch...@google.com (2026-04-10)

**M146** merge request created. **Please update [crbug/501314839](https://crbug.com/501314839) to have this merge reviewed.**

### ch...@google.com (2026-04-10)

**M147** merge request created. **Please update [crbug/501314979](https://crbug.com/501314979) to have this merge reviewed.**

### ch...@google.com (2026-04-10)

**M148** merge request created. **Please update [crbug/501315149](https://crbug.com/501315149) to have this merge reviewed.**

### dx...@google.com (2026-04-14)

Project: chromium/src  

Branch:  refs/branch-heads/7778  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7757899>

[M148] media: Zero-copy VP9 alpha decoding in VpxVideoDecoder

---


Expand for full commit details
```
     
    Configures the VP9 alpha decoder to use `memory_pool_` for external 
    frame buffers, eliminating the need for `libyuv::CopyPlane`. 
     
    The `VideoFrame` now wraps the alpha data directly from the pool using 
    a second destruction observer. `AllocateAlphaPlaneForFrameBuffer` and 
    `alpha_data` tracking are removed from `FrameBufferPool`. 
     
    (cherry picked from commit fc79e8cc2dfcc8f7ec8ee9cf0acf0993f32aec27) 
     
    Bug: 500066234, 501315149 
    Change-Id: I6e7cf13bcc8a5a1759acfd51961859c4c57fcbf2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7737984 
    Reviewed-by: Ted (Chromium) Meyer <tmathmeyer@chromium.org> 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1611919} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7757899 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7778@{#544} 
    Cr-Branched-From: 77f495ee216d4c3cc784d33658bad4778c0680ee-refs/heads/main@{#1610480}

```

---

Files:

- M `media/base/frame_buffer_pool.cc`
- M `media/base/frame_buffer_pool.h`
- M `media/base/frame_buffer_pool_unittest.cc`
- M `media/filters/vpx_video_decoder.cc`
- M `media/filters/vpx_video_decoder.h`
- M `media/filters/vpx_video_decoder_unittest.cc`

---

Hash: [ccb2058fd0285f4fa3ec5e65849d454e5125a41e](https://chromiumdash.appspot.com/commit/ccb2058fd0285f4fa3ec5e65849d454e5125a41e)  

Date: Tue Apr 14 05:42:30 2026


---

### pe...@google.com (2026-04-14)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2026-04-14)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7757381>

[M147] media: Zero-copy VP9 alpha decoding in VpxVideoDecoder

---


Expand for full commit details
```
     
    Configures the VP9 alpha decoder to use `memory_pool_` for external 
    frame buffers, eliminating the need for `libyuv::CopyPlane`. 
     
    The `VideoFrame` now wraps the alpha data directly from the pool using 
    a second destruction observer. `AllocateAlphaPlaneForFrameBuffer` and 
    `alpha_data` tracking are removed from `FrameBufferPool`. 
     
    (cherry picked from commit fc79e8cc2dfcc8f7ec8ee9cf0acf0993f32aec27) 
     
    Bug: 500066234, 501314979 
    Change-Id: I6e7cf13bcc8a5a1759acfd51961859c4c57fcbf2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7737984 
    Reviewed-by: Ted (Chromium) Meyer <tmathmeyer@chromium.org> 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1611919} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7757381 
    Cr-Commit-Position: refs/branch-heads/7727@{#2876} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `media/base/frame_buffer_pool.cc`
- M `media/base/frame_buffer_pool.h`
- M `media/base/frame_buffer_pool_unittest.cc`
- M `media/filters/vpx_video_decoder.cc`
- M `media/filters/vpx_video_decoder.h`
- M `media/filters/vpx_video_decoder_unittest.cc`

---

Hash: [4c15bc05aeb60c4a6cf3d3e61f83ce01a1a9af79](https://chromiumdash.appspot.com/commit/4c15bc05aeb60c4a6cf3d3e61f83ce01a1a9af79)  

Date: Tue Apr 14 05:45:24 2026


---

### dx...@google.com (2026-04-14)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7757063>

[M146] media: Zero-copy VP9 alpha decoding in VpxVideoDecoder

---


Expand for full commit details
```
     
    Original change's description: 
    > media: Zero-copy VP9 alpha decoding in VpxVideoDecoder 
    > 
    > Configures the VP9 alpha decoder to use `memory_pool_` for external 
    > frame buffers, eliminating the need for `libyuv::CopyPlane`. 
    > 
    > The `VideoFrame` now wraps the alpha data directly from the pool using 
    > a second destruction observer. `AllocateAlphaPlaneForFrameBuffer` and 
    > `alpha_data` tracking are removed from `FrameBufferPool`. 
    > 
    > Bug: 500066234 
    > Change-Id: I6e7cf13bcc8a5a1759acfd51961859c4c57fcbf2 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7737984 
    > Reviewed-by: Ted (Chromium) Meyer <tmathmeyer@chromium.org> 
    > Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    > Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1611919} 
     
    (cherry picked from commit fc79e8cc2dfcc8f7ec8ee9cf0acf0993f32aec27) 
     
    Bug: 501314839,500066234 
    Change-Id: I6e7cf13bcc8a5a1759acfd51961859c4c57fcbf2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7757063 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7680@{#3937} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `media/base/frame_buffer_pool.cc`
- M `media/base/frame_buffer_pool.h`
- M `media/base/frame_buffer_pool_unittest.cc`
- M `media/filters/vpx_video_decoder.cc`
- M `media/filters/vpx_video_decoder.h`
- M `media/filters/vpx_video_decoder_unittest.cc`

---

Hash: [eeb3e031eb8986048b34489743e711d28345e134](https://chromiumdash.appspot.com/commit/eeb3e031eb8986048b34489743e711d28345e134)  

Date: Tue Apr 14 05:52:33 2026


---

### sp...@google.com (2026-04-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
Baseline with bisect. Renderer RCE / memory corruption in a sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2026-06-01)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-06-01)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7858691
2. Medium - There were some conflicts.
3. 146, 147, and 148.
4. Yes, the bug has existed for a long years.

### dx...@google.com (2026-06-09)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Gyuyoung Kim [qkim@google.com](mailto:qkim@google.com)  

Link:    <https://chromium-review.googlesource.com/7858691>

[M144-LTS] media: Zero-copy VP9 alpha decoding in VpxVideoDecoder

---


Expand for full commit details
```
     
    Configures the VP9 alpha decoder to use `memory_pool_` for external 
    frame buffers, eliminating the need for `libyuv::CopyPlane`. 
     
    The `VideoFrame` now wraps the alpha data directly from the pool using 
    a second destruction observer. `AllocateAlphaPlaneForFrameBuffer` and 
    `alpha_data` tracking are removed from `FrameBufferPool`. 
     
    (cherry picked from commit fc79e8cc2dfcc8f7ec8ee9cf0acf0993f32aec27) 
     
    Bug: 500066234 
    Change-Id: I6e7cf13bcc8a5a1759acfd51961859c4c57fcbf2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7737984 
    Reviewed-by: Ted (Chromium) Meyer <tmathmeyer@chromium.org> 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1611919} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7858691 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Mohamed Omar <mohamedaomar@google.com> 
    Owners-Override: Artem Sumaneev <asumaneev@google.com> 
    Reviewed-by: Artem Sumaneev <asumaneev@google.com> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4978} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `media/base/frame_buffer_pool.cc`
- M `media/base/frame_buffer_pool.h`
- M `media/base/frame_buffer_pool_unittest.cc`
- M `media/filters/vpx_video_decoder.cc`
- M `media/filters/vpx_video_decoder.h`
- M `media/filters/vpx_video_decoder_unittest.cc`

---

Hash: [0623bc7163560f51b463abba6d73e99e6515ed10](https://chromiumdash.appspot.com/commit/0623bc7163560f51b463abba6d73e99e6515ed10)  

Date: Tue Jun 9 05:32:31 2026


---

### ch...@google.com (2026-07-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/500066234)*
