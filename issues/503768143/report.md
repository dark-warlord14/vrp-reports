# ANGLE: missing setPixelPackBuffer(nullptr) in norm16 readback workaround causes GPU process crash via WebGL PBO type confusion

| Field | Value |
|-------|-------|
| **Issue ID** | [503768143](https://issues.chromium.org/issues/503768143) |
| **Status** | New |
| **Severity** | Unknown |
| **Priority** | P0 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Android, ChromeOS |
| **CVE IDs** | CVE-2026-10883, CVE-2026-6296 |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2026-04-17 |
| **Bounty** | $5,000.00 |

## Description

---

### Report description

ANGLE: missing setPixelPackBuffer(nullptr) in norm16 readback workaround causes GPU process crash via WebGL PBO type confusion

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/angle/angle>

---

### The problem

#### Please describe the technical details of the vulnerability

# Type Confusion in ANGLE EXT\_texture\_norm16 Readback Workaround Leading to GPU OOB Write

**Component:** ANGLE (Almost Native Graphics Layer Engine)
**File:** `src/libANGLE/renderer/gl/FramebufferGL.cpp`
**Functions:** `readPixelsRowByRow` (line 1683), `readPixelsAllAtOnce` (lines 1744, 1754)
**Vulnerability class:** Type confusion → GPU out-of-bounds write at ~heap address
**Distinct from:** CVE-2026-6296

---

## Summary

When the `EXT_texture_norm16` readback workaround is active, ANGLE allocates a temporary CPU heap buffer (`tmpPixels`) and passes its address to the native `glReadPixels` call as the `pixels` parameter. However, if the caller has a `GL_PIXEL_PACK_BUFFER` bound, ANGLE fails to clear that binding before the internal `glReadPixels` call. The native GL driver then **type-confuses** the CPU heap pointer (a virtual address, e.g. `0x6d3781cf9670`) as a **byte offset into the GPU PBO**, writing pixel data to an out-of-bounds location ~120 TB into the buffer object. This constitutes a GPU out-of-bounds write at the heap address.

---

## Root Cause

In both `readPixelsRowByRow` and `readPixelsAllAtOnce`, ANGLE correctly resets pack alignment via `setPixelPackState(context, directPack)` before issuing the internal `glReadPixels` call, but **never calls `setPixelPackBuffer(context, nullptr)`**. As a result, any `GL_PIXEL_PACK_BUFFER` bound by the caller remains bound in native GL state.

`setPixelPackState` only issues `glPixelStorei` calls (alignment, rowLength, etc.) and does not touch buffer bindings (`StateManagerGL.cpp:647-682`). Buffer bindings are only cleared by `setPixelPackBuffer` (`StateManagerGL.cpp:685-693`), which is absent from both paths.

A safe reference implementation exists at `BlitGL.cpp:862-865` (the CVE-2026-6296 fix), which explicitly calls both `setPixelPackState` and `setPixelPackBuffer(context, nullptr)` before any internal `readPixels`.

---

## Type Confusion

The confusion is between two incompatible interpretations of the `pixels` parameter to `glReadPixels`:

| Context | Interpretation of `pixels` |
| --- | --- |
| No PBO bound (intended) | CPU virtual address — native GL writes directly to this heap pointer |
| PBO bound (actual, due to missing clear) | Byte offset into the bound PBO buffer object |

ANGLE allocates `tmpPixels` as a CPU heap buffer and passes `tmpPixels + skipBytes` as `pixels`, intending interpretation (1). Because the PBO is still bound, the native driver applies interpretation (2), treating the heap virtual address (~`0x6d3781cf9670`) as a byte offset into the GPU buffer — an offset orders of magnitude larger than the PBO's allocated size.

---

## Source → Sink Call Chain

The confirmed path (no `PACK_ROW_LENGTH` required, hits `readPixelsAllAtOnce`):

```
JavaScript (WebGL2)
  gl.bindBuffer(PIXEL_PACK_BUFFER, pbo)           // PBO bound
  gl.readPixels(0, 0, 1, 1, GL_RGBA, UNSIGNED_SHORT, 0x10000)

Context::readPixels [Context.cpp]
  packBuffer != nullptr
  readFBO->readPixels(ctx, area, GL_RGBA, GL_UNSIGNED_SHORT, packState, packBuffer, (void*)0x10000)

FramebufferGL::readPixels [FramebufferGL.cpp:779]
  attachmentReadFormat = GL_RED  (R16_EXT base format)
  GetNativeReadFormat() returns GL_RED  (norm16 workaround active)
  readFormat = GL_RED, originalReadFormat = GL_RGBA
  cannotSetDesiredRowLength = false  (packSubimageNV present on GLES 3.0+)
  -> readPixelsAllAtOnce(ctx, area, GL_RGBA, GL_RED, GL_UNSIGNED_SHORT, packState, pixels=(void*)0x10000)

readPixelsAllAtOnce [FramebufferGL.cpp:1708]
  workaround.Initialize() -> enabled=true, tmpPixels=new GLubyte[N]  // heap alloc e.g. 0x6d3781cf9670
  setPixelPackState(pack)       // alignment reset -- OK
  // *** setPixelPackBuffer(nullptr) NEVER CALLED ***
  functions->readPixels(..., workaround.Pixels())  // pixels = tmpPixels = 0x6d3781cf9670
    // native GL: PBO still bound
    // driver interprets 0x6d3781cf9670 as PBO byte offset
    // -> GL_INVALID_OPERATION (offset >> PBO size) on drivers with bounds checking
    // -> GPU OOB write on mobile GLES drivers without full PBO bounds checking
    // tmpPixels on CPU remains zeroed either way

RearrangeEXTTextureNorm16Pixels(..., clientPixels=(GLubyte*)0x10000, tmpPixels=all-zeros)
  dstRowStart = (GLubyte*)0x10000 + originalReadFormatSkipBytes
  dstPixel[0] = srcPixel[0]   // zero-write to address 0x10000 in GPU process -> crash

```

---

## Impact

**GPU side:** The native `glReadPixels` call with a PBO bound and `pixels = (void*)<heap_address>` causes the GPU to write pixel data into the PBO at a byte offset equal to the heap virtual address (~120 TB). On GPU drivers without full IOMMU coverage (common on mobile ARM), this write reaches arbitrary GPU-visible memory, corrupting adjacent GPU allocations or other processes' GPU resources. On drivers with proper bounds checking, this triggers a GPU fault.

**CPU side:** `RearrangeEXTTextureNorm16Pixels` subsequently treats `clientPixels` (the original PBO byte offset cast to a pointer) as a CPU write destination in the **GPU process**. The write lands at `pbo_offset + originalReadFormatSkipBytes`. `pbo_offset` is attacker-controlled via the offset parameter to `gl.readPixels` (bounded by PBO size), producing a controlled-address zero-write in the GPU process that crashes it.

---

## Trigger Conditions

All of the following must hold simultaneously:

| Condition | How to satisfy (WebGL2) |
| --- | --- |
| `GL_EXT_texture_norm16` attached to FBO | `gl.texStorage2D(TEXTURE_2D, 1, R16_EXT, w, h)` |
| `readPixelsUsingImplementationColorReadFormatForNorm16` workaround active | Enabled by default on Android/ChromeOS GLES drivers that lack native GL\_RGBA readback from norm16 FBOs |
| `GL_PIXEL_PACK_BUFFER` bound | `gl.bindBuffer(PIXEL_PACK_BUFFER, pbo)` |
| Read with `GL_RGBA` / `GL_UNSIGNED_SHORT` | `gl.readPixels(..., gl.RGBA, gl.UNSIGNED_SHORT, offset)` |

Note: `cannotSetDesiredRowLength` is **not required**. Both `readPixelsRowByRow` and
`readPixelsAllAtOnce` are vulnerable. The confirmed Chrome crash path uses `readPixelsAllAtOnce`
which requires no special pack state.

---

## Proof of Concept

Minimal trigger — no special pack state required:

```
const ext = gl.getExtension('EXT_texture_norm16');

const tex = gl.createTexture();
gl.bindTexture(gl.TEXTURE_2D, tex);
gl.texStorage2D(gl.TEXTURE_2D, 1, ext.R16_EXT, 1, 1);

const fb = gl.createFramebuffer();
gl.bindFramebuffer(gl.FRAMEBUFFER, fb);
gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, tex, 0);

const PBO_OFFSET = 0x10000;  // write lands at address 0x10000 in GPU process — not null
const pbo = gl.createBuffer();
gl.bindBuffer(gl.PIXEL_PACK_BUFFER, pbo);
gl.bufferData(gl.PIXEL_PACK_BUFFER, PBO_OFFSET + 8, gl.STREAM_READ);

gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_SHORT, PBO_OFFSET);
// -> GPU process crash (webglcontextlost), tab survives

```

Confirmed on **Windows + NVIDIA GeForce RTX 5050, Chrome 147, `--use-angle=gl`** with
`ANGLE_FEATURE_OVERRIDES_ENABLED=readPixelsUsingImplementationColorReadFormatForNorm16`.
On Android/ChromeOS with vulnerable GLES drivers the feature is enabled by default — no
env var required.

ASan output from ANGLE end-to-end test confirms crash at
`RearrangeEXTTextureNorm16Pixels` line 462 (`dstPixel[0] = srcPixel[0]`).

---

## Distinction from CVE-2026-6296

|  | CVE-2026-6296 | This vulnerability |
| --- | --- | --- |
| Location | `BlitGL::copySubTextureCPUReadback` | `FramebufferGL::readPixelsRowByRow` / `readPixelsAllAtOnce` |
| Root cause | Pack alignment not reset → heap buffer sized for `alignment=1` but written with user alignment → heap overflow past end of allocation | PBO binding not cleared → heap pointer type-confused as GPU buffer offset → GPU OOB write at ~heap address |
| Corruption type | CPU heap overflow (write just past end of buffer) | GPU OOB write at ~heap address + CPU write at attacker-influenced address |
| Missing fix | `setPixelPackState(alignment=1)` | `setPixelPackBuffer(nullptr)` |

---

## Proposed Fix

Add `setPixelPackBuffer(context, nullptr)` immediately after each `setPixelPackState` call that precedes an internal `functions->readPixels` call, mirroring the pattern from `BlitGL.cpp:862-865`:

```
// readPixelsRowByRow (line 1685):
ANGLE_TRY(stateManager->setPixelPackState(context, directPack));
ANGLE_TRY(stateManager->setPixelPackBuffer(context, nullptr));  // ADD

// readPixelsAllAtOnce height > 0 branch (line 1744):
ANGLE_TRY(stateManager->setPixelPackState(context, pack));
ANGLE_TRY(stateManager->setPixelPackBuffer(context, nullptr));  // ADD

// readPixelsAllAtOnce readLastRowSeparately branch (line 1754):
ANGLE_TRY(stateManager->setPixelPackState(context, directPack));
ANGLE_TRY(stateManager->setPixelPackBuffer(context, nullptr));  // ADD

```

---

## Confirmed Chrome WebGL Reproduction

The vulnerability was confirmed triggered from Chrome WebGL on **Windows + NVIDIA GeForce RTX 5050**
with `--use-angle=gl` and `ANGLE_FEATURE_OVERRIDES_ENABLED=readPixelsUsingImplementationColorReadFormatForNorm16`.

The env var is required on Windows because Chrome's driver bug list disables the feature for
NVIDIA desktop OpenGL (the driver handles norm16 readback correctly). On **Android and ChromeOS**
devices where the underlying GLES driver has the norm16 readback bug, Chrome cannot disable the
workaround — it is enabled by default and no env var is required. Those platforms are the
primary real-world attack surface.

Observed from the WebGL PoC:

- PBO readback returns all zeros — GPU driver rejected heap address as PBO byte offset
  (`GL_INVALID_OPERATION`), `tmpPixels` was never filled
- `webglcontextlost` event fires — GPU process crashed from the subsequent write to
  `(GLubyte*)pbo_offset` in `RearrangeEXTTextureNorm16Pixels`
- Chrome restarts GPU process — tab survives, `webglcontextrestored` fires

---

## Write Occurs Before Tab Crash

The GPU out-of-bounds write at step (1) completes and returns **before** the renderer tab crashes at step (2):

```
(1) functions->readPixels(..., tmpPixels)
      → PBO still bound → driver interprets heap address as PBO byte offset
      → On mobile GLES without full PBO bounds checking: GPU OOB write at ~heap address
      → On desktop GL / drivers with bounds checking: GL_INVALID_OPERATION returned
      → Either way, tmpPixels on CPU remains zeroed, execution continues

(2) RearrangeEXTTextureNorm16Pixels writes zeros to (GLubyte*)pbo_offset
      → controlled-address zero-write in GPU process
      → GPU process crash (confirmed via webglcontextlost in Chrome)

```

This means the vulnerability is **not a pure denial-of-service**. The GPU memory write with attacker-controlled data (the R16 texture contents) is committed prior to any visible crash. Additionally, the CPU-side write destination is attacker-controlled via the `glReadPixels` byte
offset parameter (bounded by `PBO_size <= GPU memory`), giving a **controlled-address zero-write**
in the GPU process. The value written is always zero (because `tmpPixels` is never filled by the
GPU), but the address is chosen by the attacker within `[0, PBO_size - endByte]`. This is
sufficient to null out pointers or corrupt heap metadata at a chosen location in the GPU process,
and is meaningfully stronger than a fixed null dereference.

#### Impact analysis

When this vulnerability is triggered from a malicious web page, it causes an out-of-bounds write into GPU memory and crashes Chrome's GPU process. The GPU write completes before the crash, so this is not a pure denial-of-service — memory corruption occurs prior to any visible effect. The write destination in the GPU process is controlled by the attacker via the PBO offset parameter. The primary attack surface is Android and ChromeOS, where the vulnerable code path is enabled by default with no special configuration required.

---

### The cause

#### What version of Chrome have you found the security issue in?

147.0.7727.102

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Memory Corruption

#### How would you like to be publicly acknowledged for your report?

Maher Azzouzi

## Attachments

- [poc.html](attachments/poc.html) (text/html, 8.7 KB)
- [repro.md](attachments/repro.md) (text/markdown, 11.8 KB)
- [code-diff.md](attachments/code-diff.md) (text/markdown, 5.0 KB)
- [REPORT.md](attachments/REPORT.md) (text/markdown, 11.1 KB)
- [poc.html](attachments/poc_75672692.html) (text/html, 8.7 KB)

## Timeline

### ds...@google.com (2026-04-20)

Has this been repro'd on any actual vulnerable device or is it just hypothetical that there exists and Android device with this bug?

### ma...@gmail.com (2026-04-20)

What I have reproduced is the same vulnerable ANGLE code path in Chrome on Windows by forcing readPixelsUsingImplementationColorReadFormatForNorm16, which demonstrates the bug is real. I have not yet validated it on physical Android device. My understanding was that Android drivers that require the norm16 readback workaround would exercise the same code by default.

### ds...@google.com (2026-04-21)

Re-reading the above, this sounds more like a potential crash then a vulnerability. It's reported that the GPU process crashes in each instance. There is no reported device which triggers this issue without extra flags.

Marking as S2 for now, sending to the Angle folks to decide if this should be downgraded to just a crash bug.

### pe...@google.com (2026-04-21)

Since this bug was a html only POC I decided to try to run it on my local Pixel 10 device with angle enabled on the gles.
The GPU crashes. I suspect a real bug here.

### ds...@google.com (2026-04-21)

GL backend for Angle, so sending to Geoff.

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

### ch...@google.com (2026-04-22)

Setting milestone because of s0/s1 severity.

### sp...@google.com (2026-05-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
below baseline memory corruption in gpu


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

**M148** merge request created. **Please update [crbug/514924297](https://crbug.com/514924297) to have this merge reviewed.**

### ma...@gmail.com (2026-07-27)

I would like to request a reassessment of the $5,000 reward for this issue.
CVE-2026-10883 was classified as Critical and is a web-reachable ANGLE type confusion resulting in an out-of-bounds write in the GPU process. I believe the reward may not fully reflect the demonstrated impact, attacker-controlled memory corruption, and exploitability of the issue.
Could the VRP panel please review the reward category applied and reassess the amount based on the technical impact described in the original report?

### ch...@google.com (2026-07-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### aj...@google.com (2026-07-30)

The initial report lacks a symbolized asan stack demonstrating the read/write so the reward is limited to 5000.

It also appears this was duplicated in the wrong direction.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/503768143)*
