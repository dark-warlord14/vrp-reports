# Integer truncation in ANGLE D3D11 VertexDataManager leads to heap OOB read from compromised renderer on Windows

| Field | Value |
|-------|-------|
| **Issue ID** | [505676335](https://issues.chromium.org/issues/505676335) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | je...@gmail.com |
| **Assignee** | am...@google.com |
| **Created** | 2026-04-23 |
| **Bounty** | $3,000.00 |

## Description

---

### Report description

Integer Overflow to OOB Heap Read in GPU Process

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

Compromised renderer -> GPU process

---

### The problem

#### Please describe the technical details of the vulnerability

## Root Cause

`VertexBuffer11::storeVertexAttributes` truncates a `size_t` stride to `int` via `static_cast<int>`. When the stride exceeds `INT_MAX`, it wraps to a negative value. This negative stride is then used in pointer arithmetic, causing the read pointer to move backward past the buffer allocation.

```
// VertexBuffer11.cpp:114 — VULNERABLE
int inputStride = static_cast<int>(ComputeVertexAttributeStride(attrib, binding));
// ...
// Line 125 — OOB pointer arithmetic
input += inputStride * start;  // negative stride * start → pointer goes BACKWARD
// Line 133 — reads from OOB memory
vertexFormatInfo.copyFunction(input, inputStride, count, output);

```
## Sibling Fix (not applied to this file)

The identical pattern was already fixed in `VertexDataManager.cpp` (commit `641c0d0`, bug `b/489369089`):

```
// VertexDataManager.cpp — FIXED
-const int offset = static_cast<int>(ComputeVertexAttributeOffset(attrib, binding));
+angle::CheckedNumeric<GLintptr> offset = ComputeVertexAttributeOffset(attrib, binding);

```

**The fix was NOT applied to `VertexBuffer11.cpp`.** The `static_cast<int>` truncation remains.

## Data Flow

```
Renderer command buffer shared memory: stride field = int32_t
  → Passthrough decoder: reads as GLsizei (int), NO validation
  → ANGLE entry point: GL_VertexAttribPointer(stride = -1)
  → ANGLE stores as GLuint: mStride = 0xFFFFFFFF (4294967295)
  → ComputeVertexAttributeStride() returns size_t = 4294967295
  → VertexBuffer11.cpp:114: static_cast<int>(4294967295) = -1
  → Line 125: input += (-1) * start → pointer goes BACKWARD
  → Line 133: copyFunction reads from before the buffer → OOB HEAP READ

```
## Why Validation is Bypassed

1. **WebGL validation (renderer process):** Limits stride to 255 bytes. A compromised renderer bypasses this by writing directly to command buffer shared memory.
2. **Passthrough command decoder:** On Windows, `UsePassthroughCommandDecoder() = true`. The passthrough decoder's `DoVertexAttribPointer` performs ZERO validation on stride — passes it directly to ANGLE.
3. **ANGLE validation:** `IsANGLEValidationEnabled()` returns `false` in production Chrome. `EGL_CONTEXT_OPENGL_NO_ERROR_KHR = EGL_TRUE`. All ANGLE validation is SKIPPED.
4. **Client-side array path reachable from command decoder:** A compromised renderer can issue `glVertexAttribPointer` with `buffer=0` (no VBO bound) and an arbitrary pointer value. The passthrough decoder forwards this directly to ANGLE, which interprets it as a client-side vertex array. This forces the streaming path through `VertexBuffer11::storeVertexAttributes`, bypassing the buffer bounds checks in `VertexDataManager::reserveSpaceForAttrib` (which only validate when `bufferD3D != nullptr`).

## Why Windows Only

- `angle_enable_d3d11 = is_win` — D3D11 backend only compiles on Windows
- D3D11 is the DEFAULT ANGLE backend on Windows Chrome
- Linux/Android use Vulkan or GL backends (both use `size_t`, not `int`)
- D3D9 backend uses `size_t` (no truncation — safe)

## PoC

See `VertexBuffer11OverflowTest.cpp` — an ANGLE end2end test that reproduces the bug.

The PoC uses:

- **Client-side vertex arrays** to bypass `VertexDataManager` buffer bounds checks (which were fixed separately). Client arrays always go through the streaming path via `storeVertexAttributes`.
- **No-error context** (`setNoErrorEnabled(true)`) to skip ANGLE's `glVertexAttribPointer` stride validation, matching production Chrome behavior.
- `glVertexAttribPointer(stride = -1)` — stored as `GLuint(0xFFFFFFFF)`, wraps to `-1` on `static_cast<int>`.
- `glDrawArrays(GL_TRIANGLES, first=1, count=3)` — `first=1` triggers `input += (-1) * 1`, moving the pointer 1 byte before the heap allocation.

### Build & Run

```
# Prerequisites: Visual Studio 2022 Build Tools, Windows SDK, depot_tools

# 1. Fetch ANGLE source
mkdir angle && cd angle
set DEPOT_TOOLS_WIN_TOOLCHAIN=0
fetch angle
gclient sync

# 2. Copy PoC test into the tree
copy VertexBuffer11OverflowTest.cpp src\tests\gl_tests\
# Add "gl_tests/VertexBuffer11OverflowTest.cpp" to src/tests/angle_end2end_tests.gni

# 3. Build with ASAN
gn gen out/AsanWin --args="is_asan=true is_component_build=true is_debug=false dcheck_always_on=true"
ninja -C out/AsanWin angle_end2end_tests

# 4. Run PoC
set ASAN_OPTIONS=detect_leaks=0:symbolize=1
out\AsanWin\angle_end2end_tests.exe --gtest_filter="*VertexBuffer11Overflow*" --use-angle=d3d11

```
### ASAN Output (actual crash)

```
==37328==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x123b50e23bbf
READ of size 1 at 0x123b50e23bbf thread T0
    #0 rx::GetAlignedOffsetInput<float,4>       copyvertex.inc.h:43
    #1 rx::CopyNativeVertexData<float,4,4,0>    copyvertex.inc.h:80
    #2 rx::VertexBuffer11::storeVertexAttributes VertexBuffer11.cpp:133
    #3 rx::StreamingVertexBufferInterface::storeDynamicAttribute VertexBuffer.cpp:206
    #4 rx::VertexDataManager::storeDynamicAttrib VertexDataManager.cpp:591
    #5 rx::VertexDataManager::storeDynamicAttribs VertexDataManager.cpp:462
    #6 rx::VertexArray11::updateDynamicAttribs   VertexArray11.cpp:330
    #7 rx::VertexArray11::syncStateForDraw       VertexArray11.cpp:163
    #8 rx::StateManager11::updateState           StateManager11.cpp:2001
    #9 rx::Context11::drawArrays                 Context11.cpp:285
    #10 GL_DrawArrays                            entry_points_gles_2_0_autogen.cpp:1819
    #11 VertexBuffer11OverflowTest_NegativeStrideOverflow_Test::TestBody
         VertexBuffer11OverflowTest.cpp:76

0x123b50e23bbf is located 1 bytes BEFORE 256-byte region [0x123b50e23bc0,0x123b50e23cc0)

```
## Suggested Fix

Apply the same `CheckedNumeric` pattern used in the sibling fix:

```
--- a/src/libANGLE/renderer/d3d/d3d11/VertexBuffer11.cpp
+++ b/src/libANGLE/renderer/d3d/d3d11/VertexBuffer11.cpp
@@ -111,7 +111,9 @@ angle::Result VertexBuffer11::storeVertexAttributes(...)
 {
     ASSERT(mBuffer.valid());

-    int inputStride = static_cast<int>(ComputeVertexAttributeStride(attrib, binding));
+    angle::CheckedNumeric<int> inputStride = ComputeVertexAttributeStride(attrib, binding);
+    ANGLE_CHECK_GL_MATH(GetImplAs<ContextD3D>(context), inputStride.IsValid());
+    int inputStrideValue = inputStride.ValueOrDie();

     // This will map the resource if it isn't already mapped.
     ANGLE_TRY(mapResource(context));
@@ -122,12 +124,12 @@ angle::Result VertexBuffer11::storeVertexAttributes(...)

     if (instances == 0 || binding.getDivisor() == 0)
     {
-        input += inputStride * start;
+        input += inputStrideValue * start;
     }

     // ...
-    vertexFormatInfo.copyFunction(input, inputStride, count, output);
+    vertexFormatInfo.copyFunction(input, inputStrideValue, count, output);

     return angle::Result::Continue;
 }

```
#### Impact analysis

## Attacker Capabilities

The attacker (compromised renderer) has full control over three parameters that determine the OOB read:

- **`stride`** — controls the direction and step size of the pointer displacement. Any negative value (via integer overflow) moves the read pointer backward into preceding heap allocations.
- **`start` (glDrawArrays `first`)** — multiplied with stride, controls total read offset. `offset = stride * start`, so `stride = -1, start = 4096` reads 4KB before the buffer.
- **`count` (glDrawArrays `count`)** — controls how many vertices are copied, determining the total volume of data read from OOB memory.

This means the read is not limited to a 1-byte underflow. The attacker can craft arbitrary read windows into the GPU process heap:

| stride | start | Read offset | Read volume (4-component float) |
| --- | --- | --- | --- |
| -1 | 1 | -1 byte | 16 bytes per vertex |
| -16 | 100 | -1,600 bytes | 16 \* count bytes |
| -256 | 1000 | -256,000 bytes | 16 \* count bytes |

### What Lives in the GPU Process Heap

The GPU process heap contains security-sensitive data from all renderer processes and all origins:

- **Cross-origin rendering data:** Texture contents, framebuffer data, and vertex data from other tabs and origins. A compromised renderer reading GPU heap can extract pixels rendered by other origins — effectively bypassing the same-origin policy for visual content.
- **GPU command buffers:** Serialized GL commands from other renderers, potentially containing pointers, offsets, and resource handles that reveal GPU process memory layout (useful for further exploitation).
- **D3D11 resource metadata:** Internal ANGLE and D3D11 data structures including mapped buffer pointers, device context state, and shader compilation artifacts.
- **IPC shared memory mappings:** Pointers and metadata for shared memory regions used for cross-process communication.

---

### The cause

#### What version of Chrome have you found the security issue in?

Version: Chrome 147.0.7727.117 (Stable, Windows)

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Memory Corruption

#### How would you like to be publicly acknowledged for your report?

Quac Tran

## Attachments

- [VertexBuffer11OverflowTest.cpp](attachments/VertexBuffer11OverflowTest.cpp) (text/plain, 4.3 KB)
- [asan_output.txt](attachments/asan_output.txt) (text/plain, 3.8 KB)
- fix.patch (text/x-diff, 799 B)

## Timeline

### ns...@chromium.org (2026-04-23)

Tests are not indicative of memory corruption on Chrome. Please reproduce your issue with a web PoC, not a test.

### tr...@gmail.com (2026-04-23)

This is the exact same bug class that was already acknowledged and fixed in the sibling file:

- **Commit:** <https://chromium.googlesource.com/angle/angle/+/641c0d0>
- **Code review:** <https://chromium-review.googlesource.com/c/angle/angle/+/7736785>
- **Bug:** [b/489369089](https://issues.chromium.org/issues/489369089)
- **Title:** "D3D11: Fix potential OOB read in StoreStaticAttrib"
- **File fixed:** `VertexDataManager.cpp` — replaced `static_cast<int>` with `CheckedNumeric<int>`

The unfixed code in `VertexBuffer11.cpp:114` is identical to what was fixed:

```
// VertexBuffer11.cpp:114 — UNFIXED
int inputStride = static_cast<int>(ComputeVertexAttributeStride(attrib, binding));

// VertexDataManager.cpp — FIXED (commit 641c0d0)
angle::CheckedNumeric<GLintptr> offset = ComputeVertexAttributeOffset(attrib, binding);

```

The `storeVertexAttributes` path is reachable via client-side vertex arrays, which bypass the buffer bounds checks in `VertexDataManager::reserveSpaceForAttrib` (those only validate when `bufferD3D != nullptr`).

On Windows, `UsePassthroughCommandDecoder() = true` and `IsANGLEValidationEnabled() = false` in production Chrome. There is no validation layer between the command buffer and the vulnerable `static_cast<int>`.

The ASAN test I provided reproduces the exact code path used by Chrome's D3D11 backend. The heap-buffer-overflow crash is at `VertexBuffer11.cpp:133`, confirming memory corruption.

Could you please re-evaluate this as a variant of [b/489369089](https://issues.chromium.org/issues/489369089) — same bug class, same subsystem, same fix pattern, just in the file that was missed?

### ch...@google.com (2026-04-23)

This issue has been closed as an incomplete or invalid report and we will not respond to further comments. If you can improve your report please open a fresh issue that addresses any feedback provided.

For more information on our vulnerability policies, please refer to <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md>

### ch...@google.com (2026-07-31)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/505676335)*
