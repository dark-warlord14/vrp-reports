# OOB Read in ANGLE Metal Backend During Block-Compressed PBO Texture Upload Crashes GPU Process on Mac

| Field | Value |
|-------|-------|
| **Issue ID** | [489579953](https://issues.chromium.org/issues/489579953) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebGL |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | kb...@chromium.org |
| **Created** | 2026-03-04 |
| **Bounty** | $3,000.00 |

## Description

# OOB Read in ANGLE Metal Backend During Block-Compressed PBO Texture Upload Crashes GPU Process on Mac

## Summary

The ANGLE Metal backend miscomputes the destination row pitch when uploading block-compressed texture data through a Pixel Buffer Object with a non-block-aligned offset. The function `convertAndSetPerSliceSubImage` in TextureMtl.mm calculates `dstRowPitch` as `pixelBytes * width`, treating `pixelBytes` as a per-pixel value, but for block-compressed formats this field holds the byte size of an entire compressed block. The resulting row pitch is inflated by a factor of the block width (typically 4x), and when passed to Metal's `replaceRegion`, it causes the GPU process to read far past the end of the source buffer. On macOS with Apple Silicon and ETC2 textures, a 512x512 upload produces a ~384 KB out-of-bounds read that crosses page boundaries and kills the GPU process with SIGSEGV. This is reachable from a sandboxed renderer via a plain WebGL2 page with no special flags or permissions.

Platform: macOS (Apple Silicon with native ETC2/ASTC support, macOS 11.0 or later).

## Bisect

Introducing Commit: `d33a22228ee2999ab5e2d2eda4d405c5768555d2`

- Date: Mon Apr 26 16:56:15 2021 -0700
- Author: Kyle Piddington [kpiddington@apple.com](mailto:kpiddington@apple.com)
- Review: <https://chromium-review.googlesource.com/c/angle/angle/+/2950067>

## Root Cause

When a WebGL2 page calls `compressedTexSubImage2D` with a bound `PIXEL_UNPACK_BUFFER`, the data offset encoded in the `pixels` parameter reaches `TextureMtl::setPerSliceSubImage`. If that offset is not evenly divisible by the format's `pixelBytes`, the function falls through to `convertAndSetPerSliceSubImage`:

```
// TextureMtl.mm — setPerSliceSubImage
uintptr_t offset = reinterpret_cast<uintptr_t>(pixels);
if (offset % imageFormat.actualAngleFormat().pixelBytes || pixelsRowPitch < minRowPitch)
{
    return convertAndSetPerSliceSubImage(/* ... */, unpackBuffer, pixels, imageDef);
}

```

ANGLE's ES3 validation intentionally skips the PBO offset alignment check for compressed formats, so an offset of 1 passes validation and always satisfies the modulus condition above for any format with `pixelBytes > 1`.

Inside `convertAndSetPerSliceSubImage`, when an unpack buffer is present and the format is block-compressed, the function obtains a CPU pointer to the buffer's shadow copy and recurses with `unpackBuffer` set to null:

```
// TextureMtl.mm — convertAndSetPerSliceSubImage, unpackBuffer branch
if (imageFormat.intendedAngleFormat().isBlock || /* ... */)
{
    const uint8_t *clientData = unpackBufferMtl->getBufferDataReadOnly(contextMtl);
    clientData += offset;
    ANGLE_TRY(convertAndSetPerSliceSubImage(
        context, slice, mtlArea, internalFormat, type, pixelsAngleFormat,
        pixelsRowPitch, pixelsDepthPitch, nullptr, clientData, imageDef));
}

```

The recursive call enters the `unpackBuffer == nullptr` branch, which computes the destination row pitch and dispatches based on whether the compressed format is natively supported:

```
// TextureMtl.mm — convertAndSetPerSliceSubImage, else (no unpackBuffer)
const angle::Format &dstFormat = angle::Format::Get(imageFormat.actualFormatId);
const size_t dstRowPitch       = dstFormat.pixelBytes * mtlArea.size.width;

```

For uncompressed formats, `pixelBytes` is the number of bytes per pixel, so multiplying by the pixel width gives the correct row pitch. For block-compressed formats, however, `pixelBytes` holds the number of bytes per compressed block (8 for ETC2\_RGB8, 16 for ASTC 4x4), while `mtlArea.size.width` is still the width in pixels. The product is therefore `blockWidth` times too large. For a 512x512 ETC2\_RGB8 texture with 4x4 blocks, the correct row pitch is 128 blocks times 8 bytes = 1024, but the code computes 8 times 512 = 4096.

When the intended and actual format IDs match, meaning Metal supports the compressed format natively, the code passes the inflated pitch directly to `UploadTextureContents` with staging buffers explicitly disabled:

```
// TextureMtl.mm — convertAndSetPerSliceSubImage, isBlock + native format
if (imageFormat.intendedFormatId == imageFormat.actualFormatId)
{
    const size_t dstDepthPitch = dstRowPitch * mtlArea.size.height;
    ANGLE_TRY(UploadTextureContents(
        context, dstFormat, mtlArea, mtl::kZeroNativeMipLevel, slice,
        pixels, dstRowPitch, dstDepthPitch, /*avoidStagingBuffers=*/true, imageDef.image));
}

```

`UploadTextureContents` finds that the texture is CPU-accessible (macOS managed storage) and calls Metal's `replaceRegion` with the wrong `bytesPerRow`:

```
// TextureMtl.mm — UploadTextureContents
if (texture->isCPUAccessible() && !preferGPUInitialization)
{
    texture->replaceRegion(contextMtl, region, mipmapLevel, slice,
                           data, bytesPerRow, bytesPer2DImage);
}

```

Metal interprets `bytesPerRow` as the stride between consecutive rows of blocks. With the inflated value of 4096 instead of 1024, the second block row is read from offset 4096 in the source buffer, the third from 8192, and so on. The source buffer is only 131072 bytes (the correct compressed data size), but the last block row is accessed at offset 4096 times 127 = 520192. The resulting ~384 KB out-of-bounds read crosses page boundaries and triggers SIGSEGV in the GPU process.

On macOS 11.0 and later, ETC2 maps to its native Metal pixel format (`MTLPixelFormatETC2_RGB8`), satisfying the `intendedFormatId == actualFormatId` condition. The same applies to ASTC formats on all macOS versions. Any block-compressed format that Metal supports natively is affected.

## Reproduce

This PoC reproduces a GPU process crash caused by a row pitch miscalculation in the ANGLE Metal backend when uploading block-compressed textures via PBO with a misaligned offset. It was tested on Chromium commit d0f83d769eeed (with ANGLE at 8dc22feb4412) on macOS (Apple Silicon). The bug requires a Mac with native ETC2 support, which includes all Apple Silicon machines running macOS 11.0 or later.

To check out the tested revision, run `git checkout d0f83d769eeed` in `~/chromium/src`. No source modifications or patches are needed.

Configure an ASAN build by writing the following to `~/chromium/src/out/asan-release/args.gn`:

```
is_asan = true
is_debug = false
is_component_build = true
symbol_level = 1
dcheck_always_on = false

```

Then build with `autoninja -C ~/chromium/src/out/asan-release chrome`.

Launch Chrome and open the PoC:

```
ASAN_OPTIONS=detect_odr_violation=0 ~/chromium/src/out/asan-release/Chromium.app/Contents/MacOS/Chromium --user-data-dir=/tmp/poc-test --enable-logging=stderr poc.html

```

Within a few seconds the GPU process will receive signal 11 (SEGV\_ACCERR) and crash. The browser process logs "GPU process exited unexpectedly: exit\_code=11" and "The GPU process has crashed 1 time(s)" to stderr. The crash is caused by Metal's replaceRegion reading past the end of a heap buffer due to the inflated bytesPerRow value computed by ANGLE. Because the out-of-bounds read occurs inside Apple's Metal framework rather than in ASAN-instrumented code, the crash manifests as a raw SIGSEGV rather than a formal ASAN report.

Crash log:

```
Received signal 11 SEGV_ACCERR 000344460001
 [0x000107360d88]
 [0x000107316580]
 [0x00010736093c]
 [0x00019bfd56a4]
 [0x00030a2195a4]
 [0x00030a2195a4]
 [0x00030a219530]
 [0x0003079e6640]
 [0x00030796774c]
 [0x00030796bab8]
 [0x00030796b98c]
 [0x00030796ac2c]
 [0x0003079645b0]
 [0x000307964b10]
 [0x0003075cb44c]
 [0x00030743ac1c]
 [0x00030705b344]
 [0x0001482119fc]
 [0x0001482591f0]
 [0x0001481e16d0]
 [0x00013f53ab48]
 [0x00014397e170]
 [0x00014397d2f0]
 [0x0001439a1a00]
 [0x0001439adaac]
 [0x0001439ad8c4]
 [0x00013f581b00]
 [0x00013f556010]
 [0x00013f5546a8]
 [0x00013f558850]
 [0x000107189808]
 [0x000107206e88]
 [0x000107206240]
 [0x0001073923d0]
 [0x00010737cdfc]
 [0x000107390760]
 [0x00019c086b14]
 [0x00019c086aa8]
 [0x00019c086814]
 [0x00019c085468]
 [0x00019c084a98]
 [0x00019d654c78]
 [0x000107393dbc]
 [0x00010738f338]
 [0x000107208244]
 [0x0001070f4b0c]
 [0x0001356e8a08]
 [0x000139460acc]
 [0x000139462c4c]
 [0x00013945e55c]
 [0x00013945ea4c]
 [0x00011d217728]
 [0x000104becb98]
 [0x00019bbfab98]
[end of stack trace]
[1151:68081751:0304/141207.415969:ERROR:gpu/ipc/client/command_buffer_proxy_impl.cc:484] GPU state invalid after WaitForGetOffsetInRange.
[1123:68081282:0304/141207.458497:ERROR:content/browser/gpu/gpu_process_host.cc:999] GPU process exited unexpectedly: exit_code=11
[1123:68081282:0304/141207.458534:WARNING:content/browser/gpu/gpu_process_host.cc:1441] The GPU process has crashed 1 time(s)

```
## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [readme.md](attachments/readme.md) (text/markdown, 1.5 KB)
- [asan.log](attachments/asan.log) (text/plain, 3.9 KB)
- [poc.html](attachments/poc.html) (text/html, 3.5 KB)
- [asan-crbug489579953.txt](attachments/asan-crbug489579953.txt) (text/plain, 18.3 KB)

## Timeline

### ct...@google.com (2026-03-07)

[security shepherd]

Thanks for the report. I can reproduce (on Stable and Dev), and if I specify `ASAN_OPTIONS='halt_on_error=0:allow_user_segv_handler=0'` I can get a full ASAN trace (attached), which does appear to be tickling a segfault inside the Metal system.

Adding kbr@ and kpiddington@ from the linked CL.

### ch...@google.com (2026-03-11)

Setting milestone because of s2 severity.

### ch...@google.com (2026-03-11)

Setting Priority to P2 to match Severity s2. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### kb...@google.com (2026-03-11)

Geoff, Kimmo - this is related to an earlier bug fix in the computation of sizes and pitches. Kimmo, is this resolved in your full patch for the earlier issue?

### kk...@apple.com (2026-03-13)

> Kimmo, is this resolved in your full patch for the earlier issue?
No, this is a distinct bug, reproduces with depth related pixel pack parameter state interpretation fixed.

### kb...@chromium.org (2026-03-24)

Geoff, let me try to take this one.

### dx...@google.com (2026-03-31)

Project: angle/angle  

Branch:  main  

Author:  Kenneth Russell [kbr@chromium.org](mailto:kbr@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7699417>

Metal: Fix pitch computation for compressed textures in PBOs.

---


Expand for full commit details
```
     
    Correctly detect block formats and adjust the row and depth pitch 
    computation. Inspiration taken from ANGLE's Vulkan backend. 
     
    Authored with gemini-cli, with guidance from domain experts. 
     
    Fixed: angleproject:489579953 
    Change-Id: I5656b02bc235bbe068191a0fb2049afcea9a094e 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7699417 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Commit-Queue: Kenneth Russell <kbr@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/metal/TextureMtl.mm`
- M `src/tests/gl_tests/ETCTextureTest.cpp`

---

Hash: [0323970550b9e2b52d46b3e7bb3c776bbb3c5c91](https://chromiumdash.appspot.com/commit/0323970550b9e2b52d46b3e7bb3c776bbb3c5c91)  

Date: Tue Mar 31 01:13:36 2026


---

### yn...@chromium.org (2026-04-02)

ETCTextureTest.PBOWithMisalignedOffset/ES3_OpenGLES fails on Pixel 10:
https://ci.chromium.org/ui/p/angle/builders/ci/android-arm64-exp-pixel10-test/1268/overview
I 22:34:24.860   52.660s _RunTestsOnDevice(54241FDCR00077)  [ RUN      ] ETCTextureTest.PBOWithMisalignedOffset/ES3_OpenGLES
I 22:34:24.860   52.660s _RunTestsOnDevice(54241FDCR00077)  ../../src/tests/test_utils/ANGLETest.cpp:73: Failure
I 22:34:24.860   52.661s _RunTestsOnDevice(54241FDCR00077)  RendererGL.cpp:117 (LogGLDebugMessage): 
I 22:34:24.860   52.661s _RunTestsOnDevice(54241FDCR00077)  	Source: API
I 22:34:24.860   52.661s _RunTestsOnDevice(54241FDCR00077)  	Type: Error
I 22:34:24.860   52.661s _RunTestsOnDevice(54241FDCR00077)  	ID: 0x00000000
I 22:34:24.860   52.661s _RunTestsOnDevice(54241FDCR00077)  	Severity: High
I 22:34:24.860   52.661s _RunTestsOnDevice(54241FDCR00077)  	Message: glCompressedTexSubImage2D: PBO is mapped, or incorrect imageSize/data 

I'll suppress.

### dx...@google.com (2026-04-02)

Project: angle/angle  

Branch:  main  

Author:  Yuly Novikov [ynovikov@chromium.org](mailto:ynovikov@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7726067>

Skip ETCTextureTest.PBOWithMisalignedOffset on Pixel 10 GLES

---


Expand for full commit details
```
     
    Bug: angleproject:489579953 
    Change-Id: I64343aa3a58b49eec449bcbd8b826e36b8ac17d1 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7726067 
    Commit-Queue: Yuly Novikov <ynovikov@chromium.org> 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: Yuly Novikov <ynovikov@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

```

---

Files:

- M `src/tests/angle_end2end_tests_expectations.txt`

---

Hash: [68919ec607c78ad96454e73a9a7d2bac11d1efd0](https://chromiumdash.appspot.com/commit/68919ec607c78ad96454e73a9a7d2bac11d1efd0)  

Date: Thu Apr 2 17:14:42 2026


---

### kb...@chromium.org (2026-04-02)

Thanks Yuly for suppressing the failure on the Pixel 10. Do you think that's an issue that needs to be investigated and fixed separately?

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure with bisect.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-08)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2026-07-09)

This Blink bug has been marked as either a release blocker or a vulnerability bug. Blink bugs affect all OSs supported by Chrome (except iOS), so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/489579953)*
