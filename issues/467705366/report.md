# [wasm][fast-api] Race between background compilation and NativeModule teardown could lead to UAF

| Field | Value |
|-------|-------|
| **Issue ID** | [467705366](https://issues.chromium.org/issues/467705366) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pi...@gmail.com |
| **Assignee** | ah...@google.com |
| **Created** | 2025-12-11 |
| **Bounty** | Confirmed (amount unknown) |

## Description

# VULNERABILITY DETAILS

## Summary

A use-after-free vulnerability exists in WebAssembly TurboShaft compilation pipeline when handling Fast API calls. The vulnerability stems from a lifetime management issue where background compilation threads access freed memory after the `NativeModule` destructor has released the `fast_api_targets_` and `fast_api_signatures_` arrays.

## Root Cause

The `NativeModule` constructor allocates `fast_api_targets_` and `fast_api_signatures_` arrays as `unique_ptr` members:

```
// src/wasm/wasm-code-manager.cc
NativeModule::NativeModule(...)
    : ...,
      fast_api_targets_(
          new std::atomic<Address>[module_->num_imported_functions]()),
      fast_api_signatures_(
          new std::atomic<const MachineSignature*>[module_->num_imported_functions]()) {}

```

When `CompilationEnv::ForModule()` is called, it extracts **raw pointers** to these arrays:

```
// src/wasm/compilation-environment-inl.h
inline CompilationEnv CompilationEnv::ForModule(const NativeModule* native_module) {
  return CompilationEnv(
      native_module->module(), native_module->enabled_features(),
      native_module->fast_api_targets(),    // raw pointer
      native_module->fast_api_signatures(), // raw pointer
      native_module->coverage_data());
}

```

During background compilation, `BackgroundCompileScope` temporarily holds a `shared_ptr<NativeModule>` while extracting the compilation unit and building `CompilationEnv`. However, the scope is released **before** the actual compilation begins:

```
// src/wasm/module-compiler.cc
{
  BackgroundCompileScope compile_scope(native_module);
  env.emplace(CompilationEnv::ForModule(compile_scope.native_module()));
  unit = compile_scope.compilation_state()->GetNextCompilationUnit(queue, tier);
}
// shared_ptr released here, but env still holds raw pointers

while (true) {
  // Compilation executes with potentially dangling pointers
  WasmCompilationResult result = unit->ExecuteCompilation(&env.value(), ...);
}

```

If the last `shared_ptr<NativeModule>` is released during this window, `~NativeModule()` destroys the Fast API arrays. The background compilation thread then accesses freed memory when `TurboshaftGraphBuildingInterface::WellKnown_FastApi()` reads `env_->fast_api_signatures[func_index]` or `env_->fast_api_targets[func_index]`.

**Note**: The attached poc.js loads the wasm-module-builder.js in /test/mjsunit/wasm/wasm-module-builder.js and uses a worker to reproduce it stably.

## VERSION

V8: ~ 14.4.258.6

## REPRODUCTION CASE

Build v8 with args.gn:

```
is_debug=true
is_asan=true
dcheck_always_on=true
v8_static_library=true 
v8_enable_verify_heap=true 

v8_enable_i18n_support=true
is_component_build=false

target_cpu="x64"
v8_enable_sandbox=true
v8_enable_memory_corruption_api=true

```

Run d8 with:

```
./d8 --wasm-fast-api --expose-fast-api --jit-fuzzing poc.js

```

Crash State:

```
=================================================================
==4157403==ERROR: AddressSanitizer: heap-use-after-free on address 0x7b21eb2f1110 at pc 0x564cfd50e6fa bp 0x7b01c40b7a50 sp 0x7b01c40b7a48
READ of size 8 at 0x7b21eb2f1110 thread T32 (V8 DefaultWorke)
    #0 0x564cfd50e6f9 in __cxx_atomic_load<const v8::internal::Signature<v8::internal::MachineType> *> gen/third_party/libc++/src/include/__atomic/support/c11.h:81:10
    #1 0x564cfd50e6f9 in load gen/third_party/libc++/src/include/__atomic/atomic.h:71:12
    #2 0x564cfd50e6f9 in operator const v8::internal::Signature<v8::internal::MachineType> * gen/third_party/libc++/src/include/__atomic/atomic.h:74:65
    #3 0x564cfd50e6f9 in v8::internal::wasm::TurboshaftGraphBuildingInterface::WellKnown_FastApi(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::CallFunctionImmediate const&, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*) src/wasm/turboshaft-graph-interface.cc:1901:9
    #4 0x564cfd4edcdd in v8::internal::wasm::TurboshaftGraphBuildingInterface::HandleWellKnownImport(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::CallFunctionImmediate const&, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*) src/wasm/turboshaft-graph-interface.cc:2486:9
    #5 0x564cfd4eb8da in v8::internal::wasm::TurboshaftGraphBuildingInterface::CallDirect(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::CallFunctionImmediate const&, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value const*, v8::internal::wasm::TurboshaftGraphBuildingInterface::Value*) src/wasm/turboshaft-graph-interface.cc:2505:11
    #6 0x564cfd4eb244 in v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallFunctionImpl(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::TraceLine*, v8::internal::wasm::WasmOpcode) src/wasm/function-body-decoder-impl.h:4420:40
    #7 0x564cfd46cdf5 in v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeCallFunction(v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>*, v8::internal::wasm::WasmOpcode) src/wasm/function-body-decoder-impl.h:4415:3
    #8 0x564cfd43a8f5 in v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::DecodeFunctionBody() src/wasm/function-body-decoder-impl.h:3303:17
    #9 0x564cfd430376 in v8::internal::wasm::WasmFullDecoder<v8::internal::wasm::Decoder::NoValidationTag, v8::internal::wasm::TurboshaftGraphBuildingInterface, (v8::internal::wasm::DecodingMode)0>::Decode() src/wasm/function-body-decoder-impl.h:3126:5
    #10 0x564cfd42f6bf in v8::internal::wasm::BuildTSGraph(v8::internal::compiler::turboshaft::PipelineData*, v8::internal::AccountingAllocator*, v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WasmDetectedFeatures*, v8::internal::compiler::turboshaft::Graph&, v8::internal::wasm::FunctionBody const&, v8::internal::wasm::WireBytesStorage const*, std::__Cr::unique_ptr<v8::internal::wasm::AssumptionsJournal, std::__Cr::default_delete<v8::internal::wasm::AssumptionsJournal>>*, v8::internal::ZoneVector<v8::internal::WasmInliningPosition>*, int, v8::internal::wasm::WasmFunctionCoverageData*) src/wasm/turboshaft-graph-interface.cc:9371:11
    #11 0x564cfb1f6552 in v8::internal::compiler::Pipeline::GenerateWasmCode(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmDetectedFeatures*, v8::internal::DelayedCounterUpdates*) src/compiler/pipeline.cc:3185:3
    #12 0x564cfd3d2e88 in v8::internal::compiler::turboshaft::ExecuteTurboshaftWasmCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::compiler::WasmCompilationData&, v8::internal::wasm::WasmDetectedFeatures*, v8::internal::DelayedCounterUpdates*) src/compiler/turboshaft/wasm-turboshaft-compiler.cc:26:7
    #13 0x564cfa10f8d4 in v8::internal::wasm::WasmCompilationUnit::ExecuteCompilation(v8::internal::wasm::CompilationEnv*, v8::internal::wasm::WireBytesStorage const*, v8::internal::DelayedCounterUpdates*, v8::internal::wasm::WasmDetectedFeatures*) src/wasm/function-compiler.cc:128:16
    #14 0x564cfa14606e in v8::internal::wasm::(anonymous namespace)::ExecuteCompilationUnits(std::__Cr::weak_ptr<v8::internal::wasm::NativeModule>, v8::JobDelegate*, v8::internal::wasm::(anonymous namespace)::CompilationTier) src/wasm/module-compiler.cc:2051:44
    #15 0x564cfa144a2c in v8::internal::wasm::(anonymous namespace)::BackgroundCompileJob::Run(v8::JobDelegate*) src/wasm/module-compiler.cc:2213:5
    #16 0x564cf6f0fe6a in v8::platform::DefaultJobWorker::Run() src/libplatform/default-job.h:147:18
    #17 0x564cf6f2258e in v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run() src/libplatform/default-worker-threads-task-runner.cc:95:25
    #18 0x564cf6f0387d in NotifyStartedAndRun src/base/platform/platform.h:633:5
    #19 0x564cf6f0387d in v8::base::ThreadEntry(void*) src/base/platform/platform-posix.cc:1292:11
    #20 0x564cf688eb86 in asan_thread_start(void*) asan_interceptors.cpp

0x7b21eb2f1110 is located 0 bytes inside of 8-byte region [0x7b21eb2f1110,0x7b21eb2f1118)
freed by thread T49 (WorkerThread) here:
    #0 0x564cf68caf7d in operator delete[](void*) (/home/user/v8_build/v8/out/debug_fuzz_144/d8+0x2e3af7d) (BuildId: a0b4f266c3444722)
    #1 0x564cfa25b225 in operator()<std::__Cr::atomic<const v8::internal::Signature<v8::internal::MachineType> *>, 0> gen/third_party/libc++/src/include/__memory/unique_ptr.h:88:5
    #2 0x564cfa25b225 in reset gen/third_party/libc++/src/include/__memory/unique_ptr.h:611:7
    #3 0x564cfa25b225 in ~unique_ptr gen/third_party/libc++/src/include/__memory/unique_ptr.h:566:71
    #4 0x564cfa25b225 in v8::internal::wasm::NativeModule::~NativeModule() src/wasm/wasm-code-manager.cc:2150:1
    #5 0x564cfa278494 in operator() gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #6 0x564cfa278494 in std::__Cr::__shared_ptr_pointer<v8::internal::wasm::NativeModule*, std::__Cr::shared_ptr<v8::internal::wasm::NativeModule>::__shared_ptr_default_delete<v8::internal::wasm::NativeModule, v8::internal::wasm::NativeModule>, std::__Cr::allocator<v8::internal::wasm::NativeModule>>::__on_zero_shared() gen/third_party/libc++/src/include/__memory/shared_ptr.h:122:3
    #7 0x564cfa300aa8 in __release_shared gen/third_party/libc++/src/include/__memory/shared_count.h:65:7
    #8 0x564cfa300aa8 in __release_shared gen/third_party/libc++/src/include/__memory/shared_count.h:100:25
    #9 0x564cfa300aa8 in ~shared_ptr gen/third_party/libc++/src/include/__memory/shared_ptr.h:501:17
    #10 0x564cfa300aa8 in void v8::internal::detail::Destructor<v8::internal::wasm::NativeModule>(void*) src/objects/managed-inl.h:21:3
    #11 0x564cf76cf0c9 in v8::internal::Isolate::ReleaseSharedPtrs() src/execution/isolate.cc:3836:7
    #12 0x564cf76d143f in v8::internal::Isolate::Deinit() src/execution/isolate.cc:4659:3
    #13 0x564cf76d03e2 in v8::internal::Isolate::Deinitialize(v8::internal::Isolate*) src/execution/isolate.cc:4253:12
    #14 0x564cf76d021d in v8::internal::Isolate::Delete(v8::internal::Isolate*) src/execution/isolate.cc:4234:3
    #15 0x564cf6953807 in v8::Worker::ExecuteInThread() src/d8/d8.cc:6031:13
    #16 0x564cf69522e5 in v8::Worker::WorkerThread::Run() src/d8/d8.cc:5723:11
    #17 0x564cf6f0387d in NotifyStartedAndRun src/base/platform/platform.h:633:5
    #18 0x564cf6f0387d in v8::base::ThreadEntry(void*) src/base/platform/platform-posix.cc:1292:11
    #19 0x564cf688eb86 in asan_thread_start(void*) asan_interceptors.cpp

previously allocated by thread T49 (WorkerThread) here:
    #0 0x564cf68ca75d in operator new[](unsigned long) (/home/user/v8_build/v8/out/debug_fuzz_144/d8+0x2e3a75d) (BuildId: a0b4f266c3444722)
    #1 0x564cfa24b257 in v8::internal::wasm::NativeModule::NativeModule(v8::internal::wasm::WasmEnabledFeatures, v8::internal::wasm::WasmDetectedFeatures, v8::internal::wasm::CompileTimeImports, v8::internal::VirtualMemory, std::__Cr::shared_ptr<v8::internal::wasm::WasmModule const>, std::__Cr::shared_ptr<v8::internal::wasm::NativeModule>*) src/wasm/wasm-code-manager.cc:1016:11
    #2 0x564cfa25cfa7 in v8::internal::wasm::WasmCodeManager::NewNativeModule(v8::internal::wasm::WasmEnabledFeatures, v8::internal::wasm::WasmDetectedFeatures, v8::internal::wasm::CompileTimeImports, unsigned long, std::__Cr::shared_ptr<v8::internal::wasm::WasmModule const>) src/wasm/wasm-code-manager.cc:2563:7
    #3 0x564cfa2ef29a in v8::internal::wasm::WasmEngine::NewUnownedNativeModule(v8::internal::wasm::WasmEnabledFeatures, v8::internal::wasm::WasmDetectedFeatures, v8::internal::wasm::CompileTimeImports, std::__Cr::shared_ptr<v8::internal::wasm::WasmModule const>, unsigned long) src/wasm/wasm-engine.cc:1561:29
    #4 0x564cfa2eec9e in v8::internal::wasm::WasmEngine::NewNativeModule(v8::internal::Isolate*, v8::internal::wasm::WasmEnabledFeatures, v8::internal::wasm::WasmDetectedFeatures, v8::internal::wasm::CompileTimeImports, std::__Cr::shared_ptr<v8::internal::wasm::WasmModule const>, unsigned long) src/wasm/wasm-engine.cc:1546:49
    #5 0x564cfa12b550 in GetOrCompileNewNativeModule src/wasm/module-compiler.cc:2270:36
    #6 0x564cfa12b550 in v8::internal::wasm::CompileToNativeModule(v8::internal::Isolate*, v8::internal::wasm::WasmEnabledFeatures, v8::internal::wasm::WasmDetectedFeatures, v8::internal::wasm::CompileTimeImports, v8::internal::wasm::ErrorThrower*, std::__Cr::shared_ptr<v8::internal::wasm::WasmModule const>, v8::base::OwnedVector<unsigned char const>, int, v8::metrics::Recorder::ContextId, v8::internal::wasm::ProfileInformation*) src/wasm/module-compiler.cc:2332:49
    #7 0x564cfa2d92f6 in v8::internal::wasm::WasmEngine::SyncCompile(v8::internal::Isolate*, v8::internal::wasm::WasmEnabledFeatures, v8::internal::wasm::CompileTimeImports, v8::internal::wasm::ErrorThrower*, v8::base::OwnedVector<unsigned char const>) src/wasm/wasm-engine.cc:703:49
    #8 0x564cfa34a6eb in WebAssemblyModuleImpl src/wasm/wasm-js.cc:994:48
    #9 0x564cfa34a6eb in v8::internal::wasm::WebAssemblyModule(v8::FunctionCallbackInfo<v8::Value> const&) src/wasm/wasm-js.cc:3279:33
    #10 0x564cf702de53 in v8::internal::FunctionCallbackArguments::CallOrConstruct(v8::internal::Tagged<v8::internal::FunctionTemplateInfo>, bool) src/api/api-arguments-inl.h:107:3
    #11 0x564cf702afcd in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::HeapObject>, v8::internal::DirectHandle<v8::internal::FunctionTemplateInfo>, v8::internal::DirectHandle<v8::internal::Object>, unsigned long*, int) src/builtins/builtins-api.cc:105:16
    #12 0x564cf7028172 in Builtin_Impl_HandleApiConstruct src/builtins/builtins-api.cc:137:16
    #13 0x564cf7028172 in v8::internal::Builtin_HandleApiConstruct(int, unsigned long*, v8::internal::Isolate*) src/builtins/builtins-api.cc:127:1
    #14 0x564cfddcadbc in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #15 0x564cfd85ce4c in Builtins_InterpreterPushArgsThenFastConstructFunction setup-isolate-deserialize.cc
    #16 0x564cfe6c9e06 in Builtins_ConstructHandler setup-isolate-deserialize.cc
    #17 0x564cfd85c275 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #18 0x564cfd85c275 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #19 0x564cfd84e966 in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #20 0x564cfd84e6aa in Builtins_JSEntry setup-isolate-deserialize.cc
    #21 0x564cf76688db in Call src/execution/simulator.h:212:12
    #22 0x564cf76688db in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:442:22
    #23 0x564cf766b5cb in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:542:10
    #24 0x564cf6f4222c in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:1980:7
    #25 0x564cf69106f4 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1050:44
    #26 0x564cf6953174 in v8::Worker::ExecuteInThread() src/d8/d8.cc:5995:21
    #27 0x564cf69522e5 in v8::Worker::WorkerThread::Run() src/d8/d8.cc:5723:11
    #28 0x564cf6f0387d in NotifyStartedAndRun src/base/platform/platform.h:633:5
    #29 0x564cf6f0387d in v8::base::ThreadEntry(void*) src/base/platform/platform-posix.cc:1292:11
    #30 0x564cf688eb86 in asan_thread_start(void*) asan_interceptors.cpp

Thread T32 (V8 DefaultWorke) created by T0 here:
    #0 0x564cf6874921 in pthread_create (/home/user/v8_build/v8/out/debug_fuzz_144/d8+0x2de4921) (BuildId: a0b4f266c3444722)
    #1 0x564cf6f0366b in v8::base::Thread::Start() src/base/platform/platform-posix.cc:1324:14
    #2 0x564cf6f2180c in WorkerThread src/libplatform/default-worker-threads-task-runner.cc:80:9
    #3 0x564cf6f2180c in make_unique<v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread, v8::platform::DefaultWorkerThreadsTaskRunner *, v8::base::Thread::Priority &, 0> gen/third_party/libc++/src/include/__memory/unique_ptr.h:752:30
    #4 0x564cf6f2180c in v8::platform::DefaultWorkerThreadsTaskRunner::DefaultWorkerThreadsTaskRunner(unsigned int, double (*)(), v8::base::Thread::Priority) src/libplatform/default-worker-threads-task-runner.cc:18:28
    #5 0x564cf6f069bd in construct_at<v8::platform::DefaultWorkerThreadsTaskRunner, const int &, double (*)(), v8::base::Thread::Priority, v8::platform::DefaultWorkerThreadsTaskRunner *> gen/third_party/libc++/src/include/__memory/construct_at.h:37:49
    #6 0x564cf6f069bd in __construct_at<v8::platform::DefaultWorkerThreadsTaskRunner, const int &, double (*)(), v8::base::Thread::Priority, v8::platform::DefaultWorkerThreadsTaskRunner *> gen/third_party/libc++/src/include/__memory/construct_at.h:45:10
    #7 0x564cf6f069bd in construct<v8::platform::DefaultWorkerThreadsTaskRunner, const int &, double (*)(), v8::base::Thread::Priority, 0> gen/third_party/libc++/src/include/__memory/allocator_traits.h:302:5
    #8 0x564cf6f069bd in __shared_ptr_emplace<const int &, double (*)(), v8::base::Thread::Priority, std::__Cr::allocator<v8::platform::DefaultWorkerThreadsTaskRunner>, 0> gen/third_party/libc++/src/include/__memory/shared_ptr.h:161:5
    #9 0x564cf6f069bd in allocate_shared<v8::platform::DefaultWorkerThreadsTaskRunner, std::__Cr::allocator<v8::platform::DefaultWorkerThreadsTaskRunner>, const int &, double (*)(), v8::base::Thread::Priority, 0> gen/third_party/libc++/src/include/__memory/shared_ptr.h:676:51
    #10 0x564cf6f069bd in make_shared<v8::platform::DefaultWorkerThreadsTaskRunner, const int &, double (*)(), v8::base::Thread::Priority, 0> gen/third_party/libc++/src/include/__memory/shared_ptr.h:684:10
    #11 0x564cf6f069bd in v8::platform::DefaultPlatform::EnsureBackgroundTaskRunnerInitialized() src/libplatform/default-platform.cc:141:9
    #12 0x564cf6f05631 in make_unique<v8::platform::DefaultPlatform, int &, v8::platform::IdleTaskSupport &, std::__Cr::unique_ptr<v8::TracingController, std::__Cr::default_delete<v8::TracingController> >, v8::platform::PriorityMode &, 0> gen/third_party/libc++/src/include/__memory/unique_ptr.h:752:30
    #13 0x564cf6f05631 in v8::platform::NewDefaultPlatform(int, v8::platform::IdleTaskSupport, v8::platform::InProcessStackDumping, std::__Cr::unique_ptr<v8::TracingController, std::__Cr::default_delete<v8::TracingController>>, v8::platform::PriorityMode) src/libplatform/default-platform.cc:54:19
    #14 0x564cf695da6f in v8::Shell::Main(int, char**) src/d8/d8.cc:7150:18
    #15 0x7f01ebd68d79 in __libc_start_main csu/../csu/libc-start.c:308:16

Thread T49 (WorkerThread) created by T0 here:
    #0 0x564cf6874921 in pthread_create (/home/user/v8_build/v8/out/debug_fuzz_144/d8+0x2de4921) (BuildId: a0b4f266c3444722)
    #1 0x564cf6f0366b in v8::base::Thread::Start() src/base/platform/platform-posix.cc:1324:14
    #2 0x564cf693c00f in v8::Worker::StartWorkerThread(v8::Isolate*, std::__Cr::shared_ptr<v8::Worker>, v8::base::Thread::Priority) src/d8/d8.cc:5705:16
    #3 0x564cf693b5cf in v8::Shell::WorkerNew(v8::FunctionCallbackInfo<v8::Value> const&) src/d8/d8.cc:3668:10
    #4 0x564cf702de53 in v8::internal::FunctionCallbackArguments::CallOrConstruct(v8::internal::Tagged<v8::internal::FunctionTemplateInfo>, bool) src/api/api-arguments-inl.h:107:3
    #5 0x564cf702afcd in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::HeapObject>, v8::internal::DirectHandle<v8::internal::FunctionTemplateInfo>, v8::internal::DirectHandle<v8::internal::Object>, unsigned long*, int) src/builtins/builtins-api.cc:105:16
    #6 0x564cf7028172 in Builtin_Impl_HandleApiConstruct src/builtins/builtins-api.cc:137:16
    #7 0x564cf7028172 in v8::internal::Builtin_HandleApiConstruct(int, unsigned long*, v8::internal::Isolate*) src/builtins/builtins-api.cc:127:1
    #8 0x564cfddcadbc in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc
    #9 0x564cfd85ce4c in Builtins_InterpreterPushArgsThenFastConstructFunction setup-isolate-deserialize.cc
    #10 0x564cfe6c9e06 in Builtins_ConstructHandler setup-isolate-deserialize.cc
    #11 0x564cfd85c275 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #12 0x564cfd84e966 in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #13 0x564cfd84e6aa in Builtins_JSEntry setup-isolate-deserialize.cc
    #14 0x564cf76688db in Call src/execution/simulator.h:212:12
    #15 0x564cf76688db in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:442:22
    #16 0x564cf766b5cb in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:542:10
    #17 0x564cf6f4222c in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:1980:7
    #18 0x564cf69106f4 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1050:44
    #19 0x564cf694f5d3 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5573:10
    #20 0x564cf695bec2 in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6581:37
    #21 0x564cf695ae25 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6489:18
    #22 0x564cf695f109 in v8::Shell::Main(int, char**) src/d8/d8.cc:7382:18
    #23 0x7f01ebd68d79 in __libc_start_main csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free gen/third_party/libc++/src/include/__atomic/support/c11.h:81:10 in __cxx_atomic_load<const v8::internal::Signature<v8::internal::MachineType> *>
Shadow bytes around the buggy address:
  0x7b21eb2f0e80: fa fa fd fd fa fa fd fa fa fa fd fd fa fa fd fd
  0x7b21eb2f0f00: fa fa fd fd fa fa fd fd fa fa fd fa fa fa fd fa
  0x7b21eb2f0f80: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa
  0x7b21eb2f1000: fa fa 00 fa fa fa fd fd fa fa fd fa fa fa 00 fa
  0x7b21eb2f1080: fa fa 01 fa fa fa 01 fa fa fa 00 00 fa fa fd fa
=>0x7b21eb2f1100: fa fa[fd]fa fa fa fd fa fa fa fd fa fa fa fd fa
  0x7b21eb2f1180: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa
  0x7b21eb2f1200: fa fa fd fa fa fa fd fa fa fa fd fd fa fa fd fd
  0x7b21eb2f1280: fa fa fd fa fa fa 00 00 fa fa fd fd fa fa fd fd
  0x7b21eb2f1300: fa fa fd fa fa fa fd fd fa fa fd fd fa fa fd fa
  0x7b21eb2f1380: fa fa fd fd fa fa fd fa fa fa fd fa fa fa fd fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==4157403==ABORTING 

```
## CREDIT INFORMATION

Reporter credit: Picasso

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 1.2 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2025-12-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5833488997482496.

### li...@chromium.org (2025-12-11)

Reassigning to V8 shepherd @md...@google.com for further triage.

### ch...@google.com (2025-12-12)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-12-12)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### md...@google.com (2025-12-15)

It looks like WASM fastapi owner is ahaas@, but he is OOO for some time, so I am assigning to Michael.

### ml...@chromium.org (2025-12-15)

This feels more general Wasm compilation liveness issue.

+jkummerow to triage further.

### ch...@google.com (2025-12-30)

jkummerow: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### cl...@chromium.org (2026-01-02)

Yeah, this setup cannot work. The `CompilationEnv` must be independent of the live time of the `NativeModule`. This was set up this way so that background compilation does not block a `NativeModule` from being garbage-collected.

The problem was introduced with <https://crrev.com/c/5225044> (February 2024, CCing reviewers).

Luckily `--wasm-fast-api` is still experimental. Adjusting impact.

### jk...@chromium.org (2026-01-07)

In light of Impact-None, there's no immediate urgency, so Andreas can take care of this when he's back.  

Presumably the right fix is to make `NativeModule::fast_api_targets_` be a `std::shared_ptr`, so that the getter can return a `shared_ptr` for the `CompilationEnv` to store. Same for `signatures`. See `NativeModule::coverage_data_` for precedent.

### dx...@google.com (2026-01-21)

Project: v8/v8  

Branch:  main  

Author:  Andreas Haas [ahaas@chromium.org](mailto:ahaas@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7494204>

[wasm] Store fast API targets and signatures as shared\_ptr

---


Expand for full commit details
```
     
    For the compilation of fast API calls from WebAssembly, the fast API 
    targets and signatures are needed. So far, this data is stored in the 
    NativeModule, but it is possible that the NativeModule already dies 
    while compilation is still ongoing. This caused a use-after-free when 
    compilation accessed the fast API targets when the NativeModule was 
    already de-allocated. 
     
    With this CL, the fast API targets and signatures are stored as 
    shared_ptr instead of unique_ptr, so that compilation can keep alive the 
    data while it is still using it. 
     
    Bug: 467705366 
    Change-Id: I7a2cc9a4ecbb0a4329a8e79d1ff7e42ca0bb0c36 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7494204 
    Commit-Queue: Andreas Haas <ahaas@chromium.org> 
    Reviewed-by: Clemens Backes <clemensb@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#104811}

```

---

Files:

- M `src/wasm/compilation-environment-inl.h`
- M `src/wasm/compilation-environment.h`
- M `src/wasm/turboshaft-graph-interface.cc`
- M `src/wasm/wasm-code-manager.cc`
- M `src/wasm/wasm-code-manager.h`

---

Hash: [3bd8fbc7b2cac148dd9df061d7878c278ec29c4b](https://chromiumdash.appspot.com/commit/3bd8fbc7b2cac148dd9df061d7878c278ec29c4b)  

Date: Wed Jan 21 08:33:48 2026


---

### dx...@google.com (2026-01-22)

Project: v8/v8  

Branch:  main  

Author:  Michael Achenbach [machenbach@chromium.org](mailto:machenbach@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7510103>

Revert "[wasm] Store fast API targets and signatures as shared\_ptr"

---


Expand for full commit details
```
     
    This reverts commit 3bd8fbc7b2cac148dd9df061d7878c278ec29c4b. 
     
    Reason for revert: Caused a roll revert: 
    https://crrev.com/c/7507169 
     
    Original change's description: 
    > [wasm] Store fast API targets and signatures as shared_ptr 
    > 
    > For the compilation of fast API calls from WebAssembly, the fast API 
    > targets and signatures are needed. So far, this data is stored in the 
    > NativeModule, but it is possible that the NativeModule already dies 
    > while compilation is still ongoing. This caused a use-after-free when 
    > compilation accessed the fast API targets when the NativeModule was 
    > already de-allocated. 
    > 
    > With this CL, the fast API targets and signatures are stored as 
    > shared_ptr instead of unique_ptr, so that compilation can keep alive the 
    > data while it is still using it. 
    > 
    > Bug: 467705366 
    > Change-Id: I7a2cc9a4ecbb0a4329a8e79d1ff7e42ca0bb0c36 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7494204 
    > Commit-Queue: Andreas Haas <ahaas@chromium.org> 
    > Reviewed-by: Clemens Backes <clemensb@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#104811} 
     
    Bug: 467705366 
    No-Presubmit: true 
    No-Tree-Checks: true 
    No-Try: true 
    Change-Id: Idfcf2ccb35e656f27a4b209542023619442f0db6 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7510103 
    Owners-Override: Michael Achenbach <machenbach@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: Michael Achenbach <machenbach@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#104836}

```

---

Files:

- M `src/wasm/compilation-environment-inl.h`
- M `src/wasm/compilation-environment.h`
- M `src/wasm/turboshaft-graph-interface.cc`
- M `src/wasm/wasm-code-manager.cc`
- M `src/wasm/wasm-code-manager.h`

---

Hash: [4a96c3e90caff623c2e222194bf2687dd48c2a36](https://chromiumdash.appspot.com/commit/4a96c3e90caff623c2e222194bf2687dd48c2a36)  

Date: Thu Jan 22 07:38:28 2026


---

### dx...@google.com (2026-01-23)

Project: v8/v8  

Branch:  main  

Author:  Andreas Haas [ahaas@chromium.org](mailto:ahaas@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7507835>

Reland "[wasm] Store fast API targets and signatures as shared\_ptr"

---


Expand for full commit details
```
     
    This is a reland of commit 3bd8fbc7b2cac148dd9df061d7878c278ec29c4b 
     
    For unknown reasons, the use of std::make_shared caused UBsan issues on 
    a CFI bot. The reland therefore uses the std::shared_ptr constructor 
    instead. 
     
    Original change's description: 
    > [wasm] Store fast API targets and signatures as shared_ptr 
    > 
    > For the compilation of fast API calls from WebAssembly, the fast API 
    > targets and signatures are needed. So far, this data is stored in the 
    > NativeModule, but it is possible that the NativeModule already dies 
    > while compilation is still ongoing. This caused a use-after-free when 
    > compilation accessed the fast API targets when the NativeModule was 
    > already de-allocated. 
    > 
    > With this CL, the fast API targets and signatures are stored as 
    > shared_ptr instead of unique_ptr, so that compilation can keep alive the 
    > data while it is still using it. 
    > 
    > Bug: 467705366 
    > Change-Id: I7a2cc9a4ecbb0a4329a8e79d1ff7e42ca0bb0c36 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7494204 
    > Commit-Queue: Andreas Haas <ahaas@chromium.org> 
    > Reviewed-by: Clemens Backes <clemensb@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#104811} 
     
    Bug: 467705366 
    Change-Id: I0e4cdfe6ebfa3ad2130300f6cd0110f3b6aca186 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7507835 
    Reviewed-by: Clemens Backes <clemensb@chromium.org> 
    Commit-Queue: Andreas Haas <ahaas@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#104874}

```

---

Files:

- M `src/wasm/compilation-environment-inl.h`
- M `src/wasm/compilation-environment.h`
- M `src/wasm/turboshaft-graph-interface.cc`
- M `src/wasm/wasm-code-manager.cc`
- M `src/wasm/wasm-code-manager.h`

---

Hash: [349cfd93e9dd9cb32046c0c3f8d86aad724ef703](https://chromiumdash.appspot.com/commit/349cfd93e9dd9cb32046c0c3f8d86aad724ef703)  

Date: Fri Jan 23 09:56:16 2026


---

### sp...@google.com (2026-02-19)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

Experimental Feature

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### ch...@google.com (2026-05-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Experimental Feature
> 
> 
> Note that the fact that this issue is not being rewarded does not mean
> that the product team won't fix the issue. We have filed a bug with the product
> team and they will review your report and decide if a fix is required. We'll
> let you know if the issue was fixed.
> 
> Regards, \
> Google Security Bot
> 
> *How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/467705366)*
