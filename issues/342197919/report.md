# Security: SEGV in v8_wasm_compile_fuzzer 

| Field | Value |
|-------|-------|
| **Issue ID** | [342197919](https://issues.chromium.org/issues/342197919) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Linux |
| **Reporter** | al...@goodmanemail.com |
| **Assignee** | ml...@chromium.org |
| **Created** | 2024-05-23 |
| **Bounty** | $7,000.00 |

## Description

VULNERABILITY DETAILS
SUMMARY: AddressSanitizer: SEGV setup-isolate-deserialize.cc in Builtins_WasmStringViewWtf16GetCodeUnit

This crash looks identical to https://issues.chromium.org/issues/41486636 ?

VERSION
Chrome Version: Chromium 6f0dc3ab6cf1ce47753ccefdf91988e1f206976c v8 d525711f9276a3913d4da7462f6f41a2d5bc12d1
Operating System: Ubuntu 22.04

MY ANALYSIS
It seems to be trying an unprotected load/read, at a fixed offset from the wasm null object.  In the linked case which appears to be extremely similar it turned out with some more skills and a carefully crafted test case you could cause type confusion which is obviously a scary security issue.  Maybe I found another avenue for the same issue?  Later on I will attempt to modify the example test case from that bug to see if I can hit the issue found in this new fuzzing session...

BISECT
I bisected back as far as V8 0310305059014b3dafe808364b382fa5923a6a23 using the fuzzer and it still replicates. I didnt go back any further as I think this squarely puts us in security impact stable territory and I believe that is all you care about.

If I had to guess I would say it probably goes back to this commit: https://chromium.googlesource.com/chromium/src/+log/4ad7243588ecd2115fe8799d7c337ce6e8f7a6f1..0d6f8824abe227506c93e4a834ec03f5ea768821?pretty=fuller&n=10000

REPRODUCTION CASE

I've not managed to figure out the magical flags required to get this to replicate in d8 :-( So I attach test case for v8_wasm_code_fuzzer.

// Copyright 2024 the V8 project authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// Flags: --wasm-staging

d8.file.execute('test/mjsunit/wasm/wasm-module-builder.js');

const builder = new WasmModuleBuilder();
let $sig0 = builder.addType(kSig_i_iii);
let $main = builder.addFunction(undefined, $sig0).exportAs('main');
let $mem0 = builder.addMemory(0, 32);

// func $main: [kWasmI32, kWasmI32, kWasmI32] -> [kWasmI32]
$main.addBody([
    kExprLoop, kWasmI32,
      kExprI32Const, 1,
      kExprLocalGet, 0,  // $var0
      kExprBrIf, 0,
      kExprNop,
      kExprI32Clz,
      kExprNop,
      kExprRefNull, kNullRefCode,
      kExprRefAsNonNull,
      ...wasmI32Const(-63),
      ...GCInstr(kExprStringViewWtf16GetCodeunit),
      kExprMemoryGrow, $mem0,
      kExprBr, 0,
    kExprEnd,
  ]);

let kBuiltins = { builtins: ['js-string', 'text-decoder', 'text-encoder'] };
const instance = builder.instantiate({}, kBuiltins);
try {
  print(instance.exports.main(1, 2, 3));
} catch (e) {
  print('caught exception', e);
}

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: SEGV Read
Crash State: 
$ /home/alan/chromium/src/out/libfuzzerasandbg/v8_wasm_code_fuzzer --liftoff-only crash-7cb96685df58c2f6af2abfd2650870eca7764fa7
INFO: Running with entropic power schedule (0xFF, 100).
INFO: Seed: 3331165639
INFO: Loaded 10 modules   (1659692 inline 8-bit counters): 23604 [0x7fd1dcbd03c0, 0x7fd1dcbd5ff4), 2522 [0x7fd1dc372130, 0x7fd1dc372b0a), 38358 [0x7fd1dd40e0f0, 0x7fd1dd4176c6), 54256 [0x7fd1ddfb9620, 0x7fd1ddfc6a10), 25140 [0x7fd1de6c1c10, 0x7fd1de6c7e44), 88633 [0x7fd1dfc3c130, 0x7fd1dfc51b69), 5963 [0x7fd1dfef89f0, 0x7fd1dfefa13b), 2547 [0x7fd1dfe1b490, 0x7fd1dfe1be83), 1410219 [0x7fd1eb90d280, 0x7fd1eba6572b), 8450 [0x5651a4e7bc40, 0x5651a4e7dd42), 
INFO: Loaded 10 PC tables (1659692 PCs): 23604 [0x7fd1dcbd5ff8,0x7fd1dcc32338), 2522 [0x7fd1dc372b10,0x7fd1dc37c8b0), 38358 [0x7fd1dd4176c8,0x7fd1dd4ad428), 54256 [0x7fd1ddfc6a10,0x7fd1de09a910), 25140 [0x7fd1de6c7e48,0x7fd1de72a188), 88633 [0x7fd1dfc51b70,0x7fd1dfdabf00), 5963 [0x7fd1dfefa140,0x7fd1dff115f0), 2547 [0x7fd1dfe1be88,0x7fd1dfe25db8), 1410219 [0x7fd1eba65730,0x7fd1ecfea1e0), 8450 [0x5651a4e7dd48,0x5651a4e9ed68), 
/home/alan/chromium/src/out/libfuzzerasandbg/v8_wasm_code_fuzzer: Running 1 inputs 1 time(s) each.
Running: crash-7cb96685df58c2f6af2abfd2650870eca7764fa7
AddressSanitizer:DEADLYSIGNAL
=================================================================
==1872902==ERROR: AddressSanitizer: SEGV on unknown address 0x7ea100010004 (pc 0x7fd1e46af24a bp 0x7ffe969d0680 sp 0x7ffe969d0648 T0)
==1872902==The signal is caused by a READ memory access.
    #0 0x7fd1e46af24a in Builtins_WasmStringViewWtf16GetCodeUnit setup-isolate-deserialize.cc
    #1 0x7fd1dc6d58bb  (<unknown module>)
    #2 0x7fd1e410d149 in Builtins_JSToWasmWrapperAsm setup-isolate-deserialize.cc
    #3 0x7fd1e468f8a9 in Builtins_JSToWasmWrapper setup-isolate-deserialize.cc
    #4 0x7fd1e3daa3db in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #5 0x7fd1e3daa11e in Builtins_JSEntry setup-isolate-deserialize.cc
    #6 0x7fd1e53772e4 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/simulator.h:178:12
    #7 0x7fd1e5373c6c in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution/execution.cc:505:10
    #8 0x5651a4e38736 in v8::internal::wasm::testing::CallWasmFunctionForTesting(v8::internal::Isolate*, v8::internal::Handle<v8::internal::WasmInstanceObject>, char const*, v8::base::Vector<v8::internal::Handle<v8::internal::Object>>, std::__Cr::unique_ptr<char const [], std::__Cr::default_delete<char const []>>*) v8/test/common/wasm/wasm-module-runner.cc:125:32
    #9 0x5651a4dd0204 in v8::internal::wasm::fuzzing::ExecuteAgainstReference(v8::internal::Isolate*, v8::internal::Handle<v8::internal::WasmModuleObject>, int) v8/test/fuzzer/wasm-fuzzer-common.cc:218:20
    #10 0x5651a4de53b5 in v8::internal::wasm::fuzzing::WasmExecutionFuzzer::FuzzWasmModule(v8::base::Vector<unsigned char const>, bool) v8/test/fuzzer/wasm-fuzzer-common.cc:401:5
    #11 0x5651a4cbbd66 in LLVMFuzzerTestOneInput v8/test/fuzzer/wasm-code.cc:34:20
    #12 0x5651a4d4a670 in fuzzer::Fuzzer::ExecuteCallback(unsigned char const*, unsigned long) third_party/libFuzzer/src/FuzzerLoop.cpp:614:13
    #13 0x5651a4cf490b in fuzzer::RunOneTest(fuzzer::Fuzzer*, char const*, unsigned long) third_party/libFuzzer/src/FuzzerDriver.cpp:327:6
    #14 0x5651a4cf9ea6 in fuzzer::FuzzerDriver(int*, char***, int (*)(unsigned char const*, unsigned long)) third_party/libFuzzer/src/FuzzerDriver.cpp:862:9
    #15 0x5651a4cc21f3 in main third_party/libFuzzer/src/FuzzerMain.cpp:20:10
    #16 0x7fd1dc3a6d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV setup-isolate-deserialize.cc in Builtins_WasmStringViewWtf16GetCodeUnit
==1872902==ABORTING

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: Alan Goodman

## Attachments

- [minimized-from-e1bec3281557a305d356a98bfc6b88e6d148124d](attachments/minimized-from-e1bec3281557a305d356a98bfc6b88e6d148124d) (application/octet-stream, 20 B)

## Timeline

### ps...@google.com (2024-05-23)

I was unable to reproduce with cluster fuzz using linux_asan_chrome_mp, so I am going to kick this over to V8 shepherd. 

### al...@goodmanemail.com (2024-05-23)

If you're having difficulty reproducing it then it may be worth trying it with --predictable and --single-threaded as these were set in the fuzzing session.  Ensure that you are starting it as a v8_wasm_code_fuzzer job if using the attached test case; or the correct flags + bundled with the wasm-module-builder.js if using the js test case.  If replicating in d8 please could you share the correct flags here as would be useful to me as I spent some time trying to get a repro in d8 without luck.

### al...@goodmanemail.com (2024-05-23)

I did spend some time this evening trying to see if I could replicate the type confusion from the other bug somehow but ultimately could not.  Dont take that as it not being possible though because I have almost zero skills in this area.

I ran the test case through my blind / brute force and ignorance testcase mutator paying special attention to offset 13 in the test case to ensure I tested other single byte opcodes but only 9a "kExprStringViewWtf16GetCodeunit" is triggering the crash for me.

Looking at the structure of the test case it looks like it started out with \xfb\xcf\x9a in there, which is a 'truple' from the dictionary which I added based on my understanding of the limited number of three byte strings that were valid.  The mutator has decided to delete the 0xCF from the middle leaving 0xFB 0x9A which seems to translate to GCInstr(kExprStringViewWtf16GetCodeunit).  Based on this it seems I should add \xfb\xsomething to my dictionary?  Perhaps xfb\x{every single byte opcode}?  Remembering that due to the modifications I've made to the fuzz mutator; the only source of 'new' data my session has is the dictionary.  I am doing this because I want to reduce the search space; as the search space is so enormous.  This crash was detected using my modified mutator + my hand built dictionary and your otherwise vanilla code fuzzer.  I swapped from v8_wasm_fuzzer to v8_wasm_code_fuzzer because the latter seems to add some commonly missed bits of code to the input module if they are missing and in my testing this massively increases the efficiency of the fuzzer.  This crash was found within 6 hours of starting, using just 56 cores and with a blank starting corpus.

### al...@goodmanemail.com (2024-05-23)

I should note that \xfb and \x9a are in the dictionary as singular terms as well; its just not how this testcase appears to have been 'born'.

### cf...@google.com (2024-05-24)

So it seems to be type confusion where it treats the WasmNull object as a String [here](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/builtins/wasm.tq;l=1245;drc=61453e50c45e6048bf1a2ba62e3dc8db9578beb0).  

I am unsure if there can be other confusions but if this is only a confusion with a String, then this should always safely crash as the WasmNull object is located at the end of a page and trying to load a length field (or any other field besides accessing the map) will always result in a trap in the guard page behind the WasmNull object.\

jkummerow@, could you PTAL?

### al...@goodmanemail.com (2024-05-24)

I think its an optimisation/compiler bug because its only exhibiting the type confusion behaviour (eg crashing) when ran with liftoff.  Turboshaft isnt doing it.

$ /home/alan/chromium/src/out/libfuzzerasandbg/v8_wasm_code_fuzzer --no-liftoff --turboshaft-wasm crash-segvreadmin
INFO: Running with entropic power schedule (0xFF, 100).
INFO: Seed: 234369098
INFO: Loaded 10 modules   (1659692 inline 8-bit counters): 23604 [0x7f45efab33c0, 0x7f45efab8ff4), 2522 [0x7f45ef255130, 0x7f45ef255b0a), 38358 [0x7f45f02f10f0, 0x7f45f02fa6c6), 54256 [0x7f45f0e9c620, 0x7f45f0ea9a10), 25140 [0x7f45f15a4c10, 0x7f45f15aae44), 88633 [0x7f45f2b1f130, 0x7f45f2b34b69), 5963 [0x7f45f2ddb9f0, 0x7f45f2ddd13b), 2547 [0x7f45f2cfe490, 0x7f45f2cfee83), 1410219 [0x7f45fe7f0280, 0x7f45fe94872b), 8450 [0x5585a81f0c40, 0x5585a81f2d42), 
INFO: Loaded 10 PC tables (1659692 PCs): 23604 [0x7f45efab8ff8,0x7f45efb15338), 2522 [0x7f45ef255b10,0x7f45ef25f8b0), 38358 [0x7f45f02fa6c8,0x7f45f0390428), 54256 [0x7f45f0ea9a10,0x7f45f0f7d910), 25140 [0x7f45f15aae48,0x7f45f160d188), 88633 [0x7f45f2b34b70,0x7f45f2c8ef00), 5963 [0x7f45f2ddd140,0x7f45f2df45f0), 2547 [0x7f45f2cfee88,0x7f45f2d08db8), 1410219 [0x7f45fe948730,0x7f45ffecd1e0), 8450 [0x5585a81f2d48,0x5585a8213d68), 
/home/alan/chromium/src/out/libfuzzerasandbg/v8_wasm_code_fuzzer: Running 1 inputs 1 time(s) each.
Running: crash-segvreadmin
Executed crash-segvreadmin in 78 ms
***
*** NOTE: fuzzing was not performed, you have only
***       executed the target code on a fixed set of inputs.
***
alan@dl360p10fuzz:~/v8_wasm_code_fuzzer/expo$ /home/alan/chromium/src/out/libfuzzerasandbg/v8_wasm_code_fuzzer --liftoff-only crash-segvreadmin
INFO: Running with entropic power schedule (0xFF, 100).
INFO: Seed: 240458428
INFO: Loaded 10 modules   (1659692 inline 8-bit counters): 23604 [0x7f42a053d3c0, 0x7f42a0542ff4), 2522 [0x7f429fcdf130, 0x7f429fcdfb0a), 38358 [0x7f42a0d7b0f0, 0x7f42a0d846c6), 54256 [0x7f42a1926620, 0x7f42a1933a10), 25140 [0x7f42a202ec10, 0x7f42a2034e44), 88633 [0x7f42a35a9130, 0x7f42a35beb69), 5963 [0x7f42a38659f0, 0x7f42a386713b), 2547 [0x7f42a3788490, 0x7f42a3788e83), 1410219 [0x7f42af27a280, 0x7f42af3d272b), 8450 [0x55968035cc40, 0x55968035ed42), 
INFO: Loaded 10 PC tables (1659692 PCs): 23604 [0x7f42a0542ff8,0x7f42a059f338), 2522 [0x7f429fcdfb10,0x7f429fce98b0), 38358 [0x7f42a0d846c8,0x7f42a0e1a428), 54256 [0x7f42a1933a10,0x7f42a1a07910), 25140 [0x7f42a2034e48,0x7f42a2097188), 88633 [0x7f42a35beb70,0x7f42a3718f00), 5963 [0x7f42a3867140,0x7f42a387e5f0), 2547 [0x7f42a3788e88,0x7f42a3792db8), 1410219 [0x7f42af3d2730,0x7f42b09571e0), 8450 [0x55968035ed48,0x55968037fd68), 
/home/alan/chromium/src/out/libfuzzerasandbg/v8_wasm_code_fuzzer: Running 1 inputs 1 time(s) each.
Running: crash-segvreadmin
AddressSanitizer:DEADLYSIGNAL
=================================================================
==1926622==ERROR: AddressSanitizer: SEGV on unknown address 0x7e3a00010004 (pc 0x7f42a801c24a bp 0x7ffffec17cc0 sp 0x7ffffec17c88 T0)
==1926622==The signal is caused by a READ memory access.
    #0 0x7f42a801c24a in Builtins_WasmStringViewWtf16GetCodeUnit setup-isolate-deserialize.cc
    #1 0x7f42a00428bb  (<unknown module>)
    #2 0x7f42a7a7a149 in Builtins_JSToWasmWrapperAsm setup-isolate-deserialize.cc
    #3 0x7f42a7ffc8a9 in Builtins_JSToWasmWrapper setup-isolate-deserialize.cc
    #4 0x7f42a77173db in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #5 0x7f42a771711e in Builtins_JSEntry setup-isolate-deserialize.cc
    #6 0x7f42a8ce42e4 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/simulator.h:178:12
    #7 0x7f42a8ce0c6c in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution/execution.cc:505:10
    #8 0x559680319736 in v8::internal::wasm::testing::CallWasmFunctionForTesting(v8::internal::Isolate*, v8::internal::Handle<v8::internal::WasmInstanceObject>, char const*, v8::base::Vector<v8::internal::Handle<v8::internal::Object>>, std::__Cr::unique_ptr<char const [], std::__Cr::default_delete<char const []>>*) v8/test/common/wasm/wasm-module-runner.cc:125:32
    #9 0x5596802b1204 in v8::internal::wasm::fuzzing::ExecuteAgainstReference(v8::internal::Isolate*, v8::internal::Handle<v8::internal::WasmModuleObject>, int) v8/test/fuzzer/wasm-fuzzer-common.cc:218:20
    #10 0x5596802c63b5 in v8::internal::wasm::fuzzing::WasmExecutionFuzzer::FuzzWasmModule(v8::base::Vector<unsigned char const>, bool) v8/test/fuzzer/wasm-fuzzer-common.cc:401:5
    #11 0x55968019cd66 in LLVMFuzzerTestOneInput v8/test/fuzzer/wasm-code.cc:34:20
    #12 0x55968022b670 in fuzzer::Fuzzer::ExecuteCallback(unsigned char const*, unsigned long) third_party/libFuzzer/src/FuzzerLoop.cpp:614:13
    #13 0x5596801d590b in fuzzer::RunOneTest(fuzzer::Fuzzer*, char const*, unsigned long) third_party/libFuzzer/src/FuzzerDriver.cpp:327:6
    #14 0x5596801daea6 in fuzzer::FuzzerDriver(int*, char***, int (*)(unsigned char const*, unsigned long)) third_party/libFuzzer/src/FuzzerDriver.cpp:862:9
    #15 0x5596801a31f3 in main third_party/libFuzzer/src/FuzzerMain.cpp:20:10
    #16 0x7f429fd13d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV setup-isolate-deserialize.cc in Builtins_WasmStringViewWtf16GetCodeUnit
==1926622==ABORTING


### pe...@google.com (2024-05-24)

Setting milestone because of s0/s1 severity.

### jk...@chromium.org (2024-05-24)

It's a Turbofan bug; the fact that the `v8_wasm_code_fuzzer` binary appears to trigger it with `--liftoff-only` is a red herring as the fuzzer binaries have special tiering mechanics.

I think it's pretty hard/unlikely to hit this bug in practice; and I *think* (but am not very sure) that it's not exploitable because AFAICT it only happens for `null` values, and only accesses a fixed offset (7).

The testcase in #1 does reproduce it in d8, with `--wasm-staging --no-liftoff`. I could even slightly simplify it to:

```
let builder = new WasmModuleBuilder();

let $mem0 = builder.addMemory(0, 32);
builder.addFunction("main", kSig_i_i).exportFunc().addBody([
    kExprLoop, kWasmI32,
      kExprLocalGet, 0,
      kExprBrIf, 0,
      kExprRefNull, kNullRefCode,
      kExprRefAsNonNull,
      ...wasmI32Const(0),
      ...GCInstr(kExprStringViewWtf16GetCodeunit),
      kExprMemoryGrow, $mem0,
      kExprBr, 0,
    kExprEnd,
  ]);

const instance = builder.instantiate();
try {
  print(instance.exports.main(0));
} catch (e) {
  print('caught exception', e);
}

```

Unfortunately I can't check this in as a regression test, because its correct behavior is an endless loop, and if I change it to not be an endless loop any more, then it also doesn't reproduce the crash any more.

Fix: <https://chromium-review.googlesource.com/c/v8/v8/+/5569137>

Re #4, I don't know what kind of "valid string" the sequence `fb cf 9a` is supposed to be. `fb 9a 01` is `stringview_wtf16.get_codeunit`. You can find the list of all valid opcodes in the upstream spec or V8's `wasm-opcodes.h`. Note that prefixed opcodes (=all multi-byte opcodes) are encoded as "prefix + LEB", where "LEB" means "each byte has 7 bits payload, and the 8th / most-significant bit indicates whether there's another byte coming". For example, to encode the hypothetical opcode `0xfb123`, first chop off the prefix, then split the `123` part into 7-bit chunks: `0x123 = 0b0001_0010_0011 = 0b00010 0b0100011`, then store them in little-endian order with appropriate "next-byte bits": `(0x80 | 0b0100011), (0x00 | 0b00010)`, so the final encoding is `fb a3 02`.

### al...@goodmanemail.com (2024-05-24)

Thanks.  I can confirm the patch prevents the crash and fixes all reproducers for it that are in my queue.  The Dcheck (reported separately) thats in my queue is still reproduced.

Re exploitability, I wish I could tell you more, but sadly its all way above my head.  Maybe one day :-/  I will try to adjust my 'truples' list based on the above as my initial attempt was clearly off the mark!

### al...@goodmanemail.com (2024-05-24)

Mucking about with the brute force mutator this evening trying to figure out if altering the bytes before the getcodeunit would influence the behaviour but then while looking at the results I figure that this issue wont necesarily cause the fuzzer/d8 to crash because reading offset from other builtins probably doesnt cause an out of bounds read, however never the less could still be reading areas of memory that we should not be?  Case in point the previous issue that I found which caused an OOB read offset from the null object was turned into a PoC that didnt blow up d8; but did exhibit 'undefined behavior'.  Anyhow; I dont think I have any relevant skills to figure this out; sadly.

### ap...@google.com (2024-05-27)

Project: v8/v8
Branch: main

commit ca6d6bdbbb4603b7940e909621b0b88991021201
Author: Jakob Kummerow <jkummerow@chromium.org>
Date:   Fri May 24 18:22:55 2024

    [wasm][turbofan] kPure != kEliminatable
    
    For some string-related operations, the difference between "kPure"
    (=doesn't depend on effects) and "kEliminatable" (=does depend on
    effects, hence cannot be rescheduled across control flow) matters.
    
    No regression test because the only repro I know of turns into an
    endless loop when the bug is fixed.
    
    Fixed: 342197919
    Change-Id: Id57771e3bbdf0c4e432b21effb31fb2a2e983262
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5569137
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#94096}

M       src/compiler/turboshaft/builtin-call-descriptors.h
M       src/compiler/wasm-compiler.cc
M       src/compiler/wasm-gc-lowering.cc

https://chromium-review.googlesource.com/5569137


### pe...@google.com (2024-05-27)

This is sufficiently serious that it should be merged to stable. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M125. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to beta. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M126. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### pe...@google.com (2024-05-28)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=342197919&entry.958145677=Linux&entry.763880440=Stable&entry.1678852700=High&entry.763402679=Blink>JavaScript&entry.975983575=jkummerow@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

### pe...@google.com (2024-05-28)

Merge review required: M126 is already shipping to beta.

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
Owners: govind (Android), govind (iOS), ceb (ChromeOS), srinivassista (Desktop)

### pe...@google.com (2024-05-28)

Merge review required: M125 is already shipping to stable.

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
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

### am...@chromium.org (2024-05-28)

It appears non default flags are needed to trigger this; updating as SI-None and removing merge tags

### am...@chromium.org (2024-05-29)

Thank you for the report, Alan. Since this does not appear to be an exploitable security issue, this report is unfortunately not eligible for a Chrome VRP reward.

### pe...@google.com (2024-09-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/342197919)*
