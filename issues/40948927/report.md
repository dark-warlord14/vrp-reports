# Security: Debug check failed: idx.offset() / sizeof(OperationStorageSlot) < size(), leading to segment fault.

| Field | Value |
|-------|-------|
| **Issue ID** | [40948927](https://issues.chromium.org/issues/40948927) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | ml...@chromium.org |
| **Created** | 2023-12-05 |
| **Bounty** | $10,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 90457
    - link: https://crrev.com/63405a66d43737599afec36381a9b0bb13dbb484 
- Commit Message

```
commit 63405a66d43737599afec36381a9b0bb13dbb484
Author: Manos Koukoutos <manoskouk@chromium.org>
Date:   Tue Oct 17 11:40:49 2023 +0200

    [turboshaft][wasm] Speculative inlining
    
    For each call_ref call site, if the call site is marked as inlinable,
    introduce a speculative inlined direct call at that site. This does
    not yet introduce multiple inlined direct calls.
    Drive-by: Change the signature of `InlineWasmCall` and handle null
    `InliningTree` in `should_inline`.
    
    Bug: v8:14108
    Change-Id: I3b42f25ca2c1a297842230a3e85d3e141e1b8c45
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4946031
    Commit-Queue: Manos Koukoutos <manoskouk@chromium.org>
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#90457}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-91313/d8 --turboshaft-wasm poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/compiler/turboshaft/graph.h, line 117
# Debug check failed: idx.offset() / sizeof(OperationStorageSlot) < size() (357913941 vs. 258).
#
#
#
#FailureMessage Object: 0x7f7254ff6b00
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f7290669c73]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(+0x19add) [0x7f7290610add]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x154) [0x7f7290649d14]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(+0x2b7d5) [0x7f72906497d5]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::OperationBuffer::Get(v8::internal::compiler::turboshaft::OpIndex)+0xdd) [0x7f728f2194ed]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::Graph::Get(v8::internal::compiler::turboshaft::OpIndex)+0x2a) [0x7f728f2185fa]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::TSReducerBase>>::ReducePhi(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0xa5) [0x7f728f500625]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::CallRef(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const&, v8::internal::Signature<v8::internal::wasm::ValueType> const*, unsigned int, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*)+0xd26) [0x7f728f554cb6]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallRefImpl(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::TraceLine*, v8::internal::wasm::WasmOpcode)+0x203) [0x7f728f553c93]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallRef(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::WasmOpcode)+0x8b) [0x7f728f50f0cb]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeFunctionBody()+0x203) [0x7f728f4f6333]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::Decode()+0x22f) [0x7f728f4f143f]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::BuildTSGraph(v8::internal::AccountingAllocator*, v8::internal::wasm::WasmFeatures, v8::internal::wasm::WasmModule const*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::turboshaft::Graph&, v8::internal::wasm::FunctionBody const&, v8::internal::wasm::WireBytesStorage const*, v8::internal::wasm::AssumptionsJournal*, v8::internal::ZoneVector<v8::internal::WasmInliningPosition>*, int)+0x25b) [0x7f728f4f0e7b]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::CallDescriptor*)+0x786) [0x7f728fc480f6]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmFeatures*)+0x2b1) [0x7f728fe98241]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x72b) [0x7f728f446efb]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x192) [0x7f728f446342]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(+0x3aa594a) [0x7f728f4a594a]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(+0x3aa5185) [0x7f728f4a5185]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xd3) [0x7f729060f823]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0xc3) [0x7f7290612213]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(+0x4a629) [0x7f7290668629]
    /lib/x86_64-linux-gnu/libc.so.6(+0x94ac3) [0x7f728b094ac3]
    /lib/x86_64-linux-gnu/libc.so.6(+0x126a40) [0x7f728b126a40]

```

## Other
Please note to include the flags `--turboshaft-wasm` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.0.0 - 12.1.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-91313.zip
2. Run: `d8 --turboshaft-wasm poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Jerry

Another variant case of the same introduction point, maybe a type confusion?

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-91313/d8 --turboshaft-wasm --allow-natives-syntax poc.js
# OUTPUT ==============================================================
Turboshaft operation has input #310 with wrong representation.
Expected Float64 but found Word32.


#
# Fatal error in ../../src/compiler/turboshaft/operations.h, line 985
# Debug check failed: ValidOpInputRep(*graph, result->inputs()[i], RegisterRepresentation(expected[i])).
#
#
#
#FailureMessage Object: 0x7fd9f6ffa980
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7fda36c63c73]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(+0x19add) [0x7fda36c0aadd]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x154) [0x7fda36c43d14]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(+0x2b7d5) [0x7fda36c437d5]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::PhiOp& v8::internal::compiler::turboshaft::OperationT<v8::internal::compiler::turboshaft::PhiOp>::New<v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation>(v8::internal::compiler::turboshaft::Graph*, unsigned long, v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x168) [0x7fda35828f68]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::PhiOp& v8::internal::compiler::turboshaft::Graph::Add<v8::internal::compiler::turboshaft::PhiOp, v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation>(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x6c) [0x7fda3582f21c]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false>>::Emit<v8::internal::compiler::turboshaft::PhiOp, v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation>(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x72) [0x7fda35b009e2]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false>>>::ReducePhi(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x184) [0x7fda35b00934]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::TSReducerBase>>::ReducePhi(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x63) [0x7fda35b005e3]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::CallRef(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const&, v8::internal::Signature<v8::internal::wasm::ValueType> const*, unsigned int, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*)+0xd26) [0x7fda35b54cb6]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallRefImpl(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::TraceLine*, v8::internal::wasm::WasmOpcode)+0x203) [0x7fda35b53c93]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallRef(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::WasmOpcode)+0x8b) [0x7fda35b0f0cb]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeFunctionBody()+0x203) [0x7fda35af6333]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::Decode()+0x22f) [0x7fda35af143f]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::BuildTSGraph(v8::internal::AccountingAllocator*, v8::internal::wasm::WasmFeatures, v8::internal::wasm::WasmModule const*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::turboshaft::Graph&, v8::internal::wasm::FunctionBody const&, v8::internal::wasm::WireBytesStorage const*, v8::internal::wasm::AssumptionsJournal*, v8::internal::ZoneVector<v8::internal::WasmInliningPosition>*, int)+0x25b) [0x7fda35af0e7b]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::CallDescriptor*)+0x786) [0x7fda362480f6]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmFeatures*)+0x2b1) [0x7fda36498241]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x72b) [0x7fda35a46efb]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x192) [0x7fda35a46342]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(+0x3aa594a) [0x7fda35aa594a]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(+0x3aa5185) [0x7fda35aa5185]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xd3) [0x7fda36c09823]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0xc3) [0x7fda36c0c213]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(+0x4a629) [0x7fda36c62629]
    /lib/x86_64-linux-gnu/libc.so.6(+0x94ac3) [0x7fda31694ac3]
    /lib/x86_64-linux-gnu/libc.so.6(+0x126a40) [0x7fda31726a40]

    Another variant case of the same introduction point, maybe a type confusion?

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-91313/d8 --turboshaft-wasm --allow-natives-syntax poc.js
# OUTPUT ==============================================================
Turboshaft operation has input #310 with wrong representation.
Expected Float64 but found Word32.


#
# Fatal error in ../../src/compiler/turboshaft/operations.h, line 985
# Debug check failed: ValidOpInputRep(*graph, result->inputs()[i], RegisterRepresentation(expected[i])).
#
#
#
#FailureMessage Object: 0x7fd9f6ffa980
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7fda36c63c73]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(+0x19add) [0x7fda36c0aadd]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x154) [0x7fda36c43d14]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(+0x2b7d5) [0x7fda36c437d5]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::PhiOp& v8::internal::compiler::turboshaft::OperationT<v8::internal::compiler::turboshaft::PhiOp>::New<v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation>(v8::internal::compiler::turboshaft::Graph*, unsigned long, v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x168) [0x7fda35828f68]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::PhiOp& v8::internal::compiler::turboshaft::Graph::Add<v8::internal::compiler::turboshaft::PhiOp, v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation>(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x6c) [0x7fda3582f21c]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false>>::Emit<v8::internal::compiler::turboshaft::PhiOp, v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation>(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x72) [0x7fda35b009e2]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false>>>::ReducePhi(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x184) [0x7fda35b00934]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::TSReducerBase>>::ReducePhi(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x63) [0x7fda35b005e3]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::CallRef(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const&, v8::internal::Signature<v8::internal::wasm::ValueType> const*, unsigned int, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*)+0xd26) [0x7fda35b54cb6]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallRefImpl(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::TraceLine*, v8::internal::wasm::WasmOpcode)+0x203) [0x7fda35b53c93]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallRef(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::WasmOpcode)+0x8b) [0x7fda35b0f0cb]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeFunctionBody()+0x203) [0x7fda35af6333]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::Decode()+0x22f) [0x7fda35af143f]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::BuildTSGraph(v8::internal::AccountingAllocator*, v8::internal::wasm::WasmFeatures, v8::internal::wasm::WasmModule const*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::turboshaft::Graph&, v8::internal::wasm::FunctionBody const&, v8::internal::wasm::WireBytesStorage const*, v8::internal::wasm::AssumptionsJournal*, v8::internal::ZoneVector<v8::internal::WasmInliningPosition>*, int)+0x25b) [0x7fda35af0e7b]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::CallDescriptor*)+0x786) [0x7fda362480f6]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmFeatures*)+0x2b1) [0x7fda36498241]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x72b) [0x7fda35a46efb]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x192) [0x7fda35a46342]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(+0x3aa594a) [0x7fda35aa594a]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(+0x3aa5185) [0x7fda35aa5185]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xd3) [0x7fda36c09823]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0xc3) [0x7fda36c0c213]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(+0x4a629) [0x7fda36c62629]
    /lib/x86_64-linux-gnu/libc.so.6(+0x94ac3) [0x7fda31694ac3]
    /lib/x86_64-linux-gnu/libc.so.6(+0x126a40) [0x7fda31726a40]

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 4.8 KB)
- [poc4.js](attachments/poc4.js) (text/plain, 3.4 KB)
- [poc3.js](attachments/poc3.js) (text/plain, 17.2 KB)
- [poc2.js](attachments/poc2.js) (text/plain, 4.6 KB)
- [poc1.js](attachments/poc1.js) (text/plain, 19.6 KB)
- [poc2.js](attachments/poc2.js) (text/plain, 4.6 KB)
- [poc3.js](attachments/poc3.js) (text/plain, 17.2 KB)
- [poc4.js](attachments/poc4.js) (text/plain, 3.4 KB)
- [asan.log](attachments/asan.log) (text/plain, 12.0 KB)
- [oob_poc.js](attachments/oob_poc.js) (text/plain, 3.3 KB)
- [mini_poc.js](attachments/mini_poc.js) (text/plain, 3.2 KB)

## Timeline

### je...@gmail.com (2023-12-05)

[Comment Deleted]

### [Deleted User] (2023-12-05)

[Empty comment from Monorail migration]

### je...@gmail.com (2023-12-05)

Another variant case of the same introduction point, maybe a type confusion?

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-91313/d8 --turboshaft-wasm --allow-natives-syntax poc.js
# OUTPUT ==============================================================
Turboshaft operation has input #310 with wrong representation.
Expected Float64 but found Word32.


#
# Fatal error in ../../src/compiler/turboshaft/operations.h, line 985
# Debug check failed: ValidOpInputRep(*graph, result->inputs()[i], RegisterRepresentation(expected[i])).
#
#
#
#FailureMessage Object: 0x7fd9f6ffa980
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7fda36c63c73]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(+0x19add) [0x7fda36c0aadd]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x154) [0x7fda36c43d14]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(+0x2b7d5) [0x7fda36c437d5]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::PhiOp& v8::internal::compiler::turboshaft::OperationT<v8::internal::compiler::turboshaft::PhiOp>::New<v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation>(v8::internal::compiler::turboshaft::Graph*, unsigned long, v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x168) [0x7fda35828f68]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::PhiOp& v8::internal::compiler::turboshaft::Graph::Add<v8::internal::compiler::turboshaft::PhiOp, v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation>(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x6c) [0x7fda3582f21c]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false>>::Emit<v8::internal::compiler::turboshaft::PhiOp, v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation>(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x72) [0x7fda35b009e2]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false>>>::ReducePhi(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x184) [0x7fda35b00934]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::TSReducerBase>>::ReducePhi(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x63) [0x7fda35b005e3]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::CallRef(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const&, v8::internal::Signature<v8::internal::wasm::ValueType> const*, unsigned int, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*)+0xd26) [0x7fda35b54cb6]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallRefImpl(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::TraceLine*, v8::internal::wasm::WasmOpcode)+0x203) [0x7fda35b53c93]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallRef(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::WasmOpcode)+0x8b) [0x7fda35b0f0cb]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeFunctionBody()+0x203) [0x7fda35af6333]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::Decode()+0x22f) [0x7fda35af143f]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::BuildTSGraph(v8::internal::AccountingAllocator*, v8::internal::wasm::WasmFeatures, v8::internal::wasm::WasmModule const*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::turboshaft::Graph&, v8::internal::wasm::FunctionBody const&, v8::internal::wasm::WireBytesStorage const*, v8::internal::wasm::AssumptionsJournal*, v8::internal::ZoneVector<v8::internal::WasmInliningPosition>*, int)+0x25b) [0x7fda35af0e7b]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::CallDescriptor*)+0x786) [0x7fda362480f6]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmFeatures*)+0x2b1) [0x7fda36498241]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x72b) [0x7fda35a46efb]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x192) [0x7fda35a46342]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(+0x3aa594a) [0x7fda35aa594a]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(+0x3aa5185) [0x7fda35aa5185]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xd3) [0x7fda36c09823]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0xc3) [0x7fda36c0c213]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(+0x4a629) [0x7fda36c62629]
    /lib/x86_64-linux-gnu/libc.so.6(+0x94ac3) [0x7fda31694ac3]
    /lib/x86_64-linux-gnu/libc.so.6(+0x126a40) [0x7fda31726a40]

```


### je...@gmail.com (2023-12-05)

Please cc manoskouk@chromium.org, he may be the owner of this issue.

### je...@gmail.com (2023-12-05)

Update a poc with more security features. This will result in a segment fault at a non-zero address.

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-91313/d8 --turboshaft-wasm --allow-natives-syntax poc.js
# OUTPUT ==============================================================
Received signal 11 SEGV_MAPERR ffffffffa5ff0fd0

==== C stack trace ===============================

 [0x7ff5b9123c73]
 [0x7ff5b9123bc2]
 [0x7ff5b3a42520]
 [0x7ff5b7f549a3]
 [0x7ff5b7f53c93]
 [0x7ff5b7f0f0cb]
 [0x7ff5b7ef6333]
 [0x7ff5b7ef143f]
 [0x7ff5b7ef0e7b]
 [0x7ff5b86480f6]
 [0x7ff5b8898241]
 [0x7ff5b7e46efb]
 [0x7ff5b7e46342]
 [0x7ff5b7ea594a]
 [0x7ff5b7ea5185]
 [0x7ff5b90c9823]
 [0x7ff5b90cc213]
 [0x7ff5b9122629]
 [0x7ff5b3a94ac3]
 [0x7ff5b3b26a40]
[end of stack trace]

```


### sr...@google.com (2023-12-05)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript>WebAssembly]

### je...@gmail.com (2023-12-05)

Please check all poc, Although they are the same introduction point, they may be different vulnerabilities.

I'm also trying to investigate segv exploitability, I'll update when I make progress.

### je...@gmail.com (2023-12-05)

Although I combined these three issues into one report submission because the introduction points are the same, if you can determine that they are different vulnerabilities, you can point this out to help Chrome vrp better determine the bug bounty, thank you. 

### ma...@chromium.org (2023-12-05)

[Empty comment from Monorail migration]

### je...@gmail.com (2023-12-05)

For https://crbug.com/chromium/1508213#c5:
I have been able to achieve controllable out-of-bounds write, and an exploit is on the way.

### ml...@chromium.org (2023-12-05)

I can reproduce the issue for poc1.js (I haven't looked into the other cases yet).
It seems that something is off maybe with the linlining feedback. I added a DCHECK to InlineWasmCall:
    DCHECK_EQ(inlinee.sig->return_count(), sig->return_count());
leading to
    # Debug check failed: inlinee.sig->return_count() == sig->return_count() (0 vs. 1).

I am not fully sure what the issue is but I think it's likely that we get confused with the feedback slots and read from a wrong one as we try to inline a function that can not be called from that call_ref.

### ml...@chromium.org (2023-12-05)

OK, I figured out the issue now.
The issue is the combination of CatchAll and turboshaft inlining:

In liftoff we do the following for CatchAll (https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/baseline/liftoff-compiler.cc;l=1459):
    if (!block->try_info->catch_reached) {
      decoder->SetSucceedingCodeDynamicallyUnreachable();
      return;
    }

We do something similar in Turbofan.
The new turboshaft graph builder misses this:
https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/turboshaft-graph-interface.cc;l=2278

Switching to dynamically unreachable means that we ignore any statements following this one until we are back to a reachable state, so we won't generate any feedback slots for any calls there.
In Turboshaft we treat them as reachable due to this difference and increase our feedback slot counts accordingly, so once we are back at a reachable call we already use a wrong feedback offset.

### ml...@chromium.org (2023-12-05)

[Empty comment from Monorail migration]

### ma...@chromium.org (2023-12-05)

[Empty comment from Monorail migration]

### ma...@chromium.org (2023-12-05)

[Empty comment from Monorail migration]

### je...@gmail.com (2023-12-06)

## Exploit Details

In the CallRef function in src/wasm/turboshaft-graph-interface.cc:

```
__ Bind(inline_block);
SmallZoneVector<Value, 4> direct_returns(return_count, decoder->zone_); // ==> [0]
if (v8_flags.trace_wasm_inlining) {
  PrintF(
      "[function %d%s: Speculatively inlining call_ref #%d, case #%d, "
      "to function %d]\n",
      func_index_, mode_ == kRegular ? "" : " (inlined)",
      feedback_slot_, static_cast<int>(i), inlined_index);
}
InlineWasmCall(decoder, inlined_index, sig, static_cast<uint32_t>(i),
               args, direct_returns.data());  ==> [1]
for (size_t ret = 0; ret < direct_returns.size(); ret++) {
  case_returns[ret].push_back(direct_returns[ret].op);
}
__ Goto(merge);
```

[0] direct_returns creates a vector with a size of 4

[1] direct_returns.data() is passed into InlineWasmCall, where data() is a raw pointer

In the InlineWasmCall function:
```
__ Bind(callee_return_block);
BlockPhis& return_phis = inlinee_decoder.interface().return_phis();
for (size_t i = 0; i < inlinee.sig->return_count(); i++) {
  returns[i].op = MaybePhi(base::VectorOf(return_phis.phi_inputs[i]),
                           return_phis.phi_types[i]); ==> [2]
}
```

[2] returns is the passed raw pointer, where operations are directly performed on the raw pointer, easily leading to an overflow. This actually happened. Here, inlinee.sig->return_count() is 5, which is greater than 4, the size used when creating the vector, causing out-of-bounds (oob) write.

With some construction of the proof of concept (poc), it's possible to control the OpIndex written at this point to any integer.

Additionally, the length of the write, inlinee.sig->return_count(), can also be controlled by us. This value is the number of return values for function 2, which is 5.
For example, if we change the poc like oob_poc.js:
inlinee.sig->return_count() will become 6.

With this, we've achieved an out-of-bound write of arbitrary length and content.

This is sufficient to achieve an exploit.

see asan.log

### gi...@appspot.gserviceaccount.com (2023-12-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/def7931b83728d229e94be9445529fb9db660654

commit def7931b83728d229e94be9445529fb9db660654
Author: Matthias Liedtke <mliedtke@chromium.org>
Date: Wed Dec 06 12:51:24 2023

[turboshaft][wasm] Fix reachability handling for catch blocks

Due to the reachability in the decoder influencing the  assignment of
feedback slots, it is required to handle reachability consistently
between liftoff and the optimizing compiler.

This wasn't the case for CatchException, CatchCase and CatchAll.

Bug: chromium:1508213
Change-Id: I9feede4b9397f51d3290edccef1768f500178f1f
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5088809
Reviewed-by: Manos Koukoutos <manoskouk@chromium.org>
Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
Cr-Commit-Position: refs/heads/main@{#91376}

[add] https://crrev.com/def7931b83728d229e94be9445529fb9db660654/test/mjsunit/wasm/wasm-inlining-catch-unreachable.js
[modify] https://crrev.com/def7931b83728d229e94be9445529fb9db660654/src/wasm/turboshaft-graph-interface.cc


### ml...@chromium.org (2023-12-06)

I tried all the reproducers and they should all be fixed now by the CL above.

This is all behind --future, so at least it doesn't impact stable (yet) until we start finching which means we only need to backmerge for versions which we want to finch this feature on (121).
I agree that with the broken behavior it is possible to create any kind of mismatch between a caller and an inlined function that might have different signatures, different types etc., so this should provide all kinds of possibilities for arbitrary memory access.

I'll go ahead and request the backmerge once the fix has hit canary.

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-12-07)

ClusterFuzz testcase 5644294575030272 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=91375:91376

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### ml...@chromium.org (2023-12-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-07)

Merge approved: your change passed merge requirements and is auto-approved for M121. Please go ahead and merge the CL to branch 6167 (refs/branch-heads/6167) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ml...@chromium.org (2023-12-08)

Merge landed for 121: https://chromium-review.googlesource.com/c/v8/v8/+/5099464
(My feeling is that the "(cherry picked from commit def7931b83728d229e94be9445529fb9db660654)" line created by gerrit might cause confusion as the bug label is not at the end of the commit message, so that's probably why it doesn't automatically update this bug.)

### am...@google.com (2023-12-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-12-14)

Congratulations on another one! The Chrome VRP Panel has decided to award you $10,000 for this high quality report + $1,000 bisect bonus. The reward amount was decided due to the efforts to demonstrate exploitability of this issue through the analysis provided in c#16. Thank you for your efforts and reporting this issue to us -- great work! 

### am...@google.com (2023-12-15)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-12-18)

[Description Changed]

### is...@google.com (2023-12-18)

This issue was migrated from crbug.com/chromium/1508213?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1507752, crbug.com/chromium/1508211]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40948927)*
