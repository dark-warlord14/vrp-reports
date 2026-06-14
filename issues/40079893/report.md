# Heap-use-after-free in v8::HandleScope::Initialize

| Field | Value |
|-------|-------|
| **Issue ID** | [40079893](https://issues.chromium.org/issues/40079893) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>IndexedDB |
| **Reporter** | cl...@chromium.org |
| **Assignee** | tk...@chromium.org |
| **Created** | 2014-06-24 |
| **Bounty** | $1,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5594787132473344

Fuzzer: Therealholden_worker
Job Type: Mac_asan_chrome

Crash Type: Use-after-poison READ 4
Crash Address: 0x427a9c68
Crash State:
  - crash stack -
  WebCore::IDBTransaction::registerRequest
  WebCore::IDBRequest::create
  WebCore::IDBObjectStore::put
  
Regressed: https://cluster-fuzz.appspot.com//revisions?job=mac_asan_chrome&range=273150:273188

Minimized Testcase (1.53 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95zBiOmaZjRSxMO1AclSRYTpFuNOZ3D_NSEfe-oLbN1VROenoGRFNGZfR3tN4QgIIcetMxH8aIjEgX8CJ3kU3eiKYjymiY0z7DC1oHKEVHYQLf0MzIWJJnFX2wUxD--WkE52MiMyv7mMKEtBae1_hbK-QfkIQ

## Timeline

### in...@chromium.org (2014-06-24)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-06-24)

[Empty comment from Monorail migration]

### js...@chromium.org (2014-06-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-06-24)

[Empty comment from Monorail migration]

### rs...@chromium.org (2014-06-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-06-24)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-07-03)

cmumford@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### js...@chromium.org (2014-07-07)

This looks to me like it must be an Oilpan bug or false positive.

* The worker run loop is active, and dispatches an IDB event
* In response to the IDB event, V8 runs some code which calls into IDBObjectStore::put
* The IDBObjectStore::put calls into IDBRequest::create which calls into IDBTransaction::registerRequest. The request is newly created, the transaction is held onto by the object store as a Member<IDBTransaction>

Is this a false positive due to some magic in HeapListHashSet<Member<IDBRequest>> perhaps?

### js...@chromium.org (2014-07-07)

[Empty comment from Monorail migration]

### tk...@chromium.org (2014-07-08)

jsbell, did you reproduce this locally?
This wasn't reproducible to me.

Probably this is a dupe of https://crbug.com/chromium/388267.  The testcases are very similar.


### cm...@chromium.org (2014-07-08)

I was able to reproduce on a Linux ASAN build, but w/o symbols so not sure of a complete repro. Was also able to get a 100% reproducible failure on a Linux debug build, but with a different stack - I expect just one caught earlier with a DCHECK.

### tk...@chromium.org (2014-07-08)

Hmm, both of Linux ASAN and Linux Debug look unrelated.

Linux ASAN:
==10==ERROR: AddressSanitizer: use-after-poison on address 0x7f826fd04108 at pc 0x7f82af5bd207 bp 0x7f82296fdcf0 sp 0x7f82296fdce8
WRITE of size 8 at 0x7f826fd04108 thread T84
    #0 0x7f82af5bd206 in NoBarrier_Store /usr/local/google/home/tkent/chrome/src/out_asan/Release/../../v8/src/base/atomicops_internals_x86_gcc.h:206:0
    #1 0x7f82af5bd206 in nobarrier_set_size /usr/local/google/home/tkent/chrome/src/out_asan/Release/../../v8/src/objects-inl.h:3254:0
    #2 0x7f82af5bd206 in set_size /usr/local/google/home/tkent/chrome/src/out_asan/Release/../../v8/src/spaces.cc:2017:0
    #3 0x7f82af5bd206 in v8::internal::FreeList::Free(unsigned char*, int) /usr/local/google/home/tkent/chrome/src/out_asan/Release/../../v8/src/spaces.cc:2227:0
    #4 0x7f82af5b1744 in Free /usr/local/google/home/tkent/chrome/src/out_asan/Release/../../v8/src/spaces.h:1844:0
    #5 0x7f82af5b1744 in Initialize /usr/local/google/home/tkent/chrome/src/out_asan/Release/../../v8/src/spaces-inl.h:148:0
    #6 0x7f82af5b1744 in v8::internal::MemoryAllocator::AllocatePage(long, v8::internal::PagedSpace*, v8::internal::Executability) /usr/local/google/home/tkent/chrome/src/out_asan/Release/../../v8/src/spaces.cc:730:0
    #7 0x7f82af5b2b5b in v8::internal::PagedSpace::Expand() /usr/local/google/home/tkent/chrome/src/out_asan/Release/../../v8/src/spaces.cc:1034:0
    #8 0x7f82af5bf96d in v8::internal::PagedSpace::SlowAllocateRaw(int) /usr/local/google/home/tkent/chrome/src/out_asan/Release/../../v8/src/spaces.cc:2622:0
    #9 0x7f82aeed854e in v8::internal::PagedSpace::AllocateRaw(int) /usr/local/google/home/tkent/chrome/src/out_asan/Release/../../v8/src/spaces-inl.h:260:0
    #10 0x7f82aef589b7 in v8::internal::Heap::ReserveSpace(int*, unsigned char**) /usr/local/google/home/tkent/chrome/src/out_asan/Release/../../v8/src/heap.cc:948:0
    #11 0x7f82af5a1231 in v8::internal::Deserializer::Deserialize(v8::internal::Isolate*) /usr/local/google/home/tkent/chrome/src/out_asan/Release/../../v8/src/serialize.cc:740:0
    #12 0x7f82af1cd768 in v8::internal::Isolate::Init(v8::internal::Deserializer*) /usr/local/google/home/tkent/chrome/src/out_asan/Release/../../v8/src/isolate.cc:1932:0
    #13 0x7f82af62003a in v8::internal::V8::Initialize(v8::internal::Deserializer*) /usr/local/google/home/tkent/chrome/src/out_asan/Release/../../v8/src/v8.cc:41:0
    #14 0x7f82af821026 in v8::internal::Snapshot::Initialize() /usr/local/google/home/tkent/chrome/src/out_asan/Release/../../v8/src/snapshot-common.cc:38:0
    #15 0x7f82aeced2e1 in InitializeHelper /usr/local/google/home/tkent/chrome/src/out_asan/Release/../../v8/src/api.cc:210:0
    #16 0x7f82aeced2e1 in EnsureInitializedForIsolate /usr/local/google/home/tkent/chrome/src/out_asan/Release/../../v8/src/api.cc:220:0
    #17 0x7f82aeced2e1 in v8::V8::AddMessageListener(void (*)(v8::Handle<v8::Message>, v8::Handle<v8::Value>), v8::Handle<v8::Value>) /usr/local/google/home/tkent/chrome/src/out_asan/Release/../../v8/src/api.cc:6308:0
    #18 0x7f82b1859bec in WebCore::V8Initializer::initializeWorker(v8::Isolate*) /usr/local/google/home/tkent/chrome/src/out_asan/Release/../../third_party/WebKit/Source/bindings/core/v8/V8Initializer.cpp:242:0
    #19 0x7f82b1881f06 in WebCore::WorkerScriptController::WorkerScriptController(WebCore::WorkerGlobalScope&) /usr/local/google/home/tkent/chrome/src/out_asan/Release/../../third_party/WebKit/Source/bindings/core/v8/WorkerScriptController.cpp:68:0
    #20 0x7f82b0f8a617 in WebCore::WorkerGlobalScope::WorkerGlobalScope(WebCore::KURL const&, WTF::String const&, WebCore::WorkerThread*, double, WTF::PassOwnPtr<WebCore::WorkerClients>) /usr/local/google/home/tkent/chrome/src/out_asan/Release/../../third_party/WebKit/Source/core/workers/WorkerGlobalScope.cpp:83:16
    #21 0x7f82b75ac682 in SharedWorkerGlobalScope /usr/local/google/home/tkent/chrome/src/out_asan/Release/../../third_party/WebKit/Source/core/workers/SharedWorkerGlobalScope.cpp:63:0
    #22 0x7f82b75ac682 in WebCore::SharedWorkerGlobalScope::create(WTF::String const&, WebCore::SharedWorkerThread*, WTF::PassOwnPtr<WebCore::WorkerThreadStartupData>) /usr/local/google/home/tkent/chrome/src/out_asan/Release/../../third_party/WebKit/Source/core/workers/SharedWorkerGlobalScope.cpp:55:0


Linux Debug:
[5705:5733:0708/134742:FATAL:storage_monitor.cc(367)] Check failed: false. 
#0 0x7f2d1d7fe70e base::debug::StackTrace::StackTrace()
#1 0x7f2d1d891a55 logging::LogMessage::~LogMessage()
#2 0x7f2d1a0be9ea quota::StorageMonitor::NotifyUsageChange()
#3 0x7f2d1a0cd44a quota::ClientUsageTracker::DidGetHostUsageAfterUpdate()
#4 0x7f2d1a0dd7af base::internal::RunnableAdapter<>::Run()
#5 0x7f2d1a0dd6fd base::internal::InvokeHelper<>::MakeItSo()
#6 0x7f2d1a0dd684 base::internal::Invoker<>::Run()
#7 0x7f2d19f516b6 base::Callback<>::Run()
#8 0x7f2d1a0cd258 quota::(anonymous namespace)::DidGetHostUsage()
#9 0x7f2d1a0e86ea base::internal::RunnableAdapter<>::Run()
#10 0x7f2d1a0e867f base::internal::InvokeHelper<>::MakeItSo()
#11 0x7f2d1a0e8626 base::internal::Invoker<>::Run()
#12 0x7f2d1a0cf9cb base::Callback<>::Run()
#13 0x7f2d1a0e45ff DispatchToMethod<>()
#14 0x7f2d1a0e3d0f quota::DispatchToCallback<>()


### cm...@chromium.org (2014-07-08)

I think there's something with the StorageMonitor, but if you comment out that NOTREACHED() then I get this stack trace:

Building Debug...
ninja: Entering directory `out/Debug'
[5/5] LINK chrome
Running "devchrome"...
[2214:2324:0708/085508:WARNING:raw_channel_posix.cc(214)] recvmsg: Connection reset by peer
.ASSERTION FAILED: Heap::lastGCWasConservative() || basicHeader->isFree()
../../third_party/WebKit/Source/platform/heap/Heap.cpp(928) : void WebCore::ThreadHeap<Header>::assertEmpty() [with Header = WebCore::FinalizedHeapObjectHeader]
1   0x7f7802054dce
2   0x7f7802058ea9
3   0x7f7802058f42
4   0x7f7802f6660d
5   0x7f7802f6622c
6   0x7f7807c3db16
7   0x7f780214a0f5
8   0x7f77f9d73182
9   0x7f77f812330d clone
Received signal 11 SEGV_MAPERR 0000fbadbeef
#0 0x7f7800783b7b base::debug::StackTrace::StackTrace()
#1 0x7f7800783470 base::debug::(anonymous namespace)::StackDumpSignalHandler()
#2 0x7f77f9d7b340 <unknown>
#3 0x7f7802054dd8 WebCore::ThreadHeap<>::assertEmpty()
#4 0x7f7802058ea9 WebCore::ThreadState::cleanup()
#5 0x7f7802058f42 WebCore::ThreadState::detach()
#6 0x7f7802f6660d WebCore::WorkerThread::workerThread()
#7 0x7f7802f6622c WebCore::WorkerThread::workerThreadStart()
#8 0x7f7807c3db16 ASSERTION FAILED: Heap::lastGCWasConservative() || basicHeader->isFree()
../../third_party/WebKit/Source/platform/heap/Heap.cpp(928) : void WebCore::ThreadHeap<Header>::assertEmpty() [with Header = WebCore::FinalizedHeapObjectHeader]
1   0x7f7802054dce
2   0x7f7802058ea9
3   0x7f7802058f42
4   0x7f7802f6660d
5   0x7f7802f6622c
6   0x7f7807c3db16
7   0x7f780214a0f5
8   0x7f77f9d73182
9   0x7f77f812330d clone
[2214:2324:0708/085531:WARNING:raw_channel_posix.cc(214)] recvmsg: Connection reset by peer


### th...@gmail.com (2014-07-10)

I get a different trace and can also repro this on ToT without ASAN.

ToT 282042:
Program received signal SIGSEGV, Segmentation fault.
[Switching to Thread 0x7fffdd1f5700 (LWP 12259)]
0x000055555721702c in v8::internal::HandleScope::Extend(v8::internal::Isolate*)
    ()
#0  0x000055555721702c in v8::internal::HandleScope::Extend(v8::internal::Isolate*) ()
#1  0x0000555557169a6a in v8::HandleScope::CreateHandle(v8::internal::Isolate*, v8::internal::Object*) ()
#2  0x0000555558164c47 in WebCore::V8AbstractEventListener::~V8AbstractEventListener() ()
#3  0x0000555558167177 in WebCore::V8WorkerGlobalScopeEventListener::~V8WorkerGlobalScopeEventListener() ()
#4  0x00005555575d998b in WebCore::EventTargetData::~EventTargetData() ()
#5  0x00005555581b61b0 in WebCore::IDBRequest::~IDBRequest() ()
#6  0x00005555570852b7 in WebCore::HeapPage<WebCore::FinalizedHeapObjectHeader>::sweep() ()
#7  0x0000555557085a1c in WebCore::ThreadHeap<WebCore::FinalizedHeapObjectHeader>::sweep() ()
#8  0x0000555557087755 in WebCore::ThreadState::performPendingSweep() ()
#9  0x0000555557089429 in WebCore::ThreadState::detach() ()
#10 0x0000555557a71c75 in WebCore::WorkerThread::workerThread() ()
#11 0x000055555710a721 in WTF::wtfThreadEntryPoint(void*) ()
#12 0x00007ffff3581182 in start_thread (arg=0x7fffdd1f5700)
    at pthread_create.c:312
#13 0x00007ffff193130d in clone ()
    at ../sysdeps/unix/sysv/linux/x86_64/clone.S:111

ASAN release 282042:
==7751==ERROR: AddressSanitizer: heap-use-after-free on address 0x62c00001b708 at pc 0x7f4b36f57d06 bp 0x7f4af76fc320 sp 0x7f4af76fc318
READ of size 8 at 0x62c00001b708 thread T9
    #0 0x7f4b36f57d05 in Initialize /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../v8/src/api.cc:589
    #1 0x7f4b3965d80f in ~V8AbstractEventListener /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:69
    #2 0x7f4b396628ea in ~V8WorkerGlobalScopeEventListener /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/bindings/core/v8/V8WorkerGlobalScopeEventListener.h:42
    #3 0x7f4b37a0bfb7 in destruct /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/Vector.h:64
    #4 0x7f4b37a0bd01 in finalize /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/Vector.h:596
    #5 0x7f4b37a0bc0f in deletePtr /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/OwnPtrCommon.h:52 (discriminator 3)
    #6 0x7f4b37a0bbbb in ~OwnPtr /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/OwnPtr.h:67
    #7 0x7f4b37a0ba5b in ~pair /usr/lib/gcc/x86_64-linux-gnu/4.6/../../../../include/c++/4.6/bits/stl_pair.h:87
    #8 0x7f4b37a0ce67 in destruct /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/Vector.h:64
    #9 0x7f4b37a21321 in finalize /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/Vector.h:596
    #10 0x7f4b37cc2915 in ~EventTargetWithInlineData /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/events/EventTarget.h:142
    #11 0x7f4b36cc3301 in finalize /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/heap/Heap.cpp:466
    #12 0x7f4b36cbe790 in sweep /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/heap/Heap.cpp:1083
    #13 0x7f4b36cbfd23 in sweep /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/heap/Heap.cpp:877
    #14 0x7f4b36ccbfdc in performPendingSweep /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/heap/ThreadState.cpp:857
    #15 0x7f4b36cca344 in detach /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/heap/ThreadState.cpp:408
    #16 0x7f4b385f3693 in workerThread /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/workers/WorkerThread.cpp:160
    #17 0x7f4b3ee1c6b6 in threadEntryPoint /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/Threading.cpp:69
    #18 0x7f4b36e6709e in wtfThreadEntryPoint /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/ThreadingPthreads.cpp:175
    #19 0x7f4b2b723181 in start_thread /build/buildd/eglibc-2.19/nptl/pthread_create.c:312 (discriminator 2)
    #20 0x7f4b2929e30c in clone /build/buildd/eglibc-2.19/misc/../sysdeps/unix/sysv/linux/x86_64/clone.S:111

0x62c00001b708 is located 13576 bytes inside of 31504-byte region [0x62c000018200,0x62c00001fd10)
freed by thread T9 here:
    #0 0x7f4b33395b6b in operator delete _asan_rtl_ (discriminator 2)
    #1 0x7f4b3727ac25 in TearDown /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../v8/src/isolate.cc:1528 (discriminator 1)
    #2 0x7f4b36cca07e in cleanup /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/heap/ThreadState.cpp:389
    #3 0x7f4b36cca2eb in detach /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/heap/ThreadState.cpp:397
    #4 0x7f4b385f3693 in workerThread /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/workers/WorkerThread.cpp:160
    #5 0x7f4b3ee1c6b6 in threadEntryPoint /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/Threading.cpp:69
    #6 0x7f4b36e6709e in wtfThreadEntryPoint /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/ThreadingPthreads.cpp:175
    #7 0x7f4b2b723181 in start_thread /build/buildd/eglibc-2.19/nptl/pthread_create.c:312 (discriminator 2)

### tk...@chromium.org (2014-07-10)

#13, the assertion failure is not a serious one.  We'll fix it by https://codereview.chromium.org/371623002/ .

#14,
This issue happens in WorkerRunLoop::run(), and #14 happens in a worker thread shutdown.  I think they are different.  However It looks another serious issue, and looks related to the bindings layer.


### ha...@chromium.org (2014-07-10)

Regarding #14, it looks strange. We're crashing at the point where we allocate a new V8 handle in ~V8AbstractEventListener() while doing ThreadState::detach(). At this point V8 is guaranteed to be alive, and I have no idea why allocating a new V8 handle leads to a crash.

Can you reproduce the crash?


### cl...@chromium.org (2014-07-10)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5968287466782720

Fuzzer: Therealholden_worker
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x62c000053708
Crash State:
  - crash stack -
  v8::HandleScope::Initialize
  WebCore::V8AbstractEventListener::~V8AbstractEventListener
  - free stack -
  v8::internal::Isolate::TearDown
  WebCore::ThreadState::cleanup
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=281998:282042

Minimized Testcase (2.18 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96Cvj9lDMO22bxITLIxTdNA46wOYaMwGTgCKcNse2-VXVxC9_zyHLqKxlHrSTmYY7R9qLgBtstUQXeWsiqmRkA5GI7uzRZsjvAXXnzjFtPW0Zb-ML_kofwwTnahTBlY_jdxKxLra-w9kntXdzcDxysPNMZMdg
Filer: inferno@chromium.org

### ha...@chromium.org (2014-07-11)

I was able to reproduce the crash of #14 with the test case in #17. I'll handle this.


### ha...@chromium.org (2014-07-11)

OK, I found the cause (but I was wrong that I was able to reproduce the crash; I cannot reproduce the crash).

The problem is that a thread can get involved in a GC after the thread is detached. Specifically:

(1) Thread::detach() is called. Thread::detach() calls Thread::cleanup().
(2) Thread::cleanup() destroys V8.
(3) Thread::detach() enters a safe point. It can get involved in a GC.
(4) The GC destructs V8AbstractEventListener. The destructor tries to allocate a V8 HandleScope and crashes.

Ideally all garbage on the thread heap should be collected in cleanup(). However, that's not the case in reality since the thread can fail in stopping other threads in cleanup(). Then the destruction of the V8AbstractEventListener is delayed to (4) and then we hit the crash.

wibling's change will fix this issue, so shall we just wait for the wibling's change? Or shall we make Thread::detach() not enter a safe point after cleanup()? (As we discussed before, not entering a safe point will cause a potential dead lock. The dead lock will be resolved by the GC time out.)


### tk...@chromium.org (2014-07-11)

> (2) Thread::cleanup() destroys V8.

How is V8 destroyed?  Does a destructor of on-heap objects destroy V8?

> wibling's change will fix this issue, 

I don't understand why it will fix this.  This is a destruction order issue, right?  Is it ok to destroy V8AbstractEventListener in non-originator thread?


### ha...@chromium.org (2014-07-11)

> How is V8 destroyed?  Does a destructor of on-heap objects destroy V8?

V8 is destroyed in IsolateCleanupTask::postCleanup() in WorkerScriptController.cpp. This is executed at the end of ThreadState::cleanup().

> I don't understand why it will fix this.  This is a destruction order issue, right?  Is it ok to destroy V8AbstractEventListener in non-originator thread?

No, the issue is not related to destruction order. The issue is that a GC can be triggered after V8's isolate is disposed and the GC can call destructors on objects on the thread heap.

After wibling's change, all pages on the thread heap will be moved to orphaned pages at the end of cleanup(). So even if a GC is triggered after cleanup(), the GC won't call any destructor on objects on the thread heap. So the crash won't happen, I guess.


### ag...@chromium.org (2014-07-11)

Thanks for the analysis Haraken. As you state, Gustav's change has the machinery to fix this and if we get Gustav's change right the scenario you outline here should not happen (all objects that can be finalized on worker thread pages will have been finalized). We should make sure to get Gustav's change in soon. :)



### ha...@chromium.org (2014-07-11)

Agreed. My concern is whether we need to merge the fix to already released branches. If we need the merge, we need to create a CL that doesn't rely on wibling's change.

tkent-san: Do you have an idea about whether the merge is needed or not?


### ag...@chromium.org (2014-07-11)

Can we move the post cleanup callbacks to after we detach the thread state? Where we detach the thread state should be the last place where we reach a safepoint on this thread. After that, this thread should never take part in GC (or touch Blink objects) again and it should be safe to shutdown V8.

### tk...@chromium.org (2014-07-11)

ok, I understand the wibling's change will fix the V8 shutdown issue.

[1], which is a fix for https://crbug.com/chromium/388267, exposed the V8 shutdown issue.  So, if we don't merge [1] to branches, we don't need to merge the wiblings's change for this issue.

According to [2], https://crbug.com/chromium/388267 is not vulnerable.  So merging nothing is safer.
If we have a lot of crash reports for M37 branch, disabling Oilpan for IDB would be reasonable.

[1] http://src.chromium.org/viewvc/blink?view=revision&revision=177723
[2] https://code.google.com/p/chromium/issues/detail?id=388267#c35


### ha...@chromium.org (2014-07-11)

> Can we move the post cleanup callbacks to after we detach the thread state? Where we detach the thread state should be the last place where we reach a safepoint on this thread. After that, this thread should never take part in GC (or touch Blink objects) again and it should be safe to shutdown V8.

Sounds like a nice idea. I'll prepare a CL. We can merge it if necessary.


### bu...@chromium.org (2014-07-11)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=177923

------------------------------------------------------------------
r177923 | haraken@chromium.org | 2014-07-11T10:33:33.705529Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/heap/ThreadState.cpp?r1=177923&r2=177922&pathrev=177923
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/heap/ThreadState.h?r1=177923&r2=177922&pathrev=177923

Defer calling ThreadState::postCleanup after leaving the final safe point

ThreadState::postCleanup should be called after it's guaranteed that the thread will never get involved in a GC. (See https://code.google.com/p/chromium/issues/detail?id=388294#c19 for what happens if we don't guarantee the order.) To guarantee the order, this CL moves ThreadState::postCleanup after the thread leaves the final safe point.

(FYI, the only user of the postCleanup task is WorkerScriptController.)

BUG=388294

Review URL: https://codereview.chromium.org/383093002
-----------------------------------------------------------------

### in...@chromium.org (2014-07-15)

This is fixed, but now manifesting as https://code.google.com/p/chromium/issues/detail?id=393744

### cl...@chromium.org (2014-07-15)

[Empty comment from Monorail migration]

### tk...@chromium.org (2014-07-18)

I'd like to merge the fix for https://crbug.com/chromium/388267 and the fix for this.


### am...@google.com (2014-07-23)


Please note that all merge requests must have been on or rolled into trunk
for at least 24 hours to be considered for merging (to ensure full bot
coverage and give an opportunity for any necessary reverts to occur).

To help facilitate this request, if you could please answer the following:
--------------------------------------------------------------------------
1) Has this change been on trunk for at least 24 hours?

2) Has this change shipped to at least one canary release (where applicable)?

3) Has anyone verified that these changes resolve the issue and cause no new
   crashes?

4) Why is this necessary for this milestone?

Thanks!

(this message is auto-generated each time the merge-request label is
applied; if you have previously answered these questions kindly disregard)


### am...@chromium.org (2014-07-28)

merge approved for m37 branch 2062

### bu...@chromium.org (2014-07-29)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=179071

------------------------------------------------------------------
r179071 | tkent@chromium.org | 2014-07-29T00:01:14.745595Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2062/Source/platform/heap/ThreadState.h?r1=179071&r2=179070&pathrev=179071
   M http://src.chromium.org/viewvc/blink/branches/chromium/2062/Source/platform/heap/ThreadState.cpp?r1=179071&r2=179070&pathrev=179071

Merge 177923 "Defer calling ThreadState::postCleanup after leavi..."

> Defer calling ThreadState::postCleanup after leaving the final safe point
> 
> ThreadState::postCleanup should be called after it's guaranteed that the thread will never get involved in a GC. (See https://code.google.com/p/chromium/issues/detail?id=388294#c19 for what happens if we don't guarantee the order.) To guarantee the order, this CL moves ThreadState::postCleanup after the thread leaves the final safe point.
> 
> (FYI, the only user of the postCleanup task is WorkerScriptController.)
> 
> BUG=388294
> 
> Review URL: https://codereview.chromium.org/383093002

TBR=haraken@chromium.org

Review URL: https://codereview.chromium.org/422213002
-----------------------------------------------------------------

### mb...@chromium.org (2014-08-28)

Thanks for the fuzzer contribution! This report qualifies for a $1000 reward.

### ti...@chromium.org (2014-09-18)

[Empty comment from Monorail migration]

### ti...@google.com (2014-10-07)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you. Thanks again for your help!


### cl...@chromium.org (2014-10-21)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/388294?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079893)*
