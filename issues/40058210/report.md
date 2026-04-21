# crash in v8 heap(--js-flags=--experimental-wasm-gc)

| Field | Value |
|-------|-------|
| **Issue ID** | [40058210](https://issues.chromium.org/issues/40058210) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript, Blink>JavaScript>GarbageCollection |
| **Platforms** | Android, Linux, Mac, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2021-12-12 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36

Steps to reproduce the problem:
Ubuntu:20.04
chrome version:
	-	Version 98.0.4750.0 (Official Build) dev (64-bit)
	-	Chromium 99.0.4759.0

//poc.html
<html>
<body>
<script>

function NewModule() {
"use asm";
function foo() {
}
return {foo:foo};
};
for(;;){
var _v_17_ = NewModule();
gc();
}

</script>
</body>
</html>

./chrome -js-flags=--experimental-wasm-gc,--expose-gc http://localhost:8000/poc.html

What is the expected behavior?

What went wrong?
Received signal 11 SEGV_MAPERR 7ee3ffffffff
    #0 0x55838ae083cb in __interceptor_backtrace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4277
    #1 0x55838ae083cb in ?? ??:0
    #2 0x5583992e30e9 in base::debug::CollectStackTrace(void**, unsigned long) ./../../base/debug/stack_trace_posix.cc:872
    #3 0x5583992e30e9 in ?? ??:0
    #4 0x558399099163 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:200
    #5 0x558399099163 in StackTrace ./../../base/debug/stack_trace.cc:197
    #6 0x558399099163 in ?? ??:0
    #7 0x5583992e1b9b in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:369
    #8 0x5583992e1b9b in ?? ??:0
    #9 0x7fe7031643c0 in __funlockfile :?
    #10 0x7fe7031643c0 in ?? ??:0
    #11 0x558393b6b5a4 in v8::internal::ConcurrentMarking::Run(v8::JobDelegate*, v8::base::EnumSet<v8::internal::CodeFlushMode, int>, unsigned int, bool) ./../../buildtools/third_party/libc++/trunk/include/atomic:1000
    #12 0x558393b6b5a4 in load ./../../buildtools/third_party/libc++/trunk/include/atomic:1611
    #13 0x558393b6b5a4 in atomic_load_explicit<int> ./../../buildtools/third_party/libc++/trunk/include/atomic:1967
    #14 0x558393b6b5a4 in Acquire_Load ./../../v8/src/base/atomicops.h:240
    #15 0x558393b6b5a4 in Acquire_Load<unsigned int> ./../../v8/src/base/atomic-utils.h:73
    #16 0x558393b6b5a4 in Acquire_Load_No_Unpack ./../../v8/src/objects/tagged-field-inl.h:157
    #17 0x558393b6b5a4 in map_word ./../../v8/src/objects/objects-inl.h:888
    #18 0x558393b6b5a4 in map ./../../v8/src/objects/objects-inl.h:806
    #19 0x558393b6b5a4 in Run ./../../v8/src/heap/concurrent-marking.cc:518
    #20 0x558393b6b5a4 in ?? ??:0
    #21 0x558393b81223 in v8::internal::ConcurrentMarking::JobTask::Run(v8::JobDelegate*) ./../../v8/src/heap/concurrent-marking.cc:418
    #22 0x558393b81223 in ?? ??:0
    #23 0x5583a52e9eff in base::internal::Invoker<base::internal::BindState<gin::V8Platform::PostJob(v8::TaskPriority, std::__1::unique_ptr<v8::JobTask, std::__1::default_delete<v8::JobTask> >)::$_0, std::__1::unique_ptr<v8::JobTask, std::__1::default_delete<v8::JobTask> > >, void (base::JobDelegate*)>::Run(base::internal::BindStateBase*, base::JobDelegate*) ./../../gin/v8_platform.cc:459
    #24 0x5583a52e9eff in Invoke<const (lambda at ../../gin/v8_platform.cc:456:25) &, const std::__1::unique_ptr<v8::JobTask, std::__1::default_delete<v8::JobTask> > &, base::JobDelegate *> ./../../base/bind_internal.h:416
    #25 0x5583a52e9eff in MakeItSo<const (lambda at ../../gin/v8_platform.cc:456:25) &, const std::__1::unique_ptr<v8::JobTask, std::__1::default_delete<v8::JobTask> > &, base::JobDelegate *> ./../../base/bind_internal.h:699
    #26 0x5583a52e9eff in RunImpl<const (lambda at ../../gin/v8_platform.cc:456:25) &, const std::__1::tuple<std::__1::unique_ptr<v8::JobTask, std::__1::default_delete<v8::JobTask> > > &, 0UL> ./../../base/bind_internal.h:772
    #27 0x5583a52e9eff in Run ./../../base/bind_internal.h:754
    #28 0x5583a52e9eff in ?? ??:0
    #29 0x5583a302a43d in base::internal::Invoker<base::internal::BindState<base::internal::JobTaskSource::JobTaskSource(base::Location const&, base::TaskTraits const&, base::RepeatingCallback<void (base::JobDelegate*)>, base::RepeatingCallback<unsigned long (unsigned long)>, base::internal::PooledTaskRunnerDelegate*)::$_0, base::internal::UnretainedWrapper<base::internal::JobTaskSource> >, void ()>::Run(base::internal::BindStateBase*) ./../../base/callback.h:241
    #30 0x5583a302a43d in operator() ./../../base/task/thread_pool/job_task_source.cc:100
    #31 0x5583a302a43d in Invoke<const (lambda at ../../base/task/thread_pool/job_task_source.cc:96:11) &, base::internal::JobTaskSource *> ./../../base/bind_internal.h:416
    #32 0x5583a302a43d in MakeItSo<const (lambda at ../../base/task/thread_pool/job_task_source.cc:96:11) &, base::internal::JobTaskSource *> ./../../base/bind_internal.h:699
    #33 0x5583a302a43d in RunImpl<const (lambda at ../../base/task/thread_pool/job_task_source.cc:96:11) &, const std::__1::tuple<base::internal::UnretainedWrapper<base::internal::JobTaskSource> > &, 0UL> ./../../base/bind_internal.h:772
    #34 0x5583a302a43d in Run ./../../base/bind_internal.h:754
    #35 0x5583a302a43d in ?? ??:0
    #36 0x558399200384 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/callback.h:142
    #37 0x558399200384 in RunTaskImpl ./../../base/task/common/task_annotator.cc:135
    #38 0x558399200384 in ?? ??:0
    #39 0x5583992674ab in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::SequenceToken const&) ./../../base/task/common/task_annotator.h:74
    #40 0x5583992674ab in RunTaskImpl ./../../base/task/thread_pool/task_tracker.cc:706
    #41 0x5583992674ab in ?? ??:0
    #42 0x558399268397 in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::SequenceToken const&) ./../../base/task/thread_pool/task_tracker.cc:691
    #43 0x558399268397 in ?? ??:0
    #44 0x558399266be3 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) ./../../base/task/thread_pool/task_tracker.cc:721
    #45 0x558399266be3 in RunTask ./../../base/task/thread_pool/task_tracker.cc:548
    #46 0x558399266be3 in ?? ??:0
    #47 0x558399318eed in base::internal::TaskTrackerPosix::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) ./../../base/task/thread_pool/task_tracker_posix.cc:22
    #48 0x558399318eed in ?? ??:0
    #49 0x5583992660f7 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) ./../../base/task/thread_pool/task_tracker.cc:466
    #50 0x5583992660f7 in ?? ??:0
    #51 0x55839927e4cf in base::internal::WorkerThread::RunWorker() ./../../base/task/thread_pool/worker_thread.cc:379
    #52 0x55839927e4cf in ?? ??:0
    #53 0x55839927d882 in base::internal::WorkerThread::RunPooledWorker() ./../../base/task/thread_pool/worker_thread.cc:266
    #54 0x55839927d882 in ?? ??:0
    #55 0x55839931a386 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:98
    #56 0x55839931a386 in ?? ??:0
    #57 0x7fe703158609 in start_thread /build/glibc-eX1tMB/glibc-2.31/nptl/pthread_create.c:477
    #58 0x7fe703158609 in ?? ??:0
    #59 0x7fe7012c8293 in clone ??:?
    #60 0x7fe7012c8293 in ?? ??:0

Did this work before? N/A 

Chrome version: Version 98.0.4750.0 (Official Build) dev (64-bit)  Channel: dev
OS Version: 20.04

## Timeline

### [Deleted User] (2021-12-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-12-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5732374283091968.

### do...@chromium.org (2021-12-13)

I've sent this to ClusterFuzz to take a look. +V8 clusterfuzz sheriff.

[Monorail components: Blink>JavaScript Blink>JavaScript>GarbageCollection]

### cl...@chromium.org (2021-12-13)

Detailed Report: https://clusterfuzz.com/testcase?key=5732374283091968

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7eb0fffc000a
Crash State:
  void v8::internal::MarkingVisitorBase<v8::internal::MainMarkingVisitor<v8::inter
  std::__1::pair<unsigned long, unsigned long> v8::internal::MarkCompactCollector:
  v8::internal::MarkCompactCollector::MarkLiveObjects
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=950942:950943

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5732374283091968

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### is...@chromium.org (2021-12-13)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-13)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-13)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-13)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2021-12-14)

ClusterFuzz testcase 5732374283091968 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=950948:950949

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### ma...@chromium.org (2021-12-14)

This is mistakenly marked as verified.
Removing security labels since this is only reproducible with experimental flags.

### gi...@appspot.gserviceaccount.com (2021-12-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/8c0b9b3b49b6665c641159972ef6e9c1d6163ced

commit 8c0b9b3b49b6665c641159972ef6e9c1d6163ced
Author: Manos Koukoutos <manoskouk@chromium.org>
Date: Tue Dec 14 09:02:25 2021

[wasm-gc][asm-js] Consider gc disabled for asm-js modules

An asm-js module has all wasm feature flags disabled, despite the global
flag configuration. Therefore, in WasmExportedFunction::New, we should
retrieve the enabled features from the NativeModule instead of the
flags.

Bug: chromium:1279151
Change-Id: Ic44fe535baa7cb851644457cce533c24d4c9824e
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3338256
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
Commit-Queue: Manos Koukoutos <manoskouk@chromium.org>
Cr-Commit-Position: refs/heads/main@{#78368}

[modify] https://crrev.com/8c0b9b3b49b6665c641159972ef6e9c1d6163ced/src/wasm/wasm-objects.cc
[add] https://crrev.com/8c0b9b3b49b6665c641159972ef6e9c1d6163ced/test/mjsunit/regress/wasm/regress-1279151.js


### ma...@chromium.org (2021-12-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-02-09)

An issue requiring enabling/command line arguments to enable experimental flags does not negate it from being a security bug, and security bugs should only be adjusted to bugs if it's been determine the issue is not exploitable and/or has no security implications.  
Shifting to bug-security and security_impact-none (due to being reliant on experimental flags) for VRP assessment.

### em...@gmail.com (2022-02-09)

Hi @amyressler It similar issue got a reward. Can you check this one .thanks https://bugs.chromium.org/p/chromium/issues/detail?id=980475

### am...@chromium.org (2022-02-09)

Hi emilykim@ I apologize as I don't seem to follow, what is it that you would like me to check about https://crbug.com/chromium/980475? That issue did get a reward back in 2019. I returned this one to a bug-security state so that it could be similarly handled and assessed by the VRP for a potential reward. 

### em...@gmail.com (2022-02-09)

I mean to re-evaluate my issue. 
Thanks a lot.

### am...@chromium.org (2022-02-09)

Ah okay, thanks for the clarification. Your issue has not been evaluated by the VRP; my label changes above and https://crbug.com/chromium/1279151#c15 was to help ensure it would be. :) 
This issue will be discussed at a future VRP Panel session.  

### em...@gmail.com (2022-02-09)

I mean I want the vrp to re-assess my issue.
Thanks alot.

### am...@google.com (2022-02-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-18)

Congratulations on another one, Cassidy Kim. The VRP Panel has decided to award you $5000 for this report. Thanks for your efforts and nice work! 

### am...@google.com (2022-02-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1279151?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript, Blink>JavaScript>GarbageCollection]
[Monorail components added to Component Tags custom field.]

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

### cl...@chromium.org (2026-01-08)

Removing `Clusterfuzz-ignore` hotlist from some old bugs as it's preventing Clusterfuzz from filing similar bugs.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058210)*
