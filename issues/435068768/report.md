# Debug check failed: ValidationTag::validate

| Field | Value |
|-------|-------|
| **Issue ID** | [435068768](https://issues.chromium.org/issues/435068768) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | fa...@gmail.com |
| **Assignee** | cl...@chromium.org |
| **Created** | 2025-07-30 |
| **Bounty** | Confirmed (amount unknown) |

## Description

```


#
# Fatal error in ../../src/wasm/function-body-decoder-impl.h, line 204
# Debug check failed: ValidationTag::validate.
#
#
#
#FailureMessage Object: 0x7ffdcecc5098
==== C stack trace ===============================

    /home/user/v8/v8/out/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1e) [0x7fb7c553149e]
    /home/user/v8/v8/out/x64.debug/libv8_libplatform.so(+0x4abbd) [0x7fb7c549cbbd]
    /home/user/v8/v8/out/x64.debug/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x205) [0x7fb7c5509e65]
    /home/user/v8/v8/out/x64.debug/libv8_libbase.so(+0x4e81c) [0x7fb7c550981c]
    /home/user/v8/v8/out/x64.debug/libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x4d) [0x7fb7c5509f3d]
    /home/user/v8/v8/out/x64.debug/libv8.so(void v8::internal::wasm::DecodeError<v8::internal::wasm::Decoder::NoValidationTag, unsigned int, char const*, unsigned int>(v8::internal::wasm::Decoder*, char const*, unsigned int&&, char const*&&, unsigned int&&)+0x36) [0x7fb7cf1fa3d6]
    /home/user/v8/v8/out/x64.debug/libv8.so(void v8::internal::wasm::WasmDecoder<v8::internal::wasm::Decoder::NoValidationTag, (v8::internal::wasm::DecodingMode)0>::DecodeError<char const*, unsigned int, char const*, unsigned int>(char const*, unsigned int, char const*, unsigned int)+0x34) [0x7fb7cf1fa294]
    /home/user/v8/v8/out/x64.debug/libv8.so(bool v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::TypeCheckStackAgainstMerge_Slow<(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::StackElementsCountMode)1, (v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::PushBranchValues)0, (v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::MergeType)2, (v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::RewriteStackTypes)0>(v8::internal::wasm::Merge<v8::internal::wasm::TurboshaftGraphBuildingInterface::Value>*)+0xc4) [0x7fb7cf3b3134]
    /home/user/v8/v8/out/x64.debug/libv8.so(bool v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::TypeCheckStackAgainstMerge<(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::StackElementsCountMode)1, (v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::PushBranchValues)0, (v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::MergeType)2, (v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::RewriteStackTypes)0>(v8::internal::wasm::Merge<v8::internal::wasm::TurboshaftGraphBuildingInterface::Value>*)+0xbe) [0x7fb7cf3b2ffe]
    /home/user/v8/v8/out/x64.debug/libv8.so(bool v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DoReturn<(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::StackElementsCountMode)1, (v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::MergeType)2>()+0x30) [0x7fb7cf3b0810]
    /home/user/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeEndImpl(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::TraceLine*, v8::internal::wasm::WasmOpcode)+0x92d) [0x7fb7cf3af05d]
    /home/user/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeEnd(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::WasmOpcode)+0x6e) [0x7fb7cf38c48e]
    /home/user/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeFunctionBody()+0x4a9) [0x7fb7cf37e769]
    /home/user/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::Decode()+0x276) [0x7fb7cf365f66]
    /home/user/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::BuildTSGraph(v8::internal::compiler::turboshaft::PipelineData*, v8::internal::AccountingAllocator*, v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WasmDetectedFeatures*, v8::internal::compiler::turboshaft::Graph&, v8::internal::wasm::FunctionBody const&, v8::internal::wasm::WireBytesStorage const*, std::__Cr::unique_ptr<v8::internal::wasm::AssumptionsJournal, std::__Cr::default_delete<v8::internal::wasm::AssumptionsJournal>>*, v8::internal::ZoneVector<v8::internal::WasmInliningPosition>*, int, v8::internal::wasm::WasmFunctionCoverageData*)+0x1f1) [0x7fb7cf363ef1]
    /home/user/v8/v8/out/x64.debug/libv8.so(v8::internal::compiler::Pipeline::GenerateWasmCode(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmDetectedFeatures*, v8::internal::Counters*)+0xa59) [0x7fb7cff163f9]
    /home/user/v8/v8/out/x64.debug/libv8.so(v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmDetectedFeatures*, v8::internal::Counters*)+0x53) [0x7fb7d164f0e3]
    /home/user/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmDetectedFeatures*)+0x96c) [0x7fb7cf2bef2c]
    /home/user/v8/v8/out/x64.debug/libv8.so(v8::internal::wasm::CompileLazy(v8::internal::Isolate*, v8::internal::Tagged<v8::internal::WasmTrustedInstanceData>, int)+0x2f9) [0x7fb7cf2c5959]
    /home/user/v8/v8/out/x64.debug/libv8.so(+0x9bd8cce) [0x7fb7cf11bcce]
    /home/user/v8/v8/out/x64.debug/libv8.so(v8::internal::Runtime_WasmCompileLazy(int, unsigned long*, v8::internal::Isolate*)+0x151) [0x7fb7cf11b791]
    /home/user/v8/v8/out/x64.debug/libv8.so(+0x71d2257) [0x7fb7cc715257]
Trace/breakpoint trap (core dumped)

```
#### VERSION

V8 version 13.9.0 (candidate)

#### REPRODUCTION CASE

Build: `python3 tools/dev/gm.py x64.debug`

Run: `./d8 poc.js`

---

Reporter credit: Shaheen Fazim

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 397 B)

## Timeline

### hc...@google.com (2025-07-30)

I don't see a PoC attached, was this left off by mistake?

### fa...@gmail.com (2025-07-30)

Yeah, sorry I've been bisecting this, and it seems the issue goes way back.

### pe...@google.com (2025-07-30)

Thank you for providing more feedback. Adding the requester to the CC list.

### cl...@appspot.gserviceaccount.com (2025-07-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5978689644724224.

### hc...@google.com (2025-07-30)

Setting provisional FoundIn, Severity, and OS for v8 bug, assigned to v8 sheriff.

### 24...@project.gserviceaccount.com (2025-07-30)

Detailed Report: https://clusterfuzz.com/testcase?key=5978689644724224

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  ValidationTag::validate in function-body-decoder-impl.h
  bool v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidati
  bool v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidati
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=86202:86203

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5978689644724224

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### 24...@project.gserviceaccount.com (2025-07-30)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### ch...@google.com (2025-07-31)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-07-31)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### cl...@chromium.org (2025-08-04)

There's a bug in parsing heap accesses.

There's special handling for expressions of the form `x[expr >> n]` if `x` is an array buffer and `n` is the size-log-2 of that array buffer. This is spec'ed explicitly in `ValidateHeapAccess`, see <http://asmjs.org/spec/latest/>.

However, we get confused if such expressions are nested, in this case `HEAP32[a >> (b >> 2)] = 42;`.
We first generate the code normally (`local.get 0`, `local.get 1`, `i32.const 2`, `i32.shr`, `i32.shr`), and then we detect this pattern, rewind the generated code to `local.get 0` and `local.get 1`, and emit `i32.const 3` and `i32.and`.
This generates wrong Wasm code (leaves one value too much on the stack).

We will need to fix the detection logic here to exclude such nested patterns: <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/asmjs/asm-parser.cc;l=2488;drc=3e7191831b1a3f979570b9668541770bb6624d02>

### cl...@chromium.org (2025-08-04)

And I guess we will have to keep this as a vulnerability, because this violates an encoded assumption in the code, so this is undefined behavior for the compiler. I'll reduce severity though, because there is no indication that this can be exploited.

### dx...@google.com (2025-08-04)

Project: v8/v8  

Branch:  main  

Author:  Clemens Backes [clemensb@chromium.org](mailto:clemensb@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6818796>

[asm] Fix detection of heap accesses

---


Expand for full commit details
```
     
    "Nested" shift patterns like in `HEAP32[a >> (b >> 2)]` are not valid 
    heap accesses. The old logic did lead to generating corrupted Wasm code. 
     
    R=jkummerow@chromium.org 
     
    Bug: 435068768 
    Change-Id: I7ed566826dc53906cd282ef63361ce28d72baefa 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6818796 
    Commit-Queue: Clemens Backes <clemensb@chromium.org> 
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#101748}

```

---

Files:

- M `src/asmjs/asm-parser.cc`
- A `test/mjsunit/asm/regress-435068768.js`

---

Hash: [f089fd9d11a72f393c61bb2984cab6c58457387f](http://crrev.com/f089fd9d11a72f393c61bb2984cab6c58457387f)  

Date: Mon Aug 4 12:49:56 2025


---

### 24...@project.gserviceaccount.com (2025-08-05)

ClusterFuzz testcase 5978689644724224 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=101747:101748

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### sp...@google.com (2025-09-04)

** NOTE: This is an automatically generated email **

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this issue does not meet the criteria to qualify for a reward.

Rationale for this decision:
Thank you for the report. There is no demonstration of exploitability presented and in evaluation this does not appear to be potentially exploitable, therefore, we are unfortunately unable to extend a Chrome VRP reward for this report. 

Please note that the fact that this issue is not being rewarded does not mean that the product team won't fix the issue. We have filed a bug with the product team and they will review your report and decide if a fix is required. We'll let you know if the issue was fixed.

Regards,
Google Security Bot


--
How did we do? Please fill out a short anonymous survey (https://goo.gl/IR3KRH).

### ch...@google.com (2025-11-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Thank you for the report. There is no demonstration of exploitability presented and in evaluation this does not appear to be potentially exploitable, therefore, we are unfortunately unable to extend a Chrome VRP reward for this report. 
> 
> Please note that the fact that this issue is not being rewarded does not mean that the product team won't fix the issue. We have filed a bug with the product team and they will review your report and decide if a fix is required. We'll let you know if the issue w

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/435068768)*
