# UAF in in extensions::ExtensionURLLoaderThrottle::WillProcessResponse

| Field | Value |
|-------|-------|
| **Issue ID** | [414760982](https://issues.chromium.org/issues/414760982) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools>Extensions, Platform>Extensions>API |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2025-04-30 |
| **Bounty** | $2,000.00 |

## Description

VULNERABILITY DETAILS

The UAF crash occurs in the extensions::ExtensionURLLoaderThrottle::WillProcessResponse function.
The issue happens when an extension uses the Debugger API to attach to a tab while the tab is processing a URL request.
The root cause is in how the ExtensionThrottleManager is managed during the lifecycle of throttle providers and URL loaders.

VERSION
Chromium	138.0.7153.0 (Developer Build) (64-bit) 
OS	Windows 11 Version 24H2 (Build 26120.3941)

Also reprodeced in Linux/ChromiumOS_Linux

REPRODUCTION CASE
1. run the command:
chrome.exe --user-data-dir=c:/tmp/test--no-sandbox --load-extension="extension" https://example.com

The test environment needs to access external network resources


FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [tab, browser, etc.]

=================================================================
==37512==ERROR: AddressSanitizer: heap-use-after-free on address 0x116457cb42c0 at pc 0x7ffbd24435a2 bp 0x0001043fbea0 sp 0x0001043fbee8
READ of size 1 at 0x116457cb42c0 thread T4
    #0 0x7ffbd24435a1 in base::internal::`anonymous namespace'::CrashImmediatelyOnUseAfterFree C:\b\s\w\ir\cache\builder\src\base\memory\raw_ptr_asan_hooks.cc:54:17
    #1 0x7ffbd24430f1 in base::internal::`anonymous namespace'::SafelyUnwrapForDereference C:\b\s\w\ir\cache\builder\src\base\memory\raw_ptr_asan_hooks.cc:77:5
    #2 0x7ffbd06251d6 in base::internal::RawPtrHookableImpl<1>::SafelyUnwrapPtrForDereference C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\pointers\raw_ptr_hookable_impl.h:84
    #3 0x7ffbd06251d6 in base::raw_ptr<extensions::ExtensionThrottleManager,0>::GetForDereference C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\pointers\raw_ptr.h:996
    #4 0x7ffbd06251d6 in base::raw_ptr<extensions::ExtensionThrottleManager,0>::operator-> C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\pointers\raw_ptr.h:665
    #5 0x7ffbd06251d6 in extensions::ExtensionURLLoaderThrottle::WillProcessResponse(class GURL const &, class network::mojom::URLResponseHead *, bool *) C:\b\s\w\ir\cache\builder\src\extensions\renderer\extension_url_loader_throttle.cc:51:3
    #6 0x7ffbc3d930fb in blink::ThrottlingURLLoader::OnReceiveResponse(class mojo::StructPtr<class network::mojom::URLResponseHead>, class mojo::ScopedHandleBase<class mojo::DataPipeConsumerHandle>, class std::__Cr::optional<class mojo_base::BigBuffer>) C:\b\s\w\ir\cache\builder\src\third_party\blink\common\loader\throttling_url_loader.cc:666:17
    #7 0x7ffbc0ddb911 in network::mojom::URLLoaderClientStubDispatch::Accept(class network::mojom::URLLoaderClient *, class mojo::Message *) C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\services\network\public\mojom\url_loader.mojom.cc:1127:13
    #8 0x7ffbd204e05f in mojo::InterfaceEndpointClient::HandleValidatedMessage(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:1059:54
    #9 0x7ffbd204ae5a in mojo::MessageDispatcher::Accept(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43:19
    #10 0x7ffbd20542ee in mojo::InterfaceEndpointClient::HandleIncomingMessage(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:731:20
    #11 0x7ffbd20361e0 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(class mojo::internal::MultiplexRouter::MessageWrapper *, enum mojo::internal::MultiplexRouter::ClientCallBehavior, class base::SequencedTaskRunner *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1120:42
    #12 0x7ffbd2034804 in mojo::internal::MultiplexRouter::Accept(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:733:7
    #13 0x7ffbd204ae5a in mojo::MessageDispatcher::Accept(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43:19
    #14 0x7ffbd2072414 in mojo::Connector::DispatchMessageW(class mojo::ScopedHandleBase<class mojo::MessageHandle>) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:561:49
    #15 0x7ffbd2073d20 in mojo::Connector::ReadAllAvailableMessages(void) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:619:14
    #16 0x7ffbd2073747 in mojo::Connector::OnHandleReadyInternal C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:450
    #17 0x7ffbd2073747 in mojo::Connector::OnWatcherHandleReady(char const *, unsigned int) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:416:3
    #18 0x7ffbd2075693 in base::internal::DecayedFunctorTraits<void (Connector::*)(const char *, unsigned int),mojo::Connector *,const char *const &>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:731
    #19 0x7ffbd2075693 in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (Connector::*const &)(const char *, unsigned int),mojo::Connector *,const char *const &>,void,0,1>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:923
    #20 0x7ffbd2075693 in base::internal::Invoker<base::internal::FunctorTraits<void (Connector::*const &)(const char *, unsigned int),mojo::Connector *,const char *const &>,base::internal::BindState<1,1,0,void (Connector::*)(const char *, unsigned int),base::internal::UnretainedWrapper<mojo::Connector,base::unretained_traits::MayNotDangle,0>,base::internal::UnretainedWrapper<const char,base::unretained_traits::MayNotDangle,0> >,void (unsigned int)>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1060
    #21 0x7ffbd2075693 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl mojo::Connector::*const &)(char const *, unsigned int), class mojo::Connector *, char const *const &>, struct base::internal::BindState<1, 1, 0, void (__cdecl mojo::Connector::*)(char const *, unsigned int), class base::internal::UnretainedWrapper<class mojo::Connector, struct base::unretained_traits::MayNotDangle, 0>, class base::internal::UnretainedWrapper<char const, struct base::unretained_traits::MayNotDangle, 0>>, (unsigned int)>::Run(class base::internal::BindStateBase *, unsigned int) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980:12
    #22 0x7ffbc3d855fc in base::RepeatingCallback<(unsigned int)>::Run(unsigned int) const & C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:344:12
    #23 0x7ffbc3d853ef in base::internal::DecayedFunctorTraits<void (*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),const base::RepeatingCallback<void (unsigned int)> &>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:664
    #24 0x7ffbc3d853ef in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),const base::RepeatingCallback<void (unsigned int)> &>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:923
    #25 0x7ffbc3d853ef in base::internal::Invoker<base::internal::FunctorTraits<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),const base::RepeatingCallback<void (unsigned int)> &>,base::internal::BindState<0,1,0,void (*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo::HandleSignalsState &)>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1060
    #26 0x7ffbc3d853ef in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl *const &)(class base::RepeatingCallback<(unsigned int)> const &, unsigned int, struct mojo::HandleSignalsState const &), class base::RepeatingCallback<void __cdecl(unsigned int)> const &>, struct base::internal::BindState<0, 1, 0, void (__cdecl *)(class base::RepeatingCallback<(unsigned int)> const &, unsigned int, struct mojo::HandleSignalsState const &), class base::RepeatingCallback<void __cdecl(unsigned int)>>, (unsigned int, struct mojo::HandleSignalsState const &)>::Run(class base::internal::BindStateBase *, unsigned int, struct mojo::HandleSignalsState const &) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980:12
    #27 0x7ffbd281a14b in base::RepeatingCallback<(unsigned int, struct mojo::HandleSignalsState const &)>::Run(unsigned int, struct mojo::HandleSignalsState const &) const & C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:344:12
    #28 0x7ffbd2819a55 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, struct mojo::HandleSignalsState const &) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc:278:14
    #29 0x7ffbd281ac68 in base::internal::DecayedFunctorTraits<void (SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher> &&,int &&,unsigned int &&,mojo::HandleSignalsState &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:731
    #30 0x7ffbd281ac68 in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (SimpleWatcher::*&&)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher> &&,int &&,unsigned int &&,mojo::HandleSignalsState &&>,void,0,1,2,3>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:947
    #31 0x7ffbd281ac68 in base::internal::Invoker<base::internal::FunctorTraits<void (SimpleWatcher::*&&)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher> &&,int &&,unsigned int &&,mojo::HandleSignalsState &&>,base::internal::BindState<1,1,0,void (SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher>,int,unsigned int,mojo::HandleSignalsState>,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1060
    #32 0x7ffbd281ac68 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl mojo::SimpleWatcher::*&&)(int, unsigned int, struct mojo::HandleSignalsState const &), class base::WeakPtr<class mojo::SimpleWatcher> &&, int &&, unsigned int &&, struct mojo::HandleSignalsState &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl mojo::SimpleWatcher::*)(int, unsigned int, struct mojo::HandleSignalsState const &), class base::WeakPtr<class mojo::SimpleWatcher>, int, unsigned int, struct mojo::HandleSignalsState>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:973:12
    #33 0x7ffbd23025d3 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
    #34 0x7ffbd23025d3 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:209:34
    #35 0x7ffbd225728c in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:106
    #36 0x7ffbd225728c in base::internal::TaskTracker::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:691
    #37 0x7ffbd225728c in base::internal::TaskTracker::RunSkipOnShutdown(struct base::internal::Task &, class base::TaskTraits const &, class base::internal::TaskSource *, class base::internal::SequenceToken const &) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:676:3
    #38 0x7ffbd225589a in base::internal::TaskTracker::RunTaskWithShutdownBehavior C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:706
    #39 0x7ffbd225589a in base::internal::TaskTracker::RunTask(struct base::internal::Task, class base::internal::TaskSource *, class base::TaskTraits const &) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:504:5
    #40 0x7ffbd225494e in base::internal::TaskTracker::RunAndPopNextTask(class base::internal::RegisteredTaskSource) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:394:5
    #41 0x7ffbd223df85 in base::internal::WorkerThread::RunWorker(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:473:36
    #42 0x7ffbd223cd9f in base::internal::WorkerThread::RunPooledWorker(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:359:3
    #43 0x7ffbd214b9f3 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:114:13
    #44 0x7ffc78de9a6c  (C:\chromium_version\latest_asan\clang_rt.asan_dynamic-x86_64.dll+0x180059a6c)
    #45 0x7ffccde7e8d6  (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #46 0x7ffccee51d1b  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180011d1b)

0x116457cb42c0 is located 0 bytes inside of 200-byte region [0x116457cb42c0,0x116457cb4388)
freed by thread T4 here:
    #0 0x7ffc78deae74  (C:\chromium_version\latest_asan\clang_rt.asan_dynamic-x86_64.dll+0x18005ae74)
    #1 0x7ffbd0624c20 in extensions::ExtensionThrottleManager::`scalar deleting dtor'(unsigned int) C:\b\s\w\ir\cache\builder\src\extensions\renderer\extension_throttle_manager.cc:33:55
    #2 0x7ffbe85fcc6c in std::__Cr::default_delete<extensions::ExtensionThrottleManager>::operator() C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:76
    #3 0x7ffbe85fcc6c in std::__Cr::unique_ptr<extensions::ExtensionThrottleManager,std::__Cr::default_delete<extensions::ExtensionThrottleManager> >::reset C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:287
    #4 0x7ffbe85fcc6c in std::__Cr::unique_ptr<extensions::ExtensionThrottleManager,std::__Cr::default_delete<extensions::ExtensionThrottleManager> >::~unique_ptr C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:256
    #5 0x7ffbe85fcc6c in URLLoaderThrottleProviderImpl::~URLLoaderThrottleProviderImpl(void) C:\b\s\w\ir\cache\builder\src\chrome\renderer\url_loader_throttle_provider_impl.cc:152:1
    #6 0x7ffbe85ff82f in URLLoaderThrottleProviderImpl::`scalar deleting dtor'(unsigned int) C:\b\s\w\ir\cache\builder\src\chrome\renderer\url_loader_throttle_provider_impl.cc:150:65
    #7 0x7ffbd2285cb7 in base::internal::DecayedFunctorTraits<void (*)(const void *),const void *&&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:664
    #8 0x7ffbd2285cb7 in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (*&&)(const void *),const void *&&>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:923
    #9 0x7ffbd2285cb7 in base::internal::Invoker<base::internal::FunctorTraits<void (*&&)(const void *),const void *&&>,base::internal::BindState<0,1,0,void (*)(const void *),base::internal::UnretainedWrapper<const void,base::unretained_traits::MayNotDangle,0> >,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1060
    #10 0x7ffbd2285cb7 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl *&&)(void const *), void const *&&>, struct base::internal::BindState<0, 1, 0, void (__cdecl *)(void const *), class base::internal::UnretainedWrapper<void const, struct base::unretained_traits::MayNotDangle, 0>>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:973:12
    #11 0x7ffbd23025d3 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
    #12 0x7ffbd23025d3 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:209:34
    #13 0x7ffbd225728c in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:106
    #14 0x7ffbd225728c in base::internal::TaskTracker::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:691
    #15 0x7ffbd225728c in base::internal::TaskTracker::RunSkipOnShutdown(struct base::internal::Task &, class base::TaskTraits const &, class base::internal::TaskSource *, class base::internal::SequenceToken const &) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:676:3
    #16 0x7ffbd225589a in base::internal::TaskTracker::RunTaskWithShutdownBehavior C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:706
    #17 0x7ffbd225589a in base::internal::TaskTracker::RunTask(struct base::internal::Task, class base::internal::TaskSource *, class base::TaskTraits const &) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:504:5
    #18 0x7ffbd225494e in base::internal::TaskTracker::RunAndPopNextTask(class base::internal::RegisteredTaskSource) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:394:5
    #19 0x7ffbd223df85 in base::internal::WorkerThread::RunWorker(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:473:36
    #20 0x7ffbd223cd9f in base::internal::WorkerThread::RunPooledWorker(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:359:3
    #21 0x7ffbd214b9f3 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:114:13
    #22 0x7ffc78de9a6c  (C:\chromium_version\latest_asan\clang_rt.asan_dynamic-x86_64.dll+0x180059a6c)
    #23 0x7ffccde7e8d6  (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #24 0x7ffccee51d1b  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180011d1b)

previously allocated by thread T4 here:
    #0 0x7ffc78dea28d  (C:\chromium_version\latest_asan\clang_rt.asan_dynamic-x86_64.dll+0x18005a28d)
    #1 0x7ffbe85fe4ca in std::__Cr::make_unique C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:754
    #2 0x7ffbe85fe4ca in `anonymous namespace'::CreateExtensionThrottleManager C:\b\s\w\ir\cache\builder\src\chrome\renderer\url_loader_throttle_provider_impl.cc:64
    #3 0x7ffbe85fe4ca in URLLoaderThrottleProviderImpl::CreateThrottles(class base::optional_ref<class base::TokenType<class blink::LocalFrameTokenTypeMarker> const>, struct network::ResourceRequest const &) C:\b\s\w\ir\cache\builder\src\chrome\renderer\url_loader_throttle_provider_impl.cc:241:35
    #4 0x7ffbcdf784c2 in blink::BackgroundURLLoader::Context::StartOnBackground(class scoped_refptr<class blink::WebBackgroundResourceFetchAssets>, class std::__Cr::unique_ptr<struct network::ResourceRequest, struct std::__Cr::default_delete<struct network::ResourceRequest>>, class url::Origin const &, bool, class WTF::Vector<class WTF::String, 0, class WTF::PartitionAllocator> const &, class std::__Cr::unique_ptr<class blink::ResourceLoadInfoNotifierWrapper, struct std::__Cr::default_delete<class blink::ResourceLoadInfoNotifierWrapper>>, bool, class std::__Cr::unique_ptr<class blink::BackgroundResponseProcessorFactory, struct std::__Cr::default_delete<class blink::BackgroundResponseProcessorFactory>>) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\loader\fetch\url_loader\background_url_loader.cc:423:30
    #5 0x7ffbcdf79950 in base::internal::DecayedFunctorTraits<void (Context::*)(scoped_refptr<blink::WebBackgroundResourceFetchAssets>, std::__Cr::unique_ptr<network::ResourceRequest,std::__Cr::default_delete<network::ResourceRequest> >, const url::Origin &, bool, const WTF::Vector<WTF::String,0,WTF::PartitionAllocator> &, std::__Cr::unique_ptr<blink::ResourceLoadInfoNotifierWrapper,std::__Cr::default_delete<blink::ResourceLoadInfoNotifierWrapper> >, bool, std::__Cr::unique_ptr<blink::BackgroundResponseProcessorFactory,std::__Cr::default_delete<blink::BackgroundResponseProcessorFactory> >),scoped_refptr<blink::BackgroundURLLoader::Context> &&,scoped_refptr<blink::WebBackgroundResourceFetchAssets> &&,std::__Cr::unique_ptr<network::ResourceRequest,std::__Cr::default_delete<network::ResourceRequest> > &&,url::Origin &&,bool &&,WTF::Vector<WTF::String,0,WTF::PartitionAllocator> &&,std::__Cr::unique_ptr<blink::ResourceLoadInfoNotifierWrapper,std::__Cr::default_delete<blink::ResourceLoadInfoNotifierWrapper> > &&,bool &&,std::__Cr::unique_ptr<blink::BackgroundResponseProcessorFactory,std::__Cr::default_delete<blink::BackgroundResponseProcessorFactory> > &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:731
    #6 0x7ffbcdf79950 in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (Context::*&&)(scoped_refptr<blink::WebBackgroundResourceFetchAssets>, std::__Cr::unique_ptr<network::ResourceRequest,std::__Cr::default_delete<network::ResourceRequest> >, const url::Origin &, bool, const WTF::Vector<WTF::String,0,WTF::PartitionAllocator> &, std::__Cr::unique_ptr<blink::ResourceLoadInfoNotifierWrapper,std::__Cr::default_delete<blink::ResourceLoadInfoNotifierWrapper> >, bool, std::__Cr::unique_ptr<blink::BackgroundResponseProcessorFactory,std::__Cr::default_delete<blink::BackgroundResponseProcessorFactory> >),scoped_refptr<blink::BackgroundURLLoader::Context> &&,scoped_refptr<blink::WebBackgroundResourceFetchAssets> &&,std::__Cr::unique_ptr<network::ResourceRequest,std::__Cr::default_delete<network::ResourceRequest> > &&,url::Origin &&,bool &&,WTF::Vector<WTF::String,0,WTF::PartitionAllocator> &&,std::__Cr::unique_ptr<blink::ResourceLoadInfoNotifierWrapper,std::__Cr::default_delete<blink::ResourceLoadInfoNotifierWrapper> > &&,bool &&,std::__Cr::unique_ptr<blink::BackgroundResponseProcessorFactory,std::__Cr::default_delete<blink::BackgroundResponseProcessorFactory> > &&>,void,0,1,2,3,4,5,6,7,8>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:923
    #7 0x7ffbcdf79950 in base::internal::Invoker<base::internal::FunctorTraits<void (Context::*&&)(scoped_refptr<blink::WebBackgroundResourceFetchAssets>, std::__Cr::unique_ptr<network::ResourceRequest,std::__Cr::default_delete<network::ResourceRequest> >, const url::Origin &, bool, const WTF::Vector<WTF::String,0,WTF::PartitionAllocator> &, std::__Cr::unique_ptr<blink::ResourceLoadInfoNotifierWrapper,std::__Cr::default_delete<blink::ResourceLoadInfoNotifierWrapper> >, bool, std::__Cr::unique_ptr<blink::BackgroundResponseProcessorFactory,std::__Cr::default_delete<blink::BackgroundResponseProcessorFactory> >),scoped_refptr<blink::BackgroundURLLoader::Context> &&,scoped_refptr<blink::WebBackgroundResourceFetchAssets> &&,std::__Cr::unique_ptr<network::ResourceRequest,std::__Cr::default_delete<network::ResourceRequest> > &&,url::Origin &&,bool &&,WTF::Vector<WTF::String,0,WTF::PartitionAllocator> &&,std::__Cr::unique_ptr<blink::ResourceLoadInfoNotifierWrapper,std::__Cr::default_delete<blink::ResourceLoadInfoNotifierWrapper> > &&,bool &&,std::__Cr::unique_ptr<blink::BackgroundResponseProcessorFactory,std::__Cr::default_delete<blink::BackgroundResponseProcessorFactory> > &&>,base::internal::BindState<1,1,0,void (Context::*)(scoped_refptr<blink::WebBackgroundResourceFetchAssets>, std::__Cr::unique_ptr<network::ResourceRequest,std::__Cr::default_delete<network::ResourceRequest> >, const url::Origin &, bool, const WTF::Vector<WTF::String,0,WTF::PartitionAllocator> &, std::__Cr::unique_ptr<blink::ResourceLoadInfoNotifierWrapper,std::__Cr::default_delete<blink::ResourceLoadInfoNotifierWrapper> >, bool, std::__Cr::unique_ptr<blink::BackgroundResponseProcessorFactory,std::__Cr::default_delete<blink::BackgroundResponseProcessorFactory> >),scoped_refptr<blink::BackgroundURLLoader::Context>,scoped_refptr<blink::WebBackgroundResourceFetchAssets>,std::__Cr::unique_ptr<network::ResourceRequest,std::__Cr::default_delete<network::ResourceRequest> >,url::Origin,bool,WTF::Vector<WTF::String,0,WTF::PartitionAllocator>,std::__Cr::unique_ptr<blink::ResourceLoadInfoNotifierWrapper,std::__Cr::default_delete<blink::ResourceLoadInfoNotifierWrapper> >,bool,std::__Cr::unique_ptr<blink::BackgroundResponseProcessorFactory,std::__Cr::default_delete<blink::BackgroundResponseProcessorFactory> > >,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1060
    #8 0x7ffbcdf79950 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl blink::BackgroundURLLoader::Context::*&&)(class scoped_refptr<class blink::WebBackgroundResourceFetchAssets>, class std::__Cr::unique_ptr<struct network::ResourceRequest, struct std::__Cr::default_delete<struct network::ResourceRequest>>, class url::Origin const &, bool, class WTF::Vector<class WTF::String, 0, class WTF::PartitionAllocator> const &, class std::__Cr::unique_ptr<class blink::ResourceLoadInfoNotifierWrapper, struct std::__Cr::default_delete<class blink::ResourceLoadInfoNotifierWrapper>>, bool, class std::__Cr::unique_ptr<class blink::BackgroundResponseProcessorFactory, struct std::__Cr::default_delete<class blink::BackgroundResponseProcessorFactory>>), class scoped_refptr<class blink::BackgroundURLLoader::Context> &&, class scoped_refptr<class blink::WebBackgroundResourceFetchAssets> &&, class std::__Cr::unique_ptr<struct network::ResourceRequest, struct std::__Cr::default_delete<struct network::ResourceRequest>> &&, class url::Origin &&, bool &&, class WTF::Vector<class WTF::String, 0, class WTF::PartitionAllocator> &&, class std::__Cr::unique_ptr<class blink::ResourceLoadInfoNotifierWrapper, struct std::__Cr::default_delete<class blink::ResourceLoadInfoNotifierWrapper>> &&, bool &&, class std::__Cr::unique_ptr<class blink::BackgroundResponseProcessorFactory, struct std::__Cr::default_delete<class blink::BackgroundResponseProcessorFactory>> &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl blink::BackgroundURLLoader::Context::*)(class scoped_refptr<class blink::WebBackgroundResourceFetchAssets>, class std::__Cr::unique_ptr<struct network::ResourceRequest, struct std::__Cr::default_delete<struct network::ResourceRequest>>, class url::Origin const &, bool, class WTF::Vector<class WTF::String, 0, class WTF::PartitionAllocator> const &, class std::__Cr::unique_ptr<class blink::ResourceLoadInfoNotifierWrapper, struct std::__Cr::default_delete<class blink::ResourceLoadInfoNotifierWrapper>>, bool, class std::__Cr::unique_ptr<class blink::BackgroundResponseProcessorFactory, struct std::__Cr::default_delete<class blink::BackgroundResponseProcessorFactory>>), class scoped_refptr<class blink::BackgroundURLLoader::Context>, class scoped_refptr<class blink::WebBackgroundResourceFetchAssets>, class std::__Cr::unique_ptr<struct network::ResourceRequest, struct std::__Cr::default_delete<struct network::ResourceRequest>>, class url::Origin, bool, class WTF::Vector<class WTF::String, 0, class WTF::PartitionAllocator>, class std::__Cr::unique_ptr<class blink::ResourceLoadInfoNotifierWrapper, struct std::__Cr::default_delete<class blink::ResourceLoadInfoNotifierWrapper>>, bool, class std::__Cr::unique_ptr<class blink::BackgroundResponseProcessorFactory, struct std::__Cr::default_delete<class blink::BackgroundResponseProcessorFactory>>>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:973:12
    #9 0x7ffbd23025d3 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
    #10 0x7ffbd23025d3 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:209:34
    #11 0x7ffbd225728c in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:106
    #12 0x7ffbd225728c in base::internal::TaskTracker::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:691
    #13 0x7ffbd225728c in base::internal::TaskTracker::RunSkipOnShutdown(struct base::internal::Task &, class base::TaskTraits const &, class base::internal::TaskSource *, class base::internal::SequenceToken const &) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:676:3
    #14 0x7ffbd225589a in base::internal::TaskTracker::RunTaskWithShutdownBehavior C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:706
    #15 0x7ffbd225589a in base::internal::TaskTracker::RunTask(struct base::internal::Task, class base::internal::TaskSource *, class base::TaskTraits const &) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:504:5
    #16 0x7ffbd225494e in base::internal::TaskTracker::RunAndPopNextTask(class base::internal::RegisteredTaskSource) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:394:5
    #17 0x7ffbd223df85 in base::internal::WorkerThread::RunWorker(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:473:36
    #18 0x7ffbd223cd9f in base::internal::WorkerThread::RunPooledWorker(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:359:3
    #19 0x7ffbd214b9f3 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:114:13
    #20 0x7ffc78de9a6c  (C:\chromium_version\latest_asan\clang_rt.asan_dynamic-x86_64.dll+0x180059a6c)
    #21 0x7ffccde7e8d6  (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #22 0x7ffccee51d1b  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180011d1b)

Thread T4 created by T0 here:
    #0 0x7ffc78de9982  (C:\chromium_version\latest_asan\clang_rt.asan_dynamic-x86_64.dll+0x180059982)
    #1 0x7ffbd214aaf9 in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:182:7
    #2 0x7ffbd223b37f in base::internal::WorkerThread::Start(class scoped_refptr<class base::SingleThreadTaskRunner>, class base::WorkerThreadObserver *) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:185:3
    #3 0x7ffbd224d076 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group.cc:89:13
    #4 0x7ffbd224cd5d in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group.cc:80:3
    #5 0x7ffbd22416f7 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::~ScopedCommandsExecutor C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group_impl.cc:42
    #6 0x7ffbd22416f7 in base::internal::ThreadGroupImpl::Start(unsigned __int64, unsigned __int64, class base::TimeDelta, class scoped_refptr<class base::SingleThreadTaskRunner>, class base::WorkerThreadObserver *, enum base::internal::ThreadGroup::WorkerEnvironment, bool, class std::__Cr::optional<class base::TimeDelta>) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group_impl.cc:249:3
    #7 0x7ffbd22318f2 in base::internal::ThreadPoolImpl::Start(struct base::ThreadPoolInstance::InitParams const &, class base::WorkerThreadObserver *) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_pool_impl.cc:196:35
    #8 0x7ffbdcc83600 in content::ChildProcess::ChildProcess(enum base::ThreadType, class std::__Cr::unique_ptr<struct base::ThreadPoolInstance::InitParams, struct std::__Cr::default_delete<struct base::ThreadPoolInstance::InitParams>>) C:\b\s\w\ir\cache\builder\src\content\child\child_process.h:117:38
    #9 0x7ffbe7dd0f38 in content::RenderProcess::RenderProcess(class std::__Cr::unique_ptr<struct base::ThreadPoolInstance::InitParams, struct std::__Cr::default_delete<struct base::ThreadPoolInstance::InitParams>>) C:\b\s\w\ir\cache\builder\src\content\renderer\render_process.cc:18:7
    #10 0x7ffbe7dd0601 in content::RenderProcessImpl::RenderProcessImpl(void) C:\b\s\w\ir\cache\builder\src\content\renderer\render_process_impl.cc:112:7
    #11 0x7ffbe7dd0bd5 in content::RenderProcessImpl::Create(void) C:\b\s\w\ir\cache\builder\src\content\renderer\render_process_impl.cc:227:31
    #12 0x7ffbe7cfeb1a in content::RendererMain(struct content::MainFunctionParams) C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:287:53
    #13 0x7ffbcedc7fe6 in content::RunOtherNamedProcessTypeMain(class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>> const &, struct content::MainFunctionParams, class content::ContentMainDelegate *) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:783:14
    #14 0x7ffbcedca381 in content::ContentMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1157:10
    #15 0x7ffbcedbe3f3 in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:359:36
    #16 0x7ffbcedbefad in content::ContentMain(struct content::ContentMainParams) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:372:10
    #17 0x7ffbbf632b0b in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:222:12
    #18 0x7ff693a047bb in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:201:12
    #19 0x7ff693a02021 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:352:20
    #20 0x7ff693eb896b in invoke_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #21 0x7ff693eb896b in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #22 0x7ffccde7e8d6  (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #23 0x7ffccee51d1b  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180011d1b)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\base\memory\raw_ptr_asan_hooks.cc:54:17 in base::internal::`anonymous namespace'::CrashImmediatelyOnUseAfterFree
Shadow bytes around the buggy address:
  0x116457cb4000: fa fa fa fa fa fa f7 fa 00 00 00 00 00 00 00 00
  0x116457cb4080: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x116457cb4100: 00 fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x116457cb4180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x116457cb4200: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
=>0x116457cb4280: fa fa fa fa fa fa f7 fa[fd]fd fd fd fd fd fd fd
  0x116457cb4300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x116457cb4380: fd fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x116457cb4400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x116457cb4480: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa
  0x116457cb4500: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
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

==37512==ADDITIONAL INFO

==37512==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffbd281a6f8 in mojo::SimpleWatcher::Context::Notify(unsigned int, struct MojoHandleSignalsState, unsigned int) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc:102:13


Command line: `"chrome.exe" --type=renderer --user-data-dir=c:/tmp/test --extension-process --no-pre-read-main-dll --no-sandbox --file-url-path-alias="/gen=C:\chromium_version\latest_asan\gen" --video-capture-use-gpu-memory-buffer --lang=zh-CN --device-scale-factor=1.75 --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=7 --time-ticks-at-unix-epoch=-1745603129273034 --launch-time-ticks=399984962880 --metrics-shmem-handle=3088,i,10853463304360795435,6088019744846484161,2097152 --field-trial-handle=1964,i,14414722279579164423,17627674527126514385,262144 --variations-seed-version --mojo-platform-channel-handle=4440 /prefetch:9`


MiraclePtr Status: MANUAL ANALYSIS REQUIRED
This crash occurred while a raw_ptr<T> object containing a dangling pointer was being dereferenced.
This crash occurred in the thread pool. The sequence which invoked the "free" is unknown, so the crash may have been caused by a race condition that is mislabeled as a use-after-free. Make sure that the "free" is sequenced after the "use" (e.g. both are on the same sequence, or the "free" is in a task posted after the "use"). Otherwise, the crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==37512==END OF ADDITIONAL INFO
==37512==ABORTING

## Attachments

- manifest.json (application/json, 585 B)
- icon.png (image/png, 429 B)
- poc.js (text/javascript, 550 B)
- poc.html (text/html, 170 B)

## Timeline

### ja...@chromium.org (2025-04-30)

I tried reproducing this on Linux but was not successful.

Bug reporter, how many times did you need to run the proof of concept (poc) before triggering the race condition?
Is there anything you can change in the poc to make the condition trigger more reliably?

The bug looks plausible so I'll add some people to take another look and maybe they can reproduce it.

### pe...@google.com (2025-04-30)

The issue's primary component must be in the Component Tags, so re-adding it. To change the primary component, use the edit button at the top of the issue, just above the title.

### ja...@chromium.org (2025-04-30)

I'm tentatively assigning this Medium severity (S2) as it requires a [specific extension to be installed](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md#toc-medium-severity), in this case one that calls the debug API and succeeds at triggering the race condition.

### ja...@chromium.org (2025-04-30)

Hi, solomonkinard@, can you take a look at this bug and verify the issue? I was unsuccessful reproducing it, but maybe I was missing something in setup.

### ja...@chromium.org (2025-04-30)

I'll provisionally set the found in to extended stable (136).

### 0x...@gmail.com (2025-04-30)

I apologize, there was a missing space in the command line. After loading the extension's page, it immediately triggers a UAF crash.
>  chrome.exe --user-data-dir=c:/tmp/test --no-sandbox --load-extension="extension"

The extension page will visit the external network resources, so it needs an accessible network connection.

### pe...@google.com (2025-04-30)

Thank you for providing more feedback. Adding the requester to the CC list.

### ch...@google.com (2025-05-01)

Setting milestone because of s2 severity.

### ch...@google.com (2025-05-01)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@google.com (2025-05-15)

solomonkinard: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### so...@chromium.org (2025-05-22)

Looking.

### ch...@google.com (2025-06-06)

solomonkinard: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-06-21)

solomonkinard: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-07-06)

solomonkinard: Uh oh! This issue still open and hasn't been updated in the last 44 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2025-07-09)

Project: chromium/src  

Branch: main  

Author: Solomon Kinard [solomonkinard@chromium.org](mailto:solomonkinard@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6651042>

Extensions: ExtensionThrottleManager: Observe dependency destruction

---


Expand for full commit details
```
     
    ExtensionURLLoaderThrottle relies on ExtensionThrottleManager because 
    they’re created at the same time when throttles have one manager in 
    common, but they’re managed independently so the manager can go away 
    without the throttles being aware. 
     
    Doc: 
    https://docs.google.com/document/d/1JXFBNF6-Nl6H6AjZGjALE_2UnMhCnSmKXPC4mAzZtpI/edit?usp=sharing 
     
    Bug: chromium:414760982, chromium:377724744 
    Change-Id: If53fe5f7c8a6fb197d67be3b9afacf8329e97697 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6651042 
    Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
    Commit-Queue: Solomon Kinard <solomonkinard@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1484094}

```

---

Files:

- M `extensions/renderer/extension_throttle_manager.cc`
- M `extensions/renderer/extension_throttle_manager.h`
- M `extensions/renderer/extension_throttle_unittest.cc`
- M `extensions/renderer/extension_url_loader_throttle.cc`
- M `extensions/renderer/extension_url_loader_throttle.h`

---

Hash: 0882dbc4a6dc52eb4ca80e6e6f50ff1897fc4a42  

Date:  Wed Jul 9 00:50:59 2025


---

### ch...@google.com (2025-07-09)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2025-07-15)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2025-07-15)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: andywu (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### so...@chromium.org (2025-07-15)

- Why does your merge fit within the merge criteria for these milestones? Security bug.
- Chrome Browser: Milestone: 139. Chromium: 7258.
- What changes specifically would you like to merge? [crrev.com/c/6651042](https://crrev.com/c/6651042)
- Have the changes been released and tested on canary? Yes.
- If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? No.

### pg...@google.com (2025-07-17)

This fix has been in canary for quite a while. I do not see any issues in canary that seem related to this change -

merge approved for M139! please merge to branch 7258 at your earliest convenience to get this into the next beta release!

### dx...@google.com (2025-07-17)

Project: chromium/src  

Branch:  refs/branch-heads/7258  

Author:  Solomon Kinard [solomonkinard@chromium.org](mailto:solomonkinard@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6765865>

Extensions: ExtensionThrottleManager: Observe dependency destruction

---


Expand for full commit details
```
     
    ExtensionURLLoaderThrottle relies on ExtensionThrottleManager because 
    they’re created at the same time when throttles have one manager in 
    common, but they’re managed independently so the manager can go away 
    without the throttles being aware. 
     
    Doc: 
    https://docs.google.com/document/d/1JXFBNF6-Nl6H6AjZGjALE_2UnMhCnSmKXPC4mAzZtpI/edit?usp=sharing 
     
    (cherry picked from commit 0882dbc4a6dc52eb4ca80e6e6f50ff1897fc4a42) 
     
    Bug: chromium:414760982, chromium:377724744 
    Change-Id: If53fe5f7c8a6fb197d67be3b9afacf8329e97697 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6651042 
    Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
    Commit-Queue: Solomon Kinard <solomonkinard@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1484094} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6765865 
    Cr-Commit-Position: refs/branch-heads/7258@{#1511} 
    Cr-Branched-From: f600d0656fd5b5fe4a82981f533d31ed6939e2e4-refs/heads/main@{#1477651}

```

---

Files:

- M `extensions/renderer/extension_throttle_manager.cc`
- M `extensions/renderer/extension_throttle_manager.h`
- M `extensions/renderer/extension_throttle_unittest.cc`
- M `extensions/renderer/extension_url_loader_throttle.cc`
- M `extensions/renderer/extension_url_loader_throttle.h`

---

Hash: [49f4948c1a2df0e9529da2a5edf1d3429508c45c](http://crrev.com/49f4948c1a2df0e9529da2a5edf1d3429508c45c)  

Date: Thu Jul 17 20:27:33 2025


---

### pe...@google.com (2025-07-17)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### so...@chromium.org (2025-07-17)

1. Most likely yes. [crbug.com/377724744](https://crbug.com/377724744) was opened on 2024-11-07 without a specific chrome version listed. The m132 [LTS](https://chromiumdash.appspot.com/schedule) release was 2025-04-08 and m126 on 2024-07-16.
2. Most likely no. [crrev.com/c/1157524](https://crrev.com/c/1157524) merged in m70.

### pe...@google.com (2025-07-21)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-07-21)

1. <https://chromium-review.googlesource.com/c/chromium/src/+/6774101>
2. Low - There was a conflict.
3. 139
4. Yes. According to the [comment #24](https://issues.chromium.org/issues/414760982#comment24). The issue was opened on 2024-11-07. So, M132 has likely the bug.

### sp...@google.com (2025-07-24)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
report of moderately mitigated memory corruption in a sandboxed process / renderer


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-07-24)

Thank you for your efforts and reporting this issue to us.

### rz...@google.com (2025-09-16)

@gm...@google.com requesting merge for 138, the bot didn't add the questionnaire, but answers below:

1 <https://chromium-review.googlesource.com/c/chromium/src/+/6939210>

2 Low, no conflicts

3 139

4 Yes

### dx...@google.com (2025-09-18)

Project: chromium/src  

Branch:  refs/branch-heads/6834  

Author:  Solomon Kinard [solomonkinard@chromium.org](mailto:solomonkinard@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6774101>

[M132-LTS] Extensions: ExtensionThrottleManager: Observe dependency destruction

---


Expand for full commit details
```
     
    ExtensionURLLoaderThrottle relies on ExtensionThrottleManager because 
    they’re created at the same time when throttles have one manager in 
    common, but they’re managed independently so the manager can go away 
    without the throttles being aware. 
     
    Doc: 
    https://docs.google.com/document/d/1JXFBNF6-Nl6H6AjZGjALE_2UnMhCnSmKXPC4mAzZtpI/edit?usp=sharing 
     
    (cherry picked from commit 0882dbc4a6dc52eb4ca80e6e6f50ff1897fc4a42) 
     
    Bug: chromium:414760982, chromium:377724744 
    Change-Id: If53fe5f7c8a6fb197d67be3b9afacf8329e97697 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6651042 
    Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
    Commit-Queue: Solomon Kinard <solomonkinard@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1484094} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6774101 
    Commit-Queue: Reilly Grant <reillyg@chromium.org> 
    Reviewed-by: James Cook <jamescook@chromium.org> 
    Reviewed-by: Emilia Paz <emiliapaz@chromium.org> 
    Reviewed-by: Solomon Kinard <solomonkinard@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/6834@{#5646} 
    Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```

---

Files:

- M `extensions/renderer/extension_throttle_manager.cc`
- M `extensions/renderer/extension_throttle_manager.h`
- M `extensions/renderer/extension_throttle_unittest.cc`
- M `extensions/renderer/extension_url_loader_throttle.cc`
- M `extensions/renderer/extension_url_loader_throttle.h`

---

Hash: [07e0912ae67118ca01cef66735e67e8d0308a9a9](https://chromiumdash.appspot.com/commit/07e0912ae67118ca01cef66735e67e8d0308a9a9)  

Date: Thu Sep 18 22:13:07 2025


---

### dx...@google.com (2025-09-25)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Solomon Kinard [solomonkinard@chromium.org](mailto:solomonkinard@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6939210>

[M138-LTS] Extensions: ExtensionThrottleManager: Observe dependency destruction

---


Expand for full commit details
```
     
    ExtensionURLLoaderThrottle relies on ExtensionThrottleManager because 
    they’re created at the same time when throttles have one manager in 
    common, but they’re managed independently so the manager can go away 
    without the throttles being aware. 
     
    Doc: 
    https://docs.google.com/document/d/1JXFBNF6-Nl6H6AjZGjALE_2UnMhCnSmKXPC4mAzZtpI/edit?usp=sharing 
     
    (cherry picked from commit 0882dbc4a6dc52eb4ca80e6e6f50ff1897fc4a42) 
     
    Bug: chromium:414760982, chromium:377724744 
    Change-Id: If53fe5f7c8a6fb197d67be3b9afacf8329e97697 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6651042 
    Commit-Queue: Solomon Kinard <solomonkinard@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1484094} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6939210 
    Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com> 
    Reviewed-by: Giovanni Pezzino <giovax@google.com> 
    Reviewed-by: Solomon Kinard <solomonkinard@chromium.org> 
    Reviewed-by: James Cook <jamescook@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3414} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `extensions/renderer/extension_throttle_manager.cc`
- M `extensions/renderer/extension_throttle_manager.h`
- M `extensions/renderer/extension_throttle_unittest.cc`
- M `extensions/renderer/extension_url_loader_throttle.cc`
- M `extensions/renderer/extension_url_loader_throttle.h`

---

Hash: [930232e83e284e4d7b92c63d5f59c51dab18c8cc](https://chromiumdash.appspot.com/commit/930232e83e284e4d7b92c63d5f59c51dab18c8cc)  

Date: Thu Sep 25 18:45:35 2025


---

### dx...@google.com (2025-09-29)

Project: chromium/src  

Branch:  refs/branch-heads/7204\_184  

Author:  Solomon Kinard [solomonkinard@chromium.org](mailto:solomonkinard@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6991552>

[M138-LTS] Extensions: ExtensionThrottleManager: Observe dependency destruction

---


Expand for full commit details
```
     
    ExtensionURLLoaderThrottle relies on ExtensionThrottleManager because 
    they’re created at the same time when throttles have one manager in 
    common, but they’re managed independently so the manager can go away 
    without the throttles being aware. 
     
    Doc: 
    https://docs.google.com/document/d/1JXFBNF6-Nl6H6AjZGjALE_2UnMhCnSmKXPC4mAzZtpI/edit?usp=sharing 
     
    (cherry picked from commit 0882dbc4a6dc52eb4ca80e6e6f50ff1897fc4a42) 
     
    (cherry picked from commit 930232e83e284e4d7b92c63d5f59c51dab18c8cc) 
     
    Bug: chromium:414760982, chromium:377724744 
    Change-Id: If53fe5f7c8a6fb197d67be3b9afacf8329e97697 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6651042 
    Commit-Queue: Solomon Kinard <solomonkinard@chromium.org> 
    Cr-Original-Original-Commit-Position: refs/heads/main@{#1484094} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6939210 
    Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com> 
    Reviewed-by: Giovanni Pezzino <giovax@google.com> 
    Reviewed-by: Solomon Kinard <solomonkinard@chromium.org> 
    Reviewed-by: James Cook <jamescook@chromium.org> 
    Cr-Original-Commit-Position: refs/branch-heads/7204@{#3414} 
    Cr-Original-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6991552 
    Owners-Override: Kyle Williams <kdgwill@chromium.org> 
    Auto-Submit: Kyle Williams <kdgwill@chromium.org> 
    Reviewed-by: Niko Tsirakis <ntsirakis@google.com> 
    Commit-Queue: Kyle Williams <kdgwill@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7204_184@{#61} 
    Cr-Branched-From: 7ea839044480a944888296dc0cccc5afb60b736c-refs/branch-heads/7204@{#2436} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `extensions/renderer/extension_throttle_manager.cc`
- M `extensions/renderer/extension_throttle_manager.h`
- M `extensions/renderer/extension_throttle_unittest.cc`
- M `extensions/renderer/extension_url_loader_throttle.cc`
- M `extensions/renderer/extension_url_loader_throttle.h`

---

Hash: [c6708b6c4cbc39994593cea32e8b522bd0a363ce](https://chromiumdash.appspot.com/commit/c6708b6c4cbc39994593cea32e8b522bd0a363ce)  

Date: Mon Sep 29 19:03:36 2025


---

### ch...@google.com (2025-10-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of moderately mitigated memory corruption in a sandboxed process / renderer

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/414760982)*
