# Security: Debug check failed: begin.valid().

| Field | Value |
|-------|-------|
| **Issue ID** | [40062647](https://issues.chromium.org/issues/40062647) |
| **Status** | Fixed |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Linux, Mac, Windows |
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

for (const v1 in "xRPrf") {  

for (let v2 = 0; v2 < 3818; v2++) {  

for (let v4 = 0; v4 < v2; v4 = v4 >>> v2) {  

}  

}  

}  

}  

main();

# 

# Fatal error in ../../src/compiler/turboshaft/graph.h, line 746

# Debug check failed: begin.valid().

# 

# 

# 

#FailureMessage Object: 0x7ffd8c119538  

==== C stack trace ===============================

```
/home/uuu/v8_src.main/v8/out/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1e) [0x7f54fb96a1de]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8_libplatform.so(+0x4b2bd) [0x7f54fb8be2bd]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8_libbase.so(V8_Fatal(char const\*, int, char const\*, ...)+0x1ac) [0x7f54fb9385dc]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8_libbase.so(+0x5802c) [0x7f54fb93802c]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8_libbase.so(V8_Dcheck(char const\*, int, char const\*)+0x27) [0x7f54fb938697]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::Graph::operations(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::OpIndex)+0x56) [0x7f5500acb626]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::Graph::operations(v8::internal::compiler::turboshaft::Block const&)+0x3a) [0x7f5500ad200a]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::Graph::TurnLoopIntoMerge(v8::internal::compiler::turboshaft::Block\*)+0x113) [0x7f5500a9ffa3]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::DeadCodeEliminationReducer>>::VisitBlock<false>(v8::internal::compiler::turboshaft::Block const\*)+0x239) [0x7f5500c6e379]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::DeadCodeEliminationReducer>>::VisitAllBlocks<false>()+0xeb) [0x7f5500c6e0ab]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::DeadCodeEliminationReducer>>::VisitGraph<false>()+0x375) [0x7f5500c61665]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::OptimizationPhaseImpl<v8::internal::compiler::turboshaft::DeadCodeEliminationReducer>::Run(v8::internal::compiler::turboshaft::Graph\*, v8::internal::Zone\*, v8::internal::compiler::NodeOriginTable\*, std::Cr::tuple<> const&)+0xa4) [0x7f5500c455f4]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::OptimizationPhase<v8::internal::compiler::turboshaft::DeadCodeEliminationReducer>::Run(v8::internal::Isolate\*, v8::internal::compiler::turboshaft::Graph\*, v8::internal::Zone\*, v8::internal::compiler::NodeOriginTable\*, std::Cr::tuple<> const&)+0x90) [0x7f5500c45400]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::TurboshaftDeadCodeEliminationPhase::Run(v8::internal::compiler::PipelineData\*, v8::internal::Zone\*)+0x90) [0x7f5500c45360]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(auto v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::TurboshaftDeadCodeEliminationPhase>()+0xae) [0x7f5500a7f18e]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::PipelineImpl::OptimizeGraph(v8::internal::compiler::Linkage\*)+0x6ff) [0x7f5500a70faf]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::PipelineCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats\*, v8::internal::LocalIsolate\*)+0xe3) [0x7f5500a70643]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats\*, v8::internal::LocalIsolate\*)+0x14c) [0x7f54feaf84ec]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(+0x31917f4) [0x7f54feb107f4]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(+0x3190615) [0x7f54feb0f615]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(+0x3182830) [0x7f54feb01830]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::Compiler::CompileOptimizedOSR(v8::internal::Isolate\*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::BytecodeOffset, v8::internal::ConcurrencyMode)+0x211) [0x7f54feb07f81]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(+0x400f736) [0x7f54ff98e736]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(+0x400cbb9) [0x7f54ff98bbb9]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::Runtime_CompileOptimizedOSR(int, unsigned long\*, v8::internal::Isolate\*)+0x128) [0x7f54ff98b7e8]  
[0x7f547f96b7bf]

```

## Timeline

### [Deleted User] (2023-01-14)

[Empty comment from Monorail migration]

### wh...@gmail.com (2023-01-14)

ok, please using this flag, 
--assert-types --turboshaft-assert-types --turboshaft --always-turbofan

### cl...@chromium.org (2023-01-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5078652114108416.

### cl...@chromium.org (2023-01-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-01-17)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript]

### cl...@chromium.org (2023-01-17)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/88eac4b870dc9becb11fdaa2e71ed60ceab44a60 ([turboshaft] Basic TypedOptimization and new DeadCodeElimination).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2023-01-17)

Detailed Report: https://clusterfuzz.com/testcase?key=5078652114108416

Fuzzer: None
Job Type: linux_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  begin.valid() in graph.h
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_d8_dbg&range=85142:85143

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5078652114108416

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### bo...@google.com (2023-01-18)

Setting security impact to none since reaching this bug requires non-standard flags.

@wh0tlif3 - if you're aware of a way to trigger the bug without the flags listed in https://crbug.com/chromium/1407342#c2 then please let us know.

Setting severity high on the basis that reaching this DCHECK in release builds could be abused to achieve remote code execution in the sandboxed renderer process. 

### bo...@google.com (2023-01-18)

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


### cl...@chromium.org (2023-01-26)

ClusterFuzz testcase 5078652114108416 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_d8_dbg&range=85490:85491

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

Congratulations! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-02-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-05-05)

This issue was migrated from crbug.com/chromium/1407342?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062647)*
