# malloc_consolidate(): unaligned fastbin chunk detected in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [326607001](https://issues.chromium.org/issues/326607001) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript, Infra>Client>V8 |
| **Platforms** | Linux |
| **Reporter** | wh...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2024-02-24 |
| **Bounty** | $7,000.00 |

## Description

Security Bug

Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md

Please see the following link for instructions on filing security bugs: https://www.chromium.org/Home/chromium-security/reporting-security-bugs

Reports may be eligible for reward payments under the Chrome VRP: https://g.co/chrome/vrp

NOTE: Security bugs are normally made public once a fix has been widely deployed.

-------------------------

VULNERABILITY DETAILS
Hi, I found a crash which show `malloc_consolidate(): unaligned fastbin chunk detected`, I try to get stack info. 

[Thread 0x7fabe0ffb6c0 (LWP 22913) exited]
malloc_consolidate(): unaligned fastbin chunk detected

Thread 52 "WorkerThread" received signal SIGABRT, Aborted.
[Switching to Thread 0x7fabe1ffd6c0 (LWP 22907)]
0x00007facbfc7756c in ?? () from /lib64/libc.so.6
#0  0x00007facbfc7756c in ?? () from /lib64/libc.so.6
#1  0x00007facbfc28602 in raise () from /lib64/libc.so.6
#2  0x00007facbfc114ed in abort () from /lib64/libc.so.6
#3  0x00007facbfc125a8 in ?? () from /lib64/libc.so.6
#4  0x00007facbfc80ee5 in ?? () from /lib64/libc.so.6
#5  0x00007facbfc81a2c in ?? () from /lib64/libc.so.6
#6  0x00007facbfc840a8 in ?? () from /lib64/libc.so.6
#7  0x00007facbfc85359 in malloc () from /lib64/libc.so.6
#8  0x0000555c6a2ab489 in operator_new_impl ()
    at ../../third_party/libc++/src/src/new.cpp:33
#9  operator new () at ../../third_party/libc++/src/src/new.cpp:46
#10 0x0000555c6715cffd in __libcpp_operator_new<unsigned long> ()
    at ../../third_party/libc++/src/include/new:271
#11 __libcpp_allocate () at ../../third_party/libc++/src/include/new:295
#12 allocate ()
    at ../../third_party/libc++/src/include/__memory/allocator.h:125
#13 allocate ()
    at ../../third_party/libc++/src/include/__memory/allocator_traits.h:281
#14 __add_back_capacity ()
    at ../../third_party/libc++/src/include/deque:2169
#15 0x0000555c6715cdf2 in emplace_back<int, unsigned long&> ()
    at ../../third_party/libc++/src/include/deque:1590
#16 0x0000555c6715caf5 in emplace<int, unsigned long&> ()
    at ../../third_party/libc++/src/include/queue:411
#17 IndexGenerator () at ../../src/heap/index-generator.cc:13
#18 0x0000555c6719b2d9 in PointersUpdatingJob ()
    at ../../src/heap/mark-compact.cc:4606
#19 make_unique<v8::internal::PointersUpdatingJob, v8::internal::Isolate*, v8::internal::MarkCompactCollector*, std::__Cr::vector<std::__Cr::unique_ptr<v8::internal::UpdatingItem, std::__Cr::default_delete<v8::internal::UpdatingItem> >, std::__Cr::allocator<std::__Cr::unique_ptr<v8::internal::UpdatingItem, std::__Cr::default_delete<v8::internal::UpdatingItem> > > > > ()
    at ../../third_party/libc++/src/include/__memory/unique_ptr.h:597
#20 UpdatePointersAfterEvacuation () at ../../src/heap/mark-compact.cc:5097
#21 0x0000555c6717bddd in Evacuate () at ../../src/heap/mark-compact.cc:4536
#22 0x0000555c671747bd in CollectGarbage ()
    at ../../src/heap/mark-compact.cc:418
#23 0x0000555c67078426 in MarkCompact () at ../../src/heap/heap.cc:2717
#24 0x0000555c67076c43 in PerformGarbageCollection ()
    at ../../src/heap/heap.cc:2403
#25 0x0000555c670b5ffc in operator() () at ../../src/heap/heap.cc:1870
#26 0x0000555c6707002c in SetMarkerIfNeededAndCallback<(lambda at ../../src/heap/heap.cc:1834:40)> () at ../../src/heap/base/stack.h:64
#27 CollectGarbage () at ../../src/heap/heap.cc:1834
#28 0x0000555c67075c94 in CollectAllGarbage ()
    at ../../src/heap/heap.cc:1514
#29 CollectGarbageForBackground () at ../../src/heap/heap.cc:2237
#30 0x0000555c67165a57 in ParkSlowPath ()
    at ../../src/heap/local-heap.cc:231
#31 0x0000555c66d15ccf in Park () at ../../src/heap/local-heap.h:319
#32 ParkedScope () at ../../src/heap/parked-scope.h:24
#33 ParkAndExecuteCallback<(lambda at ../../src/compiler-dispatcher/optimizing-compile-dispatcher.cc:148:9)> () at ../../src/heap/local-heap-inl.h:64
#34 operator() () at ../../src/heap/local-heap-inl.h:85
#35 0x0000555c66d15c0e in void heap::base::Stack::SetMarkerAndCallbackImpl<v8::internal::LocalHeap::BlockMainThreadWhileParked<v8::internal::OptimizingCompileDispatcher::AwaitCompileTasks()::$_0>(v8::internal::OptimizingCompileDispatcher::AwaitCompileTasks()::$_0)::{lambda()#1}>(heap::base::Stack*, void*, void const*) () at ../../src/heap/base/stack.h:95
#36 0x0000555c68ae5a97 in PushAllRegistersAndIterateStack ()
#37 0x0000555c66d13ad9 in SetMarkerIfNeededAndCallback<(lambda at ../../src/heap/local-heap-inl.h:85:7)> () at ../../src/heap/base/stack.h:60
#38 ExecuteWithStackMarker<(lambda at ../../src/heap/local-heap-inl.h:85:7)>
    () at ../../src/heap/local-heap-inl.h:95
#39 BlockMainThreadWhileParked<(lambda at ../../src/compiler-dispatcher/optimizing-compile-dispatcher.cc:148:9)> () at ../../src/heap/local-heap-inl.h:84
#40 BlockMainThreadWhileParked<(lambda at ../../src/compiler-dispatcher/optimizing-compile-dispatcher.cc:148:9)> ()
    at ../../src/execution/local-isolate-inl.h:37
#41 AwaitCompileTasks ()
    at ../../src/compiler-dispatcher/optimizing-compile-dispatcher.cc:147
#42 0x0000555c66d13e32 in FlushQueues ()
    at ../../src/compiler-dispatcher/optimizing-compile-dispatcher.cc:163
#43 Stop ()
    at ../../src/compiler-dispatcher/optimizing-compile-dispatcher.cc:179
#44 0x0000555c66ebd81a in Deinit () at ../../src/execution/isolate.cc:3832
#45 0x0000555c66ebd29e in Delete () at ../../src/execution/isolate.cc:3536
#46 0x0000555c66800915 in ExecuteInThread () at ../../src/d8/d8.cc:4778
#47 0x0000555c667ffeb7 in Run () at ../../src/d8/d8.cc:4538
#48 0x0000555c668bea99 in NotifyStartedAndRun ()
    at ../../src/base/platform/platform.h:613
#49 ThreadEntry () at ../../src/base/platform/platform-posix.cc:1189
#50 0x00007facbfc7583c in ?? () from /lib64/libc.so.6
#51 0x00007facbfce7838 in ?? () from /lib64/libc.so.6

attachment file is full log 


VERSION
Chrome Version: [x.x.x.x] + [stable, beta, or dev]
Operating System: [Please indicate OS, version, and service pack level]

REPRODUCTION CASE

run d8 with 
--expose-gc --omit-quit --allow-natives-syntax --fuzzing --jit-fuzzing --future --harmony --maglev-assert --optimize-for-size --stress-concurrent-allocation --stress-incremental-marking

PoC is 1.js file 

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [tab, browser, etc.]
Crash State: [see link above: stack trace *with symbols*, registers, exception record]
Client ID (if relevant): [see link above]

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: [goes here]

## Attachments

- [log-MolyzKYx69-11log166](attachments/log-MolyzKYx69-11log166) (application/octet-stream, 8.1 KB)
- [1.js](attachments/1.js) (text/javascript, 819 B)
- [2.js](attachments/2.js) (text/javascript, 1.6 KB)

## Timeline

### wh...@gmail.com (2024-02-24)

and I also can get a dcheck, maybe helpful 

#
# Fatal error in ../../src/base/region-allocator.cc, line 63
# Debug check failed: (*iter)->contains(address).
#
#
#
#FailureMessage Object: 0x7f260cff85f0
==== C stack trace ===============================

    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-92494/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f264d2e4853]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-92494/libv8_libplatform.so(+0x192cd) [0x7f264d28d2cd]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-92494/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x17e) [0x7f264d2c5b6e]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-92494/libv8_libbase.so(+0x2b5b5) [0x7f264d2c55b5]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-92494/libv8_libbase.so(v8::base::RegionAllocator::FindRegion(unsigned long)+0xea) [0x7f264d2d8e4a]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-92494/libv8_libbase.so(v8::base::RegionAllocator::TrimRegion(unsigned long, unsigned long)+0x35) [0x7f264d2d9ff5]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-92494/libv8_libbase.so(v8::base::BoundedPageAllocator::FreePages(void*, unsigned long)+0x32) [0x7f264d2ba842]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-92494/libv8.so(v8::internal::VirtualMemory::Free()+0x96) [0x7f264b864a56]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-92494/libv8.so(v8::internal::MemoryAllocator::Pool::ReleasePooledChunks()+0x6b) [0x7f264adee34b]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-92494/libv8.so(v8::internal::MemoryAllocator::TearDown()+0x13) [0x7f264adee253]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-92494/libv8.so(v8::internal::Heap::TearDown()+0x64f) [0x7f264ad3f1af]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-92494/libv8.so(v8::internal::Isolate::Deinit()+0x517) [0x7f264ab67127]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-92494/libv8.so(v8::internal::Isolate::Delete(v8::internal::Isolate*)+0xaa) [0x7f264ab66afa]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-92494/d8(v8::Worker::ExecuteInThread()+0x695) [0x5572805c5405]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-92494/d8(v8::Worker::WorkerThread::Run()+0x28) [0x5572805c4d28]
    /home/uuu/asan/d8_debug_zip/d8-linux-debug-v8-component-92494/libv8_libbase.so(+0x495e8) [0x7f264d2e35e8]
    /lib64/libc.so.6(+0x8683c) [0x7f2647ae483c]
    /lib64/libc.so.6(+0xf8838) [0x7f2647b56838]
Received signal 6

and 
// Received signal 11 SEGV_MAPERR 0007fdc1c0b8
// 
// ==== C stack trace ===============================
// 
//  [0x55f3753d13b2]
//  [0x7fddd77cf520]
//  [0x7fddd782e89e]
//  [0x7fddd7830bdb]
//  [0x7fddd7832139]
//  [0x55f3787f2489]
//  [0x55f375af05ad]



### wh...@gmail.com (2024-02-27)

some reproduce tips: 
When reproducing（run a loop), it is best to compile a d8, which can increase the reproduction efficiency.

### pe...@google.com (2024-02-27)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-02-27)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### sa...@google.com (2024-02-28)

Managed to reproduce this in an ASan build, which contains some useful information:

```
=================================================================                                                                                                                                                                                                                                                                                                 [184/9310]
==3747180==ERROR: AddressSanitizer: heap-use-after-free on address 0x5020000125b0 at pc 0x5594604c9ef3 bp 0x7ff0b76be250 sp 0x7ff0b76be248                                                                                                                                                                                                                                  
WRITE of size 8 at 0x5020000125b0 thread T50 (WorkerThread)                                                                                                                           
    #0 0x5594604c9ef2 in v8::internal::GlobalHandles::Node::ResetPhantomHandle() src/handles/global-handles.cc:564:13                                                                 
    #1 0x5594604c9ef2 in v8::internal::GlobalHandles::ResetWeakNodeIfDead(v8::internal::GlobalHandles::Node*, bool (*)(v8::internal::Heap*, v8::internal::FullObjectSlot)) src/handles/global-handles.cc:700:13                                                                                                                                                             
    #2 0x5594604c9ef2 in v8::internal::GlobalHandles::IterateWeakRootsForPhantomHandles(bool (*)(v8::internal::Heap*, v8::internal::FullObjectSlot)) src/handles/global-handles.cc:715:33                                                                                                                                                                                   
    #3 0x5594606ce07d in v8::internal::MarkCompactCollector::ClearNonLiveReferences() src/heap/mark-compact.cc:2840:32                                                                                                                                                                                                                                                      
    #4 0x5594606c5ead in v8::internal::MarkCompactCollector::CollectGarbage() src/heap/mark-compact.cc:413:3                                                                                                                                                                                                                                                                
    #5 0x55946065480d in v8::internal::Heap::MarkCompact() src/heap/heap.cc:2728:29                                                                                                                                                                                                                                                                                         
    #6 0x559460652789 in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const*) src/heap/heap.cc:2414:5                                                                                                                                                                                           
    #7 0x5594606974f1 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)::$_1::operator()() const src/heap/heap.cc:1877:9                                                                                                                                                                     
    #8 0x559460645ada in void heap::base::Stack::SetMarkerIfNeededAndCallback<v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)::$_1>(v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)::$_1) src/heap/base/stack.h:
64:7                                                                                                                                                                                                                                                                                                                                                                        
    #9 0x559460645ada in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) src/heap/heap.cc:1841:11                                                                                                                                                                                             
    #10 0x5594606b65ee in v8::internal::LocalHeap::ParkSlowPath() src/heap/local-heap.cc:231:18                                                                                       
    #11 0x5594602ed461 in v8::internal::LocalHeap::Park() src/heap/local-heap.h:319:7                                                                                                                                                                                                                                                                                       
    #12 0x5594602ed461 in v8::internal::ParkedScope::ParkedScope(v8::internal::LocalHeap*) src/heap/parked-scope.h:24:18                                                              
    #13 0x5594602ed461 in void v8::internal::LocalHeap::ParkAndExecuteCallback<v8::internal::OptimizingCompileDispatcher::AwaitCompileTasks()::$_0>(v8::internal::OptimizingCompileDispatcher::AwaitCompileTasks()::$_0) src/heap/local-heap-inl.h:64:15                                                                                                                    
    #14 0x5594602ed461 in void v8::internal::LocalHeap::BlockMainThreadWhileParked<v8::internal::OptimizingCompileDispatcher::AwaitCompileTasks()::$_0>(v8::internal::OptimizingCompileDispatcher::AwaitCompileTasks()::$_0)::'lambda'()::operator()() const src/heap/local-heap-inl.h:85:28                                                                                
    #15 0x5594602ed461 in void heap::base::Stack::SetMarkerAndCallbackImpl<void v8::internal::LocalHeap::BlockMainThreadWhileParked<v8::internal::OptimizingCompileDispatcher::AwaitCompileTasks()::$_0>(v8::internal::OptimizingCompileDispatcher::AwaitCompileTasks()::$_0)::'lambda'()>(heap::base::Stack*, void*, void const*) src/heap/base/stack.h:95:5               
    #16 0x5594621be9d2 in PushAllRegistersAndIterateStack push_registers_asm.cc                                                                                                       
    #17 0x5594602e8ca2 in void heap::base::Stack::SetMarkerIfNeededAndCallback<void v8::internal::LocalHeap::BlockMainThreadWhileParked<v8::internal::OptimizingCompileDispatcher::AwaitCompileTasks()::$_0>(v8::internal::OptimizingCompileDispatcher::AwaitCompileTasks()::$_0)::'lambda'()>(v8::internal::OptimizingCompileDispatcher::AwaitCompileTasks()::$_0) src/heap
/base/stack.h:60:7                                                                                                                                                                    
    #18 0x5594602e8ca2 in void v8::internal::LocalHeap::ExecuteWithStackMarker<void v8::internal::LocalHeap::BlockMainThreadWhileParked<v8::internal::OptimizingCompileDispatcher::AwaitCompileTasks()::$_0>(v8::internal::OptimizingCompileDispatcher::AwaitCompileTasks()::$_0)::'lambda'()>(v8::internal::OptimizingCompileDispatcher::AwaitCompileTasks()::$_0) src/heap
/local-heap-inl.h:95:19                                                                                                                                                                                                                                                                                                                                                     
    #19 0x5594602e8ca2 in void v8::internal::LocalHeap::BlockMainThreadWhileParked<v8::internal::OptimizingCompileDispatcher::AwaitCompileTasks()::$_0>(v8::internal::OptimizingCompileDispatcher::AwaitCompileTasks()::$_0) src/heap/local-heap-inl.h:84:3                                                                                                                     #20 0x5594602e8ca2 in void v8::internal::LocalIsolate::BlockMainThreadWhileParked<v8::internal::OptimizingCompileDispatcher::AwaitCompileTasks()::$_0>(v8::internal::OptimizingCompileDispatcher::AwaitCompileTasks()::$_0) src/execution/local-isolate-inl.h:37:9                                                                                                      
    #21 0x5594602e8ca2 in v8::internal::OptimizingCompileDispatcher::AwaitCompileTasks() src/compiler-dispatcher/optimizing-compile-dispatcher.cc:147:44                                                                                                                                                                                                                    
    #22 0x5594602e919f in v8::internal::OptimizingCompileDispatcher::FlushQueues(v8::internal::BlockingBehavior, bool) src/compiler-dispatcher/optimizing-compile-dispatcher.cc:163:54                                                                                                                                                                                      
    #23 0x5594602e950c in v8::internal::OptimizingCompileDispatcher::Stop() src/compiler-dispatcher/optimizing-compile-dispatcher.cc:179:3                                                                                                                                                                                                                                  
    #24 0x559460455585 in v8::internal::Isolate::Deinit() src/execution/isolate.cc:3851:37                                                                                            
    #25 0x559460454d1f in v8::internal::Isolate::Delete(v8::internal::Isolate*) src/execution/isolate.cc:3555:12                                                                                                                                                                                                                                                            
    #26 0x55945fefcefd in v8::Worker::ExecuteInThread() src/d8/d8.cc:4795:13                                                                                                                                                                                                                                                                                                
    #27 0x55945fefc059 in v8::Worker::WorkerThread::Run() src/d8/d8.cc:4555:11                                                                                                                                                                                                                                                                                              
    #28 0x559463eb7d08 in v8::base::Thread::NotifyStartedAndRun() src/base/platform/platform.h:613:5                                                                                  
    #29 0x559463eb7d08 in v8::base::ThreadEntry(void*) src/base/platform/platform-posix.cc:1189:11                                                                                                                                                                                                                                                                          
    #30 0x55945fe676a8 in asan_thread_start(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:239:28                                                                                                                                                                                                                           
                                                                                                                                                                                                                                                                                                                                                                            
0x5020000125b0 is located 0 bytes inside of 8-byte region [0x5020000125b0,0x5020000125b8)                                                                                                                                                                                                                                                                                   
freed by thread T50 (WorkerThread) here:                                                                                                                                                                                                                                                                                                                                    
    #0 0x55945fe9df7d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:143:3                                                                                                                                                                                                                                 
    #1 0x559462020489 in std::__Cr::default_delete<unsigned long*>::operator()(unsigned long**) const third_party/libc++/src/include/__memory/unique_ptr.h:68:5                       
    #2 0x559462020489 in std::__Cr::unique_ptr<unsigned long*, std::__Cr::default_delete<unsigned long*>>::reset(unsigned long**) third_party/libc++/src/include/__memory/unique_ptr.h:279:7                                                                                                                                                                                
    #3 0x559462020489 in std::__Cr::unique_ptr<unsigned long*, std::__Cr::default_delete<unsigned long*>>::~unique_ptr() third_party/libc++/src/include/__memory/unique_ptr.h:249:71  
    #4 0x559462020489 in v8::internal::wasm::(anonymous namespace)::ClearWeakScriptHandleTask::~ClearWeakScriptHandleTask() src/wasm/wasm-engine.cc:129:7                             
    #5 0x559462020489 in v8::internal::wasm::(anonymous namespace)::ClearWeakScriptHandleTask::~ClearWeakScriptHandleTask() src/wasm/wasm-engine.cc:129:7                                                                                                                                                                                                                   
    #6 0x559462020489 in non-virtual thunk to v8::internal::wasm::(anonymous namespace)::ClearWeakScriptHandleTask::~ClearWeakScriptHandleTask() src/wasm/wasm-engine.cc                                                                                                                                                                                                    
    #7 0x559463ec4f9e in std::__Cr::default_delete<v8::Task>::operator()(v8::Task*) const third_party/libc++/src/include/__memory/unique_ptr.h:68:5                                                                                                                                                                                                                         
    #8 0x559463ec4f9e in std::__Cr::unique_ptr<v8::Task, std::__Cr::default_delete<v8::Task>>::reset(v8::Task*) third_party/libc++/src/include/__memory/unique_ptr.h:279:7                                                                                                                                                                                                  
    #9 0x559463ec4f9e in std::__Cr::unique_ptr<v8::Task, std::__Cr::default_delete<v8::Task>>::~unique_ptr() third_party/libc++/src/include/__memory/unique_ptr.h:249:71                                                                                                                                                                                                    
    #10 0x559463ec4f9e in std::__Cr::pair<v8::platform::DefaultForegroundTaskRunner::Nestability, std::__Cr::unique_ptr<v8::Task, std::__Cr::default_delete<v8::Task>>>::~pair() third_party/libc++/src/include/__utility/pair.h:79:29                                                                                                                                      
    #11 0x559463ec4f9e in void std::__Cr::__destroy_at<std::__Cr::pair<v8::platform::DefaultForegroundTaskRunner::Nestability, std::__Cr::unique_ptr<v8::Task, std::__Cr::default_delete<v8::Task>>>, 0>(std::__Cr::pair<v8::platform::DefaultForegroundTaskRunner::Nestability, std::__Cr::unique_ptr<v8::Task, std::__Cr::default_delete<v8::Task>>>*) third_party/libc++/
src/include/__memory/construct_at.h:67:11                                                                                                                                                                                                                                                                                                                                   
    #12 0x559463ec4f9e in void std::__Cr::allocator_traits<std::__Cr::allocator<std::__Cr::pair<v8::platform::DefaultForegroundTaskRunner::Nestability, std::__Cr::unique_ptr<v8::Task, std::__Cr::default_delete<v8::Task>>>>>::destroy<std::__Cr::pair<v8::platform::DefaultForegroundTaskRunner::Nestability, std::__Cr::unique_ptr<v8::Task, std::__Cr::default_delete<v
8::Task>>>, void, 0>(std::__Cr::allocator<std::__Cr::pair<v8::platform::DefaultForegroundTaskRunner::Nestability, std::__Cr::unique_ptr<v8::Task, std::__Cr::default_delete<v8::Task>>>>&, std::__Cr::pair<v8::platform::DefaultForegroundTaskRunner::Nestability, std::__Cr::unique_ptr<v8::Task, std::__Cr::default_delete<v8::Task>>>*) third_party/libc++/src/include/__
memory/allocator_traits.h:340:5                                                                                                                                                       
    #13 0x559463ec4f9e in std::__Cr::deque<std::__Cr::pair<v8::platform::DefaultForegroundTaskRunner::Nestability, std::__Cr::unique_ptr<v8::Task, std::__Cr::default_delete<v8::Task>>>, std::__Cr::allocator<std::__Cr::pair<v8::platform::DefaultForegroundTaskRunner::Nestability, std::__Cr::unique_ptr<v8::Task, std::__Cr::default_delete<v8::Task>>>>>::pop_front() 
third_party/libc++/src/include/deque:2268:3                                                                                                                                           
    #14 0x559463ec4bc7 in v8::platform::DefaultForegroundTaskRunner::Terminate() src/libplatform/default-foreground-task-runner.cc:45:50                                                                                                                                                                                                                                    
    #15 0x559463ebc101 in v8::platform::DefaultPlatform::NotifyIsolateShutdown(v8::Isolate*) src/libplatform/default-platform.cc:302:15                                                                                                                                                                                                                                     
    #16 0x55945fefcea5 in v8::Worker::ExecuteInThread() src/d8/d8.cc:4792:5                                                                                                                                                                                                                                                                                                 
    #17 0x55945fefc059 in v8::Worker::WorkerThread::Run() src/d8/d8.cc:4555:11                                                                                                        
    #18 0x559463eb7d08 in v8::base::Thread::NotifyStartedAndRun() src/base/platform/platform.h:613:5                                                                                  
    #19 0x559463eb7d08 in v8::base::ThreadEntry(void*) src/base/platform/platform-posix.cc:1189:11                                                                                    
    #20 0x55945fe676a8 in asan_thread_start(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:239:28                                     

previously allocated by thread T50 (WorkerThread) here:                                                                                                                                                                                                                                                                                                                     
    #0 0x55945fe9d71d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:86:3                                                                                                                                                                                                                             
    #1 0x55946200601d in std::__Cr::__unique_if<unsigned long*>::__unique_single std::__Cr::make_unique<unsigned long*, unsigned long*>(unsigned long*&&) third_party/libc++/src/include/__memory/unique_ptr.h:621:26                                                                                                                                                       
    #2 0x55946200601d in v8::internal::wasm::(anonymous namespace)::WeakScriptHandle::WeakScriptHandle(v8::internal::Handle<v8::internal::Script>, v8::internal::Isolate*) src/wasm/wasm-engine.cc:161:17                                                                                                                                                                   
    #3 0x5594620049c2 in v8::internal::wasm::WasmEngine::SyncCompileTranslatedAsmJs(v8::internal::Isolate*, v8::internal::wasm::ErrorThrower*, v8::internal::wasm::ModuleWireBytes, v8::internal::Handle<v8::internal::Script>, v8::base::Vector<unsigned char const>, v8::internal::Handle<v8::internal::HeapNumber>, v8::internal::LanguageMode) src/wasm/wasm-engine.cc:5
81:44                                                                                                                                                                                 
    #4 0x559461a4b0ba in v8::internal::AsmJsCompilationJob::FinalizeJobImpl(v8::internal::Handle<v8::internal::SharedFunctionInfo>, v8::internal::Isolate*) src/asmjs/asm-js.cc:273:13                                                                                                                                                                                      
    #5 0x5594602786b7 in v8::internal::UnoptimizedCompilationJob::FinalizeJob(v8::internal::Handle<v8::internal::SharedFunctionInfo>, v8::internal::Isolate*) src/codegen/compiler.cc:419:22                                                                                                                                                                                
    #6 0x5594602786b7 in v8::internal::CompilationJob::Status v8::internal::(anonymous namespace)::FinalizeSingleUnoptimizedCompilationJob<v8::internal::Isolate>(v8::internal::UnoptimizedCompilationJob*, v8::internal::Handle<v8::internal::SharedFunctionInfo>, v8::internal::Isolate*, std::__Cr::vector<v8::internal::FinalizeUnoptimizedCompilationData, std::__Cr::a
llocator<v8::internal::FinalizeUnoptimizedCompilationData>>*) src/codegen/compiler.cc:799:40                                                                                          
    #7 0x5594602619fc in bool v8::internal::(anonymous namespace)::IterativelyExecuteAndFinalizeUnoptimizedCompilationJobs<v8::internal::Isolate>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::SharedFunctionInfo>, v8::internal::Handle<v8::internal::Script>, v8::internal::ParseInfo*, v8::internal::AccountingAllocator*, v8::internal::IsCompiledScope*, 
std::__Cr::vector<v8::internal::FinalizeUnoptimizedCompilationData, std::__Cr::allocator<v8::internal::FinalizeUnoptimizedCompilationData>>*, std::__Cr::vector<v8::internal::DeferredFinalizationJobData, std::__Cr::allocator<v8::internal::DeferredFinalizationJobData>>*) src/codegen/compiler.cc:910:32                                                                
    #8 0x5594602604c2 in v8::internal::Compiler::Compile(v8::internal::Isolate*, v8::internal::Handle<v8::internal::SharedFunctionInfo>, v8::internal::Compiler::ClearExceptionFlag, v8::internal::IsCompiledScope*, v8::internal::CreateSourcePositions) src/codegen/compiler.cc:2642:8                                                                                    
    #9 0x55946026224d in v8::internal::Compiler::Compile(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Compiler::ClearExceptionFlag, v8::internal::IsCompiledScope*) src/codegen/compiler.cc:2697:8                                                                                                                                 
    #10 0x559461341c1d in v8::internal::__RT_impl_Runtime_CompileLazy(v8::internal::Arguments<(v8::internal::ArgumentsType)0>, v8::internal::Isolate*) src/runtime/runtime-compiler.cc:64:8                                                                                                                                                                                 
    #11 0x559461341c1d in v8::internal::Runtime_CompileLazy(int, unsigned long*, v8::internal::Isolate*) src/runtime/runtime-compiler.cc:45:1                                                                                                                                                                                                                               
    #12 0x559463c5f075 in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit setup-isolate-deserialize.cc                                                                              
    #13 0x559463bc7b60 in Builtins_CompileLazy setup-isolate-deserialize.cc                                                                                                                                                                                                                                                                                                 
    #14 0x559463bc5d5d in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc                                                                                            
    #15 0x559463bc5d5d in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc                                                                                            
    #16 0x559463bc37db in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc                                                                                                     
    #17 0x559463bc3506 in Builtins_JSEntry setup-isolate-deserialize.cc                                                                                                               
    #18 0x559460407713 in v8::internal::GeneratedCode<unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**>::Call(unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**) src/execution/simulator.h:178:12                                                                                           
    #19 0x559460407713 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:418:22                                                                                                                                                                                   
    #20 0x5594604064ef in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) src/execution/execution.cc:504:10                                                                                                                 
    #21 0x55945ff94d24 in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) src/api/api.cc:5496:7                                                                                                                                                                                                                                
    #22 0x55945fefdc42 in v8::Worker::ProcessMessage(std::__Cr::unique_ptr<v8::SerializationData, std::__Cr::default_delete<v8::SerializationData>>) src/d8/d8.cc:4666:47                                                                                                                                                                                                   
    #23 0x559463ebb942 in v8::platform::DefaultPlatform::PumpMessageLoop(v8::Isolate*, v8::platform::MessageLoopBehavior) src/libplatform/default-platform.cc:173:9                   
    #24 0x55945ff02edf in v8::(anonymous namespace)::ProcessMessages(v8::Isolate*, std::__Cr::function<v8::platform::MessageLoopBehavior ()> const&) src/d8/d8.cc:5304:19                                                                                                                                                                                                   
    #25 0x55945fef8cfe in v8::Shell::CompleteMessageLoop(v8::Isolate*) src/d8/d8.cc:5356:10                                                                                                                                                                                                                                                                                 
    #26 0x55945fef8cfe in v8::Shell::FinishExecuting(v8::Isolate*, v8::Global<v8::Context> const&) src/d8/d8.cc:5360:8                                                                
    #27 0x55945fefca2a in v8::Worker::ExecuteInThread() src/d8/d8.cc:4762:14                                                                                                                                                                                                                                                                                                
    #28 0x55945fefc059 in v8::Worker::WorkerThread::Run() src/d8/d8.cc:4555:11                                                                                                        
    #29 0x559463eb7d08 in v8::base::Thread::NotifyStartedAndRun() src/base/platform/platform.h:613:5                                                                                  
    #30 0x559463eb7d08 in v8::base::ThreadEntry(void*) src/base/platform/platform-posix.cc:1189:11                                                                                    
    #31 0x55945fe676a8 in asan_thread_start(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:239:28                                     
                                                                                                                                                                                     
Thread T50 (WorkerThread) created by T0 here:                                                                                                                                         
    #0 0x55945fe4f981 in pthread_create /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:250:3                                                 
    #1 0x559463eb7b71 in v8::base::Thread::Start() src/base/platform/platform-posix.cc:1221:14                                                                                        
    #2 0x55945feec2cf in v8::Worker::StartWorkerThread(v8::Isolate*, std::__Cr::shared_ptr<v8::Worker>, v8::base::Thread::Priority) src/d8/d8.cc:4539:16                              
    #3 0x55945feebeb2 in v8::Shell::WorkerNew(v8::FunctionCallbackInfo<v8::Value> const&) src/d8/d8.cc:2920:10                                                                        
    #4 0x559460070462 in v8::internal::FunctionCallbackArguments::Call(v8::internal::Tagged<v8::internal::CallHandlerInfo>) src/api/api-arguments-inl.h:101:3                         
    #5 0x55946006e761 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, unsigned long*, int) src/builtins/builtins-api.cc:114:
36                                                                                                                                                                                                                                                                                                                                                                          
    #6 0x55946006caf3 in v8::internal::Builtin_Impl_HandleApiConstruct(v8::internal::BuiltinArguments, v8::internal::Isolate*) src/builtins/builtins-api.cc:145:3                                                                                                                                                                                                           
    #7 0x559463c5efb5 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc                                                                                 
    #8 0x559463bc69ce in construct_stub_invoke_deopt_addr setup-isolate-deserialize.cc                                                                                                
    #9 0x559463d52f53 in Builtins_ConstructHandler setup-isolate-deserialize.cc                                                                                                                                                                                                                                                                                             
    #10 0x559463bc5d5d in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc                                                                                                                                                                                                                                                                                  
    #11 0x559463bc37db in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc                                                                                                     
    #12 0x559463bc3506 in Builtins_JSEntry setup-isolate-deserialize.cc                                                                                                                                                                                                                                                                                                     
    #13 0x559460407713 in v8::internal::GeneratedCode<unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**>::Call(unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**) src/execution/simulator.h:178:12                                                                                           
    #14 0x559460407713 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:418:22                                                                                                                                                                                   
    #15 0x55946040a026 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>) src/execution/execution.cc:515:10                                                                                                             
    #16 0x55945ff4b1ae in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2154:7                                                                                                                                                                                                                                                                
    #17 0x55945fed0004 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:965:44                                                                                                                                                                                     
    #18 0x55945fef9428 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:4415:10                                                                                                 
    #19 0x55945ff024ab in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:5244:37                                                                                          
    #20 0x55945ff01a24 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:5156:18                                                                                                 
    #21 0x55945ff053d0 in v8::Shell::Main(int, char**) src/d8/d8.cc:6036:18                                                                                                           
    #22 0x7ff1fe4426c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16                                       

SUMMARY: AddressSanitizer: heap-use-after-free src/handles/global-handles.cc:564:13 in v8::internal::GlobalHandles::Node::ResetPhantomHandle()                                                                                                                                                                                                                              
Shadow bytes around the buggy address:                                                                                                                                                                                                                                                                                                                                      
  0x502000012300: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fd                                                                                                                                                                                                                                                                                                           
  0x502000012380: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa                                                                                                                                                                                                                                                                                                           
  0x502000012400: fa fa fd fa fa fa fd fd fa fa fd fa fa fa fd fa                                                                                                                                                                                                                                                                                                           
  0x502000012480: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fd                                                                                                                     
  0x502000012500: fa fa fd fd fa fa fd fa fa fa fd fd fa fa fd fa                                                                                                                                                                                                                                                                                                           
=>0x502000012580: fa fa fd fa fa fa[fd]fa fa fa fd fd fa fa fd fd                                                                                                                                                                                                                                                                                                           
  0x502000012600: fa fa fd fa fa fa fd fd fa fa fd fa fa fa fd fd                                                                                                                     
  0x502000012680: fa fa fd fd fa fa fd fa fa fa fd fa fa fa fd fa                                                                                                                                                                                                                                                                                                           
  0x502000012700: fa fa fd fa fa fa fd fa fa fa fd fd fa fa fd fd                                                                                                                     
  0x502000012780: fa fa fd fd fa fa fd fa fa fa fd fa fa fa fd fa                                                                                                                     
  0x502000012800: fa fa fd fa fa fa fc fa fa fa fd fd fa fa fd fa                                                                                                                     
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
==3747180==ABORTING  

```

The gn args I used for reproduction:

```
is_debug = false
is_asan = true
target_cpu = "x64"
v8_enable_test_features = true
symbol_level = 2
v8_enable_backtrace = true

```

And then it still required a lot (> 1000) of attempts to reproduce eventually.

This issue looks like a UaF in the WasmEngine when compiling asm.js ("AsmJsCompilationJob"). Emanuel, could you help find an Owner for this? Thanks!

### wh...@gmail.com (2024-02-29)

Hi, sorry for later 

bisect 
I tested 91287 (https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-91287.zip?generation=1701387585490273&alt=media) 
and 91288 (https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-91288.zip?generation=1701397079124102&alt=media) 
only 91288 can trigger this bug. 

[exceptions] Unify pending and scheduled exceptions

The difference wasn't very well understood, and actually leads to
wonky/broken semantics.

Scheduled exceptions were embedder-side exceptions, while pending
exceptions were used inside of v8. Conversions were done on the
boundaries. Pending exceptions could be cleared locally without
try/catch since we'd only propagate exceptions to external try/catch on
Promotion. An embedder-side TryCatch could be reused without
v8::TryCatch::Reset() first. If there already was an exception and a new
one was thrown, the exception was simply overwritten.

Or that was the theory.

V8 is reentrant. When the embedder returns to V8 a scheduled exception
had to be turned into a pending exception
(Isolate::PromoteScheduledException()). When V8 returns to the embedder,
a pending exception is turned into a scheduled exception
(Isolate::OptionalRescheduleException()) to make sure that exceptions
can be returned through multiple JS/embedder stack segments.

This CL drops the distinction between scheduled and pending exceptions.
A possible pending exception is dropped on rentry in V8, meaning the
embedder will always be able to call into V8 again despite being given
an error.

This slightly changes the semantics: if an embedder calls into V8 while
a pending exception was sitting around, it won't be "rethrown" on exit
to the caller of the embedder. However, this case (rentering V8 without
an explicit TryCatch) would already have been partially broken: if V8
would call out to the embedder again, on return to V8 the exception
would have been throw there, instead of only when returning to the first
call to V8.

Embedder code may need to be fixed to account for this change. A similar
change was needed in V8 in src/d8/async-hooks-wrapper.cc: Multiple calls
to SET_HOOK_FN needed to complete before a possible exception was
propagated to the caller. The solution is to wrap the calls in TryCatch
with ReThrow.

In a follow-up I'll look into not clearing Isolate::pending_exception on
entry at all, and instead always clear it when the exception is
propagated to TryCatch (as opposed to JS). This would change DCHECKs in
V8 that guarantee that we exit V8 when we have a pending exception. I'll
support those by adding debugmode only flags.

Bug: v8:7235
Change-Id: Iff7c8fb8ff2f0bddbac0d84ce832086fba330dd1
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5050065
Commit-Queue: Toon Verwaest <verwaest@chromium.org>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Cr-Commit-Position: refs/heads/main@{#91288}

### wh...@gmail.com (2024-02-29)

sorry for later 

bisect 
I test 91244 (https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-91244.zip?generation=1701266208070674&alt=media)
and 91245 (https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-91245.zip?generation=1701266729144274&alt=media)
only 91245 can reproduce. 


[wasm] Fix unsafe shutdown of WeakScriptHandle

The recently introduced clearing of GlobalHandles in the
~WeakScriptHandle destructor must not run on background threads,
so with this patch we now post a task to the main thread to take
care of that. However, we must be careful *not* to post that task
in case the entire Isolate is currently shutting down.

Fixed: v8:14477
Change-Id: Idd2c0fd6ed32528e9e662f48e4792e45a5ef8430
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5068358
Reviewed-by: Clemens Backes <clemensb@chromium.org>
Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
Cr-Commit-Position: refs/heads/main@{#91245}

### wh...@gmail.com (2024-03-01)

details 
1. `location` is raw ptr, 
```
 private:
  // Store the location in a unique_ptr so that its address stays the same even
  // when this object is moved/copied.
  std::unique_ptr<Address*> location_;
```

and initialized in here with global_handle
```
class WeakScriptHandle {
 public:
  WeakScriptHandle(Handle<Script> script, Isolate* isolate)
      : script_id_(script->id()), isolate_(isolate) {
    DCHECK(IsString(script->name()) || IsUndefined(script->name()));
    if (IsString(script->name())) {
      source_url_ = String::cast(script->name())->ToCString();
    }
    auto global_handle =
        script->GetIsolate()->global_handles()->Create(*script);
    location_ = std::make_unique<Address*>(global_handle.location());  <---------[1]
    GlobalHandles::MakeWeak(location_.get());
  }
```
2. then at commit (also bisect at comment 8), which move location to ClearWeakScriptHandleTask and post a task.
```
  // This function is designed for one targeted use case, which always
  // acquires a lock on {mutex_} before calling here.
  mutex_.AssertHeld();
  IsolateInfo* isolate_info = isolates_[isolate].get();
  std::shared_ptr<TaskRunner> runner = isolate_info->foreground_task_runner;
  runner->PostTask(std::make_unique<ClearWeakScriptHandleTask>(     <----------[2]
      isolate, std::move(location)));
}
```
3. then if posted task will finished, at this time, trigger gc, and location is allocated by globalhandle, lead uaf.


1.https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/wasm-engine.cc;l=161;bpv=1;bpt=1?q=wasm-engine.cc
2.https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/wasm-engine.cc;l=461;drc=f4a00cc248dd2dc8ec8759fb51620d47b5114090;bpv=1;bpt=1?q=wasm-engine.cc

### wh...@gmail.com (2024-03-01)

according recent commit 
```
commit 4096a3a83a0827f4fd36cf8be822aa77332f6469
Author: Jakob Kummerow <jkummerow@chromium.org>
Date:   Thu Nov 30 15:08:53 2023 +0100

    Reland "[wasm] Fix unsafe shutdown of WeakScriptHandle"
    
    This is a reland of commit 3e267a851cc8a72730ff395c2f55e2ba49b015b6
    Changed in reland: merged the follow-up fix from crrev.com/c/5072553,
    making the posted task cancelable.
    
    Original description:
    > The recently introduced clearing of GlobalHandles in the
    > ~WeakScriptHandle destructor must not run on background threads,
    > so with this patch we now post a task to the main thread to take
    > care of that. However, we must be careful *not* to post that task
    > in case the entire Isolate is currently shutting down.
    
    Fixed: v8:14477
    Change-Id: I251b5ae1b92eaadcb2916e607c65876c8d284ef4
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5077386
    Commit-Queue: Clemens Backes <clemensb@chromium.org>
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
    Reviewed-by: Clemens Backes <clemensb@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#91283}
```
this commit is already shipping to 121/stable, so if no other problem, 
active branch: 122/stable, 123/beta, 124/dev

[1]https://chromiumdash.appspot.com/commit/4096a3a83a0827f4fd36cf8be822aa77332f6469

### wh...@gmail.com (2024-03-05)

ping, any updates?

### jk...@chromium.org (2024-03-05)

Sure. I've looked at this last week; AFAICT it's a shutdown ordering issue, so I'm fixing some higher-priority bugs first, but I'll get back to this when I have time.

### ad...@chromium.org (2024-03-05)

jkummerow@, if it's a shutdown bug, that only reduces the severity by one notch - see the [top of the severity guidelines](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md). This is a renderer UaF which would normally be S1, so this reduces it to S2. For the record, also, S4 means "unknown severity" in the world of our new issue tracker so it shows up on the radar of our security shepherds.

### wh...@gmail.com (2024-03-14)

any update?

### jk...@chromium.org (2024-03-15)

I haven't forgotten, just been busy.

I have what I think should be a fix: <https://chromium-review.googlesource.com/c/v8/v8/+/5372733>

Since I've never managed to reproduce this issue on my machine, I can't be 100% confident that it's gone. The situation in the ASan report from #6 should be addressed by this fix, at least.

### ap...@google.com (2024-03-18)

Project: v8/v8
Branch: main

commit 73f62bd5882f878d4aea8b5b7249084eecd97525
Author: Jakob Kummerow <jkummerow@chromium.org>
Date:   Mon Mar 18 16:12:54 2024

    [wasm] Fix ClearWeakScriptHandleTask shutdown issue
    
    When an Isolate shuts down at an inconvenient moment and instructs its
    task runner to destroy all waiting tasks, these tasks must not free
    memory that later steps in the Isolate shutdown sequence will still
    write to. This patch fixes such a situation for ClearWeakScriptHandleTasks
    by letting the Isolate itself own the memory in question.
    
    I have never been able to reproduce the reported issue myself, so
    this is a somewhat speculative fix.
    
    Fixed: 326607001
    Change-Id: Ie708439d924e9344c2df6bbba1cd864336756881
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5372733
    Reviewed-by: Clemens Backes <clemensb@chromium.org>
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#92882}

M       src/execution/isolate.cc
M       src/execution/isolate.h
M       src/wasm/wasm-engine.cc
M       src/wasm/wasm-engine.h

https://chromium-review.googlesource.com/5372733


### am...@google.com (2024-03-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### wh...@gmail.com (2024-03-27)

Hi, may I get bisect bonus with comment8? 

### wh...@gmail.com (2024-03-27)

and may I get a CVE for this report?

### am...@chromium.org (2024-03-27)

Hello, the $7,000 reward amount was not the standard baseline reports for renderer process memory corruption, but was impacted by this being bug mitigated by shutdown. Because this bug did impact Stable channel at the time it was reported and also contacted a bisect, the total reward decision is $7,000.

Additionally, as mentioned on previous bugs, when a bug is eligible for a CVE, the CVE is issued at the time the bug fix is released in a Stable channel update. The CVE will be issued at that time. [1]

[1] <https://chromium.googlesource.com/chromium/src/+/main/docs/security/vrp-faq.md#will-i-receive-a-cve-for-my-bug>

### wh...@gmail.com (2024-03-27)

Thank you so much.

### pe...@google.com (2024-06-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/326607001)*
