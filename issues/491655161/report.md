# WebCodecs libaom, libvpx: OOB Read in AV1 and VP9  encoder when encoding I420 frames with mismatched U and V strides

| Field | Value |
|-------|-------|
| **Issue ID** | [491655161](https://issues.chromium.org/issues/491655161) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Media>Video |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | eu...@chromium.org |
| **Assignee** | jz...@chromium.org |
| **Created** | 2026-03-11 |
| **Bounty** | $3,000.00 |

## Description

# Heap Buffer Over-Read in OpenH264 Encoder Due to U/V Stride Mismatch

## Summary

OpenH264's encoder preprocessing copies the V chroma plane using the U plane's stride instead of the V plane's own stride. When an I420 frame has a U stride that is significantly larger than its V stride, the V plane copy reads far beyond the allocated buffer. This is reachable from the web via the WebCodecs VideoEncoder API by constructing an I420 VideoFrame from an ArrayBuffer with custom per-plane strides and using the `transfer` option to preserve them. The resulting out-of-bounds read crashes the renderer process. The crash reproduces on both ASAN builds and standard release Chrome. Affected platforms: all platforms where OpenH264 is enabled (Linux, Windows, macOS, Android, ChromeOS).

## Bisect

Introducing Commit: [`70e5e62f3dbd19f0e9300fa7bba670c7ee93dcd2`](https://github.com/cisco/openh264/commit/70e5e62f3dbd19f0e9300fa7bba670c7ee93dcd2) (OpenH264 repository)

- Date: 2013-12-09
- Author: Ethan Hugg [ehugg@cisco.com](mailto:ehugg@cisco.com)
- Note: This is the initial commit of the OpenH264 repository. The bug has existed since OpenH264's first public release.

## Root Cause

The `SSourcePicture` structure used by OpenH264's public API declares per-plane strides:

```
// third_party/openh264/src/codec/api/wels/codec_app_def.h
typedef struct Source_Picture_s {
  int       iColorFormat;
  int       iStride[4];       // stride for each plane pData
  unsigned char*  pData[4];   // plane pData
  int       iPicWidth;
  int       iPicHeight;
  // ...
} SSourcePicture;

```

Chromium's OpenH264 encoder wrapper correctly populates all three strides from the incoming `VideoFrame`:

```
// https://source.chromium.org/chromium/chromium/src/+/main:media/video/openh264_video_encoder.cc;l=473
picture_stride[0] = frame->stride(VideoFrame::Plane::kY);
picture_stride[1] = frame->stride(VideoFrame::Plane::kU);
picture_stride[2] = frame->stride(VideoFrame::Plane::kV);

```

However, inside OpenH264, `WelsMoveMemoryWrapper` reads only `iStride[1]` (the U stride) and uses it as the shared stride for both U and V plane copies:

```
// https://source.chromium.org/chromium/chromium/src/+/main:third_party/openh264/src/codec/encoder/core/src/wels_preprocess.cpp;l=1416
const int32_t kiSrcStrideUV = kpSrc->iStride[1];  // BUG: ignores iStride[2]

```

This single `kiSrcStrideUV` value is then passed to `WelsMoveMemory_c`, which uses it to advance both `pSrcU` and `pSrcV` pointers between rows:

```
// https://source.chromium.org/chromium/chromium/src/+/main:third_party/openh264/src/codec/encoder/core/src/wels_preprocess.cpp;l=1364
for (j = iHeight2; j; j--) {
    WelsMemcpy (pDstU, pSrcU, iWidth2);
    WelsMemcpy (pDstV, pSrcV, iWidth2);
    pDstU += iDstStrideUV;
    pDstV += iDstStrideUV;
    pSrcU += iSrcStrideUV;   // uses U stride for both
    pSrcV += iSrcStrideUV;   // should use V stride here
}

```

When U stride is much larger than V stride, the V plane copy reads far beyond the V plane's allocation. In the PoC, a 64x64 I420 frame is constructed with U stride=65536 and V stride=32. The V plane occupies 1024 bytes, but the copy routine advances by 65536 bytes per row, requiring approximately 2MB of readable memory from the V plane start. This produces an out-of-bounds read of approximately 1.94MB.

The WebCodecs `VideoFrame` constructor allows creating frames from an `ArrayBuffer` with custom per-plane layout. When the `transfer` option is used, the frame wraps the original ArrayBuffer memory directly via `VideoFrame::WrapExternalDataWithLayout`, preserving the caller-supplied strides without normalization. The WebCodecs stride validation in `video_frame_layout.cc` checks per-plane minimum stride constraints but does not enforce any relationship between U and V strides.

The out-of-bounds read offset and length are fully attacker-controlled. The attacker chooses the U stride value via the `layout` parameter, which directly determines how far past the V plane allocation each row read advances:

```
layout: [
  { offset: offsetY, stride: strideY },    // Y plane
  { offset: offsetU, stride: 65536 },      // U plane — this stride is used for V copy too
  { offset: offsetV, stride: 32 },         // V plane — actual stride ignored by OpenH264
]

```

The attached PoC uses a U stride of 65536 producing a ~1.94MB over-read, but any stride value is accepted.

## chrome://crashes id

e325cfe035f61694

## Reproduce

**Do NOT use ClusterFuzz to reproduce this bug.** ClusterFuzz builds do not include `proprietary_codecs` and will not have OpenH264 compiled in, so the vulnerable code path is unreachable. As an alternative, a crash ID from standard release Chrome is provided in the "chrome://crashes id" section above.

This crash reproduces on standard release Chrome (tested on Chrome 146.0.7680.71 on macOS), where it manifests as an "Aw, Snap!" renderer crash (SIGBUS, error code 10).

The open-source Chromium build defaults `proprietary_codecs` to `false` to avoid distributing patent-encumbered codecs (H.264, AAC, etc.) without a license. Google Chrome ships with `proprietary_codecs = true` and `ffmpeg_branding = "Chrome"` under its own patent licensing agreements. To reproduce with an ASAN build, these flags must be set to match the production Chrome configuration.

Tested on commit `f51a685e768b632262beaf8bd95387fffe096655`. No source modifications are required. Open `poc.html` in Chrome to trigger the crash.

The `args.gn`:

```
is_asan = true
is_debug = false
dcheck_always_on = false
target_cpu = "x64"
is_component_build = true
proprietary_codecs = true
rtc_use_h264 = true
media_use_openh264 = true
ffmpeg_branding = "Chrome"

```
```
autoninja -C ~/chromium/src/out/asan-release chrome
cd ~/chromium/src
ASAN_OPTIONS=detect_odr_violation=0 out/asan-release/chrome --user-data-dir=/tmp/poc-$(date +%s) poc.html

```

Crash log:

```
Received signal 11 SEGV_ACCERR 7a3c00215000
#5 0x7f8c738c4881 memcpy (libc.so.6+0xc4880)
#6 0x561eff6e945c __asan_memcpy (chrome+0x67e945b)
#7 0x7f8ccf90f911 WelsMoveMemoryWrapper (wels_preprocess.cpp)
#8 0x7f8ccf90b487 SingleLayerPreprocess (wels_preprocess.cpp)
#9 0x7f8ccf868ee1 WelsEncoderEncodeExt (encoder_ext.cpp)
#10 0x7f8ccf923bc3 CWelsH264SVCEncoder::EncodeFrameInternal (welsEncoderExt.cpp)
#11 0x7f8ccf9238a4 CWelsH264SVCEncoder::EncodeFrame (welsEncoderExt.cpp)
#12 0x7f8ccf2feb49 OpenH264VideoEncoder::Encode (openh264_video_encoder.cc)

```

The crash manifests as SEGV rather than a standard ASAN heap-buffer-overflow report because V8 sandbox allocates ArrayBuffer backing stores via PartitionAlloc with [`kNoMemoryToolOverride`](https://source.chromium.org/chromium/chromium/src/+/main:gin/array_buffer.cc;l=48), which disables ASAN shadow memory tracking for these allocations.

## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [poc.html](attachments/poc.html) (text/html, 2.1 KB)
- [asan.log](attachments/asan.log) (text/plain, 3.1 KB)
- [webrtc_uv_stride_crash.html](attachments/webrtc_uv_stride_crash.html) (text/html, 5.3 KB)

## Timeline

### th...@chromium.org (2026-03-11)

[security shepherd] I can reproduce the crash on stable M146 on Mac (same trace as for the chrome://crashes id). Based on the bisect in the description + git blame on the package in chrome, this has been around for a while, so setting the found in to M145. Assigning to sprang@ from third\_party/openh264/OWNERS. Speculatively extending platforms based on bug description.

### ch...@google.com (2026-03-12)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-12)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### sp...@chromium.org (2026-03-12)

Thanks for reporting this!

cc @ss...@chromium.org

I don't believe we can patch the open264 code directly, so while waiting for an upstream fix we should validate the buffers before using them. There are two potential problem areas [webrtc](https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/modules/video_coding/codecs/h264/h264_encoder_impl.cc;l=511?q=h264_encoder_im&ss=chromium) and [webcodecs](https://source.chromium.org/chromium/chromium/src/+/main:media/video/openh264_video_encoder.cc;l=476?ss=chromium%2Fchromium%2Fsrc).

From reading the code I suspect both could be impacted - though webrtc would require the use of insertable streams. If I'm reading the code right we would end up with an [adapter](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/webrtc/convert_to_webrtc_video_frame_buffer.cc;drc=8a43c6476c78c7c28b33cabedd39d0ad98a0ede1;bpv=1;bpt=0;l=40) that mirrors the `media::VideoFrame` in a `webrtc::VideoFrameBuffer` and thus would have the same weird stride. cc @il...@chromium.org since you know this code base well, can you help verify this is the case - or is there some point at which we copy the data and remove the extra stride?

cc @eu...@chromium.org and @da...@chromium.org if you guys handle webcodecs I can take care of webrtc.

### il...@chromium.org (2026-03-12)

It's true that this weird stride will be forwarded all the way to the encoder, but the webrtc::VideoFrameBuffer would forward correct values to the encoders.

I've checked every code I could find in chromium code base: we always use separate U and V strides, never confusing them. We pass correct ones to the openH264, so I'm pretty sure there's nothing we have to fix in chrome/webrtc.

### je...@gmail.com (2026-03-12)

deleted

### sp...@chromium.org (2026-03-12)

Re [comment#6](https://issues.chromium.org/issues/491655161#comment6) - This isn't a bug in Chromium per se no, the bug lies in the OpenH264 source code. That's the one that is assuming U and V strides are the same. But that is much harder to fix in a timely manner. Given your comment, it sounds like it is indeed the case that weird U/V strides can be carried all the way from JS to OpenH264 triggering that bug.

I'm creating a workaround in h264\_encoder\_impl.cc to reject frames that have different U and V strides while we try to get the actual root cause fixed.

### il...@chromium.org (2026-03-12)

Re #8, That's the reasonable workaround for now. No camera/canvas/decoder would produce unequal strides. Only insrtable streams with very manual approach would do so. I doubt it's used often, maybe even nowhere in the wild.

### dx...@google.com (2026-03-12)

Project: src  

Branch:  main  

Author:  Erik Språng [sprang@webrtc.org](mailto:sprang@webrtc.org)  

Link:    <https://webrtc-review.googlesource.com/456121>

Add workaround for OpenH264 related to U/V strides.

---


Expand for full commit details
```
     
    This CL adds a workaround for a bug in OpenH264, where using an input 
    frame where the U and V strides are different may result in a crash. 
     
    This fix should be removed once the root cause has been addressed. 
     
    Bug: chromium:491655161 
    Change-Id: I2e8bccefab3ffcd08bf1e086763407ceb461bba7 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/456121 
    Reviewed-by: Sergey Silkin <ssilkin@webrtc.org> 
    Commit-Queue: Sergey Silkin <ssilkin@webrtc.org> 
    Auto-Submit: Erik Språng <sprang@webrtc.org> 
    Cr-Commit-Position: refs/heads/main@{#47131}

```

---

Files:

- M `modules/video_coding/codecs/h264/h264_encoder_impl.cc`
- M `modules/video_coding/codecs/h264/h264_encoder_impl_unittest.cc`

---

Hash: 7c36f795d925c3f08fb89611166cc6b2e2de02a6  

Date: Thu Mar 12 10:55:13 2026


---

### sp...@chromium.org (2026-03-12)

WebRTC workaround just landed.

@eu...@chromium.org can you handle the WebCodecs part?

### eu...@chromium.org (2026-03-12)

WebCodecs can't enforce strideY==strideU without seriously breaking the encoding API.
This is the nature of API the data and its come from the website.
Why can't we fix line 1416 in `wels_preprocess.cpp`?

### eu...@chromium.org (2026-03-12)

How do we roll OpenH264? Should we fork it?

### dx...@google.com (2026-03-12)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7662057>

Roll WebRTC from 201168a998a4 to 3e0a723522b8 (22 revisions)

---


Expand for full commit details
```
     
    https://webrtc.googlesource.com/src.git/+log/201168a998a4..3e0a723522b8 
     
    2026-03-12 philipp.hancke@googlemail.com build: gn_check_autofix should retain blank lines, comments and # keep tagged lines 
    2026-03-12 mbonadei@webrtc.org Revert "Roll chromium_revision b937d39273..8fdfcb5d76 (1597657:1597876)" 
    2026-03-12 mbonadei@webrtc.org Revert "Roll chromium_revision 8fdfcb5d76..94ef474520 (1597876:1598026)" 
    2026-03-12 mbonadei@webrtc.org Revert "Roll chromium_revision 94ef474520..68ba4ea02a (1598026:1598147)" 
    2026-03-12 mbonadei@webrtc.org Revert "Roll chromium_revision 68ba4ea02a..42535d5df1 (1598147:1598261)" 
    2026-03-12 terelius@webrtc.org Remove unsupported python event log analyzer 
    2026-03-12 hta@webrtc.org Reland "Fix payload type allocation issues for Audio RED and MID recycling." 
    2026-03-12 terelius@webrtc.org Run iwyu on current CL if no files are given on command line 
    2026-03-12 sprang@webrtc.org Add workaround for OpenH264 related to U/V strides. 
    2026-03-12 peah@webrtc.org Removed the AEC3 namespace 
    2026-03-12 perkj@webrtc.org Make scream  more resilient to delay spikes 
    2026-03-12 tonypo@google.com Encapsulate and make RTP sequence number available in RtpPacketInfo. 
    2026-03-12 hta@webrtc.org pc: Enhance stability integration test 
    2026-03-12 philipp.hancke@googlemail.com build: clean up api/BUILD.gn 
    2026-03-12 jleconte@webrtc.org Make the targets leaking through 'libjingle_peerconnection_api' public 
    2026-03-12 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision 68ba4ea02a..42535d5df1 (1598147:1598261) 
    2026-03-12 webrtc-version-updater@webrtc-ci.iam.gserviceaccount.com Update WebRTC code version (2026-03-12T04:11:50). 
    2026-03-12 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision 94ef474520..68ba4ea02a (1598026:1598147) 
    2026-03-11 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision 8fdfcb5d76..94ef474520 (1597876:1598026) 
    2026-03-11 hta@webrtc.org Remove some unused calls from Video Engine classes 
    2026-03-11 tommi@webrtc.org Move Call::receive_time_calculator_ to network thread 
    2026-03-11 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision b937d39273..8fdfcb5d76 (1597657:1597876) 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/webrtc-chromium-autoroll 
    Please CC webrtc-chromium-sheriffs-robots@google.com,webrtc-infra@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in WebRTC: https://bugs.chromium.org/p/webrtc/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Bug: chromium:491655161 
    Tbr: webrtc-chromium-sheriffs-robots@google.com 
    Change-Id: I3699d3034531fdc04b2a887b6ed971916eefd309 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7662057 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1598562}

```

---

Files:

- M `DEPS`
- M `third_party/webrtc`

---

Hash: [ea196525aa028591b2a51db3502c017613bc233c](https://chromiumdash.appspot.com/commit/ea196525aa028591b2a51db3502c017613bc233c)  

Date: Thu Mar 12 18:17:07 2026


---

### eu...@chromium.org (2026-03-12)

There is similar [issue](https://issues.chromium.org/issues/492213293) in `libaom` and `libvpx`

### eu...@chromium.org (2026-03-12)

Mitigation fix in progress: <https://chromium-review.googlesource.com/c/chromium/src/+/7664025>

### sp...@chromium.org (2026-03-12)

Of course we should fix that line in openh264, just suggesting that we should do a short-term mitigation in chrome. Given that the encoder is evidently not working when the U and V strides are different, rejecting early instead of crashing seems preferrable. I think it's going to be an exceedingly rare for case in real life anyway. Different strides between Y and UV sure, but between U and V specifically seems odd.

Anyway, as far as I know we need to file an issue with OpenH264, then the a fix needs to be landed, then a release be made, and then we can roll a dependency update in Chromium. Sounds like that could take a little while and will for certain not be cherry-pickable?

### sp...@chromium.org (2026-03-12)

...and wow, interesting that libaom and libvpx have made the same (incorrect) assumptions!
Mitigation lgtm.

### dx...@google.com (2026-03-13)

Project: chromium/src  

Branch:  main  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7664025>

media: Fix OOB read in software encoders when U-stride != V-stride

---


Expand for full commit details
```
     
    When an I420 VideoFrame is created with different strides for the U and 
    V planes (e.g., via WebCodecs), passing it to software encoders (AV1, 
    VPX, OpenH264) can cause an out-of-bounds read. These encoder libraries 
    often assume or internally convert to a representation with a single 
    chroma stride, ignoring the V plane stride. 
     
    This change forces a manual copy of the frame before encoding if the U 
    and V strides do not match, ensuring safe processing. 
     
    Bug: 492213293, 491655161 
    Change-Id: Ifcf324ff2201fbb56d53e65cc98261790b9b170b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7664025 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Reviewed-by: Erik Språng <sprang@chromium.org> 
    Reviewed-by: Thomas Guilbert <tguilbert@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1598780}

```

---

Files:

- M `media/video/av1_video_encoder.cc`
- M `media/video/openh264_video_encoder.cc`
- M `media/video/software_video_encoder_test.cc`
- M `media/video/vpx_video_encoder.cc`

---

Hash: [c177cadab426b31ccc2d3a1bca86a990004b2709](https://chromiumdash.appspot.com/commit/c177cadab426b31ccc2d3a1bca86a990004b2709)  

Date: Fri Mar 13 00:08:27 2026


---

### ch...@google.com (2026-03-16)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-03-17)

Security Merge Request Consideration: Requesting merge to stable (M146) because latest trunk commit (1598780) appears to be after stable branch point (1582197).
Security Merge Request Consideration: Requesting merge to beta (M147) because latest trunk commit (1598780) appears to be after beta branch point (1596535).
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

### eu...@chromium.org (2026-03-17)

> Which CLs should be backmerged?

- <https://chromium-review.googlesource.com/c/chromium/src/+/7662057>
- <https://chromium-review.googlesource.com/c/chromium/src/+/7664025>

> Has this fix been verified on Canary to not pose any stability regressions?

yes

> Does this fix pose any potential non-verifiable stability risks?

no

> Does this fix pose any known compatibility risks?

yes, WebRTC roll includes other changes

> Does it require manual verification by the test team? If so, please describe required testing.

yes, open `poc.html` from the report and make sure there is no crash

### dr...@chromium.org (2026-03-18)

No crashes in Canary, approved to merge to M146 and M147.

### dx...@google.com (2026-03-18)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7682062>

[M146] media: Fix OOB read in software encoders when U-stride != V-stride

---


Expand for full commit details
```
     
    When an I420 VideoFrame is created with different strides for the U and 
    V planes (e.g., via WebCodecs), passing it to software encoders (AV1, 
    VPX, OpenH264) can cause an out-of-bounds read. These encoder libraries 
    often assume or internally convert to a representation with a single 
    chroma stride, ignoring the V plane stride. 
     
    This change forces a manual copy of the frame before encoding if the U 
    and V strides do not match, ensuring safe processing. 
     
    (cherry picked from commit c177cadab426b31ccc2d3a1bca86a990004b2709) 
     
    Bug: 492213293, 491655161 
    Change-Id: Ifcf324ff2201fbb56d53e65cc98261790b9b170b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7664025 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Reviewed-by: Erik Språng <sprang@chromium.org> 
    Reviewed-by: Thomas Guilbert <tguilbert@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1598780} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7682062 
    Reviewed-by: Eugene Zemtsov <eugene@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7680@{#2808} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `media/video/av1_video_encoder.cc`
- M `media/video/openh264_video_encoder.cc`
- M `media/video/software_video_encoder_test.cc`
- M `media/video/vpx_video_encoder.cc`

---

Hash: [92790c4b95aabb730b7ddf9e357be53a82c64391](https://chromiumdash.appspot.com/commit/92790c4b95aabb730b7ddf9e357be53a82c64391)  

Date: Wed Mar 18 21:38:40 2026


---

### pe...@google.com (2026-03-18)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2026-03-18)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7682079>

[M147] media: Fix OOB read in software encoders when U-stride != V-stride

---


Expand for full commit details
```
     
    When an I420 VideoFrame is created with different strides for the U and 
    V planes (e.g., via WebCodecs), passing it to software encoders (AV1, 
    VPX, OpenH264) can cause an out-of-bounds read. These encoder libraries 
    often assume or internally convert to a representation with a single 
    chroma stride, ignoring the V plane stride. 
     
    This change forces a manual copy of the frame before encoding if the U 
    and V strides do not match, ensuring safe processing. 
     
    (cherry picked from commit c177cadab426b31ccc2d3a1bca86a990004b2709) 
     
    Bug: 492213293, 491655161 
    Change-Id: Ifcf324ff2201fbb56d53e65cc98261790b9b170b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7664025 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Reviewed-by: Erik Språng <sprang@chromium.org> 
    Reviewed-by: Thomas Guilbert <tguilbert@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1598780} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7682079 
    Reviewed-by: Eugene Zemtsov <eugene@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7727@{#794} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `media/video/av1_video_encoder.cc`
- M `media/video/openh264_video_encoder.cc`
- M `media/video/software_video_encoder_test.cc`
- M `media/video/vpx_video_encoder.cc`

---

Hash: [affbad6ac46aae76e108501b30702393f2e62f1f](https://chromiumdash.appspot.com/commit/affbad6ac46aae76e108501b30702393f2e62f1f)  

Date: Wed Mar 18 22:04:53 2026


---

### eu...@chromium.org (2026-03-19)

Assigning to Erik to webrtc cherry-picks

### sp...@chromium.org (2026-03-23)

I was able to reproduce this problem with a WebRTC poc. Similar to the earlier WebCodecs-based repros, I used `autoninja -C out/Release_Asan/ chrome && ASAN_OPTIONS=detect_odr_violation=0 out/Release_Asan/chrome --enable-logging=stderr` to build and run Chrome, and then opened the attach html file. Without the fixes above, I would get a crash. With the fixes in place, I simply got an encoder failure which was handled by the usual WebRTC error handling mechanism.

Re [comment#23](https://issues.chromium.org/issues/491655161#comment23), [drubery@chromium.org](mailto:drubery@chromium.org) could you clarify if we have approval to merge the WebRTC fixes as well?
You can verify by opening the attached `webrtc_uv_stride_crash.html` file, selecting and codec and clicking start. There should be no crash or hang observed.

The two WebRTC commits in question are:

- <https://webrtc-review.git.corp.google.com/c/src/+/456203>
- <https://webrtc-review.git.corp.google.com/c/src/+/456121>

Re [comment#25](https://issues.chromium.org/issues/491655161#comment25):

1. No, this issue predates M145.
2. No, this issue predates M144.

### dr...@chromium.org (2026-03-23)

Yes, approved to merge both of those to M146 and M147.

### dx...@google.com (2026-03-24)

Project: src  

Branch:  refs/branch-heads/7727  

Author:  Erik Språng [sprang@webrtc.org](mailto:sprang@webrtc.org)  

Link:    <https://webrtc-review.googlesource.com/459700>

[M147] Add workaround for OpenH264 related to U/V strides.

---


Expand for full commit details
```
     
    This CL adds a workaround for a bug in OpenH264, where using an input 
    frame where the U and V strides are different may result in a crash. 
     
    This fix should be removed once the root cause has been addressed. 
     
    (cherry picked from commit 7c36f795d925c3f08fb89611166cc6b2e2de02a6) 
     
    Bug: chromium:491655161 
    Change-Id: I2e8bccefab3ffcd08bf1e086763407ceb461bba7 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/456121 
    Reviewed-by: Sergey Silkin <ssilkin@webrtc.org> 
    Commit-Queue: Sergey Silkin <ssilkin@webrtc.org> 
    Auto-Submit: Erik Språng <sprang@webrtc.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#47131} 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/459700 
    Commit-Queue: Erik Språng <sprang@webrtc.org> 
    Cr-Commit-Position: refs/branch-heads/7727@{#7} 
    Cr-Branched-From: 5788235ac856f62f1522d1491c4a8b00dba10c82-refs/heads/main@{#47086}

```

---

Files:

- M `modules/video_coding/codecs/h264/h264_encoder_impl.cc`
- M `modules/video_coding/codecs/h264/h264_encoder_impl_unittest.cc`

---

Hash: f74ae6a9f15350f8689fcbe390e4ec420fdbbe81  

Date: Thu Mar 12 10:55:13 2026


---

### dx...@google.com (2026-03-24)

Project: src  

Branch:  refs/branch-heads/7680  

Author:  Erik Språng [sprang@webrtc.org](mailto:sprang@webrtc.org)  

Link:    <https://webrtc-review.googlesource.com/459701>

[M146] Add workaround for OpenH264 related to U/V strides.

---


Expand for full commit details
```
     
    This CL adds a workaround for a bug in OpenH264, where using an input 
    frame where the U and V strides are different may result in a crash. 
     
    This fix should be removed once the root cause has been addressed. 
     
    (cherry picked from commit 7c36f795d925c3f08fb89611166cc6b2e2de02a6) 
     
    Bug: chromium:491655161 
    Change-Id: I2e8bccefab3ffcd08bf1e086763407ceb461bba7 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/456121 
    Reviewed-by: Sergey Silkin <ssilkin@webrtc.org> 
    Commit-Queue: Sergey Silkin <ssilkin@webrtc.org> 
    Auto-Submit: Erik Språng <sprang@webrtc.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#47131} 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/459701 
    Commit-Queue: Erik Språng <sprang@webrtc.org> 
    Cr-Commit-Position: refs/branch-heads/7680@{#4} 
    Cr-Branched-From: d1972add2a63b2a528a6471d447f82e0010b5215-refs/heads/main@{#46853}

```

---

Files:

- M `modules/video_coding/codecs/h264/h264_encoder_impl.cc`
- M `modules/video_coding/codecs/h264/h264_encoder_impl_unittest.cc`

---

Hash: 3b276ffc78cd0bebe0510d8d36522494b3e6e3cc  

Date: Thu Mar 12 10:55:13 2026


---

### sp...@chromium.org (2026-03-25)

Ah, two of the cherry-picks referenced [crbug.com/492213293](https://crbug.com/492213293) instead of this one. But all of my patches should now be included:

- <https://webrtc-review.googlesource.com/459701>
- <https://webrtc-review.googlesource.com/459700>
- <https://webrtc-review.git.corp.google.com/c/src/+/459721>
- <https://webrtc-review.git.corp.google.com/c/src/+/459702>

Can we close this bug now, or should we wait for the decision on LTS?

### sp...@chromium.org (2026-03-27)

@dr...@chromium.org I'll close this as fixed. Not sure if you want to verify.

### dr...@chromium.org (2026-03-27)

Looks fine to me.

> Can we close this bug now, or should we wait for the decision on LTS?

LTS reviewers will come along after the bug is fixed

### pe...@google.com (2026-04-01)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-04-01)

1. https://webrtc-review.git.corp.google.com/c/src/+/461440 and https://chromium-review.git.corp.google.com/c/chromium/src/+/7690549
2. Low - There were a few conflicts.
3. 146 and 147
4. Yes, the bug has existed for a long time.

### an...@google.com (2026-04-03)

Merge approved for LTS-138.

### dx...@google.com (2026-04-07)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7690549>

[M138-LTS] media: Fix OOB read in software encoders when U-stride != V-stride

---


Expand for full commit details
```
     
    When an I420 VideoFrame is created with different strides for the U and 
    V planes (e.g., via WebCodecs), passing it to software encoders (AV1, 
    VPX, OpenH264) can cause an out-of-bounds read. These encoder libraries 
    often assume or internally convert to a representation with a single 
    chroma stride, ignoring the V plane stride. 
     
    This change forces a manual copy of the frame before encoding if the U 
    and V strides do not match, ensuring safe processing. 
     
    (cherry picked from commit c177cadab426b31ccc2d3a1bca86a990004b2709) 
     
    Bug: 492213293, 491655161 
    Change-Id: Ifcf324ff2201fbb56d53e65cc98261790b9b170b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7664025 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Reviewed-by: Erik Språng <sprang@chromium.org> 
    Reviewed-by: Thomas Guilbert <tguilbert@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1598780} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7690549 
    Reviewed-by: Eugene Zemtsov <eugene@chromium.org> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Michael Ershov <miersh@google.com> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3524} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `media/video/av1_video_encoder.cc`
- M `media/video/openh264_video_encoder.cc`
- M `media/video/software_video_encoder_test.cc`
- M `media/video/vpx_video_encoder.cc`

---

Hash: [9dffa918127b05a7ced6295752d7cc93d58a0b4c](https://chromiumdash.appspot.com/commit/9dffa918127b05a7ced6295752d7cc93d58a0b4c)  

Date: Tue Apr 7 15:49:31 2026


---

### dx...@google.com (2026-04-15)

Project: src  

Branch:  refs/branch-heads/7204  

Author:  Erik Språng [sprang@webrtc.org](mailto:sprang@webrtc.org)  

Link:    <https://webrtc-review.googlesource.com/461440>

[M138-LTS] Add workaround for OpenH264 related to U/V strides.

---


Expand for full commit details
```
     
    This CL adds a workaround for a bug in OpenH264, where using an input 
    frame where the U and V strides are different may result in a crash. 
     
    This fix should be removed once the root cause has been addressed. 
     
    No-Try: True 
    Bug: chromium:491655161 
    Change-Id: I586aeaf617ccfbb93e1d237ca3681e024dc5b805 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/456121 
    Reviewed-by: Sergey Silkin <ssilkin@webrtc.org> 
    Commit-Queue: Sergey Silkin <ssilkin@webrtc.org> 
    Auto-Submit: Erik Språng <sprang@webrtc.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#47131} 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/461440 
    Reviewed-by: Erik Språng <sprang@webrtc.org> 
    Commit-Queue: Erik Språng <sprang@webrtc.org> 
    Cr-Commit-Position: refs/branch-heads/7204@{#4} 
    Cr-Branched-From: e4445e46a910eb407571ec0b0b8b7043562678cf-refs/heads/main@{#44764}

```

---

Files:

- M `modules/video_coding/codecs/h264/h264_encoder_impl.cc`
- M `modules/video_coding/codecs/h264/h264_encoder_impl_unittest.cc`

---

Hash: 7ad61a0a06fac695468b843e17b81a6ab19d0feb  

Date: Wed Apr 15 10:10:37 2026


---

### ct...@chromium.org (2026-04-15)

Downgrading renderer read to S-2 per <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md#:~:text=An%20out%2Dof%2Dbounds%20read%20in%20a%20renderer%20process>

### sp...@google.com (2026-04-16)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline with bisect. User information disclosure


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2026-05-08)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-05-08)

1. <https://chromium-review.git.corp.google.com/c/chromium/src/+/7691578> and <https://webrtc-review.git.corp.google.com/c/src/+/470720>
2. Low - There were a few conflicts.
3. 146 and 147
4. Yes, the bug has existed for a long time.

### sp...@chromium.org (2026-05-11)

cc [benzzhan@cisco.com](mailto:benzzhan@cisco.com) as point of contact at Cisco.

### dx...@google.com (2026-05-18)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7691578>

[M144-LTS] media: Fix OOB read in software encoders when U-stride != V-stride

---


Expand for full commit details
```
     
    When an I420 VideoFrame is created with different strides for the U and 
    V planes (e.g., via WebCodecs), passing it to software encoders (AV1, 
    VPX, OpenH264) can cause an out-of-bounds read. These encoder libraries 
    often assume or internally convert to a representation with a single 
    chroma stride, ignoring the V plane stride. 
     
    This change forces a manual copy of the frame before encoding if the U 
    and V strides do not match, ensuring safe processing. 
     
    (cherry picked from commit c177cadab426b31ccc2d3a1bca86a990004b2709) 
     
    Bug: 492213293, 491655161 
    Change-Id: Ifcf324ff2201fbb56d53e65cc98261790b9b170b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7664025 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Reviewed-by: Erik Språng <sprang@chromium.org> 
    Reviewed-by: Thomas Guilbert <tguilbert@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1598780} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7691578 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Eugene Zemtsov <eugene@chromium.org> 
    Reviewed-by: Giovanni Pezzino <giovax@google.com> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4864} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `media/video/av1_video_encoder.cc`
- M `media/video/openh264_video_encoder.cc`
- M `media/video/software_video_encoder_test.cc`
- M `media/video/vpx_video_encoder.cc`

---

Hash: [8a6f963b683420534bad6f21f6769d60278653b1](https://chromiumdash.appspot.com/commit/8a6f963b683420534bad6f21f6769d60278653b1)  

Date: Mon May 18 05:27:55 2026


---

### dx...@google.com (2026-05-18)

Project: src  

Branch:  refs/branch-heads/7559  

Author:  Gyuyoung Kim [qkim@google.com](mailto:qkim@google.com)  

Link:    <https://webrtc-review.googlesource.com/470720>

[M144-LTS] Add workaround for OpenH264 related to U/V strides.

---


Expand for full commit details
```
     
    This CL adds a workaround for a bug in OpenH264, where using an input 
    frame where the U and V strides are different may result in a crash. 
     
    This fix should be removed once the root cause has been addressed. 
     
    No-Try: True 
    Bug: chromium:491655161 
    Change-Id: I3ad26a7e5670079b11b8fea8b34d0d3e4f93ae1e 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/456121 
    Reviewed-by: Sergey Silkin <ssilkin@webrtc.org> 
    Commit-Queue: Sergey Silkin <ssilkin@webrtc.org> 
    Auto-Submit: Erik Språng <sprang@webrtc.org> 
    Cr-Original-Original-Commit-Position: refs/heads/main@{#47131} 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/461440 
    Reviewed-by: Erik Språng <sprang@webrtc.org> 
    Commit-Queue: Erik Språng <sprang@webrtc.org> 
    Cr-Original-Commit-Position: refs/branch-heads/7204@{#4} 
    Cr-Original-Branched-From: e4445e46a910eb407571ec0b0b8b7043562678cf-refs/heads/main@{#44764} 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/470720 
    Cr-Commit-Position: refs/branch-heads/7559@{#6} 
    Cr-Branched-From: f680c1893f3b166b370439da52ae82d02f54969c-refs/heads/main@{#46356}

```

---

Files:

- M `modules/video_coding/codecs/h264/h264_encoder_impl.cc`
- M `modules/video_coding/codecs/h264/h264_encoder_impl_unittest.cc`

---

Hash: 805adb356b95070747a9ced81fb92498852b7a10  

Date: Fri May 8 01:50:07 2026


---

### ch...@google.com (2026-07-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### sp...@chromium.org (2026-07-06)

For completeness, uploaded upstream PR: <https://github.com/cisco/openh264/pull/3961>

## Bounty Award

> Baseline with bisect. User information disclosure

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/491655161)*
