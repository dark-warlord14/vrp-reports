# ANGLE WebGL2: Missing Per-Layer Init Tracking in TEXTURE_2D_ARRAY Leaves Layers Uninitialized, Leads to Cross-Origin GPU Texture Data Leak

| Field | Value |
|-------|-------|
| **Issue ID** | [492131521](https://issues.chromium.org/issues/492131521) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Linux, Windows, ChromeOS |
| **Reporter** | sw...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2026-03-12 |
| **Bounty** | $3,000.00 |

## Description

---

### Report description

ANGLE WebGL2: Missing Per-Layer Init Tracking in TEXTURE\_2D\_ARRAY Leaves Layers Uninitialized, Leads to Cross-Origin GPU Texture Data Leak

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

## Summary

ANGLE's robust resource initialization tracks `TEXTURE_2D_ARRAY` init state per **mip-level** (mipmap level = resolution step: level 0 is full-size, level 1 is half, etc.), but **not per layer** (layer = individual 2D slice within an array texture). A `TEXTURE_2D_ARRAY` with 4 layers at mip 0 has only **one** `initState` shared across all 4 layers. Clearing one layer via `framebufferTextureLayer` + `gl.clear` marks the **entire mip level** (all layers) as initialized — but only that single layer actually receives a GPU write. Sibling layers remain filled with stale GPU memory from previously freed textures. `readPixels` on those uninitialized layers bypasses all init checks and returns the stale data directly to JavaScript.

## Tested on

- AWS G4DN instance (Nvidia T4)
- Ubuntu 24.04.4 server + XRDP
- Chromium asan build (vulkan backend)
- For reliable reproduction, I recommend testing under the same or similar environment (NVIDIA GPU + Linux + Vulkan backend). See the Notes section for details on hardware-dependent behavior.

## Root Cause

The frontend tracks `TEXTURE_2D_ARRAY` init state per mip-level (mipmap resolution step) but **missing per-layer tracking** (individual 2D slice within the array). Note that cube maps already have per-face tracking (`level * 6 + faceIndex`), but array textures do not — `GetImageDescIndex` returns only `level`, collapsing all layers into one `ImageDesc.initState`. This is a frontend logic bug — all backends (Vulkan, D3D11, Metal) are equally affected because they trust the frontend's `initState` verdict.

```
// src/libANGLE/Texture.cpp:43-47
size_t GetImageDescIndex(TextureTarget target, size_t level)
{
    return IsCubeMapFaceTarget(target) ? (level * 6 + CubeMapTextureTargetToFaceIndex(target))
                                       : level;  // ← BUG: cube maps get per-face tracking,
                                                  //    but 2D_ARRAY layers all share one ImageDesc per mip
}

```

All layers of a mip map to a single `ImageDesc.initState`. When a single layer is cleared:

```
// src/libANGLE/Framebuffer.cpp:2498-2508
if (partialClearNeedsInit(context, color, depth, stencil))
{
    ANGLE_TRY(ensureDrawAttachmentsInitialized(context));  // ← SKIPPED for full-viewport clear
}
markAttachmentsInitialized(clearedColorAttachments, depth, stencil);  // ← marks entire mip Initialized

```

`partialClearNeedsInit` returns `false` for a full-viewport, unmasked clear. The code skips `ensureDrawAttachmentsInitialized` (which would zero ALL layers) and jumps to `markAttachmentsInitialized`, setting `initState = Initialized` for the whole mip — even though only one layer received a GPU write.

After this, `ensureReadAttachmentsInitialized` (the readPixels init gate) sees `mResourceNeedsInit` is empty and skips initialization:

```
// src/libANGLE/Framebuffer.cpp:2623-2630
angle::Result Framebuffer::ensureReadAttachmentsInitialized(const Context *context)
{
    ASSERT(context->isRobustResourceInitEnabled());

    if (mState.mResourceNeedsInit.none())   // ← false because initState was set to Initialized
    {
        return angle::Result::Continue;     // ← init SKIPPED, stale GPU memory returned
    }

```

Introduced in commit `05b35b210e` (2017-10-03, "D3D11: Lazy robust resource init") which added `ImageDesc.initState`, `partialClearNeedsInit`, `markAttachmentsInitialized`, and `ensureReadAttachmentsInitialized` all at once — with per-mip-only granularity from the start.

### Execution Flow

```
texStorage3D(2D_ARRAY, 4 layers)        ImageDesc[mip0].initState = MayNeedInit
                                        (all 4 layers share this single ImageDesc)

framebufferTextureLayer(FBO_A, layer=0) FBO_A targets layer 0 only
                                        mResourceNeedsInit.set(0, true)  (MayNeedInit)

gl.clear(COLOR_BUFFER_BIT) on FBO_A     partialClearNeedsInit() = false  (full-viewport, no mask)
                                        ensureDrawAttachmentsInitialized SKIPPED
                                        GPU writes ONLY layer 0
                                        markAttachmentsInitialized:
                                          setInitState(Initialized) on attachment
                                          -> Texture::setInitState -> getImageDesc(target, level)
                                          -> GetImageDescIndex returns level=0
                                          -> ImageDesc[mip0].initState = Initialized  <-- BUG
                                          (layers 1-3 still contain stale GPU memory)

framebufferTextureLayer(FBO_B, layer=2) FBO_B attach: attachment->initState() called
                                        -> Texture::initState(imageIndex) -> getImageDesc(level=0)
                                        -> returns Initialized (false: layer 2 was never written)
                                        -> mResourceNeedsInit.set(0, false)

gl.readPixels() on FBO_B               ensureReadAttachmentsInitialized:
                                          mResourceNeedsInit.none() == true -> skip init
                                        backend reads layer 2 stale GPU memory -> INFO LEAK

```
## Notes

- **ASAN cannot detect this vulnerability.** The stale data resides in GPU device memory (VRAM), which is outside ASAN's instrumentation scope. All CPU-side operations (staging buffer allocation, `memcpy` to JavaScript `ArrayBuffer`) are correctly sized and within bounds. The bug produces wrong *data content* (stale instead of zero), not an out-of-bounds memory access — so no ASAN signal is expected.
- **Reproduction depends on GPU hardware and driver.** The leaked data comes from VRAM blocks that are freed and reallocated by the GPU driver's memory allocator (e.g. Vulkan VMA). Whether stale data persists depends on the driver's allocation behavior:
  - NVIDIA Vulkan: does **not** zero-fill VRAM on allocation → 100% reproducible
  - Apple Metal: zero-fills on allocation → not reproducible despite identical frontend bug
  - AMD/Intel Vulkan: behavior may vary by driver version
  - VRAM reuse also depends on texture size alignment and allocator fragmentation — same-sized textures maximize reuse probability.

## Suggested Fix

1. **Quick fix**: In `partialClearNeedsInit` (`Framebuffer.cpp`), treat a single-layer clear on a multi-layer texture (`TEXTURE_2D_ARRAY`, `TEXTURE_2D_MULTISAMPLE_ARRAY`, `TEXTURE_CUBE_MAP_ARRAY`) as a partial clear when the mip's `initState` is `MayNeedInit`. This forces `ensureDrawAttachmentsInitialized` to zero all sibling layers before `markAttachmentsInitialized` marks the entire mip as initialized.
2. **Thorough fix**: Extend `GetImageDescIndex` (`Texture.cpp`) to track init state per-layer for array texture types, similar to how cube maps already track per-face via `level * 6 + faceIndex`. This requires resizing `mImageDescs` to account for the layer count, which is a larger refactor.

## Reproduction Steps

### Minimal Reproduction (poc.html)

```
# Linux with Vulkan GPU (tested on T4 / Ubuntu)
./chrome --headless=new --no-sandbox --disable-gpu-sandbox \
  --use-gl=angle --use-angle=vulkan --ignore-gpu-blocklist \
  poc.html --dump-dom

```

1. Create `TEXTURE_2D_ARRAY` texture `A` (2x1, 4 layers), clear layers 1-2 with magenta `[255,0,255,255]`
2. Delete texture `A`
3. Create `TEXTURE_2D_ARRAY` texture `B` (same dimensions)
4. Clear only layer 1 of `B` with green
5. `readPixels` on layer 2 of `B`

```
**Check 'poc_html_result.png'**
Expected:  [0,0,0,0, 0,0,0,0]  (uninitialized → zeroed by robust init)
Actual:    [255,0,255,255, 255,0,255,255]  (stale magenta from deleted texture A)

```
### 10-Round Spray-and-Leak (poc\_v2\_enhanced.html)

```
./chrome --headless=new --no-sandbox --disable-gpu-sandbox \
  --use-gl=angle --use-angle=vulkan --ignore-gpu-blocklist \
  poc_v2_enhanced.html --dump-dom

```
```
Check 'poc_v2_enhanced_html_result.png'
# Output (10 rounds, 256x256x4 RGBA8):
# Round 1 seed=#deadbeef | status=LEAK | stale=100.0% (65536/65536) | err=0
# Round 2 seed=#cafebabe | status=LEAK | stale=100.0% (65536/65536) | err=0
# ...
# Total stale bytes leaked: 2621440

```

Seeds 10 different patterns (`0xDEADBEEF`, `0xCAFEBABE`, `0x41414141`, ...) into texture A across rounds, verifies each pattern leaks back through texture B's uninitialized layer 2. 256x256 RGBA8 = 262,144 bytes leaked per round.

### Cross-Origin Visual Reproduction (victim\_layer\_visual.html + poc\_attacker\_layer\_visual.html)

```
./chrome --no-sandbox --disable-gpu-sandbox --use-gl=angle --use-angle=vulkan --ignore-gpu-blocklist

```

Demonstrates real-world cross-origin GPU memory leak between two independent pages:

1. Open `victim_layer_visual.html` — sprays 100 `TEXTURE_2D_ARRAY` textures (256x256x4 layers, ~100 MB) with a distinctive blue+red cross pattern, then **deletes** all textures
2. Open `poc_attacker_layer_visual.html` in a separate tab — probes every 1 second for stale victim data via the layer leak bug
3. **Trigger condition**: The victim page must **navigate away, refresh, or close the tab** so that its WebGL textures are freed back to the GPU memory allocator (VMA free list). While the victim's textures are live, they cannot be reallocated to the attacker.
4. After victim navigation/close, the attacker's new `TEXTURE_2D_ARRAY` allocations reuse the same VMA blocks → `readPixels` on uninitialized layer 2 returns the victim's stale cross pattern

This matches the real-world attack scenario: a victim browses a GPU-intensive site (Google Maps satellite tiles, Google Earth 3D terrain, video conferencing frames), then navigates away. The attacker page — open in another tab — continuously probes and recovers the victim's freed GPU texture data.

#### Impact analysis

## Impact

A WebGL2 page can read GPU pixel data left behind by other websites after they navigate away. An attacker page continuously probes for reused GPU memory blocks; when a victim page (e.g. Google Maps, Google Earth, Google Meet) navigates away and its textures are freed, the attacker recovers the victim's rendered pixel data — satellite imagery, map tiles, video frames — without any user interaction.

cross\_origin\_texture\_leak\_poc\_1.png : Google Maps/Earth satellite imagery tiles (which were freed via leaving / navigating to other page) visible in leaked stale texture data on above aws environment. (Please check image attachments)

---

### The cause

#### What version of Chrome have you found the security issue in?

147.0.7726.0

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Information Leak

#### How would you like to be publicly acknowledged for your report?

sweetchip

## Attachments

- [cross_origin_texture_leak_poc_2.png](attachments/cross_origin_texture_leak_poc_2.png) (image/png, 620.2 KB)
- [poc_html_result.png](attachments/poc_html_result.png) (image/png, 16.9 KB)
- [poc_v2_enhanced_html_result.png](attachments/poc_v2_enhanced_html_result.png) (image/png, 151.2 KB)
- [cross_origin_texture_leak_poc_1.png](attachments/cross_origin_texture_leak_poc_1.png) (image/png, 3.0 MB)
- [poc.html](attachments/poc.html) (text/html, 1.8 KB)
- [poc_v2_enhanced.html](attachments/poc_v2_enhanced.html) (text/html, 12.9 KB)
- [poc_attacker_layer_visual.html](attachments/poc_attacker_layer_visual.html) (text/html, 7.4 KB)
- [victim_layer_visual.html](attachments/victim_layer_visual.html) (text/html, 6.2 KB)

## Timeline

### th...@chromium.org (2026-03-12)

[security shepherd] Triaging this speculatively because I don't have the hardware to repro this.

- severity high because this is a cross-origin read
- Found In current extended stable 146 based on old culprit CL
- security impact none because this depends on DefaultANGLEVulkan (based on discussing similar issues with other security folks)

syoussefi@: could you PTAL? And please correct me if I'm wrong on security impact none on this bug.

### sy...@chromium.org (2026-03-19)

This is not a Vulkan-only bug and affects all backends.

### dx...@google.com (2026-03-20)

Project: angle/angle  

Branch:  main  

Author:  Shahbaz Youssefi [syoussefi@chromium.org](mailto:syoussefi@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7684418>

Fix robust init vs arrayed textures vs glClear

---


Expand for full commit details
```
     
    Bug: chromium:492131521 
    Change-Id: I534f34a52574084808ca0ecd024f5034c565f579 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7684418 
    Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org> 
    Reviewed-by: Geoff Lang <geofflang@chromium.org>

```

---

Files:

- M `src/libANGLE/Framebuffer.cpp`
- M `src/libANGLE/Framebuffer.h`
- M `src/libANGLE/FramebufferAttachment.cpp`
- M `src/libANGLE/FramebufferAttachment.h`
- M `src/tests/gl_tests/RobustResourceInitTest.cpp`

---

Hash: [2c0fcdce8c915937764f57c70a30c5e07432645a](https://chromiumdash.appspot.com/commit/2c0fcdce8c915937764f57c70a30c5e07432645a)  

Date: Thu Mar 19 18:36:55 2026


---

### dx...@google.com (2026-03-21)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7688907>

Roll ANGLE from b3e2ed202878 to ae66dc5ad350 (3 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/b3e2ed202878..ae66dc5ad350 
     
    2026-03-20 yuxinhu@google.com IR Validation: validate merge_block with input has right precondition 
    2026-03-20 cclao@google.com Remove is_official_build recommendation from DevSetupAndroid.md 
    2026-03-20 syoussefi@chromium.org Fix robust init vs arrayed textures vs glClear 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/angle-chromium-autoroll 
    Please CC abdolrashidi@google.com,angle-team@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:492131521 
    Tbr: abdolrashidi@google.com 
    Change-Id: I5e3a08268fb27d74b2eb68b8c02d9ffc0ac64abb 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7688907 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1602944}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [7f9be90fdefad6e8a3d850c97d561c813e6e6f06](https://chromiumdash.appspot.com/commit/7f9be90fdefad6e8a3d850c97d561c813e6e6f06)  

Date: Sat Mar 21 01:39:37 2026


---

### sy...@chromium.org (2026-03-21)

@th...@chromium.org, per [Comment#3](https://issues.chromium.org/issues/492131521#comment3), I don't believe this should be Security\_Impact-None. I don't have permission to adjust that.

### ch...@google.com (2026-03-22)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-22)

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to stable (M146) because latest trunk commit (1602944) appears to be after stable branch point (1582197).

Merge review required: a commit with DEPS changes was detected.

Requesting merge to beta (M147) because latest trunk commit (1602944) appears to be after beta branch point (1596535).

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dr...@chromium.org (2026-03-23)

No crashes in Canary, approved to merge to M146 and M147.

### sy...@chromium.org (2026-03-25)

1. <https://chromium-review.googlesource.com/7684418>
2. See above
3. No
4. No
5. No

### dx...@google.com (2026-03-26)

2 changes merged

---

Project: angle/angle  

Branch:  chromium/7680  

Author:  Shahbaz Youssefi [syoussefi@chromium.org](mailto:syoussefi@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7703896>

M146: Fix robust init vs arrayed textures vs glClear

---


Expand for full commit details
```
     
    Bug: chromium:492131521 
    Change-Id: Iaa548b3ec218982f2c0a8d5dcfedacbcdd6e01bb 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7703896 
    Reviewed-by: Amirali Abdolrashidi <abdolrashidi@google.com>

```

---

Files:

- M `src/libANGLE/Framebuffer.cpp`
- M `src/libANGLE/Framebuffer.h`
- M `src/libANGLE/FramebufferAttachment.cpp`
- M `src/libANGLE/FramebufferAttachment.h`
- M `src/tests/gl_tests/RobustResourceInitTest.cpp`

---

Hash: [20cdc4df2569eb31ad76c4085f8e9c62e9df7369](https://chromiumdash.appspot.com/commit/20cdc4df2569eb31ad76c4085f8e9c62e9df7369)  

Date: Thu Mar 19 18:36:55 2026


---


---

Project: angle/angle  

Branch:  chromium/7727  

Author:  Shahbaz Youssefi [syoussefi@chromium.org](mailto:syoussefi@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7703897>

M147: Fix robust init vs arrayed textures vs glClear

---


Expand for full commit details
```
     
    Bug: chromium:492131521 
    Change-Id: Ib443519134da887bb09f7b2590b4106acd9cfb12 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7703897 
    Reviewed-by: Amirali Abdolrashidi <abdolrashidi@google.com>

```

---

Files:

- M `src/libANGLE/Framebuffer.cpp`
- M `src/libANGLE/Framebuffer.h`
- M `src/libANGLE/FramebufferAttachment.cpp`
- M `src/libANGLE/FramebufferAttachment.h`
- M `src/tests/gl_tests/RobustResourceInitTest.cpp`

---

Hash: [ec6513ff696e3a8652cc23f09401e6e019eb233b](https://chromiumdash.appspot.com/commit/ec6513ff696e3a8652cc23f09401e6e019eb233b)  

Date: Thu Mar 19 18:36:55 2026


---

### sp...@google.com (2026-05-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline with bisect. User information disclosure


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/492131521)*
