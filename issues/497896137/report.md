# Integer overflow in ANGLE D3D11 compressed 3D texture deferred-init leads to heap OOB read in GPU process

| Field | Value |
|-------|-------|
| **Issue ID** | [497896137](https://issues.chromium.org/issues/497896137) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | se...@gmail.com |
| **Assignee** | sh...@google.com |
| **Created** | 2026-03-30 |
| **Bounty** | $3,000.00 |

## Description

## Summary

The ANGLE D3D11 backend computes the zero-fill buffer size for block-compressed 3D textures using an unchecked 32-bit multiplication that does not account for block height, producing a value four times larger than the actual compressed image size. For sufficiently large textures the product wraps around in a GLuint, and the subsequent LoadCompressedToNative memcpy reads the correct (larger) number of bytes from the undersized buffer. Any WebGL2 page can trigger this through standard API calls (texStorage3D followed by a partial compressedTexSubImage3D), causing a heap-buffer-overflow read in the GPU process with no source modifications required. Platform: Windows (D3D11 ANGLE backend). Any GPU with BPTC (BC6H/BC7) support, which is standard on all Direct3D 11 hardware.

## Bisect

Introducing Commit: `05b35b210ef3dcdf7e3260d192ce51b602b6f3a7` (ANGLE repo)

- Date: 2017-10-03
- Author: Jamie Madill ([jmadill@chromium.org](mailto:jmadill@chromium.org))

This commit introduced TextureD3D::initializeContents with the slow-path zero-fill logic. The function computes imageBytes as `computeRowPitch(...) * height * depth`, which for block-compressed formats treats height as a pixel count rather than a block count, inflating the result by blockHeight (4 for BPTC). The computation has been present in every subsequent revision of this function.

## Root Cause

When a compressed 3D texture has deferred initialization pending and the fast render-target-clear path is unavailable (which is always the case for block-compressed formats since they have no renderable format), TextureD3D::initializeContents falls through to a slow path that allocates a zero-filled buffer and loads it into the texture through the normal compressed data upload path.

The slow path computes the buffer size as follows:

```
// third_party/angle/src/libANGLE/renderer/d3d/TextureD3D.cpp
GLuint imageBytes = 0;
ANGLE_CHECK_GL_MATH(contextD3D, formatInfo.computeRowPitch(formatInfo.type, image->getWidth(),
                                                           1, 0, &imageBytes));
imageBytes *= image->getHeight() * image->getDepth();

```

For BPTC (4x4 blocks, 16 bytes per block), `computeRowPitch` correctly returns `(width / 4) * 16`. However, the subsequent multiplication uses the raw pixel height rather than the block-row count `height / 4`. The result is exactly four times larger than the true compressed image size. The multiplication is performed in `GLuint` (32-bit unsigned) arithmetic with no overflow check.

The validation layer in `ValidateCompressedTexImage3D` computes the correct compressed size through `computeCompressedImageSize`, which properly divides by `blockHeight`. The two computations therefore disagree on image size for any 3D compressed texture.

For a 2048x2048x320 BPTC texture, the correct compressed size is `512 * 512 * 320 * 16 = 1,342,177,280` bytes. The `initializeContents` formula produces `8192 * 2048 * 320 = 5,368,709,120`, which wraps to `1,073,741,824` in `GLuint`. `Context::getZeroFilledBuffer` allocates this smaller buffer. `Image11::loadData` then recomputes the correct `inputImageSize` and issues a `memcpy` of that length from the undersized source, reading past the end of the allocation.

The deferred-init state is reached through standard WebGL2 API usage. Calling `texStorage3D` with a compressed internal format allocates immutable storage and marks all levels as `MayNeedInit` under robust resource initialization. A subsequent `compressedTexSubImage3D` on a small sub-region triggers `ensureSubImageInitialized`, which calls `initializeContents` for the entire mip level. The BPTC format on D3D11 has `texFormat` set to a valid DXGI format but `rtvFormat` set to `DXGI_FORMAT_UNKNOWN`, ensuring the fast clear path is never taken and the vulnerable slow path is always exercised.

## Reproduce

This issue was tested on Chromium commit `cd400b8c25335a1e2a8f3676367a21b1c82e1df1` running on Windows 11 with an NVIDIA GeForce RTX 4060 Ti. The bug is in the ANGLE D3D11 backend and requires only the default Windows GPU configuration with BPTC (BC6H/BC7) texture compression support, which is standard on all Direct3D 11 hardware. No source modifications are required to reproduce.

Configure an ASAN build with the following args.gn in `out/asan`, then build.

```
is_asan = true
is_debug = false
dcheck_always_on = false
target_cpu = "x64"

```
```
autoninja -C out/asan chrome

```

Launch Chrome and open the PoC page(`poc.html` uses absolute path).

```
$ out\asan\chrome.exe --user-data-dir=/tmp/poc /path/to/poc.html 2>/tmp/asan.txt
$ cat /tmp/asan.txt

```

The PoC page creates a WebGL2 context, obtains the `EXT_texture_compression_bptc` extension, and calls `texStorage3D` with `GL_TEXTURE_3D`, `COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT_EXT`, and dimensions 2048x2048x320. This allocates immutable compressed storage with all levels marked for deferred initialization. A subsequent `compressedTexSubImage3D` on a 4x4x1 sub-region triggers `ensureSubImageInitialized`, which calls `TextureD3D::initializeContents`. The overflowing size formula causes allocation of an undersized buffer, and the subsequent `memcpy` reads past its end. The GPU process crashes with a heap-buffer-overflow reported by AddressSanitizer.

AddressSanitizer reports the following in the GPU process:

```
=================================================================
==23284==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x12b328cb1800 at pc 0x7ffaa14db36c bp 0x00b7e95fd4a0 sp 0x00b7e95fd4e8
READ of size 1342177280 at 0x12b328cb1800 thread T0
==23284==*** WARNING: Failed to initialize DbgHelp!              ***
==23284==*** Most likely this means that the app is already      ***
==23284==*** using DbgHelp, possibly with incompatible flags.    ***
==23284==*** Due to technical reasons, symbolization might crash ***
==23284==*** or produce wrong results.                           ***
    #0 0x7ffaa14db36b in _asan_memcpy+0x25b (D:\src\chromium\src\out\asan\clang_rt.asan_dynamic-x86_64.dll+0x18004b36b)
    #1 0x7ffa968870f3 in angle::LoadCompressedToNative<4,4,1,16> D:\src\chromium\src\third_party\angle\src\image_util\loadimage.inc:389
    #2 0x7ffa9696efb4 in rx::Image11::loadData D:\src\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Image11.cpp:308
    #3 0x7ffa96aa7be1 in rx::TextureD3D::initializeContents D:\src\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp:968
    #4 0x7ffa9668789c in gl::FramebufferAttachmentObject::initializeContents D:\src\chromium\src\third_party\angle\src\libANGLE\FramebufferAttachment.cpp:365
    #5 0x7ffa967a52e8 in gl::Texture::setCompressedSubImage D:\src\chromium\src\third_party\angle\src\libANGLE\Texture.cpp:1494
    #6 0x7ffa96611e67 in gl::Context::compressedTexSubImage3D D:\src\chromium\src\third_party\angle\src\libANGLE\Context.cpp:5804
......

```

The full ASAN log is provided in `asan.txt`.

## References

- [TextureD3D::initializeContents slow-path size computation](https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/d3d/TextureD3D.cpp;l=949-952)
- [ValidateCompressedTexImage3D correct size computation](https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/validationES3.cpp;l=1889)
- [LoadCompressedToNative memcpy with correct size](https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/image_util/loadimage.inc;l=389)
- [Image11::loadData computing correct inputDepthPitch](https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/d3d/d3d11/Image11.cpp;l=308)

## Credit

Please use 86ac1f1587b71893ed2ad792cd7dde32 as the credit for this vulnerability. Thank you.

## Attachments

- [poc.html](attachments/poc.html) (text/html, 1.1 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 13.9 KB)

## Timeline

### xi...@chromium.org (2026-03-31)

shrekshao@: Could you PTAL? Unfortunately I don't have a Windows setup to test the patch. Thanks.

Setting tentative severity and foundin labels.

### ch...@google.com (2026-03-31)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-31)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-04-09)

Project: angle/angle  

Branch:  main  

Author:  Shrek Shao [shrekshao@google.com](mailto:shrekshao@google.com)  

Link:    <https://chromium-review.googlesource.com/7728091>

D3D11: Fix overflow in compressed 3D texture deferred-init

---


Expand for full commit details
```
     
    The ANGLE D3D11 backend computed the zero-fill buffer size for 
    block-compressed 3D textures using an unchecked 
    32-bit multiplication that did not account for block height. 
    This produced a value four times larger than the actual 
    compressed image size and could overflow for sufficiently large 
    textures. 
     
    This fix: 
    1. Uses InternalFormat::computeCompressedImageSize to correctly 
    calculate the required buffer size for compressed textures, 
    taking block dimensions into account. 
    2. Employs angle::CheckedNumeric for uncompressed texture size 
    calculations to prevent potential integer overflows. 
    3. Adds a regression test DeferredInit3DOverflow 
    that uses large texture dimensions (2048x2048x320) to verify 
    there is no ASAN error. 
     
    Bug: b/497896137 
    Change-Id: I76f0fb008af34e8ac78870318e608d16ed4ddd93 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7728091 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org> 
    Auto-Submit: Shrek Shao <shrekshao@google.com>

```

---

Files:

- M `src/libANGLE/renderer/d3d/TextureD3D.cpp`
- M `src/tests/gl_tests/BPTCCompressedTextureTest.cpp`

---

Hash: [838c9be2bc21df9ab804428d53bf61fa906be4b4](https://chromiumdash.appspot.com/commit/838c9be2bc21df9ab804428d53bf61fa906be4b4)  

Date: Thu Apr 2 22:41:06 2026


---

### ch...@google.com (2026-04-10)

This is sufficiently serious that it should be merged to M146. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M146. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

This is sufficiently serious that it should be merged to M147. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M147. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to M148. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M148. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

### ch...@google.com (2026-04-10)

**M146** merge request created. **Please update [crbug/501314630](https://crbug.com/501314630) to have this merge reviewed.**

### ch...@google.com (2026-04-10)

**M147** merge request created. **Please update [crbug/501314239](https://crbug.com/501314239) to have this merge reviewed.**

### ch...@google.com (2026-04-10)

**M148** merge request created. **Please update [crbug/501314162](https://crbug.com/501314162) to have this merge reviewed.**

### sh...@google.com (2026-04-10)

Pitfall: I didn't add me to the cc list of [crbug/501314162](https://crbug.com/501314162) before assigning to [merges@chromium.org](mailto:merges@chromium.org). So I lost access (facepalm). Can someone help adding me to the cc list of [crbug/501314162](https://crbug.com/501314162)? Thanks

### sh...@google.com (2026-04-10)

NVM. [merges@chromium.org](mailto:merges@chromium.org) reassign to me

### aj...@google.com (2026-04-22)

Sev=Medium as only a READ seems possible.

### dx...@google.com (2026-04-22)

Project: angle/angle  

Branch:  chromium/7778  

Author:  Shrek Shao [shrekshao@google.com](mailto:shrekshao@google.com)  

Link:    <https://chromium-review.googlesource.com/7782839>

D3D11: Fix overflow in compressed 3D texture deferred-init

---


Expand for full commit details
```
     
    The ANGLE D3D11 backend computed the zero-fill buffer size for 
    block-compressed 3D textures using an unchecked 
    32-bit multiplication that did not account for block height. 
    This produced a value four times larger than the actual 
    compressed image size and could overflow for sufficiently large 
    textures. 
     
    This fix: 
    1. Uses InternalFormat::computeCompressedImageSize to correctly 
    calculate the required buffer size for compressed textures, 
    taking block dimensions into account. 
    2. Employs angle::CheckedNumeric for uncompressed texture size 
    calculations to prevent potential integer overflows. 
    3. Adds a regression test DeferredInit3DOverflow 
    that uses large texture dimensions (2048x2048x320) to verify 
    there is no ASAN error. 
     
    Bug: b/497896137 
    Fixed: b/501314162 
    Change-Id: I76f0fb008af34e8ac78870318e608d16ed4ddd93 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7728091 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org> 
    Auto-Submit: Shrek Shao <shrekshao@google.com> 
    (cherry picked from commit 838c9be2bc21df9ab804428d53bf61fa906be4b4) 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7782839 
    Reviewed-by: Geoff Lang <geofflang@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/d3d/TextureD3D.cpp`
- M `src/tests/gl_tests/BPTCCompressedTextureTest.cpp`

---

Hash: [978e5e9095e77a9f60804a01247a7afbebe9aa5c](https://chromiumdash.appspot.com/commit/978e5e9095e77a9f60804a01247a7afbebe9aa5c)  

Date: Thu Apr 2 22:41:06 2026


---

### dx...@google.com (2026-04-22)

2 changes merged

---

Project: angle/angle  

Branch:  chromium/7727  

Author:  Shrek Shao [shrekshao@google.com](mailto:shrekshao@google.com)  

Link:    <https://chromium-review.googlesource.com/7782840>

D3D11: Fix overflow in compressed 3D texture deferred-init

---


Expand for full commit details
```
     
    The ANGLE D3D11 backend computed the zero-fill buffer size for 
    block-compressed 3D textures using an unchecked 
    32-bit multiplication that did not account for block height. 
    This produced a value four times larger than the actual 
    compressed image size and could overflow for sufficiently large 
    textures. 
     
    This fix: 
    1. Uses InternalFormat::computeCompressedImageSize to correctly 
    calculate the required buffer size for compressed textures, 
    taking block dimensions into account. 
    2. Employs angle::CheckedNumeric for uncompressed texture size 
    calculations to prevent potential integer overflows. 
    3. Adds a regression test DeferredInit3DOverflow 
    that uses large texture dimensions (2048x2048x320) to verify 
    there is no ASAN error. 
     
    Bug: b/497896137 
    Fixed: b/501314239 
    Change-Id: I76f0fb008af34e8ac78870318e608d16ed4ddd93 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7728091 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org> 
    Auto-Submit: Shrek Shao <shrekshao@google.com> 
    (cherry picked from commit 838c9be2bc21df9ab804428d53bf61fa906be4b4) 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7782840 
    Reviewed-by: Geoff Lang <geofflang@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/d3d/TextureD3D.cpp`
- M `src/tests/gl_tests/BPTCCompressedTextureTest.cpp`

---

Hash: [8b2a75086a3b09c1fc3bce02464910bb0cc67937](https://chromiumdash.appspot.com/commit/8b2a75086a3b09c1fc3bce02464910bb0cc67937)  

Date: Thu Apr 2 22:41:06 2026


---


---

Project: angle/angle  

Branch:  chromium/7680  

Author:  Shrek Shao [shrekshao@google.com](mailto:shrekshao@google.com)  

Link:    <https://chromium-review.googlesource.com/7783400>

D3D11: Fix overflow in compressed 3D texture deferred-init

---


Expand for full commit details
```
     
    The ANGLE D3D11 backend computed the zero-fill buffer size for 
    block-compressed 3D textures using an unchecked 
    32-bit multiplication that did not account for block height. 
    This produced a value four times larger than the actual 
    compressed image size and could overflow for sufficiently large 
    textures. 
     
    This fix: 
    1. Uses InternalFormat::computeCompressedImageSize to correctly 
    calculate the required buffer size for compressed textures, 
    taking block dimensions into account. 
    2. Employs angle::CheckedNumeric for uncompressed texture size 
    calculations to prevent potential integer overflows. 
    3. Adds a regression test DeferredInit3DOverflow 
    that uses large texture dimensions (2048x2048x320) to verify 
    there is no ASAN error. 
     
    Bug: b/497896137 
    Fixed: b/501314630 
    Change-Id: I76f0fb008af34e8ac78870318e608d16ed4ddd93 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7728091 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org> 
    Auto-Submit: Shrek Shao <shrekshao@google.com> 
    (cherry picked from commit 838c9be2bc21df9ab804428d53bf61fa906be4b4) 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7783400 
    Reviewed-by: Geoff Lang <geofflang@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/d3d/TextureD3D.cpp`
- M `src/tests/gl_tests/BPTCCompressedTextureTest.cpp`

---

Hash: [5141d2393c8495286cfa8823c7f664e2b6780286](https://chromiumdash.appspot.com/commit/5141d2393c8495286cfa8823c7f664e2b6780286)  

Date: Thu Apr 2 22:41:06 2026


---

### sp...@google.com (2026-04-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
User information disclosure with Bisect


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/497896137)*
