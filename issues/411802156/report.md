# Security: Fatal error in src/compiler/turboshaft/operations.cc, line 152

| Field | Value |
|-------|-------|
| **Issue ID** | [411802156](https://issues.chromium.org/issues/411802156) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Compiler>Turbofan |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | da...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2025-04-19 |
| **Bounty** | $7,000.00 |

## Description

# VULNERABILITY DETAILS

A representation mismatch occurring in Turboshaft has been identified by `ValidateOpInputRep()` located at `src/compiler/turboshaft/operations.cc, line 152`. Despite Turboshaft's invariant condition that 'all input values of Phi nodes must have the same RegisterRepresentation,' the Phi(#25) node is declared as Tagged, and one of its inputs, Phi(#251), has Word32.

```
Turboshaft operation Phi(#25, #25, #313, #222, #25)[Tagged] has input #222:Phi(#198, #222)[Word32] with wrong representation.
Expected Tagged but found Word32.
Input: Phi(#198, #222)[Word32]

```

Bisect identified the issue in the commit [Delay allocation of input locations](https://chromium-review.googlesource.com/c/v8/v8/+/6338545) on March 11, 2025.

This crash reliably triggers in both Release and Debug builds, and in Release builds, it appears that the incorrect representation propagates without causing a separate crash when run without the `--assert-types` flag.

# VERSION

Chrome Version: V8 Main branch HEAD commit ~ [24bf2aef05ec4b930feecc195874de204185f647](https://chromium-review.googlesource.com/c/v8/v8/+/6338545)

# Operating System

Ubuntu 22.04 LTS

# REPRODUCTION CASE

`./d8 --jit-fuzzing --turbolev --assert-types ./poc.js`

# Type of crash

Fatal error(representation mismatch)

# Crash State

```
1. Crash log

Turboshaft operation Phi(#25, #25, #313, #222, #25)[Tagged] has input #222:Phi(#198, #222)[Word32] with wrong representation.
Expected Tagged but found Word32.
Input: Phi(#198, #222)[Word32]


#
# Fatal error in ../../src/compiler/turboshaft/operations.cc, line 152
# unreachable code
#
#
#
#FailureMessage Object: 0x7ffc0f875c40
==== C stack trace ===============================

    ./d8(v8::base::debug::StackTrace::StackTrace()+0x13) [0x55d5c0ed1753]
    ./d8(+0x438bf6b) [0x55d5c0ed0f6b]
    ./d8(V8_Fatal(char const*, int, char const*, ...)+0x183) [0x55d5c0eb84e3]
    ./d8(v8::internal::compiler::turboshaft::ValidateOpInputRep(v8::internal::compiler::turboshaft::Graph const&, v8::internal::compiler::turboshaft::OpIndex, std::initializer_list<v8::internal::compiler::turboshaft::RegisterRepresentation>, v8::internal::compiler::turboshaft::Operation const*, std::__Cr::optional<unsigned long>)+0x217) [0x55d5c0670997]
    ./d8(v8::internal::compiler::turboshaft::ValidateOpInputRep(v8::internal::compiler::turboshaft::Graph const&, v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::RegisterRepresentation, v8::internal::compiler::turboshaft::Operation const*, std::__Cr::optional<unsigned long>)+0x2f) [0x55d5c0670cdf]
    ./d8(v8::internal::compiler::turboshaft::PhiOp& v8::internal::compiler::turboshaft::OperationT<v8::internal::compiler::turboshaft::PhiOp>::New<v8::internal::compiler::turboshaft::ShadowyOpIndexVectorWrapper, v8::internal::compiler::turboshaft::RegisterRepresentation>(v8::internal::compiler::turboshaft::Graph*, unsigned long, v8::internal::compiler::turboshaft::ShadowyOpIndexVectorWrapper, v8::internal::compiler::turboshaft::RegisterRepresentation)+0xd8) [0x55d5bf934f58]
    ./d8(v8::internal::compiler::turboshaft::PhiOp& v8::internal::compiler::turboshaft::Graph::Add<v8::internal::compiler::turboshaft::PhiOp, v8::internal::compiler::turboshaft::ShadowyOpIndexVectorWrapper, v8::internal::compiler::turboshaft::RegisterRepresentation>(v8::internal::compiler::turboshaft::ShadowyOpIndexVectorWrapper, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x5b) [0x55d5bf934b7b]
    ./d8(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>>::Emit<v8::internal::compiler::turboshaft::PhiOp, v8::internal::compiler::turboshaft::ShadowyOpIndexVectorWrapper, v8::internal::compiler::turboshaft::RegisterRepresentation>(v8::internal::compiler::turboshaft::ShadowyOpIndexVectorWrapper, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x60) [0x55d5c05c8740]
    ./d8(v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>>>::ReducePhiHelper(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x135) [0x55d5c05c86b5]
    ./d8(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>>>::ReducePhi<v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation>(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x11e) [0x55d5c05c839e]
    ./d8(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::ValueNumberingReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>>>>::ReducePhi<v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation>(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x51) [0x55d5c05c81d1]
    ./d8(v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::ValueNumberingReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>>>>>>::ReducePhiHelper(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x215) [0x55d5c05c8025]
    ./d8(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::ValueNumberingReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>>>>>>::ReducePhi<v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation>(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x11e) [0x55d5c05c7dde]
    ./d8(v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::ValueNumberingReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>>>>>>>::ReducePhiHelper(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x215) [0x55d5c05c7b85]
    ./d8(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::ValueNumberingReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>>>>>>>::ReducePhi<v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation>(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x11e) [0x55d5c05c793e]
    ./d8(v8::internal::compiler::turboshaft::VariableReducer<v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::ValueNumberingReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>>>>>>>::MergeOpIndices(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::MaybeRegisterRepresentation)+0xaf) [0x55d5c05c57cf]
    ./d8(void v8::internal::compiler::turboshaft::SnapshotTable<v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::VariableData>::MergePredecessors<v8::internal::compiler::turboshaft::VariableReducer<v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::ValueNumberingReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>>>>>>>::Bind(v8::internal::compiler::turboshaft::Block*)::'lambda'(v8::internal::compiler::turboshaft::SnapshotTableKey<v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::VariableData>, v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>), void v8::internal::compiler::turboshaft::ChangeTrackingSnapshotTable<v8::internal::compiler::turboshaft::VariableReducer<v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::ValueNumberingReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>>>>>>>::VariableTable, v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::VariableData>::StartNewSnapshot<v8::internal::compiler::turboshaft::VariableReducer<v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::ValueNumberingReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>>>>>>>::Bind(v8::internal::compiler::turboshaft::Block*)::'lambda'(v8::internal::compiler::turboshaft::SnapshotTableKey<v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::VariableData>, v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>)>(v8::base::Vector<v8::internal::compiler::turboshaft::SnapshotTable<v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::VariableData>::Snapshot const>, v8::internal::compiler::turboshaft::VariableReducer<v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::ValueNumberingReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>>>>>>>::Bind(v8::internal::compiler::turboshaft::Block*)::'lambda'(v8::internal::compiler::turboshaft::SnapshotTableKey<v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::VariableData>, v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>) const&) requires std::is_invocable_v<TL0_, v8::internal::compiler::turboshaft::ChangeTrackingSnapshotTable::Key, v8::base::Vector<T0 const>>::'lambda'(v8::internal::compiler::turboshaft::SnapshotTableKey<v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::VariableData>, v8::internal::compiler::turboshaft::OpIndex const&, v8::internal::compiler::turboshaft::OpIndex const&)>(v8::base::Vector<v8::internal::compiler::turboshaft::SnapshotTable<v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::VariableData>::Snapshot const>, v8::internal::compiler::turboshaft::VariableReducer<v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::ValueNumberingReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>>>>>>>::Bind(v8::internal::compiler::turboshaft::Block*)::'lambda'(v8::internal::compiler::turboshaft::SnapshotTableKey<v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::VariableData>, v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>) const&, T0 const&)+0x2ef) [0x55d5c05c534f]
    ./d8(v8::internal::compiler::turboshaft::VariableReducer<v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::ValueNumberingReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>>>>>>>::Bind(v8::internal::compiler::turboshaft::Block*)+0x1cc) [0x55d5c05c4a1c]
    ./d8(v8::internal::compiler::turboshaft::BlockOriginTrackingReducer<v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer<v8::internal::compiler::turboshaft::MachineOptimizationReducer<v8::internal::compiler::turboshaft::VariableReducer<v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::ValueNumberingReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal:debug2: channel 0: window 998036 sent adjust 50540
:compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>>>>>>>>>>::Bind(v8::internal::compiler::turboshaft::Block*)+0x16) [0x55d5c05c4256]
    ./d8(v8::internal::compiler::turboshaft::Assembler<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::Bind(v8::internal::compiler::turboshaft::Block*)+0x73) [0x55d5c05c39b3]
    ./d8(v8::internal::compiler::turboshaft::GraphBuildingNodeProcessor::StartMultiPredecessorExceptionBlock(v8::internal::maglev::BasicBlock*, v8::internal::compiler::turboshaft::Block*)+0x2ce) [0x55d5c05da9de]
    ./d8(v8::internal::compiler::turboshaft::GraphBuildingNodeProcessor::StartExceptionBlock(v8::internal::maglev::BasicBlock*)+0xd0) [0x55d5c05d7f70]
    ./d8(v8::internal::compiler::turboshaft::GraphBuildingNodeProcessor::PreProcessBasicBlock(v8::internal::maglev::BasicBlock*)+0x218) [0x55d5c05bbdc8]
    ./d8(v8::internal::maglev::GraphProcessor<v8::internal::compiler::turboshaft::NodeProcessorBase, true>::ProcessGraph(v8::internal::maglev::Graph*)+0x11a) [0x55d5c05aefea]
    ./d8(v8::internal::compiler::turboshaft::MaglevGraphBuildingPhase::Run(v8::internal::compiler::turboshaft::PipelineData*, v8::internal::Zone*, v8::internal::compiler::Linkage*)+0x264) [0x55d5c05aecb4]
    ./d8(auto v8::internal::compiler::turboshaft::Pipeline::Run<v8::internal::compiler::turboshaft::MaglevGraphBuildingPhase, v8::internal::compiler::Linkage*&>(v8::internal::compiler::Linkage*&)+0xd7) [0x55d5c0153567]
    ./d8(v8::internal::compiler::turboshaft::Pipeline::CreateGraphWithMaglev(v8::internal::compiler::Linkage*)+0xb0) [0x55d5c0143eb0]
    ./d8(v8::internal::compiler::PipelineCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x1f7) [0x55d5c0143cd7]
    ./d8(v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x7f) [0x55d5be985d3f]
    ./d8(+0x1e4fd04) [0x55d5be994d04]
    ./d8(v8::internal::Compiler::CompileOptimized(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::ConcurrencyMode, v8::internal::CodeKind)+0x28c) [0x55d5be99718c]
    ./d8(+0x29391ae) [0x55d5bf47e1ae]
    ./d8(+0x29330c5) [0x55d5bf4780c5]
    ./d8(v8::internal::Runtime_OptimizeTurbofanEager(int, unsigned long*, v8::internal::Isolate*)+0x90) [0x55d5bf477d10]
    ./d8(+0x40a413d) [0x55d5c0be913d]

```
```
2. Backtrace with symbols

#0  0x00005555598dc772 in v8::base::OS::Abort()::$_0::operator()() const (this=<optimized out>) at ../../src/base/platform/platform-posix.cc:731
#1  v8::base::OS::Abort () at ../../src/base/platform/platform-posix.cc:731
#2  0x00005555598c74f1 in V8_Fatal (file=0x5555569ac293 "../../src/compiler/turboshaft/operations.cc", line=line@entry=152, format=0x5555569cd65d "unreachable code") at ../../src/base/logging.cc:215
#3  0x000055555907f997 in v8::internal::compiler::turboshaft::ValidateOpInputRep (graph=..., input=..., expected_reps=..., checked_op=<optimized out>, projection_index=...) at ../../src/compiler/turboshaft/operations.cc:152
debug2: channel 0: window 999243 sent adjust 49333
#4  0x000055555907fcdf in v8::internal::compiler::turboshaft::ValidateOpInputRep (graph=..., input=..., input@entry=..., expected_rep=..., checked_op=0x2, checked_op@entry=0x106c01039470, projection_index=...) at ../../src/compiler/turboshaft/operations.cc:159
#5  0x0000555558343f58 in v8::internal::compiler::turboshaft::OperationT<v8::internal::compiler::turboshaft::PhiOp>::New<v8::internal::compiler::turboshaft::ShadowyOpIndexVectorWrapper, v8::internal::compiler::turboshaft::RegisterRepresentation> (graph=graph@entry=0x106c01060018, input_count=input_count@entry=5, args=..., args=...) at ../../src/compiler/turboshaft/operations.h:1140
#6  0x0000555558343b7b in v8::internal::compiler::turboshaft::OperationT<v8::internal::compiler::turboshaft::PhiOp>::New<v8::internal::compiler::turboshaft::RegisterRepresentation> (graph=0x106c01060018, inputs=..., args=...) at ../../src/compiler/turboshaft/operations.h:1153
#7  v8::internal::compiler::turboshaft::Graph::Add<v8::internal::compiler::turboshaft::PhiOp, v8::internal::compiler::turboshaft::ShadowyOpIndexVectorWrapper, v8::internal::compiler::turboshaft::RegisterRepresentation> (this=0x106c01060018, args=..., args=...) at ../../src/compiler/turboshaft/graph.h:725
#8  0x0000555558fd7740 in v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase> > >::Emit<v8::internal::compiler::turboshaft::PhiOp, v8::internal::compiler::turboshaft::ShadowyOpIndexVectorWrapper, v8::internal::compiler::turboshaft::RegisterRepresentation> (this=this@entry=0x7fffffffb5c0, args=..., args=...) at ../../src/compiler/turboshaft/assembler.h:986
#9  0x0000555558fd76b5 in v8::internal::compiler::turboshaft::ReducerBaseForwarder<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase> > > >::ReducePhi<v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation> (this=0x7ffff7e8fa60 <_IO_stdfile_2_lock>, args=..., args=...) at ../../src/compiler/turboshaft/assembler.h:1076
#10 v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase> > > >::ReducePhiHelper (this=0x7ffff7e8fa60 <_IO_stdfile_2_lock>, this@entry=0x7fffffffb5c0, inputs=..., rep=rep@entry=...) at ../../src/compiler/turboshaft/assembler.h:1142
#11 0x0000555558fd739e in v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase> > > >::ReducePhi<v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation> (this=0x7fffffffb5c0, args=..., args=...) at ../../src/compiler/turboshaft/assembler.h:1138
#12 0x0000555558fd71d1 in v8::internal::compiler::turboshaft::ValueNumberingReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase> > > > >::ReducePhi<v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation> (this=this@entry=0x7fffffffb5c0, args=args@entry=..., args=args@entry=...) at ../../src/compiler/turboshaft/value-numbering-reducer.h:147
#13 0x0000555558fd7025 in v8::internal::compiler::turboshaft::UniformReducerAdapter<v8::internal::compiler::turboshaft::EmitProjectionReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase> > > > > >::ReducePhiContinuation::Reduce<v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation> (args=..., args=..., this=<optimized out>) at ../../src/compiler/turboshaft/uniform-reducer-adapter.h:147
#14 v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::ValueNumberingReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase> > > > > >::ReduceOperation<(v8::internal::compiler::turboshaft::Opcode)86, v8::internal::compiler::turboshaft::UniformReducerAdapter<v8::internal::compiler::turboshaft::EmitProjectionReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase> > > > > >::ReducePhiContinuation, v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation> (this=0x7fffffffb5c0, args=..., args=...) at ../../src/compiler/turboshaft/assembler.h:940
#15 v8::internal::compiler::turboshaft::UniformReducerAdapter<v8::internal::compiler::turboshaft::EmitProjectionReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase> > > > > >::ReducePhi<v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation> (this=0x7fffffffb5c0, args=..., args=...) at ../../src/compiler/turboshaft/uniform-reducer-adapter.h:147
#16 v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::ValueNumberingReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase> > > > > > >::ReducePhiHelper (this=this@entry=0x7fffffffb5c0, inputs=..., rep=rep@entry=...) at ../../src/compiler/turboshaft/required-optimization-reducer.h:32
#17 0x0000555558fd6dde in v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::ValueNumberingReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase> > > > > > >::ReducePhi<v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation> (this=this@entry=0x7fffffffb5c0, args=args@entry=..., args=args@entry=...) at ../../src/compiler/turboshaft/required-optimization-reducer.h:30
#18 0x0000555558fd6b85 in v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::ValueNumberingReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase> > > > > > > >::ReducePhiHelper (this=0x7ffff7e8fa60 <_IO_stdfile_2_lock>, this@entry=0x7fffffffb5c0, inputs=..., rep=rep@entry=...) at ../../src/compiler/turboshaft/required-optimization-reducer.h:32
#19 0x0000555558fd693e in v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::ValueNumberingReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase> > > > > > > >::ReducePhi<v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation> (this=this@entry=0x7fffffffb5c0, args=..., args=...) at ../../src/compiler/turboshaft/required-optimization-reducer.h:30
#20 0x0000555558fd47cf in v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface<v8::internal::compiler::turboshaft::Assembler<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase> > >::ReduceIfReachablePhi<v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation> (this=0x7fffffffb908, args=..., args=...) at ../../src/compiler/turboshaft/assembler.h:5190
#21 v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface<v8::internal::compiler::turboshaft::Assembler<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase> > >::Phi (this=0x7fffffffb908, inputs=..., rep=...) at ../../src/compiler/turboshaft/assembler.h:4110
#22 v8::internal::compiler::turboshaft::VariableReducer<v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::ValueNumberingReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase> > > > > > > >::MergeOpIndices (this=0x7fffffffb5c0, inputs=..., maybe_rep=...) at ../../src/compiler/turboshaft/variable-reducer.h:235
#23 0x0000555558fd4683 in v8::internal::compiler::turboshaft::VariableReducer<v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::ValueNumberingReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase> > > > > > > >::Bind(v8::internal::compiler::turboshaft::Block*)::{lambda(v8::internal::compiler::turboshaft::SnapshotTableKey<v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::VariableData>, v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>)#1}::operator()(v8::internal::compiler::turboshaft::SnapshotTableKey<v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::VariableData>, v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>) const (this=this@entry=0x7fffffffb208, var=..., var@entry=..., predecessors=...) at ../../src/compiler/turboshaft/variable-reducer.h:123
#24 0x0000555558fd434f in _ZN2v88internal8compiler10turboshaft13SnapshotTableINS2_7OpIndexENS2_12VariableDataEE17MergePredecessorsIZNS2_15VariableReducerINS2_27RequiredOptimizationReducerINS2_21EmitProjectionReducerINS2_21ValueNumberingReducerINS2_18GenericReducerBaseINS2_13TSReducerBaseINS2_11StackBottomINS_4base3tmp5list1IJNS2_26BlockOriginTrackingReducerENS2_26MaglevEarlyLoweringReducerENS2_26MachineOptimizationReducerES8_S9_SB_SD_EEEEEEEEEEEEEEEE4BindEPNS2_5BlockEEUlNS2_16SnapshotTableKeyIS4_S5_EENSF_6VectorIKS4_EEE_ZNS2_27ChangeTrackingSnapshotTableINSS_13VariableTableES4_S5_E16StartNewSnapshotIS10_EEvNSX_IKNS6_8SnapshotEEERKT_Qsr3stdE14is_invocable_vITL0__NS2_27ChangeTrackingSnapshotTable3KeyENSX_IKT0_EEEEUlSW_RSY_S1H_E_EEvS17_S1A_RS1F_ (this=this@entry=0x7fffffffb680, predecessors=..., merge_fun=..., change_callback=...) at ../../src/compiler/turboshaft/snapshot-table.h:501
#25 0x0000555558fd3a1c in _ZN2v88internal8compiler10turboshaft13SnapshotTableINS2_7OpIndexENS2_12VariableDataEE16StartNewSnapshotIZNS2_15VariableReducerINS2_27RequiredOptimizationReducerINS2_21EmitProjectionReducerINS2_21ValueNumberingReducerINS2_18GenericReducerBaseINS2_13TSReducerBaseINS2_11StackBottomINS_4base3tmp5list1IJNS2_26BlockOriginTrackingReducerENS2_26MaglevEarlyLoweringReducerENS2_26MachineOptimizationReducerES8_S9_SB_SD_EEEEEEEEEEEEEEEE4BindEPNS2_5BlockEEUlNS2_16SnapshotTableKeyIS4_S5_EENSF_6VectorIKS4_EEE_ZNS2_27ChangeTrackingSnapshotTableINSS_13VariableTableES4_S5_E16StartNewSnapshotIS10_EEvNSX_IKNS6_8SnapshotEEERKT_Qsr3stdE14is_invocable_vITL0__NS2_27ChangeTrackingSnapshotTable3KeyENSX_IKT0_EEEEUlSW_RSY_S1H_E_EEvS17_S1A_RS1F_Qaasr3stdE14is_invocable_vIS1B_NSV_IS18_S1E_EENSX_IS19_EEEsr3stdE14is_invocable_vITL0_0_S1K_S18_S18_E (this=0x7fffffffb680, predecessors=..., merge_fun=..., change_callback=...) at ../../src/compiler/turboshaft/snapshot-table.h:184
#26 _ZN2v88internal8compiler10turboshaft27ChangeTrackingSnapshotTableINS2_15VariableReducerINS2_27RequiredOptimizationReducerINS2_21EmitProjectionReducerINS2_21ValueNumberingReducerINS2_18GenericReducerBaseINS2_13TSReducerBaseINS2_11StackBottomINS_4base3tmp5list1IJNS2_26BlockOriginTrackingReducerENS2_26MaglevEarlyLoweringReducerENS2_26MachineOptimizationReducerES4_S5_S7_S9_EEEEEEEEEEEEEEEE13VariableTableENS2_7OpIndexENS2_12VariableDataEE16StartNewSnapshotIZNSO_4BindEPNS2_5BlockEEUlNS2_16SnapshotTableKeyISQ_SR_EENSB_6VectorIKSQ_EEE_EEvNSY_IKNS2_13SnapshotTableISQ_SR_E8SnapshotEEERKT_Qsr3stdE14is_invocable_vITL0__NS2_27ChangeTrackingSnapshotTable3KeyENSY_IKT0_EEE (this=0x7fffffffb680, predecessors=..., merge_fun=...) at ../../src/compiler/turboshaft/snapshot-table.h:542
#27 v8::internal::compiler::turboshaft::VariableReducer<v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::ValueNumberingReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase> > > > > > > >::Bind (this=this@entry=0x7fffffffb5c0, new_block=new_block@entry=0x106c0103d448) at ../../src/compiler/turboshaft/variable-reducer.h:126
#28 0x0000555558fd3256 in v8::internal::compiler::turboshaft::BlockOriginTrackingReducer<v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer<v8::internal::compiler::turboshaft::MachineOptimizationReducer<v8::internal::compiler::turboshaft::VariableReducer<v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::ValueNumberingReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase> > > > > > > > > > >::Bind (this=0x7ffff7e8fa60 <_IO_stdfile_2_lock>, this@entry=0x7fffffffb5c0, block=0x0, block@entry=0x106c0103d448) at ../../src/compiler/turboshaft/maglev-graph-building-phase.cc:101
#29 0x0000555558fd29b3 in v8::internal::compiler::turboshaft::Assembler<v8::base::tmp::list1<v8::internal::compiler::turboshaft::BlockOriginTrackingReducer, v8::internal::compiler::turboshaft::MaglevEarlyLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase> >::Bind (this=this@entry=0x7fffffffb5a0, block=0x0, block@entry=0x106c0103d448) at ../../src/compiler/turboshaft/assembler.h:5335
#30 0x0000555558fe99de in v8::internal::compiler::turboshaft::GraphBuildingNodeProcessor::StartMultiPredecessorExceptionBlock (this=this@entry=0x7fffffffb570, maglev_catch_handler=maglev_catch_handler@entry=0x106c0102c0e8, turboshaft_catch_handler=turboshaft_catch_handler@entry=0x106c0103d448) at ../../src/compiler/turboshaft/maglev-graph-building-phase.cc:831
#31 0x0000555558fe6f70 in v8::internal::compiler::turboshaft::GraphBuildingNodeProcessor::StartExceptionBlock (this=0x7ffff7e8fa60 <_IO_stdfile_2_lock>, this@entry=0x7fffffffb570, maglev_catch_handler=0x0) at ../../src/compiler/turboshaft/maglev-graph-building-phase.cc:751
#32 0x0000555558fcadc8 in v8::internal::compiler::turboshaft::GraphBuildingNodeProcessor::PreProcessBasicBlock (this=0x7ffff7e8fa60 <_IO_stdfile_2_lock>, this@entry=0x7fffffffb570, maglev_block=0x106c0102c0e8) at ../../src/compiler/turboshaft/maglev-graph-building-phase.cc:616
#33 0x0000555558fbdfea in v8::internal::maglev::GraphProcessor<v8::internal::compiler::turboshaft::NodeProcessorBase, true>::ProcessGraph (this=this@entry=0x7fffffffb570, graph=graph@entry=0x106c001e3818) at ../../src/maglev/maglev-graph-processor.h:133
#34 0x0000555558fbdcb4 in v8::internal::compiler::turboshaft::MaglevGraphBuildingPhase::Run (this=<optimized out>, data=0x106c00100fc0, temp_zone=0x106c0003ee80, linkage=0x106c001bba48) at ../../src/compiler/turboshaft/maglev-graph-building-phase.cc:6131
#35 0x0000555558b62567 in _ZN2v88internal8compiler10turboshaft8Pipeline3RunITkNS2_15TurboshaftPhaseENS2_24MaglevGraphBuildingPhaseEJRPNS1_7LinkageEEEEDaDpOT0_ (this=this@entry=0x7fffffffc1c8, args=@0x7fffffffc148: 0x106c001bba48) at ../../src/compiler/turboshaft/pipelines.h:88
#36 0x0000555558b52eb0 in v8::internal::compiler::turboshaft::Pipeline::CreateGraphWithMaglev (this=this@entry=0x7fffffffc1c8, linkage=0x106c001bba48) at ../../src/compiler/turboshaft/pipelines.h:138
#37 0x0000555558b52cd7 in v8::internal::compiler::PipelineCompilationJob::ExecuteJobImpl (this=0x106c00100c00, stats=<optimized out>, local_isolate=<optimized out>) at ../../src/compiler/pipeline.cc:770
#38 0x0000555557394d3f in v8::internal::OptimizedCompilationJob::ExecuteJob (this=this@entry=0x106c00100c00, stats=0x106c000f2628, local_isolate=0x106c00138000) at ../../src/codegen/compiler.cc:470
#39 0x00005555573a3d04 in v8::internal::(anonymous namespace)::CompileTurbofan_NotConcurrent (isolate=0x106c000d0000, job=0x106c00100c00) at ../../src/codegen/compiler.cc:1103
#40 v8::internal::(anonymous namespace)::CompileTurbofan (isolate=0x106c000d0000, function=..., shared=..., mode=v8::internal::ConcurrencyMode::kSynchronous, osr_offset=..., result_behavior=v8::internal::(anonymous namespace)::CompileResultBehavior::kDefault) at ../../src/codegen/compiler.cc:1248
#41 v8::internal::(anonymous namespace)::GetOrCompileOptimized (isolate=isolate@entry=0x106c000d0000, function=function@entry=..., mode=v8::internal::ConcurrencyMode::kSynchronous, code_kind=code_kind@entry=v8::internal::CodeKind::TURBOFAN_JS, osr_offset=osr_offset@entry=..., result_behavior=result_behavior@entry=v8::internal::(anonymous namespace)::CompileResultBehavior::kDefault) at ../../src/codegen/compiler.cc:1416
#42 0x00005555573a618c in v8::internal::Compiler::CompileOptimized (isolate=0x106c000d0000, function=..., mode=v8::internal::ConcurrencyMode::kSynchronous, code_kind=<optimized out>) at ../../src/codegen/compiler.cc:3197
#43 0x0000555557e8d1ae in v8::internal::(anonymous namespace)::CompileOptimized (function=function@entry=..., mode=mode@entry=v8::internal::ConcurrencyMode::kSynchronous, target_kind=target_kind@entry=v8::internal::CodeKind::TURBOFAN_JS, isolate=isolate@entry=0x106c000d0000) at ../../src/runtime/runtime-compiler.cc:185
#44 0x0000555557e870c5 in v8::internal::__RT_impl_Runtime_OptimizeTurbofanEager (args=..., isolate=isolate@entry=0x106c000d0000) at ../../src/runtime/runtime-compiler.cc:227
#45 0x0000555557e86d10 in v8::internal::Runtime_OptimizeTurbofanEager (args_length=<optimized out>, args_object=0x7fffffffc590, isolate=0x106c000d0000) at ../../src/runtime/runtime-compiler.cc:222
#46 0x00005555595f813d in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit ()
#47 0x00005555594c05f3 in Builtins_OptimizeTurbofanEager ()
#48 0x00005555594be863 in Builtins_InterpreterEntryTrampoline ()
#49 0x000035da00081b15 in ?? ()
#50 0x000035da00000011 in ?? ()
#51 0x000035da00000011 in ?? ()
#52 0x0000000000000002 in ?? ()
#53 0x0000000000000002 in ?? ()
#54 0x000035da00249101 in ?? ()
#55 0x000035da00249101 in ?? ()
#56 0x000035da00082405 in ?? ()
#57 0x0000000000000000 in ?? ()

```

Reporter credit: Changheon Lee

## Attachments

- deleted (application/octet-stream, 0 B)
- [poc.js](attachments/poc.js) (text/javascript, 424 B)

## Timeline

### da...@gmail.com (2025-04-19)

`dcheck_always_on = true` seems to be required.

### cl...@appspot.gserviceaccount.com (2025-04-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4789736853929984.

### 24...@project.gserviceaccount.com (2025-04-21)

Detailed Report: https://clusterfuzz.com/testcase?key=4789736853929984

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: Unreachable code
Crash Address: 
Crash State:
  operations.cc
  v8::internal::compiler::turboshaft::ValidateOpInputRep
  v8::internal::compiler::turboshaft::ValidateOpInputRep
  v8::internal::compiler::turboshaft::PhiOp& v8::internal::compiler::turboshaft::O
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=99153:99154

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4789736853929984

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### 24...@project.gserviceaccount.com (2025-04-21)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### ch...@google.com (2025-04-21)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-04-21)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### cf...@google.com (2025-04-24)

victorgomes@ could you PTAL?  

ClusterFuzz claims this only impacts Beta while the commit this bisects to is already in Stable.  

I wonder if that is because this is only reachable through turbolev?

### da...@gmail.com (2025-04-28)

victorgomes@ Could you PTAL on this issue?

This problem was reported on April 19, and although this problem still occurs in the HEAD commit of the Main branch, I am somewhat concerned that the related discussion will be delayed.

### vi...@chromium.org (2025-04-30)

This issue only reproduces with the experimental flag --turbolev. This is not a vulnerability.

### dm...@chromium.org (2025-05-21)

--turbolev isn't experimental anymore ==> this counts as a vulnerability, but with impact=none since Turbolev doesn't ship anywhere.

### dm...@chromium.org (2025-05-21)

(and this bug can lead to interpreting a Smi as a Tagged value ==> should lead to arbitrary reads in the sandbox (which I think also gives arbitrary writes within the sandbox), so type=Vulnerability rather than Bug indeed)
(but once again, impact=none because Turbolev doesn't ship anywhere)

### dx...@google.com (2025-05-22)

Project: v8/v8  

Branch: main  

Author: Darius Mercadier [dmercadier@chromium.org](mailto:dmercadier@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6573553>

[turbolev] Unwrap Identity nodes before tagging for exception phis

---


Expand for full commit details
```
     
    Because the ValueRepresentation of Identity nodes in Maglev is Tagged, 
    which was tricking the Turbolev graph building in believing that they 
    didn't need to be retagged for exception phis. 
     
    Fixed: 411802156 
    Change-Id: Iccabfb031b4d023a4d7ac31ea07a3afe8defaf12 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6573553 
    Reviewed-by: Victor Gomes <victorgomes@chromium.org> 
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org> 
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#100413}

```

---

Files:

- M `src/compiler/turboshaft/turbolev-graph-builder.cc`
- A `test/mjsunit/turbolev/regress-411802156.js`

---

Hash: 36debe3a9abe6c78eb2e4fc470bf1c0226eb4924  

Date:  Wed May 21 08:21:56 2025


---

### dx...@google.com (2025-05-22)

Project: v8/v8  

Branch: main  

Author: Darius Mercadier [dmercadier@chromium.org](mailto:dmercadier@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6578316>

[maglev] Add DCHECK to ensure that Identity nodes are in exception phis

---


Expand for full commit details
```
     
    We recently had this issue in Turbolev (https://crrev.com/c/6573553), 
    which shouldn't be an issue in Maglev, but let's add a DCHECK just in 
    case. 
     
    Bug: 411802156 
    Change-Id: I4f3348561f8ca19a0b5cbc3b5125026880f0e05b 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6578316 
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org> 
    Commit-Queue: Victor Gomes <victorgomes@chromium.org> 
    Reviewed-by: Victor Gomes <victorgomes@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#100435}

```

---

Files:

- M `src/maglev/maglev-code-generator.cc`

---

Hash: 8943c6f9223d7320dfae8c6332d6f8f41df91680  

Date:  Thu May 22 12:22:42 2025


---

### 24...@project.gserviceaccount.com (2025-05-23)

ClusterFuzz testcase 4789736853929984 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=100412:100413

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### sp...@google.com (2025-05-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
report of memory corruption in a sandboxed process / renderer 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-05-29)

Thank you for your efforts and reporting this issue to us!

### pg...@google.com (2025-06-23)

(Updating OSes as I don't see why this would only impact Linux!)

### ch...@google.com (2025-08-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/411802156)*
