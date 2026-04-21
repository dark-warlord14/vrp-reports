# Security: Debug check failed: use->opcode() == IrOpcode::kLoopExitEffect || use->opcode() == IrOpcode::kLoopExitValue.

| Field | Value |
|-------|-------|
| **Issue ID** | [40948441](https://issues.chromium.org/issues/40948441) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Linux, Mac |
| **Reporter** | je...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2023-12-04 |
| **Bounty** | $7,000.00 |

## Description

Title : Debug check failed: use->opcode() == IrOpcode::kLoopExitEffect || use->opcode() == IrOpcode::kLoopExitValue. in v8

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 90887
    - link: https://crrev.com/d5d40dadd4cfe63573ec79956c744d59ffe4900d 
- Commit Message

```
commit d5d40dadd4cfe63573ec79956c744d59ffe4900d
Author: Thibaud Michaud <thibaudm@chromium.org>
Date:   Mon Nov 13 12:44:36 2023 +0100

    [wasm][exnref] Implement try-table in TurboFan
    
    R=clemensb@chromium.org
    
    Bug: v8:14398
    Change-Id: I74411c64528ecfab14d6450f9fa8fa76843cfcf0
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5023768
    Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
    Reviewed-by: Clemens Backes <clemensb@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#90887}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-91313/d8 --experimental-wasm-exnref poc.js
# OUTPUT ==============================================================
0,97,115,109,1,0,0,0,1,158,1,10,80,0,95,0,80,0,95,4,120,0,99,106,0,127,1,109,0,80,0,94,125,1,80,0,94,119,1,80,0,94,126,1,78,3,80,0,94,100,3,1,96,3,127,127,127,1,127,96,14,125,125,125,125,125,125,125,125,125,125,125,125,125,125,14,125,125,125,125,125,125,125,125,125,125,125,125,125,125,78,1,96,14,127,127,127,127,127,127,127,127,127,127,127,127,127,127,14,100,0,100,0,100,0,100,0,112,110,126,99,108,99,0,110,100,1,127,127,127,78,1,96,0,0,96,14,99,108,100,0,100,0,100,0,100,0,100,0,100,0,100,0,100,0,100,0,100,0,100,0,100,0,100,0,0,96,0,0,3,5,4,6,7,8,9,4,5,1,112,1,4,4,5,4,1,1,16,32,13,3,1,0,11,7,8,1,4,109,97,105,110,0,0,9,20,1,6,0,65,0,11,112,4,210,0,11,210,1,11,210,2,11,210,3,11,12,1,1,10,229,17,4,169,13,9,1,99,0,1,100,9,1,123,1,111,1,100,108,1,124,1,100,3,1,99,0,1,100,110,210,3,33,4,3,125,3,127,68,114,233,140,69,125,204,194,12,68,134,2,188,22,148,171,143,62,98,68,161,206,10,224,205,29,21,123,68,80,195,198,207,34,163,146,53,68,230,126,91,226,5,200,85,30,98,66,222,146,221,131,156,241,197,144,141,127,121,121,121,254,27,0,154,52,65,191,221,222,175,2,13,0,68,149,168,37,153,97,78,218,232,98,252,16,0,66,209,254,160,238,225,227,169,163,191,127,254,36,2,254,253,3,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,254,27,0,154,52,65,145,138,137,247,120,13,0,68,236,154,121,72,31,41,154,150,252,16,0,208,108,251,0,0,251,0,0,251,0,0,251,0,0,251,0,0,251,0,0,251,0,0,251,0,0,251,0,0,251,0,0,251,0,0,251,0,0,251,0,0,2,10,31,10,0,26,26,26,26,26,26,26,26,26,26,26,26,26,26,2,64,2,64,2,64,31,9,2,2,1,2,0,11,12,2,11,12,1,11,12,0,11,11,12,0,11,252,16,0,65,228,153,168,224,120,65,128,131,190,150,122,108,65,0,253,15,253,89,0,159,62,7,252,16,0,65,192,213,166,144,2,65,203,170,170,207,123,65,215,216,255,190,4,65,212,237,206,187,4,65,148,145,148,136,126,65,176,221,228,143,3,65,196,224,189,213,122,65,171,251,141,233,6,65,255,139,194,181,123,65,236,157,201,211,2,65,192,226,142,171,1,208,8,20,8,26,26,26,26,26,26,26,26,26,26,26,26,26,26,68,90,118,99,11,112,186,223,39,98,254,47,1,154,52,11,65,159,156,226,162,122,65,165,153,213,29,108,65,166,184,202,157,2,65,221,176,139,137,4,108,65,212,151,154,168,7,108,65,200,222,220,112,65,248,159,251,131,122,108,65,223,175,156,128,124,65,153,133,236,181,124,254,39,0,208,160,1,65,156,161,148,162,2,65,221,220,141,115,254,39,0,208,160,1,108,65,190,140,135,234,6,65,144,255,176,191,3,254,39,0,80,108,108,108,108,65,136,217,144,235,4,65,226,138,185,128,6,65,155,170,181,235,122,65,139,206,173,183,125,65,173,172,183,249,2,254,39,0,208,160,1,254,39,0,208,160,1,65,255,204,140,219,126,65,223,154,175,224,120,254,39,0,208,160,1,254,39,0,208,160,1,254,39,0,208,160,1,254,39,0,208,160,1,65,172,177,243,50,65,147,142,140,233,4,254,39,0,208,160,1,254,39,0,208,160,1,108,65,192,178,147,184,127,65,175,164,247,136,2,254,39,0,208,160,1,65,250,128,164,215,123,65,197,133,239,254,125,65,161,134,168,102,65,241,212,209,191,7,254,39,0,208,160,1,254,39,0,208,160,1,254,39,0,208,160,1,65,250,142,153,188,123,65,147,145,165,187,122,65,178,151,214,157,123,254,39,0,159,62,254,39,0,208,160,1,65,133,151,201,137,122,65,173,142,249,250,5,108,65,166,216,65,65,182,135,198,189,127,108,65,232,181,255,228,123,65,227,172,223,134,121,65,150,212,129,173,7,108,108,108,108,254,39,0,208,160,1,65,254,159,212,204,3,65,141,194,230,153,124,108,65,157,179,250,137,2,252,16,0,108,108,252,16,0,108,254,39,0,208,160,1,254,39,0,208,160,1,254,39,0,208,160,1,252,16,0,254,39,0,208,160,1,252,16,0,254,39,0,208,160,1,252,16,0,254,39,0,208,160,1,108,252,16,0,108,251,9,2,0,252,16,0,251,11,2,11,252,1,251,28,251,23,4,251,22,108,33,7,252,16,0,65,20,111,251,7,3,33,9,252,16,0,252,16,0,252,16,0,252,16,0,252,16,0,252,16,0,252,16,0,65,143,214,253,251,121,65,141,133,167,11,108,65,200,163,145,164,127,65,186,196,241,176,120,108,65,131,189,188,217,3,108,65,200,160,238,228,4,65,248,189,197,131,6,65,221,246,195,200,126,108,108,65,152,144,184,221,124,65,197,128,162,197,0,65,254,210,191,141,7,111,111,108,65,231,217,140,238,7,65,165,224,213,187,123,111,108,108,108,65,212,151,250,108,65,181,138,160,142,120,111,65,192,151,241,129,122,65,187,142,134,155,123,111,65,251,160,202,202,6,65,225,132,229,231,122,111,111,111,65,207,233,165,234,7,65,220,171,129,162,120,111,111,108,65,255,229,164,159,120,65,181,230,195,220,123,111,65,236,226,165,237,124,65,166,176,234,109,111,65,154,187,137,220,120,65,184,170,230,231,7,111,111,65,201,224,143,189,121,65,157,132,135,159,1,111,65,228,164,149,178,120,65,236,184,232,208,121,111,252,16,0,111,111,252,16,0,111,252,16,0,111,111,111,252,16,0,111,252,16,0,111,108,252,16,0,108,65,241,233,207,249,7,65,136,190,209,141,2,108,65,129,154,170,170,123,65,241,194,210,130,3,108,65,148,211,148,183,6,108,65,191,178,192,225,126,65,156,160,161,252,126,65,171,183,253,110,108,108,65,148,201,242,161,123,65,131,230,173,215,5,65,132,216,165,130,4,108,108,108,65,233,205,202,166,4,65,201,155,157,151,7,108,108,108,108,65,149,127,108,108,109,208,3,251,23,107,251,23,107,251,23,107,251,23,2,65,231,244,204,194,123,65,165,216,167,255,3,108,65,184,237,162,176,127,65,204,150,248,227,4,108,65,213,189,152,134,5,108,65,143,210,211,149,127,65,217,215,202,222,122,65,161,221,207,129,6,108,108,65,252,181,151,155,124,65,205,191,204,173,3,65,155,193,185,147,127,108,108,108,65,181,233,252,201,3,65,217,221,217,169,120,108,108,108,108,65,201,136,186,247,1,65,150,208,161,239,120,108,65,250,175,196,146,2,65,171,161,225,44,108,65,141,242,214,138,126,108,65,168,198,226,235,5,65,250,196,238,202,2,65,158,218,154,211,2,65,128,160,232,136,3,108,108,108,65,212,133,212,183,127,65,141,163,178,150,7,65,211,212,158,226,120,108,108,108,65,255,186,167,188,1,65,237,142,165,144,2,108,108,108,108,65,151,133,201,172,7,65,170,133,209,203,124,108,65,198,0,108,65,222,129,133,191,6,65,207,227,211,166,2,108,65,228,130,195,204,123,65,139,159,128,231,125,65,170,160,191,186,122,108,108,108,65,153,172,241,164,7,65,156,156,241,129,127,65,166,240,159,192,1,108,108,65,191,193,240,198,125,65,185,136,160,137,123,65,135,196,232,176,127,65,131,198,173,201,4,108,108,108,108,65,184,154,148,134,3,108,108,65,253,141,201,133,126,103,103,103,103,103,103,103,103,103,103,103,65,200,166,132,141,1,103,103,103,103,103,103,103,103,103,103,103,103,103,103,103,103,103,103,103,113,103,103,103,103,103,103,103,103,103,103,103,103,103,103,103,103,103,103,108,108,108,108,208,1,251,2,1,3,251,0,1,251,2,1,1,65,139,159,163,201,0,208,109,251,0,1,251,2,1,1,65,214,149,196,71,208,109,251,0,1,251,2,1,1,65,148,216,135,128,123,208,109,251,0,1,251,2,1,1,65,192,190,150,210,123,208,109,251,0,1,251,2,1,1,65,156,197,229,248,4,208,109,251,0,1,251,2,1,1,65,154,132,205,175,7,208,109,251,0,1,251,2,1,1,251,23,1,251,2,1,1,251,22,106,33,11,65,135,253,171,225,122,11,110,1,12,127,67,28,255,167,139,67,121,51,191,18,67,149,148,199,21,67,28,70,41,247,67,231,54,208,155,208,110,251,23,1,251,2,1,1,251,23,2,65,251,251,243,148,1,208,2,65,224,148,247,167,125,65,229,229,212,175,123,251,17,2,2,67,134,78,191,231,67,237,149,207,164,67,49,144,125,172,67,108,119,238,91,67,137,106,57,182,67,131,211,62,178,67,162,8,151,220,67,17,92,31,101,67,196,15,23,2,11,178,3,3,7,127,1,100,8,4,127,208,112,251,22,8,33,21,208,106,251,22,0,208,110,251,22,0,251,0,0,251,0,0,208,112,66,133,226,0,180,65,151,159,210,154,121,66,240,192,155,233,212,225,158,166,128,127,66,251,204,204,227,204,173,238,214,247,0,254,73,3,148,169,2,180,152,141,67,202,36,57,203,150,168,251,28,251,23,2,251,23,1,251,2,1,1,251,23,1,251,2,1,1,251,23,1,251,2,1,1,65,211,193,135,156,127,66,167,139,250,158,228,252,239,145,89,66,181,231,241,217,240,205,158,253,164,127,254,73,0,148,233,2,65,212,236,149,227,7,66,170,189,193,225,214,239,165,221,14,66,185,179,176,146,144,248,212,138,183,127,254,73,2,148,169,2,65,161,227,139,212,7,66,249,253,136,215,139,230,198,209,94,66,132,221,182,185,192,168,209,153,171,127,254,73,0,133,169,2,90,251,28,208,0,208,110,251,23,107,251,23,107,251,23,107,251,23,107,251,23,107,251,23,107,251,23,107,251,23,107,251,1,1,65,224,166,129,165,122,65,217,150,225,158,125,108,65,252,223,207,230,1,65,249,248,151,84,108,108,65,235,0,65,229,175,133,244,5,65,187,222,207,161,120,108,108,65,150,246,198,215,124,65,252,166,233,206,6,108,108,108,65,224,224,159,240,1,65,150,172,166,153,2,108,65,162,146,134,150,6,65,148,134,177,234,6,65,169,227,203,2,65,175,131,253,185,125,108,108,108,65,0,253,15,253,31,3,208,110,251,23,0,251,23,110,251,23,2,65,186,220,160,171,127,251,11,2,96,108,108,65,224,213,145,16,66,130,253,129,216,221,175,206,224,230,0,66,158,234,207,201,226,190,242,184,49,254,73,3,148,169,2,65,242,221,175,133,1,66,176,149,244,215,139,211,249,248,100,66,179,179,142,152,194,174,147,192,196,0,254,73,0,148,1,90,11,21,6,1,100,6,1,127,1,99,1,2,99,113,1,125,14,127,210,0,33,0,11,11,63,1,1,60,148,214,121,65,131,123,210,221,127,176,139,240,213,245,82,93,220,209,170,119,109,171,69,252,120,97,112,245,156,30,99,138,212,236,158,85,71,25,112,106,67,43,253,182,133,31,206,105,142,63,10,151,79,94,230,161,49,124,131,85


#
# Fatal error in ../../src/compiler/wasm-loop-peeling.cc, line 66
# Debug check failed: use->opcode() == IrOpcode::kLoopExitEffect || use->opcode() == IrOpcode::kLoopExitValue.
#
#
#
#FailureMessage Object: 0x7f50f8ff75a0
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f51346ebc73]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(+0x19add) [0x7f5134692add]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x154) [0x7f51346cbd14]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(+0x2b7d5) [0x7f51346cb7d5]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::PeelWasmLoop(v8::internal::compiler::Node*, v8::internal::ZoneUnorderedSet<v8::internal::compiler::Node*, v8::base::hash<v8::internal::compiler::Node*>, std::__Cr::equal_to<v8::internal::compiler::Node*>>*, v8::internal::compiler::Graph*, v8::internal::compiler::CommonOperatorBuilder*, v8::internal::Zone*, v8::internal::compiler::SourcePositionTable*, v8::internal::compiler::NodeOriginTable*)+0x968) [0x7f5133ef9b98]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::WasmLoopPeelingPhase::Run(v8::internal::compiler::PipelineData*, v8::internal::Zone*, std::__Cr::vector<v8::internal::compiler::WasmLoopInfo, std::__Cr::allocator<v8::internal::compiler::WasmLoopInfo>>*)+0x180) [0x7f5133c56800]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(auto v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::WasmLoopPeelingPhase, std::__Cr::vector<v8::internal::compiler::WasmLoopInfo, std::__Cr::allocator<v8::internal::compiler::WasmLoopInfo>>*&>(std::__Cr::vector<v8::internal::compiler::WasmLoopInfo, std::__Cr::allocator<v8::internal::compiler::WasmLoopInfo>>*&)+0x85) [0x7f5133c470d5]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::Pipeline::GenerateCodeForWasmFunction(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::compiler::CallDescriptor*, v8::internal::ZoneVector<v8::internal::WasmInliningPosition>*, v8::internal::wasm::WasmFeatures*)+0x523) [0x7f5133c44e83]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::ExecuteTurbofanWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x573) [0x7f5133ec7373]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x81e) [0x7f5133446fee]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x192) [0x7f5133446342]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(+0x3aa594a) [0x7f51334a594a]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(+0x3aa5185) [0x7f51334a5185]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xd3) [0x7f5134691823]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0xc3) [0x7f5134694213]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(+0x4a629) [0x7f51346ea629]
    /lib/x86_64-linux-gnu/libc.so.6(+0x94ac3) [0x7f512f094ac3]
    /lib/x86_64-linux-gnu/libc.so.6(+0x126a40) [0x7f512f126a40]

```

## Other
Please note to include the flags `--experimental-wasm-exnref` for clusterfuzz classification.
Please use poc.js for clusterfuzz reproduction. 
poc1.js is the corresponding wasm pseudocode. Please combine it with poc1.js for analysis.


VERSION
Tested on v8 version: 12.1.0 - 12.1.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-91313.zip
2. Run: `d8 --experimental-wasm-exnref poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Jerry

I uploaded the correct poc, please re-run clusterfuzz using this poc, remember to add the  --experimental-wasm-exnref flag

## Attachments

- [poc1.js](attachments/poc1.js) (text/plain, 33.0 KB)
- [poc.js](attachments/poc.js) (text/plain, 9.0 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [poc.js](attachments/poc.js) (text/plain, 9.0 KB)
- [poc1.js](attachments/poc1.js) (text/plain, 33.0 KB)

## Timeline

### [Deleted User] (2023-12-04)

[Empty comment from Monorail migration]

### je...@gmail.com (2023-12-04)

Title : Debug check failed: use->opcode() == IrOpcode::kLoopExitEffect || use->opcode() == IrOpcode::kLoopExitValue. in v8

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 90887
    - link: https://crrev.com/d5d40dadd4cfe63573ec79956c744d59ffe4900d 
- Commit Message

```
commit d5d40dadd4cfe63573ec79956c744d59ffe4900d
Author: Thibaud Michaud <thibaudm@chromium.org>
Date:   Mon Nov 13 12:44:36 2023 +0100

    [wasm][exnref] Implement try-table in TurboFan
    
    R=clemensb@chromium.org
    
    Bug: v8:14398
    Change-Id: I74411c64528ecfab14d6450f9fa8fa76843cfcf0
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5023768
    Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
    Reviewed-by: Clemens Backes <clemensb@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#90887}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-91313/d8 --experimental-wasm-exnref poc.js
# OUTPUT ==============================================================
0,97,115,109,1,0,0,0,1,158,1,10,80,0,95,0,80,0,95,4,120,0,99,106,0,127,1,109,0,80,0,94,125,1,80,0,94,119,1,80,0,94,126,1,78,3,80,0,94,100,3,1,96,3,127,127,127,1,127,96,14,125,125,125,125,125,125,125,125,125,125,125,125,125,125,14,125,125,125,125,125,125,125,125,125,125,125,125,125,125,78,1,96,14,127,127,127,127,127,127,127,127,127,127,127,127,127,127,14,100,0,100,0,100,0,100,0,112,110,126,99,108,99,0,110,100,1,127,127,127,78,1,96,0,0,96,14,99,108,100,0,100,0,100,0,100,0,100,0,100,0,100,0,100,0,100,0,100,0,100,0,100,0,100,0,0,96,0,0,3,5,4,6,7,8,9,4,5,1,112,1,4,4,5,4,1,1,16,32,13,3,1,0,11,7,8,1,4,109,97,105,110,0,0,9,20,1,6,0,65,0,11,112,4,210,0,11,210,1,11,210,2,11,210,3,11,12,1,1,10,229,17,4,169,13,9,1,99,0,1,100,9,1,123,1,111,1,100,108,1,124,1,100,3,1,99,0,1,100,110,210,3,33,4,3,125,3,127,68,114,233,140,69,125,204,194,12,68,134,2,188,22,148,171,143,62,98,68,161,206,10,224,205,29,21,123,68,80,195,198,207,34,163,146,53,68,230,126,91,226,5,200,85,30,98,66,222,146,221,131,156,241,197,144,141,127,121,121,121,254,27,0,154,52,65,191,221,222,175,2,13,0,68,149,168,37,153,97,78,218,232,98,252,16,0,66,209,254,160,238,225,227,169,163,191,127,254,36,2,254,253,3,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,254,27,0,154,52,65,145,138,137,247,120,13,0,68,236,154,121,72,31,41,154,150,252,16,0,208,108,251,0,0,251,0,0,251,0,0,251,0,0,251,0,0,251,0,0,251,0,0,251,0,0,251,0,0,251,0,0,251,0,0,251,0,0,251,0,0,2,10,31,10,0,26,26,26,26,26,26,26,26,26,26,26,26,26,26,2,64,2,64,2,64,31,9,2,2,1,2,0,11,12,2,11,12,1,11,12,0,11,11,12,0,11,252,16,0,65,228,153,168,224,120,65,128,131,190,150,122,108,65,0,253,15,253,89,0,159,62,7,252,16,0,65,192,213,166,144,2,65,203,170,170,207,123,65,215,216,255,190,4,65,212,237,206,187,4,65,148,145,148,136,126,65,176,221,228,143,3,65,196,224,189,213,122,65,171,251,141,233,6,65,255,139,194,181,123,65,236,157,201,211,2,65,192,226,142,171,1,208,8,20,8,26,26,26,26,26,26,26,26,26,26,26,26,26,26,68,90,118,99,11,112,186,223,39,98,254,47,1,154,52,11,65,159,156,226,162,122,65,165,153,213,29,108,65,166,184,202,157,2,65,221,176,139,137,4,108,65,212,151,154,168,7,108,65,200,222,220,112,65,248,159,251,131,122,108,65,223,175,156,128,124,65,153,133,236,181,124,254,39,0,208,160,1,65,156,161,148,162,2,65,221,220,141,115,254,39,0,208,160,1,108,65,190,140,135,234,6,65,144,255,176,191,3,254,39,0,80,108,108,108,108,65,136,217,144,235,4,65,226,138,185,128,6,65,155,170,181,235,122,65,139,206,173,183,125,65,173,172,183,249,2,254,39,0,208,160,1,254,39,0,208,160,1,65,255,204,140,219,126,65,223,154,175,224,120,254,39,0,208,160,1,254,39,0,208,160,1,254,39,0,208,160,1,254,39,0,208,160,1,65,172,177,243,50,65,147,142,140,233,4,254,39,0,208,160,1,254,39,0,208,160,1,108,65,192,178,147,184,127,65,175,164,247,136,2,254,39,0,208,160,1,65,250,128,164,215,123,65,197,133,239,254,125,65,161,134,168,102,65,241,212,209,191,7,254,39,0,208,160,1,254,39,0,208,160,1,254,39,0,208,160,1,65,250,142,153,188,123,65,147,145,165,187,122,65,178,151,214,157,123,254,39,0,159,62,254,39,0,208,160,1,65,133,151,201,137,122,65,173,142,249,250,5,108,65,166,216,65,65,182,135,198,189,127,108,65,232,181,255,228,123,65,227,172,223,134,121,65,150,212,129,173,7,108,108,108,108,254,39,0,208,160,1,65,254,159,212,204,3,65,141,194,230,153,124,108,65,157,179,250,137,2,252,16,0,108,108,252,16,0,108,254,39,0,208,160,1,254,39,0,208,160,1,254,39,0,208,160,1,252,16,0,254,39,0,208,160,1,252,16,0,254,39,0,208,160,1,252,16,0,254,39,0,208,160,1,108,252,16,0,108,251,9,2,0,252,16,0,251,11,2,11,252,1,251,28,251,23,4,251,22,108,33,7,252,16,0,65,20,111,251,7,3,33,9,252,16,0,252,16,0,252,16,0,252,16,0,252,16,0,252,16,0,252,16,0,65,143,214,253,251,121,65,141,133,167,11,108,65,200,163,145,164,127,65,186,196,241,176,120,108,65,131,189,188,217,3,108,65,200,160,238,228,4,65,248,189,197,131,6,65,221,246,195,200,126,108,108,65,152,144,184,221,124,65,197,128,162,197,0,65,254,210,191,141,7,111,111,108,65,231,217,140,238,7,65,165,224,213,187,123,111,108,108,108,65,212,151,250,108,65,181,138,160,142,120,111,65,192,151,241,129,122,65,187,142,134,155,123,111,65,251,160,202,202,6,65,225,132,229,231,122,111,111,111,65,207,233,165,234,7,65,220,171,129,162,120,111,111,108,65,255,229,164,159,120,65,181,230,195,220,123,111,65,236,226,165,237,124,65,166,176,234,109,111,65,154,187,137,220,120,65,184,170,230,231,7,111,111,65,201,224,143,189,121,65,157,132,135,159,1,111,65,228,164,149,178,120,65,236,184,232,208,121,111,252,16,0,111,111,252,16,0,111,252,16,0,111,111,111,252,16,0,111,252,16,0,111,108,252,16,0,108,65,241,233,207,249,7,65,136,190,209,141,2,108,65,129,154,170,170,123,65,241,194,210,130,3,108,65,148,211,148,183,6,108,65,191,178,192,225,126,65,156,160,161,252,126,65,171,183,253,110,108,108,65,148,201,242,161,123,65,131,230,173,215,5,65,132,216,165,130,4,108,108,108,65,233,205,202,166,4,65,201,155,157,151,7,108,108,108,108,65,149,127,108,108,109,208,3,251,23,107,251,23,107,251,23,107,251,23,2,65,231,244,204,194,123,65,165,216,167,255,3,108,65,184,237,162,176,127,65,204,150,248,227,4,108,65,213,189,152,134,5,108,65,143,210,211,149,127,65,217,215,202,222,122,65,161,221,207,129,6,108,108,65,252,181,151,155,124,65,205,191,204,173,3,65,155,193,185,147,127,108,108,108,65,181,233,252,201,3,65,217,221,217,169,120,108,108,108,108,65,201,136,186,247,1,65,150,208,161,239,120,108,65,250,175,196,146,2,65,171,161,225,44,108,65,141,242,214,138,126,108,65,168,198,226,235,5,65,250,196,238,202,2,65,158,218,154,211,2,65,128,160,232,136,3,108,108,108,65,212,133,212,183,127,65,141,163,178,150,7,65,211,212,158,226,120,108,108,108,65,255,186,167,188,1,65,237,142,165,144,2,108,108,108,108,65,151,133,201,172,7,65,170,133,209,203,124,108,65,198,0,108,65,222,129,133,191,6,65,207,227,211,166,2,108,65,228,130,195,204,123,65,139,159,128,231,125,65,170,160,191,186,122,108,108,108,65,153,172,241,164,7,65,156,156,241,129,127,65,166,240,159,192,1,108,108,65,191,193,240,198,125,65,185,136,160,137,123,65,135,196,232,176,127,65,131,198,173,201,4,108,108,108,108,65,184,154,148,134,3,108,108,65,253,141,201,133,126,103,103,103,103,103,103,103,103,103,103,103,65,200,166,132,141,1,103,103,103,103,103,103,103,103,103,103,103,103,103,103,103,103,103,103,103,113,103,103,103,103,103,103,103,103,103,103,103,103,103,103,103,103,103,103,108,108,108,108,208,1,251,2,1,3,251,0,1,251,2,1,1,65,139,159,163,201,0,208,109,251,0,1,251,2,1,1,65,214,149,196,71,208,109,251,0,1,251,2,1,1,65,148,216,135,128,123,208,109,251,0,1,251,2,1,1,65,192,190,150,210,123,208,109,251,0,1,251,2,1,1,65,156,197,229,248,4,208,109,251,0,1,251,2,1,1,65,154,132,205,175,7,208,109,251,0,1,251,2,1,1,251,23,1,251,2,1,1,251,22,106,33,11,65,135,253,171,225,122,11,110,1,12,127,67,28,255,167,139,67,121,51,191,18,67,149,148,199,21,67,28,70,41,247,67,231,54,208,155,208,110,251,23,1,251,2,1,1,251,23,2,65,251,251,243,148,1,208,2,65,224,148,247,167,125,65,229,229,212,175,123,251,17,2,2,67,134,78,191,231,67,237,149,207,164,67,49,144,125,172,67,108,119,238,91,67,137,106,57,182,67,131,211,62,178,67,162,8,151,220,67,17,92,31,101,67,196,15,23,2,11,178,3,3,7,127,1,100,8,4,127,208,112,251,22,8,33,21,208,106,251,22,0,208,110,251,22,0,251,0,0,251,0,0,208,112,66,133,226,0,180,65,151,159,210,154,121,66,240,192,155,233,212,225,158,166,128,127,66,251,204,204,227,204,173,238,214,247,0,254,73,3,148,169,2,180,152,141,67,202,36,57,203,150,168,251,28,251,23,2,251,23,1,251,2,1,1,251,23,1,251,2,1,1,251,23,1,251,2,1,1,65,211,193,135,156,127,66,167,139,250,158,228,252,239,145,89,66,181,231,241,217,240,205,158,253,164,127,254,73,0,148,233,2,65,212,236,149,227,7,66,170,189,193,225,214,239,165,221,14,66,185,179,176,146,144,248,212,138,183,127,254,73,2,148,169,2,65,161,227,139,212,7,66,249,253,136,215,139,230,198,209,94,66,132,221,182,185,192,168,209,153,171,127,254,73,0,133,169,2,90,251,28,208,0,208,110,251,23,107,251,23,107,251,23,107,251,23,107,251,23,107,251,23,107,251,23,107,251,23,107,251,1,1,65,224,166,129,165,122,65,217,150,225,158,125,108,65,252,223,207,230,1,65,249,248,151,84,108,108,65,235,0,65,229,175,133,244,5,65,187,222,207,161,120,108,108,65,150,246,198,215,124,65,252,166,233,206,6,108,108,108,65,224,224,159,240,1,65,150,172,166,153,2,108,65,162,146,134,150,6,65,148,134,177,234,6,65,169,227,203,2,65,175,131,253,185,125,108,108,108,65,0,253,15,253,31,3,208,110,251,23,0,251,23,110,251,23,2,65,186,220,160,171,127,251,11,2,96,108,108,65,224,213,145,16,66,130,253,129,216,221,175,206,224,230,0,66,158,234,207,201,226,190,242,184,49,254,73,3,148,169,2,65,242,221,175,133,1,66,176,149,244,215,139,211,249,248,100,66,179,179,142,152,194,174,147,192,196,0,254,73,0,148,1,90,11,21,6,1,100,6,1,127,1,99,1,2,99,113,1,125,14,127,210,0,33,0,11,11,63,1,1,60,148,214,121,65,131,123,210,221,127,176,139,240,213,245,82,93,220,209,170,119,109,171,69,252,120,97,112,245,156,30,99,138,212,236,158,85,71,25,112,106,67,43,253,182,133,31,206,105,142,63,10,151,79,94,230,161,49,124,131,85


#
# Fatal error in ../../src/compiler/wasm-loop-peeling.cc, line 66
# Debug check failed: use->opcode() == IrOpcode::kLoopExitEffect || use->opcode() == IrOpcode::kLoopExitValue.
#
#
#
#FailureMessage Object: 0x7f50f8ff75a0
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f51346ebc73]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(+0x19add) [0x7f5134692add]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x154) [0x7f51346cbd14]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(+0x2b7d5) [0x7f51346cb7d5]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::PeelWasmLoop(v8::internal::compiler::Node*, v8::internal::ZoneUnorderedSet<v8::internal::compiler::Node*, v8::base::hash<v8::internal::compiler::Node*>, std::__Cr::equal_to<v8::internal::compiler::Node*>>*, v8::internal::compiler::Graph*, v8::internal::compiler::CommonOperatorBuilder*, v8::internal::Zone*, v8::internal::compiler::SourcePositionTable*, v8::internal::compiler::NodeOriginTable*)+0x968) [0x7f5133ef9b98]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::WasmLoopPeelingPhase::Run(v8::internal::compiler::PipelineData*, v8::internal::Zone*, std::__Cr::vector<v8::internal::compiler::WasmLoopInfo, std::__Cr::allocator<v8::internal::compiler::WasmLoopInfo>>*)+0x180) [0x7f5133c56800]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(auto v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::WasmLoopPeelingPhase, std::__Cr::vector<v8::internal::compiler::WasmLoopInfo, std::__Cr::allocator<v8::internal::compiler::WasmLoopInfo>>*&>(std::__Cr::vector<v8::internal::compiler::WasmLoopInfo, std::__Cr::allocator<v8::internal::compiler::WasmLoopInfo>>*&)+0x85) [0x7f5133c470d5]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::Pipeline::GenerateCodeForWasmFunction(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::compiler::CallDescriptor*, v8::internal::ZoneVector<v8::internal::WasmInliningPosition>*, v8::internal::wasm::WasmFeatures*)+0x523) [0x7f5133c44e83]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::compiler::ExecuteTurbofanWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x573) [0x7f5133ec7373]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x81e) [0x7f5133446fee]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x192) [0x7f5133446342]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(+0x3aa594a) [0x7f51334a594a]
    /tmp/d8-linux-debug-v8-component-91313/libv8.so(+0x3aa5185) [0x7f51334a5185]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xd3) [0x7f5134691823]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0xc3) [0x7f5134694213]
    /tmp/d8-linux-debug-v8-component-91313/libv8_libbase.so(+0x4a629) [0x7f51346ea629]
    /lib/x86_64-linux-gnu/libc.so.6(+0x94ac3) [0x7f512f094ac3]
    /lib/x86_64-linux-gnu/libc.so.6(+0x126a40) [0x7f512f126a40]

```

## Other
Please note to include the flags `--experimental-wasm-exnref` for clusterfuzz classification.
Please use poc.js for clusterfuzz reproduction. 
poc1.js is the corresponding wasm pseudocode. Please combine it with poc1.js for analysis.


VERSION
Tested on v8 version: 12.1.0 - 12.1.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-91313.zip
2. Run: `d8 --experimental-wasm-exnref poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Jerry

### cl...@chromium.org (2023-12-04)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6288981036040192.

### je...@gmail.com (2023-12-04)

[Comment Deleted]

### je...@gmail.com (2023-12-04)

I uploaded the correct poc, please re-run clusterfuzz using this poc, remember to add the "--experimental-wasm-exnref" flag

### cl...@chromium.org (2023-12-04)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6382151568654336.

### cl...@chromium.org (2023-12-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-12-04)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5114621415849984.

### sr...@google.com (2023-12-04)

setting provisional severity of high, but not sure what the actual impact here is

[Monorail components: Blink>JavaScript>WebAssembly]

### cl...@chromium.org (2023-12-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-12-05)

Detailed Report: https://clusterfuzz.com/testcase?key=5114621415849984

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  use->opcode() == IrOpcode::kLoopExitEffect || use->opcode() == IrOpcode::kLoopEx
  v8::internal::compiler::PeelWasmLoop
  v8::internal::compiler::WasmLoopPeelingPhase::Run
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=90886:90887

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5114621415849984

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### th...@chromium.org (2023-12-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-05)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-05)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-12-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/cae87fe8391832909b73882a945f27b8b5c75195

commit cae87fe8391832909b73882a945f27b8b5c75195
Author: Manos Koukoutos <manoskouk@chromium.org>
Date: Wed Dec 06 08:53:45 2023

[wasm][exnref] Fix AnalyzeLoopAssignment for try_table

We did not increment the block depth for try_table, resulting in
AnalyzeLoopAssignment exiting early and missing assignments to locals,
or (as in the reproducer) the requirement to reload the instance cache.

Bug: chromium:1507743
Change-Id: Icb90073aca46d5e3ec5b29f19c0df99e3c93f098
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5093209
Auto-Submit: Manos Koukoutos <manoskouk@chromium.org>
Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
Reviewed-by: Thibaud Michaud <thibaudm@chromium.org>
Cr-Commit-Position: refs/heads/main@{#91372}

[add] https://crrev.com/cae87fe8391832909b73882a945f27b8b5c75195/test/mjsunit/regress/wasm/regress-1507743.js
[modify] https://crrev.com/cae87fe8391832909b73882a945f27b8b5c75195/src/wasm/function-body-decoder-impl.h


### ma...@chromium.org (2023-12-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M121. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-12-06)

This issue appears to be specific to --experimental-wasm-exnref which is not enabled and is also specific to the V8 experimental configuration. Updating to SI-None and removing merge review label. 
thibaudm@ please let me know if you're planning to finch this feature during 121 and I can reassess for backmerge -- thank you! 

### be...@google.com (2023-12-07)

Adding Hotlist-RBS-Removed for tracking purposes.

### je...@gmail.com (2023-12-07)

re https://crbug.com/chromium/1507743#c21:

Hi, amy, I agree that it is not enabled by default, however, although named experimental, exnref has already been staged, according to this commit:
[wasm][exnref] Stage the new exception handling proposal
https://chromium-review.googlesource.com/c/v8/v8/+/5032979

Running d8 with this flag does not print out 'experimental', so it should be eligible for a bug bounty.

### am...@chromium.org (2023-12-07)

Thanks for pointing at this commit. A was reviewing an incorrect clusterfuzz reproduction attempt that was related to the experimental config in https://crbug.com/chromium/1507743#c3 (https://clusterfuzz.com/testcase-detail/6288981036040192) and some of the other comments. 
This comment above was part of the merge review process and not however about VRP eligibility which is why the reward-topanel remains and I would have further assessed the status of this flag in that regard.

### am...@chromium.org (2023-12-07)

[Description Changed]

### je...@gmail.com (2023-12-07)

Haha, in fact, my earliest POC accidentally submitted another 0day that I kept that had nothing to do with wasm.
It has not been de-experimental yet, so I don't plan to submit it yet. Since it still takes some time from de-experimental to stable, I think keeping it will not affect Chrome's security, please ignore it, 

This wasm vulnerability does not require an experimental flag.

### cl...@chromium.org (2023-12-13)

ClusterFuzz testcase 6288981036040192 is still reproducing on tip-of-tree build (trunk).

Please re-test your fix against this testcase and if the fix was incorrect or incomplete, please re-open the bug. Otherwise, ignore this notification and add the ClusterFuzz-Wrong label.

### je...@gmail.com (2023-12-13)

Re https://crbug.com/chromium/1507743#c27：
I'm sure this issue has been fixed, but the wrongly uploaded POC is still waiting to be left experimental, so there is no need to continue to pay attention to it.

### je...@gmail.com (2023-12-13)

Please add ClusterFuzz-Wrong label.

### am...@google.com (2023-12-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-12-14)

Congratulations on another one! The Chrome VRP Panel has decided to award you $7,000 for this report + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-12-15)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1507743?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40948441)*
