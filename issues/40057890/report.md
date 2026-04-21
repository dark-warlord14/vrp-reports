# uaf in content::BroadcastChannelService::ConnectToChannel

| Field | Value |
|-------|-------|
| **Issue ID** | [40057890](https://issues.chromium.org/issues/40057890) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>Messaging |
| **Platforms** | Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | aw...@chromium.org |
| **Created** | 2021-11-11 |
| **Bounty** | $20,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36

Steps to reproduce the problem:
OS:
Ubuntu 20.04

Chrome Version:
Version 97.0.4692.8 (Developer Build) (64-bit) build with asan
Version 98.0.4697.0 (Developer Build) (64-bit) gs://chromium-browser-asan/linux-release/asan-linux-release-939805.zip

./chrome --user-data-dir=/tmp/2x --incognito    http://localhost:8000/crash.html

What is the expected behavior?

What went wrong?
OS:
Ubuntu 20.04

Chrome Version:
Version 97.0.4692.8 (Developer Build) (64-bit) build with asan
Version 98.0.4697.0 (Developer Build) (64-bit) gs://chromium-browser-asan/linux-release/asan-linux-release-939805.zip

./chrome --user-data-dir=/tmp/2x --incognito    http://localhost:8000/crash.html

In my local test, I can reproduce it about every 3 executions.
If it cannot be reproduced, you can increase  'loop_cnt' number

==2453754==ERROR: AddressSanitizer: heap-use-after-free on address 0x603000571db8 at pc 0x55e63b96bf88 bp 0x7ffc55167680 sp 0x7ffc55167678
READ of size 8 at 0x603000571db8 thread T0 (chrome)
    #0 0x55e63b96bf87 in __root ./../../buildtools/third_party/libc++/trunk/include/__tree:1079:59
    #1 0x55e63b96bf87 in __find_equal<blink::StorageKey> ./../../buildtools/third_party/libc++/trunk/include/__tree:1969:27
    #2 0x55e63b96bf87 in std::__1::pair<std::__1::__tree_iterator<std::__1::__value_type<blink::StorageKey, std::__1::multimap<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::unique_ptr<content::BroadcastChannelService::Connection, std::__1::default_delete<content::BroadcastChannelService::Connection> >, std::__1::less<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > >, std::__1::allocator<std::__1::pair<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const, std::__1::unique_ptr<content::BroadcastChannelService::Connection, std::__1::default_delete<content::BroadcastChannelService::Connection> > > > > >, std::__1::__tree_node<std::__1::__value_type<blink::StorageKey, std::__1::multimap<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::unique_ptr<content::BroadcastChannelService::Connection, std::__1::default_delete<content::BroadcastChannelService::Connection> >, std::__1::less<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > >, std::__1::allocator<std::__1::pair<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const, std::__1::unique_ptr<content::BroadcastChannelService::Connection, std::__1::default_delete<content::BroadcastChannelService::Connection> > > > > >, void*>*, long>, bool> std::__1::__tree<std::__1::__value_type<blink::StorageKey, std::__1::multimap<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::unique_ptr<content::BroadcastChannelService::Connection, std::__1::default_delete<content::BroadcastChannelService::Connection> >, std::__1::less<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > >, std::__1::allocator<std::__1::pair<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const, std::__1::unique_ptr<content::BroadcastChannelService::Connection, std::__1::default_delete<content::BroadcastChannelService::Connection> > > > > >, std::__1::__map_value_compare<blink::StorageKey, std::__1::__value_type<blink::StorageKey, std::__1::multimap<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::unique_ptr<content::BroadcastChannelService::Connection, std::__1::default_delete<content::BroadcastChannelService::Connection> >, std::__1::less<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > >, std::__1::allocator<std::__1::pair<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const, std::__1::unique_ptr<content::BroadcastChannelService::Connection, std::__1::default_delete<content::BroadcastChannelService::Connection> > > > > >, std::__1::less<blink::StorageKey>, true>, std::__1::allocator<std::__1::__value_type<blink::StorageKey, std::__1::multimap<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::unique_ptr<content::BroadcastChannelService::Connection, std::__1::default_delete<content::BroadcastChannelService::Connection> >, std::__1::less<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > >, std::__1::allocator<std::__1::pair<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const, std::__1::unique_ptr<content::BroadcastChannelService::Connection, std::__1::default_delete<content::BroadcastChannelService::Connection> > > > > > > >::__emplace_unique_key_args<blink::StorageKey, std::__1::piecewise_construct_t const&, std::__1::tuple<blink::StorageKey const&>, std::__1::tuple<> >(blink::StorageKey const&, std::__1::piecewise_construct_t const&, std::__1::tuple<blink::StorageKey const&>&&, std::__1::tuple<>&&) ./../../buildtools/third_party/libc++/trunk/include/__tree:2091:36
    #3 0x55e63b96ab73 in operator[] ./../../buildtools/third_party/libc++/trunk/include/map:1536:20
    #4 0x55e63b96ab73 in content::BroadcastChannelService::ConnectToChannel(blink::StorageKey const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, mojo::PendingAssociatedRemote<blink::mojom::BroadcastChannelClient>, mojo::PendingAssociatedReceiver<blink::mojom::BroadcastChannelClient>) ./../../content/browser/broadcast_channel/broadcast_channel_service.cc:113:3
    #5 0x55e63b969141 in content::BroadcastChannelProvider::ConnectToChannel(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, mojo::PendingAssociatedRemote<blink::mojom::BroadcastChannelClient>, mojo::PendingAssociatedReceiver<blink::mojom::BroadcastChannelClient>) ./../../content/browser/broadcast_channel/broadcast_channel_provider.cc:25:31
    #6 0x55e63d012e80 in blink::mojom::BroadcastChannelProviderStubDispatch::Accept(blink::mojom::BroadcastChannelProvider*, mojo::Message*) ./gen/third_party/blink/public/mojom/broadcastchannel/broadcast_channel.mojom.cc:296:13
    #7 0x55e645a80eb1 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:900:54
    #8 0x55e645a9393a in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #9 0x55e645a84f03 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:657:20
    #10 0x55e645a9fd42 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:1101:42
    #11 0x55e645a9e293 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:721:7
    #12 0x55e645a9393a in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #13 0x55e645a79d44 in mojo::Connector::DispatchMessage(mojo::Message) ./../../mojo/public/cpp/bindings/lib/connector.cc:556:49
    #14 0x55e645a7bfa6 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:614:14
    #15 0x55e645a7cd30 in Invoke<void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector> > ./../../base/bind_internal.h:533:12
    #16 0x55e645a7cd30 in MakeItSo<void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector> > ./../../base/bind_internal.h:728:5
    #17 0x55e645a7cd30 in RunImpl<void (mojo::Connector::*)(), std::__1::tuple<base::WeakPtr<mojo::Connector> >, 0UL> ./../../base/bind_internal.h:781:12
    #18 0x55e645a7cd30 in base::internal::Invoker<base::internal::BindState<void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector> >, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:750:12
    #19 0x55e644f2424f in Run ./../../base/callback.h:142:12
    #20 0x55e644f2424f in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:157:32
    #21 0x55e644f63503 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:358:29)> ./../../base/task/common/task_annotator.h:73:5
    #22 0x55e644f63503 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356:21
    #23 0x55e644f62d11 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261:30
    #24 0x55e644f640e7 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #25 0x55e644e1628a in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_glib.cc:405:48
    #26 0x55e644f647d7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:468:12
    #27 0x55e644e9b305 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:140:14
    #28 0x55e63ba0d451 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser_main_loop.cc:992:18
    #29 0x55e63ba11e91 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser_main_runner_impl.cc:152:15
    #30 0x55e63ba0797b in content::BrowserMain(content::MainFunctionParams const&) ./../../content/browser/browser_main.cc:49:28
    #31 0x55e643c7c37b in RunBrowserProcessMain ./../../content/app/content_main_runner_impl.cc:641:10
    #32 0x55e643c7c37b in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) ./../../content/app/content_main_runner_impl.cc:1137:10
    #33 0x55e643c7b471 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:1004:12
    #34 0x55e643c7487d in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) ./../../content/app/content_main.cc:390:36
    #35 0x55e643c7653e in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:418:10
    #36 0x55e636ac8131 in ChromeMain ./../../chrome/app/chrome_main.cc:172:12
    #37 0x7f2abe1660b2 in __libc_start_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

0x603000571db8 is located 8 bytes inside of 24-byte region [0x603000571db0,0x603000571dc8)
freed by thread T0 (chrome) here:
    #0 0x55e636ac59cd in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x55e63cb48c69 in operator() ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #2 0x55e63cb48c69 in reset ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #3 0x55e63cb48c69 in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:269:19
    #4 0x55e63cb48c69 in content::StoragePartitionImpl::~StoragePartitionImpl() ./../../content/browser/storage_partition_impl.cc:1125:1
    #5 0x55e63cb4a01c in content::StoragePartitionImpl::~StoragePartitionImpl() ./../../content/browser/storage_partition_impl.cc:1077:47
    #6 0x55e63cb845bd in operator() ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #7 0x55e63cb845bd in reset ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #8 0x55e63cb845bd in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:269:19
    #9 0x55e63cb845bd in ~pair ./../../buildtools/third_party/libc++/trunk/include/utility:394:29
    #10 0x55e63cb845bd in destroy<std::__1::pair<const content::StoragePartitionConfig, std::__1::unique_ptr<content::StoragePartitionImpl, std::__1::default_delete<content::StoragePartitionImpl> > >, void, void> ./../../buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:318:15
    #11 0x55e63cb845bd in std::__1::__tree<std::__1::__value_type<content::StoragePartitionConfig, std::__1::unique_ptr<content::StoragePartitionImpl, std::__1::default_delete<content::StoragePartitionImpl> > >, std::__1::__map_value_compare<content::StoragePartitionConfig, std::__1::__value_type<content::StoragePartitionConfig, std::__1::unique_ptr<content::StoragePartitionImpl, std::__1::default_delete<content::StoragePartitionImpl> > >, std::__1::less<content::StoragePartitionConfig>, true>, std::__1::allocator<std::__1::__value_type<content::StoragePartitionConfig, std::__1::unique_ptr<content::StoragePartitionImpl, std::__1::default_delete<content::StoragePartitionImpl> > > > >::destroy(std::__1::__tree_node<std::__1::__value_type<content::StoragePartitionConfig, std::__1::unique_ptr<content::StoragePartitionImpl, std::__1::default_delete<content::StoragePartitionImpl> > >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/__tree:1801:9
    #12 0x55e63cb7ead3 in ~__tree ./../../buildtools/third_party/libc++/trunk/include/__tree:1789:3
    #13 0x55e63cb7ead3 in ~map ./../../buildtools/third_party/libc++/trunk/include/map:1103:5
    #14 0x55e63cb7ead3 in ~StoragePartitionImplMap ./../../content/browser/storage_partition_impl_map.cc:326:1
    #15 0x55e63cb7ead3 in content::StoragePartitionImplMap::~StoragePartitionImplMap() ./../../content/browser/storage_partition_impl_map.cc:325:53
    #16 0x55e6443c310e in OffTheRecordProfileImpl::~OffTheRecordProfileImpl() ./../../chrome/browser/profiles/off_the_record_profile_impl.cc:239:3
    #17 0x55e6443c344c in OffTheRecordProfileImpl::~OffTheRecordProfileImpl() ./../../chrome/browser/profiles/off_the_record_profile_impl.cc:213:53
    #18 0x55e6443b987b in operator() ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #19 0x55e6443b987b in reset ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #20 0x55e6443b987b in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:269:19
    #21 0x55e6443b987b in ~pair ./../../buildtools/third_party/libc++/trunk/include/utility:394:29
    #22 0x55e6443b987b in destroy<std::__1::pair<const Profile::OTRProfileID, std::__1::unique_ptr<Profile, std::__1::default_delete<Profile> > >, void, void> ./../../buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:318:15
    #23 0x55e6443b987b in std::__1::__tree<std::__1::__value_type<Profile::OTRProfileID, std::__1::unique_ptr<Profile, std::__1::default_delete<Profile> > >, std::__1::__map_value_compare<Profile::OTRProfileID, std::__1::__value_type<Profile::OTRProfileID, std::__1::unique_ptr<Profile, std::__1::default_delete<Profile> > >, std::__1::less<Profile::OTRProfileID>, true>, std::__1::allocator<std::__1::__value_type<Profile::OTRProfileID, std::__1::unique_ptr<Profile, std::__1::default_delete<Profile> > > > >::erase(std::__1::__tree_const_iterator<std::__1::__value_type<Profile::OTRProfileID, std::__1::unique_ptr<Profile, std::__1::default_delete<Profile> > >, std::__1::__tree_node<std::__1::__value_type<Profile::OTRProfileID, std::__1::unique_ptr<Profile, std::__1::default_delete<Profile> > >, void*>*, long>) ./../../buildtools/third_party/libc++/trunk/include/__tree:2422:5
    #24 0x55e6443b4d94 in __erase_unique<Profile::OTRProfileID> ./../../buildtools/third_party/libc++/trunk/include/__tree:2445:5
    #25 0x55e6443b4d94 in erase ./../../buildtools/third_party/libc++/trunk/include/map:1317:25
    #26 0x55e6443b4d94 in ProfileImpl::DestroyOffTheRecordProfile(Profile*) ./../../chrome/browser/profiles/profile_impl.cc:1013:17
    #27 0x55e6443bdbcd in ProfileDestroyer::DestroyOffTheRecordProfileNow(Profile*) ./../../chrome/browser/profiles/profile_destroyer.cc:98:34
    #28 0x55e6443bb685 in ProfileDestroyer::DestroyProfileWhenAppropriate(Profile*) ./../../chrome/browser/profiles/profile_destroyer.cc:70:5
    #29 0x55e64f4056fd in Browser::~Browser() ./../../chrome/browser/ui/browser.cc:640:7
    #30 0x55e64f4068cc in Browser::~Browser() ./../../chrome/browser/ui/browser.cc:561:21
    #31 0x55e64fc6235e in operator() ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #32 0x55e64fc6235e in reset ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #33 0x55e64fc6235e in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:269:19
    #34 0x55e64fc6235e in BrowserView::~BrowserView() ./../../chrome/browser/ui/views/frame/browser_view.cc:868:1
    #35 0x55e64fc62d63 in ~BrowserView ./../../chrome/browser/ui/views/frame/browser_view.cc:828:29
    #36 0x55e64fc62d63 in non-virtual thunk to BrowserView::~BrowserView() ./../../chrome/browser/ui/views/frame/browser_view.cc:0:0
    #37 0x55e64e84ee3d in views::View::~View() ./../../ui/views/view.cc:254:9
    #38 0x55e6506693e1 in ~BrowserFrameViewLinuxNative ./../../chrome/browser/ui/views/frame/browser_frame_view_linux_native.cc:28:59
    #39 0x55e6506693e1 in BrowserFrameViewLinuxNative::~BrowserFrameViewLinuxNative() ./../../chrome/browser/ui/views/frame/browser_frame_view_linux_native.cc:28:59
    #40 0x55e64e95bfff in operator() ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #41 0x55e64e95bfff in reset ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #42 0x55e64e95bfff in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:269:19
    #43 0x55e64e95bfff in ~NonClientView ./../../ui/views/window/non_client_view.cc:168:1
    #44 0x55e64e95bfff in views::NonClientView::~NonClientView() ./../../ui/views/window/non_client_view.cc:164:33
    #45 0x55e64e852b29 in operator() ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #46 0x55e64e852b29 in reset ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #47 0x55e64e852b29 in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:269:19
    #48 0x55e64e852b29 in views::View::DoRemoveChildView(views::View*, bool, bool, views::View*) ./../../ui/views/view.cc:2641:1
    #49 0x55e64e852ef1 in views::View::RemoveAllChildViews() ./../../ui/views/view.cc:329:5
    #50 0x55e64e8d1565 in DestroyRootView ./../../ui/views/widget/widget.cc:1774:15
    #51 0x55e64e8d1565 in views::Widget::~Widget() ./../../ui/views/widget/widget.cc:209:3
    #52 0x55e64fc8ce1c in BrowserFrame::~BrowserFrame() ./../../chrome/browser/ui/views/frame/browser_frame.cc:87:31
    #53 0x55e64e9c8328 in views::DesktopNativeWidgetAura::~DesktopNativeWidgetAura() ./../../ui/views/widget/desktop_aura/desktop_native_widget_aura.cc:0:0
    #54 0x55e64fe0f432 in ~DesktopBrowserFrameAuraLinux ./../../chrome/browser/ui/views/frame/desktop_browser_frame_aura_linux.cc:31:61
    #55 0x55e64fe0f432 in DesktopBrowserFrameAuraLinux::~DesktopBrowserFrameAuraLinux() ./../../chrome/browser/ui/views/frame/desktop_browser_frame_aura_linux.cc:31:61
    #56 0x55e64e9b6347 in views::DesktopWindowTreeHostLinux::OnClosed() ./../../ui/views/widget/desktop_aura/desktop_window_tree_host_linux.cc:290:34
    #57 0x55e64ea05813 in views::DesktopWindowTreeHostPlatform::CloseNow() ./../../ui/views/widget/desktop_aura/desktop_window_tree_host_platform.cc:338:22
    #58 0x55e64ea10b40 in Invoke<void (views::DesktopWindowTreeHostPlatform::*)(), base::WeakPtr<views::DesktopWindowTreeHostPlatform> > ./../../base/bind_internal.h:533:12
    #59 0x55e64ea10b40 in MakeItSo<void (views::DesktopWindowTreeHostPlatform::*)(), base::WeakPtr<views::DesktopWindowTreeHostPlatform> > ./../../base/bind_internal.h:728:5
    #60 0x55e64ea10b40 in RunImpl<void (views::DesktopWindowTreeHostPlatform::*)(), std::__1::tuple<base::WeakPtr<views::DesktopWindowTreeHostPlatform> >, 0UL> ./../../base/bind_internal.h:781:12
    #61 0x55e64ea10b40 in base::internal::Invoker<base::internal::BindState<void (views::DesktopWindowTreeHostPlatform::*)(), base::WeakPtr<views::DesktopWindowTreeHostPlatform> >, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:750:12
    #62 0x55e644f2424f in Run ./../../base/callback.h:142:12
    #63 0x55e644f2424f in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:157:32
    #64 0x55e644f63503 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:358:29)> ./../../base/task/common/task_annotator.h:73:5
    #65 0x55e644f63503 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356:21
    #66 0x55e644f62d11 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261:30

previously allocated by thread T0 (chrome) here:
    #0 0x55e636ac516d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x55e63cb4c3c3 in make_unique<content::BroadcastChannelService> ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:725:28
    #2 0x55e63cb4c3c3 in content::StoragePartitionImpl::Initialize(content::StoragePartitionImpl*) ./../../content/browser/storage_partition_impl.cc:1272:32
    #3 0x55e63cb7f0a8 in content::StoragePartitionImplMap::Get(content::StoragePartitionConfig const&, bool) ./../../content/browser/storage_partition_impl_map.cc:353:14
    #4 0x55e63b97a456 in GetStoragePartition ./../../content/browser/browser_context.cc:142:52
    #5 0x55e63b97a456 in content::BrowserContext::GetDefaultStoragePartition() ./../../content/browser/browser_context.cc:185:10
    #6 0x55e63bf72b1c in content::HostZoomMap::GetDefaultForBrowserContext(content::BrowserContext*) ./../../content/browser/host_zoom_map_impl.cc:73:42
    #7 0x55e6443c2b71 in OffTheRecordProfileImpl::TrackZoomLevelsFromParent() ./../../chrome/browser/profiles/off_the_record_profile_impl.cc:266:32
    #8 0x55e6443c28b0 in OffTheRecordProfileImpl::Init() ./../../chrome/browser/profiles/off_the_record_profile_impl.cc:182:3
    #9 0x55e6443c4eee in Profile::CreateOffTheRecordProfile(Profile*, Profile::OTRProfileID const&) ./../../chrome/browser/profiles/off_the_record_profile_impl.cc:623:12
    #10 0x55e6443b45f6 in ProfileImpl::GetOffTheRecordProfile(Profile::OTRProfileID const&, bool) ./../../chrome/browser/profiles/profile_impl.cc:992:7
    #11 0x55e63e6bce80 in Profile::GetPrimaryOTRProfile(bool) ./../../chrome/browser/profiles/profile.cc:498:10
    #12 0x55e64f5b6bb7 in StartupBrowserCreator::GetPrivateProfileIfRequested(base::CommandLine const&, Profile*) ./../../chrome/browser/ui/startup/startup_browser_creator.cc:0:0
    #13 0x55e64f5b5436 in StartupBrowserCreator::ProcessCmdLineImpl(base::CommandLine const&, base::FilePath const&, bool, Profile*, std::__1::vector<Profile*, std::__1::allocator<Profile*> > const&) ./../../chrome/browser/ui/startup/startup_browser_creator.cc:814:7
    #14 0x55e64f5b4fbf in StartupBrowserCreator::Start(base::CommandLine const&, base::FilePath const&, Profile*, std::__1::vector<Profile*, std::__1::allocator<Profile*> > const&) ./../../chrome/browser/ui/startup/startup_browser_creator.cc:486:10
    #15 0x55e643e80438 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl() ./../../chrome/browser/chrome_browser_main.cc:1697:25
    #16 0x55e643e7e860 in ChromeBrowserMainParts::PreMainMessageLoopRun() ./../../chrome/browser/chrome_browser_main.cc:1083:18
    #17 0x55e63ba0b998 in content::BrowserMainLoop::PreMainMessageLoopRun() ./../../content/browser/browser_main_loop.cc:942:28
    #18 0x55e63cb4508c in Run ./../../base/callback.h:142:12
    #19 0x55e63cb4508c in content::StartupTaskRunner::RunAllTasksNow() ./../../content/browser/startup_task_runner.cc:43:29
    #20 0x55e63ba0afaa in content::BrowserMainLoop::CreateStartupTasks() ./../../content/browser/browser_main_loop.cc:850:25
    #21 0x55e63ba11636 in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams const&) ./../../content/browser/browser_main_runner_impl.cc:131:15
    #22 0x55e63ba0793b in content::BrowserMain(content::MainFunctionParams const&) ./../../content/browser/browser_main.cc:45:32
    #23 0x55e643c7c37b in RunBrowserProcessMain ./../../content/app/content_main_runner_impl.cc:641:10
    #24 0x55e643c7c37b in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) ./../../content/app/content_main_runner_impl.cc:1137:10
    #25 0x55e643c7b471 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:1004:12
    #26 0x55e643c7487d in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) ./../../content/app/content_main.cc:390:36
    #27 0x55e643c7653e in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:418:10
    #28 0x55e636ac8131 in ChromeMain ./../../chrome/app/chrome_main.cc:172:12
    #29 0x7f2abe1660b2 in __libc_start_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free (/home/pwn11/chromium/src/out/chrome_asan_shared/chrome+0xf4abf87)
Shadow bytes around the buggy address:
  0x0c06800a6360: fa fa fd fd fd fd fa fa 00 00 00 00 fa fa fd fd
  0x0c06800a6370: fd fa fa fa fd fd fd fa fa fa fd fd fd fa fa fa
  0x0c06800a6380: fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c06800a6390: fa fa fd fd fd fd fa fa fa fa fa fa fa fa fd fd
  0x0c06800a63a0: fd fd fa fa fd fd fd fa fa fa fd fd fd fa fa fa
=>0x0c06800a63b0: fd fd fd fa fa fa fd[fd]fd fa fa fa fd fd fd fa
  0x0c06800a63c0: fa fa 00 00 00 fa fa fa fa fa fa fa fa fa fa fa
  0x0c06800a63d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c06800a63e0: 00 00 07 fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c06800a63f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c06800a6400: fa fa fa fa 00 00 07 fa fa fa fa fa fa fa fa fa
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
==2453754==ABORTING
Received signal 6

Did this work before? N/A 

Chrome version:  97.0.4692.8   Channel: dev
OS Version: 20.04

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 543 B)

## Timeline

### [Deleted User] (2021-11-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-11-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5168381336289280.

### ts...@chromium.org (2021-11-11)

Assigning per content/browser/broadcast_channel/OWNERS 

[Monorail components: Blink>Messaging]

### me...@chromium.org (2021-11-11)

awillia: Could you PTAL? I think this is a bug in the new BroadcastChannel implementation.

BroadcastChannelProvider says "We store a raw pointer to the BroadcastChannelService since it's owned by the StoragePartitionImpl and should outlive any created BroadcastChannelProvider instance.", but I don't see anything that guarantees BroadcastChannelProvider instances won't outlive the storage partition.

### aw...@chromium.org (2021-11-11)

Investigating now

### aw...@chromium.org (2021-11-12)

I haven't been able to reproduce the UAF, but the new BroadcastChannel implementation does assume that StoragePartitionImpl will outlive BroadcastChannelProvider... From talking with mek@ about this, it's not safe to make this assumption, so our plan is to move away from using self-owned receivers and instead have BroadcastChannelService own the receivers+providers.

I have the corresponding code changes staged locally and will submit a CL in the morning once I determine whether any extra steps must be taken when submitting CLs that resolve security-related issues.

### aw...@chromium.org (2021-11-12)

CL submitted: https://chromium-review.googlesource.com/c/chromium/src/+/3276000

### gi...@appspot.gserviceaccount.com (2021-11-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/485d9ea92ff2dfc44d3021577c7a0919cc6e652c

commit 485d9ea92ff2dfc44d3021577c7a0919cc6e652c
Author: Andrew Williams <awillia@google.com>
Date: Mon Nov 15 22:17:12 2021

BroadcastChannel: Make providers be owned by the service

This moves the BroadcastChannelProviders from being owned by
self-owned receivers to being owned by the BroadcastChannelService
instance that they rely on. This ensures that the providers
can't outlive the service.

Bug: 1269344
Change-Id: I4eaa878d470501489307b916a05ad725b03bedf3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3276000
Reviewed-by: Ben Kelly <wanderview@chromium.org>
Reviewed-by: Ken Buchanan <kenrb@chromium.org>
Commit-Queue: Andrew Williams <awillia@google.com>
Cr-Commit-Position: refs/heads/main@{#941845}

[modify] https://crrev.com/485d9ea92ff2dfc44d3021577c7a0919cc6e652c/content/browser/broadcast_channel/broadcast_channel_service.cc
[modify] https://crrev.com/485d9ea92ff2dfc44d3021577c7a0919cc6e652c/content/browser/worker_host/shared_worker_host.cc
[modify] https://crrev.com/485d9ea92ff2dfc44d3021577c7a0919cc6e652c/content/browser/broadcast_channel/broadcast_channel_provider.cc
[modify] https://crrev.com/485d9ea92ff2dfc44d3021577c7a0919cc6e652c/content/browser/broadcast_channel/broadcast_channel_service.h
[modify] https://crrev.com/485d9ea92ff2dfc44d3021577c7a0919cc6e652c/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/485d9ea92ff2dfc44d3021577c7a0919cc6e652c/content/browser/broadcast_channel/broadcast_channel_provider.h
[modify] https://crrev.com/485d9ea92ff2dfc44d3021577c7a0919cc6e652c/content/browser/service_worker/service_worker_host.cc
[modify] https://crrev.com/485d9ea92ff2dfc44d3021577c7a0919cc6e652c/content/browser/worker_host/dedicated_worker_host.cc


### aw...@chromium.org (2021-11-16)

After changing `loop_cnt` to 2000 in the POC I was able to reproduce roughly every 20th time using `asan-linux-release-939805` on my specialist cloudtop machine.  After ~200 runs using `asan-linux-release-941921` I didn't reproduce the issue, so I think it's safe to conclude that the issue has now been resolved.

### [Deleted User] (2021-11-16)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2021-11-16)

I attempted to reproduce using `asan-linux-release-939805` without the `--incognito` flag but couldn't.  Using [1] as guidelines, does severity level High make sense for this issue?  Also, this issue was introduced in M97, so I believe we should use FoundIn-97.

CC mpdenton@ - please let me know what you think about this. Thank you!

[1] https://bugs.chromium.org/p/chromium/issues/detail?id=1100136#c8

### aw...@chromium.org (2021-11-17)

I'm going to tentatively apply the labels mentioned in my last comment so I can close this bug and submit a request to cherrypick these changes into M97 before the beta promotion.

### [Deleted User] (2021-11-17)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-17)

[Empty comment from Monorail migration]

### mp...@chromium.org (2021-11-17)

Looks like a profile shutdown bug. +amyressler@ I believe we decided this should be severity-high?

### [Deleted User] (2021-11-17)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-17)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-17)

Requesting merge to dev M97 because latest trunk commit (941845) appears to be after dev branch point (938553).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-17)

Merge approved: your change passed merge requirements and is auto-approved for M97. Please go ahead and merge the CL to branch 4692 (refs/branch-heads/4692) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2021-11-18)

M97 merge CL submitted, awaiting owner approval: https://chromium-review.googlesource.com/c/chromium/src/+/3289906

### [Deleted User] (2021-11-18)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6484ba06963e1365c708745a495e100d477ed42c

commit 6484ba06963e1365c708745a495e100d477ed42c
Author: Andrew Williams <awillia@google.com>
Date: Thu Nov 18 18:33:30 2021

BroadcastChannel: Make providers be owned by the service

This moves the BroadcastChannelProviders from being owned by
self-owned receivers to being owned by the BroadcastChannelService
instance that they rely on. This ensures that the providers
can't outlive the service.

(cherry picked from commit 485d9ea92ff2dfc44d3021577c7a0919cc6e652c)

Bug: 1269344
Change-Id: I4eaa878d470501489307b916a05ad725b03bedf3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3276000
Reviewed-by: Ben Kelly <wanderview@chromium.org>
Reviewed-by: Ken Buchanan <kenrb@chromium.org>
Commit-Queue: Andrew Williams <awillia@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#941845}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3289906
Auto-Submit: Andrew Williams <awillia@google.com>
Commit-Queue: Ken Buchanan <kenrb@chromium.org>
Cr-Commit-Position: refs/branch-heads/4692@{#277}
Cr-Branched-From: 038cd96142d384c0d2238973f1cb277725a62eba-refs/heads/main@{#938553}

[modify] https://crrev.com/6484ba06963e1365c708745a495e100d477ed42c/content/browser/worker_host/shared_worker_host.cc
[modify] https://crrev.com/6484ba06963e1365c708745a495e100d477ed42c/content/browser/broadcast_channel/broadcast_channel_service.cc
[modify] https://crrev.com/6484ba06963e1365c708745a495e100d477ed42c/content/browser/broadcast_channel/broadcast_channel_provider.cc
[modify] https://crrev.com/6484ba06963e1365c708745a495e100d477ed42c/content/browser/broadcast_channel/broadcast_channel_service.h
[modify] https://crrev.com/6484ba06963e1365c708745a495e100d477ed42c/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/6484ba06963e1365c708745a495e100d477ed42c/content/browser/broadcast_channel/broadcast_channel_provider.h
[modify] https://crrev.com/6484ba06963e1365c708745a495e100d477ed42c/content/browser/service_worker/service_worker_host.cc
[modify] https://crrev.com/6484ba06963e1365c708745a495e100d477ed42c/content/browser/worker_host/dedicated_worker_host.cc


### wf...@chromium.org (2021-11-23)

This is/was a critical sev since it was from the web to browser process.

### am...@google.com (2021-11-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-11-24)

Congratulations, Cassidy Kim! The VRP Panel has decided to award you $20,000 for this report. Nice work and thank you for this report!!

### am...@google.com (2021-11-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-05)

Hello OP, we consider attachments/pocs included with reports to be an integral part of the report (https://bughunters.google.com/about/rules/5745167867576320), so I've undeleted them. Thank you! 

### [Deleted User] (2022-02-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1269344?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057890)*
