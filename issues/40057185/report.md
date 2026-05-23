# SUMMARY: AddressSanitizer: use-after-poison timer.cc:217 in base::internal::TimerBase::OnScheduledTaskInvoked

| Field | Value |
|-------|-------|
| **Issue ID** | [40057185](https://issues.chromium.org/issues/40057185) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Media>Controls |
| **Platforms** | Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2021-09-06 |
| **Bounty** | $7,500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4624.0 Safari/537.36

Steps to reproduce the problem:

#TestOn
Windows NT 10.0; Win64; x64
gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-917567.zip

#Reproduce
This problem is not stable to reproduce manually. I wrote an automated script here through puppeteer, which is easier to reproduce, but nodejs needs to be installed.
The automated tool fails to give the minicase, I will try to make the minicase by hand.

1. install nodejs
2. python -m http.server 80
3. node ch.test.js D:\chrome_asan\asan-win32-release_x64-917567\chrome.exe http://localhost/poc.html
4. wait asan report

What is the expected behavior?

What went wrong?
Type of crash
browser process(SANDBOX ESCAPE!)

Did this work before? N/A 

Chrome version: 95.0.4624.0  Channel: n/a
OS Version: 10.0

#Analysis
ScheduleNewTask will call TimerBase::OnScheduledTaskInvoked as Task.
When TimerBase::OnScheduledTaskInvoked is called, the this pointer seems to have been freed. I haven't figured out why this happens. I'm still analyzing it further.

```
base/timer/timer.cc:168
void TimerBase::ScheduleNewTask(TimeDelta delay) {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
  DCHECK(!task_destruction_detector_);
  is_running_ = true;
  auto task_destruction_detector =
      std::make_unique<TaskDestructionDetector>(this);
  task_destruction_detector_ = task_destruction_detector.get();
  if (delay > TimeDelta::FromMicroseconds(0)) {
    GetTaskRunner()->PostDelayedTask(
        posted_from_,
        BindOnce(&TimerBase::OnScheduledTaskInvoked,
                 weak_ptr_factory_.GetWeakPtr(),
                 std::move(task_destruction_detector)),
        delay);
    scheduled_run_time_ = desired_run_time_ = Now() + delay;
  } else {
    GetTaskRunner()->PostTask(posted_from_,
                              BindOnce(&TimerBase::OnScheduledTaskInvoked,
                                       weak_ptr_factory_.GetWeakPtr(),
                                       std::move(task_destruction_detector)));
    scheduled_run_time_ = desired_run_time_ = TimeTicks();
  }
}

base/timer/timer.cc:210
void TimerBase::OnScheduledTaskInvoked(
    std::unique_ptr<TaskDestructionDetector> task_destruction_detector) {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);

  // The scheduled task is currently running so its destruction detector is no
  // longer needed.
  task_destruction_detector->Disable();
  task_destruction_detector_ = nullptr;
  task_destruction_detector.reset();

```

#Patch
Not yet

#asan
=================================================================
==3752==ERROR: AddressSanitizer: use-after-poison on address 0x7ef600857800 at pc 0x7ff909a3ad16 bp 0x000000bfeee0 sp 0x000000bfef28
WRITE of size 8 at 0x7ef600857800 thread T0
==3752==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ff909a3ad15 in base::internal::TimerBase::OnScheduledTaskInvoked C:\b\s\w\ir\cache\builder\src\base\timer\timer.cc:217
    #1 0x7ff909a3c7f2 in base::internal::Invoker<base::internal::BindState<void (base::internal::TimerBase::*)(std::__1::unique_ptr<base::internal::TaskDestructionDetector,std::__1::default_delete<base::internal::TaskDestructionDetector> >),base::WeakPtr<base::internal::TimerBase>,std::__1::unique_ptr<base::internal::TaskDestructionDetector,std::__1::default_delete<base::internal::TaskDestructionDetector> > >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:690
    #2 0x7ff9099ec41a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178
    #3 0x7ff90c393de2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:360
    #4 0x7ff90c393442 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:260
    #5 0x7ff90c36d347 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:39
    #6 0x7ff90c3952e5 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:467
    #7 0x7ff90996ea43 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #8 0x7ff90bea76b6 in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:265
    #9 0x7ff9057f38cd in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:973
    #10 0x7ff9057f0326 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:390
    #11 0x7ff9057f1368 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:418
    #12 0x7ff9096eb7ec in headless::`anonymous namespace'::RunContentMain C:\b\s\w\ir\cache\builder\src\headless\app\headless_shell.cc:176
    #13 0x7ff9096eb1bd in headless::RunChildProcessIfNeeded C:\b\s\w\ir\cache\builder\src\headless\app\headless_shell.cc:881
    #14 0x7ff9096e7bed in headless::HeadlessShellMain C:\b\s\w\ir\cache\builder\src\headless\app\headless_shell.cc:687
    #15 0x7ff8ff36147d in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:151
    #16 0x7ff656b85b74 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169
    #17 0x7ff656b82be8 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382
    #18 0x7ff656f751af in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #19 0x7ff9696b4d2d in BaseThreadInitThunk+0x1d (C:\WINDOWS\System32\KERNEL32.DLL+0x180014d2d)
    #20 0x7ff96ac35a7a in RtlUserThreadStart+0x2a (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180065a7a)

Address 0x7ef600857800 is a wild pointer inside of access range of size 0x000000000008.
SUMMARY: AddressSanitizer: use-after-poison C:\b\s\w\ir\cache\builder\src\base\timer\timer.cc:217 in base::internal::TimerBase::OnScheduledTaskInvoked
Shadow bytes around the buggy address:
  0x0fdf4010aeb0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 00 f7 f7 f7 f7
  0x0fdf4010aec0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdf4010aed0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdf4010aee0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdf4010aef0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
=>0x0fdf4010af00:[f7]f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 00 f7 f7
  0x0fdf4010af10: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdf4010af20: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdf4010af30: f7 f7 f7 f7 f7 f7 f7 f7 00 f7 f7 f7 f7 f7 f7 f7
  0x0fdf4010af40: f7 f7 f7 f7 f7 f7 00 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdf4010af50: f7 f7 f7 f7 f7 00 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
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
==3752==ABORTING

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 283.8 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [m1.html](attachments/m1.html) (text/plain, 43.4 KB)
- [dbg.patch1.diff](attachments/dbg.patch1.diff) (text/plain, 1.0 KB)
- [output.txt](attachments/output.txt) (text/plain, 904.3 KB)

## Timeline

### [Deleted User] (2021-09-06)

[Empty comment from Monorail migration]

### m....@gmail.com (2021-09-06)

I manually deleted some irrelevant code. If ClusterFuzz can be reproduced, you can try to make ClusterFuzz do a minicase.


1. chrome.exe --no-sandbox --js-flags='--expose_gc' --enable-blink-test-features --autoplay-policy=no-user-gesture-required --use-fake-device-for-media-stream --no-default-browser-check --disable-extensions --use-fake-ui-for-media-stream --user-data-dir=test http://localhost/m1.html
2. wait 10s
3. Click refresh if it does not reappear
ps. need h1.js




### cl...@chromium.org (2021-09-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5697974859268096.

### do...@chromium.org (2021-09-06)

Thanks for the report. I'll let ClusterFuzz have a go at minimising before triaging this further. :)

### cl...@chromium.org (2021-09-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5765477543247872.

### do...@chromium.org (2021-09-07)

Note that this is not a browser process crash: it has RenderMain in the stack trace, so it's a renderer.

### dc...@chromium.org (2021-09-07)

Any chance you're able to catch the ASan crash in a debugger? If you're able to do that, this stack frame will have information that would be helpful for tracking down the root cause / finding the right component:

    #2 0x7ff9099ec41a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178

Specifically, this value from the array which should be on the stack:

https://source.chromium.org/chromium/chromium/src/+/main:base/task/common/task_annotator.cc;l=166;drc=fef6fda96c479619c31b88a97fcf0945df4fbe30

And which function / line that program counter value corresponds to. That should tell us which code is trying to set the Timer.

(This seems likely to be an Oilpan issue; Oilpan is probably the biggest subsystem that takes advantage of poisoning/unpoisoning memory. Perhaps a regular GarbageCollected class is using the //base timer classes directly instead of the Oilpan-aware ones. Once an object is no longer reachable, it will be poisoned—but it won't be destroyed yet.)

### dc...@chromium.org (2021-09-07)

[Empty comment from Monorail migration]

### dc...@chromium.org (2021-09-07)

[Empty comment from Monorail migration]

### ml...@chromium.org (2021-09-07)

Oilpan indeed makes heavy use of poisoning to catch subtle issues of referring to an otherwise unreachable object.

Quick search here: https://source.chromium.org/search?q=filepath:third_party%2Fblink%2Frenderer%20base::OneShotTimer%7Cbase::RepeatingTimer&sq=&ss=chromium%2Fchromium%2Fsrc

Just skimming the files I found:
  MediaControlTimelineElement::render_timeline_timer_
which points back to
  &MediaControlTimelineElement::UpdateLiveTimeline

It was also relatively recently introduced:
  https://chromium-review.googlesource.com/c/chromium/src/+/3076478

This should really be using HeapTaskRunnerTimer.

dcheng:
1. Blink GC plugin doesn't check against this misbehavior. I think the main skeletons are already there and we'd only need to duplicate some pattern matcher.
2. We could also solve this pragmatically with fine-grained DEPS, i.e., remove the offending includes from the renderer DEPS and require them to be added to more local places if needed.
3. Or use proxy headers for these specific classes and add a trait that allows us to disable certain sets of types.

1. seems like a never ending story though as there's always some new type that is blindly used. (The same also applies to base::WeakPtr)

### m....@gmail.com (2021-09-07)

I compiled an ASAN version locally and added some debugging code.
I output the current this pointer and posted_from_ when the timebase is destroyed and OnScheduledTaskInvoked is called.
Through the output log, we can see that the this pointer called before the exception is "this.OnScheduledTaskInvoked->>00007EA7008BCB60,use-after-poison on address 0x7ea7008bcb70",
but the output log did not find that the this pointer was released,
so the problem is really strange, and it may be related to the garbage collection module.

```
[10684:9148:0907/152255.155:ERROR:timer.cc(215)] this.OnScheduledTaskInvoked->>00007EA7008BCB60
[10684:9148:0907/152255.155:ERROR:timer.cc(218)] OnMediaStoppedPlaying@third_party/blink/renderer/modules/media_controls/elements/media_control_timeline_element.cc:192

[10684:9148:0907/152256.161:ERROR:timer.cc(215)] this.OnScheduledTaskInvoked->>00007EA7008BCB60
==10684==ERROR: AddressSanitizer: use-after-poison on address 0x7ea7008bcb70 at pc 0x7ffe2113c1aa bp 0x00bd315fbec0 sp 0x00bd315fbf08

diff --git a/base/timer/timer.cc b/base/timer/timer.cc
index 1a4e0bc0ba1..cdbabefe7f6 100644
--- a/base/timer/timer.cc
+++ b/base/timer/timer.cc
@@ -16,6 +16,7 @@
 #include "base/threading/sequenced_task_runner_handle.h"
 #include "base/time/tick_clock.h"
 #include "build/build_config.h"
+#include "base/logging.h"
 
 namespace base {
 namespace internal {
@@ -96,6 +97,7 @@ TimerBase::TimerBase(const Location& posted_from,
 }
 
 TimerBase::~TimerBase() {
+  DLOG(ERROR)<<"this.~TimerBase->>"<<this;
   DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
   AbandonScheduledTask();
 }
@@ -209,7 +211,11 @@ void TimerBase::AbandonScheduledTask() {
 
 void TimerBase::OnScheduledTaskInvoked(
     std::unique_ptr<TaskDestructionDetector> task_destruction_detector) {
+
+  DLOG(ERROR)<<"this.OnScheduledTaskInvoked->>"<<this;
   DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
+  
+  DLOG(ERROR) << posted_from_.ToString();
 
   // The scheduled task is currently running so its destruction detector is no
   // longer needed.

```

### m....@gmail.com (2021-09-07)

All debug output information

### ml...@chromium.org (2021-09-07)

Thanks, that confirms MediaControlTimelineElement as the culprit. Re-assigning for this specific issues.

Lets think about better guarding against this mistake separately.

[Monorail components: Blink>Media>Controls]

### dc...@chromium.org (2021-09-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-07)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2021-09-07)

M94 stable RC is next week Sept 14, so please help review and see if this should be RBS if it is, please help get a fix landed to trunk asap and get it ready for merge next week

### gi...@appspot.gserviceaccount.com (2021-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/abee0e8c01c10c156e05afa093cb8146d81571f6

commit abee0e8c01c10c156e05afa093cb8146d81571f6
Author: Jazz Xu <jazzhsu@chromium.org>
Date: Wed Sep 08 11:43:10 2021

Media controls: Use HeapTaskRunnerTimer instead of RepeatingTimer.

Bug: 1246780
Change-Id: I8701b60dee78adea93fab53eb5f1bea3df6cdf95
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3147671
Reviewed-by: Tommy Steimel <steimel@chromium.org>
Commit-Queue: Jazz Xu <jazzhsu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#919206}

[modify] https://crrev.com/abee0e8c01c10c156e05afa093cb8146d81571f6/third_party/blink/renderer/modules/media_controls/elements/media_control_timeline_element.cc
[modify] https://crrev.com/abee0e8c01c10c156e05afa093cb8146d81571f6/third_party/blink/renderer/modules/media_controls/elements/media_control_timeline_element.h


### ja...@chromium.org (2021-09-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-08)

This bug requires manual review: We are only 12 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), harrysouders@(iOS), matthewjoseph@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-09-08)

hi jazzhsu@,  it appears the CL in https://crbug.com/chromium/1246780#c18 fully fixes this issue; please update to Fixed. You do not need to manually request merges for security bugs. Once they are marked as Fixed, sheriffbot will kick in and apply the appropriate merge review and request labels and allow us/me to merge review them as necessary. :) Thank you! 

### sr...@google.com (2021-09-08)

Pls answer https://crbug.com/chromium/1246780#c20 and also confirm this is working as expected tomorrow on canary. 

### ja...@chromium.org (2021-09-08)

Marking this as fixed per https://crbug.com/chromium/1246780#c21

### [Deleted User] (2021-09-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-09)

[Empty comment from Monorail migration]

### sr...@google.com (2021-09-10)

pls answer https://crbug.com/chromium/1246780#c20 for merge review

### ja...@chromium.org (2021-09-10)

1. Does your merge fit within the Merge Decision Guidelines?
    Yes

2. Links to the CLs you are requesting to merge.
    https://chromium-review.googlesource.com/c/chromium/src/+/3147671

3. Has the change landed and been verified on ToT?
    Yes
   
4. Does this change need to be merged into other active release branches (M-1, M+1)?
    No.

5. Why are these changes required in this milestone after branch?
    Security bug fix.

6. Is this a new feature?
     No.

7. If it is a new feature, is it behind a flag using finch?
     N/A

### sr...@google.com (2021-09-13)

Merge approved for M94 branch:4606 pls merge asap

### sr...@google.com (2021-09-13)

Please complete your merges to M94 asap .we are cutting stable RC build tomorrow morning at 2pm PST, so all merges should be in before that time. 

### gi...@appspot.gserviceaccount.com (2021-09-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/29cc44d253012ff47e37e9d0c673872cbe9175a9

commit 29cc44d253012ff47e37e9d0c673872cbe9175a9
Author: Jazz Xu <jazzhsu@chromium.org>
Date: Mon Sep 13 22:03:01 2021

[M94] Media controls: Use HeapTaskRunnerTimer instead of RepeatingTimer.

(cherry picked from commit abee0e8c01c10c156e05afa093cb8146d81571f6)

Bug: 1246780
Change-Id: I8701b60dee78adea93fab53eb5f1bea3df6cdf95
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3147671
Reviewed-by: Tommy Steimel <steimel@chromium.org>
Commit-Queue: Jazz Xu <jazzhsu@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#919206}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3158730
Commit-Queue: Tommy Steimel <steimel@chromium.org>
Auto-Submit: Jazz Xu <jazzhsu@chromium.org>
Cr-Commit-Position: refs/branch-heads/4606@{#1005}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/29cc44d253012ff47e37e9d0c673872cbe9175a9/third_party/blink/renderer/modules/media_controls/elements/media_control_timeline_element.cc
[modify] https://crrev.com/29cc44d253012ff47e37e9d0c673872cbe9175a9/third_party/blink/renderer/modules/media_controls/elements/media_control_timeline_element.h


### am...@google.com (2021-09-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-15)

Congratulations! The VRP Panel has decided to award you $7500 for the report. Thank you for this report and great work! 

### am...@google.com (2021-09-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-12-16)

This issue was migrated from crbug.com/chromium/1246780?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057185)*
