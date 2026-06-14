# Null-dereference READ in blink::AudioNode::Handler

| Field | Value |
|-------|-------|
| **Issue ID** | [40091851](https://issues.chromium.org/issues/40091851) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebAudio |
| **Platforms** | Linux |
| **Reporter** | cd...@gmail.com |
| **Assignee** | rt...@chromium.org |
| **Created** | 2018-07-05 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36

Steps to reproduce the problem:
Version 69.0.3477.0 (Developer Build) (64-bit)
1.Get new version chrome:
    Build source code 
    Config args.gn file as below:
		use_sanitizer_coverage = true
		is_asan = true
		is_debug = false
		enable_nacl = false
		treat_warnings_as_errors = false
	ninja -j16 -C out/chrome_asan chrome

What is the expected behavior?

What went wrong?
2. 
	a) ./crhome ./crash.html
	b) click "ctrl +shift+i" to open Developer tools
	c) and get heap-use-after-free(10 seconds to 2minutes),or occasionally get sig11 0x00000038(null dereference).

	==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x60e0001c3f80 at pc 0x55d1f96ad3a8 bp 0x7f8110ddb250 sp 0x7f8110ddb248
READ of size 1 at 0x60e0001c3f80 thread T273 (WebAudio thread)
    #0 0x55d1f96ad3a7 in blink::InspectorTaskRunner::V8InterruptCallback(v8::Isolate*, void*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/inspector/inspector_task_runner.cc:128:15
    #1 0x55d1ec1c3c9d in v8::internal::Isolate::InvokeApiInterruptCallbacks() /home/cowboy/chromium/src/out/chrome_asan_shared/../../v8/src/isolate.cc:1095:5
    #2 0x55d1ebe83de4 in v8::internal::StackGuard::HandleInterrupts() /home/cowboy/chromium/src/out/chrome_asan_shared/../../v8/src/execution.cc:552:15
    #3 0x55d1ec6cc543 in __RT_impl_Runtime_StackGuard /home/cowboy/chromium/src/out/chrome_asan_shared/../../v8/src/runtime/runtime-internal.cc:264:34
    #4 0x55d1ec6cc543 in v8::internal::Runtime_StackGuard(int, v8::internal::Object**, v8::internal::Isolate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../v8/src/runtime/runtime-internal.cc:254:0
    #5 0x55d1ecde8c0d in v8_Default_embedded_blob_ embedded.cc:?
    #6 0x55d1ecde8c0d in ?? ??:0
    #5 0x7e978d8040c1  (<unknown module>)
    #6 0x7e978d78868f  (<unknown module>)
    #7 0x55d1ecd4e7c2 in v8_Default_embedded_blob_ embedded.cc:?
    #8 0x55d1ecd4e7c2 in ?? ??:0
    #8 0x7e978d7855c0  (<unknown module>)
    #9 0x55d1ebe816bc in Call /home/cowboy/chromium/src/out/chrome_asan_shared/../../v8/src/simulator.h:113:12
    #10 0x55d1ebe816bc in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, bool, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, v8::internal::Handle<v8::internal::Object>, v8::internal::Execution::MessageHandling, v8::internal::Execution::Target) /home/cowboy/chromium/src/out/chrome_asan_shared/../../v8/src/execution.cc:155:0
    #11 0x55d1ebe80eb6 in CallInternal /home/cowboy/chromium/src/out/chrome_asan_shared/../../v8/src/execution.cc:191:10
    #12 0x55d1ebe80eb6 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../v8/src/execution.cc:202:0
    #13 0x55d1ec3b6211 in v8::internal::Module::RunInitializationCode(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Module>) /home/cowboy/chromium/src/out/chrome_asan_shared/../../v8/src/objects/module.cc:543:7
    #14 0x55d1ec3b587f in MaybeTransitionComponent /home/cowboy/chromium/src/out/chrome_asan_shared/../../v8/src/objects/module.cc:572:14
    #15 0x55d1ec3b587f in v8::internal::Module::FinishInstantiate(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Module>, v8::internal::ZoneForwardList<v8::internal::Handle<v8::internal::Module> >*, unsigned int*, v8::internal::Zone*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../v8/src/objects/module.cc:663:0
    #16 0x55d1ec3b24e6 in v8::internal::Module::Instantiate(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Module>, v8::Local<v8::Context>, v8::MaybeLocal<v8::Module> (*)(v8::Local<v8::Context>, v8::Local<v8::String>, v8::Local<v8::Module>)) /home/cowboy/chromium/src/out/chrome_asan_shared/../../v8/src/objects/module.cc:460:8
    #17 0x55d1eb480612 in v8::Module::InstantiateModule(v8::Local<v8::Context>, v8::MaybeLocal<v8::Module> (*)(v8::Local<v8::Context>, v8::Local<v8::String>, v8::Local<v8::Module>)) /home/cowboy/chromium/src/out/chrome_asan_shared/../../v8/src/api.cc:2355:28
    #18 0x55d1f7050194 in blink::ScriptModule::Instantiate(blink::ScriptState*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/bindings/core/v8/script_module.cc:63:14
    #19 0x55d1fa300653 in blink::ModulatorImplBase::InstantiateModule(blink::ScriptModule) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/script/modulator_impl_base.cc:193:24
    #20 0x55d1fa30aba4 in blink::ModuleTreeLinker::Instantiate() /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/loader/modulescript/module_tree_linker.cc:446:51
    #21 0x55d1fa309595 in FinalizeFetchDescendantsForOneModuleScript /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/loader/modulescript/module_tree_linker.cc:412:5
    #22 0x55d1fa309595 in blink::ModuleTreeLinker::FetchDescendants(blink::ModuleScript*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/loader/modulescript/module_tree_linker.cc:363:0
    #23 0x55d1fa30a40b in blink::ModuleTreeLinker::NotifyModuleLoadFinished(blink::ModuleScript*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/loader/modulescript/module_tree_linker.cc:289:3
    #24 0x55d1ee0a32f0 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:99:12
    #25 0x55d1ee0a32f0 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #26 0x55d1ecfa6f35 in base::sequence_manager::internal::ThreadControllerImpl::DoWork(base::sequence_manager::internal::ThreadControllerImpl::WorkType) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/scheduler/base/thread_controller_impl.cc:166:21
    #27 0x55d1ee0a32f0 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:99:12
    #28 0x55d1ee0a32f0 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #29 0x55d1ee102442 in base::MessageLoop::RunTask(base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:319:25
    #30 0x55d1ee1036bf in DeferOrRunPendingTask /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:329:5
    #31 0x55d1ee1036bf in base::MessageLoop::DoWork() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:373:0
    #32 0x55d1ee10beef in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_pump_default.cc:37:31
    #33 0x55d1ee17db20 in base::RunLoop::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/run_loop.cc:102:14
    #34 0x55d1ee209c10 in base::Thread::ThreadMain() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/thread.cc:337:3
    #35 0x55d1ee2cc1e0 in base::(anonymous namespace)::ThreadFunc(void*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/platform_thread_posix.cc:76:13
    #36 0x7f8131b406b9 in start_thread ??:0:0

0x60e0001c3f80 is located 64 bytes inside of 152-byte region [0x60e0001c3f40,0x60e0001c3fd8)
freed by thread T0 (chrome) here:
    #0 0x55d1e66feac2 in __interceptor_free _asan_rtl_:3
    #1 0x55d1fa701451 in Free /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/allocator/partition_allocator/partition_alloc.h:343:3
    #2 0x55d1fa701451 in FastFree /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/wtf/allocator/partitions.h:119:0
    #3 0x55d1fa701451 in operator delete /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/inspector/inspector_task_runner.h:29:0
    #4 0x55d1fa701451 in DeleteInternal<blink::InspectorTaskRunner> /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/wtf/thread_safe_ref_counted.h:64:0
    #5 0x55d1fa701451 in Destruct /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/wtf/thread_safe_ref_counted.h:44:0
    #6 0x55d1fa701451 in Release /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/memory/ref_counted.h:387:0
    #7 0x55d1fa701451 in Release /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/memory/scoped_refptr.h:280:0
    #8 0x55d1fa701451 in ~scoped_refptr /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/memory/scoped_refptr.h:208:0
    #9 0x55d1fa701451 in blink::WorkerThread::~WorkerThread() /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/workers/worker_thread.cc:101:0
    #10 0x55d1fc773c64 in ~AudioWorkletThread /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet_thread.cc:52:1
    #11 0x55d1fc773c64 in blink::AudioWorkletThread::~AudioWorkletThread() /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet_thread.cc:48:0
    #12 0x55d1fa6cda64 in operator() /home/cowboy/chromium/src/out/chrome_asan_shared/../../buildtools/third_party/libc++/trunk/include/memory:2321:5
    #13 0x55d1fa6cda64 in reset /home/cowboy/chromium/src/out/chrome_asan_shared/../../buildtools/third_party/libc++/trunk/include/memory:2634:0
    #14 0x55d1fa6cda64 in ~unique_ptr /home/cowboy/chromium/src/out/chrome_asan_shared/../../buildtools/third_party/libc++/trunk/include/memory:2588:0
    #15 0x55d1fa6cda64 in blink::ThreadedMessagingProxyBase::WorkerThreadTerminated() /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/workers/threaded_messaging_proxy_base.cc:164:0
    #16 0x55d1fa6d2630 in Invoke<void (blink::ThreadedMessagingProxyBase::*)(), blink::CrossThreadPersistent<blink::ThreadedMessagingProxyBase>> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:507:12
    #17 0x55d1fa6d2630 in MakeItSo<void (blink::ThreadedMessagingProxyBase::*const &)(), blink::CrossThreadPersistent<blink::ThreadedMessagingProxyBase>> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:627:0
    #18 0x55d1fa6d2630 in RunImpl<void (blink::ThreadedMessagingProxyBase::*const &)(), const std::__1::tuple<blink::CrossThreadWeakPersistent<blink::ThreadedMessagingProxyBase> > &, 0> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:680:0
    #19 0x55d1fa6d2630 in base::internal::Invoker<base::internal::BindState<void (blink::ThreadedMessagingProxyBase::*)(), blink::CrossThreadWeakPersistent<blink::ThreadedMessagingProxyBase> >, void ()>::Run(base::internal::BindStateBase*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:662:0
    #20 0x55d1f6fa7c0a in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:140:12
    #21 0x55d1f6fa7c0a in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/wtf/functional.h:320:0
    #22 0x55d1f6fa7c0a in blink::(anonymous namespace)::RunCrossThreadClosure(WTF::CrossThreadFunction<void ()>) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/web_task_runner.cc:15:0
    #23 0x55d1f6fa8cd8 in Invoke<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> > /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:407:12
    #24 0x55d1f6fa8cd8 in MakeItSo<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> > /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:607:0
    #25 0x55d1f6fa8cd8 in RunImpl<void (*)(WTF::CrossThreadFunction<void ()>), std::__1::tuple<WTF::CrossThreadFunction<void ()> >, 0> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:680:0
    #26 0x55d1f6fa8cd8 in base::internal::Invoker<base::internal::BindState<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> >, void ()>::RunOnce(base::internal::BindStateBase*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:649:0
    #27 0x55d1ee0a32f0 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:99:12
    #28 0x55d1ee0a32f0 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #29 0x55d1ecfa6f35 in base::sequence_manager::internal::ThreadControllerImpl::DoWork(base::sequence_manager::internal::ThreadControllerImpl::WorkType) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/scheduler/base/thread_controller_impl.cc:166:21
    #30 0x55d1ee0a32f0 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:99:12
    #31 0x55d1ee0a32f0 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #32 0x55d1ee102442 in base::MessageLoop::RunTask(base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:319:25
    #33 0x55d1ee1036bf in DeferOrRunPendingTask /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:329:5
    #34 0x55d1ee1036bf in base::MessageLoop::DoWork() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:373:0
    #35 0x55d1ee10beef in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_pump_default.cc:37:31
    #36 0x55d1ee17db20 in base::RunLoop::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/run_loop.cc:102:14
    #37 0x55d1fd1b05b5 in content::RendererMain(content::MainFunctionParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/renderer/renderer_main.cc:218:23
    #38 0x55d1ed5ffb59 in content::RunZygote(content::ContentMainDelegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:561:14
    #39 0x55d1ed60338d in content::ContentMainRunnerImpl::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:960:10
    #40 0x55d1ed623493 in service_manager::Main(service_manager::MainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../services/service_manager/embedder/main.cc:459:29
    #41 0x55d1ed5fe197 in content::ContentMain(content::ContentMainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main.cc:19:10
    #42 0x55d1e672e42f in ChromeMain /home/cowboy/chromium/src/out/chrome_asan_shared/../../chrome/app/chrome_main.cc:101:12
    #43 0x7f812aba782f in __libc_start_main /build/glibc-Cl5G7W/glibc-2.23/csu/../csu/libc-start.c:291:0

previously allocated by thread T0 (chrome) here:
    #0 0x55d1e66fee43 in __interceptor_malloc _asan_rtl_:3
    #1 0x55d1f8c0b48e in PartitionAllocGenericFlags /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/allocator/partition_allocator/partition_alloc.h:318:18
    #2 0x55d1f8c0b48e in Alloc /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/allocator/partition_allocator/partition_alloc.h:338:0
    #3 0x55d1f8c0b48e in FastMalloc /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/wtf/allocator/partitions.h:109:0
    #4 0x55d1f8c0b48e in operator new /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/inspector/inspector_task_runner.h:29:0
    #5 0x55d1f8c0b48e in blink::InspectorTaskRunner::Create(scoped_refptr<base::SingleThreadTaskRunner>) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/inspector/inspector_task_runner.h:35:0
    #6 0x55d1fa702111 in blink::WorkerThread::Start(std::__1::unique_ptr<blink::GlobalScopeCreationParams, std::__1::default_delete<blink::GlobalScopeCreationParams> >, base::Optional<blink::WorkerBackingThreadStartupData> const&, blink::WorkerInspectorProxy::PauseOnWorkerStart, blink::ParentExecutionContextTaskRunners*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/workers/worker_thread.cc:124:7
    #7 0x55d1fa6cccdb in blink::ThreadedMessagingProxyBase::InitializeWorkerThread(std::__1::unique_ptr<blink::GlobalScopeCreationParams, std::__1::default_delete<blink::GlobalScopeCreationParams> >, base::Optional<blink::WorkerBackingThreadStartupData> const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/workers/threaded_messaging_proxy_base.cc:96:19
    #8 0x55d1fc7b8e55 in blink::ThreadedWorkletMessagingProxy::Initialize(blink::WorkerClients*, blink::WorkletModuleResponsesMap*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/workers/threaded_worklet_messaging_proxy.cc:70:3
    #9 0x55d1fc76c191 in blink::AudioWorklet::CreateGlobalScope() /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet.cc:82:10
    #10 0x55d1fa7144a8 in blink::Worklet::FetchAndInvokeScript(blink::KURL const&, blink::WorkletOptions const&, blink::WorkletPendingTasks*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/workers/worklet.cc:147:24
    #11 0x55d1ee0a32f0 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:99:12
    #12 0x55d1ee0a32f0 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #13 0x55d1ecfa6f35 in base::sequence_manager::internal::ThreadControllerImpl::DoWork(base::sequence_manager::internal::ThreadControllerImpl::WorkType) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/scheduler/base/thread_controller_impl.cc:166:21
    #14 0x55d1ee0a32f0 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:99:12
    #15 0x55d1ee0a32f0 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #16 0x55d1ee102442 in base::MessageLoop::RunTask(base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:319:25
    #17 0x55d1ee1036bf in DeferOrRunPendingTask /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:329:5
    #18 0x55d1ee1036bf in base::MessageLoop::DoWork() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:373:0
    #19 0x55d1ee10beef in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_pump_default.cc:37:31
    #20 0x55d1ee17db20 in base::RunLoop::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/run_loop.cc:102:14
    #21 0x55d1fd1b05b5 in content::RendererMain(content::MainFunctionParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/renderer/renderer_main.cc:218:23
    #22 0x55d1ed5ffb59 in content::RunZygote(content::ContentMainDelegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:561:14
    #23 0x55d1ed60338d in content::ContentMainRunnerImpl::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:960:10
    #24 0x55d1ed623493 in service_manager::Main(service_manager::MainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../services/service_manager/embedder/main.cc:459:29
    #25 0x55d1ed5fe197 in content::ContentMain(content::ContentMainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main.cc:19:10
    #26 0x55d1e672e42f in ChromeMain /home/cowboy/chromium/src/out/chrome_asan_shared/../../chrome/app/chrome_main.cc:101:12
    #27 0x7f812aba782f in __libc_start_main /build/glibc-Cl5G7W/glibc-2.23/csu/../csu/libc-start.c:291:0

Thread T273 (WebAudio thread) created by T0 (chrome) here:
    #0 0x55d1e66e775d in __interceptor_pthread_create _asan_rtl_:3
    #1 0x55d1ee2cb45a in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, base::PlatformThreadHandle*, base::ThreadPriority) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/platform_thread_posix.cc:115:13
    #2 0x55d1ee208eb5 in base::Thread::StartWithOptions(base::Thread::Options const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/thread.cc:112:15
    #3 0x55d1ecfb6f03 in blink::scheduler::WebThreadImplForWorkerScheduler::WebThreadImplForWorkerScheduler(blink::WebThreadCreationParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/scheduler/child/webthread_impl_for_worker_scheduler.cc:30:27
    #4 0x55d1ecfb63e3 in make_unique<blink::scheduler::WebThreadImplForWorkerScheduler, const blink::WebThreadCreationParams &> /home/cowboy/chromium/src/out/chrome_asan_shared/../../buildtools/third_party/libc++/trunk/include/memory:3114:32
    #5 0x55d1ecfb63e3 in blink::scheduler::WebThreadBase::CreateWorkerThread(blink::WebThreadCreationParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/scheduler/child/webthread_base.cc:119:0
    #6 0x55d1f6b6a765 in content::BlinkPlatformImpl::CreateWebAudioThread() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/child/blink_platform_impl.cc:398:7
    #7 0x55d1fc7737d9 in EnsureSharedBackingThread /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet_thread.cc:79:46
    #8 0x55d1fc7737d9 in AudioWorkletThread /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet_thread.cc:45:0
    #9 0x55d1fc7737d9 in blink::AudioWorkletThread::Create(blink::ThreadableLoadingContext*, blink::WorkerReportingProxy&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet_thread.cc:36:0
    #10 0x55d1fc76ecc3 in blink::AudioWorkletMessagingProxy::CreateWorkerThread() /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet_messaging_proxy.cc:96:10
    #11 0x55d1fa6ccb0a in blink::ThreadedMessagingProxyBase::InitializeWorkerThread(std::__1::unique_ptr<blink::GlobalScopeCreationParams, std::__1::default_delete<blink::GlobalScopeCreationParams> >, base::Optional<blink::WorkerBackingThreadStartupData> const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/workers/threaded_messaging_proxy_base.cc:95:20
    #12 0x55d1fc7b8e55 in blink::ThreadedWorkletMessagingProxy::Initialize(blink::WorkerClients*, blink::WorkletModuleResponsesMap*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/workers/threaded_worklet_messaging_proxy.cc:70:3
    #13 0x55d1fc76c191 in blink::AudioWorklet::CreateGlobalScope() /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet.cc:82:10
    #14 0x55d1fa7144a8 in blink::Worklet::FetchAndInvokeScript(blink::KURL const&, blink::WorkletOptions const&, blink::WorkletPendingTasks*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/workers/worklet.cc:147:24
    #15 0x55d1ee0a32f0 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:99:12
    #16 0x55d1ee0a32f0 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #17 0x55d1ecfa6f35 in base::sequence_manager::internal::ThreadControllerImpl::DoWork(base::sequence_manager::internal::ThreadControllerImpl::WorkType) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/scheduler/base/thread_controller_impl.cc:166:21
    #18 0x55d1ee0a32f0 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:99:12
    #19 0x55d1ee0a32f0 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #20 0x55d1ee102442 in base::MessageLoop::RunTask(base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:319:25
    #21 0x55d1ee1036bf in DeferOrRunPendingTask /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:329:5
    #22 0x55d1ee1036bf in base::MessageLoop::DoWork() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:373:0
    #23 0x55d1ee10beef in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_pump_default.cc:37:31
    #24 0x55d1ee17db20 in base::RunLoop::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/run_loop.cc:102:14
    #25 0x55d1fd1b05b5 in content::RendererMain(content::MainFunctionParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/renderer/renderer_main.cc:218:23
    #26 0x55d1ed5ffb59 in content::RunZygote(content::ContentMainDelegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:561:14
    #27 0x55d1ed60338d in content::ContentMainRunnerImpl::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:960:10
    #28 0x55d1ed623493 in service_manager::Main(service_manager::MainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../services/service_manager/embedder/main.cc:459:29
    #29 0x55d1ed5fe197 in content::ContentMain(content::ContentMainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main.cc:19:10
    #30 0x55d1e672e42f in ChromeMain /home/cowboy/chromium/src/out/chrome_asan_shared/../../chrome/app/chrome_main.cc:101:12
    #31 0x7f812aba782f in __libc_start_main /build/glibc-Cl5G7W/glibc-2.23/csu/../csu/libc-start.c:291:0

SUMMARY: AddressSanitizer: heap-use-after-free (/home/cowboy/chromium/src/out/chrome_asan_shared/chrome+0x1ab243a7)
Shadow bytes around the buggy address:
  0x0c1c800307a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c1c800307b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c1c800307c0: fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c1c800307d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c1c800307e0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
=>0x0c1c800307f0:[fd]fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x0c1c80030800: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c1c80030810: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c1c80030820: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c1c80030830: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c1c80030840: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
Received signal 6
    #0 0x55d1e66a4811 in __interceptor_backtrace /b/build/slave/linux_upload_clang/build/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4024:13
    #1 0x55d1ee29cc3e in base::debug::StackTrace::StackTrace(unsigned long) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/stack_trace_posix.cc:808:41
    #2 0x55d1ee29bb8d in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/stack_trace_posix.cc:334:3
    #3 0x7f8131b4a390 in __funlockfile ??:?
    #4 0x7f8131b4a390 in ?? ??:0
    #5 0x7f812abbc428 in gsignal /build/glibc-Cl5G7W/glibc-2.23/signal/../sysdeps/unix/sysv/linux/raise.c:54:0
    #6 0x7f812abbe02a in abort /build/glibc-Cl5G7W/glibc-2.23/stdlib/abort.c:89:0
    #7 0x55d1e671a377 in __sanitizer::Abort() /b/build/slave/linux_upload_clang/build/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_posix_libcdep.cc:155:3
    #8 0x55d1e6718da1 in __sanitizer::Die() /b/build/slave/linux_upload_clang/build/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_termination.cc:59:5
    #9 0x55d1e6705169 in __asan::ScopedInErrorReport::~ScopedInErrorReport() _asan_rtl_:7
    #10 0x55d1e6704663 in __asan::ReportGenericError(unsigned long, unsigned long, unsigned long, unsigned long, bool, unsigned long, unsigned int, bool) _asan_rtl_:1
    #11 0x55d1e67052db in __asan_report_load1 _asan_rtl_:1
    #12 0x55d1f96ad3a8 in blink::InspectorTaskRunner::V8InterruptCallback(v8::Isolate*, void*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/inspector/inspector_task_runner.cc:128:15
    #13 0x55d1ec1c3c9e in v8::internal::Isolate::InvokeApiInterruptCallbacks() /home/cowboy/chromium/src/out/chrome_asan_shared/../../v8/src/isolate.cc:1095:5
    #14 0x55d1ebe83de5 in v8::internal::StackGuard::HandleInterrupts() /home/cowboy/chromium/src/out/chrome_asan_shared/../../v8/src/execution.cc:552:15
    #15 0x55d1ec6cc544 in __RT_impl_Runtime_StackGuard /home/cowboy/chromium/src/out/chrome_asan_shared/../../v8/src/runtime/runtime-internal.cc:264:34
    #16 0x55d1ec6cc544 in v8::internal::Runtime_StackGuard(int, v8::internal::Object**, v8::internal::Isolate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../v8/src/runtime/runtime-internal.cc:254:0
    #17 0x55d1ecde8c0e in v8_Default_embedded_blob_ embedded.cc:?
    #18 0x55d1ecde8c0e in ?? ??:0
  r8: 000000000000d5c6  r9: 0000000000000000 r10: 0000000000000008 r11: 0000000000000202
 r12: 0000000000000000 r13: 00007f8110ddb248 r14: 00007f8110ddb1f0 r15: 000055d2004337d8
  di: 0000000000000001  si: 0000000000000112  bp: 00007f8110ddb220  bx: 000055d2003a1330
  dx: 0000000000000006  ax: 0000000000000000  cx: 00007f812abbc428  sp: 00007f8110dda3a8
  ip: 00007f812abbc428 efl: 0000000000000202 cgf: 002b000000000033 erf: 0000000000000000
 trp: 0000000000000000 msk: 0000000000000000 cr2: 0000000000000000
[end of stack trace]
Calling _exit(1). Core file will not be generated.

Did this work before? N/A 

Chrome version: Version 69.0.3477.0 (Developer Build) (64-bit)  Channel: dev
OS Version: Ubuntu16.04
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [crash.html](attachments/crash.html) (text/plain, 479 B)

## Timeline

### ke...@chromium.org (2018-07-05)

Thanks for the report.

rtoy@: I know these are piling up a bit but are you able to help triage this?

[Monorail components: Blink>WebAudio]

### cd...@gmail.com (2018-07-06)

Deleted by mistake, re-uploaded.

### rt...@chromium.org (2018-07-09)

I am unable to reproduce this crash with the given backtrace.  However, using the given test code, I get a different backtrace.  This looks similar to the crash in https://crbug.com/chromium/860626.  This is pretty reliable and just loading crash.html is enough, without having to open the dev console.

Tested using ToT from a few hours ago.

Received signal 11 SEGV_MAPERR 000000000038
    #0 0x55beed121811 in __interceptor_backtrace /b/swarming/w/ir/kitchen-workdir/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4024:13
    #1 0x7f199014566e in base::debug::StackTrace::StackTrace(unsigned long) ./../../base/debug/stack_trace_posix.cc:808:41
    #2 0x7f199014449f in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:334:3
    #3 0x7f19654340c0 in __funlockfile ??:?
    #4 0x7f19654340c0 in ?? ??:0
    #5 0x7f19695ed489 in operator* ./../../base/memory/scoped_refptr.h:215:13
    #6 0x7f19695ed489 in blink::AudioNode::Handler() const ./../../third_party/blink/renderer/modules/webaudio/audio_node.cc:641:0
    #7 0x7f19695df75d in blink::AudioDestinationNode::GetAudioDestinationHandler() const ./../../third_party/blink/renderer/modules/webaudio/audio_destination_node.cc:48:48
    #8 0x7f196968b789 in CurrentSampleFrame ./../../third_party/blink/renderer/modules/webaudio/base_audio_context.h:130:31
    #9 0x7f196968b789 in blink::BaseAudioContext::UpdateWorkletGlobalScopeOnRenderingThread() ./../../third_party/blink/renderer/modules/webaudio/base_audio_context.cc:909:0
    #10 0x7f19696a4b8c in blink::DefaultAudioDestinationHandler::Render(blink::AudioBus*, unsigned long, blink::AudioIOPosition const&) ./../../third_party/blink/renderer/modules/webaudio/default_audio_destination_node.cc:248:14
    #11 0x7f196ad4257d in blink::AudioDestination::RequestRender(unsigned long, unsigned long, double, double, unsigned long) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:186:15
    #12 0x7f196b4b6ba3 in Run ./../../base/callback.h:140:12
    #13 0x7f196b4b6ba3 in Run ./../../third_party/blink/renderer/platform/wtf/functional.h:320:0
    #14 0x7f196b4b6ba3 in blink::(anonymous namespace)::RunCrossThreadClosure(WTF::CrossThreadFunction<void ()>) ./../../third_party/blink/renderer/platform/web_task_runner.cc:15:0
    #15 0x7f196b4b7f94 in Invoke<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> > ./../../base/bind_internal.h:407:12
    #16 0x7f196b4b7f94 in MakeItSo<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> > ./../../base/bind_internal.h:607:0
    #17 0x7f196b4b7f94 in RunImpl<void (*)(WTF::CrossThreadFunction<void ()>), std::__1::tuple<WTF::CrossThreadFunction<void ()> >, 0> ./../../base/bind_internal.h:680:0
    #18 0x7f196b4b7f94 in base::internal::Invoker<base::internal::BindState<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> >, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:649:0
    #19 0x7f198fe3b992 in Run ./../../base/callback.h:99:12
    #20 0x7f198fe3b992 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/debug/task_annotator.cc:101:0
    #21 0x7f199000deb6 in base::sequence_manager::internal::ThreadControllerImpl::DoWork(base::sequence_manager::internal::ThreadControllerImpl::WorkType) ./../../base/task/sequence_manager/thread_controller_impl.cc:166:21
    #22 0x7f198fe3b992 in Run ./../../base/callback.h:99:12
    #23 0x7f198fe3b992 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/debug/task_annotator.cc:101:0
    #24 0x7f198feca3ca in base::MessageLoop::RunTask(base::PendingTask*) ./../../base/message_loop/message_loop.cc:351:25
    #25 0x7f198fecbcad in DeferOrRunPendingTask ./../../base/message_loop/message_loop.cc:361:5
    #26 0x7f198fecbcad in base::MessageLoop::DoWork() ./../../base/message_loop/message_loop.cc:419:0
    #27 0x7f198fed2c8c in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:37:31
    #28 0x7f198ff72ec2 in base::RunLoop::Run() ./../../base/run_loop.cc:102:14
    #29 0x7f1990080f39 in base::Thread::ThreadMain() ./../../base/threading/thread.cc:337:3
    #30 0x7f19901801f6 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:76:13
    #31 0x7f196542a494 in start_thread ??:0:0
    #32 0x7f1961084a8f in clone ??:0:0
  r8: 0000000000641184  r9: 00007f1921ae35df r10: 00000c2a80010e20 r11: 00006150000c6f00
 r12: 00000fe3a54b8bd0 r13: f8f8f8f8f8f8f8f8 r14: 00000fdda3e3d52f r15: 00007eed1f1ea900
  di: 00007f196a074b28  si: 0000000000000001  bp: 00007f192a605e30  bx: 0000000000000038
  dx: 00007f194b22c000  ax: 0000000000000007  cx: 00000000002fc780  sp: 00007f192a605e20
  ip: 00007f19695ed489 efl: 0000000000010246 cgf: 002b000000000033 erf: 0000000000000004
 trp: 000000000000000e msk: 0000000000000000 cr2: 0000000000000038
[end of stack trace]


### rt...@chromium.org (2018-07-09)

Oh, this backtrace in c#2 is on Linux, not Windows. Haven't tried windows.

### cl...@chromium.org (2018-07-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5426280795996160.

### es...@chromium.org (2018-07-11)

Clusterfuzz is getting a null dereference instead of a UaF, but I'm going to tentatively assign this Medium based on the original report.

### es...@chromium.org (2018-07-11)

(er, should in fact be High if it's really a UaF)

### sh...@chromium.org (2018-07-12)

[Empty comment from Monorail migration]

### rt...@chromium.org (2018-07-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-07-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ca1156974cbe707fd023a00ae62104528833a44e

commit ca1156974cbe707fd023a00ae62104528833a44e
Author: Raymond Toy <rtoy@chromium.org>
Date: Tue Jul 17 01:20:11 2018

Audio thread should not access destination node

The AudioDestinationNode is an object managed by Oilpan so the audio
thread should not access it.  However, the audio thread needs
information (currentTime, etc) from the destination node. So instead
of accessing the audio destination handler (a scoped_refptr) via the
destination node, add a new member to the base audio context that
holds onto the destination handler.

The destination handler is not an oilpan object and lives at least as
long as the base audio context.

Bug: 860626, 860522, 863951
Test: Test case from 860522 doesn't crash on asan build
Change-Id: I3add844d4eb8fdc7e05b89292938b843a0abbb99
Reviewed-on: https://chromium-review.googlesource.com/1138974
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Cr-Commit-Position: refs/heads/master@{#575509}
[modify] https://crrev.com/ca1156974cbe707fd023a00ae62104528833a44e/third_party/blink/renderer/modules/webaudio/base_audio_context.cc
[modify] https://crrev.com/ca1156974cbe707fd023a00ae62104528833a44e/third_party/blink/renderer/modules/webaudio/base_audio_context.h


### rt...@chromium.org (2018-07-17)

Crash mentioned in c#3 no longer reproduces with ToT (after fix in c#9).  I let it run for about 10 minutes with no issues.

### rt...@chromium.org (2018-07-20)

cdsrc2016: Can you retry with a canary build? I cannot reproduce the V8InterruptCallback issue or the AudioNode::Handler() issue in c#3.

### rt...@chromium.org (2018-07-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### me...@google.com (2018-07-27)

cdsrc2016: Another ping from the security sheriff -- Can you please retry on Canary? 

### cd...@gmail.com (2018-07-28)

I tested it more than 10 times in the new asan build(Version 70.0.3503.0 (Developer Build) (64-bit)) ,and no any crash reproduced.;)

### cl...@chromium.org (2018-07-30)

Detailed report: <https://clusterfuzz.com/testcase?key=5426280795996160>

Job Type: linux\_asan\_chrome\_mp  

Platform Id: linux

Crash Type: Null-dereference READ  

Crash Address: 0x000000000038  

Crash State:  

blink::AudioNode::Handler  

blink::AudioDestinationNode::GetAudioDestinationHandler  

blink::AudioHandler::ProcessIfNecessary

Sanitizer: address (ASAN)

Reproducer Testcase: <https://clusterfuzz.com/download?testcase_id=5426280795996160>

Additional requirements: Requires HTTP

See <https://github.com/google/clusterfuzz-tools> for more information.

**Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days we've been seeing this crash frequently. If you are unable to reproduce this, please try a speculative fix based on the crash stacktrace in the report. The fix can be verified by looking at the crash statistics in the report, a day after the fix is deployed. We will auto-close the bug if the crash is not seen for 14 days.**

### rt...@chromium.org (2018-07-30)

cdsrc2016: Thanks for testing and confirming the fix works!

The clusterfuzz report in c#17 is for rev 573804, before the fix in c#10 (rev 575509)  Clusterfuzz can't reproduce 573804 but is apparently testing 576414 which should have the fix.

I'll wait a bit to see what clusterfuzz has to say.

### cl...@chromium.org (2018-07-30)

Detailed report: <https://clusterfuzz.com/testcase?key=5426280795996160>

Job Type: linux\_asan\_chrome\_mp  

Platform Id: linux

Crash Type: Null-dereference READ  

Crash Address: 0x000000000038  

Crash State:  

blink::AudioNode::Handler  

blink::AudioDestinationNode::GetAudioDestinationHandler  

blink::AudioHandler::ProcessIfNecessary

Sanitizer: address (ASAN)

Reproducer Testcase: <https://clusterfuzz.com/download?testcase_id=5426280795996160>

Additional requirements: Requires HTTP

See <https://github.com/google/clusterfuzz-tools> for more information.

**Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days we've been seeing this crash frequently. If you are unable to reproduce this, please try a speculative fix based on the crash stacktrace in the report. The fix can be verified by looking at the crash statistics in the report, a day after the fix is deployed. We will auto-close the bug if the crash is not seen for 14 days.**

### rt...@chromium.org (2018-07-30)

+inferno:  What should I do here?  clusterfuzz can't check to see if it's been fixed and still reports r573804 as being flaky.  The fix landed in r575509 and the backtrace can't include GetAudioDestinationHandler because CurrentSampleFrame no longer calls that.

### aa...@google.com (2018-07-30)

This no longer shows up in crash stats, marking as fixed. c#17, c#19 are caused by a recent change, where we were not updating bugs after upload when testcase status = duplicate.

### rt...@chromium.org (2018-07-30)

Thanks!

### sh...@chromium.org (2018-07-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-03)

This bug requires manual review: M69 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-08-03)

[Comment Deleted]

### go...@chromium.org (2018-08-03)

Cl listed at #10 is already in M69 branch #3497, branched at chromium revision 576753.

Is there any other merge needed for M69?

### go...@chromium.org (2018-08-03)

Rejecting merge to M69 per https://crbug.com/chromium/860522#c27.

### aw...@chromium.org (2018-08-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-08-13)

Hi cdsrc2016@, thanks for the report and the followup - the VRP panel decided to give $500. Cheers!

### aw...@google.com (2018-08-13)

[Empty comment from Monorail migration]

### cd...@gmail.com (2018-08-14)

Thanks :)

### aw...@google.com (2018-08-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wn...@gmail.com (2018-11-27)

Hello, I have a problem when reproduce the exploit
﻿```
Uncaught TypeError: Cannot read property 'addModule' of undefined
```

Should I do some changes to the poc.html or add some code such like import `.js` file?
﻿
﻿
﻿



### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/860522?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091851)*
