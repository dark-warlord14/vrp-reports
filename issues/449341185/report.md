# SEGV_ACCERR in V8

| Field | Value |
|-------|-------|
| **Issue ID** | [449341185](https://issues.chromium.org/issues/449341185) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Regexp |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | pt...@chromium.org |
| **Created** | 2025-10-06 |
| **Bounty** | $8,000.00 |

## Description

## Bisect

- Commit: 05f2468756c718612b00908e10885fa2599fef34

```
Commit: 05f2468756c718612b00908e10885fa2599fef34
Commit Message:
commit 05f2468756c718612b00908e10885fa2599fef34
Author: pthier <pthier@chromium.org>
Date:   Fri Aug 29 11:51:13 2025 +0200

    [regexp] Assemble from BC: Implement Visit for special bytecodes
    
    Implement Visit methods for all RegExp bytecodes in the special bytecode
    list (bytecodes that don't have a 1:1 mapping to a method in the
    RegExpMacroAssembler).
    
    Bug: 437003349
    Change-Id: I5959b1f06ad5a3b297e3189ab9d65b798d31e791
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6889011
    Reviewed-by: Jakob Linke <jgruber@chromium.org>
    Commit-Queue: Patrick Thier <pthier@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#102124}

```
## Reproduction

1. Download: `gs://v8-asan/linux-debug/d8-linux-debug-v8-component-102927.zip`
2. Run: `d8 --allow-natives-syntax --regexp-assemble-from-bytecode --stress-compaction poc.js`

## Crash Output

```
----------------------------------------
--------------------------------------------------------------------------------
Received signal 11 SEGV_ACCERR 39b900841c50

==== C stack trace ===============================

/home/sakura/v8/v8/out/fuzzbuild/d8(+0xc0b976)[0x55bdb06eb976]
/lib/x86_64-linux-gnu/libc.so.6(+0x42520)[0x7f9d8c642520]
/home/sakura/v8/v8/out/fuzzbuild/d8(+0x2644cc8)[0x55bdb2124cc8]
/home/sakura/v8/v8/out/fuzzbuild/d8(+0x2644b41)[0x55bdb2124b41]
/home/sakura/v8/v8/out/fuzzbuild/d8(+0x26436a0)[0x55bdb21236a0]
/home/sakura/v8/v8/out/fuzzbuild/d8(+0x264321d)[0x55bdb212321d]
/home/sakura/v8/v8/out/fuzzbuild/d8(+0x2619b7b)[0x55bdb20f9b7b]
/home/sakura/v8/v8/out/fuzzbuild/d8(+0x261afaa)[0x55bdb20fafaa]
/home/sakura/v8/v8/out/fuzzbuild/d8(+0x2610645)[0x55bdb20f0645]
/home/sakura/v8/v8/out/fuzzbuild/d8(+0x2611be4)[0x55bdb20f1be4]
/home/sakura/v8/v8/out/fuzzbuild/d8(+0x261140b)[0x55bdb20f140b]
/home/sakura/v8/v8/out/fuzzbuild/d8(+0x284fffb)[0x55bdb232fffb]
/home/sakura/v8/v8/out/fuzzbuild/d8(+0x284f661)[0x55bdb232f661]
/home/sakura/v8/v8/out/fuzzbuild/d8(+0x5ec28bd)[0x55bdb59a28bd]
[end of stack trace]
Segmentation fault



================================================================================

```

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 1.1 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2025-10-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4856069348065280.

### 24...@project.gserviceaccount.com (2025-10-06)

Testcase 4856069348065280 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=4856069348065280.

### 24...@project.gserviceaccount.com (2025-10-06)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2025-10-06)

ClusterFuzz testcase 4856069348065280 appears to be flaky, updating reproducibility hotlist.

### je...@gmail.com (2025-10-07)

I did some tests, and some additional flags in ClusterFuzz affected the triggering of this vulnerability. Could you directly assign it to @pthier to take a look? I can still reproduce this vulnerability in the latest version, and since it can directly cause a segv, it should be P1/S1.

```
➜  ✗ /tmp/d8-linux-debug-cache/d8-linux-debug-v8-component-102944/d8 --fuzzing --fuzzing --expose-gc --allow-natives-syntax --debug-code --disable-abortjs --omit-quit --disable-in-process-stack-traces --invoke-weak-callbacks --enable-slow-asserts --verify-heap --allow-natives-syntax --regexp-assemble-from-bytecode --stress-compaction poc.js


➜ ✗ /tmp/d8-linux-debug-cache/d8-linux-debug-v8-component-102944/d8  --allow-natives-syntax --regexp-assemble-from-bytecode --stress-compaction poc.js

Received signal 11 SEGV_ACCERR 1a31008404b0

==== C stack trace ===============================

/tmp/d8-linux-debug-cache/d8-linux-debug-v8-component-102944/libv8_libbase.so(_ZN2v84base5debug10StackTraceC1Ev+0x13)[0x7f470dc52d23]
/tmp/d8-linux-debug-cache/d8-linux-debug-v8-component-102944/libv8_libbase.so(+0x4cc7f)[0x7f470dc52c7f]
/lib/x86_64-linux-gnu/libc.so.6(+0x42520)[0x7f4705a42520]
/tmp/d8-linux-debug-cache/d8-linux-debug-v8-component-102944/libv8.so(+0x4d2384d)[0x7f470b12384d]
/tmp/d8-linux-debug-cache/d8-linux-debug-v8-component-102944/libv8.so(_ZN2v88internal19RegExpCodeGenerator5VisitILNS0_14RegExpBytecodeE37EEEvv+0x2f5)[0x7f470b1235b5]
/tmp/d8-linux-debug-cache/d8-linux-debug-v8-component-102944/libv8.so(_ZN2v88internal19RegExpCodeGenerator14VisitBytecodesEv+0x13e)[0x7f470b11a7de]
/tmp/d8-linux-debug-cache/d8-linux-debug-v8-component-102944/libv8.so(_ZN2v88internal19RegExpCodeGenerator8AssembleENS0_12DirectHandleINS0_6StringEEENS_4base5FlagsINS0_10RegExpFlagEiiEE+0x31)[0x7f470b11a5f1]
/tmp/d8-linux-debug-cache/d8-linux-debug-v8-component-102944/libv8.so(_ZN2v88internal10RegExpImpl27CompileIrregexpFromBytecodeEPNS0_7IsolateENS0_12DirectHandleINS0_12IrRegExpDataEEENS4_INS0_6StringEEEb+0x714)[0x7f470b19e8c4]
/tmp/d8-linux-debug-cache/d8-linux-debug-v8-component-102944/libv8.so(_ZN2v88internal10RegExpImpl22EnsureCompiledIrregexpEPNS0_7IsolateENS0_12DirectHandleINS0_12IrRegExpDataEEENS4_INS0_6StringEEEb+0x33c)[0x7f470b19f8dc]
/tmp/d8-linux-debug-cache/d8-linux-debug-v8-component-102944/libv8.so(_ZN2v88internal10RegExpImpl15IrregexpPrepareEPNS0_7IsolateENS0_12DirectHandleINS0_12IrRegExpDataEEENS4_INS0_6StringEEE+0x1c9)[0x7f470b1988d9]
/tmp/d8-linux-debug-cache/d8-linux-debug-v8-component-102944/libv8.so(_ZN2v88internal10RegExpImpl12IrregexpExecEPNS0_7IsolateENS0_12DirectHandleINS0_12IrRegExpDataEEENS4_INS0_6StringEEEiPij+0x4b3)[0x7f470b199a63]
/tmp/d8-linux-debug-cache/d8-linux-debug-v8-component-102944/libv8.so(_ZN2v88internal6RegExp4ExecEPNS0_7IsolateENS0_12DirectHandleINS0_8JSRegExpEEENS4_INS0_6StringEEEiPij+0x23f)[0x7f470b19920f]
/tmp/d8-linux-debug-cache/d8-linux-debug-v8-component-102944/libv8.so(+0x4e928e0)[0x7f470b2928e0]
/tmp/d8-linux-debug-cache/d8-linux-debug-v8-component-102944/libv8.so(_ZN2v88internal18Runtime_RegExpExecEiPmPNS0_7IsolateE+0x84)[0x7f470b292304]
/tmp/d8-linux-debug-cache/d8-linux-debug-v8-component-102944/libv8.so(+0x2b96b3d)[0x7f4708f96b3d]
[end of stack trace]
[2]    2039356 segmentation fault  /tmp/d8-linux-debug-cache/d8-linux-debug-v8-component-102944/d8    poc.js

```

### je...@gmail.com (2025-10-07)

## Vulnerability Overview

This is a use-after-free vulnerability in the V8 engine’s regular-expression JIT compiler. Reproducing it requires enabling both `--regexp-assemble-from-bytecode` and `--stress-compaction`. The fundamental cause is that, while compiling regular-expression bytecode into machine code, the compiler first extracts a raw pointer from the bytecode array. Before that pointer is dereferenced, garbage collection runs, relocating the bytecode array in memory. The raw pointer still references the old address, so dereferencing the dangling pointer ultimately crashes the process.

GDB shows the crash at line 305 of `regexp-code-generator.cc`. The stack trace reveals that the segmentation fault occurs inside `CreateBitTableByteArray` when accessing `table_data[i]`. The signal is SIGSEGV (SEGV\_ACCERR), meaning the address being accessed is valid but no longer permitted—typical use-after-free behavior. At the moment of the crash, the RAX register holds 0x32b5008404b0, the address of the `table_data` pointer that the code attempts to read.

## Technical Details of the Root Cause

The entire trigger path can be reconstructed clearly from the source. When V8 executes a regular expression with `--regexp-assemble-from-bytecode` enabled, it attempts to generate JIT code directly from existing bytecode. This job is handled by the `RegExpCodeGenerator` class. In its constructor, the bytecode array is stored in the member `bytecode_` as a `DirectHandle<TrustedByteArray>`, so the engine’s handle mechanism will automatically update the reference if garbage collection moves the object.

The flaw appears while processing the `CheckBitInTable` bytecode instruction. This instruction needs to determine whether the current character is present in a bit table whose data is embedded directly in the bytecode stream. At line 326 of `regexp-code-generator.cc`, expanding the `INIT` macro invokes `GetArgumentValuesAsTuple`, which eventually returns `pc + offset` at line 225 of `regexp-bytecodes-inl.h`. In other words, the `table_data` variable is a raw pointer into the interior of the `bytecode_` array. Although `bytecode_` itself is a managed handle, `table_data` is merely a `const uint8_t*` and therefore receives no garbage-collection protection.

Immediately afterward, on line 327, the code calls `CreateBitTableByteArray(isolate_, table_data)`. Inside that function, line 297 invokes `isolate->factory()->NewByteArray(RegExpMacroAssembler::kTableSize)` to allocate a new byte array. This allocation is the critical point where garbage collection can occur. With the `--stress-compaction` flag, V8 deliberately triggers garbage collection and heap compaction on every allocation to exercise GC-related code paths.

Of course, even without the flag there is still a chance for garbage collection to run during any allocation.

During the compaction phase, objects in the heap are moved to eliminate fragmentation. The handle `bytecode_` is updated by the garbage collector to point to the bytecode array’s new location. The raw pointer `table_data`, however, was computed from the pre-GC address; the GC has no knowledge of it and leaves it unchanged. Consequently, `table_data` becomes a dangling pointer that still targets the bytecode array’s old address.

When execution reaches line 305 and evaluates `uint8_t byte = table_data[i];`, it dereferences this stale pointer. Under `--stress-compaction`, the old memory page may already have been reclaimed or had its access permissions changed, so the access triggers a segmentation fault. GDB’s register dump confirms that the address 0x32b5008404b0 looks like a legitimate heap address but is actually a dangling reference.

### dc...@chromium.org (2025-10-07)

I'm not sure why Clusterfuzz can't reproduce this–probably some of the mandatory flags are affecting the runtime enough to break the repro case. I can confirm this does crash with the "default" GN args on the fuzzer:

```
is_asan = true
is_clang = true
is_component_build = true
is_debug = true
target_cpu = "x64"
use_remoteexec = true
v8_enable_backtrace = true
v8_enable_google_benchmark = true
v8_enable_slow_dchecks = true
v8_enable_test_features = true
v8_enable_undefined_double = true

```

Symbolized stack:

```
/usr/local/google/home/dcheng/src/v8/v8/out/asan/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f6f112a4ee3]
/usr/local/google/home/dcheng/src/v8/v8/out/asan/libv8_libbase.so(+0x92ced) [0x7f6f112a4ced]
/lib/x86_64-linux-gnu/libc.so.6(+0x3fdf0) [0x7f6f01049df0]
/usr/local/google/home/dcheng/src/v8/v8/out/asan/libv8.so(+0x8223e6f) [0x7f6f0ae23e6f]
/usr/local/google/home/dcheng/src/v8/v8/out/asan/libv8.so(void v8::internal::RegExpCodeGenerator::Visit<(v8::internal::RegExpBytecode)37>()+0x6d3) [0x7f6f0ae236f3]
/usr/local/google/home/dcheng/src/v8/v8/out/asan/libv8.so(v8::internal::RegExpCodeGenerator::VisitBytecodes()+0x302) [0x7f6f0ae0b8b2]
/usr/local/google/home/dcheng/src/v8/v8/out/asan/libv8.so(v8::internal::RegExpCodeGenerator::Assemble(v8::internal::DirectHandle<v8::internal::String>, v8::base::Flags<v8::internal::RegExpFlag, int, int>)+0x105) [0x7f6f0ae059b5]
/usr/local/google/home/dcheng/src/v8/v8/out/asan/libv8.so(v8::internal::RegExpImpl::CompileIrregexpFromBytecode(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::IrRegExpData>, v8::internal::DirectHandle<v8::internal::String>, bool)+0xd3e) [0x7f6f0af1afbe]
/usr/local/google/home/dcheng/src/v8/v8/out/asan/libv8.so(v8::internal::RegExpImpl::EnsureCompiledIrregexp(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::IrRegExpData>, v8::internal::DirectHandle<v8::internal::String>, bool)+0x663) [0x7f6f0af1d793]
/usr/local/google/home/dcheng/src/v8/v8/out/asan/libv8.so(v8::internal::RegExpImpl::IrregexpPrepare(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::IrRegExpData>, v8::internal::DirectHandle<v8::internal::String>)+0x417) [0x7f6f0af0e107]
/usr/local/google/home/dcheng/src/v8/v8/out/asan/libv8.so(v8::internal::RegExpImpl::IrregexpExec(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::IrRegExpData>, v8::internal::DirectHandle<v8::internal::String>, int, int*, unsigned int)+0x973) [0x7f6f0af108c3]
/usr/local/google/home/dcheng/src/v8/v8/out/asan/libv8.so(v8::internal::RegExp::Exec(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSRegExp>, v8::internal::DirectHandle<v8::internal::String>, int, int*, unsigned int)+0x462) [0x7f6f0af0f6f2]
/usr/local/google/home/dcheng/src/v8/v8/out/asan/libv8.so(+0x84fcab8) [0x7f6f0b0fcab8]
/usr/local/google/home/dcheng/src/v8/v8/out/asan/libv8.so(v8::internal::Runtime_RegExpExec(int, unsigned long*, v8::internal::Isolate*)+0x163) [0x7f6f0b0fbf03]
/usr/local/google/home/dcheng/src/v8/v8/out/asan/libv8.so(+0x4b8db3d) [0x7f6f0778db3d]

```

And that the blamed revision above is accurate.

Note that the Severity / FoundIn are provisional; the v8 shepherd will update these values as appropriate.

Edit: sorry just saw the comment above. Sorry, there were quite a few v8 bugs that required manual action this shift, so I was going through them all in bulk. I did think this bug was likely to be valid; it's just easier to do all the v8 bugs that Clusterfuzz can't help with in a batch.

### dc...@chromium.org (2025-10-07)

@pa...@google.com can you help with setting the FoundIn / severity appropriately? Thanks!

### pt...@chromium.org (2025-10-07)

Please set `Security_Impact-None`. The new feature `--regexp-assemble-from-bytecode` required for this issue is off by default.

### ml...@chromium.org (2025-10-07)

Setting to `Security_Impact-None` as it requires a flag that is default off (see [comment #10](https://issues.chromium.org/issues/449341185#comment10)).

### dx...@google.com (2025-10-07)

Project: v8/v8  

Branch:  main  

Author:  pthier [pthier@chromium.org](mailto:pthier@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7016609>

[regexp] Make Bytecode operand value getters GC safe

---


Expand for full commit details
```
     
    The getter for BitTable previously returned a raw pointer to embedded 
    data within the Bytecode. This is not GC safe, as the pointer will 
    become stale whenever the Bytecode is moved during GC. 
     
    To prevent this, the existing value getters now require a 
    DisallowGarbageCollection scope. 
    In addition new variants of the getters are added that are GC-safe 
    (operate on and return handles). 
     
    Fixed: 449341185 
    Change-Id: I53f0e8d961bc916ca35228b74b2aad9253e7c69d 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7016609 
    Commit-Queue: Patrick Thier <pthier@chromium.org> 
    Reviewed-by: Jakob Linke <jgruber@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#102983}

```

---

Files:

- M `src/regexp/regexp-bytecodes-inl.h`
- M `src/regexp/regexp-code-generator.cc`
- M `src/regexp/regexp-code-generator.h`
- A `test/mjsunit/regress/regress-449341185.js`

---

Hash: [3f4d6ecc29da3d483ac5ce04e6d6fd7c4e177813](https://chromiumdash.appspot.com/commit/3f4d6ecc29da3d483ac5ce04e6d6fd7c4e177813)  

Date: Tue Oct 7 14:38:57 2025


---

### sp...@google.com (2025-10-17)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
baseline memory corruption in sandboxed process + bisect


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-01-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2026-01-15)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

## Bounty Award

> baseline memory corruption in sandboxed process + bisect

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/449341185)*
