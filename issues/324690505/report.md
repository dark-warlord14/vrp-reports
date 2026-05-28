# Debug check failed: i.valid(). in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [324690505](https://issues.chromium.org/issues/324690505) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript, Blink>JavaScript>WebAssembly |
| **Platforms** | Linux |
| **Reporter** | je...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2024-02-11 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 92216
    - link: https://crrev.com/08170169a305fab1dca42bc11d86d7400f25421e 
- Commit Message

```
commit 08170169a305fab1dca42bc11d86d7400f25421e
Author: Jakob Kummerow <jkummerow@chromium.org>
Date:   Tue Feb 6 15:40:33 2024 +0100

    [wasm-imported-strings] Implement encodeStringToUtf8Array
    
    Contrary to the "Into" variant, this implicitly allocates an array
    of appropriate size.
    
    Bug: v8:14179
    Change-Id: I01974624683eef961f6c8b8c6cbe33aa65d2df6a
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5273182
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#92216}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux32-debug-v8-component-92260/d8 --allow-natives-syntax --experimental-wasm-imported-strings --turboshaft-wasm poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/compiler/turboshaft/graph.h, line 598
# Debug check failed: i.valid().
#
#
#
#FailureMessage Object: 0xe0df8990
==== C stack trace ===============================

    /tmp/d8-linux32-debug-v8-component-92260/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1f) [0xf7f4619f]
    /tmp/d8-linux32-debug-v8-component-92260/libv8_libplatform.so(+0x16274) [0xf7ef2274]
    /tmp/d8-linux32-debug-v8-component-92260/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0xf7) [0xf7f255a7]
    /tmp/d8-linux32-debug-v8-component-92260/libv8_libbase.so(+0x26fa6) [0xf7f24fa6]
    /tmp/d8-linux32-debug-v8-component-92260/libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x31) [0xf7f255f1]
    /tmp/d8-linux32-debug-v8-component-92260/libv8.so(v8::internal::compiler::turboshaft::Graph::Get(v8::internal::compiler::turboshaft::OpIndex)+0x6c) [0xf666c9fc]
    /tmp/d8-linux32-debug-v8-component-92260/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::IsArrayNewSegment(v8::internal::compiler::turboshaft::V<v8::internal::Object>)+0x2e) [0xf69eb62e]
    /tmp/d8-linux32-debug-v8-component-92260/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::StringNewWtf8ArrayImpl(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, unibrow::Utf8Variant, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const&, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const&, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const&)+0x2b) [0xf69e1fab]
    /tmp/d8-linux32-debug-v8-component-92260/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::HandleWellKnownImport(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, unsigned int, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*)+0x57d) [0xf69db64d]
    /tmp/d8-linux32-debug-v8-component-92260/libv8.so(v8::internal::wasm::TurboshaftGraphBuildingInterface::CallDirect(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::CallFunctionImmediate const&, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*)+0x40) [0xf69daf60]
    /tmp/d8-linux32-debug-v8-component-92260/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallFunctionImpl(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::TraceLine*, v8::internal::wasm::WasmOpcode)+0x16e) [0xf69dab8e]
    /tmp/d8-linux32-debug-v8-component-92260/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallFunction(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::WasmOpcode)+0x95) [0xf69af625]
    /tmp/d8-linux32-debug-v8-component-92260/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeFunctionBody()+0x24e) [0xf699b75e]
    /tmp/d8-linux32-debug-v8-component-92260/libv8.so(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::FullValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::Decode()+0x26d) [0xf69985ad]
    /tmp/d8-linux32-debug-v8-component-92260/libv8.so(v8::internal::wasm::BuildTSGraph(v8::internal::AccountingAllocator*, v8::internal::wasm::WasmFeatures, v8::internal::wasm::WasmModule const*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::turboshaft::Graph&, v8::internal::wasm::FunctionBody const&, v8::internal::wasm::WireBytesStorage const*, v8::internal::wasm::AssumptionsJournal*, v8::internal::ZoneVector<v8::internal::WasmInliningPosition>*, int)+0x30f) [0xf6997e0f]
    /tmp/d8-linux32-debug-v8-component-92260/libv8.so(v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph(v8::internal::OptimizedCompilationInfo*, v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::compiler::MachineGraph*, v8::internal::wasm::WasmFeatures*, v8::internal::compiler::CallDescriptor*)+0x65f) [0xf711394f]
    /tmp/d8-linux32-debug-v8-component-92260/libv8.so(v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmFeatures*)+0x317) [0xf73dcd27]
    /tmp/d8-linux32-debug-v8-component-92260/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x727) [0xf68ee2a7]
    /tmp/d8-linux32-debug-v8-component-92260/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x18a) [0xf68ed78a]
    /tmp/d8-linux32-debug-v8-component-92260/libv8.so(+0x334af9c) [0xf694af9c]
    /tmp/d8-linux32-debug-v8-component-92260/libv8.so(+0x334a899) [0xf694a899]
    /tmp/d8-linux32-debug-v8-component-92260/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xcb) [0xf7ef0e9b]
    /tmp/d8-linux32-debug-v8-component-92260/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0x9f) [0xf7ef362f]
    /tmp/d8-linux32-debug-v8-component-92260/libv8_libbase.so(+0x46dbe) [0xf7f44dbe]
    /lib/i386-linux-gnu/libc.so.6(+0x86c01) [0xf2c86c01]
    /lib/i386-linux-gnu/libc.so.6(+0x12372c) [0xf2d2372c]

```

## Other
Please note to include the flags `--allow-natives-syntax --experimental-wasm-imported-strings --turboshaft-wasm` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.3.0 - 12.3.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux32-debug/d8-linux32-debug-v8-component-92260.zip
2. Run: `d8 --allow-natives-syntax --experimental-wasm-imported-strings --turboshaft-wasm poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Jerry

## Attachments

- [poc2.js](attachments/poc2.js) (text/javascript, 9.2 KB)
- [wasm.bin](attachments/wasm.bin) (application/octet-stream, 2.7 KB)

## Timeline

### je...@gmail.com (2024-02-11)

Because the implementation of toBuffer in v8/test/mjsunit/wasm/wasm-module-builder.js is incorrect, this leads to the function signature being wrong, so I cannot provide you with pseudocode.

### je...@gmail.com (2024-02-11)

- segment fault in release

release/d8 --turboshaft-wasm --experimental-wasm-imported-strings poc2.js
Received signal 11 SEGV_MAPERR 7f1ccc004db7

==== C stack trace ===============================

 [0x55c0f7a81aa7]
 [0x7f1cb7e42520]
 [0x55c0f7187e97]
 [0x55c0f718401d]
 [0x55c0f718390f]
 [0x55c0f7173364]
 [0x55c0f716a16f]
 [0x55c0f7168f65]
 [0x55c0f7168a57]
 [0x55c0f74afc50]
 [0x55c0f75f031c]
 [0x55c0f7115d76]
 [0x55c0f71154d2]
 [0x55c0f714110b]
 [0x55c0f7140ad7]
 [0x55c0f7a82f0b]
 [0x55c0f7a85e1c]
 [0x55c0f7a7f2ee]
 [0x7f1cb7e94ac3]
 [0x7f1cb7f26850]
[end of stack trace]
[1]    185821 segmentation fault  release/d8 --turboshaft-wasm --experimental-wasm-imported-strings poc2.js


### je...@gmail.com (2024-02-12)

Due to recent changes in the functionality code of wasm, bisect may not necessarily be accurate. Please decide on the final entry point based on the actual situation.

### je...@gmail.com (2024-02-12)

This vulnerability report highlights a fatal error triggered in the Turboshaft compiler of the V8 engine, particularly when handling the import strings feature of WebAssembly. The following is an analysis of the vulnerability details, causes, and potential solutions.

## Vulnerability Details

The vulnerability was introduced by a specific commit that implemented the encodeStringToUtf8Array function. Unlike its "Into" variant, this function implicitly allocates an array of appropriate size. This change led to crashes when processing certain types of WebAssembly code. The direct cause of this issue was the failure to properly handle all possible inputs and boundary conditions when introducing new functionality. Specifically, the implementation of encodeStringToUtf8Array might not have taken into account type safety and memory management in certain scenarios, leading to assertion failures when attempting to use improperly initialized graph nodes.

## Crash Log

The crash occurred at ../../src/compiler/turboshaft/graph.h, line 598, with the debug check failing: i.valid().

This indicates an attempt to access an invalid index within the graph structure, which should not happen.

## Stack Trace Analysis

- Failure in Graph::Get function call: The issue started with the v8::internal::compiler::turboshaft::Graph::Get function, which attempted to retrieve an operation index (OpIndex) but failed because the provided index was invalid, triggering the assertion i.valid().
- Handling of WebAssembly: The crash occurred while processing specific functionalities of WebAssembly code, particularly operations related to StringNewWtf8ArrayImpl and IsArrayNewSegment. This suggests that there might have been logical errors or incorrect handling of boundary conditions when parsing or converting string data in WebAssembly modules.

### wf...@chromium.org (2024-02-12)

Ty for reporting this issue. I am triaging your bug.

### cl...@appspot.gserviceaccount.com (2024-02-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4910242413871104.

### wf...@chromium.org (2024-02-12)

The severity and Found In are provisional.

### 24...@project.gserviceaccount.com (2024-02-12)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2024-02-12)

Detailed Report: https://clusterfuzz.com/testcase?key=4910242413871104

Fuzzer: None
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x52d10006e417
Crash State:
  bool v8::internal::compiler::turboshaft::Operation::Is<v8::internal::compiler::t
  v8::internal::compiler::turboshaft::underlying_operation<v8::internal::compiler:
  v8::internal::wasm::TurboshaftGraphBuildingInterface::IsArrayNewSegment
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8&range=92215:92216

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4910242413871104

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### pe...@google.com (2024-02-13)

Setting milestone because of s2 severity.

### pe...@google.com (2024-02-13)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### je...@gmail.com (2024-02-15)

Hello, any update? :)

### jk...@chromium.org (2024-02-16)

Fix in flight: <https://chromium-review.googlesource.com/c/v8/v8/+/5300801>

### ap...@google.com (2024-02-16)

Project: v8/v8
Branch: main

commit bb75670599aa8cea04409f995c995017b2792189
Author: Jakob Kummerow <jkummerow@chromium.org>
Date:   Fri Feb 16 12:21:10 2024

    [wasm-imported-strings] Fix IsArrayNewSegment in unreachable code
    
    The node we query is invalid in unreachable code, so we must check
    for that before fetching it from the graph.
    
    Bonus: running the regression test in Turbofan revealed an unrelated
    issue having to do with reachability of catch blocks after replacing
    a well-known import, so this CL includes a fix for that too.
    
    Fixed: chromium:324690505
    Change-Id: If648faf7dd466ed857d723eec44fc01fc7a6a6fc
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5300801
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#92362}

M       src/wasm/graph-builder-interface.cc
M       src/wasm/turboshaft-graph-interface.cc
A       test/mjsunit/regress/wasm/regress-324690505.js

https://chromium-review.googlesource.com/5300801


### jk...@chromium.org (2024-02-16)

Note: this issue only affected unreachable code inside a Wasm function. The crash in release mode was an out-of-bounds read in the compiler:

```
(gdb) bt
#0  IsArrayNewSegment () at ../../src/wasm/turboshaft-graph-interface.cc:3485
#1  StringNewWtf8ArrayImpl () at ../../src/wasm/turboshaft-graph-interface.cc:3503
#2  0x000055d5c24643bd in HandleWellKnownImport () at ../../src/wasm/turboshaft-graph-interface.cc:1687
#3  0x000055d5c2463caf in CallDirect () at ../../src/wasm/turboshaft-graph-interface.cc:1966
#4  0x000055d5c2453675 in DecodeCallFunctionImpl () at ../../src/wasm/function-body-decoder-impl.h:3840
#5  DecodeCallFunction () at ../../src/wasm/function-body-decoder-impl.h:3835
#6  0x000055d5c244ef7f in DecodeFunctionBody () at ../../src/wasm/function-body-decoder-impl.h:2821
#7  0x000055d5c2448bc5 in Decode () at ../../src/wasm/function-body-decoder-impl.h:2644
#8  0x000055d5c24485fb in BuildTSGraph () at ../../src/wasm/turboshaft-graph-interface.cc:7094
#9  0x000055d5c2821875 in GenerateWasmCodeFromTurboshaftGraph () at ../../src/compiler/pipeline.cc:3968
#10 0x000055d5c297980c in ExecuteTurboshaftWasmCompilation () at ../../src/compiler/turboshaft/wasm-turboshaft-compiler.cc:51
(gdb) layout asm
> 0x55d5c2468217 <StringNewWtf8ArrayImpl()+39>    cmp    BYTE PTR [rax+r13*1],0x47
(gdb) p/x $rax
$1 = 0x7fc8b0004db8  ;; start address of the array of IR nodes
(gdb) p/x $r13
$2 = 0xffffffff      ;; sentinel index for "invalid" IR node

```

I cannot rule out that it might be possible, by having some way to place readable memory at the requested address, to make it past the segfault; but even if compilation successfully finished, any hypothetical invalid generated code would be in unreachable parts of the function (and I'm not even sure whether generated code would, in fact, be invalid).
In short, while I'm of course willing to be convinced otherwise, I lack the imagination to see how this would be exploitable. (Sorry, Jerry! Your reports are still very much appreciated.)

### je...@gmail.com (2024-02-16)

Thank you for your clarification. I also think that it should be quite difficult to exploit this problem. However, this is indeed an oob read in the render process. It should meet the memory corrupt condition of the render process and be worthy of the Chrome VRP reward.:)

### ap...@google.com (2024-02-16)

Project: v8/v8
Branch: main

commit 4765e4b73fcbd98af3eda5da531aab8d36109b32
Author: Jakob Kummerow <jkummerow@chromium.org>
Date:   Fri Feb 16 16:21:36 2024

    [wasm-imported-strings] Fixup Turbofan part of bb756705
    
    We shouldn't use an IfFalse as a value node. The regression test
    has been extended to cover this mistake.
    Bonus: clean up some unused things in the regression test.
    
    Bug: 324690505
    Change-Id: Ifb6d9ee5a718d6abb99a3d8646af75b46fe7e567
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5300308
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#92370}

M       src/wasm/graph-builder-interface.cc
M       test/mjsunit/regress/wasm/regress-324690505.js

https://chromium-review.googlesource.com/5300308


### ap...@google.com (2024-02-16)

Project: v8/v8
Branch: main

commit 4765e4b73fcbd98af3eda5da531aab8d36109b32
Author: Jakob Kummerow <jkummerow@chromium.org>
Date:   Fri Feb 16 16:21:36 2024

    [wasm-imported-strings] Fixup Turbofan part of bb756705
    
    We shouldn't use an IfFalse as a value node. The regression test
    has been extended to cover this mistake.
    Bonus: clean up some unused things in the regression test.
    
    Bug: 324690505
    Change-Id: Ifb6d9ee5a718d6abb99a3d8646af75b46fe7e567
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5300308
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#92370}

M       src/wasm/graph-builder-interface.cc
M       test/mjsunit/regress/wasm/regress-324690505.js

https://chromium-review.googlesource.com/5300308


### 24...@project.gserviceaccount.com (2024-02-17)

ClusterFuzz testcase 4910242413871104 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8&range=92361:92362

If this is incorrect, please add the hotlistid:5432646 and re-open the issue.

### je...@gmail.com (2024-02-20)

## Exploit Info
Hi! This vulnerability is only unreachable to the wasm code, but it is not unexploitable because it may cause damage to your memory at the v8 C++ code level.
At the same time, since the OpIndex is 0xffffffff, this may be difficult to use under 64-bit v8, but please consider the 32-bit situation. In 32-bit v8, this will cause the program to hit a valid address, which is begin_addr + 0xffffffff = begin_addr - 1. This may cause:
1. Pointer misalignment, the returned pointer will no longer be aligned with 0x8.
2. Read forward oob
3. Confusion on Opcode
Therefore, the exploitation of this vulnerability may require further investigation, and it still has many possibilities for exploitation.

### jk...@chromium.org (2024-02-21)

Re #21:

1. Pointer misalignment is not exploitable. At worst, it'll crash on a platform that doesn't support unaligned reads.
2. Yes, there's no debate that an OOB read happens here; but the data being read is only used for an equality comparison; so if you want to argue that this is exploitable, you'll need to present some idea how an incorrect result from this comparison will lead to observable incorrect behavior.
3. Yes, we're comparing opcodes, so if incorrect data is read (without immediately segfaulting), it'll look like a different opcode, so the opcode comparison may yield an incorrect result. But as I wrote before, all of this only happens in unreachable code (e.g. after a conditional jump that's always taken, or after a type check that is guaranteed to always fail, etc), so even if you managed to trick the Turboshaft compiler into emitting an incorrect instruction sequence, you still wouldn't have a way to actually execute those instructions.

I still don't see how this would be exploitable. Of course I'd be happy (well... you know what I mean :) ) to be proven wrong by a proof of concept that does manage to achieve any other outcome than a segfault in the compiler (which is harmless from a security perspective, just a bad user experience and clearly a bug).

### je...@gmail.com (2024-02-21)

Thank you for your review. Investigating the exploitability of vulnerabilities is always challenging, especially when I am not very familiar with wasm optimization. Nonetheless, I appreciate your prompt fix once again for this out-of-bounds read vulnerability. :)

### je...@gmail.com (2024-02-21)

In addition, I would like to explain that not all vulnerabilities are exploitable. As a security researcher, when I can demonstrate that a certain issue indeed leads to UAF or OOB, I consider it as a security concern, even if the UAF window is short, or there are no available placeholder objects, or the OOB read accesses irrelevant data. 

Truly exploitable issues are always rare. Chrome is a secure browser, thanks to excellent developers like you!

Regarding the Chrome VRP, I'm not certain if it meets the reward criteria, but I believe it falls under the category of "Renderer RCE / memory corruption in a sandboxed process". Many non-exploitable vulnerabilities that require the browser to be closed to trigger have also been rewarded, so I don't think this is any worse :)
Link to Google Bug Hunters Rules(https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

### am...@google.com (2024-02-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-22)

Thank you for the discourse here and the report. The Chrome VRP Panel has decided to award you $1,000 for this report of a mitigated security bug in the renderer process resulting in OOB read in which the read is of limited use. Since the potential for exploitation seems improbable but we were able to make a security relevant change, we wanted to issue a reduced reward.
As always, if you can demonstrate a greater potential for exploitability that would result in security implications for a user, we would happily welcome that information and review/reassess this issue for a potentially higher reward.
Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2024-05-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/324690505)*
