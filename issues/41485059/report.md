# Security: Debug check failed: var.has_value(). in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [41485059](https://issues.chromium.org/issues/41485059) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Compiler>Turbofan |
| **Platforms** | Android, Linux, Mac, Windows |
| **Reporter** | je...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2023-12-18 |
| **Bounty** | $8,000.00 |

## Description

Title : Debug check failed: var.has_value(). in v8

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 91054
    - link: https://crrev.com/ce5999e86e234dbd7000989556567a69e1ecafcf 
- Commit Message

```
commit ce5999e86e234dbd7000989556567a69e1ecafcf
Author: Manos Koukoutos <manoskouk@chromium.org>
Date:   Mon Nov 20 12:56:04 2023 +0100

    [turboshaft][wasm] Enable loop peeling
    
    Bug: v8:14108
    Change-Id: I360809827d10781efae9354f6eb2354d29e827f3
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5033018
    Commit-Queue: Manos Koukoutos <manoskouk@chromium.org>
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#91054}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-91561/d8 --turboshaft-wasm --allow-natives-syntax poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/compiler/turboshaft/copying-phase.h, line 187
# Debug check failed: var.has_value().
#
#
#
#FailureMessage Object: 0x7fa123ffc380
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-91561/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7fa13b90fa33]
    /tmp/d8-linux-debug-v8-component-91561/libv8_libplatform.so(+0x1971d) [0x7fa13b8b671d]
    /tmp/d8-linux-debug-v8-component-91561/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x154) [0x7fa13b8efd74]
    /tmp/d8-linux-debug-v8-component-91561/libv8_libbase.so(+0x2b835) [0x7fa13b8ef835]
    /tmp/d8-linux-debug-v8-component-91561/libv8.so(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::MapToNewGraph<false>(v8::internal::compiler::turboshaft::OpIndex, int)+0x166) [0x7fa13b03fde6]
    /tmp/d8-linux-debug-v8-component-91561/libv8.so(v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::CloneAndInlineBlock(v8::internal::compiler::turboshaft::Block const*)+0x333) [0x7fa13b040403]
    /tmp/d8-linux-debug-v8-component-91561/libv8.so(v8::internal::compiler::turboshaft::BranchEliminationReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::ReduceGoto(v8::internal::compiler::turboshaft::Block*, bool)+0xc8) [0x7fa13b03ff28]
    /tmp/d8-linux-debug-v8-component-91561/libv8.so(v8::internal::compiler::turboshaft::VariableReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::ReduceGoto(v8::internal::compiler::turboshaft::Block*, bool)+0x1c) [0x7fa13b03f1bc]
    /tmp/d8-linux-debug-v8-component-91561/libv8.so(v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::AssembleOutputGraphGoto(v8::internal::compiler::turboshaft::GotoOp const&)+0x6a) [0x7fa13b03edaa]
    /tmp/d8-linux-debug-v8-component-91561/libv8.so(v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitOpNoMappingUpdate<false>(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::Block const*)+0x156) [0x7fa13b03e276]
    /tmp/d8-linux-debug-v8-component-91561/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitBlock<false>(v8::internal::compiler::turboshaft::Block const*)+0x420) [0x7fa13b091aa0]
    /tmp/d8-linux-debug-v8-component-91561/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitAllBlocks<false>()+0xe3) [0x7fa13b091583]
    /tmp/d8-linux-debug-v8-component-91561/libv8.so(void v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, true, v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer, v8::internal::compiler::turboshaft::TSReducerBase>>::VisitGraph<false>()+0xa7) [0x7fa13b021947]
    /tmp/d8-linux-debug-v8-component-91561/libv8.so(v8::internal::compiler::turboshaft::CopyingPhaseImpl<v8::internal::compiler::turboshaft::LateEscapeAnalysisReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::MemoryOptimizationReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::BranchEliminationReducer, v8::internal::compiler::turboshaft::LateLoadEliminationReducer, v8::internal::compiler::turboshaft::ValueNumberingReducer>::Run(v8::internal::Zone*)+0x11d) [0x7fa13b02176d]
    /tmp/d8-linux-debug-v8-component-91561/libv8.so(auto v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::turboshaft::WasmOptimizePhase>()+0xd0) [0x7fa13ae3c6e0]
    /tmp/d8-linux-debug-v8-component-91561/libv8.so(v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::CallDescriptor*)+0x8dd) [0x7fa13ae3b26d]
    /tmp/d8-linux-debug-v8-component-91561/libv8.so(v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmFeatures*)+0x2b1) [0x7fa13b093a91]
    /tmp/d8-linux-debug-v8-component-91561/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x72b) [0x7fa13a63847b]
    /tmp/d8-linux-debug-v8-component-91561/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x192) [0x7fa13a6378c2]
    /tmp/d8-linux-debug-v8-component-91561/libv8.so(+0x3a97a6a) [0x7fa13a697a6a]
    /tmp/d8-linux-debug-v8-component-91561/libv8.so(+0x3a972a5) [0x7fa13a6972a5]
    /tmp/d8-linux-debug-v8-component-91561/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xd3) [0x7fa13b8b5463]
    /tmp/d8-linux-debug-v8-component-91561/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0xc3) [0x7fa13b8b7cd3]
    /tmp/d8-linux-debug-v8-component-91561/libv8_libbase.so(+0x4a778) [0x7fa13b90e778]
    /lib/x86_64-linux-gnu/libc.so.6(+0x94ac3) [0x7fa136294ac3]
    /lib/x86_64-linux-gnu/libc.so.6(+0x126a40) [0x7fa136326a40]

```

## Other
Please note to include the flags `--turboshaft-wasm --allow-natives-syntax` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.1.0 - 12.2.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-91561.zip
2. Run: `d8 --turboshaft-wasm --allow-natives-syntax poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Jerry

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 3.2 KB)
- [poc_code.js](attachments/poc_code.js) (text/plain, 10.2 KB)

## Timeline

### je...@gmail.com (2023-12-18)

[Comment Deleted]

### [Deleted User] (2023-12-18)

[Empty comment from Monorail migration]

### me...@chromium.org (2023-12-18)

Thanks for the report. Passing over to the current v8 sheriff. I didn't upload this to Clusterfuzz as the PoC are rather complicated.

[Monorail components: Blink>JavaScript Blink>JavaScript>Compiler>Turbofan]

### je...@gmail.com (2023-12-19)

Uploading to clusterfuzz is better, you can use poc.js instead of poc_code.js

### am...@chromium.org (2023-12-19)

[Description Changed]

### je...@gmail.com (2023-12-19)

Note: please use debug d8 to run clusterfuzz

### cl...@chromium.org (2023-12-19)

Detailed Report: https://clusterfuzz.com/testcase?key=5857106538725376

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  var.has_value() in copying-phase.h
  v8::internal::compiler::turboshaft::OpIndex v8::internal::compiler::turboshaft::
  v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turbosh
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&revision=91590

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5857106538725376

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2023-12-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-12-19)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-12-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/9e997077e5c54ad8a8532e3fc2c39904e102c80a

commit 9e997077e5c54ad8a8532e3fc2c39904e102c80a
Author: Darius M <dmercadier@chromium.org>
Date: Tue Dec 19 13:36:46 2023

[turboshaft] Always skip unused operations

Two things were wrong:

 * CopyingPhase::InlineBlock did not skip Phis whose use-count was
   0. This lead to visiting Phis whose input had been removed from the
   graph.

 * [debug only] Operations with use-count of 0 were not always skipped
   when --turboshaft-opt-bisect was used, which could also lead to
   visiting operations with Invalid inputs.

Bug: v8:12781
Change-Id: I1a77658bb25adf72c6b9183896a7735710048cec
Fixed: chromium:1512481
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5132813
Auto-Submit: Darius Mercadier <dmercadier@chromium.org>
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
Cr-Commit-Position: refs/heads/main@{#91595}

[modify] https://crrev.com/9e997077e5c54ad8a8532e3fc2c39904e102c80a/src/compiler/turboshaft/copying-phase.h


### [Deleted User] (2023-12-19)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dm...@chromium.org (2023-12-19)

As far as Wasm is concerned, the impact is None because Wasm doesn't use Turboshaft by default.

However, I think that this might be an issue for Javascript, although exploiting this bug would be hard. Given that Turboshaft is enabled by default for Javascript, I think that we should at least backmerge to 121, and maybe consider backmerging to 120 as well.

### [Deleted User] (2023-12-19)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2023-12-20)

ClusterFuzz testcase 5857106538725376 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=91594:91595

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-12-20)

Merge review required: M121 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-20)

Merge review required: M120 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-20)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-20)

[Empty comment from Monorail migration]

### dm...@chromium.org (2023-12-22)

Replies to Comments 15 and 16:

1. Fixes a security issue. The severity is hard to estimate, but I think that we should at least backmerge to beta.
2. https://chromium-review.googlesource.com/c/v8/v8/+/5132813
3. yes
4. no
5. N/A
6. no

### am...@chromium.org (2023-12-27)

121 and 120 merges approved for https://crrev.com/c/5132813
please merge this fix to 12.1-lkgr and 12.0-lkgr at your earliest convenience (and before EOD Tuesday 2 January) so this fix can be included in the next scheduled updates of M120 Stable and M121 Beta. Thank you! 

### [Deleted User] (2024-01-01)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2024-01-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/d1f891b4bc0f232dcb2d7f1e1ada60071ef6983d

commit d1f891b4bc0f232dcb2d7f1e1ada60071ef6983d
Author: Darius M <dmercadier@chromium.org>
Date: Tue Dec 19 13:36:46 2023

Merged: [turboshaft] Always skip unused operations

Two things were wrong:

 * CopyingPhase::InlineBlock did not skip Phis whose use-count was
   0. This lead to visiting Phis whose input had been removed from the
   graph.

 * [debug only] Operations with use-count of 0 were not always skipped
   when --turboshaft-opt-bisect was used, which could also lead to
   visiting operations with Invalid inputs.

Bug: v8:12781, chromium:1512481
(cherry picked from commit 9e997077e5c54ad8a8532e3fc2c39904e102c80a)

Change-Id: I7b8d8863fe3599471893d95844f3c57feb2a55a8
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5155973
Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
Reviewed-by: Clemens Backes <clemensb@chromium.org>
Cr-Commit-Position: refs/branch-heads/12.0@{#26}
Cr-Branched-From: ed7b4caf1fb8184ad9e24346c84424055d4d430a-refs/heads/12.0.267@{#1}
Cr-Branched-From: 210e75b19db4352c9b78dce0bae11c2dc3077df4-refs/heads/main@{#90651}

[modify] https://crrev.com/d1f891b4bc0f232dcb2d7f1e1ada60071ef6983d/src/compiler/turboshaft/optimization-phase.h


### dm...@chromium.org (2024-01-02)

It looks like the gitwatcher for 12.1 is still broken, but the backmerge to 12.1 has also landed: https://chromium-review.googlesource.com/c/v8/v8/+/5148988
(I don't have permission to add a "merge-merged-12.1" label)

### da...@google.com (2024-01-02)

I think Git Watcher is breaking due to monorail preventing new labels from being created.

### am...@google.com (2024-01-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-01-03)

Congratulations Jerry! The Chrome VRP Panel has decided to award you $7,000 for this report + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us. Happy New Year! 

### am...@chromium.org (2024-01-03)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-04)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-04)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

 - M121, which branched on 2023-12-04 (Chromium branch: 6167, Chromium branch position: 1233107)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove the Merge-TBD-## label and replace it with a Merge-NA-## label (where ## corresponds to the milestone under evaluation). If a merge is necessary, please add the appropriate Merge-Request-## labels. If you're not sure, reach out to the relevant release manager (can be found at https://chromiumdash.appspot.com/schedule).

To learn more about the merge process, including how to land any required merges, see https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2024-01-04)

dear bot this was already merged to 121, adding merge-na-121 to cease nags 

### am...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1512481?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript, Blink>JavaScript>Compiler>Turbofan]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41485059)*
