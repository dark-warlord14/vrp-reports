# Security: Debug check failed: !type.is_uninhabited()

| Field | Value |
|-------|-------|
| **Issue ID** | [343633071](https://issues.chromium.org/issues/343633071) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler, Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows |
| **Reporter** | rh...@gmail.com |
| **Assignee** | ml...@chromium.org |
| **Created** | 2024-05-30 |
| **Bounty** | $7,000.00 |

## Description

# Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

VERSION
Chrome Version: V8 version 12.7.0 (candidate)
Operating System: arm64

REPRODUCTION CASE

1. build v8 for arm64 with asan enabled
   args.gn

```

is_component_build = false
is_debug = false
target_cpu = "arm64"
v8_enable_sandbox = true
v8_enable_backtrace = true
v8_enable_disassembler = true
v8_enable_object_print = true
v8_enable_verify_heap = true
dcheck_always_on = false
v8_enable_webassembly = true
is_asan = true

```

2.

```
export ASAN_OPTIONS="alloc_dealloc_mismatch=0:allocator_may_return_null=1:allow_user_segv_handler=1:check_malloc_usable_size=0:detect_leaks=0:detect_odr_violation=0:detect_stack_use_after_return=1:fast_unwind_on_fatal=1:handle_abort=1:handle_segv=1:handle_sigbus=1:handle_sigfpe=1:handle_sigill=1:handle_sigtrap=1:print_scariness=1:print_summary=1:print_suppressions=0:redzone=128:strict_memcmp=0:symbolize_inline_frames=false:use_sigaltstack=1"

```

3. run `./out/arm64/d8 helper1.js --wasm-staging -- original.wasm`
   
   - (there's need double hypen after v8 args)

- note: clusterfuzz will not able repro if have two files, please see
- <https://issues.chromium.org/issues/342602616#comment14>

---

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: v8

```
=================================================================
==1079==ERROR: AddressSanitizer: TRAP on unknown address 0x0001037e0398 (pc 0x0001037e0398 bp 0x00016fad9b30 sp 0x00016fad9b30 T0)
SCARINESS: 10 (signal)
    #0 0x1037e0398 in v8::base::OS::Abort() src/base/platform/platform-posix.cc:699:7
    #1 0x1037cb254 in V8_Fatal(char const*, ...) src/base/logging.cc:205:3
    #2 0x102223810 in v8::internal::Assembler::LoadStore(v8::internal::CPURegister const&, v8::internal::MemOperand const&, unsigned int) src/codegen/arm64/assembler-arm64.h
    #3 0x101de16cc in v8::internal::wasm::LiftoffAssembler::PrepareTailCall(int, int) src/wasm/baseline/arm64/liftoff-assembler-arm64-inl.h:296:5
    #4 0x101de447c in v8::internal::wasm::(anonymous namespace)::LiftoffCompiler::CallIndirectImpl(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::(anonymous namespace)::LiftoffCompiler, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::CallIndirectImmediate const&, v8::internal::wasm::(anonymous namespace)::LiftoffCompiler::TailCall) src/wasm/baseline/liftoff-compiler.cc:8366:12
    #5 0x101da4d38 in v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::(anonymous namespace)::LiftoffCompiler, (v8::internal::wasm::DecodingMode)0>::DecodeReturnCallIndirect(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::(anonymous namespace)::LiftoffCompiler, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::WasmOpcode) src/wasm/baseline/liftoff-compiler.cc:4078:5
    #6 0x101d888f8 in v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::(anonymous namespace)::LiftoffCompiler, (v8::internal::wasm::DecodingMode)0>::Decode() src/wasm/function-body-decoder-impl.h:2868:17
    #7 0x101d85c84 in v8::internal::wasm::ExecuteLiftoffCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::FunctionBody const&, v8::internal::wasm::LiftoffOptions const&) src/wasm/baseline/liftoff-compiler.cc:8931:11
    #8 0x101ebf8d8 in v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*) src/wasm/function-compiler.cc:141:18
    #9 0x101ebe8b0 in v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*) src/wasm/function-compiler.cc:32:9
    #10 0x101f0dd94 in v8::internal::wasm::CompileLazy(v8::internal::Isolate*, v8::internal::Tagged<v8::internal::WasmTrustedInstanceData>, int) src/wasm/module-compiler.cc:1218:48
    #11 0x101d2ff94 in v8::internal::Runtime_WasmCompileLazy(int, unsigned long*, v8::internal::Isolate*) src/runtime/runtime-wasm.cc:406:18
    #12 0x1035c3b58 in Builtins_WasmCEntry (/Users/uu/v8/v8/out/arm64_asan/d8:arm64+0x10329fb58)
    #13 0x1035bbdc8 in Builtins_WasmCompileLazy (/Users/uu/v8/v8/out/arm64_asan/d8:arm64+0x103297dc8)
    #14 0x157e9dff0  (<unknown module>)
    #15 0x157f6a014  (<unknown module>)
    #16 0x157e0d5f4  (<unknown module>)
    #17 0x157e0b004  (<unknown module>)
    #18 0x157e0ac50  (<unknown module>)
    #19 0x1007f6828 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/simulator.h:178:12
    #20 0x1007f7e24 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>) src/execution/execution.cc:516:10
    #21 0x1003ba5d8 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2110:7
    #22 0x1003531dc in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:969:44
    #23 0x100376344 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:4499:10
    #24 0x10037f158 in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:5364:37
    #25 0x10037e760 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:5273:18
    #26 0x100381584 in v8::Shell::Main(int, char**) src/d8/d8.cc:6164:18
    #27 0x185f2e0dc  (<unknown module>)
    #28 0xbe297ffffffffffc  (<unknown module>)

==1079==Register values:
 x[0] = 0x0000000108e94000   x[1] = 0x0000000000000000   x[2] = 0x0000000000000000   x[3] = 0x000000702df7b7c0  
 x[4] = 0x000000702df7a880   x[5] = 0x0000000000000000   x[6] = 0x000000016f2e0000   x[7] = 0x0000000000000001  
 x[8] = 0x0000000000000001   x[9] = 0x0000000000000004  x[10] = 0x0000000000000003  x[11] = 0x0000000000000000  
x[12] = 0x0000000000000000  x[13] = 0x0000000000000000  x[14] = 0x0000000000000000  x[15] = 0x0000000000000000  
x[16] = 0x00000001862b1da4  x[17] = 0x0000000186158638  x[18] = 0x0000000000000000  x[19] = 0x000000016fad9b40  
x[20] = 0x0000000103dcf6a0  x[21] = 0x00000001092b0c20  x[22] = 0x00000001ece12ed8  x[23] = 0x0000007000020000  
x[24] = 0x00000001092b0c40  x[25] = 0x000000003d9c25db  x[26] = 0x00000001040d0840  x[27] = 0x0000000000000048  
x[28] = 0x00000001091cbcd0     fp = 0x000000016fad9b30     lr = 0x00000001037cb258     sp = 0x000000016fad9b30  
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: TRAP src/base/platform/platform-posix.cc:699:7 in v8::base::OS::Abort()
==1079==ABORTING

```

---

bisect: <https://chromium-review.googlesource.com/c/v8/v8/+/2473833>

## Attachments

- deleted (application/octet-stream, 0 B)
- [original.wasm](attachments/original.wasm) (application/wasm, 8.5 KB)
- deleted (application/octet-stream, 0 B)

## Timeline

### rh...@gmail.com (2024-05-30)

Hi,

Please use new single file on the attachment for upload to CF.

`./d8 --wasm-staging ./poc.js`

### cl...@appspot.gserviceaccount.com (2024-05-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6045472127909888.

### rh...@gmail.com (2024-05-30)

Hello,

Does the CF have arm64\_asan\_debug? I think it is OS-specific.

### 24...@project.gserviceaccount.com (2024-05-30)

Testcase 6045472127909888 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6045472127909888.

### cl...@appspot.gserviceaccount.com (2024-05-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5415041460273152.

### mp...@google.com (2024-05-30)

Sorry, yes, I forgot to set it to use arm64. :) Running again. Thank you for combining the poc into 1 file for us!

### rh...@gmail.com (2024-05-30)

Thank you

for the single file poc, I read from this <https://issues.chromium.org/issues/342602616#comment14>

### mp...@google.com (2024-05-31)

Clusterfuzz has reproduced and will hopefully set FoundIn for us.

### 24...@project.gserviceaccount.com (2024-05-31)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2024-05-31)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/c74783f8ec53e16a6aec28aef162569ccc75156a ([wasm-gc] Final binary encoding

This patch brings the official final binary encoding for WasmGC
instructions and types to V8.
This is a breaking change. Modules compiled for the "prototype
spec" (bit.ly/3cWcm6Q) will no longer work.
Unfortunately this also needs to shift the encodings for the
"stringref" and "stringview_wtf8" types, to resolve collisions.

Bug: v8:7748, v8:12868
Change-Id: I6d81c34867066f0388f4f2e44ec521d7a594d203
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4756846
Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
Cr-Commit-Position: refs/heads/main@{#89962}
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### mp...@google.com (2024-05-31)

Clusterfuzz sees this as a DCHECK but the report includes a deref of an unknown address, so setting severity as S1 (high).

### pe...@google.com (2024-06-01)

Setting milestone because of s0/s1 severity.

### jk...@chromium.org (2024-06-03)

I see no vulnerability here: this `CHECK`-fails in Release mode. ASan may call that a "TRAP", but as the top of the stack show, it's a safe `v8::base::OS::Abort()`.

That said, it's clearly a bug. Will fix.

### jk...@chromium.org (2024-06-03)

Fix in flight: <https://chromium-review.googlesource.com/c/v8/v8/+/5591671>

FWIW, the bisection result is bogus; the repro found by the fuzzer is overly verbose and hence incidentally needs certain Wasm features that are actually unrelated to the bug. See the fix CL for a reduced repro that would bisect much farther back (probably to the introduction of tail call support on arm64; doesn't matter at this point).

### ap...@google.com (2024-06-03)

Project: v8/v8
Branch: main

commit 59399c85628db547c207e4a228c1b1d5b974cefb
Author: Jakob Kummerow <jkummerow@chromium.org>
Date:   Mon Jun 03 11:12:29 2024

    [wasm][liftoff][arm64] Fix PrepareTailCall
    
    Both available temp registers are already in use, so we must
    carefully arrange instructions to not require additional temp
    registers under the MacroAssembler's hood.
    
    Fixed: 343633071
    Change-Id: Ie7dffbb2eacbcc641dfd050aaf2f3b36ecfb15c0
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5591671
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
    Reviewed-by: Daniel Lehmann <dlehmann@chromium.org>
    Commit-Queue: Daniel Lehmann <dlehmann@chromium.org>
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#94201}

M       src/wasm/baseline/arm64/liftoff-assembler-arm64-inl.h
A       test/mjsunit/regress/wasm/regress-343633071.js

https://chromium-review.googlesource.com/5591671


### am...@chromium.org (2024-06-05)

Thank you for the report. Since this issue does not appear to be an exploitable security issue, this report is unfortunately no eligible for a Chrome VRP reward.

### pe...@google.com (2024-09-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/343633071)*
