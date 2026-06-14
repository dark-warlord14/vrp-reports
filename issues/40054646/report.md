# Heap-use-after-free in MessageLoop::AddToIncomingQueue

| Field | Value |
|-------|-------|
| **Issue ID** | [40054646](https://issues.chromium.org/issues/40054646) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals, Internals>Media, Internals>Media>Video |
| **Platforms** | Linux |
| **Reporter** | ch...@gmail.com |
| **Assignee** | fi...@chromium.org |
| **Created** | 2012-03-08 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Running attached test.html file on chrome causes chrome to display sad tab because of a use after free.

**VERSION**  

Chrome Version: [19.0.1063.0 (125560)] + [dev]  

Operating System: [Ubuntu 10.04 64 bit]

**REPRODUCTION CASE**

1. Download and copy attached test.html and out.ogv to same folder.
2. Open chrome and open test.html.
3. Wait about 5 minutes.
4. Chrome will display sad tab.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tab]  

Crash State: Asan output

==12591== ERROR: AddressSanitizer heap-use-after-free on address 0x7ffcbb0cde80 at pc 0x7ffcfc4b2c26 bp 0x7ffcec0f4410 sp 0x7ffcec0f4408  

READ of size 4 at 0x7ffcbb0cde80 thread T1  

#0 0x7ffcfc4b2c26 in \_ZN17FileDescriptorSet14SetDescriptorsEPKij /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/ipc/file\_descriptor\_set\_posix.cc:137  

#1 0x7ffcfc493ea5 in \_ZN3IPC7Channel11ChannelImpl24WillDispatchInputMessageEPNS\_7MessageE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/ipc/ipc\_channel\_posix.cc:1074  

#2 0x7ffcfc4936a4 in \_ZN3IPC7Channel11ChannelImpl17DispatchInputDataEPKci /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/ipc/ipc\_channel\_posix.cc:524  

#3 0x7ffcfc492cfb in \_ZN3IPC7Channel11ChannelImpl23ProcessIncomingMessagesEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/ipc/ipc\_channel\_posix.cc:492  

#4 0x7ffcfc497c1d in \_ZN3IPC7Channel11ChannelImpl28OnFileCanReadWithoutBlockingEi /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/ipc/ipc\_channel\_posix.cc:859  

#5 0x7ffcfc31a62e in *ZN4base19MessagePumpLibevent21FileDescriptorWatcher28OnFileCanReadWithoutBlockingEiPS0* /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_pump\_libevent.cc:109  

#6 0x7ffcfc454fba in event\_process\_active /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third\_party/libevent/event.c:386  

#7 0x7ffcfc31ae1d in \_ZN4base19MessagePumpLibevent3RunEPNS\_11MessagePump8DelegateE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_pump\_libevent.cc:268  

#8 0x7ffcfc38237e in \_ZN11MessageLoop11RunInternalEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:418  

#9 0x7ffcfc38056f in ~AutoRunState /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:745  

#10 0x7ffcfc3fe73c in \_ZN4base6Thread10ThreadMainEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/threading/thread.cc:161  

#11 0x7ffcfc3f45ac in \_ZN4base12\_GLOBAL\_\_N\_110ThreadFuncEPv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/threading/platform\_thread\_posix.cc:63  

#12 0x7ffd02565cc5 in \_ZN6\_\_asan10AsanThread11ThreadStartEv ??:0  

0x7ffcbb0cde80 is located 0 bytes to the right of 512-byte region [0x7ffcbb0cdc80,0x7ffcbb0cde80)  

allocated by thread T1 here:  

#0 0x7ffd02560512 in \_Znwm ??:0  

#1 0x7ffcfc49c74a in \_ZNSt5dequeIiSaIiEE24\_M\_new\_elements\_at\_frontEm /usr/lib/gcc/x86\_64-linux-gnu/4.4/../../../../include/c++/4.4/bits/deque.tcc:758  

#2 0x7ffcfc499fd4 in \_ZNSt5dequeIiSaIiEE28\_M\_reserve\_elements\_at\_frontEm /usr/lib/gcc/x86\_64-linux-gnu/4.4/../../../../include/c++/4.4/bits/stl\_deque.h:1684  

#3 0x7ffcfc498adf in \_ZN3IPC7Channel11ChannelImpl32ExtractFileDescriptorsFromMsghdrEP6msghdr /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/ipc/ipc\_channel\_posix.cc:1106  

#4 0x7ffcfc493c4d in \_ZN3IPC7Channel11ChannelImpl29ReadFileDescriptorsFromFDPipeEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/ipc/ipc\_channel\_posix.cc:1032  

#5 0x7ffcfc4936a4 in \_ZN3IPC7Channel11ChannelImpl17DispatchInputDataEPKci /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/ipc/ipc\_channel\_posix.cc:524  

#6 0x7ffcfc492cfb in \_ZN3IPC7Channel11ChannelImpl23ProcessIncomingMessagesEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/ipc/ipc\_channel\_posix.cc:492  

#7 0x7ffcfc497c1d in \_ZN3IPC7Channel11ChannelImpl28OnFileCanReadWithoutBlockingEi /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/ipc/ipc\_channel\_posix.cc:859  

#8 0x7ffcfc31a62e in *ZN4base19MessagePumpLibevent21FileDescriptorWatcher28OnFileCanReadWithoutBlockingEiPS0* /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_pump\_libevent.cc:109  

#9 0x7ffcfc454fba in event\_process\_active /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third\_party/libevent/event.c:386  

#10 0x7ffcfc31ae1d in \_ZN4base19MessagePumpLibevent3RunEPNS\_11MessagePump8DelegateE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_pump\_libevent.cc:268  

#11 0x7ffcfc38237e in \_ZN11MessageLoop11RunInternalEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:418  

#12 0x7ffcfc38056f in ~AutoRunState /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:745  

#13 0x7ffcfc3fe73c in \_ZN4base6Thread10ThreadMainEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/threading/thread.cc:161  

#14 0x7ffcfc3f45ac in \_ZN4base12\_GLOBAL\_\_N\_110ThreadFuncEPv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/threading/platform\_thread\_posix.cc:63  

#15 0x7ffd02565cc5 in \_ZN6\_\_asan10AsanThread11ThreadStartEv ??:0  

Thread T1 created by T0 here:  

#0 0x7ffd02560813 in pthread\_create ??:0  

#1 0x7ffcfc3f4259 in \_ZN4base12\_GLOBAL\_\_N\_112CreateThreadEmbPNS\_14PlatformThread8DelegateEPm /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/threading/platform\_thread\_posix.cc:124  

#2 0x7ffcfc3f415a in \_ZN4base14PlatformThread6CreateEmPNS0\_8DelegateEPm /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/threading/platform\_thread\_posix.cc:228  

#3 0x7ffcfc3fe015 in \_ZN4base6Thread16StartWithOptionsERKNS0\_7OptionsE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/threading/thread.cc:72  

#4 0x7ffcfd770c0f in \_ZN12ChildProcessC2Ev /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/common/child\_process.cc:32  

#5 0x7ffd0125ae33 in \_ZN17RenderProcessImplC2Ev /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/renderer/render\_process\_impl.cc:41  

#6 0x7ffd012f0f76 in \_Z12RendererMainRKN7content18MainFunctionParamsE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/renderer/renderer\_main.cc:227  

#7 0x7ffcfc2da0d6 in RunZygote /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/app/content\_main\_runner.cc:245  

#8 0x7ffcfc2d864a in \_ZN7content11ContentMainEiPPKcPNS\_19ContentMainDelegateE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/app/content\_main.cc:35  

#9 0x7ffcfaa1f2e7 in ChromeMain /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/chrome/app/chrome\_main.cc:32  

#10 0x7ffcfaa1f23b in main /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#11 0x7ffcf3e98c4d in \_\_libc\_start\_main /build/buildd/eglibc-2.11.1/csu/libc-start.c:258  

==12591== ABORTING  

Stats: 483M malloced (182M for red zones) by 101292 calls  

Stats: 24M realloced by 6514 calls  

Stats: 472M freed by 88010 calls  

Stats: 282M really freed by 61684 calls  

Stats: 356M (91217 full pages) mmaped in 89 calls  

mmaps by size class: 8:49149; 9:8191; 10:8190; 11:4094; 12:1024; 13:2560; 14:768; 15:640; 16:192; 17:128; 18:160; 19:128; 20:16; 21:22; 22:19;  

mallocs by size class: 8:69696; 9:9685; 10:8163; 11:3434; 12:1238; 13:4998; 14:1537; 15:1262; 16:331; 17:257; 18:331; 19:258; 20:26; 21:36; 22:40;  

frees by size class: 8:57984; 9:9015; 10:7791; 11:3153; 12:1157; 13:4967; 14:1513; 15:1185; 16:317; 17:248; 18:329; 19:252; 20:25; 21:35; 22:39;  

rfrees by size class: 8:41534; 9:6353; 10:5530; 11:2032; 12:664; 13:3355; 14:809; 15:645; 16:207; 17:161; 18:194; 19:138; 20:17; 21:21; 22:24;  

Stats: malloc large: 948 small slow: 1535  

Shadow byte and word:  

0x1fff97619bd0: fd  

0x1fff97619bd0: fd fd fd fd fd fd fd fd  

More shadow bytes:  

0x1fff97619bb0: 00 00 00 00 00 00 00 00  

0x1fff97619bb8: 00 00 00 00 00 00 00 00  

0x1fff97619bc0: 00 00 00 00 00 00 00 00  

0x1fff97619bc8: 00 00 00 00 00 00 00 00  

=>0x1fff97619bd0: fd fd fd fd fd fd fd fd  

0x1fff97619bd8: fd fd fd fd fd fd fd fd  

0x1fff97619be0: fa fa fa fa fa fa fa fa  

0x1fff97619be8: fa fa fa fa fa fa fa fa  

0x1fff97619bf0: fa fa fa fa fa fa fa fa

## Attachments

- [out.ogv](attachments/out.ogv) (application/ogg; charset=binary, 1.3 MB)
- [test.html](attachments/test.html) (text/html; charset=us-ascii, 539 B)
- [issue10019018_1.diff](attachments/issue10019018_1.diff) (text/x-diff; charset=us-ascii, 2.1 KB)

## Timeline

### in...@chromium.org (2012-03-08)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-08)

[Empty comment from Monorail migration]

### ch...@gmail.com (2012-03-13)

This issue might not be a duplicate of 117335. Because I can still reproduce this issue after 117335 is fixed.

### in...@chromium.org (2012-03-13)

Tommi, can you please take a look

### to...@chromium.org (2012-03-13)

I don't suppose there's a way for you guys to figure out which IPC message it is that causes the fd to be created?

### ch...@gmail.com (2012-03-13)

tommi, I could not understand your comment.Is there something I should do?

### to...@chromium.org (2012-03-13)

It looks to me that the FD is created as a result of an IPC message from another process.  E.g. it could be created because the browser process sends an FD to the renderer process.  A SyncSocket is one example.

If that's correct, then when ExtractFileDescriptorsFromMsghdrEP is called on T1, it is extracting this IPC message and creating or dup-ing an fd that was actually created in a different process.  In addition to the fd, the message will have several other properties such as an id and other parameters.  Eventually the message will be routed based in this information to a handler function.

So, if it is possible to find out what the id is for this message, we can figure out where the fd originated and have a look at the code and see what's going on.

### in...@chromium.org (2012-03-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-13)

[Empty comment from Monorail migration]

### [Deleted User] (2012-03-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-23)

From regression range, this seems like coming from http://src.chromium.org/viewvc/chrome?view=rev&revision=128289

xhwang@, can you please take a look. m19 branching will happen soon, so we don't want to ship with this security regression.

### in...@chromium.org (2012-03-23)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=29480667

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free WRITE 1
Crash Address: 0x7fa7d19725c0
Crash State:
  - crash stack -
  MessageLoop::AddToIncomingQueue
  MessageLoop::PostTask
  - free stack -
  std::deque<base::PendingTask, std::allocator<base::PendingTask> >::~deque
  MessageLoop::~MessageLoop
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=128281:128300

Minimized Testcase (1230.33 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97maeo6XtF_Vtvq6APcxIRIYc1y7uTQdUYzyML5_Dk7-KdIgABViScP3amhP7QlWkqWjHftXVnkk_kI9PtqztawKQ6FNki71gYDXswijtO2K13R5YfhY2N8nWiqGIABI1em2iYO_b3hTliggQu4GD3PKMauLA

### xh...@chromium.org (2012-03-23)

I am now fully occupied and will start vacation later next week. So I am really not sure if I'll have time to look at it.

### in...@chromium.org (2012-03-23)

better stack from my local

[20762:20777:2155943715236:ERROR:proxy_service_factory.cc(84)] Cannot use V8 Proxy resolver in single process mode.
[20762:20777:2155944044347:ERROR:proxy_service_factory.cc(84)] Cannot use V8 Proxy resolver in single process mode.
[20762:20777:2155944085535:ERROR:proxy_service_factory.cc(84)] Cannot use V8 Proxy resolver in single process mode.
libprotobuf ERROR third_party/protobuf/src/google/protobuf/message_lite.cc:123] Can't parse message of type "in_memory_url_index.InMemoryURLIndexCacheItem" because it is missing required fields: (cannot determine missing fields for lite message)
=================================================================
==20762== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fe3c1985a80 at pc 0x7fe410a166c6 bp 0x7fe3ee43f410 sp 0x7fe3ee43f408
READ of size 4 at 0x7fe3c1985a80 thread T16
    #0 0x7fe410a166c6 in FileDescriptorSet::SetDescriptors(int const*, unsigned int) ipc/file_descriptor_set_posix.cc:137
    #1 0x7fe4109fade5 in IPC::Channel::ChannelImpl::WillDispatchInputMessage(IPC::Message*) ipc/ipc_channel_posix.cc:1010
    #2 0x7fe410a07110 in IPC::internal::ChannelReader::DispatchInputData(char const*, int) ipc/ipc_channel_reader.cc:70
    #3 0x7fe410a06d8b in IPC::internal::ChannelReader::ProcessIncomingMessages() ipc/ipc_channel_reader.cc:29
    #4 0x7fe4109f9160 in IPC::Channel::ChannelImpl::OnFileCanReadWithoutBlocking(int) ipc/ipc_channel_posix.cc:794
    #5 0x7fe410881f2e in base::MessagePumpLibevent::FileDescriptorWatcher::OnFileCanReadWithoutBlocking(int, base::MessagePumpLibevent*) base/message_pump_libevent.cc:109
    #6 0x7fe4109bd23a in event_process_active third_party/libevent/event.c:386
    #7 0x7fe41088271d in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_pump_libevent.cc:268
    #8 0x7fe4108e9f8e in MessageLoop::RunInternal() base/message_loop.cc:418
    #9 0x7fe4108e817f in ~AutoRunState base/message_loop.cc:745
    #10 0x7fe4109669bc in base::Thread::ThreadMain() base/threading/thread.cc:161
    #11 0x7fe41095c6ec in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:63
    #12 0x7fe4170a4b75 in __asan::AsanThread::ThreadStart() ??:0
0x7fe3c1985a80 is located 0 bytes to the right of 512-byte region [0x7fe3c1985880,0x7fe3c1985a80)
allocated by thread T16 here:
    #0 0x7fe41709f3c2 in operator new(unsigned long) ??:0
    #1 0x7fe4109ff6da in std::deque<int, std::allocator<int> >::_M_new_elements_at_front(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/4.4/../../../../include/c++/4.4/bits/deque.tcc:758
    #2 0x7fe4109fcf64 in std::deque<int, std::allocator<int> >::_M_reserve_elements_at_front(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/4.4/../../../../include/c++/4.4/bits/stl_deque.h:1684
    #3 0x7fe4109fa70f in IPC::Channel::ChannelImpl::ExtractFileDescriptorsFromMsghdr(msghdr*) ipc/ipc_channel_posix.cc:1042
    #4 0x7fe4109fab8d in IPC::Channel::ChannelImpl::ReadFileDescriptorsFromFDPipe() ipc/ipc_channel_posix.cc:963
    #5 0x7fe410a07110 in IPC::internal::ChannelReader::DispatchInputData(char const*, int) ipc/ipc_channel_reader.cc:70
    #6 0x7fe410a06d8b in IPC::internal::ChannelReader::ProcessIncomingMessages() ipc/ipc_channel_reader.cc:29
    #7 0x7fe4109f9160 in IPC::Channel::ChannelImpl::OnFileCanReadWithoutBlocking(int) ipc/ipc_channel_posix.cc:794
    #8 0x7fe410881f2e in base::MessagePumpLibevent::FileDescriptorWatcher::OnFileCanReadWithoutBlocking(int, base::MessagePumpLibevent*) base/message_pump_libevent.cc:109
    #9 0x7fe4109bd23a in event_process_active third_party/libevent/event.c:386
    #10 0x7fe41088271d in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_pump_libevent.cc:268
    #11 0x7fe4108e9f8e in MessageLoop::RunInternal() base/message_loop.cc:418
    #12 0x7fe4108e817f in ~AutoRunState base/message_loop.cc:745
    #13 0x7fe4109669bc in base::Thread::ThreadMain() base/threading/thread.cc:161
    #14 0x7fe41095c6ec in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:63
    #15 0x7fe4170a4b75 in __asan::AsanThread::ThreadStart() ??:0
Thread T16 created by T15 here:
    #0 0x7fe41709f6c3 in pthread_create ??:0
    #1 0x7fe41095c399 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, unsigned long*) base/threading/platform_thread_posix.cc:124
    #2 0x7fe41095c29a in base::PlatformThread::Create(unsigned long, base::PlatformThread::Delegate*, unsigned long*) base/threading/platform_thread_posix.cc:228
    #3 0x7fe410966295 in base::Thread::StartWithOptions(base::Thread::Options const&) base/threading/thread.cc:72
    #4 0x7fe411d2683f in ChildProcess::ChildProcess() content/common/child_process.cc:32
    #5 0x7fe415c6bb91 in RenderProcessImpl::RenderProcessImpl() content/renderer/render_process_impl.cc:42
    #6 0x7fe415527c5f in RendererMainThread::Init() content/browser/renderer_host/render_process_host_impl.cc:155
    #7 0x7fe41096694e in base::Thread::ThreadMain() base/threading/thread.cc:155
    #8 0x7fe41095c6ec in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:63
    #9 0x7fe4170a4b75 in __asan::AsanThread::ThreadStart() ??:0
==20762== ABORTING
Stats: 731M malloced (391M for red zones) by 521531 calls
Stats: 31M realloced by 20365 calls
Stats: 641M freed by 399708 calls
Stats: 448M really freed by 342030 calls
Stats: 608M (155764 full pages) mmaped in 151 calls
  mmaps   by size class: 8:360426; 9:24573; 10:20475; 11:10235; 12:4096; 13:4096; 14:1280; 15:896; 16:512; 17:192; 18:192; 19:176; 20:24; 21:38; 22:18; 23:1;
  mallocs by size class: 8:438265; 9:26414; 10:24286; 11:13346; 12:4746; 13:7618; 14:2806; 15:1853; 16:772; 17:432; 18:437; 19:397; 20:43; 21:74; 22:41; 23:1;
  frees   by size class: 8:327668; 9:23305; 10:22825; 11:8256; 12:4123; 13:7375; 14:2551; 15:1595; 16:714; 17:398; 18:424; 19:345; 20:38; 21:56; 22:34; 23:1;
  rfrees  by size class: 8:283507; 9:19105; 10:19555; 11:6328; 12:3361; 13:5716; 14:1835; 15:1143; 16:599; 17:288; 18:273; 19:226; 20:30; 21:40; 22:23; 23:1;
Stats: malloc large: 1425 small slow: 3573
Shadow byte and word:
  0x1ffc78330b50: fa
  0x1ffc78330b50: fa fa fa fa fa fa fa fa
More shadow bytes:
  0x1ffc78330b30: 00 00 00 00 00 00 00 00
  0x1ffc78330b38: 00 00 00 00 00 00 00 00
  0x1ffc78330b40: 00 00 00 00 00 00 00 00
  0x1ffc78330b48: 00 00 00 00 00 00 00 00
=>0x1ffc78330b50: fa fa fa fa fa fa fa fa
  0x1ffc78330b58: fa fa fa fa fa fa fa fa
  0x1ffc78330b60: fa fa fa fa fa fa fa fa
  0x1ffc78330b68: fa fa fa fa fa fa fa fa
  0x1ffc78330b70: fa fa fa fa fa fa fa fa


### in...@chromium.org (2012-03-23)

ah! didnt see c#0, regression range is wrong on this one. it reproduced on chrome 125560, but it is definitely related to some media change.
Andrew, can you please help with an owner for this ?

### ao...@gmail.com (2012-03-23)

This likely started happening a bit before 124615 according to c#21 @ https://crbug.com/chromium/115299. May have also been an older issue which was just made reachable by the fix. 

### in...@chromium.org (2012-03-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-23)

Miaubiz extremely simple repro crashes on this use-after-free

<html>
  <head>
    <script>
      setTimeout("window.location.reload()", Math.random()*200)
    </script>
  </head>
  <body>
    <video src='test.ogv'></video>
  </body>
</html>

=================================================================
==32167== ERROR: AddressSanitizer heap-use-after-free on address 0x7f896315b280 at pc 0x7f897d2b36c6 bp 0x7f895aced410 sp 0x7f895aced408
READ of size 4 at 0x7f896315b280 thread T16
    #0 0x7f897d2b36c6 in FileDescriptorSet::SetDescriptors(int const*, unsigned int) ipc/file_descriptor_set_posix.cc:137
    #1 0x7f897d297de5 in IPC::Channel::ChannelImpl::WillDispatchInputMessage(IPC::Message*) ipc/ipc_channel_posix.cc:1010
    #2 0x7f897d2a4110 in IPC::internal::ChannelReader::DispatchInputData(char const*, int) ipc/ipc_channel_reader.cc:70
    #3 0x7f897d2a3d8b in IPC::internal::ChannelReader::ProcessIncomingMessages() ipc/ipc_channel_reader.cc:29
    #4 0x7f897d296160 in IPC::Channel::ChannelImpl::OnFileCanReadWithoutBlocking(int) ipc/ipc_channel_posix.cc:794
    #5 0x7f897d11ef2e in base::MessagePumpLibevent::FileDescriptorWatcher::OnFileCanReadWithoutBlocking(int, base::MessagePumpLibevent*) base/message_pump_libevent.cc:109
    #6 0x7f897d25a23a in event_process_active third_party/libevent/event.c:386
    #7 0x7f897d11f71d in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_pump_libevent.cc:268
    #8 0x7f897d186f8e in MessageLoop::RunInternal() base/message_loop.cc:418
    #9 0x7f897d18517f in ~AutoRunState base/message_loop.cc:745
    #10 0x7f897d2039bc in base::Thread::ThreadMain() base/threading/thread.cc:161
    #11 0x7f897d1f96ec in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:63
    #12 0x7f8983941b75 in __asan::AsanThread::ThreadStart() ??:0
0x7f896315b280 is located 0 bytes to the right of 512-byte region [0x7f896315b080,0x7f896315b280)
allocated by thread T16 here:
    #0 0x7f898393c3c2 in operator new(unsigned long) ??:0
    #1 0x7f897d29c6da in std::deque<int, std::allocator<int> >::_M_new_elements_at_front(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/4.4/../../../../include/c++/4.4/bits/deque.tcc:758
    #2 0x7f897d299f64 in std::deque<int, std::allocator<int> >::_M_reserve_elements_at_front(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/4.4/../../../../include/c++/4.4/bits/stl_deque.h:1684
    #3 0x7f897d29770f in IPC::Channel::ChannelImpl::ExtractFileDescriptorsFromMsghdr(msghdr*) ipc/ipc_channel_posix.cc:1042
    #4 0x7f897d297b8d in IPC::Channel::ChannelImpl::ReadFileDescriptorsFromFDPipe() ipc/ipc_channel_posix.cc:963
    #5 0x7f897d2a4110 in IPC::internal::ChannelReader::DispatchInputData(char const*, int) ipc/ipc_channel_reader.cc:70
    #6 0x7f897d2a3d8b in IPC::internal::ChannelReader::ProcessIncomingMessages() ipc/ipc_channel_reader.cc:29
    #7 0x7f897d296160 in IPC::Channel::ChannelImpl::OnFileCanReadWithoutBlocking(int) ipc/ipc_channel_posix.cc:794
    #8 0x7f897d11ef2e in base::MessagePumpLibevent::FileDescriptorWatcher::OnFileCanReadWithoutBlocking(int, base::MessagePumpLibevent*) base/message_pump_libevent.cc:109
    #9 0x7f897d25a23a in event_process_active third_party/libevent/event.c:386
    #10 0x7f897d11f71d in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_pump_libevent.cc:268
    #11 0x7f897d186f8e in MessageLoop::RunInternal() base/message_loop.cc:418
    #12 0x7f897d18517f in ~AutoRunState base/message_loop.cc:745
    #13 0x7f897d2039bc in base::Thread::ThreadMain() base/threading/thread.cc:161
    #14 0x7f897d1f96ec in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:63
    #15 0x7f8983941b75 in __asan::AsanThread::ThreadStart() ??:0
Thread T16 created by T15 here:
    #0 0x7f898393c6c3 in pthread_create ??:0
    #1 0x7f897d1f9399 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, unsigned long*) base/threading/platform_thread_posix.cc:124
    #2 0x7f897d1f929a in base::PlatformThread::Create(unsigned long, base::PlatformThread::Delegate*, unsigned long*) base/threading/platform_thread_posix.cc:228
    #3 0x7f897d203295 in base::Thread::StartWithOptions(base::Thread::Options const&) base/threading/thread.cc:72
    #4 0x7f897e5c383f in ChildProcess::ChildProcess() content/common/child_process.cc:32
    #5 0x7f8982508b91 in RenderProcessImpl::RenderProcessImpl() content/renderer/render_process_impl.cc:42
    #6 0x7f8981dc4c5f in RendererMainThread::Init() content/browser/renderer_host/render_process_host_impl.cc:155
    #7 0x7f897d20394e in base::Thread::ThreadMain() base/threading/thread.cc:155
    #8 0x7f897d1f96ec in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:63
    #9 0x7f8983941b75 in __asan::AsanThread::ThreadStart() ??:0
==32167== ABORTING
Stats: 891M malloced (739M for red zones) by 987267 calls
Stats: 170M realloced by 50415 calls
Stats: 835M freed by 855221 calls
Stats: 688M really freed by 725370 calls
Stats: 548M (140384 full pages) mmaped in 134 calls
  mmaps   by size class: 8:360426; 9:32764; 10:24570; 11:12282; 12:5120; 13:3072; 14:3072; 15:2688; 16:512; 17:288; 18:112; 19:112; 20:12; 21:4; 22:6; 23:3;
  mallocs by size class: 8:792535; 9:61789; 10:54597; 11:30099; 12:12923; 13:9045; 14:11676; 15:10586; 16:2165; 17:1104; 18:404; 19:302; 20:19; 21:4; 22:11; 23:8;
  frees   by size class: 8:673744; 9:58088; 10:52267; 11:25119; 12:12138; 13:8632; 14:11390; 15:10051; 16:2065; 17:1031; 18:378; 19:280; 20:17; 21:3; 22:10; 23:8;
  rfrees  by size class: 8:573349; 9:48322; 10:45185; 11:20496; 12:10125; 13:7313; 14:9119; 15:8281; 16:1742; 17:867; 18:315; 19:224; 20:15; 21:3; 22:8; 23:6;
Stats: malloc large: 1852 small slow: 10678
Shadow byte and word:
  0x1ff12c62b650: fd
  0x1ff12c62b650: fd fd fd fd fd fd fd fd
More shadow bytes:
  0x1ff12c62b630: 00 00 00 00 00 00 00 00
  0x1ff12c62b638: 00 00 00 00 00 00 00 00
  0x1ff12c62b640: 00 00 00 00 00 00 00 00
  0x1ff12c62b648: 00 00 00 00 00 00 00 00
=>0x1ff12c62b650: fd fd fd fd fd fd fd fd
  0x1ff12c62b658: fd fd fd fd fd fd fd fd
  0x1ff12c62b660: fa fa fa fa fa fa fa fa
  0x1ff12c62b668: fa fa fa fa fa fa fa fa
  0x1ff12c62b670: fa fa fa fa fa fa fa fa


### in...@chromium.org (2012-03-26)

We are branching for m19 soon, can someone please help to triage this.

### in...@chromium.org (2012-03-26)

[Empty comment from Monorail migration]

### sc...@chromium.org (2012-03-26)

The page is reloading at a random 0-200ms interval and <video> happens to be involved in reproducing the crash.

To help further triage inferno if you have a local build available can you try the following?
  1) Remove <video> entirely
  2) Replace test.ogv with http://tskir-html5.kir.corp.google.com/testmatrix/mediaFiles/sync/sync0.webm (has no audio)

If it still repros in (1) then it's not a media issue. If it doesn't repro with (2) then it's an audio issue.

### in...@chromium.org (2012-03-26)

1) removing <video> completely stop the crash, so it is media related.
2) replacing with sync0.webm stops crash, so it should be video issue.
sometimes it crashes with, but i don't think it is related to this OOB write.

==15977== CHECK failed: m->alloc_tid >= 0 at /usr/local/google/chrome/src/third_party/llvm/projects/compiler-rt/lib/asan/asan_allocator.cc:705
    #0 0x7fb4f952fe2e (/usr/local/google/home/aarya/chrome-asan/src/out/Release/chrome+0x8a8be2e)


### in...@chromium.org (2012-03-26)

With sync0.webm, one time it crashed with this stack (using ASAN_OPTIONS=sleep_before_dying=1000). So, looks like audio has something messed up too.

================================================================
==31060== ERROR: AddressSanitizer heap-use-after-free on address 0x7f7d30ea5570 at pc 0x7f7d5466b490 bp 0x7f7d0fee2ea0 sp 0x7f7d0fee2e98
WRITE of size 1 at 0x7f7d30ea5570 thread T91
    #0 0x7f7d5466b490 in std::deque<base::PendingTask, std::allocator<base::PendingTask> >::push_back(base::PendingTask const&) ./base/pending_task.h:21
    #1 0x7f7d5466ade3 in MessageLoop::PostTask(tracked_objects::Location const&, base::Callback<void ()()> const&) base/message_loop.cc:256
    #2 0x7f7d5a3539f6 in ~Callback ./base/callback.h:243
    #3 0x7f7d5a382018 in media::FFmpegVideoDecoder::Initialize(media::DemuxerStream*, base::Callback<void ()(media::PipelineStatus)> const&, base::Callback<void ()(media::PipelineStatistics const&)> const&) media/filters/ffmpeg_video_decoder.cc:128
    #4 0x7f7d5466f3c6 in base::Callback<void ()()>::Run() const ./base/callback.h:272
    #5 0x7f7d5466fc28 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) base/message_loop.cc:470
    #6 0x7f7d54670f19 in MessageLoop::DoWork() base/message_loop.cc:660
    #7 0x7f7d5467b437 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_pump_default.cc:28
    #8 0x7f7d5466df8e in MessageLoop::RunInternal() base/message_loop.cc:418
    #9 0x7f7d5466c17f in ~AutoRunState base/message_loop.cc:745
    #10 0x7f7d546ea9bc in base::Thread::ThreadMain() base/threading/thread.cc:161
    #11 0x7f7d546e06ec in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:63
    #12 0x7f7d5ae28b75 in __asan::AsanThread::ThreadStart() ??:0
0x7f7d30ea5570 is located 240 bytes inside of 480-byte region [0x7f7d30ea5480,0x7f7d30ea5660)
freed by thread T90 here:
    #0 0x7f7d5ae23542 in operator delete(void*) ??:0
    #1 0x7f7d54679dfb in std::_Deque_base<base::PendingTask, std::allocator<base::PendingTask> >::_M_destroy_nodes(base::PendingTask**, base::PendingTask**) /usr/lib/gcc/x86_64-linux-gnu/4.4/../../../../include/c++/4.4/bits/stl_deque.h:553
    #2 0x7f7d54668ad4 in std::basic_string<char, std::char_traits<char>, std::allocator<char> >::_M_data() const /usr/lib/gcc/x86_64-linux-gnu/4.4/../../../../include/c++/4.4/bits/basic_string.h:272
    #3 0x7f7d546eaa38 in base::Thread::ThreadMain() base/threading/thread.cc:171
    #4 0x7f7d546e06ec in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:63
    #5 0x7f7d5ae28b75 in __asan::AsanThread::ThreadStart() ??:0
previously allocated by thread T90 here:
    #0 0x7f7d5ae233c2 in operator new(unsigned long) ??:0
    #1 0x7f7d5467a1f4 in std::_Deque_base<base::PendingTask, std::allocator<base::PendingTask> >::_M_create_nodes(base::PendingTask**, base::PendingTask**) /usr/lib/gcc/x86_64-linux-gnu/4.4/../../../../include/c++/4.4/bits/stl_deque.h:538
    #2 0x7f7d5467a59b in std::deque<base::PendingTask, std::allocator<base::PendingTask> >::size() const /usr/lib/gcc/x86_64-linux-gnu/4.4/../../../../include/c++/4.4/bits/stl_deque.h:379
    #3 0x7f7d54667456 in deque /usr/lib/gcc/x86_64-linux-gnu/4.4/../../../../include/c++/4.4/bits/stl_deque.h:790
    #4 0x7f7d546ea888 in base::Thread::ThreadMain() base/threading/thread.cc:147
    #5 0x7f7d546e06ec in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:63
    #6 0x7f7d5ae28b75 in __asan::AsanThread::ThreadStart() ??:0
Thread T91 created by T90 here:
    #0 0x7f7d5ae236c3 in pthread_create ??:0
    #1 0x7f7d546e0399 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, unsigned long*) base/threading/platform_thread_posix.cc:124
    #2 0x7f7d546e029a in base::PlatformThread::Create(unsigned long, base::PlatformThread::Delegate*, unsigned long*) base/threading/platform_thread_posix.cc:228
    #3 0x7f7d546ea295 in base::Thread::StartWithOptions(base::Thread::Options const&) base/threading/thread.cc:72
    #4 0x7f7d546ea03b in base::Thread::Start() base/threading/thread.cc:61
    #5 0x7f7d5a347276 in media::MessageLoopFactory::GetThread(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) media/base/message_loop_factory.cc:45
    #6 0x7f7d5a3470b9 in base::Thread::message_loop() const ./base/threading/thread.h:113
    #7 0x7f7d58c9496c in base::internal::RunnableAdapter<MessageLoop* (media::MessageLoopFactory::*)(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)>::Run(media::MessageLoopFactory*, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) ./base/bind_internal.h:188
    #8 0x7f7d5a381388 in base::Callback<MessageLoop* ()()>::Run() const ./base/callback.h:272
    #9 0x7f7d5a357e26 in ~Callback ./base/callback.h:282
    #10 0x7f7d5a353e03 in media::Pipeline::InitializeTask(media::PipelineStatus) media/base/pipeline.cc:690
    #11 0x7f7d5466f3c6 in base::Callback<void ()()>::Run() const ./base/callback.h:272
    #12 0x7f7d5466fc28 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) base/message_loop.cc:470
    #13 0x7f7d54670f19 in MessageLoop::DoWork() base/message_loop.cc:660
    #14 0x7f7d5467b437 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_pump_default.cc:28
    #15 0x7f7d5466df8e in MessageLoop::RunInternal() base/message_loop.cc:418
    #16 0x7f7d5466c17f in ~AutoRunState base/message_loop.cc:745
    #17 0x7f7d546ea9bc in base::Thread::ThreadMain() base/threading/thread.cc:161
    #18 0x7f7d546e06ec in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:63
    #19 0x7f7d5ae28b75 in __asan::AsanThread::ThreadStart() ??:0
Thread T90 created by T15 here:
    #0 0x7f7d5ae236c3 in pthread_create ??:0
    #1 0x7f7d546e0399 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, unsigned long*) base/threading/platform_thread_posix.cc:124
    #2 0x7f7d546e029a in base::PlatformThread::Create(unsigned long, base::PlatformThread::Delegate*, unsigned long*) base/threading/platform_thread_posix.cc:228
    #3 0x7f7d546ea295 in base::Thread::StartWithOptions(base::Thread::Options const&) base/threading/thread.cc:72
    #4 0x7f7d546ea03b in base::Thread::Start() base/threading/thread.cc:61
    #5 0x7f7d5a347276 in media::MessageLoopFactory::GetThread(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) media/base/message_loop_factory.cc:45
    #6 0x7f7d5a3470b9 in base::Thread::message_loop() const ./base/threading/thread.h:113
    #7 0x7f7d58c75067 in webkit_media::WebMediaPlayerImpl::WebMediaPlayerImpl(WebKit::WebFrame*, WebKit::WebMediaPlayerClient*, base::WeakPtr<webkit_media::WebMediaPlayerDelegate>, media::FilterCollection*, WebKit::WebAudioSourceProvider*, media::MessageLoopFactory*, webkit_media::MediaStreamClient*, media::MediaLog*) webkit/media/webmediaplayer_impl.cc:128
    #8 0x7f7d59a31904 in ~WeakPtr ./base/memory/weak_ptr.h:161
    #9 0x7f7d56148389 in createWebMediaPlayer third_party/WebKit/Source/WebKit/chromium/src/WebMediaPlayerClientImpl.cpp:63
    #10 0x7f7d56b0992a in WebCore::MediaPlayer::loadWithNextMediaEngine(WebCore::MediaPlayerFactory*) third_party/WebKit/Source/WebCore/platform/graphics/MediaPlayer.cpp:402
    #11 0x7f7d56b088c7 in WebCore::MediaPlayer::load(WebCore::KURL const&, WebCore::ContentType const&) third_party/WebKit/Source/WebCore/platform/graphics/MediaPlayer.cpp:360
    #12 0x7f7d567ed78c in WebCore::HTMLMediaElement::loadResource(WebCore::KURL const&, WebCore::ContentType&) third_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:936
    #13 0x7f7d567ec41e in ~RefPtr third_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:58
    #14 0x7f7d567da181 in WebCore::HTMLMediaElement::loadTimerFired(WebCore::Timer<WebCore::HTMLMediaElement>*) third_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:569
    #15 0x7f7d56a771f8 in WebCore::ThreadTimers::sharedTimerFiredInternal() third_party/WebKit/Source/WebCore/platform/ThreadTimers.cpp:118
    #16 0x7f7d5466f3c6 in base::Callback<void ()()>::Run() const ./base/callback.h:272
    #17 0x7f7d5466fc28 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) base/message_loop.cc:470
    #18 0x7f7d54670f19 in MessageLoop::DoWork() base/message_loop.cc:660
    #19 0x7f7d5467b437 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_pump_default.cc:28
    #20 0x7f7d5466df8e in MessageLoop::RunInternal() base/message_loop.cc:418
    #21 0x7f7d5466c17f in ~AutoRunState base/message_loop.cc:745
    #22 0x7f7d546ea9bc in base::Thread::ThreadMain() base/threading/thread.cc:161
    #23 0x7f7d546e06ec in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:63
    #24 0x7f7d5ae28b75 in __asan::AsanThread::ThreadStart() ??:0
==31060== ABORTING
Stats: 350M malloced (318M for red zones) by 515923 calls
Stats: 5M realloced by 19481 calls
Stats: 318M freed by 397427 calls
Stats: 168M really freed by 298567 calls
Stats: 544M (139362 full pages) mmaped in 134 calls
  mmaps   by size class: 8:360426; 9:24573; 10:24570; 11:10235; 12:4096; 13:7680; 14:1024; 15:256; 16:448; 17:256; 18:48; 19:184; 20:96; 21:4; 22:4; 23:2;
  mallocs by size class: 8:436312; 9:24415; 10:25659; 11:11623; 12:3613; 13:11624; 14:1132; 15:304; 16:481; 17:325; 18:70; 19:226; 20:129; 21:4; 22:4; 23:2;
  frees   by size class: 8:327995; 9:21391; 10:24325; 11:6866; 12:3080; 13:11426; 14:916; 15:272; 16:446; 17:310; 18:62; 19:203; 20:127; 21:3; 22:3; 23:2;
  rfrees  by size class: 8:250624; 9:15467; 10:18435; 11:4300; 12:2436; 13:5672; 14:765; 15:188; 16:382; 17:136; 18:30; 19:75; 20:49; 21:3; 22:3; 23:2;
Stats: malloc large: 760 small slow: 3042
Shadow byte and word:
  0x1fefa61d4aae: fd
  0x1fefa61d4aa8: fd fd fd fd fd fd fd fd
More shadow bytes:
  0x1fefa61d4a88: fa fa fa fa fa fa fa fa
  0x1fefa61d4a90: fd fd fd fd fd fd fd fd
  0x1fefa61d4a98: fd fd fd fd fd fd fd fd
  0x1fefa61d4aa0: fd fd fd fd fd fd fd fd
=>0x1fefa61d4aa8: fd fd fd fd fd fd fd fd
  0x1fefa61d4ab0: fd fd fd fd fd fd fd fd
  0x1fefa61d4ab8: fd fd fd fd fd fd fd fd
  0x1fefa61d4ac0: fd fd fd fd fd fd fd fd
  0x1fefa61d4ac8: fd fd fd fd fd fd fd fd
==31060== Sleeping for 1000 second(s)


### sc...@chromium.org (2012-03-26)

to clarify sync0.webm has no audio and the asan trace you posted looks to be a different issue

I'm guessing the crash w/ sync2.webm means it's audio-related

one more thing -- this is a regression and doesn't happen in m18? if so then we should be able to bisect

### in...@chromium.org (2012-03-27)

This did not hapoen in m18, reporter says he started noticing this just before 124615.

### sc...@chromium.org (2012-03-27)

assigning to imasaki to bisect

### im...@chromium.org (2012-03-27)

I will bisect the build manually using https://commondatastorage.googleapis.com/chromium-browser-asan/index.html

### im...@chromium.org (2012-03-28)

What I did today:

1) Tried to repro this issue with https://commondatastorage.googleapis.com/chromium-browser-asan/asan-symbolized-linux-release-129170.zip with orignal test case (test.html + out.ogv) -> Chrome crash with 

==10306== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7ffc35f0aa80 at pc 0x7ffc436d5664 bp 0x7ffc338b4b10 sp 0x7ffc338b4b08
READ of size 4 at 0x7ffc35f0aa80 thread T2

2) try to repro this issue with https://commondatastorage.googleapis.com/chromium-browser-asan/asan-symbolized-linux-release-129170.zip with simple example suggested in https://crbug.com/chromium/117341#c18 -> no success

3) modified bisect-build.py to use https://commondatastorage.googleapis.com/chromium-browser-asan/index.html and started bisecting - I used the 1) to determine good or bad build.

Result)
Got possible offending CL range
http://build.chromium.org/f/chromium/perf/dashboard/ui/changelog.html?url=/trunk/src&range=121858:121875

Webkit:
https://trac.webkit.org/log/?verbose=on&stop_rev=107621&rev=107663&limit=1000





### im...@chromium.org (2012-03-28)

[Comment Deleted]

### im...@chromium.org (2012-03-29)

Asking aarya@ to bisect build since I cannot repro the issue.


### fi...@chromium.org (2012-04-02)

[Empty comment from Monorail migration]

### kc...@chromium.org (2012-04-03)

timurrrr@, eugenis@, glider@, 
this bug looks funny. May I ask you to run tsan & memcheck on the repros? 
(I won't be able to do that for some time). 

### [Deleted User] (2012-04-03)

I've tried the repro from c#12 over ssh under Valgrind & TSan + xvfb-run on my workstation and got nothing interesting.

Unfortunately, I can't run it directly (with X, sound etc) nor can I run it over NX as I'm on a sick leave now.

### im...@chromium.org (2012-04-03)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-04-06)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=131094

------------------------------------------------------------------------
r131094 | fischman@chromium.org | Thu Apr 05 20:38:14 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/media/base/composite_filter.cc?r1=131094&r2=131093&pathrev=131094
 M http://src.chromium.org/viewvc/chrome/trunk/src/media/base/composite_filter_unittest.cc?r1=131094&r2=131093&pathrev=131094
 M http://src.chromium.org/viewvc/chrome/trunk/src/media/base/composite_filter.h?r1=131094&r2=131093&pathrev=131094
 M http://src.chromium.org/viewvc/chrome/trunk/src/media/base/message_loop_factory.cc?r1=131094&r2=131093&pathrev=131094
 M http://src.chromium.org/viewvc/chrome/trunk/src/media/base/pipeline.h?r1=131094&r2=131093&pathrev=131094
 M http://src.chromium.org/viewvc/chrome/trunk/src/media/base/pipeline.cc?r1=131094&r2=131093&pathrev=131094
 M http://src.chromium.org/viewvc/chrome/trunk/src/media/base/message_loop_factory.h?r1=131094&r2=131093&pathrev=131094

Pipeline & CompositeFilter now use MessageLoopProxy instead of plain MessageLoop.

This prevents a race between initialization and teardown, for example, where
Pipeline tries to use its message_loop_ when FFVD::Initialize() is completed (on
the decoder thread) but the pipeline thread's loop has already been freed.

Because I ran into it during this chase, also made MessageLoopFactory use a list instead of a map.  There are only 1-3 threads that the factory every knows about, and using a list allows destroying them in reverse order of creation, for at least a little more predictability.

BUG=117341


Review URL: http://codereview.chromium.org/10010031
------------------------------------------------------------------------

### fi...@chromium.org (2012-04-06)

r131094 above fixes the violation in https://crbug.com/chromium/117341#c23 above.
With that fix in, sync0.webm from https://crbug.com/chromium/117341#c21 does NOT trigger the crash, supporting the theory that the problem is in audio-specific code (sync0.webm has no audio).

Will continue looking.

### cl...@chromium.org (2012-04-06)

ClusterFuzz has detected this issue as fixed in range 131054:131098.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=29480667

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free WRITE 1
Crash Address: 0x7fa7d19725c0
Crash State:
  - crash stack -
  MessageLoop::AddToIncomingQueue
  MessageLoop::PostTask
  - free stack -
  std::deque<base::PendingTask, std::allocator<base::PendingTask> >::~deque
  MessageLoop::~MessageLoop
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=128281:128300
Fixed: https://cluster-fuzz.appspot.com/revisions?range=131054:131098

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97maeo6XtF_Vtvq6APcxIRIYc1y7uTQdUYzyML5_Dk7-KdIgABViScP3amhP7QlWkqWjHftXVnkk_kI9PtqztawKQ6FNki71gYDXswijtO2K13R5YfhY2N8nWiqGIABI1em2iYO_b3hTliggQu4GD3PKMauLA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2012-04-06)

Looks like r131094 indeed fixes it.

### al...@chromium.org (2012-04-06)

Tried on Ubuntu, gc: Version 20.0.1093.0 r131102 - I don't see sad face, but I see "He's dead, Jim!", out of memory caused by unresponsive message 

### fi...@chromium.org (2012-04-06)

This is not fixed - the SetDescriptors stack is still encountered with the originally reported .ogv file even at 131125.


### js...@chromium.org (2012-04-08)

Based on the original report date marking as impacting beta.

### fi...@chromium.org (2012-04-09)

Finally found the bug triggering the SetDescriptors stack; fix out for CR in https://chromiumcodereview.appspot.com/10019018/

### fi...@chromium.org (2012-04-09)

CR is marked private (b/c I don't know what the etiquette is for CRs fixing security bugs).  The key is that ipc/ipc_channel_posix.cc assumes &input_fds_.front() is a good way to get at a contiguous native array of fds, but input_fds_ is a deque, so doesn't guarantee that.  s/deque/vector/ makes the crash go away.

### fi...@chromium.org (2012-04-09)

FWIW, with the fix from 10019018 ASAN eventually crashes like this, but it takes a lot longer to trigger than the SetDescriptors crash did:

ASAN:SIGSEGV
==29180== ERROR: AddressSanitizer crashed on unknown address 0x000000000000 (pc 0x7f645e17d650 sp 0x7f64124f9a60 bp 0x7f64124f9cb0 T40365)
AddressSanitizer can not provide additional info. ABORTING

I'm assuming that's just an ASAN bug and not an indication of a bug in chromium.

### pa...@chromium.org (2012-04-09)

In case anyone besides me was wondering, changing deque to vector is guaranteed to work. Page 155 of The C++ Standard Library by Josuttis says:

"""The C++ standard library does not state clearly whether the elements of a vector are required to be in contiguous memory. However, it is the intention that this is guaranteed and it will be fixed due to to a defect report. Thus, you can expect that for any valid index i in vector v, the following yields true:

    &v[i] == &v[0] + i
"""

Thanks fischman!

### kc...@chromium.org (2012-04-09)

fischman@, wrt c#44: this is unlikely to be an asan bug.
More likely you are hitting some other chrome bug which is just a NULL deref and asan has not additional info. 

### fi...@chromium.org (2012-04-09)

@palmer: C++03 fixed the lack Josuttis notes; 23.2.4-1- says: The elements of a vector are stored contiguously, meaning that if v is a vector<T, Allocator> where T is some type other than bool, then it obeys the identity &v[n] == &v[0] + n for all 0 <= n < v.size().

### ao...@gmail.com (2012-04-09)

Any chance of getting the suggested patch here? I'd like to check if some likely related traces disappear with the file descriptor ones after applying it.

### fi...@chromium.org (2012-04-09)

aohelin: attached.

### bu...@chromium.org (2012-04-09)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=131443

------------------------------------------------------------------------
r131443 | fischman@chromium.org | Mon Apr 09 14:40:44 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/ipc/ipc_channel_posix.cc?r1=131443&r2=131442&pathrev=131443
 M http://src.chromium.org/viewvc/chrome/trunk/src/ipc/ipc_channel_posix.h?r1=131443&r2=131442&pathrev=131443

Prevent reading invalid memory in IPC code caused by assumption of contiguity in std::deque<>.

std::vector<int> guarantees contiguous storage (as of C++2003, 23.2.4p1,
although in practice this is true with all known STL implementations), but
std::deque<> typically uses linked chains of array blocks, so specifically
*doesn't* provide contiguity once its size grows above its basic block size
(usually 512bytes on our linux systems).

BUG=117341
TEST=test in bug stops reproducing with this.


Review URL: http://codereview.chromium.org/10019018
------------------------------------------------------------------------

### fi...@chromium.org (2012-04-09)

Requesting to merge both 131443 and 131094 to m19.

### in...@chromium.org (2012-04-09)

Security bugs have blanket approval. for m19, anytime is ok. if it was stable, then we do wait till merge window opens.

### in...@chromium.org (2012-04-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-04-09)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=131461

------------------------------------------------------------------------
r131461 | fischman@chromium.org | Mon Apr 09 15:36:04 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/1084/src/media/base/pipeline.h?r1=131461&r2=131460&pathrev=131461
 M http://src.chromium.org/viewvc/chrome/branches/1084/src/media/base/message_loop_factory.cc?r1=131461&r2=131460&pathrev=131461
 M http://src.chromium.org/viewvc/chrome/branches/1084/src/media/base/message_loop_factory.h?r1=131461&r2=131460&pathrev=131461
 M http://src.chromium.org/viewvc/chrome/branches/1084/src/media/base/pipeline.cc?r1=131461&r2=131460&pathrev=131461
 M http://src.chromium.org/viewvc/chrome/branches/1084/src/media/base/composite_filter.cc?r1=131461&r2=131460&pathrev=131461
 M http://src.chromium.org/viewvc/chrome/branches/1084/src/media/base/composite_filter_unittest.cc?r1=131461&r2=131460&pathrev=131461
 M http://src.chromium.org/viewvc/chrome/branches/1084/src/media/base/composite_filter.h?r1=131461&r2=131460&pathrev=131461

Merge 131094 - Pipeline & CompositeFilter now use MessageLoopProxy instead of plain MessageLoop.

This prevents a race between initialization and teardown, for example, where
Pipeline tries to use its message_loop_ when FFVD::Initialize() is completed (on
the decoder thread) but the pipeline thread's loop has already been freed.

Because I ran into it during this chase, also made MessageLoopFactory use a list instead of a map.  There are only 1-3 threads that the factory every knows about, and using a list allows destroying them in reverse order of creation, for at least a little more predictability.

BUG=117341


Review URL: http://codereview.chromium.org/10010031

TBR=fischman@chromium.org
Review URL: https://chromiumcodereview.appspot.com/10024038
------------------------------------------------------------------------

### bu...@chromium.org (2012-04-09)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=131462

------------------------------------------------------------------------
r131462 | fischman@chromium.org | Mon Apr 09 15:36:37 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/1084/src/ipc/ipc_channel_posix.cc?r1=131462&r2=131461&pathrev=131462
 M http://src.chromium.org/viewvc/chrome/branches/1084/src/ipc/ipc_channel_posix.h?r1=131462&r2=131461&pathrev=131462

Merge 131443 - Prevent reading invalid memory in IPC code caused by assumption of contiguity in std::deque<>.

std::vector<int> guarantees contiguous storage (as of C++2003, 23.2.4p1,
although in practice this is true with all known STL implementations), but
std::deque<> typically uses linked chains of array blocks, so specifically
*doesn't* provide contiguity once its size grows above its basic block size
(usually 512bytes on our linux systems).

BUG=117341
TEST=test in bug stops reproducing with this.


Review URL: http://codereview.chromium.org/10019018

TBR=fischman@chromium.org
Review URL: https://chromiumcodereview.appspot.com/9999008
------------------------------------------------------------------------

### ao...@gmail.com (2012-04-10)

@fischman: Thanks. I stopped seeing the remaining filedescriptor issues after the patch, and the remaining other ones don't seem to be related to this issue.

### sc...@gmail.com (2012-04-24)

@fischman: thanks for merging for us!

### in...@chromium.org (2012-04-24)

Great job Chamal in hunting this regression in media pipeline. This qualifies for the $1000 Chromium Security Reward.

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### ch...@gmail.com (2012-04-25)

Thank you very much for the reward :)

### sc...@gmail.com (2012-05-10)

Payment in system.

### [Deleted User] (2012-05-15)

Updating status to Fixed on security bugs which were fixed when m19 went to stable.

### al...@chromium.org (2012-05-16)

[Comment Deleted]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

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

This issue was migrated from crbug.com/chromium/117341?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Media, Internals>Media>Video]
[Monorail mergedwith: crbug.com/chromium/119788, crbug.com/chromium/121131]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054646)*
