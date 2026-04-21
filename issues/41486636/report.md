# Security: SEGV in v8_wasm_compile_fuzzer 

| Field | Value |
|-------|-------|
| **Issue ID** | [41486636](https://issues.chromium.org/issues/41486636) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Linux |
| **Reporter** | al...@goodmanemail.com |
| **Assignee** | ml...@chromium.org |
| **Created** | 2023-12-24 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**  

SEGV in v8\_wasm\_compile\_fuzzer unknown module

**VERSION**  

v8 0310305059014b3dafe808364b382fa5923a6a23

**REPRODUCTION CASE**  

I've tried to minimize the crash and reproduce in d8; however I've been able to. Attached test case is for chromium v8\_wasm\_compile\_fuzzer. I did spend some time trying to get my head around what is going on to cause the crash and all I could figure out was that it doesnt appear to be a null deref; therefore I am reporting as security as I am uncertain.

# $ /home/alan/chromium/src/out/libfuzzerasan/v8\_wasm\_compile\_fuzzer crash-orig-mod INFO: Running with entropic power schedule (0xFF, 100). INFO: Seed: 2838797619 INFO: Loaded 1 modules (1357575 inline 8-bit counters): 1357575 [0x55ce602c75e0, 0x55ce60412ce7), INFO: Loaded 1 PC tables (1357575 PCs): 1357575 [0x55ce60412ce8,0x55ce618c9d58), /home/alan/chromium/src/out/libfuzzerasan/v8\_wasm\_compile\_fuzzer: Running 1 inputs 1 time(s) each. Running: crash-orig-mod AddressSanitizer:DEADLYSIGNAL

==27904==ERROR: AddressSanitizer: SEGV on unknown address 0x7e8b00010004 (pc 0x7f93f40d30f9 bp 0x7ffd8c92dc48 sp 0x7ffd8c92dc20 T0)  

==27904==The signal is caused by a READ memory access.  

#0 0x7f93f40d30f9 (<unknown module>)  

#1 0x55ce5ee7c189 in Builtins\_JSToWasmWrapperAsm setup-isolate-deserialize.cc  

#2 0x55ce5efa0ad9 in Builtins\_JSToWasmWrapper setup-isolate-deserialize.cc  

#3 0x55ce5edda4db in Builtins\_JSEntryTrampoline setup-isolate-deserialize.cc  

#4 0x55ce5edda206 in Builtins\_JSEntry setup-isolate-deserialize.cc  

#5 0x55ce58d1fcb8 in Call v8/src/execution/simulator.h:178:12  

#6 0x55ce58d1fcb8 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:418:22  

#7 0x55ce58d1d6fe in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution/execution.cc:504:10  

#8 0x55ce5f039e67 in v8::internal::wasm::testing::CallWasmFunctionForTesting(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::WasmInstanceObject](javascript:void(0);), char const\*, v8::base::Vector<v8::internal::Handle[v8::internal::Object](javascript:void(0);)>, std::\_\_Cr::unique\_ptr<char const [], std::\_\_Cr::default\_delete<char const []>>\*) v8/test/common/wasm/wasm-module-runner.cc:125:32  

#9 0x55ce5f00c9ee in v8::internal::wasm::fuzzer::ExecuteAgainstReference(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::WasmModuleObject](javascript:void(0);), int) v8/test/fuzzer/wasm-fuzzer-common.cc:173:20  

#10 0x55ce5f017f17 in v8::internal::wasm::fuzzer::WasmExecutionFuzzer::FuzzWasmModule(v8::base::Vector<unsigned char const>, bool) v8/test/fuzzer/wasm-fuzzer-common.cc:906:5  

#11 0x55ce581672c0 in LLVMFuzzerTestOneInput v8/test/fuzzer/wasm-compile.cc:3523:23  

#12 0x55ce5824aa89 in fuzzer::Fuzzer::ExecuteCallback(unsigned char const\*, unsigned long) third\_party/libFuzzer/src/FuzzerLoop.cpp:614:13  

#13 0x55ce58219b56 in fuzzer::RunOneTest(fuzzer::Fuzzer\*, char const\*, unsigned long) third\_party/libFuzzer/src/FuzzerDriver.cpp:327:6  

#14 0x55ce58223f44 in fuzzer::FuzzerDriver(int\*, char\*\*\*, int (\*)(unsigned char const\*, unsigned long)) third\_party/libFuzzer/src/FuzzerDriver.cpp:862:9  

#15 0x55ce5820637d in main third\_party/libFuzzer/src/FuzzerMain.cpp:20:10  

#16 0x7f93f3c23a8f in \_\_libc\_start\_call\_main csu/../sysdeps/nptl/libc\_start\_call\_main.h:58:16

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: SEGV (<unknown module>)  

==27904==ABORTING

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Alan Goodman

## Attachments

- [crash-orig](attachments/crash-orig) (text/plain, 60 B)
- [repro-issue.js](attachments/repro-issue.js) (text/plain, 2.7 KB)

## Timeline

### [Deleted User] (2023-12-24)

[Empty comment from Monorail migration]

### al...@goodmanemail.com (2023-12-24)

13a14ca96037793631f38b92118b1d08002da0c1 is the first bad commit
commit 13a14ca96037793631f38b92118b1d08002da0c1
Author: Andreas Haas <ahaas@chromium.org>
Date:   Thu Nov 23 14:51:26 2023 +0100

    [wasm] Don't cache memory size of growable shared memory
    
    With this CL the memory size of growable shared memory does not get
    cached anymore. The cache would have to be invalidated on stack checks
    that handle interrupts, and this is difficult to implement at the
    moment. Caching the memory size for growable shared memory does not seem
    important at the moment, because it is only relevant on multi-threaded
    apps on 32-bit platforms, which by itself is not a high-priority
    combination.
    
    This CL also removes the lowering of stack checks during graph
    construction.
    
    Bug: v8:14108
    Change-Id: Ic3d21b72e3b94140d5b1f27b615d4e883dfb1bd0
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5056833
    Reviewed-by: Manos Koukoutos <manoskouk@chromium.org>
    Commit-Queue: Andreas Haas <ahaas@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#91153}

 src/wasm/turboshaft-graph-interface.cc | 106 +++++++++------------------------
 1 file changed, 27 insertions(+), 79 deletions(-)
bisect found first bad commit

### ts...@chromium.org (2023-12-26)

Provisionally setting severity high and foundin extended, assigning per V8 rotation.

[Monorail components: Blink>JavaScript]

### [Deleted User] (2023-12-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-27)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-27)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2023-12-29)

[Empty comment from Monorail migration]

### al...@goodmanemail.com (2024-01-04)

This crash appears to possibly involve memory corruption as the location its trying to read is different every time; additionally in the no sanitizers build I am fuzzing with the instruction pointer is getting set to garbage values.

My fuzz session in general is plagued by the below crash which might be related; but is not replicating at all for me.  Leading me to think perhaps my fuzzer is getting into a weird state somehow.  No idea if the below is useful to you; but am including it here in the hope that it could be useful.

#
# Fatal error in ../../v8/src/base/bit-field.h, line 63
# Debug check failed: is_valid(value).
#
#
#
#FailureMessage Object: 0x7fffcc898c30
==== C stack trace ===============================

    /home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x5c37a2d) [0x555ab1f72a2d]
    /home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x5c361e2) [0x555ab1f711e2]
    /home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x5c0c852) [0x555ab1f47852]
    /home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x5c0c1a5) [0x555ab1f471a5]
    /home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x45497da) [0x555ab08847da]
    /home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x4548464) [0x555ab0883464]
    /home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x45474da) [0x555ab08824da]
    /home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x4653a83) [0x555ab098ea83]
    /home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x464cd6b) [0x555ab0987d6b]
    /home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x464b80e) [0x555ab098680e]
    /home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x464b17c) [0x555ab098617c]
    /home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x464ac4f) [0x555ab0985c4f]
    /home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x47f208c) [0x555ab0b2d08c]
    /home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x5b5cfab) [0x555ab1e97fab]
    /home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x26f79e8) [0x555aaea329e8]
    /home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x2752fe1) [0x555aaea8dfe1]
    /home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x2752425) [0x555aaea8d425]
    /home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x2753d16) [0x555aaea8ed16]
    /home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x2754836) [0x555aaea8f836]
    /home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(+0x2743f70) [0x555aaea7ef70]
    /home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(main+0x23) [0x555aaea73483]
    /lib/x86_64-linux-gnu/libc.so.6(+0x23a90) [0x7fb917e23a90]
    /lib/x86_64-linux-gnu/libc.so.6(__libc_start_main+0x89) [0x7fb917e23b49]
    /home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer(_start+0x2a) [0x555aaea1b02a]
==180933== ERROR: libFuzzer: deadly signal
    #0 0x555aaea316e4 in __sanitizer_print_stack_trace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/ubsan/ubsan_diag_standalone.cpp:31:3
    #1 0x555aaeaa5978 in fuzzer::PrintStackTrace() ../../third_party/libFuzzer/src/FuzzerUtil.cpp:210:5
    #2 0x555aaea8c703 in fuzzer::Fuzzer::CrashCallback() ../../third_party/libFuzzer/src/FuzzerLoop.cpp:231:3
    #3 0x7fb917e3c45f  (/lib/x86_64-linux-gnu/libc.so.6+0x3c45f) (BuildId: d320ce4e63925d698610ed423fc4b1f0e8ed51f1)
    #4 0x7fb917e9152a in __pthread_kill_implementation nptl/pthread_kill.c:43:17
    #5 0x7fb917e9152a in __pthread_kill_internal nptl/pthread_kill.c:78:10
    #6 0x7fb917e9152a in pthread_kill nptl/pthread_kill.c:89:10
    #7 0x7fb917e3c3b5 in raise signal/../sysdeps/posix/raise.c:26:13
    #8 0x7fb917e2287b in abort stdlib/abort.c:79:7
    #9 0x555ab1f6bfd9 in v8::base::OS::Abort() ../../v8/src/base/platform/platform-posix.cc:704:3
    #10 0x555ab1f47865 in V8_Fatal(char const*, int, char const*, ...) ../../v8/src/base/logging.cc:181:3
    #11 0x555ab1f471a4 in v8::base::(anonymous namespace)::DefaultDcheckHandler(char const*, int, char const*) ../../v8/src/base/logging.cc:57:3
    #12 0x555ab08847d9 in encode ../../v8/src/base/bit-field.h:63:5
    #13 0x555ab08847d9 in FromIndex ../../v8/src/wasm/value-type.h:414:48
    #14 0x555ab08847d9 in v8::internal::wasm::TypeCanonicalizer::CanonicalizeValueType(v8::internal::wasm::WasmModule const*, v8::internal::wasm::ValueType, unsigned int) const ../../v8/src/wasm/canonical-types.cc:177:16
    #15 0x555ab0883463 in v8::internal::wasm::TypeCanonicalizer::CanonicalizeTypeDef(v8::internal::wasm::WasmModule const*, v8::internal::wasm::TypeDefinition, unsigned int) ../../v8/src/wasm/canonical-types.cc:226:13
    #16 0x555ab08824d9 in v8::internal::wasm::TypeCanonicalizer::AddRecursiveGroup(v8::internal::wasm::WasmModule*, unsigned int, unsigned int) ../../v8/src/wasm/canonical-types.cc:42:22
    #17 0x555ab098ea82 in v8::internal::wasm::ModuleDecoderImpl::DecodeTypeSection() ../../v8/src/wasm/module-decoder-impl.h:685:21
    #18 0x555ab0987d6a in v8::internal::wasm::ModuleDecoderImpl::DecodeSection(v8::internal::wasm::SectionCode, v8::base::Vector<unsigned char const>, unsigned int) ../../v8/src/wasm/module-decoder-impl.h:430:9
    #19 0x555ab098680d in v8::internal::wasm::ModuleDecoderImpl::DecodeModule(bool) ../../v8/src/wasm/module-decoder-impl.h:1695:9
    #20 0x555ab098617b in v8::internal::wasm::DecodeWasmModule(v8::internal::wasm::WasmFeatures, v8::base::Vector<unsigned char const>, bool, v8::internal::wasm::ModuleOrigin, v8::internal::wasm::PopulateExplicitRecGroups) ../../v8/src/wasm/module-decoder.cc:123:18
    #21 0x555ab0985c4e in v8::internal::wasm::DecodeWasmModule(v8::internal::wasm::WasmFeatures, v8::base::Vector<unsigned char const>, bool, v8::internal::wasm::ModuleOrigin, v8::internal::Counters*, std::__Cr::shared_ptr<v8::internal::metrics::Recorder>, v8::metrics::Recorder::ContextId, v8::internal::wasm::DecodingMethod) ../../v8/src/wasm/module-decoder.cc:89:25
    #22 0x555ab0b2d08b in v8::internal::wasm::WasmEngine::SyncValidate(v8::internal::Isolate*, v8::internal::wasm::WasmFeatures, v8::internal::wasm::ModuleWireBytes) ../../v8/src/wasm/wasm-engine.cc:521:17
    #23 0x555ab1e97faa in v8::internal::wasm::fuzzer::WasmExecutionFuzzer::FuzzWasmModule(v8::base::Vector<unsigned char const>, bool) ../../v8/test/fuzzer/wasm-fuzzer-common.cc:878:24
    #24 0x555aaea329e7 in LLVMFuzzerTestOneInput ../../v8/test/fuzzer/wasm-compile.cc:3523:23
    #25 0x555aaea8dfe0 in fuzzer::Fuzzer::ExecuteCallback(unsigned char const*, unsigned long) ../../third_party/libFuzzer/src/FuzzerLoop.cpp:614:13
    #26 0x555aaea8d424 in fuzzer::Fuzzer::RunOne(unsigned char const*, unsigned long, bool, fuzzer::InputInfo*, bool, bool*) ../../third_party/libFuzzer/src/FuzzerLoop.cpp:516:7
    #27 0x555aaea8ed15 in fuzzer::Fuzzer::MutateAndTestOne() ../../third_party/libFuzzer/src/FuzzerLoop.cpp:760:19
    #28 0x555aaea8f835 in fuzzer::Fuzzer::Loop(std::__Cr::vector<fuzzer::SizedFile, std::__Cr::allocator<fuzzer::SizedFile>>&) ../../third_party/libFuzzer/src/FuzzerLoop.cpp:905:5
    #29 0x555aaea7ef6f in fuzzer::FuzzerDriver(int*, char***, int (*)(unsigned char const*, unsigned long)) ../../third_party/libFuzzer/src/FuzzerDriver.cpp:914:6
    #30 0x555aaea73482 in main ../../third_party/libFuzzer/src/FuzzerMain.cpp:20:10
    #31 0x7fb917e23a8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #32 0x7fb917e23b48 in __libc_start_main csu/../csu/libc-start.c:360:3
    #33 0x555aaea1b029 in _start (/home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer+0x26e0029) (BuildId: daa9340f8ac6fc97)

NOTE: libFuzzer has rudimentary signal handlers.
      Combine libFuzzer with AddressSanitizer or similar for better crash reports.
SUMMARY: libFuzzer: deadly signal
MS: 1 CopyPart-; base unit: 97bbce796ee22688a8513c083fea1d8d7adead9a
0x4b,0x2b,0xe7,0xfa,0x91,0x1,0xfc,0xfd,0xd2,0xdf,0x0,0x26,0xf4,0xf7,0x75,0xf,0x1b,0xf4,0xef,0xf4,0x5e,0xf5,0xe6,0x6d,0xf4,0xea,0xf4,0xe,0xf6,0xc2,0xf5,0xe6,0x69,0xf4,0xea,0xf4,0x6,0xf4,0xf7,0x75,0xf,0x1b,0xf4,0xef,0xf4,0x5e,0xf5,0xe6,0x6d,0x0,0xa3,0x2c,0xfd,0xf0,
K+\347\372\221\001\374\375\322\337\000&\364\367u\017\033\364\357\364^\365\346m\364\352\364\016\366\302\365\346i\364\352\364\006\364\367u\017\033\364\357\364^\365\346m\000\243,\375\360
artifact_prefix='./'; Test unit written to ./crash-bb8142636cd94701df1be5f86e545ca98fb6dda7
Base64: Syvn+pEB/P3S3wAm9Pd1Dxv07/Re9eZt9Or0DvbC9eZp9Or0BvT3dQ8b9O/0XvXmbQCjLP3w
alan@dl360g10fuzz:~/libfuzzer_wasm_corpusbuilder3$ /home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer -entropic=0 --single-threaded --predictable --hole-fuzzing crash-bb8142636cd94701df1be5f86e545ca98fb6dda7
INFO: Seed: 2398512755
INFO: Loaded 1 modules   (1384205 inline 8-bit counters): 1384205 [0x55b2b9009928, 0x55b2b915b835), 
INFO: Loaded 1 PC tables (1384205 PCs): 1384205 [0x55b2b915b838,0x55b2ba67a908), 
/home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer: Running 1 inputs 1 time(s) each.
Running: crash-bb8142636cd94701df1be5f86e545ca98fb6dda7
Executed crash-bb8142636cd94701df1be5f86e545ca98fb6dda7 in 3 ms
***
*** NOTE: fuzzing was not performed, you have only
***       executed the target code on a fixed set of inputs.
***


### al...@goodmanemail.com (2024-01-04)

P.S. Also doesnt replicate without --hole-fuzzing; which apparently should be suppressing the dcheck errors?

### [Deleted User] (2024-01-07)

ahaas: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### al...@goodmanemail.com (2024-01-10)

This one is still replicating for me in ToT 3089157cce7a57f9c18b809b513319a632474799 using v8_simple_wasm_compile_fuzzer likewise in Chromium  ToT and v8_wasm_compile_fuzzer

Should you wish to run it through CF; there is a v8_wasm_compile_fuzzer target; I tested it on ASAN Debug build and its triggering there for me too.

### ah...@chromium.org (2024-01-15)

I can reproduce the crash in the fuzzer, but not in d8 yet.

### cl...@chromium.org (2024-01-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5616628676362240.

### cl...@chromium.org (2024-01-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6092696155783168.

### cl...@chromium.org (2024-01-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2024-01-16)

Detailed Report: https://clusterfuzz.com/testcase?key=6092696155783168

Fuzzing Engine: libFuzzer
Fuzz Target: v8_wasm_compile_fuzzer
Job Type: libfuzzer_chrome_asan
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7a1c00010004
Crash State:
  Builtins_JSToWasmWrapperAsm
  Builtins_JSToWasmWrapper
  Builtins_JSEntryTrampoline
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=1228723:1228733

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6092696155783168

See https://chromium.googlesource.com/chromium/src/+/master/testing/libfuzzer/reproducing.md for instructions on reproducing this bug locally.

The recommended severity (Security_Severity-Medium) is different from what was assigned to the bug. Please double check the accuracy of the assigned severity.

### [Deleted User] (2024-01-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2024-01-16)

Detailed Report: https://clusterfuzz.com/testcase?key=6092696155783168

Fuzzing Engine: libFuzzer
Fuzz Target: v8_wasm_compile_fuzzer
Job Type: libfuzzer_chrome_asan
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7a1c00010004
Crash State:
  Builtins_JSToWasmWrapperAsm
  Builtins_JSToWasmWrapper
  Builtins_JSEntryTrampoline
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=1228723:1228733

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6092696155783168

See https://chromium.googlesource.com/chromium/src/+/master/testing/libfuzzer/reproducing.md for instructions on reproducing this bug locally.

The recommended severity (Security_Severity-Medium) is different from what was assigned to the bug. Please double check the accuracy of the assigned severity.

### [Deleted User] (2024-01-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2024-01-16)

Removing FoundIn-120 as per the bisection. That should also stop the bots fighting for the right impact labels.

Andreas / Matthias, this is currently still disabled, right? So it shouldn't have impact. The finch is only planned for M-122 I guess.

### [Deleted User] (2024-01-16)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-16)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-16)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-17)

[Empty comment from Monorail migration]

### ah...@chromium.org (2024-01-17)

This is an issue in the Turboshaft implementation of WebAssembly, which is still experimental and off-by-default. This is not a stable blocker, and also not a P1 bug.

### ah...@chromium.org (2024-01-17)

[Empty comment from Monorail migration]

### al...@goodmanemail.com (2024-01-17)

Despite this one bisecting to a turboshaft revision I have got a niggling doubt in my head that this might not actually be a turboshaft issue.

If its a bug in turboshaft; in experimental code why does it replicate with --no-experimental --no-turboshaft --no-turboshaft-wasm arguments set?

$ /home/alan/chromium/src/out/libfuzzerasandbg/v8_wasm_compile_fuzzer --no-experimental --no-turboshaft --no-turboshaft-wasm crash-segv
INFO: Running with entropic power schedule (0xFF, 100).
INFO: Seed: 1636247791
INFO: Loaded 10 modules   (1553734 inline 8-bit counters): 23756 [0x7f7634e11ce0, 0x7f7634e179ac), 2519 [0x7f7636ff5120, 0x7f7636ff5af7), 38069 [0x7f763585ebd0, 0x7f7635868085), 54123 [0x7f76365d3ba0, 0x7f76365e0f0b), 20811 [0x7f7636e6ae60, 0x7f7636e6ffab), 108337 [0x7f7638f09000, 0x7f7638f23731), 6464 [0x7f7646594a30, 0x7f7646596370), 2474 [0x7f7646493240, 0x7f7646493bea), 1286579 [0x7f7644ea58a0, 0x7f7644fdfa53), 10602 [0x5566fa3dbef0, 0x5566fa3de85a), 
INFO: Loaded 10 PC tables (1553734 PCs): 23756 [0x7f7634e179b0,0x7f7634e74670), 2519 [0x7f7636ff5af8,0x7f7636fff868), 38069 [0x7f7635868088,0x7f76358fcbd8), 54123 [0x7f76365e0f10,0x7f76366b45c0), 20811 [0x7f7636e6ffb0,0x7f7636ec1460), 108337 [0x7f7638f23738,0x7f76390caa48), 6464 [0x7f7646596370,0x7f76465af770), 2474 [0x7f7646493bf0,0x7f764649d690), 1286579 [0x7f7644fdfa58,0x7f7646381588), 10602 [0x5566fa3de860,0x5566fa407f00), 
/home/alan/chromium/src/out/libfuzzerasandbg/v8_wasm_compile_fuzzer: Running 1 inputs 1 time(s) each.
Running: crash-segv
AddressSanitizer:DEADLYSIGNAL
=================================================================
==2505117==ERROR: AddressSanitizer: SEGV on unknown address 0x7e6e00010004 (pc 0x7f764642322e bp 0x7ffe1623afd8 sp 0x7ffe1623afb0 T0)
==2505117==The signal is caused by a READ memory access.
    #0 0x7f764642322e  (<unknown module>)
    #1 0x7f763cfbc2c9 in Builtins_JSToWasmWrapperAsm setup-isolate-deserialize.cc
    #2 0x7f763d54b6e3 in Builtins_JSToWasmWrapper setup-isolate-deserialize.cc
    #3 0x7f763cc8be5b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #4 0x7f763cc8bb86 in Builtins_JSEntry setup-isolate-deserialize.cc
    #5 0x7f763e3507df in Call v8/src/execution/simulator.h:178:12
    #6 0x7f763e3507df in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:418:22
    #7 0x7f763e34d6ae in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution/execution.cc:504:10
    #8 0x5566fa39e6e7 in v8::internal::wasm::testing::CallWasmFunctionForTesting(v8::internal::Isolate*, v8::internal::Handle<v8::internal::WasmInstanceObject>, char const*, v8::base::Vector<v8::internal::Handle<v8::internal::Object>>, std::__Cr::unique_ptr<char const [], std::__Cr::default_delete<char const []>>*) v8/test/common/wasm/wasm-module-runner.cc:125:32
    #9 0x5566fa336036 in v8::internal::wasm::fuzzer::ExecuteAgainstReference(v8::internal::Isolate*, v8::internal::Handle<v8::internal::WasmModuleObject>, int) v8/test/fuzzer/wasm-fuzzer-common.cc:173:20
    #10 0x5566fa343df5 in v8::internal::wasm::fuzzer::WasmExecutionFuzzer::FuzzWasmModule(v8::base::Vector<unsigned char const>, bool) v8/test/fuzzer/wasm-fuzzer-common.cc:906:5
    #11 0x5566fa10b771 in LLVMFuzzerTestOneInput v8/test/fuzzer/wasm-compile.cc:3525:23
    #12 0x5566fa2766cb in fuzzer::Fuzzer::ExecuteCallback(unsigned char const*, unsigned long) third_party/libFuzzer/src/FuzzerLoop.cpp:614:13
    #13 0x5566fa1f58ab in fuzzer::RunOneTest(fuzzer::Fuzzer*, char const*, unsigned long) third_party/libFuzzer/src/FuzzerDriver.cpp:327:6
    #14 0x5566fa1fda64 in fuzzer::FuzzerDriver(int*, char***, int (*)(unsigned char const*, unsigned long)) third_party/libFuzzer/src/FuzzerDriver.cpp:862:9
    #15 0x5566fa1a884f in main third_party/libFuzzer/src/FuzzerMain.cpp:20:10
    #16 0x7f7634423a8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV (<unknown module>) 
==2505117==ABORTING



### be...@google.com (2024-01-17)

Adding Hotlist-RBS-Removed for tracking purposes.

### ml...@chromium.org (2024-01-17)

I have a WIP fix available at https://chromium-review.googlesource.com/c/v8/v8/+/5204427 with a simplified reproducer.

With this fix also the original reproducer doesn't crash anymore.
Regarding https://crbug.com/chromium/1514072#c28 it seems that passing --no-turboshaft-wasm doesn't prevent the fuzzer from setting this flag.
The v8 wasm compile fuzzer also fuzzes staged wasm flags or flags we intent to ship, which is why turboshaft-wasm is included there.

Note: While --turboshaft-wasm isn't enabled by default, we plan finching it which is why it was added to --future, so it isn't an experimental feature any more (but not enabled anywhere on stable).

I think this is a security bug. While the current reproducer only causes an unprotected load of the array length on the WasmNull object (i.e. a fixed memory address that will always crash due to the design of the WasmNull object), with a carefully crafted different wasm binary it should be possible to cause a type confusion instead not only on the nullability of the value but also on the actual type.

I'll spend some more time trying to simplify the reproducer and finding alternative ways to trigger this bug that could potentially trigger type confusion.

### cl...@chromium.org (2024-01-17)

Re-setting high severity because this is basically causing type confusion. Removing M-121 as we only plan to start finching in M-122. Also leaving Impact-None because this is still disabled currently.

### da...@google.com (2024-01-17)

[Empty comment from Monorail migration]

### ml...@chromium.org (2024-01-17)

OK, so the WIP fix fixes an issue in the wasm-gc-type-reducer.cc. There is still an issue in it though and at least that issue can be used to cause a type confusion.
As the issues are closely related (tracking and merging in the analysis related to unreachable code paths), I'll just treat it as the same issue.

Attached is the reproducer for the type confusion.

1) Run it with:
$ out/x64.debug/d8 --test test/mjsunit/mjsunit.js repro-issue.js --liftoff-only
This succeeds as expected.

2) Run it again with:
$ out/x64.debug/d8 --test test/mjsunit/mjsunit.js repro-issue.js --no-liftoff --turboshaft-wasm --no-wasm-loop-unrolling --no-wasm-loop-peeling --nodebug-code
It doesn't trap and instead prints 305419896 on the console which is 0x12345678 (so one half of the i64).

Note that while it requires to explicitly disable loop unrolling and loop peeling, this is just due to this example being crafted with these optimizations disabled. It should be possible to trigger the issue otherwise but it is much harder to craft a manually craft a reproducer with optimizer passes in front of the faulty WasmGCOptimizePhase.

I don't have a fix available for this yet. I also noticed that the tracking of unreachable blocks besides not being updated on loops revisits (i.e. a block inside a loop that was tracked as unreachable has to reset its status to reachable upon revisit of that loop) we only use the reachability information on the succeeding block when merging type information.
However, a block that is only reachable by blocks marked as unreachable, are not marked unreachable, i.e. unreachability doesn't propagate making this issue harder to reach and making the optimizations weaker than they could be.

My suspicion why our compile fuzzer doesn't find it:
This bug requires running a loop revisit in the WasmGCTypeAnalysis to infer wrong type information.
The type information will only be broken for subsequent iterations of the wasm loop, i.e. running the loop body after following the loop backedge.
Our fuzzer doesn't fuzz executing the generated code of the optimizing compiler for wasm modules that time out.
Therefore, for our fuzzer to find it we need the type confusion in a loop body that is executed more than once but then exits on some subsequent iteration.

### ml...@chromium.org (2024-01-17)

For some reason the attachment wasn't added. Trying it again.

### al...@goodmanemail.com (2024-01-17)

I found this during my ongoing run of your fuzzer.  I started with crafted inputs which were 'distilled down' through abuse of the merge function and then 'polished' by whatever mutations your fuzzer is doing.  Additionally I hand crafted my own dictionary and regularly sifted out slow testcases.  I spent a lot of time mucking about with modifying the code, but then you independently made changes in the fuzzer which basically did what I was trying to achieve so I abandoned that side.  I've been running it on and off for a really long time and have collected a huge amount of correctness issues; many of which have been around since I started my run but I dont know of a sensible way to report them?  This issue really stood out to me though because the fuzzer does not find it very often and when it does it completely explodes the fuzzing process - the fuzzer actually segfaults which is extremely rare.

Out of interest; presumably you generated a d8 testcase with the --wasm-fuzzer-gen-test switch.  I tried this; but could not reproduce in d8.  Presumably this means that I didnt know which magical switches to use?  I tried the usual ones that I was aware of...

### ml...@chromium.org (2024-01-17)

@Alan: Yes, Andreas used --wasm-fuzzer-gen-test to generate a reproducer. Unfortunately, this generator doesn't generate the flags required for it.
I think the actual flags could be recovered by figuring out which flags are set in `EnableExperimentalWasmFeatures` in wasm-fuzzer-common.cc and if there are other places that modify the flags in the fuzzer.

I have tried the original repro with an asan build on more or less tip of tree (b67a2f5d905185b2c095a3f2a2db31c0cd5d0a30).
After generating the test case with --wasm-fuzzer-gen-test I can reproduce a crash with "--turboshaft-wasm --no-liftoff" (so we run the optimizing compiler and skip any tiering).
This crash also disappears with the fix.

Still, the fuzzer ran into an ASAN reported crash:
    AddressSanitizer:DEADLYSIGNAL
    ==============================
    3748800==ERROR: AddressSanitizer: SEGV on unknown address 0x7eb000010004 (pc 0x7fc4bb0cc22e bp 0x7fffcb73b978 sp 0x7fffcb73b950 T0)
while the manual run ran into a regular SIGSEGV:
    Received signal 11 SEGV_ACCERR 7df700010004

Note that only the upper half of the addresses is different, so I'm pretty certain that in both cases it's an unprotected load of the array length on an array object that is null.
I'll try to get a fix for the type confusion in https://crbug.com/chromium/1514072#c33 next and land the first fix that fixed the original reproducer.

### al...@goodmanemail.com (2024-01-17)

Thanks.  I can repro using d8 now by using those flags.  I was pretty close I guess; I ruled out --turboshaft-wasm as I thought it was the default.  --no-liftoff is the common one in my experience.  Hopefully once this bug becomes public somebody might find this information useful.

In regards of the address its trying to access/crashing on; may I draw your attention to https://crbug.com/chromium/1514072#c8; whilst the query regarding the debug check is most certainly unrelated the other information still stands - the instruction pointer appears to get set to garbage values when I reproduce using no sanitizers build.  EG built in the chromium tree using "gn gen out/libfuzzernosan '--args=use_libfuzzer=true is_ubsan=false is_msan=false is_asan=false is_tsan=false is_debug=false'" followed by autoninja -C out/libfuzzernosan v8_wasm_compile_fuzzer

Please see below example; replicated in the fuzzer because it creates more digestible output:

alan@dl360g10fuzz:~/bisect$ while :; do /home/alan/chromium/src/out/libfuzzerasandbg/v8_wasm_compile_fuzzer crash-segv 2>&1 | grep unknown\ address; done
==2547440==ERROR: AddressSanitizer: SEGV on unknown address 0x7e7200010004 (pc 0x7f7a6bdd122e bp 0x7ffd257595d8 sp 0x7ffd257595b0 T0)
==2547460==ERROR: AddressSanitizer: SEGV on unknown address 0x7e4e00010004 (pc 0x7f56d0a0922e bp 0x7fff25beeef8 sp 0x7fff25beeed0 T0)
==2547480==ERROR: AddressSanitizer: SEGV on unknown address 0x7eaa00010004 (pc 0x7e9c6dd40a2e bp 0x7ffc91179a38 sp 0x7ffc91179a10 T0)
==2547500==ERROR: AddressSanitizer: SEGV on unknown address 0x7eb900010004 (pc 0x7ea6d5510a2e bp 0x7ffc198b70f8 sp 0x7ffc198b70d0 T0)
==2547520==ERROR: AddressSanitizer: SEGV on unknown address 0x7e0800010004 (pc 0x7f10689f922e bp 0x7ffe4697dbf8 sp 0x7ffe4697dbd0 T0)
==2547540==ERROR: AddressSanitizer: SEGV on unknown address 0x7df900010004 (pc 0x7f01e523322e bp 0x7ffd7c3c91d8 sp 0x7ffd7c3c91b0 T0)
==2547560==ERROR: AddressSanitizer: SEGV on unknown address 0x7eda00010004 (pc 0x7ea5e5ec0a2e bp 0x7ffe281d4b38 sp 0x7ffe281d4b10 T0)
==2547580==ERROR: AddressSanitizer: SEGV on unknown address 0x7e6e00010004 (pc 0x7f767478722e bp 0x7ffeecffb938 sp 0x7ffeecffb910 T0)
==2547600==ERROR: AddressSanitizer: SEGV on unknown address 0x7dff00010004 (pc 0x7f0791c1622e bp 0x7ffcec06ad98 sp 0x7ffcec06ad70 T0)
==2547620==ERROR: AddressSanitizer: SEGV on unknown address 0x7e5900010004 (pc 0x7f621f1c822e bp 0x7ffdb5be9958 sp 0x7ffdb5be9930 T0)
==2547640==ERROR: AddressSanitizer: SEGV on unknown address 0x7e8400010004 (pc 0x7f8d1180922e bp 0x7ffd27e32ab8 sp 0x7ffd27e32a90 T0)
==2547660==ERROR: AddressSanitizer: SEGV on unknown address 0x7e8f00010004 (pc 0x7ffa0140b22e bp 0x7ffcba58f898 sp 0x7ffcba58f870 T0)
==2547680==ERROR: AddressSanitizer: SEGV on unknown address 0x7e7b00010004 (pc 0x7f83a821322e bp 0x7ffece9faf58 sp 0x7ffece9faf30 T0)
==2547700==ERROR: AddressSanitizer: SEGV on unknown address 0x7e9200010004 (pc 0x7e8127b40a2e bp 0x7ffddcde04f8 sp 0x7ffddcde04d0 T0)
^C
alan@dl360g10fuzz:~/bisect$ while :; do /home/alan/chromium/src/out/libfuzzernosan/v8_wasm_compile_fuzzer crash-segv 2>&1 | grep unknown\ address; done
==2547720==ERROR: UndefinedBehaviorSanitizer: SEGV on unknown address 0x23cb00010004 (pc 0x03de7fe758f9 bp 0x7ffed37bbea0 sp 0x7ffed37bbe78 T2547720)
==2547739==ERROR: UndefinedBehaviorSanitizer: SEGV on unknown address 0x099700010004 (pc 0x1feaccb4b8f9 bp 0x7fff139a2900 sp 0x7fff139a28d8 T2547739)
==2547758==ERROR: UndefinedBehaviorSanitizer: SEGV on unknown address 0x174900010004 (pc 0x31b3f89ef8f9 bp 0x7ffc0b516120 sp 0x7ffc0b5160f8 T2547758)
==2547777==ERROR: UndefinedBehaviorSanitizer: SEGV on unknown address 0x147b00010004 (pc 0x1f1df6c578f9 bp 0x7ffe10bc6870 sp 0x7ffe10bc6848 T2547777)
==2547796==ERROR: UndefinedBehaviorSanitizer: SEGV on unknown address 0x054d00010004 (pc 0x180d447518f9 bp 0x7ffed8101d80 sp 0x7ffed8101d58 T2547796)
==2547815==ERROR: UndefinedBehaviorSanitizer: SEGV on unknown address 0x1bce00010004 (pc 0x0a90d08b68f9 bp 0x7ffc95b9fb40 sp 0x7ffc95b9fb18 T2547815)
==2547834==ERROR: UndefinedBehaviorSanitizer: SEGV on unknown address 0x02af00010004 (pc 0x3bf048ed38f9 bp 0x7fffff5c0170 sp 0x7fffff5c0148 T2547834)
==2547853==ERROR: UndefinedBehaviorSanitizer: SEGV on unknown address 0x1c6c00010004 (pc 0x03a5f5c348f9 bp 0x7ffc8493fdb0 sp 0x7ffc8493fd88 T2547853)
==2547872==ERROR: UndefinedBehaviorSanitizer: SEGV on unknown address 0x394900010004 (pc 0x13c821c848f9 bp 0x7ffccb165e00 sp 0x7ffccb165dd8 T2547872)
==2547891==ERROR: UndefinedBehaviorSanitizer: SEGV on unknown address 0x184700010004 (pc 0x17c7084a98f9 bp 0x7ffe145d5220 sp 0x7ffe145d51f8 T2547891)
==2547910==ERROR: UndefinedBehaviorSanitizer: SEGV on unknown address 0x2bee00010004 (pc 0x1de6fa7838f9 bp 0x7fffc47e18c0 sp 0x7fffc47e1898 T2547910)
==2547929==ERROR: UndefinedBehaviorSanitizer: SEGV on unknown address 0x204100010004 (pc 0x3d55822b98f9 bp 0x7fffa28de520 sp 0x7fffa28de4f8 T2547929)
==2547948==ERROR: UndefinedBehaviorSanitizer: SEGV on unknown address 0x1ae500010004 (pc 0x1e8feced68f9 bp 0x7ffc2edd64f0 sp 0x7ffc2edd64c8 T2547948)
==2547967==ERROR: UndefinedBehaviorSanitizer: SEGV on unknown address 0x04d500010004 (pc 0x3a056e2ab8f9 bp 0x7fff16a61f40 sp 0x7fff16a61f18 T2547967)
==2547986==ERROR: UndefinedBehaviorSanitizer: SEGV on unknown address 0x183400010004 (pc 0x0da12130f8f9 bp 0x7ffeaea81fe0 sp 0x7ffeaea81fb8 T2547986)
==2548005==ERROR: UndefinedBehaviorSanitizer: SEGV on unknown address 0x31f900010004 (pc 0x1cfb93d508f9 bp 0x7ffd652461d0 sp 0x7ffd652461a8 T2548005)
==2548024==ERROR: UndefinedBehaviorSanitizer: SEGV on unknown address 0x34d800010004 (pc 0x0ca26fb328f9 bp 0x7ffcf49b9af0 sp 0x7ffcf49b9ac8 T2548024)
==2548043==ERROR: UndefinedBehaviorSanitizer: SEGV on unknown address 0x372800010004 (pc 0x1f140b5768f9 bp 0x7ffc7a2b0b30 sp 0x7ffc7a2b0b08 T2548043)
==2548062==ERROR: UndefinedBehaviorSanitizer: SEGV on unknown address 0x0e3a00010004 (pc 0x20a0437888f9 bp 0x7ffeeeec3ea0 sp 0x7ffeeeec3e78 T2548062)
==2548081==ERROR: UndefinedBehaviorSanitizer: SEGV on unknown address 0x158d00010004 (pc 0x18bb3df488f9 bp 0x7fff22a87280 sp 0x7fff22a87258 T2548081)
==2548100==ERROR: UndefinedBehaviorSanitizer: SEGV on unknown address 0x01d900010004 (pc 0x06497b38f8f9 bp 0x7ffea5632e30 sp 0x7ffea5632e08 T2548100)

I confirmed the same behaviour in d8 as well.

### ml...@chromium.org (2024-01-17)

So, I just checked again:
In static-roots.h we have the definition:
> kWasmNull = 0xfffd;
This is the offset from the heap start to the wasm null object.
We also have:
> WasmArray::kLengthOffset
which is 8 (this comes from some torque generated C++ files that contain some computation.
So: 10004 == kWasmNull - 1 + WasmArray::kLengthOffset

So while I can't confirm that in all cases we try to load the length of the wasm null object, it is still pretty certain that we load with an 8 Byte offset from the wasm null object.
This always crashes with a segmentation fault by design:
The wasm null is used together with our trap handler. So whenever we perform an operation on a wasm object that could be nullable with a limited offset, we actually don't perform a null check but instead just perform the load. If it is the wasm null object, the OS will signal and our "TrapHandler" will then check if the current pc points to a "protected" load or store.
If it points to a protected instruction, we convert the signal into a JS exception (a wasm trap).
If it doesn't point to a protected instruction (e.g. because the optimizer wrongly decided that a wasm value is guaranteed not to be null like in this case), then the V8 signal handler doesn't discard it and the regular signal handling happens leading to the crash.
So all these cases above are not unlikely to have the same root cause.
Potentially they might all disappear by https://chromium-review.googlesource.com/c/v8/v8/+/5204427 or they might be running into the same issue as the reproducer in https://crbug.com/chromium/1514072#c34.

I'll let you know once I have a WIP fix and hopefully all these ...10004 fuzzing crashes should disappear.

### gi...@appspot.gserviceaccount.com (2024-01-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/f57dbf09df2340d4a072c9f6bf2486811e5b2385

commit f57dbf09df2340d4a072c9f6bf2486811e5b2385
Author: Matthias Liedtke <mliedtke@chromium.org>
Date: Wed Jan 17 13:13:46 2024

[turboshaft][wasm-gc] WasmGCTypeAnalyzer: Ignore bottom types in Phi merging

The bottom type is used to indicate an uninhabitable value in the
analysis. This means, it can only be used in unreachable code.
The one exceptions are phis.

If any input value of a phi is uninhabitable, it only means that it
will never receive its value from that predecessor, therefore the
bottom type must be ignored.
Otherwise (prior to this change) the union type merges the input types
to bottom as well indicating that the phi value itself is
uninhabitable (which it isn't).

Bug: chromium:1514072
Change-Id: I2cbdb2be05db912bc422e3d44ca44efcb6f0e513
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5204427
Reviewed-by: Manos Koukoutos <manoskouk@chromium.org>
Commit-Queue: Manos Koukoutos <manoskouk@chromium.org>
Auto-Submit: Matthias Liedtke <mliedtke@chromium.org>
Cr-Commit-Position: refs/heads/main@{#91899}

[add] https://crrev.com/f57dbf09df2340d4a072c9f6bf2486811e5b2385/test/mjsunit/regress/wasm/regress-1514072.js
[modify] https://crrev.com/f57dbf09df2340d4a072c9f6bf2486811e5b2385/src/compiler/turboshaft/wasm-gc-type-reducer.cc


### al...@goodmanemail.com (2024-01-18)

Last night (about 10 ish hours ago) I put together a version of the fuzzer based on v8 ToT + the aforementioned fix.  I've ran it overnight on my 116 cores without replicating any of the segfaults.  Additionally I ran my collection of 'previous crashes' through without replicating the SEGV crashes.

The type confusion PoC in described in https://crbug.com/chromium/1514072#c33 and attached to https://crbug.com/chromium/1514072#c34 still replicates with this setup.

### [Deleted User] (2024-01-20)

[Empty comment from Monorail migration]

### ml...@chromium.org (2024-01-23)

Note: I'm out of office until the end of the week.
I have a local fix that resets the state of unreachable blocks back to the state prior to visiting a given loop on its revisit.
This seems to work fine but also seems unnecessarily complex.

It would be the more proper and better fix to check the reachability status of the block at its beginning (based on its predecessors' reachability) and insert or drop it from the unreachable list. That would also ensure that unreachability propagates properly.
I'll look into it again next week.

### ad...@google.com (2024-01-25)

(I am a bot: this is an auto-cc on a security bug)

### am...@chromium.org (2024-01-25)

[Empty comment from Monorail migration]

### ad...@google.com (2024-01-26)

(I am a bot: this is an auto-cc on a security bug)

### gi...@appspot.gserviceaccount.com (2024-01-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/25aeff681f470969af13be2cdbbf1318c7777864

commit 25aeff681f470969af13be2cdbbf1318c7777864
Author: Matthias Liedtke <mliedtke@chromium.org>
Date: Mon Jan 29 11:26:17 2024

[wasm][turboshaft] Fix reachability tracking in WasmGCTypeReducer

During loop revisits, previously unreachable blocks can become
reachable again.

Fixed: chromium:1514072
Change-Id: Icb8b5f99e7257b5c503453d9334a6bf79857fabe
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5244649
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
Auto-Submit: Matthias Liedtke <mliedtke@chromium.org>
Cr-Commit-Position: refs/heads/main@{#92058}

[modify] https://crrev.com/25aeff681f470969af13be2cdbbf1318c7777864/src/compiler/turboshaft/wasm-gc-type-reducer.cc
[add] https://crrev.com/25aeff681f470969af13be2cdbbf1318c7777864/test/mjsunit/regress/wasm/regress-1514072-2.js


### [Deleted User] (2024-01-29)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-29)

[Empty comment from Monorail migration]

### am...@google.com (2024-02-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### al...@goodmanemail.com (2024-02-02)

Wow thank you do much!  Out of interest; did I do something wrong in my bisect that caused me to miss that part of the bounty?

### am...@chromium.org (2024-02-02)

Congratulations Alan! As you already know, the Chrome VRP Panel has decided to award you $7,000 for this report! The reward amount was less of an issue about the bisect and more of an issue with the report being slightly below baseline and resulting in a lot of work by the V8 team to come up with proper test case to determine the root cause of this issue. Since this is your first Chrome VRP reward, a member of our Google p2p-vrp team will be reaching to you soon to arrange payment. We greatly appreciate all the efforts we have seen from you thus far to use your fuzzing capabilities to find potential security bugs in Chrome and how you've refined your work along the way! 

### am...@google.com (2024-02-02)

[Empty comment from Monorail migration]

### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/1514072?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-05-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41486636)*
