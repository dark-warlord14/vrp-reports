# Buffer overflow in vp9_get_token_cost via crafted VideoEncoder frame sequence

| Field | Value |
|-------|-------|
| **Issue ID** | [502107756](https://issues.chromium.org/issues/502107756) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Media>Video |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | sh...@gmail.com |
| **Assignee** | ma...@google.com |
| **Created** | 2026-04-13 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description

Signed integer overflow in VP9 encoder block\_rd\_txfm (libvpx)

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/webm/libvpx/+/e1dd14963a005523d0eb3a72954921934b3a8be7/vp9/encoder/vp9_rdopt.c#765>

---

### The problem

#### Please describe the technical details of the vulnerability

## Summary

Signed integer overflow in the VP9 encoder function `block_rd_txfm` at `vp9/encoder/vp9_rdopt.c:765`. The expression `sse = sse * 16` overflows `int64_t` when encoding 10-bit highbitdepth content in lossless mode. This is undefined behavior per the C standard and is compiler-weaponizable — the compiler may delete downstream safety checks that depend on `sse` being non-negative.

The vulnerable function `block_rd_txfm` is compiled into Chrome (confirmed via `nm` on the ASAN build: symbol at offsets `0x2d2c09e0` and `0x2d7d29c0`). Chrome builds libvpx with `CONFIG_VP9_HIGHBITDEPTH` enabled. The VP9 software encoder is used by the WebCodecs `VideoEncoder` API.

The overflow is unfixed on the latest upstream libvpx main branch (verified at `b1f431c1e`, fetched 2026-04-13). Chrome's libvpx pin (`e1dd14963`, 2026-03-08) contains the vulnerable code.

## Version

- **Chrome Version:** 148.0.7743.0
- **Operating System:** Linux x86\_64 (all platforms with VP9 highbitdepth encoding are affected)
- **Third-party component:** libvpx, pinned at commit `e1dd14963a005523d0eb3a72954921934b3a8be7`

## Vulnerable code

<https://chromium.googlesource.com/webm/libvpx/+/e1dd14963a005523d0eb3a72954921934b3a8be7/vp9/encoder/vp9_rdopt.c#765>

```
// vp9/encoder/vp9_rdopt.c, function block_rd_txfm(), line 765:
#if CONFIG_VP9_HIGHBITDEPTH
      if ((xd->cur_buf->flags & YV12_FLAG_HIGHBITDEPTH) && (xd->bd > 8))
        sse = ROUND64_POWER_OF_TWO(sse, (xd->bd - 8) * 2);
#endif
      sse = sse * 16;  // overflow: sse is int64_t, product exceeds INT64_MAX

```

When encoding a 10-bit 4:4:4 lossless VP9 frame (profile 3), the SSE value for certain blocks is extremely large. The preceding `ROUND64_POWER_OF_TWO` partially reduces the value, but for specific pixel patterns the result of `sse * 16` still exceeds `INT64_MAX`.

## Reproduction

Place `poc.html` and `poc.yuv` in the same directory. Open in a Chromium UBSAN build:

```
chrome --no-sandbox --disable-gpu-sandbox --allow-file-access-from-files file:///path/to/poc.html

```

The console will show:

```
loaded poc.yuv: 21456 samples
frame: 150x48 I420P10
output: 21861B type=key
done

```

The PoC loads `poc.yuv` (the 10-bit trigger frame), converts it to I420P10, creates a `VideoFrame`, and encodes it with VP9 profile 2 (10-bit) via WebCodecs `VideoEncoder`. The encoding succeeds and reaches `block_rd_txfm` where the overflow occurs.

Confirmed in Chromium 134.0.6991.0 UBSAN build (`chromium-browser-ubsan/linux-release/ubsan-linux-release-1413905`). Chrome UBSAN trace attached as `chrome_ubsan_trace.txt`:

```
../../third_party/libvpx/source/libvpx/vp9/encoder/vp9_rdopt.c:765:17: runtime error:
  signed integer overflow: 1152921504568624343 * 16 cannot be represented in type 'int64_t'
SUMMARY: UndefinedBehaviorSanitizer: undefined-behavior vp9_rdopt.c:765:17

```

The overflow cascades to a left-shift of negative value at line 830:

```
../../third_party/libvpx/source/libvpx/vp9/encoder/vp9_rdopt.c:830:9: runtime error:
  left shift of negative value -611562128

```

Standalone UBSAN trace also attached as `ubsan_trace.txt`.

## Crash state

```
vp9/encoder/vp9_rdopt.c:765:17: runtime error: signed integer overflow:
  1152921504526836527 * 16 cannot be represented in type 'long int'
    #0 block_rd_txfm vp9/encoder/vp9_rdopt.c:765
    #1 vp9_foreach_transformed_block_in_plane vp9/common/vp9_blockd.c:70
    #2 txfm_rd_in_plane vp9/encoder/vp9_rdopt.c:876
    #3 choose_largest_tx_size / super_block_yrd vp9/encoder/vp9_rdopt.c:903
    #4 rd_pick_intra_sby_mode vp9/encoder/vp9_rdopt.c:1393
    #5 nonrd_pick_sb_modes vp9/encoder/vp9_encodeframe.c:4422
    ...
    #13 vp9_encode_frame vp9/encoder/vp9_encodeframe.c:5953
    #14 vpx_codec_encode vpx/src/vpx_encoder.c:218

```

Full symbolized trace attached as `ubsan_trace.txt`.

## Bisect

Introduced in commit [`e357b9efe`](https://chromium.googlesource.com/webm/libvpx/+/e357b9efe08eca4c878e2a43dcde4bd4f7fb39a7) ("Support measure distortion in the pixel domain", 2016-07-01) which added the `sse = sse * 16` multiplication in the highbitdepth path of `block_rd_txfm` without an overflow guard.

## Suggested patch

Gerrit CL: <https://chromium-review.googlesource.com/c/webm/libvpx/+/7754639>

Also attached as `fix.patch`. The fix clamps `sse` before multiplying by 16, ensuring the result remains representable and also safe for the downstream `RDCOST` macro which left-shifts `sse` by `RDDIV_BITS` (7).

```
-      sse = sse * 16;
+      sse = (sse > (INT64_MAX >> (RDDIV_BITS + 4))) ? (INT64_MAX >> RDDIV_BITS) : sse * 16;

```

Validated: with the patch applied, UBSAN no longer reports the `sse * 16` overflow for the attached `poc.yuv` input.

Note: the same `poc.yuv` input also triggers a separate OOB read at `vp9/encoder/vp9_tokenize.h:120` (cat6\_high\_cost table index overflow). That is a distinct issue with a different root cause and requires a separate fix.

#### Impact analysis

An attacker who lures a victim to a web page can trigger this overflow via the WebCodecs `VideoEncoder` JavaScript API by requesting VP9 10-bit encoding with crafted frame content. No user interaction beyond visiting the page is required. The overflow produces undefined behavior in the renderer process — the wrapped `sse` value corrupts downstream rate-distortion decisions and may cause further out-of-bounds accesses in the encoder's cost tables. Exploitation for controlled write or RCE has not been demonstrated.

---

### The cause

#### What version of Chrome have you found the security issue in?

Chromium 134.0.6991.0 and Chrome 148.0.7743.0

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

Matej Smycka

## Attachments

- [chrome_ubsan_trace.txt](attachments/chrome_ubsan_trace.txt) (text/plain, 3.6 KB)
- [harness.c](attachments/harness.c) (text/x-csrc, 2.8 KB)
- [poc.html](attachments/poc.html) (text/html, 1.8 KB)
- [poc.yuv](attachments/poc.yuv) (video/x-raw-yuv, 41.9 KB)

## Timeline

### ch...@google.com (2026-04-14)

Setting Priority to P3 to match Severity s3. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### ma...@gmail.com (2026-04-14)

I found there is already working fix in the upstream.

This was addressed by input validation in 090dd8b8c (<https://chromium.googlesource.com/webm/libvpx/+/090dd8b8c>) which rejects values >= (1 << bit\_depth) in vpx\_codec\_encode before the encoder runs.

That prevents both the OOB read in vp9\_cat6\_high10\_high\_cost[] ([b/488585490](https://issues.chromium.org/issues/488585490)) and the sse\*16 overflow I reported at vp9\_rdopt.c:765 - neither is reachable once the input is validated. Chrome main rolled this on 2026-03-27 (<https://chromium.googlesource.com/chromium/src/+/51ae1a177418>).

Current stable is vulnerable right now.

### jz...@chromium.org (2026-04-14)

Thank you for the update. This was not backported, so will be fixed in an upcoming stable release.

### ma...@gmail.com (2026-04-14)

Are these types of reports eligible for a reward, or not, because you would fix them anyway?

### jz...@chromium.org (2026-04-14)

As bug reports, they're definitely useful, especially if we're not catching them through other means like existing fuzzers. The [VRP rules](https://bughunters.google.com/about/rules/chrome-friends/chrome-vulnerability-reward-program-rules) give a better idea of what is eligible for a reward than I could try to summarize.

### ct...@chromium.org (2026-05-14)

Marking as a dupe of 488585490 per the discussion above. That bug was already Sev-Medium and was not considered for merge back to Stable.

### ch...@google.com (2026-07-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/502107756)*
