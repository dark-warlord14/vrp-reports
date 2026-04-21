# heap-use-after-free in task_manager

| Field | Value |
|-------|-------|
| **Issue ID** | [40056265](https://issues.chromium.org/issues/40056265) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2021-38023 |
| **Reporter** | vm...@gmail.com |
| **Assignee** | sa...@chromium.org |
| **Created** | 2021-06-18 |
| **Bounty** | $15,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36

Steps to reproduce the problem:
1.install extension

What is the expected behavior?
crash in browser.

What went wrong?
=================================================================
==996919==ERROR: AddressSanitizer: heap-use-after-free on address 0x60f0002abdf0 at pc 0x557abc18c891 bp 0x7fffe93891b0 sp 0x7fffe93891a8
READ of size 8 at 0x60f0002abdf0 thread T0 (chrome)
==996919==WARNING: invalid path to external symbolizer!
==996919==WARNING: Failed to use and restart external symbolizer!
    #0 0x557abc18c890 in operator-> ./../../base/memory/scoped_refptr.h:236:12
    #1 0x557abc18c890 in task_manager::TaskGroup::Refresh(gpu::VideoMemoryUsageStats const&, base::TimeDelta, long) ./../../chrome/browser/task_manager/sampling/task_group.cc:238:23
    #2 0x557abc15cf12 in task_manager::TaskManagerImpl::Refresh() ./../../chrome/browser/task_manager/sampling/task_manager_impl.cc:619:24
    #3 0x557abc14e649 in task_manager::TaskManagerInterface::AddObserver(task_manager::TaskManagerObserver*) ./../../chrome/browser/task_manager/task_manager_interface.cc:72:5
    #4 0x557ac42428d5 in extensions::ProcessesGetProcessInfoFunction::Run() ./../../chrome/browser/extensions/api/processes/processes_api.cc:604:57
    #5 0x557ab4a13870 in ExtensionFunction::RunWithValidation() ./../../extensions/browser/extension_function.cc:513:10
    #6 0x557ab4a1c5c0 in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal(extensions::mojom::RequestParams const&, content::RenderFrameHost*, int, base::OnceCallback<void (ExtensionFunction::ResponseType, base::Value const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&)>) ./../../extensions/browser/extension_function_dispatcher.cc:395:15
    #7 0x557ab4a1b9ce in extensions::ExtensionFunctionDispatcher::Dispatch(mojo::StructPtr<extensions::mojom::RequestParams>, content::RenderFrameHost*, int, base::OnceCallback<void (bool, base::Value, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&)>) ./../../extensions/browser/extension_function_dispatcher.cc:257:3
    #8 0x557ab4a1099a in extensions::ExtensionFrameHost::Request(mojo::StructPtr<extensions::mojom::RequestParams>, base::OnceCallback<void (bool, base::Value, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&)>) ./../../extensions/browser/extension_frame_host.cc:40:9
    #9 0x557ab21fd74f in extensions::mojom::LocalFrameHostStubDispatch::AcceptWithResponder(extensions::mojom::LocalFrameHost*, mojo::Message*, std::__1::unique_ptr<mojo::MessageReceiverWithStatus, std::__1::default_delete<mojo::MessageReceiverWithStatus> >) ./gen/extensions/common/mojom/frame.mojom.cc:2132:13
    #10 0x557abc65be4f in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:835:56
    #11 0x557abc66d09a in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:48:24
    #12 0x557abc65fa35 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:648:21
    #13 0x557abdf4e029 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ./../../ipc/ipc_mojo_bootstrap.cc:989:24
    #14 0x557abdf468c4 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind_internal.h:509:12
    #15 0x557abdf468c4 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind_internal.h:648:12
    #16 0x557abdf468c4 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> ./../../base/bind_internal.h:721:12
    #17 0x557abdf468c4 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:690:12
    #18 0x557abacc3250 in Run ./../../base/callback.h:98:12
    #19 0x557abacc3250 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:178:33
    #20 0x557abacfda49 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:360:23
    #21 0x557abacfd1ba in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260:36
    #22 0x557abacfe401 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #23 0x557ababb88ca in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_glib.cc:405:48
    #24 0x557abacfeac4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:467:12
    #25 0x557abac403e1 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #26 0x557abac4227c in base::RunLoop::RunUntilIdle() ./../../base/run_loop.cc:143:3
    #27 0x557ab2c7ff71 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser_main_loop.cc:982:18
    #28 0x557ab2c84ba5 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser_main_runner_impl.cc:152:15
    #29 0x557ab2c79d85 in content::BrowserMain(content::MainFunctionParams const&) ./../../content/browser/browser_main.cc:47:28
    #30 0x557aba983285 in RunBrowserProcessMain ./../../content/app/content_main_runner_impl.cc:598:10
    #31 0x557aba983285 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) ./../../content/app/content_main_runner_impl.cc:1087:10
    #32 0x557aba982519 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:956:12
    #33 0x557aba97ce8d in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) ./../../content/app/content_main.cc:386:36
    #34 0x557aba97d3bc in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:412:10
    #35 0x557aadb8523d in ChromeMain ./../../chrome/app/chrome_main.cc:151:12
    #36 0x7f57727590b2 in __libc_start_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

0x60f0002abdf0 is located 32 bytes inside of 176-byte region [0x60f0002abdd0,0x60f0002abe80)
freed by thread T0 (chrome) here:
    #0 0x557aadb82f7d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160:3
    #1 0x557abc15da0c in operator() ./../../buildtools/third_party/libc++/trunk/include/memory:1335:5
    #2 0x557abc15da0c in reset ./../../buildtools/third_party/libc++/trunk/include/memory:1596:7
    #3 0x557abc15da0c in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/memory:1550:19
    #4 0x557abc15da0c in ~pair ./../../buildtools/third_party/libc++/trunk/include/utility:297:29
    #5 0x557abc15da0c in destroy<std::pair<const int, std::unique_ptr<task_manager::TaskGroup> >, void, void> ./../../buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:317:15
    #6 0x557abc15da0c in std::__1::__tree<std::__1::__value_type<int, std::__1::unique_ptr<task_manager::TaskGroup, std::__1::default_delete<task_manager::TaskGroup> > >, std::__1::__map_value_compare<int, std::__1::__value_type<int, std::__1::unique_ptr<task_manager::TaskGroup, std::__1::default_delete<task_manager::TaskGroup> > >, std::__1::less<int>, true>, std::__1::allocator<std::__1::__value_type<int, std::__1::unique_ptr<task_manager::TaskGroup, std::__1::default_delete<task_manager::TaskGroup> > > > >::destroy(std::__1::__tree_node<std::__1::__value_type<int, std::__1::unique_ptr<task_manager::TaskGroup, std::__1::default_delete<task_manager::TaskGroup> > >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/__tree:1801:9
    #7 0x557abc15d9d9 in std::__1::__tree<std::__1::__value_type<int, std::__1::unique_ptr<task_manager::TaskGroup, std::__1::default_delete<task_manager::TaskGroup> > >, std::__1::__map_value_compare<int, std::__1::__value_type<int, std::__1::unique_ptr<task_manager::TaskGroup, std::__1::default_delete<task_manager::TaskGroup> > >, std::__1::less<int>, true>, std::__1::allocator<std::__1::__value_type<int, std::__1::unique_ptr<task_manager::TaskGroup, std::__1::default_delete<task_manager::TaskGroup> > > > >::destroy(std::__1::__tree_node<std::__1::__value_type<int, std::__1::unique_ptr<task_manager::TaskGroup, std::__1::default_delete<task_manager::TaskGroup> > >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/__tree:1799:9
    #8 0x557abc15d9d9 in std::__1::__tree<std::__1::__value_type<int, std::__1::unique_ptr<task_manager::TaskGroup, std::__1::default_delete<task_manager::TaskGroup> > >, std::__1::__map_value_compare<int, std::__1::__value_type<int, std::__1::unique_ptr<task_manager::TaskGroup, std::__1::default_delete<task_manager::TaskGroup> > >, std::__1::less<int>, true>, std::__1::allocator<std::__1::__value_type<int, std::__1::unique_ptr<task_manager::TaskGroup, std::__1::default_delete<task_manager::TaskGroup> > > > >::destroy(std::__1::__tree_node<std::__1::__value_type<int, std::__1::unique_ptr<task_manager::TaskGroup, std::__1::default_delete<task_manager::TaskGroup> > >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/__tree:1799:9
    #9 0x557abc15d9d9 in std::__1::__tree<std::__1::__value_type<int, std::__1::unique_ptr<task_manager::TaskGroup, std::__1::default_delete<task_manager::TaskGroup> > >, std::__1::__map_value_compare<int, std::__1::__value_type<int, std::__1::unique_ptr<task_manager::TaskGroup, std::__1::default_delete<task_manager::TaskGroup> > >, std::__1::less<int>, true>, std::__1::allocator<std::__1::__value_type<int, std::__1::unique_ptr<task_manager::TaskGroup, std::__1::default_delete<task_manager::TaskGroup> > > > >::destroy(std::__1::__tree_node<std::__1::__value_type<int, std::__1::unique_ptr<task_manager::TaskGroup, std::__1::default_delete<task_manager::TaskGroup> > >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/__tree:1799:9
    #10 0x557abc15d9d9 in std::__1::__tree<std::__1::__value_type<int, std::__1::unique_ptr<task_manager::TaskGroup, std::__1::default_delete<task_manager::TaskGroup> > >, std::__1::__map_value_compare<int, std::__1::__value_type<int, std::__1::unique_ptr<task_manager::TaskGroup, std::__1::default_delete<task_manager::TaskGroup> > >, std::__1::less<int>, true>, std::__1::allocator<std::__1::__value_type<int, std::__1::unique_ptr<task_manager::TaskGroup, std::__1::default_delete<task_manager::TaskGroup> > > > >::destroy(std::__1::__tree_node<std::__1::__value_type<int, std::__1::unique_ptr<task_manager::TaskGroup, std::__1::default_delete<task_manager::TaskGroup> > >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/__tree:1799:9
    #11 0x557abc15d9d9 in std::__1::__tree<std::__1::__value_type<int, std::__1::unique_ptr<task_manager::TaskGroup, std::__1::default_delete<task_manager::TaskGroup> > >, std::__1::__map_value_compare<int, std::__1::__value_type<int, std::__1::unique_ptr<task_manager::TaskGroup, std::__1::default_delete<task_manager::TaskGroup> > >, std::__1::less<int>, true>, std::__1::allocator<std::__1::__value_type<int, std::__1::unique_ptr<task_manager::TaskGroup, std::__1::default_delete<task_manager::TaskGroup> > > > >::destroy(std::__1::__tree_node<std::__1::__value_type<int, std::__1::unique_ptr<task_manager::TaskGroup, std::__1::default_delete<task_manager::TaskGroup> > >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/__tree:1799:9
    #12 0x557abc15d5bb in clear ./../../buildtools/third_party/libc++/trunk/include/__tree:1838:5
    #13 0x557abc15d5bb in clear ./../../buildtools/third_party/libc++/trunk/include/map:1311:37
    #14 0x557abc15d5bb in task_manager::TaskManagerImpl::StopUpdating() ./../../chrome/browser/task_manager/sampling/task_manager_impl.cc:666:27
    #15 0x557abc14f3a4 in task_manager::TaskManagerInterface::RemoveObserver(task_manager::TaskManagerObserver*) ./../../chrome/browser/task_manager/task_manager_interface.cc:103:5
    #16 0x557ac4243808 in extensions::ProcessesGetProcessInfoFunction::GatherDataAndRespond(std::__1::vector<long, std::__1::allocator<long> > const&) ./../../chrome/browser/extensions/api/processes/processes_api.cc:703:57
    #17 0x557abc152752 in task_manager::TaskManagerInterface::NotifyObserversOnRefreshWithBackgroundCalculations(std::__1::vector<long, std::__1::allocator<long> > const&) ./../../chrome/browser/task_manager/task_manager_interface.cc:146:14
    #18 0x557abc154bfb in task_manager::TaskManagerImpl::OnTaskGroupBackgroundCalculationsDone() ./../../chrome/browser/task_manager/sampling/task_manager_impl.cc:697:3
    #19 0x557abc18ca88 in Run ./../../base/callback.h:166:12
    #20 0x557abc18ca88 in OnBackgroundRefreshTypeFinished ./../../chrome/browser/task_manager/sampling/task_group.cc:407:38
    #21 0x557abc18ca88 in OnRefreshNaClDebugStubPortDone ./../../chrome/browser/task_manager/sampling/task_group.cc:325:3
    #22 0x557abc18ca88 in task_manager::TaskGroup::RefreshNaClDebugStubPort(int) ./../../chrome/browser/task_manager/sampling/task_group.cc:309:5
    #23 0x557abc18c644 in task_manager::TaskGroup::Refresh(gpu::VideoMemoryUsageStats const&, base::TimeDelta, long) ./../../chrome/browser/task_manager/sampling/task_group.cc:233:5
    #24 0x557abc15cf12 in task_manager::TaskManagerImpl::Refresh() ./../../chrome/browser/task_manager/sampling/task_manager_impl.cc:619:24
    #25 0x557abc14e649 in task_manager::TaskManagerInterface::AddObserver(task_manager::TaskManagerObserver*) ./../../chrome/browser/task_manager/task_manager_interface.cc:72:5
    #26 0x557ac42428d5 in extensions::ProcessesGetProcessInfoFunction::Run() ./../../chrome/browser/extensions/api/processes/processes_api.cc:604:57
    #27 0x557ab4a13870 in ExtensionFunction::RunWithValidation() ./../../extensions/browser/extension_function.cc:513:10
    #28 0x557ab4a1c5c0 in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal(extensions::mojom::RequestParams const&, content::RenderFrameHost*, int, base::OnceCallback<void (ExtensionFunction::ResponseType, base::Value const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&)>) ./../../extensions/browser/extension_function_dispatcher.cc:395:15
    #29 0x557ab4a1b9ce in extensions::ExtensionFunctionDispatcher::Dispatch(mojo::StructPtr<extensions::mojom::RequestParams>, content::RenderFrameHost*, int, base::OnceCallback<void (bool, base::Value, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&)>) ./../../extensions/browser/extension_function_dispatcher.cc:257:3
    #30 0x557ab4a1099a in extensions::ExtensionFrameHost::Request(mojo::StructPtr<extensions::mojom::RequestParams>, base::OnceCallback<void (bool, base::Value, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&)>) ./../../extensions/browser/extension_frame_host.cc:40:9
    #31 0x557ab21fd74f in extensions::mojom::LocalFrameHostStubDispatch::AcceptWithResponder(extensions::mojom::LocalFrameHost*, mojo::Message*, std::__1::unique_ptr<mojo::MessageReceiverWithStatus, std::__1::default_delete<mojo::MessageReceiverWithStatus> >) ./gen/extensions/common/mojom/frame.mojom.cc:2132:13
    #32 0x557abc65be4f in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:835:56
    #33 0x557abc66d09a in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:48:24
    #34 0x557abc65fa35 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:648:21
    #35 0x557abdf4e029 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ./../../ipc/ipc_mojo_bootstrap.cc:989:24
    #36 0x557abdf468c4 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind_internal.h:509:12
    #37 0x557abdf468c4 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind_internal.h:648:12
    #38 0x557abdf468c4 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> ./../../base/bind_internal.h:721:12
    #39 0x557abdf468c4 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:690:12
    #40 0x557abacc3250 in Run ./../../base/callback.h:98:12
    #41 0x557abacc3250 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:178:33
    #42 0x557abacfda49 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:360:23
    #43 0x557abacfd1ba in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260:36

previously allocated by thread T0 (chrome) here:
    #0 0x557aadb8271d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x557abc15b6e2 in make_unique<task_manager::TaskGroup, const int &, const int &, const bool &, const base::RepeatingCallback<void ()> &, scoped_refptr<task_manager::SharedSampler> &, scoped_refptr<base::SequencedTaskRunner> &> ./../../buildtools/third_party/libc++/trunk/include/memory:2006:28
    #2 0x557abc15b6e2 in task_manager::TaskManagerImpl::TaskAdded(task_manager::Task*) ./../../chrome/browser/task_manager/sampling/task_manager_impl.cc:492:18
    #3 0x557abc187c58 in ShowTask ./../../chrome/browser/task_manager/providers/fallback_task_provider.cc:131:3
    #4 0x557abc187c58 in task_manager::FallbackTaskProvider::OnTaskAddedBySource(task_manager::Task*, task_manager::FallbackTaskProvider::SubproviderSource*) ./../../chrome/browser/task_manager/providers/fallback_task_provider.cc:161:3
    #5 0x557abc1884a0 in task_manager::FallbackTaskProvider::SubproviderSource::TaskAdded(task_manager::Task*) ./../../chrome/browser/task_manager/providers/fallback_task_provider.cc:205:28
    #6 0x557abc1770c8 in task_manager::SpareRenderProcessHostTaskProvider::SpareRenderProcessHostTaskChanged(content::RenderProcessHost*) ./../../chrome/browser/task_manager/providers/spare_render_process_host_task_provider.cc:67:5
    #7 0x557ab398b9cd in Run ./../../base/callback.h:166:12
    #8 0x557ab398b9cd in RegisterSpareRenderProcessHostChangedCallback ./../../content/browser/renderer_host/render_process_host_impl.cc:760:8
    #9 0x557ab398b9cd in content::RenderProcessHost::RegisterSpareRenderProcessHostChangedCallback(base::RepeatingCallback<void (content::RenderProcessHost*)> const&) ./../../content/browser/renderer_host/render_process_host_impl.cc:3125:8
    #10 0x557abc176d3d in task_manager::SpareRenderProcessHostTaskProvider::StartUpdating() ./../../chrome/browser/task_manager/providers/spare_render_process_host_task_provider.cc:40:7
    #11 0x557abc186726 in task_manager::FallbackTaskProvider::StartUpdating() ./../../chrome/browser/task_manager/providers/fallback_task_provider.cc:73:28
    #12 0x557abc15d420 in task_manager::TaskManagerImpl::StartUpdating() ./../../chrome/browser/task_manager/sampling/task_manager_impl.cc:650:15
    #13 0x557abc14e649 in task_manager::TaskManagerInterface::AddObserver(task_manager::TaskManagerObserver*) ./../../chrome/browser/task_manager/task_manager_interface.cc:72:5
    #14 0x557ac42428d5 in extensions::ProcessesGetProcessInfoFunction::Run() ./../../chrome/browser/extensions/api/processes/processes_api.cc:604:57
    #15 0x557ab4a13870 in ExtensionFunction::RunWithValidation() ./../../extensions/browser/extension_function.cc:513:10
    #16 0x557ab4a1c5c0 in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal(extensions::mojom::RequestParams const&, content::RenderFrameHost*, int, base::OnceCallback<void (ExtensionFunction::ResponseType, base::Value const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&)>) ./../../extensions/browser/extension_function_dispatcher.cc:395:15
    #17 0x557ab4a1b9ce in extensions::ExtensionFunctionDispatcher::Dispatch(mojo::StructPtr<extensions::mojom::RequestParams>, content::RenderFrameHost*, int, base::OnceCallback<void (bool, base::Value, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&)>) ./../../extensions/browser/extension_function_dispatcher.cc:257:3
    #18 0x557ab4a1099a in extensions::ExtensionFrameHost::Request(mojo::StructPtr<extensions::mojom::RequestParams>, base::OnceCallback<void (bool, base::Value, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&)>) ./../../extensions/browser/extension_frame_host.cc:40:9
    #19 0x557ab21fd74f in extensions::mojom::LocalFrameHostStubDispatch::AcceptWithResponder(extensions::mojom::LocalFrameHost*, mojo::Message*, std::__1::unique_ptr<mojo::MessageReceiverWithStatus, std::__1::default_delete<mojo::MessageReceiverWithStatus> >) ./gen/extensions/common/mojom/frame.mojom.cc:2132:13
    #20 0x557abc65be4f in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:835:56
    #21 0x557abc66d09a in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:48:24
    #22 0x557abc65fa35 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:648:21
    #23 0x557abdf4e029 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ./../../ipc/ipc_mojo_bootstrap.cc:989:24
    #24 0x557abdf468c4 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind_internal.h:509:12
    #25 0x557abdf468c4 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind_internal.h:648:12
    #26 0x557abdf468c4 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> ./../../base/bind_internal.h:721:12
    #27 0x557abdf468c4 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:690:12
    #28 0x557abacc3250 in Run ./../../base/callback.h:98:12
    #29 0x557abacc3250 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:178:33
    #30 0x557abacfda49 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:360:23
    #31 0x557abacfd1ba in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260:36
    #32 0x557abacfe401 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #33 0x557ababb88ca in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_glib.cc:405:48
    #34 0x557abacfeac4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:467:12
    #35 0x557abac403e1 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #36 0x557abac4227c in base::RunLoop::RunUntilIdle() ./../../base/run_loop.cc:143:3
    #37 0x557ab2c7ff71 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser_main_loop.cc:982:18

SUMMARY: AddressSanitizer: heap-use-after-free (/home/xxx/xxx/xxx_chrome/asan-linux-release-892490/chrome+0x18edd890)
Shadow bytes around the buggy address:
  0x0c1e8004d760: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c1e8004d770: 00 00 00 00 00 fa fa fa fa fa fa fa fa fa 00 00
  0x0c1e8004d780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c1e8004d790: 00 00 00 00 fa fa fa fa fa fa fa fa fd fd fd fd
  0x0c1e8004d7a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0c1e8004d7b0: fd fa fa fa fa fa fa fa fa fa fd fd fd fd[fd]fd
  0x0c1e8004d7c0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c1e8004d7d0: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x0c1e8004d7e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa
  0x0c1e8004d7f0: fa fa fa fa fa fa fd fd fd fd fd fd fd fd fd fd
  0x0c1e8004d800: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
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
==996919==ABORTING
[0618/101233.411427:ERROR:nacl_helper_linux.cc(307)] NaCl helper process running without a sandbox!
Most likely you need to configure your SUID sandbox correctly

Did this work before? N/A 

Chrome version: 93.0.4544.0  Channel: dev
OS Version: 20

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 314 B)
- [background.js](attachments/background.js) (text/plain, 62 B)
- [main.html](attachments/main.html) (text/plain, 48 B)
- deleted (application/octet-stream, 0 B)
- [main.js](attachments/main.js) (text/plain, 289 B)
- [91_stable.png](attachments/91_stable.png) (image/png, 92.6 KB)
- [93_developer_build.png](attachments/93_developer_build.png) (image/png, 57.9 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 391 B)

## Timeline

### vm...@gmail.com (2021-06-18)

hi, can I get a CVE num if this is on dev channel?

### [Deleted User] (2021-06-18)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-06-18)

This would be sev-crit, except that it requires installing an extension,so I think we can should it as sev-high.  I'd expect it to be present on all the platforms that support extensions.

I'm guessing this might be related to https://source.chromium.org/chromium/chromium/src/+/1e9fda56402e14c040fca088605b00332633b690 - jkim, can you take a look or re-assign as appropriate?

[Monorail components: Platform>Extensions]

### [Deleted User] (2021-06-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-18)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-06-18)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jk...@igalia.com (2021-06-21)

Hi, thanks for reporting. Can I ask more information to reproduce this issue?

I tried it on the current stable 91 and dev build on 93 but I couldn't see this crash.
I built with the config below.

is_debug = false
dcheck_always_on = true
is_asan = true
enable_full_stack_frames_for_profiling = true
v8_enable_verify_heap = true

And installed the attached file after enabling developer mode on chrome://extensions.
On the stable version, it seems it couldn't run because manifest version issue and 'processes' seems to be allowed on dev.(91_stable.png)
On the dev build, even though it still has manifest version issue, I can see a new tab is opened. However, I couldn't see this crash with asan enabled build.(93_developer_build.png)

Could you take a look what I missed?

### sa...@chromium.org (2021-06-21)

It looks like https://crrev.com/c/2837446 with the ProcessHostOnUI feature is enabled (and nacl enabled) is responsible. With that feature enabled, TaskGroup::RefreshNaClDebugStubPort() reports its result synchronously instead of asynchronously. A default chrome.processes.getProcessInfo() call only requests nacl debug stub port, so it's ready to report results and notifies TaskManagerImpl by calling a callback; this completes the extension call and it tears itself down, resulting in the TaskManagerImpl cleaning up and deleting the TaskGroup object that's still in the middle of TaskGroup::Refresh(). Eventually, that all unwinds and TaskGroup::Refresh() continues with a dangling this pointer.

https://crrev.com/c/2975184 should help.

### vm...@gmail.com (2021-06-21)

about https://crbug.com/chromium/1221406#c7: I was tested on asan-linux-release-892490.  And Version3 's manifest.json may help with "require version of at least 3"

### jk...@igalia.com (2021-06-21)

Thanks for updating manifest.json.
I realized that my environment has disabled NaCl after reading https://crbug.com/chromium/1221406#c8.
After enabling it, I reproduced this issue and verified the CL mentioned in https://crbug.com/chromium/1221406#c8 fixes this issue.

### gi...@appspot.gserviceaccount.com (2021-06-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a16c0a11524b417c3dd5f42014a8958cce07e452

commit a16c0a11524b417c3dd5f42014a8958cce07e452
Author: Sam McNally <sammc@chromium.org>
Date: Mon Jun 21 13:51:34 2021

Always report the nacl debug port asynchronously.

TaskGroup::RefreshNaClDebugStubPort() reports its result synchronously
if the ProcessHostOnUI feature is enabled, and asynchronously otherwise.
This complexity is confusing and error-prone so always report the result
asynchronously.

Bug: 1221406
Change-Id: I71f44506af281355c6a6fac46763a0305b6b641f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2975184
Auto-Submit: Sam McNally <sammc@chromium.org>
Commit-Queue: Ahmed Fakhry <afakhry@chromium.org>
Reviewed-by: Ahmed Fakhry <afakhry@chromium.org>
Cr-Commit-Position: refs/heads/master@{#894228}

[modify] https://crrev.com/a16c0a11524b417c3dd5f42014a8958cce07e452/chrome/browser/task_manager/sampling/task_group.cc
[modify] https://crrev.com/a16c0a11524b417c3dd5f42014a8958cce07e452/chrome/browser/task_manager/sampling/task_group_unittest.cc


### vm...@gmail.com (2021-06-22)

[Comment Deleted]

### sa...@chromium.org (2021-06-25)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-25)

This bug requires manual review: M92's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: govind@(Android), benmason@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-06-25)

[Empty comment from Monorail migration]

### sa...@chromium.org (2021-06-25)

1. It's a security fix for something introduced in 92, so probably.
2. https://chromium-review.googlesource.com/c/chromium/src/+/2975184
3. Yes.
4. No; the issue was introduced in 92 and the fix landed in 93.
5. Security fix.
6. No.


### [Deleted User] (2021-06-25)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-27)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sa...@chromium.org (2021-06-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-06-28)

merge approved for M92, please merge to branch 4515. Thanks! 

### am...@chromium.org (2021-06-28)

hi vmth...@, to respond to your question in https://crbug.com/chromium/1221406#c12, a CVE will be issued when this fix is shipped as part of a Stable channel release. The M92 stable channel release is currently planned for 20 July 2021.

### [Deleted User] (2021-06-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-06-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7c749241a482613087a48013083da2f630f0b2c0

commit 7c749241a482613087a48013083da2f630f0b2c0
Author: Sam McNally <sammc@chromium.org>
Date: Tue Jun 29 02:36:43 2021

Always report the nacl debug port asynchronously.

TaskGroup::RefreshNaClDebugStubPort() reports its result synchronously
if the ProcessHostOnUI feature is enabled, and asynchronously otherwise.
This complexity is confusing and error-prone so always report the result
asynchronously.

(cherry picked from commit a16c0a11524b417c3dd5f42014a8958cce07e452)

Bug: 1221406
Change-Id: I71f44506af281355c6a6fac46763a0305b6b641f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2975184
Auto-Submit: Sam McNally <sammc@chromium.org>
Commit-Queue: Ahmed Fakhry <afakhry@chromium.org>
Reviewed-by: Ahmed Fakhry <afakhry@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#894228}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2992347
Commit-Queue: Sam McNally <sammc@chromium.org>
Cr-Commit-Position: refs/branch-heads/4515@{#1106}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/7c749241a482613087a48013083da2f630f0b2c0/chrome/browser/task_manager/sampling/task_group.cc
[modify] https://crrev.com/7c749241a482613087a48013083da2f630f0b2c0/chrome/browser/task_manager/sampling/task_group_unittest.cc


### sr...@google.com (2021-06-29)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-07-02)

Congratulations, the VRP Panel has decided to award you $15000 for this report! Someone from our finance team will be in touch soon to arrange payment. Thank you for this report and excellent work! 

### am...@google.com (2021-07-02)

[Empty comment from Monorail migration]

### vm...@gmail.com (2021-08-26)

Hi, my credit info would be: Huinian Yang (@vmth6) of Amber Security Lab, OPPO Mobile Telecommunications Corp. Ltd. 
Thanks:)

### [Deleted User] (2021-10-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vm...@gmail.com (2021-12-21)

Hi, can I get a CVE num for this issue?

sheriffbot via monorail <monorail+v2.1950284618@chromium.org> 于2021年10月6日周三
01:30写道：

### am...@chromium.org (2021-12-21)

[Comment Deleted]

### am...@chromium.org (2021-12-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-12-21)

Hello, CVE IDs are automatically issued for vulnerabilities discovered in Stable and are allocated upon the release of the stable channel version containing the fix. As this issue discovered in beta, it was not allocated a CVE. Upon your request, I have issued a CVE ID - CVE-2021-38023. 
The description will be filed with MITRE in the future and this bug report serves as the public information about the vulnerability at this time. 

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1221406?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056265)*
