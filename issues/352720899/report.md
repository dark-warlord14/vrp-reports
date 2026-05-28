# Security: Debug check failed: !type.is_uninhabited()

| Field | Value |
|-------|-------|
| **Issue ID** | [352720899](https://issues.chromium.org/issues/352720899) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler, Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows |
| **Reporter** | rh...@gmail.com |
| **Assignee** | ml...@chromium.org |
| **Created** | 2024-07-12 |
| **Bounty** | $7,000.00 |

## Description

#### Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

#### VULNERABILITY DETAILS

This bug is similar with <https://issues.chromium.org/issues/342602616>

#### VERSION

Chrome Version: V8 version 12.8.0 (candidate)

Operating System: linux64

#### REPRODUCTION CASE

1. download latest v8-asan `d8-linux-debug-v8-component-95006.zip`
2. run with `./d8 --future --wasm-staging --no-liftoff ./poc.js`

#### FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

```
#
# Fatal error in ../../src/compiler/turboshaft/wasm-gc-typed-optimization-reducer.h, line 228
# Debug check failed: !from_type.is_uninhabited().
#
#
#
#FailureMessage Object: 0x7ffedae67a20
==== C stack trace ===============================

    /home/test_pc/prebuilt-chromium/v8-asan/d8-linux-debug-v8-component-95006/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x743206201a83]
    /home/test_pc/prebuilt-chromium/v8-asan/d8-linux-debug-v8-component-95006/libv8_libplatform.so(+0x190ad) [0x7432061ab0ad]
    /home/test_pc/prebuilt-chromium/v8-asan/d8-linux-debug-v8-component-95006/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x194) [0x7432061e3204]
    /home/test_pc/prebuilt-chromium/v8-asan/d8-linux-debug-v8-component-95006/libv8_libbase.so(+0x2bc25) [0x7432061e2c25]
    /home/test_pc/prebuilt-chromium/v8-asan/d8-linux-debug-v8-component-95006/libv8.so(v8::internal::compiler::turboshaft::WasmGCTypedOptimizationReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::WasmLoadEliminationReducer, v8::internal::compiler::turboshaft::WasmGCTypedOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::TSReducerBase>>::ReduceInputGraphWasmTypeCheckHelper(v8::internal::compiler::turboshaft::V<v8::internal::compiler::turboshaft::WordWithBits<32ul>>, v8::internal::compiler::turboshaft::WasmTypeCheckOp const&)+0x35b) [0x7432054c9ebb]
    /home/test_pc/prebuilt-chromium/v8-asan/d8-linux-debug-v8-component-95006/libv8.so(v8::internal::compiler::turboshaft::WasmGCTypedOptimizationReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::WasmLoadEliminationReducer, v8::internal::compiler::turboshaft::WasmGCTypedOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::TSReducerBase>>::ReduceInputGraphWasmTypeCheck(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::WasmTypeCheckOp const&)+0xbc) [0x7432054bf35c]
    /home/test_pc/prebuilt-chromium/v8-asan/d8-linux-debug-v8-component-95006/libv8.so(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::WasmLoadEliminationReducer, v8::internal::compiler::turboshaft::WasmGCTypedOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::WasmLoadEliminationReducer, v8::internal::compiler::turboshaft::WasmGCTypedOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitOpNoMappingUpdate<false>(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::Block const*)+0x26b) [0x7432054c2deb]
    /home/test_pc/prebuilt-chromium/v8-asan/d8-linux-debug-v8-component-95006/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::WasmLoadEliminationReducer, v8::internal::compiler::turboshaft::WasmGCTypedOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::WasmLoadEliminationReducer, v8::internal::compiler::turboshaft::WasmGCTypedOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitBlockBody<(v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::WasmLoadEliminationReducer, v8::internal::compiler::turboshaft::WasmGCTypedOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::WasmLoadEliminationReducer, v8::internal::compiler::turboshaft::WasmGCTypedOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::CanHavePhis)1, (v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::WasmLoadEliminationReducer, v8::internal::compiler::turboshaft::WasmGCTypedOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::WasmLoadEliminationReducer, v8::internal::compiler::turboshaft::WasmGCTypedOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::ForCloning)0, false>(v8::internal::compiler::turboshaft::Block const*, int)+0x40a) [0x7432054e9fca]
    /home/test_pc/prebuilt-chromium/v8-asan/d8-linux-debug-v8-component-95006/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::WasmLoadEliminationReducer, v8::internal::compiler::turboshaft::WasmGCTypedOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::WasmLoadEliminationReducer, v8::internal::compiler::turboshaft::WasmGCTypedOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitBlock<false>(v8::internal::compiler::turboshaft::Block const*)+0xde) [0x7432054e988e]
    /home/test_pc/prebuilt-chromium/v8-asan/d8-linux-debug-v8-component-95006/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::WasmLoadEliminationReducer, v8::internal::compiler::turboshaft::WasmGCTypedOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::WasmLoadEliminationReducer, v8::internal::compiler::turboshaft::WasmGCTypedOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitAllBlocks<false>()+0xe3) [0x7432054e96a3]
    /home/test_pc/prebuilt-chromium/v8-asan/d8-linux-debug-v8-component-95006/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::WasmLoadEliminationReducer, v8::internal::compiler::turboshaft::WasmGCTypedOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::WasmLoadEliminationReducer, v8::internal::compiler::turboshaft::WasmGCTypedOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitGraph<false>()+0xaf) [0x7432054b17cf]
    /home/test_pc/prebuilt-chromium/v8-asan/d8-linux-debug-v8-component-95006/libv8.so(v8::internal::compiler::turboshaft::CopyingPhase<v8::internal::compiler::turboshaft::WasmLoadEliminationReducer, v8::internal::compiler::turboshaft::WasmGCTypedOptimizationReducer>::Run(v8::internal::compiler::turboshaft::PipelineData*, v8::internal::Zone*)+0x105) [0x74320549f215]
    /home/test_pc/prebuilt-chromium/v8-asan/d8-linux-debug-v8-component-95006/libv8.so(v8::internal::compiler::turboshaft::WasmGCOptimizePhase::Run(v8::internal::compiler::turboshaft::PipelineData*, v8::internal::Zone*)+0x76) [0x74320549f086]
    /home/test_pc/prebuilt-chromium/v8-asan/d8-linux-debug-v8-component-95006/libv8.so(auto v8::internal::compiler::turboshaft::Pipeline::Run<v8::internal::compiler::turboshaft::WasmGCOptimizePhase>()+0xda) [0x743205305d1a]
    /home/test_pc/prebuilt-chromium/v8-asan/d8-linux-debug-v8-component-95006/libv8.so(v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::wasm::WasmDetectedFeatures*, v8::internal::compiler::CallDescriptor*)+0x665) [0x743205304735]
    /home/test_pc/prebuilt-chromium/v8-asan/d8-linux-debug-v8-component-95006/libv8.so(v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmDetectedFeatures*)+0x2b7) [0x7432055c8467]
    /home/test_pc/prebuilt-chromium/v8-asan/d8-linux-debug-v8-component-95006/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmDetectedFeatures*)+0x67a) [0x743204a69eaa]
    /home/test_pc/prebuilt-chromium/v8-asan/d8-linux-debug-v8-component-95006/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmDetectedFeatures*)+0x140) [0x743204a69420]
    /home/test_pc/prebuilt-chromium/v8-asan/d8-linux-debug-v8-component-95006/libv8.so(v8::internal::wasm::CompileLazy(v8::internal::Isolate*, v8::internal::Tagged<v8::internal::WasmTrustedInstanceData>, int)+0x413) [0x743204ab6823]
    /home/test_pc/prebuilt-chromium/v8-asan/d8-linux-debug-v8-component-95006/libv8.so(+0x3f1ec76) [0x74320491ec76]
    /home/test_pc/prebuilt-chromium/v8-asan/d8-linux-debug-v8-component-95006/libv8.so(v8::internal::Runtime_WasmCompileLazy(int, unsigned long*, v8::internal::Isolate*)+0x90) [0x74320491e610]
    /home/test_pc/prebuilt-chromium/v8-asan/d8-linux-debug-v8-component-95006/libv8.so(+0x1edd6d7) [0x7432028dd6d7]
Trace/breakpoint trap

```

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 147.2 KB)

## Timeline

### rh...@gmail.com (2024-07-12)

additional info:

I bisected the commits to find the cause of the crash and determined that it occurs on commit <https://chromium-review.googlesource.com/c/v8/v8/+/5385442>. However, there is a possibility I could be mistaken.

### cl...@appspot.gserviceaccount.com (2024-07-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5198611883163648.

### ja...@chromium.org (2024-07-15)

Thanks for the bug report and proof of concept. I've uploaded this to clusterfuzz. Following the shepherding documentation I'm tentatively assigning this S1 (High) and Found in of extended stable (126). These are provisional labels and may change.

### ja...@chromium.org (2024-07-15)

Assigning to the current v8 security shepherd.

### ml...@chromium.org (2024-07-16)

Here is a minimized reproducer:

```
// Flags: --future --wasm-staging --no-liftoff --no-wasm-lazy-compilation
// Flags: --no-wasm-loop-peeling --no-wasm-loop-unrolling
d8.file.execute('test/mjsunit/wasm/wasm-module-builder.js');

const builder = new WasmModuleBuilder();
let $sig115 = builder.addType(makeSig([kWasmI32], []));
let $sig201 = builder.addType(makeSig([kWasmAnyRef], [kWasmAnyRef]));

builder.addFunction(undefined, $sig115).exportAs("main").addBody([
    kExprLocalGet, 0,
    kExprIf, kWasmVoid,
      ...wasmI32Const(42),
      kGCPrefix, kExprRefI31,
      kExprBlock, $sig201,
        kGCPrefix, kExprBrOnCastFail, 0b11, 0, kAnyRefCode, kStructRefCode,
        kGCPrefix, kExprRefCastNull, kNullRefCode,
      kExprEnd,
      kExprUnreachable,
    kExprEnd,
]);

let instance = builder.instantiate({});

```

I'll investigate the root cause of the issue next.

### ml...@chromium.org (2024-07-16)

The `DCHECK` we are hitting here shows that we lose "statically known" type information when running our `WasmGCTypedOptimizationReducer`.

This is caused by `br_on_cast_fail` not adding the information to the graph that in the fallthrough case the cast succeeded, so the type is narrowed to the target type of the `br_on_cast_fail` instruction.

As this is just a missed optimization, this is not a security issue. The `DCHECK` can only be triggered in dynamically unreachable code, so even if we generated anything wrong for the `ref.cast null`, it would not impact security.

### ml...@chromium.org (2024-07-16)

Thanks a lot for fuzzing V8 and finding these issues.

Just as a note: Those initial reproducers are very large and a lot of time is spent trying to minimize it down to something that can be investigated properly. Have you considered limiting the size of the generated wasm module more? Most of these issues do not rely on hundreds of functions (having a few is very helpful for things like inlining though).

### ap...@google.com (2024-07-16)

Project: v8/v8
Branch: main

commit dad3b1c03cf8eed08ae66c126d5fa17acf23d038
Author: Matthias Liedtke <mliedtke@chromium.org>
Date:   Tue Jul 16 16:09:37 2024

    [turboshaft][wasm] Fix missing type propagation on br_on_cast_fail fallthrough
    
    For a br_on_cast_fail that always fails, the fallthrough branch is
    dynamically unreachable. The type reducer does not figure that
    out but can end up in the situation of knowing the source type and
    having a static type that doesn't fit to that (i.e. their intersection
    is zero), which should not be possible in reachable code.
    
    This fixes the DCHECK by annotating the fallthrough type on
    br_on_cast_fail.
    
    There is also a missed optimization as for br_on_cast the analyzer
    correctly handles the branch on a condition that is WasmTypeCheckOp
    but for br_on_cast_fail the condition is an equality ComparisonOp of a
    WasmTypeCheckOp and a Word32Constant(0) which it does not use to
    propagate the type check's narrowing.
    This is not addressed in this CL.
    
    Fixed: 352720899
    Change-Id: I2074dbe84f9cf124ff7e9b5bc28f8bb7e798d491
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5713611
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
    Auto-Submit: Matthias Liedtke <mliedtke@chromium.org>
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95057}

M       src/wasm/turboshaft-graph-interface.cc
A       test/mjsunit/regress/wasm/regress-352720899-2.js
A       test/mjsunit/regress/wasm/regress-352720899.js
M       tools/wasm/mjsunit-module-disassembler-impl.h

https://chromium-review.googlesource.com/5713611


### rh...@gmail.com (2024-07-16)

re #8,

> > Have you considered limiting the size of the generated WASM module further?

I apologize for not providing a minimized PoC earlier. I have set a limit for each WASM function to be no more than 10, along with other important constraints, but none exceeding 10. Before reporting this issue, I attempted to use `wasm-reduce` but failed to remove dead code and unnecessary functions.

I would like to report a minimized POC, but I have no experience in doing so. Could you please share the steps for creating a minimized POC, similar to what was done in [comment #6](https://issues.chromium.org/issues/352720899#comment6)? Any information on reducing WASM modules would be helpful for me in future issue reporting.

Thank you for the fixing this issue.

### ml...@chromium.org (2024-07-16)

I don't have much experience for minifying with `wasm-reduce`, at least for our fuzzers we had the issue that what our fuzzers generated contained features that `wasm-reduce` does not / did not support (afaik multi-value-returns).

For [comment #6](https://issues.chromium.org/issues/352720899#comment6), I built `wami` (it's a test binary that you can build from the v8 repository) and ran it with `--mjsunit` on the `poc.js` (it extracts the wasm module and generates something that should be an `mjsunit` test case).

Unfortunately, there are still a few bugs in there, so I needed some manual changes (e.g. for `br_on_cast`). And then I tried to minimize the function in which the crash occurred until I couldn't remove any more instructions from it and then looked at its dependencies and extracted the functions and its dependencies and the types out to a new file to then continuing reduction there etc. :)

So, I don't have a good automated way to reduce these modules yet, which means it helps if the initial module isn't too large.

I will bring it up internally so that `wasm-reduce` can hopefully be used in the future.

### rh...@gmail.com (2024-07-16)

> For [comment #6](https://issues.chromium.org/issues/352720899#comment6), I built wami (it's a test binary that you can build from the v8 repository) and ran it with --mjsunit on the poc.js (it extracts the wasm module and generates something that should be an mjsunit test case).

Thank you very much. I think that will be good start for me.

### 24...@project.gserviceaccount.com (2024-07-17)

ClusterFuzz testcase 5198611883163648 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=95056:95057

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### am...@chromium.org (2024-07-17)

Thank you for the report. Since this does not appear to be an exploitable security issue, this report is unfortunately not eligible for a Chrome VRP reward.

### pe...@google.com (2024-10-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/352720899)*
