# AddressSanitizer: heap-use-after-free asan-linux-release-960248 content::StoragePartitionImpl::GetLockManager() content/browser/storage_partition_impl.cc:1493

| Field | Value |
|-------|-------|
| **Issue ID** | [40058517](https://issues.chromium.org/issues/40058517) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>Core |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | wa...@chromium.org |
| **Created** | 2022-01-18 |
| **Bounty** | $15,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4761.0 Safari/537.36

Steps to reproduce the problem:
#Reproduce
This is found by my fuzzer running on ClusterFuzz, but it cannot be reproduced stably so ClusterFuzz does not automatically open a case.
https://clusterfuzz.com/testcase-detail/6269252247814144 (may require the security team to set permissions)

What is the expected behavior?

What went wrong?
Type of crash
browser process(may cause the sandbox escape)

#Analysis

1. RenderProcessHost has a raw pointer to StoragePartitionImpl object[1]
2. StoragePartitionImplMap is owner of StoragePartitionImpl[2] and will be freed when ProfileImpl get freed
3. At this time, if RenderProcessHost access StoragePartitionImpl ptr, it will lead to UAF
```
// static
RenderProcessHost* RenderProcessHostImpl::CreateRenderProcessHost(
    BrowserContext* browser_context,
    SiteInstanceImpl* site_instance) {
  if (g_render_process_host_factory_) {
    return g_render_process_host_factory_->CreateRenderProcessHost(
        browser_context, site_instance);
  }

  StoragePartitionImpl* storage_partition_impl =		<<[1]
      static_cast<StoragePartitionImpl*>(
          browser_context->GetStoragePartition(site_instance));
__CUT__

  return new RenderProcessHostImpl(browser_context, storage_partition_impl,
                                   flags);
}

[2]
previously allocated by thread T0 (chrome) here:
    #0 0x5591a70a0add in operator new(unsigned long) third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x5591ad23a0bb in content::StoragePartitionImpl::Create(content::BrowserContext*, content::StoragePartitionConfig const&, base::FilePath const&) content/browser/storage_partition_impl.cc:1154:27
    #2 0x5591ad26eb71 in content::StoragePartitionImplMap::Get(content::StoragePartitionConfig const&, bool) content/browser/storage_partition_impl_map.cc:347:7
    #3 0x5591ac066b9a in GetStoragePartition content/browser/browser_context.cc:137:52
    #4 0x5591ac066b9a in content::BrowserContext::GetDefaultStoragePartition() content/browser/browser_context.cc:180:10
[3]
freed by thread T0 (chrome) here:
    #0 0x5591a70a133d in operator delete(void*) third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
..cut..
    #7 0x5591ad26e667 in ~__tree buildtools/third_party/libc++/trunk/include/__tree:1789:3
    #8 0x5591ad26e667 in ~map buildtools/third_party/libc++/trunk/include/map:1103:5
    #9 0x5591ad26e667 in ~StoragePartitionImplMap content/browser/storage_partition_impl_map.cc:324:1
    #10 0x5591ad26e667 in content::StoragePartitionImplMap::~StoragePartitionImplMap() content/browser/storage_partition_impl_map.cc:323:53
    #11 0x5591b4a1d951 in ProfileImpl::~ProfileImpl() chrome/browser/profiles/profile_impl.cc:925:3
    #12 0x5591b4a1e02d in ProfileImpl::~ProfileImpl() chrome/browser/profiles/profile_impl.cc:860:29

```

#Patch
Not yet

#asan
=================================================================
==213227==ERROR: AddressSanitizer: heap-use-after-free on address 0x61b0000dcaf8 at pc 0x5591ad240a15 bp 0x7ffd118062c0 sp 0x7ffd118062b8
READ of size 8 at 0x61b0000dcaf8 thread T0 (chrome)
SCARINESS: 51 (8-byte-read-heap-use-after-free)
    #0 0x5591ad240a14 in get buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:288:19
    #1 0x5591ad240a14 in content::StoragePartitionImpl::GetLockManager() content/browser/storage_partition_impl.cc:1493:24
    #2 0x5591aceaca3c in content::RenderProcessHostImpl::CreateLockManagerWithBucketInfo(mojo::PendingReceiver<blink::mojom::LockManager>, storage::QuotaErrorOr<storage::BucketInfo>) content/browser/renderer_host/render_process_host_impl.cc:2093:28
    #3 0x5591acee28d8 in void base::internal::FunctorTraits<void (content::RenderProcessHostImpl::*)(mojo::PendingReceiver<blink::mojom::LockManager>, storage::QuotaErrorOr<storage::BucketInfo>), void>::Invoke<void (content::RenderProcessHostImpl::*)(mojo::PendingReceiver<blink::mojom::LockManager>, storage::QuotaErrorOr<storage::BucketInfo>), base::WeakPtr<content::RenderProcessHostImpl>, mojo::PendingReceiver<blink::mojom::LockManager>, storage::QuotaErrorOr<storage::BucketInfo> >(void (content::RenderProcessHostImpl::*)(mojo::PendingReceiver<blink::mojom::LockManager>, storage::QuotaErrorOr<storage::BucketInfo>), base::WeakPtr<content::RenderProcessHostImpl>&&, mojo::PendingReceiver<blink::mojom::LockManager>&&, storage::QuotaErrorOr<storage::BucketInfo>&&) base/bind_internal.h:535:12
    #4 0x5591bd7eb65d in Run base/callback.h:142:12
    #5 0x5591bd7eb65d in Invoke<base::OnceCallback<void (storage::QuotaErrorOr<storage::BucketInfo>)>, storage::QuotaErrorOr<storage::BucketInfo> > base/bind_internal.h:634:49
    #6 0x5591bd7eb65d in MakeItSo<base::OnceCallback<void (storage::QuotaErrorOr<storage::BucketInfo>)>, storage::QuotaErrorOr<storage::BucketInfo> > base/bind_internal.h:699:12
    #7 0x5591bd7eb65d in RunImpl<base::OnceCallback<void (storage::QuotaErrorOr<storage::BucketInfo>)>, std::__1::tuple<storage::QuotaErrorOr<storage::BucketInfo> >, 0UL> base/bind_internal.h:772:12
    #8 0x5591bd7eb65d in base::internal::Invoker<base::internal::BindState<base::OnceCallback<void (storage::QuotaErrorOr<storage::BucketInfo>)>, storage::QuotaErrorOr<storage::BucketInfo> >, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:741:12
    #9 0x5591b5565e13 in Run base/callback.h:142:12
    #10 0x5591b5565e13 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:135:32
    #11 0x5591b55a7bd3 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:358:29)> base/task/common/task_annotator.h:74:5
    #12 0x5591b55a7bd3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356:21
    #13 0x5591b55a73e7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261:30
    #14 0x5591b55a87a1 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0
    #15 0x5591b545f4e9 in HandleDispatch base/message_loop/message_pump_glib.cc:376:46
    #16 0x5591b545f4e9 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:126:43
    #17 0x7f6486e27196 in g_main_context_dispatch
0x61b0000dcaf8 is located 248 bytes inside of 1280-byte region [0x61b0000dca00,0x61b0000dcf00)
freed by thread T0 (chrome) here:
    #0 0x5591a70a133d in operator delete(void*) third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x5591ad2742ce in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #2 0x5591ad2742ce in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #3 0x5591ad2742ce in ~unique_ptr buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:269:19
    #4 0x5591ad2742ce in ~pair buildtools/third_party/libc++/trunk/include/utility:394:29
    #5 0x5591ad2742ce in destroy<std::__1::pair<const content::StoragePartitionConfig, std::__1::unique_ptr<content::StoragePartitionImpl, std::__1::default_delete<content::StoragePartitionImpl> > >, void, void> buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:318:15
    #6 0x5591ad2742ce in std::__1::__tree<std::__1::__value_type<content::StoragePartitionConfig, std::__1::unique_ptr<content::StoragePartitionImpl, std::__1::default_delete<content::StoragePartitionImpl> > >, std::__1::__map_value_compare<content::StoragePartitionConfig, std::__1::__value_type<content::StoragePartitionConfig, std::__1::unique_ptr<content::StoragePartitionImpl, std::__1::default_delete<content::StoragePartitionImpl> > >, std::__1::less<content::StoragePartitionConfig>, true>, std::__1::allocator<std::__1::__value_type<content::StoragePartitionConfig, std::__1::unique_ptr<content::StoragePartitionImpl, std::__1::default_delete<content::StoragePartitionImpl> > > > >::destroy(std::__1::__tree_node<std::__1::__value_type<content::StoragePartitionConfig, std::__1::unique_ptr<content::StoragePartitionImpl, std::__1::default_delete<content::StoragePartitionImpl> > >, void*>*) buildtools/third_party/libc++/trunk/include/__tree:1801:9
    #7 0x5591ad26e667 in ~__tree buildtools/third_party/libc++/trunk/include/__tree:1789:3
    #8 0x5591ad26e667 in ~map buildtools/third_party/libc++/trunk/include/map:1103:5
    #9 0x5591ad26e667 in ~StoragePartitionImplMap content/browser/storage_partition_impl_map.cc:324:1
    #10 0x5591ad26e667 in content::StoragePartitionImplMap::~StoragePartitionImplMap() content/browser/storage_partition_impl_map.cc:323:53
    #11 0x5591b4a1d951 in ProfileImpl::~ProfileImpl() chrome/browser/profiles/profile_impl.cc:925:3
    #12 0x5591b4a1e02d in ProfileImpl::~ProfileImpl() chrome/browser/profiles/profile_impl.cc:860:29
    #13 0x5591b4a25e6b in ProfileDestroyer::DestroyOriginalProfileNow(Profile*) chrome/browser/profiles/profile_destroyer.cc:133:3
    #14 0x5591b4a2536f in ProfileDestroyer::DestroyProfileWhenAppropriate(Profile*) chrome/browser/profiles/profile_destroyer.cc:61:5
    #15 0x5591b4a7804c in ProfileManager::ProfileInfo::~ProfileInfo() chrome/browser/profiles/profile_manager.cc:1683:3
    #16 0x5591b4a80c9e in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #17 0x5591b4a80c9e in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #18 0x5591b4a80c9e in ~unique_ptr buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:269:19
    #19 0x5591b4a80c9e in ~pair buildtools/third_party/libc++/trunk/include/utility:394:29
    #20 0x5591b4a80c9e in destroy<std::__1::pair<const base::FilePath, std::__1::unique_ptr<ProfileManager::ProfileInfo, std::__1::default_delete<ProfileManager::ProfileInfo> > >, void, void> buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:318:15
    #21 0x5591b4a80c9e in std::__1::__tree<std::__1::__value_type<base::FilePath, std::__1::unique_ptr<ProfileManager::ProfileInfo, std::__1::default_delete<ProfileManager::ProfileInfo> > >, std::__1::__map_value_compare<base::FilePath, std::__1::__value_type<base::FilePath, std::__1::unique_ptr<ProfileManager::ProfileInfo, std::__1::default_delete<ProfileManager::ProfileInfo> > >, std::__1::less<base::FilePath>, true>, std::__1::allocator<std::__1::__value_type<base::FilePath, std::__1::unique_ptr<ProfileManager::ProfileInfo, std::__1::default_delete<ProfileManager::ProfileInfo> > > > >::erase(std::__1::__tree_const_iterator<std::__1::__value_type<base::FilePath, std::__1::unique_ptr<ProfileManager::ProfileInfo, std::__1::default_delete<ProfileManager::ProfileInfo> > >, std::__1::__tree_node<std::__1::__value_type<base::FilePath, std::__1::unique_ptr<ProfileManager::ProfileInfo, std::__1::default_delete<ProfileManager::ProfileInfo> > >, void*>*, long>) buildtools/third_party/libc++/trunk/include/__tree:2422:5
    #22 0x5591b4a74f3d in __erase_unique<base::FilePath> buildtools/third_party/libc++/trunk/include/__tree:2445:5
    #23 0x5591b4a74f3d in erase buildtools/third_party/libc++/trunk/include/map:1317:25
    #24 0x5591b4a74f3d in ProfileManager::RemoveProfile(base::FilePath const&) chrome/browser/profiles/profile_manager.cc:1788:18
    #25 0x5591b4a74bb5 in ProfileManager::DeleteProfileIfNoKeepAlive(ProfileManager::ProfileInfo const*) chrome/browser/profiles/profile_manager.cc:1518:3
    #26 0x5591b4a744c3 in ProfileManager::RemoveKeepAlive(Profile const*, ProfileKeepAliveOrigin) chrome/browser/profiles/profile_manager.cc:1475:3
    #27 0x5591b5565e13 in Run base/callback.h:142:12
    #28 0x5591b5565e13 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:135:32
    #29 0x5591b55a7bd3 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:358:29)> base/task/common/task_annotator.h:74:5
    #30 0x5591b55a7bd3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356:21
    #31 0x5591b55a73e7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261:30
    #32 0x5591b55a87a1 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0
    #33 0x5591b545f4e9 in HandleDispatch base/message_loop/message_pump_glib.cc:376:46
    #34 0x5591b545f4e9 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:126:43
    #35 0x7f6486e27196 in g_main_context_dispatch
previously allocated by thread T0 (chrome) here:
    #0 0x5591a70a0add in operator new(unsigned long) third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x5591ad23a0bb in content::StoragePartitionImpl::Create(content::BrowserContext*, content::StoragePartitionConfig const&, base::FilePath const&) content/browser/storage_partition_impl.cc:1154:27
    #2 0x5591ad26eb71 in content::StoragePartitionImplMap::Get(content::StoragePartitionConfig const&, bool) content/browser/storage_partition_impl_map.cc:347:7
    #3 0x5591ac066b9a in GetStoragePartition content/browser/browser_context.cc:137:52
    #4 0x5591ac066b9a in content::BrowserContext::GetDefaultStoragePartition() content/browser/browser_context.cc:180:10
    #5 0x5591b47712fc in OptimizationGuideKeyedService::Initialize() chrome/browser/optimization_guide/optimization_guide_keyed_service.cc:135:35
    #6 0x5591b4770ff1 in OptimizationGuideKeyedServiceFactory::BuildServiceInstanceFor(content::BrowserContext*) const chrome/browser/optimization_guide/optimization_guide_keyed_service_factory.cc:59:14
    #7 0x5591b9ba131b in KeyedServiceFactory::GetServiceForContext(void*, bool) components/keyed_service/core/keyed_service_factory.cc:80:15
    #8 0x5591b9b9a3c7 in DependencyManager::CreateContextServices(void*, bool) components/keyed_service/core/dependency_manager.cc:0
    #9 0x5591bdc1aae3 in DoCreateBrowserContextServices components/keyed_service/content/browser_context_dependency_manager.cc:46:22
    #10 0x5591bdc1aae3 in BrowserContextDependencyManager::CreateBrowserContextServices(content::BrowserContext*) components/keyed_service/content/browser_context_dependency_manager.cc:31:3
    #11 0x5591b4a1fd61 in ProfileImpl::OnLocaleReady(Profile::CreateMode) chrome/browser/profiles/profile_impl.cc:1104:51
    #12 0x5591b4a18af6 in ProfileImpl::OnPrefsLoaded(Profile::CreateMode, bool) chrome/browser/profiles/profile_impl.cc:1145:3
    #13 0x5591b4a177ef in ProfileImpl::ProfileImpl(base::FilePath const&, Profile::Delegate*, Profile::CreateMode, base::Time, scoped_refptr<base::SequencedTaskRunner>) chrome/browser/profiles/profile_impl.cc:535:5
    #14 0x5591b4a14039 in Profile::CreateProfile(base::FilePath const&, Profile::Delegate*, Profile::CreateMode) chrome/browser/profiles/profile_impl.cc:366:59
    #15 0x5591b4a648c2 in ProfileManager::CreateAndInitializeProfile(base::FilePath const&) chrome/browser/profiles/profile_manager.cc:1826:38
    #16 0x5591b4a61827 in ProfileManager::GetProfile(base::FilePath const&) chrome/browser/profiles/profile_manager.cc:744:10
    #17 0x5591c00af156 in GetStartupProfile(base::FilePath const&, base::CommandLine const&) chrome/browser/ui/startup/startup_browser_creator.cc:1392:39
    #18 0x5591b45269da in (anonymous namespace)::CreatePrimaryProfile(content::MainFunctionParams const&, base::FilePath const&, base::CommandLine const&) chrome/browser/chrome_browser_main.cc:419:18
    #19 0x5591b4523ae5 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl() chrome/browser/chrome_browser_main.cc:1488:37
    #20 0x5591b4523044 in ChromeBrowserMainParts::PreMainMessageLoopRun() chrome/browser/chrome_browser_main.cc:1134:18
    #21 0x5591ac0e8359 in content::BrowserMainLoop::PreMainMessageLoopRun() content/browser/browser_main_loop.cc:978:28
    #22 0x5591ad2351d8 in Run base/callback.h:142:12
    #23 0x5591ad2351d8 in content::StartupTaskRunner::RunAllTasksNow() content/browser/startup_task_runner.cc:43:29
    #24 0x5591ac0e78fd in content::BrowserMainLoop::CreateStartupTasks() content/browser/browser_main_loop.cc:886:25
    #25 0x5591ac0ee04f in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams) content/browser/browser_main_runner_impl.cc:132:15
    #26 0x5591ac0e416e in content::BrowserMain(content::MainFunctionParams) content/browser/browser_main.cc:26:32
    #27 0x5591b4339230 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:646:10
    #28 0x5591b433c2ff in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1161:10
    #29 0x5591b433b3d2 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1027:12
    #30 0x5591b4333f2c in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:399:36
    #31 0x5591b4335b94 in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:427:10
    #32 0x5591a70a337e in ChromeMain chrome/app/chrome_main.cc:177:12
SUMMARY: AddressSanitizer: heap-use-after-free (/mnt/scratch0/clusterfuzz/bot/builds/chrome-test-builds_media_linux-release_eb660d5ee526c9c1c1608a71fcbe7a713c490533/revisions/asan-linux-release-960248/chrome+0x10b9da14) (BuildId: a660953fb73203c9)
Shadow bytes around the buggy address:
  0x0c3680013900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c3680013910: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c3680013920: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c3680013930: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c3680013940: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0c3680013950: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]
  0x0c3680013960: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3680013970: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3680013980: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3680013990: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c36800139a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:00
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
==213227==ABORTING

Did this work before? N/A 

Chrome version: 99.0.4761.0  Channel: n/a
OS Version: 10.0

## Attachments

- [clusterfuzz-testcase-6269252247814144.zip](attachments/clusterfuzz-testcase-6269252247814144.zip) (application/octet-stream, 65.5 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 17.7 KB)
- [rep.patch](attachments/rep.patch) (text/plain, 3.9 KB)
- [asan2.txt](attachments/asan2.txt) (text/plain, 16.6 KB)
- [2022-02-04 093224.png](attachments/2022-02-04 093224.png) (image/png, 133.4 KB)

## Timeline

### [Deleted User] (2022-01-18)

[Empty comment from Monorail migration]

### aj...@google.com (2022-01-19)

I'm not able to repro on Windows asan - is it possible this is a shutdown crash or that specific user interaction is required (I see a rtc share request come up?)

### aj...@google.com (2022-01-19)

[Empty comment from Monorail migration]

### aj...@google.com (2022-01-19)

Also no luck on linux. Are you using any specific flags?

### m....@gmail.com (2022-01-19)

POC does not stably reproduce the problem as the problem requires winning a race condition(CreateLockManagerWithBucketInfo is called after ~StoragePartitionImplMap).
I'm trying to patch some code to make the problem easier to reproduce.


### m....@gmail.com (2022-01-19)

re https://crbug.com/chromium/1288251#c04

#Reproduce
I have patched some code made a stably reproduce env,.

chrome --enable-logging=stderr --v=1 --ignore-gpu-blacklist --allow-file-access-from-files --disable-gesture-requirement-for-media-playback --disable-click-to-play --disable-hang-monitor --dns-prefetch-disable --disable-default-apps --disable-component-update --safebrowsing-disable-auto-update --metrics-recording-only --disable-gpu-watchdog --disable-metrics --disable-popup-blocking --disable-prompt-on-repost --enable-experimental-extension-apis --enable-extension-apps --force-internal-pdf --js-flags="--expose-gc --verify-heap" --new-window --no-default-browser-check --no-first-run --no-process-singleton-dialog --use-gl=angle --use-angle=swiftshader --enable-shadow-dom --enable-media-stream --enable-mp3-stream-parser --disable-in-process-stack-traces --user-data-dir=test --enable-logging=stdout fuzz-00817.html

#RCA
I guess the problem may be related to cross-thread posttask, I simulated the post from the IO thread in the patch and reproduced the problem stably.
From the log, we can find that GetLockManager will still be called after StoragePartitionImplMap is freed[2]
```
void QuotaManagerImpl::GetOrCreateBucket(
    const StorageKey& storage_key,
    const std::string& bucket_name,
    base::OnceCallback<void(QuotaErrorOr<BucketInfo>)> callback) {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
  EnsureDatabaseOpened();

  if (db_disabled_) {
    std::move(callback).Run(QuotaError::kDatabaseError);
    return;
  }
  PostTaskAndReplyWithResultForDBThread(		<<[1]
      base::BindOnce(&GetOrCreateBucketOnDBThread, storage_key, bucket_name),
      base::BindOnce(&QuotaManagerImpl::DidGetBucket,
                     weak_factory_.GetWeakPtr(), std::move(callback)));
}


[24448:18344:0119/185058.106:ERROR:render_process_host_impl.cc(2115)] [11000]StoragePartitionImpl::GetLockManager ->> this: 000012F532B96880
[24448:18344:0119/185058.106:ERROR:storage_partition_impl.cc(1494)] [11000]StoragePartitionImpl::GetLockManager ->> this: 000012F532B2D280
[24448:18344:0119/185058.110:ERROR:storage_partition_impl.cc(1494)] [11000]StoragePartitionImpl::GetLockManager ->> this: 000012F532B2D280
[24448:18344:0119/185058.762:ERROR:render_process_host_impl.cc(2115)] [11000]StoragePartitionImpl::GetLockManager ->> this: 000012F532B96880
[24448:18344:0119/185058.762:ERROR:storage_partition_impl.cc(1494)] [11000]StoragePartitionImpl::GetLockManager ->> this: 000012F532B2D280
[24448:18344:0119/185058.765:ERROR:render_process_host_impl.cc(2115)] [11000]StoragePartitionImpl::GetLockManager ->> this: 000012F532B96880
[24448:18344:0119/185058.766:ERROR:storage_partition_impl.cc(1494)] [11000]StoragePartitionImpl::GetLockManager ->> this: 000012F532B2D280
[24448:18344:0119/185058.767:ERROR:render_process_host_impl.cc(2115)] [11000]StoragePartitionImpl::GetLockManager ->> this: 000012F532B96880
[24448:18344:0119/185058.767:ERROR:storage_partition_impl.cc(1494)] [11000]StoragePartitionImpl::GetLockManager ->> this: 000012F532B2D280
[24448:18344:0119/185058.773:ERROR:render_process_host_impl.cc(2115)] [11000]StoragePartitionImpl::GetLockManager ->> this: 000012F532B96880
[24448:18344:0119/185058.774:ERROR:storage_partition_impl.cc(1494)] [11000]StoragePartitionImpl::GetLockManager ->> this: 000012F532B2D280
[24448:18344:0119/185058.774:ERROR:render_process_host_impl.cc(2115)] [11000]StoragePartitionImpl::GetLockManager ->> this: 000012F532B96880
[24448:18344:0119/185058.774:ERROR:storage_partition_impl.cc(1494)] [11000]StoragePartitionImpl::GetLockManager ->> this: 000012F532B2D280
[24448:18344:0119/185058.781:ERROR:render_process_host_impl.cc(2115)] [11000]StoragePartitionImpl::GetLockManager ->> this: 000012F532B96880
[24448:18344:0119/185058.781:ERROR:storage_partition_impl.cc(1494)] [11000]StoragePartitionImpl::GetLockManager ->> this: 000012F532B2D280
[24448:18344:0119/185058.903:ERROR:storage_partition_impl_map.cc(324)] [11000]StoragePartitionImplMap::~StoragePartitionImplMap ->> this: 000012CD32BB4880	 <<[2]
[24448:18344:0119/185058.934:ERROR:render_process_host_impl.cc(2115)] [11000]StoragePartitionImpl::GetLockManager ->> this: 000012F532B96880
[24448:18344:0119/185058.934:ERROR:storage_partition_impl.cc(1494)] [11000]StoragePartitionImpl::GetLockManager ->> this: 000012F532B2D280

```


### [Deleted User] (2022-01-19)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@google.com (2022-01-19)

ayui - please take a look at this uaf in the storage code (or assign to someone that can). I will continue trying to repro but in the meantime it might be good to have eyes on this. It is possible that a very recent change introduced this.

Please also see https://crbug.com/chromium/1288419 which is a duplicate report and has a good alternative poc.

Tentatively setting FoundIn-99 until I can repro in older versions or see what changed to cause this - please update if you have any extra info!
Sec=critical for a browser uaf from web contents.

[Monorail components: Blink>Storage>Quota]

### aj...@google.com (2022-01-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-19)

[Empty comment from Monorail migration]

### ay...@chromium.org (2022-01-19)

Hi jdh@, can you take a look? 
Looks like the issue is around CreateLockManagerWithBucketInfo added here https://crrev.com/c/3270364

### [Deleted User] (2022-01-19)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-19)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-19)

Setting Pri-0 to match security severity Critical. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wa...@chromium.org (2022-01-19)

If RenderProcessHostImpl has a raw pointer to StoragePartitionImpl and it can outlive the StoragePartitionImpl, then that is a bug in the RPHI architecture.  That raw pointer existed before jdh@ landed his CL.

That being said we can mitigate the problem here by binding a WeakPtr<StoragePartitionImpl> when we create the callback to the CreateLockManagerWithBucketInfo.

### wa...@chromium.org (2022-01-19)

CC nasko regarding the first issue in https://crbug.com/chromium/1288251#c15.  Not sure if there is someone who owns this setup in RPHI, but it seems like a bigger issue than what web locks is doing.

### wa...@chromium.org (2022-01-19)

I wonder if we should null out storage_partition_impl_ here:

https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_process_host_impl.cc;l=3996;drc=cc56431a98152461ad58cf220ea03f4098f7008c

Also, maybe we should explicitly call `weak_ptr_factory_.InvalidateWeakPtrs()` there as well.

### wa...@chromium.org (2022-01-19)

I made a CL for https://crbug.com/chromium/1288251#c17, but not sure if its correct or a complete fix for this issue.

https://chromium-review.googlesource.com/c/chromium/src/+/3402620

### go...@chromium.org (2022-01-19)

[Empty comment from Monorail migration]

### jd...@chromium.org (2022-01-20)

I made a CL for https://crbug.com/chromium/1288251#c15. However, if the CL wanderview@ mentioned lands, then I don't think it should be needed.

crrev.com/c/3402540

### wa...@chromium.org (2022-01-24)

Reviewer is out of office, so I asked for review from a new reviewer.  Sorry for the delay here.

### gi...@appspot.gserviceaccount.com (2022-01-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5c1a8da60506e80f9241c8ff6dd8736a9e340205

commit 5c1a8da60506e80f9241c8ff6dd8736a9e340205
Author: Ben Kelly <wanderview@chromium.org>
Date: Tue Jan 25 17:53:55 2022

WebLocks: Use RPHI.instance_weak_factory_ when getting quota bucket.

RenderProcessHostImpl has two different WeakPtrFactory members.  The
`instance_weak_factory_` gets invalidated whenever the renderer process
dies or the RPHI begins async destruction.  This is the correct
semantics for the WebLocks use case since we don't want to continue
binding the LockManager in either of these cases.

This CL also clears the storage_partition_impl_ raw pointer at the
start of deletion.  The async deletion means that the RPHI could outlive
the StoragePartitionImpl.

Finally, the CL moves the `instance_weak_factory_` to the end of the
member list for order-of-destruction safety and to make it easier for
readers to see that there are two different WeakPtrFactory objects.

Bug: 1288251
Change-Id: I4b5fa6662e5c044558301acb1cfaeed620972370
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3402620
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Commit-Queue: Ben Kelly <wanderview@chromium.org>
Cr-Commit-Position: refs/heads/main@{#963068}

[modify] https://crrev.com/5c1a8da60506e80f9241c8ff6dd8736a9e340205/content/browser/renderer_host/render_process_host_impl.cc
[modify] https://crrev.com/5c1a8da60506e80f9241c8ff6dd8736a9e340205/content/browser/renderer_host/render_process_host_impl.h


### wa...@chromium.org (2022-01-25)

Reporter, can you please attempt to reproduce with https://crbug.com/chromium/1288251#c22 commit?

### m....@gmail.com (2022-01-26)

Patch works fine.

=================================================================
==10120==ERROR: AddressSanitizer: access-violation on unknown address 0x000000000108 (pc 0x7ffce1f507e7 bp 0x00c69f9fc610 sp 0x00c69f9fc440 T0)
==10120==The signal is caused by a READ memory access.
==10120==Hint: address points to the zero page.
    #0 0x7ffce1f507e6 in content::StoragePartitionImpl::GetLockManager E:\v8\chro2\src\content\browser\storage_partition_impl.cc:1498
    #1 0x7ffce1c160ed in content::RenderProcessHostImpl::testlockptrui E:\v8\chro2\src\content\browser\renderer_host\render_process_host_impl.cc:2119
    #2 0x7ffd124df8a4 in base::TaskAnnotator::RunTaskImpl E:\v8\chro2\src\base\task\common\task_annotator.cc:135
    #3 0x7ffd1252ecbc in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl E:\v8\chro2\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:356
    #4 0x7ffd1252e3f2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork E:\v8\chro2\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:261
    #5 0x7ffd12626ba6 in base::MessagePumpForUI::DoRunLoop E:\v8\chro2\src\base\message_loop\message_pump_win.cc:220
    #6 0x7ffd12624678 in base::MessagePumpWin::Run E:\v8\chro2\src\base\message_loop\message_pump_win.cc:78
    #7 0x7ffd12530411 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run E:\v8\chro2\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:468
    #8 0x7ffd1242c943 in base::RunLoop::Run E:\v8\chro2\src\base\run_loop.cc:140
    #9 0x7ffce0edf21e in content::BrowserMainLoop::RunMainMessageLoop E:\v8\chro2\src\content\browser\browser_main_loop.cc:1048
    #10 0x7ffce0ee4d53 in content::BrowserMainRunnerImpl::Run E:\v8\chro2\src\content\browser\browser_main_runner_impl.cc:153
    #11 0x7ffce0ed8a1f in content::BrowserMain E:\v8\chro2\src\content\browser\browser_main.cc:30
    #12 0x7ffce2f5096e in content::RunBrowserProcessMain E:\v8\chro2\src\content\app\content_main_runner_impl.cc:646
    #13 0x7ffce2f53a2b in content::ContentMainRunnerImpl::RunBrowser E:\v8\chro2\src\content\app\content_main_runner_impl.cc:1160
    #14 0x7ffce2f52b8f in content::ContentMainRunnerImpl::Run E:\v8\chro2\src\content\app\content_main_runner_impl.cc:1026
    #15 0x7ffce2f4ea4f in content::RunContentProcess E:\v8\chro2\src\content\app\content_main.cc:399
    #16 0x7ffce2f4fb05 in content::ContentMain E:\v8\chro2\src\content\app\content_main.cc:427
    #17 0x7ffce5b614a5 in ChromeMain E:\v8\chro2\src\chrome\app\chrome_main.cc:177
    #18 0x7ff628d45554 in MainDllLoader::Launch E:\v8\chro2\src\chrome\app\main_dll_loader_win.cc:169
    #19 0x7ff628d42a02 in main E:\v8\chro2\src\chrome\app\chrome_exe_main_win.cc:382
    #20 0x7ff628f06fdb in __scrt_common_main_seh D:\a01\_work\9\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #21 0x7ffd63aa7033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)
    #22 0x7ffd64ec2650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: access-violation E:\v8\chro2\src\content\browser\storage_partition_impl.cc:1498 in content::StoragePartitionImpl::GetLockManager

### wa...@chromium.org (2022-01-26)

Thanks.  From the stack it appears you are testing via some code modifications, correct?  So I think that verifies that nulling the storage_partition_impl_ pointer works, but doesn't necessarily test the WeakPtr changes.  Ideally we would not run a callback after async destruction starts, but that may be harder to verify due to timing.

### wa...@chromium.org (2022-01-26)

[Empty comment from Monorail migration]

[Monorail components: -Blink>Storage>Quota Internals>Core]

### wa...@chromium.org (2022-01-26)

I'd like to merge https://crbug.com/chromium/1288251#c22 to M99.

### m....@gmail.com (2022-01-26)

re https://crbug.com/chromium/1288251#c25 correct.

### gi...@appspot.gserviceaccount.com (2022-01-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5202e7d0af95fc9fc82c5a29e11ba5755c91cda2

commit 5202e7d0af95fc9fc82c5a29e11ba5755c91cda2
Author: Ben Kelly <wanderview@chromium.org>
Date: Wed Jan 26 16:59:12 2022

WebLocks: Use RPHI.instance_weak_factory_ when getting quota bucket.

RenderProcessHostImpl has two different WeakPtrFactory members.  The
`instance_weak_factory_` gets invalidated whenever the renderer process
dies or the RPHI begins async destruction.  This is the correct
semantics for the WebLocks use case since we don't want to continue
binding the LockManager in either of these cases.

This CL also clears the storage_partition_impl_ raw pointer at the
start of deletion.  The async deletion means that the RPHI could outlive
the StoragePartitionImpl.

Finally, the CL moves the `instance_weak_factory_` to the end of the
member list for order-of-destruction safety and to make it easier for
readers to see that there are two different WeakPtrFactory objects.

(cherry picked from commit 5c1a8da60506e80f9241c8ff6dd8736a9e340205)

Bug: 1288251
Change-Id: I4b5fa6662e5c044558301acb1cfaeed620972370
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3402620
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Commit-Queue: Ben Kelly <wanderview@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#963068}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3417491
Cr-Commit-Position: refs/branch-heads/4844@{#58}
Cr-Branched-From: 007241ce2e6c8e5a7b306cc36c730cd07cd38825-refs/heads/main@{#961656}

[modify] https://crrev.com/5202e7d0af95fc9fc82c5a29e11ba5755c91cda2/content/browser/renderer_host/render_process_host_impl.cc
[modify] https://crrev.com/5202e7d0af95fc9fc82c5a29e11ba5755c91cda2/content/browser/renderer_host/render_process_host_impl.h


### [Deleted User] (2022-01-26)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-26)

Merge approved: your change passed merge requirements and is auto-approved for M99. Please go ahead and merge the CL to branch 4844 (refs/branch-heads/4844) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: benmason (Android), harrysouders (iOS), cindyb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-26)

[Empty comment from Monorail migration]

### wa...@chromium.org (2022-01-26)

Sorry, I think I mistakenly merged this before the approval label got added.  I think I must have gotten confused by an email for a different bug.

### gm...@google.com (2022-01-26)

ajgo@google.com were you able to reproduce in earlier builds. For now I will assume this doesn't apply to 96.

### aj...@google.com (2022-01-26)

gmpritchard: did not attempt.
wanderview: could you provide some indication of when this bug might have been introduced?

### wa...@chromium.org (2022-01-26)

It was introduced in M99 in:

https://chromiumdash.appspot.com/commit/ec5eaba0e021b757d5cbbf2c27ac8f06809d81e9

### aj...@google.com (2022-01-26)

Great, FoundIn-99 it is then!

### be...@google.com (2022-01-26)

[Bulk edit] Please merge to M99, branch 4844 ASAP so this can go out with this week's dev release.

### pb...@google.com (2022-01-27)

Your change has been approved for M99 branch 4844,please go ahead and merge the CL's manually asap so that they would be part of tomorrow's M99 Dev release.

### pb...@google.com (2022-01-27)

The change was merged to M99 Branch  in https://crbug.com/chromium/1288251#c29, hence dropping Merge approvals labels. The merged happened a hour before Sheriff bot approval.

### am...@google.com (2022-02-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-04)

[Comment Deleted]

### am...@chromium.org (2022-02-04)

Congratulations, 0x74960! The VRP Panel has decided to award you $15,000 for this report. If you can point us to the fuzzer report or show evidence of this fuzzer being run on ClusterFuzz, we would be happy to boost this by $1,000 for the Fuzzer Bonus that is customary for valid reports from fuzzing. Thank you for this report and your fuzzing contributions! 

### m....@gmail.com (2022-02-04)

RE https://crbug.com/chromium/1288251#c44
Thanks,because cl cannot be reproduced stably, the testcase has been deleted, but some information can still be found in the history, see screenshot.
I made some suggestions to cl, like let's keep the key testcase manually or be able to link to crbug, but no reply.
I still have a few issues in the same situation, because I haven't related to crbug in time, cl has deleted the testcase, I don't know who should I ask to associate cl testcase to crbug


### am...@chromium.org (2022-02-04)

Thanks for this info. I'll poke around and take a look in ClusterFuzz to try and find it before I run push the button to send the reward decisions to finance tomorrow. 

### am...@google.com (2022-02-04)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-02-12)

re https://crbug.com/chromium/1288251#c46 Can i get  Fuzzer Bonus for this one~

### am...@chromium.org (2022-02-14)

Sorry, we could track this report down anywhere on clusterfuzz unfortunately. The fuzzer bonus is rewarded when your fuzzer running on ClusterFuzz automatically produces the report complete with test case, data from reproduction, such as symbolized stack trace and mitigating the need for a lot of security and developer time to reproduce and hunt for relevant data. 

### [Deleted User] (2022-05-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-06-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ea0c3779fd0b20021d095809305cb2ed325a1da4

commit ea0c3779fd0b20021d095809305cb2ed325a1da4
Author: Sharon Yang <yangsharon@chromium.org>
Date: Thu Jun 16 19:50:28 2022

Rename weak_ptr_factory_ in RenderProcessHostImpl

Make clear that weak_ptr_factory_ should exclusively be used for
creating SafeRefs by renaming it and updating comments. Because of how
RenderProcessHostImpl gets cleaned up and destructed, it's important for most use cases to use instance_weak_factory_ to avoid UaF and dangling pointers.
This change preserves the intent of https://crrev.com/963512 for
https://crbug.com/1288251.

Bug: 1294045, 1288251
Change-Id: I667a9037347448a0646ad781ac7c81a45c7955fc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3707558
Reviewed-by: Charlie Reis <creis@chromium.org>
Commit-Queue: Sharon Yang <yangsharon@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1015060}

[modify] https://crrev.com/ea0c3779fd0b20021d095809305cb2ed325a1da4/content/browser/renderer_host/render_process_host_impl.cc
[modify] https://crrev.com/ea0c3779fd0b20021d095809305cb2ed325a1da4/content/browser/renderer_host/render_process_host_impl.h


### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1288251?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1288419]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058517)*
