# Security: Debug check failed: displacement == 0 . in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [41486150](https://issues.chromium.org/issues/41486150) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turbofan, Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2023-12-21 |
| **Bounty** | $8,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 91281
    - link: https://crrev.com/06df8123409d9c0c23aaa66ab11bbeeb6ba29a5d 
- Commit Message

```
commit 06df8123409d9c0c23aaa66ab11bbeeb6ba29a5d
Author: Manos Koukoutos <manoskouk@chromium.org>
Date:   Thu Nov 30 16:10:30 2023 +0100

    [turboshaft][wasm] Set up separate flags for instruction selection
    
    Introduce a "staging" flag for architectures where we plan to run a
    trial on Turboshaft instruction selection (currently x64 only), and
    an "experimental" flag for the rest.
    
    Bug: v8:14108, chromium:1496282
    Change-Id: Iee7b9baf45acf3a5478f45489d7a3f6baaa23248
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5075618
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
    Commit-Queue: Manos Koukoutos <manoskouk@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#91281}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-91616/d8 --turboshaft-wasm --turboshaft-wasm-instruction-selection-staged --wasm-tiering-budget=1000 poc.js
# OUTPUT ==============================================================
wasm-function[0]:0x106: RuntimeError: memory access out of bounds
RuntimeError: memory access out of bounds
    at wasm://wasm/dc6e19be:wasm-function[0]:0x106
    at poc.js:5:1



#
# Fatal error in ../../src/compiler/backend/x64/instruction-selector-x64.cc, line 1445
# Debug check failed: displacement == 0 (2147483647 vs. 0).
#
#
#
#FailureMessage Object: 0x7f3493ffd3c0
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-91616/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f34b8656ac3]
    /tmp/d8-linux-debug-v8-component-91616/libv8_libplatform.so(+0x1971d) [0x7f34b85fd71d]
    /tmp/d8-linux-debug-v8-component-91616/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x17e) [0x7f34b8636e0e]
    /tmp/d8-linux-debug-v8-component-91616/libv8_libbase.so(+0x2b8a5) [0x7f34b86368a5]
    /tmp/d8-linux-debug-v8-component-91616/libv8.so(+0x43665da) [0x7f34b7b665da]
    /tmp/d8-linux-debug-v8-component-91616/libv8.so(v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftAdapter>::VisitWord64AtomicStore(v8::internal::compiler::turboshaft::OpIndex)+0x79) [0x7f34b7b66879]
    /tmp/d8-linux-debug-v8-component-91616/libv8.so(v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftAdapter>::VisitBlock(v8::internal::compiler::turboshaft::Block*)+0x37a) [0x7f34b769384a]
    /tmp/d8-linux-debug-v8-component-91616/libv8.so(v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftAdapter>::SelectInstructions()+0x986) [0x7f34b7692a16]
    /tmp/d8-linux-debug-v8-component-91616/libv8.so(v8::internal::compiler::turboshaft::InstructionSelectionPhase::Run(v8::internal::Zone*, v8::internal::compiler::CallDescriptor const*, v8::internal::compiler::Linkage*, v8::internal::CodeTracer*)+0x5bf) [0x7f34b7ef5e1f]
    /tmp/d8-linux-debug-v8-component-91616/libv8.so(auto v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::turboshaft::InstructionSelectionPhase, v8::internal::compiler::CallDescriptor*&, v8::internal::compiler::Linkage*&, v8::internal::CodeTracer*&>(v8::internal::compiler::CallDescriptor*&, v8::internal::compiler::Linkage*&, v8::internal::CodeTracer*&)+0xca) [0x7f34b7a4761a]
    /tmp/d8-linux-debug-v8-component-91616/libv8.so(v8::internal::compiler::PipelineImpl::SelectInstructionsTurboshaft(v8::internal::compiler::Linkage*)+0xc8) [0x7f34b7a3a778]
    /tmp/d8-linux-debug-v8-component-91616/libv8.so(v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::CallDescriptor*)+0x959) [0x7f34b7a44359]
    /tmp/d8-linux-debug-v8-component-91616/libv8.so(v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmFeatures*)+0x2b1) [0x7f34b7c9c1e1]
    /tmp/d8-linux-debug-v8-component-91616/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x72b) [0x7f34b72420cb]
    /tmp/d8-linux-debug-v8-component-91616/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x192) [0x7f34b7241512]
    /tmp/d8-linux-debug-v8-component-91616/libv8.so(+0x3aa16ca) [0x7f34b72a16ca]
    /tmp/d8-linux-debug-v8-component-91616/libv8.so(+0x3aa0f05) [0x7f34b72a0f05]
    /tmp/d8-linux-debug-v8-component-91616/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xd3) [0x7f34b85fc463]
    /tmp/d8-linux-debug-v8-component-91616/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0xc3) [0x7f34b85fecd3]
    /tmp/d8-linux-debug-v8-component-91616/libv8_libbase.so(+0x4a808) [0x7f34b8655808]
    /lib/x86_64-linux-gnu/libc.so.6(+0x94ac3) [0x7f34b2e94ac3]
    /lib/x86_64-linux-gnu/libc.so.6(+0x126a40) [0x7f34b2f26a40]

```

## Other
Please note to include the flags `--turboshaft-wasm --turboshaft-wasm-instruction-selection-staged --wasm-tiering-budget=1000` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.1.0 - 12.2.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-91616.zip
2. Run: `d8 --turboshaft-wasm --turboshaft-wasm-instruction-selection-staged --wasm-tiering-budget=1000 poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Jerry

If further bisecting is performed using --turboshaft-wasm-instruction-selection, the results obtained are as follows:

- Commit Info
    - Version: 91249
    - link: https://crrev.com/33dab337eaafb4c795adf82f4efd62e86bc164ab 
- Commit Message

```
commit 33dab337eaafb4c795adf82f4efd62e86bc164ab
Author: Darius M <dmercadier@chromium.org>
Date:   Wed Nov 29 12:43:21 2023 +0100

    [turboshaft] Normalize loads whose base is addition and index is invalid
    
    This make the instruction selector generate better code (because the
    addition is computed with a complex memory operand rather than before
    the load).
    
    Additionally, this makes the TS graphs more normalized, which could be
    good in particular for LoadElimination and StoreStoreElimination, and
    any alias analysis we may want to do.
    
    Bug: v8:12783
    Change-Id: I08f75d83c972f2fd60c064fce2ab944f0541f7ec
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5068362
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org>
    Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#91249}

## Attachments

- [poc_code.js](attachments/poc_code.js) (text/plain, 15.8 KB)
- [poc.js](attachments/poc.js) (text/plain, 3.2 KB)

## Timeline

### je...@gmail.com (2023-12-21)

[Comment Deleted]

### [Deleted User] (2023-12-21)

[Empty comment from Monorail migration]

### je...@gmail.com (2023-12-21)

If further bisecting is performed using --turboshaft-wasm-instruction-selection, the results obtained are as follows:

- Commit Info
    - Version: 91249
    - link: https://crrev.com/33dab337eaafb4c795adf82f4efd62e86bc164ab 
- Commit Message

```
commit 33dab337eaafb4c795adf82f4efd62e86bc164ab
Author: Darius M <dmercadier@chromium.org>
Date:   Wed Nov 29 12:43:21 2023 +0100

    [turboshaft] Normalize loads whose base is addition and index is invalid
    
    This make the instruction selector generate better code (because the
    addition is computed with a complex memory operand rather than before
    the load).
    
    Additionally, this makes the TS graphs more normalized, which could be
    good in particular for LoadElimination and StoreStoreElimination, and
    any alias analysis we may want to do.
    
    Bug: v8:12783
    Change-Id: I08f75d83c972f2fd60c064fce2ab944f0541f7ec
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5068362
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org>
    Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#91249}

```


### cl...@chromium.org (2023-12-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6546378304454656.

### cl...@chromium.org (2023-12-21)

Detailed Report: https://clusterfuzz.com/testcase?key=6546378304454656

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  displacement == 0 in instruction-selector-x64.cc
  void v8::internal::compiler::VisitStoreCommon<v8::internal::compiler::Turboshaft
  v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftA
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=91280:91281

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6546378304454656

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### bb...@google.com (2023-12-21)

sending over to v8 sherriff, dcheck failure. setting provisional high. 

[Monorail components: Blink>JavaScript]

### [Deleted User] (2023-12-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-12-22)

[Empty comment from Monorail migration]

### dm...@chromium.org (2023-12-22)

[Empty comment from Monorail migration]

[Monorail components: -Blink>JavaScript Blink>JavaScript>Compiler>Turbofan]

### dm...@chromium.org (2023-12-22)

This bug only impacts Wasm Turboshaft (since Javascript doesn't have atomic loads), which is still disabled by default => impact = none.

(fix is ready but I need someone to review it, so it probably won't land until January)

[Monorail components: Blink>JavaScript>WebAssembly]

### je...@gmail.com (2024-01-04)

Friendly Ping :)

### cl...@chromium.org (2024-01-09)

ClusterFuzz testcase 6546378304454656 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=91722:91723

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### dm...@chromium.org (2024-01-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2024-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/0918f3eafb5a33480a5b735d8d20c29519824d57

commit 0918f3eafb5a33480a5b735d8d20c29519824d57
Author: Darius M <dmercadier@chromium.org>
Date: Thu Jan 11 10:52:17 2024

[turboshaft][x64] Make sure Load/Store offset=0 for atomic Loads/Stores

The instruction selector assumes that the offset of Loads and Stores
in 0. We thus now normalize atomic Load/Stores on x64 during
LoadStoreSimplificationReducer.

Drive-by: when the Index is constant but cannot be merged into the
offset because it would overflow 32 bits, we now instead merge the
offset into the index (which is a WordPtr, while the offset is a
Word32), to avoid emitting an addition in the instruction selector.

Bug: v8:12783
Change-Id: I80d33b83ac210ae54ad5a0ef17f120c7b6953027
Fixed: chromium:1513580
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5148172
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Auto-Submit: Darius Mercadier <dmercadier@chromium.org>
Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
Cr-Commit-Position: refs/heads/main@{#91778}

[modify] https://crrev.com/0918f3eafb5a33480a5b735d8d20c29519824d57/src/compiler/turboshaft/code-elimination-and-simplification-phase.cc
[modify] https://crrev.com/0918f3eafb5a33480a5b735d8d20c29519824d57/src/compiler/turboshaft/load-store-simplification-reducer.h
[modify] https://crrev.com/0918f3eafb5a33480a5b735d8d20c29519824d57/src/compiler/turboshaft/machine-optimization-reducer.h
[add] https://crrev.com/0918f3eafb5a33480a5b735d8d20c29519824d57/test/mjsunit/wasm/turboshaft/regress-crbug-1513580.js


### [Deleted User] (2024-01-11)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2024-01-18)

[Description Changed]

### am...@google.com (2024-01-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-01-19)

Congratulations Jerry! The Chrome VRP Panel has decided to award you $7,000 for this report + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2024-01-20)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-20)

This issue was migrated from crbug.com/chromium/1513580?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript>Compiler>Turbofan, Blink>JavaScript>WebAssembly]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-04-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

### cl...@chromium.org (2026-01-08)

Removing `Clusterfuzz-ignore` hotlist from some old bugs as it's preventing Clusterfuzz from filing similar bugs.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41486150)*
