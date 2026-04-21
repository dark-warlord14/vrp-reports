# Security: UAF in base::ObserverList<ash::ArcWindowWatcher::ArcWindowDisplayObserver

| Field | Value |
|-------|-------|
| **Issue ID** | [40064140](https://issues.chromium.org/issues/40064140) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Shell |
| **Platforms** | ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-04-20 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

UAF in base::ObserverList<ash::ArcWindowWatcher::ArcWindowDisplayObserver

**VERSION**  

Chromium 114.0.5725.0 (Developer Build) (64-bit)  

Revision e12348691b010c4136bee94dc95fbd10c8b6d91b-refs/heads/main@{#1133420}  

ChromiumOS in Linux

**REPRODUCTION CASE**  

Run the command in ChromiumOS in Linux and close the chromiumOS:  

./chrome --user-data-dir=/tmp/any --enable-features=ArcIdleManager --enable-arc

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** **Type of crash: [tab, browser, etc.]**

==4798==ERROR: AddressSanitizer: heap-use-after-free on address 0x60e000057ce0 at pc 0x5609f039022d bp 0x7ffea1452af0 sp 0x7ffea1452ae8  

READ of size 8 at 0x60e000057ce0 thread T0 (chrome)  

==4798==WARNING: invalid path to external symbolizer!  

==4798==WARNING: Failed to use and restart external symbolizer!  

#0 0x5609f039022c in begin ./../../buildtools/third\_party/libc++/trunk/include/vector:1425:30  

#1 0x5609f039022c in begin<std::Cr::vector<base::internal::CheckedObserverAdapter, std::Cr::allocator[base::internal::CheckedObserverAdapter](javascript:void(0);) > &> ./../../base/ranges/ranges.h:44:37  

#2 0x5609f039022c in begin<std::Cr::vector<base::internal::CheckedObserverAdapter, std::Cr::allocator[base::internal::CheckedObserverAdapter](javascript:void(0);) > &> ./../../base/ranges/ranges.h:105:10  

#3 0x5609f039022c in find\_if<std::Cr::vector<base::internal::CheckedObserverAdapter, std::Cr::allocator[base::internal::CheckedObserverAdapter](javascript:void(0);) > &, (lambda at ../../base/observer\_list.h:304:21), base::identity, std::Cr::random\_access\_iterator\_tag> ./../../base/ranges/algorithm.h:483:26  

#4 0x5609f039022c in base::ObserverList<ash::ArcWindowWatcher::ArcWindowDisplayObserver, false, true, base::internal::CheckedObserverAdapter>::RemoveObserver(ash::ArcWindowWatcher::ArcWindowDisplayObserver const\*) ./../../base/observer\_list.h:303:21  

#5 0x5609f023c1c8 in RemoveObserver ./../../base/scoped\_observation\_traits.h:72:13  

#6 0x5609f023c1c8 in Reset ./../../base/scoped\_observation.h:115:7  

#7 0x5609f023c1c8 in arc::ArcAppLaunchThrottleObserver::StopObserving() ./../../chrome/browser/ash/arc/instance\_throttle/arc\_app\_launch\_throttle\_observer.cc:45:31  

#8 0x5609f14f4546 in ash::ThrottleService::StopObservers() ./../../chrome/browser/ash/throttle\_service.cc:63:15  

#9 0x5609f781aad0 in ShutdownFactoriesInOrder ./../../components/keyed\_service/core/dependency\_manager.cc:175:14  

#10 0x5609f781aad0 in DependencyManager::PerformInterlockedTwoPhaseShutdown(DependencyManager\*, void\*, DependencyManager\*, void\*) ./../../components/keyed\_service/core/dependency\_manager.cc:152:3  

#11 0x5609fbf9dbbb in ProfileImpl::~ProfileImpl() ./../../chrome/browser/profiles/profile\_impl.cc:950:3  

#12 0x5609fbf9e2d9 in ProfileImpl::~ProfileImpl() ./../../chrome/browser/profiles/profile\_impl.cc:896:29  

#13 0x5609fbfacca3 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#14 0x5609fbfacca3 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#15 0x5609fbfacca3 in ProfileDestroyer::DestroyOriginalProfileNow(std::Cr::unique\_ptr<Profile, std::Cr::default\_delete<Profile>>) ./../../chrome/browser/profiles/profile\_destroyer.cc:273:11  

#16 0x5609fbfa9c80 in Timeout ./../../chrome/browser/profiles/profile\_destroyer.cc:435:3  

#17 0x5609fbfa9c80 in ProfileDestroyer::Start(std::Cr::set<content::RenderProcessHost\*, std::Cr::less[content::RenderProcessHost\\*](javascript:void(0);), std::Cr::allocator[content::RenderProcessHost\\*](javascript:void(0);)> const&) ./../../chrome/browser/profiles/profile\_destroyer.cc:326:5  

#18 0x5609fbfa886c in ProfileDestroyer::DestroyOriginalProfileWhenAppropriateWithTimeout(std::Cr::unique\_ptr<Profile, std::Cr::default\_delete<Profile>>, base::TimeDelta) ./../../chrome/browser/profiles/profile\_destroyer.cc:152:22  

#19 0x5609fbfc15a4 in ProfileManager::ProfileInfo::~ProfileInfo() ./../../chrome/browser/profiles/profile\_manager.cc:1571:3  

#20 0x5609fbfc865c in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#21 0x5609fbfc865c in std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>::reset(ProfileManager::ProfileInfo\*) ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#22 0x5609fbfc5e0f in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:263:75  

#23 0x5609fbfc5e0f in ~pair ./../../buildtools/third\_party/libc++/trunk/include/\_\_utility/pair.h:62:29  

#24 0x5609fbfc5e0f in void std::Cr::\_\_destroy\_at<std::Cr::pair<base::FilePath const, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>, 0>(std::Cr::pair<base::FilePath const, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>\*) ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/construct\_at.h:66:13  

#25 0x5609fbfc5dd8 in destroy\_at<std::Cr::pair<const base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >, 0> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/construct\_at.h:101:5  

#26 0x5609fbfc5dd8 in destroy<std::Cr::pair<const base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >, void, void> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator\_traits.h:323:9  

#27 0x5609fbfc5dd8 in std::Cr::\_\_tree<std::Cr::\_\_value\_type<base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>, std::Cr::\_\_map\_value\_compare<base::FilePath, std::Cr::\_\_value\_type<base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>, std::Cr::less[base::FilePath](javascript:void(0);), true>, std::Cr::allocator<std::Cr::\_\_value\_type<base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>>>::destroy(std::Cr::\_\_tree\_node<std::Cr::\_\_value\_type<base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>, void\*>\*) ./../../buildtools/third\_party/libc++/trunk/include/\_\_tree:1811:9  

#28 0x5609fbfc4b08 in clear ./../../buildtools/third\_party/libc++/trunk/include/\_\_tree:1848:5  

#29 0x5609fbfc4b08 in clear ./../../buildtools/third\_party/libc++/trunk/include/map:1394:37  

#30 0x5609fbfc4b08 in ProfileManager::~ProfileManager() ./../../chrome/browser/profiles/profile\_manager.cc:433:18  

#31 0x5609fbfb4681 in ProfileManager::~ProfileManager() ./../../chrome/browser/profiles/profile\_manager.cc:405:35  

#32 0x5609fb88eb16 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#33 0x5609fb88eb16 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#34 0x5609fb88eb16 in BrowserProcessImpl::StartTearDown() ./../../chrome/browser/browser\_process\_impl.cc:478:22  

#35 0x5609fb88aecc in ChromeBrowserMainParts::PostMainMessageLoopRun() ./../../chrome/browser/chrome\_browser\_main.cc:1918:21  

#36 0x5609f054970d in ash::ChromeBrowserMainPartsAsh::PostMainMessageLoopRun() ./../../chrome/browser/ash/chrome\_browser\_main\_parts\_ash.cc:1619:32  

#37 0x5609ead775db in content::BrowserMainLoop::ShutdownThreadsAndCleanUp() ./../../content/browser/browser\_main\_loop.cc:1131:13  

#38 0x5609ead7c621 in content::BrowserMainRunnerImpl::Shutdown() ./../../content/browser/browser\_main\_runner\_impl.cc:176:17  

#39 0x5609ead7074b in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:43:16  

#40 0x5609f1aebd44 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:706:10  

#41 0x5609f1aef25f in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1276:10  

#42 0x5609f1aeec26 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1130:12  

#43 0x5609f1ae9490 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:326:36  

#44 0x5609f1ae99a2 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:343:10  

#45 0x5609e209e2a3 in ChromeMain ./../../chrome/app/chrome\_main.cc:187:12  

#46 0x7f107ad22082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

0x60e000057ce0 is located 64 bytes inside of 152-byte region [0x60e000057ca0,0x60e000057d38)  

freed by thread T0 (chrome) here:  

#0 0x5609e209c18d in operator delete(void\*) *asan\_rtl*:3  

#1 0x5609fb88ae26 in ChromeBrowserMainParts::PostMainMessageLoopRun() ./../../chrome/browser/chrome\_browser\_main.cc:1906:24  

#2 0x5609f054970d in ash::ChromeBrowserMainPartsAsh::PostMainMessageLoopRun() ./../../chrome/browser/ash/chrome\_browser\_main\_parts\_ash.cc:1619:32  

#3 0x5609ead775db in content::BrowserMainLoop::ShutdownThreadsAndCleanUp() ./../../content/browser/browser\_main\_loop.cc:1131:13  

#4 0x5609ead7c621 in content::BrowserMainRunnerImpl::Shutdown() ./../../content/browser/browser\_main\_runner\_impl.cc:176:17  

#5 0x5609ead7074b in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:43:16  

#6 0x5609f1aebd44 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:706:10  

#7 0x5609f1aef25f in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1276:10  

#8 0x5609f1aeec26 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1130:12  

#9 0x5609f1ae9490 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:326:36  

#10 0x5609f1ae99a2 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:343:10  

#11 0x5609e209e2a3 in ChromeMain ./../../chrome/app/chrome\_main.cc:187:12  

#12 0x7f107ad22082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

previously allocated by thread T0 (chrome) here:  

#0 0x5609e209b92d in operator new(unsigned long) *asan\_rtl*:3  

#1 0x560a08fbe310 in make\_unique[ash::ArcWindowWatcher](javascript:void(0);) ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:686:26  

#2 0x560a08fbe310 in ChromeBrowserMainExtraPartsAsh::PreProfileInit() ./../../chrome/browser/ui/ash/chrome\_browser\_main\_extra\_parts\_ash.cc:155:27  

#3 0x5609fb8896bc in ChromeBrowserMainParts::PreProfileInit() ./../../chrome/browser/chrome\_browser\_main.cc:1174:24  

#4 0x5609f0543609 in ash::ChromeBrowserMainPartsAsh::PreProfileInit() ./../../chrome/browser/ash/chrome\_browser\_main\_parts\_ash.cc:992:32  

#5 0x5609fb88849b in ChromeBrowserMainParts::PreMainMessageLoopRunImpl() ./../../chrome/browser/chrome\_browser\_main.cc:1563:3  

#6 0x5609fb887f75 in ChromeBrowserMainParts::PreMainMessageLoopRun() ./../../chrome/browser/chrome\_browser\_main.cc:1148:18  

#7 0x5609f05424da in ash::ChromeBrowserMainPartsAsh::PreMainMessageLoopRun() ./../../chrome/browser/ash/chrome\_browser\_main\_parts\_ash.cc:849:39  

#8 0x5609ead74acc in content::BrowserMainLoop::PreMainMessageLoopRun() ./../../content/browser/browser\_main\_loop.cc:986:28  

#9 0x5609ec0ef1f7 in Run ./../../base/functional/callback.h:152:12  

#10 0x5609ec0ef1f7 in content::StartupTaskRunner::RunAllTasksNow() ./../../content/browser/startup\_task\_runner.cc:44:29  

#11 0x5609ead73fa1 in content::BrowserMainLoop::CreateStartupTasks() ./../../content/browser/browser\_main\_loop.cc:896:25  

#12 0x5609ead7bdb2 in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams) ./../../content/browser/browser\_main\_runner\_impl.cc:139:15  

#13 0x5609ead7066c in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:30:32  

#14 0x5609f1aebd44 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:706:10  

#15 0x5609f1aef25f in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1276:10  

#16 0x5609f1aeec26 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1130:12  

#17 0x5609f1ae9490 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:326:36  

#18 0x5609f1ae99a2 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:343:10  

#19 0x5609e209e2a3 in ChromeMain ./../../chrome/app/chrome\_main.cc:187:12  

#20 0x7f107ad22082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free (/home/zzzz/chromium\_version/latest\_asan/chrome+0x200cc22c) (BuildId: 1b008142bc2b79ec)  

Shadow bytes around the buggy address:  

0x60e000057a00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x60e000057a80: 00 00 00 fa fa fa fa fa fa fa fa fa 00 00 00 00  

0x60e000057b00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 fa  

0x60e000057b80: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x60e000057c00: 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa fa  

=>0x60e000057c80: fa fa fa fa fd fd fd fd fd fd fd fd[fd]fd fd fd  

0x60e000057d00: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa  

0x60e000057d80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x60e000057e00: fd fd fd fa fa fa fa fa fa fa fa fa fd fd fd fd  

0x60e000057e80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x60e000057f00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb

==4798==ADDITIONAL INFO

==4798==Note: Please include this section with the ASan report.  

Task trace:

==4798==END OF ADDITIONAL INFO  

==4798==ABORTING

## Timeline

### [Deleted User] (2023-04-20)

[Empty comment from Monorail migration]

### za...@google.com (2023-04-21)

Hi hidehiko@ can you help investigate this bug or reassign? It's a UAF issue related to ash. Thanks. 

[Monorail components: UI>Shell]

### [Deleted User] (2023-04-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-21)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-21)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-21)

[Empty comment from Monorail migration]

### hi...@chromium.org (2023-04-21)

crrev.com/c/4376007
crrev.com/c/4353433

Look culprit.
Looks like ArcWindowWatcher looks like destroyed too early. I.e., it is destroyed before removed from observation done in ProfileManager's destruction.

To revert, crrev.com/c/4387539 looks also need to be reverted, as this is put on top of them.
Handed over to raging@.

### [Deleted User] (2023-04-22)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-24)

This issue is marked as a release blocker with no OS labels associated. Please add an appropriate OS label.

All release blocking issues should have OS labels associated to it, so that the issue can tracked and promptly verified, once it gets fixed.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-28)

This issue is marked as a release blocker with no OS labels associated. Please add an appropriate OS label.

All release blocking issues should have OS labels associated to it, so that the issue can tracked and promptly verified, once it gets fixed.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-03)

[Empty comment from Monorail migration]

### sr...@google.com (2023-05-18)

please add the impacted OS to this bug so it gets properly reviewed. 

### am...@chromium.org (2023-05-18)

This issue is in Ash, aura shell specific to ChromeOS 

### ch...@google.com (2023-05-22)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/283714969). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting  Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed

[Monorail blocking: b/283714969]

### ra...@google.com (2023-05-22)

Ack !  will work on this as high pri !

### ra...@google.com (2023-05-22)

Please note that ArcWindowWatcher is not used by anything except for experimental code - so this can't affect any users outside of the experiments that use it (which currently means only  http://go/arcvm-doze-mode-enhancements-finchexp  (google-only link) ), currently on canary with http://cl/532035011   )


### ch...@google.com (2023-05-24)

Project: chromium/src
Branch: main

commit adca059330d5490dd116c5ab471175a1d1c64eda
Author: Alex Gimenez <raging@google.com>
Date:   Tue May 23 22:51:46 2023

    Fix security bug when destroying ArcWindowWatcher
   
    ArcWindowWatcher is being destroyed too early. It is destroyed before
    removed from observation done in ProfileManager's destruction.
    This change fixes that bug by advising ArcWindowWatcher's observers
    explicitly, just prior to ArcWindowWatcher's destruction, so
    the observers can unsubscribe.  This allows ArcWindowWatcher to
    be destroyed earlier than its observers.
   
    Bug: b:283714969
   
    TEST: manual chrome instantiation, confirm destruction order, plus:
          out/Debug_chromeos/unit_tests --single-process-tests
          '--gtest_filter=ArcIdleManagerTest.*:
          ArcAppLaunchThrottleObserverTest.*:
          ArcWindowObserverTest.*'
   
    Change-Id: I461a7dfc716bdbd673cec779c035833444ad64be
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4546656
    Reviewed-by: Yuichiro Hanada <yhanada@chromium.org>
    Reviewed-by: Xiyuan Xia <xiyuan@chromium.org>
    Commit-Queue: Alexandre Marciano Gimenez <raging@google.com>
    Reviewed-by: Yury Khmel <khmel@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1148234}

M       chrome/browser/ash/arc/idle_manager/arc_window_observer.cc
M       chrome/browser/ash/arc/idle_manager/arc_window_observer.h
M       chrome/browser/ash/arc/instance_throttle/arc_app_launch_throttle_observer.cc
M       chrome/browser/ash/arc/instance_throttle/arc_app_launch_throttle_observer.h
M       chrome/browser/ash/arc/util/arc_window_watcher.cc
M       chrome/browser/ash/arc/util/arc_window_watcher.h

https://chromium-review.googlesource.com/4546656
00:52
00:52
CLs: Merged:​<none>      crrev/c/4546656
CLs: Pending:​crrev/c/4546656      <none>

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-26)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

 - M114, which branched on 2023-04-25 (Chromium branch: 5735, Chromium branch position: 1135570)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove the Merge-TBD-## label and replace it with a Merge-NA-## label (where ## corresponds to the milestone under evaluation). If a merge is necessary, please add the appropriate Merge-Request-## labels. If you're not sure, reach out to the relevant release manager (can be found at https://chromiumdash.appspot.com/schedule).

To learn more about the merge process, including how to land any required merges, see https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-06-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-09)

Congratulations, asnine! The VRP Panel has decided to award you $1,000 for this report. The reward amount was decided based on how this issue is able to be triggered and that we are certain this would have been discovered well before this feature was enabled and launched. We did want to extend a reward to you as your report allowed us to land a fix earlier and well before launch. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-06-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1435142?no_tracker_redirect=1

[Monorail blocking: b/283714969]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064140)*
