# Security: Fatal error in src/compiler/turbofan-typer.cc, line 451

| Field | Value |
|-------|-------|
| **Issue ID** | [398431403](https://issues.chromium.org/issues/398431403) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Linux |
| **Reporter** | da...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2025-02-24 |
| **Bounty** | $7,000.00 |

## Description

# VULNERABILITY DETAILS

A type inconsistency was identified in `src/compiler/turbofan-typer.cc, line 451`.

More specifically, the previous type and current type of PhiNode in `UpdateType` appear to be inconsistent.

# VERSION

Chrome Version: V8 main branch commit `e3b5497f`

Operating System: Ubuntu 22.04 LTS

# REPRODUCTION CASE

`./d8 --allow-natives-syntax --jit-fuzzing ./poc.js`

# Type of crash:

UpdateType error

# Crash State:

```
1. Crash log

#
# Fatal error in ../../src/compiler/turbofan-typer.cc, line 451
# UpdateType error for node 133: ObjectIsArrayBufferView(88)
  88: Phi[kRepTagged](65, 133, 84)

#
#
#
#FailureMessage Object: 0x7fffffffb7b0
==== C stack trace ===============================

    /home/error403/v8/out/fuzzbuild/d8(v8::base::debug::StackTrace::StackTrace()+0x13) [0x5555571f51e3]
    /home/error403/v8/out/fuzzbuild/d8(+0x1ca09eb) [0x5555571f49eb]
    /home/error403/v8/out/fuzzbuild/d8(V8_Fatal(char const*, int, char const*, ...)+0x183) [0x5555571ed543]
    /home/error403/v8/out/fuzzbuild/d8(v8::internal::compiler::Typer::Visitor::UpdateType(v8::internal::compiler::Node*, v8::internal::compiler::Type)+0x202) [0x555559126d12]
    /home/error403/v8/out/fuzzbuild/d8(v8::internal::compiler::GraphReducer::Reduce(v8::internal::compiler::Node*)+0xb8) [0x555558e8b888]
    /home/error403/v8/out/fuzzbuild/d8(v8::internal::compiler::GraphReducer::ReduceTop()+0x3de) [0x555558e8b21e]
    /home/error403/v8/out/fuzzbuild/d8(v8::internal::compiler::GraphReducer::ReduceNode(v8::internal::compiler::Node*)+0x80) [0x555558e8a830]
    /home/error403/v8/out/fuzzbuild/d8(v8::internal::compiler::Typer::Run(v8::internal::ZoneVector<v8::internal::compiler::Node*> const&, v8::internal::compiler::LoopVariableOptimizer*)+0x127) [0x555559117347]
    /home/error403/v8/out/fuzzbuild/d8(v8::internal::compiler::TyperPhase::Run(v8::internal::compiler::TFPipelineData*, v8::internal::Zone*, v8::internal::compiler::Typer*)+0x1af) [0x555558be975f]
    /home/error403/v8/out/fuzzbuild/d8(auto v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::TyperPhase, v8::internal::compiler::Typer*>(v8::internal::compiler::Typer*&&)+0x8d) [0x555558aff5dd]
    /home/error403/v8/out/fuzzbuild/d8(v8::internal::compiler::PipelineImpl::OptimizeTurbofanGraph(v8::internal::compiler::Linkage*)+0x187) [0x555558af9db7]
    /home/error403/v8/out/fuzzbuild/d8(v8::internal::compiler::PipelineCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x144) [0x555558af9044]
    /home/error403/v8/out/fuzzbuild/d8(v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x7f) [0x5555573ecb1f]
    /home/error403/v8/out/fuzzbuild/d8(+0x1ea7ce7) [0x5555573fbce7]
    /home/error403/v8/out/fuzzbuild/d8(v8::internal::Compiler::CompileOptimized(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::ConcurrencyMode, v8::internal::CodeKind)+0x28c) [0x5555573fe06c]
    /home/error403/v8/out/fuzzbuild/d8(+0x2a3df3e) [0x555557f91f3e]
    /home/error403/v8/out/fuzzbuild/d8(+0x2a37ae5) [0x555557f8bae5]
    /home/error403/v8/out/fuzzbuild/d8(v8::internal::Runtime_OptimizeTurbofanEager(int, unsigned long*, v8::internal::Isolate*)+0x90) [0x555557f8b730]
    /home/error403/v8/out/fuzzbuild/d8(+0x4d75b3d) [0x55555a2c9b3d

```
```
2. Backtrace with symbols

#0  0x00005555571f2182 in v8::base::OS::Abort()::$_0::operator()() const (this=<optimized out>) at ../../src/base/platform/platform-posix.cc:731
#1  v8::base::OS::Abort () at ../../src/base/platform/platform-posix.cc:731
#2  0x00005555571ed551 in V8_Fatal (file=0x555556aeefd0 "../../src/compiler/turbofan-typer.cc", line=line@entry=451, format=0x555556b1d01c "UpdateType error for node %s") at ../../src/base/logging.cc:215
#3  0x0000555559126d12 in v8::internal::compiler::Typer::Visitor::UpdateType (this=0x7fffffffbf80, node=<optimized out>, current=...) at ../../src/compiler/turbofan-typer.cc:451
#4  0x0000555558e8b888 in v8::internal::compiler::Reducer::Reduce (this=0x7fffffffbf80, node=0x55555a8ed870, observe_node_manager=0x0) at
 ../../src/compiler/graph-reducer.cc:34
#5  v8::internal::compiler::GraphReducer::Reduce (this=this@entry=0x7fffffffbe88, node=node@entry=0x55555a8ed870) at ../../src/compiler/graph-reducer.cc:105
#6  0x0000555558e8b21e in v8::internal::compiler::GraphReducer::ReduceTop (this=this@entry=0x7fffffffbe88) at ../../src/compiler/graph-reducer.cc:178
#7  0x0000555558e8a830 in v8::internal::compiler::GraphReducer::ReduceNode (this=0x7fffffffbe88, node=<optimized out>) at ../../src/compiler/graph-reducer.cc:75
#8  0x0000555559117347 in v8::internal::compiler::Typer::Run (this=<optimized out>, roots=..., induction_vars=0x7fffffffc018) at ../../src/compiler/turbofan-typer.cc:479
#9  0x0000555558be975f in v8::internal::compiler::TyperPhase::Run (this=this@entry=0x7fffffffc187, data=data@entry=0x55555a8a3bd0, temp_zone=temp_zone@entry=0x55555a8c00f0, typer=0x55555a8a5010) at ../../src/compiler/pipeline.cc:1044
#10 0x0000555558aff5dd in _ZN2v88internal8compiler12PipelineImpl3RunITkNS1_10turboshaft13TurbofanPhaseENS1_10TyperPhaseEJPNS1_5TyperEEEEDaDpOT0_ (this=this@entry=0x55555a8a4000, args=@0x7fffffffc1d0: 0x55555a8a5010) at ../../src/compiler/pipeline.cc:839
#11 0x0000555558af9db7 in v8::internal::compiler::PipelineImpl::OptimizeTurbofanGraph (this=this@entry=0x55555a8a4000, linkage=0x55555a89dc58) at ../../src/compiler/pipeline.cc:1978
#12 0x0000555558af9044 in v8::internal::compiler::PipelineCompilationJob::ExecuteJobImpl (this=0x55555a8a3a30, stats=<optimized out>, local_isolate=<optimized out>) at ../../src/compiler/pipeline.cc:778
#13 0x00005555573ecb1f in v8::internal::OptimizedCompilationJob::ExecuteJob (this=this@entry=0x55555a8a3a30, stats=0x55555a83e568, local_isolate=0x55555a864b30) at ../../src/codegen/compiler.cc:470
#14 0x00005555573fbce7 in v8::internal::(anonymous namespace)::CompileTurbofan_NotConcurrent (isolate=0x55555a82a000, job=0x55555a8a3a30) at ../../src/codegen/compiler.cc:1103
#15 v8::internal::(anonymous namespace)::CompileTurbofan (isolate=0x55555a82a000, function=..., shared=..., mode=v8::internal::ConcurrencyMode::kSynchronous, osr_offset=..., result_behavior=v8::internal::(anonymous namespace)::CompileResultBehavior::kDefault) at ../../src/codegen/compiler.cc:1248
#16 v8::internal::(anonymous namespace)::GetOrCompileOptimized (isolate=isolate@entry=0x55555a82a000, function=function@entry=..., mode=v8::internal::ConcurrencyMode::kSynchronous, code_kind=code_kind@entry=v8::internal::CodeKind::TURBOFAN_JS, osr_offset=osr_offset@entry=..., result_behavior=result_behavior@entry=v8::internal::(anonymous namespace)::CompileResultBehavior::kDefault) at ../../src/codegen/compiler.cc:1416
#17 0x00005555573fe06c in v8::internal::Compiler::CompileOptimized (isolate=0x55555a82a000, function=..., mode=v8::internal::ConcurrencyMode::kSynchronous, code_kind=<optimized out>) at ../../src/codegen/compiler.cc:3197
#18 0x0000555557f91f3e in v8::internal::(anonymous namespace)::CompileOptimized (function=function@entry=..., mode=mode@entry=v8::internal::ConcurrencyMode::kSynchronous, target_kind=target_kind@entry=v8::internal::CodeKind::TURBOFAN_JS, isolate=isolate@entry=0x55555a82a000) at ../../src/runtime/runtime-compiler.cc:185
#19 0x0000555557f8bae5 in v8::internal::__RT_impl_Runtime_OptimizeTurbofanEager (args=..., isolate=isolate@entry=0x55555a82a000) at ../../src/runtime/runtime-compiler.cc:227
#20 0x0000555557f8b730 in v8::internal::Runtime_OptimizeTurbofanEager (args_length=<optimized out>, args_object=0x7fffffffc5f8, isolate=0x55555a82a000) at ../../src/runtime/runtime-compiler.cc:222
#21 0x000055555a2c9b3d in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit ()
#22 0x000055555a1925f3 in Builtins_OptimizeTurbofanEager ()
#23 0x000055555a190863 in Builtins_InterpreterEntryTrampoline ()

```

Reporter credit: Changheon Lee (@2rr0r4o3)

## Attachments

- poc.js (text/javascript, 195 B)

## Timeline

### da...@gmail.com (2025-02-24)

Tests with `regress-394650781.js` added in <https://chromium-review.googlesource.com/c/v8/v8/+/6243195>, which appears to be related to this report, pass without detected this case. Also, the crash in this report is reliably reproduced in `65beb80d`.

### cl...@appspot.gserviceaccount.com (2025-02-24)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5472612528357376.

### 24...@project.gserviceaccount.com (2025-02-24)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2025-02-24)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/65beb80d9cd6da4cca447a3a8857b59035412417 ([turbofan] Fix related to the TypedArray type

ObjectIsArrayBufferView was not expecting it.

Bug: 388844115, 394650781
Change-Id: I6bc6214f6367e76b956a759842771a325d54b175
Fixed: 394650781
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6243195
Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
Commit-Queue: Marja Hölttä <marja@chromium.org>
Cr-Commit-Position: refs/heads/main@{#98574}
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### 24...@project.gserviceaccount.com (2025-02-24)

Detailed Report: https://clusterfuzz.com/testcase?key=5472612528357376

Fuzzer: None
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: Fatal error
Crash Address: 
Crash State:
  UpdateType error for node 133: ObjectIsArrayBufferView(88)
  v8::internal::compiler::Typer::Visitor::UpdateType
  v8::internal::compiler::Reducer::Reduce
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8&range=98573:98574

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5472612528357376

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### ap...@google.com (2025-02-25)

Project: v8/v8  

Branch: main  

Author: Marja Hölttä <[marja@chromium.org](mailto:marja@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6298237>

[turbofan, typed array length] Fix typing

---


Expand for full commit details
```
[turbofan, typed array length] Fix typing 
 
This modification should've been included in 
https://chromium-review.googlesource.com/c/v8/v8/+/6243195 
but it wasn't. 
 
Bug: 388844115, 398431403 
Change-Id: I50ed97a29fa2e5e317f85b8936007c568bea8aa1 
Fixed: 398431403 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6298237 
Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
Commit-Queue: Marja Hölttä <marja@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#98911}

```

---

Files:

- M `src/compiler/turbofan-typer.cc`
- A `test/mjsunit/compiler/regress-398431403.js`

---

Hash: e9c28abfe4d8f4c86c15d0280645bc95cbae9779  

Date:  Tue Feb 25 10:20:40 2025


---

### ch...@google.com (2025-02-25)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-02-25)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### 24...@project.gserviceaccount.com (2025-02-26)

ClusterFuzz testcase 5472612528357376 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8&range=98910:98911

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2025-03-05)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M135. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
**Merge approved:** your change passed merge requirements and is auto-approved for M135. Please go ahead and merge the CL to branch 7049 (refs/branch-heads/7049) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: alonbajayo (ChromeOS), pbommana (Desktop US), danielyip (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [135].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### sp...@google.com (2025-03-06)

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

### am...@chromium.org (2025-03-06)

Congratulations Changheon! Thank you for your efforts and reporting this issue to us!

### pb...@google.com (2025-03-06)

Your Merge request has been approved, Please land your merge as soon as possible, to ensure the change is included in next week's RC build for Beta release, please complete your merges to M135 on or before 1pm PST on Tuesday March-11th. Thank you


### da...@google.com (2025-03-11)

Fix landed in M135 so there is no need to CP.

<https://chromiumdash.appspot.com/commits?commit=e9c28abfe4d8f4c86c15d0280645bc95cbae9779&platform=Mac>

### ch...@google.com (2025-06-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of memory corruption in a sandboxed process / renderer

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/398431403)*
