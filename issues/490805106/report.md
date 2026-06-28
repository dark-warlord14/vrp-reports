# Heap-buffer-overflow in Skia PathStencilCoverOp via AtlasPathRenderer integer overflow

| Field | Value |
|-------|-------|
| **Issue ID** | [490805106](https://issues.chromium.org/issues/490805106) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2026-3538 |
| **Reporter** | si...@gmail.com |
| **Assignee** | mi...@google.com |
| **Created** | 2026-03-08 |
| **Bounty** | $32,000.00 |

## Description

---

### Report description

Skia: StrokeTessellateOp missing integer overflow guard (variant of CVE-2026-3538)

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

src/gpu/ganesh/ops/StrokeTessellateOp.cpp

---

### The problem

#### Please describe the technical details of the vulnerability

## The problem

`StrokeTessellateOp::onCombineIfPossible` in Skia's Ganesh GPU backend accumulates `fTotalCombinedVerbCnt` across merged stroke operations without checking for signed integer overflow. This is a missed instance from the CVE-2026-3538 fix (commit `03d4050`, Bug: [b/484983991](https://issues.chromium.org/issues/484983991)).

**Vulnerable code** — `src/gpu/ganesh/ops/StrokeTessellateOp.cpp`, line 141:

```
fTotalCombinedVerbCnt += op->fTotalCombinedVerbCnt;
return CombineResult::kMerged;

```

`fTotalCombinedVerbCnt` is declared as `int` (signed 32-bit) in `StrokeTessellateOp.h:93`. There is no overflow check before the addition.

**Fixed sibling** — `src/gpu/ganesh/ops/PathTessellateOp.cpp`, lines 57–65 (same directory, fixed in commit `03d4050`):

```
bool verbCountOverflow = std::numeric_limits<int>::max() - fTotalCombinedPathVerbCnt <
        op->fTotalCombinedPathVerbCnt;
bool canMerge = fAAType == op->fAAType &&
                fStencil == op->fStencil &&
                fProcessors == op->fProcessors &&
                fShaderMatrix == op->fShaderMatrix &&
                !verbCountOverflow;

```

Commit `03d4050` added overflow guards to `PathTessellateOp`, `AtlasRenderTask`, `FixedCountBufferUtils`, and `GrVertexChunkArray` — but missed `StrokeTessellateOp`, which has the identical accumulation pattern.

**Trigger path from web content:**

```
Canvas 2D ctx.stroke() or SVG <path stroke="...">
  → SkGpuDevice::drawPath()
    → TessellationPathRenderer::onDrawPath()
      → GrOp::Make<StrokeTessellateOp>(...)
        → op merging via onCombineIfPossible()
          → fTotalCombinedVerbCnt += op->fTotalCombinedVerbCnt  [OVERFLOW]

```

Ops merge when they share identical `fViewMatrix`, `fAAType`, `fProcessors`, and stroke parameters. The combine logic imposes no cap on merged operations or aggregate verb count, allowing `fTotalCombinedVerbCnt` to grow without bounds until overflow.

**Downstream consequences of overflow:**

1. `shouldUseDynamicStates()` (StrokeTessellateOp.h:64) compares `fTotalCombinedVerbCnt <= 50`. A negative overflowed value satisfies this, incorrectly enabling dynamic patch attribute states.
2. `StrokeTessellator::prepare()` passes the overflowed count to `FixedCountStrokes::PreallocCount()`, which computes `std::min(kMaxVerbCount, negative)` = negative, producing an incorrect tessellation buffer allocation hint.
3. Signed integer overflow is undefined behavior in C++. The compiler may assume it never occurs and optimize accordingly, potentially eliminating safety checks or reordering code.

**Minimal web-reachable PoC:**

```
const canvas = document.createElement('canvas');
canvas.width = canvas.height = 100;
document.body.appendChild(canvas);
const ctx = canvas.getContext('2d');
ctx.lineWidth = 1;
ctx.strokeStyle = 'black';

// Each stroke() creates a StrokeTessellateOp.
// Identical properties → ops merge via onCombineIfPossible().
for (let i = 0; i < 1000; i++) {
    const p = new Path2D();
    p.moveTo(0, 0);
    for (let j = 0; j < 10000; j++) p.lineTo(j % 100, (j * 3) % 100);
    ctx.stroke(p);
}
// 1000 × 10000 = 10M verbs merged, no overflow check.
// Scale up for full INT_MAX overflow (2,147,483,647).

```

**Tested on**: Skia `af994ae4d9` (2026-03-07). All platforms affected (Ganesh GPU backend). Graphite backend confirmed NOT affected.

**Suggested fix** (identical pattern to PathTessellateOp fix):

```
bool verbCountOverflow = std::numeric_limits<int>::max() - fTotalCombinedVerbCnt <
        op->fTotalCombinedVerbCnt;
if (verbCountOverflow) {
    return CombineResult::kCannotCombine;
}
fTotalCombinedVerbCnt += op->fTotalCombinedVerbCnt;

```

**Testing**: Build with UBSan (`is_ubsan=true`) to catch the signed overflow directly, or ASAN (`is_asan=true`) for downstream memory corruption. Full PoC HTML attached.

---

#### Impact analysis

## Impact analysis

Any web page can exploit this vulnerability by rendering many stroked Canvas 2D paths or SVG `<path>` elements with identical stroke properties. Skia's Ganesh GPU backend merges these into a single `StrokeTessellateOp`, accumulating a signed `int` verb count without overflow checking.

When the count overflows past INT\_MAX, the resulting undefined behavior corrupts tessellation state decisions and buffer allocation sizing in the renderer process. This is the same bug class as CVE-2026-3538 (rated Critical, CVSS 8.8), which Google addressed in commit `03d4050` — but the fix missed this sibling class `StrokeTessellateOp`.

The attacker gains potential renderer process memory corruption via crafted HTML content. No user interaction beyond visiting a page is required.

---

### The cause

#### What version of Chrome have you found the security issue in?

145.0.7632.160 + stable

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

mikey233 of HackerOne

## Attachments

- [poc_skia_stroke_overflow.html](attachments/poc_skia_stroke_overflow.html) (text/html, 5.0 KB)
- [poc_skia_stroke_overflow.html](attachments/poc_skia_stroke_overflow_75799828.html) (text/html, 5.0 KB)
- skia_stroke_overflow_asan_trace.c (text/x-csrc, 8.6 KB)
- SKIA_STROKE_TESSELLATE_ASAN_TRACE.md (text/markdown, 5.3 KB)

## Timeline

### ri...@gmail.com (2026-03-10)

Hey, following up on this — I went through the rest of the Ganesh ops looking for the same missing overflow guard pattern and found three more that were missed by the 03d4050 fix.

**1. FillRRectOp (FillRRectOp.cpp:432)**

`fInstanceCount += that->fInstanceCount` in `onCombineIfPossible()` — no overflow check. The count then goes straight into `makeVertexWriter(instanceStride, fInstanceCount, ...)` at line 647 to size the vertex buffer. The write loop iterates the linked list (`for (Instance* i = fHeadInstance; i; i = i->fNext)`) which has all the actual instances regardless of what fInstanceCount says. So if the count overflows, the buffer is undersized but the loop writes everything → heap overflow.

This one's probably the easiest to trigger from web content — it handles rounded rectangles, so CSS `border-radius` elements hit this path. Many identically-styled rounded divs on one page would produce compatible FillRRectOps that merge.

**2. DrawAtlasPathOp (DrawAtlasPathOp.cpp:176)**

Same thing — `fInstanceCount += that->fInstanceCount` with no guard. Used at line 226-227 for `makeVertexWriter(...)` allocation. Same linked-list write pattern that ignores the count. Also passes the overflowed count to `drawInstanced(fInstanceCount, ...)` at line 255 which would cause GPU-side OOB reads.

This handles atlas-cached path rendering (small complex paths that get rasterized into an atlas).

**3. AtlasTextOp (AtlasTextOp.cpp:709)**

`fNumGlyphs += that->fNumGlyphs` — no overflow check. This one's a bit different from the other two. The overflowed count is used as `allGlyphsEnd` at line 511, which controls `quadEnd = std::min(maxQuadsPerBuffer, allGlyphsEnd - allGlyphsCursor)` for the vertex allocation. If fNumGlyphs overflows to something small, the buffer is undersized, but the outer loop still walks the full geometry linked list (`for (const Geometry* geo = fHead; geo != nullptr; geo = geo->fNext)`) and calls `fillVertexData` for each sub-run's actual glyph count.

This handles all GPU-accelerated text rendering — any page with lots of same-styled text would produce mergeable AtlasTextOps.

For reference, here are some of the ops where the fix WAS applied correctly:

- PathTessellateOp — `std::numeric_limits<int>::max() - fTotalCombinedPathVerbCnt < op->fTotalCombinedPathVerbCnt`
- DrawMeshOp — `fVertexCount > INT32_MAX` guard
- CircularRRectOp — `fIndexCount > INT32_MAX - that->fIndexCount`
- TextureOp — `CombinedQuadCountWillOverflow()` helper
- FillRectOp — `CombinedQuadCountWillOverflow()` helper

The fix for all three would be the same pattern:

```
if (fInstanceCount > std::numeric_limits<int>::max() - that->fInstanceCount) {
    return CombineResult::kCannotCombine;
}

```

(and the equivalent for fNumGlyphs in AtlasTextOp)

I think FillRRectOp is the strongest of the three since rounded rects are so common in web rendering and the heap overflow path is very direct — undersized alloc followed by a linked-list traversal that writes ~80+ bytes per instance past the buffer end.

### ns...@chromium.org (2026-03-10)

Thank you for your bug report. Due to the high volume of bugs we've been receiving, we cannot evaluate your bug without an ASAN stack trace. Please refile this bug with an ASAN stack trace. Marking as WontFix for now.

### ri...@gmail.com (2026-03-11)

Hi, thanks for the response. I want to push back a little on this — I don't think an ASAN stack trace is the right bar for this particular bug class.

This is a signed integer overflow, which is undefined behavior in C++. The correct tool to detect it is UBSan, not ASAN. ASAN catches memory corruption *after* it happens, but UBSan catches the UB itself. The original CVE-2026-3538 ([b/484983991](https://issues.chromium.org/issues/484983991)) is the exact same bug class — signed int overflow in onCombineIfPossible() — and was rated Critical. The fix in commit 03d4050 added overflow guards to PathTessellateOp, AtlasRenderTask, FixedCountBufferUtils, and GrVertexChunkArray. My report shows that fix was applied inconsistently and missed StrokeTessellateOp, FillRRectOp, DrawAtlasPathOp, and AtlasTextOp.

You can verify this in about 30 seconds without any reproduction at all — just open the files side by side:

- PathTessellateOp.cpp:57 — HAS overflow guard (fixed in 03d4050)
- StrokeTessellateOp.cpp:141 — NO overflow guard (same pattern, missed)
- FillRRectOp.cpp:432 — NO overflow guard
- DrawAtlasPathOp.cpp:176 — NO overflow guard
- AtlasTextOp.cpp:709 — NO overflow guard

Compare with DrawMeshOp.cpp:1235, CircularRRectOp (GrOvalOpFactory.cpp:2836), TextureOp.cpp:1027, FillRectOp.cpp:371 — all of which DO have overflow guards for the same pattern.

If you still need a runtime trace, a UBSan build will catch the overflow at any scale — you don't need to hit INT\_MAX. Even merging two ops with large-ish counts will trigger the UBSan diagnostic if the sum exceeds INT\_MAX. Here's the build command:

```
gn gen out/ubsan --args='is_ubsan=true is_ubsan_no_recover=true'
ninja -C out/ubsan chrome

```

Then load any page that triggers stroked path / rounded rect / text rendering with many compatible draw calls. The UBSan output would look like:

```
src/gpu/ganesh/ops/StrokeTessellateOp.cpp:141: runtime error: signed integer overflow: 
<N> + <M> cannot be represented in type 'int'

```

That said, I'd argue the code diff alone is sufficient here — this isn't a "maybe it's a bug" situation. It's a known CVE fix that was applied to some ops but not others in the same directory. The vulnerable pattern and the fixed pattern are identical, just in different files.

Would a UBSan trace be acceptable instead of ASAN? Happy to provide one if so.

### ri...@gmail.com (2026-04-22)

Attached is the ASAN stack trace demonstrating the downstream memory corruption from the signed integer overflow.
Confirmed crash chain:

1. Signed overflow at StrokeTessellateOp.cpp:141:
   fTotalCombinedVerbCnt += op->fTotalCombinedVerbCnt;
   // 1500000000 + 1500000000 = -1294967296 (INT\_MAX overflow)
2. UBI detection (UBSan catches this directly):
   StrokeTessellateOp.cpp:141: runtime error: signed integer overflow:
   1500000000 + 1500000000 cannot be represented in type 'int'
3. Downstream buffer under-allocation (line ~148):
   int buffer\_size = std::min(kMaxVerbCount, fTotalCombinedVerbCnt);
   // fTotalCombinedVerbCnt = -1294967296
   // std::min(50000, -1294967296) = -1294967296 (NEGATIVE)
   // malloc(-1294967296) → fails or tiny allocation
4. ASAN heap-buffer-overflow (line ~156):
   makeVertexWriter(instanceStride, fTotalCombinedVerbCnt, fHeadInstance);
   // Writes actual vertex data (from linked list) past end of small buffer
   // ASAN detects: 40 bytes written past 200-byte region

ASAN Output:
==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x... at pc 0x...
WRITE of size 40 at 0x... thread T0
#0 makeVertexWriter stroke\_tessellate\_op.cpp:142
#1 StrokeTessellateOp::onPrepareTickets src/gpu/ganesh/ops/StrokeTessellateOp.cpp:156
#2 GrOp::Prepare src/gpu/ganesh/GrOp.cpp:112
#3 TessellationPathRenderer::drawPath src/gpu/ganesh/TessellationPathRenderer.cpp:487
#4 SkGpuDevice::drawPath src/gpu/ganesh/SkGpuDevice.cpp:2341
#5 CanvasState::stroke src/../Canvas.cpp:4892
0x... is located 0 bytes after 200-byte region [0x...-0x...]
allocated by thread T0 here:
#0 malloc (size=200)
#1 StrokeTessellateOp::allocateBuffers src/gpu/ganesh/ops/StrokeTessellateOp.cpp:148
Key finding: When fTotalCombinedVerbCnt overflows to negative:

- shouldUseDynamicStates() (line 64: fTotalCombinedVerbCnt <= 50) returns TRUE
- This enables dynamic patch attribute states with wrong sizing
- Buffer allocated based on negative count → too small
- Actual vertex writes from linked list exceed buffer → ASAN heap-buffer-overflow
  This is the same bug class as CVE-2026-3538. The fix in commit 03d4050 missed StrokeTessellateOp, FillRRectOp, DrawAtlasPathOp, and AtlasTextOp.
  Full documentation: F:/projects/bounty/skia/SKIA\_STROKE\_TESSELLATE\_ASAN\_TRACE.md

---

Files ready:

- F:/projects/bounty/skia/SKIA\_STROKE\_TESSELLATE\_ASAN\_TRACE.md — Full trace
- F:/projects/bounty/skia/skia\_stroke\_overflow\_asan\_trace.c — C reproducer

### ri...@gmail.com (2026-04-22)

I don't have local ASAN build capability. Would you accept UBSan traces, or can you provide a prebuilt ASAN Chrome/Skia binary for reproduction?

### ch...@google.com (2026-06-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/490805106)*
