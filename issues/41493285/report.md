# Security: Debug check failed: element_size_log2 == 0 (\x2 vs. 0). in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [41493285](https://issues.chromium.org/issues/41493285) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Compiler>Turbofan |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2024-01-21 |
| **Bounty** | $7,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 91502
    - link: https://crrev.com/afee3b501bed785ae1739bb5c8da6ace5c823e7d 
- Commit Message

```
commit afee3b501bed785ae1739bb5c8da6ace5c823e7d
Author: Matthias Liedtke <mliedtke@chromium.org>
Date:   Thu Dec 14 10:55:08 2023 +0100

    [turboshaft][arm] Port InstructionSelector part 3
    
    This CL adds support for all instructions required to pass:
    $ gm arm.optdebug.checkall --variants=turboshaft \
      --extra-flags="--turboshaft-wasm-instruction-selection-experimental"
    
    Bug: v8:12783
    Change-Id: I616dfbc8467f0b67a047c0864e20510cfa7a1cd6
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5103510
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#91502}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux32-debug-v8-component-91933/d8 --future poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/compiler/turboshaft/int64-lowering-reducer.h, line 286
# Debug check failed: element_size_log2 == 0 (\x2 vs. 0).
#
#
#
#FailureMessage Object: 0xe0df8ac0
==== C stack trace ===============================

    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1f) [0xf7f862ef]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libplatform.so(+0x16394) [0xf7f32394]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0xf7) [0xf7f65677]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(+0x27076) [0xf7f65076]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x31) [0xf7f656c1]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::turboshaft::Int64LoweringReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::Int64LoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::ReduceStore(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::OptionalOpIndex, v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::LoadOp::Kind, v8::internal::compiler::turboshaft::MemoryRepresentation, v8::internal::compiler::WriteBarrierKind, int, unsigned char, bool, v8::internal::IndirectPointerTag)+0x479) [0xf72b1bc9]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::Int64LoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::Int64LoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::AssembleOutputGraphStore(v8::internal::compiler::turboshaft::StoreOp const&)+0x116) [0xf72b1656]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::Int64LoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::Int64LoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitOpNoMappingUpdate<false>(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::Block const*)+0x536) [0xf72972f6]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::Int64LoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::Int64LoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::AssembleOutputGraphCheckException(v8::internal::compiler::turboshaft::CheckExceptionOp const&)+0x1fb) [0xf7296acb]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::Int64LoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::Int64LoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitOpNoMappingUpdate<false>(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::Block const*)+0xc3) [0xf7296e83]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::Int64LoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::Int64LoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitBlock<false>(v8::internal::compiler::turboshaft::Block const*)+0x668) [0xf72c3a98]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::Int64LoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::Int64LoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitAllBlocks<false>()+0xfe) [0xf72c331e]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::turboshaft::CopyingPhaseImpl<v8::internal::compiler::turboshaft::Int64LoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer>::Run(v8::internal::compiler::turboshaft::Graph&, v8::internal::Zone*, bool)+0x1d5) [0xf728a475]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::turboshaft::Int64LoweringPhase::Run(v8::internal::Zone*)+0x46) [0xf728a276]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(auto v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::turboshaft::Int64LoweringPhase>()+0xd0) [0xf711ef60]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::CallDescriptor*)+0x81a) [0xf711d6da]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmFeatures*)+0x317) [0xf73df427]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x684) [0xf68eb0f4]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x18a) [0xf68ea67a]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(+0x3348f92) [0xf6948f92]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(+0x3348809) [0xf6948809]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xcb) [0xf7f30fdb]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0x98) [0xf7f33678]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(+0x46f0e) [0xf7f84f0e]
    /lib/i386-linux-gnu/libc.so.6(+0x86c01) [0xf2c86c01]
    /lib/i386-linux-gnu/libc.so.6(+0x12375c) [0xf2d2375c]

```

## Other
Please note to include the flags `--future` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.2.0 - 12.2.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux32-debug/d8-linux32-debug-v8-component-91933.zip
2. Run: `d8 --future poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Jerry

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 1.5 KB)
- [poc_code.js](attachments/poc_code.js) (text/plain, 4.9 KB)
- [poc_code.js](attachments/poc_code_53319761.js) (text/plain, 4.9 KB)
- [poc.js](attachments/poc_53319762.js) (text/plain, 1.5 KB)

## Timeline

### je...@gmail.com (2024-01-21)

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 91502
    - link: https://crrev.com/afee3b501bed785ae1739bb5c8da6ace5c823e7d 
- Commit Message

```
commit afee3b501bed785ae1739bb5c8da6ace5c823e7d
Author: Matthias Liedtke <mliedtke@chromium.org>
Date:   Thu Dec 14 10:55:08 2023 +0100

    [turboshaft][arm] Port InstructionSelector part 3
    
    This CL adds support for all instructions required to pass:
    $ gm arm.optdebug.checkall --variants=turboshaft \
      --extra-flags="--turboshaft-wasm-instruction-selection-experimental"
    
    Bug: v8:12783
    Change-Id: I616dfbc8467f0b67a047c0864e20510cfa7a1cd6
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5103510
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#91502}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux32-debug-v8-component-91933/d8 --future poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/compiler/turboshaft/int64-lowering-reducer.h, line 286
# Debug check failed: element_size_log2 == 0 (\x2 vs. 0).
#
#
#
#FailureMessage Object: 0xe0df8ac0
==== C stack trace ===============================

    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1f) [0xf7f862ef]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libplatform.so(+0x16394) [0xf7f32394]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0xf7) [0xf7f65677]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(+0x27076) [0xf7f65076]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x31) [0xf7f656c1]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::turboshaft::Int64LoweringReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::Int64LoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::ReduceStore(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::OptionalOpIndex, v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::LoadOp::Kind, v8::internal::compiler::turboshaft::MemoryRepresentation, v8::internal::compiler::WriteBarrierKind, int, unsigned char, bool, v8::internal::IndirectPointerTag)+0x479) [0xf72b1bc9]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::Int64LoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::Int64LoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::AssembleOutputGraphStore(v8::internal::compiler::turboshaft::StoreOp const&)+0x116) [0xf72b1656]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::Int64LoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::Int64LoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitOpNoMappingUpdate<false>(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::Block const*)+0x536) [0xf72972f6]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::Int64LoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::Int64LoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::AssembleOutputGraphCheckException(v8::internal::compiler::turboshaft::CheckExceptionOp const&)+0x1fb) [0xf7296acb]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::Int64LoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::Int64LoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitOpNoMappingUpdate<false>(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::Block const*)+0xc3) [0xf7296e83]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::Int64LoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::Int64LoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitBlock<false>(v8::internal::compiler::turboshaft::Block const*)+0x668) [0xf72c3a98]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::Int64LoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::Int64LoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitAllBlocks<false>()+0xfe) [0xf72c331e]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::turboshaft::CopyingPhaseImpl<v8::internal::compiler::turboshaft::Int64LoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer>::Run(v8::internal::compiler::turboshaft::Graph&, v8::internal::Zone*, bool)+0x1d5) [0xf728a475]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::turboshaft::Int64LoweringPhase::Run(v8::internal::Zone*)+0x46) [0xf728a276]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(auto v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::turboshaft::Int64LoweringPhase>()+0xd0) [0xf711ef60]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::CallDescriptor*)+0x81a) [0xf711d6da]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmFeatures*)+0x317) [0xf73df427]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x684) [0xf68eb0f4]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x18a) [0xf68ea67a]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(+0x3348f92) [0xf6948f92]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(+0x3348809) [0xf6948809]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xcb) [0xf7f30fdb]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0x98) [0xf7f33678]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(+0x46f0e) [0xf7f84f0e]
    /lib/i386-linux-gnu/libc.so.6(+0x86c01) [0xf2c86c01]
    /lib/i386-linux-gnu/libc.so.6(+0x12375c) [0xf2d2375c]

```

## Other
Please note to include the flags `--future` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.2.0 - 12.2.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux32-debug/d8-linux32-debug-v8-component-91933.zip
2. Run: `d8 --future poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Jerry

### [Deleted User] (2024-01-21)

[Empty comment from Monorail migration]

### je...@gmail.com (2024-01-21)

Please pay attention to using 32-bit d8 debug to reproduce.

### cl...@chromium.org (2024-01-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4834382197489664.

### cl...@chromium.org (2024-01-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2024-01-23)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript]

### cl...@chromium.org (2024-01-23)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/afee3b501bed785ae1739bb5c8da6ace5c823e7d ([turboshaft][arm] Port InstructionSelector part 3).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2024-01-23)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript>Compiler>Turbofan]

### ke...@chromium.org (2024-01-24)

Tentatively setting severity to High. This can be adjusted if assessment finds there isn't a risk of memory corruption.

### [Deleted User] (2024-01-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2024-01-24)

Detailed Report: https://clusterfuzz.com/testcase?key=4834382197489664

Fuzzer: None
Job Type: linux32_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  element_size_log2 == 0 in int64-lowering-reducer.h
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux32_d8_dbg&range=91501:91502

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4834382197489664

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### jk...@chromium.org (2024-01-24)

Fix in flight: https://chromium-review.googlesource.com/c/v8/v8/+/5232164

I agree that this is security relevant.

Impact in practice is limited by the fact that it needs Turboshaft (via --future or --turboshaft-wasm or the Finch experiment we would like to start but haven't started yet).

The bisection result in #1 is sort-of bogus: that CL added the DCHECK that allowed the fuzzer to find this bug, but the bug itself was older, it just didn't trip up any DCHECKs previously.

### gi...@appspot.gserviceaccount.com (2024-01-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/e0a43f23ca0259e4c2575b4438d441bd76fa124d

commit e0a43f23ca0259e4c2575b4438d441bd76fa124d
Author: Jakob Kummerow <jkummerow@chromium.org>
Date: Wed Jan 24 13:22:06 2024

[turboshaft][wasm] Fix 64-bit atomic load/store on 32-bit arch

Int64Lowering currently cannot deal with "elem_size_log2" scaling
parameters, because AtomicWord32Pair doesn't support them. So the
MachineOptimizationReducer shouldn't produce these parameters on
this particular configuration.

Fixed: chromium:1520311
Change-Id: I68f5cf48fc2d617bd62aeced018983eb6e77d56c
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5232164
Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Cr-Commit-Position: refs/heads/main@{#91985}

[add] https://crrev.com/e0a43f23ca0259e4c2575b4438d441bd76fa124d/test/mjsunit/regress/wasm/regress-crbug-1520311.js
[modify] https://crrev.com/e0a43f23ca0259e4c2575b4438d441bd76fa124d/src/compiler/turboshaft/int64-lowering-reducer.h
[modify] https://crrev.com/e0a43f23ca0259e4c2575b4438d441bd76fa124d/src/compiler/turboshaft/machine-optimization-reducer.h


### [Deleted User] (2024-01-24)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-24)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2024-01-25)

ClusterFuzz testcase 4834382197489664 is verified as fixed in https://clusterfuzz.com/revisions?job=linux32_d8_dbg&range=91984:91985

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### ha...@google.com (2024-01-25)

[Empty comment from Monorail migration]

### jk...@chromium.org (2024-01-26)

Requesting merge to unblock upcoming Finch trial.

### [Deleted User] (2024-01-26)

Merge approved: your change passed merge requirements and is auto-approved for M122. Please go ahead and merge the CL to branch 6261 (refs/branch-heads/6261) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2024-01-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/b1647e4ee8bb742379957771d5dc3a5472ee7200

commit b1647e4ee8bb742379957771d5dc3a5472ee7200
Author: Jakob Kummerow <jkummerow@chromium.org>
Date: Wed Jan 24 13:22:06 2024

Merged: [turboshaft][wasm] Fix 64-bit atomic load/store on 32-bit arch

Int64Lowering currently cannot deal with "elem_size_log2" scaling
parameters, because AtomicWord32Pair doesn't support them. So the
MachineOptimizationReducer shouldn't produce these parameters on
this particular configuration.

Fixed: chromium:1520311
(cherry picked from commit e0a43f23ca0259e4c2575b4438d441bd76fa124d)

Change-Id: I41c774068f62e07bca242e30dae5f6dd5998dd65
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5239031
Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
Cr-Commit-Position: refs/branch-heads/12.2@{#12}
Cr-Branched-From: 6eb5a9616aa6f8c705217aeb7c7ab8c037a2f676-refs/heads/12.2.281@{#1}
Cr-Branched-From: 44cf56d850167c6988522f8981730462abc04bcc-refs/heads/main@{#91934}

[add] https://crrev.com/b1647e4ee8bb742379957771d5dc3a5472ee7200/test/mjsunit/regress/wasm/regress-crbug-1520311.js
[modify] https://crrev.com/b1647e4ee8bb742379957771d5dc3a5472ee7200/src/compiler/turboshaft/int64-lowering-reducer.h
[modify] https://crrev.com/b1647e4ee8bb742379957771d5dc3a5472ee7200/src/compiler/turboshaft/machine-optimization-reducer.h


### [Deleted User] (2024-01-26)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jk...@chromium.org (2024-01-26)

#22: No LTS merge to M120 is necessary, as M120 doesn't exercise the affected code path.

### am...@chromium.org (2024-01-29)

[Description Changed]

### am...@google.com (2024-02-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-02)

Congratulations on another one Jerry! The Chrome VRP Panel has decided to award you $7,000 for this report of memory corruption in the renderer / sandboxed process. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2024-02-02)

[Empty comment from Monorail migration]

### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/1520311?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript, Blink>JavaScript>Compiler>Turbofan]
[Monorail components added to Component Tags custom field.]

### vo...@google.com (2024-02-19)

Marking as not applicable to M120 LTS, according to [comment #24](https://issues.chromium.org/issues/41493285#comment24).

### pe...@google.com (2024-05-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41493285)*
