# heap-use-after-free in Cancel::wasm-engine.cc

| Field | Value |
|-------|-------|
| **Issue ID** | [40095298](https://issues.chromium.org/issues/40095298) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | cl...@chromium.org |
| **Created** | 2019-06-05 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36

Steps to reproduce the problem:
1. Build asan 77.0.3815.0  version of chrome.
2. Put ws.js and bit-crusher.js into the same dir with poc.html and use nodejs to setup a webserver: node ws.js
3. Run chrome http://127.0.0.1:8605/poc.html

What is the expected behavior?

What went wrong?
==100704==ERROR: AddressSanitizer: heap-use-after-free on address 0x60200015e438 at pc 0x5577dedc078c bp 0x7f365734f1a0 sp 0x7f365734f198
WRITE of size 8 at 0x60200015e438 thread T23 (AudioWorklet th)
    #0 0x5577dedc078b in Cancel ./../../v8/src/wasm/wasm-engine.cc:110:28
    #1 0x5577dedc078b in v8::internal::wasm::WasmEngine::RemoveIsolateFromCurrentGC(v8::internal::Isolate*) ./../../v8/src/wasm/wasm-engine.cc:869:0
    #2 0x5577dedbfc5b in v8::internal::wasm::WasmEngine::RemoveIsolate(v8::internal::Isolate*) ./../../v8/src/wasm/wasm-engine.cc:592:9
    #3 0x5577ddfd185b in v8::internal::Isolate::Deinit() ./../../v8/src/execution/isolate.cc:3006:19
    #4 0x5577ddfd1208 in v8::internal::Isolate::Delete(v8::internal::Isolate*) ./../../v8/src/execution/isolate.cc:2838:12
    #5 0x5577ec20887a in gin::IsolateHolder::~IsolateHolder() ./../../gin/isolate_holder.cc:94:13
    #6 0x5577ebe1fd90 in blink::V8PerIsolateData::Destroy(v8::Isolate*) ./../../third_party/blink/renderer/platform/bindings/v8_per_isolate_data.cc:205:3
    #7 0x5577ef4a0911 in blink::WorkerBackingThread::ShutdownOnBackingThread() ./../../third_party/blink/renderer/core/workers/worker_backing_thread.cc:108:3
    #8 0x5577f14a4900 in blink::WorkletThreadHolder<blink::AudioWorkletThread>::ShutdownOnWorkletThread(base::WaitableEvent*) ./../../third_party/blink/renderer/core/workers/worklet_thread_holder.h:85:14
    #9 0x5577e1c54d8e in Run ./../../base/callback.h:97:12
    #10 0x5577e1c54d8e in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:142:0
    #11 0x5577e1c8b52f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*, bool*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:368:23
    #12 0x5577e1c8aae2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:219:7
    #13 0x5577e1b99e30 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39:55
    #14 0x5577e1c8d614 in Run ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:466:12
    #15 0x5577e1c8d614 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #16 0x5577e1c07b08 in base::RunLoop::RunWithTimeout(base::TimeDelta) ./../../base/run_loop.cc:161:14
    #17 0x5577dfd409f9 in blink::scheduler::WorkerThread::SimpleThreadImpl::Run() ./../../third_party/blink/renderer/platform/scheduler/worker/worker_thread.cc:127:14
    #18 0x5577e1dba39d in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:81:13
    #19 0x7f367881e6da in start_thread ??:0:0

0x60200015e438 is located 8 bytes inside of 16-byte region [0x60200015e430,0x60200015e440)
freed by thread T2 (ThreadPoolForeg) here:
    #0 0x5577d81a82dd in operator delete(void*) _asan_rtl_:3
    #1 0x5577ec20d665 in operator() ./../../buildtools/third_party/libc++/trunk/include/memory:2338:5
    #2 0x5577ec20d665 in reset ./../../buildtools/third_party/libc++/trunk/include/memory:2651:0
    #3 0x5577ec20d665 in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/memory:2605:0
    #4 0x5577ec20d665 in ~__tuple_leaf ./../../buildtools/third_party/libc++/trunk/include/tuple:170:0
    #5 0x5577ec20d665 in ~tuple ./../../buildtools/third_party/libc++/trunk/include/tuple:469:0
    #6 0x5577ec20d665 in ~BindState ./../../base/bind_internal.h:854:0
    #7 0x5577ec20d665 in base::internal::BindState<void (v8::Task::*)(), std::__1::unique_ptr<v8::Task, std::__1::default_delete<v8::Task> > >::Destroy(base::internal::BindStateBase const*) ./../../base/bind_internal.h:857:0
    #8 0x5577e1c73691 in base::sequence_manager::internal::TaskQueueImpl::TaskRunner::PostDelayedTask(base::Location const&, base::OnceCallback<void ()>, base::TimeDelta) ./../../base/task/sequence_manager/task_queue_impl.cc:78:3
    #9 0x5577e1cc9898 in base::TaskRunner::PostTask(base::Location const&, base::OnceCallback<void ()>) ./../../base/task_runner.cc:78:10
    #10 0x5577ec20ccb1 in gin::V8ForegroundTaskRunner::PostTask(std::__1::unique_ptr<v8::Task, std::__1::default_delete<v8::Task> >) ./../../gin/v8_foreground_task_runner.cc:23:17
    #11 0x5577dedc5b38 in v8::internal::wasm::WasmEngine::TriggerGC(signed char) ./../../v8/src/wasm/wasm-engine.cc:850:53
    #12 0x5577dedc4cb5 in v8::internal::wasm::WasmEngine::AddPotentiallyDeadCode(v8::internal::wasm::WasmCode*) ./../../v8/src/wasm/wasm-engine.cc:793:9
    #13 0x5577ded9f26b in v8::internal::wasm::WasmCode::DecRefOnPotentiallyDeadCode() ./../../v8/src/wasm/wasm-code-manager.cc:376:33
    #14 0x5577ded9f4de in DecRef ./../../v8/src/wasm/wasm-code-manager.h:158:47
    #15 0x5577ded9f4de in v8::internal::wasm::WasmCode::DecrementRefCount(v8::internal::Vector<v8::internal::wasm::WasmCode* const>) ./../../v8/src/wasm/wasm-code-manager.cc:394:0
    #16 0x5577dedac0e7 in v8::internal::wasm::WasmCodeRefScope::~WasmCodeRefScope() ./../../v8/src/wasm/wasm-code-manager.cc:1535:3
    #17 0x5577ded45ae4 in v8::internal::wasm::(anonymous namespace)::ExecuteCompilationUnits(std::__1::shared_ptr<v8::internal::wasm::(anonymous namespace)::BackgroundCompileToken> const&, v8::internal::Counters*, int, v8::internal::wasm::(anonymous namespace)::CompileBaselineOnly)::$_2::operator()(v8::internal::wasm::(anonymous namespace)::BackgroundCompileScope*) const ./../../v8/src/wasm/module-compiler.cc:975:3
    #18 0x5577ded41b22 in v8::internal::wasm::(anonymous namespace)::ExecuteCompilationUnits(std::__1::shared_ptr<v8::internal::wasm::(anonymous namespace)::BackgroundCompileToken> const&, v8::internal::Counters*, int, v8::internal::wasm::(anonymous namespace)::CompileBaselineOnly) ./../../v8/src/wasm/module-compiler.cc:1005:9
    #19 0x5577e1c54d8e in Run ./../../base/callback.h:97:12
    #20 0x5577e1c54d8e in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:142:0
    #21 0x5577e1ca6d18 in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task*) ./../../base/task/thread_pool/task_tracker.cc:747:19
    #22 0x5577e1ca58b5 in RunTaskWithShutdownBehavior ./../../base/task/thread_pool/task_tracker.cc:765:7
    #23 0x5577e1ca58b5 in base::internal::TaskTracker::RunOrSkipTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&, bool) ./../../base/task/thread_pool/task_tracker.cc:593:0
    #24 0x5577e1db8a8f in base::internal::TaskTrackerPosix::RunOrSkipTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&, bool) ./../../base/task/thread_pool/task_tracker_posix.cc:24:16
    #25 0x5577e1ca4849 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) ./../../base/task/thread_pool/task_tracker.cc:455:5
    #26 0x5577e1cc8279 in base::internal::WorkerThread::RunWorker() ./../../base/task/thread_pool/worker_thread.cc:320:34
    #27 0x5577e1cc7800 in base::internal::WorkerThread::RunPooledWorker() ./../../base/task/thread_pool/worker_thread.cc:222:3
    #28 0x5577e1dba39d in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:81:13
    #29 0x7f367881e6da in start_thread ??:0:0

previously allocated by thread T2 (ThreadPoolForeg) here:
    #0 0x5577d81a7a7d in operator new(unsigned long) _asan_rtl_:3
    #1 0x5577dedc59fc in make_unique<v8::internal::wasm::(anonymous namespace)::WasmGCForegroundTask, v8::internal::Isolate *&> ./../../v8/src/base/template-utils.h:56:29
    #2 0x5577dedc59fc in v8::internal::wasm::WasmEngine::TriggerGC(signed char) ./../../v8/src/wasm/wasm-engine.cc:847:0
    #3 0x5577dedc4cb5 in v8::internal::wasm::WasmEngine::AddPotentiallyDeadCode(v8::internal::wasm::WasmCode*) ./../../v8/src/wasm/wasm-engine.cc:793:9
    #4 0x5577ded9f26b in v8::internal::wasm::WasmCode::DecRefOnPotentiallyDeadCode() ./../../v8/src/wasm/wasm-code-manager.cc:376:33
    #5 0x5577ded9f4de in DecRef ./../../v8/src/wasm/wasm-code-manager.h:158:47
    #6 0x5577ded9f4de in v8::internal::wasm::WasmCode::DecrementRefCount(v8::internal::Vector<v8::internal::wasm::WasmCode* const>) ./../../v8/src/wasm/wasm-code-manager.cc:394:0
    #7 0x5577dedac0e7 in v8::internal::wasm::WasmCodeRefScope::~WasmCodeRefScope() ./../../v8/src/wasm/wasm-code-manager.cc:1535:3
    #8 0x5577ded45ae4 in v8::internal::wasm::(anonymous namespace)::ExecuteCompilationUnits(std::__1::shared_ptr<v8::internal::wasm::(anonymous namespace)::BackgroundCompileToken> const&, v8::internal::Counters*, int, v8::internal::wasm::(anonymous namespace)::CompileBaselineOnly)::$_2::operator()(v8::internal::wasm::(anonymous namespace)::BackgroundCompileScope*) const ./../../v8/src/wasm/module-compiler.cc:975:3
    #9 0x5577ded41b22 in v8::internal::wasm::(anonymous namespace)::ExecuteCompilationUnits(std::__1::shared_ptr<v8::internal::wasm::(anonymous namespace)::BackgroundCompileToken> const&, v8::internal::Counters*, int, v8::internal::wasm::(anonymous namespace)::CompileBaselineOnly) ./../../v8/src/wasm/module-compiler.cc:1005:9
    #10 0x5577e1c54d8e in Run ./../../base/callback.h:97:12
    #11 0x5577e1c54d8e in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:142:0
    #12 0x5577e1ca6d18 in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task*) ./../../base/task/thread_pool/task_tracker.cc:747:19
    #13 0x5577e1ca58b5 in RunTaskWithShutdownBehavior ./../../base/task/thread_pool/task_tracker.cc:765:7
    #14 0x5577e1ca58b5 in base::internal::TaskTracker::RunOrSkipTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&, bool) ./../../base/task/thread_pool/task_tracker.cc:593:0
    #15 0x5577e1db8a8f in base::internal::TaskTrackerPosix::RunOrSkipTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&, bool) ./../../base/task/thread_pool/task_tracker_posix.cc:24:16
    #16 0x5577e1ca4849 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) ./../../base/task/thread_pool/task_tracker.cc:455:5
    #17 0x5577e1cc8279 in base::internal::WorkerThread::RunWorker() ./../../base/task/thread_pool/worker_thread.cc:320:34
    #18 0x5577e1cc7800 in base::internal::WorkerThread::RunPooledWorker() ./../../base/task/thread_pool/worker_thread.cc:222:3
    #19 0x5577e1dba39d in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:81:13
    #20 0x7f367881e6da in start_thread ??:0:0

Thread T23 (AudioWorklet th) created by T0 (chrome) here:
    #0 0x5577d8169d7a in pthread_create _asan_rtl_:3
    #1 0x5577e1db956a in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, base::PlatformThreadHandle*, base::ThreadPriority) ./../../base/threading/platform_thread_posix.cc:120:13
    #2 0x5577e1ce3a20 in base::SimpleThread::StartAsync() ./../../base/threading/simple_thread.cc:51:13
    #3 0x5577dfd3f8c1 in blink::scheduler::WorkerThread::Init() ./../../third_party/blink/renderer/platform/scheduler/worker/worker_thread.cc:57:12
    #4 0x5577dfcb6f6d in CreateThread ./../../third_party/blink/renderer/platform/scheduler/common/thread.cc:91:11
    #5 0x5577dfcb6f6d in blink::Thread::CreateWebAudioThread() ./../../third_party/blink/renderer/platform/scheduler/common/thread.cc:108:0
    #6 0x5577ef4a1dcd in blink::WebThreadSupportingGC::WebThreadSupportingGC(blink::ThreadCreationParams const&) ./../../third_party/blink/renderer/platform/web_thread_supporting_gc.cc:22:15
    #7 0x5577ef49fb22 in make_unique<blink::WebThreadSupportingGC, const blink::ThreadCreationParams &> ./../../buildtools/third_party/libc++/trunk/include/memory:3131:32
    #8 0x5577ef49fb22 in blink::WorkerBackingThread::WorkerBackingThread(blink::ThreadCreationParams const&) ./../../third_party/blink/renderer/core/workers/worker_backing_thread.cc:60:0
    #9 0x5577f14a3cc7 in make_unique<blink::WorkerBackingThread, const blink::ThreadCreationParams &> ./../../buildtools/third_party/libc++/trunk/include/memory:3131:32
    #10 0x5577f14a3cc7 in blink::WorkletThreadHolder<blink::AudioWorkletThread>::EnsureInstance(blink::ThreadCreationParams const&) ./../../third_party/blink/renderer/core/workers/worklet_thread_holder.h:35:0
    #11 0x5577f14a4a88 in EnsureSharedBackingThread ./../../third_party/blink/renderer/modules/webaudio/audio_worklet_thread.cc:56:3
    #12 0x5577f14a4a88 in AudioWorkletThread ./../../third_party/blink/renderer/modules/webaudio/audio_worklet_thread.cc:39:0
    #13 0x5577f14a4a88 in blink::AudioWorkletThread::Create(blink::WorkerReportingProxy&) ./../../third_party/blink/renderer/modules/webaudio/audio_worklet_thread.cc:31:0
    #14 0x5577f14a0245 in blink::AudioWorkletMessagingProxy::CreateWorkerThread() ./../../third_party/blink/renderer/modules/webaudio/audio_worklet_messaging_proxy.cc:95:10
    #15 0x5577ef4953a7 in blink::ThreadedMessagingProxyBase::InitializeWorkerThread(std::__1::unique_ptr<blink::GlobalScopeCreationParams, std::__1::default_delete<blink::GlobalScopeCreationParams> >, base::Optional<blink::WorkerBackingThreadStartupData> const&) ./../../third_party/blink/renderer/core/workers/threaded_messaging_proxy_base.cc:72:20
    #16 0x5577f14eee97 in blink::ThreadedWorkletMessagingProxy::Initialize(blink::WorkerClients*, blink::WorkletModuleResponsesMap*, base::Optional<blink::WorkerBackingThreadStartupData> const&) ./../../third_party/blink/renderer/core/workers/threaded_worklet_messaging_proxy.cc:81:3
    #17 0x5577f149d571 in blink::AudioWorklet::CreateGlobalScope() ./../../third_party/blink/renderer/modules/webaudio/audio_worklet.cc:81:10
    #18 0x5577ef4dbd8b in blink::Worklet::FetchAndInvokeScript(blink::KURL const&, WTF::String const&, blink::WorkletPendingTasks*) ./../../third_party/blink/renderer/core/workers/worklet.cc:161:24
    #19 0x5577e1c54d8e in Run ./../../base/callback.h:97:12
    #20 0x5577e1c54d8e in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:142:0
    #21 0x5577e1c8b52f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*, bool*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:368:23
    #22 0x5577e1c8aae2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:219:7
    #23 0x5577e1b99e30 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39:55
    #24 0x5577e1c8d614 in Run ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:466:12
    #25 0x5577e1c8d614 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #26 0x5577e1c07b08 in base::RunLoop::RunWithTimeout(base::TimeDelta) ./../../base/run_loop.cc:161:14
    #27 0x5577f23f87a9 in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:208:16
    #28 0x5577e0be3176 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:873:10
    #29 0x5577e0d866c1 in service_manager::Main(service_manager::MainParams const&) ./../../services/service_manager/embedder/main.cc:422:29
    #30 0x5577e0bddfdc in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:19:10
    #31 0x5577d81aac23 in ChromeMain ./../../chrome/app/chrome_main.cc:103:12
    #32 0x7f3671556b96 in __libc_start_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310:0

Thread T2 (ThreadPoolForeg) created by T0 (chrome) here:
    #0 0x5577d8169d7a in pthread_create _asan_rtl_:3
    #1 0x5577e1db956a in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, base::PlatformThreadHandle*, base::ThreadPriority) ./../../base/threading/platform_thread_posix.cc:120:13
    #2 0x5577e1cc6b67 in base::internal::WorkerThread::Start(base::WorkerThreadObserver*) ./../../base/task/thread_pool/worker_thread.cc:68:3
    #3 0x5577e1cb4f94 in operator() ./../../base/task/thread_pool/thread_group_impl.cc:185:15
    #4 0x5577e1cb4f94 in ForEachWorker<(lambda at ../../base/task/thread_pool/thread_group_impl.cc:184:37)> ./../../base/task/thread_pool/thread_group_impl.cc:150:0
    #5 0x5577e1cb4f94 in base::internal::ThreadGroupImpl::ScopedWorkersExecutor::FlushImpl() ./../../base/task/thread_pool/thread_group_impl.cc:184:0
    #6 0x5577e1cadc97 in base::internal::ThreadGroupImpl::ScopedWorkersExecutor::~ScopedWorkersExecutor() ./../../base/task/thread_pool/thread_group_impl.cc:103:30
    #7 0x5577e1cadaf2 in base::internal::ThreadGroupImpl::Start(int, int, base::TimeDelta, scoped_refptr<base::TaskRunner>, base::WorkerThreadObserver*, base::internal::ThreadGroup::WorkerEnvironment, base::Optional<base::TimeDelta>) ./../../base/task/thread_pool/thread_group_impl.cc:425:1
    #8 0x5577e1c9ad40 in base::internal::ThreadPoolImpl::Start(base::ThreadPoolInstance::InitParams const&, base::WorkerThreadObserver*) ./../../base/task/thread_pool/thread_pool_impl.cc:192:11
    #9 0x5577eb38cb97 in content::ChildProcess::ChildProcess(base::ThreadPriority, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::unique_ptr<base::ThreadPoolInstance::InitParams, std::__1::default_delete<base::ThreadPoolInstance::InitParams> >) ./../../content/child/child_process.cc:44:40
    #10 0x5577f1124e58 in content::RenderProcess::RenderProcess(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::unique_ptr<base::ThreadPoolInstance::InitParams, std::__1::default_delete<base::ThreadPoolInstance::InitParams> >) ./../../content/renderer/render_process.cc:15:7
    #11 0x5577f1123ed6 in content::RenderProcessImpl::RenderProcessImpl() ./../../content/renderer/render_process_impl.cc:88:7
    #12 0x5577f1124c0a in content::RenderProcessImpl::Create() ./../../content/renderer/render_process_impl.cc:237:31
    #13 0x5577f23f8640 in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:182:53
    #14 0x5577e0be3176 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:873:10
    #15 0x5577e0d866c1 in service_manager::Main(service_manager::MainParams const&) ./../../services/service_manager/embedder/main.cc:422:29
    #16 0x5577e0bddfdc in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:19:10
    #17 0x5577d81aac23 in ChromeMain ./../../chrome/app/chrome_main.cc:103:12
    #18 0x7f3671556b96 in __libc_start_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310:0

SUMMARY: AddressSanitizer: heap-use-after-free (/home/cowboy/chromium/src/out/chrome_asan_shared/chrome+0xf55578b)
Shadow bytes around the buggy address:
  0x0c0480023c30: fa fa fd fa fa fa fa fa fa fa fd fd fa fa fd fa
  0x0c0480023c40: fa fa fa fa fa fa fa fa fa fa fd fa fa fa fd fd
  0x0c0480023c50: fa fa fa fa fa fa fa fa fa fa fd fa fa fa fa fa
  0x0c0480023c60: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fd
  0x0c0480023c70: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa
=>0x0c0480023c80: fa fa fd fa fa fa fd[fd]fa fa fd fa fa fa 00 fa
  0x0c0480023c90: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fd
  0x0c0480023ca0: fa fa fd fa fa fa fd fd fa fa 00 00 fa fa fd fd
  0x0c0480023cb0: fa fa 00 00 fa fa fd fd fa fa fd fd fa fa fd fa
  0x0c0480023cc0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa
  0x0c0480023cd0: fa fa fd fa fa fa 00 fa fa fa fd fa fa fa fd fd
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
==100704==ABORTING
Received signal 6
    #0 0x5577d813ed0b in backtrace /b/swarming/w/ir/k/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4090:13
    #1 0x5577e1d81ce4 in base::debug::CollectStackTrace(void**, unsigned long) ./../../base/debug/stack_trace_posix.cc:834:39
    #2 0x5577e1b3e142 in StackTrace ./../../base/debug/stack_trace.cc:206:12
    #3 0x5577e1b3e142 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:203:0
    #4 0x5577e1d8096a in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:341:3
    #5 0x7f3678829890 in __funlockfile ??:?
    #6 0x7f3678829890 in ?? ??:0
    #7 0x7f3671573e97 in __libc_signal_restore_set /build/glibc-OTsEL5/glibc-2.27/signal/../sysdeps/unix/sysv/linux/nptl-signals.h:80:0
    #8 0x7f3671573e97 in raise /build/glibc-OTsEL5/glibc-2.27/signal/../sysdeps/unix/sysv/linux/raise.c:48:0
    #9 0x7f3671575801 in abort /build/glibc-OTsEL5/glibc-2.27/stdlib/abort.c:79:0
    #10 0x5577d8197c27 in __sanitizer::Abort() /b/swarming/w/ir/k/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_posix_libcdep.cc:154:3
    #11 0x5577d8196961 in __sanitizer::Die() /b/swarming/w/ir/k/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_termination.cc:58:5
    #12 0x5577d8183339 in __asan::ScopedInErrorReport::~ScopedInErrorReport() _asan_rtl_:7
    #13 0x5577d8184b76 in __asan::ReportGenericError(unsigned long, unsigned long, unsigned long, unsigned long, bool, unsigned long, unsigned int, bool) _asan_rtl_:1
    #14 0x5577d818579b in __asan_report_store8 _asan_rtl_:1
    #15 0x5577dedc078c in Cancel ./../../v8/src/wasm/wasm-engine.cc:110:28
    #16 0x5577dedc078c in v8::internal::wasm::WasmEngine::RemoveIsolateFromCurrentGC(v8::internal::Isolate*) ./../../v8/src/wasm/wasm-engine.cc:869:0
    #17 0x5577dedbfc5c in v8::internal::wasm::WasmEngine::RemoveIsolate(v8::internal::Isolate*) ./../../v8/src/wasm/wasm-engine.cc:592:9
    #18 0x5577ddfd185c in v8::internal::Isolate::Deinit() ./../../v8/src/execution/isolate.cc:3006:19
    #19 0x5577ddfd1209 in v8::internal::Isolate::Delete(v8::internal::Isolate*) ./../../v8/src/execution/isolate.cc:2838:12
    #20 0x5577ec20887b in gin::IsolateHolder::~IsolateHolder() ./../../gin/isolate_holder.cc:94:13
    #21 0x5577ebe1fd91 in blink::V8PerIsolateData::Destroy(v8::Isolate*) ./../../third_party/blink/renderer/platform/bindings/v8_per_isolate_data.cc:205:3
    #22 0x5577ef4a0912 in blink::WorkerBackingThread::ShutdownOnBackingThread() ./../../third_party/blink/renderer/core/workers/worker_backing_thread.cc:108:3
    #23 0x5577f14a4901 in blink::WorkletThreadHolder<blink::AudioWorkletThread>::ShutdownOnWorkletThread(base::WaitableEvent*) ./../../third_party/blink/renderer/core/workers/worklet_thread_holder.h:85:14
    #24 0x5577e1c54d8f in Run ./../../base/callback.h:97:12
    #25 0x5577e1c54d8f in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:142:0
    #26 0x5577e1c8b530 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*, bool*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:368:23
    #27 0x5577e1c8aae3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:219:7
    #28 0x5577e1b99e31 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39:55
    #29 0x5577e1c8d615 in Run ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:466:12
    #30 0x5577e1c8d615 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #31 0x5577e1c07b09 in base::RunLoop::RunWithTimeout(base::TimeDelta) ./../../base/run_loop.cc:161:14
    #32 0x5577dfd409fa in blink::scheduler::WorkerThread::SimpleThreadImpl::Run() ./../../third_party/blink/renderer/platform/scheduler/worker/worker_thread.cc:127:14
    #33 0x5577e1dba39e in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:81:13
    #34 0x7f367881e6db in start_thread ??:0:0
    #35 0x7f367165688f in clone /build/glibc-OTsEL5/glibc-2.27/misc/../sysdeps/unix/sysv/linux/x86_64/clone.S:95:0
  r8: 0000000000000000  r9: 00007f365734e1e0 r10: 0000000000000008 r11: 0000000000000246
 r12: 00007f365734f1a0 r13: 00007f365734f198 r14: 00007f365734f140 r15: 00005577f5306188
  di: 0000000000000002  si: 00007f365734e1e0  bp: 00007f365734f170  bx: 00005577f5273cc8
  dx: 0000000000000000  ax: 0000000000000000  cx: 00007f3671573e97  sp: 00007f365734e1e0
  ip: 00007f3671573e97 efl: 0000000000000246 cgf: 002b000000000033 erf: 0000000000000000
 trp: 0000000000000000 msk: 0000000000000000 cr2: 0000000000000000
[end of stack trace]
Calling _exit(1). Core file will not be generated.

Did this work before? N/A 

Chrome version: Chromium 77.0.3815.0  Channel: dev
OS Version: 18.04
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [res.zip](attachments/res.zip) (application/octet-stream, 45.6 KB)

## Timeline

### cd...@gmail.com (2019-06-05)

Sorry.The second step is wrong. I'll update it.

2.File name is wrong(bit-crusher.js->wasmmodule.js) .Js and POC file paths need not be modified. Just run "node ws.js" to  setup a webserver'. 
Thanks~~


### wf...@chromium.org (2019-06-05)

Assigning to v8 sheriff -> clemensh@ as per instructions [1]

Will attempt repro in the meantime.

[1] - https://chromium.googlesource.com/chromium/src/+/master/docs/security/sheriff.md

[Monorail components: Blink>JavaScript>WebAssembly]

### cl...@chromium.org (2019-06-06)

I cannot unpack the rar archive. Maybe broken, or some weird version. Can you reupload, either as plain files or zipped?

### cd...@gmail.com (2019-06-06)

I uploaded again with zip file.Try this one.


### cl...@chromium.org (2019-06-06)

I can extract the zip now, and run it (took me a while to set up node). I don't get the crash though.
I will be OOO the next two weeks. Can you try to come up with a chrome-only version, i.e. without depending on node?

### cd...@gmail.com (2019-06-06)

I tried a single file, but failed to reproduce it. Crash can only be triggered by implementing C/S mode through webscoket.

### wf...@chromium.org (2019-06-06)

this is a shutdown-only crash? I also can't repro... is there any way to get this to repro by just using python webserver and chrome?

### cl...@chromium.org (2019-06-06)

Oh, I just realize that this probably requires the --wasm-code-gc flag (--js-flags=--wasm-code-gc on chrome). Maybe adding --stress-wasm-code-gc increases the chance to reproduce this.

Wasm code GC is a feature we are just finching (50% canary/dev and 1% beta).

Yes, this is a shutdown problem. It happens when an Isolate is destroyed while a GC is running. We try to cancel the foreground task for that isolate, which seems to have been deleted already.
This does not look too urgent, it's probably enough if I fix this in two weeks.

### cl...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### wf...@chromium.org (2019-06-07)

please don't ship wasm-code-gc to stable without this bug being fixed. Seems like it's High though as it's a UAF write.

### sh...@chromium.org (2019-06-08)

Setting milestone and target because of Security_Impact=Beta and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2019-06-08)

This issue seems to be found in M77 but https://crbug.com/chromium/971293#c1 mentioned version M74, Does this impact M75 stable roll out? As in are we blocking M75 stable roll out for this bug? If not pls remove M75 and target to M76.

### cd...@gmail.com (2019-06-09)

Not m74, I forgot modify default report  template.

### sr...@google.com (2019-06-09)

Reading through the comments, this look like caused due to a finch flag enabled for beta/dev/canary. From that this should not block . M75 stable as we are in the middle of roll out. I am updating the target version to M76 . Pls get the change fixed in M76. 

Pls feel free to add the M-75 labels, if you think this is high prioroty issue blocking M75 stable roll out. 

### go...@chromium.org (2019-06-14)

Reminder M76 is already in Beta and Stable promotion is coming soon. Please review this bug and assess if this is indeed a RBS. If not, please remove the RBS label. If so, please make sure to land the fix and request a merge into the release branch ASAP. Thank you.

### go...@chromium.org (2019-06-18)

Reminder M76 is already in Beta and Stable promotion is coming soon. Please review this bug and assess if this is indeed a RBS. If not, please remove the RBS label. If so, please make sure to land the fix and request a merge into the release branch ASAP. Thank you.


### ti...@chromium.org (2019-06-18)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-06-20)

Reminder M76 is already in Beta and Stable promotion is coming soon. Please review this bug and assess if this is indeed a RBS. If not, please remove the RBS label. If so, please make sure to land the fix and request a merge into the release branch ASAP. Thank you.

### cl...@chromium.org (2019-06-21)

Still can't reproduce, but got a CL which should fix this issue: https://crrev.com/c/1669694

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/3ea51d4692c9be52b3fce7b5420732d54987c7e3

commit 3ea51d4692c9be52b3fce7b5420732d54987c7e3
Author: Clemens Hammacher <clemensh@chromium.org>
Date: Fri Jun 21 13:43:38 2019

[wasm][gc] Deregister foreground task in destructor

The platform is allowed to remove the foreground task without ever
executing it if the isolate is shutting down. This can happen
immediately when spawning the task. This would leave a stale pointer to
the deleted task in the engine, and can lead to UAF.
Thus deregister the task also from the destructor. At that point, we do
not need to report back any live code for that isolate.

R=ahaas@chromium.org

Bug: v8:8217, chromium:971293
Change-Id: I7081efde8f306649d08956e758254a8875db8271
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1669694
Reviewed-by: Andreas Haas <ahaas@chromium.org>
Commit-Queue: Clemens Hammacher <clemensh@chromium.org>
Cr-Commit-Position: refs/heads/master@{#62312}

[modify] https://crrev.com/3ea51d4692c9be52b3fce7b5420732d54987c7e3/src/wasm/wasm-engine.cc


### cl...@chromium.org (2019-06-21)

Probably fixed by #20. Let's wait for canary coverage, then merge to 76.

### bu...@chromium.org (2019-06-21)

[Auto-generated comment by a script] We noticed that this issue is targeted for M-76; it appears the fix may have landed after branch point, meaning a merge might be required. The owner of this bug should confirm if a merge is required here. If so, add Merge-Request-76 label and indicate which commits/CLs are to be merged. Otherwise, remove Merge-TBD label. Thanks.

### sh...@chromium.org (2019-06-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-21)

Requesting merge to beta M76 even though there is no obvious Chromium repository trunk commit here. Perhaps it was fixed in another ticket; please investigate.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-06-21)

This bug requires manual review: M76 has already been promoted to the beta branch, so this requires manual review
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
Owners: govind@(Android), kariahda@(iOS), cindyb@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2019-06-24)

No new canary since Friday. Postponing till Wednesday.

### na...@google.com (2019-06-24)

[Empty comment from Monorail migration]

### ab...@google.com (2019-06-25)

clemensh@ have we confirmed this in last night's canary?

### ab...@google.com (2019-06-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-06-26)

This has enough canary coverage now. Requesting merge to M-76.

Answering sheriffbot's question:

1. Does your merge fit within the Merge Decision Guidelines?
Yes (release blocker and low complexity)

2. Links to the CLs you are requesting to merge.
3ea51d4692c9be52b3fce7b5420732d54987c7e3 (Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1669694)

3. Has the change landed and been verified on master/ToT?
Yes

4. Why are these changes required in this milestone after branch?
Fixes UAF.

5. Is this a new feature?
No

6. If it is a new feature, is it behind a flag using finch?
n/a

### ab...@google.com (2019-06-26)

branch:3809

### go...@chromium.org (2019-06-26)

Please merge your change to M76 branch 3809 ASAP. Thank you.

### cl...@chromium.org (2019-07-01)

Merged in https://crrev.com/c/1679497. Bugdroid somehow missed it.

### na...@google.com (2019-07-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-07-17)

Congrats! The Panel decided to reward $1,000 for this report!

### na...@google.com (2019-07-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2020-02-17)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/971293?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095298)*
