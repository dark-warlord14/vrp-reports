# Fatal error in ../../src/compiler/turboshaft/assembler.h, line 1028

| Field | Value |
|-------|-------|
| **Issue ID** | [360044696](https://issues.chromium.org/issues/360044696) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sw...@gmail.com |
| **Assignee** | ml...@chromium.org |
| **Created** | 2024-08-15 |
| **Bounty** | $2,000.00 |

## Description

## VULNERABILITY DETAILS

Fatal error in ../../src/compiler/turboshaft/assembler.h, line 1028
Debug check failed: ValidInputs(result).

## VERSION

V8: HEAD

## REPRODUCTION CASE

Compile `x64.release + is_asan=true` version

Run :

```
./v8_simple_wasm_deopt_fuzzer 2024814

```

ASAN crash info:

```
AddressSanitizer:DEADLYSIGNAL
=================================================================
==16443==ERROR: AddressSanitizer: SEGV on unknown address 0x52d100032417 (pc 0x5633d4071153 bp 0x7ffd43a10990 sp 0x7ffd43a108e0 T0)
==16443==The signal is caused by a READ memory access.
    #0 0x5633d4071153 in Is<v8::internal::compiler::turboshaft::ConstantOp> src/compiler/turboshaft/operations.h:956:14
    #1 0x5633d4071153 in TryCast<v8::internal::compiler::turboshaft::ConstantOp> src/compiler/turboshaft/operations.h:974:10
    #2 0x5633d4071153 in TryCast<v8::internal::compiler::turboshaft::ConstantOp> src/compiler/turboshaft/operation-matcher.h:29:31
    #3 0x5633d4071153 in MatchIntegralWordConstant src/compiler/turboshaft/operation-matcher.h:145:28
    #4 0x5633d4071153 in v8::internal::compiler::turboshaft::MachineOptimizationReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::ReduceShift(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::ShiftOp::Kind, v8::internal::compiler::turboshaft::WordRepresentation) src/compiler/turboshaft/machine-optimization-reducer.h:1612:17
    #5 0x5633d404887d in v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitOpNoMappingUpdate<false>(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::Block const*) src/compiler/turboshaft/copying-phase.h:671:7
    #6 0x5633d4038bf1 in VisitOpAndUpdateMapping<false> src/compiler/turboshaft/copying-phase.h:642:9
    #7 0x5633d4038bf1 in void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitBlockBody<(v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::CanHavePhis)1, (v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::ForCloning)0, false>(v8::internal::compiler::turboshaft::Block const*, int) src/compiler/turboshaft/copying-phase.h:616:12
    #8 0x5633d4037886 in void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitBlock<false>(v8::internal::compiler::turboshaft::Block const*) src/compiler/turboshaft/copying-phase.h:510:7
    #9 0x5633d4033486 in void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitAllBlocks<false>() src/compiler/turboshaft/copying-phase.h:486:7
    #10 0x5633d40247dc in void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitGraph<false>() src/compiler/turboshaft/copying-phase.h:127:5
    #11 0x5633d4024380 in v8::internal::compiler::turboshaft::CopyingPhaseImpl<v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer>::Run(v8::internal::compiler::turboshaft::PipelineData*, v8::internal::compiler::turboshaft::Graph&, v8::internal::Zone*, bool) src/compiler/turboshaft/copying-phase.h:1046:20
    #12 0x5633d3bce8f2 in auto v8::internal::compiler::turboshaft::Pipeline::Run<v8::internal::compiler::turboshaft::WasmOptimizePhase>() src/compiler/turboshaft/pipelines.h:73:13
    #13 0x5633d3be9c87 in v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::wasm::WasmDetectedFeatures*, v8::internal::compiler::CallDescriptor*) src/compiler/pipeline.cc:3583:25
    #14 0x5633d40fa92e in v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmDetectedFeatures*) src/compiler/turboshaft/wasm-turboshaft-compiler.cc:53:8
    #15 0x5633d2d1574f in v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmDetectedFeatures*) src/wasm/function-compiler.cc:170:18
    #16 0x5633d2d13ede in v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmDetectedFeatures*) src/wasm/function-compiler.cc:34:9
    #17 0x5633d2d163fc in v8::internal::wasm::WasmCompilationUnit::CompileWasmFunction(v8::internal::Counters*, v8::internal::wasm::NativeModule*, v8::internal::wasm::WasmDetectedFeatures*, v8::internal::wasm::WasmFunction const*, v8::internal::wasm::ExecutionTier) src/wasm/function-compiler.cc:205:39
    #18 0x5633d2fcea46 in v8::internal::wasm::WasmEngine::CompileFunction(v8::internal::Counters*, v8::internal::wasm::NativeModule*, unsigned int, v8::internal::wasm::ExecutionTier) src/wasm/wasm-engine.cc:874:3
    #19 0x5633d2d79d79 in v8::internal::wasm::TierUpNowForTesting(v8::internal::Isolate*, v8::internal::Tagged<v8::internal::WasmTrustedInstanceData>, int) src/wasm/module-compiler.cc:1666:26
    #20 0x5633d0be013d in FuzzIt test/fuzzer/wasm-deopt.cc:298:5
    #21 0x5633d0be013d in LLVMFuzzerTestOneInput test/fuzzer/wasm-deopt.cc:308:10
    #22 0x5633d0bde162 in main test/fuzzer/fuzzer.cc:59:3
    #23 0x7fbc65976d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

==16443==Register values:
rax = 0x00007fbc641ebc18  rbx = 0x00007ffd43a108e0  rcx = 0x0000000000000000  rdx = 0x00007fbc641eb868
rdi = 0x000052d100032417  rsi = 0x00007fbc63cdcb00  rbp = 0x00007ffd43a10990  rsp = 0x00007ffd43a108e0
 r8 = 0x00007fffffffff01   r9 = 0x000052d000032418  r10 = 0x00000000000004c8  r11 = 0x00007fbc641eb030
r12 = 0x00000ff78c79b960  r13 = 0x00000ff78c83d70d  r14 = 0x0000000000000001  r15 = 0x00007fbc63cdcb00
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV src/compiler/turboshaft/operations.h:956:14 in Is<v8::internal::compiler::turboshaft::ConstantOp>
==16443==ABORTING

```

Compile `x64.debug` version

crash log:

```
#
# Fatal error in ../../src/compiler/turboshaft/assembler.h, line 1028
# Debug check failed: ValidInputs(result).
#
#
#
#FailureMessage Object: 0x7fff27127258
==== C stack trace ===============================

    /data/v8/v8/out/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1e) [0x7fb194589d2e]
    /data/v8/v8/out/x64.debug/libv8_libplatform.so(+0x56d7d) [0x7fb1944e7d7d]
    /data/v8/v8/out/x64.debug/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x205) [0x7fb19455f3d5]
    /data/v8/v8/out/x64.debug/libv8_libbase.so(+0x55d8c) [0x7fb19455ed8c]
    /data/v8/v8/out/x64.debug/libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x4d) [0x7fb19455f4ad]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewLoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false>>::Emit<v8::internal::compiler::turboshaft::ShiftOp, v8::internal::compiler::turboshaft::ShadowyOpIndex, v8::internal::compiler::turboshaft::ShadowyOpIndex, v8::internal::compiler::turboshaft::ShiftOp::Kind, v8::internal::compiler::turboshaft::WordRepresentation>(v8::internal::compiler::turboshaft::ShadowyOpIndex, v8::internal::compiler::turboshaft::ShadowyOpIndex, v8::internal::compiler::turboshaft::ShiftOp::Kind, v8::internal::compiler::turboshaft::WordRepresentation)+0x21f) [0x7fb19ce4b01f]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::ReducerBaseForwarder<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewLoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false>>>::ReduceShift<v8::internal::compiler::turboshaft::V<v8::internal::compiler::turboshaft::WordWithBits<64ul>>, v8::internal::compiler::turboshaft::V<v8::internal::compiler::turboshaft::WordWithBits<32ul>>, v8::internal::compiler::turboshaft::ShiftOp::Kind, v8::internal::compiler::turboshaft::WordRepresentation>(v8::internal::compiler::turboshaft::V<v8::internal::compiler::turboshaft::WordWithBits<64ul>>, v8::internal::compiler::turboshaft::V<v8::internal::compiler::turboshaft::WordWithBits<32ul>>, v8::internal::compiler::turboshaft::ShiftOp::Kind, v8::internal::compiler::turboshaft::WordRepresentation)+0x89) [0x7fb19ce727d9]
    /data/v8/v8/out/x64.debug/libv8.so(auto v8::internal::compiler::turboshaft::UniformReducerAdapter<v8::internal::compiler::turboshaft::EmitProjectionReducer, v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewLoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false>>>>::ReduceShiftContinuation::Reduce<v8::internal::compiler::turboshaft::V<v8::internal::compiler::turboshaft::WordWithBits<64ul>>, v8::internal::compiler::turboshaft::V<v8::internal::compiler::turboshaft::WordWithBits<32ul>>, v8::internal::compiler::turboshaft::ShiftOp::Kind, v8::internal::compiler::turboshaft::WordRepresentation>(v8::internal::compiler::turboshaft::V<v8::internal::compiler::turboshaft::WordWithBits<64ul>>, v8::internal::compiler::turboshaft::V<v8::internal::compiler::turboshaft::WordWithBits<32ul>>, v8::internal::compiler::turboshaft::ShiftOp::Kind, v8::internal::compiler::turboshaft::WordRepresentation) const+0x4c) [0x7fb19ce7273c]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewLoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false>>>>::ReduceOperation<(v8::internal::compiler::turboshaft::Opcode)62, v8::internal::compiler::turboshaft::UniformReducerAdapter<v8::internal::compiler::turboshaft::EmitProjectionReducer, v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewLoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false>>>>::ReduceShiftContinuation, v8::internal::compiler::turboshaft::V<v8::internal::compiler::turboshaft::WordWithBits<64ul>>, v8::internal::compiler::turboshaft::V<v8::internal::compiler::turboshaft::WordWithBits<32ul>>, v8::internal::compiler::turboshaft::ShiftOp::Kind, v8::internal::compiler::turboshaft::WordRepresentation>(v8::internal::compiler::turboshaft::V<v8::internal::compiler::turboshaft::WordWithBits<64ul>>, v8::internal::compiler::turboshaft::V<v8::internal::compiler::turboshaft::WordWithBits<32ul>>, v8::internal::compiler::turboshaft::ShiftOp::Kind, v8::internal::compiler::turboshaft::WordRepresentation)+0x63) [0x7fb19ce72673]
    /data/v8/v8/out/x64.debug/libv8.so(auto v8::internal::compiler::turboshaft::UniformReducerAdapter<v8::internal::compiler::turboshaft::EmitProjectionReducer, v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewLoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false>>>>::ReduceShift<v8::internal::compiler::turboshaft::V<v8::internal::compiler::turboshaft::WordWithBits<64ul>>, v8::internal::compiler::turboshaft::V<v8::internal::compiler::turboshaft::WordWithBits<32ul>>, v8::internal::compiler::turboshaft::ShiftOp::Kind, v8::internal::compiler::turboshaft::WordRepresentation>(v8::internal::compiler::turboshaft::V<v8::internal::compiler::turboshaft::WordWithBits<64ul>>, v8::internal::compiler::turboshaft::V<v8::internal::compiler::turboshaft::WordWithBits<32ul>>, v8::internal::compiler::turboshaft::ShiftOp::Kind, v8::internal::compiler::turboshaft::WordRepresentation)+0x49) [0x7fb19ce725f9]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewLoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewLoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::ReduceIfReachableShift<v8::internal::compiler::turboshaft::V<v8::internal::compiler::turboshaft::WordWithBits<64ul>>, v8::internal::compiler::turboshaft::V<v8::internal::compiler::turboshaft::WordWithBits<32ul>>, v8::internal::compiler::turboshaft::ShiftOp::Kind, v8::internal::compiler::turboshaft::WordRepresentation>(v8::internal::compiler::turboshaft::V<v8::internal::compiler::turboshaft::WordWithBits<64ul>>, v8::internal::compiler::turboshaft::V<v8::internal::compiler::turboshaft::WordWithBits<32ul>>, v8::internal::compiler::turboshaft::ShiftOp::Kind, v8::internal::compiler::turboshaft::WordRepresentation)+0xc0) [0x7fb19ce72570]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewLoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewLoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::WordPtrShiftRightArithmetic(v8::internal::compiler::turboshaft::ConstOrV<v8::internal::compiler::turboshaft::WordWithBits<64ul>, unsigned long>, v8::internal::compiler::turboshaft::ConstOrV<v8::internal::compiler::turboshaft::WordWithBits<32ul>, unsigned int>)+0x6d) [0x7fb19ceef56d]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::CurrentMemoryPages(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::MemoryIndexImmediate const&, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*)+0xac) [0x7fb19ceef43c]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeMemorySizeImpl(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::TraceLine*, v8::internal::wasm::WasmOpcode)+0x1a6) [0x7fb19ceef376]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeMemorySize(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::WasmOpcode)+0x6e) [0x7fb19ce5b2de]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeFunctionBody()+0x4a9) [0x7fb19ce4ee79]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::Decode()+0x268) [0x7fb19ce360b8]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::InlineWasmCall(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, unsigned int, v8::internal::Signature<v8::internal::wasm::ValueType> const*, unsigned int, bool, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*)+0xbe2) [0x7fb19ce927d2]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::ReturnCallRef(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const&, v8::internal::Signature<v8::internal::wasm::ValueType> const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*)+0x6f6) [0x7fb19cec97c6]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeReturnCallRefImpl(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::TraceLine*, v8::internal::wasm::WasmOpcode)+0x301) [0x7fb19cec9071]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeReturnCallRef(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::WasmOpcode)+0x6e) [0x7fb19ce5a72e]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeFunctionBody()+0x4a9) [0x7fb19ce4ee79]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::Decode()+0x268) [0x7fb19ce360b8]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::InlineWasmCall(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, unsigned int, v8::internal::Signature<v8::internal::wasm::ValueType> const*, unsigned int, bool, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*)+0xbe2) [0x7fb19ce927d2]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::CallDirect(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::CallFunctionImmediate const&, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*)+0x206) [0x7fb19ce8ed96]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallFunctionImpl(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::TraceLine*, v8::internal::wasm::WasmOpcode)+0x24f) [0x7fb19ce8ea7f]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallFunction(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::WasmOpcode)+0x6e) [0x7fb19ce5a3be]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeFunctionBody()+0x4a9) [0x7fb19ce4ee79]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::Decode()+0x268) [0x7fb19ce360b8]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::InlineWasmCall(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, unsigned int, v8::internal::Signature<v8::internal::wasm::ValueType> const*, unsigned int, bool, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*)+0xbe2) [0x7fb19ce927d2]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::ReturnCallRef(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const&, v8::internal::Signature<v8::internal::wasm::ValueType> const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*)+0x6f6) [0x7fb19cec97c6]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeReturnCallRefImpl(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::TraceLine*, v8::internal::wasm::WasmOpcode)+0x301) [0x7fb19cec9071]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeReturnCallRef(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::WasmOpcode)+0x6e) [0x7fb19ce5a72e]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeFunctionBody()+0x4a9) [0x7fb19ce4ee79]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::Decode()+0x268) [0x7fb19ce360b8]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::InlineWasmCall(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, unsigned int, v8::internal::Signature<v8::internal::wasm::ValueType> const*, unsigned int, bool, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*)+0xbe2) [0x7fb19ce927d2]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::CallDirect(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::CallFunctionImmediate const&, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*)+0x206) [0x7fb19ce8ed96]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallFunctionImpl(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::TraceLine*, v8::internal::wasm::WasmOpcode)+0x24f) [0x7fb19ce8ea7f]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallFunction(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::WasmOpcode)+0x6e) [0x7fb19ce5a3be]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeFunctionBody()+0x4a9) [0x7fb19ce4ee79]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::Decode()+0x268) [0x7fb19ce360b8]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::InlineWasmCall(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, unsigned int, v8::internal::Signature<v8::internal::wasm::ValueType> const*, unsigned int, bool, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*)+0xbe2) [0x7fb19ce927d2]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::ReturnCallRef(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const&, v8::internal::Signature<v8::internal::wasm::ValueType> const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*)+0x6f6) [0x7fb19cec97c6]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeReturnCallRefImpl(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::TraceLine*, v8::internal::wasm::WasmOpcode)+0x301) [0x7fb19cec9071]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeReturnCallRef(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::WasmOpcode)+0x6e) [0x7fb19ce5a72e]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeFunctionBody()+0x4a9) [0x7fb19ce4ee79]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::Decode()+0x268) [0x7fb19ce360b8]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::InlineWasmCall(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, unsigned int, v8::internal::Signature<v8::internal::wasm::ValueType> const*, unsigned int, bool, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*)+0xbe2) [0x7fb19ce927d2]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::CallDirect(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::CallFunctionImmediate const&, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*)+0x206) [0x7fb19ce8ed96]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallFunctionImpl(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::TraceLine*, v8::internal::wasm::WasmOpcode)+0x24f) [0x7fb19ce8ea7f]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallFunction(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::WasmOpcode)+0x6e) [0x7fb19ce5a3be]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeFunctionBody()+0x4a9) [0x7fb19ce4ee79]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::Decode()+0x268) [0x7fb19ce360b8]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::InlineWasmCall(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, unsigned int, v8::internal::Signature<v8::internal::wasm::ValueType> const*, unsigned int, bool, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*)+0xbe2) [0x7fb19ce927d2]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::ReturnCallRef(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const&, v8::internal::Signature<v8::internal::wasm::ValueType> const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*)+0x6f6) [0x7fb19cec97c6]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeReturnCallRefImpl(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::TraceLine*, v8::internal::wasm::WasmOpcode)+0x301) [0x7fb19cec9071]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeReturnCallRef(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::WasmOpcode)+0x6e) [0x7fb19ce5a72e]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeFunctionBody()+0x4a9) [0x7fb19ce4ee79]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::Decode()+0x268) [0x7fb19ce360b8]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::BuildTSGraph(v8::internal::compiler::turboshaft::PipelineData*, v8::internal::AccountingAllocator*, v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WasmDetectedFeatures*, v8::internal::compiler::turboshaft::Graph&, v8::internal::wasm::FunctionBody const&, v8::internal::wasm::WireBytesStorage const*, v8::internal::wasm::AssumptionsJournal*, v8::internal::ZoneVector<v8::internal::WasmInliningPosition>*, int)+0x192) [0x7fb19ce340d2]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::wasm::WasmDetectedFeatures*, v8::internal::compiler::CallDescriptor*)+0x5fc) [0x7fb19d8fe63c]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmDetectedFeatures*)+0x384) [0x7fb19ddcfa14]
Aborted

```
## CREDIT INFORMATION

Reporter credit: Zhenjiang Zhao of pangu team, Qianxin

## Attachments

- [2024814](attachments/2024814) (application/octet-stream, 294 B)
- [repro-issue.js](attachments/repro-issue.js) (text/javascript, 2.0 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-08-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6216082308136960.

### am...@chromium.org (2024-08-15)

Fatal error in ../../v8/src/compiler/turboshaft/assembler.h, line 1028

Debug check failed: ValidInputs(result).

//AddressSanitizer:DEADLYSIGNAL

==846==ERROR: AddressSanitizer: ABRT on unknown address 0x05390000034e (pc 0x7911c825100b bp 0x7ffc53959a30 sp 0x7ffc539597d0 T0)

tentatively setting at S1/P1 with the presumption this is an exploitable DCHECK failure

### 24...@project.gserviceaccount.com (2024-08-16)

Detailed Report: https://clusterfuzz.com/testcase?key=6216082308136960

Fuzzing Engine: libFuzzer
Fuzz Target: v8_wasm_deopt_fuzzer
Job Type: libfuzzer_chrome_asan_debug
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  ValidInputs(result) in assembler.h
  v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::
  v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface<v8::internal:
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan_debug&range=1332652:1332662

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6216082308136960

See https://chromium.googlesource.com/chromium/src/+/master/testing/libfuzzer/reproducing.md for instructions on reproducing this bug locally.

### ol...@chromium.org (2024-08-16)

I locally bisected this to https://chromium-review.googlesource.com/c/v8/v8/+/5730174

@leszek can you have a look.

However, I suspect that your CL is not the root cause and we need somebody who is more familiar with wasm here.  The crash is in the wasm turboshaft frontend, ie. during `wasm::BuildTSGraph`.

### ol...@chromium.org (2024-08-16)

To repro I used: `autoninja -C out/x64.optdebug v8_simple_wasm_deopt_fuzzer &&   out/x64.optdebug/v8_simple_wasm_deopt_fuzzer ~/2024814`

### le...@chromium.org (2024-08-16)

Technically this is Michael's CL :)

But I agree that someone more Wasm should look at this. Matthias, can you look and/or dispatch?

### pe...@google.com (2024-08-16)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-08-16)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ml...@chromium.org (2024-08-19)

Thanks for reporting, I'll take a look today.

### ml...@chromium.org (2024-08-19)

Attached is a simplified reproducer. (The flags `--wasm-inlining-factor=1 --nodebug-code` are not needed but slightly reduce the graph size.)

I also exchanged any staged features like memory64 with non-staged-features and was still able to reproduce.

This is a bug with the `InstanceCache` in the turboshaft wasm graph builder.
In this particular case this happens with a `return_call_ref`, but it should be reproducible with `return_call_indirect` as well as neither of them handles the instance cache.

For the non-return-call variants for speculative inlining of `call_ref` we handle the `InstanceCache` properly meaning that we save the state prior to inlining the candidates and restore it for each candidate and for the slow path (the non-inlined case) which was added as part of <https://chromium-review.googlesource.com/c/v8/v8/+/5095095> for [issue 40948450](https://issues.chromium.org/issues/40948450).

For `call_indirect` we do the same for the slow path but we do not update the cache between each inlined candidate.

I'll fix the issues and try to write reproducers for the other cases but I think the long-term fix should be to get rid of this error-prone mechanism and instead switch to using Turboshaft's `Variable` for these values instead.
(I might even try that for this issue depending on how hard it will be to reproduce the different corner cases.)

**Edit**: Updated comment, as the fix linked above does fix the issue fully for `call_ref` and was merged at a state where there wasn't any other variant of speculative inlining implemented yet.

### ml...@chromium.org (2024-08-19)

Trying to write reproducers turns out surprisingly difficult. I'll first fix this issue as a one-of. Then I'll work on [issue 360052650](https://issues.chromium.org/issues/360052650) which is the same issue but for `return_call_indirect` instead of `return_call_ref`.
I'll reduce that reproducer as well which looks somewhat simpler as when I replaced the `return_call_ref` here with `return_call_indirect` it didn't reproduce the issue any more for non-obvious reasons. (This repro also contains some patterns like a useless global.get(global.set(local.get 0))`which should be replaceable with a`local.get 0` but in that case it doesn't repro any more for reasons that aren't directly obvious.

I'll move the investigation for figuring out these cases to later and will first focus on fixing the issue based on the minimized reproducer.

### ap...@google.com (2024-08-20)

Project: v8/v8
Branch: main

commit 782d7f5c714e67134a8a212e12cf5ba8ee74d133
Author: Matthias Liedtke <mliedtke@chromium.org>
Date:   Mon Aug 19 18:33:01 2024

    [turboshaft][wasm] Fix handling InstanceCache in return_call_ref
    
    on speculative inlining.
    A similar issue exists for return_call_indirect which is going to be
    addressed as part of https://crbug.com/360052650.
    
    Fixed: 360044696
    Change-Id: I63e19cb47bff255dd8f3739f1586d41c67d3bead
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5796803
    Auto-Submit: Matthias Liedtke <mliedtke@chromium.org>
    Reviewed-by: Daniel Lehmann <dlehmann@chromium.org>
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95708}

M       src/wasm/turboshaft-graph-interface.cc
A       test/mjsunit/regress/wasm/regress-360044696.js

https://chromium-review.googlesource.com/5796803


### ml...@chromium.org (2024-08-20)

Regarding exploitability: While this is a bug in staged code (it requires Turboshaft, which was finched on stable and we plan on ramping up the finch experiment soon again), I don't think, it's exploitable.

The missing handling for the InstanceCache leads to an optimization trying to read the invalid `OpIndex` which leads to an out of bounds read with a static offset during a later phase if `DCHECK`s are disabled. For stability reasons we'd still would like to back merge for 129 given that we'd like to continue the finch experiment soon.

### pe...@google.com (2024-08-21)

**Merge approved:** your change passed merge requirements and is auto-approved for M129. Please go ahead and merge the CL to branch 6668 (refs/branch-heads/6668) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

### 24...@project.gserviceaccount.com (2024-08-21)

ClusterFuzz testcase 6216082308136960 is verified as fixed in https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan_debug&range=1344275:1344314

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ap...@google.com (2024-08-21)

Project: v8/v8
Branch: refs/branch-heads/12.9

commit d6438f39daee63a0049c65e0865cabd9b5e8ee8d
Author: Matthias Liedtke <mliedtke@chromium.org>
Date:   Mon Aug 19 18:33:01 2024

    Merged: [turboshaft][wasm] Fix handling InstanceCache in return_call_ref
    
    on speculative inlining.
    A similar issue exists for return_call_indirect which is going to be
    addressed as part of https://crbug.com/360052650.
    
    (cherry picked from commit 782d7f5c714e67134a8a212e12cf5ba8ee74d133)
    
    Change-Id: Ib7fa4b4105c4053dc7869ba91fafcd39c8493ddf
    Fixed: 360044696
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5803642
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Reviewed-by: Daniel Lehmann <dlehmann@chromium.org>
    Commit-Queue: Daniel Lehmann <dlehmann@chromium.org>
    Auto-Submit: Matthias Liedtke <mliedtke@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.9@{#4}
    Cr-Branched-From: 64a21d7ad7fca1ddc73a9264132f703f35000b69-refs/heads/12.9.202@{#1}
    Cr-Branched-From: da4200b2cfe6eb1ad73c457ed27cf5b7ff32614f-refs/heads/main@{#95679}

M       src/wasm/turboshaft-graph-interface.cc
A       test/mjsunit/regress/wasm/regress-360044696.js

https://chromium-review.googlesource.com/5803642


### pe...@google.com (2024-08-21)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ml...@chromium.org (2024-08-21)

This issue does not impact Milestone 126 nor any other currently released version.

### go...@google.com (2024-08-21)

Please merge your change to M129 ASAP, branch details can be found here: https://chromiumdash.appspot.com/branches. 

Thank you.

### ml...@chromium.org (2024-08-21)

This has already been merged into v8 12.9 (see [comment #17](https://issues.chromium.org/issues/360044696#comment17)) and the applied `Merged-12.9` label. In the past this was enough for being merged into Chrome as well?

### jk...@chromium.org (2024-08-22)

#21: The bots/scripts don't know that V8's 12.9 branch and corresponding `Merged-12.9` label corresponds with Chromium's 129 milestone and corresponding `Approved-129` label, so the bot in #17 didn't drop the latter label, so we must drop that manually to make tools realize that there is no outstanding merge here any more and hence stop the nag mails.

### rz...@google.com (2024-08-22)

Labelling as not applicable for LTS-120: the changed code isn't present in the 12.0 branch.

### ap...@google.com (2024-08-28)

Project: v8/v8
Branch: main

commit 518df87cb8b90874768b87d41046cf9fc39e5dbd
Author: Daniel Lehmann <dlehmann@chromium.org>
Date:   Wed Aug 28 11:26:28 2024

    [wasm][turboshaft] add test for return_call inlining
    
    ...that mutates a Wasm instance field in the inlinee, since we had bugs
    there before.
    
    Bug: 360044696, 360052650
    Change-Id: I0656e338442b082725bae5346207e9664b796718
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5816134
    Commit-Queue: Daniel Lehmann <dlehmann@chromium.org>
    Auto-Submit: Daniel Lehmann <dlehmann@chromium.org>
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95849}

A       test/mjsunit/wasm/inlining-mutable-instance-fields.js

https://chromium-review.googlesource.com/5816134


### sp...@google.com (2024-08-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
$2,000 for report of OOB read equivalent to information disclosure in a sandboxed process / renderer


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-29)

Thank you for the report. While this might not be fully exploitable, the staging of the features made that difficult to discern and we felt it fair to extend a reward for this report, based on the information presented.

### rz...@google.com (2024-09-02)

Not applicable to 126 as well, turboshaft isn't enabled by default, labelling as not applicable.

### pe...@google.com (2024-11-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/360044696)*
