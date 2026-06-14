# Security: Debug check failed: displacement == 0 in V8.

| Field | Value |
|-------|-------|
| **Issue ID** | [41493286](https://issues.chromium.org/issues/41493286) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turbofan |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2024-01-21 |
| **Bounty** | $8,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 91860
    - link: https://crrev.com/bed95642cb2f4d5e9dc490d5b58085b1f2a3c870 
- Commit Message

```
commit bed95642cb2f4d5e9dc490d5b58085b1f2a3c870
Author: Matthias Liedtke <mliedtke@chromium.org>
Date:   Tue Jan 16 13:53:10 2024 +0100

    [turboshaft][wasm] Stage all official instruction selections
    
    This stages the previously experimental instruction selections for
    wasm on:
    - ia32
    - arm
    - arm64
    
    Note that x86-64 was already staged prior to this CL.
    
    Bug: v8:14108
    Change-Id: Ie4957a2188c76588c8d1ef2a8f5d2f8cab524cf6
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5201025
    Reviewed-by: Manos Koukoutos <manoskouk@chromium.org>
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Auto-Submit: Matthias Liedtke <mliedtke@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#91860}

```

- Commit Info
    - Version: 91829
    - link: https://crrev.com/bc99a57e7888c81946d9479320f74ca911977478 
- Commit Message

```
commit bc99a57e7888c81946d9479320f74ca911977478
Author: Jakob Kummerow <jkummerow@chromium.org>
Date:   Fri Jan 12 21:56:22 2024 +0100

    [turboshaft][ia32] Instruction Selector part 3
    
    This now passes mjsunit/wasm/*.
    
    Bug: v8:12783
    Change-Id: I54008423601aaeb89e06e6e4f4df54a284a43120
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5191568
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#91829}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux32-debug-v8-component-91933/d8 --future --turboshaft-wasm-instruction-selection-staged --allow-natives-syntax poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/compiler/backend/ia32/instruction-selector-ia32.cc, line 1259
# Debug check failed: displacement == 0 (-1 vs. 0).
#
#
#
#FailureMessage Object: 0xe1dfa9c0
==== C stack trace ===============================

    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1f) [0xf7ed32ef]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libplatform.so(+0x16394) [0xf7e7f394]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0xf7) [0xf7eb2677]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(+0x27076) [0xf7eb2076]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x31) [0xf7eb26c1]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(+0x3c66996) [0xf7266996]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftAdapter>::VisitWord32AtomicStore(v8::internal::compiler::turboshaft::OpIndex)+0x45) [0xf7265f25]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftAdapter>::VisitNode(v8::internal::compiler::turboshaft::OpIndex)+0x1019) [0xf6d41629]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftAdapter>::VisitBlock(v8::internal::compiler::turboshaft::Block*)+0x624) [0xf6d38524]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftAdapter>::SelectInstructions()+0x8c4) [0xf6d37444]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::InstructionSelector::SelectInstructions()+0x49) [0xf6d503c9]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::turboshaft::InstructionSelectionPhase::Run(v8::internal::Zone*, v8::internal::compiler::CallDescriptor const*, v8::internal::compiler::Linkage*, v8::internal::CodeTracer*)+0x68a) [0xf77384ea]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(auto v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::turboshaft::InstructionSelectionPhase, v8::internal::compiler::CallDescriptor*&, v8::internal::compiler::Linkage*&, v8::internal::CodeTracer*&>(v8::internal::compiler::CallDescriptor*&, v8::internal::compiler::Linkage*&, v8::internal::CodeTracer*&)+0xe5) [0xf7121025]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::PipelineImpl::SelectInstructionsTurboshaft(v8::internal::compiler::Linkage*)+0xe0) [0xf711f290]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::CallDescriptor*)+0x8ae) [0xf711d76e]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmFeatures*)+0x317) [0xf73df427]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x684) [0xf68eb0f4]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x18a) [0xf68ea67a]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(+0x3348f92) [0xf6948f92]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(+0x3348809) [0xf6948809]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xcb) [0xf7e7dfdb]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0x98) [0xf7e80678]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(+0x46f0e) [0xf7ed1f0e]
    /lib/i386-linux-gnu/libc.so.6(+0x86c01) [0xf2c86c01]
    /lib/i386-linux-gnu/libc.so.6(+0x12375c) [0xf2d2375c]

```

## Other
Please note to include the flags `--future --turboshaft-wasm-instruction-selection-staged --allow-natives-syntax` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.2.0 - 12.2.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux32-debug/d8-linux32-debug-v8-component-91933.zip
2. Run: `d8 --future --turboshaft-wasm-instruction-selection-staged --allow-natives-syntax poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Jerry


# Debug check failed: g.ValueFitsIntoImmediate(displacement). in v8

I'm not sure if they are caused by the same vulnerability, but since the introduction point is the same, I will report it to you in the same report.
Please split as needed.

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux32-debug-v8-component-91933/d8 --future --allow-natives-syntax --turboshaft-wasm-instruction-selection-staged  poc.js
# OUTPUT ==============================================================

#
# Fatal error in ../../src/compiler/backend/ia32/instruction-selector-ia32.cc, line 1263
# Debug check failed: g.ValueFitsIntoImmediate(displacement).
#
#
#
#FailureMessage Object: 0xe87f39c0
==== C stack trace ===============================

    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1f) [0xf7f252ef]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libplatform.so(+0x16394) [0xf7ed1394]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0xf7) [0xf7f04677]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(+0x27076) [0xf7f04076]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x31) [0xf7f046c1]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(+0x3c669ec) [0xf72669ec]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftAdapter>::VisitWord32AtomicStore(v8::internal::compiler::turboshaft::OpIndex)+0x45) [0xf7265f25]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftAdapter>::VisitNode(v8::internal::compiler::turboshaft::OpIndex)+0x1019) [0xf6d41629]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftAdapter>::VisitBlock(v8::internal::compiler::turboshaft::Block*)+0x624) [0xf6d38524]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftAdapter>::SelectInstructions()+0x8c4) [0xf6d37444]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::InstructionSelector::SelectInstructions()+0x49) [0xf6d503c9]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::turboshaft::InstructionSelectionPhase::Run(v8::internal::Zone*, v8::internal::compiler::CallDescriptor const*, v8::internal::compiler::Linkage*, v8::internal::CodeTracer*)+0x68a) [0xf77384ea]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(auto v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::turboshaft::InstructionSelectionPhase, v8::internal::compiler::CallDescriptor*&, v8::internal::compiler::Linkage*&, v8::internal::CodeTracer*&>(v8::internal::compiler::CallDescriptor*&, v8::internal::compiler::Linkage*&, v8::internal::CodeTracer*&)+0xe5) [0xf7121025]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::PipelineImpl::SelectInstructionsTurboshaft(v8::internal::compiler::Linkage*)+0xe0) [0xf711f290]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::CallDescriptor*)+0x8ae) [0xf711d76e]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmFeatures*)+0x317) [0xf73df427]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x684) [0xf68eb0f4]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x18a) [0xf68ea67a]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(+0x3348f92) [0xf6948f92]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(+0x3348809) [0xf6948809]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xcb) [0xf7ecffdb]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0x98) [0xf7ed2678]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(+0x46f0e) [0xf7f23f0e]
    /lib/i386-linux-gnu/libc.so.6(+0x86c01) [0xf2c86c01]
    /lib/i386-linux-gnu/libc.so.6(+0x12375c) [0xf2d2375c]

```

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 3.6 KB)
- [poc_code.js](attachments/poc_code.js) (text/plain, 14.6 KB)
- [poc (1).js](attachments/poc (1).js) (text/plain, 3.4 KB)
- [poc_code (1).js](attachments/poc_code (1).js) (text/plain, 13.7 KB)
- [poc.js](attachments/poc_53164658.js) (text/plain, 3.6 KB)
- [poc_code.js](attachments/poc_code_53164659.js) (text/plain, 14.6 KB)
- [poc.js](attachments/poc_53164711.js) (text/plain, 3.4 KB)
- [poc_code.js](attachments/poc_code_53164712.js) (text/plain, 13.7 KB)
- [poc.js](attachments/poc_53164756.js) (text/plain, 3.0 KB)
- [poc_code.js](attachments/poc_code_53164757.js) (text/plain, 14.0 KB)

## Timeline

### je...@gmail.com (2024-01-21)

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 91860
    - link: https://crrev.com/bed95642cb2f4d5e9dc490d5b58085b1f2a3c870 
- Commit Message

```
commit bed95642cb2f4d5e9dc490d5b58085b1f2a3c870
Author: Matthias Liedtke <mliedtke@chromium.org>
Date:   Tue Jan 16 13:53:10 2024 +0100

    [turboshaft][wasm] Stage all official instruction selections
    
    This stages the previously experimental instruction selections for
    wasm on:
    - ia32
    - arm
    - arm64
    
    Note that x86-64 was already staged prior to this CL.
    
    Bug: v8:14108
    Change-Id: Ie4957a2188c76588c8d1ef2a8f5d2f8cab524cf6
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5201025
    Reviewed-by: Manos Koukoutos <manoskouk@chromium.org>
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Auto-Submit: Matthias Liedtke <mliedtke@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#91860}

```

- Commit Info
    - Version: 91829
    - link: https://crrev.com/bc99a57e7888c81946d9479320f74ca911977478 
- Commit Message

```
commit bc99a57e7888c81946d9479320f74ca911977478
Author: Jakob Kummerow <jkummerow@chromium.org>
Date:   Fri Jan 12 21:56:22 2024 +0100

    [turboshaft][ia32] Instruction Selector part 3
    
    This now passes mjsunit/wasm/*.
    
    Bug: v8:12783
    Change-Id: I54008423601aaeb89e06e6e4f4df54a284a43120
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5191568
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#91829}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux32-debug-v8-component-91933/d8 --future --turboshaft-wasm-instruction-selection-staged --allow-natives-syntax poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/compiler/backend/ia32/instruction-selector-ia32.cc, line 1259
# Debug check failed: displacement == 0 (-1 vs. 0).
#
#
#
#FailureMessage Object: 0xe1dfa9c0
==== C stack trace ===============================

    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1f) [0xf7ed32ef]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libplatform.so(+0x16394) [0xf7e7f394]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0xf7) [0xf7eb2677]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(+0x27076) [0xf7eb2076]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x31) [0xf7eb26c1]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(+0x3c66996) [0xf7266996]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftAdapter>::VisitWord32AtomicStore(v8::internal::compiler::turboshaft::OpIndex)+0x45) [0xf7265f25]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftAdapter>::VisitNode(v8::internal::compiler::turboshaft::OpIndex)+0x1019) [0xf6d41629]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftAdapter>::VisitBlock(v8::internal::compiler::turboshaft::Block*)+0x624) [0xf6d38524]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftAdapter>::SelectInstructions()+0x8c4) [0xf6d37444]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::InstructionSelector::SelectInstructions()+0x49) [0xf6d503c9]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::turboshaft::InstructionSelectionPhase::Run(v8::internal::Zone*, v8::internal::compiler::CallDescriptor const*, v8::internal::compiler::Linkage*, v8::internal::CodeTracer*)+0x68a) [0xf77384ea]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(auto v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::turboshaft::InstructionSelectionPhase, v8::internal::compiler::CallDescriptor*&, v8::internal::compiler::Linkage*&, v8::internal::CodeTracer*&>(v8::internal::compiler::CallDescriptor*&, v8::internal::compiler::Linkage*&, v8::internal::CodeTracer*&)+0xe5) [0xf7121025]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::PipelineImpl::SelectInstructionsTurboshaft(v8::internal::compiler::Linkage*)+0xe0) [0xf711f290]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::CallDescriptor*)+0x8ae) [0xf711d76e]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmFeatures*)+0x317) [0xf73df427]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x684) [0xf68eb0f4]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x18a) [0xf68ea67a]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(+0x3348f92) [0xf6948f92]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(+0x3348809) [0xf6948809]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xcb) [0xf7e7dfdb]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0x98) [0xf7e80678]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(+0x46f0e) [0xf7ed1f0e]
    /lib/i386-linux-gnu/libc.so.6(+0x86c01) [0xf2c86c01]
    /lib/i386-linux-gnu/libc.so.6(+0x12375c) [0xf2d2375c]

```

## Other
Please note to include the flags `--future --turboshaft-wasm-instruction-selection-staged --allow-natives-syntax` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.2.0 - 12.2.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux32-debug/d8-linux32-debug-v8-component-91933.zip
2. Run: `d8 --future --turboshaft-wasm-instruction-selection-staged --allow-natives-syntax poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Jerry

### je...@gmail.com (2024-01-21)

Please pay attention to using 32-bit d8 debug to reproduce. In addition, the reason why I mentioned two introduction points is because bed95642cb2f4d5e9dc490d5b58085b1f2a3c870 officially de-experimentalized the vulnerability, so it is not an experimental vulnerability and was introduced more than 7 days ago. It should meet the requirements of v8 reward.

### [Deleted User] (2024-01-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2024-01-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5095504716693504.

### cl...@chromium.org (2024-01-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2024-01-23)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript]

### cl...@chromium.org (2024-01-23)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/bed95642cb2f4d5e9dc490d5b58085b1f2a3c870 ([turboshaft][wasm] Stage all official instruction selections).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### je...@gmail.com (2024-01-23)

# Debug check failed: g.ValueFitsIntoImmediate(displacement). in v8

I'm not sure if they are caused by the same vulnerability, but since the introduction point is the same, I will report it to you in the same report.
Please split as needed.

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux32-debug-v8-component-91933/d8 --future --allow-natives-syntax --turboshaft-wasm-instruction-selection-staged  poc.js
# OUTPUT ==============================================================

#
# Fatal error in ../../src/compiler/backend/ia32/instruction-selector-ia32.cc, line 1263
# Debug check failed: g.ValueFitsIntoImmediate(displacement).
#
#
#
#FailureMessage Object: 0xe87f39c0
==== C stack trace ===============================

    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1f) [0xf7f252ef]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libplatform.so(+0x16394) [0xf7ed1394]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0xf7) [0xf7f04677]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(+0x27076) [0xf7f04076]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x31) [0xf7f046c1]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(+0x3c669ec) [0xf72669ec]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftAdapter>::VisitWord32AtomicStore(v8::internal::compiler::turboshaft::OpIndex)+0x45) [0xf7265f25]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftAdapter>::VisitNode(v8::internal::compiler::turboshaft::OpIndex)+0x1019) [0xf6d41629]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftAdapter>::VisitBlock(v8::internal::compiler::turboshaft::Block*)+0x624) [0xf6d38524]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftAdapter>::SelectInstructions()+0x8c4) [0xf6d37444]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::InstructionSelector::SelectInstructions()+0x49) [0xf6d503c9]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::turboshaft::InstructionSelectionPhase::Run(v8::internal::Zone*, v8::internal::compiler::CallDescriptor const*, v8::internal::compiler::Linkage*, v8::internal::CodeTracer*)+0x68a) [0xf77384ea]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(auto v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::turboshaft::InstructionSelectionPhase, v8::internal::compiler::CallDescriptor*&, v8::internal::compiler::Linkage*&, v8::internal::CodeTracer*&>(v8::internal::compiler::CallDescriptor*&, v8::internal::compiler::Linkage*&, v8::internal::CodeTracer*&)+0xe5) [0xf7121025]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::PipelineImpl::SelectInstructionsTurboshaft(v8::internal::compiler::Linkage*)+0xe0) [0xf711f290]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::CallDescriptor*)+0x8ae) [0xf711d76e]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmFeatures*)+0x317) [0xf73df427]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x684) [0xf68eb0f4]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x18a) [0xf68ea67a]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(+0x3348f92) [0xf6948f92]
    /tmp/d8-linux32-debug-v8-component-91933/libv8.so(+0x3348809) [0xf6948809]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xcb) [0xf7ecffdb]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0x98) [0xf7ed2678]
    /tmp/d8-linux32-debug-v8-component-91933/libv8_libbase.so(+0x46f0e) [0xf7f23f0e]
    /lib/i386-linux-gnu/libc.so.6(+0x86c01) [0xf2c86c01]
    /lib/i386-linux-gnu/libc.so.6(+0x12375c) [0xf2d2375c]

```


### cl...@chromium.org (2024-01-23)

[Empty comment from Monorail migration]

[Monorail components: -Blink>JavaScript Blink>JavaScript>Compiler>Turbofan]

### ke...@chromium.org (2024-01-24)

Tentatively setting severity to High. This can be adjusted if assessment finds there isn't a risk of memory corruption.

### [Deleted User] (2024-01-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2024-01-24)

Detailed Report: https://clusterfuzz.com/testcase?key=5095504716693504

Fuzzer: None
Job Type: linux32_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  displacement == 0 in instruction-selector-ia32.cc
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux32_d8_dbg&range=91859:91860

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5095504716693504

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### [Deleted User] (2024-01-24)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-24)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-24)

[Empty comment from Monorail migration]

### je...@gmail.com (2024-01-25)

# Debug check failed: element_size_log2 == 0 (\x2 vs. 0).

I'm not sure if they are caused by the same vulnerability, but since the introduction point is the same, I will report it to you in the same report.
Please split as needed.

```
# Fatal error in ../../src/compiler/backend/ia32/instruction-selector-ia32.cc, line 1257
# Debug check failed: element_size_log2 == 0 (\x2 vs. 0).
#
#
#
```



### je...@gmail.com (2024-01-25)

[Comment Deleted]

### ha...@google.com (2024-01-25)

[Empty comment from Monorail migration]

### je...@gmail.com (2024-01-25)

Hello, any update? :)

### jk...@chromium.org (2024-01-25)

Fix in flight: https://chromium-review.googlesource.com/c/v8/v8/+/5237267

#16 is the same issue.

### gi...@appspot.gserviceaccount.com (2024-01-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/25bf4a691f829827085cb470013f4d11a1a416fd

commit 25bf4a691f829827085cb470013f4d11a1a416fd
Author: Jakob Kummerow <jkummerow@chromium.org>
Date: Thu Jan 25 14:06:03 2024

[wasm][turboshaft][ia32] Fix certain atomic stores

The MachineOperatorReducer can create the situation that an atomic
store has both an index and a displacement, which the ia32
instruction selector didn't support.

Fixed: chromium:1520312
Change-Id: I291dcf2915c9ecd9002c0e0ddc5a46b3bf5db158
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5237267
Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
Cr-Commit-Position: refs/heads/main@{#92006}

[add] https://crrev.com/25bf4a691f829827085cb470013f4d11a1a416fd/test/mjsunit/regress/wasm/regress-crbug-1520312.js
[modify] https://crrev.com/25bf4a691f829827085cb470013f4d11a1a416fd/src/compiler/backend/ia32/instruction-selector-ia32.cc
[modify] https://crrev.com/25bf4a691f829827085cb470013f4d11a1a416fd/src/compiler/turboshaft/machine-optimization-reducer.h


### cl...@chromium.org (2024-01-25)

ClusterFuzz testcase 5095504716693504 is verified as fixed in https://clusterfuzz.com/revisions?job=linux32_d8_dbg&range=92005:92006

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2024-01-25)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-25)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-26)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

 - M122, which branched on 2024-01-22 (Chromium branch: 6261, Chromium branch position: 1250580)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove the Merge-TBD-## label and replace it with a Merge-NA-## label (where ## corresponds to the milestone under evaluation). If a merge is necessary, please add the appropriate Merge-Request-## labels. If you're not sure, reach out to the relevant release manager (can be found at https://chromiumdash.appspot.com/schedule).

To learn more about the merge process, including how to land any required merges, see https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jk...@chromium.org (2024-01-29)

We have Canary coverage now. Requesting merge.

### [Deleted User] (2024-01-29)

Merge review required: M122 is already shipping to beta.

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
Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jk...@chromium.org (2024-01-29)

1. We want to start Finching the "Turboshaft" compiler redesign. This patch fixes a bug that's blocking the Finch experiment on 32-bit x86 platforms.
2. https://chromium-review.googlesource.com/c/v8/v8/+/5237267
3. Yes (123.0.6267.0). Waiting for that was the only reason I didn't request the merge last week.
4. Yes (new feature), yes (behind Finch flag), not yet (we would like to start experimenting).
5. N/A
6. N/A

### am...@chromium.org (2024-01-29)

[Description Changed]

### am...@chromium.org (2024-01-30)

M122 merge approved for https://crrev.com/c/5237267, please merge to 12.2-lkgr at your earliest convenience 

### gi...@appspot.gserviceaccount.com (2024-01-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/7d7592c2218a22aa323a91fc630832c069a18740

commit 7d7592c2218a22aa323a91fc630832c069a18740
Author: Jakob Kummerow <jkummerow@chromium.org>
Date: Thu Jan 25 14:06:03 2024

Merged: [wasm][turboshaft][ia32] Fix certain atomic stores

The MachineOperatorReducer can create the situation that an atomic
store has both an index and a displacement, which the ia32
instruction selector didn't support.

Fixed: chromium:1520312
(cherry picked from commit 25bf4a691f829827085cb470013f4d11a1a416fd)

Change-Id: I245de625bb0a1a1dc671049d521fd288c2a00826
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5253189
Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
Cr-Commit-Position: refs/branch-heads/12.2@{#20}
Cr-Branched-From: 6eb5a9616aa6f8c705217aeb7c7ab8c037a2f676-refs/heads/12.2.281@{#1}
Cr-Branched-From: 44cf56d850167c6988522f8981730462abc04bcc-refs/heads/main@{#91934}

[add] https://crrev.com/7d7592c2218a22aa323a91fc630832c069a18740/test/mjsunit/regress/wasm/regress-crbug-1520312.js
[modify] https://crrev.com/7d7592c2218a22aa323a91fc630832c069a18740/src/compiler/backend/ia32/instruction-selector-ia32.cc
[modify] https://crrev.com/7d7592c2218a22aa323a91fc630832c069a18740/src/compiler/turboshaft/machine-optimization-reducer.h


### [Deleted User] (2024-01-31)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jk...@chromium.org (2024-01-31)

#32: This is not relevant for M120.

### [Deleted User] (2024-01-31)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2024-02-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-02)

Congratulations Jerry! The Chrome VRP Panel has decided to award you $7,000 for this report of renderer memory corruptions + $1,000 bisect bonus. Thank you for your effort and reporting this issue to us! 

### am...@google.com (2024-02-02)

[Empty comment from Monorail migration]

### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/1520312?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### vo...@google.com (2024-02-07)

Introduced in M122, so marking as not applicable to M114 and M120 LTS.

### pe...@google.com (2024-05-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41493286)*
