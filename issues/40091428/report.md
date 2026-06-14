# heap-use-after-free on AudioOutputDevi

| Field | Value |
|-------|-------|
| **Issue ID** | [40091428](https://issues.chromium.org/issues/40091428) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Media>Audio, Blink>MediaStream, Blink>WebAudio |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2018-05-19 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36

Steps to reproduce the problem:
Version 68.0.3430.0 (Developer Build) (64-bit)
Version 66.0.3359.170(Windows Release)(32-bit)
heap-use-after-free on AudioOutputDevi

1.Get new version chrome:
 a) Build source code 
    config args.gn file as below:
		use_sanitizer_coverage = true
		is_asan = true
		is_debug = false
		enable_nacl = false
		treat_warnings_as_errors = false
	ninja -j16 -C out/chrome_asan chrome
2. python3.5m -m http.server 8605
3. ./crhome --no-sandbox poc.html
4.Get heap-use-after-free 

What is the expected behavior?

What went wrong?
==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x606000d734b0 at pc 0x562d96b86cf7 bp 0x7f3b26ff71f0 sp 0x7f3b26ff71e8
READ of size 8 at 0x606000d734b0 thread T43 (AudioOutputDevi)
    #0 0x562d96b86cf6 in get /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:64:27
    #1 0x562d96b86cf6 in Unwrap /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:829:0
    #2 0x562d96b86cf6 in Unwrap<const base::internal::UnretainedWrapper<content::HtmlAudioElementCapturerSource> &> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:167:0
    #3 0x562d96b86cf6 in RunImpl<void (content::HtmlAudioElementCapturerSource::*const &)(std::__1::unique_ptr<media::AudioBus, std::__1::default_delete<media::AudioBus> >, unsigned int, int), const std::__1::tuple<base::internal::UnretainedWrapper<content::HtmlAudioElementCapturerSource> > &, 0> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:623:0
    #4 0x562d96b86cf6 in base::internal::Invoker<base::internal::BindState<void (content::HtmlAudioElementCapturerSource::*)(std::__1::unique_ptr<media::AudioBus, std::__1::default_delete<media::AudioBus> >, unsigned int, int), base::internal::UnretainedWrapper<content::HtmlAudioElementCapturerSource> >, void (std::__1::unique_ptr<media::AudioBus, std::__1::default_delete<media::AudioBus> >, unsigned int, int)>::Run(base::internal::BindStateBase*, std::__1::unique_ptr<media::AudioBus, std::__1::default_delete<media::AudioBus> >&&, unsigned int, int) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:603:0
    #5 0x562d94af9fdf in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:125:12
    #6 0x562d94af9fdf in media::WebAudioSourceProviderImpl::TeeFilter::Render(base::TimeDelta, base::TimeTicks, int, media::AudioBus*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../media/blink/webaudiosourceprovider_impl.cc:333:0
    #7 0x562d81cdf509 in media::AudioRendererMixerInput::ProvideInput(media::AudioBus*, unsigned int) /home/cowboy/chromium/src/out/chrome_asan_shared/../../media/base/audio_renderer_mixer_input.cc:172:18
    #8 0x562d81cd4482 in media::AudioConverter::SourceCallback(int, media::AudioBus*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../media/base/audio_converter.cc:211:16
    #9 0x562d81cd39d4 in media::AudioConverter::ProvideInput(int, media::AudioBus*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../media/base/audio_converter.cc:254:5
    #10 0x562d81d5e506 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:125:12
    #11 0x562d81d5e506 in media::SincResampler::Resample(int, float*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../media/base/sinc_resampler.cc:286:0
    #12 0x562d81cd5f72 in media::AudioConverter::ConvertWithDelay(unsigned int, media::AudioBus*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../media/base/audio_converter.cc:147:19
    #13 0x562d81d0d1b0 in media::LoopbackAudioConverter::ProvideInput(media::AudioBus*, unsigned int) /home/cowboy/chromium/src/out/chrome_asan_shared/../../media/base/loopback_audio_converter.cc:19:20
    #14 0x562d81cd4482 in media::AudioConverter::SourceCallback(int, media::AudioBus*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../media/base/audio_converter.cc:211:16
    #15 0x562d81cd5faf in media::AudioConverter::ConvertWithDelay(unsigned int, media::AudioBus*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../media/base/audio_converter.cc:144:5
    #16 0x562d81cdd80f in media::AudioRendererMixer::Render(base::TimeDelta, base::TimeTicks, int, media::AudioBus*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../media/base/audio_renderer_mixer.cc:186:21
    #17 0x562d81c72d47 in media::AudioOutputDevice::AudioThreadCallback::Process(unsigned int) /home/cowboy/chromium/src/out/chrome_asan_shared/../../media/audio/audio_output_device.cc:498:21
    #18 0x562d81c3bf33 in media::AudioDeviceThread::ThreadMain() /home/cowboy/chromium/src/out/chrome_asan_shared/../../media/audio/audio_device_thread.cc:86:18
    #19 0x562d87efca20 in base::(anonymous namespace)::ThreadFunc(void*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/platform_thread_posix.cc:76:13
    #20 0x7f3b4e91a6b9 in start_thread ??:0:0

0x606000d734b0 is located 48 bytes inside of 56-byte region [0x606000d73480,0x606000d734b8)
freed by thread T0 (chrome) here:
    #0 0x562d80907f42 in operator delete(void*) _asan_rtl_:3
    #1 0x562d87cbdd2b in Destruct /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback_internal.cc:21:3
    #2 0x562d87cbdd2b in Release /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/memory/ref_counted.h:387:0
    #3 0x562d87cbdd2b in Release /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/memory/scoped_refptr.h:280:0
    #4 0x562d87cbdd2b in ~scoped_refptr /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/memory/scoped_refptr.h:208:0
    #5 0x562d87cbdd2b in base::internal::CallbackBaseCopyable::operator=(base::internal::CallbackBaseCopyable const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback_internal.cc:85:0
    #6 0x562d94af99aa in operator= /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:114:66
    #7 0x562d94af99aa in set_copy_audio_bus_callback /home/cowboy/chromium/src/out/chrome_asan_shared/../../media/blink/webaudiosourceprovider_impl.cc:89:0
    #8 0x562d94af99aa in media::WebAudioSourceProviderImpl::SetCopyAudioCallback(base::RepeatingCallback<void (std::__1::unique_ptr<media::AudioBus, std::__1::default_delete<media::AudioBus> >, unsigned int, int)> const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../media/blink/webaudiosourceprovider_impl.cc:289:0
    #9 0x562d96b862fc in content::HtmlAudioElementCapturerSource::SetAudioCallback() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/renderer/media_capture_from_element/html_audio_element_capturer_source.cc:60:20
    #10 0x562d87cccd18 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:96:12
    #11 0x562d87cccd18 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #12 0x562d86c47677 in blink::scheduler::internal::ThreadControllerImpl::DoWork(blink::scheduler::internal::SequencedTaskSource::WorkType) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/scheduler/base/thread_controller_impl.cc:170:21
    #13 0x562d87cccd18 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:96:12
    #14 0x562d87cccd18 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #15 0x562d87d2d1d2 in base::MessageLoop::RunTask(base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:319:25
    #16 0x562d87d2e44f in DeferOrRunPendingTask /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:329:5
    #17 0x562d87d2e44f in base::MessageLoop::DoWork() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:373:0
    #18 0x562d87d36bbf in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_pump_default.cc:37:31
    #19 0x562d87da77a0 in base::RunLoop::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/run_loop.cc:131:14
    #20 0x562d96b99f1d in content::RendererMain(content::MainFunctionParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/renderer/renderer_main.cc:250:23
    #21 0x562d872917c8 in content::RunZygote(content::ContentMainDelegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:566:14
    #22 0x562d872952af in content::ContentMainRunnerImpl::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:964:10
    #23 0x562d872ba65d in service_manager::Main(service_manager::MainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../services/service_manager/embedder/main.cc:459:29
    #24 0x562d8728fe37 in content::ContentMain(content::ContentMainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main.cc:19:10
    #25 0x562d8090aa6f in ChromeMain /home/cowboy/chromium/src/out/chrome_asan_shared/../../chrome/app/chrome_main.cc:101:12
    #26 0x7f3b47b8482f in __libc_start_main /build/glibc-Cl5G7W/glibc-2.23/csu/../csu/libc-start.c:291:0

previously allocated by thread T0 (chrome) here:
    #0 0x562d80907302 in operator new(unsigned long) _asan_rtl_:3
    #1 0x562d96b86277 in BindRepeating<void (content::HtmlAudioElementCapturerSource::*)(std::__1::unique_ptr<media::AudioBus, std::__1::default_delete<media::AudioBus> >, unsigned int, int), base::internal::UnretainedWrapper<content::HtmlAudioElementCapturerSource> > /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind.h:254:23
    #2 0x562d96b86277 in Bind<void (content::HtmlAudioElementCapturerSource::*)(std::__1::unique_ptr<media::AudioBus, std::__1::default_delete<media::AudioBus> >, unsigned int, int), base::internal::UnretainedWrapper<content::HtmlAudioElementCapturerSource> > /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind.h:266:0
    #3 0x562d96b86277 in content::HtmlAudioElementCapturerSource::SetAudioCallback() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/renderer/media_capture_from_element/html_audio_element_capturer_source.cc:60:0
    #4 0x562d87cccd18 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:96:12
    #5 0x562d87cccd18 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #6 0x562d86c47677 in blink::scheduler::internal::ThreadControllerImpl::DoWork(blink::scheduler::internal::SequencedTaskSource::WorkType) /home/cowboy/chromium/src/out/chrome_asan_shared/../../third_party/blink/renderer/platform/scheduler/base/thread_controller_impl.cc:170:21
    #7 0x562d87cccd18 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:96:12
    #8 0x562d87cccd18 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #9 0x562d87d2d1d2 in base::MessageLoop::RunTask(base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:319:25
    #10 0x562d87d2e44f in DeferOrRunPendingTask /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:329:5
    #11 0x562d87d2e44f in base::MessageLoop::DoWork() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:373:0
    #12 0x562d87d36bbf in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_pump_default.cc:37:31
    #13 0x562d87da77a0 in base::RunLoop::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/run_loop.cc:131:14
    #14 0x562d96b99f1d in content::RendererMain(content::MainFunctionParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/renderer/renderer_main.cc:250:23
    #15 0x562d872917c8 in content::RunZygote(content::ContentMainDelegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:566:14
    #16 0x562d872952af in content::ContentMainRunnerImpl::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:964:10
    #17 0x562d872ba65d in service_manager::Main(service_manager::MainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../services/service_manager/embedder/main.cc:459:29
    #18 0x562d8728fe37 in content::ContentMain(content::ContentMainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main.cc:19:10
    #19 0x562d8090aa6f in ChromeMain /home/cowboy/chromium/src/out/chrome_asan_shared/../../chrome/app/chrome_main.cc:101:12
    #20 0x7f3b47b8482f in __libc_start_main /build/glibc-Cl5G7W/glibc-2.23/csu/../csu/libc-start.c:291:0

Thread T43 (AudioOutputDevi) created by T6 (Chrome_ChildIOT) here:
    #0 0x562d808c453d in __interceptor_pthread_create _asan_rtl_:3
    #1 0x562d87efbc9a in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, base::PlatformThreadHandle*, base::ThreadPriority) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/platform_thread_posix.cc:115:13
    #2 0x562d81c3b8d5 in media::AudioDeviceThread::AudioDeviceThread(media::AudioDeviceThread::Callback*, int, char const*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../media/audio/audio_device_thread.cc:53:3
    #3 0x562d81c7159d in media::AudioOutputDevice::OnStreamCreated(base::SharedMemoryHandle, int, bool) /home/cowboy/chromium/src/out/chrome_asan_shared/../../media/audio/audio_output_device.cc:401:29
    #4 0x562d94b4eeb9 in content::MojoAudioOutputIPC::Created(mojo::InterfacePtr<media::mojom::AudioOutputStream>, mojo::StructPtr<media::mojom::AudioDataPipe>) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/renderer/media/mojo_audio_output_ipc.cc:239:14
    #5 0x562d81b0b9ca in media::mojom::AudioOutputStreamProviderClientStubDispatch::Accept(media::mojom::AudioOutputStreamProviderClient*, mojo::Message*) /home/cowboy/chromium/src/out/chrome_asan_shared/gen/media/mojo/interfaces/audio_output_stream.mojom.cc:855:13
    #6 0x562d892100c4 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:419:32
    #7 0x562d89221043 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/multiplex_router.cc:865:42
    #8 0x562d8921f81a in mojo::internal::MultiplexRouter::Accept(mojo::Message*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/multiplex_router.cc:589:38
    #9 0x562d89209d5f in mojo::Connector::ReadSingleMessage(unsigned int*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/connector.cc:443:51
    #10 0x562d8920b65c in mojo::Connector::ReadAllAvailableMessages() /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/connector.cc:472:10
    #11 0x562d891fc447 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:125:12
    #12 0x562d891fc447 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/system/simple_watcher.cc:274:0
    #13 0x562d891fcd17 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/system/simple_watcher.cc:105:22
    #14 0x562d891fa55c in mojo::SimpleWatcher::Context::CallNotify(MojoTrapEvent const*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/system/simple_watcher.cc:55:14
    #15 0x562d828001cf in mojo::edk::WatcherDispatcher::InvokeWatchCallback(unsigned long, unsigned int, mojo::edk::HandleSignalsState const&, unsigned int) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/edk/system/watcher_dispatcher.cc:90:3
    #16 0x562d827fef6e in mojo::edk::Watch::InvokeCallback(unsigned int, mojo::edk::HandleSignalsState const&, unsigned int) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/edk/system/watch.cc:78:13
    #17 0x562d827f2eb6 in mojo::edk::RequestContext::~RequestContext() /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/edk/system/request_context.cc:66:20
    #18 0x562d827d35d4 in mojo::edk::NodeChannel::OnChannelMessage(void const*, unsigned long, std::__1::vector<mojo::edk::ScopedPlatformHandle, std::__1::allocator<mojo::edk::ScopedPlatformHandle> >) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/edk/system/node_channel.cc:755:1
    #19 0x562d827a91fb in mojo::edk::Channel::OnReadComplete(unsigned long, unsigned long*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/edk/system/channel.cc:731:18
    #20 0x562d82813e5a in mojo::edk::(anonymous namespace)::ChannelPosix::OnFileCanReadWithoutBlocking(int) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/edk/system/channel_posix.cc:314:14
    #21 0x562d87f04b8a in base::MessagePumpLibevent::OnLibeventNotification(int, short, void*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_pump_libevent.cc:0:13
    #22 0x562d87f1e1f8 in event_process_active /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/third_party/libevent/event.c:381:4
    #23 0x562d87f1e1f8 in event_base_loop /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/third_party/libevent/event.c:521:0
    #24 0x562d87f055cc in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_pump_libevent.cc:247:9
    #25 0x562d87da77a0 in base::RunLoop::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/run_loop.cc:131:14
    #26 0x562d87e2ad00 in base::Thread::ThreadMain() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/thread.cc:337:3
    #27 0x562d87efca20 in base::(anonymous namespace)::ThreadFunc(void*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/platform_thread_posix.cc:76:13
    #28 0x7f3b4e91a6b9 in start_thread ??:0:0

Thread T6 (Chrome_ChildIOT) created by T0 (chrome) here:
    #0 0x562d808c453d in __interceptor_pthread_create _asan_rtl_:3
    #1 0x562d87efbc9a in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, base::PlatformThreadHandle*, base::ThreadPriority) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/platform_thread_posix.cc:115:13
    #2 0x562d87e29fc5 in base::Thread::StartWithOptions(base::Thread::Options const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/threading/thread.cc:112:15
    #3 0x562d903a11f4 in content::ChildProcess::ChildProcess(base::ThreadPriority, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::unique_ptr<base::TaskScheduler::InitParams, std::__1::default_delete<base::TaskScheduler::InitParams> >) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/child/child_process.cc:62:3
    #4 0x562d95763548 in content::RenderProcess::RenderProcess(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::unique_ptr<base::TaskScheduler::InitParams, std::__1::default_delete<base::TaskScheduler::InitParams> >) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/renderer/render_process.cc:14:7
    #5 0x562d95762640 in content::RenderProcessImpl::RenderProcessImpl(std::__1::unique_ptr<base::TaskScheduler::InitParams, std::__1::default_delete<base::TaskScheduler::InitParams> >) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/renderer/render_process_impl.cc:102:7
    #6 0x562d957631ff in content::RenderProcessImpl::Create() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/renderer/render_process_impl.cc:214:11
    #7 0x562d96b99d75 in content::RendererMain(content::MainFunctionParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/renderer/renderer_main.cc:237:27
    #8 0x562d872917c8 in content::RunZygote(content::ContentMainDelegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:566:14
    #9 0x562d872952af in content::ContentMainRunnerImpl::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:964:10
    #10 0x562d872ba65d in service_manager::Main(service_manager::MainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../services/service_manager/embedder/main.cc:459:29
    #11 0x562d8728fe37 in content::ContentMain(content::ContentMainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main.cc:19:10
    #12 0x562d8090aa6f in ChromeMain /home/cowboy/chromium/src/out/chrome_asan_shared/../../chrome/app/chrome_main.cc:101:12
    #13 0x7f3b47b8482f in __libc_start_main /build/glibc-Cl5G7W/glibc-2.23/csu/../csu/libc-start.c:291:0

SUMMARY: AddressSanitizer: heap-use-after-free (/home/cowboy/chromium/src/out/chrome_asan_shared/chrome+0x1dca5cf6)
Shadow bytes around the buggy address:
  0x0c0c801a6640: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fa
  0x0c0c801a6650: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c0c801a6660: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x0c0c801a6670: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fa
  0x0c0c801a6680: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x0c0c801a6690: fd fd fd fd fd fd[fd]fa fa fa fa fa fa fa fa fa
  0x0c0c801a66a0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fa
  0x0c0c801a66b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c0c801a66c0: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x0c0c801a66d0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fa
  0x0c0c801a66e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==1==ABORTING

Did this work before? N/A 

Chrome version: Version 68.0.3430.0 (Developer Build) (64-bit)  Channel: dev
OS Version: Ubuntu 16.04
Flash Version:

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 4.2 KB)
- [asan_symbolized.log](attachments/asan_symbolized.log) (text/plain, 22.3 KB)
- [res.zip](attachments/res.zip) (application/octet-stream, 2.6 KB)
- [844833.zip](attachments/844833.zip) (application/octet-stream, 1.9 KB)
- [asan_symbolized2.log](attachments/asan_symbolized2.log) (text/plain, 19.7 KB)
- [asan_symbolized_withpatch.log](attachments/asan_symbolized_withpatch.log) (text/plain, 22.8 KB)

## Timeline

### cl...@chromium.org (2018-05-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5449753547243520.

### cl...@chromium.org (2018-05-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5873927335968768.

### cl...@chromium.org (2018-05-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6383913229090816.

### cl...@chromium.org (2018-05-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5774370128265216.

### cl...@chromium.org (2018-05-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5288010716020736.

### cl...@chromium.org (2018-05-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5572494585757696.

### mm...@chromium.org (2018-05-21)

Thanks for your report. I've managed to reproduce it using the most recent ASan build. I'm giving another try for CF, if it manages to reproduce, that will simplify the triage.

Please not that --no-sandbox doesn't affect reproducibility, this is needed for stacktrace symbolization.

### mm...@chromium.org (2018-05-22)

Still no luck with reproducing this on CF.

chcunningham@, could you please take a look and / or help to find an owner?

[Monorail components: Blink>Media>Audio]

### da...@chromium.org (2018-05-22)

[Empty comment from Monorail migration]

### ma...@chromium.org (2018-05-22)

Looks like set_copy_audio_bus_callback on the main thread races with actually using the copy_audio_bus_callback_ on the callback thread (https://cs.chromium.org/chromium/src/media/blink/webaudiosourceprovider_impl.cc?type=cs&sq=package:chromium&g=0&l=333). Over to WebAudio.

[Monorail components: Blink>WebAudio]

### cd...@gmail.com (2018-05-22)

@mmoroz
Yes,"--no-sandbox" option does not affect to repro,I forgot to remove this option.
And I tested with new build(Version 68.0.3437.0 (Developer Build) (64-bit)),and still can repro the UAF.

If you cannot reproduce it within 30 seconds, reopen the browser. 
In my local pc,Sometimes repro immediately,or sometimes repro when reopen the browser and run again.
I attached new asan_symbol_log.

### sh...@chromium.org (2018-05-22)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-05-22)

[Empty comment from Monorail migration]

### rt...@chromium.org (2018-05-22)

The repro test case doesn't involve webaudio in any way.  Reassigning to dalecurtis for further triage.

### cd...@gmail.com (2018-05-22)

Hi,@mmoroz
I found that it can not repro with vmmware(I tried about 10 times.)
did you try repro with real pc?

### da...@chromium.org (2018-05-22)

Looks like it just needs a lock given how the capturer is used. It clears the callback without lock. Not sure why we didn't have one during review, will look back at the context. Will send a cl today.

### da...@chromium.org (2018-05-22)

Wasn't able to repro, but the code is definitely wrong for the reasons in c#10:

https://chromium-review.googlesource.com/c/chromium/src/+/1069489

### bu...@chromium.org (2018-05-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c580d9aef17d7ed8ba0b697be81c2a7334624e59

commit c580d9aef17d7ed8ba0b697be81c2a7334624e59
Author: Dale Curtis <dalecurtis@chromium.org>
Date: Tue May 22 22:02:59 2018

Don't access WASP::TeeFilter without a lock.

This can lead to issues when the copy callback has been cleared,
but the old value has already been picked up by the render thread.

BUG=844833
TEST=none

Change-Id: I96cb0f5db1e9b28139e7a148fad135b434b2984b
Reviewed-on: https://chromium-review.googlesource.com/1069489
Reviewed-by: Miguel Casas <mcasas@chromium.org>
Commit-Queue: Dale Curtis <dalecurtis@chromium.org>
Cr-Commit-Position: refs/heads/master@{#560801}
[modify] https://crrev.com/c580d9aef17d7ed8ba0b697be81c2a7334624e59/media/blink/webaudiosourceprovider_impl.cc
[modify] https://crrev.com/c580d9aef17d7ed8ba0b697be81c2a7334624e59/media/blink/webaudiosourceprovider_impl.h


### da...@chromium.org (2018-05-22)

@cdsrc2016 can you try to repro with the patch in c#18? I wasn't able to reproduce myself, but that patch should fix it.

### cd...@gmail.com (2018-05-23)

Hi,@dalecur.
After patch,I still got same UAF,but I feel the repro less stable than before (after patch,run about 3 times to get UAF).

### da...@chromium.org (2018-05-23)

Thanks, I'll try to reproduce again tomorrow.

### da...@chromium.org (2018-05-23)

@cdsrc2016: To confirm you're getting the same ASAN stack trace after the patch?

### cd...@gmail.com (2018-05-24)

Yes,I got the same ASAN stack,here is the asan.log.


### da...@chromium.org (2018-05-24)

Was able to repro on 67.0.3396.56 linux: https://crash.corp.google.com/browse?stbtiq=dfde892af3c6a3cc but still haven't been able to get my dev build w/ asan to crash :(

### da...@chromium.org (2018-05-24)

Hmm, are you sure you have the patch applied cdsrc2016? This line in your stack trace:

0x55b4cd0c413c in media::WebAudioSourceProviderImpl::TeeFilter::Render(base::TimeDelta, base::TimeTicks, int, media::AudioBus*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../media/blink/webaudiosourceprovider_impl.cc:334:0

Should end with:

../../media/blink/webaudiosourceprovider_impl.cc:336:0

if the patch is applied correctly.

### da...@chromium.org (2018-05-24)

+@mmoroz, since you could repro above can you also retry with latest ToT?

### cd...@gmail.com (2018-05-25)

@dalecur
The useful code in patch is just 1 line(base::AutoLock auto_lock(sink_lock_);) right?
 void WebAudioSourceProviderImpl::ClearCopyAudioCallback() {
+  // Use |sink_lock_| to protect |tee_filter_| too since they go in lockstep.
+  base::AutoLock auto_lock(sink_lock_);
+
   DCHECK(tee_filter_);
   tee_filter_->set_copy_audio_bus_callback(CopyAudioCB());
 }

If yes,I'm sure I patched.


### da...@chromium.org (2018-05-25)

@cdsrc2016 do you have any local modifications that would cause your stack trace to be incorrect then?

I'll keep trying some more today to try and repro, but since I'm heading OOO soon will need to hand off back to someone more familiar with MediaStreams if the locking isn't hte issue.

[Monorail components: Blink>MediaStream]

### da...@chromium.org (2018-05-25)

Got a repro with content_shell. Digging more now. 

### da...@chromium.org (2018-05-25)

Ahh TeeFilter is used without a lock through RenderCallback interface. Fix forthcoming.

### mm...@chromium.org (2018-05-25)

Dale, do you still want me to test anything?

### da...@chromium.org (2018-05-25)

Nope, I got it. Thanks.

### da...@chromium.org (2018-05-25)

Here's a fairly ugly fix:
https://chromium-review.googlesource.com/c/chromium/src/+/1073913

The gist is that we were not completely protecting the |tee_filter_| and the copy audio callback inside... but we also don't want to add yet another lock to the audio hot path. Ultimately, we probably need to rethink the whole CopyAudioBusCallback() approach. Perhaps using something similar to what lives on the audio service side for "snooping" audio for capture.

### da...@chromium.org (2018-05-29)

Fix is in the CQ, =>olka for handling any merges that may be needed after it lands since I'll be OOO.

### bu...@chromium.org (2018-05-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/78923a9e70ee2f34290bd828ead3fdd91974a161

commit 78923a9e70ee2f34290bd828ead3fdd91974a161
Author: Dale Curtis <dalecurtis@chromium.org>
Date: Tue May 29 22:15:47 2018

Add a optional lock for when AudioBus copies are desired.

WebAudioSourceProviderImpl is an unfortunate beast. It lives on
the render thread but may be accessed for 3+ threads (media, render,
audio). This really needs to be simplified or at least sectioned
better.

In the vast majority of cases, WASP is simply a passthrough
class that does nothing but stay out of the way. When copying or
WebAudio is attached things get complicated. In the copying case
an external caller will provide a callback that is used to copy
each AudioBus as its output.

The bug in this case is that writes to the callback were being
protected by a lock, but reads were only sometimes being protected
depending on if WebAudio was attached or not.

The fix is to introduce a new lock for the copy callback, but since
the vast majority of the time we don't need one, use an std::atomic
to avoid introduces yet-more audio fulfillment delay.

BUG=844833
TEST=none.

Change-Id: Idc29b65c383c99cad34072048435c5eff61eada3
Reviewed-on: https://chromium-review.googlesource.com/1073913
Reviewed-by: Olga Sharonova <olka@chromium.org>
Commit-Queue: Dale Curtis <dalecurtis@chromium.org>
Cr-Commit-Position: refs/heads/master@{#562625}
[modify] https://crrev.com/78923a9e70ee2f34290bd828ead3fdd91974a161/media/blink/webaudiosourceprovider_impl.cc
[modify] https://crrev.com/78923a9e70ee2f34290bd828ead3fdd91974a161/media/blink/webaudiosourceprovider_impl.h


### sh...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-02)

olka: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ol...@chromium.org (2018-06-04)

mmoroz@, could you retry with ToT?

### ol...@chromium.org (2018-06-05)

[Empty comment from Monorail migration]

### ol...@chromium.org (2018-06-05)

@cdsrc2016 can you try to repro with #36?

### cd...@gmail.com (2018-06-05)

Hi,@olka
I tested more than 20 times and no UAF or other Unexpected errors appeared again.^-^

### mm...@chromium.org (2018-06-05)

olka@, I've just tried with https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-release-564503.zip?generation=1528212659938450&alt=media and haven't reproduced the crash.

### ol...@chromium.org (2018-06-05)

Re#42,43 - thanks for testing! Marking as fixed.

### ol...@chromium.org (2018-06-05)

[Empty comment from Monorail migration]

### ab...@google.com (2018-06-05)

Approving for merge to M68. BRanch:3440

### sh...@chromium.org (2018-06-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-06-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ada89e825eb351a6139a44a631905ffcea18d318

commit ada89e825eb351a6139a44a631905ffcea18d318
Author: Dale Curtis <dalecurtis@chromium.org>
Date: Thu Jun 07 07:49:30 2018

Add a optional lock for when AudioBus copies are desired.

WebAudioSourceProviderImpl is an unfortunate beast. It lives on
the render thread but may be accessed for 3+ threads (media, render,
audio). This really needs to be simplified or at least sectioned
better.

In the vast majority of cases, WASP is simply a passthrough
class that does nothing but stay out of the way. When copying or
WebAudio is attached things get complicated. In the copying case
an external caller will provide a callback that is used to copy
each AudioBus as its output.

The bug in this case is that writes to the callback were being
protected by a lock, but reads were only sometimes being protected
depending on if WebAudio was attached or not.

The fix is to introduce a new lock for the copy callback, but since
the vast majority of the time we don't need one, use an std::atomic
to avoid introduces yet-more audio fulfillment delay.

BUG=844833
TEST=none.

Change-Id: Idc29b65c383c99cad34072048435c5eff61eada3
Reviewed-on: https://chromium-review.googlesource.com/1073913
Reviewed-by: Olga Sharonova <olka@chromium.org>
Commit-Queue: Dale Curtis <dalecurtis@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#562625}(cherry picked from commit 78923a9e70ee2f34290bd828ead3fdd91974a161)
Reviewed-on: https://chromium-review.googlesource.com/1090531
Cr-Commit-Position: refs/branch-heads/3440@{#236}
Cr-Branched-From: 010ddcfda246975d194964ccf20038ebbdec6084-refs/heads/master@{#561733}
[modify] https://crrev.com/ada89e825eb351a6139a44a631905ffcea18d318/media/blink/webaudiosourceprovider_impl.cc
[modify] https://crrev.com/ada89e825eb351a6139a44a631905ffcea18d318/media/blink/webaudiosourceprovider_impl.h


### ol...@chromium.org (2018-06-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-06-15)

Nice one cdsrc2016@ - the VRP panel rewarded $2,000 for this report - cheers!

### aw...@chromium.org (2018-06-15)

[Empty comment from Monorail migration]

### cd...@gmail.com (2018-06-15)

Hi,@awhalley,thank you for the reward.
By the way,is it can get cve?
and my another one(https://bugs.chromium.org/p/chromium/issues/detail?id=830303)

### sh...@chromium.org (2018-09-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-09-12)

This issue was migrated from crbug.com/chromium/844833?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Media>Audio, Blink>MediaStream, Blink>WebAudio]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-27)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/chrome-blintz-user-guide

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091428)*
