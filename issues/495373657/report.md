# GPU process arbitrary address read via unvalidated client pointer in passthrough `CompressedTexImage3D` / `CompressedTexSubImage3D` handlers

| Field | Value |
|-------|-------|
| **Issue ID** | [495373657](https://issues.chromium.org/issues/495373657) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | cw...@google.com |
| **Created** | 2026-03-23 |
| **Bounty** | $5,000.00 |

## Description

## Summary

The passthrough command decoder's handlers for `CompressedTexImage3D` and `CompressedTexSubImage3D` reinterpret the command's `data_shm_offset` field as a raw GPU-process pointer when `data_shm_id` is zero. This encoding is intended for Pixel Buffer Object offsets, but the handler performs no check that a PBO is actually bound. ANGLE's compressed texture validators pass a hardcoded `imageSize` of negative one to the internal `ValidImageDataSize` helper, which then skips all host-memory size validation when no PBO is present. Every ANGLE backend dereferences this fabricated pointer during texture upload: D3D11 through `Image11::loadCompressedData`, Vulkan through `TextureVk::stageSubresourceUpdate`, and Metal through `TextureMtl::setImageImpl`. A compromised renderer can therefore read from any address in the low 4 GB of the GPU process address space by sending a single crafted command buffer entry. Platform: Windows, macOS, Linux, ChromeOS; any GPU.

## Bisect

Introducing Commit: `95f938225bec04fe8e3d87bcc692f67c6388cf06`

- Date: 2017-04-12
- Author: Corentin Wallez
- Review: <https://codereview.chromium.org/2811693005>

This commit added PBO offset support to the passthrough command decoder's compressed texture upload handlers. The original code (from `d00f0b244d1bb`, 2016-06-03) treated all nonzero `data_shm_id` or `data_shm_offset` combinations as shared-memory lookups. The `95f938225bec0` change split the `data_shm_id == 0` case into a new branch that reinterprets `data_shm_offset` as a raw pointer for PBO offsets, but omitted a check that a pixel unpack buffer is actually bound. The legacy (non-passthrough) command decoder contains the corresponding guard: it rejects `data_shm_id == 0` when no PBO is bound by returning `error::kInvalidArguments`. The passthrough decoder never acquired an equivalent check.

## Root Cause

The vulnerability arises from a mismatch between the command buffer's data encoding convention and the validation performed downstream in ANGLE.

When the GPU-side passthrough handler receives a `CompressedTexImage3D` command, it branches on the `data_shm_id` field. A nonzero id triggers a validated shared-memory lookup with bounds checking. An id of zero, however, causes the handler to synthesize a pointer directly from `data_shm_offset`:

```
// gpu/command_buffer/service/gles2_cmd_decoder_passthrough_handlers.cc
const void* data = nullptr;
if (data_shm_id != 0) {
  unsigned int data_size = 0;
  data = GetSharedMemoryAndSizeAs<const void*>(data_shm_id, data_shm_offset,
                                               image_size, &data_size);
  if (data == nullptr) {
    return error::kOutOfBounds;
  }
} else {
  data =
      reinterpret_cast<const void*>(static_cast<intptr_t>(data_shm_offset));
}

```

The zero-id path exists to encode PBO offsets, where the `data` argument to `glCompressedTexImage3D` is treated as a byte offset into the currently bound pixel unpack buffer rather than a host pointer. The handler does not verify that a PBO is actually bound before constructing this pointer; it unconditionally forwards the fabricated address to `DoCompressedTexImage3D`, which passes it straight through to ANGLE:

```
// gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc
api()->glCompressedTexImage3DFn(target, level, internalformat, width, height,
                                depth, border, image_size, data);

```

Inside ANGLE, the `ValidateCompressedTexImage3D` function verifies format parameters and that `imageSize` matches the computed block size, then delegates to the shared `ValidateES3TexImage3DParameters` with a hardcoded `imageSize` argument of negative one:

```
// third_party/angle/src/libANGLE/validationES3.cpp
if (!ValidateES3TexImage3DParameters(context, entryPoint, target, level,
                                     internalformat, true, false, 0, 0, 0,
                                     width, height, depth, border, GL_NONE,
                                     GL_NONE, -1, data))

```

That negative-one value reaches `ValidImageDataSize`, which contains an early return that was designed to skip validation when the caller has already verified the compressed image size separately:

```
// third_party/angle/src/libANGLE/validationES.cpp
Buffer *pixelUnpackBuffer =
    context->getState().getTargetBuffer(BufferBinding::PixelUnpack);
if (pixelUnpackBuffer == nullptr && imageSize < 0)
{
    return true;
}

```

When no PBO is bound and `imageSize` is negative one, validation returns immediately without examining the `data` pointer at all. In standard OpenGL semantics a non-null `data` without a PBO is a valid client pointer upload, so ANGLE has no reason to reject it. The pointer proceeds through the D3D11 texture backend, where `GetUnpackPointer` returns it verbatim when no unpack buffer is present:

```
// third_party/angle/src/libANGLE/renderer/d3d/TextureD3D.cpp
if (unpackBuffer)
{
    // ... read from PBO ...
}
else
{
    *pointerOut = pixels;
}

```

The pointer finally reaches `Image11::loadCompressedData`, which maps a D3D11 staging texture and copies data from the pointer via a format-specific load function:

```
// third_party/angle/src/libANGLE/renderer/d3d/d3d11/Image11.cpp
loadFunction(context11->getImageLoadContext(), area.width, area.height,
             area.depth, static_cast<const uint8_t *>(input),
             inputRowPitch, inputDepthPitch, offsetMappedData,
             mappedImage.RowPitch, mappedImage.DepthPitch);

```

For a 4x4 DXT5 block this resolves to `LoadCompressedToNative<4,4,1,16>`, which performs a 16-byte `memcpy` from the attacker-supplied address into the staging texture. On a 64-bit build the fabricated pointer is zero-extended from 32 bits, restricting the read range to the low 4 GB of the GPU process virtual address space. This is sufficient to read mapped code sections and portions of static data, and the read content lands in a GPU texture that could in principle be exfiltrated back to the renderer via `readPixels`.

The passthrough decoder is the only command decoder compiled on non-Android platforms. The build system sets `enable_validating_command_decoder = is_android` in `ui/gl/features.gni`, so on Windows, macOS, Linux, and ChromeOS the passthrough path is always active and this vulnerability is always reachable.

The same `data_shm_id == 0` pointer fabrication pattern appears in all four compressed texture upload handlers: `HandleCompressedTexImage2D`, `HandleCompressedTexSubImage2D`, `HandleCompressedTexImage3D`, and `HandleCompressedTexSubImage3D`.

## Reproduce

The bug was tested on Chromium commit `d633da0f560b561113ef431f228063b059b0c896` on macOS, Ubuntu22.04 and Windows 11.

This is a compromised-renderer attack against the GPU process. The renderer-side command buffer client is patched to bypass the normal bucket transfer path for compressed texture uploads and instead send a raw `CompressedTexImage3D` command with `data_shm_id` set to zero and `data_shm_offset` set to an arbitrary 32-bit address. The GPU process passthrough handler interprets this offset as a client pointer and forwards it to ANGLE, which dereferences it during texture upload. Apply the patch to the Chromium source tree from the repository root.

Configure an ASAN build with out/asan/args.gn as follows, then build:

```
is_asan = true
is_debug = false
dcheck_always_on = false

```
```
git apply patch.diff
autoninja -C out/asan chrome

```

Launch Chrome with the PoC page:

```
# Windows(poc.html uses an absolute path)
$ out\asan\chrome.exe --enable-logging=stderr --user-data-dir=/tmp/poc /path/to/poc.html 2>/tmp/asan.txt
$ cat /tmp/asan.txt

# Linux
out/asan/chrome --enable-logging=stderr --user-data-dir=./user poc.html

```

The GPU process will crash immediately when the WebGL2 page issues `compressedTexImage3D`. AddressSanitizer reports an access-violation READ at address `0x000041414141` inside `angle::LoadCompressedToNative`, called from `rx::Image11::loadCompressedData`. The full stack trace is preserved in `asan.txt`.

ASAN log:

```
=================================================================
==23904==ERROR: AddressSanitizer: access-violation on unknown address 0x000041414141 (pc 0x7ffb3f47dc26 bp 0x0026eedfd200 sp 0x0026eedfd178 T0)
==23904==The signal is caused by a READ memory access.
==23904==*** WARNING: Failed to initialize DbgHelp!              ***
==23904==*** Most likely this means that the app is already      ***
==23904==*** using DbgHelp, possibly with incompatible flags.    ***
==23904==*** Due to technical reasons, symbolization might crash ***
==23904==*** or produce wrong results.                           ***
    #0 0x7ffb3f47dc25 in memcpy+0x125 (C:\Windows\System32\ucrtbase.dll+0x1800edc25)
    #1 0x7ffac8ecb532 in _asan_memcpy+0x422 (D:\src\chromium\src\out\asan\clang_rt.asan_dynamic-x86_64.dll+0x18004b532)
    #2 0x7ffab7786e9c in angle::LoadCompressedToNative<4,4,1,16> D:\src\chromium\src\third_party\angle\src\image_util\loadimage.inc:402
    #3 0x7ffab7872070 in rx::Image11::loadCompressedData D:\src\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Image11.cpp:352
    #4 0x7ffab79d0c73 in rx::TextureD3D_2DArray::setCompressedImage D:\src\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp:3450
    #5 0x7ffab76a4f36 in gl::Texture::setCompressedImage D:\src\chromium\src\third_party\angle\src\libANGLE\Texture.cpp:1470
......

```
## Credit

Please use 86ac1f1587b71893ed2ad792cd7dde32 as the credit for this vulnerability. Thank you.

## Attachments

- deleted (application/octet-stream, 0 B)
- [poc.html](attachments/poc.html) (text/html, 1.3 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 7.5 KB)
- [patch.diff](attachments/patch.diff) (text/x-diff, 2.1 KB)

## Timeline

### se...@gmail.com (2026-03-23)

Attached is the supplementary `patch.diff`. The patch includes judgment and isolation for the render process, ensuring that malicious attack code is only executed within the render process.

### wf...@chromium.org (2026-03-25)

Thank you for the report. This is well formatted and looks valid, but I have not reproduced this as it needs a patched renderer. I agree this looks like an arbitrary read at an attacker controlled address within the sandboxed GPU process, accessible from a compromised renderer. I am therefore assigning severity medium as per severity guidelines.

### wf...@chromium.org (2026-03-25)

I am assigning to cwallez based on context, and foundin 146 as this seems to be quite an old bug and 146 is the earliest extended stable.

### ch...@google.com (2026-03-26)

Setting milestone because of s2 severity.

### ch...@google.com (2026-03-26)

Setting Priority to P2 to match Severity s2. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-03-31)

Project: chromium/src  

Branch:  main  

Author:  Corentin Wallez [cwallez@chromium.org](mailto:cwallez@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7702692>

GLES2 passthrough decoder: validate unpack buffer is bound.

---


Expand for full commit details
```
     
    In the handling of gl[Compressed]Tex[Sub]Image[2D/3D] the 
    data_shm_offset can be used either as an offset in the 
    GL_PIXEL_UNPACK_BUFFER or as a pointer to memory to upload to the GPU. 
    When data_shm_id is 0 and the data_shm_offset is not 0. 
     
    When both id and offset are 0, it is allowed to have no unpack buffer 
    because all [Compressed]TexImage[2D/3D] use that to specify a 
    zero-initialized data store, and the [Compressed]TexSubImage[2D/3D] all 
    validate that nullptr is only used with empty sizes. 
     
    Bug: 495373657 
    Change-Id: I14f6d15889e0e5afffa45b4bc9198e76fe286939 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7702692 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Auto-Submit: Corentin Wallez <cwallez@chromium.org> 
    Commit-Queue: Corentin Wallez <cwallez@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1607944}

```

---

Files:

- M `gpu/command_buffer/service/gles2_cmd_decoder_passthrough.h`
- M `gpu/command_buffer/service/gles2_cmd_decoder_passthrough_handlers.cc`

---

Hash: [3ff819cc07be9f8a36c8294494da9b57bd2ed857](https://chromiumdash.appspot.com/commit/3ff819cc07be9f8a36c8294494da9b57bd2ed857)  

Date: Tue Mar 31 17:09:22 2026


---

### ch...@google.com (2026-04-01)

Merge review required: M147 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-04-01)

Merge review required: M146 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### dr...@chromium.org (2026-04-01)

cwallez@ - given the severity here, I don't see a strong need to merge this. Did you want to merge it for some reason? If so, we can consider it through the non-security merge process.

### cw...@chromium.org (2026-04-01)

Not merging sgtm as well.

### sp...@google.com (2026-06-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/495373657)*
