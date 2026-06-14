# Use After Free in Websockets - possible remote code execution within sandbox 

| Field | Value |
|-------|-------|
| **Issue ID** | [40089275](https://issues.chromium.org/issues/40089275) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ma...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-03-25 |
| **Bounty** | $1,000.00 |

## Description

Immediately calling a close() method on WebSocket object
can cause a user-after-free vulnerability.


Traceback from 32 bit Ubuntu 10.10:

$ apt-cache show chromium-browser 
Architecture: i386
Version: 10.0.648.133~r77742-0ubuntu0.10.10.1
MD5sum: d60ffe21bb75d18013d94ae59ff832c7

$ apt-cache show chromium-browser-dbg
Version: 10.0.648.133~r77742-0ubuntu0.10.10.1
MD5sum: 7c327515d8040ca547d5df356ebb4914

(Prerequisites: python2, pycurl, python-virtualenv)
$ cd websockets-dangling; make
 [*] Listening on http://127.0.0.1:8000/

$ chromium-browser --debug  --single-process http://127.0.0.1:8000/
(gdb) bt
#0  0x01beb74f in WebCore::WebSocketChannel::didClose (this=0x34847e0, handle=0x348c0e0) at third_party/WebKit/Source/WebCore/websockets/WebSocketChannel.cpp:180
#1  0x01f15a14 in WebCore::SocketStreamHandleInternal::didClose (this=0x358e7e0, socketHandle=0x3294200) at third_party/WebKit/Source/WebKit/chromium/src/SocketStreamHandle.cpp:171
#2  0x01199027 in webkit_glue::WebSocketStreamHandleImpl::Context::DidClose (this=0x358e7c0, web_handle=0x3294200) at webkit/glue/websocketstreamhandle_impl.cc:134
#3  0x01dd7828 in IPCWebSocketStreamHandleBridge::OnClosed (this=0x358e7a0) at chrome/common/socket_stream_dispatcher.cc:131
#4  0x01dd7c02 in DispatchToMethod<SocketStreamDispatcher, void (SocketStreamDispatcher::*)(int), int> (this=0x3183900, msg=...) at ./base/tuple.h:551
#5  Dispatch<SocketStreamDispatcher, SocketStreamDispatcher, void (SocketStreamDispatcher::*)(int)> (this=0x3183900, msg=...) at ./ipc/ipc_message_utils.h:929
#6  SocketStreamDispatcher::OnMessageReceived (this=0x3183900, msg=...) at chrome/common/socket_stream_dispatcher.cc:173
#7  0x01dea857 in ChildThread::OnMessageReceived (this=0x30bec64, msg=...) at chrome/common/child_thread.cc:146
#8  0x010e8a7b in IPC::ChannelProxy::Context::OnDispatchMessage (this=0x3386840, message=...) at ipc/ipc_channel_proxy.cc:255
#9  0x010e8bca in DispatchToMethod<IPC::ChannelProxy::Context, void (IPC::ChannelProxy::Context::*)(IPC::Message const&), IPC::Message> (this=0x3533360) at ./base/tuple.h:551
#10 RunnableMethod<IPC::ChannelProxy::Context, void (IPC::ChannelProxy::Context::*)(IPC::Message const&), Tuple1<IPC::Message> >::Run (this=0x3533360) at ./base/task.h:331
#11 0x00a8d703 in MessageLoop::RunTask (this=0xb0ba10dc, task=0x3533360) at base/message_loop.cc:356
#12 0x00a8e4de in MessageLoop::DeferOrRunPendingTask (this=0xb0ba10dc, pending_task=...) at base/message_loop.cc:365
#13 0x00a8e7cc in MessageLoop::DoWork (this=0xb0ba10dc) at base/message_loop.cc:558
#14 0x00a91070 in base::MessagePumpDefault::Run (this=0x33859a0, delegate=0xb0ba10dc) at base/message_pump_default.cc:23
#15 0x00a8e1c4 in MessageLoop::RunInternal (this=0xb0ba10dc) at base/message_loop.cc:331
#16 0x00a8e2ed in RunHandler (this=0x2e74654e) at base/message_loop.cc:304
#17 MessageLoop::Run (this=0x2e74654e) at base/message_loop.cc:234
#18 0x00ab305d in base::Thread::Run (this=0x3363c60, message_loop=0xb0ba10dc) at base/threading/thread.cc:128
#19 0x00ab359b in base::Thread::ThreadMain (this=0x3363c60) at base/threading/thread.cc:164
#20 0x00ab288c in base::(anonymous namespace)::ThreadFunc (params=0x32bb388) at base/threading/platform_thread_posix.cc:51
#21 0xb7586cc9 in start_thread () from /lib/libpthread.so.0
#22 0xb71266ae in clone () from /lib/libc.so.6

(gdb) disassemble 
Dump of assembler code for function WebCore::WebSocketChannel::didClose(WebCore::SocketStreamHandle*):
   [...]		
   0x01beb740 <+208>:	mov    (%edi),%eax
   0x01beb742 <+210>:	mov    0x10c(%esi),%edx
   0x01beb748 <+216>:	mov    %edi,(%esp)
   0x01beb74b <+219>:	mov    %edx,0x4(%esp)
=> 0x01beb74f <+223>:	call   *0x14(%eax)
   [...]

(gdb) info r
eax            0x2e74654e	779380046
ecx            0x2	2
edx            0x0	0
ebx            0x2f4e324	49603364
esp            0xb0ba0c90	0xb0ba0c90
ebp            0xb0ba0cc8	0xb0ba0cc8
esi            0x34847e0	55068640
edi            0x33ab384	54178692
eip            0x1beb74f	0x1beb74f <WebCore::WebSocketChannel::didClose(WebCore::SocketStreamHandle*)+223>
eflags         0x10206	[ PF IF RF ]

(gdb) x/s $edi
0x33ab384:	 "Net.PreconnectUtilization2_ConnectBackupJobsEnabled"

(gdb) p *client
$1 = {_vptr.WebSocketChannelClient = 0x2e74654e}


The traceback is caused by a dereference of a dangling pointer to
WebSocketChannelClient in the WebSocketChannel instance.

void WebSocketChannel::didClose(SocketStreamHandle* handle)
{
    [...]
    if (m_handle) {
        [...]
        WebSocketChannelClient* client = m_client;
        m_client = 0;
        m_context = 0;
        m_handle = 0;
        if (client)
            client->didClose(m_unhandledBufferedAmount); ## client is already released
    }
    deref();
}

To trigger the bug one need to create a websocket connection and immediately call
close(), before the onconnect event.

     var ws = new WebSocket(wsurl);
     ws.close();

At that point, the tcp/ip connection will still be hanging. When the websockets server
decides to close the connection, the didClose() method is called. To trigger
the bug the page needs to be refreshed a few times.

Test case includes a simple websockets http server: the cooperation of
websockets server is required - in oder to close the websockets connection at a proper moment.


I was able to trigger this bug in some form on Chrome/Chromium on Linux/32bits & 64bits,
Windows/32bits, Mac/64bits - though sometimes it required few page refreshes and some
modifications to the javascript.


## Attachments

- [websockets-dangling.tar.gz](attachments/websockets-dangling.tar.gz) (application/x-gzip; charset=binary, 1.1 KB)

## Timeline

### in...@chromium.org (2011-03-25)

@ukai, can you please take a look.

### uk...@chromium.org (2011-03-25)

https://bugs.webkit.org/show_bug.cgi?id=57081

### in...@chromium.org (2011-03-28)

Thanks Ukai. Fixed in http://trac.webkit.org/changeset/82088

### sc...@gmail.com (2011-03-29)

Merge to M11: Committed revision 82355.

@majek04: thanks for the great bug. The rewards panel will be discussing it :) What name would you like us to use for crediting you in our Chrome 11 release notes?

### ma...@gmail.com (2011-03-29)

Great! I'm "Marek Majkowski", I would be delighted to see my name in the release notes :)

### sc...@gmail.com (2011-04-14)

@majek04: it's a pleasure to see a new face reporting really good quality security bugs. Thanks for the stacktrace, registers, instuctions, nice testcase and code analysis!
It's also a pleasure to tag this bug with a provisional $1000 Chromium Security Reward :)

### sc...@gmail.com (2011-04-22)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-04-29)

Ok, ping cevans@chromium.org to set up payment :)

### sc...@gmail.com (2011-05-27)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/77346?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089275)*
