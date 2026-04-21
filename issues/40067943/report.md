# Security: V8: Debug check failed: result_type.IsSubtypeOf(output_graph_types_[index]).

| Field | Value |
|-------|-------|
| **Issue ID** | [40067943](https://issues.chromium.org/issues/40067943) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turbofan |
| **Platforms** | Linux |
| **Reporter** | sw...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2023-07-24 |
| **Bounty** | $7,000.00 |

## Description

deleted

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2023-07-24)

[Empty comment from Monorail migration]

### sw...@gmail.com (2023-07-24)

V8 affected version ：HEAD 
(commit 0d593b752c8721a43acb885a66dec65efb4a2238 (HEAD -> main, origin/main, origin/HEAD))

### sw...@gmail.com (2023-07-24)

In latest V8:head(commit 1b74e3049a953f2745d88e82b86da4c061275d53 (HEAD -> main, origin/main, origin/HEAD))

The detailed crash information is as follows：
build:
tools/dev/v8gen.py x64.debug
ninja -C out.gn/x64.debug

run:
./x64.debug/d8 --future --turboshaft-assert-types --always-turbofan ~/aa.js


#
# Fatal error in ../../src/compiler/turboshaft/type-inference-reducer.h, line 464
# Debug check failed: result_type.IsSubtypeOf(output_graph_types_[index]).
#
#
#
#FailureMessage Object: 0x7ffd437ea548
==== C stack trace ===============================

    /home/zj/v8/v8/out.gn/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1e) [0x7f58dff2befe]
    /home/zj/v8/v8/out.gn/x64.debug/libv8_libplatform.so(+0x5237d) [0x7f58dfe7e37d]
    /home/zj/v8/v8/out.gn/x64.debug/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x1ac) [0x7f58dfefa19c]
    /home/zj/v8/v8/out.gn/x64.debug/libv8_libbase.so(+0x55bec) [0x7f58dfef9bec]
    /home/zj/v8/v8/out.gn/x64.debug/libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x27) [0x7f58dfefa257]
    /home/zj/v8/v8/out.gn/x64.debug/libv8.so(v8::internal::compiler::turboshaft::TypeInferenceReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::AssertTypesReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TypeInferenceReducer>>, v8::internal::compiler::turboshaft::ReducerBase>>::SetType(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::Type const&, bool)+0x182) [0x7f58e665bc62]
    /home/zj/v8/v8/out.gn/x64.debug/libv8.so(v8::internal::compiler::turboshaft::TypeInferenceReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::AssertTypesReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TypeInferenceReducer>>, v8::internal::compiler::turboshaft::ReducerBase>>::RefineTypeFromInputGraph(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::Type const&, v8::internal::compiler::turboshaft::Type const&)+0x219) [0x7f58e665aba9]
    /home/zj/v8/v8/out.gn/x64.debug/libv8.so(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::TypeInferenceReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::AssertTypesReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TypeInferenceReducer>>, v8::internal::compiler::turboshaft::ReducerBase>>::ReduceInputGraphOperation<v8::internal::compiler::turboshaft::PhiOp, v8::internal::compiler::turboshaft::UniformReducerAdapter<v8::internal::compiler::turboshaft::TypeInferenceReducer, v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::AssertTypesReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TypeInferenceReducer>>, v8::internal::compiler::turboshaft::ReducerBase>>::ReducePhiContinuation>(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::PhiOp const&)+0x1b5) [0x7f58e6687775]
    /home/zj/v8/v8/out.gn/x64.debug/libv8.so(v8::internal::compiler::turboshaft::UniformReducerAdapter<v8::internal::compiler::turboshaft::TypeInferenceReducer, v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::AssertTypesReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TypeInferenceReducer>>, v8::internal::compiler::turboshaft::ReducerBase>>::ReduceInputGraphPhi(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::PhiOp const&)+0x29) [0x7f58e66875a9]
    /home/zj/v8/v8/out.gn/x64.debug/libv8.so(v8::internal::compiler::turboshaft::UniformReducerAdapter<v8::internal::compiler::turboshaft::AssertTypesReducer, v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::AssertTypesReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TypeInferenceReducer>>, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TypeInferenceReducer, v8::internal::compiler::turboshaft::ReducerBase>>::ReducePhiContinuation::ReduceInputGraph(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::PhiOp const&)+0x2c) [0x7f58e668752c]
    /home/zj/v8/v8/out.gn/x64.debug/libv8.so(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::AssertTypesReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::AssertTypesReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TypeInferenceReducer>>, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TypeInferenceReducer, v8::internal::compiler::turboshaft::ReducerBase>>::ReduceInputGraphOperation<v8::internal::compiler::turboshaft::PhiOp, v8::internal::compiler::turboshaft::UniformReducerAdapter<v8::internal::compiler::turboshaft::AssertTypesReducer, v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::AssertTypesReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TypeInferenceReducer>>, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TypeInferenceReducer, v8::internal::compiler::turboshaft::ReducerBase>>::ReducePhiContinuation>(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::PhiOp const&)+0x46) [0x7f58e6687356]
    /home/zj/v8/v8/out.gn/x64.debug/libv8.so(v8::internal::compiler::turboshaft::UniformReducerAdapter<v8::internal::compiler::turboshaft::AssertTypesReducer, v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::AssertTypesReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TypeInferenceReducer>>, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TypeInferenceReducer, v8::internal::compiler::turboshaft::ReducerBase>>::ReduceInputGraphPhi(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::PhiOp const&)+0x29) [0x7f58e6658989]
    /home/zj/v8/v8/out.gn/x64.debug/libv8.so(bool v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::AssertTypesReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TypeInferenceReducer>>>::VisitOp<false>(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::Block const*)+0x1d99) [0x7f58e66cba39]
    /home/zj/v8/v8/out.gn/x64.debug/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::AssertTypesReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TypeInferenceReducer>>>::VisitBlock<false>(v8::internal::compiler::turboshaft::Block const*)+0x1af) [0x7f58e66c9b1f]
    /home/zj/v8/v8/out.gn/x64.debug/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::AssertTypesReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TypeInferenceReducer>>>::VisitAllBlocks<false>()+0xeb) [0x7f58e66c98db]
    /home/zj/v8/v8/out.gn/x64.debug/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::AssertTypesReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TypeInferenceReducer>>>::VisitGraph<false>()+0xff) [0x7f58e661906f]
    /home/zj/v8/v8/out.gn/x64.debug/libv8.so(v8::internal::compiler::turboshaft::OptimizationPhaseImpl<v8::internal::compiler::turboshaft::AssertTypesReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TypeInferenceReducer>::Run(v8::internal::Zone*)+0x113) [0x7f58e66189d3]
    /home/zj/v8/v8/out.gn/x64.debug/libv8.so(v8::internal::compiler::turboshaft::OptimizationPhase<v8::internal::compiler::turboshaft::AssertTypesReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TypeInferenceReducer>::Run(v8::internal::Zone*)+0x15) [0x7f58e66183e5]
    /home/zj/v8/v8/out.gn/x64.debug/libv8.so(v8::internal::compiler::turboshaft::TypeAssertionsPhase::Run(v8::internal::Zone*)+0x82) [0x7f58e66182e2]
    /home/zj/v8/v8/out.gn/x64.debug/libv8.so(auto v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::turboshaft::TypeAssertionsPhase>()+0xff) [0x7f58e603ccaf]
    /home/zj/v8/v8/out.gn/x64.debug/libv8.so(v8::internal::compiler::PipelineImpl::OptimizeGraph(v8::internal::compiler::Linkage*)+0x892) [0x7f58e602bfb2]
    /home/zj/v8/v8/out.gn/x64.debug/libv8.so(v8::internal::compiler::PipelineCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0xee) [0x7f58e602b4ce]
    /home/zj/v8/v8/out.gn/x64.debug/libv8.so(v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x165) [0x7f58e3c486c5]
    /home/zj/v8/v8/out.gn/x64.debug/libv8.so(+0x3d22a9e) [0x7f58e3c63a9e]
    /home/zj/v8/v8/out.gn/x64.debug/libv8.so(+0x3d21795) [0x7f58e3c62795]
    /home/zj/v8/v8/out.gn/x64.debug/libv8.so(+0x3d11ecf) [0x7f58e3c52ecf]
    /home/zj/v8/v8/out.gn/x64.debug/libv8.so(v8::internal::Compiler::CompileOptimized(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::ConcurrencyMode, v8::internal::CodeKind)+0x180) [0x7f58e3c54520]
    /home/zj/v8/v8/out.gn/x64.debug/libv8.so(+0x4d34893) [0x7f58e4c75893]
    /home/zj/v8/v8/out.gn/x64.debug/libv8.so(v8::internal::Runtime_CompileOptimized(int, unsigned long*, v8::internal::Isolate*)+0x128) [0x7f58e4c752b8]
    [0x7f583f89cafd]
Trace/breakpoint trap (core dumped)

### cl...@chromium.org (2023-07-24)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4862391457873920.

### fl...@google.com (2023-07-24)

Hmmm, ClusterFuzz doesn't seem able to reproduce—might need some flags set that ClusterFuzz doesn't set?  So:

Assigning this to the current V8 sheriff—please take a look, thanks!

Setting provisional severity of High, assuming this causes renderer memory corruption.

Setting provisional FoundIn for Extended Stable.

[Monorail components: Blink>JavaScript]

### [Deleted User] (2023-07-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-07-25)

Re-uploading with the given flags (--future --turboshaft-assert-types --always-turbofan).

[Monorail components: -Blink>JavaScript Blink>JavaScript>WebAssembly]

### cl...@chromium.org (2023-07-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6589541688999936.

### cl...@chromium.org (2023-07-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-07-25)

Detailed Report: https://clusterfuzz.com/testcase?key=6589541688999936

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  result_type.IsSubtypeOf(output_graph_types_[index]) in type-inference-reducer.h
  v8::internal::compiler::turboshaft::TypeInferenceReducer<v8::internal::compiler:
  v8::internal::compiler::turboshaft::TypeInferenceReducer<v8::internal::compiler:
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=87820:87821

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6589541688999936

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### [Deleted User] (2023-07-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-07-25)

This is a turboshaft issue (as expected, as it requires --turboshaft-assert-types).

Clusterfuzz bisected to
00693ae [turboshaft] Move turboshaft from experimental to future by Nico Hartmann · 9 weeks ago

Nico, can you take a look please?
Also, please update the labels accordingly.

[Monorail components: -Blink>JavaScript>WebAssembly Blink>JavaScript>Compiler>Turbofan]

### [Deleted User] (2023-07-25)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ni...@chromium.org (2023-07-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-07-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/90301ad2af3d3316c97b74e5f13c3a295e904316

commit 90301ad2af3d3316c97b74e5f13c3a295e904316
Author: Nico Hartmann <nicohartmann@chromium.org>
Date: Thu Jul 27 10:18:32 2023

[turboshaft] Refine dependent types from input graph

We used to refine the static type of an operation when refining output
graph types from the input graph. This is not correct when combined
with optimizations, because we might reduce multiple operations (with
different types) of the input graph to the same operation in the output
graph. To provide proper typing, we update the flow dependent types
inside the respective blocks.

Bug: v8:12783, chromium:1467142
Change-Id: I6bdd1b24381fe2af78f4e94f15f9972db69c7328
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4720937
Reviewed-by: Tobias Tebbi <tebbi@chromium.org>
Commit-Queue: Tobias Tebbi <tebbi@chromium.org>
Auto-Submit: Nico Hartmann <nicohartmann@chromium.org>
Cr-Commit-Position: refs/heads/main@{#89229}

[modify] https://crrev.com/90301ad2af3d3316c97b74e5f13c3a295e904316/src/compiler/turboshaft/type-inference-reducer.h
[add] https://crrev.com/90301ad2af3d3316c97b74e5f13c3a295e904316/test/mjsunit/regress/regress-1467142.js


### ni...@chromium.org (2023-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-27)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-02)

Congratulations, Zhenjiang Zhao! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work!  

### sw...@gmail.com (2023-08-03)

Hi,
I saw the FoundIn-114 tag.Can this bug be assigned a CVE?

### am...@google.com (2023-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-11-21)

Hello Zhenjiang Zhao -- we consider attachments/POCs and all analysis included with reports to be an integral part of the report (https://g.co/chrome/vrp/#investigating-and-reporting-bugs), even when included in comments, so I have undeleted them. Thanks!

### am...@chromium.org (2023-11-21)

Also, apologies for not seeing your message in https://crbug.com/chromium/1467142#c21 sooner, but FoundIn does not apply here, as this issue was specific to unlaunched features, which is why it's marked as SI-None and would not be issued a CVE. 

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1467142?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067943)*
