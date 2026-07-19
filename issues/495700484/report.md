# Security issue update: Heap-Buffer-Overflow in ResourceKey::Builder::finish via Canvas2D Dash Pattern Size Packing Truncation

| Field | Value |
|-------|-------|
| **Issue ID** | [495700484](https://issues.chromium.org/issues/495700484) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Fuchsia, Linux, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | mi...@google.com |
| **Created** | 2026-03-24 |
| **Bounty** | $3,000.00 |

## Description

## Note

This issue is a resubmission of the previous one: <https://issues.chromium.org/issues/494644478>. There was an error in describing the affected scope, which led to unsuccessful reproduction:
This vulnerability affects desktop platforms using the Ganesh backend. Chromium on macOS defaults to Graphite.
**I have completed testing on Linux. Please reproduce using Linux Chromium.**

## Summary

A heap-buffer-overflow read occurs in the Chromium GPU process when a web page draws a Canvas2D stroked shape with a shadow and a dash pattern containing exactly 16364 intervals. The `skgpu::ResourceKey::Builder` packs the key's byte size into the upper 16 bits of a `uint32_t`, but only an `SkASSERT` guards against the size exceeding 65535 bytes. When the total key size reaches exactly 65536, the packed size truncates to zero. The subsequent call to `ResourceKeyHash` in `Builder::finish` computes a hash length of `0 - 4`, which underflows as `size_t` to an enormous value, causing the hash function to read far past the end of the allocated key buffer. This vulnerability affects desktop platforms that use the Ganesh backend., with no special GPU hardware requirements.

## Bisect

Introducing Commit: `24db3b1c35fb935660229da164fc5ad31977387f`

- Date: `2015-01-23`
- Author: `bsalomon <bsalomon@google.com>`
- Review: `https://codereview.chromium.org/858123002`

## Root Cause

The `skgpu::ResourceKey::Builder` constructor packs two fields into a single `uint32_t` metadata slot: the key's domain in the lower 16 bits and the key's total byte size in the upper 16 bits.

```
// third_party/skia/src/gpu/ResourceKey.h:80-87
Builder(ResourceKey* key, uint32_t domain, int data32Count) : fKey(key) {
    size_t count = SkToSizeT(data32Count);
    key->fKey.reset(kMetaDataCnt + count);
    size_t size = (count + kMetaDataCnt) * sizeof(uint32_t);
    SkASSERT(SkToU16(size) == size);  // release: removed
    key->fKey[kDomainAndSize_MetaDataIdx] = SkToU32(domain | (size << 16));
}

```

The expression `size << 16` is computed in `size_t` (64-bit), but the result is then truncated to `uint32_t` by `SkToU32`. When `size` equals 65536 (0x10000), the shift produces 0x100000000, which truncates to 0. The `SkASSERT` that would catch this is stripped in release builds.

Later, `internalSize()` extracts the packed size by shifting right:

```
// third_party/skia/src/gpu/ResourceKey.h:159
size_t internalSize() const { return fKey[kDomainAndSize_MetaDataIdx] >> 16; }

```

This returns 0. When `finish()` calls `ResourceKeyHash`, it passes `internalSize() - sizeof(uint32_t)` as the byte count. Since `internalSize()` is 0 and the subtraction operates on `size_t`, the result underflows to `0xFFFFFFFFFFFFFFFC` on 64-bit systems, causing the hash function (`wyhash`) to attempt reading approximately 18 exabytes of data starting from the key buffer.

```
// third_party/skia/src/gpu/ResourceKey.h:62-67
void finish() {
    if (nullptr == fKey) { return; }
    uint32_t* hash = &fKey->fKey[kHash_MetaDataIdx];
    *hash = ResourceKeyHash(hash + 1, fKey->internalSize() - sizeof(uint32_t));
    // ...
}

```

The trigger path from web content uses Canvas2D's `setLineDash()` API, which accepts an array of arbitrary length (only validating that values are finite and non-negative). When combined with `shadowBlur`, the rendering path enters `GrBlurUtils::DrawShapeWithMaskFilter`, which applies the dash path effect to the shape and then constructs a cache key. The `GrStyle::KeySize` function returns `2 + dashIntervalCnt` for the path effect portion, plus 4 for the stroke record. Combined with the geometric key (5 uint32s for a rect) and the fixed overhead in `compute_key_and_clip_bounds` (7 uint32s), the total `data32Count` passed to the Builder is `dashIntervalCnt + 18`. Adding the 2-element metadata prefix and multiplying by 4 bytes gives the total size as `(dashIntervalCnt + 20) * 4`. Setting `dashIntervalCnt = 16364` yields `16384 * 4 = 65536` bytes, the exact overflow boundary.

## Reproduce

Tested at commit `e6831951cd5fd2d7db105507e6f5e06ba600e073` on Ubuntu 22.04.

Configure an ASAN build with the following `args.gn` in `out/asan`:

```
is_asan = true
is_debug = false
dcheck_always_on = false

```

Build Chrome with `autoninja -C out/asan chrome`. No source modifications are required; the PoC is a self-contained HTML file.

Or download the newest asan-chromium:

```
wget https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-release-1604232.zip\?generation\=1774375934171278\&alt\=media

```

Launch Chrome as follows:

```
out/asan/chrome --user-data-dir=./userdata poc.html

```

The GPU process will crash within seconds with an AddressSanitizer heap-buffer-overflow report originating from `wyhash` in `SkChecksum.cpp`, called through `ResourceKey::Builder::finish` in `ResourceKey.h`. The crash occurs because a 65536-byte ResourceKey buffer is read past its end when the `size_t` length argument underflows to a massive value. The ASAN summary line reads `heap-buffer-overflow ... in wyhash(void const*, unsigned long, unsigned long, unsigned long const*)` and the access is located 3 bytes after a 65536-byte heap region.

ASAN output:

```
=================================================================
==191842==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7a9b28cf4803 at pc 0x5e7ce9ad9692 bp 0x7ffd713380b0 sp 0x7ffd713380a8
READ of size 8 at 0x7a9b28cf4803 thread T0 (chrome)
    #0 0x5e7ce9ad9691 in wyhash(void const*, unsigned long, unsigned long, unsigned long const*) third_party/skia/src/core/SkChecksum.cpp:45:5
    #1 0x5e7d02ee0448 in skgpu::ganesh::SoftwarePathRenderer::onDrawPath(skgpu::ganesh::PathRenderer::DrawPathArgs const&) third_party/skia/src/gpu/ResourceKey.h:67:21
    #2 0x5e7d02cf7ad2 in skgpu::ganesh::SurfaceDrawContext::drawShapeUsingPathRenderer(GrClip const*, GrPaint&&, GrAA, SkMatrix const&, GrStyledShape&&, bool) third_party/skia/src/gpu/ganesh/SurfaceDrawContext.cpp:1897:9
    #3 0x5e7d02d005c7 in skgpu::ganesh::SurfaceDrawContext::drawShape(GrClip const*, GrPaint&&, GrAA, SkMatrix const&, GrStyledShape&&) third_party/skia/src/gpu/ganesh/SurfaceDrawContext.cpp:1561:11
    #4 0x5e7d02c003ec in GrBlurUtils::draw_shape_with_mask_filter(GrRecordingContext*, skgpu::ganesh::SurfaceDrawContext*, GrClip const*, GrPaint&&, SkMatrix const&, SkMaskFilterBase const*, GrStyledShape const&) third_party/skia/src/gpu/ganesh/GrBlurUtils.cpp:303:10
......

```

The complete ASAN log is attached as `asan.txt`.

## References

- [ResourceKey::Builder constructor (size packing)](https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/gpu/ResourceKey.h;l=80-88)
- [ResourceKey::Builder::finish (underflow site)](https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/gpu/ResourceKey.h;l=62-70)
- [ResourceKey::internalSize (reads packed zero)](https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/gpu/ResourceKey.h;l=159)
- [GrBlurUtils::compute\_key\_and\_clip\_bounds (UniqueKey::Builder creation)](https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/gpu/ganesh/GrBlurUtils.cpp;l=1195)
- [GrStyle::KeySize (dash interval count in key)](https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/gpu/ganesh/GrStyle.cpp;l=19-38)

## Credit

Please use 86ac1f1587b71893ed2ad792cd7dde32 as the credit for this vulnerability. Thank you.

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 16.6 KB)
- [poc.html](attachments/poc.html) (text/html, 1.7 KB)

## Timeline

### el...@google.com (2026-03-24)

Security shepherd: thanks. I don't have a physical Linux machine that uses the Ganesh backend handy, so I'm going to route this to the GPU team for further triage.

### el...@google.com (2026-03-24)

Speculative: OS = Linux, FoundIn = 144 based on the report, Sev-1 based on renderer heap overflow. If this is actually a GPU process heap overflow please upgrade to Sev-0 :)

### mi...@google.com (2026-03-24)

`asan.txt` is showing it crashing on the main thread in the GPU process

### mi...@google.com (2026-03-24)

I am able to reproduce on my local linux machine.

### ch...@google.com (2026-03-25)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-25)

Setting Priority to P0 to match Severity s0. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-04-02)

Project: skia  

Branch:  main  

Author:  Michael Ludwig [michaelludwig@google.com](mailto:michaelludwig@google.com)  

Link:    <https://skia-review.googlesource.com/1199497>

Use 16-bit size for ResourceKeys

---


Expand for full commit details
```
     
    Internally, ResourceKey required the size to fit into a uint16_t so this 
    makes that explicit in the public API. It also changes how the size is 
    stored to instead record the num32DataCount directly and then convert to 
    bytes as needed, whereas previously it was requiring that the actual 
    byte count fit into a uint16_t. This gives a bit more head room. 
     
    Call sites to the ResourceKey builders are updated to now have the 
    responsibility of checking that their size can fit into a uint16_t. For 
    the most part, these were fixed or trivially small variable key sizes. 
    The two exceptions were Ganesh's style key (with dashes) and its 
    inherited key system for shapes with applied styles and path effects. 
    They now have reasonable limits to prevent the keys from growing bigger 
    than about 1kb. 
     
    Bug: b/495700484 
    Change-Id: I6ac4f17628b9a2e1a777c473b74e6d1f5c68b27d 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1199497 
    Reviewed-by: Robert Phillips <robertphillips@google.com> 
    Commit-Queue: Michael Ludwig <michaelludwig@google.com>

```

---

Files:

- M `src/gpu/ResourceKey.h`
- M `src/gpu/ganesh/GrStyle.cpp`
- M `src/gpu/ganesh/GrStyle.h`
- M `src/gpu/ganesh/geometry/GrStyledShape.cpp`
- M `src/gpu/ganesh/geometry/GrStyledShape.h`
- M `src/gpu/ganesh/image/GrImageUtils.cpp`
- M `src/gpu/ganesh/ops/TriangulatingPathRenderer.cpp`
- M `src/gpu/graphite/GraphiteResourceKey.h`
- M `src/gpu/graphite/RasterPathUtils.cpp`
- M `src/gpu/graphite/ResourceProvider.cpp`
- M `src/gpu/graphite/dawn/DawnCaps.cpp`
- M `src/gpu/graphite/geom/AnalyticBlurMask.cpp`
- M `src/gpu/graphite/geom/Shape.cpp`
- M `src/gpu/graphite/geom/Shape.h`
- M `src/gpu/graphite/mtl/MtlCaps.mm`
- M `src/gpu/graphite/vk/VulkanCaps.cpp`
- M `src/gpu/graphite/vk/VulkanResourceProvider.cpp`
- M `src/utils/SkShadowUtils.cpp`

---

Hash: 0566b2f5f0d1f218d9990eba838af16826d2e7e3  

Date: Wed Apr 1 13:48:48 2026


---

### ch...@google.com (2026-04-09)

This is sufficiently serious that it should be merged to M146. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M146. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

This is sufficiently serious that it should be merged to M147. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M147. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to M148. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M148. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

### ch...@google.com (2026-04-09)

**M146** merge request created. **Please update [crbug/500956394](https://crbug.com/500956394) to have this merge reviewed.**

### ch...@google.com (2026-04-09)

**M147** merge request created. **Please update [crbug/500956429](https://crbug.com/500956429) to have this merge reviewed.**

### ch...@google.com (2026-04-09)

**M148** merge request created. **Please update [crbug/500956377](https://crbug.com/500956377) to have this merge reviewed.**

### mi...@google.com (2026-04-09)

This is already in the M148 beta branch, I'm guessing it's not seeing it since it's a Skia repo change. Only M147 and M146 merges need to be created. I have closed [crbug/500956377](https://crbug.com/500956377), should I add Merged-148 anyways (it technically wasn't, it made the cutoff normally).

### dx...@google.com (2026-04-11)

Project: skia  

Branch:  chrome/m146  

Author:  Michael Ludwig [michaelludwig@google.com](mailto:michaelludwig@google.com)  

Link:    <https://skia-review.googlesource.com/1206356>

Use 16-bit size for ResourceKeys

---


Expand for full commit details
```
     
    Internally, ResourceKey required the size to fit into a uint16_t so this 
    makes that explicit in the public API. It also changes how the size is 
    stored to instead record the num32DataCount directly and then convert to 
    bytes as needed, whereas previously it was requiring that the actual 
    byte count fit into a uint16_t. This gives a bit more head room. 
     
    Call sites to the ResourceKey builders are updated to now have the 
    responsibility of checking that their size can fit into a uint16_t. For 
    the most part, these were fixed or trivially small variable key sizes. 
    The two exceptions were Ganesh's style key (with dashes) and its 
    inherited key system for shapes with applied styles and path effects. 
    They now have reasonable limits to prevent the keys from growing bigger 
    than about 1kb. 
     
    Bug: b/495700484 
    Change-Id: I6ac4f17628b9a2e1a777c473b74e6d1f5c68b27d 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1199497 
    Reviewed-by: Robert Phillips <robertphillips@google.com> 
    Commit-Queue: Michael Ludwig <michaelludwig@google.com> 
    (cherry picked from commit 0566b2f5f0d1f218d9990eba838af16826d2e7e3) 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1206356 
    Commit-Queue: Thomas Smith <thomsmit@google.com> 
    Reviewed-by: Thomas Smith <thomsmit@google.com> 
    Auto-Submit: Michael Ludwig <michaelludwig@google.com>

```

---

Files:

- M `src/gpu/ResourceKey.h`
- M `src/gpu/ganesh/GrStyle.cpp`
- M `src/gpu/ganesh/GrStyle.h`
- M `src/gpu/ganesh/geometry/GrStyledShape.cpp`
- M `src/gpu/ganesh/geometry/GrStyledShape.h`
- M `src/gpu/ganesh/image/GrImageUtils.cpp`
- M `src/gpu/ganesh/ops/TriangulatingPathRenderer.cpp`
- M `src/gpu/graphite/GraphiteResourceKey.h`
- M `src/gpu/graphite/RasterPathUtils.cpp`
- M `src/gpu/graphite/ResourceProvider.cpp`
- M `src/gpu/graphite/dawn/DawnCaps.cpp`
- M `src/gpu/graphite/geom/AnalyticBlurMask.cpp`
- M `src/gpu/graphite/geom/Shape.cpp`
- M `src/gpu/graphite/geom/Shape.h`
- M `src/gpu/graphite/mtl/MtlCaps.mm`
- M `src/gpu/graphite/vk/VulkanCaps.cpp`
- M `src/gpu/graphite/vk/VulkanResourceProvider.cpp`
- M `src/utils/SkShadowUtils.cpp`

---

Hash: bc591f8db342ee912fbb92aadde2a088e0ab8470  

Date: Wed Apr 1 13:48:48 2026


---

### dx...@google.com (2026-04-11)

Project: skia  

Branch:  chrome/m147  

Author:  Michael Ludwig [michaelludwig@google.com](mailto:michaelludwig@google.com)  

Link:    <https://skia-review.googlesource.com/1206376>

Use 16-bit size for ResourceKeys

---


Expand for full commit details
```
     
    Internally, ResourceKey required the size to fit into a uint16_t so this 
    makes that explicit in the public API. It also changes how the size is 
    stored to instead record the num32DataCount directly and then convert to 
    bytes as needed, whereas previously it was requiring that the actual 
    byte count fit into a uint16_t. This gives a bit more head room. 
     
    Call sites to the ResourceKey builders are updated to now have the 
    responsibility of checking that their size can fit into a uint16_t. For 
    the most part, these were fixed or trivially small variable key sizes. 
    The two exceptions were Ganesh's style key (with dashes) and its 
    inherited key system for shapes with applied styles and path effects. 
    They now have reasonable limits to prevent the keys from growing bigger 
    than about 1kb. 
     
    Bug: b/495700484 
    Change-Id: I6ac4f17628b9a2e1a777c473b74e6d1f5c68b27d 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1199497 
    Reviewed-by: Robert Phillips <robertphillips@google.com> 
    Commit-Queue: Michael Ludwig <michaelludwig@google.com> 
    (cherry picked from commit 0566b2f5f0d1f218d9990eba838af16826d2e7e3) 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1206376 
    Commit-Queue: Thomas Smith <thomsmit@google.com> 
    Auto-Submit: Michael Ludwig <michaelludwig@google.com> 
    Reviewed-by: Thomas Smith <thomsmit@google.com>

```

---

Files:

- M `src/gpu/ResourceKey.h`
- M `src/gpu/ganesh/GrStyle.cpp`
- M `src/gpu/ganesh/GrStyle.h`
- M `src/gpu/ganesh/geometry/GrStyledShape.cpp`
- M `src/gpu/ganesh/geometry/GrStyledShape.h`
- M `src/gpu/ganesh/image/GrImageUtils.cpp`
- M `src/gpu/ganesh/ops/TriangulatingPathRenderer.cpp`
- M `src/gpu/graphite/GraphiteResourceKey.h`
- M `src/gpu/graphite/RasterPathUtils.cpp`
- M `src/gpu/graphite/ResourceProvider.cpp`
- M `src/gpu/graphite/dawn/DawnCaps.cpp`
- M `src/gpu/graphite/geom/AnalyticBlurMask.cpp`
- M `src/gpu/graphite/geom/Shape.cpp`
- M `src/gpu/graphite/geom/Shape.h`
- M `src/gpu/graphite/mtl/MtlCaps.mm`
- M `src/gpu/graphite/vk/VulkanCaps.cpp`
- M `src/gpu/graphite/vk/VulkanResourceProvider.cpp`
- M `src/utils/SkShadowUtils.cpp`

---

Hash: d203629ce869dbb142ca186c7da60a97cfb1550d  

Date: Wed Apr 1 13:48:48 2026


---

### pe...@google.com (2026-04-11)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### aj...@google.com (2026-04-21)

Sev Medium as this just reads OOB into the hash function with no evidence of a follow on write

### pe...@google.com (2026-04-21)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-04-21)

1. https://skia-review.git.corp.google.com/c/skia/+/1215386
2. Low - There was no conflict.
3. 146 and 147
4. Yes, the bug was old, M144 has the bug as well.

### dx...@google.com (2026-04-21)

Project: skia  

Branch:  chrome/m144  

Author:  Michael Ludwig [michaelludwig@google.com](mailto:michaelludwig@google.com)  

Link:    <https://skia-review.googlesource.com/1215386>

[M144-LTS] Use 16-bit size for ResourceKeys

---


Expand for full commit details
```
     
    Internally, ResourceKey required the size to fit into a uint16_t so this 
    makes that explicit in the public API. It also changes how the size is 
    stored to instead record the num32DataCount directly and then convert to 
    bytes as needed, whereas previously it was requiring that the actual 
    byte count fit into a uint16_t. This gives a bit more head room. 
     
    Call sites to the ResourceKey builders are updated to now have the 
    responsibility of checking that their size can fit into a uint16_t. For 
    the most part, these were fixed or trivially small variable key sizes. 
    The two exceptions were Ganesh's style key (with dashes) and its 
    inherited key system for shapes with applied styles and path effects. 
    They now have reasonable limits to prevent the keys from growing bigger 
    than about 1kb. 
     
    Bug: b/495700484 
    Change-Id: I6ac4f17628b9a2e1a777c473b74e6d1f5c68b27d 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1199497 
    Reviewed-by: Robert Phillips <robertphillips@google.com> 
    Commit-Queue: Michael Ludwig <michaelludwig@google.com> 
    (cherry picked from commit 0566b2f5f0d1f218d9990eba838af16826d2e7e3) 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1206356 
    Commit-Queue: Thomas Smith <thomsmit@google.com> 
    Reviewed-by: Thomas Smith <thomsmit@google.com> 
    Auto-Submit: Michael Ludwig <michaelludwig@google.com> 
    (cherry picked from commit bc591f8db342ee912fbb92aadde2a088e0ab8470) 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1215386 
    Reviewed-by: Michael Ludwig <michaelludwig@google.com>

```

---

Files:

- M `src/gpu/ResourceKey.h`
- M `src/gpu/ganesh/GrStyle.cpp`
- M `src/gpu/ganesh/GrStyle.h`
- M `src/gpu/ganesh/geometry/GrStyledShape.cpp`
- M `src/gpu/ganesh/geometry/GrStyledShape.h`
- M `src/gpu/ganesh/image/GrImageUtils.cpp`
- M `src/gpu/ganesh/ops/TriangulatingPathRenderer.cpp`
- M `src/gpu/graphite/GraphiteResourceKey.h`
- M `src/gpu/graphite/RasterPathUtils.cpp`
- M `src/gpu/graphite/ResourceProvider.cpp`
- M `src/gpu/graphite/dawn/DawnCaps.cpp`
- M `src/gpu/graphite/geom/AnalyticBlurMask.cpp`
- M `src/gpu/graphite/geom/Shape.cpp`
- M `src/gpu/graphite/geom/Shape.h`
- M `src/gpu/graphite/mtl/MtlCaps.mm`
- M `src/gpu/graphite/vk/VulkanCaps.cpp`
- M `src/gpu/graphite/vk/VulkanResourceProvider.cpp`
- M `src/utils/SkShadowUtils.cpp`

---

Hash: 3dde9e726a05abcd66e0ccafc4397b7b045213bd  

Date: Wed Apr 1 13:48:48 2026


---

### sp...@google.com (2026-04-22)

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

### ch...@google.com (2026-07-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/495700484)*
