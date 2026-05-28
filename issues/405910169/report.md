# UAF in in BrowserTabStripTracker::Init() in browser process

| Field | Value |
|-------|-------|
| **Issue ID** | [405910169](https://issues.chromium.org/issues/405910169) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | et...@google.com |
| **Created** | 2025-03-24 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS
The crash occurs in BrowserTabStripTracker::Init() when trying to access a Browser pointer that has been freed.This is a race condition during browser startup.

VERSION
Chromium	136.0.7088.0 (Developer Build) (64-bit) 
OS	Linux

REPRODUCTION CASE
1. Download the latest asan build:
gs://chromium-browser-asan/linux-release/asan-linux-release-1436703.zip
2. run the command:
./chrome  --user-data-dir=/tmp/test  --auto-open-devtools-for-tabs --load-extension="extension1,extension2" 

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [browser,]

=================================================================
==1490314==ERROR: AddressSanitizer: heap-use-after-free on address 0x7bf446f20bf8 at pc 0x562621e6acb8 bp 0x7ffea6335010 sp 0x7ffea6335008
READ of size 8 at 0x7bf446f20bf8 thread T0 (chrome)
==1490314==WARNING: invalid path to external symbolizer!
==1490314==WARNING: Failed to use and restart external symbolizer!
    #0 0x562621e6acb7 in GetForExtraction ./../../base/allocator/partition_allocator/src/partition_alloc/pointers/raw_ptr.h:1002:47
    #1 0x562621e6acb7 in operator Browser * ./../../base/allocator/partition_allocator/src/partition_alloc/pointers/raw_ptr.h:670:59
    #2 0x562621e6acb7 in BrowserTabStripTracker::Init() ./../../chrome/browser/ui/browser_tab_strip_tracker.cc:36:25
    #3 0x56260b093f6a in make_unique<DevToolsAutoOpener, 0> ./../../third_party/libc++/src/include/__memory/unique_ptr.h:754:30
    #4 0x56260b093f6a in BrowserProcessImpl::CreateDevToolsAutoOpener() ./../../chrome/browser/browser_process_impl.cc:957:29
    #5 0x56260b0d46d9 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl() ./../../chrome/browser/chrome_browser_main.cc:1562:24
    #6 0x56260b0d371c in ChromeBrowserMainParts::PreMainMessageLoopRun() ./../../chrome/browser/chrome_browser_main.cc:1158:18
    #7 0x562601f65c7c in content::BrowserMainLoop::PreMainMessageLoopRun() ./../../content/browser/browser_main_loop.cc:1005:28
    #8 0x562601f6cf53 in Invoke<int (content::BrowserMainLoop::*)(), content::BrowserMainLoop *> ./../../base/functional/bind_internal.h:731:12
    #9 0x562601f6cf53 in MakeItSo<int (content::BrowserMainLoop::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<content::BrowserMainLoop, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > ./../../base/functional/bind_internal.h:923:12
    #10 0x562601f6cf53 in RunImpl<int (content::BrowserMainLoop::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<content::BrowserMainLoop, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> ./../../base/functional/bind_internal.h:1060:14
    #11 0x562601f6cf53 in base::internal::Invoker<base::internal::FunctorTraits<int (content::BrowserMainLoop::*&&)(), content::BrowserMainLoop*>, base::internal::BindState<true, true, false, int (content::BrowserMainLoop::*)(), base::internal::UnretainedWrapper<content::BrowserMainLoop, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, int ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:973:12
    #12 0x562603a9d69b in Run ./../../base/functional/callback.h:156:12
    #13 0x562603a9d69b in content::StartupTaskRunner::RunAllTasksNow() ./../../content/browser/startup_task_runner.cc:42:29
    #14 0x562601f64aad in content::BrowserMainLoop::CreateStartupTasks() ./../../content/browser/browser_main_loop.cc:911:25
    #15 0x562601f702d3 in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams) ./../../content/browser/browser_main_runner_impl.cc:137:15
    #16 0x562601f5f2c3 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser_main.cc:28:32
    #17 0x56260938493c in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:717:10
    #18 0x5626093880cf in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content_main_runner_impl.cc:1297:10
    #19 0x5626093877b6 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1152:12
    #20 0x562609381d4b in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:359:36
    #21 0x56260938226b in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:372:10
    #22 0x5625f6f2c79f in ChromeMain ./../../chrome/app/chrome_main.cc:222:12
    #23 0x7fd4481b7082 in __libc_start_main /build/glibc-FcRMwW/glibc-2.31/csu/../csu/libc-start.c:308:16

0x7bf446f20bf8 is located 8 bytes inside of 16-byte region [0x7bf446f20bf0,0x7bf446f20c00)
freed by thread T0 (chrome) here:
    #0 0x5625f6f2b6ed in operator delete(void*) _asan_rtl_:3
    #1 0x562608d429ef in __libcpp_operator_delete<base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1> *> ./../../third_party/libc++/src/include/__new/allocate.h:46:3
    #2 0x562608d429ef in __libcpp_deallocate<base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1> > ./../../third_party/libc++/src/include/__new/allocate.h:86:12
    #3 0x562608d429ef in deallocate ./../../third_party/libc++/src/include/__memory/allocator.h:120:7
    #4 0x562608d429ef in deallocate ./../../third_party/libc++/src/include/__memory/allocator_traits.h:302:9
    #5 0x562608d429ef in ~__split_buffer ./../../third_party/libc++/src/include/__split_buffer:337:5
    #6 0x562608d429ef in base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1>* std::__Cr::vector<base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1>, std::__Cr::allocator<base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1>>>::__emplace_back_slow_path<base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1>>(base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1>&&) ./../../third_party/libc++/src/include/__vector/vector.h:1142:1
    #7 0x562608d38b60 in emplace_back<base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1> > ./../../third_party/libc++/src/include/__vector/vector.h:1158:13
    #8 0x562608d38b60 in push_back ./../../third_party/libc++/src/include/__vector/vector.h:452:90
    #9 0x562608d38b60 in BrowserList::AddBrowser(Browser*) ./../../chrome/browser/ui/browser_list.cc:89:28
    #10 0x562621dec535 in Browser::Browser(Browser::CreateParams const&) ./../../chrome/browser/ui/browser.cc:697:3
    #11 0x562621dea839 in Browser::Create(Browser::CreateParams const&) ./../../chrome/browser/ui/browser.cc:562:14
    #12 0x562618589af4 in DevToolsWindow::CreateDevToolsBrowser() ./../../chrome/browser/devtools/devtools_window.cc:1817:7
    #13 0x56261858846d in DevToolsWindow::Show(DevToolsToggleAction const&) ./../../chrome/browser/devtools/devtools_window.cc:1001:5
    #14 0x5626185851de in ScheduleShow ./../../chrome/browser/devtools/devtools_window.cc:942:5
    #15 0x5626185851de in DevToolsWindow::ToggleDevToolsWindow(content::WebContents*, Profile*, bool, DevToolsToggleAction const&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, DevToolsOpenedByAction) ./../../chrome/browser/devtools/devtools_window.cc:846:13
    #16 0x562618584689 in DevToolsWindow::OpenDevToolsWindow(content::WebContents*, DevToolsOpenedByAction) ./../../chrome/browser/devtools/devtools_window.cc:616:3
    #17 0x5626186be442 in DevToolsAutoOpener::OnTabStripModelChanged(TabStripModel*, TabStripModelChange const&, TabStripSelectionChange const&) ./../../chrome/browser/devtools/devtools_auto_opener.cc:26:7
    #18 0x562621e6b249 in BrowserTabStripTracker::MaybeTrackBrowser(Browser*) ./../../chrome/browser/ui/browser_tab_strip_tracker.cc:62:30
    #19 0x562621e6aba9 in BrowserTabStripTracker::Init() ./../../chrome/browser/ui/browser_tab_strip_tracker.cc:37:5
    #20 0x56260b093f6a in make_unique<DevToolsAutoOpener, 0> ./../../third_party/libc++/src/include/__memory/unique_ptr.h:754:30
    #21 0x56260b093f6a in BrowserProcessImpl::CreateDevToolsAutoOpener() ./../../chrome/browser/browser_process_impl.cc:957:29
    #22 0x56260b0d46d9 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl() ./../../chrome/browser/chrome_browser_main.cc:1562:24
    #23 0x56260b0d371c in ChromeBrowserMainParts::PreMainMessageLoopRun() ./../../chrome/browser/chrome_browser_main.cc:1158:18
    #24 0x562601f65c7c in content::BrowserMainLoop::PreMainMessageLoopRun() ./../../content/browser/browser_main_loop.cc:1005:28
    #25 0x562601f6cf53 in Invoke<int (content::BrowserMainLoop::*)(), content::BrowserMainLoop *> ./../../base/functional/bind_internal.h:731:12
    #26 0x562601f6cf53 in MakeItSo<int (content::BrowserMainLoop::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<content::BrowserMainLoop, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > ./../../base/functional/bind_internal.h:923:12
    #27 0x562601f6cf53 in RunImpl<int (content::BrowserMainLoop::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<content::BrowserMainLoop, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> ./../../base/functional/bind_internal.h:1060:14
    #28 0x562601f6cf53 in base::internal::Invoker<base::internal::FunctorTraits<int (content::BrowserMainLoop::*&&)(), content::BrowserMainLoop*>, base::internal::BindState<true, true, false, int (content::BrowserMainLoop::*)(), base::internal::UnretainedWrapper<content::BrowserMainLoop, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, int ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:973:12
    #29 0x562603a9d69b in Run ./../../base/functional/callback.h:156:12
    #30 0x562603a9d69b in content::StartupTaskRunner::RunAllTasksNow() ./../../content/browser/startup_task_runner.cc:42:29
    #31 0x562601f64aad in content::BrowserMainLoop::CreateStartupTasks() ./../../content/browser/browser_main_loop.cc:911:25
    #32 0x562601f702d3 in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams) ./../../content/browser/browser_main_runner_impl.cc:137:15
    #33 0x562601f5f2c3 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser_main.cc:28:32
    #34 0x56260938493c in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:717:10
    #35 0x5626093880cf in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content_main_runner_impl.cc:1297:10
    #36 0x5626093877b6 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1152:12
    #37 0x562609381d4b in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:359:36
    #38 0x56260938226b in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:372:10
    #39 0x5625f6f2c79f in ChromeMain ./../../chrome/app/chrome_main.cc:222:12
    #40 0x7fd4481b7082 in __libc_start_main /build/glibc-FcRMwW/glibc-2.31/csu/../csu/libc-start.c:308:16

previously allocated by thread T0 (chrome) here:
    #0 0x5625f6f2ae8d in operator new(unsigned long) _asan_rtl_:3
    #1 0x562608d428cb in __libcpp_operator_new<unsigned long> ./../../third_party/libc++/src/include/__new/allocate.h:37:10
    #2 0x562608d428cb in __libcpp_allocate<base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1> > ./../../third_party/libc++/src/include/__new/allocate.h:64:28
    #3 0x562608d428cb in allocate ./../../third_party/libc++/src/include/__memory/allocator.h:105:14
    #4 0x562608d428cb in __allocate_at_least<std::__Cr::allocator<base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1> > > ./../../third_party/libc++/src/include/__memory/allocate_at_least.h:41:19
    #5 0x562608d428cb in __split_buffer ./../../third_party/libc++/src/include/__split_buffer:325:25
    #6 0x562608d428cb in base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1>* std::__Cr::vector<base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1>, std::__Cr::allocator<base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1>>>::__emplace_back_slow_path<base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1>>(base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1>&&) ./../../third_party/libc++/src/include/__vector/vector.h:1136:47
    #7 0x562608d38b60 in emplace_back<base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1> > ./../../third_party/libc++/src/include/__vector/vector.h:1158:13
    #8 0x562608d38b60 in push_back ./../../third_party/libc++/src/include/__vector/vector.h:452:90
    #9 0x562608d38b60 in BrowserList::AddBrowser(Browser*) ./../../chrome/browser/ui/browser_list.cc:89:28
    #10 0x562621dec535 in Browser::Browser(Browser::CreateParams const&) ./../../chrome/browser/ui/browser.cc:697:3
    #11 0x562621dea839 in Browser::Create(Browser::CreateParams const&) ./../../chrome/browser/ui/browser.cc:562:14
    #12 0x562621e5d0ba in GetOrCreateBrowser ./../../chrome/browser/ui/browser_navigator.cc:125:15
    #13 0x562621e5d0ba in GetBrowserAndTabForDisposition ./../../chrome/browser/ui/browser_navigator.cc:224:15
    #14 0x562621e5d0ba in Navigate(NavigateParams*) ./../../chrome/browser/ui/browser_navigator.cc:733:13
    #15 0x5626064afc20 in extensions::ExtensionTabUtil::OpenTab(ExtensionFunction*, extensions::ExtensionTabUtil::OpenTabParams const&, bool) ./../../chrome/browser/extensions/extension_tab_util.cc:347:53
    #16 0x5626066d427f in operator() ./../../chrome/browser/extensions/api/tabs/tabs_api.cc:1440:19
    #17 0x5626066d427f in extensions::TabsCreateFunction::Run() ./../../chrome/browser/extensions/api/tabs/tabs_api.cc:1425:21
    #18 0x562604ed1db3 in ExtensionFunction::RunWithValidation() ./../../extensions/browser/extension_function.cc:493:10
    #19 0x562604ee24db in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal(extensions::mojom::RequestParams const&, content::RenderFrameHost*, content::RenderProcessHost&, base::OnceCallback<void (ExtensionFunction::ResponseType, base::ListValue, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, mojo::StructPtr<extensions::mojom::ExtraResponseData>)>) ./../../extensions/browser/extension_function_dispatcher.cc:442:15
    #20 0x562604ee2f22 in extensions::ExtensionFunctionDispatcher::DispatchForServiceWorker(mojo::StructPtr<extensions::mojom::RequestParams>, int, base::OnceCallback<void (bool, base::ListValue, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, mojo::StructPtr<extensions::mojom::ExtraResponseData>)>) ./../../extensions/browser/extension_function_dispatcher.cc:256:3
    #21 0x562605032407 in extensions::ServiceWorkerHost::RequestWorker(mojo::StructPtr<extensions::mojom::RequestParams>, base::OnceCallback<void (bool, base::ListValue, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, mojo::StructPtr<extensions::mojom::ExtraResponseData>)>) ./../../extensions/browser/service_worker/service_worker_host.cc:262:16
    #22 0x5626051e3237 in extensions::mojom::ServiceWorkerHostStubDispatch::AcceptWithResponder(extensions::mojom::ServiceWorkerHost*, mojo::Message*, std::__Cr::unique_ptr<mojo::MessageReceiverWithStatus, std::__Cr::default_delete<mojo::MessageReceiverWithStatus>>) ./gen/extensions/common/mojom/service_worker_host.mojom.cc:1472:13
    #23 0x56260c391040 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1005:56
    #24 0x56260c3ae62a in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #25 0x56260c397404 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:724:20
    #26 0x56260c3be8aa in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:1121:42
    #27 0x56260c3bcaaf in mojo::internal::MultiplexRouter::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:734:7
    #28 0x56260c3ae62a in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #29 0x56260c38822a in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) ./../../mojo/public/cpp/bindings/lib/connector.cc:562:49
    #30 0x56260c3899a0 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:620:14
    #31 0x56260c3893c9 in OnHandleReadyInternal ./../../mojo/public/cpp/bindings/lib/connector.cc:452:3
    #32 0x56260c3893c9 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int) ./../../mojo/public/cpp/bindings/lib/connector.cc:418:3
    #33 0x56260c38b23a in Invoke<void (mojo::Connector::*)(const char *, unsigned int), mojo::Connector *, const char *, unsigned int> ./../../base/functional/bind_internal.h:731:12
    #34 0x56260c38b23a in MakeItSo<void (mojo::Connector::*const &)(const char *, unsigned int), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, unsigned int> ./../../base/functional/bind_internal.h:923:12
    #35 0x56260c38b23a in RunImpl<void (mojo::Connector::*const &)(const char *, unsigned int), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, 0UL, 1UL> ./../../base/functional/bind_internal.h:1060:14
    #36 0x56260c38b23a in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int) ./../../base/functional/bind_internal.h:980:12
    #37 0x5625fc29383e in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & ./../../base/functional/callback.h:344:12
    #38 0x5625fc2935df in Invoke<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind_internal.h:664:12
    #39 0x5625fc2935df in MakeItSo<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind_internal.h:923:12
    #40 0x5625fc2935df in RunImpl<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, 0UL> ./../../base/functional/bind_internal.h:1060:14
    #41 0x5625fc2935df in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) ./../../base/functional/bind_internal.h:980:12
    #42 0x56260d0f4e80 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & ./../../base/functional/callback.h:344:12
    #43 0x56260d0f47c3 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple_watcher.cc:278:14
    #44 0x56260d0f59ed in Invoke<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), const base::WeakPtr<mojo::SimpleWatcher> &, int, unsigned int, mojo::HandleSignalsState> ./../../base/functional/bind_internal.h:731:12
    #45 0x56260d0f59ed in MakeItSo<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> > ./../../base/functional/bind_internal.h:947:5
    #46 0x56260d0f59ed in RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0UL, 1UL, 2UL, 3UL> ./../../base/functional/bind_internal.h:1060:14
    #47 0x56260d0f59ed in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:973:12
    #48 0x56260c5b5f26 in Run ./../../base/functional/callback.h:156:12
    #49 0x56260c5b5f26 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:209:34
    #50 0x56260c6278e8 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:458:11)> ./../../base/task/common/task_annotator.h:106:5
    #51 0x56260c6278e8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:456:23

SUMMARY: AddressSanitizer: heap-use-after-free (/home/kuer/chromium_version/latest_asan/chrome+0x3a653cb7) (BuildId: f621a43ad15648ce)
Shadow bytes around the buggy address:
  0x7bf446f20900: f7 fa 00 fa f7 fa 00 fa f7 fa 00 fa f7 fa 00 fa
  0x7bf446f20980: f7 fa 00 fa f7 fa fd fa f7 fa fd fd f7 fa fd fa
  0x7bf446f20a00: f7 fa fd fa f7 fa fd fa f7 fa fd fd f7 fa fd fa
  0x7bf446f20a80: f7 fa fd fd f7 fa fd fa f7 fa fd fa f7 fa fd fa
  0x7bf446f20b00: f7 fa fd fa f7 fa fd fa f7 fa fd fd f7 fa fd fa
=>0x7bf446f20b80: f7 fa fd fd f7 fa fd fa f7 fa fd fa f7 fa fd[fd]
  0x7bf446f20c00: f7 fa 00 fa f7 fa fd fd f7 fa fd fd f7 fa fd fa
  0x7bf446f20c80: f7 fa fd fd f7 fa fd fd f7 fa 00 fa f7 fa fd fd
  0x7bf446f20d00: f7 fa fd fd f7 fa fd fd f7 fa fd fd f7 fa fd fd
  0x7bf446f20d80: f7 fa fd fd f7 fa fd fd f7 fa 00 fa f7 fa 00 fa
  0x7bf446f20e00: f7 fa 00 fa f7 fa 00 fa f7 fa 00 fa f7 fa 00 fa
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

==1490314==ADDITIONAL INFO

==1490314==Note: Please include this section with the ASan report.
Task trace:


Command line: `/home/kuer/chromium_version/latest_asan/chrome --user-data-dir=/tmp/1adzzzad2z --extensions-on-chrome-urls --auto-open-devtools-for-tabs --load-extension=/home/kuer/Desktop/2025/0324/gnhncnjoiknidcehmaepenfepfmejohi,/home/kuer/Desktop/2025/0324/mjaijefbmmliffhdpdbcjpmjnfkhalkc --flag-switches-begin --flag-switches-end --ozone-platform-hint=auto --ozone-platform=x11 --file-url-path-alias=/gen=/home/kuer/chromium_version/latest_asan/gen http://example.com`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==1490314==END OF ADDITIONAL INFO
==1490314==ABORTING



## Attachments

- [extension1.zip](attachments/extension1.zip) (application/zip, 1.2 KB)
- [extension2.zip](attachments/extension2.zip) (application/zip, 435 B)
- [manifest.json](attachments/manifest.json) (application/json, 194 B)
- [background.js](attachments/background.js) (text/javascript, 864 B)
- [test.html](attachments/test.html) (text/html, 53 B)
- [manifest.json](attachments/manifest.json) (application/json, 243 B)
- [Thu Mar 27 2025 10:26:01 GMT-0400 (Eastern Daylight Time).png](attachments/Thu Mar 27 2025 10_26_01 GMT-0400 (Eastern Daylight Time).png) (image/png, 794.0 KB)

## Timeline

### 0x...@gmail.com (2025-03-24)

Extension1 attchments

### 0x...@gmail.com (2025-03-24)

Extension2 attchments

### sr...@google.com (2025-03-24)

I wasn't able to reproduce this unfortunately. I'm setting Security_Impact-None since it looks like this is only reachable with the --auto-open-devtools-for-tabs page.

dbertoni@, I'm not entirely sure if this is an extensions issue. Please feel free to reassign to me if you think the problem is somewhere else.
From what I can tell from the asan report, extensions::ExtensionTabUtil creates a Browser* instance when handling a service worker request, but the main thread is still in the startup phase (PreMainMessageLoopRun) ??

### db...@google.com (2025-03-24)

This doesn't look like an Extension bug. The affected code in BrowserTabStripTracker::Init() is:

```
void BrowserTabStripTracker::Init() {
  BrowserList::AddObserver(this);

  base::AutoReset<bool> resetter(&is_processing_initial_browsers_, true);
  for (Browser* browser : *BrowserList::GetInstance()) {
    MaybeTrackBrowser(browser);
  }
}

```

So the global list returned by BrowserList::GetInstance() seems to have a dangling pointer in it.

However, looking at the reported deletion and allocation stack traces, they're both showing Browser's constructor, so this doesn't make sense to me.

```
0x7bf446f20bf8 is located 8 bytes inside of 16-byte region [0x7bf446f20bf0,0x7bf446f20c00)
freed by thread T0 (chrome) here:
    #0 0x5625f6f2b6ed in operator delete(void*) _asan_rtl_:3
    #1 0x562608d429ef in __libcpp_operator_delete<base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1> *> ./../../third_party/libc++/src/include/__new/allocate.h:46:3
    #2 0x562608d429ef in __libcpp_deallocate<base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1> > ./../../third_party/libc++/src/include/__new/allocate.h:86:12
    #3 0x562608d429ef in deallocate ./../../third_party/libc++/src/include/__memory/allocator.h:120:7
    #4 0x562608d429ef in deallocate ./../../third_party/libc++/src/include/__memory/allocator_traits.h:302:9
    #5 0x562608d429ef in ~__split_buffer ./../../third_party/libc++/src/include/__split_buffer:337:5
    #6 0x562608d429ef in base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1>* std::__Cr::vector<base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1>, std::__Cr::allocator<base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1>>>::__emplace_back_slow_path<base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1>>(base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1>&&) ./../../third_party/libc++/src/include/__vector/vector.h:1142:1
    #7 0x562608d38b60 in emplace_back<base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1> > ./../../third_party/libc++/src/include/__vector/vector.h:1158:13
    #8 0x562608d38b60 in push_back ./../../third_party/libc++/src/include/__vector/vector.h:452:90
    #9 0x562608d38b60 in BrowserList::AddBrowser(Browser*) ./../../chrome/browser/ui/browser_list.cc:89:28
    #10 0x562621dec535 in Browser::Browser(Browser::CreateParams const&) ./../../chrome/browser/ui/browser.cc:697:3

```
```
    #0 0x5625f6f2ae8d in operator new(unsigned long) _asan_rtl_:3
    #1 0x562608d428cb in __libcpp_operator_new<unsigned long> ./../../third_party/libc++/src/include/__new/allocate.h:37:10
    #2 0x562608d428cb in __libcpp_allocate<base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1> > ./../../third_party/libc++/src/include/__new/allocate.h:64:28
    #3 0x562608d428cb in allocate ./../../third_party/libc++/src/include/__memory/allocator.h:105:14
    #4 0x562608d428cb in __allocate_at_least<std::__Cr::allocator<base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1> > > ./../../third_party/libc++/src/include/__memory/allocate_at_least.h:41:19
    #5 0x562608d428cb in __split_buffer ./../../third_party/libc++/src/include/__split_buffer:325:25
    #6 0x562608d428cb in base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1>* std::__Cr::vector<base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1>, std::__Cr::allocator<base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1>>>::__emplace_back_slow_path<base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1>>(base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1>&&) ./../../third_party/libc++/src/include/__vector/vector.h:1136:47
    #7 0x562608d38b60 in emplace_back<base::raw_ptr<Browser, (partition_alloc::internal::RawPtrTraits)1> > ./../../third_party/libc++/src/include/__vector/vector.h:1158:13
    #8 0x562608d38b60 in push_back ./../../third_party/libc++/src/include/__vector/vector.h:452:90
    #9 0x562608d38b60 in BrowserList::AddBrowser(Browser*) ./../../chrome/browser/ui/browser_list.cc:89:28
    #10 0x562621dec535 in Browser::Browser(Browser::CreateParams const&) ./../../chrome/browser/ui/browser.cc:697:3

```

Perhaps ASAN is reporting the wrong deletion stack trace? In the deletion stack trace, it look likes the vector is being resized, so perhaps that's confusing ASAN?

### 0x...@gmail.com (2025-03-25)

The extension2 is a irregular extension, it will report a UI error when loads the extension2. That maybe disrupt the initialization of BrowserTabStripTracker.
When reproduce this issue on Linux, do not change the loading order of the extensions,do not click any confirmation button. Excute the command and wait for the crash.

### sr...@google.com (2025-03-25)

etienneb@ I saw you recently introduced a BrowserListIterator that fixed another issue with the BrowserList access. Could you take a look if this issue is related?

### et...@google.com (2025-03-27)

Looking quickly at the bug. There is an issue with the way browsers lists are managed.

Here: [aligned with comment 5]
https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser_tab_strip_tracker.cc;l=36;drc=a48632411d7e7263e8fd4d273d24a80f668b73ec

That list is scanned and it can be modified while being scanned. (See screenshot).

BrowserList::AddBrowser                                   <<<--- Modifying the list
Browser::Browser
Browser::Create
DevToolsWindow::CreateDevToolsBrowser
DevToolsWindow::Show
ScheduleShow
DevToolsWindow::ToggleDevToolsWindow
DevToolsWindow::OpenDevToolsWindow
DevToolsAutoOpener::OnTabStripModelChanged
BrowserTabStripTracker::MaybeTrackBrowser
BrowserTabStripTracker::Init                              <<<-- List scanning



### dx...@google.com (2025-04-16)

Project: chromium/src  

Branch: main  

Author: Etienne Bergeron [etienneb@chromium.org](mailto:etienneb@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6431316>

Fix UaF while scanning browser list

---


Expand for full commit details
```
     
    This CL is fixing a UaF caused by a vector resize while 
    scanning the content of the vector. 
     
    The broken stack is: 
     
      BrowserList::AddBrowser   <<<--- Modifying the list 
      Browser::Browser 
      Browser::Create 
      DevToolsWindow::CreateDevToolsBrowser 
      DevToolsWindow::Show 
      ScheduleShow 
      DevToolsWindow::ToggleDevToolsWindow 
      DevToolsWindow::OpenDevToolsWindow 
      DevToolsAutoOpener::OnTabStripModelChanged 
      BrowserTabStripTracker::MaybeTrackBrowser 
      BrowserTabStripTracker::Init   <<<-- List scanning 
     
    Bug: 405910169 
    Change-Id: Id1273e6c1ebaa6adac0149edab0032552b971373 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6431316 
    Reviewed-by: Dana Fried <dfried@chromium.org> 
    Commit-Queue: Etienne Bergeron <etienneb@chromium.org> 
    Reviewed-by: Greg Thompson <grt@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1447899}

```

---

Files:

- M `chrome/browser/lifetime/browser_close_manager.cc`
- M `chrome/browser/ui/BUILD.gn`
- M `chrome/browser/ui/browser_list.cc`
- M `chrome/browser/ui/browser_list.h`
- A `chrome/browser/ui/browser_list_enumerator.cc`
- A `chrome/browser/ui/browser_list_enumerator.h`
- A `chrome/browser/ui/browser_list_enumerator_browsertest.cc`
- M `chrome/browser/ui/browser_tab_strip_tracker.cc`
- M `chrome/test/BUILD.gn`

---

Hash: 5cd9c4f1229d432f42c1c901344f6e3ba9474acb  

Date:  Wed Apr 16 18:36:54 2025


---

### sp...@google.com (2025-04-25)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
significantly mitigated memory corruption in a non-sandboxed process, with the precondition of installing two extensions, one of which must be side-loaded and use of devtools for tabs


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2025-07-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/405910169)*
