# Heap OOB read in ANGLE via `CubeMapArray` texture upload due to `endByte` underestimation in `ValidImageDataSize`

| Field | Value |
|-------|-------|
| **Issue ID** | [494823889](https://issues.chromium.org/issues/494823889) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | ab...@google.com |
| **Created** | 2026-03-22 |
| **Bounty** | $3,000.00 |

## Description

## Summary

ANGLE's `ValidImageDataSize` function fails to account for `CubeMapArray` when computing `endByte`, treating it as a 2D upload instead of a 3D one. This causes the PBO bounds check and the robust-variant `bufSize` check to use an underestimated byte count, allowing undersized source buffers to pass validation. The backend then reads the full 3D extent from the undersized buffer, producing a heap-buffer-overflow. The bug is reachable from a compromised renderer on platforms where the ANGLE Vulkan or OpenGL backend exposes the `GL_EXT_texture_cube_map_array` extension (Linux, Android, Windows with Vulkan). It affects the GPU process.

## Bisect

Introducing Commit: `7fde3673a473621063f88faa35294dde43dd07c0`

- Date: 2020-05-27
- Author: Jonah Ryan-Davis
- Review: <https://chromium-review.googlesource.com/c/angle/angle/+/2215306>

This commit added `CubeMapArray` to `ImageIndex::usesTex3D()` and to various frontend dispatch paths, but did not update the `targetIs3D` variable in `ValidImageDataSize`. The original `targetIs3D` check was introduced earlier in commit `ff5b2d5128` when the `GL_ANGLE_robust_client_memory` extension was added.

## Root Cause

`ValidImageDataSize` in `validationES.cpp` determines whether a texture target requires 3D data layout calculations through a local boolean:

```
// third_party/angle/src/libANGLE/validationES.cpp
bool targetIs3D = texType == TextureType::_3D || texType == TextureType::_2DArray;

```

This variable is missing `TextureType::CubeMapArray` (and `TextureType::_2DMultisampleArray`). It is passed to `computePackUnpackEndByte`, which uses it to decide whether to include the depth pitch in the total byte count:

```
// third_party/angle/src/libANGLE/formatutils.cpp
if (is3D)
{
    CheckedNumeric<GLuint> depthMinusOne = size.depth - 1;
    checkedCopyBytes += depthMinusOne * depthPitch;
}

```

When `is3D` is false, the entire depth contribution is omitted. For a 4x4 RGBA8 CubeMapArray texture with depth=6, the correct `endByte` is 64 + 5×64 = 384, but the function computes only 64.

The implementation side does not share this oversight. `ImageIndex::usesTex3D()` correctly includes `CubeMapArray`:

```
// third_party/angle/src/libANGLE/ImageIndex.cpp
bool ImageIndex::usesTex3D() const
{
    return mType == TextureType::_3D || mType == TextureType::_2DArray ||
           mType == TextureType::_2DMultisampleArray || mType == TextureType::CubeMapArray;
}

```

The Vulkan backend calls `calculateBufferInfo` with `index.usesTex3D()`, which returns true for `CubeMapArray`, and proceeds to read the full depth extent from the source buffer.

The underestimated `endByte` is used in two places that constitute real security checks. For PBO uploads, `ValidImageDataSize` verifies that the pixel unpack buffer is large enough:

```
// third_party/angle/src/libANGLE/validationES.cpp
if (pixelUnpackBuffer)
{
    CheckedNumeric<size_t> checkedEndByte(endByte);
    CheckedNumeric<size_t> checkedOffset(reinterpret_cast<size_t>(pixels));
    checkedEndByte += checkedOffset;
    if (checkedEndByte.ValueOrDie() > static_cast<size_t>(pixelUnpackBuffer->getSize()))
    {
        return false;
    }
}

```

For the `GL_ANGLE_robust_client_memory` path (used by the Chromium command buffer via `glTexSubImage3DRobustANGLE`), it checks that the caller-supplied `bufSize` covers the pixel data:

```
if (pixels != nullptr && endByte > static_cast<GLuint>(imageSize))
{
    return false;
}

```

Both checks pass with the underestimated `endByte`, but the backend reads the correct, larger amount.

In Chromium's GPU process architecture, the passthrough command buffer decoder forwards texture targets to ANGLE without independent validation. A compromised renderer can therefore send `GL_TEXTURE_CUBE_MAP_ARRAY` (`0x9009`) as the target for `TexSubImage3D`, and if the ANGLE backend supports the extension, the command reaches the vulnerable validation path in the GPU process. The `CubeMapArray` extension is not requested by default for WebGL contexts, but a compromised renderer can enable it by calling `RequestExtensionCHROMIUM("GL_EXT_texture_cube_map_array")` through the command buffer; this maps to `glRequestExtensionANGLE`, which is processed in the GPU process and enables the extension if the Vulkan device supports `imageCubeArray`.

## Reproduce

This issue was tested on Chromium commit `e6831951cd5fd2d7db105507e6f5e06ba600e073`, Ubuntu 22.04. The ANGLE Vulkan backend is required because `GL_EXT_texture_cube_map_array` must be available and the vulnerable CPU copy path is Vulkan-specific. Use `--use-angle=vulkan` on all platforms.

Check out the commit and apply the patch, which modifies `WebGL2RenderingContextBase::texSubImage3D` in the renderer process to inject `CubeMapArray` commands when it detects a sentinel PBO offset value. This simulates a compromised renderer that sends crafted GL commands through the passthrough command buffer decoder. No GPU process code is modified.

Configure an ASAN build with `out/asan/args.gn` as follows, then build:

```
is_asan = true
is_debug = false
dcheck_always_on = false

```
```
git apply patch.diff
autoninja -C out/asan chrome

```

Launch Chrome and open the PoC page:

```
out/asan/chrome --use-angle=vulkan --enable-logging=stderr --user-data-dir=./userdata poc.html

```

The PoC page creates a WebGL2 context and calls `texSubImage3D` with PBO offset `0x900900`, which the patched renderer intercepts. The renderer requests the `GL_EXT_texture_cube_map_array` extension via `RequestExtensionCHROMIUM`, creates a 1024×1024 `CubeMapArray` texture with 6 layers (`RGBA8`), and creates a ~4MB PBO (exactly `layerSize+3` bytes). It then calls `TexSubImage3D` with the `CubeMapArray` target, `depth=6`, and PBO `offset=3`. The non-aligned offset forces ANGLE's Vulkan backend into the CPU copy path. ANGLE's `ValidImageDataSize` computes `endByte` for a single layer (~4MB) instead of all 6 layers (~24MB) because it treats `CubeMapArray` as a 2D target, so the PBO size check passes. The backend then reads ~24MB from the ~4MB PBO allocation, producing a ~20MB heap-buffer-overflow.

ASAN output (Linux):

```
=================================================================
==345063==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x778695bbb000 at pc 0x5ce65edb700b bp 0x7ffcce9e7d10 sp 0x7ffcce9e74d0
READ of size 25165824 at 0x778695bbb000 thread T0 (chrome)
    #0 0x5ce65edb700a in __asan_memcpy (/home/test/Desktop/chromium/src/out/asan/chrome+0x10d2400a) (BuildId: e191f33f940a09e4)
    #1 0x77875f943833 in void angle::LoadToNative<unsigned char, 4ul>(angle::ImageLoadContext const&, unsigned long, unsigned long, unsigned long, unsigned char const*, unsigned long, unsigned long, unsigned char*, unsigned long, unsigned long) third_party/angle/src/image_util/loadimage.inc
    #2 0x77875f43484e in rx::vk::ImageHelper::stageSubresourceUpdateImpl(rx::ContextVk*, gl::ImageIndex const&, angle::Extents<int> const&, angle::Offset<int> const&, gl::InternalFormat const&, gl::PixelUnpackState const&, unsigned int, unsigned char const*, rx::vk::Format const&, rx::vk::ImageFormatSupport, unsigned int, unsigned int, unsigned int, rx::vk::ApplyImageUpdate, bool*) third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.cpp:8538:5
    #3 0x77875f2a8c34 in rx::TextureVk::setSubImageImpl(gl::Context const*, gl::ImageIndex const&, gl::Box const&, gl::InternalFormat const&, unsigned int, gl::PixelUnpackState const&, gl::Buffer*, unsigned char const*, rx::vk::Format const&) third_party/angle/src/libANGLE/renderer/vulkan/TextureVk.cpp:1310:31
    #4 0x77875f2a7b2f in rx::TextureVk::setSubImage(gl::Context const*, gl::ImageIndex const&, gl::Box const&, unsigned int, unsigned int, gl::PixelUnpackState const&, gl::Buffer*, unsigned char const*) third_party/angle/src/libANGLE/renderer/vulkan/TextureVk.cpp:616:12
    #5 0x77875f84b246 in gl::Texture::setSubImage(gl::Context*, gl::PixelUnpackState const&, gl::Buffer*, gl::TextureTarget, int, gl::Box const&, unsigned int, unsigned int, unsigned char const*) third_party/angle/src/libANGLE/Texture.cpp:1441:25
......

```
## References

- `ValidImageDataSize` `targetIs3D` check: <https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/validationES.cpp;l=1416>
- `computePackUnpackEndByte` depth logic: <https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/formatutils.cpp;l=1976>
- `ImageIndex::usesTex3D` (correct): <https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/ImageIndex.cpp;l=123>
- `TextureVk::setSubImageImpl` uses `usesTex3D`: <https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/vulkan/TextureVk.cpp;l=1261>
- Passthrough decoder `DoTexSubImage3D` (no target validation): <https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc;l=3044>

## Credit

Please use 86ac1f1587b71893ed2ad792cd7dde32 as the credit for this vulnerability. Thank you.

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 16.4 KB)
- [patch.diff](attachments/patch.diff) (text/x-diff, 2.5 KB)
- [poc.html](attachments/poc.html) (text/html, 1.6 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6358531242491904.

### sk...@google.com (2026-03-23)

Cannot reproduce. Setting provisional FoundIn/Severity and assigning to reviewer of commit from the link in the bug

### ch...@google.com (2026-03-24)

Setting milestone because of s2 severity.

### sy...@chromium.org (2026-03-26)

@Amirali, would you mind taking a quick look at this? Looks like a simple oversight in validation:

> ```
> // third_party/angle/src/libANGLE/validationES.cpp
> bool targetIs3D = texType == TextureType::_3D || texType == TextureType::_2DArray;
> 
> ```
> 
> This variable is missing TextureType::CubeMapArray

### ab...@google.com (2026-04-01)

Hello,

Sure. I will check it out.

### dx...@google.com (2026-04-14)

Project: angle/angle  

Branch:  main  

Author:  Amirali Abdolrashidi [abdolrashidi@google.com](mailto:abdolrashidi@google.com)  

Link:    <https://chromium-review.googlesource.com/7749968>

Check depth for cube map arrays in size validation

---


Expand for full commit details
```
     
    * Updated ValidImageDataSize() so cube map arrays are also regarded as 
      3D targets, so their depth is also taken into account when checking 
      their size. 
      * (Otherwise, it can lead to memory access errors or VVLs such as 
        VUID-vkCmdCopyBufferToImage-pRegions-00171.) 
     
    * Added the test: ValidateCubeMapArrayCopyExceedsPBOSize. 
      * It attempts to copy to a cube map array from a PBO with a smaller 
        size. It is expected that the glTexSubImage3D() call fails with 
        GL_INVALID_OPERATION. 
     
    Bug: chromium:494823889 
    Change-Id: I0927d1bfa4cc75c6a26cde442f2ffc95212aaa13 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7749968 
    Commit-Queue: Amirali Abdolrashidi <abdolrashidi@google.com> 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Reviewed-by: Charlie Lao <cclao@google.com>

```

---

Files:

- M `src/libANGLE/validationES.cpp`
- M `src/tests/gl_tests/TextureTest.cpp`

---

Hash: [c83175b85bf991ff2ef05073496c50c9ebfc569d](https://chromiumdash.appspot.com/commit/c83175b85bf991ff2ef05073496c50c9ebfc569d)  

Date: Sat Apr 11 00:05:02 2026


---

### dx...@google.com (2026-04-15)

Project: chromium/src  

Branch:  main  

Author:  [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com) [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7763362>

Roll ANGLE from 7217eaf9834a to c83175b85bf9 (1 revision)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/7217eaf9834a..c83175b85bf9 
     
    2026-04-14 abdolrashidi@google.com Check depth for cube map arrays in size validation 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/angle-chromium-autoroll 
    Please CC angle-team@google.com,solti@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:494823889 
    Tbr: solti@google.com 
    Change-Id: I4ff0926341d0dfb64d806e0c20e64e6e45cc95b8 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7763362 
    Commit-Queue: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1614823}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [31647f01e44f6491beb34290192286b9d6c47c2c](https://chromiumdash.appspot.com/commit/31647f01e44f6491beb34290192286b9d6c47c2c)  

Date: Wed Apr 15 00:39:24 2026


---

### sp...@google.com (2026-06-29)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Out of bounds read with bisect


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/494823889)*
