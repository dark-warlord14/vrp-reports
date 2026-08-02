# Arbitrary Memory Read and Write in ANGLE GL Backend via PBO Desync

| Field | Value |
|-------|-------|
| **Issue ID** | [498904293](https://issues.chromium.org/issues/498904293) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2026-04-02 |
| **Bounty** | $97,000.00 |

## Description

# VULNERABILITY DETAILS

A severe state desynchronization vulnerability exists in the ANGLE OpenGL backend (`CopySubTextureCHROMIUM`), leading to Arbitrary R/W in the GPU process.

The root cause resides in `BlitGL::copySubTextureCPUReadback`. When performing a CPU fallback copy, the code explicitly unbinds the `PIXEL_PACK_BUFFER` mappings through the GL backend `StateManagerGL` using `setPixelPackBuffer(context, nullptr)` [0]. An identical mechanism unbinds the `PIXEL_UNPACK_BUFFER` via `setPixelUnpackBuffer` [1].

```
    gl::PixelPackState pack;
    pack.alignment = 1;
    ANGLE_TRY(mStateManager->setPixelPackState(context, pack));
    ANGLE_TRY(mStateManager->setPixelPackBuffer(context, nullptr)); // [0]

    // ...
    gl::PixelUnpackState unpack;
    unpack.alignment = 1;
    ANGLE_TRY(mStateManager->setPixelUnpackState(context, unpack));
    ANGLE_TRY(mStateManager->setPixelUnpackBuffer(context, nullptr)); // [1]

```

These functions effectively propagate the `glBindBuffer` command directly to the native GPU driver via `StateManagerGL::bindBuffer` [2].

```
angle::Result StateManagerGL::setPixelUnpackBuffer(const gl::Context *context,
                                                   const gl::Buffer *pixelBuffer)
{
    GLuint bufferID = 0;
    if (pixelBuffer != nullptr)
    {
        bufferID = GetImplAs<BufferGL>(pixelBuffer)->getBufferID();
    }
    bindBuffer(gl::BufferBinding::PixelUnpack, bufferID); // [2]

    return angle::Result::Continue;
}

```

However, they silently bypass the ANGLE frontend tracking system (`gl::State`). Crucially, the frontend's dirty bits (such as `DIRTY_BIT_UNPACK_BUFFER_BINDING`) are never set.

Because the frontend `gl::State` tracking and the native OpenGL driver state become desynchronized, the underlying native GL driver lacks the PBO binding (it was set to `0`), while the frontend continues to believe the PBO is actively bound. When a subsequent API call takes an offset, the native driver treats the user-supplied `offset` as a raw CPU/Host pointer, enabling arbitrary memory operations.

[0] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/gl/BlitGL.cpp;drc=a76e73df11cbb5466e8a1c8b3c9c04ce4a981f7b;l=865>

[1] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/gl/BlitGL.cpp;drc=a76e73df11cbb5466e8a1c8b3c9c04ce4a981f7b;l=883>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/gl/StateManagerGL.cpp;drc=a76e73df11cbb5466e8a1c8b3c9c04ce4a981f7b;l=642>

## Vulnerability Exploit

The PoC leverages the desynchronization bug to transform a PBO offset into an arbitrary memory pointer. The process relies on intentionally triggering a CPU fallback path (e.g., via `copyTextureCHROMIUM`), which silently unbinds the `PIXEL_PACK_BUFFER` in the native OpenGL driver while the ANGLE frontend state remains intact.

Steps to achieve an arbitrary write:

1. Desynchronize the `PIXEL_PACK_BUFFER` state.
2. Manipulate the frontend state system (e.g., via dummy `readPixels` calls) to clear dirty bits, preventing the buffer from re-binding to the driver.
3. Call `readPixels` using a controlled integer (e.g. `0x41414141`) as the `offset`.
4. Since the native OpenGL driver considers the PBO unbound (id = 0), it interprets the `offset` as an absolute virtual memory pointer, writing pixel data directly to this address.

The arbitrary read is achieved via a similar state desynchronization for `PIXEL_UNPACK_BUFFER` during operations like `texSubImage2D`.

### Arbitrary Write Crash Site

```
Thread 1 "chrome" received signal SIGSEGV, Segmentation fault.
__memcpy_avx_unaligned_erms ()
    at ../sysdeps/x86_64/multiarch/memmove-vec-unaligned-erms.S:271
warning: 271	../sysdeps/x86_64/multiarch/memmove-vec-unaligned-erms.S: No such file or directory
(gdb) x/i $pc
=> 0x7f264e788aa1 <__memcpy_avx_unaligned_erms+33>:	vmovdqu %ymm0,(%rdi)
(gdb) i r rdi
rdi            0x41414141          1094795585
(gdb) i r ymm0
ymm0           {v16_bfloat16 = {0x4242 <repeats 16 times>}, v16_half = {0x4242 <repeats 16 times>}, v8_float = {0x42424242, 0x42424242, 0x42424242, 0x42424242, 0x42424242, 0x42424242, 0x42424242, 0x42424242}, v4_double = {0x4242424242424242, 0x4242424242424242, 0x4242424242424242, 0x4242424242424242}, v32_int8 = {0x42 <repeats 32 times>}, v16_int16 = {0x4242 <repeats 16 times>}, v8_int32 = {0x42424242, 0x42424242, 0x42424242, 0x42424242, 0x42424242, 0x42424242, 0x42424242, 0x42424242}, v4_int64 = {0x4242424242424242, 0x4242424242424242, 0x4242424242424242, 0x4242424242424242}, v2_int128 = {0x42424242424242424242424242424242, 0x42424242424242424242424242424242}}
(gdb) bt
#0  __memcpy_avx_unaligned_erms ()
    at ../sysdeps/x86_64/multiarch/memmove-vec-unaligned-erms.S:271
#1  0x000056c2930d7edc in __interceptor_memcpy ()
#2  0x00007b221f1b443e in ??? ()
    at /lib/x86_64-linux-gnu/libgallium-25.2.8-0ubuntu0.24.04.1.so
#3  0x00007b221f20cc9b in ??? ()
    at /lib/x86_64-linux-gnu/libgallium-25.2.8-0ubuntu0.24.04.1.so
#4  0x00007b221f1b4d3a in ??? ()
    at /lib/x86_64-linux-gnu/libgallium-25.2.8-0ubuntu0.24.04.1.so
#5  0x00007b221f1b50d5 in ??? ()
    at /lib/x86_64-linux-gnu/libgallium-25.2.8-0ubuntu0.24.04.1.so
#6  0x00007b2241cca380 in readPixelsAllAtOnce ()
    at ../../third_party/angle/src/libANGLE/renderer/gl/FramebufferGL.cpp:1684
#7  0x00007b2241cc9442 in readPixels ()
    at ../../third_party/angle/src/libANGLE/renderer/gl/FramebufferGL.cpp:816
// ...

```
# BISECTION

Introduced by ANGLE upstream commit [0] which added the CPU fallback implementation for `CopyTextureCHROMIUM` on OpenGL but failed to safely track buffer unbindings within the frontend state.

This regression was rolled into Chromium in commit [1].

[0] <https://chromium.googlesource.com/angle/angle/+/aadc8f376a2c797db98d69d308c9980ca818f57f> (Implement the CPU fallback for CopyTextureCHROMIUM on OpenGL)

[1] <https://chromium.googlesource.com/chromium/src/+/236105a6afc95bfab50b0a3e3487c85cc049b49c> (Roll ANGLE 79f7104..92996b0)

# VERSION

Chrome Version: HEAD

Operating System: Linux

# REPRODUCTION CASE

1. Apply renderer.patch and build Chromium with ASan.
2. Host the `poc.html` on an HTTP server.
3. Run Chrome against the PoC.

```
$ python3 -m http.server 8000
$ ./out/asan/chrome "http://localhost:8000/poc.html"

```
# CRASH INFORMATION

Type of crash: GPU process

Crash log: Attached `asan_read.txt` (Arbitrary Read) and `asan_write.txt` (Arbitrary Write).

# CREDIT INFORMATION

Reporter credit: Anonymous

## Attachments

- [poc.html](attachments/poc.html) (text/html, 2.5 KB)
- [renderer.patch](attachments/renderer.patch) (text/x-diff, 6.5 KB)
- [asan_read.txt](attachments/asan_read.txt) (text/plain, 10.5 KB)
- [asan_write.txt](attachments/asan_write.txt) (text/plain, 11.0 KB)
- [pure_js_poc.html](attachments/pure_js_poc.html) (text/html, 5.2 KB)
- [asan_pure_js_read.txt](attachments/asan_pure_js_read.txt) (text/plain, 11.1 KB)
- [asan_pure_js_write.txt](attachments/asan_pure_js_write.txt) (text/plain, 10.6 KB)

## Timeline

### [Deleted User] (2026-04-03)

geofflang: This might be a dupe of [crbug.com/490170083](https://crbug.com/490170083)

### ki...@gmail.com (2026-04-03)

I've looked into the patch for [issue 490170083](https://issues.chromium.org/issues/490170083) ([CL 7708753](https://chromium-review.googlesource.com/c/angle/angle/+/7708753)). Assuming this is the correct commit, I don't think these two issues are duplicates.

That patch appears to only adjust the unbinding order to fix a local state issue. However, it still unbinds the PBO via mStateManager without updating the Frontend's DIRTY\_BIT. In my view, this leads to a state desync where the underlying PBO is 0, but the Frontend still considers it bound.

For reference, the HEAD(ANGLE commit: 07f101fbae2d8cbef53d67a2a805de9ea2154214) of my local reproduction environment already includes this patch.

### ch...@google.com (2026-04-03)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-03)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### ki...@gmail.com (2026-04-05)

Two updates after further investigation:

1. The desynchronization defect (unbinding native PBOs without updating frontend `DIRTY_BIT` tracking) is not limited to `copySubTextureCPUReadback`. It also affects other internal pathways like `BlitGL::generateMipmap` and `TextureGL::allocateMipmapLevelsForGeneration`.
2. This vulnerability does **not** require a compromised renderer. It can be triggered using pure JS:
   
   - Arbitrary Read: Triggered via `gl.generateMipmap()` on an `SRGB8_ALPHA8` texture.
   - Arbitrary Write: Triggered via `gl.texImage2D` mapping an `HTMLCanvasElement` to `LUMINANCE`, hitting the `copySubTextureCPUReadback` fallback.

Attached `pure_js_poc.html` and two ASan logs.

### ki...@gmail.com (2026-04-17)

I can still reproduce this on the latest build. Any progress on this?

### pe...@google.com (2026-04-17)

Common #6 suggests this should be a s0 not a s1.

### pe...@google.com (2026-04-17)

The GPU process crashes with SIGSEGV when I run locally on my glinux intel with the POC in [comment #7](https://issues.chromium.org/issues/498904293#comment7).

### dx...@google.com (2026-04-21)

Project: angle/angle  

Branch:  main  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7774027>

GL: Mark StateManagerGL internal buffer state dirty on bind

---


Expand for full commit details
```
     
    When changing state, StateManagerGL would set local dirty bits which 
    would be synchronized on the next syncState by ORing them with the 
    frontend dirty bits. This was not done for internal buffer binding 
    changes and allowed for incorrect pixel buffers to be bound on 
    ReadPixels or TexImage calls. 
     
    Fixed: chromium:498904293 
    Fixed: chromium:503768143 
    Change-Id: I42f5acfdb709f327205f0f8cc04c3f11f1bd2b79 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7774027 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/gl/StateManagerGL.cpp`
- M `src/libANGLE/renderer/gl/StateManagerGL.h`
- M `src/tests/angle_end2end_tests_expectations.txt`
- M `src/tests/capture_replay_tests/capture_replay_expectations.txt`
- M `src/tests/gl_tests/CopyTextureTest.cpp`

---

Hash: [1c82f3a0bd18d2046fa38ccffffbcc45891f0301](https://chromiumdash.appspot.com/commit/1c82f3a0bd18d2046fa38ccffffbcc45891f0301)  

Date: Fri Apr 17 22:03:58 2026


---

### dx...@google.com (2026-04-27)

Project: angle/angle  

Branch:  main  

Author:  Yuly Novikov [ynovikov@chromium.org](mailto:ynovikov@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7789607>

Skip CopyTextureTestES3.PBOSynchronization on Pixel10 GLES

---


Expand for full commit details
```
     
    New test added in crrev.com/c/7774027. 
    Fails in glTexSubImage2D: 
    format or type is not an accepted constant(GL_INVALID_ENUM) 
     
    Bug: chromium:498904293 
    Change-Id: I415130cd4da028ac31f008fe2a1e35d38e2713e1 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7789607 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Yuly Novikov <ynovikov@chromium.org>

```

---

Files:

- M `src/tests/angle_end2end_tests_expectations.txt`

---

Hash: [dd68975ff32c4c9d837a972349f7974faa08962c](https://chromiumdash.appspot.com/commit/dd68975ff32c4c9d837a972349f7974faa08962c)  

Date: Fri Apr 24 17:22:33 2026


---

### dx...@google.com (2026-04-27)

Project: chromium/src  

Branch:  main  

Author:  [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com) [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7797960>

Roll ANGLE from 7f1d7f4b5a0c to d5d76f88af19 (5 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/7f1d7f4b5a0c..d5d76f88af19 
     
    2026-04-27 ynovikov@chromium.org Stop end2end testing with D3D9 and WebGPU backends on Win Intel 
    2026-04-27 a.annestrand@samsung.com OpenCL: fix default and all device type handling 
    2026-04-27 syoussefi@chromium.org Initialize textures during syncState 
    2026-04-27 ynovikov@chromium.org Skip TextureFormatCompatChromiumNoStorageFd on Pixel 10 Vulkan 
    2026-04-27 ynovikov@chromium.org Skip CopyTextureTestES3.PBOSynchronization on Pixel10 GLES 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/angle-chromium-autoroll 
    Please CC angle-team@google.com,cnorthrop@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:40874754,chromium:497637277,chromium:498904293,chromium:501584689,chromium:506180945 
    Tbr: cnorthrop@google.com 
    Change-Id: I8be994170f9ce3cda9be96b8ba64c68d48ec62eb 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7797960 
    Commit-Queue: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1621405}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [b03c1855e7cb27606156906fe32685b906bbcedf](https://chromiumdash.appspot.com/commit/b03c1855e7cb27606156906fe32685b906bbcedf)  

Date: Mon Apr 27 23:19:01 2026


---

### sp...@google.com (2026-05-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $97000.00 for this report.

Rationale for this decision:
Controlled write, gpu, renderer and on Android


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-20)

Requesting merge to M148 because latest trunk commit is in 149.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

### ch...@google.com (2026-05-20)

**M148** merge request created. **Please update [crbug/514925125](https://crbug.com/514925125) to have this merge reviewed.**

### ch...@google.com (2026-07-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/498904293)*
