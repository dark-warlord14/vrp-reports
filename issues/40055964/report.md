# Heap-use-after-free in WebCore::WorkerThreadableWebSocketChannel::Bridge::mainThreadCreateWebSocketChannel

| Field | Value |
|-------|-------|
| **Issue ID** | [40055964](https://issues.chromium.org/issues/40055964) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | ax...@gmail.com |
| **Assignee** | yu...@chromium.org |
| **Created** | 2012-03-30 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Heap-use-after-free can be triggered while reloading document with working WebSockets.

**VERSION**  

Version 19.0.1079.0 (128665), Ubuntu 10.10 x64.

**REPRODUCTION CASE**  

Repro is in attachment, flaky again. It looks like a race condition, not sure how to make it more stable. First crash may occur at address 0x000000000018.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

==6163== ERROR: AddressSanitizer heap-use-after-free on address 0x7f2c15f89598 at pc 0x7f2c2eb6e578 bp 0x7fffcb421d50 sp 0x7fffcb421d48  

READ of size 8 at 0x7f2c15f89598 thread T0  

#0 0x7f2c2eb6e578 in ~PassRefPtr /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WTF/wtf/PassRefPtr.h:67  

#1 0x7f2c2eb71a32 in ~PassRefPtr /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WTF/wtf/PassRefPtr.h:67  

#2 0x7f2c2dd53aed in WebCore::Document::didReceiveTask(void\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Document.cpp:4925  

#3 0x7f2c2c5350bb in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (\*)(void\*)>, void ()(void\* const&)>::MakeItSo(base::internal::RunnableAdapter<void (\*)(void\*)>, void\* const&) /media/Chromium/chromium/depot\_tools/src/./base/bind\_internal.h:869  

#4 0x7f2c2c581823 in MessageLoop::RunTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:459  

#5 0x7f2c2c582014 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:470  

#6 0x7f2c2c5823ce in MessageLoop::DoWork() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:660  

#7 0x7f2c2c58e7de in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /media/Chromium/chromium/depot\_tools/src/base/message\_pump\_default.cc:28  

#8 0x7f2c2c58103e in MessageLoop::RunInternal() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:418  

#9 0x7f2c2c57fd18 in MessageLoop::Run() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:301  

#10 0x7f2c3066303c in RendererMain(content::MainFunctionParams const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/renderer\_main.cc:241  

#11 0x7f2c2c4b1684 in (anonymous namespace)::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main\_runner.cc:245  

#12 0x7f2c2c4b11cd in (anonymous namespace)::RunNamedProcessTypeMain(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main\_runner.cc:290  

#13 0x7f2c2c4b0b6c in (anonymous namespace)::ContentMainRunnerImpl::Run() /media/Chromium/chromium/depot\_tools/src/content/app/content\_main\_runner.cc:511  

#14 0x7f2c2c4affef in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:35  

#15 0x7f2c2b2937c7 in ChromeMain /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_main.cc:32  

#16 0x7f2c2b29371b in main /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#17 0x7f2c24197d8e in \_\_libc\_start\_main /build/buildd/eglibc-2.12.1/csu/libc-start.c:258  

0x7f2c15f89598 is located 24 bytes inside of 48-byte region [0x7f2c15f89580,0x7f2c15f895b0)  

freed by thread T5 here:  

#0 0x7f2c316de102 in free ??:0  

#1 0x7f2c2e5881e5 in WebCore::WebSocket::stop() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/Modules/websockets/WebSocket.cpp:476  

#2 0x7f2c2de06dad in WebCore::ScriptExecutionContext::stopActiveDOMObjects() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ScriptExecutionContext.cpp:222  

#3 0x7f2c2ead8bce in WebCore::WorkerThreadShutdownStartTask::performTask(WebCore::ScriptExecutionContext\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/workers/WorkerThread.cpp:226  

#4 0x7f2c2ead36a6 in WebCore::WorkerRunLoop::runCleanupTasks(WebCore::WorkerContext\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/workers/WorkerRunLoop.cpp:191  

#5 0x7f2c2ead333f in WebCore::WorkerRunLoop::run(WebCore::WorkerContext\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/workers/WorkerRunLoop.cpp:138  

#6 0x7f2c2ead827c in WebCore::WorkerThread::workerThread() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/workers/WorkerThread.cpp:161  

#7 0x7f2c30ef0cc3 in WTF::threadEntryPoint(void\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WTF/wtf/Threading.cpp:70  

#8 0x7f2c2de609ff in WTF::wtfThreadEntryPoint(void\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WTF/wtf/ThreadingPthreads.cpp:165  

#9 0x7f2c316e1805 in \_\_asan::AsanThread::ThreadStart() ??:0  

previously allocated by thread T5 here:  

#0 0x7f2c316de1c2 in malloc ??:0  

#1 0x7f2c2de5febb in WTF::fastMalloc(unsigned long) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WTF/wtf/FastMalloc.cpp:268  

#2 0x7f2c2eb69c09 in WebCore::WorkerThreadableWebSocketChannel::Bridge::create(WTF::PassRefPtr[WebCore::ThreadableWebSocketChannelClientWrapper](javascript:void(0);), WTF::PassRefPtr[WebCore::WorkerContext](javascript:void(0);), WTF::String const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/Modules/websockets/WorkerThreadableWebSocketChannel.h:131  

#3 0x7f2c2eb69a1f in WebCore::WorkerThreadableWebSocketChannel::WorkerThreadableWebSocketChannel(WebCore::WorkerContext\*, WebCore::WebSocketChannelClient\*, WTF::String const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/Modules/websockets/WorkerThreadableWebSocketChannel.cpp:57  

#4 0x7f2c2eb53c39 in WebCore::WorkerThreadableWebSocketChannel::create(WebCore::WorkerContext\*, WebCore::WebSocketChannelClient\*, WTF::String const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/Modules/websockets/WorkerThreadableWebSocketChannel.h:59  

#5 0x7f2c2eb53aa8 in ~RefPtr /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WTF/wtf/RefPtr.h:58  

#6 0x7f2c2e585296 in WebCore::WebSocket::connect(WTF::String const&, WTF::Vector<WTF::String, 0ul> const&, int&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/Modules/websockets/WebSocket.cpp:227  

#7 0x7f2c2e58446c in WebCore::WebSocket::connect(WTF::String const&, int&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/Modules/websockets/WebSocket.cpp:179  

#8 0x7f2c311939bb in WebCore::V8WebSocket::constructorCallback(v8::Arguments const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/custom/V8WebSocketCustom.cpp:85  

#9 0x7f2c2ce3f40e in HandleApiCallHelper /media/Chromium/chromium/depot\_tools/src/v8/src/builtins.cc:1115  

#10 0xe9de9b0618e  

#11 0xe9de9b23cb7  

#12 0xe9de9b2b08c  

#13 0xe9de9b23dc7  

#14 0xe9de9b11357  

#15 0x7f2c2ceabf74 in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) /media/Chromium/chromium/depot\_tools/src/v8/src/execution.cc:118  

#16 0x7f2c2cdd29b1 in v8::Script::Run() /media/Chromium/chromium/depot\_tools/src/v8/src/api.cc:1589  

#17 0x7f2c2e647684 in WebCore::WorkerContextExecutionProxy::runScript(v8::Handle[v8::Script](javascript:void(0);)) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/WorkerContextExecutionProxy.cpp:252  

#18 0x7f2c2e646ef6 in WebCore::WorkerContextExecutionProxy::evaluate(WTF::String const&, WTF::String const&, WTF::TextPosition const&, WebCore::WorkerContextExecutionState\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/WorkerContextExecutionProxy.cpp:203  

#19 0x7f2c2e648844 in WebCore::WorkerScriptController::evaluate(WebCore::ScriptSourceCode const&, WebCore::ScriptValue\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/WorkerScriptController.cpp:85  

#20 0x7f2c2ead8221 in WebCore::WorkerThread::workerThread() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/ScriptSourceCode.h:44  

Thread T5 created by T0 here:  

#0 0x7f2c316dc353 in pthread\_create ??:0  

#1 0x7f2c2de6086f in WTF::createThreadInternal(void (\*)(void\*), void\*, char const\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WTF/wtf/ThreadingPthreads.cpp:210  

#2 0x7f2c30ef0b7f in WTF::createThread(void (\*)(void\*), void\*, char const\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WTF/wtf/Threading.cpp:86  

#3 0x7f2c2ead7edf in WebCore::WorkerThread::start() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/workers/WorkerThread.cpp:122  

#4 0x7f2c2dcf7d2b in WebKit::WebWorkerClientImpl::startWorkerContext(WebCore::KURL const&, WTF::String const&, WTF::String const&, WebCore::WorkerThreadStartMode) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebKit/chromium/src/WebWorkerClientImpl.cpp:94  

#5 0x7f2c311b0e60 in ~RefPtr /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WTF/wtf/RefPtr.h:58  

#6 0x7f2c2ead750b in WebCore::WorkerScriptLoader::didFinishLoading(unsigned long, double) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/workers/WorkerScriptLoader.cpp:163  

#7 0x7f2c2e95c81e in WebCore::DocumentThreadableLoader::notifyFinished(WebCore::CachedResource\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/DocumentThreadableLoader.cpp:262  

#8 0x7f2c2e9ce66d in WebCore::CachedResource::checkNotify() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/cache/CachedResource.cpp:247  

#9 0x7f2c2eccf253 in ~PassRefPtr /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WTF/wtf/PassRefPtr.h:67  

#10 0x7f2c2e9b36a4 in WebCore::SubresourceLoader::didFinishLoading(double) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/SubresourceLoader.cpp:276  

#11 0x7f2c2f9553e5 in webkit\_glue::WebURLLoaderImpl::Context::OnCompletedRequest(net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) /media/Chromium/chromium/depot\_tools/src/webkit/glue/weburlloader\_impl.cc:655  

#12 0x7f2c2d7ed16f in ResourceDispatcher::OnRequestComplete(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:489  

#13 0x7f2c2d7ee426 in bool ResourceMsg\_RequestComplete::Dispatch<ResourceDispatcher, ResourceDispatcher, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)>(IPC::Message const\*, ResourceDispatcher\*, ResourceDispatcher\*, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)) /media/Chromium/chromium/depot\_tools/src/./content/common/resource\_messages.h:169  

#14 0x7f2c2d7eacf6 in ResourceDispatcher::DispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:559  

#15 0x7f2c2d7e9f7f in ResourceDispatcher::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:326  

#16 0x7f2c2d6e73e2 in ChildThread::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/child\_thread.cc:172  

#17 0x7f2c2c674e4a in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/ipc/ipc\_channel\_proxy.cc:268  

#18 0x7f2c2c67af98 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::\*)(IPC::Message const&)>, void ()(IPC::ChannelProxy::Context\* const&, IPC::Message const&)>::MakeItSo(base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::\*)(IPC::Message const&)>, IPC::ChannelProxy::Context\* const&, IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/./base/bind\_internal.h:897  

#19 0x7f2c2c581823 in MessageLoop::RunTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:459  

#20 0x7f2c2c582014 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:470  

#21 0x7f2c2c5823ce in MessageLoop::DoWork() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:660  

#22 0x7f2c2c58e7de in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /media/Chromium/chromium/depot\_tools/src/base/message\_pump\_default.cc:28  

#23 0x7f2c2c58103e in MessageLoop::RunInternal() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:418  

#24 0x7f2c2c57fd18 in MessageLoop::Run() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:301  

#25 0x7f2c3066303c in RendererMain(content::MainFunctionParams const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/renderer\_main.cc:241  

#26 0x7f2c2c4b1684 in (anonymous namespace)::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main\_runner.cc:245  

#27 0x7f2c2c4b11cd in (anonymous namespace)::RunNamedProcessTypeMain(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main\_runner.cc:290  

#28 0x7f2c2c4b0b6c in (anonymous namespace)::ContentMainRunnerImpl::Run() /media/Chromium/chromium/depot\_tools/src/content/app/content\_main\_runner.cc:511  

#29 0x7f2c2c4affef in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:35  

#30 0x7f2c2b2937c7 in ChromeMain /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_main.cc:32  

#31 0x7f2c2b29371b in main /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#32 0x7f2c24197d8e in \_\_libc\_start\_main /build/buildd/eglibc-2.12.1/csu/libc-start.c:258  

==6163== ABORTING  

Stats: 48M malloced (40M for red zones) by 109558 calls  

Stats: 2M realloced by 4080 calls  

Stats: 44M freed by 94857 calls  

Stats: 0M really freed by 0 calls  

Stats: 116M (29712 full pages) mmaped in 29 calls  

mmaps by size class: 8:98298; 9:16382; 10:12285; 11:4094; 12:1024; 13:1536; 14:256; 15:256; 16:64; 17:64; 18:16; 19:8; 20:4; 21:6;  

mallocs by size class: 8:82809; 9:10663; 10:11142; 11:2496; 12:547; 13:1450; 14:195; 15:156; 16:31; 17:46; 18:8; 19:8; 20:1; 21:6;  

frees by size class: 8:70237; 9:9903; 10:10403; 11:2088; 12:454; 13:1363; 14:180; 15:150; 16:24; 17:32; 18:8; 19:8; 20:1; 21:6;  

rfrees by size class:  

Stats: malloc large: 69 small slow: 534  

Shadow byte and word:  

0x1fe582bf12b3: fd  

0x1fe582bf12b0: fd fd fd fd fd fd fd fd  

More shadow bytes:  

0x1fe582bf1290: 00 00 00 00 00 00 00 00  

0x1fe582bf1298: 00 00 00 00 00 00 00 00  

0x1fe582bf12a0: fa fa fa fa fa fa fa fa  

0x1fe582bf12a8: fa fa fa fa fa fa fa fa  

=>0x1fe582bf12b0: fd fd fd fd fd fd fd fd  

0x1fe582bf12b8: fd fd fd fd fd fd fd fd  

0x1fe582bf12c0: fa fa fa fa fa fa fa fa  

0x1fe582bf12c8: fa fa fa fa fa fa fa fa  

0x1fe582bf12d0: 00 00 00 00 00 00 00 00

## Attachments

- 27-03-2012-uaf.zip (application/zip; charset=binary, 758 B)
- [tc-27-03-2012-uaf-2.zip](attachments/tc-27-03-2012-uaf-2.zip) (application/zip; charset=binary, 416 B)

## Timeline

### ax...@gmail.com (2012-03-31)

Attached more simple and stable testcase, but still may crash on address 0x000000000018 and still uses location.reload().

### in...@chromium.org (2012-03-31)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-31)

Dave, from CF regression range, this seems to be coming from https://trac.webkit.org/changeset/102473/. Can you please help to take a look. Also, ccing Dmitry, in case he has time to knock this out.

### in...@chromium.org (2012-03-31)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=32320941

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f900ea11198
Crash State:
  - crash stack -
  WebCore::WorkerThreadableWebSocketChannel::Bridge::mainThreadCreateWebSocketChannel
  WebCore::CrossThreadTask3<WebCore::WorkerThreadableWebSocketChannel::Bridge*, WebCore::WorkerThreada
  - free stack -
  WebCore::WebSocket::stop
  WebCore::ScriptExecutionContext::stopActiveDOMObjects
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=113976:113987

Minimized Testcase (0.32 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95tTVgfCDXyqjNiA7IJeFsHAticSiXbs5M6qba3g3jRGo6IHKNmXlXyJzRLRC3VAkVE1wmNLKNLEYXVIy-Htnd1GiGH3iQE7YjIVPVWP2O27kBkYW_DAfFkDj_-UJ0tTpC5m3nlqRMy_DLAlZBGhrqATznOyQ

### in...@chromium.org (2012-03-31)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-04-01)

Dave is not on the chrome team, removing him from assignee. Dmitry, can you please help us on this bug as well. Thanks!

### le...@chromium.org (2012-04-01)

I think the core problem is that the code in WorkerThreadableWebSocketChannel.cpp uses waitForMethodCompletion and assumes the method on the other thread finishes.

However, that method really should be named "waitForMethodCompletionOrQueueTerminated".

Specifically, in WorkerThreadableWebSocketChannel::Bridge::Bridge, it passes a the "this" pointer to Bridge::mainThreadCreateWebSocketChannel. 

However, if the queue is terminated, then the Bridge constructor is exited and it is possible for the Bridge to get deleted before mainThreadCreateWebSocketChannel has a chance to run.

It seems appropriate for the web socket folks to look at how best to fix this.

### yu...@chromium.org (2012-04-02)

I'm looking now.

### yu...@chromium.org (2012-04-02)

Filed a WebKit bug: https://bugs.webkit.org/show_bug.cgi?id=82873


### yu...@chromium.org (2012-04-04)

Fix landed in WebKit: http://trac.webkit.org/changeset/113138

### in...@chromium.org (2012-04-04)

[Empty comment from Monorail migration]

### yu...@chromium.org (2012-04-04)

WebKit change merged to Chromium trunk at http://src.chromium.org/viewvc/chrome?view=rev&revision=130584

### yu...@chromium.org (2012-04-04)

inferno: Do I need to merge the change to beta/stable branches by myself? Or are you going to do that?

### in...@chromium.org (2012-04-04)

Yuta, we will handle the merges, thanks a lot for the patch.!

### yu...@chromium.org (2012-04-04)

OK, thanks.

### cl...@chromium.org (2012-04-04)

ClusterFuzz has detected this issue as fixed in range 130574:130586.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=32320941

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f900ea11198
Crash State:
  - crash stack -
  WebCore::WorkerThreadableWebSocketChannel::Bridge::mainThreadCreateWebSocketChannel
  WebCore::CrossThreadTask3<WebCore::WorkerThreadableWebSocketChannel::Bridge*, WebCore::WorkerThreada
  - free stack -
  WebCore::WebSocket::stop
  WebCore::ScriptExecutionContext::stopActiveDOMObjects
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=113976:113987
Fixed: https://cluster-fuzz.appspot.com/revisions?range=130574:130586

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95tTVgfCDXyqjNiA7IJeFsHAticSiXbs5M6qba3g3jRGo6IHKNmXlXyJzRLRC3VAkVE1wmNLKNLEYXVIy-Htnd1GiGH3iQE7YjIVPVWP2O27kBkYW_DAfFkDj_-UJ0tTpC5m3nlqRMy_DLAlZBGhrqATznOyQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### js...@chromium.org (2012-04-24)

Dropping severity a notch since this is a race.

### in...@chromium.org (2012-04-24)

Nice find Ax300d! This qualifies for the $500 Chromium Security Reward. $500 because this looks like a race condition and we typically reward $500 for those.

### sc...@gmail.com (2012-04-30)

M19: http://trac.webkit.org/changeset/115612

### sc...@gmail.com (2012-05-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-05-14)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Updating status to Fixed on security bugs which were fixed when m19 went to stable.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

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

This issue was migrated from crbug.com/chromium/121223?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055964)*
