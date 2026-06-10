# TOCTOU in NdkVideoEncodeAccelerator: shared memory re-read after write allows attacker-controlled bitstream parsing

| Field | Value |
|-------|-------|
| **Issue ID** | [483109205](https://issues.chromium.org/issues/483109205) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Media |
| **Platforms** | Android |
| **Reporter** | lu...@icloud.com |
| **Assignee** | eu...@chromium.org |
| **Created** | 2026-02-10 |
| **Bounty** | Confirmed (amount unknown) |

## Description

VULNERABILITY DETAILS

The Android NDK Video Encode Accelerator (NdkVideoEncodeAccelerator) writes encoded bitstream data into an UnsafeSharedMemoryRegion, then re-reads from that same shared memory to parse temporal scalability metadata. The renderer retains write access to this region. A compromised renderer can mutate the buffer contents between the encoder's write and the metadata parse, feeding attacker-controlled bitstream data to H.264, HEVC, VP9, and AV1 parsers running in the GPU process.

The vulnerable code is in media/gpu/android/ndk_video_encode_accelerator.cc:
- Line 1460: Encoder output copied into shared memory via output_dst.copy_prefix_from
- Line 1487: svc_parser_->ParseChunk() re-reads from the same shared memory span

Between these two lines, the renderer can overwrite the buffer with crafted NALUs/OBUs. The parsers (H264Parser, H265NaluParser, Vp9Parser, libgav1 ObuParser) were not designed to handle adversarial input on this code path. They expect trusted encoder output.

Other platform encoders are not affected. VAAPI derives metadata from encoder-internal state (vaapi_video_encode_accelerator.cc:524-556). V4L2 parses from its kernel mmap'd capture buffer before copying to shared memory (v4l2_video_encode_accelerator.cc:1467-1485). MediaFoundation parses from its MF COM buffer (media_foundation_video_encode_accelerator_win.cc:2398-2413). Only the NDK path parses from the shared memory span after writing to it.

The fix is to move the ParseChunk() call to operate on the MediaCodec output buffer (out_buffer_data) before copying to shared memory, matching the pattern used by V4L2 and MediaFoundation.

VERSION

Chrome Version: trunk (verified against current main branch)
Operating System: Android (all versions using NDK MediaCodec encoder)

REPRODUCTION CASE

A standalone PoC demonstrates the race condition by simulating the GPU and renderer threads operating on the same UnsafeSharedMemoryRegion. Results: 1.9 million race wins out of 62 million iterations (3.06% hit rate) in 2 seconds.

The PoC is attached. It can also be built as a Chromium unit test.

The race window exists between ndk_video_encode_accelerator.cc lines 1460 and 1487. In real exploitation, the attacker substitutes arbitrary H.264/VP9/AV1 bitstream data, feeding crafted input to TemporalScalabilityIdExtractor::ParseChunk() (media/parsers/temporal_scalability_id_extractor.cc:56), which dispatches to:

- ParseH264 (line 77): H264Parser::AdvanceToNextNALU on attacker data
- ParseHEVC (line 108): H265NaluParser::AdvanceToNextNALU on attacker data
- ParseVP9 (line 132): Vp9Parser::ParseNextFrame on attacker data, reads ref_frame_idx[] used to index into vp9_ref_buffer_[kVp9NumRefFrames=8]
- ParseAV1 (line 175): libgav1::ObuParser::ParseOneFrame on attacker data, complex parser touching DecoderState and BufferPool

The VP9 and AV1 paths maintain persistent reference frame state across frames, so corrupted state cascades to subsequent frames.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: GPU process. Attacker-controlled data reaches bitstream parsers. Impact depends on parser robustness to adversarial input. Potential outcomes include wrong metadata propagation, parser state corruption, and possible out-of-bounds reads in complex parsers (especially libgav1).

CREDIT INFORMATION

Reporter credit: Luke Francis

## Attachments

- [M-061-F02_poc.cc](attachments/M-061-F02_poc.cc) (text/x-c++src, 9.6 KB)

## Timeline

### ts...@google.com (2026-02-10)

Did not attempt reproduction due to time constraints, but parsing directly from shared memory without copying into a private buffer is a known bad pattern.  Assigning per author of code.  Setting found-in based on age of code to extended-stable.

### da...@chromium.org (2026-02-10)

I disagree that the parsers aren't designed to handle adversarial data. They're written with the understanding that the contents are fully attacker controlled. So long as the buffers remain the same size, I'm not sure there exist issues that would result in anything other than controlled error or garbled decoding.

Are you able to demonstrate any failures of the parsers?

### lu...@icloud.com (2026-02-11)

I tested under ASAN with concurrent buffer mutation during parsing across all three codecs. The parsers are structurally safe against this because they read into locals before bounds-checking, so mid-parse mutations don't produce memory safety violations. So yes. the impact is limited to garbled temporal metadata. Still worth fixing as a one-liner to match the pattern the other platform encoders use, but the severity case for memory corruption isn't there. Thank you for triaging this. Have a good night :)

Luke

### ch...@google.com (2026-02-11)

Setting milestone because of s0/s1 severity.

### dx...@google.com (2026-02-11)

Project: chromium/src  

Branch:  main  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7567414>

media: Fix race condition in NDK VEA's temporal scalability parsing

---


Expand for full commit details
```
     
    Previously, the encoder copied bitstream data to shared memory and then 
    read it back for metadata parsing. This created a race window where a 
    compromised renderer could modify the shared memory before the browser 
    parsed it. 
     
    Bug: 483109205 
    Change-Id: Ic6aec49b840c03fed1b01e2f9c2e553e44eec158 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7567414 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1583529}

```

---

Files:

- M `media/gpu/android/ndk_video_encode_accelerator.cc`

---

Hash: [cf230cf0cda34477afd4c14096ffc6692fa79994](https://chromiumdash.appspot.com/commit/cf230cf0cda34477afd4c14096ffc6692fa79994)  

Date: Wed Feb 11 22:34:45 2026


---

### lu...@icloud.com (2026-04-23)

Hey, this has been at reward-topanel for ~2 months, any update on when the panel might review? Thank you.

### ch...@google.com (2026-05-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### sp...@google.com (2026-05-26)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

No vulnerability demonstrated

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### lu...@icloud.com (2026-05-27)

deleted

## Bounty Award

> No vulnerability demonstrated
> 
> 
> Note that the fact that this issue is not being rewarded does not mean
> that the product team won't fix the issue. We have filed a bug with the product
> team and they will review your report and decide if a fix is required. We'll
> let you know if the issue was fixed.
> 
> Regards, \
> Google Security Bot
> 
> *How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/483109205)*
