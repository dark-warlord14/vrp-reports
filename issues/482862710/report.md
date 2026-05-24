# Missing range validation on second_chroma_qp_index_offset in H.264 PPS parser (h264_parser.cc:1151) allows out-of-spec values to reach kernel GPU drivers

| Field | Value |
|-------|-------|
| **Issue ID** | [482862710](https://issues.chromium.org/issues/482862710) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media |
| **Platforms** | Linux, Windows, ChromeOS |
| **CVE IDs** | CVE-2022-21813, CVE-2022-21814 |
| **Reporter** | lu...@icloud.com |
| **Assignee** | eu...@chromium.org |
| **Created** | 2026-02-09 |
| **Bounty** | $10,000.00 |

## Description

---

### Report description

Missing range validation on second\_chroma\_qp\_index\_offset in H.264 PPS parser (h264\_parser.cc:1151) allows out-of-spec values to reach kernel GPU drivers

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/chromium/src/+/main/media/parsers/h264_parser.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

At `h264_parser.cc:1151`, `second_chroma_qp_index_offset` is read via `READ_SE_OR_RETURN` with no range check. The H.264 spec (ITU-T H.264 §7.4.2.2) requires this value to be in [-12, +12]. The identical sibling field `chroma_qp_index_offset` IS validated 33 lines earlier at line 1118:

```
// Line 1118: validated:
READ_SE_OR_RETURN(&pps->chroma_qp_index_offset);
IN_RANGE_OR_RETURN(pps->chroma_qp_index_offset, -12, 12);

// Line 1151: not validated:
READ_SE_OR_RETURN(&pps->second_chroma_qp_index_offset);
// Missing: IN_RANGE_OR_RETURN(pps->second_chroma_qp_index_offset, -12, 12);

```

`READ_SE_OR_RETURN` accepts exp-Golomb coded values up to approximately ±2³⁰. The unvalidated value is then copied directly into kernel GPU driver parameter buffers by all three hardware decoder backends, where int→int8 narrowing maps the full range to [-128, +127] — of which 231 values fall outside the spec-required [-12, +12]:

- **D3D11** (`d3d11_h264_accelerator.cc:207`): `pic_param.second_chroma_qp_index_offset = pps->second_chroma_qp_index_offset` → `DXVA_PicParams_H264` (`CHAR`)
- **VA-API** (`h264_vaapi_video_decoder_delegate.cc:171`): same pattern → `VAPictureParameterBufferH264` (`signed char`)
- **V4L2** (`v4l2_video_decoder_delegate_h264.cc:306`): same pattern → `v4l2_ctrl_h264_pps` (`__s8`)

Source analysis of Intel's open-source media-driver confirms the driver does NOT clamp the value. In `decode_avc_basic_feature.cpp:243`, the driver detects the violation and logs `DECODE_WARNINGMESSAGE("Conflict with H264 Spec!")` but does not correct the value — unlike other fields in the same function that are corrected after detection. The unclamped value is then written directly to GPU hardware command buffers (`cmd.DW3.SecondChromaQpOffset = avcPicParams->second_chroma_qp_index_offset`) across gen8/gen9/gen11/gen12.

Chrome's built-in FFmpeg software decoder rejects the malformed stream, but the hardware decode path (default on all desktop platforms) accepts and processes it. Confirmed via `chrome://media-internals` on:

- Intel Arc 130V (Windows 11 / D3D11VideoDecoder)
- NVIDIA RTX 2070 Super (Windows 11 / D3D11VideoDecoder)
- Intel Alder Lake (ChromeOS / OOPVideoDecoder)

**Fix:** one line matching the existing pattern:

```
IN_RANGE_OR_RETURN(pps->second_chroma_qp_index_offset, -12, 12);

```

**Reproduction:** Open the attached `off100_qp25_cabac.mp4` in Chrome on any desktop platform with hardware video decode enabled. Navigate to `chrome://media-internals` and observe that `D3D11VideoDecoder` (Windows) or `VaapiVideoDecoder` (Linux/ChromeOS) accepts and processes the stream. For comparison, note that Chrome's built-in FFmpeg software decoder rejects the same file with an invalid data error. A second PoC with `second_chroma_qp_index_offset = -128` (negative OOB index into the QPC table) was also tested and accepted by the hardware decoder.

Attached files:

off100\_qp25\_cabac.mp4 — Proof-of-concept H.264 High Profile MP4 with second\_chroma\_qp\_index\_offset set to 100 (spec requires [-12, +12]). Opens in Chrome via D3D11VideoDecoder/VaapiVideoDecoder hardware decode path. FFmpeg software decoder rejects it.

poc\_chroma\_qp\_long\_neg128.mp4 — 15-second variant with second\_chroma\_qp\_index\_offset set to -128 (negative OOB into QPC table). 450 frames with varying slice\_qp\_delta to hit different out-of-range qPi values. Also accepted by hardware decoder.

media-internals.txt — chrome://media-internals JSON log from Windows 11 / NVIDIA RTX 2070 Super showing FFmpegVideoDecoder rejection followed by successful D3D11VideoDecoder fallback and full stream processing.

poc\_chroma\_qp.py — Python script that generates the PoC MP4 from scratch. Self-contained, no external dependencies. Can be modified to produce variants with arbitrary second\_chroma\_qp\_index\_offset values.

poc\_v2.py — Alternative PoC generator that patches a real ffmpeg-encoded H.264 stream, modifying only the second\_chroma\_qp\_index\_offset field in the existing PPS bitstream. Generates off100\_qp25\_cabac.mp4. Requires ffmpeg

#### Impact analysis

Chromium's H.264 parser is the trust boundary between untrusted web content and kernel GPU drivers. Attacker-controlled out-of-spec values reach kernel drivers when a user visits a page containing a malicious `<video>` element. The Chrome GPU sandbox does not mitigate this — the GPU process is designed to make D3D11/VA-API/V4L2 calls, so the malformed parameters reach the kernel through the sandbox's allowed syscall surface.

GPU drivers use this value to compute chroma QP (`qPi = QPY + second_chroma_qp_index_offset`) and index into a 52-entry QPC lookup table. With the PoC values (offset=100, slice\_qp\_delta=25), `qPi` reaches 151, overshooting the table by ~100 entries. With the negative variant (offset=-128), `qPi` goes deeply negative, indexing before the array start. If any driver fails to clamp before the lookup, this is a kernel out-of-bounds read.

CVE-2022-21813 and CVE-2022-21814 (NVIDIA) were this exact bug class — out-of-range video decoder parameters causing kernel OOB access. Chromium cannot delegate validation to downstream drivers across all vendors, architectures, and firmware versions. Intel's open-source driver confirms this: it detects but does not correct the violation. ARM/Mali/Qualcomm V4L2 firmware-based decoders, where QPC table lookups occur in software rather than fixed-function silicon, represent the highest-risk targets.

No crashes were observed on tested hardware (Intel, NVIDIA), consistent with fixed-function decode units that truncate at the bitfield level. However, the parser must enforce spec compliance regardless of individual driver behavior — this is a defense-in-depth requirement at a critical trust boundary.

---

### The cause

#### What version of Chrome have you found the security issue in?

144.0.7559.133 + stable (Windows 11, 64-bit)

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a non-sandboxed process)

#### How would you like to be publicly acknowledged for your report?

Luke Francis

## Attachments

- [off100_qp25_cabac.mp4](attachments/off100_qp25_cabac.mp4) (video/mp4, 8.7 KB)
- [poc_chroma_qp_long_neg128.mp4](attachments/poc_chroma_qp_long_neg128.mp4) (video/mp4, 1.3 MB)
- [media-internals.txt](attachments/media-internals.txt) (text/plain, 15.3 KB)
- [poc_chroma_qp.py](attachments/poc_chroma_qp.py) (text/x-python-script, 18.6 KB)
- [poc_v2.py](attachments/poc_v2.py) (text/x-python-script, 12.3 KB)
- [off100_qp25_cabac.mp4](attachments/off100_qp25_cabac.mp4) (video/mp4, 8.7 KB)
- [poc_v2.py](attachments/poc_v2.py) (text/x-python-script, 12.3 KB)
- [Chromium VA-API PoC Test Results.txt](attachments/Chromium VA-API PoC Test Results.txt) (text/plain, 2.2 KB)
- [media_internals_output.txt](attachments/media_internals_output.txt) (text/plain, 4.2 KB)
- [media-internals (2).txt](attachments/media-internals (2).txt) (text/plain, 8.6 KB)
- [poc_v2.py](attachments/poc_v2.py) (text/x-python, 12.3 KB)
- [media-internals__18_.txt](attachments/media-internals_18_.txt) (text/plain, 9.8 KB)

## Timeline

### lu...@icloud.com (2026-02-09)

I just tested both PoCs on Linux with Ubuntu 24.04, an Intel Arc 130V (Lunar Lake), the xe kernel driver, iHD 24.3.4, libva 2.22.0, and Chrome 144.0.7559.132.
VaapiVideoDecoder was selected for both files. For the neg128 PoC, the keyframe carrying the malformed PPS was the one that actually decoded successfully through the hardware path. That's frame 0, the frame where second_chroma_qp_index_offset = -128 is active. The driver only errored on the following packet, which was a dependent P-frame at timestamp 33333. Chrome didn't catch the bad value and reject it at the PPS level. The iHD driver ingested the malformed PPS, performed its chroma QP computation using the out-of-spec value, and returned a decoded frame. The fallback to FFmpeg only triggered when the next frame failed.
There were no kernel faults or GPU crashes on this hardware, which is consistent with iHD doing Clip3 internally as was predicted.

### li...@chromium.org (2026-02-12)

Adding srosek since you have the "luck" of touching this part of the code last so you are likely most familiar with it. Also CCing media owners.

It looks like it makes most sense for us to validate the out of spec values ourselves, since we can't rely on the hardware drivers to do this for us.

Does Android also default to using hardware drivers, or would it use ffmpeg to decode in this case?

### da...@chromium.org (2026-02-12)

Adding this validation sgtm, thanks for the report! Our position is not to rely on any hardening that may or may not exist at the driver level, so this should be validated in our parsers. Feel free to reassign to me or Eugene.

### dx...@google.com (2026-02-13)

Project: chromium/src  

Branch:  main  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7572949>

media: Validate second\_chroma\_qp\_index\_offset range in H.264 parser

---


Expand for full commit details
```
     
    The H.264 spec requires second_chroma_qp_index_offset to be in the 
    range [-12, 12]. Previously, this value was read without validation. 
     
    Bug: 482862710 
    Change-Id: Ie40f42ff677d436a10c53779f55fcfb8279564dd 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7572949 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1584344}

```

---

Files:

- M `media/parsers/h264_parser.cc`
- M `media/parsers/h264_parser_unittest.cc`

---

Hash: [c4726aab7bf1e15741b090d8b401515bf7be2d6b](https://chromiumdash.appspot.com/commit/c4726aab7bf1e15741b090d8b401515bf7be2d6b)  

Date: Fri Feb 13 01:01:02 2026


---

### ch...@google.com (2026-02-13)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-13)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@google.com (2026-02-13)

Security Merge Request Consideration: Requesting merge to extended stable (M144) because latest trunk commit (1584344) appears to be after extended stable branch point (1552494).
Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1584344) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1584344) appears to be after beta branch point (1582197).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dx...@google.com (2026-02-13)

Project: chromium/src  

Branch:  main  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7574217>

media: Add missing range checks in H.264 parser

---


Expand for full commit details
```
     
    This CL adds missing range checks for the following H.264 syntax elements, 
    as required by the ITU-T H.264 specification: 
     
    - pic_parameter_set_id: [0, 255] (7.4.2.2) 
    - idr_pic_id: [0, 65535] (7.4.3) 
    - changing_slice_group_idc: [0, 2] (D.2.8) 
     
    Bug: 482862710 
    Change-Id: If84039d17c31bcd4a8164eb9a74c5457a423986e 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7574217 
    Commit-Queue: Ted (Chromium) Meyer <tmathmeyer@chromium.org> 
    Auto-Submit: Eugene Zemtsov <eugene@chromium.org> 
    Reviewed-by: Ted (Chromium) Meyer <tmathmeyer@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1584796}

```

---

Files:

- M `media/parsers/h264_parser.cc`
- M `media/parsers/h264_parser_unittest.cc`

---

Hash: [b4b85bc55bd540692ceb82e291c3ffb99bcd1daf](https://chromiumdash.appspot.com/commit/b4b85bc55bd540692ceb82e291c3ffb99bcd1daf)  

Date: Fri Feb 13 19:23:53 2026


---

### dx...@google.com (2026-02-13)

Project: chromium/src  

Branch:  main  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7577373>

media: Add missing range checks in H.265 parser

---


Expand for full commit details
```
     
    This CL adds missing range checks for the following H.265 syntax elements, 
    as required by the ITU-T H.265 specification: 
     
     - vps_max_layers_minus1: [0, 62] (7.4.3.1) 
     - vps_max_layer_id: [0, 62] (7.4.3.1) 
     - slice_type: [0, 2] (7.4.7.1) 
     - alpha_channel_use_idc: [0, 2] (F.7.4.3.1.1) 
     
    Bug: 482862710 
    Change-Id: I629d7fba4fbdcea889166ccf78aaee2af830a1d7 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7577373 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Reviewed-by: Ted (Chromium) Meyer <tmathmeyer@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1584897}

```

---

Files:

- M `media/parsers/h265_parser.cc`

---

Hash: [452f3fa28564cadf807215ce61293c6f20e8f2ef](https://chromiumdash.appspot.com/commit/452f3fa28564cadf807215ce61293c6f20e8f2ef)  

Date: Fri Feb 13 22:00:18 2026


---

### ch...@google.com (2026-02-14)

**Merge approved:** your change passed merge requirements and is auto-approved for M146. Please go ahead and merge the CL to branch 7680 (refs/branch-heads/7680) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-02-14)

Merge review required: M145 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: andywu (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-02-14)

Merge review required: M144 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### eu...@chromium.org (2026-02-17)

> Open the attached off100\_qp25\_cabac.mp4 in Chrome on any desktop platform with hardware video decode enabled. Navigate to chrome://media-internals and observe that D3D11VideoDecoder (Windows) or VaapiVideoDecoder (Linux/ChromeOS) accepts and processes the stream.

Can't reproduce the issue on Chrome stable with these steps. h264\_parser safely rejects these files with the following messages:

```
[33384:30744:0217/144233.359:ERROR:media\gpu\h264_decoder.cc:1480] : SetStream
[33384:30744:0217/144233.359:ERROR:media\parsers\h264_parser.cc:402] : Could not find start code, end of stream?
[33384:30744:0217/144233.359:ERROR:media\parsers\h264_parser.cc:537] : Could not find next NALU, bytes left in stream: 3081

```
```
[33384:30744:0217/144303.054:ERROR:media\gpu\windows\d3d11_h264_accelerator.cc:63] : D3D11H264Accelerator
[33384:30744:0217/144303.054:ERROR:media\gpu\h264_decoder.cc:145] : Reset
[33384:30744:0217/144303.056:ERROR:media\gpu\h264_decoder.cc:1480] : SetStream
[33384:30744:0217/144303.056:ERROR:media\parsers\h264_parser.cc:402] : Could not find start code, end of stream?
[33384:30744:0217/144303.056:ERROR:media\parsers\h264_parser.cc:537] : Could not find next NALU, bytes left in stream: 8203

```

### dx...@google.com (2026-02-18)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7584942>

[M146] media: Validate second\_chroma\_qp\_index\_offset range in H.264 parser

---


Expand for full commit details
```
     
    The H.264 spec requires second_chroma_qp_index_offset to be in the 
    range [-12, 12]. Previously, this value was read without validation. 
     
    (cherry picked from commit c4726aab7bf1e15741b090d8b401515bf7be2d6b) 
     
    Bug: 482862710 
    Change-Id: Ie40f42ff677d436a10c53779f55fcfb8279564dd 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7572949 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1584344} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7584942 
    Reviewed-by: Ted (Chromium) Meyer <tmathmeyer@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7680@{#571} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `media/parsers/h264_parser.cc`
- M `media/parsers/h264_parser_unittest.cc`

---

Hash: [72a736bf8a52df691c37dd2ef8f59de29670e1d7](https://chromiumdash.appspot.com/commit/72a736bf8a52df691c37dd2ef8f59de29670e1d7)  

Date: Wed Feb 18 00:30:23 2026


---

### lu...@icloud.com (2026-02-18)

Just tested off100_qp25_cabac.mp4 on Chrome 145.0.7632.76 stable (macOS, VideoToolbox) and it still reproduces. FFmpeg rejects, falls back to VideoToolbox, which accepts and fully decodes the stream. Logs attached.

The errors you're hitting look like NALU-level failures, not PPS validation so I think the attachments may have been corrupted by the issue tracker. You can regenerate from poc_v2.py (also attached), just needs ffmpeg.

Thanks,
Luke

### eu...@chromium.org (2026-02-18)

This is probably platform specific, I still get the same errors on Windows. I'll try Mac

### lu...@icloud.com (2026-02-18)

I just reproduced again on Chrome 145.0.7632.76 stable on Windows. Log attached. It's the same sequence as the original report where FFmpegVideoDecoder rejects, fallback, D3D11VideoDecoder accepts and completes. Are you testing with a file freshly generated from poc_v2.py, or the attached mp4? It might be getting corrupted on the download but poc_v2.py generates a fresh batch of mp4s.

Thanks,
Luke

### eu...@chromium.org (2026-02-18)

I was using the freshly generated file. There's no sing in the attached log that second\_chroma\_qp\_index\_offset was actually parsed and the out of bounds value reached GPU driver.

### eu...@chromium.org (2026-02-18)

same happens on Mac. H264Parser::ParsePPS is never called

```
[13439:1784320:0217/224928.778182:ERROR:media/parsers/h264_parser.cc:402] : Could not find start code, end of stream?
[13439:1784320:0217/224928.778557:ERROR:media/parsers/h264_parser.cc:537] : Could not find next NALU, bytes left in stream: 8203
[13439:1784320:0217/224929.847387:ERROR:media/parsers/h264_parser.cc:402] : Could not find start code, end of stream?
[13439:1784320:0217/224929.847422:ERROR:media/parsers/h264_parser.cc:537] : Could not find next NALU, bytes left in stream: 8203

```

### ch...@google.com (2026-02-18)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2026-02-18)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### eu...@chromium.org (2026-02-18)

> Was this issue a regression for the milestone it was found in?

no

> Is this issue related to a change or feature merged after the latest LTS Milestone?

no

I don't think we need to merge it to M144

### qk...@google.com (2026-02-19)

Added Not-Applicable-138 because the author didn't think this fix needed to be merged back to M144 according to the [comment #23](https://issues.chromium.org/issues/482862710#comment23). Thus, M138 doesn't need to have this fix as well.

### dr...@chromium.org (2026-02-19)

For the merge considerations - we would normally merge an S1, but if I understand correctly we never identified any drivers that are vulnerable to this, right? So there's no immediate security harm to letting this rollout in M146?

### li...@chromium.org (2026-02-19)

We did identify desktop drivers that were vulnerable to this, I was only wondering if there was any indication Android may not be vulnerable but that seems unlikely.

### dr...@chromium.org (2026-02-19)

Got it. In that case we definitely want to merge to M144. Approving the merges.

### sr...@chromium.org (2026-02-19)

@eu...@chromium.org  pls help complete the merges before 12pm PST tomorrow so they can be part of the respin , i am cutting RC tomorrwo 

### dx...@google.com (2026-02-20)

Project: chromium/src  

Branch:  refs/branch-heads/7632  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7596335>

[M145] media: Validate second\_chroma\_qp\_index\_offset range in H.264 parser

---


Expand for full commit details
```
     
    The H.264 spec requires second_chroma_qp_index_offset to be in the 
    range [-12, 12]. Previously, this value was read without validation. 
     
    (cherry picked from commit c4726aab7bf1e15741b090d8b401515bf7be2d6b) 
     
    Bug: 482862710 
    Change-Id: Ie40f42ff677d436a10c53779f55fcfb8279564dd 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7572949 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1584344} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7596335 
    Reviewed-by: Ted (Chromium) Meyer <tmathmeyer@chromium.org> 
    Reviewed-by: Eugene Zemtsov <eugene@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7632@{#3038} 
    Cr-Branched-From: 0bbdf2913883391365383b0a5dfe7bf9fd1a5213-refs/heads/main@{#1568190}

```

---

Files:

- M `media/parsers/h264_parser.cc`
- M `media/parsers/h264_parser_unittest.cc`

---

Hash: [bb3be633a35be4274f7baf64cb2e180f234b0e10](https://chromiumdash.appspot.com/commit/bb3be633a35be4274f7baf64cb2e180f234b0e10)  

Date: Fri Feb 20 00:14:16 2026


---

### dx...@google.com (2026-02-20)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7595179>

[M144]media: Validate second\_chroma\_qp\_index\_offset range in H.264 parser

---


Expand for full commit details
```
     
    The H.264 spec requires second_chroma_qp_index_offset to be in the 
    range [-12, 12]. Previously, this value was read without validation. 
     
    (cherry picked from commit c4726aab7bf1e15741b090d8b401515bf7be2d6b) 
     
    Bug: 482862710 
    Change-Id: Ie40f42ff677d436a10c53779f55fcfb8279564dd 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7572949 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1584344} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7595179 
    Reviewed-by: Ted (Chromium) Meyer <tmathmeyer@chromium.org> 
    Reviewed-by: Eugene Zemtsov <eugene@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4732} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `media/parsers/h264_parser.cc`
- M `media/parsers/h264_parser_unittest.cc`

---

Hash: [effb3a5e7ee51a5cfec63f9cb3bb22fadbad6ae6](https://chromiumdash.appspot.com/commit/effb3a5e7ee51a5cfec63f9cb3bb22fadbad6ae6)  

Date: Fri Feb 20 00:58:57 2026


---

### sp...@google.com (2026-03-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
Baseline. Memory corruption in a highly privileged process (e.g. GPU, network processes).


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### lu...@icloud.com (2026-03-06)

Thank you so much! Have a great day!

### qk...@google.com (2026-04-08)

Added Not-Applicable-144 because the author didn't think this fix needed to be merged back to M144 according to the comment #23. 

### ch...@google.com (2026-05-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Baseline. Memory corruption in a highly privileged process (e.g. GPU, network processes).

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/482862710)*
