# Security:  heap-use-after-free ScriptProcessorHandler::FireProcessEvent

| Field | Value |
|-------|-------|
| **Issue ID** | [40089014](https://issues.chromium.org/issues/40089014) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>WebAudio |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | [Deleted User] |
| **Assignee** | rt...@chromium.org |
| **Created** | 2017-09-15 |
| **Bounty** | $3,000.00 |

## Description

Tested on Chrome ASAN Beta 61.0.3163.79 Linux 
asan-coverage-win32-release-501727 on Windows

==15460==ERROR: AddressSanitizer: heap-use-after-free on address 0x072299b4 at pc 0x1f059eec bp 0x052fd3dc sp 0x052fd3d0
READ of size 4 at 0x072299b4 thread T0
    #0 0x1f059eeb in WTF::Vector<blink::Member<blink::AudioBuffer>,0,blink::HeapAllocator>::at C:\b\c\b\win_asan_release_coverage\src\third_party\WebKit\Source\platform\wtf\Vector.h:1005
    #1 0x1f054e55 in blink::ScriptProcessorHandler::FireProcessEvent C:\b\c\b\win_asan_release_coverage\src\third_party\WebKit\Source\modules\webaudio\ScriptProcessorNode.cpp:255
    #2 0x1f05a26d in base::internal::Invoker<base::internal::BindState<void (blink::ScriptProcessorHandler::*)(unsigned int) __attribute__((thiscall)),WTF::UnretainedWrapper<blink::ScriptProcessorHandler,WTF::FunctionThreadAffinity::kCrossThreadAffinity>,unsigned int>,void ()>::Run C:\b\c\b\win_asan_release_coverage\src\base\bind_internal.h:331
    #3 0x16faae6c in blink::`anonymous namespace'::RunCrossThreadClosure C:\b\c\b\win_asan_release_coverage\src\third_party\WebKit\Source\platform\WebTaskRunner.cpp:34
    #4 0x16fac314 in base::internal::FunctorTraits<void (*)(WTF::Function<void (),WTF::FunctionThreadAffinity::kCrossThreadAffinity>),void>::Invoke<WTF::Function<void (),WTF::FunctionThreadAffinity::kCrossThreadAffinity> > C:\b\c\b\win_asan_release_coverage\src\base\bind_internal.h:149
    #5 0x16fac2d0 in base::internal::Invoker<base::internal::BindState<void (*)(WTF::Function<void (),WTF::FunctionThreadAffinity::kCrossThreadAffinity>),WTF::Function<void (),WTF::FunctionThreadAffinity::kCrossThreadAffinity> >,void ()>::RunOnce C:\b\c\b\win_asan_release_coverage\src\base\bind_internal.h:319
    #6 0x135516f2 in base::debug::TaskAnnotator::RunTask C:\b\c\b\win_asan_release_coverage\src\base\debug\task_annotator.cc:59
    #7 0x12cbeddb in blink::scheduler::TaskQueueManager::ProcessTaskFromWorkQueue C:\b\c\b\win_asan_release_coverage\src\third_party\WebKit\Source\platform\scheduler\base\task_queue_manager.cc:515
    #8 0x12cba299 in blink::scheduler::TaskQueueManager::DoWork C:\b\c\b\win_asan_release_coverage\src\third_party\WebKit\Source\platform\scheduler\base\task_queue_manager.cc:312
    #9 0x12ccbea9 in base::internal::Invoker<base::internal::BindState<void (blink::scheduler::TaskQueueManager::*)(bool) __attribute__((thiscall)),base::WeakPtr<blink::scheduler::TaskQueueManager>,bool>,void ()>::Run C:\b\c\b\win_asan_release_coverage\src\base\bind_internal.h:331
    #10 0x135516f2 in base::debug::TaskAnnotator::RunTask C:\b\c\b\win_asan_release_coverage\src\base\debug\task_annotator.cc:59
    #11 0x136026b6 in base::internal::IncomingTaskQueue::RunTask C:\b\c\b\win_asan_release_coverage\src\base\message_loop\incoming_task_queue.cc:151
    #12 0x134461e2 in base::MessageLoop::RunTask C:\b\c\b\win_asan_release_coverage\src\base\message_loop\message_loop.cc:406
    #13 0x13447455 in base::MessageLoop::DeferOrRunPendingTask C:\b\c\b\win_asan_release_coverage\src\base\message_loop\message_loop.cc:417
    #14 0x13447f71 in base::MessageLoop::DoWork C:\b\c\b\win_asan_release_coverage\src\base\message_loop\message_loop.cc:524
    #15 0x13609d84 in base::MessagePumpDefault::Run C:\b\c\b\win_asan_release_coverage\src\base\message_loop\message_pump_default.cc:33
    #16 0x13445180 in base::MessageLoop::Run C:\b\c\b\win_asan_release_coverage\src\base\message_loop\message_loop.cc:346
    #17 0x134ce43c in base::RunLoop::Run C:\b\c\b\win_asan_release_coverage\src\base\run_loop.cc:123
    #18 0x18da319f in content::RendererMain C:\b\c\b\win_asan_release_coverage\src\content\renderer\renderer_main.cc:220
    #19 0x132b6925 in content::RunNamedProcessTypeMain C:\b\c\b\win_asan_release_coverage\src\content\app\content_main_runner.cc:425
    #20 0x132b80b6 in content::ContentMainRunnerImpl::Run C:\b\c\b\win_asan_release_coverage\src\content\app\content_main_runner.cc:703
    #21 0x132d054e in service_manager::Main C:\b\c\b\win_asan_release_coverage\src\services\service_manager\embedder\main.cc:469
    #22 0x132b64e0 in content::ContentMain C:\b\c\b\win_asan_release_coverage\src\content\app\content_main.cc:19
    #23 0xf5712c6 in ChromeMain C:\b\c\b\win_asan_release_coverage\src\chrome\app\chrome_main.cc:122
    #24 0x1ec11c in MainDllLoader::Launch C:\b\c\b\win_asan_release_coverage\src\chrome\app\main_dll_loader_win.cc:199
    #25 0x1e1f5d in main C:\b\c\b\win_asan_release_coverage\src\chrome\app\chrome_exe_main_win.cc:275
    #26 0x60801a in __scrt_common_main_seh f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl:253
    #27 0x745d8743 in BaseThreadInitThunk+0x23 (C:\WINDOWS\System32\KERNEL32.DLL+0x18743)
    #28 0x7711582c in RtlGetAppContainerNamedObjectPath+0xfc (C:\WINDOWS\SYSTEM32\ntdll.dll+0x6582c)
    #29 0x771157fc in RtlGetAppContainerNamedObjectPath+0xcc (C:\WINDOWS\SYSTEM32\ntdll.dll+0x657fc)

0x072299b4 is located 116 bytes inside of 192-byte region [0x07229940,0x07229a00)
freed by thread T0 here:
    #0 0x5f6b38 in free e:\b\build\slave\win_upload_clang\build\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_malloc_win.cc:44
    #1 0x1f058012 in blink::ScriptProcessorHandler::~ScriptProcessorHandler C:\b\c\b\win_asan_release_coverage\src\third_party\WebKit\Source\modules\webaudio\ScriptProcessorNode.cpp:84
    #2 0x1f05815c in blink::ScriptProcessorNode::~ScriptProcessorNode C:\b\c\b\win_asan_release_coverage\src\third_party\WebKit\Source\modules\webaudio\ScriptProcessorNode.h:110
    #3 0x17588f90 in blink::FinalizerTrait<blink::EventTarget>::Finalize C:\b\c\b\win_asan_release_coverage\src\third_party\WebKit\Source\platform\heap\GCInfo.h:61
    #4 0x12bb07f2 in blink::HeapObjectHeader::Finalize C:\b\c\b\win_asan_release_coverage\src\third_party\WebKit\Source\platform\heap\HeapPage.cpp:100
    #5 0x12bba5c6 in blink::NormalPage::Sweep C:\b\c\b\win_asan_release_coverage\src\third_party\WebKit\Source\platform\heap\HeapPage.cpp:1343
    #6 0x12bb2dbc in blink::BaseArena::SweepUnsweptPage C:\b\c\b\win_asan_release_coverage\src\third_party\WebKit\Source\platform\heap\HeapPage.cpp:282
    #7 0x12bb36b9 in blink::BaseArena::CompleteSweep C:\b\c\b\win_asan_release_coverage\src\third_party\WebKit\Source\platform\heap\HeapPage.cpp:336
    #8 0x12bc4134 in blink::ThreadState::CompleteSweep C:\b\c\b\win_asan_release_coverage\src\third_party\WebKit\Source\platform\heap\ThreadState.cpp:988
    #9 0x12bd1cab in blink::ThreadState::PreSweep C:\b\c\b\win_asan_release_coverage\src\third_party\WebKit\Source\platform\heap\ThreadState.cpp:915
    #10 0x12bc54e1 in blink::ThreadState::CollectGarbage C:\b\c\b\win_asan_release_coverage\src\third_party\WebKit\Source\platform\heap\ThreadState.cpp:1584
    #11 0x1bcb74f5 in blink::V8GCController::GcEpilogue C:\b\c\b\win_asan_release_coverage\src\third_party\WebKit\Source\bindings\core\v8\V8GCController.cpp:434
    #12 0x116f8cd9 in v8::internal::Heap::PerformGarbageCollection C:\b\c\b\win_asan_release_coverage\src\v8\src\heap\heap.cc:1528
    #13 0x116f3c55 in v8::internal::Heap::CollectGarbage C:\b\c\b\win_asan_release_coverage\src\v8\src\heap\heap.cc:1226
    #14 0x116ef15e in v8::internal::Heap::HandleGCRequest C:\b\c\b\win_asan_release_coverage\src\v8\src\heap\heap.cc:1003
    #15 0x115c83b4 in v8::internal::StackGuard::HandleInterrupts C:\b\c\b\win_asan_release_coverage\src\v8\src\execution.cc:480
    #16 0x12260b9b in v8::internal::Runtime_StackGuard C:\b\c\b\win_asan_release_coverage\src\v8\src\runtime\runtime-internal.cc:297

previously allocated by thread T0 here:
    #0 0x5f6c1c in malloc e:\b\build\slave\win_upload_clang\build\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_malloc_win.cc:60
    #1 0x10112c04 in WTF::Partitions::FastMalloc C:\b\c\b\win_asan_release_coverage\src\third_party\WebKit\Source\platform\wtf\allocator\Partitions.h:120
    #2 0x1f05653c in blink::ScriptProcessorNode::ScriptProcessorNode C:\b\c\b\win_asan_release_coverage\src\third_party\WebKit\Source\modules\webaudio\ScriptProcessorNode.cpp:346
    #3 0x1f057423 in blink::ScriptProcessorNode::Create C:\b\c\b\win_asan_release_coverage\src\third_party\WebKit\Source\modules\webaudio\ScriptProcessorNode.cpp:471
    #4 0x1efd609e in blink::BaseAudioContext::createScriptProcessor C:\b\c\b\win_asan_release_coverage\src\third_party\WebKit\Source\modules\webaudio\BaseAudioContext.cpp:477
    #5 0x1e9c7798 in blink::V8BaseAudioContext::createScriptProcessorMethodCallback C:\b\c\b\win_asan_release_coverage\src\out\release\gen\blink\bindings\modules\v8\V8BaseAudioContext.cpp:862
    #6 0x107f560e in v8::internal::FunctionCallbackArguments::Call C:\b\c\b\win_asan_release_coverage\src\v8\src\api-arguments.cc:25
    #7 0x10ab56b4 in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\b\c\b\win_asan_release_coverage\src\v8\src\builtins\builtins-api.cc:112
    #8 0x10ab2299 in v8::internal::Builtin_Impl_HandleApiCall C:\b\c\b\win_asan_release_coverage\src\v8\src\builtins\builtins-api.cc:142
    #9 0x10ab1602 in v8::internal::Builtin_HandleApiCall C:\b\c\b\win_asan_release_coverage\src\v8\src\builtins\builtins-api.cc:130

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\c\b\win_asan_release_coverage\src\third_party\WebKit\Source\platform\wtf\Vector.h:1005 in WTF::Vector<blink::Member<blink::AudioBuffer>,0,blink::HeapAllocator>::at
Shadow bytes around the buggy address:
  0x30e452e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x30e452f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x30e45300: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x30e45310: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x30e45320: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
=>0x30e45330: fd fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd
  0x30e45340: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x30e45350: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x30e45360: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x30e45370: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x30e45380: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
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
==15460==ABORTING


## Attachments

- [ScriptProcessorHandler-UAF.html](attachments/ScriptProcessorHandler-UAF.html) (text/plain, 1.6 KB)

## Timeline

### cl...@chromium.org (2017-09-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5754018898116608.

### cl...@chromium.org (2017-09-15)

Detailed report: https://clusterfuzz.com/testcase?key=5754018898116608

Job Type: linux_asan_chrome_mp
Crash Type: Heap-use-after-free READ 4
Crash Address: 0x61200009a184
Crash State:
  blink::ScriptProcessorHandler::FireProcessEvent
  base::internal::Invoker<base::internal::BindState<void
  base::debug::TaskAnnotator::RunTask
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=469635:469655

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5754018898116608

See https://github.com/google/clusterfuzz-tools for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.


### me...@chromium.org (2017-09-15)

rtoy: Do you mind taking a look? Thanks.

[Monorail components: Blink>WebAudio]

### sh...@chromium.org (2017-09-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-16)

[Empty comment from Monorail migration]

### rt...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### rt...@chromium.org (2017-09-18)

I think what is happening here is that ScriptProcessorHandler::Process is running (and ScriptProcessorHandler is still valid, of course), and posts a task to run ScriptProcessorHandler::FireProcessEvent, where we pass a pointer to this methed and to the ScriptProcessorHandler object itself.

However, there is not onaudioprocess event handler assigned in the test, ScriptProcessorHandler::HasPendingActivity returns false, and the object is deleted.

This deletion happens before FireProcessEvent is called, so that FireProcessEvent has pointers to random freed memory.

+haraken:  Is there some way we can keep ScriptProcessorHandler object alive until FireProcessEvent is finished with it?

Well, one simple way is for HasPendingActivity always to return true, but I think that causes ScriptProcessorNode's to leak if no audioprocess event handler is ever assigned.

### ha...@chromium.org (2017-09-19)

Maybe can we pass WrapPeristent(scriptProcessorHandler) when posting a task? The persistent handle will keep the object alive until the task runs.



### rt...@chromium.org (2017-09-19)

Do you mean to do WrapPersistent(this) where this is the ScriptProcessorHandler object?  The compiler rightly complains because ScriptProcessorHandler is not a GCed object.



### rt...@chromium.org (2017-09-21)

Hongchan pointed out that we should probably use WrapRefPtr(this).  

This appears to work.

### bu...@chromium.org (2017-09-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/783c28d59c4c748ef9b787d4717882c90c5b227b

commit 783c28d59c4c748ef9b787d4717882c90c5b227b
Author: Raymond Toy <rtoy@chromium.org>
Date: Fri Sep 22 03:39:46 2017

Keep ScriptProcessorHandler alive across threads

When posting a task from the ScriptProcessorHandler::Process to fire a
process event, we need to keep the handler alive in case the
ScriptProcessorNode goes away (because it has no onaudioprocess
handler) and removes the its handler.

Bug: 765495
Test: 
Change-Id: Ib4fa39d7b112c7051897700a1eff9f59a4a7a054
Reviewed-on: https://chromium-review.googlesource.com/677137
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Cr-Commit-Position: refs/heads/master@{#503629}
[modify] https://crrev.com/783c28d59c4c748ef9b787d4717882c90c5b227b/third_party/WebKit/Source/modules/webaudio/ScriptProcessorNode.cpp


### cl...@chromium.org (2017-09-22)

ClusterFuzz has detected this issue as fixed in range 503623:503655.

Detailed report: https://clusterfuzz.com/testcase?key=5754018898116608

Job Type: linux_asan_chrome_mp
Crash Type: Heap-use-after-free READ 4
Crash Address: 0x61200009a184
Crash State:
  blink::ScriptProcessorHandler::FireProcessEvent
  base::internal::Invoker<base::internal::BindState<void
  base::debug::TaskAnnotator::RunTask
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=469635:469655
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=503623:503655

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5754018898116608

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### rt...@chromium.org (2017-09-22)

Clusterfuzz says it's fixed.

Requesting merge to 62 and 61.


### sh...@chromium.org (2017-09-22)

This bug requires manual review: M62 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2017-09-22)

Approving for M62. branch:3202

### bu...@chromium.org (2017-09-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/089918851f43410a378851610f424c01135cce7a

commit 089918851f43410a378851610f424c01135cce7a
Author: Raymond Toy <rtoy@chromium.org>
Date: Fri Sep 22 19:37:28 2017

Keep ScriptProcessorHandler alive across threads

When posting a task from the ScriptProcessorHandler::Process to fire a
process event, we need to keep the handler alive in case the
ScriptProcessorNode goes away (because it has no onaudioprocess
handler) and removes the its handler.

TBR=rtoy@chromium.org

(cherry picked from commit 783c28d59c4c748ef9b787d4717882c90c5b227b)

Bug: 765495
Test: 
Change-Id: Ib4fa39d7b112c7051897700a1eff9f59a4a7a054
Reviewed-on: https://chromium-review.googlesource.com/677137
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#503629}
Reviewed-on: https://chromium-review.googlesource.com/679266
Reviewed-by: Raymond Toy <rtoy@chromium.org>
Cr-Commit-Position: refs/branch-heads/3202@{#403}
Cr-Branched-From: fa6a5d87adff761bc16afc5498c3f5944c1daa68-refs/heads/master@{#499098}
[modify] https://crrev.com/089918851f43410a378851610f424c01135cce7a/third_party/WebKit/Source/modules/webaudio/ScriptProcessorNode.cpp


### cl...@chromium.org (2017-09-23)

ClusterFuzz testcase 5754018898116608 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2017-09-23)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-09-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9f22ebc7fd06e56b0cfd4feb7140c1378d76f0c4

commit 9f22ebc7fd06e56b0cfd4feb7140c1378d76f0c4
Author: Raymond Toy <rtoy@chromium.org>
Date: Mon Sep 25 17:57:34 2017

Fix compile error

Change WrapRefPtr(this) to the equivalent RefPtr<T>(this).  WrapRefPtr
was added after M62 branched.

Bug: 768201, 765495
Test: 
Change-Id: I798f71cf3f36be2228eff07aecc540c05969764f
Reviewed-on: https://chromium-review.googlesource.com/682102
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Cr-Commit-Position: refs/branch-heads/3202@{#430}
Cr-Branched-From: fa6a5d87adff761bc16afc5498c3f5944c1daa68-refs/heads/master@{#499098}
[modify] https://crrev.com/9f22ebc7fd06e56b0cfd4feb7140c1378d76f0c4/third_party/WebKit/Source/modules/webaudio/ScriptProcessorNode.cpp


### rt...@chromium.org (2017-09-26)

Requesting merge to M61. But we'll merge the version from c#19 instead of c#16.  The change from c#16 won't work because WrapRefPtr was added after M62 was branched.  The CL from c#19 should work; verified manually on M61 branch that the patch applies and the asan test case passes.

### ke...@chromium.org (2017-09-26)

Can you please provide rationale why we need this in M61? Things are very locked down for M61 at this point.

### rt...@chromium.org (2017-09-26)

I only requested because the bug is marked as Security_Impact-Stable, Security_Severity-High, and the milestone is M-61.

If this is not correct, someone should update the labels.

### go...@chromium.org (2017-09-26)

+awhalley@ (Security TPM) for M61 merge review. The change is not yet baked in Beta.

Note: M61 is already out at 100% for Desktop and Android and we're not planning stable respin unless critical issues arise.

### as...@chromium.org (2017-09-27)

[Empty comment from Monorail migration]

### ke...@chromium.org (2017-09-28)

govind@ we need to kick off stable rc today asap. can we find someone else to review on Awhalley's team? He is ooo I believe.

### ke...@chromium.org (2017-09-28)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-09-28)

+chrome-security-tpms@ for M61 merge review.

### go...@chromium.org (2017-09-28)

+asymmetric@ (Security TPM) for M61 merge review.

### aw...@google.com (2017-10-02)

I'm OK with leaving this for M62 at this point.

### aw...@chromium.org (2017-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-10-06)

Nice one!  The Chrome VRP panel decided to award $3,000 for this report.  A member of our finance team will be in touch shortly to arrange for payment.

Cheers!

### aw...@chromium.org (2017-10-06)

[Empty comment from Monorail migration]

### aw...@google.com (2017-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/765495?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089014)*
