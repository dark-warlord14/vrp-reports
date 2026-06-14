# use-after-free in operator-> buildtools/third_party/libc++/trunk/include/memory (WebAudio thread)

| Field | Value |
|-------|-------|
| **Issue ID** | [40091681](https://issues.chromium.org/issues/40091681) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebAudio, Blink>Workers |
| **Platforms** | Linux |
| **Reporter** | cd...@gmail.com |
| **Assignee** | nh...@chromium.org |
| **Created** | 2018-06-17 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36

Steps to reproduce the problem:
Version 69.0.3451.0 (Developer Build) (64-bit)

use-after-free in operator-> buildtools/third_party/libc++/trunk/include/memory (WebAudio thread)
1.Get new version chrome:
 a) Build source code 
    config args.gn file as below:
		use_sanitizer_coverage = true
		is_asan = true
		is_debug = false
		enable_nacl = false
		treat_warnings_as_errors = false
	ninja -j16 -C out/chrome_asan chrome
2.python3.5m -m http.server 8605

3 ./crhome ./crash.html
	Click  "go back" button(top left corner) several times(repro about 3~5 times in my test).

What is the expected behavior?

What went wrong?
=================================================================
==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x61100008da08 at pc 0x55d543ee56e1 bp 0x7fcc74532390 sp 0x7fcc74532388
READ of size 8 at 0x61100008da08 thread T21 (WebAudio thread)
    #0 0x55d543ee56e0 in operator-> /home/cowboy/chromium/src/out/chrome_asan_shared/../../buildtools/third_party/libc++/trunk/include/memory:2603:19
    #1 0x55d543ee56e0 in blink::WorkerThread::PerformShutdownOnWorkerThread() /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/workers/worker_thread.cc:562:0
    #2 0x55d540721da5 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:136:12
    #3 0x55d540721da5 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/wtf/functional.h:320:0
    #4 0x55d540721da5 in blink::(anonymous namespace)::RunCrossThreadClosure(WTF::CrossThreadFunction<void ()>) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/web_task_runner.cc:15:0
    #5 0x55d540722c2d in Invoke<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> > /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:407:12
    #6 0x55d540722c2d in MakeItSo<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> > /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:607:0
    #7 0x55d540722c2d in RunImpl<void (*)(WTF::CrossThreadFunction<void ()>), std::__1::tuple<WTF::CrossThreadFunction<void ()> >, 0> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:681:0
    #8 0x55d540722c2d in base::internal::Invoker<base::internal::BindState<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> >, void ()>::RunOnce(base::internal::BindStateBase*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:649:0
    #9 0x55d537b0c2d8 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:96:12
    #10 0x55d537b0c2d8 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #11 0x55d536a50297 in base::sequence_manager::internal::ThreadControllerImpl::DoWork(base::sequence_manager::internal::ThreadControllerImpl::WorkType) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/scheduler/base/thread_controller_impl.cc:166:21
    #12 0x55d537b0c2d8 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:96:12
    #13 0x55d537b0c2d8 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #14 0x55d537b6ba12 in base::MessageLoop::RunTask(base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:319:25
    #15 0x55d537b6cc8f in DeferOrRunPendingTask /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:329:5
    #16 0x55d537b6cc8f in base::MessageLoop::DoWork() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:373:0
    #17 0x55d537b755ef in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_pump_default.cc:37:31
    #18 0x55d537be6dc0 in base::RunLoop::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/run_loop.cc:102:14
    #19 0x55d537c71000 in base::Thread::ThreadMain() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/thread.cc:337:3
    #20 0x55d537d2a050 in base::(anonymous namespace)::ThreadFunc(void*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/platform_thread_posix.cc:76:13
    #21 0x7fcc969fb6b9 in start_thread ??:0:0

0x61100008da08 is located 200 bytes inside of 256-byte region [0x61100008d940,0x61100008da40)
freed by thread T0 (chrome) here:
    #0 0x55d530559bd2 in operator delete(void*) _asan_rtl_:3
    #1 0x55d543eaca64 in operator() /home/cowboy/chromium/src/out/chrome_asan_shared/../../buildtools/third_party/libc++/trunk/include/memory:2321:5
    #2 0x55d543eaca64 in reset /home/cowboy/chromium/src/out/chrome_asan_shared/../../buildtools/third_party/libc++/trunk/include/memory:2634:0
    #3 0x55d543eaca64 in ~unique_ptr /home/cowboy/chromium/src/out/chrome_asan_shared/../../buildtools/third_party/libc++/trunk/include/memory:2588:0
    #4 0x55d543eaca64 in blink::ThreadedMessagingProxyBase::WorkerThreadTerminated() /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/workers/threaded_messaging_proxy_base.cc:164:0
    #5 0x55d543eb163f in Invoke<void (blink::ThreadedMessagingProxyBase::*)(), blink::CrossThreadPersistent<blink::ThreadedMessagingProxyBase>> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:507:12
    #6 0x55d543eb163f in MakeItSo<void (blink::ThreadedMessagingProxyBase::*const &)(), blink::CrossThreadPersistent<blink::ThreadedMessagingProxyBase>> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:627:0
    #7 0x55d543eb163f in void base::internal::Invoker<base::internal::BindState<void (blink::ThreadedMessagingProxyBase::*)(), blink::CrossThreadWeakPersistent<blink::ThreadedMessagingProxyBase> >, void ()>::RunImpl<void (blink::ThreadedMessagingProxyBase::* const&)(), std::__1::tuple<blink::CrossThreadWeakPersistent<blink::ThreadedMessagingProxyBase> > const&, 0ul>(void (blink::ThreadedMessagingProxyBase::* const&&&)(), std::__1::tuple<blink::CrossThreadWeakPersistent<blink::ThreadedMessagingProxyBase> > const&&&, std::__1::integer_sequence<unsigned long, 0ul>) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:681:0
    #8 0x55d540721da5 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:136:12
    #9 0x55d540721da5 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/wtf/functional.h:320:0
    #10 0x55d540721da5 in blink::(anonymous namespace)::RunCrossThreadClosure(WTF::CrossThreadFunction<void ()>) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/web_task_runner.cc:15:0
    #11 0x55d540722c2d in Invoke<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> > /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:407:12
    #12 0x55d540722c2d in MakeItSo<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> > /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:607:0
    #13 0x55d540722c2d in RunImpl<void (*)(WTF::CrossThreadFunction<void ()>), std::__1::tuple<WTF::CrossThreadFunction<void ()> >, 0> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:681:0
    #14 0x55d540722c2d in base::internal::Invoker<base::internal::BindState<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> >, void ()>::RunOnce(base::internal::BindStateBase*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:649:0
    #15 0x55d537b0c2d8 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:96:12
    #16 0x55d537b0c2d8 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #17 0x55d536a50297 in base::sequence_manager::internal::ThreadControllerImpl::DoWork(base::sequence_manager::internal::ThreadControllerImpl::WorkType) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/scheduler/base/thread_controller_impl.cc:166:21
    #18 0x55d537b0c2d8 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:96:12
    #19 0x55d537b0c2d8 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #20 0x55d537b6ba12 in base::MessageLoop::RunTask(base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:319:25
    #21 0x55d537b6cc8f in DeferOrRunPendingTask /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:329:5
    #22 0x55d537b6cc8f in base::MessageLoop::DoWork() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:373:0
    #23 0x55d537b755ef in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_pump_default.cc:37:31
    #24 0x55d537be6dc0 in base::RunLoop::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/run_loop.cc:102:14
    #25 0x55d546a52635 in content::RendererMain(content::MainFunctionParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/renderer/renderer_main.cc:218:23
    #26 0x55d5370a8695 in content::RunZygote(content::ContentMainDelegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:567:14
    #27 0x55d5370ac18d in content::ContentMainRunnerImpl::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:969:10
    #28 0x55d5370cbc63 in service_manager::Main(service_manager::MainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../services/service_manager/embedder/main.cc:459:29
    #29 0x55d5370a6ca7 in content::ContentMain(content::ContentMainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main.cc:19:10
    #30 0x55d53055c6ef in ChromeMain /home/cowboy/chromium/src/out/chrome_asan_shared/../../chrome/app/chrome_main.cc:101:12
    #31 0x7fcc8fc6782f in __libc_start_main /build/glibc-Cl5G7W/glibc-2.23/csu/../csu/libc-start.c:291:0

previously allocated by thread T0 (chrome) here:
    #0 0x55d530558f92 in operator new(unsigned long) _asan_rtl_:3
    #1 0x55d545fd46c6 in blink::AudioWorkletThread::Create(blink::ThreadableLoadingContext*, blink::WorkerReportingProxy&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet_thread.cc:36:7
    #2 0x55d545fcfd03 in blink::AudioWorkletMessagingProxy::CreateWorkerThread() /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet_messaging_proxy.cc:96:10
    #3 0x55d543eabb0a in blink::ThreadedMessagingProxyBase::InitializeWorkerThread(std::__1::unique_ptr<blink::GlobalScopeCreationParams, std::__1::default_delete<blink::GlobalScopeCreationParams> >, base::Optional<blink::WorkerBackingThreadStartupData> const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/workers/threaded_messaging_proxy_base.cc:95:20
    #4 0x55d54601ba77 in blink::ThreadedWorkletMessagingProxy::Initialize(blink::WorkerClients*, blink::WorkletModuleResponsesMap*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/workers/threaded_worklet_messaging_proxy.cc:70:3
    #5 0x55d545fcd1a1 in blink::AudioWorklet::CreateGlobalScope() /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet.cc:82:10
    #6 0x55d543ef2ae8 in blink::Worklet::FetchAndInvokeScript(blink::KURL const&, blink::WorkletOptions const&, blink::WorkletPendingTasks*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/workers/worklet.cc:145:24
    #7 0x55d537b0c2d8 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:96:12
    #8 0x55d537b0c2d8 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #9 0x55d536a50297 in base::sequence_manager::internal::ThreadControllerImpl::DoWork(base::sequence_manager::internal::ThreadControllerImpl::WorkType) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/scheduler/base/thread_controller_impl.cc:166:21
    #10 0x55d537b0c2d8 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:96:12
    #11 0x55d537b0c2d8 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #12 0x55d537b6ba12 in base::MessageLoop::RunTask(base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:319:25
    #13 0x55d537b6cc8f in DeferOrRunPendingTask /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:329:5
    #14 0x55d537b6cc8f in base::MessageLoop::DoWork() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:373:0
    #15 0x55d537b755ef in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_pump_default.cc:37:31
    #16 0x55d537be6dc0 in base::RunLoop::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/run_loop.cc:102:14
    #17 0x55d546a52635 in content::RendererMain(content::MainFunctionParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/renderer/renderer_main.cc:218:23
    #18 0x55d5370a8695 in content::RunZygote(content::ContentMainDelegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:567:14
    #19 0x55d5370ac18d in content::ContentMainRunnerImpl::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:969:10
    #20 0x55d5370cbc63 in service_manager::Main(service_manager::MainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../services/service_manager/embedder/main.cc:459:29
    #21 0x55d5370a6ca7 in content::ContentMain(content::ContentMainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main.cc:19:10
    #22 0x55d53055c6ef in ChromeMain /home/cowboy/chromium/src/out/chrome_asan_shared/../../chrome/app/chrome_main.cc:101:12
    #23 0x7fcc8fc6782f in __libc_start_main /build/glibc-Cl5G7W/glibc-2.23/csu/../csu/libc-start.c:291:0

Thread T21 (WebAudio thread) created by T0 (chrome) here:
    #0 0x55d530515b7d in __interceptor_pthread_create _asan_rtl_:3
    #1 0x55d537d292ca in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, base::PlatformThreadHandle*, base::ThreadPriority) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/platform_thread_posix.cc:115:13
    #2 0x55d537c702c5 in base::Thread::StartWithOptions(base::Thread::Options const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/thread.cc:112:15
    #3 0x55d536a60463 in blink::scheduler::WebThreadImplForWorkerScheduler::WebThreadImplForWorkerScheduler(blink::WebThreadCreationParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/scheduler/child/webthread_impl_for_worker_scheduler.cc:30:27
    #4 0x55d536a5f753 in make_unique<blink::scheduler::WebThreadImplForWorkerScheduler, const blink::WebThreadCreationParams &> /home/cowboy/chromium/src/out/chrome_asan_shared/../../buildtools/third_party/libc++/trunk/include/memory:3114:32
    #5 0x55d536a5f753 in blink::scheduler::WebThreadBase::CreateWorkerThread(blink::WebThreadCreationParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/scheduler/child/webthread_base.cc:134:0
    #6 0x55d5402f5a45 in content::BlinkPlatformImpl::CreateWebAudioThread() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/child/blink_platform_impl.cc:385:7
    #7 0x55d545fd4769 in EnsureSharedBackingThread /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet_thread.cc:79:46
    #8 0x55d545fd4769 in AudioWorkletThread /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet_thread.cc:45:0
    #9 0x55d545fd4769 in blink::AudioWorkletThread::Create(blink::ThreadableLoadingContext*, blink::WorkerReportingProxy&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet_thread.cc:36:0
    #10 0x55d545fcfd03 in blink::AudioWorkletMessagingProxy::CreateWorkerThread() /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet_messaging_proxy.cc:96:10
    #11 0x55d543eabb0a in blink::ThreadedMessagingProxyBase::InitializeWorkerThread(std::__1::unique_ptr<blink::GlobalScopeCreationParams, std::__1::default_delete<blink::GlobalScopeCreationParams> >, base::Optional<blink::WorkerBackingThreadStartupData> const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/workers/threaded_messaging_proxy_base.cc:95:20
    #12 0x55d54601ba77 in blink::ThreadedWorkletMessagingProxy::Initialize(blink::WorkerClients*, blink::WorkletModuleResponsesMap*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/workers/threaded_worklet_messaging_proxy.cc:70:3
    #13 0x55d545fcd1a1 in blink::AudioWorklet::CreateGlobalScope() /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet.cc:82:10
    #14 0x55d543ef2ae8 in blink::Worklet::FetchAndInvokeScript(blink::KURL const&, blink::WorkletOptions const&, blink::WorkletPendingTasks*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/workers/worklet.cc:145:24
    #15 0x55d537b0c2d8 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:96:12
    #16 0x55d537b0c2d8 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #17 0x55d536a50297 in base::sequence_manager::internal::ThreadControllerImpl::DoWork(base::sequence_manager::internal::ThreadControllerImpl::WorkType) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/scheduler/base/thread_controller_impl.cc:166:21
    #18 0x55d537b0c2d8 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:96:12
    #19 0x55d537b0c2d8 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #20 0x55d537b6ba12 in base::MessageLoop::RunTask(base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:319:25
    #21 0x55d537b6cc8f in DeferOrRunPendingTask /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:329:5
    #22 0x55d537b6cc8f in base::MessageLoop::DoWork() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:373:0
    #23 0x55d537b755ef in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_pump_default.cc:37:31
    #24 0x55d537be6dc0 in base::RunLoop::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/run_loop.cc:102:14
    #25 0x55d546a52635 in content::RendererMain(content::MainFunctionParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/renderer/renderer_main.cc:218:23
    #26 0x55d5370a8695 in content::RunZygote(content::ContentMainDelegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:567:14
    #27 0x55d5370ac18d in content::ContentMainRunnerImpl::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:969:10
    #28 0x55d5370cbc63 in service_manager::Main(service_manager::MainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../services/service_manager/embedder/main.cc:459:29
    #29 0x55d5370a6ca7 in content::ContentMain(content::ContentMainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main.cc:19:10
    #30 0x55d53055c6ef in ChromeMain /home/cowboy/chromium/src/out/chrome_asan_shared/../../chrome/app/chrome_main.cc:101:12
    #31 0x7fcc8fc6782f in __libc_start_main /build/glibc-Cl5G7W/glibc-2.23/csu/../csu/libc-start.c:291:0

SUMMARY: AddressSanitizer: heap-use-after-free (/home/cowboy/chromium/src/out/chrome_asan_shared/chrome+0x1b48a6e0)
Shadow bytes around the buggy address:
  0x0c2280009af0: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x0c2280009b00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2280009b10: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2280009b20: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c2280009b30: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0c2280009b40: fd[fd]fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x0c2280009b50: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2280009b60: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa
  0x0c2280009b70: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c2280009b80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2280009b90: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
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
    #0 0x55d5304d2c31 in __interceptor_backtrace /b/build/slave/linux_upload_clang/build/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:3980:13
    #1 0x55d537cfad1e in base::debug::StackTrace::StackTrace(unsigned long) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/stack_trace_posix.cc:808:41
    #2 0x55d537cf9c6d in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/stack_trace_posix.cc:334:3
    #3 0x7fcc96a05390 in __funlockfile ??:?
    #4 0x7fcc96a05390 in ?? ??:0
    #5 0x7fcc8fc7c428 in gsignal /build/glibc-Cl5G7W/glibc-2.23/signal/../sysdeps/unix/sysv/linux/raise.c:54:0
    #6 0x7fcc8fc7e02a in abort /build/glibc-Cl5G7W/glibc-2.23/stdlib/abort.c:89:0
    #7 0x55d5305483f7 in __sanitizer::Abort() /b/build/slave/linux_upload_clang/build/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_posix_libcdep.cc:151:3
    #8 0x55d530546e61 in __sanitizer::Die() /b/build/slave/linux_upload_clang/build/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_termination.cc:59:5
    #9 0x55d530533279 in __asan::ScopedInErrorReport::~ScopedInErrorReport() _asan_rtl_:7
    #10 0x55d530532773 in __asan::ReportGenericError(unsigned long, unsigned long, unsigned long, unsigned long, bool, unsigned long, unsigned int, bool) _asan_rtl_:1
    #11 0x55d53053363b in __asan_report_load8 _asan_rtl_:1
    #12 0x55d543ee56e1 in operator-> /home/cowboy/chromium/src/out/chrome_asan_shared/../../buildtools/third_party/libc++/trunk/include/memory:2603:19
    #13 0x55d543ee56e1 in blink::WorkerThread::PerformShutdownOnWorkerThread() /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/workers/worker_thread.cc:562:0
    #14 0x55d540721da6 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:136:12
    #15 0x55d540721da6 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/wtf/functional.h:320:0
    #16 0x55d540721da6 in blink::(anonymous namespace)::RunCrossThreadClosure(WTF::CrossThreadFunction<void ()>) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/web_task_runner.cc:15:0
    #17 0x55d540722c2e in Invoke<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> > /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:407:12
    #18 0x55d540722c2e in MakeItSo<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> > /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:607:0
    #19 0x55d540722c2e in RunImpl<void (*)(WTF::CrossThreadFunction<void ()>), std::__1::tuple<WTF::CrossThreadFunction<void ()> >, 0> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:681:0
    #20 0x55d540722c2e in base::internal::Invoker<base::internal::BindState<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> >, void ()>::RunOnce(base::internal::BindStateBase*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:649:0
    #21 0x55d537b0c2d9 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:96:12
    #22 0x55d537b0c2d9 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #23 0x55d536a50298 in base::sequence_manager::internal::ThreadControllerImpl::DoWork(base::sequence_manager::internal::ThreadControllerImpl::WorkType) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/scheduler/base/thread_controller_impl.cc:166:21
    #24 0x55d537b0c2d9 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:96:12
    #25 0x55d537b0c2d9 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #26 0x55d537b6ba13 in base::MessageLoop::RunTask(base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:319:25
    #27 0x55d537b6cc90 in DeferOrRunPendingTask /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:329:5
    #28 0x55d537b6cc90 in base::MessageLoop::DoWork() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:373:0
    #29 0x55d537b755f0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_pump_default.cc:37:31
    #30 0x55d537be6dc1 in base::RunLoop::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/run_loop.cc:102:14
    #31 0x55d537c71001 in base::Thread::ThreadMain() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/thread.cc:337:3
    #32 0x55d537d2a051 in base::(anonymous namespace)::ThreadFunc(void*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/platform_thread_posix.cc:76:13
    #33 0x7fcc969fb6ba in start_thread ??:0:0
    #34 0x7fcc8fd4e41d in clone /build/glibc-Cl5G7W/glibc-2.23/misc/../sysdeps/unix/sysv/linux/x86_64/clone.S:109:0
  r8: 000000000000dc0d  r9: 0000000000000000 r10: 0000000000000008 r11: 0000000000000202
 r12: 0000000000000000 r13: 00007fcc74532388 r14: 00007fcc74532330 r15: 000055d549d3b758
  di: 0000000000000001  si: 0000000000000016  bp: 00007fcc74532360  bx: 000055d549ca92a0
  dx: 0000000000000006  ax: 0000000000000000  cx: 00007fcc8fc7c428  sp: 00007fcc745314e8
  ip: 00007fcc8fc7c428 efl: 0000000000000202 cgf: 002b000000000033 erf: 0000000000000000
 trp: 0000000000000000 msk: 0000000000000000 cr2: 0000000000000000
[end of stack trace]
Calling _exit(1). Core file will not be generated.

Did this work before? N/A 

Chrome version: Version 69.0.3451.0 (Developer Build) (64-bit)  Channel: dev
OS Version: Ubuntu16.04
Flash Version: Shockwave Flash 30.0 r0

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [original_fuzz.html](attachments/original_fuzz.html) (text/plain, 1.7 KB)
- [uaf_symbolised2.log](attachments/uaf_symbolised2.log) (text/plain, 40.6 KB)
- deleted (application/octet-stream, 0 B)
- [audio-worklet.wasmmodule.js](attachments/audio-worklet.wasmmodule.js) (text/plain, 160.4 KB)
- [repro.mp4](attachments/repro.mp4) (video/mp4, 5.7 MB)
- [crash3.html](attachments/crash3.html) (text/plain, 351 B)
- [crash4.html](attachments/crash4.html) (text/plain, 351 B)
- [back.html](attachments/back.html) (text/plain, 100 B)
- [crash4.html](attachments/crash4_53054013.html) (text/plain, 355 B)
- [back.html](attachments/back_53054016.html) (text/plain, 129 B)
- [new.zip](attachments/new.zip) (application/octet-stream, 59.7 KB)
- [new2.zip](attachments/new2.zip) (application/octet-stream, 33.3 KB)
- [new3.zip](attachments/new3.zip) (application/octet-stream, 8.4 MB)
- [back.html](attachments/back_53054292.html) (text/plain, 138 B)
- [UNKNOWN_ReadAV_windows_release.txt](attachments/UNKNOWN_ReadAV_windows_release.txt) (text/plain, 3.9 KB)

## Timeline

### cd...@gmail.com (2018-06-17)

I find that when I test with my original fuzzed file, occasionally repro another uaf.
I'm not sure same the two uaf logs are same root cause.
==22156==ERROR: AddressSanitizer: heap-use-after-free on address 0x61100050b388 at pc 0x55790f6a1c7b bp 0x7f0677294180 sp 0x7f0677294178
READ of size 8 at 0x61100050b388 thread T34 (WebAudio thread)
    #0 0x55790f6a1c7a in blink::PersistentBase<blink::AudioWorkletProcessor, (blink::WeaknessPersistentConfiguration)0, (blink::CrossThreadnessPersistentConfiguration)1>::IsHashTableDeletedValue() const /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/heap/persistent.h:102:12
    #1 0x55790f6a3ee7 in Initialize /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/heap/persistent.h:219:18
    #2 0x55790f6a3ee7 in blink::PersistentBase<blink::AudioWorkletProcessor, (blink::WeaknessPersistentConfiguration)0, (blink::CrossThreadnessPersistentConfiguration)1>::Assign(blink::AudioWorkletProcessor*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/heap/persistent.h:198:0
    #3 0x55790f69b642 in operator=<blink::AudioWorkletProcessor> /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/heap/persistent.h:130:5
    #4 0x55790f69b642 in operator=<blink::AudioWorkletProcessor> /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/heap/persistent.h:478:0
    #5 0x55790f69b642 in blink::AudioWorkletHandler::SetProcessorOnRenderThread(blink::AudioWorkletProcessor*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet_node.cc:170:0
    #6 0x55790f674f07 in blink::AudioWorkletMessagingProxy::CreateProcessorOnRenderingThread(blink::WorkerThread*, blink::AudioWorkletHandler*, WTF::String const&, blink::MessagePortChannel, scoped_refptr<blink::SerializedScriptValue>) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet_messaging_proxy.cc:53:12
    #7 0x55790f677d89 in Invoke<void (blink::AudioWorkletMessagingProxy::*)(blink::WorkerThread *, blink::AudioWorkletHandler *, const WTF::String &, blink::MessagePortChannel, scoped_refptr<blink::SerializedScriptValue>), const blink::CrossThreadPersistent<blink::AudioWorkletMessagingProxy> &, blink::WorkerThread *, blink::AudioWorkletHandler *, const WTF::String &, const blink::MessagePortChannel &, const scoped_refptr<blink::SerializedScriptValue> &> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:507:12
    #8 0x55790f677d89 in MakeItSo<void (blink::AudioWorkletMessagingProxy::*const &)(blink::WorkerThread *, blink::AudioWorkletHandler *, const WTF::String &, blink::MessagePortChannel, scoped_refptr<blink::SerializedScriptValue>), const blink::CrossThreadPersistent<blink::AudioWorkletMessagingProxy> &, blink::WorkerThread *, blink::AudioWorkletHandler *, const WTF::String &, const blink::MessagePortChannel &, const scoped_refptr<blink::SerializedScriptValue> &> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:607:0
    #9 0x55790f677d89 in RunImpl<void (blink::AudioWorkletMessagingProxy::*const &)(blink::WorkerThread *, blink::AudioWorkletHandler *, const WTF::String &, blink::MessagePortChannel, scoped_refptr<blink::SerializedScriptValue>), const std::__1::tuple<blink::CrossThreadPersistent<blink::AudioWorkletMessagingProxy>, WTF::CrossThreadUnretainedWrapper<blink::WorkerThread>, WTF::CrossThreadUnretainedWrapper<blink::AudioWorkletHandler>, WTF::String, blink::MessagePortChannel, scoped_refptr<blink::SerializedScriptValue> > &, 0, 1, 2, 3, 4, 5> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:681:0
    #10 0x55790f677d89 in base::internal::Invoker<base::internal::BindState<void (blink::AudioWorkletMessagingProxy::*)(blink::WorkerThread*, blink::AudioWorkletHandler*, WTF::String const&, blink::MessagePortChannel, scoped_refptr<blink::SerializedScriptValue>), blink::CrossThreadPersistent<blink::AudioWorkletMessagingProxy>, WTF::CrossThreadUnretainedWrapper<blink::WorkerThread>, WTF::CrossThreadUnretainedWrapper<blink::AudioWorkletHandler>, WTF::String, blink::MessagePortChannel, scoped_refptr<blink::SerializedScriptValue> >, void ()>::Run(base::internal::BindStateBase*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:663:0
    #11 0x557909dc7da5 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:136:12
    #12 0x557909dc7da5 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/wtf/functional.h:320:0
    #13 0x557909dc7da5 in blink::(anonymous namespace)::RunCrossThreadClosure(WTF::CrossThreadFunction<void ()>) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/web_task_runner.cc:15:0
    #14 0x557909dc8c2d in Invoke<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> > /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:407:12
    #15 0x557909dc8c2d in MakeItSo<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> > /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:607:0
    #16 0x557909dc8c2d in RunImpl<void (*)(WTF::CrossThreadFunction<void ()>), std::__1::tuple<WTF::CrossThreadFunction<void ()> >, 0> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:681:0
    #17 0x557909dc8c2d in base::internal::Invoker<base::internal::BindState<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> >, void ()>::RunOnce(base::internal::BindStateBase*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:649:0
    #18 0x5579011b22d8 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:96:12
    #19 0x5579011b22d8 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #20 0x5579000f6297 in base::sequence_manager::internal::ThreadControllerImpl::DoWork(base::sequence_manager::internal::ThreadControllerImpl::WorkType) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/scheduler/base/thread_controller_impl.cc:166:21
    #21 0x5579011b22d8 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:96:12
    #22 0x5579011b22d8 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #23 0x557901211a12 in base::MessageLoop::RunTask(base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:319:25
    #24 0x557901212c8f in DeferOrRunPendingTask /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:329:5
    #25 0x557901212c8f in base::MessageLoop::DoWork() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:373:0
    #26 0x55790121b5ef in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_pump_default.cc:37:31
    #27 0x55790128cdc0 in base::RunLoop::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/run_loop.cc:102:14
    #28 0x557901317000 in base::Thread::ThreadMain() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/thread.cc:337:3
    #29 0x5579013d0050 in base::(anonymous namespace)::ThreadFunc(void*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/platform_thread_posix.cc:76:13
    #30 0x7f06ae6b36b9 in start_thread ??:0:0

0x61100050b388 is located 136 bytes inside of 208-byte region [0x61100050b300,0x61100050b3d0)
freed by thread T0 (chrome) here:
    #0 0x5578f9bd2e02 in __interceptor_free _asan_rtl_:3
    #1 0x55790f69fb20 in DeleteInternal<blink::AudioHandler> /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/wtf/thread_safe_ref_counted.h:64:5
    #2 0x55790f69fb20 in Destruct /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/wtf/thread_safe_ref_counted.h:44:0
    #3 0x55790f69fb20 in Release /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/memory/ref_counted.h:387:0
    #4 0x55790f69fb20 in Release /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/memory/scoped_refptr.h:280:0
    #5 0x55790f69fb20 in ~scoped_refptr /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/memory/scoped_refptr.h:208:0
    #6 0x55790f69fb20 in ~AudioNode /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_node.h:313:0
    #7 0x55790f69fb20 in blink::AudioWorkletNode::~AudioWorkletNode() /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet_node.h:90:0
    #8 0x5578fff8a444 in Finalize /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/heap/heap_page.cc:103:5
    #9 0x5578fff8a444 in blink::NormalPage::Sweep() /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/heap/heap_page.cc:1370:0
    #10 0x5578fff83c10 in SweepUnsweptPage /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/heap/heap_page.cc:290:11
    #11 0x5578fff83c10 in blink::BaseArena::CompleteSweep() /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/heap/heap_page.cc:345:0
    #12 0x5578fff6f647 in blink::ThreadHeap::CompleteSweep() /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/heap/heap.cc:539:17
    #13 0x5578fff9742d in blink::ThreadState::CompleteSweep() /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/heap/thread_state.cc:988:12
    #14 0x5578fff88b92 in blink::NormalPageArena::OutOfLineAllocate(unsigned long, unsigned long) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/heap/heap_page.cc:938:21
    #15 0x5578fffd4b7d in AllocateObject /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/heap/heap_page.h:1050:10
    #16 0x5578fffd4b7d in blink::ThreadHeap::AllocateOnArenaIndex(blink::ThreadState*, unsigned long, int, unsigned long, char const*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/heap/heap.h:668:0
    #17 0x55790b9ef613 in AllocateHashTableBacking<WTF::KeyValuePair<int, blink::Member<blink::DOMTimer> >, WTF::HashTable<int, WTF::KeyValuePair<int, blink::Member<blink::DOMTimer> >, WTF::KeyValuePairKeyExtractor, WTF::IntHash<unsigned int>, WTF::HashMapValueTraits<WTF::HashTraits<int>, WTF::HashTraits<blink::Member<blink::DOMTimer> > >, WTF::HashTraits<int>, blink::HeapAllocator> > /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/heap/heap_allocator.h:121:47
    #18 0x55790b9ef613 in AllocateZeroedHashTableBacking<WTF::KeyValuePair<int, blink::Member<blink::DOMTimer> >, WTF::HashTable<int, WTF::KeyValuePair<int, blink::Member<blink::DOMTimer> >, WTF::KeyValuePairKeyExtractor, WTF::IntHash<unsigned int>, WTF::HashMapValueTraits<WTF::HashTraits<int>, WTF::HashTraits<blink::Member<blink::DOMTimer> > >, WTF::HashTraits<int>, blink::HeapAllocator> > /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/heap/heap_allocator.h:126:0
    #19 0x55790b9ef613 in WTF::HashTable<int, WTF::KeyValuePair<int, blink::Member<blink::DOMTimer> >, WTF::KeyValuePairKeyExtractor, WTF::IntHash<unsigned int>, WTF::HashMapValueTraits<WTF::HashTraits<int>, WTF::HashTraits<blink::Member<blink::DOMTimer> > >, WTF::HashTraits<int>, blink::HeapAllocator>::AllocateTable(unsigned int) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/wtf/hash_table.h:1586:0
    #20 0x55790b9f0864 in Rehash /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/wtf/hash_table.h:1807:26
    #21 0x55790b9f0864 in Shrink /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/wtf/hash_table.h:855:0
    #22 0x55790b9f0864 in WTF::HashTable<int, WTF::KeyValuePair<int, blink::Member<blink::DOMTimer> >, WTF::KeyValuePairKeyExtractor, WTF::IntHash<unsigned int>, WTF::HashMapValueTraits<WTF::HashTraits<int>, WTF::HashTraits<blink::Member<blink::DOMTimer> > >, WTF::HashTraits<int>, blink::HeapAllocator>::erase(WTF::KeyValuePair<int, blink::Member<blink::DOMTimer> > const*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/wtf/hash_table.h:1511:0
    #23 0x55790b9edb38 in erase /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/wtf/hash_table.h:1526:3
    #24 0x55790b9edb38 in erase /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/wtf/hash_map.h:613:0
    #25 0x55790b9edb38 in WTF::HashMap<int, blink::Member<blink::DOMTimer>, WTF::IntHash<unsigned int>, WTF::HashTraits<int>, WTF::HashTraits<blink::Member<blink::DOMTimer> >, blink::HeapAllocator>::Take(int const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/wtf/hash_map.h:647:0
    #26 0x55790b9ed844 in blink::DOMTimerCoordinator::RemoveTimeoutByID(int) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/frame/dom_timer_coordinator.cc:36:37
    #27 0x55790b9f25e1 in blink::DOMTimer::Fired() /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/frame/dom_timer.cc:174:22
    #28 0x557909db385b in blink::TimerBase::RunInternal() /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/timer.cc:160:3
    #29 0x5579011b22d8 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:96:12
    #30 0x5579011b22d8 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #31 0x5579000f6297 in base::sequence_manager::internal::ThreadControllerImpl::DoWork(base::sequence_manager::internal::ThreadControllerImpl::WorkType) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/scheduler/base/thread_controller_impl.cc:166:21
    #32 0x5579011b22d8 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:96:12
    #33 0x5579011b22d8 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #34 0x557901211a12 in base::MessageLoop::RunTask(base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:319:25
    #35 0x557901212c8f in DeferOrRunPendingTask /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:329:5
    #36 0x557901212c8f in base::MessageLoop::DoWork() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:373:0
    #37 0x55790121b5ef in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_pump_default.cc:37:31
    #38 0x55790128cdc0 in base::RunLoop::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/run_loop.cc:102:14
    #39 0x5579100f8635 in content::RendererMain(content::MainFunctionParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/renderer/renderer_main.cc:218:23
    #40 0x55790075218d in content::ContentMainRunnerImpl::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:969:10
    #41 0x557900771c63 in service_manager::Main(service_manager::MainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../services/service_manager/embedder/main.cc:459:29
    #42 0x55790074cca7 in content::ContentMain(content::ContentMainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main.cc:19:10
    #43 0x5578f9c026ef in ChromeMain /home/cowboy/chromium/src/out/chrome_asan_shared/../../chrome/app/chrome_main.cc:101:12
    #44 0x7f06a791d82f in __libc_start_main /build/glibc-Cl5G7W/glibc-2.23/csu/../csu/libc-start.c:291:0

previously allocated by thread T0 (chrome) here:
    #0 0x5578f9bd3143 in __interceptor_malloc _asan_rtl_:3
    #1 0x55790f699383 in PartitionAllocGenericFlags /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/allocator/partition_allocator/partition_alloc.h:318:18
    #2 0x55790f699383 in Alloc /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/allocator/partition_allocator/partition_alloc.h:338:0
    #3 0x55790f699383 in FastMalloc /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/wtf/allocator/partitions.h:121:0
    #4 0x55790f699383 in operator new /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/wtf/thread_safe_ref_counted.h:54:0
    #5 0x55790f699383 in blink::AudioWorkletHandler::Create(blink::AudioNode&, float, WTF::String, WTF::HashMap<WTF::String, scoped_refptr<blink::AudioParamHandler>, WTF::StringHash, WTF::HashTraits<WTF::String>, WTF::HashTraits<scoped_refptr<blink::AudioParamHandler> >, WTF::PartitionAllocator>, blink::AudioWorkletNodeOptions const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet_node.cc:78:0
    #6 0x55790f69caf7 in blink::AudioWorkletNode::AudioWorkletNode(blink::BaseAudioContext&, WTF::String const&, blink::AudioWorkletNodeOptions const&, WTF::Vector<blink::CrossThreadAudioParamInfo, 0ul, WTF::PartitionAllocator>, blink::MessagePort*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet_node.cc:243:14
    #7 0x55790f69d754 in blink::AudioWorkletNode::Create(blink::ScriptState*, blink::BaseAudioContext*, WTF::String const&, blink::AudioWorkletNodeOptions const&, blink::ExceptionState&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet_node.cc:321:11
    #8 0x55790f6b6386 in constructor /home/cowboy/chromium/src/out/chrome_asan_shared/gen/third_party/blink/renderer/bindings/modules/v8/v8_audio_worklet_node.cc:169:28
    #9 0x55790f6b6386 in blink::V8AudioWorkletNode::constructorCallback(v8::FunctionCallbackInfo<v8::Value> const&) /home/cowboy/chromium/src/out/chrome_asan_shared/gen/third_party/blink/renderer/bindings/modules/v8/v8_audio_worklet_node.cc:226:0
    #10 0x5578fe7ed515 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../v8/src/api-arguments-inl.h:94:3
    #11 0x5578fe7e9dc2 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) /home/cowboy/chromium/src/out/chrome_asan_shared/../../v8/src/builtins/builtins-api.cc:109:36
    #12 0x5578fe7e879d in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../v8/src/builtins/builtins-api.cc:135:5
    #8 0x7ec8762d88fc  (<unknown module>)
    #9 0x7ec87628a305  (<unknown module>)
    #10 0x7ec87630c0a9  (<unknown module>)
    #11 0x7ec87628ea44  (<unknown module>)
    #12 0x7ec876287805  (<unknown module>)
    #13 0x7ec8762bf350  (<unknown module>)
    #14 0x7ec87629ca4b  (<unknown module>)
    #15 0x7ec876284d00  (<unknown module>)
    #13 0x5578ff06f38b in Call /home/cowboy/chromium/src/out/chrome_asan_shared/../../v8/src/simulator.h:113:12
    #14 0x5578ff06f38b in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, bool, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, v8::internal::Handle<v8::internal::Object>, v8::internal::Execution::MessageHandling, v8::internal::Execution::Target) /home/cowboy/chromium/src/out/chrome_asan_shared/../../v8/src/execution.cc:155:0
    #15 0x5578ff06fbc3 in CallInternal /home/cowboy/chromium/src/out/chrome_asan_shared/../../v8/src/execution.cc:191:10
    #16 0x5578ff06fbc3 in v8::internal::Execution::TryCall(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, v8::internal::Execution::MessageHandling, v8::internal::MaybeHandle<v8::internal::Object>*, v8::internal::Execution::Target) /home/cowboy/chromium/src/out/chrome_asan_shared/../../v8/src/execution.cc:241:0
    #17 0x5578ff06feec in v8::internal::Execution::RunMicrotasks(v8::internal::Isolate*, v8::internal::Execution::MessageHandling, v8::internal::MaybeHandle<v8::internal::Object>*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../v8/src/execution.cc:272:10
    #18 0x5578ff3b4fac in v8::internal::Isolate::RunMicrotasks() /home/cowboy/chromium/src/out/chrome_asan_shared/../../v8/src/isolate.cc:3925:40
    #19 0x55790b30865e in blink::Microtask::PerformCheckpoint(v8::Isolate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/bindings/microtask.cc:44:3
    #20 0x55790eceba5c in blink::(anonymous namespace)::EndOfTaskRunner::DidProcessTask() /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/controller/blink_initializer.cc:69:5
    #21 0x5579000ed519 in base::sequence_manager::TaskQueueManagerImpl::NotifyDidProcessTask(base::sequence_manager::TaskQueueManagerImpl::ExecutingTask const&, base::sequence_manager::LazyNow*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/scheduler/base/task_queue_manager_impl.cc:502:16
    #22 0x5579000eef66 in DidRunTask /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/scheduler/base/task_queue_manager_impl.cc:364:3
    #23 0x5579000eef66 in non-virtual thunk to base::sequence_manager::TaskQueueManagerImpl::DidRunTask() /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/scheduler/base/task_queue_manager_impl.cc:0:0
    #24 0x5579000f631c in base::sequence_manager::internal::ThreadControllerImpl::DoWork(base::sequence_manager::internal::ThreadControllerImpl::WorkType) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/scheduler/base/thread_controller_impl.cc:171:16
    #25 0x5579011b22d8 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:96:12
    #26 0x5579011b22d8 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #27 0x557901211a12 in base::MessageLoop::RunTask(base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:319:25
    #28 0x557901212c8f in DeferOrRunPendingTask /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:329:5
    #29 0x557901212c8f in base::MessageLoop::DoWork() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:373:0
    #30 0x55790121b5ef in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_pump_default.cc:37:31
    #31 0x55790128cdc0 in base::RunLoop::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/run_loop.cc:102:14

Thread T34 (WebAudio thread) created by T0 (chrome) here:
    #0 0x5578f9bbbb7d in __interceptor_pthread_create _asan_rtl_:3
    #1 0x5579013cf2ca in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, base::PlatformThreadHandle*, base::ThreadPriority) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/platform_thread_posix.cc:115:13
    #2 0x5579013162c5 in base::Thread::StartWithOptions(base::Thread::Options const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/thread.cc:112:15
    #3 0x557900106463 in blink::scheduler::WebThreadImplForWorkerScheduler::WebThreadImplForWorkerScheduler(blink::WebThreadCreationParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/scheduler/child/webthread_impl_for_worker_scheduler.cc:30:27
    #4 0x557900105753 in make_unique<blink::scheduler::WebThreadImplForWorkerScheduler, const blink::WebThreadCreationParams &> /home/cowboy/chromium/src/out/chrome_asan_shared/../../buildtools/third_party/libc++/trunk/include/memory:3114:32
    #5 0x557900105753 in blink::scheduler::WebThreadBase::CreateWorkerThread(blink::WebThreadCreationParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/scheduler/child/webthread_base.cc:134:0
    #6 0x55790999ba45 in content::BlinkPlatformImpl::CreateWebAudioThread() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/child/blink_platform_impl.cc:385:7
    #7 0x55790f67a769 in EnsureSharedBackingThread /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet_thread.cc:79:46
    #8 0x55790f67a769 in AudioWorkletThread /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet_thread.cc:45:0
    #9 0x55790f67a769 in blink::AudioWorkletThread::Create(blink::ThreadableLoadingContext*, blink::WorkerReportingProxy&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet_thread.cc:36:0
    #10 0x55790f675d03 in blink::AudioWorkletMessagingProxy::CreateWorkerThread() /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet_messaging_proxy.cc:96:10
    #11 0x55790d551b0a in blink::ThreadedMessagingProxyBase::InitializeWorkerThread(std::__1::unique_ptr<blink::GlobalScopeCreationParams, std::__1::default_delete<blink::GlobalScopeCreationParams> >, base::Optional<blink::WorkerBackingThreadStartupData> const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/workers/threaded_messaging_proxy_base.cc:95:20
    #12 0x55790f6c1a77 in blink::ThreadedWorkletMessagingProxy::Initialize(blink::WorkerClients*, blink::WorkletModuleResponsesMap*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/workers/threaded_worklet_messaging_proxy.cc:70:3
    #13 0x55790f6731a1 in blink::AudioWorklet::CreateGlobalScope() /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet.cc:82:10
    #14 0x55790d598ae8 in blink::Worklet::FetchAndInvokeScript(blink::KURL const&, blink::WorkletOptions const&, blink::WorkletPendingTasks*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/workers/worklet.cc:145:24
    #15 0x5579011b22d8 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:96:12
    #16 0x5579011b22d8 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #17 0x5579000f6297 in base::sequence_manager::internal::ThreadControllerImpl::DoWork(base::sequence_manager::internal::ThreadControllerImpl::WorkType) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/scheduler/base/thread_controller_impl.cc:166:21
    #18 0x5579011b22d8 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:96:12
    #19 0x5579011b22d8 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #20 0x557901211a12 in base::MessageLoop::RunTask(base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:319:25
    #21 0x557901212c8f in DeferOrRunPendingTask /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:329:5
    #22 0x557901212c8f in base::MessageLoop::DoWork() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:373:0
    #23 0x55790121b5ef in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_pump_default.cc:37:31
    #24 0x55790128cdc0 in base::RunLoop::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/run_loop.cc:102:14
    #25 0x5579100f8635 in content::RendererMain(content::MainFunctionParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/renderer/renderer_main.cc:218:23
    #26 0x55790075218d in content::ContentMainRunnerImpl::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:969:10
    #27 0x557900771c63 in service_manager::Main(service_manager::MainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../services/service_manager/embedder/main.cc:459:29
    #28 0x55790074cca7 in content::ContentMain(content::ContentMainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main.cc:19:10
    #29 0x5578f9c026ef in ChromeMain /home/cowboy/chromium/src/out/chrome_asan_shared/../../chrome/app/chrome_main.cc:101:12
    #30 0x7f06a791d82f in __libc_start_main /build/glibc-Cl5G7W/glibc-2.23/csu/../csu/libc-start.c:291:0

SUMMARY: AddressSanitizer: heap-use-after-free (/home/cowboy/chromium/src/out/chrome_asan_shared/chrome+0x1d5a0c7a)
Shadow bytes around the buggy address:
  0x0c2280099620: fd fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2280099630: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c2280099640: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2280099650: fd fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2280099660: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0c2280099670: fd[fd]fd fd fd fd fd fd fd fd fa fa fa fa fa fa
  0x0c2280099680: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c2280099690: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c22800996a0: fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c22800996b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c22800996c0: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa
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
==22156==ABORTING
Received signal 6
    #0 0x5578f9b78c31 in __interceptor_backtrace /b/build/slave/linux_upload_clang/build/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:3980:13
    #1 0x5579013a0d1e in base::debug::StackTrace::StackTrace(unsigned long) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/stack_trace_posix.cc:808:41
    #2 0x55790139fc6d in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/stack_trace_posix.cc:334:3
    #3 0x7f06ae6bd390 in __funlockfile ??:?
    #4 0x7f06ae6bd390 in ?? ??:0
    #5 0x7f06a7932428 in gsignal /build/glibc-Cl5G7W/glibc-2.23/signal/../sysdeps/unix/sysv/linux/raise.c:54:0
    #6 0x7f06a793402a in abort /build/glibc-Cl5G7W/glibc-2.23/stdlib/abort.c:89:0
    #7 0x5578f9bee3f7 in __sanitizer::Abort() /b/build/slave/linux_upload_clang/build/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_posix_libcdep.cc:151:3
    #8 0x5578f9bece61 in __sanitizer::Die() /b/build/slave/linux_upload_clang/build/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_termination.cc:59:5
    #9 0x5578f9bd9279 in __asan::ScopedInErrorReport::~ScopedInErrorReport() _asan_rtl_:7
    #10 0x5578f9bd8773 in __asan::ReportGenericError(unsigned long, unsigned long, unsigned long, unsigned long, bool, unsigned long, unsigned int, bool) _asan_rtl_:1
    #11 0x5578f9bd963b in __asan_report_load8 _asan_rtl_:1
    #12 0x55790f6a1c7b in blink::PersistentBase<blink::AudioWorkletProcessor, (blink::WeaknessPersistentConfiguration)0, (blink::CrossThreadnessPersistentConfiguration)1>::IsHashTableDeletedValue() const /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/heap/persistent.h:102:12
    #13 0x55790f6a3ee8 in Initialize /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/heap/persistent.h:219:18
    #14 0x55790f6a3ee8 in blink::PersistentBase<blink::AudioWorkletProcessor, (blink::WeaknessPersistentConfiguration)0, (blink::CrossThreadnessPersistentConfiguration)1>::Assign(blink::AudioWorkletProcessor*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/heap/persistent.h:198:0
    #15 0x55790f69b643 in operator=<blink::AudioWorkletProcessor> /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/heap/persistent.h:130:5
    #16 0x55790f69b643 in operator=<blink::AudioWorkletProcessor> /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/heap/persistent.h:478:0
    #17 0x55790f69b643 in blink::AudioWorkletHandler::SetProcessorOnRenderThread(blink::AudioWorkletProcessor*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet_node.cc:170:0
    #18 0x55790f674f08 in blink::AudioWorkletMessagingProxy::CreateProcessorOnRenderingThread(blink::WorkerThread*, blink::AudioWorkletHandler*, WTF::String const&, blink::MessagePortChannel, scoped_refptr<blink::SerializedScriptValue>) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet_messaging_proxy.cc:53:12
    #19 0x55790f677d8a in Invoke<void (blink::AudioWorkletMessagingProxy::*)(blink::WorkerThread *, blink::AudioWorkletHandler *, const WTF::String &, blink::MessagePortChannel, scoped_refptr<blink::SerializedScriptValue>), const blink::CrossThreadPersistent<blink::AudioWorkletMessagingProxy> &, blink::WorkerThread *, blink::AudioWorkletHandler *, const WTF::String &, const blink::MessagePortChannel &, const scoped_refptr<blink::SerializedScriptValue> &> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:507:12
    #20 0x55790f677d8a in MakeItSo<void (blink::AudioWorkletMessagingProxy::*const &)(blink::WorkerThread *, blink::AudioWorkletHandler *, const WTF::String &, blink::MessagePortChannel, scoped_refptr<blink::SerializedScriptValue>), const blink::CrossThreadPersistent<blink::AudioWorkletMessagingProxy> &, blink::WorkerThread *, blink::AudioWorkletHandler *, const WTF::String &, const blink::MessagePortChannel &, const scoped_refptr<blink::SerializedScriptValue> &> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:607:0
    #21 0x55790f677d8a in RunImpl<void (blink::AudioWorkletMessagingProxy::*const &)(blink::WorkerThread *, blink::AudioWorkletHandler *, const WTF::String &, blink::MessagePortChannel, scoped_refptr<blink::SerializedScriptValue>), const std::__1::tuple<blink::CrossThreadPersistent<blink::AudioWorkletMessagingProxy>, WTF::CrossThreadUnretainedWrapper<blink::WorkerThread>, WTF::CrossThreadUnretainedWrapper<blink::AudioWorkletHandler>, WTF::String, blink::MessagePortChannel, scoped_refptr<blink::SerializedScriptValue> > &, 0, 1, 2, 3, 4, 5> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:681:0
    #22 0x55790f677d8a in base::internal::Invoker<base::internal::BindState<void (blink::AudioWorkletMessagingProxy::*)(blink::WorkerThread*, blink::AudioWorkletHandler*, WTF::String const&, blink::MessagePortChannel, scoped_refptr<blink::SerializedScriptValue>), blink::CrossThreadPersistent<blink::AudioWorkletMessagingProxy>, WTF::CrossThreadUnretainedWrapper<blink::WorkerThread>, WTF::CrossThreadUnretainedWrapper<blink::AudioWorkletHandler>, WTF::String, blink::MessagePortChannel, scoped_refptr<blink::SerializedScriptValue> >, void ()>::Run(base::internal::BindStateBase*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:663:0
    #23 0x557909dc7da6 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:136:12
    #24 0x557909dc7da6 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/wtf/functional.h:320:0
    #25 0x557909dc7da6 in blink::(anonymous namespace)::RunCrossThreadClosure(WTF::CrossThreadFunction<void ()>) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/web_task_runner.cc:15:0
    #26 0x557909dc8c2e in Invoke<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> > /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:407:12
    #27 0x557909dc8c2e in MakeItSo<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> > /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:607:0
    #28 0x557909dc8c2e in RunImpl<void (*)(WTF::CrossThreadFunction<void ()>), std::__1::tuple<WTF::CrossThreadFunction<void ()> >, 0> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:681:0
    #29 0x557909dc8c2e in base::internal::Invoker<base::internal::BindState<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> >, void ()>::RunOnce(base::internal::BindStateBase*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:649:0
    #30 0x5579011b22d9 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:96:12
    #31 0x5579011b22d9 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #32 0x5579000f6298 in base::sequence_manager::internal::ThreadControllerImpl::DoWork(base::sequence_manager::internal::ThreadControllerImpl::WorkType) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/scheduler/base/thread_controller_impl.cc:166:21
    #33 0x5579011b22d9 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:96:12
    #34 0x5579011b22d9 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #35 0x557901211a13 in base::MessageLoop::RunTask(base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:319:25
    #36 0x557901212c90 in DeferOrRunPendingTask /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:329:5
    #37 0x557901212c90 in base::MessageLoop::DoWork() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:373:0
    #38 0x55790121b5f0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_pump_default.cc:37:31
    #39 0x55790128cdc1 in base::RunLoop::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/run_loop.cc:102:14
    #40 0x557901317001 in base::Thread::ThreadMain() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/thread.cc:337:3
    #41 0x5579013d0051 in base::(anonymous namespace)::ThreadFunc(void*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/platform_thread_posix.cc:76:13
    #42 0x7f06ae6b36ba in start_thread ??:0:0
    #43 0x7f06a7a0441d in clone /build/glibc-Cl5G7W/glibc-2.23/misc/../sysdeps/unix/sysv/linux/x86_64/clone.S:109:0
  r8: 000000000000d63d  r9: 0000000000000000 r10: 0000000000000008 r11: 0000000000000202
 r12: 0000000000000000 r13: 00007f0677294178 r14: 00007f0677294120 r15: 00005579133e1758
  di: 000000000000568c  si: 00000000000057fa  bp: 00007f0677294150  bx: 000055791334f2a0
  dx: 0000000000000006  ax: 0000000000000000  cx: 00007f06a7932428  sp: 00007f06772932d8
  ip: 00007f06a7932428 efl: 0000000000000202 cgf: 002b000000000033 erf: 0000000000000000
 trp: 0000000000000000 msk: 0000000000000000 cr2: 0000000000000000
[end of stack trace]
Calling _exit(1). Core file will not be generated.



### wf...@chromium.org (2018-06-18)

Haven't got a repro yet, but triaging to see if someone from webaudio can take a look.

[Monorail components: Blink>WebAudio]

### rt...@chromium.org (2018-06-18)

+hongchan for the audioworklet stuff.

### ho...@chromium.org (2018-06-18)

I also see lots of Worker infra code in the stack trace. Would like to have some feedback from Worker team too.

The stack trace in #1 is somewhat different:

// UAF happens here
#18 0x55790f674f08 in #17 0x55790f69b643 in blink::AudioWorkletHandler::SetProcessorOnRenderThread(blink::AudioWorkletProcessor*)

// After this happened.
#7 0x55790f69fb20 in blink::AudioWorkletNode::~AudioWorkletNode()

The quick solution of this is that AudioWorkletNode::HasPendingAcivity() must return true if AudioWorkletHandler is still setting up the processor.

Also the Worker thread and its GlobalScope might be terminated and gone when the AudioWorkletNode's cross-thread task tries to set the processor reference.

[Monorail components: Blink>Workers]

### sh...@chromium.org (2018-06-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-19)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-06-19)

[Empty comment from Monorail migration]

### nh...@chromium.org (2018-06-19)

hongchan@: I'm not sure why AudioWorkletMessagingProxy::CreateProcessor sends |handler| as CrossThreadUnretaned. Looks like the handler is defined as a thread-safe refcounted object, so it seems possible to send the handler in safety.

### ho...@chromium.org (2018-06-19)

Re #8: Good catch! I'll remove the CrossThreadUnretained wrapper. Hope that makes some difference in repro.

FWIW, I cannot reproduce the case on my local machine. The repro always locks up the machine so I have not seen the crash yet.



### rt...@chromium.org (2018-06-22)

I also cannot reproduce this. My machine doesn't lock up, but I pressed the back button about 50 times and no asan issues.

### cd...@gmail.com (2018-06-25)

Hi,I made simple modifications to the poc code to increase the probability of repro. Attachment file is a repro video.

### cd...@gmail.com (2018-06-25)

Sorry, don't download crash2.html, I re-upload the new version.

### rt...@chromium.org (2018-06-25)

The video wasn't really necessary; we believe you. :-)

With crash3.html, I can reproduce this.  It takes a bit of time, but it does happen on my linux box, with the stacktrace shown.

### rt...@chromium.org (2018-06-25)

Oh, the backtrace I get is somewhat different:

Received signal 11 SEGV_MAPERR 000000000000
    #0 0x5616ec01e7d1 in __interceptor_backtrace /b/build/slave/linux_upload_clang/build/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4024:13
    #1 0x7fc9dba30cdc in base::debug::StackTrace::StackTrace(unsigned long) ./../../base/debug/stack_trace_posix.cc:808:41
    #2 0x7fc9dba2fc5d in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:334:3
    #3 0x7fc9b636a0c0 in __funlockfile ??:?
    #4 0x7fc9b636a0c0 in ?? ??:0
    #5 0x7fc9bb7d8cf4 in operator-> ./../../buildtools/third_party/libc++/trunk/include/memory:2603:19
    #6 0x7fc9bb7d8cf4 in blink::WaitableEvent::Signal() ./../../third_party/blink/renderer/platform/waitable_event.cc:36:0
    #7 0x7fc9bb7dfb22 in Run ./../../base/callback.h:140:12
    #8 0x7fc9bb7dfb22 in Run ./../../third_party/blink/renderer/platform/wtf/functional.h:320:0
    #9 0x7fc9bb7dfb22 in blink::(anonymous namespace)::RunCrossThreadClosure(WTF::CrossThreadFunction<void ()>) ./../../third_party/blink/renderer/platform/web_task_runner.cc:15:0
    #10 0x7fc9bb7e0de9 in Invoke<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> > ./../../base/bind_internal.h:407:12
    #11 0x7fc9bb7e0de9 in MakeItSo<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> > ./../../base/bind_internal.h:607:0
    #12 0x7fc9bb7e0de9 in RunImpl<void (*)(WTF::CrossThreadFunction<void ()>), std::__1::tuple<WTF::CrossThreadFunction<void ()> >, 0> ./../../base/bind_internal.h:681:0
    #13 0x7fc9bb7e0de9 in base::internal::Invoker<base::internal::BindState<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> >, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:649:0
    #14 0x7fc9db7e2f44 in Run ./../../base/callback.h:99:12
    #15 0x7fc9db7e2f44 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/debug/task_annotator.cc:101:0
    #16 0x7fc9bb9d1e96 in base::sequence_manager::internal::ThreadControllerImpl::DoWork(base::sequence_manager::internal::ThreadControllerImpl::WorkType) ./../../third_party/blink/renderer/platform/scheduler/base/thread_controller_impl.cc:166:21
    #17 0x7fc9db7e2f44 in Run ./../../base/callback.h:99:12
    #18 0x7fc9db7e2f44 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/debug/task_annotator.cc:101:0
    #19 0x7fc9db859aa6 in base::MessageLoop::RunTask(base::PendingTask*) ./../../base/message_loop/message_loop.cc:319:25
    #20 0x7fc9db85af25 in DeferOrRunPendingTask ./../../base/message_loop/message_loop.cc:329:5
    #21 0x7fc9db85af25 in base::MessageLoop::DoWork() ./../../base/message_loop/message_loop.cc:373:0
    #22 0x7fc9db860230 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:37:31
    #23 0x7fc9db8e8542 in base::RunLoop::Run() ./../../base/run_loop.cc:102:14
    #24 0x7fc9db992785 in base::Thread::ThreadMain() ./../../base/threading/thread.cc:337:3
    #25 0x7fc9dba62355 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:76:13
    #26 0x7fc9b6360494 in start_thread ??:0:0
    #27 0x7fc9b1fbaa8f in clone ??:0:0
  r8: 0000000000000000  r9: 00007fc98e8a21f6 r10: 0000000000000000 r11: 0000000000000206
 r12: 00007fc98e973860 r13: 00007fc98e973840 r14: 00007fc98e973840 r15: 00000ff931d2e708
  di: 0000000000000000  si: 0000000000000000  bp: 00007fc98fdd4390  bx: 00007fc98fdd43a0
  dx: 000060400009f690  ax: 0000000000000000  cx: 0000000000000001  sp: 00007fc98fdd4390
  ip: 00007fc9bb7d8cf4 efl: 0000000000010246 cgf: 002b000000000033 erf: 0000000000000004
 trp: 000000000000000e msk: 0000000000000000 cr2: 0000000000000000
[end of stack trace]


### rt...@chromium.org (2018-06-26)

Noticed that the OP had 'use_sanitizer_coverage = true' which I didn't.  Now I can't reproduce this.  Could be coincidence, but I'll try again without use_sanitizer_coverage and see what happens.

### rt...@chromium.org (2018-06-26)

Can't reproduce this anymore.  I pressed back about 50+ times and no asan crash.

### cd...@gmail.com (2018-06-26)

Hi,
I modified the poc. Now it can reproduce without any interaction. Try this one again?
Just run 
./chrome http://xx:xx/crash4.html

If you still can not reproduce, you can manually open multiple tabs to run crash4.html, or modify the settimeout interval (you may need to reduce the time if the system performance is good enough).

### rt...@chromium.org (2018-06-26)

Did you upload the wrong crash4.html? It looks exactly like crash3.html

### cd...@gmail.com (2018-06-27)

Oh,sorry,I uploaded new one.


### cd...@gmail.com (2018-06-27)

The previous back.html may occasionally be stopped. Try this one.

### rt...@chromium.org (2018-06-27)

Thanks for the updated test files.  I was able to reproduce this once, with the same reported backtrace.  However, I tried again and let it run for 30 min without failures and restarted and let it run again for another 20 min and no failures.

This is going to take a while....

### rt...@chromium.org (2018-07-10)

[Empty comment from Monorail migration]

### rt...@chromium.org (2018-07-17)

Tried again today with ToT chromium.  Cannot reproduce this (using crash4.html).

### ho...@chromium.org (2018-07-17)

Same here. I cannot reproduce it after running ~30min. I used:

- crash4.html (re #19)
- back.html (re#20)
- audio-worklet.wasmmodule.js (re#11)

(It's funny to see what I made in the bug report...)




### bu...@chromium.org (2018-07-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/44010e122e561daf7d969f2d8d3c256775129d2d

commit 44010e122e561daf7d969f2d8d3c256775129d2d
Author: Hongchan Choi <hongchan@chromium.org>
Date: Wed Jul 18 00:35:51 2018

Remove CrossThreadUnretained wrapper when passing AudioWorkletHandler

Because AudioWorkletHandler is ThreadSafeRefCounted, wrapping with
CrossThreadUnretained() when the handler is passed via CrossThreadBind()
is unnecessary. Use scoped_refptr<> instead.

Bug: 853520
Test: All existing layout/WPT tests pass.
Change-Id: I83409b89e80a9bbb60ea98649b16efb59facbbd4
Reviewed-on: https://chromium-review.googlesource.com/1140744
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Reviewed-by: Hiroki Nakagawa <nhiroki@chromium.org>
Cr-Commit-Position: refs/heads/master@{#575874}
[modify] https://crrev.com/44010e122e561daf7d969f2d8d3c256775129d2d/third_party/blink/renderer/modules/webaudio/audio_worklet.cc
[modify] https://crrev.com/44010e122e561daf7d969f2d8d3c256775129d2d/third_party/blink/renderer/modules/webaudio/audio_worklet.h
[modify] https://crrev.com/44010e122e561daf7d969f2d8d3c256775129d2d/third_party/blink/renderer/modules/webaudio/audio_worklet_messaging_proxy.cc
[modify] https://crrev.com/44010e122e561daf7d969f2d8d3c256775129d2d/third_party/blink/renderer/modules/webaudio/audio_worklet_messaging_proxy.h
[modify] https://crrev.com/44010e122e561daf7d969f2d8d3c256775129d2d/third_party/blink/renderer/modules/webaudio/audio_worklet_node.cc
[modify] https://crrev.com/44010e122e561daf7d969f2d8d3c256775129d2d/third_party/blink/renderer/modules/webaudio/audio_worklet_node.h


### rt...@chromium.org (2018-07-23)

cdsrc2016@gmail.com can you retest with canary?

### cd...@gmail.com (2018-07-23)


I tested it for more than half an hour after patch, and never reproduced uaf.;)

### cd...@gmail.com (2018-07-23)


I tested it for more than half an hour after patch, and never reproduced uaf.;)

### rt...@chromium.org (2018-07-23)

Thanks for testing!  I'm going to declare this fixed, although it's not clear what the fix is. c#25 probably helped, but it's not clear if that is really the fix.

### cd...@gmail.com (2018-07-24)


Before the patch, my local fuzzer produced another sample(new_origin.html) that could reproduce the same UAF. This sample is more stable than the previous one(crash4.html) to reproduce the UAF. 
I tested it again with this sample(new_origin.html), and now  only reproduced sig11 0x38 (Null-Dereference). 
I also attached a log that occasionally reproduces the heap-buffer-overflow by this sample(new_origin.html) before the patch.
I hope this information is helpful for analyzing crash issue.

### sh...@chromium.org (2018-07-24)

[Empty comment from Monorail migration]

### rt...@chromium.org (2018-07-24)

Reopening per c#30.

### cm...@chromium.org (2018-07-24)

I did a quick check, with the original reproduction steps (crash.html), and get a different stack track trace. It looks like v8's gc is deleting a Worklet that still has pending tasks. My args.gn file is different from that in the report above.

Chrome Commit: ae150327d04cec716e
OS: Linux
Computer: Dell 620

args.gn:
================================================
dcheck_always_on = true
enable_full_stack_frames_for_profiling = true
enable_nacl = false
enable_profiling = false
goma_dir = "/usr/local/google/home/cmumford/goma"
is_asan = true
is_clang = true
is_component_build = false
is_debug = false
is_lsan = true
strip_absolute_paths_from_debug_symbols = true
symbol_level = 1
target_os = "linux"
use_goma = true

Stack:
========================
[43787:43787:0724/094917.418265:FATAL:worklet.cc(32)] Check failed: !HasPendingTasks().
    #0 0x56264b781711 in __interceptor_backtrace /b/swarming/w/ir/kitchen-workdir/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4024:13
    #1 0x5626557605fc in base::debug::StackTrace::StackTrace(unsigned long) ./../../base/debug/stack_trace_posix.cc:808:41
    #2 0x5626554d5ff3 in logging::LogMessage::~LogMessage() ./../../base/logging.cc:592:29
    #3 0x562664735f7d in blink::Worklet::~Worklet() ./../../third_party/blink/renderer/core/workers/worklet.cc:32:3
    #4 0x562653d2e412 in blink::HeapObjectHeader::Finalize(unsigned char*, unsigned long) ./../../third_party/blink/renderer/platform/heap/heap_page.cc:104:5
    #5 0x562653d402f7 in blink::NormalPage::Sweep() ./../../third_party/blink/renderer/platform/heap/heap_page.cc:1344:15
    #6 0x562653d31d68 in SweepUnsweptPage ./../../third_party/blink/renderer/platform/heap/heap_page.cc:284:31    #7 0x562653d31d68 in blink::BaseArena::CompleteSweep() ./../../third_party/blink/renderer/platform/heap/heap_page.cc:340:0
    #8 0x562653d6bd96 in blink::ThreadState::EagerSweep() ./../../third_party/blink/renderer/platform/heap/thread_state.cc:1025:49
    #9 0x562653d6a37e in blink::ThreadState::AtomicPauseEpilogue(blink::BlinkGC::MarkingType, blink::BlinkGC::SweepingType) ./../../third_party/blink/renderer/platform/heap/thread_state.cc:993:3
    #10 0x562653d6fcf9 in blink::ThreadState::RunAtomicPause(blink::BlinkGC::StackState, blink::BlinkGC::MarkingType, blink::BlinkGC::SweepingType, blink::BlinkGC::GCReason) ./../../third_party/blink/renderer/platform/heap/thread_state.cc:1593:5
    #11 0x562653d59f19 in blink::ThreadState::CollectGarbage(blink::BlinkGC::StackState, blink::BlinkGC::MarkingType, blink::BlinkGC::SweepingType, blink::BlinkGC::GCReason) ./../../third_party/blink/renderer/platform/heap/thread_state.cc:1536:5
    #12 0x56266176de63 in blink::V8GCController::GcEpilogue(v8::Isolate*, v8::GCType, v8::GCCallbackFlags) ./../../third_party/blink/renderer/bindings/core/v8/v8_gc_controller.cc:279:29
    #13 0x5626529787d7 in v8::internal::Heap::CallGCEpilogueCallbacks(v8::GCType, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:1863:7
    #14 0x56265296a549 in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:1832:7
    #15 0x5626529642b8 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:1398:11
    #16 0x562652981a54 in CollectAllGarbage ./../../v8/src/heap/heap.cc:1156:3    #17 0x562652981a54 in v8::internal::Heap::FinalizeIncrementalMarkingIfComplete(v8::internal::GarbageCollectionReason) ./../../v8/src/heap/heap.cc:3170:0
    #18 0x5626529b4069 in Step ./../../v8/src/heap/incremental-marking-job.cc:39:9    #19 0x5626529b4069 in v8::internal::IncrementalMarkingJob::Task::RunInternal() ./../../v8/src/heap/incremental-marking-job.cc:63:0
    #20 0x5626555029d2 in Run ./../../base/callback.h:99:12    #21 0x5626555029d2 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/debug/task_annotator.cc:101:0
    #22 0x562655637e54 in base::sequence_manager::internal::ThreadControllerImpl::DoWork(base::sequence_manager::internal::ThreadControllerImpl::WorkType) ./../../base/task/sequence_manager/thread_controller_impl.cc:166:21
    #23 0x56265563d08c in Invoke<void (base::sequence_manager::internal::ThreadControllerImpl::*)(base::sequence_manager::internal::ThreadControllerImpl::WorkType), const base::WeakPtr<base::sequence_manager::internal::ThreadControllerImpl> &, const base::sequence_manager::internal::ThreadControllerImpl::WorkType &> ./../../base/bind_internal.h:516:12    #24 0x56265563d08c in MakeItSo<void (base::sequence_manager::internal::ThreadControllerImpl::*const &)(base::sequence_manager::internal::ThreadControllerImpl::WorkType), const base::WeakPtr<base::sequence_manager::internal::ThreadControllerImpl> &, const base::sequence_manager::internal::ThreadControllerImpl::WorkType &> ./../../base/bind_internal.h:636:0    #25 0x56265563d08c in RunImpl<void (base::sequence_manager::internal::ThreadControllerImpl::*const &)(base::sequence_manager::internal::ThreadControllerImpl::WorkType), const std::__1::tuple<base::WeakPtr<base::sequence_manager::internal::ThreadControllerImpl>, base::sequence_manager::internal::ThreadControllerImpl::WorkType> &, 0, 1> ./../../base/bind_internal.h:689:0    #26 0x56265563d08c in base::internal::Invoker<base::internal::BindState<void (base::sequence_manager::internal::ThreadControllerImpl::*)(base::sequence_manager::internal::ThreadControllerImpl::WorkType), base::WeakPtr<base::sequence_manager::internal::ThreadControllerImpl>, base::sequence_manager::internal::ThreadControllerImpl::WorkType>, void ()>::Run(base::internal::BindStateBase*) ./../../base/bind_internal.h:671:0
    #27 0x5626555029d2 in Run ./../../base/callback.h:99:12    #28 0x5626555029d2 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/debug/task_annotator.cc:101:0
    #29 0x5626554fafc9 in base::MessageLoop::RunTask(base::PendingTask*) ./../../base/message_loop/message_loop.cc:421:46
    #30 0x5626554fc173 in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask) ./../../base/message_loop/message_loop.cc:432:5
    #31 0x5626554fca47 in base::MessageLoop::DoWork() ./../../base/message_loop/message_loop.cc:480:16
    #32 0x56265550f840 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:37:31
    #33 0x5626554f9ad2 in base::MessageLoop::Run(bool) ./../../base/message_loop/message_loop.cc:373:12
    #34 0x5626555a254b in base::RunLoop::Run() ./../../base/run_loop.cc:102:14
    #35 0x562667ccb816 in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:200:23
    #36 0x5626546cf84f in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:554:14
    #37 0x5626546d3062 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:951:10
    #38 0x5626546f4a22 in service_manager::Main(service_manager::MainParams const&) ./../../services/service_manager/embedder/main.cc:472:29
    #39 0x5626546cded0 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:19:10
    #40 0x56264b80b448 in ChromeMain ./../../chrome/app/chrome_main.cc:101:12
    #41 0x7f975c1d12b1 in __libc_start_main ??:0:0
    #42 0x56264b73402a in _start ??:0:0


### rt...@chromium.org (2018-07-24)

There are enough crashes here with the same test case(s) that we should probably separate them out into different issues.  It's getting hard to keep track of what we're actually trying to fix.

I'll do that shortly.

### rt...@chromium.org (2018-07-24)

From new.zip from c#30, the log for the sig11 crash looks like (in part):

 #0 0x56270d8d8811 in __interceptor_backtrace /b/build/slave/linux_upload_clang/
build/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_co
mmon_interceptors.inc:4024:13
    #1 0x5627154d12fe in base::debug::StackTrace::StackTrace(unsigned long) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/stack_trace_posix.cc:808:41
    #2 0x5627154d024d in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/stack_trace_posix.cc:334:3
    #3 0x7f13f87b5390 in __funlockfile ??:?
    #4 0x7f13f87b5390 in ?? ??:0
    #5 0x5627238e8be9 in operator* /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/memory/scoped_refptr.h:215:13
    #6 0x5627238e8be9 in blink::AudioNode::Handler() const /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_node.cc:639:0
    #7 0x56272393d66d in blink::AudioDestinationNode::GetAudioDestinationHandler() const /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_destination_node.cc:48:48
    #8 0x5627238e6bd9 in CurrentSampleFrame /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/base_audio_context.h:130:31

That doesn't make sense unless this is from a slightly older build.  CurrentSampleFrame no longer calls AudioDestinationNode::GetAudioDestinationHandler(), but did originally.  So the backtrace for heap-buffer-overflow is a little suspect too, because it might be from a slightly older version.

I'm doing a build now with current sources to see what I can get....

### rt...@chromium.org (2018-07-24)

Unable to reproduce any asan issues using new.zip on my Linux system.  I let the test run for about 30 minutes.

If you can, please try again with a more recent asan build.  The sig11 crash should not be happening anymore (at least not with that backtrace).

### rt...@chromium.org (2018-07-24)

Ran new.zip on my other linux machine that was able to repro https://crbug.com/chromium/860522.

After letting it run for about 30 minutes, asan failed to allocate memory for itself, so I'm still unable to reproduce this.

### cd...@gmail.com (2018-07-25)

I may test the old version, I will test it again with the new ASAN build.
My test environment is as follows:
Chrome Version 69.0.3477.0 (Developer Build) (64-bit)(with patch from https://crbug.com/chromium/853520#c30)
OS version:Ubuntu 16.04



### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### cd...@gmail.com (2018-07-25)

I tested it in the new build for more than half an hour, and no any crashes reproduced.
chrome version:Version 70.0.3503.0 (Developer Build) (64-bit)
os:Ubuntu 16.04

### rt...@chromium.org (2018-07-25)

Ah, great news!  Thanks for testing again.

So I'm going to say this is fixed, again.  While I hate working on these things, they're real bugs and we appreciate your time in finding them.

### aw...@chromium.org (2018-07-30)

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

CL listed at #25 is already in M69 branch #3497.

### aw...@chromium.org (2018-08-03)

No merge needed.

### cd...@gmail.com (2018-08-06)

Oops,,,,
My fuzzer reproduced this uaf in the new build(asan-linux-release-580151) again,and is pretty stable. 
The strange thing is that occasionally reproduced another uaf. 
Please see the attachments.

### rt...@chromium.org (2018-08-06)

Reopen per c#47

### sh...@chromium.org (2018-08-07)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rt...@chromium.org (2018-08-07)

I was able to reproduce this using new2.zip on my Linux machine. Same stack trace.

Reopen (again?) and assign to @hongchan since it's a worklet issue.

### go...@chromium.org (2018-08-07)

M69 Stable promotion is coming VERY soon. Your bug is labelled as Stable ReleaseBlock, pls make sure to land the fix and request a merge into the release branch ASAP. Thank you.

### ho...@chromium.org (2018-08-08)

govind@

I am traveling at the moment and will be back at MTV by 8/18. I will try to develop a fix for this after that. Would it work for our stable promotion schedule?

If this is not feasible, I am hoping rtoy@ or nhiroki@ can take a look at this.

### rt...@chromium.org (2018-08-08)

Aargh.  I updated my Chromium tree to ToT today and can no longer reproduce this with new2 case. I let it run for about an hour without any issues.

This is going to be hard to fix since the backtrace doesn't provide enough information to guess what the problem could be.

### cd...@gmail.com (2018-08-09)

Hi,@rtoy
The new version(Version 70.0.3515.0 (Developer Build) (64-bit))  still  able to  reproduce the UAF(--;) in my local machine.
However, the previous way is not easy to reproduce the UAF. I don't know the reasons.
No matter what, you can try the following method, which is pretty stable in my local machine.
	-	Use the minimised poc in the attachments and open 2 or more tabs at the same time. 
	-	If the page is suspended(blank), reopen  browser and open 2 or more tabs again. The UAF reproduced within 30 seconds in my local machine.

Attachments include a minimised poc(minimised_poc.html), new uaf log that occasionally reproduced, and repro video. 
I hope this information useful for analyzing the UAF issues.



### cd...@gmail.com (2018-08-09)

[Empty comment from Monorail migration]

### cd...@gmail.com (2018-08-09)

I found that the windows release version( 68.0.3440.106 official release 32bit) also crashes after increasing the number of loops(260 to 500).
The attachment is the pydbg log.
test env:
OS version:Win7
system type:64bit
memory:16GB
cpu:i5 3570

### rt...@chromium.org (2018-08-09)

Ran the repro case in new3 using 3 separate tabs.  After some 30 minutes, I got a failure, but it's not the one mentioned here.  The backtrace is the same as in https://crbug.com/chromium/870678.

### ho...@chromium.org (2018-08-10)

I can't find the https://crbug.com/chromium/870678.

### cd...@gmail.com (2018-08-10)

After many tests, I found that the same poc (minimised_poc.html) will reproduce this UAF when using "back.html", and will reproduce another UAF (870678) when using "<meta http-equiv="refresh" content="1">" .

### go...@chromium.org (2018-08-10)

Is there anything needed for M69? Per comments #46 & #47 no merge needed. If nothing is pending for M69, pls mark bug as fixed.

### aw...@google.com (2018-08-13)

Moving to M70

### sh...@chromium.org (2018-08-16)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ho...@chromium.org (2018-08-20)

nhiroki@, haraken@

Could you take a look at the stack trace in #56? (asan_symbolize3.log)

It seems like the message loop is trying to access the Worker thread after it is destroyed. Any input would be appreciated.

---
READ of size 8 at 0x602001492af0 thread T304 (WebAudio thread)
    #0 0x55c2994ea2b5 in operator-> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/memory/scoped_refptr.h:220:12
    #1 0x55c2994ea2b5 in base::WaitableEvent::Signal() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/synchronization/waitable_event_posix.cc:59:0
    #2 0x55c2a23de19a in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:140:12
    #3 0x55c2a23de19a in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/wtf/functional.h:331:0
    #4 0x55c2a23de19a in blink::(anonymous namespace)::RunCrossThreadClosure(WTF::CrossThreadFunction<void ()>) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/web_task_runner.cc:15:0
    #5 0x55c2a23df268 in Invoke<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> > /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:416:12
    #6 0x55c2a23df268 in MakeItSo<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> > /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:616:0
    #7 0x55c2a23df268 in RunImpl<void (*)(WTF::CrossThreadFunction<void ()>), std::__1::tuple<WTF::CrossThreadFunction<void ()> >, 0> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:689:0
    #8 0x55c2a23df268 in base::internal::Invoker<base::internal::BindState<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> >, void ()>::RunOnce(base::internal::BindStateBase*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:658:0
    #9 0x55c2992ff5c0 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:99:12
    #10 0x55c2992ff5c0 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #11 0x55c2993e3bb5 in base::sequence_manager::internal::ThreadControllerImpl::DoWork(base::sequence_manager::internal::ThreadControllerImpl::WorkType) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/sequence_manager/thread_controller_impl.cc:169:21
    #12 0x55c2992ff5c0 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:99:12
    #13 0x55c2992ff5c0 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #14 0x55c2992fa8ed in base::MessageLoop::RunTask(base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:431:46
    #15 0x55c2992fbb78 in DeferOrRunPendingTask /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:442:5
    #16 0x55c2992fbb78 in base::MessageLoop::DoWork() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:514:0
    #17 0x55c29930342f in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_pump_default.cc:37:31
    #18 0x55c299374c70 in base::RunLoop::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/run_loop.cc:102:14
    #19 0x55c29943205f in base::Thread::ThreadMain() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/thread.cc:357:3
    #20 0x55c2994f6790 in base::(anonymous namespace)::ThreadFunc(void*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/platform_thread_posix.cc:76:13
    #21 0x7f4db03556da in start_thread ??:0:0

0x602001492af0 is located 0 bytes inside of 8-byte region [0x602001492af0,0x602001492af8)
freed by thread T0 (chrome) here:
    #0 0x55c2915d12b2 in operator delete(void*) _asan_rtl_:3
    #1 0x55c2a5c121c0 in operator() /home/cowboy/chromium/src/out/chrome_asan_shared/../../buildtools/third_party/libc++/trunk/include/memory:2321:5
    #2 0x55c2a5c121c0 in reset /home/cowboy/chromium/src/out/chrome_asan_shared/../../buildtools/third_party/libc++/trunk/include/memory:2634:0
    #3 0x55c2a5c121c0 in ~unique_ptr /home/cowboy/chromium/src/out/chrome_asan_shared/../../buildtools/third_party/libc++/trunk/include/memory:2588:0
    #4 0x55c2a5c121c0 in blink::WorkerThread::~WorkerThread() /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/workers/worker_thread.cc:101:0
    #5 0x55c2a7d2cca4 in ~AudioWorkletThread /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet_thread.cc:49:1
    #6 0x55c2a7d2cca4 in blink::AudioWorkletThread::~AudioWorkletThread() /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/modules/webaudio/audio_worklet_thread.cc:45:0
    #7 0x55c2a5be1584 in operator() /home/cowboy/chromium/src/out/chrome_asan_shared/../../buildtools/third_party/libc++/trunk/include/memory:2321:5
    #8 0x55c2a5be1584 in reset /home/cowboy/chromium/src/out/chrome_asan_shared/../../buildtools/third_party/libc++/trunk/include/memory:2634:0
    #9 0x55c2a5be1584 in ~unique_ptr /home/cowboy/chromium/src/out/chrome_asan_shared/../../buildtools/third_party/libc++/trunk/include/memory:2588:0
    #10 0x55c2a5be1584 in blink::ThreadedMessagingProxyBase::WorkerThreadTerminated() /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/core/workers/threaded_messaging_proxy_base.cc:163:0
    #11 0x55c2a5be6190 in Invoke<void (blink::ThreadedMessagingProxyBase::*)(), blink::CrossThreadPersistent<blink::ThreadedMessagingProxyBase>> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:516:12
    #12 0x55c2a5be6190 in MakeItSo<void (blink::ThreadedMessagingProxyBase::*const &)(), blink::CrossThreadPersistent<blink::ThreadedMessagingProxyBase>> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:636:0
    #13 0x55c2a5be6190 in RunImpl<void (blink::ThreadedMessagingProxyBase::*const &)(), const std::__1::tuple<blink::CrossThreadWeakPersistent<blink::ThreadedMessagingProxyBase> > &, 0> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:689:0
    #14 0x55c2a5be6190 in base::internal::Invoker<base::internal::BindState<void (blink::ThreadedMessagingProxyBase::*)(), blink::CrossThreadWeakPersistent<blink::ThreadedMessagingProxyBase> >, void ()>::Run(base::internal::BindStateBase*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:671:0
    #15 0x55c2a23de19a in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:140:12
    #16 0x55c2a23de19a in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/wtf/functional.h:331:0
    #17 0x55c2a23de19a in blink::(anonymous namespace)::RunCrossThreadClosure(WTF::CrossThreadFunction<void ()>) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/web_task_runner.cc:15:0
    #18 0x55c2a23df268 in Invoke<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> > /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:416:12
    #19 0x55c2a23df268 in MakeItSo<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> > /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:616:0
    #20 0x55c2a23df268 in RunImpl<void (*)(WTF::CrossThreadFunction<void ()>), std::__1::tuple<WTF::CrossThreadFunction<void ()> >, 0> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:689:0
    #21 0x55c2a23df268 in base::internal::Invoker<base::internal::BindState<void (*)(WTF::CrossThreadFunction<void ()>), WTF::CrossThreadFunction<void ()> >, void ()>::RunOnce(base::internal::BindStateBase*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:658:0
    #22 0x55c2992ff5c0 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:99:12
    #23 0x55c2992ff5c0 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #24 0x55c2993e3bb5 in base::sequence_manager::internal::ThreadControllerImpl::DoWork(base::sequence_manager::internal::ThreadControllerImpl::WorkType) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/task/sequence_manager/thread_controller_impl.cc:169:21
    #25 0x55c2992ff5c0 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:99:12
    #26 0x55c2992ff5c0 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #27 0x55c2992fa8ed in base::MessageLoop::RunTask(base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:431:46
    #28 0x55c2992fbb78 in DeferOrRunPendingTask /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:442:5
    #29 0x55c2992fbb78 in base::MessageLoop::DoWork() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:514:0
    #30 0x55c29930342f in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_pump_default.cc:37:31
    #31 0x55c299374c70 in base::RunLoop::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/run_loop.cc:102:14
    #32 0x55c2a87a7c54 in content::RendererMain(content::MainFunctionParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/renderer/renderer_main.cc:200:23
    #33 0x55c29869174d in content::RunZygote(content::ContentMainDelegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:493:14
    #34 0x55c2986949a6 in content::ContentMainRunnerImpl::Run(bool) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:891:10
    #35 0x55c2987c2d24 in service_manager::Main(service_manager::MainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../services/service_manager/embedder/main.cc:472:29
    #36 0x55c29868fe7e in content::ContentMain(content::ContentMainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main.cc:19:10
    #37 0x55c2915d3e6f in ChromeMain /home/cowboy/chromium/src/out/chrome_asan_shared/../../chrome/app/chrome_main.cc:101:12
    #38 0x7f4da92bdb96 in __libc_start_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310:0
---

### ho...@chromium.org (2018-08-20)

So the core issue here is that AudioWorkletThread is destroyed by blink::ThreadedMessagingProxyBase::WorkerThreadTerminated() and then accessed by blink::WorkerThread::PerformShutdownOnWorkerThread().

Considering the reproduction requires "two or more tabs", I am speculating this might be due to the AudioWorkletThread uses a static WebThread for the singleton backing thread. I am unfamiliar with the life cycle of WorkerThread, so would love to have some inputs from the Worker infra's perspective.

nhiroki@ WDYT?

### ha...@chromium.org (2018-08-21)

Yeah, this looks like a bug of worker's infra. hiroki-san?


### nh...@chromium.org (2018-08-21)

I'll take a look today.

### nh...@chromium.org (2018-08-21)

I suspect that a task posed to the main thread in DidTerminateWorkerThread() may delete the instance of WorkerThread before |shutdown_event_->Signal()| is called. Probably we can save |shutdown_event_| in a local variable and then call it after DidTerminateWorkerThread().

void WorkerThread::PerformShutdownOnWorkerThread() {
  // ... <snip> ...

  // Notify the proxy that the WorkerOrWorkletGlobalScope has been disposed
  // of. This can free this thread object, hence it must not be touched
  // afterwards.
  GetWorkerReportingProxy().DidTerminateWorkerThread();

  // <=== Delete |this| at this point??

  shutdown_event_->Signal();
}

### nh...@chromium.org (2018-08-21)

CL is under review: https://chromium-review.googlesource.com/c/chromium/src/+/1183005

### bu...@chromium.org (2018-08-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/38e84f694bd97f13b92f23a873621b9441c045fe

commit 38e84f694bd97f13b92f23a873621b9441c045fe
Author: Hiroki Nakagawa <nhiroki@chromium.org>
Date: Fri Aug 24 09:03:43 2018

Worker: Fix possible race condition in worker thread termination

In WorkerThread::PerformShutdownOnWorkerThread(), DidTerminateWorkerThread() may
induce the main thread to destroy the instance of WorkerThread, so accessing
|this| after the function call is dangerous. This CL avoids it.

Bug: 853520
Change-Id: If0b57ceb05fce97fa4d28d7ca9defb76e39d1c27
Reviewed-on: https://chromium-review.googlesource.com/1183005
Reviewed-by: Matt Falkenhagen <falken@chromium.org>
Commit-Queue: Hiroki Nakagawa <nhiroki@chromium.org>
Cr-Commit-Position: refs/heads/master@{#585769}
[modify] https://crrev.com/38e84f694bd97f13b92f23a873621b9441c045fe/third_party/blink/renderer/core/workers/worker_thread.cc
[modify] https://crrev.com/38e84f694bd97f13b92f23a873621b9441c045fe/third_party/blink/renderer/core/workers/worker_thread.h


### ho...@chromium.org (2018-08-27)

nhiroki@

I am marking this as fixed - do we need verification? Have you tried to repro the attached PoC here?

### aw...@chromium.org (2018-09-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-09-05)

Nice one cdsrc2016@! The VRP panel decided to award $1,000 for this report, and would like to thank you for all the additional help :-)

### cd...@gmail.com (2018-09-06)

Hi~
Thank you for the reward. :-)

### aw...@chromium.org (2018-09-11)

[Empty comment from Monorail migration]

### aw...@google.com (2018-09-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/853520?no_tracker_redirect=1

[Multiple monorail components: Blink>WebAudio, Blink>Workers]
[Monorail mergedwith: crbug.com/chromium/856588]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091681)*
