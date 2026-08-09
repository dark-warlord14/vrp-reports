# V8 Sandbox Bypass: Compiler-Eliminated CPT Tag Check

| Field | Value |
|-------|-------|
| **Issue ID** | [500771385](https://issues.chromium.org/issues/500771385) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | qw...@gmail.com |
| **Assignee** | ml...@google.com |
| **Created** | 2026-04-08 |
| **Bounty** | $20,000.00 |

## Description

---

### Report description

V8 Sandbox Bypass: Compiler-Eliminated CPT Tag Check

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/v8/v8>

---

### The problem

#### Please describe the technical details of the vulnerability

## The problem

### Summary

Each Blink wrapper class is assigned a unique CPT tag by the IDL compiler. When JavaScript calls a method on a wrapper object, `ReadCppHeapPointerField()` extracts the C++ pointer from the CppHeapPointerTable and is supposed to validate the tag before returning it. If the tag doesn't match, the function returns `nullptr`, and the caller is expected to crash on the subsequent dereference.

The problem is that Clang sees through this. Chromium is built with `-fno-delete-null-pointer-checks` (`build/config/compiler/BUILD.gn`, enabled when `!is_ubsan && is_clang`). This flag makes null dereference a defined trap (noreturn) rather than undefined behavior. Ironically, the compiler now exploits the *defined* trap semantics: in the majority of generated binding callbacks, the unwrapped pointer is immediately dereferenced for a single member function call, with no other observable side effects on the null path. Since the null dereference is a guaranteed noreturn trap, the compiler concludes that the `entry = 0` branch always leads to a trap — making the entire tag check dead code. It removes it.

In release Chrome, the majority of CPT unwrap sites have no tag check. An attacker who can overwrite 4 bytes within the sandbox (the CPT handle at offset +12 of any wrapper) can swap the handle of one type for another. The binding layer extracts the wrong C++ pointer and calls the wrong type's methods on it. The C++ objects live on the Oilpan heap, which is outside the V8 sandbox. We have confirmed that this allows reading out-of-sandbox C++ memory through JavaScript APIs (Test 2) and controlling the specific values read by manipulating the donor object's JavaScript-accessible fields (Test 3). PoC demonstrates that this leads to a full arbitrary address write (AAW) primitive over out-of-sandbox memory, with both the write target and write value controlled from JavaScript.

### Chrome Version

Chromium 148.0.7766.3 (Linux x86\_64), sbx-testing build. Also Chrome 146.0.7680.177 stable (release).

### Root Cause

#### The Tag Check (v8-sandbox.h)

```
// v8-sandbox.h (ReadCppHeapPointerField)
uint32_t actual_tag = static_cast<uint16_t>(entry);
uint32_t first_tag = static_cast<uint32_t>(tag_range.first) << kTagShift;
uint32_t last_tag = (static_cast<uint32_t>(tag_range.last) << kTagShift) + 1;
if (V8_LIKELY(actual_tag >= first_tag && actual_tag <= last_tag)) {
    entry = entry >> kCppHeapPointerPayloadShift;  // Extract the C++ pointer
} else {
    entry = 0;  // Tag mismatch → return nullptr
}
return reinterpret_cast<T*>(entry);

```

On tag match, the upper 48 bits are extracted as the pointer. On mismatch, `nullptr` is returned. This design assumes the caller will crash on the null dereference, but it doesn't account for how the compiler reasons about that crash.

#### Per-Type Tags Are Genuinely Different

The IDL compiler assigns each Blink interface a unique tag at build time. Here are the tags for the types involved in this report, taken directly from the generated headers in the sbx-testing build:

```
// v8_canvas_rendering_context_2d.h (generated)
static constexpr v8::CppHeapPointerTag kThisTag =
    static_cast<v8::CppHeapPointerTag>(1105);
static constexpr v8::CppHeapPointerTagRange kTagRange =
    v8::CppHeapPointerTagRange(kThisTag, kThisTag);  // [1105, 1105]

// v8_dom_matrix.h (generated)
static constexpr v8::CppHeapPointerTag kThisTag =
    static_cast<v8::CppHeapPointerTag>(886);
static constexpr v8::CppHeapPointerTagRange kTagRange =
    v8::CppHeapPointerTagRange(kThisTag, kThisTag);  // [886, 886]

```

CanvasRenderingContext2D's tag (1105) is nowhere near DOMMatrix's (886). A working tag check would reject this swap. But the tag check is not there.

#### How the Compiler Eliminates the Check

Consider the generated binding for `Canvas2D.getContextAttributes()`:

```
// v8_canvas_rendering_context_2d.cc (generated)
void GetContextAttributesOperationCallback(
    const v8::FunctionCallbackInfo<v8::Value>& info) {
  // ...
  CanvasRenderingContext2D* blink_receiver =
      V8CanvasRenderingContext2D::ToWrappableUnsafe(isolate, v8_receiver);
  auto&& return_value = blink_receiver->getContextAttributes();
  v8::Local<v8::Value> v8_return_value =
      ToV8Traits<CanvasRenderingContext2DSettings>::ToV8(
          script_state, return_value);
  bindings::V8SetReturnValue(info, v8_return_value);
}

```

`ToWrappableUnsafe()` calls `Object::Unwrap()`, which calls `ReadCppHeapPointerField()` with `kTagRange = [1105, 1105]`. If the tag check returns `nullptr`, the very next thing that happens is `blink_receiver->getContextAttributes()`, a member function call through a null pointer. Under `-fno-delete-null-pointer-checks`, this is a defined trap (noreturn). No other observable side effect exists on the null path. LLVM concludes the `entry = 0` branch is dead and eliminates it.

The same applies to `lineWidth`, `globalAlpha`, and the majority of callbacks in the Canvas2D binding file:

```
// v8_canvas_rendering_context_2d.cc (generated)
void LineWidthAttributeGetCallback(
    const v8::FunctionCallbackInfo<v8::Value>& info) {
  // ...
  CanvasRenderingContext2D* blink_receiver =
      V8CanvasRenderingContext2D::ToWrappableUnsafe(isolate, v8_receiver);
  auto&& return_value = blink_receiver->lineWidth();
  bindings::V8SetReturnValue(info, return_value,
      bindings::V8ReturnValue::PrimitiveType<double>());
}

```

`blink_receiver` is used only for `->lineWidth()`, then discarded. Same optimization, same elimination.

#### When the Check Survives

When `blink_receiver` is passed to an opaque function—one whose body the compiler cannot see—it can no longer prove that the null path leads to a trap. The most common case is binding callbacks that return wrapper objects:

```
// v8_canvas_rendering_context_2d.cc (generated)
void CanvasAttributeGetCallback(
    const v8::FunctionCallbackInfo<v8::Value>& info) {
  // ...
  CanvasRenderingContext2D* blink_receiver =
      V8CanvasRenderingContext2D::ToWrappableUnsafe(isolate, v8_receiver);
  auto&& return_value = blink_receiver->canvas();
  bindings::V8SetReturnValue(info, return_value, blink_receiver);
  //                                              ^^^^^^^^^^^^^^
  //  blink_receiver escapes to V8SetReturnValue → compiler can't prove
  //  the null path traps → tag check is preserved
}

```

This pattern is deterministic: any callback where `blink_receiver` doesn't escape to an opaque callee will have its tag check eliminated.

#### Assembly Evidence

The sbx-testing binary confirms both patterns side by side.

**Tag check ELIMINATED** — `GetContextAttributesOperationCallback` (VA `0x0f866920`):

GDB disassembly from the sbx-testing binary (Chromium 148.0.7766.3):

```
   0xf866987 <blink::(anonymous namespace)::v8_canvas_rendering_context_2d::GetContextAttributesOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&)+103>:
    mov    eax,DWORD PTR [rax+0xb]
   0xf86698a <...+106>:
    mov    rcx,QWORD PTR [r14+0x2a0]
   0xf866991 <...+113>:      shr    eax,0x6
   0xf866994 <...+116>:
    mov    rdi,QWORD PTR [rcx+rax*8]
   0xf866998 <...+120>:      shr    rdi,0x10
   0xf86699c <...+124>:      add    rdi,0x10
   0xf8669a0 <...+128>:
    call   0xfd30d80 <blink::BaseRenderingContext2D::getContextAttributes() const>

```
```
mov    eax, DWORD PTR [rax+0xb]       ; read 32-bit CPT handle (offset 12)
mov    rcx, QWORD PTR [r14+0x2a0]     ; CPT table base from isolate
shr    eax, 0x6                        ; index = handle >> 6
mov    rdi, QWORD PTR [rcx+rax*8]     ; load 64-bit CPT entry
shr    rdi, 0x10                       ; payload = entry >> 16 (NO TAG CHECK)
add    rdi, 0x10                       ; static_cast offset
call   <getContextAttributes>          ; call with unchecked pointer

```

No `and`/`cmp`/`cmov`/`jne`. The tag bits are simply shifted away.

**Tag check PRESERVED** — `GetImageDataOperationCallback` (VA `0x0f8669e0`):

GDB disassembly from the sbx-testing binary (Chromium 148.0.7766.3):

```
   0xf866a69 <blink::(anonymous namespace)::v8_canvas_rendering_context_2d::GetImageDataOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&)+137>:
    mov    ecx,DWORD PTR [rcx+0xb]
   0xf866a6c <...+140>:
    mov    rdx,QWORD PTR [r14+0x2a0]
   0xf866a73 <...+147>:      shr    ecx,0x6
   0xf866a76 <...+150>:
    mov    r12,QWORD PTR [rdx+rcx*8]
   0xf866a7a <...+154>:      mov    ecx,r12d
   0xf866a7d <...+157>:      and    ecx,0xfffe
   0xf866a83 <...+163>:      shr    r12,0x10
   0xf866a87 <...+167>:      mov    rdx,r12
   0xf866a8a <...+170>:      cmp    ecx,0x8a2
   0xf866a90 <...+176>:
    jne    0xf866ea1 <...+1217>

```
```
mov    ecx, DWORD PTR [rcx+0xb]       ; read 32-bit CPT handle
mov    rdx, QWORD PTR [r14+0x2a0]     ; CPT table base from isolate
shr    ecx, 0x6                        ; index = handle >> 6
mov    r12, QWORD PTR [rdx+rcx*8]     ; load 64-bit CPT entry
mov    ecx, r12d                       ; extract low 32 bits (tag)
and    ecx, 0xfffe                     ; mask out marking bit
shr    r12, 0x10                       ; payload = entry >> 16
cmp    ecx, 0x8a2                      ; compare tag (0x8a2 = 1105 << 1 = 2210)
jne    <tag_mismatch_handler>          ; bail on mismatch

```

Full tag validation is present.

#### Release vs. Testing Build

The sbx-testing build has `DCHECK_ALWAYS_ON`, which inserts assertion calls (opaque function calls) before the member dereference. This causes `blink_receiver` to escape, preserving the tag check in most callbacks. In release, DCHECKs are compiled out—the only use of `blink_receiver` is the member call itself, and the majority of tag checks are eliminated. The assembly evidence above (from the sbx-testing build) shows that even with `DCHECK_ALWAYS_ON`, some callbacks like `GetContextAttributesOperationCallback` still have the tag check eliminated. In release, the elimination is far more widespread.

---

## Reproduction

### Test Build

sbx-testing build (Chromium 148.0.7766.3, Linux x64)
Build config: `v8_enable_sandbox = true, v8_enable_memory_corruption_api = true`

### How to Run

```
CHROME="/path/to/sbx-testing/chrome"
FLAGS="--no-sandbox --js-flags=--sandbox-testing --disable-gpu --headless=new --enable-logging=stderr --disable-crash-reporter --disable-breakpad"

# Test 1: Sandbox violation — DOMMatrix(tag=886) → Canvas2D(tag=1105)
timeout 15 $CHROME $FLAGS file://$(pwd)/test-1-sbx-violation.html 2>&1

# Test 2: Cross-type READ — DOMMatrix(tag=886) → Canvas2D(tag=1105)
timeout 15 $CHROME $FLAGS file://$(pwd)/test-2-crosstype-read.html 2>&1

# Test 3: Controlled enum injection via DOMMatrix.m22
timeout 15 $CHROME $FLAGS file://$(pwd)/test-3-enum-inject.html 2>&1

# PoC: Arbitrary Address Write via SkPathBuilder
timeout 20 $CHROME $FLAGS file://$(pwd)/poc.html 2>&1

```
### PoC Description

**test-1-sbx-violation.html** swaps DOMMatrix's CPT handle (tag 886) into a Canvas2D wrapper (expected tag 1105), fills all DOMMatrix fields with out-of-sandbox pointer patterns (`0x00004141_4141x000`), then calls `beginPath()` + `moveTo()` + `stroke()`. The binding layer extracts `DOMMatrix*` as `CanvasRenderingContext2D*` without tag validation. The Canvas2D rendering methods follow internal pointer fields (SkPath, PathBuilder) that land in DOMMatrix's float64 data — now interpreted as out-of-sandbox addresses — triggering `## V8 sandbox violation detected!`.

**test-2-crosstype-read.html** swaps DOMMatrix's CPT handle (tag 886) into a Canvas2D wrapper (expected tag 1105). `getContextAttributes()` reads inline fields from `this` at fixed offsets to populate a `CanvasRenderingContext2DSettings` dictionary. When `this` points to a zeroed DOMMatrix instead of a Canvas2D object, the returned values differ from the Canvas2D baseline: `alpha` flips from `true` to `false`, `willReadFrequently` flips from `false` to `true`. This confirms the API is reading DOMMatrix's Oilpan C++ memory.

**test-3-enum-inject.html** demonstrates that the attacker controls the data read through the confused API. DOMMatrix's inline field `m22` (a float64) overlaps the C++ memory offsets where `getContextAttributes()` reads `alpha` (low 4 bytes) and `colorSpace` (high 4 bytes). By setting `m22` to specific bit patterns via `bits2d(hi, lo)`, the PoC exercises all 8 `PredefinedColorSpace` enum values (srgb, rec2020, display-p3, etc.) and the `alpha` boolean.

**poc.html** achieves an arbitrary address write. It uses the DOMMatrix→Canvas2D confusion, then probes SkPathBuilder's field layout via `beginPath()` to map which DOMMatrix fields correspond to SkPath's `fPts.fData`, `fPts.fSize`, `fPts.fCapacity` etc. It then sets `fPts.fData` to `0x414141414000` (an out-of-sandbox address) and calls `moveTo(48.56470489501953, 48.56470489501953)`, which flushes an `SkPoint{0x42424242, 0x42424242}` to that address via `TArray::push_back()`. Both the write target and write value are fully controlled from JavaScript.

---

## Test Results

### Test 1: Sandbox Violation (DOMMatrix → Canvas2D)

DOMMatrix's CPT handle (tag 886) is transplanted into a Canvas2D wrapper (expected tag 1105). All DOMMatrix fields are filled with out-of-sandbox pointer patterns:

```
// v8_dom_matrix.h — donor type
static constexpr v8::CppHeapPointerTag kThisTag = static_cast<v8::CppHeapPointerTag>(886);
static constexpr v8::CppHeapPointerTagRange kTagRange = {kThisTag, kThisTag}; // [886, 886]

// v8_canvas_rendering_context_2d.h — receiver type
static constexpr v8::CppHeapPointerTag kThisTag = static_cast<v8::CppHeapPointerTag>(1105);
static constexpr v8::CppHeapPointerTagRange kTagRange = {kThisTag, kThisTag}; // [1105, 1105]

```

After the swap, `beginPath()` + `moveTo()` + `stroke()` are called. The Canvas2D rendering path follows internal pointer fields (SkPath, PathBuilder) that land in DOMMatrix's float64 data — filled with `0x00004141_4141x000` — causing an out-of-sandbox memory access.

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x3b6900000000,0x3c6900000000)
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x326700000000,0x336700000000)

## V8 sandbox violation detected!
The sandbox violation was a *read* access which is technically not a sandbox violation. This requires manual investigation.

"ctx_handle=0x80140 dm_handle=0x80180"
"Swapped. Calling beginPath+moveTo+stroke..."
Received signal 11 SEGV_MAPERR 414141420018

```

The faulting address `0x414141420018` is derived from DOMMatrix's `m11` field value (`0x00004141_41414000` + offset `0x18`). This address is far outside both sandbox regions, confirming that the confused Canvas2D code path followed a DOMMatrix float64 field as a pointer into out-of-sandbox memory.

### Test 2: Cross-Type READ (DOMMatrix → Canvas2D)

DOMMatrix's CPT handle (tag 886) is transplanted into a Canvas2D wrapper (tag 1105). The two types have completely disjoint tag ranges:

```
// v8_canvas_rendering_context_2d.h — the receiver type
static constexpr v8::CppHeapPointerTag kThisTag = static_cast<v8::CppHeapPointerTag>(1105);
static constexpr v8::CppHeapPointerTagRange kTagRange = {kThisTag, kThisTag}; // [1105, 1105]

// v8_dom_matrix.h — the donor type
static constexpr v8::CppHeapPointerTag kThisTag = static_cast<v8::CppHeapPointerTag>(886);
static constexpr v8::CppHeapPointerTagRange kTagRange = {kThisTag, kThisTag}; // [886, 886]

```

When `ctx.getContextAttributes()` is called, the binding layer executes:

```
// v8_canvas_rendering_context_2d.cc (generated)
void GetContextAttributesOperationCallback(const v8::FunctionCallbackInfo<v8::Value>& info) {
  // ...
  CanvasRenderingContext2D* blink_receiver =
      V8CanvasRenderingContext2D::ToWrappableUnsafe(isolate, v8_receiver);
      // → Object::Unwrap() → ReadCppHeapPointerField(isolate, obj, 12, {1105, 1105})
      //   CPT entry at swapped index carries tag 886 → outside [1105, 1105]
      //   Tag check SHOULD return nullptr, but it's eliminated
      //   → returns DOMMatrix* as CanvasRenderingContext2D*
  auto&& return_value = blink_receiver->getContextAttributes();
  // reads CanvasRenderingContext2DSettings fields from DOMMatrix's Oilpan memory
}

```
```
BASELINE={"alpha":true,"colorSpace":"srgb","colorType":"unorm8","desynchronized":false,"toneMapping":{"mode":"standard"},"willReadFrequently":false}
CONFUSED={"alpha":false,"colorSpace":"srgb","colorType":"unorm8","desynchronized":false,"toneMapping":{"mode":"standard"},"willReadFrequently":true}
VALUES_DIFFER=true
DONE

```

`alpha` changed from `true` to `false`, `willReadFrequently` changed from `false` to `true`. The API returned data from DOMMatrix's Oilpan C++ memory.

### Test 3: Controlled Enum Injection via DOMMatrix.m22

Same DOMMatrix(tag 886) → Canvas2D(tag 1105) confusion as Test 2. DOMMatrix stores its matrix elements as inline doubles in the C++ object:

```
// dom_matrix_read_only.h
class DOMMatrixReadOnly : public ScriptWrappable {
  // ...
  double m11_, m12_, m13_, m14_;  // row 1
  double m21_, m22_, m23_, m24_;  // row 2 — m22_ overlaps with where
  // ...                          // getContextAttributes() reads alpha/colorSpace
};

```

When `blink_receiver->getContextAttributes()` executes on a `DOMMatrix*`, the bytes of `m22_` are interpreted as Canvas2D's `alpha` (low 4 bytes) and `colorSpace` enum (high 4 bytes). JavaScript can set `dm.m22` to any float64, so the attacker encodes specific uint32 pairs into the float64 bits:

```
ENUM_0=srgb expected=srgb match=true
ENUM_1=rec2020 expected=rec2020 match=true
ENUM_2=display-p3 expected=display-p3 match=true
ENUM_3=rec2100-hlg expected=rec2100-hlg match=true
ENUM_4=rec2100-pq expected=rec2100-pq match=true
ENUM_5=srgb-linear expected=srgb-linear match=true
ENUM_6=display-p3-linear expected=display-p3-linear match=true
ENUM_7=rec2100-linear expected=rec2100-linear match=true
ENUM_PASS=8/8
ALPHA_CONTROL=true (expected true)
DONE

```

All 8 PredefinedColorSpace enum values are controllable. The alpha boolean is independently controllable via the low 4 bytes.

### PoC: Arbitrary Address Write (DOMMatrix → Canvas2D → SkPath)

Building on the cross-type confusion, this test achieves an arbitrary write to an out-of-sandbox address. The technique uses `beginPath()` on a DOMMatrix-confused Canvas2D to probe the SkPathBuilder field mapping, then sets DOMMatrix fields so that `fPts.fData` (the SkPath point array base pointer) points to a chosen out-of-sandbox address. Calling `moveTo(x, y)` pushes an `SkPoint{float(x), float(y)}` to that address via `TArray<SkPoint>::push_back()`.

The write instruction in `TArray::push_back` (`SkTArray.h:218`):

```
; TArray<SkPoint>::push_back — skia_private::TArray<>::push_back()
 4e4e556: 48 8b 13              mov    rdx, QWORD PTR [rbx]        ; rdx = fData (controlled)
 4e4e559: 48 8d 04 ca           lea    rax, [rdx+rcx*8]            ; target = fData + fSize*8
 4e4e55d: 49 8b 36              mov    rsi, QWORD PTR [r14]        ; rsi = SkPoint value
 4e4e560: 48 89 34 ca           mov    QWORD PTR [rdx+rcx*8], rsi  ; ★ WRITE *target = value

```

`fData` is derived from a DOMMatrix float64 field, and `fSize` is zero (reset by `beginPath`), so the write goes directly to `fData + 0`. The SkPoint value comes from `moveTo(48.56470489501953, 48.56470489501953)`, where `float32(48.56470489501953) = 0x42424242` exactly.

```
## V8 sandbox violation detected!

Received signal 11 SEGV_MAPERR 414141414000
#4 skia_private::TArray<>::push_back() [../../third_party/skia/include/private/base/SkTArray.h:218:42]
#5 SkPathBuilder::moveTo() [../../third_party/skia/src/core/SkPathBuilder.cpp:168:14]
#6 blink::PathBuilder::MoveTo()
#7 blink::CanvasPath::UpdatePathFromLineOrArcIfNecessary()
#8 blink::CanvasPath::moveTo()
#9 blink::v8_canvas_rendering_context_2d::MoveToOperationCallback()
#10 Builtins_CallApiCallbackGeneric

Registers:
  r8: 0000000000000002  r9: 0000000000000003 r10: 000039f4004b0000 r11: 00002609010c1cc5
 r12: 00007ffd0204e5f8 r13: 000039f4004b0080 r14: 00007ffd0204e450 r15: 00007ffd0204e5f8
  di: 000028ec02123bf0  si: 4242424242424242  bp: 00007ffd0204e440  bx: 000028ec02123bf0
  dx: 0000414141414000  ax: 0000414141414000  cx: 0000000000000000  sp: 00007ffd0204e400
  ip: 0000558641c0e560 efl: 0000000000010206 cgf: 002b000000000033 erf: 0000000000000006
 trp: 000000000000000e msk: 0000000000000000 cr2: 0000414141414000

  dx/ax: 0000414141414000  ← fData pointer (write target, controlled via DOMMatrix field)
  si:    4242424242424242  ← SkPoint value (write data, controlled via moveTo arguments)
  cx:    0000000000000000  ← fSize = 0 (reset by beginPath), so write goes to fData+0
  erf:   0000000000000006  ← page fault error code: PF_WRITE|PF_PROT (write access)
  cr2:   0000414141414000  ← faulting address = fData (confirms out-of-sandbox write target)

```

The attacker controls both the write address (`cr2 = 0x414141414000`, set via DOMMatrix field → `fPts.fData`) and the write value (`si = 0x4242424242424242`, set via `moveTo()` arguments). `erf = 6` confirms this is a write fault. This is an arbitrary address write primitive over out-of-sandbox memory.

---

## Suggested Fix

The root cause is that `ReadCppHeapPointerField()` returns `nullptr` on tag mismatch, and LLVM removes the null path when the returned pointer is provably dereferenced immediately.

The existing `entry = 0` design serves three purposes documented in the source comments: (1) the null handle (index 0) naturally returns nullptr without a separate branch, (2) nullptr guarantees a crash even on Arm64 with TBI (top byte ignore), and (3) the generated machine code stays short, which matters because this function is inlined into thousands of call sites. A fix should preserve these properties.

**Option A (minimal, preserves semantics): `volatile` to prevent DCE**

```
--- a/include/v8-sandbox.h
+++ b/include/v8-sandbox.h
+  volatile Address safe_entry = entry;
   if (V8_LIKELY(actual_tag >= first_tag && actual_tag <= last_tag)) {
-    entry = entry >> kCppHeapPointerPayloadShift;
+    safe_entry = entry >> kCppHeapPointerPayloadShift;
   } else {
-    entry = 0;
+    safe_entry = 0;
   }
-  return reinterpret_cast<T*>(entry);
+  return reinterpret_cast<T*>(safe_entry);

```

The `volatile` qualifier forces the compiler to materialize both branches, since a write to a volatile variable is an observable side effect that cannot be eliminated. This preserves the existing nullptr-on-mismatch semantics, null handle behavior, Arm64 TBI safety, and keeps the code size impact minimal (one extra stack spill).

**Option B (defense in depth): trap on tag mismatch**

```
--- a/include/v8-sandbox.h
+++ b/include/v8-sandbox.h
   if (V8_LIKELY(actual_tag >= first_tag && actual_tag <= last_tag)) {
     entry = entry >> kCppHeapPointerPayloadShift;
   } else {
-    entry = 0;
+    SBXCHECK(false);  // or __builtin_trap()
+    __builtin_unreachable();
   }

```

This makes the tag mismatch a definite crash independent of how the caller uses the return value. However, it changes the semantics: the null handle (index 0, tag 0) would now trap instead of returning nullptr, so callers that rely on the null-handle-returns-nullptr property would need adjustment. It also increases code size at every inlined call site due to the trap instruction.

#### Impact analysis

## Impact Analysis

The CPT tag check was introduced specifically to prevent type confusion between wrapper objects. With the check eliminated in the majority of binding callbacks in release Chrome, an attacker who can corrupt 4 bytes within the sandbox (the CPT handle at offset +12) can swap a wrapper's handle to point to a different-type C++ object on the Oilpan heap. The sandbox testing harness confirms this as a sandbox violation (Test 1).

Once the cross-type confusion is established, JavaScript APIs operating on the confused pointer read C++ memory outside the V8 sandbox. Test 2 demonstrates this: `getContextAttributes()` returns field values from DOMMatrix's Oilpan allocation instead of Canvas2D's. The attacker can also control what is read — Test 3 shows that setting `DOMMatrix.m22` from JavaScript directly determines the `colorSpace` enum and `alpha` boolean returned through the confused API, because the float64 bits of `m22` overlap with the C++ memory offsets that `getContextAttributes()` interprets as those fields.

PoC demonstrates a full arbitrary address write (AAW) primitive: by controlling DOMMatrix fields that overlap with SkPathBuilder's `fPts.fData` pointer, the attacker directs `moveTo()`'s `TArray::push_back()` to write attacker-controlled float data to an arbitrary out-of-sandbox address. Both the write target and write value are fully controlled from JavaScript. All accessed memory resides on the Oilpan C++ heap, outside the V8 sandbox.

---

### The cause

#### What version of Chrome have you found the security issue in?

148.0.7766.3 dev, 146.0.7680.177 stable

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Sandbox Escape

#### How would you like to be publicly acknowledged for your report?

Jungwoo Lee (@physicube) and Wongi Lee (@\_qwerty\_po)

## Attachments

- [poc.html](attachments/poc.html) (text/html, 8.7 KB)
- [test-2-crosstype-read.log](attachments/test-2-crosstype-read.log) (application/octet-stream, 6.9 KB)
- [test-1-sbx-violation.html](attachments/test-1-sbx-violation.html) (text/html, 1.7 KB)
- [test-1-sbx-violation.log](attachments/test-1-sbx-violation.log) (application/octet-stream, 7.6 KB)
- [test-2-crosstype-read.html](attachments/test-2-crosstype-read.html) (text/html, 1.3 KB)
- [test-3-enum-inject.html](attachments/test-3-enum-inject.html) (text/html, 1.8 KB)
- [poc.log](attachments/poc.log) (application/octet-stream, 7.5 KB)
- [test-3-enum-inject.log](attachments/test-3-enum-inject.log) (application/octet-stream, 7.9 KB)

## Timeline

### ml...@google.com (2026-04-09)

I wonder if clang got more aggressive here as we have verified that the tag checks are present at some point. Either way, thanks for the report!

### qw...@gmail.com (2026-04-09)

Could you please add jwlee2217@gmail.com to the CC list so that both accounts can access the issue?

### dx...@google.com (2026-04-27)

Project: v8/v8  

Branch:  main  

Author:  Michael Lippautz [mlippautz@chromium.org](mailto:mlippautz@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7789384>

sandbox: Avoid DCE on tag checks

---


Expand for full commit details
```
     
    Bug: 500771385 
    Change-Id: I7bf8e782ae2f3d1d7f90df0599a10716e2a21586 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7789384 
    Reviewed-by: Samuel Groß <saelo@chromium.org> 
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106844}

```

---

Files:

- M `include/v8-internal.h`
- M `include/v8-sandbox.h`

---

Hash: [cfaa590b517161e60da356c0df7ecf4db149a26c](https://chromiumdash.appspot.com/commit/cfaa590b517161e60da356c0df7ecf4db149a26c)  

Date: Fri Apr 24 12:48:50 2026


---

### sa...@google.com (2026-04-29)

I think this would be worth backmerging as it likely allows for a V8 sandbox breakout.

### ch...@google.com (2026-04-29)

**M148** merge request created. **Please update [crbug/507720757](https://crbug.com/507720757) to have this merge reviewed.**

### dx...@google.com (2026-05-04)

Project: v8/v8  

Branch:  refs/branch-heads/14.8  

Author:  Michael Lippautz [mlippautz@chromium.org](mailto:mlippautz@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7806934>

[M148] sandbox: Avoid DCE on tag checks

---


Expand for full commit details
```
     
    Original change's description: 
    > sandbox: Avoid DCE on tag checks 
    > 
    > Bug: 500771385 
    > Change-Id: I7bf8e782ae2f3d1d7f90df0599a10716e2a21586 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7789384 
    > Reviewed-by: Samuel Groß <saelo@chromium.org> 
    > Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#106844} 
     
    (cherry picked from commit cfaa590b517161e60da356c0df7ecf4db149a26c) 
     
    Bug: 507720757,500771385 
    Change-Id: I7bf8e782ae2f3d1d7f90df0599a10716e2a21586 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7806934 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/14.8@{#34} 
    Cr-Branched-From: f9659283a5f8d42b3c09228cf5df606fcaf47a3d-refs/heads/14.8.178@{#1} 
    Cr-Branched-From: 141232520dc4910401240c531db3af36910a0fd1-refs/heads/main@{#106240}

```

---

Files:

- M `include/v8-internal.h`
- M `include/v8-sandbox.h`

---

Hash: [adcd432c064f33f073c7fb4588312f6abd47bde5](https://chromiumdash.appspot.com/commit/adcd432c064f33f073c7fb4588312f6abd47bde5)  

Date: Fri Apr 24 12:48:50 2026


---

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $20000.00 for this report.

Rationale for this decision:
v8 Sandbox bypass with write.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-08-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/500771385)*
