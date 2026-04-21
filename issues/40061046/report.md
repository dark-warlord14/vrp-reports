# Security: [maglev] VisitSwitchOnGeneratorState function  JumpTableTargetOffsets can be  0 

| Field | Value |
|-------|-------|
| **Issue ID** | [40061046](https://issues.chromium.org/issues/40061046) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | vi...@gmail.com |
| **Assignee** | le...@chromium.org |
| **Created** | 2022-09-19 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**

the bug occur in the maglev phase. which can be exploited lead to RCE

**VERSION**  

Chrome Version: dev  

Operating System: ubuntu20.04 tls x64

**REPRODUCTION CASE**  

compile debug version v8 with maglev engable,  

run the command line:  

./d8 --expose-gc --maglev --allow-natives-syntax 1.js

Crash info:

# 

# Fatal error in ../../src/maglev/maglev-graph-builder.cc, line 3036

# Debug check failed: offsets.size() != 0 (0 vs. 0).

# 

# 

# 

#FailureMessage Object: 0x7fa9a1604380  

==== C stack trace ===============================

```
/home//v8/out/fuzzbuild/d8(+0x6b0502) [0x562e18b76502]  
/home//v8/out/fuzzbuild/d8(+0x6af117) [0x562e18b75117]  
/home//v8/out/fuzzbuild/d8(+0x6a19fe) [0x562e18b679fe]  
/home//v8/out/fuzzbuild/d8(+0x6a1385) [0x562e18b67385]  
/home//v8/out/fuzzbuild/d8(+0x19c2f3a) [0x562e19e88f3a]  
/home//v8/out/fuzzbuild/d8(+0x1927a5a) [0x562e19deda5a]  
/home//v8/out/fuzzbuild/d8(+0x19223d8) [0x562e19de83d8]  
/home//v8/out/fuzzbuild/d8(+0x192152f) [0x562e19de752f]  
/home//v8/out/fuzzbuild/d8(+0x191e41b) [0x562e19de441b]  
/home//v8/out/fuzzbuild/d8(+0x9441ff) [0x562e18e0a1ff]  
/home//v8/out/fuzzbuild/d8(+0x191f1b9) [0x562e19de51b9]  
/home//v8/out/fuzzbuild/d8(+0x6b30bf) [0x562e18b790bf]  
/home//v8/out/fuzzbuild/d8(+0x6bdbf9) [0x562e18b83bf9]  
/home//v8/out/fuzzbuild/d8(+0x6acab9) [0x562e18b72ab9]  
/lib/x86_64-linux-gnu/libpthread.so.0(+0x8609) [0x7fa9a2862609]  
/lib/x86_64-linux-gnu/libc.so.6(clone+0x43) [0x7fa9a25f5163]  

```

Thread 2 "V8 DefaultWorke" received signal SIGTRAP, Trace/breakpoint trap.  

[Switching to Thread 0x7fa9a1605700 (LWP 41982)]

## Attachments

- [1.js](attachments/1.js) (text/plain, 423 B)

## Timeline

### [Deleted User] (2022-09-19)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-09-19)

Assigning to v8 security team.

[Monorail components: Blink>JavaScript]

### ts...@chromium.org (2022-09-19)

Asan trace is

==2729379==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7ff51c9012c0 at pc 0x55911248b394 bp 0x7ff51fa018f0 sp 0x7ff51fa018e8
READ of size 4 at 0x7ff51c9012c0 thread T1 (V8 DefaultWorke)
    #0 0x55911248b393 in id v8/src/maglev/maglev-ir.h:838:12
    #1 0x55911248b393 in HighestPostDominatingHole v8/src/maglev/maglev-regalloc.cc:82:16
    #2 0x55911248b393 in HighestPostDominatingHole<16UL> v8/src/maglev/maglev-regalloc.cc:120:9
    #3 0x55911248b393 in v8::internal::maglev::StraightForwardRegisterAllocator::ComputePostDominatingHoles() v8/src/maglev/maglev-regalloc.cc:266:46
    #4 0x559112489c81 in v8::internal::maglev::StraightForwardRegisterAllocator::StraightForwardRegisterAllocator(v8::internal::maglev::MaglevCompilationInfo*, v8::internal::maglev::Graph*) v8/src/maglev/maglev-regalloc.cc:162:3
    #5 0x55911228c65d in v8::internal::maglev::MaglevCompiler::Compile(v8::internal::LocalIsolate*, v8::internal::maglev::MaglevCompilationInfo*) v8/src/maglev/maglev-compiler.cc:584:36
    #6 0x5591122da650 in v8::internal::maglev::MaglevCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*) v8/src/maglev/maglev-concurrent-dispatcher.cc:104:3
    #7 0x559110d95115 in v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*) v8/src/codegen/compiler.cc:493:22
    #8 0x5591122dbcd8 in v8::internal::maglev::MaglevConcurrentDispatcher::JobTask::Run(v8::JobDelegate*) v8/src/maglev/maglev-concurrent-dispatcher.cc:138:44
    #9 0x55911398b846 in v8::platform::DefaultJobWorker::Run() v8/src/libplatform/default-job.h:147:18
    #10 0x55911399786c in v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run() v8/src/libplatform/default-worker-threads-task-runner.cc:73:11
    #11 0x55911397fd7d in NotifyStartedAndRun v8/src/base/platform/platform.h:596:5
    #12 0x55911397fd7d in v8::base::ThreadEntry(void*) v8/src/base/platform/platform-posix.cc:1112:11
    #13 0x7ff522fc6d7f in start_thread nptl/pthread_create.c:481:8

Address 0x7ff51c9012c0 is located in stack of thread T1 (V8 DefaultWorke) at offset 192 in frame
    #0 0x559112489e0f in v8::internal::maglev::StraightForwardRegisterAllocator::ComputePostDominatingHoles() v8/src/maglev/maglev-regalloc.cc:229

  This frame has 1 object(s):
    [32, 184) 'holes' (line 257) <== Memory access at offset 192 overflows this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
Thread T1 (V8 DefaultWorke) created by T0 here:
    #0 0x559110959c1c in pthread_create /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:208:3
    #1 0x55911397fbc1 in v8::base::Thread::Start() v8/src/base/platform/platform-posix.cc:1144:14
    #2 0x559113996f24 in WorkerThread v8/src/libplatform/default-worker-threads-task-runner.cc:66:3
    #3 0x559113996f24 in make_unique<v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread, v8::platform::DefaultWorkerThreadsTaskRunner *> buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:670:30
    #4 0x559113996f24 in v8::platform::DefaultWorkerThreadsTaskRunner::DefaultWorkerThreadsTaskRunner(unsigned int, double (*)()) v8/src/libplatform/default-worker-threads-task-runner.cc:16:28
    #5 0x559113985367 in __shared_ptr_emplace<const int &, double (*)()> buildtools/third_party/libc++/trunk/include/__memory/shared_ptr.h:297:37
    #6 0x559113985367 in allocate_shared<v8::platform::DefaultWorkerThreadsTaskRunner, std::Cr::allocator<v8::platform::DefaultWorkerThreadsTaskRunner>, const int &, double (*)(), void> buildtools/third_party/libc++/trunk/include/__memory/shared_ptr.h:956:55
 


### sa...@chromium.org (2022-09-19)

The maglev compiler is not currently enabled, so issues related to it have no security impact. Leszek, could you help find the right owner for this issue? Thanks!

### sa...@chromium.org (2022-09-19)

[Empty comment from Monorail migration]

### le...@chromium.org (2022-12-01)

Sorry for letting this fall through the cracks -- this was fixed by https://crrev.com/c/3932946

### vi...@gmail.com (2022-12-01)

seems I reported this first at Sep 19, 2022, https://crbug.com/chromium/1370396 found the bug at Oct 3, 2022. I reported the issue before https://crbug.com/chromium/1370396

### le...@chromium.org (2022-12-01)

That's true -- I bisected to find the fix but didn't look at the relative dates when setting the duplicate.

+amyressler, should I flip the duplicate status of this given that it's an external report?

### am...@chromium.org (2022-12-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-12-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-12-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-12-01)

re:https://crbug.com/chromium/1365366#c8, thanks leszeks@ since I had to look at them both, I went ahead and flipped the duplicate status around :) 

### [Deleted User] (2022-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-12-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-09)

Congratulations, @ma1fn! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2022-12-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-03-09)

This issue was migrated from crbug.com/chromium/1365366?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1370396]
[Monorail mergedinto: crbug.com/chromium/1370396]
[Monorail components added to Component Tags custom field.]

### dt...@google.com (2025-02-13)

Bulk update of issues accidentally marked as duplicate in issue tracker migration (b/325072672)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061046)*
