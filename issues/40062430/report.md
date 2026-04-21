# Security: Debug check failed: ReadOnlyHeap::Contains(object) || heap_->Contains(object)

| Field | Value |
|-------|-------|
| **Issue ID** | [40062430](https://issues.chromium.org/issues/40062430) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | wh...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2022-12-29 |
| **Bounty** | $7,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

v8 main branch  

commit d65596fc36f3b8362e1f8e04a6c9ce04c569f7a5

// CRASH INFO  

// ==========  

// TERMSIG: 6  

// STDERR:  

// #  

// # Fatal error in ../../src/heap/marking-visitor-inl.h, line 29  

// # Debug check failed: ReadOnlyHeap::Contains(object) || heap\_->Contains(object).  

// #  

// #  

// #  

// #FailureMessage Object: 0x7fee2babd610  

// ==== C stack trace ===============================  

// Debug check failed: ReadOnlyHeap::Contains(object) || heap\_->Contains  

//  

// #  

// #  

// #  

// #FailureMessage Object: 0x7fee2fac56106faa97) [0x55aa00019a97]  

// /home/uuu/v8\_src.main/v8/out/fuzzbuild/d8(+0x6ed70a) [0x55aa0000c70a]  

// /home/uuu/v8\_src.main/v8/out/fuzzbuild/d8(+0x6ed065) [0x55aa0000c065]  

// /home/uuu/v8\_src.main/v8/out/fuzzbuild/d8(+0xd5a47f) [0x55aa0067947f]  

// /home/uuu/v8\_src.main/v8/out/fuzzbuild/d8(+0xd7aab9) [0x55aa00699ab9]  

// /home/uuu/v8\_src.main/v8/out/fuzzbuild/d8(+0xd54736) [0x55aa00673736]  

// /home/uuu/v8\_src.main/v8/out/fuzzbuild/d8(+0xd8fb2e) [0x55aa006aeb2e]  

// /home/uuu/v8\_src.main/v8/out/fuzzbuild/d8(+0x6fed6f) [0x55aa0001dd6f]  

// /home/uuu/v8\_src.main/v8/out/fuzzbuild/d8(+0x708a39) [0x55aa00027a39]  

// /home/uuu/v8\_src.main/v8/out/fuzzbuild/d8(+0x6f8469) [0x55aa00017469]  

// /lib/x86\_64-linux-gnu/libpthread.so.0(+0x8609) [0x7fee32968609]  

// /lib/x86\_64-linux-gnu/libc.so.6(clone+0x43) [0x7fee326fb133]  

// Received signal 6

## Attachments

- [program_20221228110724_55360795-D32C-462F-9290-13331DEA2073_flaky.js](attachments/program_20221228110724_55360795-D32C-462F-9290-13331DEA2073_flaky.js) (text/plain, 41.1 KB)

## Timeline

### [Deleted User] (2022-12-29)

[Empty comment from Monorail migration]

### wh...@gmail.com (2022-12-29)

__GI_raise (sig=sig@entry=6) at ../sysdeps/unix/sysv/linux/raise.c:50
50      ../sysdeps/unix/sysv/linux/raise.c: No such file or directory.
#0  __GI_raise (sig=sig@entry=6) at ../sysdeps/unix/sysv/linux/raise.c:50
#1  0x00007fd0d8f71859 in __GI_abort () at abort.c:79
#2  0x00007fd0d97d29f8 in v8::base::OS::Abort() () at ../../src/base/platform/platform-posix.cc:677
#3  0x00007fd0d97a43f6 in V8_Fatal(char const*, int, char const*, ...) () at ../../src/base/logging.cc:167
#4  0x00007fd0d97a3e1c in v8::base::(anonymous namespace)::DefaultDcheckHandler(char const*, int, char const*) () at ../../src/base/logging.cc:57
#5  0x00007fd0d97a4487 in V8_Dcheck(char const*, int, char const*) () at ../../src/base/logging.cc:171
#6  0x00007fd0dcb809f7 in v8::internal::MarkingVisitorBase<v8::internal::ConcurrentMarkingVisitor, v8::internal::ConcurrentMarkingState>::MarkObject(v8::internal::HeapObject, v8::internal::HeapObject) () at ../../src/heap/marking-visitor-inl.h:29
#7  0x00007fd0dcb808b4 in void v8::internal::MarkingVisitorBase<v8::internal::ConcurrentMarkingVisitor, v8::internal::ConcurrentMarkingState>::ProcessStrongHeapObject<v8::internal::CompressedHeapObjectSlot>(v8::internal::HeapObject, v8::internal::CompressedHeapObjectSlot, v8::internal::HeapObject) () at ../../src/heap/marking-visitor-inl.h:49
#8  0x00007fd0dcb806de in void v8::internal::MarkingVisitorBase<v8::internal::ConcurrentMarkingVisitor, v8::internal::ConcurrentMarkingState>::VisitPointersImpl<v8::internal::CompressedObjectSlot>(v8::internal::HeapObject, v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot) () at ../../src/heap/marking-visitor-inl.h:91
#9  0x00007fd0dcb7fb95 in v8::internal::MarkingVisitorBase<v8::internal::ConcurrentMarkingVisitor, v8::internal::ConcurrentMarkingState>::VisitPointers(v8::internal::HeapObject, v8::internal::CompressedObjectSlot, v8::internal::CompressedObjectSlot) () at ../../src/heap/marking-visitor.h:94
#10 0x00007fd0dcb96213 in void v8::internal::BodyDescriptorBase::IteratePointers<v8::internal::ConcurrentMarkingVisitor>(v8::internal::HeapObject, int, int, v8::internal::ConcurrentMarkingVisitor*) () at ../../src/objects/objects-body-descriptors-inl.h:128
#11 0x00007fd0dcba1184 in void v8::internal::SuffixRangeBodyDescriptor<4>::IterateBody<v8::internal::ConcurrentMarkingVisitor>(v8::internal::Map, v8::internal::HeapObject, int, v8::internal::ConcurrentMarkingVisitor*) () at ../../src/objects/objects-body-descriptors.h:135
#12 0x00007fd0dcba2208 in int v8::internal::ConcurrentMarkingVisitor::VisitLeftTrimmableArray<v8::internal::FixedArray>(v8::internal::Map, v8::internal::FixedArray) () at ../../src/heap/concurrent-marking.cc:563
#13 0x00007fd0dcb91f69 in v8::internal::MarkingVisitorBase<v8::internal::ConcurrentMarkingVisitor, v8::internal::ConcurrentMarkingState>::VisitFixedArray(v8::internal::Map, v8::internal::FixedArray) () at ../../src/heap/marking-visitor-inl.h:273
#14 0x00007fd0dcb7a0d7 in v8::internal::HeapVisitor<int, v8::internal::ConcurrentMarkingVisitor>::Visit(v8::internal::Map, v8::internal::HeapObject) () at ../../src/heap/objects-visiting-inl.h:66
#15 0x00007fd0dcb75f09 in v8::internal::ConcurrentMarking::RunMajor(v8::JobDelegate*, v8::base::EnumSet<v8::internal::CodeFlushMode, int>, unsigned int, bool) () at ../../src/heap/concurrent-marking.cc:813
#16 0x00007fd0dcbb884d in v8::internal::ConcurrentMarking::JobTaskMajor::Run(v8::JobDelegate*) () at ../../src/heap/concurrent-marking.cc:661
#17 0x00007fd0d97282e9 in v8::platform::DefaultJobWorker::Run() () at ../../src/libplatform/default-job.h:147
#18 0x00007fd0d9730c0f in v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run() () at ../../src/libplatform/default-worker-threads-task-runner.cc:73
#19 0x00007fd0d97d51d6 in v8::base::Thread::NotifyStartedAndRun() () at ../../src/base/platform/platform.h:596
#20 0x00007fd0d97d40fd in v8::base::ThreadEntry(void*) () at ../../src/base/platform/platform-posix.cc:1112
#21 0x00007fd0d929a609 in start_thread (arg=<optimized out>) at pthread_create.c:477
#22 0x00007fd0d906e133 in clone () at ../sysdeps/unix/sysv/linux/x86_64/clone.S:95


### cl...@chromium.org (2022-12-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4777740877365248.

### li...@chromium.org (2022-12-29)

Assigning to CL author to take a closer look.

[Monorail components: Blink>JavaScript]

### ol...@chromium.org (2022-12-30)

Nice, I can repro locally, however this is not related to my CL and behind --harmony, so probably limited scope.

Command line args `--harmony --harmony-struct` are required for repro. I don't have permissions to pass these to ClusterFuzz.
Did some initial bisecting and it's tricky because the error changes and it reporduces with `--no-shared-space` and disappears with `--shared-space` (which recently changed default...).

The current error appears with the unrelated CL https://chromium-review.googlesource.com/c/v8/v8/+/4020296 .

As far as I can tell this issue begins with https://chromium-review.googlesource.com/c/v8/v8/+/3704809 where I observe the following crash for the first time:
```
# Fatal error in ../../src/objects/code-inl.h, line 1872
# Debug check failed: !object.InSharedHeap().
```

+syg: CL 3704809 is a likely culprit, because what triggers the DCHECK is a heap number -1460565461 reachable through a FixedArray[3999] (backing store of shared array?). This number is initially created by turbofan (in `Assembler::AllocateAndInstallRequestedHeapNumbers`) when compiling `main`. The crash happens after eager deopt and re-opt of `main`.

### ol...@chromium.org (2022-12-30)

Here is a reduced repro (no deopt):
```
while (true) {
  c = SharedArray(4000);
  c[0] = 2000000000
}
```

### sy...@chromium.org (2023-01-06)

Thanks for the investigation and explanation, olivf@! Looking. Setting Security_Impact-None since this is in an experimental, off-by-default feature.

### gi...@appspot.gserviceaccount.com (2023-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/f1adbe2e4443ea539bf6e2a7b451497b6d4db312

commit f1adbe2e4443ea539bf6e2a7b451497b6d4db312
Author: Shu-yu Guo <syg@chromium.org>
Date: Fri Jan 06 01:44:25 2023

[shared-struct] Fix shared value barrier in TF

This CL fixes a bug where TurboFan was incorrectly compiling away the
shared value barrier for shared arrays.

TurboFan should not be compiling accesses to objects in the shared heap
until it natively has support for the shared value barrier, because it
is an invariant that shared objects do not point to non-shared objects.

Bug: chromium:1404052, v8:12547
Change-Id: I5bd44ce5c44ad81a97421598e6d5b24fb5e210cd
Fixed: chromium:1404052
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4136980
Commit-Queue: Shu-yu Guo <syg@chromium.org>
Reviewed-by: Tobias Tebbi <tebbi@chromium.org>
Cr-Commit-Position: refs/heads/main@{#85233}

[modify] https://crrev.com/f1adbe2e4443ea539bf6e2a7b451497b6d4db312/src/compiler/js-native-context-specialization.cc
[add] https://crrev.com/f1adbe2e4443ea539bf6e2a7b451497b6d4db312/test/mjsunit/shared-memory/shared-value-barrier-optimization.js


### [Deleted User] (2023-01-11)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2023-01-12)

I assume this can cause heap corruption, so marking as Security_Severity-High. It doesn't matter much for Security_Impact-None bugs.

### [Deleted User] (2023-01-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-12)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-18)

Congratulations on another one! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us -- good work! 

### am...@chromium.org (2023-01-18)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-04-20)

This issue was migrated from crbug.com/chromium/1404052?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062430)*
