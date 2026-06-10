# WebAssembly Shared-Everything Threads proposal implementation tracking bug

| Field | Value |
|-------|-------|
| **Issue ID** | [482742896](https://issues.chromium.org/issues/482742896) |
| **Status** | Accepted |
| **Severity** | S2-Medium |
| **Priority** | P4 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | ma...@chromium.org |
| **Assignee** | ml...@chromium.org |
| **Created** | 2026-02-09 |
| **Bounty** | Confirmed (amount unknown) |

## Description

# Steps to reproduce the problem

V8 14.6.199 (commit 01d64e2c6be), Linux x86\_64, Ubuntu 24.04.

1. Build d8 with DrumBrake enabled. Use the following args.gn:
   
   v8\_enable\_sandbox = true
   is\_asan = true
   is\_debug = false
   symbol\_level = 1
   v8\_enable\_drumbrake = true
   v8\_enable\_webassembly = true
   target\_cpu = "x64"
   is\_component\_build = false
2. Apply two patches. These are needed because shared Wasm types are not yet
   enabled under --wasm-jitless (see "Current reachability" in description).
   
   Patch 1 -- v8/src/wasm/wasm-features.cc
   In FromFlags(), inside the V8\_ENABLE\_DRUMBRAKE / wasm\_jitless block,
   after the line "features.Add(WasmEnabledFeature::legacy\_eh);", add:
   
   if (v8\_flags.experimental\_wasm\_shared)
   features.Add(WasmEnabledFeature::shared);
   
   Patch 2 -- v8/src/wasm/interpreter/wasm-interpreter-runtime.cc
   Replace the RttCanon() function body (line 2397) with:
   
   DirectHandle<Map> WasmInterpreterRuntime::RttCanon(
   uint32\_t type\_index) const {
   bool type\_is\_shared = module\_->types[type\_index].is\_shared;
   DirectHandle<WasmTrustedInstanceData> data = type\_is\_shared
   ? direct\_handle(
   wasm\_trusted\_instance\_data()->shared\_part(), isolate\_)
   : wasm\_trusted\_instance\_data();
   DirectHandle<Map> rtt{
   TrustedCast<Map>(
   data->managed\_object\_maps()->get(type\_index)),
   isolate\_};
   return rtt;
   }
   
   Patch 2 fixes a separate bug: RttCanon() always reads from non-shared
   instance data, but shared type maps live in shared\_part(). This must be
   fixed before the write barrier bug is reachable.
3. Rebuild d8.
4. Save the following as poc.js:
   d8.file.execute("test/mjsunit/wasm/wasm-module-builder.js");
   (function() {
   let b = new WasmModuleBuilder();
   let inner = b.addStruct(
   [makeField(kWasmI32, true)],
   kNoSuperType, false, true);
   let outer = b.addStruct(
   [makeField(wasmRefNullType(inner), true),
   makeField(kWasmI32, true)],
   kNoSuperType, false, true);
   b.addFunction("test", makeSig([], [kWasmI32]))
   .addBody([
   kExprI32Const, 42,
   kGCPrefix, kExprStructNew, inner,
   kExprI32Const, 99,
   kGCPrefix, kExprStructNew, outer,
   kGCPrefix, kExprStructGet, outer, 0,
   kExprRefAsNonNull,
   kGCPrefix, kExprStructGet, inner, 0,
   ]).exportFunc();
   b.instantiate().exports.test();
   })();
5. Run:
   
   ./d8 --wasm-jitless --experimental-wasm-shared --expose-gc poc.js
6. Observe crash:
   
   Fatal error in ../../v8/src/heap/heap-write-barrier-inl.h, line 166
   Check failed: !WriteBarrier::IsRequired(host, value).
   
   WriteBarrier::VerifySkipWriteBarrier<Object>(...)
   Handlers<false>::s2s\_StructNew(...)
   v8/src/wasm/interpreter/wasm-interpreter.cc:6025
   WasmInterpreterRuntime::ExecuteFunction(...)
   v8/src/wasm/interpreter/wasm-interpreter-runtime.cc:1423
   
   The same CHECK fires for s2s\_RefArrayNew (line 6261) and
   s2s\_ArrayNewFixed (line 6331) when using array.new or
   array.new\_fixed with shared ref-typed arrays.

# Problem Description

The V8 Wasm interpreter (DrumBrake) has three missing GC write barriers in v8/src/wasm/interpreter/wasm-interpreter.cc. When creating shared
structs or arrays with reference-typed fields/elements, the interpreter unconditionally passes SKIP\_WRITE\_BARRIER to StoreRefIntoMemory(). Since shared Wasm objects are allocated in kSharedOld (the shared old generation), this creates untracked old-to-young pointers. Minor GC can then relocate or free the young-generation target, producing a dangling pointer (UAF).

This is an incomplete fix of [bug 42204563](https://issues.chromium.org/issues/42204563) (commit 56cd8297b40, "[wasm][shared] Fix write barrier"). That commit patched only
constant-expression-interface.cc but missed three identical sites in the interpreter.

Affected sites in wasm-interpreter.cc:

1. s2s\_StructNew, line 6025 -- stores ref fields into new shared struct:
   StoreRefIntoMemory(\*struct\_obj, field\_addr,
   field\_offset + kHeapObjectTag, \*ref, SKIP\_WRITE\_BARRIER);
2. s2s\_RefArrayNew, line 6261 -- stores ref fill value into new shared array:
   StoreRefIntoMemory(TrustedCast<HeapObject>(\*array), element\_addr,
   element\_offset, \*value, SKIP\_WRITE\_BARRIER);
3. s2s\_ArrayNewFixed, line 6331 -- stores each ref element into new shared array:
   StoreRefIntoMemory(TrustedCast<HeapObject>(\*array), element\_addr,
   element\_offset, \*ref, SKIP\_WRITE\_BARRIER);

Root cause: Shared Wasm structs/arrays are allocated in kSharedOld (wasm-interpreter-runtime.cc:2413):
type.is\_shared ? AllocationType::kSharedOld : AllocationType::kYoung

SKIP\_WRITE\_BARRIER is only valid for young-gen objects because the GC already scans young space fully. For kSharedOld objects storing references to young-gen objects, the GC's remembered set must be updated via a write barrier. Without it, minor GC may collect the referenced young-gen object while it is still reachable, causing a use-after-free.

The interpreter's own s2s\_StructSet (line 6183) and s2s\_ArraySet (line 6680) correctly use UPDATE\_WRITE\_BARRIER, confirming the mutation
paths are safe. Only the creation/initialization paths are affected.

Additional bug: RttCanon() at wasm-interpreter-runtime.cc:2397 always reads type maps from wasm\_trusted\_instance\_data()->managed\_object\_maps(), but shared type maps are stored in shared\_part()->managed\_object\_maps().
This is a second bug that prevents shared types from working in the interpreter. The constant-expression interface handles this correctly
via GetTrustedInstanceDataForTypeIndex() which dispatches on is\_shared.

Current reachability: wasm-features.cc:FromFlags() disables all experimental features under --wasm-jitless. The reproduction patches
bypass this gate and the RttCanon bug to reach the write barrier issue. When shared types graduate from experimental to standard (the
shared-everything-threads proposal is actively progressing), these code paths become reachable without patches on all interpreter platforms:

- iOS/tvOS (all Wasm runs through interpreter, no JIT available)
- Android WebView in some configurations
- Any V8 embedder using --jitless or --wasm-jitless
  On release builds without V8\_VERIFY\_WRITE\_BARRIERS, the missing barriers silently create dangling pointers. An attacker controls what references are stored, when GC runs via allocation pressure, when the dangling pointer is dereferenced via struct.get/array.get, and object sizes for
  heap shaping. This enables read/write through freed or relocated objects.

Suggested fix -- condition write barrier mode on type.is\_shared, matching the pattern from commit 56cd8297b40:

```
WriteBarrierMode mode = type.is_shared
    ? UPDATE_WRITE_BARRIER : SKIP_WRITE_BARRIER;

```

Apply to all three StoreRefIntoMemory() call sites above. Also fix
RttCanon() to dispatch shared types to shared\_part()->managed\_object\_maps(),
and enable the shared feature under --wasm-jitless in FromFlags().

Related: [bug 42204563](https://issues.chromium.org/issues/42204563) / commit 56cd8297b40.

# Additional Comments

This is an incomplete fix of [bug 42204563](https://issues.chromium.org/issues/42204563) (commit 56cd8297b40). That commit patched constant-expression-interface.cc but missed three
identical SKIP\_WRITE\_BARRIER sites in the Wasm interpreter (DrumBrake).

Two separate bugs are reported here:

1. Missing write barriers in s2s\_StructNew, s2s\_RefArrayNew, and s2s\_ArrayNewFixed (the security-relevant bug).
2. RttCanon() does not dispatch shared types to shared\_part() (a functional bug that also blocks shared types in the interpreter).

The reproduction requires two source patches because shared types are not yet enabled under --wasm-jitless. These patches are not exploits
-- they fix the feature gate and RttCanon so the interpreter can actually execute shared types, exposing the underlying write barrier bug. The write barrier bug itself is in unpatched upstream code.

The fix is straightforward: condition the write barrier mode on type.is\_shared in all three sites, matching the pattern already used in the original fix (56cd8297b40).

# Summary

V8 Wasm interpreter (DrumBrake) missing write barriers for shared struct/array creation

# Custom Questions

#### Type of crash:

Tab crash — the bug is in the V8 Wasm interpreter, which runs in the renderer process. A renderer process maps to a tab (or site isolation group). The crash occurs during Wasm execution within that renderer, not in the browser process.

#### Crash state:

Fatal error in ../../v8/src/heap/heap-write-barrier-inl.h, line 166
Check failed: !WriteBarrier::IsRequired(host, value).

Symbolized stack trace:

#0 v8::base::debug::StackTrace::StackTrace()
v8/src/base/debug/stack\_trace\_posix.cc:395
#1 v8::platform::(anonymous namespace)::PrintStackTrace()
v8/src/libplatform/default-platform.cc:28
#2 V8\_Fatal(char const\*, int, char const\*, ...)
v8/src/base/logging.cc:231
#3 WriteBarrier::VerifySkipWriteBarrier<Object>(Tagged<HeapObject>, Tagged<Object>, WriteBarrierMode)
v8/src/heap/heap-write-barrier-inl.h:166
#4 wasm::Handlers<false>::s2s\_StructNew(...)
v8/src/wasm/interpreter/wasm-interpreter.cc:6025
#5 wasm::WasmInterpreterRuntime::ExecuteFunction(...)
v8/src/wasm/interpreter/wasm-interpreter-runtime.cc:1423
#6 wasm::WasmInterpreterRuntime::ContinueExecution(WasmInterpreterThread\*, bool)
v8/src/wasm/interpreter/wasm-interpreter-runtime.cc
#7 wasm::WasmInterpreter::ContinueExecution(WasmInterpreterThread\*, bool)
v8/src/wasm/interpreter/wasm-interpreter.h:653
#8 wasm::InterpreterHandle::Execute(...)
v8/src/wasm/interpreter/wasm-interpreter-runtime.cc:2887
#9 \_\_RT\_impl\_Runtime\_WasmRunInterpreter(Arguments<>, Isolate\*)
v8/src/wasm/interpreter/wasm-interpreter-runtime.cc:190
#10 Runtime\_WasmRunInterpreter(int, unsigned long\*, Isolate\*)
v8/src/wasm/interpreter/wasm-interpreter-runtime.cc:73
#11 Builtins\_CEntry\_Return1\_ArgvOnStack\_NoBuiltinExit

The crash is a V8\_Fatal triggered by the write barrier verification CHECK at frame #3. Frame #4 is the buggy handler — s2s\_StructNew passes SKIP\_WRITE\_BARRIER when storing a reference into a shared struct allocated in kSharedOld. No registers/exception record because this is a CHECK failure (intentional abort), not a signal-based crash.

#### Reporter credit:

Peter Malone

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [report_010.txt](attachments/report_010.txt) (text/plain, 7.1 KB)
- [poc_interpreter_wb_minimal.js](attachments/poc_interpreter_wb_minimal.js) (text/javascript, 1.7 KB)
- [poc.js](attachments/poc.js) (text/javascript, 4.9 KB)

## Timeline

### pe...@gmail.com (2026-02-09)

Apologies, chrome channel should've been set to "N/A — bug is in V8 source at HEAD, not specific to a Chrome release channel".

I should've submitted this with markdown too not as classic, my bad.

### pe...@gmail.com (2026-02-09)

I did some further testing to see if the missing barrier causes real heap corruption beyond the debug check.

I ran the PoC with --gc-interval at various values to stress the garbage collector. With --gc-interval=50 and explicit gc() calls, no corruption — full GC traces everything transitively so it finds references even without the barrier. But with --gc-interval between 100 and 500 combined with allocation pressure, the GC itself segfaults during marking. It's following a dangling pointer on the heap.

This makes sense — minor GC doesn't see the untracked old-to-young reference, so it relocates or frees the young-gen target. Later when the GC tries to trace through that reference it hits garbage memory. On release builds without V8_VERIFY_WRITE_BARRIERS this corruption would happen silently.

Attached the UAF demo PoC and the crash output below.

Crash output:

V8 is running with experimental features enabled. Stability and security will suffer.
=== UAF Demonstration: Interpreter Write Barrier ===
  Instantiating module...
  Phase 1: Warming up allocator and triggering marking...
  Phase 2: Creating structs during GC pressure...
Received signal 11 SEGV_ACCERR 7426dd2c7ff8
==== C stack trace ===============================
/home/sj/chromium/src/out/v8_drumbrake/d8(___interceptor_backtrace+0x46)[0x6323e5ffeb66]
/home/sj/chromium/src/out/v8_drumbrake/d8(+0x7404899)[0x6323ebd11899]
/lib/x86_64-linux-gnu/libc.so.6(+0x45330)[0x782722045330]
[0x6323c440533b]
[end of stack trace]

### ts...@google.com (2026-02-10)

Drumbrake issues assigned without further triage by Chrome team.

### pa...@microsoft.com (2026-02-10)

@pe...@gmail.com Peter, thanks a lot for reporting this!
To tell the true, the support for shared Wasm types was not in the immediate backlog, but your analysis will be really useful!
I will fix this as you suggested as soon as possible.

### ch...@google.com (2026-02-10)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### ts...@google.com (2026-02-10)

Actually, this is a hard CHECK(), not a DCHECK(). Execution end => DoS => functional bug.

### pe...@gmail.com (2026-02-10)

Thanks for looking at this. I want to flag something about the CHECK if that's alright — the check at heap-write-barrier-inl.h is inside #if V8_VERIFY_WRITE_BARRIERS, which only gets compiled with v8_dcheck_always_on=true. In release Chrome this is all compiled out.

Here's the relevant code in WriteBarrier::ForValue() (heap-write-barrier-inl.h, around line 144):

if (IsSkipWriteBarrierMode(mode)) {
#if V8_VERIFY_WRITE_BARRIERS
    VerifySkipWriteBarrier(host, value, mode);
#endif
    return;  // in release, just returns — no barrier emitted
}

So on release builds there's no CHECK and no crash — the barrier is just silently skipped. 

The impact isn't "CHECK fires ==> DoS", it's "no barrier ==> GC doesn't see the reference ==> silent heap corruption." 

The incremental/concurrent marker misses the shared-old store, which can lead to premature sweeping of objects that are still reachable.

This is the same pattern addressed in commit 56cd8297b40, which changed SKIP_WRITE_BARRIER to include a proper barrier for shared old-space stores in constant-expression-interface.cc. 

The interpreter paths (s2s_StructNew, s2s_RefArrayNew, s2s_ArrayNewFixed) weren't included in that fix. Worth noting that the interpreter's own mutation handlers (s2s_StructSet, s2s_ArraySet) already use UPDATE_WRITE_BARRIER correctly — so the intended pattern is clear, the init paths just got missed.

Would you mind taking another look at severity given the above? Sorry for the trouble here. Thank you!

### ts...@google.com (2026-02-11)

SI_None merely means it doesn't affect a Chrome release as this only ships in other browsers. It is still likely an issue.

### dx...@google.com (2026-02-18)

Project: v8/v8  

Branch:  main  

Author:  Paolo Severini [paolosev@microsoft.com](mailto:paolosev@microsoft.com)  

Link:    <https://chromium-review.googlesource.com/7580859>

[Wasm interpreter] Fix write barriers for shared struct/array

---


Expand for full commit details
```
     
    Add missing GC write barriers for shared struct/array fields in the Wasm 
    interpreter. This is needed to ensure correct behavior when using shared 
    memory with GC objects. 
     
    Bug: 482742896 
    Change-Id: I2d3593e21c23616835eb9060ac5750120b77acee 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7580859 
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
    Commit-Queue: Paolo Severini <paolosev@microsoft.com> 
    Reviewed-by: Daniel Lehmann <dlehmann@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105311}

```

---

Files:

- M `src/execution/frames.cc`
- M `src/wasm/interpreter/wasm-interpreter-runtime.cc`
- M `src/wasm/interpreter/wasm-interpreter-runtime.h`
- M `src/wasm/interpreter/wasm-interpreter.cc`
- M `src/wasm/wasm-objects.cc`

---

Hash: [ca4637f8b73bfb10a449f4ab2a3fab756fbf8b43](https://chromiumdash.appspot.com/commit/ca4637f8b73bfb10a449f4ab2a3fab756fbf8b43)  

Date: Tue Feb 17 16:17:01 2026


---

### wf...@chromium.org (2026-03-11)

drumbrake is behind a gn flag and does not ship with Chrome, so although this might affect Edge which might ship drumbrake, it does not affect Chrome.

### sp...@google.com (2026-03-11)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

Drumbrake is not shipped as part of Chrome hence not eligible VRP

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### ch...@google.com (2026-05-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Drumbrake is not shipped as part of Chrome hence not eligible VRP
> 
> 
> Note that the fact that this issue is not being rewarded does not mean
> that the product team won't fix the issue. We have filed a bug with the product
> team and they will review your report and decide if a fix is required. We'll
> let you know if the issue was fixed.
> 
> Regards, \
> Google Security Bot
> 
> *How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/482742896)*
