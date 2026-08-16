# Heap OOB read in ANGLE via `CubeMapArray` texture upload due to `endByte` underestimation in `ValidImageDataSize`

| Field | Value |
|-------|-------|
| **Issue ID** | [495052581](https://issues.chromium.org/issues/495052581) |
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

ANGLE's D3D11 backend computes the source row pitch for texture uploads using the texture's internal format rather than the upload format. When a compromised renderer creates a texture with `GL_RGBX8_ANGLE` (4 bytes per pixel) and uploads data as `GL_RGB` (3 bytes per pixel), the validation layer sizes the input buffer using the 3-byte format while the upload path strides through the data using the 4-byte format. The resulting heap-buffer-overflow occurs in CPU-side pixel conversion within the GPU process. `GL_RGBX8_ANGLE` passes `TexStorage` validation unconditionally because its `textureSupport` function is registered as `AlwaysSupported` without an extension gate. **Platform: Windows (D3D11 ANGLE backend).**

## Bisect

Introducing Commit: `4f42a4d3f72518e310cad6ef5cc991078577a747`

- Date: 2021-12-08
- Author: Tim Van Patten
- Review: <https://chromium-review.googlesource.com/c/angle/angle/+/3312367>

This commit registered `GL_RGBX8_ANGLE` with `AlwaysSupported` for `textureSupport` in the format table. The original `GL_RGBX8_ANGLEX` format was added in `c0aa61082d` (2021-09-28) with more restrictive support. The `4f42a4d` commit broadened support but did not add an extension gate in `ValidateES2TexStorageParametersBase`, creating the validation gap that allows a compromised renderer to instantiate the format.

## Root Cause

The vulnerability has two components that combine to produce a heap-buffer-overflow.

The first component is a validation gap in `TexStorage2DEXT`. `ValidateES2TexStorageParametersBase` checks whether the requested internal format is supported by calling the format's `textureSupport` function:

```
// validationES2.cpp — ValidateES2TexStorageParametersBase
const InternalFormat &formatInfo = GetSizedInternalFormatInfo(internalformat);
if (!formatInfo.textureSupport(context->getClientVersion(), context->getExtensions()))
{
    return false;
}

```

The format table registers `GL_RGBX8_ANGLE` with `AlwaysSupported`:

```
// formatutils.cpp
AddRGBAXFormat(&map, GL_RGBX8_ANGLE, true, ..., AlwaysSupported, AlwaysSupported, ...);

```

The `TexImage` path has a separate extension check for `rgbxInternalFormatANGLE`, but the `TexStorage` path does not. A compromised renderer can therefore create a texture with `GL_RGBX8_ANGLE` as its internal format through the `TexStorage2DEXT` command, which the passthrough decoder forwards to ANGLE without additional validation.

The second component is a row pitch mismatch between validation and the D3D11 upload implementation. When `TexSubImage2D` is called on the RGBX8 texture with `format=GL_RGB` and `type=GL_UNSIGNED_BYTE`, the validation layer computes the input data size using the upload format (3 bytes per pixel):

```
// validationES2.cpp — ValidateES2TexImageParametersBase
GLenum sizeCheckFormat = isSubImage ? format : internalformat;
return ValidImageDataSize(context, ..., sizeCheckFormat, type, pixels, imageSize);

```

The D3D11 upload path, however, recomputes `srcRowPitch` using the texture's actual internal format:

```
// TextureStorage11.cpp — TextureStorage11::setData
const gl::InternalFormat &internalFormatInfo =
    gl::GetInternalFormatInfo(image->getInternalFormat(), type);
internalFormatInfo.computeRowPitch(type, width, unpack.alignment, unpack.rowLength, &srcRowPitch);

```

For `GL_RGBX8_ANGLE`, `formatutils.cpp` special-cases the component count to 4:

```
// formatutils.cpp — InternalFormat::computePixelBytes
if (sizedInternalFormat == GL_RGBX8_ANGLE)
{
    components = 4;
}

```

This produces `srcRowPitch = width * 4` instead of the expected `width * 3`. The load function `LoadToNativeByte3To4Impl` then reads the source data with 3-byte pixel access but advances rows using the inflated 4-byte row pitch. For a 256×256 texture, the validation allows 196608 bytes (256 × 3 × 256), while the D3D11 backend reads up to 261888 bytes (1024 × 255 + 768), overflowing the heap allocation by 65280 bytes.

The PBO upload path is particularly suited for triggering this because ANGLE's D3D11 backend retrieves PBO data through `Buffer11::getData`, which returns a pointer to `SystemMemoryStorage` backed by `angle::MemoryBuffer`, a malloc-allocated buffer. AddressSanitizer tracks this allocation and detects the overflow in the GPU process.

## Reproduce

This issue was tested on Chromium commit `8a39e4056b7ab6470456e5281ebe8cf4a236ec08` running on Windows 11 with an NVIDIA GeForce RTX 4060 Ti. The bug is in the ANGLE D3D11 backend and requires only the default Windows GPU configuration.

Apply the patch, which modifies `WebGL2RenderingContextBase::texSubImage3D` in the renderer process to inject `GL_RGBX8_ANGLE` texture commands when it detects a sentinel PBO offset value. This simulates a compromised renderer sending crafted GL commands through the passthrough command buffer decoder. No GPU process code is modified.

Configure an ASAN build with `out/asan/args.gn` as follows, then build:

```
is_asan = true
is_debug = false
dcheck_always_on = false
target_cpu = "x64"

```
```
git apply patch.diff
autoninja -C out/asan chrome

```

Launch Chrome and open the poc page(poc.html uses an absolute path).

```
$ out\asan\chrome.exe --enable-logging=stderr --user-data-dir=/tmp/poc /path/to/poc.html 2>/tmp/asan.txt
$ cat /tmp/asan.txt

```

The PoC page creates a WebGL2 context and calls `texSubImage3D` with PBO offset `0x120012`, which the patched renderer intercepts. The renderer unbinds the PBO, creates a 256×256 texture with internal format `GL_RGBX8_ANGLE` (`0x96BA`) via `TexStorage2DEXT`, then creates a 196608-byte PBO matching the RGB 3-bytes-per-pixel validation expectation. It calls `TexSubImage2D` with `format=GL_RGB` and `type=GL_UNSIGNED_BYTE` via the PBO. ANGLE's validation computes `endByte` as 196608 using 3 bytes per pixel and passes the PBO size check. The D3D11 backend recalculates `srcRowPitch` using the texture's internal format `GL_RGBX8_ANGLE`, which has 4 components, producing a row pitch of 1024 instead of the correct 768. The load function `LoadToNativeByte3To4Impl` reads with 1024-byte row stride across 256 rows, accessing a total of 261888 bytes from the 196608-byte PBO heap allocation. AddressSanitizer detects the 65280-byte heap-buffer-overflow in the GPU process.

ASAN output:

```
=================================================================
==25884==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x1211da001800 at pc 0x7ffabf0f6ae5 bp 0x00650bbfd6b0 sp 0x00650bbfd6f8
READ of size 4 at 0x1211da001800 thread T0
==25884==*** WARNING: Failed to initialize DbgHelp!              ***
==25884==*** Most likely this means that the app is already      ***
==25884==*** using DbgHelp, possibly with incompatible flags.    ***
==25884==*** Due to technical reasons, symbolization might crash ***
==25884==*** or produce wrong results.                           ***
[5908:21516:0323/045638.730:ERROR:google_apis\gcm\engine\registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
    #0 0x7ffabf0f6ae4 in angle::LoadToNativeByte3To4Impl D:\src\chromium\src\third_party\angle\src\image_util\loadimage.inc:198
    #1 0x7ffabf0f5e2f in angle::LoadToNative3To4<unsigned char,255> D:\src\chromium\src\third_party\angle\src\image_util\loadimage.inc:243
    #2 0x7ffabf25e691 in rx::TextureStorage11::setData D:\src\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\TextureStorage11.cpp:921
    #3 0x7ffabf315ab0 in rx::TextureD3D::subImage D:\src\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp:375
    #4 0x7ffabf31dd77 in rx::TextureD3D_2D::setSubImage D:\src\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp:1148
......

```
## References

- `ValidateES2TexStorageParametersBase` `textureSupport` check: <https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/validationES2.cpp;l=1843>
- `GL_RGBX8_ANGLE` registered as `AlwaysSupported`: <https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/formatutils.cpp;l=1151>
- `RGBX8_ANGLE` component count special case: <https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/formatutils.cpp;l=1692>
- `TextureStorage11::setData` uses internal format for `srcRowPitch`: <https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/d3d/d3d11/TextureStorage11.cpp;l=872>
- `ValidateES2TexImageParametersBase` uses upload format for `sizeCheckFormat`: <https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/validationES2.cpp;l=1746>
- `LoadToNativeByte3To4Impl` row-stride read: <https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/image_util/loadimage.inc;l=198>
- Passthrough decoder `DoTexStorage2DEXT` (no validation): <https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc;l=3574>

## Credit

Please use 86ac1f1587b71893ed2ad792cd7dde32 as the credit for this vulnerability. Thank you.

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 14.2 KB)
- [patch.diff](attachments/patch.diff) (text/x-diff, 2.4 KB)
- [poc.html](attachments/poc.html) (text/html, 801 B)

## Timeline

### se...@gmail.com (2026-03-23)

Hi! Please note that the ASAN crash for this vulnerability may appear somewhat similar to the one in <https://issues.chromium.org/issues/494823889>. However, they are two completely distinct vulnerabilities with different root causes, PoCs, triggering environments, and conditions.

### cl...@appspot.gserviceaccount.com (2026-03-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5598758439944192.

### sk...@google.com (2026-03-23)

Cannot reproduce. Setting provisional FoundIn/Severity and assigning to author commit from the link in the bug

### ch...@google.com (2026-03-24)

Setting milestone because of s2 severity.

### dx...@google.com (2026-04-11)

Project: angle/angle  

Branch:  main  

Author:  Gregg Tavares [gman@chromium.org](mailto:gman@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7723225>

Fix for Angle D3D RGBX Data Upload via PBO issue

---


Expand for full commit details
```
     
    There were 2 issues 
     
    1. in formatutils.cpp, GL_RGBX8_ANGLE format and related 
       were set to always be enabled. This meant, even if 
       the extension was not on, ANGLE would incorrectly allow 
       using the format. It should have instead generated a 
       GL error. The extension is only turned on in vulkan 
       but the bug allowed its use on other backends. 
     
       This is fixed. ANGLE will correctly emit an error if 
       the extension is not turned on. Tests added. 
     
    2. In D3D, when uploading to GL_RGBX8_ANGLE with a 
       GL_RGB source,  the code would take the fast path for 
       uploading which wrongly computed the size of the upload 
       based on the texture's internal format (4 bytes per 
       pixel), not on the source's format (3 bytes per pixel), 
       and so would access out of bounds data. 
     
       This is fixed by forcing the slow path that handles 
       this use case. A test has been added so if someone 
       enables the fast path that does not handle this case 
       they will get a test failure to fix the fast path. 
     
    Bug: chromium:495052581 
    Change-Id: Ic7257049ba18d12e9d5f775c81722306dad96c9b 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7723225 
    Commit-Queue: Gregg Tavares <gman@chromium.org> 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Auto-Submit: Gregg Tavares <gman@chromium.org>

```

---

Files:

- M `src/libANGLE/formatutils.cpp`
- M `src/libANGLE/formatutils.h`
- M `src/libANGLE/renderer/d3d/TextureD3D.cpp`
- M `src/tests/gl_tests/TextureTest.cpp`

---

Hash: [97d33bc6e1356dcb2e63ea4ca7e6ebd2bc81a39d](https://chromiumdash.appspot.com/commit/97d33bc6e1356dcb2e63ea4ca7e6ebd2bc81a39d)  

Date: Fri Apr 3 08:01:17 2026


---

### dx...@google.com (2026-04-11)

Project: chromium/src  

Branch:  main  

Author:  [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com) [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7750427>

Roll ANGLE from 1433dd4e8a59 to 97d33bc6e135 (4 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/1433dd4e8a59..97d33bc6e135 
     
    2026-04-11 gman@chromium.org Fix for Angle D3D RGBX Data Upload via PBO issue 
    2026-04-11 syoussefi@chromium.org Fix format check for a few glTexImage2D combinations 
    2026-04-10 bsheedy@chromium.org Remove legacy Android/arm64 infra/specs entries 
    2026-04-10 bsheedy@chromium.org Remove legacy Android/arm64 builders 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/angle-chromium-autoroll 
    Please CC angle-team@google.com,geofflang@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:495052581,chromium:500501226 
    Tbr: geofflang@google.com 
    Change-Id: Iab7c8dbe02ed8a07349dff812c6e6680f3ec0308 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7750427 
    Commit-Queue: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1613220}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [a44ea6444c55b8fa2bd93320ad75042ed039accb](https://chromiumdash.appspot.com/commit/a44ea6444c55b8fa2bd93320ad75042ed039accb)  

Date: Sat Apr 11 02:12:06 2026


---

### dx...@google.com (2026-04-15)

Project: angle/angle  

Branch:  main  

Author:  Gregg Tavares [gman@chromium.org](mailto:gman@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7764324>

Fix RGBX Tests

---


Expand for full commit details
```
     
    RGBX support was fixed to generate errors if not enabled. 
    These tests were passing because they didn't check if it was 
    valid to use RGBX 
     
    Bug: chromium:495052581 
    Change-Id: I3c5695422037214673d332fb9147325de5bbb389 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7764324 
    Commit-Queue: Gregg Tavares <gman@chromium.org> 
    Reviewed-by: Geoff Lang <geofflang@chromium.org>

```

---

Files:

- M `src/tests/gl_tests/ImageTest.cpp`

---

Hash: [942c07d0c8a6ab15368faa6c972385536189244c](https://chromiumdash.appspot.com/commit/942c07d0c8a6ab15368faa6c972385536189244c)  

Date: Wed Apr 15 17:06:55 2026


---

### dx...@google.com (2026-04-16)

Project: chromium/src  

Branch:  main  

Author:  [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com) [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7767115>

Roll ANGLE from e24b8693b5e4 to 942c07d0c8a6 (1 revision)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/e24b8693b5e4..942c07d0c8a6 
     
    2026-04-15 gman@chromium.org Fix RGBX Tests 
     
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
    Bug: chromium:495052581 
    Tbr: solti@google.com 
    Change-Id: I8c834889f2f5f52b42dc95255d653b56ddb2c100 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7767115 
    Commit-Queue: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1615609}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [1720c52c94d1b2464dbd1ba70a5c7610ce9fe68b](https://chromiumdash.appspot.com/commit/1720c52c94d1b2464dbd1ba70a5c7610ce9fe68b)  

Date: Thu Apr 16 03:18:09 2026


---

### sp...@google.com (2026-06-29)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
User information disclosure with bisect.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-08-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/495052581)*
