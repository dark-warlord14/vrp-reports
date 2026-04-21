# DCHECK Fail when Maglev Generates Exception Handler Trampoline Instructions

| Field | Value |
|-------|-------|
| **Issue ID** | [457351015](https://issues.chromium.org/issues/457351015) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ol...@chromium.org |
| **Created** | 2025-11-03 |
| **Bounty** | $10,000.00 |

## Description

VULNERABILITY DETAILS

I am still analyzing this PoC and have not yet identified the root cause. I can only explain the reason for the crash.

This crash is related to the Maglev register allocation process. The relevant Maglev graph is as follows:

```
After register allocation
Graph
    ....
│╭───►Block b2 (effects: ua)
││      32/35: φᵀ r1 (n33, n85) (compressed) → [rax|R|t] (spilled: [stack:15|t]), live range: [32-66]
││      33/36: φᵀ r5 (n32, n89) (decompressed) → [rdx|R|t] (spilled: [stack:7|t]), live range: [33-60]
││         98: GapMove([rdx|R|t] → [rbx|R|t])
││     79 : TestLessThan r5, [14]
││             ↱ eager @79 (11 live vars)
││      34/38: CheckedSmiUntag [v33/n36:[rdx|R|t]] → [rdx|R|w32] (spilled: [stack:1|w32]), live range: [34-60]
││         99: ConstantGapMove(n39 → [rsi|R|w32])
││     82 : JumpIfFalse [81]
││╭─────35/41: BranchIfInt32Compare(LessThan) [v34/n38:[rdx|R|w32], v13/n39:[rsi|R|w32]] b3 b9
│││         ↓
│││   Block b3    /*=== k[9] = k; ===*/
|||        ...
│││  0x09b1008384b1 <SharedFunctionInfo> (0x09b100848915 <String[8]: "./poc.js">:5:21)
│││    93 : SetKeyedProperty r5, r17, [15]
│││     36/44: 🐢 CallBuiltin(KeyedStoreIC_Megamorphic) [v33/n36:[rdx|R|t], v9/n43:[rcx|R|t], v33/n36:[rax|R|t], v16/n2:[rsi|R|t]] → [rax|R|t]
│││            ↳ lazy @93 (11 live vars)
│││            ↳ throw @126 (b7) : {<this>:n1, <context>:n2, r1:n35, r4:n26, r5:n36, r7:n11, r8:n12, r10:n14, r13:n17, r14:n18}

....        /*=== for (let m = 0; m<10; m++) { } ===*/

│││ ╰►Block b6    /*=== undefined(); ===*/
│││       108: ConstantGapMove(n33 → [rdi|R|t])
│││       109: GapMove([stack:-3|t] → [rsi|R|t])
│││  0x09b1008384b1 <SharedFunctionInfo> (0x09b100848915 <String[8]: "./poc.js">:8:16)
│││   120 : CallUndefinedReceiver0 r16, [20]
│││     44/62: 🐢 Call(NULL_OR_UNDEFINED, Any) [v4/n33:[rdi|R|t], v16/n2:[rsi|R|t], v4/n33:[rdi|R|t]] → [rax|R|t], live range: [44-45]
│││            ↳ lazy @120 (11 live vars)
│││            ↳ throw @126 (b7) : {<this>:n1, <context>:n2, r1:n33, r4:n26, r5:n36, r7:n11, r8:n12, r10:n14, r13:n17, r14:n18}
│││   124 : Jump [30]
│││╭────45/63: Jump b8
││││           with gap moves:
││││             - v44/n62:[rax|R|t] → 85: φᵀ r1 [rax|R|t]
││││           with register merges:
││││ 
││││  Block b7 (exception handler)    /*=== catch(exception) { ... } ===*/
││││    46/64: φᵀₑ <accumulator> (compressed) → [rax|R|t], live range: [46-54]
││││    47/65: φᵀₑ r1 (compressed) → [rcx|R|t] (spilled: [stack:14|t]), live range: [47-57]
....

```

In the PoC, there are two nodes that may throw exceptions, and the exceptions thrown by both will be handled by `Block b7 (exception handler)`.

1. `36/44: CallBuiltin(...)`. If an exception is thrown from here, the value of `r1` will be `n35`.
2. `44/62: Call(...)`. If an exception is thrown from here, the value of `r1` will be `n33`.

Since the value of `r1` differs in the two paths, an exception phi node `47/65: φᵀₑ r1` is additionally added in `Block b7`.

The crash occurs during the Maglev assembly process. According to the comments in the `ExceptionHandlerTrampolineBuilder::EmitTrampolineFor()` method, when handling exception phis, the `NewHeapNumber` builtin may be called to create a `HeapNumber` object for float64, which may overwrite registers. Therefore, it is required that the source of every exception phi must be spilled to the stack during processing.

However, when `ExceptionHandlerTrampolineBuilder` processes the `36/44: CallBuiltin` node, `n35` is the source of the exception phi node, but `n35` is not spilled to the stack. Instead, it is simultaneously located in `[rax|R|t]` and `(spilled: [stack:15|t])`, causing the DCHECK to fail.

In the release version, `ExceptionHandlerTrampolineBuilder` directly loads the value from `rax`, which is unsafe because the `NewHeapNumber` builtin may overwrite the value in `rax` at any time.

As I continued to study the Maglev register allocation process, I found:

- When `StraightForwardRegisterAllocator::AllocateNode()` processes the `36/44: CallBuiltin(...)` node, it correctly calls `SpillAndClearRegisters()` to spill all registers to the stack. Therefore, the location information of the `32/35: φᵀ r1 (n33, n85)` node is `(spilled: [stack:15|t])`.
- However, when processing `Block b9`, `InitializeRegisterValues()` is called to reload the `32/35: φᵀ r1 (n33, n85)` node into `rax`. This results in the location information (i.e., `regalloc_info`) of the node being `[rax|R|t] (spilled: [stack:15|t])`.

```
│││   Block b3
│││   live regs: rax=v32, rcx=v1, rdx=v34, rbx=v33, rsi=v13
│││   [holes: 45-59 63↰]
.....
│││   Using n2...
│││     clearing registers with n36      /* <=== Spill and Clean */
│││     spill: [stack:7|t] ← n36  
│││     clearing registers with n43
│││     clearing registers with n2
│││     clearing registers with n38
│││     spill: [stack:1|w32] ← n38
│││     clearing registers with n35
│││     spill: [stack:15|t] ← n35
│││   Allocating result...
│││     forcing rax to n44...
│││   Allocating lazy deopt inputs...
│││   Using n3...
│││   Using n1...
│││   Using n2...
│││   Using n35...
│││   Using n26...
│││   Using n36...
│││   Using n11...
│││   Using n12...
│││   Using n14...
│││   Using n17...
│││   Using n18...
│││   Using n2...
│││  0x09b1008384b1 <SharedFunctionInfo> (0x09b100848915 <String[8]: "./poc.js">:5:21)
│││    93 : SetKeyedProperty r5, r17, [15]
│││     44: 🐢 CallBuiltin(KeyedStoreIC_Megamorphic) [n36, n43, n36, n2], 0 uses, but required
│││         ↳ lazy @93 (11 live vars)
│││         ↳ throw @126 (b7) : {<this>:n1, <context>:n2, r1:n35, r4:n26, r5:n36, r7:n11, r8:n12, r10:n14, r13:n17, r14:n18}
....
│ ╰──►Block b9
│     live regs: rax=v32, rcx=v1, rsi=v13    /* Force Load */

```

`RecordMoves()` retrieves the location information of the node from `source->regalloc_info()->allocation()`. If a node's value is simultaneously in a register and on the stack, `allocation()` will choose to load the value from the register.

```
class RegallocValueNodeInfo : public RegallocNodeInfo {
  ...
  compiler::InstructionOperand allocation() const {
    if (has_register()) {
      return compiler::AllocatedOperand(compiler::LocationOperand::REGISTER,
                                        representation_, FirstRegisterCode());
    }
    CHECK(is_loadable());
    return loadable_slot();
  }
  ...
}

```

That is all I know so far. I cannot determine the root cause of this crash. I believe you have a better understanding of Maglev than I do, so I report it to you.

REPRODUCTION CASE

poc.js:

```
let arr = [1, 2, 3];
for (const i of arr) {
    for (let j = 0; j < 50, true; j++) {
        for (let k = 0; k < 5; k++) {
            try {
                k[9] = k;
                for (let m = 0; m<10; m++) {
                }
                undefined();   
            } catch(exception) {
                print(exception);
            }
        }
    }
}

```

V8 must be built with a debug configuration, Execute v8 as follows:

```
./d8 \
    --predictable \
    --jit-fuzzing \
    ./poc.js

```

This will result in the following crash:

```
#
# Fatal error in ../../src/maglev/maglev-code-generator.cc, line 623
# Debug check failed: !source->regalloc_info()->allocation().IsRegister().
#

```

CREDIT INFORMATION

Reporter credit: [303f06e3]

## Timeline

### cl...@appspot.gserviceaccount.com (2025-11-03)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4650717113417728.

### 24...@project.gserviceaccount.com (2025-11-03)

Detailed Report: https://clusterfuzz.com/testcase?key=4650717113417728

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  !source->regalloc_info()->allocation().IsRegister() in maglev-code-generator.cc
  v8::internal::maglev::MaglevCodeGenerator::EmitExceptionHandlerTrampolines
  v8::internal::maglev::MaglevCodeGenerator::EmitCode
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=99811:99812

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4650717113417728

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### 24...@project.gserviceaccount.com (2025-11-03)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/56f9ec26f228aea249900dfe4bcb9cb664a3c8d8 ([maglev] TryOnStackReplacement only has a deferred call

Fixed: 410818019

Change-Id: Ia40a54000a7be11bd345b90707551d1a4be5acf2
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6448399
Auto-Submit: Olivier Flückiger <olivf@chromium.org>
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Commit-Queue: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/heads/main@{#99812}
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### ch...@google.com (2025-11-04)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### dx...@google.com (2025-11-05)

Project: v8/v8  

Branch:  main  

Author:  Olivier Flückiger [olivf@chromium.org](mailto:olivf@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7119379>

[maglev] Fix left over register allocations from regalloc

---


Expand for full commit details
```
     
    The regalloc should clear the node allocations when it is done. 
    Failing to do so can cause the codegen to use stale register state. 
    In this concrete example the exception handler trampolines would not 
    load from the spill slot due to the left over allocation. 
     
    Bug: 457351015 
    Change-Id: Ia113c0b3373b5b11250e11d66d63b6a67b63b13f 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7119379 
    Auto-Submit: Olivier Flückiger <olivf@chromium.org> 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#103535}

```

---

Files:

- M `src/maglev/maglev-code-generator.cc`
- M `src/maglev/maglev-regalloc.cc`
- M `src/maglev/maglev-regalloc.h`

---

Hash: [7ef5ae531a9e79a084b5f0bebd5496d5d481e0ea](https://chromiumdash.appspot.com/commit/7ef5ae531a9e79a084b5f0bebd5496d5d481e0ea)  

Date: Wed Nov 5 13:11:51 2025


---

### 24...@project.gserviceaccount.com (2025-11-06)

ClusterFuzz testcase 4650717113417728 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=103534:103535

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2025-11-06)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches (as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels. Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security>
  After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ma...@google.com (2025-11-07)

olivf@, could you comment on the security impact of this bug?

### ol...@chromium.org (2025-11-07)

I can see this being a memory corruption issue. We should back-merge the fix.

### ch...@google.com (2025-11-07)

Merge review required: M143 is already shipping to beta.

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
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2025-11-07)

Merge review required: M142 is already shipping to stable.

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
Owners: andywu (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ol...@chromium.org (2025-11-07)

1. v8 security fix
2. <https://chromium-review.googlesource.com/c/v8/v8/+/7119379>
3. y
   4-6. no

### ol...@chromium.org (2025-11-07)

@hughfreeman1998 thanks for the report. The issue was a temporary register allocation from the regalloc phase leaking into the codegen phase. The value was supposed to be loaded from a spill slot in the exception case, however it was loaded from a (at that point) stale register.

### hu...@gmail.com (2025-11-07)

Thank you for your reply. The register allocation error is an interesting issue. I feel that this vulnerability is likely exploitable. I am still researching this issue and will keep you updated on any progress.

### ch...@google.com (2025-11-07)

Setting milestone because of s0/s1 severity.

### dx...@google.com (2025-11-10)

Project: v8/v8  

Branch:  refs/branch-heads/14.2  

Author:  Olivier Flückiger [olivf@chromium.org](mailto:olivf@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7137280>

Merged: [maglev] Fix left over register allocations from regalloc

---


Expand for full commit details
```
     
    The regalloc should clear the node allocations when it is done. 
    Failing to do so can cause the codegen to use stale register state. 
    In this concrete example the exception handler trampolines would not 
    load from the spill slot due to the left over allocation. 
     
    Bug: 457351015 
    (cherry picked from commit 7ef5ae531a9e79a084b5f0bebd5496d5d481e0ea) 
     
    Change-Id: Ibf50e9c77f68654abf1b610bc1f37ccd17904c84 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7137280 
    Reviewed-by: Victor Gomes <victorgomes@chromium.org> 
    Commit-Queue: Victor Gomes <victorgomes@chromium.org> 
    Auto-Submit: Olivier Flückiger <olivf@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.2@{#35} 
    Cr-Branched-From: 37f82dbb9f640dc5eea09870dd391cd3712546e5-refs/heads/14.2.231@{#1} 
    Cr-Branched-From: d1a6089b861336cf4b3887edfd3fdd280b23b5dd-refs/heads/main@{#102804}

```

---

Files:

- M `src/maglev/maglev-code-generator.cc`
- M `src/maglev/maglev-regalloc.cc`
- M `src/maglev/maglev-regalloc.h`

---

Hash: [9fcb46c0af03be16e200c2b7b0e6ef7f9b9aab1f](https://chromiumdash.appspot.com/commit/9fcb46c0af03be16e200c2b7b0e6ef7f9b9aab1f)  

Date: Wed Nov 5 13:11:51 2025


---

### dx...@google.com (2025-11-10)

Project: v8/v8  

Branch:  refs/branch-heads/14.3  

Author:  Olivier Flückiger [olivf@chromium.org](mailto:olivf@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7137279>

Merged: [maglev] Fix left over register allocations from regalloc

---


Expand for full commit details
```
     
    The regalloc should clear the node allocations when it is done. 
    Failing to do so can cause the codegen to use stale register state. 
    In this concrete example the exception handler trampolines would not 
    load from the spill slot due to the left over allocation. 
     
    Bug: 457351015 
    (cherry picked from commit 7ef5ae531a9e79a084b5f0bebd5496d5d481e0ea) 
     
    Change-Id: I4d98362923bda183a7adb446a72a33dee1c29dd8 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7137279 
    Reviewed-by: Victor Gomes <victorgomes@chromium.org> 
    Commit-Queue: Victor Gomes <victorgomes@chromium.org> 
    Auto-Submit: Olivier Flückiger <olivf@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.3@{#12} 
    Cr-Branched-From: 13c7e3135187c1b0c7344e42529fbc27ba0e47f1-refs/heads/14.3.127@{#1} 
    Cr-Branched-From: 01af089bd89645143fc60f0da72267f95645afb3-refs/heads/main@{#103352}

```

---

Files:

- M `src/maglev/maglev-code-generator.cc`
- M `src/maglev/maglev-regalloc.cc`
- M `src/maglev/maglev-regalloc.h`

---

Hash: [a20ede8226308b9c0d5efc975c2a486cf5231af7](https://chromiumdash.appspot.com/commit/a20ede8226308b9c0d5efc975c2a486cf5231af7)  

Date: Wed Nov 5 13:11:51 2025


---

### go...@google.com (2025-11-10)

This already merged to M142 and M143 at #17 and #18, Anything pending here?

### ol...@chromium.org (2025-11-10)

All good

### pe...@google.com (2025-11-10)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### sp...@google.com (2025-11-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
high quality memory corruption in sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2025-11-21)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### rz...@google.com (2025-11-21)

1. Just <https://crrev.com/c/7176667>
2. Low, just a simple conflict
3. 142, 143
4. Yes

### an...@google.com (2025-12-04)

Approved for M138

### dx...@google.com (2025-12-10)

Project: v8/v8  

Branch:  refs/branch-heads/13.8  

Author:  Olivier Flückiger [olivf@chromium.org](mailto:olivf@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7176667>

[M138-LTS][maglev] Fix left over register allocations from regalloc

---


Expand for full commit details
```
     
    M138 merge issues: 
     
    src/maglev/maglev-code-generator.cc: 
      in MaglevCodeGeneratingNodeProcessor::Process(): 
      regalloc_info() doesn't exist in M138, called it directly using 
      the node object: 
    -      DCHECK(!node->regalloc_info()->has_register()); 
    +      DCHECK(!node->has_register()); 
     
    The regalloc should clear the node allocations when it is done. 
    Failing to do so can cause the codegen to use stale register state. 
    In this concrete example the exception handler trampolines would not 
    load from the spill slot due to the left over allocation. 
     
    (cherry picked from commit 7ef5ae531a9e79a084b5f0bebd5496d5d481e0ea) 
     
    Bug: 457351015 
    Change-Id: Ia113c0b3373b5b11250e11d66d63b6a67b63b13f 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7119379 
    Auto-Submit: Olivier Flückiger <olivf@chromium.org> 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#103535} 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7176667 
    Reviewed-by: Olivier Flückiger <olivf@chromium.org> 
    Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com> 
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
    Reviewed-by: Toon Verwaest <verwaest@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/13.8@{#84} 
    Cr-Branched-From: 61ddd471ece346840bbebbb308dceb4b4ce31b28-refs/heads/13.8.258@{#1} 
    Cr-Branched-From: fdb5de2c741658e94944f2ec1218530e98601c23-refs/heads/main@{#100480}

```

---

Files:

- M `src/maglev/maglev-code-generator.cc`
- M `src/maglev/maglev-regalloc.cc`
- M `src/maglev/maglev-regalloc.h`

---

Hash: [ddc4473ba62a0c14777e1d911f91cce285029adb](https://chromiumdash.appspot.com/commit/ddc4473ba62a0c14777e1d911f91cce285029adb)  

Date: Wed Nov 5 13:11:51 2025


---

### ch...@google.com (2026-02-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> high quality memory corruption in sandboxed process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/457351015)*
