# Heap-use-after-free in media_stream::

| Field | Value |
|-------|-------|
| **Issue ID** | [40060507](https://issues.chromium.org/issues/40060507) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>WebRTC, Internals |
| **Reporter** | in...@chromium.org |
| **Assignee** | [Deleted User] |
| **Created** | 2012-06-28 |
| **Bounty** | $3,133.00 |

## Description

Report from Ax330d

It is a browser crash with use-after-free.

Version 21.0.1181.0 (142942) Ubuntu 10.10 x64
22.0.1188.0 canary Windows 7 x64


<script>
    setTimeout(function() {
        navigator.webkitGetUserMedia({video:true}, function() {});
        location.reload();
    }, 10);
</script>


=================================================================
==7694== ERROR: AddressSanitizer heap-use-after-free on address 0x7faf1da61280 at pc 0x7faf632318dc bp 0x7fff34f2d570 sp 0x7fff34f2d568
READ of size 4 at 0x7faf1da61280 thread T0
    #0 0x7faf632318dc in media_stream::(anonymous namespace)::DoDeviceRequest(media_stream::MediaStreamDeviceSettingsRequest const*, base::Callback<void ()(std::vector<content::MediaStreamDevice, std::allocator<content::MediaStreamDevice> > const&)> const&) /media/Chromium/chromium/depot_tools/src/content/browser/renderer_host/media/media_stream_device_settings.cc:121
    #1 0x7faf63231d7b in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (*)(media_stream::MediaStreamDeviceSettingsRequest const*, base::Callback<void ()(std::vector<content::MediaStreamDevice, std::allocator<content::MediaStreamDevice> > const&)> const&)>, void ()(media_stream::MediaStreamDeviceSettingsRequest* const&, base::Callback<void ()(std::vector<content::MediaStreamDevice, std::allocator<content::MediaStreamDevice> > const&)> const&)>::MakeItSo(base::internal::RunnableAdapter<void (*)(media_stream::MediaStreamDeviceSettingsRequest const*, base::Callback<void ()(std::vector<content::MediaStreamDevice, std::allocator<content::MediaStreamDevice> > const&)> const&)>, media_stream::MediaStreamDeviceSettingsRequest* const&, base::Callback<void ()(std::vector<content::MediaStreamDevice, std::allocator<content::MediaStreamDevice> > const&)> const&) /media/Chromium/chromium/depot_tools/src/./base/bind_internal.h:897
    #2 0x7faf5f5cd1d3 in MessageLoop::RunTask(base::PendingTask const&) /media/Chromium/chromium/depot_tools/src/base/message_loop.cc:466
    #3 0x7faf5f5cd939 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /media/Chromium/chromium/depot_tools/src/base/message_loop.cc:477
    #4 0x7faf5f5cdc52 in MessageLoop::DoWork() /media/Chromium/chromium/depot_tools/src/base/message_loop.cc:654
    #5 0x7faf5f674a36 in base::MessagePumpGlib::RunWithDispatcher(base::MessagePump::Delegate*, base::MessagePumpDispatcher*) /media/Chromium/chromium/depot_tools/src/base/message_pump_glib.cc:203
    #6 0x7faf5f5cc9cc in MessageLoop::RunInternal() /media/Chromium/chromium/depot_tools/src/base/message_loop.cc:425
    #7 0x7faf5f5ce7dc in MessageLoopForUI::RunWithDispatcher(base::MessagePumpDispatcher*) /media/Chromium/chromium/depot_tools/src/base/message_loop.cc:771
    #8 0x7faf5effb322 in ChromeBrowserMainParts::MainMessageLoopRun(int*) /media/Chromium/chromium/depot_tools/src/chrome/browser/chrome_browser_main.cc:1924
    #9 0x7faf62def9a2 in content::BrowserMainLoop::RunMainMessageLoopParts() /media/Chromium/chromium/depot_tools/src/content/browser/browser_main_loop.cc:440
    #10 0x7faf62df27aa in (anonymous namespace)::BrowserMainRunnerImpl::Run() /media/Chromium/chromium/depot_tools/src/content/browser/browser_main_runner.cc:99
    #11 0x7faf62ded39f in BrowserMain(content::MainFunctionParams const&) /media/Chromium/chromium/depot_tools/src/content/browser/browser_main.cc:21
    #12 0x7faf5f4b518e in content::RunNamedProcessTypeMain(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate*) /media/Chromium/chromium/depot_tools/src/content/app/content_main_runner.cc:371
    #13 0x7faf5f4b5ef0 in content::ContentMainRunnerImpl::Run() /media/Chromium/chromium/depot_tools/src/content/app/content_main_runner.cc:626
    #14 0x7faf5f4b3e9f in content::ContentMain(int, char const**, content::ContentMainDelegate*) /media/Chromium/chromium/depot_tools/src/content/app/content_main.cc:35
    #15 0x7faf5e1aea47 in ChromeMain /media/Chromium/chromium/depot_tools/src/chrome/app/chrome_main.cc:32
    #16 0x7faf5e1ae9ab in main /media/Chromium/chromium/depot_tools/src/chrome/app/chrome_exe_main_gtk.cc:18
    #17 0x7faf56fdbd8e in __libc_start_main /build/buildd/eglibc-2.12.1/csu/libc-start.c:258
0x7faf1da61280 is located 0 bytes inside of 216-byte region [0x7faf1da61280,0x7faf1da61358)
freed by thread T11 here:
    #0 0x7faf6479cc02 in operator delete(void*) ??:0
    #1 0x7faf6322e2bc in media_stream::MediaStreamDeviceSettings::RemovePendingCaptureRequest(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) /media/Chromium/chromium/depot_tools/src/content/browser/renderer_host/media/media_stream_device_settings.cc:173
    #2 0x7faf63194fbd in media_stream::MediaStreamManager::CancelGenerateStream(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) /media/Chromium/chromium/depot_tools/src/content/browser/renderer_host/media/media_stream_manager.cc:247
    #3 0x7faf6318f867 in media_stream::MediaStreamDispatcherHost::OnCancelGenerateStream(int, int) /media/Chromium/chromium/depot_tools/src/content/browser/renderer_host/media/media_stream_dispatcher_host.cc:218
    #4 0x7faf6318f6a0 in bool MediaStreamHostMsg_CancelGenerateStream::Dispatch<media_stream::MediaStreamDispatcherHost, media_stream::MediaStreamDispatcherHost, void (media_stream::MediaStreamDispatcherHost::*)(int, int)>(IPC::Message const*, media_stream::MediaStreamDispatcherHost*, media_stream::MediaStreamDispatcherHost*, void (media_stream::MediaStreamDispatcherHost::*)(int, int)) /media/Chromium/chromium/depot_tools/src/./content/common/media/media_stream_messages.h:88
    #5 0x7faf6318f21c in media_stream::MediaStreamDispatcherHost::OnMessageReceived(IPC::Message const&, bool*) /media/Chromium/chromium/depot_tools/src/content/browser/renderer_host/media/media_stream_dispatcher_host.cc:162
    #6 0x7faf62ddc3ba in content::BrowserMessageFilter::DispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot_tools/src/content/public/browser/browser_message_filter.cc:136
    #7 0x7faf62ddbf89 in content::BrowserMessageFilter::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot_tools/src/content/public/browser/browser_message_filter.cc:52
    #8 0x7faf5f6cb9b2 in IPC::ChannelProxy::Context::TryFilters(IPC::Message const&) /media/Chromium/chromium/depot_tools/src/ipc/ipc_channel_proxy.cc:72
    #9 0x7faf5f6cbaa2 in IPC::ChannelProxy::Context::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot_tools/src/ipc/ipc_channel_proxy.cc:86
    #10 0x7faf5f6d3347 in IPC::internal::ChannelReader::DispatchInputData(char const*, int) /media/Chromium/chromium/depot_tools/src/ipc/ipc_channel_reader.cc:75
    #11 0x7faf5f6d3020 in IPC::internal::ChannelReader::ProcessIncomingMessages() /media/Chromium/chromium/depot_tools/src/ipc/ipc_channel_reader.cc:28
    #12 0x7faf5f6c57e8 in IPC::Channel::ChannelImpl::OnFileCanReadWithoutBlocking(int) /media/Chromium/chromium/depot_tools/src/ipc/ipc_channel_posix.cc:796
    #13 0x7faf5f566a8a in base::MessagePumpLibevent::FileDescriptorWatcher::OnFileCanReadWithoutBlocking(int, base::MessagePumpLibevent*) /media/Chromium/chromium/depot_tools/src/base/message_pump_libevent.cc:107
    #14 0x7faf5f567ee4 in base::MessagePumpLibevent::OnLibeventNotification(int, short, void*) /media/Chromium/chromium/depot_tools/src/base/message_pump_libevent.cc:365
    #15 0x7faf5f69bb0a in event_process_active /media/Chromium/chromium/depot_tools/src/third_party/libevent/event.c:385
    #16 0x7faf5f69ad0d in event_base_loop /media/Chromium/chromium/depot_tools/src/third_party/libevent/event.c:526
    #17 0x7faf5f56875b in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) /media/Chromium/chromium/depot_tools/src/base/message_pump_libevent.cc:277
    #18 0x7faf5f5cc9cc in MessageLoop::RunInternal() /media/Chromium/chromium/depot_tools/src/base/message_loop.cc:425
    #19 0x7faf5f5cb6c8 in MessageLoop::Run() /media/Chromium/chromium/depot_tools/src/base/message_loop.cc:308
    #20 0x7faf5f647381 in base::Thread::ThreadMain() /media/Chromium/chromium/depot_tools/src/base/threading/thread.cc:169
    #21 0x7faf5f63c1cc in base::(anonymous namespace)::ThreadFunc(void*) /media/Chromium/chromium/depot_tools/src/base/threading/platform_thread_posix.cc:65
    #22 0x7faf6479948c in __asan::AsanThread::ThreadStart() ??:0
previously allocated by thread T11 here:
    #0 0x7faf6479ca82 in operator new(unsigned long) ??:0
    #1 0x7faf6322de7f in media_stream::MediaStreamDeviceSettings::RequestCaptureDeviceUsage(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, int, int, media_stream::StreamOptions const&, GURL const&) /media/Chromium/chromium/depot_tools/src/content/browser/renderer_host/media/media_stream_device_settings.cc:159
    #2 0x7faf6319e4a1 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (media_stream::MediaStreamDeviceSettings::*)(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, int, int, media_stream::StreamOptions const&, GURL const&)>, void ()(media_stream::MediaStreamDeviceSettings*, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, int const&, int const&, media_stream::StreamOptions const&, GURL const&)>::MakeItSo(base::internal::RunnableAdapter<void (media_stream::MediaStreamDeviceSettings::*)(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, int, int, media_stream::StreamOptions const&, GURL const&)>, media_stream::MediaStreamDeviceSettings*, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, int const&, int const&, media_stream::StreamOptions const&, GURL const&) /media/Chromium/chromium/depot_tools/src/./base/bind_internal.h:1029
    #3 0x7faf6319e2dd in base::internal::Invoker<6, base::internal::BindState<base::internal::RunnableAdapter<void (media_stream::MediaStreamDeviceSettings::*)(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, int, int, media_stream::StreamOptions const&, GURL const&)>, void ()(media_stream::MediaStreamDeviceSettings*, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, int, int, media_stream::StreamOptions const&, GURL const&), void ()(base::internal::UnretainedWrapper<media_stream::MediaStreamDeviceSettings>, std::basic_string<char, std::char_traits<char>, std::allocator<char> >, int, int, media_stream::StreamOptions, GURL)>, void ()(media_stream::MediaStreamDeviceSettings*, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, int, int, media_stream::StreamOptions const&, GURL const&)>::Run(base::internal::BindStateBase*) /media/Chromium/chromium/depot_tools/src/./base/bind_internal.h:2127
    #4 0x7faf5f5cd1d3 in MessageLoop::RunTask(base::PendingTask const&) /media/Chromium/chromium/depot_tools/src/base/message_loop.cc:466
    #5 0x7faf5f5cd939 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /media/Chromium/chromium/depot_tools/src/base/message_loop.cc:477
    #6 0x7faf5f5cdc52 in MessageLoop::DoWork() /media/Chromium/chromium/depot_tools/src/base/message_loop.cc:654
    #7 0x7faf5f568422 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) /media/Chromium/chromium/depot_tools/src/base/message_pump_libevent.cc:239
    #8 0x7faf5f5cc9cc in MessageLoop::RunInternal() /media/Chromium/chromium/depot_tools/src/base/message_loop.cc:425
    #9 0x7faf5f5cb6c8 in MessageLoop::Run() /media/Chromium/chromium/depot_tools/src/base/message_loop.cc:308
    #10 0x7faf5f647381 in base::Thread::ThreadMain() /media/Chromium/chromium/depot_tools/src/base/threading/thread.cc:169
    #11 0x7faf5f63c1cc in base::(anonymous namespace)::ThreadFunc(void*) /media/Chromium/chromium/depot_tools/src/base/threading/platform_thread_posix.cc:65
    #12 0x7faf6479948c in __asan::AsanThread::ThreadStart() ??:0
Thread T11 created by T0 here:
    #0 0x7faf64791c15 in pthread_create ??:0
    #1 0x7faf5f63bd66 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, unsigned long*, base::ThreadPriority) /media/Chromium/chromium/depot_tools/src/base/threading/platform_thread_posix.cc:127
    #2 0x7faf5f63bc4d in base::PlatformThread::Create(unsigned long, base::PlatformThread::Delegate*, unsigned long*) /media/Chromium/chromium/depot_tools/src/base/threading/platform_thread_posix.cc:252
    #3 0x7faf5f646c45 in base::Thread::StartWithOptions(base::Thread::Options const&) /media/Chromium/chromium/depot_tools/src/base/threading/thread.cc:74
    #4 0x7faf62def220 in content::BrowserMainLoop::CreateThreads() /media/Chromium/chromium/depot_tools/src/content/browser/browser_main_loop.cc:362
    #5 0x7faf62df2547 in (anonymous namespace)::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams const&) /media/Chromium/chromium/depot_tools/src/content/browser/browser_main_runner.cc:86
    #6 0x7faf62ded352 in BrowserMain(content::MainFunctionParams const&) /media/Chromium/chromium/depot_tools/src/content/browser/browser_main.cc:17
    #7 0x7faf5f4b518e in content::RunNamedProcessTypeMain(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate*) /media/Chromium/chromium/depot_tools/src/content/app/content_main_runner.cc:371
    #8 0x7faf5f4b5ef0 in content::ContentMainRunnerImpl::Run() /media/Chromium/chromium/depot_tools/src/content/app/content_main_runner.cc:626
    #9 0x7faf5f4b3e9f in content::ContentMain(int, char const**, content::ContentMainDelegate*) /media/Chromium/chromium/depot_tools/src/content/app/content_main.cc:35
    #10 0x7faf5e1aea47 in ChromeMain /media/Chromium/chromium/depot_tools/src/chrome/app/chrome_main.cc:32
    #11 0x7faf5e1ae9ab in main /media/Chromium/chromium/depot_tools/src/chrome/app/chrome_exe_main_gtk.cc:18
    #12 0x7faf56fdbd8e in __libc_start_main /build/buildd/eglibc-2.12.1/csu/libc-start.c:258
==7694== ABORTING
Stats: 148M malloced (436M for red zones) by 1880943 calls
Stats: 4M realloced by 23049 calls
Stats: 138M freed by 1806049 calls
Stats: 78M really freed by 901196 calls
Stats: 548M (140311 full pages) mmaped in 136 calls
  mmaps   by size class: 8:1638300; 9:65528; 10:12285; 11:4094; 12:2048; 13:1024; 14:768; 15:256; 16:256; 17:96; 18:32; 19:8; 20:4; 21:2; 22:1; 23:1;
  mallocs by size class: 8:1791434; 9:67220; 10:14248; 11:3192; 12:2475; 13:800; 14:848; 15:300; 16:289; 17:92; 18:36; 19:4; 20:2; 21:1; 22:1; 23:1;
  frees   by size class: 8:1721816; 9:64665; 10:13316; 11:2259; 12:1920; 13:640; 14:777; 15:267; 16:265; 17:84; 18:32; 19:4; 20:1; 21:1; 22:1; 23:1;
  rfrees  by size class: 8:841959; 9:50312; 10:5238; 11:1383; 12:994; 13:336; 14:594; 15:131; 16:198; 17:24; 18:20; 19:3; 20:1; 21:1; 22:1; 23:1;
Stats: malloc large: 137 small slow: 4458
Shadow byte and word:
  0x1ff5e3b4c250: fd
  0x1ff5e3b4c250: fd fd fd fd fd fd fd fd
More shadow bytes:
  0x1ff5e3b4c230: fa fa fa fa fa fa fa fa
  0x1ff5e3b4c238: fa fa fa fa fa fa fa fa
  0x1ff5e3b4c240: fa fa fa fa fa fa fa fa
  0x1ff5e3b4c248: fa fa fa fa fa fa fa fa
=>0x1ff5e3b4c250: fd fd fd fd fd fd fd fd
  0x1ff5e3b4c258: fd fd fd fd fd fd fd fd
  0x1ff5e3b4c260: fd fd fd fd fd fd fd fd
  0x1ff5e3b4c268: fd fd fd fd fd fd fd fd
  0x1ff5e3b4c270: fa fa fa fa fa fa fa fa

## Timeline

### js...@chromium.org (2012-06-29)

The GetUserMedia API is part of WebRTC.

### js...@chromium.org (2012-06-29)

@niklase - This is a critical-severity bug, so pri-0. Can you get it assigned to the right person so it gets fixed ASAP?

### ni...@chromium.org (2012-06-29)

[Empty comment from Monorail migration]

### [Deleted User] (2012-06-29)

[Empty comment from Monorail migration]

### ni...@chromium.org (2012-06-29)

[Empty comment from Monorail migration]

### ni...@chromium.org (2012-06-29)

[Empty comment from Monorail migration]

### ni...@chromium.org (2012-06-29)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-06-29)

This doesn't appear to affect m20 stable, but I haven't checked against ASAN yet. And we haven't cut an m21 beta yet. So, can someone clarify if this code is enabled by default (not behind a switch) in m20 and m21?

### ni...@chromium.org (2012-06-29)

The switch is removed for M21.

### [Deleted User] (2012-06-29)

The crash happens when the UI thread is proceeding the request while we are removing the request in IO thread. A patch will be soon out.

### js...@chromium.org (2012-06-29)

Thanks for the clarification; I'm updating flags as needed. As long as we get this resolved before m21 stable ships we can avoid a critical regression.

### [Deleted User] (2012-06-29)

add Ami who helps reviewing the CL.

### js...@chromium.org (2012-06-29)

Clusterfuzz still hates my logon, so adding this link manually:
https://cluster-fuzz.appspot.com/testcase?key=69850383

@inferno or someone else, please link this bug ID with the report above.

### in...@chromium.org (2012-06-29)

I will update the bug once ClusterFuzz finishes with the regression range hunting.

### in...@chromium.org (2012-06-29)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=69850383

Uploader: jschuh@chromium.org

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x7f14839bd680
Crash State:
  - crash stack -
  media_stream::
  MessageLoop::RunTask
  - free stack -
  media_stream::MediaStreamDeviceSettings::RemovePendingCaptureRequest
  media_stream::MediaStreamManager::CancelGenerateStream
  

Minimized Testcase (0.15 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv959w9j8c_2KTSHhIA4XBSaeTRln5Gn1vC8Lj0MdkMOtvJxZLqMzfSq3_rejr_30pgXZOqSyggNAfMP-fMo-fc9Pkq8z5oxEmG-vf7pImxnksHbxrs5l7g-kV480zeT6EY5S40fHTtgUdYzjv0UpFGh61-nRXSCwnK6CtXyP7i5PYxcTkmk
<script>
    setTimeout(function() {
        navigator.webkitGetUserMedia({video:true}, function() {});
        location.reload();
    }, 10);
</script>

### bu...@chromium.org (2012-07-03)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=145282

------------------------------------------------------------------------
r145282 | xians@chromium.org | Tue Jul 03 04:14:55 PDT 2012

Changed paths:
 A http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/renderer_host/media/media_stream_device_settings_unittest.cc?r1=145282&r2=145281&pathrev=145282
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/content_tests.gypi?r1=145282&r2=145281&pathrev=145282
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/media/media_stream_devices_controller.h?r1=145282&r2=145281&pathrev=145282
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/renderer_host/media/media_stream_device_settings.cc?r1=145282&r2=145281&pathrev=145282
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/media/media_stream_devices_controller.cc?r1=145282&r2=145281&pathrev=145282

When we post a DoDeviceRequest on the UI thread, we use a pointer for the variable |request| for the PostTask(), this can crash the browser if RemovePendingCaptureRequest is called on the IO thread which delete the memory.

We can simply use a const reference instead of a pointer to fix the crash.

TBR=xians@chromium.org

BUG=135043
TEST=content_unittests --gtest_filter="*MediaStreamDevice*"

Review URL: https://chromiumcodereview.appspot.com/10701037
------------------------------------------------------------------------

### in...@chromium.org (2012-07-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2012-07-03)

ClusterFuzz has detected this issue as fixed in range 145281:145282.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=69850383

Uploader: jschuh@chromium.org

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x7f14839bd680
Crash State:
  - crash stack -
  media_stream::
  MessageLoop::RunTask
  - free stack -
  media_stream::MediaStreamDeviceSettings::RemovePendingCaptureRequest
  media_stream::MediaStreamManager::CancelGenerateStream
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=140520:140773
Fixed: https://cluster-fuzz.appspot.com/revisions?range=145281:145282

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv959w9j8c_2KTSHhIA4XBSaeTRln5Gn1vC8Lj0MdkMOtvJxZLqMzfSq3_rejr_30pgXZOqSyggNAfMP-fMo-fc9Pkq8z5oxEmG-vf7pImxnksHbxrs5l7g-kV480zeT6EY5S40fHTtgUdYzjv0UpFGh61-nRXSCwnK6CtXyP7i5PYxcTkmk

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### ph...@chromium.org (2012-07-04)

Hi!

I''ll shortly update our GetUserMedia fuzzer so that it has a chance to insert location.reload statements before and after the GetUserMedia call. That should be able to keep this bug from regressing in the future. You can see the patch here. https://webrtc-codereview.appspot.com/679008/

/ P

### [Deleted User] (2012-07-04)

Anyone knows if I need to merge the fix into M21?

### sc...@gmail.com (2012-07-09)

Yes, definitely a blocker for M21, merge required. We (security team) can do it if you prefer.

### [Deleted User] (2012-07-09)

please do it, thanks a lot.

short msg from my vocation.

sx

### sc...@gmail.com (2012-07-09)

Hmm. Nasty-looking path conflict trying the merge. Anyone on the media team we can get to tackle this?

### [Deleted User] (2012-07-09)

+tommi

Tommi, could you please help or assign someone to take care of this issue?

### [Deleted User] (2012-07-10)

+Tommi

### sc...@gmail.com (2012-07-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-07-10)

Dale is one of my favourite media superstars. Dale, any chance you'd be interested in merging this for the next beta?

### da...@chromium.org (2012-07-10)

I don't think this can be merged as is, a new version will have to be written for M21 or https://chromiumcodereview.appspot.com/10537099 will have to be merged as well since media_stream_devices_controller.* doesn't exist in M21.

xians: Thoughts?

### to...@chromium.org (2012-07-11)

xians is on vacation right now.  I think that merging 10537099 will be rather risky since there have been a number of changes committed on top of it since that would also be required - the last one that I know of was committed just yesterday.  Do you know how much work it would be to fix on the branch?

### js...@chromium.org (2012-07-11)

Just to convey the urgency of getting a fix, a critical security regression is one of the only things we'd block a feature over. (Because criticals are so dangerous, and pretty rare in Chrome.)

### [Deleted User] (2012-07-11)

To Tommi,

From the code perspective, it should be quite easy to make a new fix to the
branch.

sx

### ka...@google.com (2012-07-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-07-11)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=146225

------------------------------------------------------------------------
r146225 | wjia@chromium.org | Wed Jul 11 15:21:40 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/1180/src/content/browser/renderer_host/media/media_stream_device_settings.cc?r1=146225&r2=146224&pathrev=146225
 M http://src.chromium.org/viewvc/chrome/branches/1180/src/chrome/browser/ui/media_stream_infobar_delegate.cc?r1=146225&r2=146224&pathrev=146225
 M http://src.chromium.org/viewvc/chrome/branches/1180/src/chrome/browser/ui/media_stream_infobar_delegate.h?r1=146225&r2=146224&pathrev=146225

Use reference instead of pointer for media stream device request
This is a simplified merge of r145282 into branch 1180.
Since the pointer will be out of scope when posting a task, need to use reference.
Also MediaStreamInfoBarDelegate needs to keep a copy of request, instead of a pointer.

BUG=135043
Review URL: https://chromiumcodereview.appspot.com/10692174
------------------------------------------------------------------------

### wj...@chromium.org (2012-07-11)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-07-12)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-07-17)

[Empty comment from Monorail migration]

### ph...@chromium.org (2012-07-30)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-08-20)

@Ax330d: sorry for the delay on this one.
Thanks for detecting this Critical regression and prevent it from hitting any stable release. $3133.7, obviously.

### sc...@gmail.com (2012-09-12)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-14)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### la...@google.com (2013-01-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-05-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/135043?no_tracker_redirect=1

[Multiple monorail components: Blink>WebRTC, Internals]
[Monorail mergedwith: crbug.com/chromium/131785]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060507)*
