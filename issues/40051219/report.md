# heap-buffer-overflow in HRTFKernel

| Field | Value |
|-------|-------|
| **Issue ID** | [40051219](https://issues.chromium.org/issues/40051219) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>WebAudio |
| **Platforms** | Linux |
| **Reporter** | cd...@gmail.com |
| **Assignee** | rt...@chromium.org |
| **Created** | 2020-01-13 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36

Steps to reproduce the problem:
1 build latest chrome with asan.(Chromium 81.0.4016.0)
2 ./crhome poc.html

What is the expected behavior?

What went wrong?
=================================================================
==1==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60b000080380 at pc 0x55ff07eb390a bp 0x7f348f809ad0 sp 0x7f348f809ac8
READ of size 16 at 0x60b000080380 thread T13 (HRTF database l)
==1==WARNING: invalid path to external symbolizer!
==1==WARNING: Failed to use and restart external symbolizer!
    #0 0x55ff07eb3909 in radf4_ps ./../../third_party/pffft/src/pffft.c:624:35
    #1 0x55ff07eae03d in rfftf1_ps ./../../third_party/pffft/src/pffft.c:977:9
    #2 0x55ff07ead788 in pffft_transform_internal ./../../third_party/pffft/src/pffft.c:1622:13
    #3 0x55ff130d80d6 in blink::FFTFrame::DoFFT(float const*) ./../../third_party/blink/renderer/platform/audio/pffft/fft_frame_pffft.cc:164:3
    #4 0x55ff130d4d0c in ExtractAverageGroupDelay ./../../third_party/blink/renderer/platform/audio/hrtf_kernel.cc:58:20
    #5 0x55ff130d4d0c in blink::HRTFKernel::HRTFKernel(blink::AudioChannel*, unsigned long, float) ./../../third_party/blink/renderer/platform/audio/hrtf_kernel.cc:74:18
    #6 0x55ff130d0345 in make_unique<blink::HRTFKernel, blink::AudioChannel *&, const unsigned long &, float &> ./../../buildtools/third_party/libc++/trunk/include/memory:3043:32
    #7 0x55ff130d0345 in blink::HRTFElevation::CalculateKernelsForAzimuthElevation(int, int, float, int, std::__1::unique_ptr<blink::HRTFKernel, std::__1::default_delete<blink::HRTFKernel> >&, std::__1::unique_ptr<blink::HRTFKernel, std::__1::default_delete<blink::HRTFKernel> >&) ./../../third_party/blink/renderer/platform/audio/hrtf_elevation.cc:165:14
    #8 0x55ff130d12f8 in blink::HRTFElevation::CreateForSubject(int, int, float) ./../../third_party/blink/renderer/platform/audio/hrtf_elevation.cc:226:20
    #9 0x55ff130cec2c in blink::HRTFDatabase::HRTFDatabase(float) ./../../third_party/blink/renderer/platform/audio/hrtf_database.cc:55:9
    #10 0x55ff130cc95b in make_unique<blink::HRTFDatabase, float &> ./../../buildtools/third_party/libc++/trunk/include/memory:3043:32
    #11 0x55ff130cc95b in blink::HRTFDatabaseLoader::LoadTask() ./../../third_party/blink/renderer/platform/audio/hrtf_database_loader.cc:83:20
    #12 0x55ff02c31b5e in Run ./../../base/callback.h:98:12
    #13 0x55ff02c31b5e in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:142:33
    #14 0x55ff02c6b659 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*, bool*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:365:23
    #15 0x55ff02c6afc2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:219:7
    #16 0x55ff02b6ddc0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39:55
    #17 0x55ff02c6d4a4 in Run ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:463:12
    #18 0x55ff02c6d4a4 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #19 0x55ff02bdf74d in base::RunLoop::Run() ./../../base/run_loop.cc:155:14
    #20 0x55ff00e58889 in blink::scheduler::WorkerThread::SimpleThreadImpl::Run() ./../../third_party/blink/renderer/platform/scheduler/worker/worker_thread.cc:169:14
    #21 0x55ff02d9c05d in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:81:13
    #22 0x7f34b2c146da in start_thread ??:0:0

0x60b000080380 is located 12 bytes to the right of 100-byte region [0x60b000080310,0x60b000080374)
allocated by thread T13 (HRTF database l) here:
    #0 0x55fef8b28642 in calloc /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x55ff07f3e72e in PartitionAllocGenericFlags ./../../base/allocator/partition_allocator/partition_alloc.h:402:30
    #2 0x55ff07f3e72e in AllocFlags ./../../base/allocator/partition_allocator/partition_alloc.h:443:10
    #3 0x55ff07f3e72e in WTF::Partitions::FastZeroedMalloc(unsigned long, char const*) ./../../third_party/blink/renderer/platform/wtf/allocator/partitions.cc:236:33
    #4 0x55ff00e6f81d in blink::AudioArray<float>::Allocate(unsigned long) ./../../third_party/blink/renderer/platform/audio/audio_array.h:83:39
    #5 0x55ff0ce1c8e8 in AudioArray ./../../third_party/blink/renderer/platform/audio/audio_array.h:50:5
    #6 0x55ff0ce1c8e8 in make_unique<blink::AudioArray<float>, unsigned long &> ./../../buildtools/third_party/libc++/trunk/include/memory:3043:32
    #7 0x55ff0ce1c8e8 in AudioChannel ./../../third_party/blink/renderer/platform/audio/audio_channel.h:58:19
    #8 0x55ff0ce1c8e8 in make_unique<blink::AudioChannel, unsigned int &> ./../../buildtools/third_party/libc++/trunk/include/memory:3043:32
    #9 0x55ff0ce1c8e8 in blink::AudioBus::AudioBus(unsigned int, unsigned int, bool) ./../../third_party/blink/renderer/platform/audio/audio_bus.cc:69:20
    #10 0x55ff0ce26e72 in Create ./../../third_party/blink/renderer/platform/audio/audio_bus.cc:60:29
    #11 0x55ff0ce26e72 in blink::AudioBus::CreateBySampleRateConverting(blink::AudioBus const*, bool, double) ./../../third_party/blink/renderer/platform/audio/audio_bus.cc:624:7
    #12 0x55ff130d001e in blink::HRTFElevation::CalculateKernelsForAzimuthElevation(int, int, float, int, std::__1::unique_ptr<blink::HRTFKernel, std::__1::default_delete<blink::HRTFKernel> >&, std::__1::unique_ptr<blink::HRTFKernel, std::__1::default_delete<blink::HRTFKernel> >&) ./../../third_party/blink/renderer/platform/audio/hrtf_elevation.cc:155:36
    #13 0x55ff130d12f8 in blink::HRTFElevation::CreateForSubject(int, int, float) ./../../third_party/blink/renderer/platform/audio/hrtf_elevation.cc:226:20
    #14 0x55ff130cec2c in blink::HRTFDatabase::HRTFDatabase(float) ./../../third_party/blink/renderer/platform/audio/hrtf_database.cc:55:9
    #15 0x55ff130cc95b in make_unique<blink::HRTFDatabase, float &> ./../../buildtools/third_party/libc++/trunk/include/memory:3043:32
    #16 0x55ff130cc95b in blink::HRTFDatabaseLoader::LoadTask() ./../../third_party/blink/renderer/platform/audio/hrtf_database_loader.cc:83:20
    #17 0x55ff02c31b5e in Run ./../../base/callback.h:98:12
    #18 0x55ff02c31b5e in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:142:33
    #19 0x55ff02c6b659 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*, bool*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:365:23
    #20 0x55ff02c6afc2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:219:7
    #21 0x55ff02b6ddc0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39:55
    #22 0x55ff02c6d4a4 in Run ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:463:12
    #23 0x55ff02c6d4a4 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #24 0x55ff02bdf74d in base::RunLoop::Run() ./../../base/run_loop.cc:155:14
    #25 0x55ff00e58889 in blink::scheduler::WorkerThread::SimpleThreadImpl::Run() ./../../third_party/blink/renderer/platform/scheduler/worker/worker_thread.cc:169:14
    #26 0x55ff02d9c05d in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:81:13
    #27 0x7f34b2c146da in start_thread ??:0:0

Thread T13 (HRTF database l) created by T0 (chrome) here:
    #0 0x55fef8b12d5a in pthread_create /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:214:3
    #1 0x55ff02d9b1da in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, base::PlatformThreadHandle*, base::ThreadPriority) ./../../base/threading/platform_thread_posix.cc:120:13
    #2 0x55ff02cb89cf in base::SimpleThread::StartAsync() ./../../base/threading/simple_thread.cc:51:13
    #3 0x55ff00e56da1 in blink::scheduler::WorkerThread::Init() ./../../third_party/blink/renderer/platform/scheduler/worker/worker_thread.cc:61:12
    #4 0x55ff00dba366 in blink::Thread::CreateThread(blink::ThreadCreationParams const&) ./../../third_party/blink/renderer/platform/scheduler/common/thread.cc:82:11
    #5 0x55ff0cbcc2c3 in blink::Platform::CreateThread(blink::ThreadCreationParams const&) ./../../third_party/blink/renderer/platform/exported/platform.cc:302:10
    #6 0x55ff130cbed1 in blink::HRTFDatabaseLoader::LoadAsynchronously() ./../../third_party/blink/renderer/platform/audio/hrtf_database_loader.cc:97:34
    #7 0x55ff130cbb59 in blink::HRTFDatabaseLoader::CreateAndLoadAsynchronouslyIfNecessary(float) ./../../third_party/blink/renderer/platform/audio/hrtf_database_loader.cc:60:11
    #8 0x55ff130c5f7d in blink::AudioListener::CreateAndLoadHRTFDatabaseLoader(float) ./../../third_party/blink/renderer/modules/webaudio/audio_listener.cc:283:9
    #9 0x55ff1302acf7 in blink::PannerHandler::SetPanningModel(unsigned int) ./../../third_party/blink/renderer/modules/webaudio/panner_node.cc:389:17
    #10 0x55ff13024e9b in blink::PannerHandler::SetPanningModel(WTF::String const&) ./../../third_party/blink/renderer/modules/webaudio/panner_node.cc:0:12
    #11 0x55ff1302d05b in setPanningModel ./../../third_party/blink/renderer/modules/webaudio/panner_node.cc:840:22
    #12 0x55ff1302d05b in blink::PannerNode::Create(blink::BaseAudioContext*, blink::PannerOptions const*, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/webaudio/panner_node.cc:810:9
    #13 0x55ff130a2464 in Constructor ./gen/third_party/blink/renderer/bindings/modules/v8/v8_panner_node.cc:540:22
    #14 0x55ff130a2464 in blink::panner_node_v8_internal::ConstructorCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_panner_node.cc:566:3
    #15 0x55fefeaf1daf in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:158:3
    #16 0x55fefeaeec14 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:111:36
    #17 0x55fefeaed67d in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:137:5
    #18 0x55ff00b0d457 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit ??:0:0
    #19 0x55ff00a93f44 in Builtins_JSBuiltinsConstructStub ??:0:0
    #20 0x55ff00b8dcc6 in Builtins_ConstructHandler ??:0:0
    #21 0x55ff00a982ea in Builtins_InterpreterEntryTrampoline ??:0:0
    #22 0x55ff00a95cd9 in Builtins_JSEntryTrampoline ??:0:0
    #23 0x55ff00a95ab7 in Builtins_JSEntry ??:0:0
    #24 0x55fefed70279 in Call ./../../v8/src/execution/simulator.h:142:12
    #25 0x55fefed70279 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:271:33
    #26 0x55fefed6f57e in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) ./../../v8/src/execution/execution.cc:365:10
    #27 0x55fefe991eb9 in v8::Script::Run(v8::Local<v8::Context>) ./../../v8/src/api/api.cc:2158:7
    #28 0x55ff0cf9ad9f in blink::V8ScriptRunner::RunCompiledScript(v8::Isolate*, v8::Local<v8::Script>, blink::ExecutionContext*) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:341:22
    #29 0x55ff0e5be8ee in blink::ScriptController::ExecuteScriptAndReturnValue(v8::Local<v8::Context>, blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&) ./../../third_party/blink/renderer/bindings/core/v8/script_controller.cc:132:20
    #30 0x55ff0e5c153a in blink::ScriptController::EvaluateScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&, blink::ScriptController::ExecuteScriptPolicy) ./../../third_party/blink/renderer/bindings/core/v8/script_controller.cc:359:33
    #31 0x55ff0e5c1f6e in blink::ScriptController::ExecuteScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&) ./../../third_party/blink/renderer/bindings/core/v8/script_controller.cc:324:3
    #32 0x55ff1085ede2 in blink::PendingScript::ExecuteScriptBlockInternal(blink::Script*, blink::ScriptElementBase*, bool, bool, bool, base::TimeTicks, bool) ./../../third_party/blink/renderer/core/script/pending_script.cc:267:13
    #33 0x55ff1085e874 in blink::PendingScript::ExecuteScriptBlock(blink::KURL const&) ./../../third_party/blink/renderer/core/script/pending_script.cc:175:3
    #34 0x55ff10863ba3 in blink::ScriptLoader::PrepareScript(WTF::TextPosition const&, blink::ScriptLoader::LegacyTypeSupport) ./../../third_party/blink/renderer/core/script/script_loader.cc:906:9
    #35 0x55ff107fea87 in blink::HTMLParserScriptRunner::ProcessScriptElementInternal(blink::Element*, WTF::TextPosition const&) ./../../third_party/blink/renderer/core/script/html_parser_script_runner.cc:610:20
    #36 0x55ff107fe5f8 in blink::HTMLParserScriptRunner::ProcessScriptElement(blink::Element*, WTF::TextPosition const&) ./../../third_party/blink/renderer/core/script/html_parser_script_runner.cc:333:3
    #37 0x55ff0f4cf9cc in RunScriptsForPausedTreeBuilder ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:299:21
    #38 0x55ff0f4cf9cc in blink::HTMLDocumentParser::ProcessTokenizedChunkFromBackgroundParser(std::__1::unique_ptr<blink::HTMLDocumentParser::TokenizedChunk, std::__1::default_delete<blink::HTMLDocumentParser::TokenizedChunk> >) ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:535:9
    #39 0x55ff0f4cb739 in blink::HTMLDocumentParser::PumpPendingSpeculations() ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:593:9
    #40 0x55ff00db4fb3 in Run ./../../base/callback.h:98:12
    #41 0x55ff00db4fb3 in blink::TaskHandle::Runner::Run(blink::TaskHandle const&) ./../../third_party/blink/renderer/platform/scheduler/common/post_cancellable_task.cc:47:21
    #42 0x55ff02c31b5e in Run ./../../base/callback.h:98:12
    #43 0x55ff02c31b5e in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:142:33
    #44 0x55ff02c6b659 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*, bool*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:365:23
    #45 0x55ff02c6afc2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:219:7
    #46 0x55ff02b6ddc0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39:55
    #47 0x55ff02c6d4a4 in Run ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:463:12
    #48 0x55ff02c6d4a4 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #49 0x55ff02bdf74d in base::RunLoop::Run() ./../../base/run_loop.cc:155:14
    #50 0x55ff140d9b0b in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:213:16
    #51 0x55ff01b7e32f in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:501:14
    #52 0x55ff01b81796 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:880:10
    #53 0x55ff01d2bc67 in service_manager::Main(service_manager::MainParams const&) ./../../services/service_manager/embedder/main.cc:423:29
    #54 0x55ff01b7c846 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:19:10
    #55 0x55fef8b5503f in ChromeMain ./../../chrome/app/chrome_main.cc:121:12
    #56 0x7f34ab739b96 in __libc_start_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310:0

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/cowboy/chromium/src/out/chrome_asan_shared/chrome+0x180ef909)
Shadow bytes around the buggy address:
  0x0c1680008020: 00 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa
  0x0c1680008030: fa fa fa fa fa fa 00 00 00 00 00 00 00 00 00 00
  0x0c1680008040: 00 00 00 fa fa fa fa fa fa fa fa fa fd fd fd fd
  0x0c1680008050: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa
  0x0c1680008060: fa fa 00 00 00 00 00 00 00 00 00 00 00 00 04 fa
=>0x0c1680008070:[fa]fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x0c1680008080: 00 00 00 00 04 fa fa fa fa fa fa fa fa fa fa fa
  0x0c1680008090: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c16800080a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c16800080b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c16800080c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
  Shadow gap:              cc
==1==ABORTING

Did this work before? N/A 

Chrome version: Chromium 81.0.4016.0   Channel: dev
OS Version: Ubuntu 18.04
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- [asan.log](attachments/asan.log) (text/plain, 18.4 KB)

## Timeline

### cl...@chromium.org (2020-01-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6595839713673216.

### cl...@chromium.org (2020-01-14)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/f832371e1fa25030c962cc30fc7a33058f95ed56 (Follow style guide on use of DCHECK).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2020-01-14)

Detailed Report: https://clusterfuzz.com/testcase?key=6595839713673216

Fuzzer: 
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 16
Crash Address: 0x6100000599f0
Crash State:
  radf4_ps
  rfftf1_ps
  pffft_transform_internal
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=690144:690145

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6595839713673216

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/6595839713673216 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### sh...@chromium.org (2020-01-14)

Setting milestone and target because of Security_Impact=Head and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2020-01-14)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2020-01-14)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rt...@chromium.org (2020-01-14)

Same as https://crbug.com/chromium/1032000 ?

[Monorail components: Blink>WebAudio]

### rt...@chromium.org (2020-01-16)

It is the same issue.  But with a more reliable test case?

### rt...@chromium.org (2020-01-16)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6e00639d878b4e71689798aba8e0e216bd59e42c

commit 6e00639d878b4e71689798aba8e0e216bd59e42c
Author: Raymond Toy <rtoy@chromium.org>
Date: Fri Jan 17 13:50:58 2020

Zero-pad HRTF response if needed

The HRTF response size can some times be smaller than the FFT size.
This can happen if the FFT size has a lower limit, such as for PFFFT
which clamps the size to the lower bound.  To account for this, create
a new HRTF response that is zero-padded to the FFT size.

Manually tested against repro cases from the bugs; ASAN issue no
longer reproduces.

Bug: 1032000, 1041411
Change-Id: Ic2136a92a6e1bf4f2f78f434b065c21dc1b72b5d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2003571
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Cr-Commit-Position: refs/heads/master@{#732837}

[modify] https://crrev.com/6e00639d878b4e71689798aba8e0e216bd59e42c/third_party/blink/renderer/platform/audio/hrtf_elevation.cc


### cl...@chromium.org (2020-01-17)

Detailed Report: https://clusterfuzz.com/testcase?key=6595839713673216

Fuzzer: 
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 16
Crash Address: 0x6100000599f0
Crash State:
  radf4_ps
  rfftf1_ps
  pffft_transform_internal
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=690144:690145

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6595839713673216

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/6595839713673216 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2020-01-17)

ClusterFuzz testcase 6595839713673216 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=732833:732837

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2020-01-18)

[Empty comment from Monorail migration]

### rt...@chromium.org (2020-01-18)

[Empty comment from Monorail migration]

### rt...@chromium.org (2020-01-18)

[Empty comment from Monorail migration]

### rt...@chromium.org (2020-01-18)

[Empty comment from Monorail migration]

### rt...@chromium.org (2020-01-18)

Requesting merge to 80.

### sh...@chromium.org (2020-01-18)

This bug requires manual review: M80's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), Kariahda@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2020-01-19)

[Empty comment from Monorail migration]

### sr...@google.com (2020-01-20)

merge approved for M80, branch:3987 pls merge your changes asap

### sr...@google.com (2020-01-20)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-21)

[Empty comment from Monorail migration]

### sr...@google.com (2020-01-21)

Pls help complete the merges before 2pm PST today so they can be included in tomrorow beta release. Next week is stable RC, so pls help get the changes in asap so we can get beta coverage and identify any unforeseen issues.

### rt...@chromium.org (2020-01-21)

It's in the CQ right now:  https://chromium-review.googlesource.com/c/chromium/src/+/2011132

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b6dcb22b638605068d8c74e9821827e7948d5fe1

commit b6dcb22b638605068d8c74e9821827e7948d5fe1
Author: Raymond Toy <rtoy@chromium.org>
Date: Tue Jan 21 19:14:13 2020

Zero-pad HRTF response if needed

The HRTF response size can some times be smaller than the FFT size.
This can happen if the FFT size has a lower limit, such as for PFFFT
which clamps the size to the lower bound.  To account for this, create
a new HRTF response that is zero-padded to the FFT size.

Manually tested against repro cases from the bugs; ASAN issue no
longer reproduces.

(cherry picked from commit 6e00639d878b4e71689798aba8e0e216bd59e42c)

Bug: 1032000, 1041411
Change-Id: Ic2136a92a6e1bf4f2f78f434b065c21dc1b72b5d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2003571
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#732837}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2010172
Reviewed-by: Raymond Toy <rtoy@chromium.org>
Cr-Commit-Position: refs/branch-heads/3987@{#642}
Cr-Branched-From: c4e8da9871cc266be74481e212f3a5252972509d-refs/heads/master@{#722274}

[modify] https://crrev.com/b6dcb22b638605068d8c74e9821827e7948d5fe1/third_party/blink/renderer/platform/audio/hrtf_elevation.cc


### rt...@chromium.org (2020-01-23)

Requesting merge to m79, just in case we need it.

### na...@google.com (2020-01-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-01-23)

Congrats the Panel decided to reward $500 for this report!

### na...@google.com (2020-01-23)

[Empty comment from Monorail migration]

### go...@chromium.org (2020-01-29)

Rejecting merge to M79 as we're not planning any further M79 release.

### [Deleted User] (2020-04-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-05-15)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-16)

The older reward-topanel https://crbug.com/chromium/1032000 has been merged into this one. Please manually review this issue to see if the duplicate is potentially eligible for a reward.



### [Deleted User] (2020-05-16)

The older reward-topanel https://crbug.com/chromium/1003908 has been merged into this one. Please manually review this issue to see if the duplicate is potentially eligible for a reward.



### na...@google.com (2020-05-21)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1041411?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1003908, crbug.com/chromium/1032000]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051219)*
