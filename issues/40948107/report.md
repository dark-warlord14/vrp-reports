# Security: Debug check failed: HasFeedbackMetadata(kAcquireLoad)

| Field | Value |
|-------|-------|
| **Issue ID** | [40948107](https://issues.chromium.org/issues/40948107) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Maglev, Blink>JavaScript>Compiler>Turbofan |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | wh...@gmail.com |
| **Assignee** | di...@chromium.org |
| **Created** | 2023-12-02 |
| **Bounty** | $1,000.00 |

## Description

/home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7fb9af097c73]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8_libplatform.so(+0x19add) [0x7fb9af03eadd]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x154) [0x7fb9af077d14]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8_libbase.so(+0x2b7d5) [0x7fb9af0777d5]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::FeedbackVector::metadata(v8::internal::PtrComprCageBase, v8::AcquireLoadTag) const+0x173) [0x7fb9b1d8f4d3]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::FeedbackNexus::FeedbackNexus(v8::internal::Handle<v8::internal::FeedbackVector>, v8::internal::FeedbackSlot, v8::internal::NexusConfig const&)+0xae) [0x7fb9b1d8763e]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::compiler::JSHeapBroker::ReadFeedbackForPropertyAccess(v8::internal::compiler::FeedbackSource const&, v8::internal::compiler::AccessMode, v8::internal::compiler::OptionalRef<v8::internal::compiler::NameRef>)+0x86) [0x7fb9b31fcad6]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::compiler::JSHeapBroker::GetFeedbackForPropertyAccess(v8::internal::compiler::FeedbackSource const&, v8::internal::compiler::AccessMode, v8::internal::compiler::OptionalRef<v8::internal::compiler::NameRef>)+0x5d) [0x7fb9b31ff8ed]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevGraphBuilder::VisitGetNamedProperty()+0xb7) [0x7fb9b261bbc7]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevGraphBuilder::VisitSingleBytecode()+0xd6e) [0x7fb9b254180e]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevGraphBuilder::BuildBody()+0x13b) [0x7fb9b253dbcb]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevGraphBuilder::BuildInlined(v8::internal::maglev::ValueNode*, v8::internal::maglev::ValueNode*, v8::internal::maglev::ValueNode*, v8::internal::maglev::CallArguments const&)+0x430) [0x7fb9b2623c90]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevGraphBuilder::TryBuildInlinedCall(v8::internal::maglev::ValueNode*, v8::internal::maglev::ValueNode*, v8::internal::maglev::ValueNode*, v8::internal::compiler::SharedFunctionInfoRef, v8::internal::compiler::OptionalRef<v8::internal::compiler::FeedbackVectorRef>, v8::internal::maglev::CallArguments&, v8::internal::compiler::FeedbackSource const&)+0x42a) [0x7fb9b262580a]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevGraphBuilder::TryBuildCallKnownJSFunction(v8::internal::maglev::ValueNode*, v8::internal::maglev::ValueNode*, v8::internal::maglev::ValueNode*, v8::internal::compiler::SharedFunctionInfoRef, v8::internal::compiler::OptionalRef<v8::internal::compiler::FeedbackVectorRef>, v8::internal::maglev::CallArguments&, v8::internal::compiler::FeedbackSource const&)+0x46) [0x7fb9b2631da6]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevGraphBuilder::TryBuildCallKnownJSFunction(v8::internal::compiler::JSFunctionRef, v8::internal::maglev::ValueNode*, v8::internal::maglev::CallArguments&, v8::internal::compiler::FeedbackSource const&)+0x11b) [0x7fb9b2631c8b]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevGraphBuilder::ReduceCallForConstant(v8::internal::compiler::JSFunctionRef, v8::internal::maglev::CallArguments&, v8::internal::compiler::FeedbackSource const&, v8::internal::SpeculationMode)+0x1fa) [0x7fb9b261407a]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevGraphBuilder::ReduceCall(v8::internal::maglev::ValueNode*, v8::internal::maglev::CallArguments&, v8::internal::compiler::FeedbackSource const&, v8::internal::SpeculationMode)+0x127) [0x7fb9b2627637]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevGraphBuilder::BuildCallWithFeedback(v8::internal::maglev::ValueNode*, v8::internal::maglev::CallArguments&, v8::internal::compiler::FeedbackSource const&)+0x10d) [0x7fb9b263253d]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevGraphBuilder::BuildCallFromRegisters(int, v8::internal::ConvertReceiverMode)+0x17c) [0x7fb9b2632d0c]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevGraphBuilder::VisitSingleBytecode()+0x6fb) [0x7fb9b254119b]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevGraphBuilder::BuildBody()+0x13b) [0x7fb9b253dbcb]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevGraphBuilder::Build()+0x284) [0x7fb9b253b0b4]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevCompiler::Compile(v8::internal::LocalIsolate*, v8::internal::maglev::MaglevCompilationInfo*)+0x657) [0x7fb9b2539db7]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x6a) [0x7fb9b25fff5a]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x96) [0x7fb9b14603d6]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevConcurrentDispatcher::JobTask::Run(v8::JobDelegate*)+0x32c) [0x7fb9b2601d1c]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8_libpatform.so(v8::platform::DefaultJobWorker::Run()+0xd3) [0x7fb9af03d823]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8_libpatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+xc3) [0x7fb9af040213]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8_libbse.so(+0x4a629) [0x7fb9af096629]

my fuzz d8 gn: 
is_debug=false 
dcheck_always_on=true 
v8_static_library=true v8_enable_slow_
dchecks=true 
v8_enable_verify_heap=true 
v8_enable_verify_csa=true
v8_fuzzilli=true 
sanitizer_coverage_flags="trace-pc-guard" 
target_cpu="x64"

I also can reproduce with linux-debug_d8-linux-debug-v8-component-91311.zip
and gn is 
is_component_build = true
is_debug = true
target_cpu = "x64"
use_remoteexec = true
v8_enable_backtrace = true
v8_enable_google_benchmark = true
v8_enable_slow_dchecks = true

You can run following command in many terminal: 
```fire.bash 
#!/usr/bin/env bash 
#
#
for i in {1..999}
do 
        echo ======== $i ============
        $@ 
        RET=$?
        if [ $RET -ne 0 ] && [ $RET -ne 134 ]; then 
                                        echo $RET
          break 
        fi 
done
```

fire.bash ~/asan/d8_debug_zip/d8-linux-debug-v8-component-91325/d8 --expose-gc --omit-quit --allow-natives-syntax --fuzzing --jit-fuzzing --future --harmony --js-staging --no-harmony-set-methods --no-enable-sharedarraybuffer-per-context --maglev-inline-api-calls --concurrent-maglev-high-priority-threads --no-optimize-on-next-call-optimizes-to-maglev --no-jitless --osr-from-maglev --always-osr-from-maglev --no-stress-lazy-source-positions --concurrent-sparkplug-high-priority-threads --no-sparkplug-needs-short-builtins --no-shared-string-table --no-transition-strings-during-gc-with-stack --no-stress-concurrent-inlining-attach-code --stress-turbo-late-spilling --no-stress-inline --reorder-builtins --turbo-instruction-scheduling --turbo-stress-instruction-scheduling --stress-gc-during-compilation --turboshaft-instruction-selection --no-turboshaft-wasm-instruction-selection-staged --no-turboshaft-verify-reductions --no-optimize-for-size --no-stress-wasm-code-gc --no-lazy-new-space-shrinking --no-separate-gc-phases --no-gc-global --scavenge-separate-stack-scanning --optimize-gc-for-battery --no-verify-heap --no-compact-on-every-full-gc --stress-compaction --no-stress-compaction-random --no-flush-baseline-code --flush-code-based-on-time --stress-flush-code --no-stress-per-context-marking-worklist --no-stress-incremental-marking --no-concurrent-marking-high-priority-threads --no-randomize-all-allocations --manual-evacuation-candidates-selection --no-enable-source-at-csa-bind --no-stress-background-compile --no-embedder-instance-types --no-expose-externalize-string --no-allow-unsafe-function-constructor --no-force-slow-path --no-max-lazy --always-turbofan --no-always-osr --prepare-always-turbofan --no-deopt-to-baseline --parallel-compile-tasks-for-eager-toplevel --no-expose-inspector-scripts --no-mega-dom-ic --no-regexp-interpret-all --no-minor-ms --no-slow-histograms --use-external-strings ./program_20231203045840_D49EF96A-E158-46A0-B38B-5B45F52B7759_flaky.js

and wait a long time. 

It works on my local.
#
# Fatal error in ../../src/objects/shared-function-info-inl.h, line 629
# Debug check failed: HasFeedbackMetadata(kAcquireLoad).
#
#
#
#FailureMessage Object: 0x7ff1a0bfae20
==== C stack trace ===============================

    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91325/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7ff1b5d7cdd3]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91325/libv8_libplatform.so(+0x19add) [0x7ff1b5d23add]
...

## Attachments

- [log.txt](attachments/log.txt) (text/plain, 6.4 KB)
- [program_20231203030957_557F1142-4278-457A-ACF6-7D57F68712CD_flaky.js](attachments/program_20231203030957_557F1142-4278-457A-ACF6-7D57F68712CD_flaky.js) (text/plain, 6.6 KB)
- [program_20231203013939_F30B454F-44CF-4A98-AE98-122CA44DFECC_flaky.js](attachments/program_20231203013939_F30B454F-44CF-4A98-AE98-122CA44DFECC_flaky.js) (text/plain, 19.5 KB)
- [program_20231203004608_9125402D-2FEC-4F7C-B929-767021731303_flaky.js](attachments/program_20231203004608_9125402D-2FEC-4F7C-B929-767021731303_flaky.js) (text/plain, 20.5 KB)
- [program_20231202223653_DFC5A2A0-B04B-4F95-8743-332C5F439182_flaky.js](attachments/program_20231202223653_DFC5A2A0-B04B-4F95-8743-332C5F439182_flaky.js) (text/plain, 20.1 KB)
- [program_20231202211949_F2F3F4A6-A713-4164-A8D8-72485EFA79F3_flaky.js](attachments/program_20231202211949_F2F3F4A6-A713-4164-A8D8-72485EFA79F3_flaky.js) (text/plain, 21.1 KB)
- [program_20231202114925_4DDEF1B6-6A57-4456-AE42-0EEDE9E79E2D_flaky.js](attachments/program_20231202114925_4DDEF1B6-6A57-4456-AE42-0EEDE9E79E2D_flaky.js) (text/plain, 24.5 KB)
- [testcase.tar.bz2](attachments/testcase.tar.bz2) (application/octet-stream, 14.5 KB)
- [1.png](attachments/1.png) (image/png, 341.6 KB)

## Timeline

### [Deleted User] (2023-12-02)

[Empty comment from Monorail migration]

### wh...@gmail.com (2023-12-02)

    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7fb9af097c73]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8_libplatform.so(+0x19add) [0x7fb9af03eadd]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x154) [0x7fb9af077d14]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8_libbase.so(+0x2b7d5) [0x7fb9af0777d5]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::FeedbackVector::metadata(v8::internal::PtrComprCageBase, v8::AcquireLoadTag) const+0x173) [0x7fb9b1d8f4d3]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::FeedbackNexus::FeedbackNexus(v8::internal::Handle<v8::internal::FeedbackVector>, v8::internal::FeedbackSlot, v8::internal::NexusConfig const&)+0xae) [0x7fb9b1d8763e]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::compiler::JSHeapBroker::ReadFeedbackForPropertyAccess(v8::internal::compiler::FeedbackSource const&, v8::internal::compiler::AccessMode, v8::internal::compiler::OptionalRef<v8::internal::compiler::NameRef>)+0x86) [0x7fb9b31fcad6]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::compiler::JSHeapBroker::GetFeedbackForPropertyAccess(v8::internal::compiler::FeedbackSource const&, v8::internal::compiler::AccessMode, v8::internal::compiler::OptionalRef<v8::internal::compiler::NameRef>)+0x5d) [0x7fb9b31ff8ed]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevGraphBuilder::VisitGetNamedProperty()+0xb7) [0x7fb9b261bbc7]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevGraphBuilder::VisitSingleBytecode()+0xd6e) [0x7fb9b254180e]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevGraphBuilder::BuildBody()+0x13b) [0x7fb9b253dbcb]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevGraphBuilder::BuildInlined(v8::internal::maglev::ValueNode*, v8::internal::maglev::ValueNode*, v8::internal::maglev::ValueNode*, v8::internal::maglev::CallArguments const&)+0x430) [0x7fb9b2623c90]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevGraphBuilder::TryBuildInlinedCall(v8::internal::maglev::ValueNode*, v8::internal::maglev::ValueNode*, v8::internal::maglev::ValueNode*, v8::internal::compiler::SharedFunctionInfoRef, v8::internal::compiler::OptionalRef<v8::internal::compiler::FeedbackVectorRef>, v8::internal::maglev::CallArguments&, v8::internal::compiler::FeedbackSource const&)+0x42a) [0x7fb9b262580a]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevGraphBuilder::TryBuildCallKnownJSFunction(v8::internal::maglev::ValueNode*, v8::internal::maglev::ValueNode*, v8::internal::maglev::ValueNode*, v8::internal::compiler::SharedFunctionInfoRef, v8::internal::compiler::OptionalRef<v8::internal::compiler::FeedbackVectorRef>, v8::internal::maglev::CallArguments&, v8::internal::compiler::FeedbackSource const&)+0x46) [0x7fb9b2631da6]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevGraphBuilder::TryBuildCallKnownJSFunction(v8::internal::compiler::JSFunctionRef, v8::internal::maglev::ValueNode*, v8::internal::maglev::CallArguments&, v8::internal::compiler::FeedbackSource const&)+0x11b) [0x7fb9b2631c8b]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevGraphBuilder::ReduceCallForConstant(v8::internal::compiler::JSFunctionRef, v8::internal::maglev::CallArguments&, v8::internal::compiler::FeedbackSource const&, v8::internal::SpeculationMode)+0x1fa) [0x7fb9b261407a]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevGraphBuilder::ReduceCall(v8::internal::maglev::ValueNode*, v8::internal::maglev::CallArguments&, v8::internal::compiler::FeedbackSource const&, v8::internal::SpeculationMode)+0x127) [0x7fb9b2627637]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevGraphBuilder::BuildCallWithFeedback(v8::internal::maglev::ValueNode*, v8::internal::maglev::CallArguments&, v8::internal::compiler::FeedbackSource const&)+0x10d) [0x7fb9b263253d]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevGraphBuilder::BuildCallFromRegisters(int, v8::internal::ConvertReceiverMode)+0x17c) [0x7fb9b2632d0c]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevGraphBuilder::VisitSingleBytecode()+0x6fb) [0x7fb9b254119b]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevGraphBuilder::BuildBody()+0x13b) [0x7fb9b253dbcb]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevGraphBuilder::Build()+0x284) [0x7fb9b253b0b4]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevCompiler::Compile(v8::internal::LocalIsolate*, v8::internal::maglev::MaglevCompilationInfo*)+0x657) [0x7fb9b2539db7]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x6a) [0x7fb9b25fff5a]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x96) [0x7fb9b14603d6]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8.so(v8::internal::maglev::MaglevConcurrentDispatcher::JobTask::Run(v8::JobDelegate*)+0x32c) [0x7fb9b2601d1c]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8_libpatform.so(v8::platform::DefaultJobWorker::Run()+0xd3) [0x7fb9af03d823]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8_libpatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+xc3) [0x7fb9af040213]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91311/libv8_libbse.so(+0x4a629) [0x7fb9af096629]

### wh...@gmail.com (2023-12-03)

Hi, the bug is very hard to reproduce. I not any other ideas, just run many instances and wait. 

here is poc generated by Fuzzilli.

### sr...@google.com (2023-12-04)

Assigning to the v8 sheriff since per https://crbug.com/chromium/1507412#c3 it sounds unlikely that CF will reproduce this.
The foundin and severity labels are just provisional.

[Monorail components: Blink>JavaScript>Compiler>Maglev]

### [Deleted User] (2023-12-04)

[Empty comment from Monorail migration]

### is...@chromium.org (2023-12-04)

Thank you for the report. What are the command line and GN args you used for triggering the issue?

### wh...@gmail.com (2023-12-04)

my fuzz d8 gn: 
is_debug=false 
dcheck_always_on=true 
v8_static_library=true v8_enable_slow_
dchecks=true 
v8_enable_verify_heap=true 
v8_enable_verify_csa=true
v8_fuzzilli=true 
sanitizer_coverage_flags="trace-pc-guard" 
target_cpu="x64"

I also can reproduce with linux-debug_d8-linux-debug-v8-component-91311.zip
and gn is 
is_component_build = true
is_debug = true
target_cpu = "x64"
use_remoteexec = true
v8_enable_backtrace = true
v8_enable_google_benchmark = true
v8_enable_slow_dchecks = true


### wh...@gmail.com (2023-12-04)

You can run following command in many terminal: 
```fire.bash 
#!/usr/bin/env bash 
#
#
for i in {1..999}
do 
        echo ======== $i ============
        $@ 
        RET=$?
        if [ $RET -ne 0 ] && [ $RET -ne 134 ]; then 
                                        echo $RET
          break 
        fi 
done
```

fire.bash ~/asan/d8_debug_zip/d8-linux-debug-v8-component-91325/d8 --expose-gc --omit-quit --allow-natives-syntax --fuzzing --jit-fuzzing --future --harmony --js-staging --no-harmony-set-methods --no-enable-sharedarraybuffer-per-context --maglev-inline-api-calls --concurrent-maglev-high-priority-threads --no-optimize-on-next-call-optimizes-to-maglev --no-jitless --osr-from-maglev --always-osr-from-maglev --no-stress-lazy-source-positions --concurrent-sparkplug-high-priority-threads --no-sparkplug-needs-short-builtins --no-shared-string-table --no-transition-strings-during-gc-with-stack --no-stress-concurrent-inlining-attach-code --stress-turbo-late-spilling --no-stress-inline --reorder-builtins --turbo-instruction-scheduling --turbo-stress-instruction-scheduling --stress-gc-during-compilation --turboshaft-instruction-selection --no-turboshaft-wasm-instruction-selection-staged --no-turboshaft-verify-reductions --no-optimize-for-size --no-stress-wasm-code-gc --no-lazy-new-space-shrinking --no-separate-gc-phases --no-gc-global --scavenge-separate-stack-scanning --optimize-gc-for-battery --no-verify-heap --no-compact-on-every-full-gc --stress-compaction --no-stress-compaction-random --no-flush-baseline-code --flush-code-based-on-time --stress-flush-code --no-stress-per-context-marking-worklist --no-stress-incremental-marking --no-concurrent-marking-high-priority-threads --no-randomize-all-allocations --manual-evacuation-candidates-selection --no-enable-source-at-csa-bind --no-stress-background-compile --no-embedder-instance-types --no-expose-externalize-string --no-allow-unsafe-function-constructor --no-force-slow-path --no-max-lazy --always-turbofan --no-always-osr --prepare-always-turbofan --no-deopt-to-baseline --parallel-compile-tasks-for-eager-toplevel --no-expose-inspector-scripts --no-mega-dom-ic --no-regexp-interpret-all --no-minor-ms --no-slow-histograms --use-external-strings ./program_20231203045840_D49EF96A-E158-46A0-B38B-5B45F52B7759_flaky.js

and wait a long time. 

It works on my local.
#
# Fatal error in ../../src/objects/shared-function-info-inl.h, line 629
# Debug check failed: HasFeedbackMetadata(kAcquireLoad).
#
#
#
#FailureMessage Object: 0x7ff1a0bfae20
==== C stack trace ===============================

    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91325/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7ff1b5d7cdd3]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-91325/libv8_libplatform.so(+0x19add) [0x7ff1b5d23add]
...

### [Deleted User] (2023-12-04)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### ja...@chromium.org (2023-12-13)

Reassigning to the current v8 shepherd.

clemensb@, now that we have the relevant gn args, could you take a look and further triage it?

Thanks!

### wh...@gmail.com (2023-12-14)

Note that I can reproduce at 91499. 

### is...@chromium.org (2023-12-14)

Last week it didn't work for me at 91311 and on last week's ToT. Maybe there will be a better luck at 91499.

### wh...@gmail.com (2023-12-14)

You can try run multiples instance d8 and try make cpu to 100%, it may better to reproduce. 

### is...@chromium.org (2023-12-14)

Yes, I tried that. Will give another try in the next days.

### cl...@chromium.org (2023-12-14)

I tried for three hours now, always running 50 instances in parallel. No reproduction. This was on 91500.

I will close this as WontFix for now, until we have a better reproducer. It's not actionable otherwise.

### wh...@gmail.com (2023-12-14)

Why don't you try to analyze the source code? Doesn't it provide stack trace information?

And I just now reproduce successful on 91510. 

My env is 6core,12threads, 48g memory 
and I just running 8 instances, it successful reproce. 

I use poc named program_20231202114925_4DDEF1B6-6A57-4456-AE42-0EEDE9E79E2D_flaky.js

Please consider maybe you can try reproduce on you laptop? or less cpu ? 




### wh...@gmail.com (2023-12-14)

And you just tested 3 hours...

### is...@chromium.org (2023-12-14)

[Empty comment from Monorail migration]

### is...@chromium.org (2023-12-14)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript>Compiler>Turbofan]

### is...@chromium.org (2023-12-14)

I'll try to prepare a speculative fix.

### di...@chromium.org (2023-12-15)

Could you please test whether you can still reproduce the crash with this CL here: https://chromium-review.googlesource.com/c/v8/v8/+/5125960

### wh...@gmail.com (2023-12-15)

Sure.

### di...@chromium.org (2023-12-15)

I was able to reproduce your crash and that CL fixed it for me locally.

### wh...@gmail.com (2023-12-15)

get, I'll test it again.

### wh...@gmail.com (2023-12-15)

I tried different poc and can't reproduce, it should be fixed I think.

### is...@chromium.org (2023-12-15)

Thank you for the report!

### gi...@appspot.gserviceaccount.com (2023-12-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/46cb67e3b296e50d7fda5a58233d18b9f3dab0d5

commit 46cb67e3b296e50d7fda5a58233d18b9f3dab0d5
Author: Dominik Inführ <dinfuehr@chromium.org>
Date: Mon Dec 18 08:15:00 2023

[codegen] Install BytecodeArray last in SharedFunctionInfo

Maglev assumes that when a SharedFunctionInfo has a BytecodeArray,
then it should also have FeedbackMetadata. However, this may not
hold with concurrent compilation when the SharedFunctionInfo is
re-compiled after being flushed. Here the BytecodeArray was installed
on the SFI before the FeedbackMetadata and a concurrent thread could
observe the BytecodeArray but not the FeedbackMetadata.

Drive-by: Reset the age field before setting the BytecodeArray as
well. This ensures that the concurrent marker will not observe the
old age for the new BytecodeArray.

Bug: chromium:1507412
Change-Id: I8855ed7ecc50c4a47d2c89043d62ac053858bc75
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5125960
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#91568}

[modify] https://crrev.com/46cb67e3b296e50d7fda5a58233d18b9f3dab0d5/src/codegen/compiler.cc


### di...@chromium.org (2023-12-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-18)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M120. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M121. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-19)

Merge review required: M121 is already shipping to beta.

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
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-19)

Merge review required: M120 is already shipping to stable.

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
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-12-19)

Since this fix was just landed 24 hours ago, I'm going to defer merge review until tomorrow or Thursday there has been a bit more canary bake time for this fix on Canary.

### [Deleted User] (2023-12-20)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=1507412&entry.364066060=External&entry.958145677=Android&entry.958145677=Chrome&entry.958145677=Fuchsia&entry.958145677=Linux&entry.958145677=Mac&entry.958145677=Windows&entry.958145677=Lacros&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>JavaScript>Compiler>Maglev,Blink>JavaScript>Compiler>Turbofan&entry.975983575=dinfuehr@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-12-27)

121 and 120 merges approved for https://crrev.com/c/5125960
please merge this fix to 12.1-lkgr and 12.0-lkgr before Tuesday 2 January so this fix can be included in the next M121 Beta and M120 Stable updates -- thank you`

### [Deleted User] (2024-01-01)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-05)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2024-01-08)

Please merge your change to M121 by 3:00 PM PT today so we can take it in for tomorrow's beta release. Thank you. 

### am...@chromium.org (2024-01-08)

[Description Changed]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2024-01-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/83b0567f57ac4764e2fe65626071e2cb6faa9ba0

commit 83b0567f57ac4764e2fe65626071e2cb6faa9ba0
Author: Dominik Inführ <dinfuehr@chromium.org>
Date: Mon Dec 18 08:15:00 2023

Merged: [codegen] Install BytecodeArray last in SharedFunctionInfo

Maglev assumes that when a SharedFunctionInfo has a BytecodeArray,
then it should also have FeedbackMetadata. However, this may not
hold with concurrent compilation when the SharedFunctionInfo is
re-compiled after being flushed. Here the BytecodeArray was installed
on the SFI before the FeedbackMetadata and a concurrent thread could
observe the BytecodeArray but not the FeedbackMetadata.

Drive-by: Reset the age field before setting the BytecodeArray as
well. This ensures that the concurrent marker will not observe the
old age for the new BytecodeArray.

Bug: chromium:1507412
(cherry picked from commit 46cb67e3b296e50d7fda5a58233d18b9f3dab0d5)

Change-Id: I7b876a5195ed16ae94ca9ffbca0fb51cfdb5e809
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5180368
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
Cr-Commit-Position: refs/branch-heads/12.1@{#39}
Cr-Branched-From: b74ef6f2cd2fe60c91abcd3271b661547a47ca4f-refs/heads/12.1.285@{#1}
Cr-Branched-From: 32857fbeb042c27010127aa02bbfaffcc0bf0829-refs/heads/main@{#91313}

[modify] https://crrev.com/83b0567f57ac4764e2fe65626071e2cb6faa9ba0/src/codegen/compiler.cc


### [Deleted User] (2024-01-09)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2024-01-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/da8b9065d1a1cb8a521ed6c76337400ec19e1143

commit da8b9065d1a1cb8a521ed6c76337400ec19e1143
Author: Dominik Inführ <dinfuehr@chromium.org>
Date: Mon Dec 18 08:15:00 2023

Merged: [codegen] Install BytecodeArray last in SharedFunctionInfo

Maglev assumes that when a SharedFunctionInfo has a BytecodeArray,
then it should also have FeedbackMetadata. However, this may not
hold with concurrent compilation when the SharedFunctionInfo is
re-compiled after being flushed. Here the BytecodeArray was installed
on the SFI before the FeedbackMetadata and a concurrent thread could
observe the BytecodeArray but not the FeedbackMetadata.

Drive-by: Reset the age field before setting the BytecodeArray as
well. This ensures that the concurrent marker will not observe the
old age for the new BytecodeArray.

Bug: chromium:1507412
(cherry picked from commit 46cb67e3b296e50d7fda5a58233d18b9f3dab0d5)

Change-Id: Ide73ac1c6b0a68a1fcf847c8351ec65016e55762
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5180369
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
Cr-Commit-Position: refs/branch-heads/12.0@{#28}
Cr-Branched-From: ed7b4caf1fb8184ad9e24346c84424055d4d430a-refs/heads/12.0.267@{#1}
Cr-Branched-From: 210e75b19db4352c9b78dce0bae11c2dc3077df4-refs/heads/main@{#90651}

[modify] https://crrev.com/da8b9065d1a1cb8a521ed6c76337400ec19e1143/src/codegen/compiler.cc


### go...@chromium.org (2024-01-09)

[Empty comment from Monorail migration]

### wh...@gmail.com (2024-01-10)

Hi,
May I get a CVE for the report?

### am...@chromium.org (2024-01-10)

Hello, CVEs are issued to reports at the time the fix ships in a Stable channel update. [1]
Barring any issues or unforeseen circumstances, this should occur next week when this fix ships in the scheduled M120 Stable update. 


[1] https://chromium.googlesource.com/chromium/src/+/main/docs/security/life-of-a-security-issue.md#10_assign-cve

### wh...@gmail.com (2024-01-10)

Thanks for the reply.

### am...@google.com (2024-01-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-01-11)

Congratulations! The Chrome VRP Panel has decided to award you $1,000 for this report of a significantly mitigated renderer memory corruption issue, mitigated by race and reliably to successfully trigger. Thank you for your efforts and reporting this issue to us. 

### wh...@gmail.com (2024-01-11)

[Comment Deleted]

### wh...@gmail.com (2024-01-11)

[1] https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules#reward-amounts-for-mitigated-security-bugs

### am...@chromium.org (2024-01-11)

Hello, if race were the only mitigation here, then we could have potentially considered this issue to be moderately mitigated; however, this issue was not able to be reliably or efficiently reproduced by the team based on the information and testcase provided. Running a POC for many hours and leveraging many cores or machines is indeed considered part of mitigations and report quality/characteristics. 

Additionally, please re-review the chart that you've linked above. The reward amount of $3,000 for a moderately mitigated is for a moderately mitigated bug in the browser process or other non-sandboxed process. This issue is in the renderer/sandboxed process, which is up to $2,000 for a moderately mitigated bug. 

### wh...@gmail.com (2024-01-11)

[Comment Deleted]

### am...@chromium.org (2024-01-11)

I said if it was just a race it could potentially be considered moderately mitigated, but it is mitigated by both race and substantial inability to trigger or reproduce this issue, such as that it was not demonstrated to even trigger in a default, shipped configuration of Chrome based on the information you provided and the analysis by the team. It is also important to remember that report quality impacts reward amounts. Reward amounts are "up to" an amount reflected in the table. This report did not meet baseline characteristics expected from VRP reports. 

So even with if this report were considered moderately mitigated, which we do not consider it to be, the reward amount for a moderately mitigated bug in a sandboxed process is "up to $2,000" with highly mitigated being up to $1,000. Based on all of the parameters listed above, we feel this reward amount is adequate and fitting for the issue and report. 

### wh...@gmail.com (2024-01-11)

All right, thank you for the reply.

### rz...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-11)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2024-01-11)

1. Just https://crrev.com/c/5189926
2. Low, just a simple conflict
3. 120, 121
4. Yes

### am...@google.com (2024-01-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2024-01-12)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-16)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-16)

[Empty comment from Monorail migration]

### na...@google.com (2024-01-22)

Merge approved for LTS-114

### gi...@appspot.gserviceaccount.com (2024-01-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/dd1b8f7969111b2227fc01b408d07005927e72a4

commit dd1b8f7969111b2227fc01b408d07005927e72a4
Author: Dominik Inführ <dinfuehr@chromium.org>
Date: Mon Dec 18 08:15:00 2023

[M114-LTS][codegen] Install BytecodeArray last in SharedFunctionInfo

M114 merge issues:
  codegen/compiler.cc:
    set_age() isn't called in 114 - removed it from the change.

Maglev assumes that when a SharedFunctionInfo has a BytecodeArray,
then it should also have FeedbackMetadata. However, this may not
hold with concurrent compilation when the SharedFunctionInfo is
re-compiled after being flushed. Here the BytecodeArray was installed
on the SFI before the FeedbackMetadata and a concurrent thread could
observe the BytecodeArray but not the FeedbackMetadata.

Drive-by: Reset the age field before setting the BytecodeArray as
well. This ensures that the concurrent marker will not observe the
old age for the new BytecodeArray.

(cherry picked from commit 46cb67e3b296e50d7fda5a58233d18b9f3dab0d5)

Bug: chromium:1507412
No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Change-Id: I8855ed7ecc50c4a47d2c89043d62ac053858bc75
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5125960
Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#91568}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5189926
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/11.4@{#79}
Cr-Branched-From: 8a8a1e7086dacc426965d3875914efa66663c431-refs/heads/11.4.183@{#1}
Cr-Branched-From: 5483d8e816e0bbce865cbbc3fa0ab357e6330bab-refs/heads/main@{#87241}

[modify] https://crrev.com/dd1b8f7969111b2227fc01b408d07005927e72a4/src/codegen/compiler.cc


### rz...@google.com (2024-01-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2024-01-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/eb2fa83c6b4a19d4d066fe3abd62ba6fc79e652b

commit eb2fa83c6b4a19d4d066fe3abd62ba6fc79e652b
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Jan 25 18:13:58 2024

Roll v8 11.4 from d53ecb521a43 to 8103d8ca6048 (2 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/d53ecb521a43..8103d8ca6048

2024-01-25 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.4.183.40
2024-01-25 dinfuehr@chromium.org [M114-LTS][codegen] Install BytecodeArray last in SharedFunctionInfo

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-11-4-chromium-m114
Please CC liviurau@google.com,v8-waterfall-sheriff@grotations.appspotmail.com,vahl@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 11.4: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m114: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://issues.skia.org/issues/new?component=1389291&template=1850622

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1507412
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: Ib257470d15deb9c529a71f60d4cfd21715c41847
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5236832
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5735@{#1674}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/eb2fa83c6b4a19d4d066fe3abd62ba6fc79e652b/DEPS


### is...@google.com (2024-01-25)

This issue was migrated from crbug.com/chromium/1507412?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript>Compiler>Maglev, Blink>JavaScript>Compiler>Turbofan]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40948107)*
