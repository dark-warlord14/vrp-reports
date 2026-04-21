# AddressSanitizer: heap-use-after-free scoped_blocking_call_internal.cc:208 in base::internal::IOJankMonitoringWindow::OnBlockingCallCompleted

| Field | Value |
|-------|-------|
| **Issue ID** | [40055891](https://issues.chromium.org/issues/40055891) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Core |
| **Platforms** | Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | ga...@chromium.org |
| **Created** | 2021-05-16 |
| **Bounty** | $15,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4494.0 Safari/537.36

Steps to reproduce the problem:
#TestOn
Windows NT 10.0; Win64; x64
asan-win32-release_x64-880310

#SANDBOX
Need to pay attention to when the problem occurs in the browser process, so it may cause the sandbox escape

#Reproduce
python3.6m -m http.server 8000
chrome.exe --no-sandbox --js-flags='--expose_gc' --enable-blink-test-features --single-process --autoplay-policy=no-user-gesture-required --use-fake-device-for-media-stream --no-default-browser-check --disable-extensions --user-data-dir=chrome_test

open http://localhost:8000/fuzz-00015.html

The reproduction of this case seems to need to simulate the IO failure.
I captured it on the fuzzing machine. It may be that the fuzzing machine has many IO operations that caused the problem to be reproduced. 
The ASAN log provides a detailed vulnerability trigger path.
Hope it can help you find the root cause of the problem.

Note that this is *not* a renderer bug; it's a browser process bug that's reachable from the renderer.

What is the expected behavior?

What went wrong?
=================================================================
==8448==ERROR: AddressSanitizer: heap-use-after-free on address 0x102c805acaa0 at pc 0x7ffc240029c5 bp 0x00006444f080 sp 0x00006444f0c8
READ of size 16 at 0x102c805acaa0 thread T258
==8448==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ffc240029c4 in base::internal::IOJankMonitoringWindow::OnBlockingCallCompleted C:\b\s\w\ir\cache\builder\src\base\threading\scoped_blocking_call_internal.cc:208
    #1 0x7ffc240038ba in base::internal::UncheckedScopedBlockingCall::~UncheckedScopedBlockingCall C:\b\s\w\ir\cache\builder\src\base\threading\scoped_blocking_call_internal.cc:317
    #2 0x7ffc2195e86d in base::`anonymous namespace'::CancelableFileOperation<char,int (*)(void *, void *, unsigned long, unsigned long *, _OVERLAPPED *)> C:\b\s\w\ir\cache\builder\src\base\sync_socket_win.cc:204
    #3 0x7ffc2195eabd in base::CancelableSyncSocket::ReceiveWithTimeout C:\b\s\w\ir\cache\builder\src\base\sync_socket_win.cc:306
    #4 0x7ffc1c3a0fca in audio::SyncReader::WaitUntilDataIsReady C:\b\s\w\ir\cache\builder\src\services\audio\sync_reader.cc:258
    #5 0x7ffc1c3a0849 in audio::SyncReader::Read C:\b\s\w\ir\cache\builder\src\services\audio\sync_reader.cc:185
    #6 0x7ffc1c387abb in audio::OutputController::OnMoreData C:\b\s\w\ir\cache\builder\src\services\audio\output_controller.cc:433
    #7 0x7ffc1988a867 in media::OnMoreDataConverter::ProvideInput C:\b\s\w\ir\cache\builder\src\media\audio\audio_output_resampler.cc:485
    #8 0x7ffc198d3017 in media::AudioConverter::SourceCallback C:\b\s\w\ir\cache\builder\src\media\base\audio_converter.cc:222
    #9 0x7ffc198d412b in media::AudioConverter::ConvertWithDelay C:\b\s\w\ir\cache\builder\src\media\base\audio_converter.cc:155
    #10 0x7ffc1988a1a8 in media::OnMoreDataConverter::OnMoreData C:\b\s\w\ir\cache\builder\src\media\audio\audio_output_resampler.cc:469
    #11 0x7ffc198b0630 in media::WASAPIAudioOutputStream::RenderAudioFromSource C:\b\s\w\ir\cache\builder\src\media\audio\win\audio_low_latency_output_win.cc:692
    #12 0x7ffc198af436 in media::WASAPIAudioOutputStream::Run C:\b\s\w\ir\cache\builder\src\media\audio\win\audio_low_latency_output_win.cc:517
    #13 0x7ffc21962a1f in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:121
    #14 0x7ff60db5dac7 in __asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_thread.cpp:279
    #15 0x7ffca9084d2d in BaseThreadInitThunk+0x1d (C:\WINDOWS\System32\KERNEL32.DLL+0x180014d2d)
    #16 0x7ffcaa9d5a7a in RtlUserThreadStart+0x2a (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180065a7a)

0x102c805acaa8 is located 0 bytes to the right of 552-byte region [0x102c805ac880,0x102c805acaa8)
freed by thread T0 here:
    #0 0x7ff60db53bcb in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ffc2ac3e278 in cc::`anonymous namespace'::RasterTaskImpl::~RasterTaskImpl C:\b\s\w\ir\cache\builder\src\cc\tiles\tile_manager.cc:150
    #2 0x7ffc2dfab99f in cc::TileTaskManagerImpl::CheckForCompletedTasks C:\b\s\w\ir\cache\builder\src\cc\tiles\tile_task_manager.cc:46
    #3 0x7ffc2ac24442 in cc::TileManager::FlushAndIssueSignals C:\b\s\w\ir\cache\builder\src\cc\tiles\tile_manager.cc:1506
    #4 0x7ffc2dfab346 in base::internal::Invoker<base::internal::BindState<void (cc::UniqueNotifier::*)(),base::WeakPtr<cc::UniqueNotifier> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:690
    #5 0x7ffc2189101a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178
    #6 0x7ffc23ff1a5f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:357
    #7 0x7ffc23ff10d9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:270
    #8 0x7ffc21941c70 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:220
    #9 0x7ffc2193fe58 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #10 0x7ffc23ff3104 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:466
    #11 0x7ffc21816ba3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #12 0x7ffc1b0298bd in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1010
    #13 0x7ffc1b02ec25 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:152
    #14 0x7ffc1b022d22 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:47
    #15 0x7ffc215acbe8 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:597
    #16 0x7ffc215af51f in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1080
    #17 0x7ffc215ae72f in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:955
    #18 0x7ffc215aba97 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:372
    #19 0x7ffc215ac08b in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:398
    #20 0x7ffc1755145a in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:151
    #21 0x7ff60dab5bd1 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169
    #22 0x7ff60dab2c1d in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:369
    #23 0x7ff60de9bb7f in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #24 0x7ffca9084d2d in BaseThreadInitThunk+0x1d (C:\WINDOWS\System32\KERNEL32.DLL+0x180014d2d)
    #25 0x7ffcaa9d5a7a in RtlUserThreadStart+0x2a (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180065a7a)

previously allocated by thread T0 here:
    #0 0x7ff60db53ccb in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffc33b9852a in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
    #2 0x7ffc2ac31f5b in cc::TileManager::CreateRasterTask C:\b\s\w\ir\cache\builder\src\cc\tiles\tile_manager.cc:1331
    #3 0x7ffc2ac27eed in cc::TileManager::AssignGpuMemoryToTiles C:\b\s\w\ir\cache\builder\src\cc\tiles\tile_manager.cc:845
    #4 0x7ffc2ac267bb in cc::TileManager::PrepareTiles C:\b\s\w\ir\cache\builder\src\cc\tiles\tile_manager.cc:580
    #5 0x7ffc26de8143 in cc::LayerTreeHostImpl::PrepareTiles C:\b\s\w\ir\cache\builder\src\cc\trees\layer_tree_host_impl.cc:935
    #6 0x7ffc26de603f in cc::LayerTreeHostImpl::NotifyPendingTreeFullyPainted C:\b\s\w\ir\cache\builder\src\cc\trees\layer_tree_host_impl.cc:830
    #7 0x7ffc26de4335 in cc::LayerTreeHostImpl::UpdateSyncTreeAfterCommitOrImplSideInvalidation C:\b\s\w\ir\cache\builder\src\cc\trees\layer_tree_host_impl.cc:723
    #8 0x7ffc26de2ec2 in cc::LayerTreeHostImpl::CommitComplete C:\b\s\w\ir\cache\builder\src\cc\trees\layer_tree_host_impl.cc:631
    #9 0x7ffc26dd19ed in cc::SingleThreadProxy::DoCommit C:\b\s\w\ir\cache\builder\src\cc\trees\single_thread_proxy.cc:215
    #10 0x7ffc2abfc66f in cc::Scheduler::ProcessScheduledActions C:\b\s\w\ir\cache\builder\src\cc\scheduler\scheduler.cc:899
    #11 0x7ffc2abfdd4f in cc::Scheduler::NotifyReadyToCommit C:\b\s\w\ir\cache\builder\src\cc\scheduler\scheduler.cc:196
    #12 0x7ffc26dd51f0 in cc::SingleThreadProxy::DoPainting C:\b\s\w\ir\cache\builder\src\cc\trees\single_thread_proxy.cc:905
    #13 0x7ffc26dd6f00 in cc::SingleThreadProxy::BeginMainFrame C:\b\s\w\ir\cache\builder\src\cc\trees\single_thread_proxy.cc:875
    #14 0x7ffc26dd7e12 in base::internal::Invoker<base::internal::BindState<void (cc::SingleThreadProxy::*)(const viz::BeginFrameArgs &),base::WeakPtr<cc::SingleThreadProxy>,viz::BeginFrameArgs>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:690
    #15 0x7ffc2189101a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178
    #16 0x7ffc23ff1a5f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:357
    #17 0x7ffc23ff10d9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:270
    #18 0x7ffc21941c70 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:220
    #19 0x7ffc2193fe58 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #20 0x7ffc23ff3104 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:466
    #21 0x7ffc21816ba3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #22 0x7ffc1b0298bd in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1010
    #23 0x7ffc1b02ec25 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:152
    #24 0x7ffc1b022d22 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:47
    #25 0x7ffc215acbe8 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:597
    #26 0x7ffc215af51f in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1080
    #27 0x7ffc215ae72f in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:955
    #28 0x7ffc215aba97 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:372

Thread T258 created by T18 here:
    #0 0x7ff60db5e5b2 in __asan_wrap_CreateThread C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:146
    #1 0x7ffc21961dfe in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:185
    #2 0x7ffc218d5460 in base::SimpleThread::StartAsync C:\b\s\w\ir\cache\builder\src\base\threading\simple_thread.cc:51
    #3 0x7ffc218d52ec in base::SimpleThread::Start C:\b\s\w\ir\cache\builder\src\base\threading\simple_thread.cc:30
    #4 0x7ffc198adae8 in media::WASAPIAudioOutputStream::Start C:\b\s\w\ir\cache\builder\src\media\audio\win\audio_low_latency_output_win.cc:357
    #5 0x7ffc19881e00 in media::AudioOutputDispatcherImpl::StartStream C:\b\s\w\ir\cache\builder\src\media\audio\audio_output_dispatcher_impl.cc:96
    #6 0x7ffc19888ba8 in media::AudioOutputResampler::StartStream C:\b\s\w\ir\cache\builder\src\media\audio\audio_output_resampler.cc:355
    #7 0x7ffc19886bbe in media::AudioOutputProxy::Start C:\b\s\w\ir\cache\builder\src\media\audio\audio_output_proxy.cc:45
    #8 0x7ffc1c386548 in audio::OutputController::Play C:\b\s\w\ir\cache\builder\src\services\audio\output_controller.cc:319
    #9 0x7ffc1c38c614 in audio::OutputStream::Play C:\b\s\w\ir\cache\builder\src\services\audio\output_stream.cc:124
    #10 0x7ffc1969379c in media::mojom::AudioOutputStreamStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\media\mojo\mojom\audio_output_stream.mojom.cc:212
    #11 0x7ffc21cf09b4 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:858
    #12 0x7ffc2444f2a6 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #13 0x7ffc21d07a53 in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1076
    #14 0x7ffc21d06a2e in mojo::internal::MultiplexRouter::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:705
    #15 0x7ffc2444f2a6 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #16 0x7ffc21ceb471 in mojo::Connector::DispatchMessageW C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:539
    #17 0x7ffc21cece77 in mojo::Connector::ReadAllAvailableMessages C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:597
    #18 0x7ffc21d3c2fc in mojo::SimpleWatcher::OnHandleReady C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc:278
    #19 0x7ffc2189101a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178
    #20 0x7ffc23ff1a5f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:357
    #21 0x7ffc23ff10d9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:270
    #22 0x7ffc23fc520f in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:39
    #23 0x7ffc23ff3104 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:466
    #24 0x7ffc21816ba3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #25 0x7ffc218d78f9 in base::Thread::Run C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:312
    #26 0x7ffc218d7e10 in base::Thread::ThreadMain C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:383
    #27 0x7ffc21962a1f in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:121
    #28 0x7ff60db5dac7 in __asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_thread.cpp:279
    #29 0x7ffca9084d2d in BaseThreadInitThunk+0x1d (C:\WINDOWS\System32\KERNEL32.DLL+0x180014d2d)
    #30 0x7ffcaa9d5a7a in RtlUserThreadStart+0x2a (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180065a7a)

Thread T18 created by T0 here:
    #0 0x7ff60db5e5b2 in __asan_wrap_CreateThread C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:146
    #1 0x7ffc21961dfe in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:185
    #2 0x7ffc218d6bca in base::Thread::StartWithOptions C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:187
    #3 0x7ffc19890c89 in media::AudioThreadImpl::AudioThreadImpl C:\b\s\w\ir\cache\builder\src\media\audio\audio_thread_impl.cc:26
    #4 0x7ffc1b02b860 in content::BrowserMainLoop::InitializeAudio C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1473
    #5 0x7ffc1b027cbc in content::BrowserMainLoop::PostCreateThreadsImpl C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1265
    #6 0x7ffc1b027047 in content::BrowserMainLoop::PostCreateThreads C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:943
    #7 0x7ffc1bdbf283 in content::StartupTaskRunner::RunAllTasksNow C:\b\s\w\ir\cache\builder\src\content\browser\startup_task_runner.cc:41
    #8 0x7ffc1b0266e8 in content::BrowserMainLoop::CreateStartupTasks C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:868
    #9 0x7ffc1b02e125 in content::BrowserMainRunnerImpl::Initialize C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:131
    #10 0x7ffc1b022cd4 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:43
    #11 0x7ffc215acbe8 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:597
    #12 0x7ffc215af51f in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1080
    #13 0x7ffc215ae72f in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:955
    #14 0x7ffc215aba97 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:372
    #15 0x7ffc215ac08b in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:398
    #16 0x7ffc1755145a in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:151
    #17 0x7ff60dab5bd1 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169
    #18 0x7ff60dab2c1d in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:369
    #19 0x7ff60de9bb7f in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #20 0x7ffca9084d2d in BaseThreadInitThunk+0x1d (C:\WINDOWS\System32\KERNEL32.DLL+0x180014d2d)
    #21 0x7ffcaa9d5a7a in RtlUserThreadStart+0x2a (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180065a7a)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\base\threading\scoped_blocking_call_internal.cc:208 in base::internal::IOJankMonitoringWindow::OnBlockingCallCompleted
Shadow bytes around the buggy address:
  0x0206100b5900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0206100b5910: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0206100b5920: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0206100b5930: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0206100b5940: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0206100b5950: fd fd fd fd[fd]fa fa fa fa fa fa fa fa fa fa fa
  0x0206100b5960: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0206100b5970: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0206100b5980: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0206100b5990: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0206100b59a0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
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
==8448==ABORTING

Did this work before? N/A 

Chrome version: 92.0.4494.0  Channel: dev
OS Version: 10.0
Flash Version:

## Attachments

- [poc.zip](attachments/poc.zip) (application/octet-stream, 21.9 KB)
- [fuzz-00015.html](attachments/fuzz-00015.html) (text/plain, 63.1 KB)
- [viper.mp3](attachments/viper.mp3) (application/octet-stream, 3.3 KB)
- [viper.ogg](attachments/viper.ogg) (application/octet-stream, 2.5 KB)
- [asan_heap-buffer-overflow_on_address_1620888420857_811867_cr.html](attachments/asan_heap-buffer-overflow_on_address_1620888420857_811867_cr.html) (text/plain, 25.0 KB)
- [asan_heap-buffer-overflow_on_address_1621013750618_723460_cr.html](attachments/asan_heap-buffer-overflow_on_address_1621013750618_723460_cr.html) (text/plain, 17.5 KB)
- [asan_heap-buffer-overflow_on_address_1621081285572_830888_cr.html](attachments/asan_heap-buffer-overflow_on_address_1621081285572_830888_cr.html) (text/plain, 20.9 KB)
- [asan_heap-buffer-overflow_on_address_1621107985633_798066_cr.html](attachments/asan_heap-buffer-overflow_on_address_1621107985633_798066_cr.html) (text/plain, 26.7 KB)
- [asan_heap-buffer-overflow_on_address_1621199112669_747308_cr.html](attachments/asan_heap-buffer-overflow_on_address_1621199112669_747308_cr.html) (text/plain, 23.9 KB)
- [asan_heap-buffer-overflow_on_address_1621228114540_770024_cr.html](attachments/asan_heap-buffer-overflow_on_address_1621228114540_770024_cr.html) (text/plain, 23.8 KB)
- [asan_heap-buffer-overflow_on_address_1621235788938_142506_cr.html](attachments/asan_heap-buffer-overflow_on_address_1621235788938_142506_cr.html) (text/plain, 22.6 KB)
- [asan_heap-use-after-free_on_address_01620819091012_471010_cr.html](attachments/asan_heap-use-after-free_on_address_01620819091012_471010_cr.html) (text/plain, 19.0 KB)
- [asan_heap-use-after-free_on_address_01620934150316_618769_cr.html](attachments/asan_heap-use-after-free_on_address_01620934150316_618769_cr.html) (text/plain, 24.1 KB)
- [asan_heap-use-after-free_on_address_01621241568684_5470_cr.html](attachments/asan_heap-use-after-free_on_address_01621241568684_5470_cr.html) (text/plain, 20.8 KB)
- [asan_heap-use-after-free_on_address_01621249625972_718155_cr.html](attachments/asan_heap-use-after-free_on_address_01621249625972_718155_cr.html) (text/plain, 21.8 KB)
- [Screenshot 2021-05-18 121958.jpg](attachments/Screenshot 2021-05-18 121958.jpg) (image/jpeg, 180.4 KB)
- [foreproduce.diff](attachments/foreproduce.diff) (text/plain, 2.3 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 13.0 KB)
- [asan_breakpoint_on_unknown_address_0x7ffbce7de56d_pc 0x7ffbce7de56d 1627376232558_674693_cr.txt](attachments/asan_breakpoint_on_unknown_address_0x7ffbce7de56d_pc 0x7ffbce7de56d 1627376232558_674693_cr.txt) (text/plain, 17.0 KB)
- [asan_breakpoint_on_unknown_address_0x7ffbce7de56d_pc 0x7ffbce7de56d 1627382146697_804060_cr.txt](attachments/asan_breakpoint_on_unknown_address_0x7ffbce7de56d_pc 0x7ffbce7de56d 1627382146697_804060_cr.txt) (text/plain, 15.1 KB)

## Timeline

### [Deleted User] (2021-05-16)

[Empty comment from Monorail migration]

### xi...@chromium.org (2021-05-17)

Thanks for the report! Attaching the html file in the zip file. Next time please attach individual files directly instead of a zip file.

henrika@, could you take a look? Thanks!

[Monorail components: Internals>Media>Audio]

### he...@chromium.org (2021-05-17)

[Comment Deleted]

### he...@chromium.org (2021-05-17)

[Empty comment from Monorail migration]

### he...@chromium.org (2021-05-17)

Looks related to WebAudio APIs in [1]. Will try to reproduce locally but reassigning to WebAudio owner for now.

[1] fuzz-00015.html


### he...@chromium.org (2021-05-17)

[Empty comment from Monorail migration]

### he...@chromium.org (2021-05-17)

Are there any more details on how to reproduce this issue, building details etc.?

### m....@gmail.com (2021-05-17)

Unfortunately, these samples cannot be reproduced under normal circumstances. It is observed that the CPU and IO load of the system are very high when the crash occurs. 
Here are also some ASAN record files when the crash occurs. The crash point is the same but the trigger path is different. I hope it helps to find the root cause.

If you need samples associated with these logs, please let me know.


### he...@chromium.org (2021-05-17)

Which build flags are utilized when building Chrome?

### m....@gmail.com (2021-05-17)

gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-880310.zip

### ho...@chromium.org (2021-05-17)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebAudio]

### ho...@chromium.org (2021-05-17)

m.cooolie@

Is ASAN crash instant? Should I press something on the page to repro the crash?
I believe we can exclude mac; I wasn't able to reproduce the crash after several attempts. (rapid refresh, clicking buttons)
The problem here is that I can't see anything Web Audio in the stack trace above, but the repro code contains a lot of Web Audio JS codes.

### ho...@chromium.org (2021-05-17)

I'll try to repro this on Linux as well. For the time being, my Windows machine is not accessible and I might need to kick off a process to get my hands on.

### [Deleted User] (2021-05-17)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ho...@chromium.org (2021-05-17)

Couldn't repro on Linux either.

### ho...@chromium.org (2021-05-17)

henrika@

Would love to know if you're able to repro this on Windows.

Cc-ing adetaylor@ to get some advice on reproducing this on Win ASAN fuzzer.

### he...@chromium.org (2021-05-18)

Tried to reproduce using the instructions above but the test fails for me and it seems unrelated to the reported issue. Not sure how to proceed from here.

### he...@chromium.org (2021-05-18)

Should the test just keep running or am I supposed to klick things in any certain sequence?

### he...@chromium.org (2021-05-18)

Also, the tests above uses '--single-process' and that is only a test version of Chrome which is not officially supported.

https://www.chromium.org/developers/design-documents/process-models

"Finally, for the purposes of comparison, Chromium supports a single process model that can be enabled using the --single-process command-line switch. In this model, both the browser and rendering engine are run within a single OS process.

The single process model provides a baseline for measuring any overhead that the multi-process architectures impose. It is not a safe or robust architecture, as any renderer crash will cause the loss of the entire browser process. It is designed for testing and development purposes, and it may contain bugs that are not present in the other architectures."

### he...@chromium.org (2021-05-18)

m.cooolie@gmail.com@ are you able to reproduce the issue also without --single-process and --no-sandbox?  

### he...@chromium.org (2021-05-18)

[Empty comment from Monorail migration]

### m....@gmail.com (2021-05-18)

As I mentioned before, this only keeps appearing on fuzz machines. 
Analysis of the asan log and code found that the high load of the fuzz machine may have triggered the problem caused by the IOJankMonitoringWindow related code, which makes it difficult to reproduce under normal circumstances. 
We are now Try to modify the value of TimeDelta kMonitoringWindow to try to reproduce the problem. 
If you can’t reproduce it or find the problem through the asan log, you can close the case.

### he...@chromium.org (2021-05-18)

Thanks but my question still stands even if it only happens on fuzz machines. 

### he...@chromium.org (2021-05-18)

[Comment Deleted]

### he...@chromium.org (2021-05-18)

To use --single-process and --no-sandbox is not a requirement to run fuzz tests but it adds information to know if they are required to trigger the issue or not.

### he...@chromium.org (2021-05-20)

Reducing priority until we know if the issue can be reproduced with a real Chrome without --single-process and --no-sandbox flags.

### [Deleted User] (2021-05-20)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rt...@chromium.org (2021-05-20)

FWIW, I tried to reproduce this issue on my Windows machine using the command line args suggested.  I didn't get any crashes after letting it run for a while.  (For whatever reason, I generally have a hard time  reproducing asan issues on my windows machine.)

### ho...@chromium.org (2021-05-20)

Per https://crbug.com/chromium/1209622#c12, https://crbug.com/chromium/1209622#c15, https://crbug.com/chromium/1209622#c25, https://crbug.com/chromium/1209622#c28 - perhaps the right status for this issue is "unconfirmed".

adetaylor@ Could you help us run this on our CF bots?

### ho...@chromium.org (2021-05-24)

Re https://crbug.com/chromium/1209622#c22: 

> We are now Try to modify the value of TimeDelta kMonitoringWindow to try to reproduce the problem. 

m.cooolie@ Were you able to get a better repro case?

### ad...@chromium.org (2021-05-25)

Re https://crbug.com/chromium/1209622#c29 it's the security sheriff's job to reproduce bugs before passing them on (ideally on ClusterFuzz) -  xinghuilu@, sorry to be a pain, but could I ask you to do it as you were the relevant sheriff? I'm sheriff this week and therefore drowning in trying to reproduce all sorts of other bugs.

### m....@gmail.com (2021-05-26)

Re #30
I am trying to read the code understanding related logic, it looks quite complicated ~

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### m....@gmail.com (2021-05-27)

After in-depth reading and analysis code, the root cause is the vulnerability triggered by multi-threaded race conditions.
Function IojankMonitoringWindow :: MonitorNextJankWindowifNessary[1] is called in the thread pool, which may release the current_jank_window_ref[2] object when calling, the function iojankmonitoringWindow :: Addjank[3] may be accessed in other threads, resulting in the UAF triggered by the race condition.

In order to reproduce the vulnerability, I have modified some code execution conditions to make the race conditions more easily reproduced.
Running Chrome after finishing the patch will reproduce the issues.

//[1]
#base/threading/scoped_blocking_call_internal.cc:152
// Post a task to kick off the next monitoring window if no monitored thread
// beats us to it. Adjust the timing to alleviate any drift in the timer. Do
// this outside the lock to avoid scheduling tasks while holding it.

ThreadPool::PostDelayedTask(
  FROM_HERE, BindOnce([]() {
	IOJankMonitoringWindow::MonitorNextJankWindowIfNecessary(
		TimeTicks::Now());
  }),
  kMonitoringWindow - (recent_now - next_jank_window->start_time_));

//[2]
#base/threading/scoped_blocking_call_internal.cc:134
next_jank_window =
	MakeRefCounted<IOJankMonitoringWindow>(next_window_start_time);

if (current_jank_window_ref && !current_jank_window_ref->canceled_) {
  // If there are still IO operations in progress within
  // |current_jank_window_ref|, they have a ref to it and will be the ones
  // triggering ~IOJankMonitoringWindow(). When doing so, they will overlap
  // into the |next_jank_window| we are setting up (|next_| will also own a
  // ref so a very long jank can safely unwind across a chain of pending
  // |next_|'s).
  DCHECK(!current_jank_window_ref->next_);
  current_jank_window_ref->next_ = next_jank_window;
}

// Make |next_jank_window| the new current before releasing the lock.
current_jank_window_ref = next_jank_window;
}

//[3]
#base/threading/scoped_blocking_call_internal.cc:211
void IOJankMonitoringWindow::AddJank(int local_jank_start_index,
                                     int num_janky_intervals) {
  // Increment jank counts for intervals in this window. If
  // |num_janky_intervals| lands beyond kNumIntervals, the additional intervals
  // will be reported to |next_|.
  const int jank_end_index = local_jank_start_index + num_janky_intervals;
  const int local_jank_end_index = std::min(kNumIntervals, jank_end_index);

  {
    // Note: while this window could be |canceled| here we must add our count
    // unconditionally as it is only thread-safe to read |canceled| in
    // ~IOJankMonitoringWindow().
    AutoLock lock(intervals_lock_);
    for (int i = local_jank_start_index; i < local_jank_end_index; ++i)
      ++intervals_jank_count_[i];<<
  }


### ho...@chromium.org (2021-05-27)

This needs to be retriaged; it does not look like an audio issue at all.

I am not sure who's the owner of base/threading, so assigning to gab@ who worked on IOJankMonitoringWindow for further triaging.

Keeping WebAudio label because the repro code uses OfflineAudioContext.

[Monorail components: -Internals>Media>Audio]

### ho...@chromium.org (2021-05-27)

gab@ is on leave. Could you take a look olivierli@?

### [Deleted User] (2021-05-30)

olivierli: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ol...@chromium.org (2021-05-31)

I've started taking a look.

### ol...@chromium.org (2021-05-31)

Hello @m.coolie,

Can you pleas tell me more about the clock setup of your fuzzing machine?

Does it somehow override or mock the system clock?

Looking at the ASAN report and seeing "heap-buffer-overflow" makes me think that this is a problem with an out-of bounds access on the |intervals_jank_count_| member which can happen if the clock used is susceptible to time adjustments (it should not on Windows under normal circumstances) or timings are not consistent between processes.



### ol...@chromium.org (2021-05-31)

Ok you can forget my previous comment this does not seem likely after all since there is already code to not call AddJank() if call_end was ever smaller than call_start

### ch...@chromium.org (2021-05-31)

I think https://crbug.com/chromium/1209622#c34 is a bit of a red herring, because all of the access around current_jank_window is protected by a lock. This lock is used both when setting the new current jank window, and when reading the current jank window. Calls to OnBlockingCompleted from remote threads are to objects whose scoped_refptr was safely acquired behind this lock.

The only bit of raciness I can find seems to be around the |IOJankMonitoringWindow::next_| pointer. This is first created in OnBlockingCompleted, and then subsequently accessed in AddJank. However, two threads can race to create/read the next window. Something like this could happen:

On thread 1:
- OnBlockingCompleted is called
- next_ is created and set
- AddJank is called
- next_ is read

On thread 2:
- OnBlockingCompleted is called
- next_ is created and set, and the next_ object set by thread 1 is destroyed (reference count goes from 1 to 0)

Back over on thread 1:
- a new scoped_refptr instance tries to attach to the next set and read on thread 1, which was since destroyed on thread 2

### ch...@chromium.org (2021-05-31)

Okay... so the sequence of events in https://crbug.com/chromium/1209622#c41 isn't possible because setting |next_| occurs under a global lock, and then |current_window| is updated as well. So for any given window object, |next_| can only transition exactly once from null to non-null. Thus, subsequently reading from |next_| is always safe from any thread if you can guarantee that the potential write has already completed, which appears to occur in MonitorNextJankWindowIfNecessary.

Still digging into this...

### ch...@chromium.org (2021-05-31)

I'm struggling to see any unsafe patterns in the code after a careful audit.

Is it possible that there's a memory error in some other code that allocates objects with the same size class as the IOJankMonitoringWindow object? The sample traces show all sorts of type confusion in the "previously allocated here" stacks. On Windows ASAN bots don't have perfect coverage because they don't instrument third party code that gets injected. Thus it's possible for there to be uninstrumented pointers and memory accesses that can lead to corruption and confusion when blaming things when they eventually go wrong.

Is this reproducible on other platforms? Not in single process mode?

### si...@chromium.org (2021-05-31)

The size of the object is around 500 bytes in a 64 bit build.

### ch...@chromium.org (2021-05-31)

Given the random offsets and object sizes / types that are being blamed, is this just corrupt memory (uninstrumented writes, or quarantine too small to be effective), and we end up blaming the IO jank machinery simply because it's the most common operation that occurs on objects of this particular size class?

Separately, I *do* think there's a small race in reading |next_| at line 234. It's that one thread is reading |next_| in AddJank (when it was left null by OnBlockingCallCompleted), and that another thread is currently in the process of writing |next_|. This is fine on Intel (atomic pointer-sized writes), but might not be safe on other platforms? Likely all |next_| and |canceled_| access should be under a lock?

Also, this is a release build. Is it possible to build with dcheck_always_enabled? There are a bunch of DCHECKs that might provide more information here.

Also, we're only blamed line 208 (AddJank), without any particular line of AddJank. Would changing optimization levels lead to better symbols to help diagnose a little further?

### ho...@chromium.org (2021-06-03)

[Empty comment from Monorail migration]

[Monorail components: -Blink>WebAudio]

### ts...@chromium.org (2021-06-19)

[Empty comment from Monorail migration]

[Monorail components: Internals>Core]

### ad...@google.com (2021-07-08)

Setting FoundIn-91 to match Security_Impact-Stable. I have no additional information that this can be reproduced in M91. But this label will become important to Sheriffbot in the near future.

### rt...@chromium.org (2021-07-12)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-16)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ga...@chromium.org (2021-07-19)

Back and will take a look at this.

### ga...@chromium.org (2021-07-19)

[Empty comment from Monorail migration]

### ch...@chromium.org (2021-07-19)

FWIW gab, I'm still convinced that this is noise and blame-of-an-innocent-bystander. See https://crbug.com/chromium/1209622#c45.

### ga...@chromium.org (2021-07-20)

I see, then setting as Needs-Feedback + ExternalDependency while waiting on reply to #45.

### m....@gmail.com (2021-07-21)

re #45 #54
I compiled a debug version, patched it whith #34, and output the following error message.

chrome.exe --no-sandbox  --user-data-dir=0721
```
[1464:19976:0721/111635.296:FATAL:lock.cc(23)] Check failed: owning_thread_ref_ == PlatformThread::CurrentRef(). 
Backtrace:
	base::debug::CollectStackTrace [0x00007FFCBE763F67+39] (E:\v8\chromium\src\base\debug\stack_trace_win.cc:303)
	base::debug::StackTrace::StackTrace [0x00007FFCBE46CB7D+77] (E:\v8\chromium\src\base\debug\stack_trace.cc:200)
	base::debug::StackTrace::StackTrace [0x00007FFCBE46CB15+37] (E:\v8\chromium\src\base\debug\stack_trace.cc:197)
	logging::LogMessage::~LogMessage [0x00007FFCBE4BF7BB+187] (E:\v8\chromium\src\base\logging.cc:589)
	logging::LogMessage::~LogMessage [0x00007FFCBE4C0FBC+44] (E:\v8\chromium\src\base\logging.cc:583)
	logging::CheckError::~CheckError [0x00007FFCBE42AAFF+47] (E:\v8\chromium\src\base\check.cc:107)
	base::Lock::AssertAcquired [0x00007FFCBE619F75+165] (E:\v8\chromium\src\base\synchronization\lock.cc:24)
	base::internal::BasicAutoLock<base::Lock>::~BasicAutoLock [0x00007FFCBE42197B+27] (E:\v8\chromium\src\base\synchronization\lock_impl.h:139)
	base::internal::IOJankMonitoringWindow::AddJank [0x00007FFCBE6FB925+229] (E:\v8\chromium\src\base\threading\scoped_blocking_call_internal.cc:228)
	base::internal::IOJankMonitoringWindow::OnBlockingCallCompleted [0x00007FFCBE6FAE54+468] (E:\v8\chromium\src\base\threading\scoped_blocking_call_internal.cc:209)
	base::internal::IOJankMonitoringWindow::ScopedMonitoredCall::~ScopedMonitoredCall [0x00007FFCBE6FAB76+118] (E:\v8\chromium\src\base\threading\scoped_blocking_call_internal.cc:66)
	absl::optional_internal::optional_data_dtor_base<base::internal::IOJankMonitoringWindow::ScopedMonitoredCall,0>::destruct [0x00007FFCBE6FC8BA+42] (E:\v8\chromium\src\third_party\abseil-cpp\absl\types\internal\optional.h:94)
	absl::optional_internal::optional_data_dtor_base<base::internal::IOJankMonitoringWindow::ScopedMonitoredCall,0>::~optional_data_dtor_base [0x00007FFCBE6FC883+19] (E:\v8\chromium\src\third_party\abseil-cpp\absl\types\internal\optional.h:106)
	absl::optional_internal::optional_data_base<base::internal::IOJankMonitoringWindow::ScopedMonitoredCall>::~optional_data_base [0x00007FFCBE6FC863+19] (E:\v8\chromium\src\third_party\abseil-cpp\absl\types\internal\optional.h:137)
	absl::optional_internal::optional_data<base::internal::IOJankMonitoringWindow::ScopedMonitoredCall,0>::~optional_data [0x00007FFCBE6FC843+19] (E:\v8\chromium\src\third_party\abseil-cpp\absl\types\internal\optional.h:195)
	absl::optional<base::internal::IOJankMonitoringWindow::ScopedMonitoredCall>::~optional [0x00007FFCBE6FC513+19] (E:\v8\chromium\src\third_party\abseil-cpp\absl\types\optional.h:263)
	base::internal::UncheckedScopedBlockingCall::~UncheckedScopedBlockingCall [0x00007FFCBE6FC443+307] (E:\v8\chromium\src\base\threading\scoped_blocking_call_internal.cc:317)
	base::ScopedBlockingCall::~ScopedBlockingCall [0x00007FFCBE6F9524+228] (E:\v8\chromium\src\base\threading\scoped_blocking_call.cc:60)
	`anonymous namespace'::RecordProcessorMetrics [0x00007FFC7638FAE2+242] (E:\v8\chromium\src\chrome\services\util_win\processor_metrics.cc:140)
	ProcessorMetricsImpl::RecordProcessorMetrics [0x00007FFC7638FD34+68] (E:\v8\chromium\src\chrome\services\util_win\processor_metrics.cc:159)
	chrome::mojom::ProcessorMetricsStubDispatch::AcceptWithResponder [0x00007FFC73E2B748+600] (E:\v8\chromium\src\out\0330_debug\gen\chrome\services\util_win\public\mojom\util_win.mojom.cc:1595)
	chrome::mojom::ProcessorMetricsStub<mojo::RawPtrImplRefTraits<chrome::mojom::ProcessorMetrics> >::AcceptWithResponder [0x00007FFC76390C45+149] (E:\v8\chromium\src\out\0330_debug\gen\chrome\services\util_win\public\mojom\util_win.mojom.h:252)
	mojo::InterfaceEndpointClient::HandleValidatedMessage [0x00007FFCD7A349FE+878] (E:\v8\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:853)
	mojo::InterfaceEndpointClient::HandleIncomingMessageThunk::Accept [0x00007FFCD7A34681+33] (E:\v8\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:329)
	mojo::MessageDispatcher::Accept [0x00007FFCD7A4FED2+338] (E:\v8\chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43)
	mojo::InterfaceEndpointClient::HandleIncomingMessage [0x00007FFCD7A37A94+100] (E:\v8\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:650)
	mojo::internal::MultiplexRouter::ProcessIncomingMessage [0x00007FFCD7A5A1B7+1575] (E:\v8\chromium\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1098)
	mojo::internal::MultiplexRouter::Accept [0x00007FFCD7A59665+629] (E:\v8\chromium\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:717)
	mojo::MessageDispatcher::Accept [0x00007FFCD7A4FED2+338] (E:\v8\chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43)
	mojo::Connector::DispatchMessageW [0x00007FFCD7A1CB29+1129] (E:\v8\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:548)
	mojo::Connector::ReadAllAvailableMessages [0x00007FFCD7A1DC96+502] (E:\v8\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:608)
	mojo::Connector::OnHandleReadyInternal [0x00007FFCD7A1D8B2+162] (E:\v8\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:441)
	mojo::Connector::OnWatcherHandleReady [0x00007FFCD7A1D7FB+27] (E:\v8\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:411)
	base::internal::FunctorTraits<void (mojo::Connector::*)(unsigned int),void>::Invoke<void (mojo::Connector::*)(unsigned int),mojo::Connector *,unsigned int> [0x00007FFCD7A24FA5+69] (E:\v8\chromium\src\base\bind_internal.h:509)
	base::internal::InvokeHelper<0,void>::MakeItSo<void (mojo::Connector::*const &)(unsigned int),mojo::Connector *,unsigned int> [0x00007FFCD7A24EDD+77] (E:\v8\chromium\src\base\bind_internal.h:648)
	base::internal::Invoker<base::internal::BindState<void (mojo::Connector::*)(unsigned int),base::internal::UnretainedWrapper<mojo::Connector> >,void (unsigned int)>::RunImpl<void (mojo::Connector::*const &)(unsigned int),const std::tuple<base::internal::Un [0x00007FFCD7A24E71+113] (E:\v8\chromium\src\base\bind_internal.h:721)
	base::internal::Invoker<base::internal::BindState<void (mojo::Connector::*)(unsigned int),base::internal::UnretainedWrapper<mojo::Connector> >,void (unsigned int)>::Run [0x00007FFCD7A24DDE+94] (E:\v8\chromium\src\base\bind_internal.h:703)
	base::RepeatingCallback<void (unsigned int)>::Run [0x00007FFCD7A20D51+113] (E:\v8\chromium\src\base\callback.h:166)
	mojo::SimpleWatcher::DiscardReadyState [0x00007FFCD7A20500+32] (E:\v8\chromium\src\mojo\public\cpp\system\simple_watcher.h:190)
	base::internal::FunctorTraits<void (*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),void>::Invoke<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::Hand [0x00007FFCD7A208D6+102] (E:\v8\chromium\src\base\bind_internal.h:404)
	base::internal::InvokeHelper<0,void>::MakeItSo<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),const base::RepeatingCallback<void (unsigned int)> &,unsigned int,const mojo::HandleSignal [0x00007FFCD7A207F6+102] (E:\v8\chromium\src\base\bind_internal.h:648)
	base::internal::Invoker<base::internal::BindState<void (*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo::HandleSignalsSt [0x00007FFCD7A20771+129] (E:\v8\chromium\src\base\bind_internal.h:721)
	base::internal::Invoker<base::internal::BindState<void (*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo::HandleSignalsSt [0x00007FFCD7A206DC+124] (E:\v8\chromium\src\base\bind_internal.h:703)
	base::RepeatingCallback<void (unsigned int, const mojo::HandleSignalsState &)>::Run [0x00007FFCDDACA65A+138] (E:\v8\chromium\src\base\callback.h:166)
	mojo::SimpleWatcher::OnHandleReady [0x00007FFCDDACA2D9+377] (E:\v8\chromium\src\mojo\public\cpp\system\simple_watcher.cc:279)
	base::internal::FunctorTraits<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &),void>::Invoke<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher>,int,unsign [0x00007FFCDDACB100+128] (E:\v8\chromium\src\base\bind_internal.h:509)
	base::internal::InvokeHelper<1,void>::MakeItSo<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher>,int,unsigned int,mojo::HandleSignalsState> [0x00007FFCDDACAF54+164] (E:\v8\chromium\src\base\bind_internal.h:671)
	base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher>,int,unsigned int,mojo::HandleSignalsState>,void ()>::RunImpl<void (mojo::SimpleWatcher: [0x00007FFCDDACAE8A+186] (E:\v8\chromium\src\base\bind_internal.h:721)
	base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher>,int,unsigned int,mojo::HandleSignalsState>,void ()>::RunOnce [0x00007FFCDDACADC5+85] (E:\v8\chromium\src\base\bind_internal.h:690)
	base::OnceCallback<void ()>::Run [0x00007FFCBE421A97+119] (E:\v8\chromium\src\base\callback.h:99)
	base::TaskAnnotator::RunTask [0x00007FFCBE637502+1266] (E:\v8\chromium\src\base\task\common\task_annotator.cc:180)
	base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl [0x00007FFCBE68A7AB+1915] (E:\v8\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:361)
	base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork [0x00007FFCBE689D26+294] (E:\v8\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:260)
	base::MessagePumpDefault::Run [0x00007FFCBE4ED1E1+145] (E:\v8\chromium\src\base\message_loop\message_pump_default.cc:40)
	base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run [0x00007FFCBE68B31F+671] (E:\v8\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:470)
	base::RunLoop::Run [0x00007FFCBE5BBA2D+749] (E:\v8\chromium\src\base\run_loop.cc:134)
	base::Thread::Run [0x00007FFCBE7099ED+349] (E:\v8\chromium\src\base\threading\thread.cc:341)
	base::Thread::ThreadMain [0x00007FFCBE709F54+1284] (E:\v8\chromium\src\base\threading\thread.cc:412)
	base::`anonymous namespace'::ThreadFunc [0x00007FFCBE79BFF8+440] (E:\v8\chromium\src\base\threading\platform_thread_win.cc:123)
	BaseThreadInitThunk [0x00007FFD0DE87034+20]
	RtlUserThreadStart [0x00007FFD0FCA2651+33]
Task trace:
Backtrace:
	mojo::SimpleWatcher::ArmOrNotify [0x00007FFCDDAC9A5F+575] (E:\v8\chromium\src\mojo\public\cpp\system\simple_watcher.cc:238)
	content::`anonymous namespace'::ServiceBinderImpl::BindServiceInterface [0x00007FFC70F42D05+1029] (E:\v8\chromium\src\content\utility\utility_thread_impl.cc:82)
	mojo::SimpleWatcher::ArmOrNotify [0x00007FFCDDAC9A5F+575] (E:\v8\chromium\src\mojo\public\cpp\system\simple_watcher.cc:238)
	content::ChildThreadImpl::Init [0x00007FFC6D18DED6+4198] (E:\v8\chromium\src\content\child\child_thread_impl.cc:681)
	content::InProcessUtilityThread::Init [0x00007FFC70F2D643+131] (E:\v8\chromium\src\content\utility\in_process_utility_thread.cc:37)


```

### [Deleted User] (2021-07-21)

[Empty comment from Monorail migration]

### ch...@chromium.org (2021-07-21)

The failure in https://crbug.com/chromium/1209622#c55 does seem to indicate that there is a UAF on the memory occupied by the lock. For the failure path to occur there must be racy access to the lock memory, and it must involve some piece of code treating that memory *not* as a lock, and not using the appropriate semanics to write to it. The question is then whether the lock reference to the memory is valid (other code is at fault) or if the non-lock reference is valid (the jank monitoring code is at fault).

So this doesn't yet prove to me that the jank monitoring code is performing a use-after-free. A possible sequence of events is for some other code with a stale pointer to be doing a double free (causing the jank-monitoring object to be freed), But it is certainly suspicious.

### ga...@chromium.org (2021-07-21)

I can repro with the diff in #34 and running base_unittests --gtest_filter=ScopedBlockingCallIOJankMonitoringTest.Basic

Seems something really weird is happening, I get the same failure as in #55 with Check failed: owning_thread_ref_ == PlatformThread::CurrentRef(). But there's only one thread. Adding logging I get an (43833 vs. 43832) and further logging confirms that the original value stored in owning_thread_ref_  was 43832. So something is touching the last bit.

I'm digging.

### ga...@chromium.org (2021-07-21)

[Empty comment from Monorail migration]

### ga...@chromium.org (2021-07-22)

I think I've figured it out.

The repro from #34 causes two "impossible" situations to occur:
 1) By adding 40ms to |recent_now| in MonitorNextJankWindowIfNecessary() it caused ScopedMonitoredCall::call_start_ to be behind ScopedMonitoredCall::assigned_jank_window_->start_time_ by 40ms when that ScopedMonitoredCall creates the window. This should never happen because TimeTicks is supposed to be monotonically increasing.
 2) By forcing the delayed task at the end of MonitorNextJankWindowIfNecessary() to be at 10ms it reordered when the next window is created. The next window assumes it's responsible for |next_window_start_time = current_jank_window_ref->start_time_ + kMonitoringWindow| and hence monitors the future.

Both of these cause a |past - future| computation in OnBlockingCallCompleted() and results in a negative |jank_start_index|. This in turn results in indexing negatively into |intervals_jank_count_| when AddJank() performs |++intervals_jank_count_[i]| on i = [local_jank_start_index, local_jank_end_index).

Nonetheless the repro highlights that *if* the TimeTicks monotonic clock *was* to move backwards. The logic in this file breaks down. This should never happen under regular conditions in the browser process AFAIK but maybe it's possible under single-process fuzzing mode. For instance, there's a devtools API (Emulation.setVirtualTimePolicy) that allows overriding TimeTicks for the entire renderer process. Under --single-process this would also affect the browser process (EnableIOJankMonitoringForProcess() is only invoked in the browser process so this code is typically inactive in renderers).

I've written https://chromium-review.googlesource.com/c/chromium/src/+/3042207 to protect against OOB-indexing in the very rare cases where this can happen. I'm not convinced this can happen in the browser process in production hence lowering Security_Severity

### ga...@chromium.org (2021-07-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-07-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c91f42272129eca38cc3c6b85784c4bf9cddfe58

commit c91f42272129eca38cc3c6b85784c4bf9cddfe58
Author: Gabriel Charette <gab@chromium.org>
Date: Thu Jul 22 17:36:29 2021

[base] Improve logging of DCHECKs in lock.cc

This proved useful when debugging crbug.com/1209622#c55

R=danakj@chromium.org

Bug: 1209622
Change-Id: Ia588e561fae01d16050d15e18ca8eb39d71b4a30
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3043085
Commit-Queue: Gabriel Charette <gab@chromium.org>
Commit-Queue: danakj <danakj@chromium.org>
Auto-Submit: Gabriel Charette <gab@chromium.org>
Reviewed-by: danakj <danakj@chromium.org>
Cr-Commit-Position: refs/heads/master@{#904384}

[modify] https://crrev.com/c91f42272129eca38cc3c6b85784c4bf9cddfe58/base/synchronization/lock.cc
[modify] https://crrev.com/c91f42272129eca38cc3c6b85784c4bf9cddfe58/base/threading/platform_thread.cc
[modify] https://crrev.com/c91f42272129eca38cc3c6b85784c4bf9cddfe58/base/threading/platform_thread.h


### gi...@appspot.gserviceaccount.com (2021-07-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6ff4fee50c9cd36c2f0f0463244e2ea2593e056c

commit 6ff4fee50c9cd36c2f0f0463244e2ea2593e056c
Author: Gabriel Charette <gab@chromium.org>
Date: Fri Jul 23 20:56:53 2021

[base] Make IOJankMonitoringWindow robust to a non-monotonic tick clock

The repro @ crbug.com/1209622#c34 involved an impossible TimeTicks
value because it added 40ms to |recent_now|, causing |call_start_| to
be behind |assigned_jank_window_->start_time_| which is not possible
unless the monotonic tick clock somehow ticks backwards. Harden
against this unexpected condition.

Also harden a few more preconditions.

Bug: 1209622
Change-Id: I34450bf661f45414e69db4411ae63a9b5700b2a7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3042207
Commit-Queue: Gabriel Charette <gab@chromium.org>
Reviewed-by: Chris Hamilton <chrisha@chromium.org>
Cr-Commit-Position: refs/heads/master@{#904891}

[modify] https://crrev.com/6ff4fee50c9cd36c2f0f0463244e2ea2593e056c/base/threading/scoped_blocking_call_internal.cc
[modify] https://crrev.com/6ff4fee50c9cd36c2f0f0463244e2ea2593e056c/base/threading/scoped_blocking_call_internal.h
[modify] https://crrev.com/6ff4fee50c9cd36c2f0f0463244e2ea2593e056c/base/threading/scoped_blocking_call_unittest.cc


### ga...@chromium.org (2021-07-26)

Looking for instances of this new CHECK being hit I stumbled upon a crash which I think is this issue (http://crash/f08bf9e12d27e4cd) on 94.0.4581.0 (before r904891 -- 94.0.4585.0). And other similar ones at a very low frequency : go/dyirs

But no crashes past 94.0.4581.0 yet (so none of the CHECK).

### ga...@chromium.org (2021-07-26)

@chrisha:
Re. #45 : "Separately, I *do* think there's a small race in reading |next_| at line 234. It's that one thread is reading |next_| in AddJank (when it was left null by OnBlockingCallCompleted), and that another thread is currently in the process of writing |next_|. This is fine on Intel (atomic pointer-sized writes), but might not be safe on other platforms? Likely all |next_| and |canceled_| access should be under a lock?"

I initially thought you were right but now convinced myself otherwise. The read of |next_| in AddJank() on L234 cannot race with a write because |next_| can only have been written from one of two situations:
 (1) The call to MonitorNextJankWindowIfNecessary() from OnBlockingCallCompleted() on the same thread just before calling AddJank().
 (2) A call to MonitorNextJankWindowIfNecessary() on another thread which was synchronized with the current thread by (1) acquiring the lock to realize it didn't need to do it itself.

Since we only read |next_| when the jank overlaps into the next window and the creation of the next window happens-before this read (per 1&2 above), it's not racy.


There's clearly some logic that's flawed though because I just stumbled upon something which had fallen off my radar : ScopedBlockingCallIOJankMonitoringTest.MultiThreadedOverlappedWindows is flaky. Was disabled on CrOS+Linux but looks like it's flaking on all platforms : https://crbug.com/chromium/1071166 has all the details. I'll focus my attention there to see if there's a link.

### ga...@chromium.org (2021-07-26)

@m.cooolie@gmail.com: could you try the fuzzer on a build @ 6ff4fee50c9cd36c2f0f0463244e2ea2593e056c and report the logs if you can trip this check on Windows?

The patch will be reverted on trunk for now, so you'll need to be at that specific revision to test.

Thanks!

### gi...@appspot.gserviceaccount.com (2021-07-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/62d89fe5f479354a579d8b5ca7a3bced36cdbc68

commit 62d89fe5f479354a579d8b5ca7a3bced36cdbc68
Author: Gabriel Charette <gab@chromium.org>
Date: Tue Jul 27 01:17:38 2021

[base] Document more prereqs of IOJank constants with static_asserts

R=chrisha@chromium.org

Bug: 1209622
Change-Id: I07085fa2cebc054454675eb3641793174874020b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3054398
Auto-Submit: Gabriel Charette <gab@chromium.org>
Commit-Queue: Chris Hamilton <chrisha@chromium.org>
Reviewed-by: Chris Hamilton <chrisha@chromium.org>
Cr-Commit-Position: refs/heads/master@{#905533}

[modify] https://crrev.com/62d89fe5f479354a579d8b5ca7a3bced36cdbc68/base/threading/scoped_blocking_call_internal.h


### m....@gmail.com (2021-07-27)

#66
I would love to try it, can I find the compiled version from gs://chromium-browser-asan/win32-release_x64/?

### m....@gmail.com (2021-07-27)

#66
I triggered this check on version on asan-win32-release_x64-905113.




### gi...@appspot.gserviceaccount.com (2021-07-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4929a06ef55d96c519523eedece8fa7dfee0e1f7

commit 4929a06ef55d96c519523eedece8fa7dfee0e1f7
Author: Victor Vianna <victorvianna@google.com>
Date: Tue Jul 27 12:17:23 2021

Revert "[base] Document more prereqs of IOJank constants with static_asserts"

This reverts commit 62d89fe5f479354a579d8b5ca7a3bced36cdbc68.

Reason for revert: Unrolling changes after 6ff4fee50c9cd36c2f0f0463244e2ea2593e056c

Original change's description:
> [base] Document more prereqs of IOJank constants with static_asserts
>
> R=​chrisha@chromium.org
>
> Bug: 1209622
> Change-Id: I07085fa2cebc054454675eb3641793174874020b
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3054398
> Auto-Submit: Gabriel Charette <gab@chromium.org>
> Commit-Queue: Chris Hamilton <chrisha@chromium.org>
> Reviewed-by: Chris Hamilton <chrisha@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#905533}

Bug: 1209622, 1233483
Change-Id: I934e3d7dca96231095fb7e7e8e057c606fcbeb6f
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3055247
Auto-Submit: Victor Vianna <victorvianna@google.com>
Owners-Override: Victor Vianna <victorvianna@google.com>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#905691}

[modify] https://crrev.com/4929a06ef55d96c519523eedece8fa7dfee0e1f7/base/threading/scoped_blocking_call_internal.h


### gi...@appspot.gserviceaccount.com (2021-07-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/84dc40483c5dde99e4c833d3afe166bdf2b4024a

commit 84dc40483c5dde99e4c833d3afe166bdf2b4024a
Author: Gabriel Charette <gab@chromium.org>
Date: Tue Jul 27 13:08:03 2021

Revert "[base] Make IOJankMonitoringWindow robust to a non-monotonic tick clock"

This reverts commit 6ff4fee50c9cd36c2f0f0463244e2ea2593e056c.

Reason for revert: top crasher on Android...

Original change's description:
> [base] Make IOJankMonitoringWindow robust to a non-monotonic tick clock
>
> The repro @ crbug.com/1209622#c34 involved an impossible TimeTicks
> value because it added 40ms to |recent_now|, causing |call_start_| to
> be behind |assigned_jank_window_->start_time_| which is not possible
> unless the monotonic tick clock somehow ticks backwards. Harden
> against this unexpected condition.
>
> Also harden a few more preconditions.
>
> Bug: 1209622
> Change-Id: I34450bf661f45414e69db4411ae63a9b5700b2a7
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3042207
> Commit-Queue: Gabriel Charette <gab@chromium.org>
> Reviewed-by: Chris Hamilton <chrisha@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#904891}

No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: 1209622, 1232736
Change-Id: I50af255f6db47748b8bde2391034b973435a12e4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3054400
Commit-Queue: Victor Vianna <victorvianna@google.com>
Owners-Override: Victor Vianna <victorvianna@google.com>
Reviewed-by: Chris Hamilton <chrisha@chromium.org>
Cr-Commit-Position: refs/heads/master@{#905701}

[modify] https://crrev.com/84dc40483c5dde99e4c833d3afe166bdf2b4024a/base/threading/scoped_blocking_call_internal.cc
[modify] https://crrev.com/84dc40483c5dde99e4c833d3afe166bdf2b4024a/base/threading/scoped_blocking_call_internal.h
[modify] https://crrev.com/84dc40483c5dde99e4c833d3afe166bdf2b4024a/base/threading/scoped_blocking_call_unittest.cc


### gi...@appspot.gserviceaccount.com (2021-07-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b32c57df33d3e6d3e090f9f10bc1ec69c2d09fdc

commit b32c57df33d3e6d3e090f9f10bc1ec69c2d09fdc
Author: Gabriel Charette <gab@chromium.org>
Date: Thu Jul 29 22:24:54 2021

[base] Hotfix OOB-indexing in IOJank and document prereqs

This is a mix of crrev.com/904891 and crrev.com/905533 without
non-debug checks. To be merged as a hotfix to Stable while the real
fix is being worked on.

Bug: 1209622
Change-Id: I1b0abf784ba94c1b0573b6435af329d3c345431b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3055036
Commit-Queue: Gabriel Charette <gab@chromium.org>
Auto-Submit: Gabriel Charette <gab@chromium.org>
Reviewed-by: Chris Hamilton <chrisha@chromium.org>
Cr-Commit-Position: refs/heads/master@{#906876}

[modify] https://crrev.com/b32c57df33d3e6d3e090f9f10bc1ec69c2d09fdc/base/threading/scoped_blocking_call_internal.cc
[modify] https://crrev.com/b32c57df33d3e6d3e090f9f10bc1ec69c2d09fdc/base/threading/scoped_blocking_call_internal.h
[modify] https://crrev.com/b32c57df33d3e6d3e090f9f10bc1ec69c2d09fdc/base/threading/scoped_blocking_call_unittest.cc


### m....@gmail.com (2021-07-30)

https://crbug.com/chromium/1209622#c60 It seems that this is not an impossible situation, so do we need to adjust the security to high?

### ga...@chromium.org (2021-07-30)

[Empty comment from Monorail migration]

### ga...@chromium.org (2021-07-30)

[Empty comment from Monorail migration]

### ga...@chromium.org (2021-08-01)

No crashes (ref. #64) since r906876.

@m.cooolie to verify the fix on their end.

Requesting merge of r906876 for stability issue. Security-wise, it'd be quite difficult to exploit this race I think but the fix is trivial and worth it no-less.

@etiennep to perform merge while I'm OOO next week.

### [Deleted User] (2021-08-01)

This bug requires manual review: Reverts referenced in bugdroid comments after merge request.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), govind@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-08-02)

Hi etiennep@ & gab@ (when you return), this issue appears to be fully fixed with the combined CL of r906876. Please update the status of this issue as Fixed and we and Sheriffbot will take care of the rest. You do not need to manually request merges for security fixes. Thank you! 



### et...@chromium.org (2021-08-03)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-08-03)

please go ahead and merge to M93, branch 4577 asap (before 2pm PDT today), so it can be a part of this weeks beta release; thank you! 

### am...@chromium.org (2021-08-03)

[Empty comment from Monorail migration]

### et...@chromium.org (2021-08-03)

Cherry-picked create here: https://chromium-review.googlesource.com/c/chromium/src/+/3068021
but I need approval? gab@ is OOO.

### si...@chromium.org (2021-08-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d535a10e66bd49b42d83d02ecb845924a9251626

commit d535a10e66bd49b42d83d02ecb845924a9251626
Author: Gabriel Charette <gab@chromium.org>
Date: Wed Aug 04 19:43:58 2021

[base] Hotfix OOB-indexing in IOJank and document prereqs

This is a mix of crrev.com/904891 and crrev.com/905533 without
non-debug checks. To be merged as a hotfix to Stable while the real
fix is being worked on.

(cherry picked from commit b32c57df33d3e6d3e090f9f10bc1ec69c2d09fdc)

Bug: 1209622
Change-Id: I1b0abf784ba94c1b0573b6435af329d3c345431b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3055036
Commit-Queue: Gabriel Charette <gab@chromium.org>
Auto-Submit: Gabriel Charette <gab@chromium.org>
Reviewed-by: Chris Hamilton <chrisha@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#906876}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3068021
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Etienne Pierre-Doray <etiennep@chromium.org>
Reviewed-by: Olivier Li <olivierli@google.com>
Reviewed-by: Wez <wez@chromium.org>
Auto-Submit: Etienne Pierre-Doray <etiennep@chromium.org>
Cr-Commit-Position: refs/branch-heads/4577@{#441}
Cr-Branched-From: 761ddde228655e313424edec06497d0c56b0f3c4-refs/heads/master@{#902210}

[modify] https://crrev.com/d535a10e66bd49b42d83d02ecb845924a9251626/base/threading/scoped_blocking_call_internal.cc
[modify] https://crrev.com/d535a10e66bd49b42d83d02ecb845924a9251626/base/threading/scoped_blocking_call_internal.h
[modify] https://crrev.com/d535a10e66bd49b42d83d02ecb845924a9251626/base/threading/scoped_blocking_call_unittest.cc


### mp...@chromium.org (2021-08-09)

[Empty comment from Monorail migration]

### wf...@chromium.org (2021-08-11)

#72 implies more fixes are coming, is this bug totally fixed?

### am...@google.com (2021-08-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-11)

Congratulations! The VRP Panel has awarded you $15,000 for this report. Thank you for reporting this issue! 

### et...@chromium.org (2021-08-11)

wfh@: I think gab@ meant this is an ugly solution to a situation that shouldn't happen. The bug is fixed, but it could be prettier with better synchronization. 

### ga...@chromium.org (2021-08-13)

Re. #87/90: Right. r906876 fixes the bug by discarding monitoring of that instance when the bug occurs. The better fix which I'll work on when I'm back is to handle the race and still have monitoring in the rare cases where this occurs, that's going to be slightly more advanced and not suitable for a Stable merge.

### am...@google.com (2021-08-13)

[Empty comment from Monorail migration]

### ga...@chromium.org (2021-08-26)

[Empty comment from Monorail migration]

### ga...@chromium.org (2021-08-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-08-30)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-31)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-03)

[Empty comment from Monorail migration]

### as...@google.com (2021-09-08)

[Empty comment from Monorail migration]

### as...@google.com (2021-09-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-08)

[Empty comment from Monorail migration]

### ma...@google.com (2021-09-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4ef5266d00ff8baafd1039d1bef1cfed87d554fa

commit 4ef5266d00ff8baafd1039d1bef1cfed87d554fa
Author: Gabriel Charette <gab@chromium.org>
Date: Fri Sep 10 14:02:59 2021

[M90-LTS][base] Hotfix OOB-indexing in IOJank and document prereqs

This is a mix of crrev.com/904891 and crrev.com/905533 without
non-debug checks. To be merged as a hotfix to Stable while the real
fix is being worked on.

(cherry picked from commit b32c57df33d3e6d3e090f9f10bc1ec69c2d09fdc)

(cherry picked from commit d535a10e66bd49b42d83d02ecb845924a9251626)

Bug: 1209622
Change-Id: I1b0abf784ba94c1b0573b6435af329d3c345431b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3055036
Commit-Queue: Gabriel Charette <gab@chromium.org>
Auto-Submit: Gabriel Charette <gab@chromium.org>
Reviewed-by: Chris Hamilton <chrisha@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#906876}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3068021
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Etienne Pierre-Doray <etiennep@chromium.org>
Reviewed-by: Olivier Li <olivierli@google.com>
Reviewed-by: Wez <wez@chromium.org>
Auto-Submit: Etienne Pierre-Doray <etiennep@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4577@{#441}
Cr-Original-Branched-From: 761ddde228655e313424edec06497d0c56b0f3c4-refs/heads/master@{#902210}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3148057
Reviewed-by: Gabriel Charette <gab@chromium.org>
Reviewed-by: Jana Grill <janagrill@google.com>
Commit-Queue: Artem Sumaneev <asumaneev@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1595}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/4ef5266d00ff8baafd1039d1bef1cfed87d554fa/base/threading/scoped_blocking_call_internal.cc
[modify] https://crrev.com/4ef5266d00ff8baafd1039d1bef1cfed87d554fa/base/threading/scoped_blocking_call_internal.h
[modify] https://crrev.com/4ef5266d00ff8baafd1039d1bef1cfed87d554fa/base/threading/scoped_blocking_call_unittest.cc


### as...@google.com (2021-09-10)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/52e1634ec29cb287fbe5ae829dfe67ac19465fe2

commit 52e1634ec29cb287fbe5ae829dfe67ac19465fe2
Author: Gabriel Charette <gab@chromium.org>
Date: Fri Sep 10 19:21:53 2021

[base] Real fix for sampling race in ScopedMonitoredCall

Added a test that replicates the race and can be forced to fail under
the following conditions:
 1) Comment out the fix in ScopedMonitoredCall::ScopedMonitoredCall

 2) Add this before task_environment_.AdvanceClock(kDeltaFromBoundary);
  // Sleep the test thread a little bit to let the workers sample Now() before
  // advancing the clock.
  PlatformThread::Sleep(TimeDelta::FromMilliseconds(10));

3) Add this at the top of MonitorNextJankWindowIfNecessary():
  // Only count ScopedBlockingCalls in the test (the test framework triggers a
  // bunch before that point).
  bool enabled = false;
  {
    AutoLock lock(current_jank_window_lock());
    enabled = !!reporting_callback_storage();
  }
  // Sleep for the first 4 (kNumRacingThreads) calls to let the test thread get
  // ahead and move the window in front of the workers' sampled |call_start_|.
  static int x = 0;
  if (enabled && x++ < 4)
    PlatformThread::Sleep(TimeDelta::FromMilliseconds(50));

The test passes in the presence of 2.+3. but without commenting
out 1.; confirming that the fix works.

This allows deleting ScopedBlockingCallIOJankMonitoringManualMockTimeTest
which were flaky. Global time moving backwards was causing havoc for
unrelated checks (namely the ThreadPool's ServiceThread running into
Now() <= recent_now).

R=chrisha@chromium.org

Fixed: 1209622, 1235945
Change-Id: Iccb08ae7c2879f8a6241fbe8f5c9239402fe9ac2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3146031
Auto-Submit: Gabriel Charette <gab@chromium.org>
Reviewed-by: Chris Hamilton <chrisha@chromium.org>
Commit-Queue: Gabriel Charette <gab@chromium.org>
Cr-Commit-Position: refs/heads/main@{#920326}

[modify] https://crrev.com/52e1634ec29cb287fbe5ae829dfe67ac19465fe2/base/threading/scoped_blocking_call_internal.cc
[modify] https://crrev.com/52e1634ec29cb287fbe5ae829dfe67ac19465fe2/base/threading/scoped_blocking_call_internal.h
[modify] https://crrev.com/52e1634ec29cb287fbe5ae829dfe67ac19465fe2/base/threading/scoped_blocking_call_unittest.cc


### [Deleted User] (2021-11-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1209622?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/1071166]
[Monorail blocking: crbug.com/chromium/1236278]
[Monorail mergedwith: crbug.com/chromium/1078326, crbug.com/chromium/1110547, crbug.com/chromium/1233832, crbug.com/chromium/1238148, crbug.com/chromium/1242955]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055891)*
