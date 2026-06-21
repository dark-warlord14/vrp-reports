# Integer overflow in ANGLE TextureVk::reinitImageAsRenderable leads to heap buffer overflow in GPU process

| Field | Value |
|-------|-------|
| **Issue ID** | [487208468](https://issues.chromium.org/issues/487208468) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>Vulkan |
| **Platforms** | Linux, Windows, ChromeOS |
| **Reporter** | yu...@gmail.com |
| **Assignee** | ab...@google.com |
| **Created** | 2026-02-24 |
| **Bounty** | $17,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md

Please see the following link for instructions on filing security bugs: https://www.chromium.org/Home/chromium-security/reporting-security-bugs

Reports may be eligible for reward payments under the Chrome VRP: https://g.co/chrome/vrp

NOTE: Security bugs are normally made public once a fix has been widely deployed.

-------------------------

VULNERABILITY DETAILS

Integer overflow in ANGLE TextureVk::reinitImageAsRenderable() leads to heap
buffer overflow in the GPU process via WebGL2.

When a WebGL2 TEXTURE_2D_ARRAY with RGB16F internal format is bound as a
framebuffer attachment, ANGLE's Vulkan backend converts the texture from
sample-only format (R16G16B16_FLOAT, 6 bytes/pixel) to renderable format
(R16G16B16A16_FLOAT, 8 bytes/pixel). The destination staging buffer size
calculation at TextureVk.cpp:3167-3168 uses mixed-type integer arithmetic
that silently overflows uint32, producing a zero-byte allocation. The
subsequent CopyImageCHROMIUM call writes up to 4 GB of attacker-supplied
texture data into this ~64-byte buffer, causing a heap buffer overflow in the
GPU process.

This is triggerable from any web page using WebGL2 JavaScript, with no user
interaction beyond visiting the page.


ROOT CAUSE

File: third_party/angle/src/libANGLE/renderer/vulkan/TextureVk.cpp
Function: TextureVk::reinitImageAsRenderable()
Lines: 3167-3168

Vulnerable code:

    size_t dstBufferSize = sourceBox.width * sourceBox.height * sourceBox.depth *
                           dstFormat.pixelBytes * layerCount;

C++ type promotion analysis (left-to-right, usual arithmetic conversions):

  Step 1: sourceBox.width (int) * sourceBox.height (int) -> int
          16384 * 16384 = 268,435,456  (fits in int32)

  Step 2: result (int) * sourceBox.depth (int) -> int
          268,435,456 * 1 = 268,435,456  (fits in int32)

  Step 3: result (int) * dstFormat.pixelBytes (GLuint/unsigned int) -> unsigned int
          int promoted to unsigned int per C++ [conv.rank]:
          268,435,456u * 8u = 2,147,483,648  (fits in uint32)

  Step 4: result (unsigned int) * layerCount (uint32_t) -> unsigned int
          2,147,483,648u * 2u = 4,294,967,296 = 2^32
          WRAPS TO 0 (unsigned overflow is defined behavior per C++ [basic.fundamental])

  Step 5: 0u zero-extended to size_t -> dstBufferSize = 0

Chromium builds with -fno-strict-overflow (build/config/compiler/BUILD.gn),
making the signed multiplication at step 1 deterministic (two's complement).
The uint32 wrap at step 4 is defined behavior per the C++ standard.

The overflowed dstBufferSize (0) is passed to stageSubresourceUpdateAndGetData()
at line 3172, which allocates a buffer of ~64 bytes (imageCopyAlignment padding,
see ContextVk.cpp:7093). CopyImageCHROMIUM at lines 3192-3197 then writes
width * height * dstPixelBytes * layerCount = 4,294,967,296 bytes into this
64-byte buffer.

Additionally, both the source buffer allocation (vk_helpers.cpp:10747-10748)
and all pitch calculations (TextureVk.cpp:3177-3184, GLuint type) contain the
same overflow pattern, causing both GPU-side and CPU-side out-of-bounds access.

A standalone C program (verify_overflow.c) is attached that reproduces the
exact type promotion chain and confirms the overflow to zero.


TRIGGER PATH (WebGL2 JavaScript -> GPU process heap overflow)

1. Create a TEXTURE_2D_ARRAY with gl.RGB16F internal format
   - ANGLE maps to VK_FORMAT_R16G16B16_SFLOAT on Vulkan
   - On NVIDIA/AMD, this format supports sampling but NOT rendering
   - SampleOnly format: R16G16B16_FLOAT (pixelBytes = 6)
   - Renderable fallback: R16G16B16A16_FLOAT (pixelBytes = 8)

2. Choose dimensions where width * height * 8 * layers = 2^32:
   - 16384 x 16384 x 2 layers  (requires ~3.2 GB VRAM)
   - 8192  x 8192  x 8 layers  (requires ~3.2 GB VRAM)
   - 4096  x 4096  x 32 layers (requires ~3.2 GB VRAM)

3. Bind texture to framebuffer via gl.framebufferTextureLayer()
   -> sets mState.hasBeenBoundAsAttachment() = true

4. Issue a draw call (gl.drawArrays) to trigger syncState():
   -> TextureVk.cpp:3840: respecifyImageStorageIfNecessary()
   -> Line 3641: checks hasBeenBoundAsAttachment()
   -> Line 3644: ensureRenderable() -> ensureRenderableWithFormat()
   -> Line 4835: sets mRequiredFormatSupport = Renderable
   -> Line 4907: respecifyImageStorage()
   -> Line 3256-3258: detects format mismatch (R16G16B16_FLOAT != R16G16B16A16_FLOAT)
   -> Line 3260: reinitImageAsRenderable()

5. In reinitImageAsRenderable() multi-layer slow path (line 3138):
   -> Line 3111: layerCount > 1, takes CPU copy path (not draw path)
   -> Line 3158: copyImageDataToBuffer() reads GPU texture to srcBuffer
   -> Line 3167: dstBufferSize = 16384*16384*1*8*2 = 2^32 -> WRAPS TO 0
   -> Line 3172: stageSubresourceUpdateAndGetData() allocates ~64 bytes
   -> Lines 3192-3197: CopyImageCHROMIUM writes 4 GB to 64-byte buffer
   -> HEAP BUFFER OVERFLOW


ADDITIONAL OVERFLOW INSTANCES (same unchecked pattern)

The ANGLE Vulkan renderer contains at least 15 instances of the same
vulnerability pattern (unchecked integer multiplication for buffer sizing).
None use CheckedNumeric or any overflow validation. Key locations:

a) vk_helpers.cpp:10747-10748 - copyImageDataToBuffer()
   size_t bufferSize = sourceArea.width * sourceArea.height *
                       sourceArea.depth * pixelBytes * layerCount;
   Overflows the SOURCE staging buffer; called from the same trigger path.

b) TextureVk.cpp:1781-1782 - copySubTextureImpl()
   size_t destinationAllocationSize =
       sourceBox.width * sourceBox.height * sourceBox.depth *
       dstTextureFormat.pixelBytes;
   Reachable via gl.copyTexSubImage3D() with cross-format textures.

c) TextureVk.cpp:2891-2893 - generateMipmapsWithCPU()
   GLuint sourceRowPitch = baseLevelExtents.width * angleFormat.pixelBytes;
   GLuint sourceDepthPitch = sourceRowPitch * baseLevelExtents.height;
   size_t baseLevelAllocationSize = sourceDepthPitch * baseLevelExtents.depth;
   GLuint pitch overflows, truncated value used for buffer offset calculation.

d) TextureVk.cpp:1812-1816 - copySubTextureImpl() pitches
   GLuint srcDataRowPitch/dstDataRowPitch/srcDataDepthPitch/dstDataDepthPitch
   Same GLuint overflow pattern in pitch calculations.

e) vk_helpers.cpp:8792-8796 - reformatStagedBufferUpdates()
   Same GLuint row/depth pitch overflow pattern.

f) vk_helpers.cpp:9387 - readPixelsImpl() conversion path
g) vk_helpers.cpp:11195-11215 - readPixelsImpl() depth/stencil path
h) vk_helpers.cpp:11455 - readPixelsImpl() allocation
i) SurfaceVk.cpp:284-286 - readPixels() GLuint rowStride overflow


IMPACT

- Heap buffer overflow in Chrome's GPU process, triggered from WebGL2 JS
- Attacker-supplied texture data (uploaded via texSubImage3D) is written
  past the staging buffer bounds via CopyImageCHROMIUM
- Up to 4 GB written to a ~64-byte buffer
- No user interaction required beyond visiting a malicious web page
- The GPU process has a more permissive sandbox than the renderer process
  (weaker seccomp-bpf filter on Linux, broader syscall allowlist)


AFFECTED PLATFORMS

Requires a GPU where VK_FORMAT_R16G16B16_SFLOAT supports sampling
(VK_FORMAT_FEATURE_SAMPLED_IMAGE_BIT) but NOT rendering
(no VK_FORMAT_FEATURE_COLOR_ATTACHMENT_BIT):

- NVIDIA GPUs on Linux and Windows (nvidia-driver-535+): AFFECTED
- AMD GPUs on Linux (RADV/AMDVLK) and Windows: AFFECTED
- macOS (Metal backend): NOT affected (Metal uses RGBA16F for both)
- Mobile/Android: NOT affected (most mobile GPUs differ)

Additional requirements:
- MAX_TEXTURE_SIZE >= 4096 (universal on desktop GPUs)
- VRAM >= ~3.2 GB (common on modern desktop GPUs, GTX 1070+)
- Chrome using ANGLE Vulkan backend (default on Linux)


SUGGESTED FIX

1. Use checked arithmetic for dstBufferSize (TextureVk.cpp:3167-3168):

   base::CheckedNumeric<size_t> dstBufferSize =
       base::CheckedNumeric<size_t>(sourceBox.width) * sourceBox.height *
       sourceBox.depth * dstFormat.pixelBytes * layerCount;
   if (!dstBufferSize.IsValid()) {
       return angle::Result::Stop;
   }

2. Fix copySubTextureImpl allocation (TextureVk.cpp:1781-1782):

   base::CheckedNumeric<size_t> destinationAllocationSize =
       base::CheckedNumeric<size_t>(sourceBox.width) * sourceBox.height *
       sourceBox.depth * dstTextureFormat.pixelBytes;

3. Change pitch types from GLuint to size_t (TextureVk.cpp:3177-3184):

   size_t srcDataRowPitch = static_cast<size_t>(sourceBox.width) *
                            srcFormat.pixelBytes;
   size_t dstDataRowPitch = static_cast<size_t>(sourceBox.width) *
                            dstFormat.pixelBytes;
   size_t srcDataDepthPitch = srcDataRowPitch * sourceBox.height;
   size_t dstDataDepthPitch = dstDataRowPitch * sourceBox.height;

4. Apply the same pattern to all 15 affected locations listed above.


VERSION

Chrome Version: 147.0.7682.0 (Developer Build, 64-bit)
ANGLE: Vulkan backend
Operating System: Linux or Windows with NVIDIA/AMD Vulkan GPU

The vulnerable code has been present since at least Chrome 100
(reinitImageAsRenderable was introduced for format fallback support).


REPRODUCTION CASE

Prerequisites:
- Linux system with NVIDIA or AMD GPU (Vulkan driver installed)
- GPU VRAM >= 3.2 GB
- Chrome with ANGLE Vulkan backend (default on Linux)

To verify the format prerequisite, run:
  vulkaninfo | grep -A5 "VK_FORMAT_R16G16B16_SFLOAT"
  -> VK_FORMAT_FEATURE_SAMPLED_IMAGE_BIT should be present
  -> VK_FORMAT_FEATURE_COLOR_ATTACHMENT_BIT should be ABSENT

Steps:
1. Serve poc.html locally:
     python3 -m http.server 8080

2. Open Chrome:
     chrome --use-angle=vulkan http://localhost:8080/poc.html

3. Click "Check Environment" to verify:
   - WebGL2 is available
   - RGB16F is NOT renderable (FBO status is INCOMPLETE)
   - "This system is vulnerable to the overflow" message appears

4. Click "Run PoC" to trigger the overflow:
   - Expected: GPU process crashes, WebGL context is lost

For ASAN builds (recommended for clear crash report):
  gn gen out/asan --args='
    is_asan = true
    is_debug = false
    is_component_build = false
    dcheck_always_on = true
    target_cpu = "x64"
    angle_enable_vulkan = true
  '
  autoninja -C out/asan chrome
  out/asan/chrome --use-angle=vulkan --no-sandbox --disable-gpu-sandbox \
    http://localhost:8080/poc.html

Expected ASAN output:
  ==GPU_PID==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x...
  WRITE of size ... at 0x... thread T...
      #0 in angle::CopyImageCHROMIUM(...)
      #1 in rx::TextureVk::reinitImageAsRenderable(...)
      #2 in rx::TextureVk::respecifyImageStorage(...)

Standalone arithmetic verification (no GPU required):
  cc -o verify_overflow verify_overflow.c && ./verify_overflow
  This confirms dstBufferSize overflows to 0 using the exact C++ type
  promotion rules, independent of any hardware.

If the system has < 3.2 GB free VRAM, texStorage3D will fail with
OUT_OF_MEMORY. Use a GPU with more VRAM, or adjust dimensions (any
combination where width * height * 8 * layers >= 2^32 triggers the overflow).


FOR CRASHES

Type of crash: GPU process crash (not tab, not browser)
Crash state (from source analysis, ASAN build on affected hardware required
for runtime stack trace):

  Expected crash stack:
    angle::CopyImageCHROMIUM(...)                       <- writes 4 GB to 64-byte buffer
    rx::TextureVk::reinitImageAsRenderable(...)         <- TextureVk.cpp:3192
    rx::TextureVk::respecifyImageStorage(...)            <- TextureVk.cpp:3260
    rx::TextureVk::respecifyImageStorageIfNecessary(...) <- TextureVk.cpp:3641
    rx::TextureVk::syncState(...)                        <- TextureVk.cpp:3840

  Root cause frame: TextureVk.cpp:3167-3168
    size_t dstBufferSize = sourceBox.width * sourceBox.height * sourceBox.depth *
                           dstFormat.pixelBytes * layerCount;
    // Evaluates to 0 due to uint32 overflow (16384*16384*1*8*2 = 2^32 -> 0)

  Allocation frame: TextureVk.cpp:3172
    stageSubresourceUpdateAndGetData(contextVk, dstBufferSize=0, ...)
    // Allocates ~64 bytes (imageCopyAlignment padding)

  Overflow frame: TextureVk.cpp:3192-3197
    CopyImageCHROMIUM(srcData, ..., dstData, ..., width=16384, height=16384, ...)
    // Writes 16384 * 16384 * 8 = 2,147,483,648 bytes PER LAYER to 64-byte dstData

  The GPU process will crash with SIGSEGV (release/debug build) or report
  heap-buffer-overflow (ASAN build). In a release build, the GPU process
  restarts and the WebGL context is reported as lost.


ATTACHED FILES

1. poc.html           - Self-contained WebGL2 PoC with environment check
2. verify_overflow.c  - Standalone C program proving the integer overflow
                        (reproduces exact C++ type promotion chain)


CREDIT INFORMATION

Reporter credit: heesun

## Attachments

- [poc.html](attachments/poc.html) (text/html, 12.7 KB)
- [verify_overflow.c](attachments/verify_overflow.c) (text/x-csrc, 6.9 KB)

## Timeline

### li...@chromium.org (2026-02-24)

I'm unable to repro on Linux, as my GPU limits are too small.

@sy...@chromium.org - do you mind taking a look or rerouting as necessary?

### ch...@google.com (2026-02-25)

Setting milestone because of s2 severity.

### sy...@chromium.org (2026-02-25)

Thank you for the report. This same bug was reported in [issue 486972661](https://issues.chromium.org/issues/486972661) a few days ago, but yours have identified more places where this problem exists.

Reassigning to @ab...@google.com who's taking care of the other bug.

### yu...@gmail.com (2026-02-25)

Thank you for the update. I'd like to note that the 15 additional overflow instances I identified span different code paths and functions beyond reinitImageAsRenderable():

- copySubTextureImpl() (TextureVk.cpp:1781)
- generateMipmapsWithCPU() (TextureVk.cpp:2891) 
- copyImageDataToBuffer() (vk_helpers.cpp:10747)
- reformatStagedBufferUpdates() (vk_helpers.cpp:8792)
- readPixelsImpl() (vk_helpers.cpp:9387, 11195, 11455)
- SurfaceVk::readPixels() (SurfaceVk.cpp:284)

These are reachable through different WebGL API entry points(copyTexSubImage3D, generateMipmap, readPixels) and each contains independent unchecked integer arithmetic that would need separate fixes. Happy to assist with patches if helpful.


### dx...@google.com (2026-03-02)

Project: angle/angle  

Branch:  main  

Author:  Amirali Abdolrashidi [abdolrashidi@google.com](mailto:abdolrashidi@google.com)  

Link:    <https://chromium-review.googlesource.com/7615650>

Vulkan: Cap memory allocation size to 1GB

---


Expand for full commit details
```
     
      Currently the maximum memory allocation size for a single object 
    can be inquired from the Vulkan driver via KHR_maintenance3 (promoted 
    to core in Vulkan 1.1). However, the reported limit can still be quite 
    large for common usage. In addition, it can increase the risk of memory 
    size calculations overflowing if the operands are not 64 bits. As an 
    example, if the limit is 4GB and an image is defined with 32-bit dims 
    and format that theoretically require 4GB, the multiplication of these 
    values can result in overflow, even if it is to be assigned to a 64-bit 
    value. 
      * (One way to avoid such overflow cases is to split multiplication 
        into several steps, e.g., CL:7595734) 
     
    This change aims to reduce the maximum size allowed for allocation in 
    order to reduce the risk of such overflow issues. 
     
    * Added kMemoryAllocationSizeLimit to vk_renderer. 
      * Currently set to 1GB. 
     
    * Added to vk::Renderer: mMaxMemoryAllocationSize 
      * Set to the minimum of kMemoryAllocationSizeLimit and 
        the maxMemoryAllocationSize reported from the driver. 
     
    * Cast the values used in some buffer size calculations to 
      size_t. 
      * (The leftmost value being size_t should be enough to propagate 
        this type for the result of each multiplication.) 
     
    * Updated the following test to use a smaller width and height to 
      avoid error due to the new cap: 
      TextureCubeTestES32.MaxArrayTextureLayersVerify 
     
    Bug: chromium:486972661 
    Bug: chromium:487208468 
    Change-Id: I98bde71ede153324f524bb579b19043a474823d5 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7615650 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Commit-Queue: Amirali Abdolrashidi <abdolrashidi@google.com>

```

---

Files:

- M `src/libANGLE/renderer/vulkan/TextureVk.cpp`
- M `src/libANGLE/renderer/vulkan/vk_helpers.cpp`
- M `src/libANGLE/renderer/vulkan/vk_renderer.cpp`
- M `src/libANGLE/renderer/vulkan/vk_renderer.h`
- M `src/tests/gl_tests/TextureTest.cpp`

---

Hash: [4de47461e45248eeaf8fd0ef04ca3949f98029da](https://chromiumdash.appspot.com/commit/4de47461e45248eeaf8fd0ef04ca3949f98029da)  

Date: Thu Feb 26 23:17:40 2026


---

### ab...@google.com (2026-03-02)

Hello,

Based on [comment #1](https://issues.chromium.org/issues/487208468#comment1) (ADDITIONAL OVERFLOW INSTANCES → (a)), the overflow is due to the overflow in `bufferSize`, which was addressed by the following recent change: <https://chromium-review.git.corp.google.com/c/angle/angle/+/7595734>

However, to address a similar issue, [the change above](https://crrev.com/c/7615650) has been submitted. Here, the allocation size for a single device memory on the Vulkan backend has been limited to 1GB (or the reported max size from the driver, whichever is smaller), which should make overflow in the size calculations across the Vulkan backend code less likely.

In addition, in the size calculations in the functions `TextureVk::reinitImageAsRenderable()` and `ImageHelper::copyImageDataToBuffer()`, the dimension operands have been casted to `size_t` to avoid overflow.

This change should resolve the heap overflow issue described at the top. (Unfortunately I was unable to reliably reproduce the issue locally.)

Please feel free to reach out in case of further questions.

Thanks.

### dx...@google.com (2026-03-03)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7623972>

Roll ANGLE from 425ea1de41aa to 71f8079e12be (5 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/425ea1de41aa..71f8079e12be 
     
    2026-03-02 cclao@google.com Vulkan: Only dirty flipXY when it changed. 
    2026-03-02 lexa.knyazev@gmail.com Update GetTexLevelParameter* and multisample texture ANGLE specs 
    2026-03-02 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from 7d6f99b1bd5d to 0b8ee538955f (934 revisions) 
    2026-03-02 ynovikov@chromium.org Promote angle_deqp_egl_vulkan_tests skip to Stable 
    2026-03-02 abdolrashidi@google.com Vulkan: Cap memory allocation size to 1GB 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/angle-chromium-autoroll 
    Please CC angle-team@google.com,ynovikov@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:486972661,chromium:487208468 
    Tbr: ynovikov@google.com 
    Change-Id: I7e767625d9a0f7b69fa3f23702acb6e161be57cd 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7623972 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1592814}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [379e51beedc724b45efe1b5d03102a3365244d2b](https://chromiumdash.appspot.com/commit/379e51beedc724b45efe1b5d03102a3365244d2b)  

Date: Tue Mar 3 00:13:45 2026


---

### dx...@google.com (2026-03-06)

Project: angle/angle  

Branch:  main  

Author:  Amirali Abdolrashidi [abdolrashidi@google.com](mailto:abdolrashidi@google.com)  

Link:    <https://chromium-review.googlesource.com/7633508>

Vulkan: Cast size calculations to reduce overflow

---


Expand for full commit details
```
     
    * Updated or cast some extents used in size calculations to 
      size_t to reduce the possibility of 32-bit overflow if the 
      sizes are too large. 
     
    Bug: chromium:487208468 
    Change-Id: I48a8e14b2d9fd4ceb967f9fd66e9ebc43a78a391 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7633508 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Commit-Queue: Amirali Abdolrashidi <abdolrashidi@google.com>

```

---

Files:

- M `src/libANGLE/renderer/vulkan/TextureVk.cpp`
- M `src/libANGLE/renderer/vulkan/vk_helpers.cpp`

---

Hash: [56c952c65e74493b4a6ce3c0d98f072e46651db3](https://chromiumdash.appspot.com/commit/56c952c65e74493b4a6ce3c0d98f072e46651db3)  

Date: Wed Mar 4 20:14:08 2026


---

### dx...@google.com (2026-03-06)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7642203>

Roll ANGLE from 2ec1a01ba6b2 to 56c952c65e74 (4 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/2ec1a01ba6b2..56c952c65e74 
     
    2026-03-06 abdolrashidi@google.com Vulkan: Cast size calculations to reduce overflow 
    2026-03-06 yuxinhu@google.com IR Validation: validation all registers are declared in scope 
    2026-03-06 m.maiya@samsung.com Update ComputeGenericHash(...) 
    2026-03-06 m.maiya@samsung.com Reland "Update xxhash to version 0.8.3" 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/angle-chromium-autoroll 
    Please CC angle-team@google.com,ynovikov@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:487208468 
    Tbr: ynovikov@google.com 
    Change-Id: I1ae63557852cdafb24e36feb1242a43d798d81be 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7642203 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1595731}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [4f23abf63f001e03990dcfcd1a10eca50099ed7d](https://chromiumdash.appspot.com/commit/4f23abf63f001e03990dcfcd1a10eca50099ed7d)  

Date: Fri Mar 6 23:05:48 2026


---

### ab...@google.com (2026-03-07)

The [change above](https://chromium-review.git.corp.google.com/c/angle/angle/+/7633508/) has been submitted based on the suggestions made in [comment #5](https://issues.chromium.org/issues/487208468#comment5). Thank you. It has also rolled into Chromium.

- Although, regarding `SurfaceVk::LockSurfaceImpl()`, `bufferSize` is already `VkDeviceSize` (64 bits), which is computed from values also cast to `VkDeviceSize`, which should not result in overflow. Therefore, it remains unchanged.

After the submitted changes above, the reported overflow case is no longer expected to occur. Please let us know in case of further issues.

Thank you.

### ab...@google.com (2026-03-09)

Since this change has rolled into Chromium, I will mark this issue as closed.

However, please feel free to re-open in case of further questions or concerns.

### dx...@google.com (2026-03-09)

Project: angle/angle  

Branch:  chromium/7680  

Author:  Amirali Abdolrashidi [abdolrashidi@google.com](mailto:abdolrashidi@google.com)  

Link:    <https://chromium-review.googlesource.com/7648876>

[M146] Vulkan: Cap memory allocation size to 1GB

---


Expand for full commit details
```
     
      Currently the maximum memory allocation size for a single object 
    can be inquired from the Vulkan driver via KHR_maintenance3 (promoted 
    to core in Vulkan 1.1). However, the reported limit can still be quite 
    large for common usage. In addition, it can increase the risk of memory 
    size calculations overflowing if the operands are not 64 bits. As an 
    example, if the limit is 4GB and an image is defined with 32-bit dims 
    and format that theoretically require 4GB, the multiplication of these 
    values can result in overflow, even if it is to be assigned to a 64-bit 
    value. 
      * (One way to avoid such overflow cases is to split multiplication 
        into several steps, e.g., CL:7595734) 
     
    This change aims to reduce the maximum size allowed for allocation in 
    order to reduce the risk of such overflow issues. 
     
    * Added kMemoryAllocationSizeLimit to vk_renderer. 
      * Currently set to 1GB. 
     
    * Added to vk::Renderer: mMaxMemoryAllocationSize 
      * Set to the minimum of kMemoryAllocationSizeLimit and 
        the maxMemoryAllocationSize reported from the driver. 
     
    * Cast the values used in some buffer size calculations to 
      size_t. 
      * (The leftmost value being size_t should be enough to propagate 
        this type for the result of each multiplication.) 
     
    * Updated the following test to use a smaller width and height to 
      avoid error due to the new cap: 
      TextureCubeTestES32.MaxArrayTextureLayersVerify 
     
    Bug: chromium:486972661 
    Bug: chromium:487208468 
    Change-Id: I98bde71ede153324f524bb579b19043a474823d5 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7615650 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Commit-Queue: Amirali Abdolrashidi <abdolrashidi@google.com> 
    (cherry picked from commit 4de47461e45248eeaf8fd0ef04ca3949f98029da) 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7648876 
    Reviewed-by: Yuly Novikov <ynovikov@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/vulkan/TextureVk.cpp`
- M `src/libANGLE/renderer/vulkan/vk_helpers.cpp`
- M `src/libANGLE/renderer/vulkan/vk_renderer.cpp`
- M `src/libANGLE/renderer/vulkan/vk_renderer.h`
- M `src/tests/gl_tests/TextureTest.cpp`

---

Hash: [1a72ef5e089e464fefae8b89922060bdbc5a5d2d](https://chromiumdash.appspot.com/commit/1a72ef5e089e464fefae8b89922060bdbc5a5d2d)  

Date: Thu Feb 26 23:17:40 2026


---

### pe...@google.com (2026-03-09)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ab...@google.com (2026-03-09)

Hello,

1. No
2. No

### qk...@google.com (2026-03-16)

Labeled `LTS-NotApplicable-138` since there were some conflicts[1] when trying to merge the fix to M138. And, it looks like the conflict might not be safe although the cherry-picked patch passed all trybots.

[1] https://chromium-review.git.corp.google.com/c/angle/angle/+/7659084/1..2

### pe...@google.com (2026-04-09)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-04-09)

1. https://chromium-review.git.corp.google.com/c/angle/angle/+/7691581
2. Low - There was a conflict.
3. 146
4. Yes.

### an...@google.com (2026-04-10)

Merge approved for LTS-144.

### dx...@google.com (2026-04-16)

Project: angle/angle  

Branch:  chromium/7559  

Author:  Amirali Abdolrashidi [abdolrashidi@google.com](mailto:abdolrashidi@google.com)  

Link:    <https://chromium-review.googlesource.com/7691581>

[M144-LTS] Vulkan: Cap memory allocation size to 1GB

---


Expand for full commit details
```
     
      Currently the maximum memory allocation size for a single object 
    can be inquired from the Vulkan driver via KHR_maintenance3 (promoted 
    to core in Vulkan 1.1). However, the reported limit can still be quite 
    large for common usage. In addition, it can increase the risk of memory 
    size calculations overflowing if the operands are not 64 bits. As an 
    example, if the limit is 4GB and an image is defined with 32-bit dims 
    and format that theoretically require 4GB, the multiplication of these 
    values can result in overflow, even if it is to be assigned to a 64-bit 
    value. 
      * (One way to avoid such overflow cases is to split multiplication 
        into several steps, e.g., CL:7595734) 
     
    This change aims to reduce the maximum size allowed for allocation in 
    order to reduce the risk of such overflow issues. 
     
    * Added kMemoryAllocationSizeLimit to vk_renderer. 
      * Currently set to 1GB. 
     
    * Added to vk::Renderer: mMaxMemoryAllocationSize 
      * Set to the minimum of kMemoryAllocationSizeLimit and 
        the maxMemoryAllocationSize reported from the driver. 
     
    * Cast the values used in some buffer size calculations to 
      size_t. 
      * (The leftmost value being size_t should be enough to propagate 
        this type for the result of each multiplication.) 
     
    * Updated the following test to use a smaller width and height to 
      avoid error due to the new cap: 
      TextureCubeTestES32.MaxArrayTextureLayersVerify 
     
    Bug: chromium:486972661 
    Bug: chromium:487208468 
    Change-Id: I98bde71ede153324f524bb579b19043a474823d5 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7615650 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Commit-Queue: Amirali Abdolrashidi <abdolrashidi@google.com> 
    (cherry picked from commit 4de47461e45248eeaf8fd0ef04ca3949f98029da) 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7691581 
    Reviewed-by: Amirali Abdolrashidi <abdolrashidi@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com>

```

---

Files:

- M `src/libANGLE/renderer/vulkan/TextureVk.cpp`
- M `src/libANGLE/renderer/vulkan/vk_helpers.cpp`
- M `src/libANGLE/renderer/vulkan/vk_renderer.cpp`
- M `src/libANGLE/renderer/vulkan/vk_renderer.h`
- M `src/tests/gl_tests/TextureTest.cpp`

---

Hash: [f56543421c45455f1c5d746a4d84ebe0549da745](https://chromiumdash.appspot.com/commit/f56543421c45455f1c5d746a4d84ebe0549da745)  

Date: Thu Feb 26 23:17:40 2026


---

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $17000.00 for this report.

Rationale for this decision:
Baseline. Renderer RCE / memory corruption in a sandboxed process.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/487208468)*
