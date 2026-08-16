# Integer truncation in ANGLE D3D11 VertexDataManager leads to heap OOB read from compromised renderer on Windows

| Field | Value |
|-------|-------|
| **Issue ID** | [506212452](https://issues.chromium.org/issues/506212452) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **CVE IDs** | CVE-2026-5281 |
| **Reporter** | je...@gmail.com |
| **Assignee** | am...@google.com |
| **Created** | 2026-04-24 |
| **Bounty** | $3,000.00 |

## Description

---

### Report description

Integer Overflow to OOB Heap Read in GPU Process (VertexBuffer11, D3D11)

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

third\_party/angle/src/libANGLE/renderer/d3d/d3d11/VertexBuffer11.cpp

---

### The problem

#### Please describe the technical details of the vulnerability

## Summary

`VertexBuffer11::storeVertexAttributes` (VertexBuffer11.cpp:114) truncates a `size_t` stride to `int` via `static_cast<int>`. When stride exceeds `INT_MAX`, it wraps to a negative value. This negative stride is used in pointer arithmetic, causing the read pointer to move backward past the buffer allocation — an out-of-bounds heap read in the GPU process.

This is the same bug class as [b/489369089](https://issues.chromium.org/issues/489369089), which was fixed with `CheckedNumeric` in `VertexDataManager.cpp` (commit 641c0d0). The fix was NOT applied to `VertexBuffer11.cpp` — the `static_cast<int>` truncation remains.

**Component:** ANGLE (D3D11 backend)
**File:** `third_party/angle/src/libANGLE/renderer/d3d/d3d11/VertexBuffer11.cpp`, line 114
**Type:** Integer overflow → out-of-bounds heap read
**Process:** GPU process
**Platform:** Windows (D3D11 backend)
**Attack model:** Compromised renderer → GPU process

## Vulnerable Code

```
// VertexBuffer11.cpp:114
int inputStride = static_cast<int>(ComputeVertexAttributeStride(attrib, binding));
// ...
// Line 125 — OOB pointer arithmetic
input += inputStride * start;  // negative stride * start → pointer goes BACKWARD
// Line 133 — reads from OOB memory
vertexFormatInfo.copyFunction(input, inputStride, count, output);

```
## Sibling Fix (same class, already applied to different file)

Commit 641c0d0 — "D3D11: Fix potential OOB read in StoreStaticAttrib" ([b/489369089](https://issues.chromium.org/issues/489369089)):

- <https://chromium.googlesource.com/angle/angle/+/641c0d0>
- <https://chromium-review.googlesource.com/c/angle/angle/+/7736785>

```
// VertexDataManager.cpp — FIXED
-const int offset = static_cast<int>(ComputeVertexAttributeOffset(attrib, binding));
+angle::CheckedNumeric<GLintptr> offset = ComputeVertexAttributeOffset(attrib, binding);

```

The identical `static_cast<int>` pattern in VertexBuffer11.cpp was NOT fixed.

## Web PoC

**Attached: `poc.html`** — an HTML page with WebGL that triggers the OOB read.

The PoC uses `GL_UNSIGNED_BYTE` normalized attributes (forces D3D11 format conversion → streaming path through `storeVertexAttributes`) with `stride = -4` and `glDrawArrays(GL_TRIANGLES, first=1, count=3)`.

### Reproduction

```
# 1. Build Chromium with ASAN (release mode, Windows)
gn gen out/AsanRelease --args='is_asan=true is_debug=false is_component_build=false dcheck_always_on=false'
autoninja -C out/AsanRelease content_shell

# 2. Apply validation_bypass.patch (simulates compromised renderer — see below)

# 3. Rebuild (incremental, ~1 min)
autoninja -C out/AsanRelease content_shell

# 4. Run
set ASAN_OPTIONS=detect_leaks=0:symbolize=1:halt_on_error=1
out\AsanRelease\content_shell.exe --enable-gpu --use-angle=d3d11 --no-sandbox --single-process poc.html

```
### ASAN Output (from content\_shell)

```
==PID==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x1245f3685cbc
READ of size 4 at 0x1245f3685cbc thread T15
    #0 rx::CopyNativeVertexData<signed char,4,4,0>    copyvertex.inc.h:84
    #1 rx::VertexBuffer11::storeVertexAttributes       VertexBuffer11.cpp:133
    #2 rx::StreamingVertexBufferInterface::storeDynamicAttribute  VertexBuffer.cpp:206
    #3 rx::VertexDataManager::storeDynamicAttrib        VertexDataManager.cpp:595
    #4 rx::VertexDataManager::storeDynamicAttribs       VertexDataManager.cpp:462
    #5 rx::VertexArray11::updateDynamicAttribs          VertexArray11.cpp:330
    #6 rx::VertexArray11::syncStateForDraw              VertexArray11.cpp:163
    #7 rx::StateManager11::updateState                  StateManager11.cpp:2001
    #8 rx::Context11::drawArrays                        Context11.cpp:285
    #9 GL_DrawArrays                                    entry_points_gles_2_0_autogen.cpp:1819
    #10 gl::RealGLApi::glDrawArraysFn                   gl_gl_api_implementation.cc:390
    #11 gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArrays  gles2_cmd_decoder_passthrough_doers.cc:1149
    #12 gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl  gles2_cmd_decoder_passthrough.cc:745
    #13 gpu::CommandBufferService::Flush                 command_buffer_service.cc:267

0x1245f3685cbc is located 4 bytes before 256-byte region [0x1245f3685cc0,0x1245f3685dc0)
SUMMARY: AddressSanitizer: heap-buffer-overflow copyvertex.inc.h:84

```
## Why Validation Bypass Patches Are Needed

This is a **compromised renderer → GPU process** bug. The `validation_bypass.patch` contains 3 changes that simulate what a compromised renderer does:

### Patch 1: Stride < 0 check (validationES2.h)

A compromised renderer writes directly to GPU command buffer shared memory. The passthrough command decoder (`DoVertexAttribPointer` in `gles2_cmd_decoder_passthrough_doers.cc:3474`) performs **zero validation** on stride — it reads the value and calls ANGLE directly:

```
// Passthrough decoder — NO validation on stride
error::Error GLES2DecoderPassthroughImpl::DoVertexAttribPointer(
    GLuint indx, GLint size, GLenum type, GLboolean normalized,
    GLsizei stride, const void* ptr) {
  api()->glVertexAttribPointerFn(indx, size, type, normalized, stride, ptr);
  return error::kNoError;
}

```
### Patch 2: WebGL stride > 255 limit (validationES.cpp)

The stride ≤ 255 limit is WebGL spec validation enforced in the renderer process (Blink/ANGLE). A compromised renderer bypasses all renderer-side validation.

### Patch 3: Buffer bounds check (VertexDataManager.cpp)

A compromised renderer issues `glVertexAttribPointer` with `buffer=0` (no VBO bound), creating client-side vertex arrays. The buffer bounds check in `reserveSpaceForAttrib` (line 517) only runs when `bufferD3D != nullptr`:

```
if (bufferD3D)  // Skipped for client-side arrays (bufferD3D == nullptr)
{
    // bounds check here — NOT reached with client-side arrays
}

```

Client-side arrays bypass this check entirely, allowing the malformed stride to reach `storeVertexAttributes`.

## Data Flow (Compromised Renderer)

```
Compromised renderer → GPU command buffer shared memory: stride = 0xFFFFFFFC
  → Passthrough decoder: ZERO validation, calls ANGLE directly
  → ANGLE stores as GLuint mStride = 0xFFFFFFFC
  → ComputeVertexAttributeStride() returns size_t(0xFFFFFFFC)
  → VertexBuffer11.cpp:114: static_cast<int>(0xFFFFFFFC) = -4
  → Line 125: input += (-4) * start → pointer goes BACKWARD
  → Line 133: copyFunction reads OOB memory → HEAP BUFFER OVERFLOW

```
## Suggested Fix

Apply the same `CheckedNumeric` pattern used in the sibling fix ([b/489369089](https://issues.chromium.org/issues/489369089)):

```
--- a/src/libANGLE/renderer/d3d/d3d11/VertexBuffer11.cpp
+++ b/src/libANGLE/renderer/d3d/d3d11/VertexBuffer11.cpp
@@ -111,7 +111,9 @@
 {
     ASSERT(mBuffer.valid());

-    int inputStride = static_cast<int>(ComputeVertexAttributeStride(attrib, binding));
+    angle::CheckedNumeric<int> checkedInputStride = ComputeVertexAttributeStride(attrib, binding);
+    ANGLE_CHECK_GL_MATH(GetImplAs<ContextD3D>(context), checkedInputStride.IsValid());
+    int inputStride = checkedInputStride.ValueOrDie();

```
## Attached Files

- `poc.html` — Web PoC (HTML + WebGL)
- `web_poc_asan_output.txt` — Full ASAN output from content\_shell
- `validation_bypass.patch` — 3 patches to simulate compromised renderer
- `fix.patch` — Suggested fix (CheckedNumeric)
- `VertexBuffer11OverflowTest.cpp` — ANGLE standalone regression test
- `asan_output.txt` — ANGLE standalone ASAN output

#### Impact analysis

## Impact

The attacker (compromised renderer) controls three parameters:

- **stride** — direction and step size of pointer displacement
- **start** (`glDrawArrays` first) — multiplied with stride, controls total read offset
- **count** (`glDrawArrays` count) — controls volume of data read from OOB memory

This enables arbitrary read windows into the GPU process heap, which contains cross-origin rendering data, GPU command buffers, and D3D11 resource metadata from all renderer processes.

---

### The cause

#### What version of Chrome have you found the security issue in?

149.0.7810.0 (Chromium source at HEAD, built with ASAN. Vulnerable code confirmed present at ANGLE commit 3c125a0. The bug also affects current Chrome Stable on Windows — the vulnerable static\_cast<int> at VertexBuffer11.cpp:114 has ▎ not been patched in any release.)

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Memory Corruption

#### How would you like to be publicly acknowledged for your report?

Quac Tran

## Attachments

- [web_poc_asan_output.txt](attachments/web_poc_asan_output.txt) (text/plain, 3.8 KB)
- [fix.patch](attachments/fix.patch) (application/octet-stream, 799 B)
- [validation_bypass.patch](attachments/validation_bypass.patch) (application/octet-stream, 2.0 KB)
- [poc.html](attachments/poc.html) (text/html, 4.0 KB)

## Timeline

### tr...@gmail.com (2026-04-24)

For reference, CVE-2026-5281 (Use After Free in Dawn, CVSS 8.8 HIGH, CISA KEV) uses the exact same attack model: **compromised renderer → GPU process**, triggered via a crafted HTML page.

This bug is the same attack model, same process (GPU), different component (ANGLE D3D11 instead of Dawn). The passthrough command decoder performs zero validation on the stride parameter — a compromised renderer can pass any value directly to ANGLE, triggering the integer overflow in `VertexBuffer11::storeVertexAttributes`.

This is also a variant of [b/489369089](https://issues.chromium.org/issues/489369089), which was already fixed with `CheckedNumeric` in the sibling file `VertexDataManager.cpp` (commit 641c0d0). The identical `static_cast<int>` pattern in `VertexBuffer11.cpp:114` was missed.

### ca...@chromium.org (2026-04-24)

Passing to graphics folks for delegated triage

### pe...@google.com (2026-04-25)

Compromised renderer and limited use OOB read. At most s1. S2 is likely given similarity to other bug ([comment #2](https://issues.chromium.org/issues/506212452#comment2))

### ch...@google.com (2026-04-26)

Setting milestone because of s0/s1 severity.

### ge...@google.com (2026-04-29)

This should be fixed by both adding the WebGL stride validation to ANGLE and overflow validation in VertexDataManager.

### ge...@google.com (2026-04-29)

Nevermind, WebGL validation is done already [here](https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/validationES.cpp;l=1518;drc=3651f9e5dc60ded0e9141ca658e78c03f9428450). This vuln requires the compromised renderer to force a non-webgl context.

### sy...@chromium.org (2026-04-30)

Over to you Geoff since it's d3d/. I suspect the solution is to apply the validation for hardened contexts instead of webgl though, right?

### dx...@google.com (2026-05-05)

Project: angle/angle  

Branch:  main  

Author:  Zhenyao Mo [zmo@chromium.org](mailto:zmo@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7814021>

D3D11: Defend against potential integer overflow in a function.

---


Expand for full commit details
```
     
    VertexBuffer11::storeVertexAttributes(). 
     
    Also, added a regression test for this. 
     
    Bug: b/506212452 
    Change-Id: Id82847ef730287515e64a3836e3479fc208ed704 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7814021 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Auto-Submit: Zhenyao Mo <zmo@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/d3d/d3d11/VertexBuffer11.cpp`
- M `src/tests/gl_tests/VertexAttributeTest.cpp`

---

Hash: [13738a97e6a19fbaf280a9f9c67cfde5f714963e](https://chromiumdash.appspot.com/commit/13738a97e6a19fbaf280a9f9c67cfde5f714963e)  

Date: Mon May 4 19:37:02 2026


---

### aj...@google.com (2026-05-12)

-> medium as this is a read in the gpu

### sp...@google.com (2026-05-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Below baseline. User information disclosure


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/506212452)*
