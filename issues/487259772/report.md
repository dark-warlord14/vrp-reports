# Out-of-bounds heap read in VP9 encoder via WebCodecs VideoEncoder dimension reconfiguration

| Field | Value |
|-------|-------|
| **Issue ID** | [487259772](https://issues.chromium.org/issues/487259772) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>WebCodecs |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ca...@gmail.com |
| **Assignee** | jz...@google.com |
| **Created** | 2026-02-24 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description

Out-of-bounds heap read in VP9 encoder via WebCodecs VideoEncoder dimension reconfiguration

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/chromium/src/+/main/third_party/libvpx/source/libvpx/vp9/encoder/>

---

### The problem

#### Please describe the technical details of the vulnerability

Calling `configure()` with changing dimensions on a WebCodecs `VideoEncoder` (VP9 or AV1), followed by `encode()` without waiting for the previous encode to complete, causes memory corruption in both the VP9 and AV1 encode pipelines. The crash is stochastic and typically fires within 30 to 80 rounds of rapid dimension changes.

Tested on Windows 10 x64, reproduced on both ASAN Chrome 147.0.7696.0 and latest stable Chrome 145.0.7632.110.

The core issue is in Chrome's `OffloadingVideoEncoder`, which dispatches `Encode` and `ChangeOptions` (the internal path for JS `configure()`) onto the encoder's task queue without properly serializing them. When `configure()` arrives while codec-internal row-MT worker threads are still mid-encode, the reconfigure tears down internal state (reference frame buffers, context structures) while those threads still hold live pointers into the old allocations.

The ASAN task traces for both crashes confirm this interleaving:

```
OffloadingVideoEncoder::Encode
OffloadingVideoEncoder::WrapCallback
OffloadingVideoEncoder::ChangeOptions    <- reconfigure while encode in flight
OffloadingVideoEncoder::WrapCallback

```

When the encoder gets reconfigured to different dimensions, internal reference frame buffers from earlier configurations remain in the encoder's buffer pool while the encoder begins operating at the new dimensions. Motion estimation then computes offsets into these undersized reference buffers using the new dimensions, reading past the end of the allocation.

The row-MT worker thread (`enc_row_mt_worker_hook`) continues executing `vp9_pick_inter_mode`, which calls into SAD (sum of absolute differences) functions against a reference frame buffer that's already been freed and reallocated for the new dimensions. The SAD function reads a 64x64 block at a stride (`rdx=0x360`, 864 bytes) calibrated to the old frame width, walking off the end of the new allocation. ASAN catches this as an access-violation READ at a heap address, confirming genuine use-after-free with heap-relative addressing.

By toying with the timing and dimension configurations, we've been able to hit multiple crash sites in the VP9 path. The primary crash is in `vpx_sad64x64_avx2` (sad\_avx2.c:113), but we've also triggered `vpx_sad16x16_sse2` with smaller dimension transitions. The crash site depends on which block partition size the encoder selects for the current superblock, which varies with the dimension mismatch and content. By carefully selecting the dimensions we have some control over the length of the read (64x64, 32x32, 16x16, 8x, 4x), making it a controlled read.

The VP9 path requires `latencyMode: 'realtime'` to force threaded tile encoding (`vp9_encode_tiles_row_mt`), which widens the race window. Rapid dimension changes across superblock/MI allocation boundaries (e.g. 120x120 to 128x128, crossing mi\_cols 15 to 16) maximize the likelihood that the internal reallocation changes buffer sizes and strides. The race is reachable from any origin via the WebCodecs `VideoEncoder` API with no user interaction, permissions, or flags required. Both crashes occur in the renderer process on a thread pool worker thread (T5/T6).

**AV1 (libaom):** The same root cause also affects the AV1 encoder, which is expected given that libaom's buffer pool design and encoder architecture originate from its fork of libvpx. The AV1 variant manifests differently: `av1_encode_tiles_row_mt` calls `memset` on a buffer pointer that the reconfigure has already nulled out, resulting in a WRITE to `0x000000000000` (`rax=0` at crash). Unlike VP9 where libvpx leaves the pointer dangling, libaom's teardown zeroes it, so it surfaces as a null dereference rather than a UAF. AV1 triggers under default encoder settings without needing `latencyMode: 'realtime'`.

Reproducer: open the attached HTML, click VP9 or AV1, wait. It calls `configure()` with random dimensions (1x1 through 800x600) followed by `encode()` in a loop. On the systems I've tested this on the VP9 crash happens roughly after 30 seconds, the AV1 crash is close to instant.

#### Impact analysis

At minimum this is an controlled out-of-bounds heap read in the renderer process, triggerable from any webpage via the WebCodecs API without user interaction. On most heap layouts the read hits unmapped pages and crashes the tab. When adjacent pages happen to be committed, the read crosses into neighboring allocations, which could theoretically be an information disclosure or ASLR bypass vector, with the right heap massaging and finding an read length that ends up in between the padding of the frame and end of mapped heap pages, though we haven't been able to demonstrate that from JavaScript.

Since the underlying issue is the encoder operating in an invalid state (mismatched dimensions between active config and retained reference buffers), it's hard to fully determine the impact. The bug surfaces as an OOB read in VP9 motion estimation, but the same invalid state is present throughout the encode pipeline. We've confirmed multiple crash sites in the VP9 path (`vpx_sad64x64_avx2`, `vpx_sad16x16_sse2`) depending on timing and dimension configuration, which supports this: the stale reference buffers are reachable from various points in the encoder, and which one faults first depends on the specific encode parameters. The AV1 variant crashing as a write to a low constant address rather than a heap read further supports the idea that the consequences depend on which code path encounters the stale buffers first. Other code paths in the encoder that touch reference frames (reconstruction, loop filtering, etc.) could potentially be reached with different exploitation strategies.

---

### The cause

#### What version of Chrome have you found the security issue in?

[147.0.7696.0] + [ASAN], [145.0.7632.110] + [stable]

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

Casper Woudenberg

## Attachments

- [asan.log](attachments/asan.log) (application/octet-stream, 19.6 KB)
- [vp9_av1_oob_poc.html](attachments/vp9_av1_oob_poc.html) (text/html, 4.5 KB)
- [clean-vp9-iso.html](attachments/clean-vp9-iso.html) (text/html, 3.1 KB)
- [b487259772-clean-vp9-iso.html](attachments/b487259772-clean-vp9-iso.html) (text/html, 12.3 KB)
- [b487259772-clean-vp9-iso.html](attachments/b487259772-clean-vp9-iso_73984717.html) (text/html, 257.2 KB)

## Timeline

### li...@chromium.org (2026-02-24)

I wasn't able to repro with VP9, but AV1 did get a SIGSEGV on the tab. Tentatively set severity and other fields accordingly.

@da...@chromium.org - do you mind taking a look or reassigning as necessary?

### da...@chromium.org (2026-02-24)

Thanks for the report! The media/ encoder wrappers all operate in a single-threaded fashion, so I don't think we're doing anything wrong there, but libvpx and libaom may have some expectations on when the effects of ChangeOptions can be called.

Passing to James to let us know if there are restrictions on when ChangeOptions can be called:

- <https://source.chromium.org/chromium/chromium/src/+/main:media/video/av1_video_encoder.cc;l=632;drc=ca9257cf71443de9eadadb286ef24f5b25c1945f>
- <https://source.chromium.org/chromium/chromium/src/+/main:media/video/vpx_video_encoder.cc;l=771;drc=ca9257cf71443de9eadadb286ef24f5b25c1945f>

I suspect libvpx/libaom are missing some synchronization, but let us know James.

### jz...@google.com (2026-02-24)

If the access to the encoder context is serialized on a single thread, then this is a bug in the libraries.

### ca...@gmail.com (2026-02-24)

In case others have issues reproducing the VP9 crash, here is an alternative version of the VP9 harness that is more consistent on my machine.

### jz...@google.com (2026-02-24)

Thank you for the POCs. I can reproduce this with both codecs. The one from [comment#5](https://issues.chromium.org/issues/487259772#comment5) fails more quickly for me too.

### ch...@google.com (2026-02-25)

Setting milestone because of s2 severity.

### jz...@google.com (2026-02-25)

Note the failure in VP9 happens with threading disabled as well. I haven't been able to reproduce the issue with AV1 in single threaded mode, however. Non-row-mt for AV1 hits an assert instead, though I'm assuming there would be a crash without them enabled.

The calls are serialized and from the same thread in both media/video/ wrappers. The encode call consists of a call to `*_codec_encode()` followed by `*_codec_get_cx_data()`, which is correct use of the API.

### jz...@google.com (2026-02-26)

I modified the POC in [comment#5](https://issues.chromium.org/issues/487259772#comment5) to dump the code being run to generate a deterministic repro.

### jz...@google.com (2026-02-27)

The key issue in VP9 is due to use of scaled references. These are supported by the bitstream with some limitations on the change in scale. In this case the encoder decides it can support the feature, so it doesn't throw a key frame and clear its references. Later it is unable to produce the scaled reference due to limitations in how many reference buffers are active. The code broadly assumes that the scaling has been done, however, resulting in the out of bounds accesses.

AV1 has similar code and the same fixes may address the issues there, but I haven't extracted a repro for it yet.

I plan on landing fixes for VP9 and then creating 2 child bugs to allow backports to happen separately.

### ca...@gmail.com (2026-02-27)

Thanks for your updates!

I've done a deeper dive into the AV1 crash (null write), to see if the root causes are distinct. While debugging I found that it diverges from the VP9 logic. Specifically, media::OffloadingVideoEncoder appears to have a race in the configure/encode overlap path where the threading state becomes inconsistent. I think this issue could also have the same root cause as the null write.

I captured a TTD trace where the renderer crashes at worker_thread.cc:493 with a CHECK failure in RunWorker. The Sequence object referenced by the worker contains partially uninitialized or stale memory (0xbadbad00 fill from Application Verifier visible in several fields), suggesting the worker is operating on corrupted state after the encoder teardown/recreate cycle. The bug doesn't reproduce under ASAN due to timing sensitivity, but the TTD trace is fully replayable and shows the exact crash path.

Since this root cause for the av1 issues/in the tasking wrapper seems distinct from the libvpx scaling issue and the severity of the two differ, since this seems to corrupt a task object, should I file this as a separate VRP submission? or should I provide the details here?

### ca...@gmail.com (2026-03-02)

Quick correction on my [comment #11](https://issues.chromium.org/issues/487259772#comment11), while investigating the AV1 null write root cause I modified the PoC to include profile switching, which led me to a separate bug: a Windows x64 ABI violation where libaom and libyuv SIMD code clobbers the callee-saved xmm6 register, corrupting RunWorker's stack state. That's what causes the CHECK failure and the 0xbadbad00 patterns I mentioned.

After further analysis I'm now confident this is a distinct issue from the null write, not its root cause. I'll file the ABI violation separately.

Apologies for the noise in this thread.

### dx...@google.com (2026-03-03)

2 changes merged

---

Project: webm/libvpx  

Branch:  main  

Author:  James Zern [jzern@google.com](mailto:jzern@google.com)  

Link:    <https://chromium-review.googlesource.com/7624803>

vp9\_pick\_inter\_mode: fix buf offsets w/scaled refs

---


Expand for full commit details
```
     
    When calculating SAD for `NEWMV` with the `LAST_FRAME`, check whether a 
    scaled reference frame is available and update `xd->plane[].pre[0]` 
    offsets accordingly. This matches the behavior in 
    `combined_motion_search()`. 
     
    This fixes a heap overflow (read) when calculating the SAD when using 
    scaled references. 
     
    Bug: 487259772 
    Change-Id: I13cb02faa13d95b4f9dc4c8a49363c55d5e90efa

```

---

Files:

- M `test/acm_random.h`
- M `test/encode_api_test.cc`
- M `vp9/encoder/vp9_pickmode.c`

---

Hash: [ab5ec7a1852f634b81d29ade3c5fa74056498973](https://chromiumdash.appspot.com/commit/ab5ec7a1852f634b81d29ade3c5fa74056498973)  

Date: Mon Mar 2 22:51:36 2026


---


---

Project: webm/libvpx  

Branch:  main  

Author:  James Zern [jzern@google.com](mailto:jzern@google.com)  

Link:    <https://chromium-review.googlesource.com/7624804>

vp9\_scale\_references: fail if no free buffer is available

---


Expand for full commit details
```
     
    If `get_free_fb()` fails to return a buffer for use with scaling, fail 
    immediately. This avoids heap overflows (read) in code that assumes the 
    frame has been scaled to the current resolution 
    (`vp9_int_pro_motion_estimation()` and `combined_motion_search()`). 
     
    A test case will be added in a follow up. 
     
    This matches the behavior in libaom since: 
      4a8c004b80 Move the assertion back to get_free_fb(). 
      ... 
      Also change the scale_references() function to not ignore 
      get_free_fb() failure. 
     
    Bug: 487259772 
    Change-Id: If8028e40173b06b67cc161735af730eeb99ac57e

```

---

Files:

- M `vp9/encoder/vp9_encoder.c`
- M `vp9/encoder/vp9_mcomp.c`
- M `vp9/encoder/vp9_pickmode.c`

---

Hash: [9a2d3d1f46afbdfa9b9820a9fd3aacb084e65e2f](https://chromiumdash.appspot.com/commit/9a2d3d1f46afbdfa9b9820a9fd3aacb084e65e2f)  

Date: Mon Mar 2 23:04:57 2026


---

### jz...@google.com (2026-03-03)

> After further analysis I'm now confident this is a distinct issue from the null write, not its root cause. I'll file the ABI violation separately.

Thanks for following up. And to your earlier question, in general if you're seeing different behavior then it makes sense to file a separate issue. We can always mark it as a duplicate if we end up finding out they're the same.

### dx...@google.com (2026-03-03)

Project: chromium/src  

Branch:  main  

Author:  James Zern [jzern@chromium.org](mailto:jzern@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7629421>

Roll src/third\_party/libvpx/source/libvpx/ 4fcebeabe..9a2d3d1f4 (2 commits)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/webm/libvpx.git/+log/4fcebeabe58e..9a2d3d1f46af 
     
    $ git log 4fcebeabe..9a2d3d1f4 --date=short --no-merges --format='%ad %ae %s' 
    2026-03-02 jzern vp9_scale_references: fail if no free buffer is available 
    2026-03-02 jzern vp9_pick_inter_mode: fix buf offsets w/scaled refs 
     
    Created with: 
      roll-dep src/third_party/libvpx/source/libvpx 
     
    Bug: 487259772, 308446709 
    Change-Id: I15f4759b1dec9c73042986f1ad6cc161445cb2c3 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7629421 
    Reviewed-by: Wan-Teh Chang <wtc@google.com> 
    Commit-Queue: James Zern <jzern@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1593487}

```

---

Files:

- M `DEPS`
- M `third_party/libvpx/README.chromium`
- M `third_party/libvpx/source/config/vpx_version.h`
- M `third_party/libvpx/source/libvpx`

---

Hash: [d8fcb0f1e7991f0decb0285f4204106700becd27](https://chromiumdash.appspot.com/commit/d8fcb0f1e7991f0decb0285f4204106700becd27)  

Date: Tue Mar 3 21:31:13 2026


---

### jz...@google.com (2026-03-04)

I added a few more repros to the script in [comment #9](https://issues.chromium.org/issues/487259772#comment9) while trying to get ASan reports for use-after-free instead of heap overflow, though the UAF was due to the same root cause and may be reported as use-after-free depending on the memory layout and buffer offsets.

### dx...@google.com (2026-03-06)

Project: aom  

Branch:  main  

Author:  Wan-Teh Chang [wtc@google.com](mailto:wtc@google.com)  

Link:    <https://aomedia-review.googlesource.com/207941>

Use enc\_row\_mt->allocated\_tile\_cols/rows correctly

---


Expand for full commit details
```
     
    enc_row_mt->allocated_tile_cols and enc_row_mt->allocated_tile_rows 
    should reflect the number of elements in the cpi->tile_data array whose 
    row_mt_sync field has been allocated by row_mt_mem_alloc(). 
     
    Do not modify enc_row_mt->allocated_tile_cols and 
    enc_row_mt->allocated_tile_rows in av1_alloc_tile_data(). Instead, 
    modify them in row_mt_mem_alloc() and av1_row_mt_mem_dealloc(). 
     
    Bug: 487259772 
    Change-Id: Id2db863a6cdeac6bbb93a45f7bf87a5226eb8dde

```

---

Files:

- M `av1/encoder/encodeframe.c`
- M `av1/encoder/encoder_alloc.h`
- M `av1/encoder/ethread.c`

---

Hash: c2daa0f13c4b236576e3ef48dc625cb836653704  

Date: Fri Mar 6 02:27:52 2026


---

### ca...@gmail.com (2026-03-06)

Thanks to James and Wan-Teh for the quick fixes.

For CVE assignment and VRP tracking purposes, I want to note that while these share a common WebCodecs trigger (rapid configure/encode without flush), the underlying vulnerabilities are in different codebases with distinct root causes:

VP9 (libvpx): vp9_scale_references silently continues when get_free_fb() fails to return a buffer for scaling references to the current resolution. Subsequent motion estimation computes offsets assuming correctly scaled references, resulting in a heap-buffer-overflow read. Additionally, vp9_pick_inter_mode computed SAD buffer offsets without checking for scaled references.
AV1 (libaom): enc_row_mt->allocated_tile_cols/rows was updated in av1_alloc_tile_data() before row_mt_mem_alloc() allocated the corresponding synchronization memory. Under rapid reconfiguration, the row-MT encoding path accesses tile structures whose buffers have been deallocated but not yet reallocated, resulting in a write through a null pointer.

Since these required separate architectural fixes across two different third-party libraries, should they remain tracked under this single issue for VRP evaluation and CVE assignment, or will the AV1 fix be split into a separate tracker?

Thanks in advance!

### dx...@google.com (2026-03-06)

2 changes merged

---

Project: aom  

Branch:  main  

Author:  James Zern [jzern@google.com](mailto:jzern@google.com)  

Link:    <https://aomedia-review.googlesource.com/207981>

encode\_api\_test: add test coverage for [issue 487259772](https://issues.chromium.org/issues/487259772)

---


Expand for full commit details
```
     
    This covers a fix made in 
      c2daa0f13c Use enc_row_mt->allocated_tile_cols/rows correctly 
    that involved resolution / tile configurations related to row-mt. In 
    some situations this would cause the tile data size to fall out of sync 
    with the `row_mt_sync` allocation causing a memset on a NULL value. 
     
    Note there is still an additional crash with row-mt disabled. A test is 
    added, but disabled in this commit. 
     
    Bug: 487259772 
    Change-Id: I58cf96e729a64c3cf1ca0e93d77fb636cbc271a9

```

---

Files:

- M `test/encode_api_test.cc`

---

Hash: 2468231c631b71a34900ab388049311ae7e82219  

Date: Fri Mar 6 19:07:28 2026


---


---

Project: aom  

Branch:  main  

Author:  James Zern [jzern@google.com](mailto:jzern@google.com)  

Link:    <https://aomedia-review.googlesource.com/207901>

enc: always alloc tile data w/tile count change

---


Expand for full commit details
```
     
    Previously the code would retain an earlier allocation if the number of 
    tiles was less than or equal to the current count. This change always 
    reallocates tile data when the tile count changes. It avoids holding on 
    to extra memory unnecessarily. This is an uncommon condition, so there's 
    no need to optimize this. 
     
    Note this may be unnecessary after 
      c2daa0f13c Use enc_row_mt->allocated_tile_cols/rows correctly 
    but given the complex logic around this code, forcing the allocation may 
    be safest. 
     
    Bug: 487259772 
    Change-Id: I6acd5febcd79dce89b59869bf65386df2c993dc8

```

---

Files:

- M `av1/encoder/encodeframe.c`
- M `av1/encoder/ethread.c`
- M `av1/encoder/firstpass.c`

---

Hash: 900fa7eef8505fe0a530115c67c04d956e20f48e  

Date: Thu Mar 5 19:02:08 2026


---

### dx...@google.com (2026-03-09)

2 changes merged

---

Project: webm/libvpx  

Branch:  xenonetta  

Author:  James Zern [jzern@google.com](mailto:jzern@google.com)  

Link:    <https://chromium-review.googlesource.com/7644124>

vp9\_scale\_references: fail if no free buffer is available

---


Expand for full commit details
```
     
    If `get_free_fb()` fails to return a buffer for use with scaling, fail 
    immediately. This avoids heap overflows (read) in code that assumes the 
    frame has been scaled to the current resolution 
    (`vp9_int_pro_motion_estimation()` and `combined_motion_search()`). 
     
    A test case will be added in a follow up. 
     
    This matches the behavior in libaom since: 
      4a8c004b80 Move the assertion back to get_free_fb(). 
      ... 
      Also change the scale_references() function to not ignore 
      get_free_fb() failure. 
     
    Bug: 487259772 
    Change-Id: If8028e40173b06b67cc161735af730eeb99ac57e 
    (cherry picked from commit 9a2d3d1f46afbdfa9b9820a9fd3aacb084e65e2f)

```

---

Files:

- M `vp9/encoder/vp9_encoder.c`
- M `vp9/encoder/vp9_mcomp.c`
- M `vp9/encoder/vp9_pickmode.c`

---

Hash: [478b97817e90d7b9e87e27de05f31198555f629d](https://chromiumdash.appspot.com/commit/478b97817e90d7b9e87e27de05f31198555f629d)  

Date: Mon Mar 2 23:04:57 2026


---


---

Project: webm/libvpx  

Branch:  xenonetta  

Author:  James Zern [jzern@google.com](mailto:jzern@google.com)  

Link:    <https://chromium-review.googlesource.com/7644634>

vp9\_pick\_inter\_mode: fix buf offsets w/scaled refs

---


Expand for full commit details
```
     
    When calculating SAD for `NEWMV` with the `LAST_FRAME`, check whether a 
    scaled reference frame is available and update `xd->plane[].pre[0]` 
    offsets accordingly. This matches the behavior in 
    `combined_motion_search()`. 
     
    This fixes a heap overflow (read) when calculating the SAD when using 
    scaled references. 
     
    Bug: 487259772 
    Change-Id: I13cb02faa13d95b4f9dc4c8a49363c55d5e90efa 
    (cherry picked from commit ab5ec7a1852f634b81d29ade3c5fa74056498973)

```

---

Files:

- M `test/acm_random.h`
- M `test/encode_api_test.cc`
- M `vp9/encoder/vp9_pickmode.c`

---

Hash: [0de71c107a657f5ecd8afc6db026c7bd080ce020](https://chromiumdash.appspot.com/commit/0de71c107a657f5ecd8afc6db026c7bd080ce020)  

Date: Mon Mar 2 22:51:36 2026


---

### dx...@google.com (2026-03-09)

Project: chromium/src  

Branch:  main  

Author:  James Zern [jzern@chromium.org](mailto:jzern@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7648045>

Roll src/third\_party/libaom/source/libaom/ 98ce0d2a6..cd17f2fe0 (14 commits)

---


Expand for full commit details
```
     
    https://aomedia.googlesource.com/aom.git/+log/98ce0d2a610f..cd17f2fe0c56 
     
    $ git log 98ce0d2a6..cd17f2fe0 --date=short --no-merges --format='%ad %ae %s' 
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
     
    Bug: 307414544, 489473886, 487259772 
    Change-Id: I14d97c11b1cb5682b2ebffb9a4ebe54f1a5e5e74 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7648045 
    Commit-Queue: James Zern <jzern@google.com> 
    Reviewed-by: Wan-Teh Chang <wtc@google.com> 
    Commit-Queue: Wan-Teh Chang <wtc@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1596670}

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

Hash: [64002bc407410c0d20de0dc9257d9f287617f502](https://chromiumdash.appspot.com/commit/64002bc407410c0d20de0dc9257d9f287617f502)  

Date: Mon Mar 9 22:57:16 2026


---

### dx...@google.com (2026-03-10)

Project: chromium/src  

Branch:  main  

Author:  [luci-bisection@appspot.gserviceaccount.com](mailto:luci-bisection@appspot.gserviceaccount.com) [luci-bisection@appspot.gserviceaccount.com](mailto:luci-bisection@appspot.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7651036>

Revert "Roll src/third\_party/libaom/source/libaom/ 98ce0d2a6..cd17f2fe0 (14 commits)"

---


Expand for full commit details
```
     
    This reverts commit 64002bc407410c0d20de0dc9257d9f287617f502. 
     
    Reason for revert: 
    LUCI Bisection has identified this change as the cause of a test failure. See the analysis: https://ci.chromium.org/ui/p/chromium/bisection/test-analysis/b/5260263524663296 
     
    Sample build with failed test: https://ci.chromium.org/b/8687759307770088065 
    Affected test(s): 
    [://chrome/test\:telemetry_gpu_integration_test!flat::#gpu_tests.webcodecs_integration_test.WebCodecsIntegrationTest.WebCodecs_EncodingRateControl_av01.0.04M.08_prefer-software_variable_3000000](https://ci.chromium.org/ui/test/chromium/:%2F%2Fchrome%2Ftest%5C:telemetry_gpu_integration_test%21flat::%23gpu_tests.webcodecs_integration_test.WebCodecsIntegrationTest.WebCodecs_EncodingRateControl_av01.0.04M.08_prefer-software_variable_3000000?q=VHash%3A0e5e059025d0c9d8) 
    [://chrome/test\:telemetry_gpu_integration_test!flat::#gpu_tests.webcodecs_integration_test.WebCodecsIntegrationTest.WebCodecs_EncodingRateControl_av01.0.04M.08_prefer-software_variable_3000000](https://ci.chromium.org/ui/test/chromium/:%2F%2Fchrome%2Ftest%5C:telemetry_gpu_integration_test%21flat::%23gpu_tests.webcodecs_integration_test.WebCodecsIntegrationTest.WebCodecs_EncodingRateControl_av01.0.04M.08_prefer-software_variable_3000000?q=VHash%3A3212e6c746fb09ae) 
    [://chrome/test\:telemetry_gpu_integration_test!flat::#gpu_tests.webcodecs_integration_test.WebCodecsIntegrationTest.WebCodecs_EncodingRateControl_av01.0.04M.08_prefer-software_variable_3000000](https://ci.chromium.org/ui/test/chromium/:%2F%2Fchrome%2Ftest%5C:telemetry_gpu_integration_test%21flat::%23gpu_tests.webcodecs_integration_test.WebCodecsIntegrationTest.WebCodecs_EncodingRateControl_av01.0.04M.08_prefer-software_variable_3000000?q=VHash%3Ab73e25ffea0cd85c) 
    [://chrome/test\:telemetry_gpu_integration_test!flat::#gpu_tests.webcodecs_integration_test.WebCodecsIntegrationTest.WebCodecs_SVC_av01.0.04M.08_prefer-software_layers_2](https://ci.chromium.org/ui/test/chromium/:%2F%2Fchrome%2Ftest%5C:telemetry_gpu_integration_test%21flat::%23gpu_tests.webcodecs_integration_test.WebCodecsIntegrationTest.WebCodecs_SVC_av01.0.04M.08_prefer-software_layers_2?q=VHash%3A0e5e059025d0c9d8) 
    [://chrome/test\:telemetry_gpu_integration_test!flat::#gpu_tests.webcodecs_integration_test.WebCodecsIntegrationTest.WebCodecs_SVC_av01.0.04M.08_prefer-software_layers_2](https://ci.chromium.org/ui/test/chromium/:%2F%2Fchrome%2Ftest%5C:telemetry_gpu_integration_test%21flat::%23gpu_tests.webcodecs_integration_test.WebCodecsIntegrationTest.WebCodecs_SVC_av01.0.04M.08_prefer-software_layers_2?q=VHash%3A3212e6c746fb09ae) 
    and 4 more ... 
     
    If this is a false positive, please report it at http://b.corp.google.com/createIssue?component=1199205&description=Analysis%3A+https%3A%2F%2Fci.chromium.org%2Fui%2Fp%2Fchromium%2Fbisection%2Ftest-analysis%2Fb%2F5260263524663296&format=PLAIN&priority=P3&title=Wrongly+blamed+https%3A%2F%2Fchromium-review.googlesource.com%2Fc%2Fchromium%2Fsrc%2F%2B%2F7648045&type=BUG 
     
    Original change's description: 
    > Roll src/third_party/libaom/source/libaom/ 98ce0d2a6..cd17f2fe0 (14 commits) 
    > 
    > https://aomedia.googlesource.com/aom.git/+log/98ce0d2a610f..cd17f2fe0c56 
    > 
    > $ git log 98ce0d2a6..cd17f2fe0 --date=short --no-merges --format='%ad %ae %s' 
    > 2026-03-09 rohan.baid Fix build issue related to av1_convolve_x_sr_general_avx2() 
    > 2026-03-07 juliobbv Fix UseFixedQPOffsetsTest uninitialized value 
    > 2026-03-05 jzern Fix int16_t overflow in CDEF search for frames > 32768 pixels 
    > 2026-03-06 linzhen Fix BasicRateTargetingVBRLagRealtime after 2fed9c 
    > 2026-03-06 juliobbv Fix `use_fixed_qp_offsets` comment 
    > 2026-02-24 juliobbv Introduce `use_fixed_qp_offsets = 2` 
    > 2026-03-05 jzern enc: always alloc tile data w/tile count change 
    > 2026-03-06 jzern encode_api_test: add test coverage for issue 487259772 
    > 2026-03-05 wtc Use enc_row_mt->allocated_tile_cols/rows correctly 
    > 2026-03-06 rohan.baid Improve av1_convolve_x_sr_general_avx2() 
    > 2026-03-05 satheesh.kumar Improve av1_convolve_2d_sr_avx2() 
    > 2026-03-04 yunqingwang Optimization in apply_temporal_filter function 
    > 2026-02-02 ttwu add high bit depth compound convolve optimization 
    > 2026-02-25 linzhen Tweak the rate control for GOOD mode. 
    > 
    > Created with: 
    >   roll-dep src/third_party/libaom/source/libaom 
    > 
    > Bug: 307414544, 489473886, 487259772 
    > Change-Id: I14d97c11b1cb5682b2ebffb9a4ebe54f1a5e5e74 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7648045 
    > Commit-Queue: James Zern <jzern@google.com> 
    > Reviewed-by: Wan-Teh Chang <wtc@google.com> 
    > Commit-Queue: Wan-Teh Chang <wtc@google.com> 
    > Cr-Commit-Position: refs/heads/main@{#1596670} 
    > 
     
    Bug: 307414544, 489473886, 487259772 
    No-Presubmit: true 
    No-Tree-Checks: true 
    No-Try: true 
    Change-Id: Ifa131a6788d48590ec9f4a839412bf4ee2e2ab4e 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7651036 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Reviewed-by: Marc Treib <treib@chromium.org> 
    Commit-Queue: Marc Treib <treib@chromium.org> 
    Owners-Override: Marc Treib <treib@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1596912}

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

Hash: [fb1d237d6d5aeed4db51ff54e8b11dff6ce4a82c](https://chromiumdash.appspot.com/commit/fb1d237d6d5aeed4db51ff54e8b11dff6ce4a82c)  

Date: Tue Mar 10 08:57:29 2026


---

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

### dx...@google.com (2026-03-17)

3 changes merged

---

Project: aom  

Branch:  opaline  

Author:  James Zern [jzern@google.com](mailto:jzern@google.com)  

Link:    <https://aomedia-review.googlesource.com/208622>

encode\_api\_test: add test coverage for [issue 487259772](https://issues.chromium.org/issues/487259772)

---


Expand for full commit details
```
     
    This covers a fix made in 
      c2daa0f13c Use enc_row_mt->allocated_tile_cols/rows correctly 
    that involved resolution / tile configurations related to row-mt. In 
    some situations this would cause the tile data size to fall out of sync 
    with the `row_mt_sync` allocation causing a memset on a NULL value. 
     
    Note there is still an additional crash with row-mt disabled. A test is 
    added, but disabled in this commit. 
     
    Bug: 487259772 
    Change-Id: I58cf96e729a64c3cf1ca0e93d77fb636cbc271a9 
    (cherry picked from commit 2468231c631b71a34900ab388049311ae7e82219)

```

---

Files:

- M `test/encode_api_test.cc`

---

Hash: e53950bd064468ed30c149489c8c976feb75f4a8  

Date: Fri Mar 6 19:07:28 2026


---


---

Project: aom  

Branch:  opaline  

Author:  Wan-Teh Chang [wtc@google.com](mailto:wtc@google.com)  

Link:    <https://aomedia-review.googlesource.com/208661>

Use enc\_row\_mt->allocated\_tile\_cols/rows correctly

---


Expand for full commit details
```
     
    enc_row_mt->allocated_tile_cols and enc_row_mt->allocated_tile_rows 
    should reflect the number of elements in the cpi->tile_data array whose 
    row_mt_sync field has been allocated by row_mt_mem_alloc(). 
     
    Do not modify enc_row_mt->allocated_tile_cols and 
    enc_row_mt->allocated_tile_rows in av1_alloc_tile_data(). Instead, 
    modify them in row_mt_mem_alloc() and av1_row_mt_mem_dealloc(). 
     
    Bug: 487259772 
    Change-Id: Id2db863a6cdeac6bbb93a45f7bf87a5226eb8dde 
    (cherry picked from commit c2daa0f13c4b236576e3ef48dc625cb836653704)

```

---

Files:

- M `av1/encoder/encodeframe.c`
- M `av1/encoder/encoder_alloc.h`
- M `av1/encoder/ethread.c`

---

Hash: 61fc25e8076054e5c0176b6256f550d081d10fc0  

Date: Fri Mar 6 02:27:52 2026


---


---

Project: aom  

Branch:  opaline  

Author:  James Zern [jzern@google.com](mailto:jzern@google.com)  

Link:    <https://aomedia-review.googlesource.com/208623>

enc: always alloc tile data w/tile count change

---


Expand for full commit details
```
     
    Previously the code would retain an earlier allocation if the number of 
    tiles was less than or equal to the current count. This change always 
    reallocates tile data when the tile count changes. It avoids holding on 
    to extra memory unnecessarily. This is an uncommon condition, so there's 
    no need to optimize this. 
     
    Note this may be unnecessary after 
      c2daa0f13c Use enc_row_mt->allocated_tile_cols/rows correctly 
    but given the complex logic around this code, forcing the allocation may 
    be safest. 
     
    Bug: 487259772 
    Change-Id: I6acd5febcd79dce89b59869bf65386df2c993dc8 
    (cherry picked from commit 900fa7eef8505fe0a530115c67c04d956e20f48e)

```

---

Files:

- M `av1/encoder/encodeframe.c`
- M `av1/encoder/ethread.c`
- M `av1/encoder/firstpass.c`

---

Hash: 24ab1dd15d5bca73178e1e42dd3b93bb9caa5db3  

Date: Thu Mar 5 19:02:08 2026


---

### jz...@google.com (2026-03-18)

> Since these required separate architectural fixes across two different third-party libraries, should they remain tracked under this single issue for VRP evaluation and CVE assignment, or will the AV1 fix be split into a separate tracker?

I don't have any knowledge of the requirements for VRP. For those reviewing this bug, see [comment #18](https://issues.chromium.org/issues/487259772#comment18).

There is still an issue in libaom (see [comment #19](https://issues.chromium.org/issues/487259772#comment19)), but code reachable via Chrome is fixed. I'll close this for now.

### pe...@google.com (2026-03-18)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ch...@google.com (2026-03-18)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### jz...@google.com (2026-03-18)

Note the merge for VP9 (which was rejected) is tracked in [b/489755020](https://issues.chromium.org/issues/489755020). The issues in libaom are similar, so wouldn't qualify for a backport.

### ca...@gmail.com (2026-04-13)

Hi all,

Thanks for fixing this issue! I enjoyed being able to witness how these bugs got resolved.
I was wondering what I can expect in terms of finalization of this report, and the applicable timelines.

Thanks in advance and with kind regards,

Casper

### vi...@google.com (2026-05-12)

Labeling as `LTS-NotApplicable-144` given these bugs are related to source buffers, meant to read-only to get statistics and the security impact wouldn't justify the stability risk. (based on [#comment10](https://issues.chromium.org/issues/487259772#comment10) and [#comment11](https://issues.chromium.org/issues/487259772#comment11) from [b/489755020](https://issues.chromium.org/issues/489755020))

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/487259772)*
