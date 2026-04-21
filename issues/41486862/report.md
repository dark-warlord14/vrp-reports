# Security: Memory Corrupt in V8 Webassembly

| Field | Value |
|-------|-------|
| **Issue ID** | [41486862](https://issues.chromium.org/issues/41486862) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turbofan, Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2023-12-26 |
| **Bounty** | $7,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 90457
    - link: https://crrev.com/63405a66d43737599afec36381a9b0bb13dbb484 
- Commit Message

```
commit 63405a66d43737599afec36381a9b0bb13dbb484
Author: Manos Koukoutos <manoskouk@chromium.org>
Date:   Tue Oct 17 11:40:49 2023 +0200

    [turboshaft][wasm] Speculative inlining
    
    For each call_ref call site, if the call site is marked as inlinable,
    introduce a speculative inlined direct call at that site. This does
    not yet introduce multiple inlined direct calls.
    Drive-by: Change the signature of `InlineWasmCall` and handle null
    `InliningTree` in `should_inline`.
    
    Bug: v8:14108
    Change-Id: I3b42f25ca2c1a297842230a3e85d3e141e1b8c45
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4946031
    Commit-Queue: Manos Koukoutos <manoskouk@chromium.org>
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#90457}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-release-v8-component-91641/d8 --allow-natives-syntax --turboshaft-wasm --wasm-tiering-budget=1000 poc.js
# OUTPUT ==============================================================
Received signal 11 SEGV_MAPERR 7f7e44004f57

==== C stack trace ===============================

 [0x555d3878d817]
 [0x7f7e2e042520]
 [0x555d37eaf942]
 [0x555d37ed33c8]
 [0x555d37eb7630]
 [0x555d37eac91f]
 [0x555d37eab6f5]
 [0x555d37eab1b7]
 [0x555d381f791b]
 [0x555d383250cc]
 [0x555d37e54c3b]
 [0x555d37e54342]
 [0x555d37e7ff71]
 [0x555d37e7f947]
 [0x555d3878ec2b]
 [0x555d38791b2e]
 [0x555d3878acce]
 [0x7f7e2e094ac3]
 [0x7f7e2e126a40]
[end of stack trace]

```

## Other
Please note to include the flags `--allow-natives-syntax --turboshaft-wasm --wasm-tiering-budget=1000` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.0.0 - 12.2.0

REPRODUCTION CASE
1. Download release v8 from: gs://v8-asan/linux-release/d8-linux-release-v8-component-91641.zip
2. Run: `d8 --allow-natives-syntax --turboshaft-wasm --wasm-tiering-budget=1000 poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Jerry


Debug Check will bisect to another location, maybe it's more accurate.

## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 90931
    - link: https://crrev.com/c89fb798454d076f3d404185678ac5a71fd09c28 
- Commit Message

```
commit c89fb798454d076f3d404185678ac5a71fd09c28
Author: Nico Hartmann <nicohartmann@chromium.org>
Date:   Tue Nov 14 15:04:29 2023 +0100

    [compiler] Generalize InstructionSelectorT for Turboshaft (part 19)
    
    Support more atomic and simd128 instructions for
    --turboshaft-wasm-instruction-selection.
    
    Bug: v8:12783
    Change-Id: If2a28a423714164bdd41532f4b285abc4080b76b
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5001637
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
    Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#90931}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-91641/d8 --allow-natives-syntax --turboshaft-wasm --wasm-tiering-budget=1000 poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/compiler/turboshaft/graph.h, line 590
# Debug check failed: i.valid().
#
#
#
#FailureMessage Object: 0x7fd921ff8aa0
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-91641/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7fd95dc42ac3]
    /tmp/d8-linux-debug-v8-component-91641/libv8_libplatform.so(+0x1971d) [0x7fd95dbe971d]
    /tmp/d8-linux-debug-v8-component-91641/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x17e) [0x7fd95dc22e0e]
    /tmp/d8-linux-debug-v8-component-91641/libv8_libbase.so(+0x2b8a5) [0x7fd95dc228a5]
    /tmp/d8-linux-debug-v8-component-91641/libv8.so(v8::internal::compiler::turboshaft::Graph::Get(v8::internal::compiler::turboshaft::OpIndex)+0x60) [0x7fd95c6033e0]
    /tmp/d8-linux-debug-v8-component-91641/libv8.so(v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::TSReducerBase>>::ReducePhi(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x70) [0x7fd95c8f1ac0]
    /tmp/d8-linux-debug-v8-component-91641/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::CallRef(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const&, v8::internal::Signature<v8::internal::wasm::ValueType> const*, unsigned int, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*)+0xf06) [0x7fd95c950c56]
    /tmp/d8-linux-debug-v8-component-91641/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallRefImpl(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::TraceLine*, v8::internal::wasm::WasmOpcode)+0x203) [0x7fd95c94fa53]
    /tmp/d8-linux-debug-v8-component-91641/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallRef(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::WasmOpcode)+0x8b) [0x7fd95c90323b]
    /tmp/d8-linux-debug-v8-component-91641/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeFunctionBody()+0x203) [0x7fd95c8e6473]
    /tmp/d8-linux-debug-v8-component-91641/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::Decode()+0x22f) [0x7fd95c8e0eef]
    /tmp/d8-linux-debug-v8-component-91641/libv8.so(v8::internal::wasm::BuildTSGraph(v8::internal::AccountingAllocator*, v8::internal::wasm::WasmFeatures, v8::internal::wasm::WasmModule const*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::turboshaft::Graph&, v8::internal::wasm::FunctionBody const&, v8::internal::wasm::WireBytesStorage const*, v8::internal::wasm::AssumptionsJournal*, v8::internal::ZoneVector<v8::internal::WasmInliningPosition>*, int)+0x259) [0x7fd95c8e07e9]
    /tmp/d8-linux-debug-v8-component-91641/libv8.so(v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::CallDescriptor*)+0x79a) [0x7fd95d037efa]
    /tmp/d8-linux-debug-v8-component-91641/libv8.so(v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmFeatures*)+0x2b1) [0x7fd95d28ff41]
    /tmp/d8-linux-debug-v8-component-91641/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x72b) [0x7fd95c8363fb]
    /tmp/d8-linux-debug-v8-component-91641/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x192) [0x7fd95c835842]
    /tmp/d8-linux-debug-v8-component-91641/libv8.so(+0x3a959fa) [0x7fd95c8959fa]
    /tmp/d8-linux-debug-v8-component-91641/libv8.so(+0x3a95235) [0x7fd95c895235]
    /tmp/d8-linux-debug-v8-component-91641/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xd3) [0x7fd95dbe8463]
    /tmp/d8-linux-debug-v8-component-91641/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0xc3) [0x7fd95dbeacd3]
    /tmp/d8-linux-debug-v8-component-91641/libv8_libbase.so(+0x4a808) [0x7fd95dc41808]
    /lib/x86_64-linux-gnu/libc.so.6(+0x94ac3) [0x7fd958494ac3]
    /lib/x86_64-linux-gnu/libc.so.6(+0x126a40) [0x7fd958526a40]

```

## Attachments

- [poc_code.js](attachments/poc_code.js) (text/plain, 14.4 KB)
- [poc.js](attachments/poc.js) (text/plain, 3.2 KB)
- [poc.js](attachments/poc.js) (text/plain, 1.3 KB)

## Timeline

### je...@gmail.com (2023-12-26)

[Comment Deleted]

### [Deleted User] (2023-12-26)

[Empty comment from Monorail migration]

### je...@gmail.com (2023-12-26)

[Comment Deleted]

### je...@gmail.com (2023-12-26)

Debug Check will bisect to another location, maybe it's more accurate.

## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 90931
    - link: https://crrev.com/c89fb798454d076f3d404185678ac5a71fd09c28 
- Commit Message

```
commit c89fb798454d076f3d404185678ac5a71fd09c28
Author: Nico Hartmann <nicohartmann@chromium.org>
Date:   Tue Nov 14 15:04:29 2023 +0100

    [compiler] Generalize InstructionSelectorT for Turboshaft (part 19)
    
    Support more atomic and simd128 instructions for
    --turboshaft-wasm-instruction-selection.
    
    Bug: v8:12783
    Change-Id: If2a28a423714164bdd41532f4b285abc4080b76b
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5001637
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
    Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#90931}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-91641/d8 --allow-natives-syntax --turboshaft-wasm --wasm-tiering-budget=1000 poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/compiler/turboshaft/graph.h, line 590
# Debug check failed: i.valid().
#
#
#
#FailureMessage Object: 0x7fd921ff8aa0
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-91641/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7fd95dc42ac3]
    /tmp/d8-linux-debug-v8-component-91641/libv8_libplatform.so(+0x1971d) [0x7fd95dbe971d]
    /tmp/d8-linux-debug-v8-component-91641/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x17e) [0x7fd95dc22e0e]
    /tmp/d8-linux-debug-v8-component-91641/libv8_libbase.so(+0x2b8a5) [0x7fd95dc228a5]
    /tmp/d8-linux-debug-v8-component-91641/libv8.so(v8::internal::compiler::turboshaft::Graph::Get(v8::internal::compiler::turboshaft::OpIndex)+0x60) [0x7fd95c6033e0]
    /tmp/d8-linux-debug-v8-component-91641/libv8.so(v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::SelectLoweringReducer, v8::internal::compiler::turboshaft::DataViewReducer, v8::internal::compiler::turboshaft::VariableReducer, v8::internal::compiler::turboshaft::RequiredOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase>>, false, v8::internal::compiler::turboshaft::TSReducerBase>>::ReducePhi(v8::base::Vector<v8::internal::compiler::turboshaft::OpIndex const>, v8::internal::compiler::turboshaft::RegisterRepresentation)+0x70) [0x7fd95c8f1ac0]
    /tmp/d8-linux-debug-v8-component-91641/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::CallRef(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const&, v8::internal::Signature<v8::internal::wasm::ValueType> const*, unsigned int, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*)+0xf06) [0x7fd95c950c56]
    /tmp/d8-linux-debug-v8-component-91641/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallRefImpl(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::TraceLine*, v8::internal::wasm::WasmOpcode)+0x203) [0x7fd95c94fa53]
    /tmp/d8-linux-debug-v8-component-91641/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallRef(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::WasmOpcode)+0x8b) [0x7fd95c90323b]
    /tmp/d8-linux-debug-v8-component-91641/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeFunctionBody()+0x203) [0x7fd95c8e6473]
    /tmp/d8-linux-debug-v8-component-91641/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::Decode()+0x22f) [0x7fd95c8e0eef]
    /tmp/d8-linux-debug-v8-component-91641/libv8.so(v8::internal::wasm::BuildTSGraph(v8::internal::AccountingAllocator*, v8::internal::wasm::WasmFeatures, v8::internal::wasm::WasmModule const*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::turboshaft::Graph&, v8::internal::wasm::FunctionBody const&, v8::internal::wasm::WireBytesStorage const*, v8::internal::wasm::AssumptionsJournal*, v8::internal::ZoneVector<v8::internal::WasmInliningPosition>*, int)+0x259) [0x7fd95c8e07e9]
    /tmp/d8-linux-debug-v8-component-91641/libv8.so(v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::CallDescriptor*)+0x79a) [0x7fd95d037efa]
    /tmp/d8-linux-debug-v8-component-91641/libv8.so(v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmFeatures*)+0x2b1) [0x7fd95d28ff41]
    /tmp/d8-linux-debug-v8-component-91641/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x72b) [0x7fd95c8363fb]
    /tmp/d8-linux-debug-v8-component-91641/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x192) [0x7fd95c835842]
    /tmp/d8-linux-debug-v8-component-91641/libv8.so(+0x3a959fa) [0x7fd95c8959fa]
    /tmp/d8-linux-debug-v8-component-91641/libv8.so(+0x3a95235) [0x7fd95c895235]
    /tmp/d8-linux-debug-v8-component-91641/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xd3) [0x7fd95dbe8463]
    /tmp/d8-linux-debug-v8-component-91641/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0xc3) [0x7fd95dbeacd3]
    /tmp/d8-linux-debug-v8-component-91641/libv8_libbase.so(+0x4a808) [0x7fd95dc41808]
    /lib/x86_64-linux-gnu/libc.so.6(+0x94ac3) [0x7fd958494ac3]
    /lib/x86_64-linux-gnu/libc.so.6(+0x126a40) [0x7fd958526a40]

```

### cl...@chromium.org (2023-12-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5254995555844096.

### hc...@google.com (2023-12-26)

Reassigning to v8 sherriff. Provisional Foundin and severity.

### hc...@google.com (2023-12-26)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### [Deleted User] (2023-12-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-12-26)

Detailed Report: https://clusterfuzz.com/testcase?key=5254995555844096

Fuzzer: None
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x52d100014417
Crash State:
  bool v8::internal::compiler::turboshaft::Operation::Is<v8::internal::compiler::t
  v8::internal::compiler::turboshaft::underlying_operation<v8::internal::compiler:
  v8::internal::compiler::turboshaft::RequiredOptimizationReducer<v8::internal::co
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8&range=90456:90457

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5254995555844096

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


The recommended severity (Security_Severity-Medium) is different from what was assigned to the bug. Please double check the accuracy of the assigned severity.

### [Deleted User] (2023-12-27)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-27)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ts...@chromium.org (2023-12-27)

Assigning per suspect CL.

### ts...@chromium.org (2023-12-27)

(since V8 roll brought in only https://chromium-review.googlesource.com/c/v8/v8/+/4946031)

### cl...@chromium.org (2024-01-09)

ClusterFuzz testcase 5254995555844096 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8&range=91722:91723

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### je...@gmail.com (2024-01-09)

Hello, clusterfuzz seems to have made a wrong verify. Since this commit (https://chromium.googlesource.com/v8/v8/+/058a45d7e4268375eaa26d7e4a7c2cd9607d289b) modified the opcode, this issue was accidentally marked as fixed, but it obviously has not been fixed.
I can still reproduce it with other pocs.


d8-linux-release-cache/d8-linux-release-v8-component-91726/d8 --wasm-tiering-budget=1000 --future poc.js     
Received signal 11 SEGV_MAPERR 7f7330004f57

==== C stack trace ===============================

 [0x5576cac97fd7]
 [0x7f731bc42520]
 [0x5576ca3b82d2]
 [0x5576ca3dc578]
 [0x5576ca3c02f1]
 [0x5576ca3b528f]
 [0x5576ca3b4065]
 [0x5576ca3b3b27]
 [0x5576ca70250b]
 [0x5576ca82fe2c]
 [0x5576ca35d4cb]
 [0x5576ca35cbd2]
 [0x5576ca388641]
 [0x5576ca388027]
 [0x5576cac9933b]
 [0x5576cac9c1de]
 [0x5576cac9564e]
 [0x7f731bc94ac3]
 [0x7f731bd26a40]
[end of stack trace]


### cl...@chromium.org (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ma...@chromium.org (2024-01-09)

[Empty comment from Monorail migration]

### dm...@chromium.org (2024-01-10)

[Empty comment from Monorail migration]

[Monorail components: -Blink>JavaScript Blink>JavaScript>Compiler>Turbofan Blink>JavaScript>WebAssembly]

### ma...@chromium.org (2024-01-10)

[Empty comment from Monorail migration]

### ma...@chromium.org (2024-01-10)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2024-01-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/bd9ce10affdbdb3a0c45e1be0fc45678551de950

commit bd9ce10affdbdb3a0c45e1be0fc45678551de950
Author: Manos Koukoutos <manoskouk@chromium.org>
Date: Wed Jan 10 12:34:05 2024

[turboshaft][wasm] Only add phi inputs from reachable inlined blocks

Bug: chromium:1514304
Change-Id: Iec30d3139d2def0c4b0f5c14adda6c6caaa126cd
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5184134
Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
Commit-Queue: Manos Koukoutos <manoskouk@chromium.org>
Cr-Commit-Position: refs/heads/main@{#91755}

[add] https://crrev.com/bd9ce10affdbdb3a0c45e1be0fc45678551de950/test/mjsunit/regress/wasm/regress-1514304.js
[modify] https://crrev.com/bd9ce10affdbdb3a0c45e1be0fc45678551de950/src/wasm/turboshaft-graph-interface.cc


### ma...@chromium.org (2024-01-11)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-11)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-11)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-11)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M120. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M121. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: M120 is already shipping to stable.

Merge review required: M121 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [120, 121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-12)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=1514304&entry.364066060=External&entry.958145677=Android&entry.958145677=Chrome&entry.958145677=Fuchsia&entry.958145677=Linux&entry.958145677=Mac&entry.958145677=Windows&entry.958145677=Lacros&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>JavaScript>Compiler>Turbofan,Blink>JavaScript>WebAssembly&entry.975983575=manoskouk@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2024-01-12)

I do not believe this requires either backmerging or a postmortem. It only manifests with experimental wasm features enabled (Turboshaft).

### cl...@chromium.org (2024-01-12)

Setting impact none based on #28. This should also avoid more action from the bots.

### cl...@chromium.org (2024-01-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2024-01-18)

[Description Changed]

### wf...@chromium.org (2024-01-18)

hi manoskouk@ re: https://crbug.com/chromium/1514304#c28 can you highlight where it shows this is experimental (to help security shepherd and VRP panel going fowrad), as normally I would expect d8 to print a warning message to this effect?

### je...@gmail.com (2024-01-18)

Hi, turboshaft wasm has been removed from the experimental flag here. I think what the developer meant by experimental is that it is not stable. This can be rewarded because the turboshaft wasm has entered the head finch. 

### je...@gmail.com (2024-01-18)

You can print the output with this flag on the version of d8 where I submitted the vulnerability, which will not output experimental. 

### ma...@chromium.org (2024-01-19)

Apologies for the confusion: Turboshaft wasm is staged behind --future and is not experimental. What I meant is that it is not available without 
experimental flags enabled in Chrome, so is should not require backmerging or a postmortem.

### je...@gmail.com (2024-01-20)

Thanks for the explanation, as far as I know the flag in --future satisfies the requirements of Chrome v8 vrp. 

### am...@google.com (2024-01-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-01-25)

Congratulations Jerry! The Chrome VRP Panel has decided to award you $7,000 for this report + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2024-01-27)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-27)

This issue was migrated from crbug.com/chromium/1514304?no_tracker_redirect=1

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
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41486862)*
