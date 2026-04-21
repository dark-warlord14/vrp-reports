# Security: heap-use-after-free in PPAPIDownloadRequest::AllowlistCheckComplete

| Field | Value |
|-------|-------|
| **Issue ID** | [40057113](https://issues.chromium.org/issues/40057113) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | me...@gmail.com |
| **Assignee** | dr...@chromium.org |
| **Created** | 2021-09-01 |
| **Bounty** | $20,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36

Steps to reproduce the problem:
1. download asan-linux-release-917083.zip and unzip chrome
2. copy the mojom.js file: `python copy_mojo_js_bindings.py /path/to/ASAN/gen/` and start a server at floder of poc.html & test.html : `python -m SimpleHTTPServer 8605`
3. ./asan-linux-release-917083/chrome  --enable-blink-features=MojoJS --user-data-dir=/tmp/noexist http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html
4. UAF occurs

What is the expected behavior?

What went wrong?
In function PPAPIDownloadRequest::CheckAllowlistsOnIOThread()[1], UIThreadTaskRunner will post a task which will call AllowlistCheckComplete()[2]. AllowlistCheckComplete will then call function like this: `SendRequest`[2] => `AddReferrerChainToPPAPIClientDownloadRequest` => `GetNavigationObserverManager`[3].And GetNavigationObserverManager will use `web_contents` without check, if we could delete `web_contents` before the posted taks is called, UAF occurs.

[1]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/safe_browsing/download_protection/ppapi_download_request.cc;l=142
[2]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/safe_browsing/download_protection/ppapi_download_request.cc;l=168
[3]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/safe_browsing/download_protection/download_protection_service.cc;l=712

=================================================================
==137709==ERROR: AddressSanitizer: heap-use-after-free on address 0x61e000082880 at pc 0x5615ba00620c bp 0x7ffe74afa190 sp 0x7ffe74afa188
READ of size 8 at 0x61e000082880 thread T0 (chrome)
    #0 0x5615ba00620b in GetNavigationObserverManager chrome/browser/safe_browsing/download_protection/download_protection_service.cc:712:21
    #1 0x5615ba00620b in safe_browsing::DownloadProtectionService::AddReferrerChainToPPAPIClientDownloadRequest(content::WebContents*, GURL const&, GURL const&, SessionID, bool, safe_browsing::ClientDownloadRequest*) chrome/browser/safe_browsing/download_protection/download_protection_service.cc:586:7
    #2 0x5615ba045c21 in safe_browsing::PPAPIDownloadRequest::SendRequest() chrome/browser/safe_browsing/download_protection/ppapi_download_request.cc:205:13
    #3 0x5615ba0444f0 in safe_browsing::PPAPIDownloadRequest::AllowlistCheckComplete(bool) chrome/browser/safe_browsing/download_protection/ppapi_download_request.cc:168:3
    #4 0x5615ba048978 in Invoke<void (safe_browsing::PPAPIDownloadRequest::*)(bool), base::WeakPtr<safe_browsing::PPAPIDownloadRequest>, bool> base/bind_internal.h:509:12
    #5 0x5615ba048978 in MakeItSo<void (safe_browsing::PPAPIDownloadRequest::*)(bool), base::WeakPtr<safe_browsing::PPAPIDownloadRequest>, bool> base/bind_internal.h:668:5
    #6 0x5615ba048978 in RunImpl<void (safe_browsing::PPAPIDownloadRequest::*)(bool), std::__1::tuple<base::WeakPtr<safe_browsing::PPAPIDownloadRequest>, bool>, 0UL, 1UL> base/bind_internal.h:721:12
    #7 0x5615ba048978 in base::internal::Invoker<base::internal::BindState<void (safe_browsing::PPAPIDownloadRequest::*)(bool), base::WeakPtr<safe_browsing::PPAPIDownloadRequest>, bool>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #8 0x5615b06a0700 in Run base/callback.h:99:12
    #9 0x5615b06a0700 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:178:33
    #10 0x5615b06d8d29 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:360:23
    #11 0x5615b06d84b8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260:36
    #12 0x5615b06d96d1 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #13 0x5615b059a97a in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:405:48
    #14 0x5615b06d9d9b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:467:12
    #15 0x5615b061c411 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #16 0x5615a7627025 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:988:18
    #17 0x5615a762bb65 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:152:15
    #18 0x5615a7620eff in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser_main.cc:49:28
    #19 0x5615af49a2cd in RunBrowserProcessMain content/app/content_main_runner_impl.cc:608:10
    #20 0x5615af49a2cd in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content/app/content_main_runner_impl.cc:1104:10
    #21 0x5615af4993d5 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:971:12
    #22 0x5615af492987 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content/app/content_main.cc:390:36
    #23 0x5615af4945a2 in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:418:10
    #24 0x5615a28c5735 in ChromeMain chrome/app/chrome_main.cc:172:12
    #25 0x7f80d57c30b2 in __libc_start_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

0x61e000082880 is located 0 bytes inside of 2792-byte region [0x61e000082880,0x61e000083368)
freed by thread T0 (chrome) here:
    #0 0x5615a28c372d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x5615ba759bb8 in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #2 0x5615ba759bb8 in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #3 0x5615ba759bb8 in TabStripModel::SendDetachWebContentsNotifications(TabStripModel::DetachNotifications*) chrome/browser/ui/tabs/tab_strip_model.cc:556:27
    #4 0x5615ba76273b in TabStripModel::CloseTabs(base::span<content::WebContents* const, 18446744073709551615ul>, unsigned int) chrome/browser/ui/tabs/tab_strip_model.cc:1798:5
    #5 0x5615ba761b41 in TabStripModel::CloseAllTabs() chrome/browser/ui/tabs/tab_strip_model.cc:745:3
    #6 0x5615bad9bb85 in OnWindowCloseRequested chrome/browser/ui/views/frame/browser_view.cc:2937:13
    #7 0x5615bad9bb85 in non-virtual thunk to BrowserView::OnWindowCloseRequested() chrome/browser/ui/views/frame/browser_view.cc
    #8 0x5615b9bc3cd4 in views::Widget::CloseWithReason(views::Widget::ClosedReason) ui/views/widget/widget.cc:671:45
    #9 0x5615aff1828a in BrowserCloseManager::CloseBrowsers() chrome/browser/lifetime/browser_close_manager.cc:171:24
    #10 0x5615aff18c1c in BrowserCloseManager::CheckForDownloadsInProgress() chrome/browser/lifetime/browser_close_manager.cc:109:5
    #11 0x5615aff188ab in BrowserCloseManager::TryToCloseBrowsers() chrome/browser/lifetime/browser_close_manager.cc:86:3
    #12 0x5615af799e39 in chrome::CloseAllBrowsers() chrome/browser/lifetime/application_lifetime.cc:267:26
    #13 0x5615af799b06 in chrome::AttemptExitInternal(bool) chrome/browser/lifetime/application_lifetime.cc:223:39
    #14 0x5615b01b868e in Exit chrome/browser/chrome_browser_main_posix.cc:130:3
    #15 0x5615b01b868e in (anonymous namespace)::ExitHandler::ExitWhenPossibleOnUIThread(int) chrome/browser/chrome_browser_main_posix.cc:83:9
    #16 0x5615a6877741 in Run base/callback.h:99:12
    #17 0x5615a6877741 in Invoke<base::OnceCallback<void (int)>, int> base/bind_internal.h:608:49
    #18 0x5615a6877741 in MakeItSo<base::OnceCallback<void (int)>, int> base/bind_internal.h:648:12
    #19 0x5615a6877741 in RunImpl<base::OnceCallback<void (int)>, std::__1::tuple<int>, 0UL> base/bind_internal.h:721:12
    #20 0x5615a6877741 in base::internal::Invoker<base::internal::BindState<base::OnceCallback<void (int)>, int>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #21 0x5615b06a0700 in Run base/callback.h:99:12
    #22 0x5615b06a0700 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:178:33
    #23 0x5615b06d8d29 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:360:23
    #24 0x5615b06d84b8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260:36
    #25 0x5615b06d96d1 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #26 0x5615b059b779 in HandleDispatch base/message_loop/message_pump_glib.cc:375:46
    #27 0x5615b059b779 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:125:43
    #28 0x7f80d75dffbc in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x51fbc)

previously allocated by thread T0 (chrome) here:
    #0 0x5615a28c2ecd in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x5615a87c3e98 in content::WebContentsImpl::CreateWithOpener(content::WebContents::CreateParams const&, content::RenderFrameHostImpl*) content/browser/web_contents/web_contents_impl.cc:1023:7
    #2 0x5615ba638b9b in CreateTargetContents chrome/browser/ui/browser_navigator.cc:457:7
    #3 0x5615ba638b9b in Navigate(NavigateParams*) chrome/browser/ui/browser_navigator.cc:644:28
    #4 0x5615ba73680c in StartupBrowserCreatorImpl::OpenTabsInBrowser(Browser*, bool, std::__1::vector<StartupTab, std::__1::allocator<StartupTab> > const&) chrome/browser/ui/startup/startup_browser_creator_impl.cc:319:5
    #5 0x5615ba7393a5 in StartupBrowserCreatorImpl::RestoreOrCreateBrowser(std::__1::vector<StartupTab, std::__1::allocator<StartupTab> > const&, StartupBrowserCreatorImpl::BrowserOpenBehavior, unsigned int, bool, bool) chrome/browser/ui/startup/startup_browser_creator_impl.cc:621:13
    #6 0x5615ba7359fc in StartupBrowserCreatorImpl::DetermineURLsAndLaunch(bool) chrome/browser/ui/startup/startup_browser_creator_impl.cc:429:22
    #7 0x5615ba734eef in StartupBrowserCreatorImpl::Launch(Profile*, bool, std::__1::unique_ptr<LaunchModeRecorder, std::__1::default_delete<LaunchModeRecorder> >) chrome/browser/ui/startup/startup_browser_creator_impl.cc:209:32
    #8 0x5615ba72badb in StartupBrowserCreator::LaunchBrowser(base::CommandLine const&, Profile*, base::FilePath const&, chrome::startup::IsProcessStartup, chrome::startup::IsFirstRun, std::__1::unique_ptr<LaunchModeRecorder, std::__1::default_delete<LaunchModeRecorder> >) chrome/browser/ui/startup/startup_browser_creator.cc:617:31
    #9 0x5615ba72d060 in StartupBrowserCreator::ProcessLastOpenedProfiles(base::CommandLine const&, base::FilePath const&, chrome::startup::IsProcessStartup, chrome::startup::IsFirstRun, Profile*, std::__1::vector<Profile*, std::__1::allocator<Profile*> > const&) chrome/browser/ui/startup/startup_browser_creator.cc:1233:10
    #10 0x5615ba72c6c3 in StartupBrowserCreator::LaunchBrowserForLastProfiles(base::CommandLine const&, base::FilePath const&, bool, Profile*, std::__1::vector<Profile*, std::__1::allocator<Profile*> > const&) chrome/browser/ui/startup/startup_browser_creator.cc:708:10
    #11 0x5615ba7305f9 in StartupBrowserCreator::StartupLaunchAfterProtocolHandler(base::CommandLine const&, base::FilePath const&, Profile*, bool, Profile*, std::__1::vector<Profile*, std::__1::allocator<Profile*> > const&) chrome/browser/ui/startup/startup_browser_creator.cc:1186:10
    #12 0x5615ba72b231 in StartupBrowserCreator::ProcessCmdLineImpl(base::CommandLine const&, base::FilePath const&, bool, Profile*, std::__1::vector<Profile*, std::__1::allocator<Profile*> > const&) chrome/browser/ui/startup/startup_browser_creator.cc:1146:10
    #13 0x5615ba729fd2 in StartupBrowserCreator::Start(base::CommandLine const&, base::FilePath const&, Profile*, std::__1::vector<Profile*, std::__1::allocator<Profile*> > const&) chrome/browser/ui/startup/startup_browser_creator.cc:556:10
    #14 0x5615af697745 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl() chrome/browser/chrome_browser_main.cc:1668:25
    #15 0x5615af6958f4 in ChromeBrowserMainParts::PreMainMessageLoopRun() chrome/browser/chrome_browser_main.cc:1052:18
    #16 0x5615a7624fac in content::BrowserMainLoop::PreMainMessageLoopRun() content/browser/browser_main_loop.cc:938:28
    #17 0x5615a8723a08 in Run base/callback.h:99:12
    #18 0x5615a8723a08 in content::StartupTaskRunner::RunAllTasksNow() content/browser/startup_task_runner.cc:41:29
    #19 0x5615a76245eb in content::BrowserMainLoop::CreateStartupTasks() content/browser/browser_main_loop.cc:846:25
    #20 0x5615a762b31a in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams const&) content/browser/browser_main_runner_impl.cc:131:15
    #21 0x5615a7620ebf in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser_main.cc:45:32
    #22 0x5615af49a2cd in RunBrowserProcessMain content/app/content_main_runner_impl.cc:608:10
    #23 0x5615af49a2cd in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content/app/content_main_runner_impl.cc:1104:10
    #24 0x5615af4993d5 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:971:12
    #25 0x5615af492987 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content/app/content_main.cc:390:36
    #26 0x5615af4945a2 in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:418:10
    #27 0x5615a28c5735 in ChromeMain chrome/app/chrome_main.cc:172:12
    #28 0x7f80d57c30b2 in __libc_start_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free chrome/browser/safe_browsing/download_protection/download_protection_service.cc:712:21 in GetNavigationObserverManager
Shadow bytes around the buggy address:
  0x0c3c800084c0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3c800084d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c3c800084e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c3c800084f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c3c80008500: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x0c3c80008510:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3c80008520: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3c80008530: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3c80008540: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3c80008550: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3c80008560: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==137709==ABORTING

Did this work before? N/A 

Chrome version: 92.0.4515.107  Channel: n/a
OS Version:

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.2 KB)
- [video.webm](attachments/video.webm) (video/webm, 3.6 MB)

## Timeline

### [Deleted User] (2021-09-01)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-09-02)

+download_protection owners, can you take a look please? Browser process UaF accessible from a compromised renderer is High severity, but I'm not sure which release this affects.

[Monorail components: Services>Safebrowsing]

### do...@chromium.org (2021-09-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-02)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@google.com (2021-09-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-09-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5692138292314112.

### ad...@google.com (2021-09-07)

Feeding this to ClusterFuzz to try to figure out the first impacted version and set FoundIn. Pretty sure CF won't figure it out, due to the fact the POC refers to a hard-coded port 8605, so if not, I'll test on different versions in due course.

### ad...@google.com (2021-09-07)

OK, I managed to reproduce this manually using asan-linux-release-917083 on redshell. I'm now going to try the same with stable asan.

### ad...@google.com (2021-09-07)

Reproduced a UaF with asan-linux-release-902206, so confidently setting FoundIn-93, the current stable release.

### [Deleted User] (2021-09-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-08)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dr...@chromium.org (2021-09-08)

I'm struggling to reproduce this, but the fix looks pretty straightforward. I've uploaded https://chromium-review.googlesource.com/c/chromium/src/+/3150060 to fix it.

### gi...@appspot.gserviceaccount.com (2021-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e7d560979f89705ea2844f9f64b5c7a598a03f2b

commit e7d560979f89705ea2844f9f64b5c7a598a03f2b
Author: Daniel Rubery <drubery@chromium.org>
Date: Wed Sep 08 22:25:30 2021

Observe WebContents in PPAPIDownloadRequest

If the WebContents is destroyed while the PPAPIDownloadRequest is
checking the allowlist, we end up with a UaF. The fix for this is to
observe the WebContents and cancel the request.

Bug: 1245578
Change-Id: Idbe5c1cb966fe21ab1a49a7345a5b197afa0b807
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3150060
Reviewed-by: Bettina Dea <bdea@chromium.org>
Commit-Queue: Daniel Rubery <drubery@chromium.org>
Cr-Commit-Position: refs/heads/main@{#919488}

[modify] https://crrev.com/e7d560979f89705ea2844f9f64b5c7a598a03f2b/chrome/browser/safe_browsing/download_protection/ppapi_download_request.cc
[modify] https://crrev.com/e7d560979f89705ea2844f9f64b5c7a598a03f2b/chrome/browser/safe_browsing/download_protection/ppapi_download_request.h


### [Deleted User] (2021-09-10)

[Empty comment from Monorail migration]

### dr...@chromium.org (2021-09-13)

I expect the fix from #13 to fix it, but was unable to reproduce the bug with or without the patch.

merc.ouc@ - can you confirm that you cannot reproduce it either on 95.0.4638.0 or above (Chrome Canary should work)

### me...@gmail.com (2021-09-14)

Hi drubery@
I just confirm that it is not reproducible in this version :
```
Chromium	96.0.4641.0 (Developer Build) (64-bit)
Revision	ea186bcc971760874aef66d2cddaa6bafe80a666-refs/heads/main@{#920622}
OS	Linux
```
But I can reproduce it wiht the old version before patch:
```
Chromium	95.0.4637.0 (Developer Build) (64-bit)
Revision	19ecd18d6def9ed0fe319d9f1e4fce627809b8be-refs/heads/main@{#919472}
OS	Linux
```
So I think this patch fixes this UAF. 

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### me...@gmail.com (2021-09-24)

Hi, can we mark this as fixed?

### dr...@chromium.org (2021-09-24)

Ah yes we can. Thank you for confirming in https://crbug.com/chromium/1245578#c16.

### [Deleted User] (2021-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-26)

Requesting merge to stable M94 because latest trunk commit (919488) appears to be after stable branch point (911515).

Not requesting merge to beta (M95) because latest trunk commit (919488) appears to be prior to beta branch point (920003). If this is incorrect, please replace the Merge-NA-95 label with Merge-Request-95. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-26)

Merge review required: M94 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-09-27)

merge approved for M94, please go ahead and merge to branch 4606 as soon as possible; thank you

### gi...@appspot.gserviceaccount.com (2021-09-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/edbb462a3b0c5f9528cf8d7cb982bb5ddc0b5cc1

commit edbb462a3b0c5f9528cf8d7cb982bb5ddc0b5cc1
Author: Daniel Rubery <drubery@chromium.org>
Date: Tue Sep 28 19:16:15 2021

[Merge M94] Observe WebContents in PPAPIDownloadRequest

If the WebContents is destroyed while the PPAPIDownloadRequest is
checking the allowlist, we end up with a UaF. The fix for this is to
observe the WebContents and cancel the request.

(cherry picked from commit e7d560979f89705ea2844f9f64b5c7a598a03f2b)

Bug: 1245578
Change-Id: Idbe5c1cb966fe21ab1a49a7345a5b197afa0b807
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3150060
Reviewed-by: Bettina Dea <bdea@chromium.org>
Commit-Queue: Daniel Rubery <drubery@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#919488}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3188403
Auto-Submit: Daniel Rubery <drubery@chromium.org>
Commit-Queue: Bettina Dea <bdea@chromium.org>
Cr-Commit-Position: refs/branch-heads/4606@{#1241}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/edbb462a3b0c5f9528cf8d7cb982bb5ddc0b5cc1/chrome/browser/safe_browsing/download_protection/ppapi_download_request.h
[modify] https://crrev.com/edbb462a3b0c5f9528cf8d7cb982bb5ddc0b5cc1/chrome/browser/safe_browsing/download_protection/ppapi_download_request.cc


### am...@google.com (2021-09-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-30)

Congratulations! The VRP Panel has decided to award you $20,000 for this report. Thank you for your report and great finding! 

### am...@chromium.org (2021-09-30)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-30)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-01)

[Empty comment from Monorail migration]

### rz...@google.com (2021-10-04)

[Empty comment from Monorail migration]

### gi...@google.com (2021-10-05)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-10-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/65e7f7c5442eb4860ddd647d98936cacfeec2d1b

commit 65e7f7c5442eb4860ddd647d98936cacfeec2d1b
Author: Daniel Rubery <drubery@chromium.org>
Date: Wed Oct 06 15:25:10 2021

[M90-LTS] Observe WebContents in PPAPIDownloadRequest

If the WebContents is destroyed while the PPAPIDownloadRequest is
checking the allowlist, we end up with a UaF. The fix for this is to
observe the WebContents and cancel the request.

M90 merge notes:
  Conflicting lines for checking HasUserGesture().
  Decided to keep the web_contents nullity check since
  the comments say it can be null in tests.

(cherry picked from commit e7d560979f89705ea2844f9f64b5c7a598a03f2b)

Bug: 1245578
Change-Id: Idbe5c1cb966fe21ab1a49a7345a5b197afa0b807
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3150060
Commit-Queue: Daniel Rubery <drubery@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#919488}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3198083
Reviewed-by: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1638}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/65e7f7c5442eb4860ddd647d98936cacfeec2d1b/chrome/browser/safe_browsing/download_protection/ppapi_download_request.h
[modify] https://crrev.com/65e7f7c5442eb4860ddd647d98936cacfeec2d1b/chrome/browser/safe_browsing/download_protection/ppapi_download_request.cc


### rz...@google.com (2021-10-06)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1245578?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057113)*
