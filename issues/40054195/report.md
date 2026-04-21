# uaf in media::learning::MojoLearningTaskControllerService::PredictDistribution

| Field | Value |
|-------|-------|
| **Issue ID** | [40054195](https://issues.chromium.org/issues/40054195) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media |
| **Platforms** | Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | li...@google.com |
| **Created** | 2020-12-17 |
| **Bounty** | $15,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36

Steps to reproduce the problem:
tested environment
os:ubuntu 20.04
Chromium 88.0.4324.11(dev with asan build)
Chromium 89.0.4350.4(dev with asan build)
Chromium 89.0.4355.0(latest canary)

./crome --user-data-dir=/tmp/non-exist --incognito http://localhost:8000/crash.html

repro is not 100% stable, because UAF is  triggered when the browser is closed. 
In my local test, the probability of repro is about 50%.

What is the expected behavior?

What went wrong?
==1808626==ERROR: AddressSanitizer: heap-use-after-free on address 0x60700044ca28 at pc 0x560d228c3615 bp 0x7ffc702810b0 sp 0x7ffc702810a8
READ of size 8 at 0x60700044ca28 thread T0 (chrome)
    #0 0x560d228c3614 in media::learning::WeakLearningTaskController::PredictDistribution(std::__1::vector<media::learning::Value, std::__1::allocator<media::learning::Value> > const&, base::OnceCallback<void (base::Optional<media::learning::TargetHistogram> const&)>) ./../../base/threading/sequence_bound.h:463
    #1 0x560d228c3614 in PredictDistribution ./../../media/learning/impl/learning_session_impl.cc:96
    #2 0x560d228c3614 in ?? ??:0
    #3 0x560d26a95e4d in media::learning::MojoLearningTaskControllerService::PredictDistribution(std::__1::vector<media::learning::Value, std::__1::allocator<media::learning::Value> > const&, base::OnceCallback<void (base::Optional<media::learning::TargetHistogram> const&)>) ./../../media/learning/mojo/mojo_learning_task_controller_service.cc:80
    #4 0x560d26a95e4d in ?? ??:0
    #5 0x560d14eed7ac in media::learning::mojom::LearningTaskControllerStubDispatch::AcceptWithResponder(media::learning::mojom::LearningTaskController*, mojo::Message*, std::__1::unique_ptr<mojo::MessageReceiverWithStatus, std::__1::default_delete<mojo::MessageReceiverWithStatus> >) ./gen/media/learning/mojo/public/mojom/learning_task_controller.mojom.cc:727
    #6 0x560d14eed7ac in ?? ??:0
    #7 0x560d26a38b2f in media::learning::mojom::LearningTaskControllerStub<mojo::RawPtrImplRefTraits<media::learning::mojom::LearningTaskController> >::AcceptWithResponder(mojo::Message*, std::__1::unique_ptr<mojo::MessageReceiverWithStatus, std::__1::default_delete<mojo::MessageReceiverWithStatus> >) ./gen/media/learning/mojo/public/mojom/learning_task_controller.mojom.h:171
    #8 0x560d26a38b2f in ?? ??:0
    #9 0x560d1fd21784 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:528
    #10 0x560d1fd21784 in ?? ??:0
    #11 0x560d1fd2e646 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:41
    #12 0x560d1fd2e646 in ?? ??:0
    #13 0x560d1fd3a14c in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:955
    #14 0x560d1fd3a14c in ?? ??:0
    #15 0x560d1fd38888 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:622
    #16 0x560d1fd38888 in ?? ??:0
    #17 0x560d1fd2e646 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:41
    #18 0x560d1fd2e646 in ?? ??:0
    #19 0x560d1fd1a518 in mojo::Connector::DispatchMessage(mojo::Message) ./../../mojo/public/cpp/bindings/lib/connector.cc:508
    #20 0x560d1fd1a518 in ?? ??:0
    #21 0x560d1fd1c9db in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:566
    #22 0x560d1fd1c9db in ?? ??:0
    #23 0x560d1fd83632 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../base/callback.h:168
    #24 0x560d1fd83632 in OnHandleReady ./../../mojo/public/cpp/system/simple_watcher.cc:278
    #25 0x560d1fd83632 in ?? ??:0
    #26 0x560d1fd85094 in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:498
    #27 0x560d1fd85094 in MakeItSo<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> ./../../base/bind_internal.h:657
    #28 0x560d1fd85094 in RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), std::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0, 1, 2, 3> ./../../base/bind_internal.h:710
    #29 0x560d1fd85094 in RunOnce ./../../base/bind_internal.h:679
    #30 0x560d1fd85094 in ?? ??:0
    #31 0x560d1e3b5e47 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/callback.h:101
    #32 0x560d1e3b5e47 in RunTask ./../../base/task/common/task_annotator.cc:163
    #33 0x560d1e3b5e47 in ?? ??:0
    #34 0x560d1e3f3431 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:351
    #35 0x560d1e3f3431 in ?? ??:0
    #36 0x560d1e3f2b74 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:264
    #37 0x560d1e3f2b74 in ?? ??:0
    #38 0x560d1e2e0750 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_glib.cc:404
    #39 0x560d1e2e0750 in ?? ??:0
    #40 0x560d1e3f540c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:460
    #41 0x560d1e3f540c in ?? ??:0
    #42 0x560d1e3636b0 in base::RunLoop::Run() ./../../base/run_loop.cc:131
    #43 0x560d1e3636b0 in ?? ??:0
    #44 0x560d1ee59b80 in ChromeBrowserMainParts::MainMessageLoopRun(int*) ./../../chrome/browser/chrome_browser_main.cc:1733
    #45 0x560d1ee59b80 in ?? ??:0
    #46 0x560d177918e8 in content::BrowserMainLoop::RunMainMessageLoopParts() ./../../content/browser/browser_main_loop.cc:1013
    #47 0x560d177918e8 in ?? ??:0
    #48 0x560d177976f5 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser_main_runner_impl.cc:150
    #49 0x560d177976f5 in ?? ??:0
    #50 0x560d17789805 in content::BrowserMain(content::MainFunctionParams const&) ./../../content/browser/browser_main.cc:47
    #51 0x560d17789805 in ?? ??:0
    #52 0x560d1e0c48fb in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) ./../../content/app/content_main_runner_impl.cc:535
    #53 0x560d1e0c48fb in RunBrowser ./../../content/app/content_main_runner_impl.cc:1031
    #54 0x560d1e0c48fb in ?? ??:0
    #55 0x560d1e0c3bb2 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:900
    #56 0x560d1e0c3bb2 in ?? ??:0
    #57 0x560d1e0bdcde in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) ./../../content/app/content_main.cc:372
    #58 0x560d1e0bdcde in ?? ??:0
    #59 0x560d1e0be2cc in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:398
    #60 0x560d1e0be2cc in ?? ??:0
    #61 0x560d13026667 in ChromeMain ./../../chrome/app/chrome_main.cc:130
    #62 0x560d13026667 in ?? ??:0
    #63 0x7f59e02130b2 in __libc_start_main ??:?
    #64 0x7f59e02130b2 in ?? ??:0

0x60700044ca28 is located 56 bytes inside of 80-byte region [0x60700044c9f0,0x60700044ca40)
freed by thread T0 (chrome) here:
    #0 0x560d130243ad in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160
    #1 0x560d130243ad in ?? ??:0
    #2 0x560d228c0ab1 in std::__1::__tree<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, base::SequenceBound<media::learning::LearningTaskController> >, std::__1::__map_value_compare<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, base::SequenceBound<media::learning::LearningTaskController> >, std::__1::less<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > >, true>, std::__1::allocator<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, base::SequenceBound<media::learning::LearningTaskController> > > >::destroy(std::__1::__tree_node<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, base::SequenceBound<media::learning::LearningTaskController> >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/__tree:1830
    #3 0x560d228c0ab1 in ?? ??:0
    #4 0x560d228bebbe in media::learning::LearningSessionImpl::~LearningSessionImpl() ./../../buildtools/third_party/libc++/trunk/include/__tree:1821
    #5 0x560d228bebbe in ~map ./../../buildtools/third_party/libc++/trunk/include/map:1090
    #6 0x560d228bebbe in ~LearningSessionImpl ./../../media/learning/impl/learning_session_impl.cc:122
    #7 0x560d228bebbe in ?? ??:0
    #8 0x560d228bec4d in media::learning::LearningSessionImpl::~LearningSessionImpl() ./../../media/learning/impl/learning_session_impl.cc:122
    #9 0x560d228bec4d in ?? ??:0
    #10 0x560d1e3a974d in std::__1::__tree<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, std::__1::__map_value_compare<void const*, std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, std::__1::less<void const*>, true>, std::__1::allocator<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > > > >::destroy(std::__1::__tree_node<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/memory:2378
    #11 0x560d1e3a974d in reset ./../../buildtools/third_party/libc++/trunk/include/memory:2633
    #12 0x560d1e3a974d in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/memory:2587
    #13 0x560d1e3a974d in ~pair ./../../buildtools/third_party/libc++/trunk/include/utility:297
    #14 0x560d1e3a974d in __destroy<std::pair<const void *const, std::unique_ptr<base::SupportsUserData::Data> > > ./../../buildtools/third_party/libc++/trunk/include/memory:1787
    #15 0x560d1e3a974d in destroy<std::pair<const void *const, std::unique_ptr<base::SupportsUserData::Data> > > ./../../buildtools/third_party/libc++/trunk/include/memory:1619
    #16 0x560d1e3a974d in destroy ./../../buildtools/third_party/libc++/trunk/include/__tree:1833
    #17 0x560d1e3a974d in ?? ??:0
    #18 0x560d1e3a96e1 in std::__1::__tree<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, std::__1::__map_value_compare<void const*, std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, std::__1::less<void const*>, true>, std::__1::allocator<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > > > >::destroy(std::__1::__tree_node<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/__tree:1830
    #19 0x560d1e3a96e1 in ?? ??:0
    #20 0x560d1e3a96e1 in std::__1::__tree<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, std::__1::__map_value_compare<void const*, std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, std::__1::less<void const*>, true>, std::__1::allocator<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > > > >::destroy(std::__1::__tree_node<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/__tree:1830
    #21 0x560d1e3a96e1 in ?? ??:0
    #22 0x560d1e3a91d7 in base::SupportsUserData::~SupportsUserData() ./../../buildtools/third_party/libc++/trunk/include/__tree:1821
    #23 0x560d1e3a91d7 in ~map ./../../buildtools/third_party/libc++/trunk/include/map:1090
    #24 0x560d1e3a91d7 in ~SupportsUserData ./../../base/supports_user_data.cc:67
    #25 0x560d1e3a91d7 in ?? ??:0
    #26 0x560d17705970 in content::BrowserContext::~BrowserContext() ./../../content/browser/browser_context.cc:518
    #27 0x560d17705970 in ?? ??:0
    #28 0x560d1f3e53fd in OffTheRecordProfileImpl::~OffTheRecordProfileImpl() ./../../chrome/browser/profiles/off_the_record_profile_impl.cc:191
    #29 0x560d1f3e53fd in ?? ??:0
    #30 0x560d1f3be43b in std::__1::__tree<std::__1::__value_type<Profile::OTRProfileID, std::__1::unique_ptr<Profile, std::__1::default_delete<Profile> > >, std::__1::__map_value_compare<Profile::OTRProfileID, std::__1::__value_type<Profile::OTRProfileID, std::__1::unique_ptr<Profile, std::__1::default_delete<Profile> > >, std::__1::less<Profile::OTRProfileID>, true>, std::__1::allocator<std::__1::__value_type<Profile::OTRProfileID, std::__1::unique_ptr<Profile, std::__1::default_delete<Profile> > > > >::erase(std::__1::__tree_const_iterator<std::__1::__value_type<Profile::OTRProfileID, std::__1::unique_ptr<Profile, std::__1::default_delete<Profile> > >, std::__1::__tree_node<std::__1::__value_type<Profile::OTRProfileID, std::__1::unique_ptr<Profile, std::__1::default_delete<Profile> > >, void*>*, long>) ./../../buildtools/third_party/libc++/trunk/include/memory:2378
    #31 0x560d1f3be43b in reset ./../../buildtools/third_party/libc++/trunk/include/memory:2633
    #32 0x560d1f3be43b in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/memory:2587
    #33 0x560d1f3be43b in ~pair ./../../buildtools/third_party/libc++/trunk/include/utility:297
    #34 0x560d1f3be43b in __destroy<std::pair<const Profile::OTRProfileID, std::unique_ptr<Profile> > > ./../../buildtools/third_party/libc++/trunk/include/memory:1787
    #35 0x560d1f3be43b in destroy<std::pair<const Profile::OTRProfileID, std::unique_ptr<Profile> > > ./../../buildtools/third_party/libc++/trunk/include/memory:1619
    #36 0x560d1f3be43b in erase ./../../buildtools/third_party/libc++/trunk/include/__tree:2519
    #37 0x560d1f3be43b in ?? ??:0
    #38 0x560d1f3b69c9 in ProfileImpl::DestroyOffTheRecordProfile(Profile*) ./../../buildtools/third_party/libc++/trunk/include/__tree:2542
    #39 0x560d1f3b69c9 in erase ./../../buildtools/third_party/libc++/trunk/include/map:1304
    #40 0x560d1f3b69c9 in DestroyOffTheRecordProfile ./../../chrome/browser/profiles/profile_impl.cc:983
    #41 0x560d1f3b69c9 in ?? ??:0
    #42 0x560d1f3c3374 in ProfileDestroyer::DestroyOffTheRecordProfileNow(Profile*) ./../../chrome/browser/profiles/profile_destroyer.cc:85
    #43 0x560d1f3c3374 in ?? ??:0
    #44 0x560d1f3c18f0 in ProfileDestroyer::DestroyProfileWhenAppropriate(Profile*) ./../../chrome/browser/profiles/profile_destroyer.cc:62
    #45 0x560d1f3c18f0 in ?? ??:0
    #46 0x560d2893311a in Browser::~Browser() ./../../chrome/browser/ui/browser.cc:618
    #47 0x560d2893311a in ?? ??:0
    #48 0x560d289343bd in Browser::~Browser() ./../../chrome/browser/ui/browser.cc:542
    #49 0x560d289343bd in ?? ??:0
    #50 0x560d28f9c248 in BrowserView::~BrowserView() ./../../buildtools/third_party/libc++/trunk/include/memory:2378
    #51 0x560d28f9c248 in reset ./../../buildtools/third_party/libc++/trunk/include/memory:2633
    #52 0x560d28f9c248 in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/memory:2587
    #53 0x560d28f9c248 in ~BrowserView ./../../chrome/browser/ui/views/frame/browser_view.cc:670
    #54 0x560d28f9c248 in ?? ??:0
    #55 0x560d28f9cab7 in non-virtual thunk to BrowserView::~BrowserView() ./../../chrome/browser/ui/views/frame/browser_view.cc:635
    #56 0x560d28f9cab7 in ?? ??:0
    #57 0x560d283fdb79 in ?? ??:0
    #58 0x560d283fdb79 in views::View::~View() ./../../ui/views/view.cc:220
    #59 0x560d283fdb79 in ?? ??:0
    #60 0x560d284ab11b in views::NonClientView::~NonClientView() ./../../ui/views/window/non_client_view.cc:164
    #61 0x560d284ab11b in ~NonClientView ./../../ui/views/window/non_client_view.cc:160
    #62 0x560d284ab11b in ?? ??:0
    #63 0x560d28400e83 in views::View::DoRemoveChildView(views::View*, bool, bool, views::View*) ./../../buildtools/third_party/libc++/trunk/include/memory:2378
    #64 0x560d28400e83 in reset ./../../buildtools/third_party/libc++/trunk/include/memory:2633
    #65 0x560d28400e83 in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/memory:2587
    #66 0x560d28400e83 in DoRemoveChildView ./../../ui/views/view.cc:2474
    #67 0x560d28400e83 in ?? ??:0
    #68 0x560d28401185 in views::View::RemoveAllChildViews(bool) ./../../ui/views/view.cc:287
    #69 0x560d28401185 in ?? ??:0
    #70 0x560d2845f34c in views::Widget::~Widget() ./../../ui/views/widget/widget.cc:1536
    #71 0x560d2845f34c in ~Widget ./../../ui/views/widget/widget.cc:178
    #72 0x560d2845f34c in ?? ??:0
    #73 0x560d28fd13ad in BrowserFrame::~BrowserFrame() ./../../chrome/browser/ui/views/frame/browser_frame.cc:76
    #74 0x560d28fd13ad in ?? ??:0
    #75 0x560d2850dc4f in views::DesktopNativeWidgetAura::~DesktopNativeWidgetAura() desktop_native_widget_aura.cc:?
    #76 0x560d2850dc4f in ?? ??:0
    #77 0x560d290adad6 in DesktopBrowserFrameAuraLinux::~DesktopBrowserFrameAuraLinux() ./../../chrome/browser/ui/views/frame/desktop_browser_frame_aura_linux.cc:29
    #78 0x560d290adad6 in ~DesktopBrowserFrameAuraLinux ./../../chrome/browser/ui/views/frame/desktop_browser_frame_aura_linux.cc:29
    #79 0x560d290adad6 in ?? ??:0
    #80 0x560d2854b203 in views::DesktopWindowTreeHostPlatform::OnClosed() ./../../ui/views/widget/desktop_aura/desktop_window_tree_host_platform.cc:683
    #81 0x560d2854b203 in ?? ??:0
    #82 0x560d284fa3ab in views::DesktopWindowTreeHostLinux::OnClosed() ./../../ui/views/widget/desktop_aura/desktop_window_tree_host_linux.cc:248
    #83 0x560d284fa3ab in ?? ??:0
    #84 0x560d28543926 in views::DesktopWindowTreeHostPlatform::CloseNow() ./../../ui/views/widget/desktop_aura/desktop_window_tree_host_platform.cc:279
    #85 0x560d28543926 in ?? ??:0
    #86 0x560d2854cee4 in base::internal::Invoker<base::internal::BindState<void (views::DesktopWindowTreeHostPlatform::*)(), base::WeakPtr<views::DesktopWindowTreeHostPlatform> >, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:498
    #87 0x560d2854cee4 in MakeItSo<void (views::DesktopWindowTreeHostPlatform::*)(), base::WeakPtr<views::DesktopWindowTreeHostPlatform>> ./../../base/bind_internal.h:657
    #88 0x560d2854cee4 in RunImpl<void (views::DesktopWindowTreeHostPlatform::*)(), std::tuple<base::WeakPtr<views::DesktopWindowTreeHostPlatform> >, 0> ./../../base/bind_internal.h:710
    #89 0x560d2854cee4 in RunOnce ./../../base/bind_internal.h:679
    #90 0x560d2854cee4 in ?? ??:0

previously allocated by thread T0 (chrome) here:
    #0 0x560d13023b4d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99
    #1 0x560d13023b4d in ?? ??:0
    #2 0x560d228c488d in std::__1::pair<std::__1::__tree_iterator<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, base::SequenceBound<media::learning::LearningTaskController> >, std::__1::__tree_node<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, base::SequenceBound<media::learning::LearningTaskController> >, void*>*, long>, bool> std::__1::__tree<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, base::SequenceBound<media::learning::LearningTaskController> >, std::__1::__map_value_compare<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, base::SequenceBound<media::learning::LearningTaskController> >, std::__1::less<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > >, true>, std::__1::allocator<std::__1::__value_type<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, base::SequenceBound<media::learning::LearningTaskController> > > >::__emplace_unique_key_args<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, base::SequenceBound<media::learning::LearningTaskController> >(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, base::SequenceBound<media::learning::LearningTaskController>&&) ./../../buildtools/third_party/libc++/trunk/include/new:253
    #3 0x560d228c488d in allocate ./../../buildtools/third_party/libc++/trunk/include/memory:1853
    #4 0x560d228c488d in allocate ./../../buildtools/third_party/libc++/trunk/include/memory:1570
    #5 0x560d228c488d in __construct_node<const std::basic_string<char> &, base::SequenceBound<media::learning::LearningTaskController> > ./../../buildtools/third_party/libc++/trunk/include/__tree:2190
    #6 0x560d228c488d in __emplace_unique_key_args<std::basic_string<char>, const std::basic_string<char> &, base::SequenceBound<media::learning::LearningTaskController> > ./../../buildtools/third_party/libc++/trunk/include/__tree:2136
    #7 0x560d228c488d in ?? ??:0
    #8 0x560d228bf2b5 in media::learning::LearningSessionImpl::RegisterTask(media::learning::LearningTask const&, base::SequenceBound<media::learning::FeatureProvider>) ./../../buildtools/third_party/libc++/trunk/include/__tree:1179
    #9 0x560d228bf2b5 in emplace<const std::basic_string<char> &, base::SequenceBound<media::learning::LearningTaskController> > ./../../buildtools/third_party/libc++/trunk/include/map:1148
    #10 0x560d228bf2b5 in RegisterTask ./../../media/learning/impl/learning_session_impl.cc:145
    #11 0x560d228bf2b5 in ?? ??:0
    #12 0x560d17708b73 in base::internal::Invoker<base::internal::BindState<content::BrowserContext::GetLearningSession()::$_0, media::learning::LearningSessionImpl*>, void (media::learning::LearningTask const&)>::Run(base::internal::BindStateBase*, media::learning::LearningTask const&) ./../../content/browser/browser_context.cc:594
    #13 0x560d17708b73 in Invoke<const (lambda at ../../content/browser/browser_context.cc:592:9) &, media::learning::LearningSessionImpl *const &, const media::learning::LearningTask &> ./../../base/bind_internal.h:379
    #14 0x560d17708b73 in MakeItSo<const (lambda at ../../content/browser/browser_context.cc:592:9) &, media::learning::LearningSessionImpl *const &, const media::learning::LearningTask &> ./../../base/bind_internal.h:637
    #15 0x560d17708b73 in RunImpl<const (lambda at ../../content/browser/browser_context.cc:592:9) &, const std::tuple<media::learning::LearningSessionImpl *> &, 0> ./../../base/bind_internal.h:710
    #16 0x560d17708b73 in Run ./../../base/bind_internal.h:692
    #17 0x560d17708b73 in ?? ??:0
    #18 0x560d224accb8 in media::learning::MediaLearningTasks::Register(base::RepeatingCallback<void (media::learning::LearningTask const&)>) ./../../base/callback.h:168
    #19 0x560d224accb8 in Register ./../../media/learning/common/media_learning_tasks.cc:97
    #20 0x560d224accb8 in ?? ??:0
    #21 0x560d17706f90 in content::BrowserContext::GetLearningSession() ./../../content/browser/browser_context.cc:597
    #22 0x560d17706f90 in ?? ??:0
    #23 0x560d183ccbb9 in base::internal::Invoker<base::internal::BindState<content::RenderFrameHostImpl::BindMediaMetricsProviderReceiver(mojo::PendingReceiver<media::mojom::MediaMetricsProvider>)::$_20, base::WeakPtr<content::RenderFrameHostImpl> >, media::learning::LearningSession* ()>::Run(base::internal::BindStateBase*) ./../../content/browser/renderer_host/render_frame_host_impl.cc:7786
    #24 0x560d183ccbb9 in Invoke<const (lambda at ../../content/browser/renderer_host/render_frame_host_impl.cc:7777:11) &, const base::WeakPtr<content::RenderFrameHostImpl> &> ./../../base/bind_internal.h:379
    #25 0x560d183ccbb9 in MakeItSo<const (lambda at ../../content/browser/renderer_host/render_frame_host_impl.cc:7777:11) &, const base::WeakPtr<content::RenderFrameHostImpl> &> ./../../base/bind_internal.h:637
    #26 0x560d183ccbb9 in RunImpl<const (lambda at ../../content/browser/renderer_host/render_frame_host_impl.cc:7777:11) &, const std::tuple<base::WeakPtr<content::RenderFrameHostImpl> > &, 0> ./../../base/bind_internal.h:710
    #27 0x560d183ccbb9 in Run ./../../base/bind_internal.h:692
    #28 0x560d183ccbb9 in ?? ??:0
    #29 0x560d26a33d5d in media::MediaMetricsProvider::AcquireLearningTaskController(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, mojo::PendingReceiver<media::learning::mojom::LearningTaskController>) ./../../base/callback.h:168
    #30 0x560d26a33d5d in AcquireLearningTaskController ./../../media/mojo/services/media_metrics_provider.cc:304
    #31 0x560d26a33d5d in ?? ??:0
    #32 0x560d14c6d19b in media::mojom::MediaMetricsProviderStubDispatch::Accept(media::mojom::MediaMetricsProvider*, mojo::Message*) ./gen/media/mojo/mojom/media_metrics_provider.mojom.cc:1218
    #33 0x560d14c6d19b in ?? ??:0
    #34 0x560d1fd21836 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:554
    #35 0x560d1fd21836 in ?? ??:0
    #36 0x560d1fd2e646 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:41
    #37 0x560d1fd2e646 in ?? ??:0
    #38 0x560d1fd3a14c in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:955
    #39 0x560d1fd3a14c in ?? ??:0
    #40 0x560d1fd38888 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:622
    #41 0x560d1fd38888 in ?? ??:0
    #42 0x560d1fd2e646 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:41
    #43 0x560d1fd2e646 in ?? ??:0
    #44 0x560d1fd1a518 in mojo::Connector::DispatchMessage(mojo::Message) ./../../mojo/public/cpp/bindings/lib/connector.cc:508
    #45 0x560d1fd1a518 in ?? ??:0
    #46 0x560d1fd1c9db in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:566
    #47 0x560d1fd1c9db in ?? ??:0
    #48 0x560d1fd83632 in Run ./../../base/callback.h:168
    #49 0x560d1fd83632 in OnHandleReady ./../../mojo/public/cpp/system/simple_watcher.cc:278
    #50 0x560d1fd83632 in ?? ??:0
    #51 0x560d1fd85094 in Invoke<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> ./../../base/bind_internal.h:498
    #52 0x560d1fd85094 in MakeItSo<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> ./../../base/bind_internal.h:657
    #53 0x560d1fd85094 in RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), std::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0, 1, 2, 3> ./../../base/bind_internal.h:710
    #54 0x560d1fd85094 in RunOnce ./../../base/bind_internal.h:679
    #55 0x560d1fd85094 in ?? ??:0
    #56 0x560d1e3b5e47 in Run ./../../base/callback.h:101
    #57 0x560d1e3b5e47 in RunTask ./../../base/task/common/task_annotator.cc:163
    #58 0x560d1e3b5e47 in ?? ??:0
    #59 0x560d1e3f3431 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:351
    #60 0x560d1e3f3431 in ?? ??:0
    #61 0x560d1e3f2b74 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:264
    #62 0x560d1e3f2b74 in ?? ??:0
    #63 0x560d1e2e0750 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_glib.cc:404
    #64 0x560d1e2e0750 in ?? ??:0
    #65 0x560d1e3f540c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:460
    #66 0x560d1e3f540c in ?? ??:0
    #67 0x560d1e3636b0 in base::RunLoop::Run() ./../../base/run_loop.cc:131
    #68 0x560d1e3636b0 in ?? ??:0
    #69 0x560d1ee59b80 in ChromeBrowserMainParts::MainMessageLoopRun(int*) ./../../chrome/browser/chrome_browser_main.cc:1733
    #70 0x560d1ee59b80 in ?? ??:0
    #71 0x560d177918e8 in content::BrowserMainLoop::RunMainMessageLoopParts() ./../../content/browser/browser_main_loop.cc:1013
    #72 0x560d177918e8 in ?? ??:0
    #73 0x560d177976f5 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser_main_runner_impl.cc:150
    #74 0x560d177976f5 in ?? ??:0
    #75 0x560d17789805 in content::BrowserMain(content::MainFunctionParams const&) ./../../content/browser/browser_main.cc:47
    #76 0x560d17789805 in ?? ??:0
    #77 0x560d1e0c48fb in RunBrowserProcessMain ./../../content/app/content_main_runner_impl.cc:535
    #78 0x560d1e0c48fb in RunBrowser ./../../content/app/content_main_runner_impl.cc:1031
    #79 0x560d1e0c48fb in ?? ??:0
    #80 0x560d1e0c3bb2 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:900
    #81 0x560d1e0c3bb2 in ?? ??:0

SUMMARY: AddressSanitizer: heap-use-after-free (/home/pwnexp/asan-linux-release/chrome+0x19c40614)
Shadow bytes around the buggy address:
  0x0c0e800818f0: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c0e80081900: fd fd fa fa fa fa fd fd fd fd fd fd fd fd fd fd
  0x0c0e80081910: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fa fa
  0x0c0e80081920: fa fa fd fd fd fd fd fd fd fd fd fd fa fa fa fa
  0x0c0e80081930: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fd fd
=>0x0c0e80081940: fd fd fd fd fd[fd]fd fd fa fa fa fa fd fd fd fd
  0x0c0e80081950: fd fd fd fd fd fd fa fa fa fa 00 00 00 00 00 00
  0x0c0e80081960: 00 00 00 fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c0e80081970: fd fd fa fa fa fa fd fd fd fd fd fd fd fd fd fd
  0x0c0e80081980: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fa fa
  0x0c0e80081990: fa fa 00 00 00 00 00 00 00 00 00 00 fa fa fa fa
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
==1808626==ABORTING
Received signal 6
    #0 0x560d12fb635b in __interceptor_backtrace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4186
    #1 0x560d12fb635b in ?? ??:0
    #2 0x560d1e4a2fb9 in base::debug::CollectStackTrace(void**, unsigned long) ./../../base/debug/stack_trace_posix.cc:833
    #3 0x560d1e4a2fb9 in ?? ??:0
    #4 0x560d1e28ca63 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:198
    #5 0x560d1e28ca63 in StackTrace ./../../base/debug/stack_trace.cc:195
    #6 0x560d1e28ca63 in ?? ??:0
    #7 0x560d1e4a1b8f in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:345
    #8 0x560d1e4a1b8f in ?? ??:0
    #9 0x7f59e208f3c0 in __funlockfile :?
    #10 0x7f59e208f3c0 in ?? ??:0
    #11 0x7f59e023218b in gsignal ??:?
    #12 0x7f59e023218b in ?? ??:0
    #13 0x7f59e0211859 in abort ??:?
    #14 0x7f59e0211859 in ?? ??:0
    #15 0x560d13012cf7 in __sanitizer::Abort() /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_posix_libcdep.cpp:151
    #16 0x560d13012cf7 in ?? ??:0
    #17 0x560d13011871 in __sanitizer::Die() /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_termination.cpp:58
    #18 0x560d13011871 in ?? ??:0
    #19 0x560d12ffdcd4 in __asan::ScopedInErrorReport::~ScopedInErrorReport() /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_report.cpp:190
    #20 0x560d12ffdcd4 in ?? ??:0
    #21 0x560d12fff6be in __asan::ReportGenericError(unsigned long, unsigned long, unsigned long, unsigned long, bool, unsigned long, unsigned int, bool) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_report.cpp:478
    #22 0x560d12fff6be in ?? ??:0
    #23 0x560d12ffff48 in __asan_report_load8 /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_rtl.cpp:121
    #24 0x560d12ffff48 in ?? ??:0
    #25 0x560d228c3615 in WithArgs<const std::vector<media::learning::Value> &, base::OnceCallback<void (const base::Optional<media::learning::TargetHistogram> &)> > ./../../base/threading/sequence_bound.h:463
    #26 0x560d228c3615 in PredictDistribution ./../../media/learning/impl/learning_session_impl.cc:96
    #27 0x560d228c3615 in ?? ??:0
    #28 0x560d26a95e4e in media::learning::MojoLearningTaskControllerService::PredictDistribution(std::__1::vector<media::learning::Value, std::__1::allocator<media::learning::Value> > const&, base::OnceCallback<void (base::Optional<media::learning::TargetHistogram> const&)>) ./../../media/learning/mojo/mojo_learning_task_controller_service.cc:80
    #29 0x560d26a95e4e in ?? ??:0
    #30 0x560d14eed7ad in media::learning::mojom::LearningTaskControllerStubDispatch::AcceptWithResponder(media::learning::mojom::LearningTaskController*, mojo::Message*, std::__1::unique_ptr<mojo::MessageReceiverWithStatus, std::__1::default_delete<mojo::MessageReceiverWithStatus> >) ./gen/media/learning/mojo/public/mojom/learning_task_controller.mojom.cc:727
    #31 0x560d14eed7ad in ?? ??:0
    #32 0x560d26a38b30 in media::learning::mojom::LearningTaskControllerStub<mojo::RawPtrImplRefTraits<media::learning::mojom::LearningTaskController> >::AcceptWithResponder(mojo::Message*, std::__1::unique_ptr<mojo::MessageReceiverWithStatus, std::__1::default_delete<mojo::MessageReceiverWithStatus> >) ./gen/media/learning/mojo/public/mojom/learning_task_controller.mojom.h:171
    #33 0x560d26a38b30 in ?? ??:0
    #34 0x560d1fd21785 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:528
    #35 0x560d1fd21785 in ?? ??:0
    #36 0x560d1fd2e647 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:41
    #37 0x560d1fd2e647 in ?? ??:0
    #38 0x560d1fd3a14d in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:955
    #39 0x560d1fd3a14d in ?? ??:0
    #40 0x560d1fd38889 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:622
    #41 0x560d1fd38889 in ?? ??:0
    #42 0x560d1fd2e647 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:41
    #43 0x560d1fd2e647 in ?? ??:0
    #44 0x560d1fd1a519 in mojo::Connector::DispatchMessage(mojo::Message) ./../../mojo/public/cpp/bindings/lib/connector.cc:508
    #45 0x560d1fd1a519 in ?? ??:0
    #46 0x560d1fd1c9dc in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:566
    #47 0x560d1fd1c9dc in ?? ??:0
    #48 0x560d1fd83633 in Run ./../../base/callback.h:168
    #49 0x560d1fd83633 in OnHandleReady ./../../mojo/public/cpp/system/simple_watcher.cc:278
    #50 0x560d1fd83633 in ?? ??:0
    #51 0x560d1fd85095 in Invoke<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> ./../../base/bind_internal.h:498
    #52 0x560d1fd85095 in MakeItSo<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> ./../../base/bind_internal.h:657
    #53 0x560d1fd85095 in RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), std::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0, 1, 2, 3> ./../../base/bind_internal.h:710
    #54 0x560d1fd85095 in RunOnce ./../../base/bind_internal.h:679
    #55 0x560d1fd85095 in ?? ??:0
    #56 0x560d1e3b5e48 in Run ./../../base/callback.h:101
    #57 0x560d1e3b5e48 in RunTask ./../../base/task/common/task_annotator.cc:163
    #58 0x560d1e3b5e48 in ?? ??:0
    #59 0x560d1e3f3432 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:351
    #60 0x560d1e3f3432 in ?? ??:0
    #61 0x560d1e3f2b75 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:264
    #62 0x560d1e3f2b75 in ?? ??:0
    #63 0x560d1e2e0751 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_glib.cc:404
    #64 0x560d1e2e0751 in ?? ??:0
    #65 0x560d1e3f540d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:460
    #66 0x560d1e3f540d in ?? ??:0
    #67 0x560d1e3636b1 in base::RunLoop::Run() ./../../base/run_loop.cc:131
    #68 0x560d1e3636b1 in ?? ??:0
    #69 0x560d1ee59b81 in ChromeBrowserMainParts::MainMessageLoopRun(int*) ./../../chrome/browser/chrome_browser_main.cc:1733
    #70 0x560d1ee59b81 in ?? ??:0
    #71 0x560d177918e9 in content::BrowserMainLoop::RunMainMessageLoopParts() ./../../content/browser/browser_main_loop.cc:1013
    #72 0x560d177918e9 in ?? ??:0
    #73 0x560d177976f6 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser_main_runner_impl.cc:150
    #74 0x560d177976f6 in ?? ??:0
    #75 0x560d17789806 in content::BrowserMain(content::MainFunctionParams const&) ./../../content/browser/browser_main.cc:47
    #76 0x560d17789806 in ?? ??:0
    #77 0x560d1e0c48fc in RunBrowserProcessMain ./../../content/app/content_main_runner_impl.cc:535
    #78 0x560d1e0c48fc in RunBrowser ./../../content/app/content_main_runner_impl.cc:1031
    #79 0x560d1e0c48fc in ?? ??:0
    #80 0x560d1e0c3bb3 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:900
    #81 0x560d1e0c3bb3 in ?? ??:0
    #82 0x560d1e0bdcdf in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) ./../../content/app/content_main.cc:372
    #83 0x560d1e0bdcdf in ?? ??:0
    #84 0x560d1e0be2cd in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:398
    #85 0x560d1e0be2cd in ?? ??:0
    #86 0x560d13026668 in ChromeMain ./../../chrome/app/chrome_main.cc:130
    #87 0x560d13026668 in ?? ??:0
    #88 0x7f59e02130b3 in __libc_start_main ??:?
    #89 0x7f59e02130b3 in ?? ??:0
    #90 0x560d12f7f86a in _start ??:?
    #91 0x560d12f7f86a in ?? ??:0
  r8: 0000000000000000  r9: 00007ffc702800f0 r10: 0000000000000008 r11: 0000000000000246
 r12: 00007ffc702810a8 r13: 00007ffc702810b0 r14: 00007ffc70281050 r15: 0000560d34fd4488
  di: 0000000000000002  si: 00007ffc702800f0  bp: 00007ffc70281080  bx: 00007f59df11ae00
  dx: 0000000000000000  ax: 0000000000000000  cx: 00007f59e023218b  sp: 00007ffc702800f0
  ip: 00007f59e023218b efl: 0000000000000246 cgf: 002b000000000033 erf: 0000000000000000
 trp: 0000000000000000 msk: 0000000000000000 cr2: 0000000000000000
[end of stack trace]
Calling _exit(1). Core file will not be generated.

Did this work before? N/A 

Chrome version: 88.0.4324.11(dev with asan build)  Channel: dev
OS Version: 20.04
Flash Version:

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 726 B)
- [testharness.js](attachments/testharness.js) (text/plain, 141.4 KB)

## Timeline

### [Deleted User] (2020-12-17)

[Empty comment from Monorail migration]

### em...@gmail.com (2020-12-17)

I just missed a repro step. 
Opening multiple tabs will increases the probability of repro. 
For example: 
./chrome --user-data-dir=/tmp/non-exist --incognito http://localhost:8000/crash.html http://localhost:8000/crash.html http://localhost:8000/crash.html http://localhost:8000/crash.html http://localhost:8000/crash.html http://localhost:8000/crash.html

### cl...@chromium.org (2020-12-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5733882929676288.

### cl...@chromium.org (2020-12-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5683300252581888.

### ca...@chromium.org (2020-12-22)

Looks like CF couldn't reproduce, and I can't either on latest asan. liberato: Can you try reproducing this (and reassign as appropriate) Thanks.



### ca...@chromium.org (2020-12-22)

[Empty comment from Monorail migration]

[Monorail components: Internals>Media]

### ca...@chromium.org (2020-12-22)

[Empty comment from Monorail migration]

### li...@google.com (2020-12-22)

thanks, i'll take a look.

+chcunningham, FYI.

### [Deleted User] (2020-12-23)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### li...@google.com (2020-12-23)

there's a missing weak ptr guard at [1].  should check for `!weak_session_`.  i'll put out a cl.

[1] https://source.chromium.org/chromium/chromium/src/+/master:media/learning/impl/learning_session_impl.cc;drc=ab84faeac34f74b7f640429afa59ed63d4e6cb1a;l=95

### [Deleted User] (2020-12-23)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### li...@google.com (2020-12-23)

https://chromium-review.googlesource.com/c/chromium/src/+/2602258


### [Deleted User] (2020-12-23)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c4225c3f308312a28342f1e162f0fa2d1890ac4d

commit c4225c3f308312a28342f1e162f0fa2d1890ac4d
Author: Frank Liberato <liberato@chromium.org>
Date: Wed Dec 23 20:08:14 2020

Added missing weak ptr null check.

WeakLearningSessionImpl::PredictDistribution accessed the session,
without first checking if its weak ptr was valid.  This CL adds that
wp check.

Bug: 1159663
Change-Id: I2c26fd8cb22cd2c78d39267e58e8b79217cee1c3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2602258
Reviewed-by: Ted Meyer <tmathmeyer@chromium.org>
Commit-Queue: Frank Liberato <liberato@chromium.org>
Cr-Commit-Position: refs/heads/master@{#839165}

[modify] https://crrev.com/c4225c3f308312a28342f1e162f0fa2d1890ac4d/media/learning/impl/learning_session_impl.cc


### li...@google.com (2020-12-23)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-24)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-24)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-13)

From the original description this seems to impact M88, so altering labels such that sheriffbot will (hopefully) ask to merge this back to M88.

### am...@google.com (2021-01-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-01-14)

Congratulations! The VRP panel has decided to award you $15,000 for this report! Great job and thank you!

### ad...@google.com (2021-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-14)

Requesting merge to beta M88 because latest trunk commit (839165) appears to be after beta branch point (827102).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-01-14)

This bug requires manual review: We are only 4 days from stable.
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
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### li...@google.com (2021-01-14)

1. Does your merge fit within the Merge Decision Guidelines?

  yes -- very safe fix, security issue.

2. Links to the CLs you are requesting to merge.

  https://chromium-review.googlesource.com/c/chromium/src/+/2602258

3. Has the change landed and been verified on ToT?

  yes.

4. Does this change need to be merged into other active release branches (M-1, M+1)?

  no.

5. Why are these changes required in this milestone after branch?

  sheriffbot auto-requested it.

6. Is this a new feature?

  no.

7. If it is a new feature, is it behind a flag using finch?

  n/a.


### sr...@google.com (2021-01-14)

adetaylor@ can u review , and see if this can wait for next re-spin or do we need to take it to final build?

### ad...@google.com (2021-01-14)

I'm approving merge to M88, branch 4324. Obviously it'd be nice if we can get this into the build tomorrow, but if the merge doesn't land in time, and we end up releasing it two weeks later that's OK.

### sr...@google.com (2021-01-15)

Created a CP here - https://chromium-review.googlesource.com/c/chromium/src/+/2631348 for merge to 4324 branch and put through CQ in the interest of time

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cf7ec42354d9ab6c8947febff00405c58c5a2f1e

commit cf7ec42354d9ab6c8947febff00405c58c5a2f1e
Author: Frank Liberato <liberato@chromium.org>
Date: Fri Jan 15 10:35:53 2021

Added missing weak ptr null check.

WeakLearningSessionImpl::PredictDistribution accessed the session,
without first checking if its weak ptr was valid.  This CL adds that
wp check.

(cherry picked from commit c4225c3f308312a28342f1e162f0fa2d1890ac4d)

Bug: 1159663
Change-Id: I2c26fd8cb22cd2c78d39267e58e8b79217cee1c3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2602258
Reviewed-by: Ted Meyer <tmathmeyer@chromium.org>
Commit-Queue: Frank Liberato <liberato@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#839165}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2631348
Reviewed-by: Srinivas Sista <srinivassista@chromium.org>
Commit-Queue: Ben Mason <benmason@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#1763}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/cf7ec42354d9ab6c8947febff00405c58c5a2f1e/media/learning/impl/learning_session_impl.cc


### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-01-05)

Hello OP/emilykim@, we consider attachments/pocs included with reports to be an integral part of the report (https://bughunters.google.com/about/rules/5745167867576320), so I've undeleted them. Thank you! 

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1159663?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### ap...@google.com (2024-03-22)

Project: chromium/src
Branch: master

commit c4225c3f308312a28342f1e162f0fa2d1890ac4d
Author: Frank Liberato <liberato@chromium.org>
Date:   Wed Dec 23 20:08:14 2020

    Added missing weak ptr null check.
    
    WeakLearningSessionImpl::PredictDistribution accessed the session,
    without first checking if its weak ptr was valid.  This CL adds that
    wp check.
    
    Bug: 1159663
    Change-Id: I2c26fd8cb22cd2c78d39267e58e8b79217cee1c3
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2602258
    Reviewed-by: Ted Meyer <tmathmeyer@chromium.org>
    Commit-Queue: Frank Liberato <liberato@chromium.org>
    Cr-Commit-Position: refs/heads/master@{#839165}

M       media/learning/impl/learning_session_impl.cc

https://chromium-review.googlesource.com/2602258


---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054195)*
