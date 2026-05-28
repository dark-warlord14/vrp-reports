# container overflow in Browser Process(PermissionUmaUtil::PermissionPromptResolved)

| Field | Value |
|-------|-------|
| **Issue ID** | [40056714](https://issues.chromium.org/issues/40056714) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P2 |
| **Component** | UI>Browser>Permissions |
| **Platforms** | Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2021-07-29 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36

Steps to reproduce the problem:
Chrome Version:
Chromium 93.0.4573.0
Chromium 94.0.4591.0(gs://chromium-browser-asan/linux-release/asan-linux-release-906563.zip)
OS version:
Ubuntu 20.04

1. ./chrome --incognito -user-data-dir=/tmp/xx  http://localhost:8000/crash.html
2. click "always allow popups"
3. then refresh page again.
4. after about 20 seconds,it will repro this issue.

What is the expected behavior?

What went wrong?
==1560894==ERROR: AddressSanitizer: container-overflow on address 0x602000b57a10 at pc 0x55b7e960f0b1 bp 0x7fff78b46930 sp 0x7fff78b46928
READ of size 8 at 0x602000b57a10 thread T0 (chrome)
    #0 0x55b7e960f0b0 in permissions::PermissionUmaUtil::PermissionPromptResolved(std::__1::vector<permissions::PermissionRequest*, std::__1::allocator<permissions::PermissionRequest*> > const&, content::WebContents*, permissions::PermissionAction, base::TimeDelta, permissions::PermissionPromptDisposition, absl::optional<permissions::PermissionPromptDispositionReason>, absl::optional<permissions::PermissionPrediction_Likelihood_DiscretizedLikelihood>) ./../../components/permissions/permission_uma_util.cc:171
    #1 0x55b7e960f0b0 in PermissionPromptResolved ./../../components/permissions/permission_uma_util.cc:474
    #2 0x55b7e960f0b0 in ?? ??:0
    #3 0x55b7e95fd9bc in permissions::PermissionRequestManager::FinalizeCurrentRequests(permissions::PermissionAction) ./../../components/permissions/permission_request_manager.cc:713
    #4 0x55b7e95fd9bc in ?? ??:0
    #5 0x55b7e9602ee8 in non-virtual thunk to permissions::PermissionRequestManager::Closing() ./../../components/permissions/permission_request_manager.cc:520
    #6 0x55b7e9602ee8 in ?? ??:0
    #7 0x55b7fb5ff34b in ?? ??:0
    #8 0x55b7fb5ff34b in PermissionChip::Dismiss() ./../../chrome/browser/ui/views/location_bar/permission_chip.cc:192
    #9 0x55b7fb5ff34b in ?? ??:0
    #10 0x55b7f0b90380 in base::OneShotTimer::RunUserTask() ./../../base/callback.h:98
    #11 0x55b7f0b90380 in RunUserTask ./../../base/timer/timer.cc:281
    #12 0x55b7f0b90380 in ?? ??:0
    #13 0x55b7f0b91563 in base::internal::Invoker<base::internal::BindState<void (base::internal::TimerBase::*)(std::__1::unique_ptr<base::internal::TaskDestructionDetector, std::__1::default_delete<base::internal::TaskDestructionDetector> >), base::WeakPtr<base::internal::TimerBase>, std::__1::unique_ptr<base::internal::TaskDestructionDetector, std::__1::default_delete<base::internal::TaskDestructionDetector> > >, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:509
    #14 0x55b7f0b91563 in MakeItSo<void (base::internal::TimerBase::*)(std::unique_ptr<base::internal::TaskDestructionDetector>), base::WeakPtr<base::internal::TimerBase>, std::unique_ptr<base::internal::TaskDestructionDetector> > ./../../base/bind_internal.h:668
    #15 0x55b7f0b91563 in RunImpl<void (base::internal::TimerBase::*)(std::unique_ptr<base::internal::TaskDestructionDetector>), std::tuple<base::WeakPtr<base::internal::TimerBase>, std::unique_ptr<base::internal::TaskDestructionDetector> >, 0UL, 1UL> ./../../base/bind_internal.h:721
    #16 0x55b7f0b91563 in RunOnce ./../../base/bind_internal.h:690
    #17 0x55b7f0b91563 in ?? ??:0
    #18 0x55b7f0aedc10 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/callback.h:98
    #19 0x55b7f0aedc10 in RunTask ./../../base/task/common/task_annotator.cc:178
    #20 0x55b7f0aedc10 in ?? ??:0
    #21 0x55b7f0b27f39 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:360
    #22 0x55b7f0b27f39 in ?? ??:0
    #23 0x55b7f0b276aa in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260
    #24 0x55b7f0b276aa in ?? ??:0
    #25 0x55b7f0b288e1 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() thread_controller_with_message_pump_impl.cc:?
    #26 0x55b7f0b288e1 in ?? ??:0
    #27 0x55b7f09e8469 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) ./../../base/message_loop/message_pump_glib.cc:375
    #28 0x55b7f09e8469 in WorkSourceDispatch ./../../base/message_loop/message_pump_glib.cc:125
    #29 0x55b7f09e8469 in ?? ??:0
    #30 0x7fcaf758117c in g_main_context_dispatch ??:?
    #31 0x7fcaf758117c in ?? ??:0

0x602000b57a10 is located 0 bytes inside of 8-byte region [0x602000b57a10,0x602000b57a18)
allocated by thread T0 (chrome) here:
    #0 0x55b7e2948b3d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95
    #1 0x55b7e2948b3d in ?? ??:0
    #2 0x55b7e9609544 in void std::__1::vector<permissions::PermissionRequest*, std::__1::allocator<permissions::PermissionRequest*> >::__push_back_slow_path<permissions::PermissionRequest* const&>(permissions::PermissionRequest* const&) ./../../buildtools/third_party/libc++/trunk/include/new:235
    #3 0x55b7e9609544 in __libcpp_allocate ./../../buildtools/third_party/libc++/trunk/include/new:261
    #4 0x55b7e9609544 in allocate ./../../buildtools/third_party/libc++/trunk/include/__memory/allocator.h:82
    #5 0x55b7e9609544 in allocate ./../../buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:261
    #6 0x55b7e9609544 in __split_buffer ./../../buildtools/third_party/libc++/trunk/include/__split_buffer:314
    #7 0x55b7e9609544 in __push_back_slow_path<permissions::PermissionRequest *const &> ./../../buildtools/third_party/libc++/trunk/include/vector:1625
    #8 0x55b7e9609544 in ?? ??:0
    #9 0x55b7e96040da in permissions::PermissionRequestManager::DequeueRequestIfNeeded() ./../../buildtools/third_party/libc++/trunk/include/vector:1642
    #10 0x55b7e96040da in DequeueRequestIfNeeded ./../../components/permissions/permission_request_manager.cc:564
    #11 0x55b7e96040da in ?? ??:0
    #12 0x55b7e9609354 in base::internal::Invoker<base::internal::BindState<void (permissions::PermissionRequestManager::*)(), base::WeakPtr<permissions::PermissionRequestManager> >, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:509
    #13 0x55b7e9609354 in MakeItSo<void (permissions::PermissionRequestManager::*)(), base::WeakPtr<permissions::PermissionRequestManager>> ./../../base/bind_internal.h:668
    #14 0x55b7e9609354 in RunImpl<void (permissions::PermissionRequestManager::*)(), std::tuple<base::WeakPtr<permissions::PermissionRequestManager> >, 0UL> ./../../base/bind_internal.h:721
    #15 0x55b7e9609354 in RunOnce ./../../base/bind_internal.h:690
    #16 0x55b7e9609354 in ?? ??:0
    #17 0x55b7f0aedc10 in Run ./../../base/callback.h:98
    #18 0x55b7f0aedc10 in RunTask ./../../base/task/common/task_annotator.cc:178
    #19 0x55b7f0aedc10 in ?? ??:0
    #20 0x55b7f0b27f39 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:360
    #21 0x55b7f0b27f39 in ?? ??:0
    #22 0x55b7f0b276aa in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260
    #23 0x55b7f0b276aa in ?? ??:0
    #24 0x55b7f0b288e1 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:?
    #25 0x55b7f0b288e1 in ?? ??:0
    #26 0x55b7f09e766a in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_glib.cc:405
    #27 0x55b7f09e766a in ?? ??:0
    #28 0x55b7f0b28fa4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:467
    #29 0x55b7f0b28fa4 in ?? ??:0
    #30 0x55b7f0a69281 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134
    #31 0x55b7f0a69281 in ?? ??:0
    #32 0x55b7e7bbb105 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser_main_loop.cc:996
    #33 0x55b7e7bbb105 in ?? ??:0
    #34 0x55b7e7bbfc45 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser_main_runner_impl.cc:152
    #35 0x55b7e7bbfc45 in ?? ??:0
    #36 0x55b7e7bb4e25 in content::BrowserMain(content::MainFunctionParams const&) ./../../content/browser/browser_main.cc:47
    #37 0x55b7e7bb4e25 in ?? ??:0
    #38 0x55b7ef90a115 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) ./../../content/app/content_main_runner_impl.cc:595
    #39 0x55b7ef90a115 in RunBrowser ./../../content/app/content_main_runner_impl.cc:1084
    #40 0x55b7ef90a115 in ?? ??:0
    #41 0x55b7ef9093a9 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:953
    #42 0x55b7ef9093a9 in ?? ??:0
    #43 0x55b7ef903c89 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) ./../../content/app/content_main.cc:386
    #44 0x55b7ef903c89 in ?? ??:0
    #45 0x55b7ef9041bc in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:412
    #46 0x55b7ef9041bc in ?? ??:0
    #47 0x55b7e294b65d in ChromeMain ./../../chrome/app/chrome_main.cc:151
    #48 0x55b7e294b65d in ?? ??:0
    #49 0x7fcaf57630b2 in __libc_start_main ??:?
    #50 0x7fcaf57630b2 in ?? ??:0

HINT: if you don't care about these errors you may set ASAN_OPTIONS=detect_container_overflow=0.
If you suspect a false positive see also: https://github.com/google/sanitizers/wiki/AddressSanitizerContainerOverflow.
SUMMARY: AddressSanitizer: container-overflow (/home/exp11/asan-linux-release/chrome+0x1173c0b0)
Shadow bytes around the buggy address:
  0x0c0480162ef0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa
  0x0c0480162f00: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa
  0x0c0480162f10: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa
  0x0c0480162f20: fa fa fd fd fa fa fd fd fa fa fd fa fa fa fd fa
  0x0c0480162f30: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa
=>0x0c0480162f40: fa fa[fc]fa fa fa fd fa fa fa fd fd fa fa fd fa
  0x0c0480162f50: fa fa fd fa fa fa fd fd fa fa fd fa fa fa fd fa
  0x0c0480162f60: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa
  0x0c0480162f70: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa
  0x0c0480162f80: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa
  0x0c0480162f90: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa
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
==1560894==ABORTING

Did this work before? N/A 

Chrome version: 93.0.4573.0  Channel: n/a
OS Version: 20.04

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 218 B)
- [crash2.html](attachments/crash2.html) (text/plain, 289 B)

## Timeline

### [Deleted User] (2021-07-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-07-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5742093824491520.

### me...@google.com (2021-07-30)

I wasn't able to repro this, I ran the PoC for a minute or so and didn't get a crash.

engedy: Could you please take another look? The stack contains permissions code but I'm not sure if that's the root cause. Thanks.

[Monorail components: UI>Browser>Permissions]

### [Deleted User] (2021-07-30)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-12)

engedy: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### em...@gmail.com (2021-08-13)

gs://chromium-browser-asan/linux-release/asan-linux-release-910752.zip
I tested with new canary, and still can repro this issue.
Can you try this new poc.
Thanks.

### [Deleted User] (2021-08-27)

engedy: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ct...@chromium.org (2021-09-03)

Thanks for the updated poc. I'm unfortunately unable to reproduce the crash on r910752 ASAN build using the new crash2.html. After following the repro steps, I see a new tab get repeatedly opened and closed. The location chip shows a few times on the left of the Omnibox, and then the "location denied" icon shows in the right of the Omnibox. Letting it run for a few minutes no crash occurs.

I'm not sure this will affect things, since the ASAN builds are non-official chromium builds, but could you share the "Variations" listed in chrome://version for the browser that you're able to reproduce this in, just in case there is some feature state that we're missing? Are there any notable details about your system that you are able to repro this on?

Otherwise, this may need to be a speculative fix by Permissions folks, which may take a bit longer, but the ASAN stack trace seems plausible so we should keep this open and investigate.

### [Deleted User] (2021-09-03)

[Empty comment from Monorail migration]

### en...@chromium.org (2021-09-07)

Illia, Ravjit, can you please check if this might be related to the other issue we have been looking at?

### ra...@chromium.org (2021-09-07)

I believe this issue has been fixed recently. 
@emilykim8708 could you please verify it on your side with the latest Canary build?

### [Deleted User] (2021-09-10)

[Empty comment from Monorail migration]

### em...@gmail.com (2021-09-13)

Hi, @ravjit
I tested with Chromium 96.0.4642.0(gs://chromium-browser-asan/linux-release/asan-linux-release-920642.zip),and never repro this issue again.


### el...@chromium.org (2021-09-27)

Closing the ticket as it is no longer reproducible. Feel free to reopen.

### en...@chromium.org (2021-09-27)

Actually, let us just leave this open for now. We are still in the process of discussing how to de-dupe this report against https://crbug.com/chromium/1243646, which is a parallel report of the same issue. That other report came in later, but ultimately was the one that led to us being able to identify, reproduce, and resolve this issue. We will post an update here in the next couple of days.

### en...@chromium.org (2021-09-28)

Based on manual analysis of the stack trace, its similarity to the trace from https://crbug.com/chromium/1245158 (which was merged into https://crbug.com/chromium/1243646), and confirmation in https://crbug.com/chromium/1234252#c13 that the issue is no longer reproduced using a version containing https://crrev.com/c/3136913, it seems safe to assume that this issue and https://crbug.com/chromium/1243646 share the root cause.

With that, I am going to resolve this issue by merging it into https://crbug.com/chromium/1243646, which, as mentioned above, came in later, but ultimately was the one that led to us being able to identify, reproduce, and resolve this issue.

In the next couple of days, amyressler@ will follow up on potential VRP reward consideration and circle back to you on this bug.

### am...@chromium.org (2021-09-30)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-09-30)

Hello, the VRP Panel would like to extend to you a reward for $5000 for your report. While we do normally only reward the first reporting of a bug for duplicates of an issue with the same root cause, because the later report (https://crbug.com/chromium/1243646) allowed the issue to be reliably reproduced, and root cause identified and resolved we have also rewarded and credited that report for this issue (as the fix was released in a security refresh of M93). 
This is a unique situation, so in the interest of fairness, we wanted to reward you for your efforts, but we also felt it was right to reward and credit the report that led to finding and fixing this issue. 
Thank you! 
 

### am...@google.com (2021-10-01)

[Empty comment from Monorail migration]

### em...@gmail.com (2021-10-08)

wow ,thanks for the reward.


### [Deleted User] (2022-01-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-01-04)

This issue was migrated from crbug.com/chromium/1234252?no_tracker_redirect=1

[Monorail mergedinto: crbug.com/chromium/1243646]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056714)*
