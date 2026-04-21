# Security: UAF in ServiceWorker with bfcache

| Field | Value |
|-------|-------|
| **Issue ID** | [40055982](https://issues.chromium.org/issues/40055982) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>ServiceWorker, UI>Browser>Navigation>BFCache |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | jt...@gmail.com |
| **Assignee** | as...@chromium.org |
| **Created** | 2021-05-24 |
| **Bounty** | $25,000.00 |

## Description

**VULNERABILITY DETAILS**

In function ServiceWorkerContainerHost::UpdateController, |this| was removed from |controllee\_map\_| of the old controller [1]. However, |controllee\_map\_| would not contain |this| if the ServiceWorkerContainerHost was in back-forward cache, and |this| should be removed from |bfcached\_controllee\_map\_| instead. So |bfcached\_controllee\_map\_| of old controller would keep a raw pointer to the ServiceWorkerContainerHost after its decontruction, which may leads to UAF.

```
void ServiceWorkerContainerHost::UpdateController(  
    bool notify_controllerchange) {  
  // skip  
  
  scoped_refptr<ServiceWorkerVersion> previous_version = controller_;  
  controller_ = version;  
  if (version) {  
    version->AddControllee(this);  
    if (IsBackForwardCacheEnabled() && IsInBackForwardCache()) {  
      // |this| was not |version|'s controllee when |OnEnterBackForwardCache|  
      // was called.  
      version->MoveControlleeToBackForwardCacheMap(client_uuid());  
    }  
  }  
  if (previous_version)  
    previous_version->RemoveControllee(client_uuid());  // =====> [1]  
  
  // skip  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/service_worker/service_worker_container_host.cc;l=1254;drc=f62d1bf48ec3e52b3d5ed34f768b5e5abf989a4c>

**VERSION**  

Chrome Version: 90.0.4430.212 (stable)

**REPRODUCTION CASE**  

Steps to reproduce (on Linux platform):

1. Unzip the attached file to <poc\_dir>.
2. Setup a HTTPServer with nodejs.  
   
   cd <poc\_dir>  
   
   nodejs ./server.js
3. Run asan build chrome, and click the link in the page, the browser process should crash in a few seconds.  
   
   ./chrome --enable-features=BackForwardCache <http://localhost:8000/foo/a.html>

Note:

1. This bug can be triggered WITHOUT a compromised renderer.
2. BackForwardCache was enabled by default on Android, but behind a flag on other platforms, so the command '--enable-features=BackForwardCache' is required to repro the bug for convenience.

## Attachments

- [poc.zip](attachments/poc.zip) (application/octet-stream, 1.9 KB)
- [asan.log](attachments/asan.log) (text/plain, 26.8 KB)

## Timeline

### [Deleted User] (2021-05-24)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-05-26)

Tentatively applying labels, I'm still working on reproducing the crash.

[Monorail components: Blink>ServiceWorker]

### va...@chromium.org (2021-05-26)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-05-26)

[Empty comment from Monorail migration]

### fa...@chromium.org (2021-05-26)

asamidoi: Would you like to take this one?

[Monorail components: UI>Browser>Navigation>BFCache]

### va...@chromium.org (2021-05-26)

$ builds/asan-linux-release-857950-90.0.4430.212-Stable/chrome-wrapper --enable-features=BackForwardCache http://localhost:8000/foo/a.html | tools/valgrind/asan/asan_symbolize.py


=================================================================
==375787==ERROR: AddressSanitizer: heap-use-after-free on address 0x619000702a58 at pc 0x55a4769b7e74 bp 0x7ffc58722630 sp 0x7ffc58722628
WRITE of size 1 at 0x619000702a58 thread T0 (chrome)
    #0 0x55a4769b7e73 in content::ServiceWorkerContainerHost::EvictFromBackForwardCache(content::BackForwardCacheMetrics::NotRestoredReason) content/browser/service_worker/service_worker_container_host.cc:1090:29
    #1 0x55a476b390a9 in EvictBackForwardCachedControllee content/browser/service_worker/service_worker_version.cc:932:15
    #2 0x55a476b390a9 in content::ServiceWorkerVersion::EvictBackForwardCachedControllees(content::BackForwardCacheMetrics::NotRestoredReason) content/browser/service_worker/service_worker_version.cc:925:5
    #3 0x55a476aa2fa4 in content::ServiceWorkerRegistration::ActivateWaitingVersion(bool) content/browser/service_worker/service_worker_registration.cc:494:24
    #4 0x55a476b3528e in content::ServiceWorkerVersion::OnNoWorkInBrowser() content/browser/service_worker/service_worker_version.cc:2309:21
    #5 0x55a476b3f813 in content::ServiceWorkerVersion::OnStoppedInternal(content::EmbeddedWorkerStatus) content/browser/service_worker/service_worker_version.cc:2281:5
    #6 0x55a4769782a1 in content::EmbeddedWorkerInstance::OnStopped() content/browser/service_worker/embedded_worker_instance.cc:688:14
    #7 0x55a4739bc85d in blink::mojom::EmbeddedWorkerInstanceHostStubDispatch::Accept(blink::mojom::EmbeddedWorkerInstanceHost*, mojo::Message*) gen/third_party/blink/public/mojom/service_worker/embedded_worker.mojom.cc:1333:13
    #8 0x55a47ee0f5ba in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:554:54
    #9 0x55a47ee1b4f1 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #10 0x55a47ee26d16 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:955:42
    #11 0x55a47ee25408 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:622:38
    #12 0x55a47ee1b4f1 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #13 0x55a47ee08db4 in mojo::Connector::DispatchMessage(mojo::Message) mojo/public/cpp/bindings/lib/connector.cc:508:49
    #14 0x55a47ee0a790 in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:566:14
    #15 0x55a47ee70edd in Run base/callback.h:168:12
    #16 0x55a47ee70edd in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.cc:278:14
    #17 0x55a47ee720a4 in Invoke<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> base/bind_internal.h:498:12
    #18 0x55a47ee720a4 in MakeItSo<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> base/bind_internal.h:657:5
    #19 0x55a47ee720a4 in RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), std::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0, 1, 2, 3> base/bind_internal.h:710:12
    #20 0x55a47ee720a4 in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:679:12
    #21 0x55a47d447dd0 in Run base/callback.h:101:12
    #22 0x55a47d447dd0 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:163:33
    #23 0x55a47d482977 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:351:25
    #24 0x55a47d4821a4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:264:36
    #25 0x55a47d347459 in HandleDispatch base/message_loop/message_pump_glib.cc:374:46
    #26 0x55a47d347459 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:124:43
    #27 0x7f0741396e6a in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x51e6a)

0x619000702a58 is located 984 bytes inside of 1016-byte region [0x619000702680,0x619000702a78)
freed by thread T0 (chrome) here:
    #0 0x55a470d618bd in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160:3
    #1 0x55a4769e0c2e in operator() buildtools/third_party/libc++/trunk/include/memory:1335:5
    #2 0x55a4769e0c2e in reset buildtools/third_party/libc++/trunk/include/memory:1596:7
    #3 0x55a4769e0c2e in ~unique_ptr buildtools/third_party/libc++/trunk/include/memory:1550:19
    #4 0x55a4769e0c2e in ~pair buildtools/third_party/libc++/trunk/include/utility:297:29
    #5 0x55a4769e0c2e in destroy<std::pair<const std::string, std::unique_ptr<content::ServiceWorkerContainerHost> >, void, void> buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:317:15
    #6 0x55a4769e0c2e in std::__1::__tree<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::unique_ptr<content::ServiceWorkerContainerHost, std::__1::default_delete<content::ServiceWorkerContainerHost> > >, std::__1::__map_value_compare<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::unique_ptr<content::ServiceWorkerContainerHost, std::__1::default_delete<content::ServiceWorkerContainerHost> > >, std::__1::less<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > >, true>, std::__1::allocator<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::unique_ptr<content::ServiceWorkerContainerHost, std::__1::default_delete<content::ServiceWorkerContainerHost> > > > >::erase(std::__1::__tree_const_iterator<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::unique_ptr<content::ServiceWorkerContainerHost, std::__1::default_delete<content::ServiceWorkerContainerHost> > >, std::__1::__tree_node<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::unique_ptr<content::ServiceWorkerContainerHost, std::__1::default_delete<content::ServiceWorkerContainerHost> > >, void*>*, long>) buildtools/third_party/libc++/trunk/include/__tree:2422:5
    #7 0x55a4769c6acd in __erase_unique<std::string> buildtools/third_party/libc++/trunk/include/__tree:2445:5
    #8 0x55a4769c6acd in erase buildtools/third_party/libc++/trunk/include/map:1306:25
    #9 0x55a4769c6acd in content::ServiceWorkerContextCore::OnContainerHostReceiverDisconnected() content/browser/service_worker/service_worker_context_core.cc:506:44
    #10 0x55a4769e04ba in Run base/callback.h:168:12
    #11 0x55a4769e04ba in mojo::ReceiverSetBase<mojo::AssociatedReceiver<blink::mojom::ServiceWorkerContainerHost, mojo::RawPtrImplRefTraits<blink::mojom::ServiceWorkerContainerHost> >, content::ServiceWorkerContainerHost*>::OnDisconnect(unsigned long, unsigned int, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) mojo/public/cpp/bindings/receiver_set.h:382:27
    #12 0x55a47ee12721 in Run base/callback.h:101:12
    #13 0x55a47ee12721 in mojo::InterfaceEndpointClient::NotifyError(base::Optional<mojo::DisconnectReason> const&) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:380:45
    #14 0x55a4807652c1 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::NotifyEndpointOfError(IPC::(anonymous namespace)::ChannelAssociatedGroupController::Endpoint*, bool) ipc/ipc_mojo_bootstrap.cc:783:15
    #15 0x55a480765643 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::NotifyEndpointOfErrorOnEndpointThread(unsigned int, IPC::(anonymous namespace)::ChannelAssociatedGroupController::Endpoint*) ipc/ipc_mojo_bootstrap.cc:803:5
    #16 0x55a47d447dd0 in Run base/callback.h:101:12
    #17 0x55a47d447dd0 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:163:33
    #18 0x55a47d482977 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:351:25
    #19 0x55a47d4821a4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:264:36
    #20 0x55a47d347459 in HandleDispatch base/message_loop/message_pump_glib.cc:374:46
    #21 0x55a47d347459 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:124:43
    #22 0x7f0741396e6a in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x51e6a)

previously allocated by thread T0 (chrome) here:
    #0 0x55a470d6105d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x55a4769c97ba in make_unique<content::ServiceWorkerContainerHost, base::WeakPtr<content::ServiceWorkerContextCore>, bool &, mojo::PendingAssociatedRemote<blink::mojom::ServiceWorkerContainer>, int &> buildtools/third_party/libc++/trunk/include/memory:2006:28
    #2 0x55a4769c97ba in content::ServiceWorkerContextCore::CreateContainerHostForWindow(mojo::PendingAssociatedReceiver<blink::mojom::ServiceWorkerContainerHost>, bool, mojo::PendingAssociatedRemote<blink::mojom::ServiceWorkerContainer>, int) content/browser/service_worker/service_worker_context_core.cc:416:25
    #3 0x55a476a6eaf4 in content::ServiceWorkerMainResourceLoaderInterceptor::MaybeCreateLoader(network::ResourceRequest const&, content::BrowserContext*, base::OnceCallback<void (scoped_refptr<network::SharedURLLoaderFactory>)>, base::OnceCallback<void (bool)>) content/browser/service_worker/service_worker_main_resource_loader_interceptor.cc:154:38
    #4 0x55a4762888ac in content::NavigationURLLoaderImpl::MaybeStartLoader(content::NavigationLoaderInterceptor*, scoped_refptr<network::SharedURLLoaderFactory>) content/browser/loader/navigation_url_loader_impl.cc:546:23
    #5 0x55a4762874fd in content::NavigationURLLoaderImpl::Restart() content/browser/loader/navigation_url_loader_impl.cc:483:3
    #6 0x55a476284ec1 in content::NavigationURLLoaderImpl::Start(scoped_refptr<network::SharedURLLoaderFactory>, content::AppCacheNavigationHandle*, scoped_refptr<content::PrefetchedSignedExchangeCache>, scoped_refptr<content::SignedExchangePrefetchMetricRecorder>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, bool) content/browser/loader/navigation_url_loader_impl.cc:392:3
    #7 0x55a476295d03 in content::NavigationURLLoaderImpl::NavigationURLLoaderImpl(content::BrowserContext*, content::StoragePartition*, std::__1::unique_ptr<content::NavigationRequestInfo, std::__1::default_delete<content::NavigationRequestInfo> >, std::__1::unique_ptr<content::NavigationUIData, std::__1::default_delete<content::NavigationUIData> >, content::ServiceWorkerMainResourceHandle*, content::AppCacheNavigationHandle*, scoped_refptr<content::PrefetchedSignedExchangeCache>, content::NavigationURLLoaderDelegate*, mojo::PendingRemote<network::mojom::CookieAccessObserver>, mojo::PendingRemote<network::mojom::AuthenticationAndCertificateObserver>, std::__1::vector<std::__1::unique_ptr<content::NavigationLoaderInterceptor, std::__1::default_delete<content::NavigationLoaderInterceptor> >, std::__1::allocator<std::__1::unique_ptr<content::NavigationLoaderInterceptor, std::__1::default_delete<content::NavigationLoaderInterceptor> > > >) content/browser/loader/navigation_url_loader_impl.cc:1244:3
    #8 0x55a476282d0b in std::__1::__unique_if<content::NavigationURLLoaderImpl>::__unique_single std::__1::make_unique<content::NavigationURLLoaderImpl, content::BrowserContext*&, content::StoragePartition*&, std::__1::unique_ptr<content::NavigationRequestInfo, std::__1::default_delete<content::NavigationRequestInfo> >, std::__1::unique_ptr<content::NavigationUIData, std::__1::default_delete<content::NavigationUIData> >, content::ServiceWorkerMainResourceHandle*&, content::AppCacheNavigationHandle*&, scoped_refptr<content::PrefetchedSignedExchangeCache>, content::NavigationURLLoaderDelegate*&, mojo::PendingRemote<network::mojom::CookieAccessObserver>, mojo::PendingRemote<network::mojom::AuthenticationAndCertificateObserver>, std::__1::vector<std::__1::unique_ptr<content::NavigationLoaderInterceptor, std::__1::default_delete<content::NavigationLoaderInterceptor> >, std::__1::allocator<std::__1::unique_ptr<content::NavigationLoaderInterceptor, std::__1::default_delete<content::NavigationLoaderInterceptor> > > > >(content::BrowserContext*&, content::StoragePartition*&, std::__1::unique_ptr<content::NavigationRequestInfo, std::__1::default_delete<content::NavigationRequestInfo> >&&, std::__1::unique_ptr<content::NavigationUIData, std::__1::default_delete<content::NavigationUIData> >&&, content::ServiceWorkerMainResourceHandle*&, content::AppCacheNavigationHandle*&, scoped_refptr<content::PrefetchedSignedExchangeCache>&&, content::NavigationURLLoaderDelegate*&, mojo::PendingRemote<network::mojom::CookieAccessObserver>&&, mojo::PendingRemote<network::mojom::AuthenticationAndCertificateObserver>&&, std::__1::vector<std::__1::unique_ptr<content::NavigationLoaderInterceptor, std::__1::default_delete<content::NavigationLoaderInterceptor> >, std::__1::allocator<std::__1::unique_ptr<content::NavigationLoaderInterceptor, std::__1::default_delete<content::NavigationLoaderInterceptor> > > >&&) buildtools/third_party/libc++/trunk/include/memory:2006:32
    #9 0x55a47628284b in content::NavigationURLLoader::Create(content::BrowserContext*, content::StoragePartition*, std::__1::unique_ptr<content::NavigationRequestInfo, std::__1::default_delete<content::NavigationRequestInfo> >, std::__1::unique_ptr<content::NavigationUIData, std::__1::default_delete<content::NavigationUIData> >, content::ServiceWorkerMainResourceHandle*, content::AppCacheNavigationHandle*, scoped_refptr<content::PrefetchedSignedExchangeCache>, content::NavigationURLLoaderDelegate*, content::NavigationURLLoader::LoaderType, mojo::PendingRemote<network::mojom::CookieAccessObserver>, mojo::PendingRemote<network::mojom::AuthenticationAndCertificateObserver>, std::__1::vector<std::__1::unique_ptr<content::NavigationLoaderInterceptor, std::__1::default_delete<content::NavigationLoaderInterceptor> >, std::__1::allocator<std::__1::unique_ptr<content::NavigationLoaderInterceptor, std::__1::default_delete<content::NavigationLoaderInterceptor> > > >) content/browser/loader/navigation_url_loader.cc:49:10
    #10 0x55a4766ede93 in content::NavigationRequest::OnStartChecksComplete(content::NavigationThrottle::ThrottleCheckResult) content/browser/renderer_host/navigation_request.cc:3125:13
    #11 0x55a4766f68ce in content::NavigationRequest::OnWillStartRequestProcessed(content::NavigationThrottle::ThrottleCheckResult) content/browser/renderer_host/navigation_request.cc:4261:3
    #12 0x55a4766f65e4 in content::NavigationRequest::OnNavigationEventProcessed(content::NavigationThrottleRunner::Event, content::NavigationThrottle::ThrottleCheckResult) content/browser/renderer_host/navigation_request.cc:4231:7
    #13 0x55a476717443 in InformDelegate content/browser/renderer_host/navigation_throttle_runner.cc:214:14
    #14 0x55a476717443 in content::NavigationThrottleRunner::ProcessInternal() content/browser/renderer_host/navigation_throttle_runner.cc:203:3
    #15 0x55a4766df3e9 in content::NavigationRequest::WillStartRequest() content/browser/renderer_host/navigation_request.cc:4464:21
    #16 0x55a4766d3150 in content::NavigationRequest::BeginNavigation() content/browser/renderer_host/navigation_request.cc:1629:3
    #17 0x55a47671f683 in content::Navigator::Navigate(std::__1::unique_ptr<content::NavigationRequest, std::__1::default_delete<content::NavigationRequest> >, content::ReloadType) content/browser/renderer_host/navigator.cc:558:44
    #18 0x55a4766823de in content::NavigationControllerImpl::NavigateWithoutEntry(content::NavigationController::LoadURLParams const&) content/browser/renderer_host/navigation_controller_impl.cc:3163:21
    #19 0x55a476681a04 in content::NavigationControllerImpl::LoadURLWithParams(content::NavigationController::LoadURLParams const&) content/browser/renderer_host/navigation_controller_impl.cc:1042:3
    #20 0x55a4884013fd in (anonymous namespace)::LoadURLInContents(content::WebContents*, GURL const&, NavigateParams*) chrome/browser/ui/browser_navigator.cc:385:36
    #21 0x55a4883fed6a in Navigate(NavigateParams*) chrome/browser/ui/browser_navigator.cc:660:7
    #22 0x55a4884e9784 in StartupBrowserCreatorImpl::OpenTabsInBrowser(Browser*, bool, std::__1::vector<StartupTab, std::__1::allocator<StartupTab> > const&) chrome/browser/ui/startup/startup_browser_creator_impl.cc:273:5
    #23 0x55a4884ebdc7 in StartupBrowserCreatorImpl::RestoreOrCreateBrowser(std::__1::vector<StartupTab, std::__1::allocator<StartupTab> > const&, StartupBrowserCreatorImpl::BrowserOpenBehavior, unsigned int, bool, bool) chrome/browser/ui/startup/startup_browser_creator_impl.cc:521:13
    #24 0x55a4884e890e in StartupBrowserCreatorImpl::DetermineURLsAndLaunch(bool, std::__1::vector<GURL, std::__1::allocator<GURL> > const&) chrome/browser/ui/startup/startup_browser_creator_impl.cc:385:22
    #25 0x55a4884e7cf1 in StartupBrowserCreatorImpl::Launch(Profile*, std::__1::vector<GURL, std::__1::allocator<GURL> > const&, bool, std::__1::unique_ptr<LaunchModeRecorder, std::__1::default_delete<LaunchModeRecorder> >) chrome/browser/ui/startup/startup_browser_creator_impl.cc:186:3
    #26 0x55a4884dbbd8 in StartupBrowserCreator::LaunchBrowser(base::CommandLine const&, Profile*, base::FilePath const&, chrome::startup::IsProcessStartup, chrome::startup::IsFirstRun, std::__1::unique_ptr<LaunchModeRecorder, std::__1::default_delete<LaunchModeRecorder> >) chrome/browser/ui/startup/startup_browser_creator.cc:519:13
    #27 0x55a4884e392d in StartupBrowserCreator::ProcessLastOpenedProfiles(base::CommandLine const&, base::FilePath const&, chrome::startup::IsProcessStartup, chrome::startup::IsFirstRun, Profile*, std::__1::vector<Profile*, std::__1::allocator<Profile*> > const&) chrome/browser/ui/startup/startup_browser_creator.cc:1052:10
    #28 0x55a4884e3292 in StartupBrowserCreator::LaunchBrowserForLastProfiles(base::CommandLine const&, base::FilePath const&, bool, Profile*, std::__1::vector<Profile*, std::__1::allocator<Profile*> > const&) chrome/browser/ui/startup/startup_browser_creator.cc:1002:10
    #29 0x55a4884db250 in StartupBrowserCreator::ProcessCmdLineImpl(base::CommandLine const&, base::FilePath const&, bool, Profile*, std::__1::vector<Profile*, std::__1::allocator<Profile*> > const&) chrome/browser/ui/startup/startup_browser_creator.cc:921:10
    #30 0x55a4884d98d2 in StartupBrowserCreator::Start(base::CommandLine const&, base::FilePath const&, Profile*, std::__1::vector<Profile*, std::__1::allocator<Profile*> > const&) chrome/browser/ui/startup/startup_browser_creator.cc:471:10
    #31 0x55a47de9ae76 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl() chrome/browser/chrome_browser_main.cc:1638:25

SUMMARY: AddressSanitizer: heap-use-after-free content/browser/service_worker/service_worker_container_host.cc:1090:29 in content::ServiceWorkerContainerHost::EvictFromBackForwardCache(content::BackForwardCacheMetrics::NotRestoredReason)
Shadow bytes around the buggy address:
  0x0c32800d84f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c32800d8500: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c32800d8510: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c32800d8520: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c32800d8530: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0c32800d8540: fd fd fd fd fd fd fd fd fd fd fd[fd]fd fd fd fa
  0x0c32800d8550: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c32800d8560: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c32800d8570: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c32800d8580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c32800d8590: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
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
==375787==ABORTING


### ad...@google.com (2021-05-26)

+benmason@ - This appears to be a genuinely Critical bug, in BFCache. Can we disable BFCache via a Finch kill switch until we have a fix? Otherwise we will need to crank out a special M91 release to accommodate the fix here within the next few days, though probably just for Android (I believe BFCache isn't launching on desktop till M92).

### fa...@chromium.org (2021-05-26)

+fergal also for the Q of disabling bfcache.

### fe...@google.com (2021-05-26)

We can disable it via finch if that's required. Let me know and I will put send a CL.

### ra...@chromium.org (2021-05-26)

We should probably revert crrev.com/c/2904426 as well, which enables bfcache by default on Android?

### as...@chromium.org (2021-05-26)

I think this will be fixed by something like

```
if (!base::Contains(controllee_map_, client_uuid) && !base::Contains(bfcached_controllee_map_, client_uuid))
  return;

controllee_map_.erase(client_uuid);
bfcached_controllee_map_.erase(client_uuid);
```

We may have other places to be fixed by adding/erasing a client from `bfcached_controllee_map_`.

### al...@chromium.org (2021-05-26)

Thanks for the report and for coming up with a fix!  

+1 to disabling bfcache for now — it's only enabled via Finch, so it should be easy. We have flipped the flag to enabling-by-default just a few days ago (after the M92 branch), so I think that crrev.com/c/2904426 can probably stay for now if we think that the fix is close.

### ha...@chromium.org (2021-05-26)

I'm okay with disabling BFcache as long as we can land the fix and enable it asap.

asamidoi: Thanks for working on this!


### as...@chromium.org (2021-05-26)

I'm trying to reproduce this issue to fix in my environment (93.0.4523.0 (Developer Build) (64-bit)), but I can't.

1. build chrome with `is_asan = true` by `gn args`.
2. Setup a HTTPServer with poc directory attached at the description.
3. execute $ ./out/Asan/chrome --enable-features=BackForwardCache http://localhost:8000/foo/a.html | tools/valgrind/asan/asan_symbolize.py
commented at c#6.
4. click "Click me" in foo/a.html

The above process do not show anything. Am I missing something?

### ra...@chromium.org (2021-05-26)

Not sure if the previous page needs to be actually cached, if so since it's a same-site navigation you'd need to enable same-site BFCache with --enable-features=BackForwardCache:enable_same_site/true (or change the code here https://source.chromium.org/chromium/chromium/src/+/main:content/common/content_navigation_policy.cc;l=74;drc=9013bf7765d7febaa58224542782307fa952ac14) 

### jt...@gmail.com (2021-05-26)

I would like to add that if you want to reproduce the issue for multiple times, make sure that there is no service worker registered before clicking "Click me". This can be done by unregistering in developer tools and reloading the page, or just deleting  the user data directory if it is for test purpose only.

### ha...@chromium.org (2021-05-26)

[Empty comment from Monorail migration]

### fa...@chromium.org (2021-05-26)

[Empty comment from Monorail migration]

### fe...@google.com (2021-05-26)

Finch change to disable bfcache has been submitted as http://cl/375943715 .

### [Deleted User] (2021-05-26)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-26)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-26)

Setting Pri-0 to match security severity Critical. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2021-05-26)

[Empty comment from Monorail migration]

### go...@google.com (2021-05-27)

+adetaylor@ (Security TPM) as we started shipping M91 to Stable.

### as...@chromium.org (2021-05-27)

I'm still struggled to repro UAF but I created a CL based on code reading and ASAN log in this issue.
https://chromium-review.googlesource.com/c/chromium/src/+/2919020

Can someone help me to confirm the CL fixes UAF?

### ad...@google.com (2021-05-27)

vakh@, since you were able to reproduce the problem would you be kind enough to see if https://crbug.com/chromium/1212618#c25 fixes it? Otherwise I'll have a go at getting the POC running myself.

### fa...@chromium.org (2021-05-27)

I tried to make a glitch with the repro but have not been able to repro: https://sideways-harvest-sidecar.glitch.me/foo/a.html

For those who can repro it, does the repro happen on the glitch site?

vakh: Where can I download builds/asan-linux-release-857950-90.0.4430.212-Stable/ from?

### fa...@chromium.org (2021-05-27)

I got it to repro on ToT asan build with this:

$ out/asan/chrome --enable-features=BackForwardCache:enable_same_site/true --user-data-dir=/tmp/bbb https://sideways-harvest-sidecar.glitch.me/foo/a.html | tools/valgrind/asan/asan_symbolize.py

### as...@chromium.org (2021-05-27)

I can repro it too. I'll check if my CL fixes UAF.

### as...@chromium.org (2021-05-27)

I confirmed this CL fixes the UAF issue. This is being merged to the latest branch.
https://chromium-review.googlesource.com/c/chromium/src/+/2919020

I'll add a browser test next week to confirm the issue is actually fixed and to make sure changes in the future do not break it again.

### gi...@appspot.gserviceaccount.com (2021-05-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a2414a05a486ca0ad18ba4caf78e883a668a0555

commit a2414a05a486ca0ad18ba4caf78e883a668a0555
Author: Asami Doi <asamidoi@chromium.org>
Date: Thu May 27 11:19:58 2021

BFCache: remove a controllee stored in `bfcached_controllee_map_`

This CL fixes the UAF that happens with the following case:
Let's assume we have 2 service workers (sw1.js and sw2.js) are
registered in the same page. When the second service worker (sw2.js) is
registered, ServiceWorkerContainerHost::UpdateController() is called
and the previous SWVersion (sw1.js) removes a controllee from
`controllee_map_`. If BackForwardCache is enabled, a controllee is
stored in `bfcached_controllee_map_` instead and the controllee will
not be removed in ServiceWorkerContainerHost::UpdateController().
When ServiceWorkerContainerHost::UpdateController() is called and
keep a controllee in `bfcached_controllee_map_`, and a page navigates to
a different page (evicts BFCache), use-after-free (UAF) happens.

This CL updates ServiceWorkerContainerHost::UpdateController()
to remove a controllee from `bfcached_controllee_map_` if it exists.

Bug: 1212618
Change-Id: I13e023e6d273268a08ea9276a056f7f5acba39cd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2919020
Commit-Queue: Asami Doi <asamidoi@chromium.org>
Reviewed-by: Matt Falkenhagen <falken@chromium.org>
Cr-Commit-Position: refs/heads/master@{#887109}

[modify] https://crrev.com/a2414a05a486ca0ad18ba4caf78e883a668a0555/content/browser/service_worker/service_worker_container_host.cc
[modify] https://crrev.com/a2414a05a486ca0ad18ba4caf78e883a668a0555/content/browser/service_worker/service_worker_version.cc
[modify] https://crrev.com/a2414a05a486ca0ad18ba4caf78e883a668a0555/content/browser/service_worker/service_worker_version.h


### sr...@google.com (2021-05-27)

has this been verified and ready for Merge to M92? if so please add the merge request label and get the merge ready for branch:4515 asap

### ad...@chromium.org (2021-05-27)

Yep. Better still, mark it as Fixed so that Sheriffbot can add the right merge labels:
https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/security-labels.md#TOC-Merge-labels

### fe...@google.com (2021-05-31)

Closing this.

I have filed https://crbug.com/1214665 to track adding a browsertest.

### fe...@google.com (2021-05-31)

[Empty comment from Monorail migration]

### fe...@google.com (2021-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-31)

This bug requires manual review: Request affecting a post-stable build
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

### as...@chromium.org (2021-05-31)

[Empty comment from Monorail migration]

### as...@chromium.org (2021-05-31)

[Empty comment from Monorail migration]

### fe...@google.com (2021-05-31)

Here are the details for M91


1. Does your merge fit within the Merge Decision Guidelines?

Unclear. BFCache will have to remain disabled for M91 if we do not CP.

2. Links to the CLs you are requesting to merge.

https://chromium-review.googlesource.com/c/chromium/src/+/2919020

3. Has the change landed and been verified on ToT?

Yes

4. Does this change need to be merged into other active release branches (M-1, M+1)?

M92

5. Why are these changes required in this milestone after branch?

Without them BFCache must be disabled. This disrupts search experiments and also hurts latency.

6. Is this a new feature?


No.

7. If it is a new feature, is it behind a flag using finch?

It is behind a flag


### [Deleted User] (2021-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-31)

[Empty comment from Monorail migration]

### as...@chromium.org (2021-06-01)

Here is the cherry-picked CLs for M92 and M91.

M92: https://chromium-review.googlesource.com/c/chromium/src/+/2929616
M91: https://chromium-review.googlesource.com/c/chromium/src/+/2929401

### [Deleted User] (2021-06-01)

Your change meets the bar and is auto-approved for M92. Please go ahead and merge the CL to branch 4515 (refs/branch-heads/4515) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-06-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/be8d69148374f5f315b39e69d04cfe58946cc9a4

commit be8d69148374f5f315b39e69d04cfe58946cc9a4
Author: Asami Doi <asamidoi@chromium.org>
Date: Tue Jun 01 06:51:57 2021

[M92] BFCache: remove a controllee stored in `bfcached_controllee_map_`

This CL fixes the UAF that happens with the following case:
Let's assume we have 2 service workers (sw1.js and sw2.js) are
registered in the same page. When the second service worker (sw2.js) is
registered, ServiceWorkerContainerHost::UpdateController() is called
and the previous SWVersion (sw1.js) removes a controllee from
`controllee_map_`. If BackForwardCache is enabled, a controllee is
stored in `bfcached_controllee_map_` instead and the controllee will
not be removed in ServiceWorkerContainerHost::UpdateController().
When ServiceWorkerContainerHost::UpdateController() is called and
keep a controllee in `bfcached_controllee_map_`, and a page navigates to
a different page (evicts BFCache), use-after-free (UAF) happens.

This CL updates ServiceWorkerContainerHost::UpdateController()
to remove a controllee from `bfcached_controllee_map_` if it exists.

(cherry picked from commit a2414a05a486ca0ad18ba4caf78e883a668a0555)

Bug: 1212618
Change-Id: I13e023e6d273268a08ea9276a056f7f5acba39cd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2919020
Commit-Queue: Asami Doi <asamidoi@chromium.org>
Reviewed-by: Matt Falkenhagen <falken@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#887109}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2929616
Cr-Commit-Position: refs/branch-heads/4515@{#181}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/be8d69148374f5f315b39e69d04cfe58946cc9a4/content/browser/service_worker/service_worker_container_host.cc
[modify] https://crrev.com/be8d69148374f5f315b39e69d04cfe58946cc9a4/content/browser/service_worker/service_worker_version.cc
[modify] https://crrev.com/be8d69148374f5f315b39e69d04cfe58946cc9a4/content/browser/service_worker/service_worker_version.h


### ad...@google.com (2021-06-01)

Approving merge to M91, branch 4472, assuming no problems showed up in Canary over the weekend.

### gi...@appspot.gserviceaccount.com (2021-06-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7cd7f6741fc4491c2f7ef21052a370ee23887e37

commit 7cd7f6741fc4491c2f7ef21052a370ee23887e37
Author: Asami Doi <asamidoi@chromium.org>
Date: Tue Jun 01 17:45:57 2021

[M91] BFCache: remove a controllee stored in `bfcached_controllee_map_`

This CL fixes the UAF that happens with the following case:
Let's assume we have 2 service workers (sw1.js and sw2.js) are
registered in the same page. When the second service worker (sw2.js) is
registered, ServiceWorkerContainerHost::UpdateController() is called
and the previous SWVersion (sw1.js) removes a controllee from
`controllee_map_`. If BackForwardCache is enabled, a controllee is
stored in `bfcached_controllee_map_` instead and the controllee will
not be removed in ServiceWorkerContainerHost::UpdateController().
When ServiceWorkerContainerHost::UpdateController() is called and
keep a controllee in `bfcached_controllee_map_`, and a page navigates to
a different page (evicts BFCache), use-after-free (UAF) happens.

This CL updates ServiceWorkerContainerHost::UpdateController()
to remove a controllee from `bfcached_controllee_map_` if it exists.

(cherry picked from commit a2414a05a486ca0ad18ba4caf78e883a668a0555)

Bug: 1212618
Change-Id: I13e023e6d273268a08ea9276a056f7f5acba39cd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2919020
Commit-Queue: Asami Doi <asamidoi@chromium.org>
Reviewed-by: Matt Falkenhagen <falken@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#887109}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2929401
Reviewed-by: Krishna Govind <govind@chromium.org>
Reviewed-by: Ben Mason <benmason@chromium.org>
Reviewed-by: Prudhvi Kumar Bommana <pbommana@google.com>
Commit-Queue: Krishna Govind <govind@chromium.org>
Owners-Override: Krishna Govind <govind@chromium.org>
Cr-Commit-Position: refs/branch-heads/4472@{#1375}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/7cd7f6741fc4491c2f7ef21052a370ee23887e37/content/browser/service_worker/service_worker_container_host.cc
[modify] https://crrev.com/7cd7f6741fc4491c2f7ef21052a370ee23887e37/content/browser/service_worker/service_worker_version.cc
[modify] https://crrev.com/7cd7f6741fc4491c2f7ef21052a370ee23887e37/content/browser/service_worker/service_worker_version.h


### va...@chromium.org (2021-06-01)

Re https://crbug.com/chromium/1212618#c26 by adetaylor@google.com:
> vakh@, since you were able to reproduce the problem would you be kind enough to see if https://crbug.com/chromium/1212618#c25 fixes it?

Re https://crbug.com/chromium/1212618#c27 by falken@chromium.org:
> vakh: Where can I download builds/asan-linux-release-857950-90.0.4430.212-Stable/ from?

Sorry, I was OOO so just saw this. Please let me know if you still need help to reproduce the problem or fetching the ASAN build (see go/paste/4934839670145024)

### am...@google.com (2021-06-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-06-02)

Congratulations! The VRP Panel has decided to award you $25,000 for this report. Excellent work and thank you for your help in keeping Chrome users safe from this type of nasty memory safety issue! 

### am...@google.com (2021-06-04)

[Empty comment from Monorail migration]

### dh...@google.com (2021-06-04)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-06-08)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-08)

[Empty comment from Monorail migration]

### vs...@google.com (2021-06-09)

[Empty comment from Monorail migration]

### gi...@google.com (2021-06-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-06-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/34d5af37f9ac64b3d838facf975065a2d6ebd471

commit 34d5af37f9ac64b3d838facf975065a2d6ebd471
Author: Asami Doi <asamidoi@chromium.org>
Date: Thu Jun 10 07:03:17 2021

[M90-LTS] BFCache: remove a controllee stored in `bfcached_controllee_map_`

This CL fixes the UAF that happens with the following case:
Let's assume we have 2 service workers (sw1.js and sw2.js) are
registered in the same page. When the second service worker (sw2.js) is
registered, ServiceWorkerContainerHost::UpdateController() is called
and the previous SWVersion (sw1.js) removes a controllee from
`controllee_map_`. If BackForwardCache is enabled, a controllee is
stored in `bfcached_controllee_map_` instead and the controllee will
not be removed in ServiceWorkerContainerHost::UpdateController().
When ServiceWorkerContainerHost::UpdateController() is called and
keep a controllee in `bfcached_controllee_map_`, and a page navigates to
a different page (evicts BFCache), use-after-free (UAF) happens.

This CL updates ServiceWorkerContainerHost::UpdateController()
to remove a controllee from `bfcached_controllee_map_` if it exists.

(cherry picked from commit a2414a05a486ca0ad18ba4caf78e883a668a0555)

(cherry picked from commit 7cd7f6741fc4491c2f7ef21052a370ee23887e37)

Bug: 1212618
Change-Id: I13e023e6d273268a08ea9276a056f7f5acba39cd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2919020
Commit-Queue: Asami Doi <asamidoi@chromium.org>
Reviewed-by: Matt Falkenhagen <falken@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#887109}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2929401
Reviewed-by: Krishna Govind <govind@chromium.org>
Reviewed-by: Ben Mason <benmason@chromium.org>
Reviewed-by: Prudhvi Kumar Bommana <pbommana@google.com>
Commit-Queue: Krishna Govind <govind@chromium.org>
Owners-Override: Krishna Govind <govind@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4472@{#1375}
Cr-Original-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2944946
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1512}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/34d5af37f9ac64b3d838facf975065a2d6ebd471/content/browser/service_worker/service_worker_container_host.cc
[modify] https://crrev.com/34d5af37f9ac64b3d838facf975065a2d6ebd471/content/browser/service_worker/service_worker_version.cc
[modify] https://crrev.com/34d5af37f9ac64b3d838facf975065a2d6ebd471/content/browser/service_worker/service_worker_version.h


### gi...@appspot.gserviceaccount.com (2021-06-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0e36d324d6ef42ddedf67bdd82001f31a47c994e

commit 0e36d324d6ef42ddedf67bdd82001f31a47c994e
Author: Asami Doi <asamidoi@chromium.org>
Date: Thu Jun 10 07:07:44 2021

[M86-LTS] BFCache: remove a controllee stored in `bfcached_controllee_map_`

This CL fixes the UAF that happens with the following case:
Let's assume we have 2 service workers (sw1.js and sw2.js) are
registered in the same page. When the second service worker (sw2.js) is
registered, ServiceWorkerContainerHost::UpdateController() is called
and the previous SWVersion (sw1.js) removes a controllee from
`controllee_map_`. If BackForwardCache is enabled, a controllee is
stored in `bfcached_controllee_map_` instead and the controllee will
not be removed in ServiceWorkerContainerHost::UpdateController().
When ServiceWorkerContainerHost::UpdateController() is called and
keep a controllee in `bfcached_controllee_map_`, and a page navigates to
a different page (evicts BFCache), use-after-free (UAF) happens.

This CL updates ServiceWorkerContainerHost::UpdateController()
to remove a controllee from `bfcached_controllee_map_` if it exists.

(cherry picked from commit a2414a05a486ca0ad18ba4caf78e883a668a0555)

(cherry picked from commit 7cd7f6741fc4491c2f7ef21052a370ee23887e37)

Bug: 1212618
Change-Id: I13e023e6d273268a08ea9276a056f7f5acba39cd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2919020
Commit-Queue: Asami Doi <asamidoi@chromium.org>
Reviewed-by: Matt Falkenhagen <falken@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#887109}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2929401
Reviewed-by: Krishna Govind <govind@chromium.org>
Reviewed-by: Ben Mason <benmason@chromium.org>
Reviewed-by: Prudhvi Kumar Bommana <pbommana@google.com>
Commit-Queue: Krishna Govind <govind@chromium.org>
Owners-Override: Krishna Govind <govind@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4472@{#1375}
Cr-Original-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2948660
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1663}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/0e36d324d6ef42ddedf67bdd82001f31a47c994e/content/browser/service_worker/service_worker_container_host.cc
[modify] https://crrev.com/0e36d324d6ef42ddedf67bdd82001f31a47c994e/content/browser/service_worker/service_worker_version.cc
[modify] https://crrev.com/0e36d324d6ef42ddedf67bdd82001f31a47c994e/content/browser/service_worker/service_worker_version.h


### vs...@google.com (2021-06-10)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-15)

[Empty comment from Monorail migration]

### dh...@google.com (2021-07-02)

[Empty comment from Monorail migration]

### dh...@google.com (2021-07-02)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-07-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1212618?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>ServiceWorker, UI>Browser>Navigation>BFCache]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055982)*
