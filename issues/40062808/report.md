# heap-buffer-overflow in aom_yv12_copy_v_c

| Field | Value |
|-------|-------|
| **Issue ID** | [40062808](https://issues.chromium.org/issues/40062808) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>Video |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | jz...@chromium.org |
| **Created** | 2023-01-27 |
| **Bounty** | $10,000.00 |

## Description

**Steps to reproduce the problem:**  

chrome version:  

111.0.5545.6(custom asan build)  

Chromium 112.0.5564.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1097856.zip)  

operating system:  

macos 12.6  

ubuntu 22,04

repro steps:  

./chrome --user-data-dir=/tmp/x1 ./crash.html  

The heap buffer overflow will be reproduced immediately.

# **Problem Description:**

==175932==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7f352dd8e827 at pc 0x555b75c840c6 bp 0x7f35c09764a0 sp 0x7f35c0975c68  

WRITE of size 400 at 0x7f352dd8e827 thread T2 (ThreadPoolForeg)  

#0 0x555b75c840c5 in \_\_asan\_memcpy *asan\_rtl*:3  

#1 0x555b88a342d3 in aom\_yv12\_copy\_v\_c ./../../third\_party/libaom/source/libaom/aom\_scale/generic/yv12extend.c:372:5  

#2 0x555b88b9ca90 in av1\_encode\_strategy ./../../third\_party/libaom/source/libaom/av1/encoder/encode\_strategy.c:1689:5  

#3 0x555b88b17b8f in av1\_get\_compressed\_data ./../../third\_party/libaom/source/libaom/av1/encoder/encoder.c:4666:22  

#4 0x555b88a43aeb in encoder\_encode ./../../third\_party/libaom/source/libaom/av1/av1\_cx\_iface.c:3091:20  

#5 0x555b88a3625d in aom\_codec\_encode ./../../third\_party/libaom/source/libaom/aom/src/aom\_encoder.c:176:11  

#6 0x555b79b84805 in media::Av1VideoEncoder::Encode(scoped\_refptr[media::VideoFrame](javascript:void(0);), bool, base::OnceCallback<void (media::TypedStatus[media::EncoderStatusTraits](javascript:void(0);))>) ./../../media/video/av1\_video\_encoder.cc:411:7  

#7 0x555b79b4f36b in Invoke<void (media::VideoEncoder::\*)(scoped\_refptr[media::VideoFrame](javascript:void(0);), bool, base::OnceCallback<void (media::TypedStatus[media::EncoderStatusTraits](javascript:void(0);))>), media::VideoEncoder \*, scoped\_refptr[media::VideoFrame](javascript:void(0);), bool, base::OnceCallback<void (media::TypedStatus[media::EncoderStatusTraits](javascript:void(0);))> > ./../../base/functional/bind\_internal.h:733:12  

#8 0x555b79b4f36b in MakeItSo<void (media::VideoEncoder::\*)(scoped\_refptr[media::VideoFrame](javascript:void(0);), bool, base::OnceCallback<void (media::TypedStatus[media::EncoderStatusTraits](javascript:void(0);))>), std::Cr::tuple<base::internal::UnretainedWrapper<media::VideoEncoder, base::unretained\_traits::MayNotDangle>, scoped\_refptr[media::VideoFrame](javascript:void(0);), bool, base::OnceCallback<void (media::TypedStatus[media::EncoderStatusTraits](javascript:void(0);))> > > ./../../base/functional/bind\_internal.h:912:12  

#9 0x555b79b4f36b in RunImpl<void (media::VideoEncoder::\*)(scoped\_refptr[media::VideoFrame](javascript:void(0);), bool, base::OnceCallback<void (media::TypedStatus[media::EncoderStatusTraits](javascript:void(0);))>), std::Cr::tuple<base::internal::UnretainedWrapper<media::VideoEncoder, base::unretained\_traits::MayNotDangle>, scoped\_refptr[media::VideoFrame](javascript:void(0);), bool, base::OnceCallback<void (media::TypedStatus[media::EncoderStatusTraits](javascript:void(0);))> >, 0UL, 1UL, 2UL, 3UL> ./../../base/functional/bind\_internal.h:1007:12  

#10 0x555b79b4f36b in base::internal::Invoker<base::internal::BindState<void (media::VideoEncoder::\*)(scoped\_refptr[media::VideoFrame](javascript:void(0);), bool, base::OnceCallback<void (media::TypedStatus[media::EncoderStatusTraits](javascript:void(0);))>), base::internal::UnretainedWrapper<media::VideoEncoder, base::unretained\_traits::MayNotDangle>, scoped\_refptr[media::VideoFrame](javascript:void(0);), bool, base::OnceCallback<void (media::TypedStatus[media::EncoderStatusTraits](javascript:void(0);))>>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:958:12

0x7f352dd8e827 is located 0 bytes after 258087-byte region [0x7f352dd4f800,0x7f352dd8e827)  

allocated by thread T2 (ThreadPoolForeg) here:  

#0 0x555b75c84cbe in malloc *asan\_rtl*:3  

#1 0x555b88a01737 in aom\_memalign ./../../third\_party/libaom/source/libaom/aom\_mem/aom\_mem.c:59:22  

#2 0x555b88a314d1 in realloc\_frame\_buffer\_aligned ./../../third\_party/libaom/source/libaom/aom\_scale/generic/yv12config.c:114:38  

#3 0x555b88a314d1 in aom\_realloc\_frame\_buffer ./../../third\_party/libaom/source/libaom/aom\_scale/generic/yv12config.c:241:12  

#4 0x555b88a31c07 in aom\_alloc\_frame\_buffer ./../../third\_party/libaom/source/libaom/aom\_scale/generic/yv12config.c:255:12  

#5 0x555b88b1dc19 in encode\_without\_recode ./../../third\_party/libaom/source/libaom/av1/encoder/encoder.c:2480:9  

#6 0x555b88b1dc19 in encode\_with\_recode\_loop\_and\_filter ./../../third\_party/libaom/source/libaom/av1/encoder/encoder.c:3132:9  

#7 0x555b88b10c2b in encode\_frame\_to\_data\_rate ./../../third\_party/libaom/source/libaom/av1/encoder/encoder.c:3797:9  

#8 0x555b88b10c2b in av1\_encode ./../../third\_party/libaom/source/libaom/av1/encoder/encoder.c:3952:9  

#9 0x555b88b9c4a5 in av1\_encode\_strategy ./../../third\_party/libaom/source/libaom/av1/encoder/encode\_strategy.c:1618:7  

#10 0x555b88b17b8f in av1\_get\_compressed\_data ./../../third\_party/libaom/source/libaom/av1/encoder/encoder.c:4666:22  

#11 0x555b88a43aeb in encoder\_encode ./../../third\_party/libaom/source/libaom/av1/av1\_cx\_iface.c:3091:20  

#12 0x555b88a3625d in aom\_codec\_encode ./../../third\_party/libaom/source/libaom/aom/src/aom\_encoder.c:176:11  

#13 0x555b79b84805 in media::Av1VideoEncoder::Encode(scoped\_refptr[media::VideoFrame](javascript:void(0);), bool, base::OnceCallback<void (media::TypedStatus[media::EncoderStatusTraits](javascript:void(0);))>) ./../../media/video/av1\_video\_encoder.cc:411:7  

#14 0x555b79b4f36b in Invoke<void (media::VideoEncoder::\*)(scoped\_refptr[media::VideoFrame](javascript:void(0);), bool, base::OnceCallback<void (media::TypedStatus[media::EncoderStatusTraits](javascript:void(0);))>), media::VideoEncoder \*, scoped\_refptr

**Additional Comments:**

\*\*Chrome version: \*\* 111.0.5545.6 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 1.1 KB)
- [asan.log](attachments/asan.log) (text/plain, 15.4 KB)
- [crbug-1410766.diff](attachments/crbug-1410766.diff) (text/plain, 2.0 KB)
- [crash2.html](attachments/crash2.html) (text/plain, 1.2 KB)

## Timeline

### [Deleted User] (2023-01-27)

[Empty comment from Monorail migration]

### em...@gmail.com (2023-01-27)

[Comment Deleted]

### em...@gmail.com (2023-01-27)

Simple Analysis:
The configuration for the first encoder is used in [0], and the configuration for the second encoder is used in [1]. 
If the values of width and height in the configuration parameters are smaller during the second decoding, which means that the size of n dst_bc->v_buffer is smaller than src_bc->v_buffer , it will cause an out-of-bounds write.

https://source.chromium.org/chromium/chromium/src/+/main:third_party/libaom/source/libaom/aom_scale/generic/yv12extend.c;drc=674eaa06e02193c48fc66991d7508d3e6a4763d1;l=364
void aom_yv12_copy_v_c(const YV12_BUFFER_CONFIG *src_bc,[0]
                       YV12_BUFFER_CONFIG *dst_bc) {[1]
  int row;
  const uint8_t *src = src_bc->v_buffer;
  uint8_t *dst = dst_bc->v_buffer;
#if CONFIG_AV1_HIGHBITDEPTH
  if (src_bc->flags & YV12_FLAG_HIGHBITDEPTH) {
    const uint16_t *src16 = CONVERT_TO_SHORTPTR(src);
    uint16_t *dst16 = CONVERT_TO_SHORTPTR(dst);
    for (row = 0; row < src_bc->uv_height; ++row) {
      memcpy(dst16, src16, src_bc->uv_width * sizeof(uint16_t));
      src16 += src_bc->uv_stride;
      dst16 += dst_bc->uv_stride;
    }
    return;
  }

### em...@gmail.com (2023-01-28)

Analysise：
The issue is caused by an out-of-bounds write due to the destination buffer being smaller than the source buffer in a call to memcpy[0].

(1)The source buffer is initialized in the `encoder_encode()` function by calling `av1_lookahead_init`[B], which sets the `YV12_BUFFER_CONFIG`. However, for the same encoder, **this initialization only occurs once**, as determined by the if (!ppi->lookahead) check [A].

    https://source.chromium.org/chromium/chromium/src/+/main:third_party/libaom/source/libaom/av1/av1_cx_iface.cdrc=706ee36dcc82db6398fadae3ee93a9de1ead7aa6;l=2990
    ```
    static aom_codec_err_t encoder_encode(aom_codec_alg_priv_t *ctx,
                                    const aom_image_t *img,
                                    aom_codec_pts_t pts,
                                    unsigned long duration,
                                    aom_enc_frame_flags_t enc_flags) {
    ...
    if (!ppi->lookahead) {                                        ==>[A]  
      int lag_in_frames = cpi_lap != NULL ? cpi_lap->oxcf.gf_cfg.lag_in_frames
                                          : cpi->oxcf.gf_cfg.lag_in_frames;
      AV1EncoderConfig *oxcf = &cpi->oxcf;
      const BLOCK_SIZE sb_size = av1_select_sb_size(
          oxcf, oxcf->frm_dim_cfg.width, oxcf->frm_dim_cfg.height,
          cpi->svc.number_spatial_layers);
      oxcf->border_in_pixels =
          av1_get_enc_border_size(av1_is_resize_needed(oxcf),
                                  oxcf->kf_cfg.key_freq_max == 0, sb_size);
      for (int i = 0; i < ppi->num_fp_contexts; i++) {
        ppi->parallel_cpi[i]->oxcf.border_in_pixels = oxcf->border_in_pixels;
      }
      const int src_border_in_pixels = get_src_border_in_pixels(cpi, sb_size);
      ppi->lookahead = av1_lookahead_init(                         ==>[B]
          cpi->oxcf.frm_dim_cfg.width, cpi->oxcf.frm_dim_cfg.height,    
          subsampling_x, subsampling_y, use_highbitdepth, lag_in_frames,
          src_border_in_pixels, cpi->common.features.byte_alignment,
          ctx->num_lap_buffers, (cpi->oxcf.kf_cfg.key_freq_max == 0),
          cpi->image_pyramid_levels);
    }
    ```

(2)On the other hand, the destination buffer is set in the `function encode_without_recode`[C], and it will be reset as long as the two conditions `cm->current_frame.frame_number == 0 && cpi->ppi->use_svc`[D] are met.
     https://source.chromium.org/chromium/chromium/src/+/main:third_party/libaom/source/libaom/av1/encoder/encoder.c;drc=706ee36dcc82db6398fadae3ee93a9de1ead7aa6;l=2494
    ```
    static int encode_without_recode(AV1_COMP *cpi) {
    ...
     if (cm->current_frame.frame_number == 0 && cpi->ppi->use_svc) { [D]
        const SequenceHeader *seq_params = cm->seq_params;
        if (aom_alloc_frame_buffer(
                &cpi->svc.source_last_TL0, cpi->oxcf.frm_dim_cfg.width,     ==>[C]
                cpi->oxcf.frm_dim_cfg.height, seq_params->subsampling_x,
                seq_params->subsampling_y, seq_params->use_highbitdepth,
                cpi->oxcf.border_in_pixels, cm->features.byte_alignment, 0, 0)) {
          aom_internal_error(cm->error, AOM_CODEC_MEM_ERROR,
                             "Failed to allocate buffer for source_last_TL0");
        }
      }
      ```
(3)In the same encoder, since the target buffer (YV12_BUFFER_CONFIG) is set twice, the size of the second time is smaller than the first time, which will cause the size of the target buffer of the memory copy to be smaller than the source buffer, and finally cause the buffer Out-of-bounds write.
(3)Therefore, setting up destination buffer(YV12_BUFFER_CONFIG)  twice, with the second one being smaller than the first, will result in a memcpy operation where the destination buffer is smaller than the source buffer, ultimately leading to an out-of-bounds write.

[0]https://source.chromium.org/chromium/chromium/src/+/main:third_party/libaom/source/libaom/aom_scale/generic/yv12extend.c;l=372

### em...@gmail.com (2023-01-28)

Sorry, because the previous analysis was incomplete, I deleted the previous comment and resubmitted the analysis. thanks.
Analysise：
The issue is caused by an out-of-bounds write due to the destination buffer being smaller than the source buffer in a call to memcpy[0].

(1)The source buffer is initialized in the `encoder_encode()` function by calling `av1_lookahead_init`[B], which sets the `YV12_BUFFER_CONFIG`. However, for the same encoder, **this initialization only occurs once**, as determined by the if (!ppi->lookahead) check [A].

    https://source.chromium.org/chromium/chromium/src/+/main:third_party/libaom/source/libaom/av1/av1_cx_iface.cdrc=706ee36dcc82db6398fadae3ee93a9de1ead7aa6;l=2990
    ```
    static aom_codec_err_t encoder_encode(aom_codec_alg_priv_t *ctx,
                                    const aom_image_t *img,
                                    aom_codec_pts_t pts,
                                    unsigned long duration,
                                    aom_enc_frame_flags_t enc_flags) {
    ...
    if (!ppi->lookahead) {                                        ==>[A]  
      int lag_in_frames = cpi_lap != NULL ? cpi_lap->oxcf.gf_cfg.lag_in_frames
                                          : cpi->oxcf.gf_cfg.lag_in_frames;
      AV1EncoderConfig *oxcf = &cpi->oxcf;
      const BLOCK_SIZE sb_size = av1_select_sb_size(
          oxcf, oxcf->frm_dim_cfg.width, oxcf->frm_dim_cfg.height,
          cpi->svc.number_spatial_layers);
      oxcf->border_in_pixels =
          av1_get_enc_border_size(av1_is_resize_needed(oxcf),
                                  oxcf->kf_cfg.key_freq_max == 0, sb_size);
      for (int i = 0; i < ppi->num_fp_contexts; i++) {
        ppi->parallel_cpi[i]->oxcf.border_in_pixels = oxcf->border_in_pixels;
      }
      const int src_border_in_pixels = get_src_border_in_pixels(cpi, sb_size);
      ppi->lookahead = av1_lookahead_init(                         ==>[B]
          cpi->oxcf.frm_dim_cfg.width, cpi->oxcf.frm_dim_cfg.height,    
          subsampling_x, subsampling_y, use_highbitdepth, lag_in_frames,
          src_border_in_pixels, cpi->common.features.byte_alignment,
          ctx->num_lap_buffers, (cpi->oxcf.kf_cfg.key_freq_max == 0),
          cpi->image_pyramid_levels);
    }
    ```

(2)On the other hand, the destination buffer is set in the `function encode_without_recode`[C], and it will be reset as long as the two conditions `cm->current_frame.frame_number == 0 && cpi->ppi->use_svc`[D] are met.
     https://source.chromium.org/chromium/chromium/src/+/main:third_party/libaom/source/libaom/av1/encoder/encoder.c;drc=706ee36dcc82db6398fadae3ee93a9de1ead7aa6;l=2494
    ```
    static int encode_without_recode(AV1_COMP *cpi) {
    ...
     if (cm->current_frame.frame_number == 0 && cpi->ppi->use_svc) { [D]
        const SequenceHeader *seq_params = cm->seq_params;
        if (aom_alloc_frame_buffer(
                &cpi->svc.source_last_TL0, cpi->oxcf.frm_dim_cfg.width,     ==>[C]
                cpi->oxcf.frm_dim_cfg.height, seq_params->subsampling_x,
                seq_params->subsampling_y, seq_params->use_highbitdepth,
                cpi->oxcf.border_in_pixels, cm->features.byte_alignment, 0, 0)) {
          aom_internal_error(cm->error, AOM_CODEC_MEM_ERROR,
                             "Failed to allocate buffer for source_last_TL0");
        }
      }
      ```

(3)Therefore, setting up destination buffer(YV12_BUFFER_CONFIG)  twice, with the second one being smaller than the first, will result in a memcpy operation where the destination buffer is smaller than the source buffer, ultimately leading to an out-of-bounds write.

[0]https://source.chromium.org/chromium/chromium/src/+/main:third_party/libaom/source/libaom/aom_scale/generic/yv12extend.c;l=372

### dc...@chromium.org (2023-01-30)

I was able to repro at the branch base position for M109 and at ToT.

[Monorail components: Internals>Media>Video]

### [Deleted User] (2023-01-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-30)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dc...@chromium.org (2023-01-30)

[Empty comment from Monorail migration]

### jz...@chromium.org (2023-01-31)

Marco, this looks similar to https://crbug.com/1393384. I can reproduce the issue with the test case, but haven't tried extracting this to a standalone libaom repro.

### jz...@chromium.org (2023-01-31)

The attached patch is enough to convert the test from https://crbug.com/1393384 to one that reproduces this one; note the resolution change was necessary as well as using SVC. That test looks like it could be expanded for SVC as well as the cpu-used settings used in Chrome (7 & 9).

### jz...@google.com (2023-01-31)

[Empty comment from Monorail migration]

### wt...@google.com (2023-01-31)

James and I verified that this bug was introduced after libaom v3.5.0, so this bug blocks the libaom v3.6.0 release.

I did a bisection. (We need to apply the fix for issue https://crbug.com/1393384 during the bisection.) git bisect says:

b5b1be8589aa21a39fa7dc6dccb3edac78db3322 is the first bad commit
commit b5b1be8589aa21a39fa7dc6dccb3edac78db3322
Author: Marco Paniconi <marpan@google.com>
Date:   Sat Oct 22 23:37:42 2022 -0700

    rtc: Fix to screen with temporal layers
    
    In real-time mode there are speed features, i.e.,
    scene_detection and source_metrics_sb, that use
    current source vs last_source (source of previous frame),
    but for temporal layers the previous frames does not
    always correspond to the prediction reference (LAST).
    For example, the base temporal layers (TL0) always predicts
    from the previous base TL0, which is 2/4 frames away for
    number_temporal_layers = 2/3.
    
    For screen: the scene_detection and source_metrics_sb have
    big impact on quality and so this wrong choice of
    last_source for these features can have big loss in
    compression efficiency.
    
    This CL fixes this by keeping track of the source frame for
    the LAST reference, and using that for the last_source.
    
    This fix only applies to number_spatial_layers = 1,
    follow-up will be made to handle spatial layers.
    
    Added screen option to svc_encoder_rtc.c, via the patch
    attached in the issue below.
    
    Bug: aomedia:3346
    Change-Id: Ic809feb19b87d0881c95b2749968f9e7931f22f8

 av1/encoder/encode_strategy.c  | 24 ++++++++++++++++++++++++
 av1/encoder/encoder.c          | 15 +++++++++++++++
 av1/encoder/encoder_alloc.h    |  1 +
 av1/encoder/svc_layercontext.c | 10 ++++++++++
 av1/encoder/svc_layercontext.h |  8 ++++++++
 examples/svc_encoder_rtc.c     | 19 +++++++++++++++++++
 6 files changed, 77 insertions(+)

### gi...@appspot.gserviceaccount.com (2023-01-31)

The following revision refers to this bug:
  https://aomedia.googlesource.com/aom/+/50dfbacb57aefb9ed55c0f83f2238d22114ec9fe

commit 50dfbacb57aefb9ed55c0f83f2238d22114ec9fe
Author: Marco Paniconi <marpan@google.com>
Date: Tue Jan 31 20:48:14 2023

rtc: Fix to crash for SVC with resize.

Add new test SmallerFrameSizeSVC that
repros the crash.

Bug: chromium:1410766

Change-Id: Idbe897340d5ca41f0a38a82c1c6d412fb4f4d89a

[modify] https://crrev.com/50dfbacb57aefb9ed55c0f83f2238d22114ec9fe/av1/encoder/encode_strategy.c
[modify] https://crrev.com/50dfbacb57aefb9ed55c0f83f2238d22114ec9fe/test/resize_test.cc
[modify] https://crrev.com/50dfbacb57aefb9ed55c0f83f2238d22114ec9fe/av1/encoder/encoder.c


### gi...@appspot.gserviceaccount.com (2023-02-01)

The following revision refers to this bug:
  https://aomedia.googlesource.com/aom/+/95c81f71c0d5b0dfef22aadf7203d30e033a76d3

commit 95c81f71c0d5b0dfef22aadf7203d30e033a76d3
Author: Marco Paniconi <marpan@google.com>
Date: Tue Jan 31 20:48:14 2023

rtc: Fix to crash for SVC with resize.

Add new test SmallerFrameSizeSVC that
repros the crash.

Bug: chromium:1410766

Change-Id: Idbe897340d5ca41f0a38a82c1c6d412fb4f4d89a
(cherry picked from commit 50dfbacb57aefb9ed55c0f83f2238d22114ec9fe)

[modify] https://crrev.com/95c81f71c0d5b0dfef22aadf7203d30e033a76d3/av1/encoder/encode_strategy.c
[modify] https://crrev.com/95c81f71c0d5b0dfef22aadf7203d30e033a76d3/test/resize_test.cc
[modify] https://crrev.com/95c81f71c0d5b0dfef22aadf7203d30e033a76d3/av1/encoder/encoder.c


### em...@gmail.com (2023-02-02)

I can still repro the same oob write after a simple modification to crash.html. Please confirm.
thanks.

### gi...@appspot.gserviceaccount.com (2023-02-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ce74c2d63b25d0718e1aa8471a0fbaf619cae0ae

commit ce74c2d63b25d0718e1aa8471a0fbaf619cae0ae
Author: James Zern <jzern@chromium.org>
Date: Sat Feb 04 00:56:44 2023

Roll src/third_party/libaom/source/libaom/ 706ee36dc..0144dca8b (31 commits)

https://aomedia.googlesource.com/aom.git/+log/706ee36dcc82..0144dca8bdd0

$ git log 706ee36dc..0144dca8b --date=short --no-merges --format='%ad %ae %s'
2023-02-02 bohanli Improve ConstructGop function
2023-02-02 jzern ext_rate_guided_quantization: check fscanf return
2023-02-01 jzern av1_round_shift_rect_array_32_neon: fix undefined behavior
2023-01-21 wtc Move some var decls in aom_flat_block_finder_run()
2023-01-25 gerdazsejke.more Add Neon implementation of av1_convolve_x_sr for 12-tap filter
2023-02-02 wachsler Move declaration of TplBlockStats
2023-02-02 jingning Fix key frame related encoder failure in LAP
2023-01-27 mudassir.galaganath Allintra: Introduce sf prune_intra_mode_using_best_sad_so_far
2023-02-01 wtc Revert "Correct buffer fullness Q adjustment."
2023-01-25 diksha.singh Speed-up weight calculation during highbd temporal filtering
(...)
2023-01-23 apurve.pandey Speed-up the calculation in av1_set_ssim_rdmult()
2023-01-30 chiyotsai Fix a crash in MSVC x86 Build
2023-01-27 jzern README.md: add VS2022 configure/build examples
2023-01-30 jingning Remove an assertion condition in convolve_c function
2023-01-26 jonathan.wright Use mem_neon.h helpers consistently in convolution paths
2023-01-24 narayan.kalaburgi Abstract round operation in apply_temporal_filter()
2023-01-27 wachsler Prepare to remove subpel_bits field.
2023-01-27 jzern README: bump VS requirement to 2019 (v16)
2023-01-22 wtc Disable MSVC forceinline only in cdef_block_simd.h
2023-01-24 chiyotsai Fix a bug where an uninitalized search_site is used

Created with:
  roll-dep src/third_party/libaom/source/libaom

Bug: 1410766
Change-Id: I525c8420c7cb10ed9300ecbff6a70eb849370ced
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4218003
Reviewed-by: Wan-Teh Chang <wtc@google.com>
Commit-Queue: James Zern <jzern@google.com>
Cr-Commit-Position: refs/heads/main@{#1101292}

[modify] https://crrev.com/ce74c2d63b25d0718e1aa8471a0fbaf619cae0ae/third_party/libaom/source/config/config/aom_version.h
[modify] https://crrev.com/ce74c2d63b25d0718e1aa8471a0fbaf619cae0ae/third_party/libaom/README.chromium
[modify] https://crrev.com/ce74c2d63b25d0718e1aa8471a0fbaf619cae0ae/DEPS


### jz...@chromium.org (2023-02-04)

Given the stable promotion for M110 is slated for 2/7 this might not make the cut.

### [Deleted User] (2023-02-04)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: harrysouders (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-04)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-04)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-04)

LTS Milestone M108

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jz...@chromium.org (2023-02-04)

1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

This fixes tab crash / DoS when using the WebCodecs API.

2. What changes specifically would you like to merge? Please link to Gerrit.

https://aomedia-review.googlesource.com/c/aom/+/169688

3. Have the changes been released and tested on canary?

Yes.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No.


### [Deleted User] (2023-02-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-05)

[Empty comment from Monorail migration]

### rz...@google.com (2023-02-06)

Fixed code doesn't exist in 102.

### rz...@google.com (2023-02-06)

Same for 108

### am...@chromium.org (2023-02-06)

M110 becomes Stable and next Extended as of tomorrow and there are no further planned releases of M109
M111 merge approved, please merge this fix to branch 5563 by 3pm Pacific tomorrow / Tuesday, 7 February so this fix can be included in the next M111 dev/beta
M110 merge approved, please merge to branch 5481 so this fix can be included in the next Stable channel update -- thank you! 

### gi...@appspot.gserviceaccount.com (2023-02-07)

The following revision refers to this bug:
  https://aomedia.googlesource.com/aom/+/74d61ae86f20bc9fb707347bfe618425024f3865

commit 74d61ae86f20bc9fb707347bfe618425024f3865
Author: Marco Paniconi <marpan@google.com>
Date: Tue Jan 31 20:48:14 2023

rtc: Fix to crash for SVC with resize.

Add new test SmallerFrameSizeSVC that
repros the crash.

Bug: chromium:1410766

Change-Id: Idbe897340d5ca41f0a38a82c1c6d412fb4f4d89a
(cherry picked from commit 50dfbacb57aefb9ed55c0f83f2238d22114ec9fe)

[modify] https://crrev.com/74d61ae86f20bc9fb707347bfe618425024f3865/av1/encoder/encode_strategy.c
[modify] https://crrev.com/74d61ae86f20bc9fb707347bfe618425024f3865/test/resize_test.cc
[modify] https://crrev.com/74d61ae86f20bc9fb707347bfe618425024f3865/av1/encoder/encoder.c


### gi...@appspot.gserviceaccount.com (2023-02-07)

The following revision refers to this bug:
  https://aomedia.googlesource.com/aom/+/6770d15de0244bde00f67554f70fc8836826902c

commit 6770d15de0244bde00f67554f70fc8836826902c
Author: Marco Paniconi <marpan@google.com>
Date: Tue Jan 31 20:48:14 2023

rtc: Fix to crash for SVC with resize.

Add new test SmallerFrameSizeSVC that
repros the crash.

Bug: chromium:1410766

Change-Id: Idbe897340d5ca41f0a38a82c1c6d412fb4f4d89a
(cherry picked from commit 50dfbacb57aefb9ed55c0f83f2238d22114ec9fe)

[modify] https://crrev.com/6770d15de0244bde00f67554f70fc8836826902c/av1/encoder/encode_strategy.c
[modify] https://crrev.com/6770d15de0244bde00f67554f70fc8836826902c/test/resize_test.cc
[modify] https://crrev.com/6770d15de0244bde00f67554f70fc8836826902c/av1/encoder/encoder.c


### gi...@appspot.gserviceaccount.com (2023-02-07)

The following revision refers to this bug:
  https://aomedia.googlesource.com/aom/+/74d61ae86f20bc9fb707347bfe618425024f3865

commit 74d61ae86f20bc9fb707347bfe618425024f3865
Author: Marco Paniconi <marpan@google.com>
Date: Tue Jan 31 20:48:14 2023

rtc: Fix to crash for SVC with resize.

Add new test SmallerFrameSizeSVC that
repros the crash.

Bug: chromium:1410766

Change-Id: Idbe897340d5ca41f0a38a82c1c6d412fb4f4d89a
(cherry picked from commit 50dfbacb57aefb9ed55c0f83f2238d22114ec9fe)

[modify] https://crrev.com/74d61ae86f20bc9fb707347bfe618425024f3865/av1/encoder/encode_strategy.c
[modify] https://crrev.com/74d61ae86f20bc9fb707347bfe618425024f3865/test/resize_test.cc
[modify] https://crrev.com/74d61ae86f20bc9fb707347bfe618425024f3865/av1/encoder/encoder.c


### gi...@appspot.gserviceaccount.com (2023-02-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/faa6afba3365180c4929e04754f4993001642911

commit faa6afba3365180c4929e04754f4993001642911
Author: James Zern <jzern@chromium.org>
Date: Tue Feb 07 03:30:07 2023

Roll src/third_party/libaom/source/libaom/ a84503456..6770d15de (1 commit)

https://aomedia.googlesource.com/aom.git/+log/a84503456d42..6770d15de024

$ git log a84503456..6770d15de --date=short --no-merges --format='%ad %ae %s'
2023-01-31 marpan rtc: Fix to crash for SVC with resize.

Created with:
  roll-dep src/third_party/libaom/source/libaom

Bug: 1410766
Change-Id: Ie083b2e96da16e43406d96a808ba4f87d253e6c6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4225608
Reviewed-by: Wan-Teh Chang <wtc@google.com>
Commit-Queue: James Zern <jzern@google.com>
Cr-Commit-Position: refs/branch-heads/5481@{#1008}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/faa6afba3365180c4929e04754f4993001642911/third_party/libaom/source/config/linux/arm-neon-cpu-detect/config/aom_config.h
[modify] https://crrev.com/faa6afba3365180c4929e04754f4993001642911/third_party/libaom/source/config/config/aom_version.h
[modify] https://crrev.com/faa6afba3365180c4929e04754f4993001642911/third_party/libaom/source/config/linux/arm64/config/aom_config.asm
[modify] https://crrev.com/faa6afba3365180c4929e04754f4993001642911/third_party/libaom/source/config/linux/arm-neon/config/aom_config.asm
[modify] https://crrev.com/faa6afba3365180c4929e04754f4993001642911/third_party/libaom/source/config/win/x64/config/aom_config.h
[modify] https://crrev.com/faa6afba3365180c4929e04754f4993001642911/third_party/libaom/README.chromium
[modify] https://crrev.com/faa6afba3365180c4929e04754f4993001642911/third_party/libaom/source/config/linux/arm-neon-cpu-detect/config/aom_config.asm
[modify] https://crrev.com/faa6afba3365180c4929e04754f4993001642911/third_party/libaom/source/config/ios/arm64/config/aom_config.asm
[modify] https://crrev.com/faa6afba3365180c4929e04754f4993001642911/third_party/libaom/source/config/linux/x64/config/aom_config.h
[modify] https://crrev.com/faa6afba3365180c4929e04754f4993001642911/third_party/libaom/source/config/linux/arm/config/aom_config.asm
[modify] https://crrev.com/faa6afba3365180c4929e04754f4993001642911/third_party/libaom/source/config/linux/arm/config/aom_config.h
[modify] https://crrev.com/faa6afba3365180c4929e04754f4993001642911/third_party/libaom/source/config/ios/arm-neon/config/aom_config.h
[modify] https://crrev.com/faa6afba3365180c4929e04754f4993001642911/third_party/libaom/source/config/win/arm64/config/aom_config.h
[modify] https://crrev.com/faa6afba3365180c4929e04754f4993001642911/third_party/libaom/source/config/linux/ia32/config/aom_config.h
[modify] https://crrev.com/faa6afba3365180c4929e04754f4993001642911/third_party/libaom/source/config/linux/generic/config/aom_config.asm
[modify] https://crrev.com/faa6afba3365180c4929e04754f4993001642911/third_party/libaom/source/config/ios/arm64/config/aom_config.h
[modify] https://crrev.com/faa6afba3365180c4929e04754f4993001642911/third_party/libaom/source/config/linux/arm-neon/config/aom_config.h
[modify] https://crrev.com/faa6afba3365180c4929e04754f4993001642911/third_party/libaom/source/config/win/arm64/config/aom_config.asm
[modify] https://crrev.com/faa6afba3365180c4929e04754f4993001642911/third_party/libaom/source/config/win/ia32/config/aom_config.h
[modify] https://crrev.com/faa6afba3365180c4929e04754f4993001642911/third_party/libaom/source/config/linux/generic/config/aom_config.h
[modify] https://crrev.com/faa6afba3365180c4929e04754f4993001642911/DEPS
[modify] https://crrev.com/faa6afba3365180c4929e04754f4993001642911/third_party/libaom/source/config/linux/arm64/config/aom_config.h
[modify] https://crrev.com/faa6afba3365180c4929e04754f4993001642911/third_party/libaom/source/config/ios/arm-neon/config/aom_config.asm


### gi...@appspot.gserviceaccount.com (2023-02-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ee8c79fa44f71f25a354660e6bbf457713f35787

commit ee8c79fa44f71f25a354660e6bbf457713f35787
Author: James Zern <jzern@chromium.org>
Date: Tue Feb 07 03:32:43 2023

Roll src/third_party/libaom/source/libaom/ 706ee36dc..74d61ae86 (1 commit)

https://aomedia.googlesource.com/aom.git/+log/706ee36dcc82..74d61ae86f20

$ git log 706ee36dc..74d61ae86 --date=short --no-merges --format='%ad %ae %s'
2023-01-31 marpan rtc: Fix to crash for SVC with resize.

Created with:
  roll-dep src/third_party/libaom/source/libaom

Bug: 1410766
Change-Id: If542dfd869e1b83b28bcd5d5fbef47436e22dfc5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4226082
Reviewed-by: Wan-Teh Chang <wtc@google.com>
Commit-Queue: James Zern <jzern@google.com>
Cr-Commit-Position: refs/branch-heads/5563@{#228}
Cr-Branched-From: 3ac59a6729cdb287a7ee629a0004c907ec1b06dc-refs/heads/main@{#1097615}

[modify] https://crrev.com/ee8c79fa44f71f25a354660e6bbf457713f35787/third_party/libaom/source/config/config/aom_version.h
[modify] https://crrev.com/ee8c79fa44f71f25a354660e6bbf457713f35787/third_party/libaom/README.chromium
[modify] https://crrev.com/ee8c79fa44f71f25a354660e6bbf457713f35787/DEPS


### jz...@chromium.org (2023-02-07)

The work needed for this bug is now complete.

### am...@google.com (2023-02-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-09)

Congratulations on yet another one, Cassidy Kim! The VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts and reporting this issue to us -- great work! 

### em...@gmail.com (2023-02-10)

Thanks to VRP for the rewards.:)

### am...@google.com (2023-02-10)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-20)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-21)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1410766?no_tracker_redirect=1

[Monorail blocking: crbug.com/aomedia/3342]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062808)*
