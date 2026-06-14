# Security: UAF/Crash in (websockets) onsentdata/reset with web and shared workers combined

| Field | Value |
|-------|-------|
| **Issue ID** | [40079227](https://issues.chromium.org/issues/40079227) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Network>WebSockets, Blink>Workers |
| **Reporter** | th...@gmail.com |
| **Assignee** | ri...@chromium.org |
| **Created** | 2014-03-30 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The repro script causes a browser crash/UAF because shared and web worker (combined) cause Chrome to access already freed websocket related objects after the window/tab has been closed (automatically).

**VERSION**  

Chrome Version: 33.0.1750.152 stable - 35.0.1916.0 (260135) ToT  

Operating System: Ubuntu 13.10 x64

**REPRODUCTION CASE**

1. Start Chrome with at least 2 tabs (one will also do, but the script will then close the browser)
2. Run the repro script in one of them

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see added asan trace

## Attachments

- [websockets_onsentdata_uaf_asan_trace.txt](attachments/websockets_onsentdata_uaf_asan_trace.txt) (text/plain, 12.5 KB)
- [websockets_onsentdata_uaf_repro.html](attachments/websockets_onsentdata_uaf_repro.html) (text/html, 975 B)
- [websocket_worker_repro.html](attachments/websocket_worker_repro.html) (text/html, 1.4 KB)

## Timeline

### cl...@chromium.org (2014-03-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-30)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5181488169484288

### jw...@chromium.org (2014-03-31)

[Empty comment from Monorail migration]

### ri...@chromium.org (2014-03-31)

Thank you for the report. I got a renderer-side crash on tip-of-tree:

==103==ERROR: AddressSanitizer: heap-use-after-free on address 0x603004193710 at pc 0x7f830b83cbab bp 0x7fff6b5be320 sp 0x7fff6b5be318
READ of size 4 at 0x603004193710 thread T0 (chrome)
    #0 0x7f830b83cbaa in ~String /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/wtf/text/StringImpl.h:275
    #1 0x7f830b818b6a in deletePtr /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/wtf/OwnPtrCommon.h:52
    #2 0x7f830b818f8d in ~MainThreadWebSocketChannel /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/modules/websockets/MainThreadWebSocketChannel.cpp:88
    #3 0x7f830b81f7a5 in deref /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/wtf/RefCounted.h:181
    #4 0x7f830e5655e2 in DidClose /usr/local/google/home/ricea/src/out/Release/../../content/child/web_socket_stream_handle_impl.cc:151
    #5 0x7f830e56028a in OnClosed /usr/local/google/home/ricea/src/out/Release/../../content/child/socket_stream_dispatcher.cc:160
    #6 0x7f830e561091 in OnClosed /usr/local/google/home/ricea/src/out/Release/../../content/child/socket_stream_dispatcher.cc:240
    #7 0x7f830e4e945d in OnMessageReceived /usr/local/google/home/ricea/src/out/Release/../../content/child/child_thread.cc:420
    #8 0x7f830f4244bf in OnMessageReceived /usr/local/google/home/ricea/src/out/Release/../../content/worker/worker_thread.cc:113
    #9 0x7f83065555cf in OnDispatchMessage /usr/local/google/home/ricea/src/out/Release/../../ipc/ipc_channel_proxy.cc:375
    #10 0x7f830593de29 in Run /usr/local/google/home/ricea/src/out/Release/../../base/callback.h:401
    #11 0x7f8305940414 in DeferOrRunPendingTask /usr/local/google/home/ricea/src/out/Release/../../base/message_loop/message_loop.cc:461
    #12 0x7f83059479c1 in Run /usr/local/google/home/ricea/src/out/Release/../../base/message_loop/message_pump_default.cc:32
    #13 0x7f830597e8c7 in Run /usr/local/google/home/ricea/src/out/Release/../../base/run_loop.cc:49
    #14 0x7f830593bfa4 in Run /usr/local/google/home/ricea/src/out/Release/../../base/message_loop/message_loop.cc:292
    #15 0x7f830f422b4d in WorkerMain /usr/local/google/home/ricea/src/out/Release/../../content/worker/worker_main.cc:69
    #16 0x7f83058a4fac in RunZygote /usr/local/google/home/ricea/src/out/Release/../../content/app/content_main_runner.cc:395
    #17 0x7f83058a7590 in Run /usr/local/google/home/ricea/src/out/Release/../../content/app/content_main_runner.cc:797
    #18 0x7f83058a47bf in ContentMain /usr/local/google/home/ricea/src/out/Release/../../content/app/content_main.cc:19
    #19 0x7f83045656a1 in ChromeMain /usr/local/google/home/ricea/src/out/Release/../../chrome/app/chrome_main.cc:46
    #20 0x7f82fae6876c in __libc_start_main /build/buildd/eglibc-2.15/csu/libc-start.c:226
    #21 0x7f83045653fc in _start ??:0

0x603004193710 is located 0 bytes inside of 27-byte region [0x603004193710,0x60300419372b)
freed by thread T0 (chrome) here:
    #0 0x7f830454aa61 in __interceptor_free _asan_rtl_
    #1 0x7f8310207724 in deref /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/wtf/text/StringImpl.h:286
    #2 0x7f831020789d in ~SocketStreamHandle /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/platform/network/SocketStreamHandle.cpp:176
    #3 0x7f830b81f62e in deref /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/wtf/RefCounted.h:181
    #4 0x7f830e5655e2 in DidClose /usr/local/google/home/ricea/src/out/Release/../../content/child/web_socket_stream_handle_impl.cc:151
    #5 0x7f830e56028a in OnClosed /usr/local/google/home/ricea/src/out/Release/../../content/child/socket_stream_dispatcher.cc:160
    #6 0x7f830e561091 in OnClosed /usr/local/google/home/ricea/src/out/Release/../../content/child/socket_stream_dispatcher.cc:240
    #7 0x7f830e4e945d in OnMessageReceived /usr/local/google/home/ricea/src/out/Release/../../content/child/child_thread.cc:420
    #8 0x7f830f4244bf in OnMessageReceived /usr/local/google/home/ricea/src/out/Release/../../content/worker/worker_thread.cc:113
    #9 0x7f83065555cf in OnDispatchMessage /usr/local/google/home/ricea/src/out/Release/../../ipc/ipc_channel_proxy.cc:375
    #10 0x7f830593de29 in Run /usr/local/google/home/ricea/src/out/Release/../../base/callback.h:401
    #11 0x7f8305940414 in DeferOrRunPendingTask /usr/local/google/home/ricea/src/out/Release/../../base/message_loop/message_loop.cc:461
    #12 0x7f83059479c1 in Run /usr/local/google/home/ricea/src/out/Release/../../base/message_loop/message_pump_default.cc:32
    #13 0x7f830597e8c7 in Run /usr/local/google/home/ricea/src/out/Release/../../base/run_loop.cc:49
    #14 0x7f830593bfa4 in Run /usr/local/google/home/ricea/src/out/Release/../../base/message_loop/message_loop.cc:292
    #15 0x7f830f422b4d in WorkerMain /usr/local/google/home/ricea/src/out/Release/../../content/worker/worker_main.cc:69
    #16 0x7f83058a4fac in RunZygote /usr/local/google/home/ricea/src/out/Release/../../content/app/content_main_runner.cc:395
    #17 0x7f83058a7590 in Run /usr/local/google/home/ricea/src/out/Release/../../content/app/content_main_runner.cc:797
    #18 0x7f83058a47bf in ContentMain /usr/local/google/home/ricea/src/out/Release/../../content/app/content_main.cc:19
    #19 0x7f83045656a1 in ChromeMain /usr/local/google/home/ricea/src/out/Release/../../chrome/app/chrome_main.cc:46
    #20 0x7f82fae6876c in __libc_start_main /build/buildd/eglibc-2.15/csu/libc-start.c:226

previously allocated by thread T10 here:
    #0 0x7f830454ac81 in __interceptor_malloc _asan_rtl_
    #1 0x7f8307887746 in partitionAllocGenericFlags /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/wtf/PartitionAlloc.h:533
    #2 0x7f83078b3dc6 in isolatedCopy /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/wtf/text/StringImpl.h:721
    #3 0x7f83076e643d in copy /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/platform/weborigin/KURL.cpp:261
    #4 0x7f830b7d4d54 in connect /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/modules/websockets/WorkerThreadableWebSocketChannel.cpp:478
    #5 0x7f830b7c86fd in connect /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/modules/websockets/WebSocket.cpp:363
    #6 0x7f830b7c5be2 in create /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/modules/websockets/WebSocket.cpp:261
    #7 0x7f830b7c573f in create /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/modules/websockets/WebSocket.cpp:248
    #8 0x7f830aaaaed3 in constructor1 /usr/local/google/home/ricea/src/out/Release/gen/blink/bindings/V8WebSocket.cpp:420
    #9 0x7f83084783b0 in Call /usr/local/google/home/ricea/src/out/Release/../../v8/src/arguments.cc:56
    #10 0x7f8307a37cf4 in HandleApiCallHelper<true> /usr/local/google/home/ricea/src/out/Release/../../v8/src/builtins.cc:1212
    #11 0x7f8307b2a561 in Invoke /usr/local/google/home/ricea/src/out/Release/../../v8/src/execution.cc:126
    #12 0x7f83079b89eb in Call /usr/local/google/home/ricea/src/out/Release/../../v8/src/api.cc:4012
    #13 0x7f830b198b90 in callFunction /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/bindings/v8/V8ScriptRunner.cpp:140
    #14 0x7f830b1a6335 in callListenerFunction /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/bindings/v8/V8WorkerGlobalScopeEventListener.cpp:104
    #15 0x7f830b507286 in invokeEventHandler /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/bindings/v8/V8AbstractEventListener.cpp:126
    #16 0x7f830b1a5a16 in handleEvent /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/bindings/v8/V8WorkerGlobalScopeEventListener.cpp:78
    #17 0x7f83088ecdbc in fireEventListeners /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/core/events/EventTarget.cpp:332
    #18 0x7f83088ebdb1 in fireEventListeners /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/core/events/EventTarget.cpp:274
    #19 0x7f83088eb909 in dispatchEvent /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/core/events/EventTarget.cpp:182
    #20 0x7f8310314bfe in connectTask /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/web/WebSharedWorkerImpl.cpp:314
    #21 0x7f8310317811 in performTask /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/core/dom/CrossThreadTask.h:81
    #22 0x7f83099437b4 in run /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/core/workers/WorkerRunLoop.cpp:223
    #23 0x7f83099430a8 in run /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/core/workers/WorkerRunLoop.cpp:164
    #24 0x7f8309946e7b in workerThread /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/core/workers/WorkerThread.cpp:134

Thread T10 created by T0 (chrome) here:
    #0 0x7f8304536e45 in __interceptor_pthread_create _asan_rtl_
    #1 0x7f830786437f in createThreadInternal /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/wtf/ThreadingPthreads.cpp:183
    #2 0x7f831025d226 in createThread /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/wtf/Threading.cpp:86
    #3 0x7f83099465d4 in start /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/core/workers/WorkerThread.cpp:95
    #4 0x7f8310312995 in onScriptLoaderFinished /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/web/WebSharedWorkerImpl.cpp:362
    #5 0x7f8309d169d9 in notifyFinished /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/core/workers/WorkerScriptLoader.cpp:188
    #6 0x7f8309597903 in checkNotify /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/core/fetch/Resource.cpp:199
    #7 0x7f8309598cdc in finish /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/core/fetch/Resource.cpp:259
    #8 0x7f83095c7fbe in didFinishLoading /usr/local/google/home/ricea/src/out/Release/../../third_party/WebKit/Source/core/fetch/ResourceLoader.cpp:407
    #9 0x7f830e56e265 in OnCompletedRequest /usr/local/google/home/ricea/src/out/Release/../../content/child/web_url_loader_impl.cc:632
    #10 0x7f830e54b522 in OnRequestComplete /usr/local/google/home/ricea/src/out/Release/../../content/child/resource_dispatcher.cc:557
    #11 0x7f830e546fdb in DispatchToMethod<content::ResourceDispatcher, void (content::ResourceDispatcher::*)(int, const ResourceMsg_RequestCompleteData &), int, ResourceMsg_RequestCompleteData> /usr/local/google/home/ricea/src/out/Release/../../base/tuple.h:555
    #12 0x7f830e544b25 in OnMessageReceived /usr/local/google/home/ricea/src/out/Release/../../content/child/resource_dispatcher.cc:322
    #13 0x7f830e4e9403 in OnMessageReceived /usr/local/google/home/ricea/src/out/Release/../../content/child/child_thread.cc:418
    #14 0x7f830f4244bf in OnMessageReceived /usr/local/google/home/ricea/src/out/Release/../../content/worker/worker_thread.cc:113
    #15 0x7f83065555cf in OnDispatchMessage /usr/local/google/home/ricea/src/out/Release/../../ipc/ipc_channel_proxy.cc:375
    #16 0x7f830593de29 in Run /usr/local/google/home/ricea/src/out/Release/../../base/callback.h:401
    #17 0x7f8305940414 in DeferOrRunPendingTask /usr/local/google/home/ricea/src/out/Release/../../base/message_loop/message_loop.cc:461
    #18 0x7f83059479c1 in Run /usr/local/google/home/ricea/src/out/Release/../../base/message_loop/message_pump_default.cc:32
    #19 0x7f830597e8c7 in Run /usr/local/google/home/ricea/src/out/Release/../../base/run_loop.cc:49
    #20 0x7f830593bfa4 in Run /usr/local/google/home/ricea/src/out/Release/../../base/message_loop/message_loop.cc:292
    #21 0x7f830f422b4d in WorkerMain /usr/local/google/home/ricea/src/out/Release/../../content/worker/worker_main.cc:69
    #22 0x7f83058a4fac in RunZygote /usr/local/google/home/ricea/src/out/Release/../../content/app/content_main_runner.cc:395
    #23 0x7f83058a7590 in Run /usr/local/google/home/ricea/src/out/Release/../../content/app/content_main_runner.cc:797
    #24 0x7f83058a47bf in ContentMain /usr/local/google/home/ricea/src/out/Release/../../content/app/content_main.cc:19
    #25 0x7f83045656a1 in ChromeMain /usr/local/google/home/ricea/src/out/Release/../../chrome/app/chrome_main.cc:46
    #26 0x7f82fae6876c in __libc_start_main /build/buildd/eglibc-2.15/csu/libc-start.c:226

SUMMARY: AddressSanitizer: heap-use-after-free ??:0 ??
Shadow bytes around the buggy address:
  0x0c068082a690: fd fd fa fa fd fd fd fd fa fa fd fd fd fa fa fa
  0x0c068082a6a0: fd fd fd fa fa fa fd fd fd fd fa fa fd fd fd fd
  0x0c068082a6b0: fa fa 00 00 00 fa fa fa fd fd fd fa fa fa fd fd
  0x0c068082a6c0: fd fd fa fa fd fd fd fd fa fa 00 00 00 fa fa fa
  0x0c068082a6d0: fd fd fd fd fa fa 00 00 00 fa fa fa fd fd fd fa
=>0x0c068082a6e0: fa fa[fd]fd fd fd fa fa fd fd fd fd fa fa fd fd
  0x0c068082a6f0: fd fa fa fa 00 00 00 fa fa fa fd fd fd fa fa fa
  0x0c068082a700: fd fd fd fd fa fa fd fd fd fd fa fa 00 00 00 fa
  0x0c068082a710: fa fa fd fd fd fd fa fa fd fd fd fd fa fa fd fd
  0x0c068082a720: fd fa fa fa 00 00 00 03 fa fa fd fd fd fd fa fa
  0x0c068082a730: fd fd fd fa fa fa 00 00 00 fa fa fa fd fd fd fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Heap right redzone:      fb
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack partial redzone:   f4
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Contiguous container OOB:fc
  ASan internal:           fe
ASAN:SIGSEGV
==103==AddressSanitizer: while reporting a bug found another one.Ignoring.


 It looks like clusterfuzz also only found a renderer-side crash. Still looking.

### in...@chromium.org (2014-03-31)

Just a fyi, cf won't have created the stuff in two tabs, etc instructions. so best to handle this case manually.

### ri...@chromium.org (2014-03-31)

I found the browser bug. I can't reproduce it, so I can't fix it yet, but I found it. At websocket_job.cc:427, WebSocketJob::OnSentHandshakeRequest() calls delegate_->OnSendData(). This calls DeleteSocketStreamHost, which removes the final reference from the WebSocketJob object, deleting it.

On line 430, WebSocketJob calls handshake_request_.reset(), accessing one of its own deleted members.

The code is confusing because DeleteSocketStreamHost explicitly prevents SocketStream from calling into WebSocketJob, but at the point at which it runs, WebSocketJob is already on the callstack so the protection is ineffective.

### ri...@chromium.org (2014-03-31)

I've created a unit test which can reproduce the stack trace that therealholden reported. I will have a fix tomorrow.

I still haven't managed to reproduce the crash organically using the supplied test case. The precise timing of the render crash is critical to trigger the browser crash.

### jw...@chromium.org (2014-03-31)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-31)

[Empty comment from Monorail migration]

### ri...@chromium.org (2014-04-03)

Just to update on current status, the fix is currently under review at http://crrev.com/221833002

### ri...@chromium.org (2014-04-03)

I have created a fairly reliable reproduction case. The set-up is a little bit cumbersome, because it requires an HTTP server to be running on 127.0.0.1 on all ports in the range 50000 to 60000. On Linux this can be accomplished by running an HTTP server on port 80 and then using NAT like this:

sudo iptables -t nat -A OUTPUT -p tcp -d 127.0.0.0/8 --match multiport --dports 50000:60000 -j REDIRECT --to-port 80

You need a browser compiled with ASAN to detect the UAF. I've never seen the UAF the first time on a freshly started browser: when it fails to reproduce, you just get a sad tab. Reloading 2 or 3 times always seems to be sufficient to reproduce the UAF.

### bu...@chromium.org (2014-04-04)

------------------------------------------------------------------
r261707 | ricea@chromium.org | 2014-04-04T08:30:55.023436Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/websockets/websocket_job_test.cc?r1=261707&r2=261706&pathrev=261707
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/websockets/websocket_job.cc?r1=261707&r2=261706&pathrev=261707

Test for WebSocketJob being deleted on the stack

SocketStreamDispatcherHost can delete the WebSocketJob while it is still
on the stack. Add tests to ensure that WebSocketJob does not attempt to
access its own members after being deleted.

Also fix two cases where WebSocketJob attempted to access its members after
being deleted.

BUG=358038
TEST=net_unittests --gtest_filter=WebSocketJobDeleteTest*

Review URL: https://codereview.chromium.org/221833002
-----------------------------------------------------------------

### in...@chromium.org (2014-04-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-04-04)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ri...@chromium.org (2014-04-11)

+therealholden The fix is now available on the dev channel (version 36.0.1933.0). Can you verify the fix?

Please verify with the "Experimental Web Platform features" flag disabled. If that flag is enabled, you get the new WebSocket implementation, which shares very little code with the stable one.

### th...@gmail.com (2014-04-11)

Fix verified, I can't repro the crash/UAF anymore starting with (ToT) v36.0.1928.0 (261961).


### mb...@chromium.org (2014-04-11)

[Empty comment from Monorail migration]

### ri...@chromium.org (2014-04-15)

[Empty comment from Monorail migration]

### ka...@google.com (2014-04-15)

approved for m35. 1916 branch.

### bu...@chromium.org (2014-04-16)

------------------------------------------------------------------
r264050 | ricea@chromium.org | 2014-04-16T01:04:30.866142Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1916/src/net/websockets/websocket_job_test.cc?r1=264050&r2=264049&pathrev=264050
   M http://src.chromium.org/viewvc/chrome/branches/1916/src/net/websockets/websocket_job.cc?r1=264050&r2=264049&pathrev=264050

Merge 261707 "Test for WebSocketJob being deleted on the stack"

> Test for WebSocketJob being deleted on the stack
> 
> SocketStreamDispatcherHost can delete the WebSocketJob while it is still
> on the stack. Add tests to ensure that WebSocketJob does not attempt to
> access its own members after being deleted.
> 
> Also fix two cases where WebSocketJob attempted to access its members after
> being deleted.
> 
> BUG=358038
> TEST=net_unittests --gtest_filter=WebSocketJobDeleteTest*
> 
> Review URL: https://codereview.chromium.org/221833002

TBR=tyoshino@chromium.org

Review URL: https://codereview.chromium.org/235953018
-----------------------------------------------------------------

### ti...@chromium.org (2014-04-22)

If there is another patch to M34/stable, this should be a candidate for submission.

### in...@chromium.org (2014-04-25)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-04-25)

Merge requested for m34 patch 2.

### bu...@chromium.org (2014-04-25)

------------------------------------------------------------------
r266137 | ricea@chromium.org | 2014-04-25T05:43:08.986587Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/net/websockets/websocket_job_test.cc?r1=266137&r2=266136&pathrev=266137
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/net/websockets/websocket_job.cc?r1=266137&r2=266136&pathrev=266137

Merge 261707 "Test for WebSocketJob being deleted on the stack"

> Test for WebSocketJob being deleted on the stack
> 
> SocketStreamDispatcherHost can delete the WebSocketJob while it is still
> on the stack. Add tests to ensure that WebSocketJob does not attempt to
> access its own members after being deleted.
> 
> Also fix two cases where WebSocketJob attempted to access its members after
> being deleted.
> 
> BUG=358038
> TEST=net_unittests --gtest_filter=WebSocketJobDeleteTest*
> 
> Review URL: https://codereview.chromium.org/221833002

TBR=tyoshino@chromium.org

Review URL: https://codereview.chromium.org/255813002
-----------------------------------------------------------------

### bu...@chromium.org (2014-04-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/52be733392b0c17b3cd46f5a4f93847a0390208d

commit 52be733392b0c17b3cd46f5a4f93847a0390208d
Author: ricea@chromium.org <ricea@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Fri Apr 25 05:43:08 2014 +0000

Merge 261707 "Test for WebSocketJob being deleted on the stack"

> Test for WebSocketJob being deleted on the stack
> 
> SocketStreamDispatcherHost can delete the WebSocketJob while it is still
> on the stack. Add tests to ensure that WebSocketJob does not attempt to
> access its own members after being deleted.
> 
> Also fix two cases where WebSocketJob attempted to access its members after
> being deleted.
> 
> BUG=358038
> TEST=net_unittests --gtest_filter=WebSocketJobDeleteTest*
> 
> Review URL: https://codereview.chromium.org/221833002

TBR=tyoshino@chromium.org

Review URL: https://codereview.chromium.org/255813002

git-svn-id: svn://svn.chromium.org/chrome/branches/1847/src@266137 0039d316-1c4b-4281-b951-d872f2087c98



### ri...@chromium.org (2014-04-25)

Oops, I should have waited for Merge-Approved. Sorry.

### bu...@chromium.org (2014-04-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4dc0eb2319ab5177f82d7d627610fbec098cf203

commit 4dc0eb2319ab5177f82d7d627610fbec098cf203
Author: ricea@chromium.org <ricea@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Fri Apr 25 06:30:53 2014 +0000

Revert 266137 "Merge 261707 "Test for WebSocketJob being deleted..."

Reason for revert: the test for the fix uses methods which did not exist in M34,
and so broken the build.

> Merge 261707 "Test for WebSocketJob being deleted on the stack"
> 
> > Test for WebSocketJob being deleted on the stack
> > 
> > SocketStreamDispatcherHost can delete the WebSocketJob while it is still
> > on the stack. Add tests to ensure that WebSocketJob does not attempt to
> > access its own members after being deleted.
> > 
> > Also fix two cases where WebSocketJob attempted to access its members after
> > being deleted.
> > 
> > BUG=358038
> > TEST=net_unittests --gtest_filter=WebSocketJobDeleteTest*
> > 
> > Review URL: https://codereview.chromium.org/221833002
> 
> TBR=tyoshino@chromium.org
> 
> Review URL: https://codereview.chromium.org/255813002

TBR=tyoshino

Review URL: https://codereview.chromium.org/257773004

git-svn-id: svn://svn.chromium.org/chrome/branches/1847/src@266144 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-04-25)

------------------------------------------------------------------
r266144 | ricea@chromium.org | 2014-04-25T06:30:53.900988Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/net/websockets/websocket_job_test.cc?r1=266144&r2=266143&pathrev=266144
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/net/websockets/websocket_job.cc?r1=266144&r2=266143&pathrev=266144

Revert 266137 "Merge 261707 "Test for WebSocketJob being deleted..."

Reason for revert: the test for the fix uses methods which did not exist in M34,
and so broken the build.

> Merge 261707 "Test for WebSocketJob being deleted on the stack"
> 
> > Test for WebSocketJob being deleted on the stack
> > 
> > SocketStreamDispatcherHost can delete the WebSocketJob while it is still
> > on the stack. Add tests to ensure that WebSocketJob does not attempt to
> > access its own members after being deleted.
> > 
> > Also fix two cases where WebSocketJob attempted to access its members after
> > being deleted.
> > 
> > BUG=358038
> > TEST=net_unittests --gtest_filter=WebSocketJobDeleteTest*
> > 
> > Review URL: https://codereview.chromium.org/221833002
> 
> TBR=tyoshino@chromium.org
> 
> Review URL: https://codereview.chromium.org/255813002

TBR=tyoshino

Review URL: https://codereview.chromium.org/257773004
-----------------------------------------------------------------

### ri...@chromium.org (2014-04-25)

The tests from this CL break the build on M34. Assuming we get Merge-Approved, I will land just the fix, without the tests.

### ti...@chromium.org (2014-04-25)

dxie@ - can you merge-approve this for M34? 

### ti...@chromium.org (2014-04-28)

ping dxie@ - merge requested for M34 patch 2.

### ti...@chromium.org (2014-04-30)

On second thought, no need to patch to M34 (see c#28).

### ri...@chromium.org (2014-05-01)

To clarify, M34 is vulnerable. It is just the methods I used in the unit test which tests for the vulnerability which aren't available in M34.

### dx...@google.com (2014-05-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-05-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0f3f1ff9be2a58fdf817566aa05067018e784e40

commit 0f3f1ff9be2a58fdf817566aa05067018e784e40
Author: ricea@chromium.org <ricea@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Sat May 03 07:54:59 2014 +0000

Merge 261707 "Test for WebSocketJob being deleted on the stack"

> Test for WebSocketJob being deleted on the stack
> 
> SocketStreamDispatcherHost can delete the WebSocketJob while it is still
> on the stack. Add tests to ensure that WebSocketJob does not attempt to
> access its own members after being deleted.
> 
> Also fix two cases where WebSocketJob attempted to access its members after
> being deleted.
> 
> BUG=358038
> TEST=net_unittests --gtest_filter=WebSocketJobDeleteTest*
> 
> Review URL: https://codereview.chromium.org/221833002

TBR=tyoshino@chromium.org

Review URL: https://codereview.chromium.org/264743015

git-svn-id: svn://svn.chromium.org/chrome/branches/1847/src@268057 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-05-05)

------------------------------------------------------------------
r268057 | ricea@chromium.org | 2014-05-03T07:54:59.767557Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/net/websockets/websocket_job.cc?r1=268057&r2=268056&pathrev=268057

Merge 261707 "Test for WebSocketJob being deleted on the stack"

> Test for WebSocketJob being deleted on the stack
> 
> SocketStreamDispatcherHost can delete the WebSocketJob while it is still
> on the stack. Add tests to ensure that WebSocketJob does not attempt to
> access its own members after being deleted.
> 
> Also fix two cases where WebSocketJob attempted to access its members after
> being deleted.
> 
> BUG=358038
> TEST=net_unittests --gtest_filter=WebSocketJobDeleteTest*
> 
> Review URL: https://codereview.chromium.org/221833002

TBR=tyoshino@chromium.org

Review URL: https://codereview.chromium.org/264743015
-----------------------------------------------------------------

### ti...@chromium.org (2014-05-12)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-05-13)

Congrats - $2000 for this one.

### th...@gmail.com (2014-05-13)

Thanks!

### cl...@chromium.org (2014-07-11)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-09-06)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you. Thanks again for your help!

### tk...@chromium.org (2015-11-26)

[Empty comment from Monorail migration]

### tk...@chromium.org (2015-11-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

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

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/358038?no_tracker_redirect=1

[Multiple monorail components: Blink>Network>WebSockets, Blink>Workers]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079227)*
