# UAF in SVC reconfiguration of AV1 encoder

| Field | Value |
|-------|-------|
| **Issue ID** | [495477995](https://issues.chromium.org/issues/495477995) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>Video |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | jz...@chromium.org |
| **Created** | 2026-03-24 |
| **Bounty** | $8,000.00 |

## Description

### Summary

When the AV1 encoder undergoes SVC reconfiguration with concurrent resolution changes, row-mt worker threads continue access per-block state from a prior encode configuration that has already been freed, leading to the UAF.

### Details

The WebRTC SVC spec exposes `scalabilityMode` as a mutable property on `RTCRtpEncodingParameters`. Blink forwards this string directly into the native layer in [`RTCRtpSender::ToRtpParameters`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/peerconnection/rtc_rtp_sender.cc;l=568):

```
if (encoding->hasScalabilityMode()) {
  webrtc_encoding.scalability_mode = encoding->scalabilityMode().Utf8();
}

```

WebRTC maps the mode string into AV1 SVC configuration via [`SetAv1SvcConfig`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/modules/video_coding/codecs/av1/av1_svc_config.cc;l=97), which also clamps spatial layers against the current frame dimensions:

```
if (ScalabilityMode reduced = LimitNumSpatialLayers(
        *scalability_mode,
        GetLimitedNumSpatialLayers(video_codec.width, video_codec.height));
    *scalability_mode != reduced) {
  scalability_mode = reduced;
}

```

Any `scalabilityMode` change forces a full encoder reset via [`VideoStreamEncoder::RequiresEncoderReset`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/video/video_stream_encoder.cc;l=250):

```
if (new_send_codec.GetScalabilityMode() !=
    prev_send_codec.GetScalabilityMode()) {
  return true;
}

```

This means that mode changes combined with resolution changes (which alter the clamped spatial layer count) can produce a rapid sequence of encoder resets.

The encoder reset tears down and rebuilds internal AV1 state, but does not ensure that in-flight row-mt worker threads have drained before freeing backing buffers. The non-RD encode path follows this call chain on worker threads:

[`enc_row_mt_worker_hook`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/libaom/source/libaom/av1/encoder/ethread.c) → [`av1_encode_sb_row`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/libaom/source/libaom/av1/encoder/encodeframe.c) → [`av1_nonrd_use_partition`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/libaom/source/libaom/av1/encoder/partition_search.c;l=3020) → [`pick_sb_modes_nonrd`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/libaom/source/libaom/av1/encoder/partition_search.c;l=2334) → [`av1_nonrd_pick_inter_mode_sb`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/libaom/source/libaom/av1/encoder/nonrd_pickmode.c;l=1997) → [`av1_block_yrd`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/libaom/source/libaom/av1/encoder/nonrd_opt.c;l=186)

Within `av1_block_yrd`, the worker reads per-block coefficient and reference buffers. The local buffers are declared by the `DECLARE_BLOCK_YRD_BUFFERS()` macro in [`nonrd_opt.c`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/libaom/source/libaom/av1/encoder/nonrd_opt.c;l=25). When an encoder reset frees or recycles the backing encoder state while a worker thread is still executing this path, the worker access freed memory, leading to the UAF.

### Reproduction

Run chromium (e.g., <https://storage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-1603396.zip>) with:

```
chrome --no-sandbox poc.html

```

You would observe the UAF shown in `asan.txt`.

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 28.4 KB)
- [poc.html](attachments/poc.html) (text/html, 4.7 KB)

## Timeline

### he...@gmail.com (2026-03-24)

Add the bisection for this issue:

### Bisection

This issue is introduced by the commit <https://aomedia.googlesource.com/aom/+/c1279721dee3d3cdce3f0a3f8e7e701dcb1bb06e>

This commit moved `allocated_tile_cols/rows` tracking into `av1_alloc_tile_data()`, which is guarded by `allocated_tiles < tile_cols * tile_rows` and skipped when tile count decreases. This causes `row_mt_mem_alloc()` to skip reallocating row-MT sync structures on resolution downsizes, leaving workers to access freed tile data.

### cl...@appspot.gserviceaccount.com (2026-03-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5472738596651008.

### wf...@chromium.org (2026-03-25)

Thank you for your report. This is a well formed report. Thank you for your concise analysis and PoC, and the ASAN stack. This looks like a memory corruption in a sandboxed process so I am triaging as Sev High.

### wf...@chromium.org (2026-03-25)

Note: This could be Sev medium if there is only guaranteed to be a read and the read is not used to control flow in any way (which if reading buffers it looks like it is). I will leave that determination to the webrtc team.

### jz...@chromium.org (2026-03-25)

This looks similar to [b/487259772](https://issues.chromium.org/issues/487259772) which, despite the bug title, covers both VP9 and AV1.

### jz...@chromium.org (2026-03-26)

> This looks similar to [b/487259772](https://issues.chromium.org/issues/487259772) which, despite the bug title, covers both VP9 and AV1.

This still reproduces at a0fcf7656427472eafc362dd32dfda5126546c01 which is past that fix. Eugene has been looking into <https://issues.chromium.org/495996858> and mentioned the failures may be similar.

### ch...@google.com (2026-03-26)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-26)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### eu...@chromium.org (2026-03-26)

To me it looks very similar to [b/495996858](https://issues.chromium.org/issues/495996858). Frequent reconfigurations make `libaom` unhappy in strange ways.

### jz...@chromium.org (2026-03-26)

> To me it looks very similar to [b/495996858](https://issues.chromium.org/issues/495996858). Frequent reconfigurations make libaom unhappy in strange ways.

I agree. The same stacktrace is present in both. Locally for this one I get something different, but the issue is likely due to use of buffers of differing resolutions. The SAD functions expect them to match.

### dx...@google.com (2026-03-27)

Project: aom  

Branch:  main  

Author:  James Zern [jzern@google.com](mailto:jzern@google.com)  

Link:    <https://aomedia-review.googlesource.com/209581>

av1\_nonrd\_pick\_inter\_mode\_sb: add missing ref\_frame\_flags check

---


Expand for full commit details
```
     
    Before calling `set_block_source_sad()` ensure `LAST_FRAME` is 
    available. Fixes a crash that may present as a use after free (UAF). 
     
    Bug: 495477995, 495996858 
    Change-Id: I61452ce412fb9071c3370b4350ed8878013a8355

```

---

Files:

- M `av1/encoder/nonrd_pickmode.c`

---

Hash: 4369bd1258dc99fa759916d9aba6509cdda9d877  

Date: Fri Mar 27 17:56:13 2026


---

### dx...@google.com (2026-03-30)

Project: aom  

Branch:  main  

Author:  Marco Paniconi [marpan@google.com](mailto:marpan@google.com)  

Link:    <https://aomedia-review.googlesource.com/209821>

Set force\_mv\_inter\_layer earlier in skip\_inter\_mode

---


Expand for full commit details
```
     
    For nonrd_pickmode: move the setting of 
    force_mv_inter_layer earlier in the 
    skip_inter_mode_nonrd(), to make sure it always 
    get set (in case of false return in that function). 
     
    Thie prevents the usage of a scaled_ref in pickmode 
    (combined_motion search) when it has actually not been 
    set/scaled in av1_scale_references (before encoding). 
     
    Fixes a crash for use after free (UAF), reported 
    in the issues below. 
     
    Added svc unittest to generate the issue. Also added 
    assert check for scaled_ref in combined_motion_search. 
     
    Bug: 495477995, 495996858 
    Change-Id: I578d19156d97a50546edc9422bc3581566f1236e

```

---

Files:

- M `av1/encoder/nonrd_pickmode.c`
- M `test/svc_datarate_test.cc`

---

Hash: a047955845e50e43786d51cdefcfc9e87804ed61  

Date: Mon Mar 30 03:27:20 2026


---

### dx...@google.com (2026-03-31)

Project: chromium/src  

Branch:  main  

Author:  James Zern [jzern@chromium.org](mailto:jzern@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7718706>

Roll src/third\_party/libaom/source/libaom/ de575da20..dc0b27cfb (15 commits)

---


Expand for full commit details
```
     
    https://aomedia.googlesource.com/aom.git/+log/de575da20409..dc0b27cfbc49 
     
    $ git log de575da20..dc0b27cfb --date=short --no-merges --format='%ad %ae %s' 
    2026-03-27 juliobbv Update CHANGELOG with more changes 
    2026-03-26 jianj use unaligned load for av1_convolve_*_avx2 
    2026-03-25 fgalligan Add support for more color spaces 
    2026-03-27 wtc Revert "av1/decoder/obu.c: don't fail on undefined levels" 
    2026-03-26 jzern remove third_party/SVT-AV1 
    2026-03-27 jzern av1_nonrd_pick_inter_mode_sb: add missing ref_frame_flags check 
    2026-03-25 rohan.baid Enable SIMD of av1_apply_temporal_filter() for 422 format 
    2026-03-25 jzern Revert "Prune the evaluation of inter transform split" 
    2026-03-20 rohan.baid Enable AVX2 and SSE2 for av1_highbd_apply_temporal_filter() 
    2026-03-25 fgalligan Fix typo in matrix_coefficients_enum 
    2026-03-24 yunqingwang Optimize diamond_search_sad 
    2026-03-24 jzern encode_api_test.cc: fix Visual Studio warnings 
    2026-03-24 juliobbv Update CHANGELOG with new features and bug fixes 
    2026-03-24 ranjit.tulabandu Prune the evaluation of inter transform split 
    2026-03-23 diksha.singh Extend sf 'prune_single_ref' to speed 2 
     
    Created with: 
      roll-dep src/third_party/libaom/source/libaom 
     
    Bug: 307414544, 495477995, 495996858, 446258249 
    Change-Id: Ifee42bc36eda1442f612a2479d47bd4c58385c78 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7718706 
    Commit-Queue: Wan-Teh Chang <wtc@google.com> 
    Reviewed-by: Wan-Teh Chang <wtc@google.com> 
    Auto-Submit: James Zern <jzern@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1608139}

```

---

Files:

- M `DEPS`
- M `third_party/libaom/README.chromium`
- M `third_party/libaom/cmake_update.sh`
- M `third_party/libaom/source/config/config/aom_version.h`
- M `third_party/libaom/source/config/linux/arm-neon/config/aom_config.asm`
- M `third_party/libaom/source/config/linux/arm-neon/config/aom_config.c`
- M `third_party/libaom/source/config/linux/arm-neon/config/aom_config.h`
- M `third_party/libaom/source/config/linux/arm64-cpu-detect/config/aom_config.asm`
- M `third_party/libaom/source/config/linux/arm64-cpu-detect/config/aom_config.c`
- M `third_party/libaom/source/config/linux/arm64-cpu-detect/config/aom_config.h`
- M `third_party/libaom/source/config/linux/generic/config/aom_config.asm`
- M `third_party/libaom/source/config/linux/generic/config/aom_config.c`
- M `third_party/libaom/source/config/linux/generic/config/aom_config.h`
- M `third_party/libaom/source/config/linux/ia32/config/aom_config.asm`
- M `third_party/libaom/source/config/linux/ia32/config/aom_config.c`
- M `third_party/libaom/source/config/linux/ia32/config/aom_config.h`
- M `third_party/libaom/source/config/linux/x64/config/aom_config.asm`
- M `third_party/libaom/source/config/linux/x64/config/aom_config.c`
- M `third_party/libaom/source/config/linux/x64/config/aom_config.h`
- M `third_party/libaom/source/config/win/arm64-cpu-detect/config/aom_config.asm`
- M `third_party/libaom/source/config/win/arm64-cpu-detect/config/aom_config.c`
- M `third_party/libaom/source/config/win/arm64-cpu-detect/config/aom_config.h`
- M `third_party/libaom/source/config/win/ia32/config/aom_config.asm`
- M `third_party/libaom/source/config/win/ia32/config/aom_config.c`
- M `third_party/libaom/source/config/win/ia32/config/aom_config.h`
- M `third_party/libaom/source/config/win/x64/config/aom_config.asm`
- M `third_party/libaom/source/config/win/x64/config/aom_config.c`
- M `third_party/libaom/source/config/win/x64/config/aom_config.h`
- M `third_party/libaom/source/libaom`

---

Hash: [5ef6340f7ee1764c9ccdf8e1a225141209477d32](https://chromiumdash.appspot.com/commit/5ef6340f7ee1764c9ccdf8e1a225141209477d32)  

Date: Tue Mar 31 22:23:05 2026


---

### dx...@google.com (2026-04-01)

Project: chromium/src  

Branch:  main  

Author:  Marco Paniconi [marpan@google.com](mailto:marpan@google.com)  

Link:    <https://chromium-review.googlesource.com/7722240>

Roll src/third\_party/libaom/source/libaom/ dc0b27cfb..1ee384377 (13 commits)

---


Expand for full commit details
```
     
    https://aomedia.googlesource.com/aom.git/+log/dc0b27cfbc49..1ee384377191 
     
    $ git log dc0b27cfb..1ee384377 --date=short --no-merges --format='%ad %ae %s' 
    2026-03-31 wtc Enable Clang's -Wc23-extensions warning 
    2026-03-31 wtc Spelling fix: change "an" to "a" 
    2026-03-31 jianj RC: skip shortern GF when using ext RC 
    2026-03-31 marpan Fix unitialized variable in nonrd_pickmode 
    2026-03-30 wtc Convert some assert() to static_assert() 
    2026-03-31 juliobbv Add valuable tune IQ info to `adjust_rdcost()` 
    2026-03-29 marpan Set force_mv_inter_layer earlier in skip_inter_mode 
    2026-03-29 wtc Enable the ISO C11 standard 
    2026-03-30 li.zhang2 Arm: Improve av1_apply_temporal_filter 
    2026-03-30 li.zhang2 Arm: Enable Neon and Neon Dotprod for av1_apply_temporal_filter 
    2026-03-30 li.zhang2 Fix apply_temporal_filter unit test 
    2026-03-30 diksha.singh Extend sf 'weight_calc_level_in_tf' to speed 3 
    2026-03-28 ranjit.tulabandu Fix the calculation of known_rd 
     
    Created with: 
      roll-dep src/third_party/libaom/source/libaom 
    R=jzern@google.com 
     
    Bug: 495477995, 495996858, 307414544 
    Change-Id: I6a059e50d48e93956fd105afdf9785fcd533d1a5 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7722240 
    Reviewed-by: Wan-Teh Chang <wtc@google.com> 
    Commit-Queue: Marco Paniconi <marpan@google.com> 
    Commit-Queue: Wan-Teh Chang <wtc@google.com> 
    Reviewed-by: James Zern <jzern@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1608757}

```

---

Files:

- M `DEPS`
- M `third_party/libaom/README.chromium`
- M `third_party/libaom/source/config/config/aom_version.h`
- M `third_party/libaom/source/libaom`

---

Hash: [8294475710edc805fa56440bc3b82f52385e59fb](https://chromiumdash.appspot.com/commit/8294475710edc805fa56440bc3b82f52385e59fb)  

Date: Wed Apr 1 20:56:52 2026


---

### dx...@google.com (2026-04-02)

Project: aom  

Branch:  main  

Author:  Wan-Teh Chang [wtc@google.com](mailto:wtc@google.com)  

Link:    <https://aomedia-review.googlesource.com/210043>

Change cm back to const in combined\_motion\_search

---


Expand for full commit details
```
     
    The local variable cm in combined_motion_search() was changed to a 
    non-const pointer so that it could be passed to get_ref_scale_factors(). 
    There is a get_ref_scale_factors_const() function for this purpose. 
     
    A follow-up to commit a047955. 
     
    Bug: 495477995, 495996858 
    Change-Id: Ic8b66f8060247a3487a7740fe5383c6e5455fa10

```

---

Files:

- M `av1/encoder/nonrd_pickmode.c`

---

Hash: c61e9586156f0023ad31e8a6abb0dfdcfd820927  

Date: Thu Apr 2 01:57:32 2026


---

### dx...@google.com (2026-04-02)

Project: aom  

Branch:  main  

Author:  James Zern [jzern@google.com](mailto:jzern@google.com)  

Link:    <https://aomedia-review.googlesource.com/210101>

av1\_nonrd\_pick\_inter\_mode\_sb: normalize ref frame check

---


Expand for full commit details
```
     
    Prefer `search_state.use_ref_frame_mask[]` over `cpi->ref_frame_flags`. 
    These are equivalent and checking the former is more consistent with the 
    rest of the function. This is a follow up to: 
     4369bd1258 av1_nonrd_pick_inter_mode_sb: add missing ref_frame_flags check 
     
    Bug: 495477995, 495996858 
    Change-Id: Ie4bd1f4c80c4182add35c7a9c1977c15ce97d3bd

```

---

Files:

- M `av1/encoder/nonrd_pickmode.c`

---

Hash: 395efd18d8ef31d8452a0336e848c02072feffe7  

Date: Thu Apr 2 03:56:24 2026


---

### ch...@google.com (2026-04-08)

Requesting merge to M146 because latest trunk commit (1608757) appears to be after M146 branch point (1582197).

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M147 because latest trunk commit (1608757) appears to be after M147 branch point (1596535).

### ch...@google.com (2026-04-08)

**M146** merge request created. **Please update [crbug/500599336](https://crbug.com/500599336) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M147** merge request created. **Please update [crbug/500600182](https://crbug.com/500600182) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M146** merge request created. **Please update [crbug/500824968](https://crbug.com/500824968) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M147** merge request created. **Please update [crbug/500824097](https://crbug.com/500824097) to have this merge reviewed.**

### dx...@google.com (2026-04-09)

2 changes merged

---

Project: aom  

Branch:  m147-7727  

Author:  Marco Paniconi [marpan@google.com](mailto:marpan@google.com)  

Link:    <https://aomedia-review.googlesource.com/210481>

Set force\_mv\_inter\_layer earlier in skip\_inter\_mode

---


Expand for full commit details
```
     
    For nonrd_pickmode: move the setting of 
    force_mv_inter_layer earlier in the 
    skip_inter_mode_nonrd(), to make sure it always 
    get set (in case of false return in that function). 
     
    Thie prevents the usage of a scaled_ref in pickmode 
    (combined_motion search) when it has actually not been 
    set/scaled in av1_scale_references (before encoding). 
     
    Fixes a crash for use after free (UAF), reported 
    in the issues below. 
     
    Added svc unittest to generate the issue. Also added 
    assert check for scaled_ref in combined_motion_search. 
     
    Bug: 495477995, 495996858, 500600182 
    Change-Id: I578d19156d97a50546edc9422bc3581566f1236e 
    (cherry picked from commit a047955845e50e43786d51cdefcfc9e87804ed61)

```

---

Files:

- M `av1/encoder/nonrd_pickmode.c`
- M `test/svc_datarate_test.cc`

---

Hash: ab9876a5983227865ee26e91caac87c6b8750e27  

Date: Mon Mar 30 03:27:20 2026


---


---

Project: aom  

Branch:  m147-7727  

Author:  James Zern [jzern@google.com](mailto:jzern@google.com)  

Link:    <https://aomedia-review.googlesource.com/210461>

av1\_nonrd\_pick\_inter\_mode\_sb: add missing ref\_frame\_flags check

---


Expand for full commit details
```
     
    Before calling `set_block_source_sad()` ensure `LAST_FRAME` is 
    available. Fixes a crash that may present as a use after free (UAF). 
     
    Bug: 495477995, 495996858, 500600182 
    Change-Id: I61452ce412fb9071c3370b4350ed8878013a8355 
    (cherry picked from commit 4369bd1258dc99fa759916d9aba6509cdda9d877)

```

---

Files:

- M `av1/encoder/nonrd_pickmode.c`

---

Hash: c17573bf30a4901dedc98ded5b91aec060784d8d  

Date: Fri Mar 27 17:56:13 2026


---

### dx...@google.com (2026-04-09)

2 changes merged

---

Project: aom  

Branch:  m146-7680  

Author:  James Zern [jzern@google.com](mailto:jzern@google.com)  

Link:    <https://aomedia-review.googlesource.com/210462>

av1\_nonrd\_pick\_inter\_mode\_sb: add missing ref\_frame\_flags check

---


Expand for full commit details
```
     
    Before calling `set_block_source_sad()` ensure `LAST_FRAME` is 
    available. Fixes a crash that may present as a use after free (UAF). 
     
    Bug: 495477995, 495996858, 500599336 
    Change-Id: I61452ce412fb9071c3370b4350ed8878013a8355 
    (cherry picked from commit 4369bd1258dc99fa759916d9aba6509cdda9d877)

```

---

Files:

- M `av1/encoder/nonrd_pickmode.c`

---

Hash: 5fb0845b95f21fec4113ce03e9647e31b78e610d  

Date: Fri Mar 27 17:56:13 2026


---


---

Project: aom  

Branch:  m146-7680  

Author:  Marco Paniconi [marpan@google.com](mailto:marpan@google.com)  

Link:    <https://aomedia-review.googlesource.com/210463>

Set force\_mv\_inter\_layer earlier in skip\_inter\_mode

---


Expand for full commit details
```
     
    For nonrd_pickmode: move the setting of 
    force_mv_inter_layer earlier in the 
    skip_inter_mode_nonrd(), to make sure it always 
    get set (in case of false return in that function). 
     
    Thie prevents the usage of a scaled_ref in pickmode 
    (combined_motion search) when it has actually not been 
    set/scaled in av1_scale_references (before encoding). 
     
    Fixes a crash for use after free (UAF), reported 
    in the issues below. 
     
    Added svc unittest to generate the issue. Also added 
    assert check for scaled_ref in combined_motion_search. 
     
    Bug: 495477995, 495996858, 500599336 
    Change-Id: I578d19156d97a50546edc9422bc3581566f1236e 
    (cherry picked from commit a047955845e50e43786d51cdefcfc9e87804ed61)

```

---

Files:

- M `av1/encoder/nonrd_pickmode.c`
- M `test/svc_datarate_test.cc`

---

Hash: b5d2fb00c10392da233017c223b1a5662bc7bb0c  

Date: Mon Mar 30 03:27:20 2026


---

### pe...@google.com (2026-04-09)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2026-04-10)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  James Zern [jzern@chromium.org](mailto:jzern@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7745843>

Roll src/third\_party/libaom/source/libaom/ 446588f90..b5d2fb00c (2 commits)

---


Expand for full commit details
```
     
    https://aomedia.googlesource.com/aom.git/+log/446588f90da2..b5d2fb00c103 
     
    $ git log 446588f90..b5d2fb00c --date=short --no-merges --format='%ad %ae %s' 
    2026-03-29 marpan Set force_mv_inter_layer earlier in skip_inter_mode 
    2026-03-27 jzern av1_nonrd_pick_inter_mode_sb: add missing ref_frame_flags check 
     
    Created with: 
      roll-dep src/third_party/libaom/source/libaom 
     
    Bug: 495477995, 495996858, 500599336 
    Fixed: 500599336 
    Change-Id: I73fa7bcdd1d14cabea5dc27aca53086f74af8fc4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7745843 
    Auto-Submit: James Zern <jzern@google.com> 
    Reviewed-by: Wan-Teh Chang <wtc@google.com> 
    Commit-Queue: James Zern <jzern@google.com> 
    Cr-Commit-Position: refs/branch-heads/7680@{#3912} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `DEPS`
- M `third_party/libaom/README.chromium`
- M `third_party/libaom/source/config/config/aom_version.h`
- M `third_party/libaom/source/libaom`

---

Hash: [038ad16930bf61db3b1f19b1b2a8e8df1fc786e0](https://chromiumdash.appspot.com/commit/038ad16930bf61db3b1f19b1b2a8e8df1fc786e0)  

Date: Fri Apr 10 16:21:20 2026


---

### dx...@google.com (2026-04-10)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  James Zern [jzern@chromium.org](mailto:jzern@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7746328>

Roll src/third\_party/libaom/source/libaom/ 9dd1b8af5..ab9876a59 (2 commits)

---


Expand for full commit details
```
     
    https://aomedia.googlesource.com/aom.git/+log/9dd1b8af51cf..ab9876a59832 
     
    $ git log 9dd1b8af5..ab9876a59 --date=short --no-merges --format='%ad %ae %s' 
    2026-03-29 marpan Set force_mv_inter_layer earlier in skip_inter_mode 
    2026-03-27 jzern av1_nonrd_pick_inter_mode_sb: add missing ref_frame_flags check 
     
    Created with: 
      roll-dep src/third_party/libaom/source/libaom 
     
    Bug: 495477995, 495996858, 500600182 
    Fixed: 500600182 
    Change-Id: I88222975371a637865e185b07391a5a94a54c9bd 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7746328 
    Auto-Submit: James Zern <jzern@google.com> 
    Reviewed-by: Wan-Teh Chang <wtc@google.com> 
    Commit-Queue: James Zern <jzern@google.com> 
    Cr-Commit-Position: refs/branch-heads/7727@{#2615} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `DEPS`
- M `third_party/libaom/README.chromium`
- M `third_party/libaom/source/config/config/aom_version.h`
- M `third_party/libaom/source/libaom`

---

Hash: [5baded2e60b157b76c8041d3c9dda1ad5f7b8e3f](https://chromiumdash.appspot.com/commit/5baded2e60b157b76c8041d3c9dda1ad5f7b8e3f)  

Date: Fri Apr 10 17:34:03 2026


---

### sp...@google.com (2026-04-23)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
Baseline with bisect. Renderer RCE / memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2026-05-21)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vi...@google.com (2026-05-25)

1. <https://aomedia-review.git.corp.google.com/c/aom/+/212504> and <https://aomedia-review.git.corp.google.com/c/aom/+/212523>
2. Medium. I haven’ t been able to build and test but the reviewer seems positive: <https://aomedia-review.git.corp.google.com/c/aom/+/212523/comments/861381a6_e02c7d73>
3. 147
4. Yes

### dx...@google.com (2026-05-28)

Project: aom  

Branch:  m144-7559  

Author:  Tiago Vignatti [vignatti@google.com](mailto:vignatti@google.com)  

Link:    <https://aomedia-review.googlesource.com/212504>

av1\_nonrd\_pick\_inter\_mode\_sb: add missing ref\_frame\_flags check

---


Expand for full commit details
```
     
    Before calling `set_block_source_sad()` ensure `LAST_FRAME` is 
    available. Fixes a crash that may present as a use after free (UAF). 
     
    Bug: 495477995, 495996858 
    Change-Id: I61452ce412fb9071c3370b4350ed8878013a8355

```

---

Files:

- M `av1/encoder/nonrd_pickmode.c`

---

Hash: 3d8513679f0a825d02999e3866495e19190a4d8c  

Date: Fri Mar 27 17:56:13 2026


---

### dx...@google.com (2026-05-29)

Project: aom  

Branch:  m144-7559  

Author:  Tiago Vignatti [vignatti@google.com](mailto:vignatti@google.com)  

Link:    <https://aomedia-review.googlesource.com/212523>

Set force\_mv\_inter\_layer earlier in skip\_inter\_mode

---


Expand for full commit details
```
     
    For nonrd_pickmode: move the setting of 
    force_mv_inter_layer earlier in the 
    skip_inter_mode_nonrd(), to make sure it always 
    get set (in case of false return in that function). 
     
    Thie prevents the usage of a scaled_ref in pickmode 
    (combined_motion search) when it has actually not been 
    set/scaled in av1_scale_references (before encoding). 
     
    Fixes a crash for use after free (UAF), reported 
    in the issues below. 
     
    Added svc unittest to generate the issue. Also added 
    assert check for scaled_ref in combined_motion_search. 
     
    Bug: 495477995, 495996858 
    Change-Id: I578d19156d97a50546edc9422bc3581566f1236e

```

---

Files:

- M `av1/encoder/nonrd_pickmode.c`
- M `test/svc_datarate_test.cc`

---

Hash: 725d73571b392cb6acdff4a72b8e98ca6f5ce87c  

Date: Mon Mar 30 03:27:20 2026


---

### ch...@google.com (2026-07-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/495477995)*
