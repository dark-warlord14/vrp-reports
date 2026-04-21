# Security: Debug check failed: !can_be_invalid implies result.valid().

| Field | Value |
|-------|-------|
| **Issue ID** | [40948479](https://issues.chromium.org/issues/40948479) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2023-12-04 |
| **Bounty** | $10,000.00 |

## Description

Title : Debug check failed: !can_be_invalid implies result.valid(). in v8

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 91054
    - link: https://crrev.com/ce5999e86e234dbd7000989556567a69e1ecafcf 
- Commit Message

```
commit ce5999e86e234dbd7000989556567a69e1ecafcf
Author: Manos Koukoutos <manoskouk@chromium.org>
Date:   Mon Nov 20 12:56:04 2023 +0100

    [turboshaft][wasm] Enable loop peeling
    
    Bug: v8:14108
    Change-Id: I360809827d10781efae9354f6eb2354d29e827f3
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5033018
    Commit-Queue: Manos Koukoutos <manoskouk@chromium.org>
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#91054}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-91313/d8 --turboshaft-wasm poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/compiler/turboshaft/copying-phase.h, line 194
# Debug check failed: !can_be_invalid implies result.valid().
#
#
#
#FailureMessage Object: 0x7f6e85ff8ac0
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f6eaa2f4c73]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(+0x19add) [0x7f6eaa29badd]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x154) [0x7f6eaa2d4d14]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(+0x2b7d5) [0x7f6eaa2d47d5]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::MapToNewGraph<false>(v8::internal::compiler::turboshaft::OpIndex, int)+0x1de) [0x7f6ea9c0341e]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::LoopPeelingReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::ReduceInputGraphPhi(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::PhiOp const&)+0x68) [0x7f6ea9c00908]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitOpNoMappingUpdate<false>(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::Block const*)+0x1b5) [0x7f6ea9c01985]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitBlock<false>(v8::internal::compiler::turboshaft::Block const*)+0x1d3) [0x7f6ea9c06613]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::Block* v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::CloneSubGraph<v8::internal::ZoneSet<v8::internal::compiler::turboshaft::Block*, v8::internal::compiler::turboshaft::LoopFinder::BlockCmp>>(v8::internal::ZoneSet<v8::internal::compiler::turboshaft::Block*, v8::internal::compiler::turboshaft::LoopFinder::BlockCmp>, bool, bool)+0x22d) [0x7f6ea9c05e4d]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::LoopPeelingReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::PeelFirstIteration(v8::internal::compiler::turboshaft::Block*)+0x1c8) [0x7f6ea9c02578]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::LoopPeelingReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::ReduceInputGraphGoto(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::GotoOp const&)+0xa1) [0x7f6ea9c000c1]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitOpNoMappingUpdate<false>(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::Block const*)+0x10c) [0x7f6ea9c018dc]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitBlock<false>(v8::internal::compiler::turboshaft::Block const*)+0x3d0) [0x7f6ea9c06810]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitAllBlocks<false>()+0xe3) [0x7f6ea9c4e003]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::CopyingPhaseImpl<v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer>::Run(v8::internal::Zone*)+0x18d) [0x7f6ea9bf3bad]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(auto v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::turboshaft::LoopPeelingPhase>()+0xd0) [0x7f6ea983dd60]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::CallDescriptor*)+0x872) [0x7f6ea98481e2]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmFeatures*)+0x2b1) [0x7f6ea9a98241]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x72b) [0x7f6ea9046efb]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x192) [0x7f6ea9046342]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(+0x3aa594a) [0x7f6ea90a594a]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(+0x3aa5185) [0x7f6ea90a5185]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xd3) [0x7f6eaa29a823]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0xc3) [0x7f6eaa29d213]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(+0x4a629) [0x7f6eaa2f3629]
    /lib/x86_64-linux-gnu/libc.so.6(+0x94ac3) [0x7f6ea4c94ac3]
    /lib/x86_64-linux-gnu/libc.so.6(+0x126a40) [0x7f6ea4d26a40]

```

## Other
Please note to include the flags `--turboshaft-wasm` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.1.0 - 12.1.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-91313.zip
2. Run: `d8 --turboshaft-wasm poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Jerry


When I was sorting out the crash, I found another case of the same introduction point, but since the introduction point I could locate was just turning on the loop peeling flag switch, I couldn't be completely sure that they were the same problem with the same root cause.

If they are not the same problem, please split it into two reports, or identify it as two problems, to ensure that I can get the bug bounty for both vulnerabilities, thank you.


## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-91313/d8 --turboshaft-wasm poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/compiler/turboshaft/operations.h, line 817
# Debug check failed: Is<Op>().
#
#
#
#FailureMessage Object: 0x7f2d6bffce30
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f2da5e33c73]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(+0x19add) [0x7f2da5ddaadd]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x154) [0x7f2da5e13d14]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(+0x2b7d5) [0x7f2da5e137d5]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::WasmGCTypeAnalyzer::ProcessAllocateArray(v8::internal::compiler::turboshaft::WasmAllocateArrayOp const&)+0x13e) [0x7f2da55ebe6e]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::WasmGCTypeAnalyzer::ProcessOperations(v8::internal::compiler::turboshaft::Block const&)+0xc6) [0x7f2da55ea3d6]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::WasmGCTypeAnalyzer::Run()+0x16d) [0x7f2da55e8edd]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::WasmLoadEliminationReducer, v8::internal::compiler::turboshaft::WasmGCTypeReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::WasmLoadEliminationReducer, v8::internal::compiler::turboshaft::WasmGCTypeReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitGraph<false>()+0x46) [0x7f2da55b8706]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::CopyingPhaseImpl<v8::internal::compiler::turboshaft::WasmLoadEliminationReducer, v8::internal::compiler::turboshaft::WasmGCTypeReducer>::Run(v8::internal::Zone*)+0x120) [0x7f2da55b8510]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(auto v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::turboshaft::WasmGCOptimizePhase>()+0xd0) [0x7f2da5449370]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::CallDescriptor*)+0x8a6) [0x7f2da5448216]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmFeatures*)+0x2b1) [0x7f2da5698241]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x72b) [0x7f2da4c46efb]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x192) [0x7f2da4c46342]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(+0x3aa594a) [0x7f2da4ca594a]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(+0x3aa5185) [0x7f2da4ca5185]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xd3) [0x7f2da5dd9823]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0xc3) [0x7f2da5ddc213]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(+0x4a629) [0x7f2da5e32629]
    /lib/x86_64-linux-gnu/libc.so.6(+0x94ac3) [0x7f2da0894ac3]
    /lib/x86_64-linux-gnu/libc.so.6(+0x126a40) [0x7f2da0926a40]

```

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 2.8 KB)
- [poc1.js](attachments/poc1.js) (text/plain, 8.8 KB)
- [poc2.js](attachments/poc2.js) (text/plain, 4.6 KB)
- [poc3.js](attachments/poc3.js) (text/plain, 18.9 KB)
- [poc1.js](attachments/poc1.js) (text/plain, 8.8 KB)
- [poc.js](attachments/poc.js) (text/plain, 2.8 KB)
- [poc2.js](attachments/poc2.js) (text/plain, 4.6 KB)
- [poc3.js](attachments/poc3.js) (text/plain, 18.9 KB)

## Timeline

### je...@gmail.com (2023-12-04)

Title : Debug check failed: !can_be_invalid implies result.valid(). in v8

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 91054
    - link: https://crrev.com/ce5999e86e234dbd7000989556567a69e1ecafcf 
- Commit Message

```
commit ce5999e86e234dbd7000989556567a69e1ecafcf
Author: Manos Koukoutos <manoskouk@chromium.org>
Date:   Mon Nov 20 12:56:04 2023 +0100

    [turboshaft][wasm] Enable loop peeling
    
    Bug: v8:14108
    Change-Id: I360809827d10781efae9354f6eb2354d29e827f3
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5033018
    Commit-Queue: Manos Koukoutos <manoskouk@chromium.org>
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#91054}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-91313/d8 --turboshaft-wasm poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/compiler/turboshaft/copying-phase.h, line 194
# Debug check failed: !can_be_invalid implies result.valid().
#
#
#
#FailureMessage Object: 0x7f6e85ff8ac0
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f6eaa2f4c73]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(+0x19add) [0x7f6eaa29badd]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x154) [0x7f6eaa2d4d14]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(+0x2b7d5) [0x7f6eaa2d47d5]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::MapToNewGraph<false>(v8::internal::compiler::turboshaft::OpIndex, int)+0x1de) [0x7f6ea9c0341e]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::LoopPeelingReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::ReduceInputGraphPhi(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::PhiOp const&)+0x68) [0x7f6ea9c00908]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitOpNoMappingUpdate<false>(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::Block const*)+0x1b5) [0x7f6ea9c01985]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitBlock<false>(v8::internal::compiler::turboshaft::Block const*)+0x1d3) [0x7f6ea9c06613]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::Block* v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::CloneSubGraph<v8::internal::ZoneSet<v8::internal::compiler::turboshaft::Block*, v8::internal::compiler::turboshaft::LoopFinder::BlockCmp>>(v8::internal::ZoneSet<v8::internal::compiler::turboshaft::Block*, v8::internal::compiler::turboshaft::LoopFinder::BlockCmp>, bool, bool)+0x22d) [0x7f6ea9c05e4d]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::LoopPeelingReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::PeelFirstIteration(v8::internal::compiler::turboshaft::Block*)+0x1c8) [0x7f6ea9c02578]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::LoopPeelingReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::ReduceInputGraphGoto(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::GotoOp const&)+0xa1) [0x7f6ea9c000c1]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitOpNoMappingUpdate<false>(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::Block const*)+0x10c) [0x7f6ea9c018dc]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitBlock<false>(v8::internal::compiler::turboshaft::Block const*)+0x3d0) [0x7f6ea9c06810]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitAllBlocks<false>()+0xe3) [0x7f6ea9c4e003]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::CopyingPhaseImpl<v8::internal::compiler::turboshaft::LoopPeelingReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer>::Run(v8::internal::Zone*)+0x18d) [0x7f6ea9bf3bad]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(auto v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::turboshaft::LoopPeelingPhase>()+0xd0) [0x7f6ea983dd60]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::CallDescriptor*)+0x872) [0x7f6ea98481e2]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmFeatures*)+0x2b1) [0x7f6ea9a98241]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x72b) [0x7f6ea9046efb]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x192) [0x7f6ea9046342]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(+0x3aa594a) [0x7f6ea90a594a]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(+0x3aa5185) [0x7f6ea90a5185]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xd3) [0x7f6eaa29a823]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0xc3) [0x7f6eaa29d213]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(+0x4a629) [0x7f6eaa2f3629]
    /lib/x86_64-linux-gnu/libc.so.6(+0x94ac3) [0x7f6ea4c94ac3]
    /lib/x86_64-linux-gnu/libc.so.6(+0x126a40) [0x7f6ea4d26a40]

```

## Other
Please note to include the flags `--turboshaft-wasm` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.1.0 - 12.1.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-91313.zip
2. Run: `d8 --turboshaft-wasm poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Jerry

### [Deleted User] (2023-12-04)

[Empty comment from Monorail migration]

### sr...@google.com (2023-12-04)

Setting provisional severity high but not sure what the impact is.

[Monorail components: Blink>JavaScript>WebAssembly]

### je...@gmail.com (2023-12-05)

When I was sorting out the crash, I found another case of the same introduction point, but since the introduction point I could locate was just turning on the loop peeling flag switch, I couldn't be completely sure that they were the same problem with the same root cause.

If they are not the same problem, please split it into two reports, or identify it as two problems, to ensure that I can get the bug bounty for both vulnerabilities, thank you.


## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-91313/d8 --turboshaft-wasm poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/compiler/turboshaft/operations.h, line 817
# Debug check failed: Is<Op>().
#
#
#
#FailureMessage Object: 0x7f2d6bffce30
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f2da5e33c73]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(+0x19add) [0x7f2da5ddaadd]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x154) [0x7f2da5e13d14]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(+0x2b7d5) [0x7f2da5e137d5]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::WasmGCTypeAnalyzer::ProcessAllocateArray(v8::internal::compiler::turboshaft::WasmAllocateArrayOp const&)+0x13e) [0x7f2da55ebe6e]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::WasmGCTypeAnalyzer::ProcessOperations(v8::internal::compiler::turboshaft::Block const&)+0xc6) [0x7f2da55ea3d6]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::WasmGCTypeAnalyzer::Run()+0x16d) [0x7f2da55e8edd]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::WasmLoadEliminationReducer, v8::internal::compiler::turboshaft::WasmGCTypeReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::WasmLoadEliminationReducer, v8::internal::compiler::turboshaft::WasmGCTypeReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitGraph<false>()+0x46) [0x7f2da55b8706]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::CopyingPhaseImpl<v8::internal::compiler::turboshaft::WasmLoadEliminationReducer, v8::internal::compiler::turboshaft::WasmGCTypeReducer>::Run(v8::internal::Zone*)+0x120) [0x7f2da55b8510]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(auto v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::turboshaft::WasmGCOptimizePhase>()+0xd0) [0x7f2da5449370]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::CallDescriptor*)+0x8a6) [0x7f2da5448216]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmFeatures*)+0x2b1) [0x7f2da5698241]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x72b) [0x7f2da4c46efb]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x192) [0x7f2da4c46342]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(+0x3aa594a) [0x7f2da4ca594a]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(+0x3aa5185) [0x7f2da4ca5185]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xd3) [0x7f2da5dd9823]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0xc3) [0x7f2da5ddc213]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(+0x4a629) [0x7f2da5e32629]
    /lib/x86_64-linux-gnu/libc.so.6(+0x94ac3) [0x7f2da0894ac3]
    /lib/x86_64-linux-gnu/libc.so.6(+0x126a40) [0x7f2da0926a40]

```



### ma...@chromium.org (2023-12-05)

[Empty comment from Monorail migration]

### ma...@chromium.org (2023-12-05)

Darius: `poc.js` seems to be related to a loop peeling bug. Can you PTAL?

### je...@gmail.com (2023-12-05)

Hello, please check all pocs. They may be related to two different vulnerabilities.

### dm...@chromium.org (2023-12-05)

Regarding `poc.js`: the initial graph is invalid: Phi 83 has 175 as backedge input, but 175 is defined in block 12, which does not dominate the backedge. Looks like a wasm graph builder issue, so back to you Manos ;)

### gi...@appspot.gserviceaccount.com (2023-12-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/7d113bf309001a124498f2049510ab0e6e038dbe

commit 7d113bf309001a124498f2049510ab0e6e038dbe
Author: Manos Koukoutos <manoskouk@chromium.org>
Date: Tue Dec 05 11:21:43 2023

[turboshaft][wasm] Resolve Phi of RttCanons

Under specific circumstances involving a combination of the
ValueNumberingReducer and loop unrolling, we ended up with a phi as
an rtt input for a wasm-gc allocation. This was not handled correctly
by the `WasmGCTypeReducer`, which expected an `RttCanonOp` input.
We are fixing this by resolving phis to identical rtts in the
RequiredOptimizationReducer.

Bug: chromium:1507779
Change-Id: Iacafc6982ec2a22655203a47cbb8d3f0a6785058
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5088207
Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
Commit-Queue: Manos Koukoutos <manoskouk@chromium.org>
Cr-Commit-Position: refs/heads/main@{#91355}

[modify] https://crrev.com/7d113bf309001a124498f2049510ab0e6e038dbe/src/compiler/turboshaft/required-optimization-reducer.h
[add] https://crrev.com/7d113bf309001a124498f2049510ab0e6e038dbe/test/mjsunit/regress/wasm/regress-1507779.js


### dm...@chromium.org (2023-12-05)

[Empty comment from Monorail migration]

### je...@gmail.com (2023-12-06)

Thank you for your prompt fix. After my testing, using the poc.js provided in the issue, we are able to trigger a non-null address segment fault on the release version. This is clearly a serious security issue, and I will continue to investigate its exploit.

```
./d8 poc.js --turboshaft-wasm
Received signal 11 SEGV_MAPERR 7fcf40019bb8

==== C stack trace ===============================

 [0x55fbb9c89757]
 [0x7fcf25842520]
 [0x55fbb98df78e]
 [0x55fbb98dc86e]
 [0x55fbb98e2f61]
 [0x55fbb98e1fa8]
 [0x55fbb98df90b]
 [0x55fbb98dc923]
 [0x55fbb98db93a]
 [0x55fbb98db760]
 [0x55fbb9707f9f]
 [0x55fbb970e2ad]
 [0x55fbb9839a9b]
 [0x55fbb936cc9b]
 [0x55fbb936c3a2]
 [0x55fbb9397d91]
 [0x55fbb9397767]
 [0x55fbb9c8aa8b]
 [0x55fbb9c8d92e]
 [0x55fbb9c86bbf]
 [0x7fcf25894ac3]
 [0x7fcf25926a40]
[end of stack trace]
[1]    3971469 segmentation fault  ./d8 poc.js --turboshaft-wasm
```

### dm...@chromium.org (2023-12-06)

A note on poc.js: I don't think that the bug it showcases can be exploited. The bug comes from the fact that an input of a Phi is not defined in all of the control paths lead to the Phi (in particular, the input from the backedge of a loop phi does not dominate the backedge). Then:
  - If no optimizations trigger, I think that this should lead to a CHECK failure in the register allocator (which is safe, because it's a CHECK failure).
  - if any control-flow related optimization triggers (branch elimination, loop peeling, loop unrolling), this should lead to the input of a Phi being OpIndex::Invalid() instead of a valid OpIndex. This in turn will probably lead to an out-of-bound access in some array around offset +-2**32, which should most of the time lead to a segfault. When it doesn't segfault, this could lead to incorrect information being propagated throughout the pipeline, which could eventually lead to generating wrong code, but I don't think that one can reliably control what happens in such cases.

In poc.js in particular, 
  - When loop peeling is enabled, we segfault when trying to access an array at offset 0xffffffff. 
  - When loop peeling is disabled, the Phi with the wrong inputs is unused and is thus removed from the graph quickly, so it's safe.

Let me know if you disagree, I'm not a security expert, and I might have missed something :)

(also, I didn't look at the other repros, so they might be more exploitable)

### je...@gmail.com (2023-12-06)

Thanks for the reply, I'm still investigating its exploitability and I'm trying to exploit it on a **32-bit d8**. 

Note that on 32-bit offset 0xffffffff will apparently not cause a crash, this will result in a forward out-of-bounds read and write. 
with a suitable heap layout I think exploit is possible.

I'm not sure if it can be done yet, but I think it's a security bug. 

### je...@gmail.com (2023-12-06)

[Comment Deleted]

### je...@gmail.com (2023-12-06)

Please consider the 32-bit environment, which continues to be extensively used and has a considerable impact. :)
When loop peeling is enabled, it will cause the 32-bit version of V8 to trigger a forward out-of-bounds write when trying to access an array at offset 0xffffffff, instead of directly causing a segmentation fault.

### je...@gmail.com (2023-12-06)

## Exploit Details

[0] In src/compiler/turboshaft/graph.h, the poc will result in an out-of-bounds access. At this location, there is an accumulation operation on the 'saturated_use_count' member of the 'operation.' And at this particular instance, 'input.offset()' is set to 0xffffffff.
```
template <class Op>
void IncrementInputUses(const Op& op) {
  for (OpIndex input : op.inputs()) {
    Get(input).saturated_use_count.Incr(); // ==> [0]
  }
}
```

[1] Subsequently, the code calls 'graph->operations.get(input)' as follows:
```
OperationStorageSlot* Get(OpIndex idx) {
  DCHECK_LT(idx.offset() / sizeof(OperationStorageSlot), size());
  return reinterpret_cast<OperationStorageSlot*>(
      reinterpret_cast<Address>(begin_) + idx.offset()); // ==> [1]
}
```

[2] Therefore, the code at [0] is ultimately equivalent to:
```
*(uint8_t*)(graph->operations.begin_ + input.offset() + 1) += 1; // input.offset() == 0xffffffff
```

In a 64-bit environment, this may result in an illegal address access. However, in a 32-bit d8 environment, it is a valid address access. In 32-bit, it is equivalent to:
```
*(uint8_t*)(graph->operations.begin_ + 0xffffffff + 1) += 1;
```

Carry-over in 32-bit will be lost, and the final calculated address is:
```
*(uint8_t*)graph->operations.begin_ += 1;
```

This leads to a misaligned write. The 'begin_' pointer points to the first byte of the opcode field of the first operation. This will result in the following exploitation scenario:

1. The opcode of the first operation is incorrectly changed to any opcode desired by the attacker.
2. Confusion arises between the 'saturated_use_count' of some operations and the opcode of the first operation.

**Furthermore, the status of this issue should be updated to "FIXED".**



### jk...@chromium.org (2023-12-06)

With the fix in #9 and crrev.com/c/5095095, all four poc{,1,2,3}.js seem to just run forever now, with both ia32.debug and x64.debug builds. So the remaining issue appears to have been a dupe of https://crbug.com/chromium/1507751.

Requesting merge of #9 to the just-created branch.

### jk...@chromium.org (2023-12-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

Merge rejected: M121 is already shipping to beta and this issue is marked as a Pri-2, Pri-3, or Type-Feature.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2023-12-06)

Requesting merge again with higher priority.

### [Deleted User] (2023-12-06)

Merge review required: M121 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-12-06)

[Description Changed]

### am...@chromium.org (2023-12-06)

Sheriffbot is not asking for a merge because of the priority but also because this issue is marked SI-None, as we don't generally backmerge issues triaged as SI-None unless that code has been enabled or is going to OT in a particular release cycle for which merge is being requested.
If the bisect presented is correct, this issue should be FoundIn-121, sroetteger@ label this as SI-None during triage so it would be helpful to understand that before making a merge decision here. I'm tentatively updating as FoundIn-121 but leaving the SI-None label. I've reached out to sroettger@ to understand the reasoning for the triage as SI-None. 

### jk...@chromium.org (2023-12-06)

#23: Presumably it's SI-None because this code is still behind a flag. However, we would like to (gradually) enable this flag on 121 via Finch, mostly in order to learn about any as yet undetected issues with it, which of course we can only do if we fix known issues first. That's why we would like to merge this to 121.

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-12-06)

Ah yeah, if the plan is to enable this flag in Finch in 121, we can absolutely consider this for backmerge. First M121 Beta already was already cut for today's release, let's let this get a bit more bake time before backmerge for M121 update. Thanks! 

### dm...@chromium.org (2023-12-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-12-12)

I was remiss in updating here yesterday, but in reviewing stability and perf data related to this fix I ran across a crash that looked like a potential security issue. It was crashing on few clients below the crash auto bug filer threshold, so I erred on the side of caution and opened it as a bug for investigation: https://crbug.com/chromium/1510626 before approving this merge. That has been now investigated by the folks working on turboshaft-wasm and has been attributed to a different bug, and has since been resolved. After re-reviewing crash data this morning, approving merges of this fix to 121. 
Please merge this fix to 12.1-lkgr as soon as possible so this fix can be including in tomorrow's M121 Beta. 

### go...@google.com (2023-12-12)

Please merge your change to M121 before 2:00 PM PT today so we can take it in for tomorrow's beta (Last Beta release before holiday freeze).

Branch details: https://chromiumdash.appspot.com/branches

### jk...@chromium.org (2023-12-12)

The merge is in flight: https://chromium-review.googlesource.com/c/v8/v8/+/5116183
Its timeline for reaching 12.1-lkgr now depends on the speed of various bots, no further human interaction is necessary.

### ma...@chromium.org (2023-12-13)

[Empty comment from Monorail migration]

### am...@google.com (2023-12-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-12-14)

Congratulations! The Chrome VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-12-15)

[Empty comment from Monorail migration]

### is...@google.com (2023-12-15)

This issue was migrated from crbug.com/chromium/1507779?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ap...@google.com (2024-03-20)

Project: v8/v8
Branch: refs/branch-heads/12.2

commit 4a92c1a90a5a8b904505e5ca8bff094376dff38c
Author: Choongwoo Han <choongwoo.han@microsoft.com>
Date:   Mon Mar 11 11:24:19 2024

    Merged: [osr] Avoid baseline compile in the middle of OSR
    
    In InterpreterAssembler::OnStackReplacement, code is checked whether
    it's marked for deoptimization before calling Budget Interrupt. And,
    the interrupt can trigger GC and deoptimize the OSR code when running
    baseline compile, which will lead to jumping to the deoptimized OSR
    code. Thus, avoid baseline compilation if the function has optimized OSR
    code.
    
    (cherry picked from commit 78efe86c8a87994da34afc4bf37dc444c58587e5)
    
    Bug: chromium:1507779
    Change-Id: I45284d7a834f379c88452c78bdbc977676ba4d32
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5381227
    Reviewed-by: Toon Verwaest <verwaest@chromium.org>
    Commit-Queue: Choongwoo Han <choongwoo.han@microsoft.com>
    Cr-Commit-Position: refs/branch-heads/12.2@{#46}
    Cr-Branched-From: 6eb5a9616aa6f8c705217aeb7c7ab8c037a2f676-refs/heads/12.2.281@{#1}
    Cr-Branched-From: 44cf56d850167c6988522f8981730462abc04bcc-refs/heads/main@{#91934}

M       src/execution/tiering-manager.cc

https://chromium-review.googlesource.com/5381227


### ap...@google.com (2024-03-20)

Project: v8/v8
Branch: refs/branch-heads/12.3

commit 69cecb7ff8c363756b5969771c4ddc613f254702
Author: Choongwoo Han <choongwoo.han@microsoft.com>
Date:   Mon Mar 11 11:24:19 2024

    Merged: [osr] Avoid baseline compile in the middle of OSR
    
    In InterpreterAssembler::OnStackReplacement, code is checked whether
    it's marked for deoptimization before calling Budget Interrupt. And,
    the interrupt can trigger GC and deoptimize the OSR code when running
    baseline compile, which will lead to jumping to the deoptimized OSR
    code. Thus, avoid baseline compilation if the function has optimized OSR
    code.
    
    (cherry picked from commit 78efe86c8a87994da34afc4bf37dc444c58587e5)
    
    Bug: chromium:1507779
    Change-Id: Ife40cff04763917949ebc41fbb7624b13daeb802
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5381523
    Reviewed-by: Toon Verwaest <verwaest@chromium.org>
    Commit-Queue: Choongwoo Han <choongwoo.han@microsoft.com>
    Cr-Commit-Position: refs/branch-heads/12.3@{#20}
    Cr-Branched-From: a86e1971579f4165123467fa6ad378e552536b43-refs/heads/12.3.219@{#1}
    Cr-Branched-From: 21869f7f6f3e8f5a58a0b2e61e0f7412480230b1-refs/heads/main@{#92385}

M       src/execution/tiering-manager.cc

https://chromium-review.googlesource.com/5381523


---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40948479)*
