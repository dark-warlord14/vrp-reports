# Fatal error in ../../src/compiler/turboshaft/graph.h, line 613

| Field | Value |
|-------|-------|
| **Issue ID** | [360052650](https://issues.chromium.org/issues/360052650) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Compiler |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sw...@gmail.com |
| **Assignee** | ml...@chromium.org |
| **Created** | 2024-08-15 |
| **Bounty** | $2,000.00 |

## Description

## VULNERABILITY DETAILS

Fatal error in ../../src/compiler/turboshaft/graph.h, line 613
Debug check failed: i.valid().

## VERSION

V8: HEAD

## REPRODUCTION CASE

Compile `x64.release + is_asan=true` version

Run :

```
./v8_simple_wasm_deopt_fuzzer 2024815

```

ASAN crash info:

```
AddressSanitizer:DEADLYSIGNAL
=================================================================
==16262==ERROR: AddressSanitizer: SEGV on unknown address 0x52d100000417 (pc 0x565541fdfc1f bp 0x7ffc5b2cd270 sp 0x7ffc5b2cd220 T0)
==16262==The signal is caused by a READ memory access.
    #0 0x565541fdfc1f in Is<v8::internal::compiler::turboshaft::ConstantOp> src/compiler/turboshaft/operations.h:956:21
    #1 0x565541fdfc1f in TryCast<v8::internal::compiler::turboshaft::ConstantOp> src/compiler/turboshaft/operations.h:974:10
    #2 0x565541fdfc1f in v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewLoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::TSReducerBase>>::ReducePhi(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation) src/compiler/turboshaft/required-optimization-reducer.h:46:36
    #3 0x56554204f682 in ReduceIfReachablePhi<v8::base::Vector<const v8::internal::compiler::turboshaft::OpIndex>, v8::internal::compiler::turboshaft::RegisterRepresentation> src/compiler/turboshaft/assembler.h:5099:3
    #4 0x56554204f682 in Phi src/compiler/turboshaft/assembler.h:4061:12
    #5 0x56554204f682 in MaybePhi src/wasm/turboshaft-graph-interface.cc:5840:19
    #6 0x56554204f682 in v8::internal::wasm::TurboshaftGraphBuildingInterface::InlineWasmCall(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, unsigned int, v8::internal::Signature<v8::internal::wasm::ValueType> const*, unsigned int, bool, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*) src/wasm/turboshaft-graph-interface.cc:8345:23
    #7 0x565542047cb9 in v8::internal::wasm::TurboshaftGraphBuildingInterface::CallDirect(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::CallFunctionImmediate const&, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*) src/wasm/turboshaft-graph-interface.cc:2643:9
    #8 0x565541ffde9d in DecodeCallFunctionImpl src/wasm/function-body-decoder-impl.h:3927:5
    #9 0x565541ffde9d in v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallFunction(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::WasmOpcode) src/wasm/function-body-decoder-impl.h:3922:3
    #10 0x565541fef747 in v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeFunctionBody() src/wasm/function-body-decoder-impl.h:2875:17
    #11 0x565541fd842f in v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::Decode() src/wasm/function-body-decoder-impl.h:2698:5
    #12 0x56554204daf0 in v8::internal::wasm::TurboshaftGraphBuildingInterface::InlineWasmCall(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, unsigned int, v8::internal::Signature<v8::internal::wasm::ValueType> const*, unsigned int, bool, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*) src/wasm/turboshaft-graph-interface.cc:8290:21
    #13 0x565542085bc0 in v8::internal::wasm::TurboshaftGraphBuildingInterface::ReturnCallIndirect(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const&, v8::internal::wasm::CallIndirectImmediate const&, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*) src/wasm/turboshaft-graph-interface.cc:2965:11
    #14 0x5655420001de in DecodeReturnCallIndirectImpl src/wasm/function-body-decoder-impl.h:3975:5
    #15 0x5655420001de in v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeReturnCallIndirect(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::WasmOpcode) src/wasm/function-body-decoder-impl.h:3963:3
    #16 0x565541fef747 in v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeFunctionBody() src/wasm/function-body-decoder-impl.h:2875:17
    #17 0x565541fd842f in v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::Decode() src/wasm/function-body-decoder-impl.h:2698:5
    #18 0x565541fd6fc0 in v8::internal::wasm::BuildTSGraph(v8::internal::compiler::turboshaft::PipelineData*, v8::internal::AccountingAllocator*, v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WasmDetectedFeatures*, v8::internal::compiler::turboshaft::Graph&, v8::internal::wasm::FunctionBody const&, v8::internal::wasm::WireBytesStorage const*, v8::internal::wasm::AssumptionsJournal*, v8::internal::ZoneVector<v8::internal::WasmInliningPosition>*, int) src/wasm/turboshaft-graph-interface.cc:8550:11
    #19 0x565542d93a0e in v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::wasm::WasmDetectedFeatures*, v8::internal::compiler::CallDescriptor*) src/compiler/pipeline.cc:3518:8
    #20 0x5655432a492e in v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmDetectedFeatures*) src/compiler/turboshaft/wasm-turboshaft-compiler.cc:53:8
    #21 0x565541ebf74f in v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmDetectedFeatures*) src/wasm/function-compiler.cc:170:18
    #22 0x565541ebdede in v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmDetectedFeatures*) src/wasm/function-compiler.cc:34:9
    #23 0x565541ec03fc in v8::internal::wasm::WasmCompilationUnit::CompileWasmFunction(v8::internal::Counters*, v8::internal::wasm::NativeModule*, v8::internal::wasm::WasmDetectedFeatures*, v8::internal::wasm::WasmFunction const*, v8::internal::wasm::ExecutionTier) src/wasm/function-compiler.cc:205:39
    #24 0x565542178a46 in v8::internal::wasm::WasmEngine::CompileFunction(v8::internal::Counters*, v8::internal::wasm::NativeModule*, unsigned int, v8::internal::wasm::ExecutionTier) src/wasm/wasm-engine.cc:874:3
    #25 0x565541f23d79 in v8::internal::wasm::TierUpNowForTesting(v8::internal::Isolate*, v8::internal::Tagged<v8::internal::WasmTrustedInstanceData>, int) src/wasm/module-compiler.cc:1666:26
    #26 0x56553fd8a13d in FuzzIt test/fuzzer/wasm-deopt.cc:298:5
    #27 0x56553fd8a13d in LLVMFuzzerTestOneInput test/fuzzer/wasm-deopt.cc:308:10
    #28 0x56553fd88162 in main test/fuzzer/fuzzer.cc:59:3
    #29 0x7f736620bd8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

==16262==Register values:
rax = 0x0000000000000000  rbx = 0x00007f7364931130  rcx = 0x0000000000000001  rdx = 0x0000000000000002
rdi = 0x0000525000087120  rsi = 0x0000529000015c30  rbp = 0x00007ffc5b2cd270  rsp = 0x00007ffc5b2cd220
 r8 = 0x00007f7364931128   r9 = 0x00000fee6c926225  r10 = 0x000052d100000417  r11 = 0x0000000000000008
r12 = 0x00007f7364932194  r13 = 0x000052d000000418  r14 = 0x0000000000000004  r15 = 0x00000000ffffffff
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV src/compiler/turboshaft/operations.h:956:21 in Is<v8::internal::compiler::turboshaft::ConstantOp>
==16262==ABORTING

```

Compile `x64.debug` version

crash log:

```
#
# Fatal error in ../../src/compiler/turboshaft/graph.h, line 613
# Debug check failed: i.valid().
#
#
#
#FailureMessage Object: 0x7ffc7ce10618
==== C stack trace ===============================

    /data/v8/v8/out/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1e) [0x7ff0c8fc2d2e]
    /data/v8/v8/out/x64.debug/libv8_libplatform.so(+0x56d7d) [0x7ff0c8f20d7d]
    /data/v8/v8/out/x64.debug/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x205) [0x7ff0c8f983d5]
    /data/v8/v8/out/x64.debug/libv8_libbase.so(+0x55d8c) [0x7ff0c8f97d8c]
    /data/v8/v8/out/x64.debug/libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x4d) [0x7ff0c8f984ad]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::Graph::Get(v8::internal::compiler::turboshaft::OpIndex)+0x44) [0x7ff0d143ecc4]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewLoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::Get(v8::internal::compiler::turboshaft::OpIndex) const+0x29) [0x7ff0d1877b49]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewLoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::TSReducerBase>>::ReducePhiHelper(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x15b) [0x7ff0d187826b]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewLoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::TSReducerBase>>::ReducePhi<v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation>(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x1c2) [0x7ff0d1878082]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewLoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewLoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::ReduceIfReachablePhi<v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation>(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0xbb) [0x7ff0d1877e7b]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewLoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewLoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::Phi(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x44) [0x7ff0d1877b94]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::MaybePhi(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::wasm::ValueType)+0xe4) [0x7ff0d18a3924]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::InlineWasmCall(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, unsigned int, v8::internal::Signature<v8::internal::wasm::ValueType> const*, unsigned int, bool, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*)+0x11b1) [0x7ff0d18cbda1]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::CallDirect(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::CallFunctionImmediate const&, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*)+0x206) [0x7ff0d18c7d96]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallFunctionImpl(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::TraceLine*, v8::internal::wasm::WasmOpcode)+0x24f) [0x7ff0d18c7a7f]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallFunction(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::WasmOpcode)+0x6e) [0x7ff0d18933be]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeFunctionBody()+0x4a9) [0x7ff0d1887e79]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::Decode()+0x268) [0x7ff0d186f0b8]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::InlineWasmCall(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, unsigned int, v8::internal::Signature<v8::internal::wasm::ValueType> const*, unsigned int, bool, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*)+0xbe2) [0x7ff0d18cb7d2]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::ReturnCallIndirect(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const&, v8::internal::wasm::CallIndirectImmediate const&, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*)+0x851) [0x7ff0d1900291]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeReturnCallIndirectImpl(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::TraceLine*, v8::internal::wasm::WasmOpcode)+0x2e5) [0x7ff0d18ff9a5]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeReturnCallIndirect(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::WasmOpcode)+0x6e) [0x7ff0d18935ce]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeFunctionBody()+0x4a9) [0x7ff0d1887e79]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::Decode()+0x268) [0x7ff0d186f0b8]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::BuildTSGraph(v8::internal::compiler::turboshaft::PipelineData*, v8::internal::AccountingAllocator*, v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WasmDetectedFeatures*, v8::internal::compiler::turboshaft::Graph&, v8::internal::wasm::FunctionBody const&, v8::internal::wasm::WireBytesStorage const*, v8::internal::wasm::AssumptionsJournal*, v8::internal::ZoneVector<v8::internal::WasmInliningPosition>*, int)+0x192) [0x7ff0d186d0d2]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::wasm::WasmDetectedFeatures*, v8::internal::compiler::CallDescriptor*)+0x5fc) [0x7ff0d233763c]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmDetectedFeatures*)+0x384) [0x7ff0d2808a14]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmDetectedFeatures*)+0x889) [0x7ff0d177aa59]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmDetectedFeatures*)+0xce) [0x7ff0d177a00e]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmCompilationUnit::CompileWasmFunction(v8::internal::Counters*, v8::internal::wasm::NativeModule*, v8::internal::wasm::WasmDetectedFeatures*, v8::internal::wasm::WasmFunction const*, v8::internal::wasm::ExecutionTier)+0x2ea) [0x7ff0d177ae6a]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmEngine::CompileFunction(v8::internal::Counters*, v8::internal::wasm::NativeModule*, unsigned int, v8::internal::wasm::ExecutionTier)+0xa9) [0x7ff0d19d2639]
    /data/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::TierUpNowForTesting(v8::internal::Isolate*, v8::internal::Tagged<v8::internal::WasmTrustedInstanceData>, int)+0xb4) [0x7ff0d17cc5c4]
    /data/v8/v8/out/x64.debug/v8_simple_wasm_deopt_fuzzer(+0x84b2d) [0x560c96a6db2d]
    /data/v8/v8/out/x64.debug/v8_simple_wasm_deopt_fuzzer(LLVMFuzzerTestOneInput+0x2e) [0x560c96a6cd0e]
    /data/v8/v8/out/x64.debug/v8_simple_wasm_deopt_fuzzer(main+0x220) [0x560c96a6b830]
    /lib/x86_64-linux-gnu/libc.so.6(+0x29d90) [0x7ff0c8af6d90]
    /lib/x86_64-linux-gnu/libc.so.6(__libc_start_main+0x80) [0x7ff0c8af6e40]
    /data/v8/v8/out/x64.debug/v8_simple_wasm_deopt_fuzzer(_start+0x2a) [0x560c96a6b54a]
Aborted

```
## CREDIT INFORMATION

Reporter credit: Zhenjiang Zhao of pangu team, Qianxin

## Attachments

- [2024815](attachments/2024815) (application/octet-stream, 294 B)

## Timeline

### sw...@gmail.com (2024-08-15)

Attach PoC crash file

### cl...@appspot.gserviceaccount.com (2024-08-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5168124615655424.

### ad...@google.com (2024-08-15)

Assigning to current V8 sheriff with a provisional severity and FoundIn. Samuel, please adjust. I also tried to upload this to CF but I'm not sure whether I've attempted to feed it to the right fuzzer or not.

### pe...@google.com (2024-08-15)

Setting milestone because of s0/s1 severity.

### sa...@google.com (2024-08-15)

Clusterfuzz doesn't seem to make much progress on this one for some reason. Matthias, could you take a look at this as you added that fuzzer IIRC?

### pe...@google.com (2024-08-15)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### 24...@project.gserviceaccount.com (2024-08-16)

Detailed Report: https://clusterfuzz.com/testcase?key=5168124615655424

Fuzzing Engine: libFuzzer
Fuzz Target: v8_wasm_deopt_fuzzer
Job Type: libfuzzer_chrome_asan_debug
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  i.valid() in graph.h
  v8::internal::compiler::turboshaft::Graph::Get
  v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::co
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan_debug&range=1327366:1327384

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5168124615655424

See https://chromium.googlesource.com/chromium/src/+/master/testing/libfuzzer/reproducing.md for instructions on reproducing this bug locally.

### 24...@project.gserviceaccount.com (2024-08-16)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### ml...@chromium.org (2024-08-19)

Thanks for reporting, I'll take a look today. It is not unlikely that this issue and [issue 360044696](https://issues.chromium.org/issues/360044696) have the same root cause.

### ml...@chromium.org (2024-08-19)

> It is not unlikely that this issue and [issue 360044696](https://issues.chromium.org/issues/360044696) have the same root cause.

Yes, same root cause, one uses `return_call_ref` and the other uses `return_call_indirect` but it's the same thing (although it's two different code locations).
The fix is WIP: <https://chromium-review.googlesource.com/c/v8/v8/+/5798122>

### ap...@google.com (2024-08-20)

Project: v8/v8
Branch: main

commit 72c9d556f9364a634726b857000a18b2835b6f47
Author: Matthias Liedtke <mliedtke@chromium.org>
Date:   Mon Aug 19 18:48:12 2024

    [turboshaft][wasm] Fix handling InstanceCache in return_call_indirect
    
    on speculative inlining.
    Same change as for return_call_ref in https://crrev.com/c/5796803
    
    Fixed: 360052650
    Change-Id: I54de1f2145db25324b6d0cce0ccfac9530a08b13
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5798122
    Reviewed-by: Daniel Lehmann <dlehmann@chromium.org>
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95709}

M       src/wasm/turboshaft-graph-interface.cc
M       test/mjsunit/mjsunit.status
A       test/mjsunit/regress/wasm/regress-360052650.js

https://chromium-review.googlesource.com/5798122


### pe...@google.com (2024-08-20)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M126. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to other stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M127. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M128. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### ml...@chromium.org (2024-08-20)

This particular bug requires the experimental feature `--wasm-inlining-call-indirect` which is enabled by the fuzzer for initial coverage but is still experimental and not staged yet.

Therefore this isn't really a security bug either. We are not going to stage and finch it prior to chrome 130, so we don't need any backmerges here.

### ml...@chromium.org (2024-08-20)

I forgot to include this on the previous message: Even though it is "just" a bug in an experimental feature, thanks a lot for the report! While we run the `wasm_deopt` fuzzer on our infrastructure we have not seen this particular crash there, so this report is very helpful.

### 24...@project.gserviceaccount.com (2024-08-21)

ClusterFuzz testcase 5168124615655424 is verified as fixed in https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan_debug&range=1344275:1344314

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

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

Thank you for the report! While this might not be fully exploitable based on the status of these features at this time, the staging of the features made that difficult to discern and we felt it fair to extend a reward for this report, based on the information presented.

### pe...@google.com (2024-11-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/360052650)*
