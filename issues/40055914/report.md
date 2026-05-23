# AddressSanitizer: use-after-poison long_task_detector.cc:46 in blink::LongTaskDetector::DidProcessTask

| Field | Value |
|-------|-------|
| **Issue ID** | [40055914](https://issues.chromium.org/issues/40055914) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Loader |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | yh...@chromium.org |
| **Created** | 2021-05-18 |
| **Bounty** | $7,500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4494.0 Safari/537.36

Steps to reproduce the problem:
#TestOn
Windows NT 10.0; Win64; x64
gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-880310.zip

#Reproduce
I did not provide POC because there is no stable reproducible sample, but also because the method in the video can be reproduced without POC.
See attached video

What is the expected behavior?

What went wrong?
#Analysis
third_party/blink/renderer/core/loader/long_task_detector.cc
```
void LongTaskDetector::DidProcessTask(base::TimeTicks start_time,
                                      base::TimeTicks end_time) {
  if ((end_time - start_time) < LongTaskDetector::kLongTaskThreshold)
    return;

  for (auto& observer : observers_) {
    observer->OnLongTaskDetected(start_time, end_time);		//[1]
  }
}

void LongTaskDetector::UnregisterObserver(LongTaskObserver* observer) {
  DCHECK(IsMainThread());
  observers_.erase(observer);		//[2]
  if (observers_.size() == 0) {
    Thread::Current()->RemoveTaskTimeObserver(this);
  }
}

[0x0]   blink_core!blink::LongTaskDetector::UnregisterObserver + 0x9b   
[0x1]   blink_core!blink::InteractiveDetector::OnTimeToInteractiveDetected + 0x47   
[0x2]   blink_core!blink::InteractiveDetector::CheckTimeToInteractiveReached + 0x1e6   
[0x3]   blink_core!blink::InteractiveDetector::TimeToInteractiveTimerFired + 0x71   
[0x4]   blink_core!blink::InteractiveDetector::StartOrPostponeCITimer + 0x1b9   
[0x5]   blink_core!blink::InteractiveDetector::OnLongTaskDetected + 0xfb   
[0x6]   blink_core!blink::LongTaskDetector::DidProcessTask + 0x21c   
[0x7]   base!base::sequence_manager::internal::SequenceManagerImpl::NotifyDidProcessTask + 0x7a9   
[0x8]   base!base::sequence_manager::internal::SequenceManagerImpl::DidRunTask + 0x28e   
[0x9]   base!base::sequence_manager::internal::ThreadControllerImpl::DoWork + 0x67c  

//In some special cases, OnLongTaskDetected[1] will eventually be called to UnregisterObserver, and the function UnregisterObserver will be modified
observers_[2] causes the OnLongTaskDetected iterator in the function OnLongTaskDetected to be invalid, resulting in a security vulnerability.

//In order to easily reproduce the problem, I invalidated the following code logic

if ((end_time - start_time) < LongTaskDetector::kLongTaskThreshold)
return;

=================================================================
==8904==ERROR: AddressSanitizer: use-after-poison on address 0x7ebf3fdca9f0 at pc 0x7ffa0e7fc971 bp 0x000043e1f090 sp 0x000043e1f0d8
READ of size 8 at 0x7ebf3fdca9f0 thread T36
==8904==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ffa0e7fc970 in blink::LongTaskDetector::DidProcessTask C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\long_task_detector.cc:46
    #1 0x7ffa033bfccf in base::sequence_manager::internal::SequenceManagerImpl::NotifyDidProcessTask C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\sequence_manager_impl.cc:871
    #2 0x7ffa033bf1ec in base::sequence_manager::internal::SequenceManagerImpl::DidRunTask C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\sequence_manager_impl.cc:677
    #3 0x7ffa05b0cc31 in base::sequence_manager::internal::ThreadControllerImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_impl.cc:206
    #4 0x7ffa05b0f7d3 in base::internal::Invoker<base::internal::BindState<void (base::sequence_manager::internal::ThreadControllerImpl::*)(base::sequence_manager::internal::ThreadControllerImpl::WorkType),base::WeakPtr<base::sequence_manager::internal::ThreadControllerImpl>,base::sequence_manager::internal::ThreadControllerImpl::WorkType>,void ()>::Run C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:703
    #5 0x7ffa033b101a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178
    #6 0x7ffa05b11a5f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:357
    #7 0x7ffa05b110d9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:270
    #8 0x7ffa03461c70 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:220
    #9 0x7ffa0345fe58 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #10 0x7ffa05b13104 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:466
    #11 0x7ffa03336ba3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #12 0x7ffa033f78f9 in base::Thread::Run C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:312
    #13 0x7ffa033f7e10 in base::Thread::ThreadMain C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:383
    #14 0x7ffa03482a1f in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:121
    #15 0x7ff6c9dddac7 in __asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_thread.cpp:279
    #16 0x7ffa6aa04d2d in BaseThreadInitThunk+0x1d (C:\WINDOWS\System32\KERNEL32.DLL+0x180014d2d)
    #17 0x7ffa6b715a7a in RtlUserThreadStart+0x2a (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180065a7a)

Address 0x7ebf3fdca9f0 is a wild pointer inside of access range of size 0x000000000008.
SUMMARY: AddressSanitizer: use-after-poison C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\long_task_detector.cc:46 in blink::LongTaskDetector::DidProcessTask
Shadow bytes around the buggy address:
  0x0fd867fb94e0: 00 00 00 00 00 00 00 00 00 f7 00 00 f7 00 00 00
  0x0fd867fb94f0: 00 f7 00 f7 00 00 f7 00 00 00 00 f7 00 f7 00 00
  0x0fd867fb9500: f7 00 f7 00 00 f7 00 f7 00 00 f7 00 00 00 00 f7
  0x0fd867fb9510: 00 00 f7 00 00 00 00 f7 00 00 00 00 00 00 00 00
  0x0fd867fb9520: f7 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0fd867fb9530: 00 f7 00 00 00 00 00 00 00 00 f7 f7 f7 f7[f7]f7
  0x0fd867fb9540: f7 f7 f7 f7 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fd867fb9550: 00 00 00 00 f7 00 00 00 00 f7 00 00 00 00 00 00
  0x0fd867fb9560: 00 00 f7 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fd867fb9570: 00 00 00 f7 00 00 f7 00 00 00 00 f7 00 00 00 00
  0x0fd867fb9580: 00 00 00 00 f7 00 00 00 00 00 00 00 00 00 00 00
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
  Shadow gap:              cc
Thread T36 created by T0 here:
    #0 0x7ff6c9dde5b2 in __asan_wrap_CreateThread C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:146
    #1 0x7ffa03481dfe in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:185
    #2 0x7ffa033f6bca in base::Thread::StartWithOptions C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:187
    #3 0x7ff9fd6327ba in content::RenderProcessHostImpl::Init C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_process_host_impl.cc:1861
    #4 0x7ff9fd6155d2 in content::RenderFrameHostManager::InitRenderView C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:2806
    #5 0x7ff9fd60cdb5 in content::RenderFrameHostManager::ReinitializeMainRenderFrame C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:3032
    #6 0x7ff9fd60ab48 in content::RenderFrameHostManager::GetFrameHostForNavigation C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:1052
    #7 0x7ff9fd60970c in content::RenderFrameHostManager::DidCreateNavigationRequest C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:807
    #8 0x7ff9fd38f5e5 in content::FrameTreeNode::CreatedNavigationRequest C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\frame_tree_node.cc:532
    #9 0x7ff9fd549c5f in content::Navigator::Navigate C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigator.cc:596
    #10 0x7ff9fd4b957e in content::NavigationControllerImpl::NavigateWithoutEntry C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigation_controller_impl.cc:3302
    #11 0x7ff9fd4b8734 in content::NavigationControllerImpl::LoadURLWithParams C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigation_controller_impl.cc:1136
    #12 0x7ffa055fafb9 in `anonymous namespace'::LoadURLInContents C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser_navigator.cc:386
    #13 0x7ffa055f8316 in Navigate C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser_navigator.cc:658
    #14 0x7ffa0cacc291 in StartupBrowserCreatorImpl::OpenTabsInBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:313
    #15 0x7ffa0cace06f in StartupBrowserCreatorImpl::RestoreOrCreateBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:582
    #16 0x7ffa0cacb438 in StartupBrowserCreatorImpl::DetermineURLsAndLaunch C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:429
    #17 0x7ffa0cacaaa0 in StartupBrowserCreatorImpl::Launch C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:218
    #18 0x7ffa08abce4e in StartupBrowserCreator::LaunchBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:689
    #19 0x7ffa08ac37ff in StartupBrowserCreator::ProcessLastOpenedProfiles C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1259
    #20 0x7ffa08ac2d43 in StartupBrowserCreator::LaunchBrowserForLastProfiles C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1209
    #21 0x7ffa08abc349 in StartupBrowserCreator::ProcessCmdLineImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1127
    #22 0x7ffa08aba973 in StartupBrowserCreator::Start C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:624
    #23 0x7ffa05c4c310 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1647
    #24 0x7ffa05c49dbe in ChromeBrowserMainParts::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1039
    #25 0x7ff9fcb471de in content::BrowserMainLoop::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:960
    #26 0x7ff9fd8df283 in content::StartupTaskRunner::RunAllTasksNow C:\b\s\w\ir\cache\builder\src\content\browser\startup_task_runner.cc:41
    #27 0x7ff9fcb466e8 in content::BrowserMainLoop::CreateStartupTasks C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:868
    #28 0x7ff9fcb4e125 in content::BrowserMainRunnerImpl::Initialize C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:131
    #29 0x7ff9fcb42cd4 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:43
    #30 0x7ffa030ccbe8 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:597
    #31 0x7ffa030cf51f in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1080
    #32 0x7ffa030ce72f in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:955
    #33 0x7ffa030cba97 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:372
    #34 0x7ffa030cc08b in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:398
    #35 0x7ff9f907145a in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:151
    #36 0x7ff6c9d35bd1 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169
    #37 0x7ff6c9d32c1d in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:369
    #38 0x7ff6ca11bb7f in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #39 0x7ffa6aa04d2d in BaseThreadInitThunk+0x1d (C:\WINDOWS\System32\KERNEL32.DLL+0x180014d2d)
    #40 0x7ffa6b715a7a in RtlUserThreadStart+0x2a (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180065a7a)

==8904==ABORTING

```
#Patch
```
diff --git a/long_task_detector.cc b/long_task_detector.cc
index 996a7c2..0ba2885 100644
--- a/domato-master_forhtml/webidl_parser/crashes/minicase/4/long_task_detector.cc
+++ b/domato-master_forhtml/webidl_parser/crashes/minicase/4/long_task_detector.cc
@@ -33,7 +33,10 @@ void LongTaskDetector::DidProcessTask(base::TimeTicks start_time,
                                       base::TimeTicks end_time) {
   if ((end_time - start_time) < LongTaskDetector::kLongTaskThreshold)
     return;
-  for (auto& observer : observers_) {
+
+  HeapHashSet<Member<LongTaskObserver>> observers;
+  observers.swap(observers);
+  for (auto& observer : observers) {
     observer->OnLongTaskDetected(start_time, end_time);
   }
 }
```

Did this work before? N/A 

Chrome version: 92.0.4494.0  Channel: dev
OS Version: 10.0
Flash Version: 

fuzz22.debug.webm is test on debug version
fuzz22.release.asan.webm test on gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-880310.zip

## Attachments

- [182651.png](attachments/182651.png) (image/png, 226.8 KB)
- [182952.png](attachments/182952.png) (image/png, 161.6 KB)
- [fuzz22.debug.webm](attachments/fuzz22.debug.webm) (video/webm, 3.2 MB)
- [fuzz22.release.asan.webm](attachments/fuzz22.release.asan.webm) (video/webm, 9.3 MB)
- [patch.diff](attachments/patch.diff) (text/plain, 717 B)

## Timeline

### [Deleted User] (2021-05-18)

[Empty comment from Monorail migration]

### m....@gmail.com (2021-05-18)

Try to provide a repair patch, and make a copy if it is possible to modify the iterator.

### va...@chromium.org (2021-05-19)

verwaest@ for UAP, yhirano@ based on OWNERS.

[Monorail components: Blink>Loader]

### va...@chromium.org (2021-05-20)

[Empty comment from Monorail migration]

### ve...@chromium.org (2021-05-20)

Reassigning to yhirano. Unsure why this was assigned to me.

### yh...@chromium.org (2021-05-20)

Sorry I don't understand the problem even with the video. Can you provide a bit more textual explanation?

What's the relationship between the stack trace the Address Sanitizer generated and the stack trace seemingly coming from the debugger?

### m....@gmail.com (2021-05-20)

The stack trace shows the execution path from DidProcessTask[1] to UnregisterObserver[2], which is the root cause of the vulnerability.
The ASAN log can only see the access violation at DidProcessTask[1] due to the invalidation of the iterator, and it is impossible to see why the iterator is invalid.
```
void LongTaskDetector::DidProcessTask(base::TimeTicks start_time,
                                      base::TimeTicks end_time) {
  if ((end_time - start_time) < LongTaskDetector::kLongTaskThreshold)
    return;

  for (auto& observer : observers_) {
    observer->OnLongTaskDetected(start_time, end_time);		//[1]
  }
}

void LongTaskDetector::UnregisterObserver(LongTaskObserver* observer) {
  DCHECK(IsMainThread());
  observers_.erase(observer);		//[2]
  if (observers_.size() == 0) {
    Thread::Current()->RemoveTaskTimeObserver(this);
  }
}
```

### yh...@chromium.org (2021-05-20)

Ah I see thank you. Regarding your proposal I think we need to copy the observers instead of swapping.

### yh...@chromium.org (2021-05-20)

https://chromium-review.googlesource.com/c/chromium/src/+/2909934

### m....@gmail.com (2021-05-20)

Yes, you are right. I meant to make a copy. I misunderstood the function of the swapping function.

### yh...@chromium.org (2021-05-20)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/702f4d4ddb963cafb0d133972282dfc803510b75

commit 702f4d4ddb963cafb0d133972282dfc803510b75
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Thu May 20 15:21:39 2021

[LongTaskDetector] Remove container mutation during iteration

On LongTaskDetector, we call OnLongTaskDetected for all registered
observers. Some observers call LongTaskDetector::UnregisterObserver
in the callback, which is problematic because container mutation is
not allowed during iteration.

Copy the observer set to avoid the violation.

Bug: 1210487
Change-Id: Iccea748ac144def6884be8cf542cdc3572bed81a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2909934
Reviewed-by: Deep Roy <dproy@chromium.org>
Reviewed-by: Nicolás Peña Moreno <npm@chromium.org>
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/heads/master@{#885033}

[modify] https://crrev.com/702f4d4ddb963cafb0d133972282dfc803510b75/third_party/blink/renderer/core/loader/long_task_detector.cc
[modify] https://crrev.com/702f4d4ddb963cafb0d133972282dfc803510b75/third_party/blink/renderer/core/loader/long_task_detector_test.cc


### ad...@google.com (2021-05-20)

yhirano@ do you believe this problem exists in M90 or earlier, or is it more recently introduced than that? I'm asking because we need to set the Security_Impact label appropriately, in order to drive the merge & release note processes right. Thanks!

### [Deleted User] (2021-05-20)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yh...@chromium.org (2021-05-21)

This is a long-standing issue.

### yh...@chromium.org (2021-05-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-21)

This bug requires manual review: We are only 3 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: benmason@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yh...@chromium.org (2021-05-21)

1. Yes
2. https://chromium-review.googlesource.com/c/chromium/src/+/2909934
3. No - it's hard for me to reproduce. I wrote a unittest.
4. No
5. This is a fix for a stability issue with security implication.
6. No
7. N/A
8. No

### ad...@google.com (2021-05-21)

Thanks. Do you believe this is fully fixed? If so please mark it as Fixed - https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/security-labels.md#TOC-Merge-labels

### [Deleted User] (2021-05-22)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yh...@chromium.org (2021-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-24)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8097e73295a88e64d8318d982847a5e4f2bcc4d2

commit 8097e73295a88e64d8318d982847a5e4f2bcc4d2
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Tue May 25 09:45:50 2021

Reduce memory consumption on LongTaskObserver::DidProcessTask

https://crrev.com/c/2909934 fixed a security issue, but it introduced a
copy operation for each DidProcessTask for a long task. We see a memory
regression on the change, and this is an attempt to mitigate the
regression.

Bug: 1210487, 1211539
Change-Id: Ib9101e29d70fadb11b7967754e847bb5cc754feb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2915153
Reviewed-by: Benoit L <lizeb@chromium.org>
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/heads/master@{#886221}

[modify] https://crrev.com/8097e73295a88e64d8318d982847a5e4f2bcc4d2/third_party/blink/renderer/core/loader/long_task_detector.cc
[modify] https://crrev.com/8097e73295a88e64d8318d982847a5e4f2bcc4d2/third_party/blink/renderer/core/loader/long_task_detector.h
[modify] https://crrev.com/8097e73295a88e64d8318d982847a5e4f2bcc4d2/third_party/blink/renderer/core/loader/long_task_detector_test.cc


### ad...@google.com (2021-05-26)

https://crbug.com/chromium/1210487#c24 landed after M92 branch point, so adding merge request for M92 for later consideration.

### [Deleted User] (2021-05-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-27)

Your change meets the bar and is auto-approved for M92. Please go ahead and merge the CL to branch 4515 (refs/branch-heads/4515) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-31)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-06-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d5c4282bc577aad7490407a1f15cc79f3ac24492

commit d5c4282bc577aad7490407a1f15cc79f3ac24492
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Tue Jun 01 06:17:17 2021

Reduce memory consumption on LongTaskObserver::DidProcessTask

https://crrev.com/c/2909934 fixed a security issue, but it introduced a
copy operation for each DidProcessTask for a long task. We see a memory
regression on the change, and this is an attempt to mitigate the
regression.

(cherry picked from commit 8097e73295a88e64d8318d982847a5e4f2bcc4d2)

Bug: 1210487, 1211539
Change-Id: Ib9101e29d70fadb11b7967754e847bb5cc754feb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2915153
Reviewed-by: Benoit L <lizeb@chromium.org>
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#886221}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2928691
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4515@{#180}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/d5c4282bc577aad7490407a1f15cc79f3ac24492/third_party/blink/renderer/core/loader/long_task_detector.cc
[modify] https://crrev.com/d5c4282bc577aad7490407a1f15cc79f3ac24492/third_party/blink/renderer/core/loader/long_task_detector.h
[modify] https://crrev.com/d5c4282bc577aad7490407a1f15cc79f3ac24492/third_party/blink/renderer/core/loader/long_task_detector_test.cc


### ad...@google.com (2021-06-03)

Approving merge to M91. Please merge to branch 4472 as we plan to cut a security refresh release tomorrow.

### pb...@google.com (2021-06-03)

Your change has been approved for M91. Please go ahead and merge the CL to M91 branch : 4472 (refs/branch-heads/4472) manually asap.

### yh...@chromium.org (2021-06-04)

Now the first CL is being merged. It fixes the security issue but has a performance regression (see https://crbug.com/chromium/1211539). I'm wondering I need to merge d5c4282bc577aad7490407a1f15cc79f3ac24492, the fix for the performance regression, too. adetaylor@, what do you think?

### gi...@appspot.gserviceaccount.com (2021-06-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e88c656a9fb4a7bb1c66ddcedae8049a448ebef4

commit e88c656a9fb4a7bb1c66ddcedae8049a448ebef4
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Fri Jun 04 16:50:25 2021

[LongTaskDetector] Remove container mutation during iteration

On LongTaskDetector, we call OnLongTaskDetected for all registered
observers. Some observers call LongTaskDetector::UnregisterObserver
in the callback, which is problematic because container mutation is
not allowed during iteration.

Copy the observer set to avoid the violation.

(cherry picked from commit 702f4d4ddb963cafb0d133972282dfc803510b75)

Bug: 1210487
Change-Id: Iccea748ac144def6884be8cf542cdc3572bed81a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2909934
Reviewed-by: Deep Roy <dproy@chromium.org>
Reviewed-by: Nicolás Peña Moreno <npm@chromium.org>
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#885033}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2939704
Auto-Submit: Yutaka Hirano <yhirano@chromium.org>
Owners-Override: Prudhvi Kumar Bommana <pbommana@google.com>
Reviewed-by: Prudhvi Kumar Bommana <pbommana@google.com>
Cr-Commit-Position: refs/branch-heads/4472@{#1443}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/e88c656a9fb4a7bb1c66ddcedae8049a448ebef4/third_party/blink/renderer/core/loader/long_task_detector.cc
[modify] https://crrev.com/e88c656a9fb4a7bb1c66ddcedae8049a448ebef4/third_party/blink/renderer/core/loader/long_task_detector_test.cc


### am...@chromium.org (2021-06-07)

hi yhirano@, adetaylor@ is OOO, so I am stepping in. The fix for the performance regression looks like it's had a few days in canary, so yes, please go ahead and merge it for 91, branch 4472. We are doing the m91 respin soon, so please go ahead and merge as soon as possible. 

### gi...@appspot.gserviceaccount.com (2021-06-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7be6a34fe2f01af881bb074bc616bf5b6b5f7c31

commit 7be6a34fe2f01af881bb074bc616bf5b6b5f7c31
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Tue Jun 08 07:29:38 2021

Reduce memory consumption on LongTaskObserver::DidProcessTask

https://crrev.com/c/2909934 fixed a security issue, but it introduced a
copy operation for each DidProcessTask for a long task. We see a memory
regression on the change, and this is an attempt to mitigate the
regression.

(cherry picked from commit 8097e73295a88e64d8318d982847a5e4f2bcc4d2)

Bug: 1210487, 1211539
Change-Id: Ib9101e29d70fadb11b7967754e847bb5cc754feb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2915153
Reviewed-by: Benoit L <lizeb@chromium.org>
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#886221}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2944320
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4472@{#1460}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/7be6a34fe2f01af881bb074bc616bf5b6b5f7c31/third_party/blink/renderer/core/loader/long_task_detector.cc
[modify] https://crrev.com/7be6a34fe2f01af881bb074bc616bf5b6b5f7c31/third_party/blink/renderer/core/loader/long_task_detector.h
[modify] https://crrev.com/7be6a34fe2f01af881bb074bc616bf5b6b5f7c31/third_party/blink/renderer/core/loader/long_task_detector_test.cc


### am...@chromium.org (2021-06-08)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-08)

[Empty comment from Monorail migration]

### vs...@google.com (2021-06-09)

[Empty comment from Monorail migration]

### gi...@google.com (2021-06-09)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-06-10)

Congratulations - the VRP Panel has decided to award you $7500 for this report. Nice work!

### gi...@appspot.gserviceaccount.com (2021-06-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b7a1f498f17ef4a617ff7c1133c4b1d8785f9434

commit b7a1f498f17ef4a617ff7c1133c4b1d8785f9434
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Fri Jun 11 08:05:05 2021

[M90-LTS][LongTaskDetector] Remove container mutation during iteration

On LongTaskDetector, we call OnLongTaskDetected for all registered
observers. Some observers call LongTaskDetector::UnregisterObserver
in the callback, which is problematic because container mutation is
not allowed during iteration.

Copy the observer set to avoid the violation.

(cherry picked from commit 702f4d4ddb963cafb0d133972282dfc803510b75)

(cherry picked from commit e88c656a9fb4a7bb1c66ddcedae8049a448ebef4)

Bug: 1210487
Change-Id: Iccea748ac144def6884be8cf542cdc3572bed81a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2909934
Reviewed-by: Deep Roy <dproy@chromium.org>
Reviewed-by: Nicolás Peña Moreno <npm@chromium.org>
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#885033}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2939704
Auto-Submit: Yutaka Hirano <yhirano@chromium.org>
Owners-Override: Prudhvi Kumar Bommana <pbommana@google.com>
Reviewed-by: Prudhvi Kumar Bommana <pbommana@google.com>
Cr-Original-Commit-Position: refs/branch-heads/4472@{#1443}
Cr-Original-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2945126
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1518}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/b7a1f498f17ef4a617ff7c1133c4b1d8785f9434/third_party/blink/renderer/core/loader/long_task_detector.cc
[modify] https://crrev.com/b7a1f498f17ef4a617ff7c1133c4b1d8785f9434/third_party/blink/renderer/core/loader/long_task_detector_test.cc


### gi...@appspot.gserviceaccount.com (2021-06-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1856470e257006c9a770d01ceb216f706683dcfd

commit 1856470e257006c9a770d01ceb216f706683dcfd
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Fri Jun 11 08:07:55 2021

[M86-LTS][LongTaskDetector] Remove container mutation during iteration

On LongTaskDetector, we call OnLongTaskDetected for all registered
observers. Some observers call LongTaskDetector::UnregisterObserver
in the callback, which is problematic because container mutation is
not allowed during iteration.

Copy the observer set to avoid the violation.

(cherry picked from commit 702f4d4ddb963cafb0d133972282dfc803510b75)

(cherry picked from commit e88c656a9fb4a7bb1c66ddcedae8049a448ebef4)

Bug: 1210487
Change-Id: Iccea748ac144def6884be8cf542cdc3572bed81a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2909934
Reviewed-by: Deep Roy <dproy@chromium.org>
Reviewed-by: Nicolás Peña Moreno <npm@chromium.org>
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#885033}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2939704
Auto-Submit: Yutaka Hirano <yhirano@chromium.org>
Owners-Override: Prudhvi Kumar Bommana <pbommana@google.com>
Reviewed-by: Prudhvi Kumar Bommana <pbommana@google.com>
Cr-Original-Commit-Position: refs/branch-heads/4472@{#1443}
Cr-Original-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2945787
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1669}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/1856470e257006c9a770d01ceb216f706683dcfd/third_party/blink/renderer/core/loader/long_task_detector.cc
[modify] https://crrev.com/1856470e257006c9a770d01ceb216f706683dcfd/third_party/blink/renderer/core/loader/long_task_detector_test.cc


### gi...@appspot.gserviceaccount.com (2021-06-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9037876f53217bb229b0998e5110bc5d30b59e37

commit 9037876f53217bb229b0998e5110bc5d30b59e37
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Fri Jun 11 08:42:36 2021

[M86-LTS] Reduce memory consumption on LongTaskObserver::DidProcessTask

https://crrev.com/c/2909934 fixed a security issue, but it introduced a
copy operation for each DidProcessTask for a long task. We see a memory
regression on the change, and this is an attempt to mitigate the
regression.

(cherry picked from commit 8097e73295a88e64d8318d982847a5e4f2bcc4d2)

(cherry picked from commit 7be6a34fe2f01af881bb074bc616bf5b6b5f7c31)

Bug: 1210487, 1211539
Change-Id: Ib9101e29d70fadb11b7967754e847bb5cc754feb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2915153
Reviewed-by: Benoit L <lizeb@chromium.org>
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#886221}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2944320
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Original-Commit-Position: refs/branch-heads/4472@{#1460}
Cr-Original-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2952502
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1670}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/9037876f53217bb229b0998e5110bc5d30b59e37/third_party/blink/renderer/core/loader/long_task_detector.cc
[modify] https://crrev.com/9037876f53217bb229b0998e5110bc5d30b59e37/third_party/blink/renderer/core/loader/long_task_detector.h
[modify] https://crrev.com/9037876f53217bb229b0998e5110bc5d30b59e37/third_party/blink/renderer/core/loader/long_task_detector_test.cc


### gi...@appspot.gserviceaccount.com (2021-06-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fad297a48aceb4efa1b43ea1e0fdfdbe25ecf515

commit fad297a48aceb4efa1b43ea1e0fdfdbe25ecf515
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Fri Jun 11 08:42:15 2021

[M90-LTS] Reduce memory consumption on LongTaskObserver::DidProcessTask

https://crrev.com/c/2909934 fixed a security issue, but it introduced a
copy operation for each DidProcessTask for a long task. We see a memory
regression on the change, and this is an attempt to mitigate the
regression.

(cherry picked from commit 8097e73295a88e64d8318d982847a5e4f2bcc4d2)

(cherry picked from commit 7be6a34fe2f01af881bb074bc616bf5b6b5f7c31)

Bug: 1210487, 1211539
Change-Id: Ib9101e29d70fadb11b7967754e847bb5cc754feb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2915153
Reviewed-by: Benoit L <lizeb@chromium.org>
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#886221}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2944320
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Original-Commit-Position: refs/branch-heads/4472@{#1460}
Cr-Original-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2948750
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1520}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/fad297a48aceb4efa1b43ea1e0fdfdbe25ecf515/third_party/blink/renderer/core/loader/long_task_detector.cc
[modify] https://crrev.com/fad297a48aceb4efa1b43ea1e0fdfdbe25ecf515/third_party/blink/renderer/core/loader/long_task_detector.h
[modify] https://crrev.com/fad297a48aceb4efa1b43ea1e0fdfdbe25ecf515/third_party/blink/renderer/core/loader/long_task_detector_test.cc


### gi...@appspot.gserviceaccount.com (2021-06-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9037876f53217bb229b0998e5110bc5d30b59e37

commit 9037876f53217bb229b0998e5110bc5d30b59e37
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Fri Jun 11 08:42:36 2021

[M86-LTS] Reduce memory consumption on LongTaskObserver::DidProcessTask

https://crrev.com/c/2909934 fixed a security issue, but it introduced a
copy operation for each DidProcessTask for a long task. We see a memory
regression on the change, and this is an attempt to mitigate the
regression.

(cherry picked from commit 8097e73295a88e64d8318d982847a5e4f2bcc4d2)

(cherry picked from commit 7be6a34fe2f01af881bb074bc616bf5b6b5f7c31)

Bug: 1210487, 1211539
Change-Id: Ib9101e29d70fadb11b7967754e847bb5cc754feb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2915153
Reviewed-by: Benoit L <lizeb@chromium.org>
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#886221}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2944320
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Original-Commit-Position: refs/branch-heads/4472@{#1460}
Cr-Original-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2952502
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1670}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/9037876f53217bb229b0998e5110bc5d30b59e37/third_party/blink/renderer/core/loader/long_task_detector.cc
[modify] https://crrev.com/9037876f53217bb229b0998e5110bc5d30b59e37/third_party/blink/renderer/core/loader/long_task_detector.h
[modify] https://crrev.com/9037876f53217bb229b0998e5110bc5d30b59e37/third_party/blink/renderer/core/loader/long_task_detector_test.cc


### vs...@google.com (2021-06-11)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-14)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1210487?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055914)*
