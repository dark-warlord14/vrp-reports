# Debug check failed: input_count <= std::numeric_limits<decltype(this->input_count)>::max() (65554 vs. 65535). in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [380487911](https://issues.chromium.org/issues/380487911) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turbofan |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2024-11-23 |
| **Bounty** | $8,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 97096
    - link: https://crrev.com/033ed071b5fee9d55f87ad88c10b4cc1aeee84b4 
- Commit Message

```
commit 033ed071b5fee9d55f87ad88c10b4cc1aeee84b4
Author: Darius Mercadier <dmercadier@chromium.org>
Date:   Mon Nov 11 12:30:14 2024 +0100

    [turboshaft] Escape analysis for string concatenation
    
    Change-Id: I4bce8c2ee504984240540f1dae6dcce538b90fd0
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5993586
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
    Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#97096}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-97365/d8 --allow-natives-syntax --turboshaft-string-concat-escape-analysis poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/compiler/turboshaft/operations.h, line 1008
# Debug check failed: input_count <= std::numeric_limits<decltype(this->input_count)>::max() (65554 vs. 65535).
#
#
#
#FailureMessage Object: 0x7ffec09f72a0
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-97365/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7fdbdfcd2583]
    /tmp/d8-linux-debug-v8-component-97365/libv8_libplatform.so(+0x1a05d) [0x7fdbdfc7c05d]
    /tmp/d8-linux-debug-v8-component-97365/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x194) [0x7fdbdfcb41a4]
    /tmp/d8-linux-debug-v8-component-97365/libv8_libbase.so(+0x2bbb5) [0x7fdbdfcb3bb5]
    /tmp/d8-linux-debug-v8-component-97365/libv8.so(v8::internal::compiler::turboshaft::OperationT<v8::internal::compiler::turboshaft::FrameStateOp>::OperationT(v8::internal::compiler::turboshaft::ShadowyOpIndexVectorWrapper)+0x9a) [0x7fdbde24b87a]
    /tmp/d8-linux-debug-v8-component-97365/libv8.so(v8::internal::compiler::turboshaft::FrameStateOp& v8::internal::compiler::turboshaft::OperationT<v8::internal::compiler::turboshaft::FrameStateOp>::New<v8::internal::compiler::turboshaft::ShadowyOpIndexVectorWrapper, bool, v8::internal::compiler::turboshaft::FrameStateData const*>(v8::internal::compiler::turboshaft::Graph*, unsigned long, v8::internal::compiler::turboshaft::ShadowyOpIndexVectorWrapper, bool, v8::internal::compiler::turboshaft::FrameStateData const*)+0x4f) [0x7fdbde24b74f]
    /tmp/d8-linux-debug-v8-component-97365/libv8.so(v8::internal::compiler::turboshaft::FrameStateOp& v8::internal::compiler::turboshaft::Graph::Add<v8::internal::compiler::turboshaft::FrameStateOp, v8::internal::compiler::turboshaft::ShadowyOpIndexVectorWrapper, bool, v8::internal::compiler::turboshaft::FrameStateData const*>(v8::internal::compiler::turboshaft::ShadowyOpIndexVectorWrapper, bool, v8::internal::compiler::turboshaft::FrameStateData const*)+0x81) [0x7fdbde24b381]
    /tmp/d8-linux-debug-v8-component-97365/libv8.so(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::StringEscapeAnalysisReducer, v8::internal::compiler::turboshaft::JSGenericLoweringReducer, v8::internal::compiler::turboshaft::DataViewLoweringReducer, v8::internal::compiler::turboshaft::MachineLoweringReducer, v8::internal::compiler::turboshaft::FastApiCallLoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>>::Emit<v8::internal::compiler::turboshaft::FrameStateOp, v8::internal::compiler::turboshaft::ShadowyOpIndexVectorWrapper, bool, v8::internal::compiler::turboshaft::FrameStateData const*>(v8::internal::compiler::turboshaft::ShadowyOpIndexVectorWrapper, bool, v8::internal::compiler::turboshaft::FrameStateData const*)+0x85) [0x7fdbdf2cf5d5]
    /tmp/d8-linux-debug-v8-component-97365/libv8.so(v8::internal::compiler::turboshaft::StringEscapeAnalysisReducer<v8::internal::compiler::turboshaft::JSGenericLoweringReducer<v8::internal::compiler::turboshaft::DataViewLoweringReducer<v8::internal::compiler::turboshaft::MachineLoweringReducer<v8::internal::compiler::turboshaft::FastApiCallLoweringReducer<v8::internal::compiler::turboshaft::VariableReducer<v8::internal::compiler::turboshaft::SelectLoweringReducer<v8::internal::compiler::turboshaft::MachineOptimizationReducer<v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::StringEscapeAnalysisReducer, v8::internal::compiler::turboshaft::JSGenericLoweringReducer, v8::internal::compiler::turboshaft::DataViewLoweringReducer, v8::internal::compiler::turboshaft::MachineLoweringReducer, v8::internal::compiler::turboshaft::FastApiCallLoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>>>>>>>>>>>>::BuildFrameState(v8::internal::compiler::turboshaft::FrameStateOp const&)+0x342) [0x7fdbdf301ef2]
    /tmp/d8-linux-debug-v8-component-97365/libv8.so(v8::internal::compiler::turboshaft::StringEscapeAnalysisReducer<v8::internal::compiler::turboshaft::JSGenericLoweringReducer<v8::internal::compiler::turboshaft::DataViewLoweringReducer<v8::internal::compiler::turboshaft::MachineLoweringReducer<v8::internal::compiler::turboshaft::FastApiCallLoweringReducer<v8::internal::compiler::turboshaft::VariableReducer<v8::internal::compiler::turboshaft::SelectLoweringReducer<v8::internal::compiler::turboshaft::MachineOptimizationReducer<v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::StringEscapeAnalysisReducer, v8::internal::compiler::turboshaft::JSGenericLoweringReducer, v8::internal::compiler::turboshaft::DataViewLoweringReducer, v8::internal::compiler::turboshaft::MachineLoweringReducer, v8::internal::compiler::turboshaft::FastApiCallLoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>>>>>>>>>>>>::ReduceInputGraphFrameState(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::FrameStateOp const&)+0x133) [0x7fdbdf2d54a3]
    /tmp/d8-linux-debug-v8-component-97365/libv8.so(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::StringEscapeAnalysisReducer<v8::internal::compiler::turboshaft::JSGenericLoweringReducer<v8::internal::compiler::turboshaft::DataViewLoweringReducer<v8::internal::compiler::turboshaft::MachineLoweringReducer<v8::internal::compiler::turboshaft::FastApiCallLoweringReducer<v8::internal::compiler::turboshaft::VariableReducer<v8::internal::compiler::turboshaft::SelectLoweringReducer<v8::internal::compiler::turboshaft::MachineOptimizationReducer<v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::StringEscapeAnalysisReducer, v8::internal::compiler::turboshaft::JSGenericLoweringReducer, v8::internal::compiler::turboshaft::DataViewLoweringReducer, v8::internal::compiler::turboshaft::MachineLoweringReducer, v8::internal::compiler::turboshaft::FastApiCallLoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>>>>>>>>>>>>>::VisitOpNoMappingUpdate<false>(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::Block const*)+0x90a) [0x7fdbdf2d7d1a]
    /tmp/d8-linux-debug-v8-component-97365/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::StringEscapeAnalysisReducer<v8::internal::compiler::turboshaft::JSGenericLoweringReducer<v8::internal::compiler::turboshaft::DataViewLoweringReducer<v8::internal::compiler::turboshaft::MachineLoweringReducer<v8::internal::compiler::turboshaft::FastApiCallLoweringReducer<v8::internal::compiler::turboshaft::VariableReducer<v8::internal::compiler::turboshaft::SelectLoweringReducer<v8::internal::compiler::turboshaft::MachineOptimizationReducer<v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::StringEscapeAnalysisReducer, v8::internal::compiler::turboshaft::JSGenericLoweringReducer, v8::internal::compiler::turboshaft::DataViewLoweringReducer, v8::internal::compiler::turboshaft::MachineLoweringReducer, v8::internal::compiler::turboshaft::FastApiCallLoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>>>>>>>>>>>>>::VisitBlockBody<(v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::StringEscapeAnalysisReducer<v8::internal::compiler::turboshaft::JSGenericLoweringReducer<v8::internal::compiler::turboshaft::DataViewLoweringReducer<v8::internal::compiler::turboshaft::MachineLoweringReducer<v8::internal::compiler::turboshaft::FastApiCallLoweringReducer<v8::internal::compiler::turboshaft::VariableReducer<v8::internal::compiler::turboshaft::SelectLoweringReducer<v8::internal::compiler::turboshaft::MachineOptimizationReducer<v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::StringEscapeAnalysisReducer, v8::internal::compiler::turboshaft::JSGenericLoweringReducer, v8::internal::compiler::turboshaft::DataViewLoweringReducer, v8::internal::compiler::turboshaft::MachineLoweringReducer, v8::internal::compiler::turboshaft::FastApiCallLoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>>>>>>>>>>>>>::CanHavePhis)1, (v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::StringEscapeAnalysisReducer<v8::internal::compiler::turboshaft::JSGenericLoweringReducer<v8::internal::compiler::turboshaft::DataViewLoweringReducer<v8::internal::compiler::turboshaft::MachineLoweringReducer<v8::internal::compiler::turboshaft::FastApiCallLoweringReducer<v8::internal::compiler::turboshaft::VariableReducer<v8::internal::compiler::turboshaft::SelectLoweringReducer<v8::internal::compiler::turboshaft::MachineOptimizationReducer<v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::StringEscapeAnalysisReducer, v8::internal::compiler::turboshaft::JSGenericLoweringReducer, v8::internal::compiler::turboshaft::DataViewLoweringReducer, v8::internal::compiler::turboshaft::MachineLoweringReducer, v8::internal::compiler::turboshaft::FastApiCallLoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>>>>>>>>>>>>>::ForCloning)0, false>(v8::internal::compiler::turboshaft::Block const*, int)+0x40a) [0x7fdbdf36d53a]
    /tmp/d8-linux-debug-v8-component-97365/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::StringEscapeAnalysisReducer<v8::internal::compiler::turboshaft::JSGenericLoweringReducer<v8::internal::compiler::turboshaft::DataViewLoweringReducer<v8::internal::compiler::turboshaft::MachineLoweringReducer<v8::internal::compiler::turboshaft::FastApiCallLoweringReducer<v8::internal::compiler::turboshaft::VariableReducer<v8::internal::compiler::turboshaft::SelectLoweringReducer<v8::internal::compiler::turboshaft::MachineOptimizationReducer<v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::StringEscapeAnalysisReducer, v8::internal::compiler::turboshaft::JSGenericLoweringReducer, v8::internal::compiler::turboshaft::DataViewLoweringReducer, v8::internal::compiler::turboshaft::MachineLoweringReducer, v8::internal::compiler::turboshaft::FastApiCallLoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>>>>>>>>>>>>>::VisitBlock<false>(v8::internal::compiler::turboshaft::Block const*)+0xa9) [0x7fdbdf36ce39]
    /tmp/d8-linux-debug-v8-component-97365/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::StringEscapeAnalysisReducer<v8::internal::compiler::turboshaft::JSGenericLoweringReducer<v8::internal::compiler::turboshaft::DataViewLoweringReducer<v8::internal::compiler::turboshaft::MachineLoweringReducer<v8::internal::compiler::turboshaft::FastApiCallLoweringReducer<v8::internal::compiler::turboshaft::VariableReducer<v8::internal::compiler::turboshaft::SelectLoweringReducer<v8::internal::compiler::turboshaft::MachineOptimizationReducer<v8::internal::compiler::turboshaft::EmitProjectionReducer<v8::internal::compiler::turboshaft::GenericReducerBase<v8::internal::compiler::turboshaft::TSReducerBase<v8::internal::compiler::turboshaft::StackBottom<v8::base::tmp::list1<v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::StringEscapeAnalysisReducer, v8::internal::compiler::turboshaft::JSGenericLoweringReducer, v8::internal::compiler::turboshaft::DataViewLoweringReducer, v8::internal::compiler::turboshaft::MachineLoweringReducer, v8::internal::compiler::turboshaft::FastApiCallLoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>>>>>>>>>>>>>::VisitAllBlocks<false>()+0xe3) [0x7fdbdf36cc83]
    /tmp/d8-linux-debug-v8-component-97365/libv8.so(v8::internal::compiler::turboshaft::CopyingPhaseImpl<v8::internal::compiler::turboshaft::StringEscapeAnalysisReducer, v8::internal::compiler::turboshaft::JSGenericLoweringReducer, v8::internal::compiler::turboshaft::DataViewLoweringReducer, v8::internal::compiler::turboshaft::MachineLoweringReducer, v8::internal::compiler::turboshaft::FastApiCallLoweringReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer>::Run(v8::internal::compiler::turboshaft::PipelineData*, v8::internal::compiler::turboshaft::Graph&, v8::internal::Zone*, bool)+0x1c8) [0x7fdbdf2c72c8]
    /tmp/d8-linux-debug-v8-component-97365/libv8.so(auto v8::internal::compiler::turboshaft::Pipeline::Run<v8::internal::compiler::turboshaft::MachineLoweringPhase>()+0xda) [0x7fdbded3128a]
    /tmp/d8-linux-debug-v8-component-97365/libv8.so(v8::internal::compiler::turboshaft::Pipeline::OptimizeTurboshaftGraph(v8::internal::compiler::Linkage*)+0xc1) [0x7fdbded170c1]
    /tmp/d8-linux-debug-v8-component-97365/libv8.so(v8::internal::compiler::PipelineCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x13c) [0x7fdbded15f9c]
    /tmp/d8-linux-debug-v8-component-97365/libv8.so(v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x8d) [0x7fdbdcc03b6d]
    /tmp/d8-linux-debug-v8-component-97365/libv8.so(+0x2c18ce5) [0x7fdbdcc18ce5]
    /tmp/d8-linux-debug-v8-component-97365/libv8.so(v8::internal::Compiler::CompileOptimized(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::ConcurrencyMode, v8::internal::CodeKind)+0x31f) [0x7fdbdcc1c2ff]
    /tmp/d8-linux-debug-v8-component-97365/libv8.so(+0x3ba0102) [0x7fdbddba0102]
    /tmp/d8-linux-debug-v8-component-97365/libv8.so(+0x3b986e8) [0x7fdbddb986e8]
    /tmp/d8-linux-debug-v8-component-97365/libv8.so(v8::internal::Runtime_OptimizeTurbofanEager(int, unsigned long*, v8::internal::Isolate*)+0x90) [0x7fdbddb982c0]
    /tmp/d8-linux-debug-v8-component-97365/libv8.so(+0x20936fd) [0x7fdbdc0936fd]

```

## Other
Please note to include the flags `--allow-natives-syntax --turboshaft-string-concat-escape-analysis` for clusterfuzz classification.

VERSION
Tested on v8 version: 13.2.0 - 13.3.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-97365.zip
2. Run: `d8 --allow-natives-syntax --turboshaft-string-concat-escape-analysis poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Jerry

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 457 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-11-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4924031723569152.

### am...@chromium.org (2024-11-25)

Thank for the report, Jerry.
I've uploaded the testcase in clusterfuzz for now.
In the meantime, assigning to dmercadier@ based on bisect provided by the reporter, and set provisional severity and priority as S1/P1 since this is potential memory corruption in the renderer.

### 24...@project.gserviceaccount.com (2024-11-25)

ClusterFuzz testcase 4924031723569152 appears to be flaky, updating reproducibility hotlist.

### 24...@project.gserviceaccount.com (2024-11-25)

Detailed Report: https://clusterfuzz.com/testcase?key=4924031723569152

Fuzzer: None
Job Type: linux_asan_d8_dbg
Crash Type: 
Crash Address: 
Crash State:
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&revision=0

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4924031723569152

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

### je...@gmail.com (2024-11-26)

I'm not sure why ClusterFuzz can't reproduce it. Could you add the --future flag and check it? I can still reproduce it on the HEAD.

### ma...@google.com (2024-11-26)

This reproduces locally with the build that CF would use. We might have some CF infra problem atm.

### pe...@google.com (2024-11-26)

Setting milestone because of s0/s1 severity.

### cl...@appspot.gserviceaccount.com (2024-11-26)

Detailed Report: https://clusterfuzz.com/testcase?key=6534773577023488

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  input_count <= std::numeric_limits<decltype(this->input_count)>::max() in operat
  v8::internal::compiler::turboshaft::Operation::Operation
  v8::internal::compiler::turboshaft::FrameStateOp& v8::internal::compiler::turbos
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=97095:97096

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6534773577023488

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### ap...@google.com (2024-11-27)

Project: v8/v8  

Branch: main  

Author: Darius Mercadier <[dmercadier@chromium.org](mailto:dmercadier@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6048886>

[turboshaft] Deduplicate String concatenations in FrameState

---


Expand for full commit details
```
[turboshaft] Deduplicate String concatenations in FrameState 
 
This is a performance optimization, in particular because some common 
patterns can easily lead to a quadratic or even exponential FrameState 
size. 
 
Quadratic: 
 
    str += a 
    str += b 
    str += c 
 
Exponential: 
 
    str += str 
    str += str 
    str += str 
 
Bug: chromium:380487911 
Change-Id: I0361aeba697bf29ee69fd688d7dbb3f4c249bea3 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6048886 
Commit-Queue: Darius Mercadier <dmercadier@chromium.org> 
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#97441}

```

---

Files:

- M `src/compiler/backend/instruction-selector.cc`
- M `src/compiler/backend/instruction.h`
- M `src/compiler/turboshaft/deopt-data.h`
- M `src/compiler/turboshaft/maglev-graph-building-phase.cc`
- M `src/compiler/turboshaft/operations.cc`
- M `src/compiler/turboshaft/string-escape-analysis-reducer.h`
- M `src/deoptimizer/translated-state.cc`
- M `src/deoptimizer/translated-state.h`
- A `test/mjsunit/turboshaft/string-escape-analysis-exponential-state.js`

---

Hash: 29e1428ecc57d9bd672e07f5060d3615381ca6c6  

Date:  Wed Nov 27 11:07:58 2024


---

### dm...@chromium.org (2024-11-27)

Thanks for the report :)

What's happening is that we try to create a Turboshaft operation (a FrameState to be precise) with more than 2\*\*16-1 input. In DEBUG mode, this triggers the DCHECK, and in release mode, the number of inputs wraps around, so we end up creating a FrameState with very few actual inputs, but with other meta data that say that the FrameState has many inputs. Then, in the instruction selector, we trust the meta data and try to read inputs that don't exist, which will either lead to a segfault when reading at a wrong address, or it will lead to interpreting random(ish) memory as Turbosahft operations, which will lead to once again either crashing when trying to read their fields (this is what I always get in my tests), or to generating wrong code.

In order to exploit this, one would have to create a fairly large Turboshaft graph with carefully chosen instructions, carefully placed, which, when interpreted as inputs to the FrameState, don't cause crashes, but lead to producing a code that does bad things in a controlled way. With the caveat that because of redundancy elimination, each of the many instructions has to be unique. And, because instructions are unique, there is a high chance that they will have to be inputs into a FrameState, leading to Turboshaft bailing out at graph building time because FrameStates have already too many inputs (during graph building, this issue is cleanly handled and leads to a clean bailout).

So, I don't think that this is exploitable.

Let me know if you disagree.

(btw, the commit in [comment #10](https://issues.chromium.org/issues/380487911#comment10) fixes this specific repro, but not the issue in general. The real fix is <https://crrev.com/c/6054199>; landing soon)

### je...@gmail.com (2024-11-27)

I'm not quite sure about this, but you can directly decide whether to keep the vulnerability or classify it as a bug.

### je...@gmail.com (2024-11-27)

However, according to what you said, it seems that there is a possibility of interpreting random memory as instructions, resulting in type confusion. Although I think it would be very difficult to exploit this vulnerability, it would be better to keep it as a vulnerability out of caution, as there may still be unknown exploitation methods.

### ap...@google.com (2024-11-28)

Project: v8/v8  

Branch: main  

Author: Darius Mercadier <[dmercadier@chromium.org](mailto:dmercadier@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6054199>

[turboshaft] string escape analysis: avoid having too many inputs in ops

---


Expand for full commit details
```
[turboshaft] string escape analysis: avoid having too many inputs in ops 
 
String escape analysis can require adding additional inputs to 
FrameStates, which could lead to trying to create a FrameState with 
more than the maximum number of allowed inputs (2**16-1). 
This CL fixes this issue. 
 
Fixed: chromium:380487911 
Change-Id: I903a7f96804782c4ed894b88986460858355411c 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6054199 
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org> 
Commit-Queue: Darius Mercadier <dmercadier@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#97452}

```

---

Files:

- M `src/compiler/turboshaft/string-escape-analysis-reducer.cc`
- M `src/compiler/turboshaft/string-escape-analysis-reducer.h`
- A `test/mjsunit/turboshaft/regress-380487911.js`

---

Hash: c8e4bf25f4b1f4e1819f44426b2ea6c94b8fd00f  

Date:  Wed Nov 27 12:15:04 2024


---

### ap...@google.com (2024-11-28)

Project: v8/v8  

Branch: main  

Author: Darius Mercadier <[dmercadier@chromium.org](mailto:dmercadier@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6054991>

Revert "[turboshaft] string escape analysis: avoid having too many inputs in ops"

---


Expand for full commit details
```
Revert "[turboshaft] string escape analysis: avoid having too many inputs in ops" 
 
This reverts commit c8e4bf25f4b1f4e1819f44426b2ea6c94b8fd00f. 
 
Reason for revert: the test is too slow; our bots don't like that. 
 
Original change's description: 
> [turboshaft] string escape analysis: avoid having too many inputs in ops 
> 
> String escape analysis can require adding additional inputs to 
> FrameStates, which could lead to trying to create a FrameState with 
> more than the maximum number of allowed inputs (2**16-1). 
> This CL fixes this issue. 
> 
> Fixed: chromium:380487911 
> Change-Id: I903a7f96804782c4ed894b88986460858355411c 
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6054199 
> Reviewed-by: Nico Hartmann <nicohartmann@chromium.org> 
> Commit-Queue: Darius Mercadier <dmercadier@chromium.org> 
> Cr-Commit-Position: refs/heads/main@{#97452} 
 
Change-Id: I7a6aeb95eb38f2b5825ca1ac57c9c739f0aebe9a 
No-Presubmit: true 
No-Tree-Checks: true 
No-Try: true 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6054991 
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
Commit-Queue: Darius Mercadier <dmercadier@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#97459}

```

---

Files:

- M `src/compiler/turboshaft/string-escape-analysis-reducer.cc`
- M `src/compiler/turboshaft/string-escape-analysis-reducer.h`
- D `test/mjsunit/turboshaft/regress-380487911.js`

---

Hash: 631bcfd3abfdcaa98a5e8e8bb7d8efd278770593  

Date:  Thu Nov 28 11:38:38 2024


---

### ap...@google.com (2024-11-28)

Project: v8/v8  

Branch: main  

Author: Darius Mercadier <[dmercadier@chromium.org](mailto:dmercadier@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6054992>

Reland "[turboshaft] string escape analysis: avoid having too many inputs in ops"

---


Expand for full commit details
```
Reland "[turboshaft] string escape analysis: avoid having too many inputs in ops" 
 
This is a reland of commit c8e4bf25f4b1f4e1819f44426b2ea6c94b8fd00f 
 
The mjsunit test was a bit slow, so in the reland I've marked it as 
such and I'm skipping it on most platforms. 
 
Original change's description: 
> [turboshaft] string escape analysis: avoid having too many inputs in ops 
> 
> String escape analysis can require adding additional inputs to 
> FrameStates, which could lead to trying to create a FrameState with 
> more than the maximum number of allowed inputs (2**16-1). 
> This CL fixes this issue. 
> 
> Fixed: chromium:380487911 
> Change-Id: I903a7f96804782c4ed894b88986460858355411c 
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6054199 
> Reviewed-by: Nico Hartmann <nicohartmann@chromium.org> 
> Commit-Queue: Darius Mercadier <dmercadier@chromium.org> 
> Cr-Commit-Position: refs/heads/main@{#97452} 
 
Change-Id: Iecef95009019dfa7c9123cd40ede9ad0f43eee04 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6054992 
Auto-Submit: Darius Mercadier <dmercadier@chromium.org> 
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org> 
Commit-Queue: Nico Hartmann <nicohartmann@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#97463}

```

---

Files:

- M `src/compiler/turboshaft/string-escape-analysis-reducer.cc`
- M `src/compiler/turboshaft/string-escape-analysis-reducer.h`
- M `test/mjsunit/mjsunit.status`
- A `test/mjsunit/turboshaft/regress-380487911.js`

---

Hash: 0933c22b536f0e41e1fe9a3ebd29efe05ff525ee  

Date:  Thu Nov 28 13:32:05 2024


---

### sp...@google.com (2024-12-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
$7,000 for report of memory corruption in a sandboxed process / renderer + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-12-05)

Congratulations Jerry! Thank you for your efforts and reporting this issue to us.

### 24...@project.gserviceaccount.com (2024-12-05)

ClusterFuzz testcase 4924031723569152 is still reproducing on the latest available build .

Please re-test your fix against this testcase and if the fix was incorrect or incomplete, please re-open the bug. Otherwise, ignore this notification and add the hotlistid:5433040.

### pe...@google.com (2025-01-08)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M133. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: a reverted commit was detected after the merge request.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [133].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dm...@chromium.org (2025-01-08)

The broken optimization that lead to this bug was disabled by default ==> nothing to merge.

### ch...@google.com (2025-03-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/380487911)*
