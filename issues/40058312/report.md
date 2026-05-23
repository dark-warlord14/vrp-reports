# Heap-use-after-free in optimization_guide::OptimizationGuideStore::ClearFetchedHintsFromDatabase

| Field | Value |
|-------|-------|
| **Issue ID** | [40058312](https://issues.chromium.org/issues/40058312) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>OptimizationGuide |
| **Platforms** | Windows |
| **Reporter** | sa...@gmail.com |
| **Assignee** | so...@chromium.org |
| **Created** | 2021-12-21 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62

Steps to reproduce the problem:
1)Open two windows in the same profile.
2) Open a guest profile window.
3) Install a plugin in the first window and close all windows after confirming the confirmation bubble.

- You can follow the detailed steps in the video.

What is the expected behavior?

What went wrong?
=================================================================
==5200==ERROR: AddressSanitizer: heap-use-after-free on address 0x120953c6a9e0 at pc 0x7ffba93fb882 bp 0x00261b1fd580 sp 0x00261b1fd5c8
READ of size 4 at 0x120953c6a9e0 thread T0
==5200==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ffba93fb881 in optimization_guide::OptimizationGuideStore::ClearFetchedHintsFromDatabase C:\b\s\w\ir\cache\builder\src\components\optimization_guide\core\optimization_guide_store.cc:620
    #1 0x7ffba6da32c9 in optimization_guide::HintsManager::ClearFetchedHints C:\b\s\w\ir\cache\builder\src\components\optimization_guide\core\hints_manager.cc:1534
    #2 0x7ffba619794b in OptimizationGuideKeyedService::ClearData C:\b\s\w\ir\cache\builder\src\chrome\browser\optimization_guide\optimization_guide_keyed_service.cc:327
    #3 0x7ffba6103ce3 in ChromeBrowsingDataRemoverDelegate::RemoveEmbedderData C:\b\s\w\ir\cache\builder\src\chrome\browser\browsing_data\chrome_browsing_data_remover_delegate.cc:547
    #4 0x7ffb95ad9d1b in content::BrowsingDataRemoverImpl::RemoveImpl C:\b\s\w\ir\cache\builder\src\content\browser\browsing_data\browsing_data_remover_impl.cc:564
    #5 0x7ffb95ad845f in content::BrowsingDataRemoverImpl::RunNextTask C:\b\s\w\ir\cache\builder\src\content\browser\browsing_data\browsing_data_remover_impl.cc:261
    #6 0x7ffb95ad72f9 in content::BrowsingDataRemoverImpl::RemoveInternal C:\b\s\w\ir\cache\builder\src\content\browser\browsing_data\browsing_data_remover_impl.cc:245
    #7 0x7ffb95ad69c3 in content::BrowsingDataRemoverImpl::Remove C:\b\s\w\ir\cache\builder\src\content\browser\browsing_data\browsing_data_remover_impl.cc:179
    #8 0x7ffb97ced9c7 in Profile::Wipe C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile.cc:485
    #9 0x7ffb9c7282d3 in ProfileManager::CleanUpGuestProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:2096
    #10 0x7ffb9c729831 in ProfileManager::OnBrowserClosed C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:2326
    #11 0x7ffb9ec10039 in BrowserList::RemoveBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser_list.cc:113
    #12 0x7ffb9ebfc191 in Browser::~Browser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser.cc:581
    #13 0x7ffb9ec0dc11 in Browser::~Browser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser.cc:562
    #14 0x7ffba24b5a4c in BrowserView::~BrowserView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_view.cc:853
    #15 0x7ffba24ce1af in BrowserView::`vector deleting destructor'+0x19 (D:\files\asan\asan-win32-release_x64-952789\chrome.dll+0x1906be1af)
    #16 0x7ffb9c64618d in views::View::~View C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:253
    #17 0x7ffbaa37835f in GlassBrowserFrameView::~GlassBrowserFrameView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\glass_browser_frame_view.cc:134
    #18 0x7ffb9c68dffd in views::NonClientView::~NonClientView C:\b\s\w\ir\cache\builder\src\ui\views\window\non_client_view.cc:168
    #19 0x7ffb9c68fdb3 in views::NonClientView::~NonClientView C:\b\s\w\ir\cache\builder\src\ui\views\window\non_client_view.cc:164
    #20 0x7ffb9c64824d in views::View::DoRemoveChildView C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:2638
    #21 0x7ffb9c6485d6 in views::View::RemoveAllChildViews C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:328
    #22 0x7ffb9c674895 in views::Widget::DestroyRootView C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1766
    #23 0x7ffb9c674497 in views::Widget::~Widget C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:208
    #24 0x7ffba3f2ee21 in BrowserFrame::~BrowserFrame C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_frame.cc:87
    #25 0x7ffba5ea6b84 in views::DesktopNativeWidgetAura::~DesktopNativeWidgetAura C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_native_widget_aura.cc:304
    #26 0x7ffbab9da00f in DesktopBrowserFrameAura::~DesktopBrowserFrameAura C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\desktop_browser_frame_aura.cc:39
    #27 0x7ffba5e86072 in views::HWNDMessageHandler::OnWndProc C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:1036
    #28 0x7ffb9f7a5106 in gfx::WindowImpl::WndProc C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window_impl.cc:306
    #29 0x7ffb9f7a3a21 in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> C:\b\s\w\ir\cache\builder\src\base\win\wrapped_window_proc.h:74
    #30 0x7ffc36851c4b in CallWindowProcW+0x43b (C:\WINDOWS\System32\user32.dll+0x180011c4b)
    #31 0x7ffc3685179b in EnumChildWindows+0x19b (C:\WINDOWS\System32\user32.dll+0x18001179b)
    #32 0x7ffc368671c1 in RegisterWindowMessageW+0x91 (C:\WINDOWS\System32\user32.dll+0x1800271c1)
    #33 0x7ffc388472b3 in KiUserCallbackDispatcher+0x23 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800a72b3)
    #34 0x7ffc36282633 in NtUserDestroyWindow+0x13 (C:\WINDOWS\System32\win32u.dll+0x180002633)
    #35 0x7ffb9c911f14 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135
    #36 0x7ffb9f445755 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:356
    #37 0x7ffb9f444e28 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:261
    #38 0x7ffb9c9b90b6 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:220
    #39 0x7ffb9c9b7348 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #40 0x7ffb9f446e21 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:468
    #41 0x7ffb9c890a83 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:140
    #42 0x7ffb95ac4bc9 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1048
    #43 0x7ffb95ac9fe9 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:153
    #44 0x7ffb95abe251 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:30
    #45 0x7ffb98543687 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:646
    #46 0x7ffb985466c7 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1160
    #47 0x7ffb985457fa in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1026
    #48 0x7ffb98541ad1 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:398
    #49 0x7ffb98542b5c in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:426
    #50 0x7ffb91e1148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:177
    #51 0x7ff731735b85 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169
    #52 0x7ff731732b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382
    #53 0x7ff731b3457f in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #54 0x7ffc37b154df in BaseThreadInitThunk+0xf (C:\WINDOWS\System32\KERNEL32.DLL+0x1800154df)
    #55 0x7ffc387a485a in RtlUserThreadStart+0x2a (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18000485a)

0x120953c6a9e0 is located 16 bytes inside of 136-byte region [0x120953c6a9d0,0x120953c6aa58)
freed by thread T0 here:
    #0 0x7ff7317e280b in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ffba9401d31 in optimization_guide::OptimizationGuideStore::~OptimizationGuideStore C:\b\s\w\ir\cache\builder\src\components\optimization_guide\core\optimization_guide_store.cc:133
    #2 0x7ffba6196d51 in OptimizationGuideKeyedService::~OptimizationGuideKeyedService C:\b\s\w\ir\cache\builder\src\chrome\browser\optimization_guide\optimization_guide_keyed_service.cc:123
    #3 0x7ffba61979b7 in OptimizationGuideKeyedService::~OptimizationGuideKeyedService C:\b\s\w\ir\cache\builder\src\chrome\browser\optimization_guide\optimization_guide_keyed_service.cc:121
    #4 0x7ffb9504aacc in std::__1::__tree<std::__1::__value_type<unsigned int,std::__1::unique_ptr<gpu::gles2::AbstractTexture,std::__1::default_delete<gpu::gles2::AbstractTexture> > >,std::__1::__map_value_compare<unsigned int,std::__1::__value_type<unsigned int,std::__1::unique_ptr<gpu::gles2::AbstractTexture,std::__1::default_delete<gpu::gles2::AbstractTexture> > >,std::__1::less<unsigned int>,1>,std::__1::allocator<std::__1::__value_type<unsigned int,std::__1::unique_ptr<gpu::gles2::AbstractTexture,std::__1::default_delete<gpu::gles2::AbstractTexture> > > > >::erase C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__tree:2422
    #5 0x7ffb9da36d3c in KeyedServiceFactory::Disassociate C:\b\s\w\ir\cache\builder\src\components\keyed_service\core\keyed_service_factory.cc:97
    #6 0x7ffb9da36fcc in KeyedServiceFactory::ContextDestroyed C:\b\s\w\ir\cache\builder\src\components\keyed_service\core\keyed_service_factory.cc:107
    #7 0x7ffba044b073 in DependencyManager::PerformInterlockedTwoPhaseShutdown C:\b\s\w\ir\cache\builder\src\components\keyed_service\core\dependency_manager.cc:127
    #8 0x7ffb9f367a21 in ProfileImpl::~ProfileImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_impl.cc:914
    #9 0x7ffb9f36b6fd in ProfileImpl::~ProfileImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_impl.cc:861
    #10 0x7ffb9f37d287 in ProfileDestroyer::DestroyOriginalProfileNow C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_destroyer.cc:133
    #11 0x7ffb9f37cabb in ProfileDestroyer::DestroyProfileWhenAppropriate C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_destroyer.cc:61
    #12 0x7ffb9c7261f1 in ProfileManager::ProfileInfo::~ProfileInfo C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:1683
    #13 0x7ffb9c72cb19 in std::__1::unique_ptr<ProfileManager::ProfileInfo,std::__1::default_delete<ProfileManager::ProfileInfo> >::reset C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h:315
    #14 0x7ffb9c72d010 in std::__1::__tree<std::__1::__value_type<base::FilePath,std::__1::unique_ptr<ProfileManager::ProfileInfo,std::__1::default_delete<ProfileManager::ProfileInfo> > >,std::__1::__map_value_compare<base::FilePath,std::__1::__value_type<base::FilePath,std::__1::unique_ptr<ProfileManager::ProfileInfo,std::__1::default_delete<ProfileManager::ProfileInfo> > >,std::__1::less<base::FilePath>,1>,std::__1::allocator<std::__1::__value_type<base::FilePath,std::__1::unique_ptr<ProfileManager::ProfileInfo,std::__1::default_delete<ProfileManager::ProfileInfo> > > > >::erase C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__tree:2422
    #15 0x7ffb9c72cf65 in std::__1::__tree<std::__1::__value_type<base::FilePath,std::__1::unique_ptr<ProfileManager::ProfileInfo,std::__1::default_delete<ProfileManager::ProfileInfo> > >,std::__1::__map_value_compare<base::FilePath,std::__1::__value_type<base::FilePath,std::__1::unique_ptr<ProfileManager::ProfileInfo,std::__1::default_delete<ProfileManager::ProfileInfo> > >,std::__1::less<base::FilePath>,1>,std::__1::allocator<std::__1::__value_type<base::FilePath,std::__1::unique_ptr<ProfileManager::ProfileInfo,std::__1::default_delete<ProfileManager::ProfileInfo> > > > >::__erase_unique<base::FilePath> C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__tree:2445
    #16 0x7ffb9c723922 in ProfileManager::RemoveProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:1788
    #17 0x7ffb9c723698 in ProfileManager::DeleteProfileIfNoKeepAlive C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:1518
    #18 0x7ffb9c723165 in ProfileManager::RemoveKeepAlive C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:1475
    #19 0x7ffb9c911f14 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135
    #20 0x7ffb9f445755 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:356
    #21 0x7ffb9f444e28 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:261
    #22 0x7ffb9c9b90b6 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:220
    #23 0x7ffb9c9b7348 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #24 0x7ffb9f446e21 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:468
    #25 0x7ffb9c890a83 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:140
    #26 0x7ffb95ac4bc9 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1048
    #27 0x7ffb95ac9fe9 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:153

previously allocated by thread T0 here:
    #0 0x7ff7317e290b in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffbaf0b9cfe in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
    #2 0x7ffba6195d3b in OptimizationGuideKeyedService::Initialize C:\b\s\w\ir\cache\builder\src\chrome\browser\optimization_guide\optimization_guide_keyed_service.cc:181
    #3 0x7ffba619554c in OptimizationGuideKeyedService::OptimizationGuideKeyedService C:\b\s\w\ir\cache\builder\src\chrome\browser\optimization_guide\optimization_guide_keyed_service.cc:118
    #4 0x7ffb9e9b6c93 in BrowserContextKeyedServiceFactory::BuildServiceInstanceFor C:\b\s\w\ir\cache\builder\src\components\keyed_service\content\browser_context_keyed_service_factory.cc:95
    #5 0x7ffb9da36504 in KeyedServiceFactory::GetServiceForContext C:\b\s\w\ir\cache\builder\src\components\keyed_service\core\keyed_service_factory.cc:80
    #6 0x7ffba044a635 in DependencyManager::CreateContextServices C:\b\s\w\ir\cache\builder\src\components\keyed_service\core\dependency_manager.cc:87
    #7 0x7ffb9e9b613c in BrowserContextDependencyManager::DoCreateBrowserContextServices C:\b\s\w\ir\cache\builder\src\components\keyed_service\content\browser_context_dependency_manager.cc:46
    #8 0x7ffb9f369ef3 in ProfileImpl::OnLocaleReady C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_impl.cc:1105
    #9 0x7ffb9f363c48 in ProfileImpl::OnPrefsLoaded C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_impl.cc:1146
    #10 0x7ffb9f360fe2 in ProfileImpl::ProfileImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_impl.cc:536
    #11 0x7ffb9f360174 in Profile::CreateProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_impl.cc:366
    #12 0x7ffb9c7213b9 in ProfileManager::CreateProfileHelper C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:1379
    #13 0x7ffb9c714c86 in ProfileManager::CreateAndInitializeProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:1826
    #14 0x7ffb9c712836 in ProfileManager::GetProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:744
    #15 0x7ffba215b434 in GetStartupProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1379
    #16 0x7ffb9f15de45 in `anonymous namespace'::CreatePrimaryProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:420
    #17 0x7ffb9f15aed2 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1426
    #18 0x7ffb9f159ac4 in ChromeBrowserMainParts::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1081
    #19 0x7ffb95ac25ea in content::BrowserMainLoop::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:978
    #20 0x7ffb96905b9d in content::StartupTaskRunner::RunAllTasksNow C:\b\s\w\ir\cache\builder\src\content\browser\startup_task_runner.cc:43
    #21 0x7ffb95ac1a47 in content::BrowserMainLoop::CreateStartupTasks C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:886
    #22 0x7ffb95ac94d9 in content::BrowserMainRunnerImpl::Initialize C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:132
    #23 0x7ffb95abe1fc in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:26
    #24 0x7ffb98543687 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:646
    #25 0x7ffb985466c7 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1160
    #26 0x7ffb985457fa in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1026
    #27 0x7ffb98541ad1 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:398

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\components\optimization_guide\core\optimization_guide_store.cc:620 in optimization_guide::OptimizationGuideStore::ClearFetchedHintsFromDatabase
Shadow bytes around the buggy address:
  0x04307e38d4e0: fd fd fd fa fa fa fa fa fa fa fa fa fd fd fd fd
  0x04307e38d4f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa
  0x04307e38d500: fa fa fa fa fa fa fd fd fd fd fd fd fd fd fd fd
  0x04307e38d510: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x04307e38d520: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x04307e38d530: fd fd fa fa fa fa fa fa fa fa fd fd[fd]fd fd fd
  0x04307e38d540: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x04307e38d550: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x04307e38d560: fd fd fd fd fd fd fa fa fa fa fa fa fa fa fd fd
  0x04307e38d570: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa
  0x04307e38d580: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
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
==5200==ABORTING

Did this work before? N/A 

Chrome version: 96.0.4664.110  Channel: stable
OS Version: 10.0

I will share the detailed analysis very soon and if possible I will try to create a plugin that will trigger this easily. 

Thanks!

- Samet Bekmezci @sametbekmezci

## Attachments

- [poc.mp4](attachments/poc.mp4) (video/mp4, 2.2 MB)
- [asan.log](attachments/asan.log) (text/plain, 19.2 KB)

## Timeline

### [Deleted User] (2021-12-21)

[Empty comment from Monorail migration]

### me...@chromium.org (2021-12-21)

Thanks for the report. This is a UAF in the browser process but requires significant user interaction, so assigning high severity.

sophiechang: Could you PTAL? Thanks.

[Monorail components: Internals>OptimizationGuide]

### [Deleted User] (2021-12-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-21)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### so...@chromium.org (2021-12-21)

CL to fix is out for review - https://chromium-review.googlesource.com/c/chromium/src/+/3352192

### [Deleted User] (2021-12-21)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-12-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5163b969bc7a846044df54311f6b217c3bed3718

commit 5163b969bc7a846044df54311f6b217c3bed3718
Author: Sophie Chang <sophiechang@chromium.org>
Date: Tue Dec 21 19:20:24 2021

Pass weak ptr of store to Opt Guide members

Apparently otr profiles can outlive original profiles so we should guard
against using the store in otr profiles in the code by using weak ptr
instead of raw ptr

Bug: 1281881
Change-Id: I6a1ec451245bbb8af88bd55ab5718d30ed7929da
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3352192
Reviewed-by: Robert Ogden <robertogden@chromium.org>
Commit-Queue: Sophie Chang <sophiechang@chromium.org>
Cr-Commit-Position: refs/heads/main@{#953281}

[modify] https://crrev.com/5163b969bc7a846044df54311f6b217c3bed3718/ios/chrome/browser/optimization_guide/ios_chrome_hints_manager.mm
[modify] https://crrev.com/5163b969bc7a846044df54311f6b217c3bed3718/chrome/browser/optimization_guide/chrome_hints_manager.h
[modify] https://crrev.com/5163b969bc7a846044df54311f6b217c3bed3718/ios/chrome/browser/optimization_guide/optimization_guide_service.mm
[modify] https://crrev.com/5163b969bc7a846044df54311f6b217c3bed3718/chrome/browser/optimization_guide/prediction/prediction_manager.cc
[modify] https://crrev.com/5163b969bc7a846044df54311f6b217c3bed3718/components/optimization_guide/core/hints_manager_unittest.cc
[modify] https://crrev.com/5163b969bc7a846044df54311f6b217c3bed3718/chrome/browser/optimization_guide/optimization_guide_keyed_service.cc
[modify] https://crrev.com/5163b969bc7a846044df54311f6b217c3bed3718/components/optimization_guide/core/hints_manager.h
[modify] https://crrev.com/5163b969bc7a846044df54311f6b217c3bed3718/components/optimization_guide/core/hints_manager.cc
[modify] https://crrev.com/5163b969bc7a846044df54311f6b217c3bed3718/components/optimization_guide/core/hint_cache.cc
[modify] https://crrev.com/5163b969bc7a846044df54311f6b217c3bed3718/components/optimization_guide/core/hint_cache.h
[modify] https://crrev.com/5163b969bc7a846044df54311f6b217c3bed3718/chrome/browser/optimization_guide/chrome_hints_manager_unittest.cc
[modify] https://crrev.com/5163b969bc7a846044df54311f6b217c3bed3718/chrome/browser/optimization_guide/prediction/prediction_manager_unittest.cc
[modify] https://crrev.com/5163b969bc7a846044df54311f6b217c3bed3718/components/optimization_guide/core/optimization_guide_store.h
[modify] https://crrev.com/5163b969bc7a846044df54311f6b217c3bed3718/chrome/browser/optimization_guide/prediction/prediction_manager.h
[modify] https://crrev.com/5163b969bc7a846044df54311f6b217c3bed3718/ios/chrome/browser/optimization_guide/ios_chrome_hints_manager.h
[modify] https://crrev.com/5163b969bc7a846044df54311f6b217c3bed3718/chrome/browser/optimization_guide/chrome_hints_manager.cc
[modify] https://crrev.com/5163b969bc7a846044df54311f6b217c3bed3718/components/optimization_guide/core/hint_cache_unittest.cc


### sa...@gmail.com (2021-12-21)

There is no need for step three in this report, so no need to install plugins. just closing all windows is enough.

### so...@chromium.org (2021-12-21)

Thanks for the helpful video with clear repro steps. Should be fixed on head now - will merge back to M98 

### so...@chromium.org (2021-12-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-12-22)

updating as fixed based on CL and merge request; in the future, please update the issue to Fixed upon fix CL completion and the sheriffbot will take care of the rest in terms of appropriate merge review/request labels, so you do not need to manually request merges and this will end up in our merge review queue. :) 

Since this CL landed < 24 hours ago, going to let this get a bit more bake time on canary before merge approval; please let me know if there are any issues or concerns with this plan. Thanks! 

### [Deleted User] (2021-12-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-22)

Merge approved: your change passed merge requirements and is auto-approved for M98. Please go ahead and merge the CL to branch 4758 (refs/branch-heads/4758) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### so...@chromium.org (2021-12-22)

setting next action for actual merge to some time next week per c#11 

### [Deleted User] (2021-12-27)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-31)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-01-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b7e4b8abcb25502c1a43c4f51ffacb01d3d2dae1

commit b7e4b8abcb25502c1a43c4f51ffacb01d3d2dae1
Author: Sophie Chang <sophiechang@chromium.org>
Date: Tue Jan 04 18:32:04 2022

Pass weak ptr of store to Opt Guide members

Apparently otr profiles can outlive original profiles so we should guard
against using the store in otr profiles in the code by using weak ptr
instead of raw ptr

(cherry picked from commit 5163b969bc7a846044df54311f6b217c3bed3718)

Bug: 1281881
Change-Id: I6a1ec451245bbb8af88bd55ab5718d30ed7929da
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3352192
Reviewed-by: Robert Ogden <robertogden@chromium.org>
Commit-Queue: Sophie Chang <sophiechang@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#953281}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3354068
Auto-Submit: Sophie Chang <sophiechang@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4758@{#307}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/b7e4b8abcb25502c1a43c4f51ffacb01d3d2dae1/ios/chrome/browser/optimization_guide/ios_chrome_hints_manager.mm
[modify] https://crrev.com/b7e4b8abcb25502c1a43c4f51ffacb01d3d2dae1/chrome/browser/optimization_guide/chrome_hints_manager.h
[modify] https://crrev.com/b7e4b8abcb25502c1a43c4f51ffacb01d3d2dae1/ios/chrome/browser/optimization_guide/optimization_guide_service.mm
[modify] https://crrev.com/b7e4b8abcb25502c1a43c4f51ffacb01d3d2dae1/chrome/browser/optimization_guide/prediction/prediction_manager.cc
[modify] https://crrev.com/b7e4b8abcb25502c1a43c4f51ffacb01d3d2dae1/components/optimization_guide/core/hints_manager_unittest.cc
[modify] https://crrev.com/b7e4b8abcb25502c1a43c4f51ffacb01d3d2dae1/chrome/browser/optimization_guide/optimization_guide_keyed_service.cc
[modify] https://crrev.com/b7e4b8abcb25502c1a43c4f51ffacb01d3d2dae1/components/optimization_guide/core/hints_manager.h
[modify] https://crrev.com/b7e4b8abcb25502c1a43c4f51ffacb01d3d2dae1/components/optimization_guide/core/hint_cache.cc
[modify] https://crrev.com/b7e4b8abcb25502c1a43c4f51ffacb01d3d2dae1/components/optimization_guide/core/hints_manager.cc
[modify] https://crrev.com/b7e4b8abcb25502c1a43c4f51ffacb01d3d2dae1/chrome/browser/optimization_guide/chrome_hints_manager_unittest.cc
[modify] https://crrev.com/b7e4b8abcb25502c1a43c4f51ffacb01d3d2dae1/components/optimization_guide/core/hint_cache.h
[modify] https://crrev.com/b7e4b8abcb25502c1a43c4f51ffacb01d3d2dae1/chrome/browser/optimization_guide/prediction/prediction_manager_unittest.cc
[modify] https://crrev.com/b7e4b8abcb25502c1a43c4f51ffacb01d3d2dae1/components/optimization_guide/core/optimization_guide_store.h
[modify] https://crrev.com/b7e4b8abcb25502c1a43c4f51ffacb01d3d2dae1/chrome/browser/optimization_guide/prediction/prediction_manager.h
[modify] https://crrev.com/b7e4b8abcb25502c1a43c4f51ffacb01d3d2dae1/chrome/browser/optimization_guide/chrome_hints_manager.cc
[modify] https://crrev.com/b7e4b8abcb25502c1a43c4f51ffacb01d3d2dae1/ios/chrome/browser/optimization_guide/ios_chrome_hints_manager.h
[modify] https://crrev.com/b7e4b8abcb25502c1a43c4f51ffacb01d3d2dae1/components/optimization_guide/core/hint_cache_unittest.cc


### am...@chromium.org (2022-01-05)

looks like the manual merge request has confused sheriffbot, causing it to not update with the appropriate merge request/review labels for this issue given severity and impact; updating accordingly so this can be in the merge review queue for stable and extended 

### [Deleted User] (2022-01-05)

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

### [Deleted User] (2022-01-05)

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

### am...@chromium.org (2022-01-11)

after some checks merge tentatively approved for M97 and M96; please confirm there are not stability issues or other concerns since this landed on Canary, once confirmed please merge to M97, branch 4692 so this fix can be included in the next Stable security refresh; 
likewise, please merge to M97, branch 4664, so so this fix can be included in the next Extended stable refresh -- thank you

### so...@chromium.org (2022-01-11)

this has been verified on 98 and 99 so ill merge back to 96 and 97 now. 

### am...@chromium.org (2022-01-11)

awesome-- thanks so much, sophiechang@ 

### gi...@appspot.gserviceaccount.com (2022-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fe0d886f433dae78b715ab101e0661938ed2ea69

commit fe0d886f433dae78b715ab101e0661938ed2ea69
Author: Sophie Chang <sophiechang@chromium.org>
Date: Tue Jan 11 05:35:58 2022

Pass weak ptr of store to Opt Guide members

Apparently otr profiles can outlive original profiles so we should guard
against using the store in otr profiles in the code by using weak ptr
instead of raw ptr

(cherry picked from commit 5163b969bc7a846044df54311f6b217c3bed3718)

Bug: 1281881
Change-Id: I6a1ec451245bbb8af88bd55ab5718d30ed7929da
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3352192
Reviewed-by: Robert Ogden <robertogden@chromium.org>
Commit-Queue: Sophie Chang <sophiechang@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#953281}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3379051
Auto-Submit: Sophie Chang <sophiechang@chromium.org>
Commit-Queue: Robert Ogden <robertogden@chromium.org>
Cr-Commit-Position: refs/branch-heads/4692@{#1400}
Cr-Branched-From: 038cd96142d384c0d2238973f1cb277725a62eba-refs/heads/main@{#938553}

[modify] https://crrev.com/fe0d886f433dae78b715ab101e0661938ed2ea69/ios/chrome/browser/optimization_guide/ios_chrome_hints_manager.mm
[modify] https://crrev.com/fe0d886f433dae78b715ab101e0661938ed2ea69/chrome/browser/optimization_guide/chrome_hints_manager.h
[modify] https://crrev.com/fe0d886f433dae78b715ab101e0661938ed2ea69/ios/chrome/browser/optimization_guide/optimization_guide_service.mm
[modify] https://crrev.com/fe0d886f433dae78b715ab101e0661938ed2ea69/chrome/browser/optimization_guide/prediction/prediction_manager.cc
[modify] https://crrev.com/fe0d886f433dae78b715ab101e0661938ed2ea69/components/optimization_guide/core/hints_manager_unittest.cc
[modify] https://crrev.com/fe0d886f433dae78b715ab101e0661938ed2ea69/chrome/browser/optimization_guide/optimization_guide_keyed_service.cc
[modify] https://crrev.com/fe0d886f433dae78b715ab101e0661938ed2ea69/components/optimization_guide/core/hints_manager.h
[modify] https://crrev.com/fe0d886f433dae78b715ab101e0661938ed2ea69/components/optimization_guide/core/hint_cache.cc
[modify] https://crrev.com/fe0d886f433dae78b715ab101e0661938ed2ea69/components/optimization_guide/core/hints_manager.cc
[modify] https://crrev.com/fe0d886f433dae78b715ab101e0661938ed2ea69/chrome/browser/optimization_guide/chrome_hints_manager_unittest.cc
[modify] https://crrev.com/fe0d886f433dae78b715ab101e0661938ed2ea69/components/optimization_guide/core/hint_cache.h
[modify] https://crrev.com/fe0d886f433dae78b715ab101e0661938ed2ea69/chrome/browser/optimization_guide/prediction/prediction_manager_unittest.cc
[modify] https://crrev.com/fe0d886f433dae78b715ab101e0661938ed2ea69/components/optimization_guide/core/optimization_guide_store.h
[modify] https://crrev.com/fe0d886f433dae78b715ab101e0661938ed2ea69/chrome/browser/optimization_guide/prediction/prediction_manager.h
[modify] https://crrev.com/fe0d886f433dae78b715ab101e0661938ed2ea69/chrome/browser/optimization_guide/chrome_hints_manager.cc
[modify] https://crrev.com/fe0d886f433dae78b715ab101e0661938ed2ea69/ios/chrome/browser/optimization_guide/ios_chrome_hints_manager.h
[modify] https://crrev.com/fe0d886f433dae78b715ab101e0661938ed2ea69/components/optimization_guide/core/hint_cache_unittest.cc


### gi...@appspot.gserviceaccount.com (2022-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6f5ef89dc45d9fcd3e1b47292212dc8ca7bd35ae

commit 6f5ef89dc45d9fcd3e1b47292212dc8ca7bd35ae
Author: Sophie Chang <sophiechang@chromium.org>
Date: Tue Jan 11 05:43:17 2022

Pass weak ptr of store to Opt Guide members

Apparently otr profiles can outlive original profiles so we should guard
against using the store in otr profiles in the code by using weak ptr
instead of raw ptr

(cherry picked from commit 5163b969bc7a846044df54311f6b217c3bed3718)

Bug: 1281881
Change-Id: I6a1ec451245bbb8af88bd55ab5718d30ed7929da
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3352192
Reviewed-by: Robert Ogden <robertogden@chromium.org>
Commit-Queue: Sophie Chang <sophiechang@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#953281}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3379053
Auto-Submit: Sophie Chang <sophiechang@chromium.org>
Commit-Queue: Robert Ogden <robertogden@chromium.org>
Cr-Commit-Position: refs/branch-heads/4664@{#1382}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/6f5ef89dc45d9fcd3e1b47292212dc8ca7bd35ae/ios/chrome/browser/optimization_guide/ios_chrome_hints_manager.mm
[modify] https://crrev.com/6f5ef89dc45d9fcd3e1b47292212dc8ca7bd35ae/chrome/browser/optimization_guide/chrome_hints_manager.h
[modify] https://crrev.com/6f5ef89dc45d9fcd3e1b47292212dc8ca7bd35ae/ios/chrome/browser/optimization_guide/optimization_guide_service.mm
[modify] https://crrev.com/6f5ef89dc45d9fcd3e1b47292212dc8ca7bd35ae/chrome/browser/optimization_guide/prediction/prediction_manager.cc
[modify] https://crrev.com/6f5ef89dc45d9fcd3e1b47292212dc8ca7bd35ae/components/optimization_guide/core/hints_manager_unittest.cc
[modify] https://crrev.com/6f5ef89dc45d9fcd3e1b47292212dc8ca7bd35ae/chrome/browser/optimization_guide/optimization_guide_keyed_service.cc
[modify] https://crrev.com/6f5ef89dc45d9fcd3e1b47292212dc8ca7bd35ae/components/optimization_guide/core/hints_manager.h
[modify] https://crrev.com/6f5ef89dc45d9fcd3e1b47292212dc8ca7bd35ae/components/optimization_guide/core/hints_manager.cc
[modify] https://crrev.com/6f5ef89dc45d9fcd3e1b47292212dc8ca7bd35ae/components/optimization_guide/core/hint_cache.cc
[modify] https://crrev.com/6f5ef89dc45d9fcd3e1b47292212dc8ca7bd35ae/components/optimization_guide/core/hint_cache.h
[modify] https://crrev.com/6f5ef89dc45d9fcd3e1b47292212dc8ca7bd35ae/chrome/browser/optimization_guide/chrome_hints_manager_unittest.cc
[modify] https://crrev.com/6f5ef89dc45d9fcd3e1b47292212dc8ca7bd35ae/chrome/browser/optimization_guide/prediction/prediction_manager_unittest.cc
[modify] https://crrev.com/6f5ef89dc45d9fcd3e1b47292212dc8ca7bd35ae/components/optimization_guide/core/optimization_guide_store.h
[modify] https://crrev.com/6f5ef89dc45d9fcd3e1b47292212dc8ca7bd35ae/chrome/browser/optimization_guide/prediction/prediction_manager.h
[modify] https://crrev.com/6f5ef89dc45d9fcd3e1b47292212dc8ca7bd35ae/ios/chrome/browser/optimization_guide/ios_chrome_hints_manager.h
[modify] https://crrev.com/6f5ef89dc45d9fcd3e1b47292212dc8ca7bd35ae/chrome/browser/optimization_guide/chrome_hints_manager.cc
[modify] https://crrev.com/6f5ef89dc45d9fcd3e1b47292212dc8ca7bd35ae/components/optimization_guide/core/hint_cache_unittest.cc


### am...@chromium.org (2022-01-12)

Based on this issue not being web triaggerable and relying solely on a significant amount of user gesture, adjusting security-severity accordingly 

### am...@google.com (2022-01-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-13)

[Comment Deleted]

### am...@chromium.org (2022-01-13)

Congratulations, the VRP Panel has decided to award you $2,000 for this report. A member of our finance team will reach out to you soon to arrange payment. 
Thank you for your efforts and reporting this issue to us! 

### sa...@gmail.com (2022-01-13)

Thank you ^-^

### sa...@gmail.com (2022-01-13)

By the way, as I mentioned in my https://crbug.com/chromium/1281881#c8, there is no need for step 3, it becomes UaF with just 2 clicks.

poc.html:

<html>
<body>
  <script>
   new_window = open("", "", "width=200,height=100");

   setTimeout(() => {
     new_window.close()
     close()
   }, 2000);
   
  </script>
</body>
</html>


1) --disable-popup-blocking.

2) open guest profile.

So I believe the report should have a severity status of high. But I guess it's too late for that now. Anyway, thank you to the whole team for rectifying this report so quickly.

### am...@google.com (2022-01-14)

[Empty comment from Monorail migration]

### sa...@gmail.com (2022-01-17)

Hi amyressler@,What do you think of  https://crbug.com/chromium/1281881#c32?

### am...@google.com (2022-01-17)

https://crbug.com/chromium/1281881#c8 was part of the information evaluated by the VRP Panel for the reward decision. As per https://crbug.com/chromium/1281881#c8, there are still two steps of user interaction required, plus closing the browser. The closing the browser to trigger this provides minimal attacker control and a limited window of exploitation, which is why with all of this combined, a lower reward amount was decided upon. 

Additionally, while this is an issue in the browser process, because this issue requires a non-standard flag to be set + user interaction + closing the browser to trigger, the appropriate severity of this issue would be medium severity based on severity guidelines. 


### am...@chromium.org (2022-01-19)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1281881?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058312)*
