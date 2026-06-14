# Security: Debug check failed: var.has_value().

| Field | Value |
|-------|-------|
| **Issue ID** | [40887781](https://issues.chromium.org/issues/40887781) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
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

for (let v1 = 0; v1 < 4002; v1++) {  

const v3 = [-160421.17589718767];  

v3.constructor = v1;  

try {  

const v4 = (-9223372036854775807)();  

} catch(v5) {  

}  

}  

}  

main();

# 

# Fatal error in ../../src/compiler/turboshaft/optimization-phase.h, line 254

# Debug check failed: var.has\_value().

# 

# 

# 

#FailureMessage Object: 0x7fff32609f88  

==== C stack trace ===============================

```
/home/uuu/v8_src.main/v8/out/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1e) [0x7f16ea2251de]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8_libplatform.so(+0x4b2bd) [0x7f16ea1792bd]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8_libbase.so(V8_Fatal(char const\*, int, char const\*, ...)+0x1ac) [0x7f16ea1f35dc]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8_libbase.so(+0x5802c) [0x7f16ea1f302c]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8_libbase.so(V8_Dcheck(char const\*, int, char const\*)+0x27) [0x7f16ea1f3697]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::DeadCodeEliminationReducer>>::MapToNewGraph<false>(v8::internal::compiler::turboshaft::OpIndex, int)+0xfa) [0x7f16ef51f08a]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::DeadCodeEliminationReducer>>::VisitPhi(v8::internal::compiler::turboshaft::PhiOp const&)+0x739) [0x7f16ef520f89]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(bool v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::DeadCodeEliminationReducer>>::VisitOp<false>(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::Block const\*)+0x100a) [0x7f16ef52a4ea]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::DeadCodeEliminationReducer>>::VisitBlock<false>(v8::internal::compiler::turboshaft::Block const\*)+0x374) [0x7f16ef5294b4]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::DeadCodeEliminationReducer>>::VisitAllBlocks<false>()+0xeb) [0x7f16ef5290ab]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::DeadCodeEliminationReducer>>::VisitGraph<false>()+0x375) [0x7f16ef51c665]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::OptimizationPhaseImpl<v8::internal::compiler::turboshaft::DeadCodeEliminationReducer>::Run(v8::internal::compiler::turboshaft::Graph\*, v8::internal::Zone\*, v8::internal::compiler::NodeOriginTable\*, std::Cr::tuple<> const&)+0xa4) [0x7f16ef5005f4]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::OptimizationPhase<v8::internal::compiler::turboshaft::DeadCodeEliminationReducer>::Run(v8::internal::Isolate\*, v8::internal::compiler::turboshaft::Graph\*, v8::internal::Zone\*, v8::internal::compiler::NodeOriginTable\*, std::Cr::tuple<> const&)+0x90) [0x7f16ef500400]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::TurboshaftDeadCodeEliminationPhase::Run(v8::internal::compiler::PipelineData\*, v8::internal::Zone\*)+0x90) [0x7f16ef500360]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(auto v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::TurboshaftDeadCodeEliminationPhase>()+0xae) [0x7f16ef33a18e]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::PipelineImpl::OptimizeGraph(v8::internal::compiler::Linkage\*)+0x6ff) [0x7f16ef32bfaf]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::compiler::PipelineCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats\*, v8::internal::LocalIsolate\*)+0xe3) [0x7f16ef32b643]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats\*, v8::internal::LocalIsolate\*)+0x14c) [0x7f16ed3b34ec]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(+0x31917f4) [0x7f16ed3cb7f4]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(+0x3190615) [0x7f16ed3ca615]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(+0x3182830) [0x7f16ed3bc830]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::Compiler::CompileOptimizedOSR(v8::internal::Isolate\*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::BytecodeOffset, v8::internal::ConcurrencyMode)+0x211) [0x7f16ed3c2f81]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(+0x400f736) [0x7f16ee249736]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(+0x400cbb9) [0x7f16ee246bb9]  
/home/uuu/v8_src.main/v8/out/x64.debug/libv8.so(v8::internal::Runtime_CompileOptimizedOSR(int, unsigned long\*, v8::internal::Isolate\*)+0x128) [0x7f16ee2467e8]  
[0x7f167f96b7bf]

```

## Timeline

### wh...@gmail.com (2023-01-14)

[Comment Deleted]

### [Deleted User] (2023-01-14)

[Empty comment from Monorail migration]

### wh...@gmail.com (2023-01-14)

[Comment Deleted]

### wh...@gmail.com (2023-01-14)

ok, please run d8 with this args:
--assert-types  --interrupt-budget=1000  --turboshaft

### cl...@chromium.org (2023-01-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6304925029171200.

### cl...@chromium.org (2023-01-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-01-17)

Detailed Report: https://clusterfuzz.com/testcase?key=6304925029171200

Fuzzer: None
Job Type: linux_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  var.has_value() in optimization-phase.h
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_d8_dbg&range=85142:85143

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6304925029171200

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2023-01-17)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript]

### cl...@chromium.org (2023-01-17)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/88eac4b870dc9becb11fdaa2e71ed60ceab44a60 ([turboshaft] Basic TypedOptimization and new DeadCodeElimination).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### dc...@chromium.org (2023-01-17)

Under the assumption that a DCHECK failures in V8 leads to further issues that may cause arbitrary code execution, tagging this as high. If that is not the case here, please add that info to the bug so the severity can be updated.

### ni...@chromium.org (2023-01-18)

Fix is coming. Still behind --turboshaft which is not shipped to users, yet.

### gi...@appspot.gserviceaccount.com (2023-01-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/83315824148ac3d25e7b4114d36eea8a98286c61

commit 83315824148ac3d25e7b4114d36eea8a98286c61
Author: Nico Hartmann <nicohartmann@chromium.org>
Date: Wed Jan 18 10:43:25 2023

[turboshaft] Remove weak liveness from dead code elimination

Bug: v8:12783, chromium:1407349
Change-Id: If90c5323e36641c2fe7ae6ea79985dc09cf9e2eb
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4176736
Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
Auto-Submit: Nico Hartmann <nicohartmann@chromium.org>
Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
Cr-Commit-Position: refs/heads/main@{#85362}

[add] https://crrev.com/83315824148ac3d25e7b4114d36eea8a98286c61/test/mjsunit/regress/regress-1407349.js
[modify] https://crrev.com/83315824148ac3d25e7b4114d36eea8a98286c61/src/compiler/turboshaft/dead-code-elimination-reducer.h


### ni...@chromium.org (2023-01-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-01-18)

ClusterFuzz testcase 6304925029171200 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_d8_dbg&range=85361:85362

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-01-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-18)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-26)

Congratulations! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts in discovering and reporting this issue to us.

### am...@google.com (2023-01-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-04-26)

This issue was migrated from crbug.com/chromium/1407349?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40887781)*
