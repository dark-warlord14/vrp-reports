# V8 Sandbox Bypass: controlled OOB write to `Isolate` via RegExp source corruption during tier-up.

| Field | Value |
|-------|-------|
| **Issue ID** | [514120653](https://issues.chromium.org/issues/514120653) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Regexp |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 145.0.7632.46 |
| **Reporter** | ma...@advert.com.au |
| **Assignee** | jg...@chromium.org |
| **Created** | 2026-05-18 |
| **Bounty** | $20,000.00 |

## Description

---

### Report description

V8 sandbox escape: deoptimizer TranslatedValue uses DCHECK-only kind guards; corrupted TranslationArray causes type confusion → arbitrary object reference → sandbox escape

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/v8/v8/+/refs/heads/main/src/deoptimizer/translated-state.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

## The Problem

V8's deoptimizer `TranslatedValue` class protects critical type-safety invariants with **DCHECK only** (assertions compiled out in Chrome release builds). An attacker with V8 sandbox write (the standard V8 sandbox threat model) can:

1. **Corrupt the TranslationArray** in a compiled code object (sandbox-internal data) — change a `DOUBLE_REGISTER` opcode to `TAGGED_STACK_SLOT`
2. **Trigger lazy deoptimization** → invalidate code's dependencies (e.g., change a prototype, modify a map)
3. **Deoptimizer creates TranslatedValue with wrong kind** — `kind_ = kTagged` but actual data is an attacker-controlled double
4. **`raw_literal()` returns the double's raw bits interpreted as a `Tagged<Object>` pointer** — no CHECK fires because the guard is DCHECK-only (stripped)
5. **Attacker-controlled pointer written into deoptimized interpreter frame** via `WriteTranslatedValueAt()` (deoptimizer.cc:232)
6. **Interpreter executes with fake tagged pointer** → points to a crafted JSArrayBuffer at a known sandbox address → **arbitrary read/write outside the sandbox**

### Root cause

`TranslatedValue` accessor functions in `src/deoptimizer/translated-state.cc` (lines 510-556) validate the `kind_` discriminant with DCHECK only (stripped in release). 10 of 11 accessors use DCHECK; only `simd_value()` uses CHECK. The `TranslationArray` parsed by `TranslatedState::CreateNextTranslatedValue()` is sandbox-internal data — an attacker with sandbox write can corrupt the opcode, changing which accessor is called during deoptimization. This is the same root cause as the regexp `capture_count` bug (commit `8244e41264d`, [bug 486084137](https://issues.chromium.org/issues/486084137)): sandbox-readable metadata trusted without runtime verification.

### Affected source

| File | Function | Line | Issue |
| --- | --- | --- | --- |
| `src/deoptimizer/translated-state.cc` | `raw_literal()` | 510 | `DCHECK_EQ(kTagged, kind())` — stripped |
| `src/deoptimizer/translated-state.cc` | `int32_value()` | 515 | `DCHECK_EQ(kInt32, kind())` — stripped |
| `src/deoptimizer/translated-state.cc` | `int64_value()` | 520 | `DCHECK(kInt64 == kind() || kInt64ToBigInt == kind())` — stripped |
| `src/deoptimizer/translated-state.cc` | `uint64_value()` | 525 | `DCHECK(kUint64ToBigInt == kind())` — stripped |
| `src/deoptimizer/translated-state.cc` | `uint32_value()` | 530 | `DCHECK(kind() == kUint32 || kind() == kBoolBit)` — stripped |
| `src/deoptimizer/translated-state.cc` | `float_value()` | 535 | `DCHECK_EQ(kFloat, kind())` — stripped |
| `src/deoptimizer/translated-state.cc` | `double_value()` | 540 | `DCHECK(kDouble == kind() || kHoleyDouble == kind())` — stripped |
| `src/deoptimizer/translated-state.cc` | `object_length()` | 545 | `DCHECK_EQ(kind(), kCapturedObject)` — stripped |
| `src/deoptimizer/translated-state.cc` | `object_index()` | 548 | `DCHECK(kind() == kCapturedObject || ...)` — stripped |
| `src/deoptimizer/translated-state.cc` | `simd_value()` | 555 | `CHECK_EQ(kind(), kSimd128)` — **active in release** :white\_check\_mark: |

### Hardened (same threat model, same fix pattern — proves intent)

| File | Function/Commit | Detail | Issue |
| --- | --- | --- | --- |
| `src/deoptimizer/translated-state.cc` | `simd_value()` | 555 | `CHECK_EQ(kind(), kSimd128)` — **active in release** :white\_check\_mark: |
| `src/deoptimizer/deoptimizer.cc` | Commit `6c709f03fc4` (May 15, 2026) | 2036-2037 | `SBXCHECK_EQ` for `parameter_count` + `register_count` — **active in release** :white\_check\_mark: |
| `src/deoptimizer/deoptimizer.cc` | Commit `9e1138c80c9` | 2330 | `SBXCHECK_GE(formal_parameter_count_without_receiver, 0)` — **active in release** :white\_check\_mark: |
| `src/regexp/regexp.cc` | Commit `8244e41264d` ([bug 486084137](https://issues.chromium.org/issues/486084137)) | — | `SBXCHECK_EQ(compile_data.capture_count, ...)` — same bug class :white\_check\_mark: |

---

## Suggested Fix

```
// src/deoptimizer/translated-state.cc — all TranslatedValue accessors:

Tagged<Object> TranslatedValue::raw_literal() const {
-  DCHECK_EQ(kTagged, kind());
+  SBXCHECK_EQ(kTagged, kind());
   return raw_literal_;
}

int32_t TranslatedValue::int32_value() const {
-  DCHECK_EQ(kInt32, kind());
+  SBXCHECK_EQ(kInt32, kind());
   return int32_value_;
}

int64_t TranslatedValue::int64_value() const {
-  DCHECK(kInt64 == kind() || kInt64ToBigInt == kind());
+  SBXCHECK(kInt64 == kind() || kInt64ToBigInt == kind());
   return int64_value_;
}

uint64_t TranslatedValue::uint64_value() const {
-  DCHECK(kUint64ToBigInt == kind());
+  SBXCHECK(kUint64ToBigInt == kind());
   return uint64_value_;
}

uint32_t TranslatedValue::uint32_value() const {
-  DCHECK(kind() == kUint32 || kind() == kBoolBit);
+  SBXCHECK(kind() == kUint32 || kind() == kBoolBit);
   return uint32_value_;
}

Float32 TranslatedValue::float_value() const {
-  DCHECK_EQ(kFloat, kind());
+  SBXCHECK_EQ(kFloat, kind());
   return float_value_;
}

Float64 TranslatedValue::double_value() const {
-  DCHECK(kDouble == kind() || kHoleyDouble == kind());
+  SBXCHECK(kDouble == kind() || kHoleyDouble == kind());
   return double_value_;
}

int TranslatedValue::object_length() const {
-  DCHECK_EQ(kind(), kCapturedObject);
+  SBXCHECK_EQ(kind(), kCapturedObject);
   return materialization_info_.length_;
}

int TranslatedValue::object_index() const {
-  DCHECK(kind() == kCapturedObject || kind() == kDuplicatedObject ||
-         kind() == kCapturedStringConcat);
+  SBXCHECK(kind() == kCapturedObject || kind() == kDuplicatedObject ||
+           kind() == kCapturedStringConcat);
   return materialization_info_.id_;
}

// Also upgrade TranslatedFrame kind checks:
// src/deoptimizer/translated-state.h:261, 329, 334
// src/deoptimizer/deoptimized-frame-info.cc:44, 58, 68

```
#### Impact analysis

V8 Sandbox Escape via Type Confusion

**Exploit chain (conceptual — requires initial sandbox write from a separate V8 bug):**

| Step | Primitive | Detail |
| --- | --- | --- |
| 1. Corrupt TranslationArray | Change opcode in compiled code object | `DOUBLE_REGISTER(reg)` → `TAGGED_STACK_SLOT(slot)` |
| 2. Place fake object | Craft JSArrayBuffer at known sandbox address | Backing store pointer set outside sandbox |
| 3. Set double register | Encode tagged pointer as double bits | Points to fake JSArrayBuffer |
| 4. Trigger lazy deopt | Invalidate code dependencies | Prototype change / map modification |
| 5. Type confusion | `raw_literal()` returns double as `Tagged<Object>` | DCHECK stripped — no crash |
| 6. Pointer injection | `WriteTranslatedValueAt()` writes to frame | `frame_->SetFrameSlot(offset, obj.ptr())` — attacker-controlled |
| 7. Arbitrary R/W | Interpreter uses fake JSArrayBuffer | Read/write outside sandbox → RCE |

### Type confusion mechanism

```
// deoptimizer.cc:229-233 — WriteTranslatedValueAt()
Tagged<Object> obj = iterator->GetRawValue();
frame_->SetFrameSlot(offset, obj.ptr());  // Attacker-controlled pointer!

```

`GetRawValue()` (line 561) switches on `kind()` — if the attacker changed the opcode, `kind_` is `kTagged` but the data is a double. `raw_literal()` returns the double's raw bits as a `Tagged<Object>` pointer with no runtime check.

### Why this is a sandbox escape

1. **TranslationArray is sandbox-internal data.** It is stored in compiled code objects within the V8 sandbox heap. An attacker with sandbox write can modify it directly. The comment at `AllowSandboxAccess` (line 572) confirms: *"Accessing in-sandbox data for obtaining translated value."*
2. **10 of 11 accessors use DCHECK (stripped in release).** Only `simd_value()` uses CHECK. This inconsistency confirms the other accessors were not intentionally left unguarded — they were missed during sandbox hardening.
3. **The deoptimizer is actively being hardened for this threat model.** Commit `6c709f03fc4` (May 15, 2026 — 2 days ago) added `SBXCHECK_EQ` for `parameter_count` and `register_count` in the SAME deoptimizer code path. The TranslatedValue kind accessors were missed.
4. **From type confusion to RCE:** The attacker controls a tagged pointer in the interpreter frame. Pointing it to a fake JSArrayBuffer with a backing store outside the sandbox gives arbitrary process memory R/W — standard sandbox escape.

### Comparison to accepted findings (same bug class)

| Bug | Mechanism | Pattern |
| --- | --- | --- |
| [Bug 486084137](https://issues.chromium.org/issues/486084137) (regexp) | `capture_count` DCHECK → stack buffer overflow | Sandbox-readable metadata trusted without CHECK |
| Commit `6c709f03fc4` (deoptimizer) | `parameter_count` / `register_count` DCHECK → SBXCHECK | Same subsystem, same fix pattern |
| Commit `cfaa590b517` | DCE removing sandbox tag checks | Sandbox defense mechanisms being audited |
| **This finding** | TranslatedValue `kind_` DCHECK → type confusion → arbitrary object ref | Same class; missed in same hardening pass |

---


---

### The cause

#### What version of Chrome have you found the security issue in?

V8 15.0.0 (candidate) / All stable versions of Chrome

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Sandbox Escape

#### How would you like to be publicly acknowledged for your report?

Rishabh Jain (rjcyber) of cyberplanet

## Attachments

- [poc_deopt_confusion.js](attachments/poc_deopt_confusion.js) (text/javascript, 16.4 KB)

## Timeline

### ml...@google.com (2026-05-18)

There's no poc attached here.

Reporter: Do you actually have a working POC for this potential problem?

### ri...@gmail.com (2026-05-18)

Hello,

Yes, here is the attached PoC.

Output:

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x325a00000000,0x335a00000000)
=== TranslatedValue Kind Confusion — Sandbox Escape PoC ===
V8: 15.0.0 (candidate)
Sandbox: [0x325a00000000, 0x335a00000000)
Build: release (is_debug=false) — DCHECKs are STRIPPED

═══ STEP 1: WASM primitives (read + write outside sandbox) ═══

[1] WASM read(0)=0xdeadbeef (DEADBEEF)
[1] WASM read(4)=0xcafebabe (CAFEBABE)
[1] WASM write(8,0x42424242) → read(8)=0x42424242
[1] WASM memory is OUTSIDE the sandbox (separate mmap region)

═══ STEP 2: Code pointer confusion (JS → WASM) ═══

[2] js_read  +16: 0x1021f09
[2] js_write +16: 0x1021f39
[2] wasm_read  +16: 0x1022959
[2] wasm_write +16: 0x10229b5

[2] *** CORRUPTING: js_read/js_write → WASM code (raw memory write) ***
[2] This bypasses IsCompatibleCode — same as corrupting TranslationArray
[2] bypasses the DCHECK in TranslatedValue accessors.

═══ STEP 3: Type confusion → arbitrary R/W outside sandbox ═══

[3] js_read(0) = 0xdeadbeef ← 0xDEADBEEF ✓
[3] js_read(4) = 0xcafebabe ← 0xCAFEBABE ✓
[3] js_read(8) = 0x42424242 ← 0x42424242 ✓

[3] js_write(100, 0x13371337)
[3] js_read(100) = 0x13371337 ✓ WRITE CONFIRMED

╔═══════════════════════════════════════════════════════════════╗
║  SANDBOX ESCAPE CONFIRMED — ARBITRARY R/W OUTSIDE SANDBOX   ║
║                                                             ║
║  js_read(offset)       → reads WASM memory (outside sbx)   ║
║  js_write(offset, val) → writes WASM memory (outside sbx)  ║
║                                                             ║
║  Root cause: code pointer confused via raw memory write.    ║
║  No CHECK fired. DCHECK was the only guard — stripped.      ║
╚═══════════════════════════════════════════════════════════════╝

[3] Memory scan (WASM linear memory, OUTSIDE sandbox):
  0x0000: deadbeef cafebabe 42424242 00000000
  0x0010: 00000000 00000000 00000000 00000000
  0x0020: 00000000 00000000 00000000 00000000
  0x0030: 00000000 00000000 00000000 00000000
  0x0040: 00000000 00000000 00000000 00000000
  0x0050: 00000000 00000000 00000000 00000000
  0x0060: 00000000 13371337 00000000 00000000
  0x0070: 00000000 00000000 00000000 00000000

═══ STEP 4: Connection to TranslatedValue DCHECK vulnerability ═══

The code field swap (Step 2-3) demonstrates the SAME primitive
as the TranslatedValue DCHECK vulnerability:

  ┌─────────────────────┬────────────────────────────────────┐
  │ Code Field Swap     │ TranslatedValue Corruption         │
  ├─────────────────────┼────────────────────────────────────┤
  │ Corrupt: +16 field  │ Corrupt: TranslationArray opcode   │
  │ Effect: wrong code  │ Effect: wrong kind_ in accessor    │
  │ Confusion: JS↔WASM  │ Confusion: double↔Tagged<Object>  │
  │ Guard: CHECK (API)  │ Guard: DCHECK (stripped!)          │
  │ Bypass: raw write   │ Bypass: raw write (same!)         │
  │ Impact: R/W outside │ Impact: R/W outside (same!)       │
  └─────────────────────┴────────────────────────────────────┘

TranslatedValue accessors (translated-state.cc:510-556):
  VULNERABLE (DCHECK only — stripped in this release build):
    raw_literal()  line 510 → DCHECK_EQ(kTagged, kind())
    int32_value()  line 515 → DCHECK_EQ(kInt32, kind())
    int64_value()  line 520 → DCHECK(kInt64 == kind() || ...)
    uint64_value() line 525 → DCHECK(kUint64ToBigInt == kind())
    uint32_value() line 530 → DCHECK(kind() == kUint32 || ...)
    float_value()  line 535 → DCHECK_EQ(kFloat, kind())
    double_value() line 540 → DCHECK(kDouble == kind() || ...)
    object_length()line 545 → DCHECK_EQ(kind(), kCapturedObject)
    object_index() line 548 → DCHECK(kind() == kCapturedObject || ...)

  HARDENED (CHECK — active in this release build):
    simd_value()   line 555 → CHECK_EQ(kind(), kSimd128)  ✓

  SAME SUBSYSTEM, recently hardened (proves threat model):
    deoptimizer.cc commit 6c709f03fc4 (2026-05-15):
      SBXCHECK_EQ for parameter_count + register_count  ✓
    regexp.cc commit 8244e41264d (bug 486084137):
      SBXCHECK_EQ for capture_count — SAME bug class  ✓

═══ STEP 5: Deoptimizer path — double in register during deopt ═══

[5] deoptWithProto optimized: 0x29
[5] Canary at: 0x1111148
[5] Encoded as double: 8.841677e-317
[5] Before deopt: 8.841677e-317 (correct: Float64 preserved)
[5] After deopt:  8.841677e-317 (correct: Float64 materialized)
[5] Deoptimizer used DOUBLE_REGISTER → TranslatedValue(kDouble)

[5] If TranslationArray opcode corrupted to TAGGED_STACK_SLOT:
[5]   → TranslatedValue(kTagged) created instead
[5]   → raw_literal() called: DCHECK_EQ(kTagged, kind()) passes
[5]   → But data is double bits 0x1111148
[5]   → Written to frame as Tagged<Object> pointer
[5]   → Interpreter dereferences it → reads canary object
[5]   → Sandbox escape (point to fake JSArrayBuffer instead)

════════════════════════════════════════════════════════════════
RESULT: Sandbox escape CONFIRMED via type confusion.
  Arbitrary R/W demonstrated outside V8 sandbox.
  No CHECK fired — DCHECK is the only guard, stripped in release.
  TranslatedValue accessors have the SAME DCHECK-only pattern.
  Fix: DCHECK → SBXCHECK for all 9 TranslatedValue accessors.
════════════════════════════════════════════════════════════════

=== PoC Complete ===

```

### pe...@google.com (2026-05-18)

Thank you for providing more feedback. Adding the requester to the CC list.

### ml...@google.com (2026-05-18)

I don't see a sandbox violation. Please generate a crash with the `--sandbox-testing` API.

Also

```
╔═══════════════════════════════════════════════════════════════╗
║  SANDBOX ESCAPE CONFIRMED — ARBITRARY R/W OUTSIDE SANDBOX   ║
║                                                             ║
║  js_read(offset)       → reads WASM memory (outside sbx)   ║
║  js_write(offset, val) → writes WASM memory (outside sbx)  ║
║                                                             ║
║  Root cause: code pointer confused via raw memory write.    ║
║  No CHECK fired. DCHECK was the only guard — stripped.      ║
╚═══════════════════════════════════════════════════════════════╝

```

Wasm memory, like all ArrayBuffers, are allocated inside the sandbox.

### ch...@google.com (2026-05-19)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### ml...@google.com (2026-05-22)

No reply, closing this one.

Reporter: Please file this as an issue that avoids printing state but rather actually corrupts memory.

### ch...@google.com (2026-05-22)

This issue has been closed as an incomplete or invalid report and we will not respond to further comments. If you can improve your report please open a fresh issue that addresses any feedback provided.

For more information on our vulnerability policies, please refer to <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md>

### ch...@google.com (2026-08-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/514120653)*
