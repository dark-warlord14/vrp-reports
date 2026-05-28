# UAF in safe_browsing::RendererURLLoaderThrottle::WillRedirectRequest due to Mojo Remote being freed during resource load lifecycle

| Field | Value |
|-------|-------|
| **Issue ID** | [447192722](https://issues.chromium.org/issues/447192722) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Services (Use Subcomponents)>Safebrowsing |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2025-09-25 |
| **Bounty** | $7,000.00 |

## Description


VULNERABILITY DETAILS
A UAF condition was detected in the renderer process within the Safe Browsing URL loading throttle mechanism. This vulnerability occurs when a resource load that triggers the safe_browsing::RendererURLLoaderThrottle is redirected, and a race condition is won against the tear-down of the associated renderer context.
The crash occurs when safe_browsing::RendererURLLoaderThrottle::WillRedirectRequest attempts to dereference a raw_ptr to safe_browsing::mojom::ExtensionWebRequestReporter, which has been freed shortly beforehand as part of the URLLoaderThrottleProviderImpl destruction.

When the injected contentjs fetch the 307 Temporary Redirect url(in content.js) cause the UAF.

VERSION
Chrome Version: 142.0.7433.0 (Developer Build) (64-bit) 
Operating System: Windows 10 Version 22H2 (Build 19045.6332)

REPRODUCTION CASE
1. run the command:
./chrome.exe --user-data-dir=C:/tmp/test --no-sandbox --no-first-run  --load-extension="extension_dir" https://example.com https://example.com https://example.com 

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [tab]
==4664==ERROR: AddressSanitizer: heap-use-after-free on address 0x118c5a3b78f0 at pc 0x7ffd9d2b61bf bp 0x005380ffe380 sp 0x005380ffe3c8
READ of size 1 at 0x118c5a3b78f0 thread T5
    #0 0x7ffd9d2b61be in base::internal::`anonymous namespace'::CrashImmediatelyOnUseAfterFree C:\b\s\w\ir\cache\builder\src\base\memory\raw_ptr_asan_hooks.cc:54:17
    #1 0x7ffd9d2b5d11 in base::internal::`anonymous namespace'::SafelyUnwrapForDereference C:\b\s\w\ir\cache\builder\src\base\memory\raw_ptr_asan_hooks.cc:77:5
    #2 0x7ffd9a5192b5 in base::internal::RawPtrHookableImpl<1>::SafelyUnwrapPtrForDereference C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\pointers\raw_ptr_hookable_impl.h:84
    #3 0x7ffd9a5192b5 in base::raw_ptr<safe_browsing::mojom::ExtensionWebRequestReporter,1>::GetForDereference C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\pointers\raw_ptr.h:1019
    #4 0x7ffd9a5192b5 in base::raw_ptr<safe_browsing::mojom::ExtensionWebRequestReporter,1>::operator-> C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\pointers\raw_ptr.h:665
    #5 0x7ffd9a5192b5 in safe_browsing::RendererURLLoaderThrottle::WillRedirectRequest(struct net::RedirectInfo *, class network::mojom::URLResponseHead const &, bool *, class std::__Cr::vector<class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>>, class std::__Cr::allocator<class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>>>> *, class net::HttpRequestHeaders *, class net::HttpRequestHeaders *) C:\b\s\w\ir\cache\builder\src\components\safe_browsing\content\renderer\renderer_url_loader_throttle.cc:120:5
    #6 0x7ffd8d82021b in blink::ThrottlingURLLoader::OnReceiveRedirect(struct net::RedirectInfo const &, class mojo::StructPtr<class network::mojom::URLResponseHead>) C:\b\s\w\ir\cache\builder\src\third_party\blink\common\loader\throttling_url_loader.cc:767:17
    #7 0x7ffd8abbff74 in network::mojom::URLLoaderClientStubDispatch::Accept(class network::mojom::URLLoaderClient *, class mojo::Message *) C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\services\network\public\mojom\url_loader.mojom.cc:1191:13
    #8 0x7ffd9cebadb4 in mojo::InterfaceEndpointClient::HandleValidatedMessage(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:1060:54
    #9 0x7ffd9ceb7b2a in mojo::MessageDispatcher::Accept(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43:19
    #10 0x7ffd9cec147e in mojo::InterfaceEndpointClient::HandleIncomingMessage(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:731:20
    #11 0x7ffd9cea2b1f in mojo::internal::MultiplexRouter::ProcessIncomingMessage(class mojo::internal::MultiplexRouter::MessageWrapper *, enum mojo::internal::MultiplexRouter::ClientCallBehavior, class base::SequencedTaskRunner *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1164:42
    #12 0x7ffd9cea109c in mojo::internal::MultiplexRouter::Accept(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:767:7
    #13 0x7ffd9ceb7b2a in mojo::MessageDispatcher::Accept(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43:19
    #14 0x7ffd9cedfa38 in mojo::Connector::DispatchMessageW(class mojo::ScopedHandleBase<class mojo::MessageHandle>) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:561:49
    #15 0x7ffd9cee1380 in mojo::Connector::ReadAllAvailableMessages(void) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:619:14
    #16 0x7ffd9cee0da7 in mojo::Connector::OnHandleReadyInternal C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:450
    #17 0x7ffd9cee0da7 in mojo::Connector::OnWatcherHandleReady(char const *, unsigned int) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:416:3
    #18 0x7ffd9cee2d23 in base::internal::DecayedFunctorTraits<void (mojo::Connector::*)(const char *, unsigned int),mojo::Connector *,const char *const &>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:730
    #19 0x7ffd9cee2d23 in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (mojo::Connector::*const &)(const char *, unsigned int),mojo::Connector *,const char *const &>,void,0,1>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:922
    #20 0x7ffd9cee2d23 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::*const &)(const char *, unsigned int),mojo::Connector *,const char *const &>,base::internal::BindState<1,1,0,void (mojo::Connector::*)(const char *, unsigned int),base::internal::UnretainedWrapper<mojo::Connector,base::unretained_traits::MayNotDangle,0>,base::internal::UnretainedWrapper<const char,base::unretained_traits::MayNotDangle,0> >,void (unsigned int)>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1059
    #21 0x7ffd9cee2d23 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl mojo::Connector::*const &)(char const *, unsigned int), class mojo::Connector *, char const *const &>, struct base::internal::BindState<1, 1, 0, void (__cdecl mojo::Connector::*)(char const *, unsigned int), class base::internal::UnretainedWrapper<class mojo::Connector, struct base::unretained_traits::MayNotDangle, 0>, class base::internal::UnretainedWrapper<char const, struct base::unretained_traits::MayNotDangle, 0>>, (unsigned int)>::Run(class base::internal::BindStateBase *, unsigned int) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:979:12
    #22 0x7ffd8d81047c in base::RepeatingCallback<(unsigned int)>::Run(unsigned int) const & C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:343:12
    #23 0x7ffd8d81026f in base::internal::DecayedFunctorTraits<void (*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),const base::RepeatingCallback<void (unsigned int)> &>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:663
    #24 0x7ffd8d81026f in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),const base::RepeatingCallback<void (unsigned int)> &>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:922
    #25 0x7ffd8d81026f in base::internal::Invoker<base::internal::FunctorTraits<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),const base::RepeatingCallback<void (unsigned int)> &>,base::internal::BindState<0,1,0,void (*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo::HandleSignalsState &)>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1059
    #26 0x7ffd8d81026f in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl *const &)(class base::RepeatingCallback<(unsigned int)> const &, unsigned int, struct mojo::HandleSignalsState const &), class base::RepeatingCallback<void __cdecl(unsigned int)> const &>, struct base::internal::BindState<0, 1, 0, void (__cdecl *)(class base::RepeatingCallback<(unsigned int)> const &, unsigned int, struct mojo::HandleSignalsState const &), class base::RepeatingCallback<void __cdecl(unsigned int)>>, (unsigned int, struct mojo::HandleSignalsState const &)>::Run(class base::internal::BindStateBase *, unsigned int, struct mojo::HandleSignalsState const &) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:979:12
    #27 0x7ffd9d6a06fb in base::RepeatingCallback<(unsigned int, struct mojo::HandleSignalsState const &)>::Run(unsigned int, struct mojo::HandleSignalsState const &) const & C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:343:12
    #28 0x7ffd9d69fff5 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, struct mojo::HandleSignalsState const &) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc:278:14
    #29 0x7ffd9d6a11d8 in base::internal::DecayedFunctorTraits<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher> &&,int &&,unsigned int &&,mojo::HandleSignalsState &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:730
    #30 0x7ffd9d6a11d8 in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher> &&,int &&,unsigned int &&,mojo::HandleSignalsState &&>,void,0,1,2,3>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:946
    #31 0x7ffd9d6a11d8 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher> &&,int &&,unsigned int &&,mojo::HandleSignalsState &&>,base::internal::BindState<1,1,0,void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher>,int,unsigned int,mojo::HandleSignalsState>,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1059
    #32 0x7ffd9d6a11d8 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl mojo::SimpleWatcher::*&&)(int, unsigned int, struct mojo::HandleSignalsState const &), class base::WeakPtr<class mojo::SimpleWatcher> &&, int &&, unsigned int &&, struct mojo::HandleSignalsState &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl mojo::SimpleWatcher::*)(int, unsigned int, struct mojo::HandleSignalsState const &), class base::WeakPtr<class mojo::SimpleWatcher>, int, unsigned int, struct mojo::HandleSignalsState>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:972:12
    #33 0x7ffd9d171033 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:155
    #34 0x7ffd9d171033 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:207:34
    #35 0x7ffd9d0c611c in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:104
    #36 0x7ffd9d0c611c in base::internal::TaskTracker::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:686
    #37 0x7ffd9d0c611c in base::internal::TaskTracker::RunSkipOnShutdown(struct base::internal::Task &, class base::TaskTraits const &, class base::internal::TaskSource *, class base::internal::SequenceToken const &) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:671:3
    #38 0x7ffd9d0c475a in base::internal::TaskTracker::RunTaskWithShutdownBehavior C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:701
    #39 0x7ffd9d0c475a in base::internal::TaskTracker::RunTask(struct base::internal::Task, class base::internal::TaskSource *, class base::TaskTraits const &) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:501:5
    #40 0x7ffd9d0c382e in base::internal::TaskTracker::RunAndPopNextTask(class base::internal::RegisteredTaskSource) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:391:5
    #41 0x7ffd9d0adc95 in base::internal::WorkerThread::RunWorker(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:473:36
    #42 0x7ffd9d0acaff in base::internal::WorkerThread::RunPooledWorker(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:359:3
    #43 0x7ffd9cfb8cd3 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:114:13
    #44 0x7ffddda3beee  (C:\chromium_version\latest_asan\clang_rt.asan_dynamic-x86_64.dll+0x18005beee)
    #45 0x7ffe4c127373  (C:\WINDOWS\System32\KERNEL32.DLL+0x180017373)
    #46 0x7ffe4d6dcc90  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18004cc90)

0x118c5a3b78f0 is located 0 bytes inside of 16-byte region [0x118c5a3b78f0,0x118c5a3b7900)
freed by thread T5 here:
    #0 0x7ffddda3d2c6  (C:\chromium_version\latest_asan\clang_rt.asan_dynamic-x86_64.dll+0x18005d2c6)
    #1 0x7ffd899008d8 in google::protobuf::ZeroCopyCodedInputStream::`scalar deleting dtor'(unsigned int) C:\b\s\w\ir\cache\builder\src\chrome\common\profiler\thread_profiler_platform_configuration.cc:25:7
    #2 0x7ffdb44c8b95 in std::__Cr::default_delete<safe_browsing::mojom::ExtensionWebRequestReporterProxy>::operator() C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:77
    #3 0x7ffdb44c8b95 in std::__Cr::unique_ptr<safe_browsing::mojom::ExtensionWebRequestReporterProxy,std::__Cr::default_delete<safe_browsing::mojom::ExtensionWebRequestReporterProxy> >::reset C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:290
    #4 0x7ffdb44c8b95 in std::__Cr::unique_ptr<safe_browsing::mojom::ExtensionWebRequestReporterProxy,std::__Cr::default_delete<safe_browsing::mojom::ExtensionWebRequestReporterProxy> >::~unique_ptr C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:259
    #5 0x7ffdb44c8b95 in mojo::internal::InterfacePtrState<safe_browsing::mojom::ExtensionWebRequestReporter>::~InterfacePtrState C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_ptr_state.h:142
    #6 0x7ffdb44c8b95 in mojo::Remote<safe_browsing::mojom::ExtensionWebRequestReporter>::~Remote C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\remote.h:88
    #7 0x7ffdb44c8b95 in URLLoaderThrottleProviderImpl::~URLLoaderThrottleProviderImpl(void) C:\b\s\w\ir\cache\builder\src\chrome\renderer\url_loader_throttle_provider_impl.cc:175:1
    #8 0x7ffdb44cbd0f in URLLoaderThrottleProviderImpl::`scalar deleting dtor'(unsigned int) C:\b\s\w\ir\cache\builder\src\chrome\renderer\url_loader_throttle_provider_impl.cc:163:65
    #9 0x7ffd9d0f4f77 in base::internal::DecayedFunctorTraits<void (*)(const void *),const void *&&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:663
    #10 0x7ffd9d0f4f77 in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (*&&)(const void *),const void *&&>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:922
    #11 0x7ffd9d0f4f77 in base::internal::Invoker<base::internal::FunctorTraits<void (*&&)(const void *),const void *&&>,base::internal::BindState<0,1,0,void (*)(const void *),base::internal::UnretainedWrapper<const void,base::unretained_traits::MayNotDangle,0> >,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1059
    #12 0x7ffd9d0f4f77 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl *&&)(void const *), void const *&&>, struct base::internal::BindState<0, 1, 0, void (__cdecl *)(void const *), class base::internal::UnretainedWrapper<void const, struct base::unretained_traits::MayNotDangle, 0>>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:972:12
    #13 0x7ffd9d171033 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:155
    #14 0x7ffd9d171033 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:207:34
    #15 0x7ffd9d0c611c in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:104
    #16 0x7ffd9d0c611c in base::internal::TaskTracker::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:686
    #17 0x7ffd9d0c611c in base::internal::TaskTracker::RunSkipOnShutdown(struct base::internal::Task &, class base::TaskTraits const &, class base::internal::TaskSource *, class base::internal::SequenceToken const &) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:671:3
    #18 0x7ffd9d0c475a in base::internal::TaskTracker::RunTaskWithShutdownBehavior C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:701
    #19 0x7ffd9d0c475a in base::internal::TaskTracker::RunTask(struct base::internal::Task, class base::internal::TaskSource *, class base::TaskTraits const &) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:501:5
    #20 0x7ffd9d0c382e in base::internal::TaskTracker::RunAndPopNextTask(class base::internal::RegisteredTaskSource) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:391:5
    #21 0x7ffd9d0adc95 in base::internal::WorkerThread::RunWorker(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:473:36
    #22 0x7ffd9d0acaff in base::internal::WorkerThread::RunPooledWorker(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:359:3
    #23 0x7ffd9cfb8cd3 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:114:13
    #24 0x7ffddda3beee  (C:\chromium_version\latest_asan\clang_rt.asan_dynamic-x86_64.dll+0x18005beee)
    #25 0x7ffe4c127373  (C:\WINDOWS\System32\KERNEL32.DLL+0x180017373)
    #26 0x7ffe4d6dcc90  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18004cc90)

previously allocated by thread T5 here:
    #0 0x7ffddda3c6ff  (C:\chromium_version\latest_asan\clang_rt.asan_dynamic-x86_64.dll+0x18005c6ff)
    #1 0x7ffd9a51b381 in std::__Cr::make_unique C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:759
    #2 0x7ffd9a51b381 in mojo::internal::InterfacePtrState<class safe_browsing::mojom::ExtensionWebRequestReporter>::ConfigureProxyIfNecessary(void) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_ptr_state.h:274:16
    #3 0x7ffd9a51af64 in mojo::internal::InterfacePtrState<safe_browsing::mojom::ExtensionWebRequestReporter>::instance C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_ptr_state.h:145
    #4 0x7ffd9a51af64 in mojo::Remote<class safe_browsing::mojom::ExtensionWebRequestReporter>::Bind(class mojo::PendingRemote<class safe_browsing::mojom::ExtensionWebRequestReporter>, class scoped_refptr<class base::SequencedTaskRunner>) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\remote.h:297:35
    #5 0x7ffdb44c9ee8 in mojo::Remote<safe_browsing::mojom::ExtensionWebRequestReporter>::Bind C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\remote.h:270
    #6 0x7ffdb44c9ee8 in URLLoaderThrottleProviderImpl::CreateThrottles(class base::optional_ref<class base::TokenType<class blink::LocalFrameTokenTypeMarker> const, 0>, struct network::ResourceRequest const &) C:\b\s\w\ir\cache\builder\src\chrome\renderer\url_loader_throttle_provider_impl.cc:211:39
    #7 0x7ffd96a8fb12 in blink::BackgroundURLLoader::Context::StartOnBackground(class scoped_refptr<class blink::WebBackgroundResourceFetchAssets>, class std::__Cr::unique_ptr<struct network::ResourceRequest, struct std::__Cr::default_delete<struct network::ResourceRequest>>, class url::Origin const &, bool, class blink::Vector<class blink::String, 0, class blink::PartitionAllocator> const &, class std::__Cr::unique_ptr<class blink::ResourceLoadInfoNotifierWrapper, struct std::__Cr::default_delete<class blink::ResourceLoadInfoNotifierWrapper>>, bool, class std::__Cr::unique_ptr<class blink::BackgroundResponseProcessorFactory, struct std::__Cr::default_delete<class blink::BackgroundResponseProcessorFactory>>) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\loader\fetch\url_loader\background_url_loader.cc:418:30
    #8 0x7ffd96a90fd0 in base::internal::DecayedFunctorTraits<void (blink::BackgroundURLLoader::Context::*)(scoped_refptr<blink::WebBackgroundResourceFetchAssets>, std::__Cr::unique_ptr<network::ResourceRequest,std::__Cr::default_delete<network::ResourceRequest> >, const url::Origin &, bool, const blink::Vector<blink::String,0,blink::PartitionAllocator> &, std::__Cr::unique_ptr<blink::ResourceLoadInfoNotifierWrapper,std::__Cr::default_delete<blink::ResourceLoadInfoNotifierWrapper> >, bool, std::__Cr::unique_ptr<blink::BackgroundResponseProcessorFactory,std::__Cr::default_delete<blink::BackgroundResponseProcessorFactory> >),scoped_refptr<blink::BackgroundURLLoader::Context> &&,scoped_refptr<blink::WebBackgroundResourceFetchAssets> &&,std::__Cr::unique_ptr<network::ResourceRequest,std::__Cr::default_delete<network::ResourceRequest> > &&,url::Origin &&,bool &&,blink::Vector<blink::String,0,blink::PartitionAllocator> &&,std::__Cr::unique_ptr<blink::ResourceLoadInfoNotifierWrapper,std::__Cr::default_delete<blink::ResourceLoadInfoNotifierWrapper> > &&,bool &&,std::__Cr::unique_ptr<blink::BackgroundResponseProcessorFactory,std::__Cr::default_delete<blink::BackgroundResponseProcessorFactory> > &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:730
    #9 0x7ffd96a90fd0 in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (blink::BackgroundURLLoader::Context::*&&)(scoped_refptr<blink::WebBackgroundResourceFetchAssets>, std::__Cr::unique_ptr<network::ResourceRequest,std::__Cr::default_delete<network::ResourceRequest> >, const url::Origin &, bool, const blink::Vector<blink::String,0,blink::PartitionAllocator> &, std::__Cr::unique_ptr<blink::ResourceLoadInfoNotifierWrapper,std::__Cr::default_delete<blink::ResourceLoadInfoNotifierWrapper> >, bool, std::__Cr::unique_ptr<blink::BackgroundResponseProcessorFactory,std::__Cr::default_delete<blink::BackgroundResponseProcessorFactory> >),scoped_refptr<blink::BackgroundURLLoader::Context> &&,scoped_refptr<blink::WebBackgroundResourceFetchAssets> &&,std::__Cr::unique_ptr<network::ResourceRequest,std::__Cr::default_delete<network::ResourceRequest> > &&,url::Origin &&,bool &&,blink::Vector<blink::String,0,blink::PartitionAllocator> &&,std::__Cr::unique_ptr<blink::ResourceLoadInfoNotifierWrapper,std::__Cr::default_delete<blink::ResourceLoadInfoNotifierWrapper> > &&,bool &&,std::__Cr::unique_ptr<blink::BackgroundResponseProcessorFactory,std::__Cr::default_delete<blink::BackgroundResponseProcessorFactory> > &&>,void,0,1,2,3,4,5,6,7,8>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:922
    #10 0x7ffd96a90fd0 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::BackgroundURLLoader::Context::*&&)(scoped_refptr<blink::WebBackgroundResourceFetchAssets>, std::__Cr::unique_ptr<network::ResourceRequest,std::__Cr::default_delete<network::ResourceRequest> >, const url::Origin &, bool, const blink::Vector<blink::String,0,blink::PartitionAllocator> &, std::__Cr::unique_ptr<blink::ResourceLoadInfoNotifierWrapper,std::__Cr::default_delete<blink::ResourceLoadInfoNotifierWrapper> >, bool, std::__Cr::unique_ptr<blink::BackgroundResponseProcessorFactory,std::__Cr::default_delete<blink::BackgroundResponseProcessorFactory> >),scoped_refptr<blink::BackgroundURLLoader::Context> &&,scoped_refptr<blink::WebBackgroundResourceFetchAssets> &&,std::__Cr::unique_ptr<network::ResourceRequest,std::__Cr::default_delete<network::ResourceRequest> > &&,url::Origin &&,bool &&,blink::Vector<blink::String,0,blink::PartitionAllocator> &&,std::__Cr::unique_ptr<blink::ResourceLoadInfoNotifierWrapper,std::__Cr::default_delete<blink::ResourceLoadInfoNotifierWrapper> > &&,bool &&,std::__Cr::unique_ptr<blink::BackgroundResponseProcessorFactory,std::__Cr::default_delete<blink::BackgroundResponseProcessorFactory> > &&>,base::internal::BindState<1,1,0,void (blink::BackgroundURLLoader::Context::*)(scoped_refptr<blink::WebBackgroundResourceFetchAssets>, std::__Cr::unique_ptr<network::ResourceRequest,std::__Cr::default_delete<network::ResourceRequest> >, const url::Origin &, bool, const blink::Vector<blink::String,0,blink::PartitionAllocator> &, std::__Cr::unique_ptr<blink::ResourceLoadInfoNotifierWrapper,std::__Cr::default_delete<blink::ResourceLoadInfoNotifierWrapper> >, bool, std::__Cr::unique_ptr<blink::BackgroundResponseProcessorFactory,std::__Cr::default_delete<blink::BackgroundResponseProcessorFactory> >),scoped_refptr<blink::BackgroundURLLoader::Context>,scoped_refptr<blink::WebBackgroundResourceFetchAssets>,std::__Cr::unique_ptr<network::ResourceRequest,std::__Cr::default_delete<network::ResourceRequest> >,url::Origin,bool,blink::Vector<blink::String,0,blink::PartitionAllocator>,std::__Cr::unique_ptr<blink::ResourceLoadInfoNotifierWrapper,std::__Cr::default_delete<blink::ResourceLoadInfoNotifierWrapper> >,bool,std::__Cr::unique_ptr<blink::BackgroundResponseProcessorFactory,std::__Cr::default_delete<blink::BackgroundResponseProcessorFactory> > >,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1059
    #11 0x7ffd96a90fd0 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl blink::BackgroundURLLoader::Context::*&&)(class scoped_refptr<class blink::WebBackgroundResourceFetchAssets>, class std::__Cr::unique_ptr<struct network::ResourceRequest, struct std::__Cr::default_delete<struct network::ResourceRequest>>, class url::Origin const &, bool, class blink::Vector<class blink::String, 0, class blink::PartitionAllocator> const &, class std::__Cr::unique_ptr<class blink::ResourceLoadInfoNotifierWrapper, struct std::__Cr::default_delete<class blink::ResourceLoadInfoNotifierWrapper>>, bool, class std::__Cr::unique_ptr<class blink::BackgroundResponseProcessorFactory, struct std::__Cr::default_delete<class blink::BackgroundResponseProcessorFactory>>), class scoped_refptr<class blink::BackgroundURLLoader::Context> &&, class scoped_refptr<class blink::WebBackgroundResourceFetchAssets> &&, class std::__Cr::unique_ptr<struct network::ResourceRequest, struct std::__Cr::default_delete<struct network::ResourceRequest>> &&, class url::Origin &&, bool &&, class blink::Vector<class blink::String, 0, class blink::PartitionAllocator> &&, class std::__Cr::unique_ptr<class blink::ResourceLoadInfoNotifierWrapper, struct std::__Cr::default_delete<class blink::ResourceLoadInfoNotifierWrapper>> &&, bool &&, class std::__Cr::unique_ptr<class blink::BackgroundResponseProcessorFactory, struct std::__Cr::default_delete<class blink::BackgroundResponseProcessorFactory>> &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl blink::BackgroundURLLoader::Context::*)(class scoped_refptr<class blink::WebBackgroundResourceFetchAssets>, class std::__Cr::unique_ptr<struct network::ResourceRequest, struct std::__Cr::default_delete<struct network::ResourceRequest>>, class url::Origin const &, bool, class blink::Vector<class blink::String, 0, class blink::PartitionAllocator> const &, class std::__Cr::unique_ptr<class blink::ResourceLoadInfoNotifierWrapper, struct std::__Cr::default_delete<class blink::ResourceLoadInfoNotifierWrapper>>, bool, class std::__Cr::unique_ptr<class blink::BackgroundResponseProcessorFactory, struct std::__Cr::default_delete<class blink::BackgroundResponseProcessorFactory>>), class scoped_refptr<class blink::BackgroundURLLoader::Context>, class scoped_refptr<class blink::WebBackgroundResourceFetchAssets>, class std::__Cr::unique_ptr<struct network::ResourceRequest, struct std::__Cr::default_delete<struct network::ResourceRequest>>, class url::Origin, bool, class blink::Vector<class blink::String, 0, class blink::PartitionAllocator>, class std::__Cr::unique_ptr<class blink::ResourceLoadInfoNotifierWrapper, struct std::__Cr::default_delete<class blink::ResourceLoadInfoNotifierWrapper>>, bool, class std::__Cr::unique_ptr<class blink::BackgroundResponseProcessorFactory, struct std::__Cr::default_delete<class blink::BackgroundResponseProcessorFactory>>>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:972:12
    #12 0x7ffd9d171033 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:155
    #13 0x7ffd9d171033 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:207:34
    #14 0x7ffd9d0c611c in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:104
    #15 0x7ffd9d0c611c in base::internal::TaskTracker::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:686
    #16 0x7ffd9d0c611c in base::internal::TaskTracker::RunSkipOnShutdown(struct base::internal::Task &, class base::TaskTraits const &, class base::internal::TaskSource *, class base::internal::SequenceToken const &) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:671:3
    #17 0x7ffd9d0c475a in base::internal::TaskTracker::RunTaskWithShutdownBehavior C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:701
    #18 0x7ffd9d0c475a in base::internal::TaskTracker::RunTask(struct base::internal::Task, class base::internal::TaskSource *, class base::TaskTraits const &) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:501:5
    #19 0x7ffd9d0c382e in base::internal::TaskTracker::RunAndPopNextTask(class base::internal::RegisteredTaskSource) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:391:5
    #20 0x7ffd9d0adc95 in base::internal::WorkerThread::RunWorker(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:473:36
    #21 0x7ffd9d0acaff in base::internal::WorkerThread::RunPooledWorker(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:359:3
    #22 0x7ffd9cfb8cd3 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:114:13
    #23 0x7ffddda3beee  (C:\chromium_version\latest_asan\clang_rt.asan_dynamic-x86_64.dll+0x18005beee)
    #24 0x7ffe4c127373  (C:\WINDOWS\System32\KERNEL32.DLL+0x180017373)
    #25 0x7ffe4d6dcc90  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18004cc90)

Thread T5 created by T0 here:
    #0 0x7ffddda3be04  (C:\chromium_version\latest_asan\clang_rt.asan_dynamic-x86_64.dll+0x18005be04)
    #1 0x7ffd9cfb7ffc in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:182:7
    #2 0x7ffd9d0ab13f in base::internal::WorkerThread::Start(class scoped_refptr<class base::SingleThreadTaskRunner>, class base::WorkerThreadObserver *) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:185:3
    #3 0x7ffd9d0bbc97 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group.cc:90:13
    #4 0x7ffd9d0bb96d in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group.cc:81:3
    #5 0x7ffd9d0b0557 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::~ScopedCommandsExecutor C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group_impl.cc:43
    #6 0x7ffd9d0b0557 in base::internal::ThreadGroupImpl::Start(unsigned __int64, unsigned __int64, class base::TimeDelta, class scoped_refptr<class base::SingleThreadTaskRunner>, class base::WorkerThreadObserver *, enum base::internal::ThreadGroup::WorkerEnvironment, bool, class std::__Cr::optional<class base::TimeDelta>) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group_impl.cc:252:3
    #7 0x7ffd9d0a1805 in base::internal::ThreadPoolImpl::Start(struct base::ThreadPoolInstance::InitParams const &, class base::WorkerThreadObserver *) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_pool_impl.cc:198:35
    #8 0x7ffda725b2a8 in content::ChildProcess::ChildProcess(enum base::ThreadType, class std::__Cr::unique_ptr<struct base::ThreadPoolInstance::InitParams, struct std::__Cr::default_delete<struct base::ThreadPoolInstance::InitParams>>, bool) C:\b\s\w\ir\cache\builder\src\content\child\child_process.cc:113:20
    #9 0x7ffda73679eb in content::RenderProcess::RenderProcess(class std::__Cr::unique_ptr<struct base::ThreadPoolInstance::InitParams, struct std::__Cr::default_delete<struct base::ThreadPoolInstance::InitParams>>) C:\b\s\w\ir\cache\builder\src\content\renderer\render_process.cc:18:7
    #10 0x7ffda73670bd in content::RenderProcessImpl::RenderProcessImpl(void) C:\b\s\w\ir\cache\builder\src\content\renderer\render_process_impl.cc:98:7
    #11 0x7ffda7367685 in content::RenderProcessImpl::Create(void) C:\b\s\w\ir\cache\builder\src\content\renderer\render_process_impl.cc:216:31
    #12 0x7ffda7284806 in content::RendererMain(struct content::MainFunctionParams) C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:276:53
    #13 0x7ffd99053b6c in content::RunOtherNamedProcessTypeMain(class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>> const &, struct content::MainFunctionParams, class content::ContentMainDelegate *) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:764:14
    #14 0x7ffd99055fa3 in content::ContentMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1130:10
    #15 0x7ffd9904a31f in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:346:36
    #16 0x7ffd9904a88e in content::ContentMain(struct content::ContentMainParams) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:359:10
    #17 0x7ffd898f300f in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:228:12
    #18 0x7ff784f5483b in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:201:12
    #19 0x7ff784f52085 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:352:20
    #20 0x7ff78542e7bf in invoke_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #21 0x7ff78542e7bf in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #22 0x7ffe4c127373  (C:\WINDOWS\System32\KERNEL32.DLL+0x180017373)
    #23 0x7ffe4d6dcc90  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18004cc90)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\base\memory\raw_ptr_asan_hooks.cc:54:17 in base::internal::`anonymous namespace'::CrashImmediatelyOnUseAfterFree
Shadow bytes around the buggy address:
  0x118c5a3b7600: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fa
  0x118c5a3b7680: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fa
  0x118c5a3b7700: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fa
  0x118c5a3b7780: f7 fa fd fa f7 fa fd fa f7 fa fd fd f7 fa fd fd
  0x118c5a3b7800: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fa
=>0x118c5a3b7880: f7 fa fd fa f7 fa fd fa f7 fa fd fd f7 fa[fd]fd
  0x118c5a3b7900: f7 fa 00 fa f7 fa fd fa f7 fa fd fd f7 fa 00 fa
  0x118c5a3b7980: f7 fa 00 fa f7 fa 00 fa f7 fa 00 fa f7 fa 00 fa
  0x118c5a3b7a00: f7 fa 00 fa f7 fa 00 fa f7 fa 00 fa f7 fa 00 fa
  0x118c5a3b7a80: f7 fa 00 fa f7 fa 00 00 f7 fa 00 00 f7 fa 00 fa
  0x118c5a3b7b00: f7 fa 00 fa f7 fa 00 fa f7 fa 00 fa f7 fa 00 fa
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

==4664==ADDITIONAL INFO

==4664==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffd9d6a0c9f in mojo::SimpleWatcher::Context::Notify(unsigned int, struct MojoHandleSignalsState, unsigned int) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc:102:13


Command line: `"C:\asan\chrome.exe" --type=renderer --user-data-dir=C:/tmp/test--extensions-on-chrome-urls --no-pre-read-main-dll --no-sandbox --file-url-path-alias="/gen=C:\asan\gen" --video-capture-use-gpu-memory-buffer --lang=en-US --device-scale-factor=1.75 --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1758707867337761 --launch-time-ticks=51381261914 --metrics-shmem-handle=3212,i,1427474096340128744,5752336122806041417,2097152 --field-trial-handle=1920,i,6349326568880425583,5959785934015148551,262144 --variations-seed-version --trace-process-track-uuid=3190708990997080739 --mojo-platform-channel-handle=3208 /prefetch:1`


MiraclePtr Status: MANUAL ANALYSIS REQUIRED
This crash occurred while a raw_ptr<T> object containing a dangling pointer was being dereferenced.
This crash occurred in the thread pool. The sequence which invoked the "free" is unknown, so the crash may have been caused by a race condition that is mislabeled as a use-after-free. Make sure that the "free" is sequenced after the "use" (e.g. both are on the same sequence, or the "free" is in a task posted after the "use"). Otherwise, the crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==4664==END OF ADDITIONAL INFO
==4664==ABORTING



## Attachments

- [manifest.json](attachments/manifest.json) (application/json, 466 B)
- [background.js](attachments/background.js) (text/javascript, 794 B)
- [content.js](attachments/content.js) (text/javascript, 158 B)

## Timeline

### wf...@chromium.org (2025-09-25)

Thank you for your report.

### wf...@chromium.org (2025-09-25)

Thanks, I tried to repro on asan build 142.0.7432.0 and was unable to reproduce. I'll try the official asan archive binaries.

### wf...@chromium.org (2025-09-25)

took me a few tries but I am able to repro this, same stack as the reporter. `safe_browsing::mojom::ExtensionWebRequestReporter` freeing does appear to be culprit. Will continue triage shortly.

Thank you for your report!

### wf...@chromium.org (2025-09-25)

richche@, please can you take a look at this security issue. thank you.

### ch...@google.com (2025-09-26)

Setting milestone because of s0/s1 severity.

### va...@chromium.org (2025-09-26)

Assigning to anunoy@ for the initial triage since richche@ is OOO right now.

### ja...@chromium.org (2025-10-02)

[safebrowsing triage] @an...@chromium.org seems like a good owner for this bug and has a CL out for review. Marking this as triaged for the component.

### dx...@google.com (2025-10-03)

Project: chromium/src  

Branch:  main  

Author:  Anunoy Ghosh [anunoy@chromium.org](mailto:anunoy@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6997254>

safe\_browsing: Fix UAF in RendererURLLoaderThrottle

---


Expand for full commit details
```
     
    A race condition could cause a Use-After-Free in the renderer when a 
    resource load was redirected. 
     
    The RendererURLLoaderThrottle held a raw_ptr to the 
    ExtensionWebRequestReporter. This reporter is owned by the 
    URLLoaderThrottleProviderImpl. If the provider was destroyed (e.g., due 
    to a frame navigating away) while a throttled request was in flight, the 
    reporter would be freed. 
     
    If the request then received a redirect, the throttle's 
    WillRedirectRequest method would attempt to dereference the dangling 
    pointer to the reporter, causing a crash. 
     
    This change fixes the UAF by replacing the raw_ptr with a 
    mojo::Remote<ExtensionWebRequestReporter>. The provider now holds a 
    mojo::Receiver for the reporter and clones a mojo::PendingRemote to pass 
    to the throttle. This leverages Mojo's connection-based lifetime 
    management. If the provider is destroyed, the pipe is closed, and any 
    subsequent calls on the throttle's remote are safely dropped. 
     
    To handle cases where the URLLoaderThrottle is used on a different 
    thread from where it was created, the PendingRemote is unbound from its 
    original thread and rebound on the thread where the throttle's methods 
    are invoked. This ensures that the mojo::Remote is bound to the correct 
    sequence. 
     
    A unit test was added to simulate the race condition by destroying the 
    reporter after a redirect is initiated, verifying that the crash no 
    longer occurs. 
     
    Bug: 447192722 
    Change-Id: Ie786b5520c10af6c9de8880be66239531c91bd32 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6997254 
    Reviewed-by: Ted Choc <tedchoc@chromium.org> 
    Commit-Queue: Anunoy Ghosh <anunoy@chromium.org> 
    Reviewed-by: Daniel Rubery <drubery@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1525014}

```

---

Files:

- M `chrome/renderer/url_loader_throttle_provider_impl.cc`
- M `components/safe_browsing/content/renderer/renderer_url_loader_throttle.cc`
- M `components/safe_browsing/content/renderer/renderer_url_loader_throttle.h`
- M `components/safe_browsing/content/renderer/renderer_url_loader_throttle_unittest.cc`

---

Hash: [8fee64979a32f85b4107f8e53e802f3ae782c6a1](https://chromiumdash.appspot.com/commit/8fee64979a32f85b4107f8e53e802f3ae782c6a1)  

Date: Fri Oct 3 21:06:47 2025


---

### ch...@google.com (2025-10-03)

This issue has a target milestone of 140 (currently shipping to stable), but the following CLs are not present in that milestone!

- <https://chromium-review.googlesource.com/6997254>

[Request a merge](https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md) to 140 if this is unintended.

This comment was automatically generated by the [CrCA Milestone Checker Apps Script](http://go/crca-milestone-checker). This script will not comment again on this issue for M140 unless more CLs are added.

### an...@chromium.org (2025-10-06)

I've landed a fix and verified it in a Canary build. Will request merges back to M140, M141 now.

### ch...@google.com (2025-10-06)

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
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2025-10-06)

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
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### an...@chromium.org (2025-10-06)

1. This fix addresses a high-severity security issue
2. <https://chromium-review.googlesource.com/6997254>
3. Change has been released and tested on Canary
4. No, this is not a new feature
5. N/A
6. No manual testing required by the test team

### ch...@google.com (2025-10-06)

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
Owners: andywu (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### an...@chromium.org (2025-10-06)

See c#14

### ts...@google.com (2025-10-06)

Would like to get this into m141 but we are too close to the current re-spin.  It can merge to m142 (7444) at present.

### an...@chromium.org (2025-10-06)

Ack, do we need to merge to M140 at all?

### ts...@google.com (2025-10-07)

Can now merge to m141 (7390) to pick up the next respin, please merge by Fri 10-Oct.

### ts...@google.com (2025-10-07)

re #18: M140 merges not required 

### dx...@google.com (2025-10-07)

Project: chromium/src  

Branch:  refs/branch-heads/7444  

Author:  Anunoy Ghosh [anunoy@chromium.org](mailto:anunoy@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7013507>

[M142] safe\_browsing: Fix UAF in RendererURLLoaderThrottle

---


Expand for full commit details
```
     
    A race condition could cause a Use-After-Free in the renderer when a 
    resource load was redirected. 
     
    The RendererURLLoaderThrottle held a raw_ptr to the 
    ExtensionWebRequestReporter. This reporter is owned by the 
    URLLoaderThrottleProviderImpl. If the provider was destroyed (e.g., due 
    to a frame navigating away) while a throttled request was in flight, the 
    reporter would be freed. 
     
    If the request then received a redirect, the throttle's 
    WillRedirectRequest method would attempt to dereference the dangling 
    pointer to the reporter, causing a crash. 
     
    This change fixes the UAF by replacing the raw_ptr with a 
    mojo::Remote<ExtensionWebRequestReporter>. The provider now holds a 
    mojo::Receiver for the reporter and clones a mojo::PendingRemote to pass 
    to the throttle. This leverages Mojo's connection-based lifetime 
    management. If the provider is destroyed, the pipe is closed, and any 
    subsequent calls on the throttle's remote are safely dropped. 
     
    To handle cases where the URLLoaderThrottle is used on a different 
    thread from where it was created, the PendingRemote is unbound from its 
    original thread and rebound on the thread where the throttle's methods 
    are invoked. This ensures that the mojo::Remote is bound to the correct 
    sequence. 
     
    A unit test was added to simulate the race condition by destroying the 
    reporter after a redirect is initiated, verifying that the crash no 
    longer occurs. 
     
    (cherry picked from commit 5efb5dc5f2842f9fc448d2eca9c8835c712bf674) 
     
    Bug: 447192722 
    Change-Id: Ie786b5520c10af6c9de8880be66239531c91bd32 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6997254 
    Reviewed-by: Ted Choc <tedchoc@chromium.org> 
    Commit-Queue: Anunoy Ghosh <anunoy@chromium.org> 
    Reviewed-by: Daniel Rubery <drubery@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1525014} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7013507 
    Auto-Submit: Anunoy Ghosh <anunoy@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7444@{#480} 
    Cr-Branched-From: 29907d3c18078029695f458b42fb8e6fda3e493d-refs/heads/main@{#1522585}

```

---

Files:

- M `chrome/renderer/url_loader_throttle_provider_impl.cc`
- M `components/safe_browsing/content/renderer/renderer_url_loader_throttle.cc`
- M `components/safe_browsing/content/renderer/renderer_url_loader_throttle.h`
- M `components/safe_browsing/content/renderer/renderer_url_loader_throttle_unittest.cc`

---

Hash: [58dfeb9291bd77d383a791c096e50c659d48b113](https://chromiumdash.appspot.com/commit/58dfeb9291bd77d383a791c096e50c659d48b113)  

Date: Tue Oct 7 17:14:23 2025


---

### pe...@google.com (2025-10-07)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### an...@chromium.org (2025-10-07)

In response to c#22,

1. This is a security bug (UAF) that has existed since M118
2. No, this is not an issue related to a change or feature merged after latest LTS milestone

### dx...@google.com (2025-10-07)

Project: chromium/src  

Branch:  refs/branch-heads/7390  

Author:  Anunoy Ghosh [anunoy@chromium.org](mailto:anunoy@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7018151>

[M141] safe\_browsing: Fix UAF in RendererURLLoaderThrottle

---


Expand for full commit details
```
     
    A race condition could cause a Use-After-Free in the renderer when a 
    resource load was redirected. 
     
    The RendererURLLoaderThrottle held a raw_ptr to the 
    ExtensionWebRequestReporter. This reporter is owned by the 
    URLLoaderThrottleProviderImpl. If the provider was destroyed (e.g., due 
    to a frame navigating away) while a throttled request was in flight, the 
    reporter would be freed. 
     
    If the request then received a redirect, the throttle's 
    WillRedirectRequest method would attempt to dereference the dangling 
    pointer to the reporter, causing a crash. 
     
    This change fixes the UAF by replacing the raw_ptr with a 
    mojo::Remote<ExtensionWebRequestReporter>. The provider now holds a 
    mojo::Receiver for the reporter and clones a mojo::PendingRemote to pass 
    to the throttle. This leverages Mojo's connection-based lifetime 
    management. If the provider is destroyed, the pipe is closed, and any 
    subsequent calls on the throttle's remote are safely dropped. 
     
    To handle cases where the URLLoaderThrottle is used on a different 
    thread from where it was created, the PendingRemote is unbound from its 
    original thread and rebound on the thread where the throttle's methods 
    are invoked. This ensures that the mojo::Remote is bound to the correct 
    sequence. 
     
    A unit test was added to simulate the race condition by destroying the 
    reporter after a redirect is initiated, verifying that the crash no 
    longer occurs. 
     
    (cherry picked from commit 8fee64979a32f85b4107f8e53e802f3ae782c6a1) 
     
    Bug: 447192722 
    Change-Id: Ie786b5520c10af6c9de8880be66239531c91bd32 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6997254 
    Reviewed-by: Ted Choc <tedchoc@chromium.org> 
    Commit-Queue: Anunoy Ghosh <anunoy@chromium.org> 
    Reviewed-by: Daniel Rubery <drubery@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1525014} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7018151 
    Cr-Commit-Position: refs/branch-heads/7390@{#2189} 
    Cr-Branched-From: d481efce5eb300acbb896686676ebd0352a6f1db-refs/heads/main@{#1509326}

```

---

Files:

- M `chrome/renderer/url_loader_throttle_provider_impl.cc`
- M `components/safe_browsing/content/renderer/renderer_url_loader_throttle.cc`
- M `components/safe_browsing/content/renderer/renderer_url_loader_throttle.h`
- M `components/safe_browsing/content/renderer/renderer_url_loader_throttle_unittest.cc`

---

Hash: [6318e0d832f22409b9be3a564073ef5508ce2184](https://chromiumdash.appspot.com/commit/6318e0d832f22409b9be3a564073ef5508ce2184)  

Date: Tue Oct 7 18:52:04 2025


---

### sp...@google.com (2025-10-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
Baseline renderer memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### rz...@google.com (2025-10-16)

The bot isn't adding the questionnaire for LTS-138, but here are the answers:

1. <https://crrev.com/c/7027591>
2. Low, no coflicts
3. 141, 142
4. Yes

### pe...@google.com (2025-10-16)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### dx...@google.com (2025-11-03)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Anunoy Ghosh [anunoy@chromium.org](mailto:anunoy@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7027591>

[M138-LTS] safe\_browsing: Fix UAF in RendererURLLoaderThrottle

---


Expand for full commit details
```
     
    A race condition could cause a Use-After-Free in the renderer when a 
    resource load was redirected. 
     
    The RendererURLLoaderThrottle held a raw_ptr to the 
    ExtensionWebRequestReporter. This reporter is owned by the 
    URLLoaderThrottleProviderImpl. If the provider was destroyed (e.g., due 
    to a frame navigating away) while a throttled request was in flight, the 
    reporter would be freed. 
     
    If the request then received a redirect, the throttle's 
    WillRedirectRequest method would attempt to dereference the dangling 
    pointer to the reporter, causing a crash. 
     
    This change fixes the UAF by replacing the raw_ptr with a 
    mojo::Remote<ExtensionWebRequestReporter>. The provider now holds a 
    mojo::Receiver for the reporter and clones a mojo::PendingRemote to pass 
    to the throttle. This leverages Mojo's connection-based lifetime 
    management. If the provider is destroyed, the pipe is closed, and any 
    subsequent calls on the throttle's remote are safely dropped. 
     
    To handle cases where the URLLoaderThrottle is used on a different 
    thread from where it was created, the PendingRemote is unbound from its 
    original thread and rebound on the thread where the throttle's methods 
    are invoked. This ensures that the mojo::Remote is bound to the correct 
    sequence. 
     
    A unit test was added to simulate the race condition by destroying the 
    reporter after a redirect is initiated, verifying that the crash no 
    longer occurs. 
     
    (cherry picked from commit 8fee64979a32f85b4107f8e53e802f3ae782c6a1) 
     
    Bug: 447192722 
    Change-Id: Ie786b5520c10af6c9de8880be66239531c91bd32 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6997254 
    Commit-Queue: Anunoy Ghosh <anunoy@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1525014} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7027591 
    Reviewed-by: Theresa Sullivan <twellington@chromium.org> 
    Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com> 
    Reviewed-by: Fahad Mansoor <fahadmansoor@google.com> 
    Reviewed-by: Daniel Rubery <drubery@chromium.org> 
    Reviewed-by: Anunoy Ghosh <anunoy@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3441} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `chrome/renderer/url_loader_throttle_provider_impl.cc`
- M `components/safe_browsing/content/renderer/renderer_url_loader_throttle.cc`
- M `components/safe_browsing/content/renderer/renderer_url_loader_throttle.h`
- M `components/safe_browsing/content/renderer/renderer_url_loader_throttle_unittest.cc`

---

Hash: [97ff17d35aa2c4de45708096272a22cc04838010](https://chromiumdash.appspot.com/commit/97ff17d35aa2c4de45708096272a22cc04838010)  

Date: Mon Nov 3 18:58:30 2025


---

### ch...@google.com (2026-01-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/447192722)*
