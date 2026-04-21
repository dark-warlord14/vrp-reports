# memory corruption in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [40063818](https://issues.chromium.org/issues/40063818) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>GarbageCollection |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | di...@chromium.org |
| **Created** | 2023-03-29 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

memory corruption in v8  

chrome version:  

Chromium 113.0.5653.0  

Chromium 114.0.5682.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1123423.zip)  

os version:  

ubuntu 22.04

repro steps:  

1 python3 -m http.server 8000 --dir=|path|  

2 ~/asan-linux-release/chrome <http://localhost:8000/crash.html> --no-sandbox --js-flags=--harmony-struct --incognito --user-data-dir=/tmp/xx23

After about ten seconds, a SIG11 crash will be reproduced.

**Problem Description:**  

Received signal 11 SEGV\_ACCERR 7d9b023c0008  

#0 0x563f4e9213c7 in backtrace /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/../sanitizer\_common/sanitizer\_common\_interceptors.inc:4410:13  

#1 0x563f5fe3d242 in base::debug::CollectStackTrace(void\*\*, unsigned long) ./../../base/debug/stack\_trace\_posix.cc:979:7  

#2 0x563f5fdfa683 in StackTrace ./../../base/debug/stack\_trace.cc:221:12  

#3 0x563f5fdfa683 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack\_trace.cc:218:28  

#4 0x563f5fe3bb9a in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo\_t\*, void\*) ./../../base/debug/stack\_trace\_posix.cc:456:3  

#5 0x7f21c4a42520 in \_\_GI\_\_\_sigaction :?  

#6 0x563f542fdf8d in operator& ./../../v8/src/base/flags.h:56:18  

#7 0x563f542fdf8d in operator& ./../../v8/src/base/flags.h:70:12  

#8 0x563f542fdf8d in IsFlagSet ./../../v8/src/heap/basic-memory-chunk.h:192:63  

#9 0x563f542fdf8d in InWritableSharedSpace ./../../v8/src/heap/basic-memory-chunk.h:257:12  

#10 0x563f542fdf8d in InWritableSharedSpace ./../../v8/src/objects/objects-inl.h:207:51  

#11 0x563f542fdf8d in MaybeForwardSlot ./../../v8/src/heap/heap.cc:4786:21  

#12 0x563f542fdf8d in v8::internal::ClientRootVisitor::VisitRootPointers(v8::internal::Root, char const\*, v8::internal::FullObjectSlot, v8::internal::FullObjectSlot) ./../../v8/src/heap/heap.cc:4757:7  

#13 0x563f541804c2 in Iterate ./../../v8/src/handles/traced-handles.cc:945:16  

#14 0x563f541804c2 in v8::internal::TracedHandles::Iterate(v8::internal::RootVisitor\*) ./../../v8/src/handles/traced-handles.cc:1049:60  

#15 0x563f542de0ac in v8::internal::Heap::IterateRoots(v8::internal::RootVisitor\*, v8::base::EnumSet<v8::internal::SkipRoot, int>) ./../../v8/src/heap/heap.cc:4663:39  

#16 0x563f542dee83 in operator() ./../../v8/src/heap/heap.cc:4805:27  

#17 0x563f542dee83 in IterateClientIsolates<(lambda at ../../v8/src/heap/heap.cc:4804:9)> ./../../v8/src/heap/safepoint.h:178:7  

#18 0x563f542dee83 in v8::internal::Heap::IterateRootsIncludingClients(v8::internal::RootVisitor\*, v8::base::EnumSet<v8::internal::SkipRoot, int>) ./../../v8/src/heap/heap.cc:4803:36  

#19 0x563f54395c2b in v8::internal::MarkCompactCollector::UpdatePointersAfterEvacuation() ./../../v8/src/heap/mark-compact.cc:5109:12  

#20 0x563f543518cc in v8::internal::MarkCompactCollector::Evacuate() ./../../v8/src/heap/mark-compact.cc:4588:3  

#21 0x563f54336e11 in v8::internal::MarkCompactCollector::CollectGarbage() ./../../v8/src/heap/mark-compact.cc:555:3  

#22 0x563f542c74f4 in v8::internal::Heap::MarkCompact() ./../../v8/src/heap/heap.cc:2534:29  

#23 0x563f542bdb42 in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const\*) ./../../v8/src/heap/heap.cc:2283:5  

#24 0x563f542b6c94 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:1781:9  

#25 0x563f542bbce8 in CollectAllGarbage ./../../v8/src/heap/heap.cc:1477:3  

#26 0x563f542bbce8 in v8::internal::Heap::ReportExternalMemoryPressure() ./../../v8/src/heap/heap.cc:1625:5  

#27 0x563f53c27ccd in ReportExternalAllocationLimitReached ./../../v8/src/api/api.cc:9166:9  

#28 0x563f53c27ccd in v8::Isolate::AdjustAmountOfExternalAllocatedMemory(long) ./../../v8/src/api/api.cc:9841:5  

#29 0x563f53cfabda in v8::internal::(anonymous namespace)::ConstructBuffer(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::JSReceiver](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::InitializedFlag) ./../../v8/src/builtins/builtins-arraybuffer.cc:108:17  

#30 0x563f53cf5148 in v8::internal::Builtin\_Impl\_ArrayBufferConstructor(v8::internal::BuiltinArguments, v8::internal::Isolate\*) ./../../v8/src/builtins/builtins-arraybuffer.cc:152:10  

#31 0x563f56cfbcb6 in Builtins\_CEntry\_Return1\_ArgvOnStack\_BuiltinExit setup-isolate-deserialize.cc:0:0  

r8: 0000606000a25638 r9: 0000000000001fff r10: 0000000000000000 r11: 00007ffdc9c0a6c8  

r12: 00000fe438399a35 r13: 000000000000000d r14: 0000606000a25638 r15: 00007f21c1ccd1a8  

di: 00007d9b023c0008 si: 000000000000000d bp: 00007ffdc9c09820 bx: 0000606000a25630  

dx: 0000000000000000 ax: 00000fb360478001 cx: 0000606000a25630 sp: 00007ffdc9c097f0  

ip: 0000563f542fdf8d efl: 0000000000010246 cgf: 002b000000000033 erf: 0000000000000004  

trp: 000000000000000e msk: 0000000000000000 cr2: 00007d9b023c0008  

[end of stack trace]

**Additional Comments:**

\*\*Chrome version: \*\* 111.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 1.2 KB)
- [ws.js](attachments/ws.js) (text/plain, 179 B)

## Timeline

### [Deleted User] (2023-03-29)

[Empty comment from Monorail migration]

### em...@gmail.com (2023-03-29)

The following dcheck is triggered in debug build.
# Fatal error in ../../v8/src/heap/mark-compact.cc, line 2382
# Debug check failed: heap()->Contains(object).
#
#
#
#FailureMessage Object: 0x7f2f0ff20060#0 0x55a6a73f33f7 (/home/pwn11/chromium/src/out/debug/chrome+0x111843f6)
    #0 0x55a6bc1c1fd2 in base::debug::CollectStackTrace(void**, unsigned long) ./../../base/debug/stack_trace_posix.cc:979:7
    #1 0x55a6bc173f13 in StackTrace ./../../base/debug/stack_trace.cc:221:12
    #2 0x55a6bc173f13 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:218:28
    #3 0x55a6c39f851c in gin::(anonymous namespace)::PrintStackTrace() ./../../gin/v8_platform.cc:44:27
    #4 0x55a6c2bee0ef in V8_Fatal(char const*, int, char const*, ...) ./../../v8/src/base/logging.cc:164:38
    #5 0x55a6c2bed1bf in v8::base::(anonymous namespace)::DefaultDcheckHandler(char const*, int, char const*) ./../../v8/src/base/logging.cc:57:3
    #6 0x55a6ae231ef4 in v8::internal::MarkCompactCollector::ProcessMarkingWorklist(unsigned long, v8::internal::MarkCompactCollector::MarkingWorklistProcessingMode) ./../../v8/src/heap/mark-compact.cc:2382:5
    #7 0x55a6ae22e188 in ProcessMarkingWorklist ./../../v8/src/heap/mark-compact.cc:2345:10
    #8 0x55a6ae22e188 in v8::internal::MarkCompactCollector::ProcessEphemerons() ./../../v8/src/heap/mark-compact.cc:2220:46
    #9 0x55a6ae22d0a7 in v8::internal::MarkCompactCollector::MarkTransitiveClosureUntilFixpoint() ./../../v8/src/heap/mark-compact.cc:2188:49
    #10 0x55a6ae2188c1 in MarkTransitiveClosure ./../../v8/src/heap/mark-compact.cc:2451:8
    #11 0x55a6ae2188c1 in v8::internal::MarkCompactCollector::MarkLiveObjects() ./../../v8/src/heap/mark-compact.cc:2621:5
    #12 0x55a6ae216b4b in v8::internal::MarkCompactCollector::CollectGarbage() ./../../v8/src/heap/mark-compact.cc:557:3
    #13 0x55a6ae18d309 in v8::internal::Heap::MarkCompact() ./../../v8/src/heap/heap.cc:2566:29
    #14 0x55a6ae186627 in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const*) ./../../v8/src/heap/heap.cc:2315:5
    #15 0x55a6ae180707 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:1806:9
    #16 0x55a6ae17df91 in CollectAllGarbage ./../../v8/src/heap/heap.cc:1502:3
    #17 0x55a6ae17df91 in v8::internal::Heap::HandleGCRequest() ./../../v8/src/heap/heap.cc:1470:5
    #18 0x55a6adf915be in v8::internal::StackGuard::HandleInterrupts() ./../../v8/src/execution/stack-guard.cc:293:23
    #19 0x55a6af5929ca in v8::internal::__RT_impl_Runtime_StackGuard(v8::internal::Arguments<(v8::internal::ArgumentsType)0>, v8::internal::Isolate*) ./../../v8/src/runtime/runtime-internal.cc:349:34
    #20 0x55a6af591af1 in v8::internal::Runtime_StackGuard(int, unsigned long*, v8::internal::Isolate*) ./../../v8/src/runtime/runtime-internal.cc:338:1
    #21 0x55a6b1b38cf6 in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit setup-isolate-deserialize.cc:0:0


### cl...@chromium.org (2023-03-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6233155800072192.

### cl...@chromium.org (2023-03-31)

ClusterFuzz testcase 6233155800072192 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2023-03-31)

Detailed Report: https://clusterfuzz.com/testcase?key=6233155800072192

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: CHECK failure
Crash Address: 
Crash State:
  r. Sending zygote magic failed in zygote_linux.cc
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1124079

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6233155800072192

Additional requirements: Requires HTTP

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

### mp...@chromium.org (2023-04-01)

I can reproduce this on my machine. I'm not sure if clusterfuzz is obeying the use of the --harmony-struct flag.

This also reproduces under --shared-string-table. I'm a little confused whether this is considered Security_Impact-None because according to [1] this flag is not experimental but does not affect shipping configurations. Saelo@ can you confirm whether this should be Security_Impact-None or not?

This reproduces on my current M111 build but does NOT reproduce on my M110 build. Setting FoundIn until I know whether it's Security_Impact-None.

[1] https://bugs.chromium.org/p/chromium/issues/detail?id=1424955#c19

[Monorail components: Blink>JavaScript>GarbageCollection]

### [Deleted User] (2023-04-01)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-01)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sa...@google.com (2023-04-03)

This looks like another shared heap issue, so Cc'ing Dominik. If it reproduces with `--shared-string-table`, then it's Impact-None, but (presumably) Severity-High.

### di...@chromium.org (2023-04-04)

I think this is an issue with traced handles and the shared heap. Assigning to me.

### di...@chromium.org (2023-04-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-04-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/e339a95528494a82a15468693df9e78ba34bc5f1

commit e339a95528494a82a15468693df9e78ba34bc5f1
Author: Dominik Inführ <dinfuehr@chromium.org>
Date: Wed Apr 05 07:02:28 2023

[heap] Add kTracedHandles to skip those roots in IterateRoots

This CL splits traced handles off from SkipRoot::kGlobalHandles and
introduces a separate flag SkipRoot::kTracedHandles.

The CL adds the flag to all IterateRoots invocations that either
skipped kWeak or kGlobalHandles. The only exception is the evacuation
verifier where it's probably a good idea to also verify pointers
in traced handles.

Bug: chromium:1428786
Change-Id: I492d194b5e3d0f0440e82482f93e5f412e96b06c
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4399950
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#86937}

[modify] https://crrev.com/e339a95528494a82a15468693df9e78ba34bc5f1/src/snapshot/startup-deserializer.cc
[modify] https://crrev.com/e339a95528494a82a15468693df9e78ba34bc5f1/src/heap/incremental-marking.cc
[modify] https://crrev.com/e339a95528494a82a15468693df9e78ba34bc5f1/src/heap/scavenger.cc
[modify] https://crrev.com/e339a95528494a82a15468693df9e78ba34bc5f1/src/heap/heap.h
[modify] https://crrev.com/e339a95528494a82a15468693df9e78ba34bc5f1/src/heap/heap.cc
[modify] https://crrev.com/e339a95528494a82a15468693df9e78ba34bc5f1/src/heap/mark-compact.cc
[modify] https://crrev.com/e339a95528494a82a15468693df9e78ba34bc5f1/src/snapshot/startup-serializer.cc
[modify] https://crrev.com/e339a95528494a82a15468693df9e78ba34bc5f1/src/profiler/heap-snapshot-generator.cc


### gi...@appspot.gserviceaccount.com (2023-04-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/fcbc77b9b36e24e2eaf8a4b2141e09a16550a1a6

commit fcbc77b9b36e24e2eaf8a4b2141e09a16550a1a6
Author: Dominik Inführ <dinfuehr@chromium.org>
Date: Wed Apr 05 12:32:31 2023

[heap] Mark all objects in client traced handles during shared GC

In a shared GC we need to assume that all traced handles in client
isolates are alive and mark their referenced object. We can only skip
traced handles on the main thread because we will perform a unified GC
for the main isolate during a shared GC. We don't do that for
client isolates which means that client isolate traced handles
need to be roots here.

Since we need to invoke Heap::IterateRoots for client isolates with
different options, we can't use IterateRootsIncludingClients. We
then also need a ClientRootMarkingVisitor for client isolates since
for client isolates we only care about pointers into the shared spaces.

Bug: chromium:1428786
Change-Id: I8edb989774f8e2dc8a0b463ed23ab1152369bb4b
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4403216
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#86956}

[modify] https://crrev.com/fcbc77b9b36e24e2eaf8a4b2141e09a16550a1a6/src/heap/mark-compact.h
[modify] https://crrev.com/fcbc77b9b36e24e2eaf8a4b2141e09a16550a1a6/src/heap/mark-compact.cc


### di...@chromium.org (2023-04-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-17)

[Empty comment from Monorail migration]

### am...@google.com (2023-04-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-27)

Congratulations, Cassidy Kim! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-04-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-07-24)

This issue was migrated from crbug.com/chromium/1428786?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063818)*
