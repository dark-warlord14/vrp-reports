# Heap-use-after-free in extensions::ChromeExtensionsBrowserClient::GetOriginalContext

| Field | Value |
|-------|-------|
| **Issue ID** | [40058314](https://issues.chromium.org/issues/40058314) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions, UI>Browser>Profiles |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | sa...@gmail.com |
| **Assignee** | la...@chromium.org |
| **Created** | 2021-12-21 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36

Steps to reproduce the problem:
1) Go to test.com. and press ctrl+N twice.

2) Click on your profile in the upper right corner and press the manage profiles icon.

3) Press the "Add to Chrome" button in your first tab and after confirming, quickly close all windows except the "Manage profiles" window.

What is the expected behavior?

What went wrong?
=================================================================
==4148==ERROR: AddressSanitizer: heap-use-after-free on address 0x12f847d28e40 at pc 0x7ffb98edf532 bp 0x00dcab1fe730 sp 0x00dcab1fe778
READ of size 8 at 0x12f847d28e40 thread T0
==4148==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ffb98edf531 in extensions::ChromeExtensionsBrowserClient::GetOriginalContext C:\b\s\w\ir\cache\builder\src\chrome\browser\extensions\chrome_extensions_browser_client.cc:162
    #1 0x7ffb90686295 in KeyedServiceFactory::GetServiceForContext C:\b\s\w\ir\cache\builder\src\components\keyed_service\core\keyed_service_factory.cc:56
    #2 0x7ffb99c1eaae in extensions::ExtensionSystemImpl::ExtensionSystemImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\extensions\extension_system_impl.cc:361
    #3 0x7ffb91606c93 in BrowserContextKeyedServiceFactory::BuildServiceInstanceFor C:\b\s\w\ir\cache\builder\src\components\keyed_service\content\browser_context_keyed_service_factory.cc:95
    #4 0x7ffb90686504 in KeyedServiceFactory::GetServiceForContext C:\b\s\w\ir\cache\builder\src\components\keyed_service\core\keyed_service_factory.cc:80
    #5 0x7ffb93cc2068 in extensions::CrxInstaller::GetContentVerifierKeyOnUI C:\b\s\w\ir\cache\builder\src\chrome\browser\extensions\crx_installer.cc:481
    #6 0x7ffb93ccc4f6 in base::internal::Invoker<base::internal::BindState<void (extensions::CrxInstaller::*)(base::OnceCallback<void (base::span<const unsigned char,18446744073709551615>)>),scoped_refptr<extensions::CrxInstaller>,base::OnceCallback<void (base::span<const unsigned char,18446744073709551615>)> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:741
    #7 0x7ffb8f561f14 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135
    #8 0x7ffb92095755 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:356
    #9 0x7ffb92094e28 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:261
    #10 0x7ffb8f6090b6 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:220
    #11 0x7ffb8f607348 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #12 0x7ffb92096e21 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:468
    #13 0x7ffb8f4e0a83 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:140
    #14 0x7ffb88714bc9 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1048
    #15 0x7ffb88719fe9 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:153
    #16 0x7ffb8870e251 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:30
    #17 0x7ffb8b193687 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:646
    #18 0x7ffb8b1966c7 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1160
    #19 0x7ffb8b1957fa in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1026
    #20 0x7ffb8b191ad1 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:398
    #21 0x7ffb8b192b5c in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:426
    #22 0x7ffb84a6148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:177
    #23 0x7ff731735b85 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169
    #24 0x7ff731732b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382
    #25 0x7ff731b3457f in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #26 0x7ffc37b154df in BaseThreadInitThunk+0xf (C:\WINDOWS\System32\KERNEL32.DLL+0x1800154df)
    #27 0x7ffc387a485a in RtlUserThreadStart+0x2a (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18000485a)

0x12f847d28e40 is located 0 bytes inside of 424-byte region [0x12f847d28e40,0x12f847d28fe8)
freed by thread T0 here:
    #0 0x7ff7317e280b in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ffb91fbb709 in ProfileImpl::~ProfileImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_impl.cc:861
    #2 0x7ffb91fcd287 in ProfileDestroyer::DestroyOriginalProfileNow C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_destroyer.cc:133
    #3 0x7ffb91fccabb in ProfileDestroyer::DestroyProfileWhenAppropriate C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_destroyer.cc:61
    #4 0x7ffb8f3761f1 in ProfileManager::ProfileInfo::~ProfileInfo C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:1683
    #5 0x7ffb8f37cb19 in std::__1::unique_ptr<ProfileManager::ProfileInfo,std::__1::default_delete<ProfileManager::ProfileInfo> >::reset C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h:315
    #6 0x7ffb8f37d010 in std::__1::__tree<std::__1::__value_type<base::FilePath,std::__1::unique_ptr<ProfileManager::ProfileInfo,std::__1::default_delete<ProfileManager::ProfileInfo> > >,std::__1::__map_value_compare<base::FilePath,std::__1::__value_type<base::FilePath,std::__1::unique_ptr<ProfileManager::ProfileInfo,std::__1::default_delete<ProfileManager::ProfileInfo> > >,std::__1::less<base::FilePath>,1>,std::__1::allocator<std::__1::__value_type<base::FilePath,std::__1::unique_ptr<ProfileManager::ProfileInfo,std::__1::default_delete<ProfileManager::ProfileInfo> > > > >::erase C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__tree:2422
    #7 0x7ffb8f37cf65 in std::__1::__tree<std::__1::__value_type<base::FilePath,std::__1::unique_ptr<ProfileManager::ProfileInfo,std::__1::default_delete<ProfileManager::ProfileInfo> > >,std::__1::__map_value_compare<base::FilePath,std::__1::__value_type<base::FilePath,std::__1::unique_ptr<ProfileManager::ProfileInfo,std::__1::default_delete<ProfileManager::ProfileInfo> > >,std::__1::less<base::FilePath>,1>,std::__1::allocator<std::__1::__value_type<base::FilePath,std::__1::unique_ptr<ProfileManager::ProfileInfo,std::__1::default_delete<ProfileManager::ProfileInfo> > > > >::__erase_unique<base::FilePath> C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__tree:2445
    #8 0x7ffb8f373922 in ProfileManager::RemoveProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:1788
    #9 0x7ffb8f373698 in ProfileManager::DeleteProfileIfNoKeepAlive C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:1518
    #10 0x7ffb8f373165 in ProfileManager::RemoveKeepAlive C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:1475
    #11 0x7ffb8f561f14 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135
    #12 0x7ffb92095755 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:356
    #13 0x7ffb92094e28 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:261
    #14 0x7ffb8f6090b6 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:220
    #15 0x7ffb8f607348 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #16 0x7ffb92096e21 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:468
    #17 0x7ffb8f4e0a83 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:140
    #18 0x7ffb88714bc9 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1048
    #19 0x7ffb88719fe9 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:153
    #20 0x7ffb8870e251 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:30
    #21 0x7ffb8b193687 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:646
    #22 0x7ffb8b1966c7 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1160
    #23 0x7ffb8b1957fa in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1026
    #24 0x7ffb8b191ad1 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:398
    #25 0x7ffb8b192b5c in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:426
    #26 0x7ffb84a6148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:177
    #27 0x7ff731735b85 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169

previously allocated by thread T0 here:
    #0 0x7ff7317e290b in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffba1d09cfe in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
    #2 0x7ffb91fb0101 in Profile::CreateProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_impl.cc:366
    #3 0x7ffb8f3713b9 in ProfileManager::CreateProfileHelper C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:1379
    #4 0x7ffb8f364c86 in ProfileManager::CreateAndInitializeProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:1826
    #5 0x7ffb8f362836 in ProfileManager::GetProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:744
    #6 0x7ffb94dab434 in GetStartupProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1379
    #7 0x7ffb91dade45 in `anonymous namespace'::CreatePrimaryProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:420
    #8 0x7ffb91daaed2 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1426
    #9 0x7ffb91da9ac4 in ChromeBrowserMainParts::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1081
    #10 0x7ffb887125ea in content::BrowserMainLoop::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:978
    #11 0x7ffb89555b9d in content::StartupTaskRunner::RunAllTasksNow C:\b\s\w\ir\cache\builder\src\content\browser\startup_task_runner.cc:43
    #12 0x7ffb88711a47 in content::BrowserMainLoop::CreateStartupTasks C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:886
    #13 0x7ffb887194d9 in content::BrowserMainRunnerImpl::Initialize C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:132
    #14 0x7ffb8870e1fc in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:26
    #15 0x7ffb8b193687 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:646
    #16 0x7ffb8b1966c7 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1160
    #17 0x7ffb8b1957fa in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1026
    #18 0x7ffb8b191ad1 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:398
    #19 0x7ffb8b192b5c in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:426
    #20 0x7ffb84a6148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:177
    #21 0x7ff731735b85 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169
    #22 0x7ff731732b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382
    #23 0x7ff731b3457f in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #24 0x7ffc37b154df in BaseThreadInitThunk+0xf (C:\WINDOWS\System32\KERNEL32.DLL+0x1800154df)
    #25 0x7ffc387a485a in RtlUserThreadStart+0x2a (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18000485a)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\chrome\browser\extensions\chrome_extensions_browser_client.cc:162 in extensions::ChromeExtensionsBrowserClient::GetOriginalContext
Shadow bytes around the buggy address:
  0x052f50ca5170: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x052f50ca5180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x052f50ca5190: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x052f50ca51a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x052f50ca51b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x052f50ca51c0: fa fa fa fa fa fa fa fa[fd]fd fd fd fd fd fd fd
  0x052f50ca51d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x052f50ca51e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x052f50ca51f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa
  0x052f50ca5200: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x052f50ca5210: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==4148==ABORTING

Did this work before? N/A 

Chrome version: 96.0.4664.110  Channel: stable
OS Version: 10.0

This is similar to report #1281881 but root issue is different.

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 14.4 KB)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 6.0 MB)

## Timeline

### [Deleted User] (2021-12-21)

[Empty comment from Monorail migration]

### sa...@gmail.com (2021-12-21)

Sorry, you need to go to the following link instead of test.com:
https://chrome.google.com/webstore/detail/google-translate/aapbdbdomjkkjkaonfhkkikfgjllcleb?hl=en-US

### wf...@chromium.org (2021-12-21)

Thank you for your report.

[Monorail components: Platform>Extensions UI>Browser>Profiles]

### wf...@chromium.org (2021-12-21)

[Empty comment from Monorail migration]

### wf...@chromium.org (2021-12-21)

https://crbug.com/chromium/827181 seems to be a crash in this area. lazyboy, you might have most memory of this? Can you take a look at this externally reported high severity UAF?

### [Deleted User] (2021-12-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-22)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@chromium.org (2022-01-04)

The way to get UaF(c#1) is quite tricky because of async call timing AFAICT. I weren't able to repro it verbatim.

However, I've changed CrxInstaller::GetContentVerifierKey to use PostDelayedTask instead of PostTask to CrxInstaller::GetContentVerifierKeyOnUI [1] to mimic the failure on asan build and did get asan logs similar to https://crbug.com/chromium/1281941#c1.

[1]
https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/crx_installer.cc;drc=a0c577275320741e104ae963aac4d8d7388da800;l=493

### sa...@gmail.com (2022-01-05)

Hi lazyboy@, I noticed that I missed a detail in the steps. Wait a bit after pressing the "Add the chrome" button. Because other tabs are not closed because a download is in progress. I am sharing video for you. Could you repeat that? 

### gi...@appspot.gserviceaccount.com (2022-01-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5c6992807466506b4d4215465b07077984a4165e

commit 5c6992807466506b4d4215465b07077984a4165e
Author: Istiaque Ahmed <lazyboy@chromium.org>
Date: Fri Jan 07 22:05:01 2022

Fix a UaF originating from CrxInstaller::GetContentVerifierKeyOnUI

This change adds ref-count to CrxInstaller's Profile (via
ScopedProfileKeepAlive) while an installation is in progress.

Bug: 1281941
Change-Id: I22a6e4eda275f705749bf842af27d9d2df41eaeb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3367235
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
Reviewed-by: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Commit-Queue: Istiaque Ahmed <lazyboy@chromium.org>
Cr-Commit-Position: refs/heads/main@{#956684}

[modify] https://crrev.com/5c6992807466506b4d4215465b07077984a4165e/chrome/browser/extensions/crx_installer.cc
[modify] https://crrev.com/5c6992807466506b4d4215465b07077984a4165e/tools/metrics/histograms/enums.xml
[modify] https://crrev.com/5c6992807466506b4d4215465b07077984a4165e/chrome/browser/extensions/crx_installer.h
[modify] https://crrev.com/5c6992807466506b4d4215465b07077984a4165e/chrome/browser/profiles/keep_alive/profile_keep_alive_types.cc
[modify] https://crrev.com/5c6992807466506b4d4215465b07077984a4165e/chrome/browser/profiles/keep_alive/profile_keep_alive_types.h


### la...@chromium.org (2022-01-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-19)

Requesting merge to extended stable M96 because latest trunk commit (956684) appears to be after extended stable branch point (929512).

Requesting merge to stable M97 because latest trunk commit (956684) appears to be after stable branch point (938553).

Requesting merge to beta M98 because latest trunk commit (956684) appears to be after beta branch point (950365).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-19)

Merge review required: M98 is already shipping to beta.

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

### [Deleted User] (2022-01-19)

Merge review required: M97 is already shipping to stable.

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
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-19)

Merge review required: M96 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-01-21)

there does not appear to be in stability impact from this fix on canary, approving for merge to M98; please confirm there are no issues and merge to branch 4758 NLT 11am PST, Tuesday, 25 January 2021 so this fix can be included in the stable cut for M98 -- thank you 

### [Deleted User] (2022-01-25)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-01-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7150f9edf134a1dea4d6a0e09b9213d7e9550356

commit 7150f9edf134a1dea4d6a0e09b9213d7e9550356
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Tue Jan 25 17:32:09 2022

[M98] Fix a UaF originating from CrxInstaller::GetContentVerifierKeyOnUI

This change adds ref-count to CrxInstaller's Profile (via
ScopedProfileKeepAlive) while an installation is in progress.

Manual Merge Notes:
* There was a conflict because the ProfileKeepAliveOrigin
  kGettingWebAppInfo did not exist in M98, but the kCrxInstaller origin
  this CL introduced comes after that one. This CL now introduces both
  of these origins (though it does not use kGettingWebAppInfo). This
  ensures a constant value is used for the keep alive origin across
  Chrome versions.
* The keep alive files moved in M99 to a subdirectory. This
  CL updates the original patch to point to the old file locations.

(cherry picked from commit 5c6992807466506b4d4215465b07077984a4165e)

Bug: 1281941
Change-Id: I22a6e4eda275f705749bf842af27d9d2df41eaeb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3367235
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
Reviewed-by: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Commit-Queue: Istiaque Ahmed <lazyboy@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#956684}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3413746
Auto-Submit: Devlin Cronin <rdevlin.cronin@chromium.org>
Commit-Queue: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Cr-Commit-Position: refs/branch-heads/4758@{#903}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/7150f9edf134a1dea4d6a0e09b9213d7e9550356/chrome/browser/profiles/profile_keep_alive_types.cc
[modify] https://crrev.com/7150f9edf134a1dea4d6a0e09b9213d7e9550356/chrome/browser/extensions/crx_installer.cc
[modify] https://crrev.com/7150f9edf134a1dea4d6a0e09b9213d7e9550356/chrome/browser/profiles/profile_keep_alive_types.h
[modify] https://crrev.com/7150f9edf134a1dea4d6a0e09b9213d7e9550356/tools/metrics/histograms/enums.xml
[modify] https://crrev.com/7150f9edf134a1dea4d6a0e09b9213d7e9550356/chrome/browser/extensions/crx_installer.h


### [Deleted User] (2022-01-25)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-01-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-28)

Hello, we appreciate your efforts that allowed us to fix a UAF, but as this bug is solely reliant on user interaction, requires accessing the webstore, and requires an unusual amount of steps to trigger, the VRP Panel has decided to award you $1,000 for this report. There is a very steep curve for an attacker to be able to reasonably convince a user to perform this level of user interaction, but because it is not out of the realm of possibility and allowed us to fix a potential issue, we did want to offer you a reward. 
Thank you again for your efforts. 

### am...@google.com (2022-01-29)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-31)

adjusting security severity to reflect mitigations and unusual amount of user interaction 

### am...@chromium.org (2022-01-31)

[Empty comment from Monorail migration]

### rz...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### rz...@google.com (2022-02-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-04)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-02-04)

1. Number of CLs needed for this fix and links to them.
1, https://crrev.com/c/3427546

2. Level of complexity (High, Medium, Low - Explain)
Low, minor conflict with ProfileKeepAliveOrigin elements

3. Has this been merged to a stable release? beta release?
98

4. Overall Recommendation (Yes, No)
Yes

### gm...@google.com (2022-02-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-02-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/50859367448970d8c75685d2f5a333b6878de00d

commit 50859367448970d8c75685d2f5a333b6878de00d
Author: Istiaque Ahmed <lazyboy@chromium.org>
Date: Mon Feb 07 15:51:31 2022

[M96-LTS] Fix a UaF originating from CrxInstaller::GetContentVerifierKeyOnUI

M96 merge issues:
  profile_keep_alive_types.h/cpp, tools/metrics/histograms/enums.xml:
    Minor conflicts because ProfileKeepAliveOrigin enum has more items on main

This change adds ref-count to CrxInstaller's Profile (via
ScopedProfileKeepAlive) while an installation is in progress.

(cherry picked from commit 5c6992807466506b4d4215465b07077984a4165e)

Bug: 1281941
Change-Id: I22a6e4eda275f705749bf842af27d9d2df41eaeb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3367235
Commit-Queue: Istiaque Ahmed <lazyboy@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#956684}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3427546
Reviewed-by: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1458}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/50859367448970d8c75685d2f5a333b6878de00d/chrome/browser/profiles/profile_keep_alive_types.cc
[modify] https://crrev.com/50859367448970d8c75685d2f5a333b6878de00d/chrome/browser/extensions/crx_installer.cc
[modify] https://crrev.com/50859367448970d8c75685d2f5a333b6878de00d/chrome/browser/profiles/profile_keep_alive_types.h
[modify] https://crrev.com/50859367448970d8c75685d2f5a333b6878de00d/tools/metrics/histograms/enums.xml
[modify] https://crrev.com/50859367448970d8c75685d2f5a333b6878de00d/chrome/browser/extensions/crx_installer.h


### rz...@google.com (2022-02-07)

[Empty comment from Monorail migration]

### ho...@chromium.org (2022-02-07)

I suspect the merge in https://crbug.com/chromium/1281941#c21 may be causing some test failures on a branch builder:
https://bugs.chromium.org/p/chromium/issues/detail?id=1295015

https://ci.chromium.org/p/chromium-m98/builders/ci/linux-chromeos-dbg

### am...@google.com (2022-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1281941?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Extensions, UI>Browser>Profiles]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058314)*
