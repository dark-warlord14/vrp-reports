# Use-after-poison in blink::WorkerWebSocketChannel::Bridge::traceImpl<blink::InlinedGlobalMarkingVisi

| Field | Value |
|-------|-------|
| **Issue ID** | [40083118](https://issues.chromium.org/issues/40083118) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GarbageCollection, Blink>Network>WebSockets, Blink>Workers |
| **Platforms** | Windows |
| **Reporter** | th...@gmail.com |
| **Assignee** | yh...@chromium.org |
| **Created** | 2015-11-02 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5934574129905664

Fuzzer: therealholden_worker
Job Type: windows_asan_chrome
Platform Id: windows

Crash Type: Use-after-poison READ 4
Crash Address: 0x0c226e48
Crash State:
  blink::WorkerWebSocketChannel::Bridge::traceImpl<blink::InlinedGlobalMarkingVisi
  blink::TraceTrait<blink::WorkerWebSocketChannel::Bridge>::mark<blink::Visitor
  blink::TraceMethodDelegate<blink::PersistentBase<blink::WorkerWebSocketChannel::
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv958NcgCZfw5mZbSEIAHl-Rtk8iRpnBIXQVaEMdalNf118GG6CiNMT53okSvR4dbo0mDqiGhZl0f13Wy0YAWuSf6RqUcjXQIW86lDGGIC05Ckbs89ZkNSiSUhue_2D4IbBPyvjBkAcSffNxoncwJSpH3JWHiRg


Additional requirements: Requires HTTP

Filer: mbarbella

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### me...@chromium.org (2015-11-03)

Not getting a crash on stable or beta.

+yhirano: Can you PTAL and reassign as appropriate? Thanks.

### me...@chromium.org (2015-11-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-03)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### yh...@chromium.org (2015-11-04)

[Empty comment from Monorail migration]

### yh...@chromium.org (2015-11-04)

Added Cr-Blink-MemoryAllocator-GarbageCollection label due to the issue title (but strangely the clusterfuzz report doesn't contain the string).

meacer@, I don't know what "use-after-poison" means: can you tell me?

### yh...@chromium.org (2015-11-04)

[Empty comment from Monorail migration]

### yu...@chromium.org (2015-11-04)

[Empty comment from Monorail migration]

### yu...@chromium.org (2015-11-05)

I've looked at Oilpan's code of poisoning, but turns out we do not mass-poison the
to-be-swept memory when enable_oilpan=0:

https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/platform/heap/ThreadState.cpp&l=1044

So, what we are seeing in this crash is probably the memory poisoned in
the manual poisoning for freed memory in HeapPage.cpp
(search for SET_MEMORY_INACCESSIBLE):
https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/platform/heap/HeapPage.cpp

I think this is a typical use-after-free...

### bu...@chromium.org (2015-11-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4b823461db8e2bc8faf5438be4cc30f6a9401aef

commit 4b823461db8e2bc8faf5438be4cc30f6a9401aef
Author: yhirano <yhirano@chromium.org>
Date: Thu Nov 05 13:10:36 2015

[WebSocket] Add assertions to check handles are properly disconnected.

It is critical to clear WebSocketHandle in DocumentWebSocketChannel
appropriately because failing that makes |WebSocketBridge::client_| a dangling
pointer. This CL adds release assertions to check it.

BUG=550632

Review URL: https://codereview.chromium.org/1411473011

Cr-Commit-Position: refs/heads/master@{#358043}

[modify] http://crrev.com/4b823461db8e2bc8faf5438be4cc30f6a9401aef/third_party/WebKit/Source/modules/websockets/DocumentWebSocketChannel.cpp
[modify] http://crrev.com/4b823461db8e2bc8faf5438be4cc30f6a9401aef/third_party/WebKit/Source/modules/websockets/DocumentWebSocketChannel.h
[modify] http://crrev.com/4b823461db8e2bc8faf5438be4cc30f6a9401aef/third_party/WebKit/Source/modules/websockets/WorkerWebSocketChannel.cpp
[modify] http://crrev.com/4b823461db8e2bc8faf5438be4cc30f6a9401aef/third_party/WebKit/Source/modules/websockets/WorkerWebSocketChannel.h


### ti...@google.com (2015-11-09)

Hey, a friendly reminder M48 branching is coming on Nov 13,and this bug is marked as a beta blocker. Please take a look and land a fix by Nov 11, so that your change can go through bake time on trunk/master before branching. Thanks!

### yh...@chromium.org (2015-11-12)

I succeeded to reproduce the issue locally.

I confirmed that a DOMWebSocket was finalized while |m_channel| was not null on a dedicated worker.
DOMWebSocket is a subclass of ActiveDOMObject and its |hasPendingActivity| returns true while |m_channel| is non-null. As the associated JS wrapper is created right after a DOMWebSocket object is created (in DOMWebSocket::create()), I have no idea why there is such a case.

haraken@, oilpan people, do you have any idea? 

### ha...@chromium.org (2015-11-12)

[Empty comment from Monorail migration]

### ha...@chromium.org (2015-11-12)

More detailed stack trace:

==1624==ERROR: AddressSanitizer: use-after-poison on address 0x0c0747c0 at pc 0x12e62305 bp 0xdeadbeef sp 0x0089d010
READ of size 4 at 0x0c0747c0 thread T0
==1624==*** WARNING: Failed to initialize DbgHelp!              ***
==1624==*** Most likely this means that the app is already      ***
==1624==*** using DbgHelp, possibly with incompatible flags.    ***
==1624==*** Due to technical reasons, symbolization might crash ***
==1624==*** or produce wrong results.                           ***
    #0 0x12e62304 in blink::DocumentWebSocketChannel::fail third_party/WebKit/Source/modules/websockets/DocumentWebSocketChannel.cpp:245
    #1 0x12e643f0 in blink::DocumentWebSocketChannel::didFail third_party/WebKit/Source/modules/websockets/DocumentWebSocketChannel.h:133
    #2 0x163031ea in content::WebSocketBridge::OnMessageReceived content/child/websocket_bridge.cc:139
    #3 0x162a96ac in content::WebSocketDispatcher::OnMessageReceived content/child/websocket_dispatcher.cc:55
    #4 0x1627e242 in content::ChildThreadImpl::OnMessageReceived content/child/child_thread_impl.cc:634
    #5 0x19158c23 in IPC::ChannelProxy::Context::OnDispatchMessage ipc/ipc_channel_proxy.cc:288
    #6 0x1915e59b in base::internal::Invoker<base::IndexSequence<0,1>,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall content::WebRtcLocalAudioRenderer::*)(media::AudioParameters const &)>,void __cdecl(content::WebRtcLocalAudioRenderer *,media::AudioParameters const &),base::internal::TypeList<content::WebRtcLocalAudioRenderer *,media::AudioParameters> >,base::internal::TypeList<base::internal::UnwrapTraits<content::WebRtcLocalAudioRenderer *>,base::internal::UnwrapTraits<media::AudioParameters> >,base::internal::InvokeHelper<0,void,base::internal::RunnableAdapter<void (__thiscall content::WebRtcLocalAudioRenderer::*)(media::AudioParameters const &)>,base::internal::TypeList<content::WebRtcLocalAudioRenderer * const &,media::AudioParameters const &> >,void __cdecl(void)>::Run base/bind_internal.h:176
    #7 0xf67cba5 in base::debug::TaskAnnotator::RunTask base/callback.h:396
    #8 0x1bbc0d7f in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue components/scheduler/base/task_queue_manager.cc:357
    #9 0x1bbba31e in scheduler::TaskQueueManager::DoWork components/scheduler/base/task_queue_manager.cc:282
    #10 0x19412090 in base::internal::Invoker<base::IndexSequence<0,1>,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall scheduler::TaskQueueManager::*)(bool)>,void __cdecl(scheduler::TaskQueueManager *,bool),base::internal::TypeList<base::WeakPtr<scheduler::TaskQueueManager>,bool> >,base::internal::TypeList<base::internal::UnwrapTraits<base::WeakPtr<scheduler::TaskQueueManager> >,base::internal::UnwrapTraits<bool> >,base::internal::InvokeHelper<1,void,base::internal::RunnableAdapter<void (__thiscall scheduler::TaskQueueManager::*)(bool)>,base::internal::TypeList<base::WeakPtr<scheduler::TaskQueueManager> const &,bool const &> >,void __cdecl(void)>::Run base/bind_internal.h:176

(I'll take a look on Monday, but any insight is welcome.)


### yh...@chromium.org (2015-11-12)

By the way, I will put a RELEASE_ASSERT to crash the renderer process in such a case, as a workaround.
https://codereview.chromium.org/1434213002/


### ha...@chromium.org (2015-11-12)

If you can reproduce the crash, would it be possible to confirm that DOMWebSocket::hasPendingActivity is really returning true in the V8 GC that happens just before you hit the crash?

I'm suspecting that the new minor GC we introduced recently may not working as expected.


### [Deleted User] (2015-11-12)

Can't a worker & its execution context be terminated without the DOMWebSocket having been orderly stopped first?

### yh...@chromium.org (2015-11-12)

> #17
DOMWebSocket::stop releases the channel, and I though it would be enough. If it's a false assumption, please let me know.

### yh...@chromium.org (2015-11-12)

>#18
s/though/thought/


### yh...@chromium.org (2015-11-12)

>#16
It looks hasPendingActivity is not called for the object.

With https://codereview.chromium.org/1440993002, I get the following output.

virtual bool blink::DOMWebSocket::hasPendingActivity() const, this = 0x7eee89ec1a30, m_channel = (nil), returns 0
virtual bool blink::DOMWebSocket::hasPendingActivity() const, this = 0x7eee89ec1a30, m_channel = (nil), returns 0
virtual blink::DOMWebSocket::~DOMWebSocket(), this = 0x7ef34c009dc8, channel = 0x7ed132cfc538, mainthread = 0
Received signal 4 ILL_ILLOPN 7fb6ddf4eede
virtual blink::DOMWebSocket::~DOMWebSocket(), this = 0x7eccd7a10308, channel = 0x7ee0bdb3edb8, mainthread = 0


### ha...@chromium.org (2015-11-12)

- Are you really creating a wrapper for the DOMWebSocket?

- Would you also printf the place where V8GCController is calling hasPendingActivity() (line 119 and 177)?


### yh...@chromium.org (2015-11-12)

> #21

https://codereview.chromium.org/1440993002/#ps50001.

...
static blink::DOMWebSocket *blink::DOMWebSocket::create(blink::ExecutionContext *, const WTF::String &, const blink::StringOrStringSequence &, blink::ExceptionState &) webSocket = 0x7ec8f8249558 (0x7ec8f8249590)
...
static blink::DOMWebSocket *blink::DOMWebSocket::create(blink::ExecutionContext *, const WTF::String &, const blink::StringOrStringSequence &, blink::ExceptionState &) webSocket = 0x7ec8f8208ce8 (0x7ec8f8208d20)
...
virtual blink::DOMWebSocket::~DOMWebSocket(), this = 0x7ec8f8249558, channel = 0x7eb4f053c1d8, mainthread = 0
virtual blink::DOMWebSocket::~DOMWebSocket(), this = 0x7ec8f8208ce8, channel = 0x7eb4f04bbe78, mainthread = 0
Received signal 4 ILL_ILLOPN 7ff33e0a619e

These are all lines containing one of
 - 0x7ec8f8249558
 - 0x7ec8f8249590
 - 0x7ec8f8208ce8 
 - 0x7ec8f8208d20
in the whole log.

> - Are you really creating a wrapper for the DOMWebSocket?
Hm. The DOMWebSocket pointer 0x7ec8f8249558 is actually returned from DOMWebSocket::create and the ExceptionState is empty at the end of the function. DOMWebSocket functions are only called from the binding layer according to the codesearch. 
https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/modules/websockets/DOMWebSocket.h&l=70
https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/modules/websockets/DOMWebSocket.h&l=71

### ha...@chromium.org (2015-11-12)

Does it mean that neither minor nor major V8 GC is invoked, right?

Maybe it would be helpful to know the stack trace for blink::DOMWebSocket::~DOMWebSocket().

- 0x7ec8f8249558
- 0x7ec8f8249590
- 0x7ec8f8208ce8 
- 0x7ec8f8208d20

^^^ BTW, aren't they on-stack addresses? Maybe you're allocating the DOMWebSocket on stack?


### cl...@chromium.org (2015-11-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-11-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a6af78bd57595484765d2a3ca18f38fa135be796

commit a6af78bd57595484765d2a3ca18f38fa135be796
Author: yhirano <yhirano@chromium.org>
Date: Fri Nov 13 12:55:55 2015

[WebSocket] Detect DOMWebSocket lifetime assumption violation eagerly

It turns out a DOMWebSocket can be finalized while its |hasPendingActivity| is
returning true. As RELEASE_ASSERT failure is better than use-after-free, this
change places a RELEASE_ASSERT to detect such a violation and crash a renderer,
as a workaround.

BUG=550632
R=tyoshino

Review URL: https://codereview.chromium.org/1434213002

Cr-Commit-Position: refs/heads/master@{#359534}

[modify] http://crrev.com/a6af78bd57595484765d2a3ca18f38fa135be796/third_party/WebKit/Source/modules/websockets/DOMWebSocket.cpp


### cl...@chromium.org (2015-11-13)

[Empty comment from Monorail migration]

### yh...@chromium.org (2015-11-14)

> Does it mean that neither minor nor major V8 GC is invoked, right?

I don't think so. There are many hasPendingActivity() entries in the log, but none them are for the websocket objects causing crashes.

> Maybe it would be helpful to know the stack trace for blink::DOMWebSocket::~DOMWebSocket().
Stack trace with https://codereview.chromium.org/1440993002/#ps70001:

    #0 0x7f60315e7541 in blink::DOMWebSocket::~DOMWebSocket() third_party/WebKit/Source/modules/websockets/DOMWebSocket.cpp:249:12
    #1 0x7f602f6d02d3 in finalize third_party/WebKit/Source/platform/heap/HeapPage.cpp:104:9
    #2 0x7f602f6d02d3 in blink::NormalPage::sweep() third_party/WebKit/Source/platform/heap/HeapPage.cpp:1148:0
    #3 0x7f602f6cb330 in sweepUnsweptPage third_party/WebKit/Source/platform/heap/HeapPage.cpp:323:9
    #4 0x7f602f6cb330 in blink::BaseHeap::completeSweep() third_party/WebKit/Source/platform/heap/HeapPage.cpp:364:0
    #5 0x7f602f6e6fc8 in blink::ThreadState::eagerSweep() third_party/WebKit/Source/platform/heap/ThreadState.cpp:1083:9
    #6 0x7f602f6e6515 in blink::ThreadState::preSweep() third_party/WebKit/Source/platform/heap/ThreadState.cpp:1029:5
    #7 0x7f602f6c495d in ~SafePointScope third_party/WebKit/Source/platform/heap/SafePoint.h:28:13
    #8 0x7f602f6c495d in blink::Heap::collectGarbage(blink::BlinkGC::StackState, blink::BlinkGC::GCType, blink::BlinkGC::GCReason) third_party/WebKit/Source/platform
/heap/Heap.cpp:468:0
    #9 0x7f602f6ce748 in blink::NormalPageHeap::outOfLineAllocate(unsigned long, unsigned long) third_party/WebKit/Source/platform/heap/HeapPage.cpp:745:5
    #10 0x7f60315e86d3 in allocateObject third_party/WebKit/Source/platform/heap/HeapPage.h:873:12
    #11 0x7f60315e86d3 in allocateOnHeapIndex third_party/WebKit/Source/platform/heap/Heap.h:458:0
    #12 0x7f60315e86d3 in allocate<blink::DOMWebSocket> third_party/WebKit/Source/platform/heap/Heap.h:465:0
    #13 0x7f60315e86d3 in allocateObject third_party/WebKit/Source/platform/heap/Heap.h:363:0
    #14 0x7f60315e86d3 in blink::DOMWebSocket::operator new(unsigned long) third_party/WebKit/Source/modules/websockets/DOMWebSocket.h:64:0
    #15 0x7f60315e7cde in blink::DOMWebSocket::create(blink::ExecutionContext*, WTF::String const&, blink::StringOrStringSequence const&, blink::ExceptionState&) thi
rd_party/WebKit/Source/modules/websockets/DOMWebSocket.cpp:271:31
    #16 0x7f60315e7b6d in blink::DOMWebSocket::create(blink::ExecutionContext*, WTF::String const&, blink::ExceptionState&) third_party/WebKit/Source/modules/websock
ets/DOMWebSocket.cpp:261:12
    #17 0x7f60310011a5 in constructor /usr/local/google/home/yhirano/work/chromium/git/src/out/Release/gen/blink/bindings/modules/v8/V8WebSocket.cpp:463:41
    #18 0x7f60310011a5 in blink::V8WebSocket::constructorCallback(v8::FunctionCallbackInfo<v8::Value> const&) /usr/local/google/home/yhirano/work/chromium/git/src/ou
t/Release/gen/blink/bindings/modules/v8/V8WebSocket.cpp:523:0
    #19 0x7f60304060a5 in v8::internal::FunctionCallbackArguments::Call(void (*)(v8::FunctionCallbackInfo<v8::Value> const&)) v8/src/arguments.cc:33:3
    #20 0x7f602f8e31f4 in HandleApiCallHelper<true> v8/src/builtins.cc:1846:34
    #21 0x7f602f8e31f4 in Builtin_implHandleApiCallConstruct v8/src/builtins.cc:1879:0
    #22 0x7f602f8e31f4 in v8::internal::Builtin_HandleApiCallConstruct(int, v8::internal::Object**, v8::internal::Isolate*) v8/src/builtins.cc:1875:0
    #13 0x7f5e1830b61a  (<unknown module>)
    #14 0x7f5e18336ca3  (<unknown module>)
    #15 0x7f5e1833d49c  (<unknown module>)
    #16 0x7f5e18336dc3  (<unknown module>)
    #17 0x7f5e1831a8e1  (<unknown module>)
    #23 0x7f602fc32735 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, bool, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<
v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, v8::internal::Handle<v8::internal::Object>) v8/src/execution.cc:98:13
    #24 0x7f602fc31aa3 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object
>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution.cc:167:10
    #25 0x7f602f841f5d in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) v8/src/api.cc:4420:7
    #26 0x7f60337d1d49 in blink::V8ScriptRunner::callFunction(v8::Local<v8::Function>, blink::ExecutionContext*, v8::Local<v8::Value>, int, v8::Local<v8::Value>*, v8::Isolate*) third_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:441:40
    #27 0x7f60337dc613 in blink::V8WorkerGlobalScopeEventListener::callListenerFunction(blink::ScriptState*, v8::Local<v8::Value>, blink::Event*) third_party/WebKit/Source/bindings/core/v8/V8WorkerGlobalScopeEventListener.cpp:82:45
    #28 0x7f603378c2d6 in blink::V8AbstractEventListener::invokeEventHandler(blink::ScriptState*, blink::Event*, v8::Local<v8::Value>) third_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:128:23
    #29 0x7f60337dc148 in blink::V8WorkerGlobalScopeEventListener::handleEvent(blink::ScriptState*, blink::Event*) third_party/WebKit/Source/bindings/core/v8/V8WorkerGlobalScopeEventListener.cpp:70:5
    #30 0x7f603378b9b9 in blink::V8AbstractEventListener::handleEvent(blink::ExecutionContext*, blink::Event*) third_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:85:5
    #31 0x7f6031c247f5 in blink::EventTarget::fireEventListeners(blink::Event*, blink::EventTargetData*, WTF::Vector<blink::RegisteredEventListener, 1ul, WTF::PartitionAllocator>&) third_party/WebKit/Source/core/events/EventTarget.cpp:435:9
    #32 0x7f6031c234e9 in blink::EventTarget::fireEventListeners(blink::Event*) third_party/WebKit/Source/core/events/EventTarget.cpp:361:9
    #33 0x7f6031c23054 in blink::EventTarget::dispatchEventInternal(WTF::PassRefPtr<blink::Event>) third_party/WebKit/Source/core/events/EventTarget.cpp:278:35
    #34 0x7f6031c22bfb in blink::EventTarget::dispatchEvent(WTF::PassRefPtr<blink::Event>) third_party/WebKit/Source/core/events/EventTarget.cpp:270:12
    #35 0x7f603a094736 in blink::WebSharedWorkerImpl::connectTask(WTF::PassOwnPtr<blink::WebMessagePortChannel>, blink::ExecutionContext*) third_party/WebKit/Source/web/WebSharedWorkerImpl.cpp:293:5
    #36 0x7f603a095a87 in operator() third_party/WebKit/Source/wtf/Functional.h:62:16
    #37 0x7f603a095a87 in WTF::PartBoundFunctionImpl<1, WTF::FunctionWrapper<void (*)(WTF::PassOwnPtr<blink::WebMessagePortChannel>, blink::ExecutionContext*)>, void (WTF::PassOwnPtr<blink::WebMessagePortChannel>, blink::ExecutionContext*)>::operator()(blink::ExecutionContext*) third_party/WebKit/Source/wtf/Functional.h:178:0
    #38 0x7f6032c1715c in blink::WorkerThreadTask::run() third_party/WebKit/Source/core/workers/WorkerThread.cpp:130:9
    #39 0x7f6035da3371 in Run base/bind_internal.h:157:12
    #40 0x7f6035da3371 in MakeItSo base/bind_internal.h:293:0
    #41 0x7f6035da3371 in base::internal::Invoker<base::IndexSequence<0ul>, base::internal::BindState<base::internal::RunnableAdapter<void (*)(scoped_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter<blink::WebTaskRunner::Task> >)>, void (scoped_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter<blink::WebTaskRunner::Task> >), base::internal::TypeList<base::internal::PassedWrapper<scoped_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter<blink::WebTaskRunner::Task> > > > >, base::internal::TypeList<base::internal::UnwrapTraits<base::internal::PassedWrapper<scoped_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter<blink::WebTaskRunner::Task> > > > >, base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (*)(scoped_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter<blink::WebTaskRunner::Task> >)>, base::internal::TypeList<scoped_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter<blink::WebTaskRunner::Task> > > >, void ()>::Run(base::internal::BindStateBase*) base/bind_internal.h:343:0
    #42 0x7f602cf329a4 in Run base/callback.h:396:12
    #43 0x7f602cf329a4 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask const&) base/debug/task_annotator.cc:51:0
    #44 0x7f6035db87f2 in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(scheduler::internal::TaskQueueImpl*, scheduler::internal::TaskQueueImpl::Task*) components/scheduler/base/task_queue_manager.cc:357:3
    #45 0x7f6035db44e0 in scheduler::TaskQueueManager::DoWork(bool) components/scheduler/base/task_queue_manager.cc:282:13
    #46 0x7f602cf329a4 in Run base/callback.h:396:12
    #47 0x7f602cf329a4 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask const&) base/debug/task_annotator.cc:51:0
    #48 0x7f602ce4865f in base::MessageLoop::RunTask(base::PendingTask const&) base/message_loop/message_loop.cc:481:3
    #49 0x7f602ce49ae4 in DeferOrRunPendingTask base/message_loop/message_loop.cc:490:5
    #50 0x7f602ce49ae4 in base::MessageLoop::DoWork() base/message_loop/message_loop.cc:602:0
    #51 0x7f602ce4fea0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:32:21
    #52 0x7f602ce7d6d8 in base::RunLoop::Run() base/run_loop.cc:55:3
    #53 0x7f602ce46c4e in base::MessageLoop::Run() base/message_loop/message_loop.cc:288:3
    #54 0x7f602cedf9b5 in base::Thread::ThreadMain() base/threading/thread.cc:251:3
    #55 0x7f602ced3a9e in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:64:3
    #56 0x7f60232c1181 in start_thread /build/buildd/eglibc-2.19/nptl/pthread_create.c:312:0

> - 0x7ec8f8249558
> - 0x7ec8f8249590
> - 0x7ec8f8208ce8 
> - 0x7ec8f8208d20
>
> ^^^ BTW, aren't they on-stack addresses? Maybe you're allocating the DOMWebSocket on stack?

As you can see at DOMWebSocket:280 in https://codereview.chromium.org/1440993002/#ps50001, they are addresses gotten from "new DOMWebSocket(...)".

### [Deleted User] (2015-11-14)

For #14, DocumentWebSocketChannel::BlobLoader needs to be eagerly finalized (like DocumentWebSocketChannel already is.)

### [Deleted User] (2015-11-15)

[Comment Deleted]

### [Deleted User] (2015-11-15)

[Comment Deleted]

### [Deleted User] (2015-11-16)

For #16 (and questions being raised around hasPendingActivity()), I can't pick out problems with https://codereview.chromium.org/1411993003/ , but it is an interesting theory worth double checking.

### yh...@chromium.org (2015-11-17)

> #28

Can you tell me why calling FileReaderLoader::cancel (via DocumentWebSocketChannel::disconnect) is not enough?

### ha...@chromium.org (2015-11-17)

[Empty comment from Monorail migration]

### [Deleted User] (2015-11-17)

If you don't disconnect cleanly, for some reason, you've got a mismatch in terms of finalization -- the DocumentWebSocketChannel will be eagerly finalized !OILPAN, whereas that loader object won't. => If the load is completed later, you'll access a freed m_channel.

### ha...@chromium.org (2015-11-17)

BTW, the direct cause of this crash looks like https://codereview.chromium.org/1450293002/.


### [Deleted User] (2015-11-17)

awesome :)

### bu...@chromium.org (2015-11-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/84814a37400d1cfa6707e7bb06dddeacd492d7f2

commit 84814a37400d1cfa6707e7bb06dddeacd492d7f2
Author: haraken <haraken@chromium.org>
Date: Tue Nov 17 07:56:16 2015

Enable MinorGCUnmodifiedWrapperVisitor in workers

Currently MinorGCUnmodifiedWrapperVisitor is disabled in workers.
Consequently, hasPendingActivity is ignored and a bunch of wrappers are wrongly collected
when a V8 minor GC is triggered in workers. This has caused a bunch of undeterministic crashes
in workers.

BUG=550632,553769

Review URL: https://codereview.chromium.org/1450293002

Cr-Commit-Position: refs/heads/master@{#360032}

[modify] http://crrev.com/84814a37400d1cfa6707e7bb06dddeacd492d7f2/third_party/WebKit/Source/bindings/core/v8/V8GCController.cpp


### bu...@chromium.org (2015-11-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/44fc1a4e012e9694b558a1f0cb7b73178dc1bcf6

commit 44fc1a4e012e9694b558a1f0cb7b73178dc1bcf6
Author: Kentaro Hara <haraken@chromium.org>
Date: Tue Nov 24 01:41:58 2015

Enable MinorGCUnmodifiedWrapperVisitor in workers

Currently MinorGCUnmodifiedWrapperVisitor is disabled in workers.
Consequently, hasPendingActivity is ignored and a bunch of wrappers are wrongly collected
when a V8 minor GC is triggered in workers. This has caused a bunch of undeterministic crashes
in workers.

BUG=550632,553769

Review URL: https://codereview.chromium.org/1450293002

Cr-Commit-Position: refs/heads/master@{#360032}
(cherry picked from commit 84814a37400d1cfa6707e7bb06dddeacd492d7f2)

Review URL: https://codereview.chromium.org/1475493002 .

Cr-Commit-Position: refs/branch-heads/2564@{#98}
Cr-Branched-From: 1283eca15bd9f772387f75241576cde7bdec7f54-refs/heads/master@{#359700}

[modify] http://crrev.com/44fc1a4e012e9694b558a1f0cb7b73178dc1bcf6/third_party/WebKit/Source/bindings/core/v8/V8GCController.cpp


### yh...@chromium.org (2015-11-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-24)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-11-24)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/44fc1a4e012e9694b558a1f0cb7b73178dc1bcf6

commit 44fc1a4e012e9694b558a1f0cb7b73178dc1bcf6
Author: Kentaro Hara <haraken@chromium.org>
Date: Tue Nov 24 01:41:58 2015


### [Deleted User] (2015-11-24)

Shouldn't the temporary release asserts (#10, #25) be reverted?

### yh...@chromium.org (2015-11-24)

> #42
Under review:
https://codereview.chromium.org/1456463002/

### bu...@chromium.org (2015-11-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c9feab14e31c6e5bbaaef2461529f7b20df47ac6

commit c9feab14e31c6e5bbaaef2461529f7b20df47ac6
Author: yhirano <yhirano@chromium.org>
Date: Tue Nov 24 11:55:29 2015

[WebSocket] Remove release assertions that are no longer needed.

[1] and [2] placed release assertions to investigate a crash bug and provide a
workaround solution. Now the right fix has been landed and we can remove them.

1: https://crrev.com/4b823461db8e2bc8faf5438be4cc30f6a9401aef
2: https://crrev.com/a6af78bd57595484765d2a3ca18f38fa135be796

BUG=550632

Review URL: https://codereview.chromium.org/1456463002

Cr-Commit-Position: refs/heads/master@{#361320}

[modify] http://crrev.com/c9feab14e31c6e5bbaaef2461529f7b20df47ac6/third_party/WebKit/Source/modules/websockets/DOMWebSocket.cpp
[modify] http://crrev.com/c9feab14e31c6e5bbaaef2461529f7b20df47ac6/third_party/WebKit/Source/modules/websockets/DocumentWebSocketChannel.cpp
[modify] http://crrev.com/c9feab14e31c6e5bbaaef2461529f7b20df47ac6/third_party/WebKit/Source/modules/websockets/DocumentWebSocketChannel.h
[modify] http://crrev.com/c9feab14e31c6e5bbaaef2461529f7b20df47ac6/third_party/WebKit/Source/modules/websockets/WorkerWebSocketChannel.cpp
[modify] http://crrev.com/c9feab14e31c6e5bbaaef2461529f7b20df47ac6/third_party/WebKit/Source/modules/websockets/WorkerWebSocketChannel.h


### ty...@chromium.org (2016-02-22)

[Empty comment from Monorail migration]

[Monorail components: -Blink>WebSockets Blink>Network>WebSockets]

### cl...@chromium.org (2016-03-02)

This security bug has been closed for more than 14 weeks. Removing view restrictions.

- Your friendly Sheriffbot

### ti...@google.com (2016-06-30)

Another backlog round bug, and another $3,500 here ($3k for the bug, $500 for the fuzzer).

### aw...@chromium.org (2016-06-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-09-16)

[Empty comment from Monorail migration]

[Monorail components: -Blink>MemoryAllocator>GarbageCollection Blink>GarbageCollection]

### is...@google.com (2021-09-16)

This issue was migrated from crbug.com/chromium/550632?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>GarbageCollection, Blink>Network>WebSockets, Blink>Workers]
[Monorail mergedwith: crbug.com/chromium/563727, crbug.com/chromium/563731]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083118)*
