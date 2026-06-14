# uaf in extensions

| Field | Value |
|-------|-------|
| **Issue ID** | [40052566](https://issues.chromium.org/issues/40052566) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>TaskManager |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | pm...@chromium.org |
| **Created** | 2020-06-12 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36

Steps to reproduce the problem:
1.  unzip poc.zip
2. open chrome
3. click "Settings"->"Load unpacked"
4. select unzipped folder path

What is the expected behavior?

What went wrong?

=================================================================
==21797==ERROR: AddressSanitizer: heap-use-after-free on address 0x611000451910 at pc 0x55a56f9f7c01 bp 0x7fff17dd18f0 sp 0x7fff17dd18e8
READ of size 8 at 0x611000451910 thread T0 (chrome)
    #0 0x55a56f9f7c00 in begin ./../../buildtools/third_party/libc++/trunk/include/vector:1516:30
    #1 0x55a56f9f7c00 in base::ObserverList<ProfileManagerObserver, false, true, base::internal::CheckedObserverAdapter>::RemoveObserver(ProfileManagerObserver const*) ./../../base/observer_list.h:282:33
    #2 0x55a56fe04db4 in RemoveAll ./../../base/scoped_observer.h:67:7
    #3 0x55a56fe04db4 in ScopedObserver<ProfileManager, ProfileManagerObserver, &(ProfileManager::AddObserver(ProfileManagerObserver*)), &(ProfileManager::RemoveObserver(ProfileManagerObserver*))>::~ScopedObserver() ./../../base/scoped_observer.h:48:5
    #4 0x55a56fe04c08 in task_manager::WorkerTaskProvider::~WorkerTaskProvider() ./../../chrome/browser/task_manager/providers/worker_task_provider.cc:15:41
    #5 0x55a56fe04fec in task_manager::WorkerTaskProvider::~WorkerTaskProvider() ./../../chrome/browser/task_manager/providers/worker_task_provider.cc:15:41
    #6 0x55a56fde8221 in operator() ./../../buildtools/third_party/libc++/trunk/include/memory:2378:5
    #7 0x55a56fde8221 in reset ./../../buildtools/third_party/libc++/trunk/include/memory:2633:7
    #8 0x55a56fde8221 in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/memory:2587:19
    #9 0x55a56fde8221 in destroy ./../../buildtools/third_party/libc++/trunk/include/memory:1920:64
    #10 0x55a56fde8221 in __destroy<std::__Cr::unique_ptr<task_manager::TaskProvider, std::__Cr::default_delete<task_manager::TaskProvider>>> ./../../buildtools/third_party/libc++/trunk/include/memory:1782:18
    #11 0x55a56fde8221 in destroy<std::__Cr::unique_ptr<task_manager::TaskProvider, std::__Cr::default_delete<task_manager::TaskProvider>>> ./../../buildtools/third_party/libc++/trunk/include/memory:1619:14
    #12 0x55a56fde8221 in __destruct_at_end ./../../buildtools/third_party/libc++/trunk/include/vector:426:9
    #13 0x55a56fde8221 in clear ./../../buildtools/third_party/libc++/trunk/include/vector:369:29
    #14 0x55a56fde8221 in ~__vector_base ./../../buildtools/third_party/libc++/trunk/include/vector:463:9
    #15 0x55a56fde8221 in ~vector ./../../buildtools/third_party/libc++/trunk/include/vector:555:5
    #16 0x55a56fde8221 in task_manager::TaskManagerImpl::~TaskManagerImpl() ./../../chrome/browser/task_manager/sampling/task_manager_impl.cc:117:1
    #17 0x55a56fdf2542 in CallDestructor ./../../base/lazy_instance.h:73:16
    #18 0x55a56fdf2542 in Delete ./../../base/lazy_instance.h:96:5
    #19 0x55a56fdf2542 in base::LazyInstance<task_manager::TaskManagerImpl, base::internal::DestructorAtExitLazyInstanceTraits<task_manager::TaskManagerImpl> >::OnExit(void*) ./../../base/lazy_instance.h:203:5
    #20 0x7f6282b0d9f9 in Run ./../../base/callback.h:99:12
    #21 0x7f6282b0d9f9 in base::AtExitManager::ProcessCallbacksNow() ./../../base/at_exit.cc:93:28
    #22 0x7f6282b0d6bd in base::AtExitManager::~AtExitManager() ./../../base/at_exit.cc:45:5
    #23 0x7f62793dff3c in operator() ./../../buildtools/third_party/libc++/trunk/include/memory:2378:5
    #24 0x7f62793dff3c in reset ./../../buildtools/third_party/libc++/trunk/include/memory:2633:7
    #25 0x7f62793dff3c in content::ContentMainRunnerImpl::Shutdown() ./../../content/app/content_main_runner_impl.cc:969:17
    #26 0x7f6282f5da9c in service_manager::Main(service_manager::MainParams const&) ./../../services/service_manager/embedder/main.cc:474:15
    #27 0x7f62793d9e16 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:19:10
    #28 0x55a56d5cbc94 in ChromeMain ./../../chrome/app/chrome_main.cc:110:12
    #29 0x7f624cbcd1e2 in __libc_start_main /build/glibc-t7JzpG/glibc-2.30/csu/../csu/libc-start.c:308:16

0x611000451910 is located 16 bytes inside of 232-byte region [0x611000451900,0x6110004519e8)
freed by thread T0 (chrome) here:
    #0 0x55a56d5c99ad in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160:3
    #1 0x55a56f455428 in operator() ./../../buildtools/third_party/libc++/trunk/include/memory:2378:5
    #2 0x55a56f455428 in reset ./../../buildtools/third_party/libc++/trunk/include/memory:2633:7
    #3 0x55a56f455428 in BrowserProcessImpl::StartTearDown() ./../../chrome/browser/browser_process_impl.cc:425:22
    #4 0x55a56f450ce9 in ChromeBrowserMainParts::PostMainMessageLoopRun() ./../../chrome/browser/chrome_browser_main.cc:1716:21
    #5 0x7f62773c84a6 in content::BrowserMainLoop::ShutdownThreadsAndCleanUp() ./../../content/browser/browser_main_loop.cc:1091:13
    #6 0x7f62773ce786 in content::BrowserMainRunnerImpl::Shutdown() ./../../content/browser/browser_main_runner_impl.cc:178:17
    #7 0x7f62773bf9f2 in content::BrowserMain(content::MainFunctionParams const&) ./../../content/browser/browser_main.cc:49:16
    #8 0x7f62793df989 in RunBrowserProcessMain ./../../content/app/content_main_runner_impl.cc:496:10
    #9 0x7f62793df989 in content::ContentMainRunnerImpl::RunServiceManager(content::MainFunctionParams&, bool) ./../../content/app/content_main_runner_impl.cc:941:10
    #10 0x7f62793ded21 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:839:12
    #11 0x7f6282f5d1b5 in service_manager::Main(service_manager::MainParams const&) ./../../services/service_manager/embedder/main.cc:454:29
    #12 0x7f62793d9e16 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:19:10
    #13 0x55a56d5cbc94 in ChromeMain ./../../chrome/app/chrome_main.cc:110:12
    #14 0x7f624cbcd1e2 in __libc_start_main /build/glibc-t7JzpG/glibc-2.30/csu/../csu/libc-start.c:308:16

previously allocated by thread T0 (chrome) here:
    #0 0x55a56d5c914d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x55a56f45752d in make_unique<ProfileManager, base::FilePath &> ./../../buildtools/third_party/libc++/trunk/include/memory:3043:28
    #2 0x55a56f45752d in CreateProfileManager ./../../chrome/browser/browser_process_impl.cc:1106:22
    #3 0x55a56f45752d in BrowserProcessImpl::profile_manager() ./../../chrome/browser/browser_process_impl.cc:696:5
    #4 0x55a571bd6435 in extensions::UserScriptListener::UserScriptListener() ./../../chrome/browser/extensions/user_script_listener.cc:80:26
    #5 0x55a5719a2bc2 in extensions::ChromeExtensionsBrowserClient::ChromeExtensionsBrowserClient() ./../../chrome/browser/extensions/chrome_extensions_browser_client.cc:91:32
    #6 0x55a56f452e53 in make_unique<extensions::ChromeExtensionsBrowserClient> ./../../buildtools/third_party/libc++/trunk/include/memory:3043:32
    #7 0x55a56f452e53 in BrowserProcessImpl::Init() ./../../chrome/browser/browser_process_impl.cc:285:7
    #8 0x55a56f44a383 in ChromeBrowserMainParts::PreCreateThreadsImpl() ./../../chrome/browser/chrome_browser_main.cc:882:23
    #9 0x55a56f449c80 in ChromeBrowserMainParts::PreCreateThreads() ./../../chrome/browser/chrome_browser_main.cc:742:18
    #10 0x7f62773c37f8 in content::BrowserMainLoop::PreCreateThreads() ./../../content/browser/browser_main_loop.cc:826:28
    #11 0x7f6278440758 in Run ./../../base/callback.h:99:12
    #12 0x7f6278440758 in content::StartupTaskRunner::RunAllTasksNow() ./../../content/browser/startup_task_runner.cc:41:29
    #13 0x7f62773c4895 in content::BrowserMainLoop::CreateStartupTasks() ./../../content/browser/browser_main_loop.cc:930:25
    #14 0x7f62773cdc57 in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams const&) ./../../content/browser/browser_main_runner_impl.cc:129:15
    #15 0x7f62773bf95e in content::BrowserMain(content::MainFunctionParams const&) ./../../content/browser/browser_main.cc:43:32
    #16 0x7f62793df989 in RunBrowserProcessMain ./../../content/app/content_main_runner_impl.cc:496:10
    #17 0x7f62793df989 in content::ContentMainRunnerImpl::RunServiceManager(content::MainFunctionParams&, bool) ./../../content/app/content_main_runner_impl.cc:941:10
    #18 0x7f62793ded21 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:839:12
    #19 0x7f6282f5d1b5 in service_manager::Main(service_manager::MainParams const&) ./../../services/service_manager/embedder/main.cc:454:29
    #20 0x7f62793d9e16 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:19:10
    #21 0x55a56d5cbc94 in ChromeMain ./../../chrome/app/chrome_main.cc:110:12
    #22 0x7f624cbcd1e2 in __libc_start_main /build/glibc-t7JzpG/glibc-2.30/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free (/home/yhn/chromium/chromium-src/src/out/chrome_asan_shared/chrome+0x524cc00)
Shadow bytes around the buggy address:
  0x0c22800822d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c22800822e0: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa
  0x0c22800822f0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c2280082300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2280082310: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa
=>0x0c2280082320: fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2280082330: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa
  0x0c2280082340: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x0c2280082350: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c2280082360: 00 00 fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2280082370: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
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
==21797==ABORTING

Did this work before? N/A 

Chrome version: 85.0.4151.0  Channel: n/a
OS Version: 18.04
Flash Version:

## Attachments

- poc.zip (application/octet-stream, 1.2 KB)
- background.js (text/plain, 176 B)
- manifest.json (text/plain, 228 B)
- main.html (text/plain, 55 B)
- main.js (text/plain, 100 B)

## Timeline

### cd...@gmail.com (2020-06-12)

Sorry, I forgot the last step.
It need to close the browser manually after the extension was loaded successfully.

### wf...@chromium.org (2020-06-12)

Thanks for your report. Devlin, do you know what might be happening here?

Reporter - does this extension need to be side-loaded or can it work from the extension store as well?

[Monorail components: Platform>Extensions]

### [Deleted User] (2020-06-12)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-12)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rd...@chromium.org (2020-06-12)

Thank you for the report!

I don't think this is directly extensions related.  The UAF in the trace is coming from the WorkerTaskProvider, which is part of the TaskManager.  It looks like the WorkerTaskProvider is a ProfileManagerObserver [1] and uses a ScopedObserver for that, but ends up outliving the ProfileManager.  The ProfileManager is owned by the BrowserProcessImpl and is destroyed in BrowserProcessImpl::StartTearDown()

[1] https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/task_manager/providers/worker_task_provider.h;l=34;drc=f4f5ca4a8f3940b12f6b6da979baf1172a75025c

### rd...@chromium.org (2020-06-12)

grr... hit enter too soon


Thank you for the report!

I don't think this is directly extensions related (it just uses an extension to trigger the flow).  The UAF in the trace is coming from the WorkerTaskProvider, which is part of the TaskManager.  It looks like the WorkerTaskProvider is a ProfileManagerObserver [1] and uses a ScopedObserver for that, but ends up outliving the ProfileManager.  The ProfileManager is owned by the BrowserProcessImpl and is destroyed in BrowserProcessImpl::StartTearDown() [2], but the WorkerTaskProvider is owned by the TaskManagerImpl, which is a LazyInstance with a DestructorAtExit [3].  This destructor triggers the WorkerTaskProvider destructor, which triggers the ScopedObserver dtor, which tries to remove itself as an observer of the ProfileManager, which is already destroyed - resulting in the UAF.

afakhry@, can you take a look as OWNER of the task_manager?

[1] https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/task_manager/providers/worker_task_provider.h;l=34;drc=f4f5ca4a8f3940b12f6b6da979baf1172a75025c
[2] https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/browser_process_impl.cc;l=424;drc=e7cdc5cd07d668fe31ec9072fa20f7c7b8509a7b
[3] https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/task_manager/sampling/task_manager_impl.cc;l=52-53;drc=ffc15ee0645cf733182e4b7f832bff4961d53e7a

[Monorail components: -Platform>Extensions UI>TaskManager]

### rd...@chromium.org (2020-06-12)

Also worth noting: The processes API that's being used to trigger this is only available to allowlisted extensions on stable channels (though since this is task manager code that's causing the UAF, there may be other ways of hitting it)

### af...@chromium.org (2020-06-12)

Devlin, thank you so much for the detailed analysis! 

pmonette@ can you take a look at the WorkerTaskProvider?

### pm...@chromium.org (2020-06-15)

I'll take a look at this.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/19f51b3583e526ac7d41bcd94d490aa9d3e4334a

commit 19f51b3583e526ac7d41bcd94d490aa9d3e4334a
Author: Patrick Monette <pmonette@chromium.org>
Date: Thu Jun 18 20:18:57 2020

WorkerTaskProvider: Don't unregister from ProfileManager if null

The ordering between the destruction of each WorkerTaskProvider and
the ProfileManager/g_browser_process instance is not guaranteed.
This means that it's necessary to check if the ProfileManager still
exists before unregistering from it, which preclude us from using
ScopedObserver.

This is a common pattern for other ProfileManager observers
instances.

Bug: 1094235
Change-Id: I35369d8938c95dcc6ef5204ea15b5f4dfa4d000e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2248073
Commit-Queue: Patrick Monette <pmonette@chromium.org>
Reviewed-by: Ahmed Fakhry <afakhry@chromium.org>
Cr-Commit-Position: refs/heads/master@{#779982}

[modify] https://crrev.com/19f51b3583e526ac7d41bcd94d490aa9d3e4334a/chrome/browser/task_manager/providers/worker_task_provider.cc
[modify] https://crrev.com/19f51b3583e526ac7d41bcd94d490aa9d3e4334a/chrome/browser/task_manager/providers/worker_task_provider.h


### pm...@chromium.org (2020-06-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-28)

[Empty comment from Monorail migration]

### na...@google.com (2020-07-13)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-14)

Requesting merge to beta M84 because latest trunk commit (779982) appears to be after beta branch point (768962).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-15)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-07-20)

pmonette@ please could you reply to the previous auto-generated comment, and in general comment on whether there are stability risks by merging this back to the current stable release? It looks like a safe localized object lifetime fix but I'd still like your subjective comment on your confidence in the fix, because when we merge stuff directly to stable it really doesn't get the usual bake time.

Then again this has also been in trunk for ages so I expect we'd have spotted problems by now.

### pm...@chromium.org (2020-07-20)

Sorry for the delay. 

Yeah I have high confidence that this is safe to merge. It's a pretty simple fix and it's been one month in trunk without issues.

Is there any chance you can do the merge? I'm currently on vacation and I don't have access to a computer.

### ad...@google.com (2020-07-23)

Thanks. I'm going to wait till you return before approving merge. It's not so much the merging itself, it's more the expertise and wisdom for how to look for signs of trouble on Canary etc. As a medium severity fix, I'm OK waiting a couple of weeks for the next stable refresh.

### ad...@google.com (2020-07-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-07-23)

Congratulations, the VRP panel has awarded $5000 for this bug.

### ad...@google.com (2020-07-23)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-03)

Approving merge to M84, branch 4147, assuming there are no problems found so far (per https://crbug.com/chromium/1094235#c18). 

### pm...@chromium.org (2020-08-03)

I'm back from vacation so I can handle the merge


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/afb24bd9cbce33314b522e6495bd7020763b8eb7

commit afb24bd9cbce33314b522e6495bd7020763b8eb7
Author: Patrick Monette <pmonette@chromium.org>
Date: Tue Aug 04 15:55:00 2020

WorkerTaskProvider: Don't unregister from ProfileManager if null

The ordering between the destruction of each WorkerTaskProvider and
the ProfileManager/g_browser_process instance is not guaranteed.
This means that it's necessary to check if the ProfileManager still
exists before unregistering from it, which preclude us from using
ScopedObserver.

This is a common pattern for other ProfileManager observers
instances.

(cherry picked from commit 19f51b3583e526ac7d41bcd94d490aa9d3e4334a)

Bug: 1094235
Change-Id: I35369d8938c95dcc6ef5204ea15b5f4dfa4d000e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2248073
Commit-Queue: Patrick Monette <pmonette@chromium.org>
Reviewed-by: Ahmed Fakhry <afakhry@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#779982}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2335897
Reviewed-by: Patrick Monette <pmonette@chromium.org>
Cr-Commit-Position: refs/branch-heads/4147@{#1018}
Cr-Branched-From: 16307825352720ae04d898f37efa5449ad68b606-refs/heads/master@{#768962}

[modify] https://crrev.com/afb24bd9cbce33314b522e6495bd7020763b8eb7/chrome/browser/task_manager/providers/worker_task_provider.cc
[modify] https://crrev.com/afb24bd9cbce33314b522e6495bd7020763b8eb7/chrome/browser/task_manager/providers/worker_task_provider.h


### ad...@google.com (2020-08-07)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-07)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1094235?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052566)*
