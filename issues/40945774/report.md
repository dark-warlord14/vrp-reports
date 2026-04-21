# Security: AddressSanitizer: heap-use-after-free on address 0x11f602026080 at pc 0x7ffc02e5a899 bp 0x000bbe7fed80 sp 0x000bbe7fedc8

| Field | Value |
|-------|-------|
| **Issue ID** | [40945774](https://issues.chromium.org/issues/40945774) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Passwords |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 18...@gmail.com |
| **Assignee** | vs...@google.com |
| **Created** | 2023-11-25 |
| **Bounty** | $1,000.00 |

## Description

Hey, the bug introduced has discover accidental by when I want to reproduce https://crbug.com/chromium/1504487 c#9:

1. https://bugs.chromium.org/p/chromium/issues/detail?id=1504487#c9.

 vsemeniuk@google.com  has offer a new way to reproduce https://crbug.com/chromium/1504487 , even if I am failed. But seems I still found a new bug.

I don't inversitigate it more, Because I am a little busy now... But I suspect it should different bug , because it have different asan log.



## Attachments

- [asan_other.log](attachments/asan_other.log) (text/plain, 31.6 KB)
- [repro_fun.mp4](attachments/repro_fun.mp4) (video/mp4, 8.7 MB)

## Timeline

### [Deleted User] (2023-11-25)

[Empty comment from Monorail migration]

### 18...@gmail.com (2023-11-25)

use this step to reproduce the bug.
1. apply https://crbug.com/chromium/1504487 patch. compile it with asan.
2. run ".\out\asan\chrome.exe  --user-data-dir=D:\mini_tmp"
2. open "chrome://password-manager/passwords"
 note: at here, just open this one tab, that's the  difference with previous one.
3. click download file. then input computer password, make auth success.
4. click download file again. follow ctrl+w(This will close this only tab, which will close the browser too, so seems there maybe a browser shutdown bug).
5. asan log will show again.

If there are a cve for this bug, plz credit as "@18楼梦想改造家". Thx!

### 18...@gmail.com (2023-11-25)

I think I could ensure this is a different security issue, base on two things.

1. at https://bugs.chromium.org/p/chromium/issues/detail?id=1504487#c3, I offer a fix.patch, which should fix previous bug. I apply this patch, found this bug still could be triggerd.
2. the previous bug(https://crbug.com/chromium/1504487) depends on 2 tabs or more tabs. we must have at least 2 tabs. Because |weak_ptr_factory_| passed in |OnExportPasswordsAuthResult|, close browser will invalidate`|weak_ptr_factory_|`. which make the bug reproduce failed. however, when I try to reproduce this bug, I found 1 tab is enough.

### 18...@gmail.com (2023-11-27)

If anybody see this bug, could u cc to  vsemeniuk@google.com? Thx.

And  vsemeniuk@google.com, I don't fully understand your patch, could u see https://crbug.com/chromium/1505176#c3? Thx.

### 18...@gmail.com (2023-11-27)

after the fix patch of https://crbug.com/chromium/1504487, the bug still could be triggered. 

here is my test commit:

``` c++
commit 65b0377b746a1a74da64533f851863303b8d2a86 (HEAD, origin/main, origin/HEAD)
Author: Gyuyoung Kim <gyuyoung@igalia.com>
Date:   Mon Nov 27 13:06:28 2023 +0000

    [iOS Blink] Fix CaretPositionForOffsetText.CaretPositionForOffsets

    crrev.com/c/5042662 added the test, but the test has been failing on
    iOS for Blink port because it only considered Mac port in the test.

    This CL shares the caret position of the Mac port with iOS port
    by using IS_APPLE guard.

    Bug: 1503304
    Change-Id: I44c46b584b64b18500e38b989719710214a0e1dd
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5058691
    Commit-Queue: Stephen Chenney <schenney@chromium.org>
    Reviewed-by: Stephen Chenney <schenney@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1229268}
```

here is the asan log:

``` c++
PS D:\chrome\src> out/asan/chrome  --user-data-dir=D:\mini_tmp
[17412:4764:1127/234544.697:ERROR:policy_logger.cc(156)] :components\enterprise\browser\controller\chrome_browser_cloud_management_controller.cc(161) Cloud management controller initialization aborted as CBCM is not enabled. Please use the `--enable-chrome-browser-cloud-management` command line flag to enable it if you are not using the official Google Chrome build.
[17412:4764:1127/234601.448:ERROR:observer_list.h(270)] Check failed: observers_.empty().
For observer stack traces, build with `dcheck_always_on=true`.
=================================================================
==17412==ERROR: AddressSanitizer: heap-use-after-free on address 0x1249d3427e80 at pc 0x7ffa0a9d55e2 bp 0x0045105ff0a0 sp 0x0045105ff0e8
READ of size 8 at 0x1249d3427e80 thread T0
    #0 0x7ffa0a9d55e1 in base::ScopedObservationTraits<syncer::SyncService,syncer::SyncServiceObserver>::RemoveObserver D:\chrome\src\base\scoped_observation_traits.h:74
    #1 0x7ffa0a9d55e1 in base::ScopedObservation<class syncer::SyncService, class syncer::SyncServiceObserver>::Reset(void) D:\chrome\src\base\scoped_observation.h:115:7
    #2 0x7ffa0a9d4e37 in base::ScopedObservation<class syncer::SyncService, class syncer::SyncServiceObserver>::~ScopedObservation<class syncer::SyncService, class syncer::SyncServiceObserver>(void) D:\chrome\src\base\scoped_observation.h:101:26
    #3 0x7ffa1eb85373 in extensions::PasswordsPrivateDelegateImpl::~PasswordsPrivateDelegateImpl(void) D:\chrome\src\chrome\browser\extensions\api\passwords_private\passwords_private_delegate_impl.cc:327:1
    #4 0x7ffa1eb93489 in extensions::PasswordsPrivateDelegateImpl::`scalar deleting dtor'(unsigned int) D:\chrome\src\chrome\browser\extensions\api\passwords_private\passwords_private_delegate_impl.cc:324:63
    #5 0x7ffa1eb9a45a in scoped_refptr<extensions::PasswordsPrivateDelegateImpl>::Release D:\chrome\src\base\memory\scoped_refptr.h:368
    #6 0x7ffa1eb9a45a in scoped_refptr<extensions::PasswordsPrivateDelegateImpl>::~scoped_refptr D:\chrome\src\base\memory\scoped_refptr.h:271
    #7 0x7ffa1eb9a45a in std::__Cr::__tuple_leaf<0,scoped_refptr<extensions::PasswordsPrivateDelegateImpl>,0>::~__tuple_leaf D:\chrome\src\third_party\libc++\src\include\tuple:305
    #8 0x7ffa1eb9a45a in std::__Cr::tuple<scoped_refptr<extensions::PasswordsPrivateDelegateImpl> >::~tuple D:\chrome\src\third_party\libc++\src\include\tuple:578
    #9 0x7ffa1eb9a45a in base::internal::BindState<bool (extensions::PasswordsPrivateDelegateImpl::*)(bool),scoped_refptr<extensions::PasswordsPrivateDelegateImpl> >::~BindState D:\chrome\src\base\functional\bind_internal.h:1157
    #10 0x7ffa1eb9a45a in base::internal::BindState<bool (__cdecl extensions::PasswordsPrivateDelegateImpl::*)(bool), class scoped_refptr<class extensions::PasswordsPrivateDelegateImpl>>::Destroy(class base::internal::BindStateBase const *) D:\chrome\src\base\functional\bind_internal.h:1160:5
    #11 0x7ffa036e03d2 in base::OnceCallback<std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > (base::expected<std::__Cr::vector<unsigned char,std::__Cr::allocator<unsigned char> >,unexportable_keys::ServiceError>)>::~OnceCallback D:\chrome\src\base\functional\callback.h:98
    #12 0x7ffa036e03d2 in std::__Cr::__tuple_leaf<0,base::OnceCallback<std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > (base::expected<std::__Cr::vector<unsigned char,std::__Cr::allocator<unsigned char> >,unexportable_keys::ServiceError>)>,0>::~__tuple_leaf D:\chrome\src\third_party\libc++\src\include\tuple:305
    #13 0x7ffa036e03d2 in std::__Cr::__tuple_impl<std::__Cr::__tuple_indices<0,1>,base::OnceCallback<std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > (base::expected<std::__Cr::vector<unsigned char,std::__Cr::allocator<unsigned char> >,unexportable_keys::ServiceError>)>,base::OnceCallback<void (std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >)> >::~__tuple_impl D:\chrome\src\third_party\libc++\src\include\tuple:491
    #14 0x7ffa036e03d2 in std::__Cr::tuple<base::OnceCallback<std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > (base::expected<std::__Cr::vector<unsigned char,std::__Cr::allocator<unsigned char> >,unexportable_keys::ServiceError>)>,base::OnceCallback<void (std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >)> >::~tuple D:\chrome\src\third_party\libc++\src\include\tuple:578
    #15 0x7ffa036e03d2 in base::internal::BindState<`lambda at ..\..\base\functional\callback_internal.h:208:12',base::OnceCallback<std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > (base::expected<std::__Cr::vector<unsigned char,std::__Cr::allocator<unsigned char> >,unexportable_keys::ServiceError>)>,base::OnceCallback<void (std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >)> >::~BindState D:\chrome\src\base\functional\bind_internal.h:1157
    #16 0x7ffa036e03d2 in base::internal::BindState<class `public: class views::Builder<class views::View> & __cdecl views::BaseViewBuilderT<class views::Builder<class views::View>>::CustomConfigure(class base::OnceCallback<void __cdecl(class views::View *)>) &'::`1'::<lambda_1>, class base::OnceCallback<void __cdecl(class views::View *)>, class base::OnceCallback<void __cdecl(class views::View *)>>::Destroy(class base::internal::BindStateBase const *) D:\chrome\src\base\functional\bind_internal.h:1160:5
    #17 0x7ff9ff6d7765 in base::RepeatingCallback<int (int, int)>::~RepeatingCallback D:\chrome\src\base\functional\callback.h:301
    #18 0x7ff9ff6d7765 in base::internal::BindState<base::RepeatingCallback<int (int, int)>,int,unsigned short>::~BindState D:\chrome\src\base\functional\bind_internal.h:1157
    #19 0x7ff9ff6d7765 in base::internal::BindState<class base::RepeatingCallback<(enum policy::PolicyDomain, class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>> const &)>, enum policy::PolicyDomain>::Destroy(class base::internal::BindStateBase const *) D:\chrome\src\base\functional\bind_internal.h:1160:5
    #20 0x7ffa11bbd504 in std::__Cr::__destroy_at D:\chrome\src\third_party\libc++\src\include\__memory\construct_at.h:69
    #21 0x7ffa11bbd504 in std::__Cr::destroy_at D:\chrome\src\third_party\libc++\src\include\__memory\construct_at.h:104
    #22 0x7ffa11bbd504 in std::__Cr::allocator_traits<std::__Cr::allocator<base::sequence_manager::Task> >::destroy D:\chrome\src\third_party\libc++\src\include\__memory\allocator_traits.h:323
    #23 0x7ffa11bbd504 in std::__Cr::vector<base::sequence_manager::Task,std::__Cr::allocator<base::sequence_manager::Task> >::__base_destruct_at_end D:\chrome\src\third_party\libc++\src\include\vector:944
    #24 0x7ffa11bbd504 in std::__Cr::vector<base::sequence_manager::Task,std::__Cr::allocator<base::sequence_manager::Task> >::__clear D:\chrome\src\third_party\libc++\src\include\vector:938
    #25 0x7ffa11bbd504 in std::__Cr::vector<base::sequence_manager::Task,std::__Cr::allocator<base::sequence_manager::Task> >::clear D:\chrome\src\third_party\libc++\src\include\vector:723
    #26 0x7ffa11bbd504 in base::IntrusiveHeap<struct base::sequence_manager::Task, struct base::sequence_manager::internal::TaskQueueImpl::DelayedIncomingQueue::Compare, struct base::DefaultHeapHandleAccessor<struct base::sequence_manager::Task>>::clear(void) D:\chrome\src\base\containers\intrusive_heap.h:783:15
    #27 0x7ffa11baa73e in base::IntrusiveHeap<base::sequence_manager::Task,base::sequence_manager::internal::TaskQueueImpl::DelayedIncomingQueue::Compare,base::DefaultHeapHandleAccessor<base::sequence_manager::Task> >::~IntrusiveHeap D:\chrome\src\base\containers\intrusive_heap.h:743
    #28 0x7ffa11baa73e in base::sequence_manager::internal::TaskQueueImpl::DelayedIncomingQueue::~DelayedIncomingQueue D:\chrome\src\base\task\sequence_manager\task_queue_impl.cc:1521
    #29 0x7ffa11baa73e in base::sequence_manager::internal::TaskQueueImpl::UnregisterTaskQueue(void) D:\chrome\src\base\task\sequence_manager\task_queue_impl.cc:288:1
    #30 0x7ffa0e189743 in base::sequence_manager::internal::SequenceManagerImpl::UnregisterTaskQueueImpl(class std::__Cr::unique_ptr<class base::sequence_manager::internal::TaskQueueImpl, struct std::__Cr::default_delete<class base::sequence_manager::internal::TaskQueueImpl>>) D:\chrome\src\base\task\sequence_manager\sequence_manager_impl.cc:412:15
    #31 0x7ffa0e1843c9 in base::sequence_manager::TaskQueue::Handle::reset(void) D:\chrome\src\base\task\sequence_manager\task_queue.cc:98:22
    #32 0x7ffa08dbcd9e in content::BrowserTaskQueues::~BrowserTaskQueues(void) D:\chrome\src\content\browser\scheduler\browser_task_queues.cc:213:22
    #33 0x7ffa08dbdcc0 in content::BrowserUIThreadScheduler::~BrowserUIThreadScheduler(void) D:\chrome\src\content\browser\scheduler\browser_ui_thread_scheduler.cc:123:53
    #34 0x7ffa08dbad1a in std::__Cr::default_delete<content::BrowserUIThreadScheduler>::operator() D:\chrome\src\third_party\libc++\src\include\__memory\unique_ptr.h:68
    #35 0x7ffa08dbad1a in std::__Cr::unique_ptr<class content::BrowserUIThreadScheduler, struct std::__Cr::default_delete<class content::BrowserUIThreadScheduler>>::reset(class content::BrowserUIThreadScheduler *) D:\chrome\src\third_party\libc++\src\include\__memory\unique_ptr.h:297:7
    #36 0x7ffa08dbaca0 in std::__Cr::unique_ptr<content::BrowserUIThreadScheduler,std::__Cr::default_delete<content::BrowserUIThreadScheduler> >::~unique_ptr D:\chrome\src\third_party\libc++\src\include\__memory\unique_ptr.h:263
    #37 0x7ffa08dbaca0 in content::BrowserTaskExecutor::UIThreadExecutor::~UIThreadExecutor D:\chrome\src\content\browser\scheduler\browser_task_executor.cc:320
    #38 0x7ffa08dbaca0 in content::BrowserTaskExecutor::UIThreadExecutor::`scalar deleting dtor'(unsigned int) D:\chrome\src\content\browser\scheduler\browser_task_executor.cc:320:58
    #39 0x7ffa08db9c41 in std::__Cr::default_delete<content::BrowserTaskExecutor::UIThreadExecutor>::operator() D:\chrome\src\third_party\libc++\src\include\__memory\unique_ptr.h:68
    #40 0x7ffa08db9c41 in std::__Cr::unique_ptr<content::BrowserTaskExecutor::UIThreadExecutor,std::__Cr::default_delete<content::BrowserTaskExecutor::UIThreadExecutor> >::reset D:\chrome\src\third_party\libc++\src\include\__memory\unique_ptr.h:297
    #41 0x7ffa08db9c41 in content::BrowserTaskExecutor::Shutdown(void) D:\chrome\src\content\browser\scheduler\browser_task_executor.cc:224:30
    #42 0x7ffa0c715be0 in content::ContentMainRunnerImpl::Shutdown(void) D:\chrome\src\content\app\content_main_runner_impl.cc:1323:3
    #43 0x7ffa0c70e94c in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) D:\chrome\src\content\app\content_main.cc:337:24
    #44 0x7ffa0c70f5c8 in content::ContentMain(struct content::ContentMainParams) D:\chrome\src\content\app\content_main.cc:347:10
    #45 0x7ff9ff2c1746 in ChromeMain D:\chrome\src\chrome\app\chrome_main.cc:194:12
    #46 0x7ff6e7b960b4 in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) D:\chrome\src\chrome\app\main_dll_loader_win.cc:169:12
    #47 0x7ff6e7b92a51 in main D:\chrome\src\chrome\app\chrome_exe_main_win.cc:392:20
    #48 0x7ff6e7fc48d3 in invoke_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #49 0x7ff6e7fc48d3 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #50 0x7ffab6857343  (C:\WINDOWS\System32\KERNEL32.DLL+0x180017343)
    #51 0x7ffab77226b0  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800526b0)

0x1249d3427e80 is located 0 bytes inside of 1376-byte region [0x1249d3427e80,0x1249d34283e0)
freed by thread T0 here:
    #0 0x7ff6e7c5d7cd in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ffa11794551 in syncer::SyncServiceImpl::`scalar deleting dtor'(unsigned int) D:\chrome\src\components\sync\service\sync_service_impl.cc:228:37
    #2 0x7ffa0f5395c5 in std::__Cr::destroy_at D:\chrome\src\third_party\libc++\src\include\__memory\construct_at.h:104
    #3 0x7ffa0f5395c5 in std::__Cr::allocator_traits<std::__Cr::allocator<std::__Cr::__tree_node<std::__Cr::__value_type<void *,std::__Cr::unique_ptr<KeyedService,std::__Cr::default_delete<KeyedService> > >,void *> > >::destroy D:\chrome\src\third_party\libc++\src\include\__memory\allocator_traits.h:323
    #4 0x7ffa0f5395c5 in std::__Cr::__tree<std::__Cr::__value_type<void *,std::__Cr::unique_ptr<KeyedService,std::__Cr::default_delete<KeyedService> > >,std::__Cr::__map_value_compare<void *,std::__Cr::__value_type<void *,std::__Cr::unique_ptr<KeyedService,std::__Cr::default_delete<KeyedService> > >,std::__Cr::less<void *>,1>,std::__Cr::allocator<std::__Cr::__value_type<void *,std::__Cr::unique_ptr<KeyedService,std::__Cr::default_delete<KeyedService> > > > >::erase D:\chrome\src\third_party\libc++\src\include\__tree:2435
    #5 0x7ffa0f5395c5 in std::__Cr::map<void *, class std::__Cr::unique_ptr<class KeyedService, struct std::__Cr::default_delete<class KeyedService>>, struct std::__Cr::less<void *>, class std::__Cr::allocator<struct std::__Cr::pair<void *const, class std::__Cr::unique_ptr<class KeyedService, struct std::__Cr::default_delete<class KeyedService>>>>>::erase(class std::__Cr::__map_iterator<class std::__Cr::__tree_iterator<struct std::__Cr::__value_type<void *, class std::__Cr::unique_ptr<class KeyedService, struct std::__Cr::default_delete<class KeyedService>>>, class std::__Cr::__tree_node<struct std::__Cr::__value_type<void *, class std::__Cr::unique_ptr<class KeyedService, struct std::__Cr::default_delete<class KeyedService>>>, void *> *, __int64>>) D:\chrome\src\third_party\libc++\src\include\map:1453:56
    #6 0x7ffa0f53942a in KeyedServiceFactory::Disassociate(void *) D:\chrome\src\components\keyed_service\core\keyed_service_factory.cc:119:14
    #7 0x7ffa0f53984a in KeyedServiceFactory::ContextDestroyed(void *) D:\chrome\src\components\keyed_service\core\keyed_service_factory.cc:130:3
    #8 0x7ffa12e829bf in DependencyManager::DestroyFactoriesInOrder D:\chrome\src\components\keyed_service\core\dependency_manager.cc:186
    #9 0x7ffa12e829bf in DependencyManager::PerformInterlockedTwoPhaseShutdown(class DependencyManager *, void *, class DependencyManager *, void *) D:\chrome\src\components\keyed_service\core\dependency_manager.cc:159:3
    #10 0x7ffa1180d0c5 in ProfileImpl::~ProfileImpl(void) D:\chrome\src\chrome\browser\profiles\profile_impl.cc:948:3
    #11 0x7ffa11811967 in ProfileImpl::`scalar deleting dtor'(unsigned int) D:\chrome\src\chrome\browser\profiles\profile_impl.cc:894:29
    #12 0x7ffa118451d3 in std::__Cr::default_delete<Profile>::operator() D:\chrome\src\third_party\libc++\src\include\__memory\unique_ptr.h:68
    #13 0x7ffa118451d3 in std::__Cr::unique_ptr<Profile,std::__Cr::default_delete<Profile> >::reset D:\chrome\src\third_party\libc++\src\include\__memory\unique_ptr.h:297
    #14 0x7ffa118451d3 in ProfileDestroyer::DestroyOriginalProfileNow(class std::__Cr::unique_ptr<class Profile, struct std::__Cr::default_delete<class Profile>>) D:\chrome\src\chrome\browser\profiles\profile_destroyer.cc:273:11
    #15 0x7ffa1184721e in OriginalProfileDestroyer::DoDestroyUnderlyingProfile(void) D:\chrome\src\chrome\browser\profiles\profile_destroyer.cc:105:5
    #16 0x7ffa11843447 in ProfileDestroyer::Timeout D:\chrome\src\chrome\browser\profiles\profile_destroyer.cc:435
    #17 0x7ffa11843447 in ProfileDestroyer::Start(class std::__Cr::set<class content::RenderProcessHost *, struct std::__Cr::less<class content::RenderProcessHost *>, class std::__Cr::allocator<class content::RenderProcessHost *>> const &) D:\chrome\src\chrome\browser\profiles\profile_destroyer.cc:326:5
    #18 0x7ffa11842491 in ProfileDestroyer::DestroyOriginalProfileWhenAppropriateWithTimeout(class std::__Cr::unique_ptr<class Profile, struct std::__Cr::default_delete<class Profile>>, class base::TimeDelta) D:\chrome\src\chrome\browser\profiles\profile_destroyer.cc:152:22
    #19 0x7ffa11841f62 in ProfileDestroyer::DestroyOriginalProfileWhenAppropriate(class std::__Cr::unique_ptr<class Profile, struct std::__Cr::default_delete<class Profile>>) D:\chrome\src\chrome\browser\profiles\profile_destroyer.cc:121:3
    #20 0x7ffa0df302d1 in ProfileManager::ProfileInfo::~ProfileInfo(void) D:\chrome\src\chrome\browser\profiles\profile_manager.cc:1632:3
    #21 0x7ffa0df37f6a in std::__Cr::default_delete<ProfileManager::ProfileInfo>::operator() D:\chrome\src\third_party\libc++\src\include\__memory\unique_ptr.h:68
    #22 0x7ffa0df37f6a in std::__Cr::unique_ptr<class ProfileManager::ProfileInfo, struct std::__Cr::default_delete<class ProfileManager::ProfileInfo>>::reset(class ProfileManager::ProfileInfo *) D:\chrome\src\third_party\libc++\src\include\__memory\unique_ptr.h:297:7
    #23 0x7ffa0df360d7 in std::__Cr::unique_ptr<ProfileManager::ProfileInfo,std::__Cr::default_delete<ProfileManager::ProfileInfo> >::~unique_ptr D:\chrome\src\third_party\libc++\src\include\__memory\unique_ptr.h:263
    #24 0x7ffa0df360d7 in std::__Cr::pair<const base::FilePath,std::__Cr::unique_ptr<ProfileManager::ProfileInfo,std::__Cr::default_delete<ProfileManager::ProfileInfo> > >::~pair D:\chrome\src\third_party\libc++\src\include\__utility\pair.h:81
    #25 0x7ffa0df360d7 in std::__Cr::__destroy_at<struct std::__Cr::pair<class base::FilePath const, class std::__Cr::unique_ptr<class ProfileManager::ProfileInfo, struct std::__Cr::default_delete<class ProfileManager::ProfileInfo>>>, 0>(struct std::__Cr::pair<class base::FilePath const, class std::__Cr::unique_ptr<class ProfileManager::ProfileInfo, struct std::__Cr::default_delete<class ProfileManager::ProfileInfo>>> *) D:\chrome\src\third_party\libc++\src\include\__memory\construct_at.h:69:13
    #26 0x7ffa0df36099 in std::__Cr::destroy_at D:\chrome\src\third_party\libc++\src\include\__memory\construct_at.h:104
    #27 0x7ffa0df36099 in std::__Cr::allocator_traits<std::__Cr::allocator<std::__Cr::__tree_node<std::__Cr::__value_type<base::FilePath,std::__Cr::unique_ptr<ProfileManager::ProfileInfo,std::__Cr::default_delete<ProfileManager::ProfileInfo> > >,void *> > >::destroy D:\chrome\src\third_party\libc++\src\include\__memory\allocator_traits.h:323
    #28 0x7ffa0df36099 in std::__Cr::__tree<struct std::__Cr::__value_type<class base::FilePath, class std::__Cr::unique_ptr<class ProfileManager::ProfileInfo, struct std::__Cr::default_delete<class ProfileManager::ProfileInfo>>>, class std::__Cr::__map_value_compare<class base::FilePath, struct std::__Cr::__value_type<class base::FilePath, class std::__Cr::unique_ptr<class ProfileManager::ProfileInfo, struct std::__Cr::default_delete<class ProfileManager::ProfileInfo>>>, struct std::__Cr::less<class base::FilePath>, 1>, class std::__Cr::allocator<struct std::__Cr::__value_type<class base::FilePath, class std::__Cr::unique_ptr<class ProfileManager::ProfileInfo, struct std::__Cr::default_delete<class ProfileManager::ProfileInfo>>>>>::destroy(class std::__Cr::__tree_node<struct std::__Cr::__value_type<class base::FilePath, class std::__Cr::unique_ptr<class ProfileManager::ProfileInfo, struct std::__Cr::default_delete<class ProfileManager::ProfileInfo>>>, void *> *) D:\chrome\src\third_party\libc++\src\include\__tree:1814:9
    #29 0x7ffa0df3984a in std::__Cr::__tree<std::__Cr::__value_type<base::FilePath,std::__Cr::unique_ptr<ProfileManager::ProfileInfo,std::__Cr::default_delete<ProfileManager::ProfileInfo> > >,std::__Cr::__map_value_compare<base::FilePath,std::__Cr::__value_type<base::FilePath,std::__Cr::unique_ptr<ProfileManager::ProfileInfo,std::__Cr::default_delete<ProfileManager::ProfileInfo> > >,std::__Cr::less<base::FilePath>,1>,std::__Cr::allocator<std::__Cr::__value_type<base::FilePath,std::__Cr::unique_ptr<ProfileManager::ProfileInfo,std::__Cr::default_delete<ProfileManager::ProfileInfo> > > > >::clear D:\chrome\src\third_party\libc++\src\include\__tree:1851
    #30 0x7ffa0df3984a in std::__Cr::map<base::FilePath,std::__Cr::unique_ptr<ProfileManager::ProfileInfo,std::__Cr::default_delete<ProfileManager::ProfileInfo> >,std::__Cr::less<base::FilePath>,std::__Cr::allocator<std::__Cr::pair<const base::FilePath,std::__Cr::unique_ptr<ProfileManager::ProfileInfo,std::__Cr::default_delete<ProfileManager::ProfileInfo> > > > >::clear D:\chrome\src\third_party\libc++\src\include\map:1461
    #31 0x7ffa0df3984a in ProfileManager::~ProfileManager(void) D:\chrome\src\chrome\browser\profiles\profile_manager.cc:474:18
    #32 0x7ffa0df34c8b in ProfileManager::`scalar deleting dtor'(unsigned int) D:\chrome\src\chrome\browser\profiles\profile_manager.cc:446:35
    #33 0x7ffa1550a23c in std::__Cr::default_delete<ProfileManager>::operator() D:\chrome\src\third_party\libc++\src\include\__memory\unique_ptr.h:68
    #34 0x7ffa1550a23c in std::__Cr::unique_ptr<ProfileManager,std::__Cr::default_delete<ProfileManager> >::reset D:\chrome\src\third_party\libc++\src\include\__memory\unique_ptr.h:297
    #35 0x7ffa1550a23c in BrowserProcessImpl::StartTearDown(void) D:\chrome\src\chrome\browser\browser_process_impl.cc:499:22
    #36 0x7ffa1170df39 in ChromeBrowserMainParts::PostMainMessageLoopRun(void) D:\chrome\src\chrome\browser\chrome_browser_main.cc:1909:21
    #37 0x7ffa079b3b65 in content::BrowserMainLoop::ShutdownThreadsAndCleanUp(void) D:\chrome\src\content\browser\browser_main_loop.cc:1147:13
    #38 0x7ffa079bbb17 in content::BrowserMainRunnerImpl::Shutdown(void) D:\chrome\src\content\browser\browser_main_runner_impl.cc:176:17
    #39 0x7ffa079a8e3d in content::BrowserMain(struct content::MainFunctionParams) D:\chrome\src\content\browser\browser_main.cc:43:16
    #40 0x7ffa0c7107df in content::RunBrowserProcessMain(struct content::MainFunctionParams, class content::ContentMainDelegate *) D:\chrome\src\content\app\content_main_runner_impl.cc:706:10
    #41 0x7ffa0c7147e6 in content::ContentMainRunnerImpl::RunBrowser(struct content::MainFunctionParams, bool) D:\chrome\src\content\app\content_main_runner_impl.cc:1294:10
    #42 0x7ffa0c713e51 in content::ContentMainRunnerImpl::Run(void) D:\chrome\src\content\app\content_main_runner_impl.cc:1138:12
    #43 0x7ffa0c70e915 in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) D:\chrome\src\content\app\content_main.cc:334:36

previously allocated by thread T0 here:
    #0 0x7ff6e7c5d8cd in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffa24c6206e in operator new(unsigned __int64) D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
    #2 0x7ffa0df14a51 in std::__Cr::make_unique D:\chrome\src\third_party\libc++\src\include\__memory\unique_ptr.h:685
    #3 0x7ffa0df14a51 in `anonymous namespace'::BuildSyncService D:\chrome\src\chrome\browser\sync\sync_service_factory.cc:170:7
    #4 0x7ffa0df14344 in SyncServiceFactory::BuildServiceInstanceForBrowserContext(class content::BrowserContext *) const D:\chrome\src\chrome\browser\sync\sync_service_factory.cc:302:10
    #5 0x7ffa10945907 in RefcountedBrowserContextKeyedServiceFactory::BuildServiceInstanceFor(void *) const D:\chrome\src\components\keyed_service\content\refcounted_browser_context_keyed_service_factory.cc:94:10
    #6 0x7ffa0f5386a9 in KeyedServiceFactory::GetServiceForContext(void *, bool) D:\chrome\src\components\keyed_service\core\keyed_service_factory.cc:93:15
    #7 0x7ffa14f1449b in commerce::ShoppingServiceFactory::BuildServiceInstanceForBrowserContext(class content::BrowserContext *) const D:\chrome\src\chrome\browser\commerce\shopping_service_factory.cc:91:7
    #8 0x7ffa10945907 in RefcountedBrowserContextKeyedServiceFactory::BuildServiceInstanceFor(void *) const D:\chrome\src\components\keyed_service\content\refcounted_browser_context_keyed_service_factory.cc:94:10
    #9 0x7ffa0f5386a9 in KeyedServiceFactory::GetServiceForContext(void *, bool) D:\chrome\src\components\keyed_service\core\keyed_service_factory.cc:93:15
    #10 0x7ffa12e81d8e in DependencyManager::CreateContextServices(void *, bool) D:\chrome\src\components\keyed_service\core\dependency_manager.cc:111:16
    #11 0x7ffa1094614e in BrowserContextDependencyManager::DoCreateBrowserContextServices(class content::BrowserContext *, bool) D:\chrome\src\components\keyed_service\content\browser_context_dependency_manager.cc:46:22
    #12 0x7ffa1180fe8d in ProfileImpl::OnLocaleReady(enum Profile::CreateMode) D:\chrome\src\chrome\browser\profiles\profile_impl.cc:1173:51
    #13 0x7ffa11808dd4 in ProfileImpl::OnPrefsLoaded(enum Profile::CreateMode, bool) D:\chrome\src\chrome\browser\profiles\profile_impl.cc:1217:3
    #14 0x7ffa11805864 in ProfileImpl::ProfileImpl(class base::FilePath const &, class Profile::Delegate *, enum Profile::CreateMode, class base::Time, class scoped_refptr<class base::SequencedTaskRunner>) D:\chrome\src\chrome\browser\profiles\profile_impl.cc:531:5
    #15 0x7ffa1180485f in Profile::CreateProfile(class base::FilePath const &, class Profile::Delegate *, enum Profile::CreateMode) D:\chrome\src\chrome\browser\profiles\profile_impl.cc:364:59
    #16 0x7ffa0df2a07c in ProfileManager::CreateProfileHelper(class base::FilePath const &) D:\chrome\src\chrome\browser\profiles\profile_manager.cc:1261:10
    #17 0x7ffa0df208d4 in ProfileManager::CreateAndInitializeProfile(class base::FilePath const &) D:\chrome\src\chrome\browser\profiles\profile_manager.cc:1814:38
    #18 0x7ffa0df1e8d8 in ProfileManager::GetProfile(class base::FilePath const &) D:\chrome\src\chrome\browser\profiles\profile_manager.cc:713:10
    #19 0x7ffa15521b83 in GetStartupProfile(class base::FilePath const &, class base::CommandLine const &) D:\chrome\src\chrome\browser\ui\startup\startup_browser_creator.cc:1655:39
    #20 0x7ffa1170cb22 in `anonymous namespace'::CreateInitialProfile D:\chrome\src\chrome\browser\chrome_browser_main.cc:465:18
    #21 0x7ffa117091a3 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl(void) D:\chrome\src\chrome\browser\chrome_browser_main.cc:1570:37
    #22 0x7ffa11708618 in ChromeBrowserMainParts::PreMainMessageLoopRun(void) D:\chrome\src\chrome\browser\chrome_browser_main.cc:1221:18
    #23 0x7ffa079aff3c in content::BrowserMainLoop::PreMainMessageLoopRun(void) D:\chrome\src\content\browser\browser_main_loop.cc:1003:28
    #24 0x7ffa079b857d in base::internal::FunctorTraits<int (content::BrowserMainLoop::*)()>::Invoke D:\chrome\src\base\functional\bind_internal.h:713
    #25 0x7ffa079b857d in base::internal::InvokeHelper<0,int,0>::MakeItSo D:\chrome\src\base\functional\bind_internal.h:868
    #26 0x7ffa079b857d in base::internal::Invoker<base::internal::BindState<int (content::BrowserMainLoop::*)(),base::internal::UnretainedWrapper<content::BrowserMainLoop,base::unretained_traits::MayNotDangle,0> >,int ()>::RunImpl D:\chrome\src\base\functional\bind_internal.h:968
    #27 0x7ffa079b857d in base::internal::Invoker<struct base::internal::BindState<int (__cdecl content::BrowserMainLoop::*)(void), class base::internal::UnretainedWrapper<class content::BrowserMainLoop, struct base::unretained_traits::MayNotDangle, 0>>, (void)>::RunOnce(class base::internal::BindStateBase *) D:\chrome\src\base\functional\bind_internal.h:919:12
    #28 0x7ff9ff7734b9 in base::OnceCallback<(void)>::Run(void) && D:\chrome\src\base\functional\callback.h:156:12
    #29 0x7ffa090e6596 in content::StartupTaskRunner::RunAllTasksNow(void) D:\chrome\src\content\browser\startup_task_runner.cc:42:29
    #30 0x7ffa079aec41 in content::BrowserMainLoop::CreateStartupTasks(void) D:\chrome\src\content\browser\browser_main_loop.cc:914:25
    #31 0x7ffa079bacf1 in content::BrowserMainRunnerImpl::Initialize(struct content::MainFunctionParams) D:\chrome\src\content\browser\browser_main_runner_impl.cc:139:15

SUMMARY: AddressSanitizer: heap-use-after-free D:\chrome\src\base\scoped_observation_traits.h:74 in base::ScopedObservationTraits<syncer::SyncService,syncer::SyncServiceObserver>::RemoveObserver
Shadow bytes around the buggy address:
  0x1249d3427c00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1249d3427c80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1249d3427d00: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x1249d3427d80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1249d3427e00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
=>0x1249d3427e80:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1249d3427f00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1249d3427f80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1249d3428000: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1249d3428080: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1249d3428100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==17412==ADDITIONAL INFO

==17412==Note: Please include this section with the ASan report.
Task trace:


MiraclePtr Status: MANUAL ANALYSIS REQUIRED
A pointer to the same region was extracted from a raw_ptr<T> object prior to this crash.
To determine the protection status, enable extraction warnings and check whether the raw_ptr<T> object can be destroyed or overwritten between the extraction and use.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==17412==END OF ADDITIONAL INFO
==17412==ABORTING
```


### pg...@google.com (2023-11-27)

[Empty comment from Monorail migration]

### ma...@google.com (2023-11-28)

This looks like a browser UAF, requiring highly specific user interaction, a browser shutdown, and a patch to make a race more deterministic. Provisionally setting Severity-Medium and FoundIn-118. I didn't attempt to repro, but the recording and stack trace look plausible.

Passwords folks, could you PTAL?

[Monorail components: UI>Browser>Passwords]

### [Deleted User] (2023-11-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-28)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-28)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2023-11-28)

(I am a bot: this is an auto-cc on a security bug)

### vs...@google.com (2023-11-29)

It's easier to reproduce the issue on Mac because there the auth dialog doesn't freeze Chrome (although you need to have biometric authentication enabled). Again I haven't used your patch. Reproduction steps are the following:

1. Open "chrome://password-manager/passwords"
2. Trigger authentication (it doesn't have to be export, viewing a password also works).
3. Close the tab. 

 I noticed two problems:
1. PasswordsPrivateDelegateImpl doesn't remove itself from SyncService observers on SyncShutdown. This is what we see in the stacktrase in https://crbug.com/chromium/1505176#c2. I fixed this here: https://crrev.com/c/5070554
2. Even though the profile is destroyed PasswordsPrivateDelegateImpl is still retained in memory because of [1]. This is also a bug. The fix is here: crrev.com/c/5070036

Arguably fixing 2 will also prevent 1. But it's safer to fix both problems.  

[1]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/api/passwords_private/passwords_private_delegate_impl.cc;l=1147-1148

### gi...@appspot.gserviceaccount.com (2023-11-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fe6b4163351f503045b83bffd870d18da622a865

commit fe6b4163351f503045b83bffd870d18da622a865
Author: Viktor Semeniuk <vsemeniuk@google.com>
Date: Wed Nov 29 10:37:28 2023

Stop observing sync service on shutdown in PasswordsPrivateDelegate

Bug: 1505176
Change-Id: If1fa60a92120afb7ce53278ceaa7d4fde180bf8a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5070554
Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org>
Commit-Queue: Viktor Semeniuk <vsemeniuk@google.com>
Cr-Commit-Position: refs/heads/main@{#1230542}

[modify] https://crrev.com/fe6b4163351f503045b83bffd870d18da622a865/chrome/browser/extensions/api/passwords_private/passwords_private_delegate_impl.h
[modify] https://crrev.com/fe6b4163351f503045b83bffd870d18da622a865/chrome/browser/extensions/api/passwords_private/passwords_private_delegate_impl.cc


### 18...@gmail.com (2023-12-02)

hey, could this bug marked as fixed(closed)?

### gi...@appspot.gserviceaccount.com (2023-12-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c1046c5d203e87b8a90bbf0bfd8d14d888e8ccb6

commit c1046c5d203e87b8a90bbf0bfd8d14d888e8ccb6
Author: Viktor Semeniuk <vsemeniuk@google.com>
Date: Mon Dec 04 10:20:30 2023

Cancel authentication when PasswordsPrivateDelegate is destroyed

This CL prevents retaining scoped_ptr when triggering authentication.
When the tab containing PasswordsPrivateDelegate is closed, any ongoing
authentication is automatically canceled.

Fixed: 1505176
Change-Id: I66c85e2a08ff0559a288173fc528405723643e88
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5070036
Reviewed-by: Mohamed Amir Yosef <mamir@chromium.org>
Commit-Queue: Viktor Semeniuk <vsemeniuk@google.com>
Cr-Commit-Position: refs/heads/main@{#1232623}

[modify] https://crrev.com/c1046c5d203e87b8a90bbf0bfd8d14d888e8ccb6/chrome/browser/extensions/api/passwords_private/passwords_private_delegate_impl.h
[modify] https://crrev.com/c1046c5d203e87b8a90bbf0bfd8d14d888e8ccb6/chrome/browser/extensions/api/passwords_private/passwords_private_delegate_impl.cc
[modify] https://crrev.com/c1046c5d203e87b8a90bbf0bfd8d14d888e8ccb6/chrome/browser/extensions/api/passwords_private/passwords_private_delegate_impl_unittest.cc


### [Deleted User] (2023-12-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-04)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### am...@google.com (2024-01-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-01-11)

Congratulations! The Chrome VRP Panel has decided to award you $1,000 for this report of a very highly mitigated security bug, mitigated by BRP protection and the significant user interactions and preconditions to trigger this issue. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2024-01-12)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-22)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-23)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-23)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-23)

This issue was migrated from crbug.com/chromium/1505176?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### pe...@google.com (2024-03-26)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



### pe...@google.com (2024-03-26)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



### rz...@google.com (2024-03-26)

1. <https://crrev.com/c/5356566> and <https://crrev.com/c/5356417/1>
2. Medium, the conflicts are simple but the changed class doesn't inherit syncer::SyncServiceObserver in 114 and 120, and one of the CLs was dropped
3. 121
4. No, a significant amount of the code needed to be dropped

### pe...@google.com (2024-04-09)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



### va...@chromium.org (2024-04-09)

rzanoni@, why are you merging this old bug into an ancient Chrome release?

### rz...@google.com (2024-04-09)

@vasilii I assume you mean M114; it was an active ChromeOS LTS milestone until a week ago and in my comment I'm recommending *not* to merge the CLs

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40945774)*
