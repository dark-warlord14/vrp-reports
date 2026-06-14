# Security: Use-after-free in net::SocketStream::Finish

| Field | Value |
|-------|-------|
| **Issue ID** | [40077581](https://issues.chromium.org/issues/40077581) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink, Blink>Network>WebSockets, Blink>Workers |
| **Reporter** | me...@chromium.org |
| **Assignee** | ri...@chromium.org |
| **Created** | 2013-05-22 |
| **Bounty** | $3,133.00 |

## Description

Originally reported in https://crbug.com/chromium/225546 by therealholden. I'm spinning this off as it's a separate issue.
It's still Workers related though.

The attached repro hits a UAF in SocketStream::Finish.

ASAN trace:

=================================================================
==1361==ERROR: AddressSanitizer: heap-use-after-free on address 0x6130005a3558 at pc 0x7ffd88cf92f5 bp 0x7ffd669bffb0 sp 0x7ffd669bffa8
READ of size 8 at 0x6130005a3558 thread T15 (Chrome_IOThread)
    #0 0x7ffd88cf92f4 in net::SocketStream::Finish(int) src/blink/src/out/Release/../../net/socket_stream/socket_stream.cc:364
    #1 0x7ffd88cf56d2 in net::SocketStream::DoLoop(int) src/blink/src/out/Release/../../net/socket_stream/socket_stream.cc:555
    #2 0x7ffd88aa0ef3 in base::Callback<void (int)>::Run(int const&) const src/blink/src/out/Release/../../base/callback.h:436
    #3 0x7ffd88aa01d5 in net::TCPClientSocketLibevent::DidCompleteConnect() src/blink/src/out/Release/../../net/socket/tcp_client_socket_libevent.cc:671
    #4 0x7ffd87feb766 in base::MessagePumpLibevent::FileDescriptorWatcher::OnFileCanWriteWithoutBlocking(int, base::MessagePumpLibevent*) src/blink/src/out/Release/../../base/message_pump_libevent.cc:110
    #5 0x7ffd87fecb02 in base::MessagePumpLibevent::OnLibeventNotification(int, short, void*) src/blink/src/out/Release/../../base/message_pump_libevent.cc:354
    #6 0x7ffd8efaa144 in event_process_active src/blink/src/out/Release/../../third_party/libevent/event.c:385
    #7 0x7ffd87fed303 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) src/blink/src/out/Release/../../base/message_pump_libevent.cc:239
    #8 0x7ffd88063860 in base::MessageLoop::RunInternal() src/blink/src/out/Release/../../base/message_loop.cc:441
    #9 0x7ffd880a6fb3 in base::RunLoop::Run() src/blink/src/out/Release/../../base/run_loop.cc:45
    #10 0x7ffd88061fcd in base::MessageLoop::Run() src/blink/src/out/Release/../../base/message_loop.cc:321
    #11 0x7ffd88eda43e in content::BrowserThreadImpl::IOThreadRun(base::MessageLoop*) src/blink/src/out/Release/../../content/browser/browser_thread_impl.cc:164
    #12 0x7ffd88eda6b5 in content::BrowserThreadImpl::Run(base::MessageLoop*) src/blink/src/out/Release/../../content/browser/browser_thread_impl.cc:192
    #13 0x7ffd880ea5cb in base::Thread::ThreadMain() src/blink/src/out/Release/../../base/threading/thread.cc:197
    #14 0x7ffd880dbfdc in base::(anonymous namespace)::ThreadFunc(void*) src/blink/src/out/Release/../../base/threading/platform_thread_posix.cc:95
    #15 0x7ffd85ff8291 in __asan::AsanThread::ThreadStart(unsigned long) ??:0
    #16 0x7ffd7f585e99 in start_thread /build/buildd/eglibc-2.15/nptl/pthread_create.c:308
    #17 0x7ffd7c64accc in ?? /build/buildd/eglibc-2.15/misc/../sysdeps/unix/sysv/linux/x86_64/clone.S:112
0x6130005a3558 is located 24 bytes inside of 336-byte region [0x6130005a3540,0x6130005a3690)
freed by thread T15 (Chrome_IOThread) here:
    #0 0x7ffd85ff2752 in operator delete(void*) ??:0
    #1 0x7ffd89180fa9 in base::RefCountedThreadSafe<net::SocketStreamJob, base::DefaultRefCountedThreadSafeTraits<net::SocketStreamJob> >::DeleteInternal(net::SocketStreamJob const*) src/blink/src/out/Release/../../base/memory/ref_counted.h:151
    #2 0x7ffd8917b7d5 in content::SocketStreamDispatcherHost::DeleteSocketStreamHost(int) src/blink/src/out/Release/../../content/browser/renderer_host/socket_stream_dispatcher_host.cc:237
    #3 0x7ffd8917c3eb in content::SocketStreamDispatcherHost::OnError(net::SocketStream const*, int) src/blink/src/out/Release/../../content/browser/renderer_host/socket_stream_dispatcher_host.cc:117
    #4 0x7ffd88cf910d in net::SocketStream::Finish(int) src/blink/src/out/Release/../../net/socket_stream/socket_stream.cc:362
    #5 0x7ffd88cf56d2 in net::SocketStream::DoLoop(int) src/blink/src/out/Release/../../net/socket_stream/socket_stream.cc:555
    #6 0x7ffd88aa0ef3 in base::Callback<void (int)>::Run(int const&) const src/blink/src/out/Release/../../base/callback.h:436
    #7 0x7ffd88aa01d5 in net::TCPClientSocketLibevent::DidCompleteConnect() src/blink/src/out/Release/../../net/socket/tcp_client_socket_libevent.cc:671
    #8 0x7ffd87feb766 in base::MessagePumpLibevent::FileDescriptorWatcher::OnFileCanWriteWithoutBlocking(int, base::MessagePumpLibevent*) src/blink/src/out/Release/../../base/message_pump_libevent.cc:110
    #9 0x7ffd87fecb02 in base::MessagePumpLibevent::OnLibeventNotification(int, short, void*) src/blink/src/out/Release/../../base/message_pump_libevent.cc:354
    #10 0x7ffd8efaa144 in event_process_active src/blink/src/out/Release/../../third_party/libevent/event.c:385
    #11 0x7ffd87fed303 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) src/blink/src/out/Release/../../base/message_pump_libevent.cc:239
    #12 0x7ffd88063860 in base::MessageLoop::RunInternal() src/blink/src/out/Release/../../base/message_loop.cc:441
    #13 0x7ffd880a6fb3 in base::RunLoop::Run() src/blink/src/out/Release/../../base/run_loop.cc:45
    #14 0x7ffd88061fcd in base::MessageLoop::Run() src/blink/src/out/Release/../../base/message_loop.cc:321
    #15 0x7ffd88eda43e in content::BrowserThreadImpl::IOThreadRun(base::MessageLoop*) src/blink/src/out/Release/../../content/browser/browser_thread_impl.cc:164
    #16 0x7ffd88eda6b5 in content::BrowserThreadImpl::Run(base::MessageLoop*) src/blink/src/out/Release/../../content/browser/browser_thread_impl.cc:192
    #17 0x7ffd880ea5cb in base::Thread::ThreadMain() src/blink/src/out/Release/../../base/threading/thread.cc:197
    #18 0x7ffd880dbfdc in base::(anonymous namespace)::ThreadFunc(void*) src/blink/src/out/Release/../../base/threading/platform_thread_posix.cc:95
    #19 0x7ffd85ff8291 in __asan::AsanThread::ThreadStart(unsigned long) ??:0
previously allocated by thread T15 (Chrome_IOThread) here:
    #0 0x7ffd85ff2592 in operator new(unsigned long) ??:0
    #1 0x7ffd88b80efa in (anonymous namespace)::WebSocketJobFactory(GURL const&, net::SocketStream::Delegate*) src/blink/src/out/Release/../../net/websockets/websocket_job.cc:40
    #2 0x7ffd88d083e0 in net::SocketStreamJobManager::CreateJob(GURL const&, net::SocketStream::Delegate*) const src/blink/src/out/Release/../../net/socket_stream/socket_stream_job_manager.cc:37
    #3 0x7ffd88d07880 in net::SocketStreamJob::CreateSocketStreamJob(GURL const&, net::SocketStream::Delegate*, net::TransportSecurityState*, net::SSLConfigService*) src/blink/src/out/Release/../../net/socket_stream/socket_stream_job.cc:39
    #4 0x7ffd89181161 in content::SocketStreamHost::Connect(GURL const&, net::URLRequestContext*) src/blink/src/out/Release/../../content/browser/renderer_host/socket_stream_host.cc:62
    #5 0x7ffd8917afdd in content::SocketStreamDispatcherHost::OnConnect(int, GURL const&, int) src/blink/src/out/Release/../../content/browser/renderer_host/socket_stream_dispatcher_host.cc:208
    #6 0x7ffd8917aaee in void DispatchToMethod<content::SocketStreamDispatcherHost, void (content::SocketStreamDispatcherHost::*)(int, GURL const&, int), int, GURL, int>(content::SocketStreamDispatcherHost*, void (content::SocketStreamDispatcherHost::*)(int, GURL const&, int), Tuple3<int, GURL, int> const&) src/blink/src/out/Release/../../base/tuple.h:559
    #7 0x7ffd88ebb473 in content::BrowserMessageFilter::DispatchMessage(IPC::Message const&) src/blink/src/out/Release/../../content/public/browser/browser_message_filter.cc:136
    #8 0x7ffd88ebb260 in content::BrowserMessageFilter::OnMessageReceived(IPC::Message const&) src/blink/src/out/Release/../../content/public/browser/browser_message_filter.cc:52
    #9 0x7ffd8b10a8aa in content::ChildProcessHostImpl::OnMessageReceived(IPC::Message const&) src/blink/src/out/Release/../../content/common/child_process_host_impl.cc:237
    #10 0x7ffd8b10ac6c in non-virtual thunk to content::ChildProcessHostImpl::OnMessageReceived(IPC::Message const&) src/blink/src/out/Release/../../content/common/child_process_host_impl.cc:262
    #11 0x7ffd872a362b in IPC::internal::ChannelReader::DispatchInputData(char const*, int) src/blink/src/out/Release/../../ipc/ipc_channel_reader.cc:90
    #12 0x7ffd872a2ecc in IPC::internal::ChannelReader::ProcessIncomingMessages() src/blink/src/out/Release/../../ipc/ipc_channel_reader.cc:32
    #13 0x7ffd8729777b in IPC::Channel::ChannelImpl::OnFileCanReadWithoutBlocking(int) src/blink/src/out/Release/../../ipc/ipc_channel_posix.cc:641
    #14 0x7ffd87fecbb0 in base::MessagePumpLibevent::FileDescriptorWatcher::OnFileCanReadWithoutBlocking(int, base::MessagePumpLibevent*) src/blink/src/out/Release/../../base/message_pump_libevent.cc:102
    #15 0x7ffd8efaa144 in event_process_active src/blink/src/out/Release/../../third_party/libevent/event.c:385
    #16 0x7ffd87fed303 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) src/blink/src/out/Release/../../base/message_pump_libevent.cc:239
    #17 0x7ffd88063860 in base::MessageLoop::RunInternal() src/blink/src/out/Release/../../base/message_loop.cc:441
    #18 0x7ffd880a6fb3 in base::RunLoop::Run() src/blink/src/out/Release/../../base/run_loop.cc:45
    #19 0x7ffd88061fcd in base::MessageLoop::Run() src/blink/src/out/Release/../../base/message_loop.cc:321
    #20 0x7ffd88eda43e in content::BrowserThreadImpl::IOThreadRun(base::MessageLoop*) src/blink/src/out/Release/../../content/browser/browser_thread_impl.cc:164
    #21 0x7ffd88eda6b5 in content::BrowserThreadImpl::Run(base::MessageLoop*) src/blink/src/out/Release/../../content/browser/browser_thread_impl.cc:192
    #22 0x7ffd880ea5cb in base::Thread::ThreadMain() src/blink/src/out/Release/../../base/threading/thread.cc:197
    #23 0x7ffd880dbfdc in base::(anonymous namespace)::ThreadFunc(void*) src/blink/src/out/Release/../../base/threading/platform_thread_posix.cc:95
    #24 0x7ffd85ff8291 in __asan::AsanThread::ThreadStart(unsigned long) ??:0
Thread T15 (Chrome_IOThread) created by T0 (chrome) here:
    #0 0x7ffd85fee158 in pthread_create ??:0
    #1 0x7ffd880dbd31 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, unsigned long*, base::ThreadPriority) src/blink/src/out/Release/../../base/threading/platform_thread_posix.cc:159
    #2 0x7ffd880dbbdc in base::PlatformThread::Create(unsigned long, base::PlatformThread::Delegate*, unsigned long*) src/blink/src/out/Release/../../base/threading/platform_thread_posix.cc:260
    #3 0x7ffd880e9dda in base::Thread::StartWithOptions(base::Thread::Options const&) src/blink/src/out/Release/../../base/threading/thread.cc:93
    #4 0x7ffd88ed4061 in content::BrowserMainLoop::CreateThreads() src/blink/src/out/Release/../../content/browser/browser_main_loop.cc:524
    #5 0x7ffd8926edd7 in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams const&) src/blink/src/out/Release/../../content/browser/browser_main_runner.cc:112
    #6 0x7ffd8f5c7732 in content::BrowserMain(content::MainFunctionParams const&) src/blink/src/out/Release/../../content/browser/browser_main.cc:18
    #7 0x7ffd8bd3599d in content::RunNamedProcessTypeMain(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate*) src/blink/src/out/Release/../../content/app/content_main_runner.cc:449
    #8 0x7ffd8bd373f8 in content::ContentMainRunnerImpl::Run() src/blink/src/out/Release/../../content/app/content_main_runner.cc:772
    #9 0x7ffd8bd33b01 in content::ContentMain(int, char const**, content::ContentMainDelegate*) src/blink/src/out/Release/../../content/app/content_main.cc:35
    #10 0x7ffd85fffed6 in ChromeMain src/blink/src/out/Release/../../chrome/app/chrome_main.cc:32
    #11 0x7ffd85fffe1a in main src/blink/src/out/Release/../../chrome/app/chrome_exe_main_gtk.cc:39
    #12 0x7ffd7c57876c in __libc_start_main /build/buildd/eglibc-2.15/csu/libc-start.c:226
Shadow bytes around the buggy address:
  0x0c26800ac650: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c26800ac660: 00 00 fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c26800ac670: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c26800ac680: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c26800ac690: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa
=>0x0c26800ac6a0: fa fa fa fa fa fa fa fa fd fd fd[fd]fd fd fd fd
  0x0c26800ac6b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c26800ac6c0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c26800ac6d0: fd fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c26800ac6e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c26800ac6f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:     fa
  Heap righ redzone:     fb
  Freed Heap region:     fd
  Stack left redzone:    f1
  Stack mid redzone:     f2
  Stack right redzone:   f3
  Stack partial redzone: f4
  Stack after return:    f5
  Stack use after scope: f8
  Global redzone:        f9
  Global init order:     f6
  Poisoned by user:      f7
  ASan internal:         fe
==1361==ABORTING



## Attachments

- [websocket.html](attachments/websocket.html) (text/x-c++; charset=us-ascii, 297 B)
- [242762_WebSocket_browser_crash_repro.html](attachments/242762_WebSocket_browser_crash_repro.html) (text/plain; charset=us-ascii, 568 B)
- [242762_webSocket_browser_crash.txt](attachments/242762_webSocket_browser_crash.txt) (text/x-c++; charset=us-ascii, 50.6 KB)
- [issue_242762_crash_trace_ToT_202479.txt](attachments/issue_242762_crash_trace_ToT_202479.txt) (text/x-c++; charset=us-ascii, 15.0 KB)

## Timeline

### in...@chromium.org (2013-05-22)

Julien, can you be the security owner on this ? You might lure Mustafa into fixing this :) ?

### jl...@chromium.org (2013-05-22)

Alright! Mustafa: let me know if you feel like looking into it!

### ri...@chromium.org (2013-05-23)

I am looking at it. It appears the "Connect" callback is called twice. base::Unretained(this) makes this into a use-after-free. Whether the callback was registered twice or some other bogosity happened is not yet clear to me.

### ri...@chromium.org (2013-05-23)

I was wrong. The "Connect" callback is only called once.

The UAF only happens if IPC to the renderer fails immediately after a WebSocket connection error (some other kinds of errors on a WebSocket connection might also be able to trigger it). The problem code is in net::SocketStream::Finish() and looks like this:

    if (result != ERR_CONNECTION_CLOSED)
      delegate->OnError(this, result);
    if (result != ERR_PROTOCOL_SWITCHED)
      delegate->OnClose(this);

If the IPC to the renderer fails, then the delegate->OnError() call will have the side-effect of deleting the net::WebSocketJob object "delegate". Then the UAF happens in the vtable lookup for OnClose().

It is hard and boring to reproduce (usually the renderer just crashes) and I don't know how to write a test to reproduce it it so I am leaving the status as "Available".

With verbose logging turned on, this is what is logged:

[30545:30571:0523/211900:VERBOSE1:socket_stream.cc(369)] Finish result=net::ERR_
CONNECTION_REFUSED
[30545:30571:0523/211900:VERBOSE1:socket_stream_dispatcher_host.cc(107)] SocketS
treamDispatcherHost::OnError socket_id=3340
[30545:30571:0523/211900:ERROR:socket_stream_dispatcher_host.cc(116)] SocketStreamMsg_Failed failed.
[30545:30571:0523/211900:VERBOSE1:socket_stream_host.cc(53)] SocketStreamHost destructed socket_id=3340
[30545:30571:0523/211901:ERROR:socket_stream_dispatcher_host.cc(243)] SocketStreamMsg_Closed failed.

It appears that the "SocketStreamMsg_Failed failed." message is highly correlated with the UAF.

A potential fix would be to postpone the call to DeleteSocketStreamHost() in net::SocketStreamDispatcherHost::OnError() until after the event loop has run.

### th...@gmail.com (2013-05-23)

It should be a lot easier to repro with the script added to this comment.

The repro steps are with the this script:

1. Start Chrome and open an incognito window
2. Launch the script in the incognito window (has a close timer)
3. Move focus back to the non-incognito window
4. Browser crash



### ri...@chromium.org (2013-05-24)

I think I have worked out a way to write a test for this.

### in...@chromium.org (2013-05-24)

[Empty comment from Monorail migration]

### ri...@chromium.org (2013-05-24)

Proposed fix is at https://codereview.chromium.org/15989003/

By the way, I reviewed SocketStream for similar bugs but this appears to be the only one.

### ri...@chromium.org (2013-05-28)

Fix landed on trunk as https://src.chromium.org/viewvc/chrome?view=rev&revision=202414

Letting it bake...

### sc...@gmail.com (2013-05-28)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-05-28)

@meacer: isn't this a Critical, not a High? It sounds like a browser UAF, right? These are usually critical.

### ri...@chromium.org (2013-05-28)

I am not yet a committer; would you like someone else on the WebSocket team to perform a branch merge?

### sc...@gmail.com (2013-05-28)

That's ok; merging is a service that Chrome Security Team usually provides :D

### th...@gmail.com (2013-05-28)

I can still repro the original NetworkDelegate::NotifyBeforeSocketStreamConnect browser crash on ToT 202479. I thought the browser crash was caused by the UAF?

The trace hasn't changed afaict.

### ri...@chromium.org (2013-05-28)

Apparently not. Which makes sense; the UAF in net::SocketStream::Finish happens very quickly and would not normally be detectable unless you're using a malloc instrumented to catch UAF.

Has anyone reproduced the NetworkDelegate::NotifyBeforeSocketStreamConnect crash on Linux?

### th...@gmail.com (2013-05-28)

I had to use the core dump to get this one. I have seen a lot of other crashes though. Some of them look familiar.

I used ToT Version 29.0.1522.0 (202528) on Ubuntu 13.04 for the trace.

[9919:9938:0528/163819:ERROR:socket_stream_dispatcher_host.cc(116)] SocketStreamMsg_Failed failed.
[9919:9938:0528/163819:ERROR:socket_stream_dispatcher_host.cc(243)] SocketStreamMsg_Closed failed.
Segmentation fault (core dumped)

Program terminated with signal 11, Segmentation fault.
#0  0xb3cdb68b in net::NetworkDelegate::NotifyBeforeSocketStreamConnect(net::SocketStream*, base::Callback<void (int)> const&) ()
(gdb) bt
#0  0xb3cdb68b in net::NetworkDelegate::NotifyBeforeSocketStreamConnect(net::SocketStream*, base::Callback<void (int)> const&) ()
#1  0x0001c667 in ?? ()
#2  0xba2be3d1 in ?? ()
#3  0xb8e8a6a4 in ?? ()
#4  0xb676df80 in tc_delete ()
#5  0xba1d8774 in ?? ()
#6  0xb677769c in ?? ()
Cannot access memory at address 0xb3ed9149

Also, the original script indeed reproduced an UAF. While trying to improve it, I may have hit an(other) (browser) issue and just assumed the crash was caused by the UAF since both issues happen in the browser process.


### ri...@chromium.org (2013-05-29)

Okay, I reproduced on a release build with asan. I'm not sure why the behaviour is so different from a debug build. Here's the stack trace:

=================================================================
==24202==ERROR: AddressSanitizer: heap-use-after-free on address 0x60f00003d528 at pc 0x7f049da76728 bp 0x7f04750aa1b0 sp 0x7f04750aa1a8
READ of size 8 at 0x60f00003d528 thread T17 (Chrome_IOThread)
    #0 0x7f049da76727 in DoBeforeConnect /usr/local/google/home/ricea/src/out/Release/../../net/url_request/url_request_context.h:135
    #1 0x7f049e0df547 in Run /usr/local/google/home/ricea/src/out/Release/../../base/callback.h:396
    #2 0x7f049e0dfd44 in DeferOrRunPendingTask /usr/local/google/home/ricea/src/out/Release/../../base/message_loop.cc:496
    #3 0x7f049e0e0de0 in DoWork /usr/local/google/home/ricea/src/out/Release/../../base/message_loop.cc:688
    #4 0x7f049e035181 in Run /usr/local/google/home/ricea/src/out/Release/../../base/message_pump_libevent.cc:235
    #5 0x7f049e0de339 in RunInternal /usr/local/google/home/ricea/src/out/Release/../../base/message_loop.cc:441
    #6 0x7f049e1374b3 in Run /usr/local/google/home/ricea/src/out/Release/../../base/run_loop.cc:45
    #7 0x7f049e0dcacd in Run /usr/local/google/home/ricea/src/out/Release/../../base/message_loop.cc:321
    #8 0x7f0493d1f9ae in IOThreadRun /usr/local/google/home/ricea/src/out/Release/../../content/browser/browser_thread_impl.cc:164
    #9 0x7f0493d1fc25 in Run /usr/local/google/home/ricea/src/out/Release/../../content/browser/browser_thread_impl.cc:192
    #10 0x7f049e191eeb in ThreadMain /usr/local/google/home/ricea/src/out/Release/../../base/threading/thread.cc:203
    #11 0x7f049e17e528 in ThreadFunc /usr/local/google/home/ricea/src/out/Release/../../base/threading/platform_thread_posix.cc:80
    #12 0x7f04a1e04c31 in __asan::AsanThread::ThreadStart(unsigned long) ??:0
    #13 0x7f048de6be99 in start_thread /build/buildd/eglibc-2.15/nptl/pthread_create.c:308
    #14 0x7f048bf9accc in ?? /build/buildd/eglibc-2.15/misc/../sysdeps/unix/sysv/linux/x86_64/clone.S:112
0x60f00003d528 is located 72 bytes inside of 168-byte region [0x60f00003d4e0,0x60f00003d588)
freed by thread T17 (Chrome_IOThread) here:
    #0 0x7f04a1dff0f2 in operator delete(void*) ??:0
    #1 0x7f04a20d09e5 in operator() /usr/local/google/home/ricea/src/out/Release/../../base/memory/scoped_ptr.h:137
    #2 0x7f04a2aac6ad in ~OffTheRecordProfileIOData /usr/local/google/home/ricea/src/out/Release/../../chrome/browser/profiles/off_the_record_profile_io_data.cc:159
    #3 0x7f049e0df547 in Run /usr/local/google/home/ricea/src/out/Release/../../base/callback.h:396
    #4 0x7f049e0dfd44 in DeferOrRunPendingTask /usr/local/google/home/ricea/src/out/Release/../../base/message_loop.cc:496
    #5 0x7f049e0e0de0 in DoWork /usr/local/google/home/ricea/src/out/Release/../../base/message_loop.cc:688
    #6 0x7f049e035181 in Run /usr/local/google/home/ricea/src/out/Release/../../base/message_pump_libevent.cc:235
    #7 0x7f049e0de339 in RunInternal /usr/local/google/home/ricea/src/out/Release/../../base/message_loop.cc:441
    #8 0x7f049e1374b3 in Run /usr/local/google/home/ricea/src/out/Release/../../base/run_loop.cc:45
    #9 0x7f049e0dcacd in Run /usr/local/google/home/ricea/src/out/Release/../../base/message_loop.cc:321
    #10 0x7f0493d1f9ae in IOThreadRun /usr/local/google/home/ricea/src/out/Release/../../content/browser/browser_thread_impl.cc:164
    #11 0x7f0493d1fc25 in Run /usr/local/google/home/ricea/src/out/Release/../../content/browser/browser_thread_impl.cc:192
    #12 0x7f049e191eeb in ThreadMain /usr/local/google/home/ricea/src/out/Release/../../base/threading/thread.cc:203
    #13 0x7f049e17e528 in ThreadFunc /usr/local/google/home/ricea/src/out/Release/../../base/threading/platform_thread_posix.cc:80
    #14 0x7f04a1e04c31 in __asan::AsanThread::ThreadStart(unsigned long) ??:0
previously allocated by thread T17 (Chrome_IOThread) here:
    #0 0x7f04a1dfef32 in operator new(unsigned long) ??:0
    #1 0x7f04a20d452c in Init /usr/local/google/home/ricea/src/out/Release/../../chrome/browser/profiles/profile_io_data.cc:651
    #2 0x7f04a2488d3d in Create /usr/local/google/home/ricea/src/out/Release/../../chrome/browser/net/chrome_url_request_context.cc:51
    #3 0x7f04a2486514 in GetURLRequestContext /usr/local/google/home/ricea/src/out/Release/../../chrome/browser/net/chrome_url_request_context.cc:179
    #4 0x7f0493ce154f in InitializeOnIOThread /usr/local/google/home/ricea/src/out/Release/../../content/browser/appcache/chrome_appcache_service.cc:40
    #5 0x7f04941ea606 in scoped_refptr /usr/local/google/home/ricea/src/out/Release/../../base/bind_internal.h:379
    #6 0x7f04941ea47e in Run /usr/local/google/home/ricea/src/out/Release/../../base/bind_internal.h:1815
    #7 0x7f049e0df547 in Run /usr/local/google/home/ricea/src/out/Release/../../base/callback.h:396
    #8 0x7f049e0dfd44 in DeferOrRunPendingTask /usr/local/google/home/ricea/src/out/Release/../../base/message_loop.cc:496
    #9 0x7f049e0e0de0 in DoWork /usr/local/google/home/ricea/src/out/Release/../../base/message_loop.cc:688
    #10 0x7f049e035181 in Run /usr/local/google/home/ricea/src/out/Release/../../base/message_pump_libevent.cc:235
    #11 0x7f049e0de339 in RunInternal /usr/local/google/home/ricea/src/out/Release/../../base/message_loop.cc:441
    #12 0x7f049e1374b3 in Run /usr/local/google/home/ricea/src/out/Release/../../base/run_loop.cc:45
    #13 0x7f049e0dcacd in Run /usr/local/google/home/ricea/src/out/Release/../../base/message_loop.cc:321
    #14 0x7f0493d1f9ae in IOThreadRun /usr/local/google/home/ricea/src/out/Release/../../content/browser/browser_thread_impl.cc:164
    #15 0x7f0493d1fc25 in Run /usr/local/google/home/ricea/src/out/Release/../../content/browser/browser_thread_impl.cc:192
    #16 0x7f049e191eeb in ThreadMain /usr/local/google/home/ricea/src/out/Release/../../base/threading/thread.cc:203
    #17 0x7f049e17e528 in ThreadFunc /usr/local/google/home/ricea/src/out/Release/../../base/threading/platform_thread_posix.cc:80
    #18 0x7f04a1e04c31 in __asan::AsanThread::ThreadStart(unsigned long) ??:0
Thread T17 (Chrome_IOThread) created by T0 (chrome) here:
    #0 0x7f04a1dfaaf8 in pthread_create ??:0
    #1 0x7f049e17e02a in CreateThread /usr/local/google/home/ricea/src/out/Release/../../base/threading/platform_thread_posix.cc:120
    #2 0x7f049e17dd5c in Create /usr/local/google/home/ricea/src/out/Release/../../base/threading/platform_thread_posix.cc:199
    #3 0x7f049e191542 in StartWithOptions /usr/local/google/home/ricea/src/out/Release/../../base/threading/thread.cc:92
    #4 0x7f0493cf0601 in CreateThreads /usr/local/google/home/ricea/src/out/Release/../../content/browser/browser_main_loop.cc:540
    #5 0x7f0493cf6ec7 in Initialize /usr/local/google/home/ricea/src/out/Release/../../content/browser/browser_main_runner.cc:112
    #6 0x7f0493cec082 in BrowserMain /usr/local/google/home/ricea/src/out/Release/../../content/browser/browser_main.cc:18
    #7 0x7f0493cada7d in RunNamedProcessTypeMain /usr/local/google/home/ricea/src/out/Release/../../content/app/content_main_runner.cc:433
    #8 0x7f0493caf310 in Run /usr/local/google/home/ricea/src/out/Release/../../content/app/content_main_runner.cc:756
    #9 0x7f0493cabe81 in ContentMain /usr/local/google/home/ricea/src/out/Release/../../content/app/content_main.cc:35
    #10 0x7f04a1e0c876 in ChromeMain /usr/local/google/home/ricea/src/out/Release/../../chrome/app/chrome_main.cc:32
    #11 0x7f04a1e0c7ba in main /usr/local/google/home/ricea/src/out/Release/../../chrome/app/chrome_exe_main_gtk.cc:39
    #12 0x7f048bec876c in __libc_start_main /build/buildd/eglibc-2.15/csu/libc-start.c:226
Shadow bytes around the buggy address:
  0x0c1e7ffffa50: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x0c1e7ffffa60: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c1e7ffffa70: fd fd fd fd fd fa fa fa fa fa fa fa fa fa fd fd
  0x0c1e7ffffa80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c1e7ffffa90: fd fd fd fa fa fa fa fa fa fa fa fa fd fd fd fd
=>0x0c1e7ffffaa0: fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd
  0x0c1e7ffffab0: fd fa fa fa fa fa fa fa fa fa 00 00 00 00 00 00
  0x0c1e7ffffac0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 fa
  0x0c1e7ffffad0: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x0c1e7ffffae0: 00 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa
  0x0c1e7ffffaf0: fa fa fa fa fa fa 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:     fa
  Heap righ redzone:     fb
  Freed Heap region:     fd
  Stack left redzone:    f1
  Stack mid redzone:     f2
  Stack right redzone:   f3
  Stack partial redzone: f4
  Stack after return:    f5
  Stack use after scope: f8
  Global redzone:        f9
  Global init order:     f6
  Poisoned by user:      f7
  ASan internal:         fe
==24202==ABORTING

The crash occurs while looking up a member of the ChromeUrlRequestContext object, which confirms my suspicion that it is a dangling UrlRequestContext pointer that is the root cause of the crash. Without ASAN, it doesn't crash until slightly later when it tries to use the NetworkDelegate pointer it retrieved from the ChromeUrlRequestContext object in NetworkDelegate::NotifyBeforeSocketStreamConnect.

I have filed https://crbug.com/chromium/244746 to do a narrowly-scoped fix of this particular issue, as I am in the middle of trying to deprecate net::SocketStream and I don't want to embark on a large-scale refactoring of it.

### th...@gmail.com (2013-05-29)

I can't access it, Could you add me to it?

### ri...@chromium.org (2013-05-29)

+therealholden try it now.

### in...@chromium.org (2013-06-06)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-06-21)

M28: r207666

### pa...@chromium.org (2013-06-27)

$3133.7 for this one!

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties.
          *********************************

### sc...@gmail.com (2013-07-03)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-08-20)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### tk...@chromium.org (2015-11-27)

[Empty comment from Monorail migration]

### tk...@chromium.org (2015-11-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/242762?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>Network>WebSockets, Blink>Workers]
[Monorail mergedwith: crbug.com/chromium/244726]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077581)*
