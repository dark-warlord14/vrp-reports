# v8_wasm_fuzzer Debug check failed: begin.valid() in v8/src/compiler/turboshaft/graph.h, line 946

| Field | Value |
|-------|-------|
| **Issue ID** | [336007400](https://issues.chromium.org/issues/336007400) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler, Blink>JavaScript>WebAssembly |
| **Platforms** | Linux |
| **Reporter** | al...@goodmanemail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2024-04-21 |
| **Bounty** | $2,000.00 |

## Description

VULNERABILITY DETAILS
# Fatal error in ../../v8/src/compiler/turboshaft/graph.h, line 946
# Debug check failed: begin.valid().

VERSION
Chrome Version: be0b3aaa7aa7e8271feecde55d39e86891d91e6f + V8 5536989289b4f6e923fb2f4e40f829480136573c
Operating System: Ubuntu 22.04

REPRODUCTION CASE
(Attached)

Testcase is unminimized beecause the fuzzer is apparently ignoring the options that are set unless ran in 'one shot' mode - eg with a filename as the last param?

$ /home/alan/chromium/src/out/libfuzzerasandbg/v8_wasm_fuzzer --single-threaded --no-liftoff --turboshaft-wasm in_min/250e0de4e709fdbc7d08e0b679b5b0ce9db9d81d
INFO: Running with entropic power schedule (0xFF, 100).
INFO: Seed: 362513560
INFO: Loaded 10 modules   (1623498 inline 8-bit counters): 23606 [0x7fbd41ec2f20, 0x7fbd41ec8b56), 2521 [0x7fbd4163a410, 0x7fbd4163ade9), 38357 [0x7fbd427554f0, 0x7fbd4275eac5), 54255 [0x7fbd43373000, 0x7fbd433803ef), 24827 [0x7fbd43a9d790, 0x7fbd43aa388b), 85903 [0x7fbd45018dd0, 0x7fbd4502dd5f), 5963 [0x7fbd452c99f0, 0x7fbd452cb13b), 2551 [0x7fbd451edbc0, 0x7fbd451ee5b7), 1379409 [0x7fbd509ef8f0, 0x7fbd50b40541), 6106 [0x564f52ec8b50, 0x564f52eca32a), 
INFO: Loaded 10 PC tables (1623498 PCs): 23606 [0x7fbd41ec8b58,0x7fbd41f24eb8), 2521 [0x7fbd4163adf0,0x7fbd41644b80), 38357 [0x7fbd4275eac8,0x7fbd427f4818), 54255 [0x7fbd433803f0,0x7fbd434542e0), 24827 [0x7fbd43aa3890,0x7fbd43b04840), 85903 [0x7fbd4502dd60,0x7fbd4517d650), 5963 [0x7fbd452cb140,0x7fbd452e25f0), 2551 [0x7fbd451ee5b8,0x7fbd451f8528), 1379409 [0x7fbd50b40548,0x7fbd5204ca58), 6106 [0x564f52eca330,0x564f52ee20d0), 
/home/alan/chromium/src/out/libfuzzerasandbg/v8_wasm_fuzzer: Running 1 inputs 1 time(s) each.
Running: in_min/250e0de4e709fdbc7d08e0b679b5b0ce9db9d81d


#
# Fatal error in ../../v8/src/compiler/turboshaft/graph.h, line 946
# Debug check failed: begin.valid().
#
#
#
#FailureMessage Object: 0x7fbd2b21c460
==== C stack trace ===============================

    /home/alan/chromium/src/out/libfuzzerasandbg/v8_wasm_fuzzer(__interceptor_backtrace+0x46) [0x564f52c93896]
    /home/alan/chromium/src/out/libfuzzerasandbg/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x2d) [0x7fbd452aeaad]
    /home/alan/chromium/src/out/libfuzzerasandbg/libv8_libplatform.so(+0x40671) [0x7fbd451d6671]
    /home/alan/chromium/src/out/libfuzzerasandbg/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x2d7) [0x7fbd4526d497]
    /home/alan/chromium/src/out/libfuzzerasandbg/libv8_libbase.so(+0x7397f) [0x7fbd4526c97f]
    /home/alan/chromium/src/out/libfuzzerasandbg/libv8.so(+0x9816b23) [0x7fbd4eafab23]
    /home/alan/chromium/src/out/libfuzzerasandbg/libv8.so(+0x9814a90) [0x7fbd4eaf8a90]
    /home/alan/chromium/src/out/libfuzzerasandbg/libv8.so(+0x98140b2) [0x7fbd4eaf80b2]
    /home/alan/chromium/src/out/libfuzzerasandbg/libv8.so(+0x973ef5c) [0x7fbd4ea22f5c]
    /home/alan/chromium/src/out/libfuzzerasandbg/libv8.so(+0x973e555) [0x7fbd4ea22555]
    /home/alan/chromium/src/out/libfuzzerasandbg/libv8.so(+0x973dfe8) [0x7fbd4ea21fe8]
    /home/alan/chromium/src/out/libfuzzerasandbg/libv8.so(+0x930a552) [0x7fbd4e5ee552]
    /home/alan/chromium/src/out/libfuzzerasandbg/libv8.so(+0x93078f4) [0x7fbd4e5eb8f4]
    /home/alan/chromium/src/out/libfuzzerasandbg/libv8.so(+0x994fc3c) [0x7fbd4ec33c3c]
    /home/alan/chromium/src/out/libfuzzerasandbg/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x1051) [0x7fbd4d2a5441]
    /home/alan/chromium/src/out/libfuzzerasandbg/libv8.so(v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::Counters*, v8::internal::wasm::WasmFeatures*)+0x38e) [0x7fbd4d2a37ee]
    /home/alan/chromium/src/out/libfuzzerasandbg/libv8.so(+0x80a0ca1) [0x7fbd4d384ca1]
    /home/alan/chromium/src/out/libfuzzerasandbg/libv8.so(+0x809fd5d) [0x7fbd4d383d5d]
    /home/alan/chromium/src/out/libfuzzerasandbg/libv8_libplatform.so(+0x3d4f9) [0x7fbd451d34f9]
    /home/alan/chromium/src/out/libfuzzerasandbg/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0x208) [0x7fbd451db418]
    /home/alan/chromium/src/out/libfuzzerasandbg/libv8_libbase.so(+0xb2d68) [0x7fbd452abd68]
    /home/alan/chromium/src/out/libfuzzerasandbg/v8_wasm_fuzzer(+0x1ceff7) [0x564f52ce7ff7]
    /lib/x86_64-linux-gnu/libc.so.6(+0x94ac3) [0x7fbd416d9ac3]
    /lib/x86_64-linux-gnu/libc.so.6(+0x126850) [0x7fbd4176b850]
==3670289== ERROR: libFuzzer: deadly signal
    #0 0x564f52cf5a41 in __sanitizer_print_stack_trace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_stack.cpp:87:3
    #1 0x564f52e37601 in fuzzer::PrintStackTrace() third_party/libFuzzer/src/FuzzerUtil.cpp:210:5
    #2 0x564f52dbcf51 in fuzzer::Fuzzer::CrashCallback() third_party/libFuzzer/src/FuzzerLoop.cpp:231:3
    #3 0x564f52dbce56 in fuzzer::Fuzzer::StaticCrashSignalCallback() third_party/libFuzzer/src/FuzzerLoop.cpp:202:6
    #4 0x564f52e39ae7 in fuzzer::CrashHandler(int, siginfo_t*, void*) third_party/libFuzzer/src/FuzzerUtilPosix.cpp:46:3
    #5 0x7fbd4168751f  (/lib/x86_64-linux-gnu/libc.so.6+0x4251f) (BuildId: 962015aa9d133c6cbcfb31ec300596d7f44d3348)

NOTE: libFuzzer has rudimentary signal handlers.
      Combine libFuzzer with AddressSanitizer or similar for better crash reports.
SUMMARY: libFuzzer: deadly signal

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: Dcheck
Crash State: 
#0  __pthread_kill_implementation (no_tid=0, signo=6, threadid=140736728229440) at ./nptl/pthread_kill.c:44
#1  __pthread_kill_internal (signo=6, threadid=140736728229440) at ./nptl/pthread_kill.c:78
#2  __GI___pthread_kill (threadid=140736728229440, signo=signo@entry=6) at ./nptl/pthread_kill.c:89
#3  0x00007fffe7563476 in __GI_raise (sig=sig@entry=6) at ../sysdeps/posix/raise.c:26
#4  0x00007fffe75497f3 in __GI_abort () at ./stdlib/abort.c:79
#5  0x00007fffeb184b66 in v8::base::OS::Abort () at ../../v8/src/base/platform/platform-posix.cc:704
#6  0x00007fffeb1494bb in V8_Fatal (file=<optimized out>, line=<optimized out>, format=<optimized out>) at ../../v8/src/base/logging.cc:205
#7  0x00007fffeb14897f in v8::base::(anonymous namespace)::DefaultDcheckHandler (file=0x7fffee912ac0 <str> "../../v8/src/compiler/turboshaft/graph.h", line=946, 
    message=0x7fffee915ac0 <str> "begin.valid()") at ../../v8/src/base/logging.cc:57
#8  0x00007ffff49d6b23 in v8::internal::compiler::turboshaft::Graph::OperationIndices (this=0x525000061d90, begin=..., end=...) at ../../v8/src/compiler/turboshaft/graph.h:946
#9  v8::internal::compiler::turboshaft::Graph::OperationIndices (this=0x525000061d90, block=...) at ../../v8/src/compiler/turboshaft/graph.h:926
#10 v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::WasmLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase> >, false, v8::internal::compiler::turboshaft::WasmLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase> >::VisitBlockBody<(v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::WasmLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase> >, false, v8::internal::compiler::turboshaft::WasmLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase> >::CanHavePhis)0, (v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::WasmLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase> >, false, v8::internal::compiler::turboshaft::WasmLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase> >::ForCloning)0, false> (this=<optimized out>, input_block=<optimized out>, added_block_phi_input=<optimized out>)
    at ../../v8/src/compiler/turboshaft/copying-phase.h:471
#11 0x00007ffff49d4a90 in v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::WasmLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase> >, false, v8::internal::compiler::turboshaft::WasmLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase> >::InlineWaitingBlock<false> (
    this=0x7fffd1213838) at ../../v8/src/compiler/turboshaft/copying-phase.h:611
#12 v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::WasmLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase> >, false, v8::internal::compiler::turboshaft::WasmLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase> >::ProcessWaitingCloningAndInlining<false> (
    this=this@entry=0x7fffd1213838) at ../../v8/src/compiler/turboshaft/copying-phase.h:592
#13 0x00007ffff49d40b2 in v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::WasmLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase> >, false, v8::internal::compiler::turboshaft::WasmLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase> >::VisitAllBlocks<false> (
    this=<optimized out>) at ../../v8/src/compiler/turboshaft/copying-phase.h:357
#14 0x00007ffff48fef5c in v8::internal::compiler::turboshaft::GraphVisitor<v8::internal::compiler::turboshaft::ReducerStack<v8::internal::compiler::turboshaft::Assembler<v8::internal::compiler::turboshaft::reducer_list<v8::internal::compiler::turboshaft::TurboshaftAssemblerOpInterface, v8::internal::compiler::turboshaft::GraphVisitor, v8::internal::compiler::turboshaft::WasmLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase> >, false, v8::internal::compiler::turboshaft::WasmLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer, v8::internal::compiler::turboshaft::TSReducerBase> >::VisitGraph<false> (
    this=this@entry=0x7fffd1213838) at ../../v8/src/compiler/turboshaft/copying-phase.h:121
#15 0x00007ffff48fe555 in v8::internal::compiler::turboshaft::CopyingPhaseImpl<v8::internal::compiler::turboshaft::WasmLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer>::Run (input_graph=..., phase_zone=<optimized out>, trace_reductions=<optimized out>) at ../../v8/src/compiler/turboshaft/copying-phase.h:1016
#16 0x00007ffff48fdfe8 in v8::internal::compiler::turboshaft::CopyingPhase<v8::internal::compiler::turboshaft::WasmLoweringReducer, v8::internal::compiler::turboshaft::MachineOptimizationReducer>::Run (phase_zone=0x5060000094a0) at ../../v8/src/compiler/turboshaft/copying-phase.h:1030
#17 v8::internal::compiler::turboshaft::WasmLoweringPhase::Run (this=<optimized out>, temp_zone=<optimized out>) at ../../v8/src/compiler/turboshaft/wasm-lowering-phase.cc:23
#18 0x00007ffff44ca552 in v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::turboshaft::WasmLoweringPhase> (this=<optimized out>)
    at ../../v8/src/compiler/pipeline.cc:787
#19 0x00007ffff44c78f4 in v8::internal::compiler::Pipeline::GenerateWasmCodeFromTurboshaftGraph (info=<optimized out>, env=<optimized out>, compilation_data=..., 
--Type <RET> for more, q to quit, c to continue without paging--c
    mcgraph=<optimized out>, detected=<optimized out>, call_descriptor=0x52500005f598) at ../../v8/src/compiler/pipeline.cc:3437
#20 0x00007ffff4b0fc3c in v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation (env=<optimized out>, data=..., detected=<optimized out>) at ../../v8/src/compiler/turboshaft/wasm-turboshaft-compiler.cc:51
#21 0x00007ffff3181441 in v8::internal::wasm::WasmCompilationUnit::ExecuteFunctionCompilation (this=<optimized out>, env=<optimized out>, wire_bytes_storage=<optimized out>, counters=<optimized out>, detected=<optimized out>) at ../../v8/src/wasm/function-compiler.cc:163
#22 0x00007ffff317f7ee in v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation (this=<optimized out>, env=<optimized out>, wire_bytes_storage=<optimized out>, counters=<optimized out>, detected=<optimized out>) at ../../v8/src/wasm/function-compiler.cc:32
#23 0x00007ffff3260ca1 in v8::internal::wasm::(anonymous namespace)::ExecuteCompilationUnits (native_module=..., counters=<optimized out>, delegate=<optimized out>, tier=<optimized out>) at ../../v8/src/wasm/module-compiler.cc:1835
#24 0x00007ffff325fd5d in v8::internal::wasm::(anonymous namespace)::BackgroundCompileJob::Run (this=<optimized out>, delegate=<optimized out>) at ../../v8/src/wasm/module-compiler.cc:2288
#25 0x00007fffeb0af4f9 in v8::platform::DefaultJobWorker::Run (this=<optimized out>) at ../../v8/src/libplatform/default-job.h:147
#26 0x00007fffeb0b7418 in v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run (this=<optimized out>) at ../../v8/src/libplatform/default-worker-threads-task-runner.cc:95
#27 0x00007fffeb187d68 in v8::base::Thread::NotifyStartedAndRun (this=0x50b000000bf0) at ../../v8/src/base/platform/platform.h:611
#28 v8::base::ThreadEntry (arg=0x50b000000bf0) at ../../v8/src/base/platform/platform-posix.cc:1189
#29 0x0000555555722ff7 in asan_thread_start () at /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:239
#30 0x00007fffe75b5ac3 in start_thread (arg=<optimized out>) at ./nptl/pthread_create.c:442
#31 0x00007fffe7647850 in clone3 () at ../sysdeps/unix/sysv/linux/x86_64/clone3.S:81

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: Alan Goodman

## Attachments

- [crash-dcheck-begin](attachments/crash-dcheck-begin) (application/octet-stream, 100 B)

## Timeline

### sk...@google.com (2024-04-22)

Setting FoundIn/Severity/Component and assigning to v8 shepherd

### al...@goodmanemail.com (2024-04-22)

I think this is fixed in https://chromium-review.googlesource.com/c/v8/v8/+/5468105

### pe...@google.com (2024-04-22)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-04-22)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### cl...@appspot.gserviceaccount.com (2024-04-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4867610614104064.

### am...@chromium.org (2024-05-02)

code / fix only relevant to a finch trial on beta; updating Security Impact to reflect this

### am...@chromium.org (2024-05-02)

Hi Alan, thank you for this report! While this was a duplicate of a previous report with a patch already landed at the time of this report, the data in your reports for this issue enabled the V8 engineering team to consider this a security issue rather than a functional bug. And while the patch was already landed before your reports, we did want to extend a thank you / bisect reward as this information did enable us to consider this a security issue and backport this fix.
Our new automation was supposed to update this with that information, however, there appears to be a bug and only the vrp-reward field was updated a bit ago, so I wanted to follow up to communicate this.

Thanks again for your reports on this!

### pe...@google.com (2024-05-03)

This is sufficiently serious that it should be merged to stable. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M124. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to beta. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M125. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.


Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [124, 125].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### pg...@google.com (2024-05-03)

Removing Review-125 since it was already backmerged <https://chromium-review.googlesource.com/c/v8/v8/+/5492421> and updating FoundIn to 125 per comment 7!

### pe...@google.com (2024-07-31)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/336007400)*
