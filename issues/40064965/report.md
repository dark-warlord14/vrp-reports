# Security: heap-use-after-free on LibcastSocketService

| Field | Value |
|-------|-------|
| **Issue ID** | [40064965](https://issues.chromium.org/issues/40064965) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>Cast>Providers |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | mf...@chromium.org |
| **Created** | 2023-05-29 |
| **Bounty** | $16,000.00 |

## Description

VULNERABILITY DETAILS
## Bisect
Based on the analysis with bisect, it was determined that the vulnerability was introduced by this commit: https://source.chromium.org/chromium/chromium/src/+/1834fac498edb068c7fc036ca6e834d330ef5bad
```
Use libcast CastSocket in CastSocketService

This change makes CastSocketService use libcast's CastSocket to back all
the Cast channels it opens.  This change is compatible with both the
extension and native MRPs.  Although the API and state management are
slightly different between Chromium's existing CastSocket and libcast's,
this change should keep observable behavior very similar.

Bug: 1050913
Change-Id: Ibfae4cecd0c1a27f660fc13e3f463542eb8ede05
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2714892
Commit-Queue: Brandon Tolsch <btolsch@chromium.org>
Reviewed-by: mark a. foltz <mfoltz@chromium.org>
Cr-Commit-Position: refs/heads/master@{#858785}
```

## RCA
This is a race condition vulnerability, as indicated by ASAN LOG. The functions create/free and use are executed in two different threads, T11 and T0, respectively. T11 is an IO thread created by T0 using BrowserTaskExecutor::CreateIOThread.

allocate: LibcastSocketService is derived from CastSocketService, which is a global singleton. Based on the constructor and comments, it runs on the IO thread. In the same IO thread, LibcastSocketService::OnConnectedIOThread creates a CastSocketWrapper object [0], which inherits from CastSocket, and stores it in the sockets_ container [1] of LibcastSocketService, managing its lifecycle.

free: In the LibcastSocketService::OnConnectedIOThread function, a KeepAliveHandler is registered and bound with LibcastSocketService::OnErrorBounce [2] function. This is done to detect any abnormalities in the socket and notify the observer to invoke the corresponding handling logic. Ultimately, it will invoke CastMediaSinkServiceImpl::OnError [3] function.
When CastMediaSinkServiceImpl::OnError [4] is triggered, it sends a callback, CastSocketService::RemoveSocket, to the IO thread. Eventually, this will invoke LibcastSocketService::RemoveSocket and erase the previously created CastSocketWrapper object from the sockets_ container [5], triggering the free operation.

use: The field transport_ [6] of the CastSocketWrapper object creates a callback [7] when calling the SendMessage function, which is then sent to the openscreen_task_runner_ from the UI thread. Inside the callback, it accesses the CastSocketWrapper that has already been freed in the IO thread [8], causing a use-after-free vulnerability.

[0] https://source.chromium.org/chromium/chromium/src/+/main:components/media_router/common/providers/cast/channel/libcast_socket_service.cc;l=377;drc=10c56a7c2d1f9bf623a1bbdd506683a430594267
[1] https://source.chromium.org/chromium/chromium/src/+/main:components/media_router/common/providers/cast/channel/libcast_socket_service.cc;l=390;drc=10c56a7c2d1f9bf623a1bbdd506683a430594267
[2] https://source.chromium.org/chromium/chromium/src/+/main:components/media_router/common/providers/cast/channel/libcast_socket_service.cc;l=383;drc=10c56a7c2d1f9bf623a1bbdd506683a430594267
[3] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:components/media_router/common/providers/cast/channel/libcast_socket_service.cc;l=333;drc=10c56a7c2d1f9bf623a1bbdd506683a430594267
[4] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/media/router/discovery/mdns/cast_media_sink_service_impl.cc;l=352;drc=10c56a7c2d1f9bf623a1bbdd506683a430594267
[5] https://source.chromium.org/chromium/chromium/src/+/main:components/media_router/common/providers/cast/channel/libcast_socket_service.cc;l=192;drc=10c56a7c2d1f9bf623a1bbdd506683a430594267
[6] https://source.chromium.org/chromium/chromium/src/+/main:components/media_router/common/providers/cast/channel/libcast_socket_service.cc;l=163;drc=10c56a7c2d1f9bf623a1bbdd506683a430594267
[7] https://source.chromium.org/chromium/chromium/src/+/main:components/media_router/common/providers/cast/channel/libcast_socket_service.cc;l=93;drc=10c56a7c2d1f9bf623a1bbdd506683a430594267
[8] https://source.chromium.org/chromium/chromium/src/+/main:components/media_router/common/providers/cast/channel/libcast_socket_service.cc;l=94;drc=10c56a7c2d1f9bf623a1bbdd506683a430594267

VERSION
Chrome Version: 116.0.5800.0
Operating System: Windows
TestOn: asan-win32-release_x64-1150200, Version 116.0.5800.0 (Developer Build) (64-bit), Window 10
Download From Here: https://commondatastorage.googleapis.com/chromium-browser-asan/index.html?prefix=win32-release_x64/asan-win32-release_x64-1150200

REPRODUCTION CASE
The vulnerability was triggered by my fuzzer, which requires enabling LibcastSocketService with the --enable-features=LibcastSocketService flag. However, it does not require any interaction and only needs to trigger a socket error to cause a use-after-free in the browser process. This is likely an exploitable vulnerability.
I am unable to provide a minimized poc at this time. However, I have provided the root cause analysis and ASAN log to assist with the vulnerability fix.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: browser
Crash State: see asan log

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 14.0 KB)
- [asan.log](attachments/asan.log) (text/plain, 14.0 KB)

## Timeline

### je...@gmail.com (2023-05-29)

VULNERABILITY DETAILS
## Bisect
Based on the analysis with bisect, it was determined that the vulnerability was introduced by this commit: https://source.chromium.org/chromium/chromium/src/+/1834fac498edb068c7fc036ca6e834d330ef5bad
```
Use libcast CastSocket in CastSocketService

This change makes CastSocketService use libcast's CastSocket to back all
the Cast channels it opens.  This change is compatible with both the
extension and native MRPs.  Although the API and state management are
slightly different between Chromium's existing CastSocket and libcast's,
this change should keep observable behavior very similar.

Bug: 1050913
Change-Id: Ibfae4cecd0c1a27f660fc13e3f463542eb8ede05
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2714892
Commit-Queue: Brandon Tolsch <btolsch@chromium.org>
Reviewed-by: mark a. foltz <mfoltz@chromium.org>
Cr-Commit-Position: refs/heads/master@{#858785}
```

## RCA
This is a race condition vulnerability, as indicated by ASAN LOG. The functions create/free and use are executed in two different threads, T11 and T0, respectively. T11 is an IO thread created by T0 using BrowserTaskExecutor::CreateIOThread.

allocate: LibcastSocketService is derived from CastSocketService, which is a global singleton. Based on the constructor and comments, it runs on the IO thread. In the same IO thread, LibcastSocketService::OnConnectedIOThread creates a CastSocketWrapper object [0], which inherits from CastSocket, and stores it in the sockets_ container [1] of LibcastSocketService, managing its lifecycle.

free: In the LibcastSocketService::OnConnectedIOThread function, a KeepAliveHandler is registered and bound with LibcastSocketService::OnErrorBounce [2] function. This is done to detect any abnormalities in the socket and notify the observer to invoke the corresponding handling logic. Ultimately, it will invoke CastMediaSinkServiceImpl::OnError [3] function.
When CastMediaSinkServiceImpl::OnError [4] is triggered, it sends a callback, CastSocketService::RemoveSocket, to the IO thread. Eventually, this will invoke LibcastSocketService::RemoveSocket and erase the previously created CastSocketWrapper object from the sockets_ container [5], triggering the free operation.

use: The field transport_ [6] of the CastSocketWrapper object creates a callback [7] when calling the SendMessage function, which is then sent to the openscreen_task_runner_ from the UI thread. Inside the callback, it accesses the CastSocketWrapper that has already been freed in the IO thread [8], causing a use-after-free vulnerability.

[0] https://source.chromium.org/chromium/chromium/src/+/main:components/media_router/common/providers/cast/channel/libcast_socket_service.cc;l=377;drc=10c56a7c2d1f9bf623a1bbdd506683a430594267
[1] https://source.chromium.org/chromium/chromium/src/+/main:components/media_router/common/providers/cast/channel/libcast_socket_service.cc;l=390;drc=10c56a7c2d1f9bf623a1bbdd506683a430594267
[2] https://source.chromium.org/chromium/chromium/src/+/main:components/media_router/common/providers/cast/channel/libcast_socket_service.cc;l=383;drc=10c56a7c2d1f9bf623a1bbdd506683a430594267
[3] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:components/media_router/common/providers/cast/channel/libcast_socket_service.cc;l=333;drc=10c56a7c2d1f9bf623a1bbdd506683a430594267
[4] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/media/router/discovery/mdns/cast_media_sink_service_impl.cc;l=352;drc=10c56a7c2d1f9bf623a1bbdd506683a430594267
[5] https://source.chromium.org/chromium/chromium/src/+/main:components/media_router/common/providers/cast/channel/libcast_socket_service.cc;l=192;drc=10c56a7c2d1f9bf623a1bbdd506683a430594267
[6] https://source.chromium.org/chromium/chromium/src/+/main:components/media_router/common/providers/cast/channel/libcast_socket_service.cc;l=163;drc=10c56a7c2d1f9bf623a1bbdd506683a430594267
[7] https://source.chromium.org/chromium/chromium/src/+/main:components/media_router/common/providers/cast/channel/libcast_socket_service.cc;l=93;drc=10c56a7c2d1f9bf623a1bbdd506683a430594267
[8] https://source.chromium.org/chromium/chromium/src/+/main:components/media_router/common/providers/cast/channel/libcast_socket_service.cc;l=94;drc=10c56a7c2d1f9bf623a1bbdd506683a430594267

VERSION
Chrome Version: 116.0.5800.0
Operating System: Windows
TestOn: asan-win32-release_x64-1150200, Version 116.0.5800.0 (Developer Build) (64-bit), Window 10
Download From Here: https://commondatastorage.googleapis.com/chromium-browser-asan/index.html?prefix=win32-release_x64/asan-win32-release_x64-1150200

REPRODUCTION CASE
The vulnerability was triggered by my fuzzer, which requires enabling LibcastSocketService with the --enable-features=LibcastSocketService flag. However, it does not require any interaction and only needs to trigger a socket error to cause a use-after-free in the browser process. This is likely an exploitable vulnerability.
I am unable to provide a minimized poc at this time. However, I have provided the root cause analysis and ASAN log to assist with the vulnerability fix.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: browser
Crash State: see asan log

### [Deleted User] (2023-05-29)

[Empty comment from Monorail migration]

### je...@gmail.com (2023-05-29)

The following is the asan log reproduced using asan-win32-release_x64-1150200


==77560==ERROR: AddressSanitizer: heap-use-after-free on address 0x1256131264a0 at pc 0x7ffe84229587 bp 0x00c7831fe280 sp 0x00c7831fe2c8
READ of size 8 at 0x1256131264a0 thread T0
==77560==WARNING: Failed to use and restart external symbolizer!
[86628:108816:0529/225114.625:INFO:peer_connection_dependency_factory.cc(629)] Running WebRTC with a combined Network and Worker thread.
[97616:36804:0529/225114.835:INFO:peer_connection_dependency_factory.cc(629)] Running WebRTC with a combined Network and Worker thread.
    #0 0x7ffe84229586 in std::__Cr::__packaged_task_func<`lambda at ..\..\components\media_router\common\providers\cast\channel\libcast_socket_service.cc:93:11',std::__Cr::allocator<`lambda at ..\..\components\media_router\common\providers\cast\channel\libcast_socket_service.cc:93:11'>,void ()>::operator() C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\future:1705
    #1 0x7ffe6dbc4e69 in std::__Cr::packaged_task<void ()>::operator() C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\future:2093
    #2 0x7ffe6dbc49c1 in openscreen_platform::`anonymous namespace'::ExecuteTask C:\b\s\w\ir\cache\builder\src\components\openscreen_platform\task_runner.cc:23
    #3 0x7ffe6dbc53d4 in base::internal::FunctorTraits<void (*)(std::__Cr::packaged_task<void ()>),void>::Invoke<void (*)(std::__Cr::packaged_task<void ()>),std::__Cr::packaged_task<void ()> > C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:636
    #4 0x7ffe6dbc515f in base::internal::Invoker<base::internal::BindState<void (*)(std::__Cr::packaged_task<void ()>),std::__Cr::packaged_task<void ()> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:976
    #5 0x7ffe713f3b36 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:186
    #6 0x7ffe74a0e222 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:486
    #7 0x7ffe74a0cf9f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:351
    #8 0x7ffe71330ed0 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:211
    #9 0x7ffe7132e956 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:77
    #10 0x7ffe74a1090f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:651
    #11 0x7ffe7145e2a7 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #12 0x7ffe6b3dbc33 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1067
    #13 0x7ffe6b3e2e3f in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:158
    #14 0x7ffe6b3d38aa in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:34
    #15 0x7ffe6fb5d8d5 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:707
    #16 0x7ffe6fb61991 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1284
    #17 0x7ffe6fb610db in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1138
    #18 0x7ffe6fb5b9cf in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:326
    #19 0x7ffe6fb5c6d9 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:343
    #20 0x7ffe638a171d in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:187
    #21 0x7ff7cf5663e4 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:166
    #22 0x7ff7cf562bd8 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:390
    #23 0x7ff7cf9922cb in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #24 0x7ffefa467033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)
    #25 0x7ffefc1c2650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

0x1256131264a0 is located 64 bytes inside of 112-byte region [0x125613126460,0x1256131264d0)
freed by thread T11 here:
    #0 0x7ff7cf61f23d in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ffe84228187 in cast_channel::CastSocketWrapper::~CastSocketWrapper C:\b\s\w\ir\cache\builder\src\components\media_router\common\providers\cast\channel\libcast_socket_service.cc:121
    #2 0x7ffe7dc7ecdc in base::internal::Invoker<base::internal::BindState<base::internal::IgnoreResultHelper<std::__Cr::unique_ptr<cast_channel::CastSocket,std::__Cr::default_delete<cast_channel::CastSocket> > (cast_channel::CastSocketService::*)(int)>,base::internal::UnretainedWrapper<cast_channel::CastSocketService,base::unretained_traits::MayNotDangle,0>,int>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:976
    #3 0x7ffe713f3b36 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:186
    #4 0x7ffe74a0e222 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:486
    #5 0x7ffe74a0cf9f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:351
    #6 0x7ffe71335232 in base::MessagePumpForIO::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:713
    #7 0x7ffe7132e956 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:77
    #8 0x7ffe74a1090f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:651
    #9 0x7ffe7145e2a7 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #10 0x7ffe713b75ed in base::Thread::Run C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:342
    #11 0x7ffe6b3e6c39 in content::BrowserProcessIOThread::IOThreadRun C:\b\s\w\ir\cache\builder\src\content\browser\browser_process_io_thread.cc:119
    #12 0x7ffe713b7abe in base::Thread::ThreadMain C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:414
    #13 0x7ffe7130eca1 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:133
    #14 0x7ff7cf615cf5 in __asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_thread.cpp:291
    #15 0x7ffefa467033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)
    #16 0x7ffefc1c2650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

previously allocated by thread T11 here:
    #0 0x7ff7cf61f33d in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffe87111c9e in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
    #2 0x7ffe842215ff in cast_channel::LibcastSocketService::OnConnectedIOThread C:\b\s\w\ir\cache\builder\src\components\media_router\common\providers\cast\channel\libcast_socket_service.cc:377
    #3 0x7ffe84225964 in base::internal::Invoker<base::internal::BindState<void (cast_channel::LibcastSocketService::*)(openscreen::cast::SenderSocketFactory *, const openscreen::IPEndpoint &, std::__Cr::unique_ptr<openscreen::cast::CastSocket,std::__Cr::default_delete<openscreen::cast::CastSocket> >),base::internal::UnretainedWrapper<cast_channel::LibcastSocketService,base::unretained_traits::MayNotDangle,0>,base::internal::UnretainedWrapper<openscreen::cast::SenderSocketFactory,base::unretained_traits::MayNotDangle,0>,openscreen::IPEndpoint,std::__Cr::unique_ptr<openscreen::cast::CastSocket,std::__Cr::default_delete<openscreen::cast::CastSocket> > >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:976
    #4 0x7ffe713f3b36 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:186
    #5 0x7ffe74a0e222 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:486
    #6 0x7ffe74a0cf9f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:351
    #7 0x7ffe71335232 in base::MessagePumpForIO::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:713
    #8 0x7ffe7132e956 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:77
    #9 0x7ffe74a1090f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:651
    #10 0x7ffe7145e2a7 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #11 0x7ffe713b75ed in base::Thread::Run C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:342
    #12 0x7ffe6b3e6c39 in content::BrowserProcessIOThread::IOThreadRun C:\b\s\w\ir\cache\builder\src\content\browser\browser_process_io_thread.cc:119
    #13 0x7ffe713b7abe in base::Thread::ThreadMain C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:414
    #14 0x7ffe7130eca1 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:133
    #15 0x7ff7cf615cf5 in __asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_thread.cpp:291
    #16 0x7ffefa467033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)
    #17 0x7ffefc1c2650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

Thread T11 created by T0 here:
    #0 0x7ff7cf614832 in __asan_wrap_CreateThread C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:146
    #1 0x7ffe7130dacf in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:198
    #2 0x7ffe713b6771 in base::Thread::StartWithOptions C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:215
    #3 0x7ffe6c61fe8c in content::BrowserTaskExecutor::CreateIOThread C:\b\s\w\ir\cache\builder\src\content\browser\scheduler\browser_task_executor.cc:301
    #4 0x7ffe6fb621da in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1254
    #5 0x7ffe6fb610db in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1138
    #6 0x7ffe6fb5b9cf in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:326
    #7 0x7ffe6fb5c6d9 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:343
    #8 0x7ffe638a171d in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:187
    #9 0x7ff7cf5663e4 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:166
    #10 0x7ff7cf562bd8 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:390
    #11 0x7ff7cf9922cb in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #12 0x7ffefa467033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)
    #13 0x7ffefc1c2650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\future:1705 in std::__Cr::__packaged_task_func<`lambda at ..\..\components\media_router\common\providers\cast\channel\libcast_socket_service.cc:93:11',std::__Cr::allocator<`lambda at ..\..\components\media_router\common\providers\cast\channel\libcast_socket_service.cc:93:11'>,void ()>::operator()
Shadow bytes around the buggy address:
  0x125613126200: fd fd fa fa fa fa fa fa f7 fa fd fd fd fd fd fd
  0x125613126280: fd fd fd fd fd fd fd fd fa fa fa fa fa fa f7 fa
  0x125613126300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa
  0x125613126380: fa fa fa fa f7 fa fd fd fd fd fd fd fd fd fd fd
  0x125613126400: fd fd fd fd fa fa fa fa fa fa f7 fa fd fd fd fd
=>0x125613126480: fd fd fd fd[fd]fd fd fd fd fd fa fa fa fa fa fa
  0x125613126500: f7 fa fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x125613126580: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x125613126600: fd fd fd fd fd fa fa fa fa fa fa fa f7 fa fd fd
  0x125613126680: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x125613126700: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
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

==77560==ADDITIONAL INFO

==77560==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffe6dbc4853 in openscreen_platform::TaskRunner::PostPackagedTask C:\b\s\w\ir\cache\builder\src\components\openscreen_platform\task_runner.cc:34
    #1 0x7ffe8425b5aa in cast_channel::KeepAliveHandler::Start C:\b\s\w\ir\cache\builder\src\components\media_router\common\providers\cast\channel\keep_alive_handler.cc:66
    #2 0x7ffe84222f35 in cast_channel::LibcastSocketService::OnMessage C:\b\s\w\ir\cache\builder\src\components\media_router\common\providers\cast\channel\libcast_socket_service.cc:303
    #3 0x7ffe71ba32d5 in mojo::SimpleWatcher::Context::Notify C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc:102


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==77560==END OF ADDITIONAL INFO
==77560==ABORTING

### ct...@chromium.org (2023-05-31)

Thanks for the report. Please update this bug when you have a proof-of-concept you can share. Even a non-mimized POC is useful for us to be able to reproduce and test the issue. Also, were you able to reproduce this on other Chrome versions (especially M113/M114 for Stable channel)?

In the meantime, setting some tentative labels and component based on the analysis you have provided. 

mfoltz@ could you comment on whether LibcastSocketService is reachable in any shipping configurations? It appears to be disabled in tree and I couldn't find any field-trial configs, but it is relatively old so I think I might be missing some shipping configuration (in Cast maybe?). I'm waiting to be able to reproduce directly, but given that this appears to be a Sev-Critical I want to get discussion started about the impact question.

[Monorail components: Internals>Cast>Providers]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-31)

Setting Pri-0 to match security severity Critical. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mf...@chromium.org (2023-05-31)

This is not shipping anywhere.

### ct...@chromium.org (2023-05-31)

Thanks for confirming! Marking this as Security_Impact-None then.

From a quick look at codesearch while I was triaging this, it appears the feature flag was added in 2021 or earlier [1]. Is https://crbug.com/chromium/1050913 the tracking bug for this feature?

[1]: https://source.chromium.org/chromium/chromium/src/+/main:components/media_router/common/providers/cast/channel/cast_socket_service.cc;l=26;drc=5cb606841c407df269b6027b9d18f13254c9fbc2

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### je...@gmail.com (2023-06-01)

[Comment Deleted]

### [Deleted User] (2023-06-01)

This issue is marked as a release blocker with no milestone associated. Please add an appropriate milestone.

All release blocking issues should have milestones associated to it, so that the issue can tracked and the fixes can be pushed promptly.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ct...@chromium.org (2023-06-01)

Fixing up some labels as this is Security_Impact-None.

### je...@gmail.com (2023-06-07)

[Comment Deleted]

### ad...@google.com (2023-06-07)

Re https://crbug.com/chromium/1449678#c14:

Per https://crbug.com/chromium/1449678#c8 this bug does not affect end users, so you should not expect immediate action here. If you have reason to believe that this code is reachable by end users in a default configuration of Chrome, please let us know.

That said, mfoltz@, as it's Critical severity, we'll be a little jumpy in the security team until this code is fully removed or the bug is fixed, so you should expect us to pester you occasionally. It would be great to see this resolved sometime in the next few weeks.

### mf...@chromium.org (2023-06-07)

We don't have a line of sight to ship this at our current staffing levels.  It's probably best to remove it until we have the resources to commit.

### gi...@appspot.gserviceaccount.com (2023-06-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e74a812e4980bc9b74f308f96b516cf839046ec8

commit e74a812e4980bc9b74f308f96b516cf839046ec8
Author: mark a. foltz <mfoltz@chromium.org>
Date: Wed Jun 07 22:52:33 2023

[Cast Channel] Remove libcast socket service.

This removes a partial implementation of the Chromium Cast socket client
using libcast.  It is not able to be shipped as-is and additional work
will be required to make it ready to ship, which we are not ready to do
yet.

Bug: 1050913,1449678
Change-Id: I04d522a41784817cae242bfbd2f50f6022bf3629
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4599573
Reviewed-by: Muyao Xu <muyaoxu@google.com>
Reviewed-by: Takumi Fujimoto <takumif@chromium.org>
Commit-Queue: Mark Foltz <mfoltz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1154629}

[modify] https://crrev.com/e74a812e4980bc9b74f308f96b516cf839046ec8/components/media_router/common/providers/cast/channel/cast_socket_service.cc
[modify] https://crrev.com/e74a812e4980bc9b74f308f96b516cf839046ec8/components/media_router/common/providers/cast/channel/BUILD.gn
[modify] https://crrev.com/e74a812e4980bc9b74f308f96b516cf839046ec8/components/media_router/common/providers/cast/channel/DEPS
[delete] https://crrev.com/374d9a9f24f4b93334c7fe5e11cab0f22b514c40/components/media_router/common/providers/cast/channel/libcast_socket_service_unittest.cc
[delete] https://crrev.com/374d9a9f24f4b93334c7fe5e11cab0f22b514c40/components/media_router/common/providers/cast/channel/libcast_socket_service.h
[delete] https://crrev.com/374d9a9f24f4b93334c7fe5e11cab0f22b514c40/components/media_router/common/providers/cast/channel/libcast_socket_service.cc


### mf...@chromium.org (2023-06-07)

[Empty comment from Monorail migration]

### aj...@google.com (2023-06-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-09)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-16)

Congratulations! The VRP Panel has decided to award yo $15,000 for this report + $1,000 bisect bonus. The reward amount was based on the lack of PoC or other reproducer to help trigger and demonstrate the security impact for this issue. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering this issue and reporting it to us! 

### am...@google.com (2023-06-17)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-07-24)

[Description Changed]

### [Deleted User] (2023-09-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-09-14)

This issue was migrated from crbug.com/chromium/1449678?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1451770]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064965)*
