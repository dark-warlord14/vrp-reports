# [PassAsSpan] ArrayBuffer.transfer() re-entrancy UAF / SEGV in TextDecoder.decode

| Field | Value |
|-------|-------|
| **Issue ID** | [491518619](https://issues.chromium.org/issues/491518619) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>TextEncoding |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | pk...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2026-03-11 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

1. Save the two attached PoC HTML files
2. Serve via HTTP: python -m http.server 8899
3. Open webgl2-passasspan-uaf-v4.html in Chrome
4. Observe output: "UAF DETECTED" with R=252 (spray value) instead of R=3 (original value)
5. Open webgl2-passasspan-infoleak-v1.html for 32-bit precision info leak confirmation

Tested on: Chrome Dev 147.0.7726.0 (ASAN build, 64-bit, v8\_enable\_sandbox=true, Windows 11)

PoC 1 mechanism (webgl2-passasspan-uaf-v4.html):

- Allocates Float32Array(4096) filled with 0.01
- Calls gl.uniform1fv(loc, data, evilSrcOffset, 64)
- evilSrcOffset is an object with valueOf() that:
  (a) Detaches the buffer via data.buffer.transfer(0)
  (b) Sprays freed memory with ArrayBuffers filled with 0.99
- PassAsSpan already captured a raw pointer without retaining the backing store
  (kSupportReentry=false due to [NoAllocDirectCall])
- The dangling span reads spray value 0.99 instead of original 0.01
- readPixels confirms R=252 (from 0.99) instead of R=3 (from 0.01)

PoC 2 mechanism (webgl2-passasspan-infoleak-v1.html):

- Same UAF trigger, sprays known float patterns into freed memory
- Vertex shader reads u\_data[gl\_VertexID] and outputs via Transform Feedback varying
- getBufferSubData extracts exact IEEE 754 float bit patterns from freed memory
- 30/30 attempts: 64/64 values exact-matched (0 ULP error), 256 bytes per call

Reproduction rate: 20/20 (PoC 1), 30/30 (PoC 2) — 100%
ASAN does NOT detect this UAF — see problem description.

# Problem Description

INCOMPLETE FIX FOR [BUG 484946544](https://issues.chromium.org/issues/484946544): USE-AFTER-FREE IN 31 WEBGL2/WEBGPU FUNCTIONS

[Bug 484946544](https://issues.chromium.org/issues/484946544) fixed TextDecoder.decode() PassAsSpan UAF by setting kSupportReentry=true for that function. However the root cause in the bindings generator was not corrected.

ROOT CAUSE (blink\_v8\_bridge.py:506):
support\_reentry = "NoAllocDirectCall" not in argument.owner.extended\_attributes

This sets kSupportReentry=false for ALL [NoAllocDirectCall] functions. When false, PassAsSpan's MaybeSetBackingStore() is a no-op — the backing store shared\_ptr is NOT retained. Only a raw pointer+size span is stored.

A TODO(caseq) at line 504 acknowledges this gap but only mentions "strings, dicts" — not numeric params (GLuint,GLintptr) that accept objects with valueOf().

TRIGGER: When srcOffset is a JS object (not a number), V8 cannot use the fast API path and falls to the slow path.
During slow-path parameter conversion, valueOf() is called AFTER the span is already captured. valueOf() detaches the buffer → span becomes dangling.

ASAN DETECTION BYPASS (SYSTEMIC):
gin/array\_buffer.cc (lines 54, 67) allocates and frees AB backing stores with kNoMemoryToolOverride when V8\_ENABLE\_SANDBOX is enabled (default). This bypasses ASAN quarantine/poisoning entirely. ClusterFuzz cannot detect ANY ArrayBuffer backing store lifetime bug.

AFFECTED FUNCTIONS (31):
WebGL2 (24): uniform{1,2,3,4}{f,i,ui}v (12), uniformMatrix{2,3,4,2x3,3x2,2x4,4x2,3x4,4x3}fv (9), clearBuffer{i,ui,f}v(3)
WebGL Multi-Draw (6): multiDraw{Arrays,Elements}{,Instanced}WEBGL + 2 base vertex/instance variants
WebGPU (1): GPUProgrammablePassEncoder.setBindGroup

All use [NoAllocDirectCall] + PassAsSpan (via Float32List/Int32List/Uint32List typedefs or direct [PassAsSpan] annotation) with post-span numeric parameters.

SECURITY IMPACT:

1. Read-after-free with offset control (valueOf return), size control (AB size selects PA bucket), 32-bit precision(Transform Feedback)
2. PartitionAlloc freelist metadata exposure from unsprayed freed slots
3. ASAN-invisible bug class affecting all AB backing store UAFs
4. Systemic generator flaw: future [NoAllocDirectCall]+[PassAsSpan] functions auto-vulnerable

Note: AB backing stores are in PA's Buffer Partition (ConfigurablePool), isolated from Blink DOM and V8 heap.

SUGGESTED FIX:
In blink\_v8\_bridge.py:506, set kSupportReentry=true when any post-span argument can trigger JS re-entry(valueOf/toString), not just when [NoAllocDirectCall] is absent.

# Additional Comments

This is a variant of [bug 484946544](https://issues.chromium.org/issues/484946544). The fix (CL 7595948, commit ec1a6357e246a) added kSupportReentry for PassAsSpan but uses [NoAllocDirectCall] as the sole heuristic, missing 31 functions where post-span numeric parameters accept valueOf() objects.

Fix CL: <https://chromium-review.googlesource.com/c/chromium/src/+/7595948>

The ASAN evasion via kNoMemoryToolOverride is a systemic issue — all ArrayBuffer backing store lifetime bugs are invisible to ClusterFuzz.

Build config:
is\_asan = true, v8\_enable\_sandbox = true
is\_component\_build = false, dcheck\_always\_on = false

2 PoC files attached:
webgl2-passasspan-uaf-v4.html — data substitution (readPixels)
webgl2-passasspan-infoleak-v1.html — info leak (Transform Feedback, 32-bit)

# Summary

UAF in 31 WebGL2/WebGPU funcs via PassAsSpan+NoAllocDirectCall (incomplete fix for 484946544)

# Custom Questions

#### Type of crash:

no crash occurs. The UAF silently reads freed memory without triggering any error.

#### Crash state:

ASAN does not detect this. gin/array\_buffer.cc uses kNoMemoryToolOverride for AB backing store alloc/free under V8\_ENABLE\_SANDBOX, bypassing ASAN instrumentation entirely. No crash, no ASAN report, no error logged.

#### Reporter credit:

D3LV

# Additional Data

Category: Security   

Chrome Channel: Dev   

Regression: N/A \

## Attachments

- [webgl2-passasspan-infoleak-v1.html](attachments/webgl2-passasspan-infoleak-v1.html) (text/html, 22.2 KB)
- [webgl2-passasspan-uaf-v4.html](attachments/webgl2-passasspan-uaf-v4.html) (text/html, 10.4 KB)
- [chrome-asan-uaf-trace.txt](attachments/chrome-asan-uaf-trace.txt) (text/plain, 19.8 KB)
- [chrome-asan-uaf-trace.txt](attachments/chrome-asan-uaf-trace_74232108.txt) (text/plain, 54.5 KB)

## Timeline

### th...@chromium.org (2026-03-11)

[security shepherd] <https://bughunters.google.com/about/rules/chrome-friends/chrome-vulnerability-reward-program-rules#report-formatting-attachments> notes that reports must have a trace attached.

### d3...@gmail.com (2026-03-12)

Attaching the ASAN trace. The initial report was tested against a build with v8\_enable\_sandbox=true, which uses kNoMemoryToolOverride and prevents ASAN from instrumenting ArrayBuffer allocations. Rebuilding with v8\_enable\_sandbox=false produces the attached heap-use-after-free report.

### d3...@gmail.com (2026-03-12)

Apologies, forgot to attach the symbolized version. rebuilding with llvm-symbolizer attached gives full function names. Re-attaching chrome-asan-uaf-trace.txt.

### ch...@google.com (2026-06-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2026-06-18)

This issue has been closed as an incomplete or invalid report and we will not respond to further comments. If you can improve your report please open a fresh issue that addresses any feedback provided.

For more information on our vulnerability policies, please refer to <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md>

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/491518619)*
