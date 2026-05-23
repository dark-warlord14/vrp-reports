# Security: Debug check failed: pred_reverse_index != -1 (-1 vs. -1)

| Field | Value |
|-------|-------|
| **Issue ID** | [40062717](https://issues.chromium.org/issues/40062717) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | Blink>JavaScript>Compiler>Turbofan |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | wh...@gmail.com |
| **Assignee** | ms...@chromium.org |
| **Created** | 2023-01-18 |
| **Bounty** | $7,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**  

v8 current HEAD

PoC  

function main() {  

for (const v1 in "0Ohlah") {  

let v2 = 0;  

do {  

const v3 = --v2;  

const v5 = "-4294967297".**proto**;  

const v6 = v5.codePointAt();  

} while (v2 > v2);  

for (let v7 = 0; v7 < 3818; v7++) {  

}  

}  

}  

main();

# 

# Fatal error in ../../src/compiler/turboshaft/graph.h, line 326

# Debug check failed: pred\_reverse\_index != -1 (-1 vs. -1).

# 

# 

# 

#FailureMessage Object: 0x7fff43580f68  

==== C stack trace ===============================

```
/home/uuu/v8_src.main/v8/out/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1e) [0x7fab87b1b1de]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8_libplatform.so(+0x4b2bd) [0x7fab87a6f2bd]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8_libbase.so(V8_Fatal(char const\*, int, char const\*, ...)+0x1ac) [0x7fab87ae95dc]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8_libbase.so(+0x5802c) [0x7fab87ae902c]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8_libbase.so(V8_Dcheck(char const\*, int, char const\*)+0x27) [0x7fab87ae9697]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::Block::GetPredecessorIndex(v8::internal::compiler::turboshaft::Block const\*) const+0x153) [0x7fab8cd97493]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducerSignallingNanImpossible, v8::internal::compiler::turboshaft::ValueNumberingReducer>>::CloneAndInlineBlock(v8::internal::compiler::turboshaft::Block const\*, bool)+0x72) [0x7fab8cdf8de2]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::BranchEliminationReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducerSignallingNanImpossible, v8::internal::compiler::turboshaft::ValueNumberingReducer>, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducerSignallingNanImpossible, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::ReducerBase>>::ReduceGoto(v8::internal::compiler::turboshaft::Block\*)+0x1ba) [0x7fab8cdf723a]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::AssemblerOpInterface<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducerSignallingNanImpossible, v8::internal::compiler::turboshaft::ValueNumberingReducer>>::Goto(v8::internal::compiler::turboshaft::Block\*)+0x2c) [0x7fab8cdf4a8c]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::BranchEliminationReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducerSignallingNanImpossible, v8::internal::compiler::turboshaft::ValueNumberingReducer>, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducerSignallingNanImpossible, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::ReducerBase>>::ReduceBranch(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::Block\*, v8::internal::compiler::turboshaft::Block\*, v8::internal::BranchHint)+0x2c4) [0x7fab8cdf6dd4]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducerSignallingNanImpossible, v8::internal::compiler::turboshaft::ValueNumberingReducer>>::VisitBranch(v8::internal::compiler::turboshaft::BranchOp const&)+0x19e) [0x7fab8cde698e]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(bool v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducerSignallingNanImpossible, v8::internal::compiler::turboshaft::ValueNumberingReducer>>::VisitOp<false>(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::Block const\*)+0x13aa) [0x7fab8cdfa95a]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducerSignallingNanImpossible, v8::internal::compiler::turboshaft::ValueNumberingReducer>>::VisitBlock<false>(v8::internal::compiler::turboshaft::Block const\*)+0x374) [0x7fab8ce0dbe4]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducerSignallingNanImpossible, v8::internal::compiler::turboshaft::ValueNumberingReducer>>::VisitAllBlocks<false>()+0xeb) [0x7fab8ce0d7db]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducerSignallingNanImpossible, v8::internal::compiler::turboshaft::ValueNumberingReducer>>::VisitGraph<false>()+0x375) [0x7fab8cddace5]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::OptimizationPhaseImpl<v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducerSignallingNanImpossible, v8::internal::compiler::turboshaft::ValueNumberingReducer>::Run(v8::internal::compiler::turboshaft::Graph\*, v8::internal::Zone\*, v8::internal::compiler::NodeOriginTable\*, std::Cr::tuple<> const&)+0xcc) [0x7fab8cd1212c]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::OptimizationPhase<v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducerSignallingNanImpossible, v8::internal::compiler::turboshaft::ValueNumberingReducer>::Run(v8::internal::Isolate\*, v8::internal::compiler::turboshaft::Graph\*, v8::internal::Zone\*, v8::internal::compiler::NodeOriginTable\*, std::Cr::tuple<> const&)+0x90) [0x7fab8cd11e50]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::LateOptimizationPhase::Run(v8::internal::compiler::PipelineData\*, v8::internal::Zone\*)+0xaa) [0x7fab8cd1176a]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(auto v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::LateOptimizationPhase>()+0xae) [0x7fab8cd02a0e]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::PipelineImpl::OptimizeGraph(v8::internal::compiler::Linkage\*)+0x629) [0x7fab8ccf5099]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::PipelineCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats\*, v8::internal::LocalIsolate\*)+0xe3) [0x7fab8ccf4803]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats\*, v8::internal::LocalIsolate\*)+0x14c) [0x7fab8ad76a0c]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(+0x325ed14) [0x7fab8ad8ed14]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(+0x325db35) [0x7fab8ad8db35]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(+0x324fd50) [0x7fab8ad7fd50]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::Compiler::CompileOptimizedOSR(v8::internal::Isolate\*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::BytecodeOffset, v8::internal::ConcurrencyMode)+0x211) [0x7fab8ad864a1]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(+0x40dfe76) [0x7fab8bc0fe76]

```

## Timeline

### wh...@gmail.com (2023-01-18)

run d8 with 
--assert-types --turboshaft

### [Deleted User] (2023-01-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-01-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4857078400352256.

### bo...@google.com (2023-01-19)

Confirming repro on Linux at today's tip of tree, but not 111.0.5532.2. Sending to ClusterFuzz for bisection. 

Severity high because implied memory corruption within renderer sandbox on non-debug builds. 

Impact none due to requirement for non-standard flags. 

[Monorail components: Blink>JavaScript>Compiler>Turbofan]

### cl...@chromium.org (2023-01-19)

Detailed Report: https://clusterfuzz.com/testcase?key=4857078400352256

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  pred_reverse_index != -1 in graph.h
  v8::internal::compiler::turboshaft::Block::GetPredecessorIndex
  v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turbosh
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=84736:84737

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4857078400352256

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### [Deleted User] (2023-01-21)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-21)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-21)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jg...@chromium.org (2023-01-23)

Reassigning since the backtrace points into Turboshaft.

### te...@chromium.org (2023-01-23)

Turboshaft is not yet shipping and won't be shipping for some more months. So this this has no security impact for now. Assigning to Maya based on the regression range.

### ms...@chromium.org (2023-01-23)

The DCHECK only triggers when --turboshaft is enabled, which won't be on by default in the coming months, so reclassifying again.

### gi...@appspot.gserviceaccount.com (2023-01-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/930b17be777336510374ee873a40d043dcd9b172

commit 930b17be777336510374ee873a40d043dcd9b172
Author: Maya Lekova <mslekova@chromium.org>
Date: Wed Jan 25 13:46:27 2023

[turboshaft] Fix a crash in BranchEliminationReducer

This CL allows GetPredecessorIndex gracefully fail when an indirect
predecessor of the current block is passed as an argument.

Bug: chromium:1408354
Change-Id: I5eaab6c6905839e5833faea5c4b0540e4a63699b
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4191773
Commit-Queue: Maya Lekova <mslekova@chromium.org>
Reviewed-by: Tobias Tebbi <tebbi@chromium.org>
Cr-Commit-Position: refs/heads/main@{#85478}

[modify] https://crrev.com/930b17be777336510374ee873a40d043dcd9b172/src/compiler/turboshaft/graph.h


### ms...@chromium.org (2023-01-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-01-26)

ClusterFuzz testcase 4857078400352256 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=85477:85478

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-01-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-27)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-03)

Congratulations again! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-02-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-05-05)

This issue was migrated from crbug.com/chromium/1408354?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062717)*
