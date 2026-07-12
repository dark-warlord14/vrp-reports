# ANGLE Vulkan: invalidateFramebuffer Erases Pending robust_resource_init Clear, Leads to Cross-Origin GPU Texture Data Leak

| Field | Value |
|-------|-------|
| **Issue ID** | [492153658](https://issues.chromium.org/issues/492153658) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE, Internals>GPU>Vulkan |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sw...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2026-03-12 |
| **Bounty** | $3,000.00 |

## Description

---

### Report description

ANGLE Vulkan: invalidateFramebuffer Erases Pending robust\_resource\_init Clear, Leads to Cross-Origin GPU Texture Data Leak

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

## Summary

ANGLE's Vulkan backend processes `invalidateFramebuffer()` in two internal phases. First, `syncState()` migrates the pending robust-init clear from the image's staged updates into `mDeferredClears` — and **removes** it from the image's update queue (`flushSingleSubresourceStagedUpdates` in vk\_helpers.cpp). Then `invalidateImpl()` unconditionally calls `mDeferredClears.reset(colorIndexGL)` (FramebufferVk.cpp), destroying the **only remaining** initialization path. After this, no code path re-creates the robust-init clear. A subsequent scissored `clear()` starts a render pass with `loadOp = DontCare` because `hasDefinedContent()` returns false, leaving untouched pixels filled with stale VMA data from any previously freed texture. `readPixels()` on those pixels bypasses all init checks and returns the stale data directly to JavaScript.

Chrome's GPU process shares a single `VmaAllocator` across all tabs and origins (`global_texture_share_group = true`, service\_utils.cc:144). When a victim page navigates away and its textures are freed, the VMA sub-allocations return to the free list. An attacker page allocating same-sized textures receives the same VMA blocks. With the robust-init bypass above, `readPixels()` on the attacker's texture returns the victim's stale pixel data — satellite imagery, map tiles, video frames — without any user interaction.

## Tested on

- AWS G4DN instance (Nvidia T4)
- Ubuntu 24.04.4 server + XRDP
- Chromium ASAN build (Vulkan backend)
- For reliable reproduction, I recommend testing under the same or similar environment (NVIDIA GPU + Linux + Vulkan backend). See the Notes section for details on hardware-dependent behavior.

## Root Cause

The bug is a three-step destruction of the robust-init clear during `invalidateFramebuffer()`. The key insight is that `invalidateFramebuffer()` triggers `syncState()` as a side effect, which migrates the robust-init clear into a transient location (`mDeferredClears`) — and then `invalidateImpl()` immediately destroys it.

```
// Step 1: syncState() migrates robust init from staged updates to deferred clears
// vk_helpers.cpp — flushSingleSubresourceStagedUpdates()
if (foundClear.valid())
{
    const ClearUpdate &update = (*levelUpdates)[foundIndex].data.clear;
    deferredClears->store(deferredClearIndex, update.aspectFlags, update.value);
    //                    ^ robust init clear now lives in mDeferredClears
    removeSingleSubresourceStagedUpdates(contextVk, levelGL, layer, layerCount);
    //  ← REMOVED from image staged updates
}

```
```
// Step 2: invalidateImpl() destroys the deferred clear
// FramebufferVk.cpp — invalidateImpl()
for (size_t colorIndexGL : invalidateColorBuffers)
{
    mDeferredClears.reset(colorIndexGL);    // ← BUG: erases the ONLY remaining robust init clear
}

```
```
// Step 3: next render pass sees undefined content, uses DontCare
// FramebufferVk.cpp — startNewRenderPass()
const vk::RenderPassLoadOp loadOp = colorRenderTarget->hasDefinedContent()
                                        ? vk::RenderPassLoadOp::Load
                                        : vk::RenderPassLoadOp::DontCare;  // ← stale data preserved

```

No path re-creates the robust-init clear after Step 2. The initialization is permanently lost.

### Timeline

| Date | Commit | Description |
| --- | --- | --- |
| 2020-04-24 | `d657e1d744` | "Vulkan: Defer framebuffer clears" — introduces `flushSingleSubresourceStagedUpdates`, which migrates robust-init clears from staged updates into `mDeferredClears`. Bug not yet present. |
| **2020-07-20** | **`f6659b3df02`** | **"Vulkan: Fix invalidate + deferred clear" — adds unconditional `mDeferredClears.reset(colorIndexGL)` inside `invalidateImpl()`. This is the commit that introduced the vulnerability.** |

### Execution Flow

```
texStorage2D()              stages robust init clear as SubresourceUpdate (Clear type)

framebufferTexture2D()      marks FBO as dirty, triggers syncState on next operation

invalidateFramebuffer():
  prepareForInvalidate()
    syncDirtyObject()
      syncState()
        flushColorAttachmentUpdates()
          flushSingleSubresourceStagedUpdates()
            → robust init clear MOVED to mDeferredClears
            → staged update REMOVED from image
  invalidateImpl()
    mDeferredClears.reset(colorIndexGL)                      ← BUG: destroys robust init
    invalidateEntireContent() → clearLevelContentDefined()

clear() with scissor:
  startNewRenderPass()
    hasDefinedContent() = false → loadOp = DontCare
    → Vulkan driver skips initialization of untouched pixels
    → GPU writes ONLY scissored region

readPixels()                → returns stale VMA data from ANY previous allocation → INFO LEAK

```
## Reproduction Steps

### Minimal Reproduction (poc.html)

```
./chrome --headless=new --no-sandbox --disable-gpu-sandbox \
  --use-gl=angle --use-angle=vulkan --ignore-gpu-blocklist \
  poc.html --dump-dom

```

1. Create texture `A` (2x1 RGBA8), clear to yellow `[255,255,0,255]`, delete it
2. Create texture `B` (same size), call `invalidateFramebuffer(GL_FRAMEBUFFER, [GL_COLOR_ATTACHMENT0])`
3. Scissor-clear only the left pixel of `B` to blue
4. `readPixels()` the full row

```
**Check 'poc_html_result.png'**
Expected:  B = [0,0,255,255, 0,0,0,0]       (right pixel zero-initialized by robust init)
Actual:    B = [0,0,255,255, 255,255,0,255]  (right pixel = deleted texture A's yellow)

```
### Cross-Origin Visual Reproduction (victim\_visual\_v3.html + poc\_attacker\_visual\_v3.html)

```
./chrome --no-sandbox --disable-gpu-sandbox --use-gl=angle --use-angle=vulkan --ignore-gpu-blocklist

```

Demonstrates real-world cross-origin GPU memory leak between two independent pages:

1. Open `victim_visual_v3.html` in tab 1 — sprays 200 x 512x512 textures (~200 MB) with a distinctive blue background + red cross pattern, then **deletes** all textures. Wait for status bar to turn green ("READY").
2. Open `poc_attacker_visual_v3.html` in tab 2 — exhausts VMA free list with 300 fillers, then continuously probes every 1 second via `invalidateFramebuffer` + scissor clear + bulk `readPixels`
3. **Trigger condition**: The victim page must **navigate away, refresh, or close the tab** so that its WebGL textures are freed back to the GPU memory allocator (VMA free list). While the victim's textures are live, they cannot be reallocated to the attacker.
4. After victim navigation/close, the attacker's probes start hitting stale VMA blocks — victim's cross pattern becomes visible in the leaked canvases (newest results appear first)

This matches the real-world attack scenario: a victim browses a GPU-intensive site (Google Maps satellite tiles, Google Earth 3D terrain, video conferencing frames), then navigates away. The attacker page — open in another tab — continuously probes and recovers the victim's freed GPU texture data.

**cross\_tab\_texture\_leak\_poc\_2.png** : Cross-origin texture patterns deterministically leaked between two independent tabs on different origins. Please check image attachments.

## Notes

- **ASAN cannot detect this vulnerability.** The stale data resides in GPU device memory (VRAM), which is outside ASAN's instrumentation scope. All CPU-side operations (staging buffer allocation, `memcpy` to JavaScript `ArrayBuffer`) are correctly sized and within bounds. The bug produces wrong *data content* (stale instead of zero), not an out-of-bounds memory access — so no ASAN signal is expected.
- **Reproduction depends on GPU hardware and driver.** The leaked data comes from VRAM blocks that are freed and reallocated by the GPU driver's memory allocator (Vulkan VMA). Whether stale data persists depends on the driver's allocation behavior:
  - NVIDIA Vulkan: does **not** zero-fill VRAM on allocation → reproducible!
  - Apple Metal: didn't tested.
  - VRAM reuse also depends on texture size alignment and allocator fragmentation — same-sized textures maximize reuse probability.

## Suggested Fix

1. **Quick fix**: In `invalidateImpl()` (FramebufferVk.cpp), skip `mDeferredClears.reset()` when `robust_resource_initialization` is enabled. The invalidate should mark content as undefined for the rendering optimization, but the robust-init clear must still execute to prevent stale data exposure from the shared VMA pool:

```
for (size_t colorIndexGL : invalidateColorBuffers)
{
    if (!contextVk->isRobustResourceInitEnabled())
    {
        mDeferredClears.reset(colorIndexGL);
    }
}

```

2. **Thorough fix**: Audit all `mDeferredClears.reset()` call sites in FramebufferVk.cpp (14 total) to ensure none can erase a pending robust-init clear. Consider tagging deferred clears with their origin (robust-init vs. application-requested) so that invalidation can selectively preserve initialization clears while still optimizing away application clears.

#### Impact analysis

## Impact

- A WebGL2 page can read GPU pixel data left behind by other websites after they navigate away. An attacker page continuously probes for reused GPU memory blocks; when a victim page (e.g. Google Maps, Google Earth, Google Meet) navigates away and its textures are freed, the attacker recovers the victim's rendered pixel data — satellite imagery, map tiles, video frames — without any user interaction.
- Please check an attachment file 'cross\_origin\_texture\_leak\_poc.png'.

---

### The cause

#### What version of Chrome have you found the security issue in?

147.0.7726.0

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Information Leak

#### How would you like to be publicly acknowledged for your report?

sweetchip

## Attachments

- [poc_html_result.png](attachments/poc_html_result.png) (image/png, 13.5 KB)
- [cross_origin_texture_leak_poc.png](attachments/cross_origin_texture_leak_poc.png) (image/png, 1.5 MB)
- [cross_tab_texture_leak_poc_2.png](attachments/cross_tab_texture_leak_poc_2.png) (image/png, 495.1 KB)
- [poc.html](attachments/poc.html) (text/html, 1.8 KB)
- [poc_attacker_visual_v3.html](attachments/poc_attacker_visual_v3.html) (text/html, 6.1 KB)
- [victim_visual_v3.html](attachments/victim_visual_v3.html) (text/html, 6.4 KB)

## Timeline

### dc...@chromium.org (2026-03-13)

Per Geoff, this doesn't have a security impact because it depends on `DefaultANGLEVulkan`. I'm unable to personally reproduce though.

### dx...@google.com (2026-03-28)

Project: angle/angle  

Branch:  main  

Author:  Shahbaz Youssefi [syoussefi@chromium.org](mailto:syoussefi@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7697282>

Vulkan: Fix robust resource init vs invalidate

---


Expand for full commit details
```
     
    If robust resource init is enabled, invalidate should not leave the 
    contents of the image undefined.  With this change, after the 
    framebuffer is invalidated, the render pass store op is still 
    STORE_OP_DONT_CARE so that it would be efficient, but a robust init 
    clear is restaged in the image.  In the next render pass, or on 
    read-back, the content is cleared again automatically. 
     
    Bug: chromium:492153658 
    Change-Id: I84089b955c44be1569ed1d71ab406d3df681590f 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7697282 
    Reviewed-by: Amirali Abdolrashidi <abdolrashidi@google.com> 
    Reviewed-by: Charlie Lao <cclao@google.com> 
    Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/vulkan/FramebufferVk.cpp`
- M `src/libANGLE/renderer/vulkan/RenderbufferVk.cpp`
- M `src/libANGLE/renderer/vulkan/SurfaceVk.cpp`
- M `src/libANGLE/renderer/vulkan/vk_helpers.cpp`
- M `src/libANGLE/renderer/vulkan/vk_helpers.h`
- M `src/libANGLE/renderer/vulkan/vk_renderer.cpp`
- M `src/tests/angle_end2end_tests_expectations.txt`
- M `src/tests/gl_tests/RobustResourceInitTest.cpp`

---

Hash: [8d8796935e4faeaf19e67ac0a5949e71a5252e7f](https://chromiumdash.appspot.com/commit/8d8796935e4faeaf19e67ac0a5949e71a5252e7f)  

Date: Tue Mar 24 20:44:38 2026


---

### dx...@google.com (2026-03-28)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7709301>

Roll ANGLE from 2b53114def9f to 8d8796935e4f (1 revision)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/2b53114def9f..8d8796935e4f 
     
    2026-03-28 syoussefi@chromium.org Vulkan: Fix robust resource init vs invalidate 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/angle-chromium-autoroll 
    Please CC angle-team@google.com,yuxinhu@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:492153658 
    Tbr: yuxinhu@google.com 
    Change-Id: I14ecc64bb8d0ca30dcd45e2840f0bd22eee6fafd 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7709301 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1606632}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [527fe1550b1635b908705f6d54becf3414232330](https://chromiumdash.appspot.com/commit/527fe1550b1635b908705f6d54becf3414232330)  

Date: Sat Mar 28 05:56:52 2026


---

### sw...@gmail.com (2026-05-21)

Hello, Would it be possible to have a CVE assigned (or to share the CVE ID once it's allocated)?

### sp...@google.com (2026-05-21)

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

### ch...@google.com (2026-07-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/492153658)*
